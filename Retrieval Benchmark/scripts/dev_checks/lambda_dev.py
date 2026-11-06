"""Dev-only lambda analysis: fine grid, R@1 vs MRR, bootstrap stability. Never touches test."""
import csv, json, sys
from pathlib import Path
import numpy as np
import rdflib
from sklearn.linear_model import LogisticRegression

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "Retrieval Benchmark/scripts"))
import step2_rerank as S

g = rdflib.Graph(); g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
rows = list(csv.DictReader((root / "Retrieval Benchmark/splits/images_split.csv").open(encoding="utf-8")))
gold_of = {r["image"]: r["gold"] for r in csv.DictReader((root / "Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8"))}
st = np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)
entities = [str(e) for e in st["entities"]]; e_idx = {e: i for i, e in enumerate(entities)}
feats = np.load(root / "Data/retrieval/feats_clip-l14.npz", allow_pickle=True)["feats"]
row_of = {r["image"]: i for i, r in enumerate(rows)}
split = np.array([r["split"] for r in rows]); dataset = np.array([r["dataset"] for r in rows])
gold_all = np.array([e_idx[gold_of[r["image"]]] for r in rows])
vlm = [json.loads(x) for x in (root / "Retrieval Benchmark/results/vlm_triples_closed.jsonl").read_text(encoding="utf-8").splitlines()]
vlm = [r for r in vlm if r["image"] in row_of and split[row_of[r["image"]]] == "dev"]   # dev only
idx = np.array([row_of[r["image"]] for r in vlm])
kg, _ = S.kg_scores(vlm, entities, g)

def probe(m, q):
    lr = LogisticRegression(max_iter=2000, C=1.0).fit(feats[m], gold_all[m])
    out = np.full((len(q), len(entities)), -np.inf); out[:, lr.classes_] = lr.predict_log_proba(feats[q]); return out

train = split == "train"
s1 = {"in-source": probe(train, idx), "cross-source": np.full((len(idx), len(entities)), -np.inf)}
usable = {"in-source": np.ones(len(idx), bool), "cross-source": np.zeros(len(idx), bool)}
for held in sorted(set(dataset[idx])):
    gal = train & (dataset != held)
    qm = (dataset[idx] == held) & np.isin(gold_all[idx], np.unique(gold_all[gal]))
    if qm.any():
        s1["cross-source"][qm] = probe(gal, idx[qm]); usable["cross-source"][qm] = True
gold = gold_all[idx]; main_q = ~np.isin(dataset[idx], list(S.SINGLE_SOURCE))

GRID = np.concatenate([[0], np.geomspace(0.01, 10, 40)])
rng = np.random.default_rng(0); B = 2000
for proto, sc in s1.items():
    m = usable[proto] & main_q
    R = np.stack([S.ranks(S.fuse(sc[m], kg[m], l), gold[m]) for l in GRID])  # (grid, n)
    r1, rr = (R == 1).astype(float), 1.0 / R
    boot = rng.integers(0, m.sum(), size=(B, m.sum()))
    print(f"\n== {proto}  n_dev={m.sum()}")
    print(" lambda   R@1    MRR   P(MRR>λ0)")
    for k, l in enumerate(GRID):
        d = rr[k] - rr[0]
        p = np.mean(d[boot].mean(1) > 0) if k else float("nan")
        if k == 0 or k % 3 == 0 or r1[k].mean() >= r1.mean(1).max() - 1e-9 or rr[k].mean() >= rr.mean(1).max() - 1e-9:
            print(f"{l:7.3f} {r1[k].mean():.3f} {rr[k].mean():.4f}  {p:.3f}")
    for name, M in (("R@1", r1), ("MRR", rr)):
        argb = [int(np.argmax(M[:, b].mean(1))) for b in boot[:500]]
        picks = np.array(GRID)[argb]
        sm = M[:, boot].mean(2).mean(1)  # bootstrap-smoothed curve
        print(f" {name}: raw argmax λ={GRID[np.argmax(M.mean(1))]:.3f}; smoothed argmax λ={GRID[np.argmax(sm)]:.3f}; "
              f"bootstrap pick λ=0 in {np.mean(picks==0):.2f}, median pick {np.median(picks):.3f}, IQR {np.percentile(picks,25):.3f}-{np.percentile(picks,75):.3f}")
