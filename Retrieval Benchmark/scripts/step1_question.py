"""Step 1 with the farmer's words, on dev only. Stage-1 scores come from
results/verify_dev.jsonl; the questions from make_questions.py.

text(e) = highest bge-m3 cosine between the observation and a KG symptom label of e
(Normal_Health: a label meaning healthy). Fusion: z(stage 1) + lambda * z(text), over
the stage-1 top 5. lambda is tuned by two-fold cross-fitting, so each photo is scored
with a weight chosen on the other fold.

The observation is simulated (make_questions.py), so this is a sensitivity analysis.
With noise 1.0 the observation would say nothing about the photo; the template
question alone carries no entity information.

    <venv python> -I step1_question.py <repo root> <out.md>
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import rdflib

root, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / "Retrieval Benchmark/scripts"))
from stage2_passages import embed
from step2_rerank import PAIRS, R, label, local, sign_flip

TOP = 5
LAMBDAS = (0, 0.25, 0.5, 1, 2, 4, 8)
NOISES = ("0.0", "0.3", "0.5")
HEALTHY_LABEL = "healthy rice plant with no symptoms"

recs = {r["image"]: r for r in map(json.loads, (root / "Retrieval Benchmark/results/verify_dev.jsonl").read_text(encoding="utf-8").splitlines())}
with (root / "Retrieval Benchmark/splits/questions_dev.csv").open(encoding="utf-8") as f:
    qs = list(csv.DictReader(f))
entities = [str(e) for e in np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)["entities"]]
g = rdflib.Graph()
g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
labels = sorted({label(g, s) for e in entities for s in g.objects(R[e], R.indicatedBy)}) + [HEALTHY_LABEL]
pos = {x: i for i, x in enumerate(labels)}
lab_vec = np.array(embed(labels))
lab_vec /= np.linalg.norm(lab_vec, axis=1, keepdims=True)
members = {e: [pos[label(g, s)] for s in g.objects(R[e], R.indicatedBy)] or [pos[HEALTHY_LABEL]] for e in entities}


def text_scores(texts):
    v = np.array(embed(texts))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    sim = v @ lab_vec.T
    return np.stack([sim[:, members[e]].max(1) for e in entities], 1)


def z(x):
    x = np.where(np.isinf(x), np.nan, x)
    return np.nan_to_num((x - np.nanmean(x, 1, keepdims=True)) / np.nanstd(x, 1, keepdims=True), nan=-10.0)


def rank(s1, tx, lam, gold):
    zs = z(s1)
    top = np.argsort(-zs, 1)[:, :TOP]
    full = zs - 1000.0
    rows = np.arange(len(zs))[:, None]
    full[rows, top] = zs[rows, top] + lam * z(tx)[rows, top]
    return np.argmax(np.argsort(-full, 1) == gold[:, None], 1) + 1


lines = ["Step 1 with a SIMULATED farmer observation, dev_core main subset (sensitivity analysis, not a result).", "",
         "| Protocol | Noise | n | Stage 1 R@1 | + words R@1 | Stage 1 MRR | + words MRR | p (MRR) | Blast / brown spot R@1 | lambda (folds) |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
for proto in ("in-source", "cross-source"):
    use = [q for q in qs if proto in recs[q["image"]]["stage1"]]
    s1 = np.array([recs[q["image"]]["stage1"][proto] for q in use])
    gold = np.array([entities.index(q["gold"]) for q in use])
    fold = np.array([int(hashlib.md5(q["image"].encode()).hexdigest(), 16) % 2 for q in use])
    pair = np.isin(np.array(entities)[gold], list(PAIRS["blast / brown spot"]))
    for noise in NOISES:
        tx = text_scores([q[f"observation_{noise}"] for q in use])
        new, chosen = np.zeros(len(use), int), []
        for k in (0, 1):
            tune, test = fold == k, fold != k
            lam = max(LAMBDAS, key=lambda v: (np.mean(rank(s1[tune], tx[tune], v, gold[tune]) == 1), -v))
            chosen.append(lam)
            new[test] = rank(s1[test], tx[test], lam, gold[test])
        base = rank(s1, tx, 0, gold)
        lines.append(f"| {proto} | {noise} | {len(use)} | {np.mean(base == 1):.3f} | {np.mean(new == 1):.3f} | {np.mean(1 / base):.3f} "
                     f"| {np.mean(1 / new):.3f} | {sign_flip(base, new):.4f} | {np.mean(base[pair] == 1):.3f} → {np.mean(new[pair] == 1):.3f} | {chosen} |")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
