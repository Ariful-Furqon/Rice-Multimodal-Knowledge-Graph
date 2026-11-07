"""Step 2 field context, on dev only. Plant age is the only context that comes with
the photos, and only Paddy Doctor has it. It is mapped to growth stages by fixed bands
set before the run, then to candidates through the KG:

    context(e) = 1 if e occursIn a stage of this age, 0 if e occursIn other stages only,
                 0.5 if the KG gives e no stage (Normal_Health, the nutrient disorders)

Fusion: z(stage 1) + lambda * context over the top 5, lambda cross-fitted on two folds.
No training: the bands and the KG decide, so no age statistic of a dataset is learned.
Ages are read from the full ontology, because the query-time graph holds no dev image.

    <venv python> -I step2_field_context.py <repo root> <out.md>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import rdflib

root, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / "Retrieval Benchmark/scripts"))
from step2_rerank import R, local, sign_flip
import kg_paths

TOP = 5
LAMBDAS = (0, 0.25, 0.5, 1, 2, 4, 8)
BANDS = [(30, {"Seedling_Stage"}), (60, {"Tillering_Stage", "Vegetative_Stage"}),
         (90, {"Reproductive_Stage", "Flowering_Stage"}), (10 ** 6, {"Maturity_Stage"})]

recs = [json.loads(x) for x in (root / "Retrieval Benchmark/results/verify_dev.jsonl").read_text(encoding="utf-8").splitlines()]
entities = [str(e) for e in np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)["entities"]]
g = rdflib.Graph()
g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
stages = {e: {local(s) for s in g.objects(R[e], R.occursIn)} for e in entities}

wanted = {r["image"] for r in recs}
ages, current = {}, None
with kg_paths.ontology(root).open(encoding="utf-8") as f:
    for line in f:
        m = re.search(r'rdf:about="https://w3id.org/ricemmkg#([^"]+)"', line)
        if m:
            current = m.group(1)
        elif "plantAgeDays" in line and current in wanted:
            ages[current] = int(re.search(r">(\d+)<", line).group(1))


def context(age):
    stage = next(s for limit, s in BANDS if age <= limit)
    return [0.5 if not stages[e] else float(bool(stages[e] & stage)) for e in entities]


def z(x):
    x = np.where(np.isinf(x), np.nan, x)
    return np.nan_to_num((x - np.nanmean(x, 1, keepdims=True)) / np.nanstd(x, 1, keepdims=True), nan=-10.0)


def rank(s1, cx, lam, gold):
    zs = z(s1)
    top = np.argsort(-zs, 1)[:, :TOP]
    full = zs - 1000.0
    rows = np.arange(len(zs))[:, None]
    full[rows, top] = zs[rows, top] + lam * cx[rows, top]
    return np.argmax(np.argsort(-full, 1) == gold[:, None], 1) + 1


lines = [f"Field context (plant age through occursIn), dev_core. {len(ages)} of {len(recs)} photos have an age, all Paddy Doctor.", "",
         "| Protocol | n with age | Stage 1 R@1 | + context R@1 | Stage 1 MRR | + context MRR | p (MRR) | lambda (folds) | Gold allowed by its stage |",
         "|---|---:|---:|---:|---:|---:|---:|---|---:|"]
for proto in ("in-source", "cross-source"):
    use = [r for r in recs if proto in r["stage1"] and r["image"] in ages]
    if not use:
        lines.append(f"| {proto} | 0 | | | | | | | |")
        continue
    s1 = np.array([r["stage1"][proto] for r in use])
    cx = np.array([context(ages[r["image"]]) for r in use])
    gold = np.array([entities.index(r["gold"]) for r in use])
    fold = np.array([int(hashlib.md5(r["image"].encode()).hexdigest(), 16) % 2 for r in use])
    new, chosen = np.zeros(len(use), int), []
    for k in (0, 1):
        tune, test = fold == k, fold != k
        lam = max(LAMBDAS, key=lambda v: (np.mean(rank(s1[tune], cx[tune], v, gold[tune]) == 1), -v))
        chosen.append(lam)
        new[test] = rank(s1[test], cx[test], lam, gold[test])
    base = rank(s1, cx, 0, gold)
    allowed = np.mean(cx[np.arange(len(use)), gold] > 0)
    lines.append(f"| {proto} | {len(use)} | {np.mean(base == 1):.3f} | {np.mean(new == 1):.3f} | {np.mean(1 / base):.3f} | "
                 f"{np.mean(1 / new):.3f} | {sign_flip(base, new):.4f} | {chosen} | {allowed:.3f} |")
print("ages", sorted(set(ages.values())))
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
