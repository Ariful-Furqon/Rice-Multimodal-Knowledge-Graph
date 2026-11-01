"""Step 2, part 2: re-rank the stage-1 conditions with the VLM's symptom triples
(step2_vlm_triples.py), matched against the KG. This is checkpoint 1 of the plan:
step 2 must raise entity R@1 over step 1 alone, cross-source too.

Stage 1 is the linear probe on CLIP features, in two protocols:
- in-source:    trained on the train split.
- cross-source: for each dataset, trained on the train split of the others. Only
                images whose target another dataset also has are scored.

KG score of condition e for one image, over the VLM's closed-vocabulary triples:
    kg(e) = sum over triples (s, part) with e indicatedBy s of
            confidence * idf(s) * (1 if the KG links s to part else PART_MISS)
idf(s) = log(n conditions / n conditions indicated by s), so a symptom that many
conditions share counts for little. A symptom repeated in one reply counts once, at
its highest confidence. Normal_Health has no symptoms in the KG: it gets the mean idf
when the VLM reports no triples, as if one symptom matched.

Fusion: z(stage 1) + lambda * kg, over the stage-1 top 5 only (soft linking). The
other conditions keep their stage-1 order below the five. lambda is tuned on dev_core
(R@1), per protocol. test_core is used once, with the chosen weight.

Reported on the main subset (no single-source dataset) of test_core, with a paired
sign-flip test on per-image reciprocal rank against stage 1, and on the confusable
pairs of the plan (blast / brown spot, bacterial leaf blight / streak).

KGMEL baseline (design_v2.md, section 3): the VLM's open-vocabulary description and
triples plus the KG symptoms of the stage-1 top 5 go to a text LLM, which names one
condition. It moves to rank 1; the others keep their stage-1 order. Needs no tuning.
Answers are cached in <out dir>/kgmel_answers.jsonl.

    <venv python> -I step2_rerank.py <repo root> <closed triples.jsonl> <open triples.jsonl> <out dir>
"""
import collections
import csv
import json
import math
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
import rdflib
from sklearn.linear_model import LogisticRegression

R = rdflib.Namespace("https://w3id.org/ricemmkg#")
SINGLE_SOURCE = {"NetrokonaRiceDataset", "YukeWbcDataset"}
TOP = 5
PART_MISS = 0.5
LAMBDAS = (0, 0.1, 0.2, 0.5, 1, 2, 5, 10)
PERMUTATIONS = 10000
OLLAMA = "http://127.0.0.1:11434/api/chat"
LLM = "qwen2.5:7b"
PAIRS = {"blast / brown spot": {"Rice_Blast_Disease", "Brown_Spot"},
         "BLB / BLS": {"Bacterial_Leaf_Blight", "Bacterial_Leaf_Streak"}}


def local(term):
    return str(term).split("#")[-1]


def label(g, node):
    return str(g.value(node, rdflib.RDFS.label) or local(node).replace("_", " "))


def zs(x):
    x = np.where(np.isinf(x), np.nan, x)
    return np.nan_to_num((x - np.nanmean(x, 1, keepdims=True)) / np.nanstd(x, 1, keepdims=True), nan=-10.0)


def kg_scores(rows, entities, g):
    """(images, conditions) KG score, plus the share of triples outside the vocabulary."""
    sym_of = {e: {label(g, s).lower(): s for s in g.objects(R[e], R.indicatedBy)} for e in entities}
    df = collections.Counter(s for e in entities for s in sym_of[e])
    with_sym = sum(bool(sym_of[e]) for e in entities)
    idf = {s: math.log(with_sym / n) + 1e-3 for s, n in df.items()}
    mean_idf = float(np.mean(list(idf.values())))
    parts = collections.defaultdict(set)
    for s, p in g.subject_objects(R.affectsPlantPart):
        parts[s].add(label(g, p).lower())
    i_norm = entities.index("Normal_Health")

    out = np.zeros((len(rows), len(entities)))
    known = total = 0
    for i, r in enumerate(rows):
        best = {}
        for t in (r["parsed"] or {}).get("triples") or []:
            if not isinstance(t, dict):
                continue
            s = str(t.get("symptom", "")).lower()
            try:
                conf = float(t.get("confidence", 0.5))
            except (TypeError, ValueError):
                conf = 0.5
            if s not in best or conf > best[s][0]:
                best[s] = (conf, str(t.get("part", "")).lower())
        if not best:
            out[i, i_norm] = mean_idf
        for s, (conf, part) in best.items():
            total += 1
            known += s in df
            for j, e in enumerate(entities):
                if s in sym_of[e]:
                    out[i, j] += conf * idf[s] * (1 if part in parts[sym_of[e][s]] else PART_MISS)
    return out, known / max(total, 1)


def fuse(stage1, kg, lam):
    """Stage-1 order is kept outside the top 5; inside, z(stage 1) + lam * kg decides."""
    z = zs(stage1)
    top = np.argsort(-z, axis=1)[:, :TOP]
    out = z - 1000.0
    rows = np.arange(len(z))[:, None]
    out[rows, top] = z[rows, top] + lam * kg[rows, top]
    return out


def ranks(scores, gold):
    order = np.argsort(-scores, axis=1)
    return np.argmax(order == gold[:, None], axis=1) + 1


def summary(rank, gold):
    return {"n": len(rank), "R@1": float(np.mean(rank == 1)), "R@3": float(np.mean(rank <= 3)),
            "MRR": float(np.mean(1.0 / rank)),
            "macroR@1": float(np.mean([np.mean(rank[gold == c] == 1) for c in np.unique(gold)]))}


def sign_flip(a, b, seed=0):
    """Two-sided paired sign-flip test on reciprocal rank."""
    d = 1.0 / b - 1.0 / a
    if not d.any():
        return 1.0
    rng = np.random.default_rng(seed)
    flips = rng.choice((-1.0, 1.0), size=(PERMUTATIONS, len(d)))
    return float((np.sum(np.abs((flips * d).mean(1)) >= abs(d.mean()) - 1e-12) + 1) / (PERMUTATIONS + 1))


def llm_choice(prompt, n):
    body = {"model": LLM, "stream": False, "format": "json", "options": {"temperature": 0, "seed": 0, "num_predict": 40},
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(OLLAMA, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                raw = json.load(r)["message"]["content"]
            break
        except OSError:  # urllib's errors; the local server fails briefly now and then
            if attempt == 4:
                raise
            time.sleep(10 * (attempt + 1))
    try:
        k = int(json.loads(raw)["answer"])
    except (ValueError, KeyError, TypeError):
        return 1
    return k if 1 <= k <= n else 1


def kgmel_prompt(rec, candidates, entities, g):
    parsed = rec["parsed"] or {}
    seen = "; ".join(" ".join(str(t.get(k, "")) for k in ("subject", "relation", "object"))
                     for t in parsed.get("triples") or [] if isinstance(t, dict))
    lines = []
    for k, c in enumerate(candidates, 1):
        e = entities[c]
        sym = sorted(label(g, s) for s in g.objects(R[e], R.indicatedBy))
        lines.append(f"{k}. {label(g, R[e])}: " + (", ".join(sym) if sym else "healthy plant, no symptoms"))
    return (f"A rice photo was described as: {parsed.get('description', '')}\nObserved: {seen}\n\n"
            "Candidates and their known symptoms:\n" + "\n".join(lines) +
            '\n\nWhich candidate fits best? Reply with JSON only: {"answer": <candidate number>}')


def main(root, triples, open_triples, out_dir):
    root, out_dir = Path(root), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    g = rdflib.Graph()
    g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
    with (root / "Retrieval Benchmark/splits/images_split.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with (root / "Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8") as f:
        gold_of = {r["image"]: r["gold"] for r in csv.DictReader(f)}
    stage1 = np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)
    entities = [str(e) for e in stage1["entities"]]
    e_idx = {e: i for i, e in enumerate(entities)}
    data = np.load(root / "Data/retrieval/feats_clip-l14.npz", allow_pickle=True)
    assert list(data["urls"]) == [r["url"] for r in rows]
    feats = data["feats"]
    row_of = {r["image"]: i for i, r in enumerate(rows)}
    split = np.array([r["split"] for r in rows])
    dataset = np.array([r["dataset"] for r in rows])
    gold_all = np.array([e_idx[gold_of[r["image"]]] for r in rows])

    vlm = [json.loads(x) for x in Path(triples).read_text(encoding="utf-8").splitlines()]
    vlm = [r for r in vlm if r["image"] in row_of]
    idx = np.array([row_of[r["image"]] for r in vlm])
    kg, known = kg_scores(vlm, entities, g)
    parse_ok = float(np.mean([r["parsed"] is not None for r in vlm]))
    healthy = np.array([not (r["parsed"] or {}).get("triples") for r in vlm])
    print(f"{len(vlm)} images; parsed {parse_ok:.3f}; triples in vocabulary {known:.3f}; "
          f"no triples {healthy.mean():.3f}", flush=True)

    def probe(train_mask, query):
        lr = LogisticRegression(max_iter=2000, C=1.0).fit(feats[train_mask], gold_all[train_mask])
        out = np.full((len(query), len(entities)), -np.inf)
        out[:, lr.classes_] = lr.predict_log_proba(feats[query])
        return out

    train = split == "train"
    s1 = {"in-source": probe(train, idx), "cross-source": np.full((len(idx), len(entities)), -np.inf)}
    usable = {"in-source": np.ones(len(idx), bool), "cross-source": np.zeros(len(idx), bool)}
    for held in sorted(set(dataset[idx])):
        gal = train & (dataset != held)
        qm = (dataset[idx] == held) & np.isin(gold_all[idx], np.unique(gold_all[gal]))
        if qm.any():
            s1["cross-source"][qm] = probe(gal, idx[qm])
            usable["cross-source"][qm] = True

    gold = gold_all[idx]
    is_dev = split[idx] == "dev"
    main_q = ~np.isin(dataset[idx], list(SINGLE_SOURCE))
    open_of = {r["image"]: r for r in map(json.loads, Path(open_triples).read_text(encoding="utf-8").splitlines())}
    cache_path = out_dir / "kgmel_answers.jsonl"
    cache = {}
    if cache_path.exists():
        cache = {(c["protocol"], c["image"]): c["answer"]
                 for c in map(json.loads, cache_path.read_text(encoding="utf-8").splitlines())}
    results, per_ds, tuned = {}, {}, {}
    for proto, sc in s1.items():
        m = usable[proto] & main_q
        dev, test = m & is_dev, m & ~is_dev
        grid = {lam: float(np.mean(ranks(fuse(sc[dev], kg[dev], lam), gold[dev]) == 1)) for lam in LAMBDAS}
        lam = max(LAMBDAS, key=lambda v: (grid[v], -v))
        tuned[proto] = {"lambda": lam, "dev_R@1": grid}
        base = ranks(fuse(sc[test], kg[test], 0), gold[test])
        new = ranks(fuse(sc[test], kg[test], lam), gold[test])
        results[proto] = {"stage 1": summary(base, gold[test]), "stage 1 + KG triples": summary(new, gold[test]),
                          "p": sign_flip(base, new)}
        test_i = np.nonzero(test)[0]
        order = np.argsort(-zs(sc[test]), axis=1)
        kgmel = []
        with cache_path.open("a", encoding="utf-8") as f:
            for row, i in enumerate(test_i):
                image, top = vlm[i]["image"], order[row][:TOP]
                if (proto, image) not in cache:
                    cache[(proto, image)] = llm_choice(kgmel_prompt(open_of[image], top, entities, g), TOP)
                    f.write(json.dumps({"protocol": proto, "image": image, "answer": cache[(proto, image)]}) + "\n")
                first = top[cache[(proto, image)] - 1]
                kgmel.append(1 + list(c for c in [first] + [x for x in order[row] if x != first]).index(gold[i]))
        kgmel = np.array(kgmel)
        results[proto]["KGMEL baseline"] = summary(kgmel, gold[test])
        results[proto]["p KGMEL"] = sign_flip(base, kgmel)
        names = np.array(entities)[gold[test]]
        for pair, members in PAIRS.items():
            pm = np.isin(names, list(members))
            if pm.any():
                results[proto][pair] = {"stage 1": summary(base[pm], gold[test][pm]),
                                        "stage 1 + KG triples": summary(new[pm], gold[test][pm]),
                                        "KGMEL baseline": summary(kgmel[pm], gold[test][pm])}
        ds = dataset[idx][test]
        per_ds[proto] = {d: {"n": int((ds == d).sum()), "stage 1": float(np.mean(base[ds == d] == 1)),
                             "stage 1 + KG triples": float(np.mean(new[ds == d] == 1)),
                             "KGMEL baseline": float(np.mean(kgmel[ds == d] == 1))} for d in sorted(set(ds))}

    res = {"images": len(vlm), "parsed": parse_ok, "triples_in_vocabulary": known,
           "no_triples": float(healthy.mean()), "tuned": tuned, "results": results, "per_dataset": per_ds}
    (out_dir / "step2_results.json").write_text(json.dumps(res, indent=1), encoding="utf-8")

    lines = [f"Step 2 on test_core, main subset. {len(vlm)} VLM runs (test_core + dev_core): parsed {parse_ok:.3f}, "
             f"triples in vocabulary {known:.3f}, no triples {healthy.mean():.3f}.", "",
             "| Protocol | System | n | R@1 | macro R@1 | R@3 | MRR | p (MRR) |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for proto, r in results.items():
        for name, pk in (("stage 1", None), ("stage 1 + KG triples", "p"), ("KGMEL baseline", "p KGMEL")):
            v = r[name]
            p = f"{r[pk]:.3f}" if pk else ""
            lines.append(f"| {proto} | {name} | {v['n']} | {v['R@1']:.3f} | {v['macroR@1']:.3f} | {v['R@3']:.3f} "
                         f"| {v['MRR']:.3f} | {p} |")
    lines += ["", "Lambda tuned on dev_core: " + ", ".join(f"{p} {t['lambda']}" for p, t in tuned.items()), "",
              "Confusable pairs (R@1, photos of the two conditions only):", "",
              "| Protocol | Pair | n | Stage 1 | Stage 1 + KG triples | KGMEL baseline |", "|---|---|---:|---:|---:|---:|"]
    for proto, r in results.items():
        for pair in PAIRS:
            if pair in r:
                lines.append(f"| {proto} | {pair} | {r[pair]['stage 1']['n']} | {r[pair]['stage 1']['R@1']:.3f} "
                             f"| {r[pair]['stage 1 + KG triples']['R@1']:.3f} | {r[pair]['KGMEL baseline']['R@1']:.3f} |")
    lines += ["", "Per dataset (R@1):", "", "| Protocol | Dataset | n | Stage 1 | Stage 1 + KG triples | KGMEL baseline |",
              "|---|---|---:|---:|---:|---:|"]
    for proto, ds in per_ds.items():
        for d, v in ds.items():
            lines.append(f"| {proto} | {d} | {v['n']} | {v['stage 1']:.3f} | {v['stage 1 + KG triples']:.3f} | {v['KGMEL baseline']:.3f} |")
    (out_dir / "step2_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:5])
