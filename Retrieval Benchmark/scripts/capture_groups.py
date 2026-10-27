"""Group images taken in one capture session, so that make_split.py keeps each
group in one split. Burst photos of the same plant otherwise sit in train and
test at once: on the first split (2026-10-26, MD5 groups only) 70% of test
images had a train image with CLIP similarity >= 0.98, and image kNN scored
R@1 0.917.

Rules:
- Paddy Doctor: one group per (label, variety, age) from its metadata.csv.
  96% of image pairs that are each other's nearest neighbour (CLIP >= 0.95)
  share this key; random same-label pairs share it 19% of the time.
- Other datasets (no capture metadata): union of pairs with CLIP ViT-L/14
  cosine >= SIM_THRESHOLD within one (dataset, label). Spot checks: at
  0.98-0.99 Nutrient Kaggle and Netrokona pairs are the same leaf with
  consecutive file numbers; Dhan-Shomadhan and Stem Borer pairs are different
  photos, so grouping them only makes the split stricter. Pairs across
  labels are not joined.
- Byte-identical files (same MD5) within one (dataset, label) are joined.
  Clustering all of Paddy Doctor by similarity does not work: at 0.98 one
  chained group holds 12,050 images.

Needs the CLIP features cached by stage1_baselines.py.

    <venv python> -I capture_groups.py <repo root>
"""
import collections
import csv
import sys
from pathlib import Path

import numpy as np
import torch

SIM_THRESHOLD = 0.98
PADDY = "PaddyDoctorDataset"


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def main(root):
    root = Path(root)
    splits = root / "Retrieval Benchmark" / "splits"
    with (splits / "images_split.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with (root / "Data/paddy-doctor-diseases/metadata.csv").open(encoding="utf-8") as f:
        session = {r["image_id"]: (r["label"], r["variety"], r["age"]) for r in csv.DictReader(f)}

    cache = np.load(root / "Data/retrieval/feats_clip-l14.npz", allow_pickle=True)
    pos = {u: i for i, u in enumerate(cache["urls"])}
    feats = torch.tensor(cache["feats"]).cuda()

    uf = UnionFind(len(rows))
    strata = collections.defaultdict(list)
    for i, r in enumerate(rows):
        strata[(r["dataset"], r["annotatedAs"])].append(i)

    for (dataset, _), idx in sorted(strata.items()):
        first = {}
        for i in idx:
            r = rows[i]
            keys = [("md5", r["md5"])]
            if dataset == PADDY:
                keys.append(("session", session[Path(r["url"]).name]))
            for k in keys:
                if k in first:
                    uf.union(i, first[k])
                else:
                    first[k] = i
        if dataset == PADDY:
            continue
        f = feats[[pos[rows[i]["url"]] for i in idx]]
        sim = f @ f.T
        a, b = torch.nonzero(torch.triu(sim >= SIM_THRESHOLD, diagonal=1), as_tuple=True)
        for x, y in zip(a.tolist(), b.tolist()):
            uf.union(idx[x], idx[y])

    group_id = {}
    with (splits / "capture_groups.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["image", "group"])
        for i, r in enumerate(rows):
            g = group_id.setdefault(uf.find(i), f"G{len(group_id):05d}")
            w.writerow([r["image"], g])

    sizes = collections.Counter(uf.find(i) for i in range(len(rows)))
    per_ds = collections.defaultdict(list)
    for root_i, n in sizes.items():
        per_ds[rows[root_i]["dataset"]].append(n)
    for ds, ns in sorted(per_ds.items()):
        ns.sort(reverse=True)
        print(f"{ds}: {len(ns)} groups, largest {ns[:3]}")


if __name__ == "__main__":
    main(sys.argv[1])
