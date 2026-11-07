"""Removing the source dataset from the image features, dev only.

Motivation (Analysis and Alignment/Related_Work_Leakage_and_Dataset_Bias.md, section 3):
the source dataset is linearly decodable from CLIP features (0.993, as in "Name That
Dataset", Torralba & Efros 2011; Liu & He 2025), and a source that is visible in the
pixels confounds the label (Zech et al. 2018). If the stage-1 image systems lean on it,
removing it should raise cross-source R@1, the checkpoint-1 target.

Feature transforms, applied to the L2-normalised CLIP ViT-L/14 features before the
stage-1 systems (knn_image, linear_probe as in stage1_baselines.py), then re-normalised:
  none       the stage-1 features
  project    remove the source subspace: fit a linear source classifier on the training
             images, project its weight directions out, repeat (iterative nullspace
             projection, ITERS rounds). Uses training images and their source only.
  center     subtract each source's mean feature. A training source uses the mean of its
             training images. The query source uses the mean of its own dev images,
             (all of them, whatever their target), without labels: this is
             transductive, it needs a batch of unlabelled photos
             from the new source. In-source the query source is a training source, so
             its training mean is used.
  both       center, then project
  project_cc as project, but the source classifier is fitted on the training features
             minus their class (gold) mean, so only directions that separate sources
             within a class are removed. Added after `project` removed the label too
             where a class comes from one source only (potassium: Netrokona).

Protocols as in link_pred_dev.py: in-source (train split -> dev main) and cross-source
(leave one dataset out; queries limited to targets seen in training). Deterministic, no
seeds. Δ MRR against `none` with a 95% bootstrap interval over capture groups.

    <venv python> -I debias_dev.py <repo root> <out .md>
"""
import collections
import csv
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ikrl_v2_dev import SINGLE_SOURCE, metrics  # noqa: E402

KNN_K = 5
ITERS = 3
BOOT = 1000
TRANSFORMS = ("none", "project", "center", "both", "project_cc")
SYSTEMS = ("knn_image", "linear_probe")


def unit(x):
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def source_basis(x, src, iters=ITERS, cls=None):
    """Orthonormal basis of the directions a linear source classifier uses, found
    iteratively: each round fits on the features with the earlier directions removed.
    With `cls`, the classifier sees the features minus their class mean, so it can only
    use directions that separate sources within a class."""
    if cls is not None:
        x = x.copy()
        for c in np.unique(cls):
            x[cls == c] -= x[cls == c].mean(0)
    basis = np.zeros((0, x.shape[1]))
    for _ in range(iters):
        xr = x - (x @ basis.T) @ basis
        clf = LogisticRegression(max_iter=2000).fit(xr, src)
        w = clf.coef_ if clf.coef_.ndim == 2 else clf.coef_[None]
        w = w - (w @ basis.T) @ basis
        basis = np.vstack([basis, np.linalg.svd(w, full_matrices=False)[2]])
        basis = np.linalg.svd(basis, full_matrices=False)[2]
    return basis


def source_acc(x_tr, s_tr, x_te, s_te):
    return float(LogisticRegression(max_iter=2000).fit(x_tr, s_tr).score(x_te, s_te))


def knn_scores(q, g, g_gold, n):
    sims = q @ g.T
    out = np.full((len(q), n), -np.inf)
    for c in np.unique(g_gold):
        s = sims[:, g_gold == c]
        k = min(KNN_K, s.shape[1])
        out[:, c] = np.sort(s, 1)[:, -k:].mean(1)
    return out


def probe_scores(q, g, g_gold, n):
    clf = LogisticRegression(max_iter=2000, C=1.0).fit(g, g_gold)
    out = np.full((len(q), n), -np.inf)
    out[:, clf.classes_] = clf.predict_log_proba(q)
    return out


def transform(name, feats, ds, tr, pool, gold):
    """Transformed copy of all features. `pool` = the dev images of the query sources,
    all of them, whatever their label (no label is used to centre). `gold` is used only
    on training images (project_cc)."""
    if name == "project_cc":
        basis = source_basis(feats[tr], ds[tr], cls=gold[tr])
        return unit(feats - (feats @ basis.T) @ basis)
    x = feats.copy()
    if name in ("center", "both"):
        for d in np.unique(ds[tr | pool]):
            ref = tr & (ds == d)
            if not ref.any():  # the held-out source: its own unlabelled dev images
                ref = pool & (ds == d)
            x[ds == d] -= feats[ref].mean(0)
    if name in ("project", "both"):
        basis = source_basis(x[tr], ds[tr])
        x = x - (x @ basis.T) @ basis
    return unit(x)


def boot_ci(delta, groups, rng):
    """95% interval of the mean of delta, resampling capture groups."""
    ug, inv = np.unique(groups, return_inverse=True)
    sums, counts = np.bincount(inv, delta), np.bincount(inv)
    stats = []
    for _ in range(BOOT):
        pick = rng.integers(0, len(ug), len(ug))
        stats.append(sums[pick].sum() / counts[pick].sum())
    return np.percentile(stats, [2.5, 97.5])


def main(root, out_md):
    sys.stdout.reconfigure(encoding="utf-8")
    root = Path(root)
    rows = list(csv.DictReader((root / "Retrieval Benchmark/splits/images_split.csv").open(encoding="utf-8")))
    with (root / "Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8") as f:
        gold_of = {r["image"]: r["gold"] for r in csv.DictReader(f)}
    ents = [str(e) for e in np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)["entities"]]
    e_idx = {e: i for i, e in enumerate(ents)}
    data = np.load(root / "Data/retrieval/feats_clip-l14.npz", allow_pickle=True)
    assert list(data["urls"]) == [r["url"] for r in rows]
    feats = unit(data["feats"].astype(np.float64))
    split = np.array([r["split"] for r in rows]); ds = np.array([r["dataset"] for r in rows])
    group = np.array([r["group"] for r in rows]); gold = np.array([e_idx[gold_of[r["image"]]] for r in rows])

    train, dev_main = split == "train", (split == "dev") & ~np.isin(ds, list(SINGLE_SOURCE))
    main_ds = sorted(set(ds[dev_main]))
    protocols = {"in-source": [(train, dev_main, dev_main)], "cross-source": []}
    for held in main_ds:
        tr = train & (ds != held)
        pool = dev_main & (ds == held)
        q = pool & np.isin(gold, np.unique(gold[tr]))
        if q.any():
            protocols["cross-source"].append((tr, q, pool))

    rng = np.random.default_rng(0)
    rr = collections.defaultdict(dict); mt = collections.defaultdict(dict)
    per_ds = collections.defaultdict(dict); n_ds = {}; src_acc = collections.defaultdict(list)
    for proto, parts in protocols.items():
        S = collections.defaultdict(list); G, D, Gr = [], [], []
        for tr, q, pool in parts:
            # source decodability on the train-split images of the training sources
            # (half to fit, half to test), before and after each transform
            half = rng.random(len(feats)) < 0.5
            for t in TRANSFORMS:
                x = transform(t, feats, ds, tr, pool, gold)
                src_acc[(proto, t)].append(source_acc(x[tr & half], ds[tr & half], x[tr & ~half], ds[tr & ~half]))
                for sys_name, fn in (("knn_image", knn_scores), ("linear_probe", probe_scores)):
                    S[(t, sys_name)].append(fn(x[q], x[tr], gold[tr], len(ents)))
            G.append(gold[q]); D.append(ds[q]); Gr.append(group[q])
            print(f"{proto} fold done ({len(G)}/{len(parts)})", flush=True)
        G, D, Gr = map(np.concatenate, (G, D, Gr))
        n_ds[proto] = {d: int((D == d).sum()) for d in sorted(set(D))}
        for key, s in S.items():
            s = np.concatenate(s)
            m, r = metrics(s, G)
            rank = 1.0 / r
            m["R@3"] = float(np.mean(rank <= 3))
            mt[proto][key], rr[proto][key] = m, r
            per_ds[proto][key] = {d: float(np.mean(rank[D == d] == 1)) for d in n_ds[proto]}
        rr[proto]["groups"] = Gr

    lines = ["Source removal from CLIP ViT-L/14 features before the stage-1 image systems, dev main subset "
             "(no single-source dataset). Transforms: `project` removes the source subspace learned on the "
             f"training images ({ITERS} rounds of nullspace projection); `center` subtracts each source's mean "
             "feature, for a held-out source the mean of its own unlabelled dev images (transductive); `both` "
             "is center then project; `project_cc` is project with the source classifier fitted on features minus "
             "their class mean (within-class source directions only). Δ MRR against `none`, 95% bootstrap interval over capture groups. "
             "Script: `scripts/dev_checks/debias_dev.py`.", "",
             "**Source predictable from the features** (linear probe, train images of the training sources, "
             "half to fit and half to test; mean over folds):", "",
             "| Protocol | " + " | ".join(TRANSFORMS) + " |", "|---|" + "---:|" * len(TRANSFORMS)]
    for proto in protocols:
        lines.append(f"| {proto} | " + " | ".join(f"{np.mean(src_acc[(proto, t)]):.3f}" for t in TRANSFORMS) + " |")
    lines += ["", "| Protocol | System | Transform | n | R@1 | macro R@1 | R@3 | MRR | Δ MRR [95% CI] |",
              "|---|---|---|---:|---:|---:|---:|---:|---|"]
    for proto in protocols:
        for sys_name in SYSTEMS:
            base = rr[proto][("none", sys_name)]
            for t in TRANSFORMS:
                m = mt[proto][(t, sys_name)]
                if t == "none":
                    d = ""
                else:
                    delta = rr[proto][(t, sys_name)] - base
                    lo, hi = boot_ci(delta, rr[proto]["groups"], rng)
                    d = f"{delta.mean():+.4f} [{lo:+.4f}, {hi:+.4f}]"
                lines.append(f"| {proto} | {sys_name} | {t} | {len(base)} | {m['R@1']:.3f} | {m['macroR@1']:.3f} | "
                             f"{m['R@3']:.3f} | {m['MRR']:.3f} | {d} |")
    lines += ["", "**R@1 per dataset:**", "",
              "| Protocol | System | Dataset | n | " + " | ".join(TRANSFORMS) + " |",
              "|---|---|---|---:|" + "---:|" * len(TRANSFORMS)]
    for proto in protocols:
        for sys_name in SYSTEMS:
            for d, n in n_ds[proto].items():
                lines.append(f"| {proto} | {sys_name} | {d} | {n} | " +
                             " | ".join(f"{per_ds[proto][(t, sys_name)][d]:.3f}" for t in TRANSFORMS) + " |")
    Path(out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    Path(out_md).with_suffix(".json").write_text(json.dumps(
        {"source_acc": {f"{p}|{t}": v for (p, t), v in src_acc.items()},
         "metrics": {p: {f"{t}|{s}": m for (t, s), m in d.items()} for p, d in mt.items()},
         "per_dataset_R@1": {p: {f"{t}|{s}": m for (t, s), m in d.items()} for p, d in per_ds.items()}}, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:3])
