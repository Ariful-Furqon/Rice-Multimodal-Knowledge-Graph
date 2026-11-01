"""Step 2 fallback (plan, checkpoint 1), on dev only: LLM rerank that keeps stage 1.
The KGMEL prompt is given the stage-1 confidence of the top 3, and its answer counts
only when stage 1 is unsure: top-1 minus top-2 probability below a threshold tuned by
two-fold cross-fitting. Threshold 0 means stage 1 alone. Answers are cached.

    <venv python> -I step2_llm_gate.py <repo root> <open triples.jsonl> <out dir>
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import rdflib

root, open_triples, out_dir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(root / "Retrieval Benchmark/scripts"))
from step2_rerank import R, kgmel_prompt, llm_choice, sign_flip

TOP = 3
GATES = (0, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1.01)

recs = [json.loads(x) for x in (root / "Retrieval Benchmark/results/verify_dev.jsonl").read_text(encoding="utf-8").splitlines()]
open_of = {r["image"]: r for r in map(json.loads, open_triples.read_text(encoding="utf-8").splitlines())}
entities = [str(e) for e in np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)["entities"]]
g = rdflib.Graph()
g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
cache_path = out_dir / "llm_gate_answers.jsonl"
cache = {}
if cache_path.exists():
    cache = {(c["protocol"], c["image"]): c["answer"] for c in map(json.loads, cache_path.read_text(encoding="utf-8").splitlines())}

lines = ["LLM rerank gated on stage-1 confidence, top 3, dev_core main subset, thresholds cross-fitted.", "",
         "| Protocol | n | Stage 1 R@1 | Gated R@1 | Stage 1 MRR | Gated MRR | p (MRR) | Threshold (folds) | Photos changed |",
         "|---|---:|---:|---:|---:|---:|---:|---|---:|"]
with cache_path.open("a", encoding="utf-8") as f:
    for proto in ("in-source", "cross-source"):
        use = [r for r in recs if proto in r["stage1"]]
        s1 = np.exp(np.array([r["stage1"][proto] for r in use]))
        order = np.argsort(-s1, 1)
        gold = np.array([entities.index(r["gold"]) for r in use])
        picks = []
        for r, o, p in zip(use, order, s1):
            top = o[:TOP]
            key = (proto, r["image"])
            if key not in cache:
                prompt = kgmel_prompt(open_of[r["image"]], top, entities, g)
                conf = ", ".join(f"candidate {k} {p[c]:.0%}" for k, c in enumerate(top, 1))
                prompt = prompt.replace("Which candidate fits best?", f"An image classifier gave: {conf}. Change its first choice only "
                                        "if the observation clearly favours another candidate. Which candidate fits best?")
                cache[key] = llm_choice(prompt, TOP)
                f.write(json.dumps({"protocol": proto, "image": r["image"], "answer": cache[key]}) + "\n")
                f.flush()
            picks.append(top[cache[key] - 1])
        picks = np.array(picks)
        margin = s1[np.arange(len(use)), order[:, 0]] - s1[np.arange(len(use)), order[:, 1]]

        def rank(gate, mask):
            out = []
            for o, p, m, y in zip(order[mask], picks[mask], margin[mask], gold[mask]):
                first = p if m < gate else o[0]
                out.append(1 + [first, *[c for c in o if c != first]].index(y))
            return np.array(out)

        fold = np.array([int(hashlib.md5(r["image"].encode()).hexdigest(), 16) % 2 for r in use])
        new, chosen, changed = np.zeros(len(use), int), [], 0
        for k in (0, 1):
            tune, test = fold == k, fold != k
            gate = max(GATES, key=lambda v: (np.mean(rank(v, tune) == 1), -v))
            chosen.append(gate)
            new[test] = rank(gate, test)
            changed += int(np.sum((margin[test] < gate) & (picks[test] != order[test, 0])))
        base = rank(0, np.ones(len(use), bool))
        lines.append(f"| {proto} | {len(use)} | {np.mean(base == 1):.3f} | {np.mean(new == 1):.3f} | {np.mean(1 / base):.3f} | "
                     f"{np.mean(1 / new):.3f} | {sign_flip(base, new):.4f} | {chosen} | {changed} |")
(out_dir / "step2_llm_gate_dev.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines).encode("ascii", "replace").decode())
