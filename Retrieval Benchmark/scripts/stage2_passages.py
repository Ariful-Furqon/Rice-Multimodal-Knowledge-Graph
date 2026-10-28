"""Stage 2: from a farmer's photo and question to the passages that answer it,
with and without the knowledge graph. Also writes the coverage table.

Query = (test image, question). Three question intents:
- cause:    "What causes this problem on my rice?"
- manage:   "How can I control or prevent it?"   (IRRI sheets put control and
            prevention in one section, so they are one intent here)
- identify: "Which symptoms confirm it?"

Two gold sets (binary relevance):
- section gold (main): the passages of the target's own IRRI fact sheet, in the
  section that answers the intent. The target -> fact sheet map (GOLD_DOCS) is
  written by hand, not taken from the graph, so it does not favour the KG route.
  Silver: no human judged these passages yet (plan, section 5.1).
- fact gold (strict): the passages linked by hasEvidencePassage to the target's
  facts of the intent's properties. Reported where it exists; it favours the
  KG route by construction.

Systems (stage 1 -> stage 2):
- no_kg:  linear probe top-1 -> bge-m3 search over all passages with
          "<condition label>: <question>".
- kg:     probe fused with the KG symptom prompts (weight tuned on dev) top-1 ->
          the condition's facts of the intent -> their linked passages, then the
          passages of the documents its facts cite (dcterms:source), then the
          rest; bge-m3 orders within each tier.
- oracle_*: the gold condition instead of the stage-1 prediction, to separate
          stage-1 errors from stage-2 errors.
- +rerank: OMGM step 3. A cross-encoder (bge-reranker-v2-m3) re-orders the top
          POOL passages of the ranking above with "<condition label>: <question>";
          the rest keep their order. On the KG route it re-orders within each tier,
          so passages the graph links stay first.
- topK+rerank: instead of trusting the stage-1 top-1, the top K conditions each
          bring their pool; a passage scores
          max over conditions e of  log p(e | image) + beta * (rerank(e, passage) + gamma * tier bonus),
          with the tier bonus 2 / 1 / 0 for KG tiers 0 / 1 / 2 (gamma = 0 without the KG).
          K, beta and gamma are tuned on dev (section gold, mean MRR over intents).

Queries: test images of the main subset (no single-source dataset) whose gold
target has section gold for the intent.

    <venv python> -I stage2_passages.py <repo root> <out dir>
"""
import collections
import csv
import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
import rdflib

R = rdflib.Namespace("https://w3id.org/ricemmkg#")
DCT = rdflib.Namespace("http://purl.org/dc/terms/")
OWL = rdflib.OWL
SINGLE_SOURCE = {"NetrokonaRiceDataset", "YukeWbcDataset"}
OLLAMA = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"
RERANK_MODEL = "BAAI/bge-reranker-v2-m3"
POOL = 50
KS = (1, 3, 10)
LAMBDAS = (0, 0.5, 1, 2, 5, 10, 20, 50, 100)
TOPKS = (1, 2, 3, 5)
BETAS = (0.05, 0.1, 0.2, 0.5, 1, 2, 5)
GAMMAS = (0, 1, 2, 5, 10)

GOLD_DOCS = {
    "Bacterial_Leaf_Blight": ["IRRI_RKB_bacterial-blight"],
    "Bacterial_Leaf_Streak": ["IRRI_RKB_bacterial-leaf-streak"],
    "Brown_Planthopper": ["IRRI_RKB_planthopper"],
    "Brown_Spot": ["IRRI_RKB_brown-spot"],
    "Hispa": ["IRRI_RKB_rice-hispa"],
    "Leaf_Folder": ["IRRI_RKB_rice-leaffolder"],
    "Nitrogen_Deficiency_Disorder": ["IRRI_RKB_nitrogen"],
    "Phosphorus_Deficiency_Disorder": ["IRRI_RKB_phosphorus"],
    "Potassium_Deficiency_Disorder": ["IRRI_RKB_potassium-k"],
    "Rice_Blast_Disease": ["IRRI_RKB_blast-leaf-collar", "IRRI_RKB_blast-node-neck"],
    "Rice_Tungro_Disease": ["IRRI_RKB_tungro"],
    "Sheath_Blight": ["IRRI_RKB_sheath-blight"],
    "Stem_Borer": ["IRRI_RKB_stem-borer"],
}

INTENTS = {
    "cause": {"question": "What causes this problem on my rice?",
              "sections": ("What it does", "Why and where it occurs"),
              "props": [(R.causes, "in")]},
    "manage": {"question": "How can I control or prevent it?",
               "sections": ("How to manage", "Management principles"),
               "props": [(R.controlledBy, "out"), (R.preventedBy, "out"), (R.recommends, "out")]},
    "identify": {"question": "Which symptoms confirm it?",
                 "sections": ("How to identify",),
                 "props": [(R.indicatedBy, "out")]},
}


def local(term):
    return str(term).split("#")[-1]


def embed(texts):
    out = []
    for i in range(0, len(texts), 32):
        req = urllib.request.Request(OLLAMA, data=json.dumps(
            {"model": EMBED_MODEL, "input": texts[i:i + 32]}).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            out += json.load(r)["embeddings"]
    v = np.array(out)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def rerank_scores(pairs):
    """Cross-encoder logits for (query, passage) pairs."""
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(RERANK_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(RERANK_MODEL, dtype=torch.float16).cuda().eval()
    out = []
    with torch.no_grad():
        for i in range(0, len(pairs), 64):
            x = tok(pairs[i:i + 64], padding=True, truncation=True, max_length=512, return_tensors="pt").to("cuda")
            out += model(**x).logits.view(-1).float().tolist()
    return out


def log_softmax(x):
    x = x - x.max(1, keepdims=True)
    return x - np.log(np.exp(x).sum(1, keepdims=True))


def metrics(ranked, gold):
    """ranked: passage ids in order; gold: set of passage ids."""
    hits = [p in gold for p in ranked]
    first = hits.index(True) + 1 if any(hits) else None
    out = {f"Hit@{k}": float(any(hits[:k])) for k in KS}
    out["MRR"] = 1.0 / first if first else 0.0
    dcg = sum(1 / np.log2(i + 2) for i, h in enumerate(hits[:10]) if h)
    idcg = sum(1 / np.log2(i + 2) for i in range(min(len(gold), 10)))
    out["nDCG@10"] = dcg / idcg
    out["Recall@10"] = sum(hits[:10]) / len(gold)
    return out


def main(root, out_dir):
    root, out_dir = Path(root), Path(out_dir)
    g = rdflib.Graph()
    g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
    text = rdflib.Graph()
    text.parse(root / "Text Modality/RiceMMKG_IRRI_text.ttl")

    passages = sorted(g.subjects(rdflib.RDF.type, R.TextPassage))
    pid = [local(p) for p in passages]
    p_doc = {local(p): local(g.value(p, R.inDocument)) for p in passages}
    p_sec = {local(p): str(g.value(p, R.sectionTitle) or "") for p in passages}
    p_text = [str(text.value(p, R.passageText)) for p in passages]
    doc_url = {local(d): str(g.value(d, DCT.source)) for d in g.subjects(rdflib.RDF.type, R.TextDocument)}
    url_doc = {u: d for d, u in doc_url.items()}

    axioms = []
    for a in g.subjects(rdflib.RDF.type, OWL.Axiom):
        axioms.append((g.value(a, OWL.annotatedSource), g.value(a, OWL.annotatedProperty),
                       g.value(a, OWL.annotatedTarget), {local(x) for x in g.objects(a, R.hasEvidencePassage)},
                       {str(x) for x in g.objects(a, DCT.source)}))

    def facts(target, intent):
        node = R[target]
        out = []
        for s, p, o, ps, src in axioms:
            for prop, d in INTENTS[intent]["props"]:
                if p == prop and ((d == "out" and s == node) or (d == "in" and o == node)):
                    out.append((ps, src))
        return out

    def section_gold(target, intent):
        secs = INTENTS[intent]["sections"]
        return {p for p in pid if p_doc[p] in GOLD_DOCS.get(target, []) and p_sec[p].startswith(secs)}

    def fact_gold(target, intent):
        return set().union(*[ps for ps, _ in facts(target, intent)]) if facts(target, intent) else set()

    stage1 = np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)
    entities = list(stage1["entities"])
    with (root / "Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8") as f:
        gold_of = {r["image"]: r["gold"] for r in csv.DictReader(f)}
    with (root / "Retrieval Benchmark/splits/images_split.csv").open(encoding="utf-8") as f:
        ds_of = {r["image"]: r["dataset"] for r in csv.DictReader(f)}

    # coverage table
    test_imgs = [i for i in stage1["test_images"] if ds_of[i] not in SINGLE_SOURCE]
    photos = collections.Counter(gold_of[i] for i in test_imgs)
    coverage = {}
    for e in entities:
        row = {"test_photos": photos.get(e, 0), "fact_sheet": ", ".join(GOLD_DOCS.get(e, [])) or "none"}
        for it in INTENTS:
            fs = facts(e, it)
            row[it] = {"facts": len(fs), "facts_with_sentence": sum(bool(ps) for ps, _ in fs),
                       "section_passages": len(section_gold(e, it))}
        coverage[e] = row

    # stage 1: fuse probe with KG prompts, weight tuned on dev (main subset)
    def main_mask(images):
        return np.array([ds_of[i] not in SINGLE_SOURCE for i in images])
    e_idx = {e: i for i, e in enumerate(entities)}
    dm = main_mask(stage1["dev_images"])
    dev_gold = np.array([e_idx[gold_of[i]] for i in stage1["dev_images"]])[dm]

    def zs(x):
        return (x - x.mean(1, keepdims=True)) / x.std(1, keepdims=True)
    acc = {lam: float(np.mean(np.argmax(zs(stage1["dev_linear_probe"][dm]) + lam * zs(stage1["dev_clip_kg"][dm]), 1)
                              == dev_gold)) for lam in LAMBDAS}
    best = max(acc, key=acc.get)
    print("dev R@1 by KG weight:", acc, "-> chosen", best)
    tm = main_mask(stage1["test_images"])
    t_imgs = list(np.array(stage1["test_images"])[tm])
    t_gold = np.array([e_idx[gold_of[i]] for i in t_imgs])
    pred = {"no_kg": np.argmax(stage1["test_linear_probe"][tm], 1),
            "kg": np.argmax(zs(stage1["test_linear_probe"][tm]) + best * zs(stage1["test_clip_kg"][tm]), 1),
            "oracle": t_gold}
    stage1_r1 = {k: float(np.mean(v == t_gold)) for k, v in pred.items()}
    print("test R@1 stage 1:", stage1_r1)

    # stage 2
    p_emb = embed(p_text)
    label = {e: str(g.value(R[e], rdflib.RDFS.label) or e.replace("_", " ")) for e in entities}
    q_text = {(e, it): f"{label[e]}: {INTENTS[it]['question']}" for e in entities for it in INTENTS}
    keys = list(q_text)
    q_emb = dict(zip(keys, embed([q_text[k] for k in keys])))

    def dense(e, it):
        s = p_emb @ q_emb[(e, it)]
        return [pid[i] for i in np.argsort(-s)], s

    def kg_tier(e, it):
        fs = facts(e, it)
        linked = set().union(*[ps for ps, _ in fs]) if fs else set()
        cited = {url_doc[u] for _, src in fs for u in src if u in url_doc}
        return {p: 0 if p in linked else 1 if p_doc[p] in cited else 2 for p in pid}

    def kg_route(e, it):
        tier = kg_tier(e, it)
        return sorted(dense(e, it)[0], key=lambda p: tier[p])

    base = {}
    for e in entities:
        for it in INTENTS:
            base[("dense", e, it)] = dense(e, it)[0]
            base[("kg_route", e, it)] = kg_route(e, it)

    # step 3: cross-encoder over the top POOL of either ranking (one batch for all)
    rr_keys = sorted({(e, it, p) for (_, e, it), order in base.items() for p in order[:POOL]})
    p_index = {p: i for i, p in enumerate(pid)}
    print(f"reranking {len(rr_keys)} (condition, intent, passage) pairs", flush=True)
    rr_vals = rerank_scores([[q_text[(e, it)], p_text[p_index[p]]] for e, it, p in rr_keys])
    rr = dict(zip(rr_keys, rr_vals))

    # the KG route keeps its tiers: the reranker orders passages within a tier only
    tiers = {(e, it): kg_tier(e, it) for e in entities for it in INTENTS}
    for e in entities:
        for it in INTENTS:
            order = base[("dense", e, it)]
            base[("dense+rerank", e, it)] = sorted(order[:POOL], key=lambda p: -rr[(e, it, p)]) + order[POOL:]
            order, t = base[("kg_route", e, it)], tiers[(e, it)]
            base[("kg_route+rerank", e, it)] = sorted(order[:POOL], key=lambda p: (t[p], -rr[(e, it, p)])) + order[POOL:]

    def topk_rank(logp_row, k, beta, b, it, gamma=0.0):
        """Passages from the top-k conditions' pools, scored by
        stage-1 log p + beta * (rerank + gamma * KG tier bonus); the bonus is 2, 1, 0 for tiers 0, 1, 2."""
        top = np.argsort(-logp_row)[:k]
        score = {}
        for ei in top:
            e = entities[ei]
            t = tiers[(e, it)]
            for p in base[(b, e, it)][:POOL]:
                s = logp_row[ei] + beta * (rr[(e, it, p)] + gamma * (2 - t[p]))
                if s > score.get(p, -np.inf):
                    score[p] = s
        head = sorted(score, key=lambda p: -score[p])
        return head + [p for p in base[(b, entities[top[0]], it)] if p not in score]

    # stage-1 log p(condition | image): the probe gives log-probabilities; the fused score is put
    # through a softmax so both systems use the same form
    logp = {"test": {"no_kg": stage1["test_linear_probe"][tm],
                     "kg": log_softmax(zs(stage1["test_linear_probe"][tm]) + best * zs(stage1["test_clip_kg"][tm]))},
            "dev": {"no_kg": stage1["dev_linear_probe"][dm],
                    "kg": log_softmax(zs(stage1["dev_linear_probe"][dm]) + best * zs(stage1["dev_clip_kg"][dm]))}}

    def dev_mrr(s1, b, k, beta, gamma):
        vals = []
        for it in INTENTS:
            for row, gi in zip(logp["dev"][s1], dev_gold):
                gold = section_gold(entities[gi], it)
                if gold:
                    vals.append(metrics(topk_rank(row, k, beta, b, it, gamma), gold)["MRR"])
        return float(np.mean(vals))

    topk_dev, topk_best = {}, {}
    for s1, b, gammas in (("no_kg", "dense", (0,)), ("kg", "kg_route", GAMMAS)):
        grid = {(k, beta, gm): dev_mrr(s1, b, k, beta, gm) for k in TOPKS for beta in BETAS for gm in gammas}
        topk_best[s1] = max(grid, key=grid.get)
        topk_dev[s1] = {f"K={k} beta={beta} gamma={gm}": v for (k, beta, gm), v in grid.items()}
        print(f"dev MRR top-k {s1}: best K, beta, gamma = {topk_best[s1]} ({grid[topk_best[s1]]:.3f})", flush=True)

    systems = {"no_kg": ("no_kg", "dense"), "kg": ("kg", "kg_route"),
               "no_kg_stage1+kg_route": ("no_kg", "kg_route"),
               "no_kg+rerank": ("no_kg", "dense+rerank"), "kg+rerank": ("kg", "kg_route+rerank"),
               "no_kg top-k+rerank": ("no_kg", "topk:dense"), "kg top-k+rerank": ("kg", "topk:kg_route"),
               "oracle+dense": ("oracle", "dense"), "oracle+kg_route": ("oracle", "kg_route"),
               "oracle+dense+rerank": ("oracle", "dense+rerank"), "oracle+kg_route+rerank": ("oracle", "kg_route+rerank")}
    results = {}
    for name, (s1, s2) in systems.items():
        res = {}
        for it in INTENTS:
            for gname, gfun in (("section", section_gold), ("fact", fact_gold)):
                rows = []
                for img_i, gi in enumerate(t_gold):
                    gold = gfun(entities[gi], it)
                    if not gold:
                        continue
                    if s2.startswith("topk:"):
                        k, beta, gm = topk_best[s1]
                        ranked = topk_rank(logp["test"][s1][img_i], k, beta, s2[5:], it, gm)
                    else:
                        ranked = base[(s2, entities[pred[s1][img_i]], it)]
                    rows.append(metrics(ranked, gold))
                if rows:
                    res[f"{it}/{gname}"] = {m: float(np.mean([r[m] for r in rows])) for m in rows[0]} | {"n": len(rows)}
        results[name] = res

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "stage2_results.json").write_text(json.dumps(
        {"embed_model": EMBED_MODEL, "rerank_model": RERANK_MODEL, "rerank_pool": POOL,
         "kg_weight_dev": acc, "kg_weight": best, "stage1_test_R@1": stage1_r1,
         "topk_dev_mrr": topk_dev,
         "topk_chosen": {s: {"K": kb[0], "beta": kb[1], "gamma": kb[2]} for s, kb in topk_best.items()},
         "intents": {k: {"question": v["question"], "sections": v["sections"]} for k, v in INTENTS.items()},
         "coverage": coverage, "results": results}, indent=1), encoding="utf-8")

    lines = ["Coverage (main test photos; facts / facts with a linked sentence / section passages per intent)", "",
             "| Target | Test photos | Fact sheet | cause | manage | identify |", "|---|---:|---|---|---|---|"]
    for e, r in coverage.items():
        cells = [f"{r[it]['facts']} / {r[it]['facts_with_sentence']} / {r[it]['section_passages']}" for it in INTENTS]
        lines.append(f"| {e} | {r['test_photos']} | {r['fact_sheet']} | " + " | ".join(cells) + " |")
    lines += ["", f"Stage 1 R@1 on the main test subset: " +
              ", ".join(f"{k} {v:.3f}" for k, v in stage1_r1.items()) + f" (KG weight {best}, tuned on dev)", "",
              f"Reranker {RERANK_MODEL} over the top {POOL}. Top-k propagation, tuned on dev: " +
              ", ".join(f"{s} K={kb[0]} beta={kb[1]} gamma={kb[2]}" for s, kb in topk_best.items()), ""]
    for gname in ("section", "fact"):
        lines += [f"Stage 2, {gname} gold", "",
                  "| System | Intent | n | MRR | Hit@1 | Hit@3 | Hit@10 | nDCG@10 | Recall@10 |",
                  "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
        for name, res in results.items():
            for it in INTENTS:
                r = res.get(f"{it}/{gname}")
                if r:
                    lines.append(f"| {name} | {it} | {r['n']} | {r['MRR']:.3f} | {r['Hit@1']:.3f} | {r['Hit@3']:.3f} "
                                 f"| {r['Hit@10']:.3f} | {r['nDCG@10']:.3f} | {r['Recall@10']:.3f} |")
        lines.append("")
    (out_dir / "stage2_results.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:3])
