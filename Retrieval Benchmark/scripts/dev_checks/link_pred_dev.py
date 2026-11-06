"""Link prediction with the photo's own edges, dev only (design_v2.md, section 9.3).

The supervisor's idea: keep the photo node, cut `annotatedAs`, and predict it from the
pixels and the photo's other edges. The edges come from the full graph
(Ontology/Rice MMKG.rdf), because the query-time graph drops every triple of a dev or
test photo.

Head: C of ikrl_v2_dev.py (linear + MLP distance to random frozen class vectors), which
equals the TransE head there. Input: standardised CLIP ViT-L/14 features, concatenated
with binary edge features (one-hot values plus a presence flag per edge).

Variants (cumulative where stated):
  1 pixels      none
  2 safe        recordedAtDate (presence + month), hasSpatialLocation, environmentCondition
  3 context     2 + plantAgeDays (one-hot days) + ofVariety
  4 dataset     2 + prov:wasDerivedFrom (one-hot)
  5 leaking     2 + sourceLabel, captures, and the folder name in schema:contentUrl

Every safe edge occurs in one or two datasets only, so its presence alone tells the
dataset (see the report). Split v2, early stopping on 10% of the train capture groups,
dev main subset, 5 seeds, in-source and cross-source (leave one dataset out).

    <venv python> -I link_pred_dev.py <repo root> <out .md>
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
from rdflib.namespace import PROV

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ikrl_v2_dev import DIM, SINGLE_SOURCE, fit, metrics  # noqa: E402

R = "https://w3id.org/ricemmkg#"
SDO = "http://schema.org/"
SEEDS = range(5)
VARIANTS = {"1 pixels": [], "2 safe": ["safe"], "3 + age, variety": ["safe", "context"],
            "4 + dataset": ["safe", "dataset"], "5 + leaking edges": ["safe", "leak"]}


def edge_features(g, images):
    """Binary feature blocks per photo: {block: (n, d) array}, plus their column names."""
    def objects(p):
        out = collections.defaultdict(list)
        for s, o in g.subject_objects(p):
            out[str(s)].append(o)
        return out

    def onehot(values_of, prefix):
        vocab = sorted({v for vs in values_of for v in vs})
        x = np.zeros((len(values_of), len(vocab) + 1), np.float32)
        col = {v: j for j, v in enumerate(vocab)}
        for i, vs in enumerate(values_of):
            for v in vs:
                x[i, col[v]] = 1
            x[i, -1] = bool(vs)  # presence flag
        return x, [f"{prefix}={v}" for v in vocab] + [f"{prefix}?"]

    def local(o):
        return str(o).split("#")[-1]

    ids = [R + i for i in images]
    get = {p: objects(rdflib.URIRef(R + p)) for p in
           ("recordedAtDate", "hasSpatialLocation", "environmentCondition", "plantAgeDays", "ofVariety",
            "captures", "sourceLabel")}
    get["derived"] = objects(PROV.wasDerivedFrom)
    get["url"] = objects(rdflib.URIRef(SDO + "contentUrl"))

    blocks = {}
    parts = [onehot([[str(o)[5:7] for o in get["recordedAtDate"][i]] for i in ids], "month"),
             onehot([[local(o) for o in get["hasSpatialLocation"][i]] for i in ids], "location"),
             onehot([[str(o) for o in get["environmentCondition"][i]] for i in ids], "environment")]
    blocks["safe"] = (np.hstack([p[0] for p in parts]), sum((p[1] for p in parts), []))
    parts = [onehot([[str(o) for o in get["plantAgeDays"][i]] for i in ids], "age"),
             onehot([[local(o) for o in get["ofVariety"][i]] for i in ids], "variety")]
    blocks["context"] = (np.hstack([p[0] for p in parts]), sum((p[1] for p in parts), []))
    blocks["dataset"] = onehot([[local(o) for o in get["derived"][i]] for i in ids], "dataset")
    parts = [onehot([[str(o) for o in get["sourceLabel"][i]] for i in ids], "sourceLabel"),
             onehot([[local(o) for o in get["captures"][i]] for i in ids], "captures"),
             onehot([[str(o).split("/")[-2] for o in get["url"][i]] for i in ids], "folder")]
    blocks["leak"] = (np.hstack([p[0] for p in parts]), sum((p[1] for p in parts), []))
    return blocks


def main(root, out_md):
    root = Path(root)
    rows = list(csv.DictReader((root / "Retrieval Benchmark/splits/images_split.csv").open(encoding="utf-8")))
    with (root / "Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8") as f:
        gold_of = {r["image"]: r["gold"] for r in csv.DictReader(f)}
    ents = [str(e) for e in np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)["entities"]]
    e_idx = {e: i for i, e in enumerate(ents)}
    data = np.load(root / "Data/retrieval/feats_clip-l14.npz", allow_pickle=True)
    assert list(data["urls"]) == [r["url"] for r in rows]
    feats = data["feats"].astype(np.float32)
    split = np.array([r["split"] for r in rows]); ds = np.array([r["dataset"] for r in rows])
    group = np.array([r["group"] for r in rows]); gold = np.array([e_idx[gold_of[r["image"]]] for r in rows])

    g = rdflib.Graph(); g.parse(root / "Ontology/Rice MMKG.rdf", format="xml")
    blocks = edge_features(g, [r["image"] for r in rows])
    coverage = {b: {d: float(np.mean(x[ds == d, :][:, [j for j, n in enumerate(names) if n.endswith("?")]].max(1)))
                    for d in sorted(set(ds))} for b, (x, names) in blocks.items()}
    print("edge coverage by dataset:", json.dumps(coverage, indent=1), flush=True)

    rng = np.random.default_rng(0)
    ugroups = np.unique(group[split == "train"])
    val_groups = set(rng.choice(ugroups, size=len(ugroups) // 10, replace=False))
    is_val = np.isin(group, list(val_groups)) & (split == "train")
    fit_mask, dev_main = (split == "train") & ~is_val, (split == "dev") & ~np.isin(ds, list(SINGLE_SOURCE))
    protocols = {"in-source": [(fit_mask, is_val, dev_main)]}
    protocols["cross-source"] = []
    for held in sorted(set(ds[dev_main])):
        tr, va = fit_mask & (ds != held), is_val & (ds != held)
        q = dev_main & (ds == held) & np.isin(gold, np.unique(gold[tr]))
        if q.any():
            protocols["cross-source"].append((tr, va, q))

    res = collections.defaultdict(lambda: collections.defaultdict(list))
    rr_all = collections.defaultdict(lambda: collections.defaultdict(list))
    per_ds = collections.defaultdict(lambda: collections.defaultdict(list))
    for seed in SEEDS:
        gen = torch.Generator().manual_seed(1000 + seed)
        rand = nn.functional.normalize(torch.randn(len(ents), DIM, generator=gen), dim=1)
        for proto, parts in protocols.items():
            S = collections.defaultdict(list); G = []; D = []
            for tr, va, q in parts:
                mu, sd = feats[tr].mean(0), feats[tr].std(0) + 1e-6
                seen = np.unique(gold[tr])
                for v, use in VARIANTS.items():
                    x = np.hstack([(feats - mu) / sd] + [blocks[b][0] for b in use]).astype(np.float32)
                    m, _ = fit(torch.tensor(x[tr]), torch.tensor(gold[tr]), torch.tensor(x[va]), torch.tensor(gold[va]),
                               len(ents), rand, seed)
                    with torch.no_grad():
                        s = m(torch.tensor(x[q])).numpy()
                    s[:, np.setdiff1d(np.arange(len(ents)), seen)] = -np.inf
                    S[v].append(s)
                G.append(gold[q]); D.append(ds[q])
            G, D = np.concatenate(G), np.concatenate(D)
            for v in VARIANTS:
                mt, rr = metrics(np.concatenate(S[v]), G)
                for name, val in mt.items():
                    res[proto][(v, name)].append(val)
                rr_all[proto][v].append(rr)
                for d in sorted(set(D)):
                    per_ds[proto][(v, d)].append(float(np.mean(rr[D == d] == 1)))
            per_ds[proto]["n"] = {d: int((D == d).sum()) for d in sorted(set(D))}
            print(f"seed {seed} {proto}: " + "  ".join(f"{v.split()[0]} {res[proto][(v, 'R@1')][-1]:.3f}" for v in VARIANTS),
                  flush=True)

    lines = ["Link prediction with the photo's own edges, dev main subset (no single-source dataset). CLIP ViT-L/14 "
             f"features + binary edge features from `Ontology/Rice MMKG.rdf`; head C of `ikrl_v2_dev.py`; {len(SEEDS)} seeds "
             "(mean ± sd). Script: `scripts/dev_checks/link_pred_dev.py`.", "",
             "**Edge coverage by dataset** (share of photos with at least one edge of the block):", "",
             "| Block | " + " | ".join(sorted(set(ds))) + " |", "|---|" + "---:|" * len(set(ds))]
    for b, cov in coverage.items():
        lines.append(f"| {b} | " + " | ".join(f"{cov[d]:.2f}" for d in sorted(set(ds))) + " |")
    lines += ["", "| Protocol | Variant | n | R@1 | macro R@1 | MRR | Δ MRR vs 1 | seeds > 0 |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for proto in protocols:
        n = len(rr_all[proto]["1 pixels"][0])
        for v in VARIANTS:
            f = lambda name: f"{np.mean(res[proto][(v, name)]):.3f} ± {np.std(res[proto][(v, name)]):.3f}"
            d = [float(np.mean(a - b)) for a, b in zip(rr_all[proto][v], rr_all[proto]["1 pixels"])]
            dd = "" if v == "1 pixels" else f"{np.mean(d):+.4f} | {sum(x > 0 for x in d)}/{len(d)}"
            lines.append(f"| {proto} | {v} | {n} | {f('R@1')} | {f('macroR@1')} | {f('MRR')} | {dd or ' | '} |")
    lines += ["", "**R@1 per dataset** (mean over seeds):", "",
              "| Protocol | Dataset | n | " + " | ".join(VARIANTS) + " |", "|---|---|---:|" + "---:|" * len(VARIANTS)]
    for proto in protocols:
        for d, n in per_ds[proto]["n"].items():
            lines.append(f"| {proto} | {d} | {n} | " + " | ".join(f"{np.mean(per_ds[proto][(v, d)]):.3f}" for v in VARIANTS) + " |")
    Path(out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    Path(out_md).with_suffix(".json").write_text(json.dumps(
        {"coverage": coverage} | {p: {f"{v}|{n}": x for (v, n), x in d.items()} for p, d in res.items()}, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:3])
