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
  3 context     2 + plantAgeDays (growth-stage band, BANDS of step2_field_context.py) + ofVariety
  3b            3, trained without early stopping for exactly the epochs variant 1 stopped at
                (same seed and fold): separates the effect of the inputs from that of the
                stopping point
  4 dataset     2 + prov:wasDerivedFrom (one-hot); in-source only, because the held-out
                dataset's column is never set in cross-source training
  5 leaking     2 + sourceLabel, captures, and the folder name in schema:contentUrl

Also a lookup baseline with no model: folder name in contentUrl -> majority train gold
(a folder never seen in train is a miss).

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
from ikrl_v2_dev import DIM, SINGLE_SOURCE, Head, fit, metrics  # noqa: E402

R = "https://w3id.org/ricemmkg#"
SDO = "http://schema.org/"
SEEDS = range(5)
# Same bands as scripts/step2_field_context.py (upper age limit in days -> stage).
BANDS = [(30, "Seedling"), (60, "Tillering/Vegetative"), (90, "Reproductive/Flowering"), (10 ** 6, "Maturity")]
VARIANTS = {"1 pixels": [], "2 safe": ["safe"], "3 + age, variety": ["safe", "context"],
            "3b = 3, epochs of 1": ["safe", "context"],
            "4 + dataset": ["safe", "dataset"], "5 + leaking edges": ["safe", "leak"]}
FIXED_EPOCHS = {"3b = 3, epochs of 1": "1 pixels"}
IN_SOURCE_ONLY = {"4 + dataset"}


def band(age):
    return next(name for limit, name in BANDS if int(age) <= limit)


def fit_fixed(x_tr, y_tr, n, class_emb, seed, epochs):
    """fit() of ikrl_v2_dev.py without early stopping: the model after `epochs` steps."""
    torch.manual_seed(seed)
    m = Head(x_tr.shape[1], n, class_emb)
    opt = torch.optim.Adam(m.parameters(), lr=1e-3, weight_decay=1e-4)
    for _ in range(epochs):
        m.train(); opt.zero_grad()
        nn.functional.cross_entropy(m(x_tr), y_tr).backward(); opt.step()
    m.eval()
    return m


def edge_features(g, images):
    """Binary feature blocks per photo: {block: (n, d) array}, plus their column names.
    Also returns the folder name of each photo (for the lookup baseline)."""
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
    folders = [[str(o).split("/")[-2] for o in get["url"][i]] for i in ids]

    blocks = {}
    parts = [onehot([[str(o)[5:7] for o in get["recordedAtDate"][i]] for i in ids], "month"),
             onehot([[local(o) for o in get["hasSpatialLocation"][i]] for i in ids], "location"),
             onehot([[str(o) for o in get["environmentCondition"][i]] for i in ids], "environment")]
    blocks["safe"] = (np.hstack([p[0] for p in parts]), sum((p[1] for p in parts), []))
    parts = [onehot([[band(o) for o in get["plantAgeDays"][i]] for i in ids], "stage"),
             onehot([[local(o) for o in get["ofVariety"][i]] for i in ids], "variety")]
    blocks["context"] = (np.hstack([p[0] for p in parts]), sum((p[1] for p in parts), []))
    blocks["dataset"] = onehot([[local(o) for o in get["derived"][i]] for i in ids], "dataset")
    parts = [onehot([[str(o) for o in get["sourceLabel"][i]] for i in ids], "sourceLabel"),
             onehot([[local(o) for o in get["captures"][i]] for i in ids], "captures"),
             onehot(folders, "folder")]
    blocks["leak"] = (np.hstack([p[0] for p in parts]), sum((p[1] for p in parts), []))
    return blocks, ["/".join(sorted(f)) for f in folders]


def lookup_r1(folder, gold, tr, q):
    """Folder name -> majority train gold; R@1 on q (unseen folder = miss)."""
    votes = collections.defaultdict(collections.Counter)
    for i in np.flatnonzero(tr):
        votes[folder[i]][gold[i]] += 1
    hit = [bool(votes[folder[i]]) and votes[folder[i]].most_common(1)[0][0] == gold[i] for i in np.flatnonzero(q)]
    seen = [bool(votes[folder[i]]) for i in np.flatnonzero(q)]
    return int(sum(hit)), int(sum(seen)), len(hit)


def main(root, out_md):
    sys.stdout.reconfigure(encoding="utf-8")  # the report has non-ASCII; a Windows console is cp1252
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
    blocks, folder = edge_features(g, [r["image"] for r in rows])

    rng = np.random.default_rng(0)
    ugroups = np.unique(group[split == "train"])
    val_groups = set(rng.choice(ugroups, size=len(ugroups) // 10, replace=False))
    is_val = np.isin(group, list(val_groups)) & (split == "train")
    fit_mask, dev_main = (split == "train") & ~is_val, (split == "dev") & ~np.isin(ds, list(SINGLE_SOURCE))
    main_ds = sorted(set(ds[dev_main]))
    coverage = {b: {d: float(np.mean(x[dev_main & (ds == d)][:, [j for j, n in enumerate(names) if n.endswith("?")]].max(1)))
                    for d in main_ds} for b, (x, names) in blocks.items()}
    print("edge coverage on dev main:", json.dumps(coverage, indent=1), flush=True)

    protocols = {"in-source": [(fit_mask, is_val, dev_main)]}
    protocols["cross-source"] = []
    for held in main_ds:
        tr, va = fit_mask & (ds != held), is_val & (ds != held)
        q = dev_main & (ds == held) & np.isin(gold, np.unique(gold[tr]))
        if q.any():
            protocols["cross-source"].append((tr, va, q))
    lookup = {p: [sum(x) for x in zip(*(lookup_r1(folder, gold, tr | va, q) for tr, va, q in parts))]
              for p, parts in protocols.items()}

    def active(proto):
        return [v for v in VARIANTS if not (proto == "cross-source" and v in IN_SOURCE_ONLY)]

    res = collections.defaultdict(lambda: collections.defaultdict(list))
    rr_all = collections.defaultdict(lambda: collections.defaultdict(list))
    per_ds = collections.defaultdict(lambda: collections.defaultdict(list))
    epochs = collections.defaultdict(lambda: collections.defaultdict(list))
    n_ds = {}
    for seed in SEEDS:
        gen = torch.Generator().manual_seed(1000 + seed)
        rand = nn.functional.normalize(torch.randn(len(ents), DIM, generator=gen), dim=1)
        for proto, parts in protocols.items():
            S = collections.defaultdict(list); G = []; D = []
            for tr, va, q in parts:
                mu, sd = feats[tr].mean(0), feats[tr].std(0) + 1e-6
                seen = np.unique(gold[tr])
                stop = {}
                for v in active(proto):
                    x = np.hstack([(feats - mu) / sd] + [blocks[b][0] for b in VARIANTS[v]]).astype(np.float32)
                    if v in FIXED_EPOCHS:
                        k = stop[FIXED_EPOCHS[v]]
                        m = fit_fixed(torch.tensor(x[tr]), torch.tensor(gold[tr]), len(ents), rand, seed, k)
                    else:
                        info = {}
                        m, _ = fit(torch.tensor(x[tr]), torch.tensor(gold[tr]), torch.tensor(x[va]), torch.tensor(gold[va]),
                                   len(ents), rand, seed, info=info)
                        k = stop[v] = info["epoch"]
                    epochs[proto][v].append(k)
                    with torch.no_grad():
                        s = m(torch.tensor(x[q])).numpy()
                    s[:, np.setdiff1d(np.arange(len(ents)), seen)] = -np.inf
                    S[v].append(s)
                G.append(gold[q]); D.append(ds[q])
            G, D = np.concatenate(G), np.concatenate(D)
            for v in active(proto):
                mt, rr = metrics(np.concatenate(S[v]), G)
                for name, val in mt.items():
                    res[proto][(v, name)].append(val)
                rr_all[proto][v].append(rr)
                for d in sorted(set(D)):
                    per_ds[proto][(v, d)].append(float(np.mean(rr[D == d] == 1)))
            n_ds[proto] = {d: int((D == d).sum()) for d in sorted(set(D))}
            print(f"seed {seed} {proto}: " + "  ".join(f"{v.split()[0]} {res[proto][(v, 'R@1')][-1]:.3f}"
                                                      for v in active(proto)), flush=True)

    lines = ["Link prediction with the photo's own edges, dev main subset (no single-source dataset). CLIP ViT-L/14 "
             f"features + binary edge features from `Ontology/Rice MMKG.rdf`; head C of `ikrl_v2_dev.py`; {len(SEEDS)} seeds "
             "(mean ± sd). Plant age enters as its growth-stage band. Variant 3b is variant 3 trained, without early "
             "stopping, for the epochs at which variant 1 stopped. Script: `scripts/dev_checks/link_pred_dev.py`.", "",
             "**Edge coverage on the dev main subset** (share of photos with at least one edge of the block):", "",
             "| Block | " + " | ".join(main_ds) + " |", "|---|" + "---:|" * len(main_ds)]
    for b, cov in coverage.items():
        lines.append(f"| {b} | " + " | ".join(f"{cov[d]:.2f}" for d in main_ds) + " |")
    lines += ["", "**Lookup baseline, no model:** folder name in `contentUrl` → majority train gold "
              "(an unseen folder is a miss).", "",
              "| Protocol | n | R@1 | folder seen in train |", "|---|---:|---:|---:|"]
    for proto, (hit, seen, n) in lookup.items():
        lines.append(f"| {proto} | {n} | {hit / n:.3f} | {seen / n:.3f} |")
    lines += ["", "| Protocol | Variant | n | R@1 | macro R@1 | MRR | Δ MRR vs 1 | seeds > 0 | stop epoch |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for proto in protocols:
        n = len(rr_all[proto]["1 pixels"][0])
        for v in VARIANTS:
            if v not in active(proto):
                lines.append(f"| {proto} | {v} | | n/a | | | | | |")
                continue
            f = lambda name: f"{np.mean(res[proto][(v, name)]):.3f} ± {np.std(res[proto][(v, name)]):.3f}"
            d = [float(np.mean(a - b)) for a, b in zip(rr_all[proto][v], rr_all[proto]["1 pixels"])]
            dd = " | " if v == "1 pixels" else f"{np.mean(d):+.4f} | {sum(x > 0 for x in d)}/{len(d)}"
            lines.append(f"| {proto} | {v} | {n} | {f('R@1')} | {f('macroR@1')} | {f('MRR')} | {dd} | "
                         f"{np.mean(epochs[proto][v]):.0f} |")
    lines += ["", "Stop epoch: mean epoch of the kept model (of 400), over seeds and, cross-source, the held-out folds.",
              "", "**R@1 per dataset** (mean over seeds):", "",
              "| Protocol | Dataset | n | " + " | ".join(VARIANTS) + " |", "|---|---|---:|" + "---:|" * len(VARIANTS)]
    for proto in protocols:
        for d, n in n_ds[proto].items():
            lines.append(f"| {proto} | {d} | {n} | " + " | ".join(
                f"{np.mean(per_ds[proto][(v, d)]):.3f}" if v in active(proto) else "n/a" for v in VARIANTS) + " |")
    Path(out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    Path(out_md).with_suffix(".json").write_text(json.dumps(
        {"coverage_dev_main": coverage,
         "lookup": {p: dict(zip(("hits", "folder_seen", "n"), x)) for p, x in lookup.items()},
         "stop_epoch": {p: dict(d) for p, d in epochs.items()},
         "per_dataset_R@1": {p: {f"{v}|{d}": x for (v, d), x in dd.items()} for p, dd in per_ds.items()}}
        | {p: {f"{v}|{n}": x for (v, n), x in d.items()} for p, d in res.items()}, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:3])
