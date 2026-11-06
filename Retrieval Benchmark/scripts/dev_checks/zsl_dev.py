"""KG-based generalized zero-shot recognition, dev only: is the KG worth anything for a
condition with no training photo?

Leave one condition out: for each condition u with dev main photos, train on the train
photos of the other 16 and score all 17 on dev. u's dev photos measure the unseen class
(GZSL: u competes with the 16 seen classes, no calibration); the other dev main photos
measure the cost on seen classes.

Model: s(x, c) = (W x) . phi(c), W trained with cross-entropy over the seen classes on
standardised CLIP ViT-L/14 image features. Class representations phi(c):
  kg          multi-hot over the condition's domain triples in the query-time graph,
              (direction, relation, neighbour), plus 2 hops symptom -> plant part, plus
              its rdf:type; idf-weighted, L2-normalised
  kg-shuffled kg rows permuted among the conditions (control: same vectors, wrong class)
  label-text  CLIP text embedding of the label prompt (no KG: the name only)
  kg-text     mean CLIP text embedding of the label prompt and one prompt per KG symptom
              (as clip_kg in stage1_baselines.py)
  kg + label  kg concatenated with label-text
plus CLIP zero-shot with label-text and kg-text (no training, image . text).

The KG effect on unseen classes is kg - kg-shuffled, and kg-text - label-text.
Text embeddings are cached in Data/retrieval/text_emb_zsl.npz (needs openai/clip-vit-large-patch14
once; runs on CPU).

    <venv python> -I zsl_dev.py <repo root> <out .md>
"""
import collections
import csv
import json
import sys
from pathlib import Path

import numpy as np
import rdflib
import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ikrl_v2_dev import DOMAIN, SINGLE_SOURCE  # noqa: E402

R = rdflib.Namespace("https://w3id.org/ricemmkg#")
SEEDS = range(3)


def local(t):
    return str(t).split("#")[-1]


def label_of(g, node):
    lab = g.value(node, rdflib.RDFS.label)
    return str(lab) if lab else local(node).replace("_", " ")


def kg_vectors(g, ents):
    feats = collections.defaultdict(set)
    for e in ents:
        n = R[e]
        for p in DOMAIN:
            for o in g.objects(n, R[p]):
                feats[e].add(f"out:{p}:{local(o)}")
                if p == "indicatedBy":
                    for part in g.objects(o, R.affectsPlantPart):
                        feats[e].add(f"symptomPart:{local(part)}")
            for s in g.subjects(R[p], n):
                feats[e].add(f"in:{p}:{local(s)}")
        for t in g.objects(n, rdflib.RDF.type):
            if str(t).startswith(str(R)):
                feats[e].add(f"type:{local(t)}")
        if not any(f.startswith("out:indicatedBy") for f in feats[e]):
            feats[e].add("noSymptom")
    vocab = sorted({f for fs in feats.values() for f in fs})
    col = {f: j for j, f in enumerate(vocab)}
    x = np.zeros((len(ents), len(vocab)), np.float32)
    for i, e in enumerate(ents):
        for f in feats[e]:
            x[i, col[f]] = 1
    idf = np.log(len(ents) / x.sum(0)) + 0.1
    x = x * idf
    return x / np.linalg.norm(x, axis=1, keepdims=True), vocab


def text_vectors(g, ents, cache):
    if cache.exists():
        d = np.load(cache, allow_pickle=True)
        if list(d["ents"]) == ents:
            return d["label"], d["kg"]
    from transformers import CLIPModel, CLIPProcessor
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14").eval()
    proc = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

    @torch.no_grad()
    def enc(texts):
        x = proc(text=texts, return_tensors="pt", padding=True, truncation=True)
        f = model.text_projection(model.text_model(**x).pooler_output)
        return nn.functional.normalize(f, dim=-1).numpy()

    lab, kg = [], []
    for e in ents:
        first = "a photo of a healthy rice plant" if e == "Normal_Health" else f"a photo of a rice plant with {label_of(g, R[e])}"
        sym = sorted(label_of(g, s) for s in g.objects(R[e], R.indicatedBy))
        t = enc([first] + [f"a photo of a rice plant showing {s.lower()}" for s in sym])
        lab.append(t[0]); m = t.mean(0); kg.append(m / np.linalg.norm(m))
    np.savez(cache, ents=np.array(ents, dtype=object), label=np.array(lab), kg=np.array(kg))
    return np.array(lab), np.array(kg)


def fit(x_tr, y_tr, x_va, y_va, phi, seen, seed, epochs=300):
    torch.manual_seed(seed)
    W = nn.Linear(x_tr.shape[1], phi.shape[1], bias=False)
    scale = nn.Parameter(torch.tensor(10.0))
    opt = torch.optim.Adam(list(W.parameters()) + [scale], lr=1e-3, weight_decay=1e-4)
    P = torch.tensor(phi[seen]); remap = {c: i for i, c in enumerate(seen)}
    yt = torch.tensor([remap[c] for c in y_tr]); yv = torch.tensor([remap[c] for c in y_va])
    best, state = -1.0, None
    for _ in range(epochs):
        opt.zero_grad()
        nn.functional.cross_entropy(scale * nn.functional.normalize(W(x_tr), dim=1) @ P.T, yt).backward()
        opt.step()
        with torch.no_grad():
            acc = ((nn.functional.normalize(W(x_va), dim=1) @ P.T).argmax(1) == yv).float().mean().item()
        if acc > best:
            best, state = acc, (W.weight.detach().clone())
    W.weight.data = state
    return lambda x: (nn.functional.normalize(W(torch.tensor(x)), dim=1) @ torch.tensor(phi).T).detach().numpy()


def ranks(s, gold):
    return (s > s[np.arange(len(gold)), gold][:, None]).sum(1) + 1


def main(root, out_md):
    root = Path(root)
    rows = list(csv.DictReader((root / "Retrieval Benchmark/splits/images_split.csv").open(encoding="utf-8")))
    with (root / "Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8") as f:
        gold_of = {r["image"]: r["gold"] for r in csv.DictReader(f)}
    ents = [str(e) for e in np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)["entities"]]
    e_idx = {e: i for i, e in enumerate(ents)}
    data = np.load(root / "Data/retrieval/feats_clip-l14.npz", allow_pickle=True)
    assert list(data["urls"]) == [r["url"] for r in rows]
    raw = data["feats"].astype(np.float32)
    split = np.array([r["split"] for r in rows]); ds = np.array([r["dataset"] for r in rows])
    group = np.array([r["group"] for r in rows]); gold = np.array([e_idx[gold_of[r["image"]]] for r in rows])

    g = rdflib.Graph(); g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
    kg, vocab = kg_vectors(g, ents)
    lab_t, kg_t = text_vectors(g, ents, root / "Data/retrieval/text_emb_zsl.npz")
    sim = kg @ kg.T
    print(f"kg vectors: {len(vocab)} features; mean off-diagonal cosine {sim[~np.eye(len(ents), dtype=bool)].mean():.3f}", flush=True)
    perm = np.random.default_rng(0).permutation(len(ents))
    while (perm == np.arange(len(ents))).any():
        perm = np.random.default_rng(int(perm[0]) + 1).permutation(len(ents))
    reps = {"kg": kg, "kg-shuffled": kg[perm], "label-text": lab_t, "kg-text": kg_t,
            "kg + label": np.hstack([kg, lab_t]) / np.sqrt(2)}

    rng = np.random.default_rng(0)
    ug = np.unique(group[split == "train"])
    is_val = np.isin(group, list(rng.choice(ug, size=len(ug) // 10, replace=False))) & (split == "train")
    fit_m, dev = (split == "train") & ~is_val, (split == "dev") & ~np.isin(ds, list(SINGLE_SOURCE))
    mu, sd = raw[fit_m].mean(0), raw[fit_m].std(0) + 1e-6
    X = (raw - mu) / sd

    held_out = [c for c in range(len(ents)) if (dev & (gold == c)).any()]
    out = collections.defaultdict(lambda: collections.defaultdict(list))  # method -> class -> [ (unseen rank array, seen R@1) ]
    for u in held_out:
        seen = [c for c in range(len(ents)) if c != u]
        tr, va = fit_m & (gold != u), is_val & (gold != u)
        qu, qs = dev & (gold == u), dev & (gold != u)
        for name, t in (("zero-shot label-text", lab_t), ("zero-shot kg-text", kg_t)):
            s = raw / np.linalg.norm(raw, axis=1, keepdims=True) @ t.T
            out[name][u].append((ranks(s[qu], gold[qu]), float(np.mean(ranks(s[qs], gold[qs]) == 1))))
        for name, phi in reps.items():
            for seed in SEEDS:
                score = fit(torch.tensor(X[tr]), gold[tr], torch.tensor(X[va]), gold[va], phi.astype(np.float32), seen, seed)
                su, ss = score(X[qu]), score(X[qs])
                out[name][u].append((ranks(su, gold[qu]), float(np.mean(ranks(ss, gold[qs]) == 1))))
        print(f"{ents[u]:28s} n={qu.sum():4d}  " + "  ".join(
            f"{m}: MRR {np.mean([np.mean(1 / r) for r, _ in out[m][u]]):.3f}" for m in ("kg", "kg-shuffled", "label-text", "kg-text")),
            flush=True)

    methods = list(out)
    def agg(m, f):
        return np.mean([np.mean([f(r) for r, _ in out[m][u]]) for u in held_out])
    lines = ["Generalized zero-shot, leave one condition out, dev main subset. Unseen metrics are the mean over the "
             f"{len(held_out)} held-out conditions (each condition weighted equally); the unseen class competes with the 16 "
             f"seen ones, without calibration. Chance MRR over 17 classes is {np.mean(1 / np.arange(1, 18)):.3f}. "
             f"{len(SEEDS)} seeds for trained methods. KG vectors: {len(vocab)} features. Script: `scripts/dev_checks/zsl_dev.py`.", "",
             "| Method | Unseen R@1 | Unseen R@3 | Unseen MRR | Seen R@1 |", "|---|---:|---:|---:|---:|"]
    for m in methods:
        seen_acc = np.mean([np.mean([s for _, s in out[m][u]]) for u in held_out])
        lines.append(f"| {m} | {agg(m, lambda r: np.mean(r == 1)):.3f} | {agg(m, lambda r: np.mean(r <= 3)):.3f} "
                     f"| {agg(m, lambda r: np.mean(1 / r)):.3f} | {seen_acc:.3f} |")
    lines += ["", "**Unseen MRR per held-out condition:**", "",
              "| Condition | n | " + " | ".join(methods) + " |", "|---|---:|" + "---:|" * len(methods)]
    for u in held_out:
        n = int((dev & (gold == u)).sum())
        lines.append(f"| {ents[u]} | {n} | " + " | ".join(f"{np.mean([np.mean(1 / r) for r, _ in out[m][u]]):.3f}" for m in methods) + " |")
    Path(out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    Path(out_md).with_suffix(".json").write_text(json.dumps(
        {m: {ents[u]: [float(np.mean(1 / r)) for r, _ in out[m][u]] for u in held_out} for m in methods}, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:3])
