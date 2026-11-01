"""Dev-only experiment: the VLM checks the symptoms of the stage-1 top 3 as a yes/no
list. Two lesion-shape symptoms are trial additions, not yet in the KG.

    python verify_dev.py <repo root> <out.jsonl>
"""
import csv
import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
import rdflib
from sklearn.linear_model import LogisticRegression

root, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / "Retrieval Benchmark/scripts"))
from step2_rerank import R, SINGLE_SOURCE, label
from step2_vlm_triples import image_b64, OLLAMA, VLM

TOP = 3
TRIAL = {"Rice_Blast_Disease": ["spindle-shaped or diamond-shaped lesion, pointed at both ends"],
         "Brown_Spot": ["circular to oval lesion"]}
PROMPT = """You are checking a rice plant photo. For each numbered item, answer true only if it is clearly visible in this photo, otherwise false.

{items}

Reply with JSON only, one key per number, for example {{"1": false, "2": true}}."""

rows = list(csv.DictReader((root / "Retrieval Benchmark/splits/images_split.csv").open(encoding="utf-8")))
gold = {r["image"]: r["gold"] for r in csv.DictReader((root / "Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8"))}
entities = [str(e) for e in np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)["entities"]]
ei = {e: i for i, e in enumerate(entities)}
feats = np.load(root / "Data/retrieval/feats_clip-l14.npz", allow_pickle=True)["feats"]
pos = {r["image"]: i for i, r in enumerate(rows)}
split = np.array([r["split"] for r in rows])
ds = np.array([r["dataset"] for r in rows])
y = np.array([ei[gold[r["image"]]] for r in rows])
dev = [r["image"] for r in csv.DictReader((root / "Retrieval Benchmark/splits/dev_core.csv").open(encoding="utf-8"))]
idx = np.array([pos[i] for i in dev if ds[pos[i]] not in SINGLE_SOURCE])
train = split == "train"

g = rdflib.Graph()
g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
symptoms = {e: sorted(label(g, s) for s in g.objects(R[e], R.indicatedBy)) + TRIAL.get(e, []) for e in entities}


def probe(mask, q):
    lr = LogisticRegression(max_iter=2000).fit(feats[mask], y[mask])
    p = np.full((len(q), len(entities)), -np.inf)
    p[:, lr.classes_] = lr.predict_log_proba(feats[q])
    return p


s1 = {"in-source": dict(zip(idx.tolist(), probe(train, idx)))}
cross = {}
for held in sorted(set(ds[idx])):
    gal = train & (ds != held)
    q = idx[(ds[idx] == held) & np.isin(y[idx], np.unique(y[gal]))]
    if len(q):
        cross.update(zip(q.tolist(), probe(gal, q)))
s1["cross-source"] = cross

done = set()
if out.exists():
    done = {json.loads(x)["image"] for x in out.read_text(encoding="utf-8").splitlines()}
with out.open("a", encoding="utf-8") as f:
    for n, i in enumerate(idx.tolist()):
        image = rows[i]["image"]
        if image in done:
            continue
        cands = {p: [entities[c] for c in np.argsort(-s[i])[:TOP]] for p, s in s1.items() if i in s}
        items = sorted({x for c in cands.values() for e in c for x in symptoms[e]})
        scores = {p: s[i].tolist() for p, s in s1.items() if i in s}
        rec = {"image": image, "gold": gold[image], "dataset": str(ds[i]), "candidates": cands, "items": items,
               "stage1": scores, "answers": None}
        if items:
            text = PROMPT.format(items="\n".join(f"{k}. {x}" for k, x in enumerate(items, 1)))
            body = {"model": VLM, "stream": False, "format": "json",
                    "options": {"temperature": 0, "seed": 0, "num_predict": 300},
                    "messages": [{"role": "user", "content": text, "images": [image_b64(root / rows[i]["url"])]}]}
            req = urllib.request.Request(OLLAMA, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                raw = json.load(r)["message"]["content"]
            try:
                rec["answers"] = json.loads(raw)
            except json.JSONDecodeError:
                rec["raw"] = raw
        f.write(json.dumps(rec) + "\n")
        f.flush()
        if n % 20 == 0:
            print(n, len(idx), flush=True)
print("FINISHED", flush=True)
