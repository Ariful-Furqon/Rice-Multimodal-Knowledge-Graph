"""Dev check: shape_crops.py with another VLM, whole photo and reference photos only.
Same 60 blast and brown spot photos of dev_core as shape_dev.py. Stop rule set before
the run: balanced accuracy of at least 0.7, against 0.367 for the whole photo.

- reference: two train photos per condition shown first, with their shape.

    <venv python> -I shape_crops.py <repo root> <out.jsonl> <model>
"""
import base64
import collections
import csv
import io
import json
import random
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

root, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / "Retrieval Benchmark/scripts"))
from step2_rerank import SINGLE_SOURCE
from step2_vlm_triples import image_b64, OLLAMA, VLM

SHAPES = {"Rice_Blast_Disease": "spindle", "Brown_Spot": "round"}
THRESHOLD = 0.7
TILES = 3
VLM = sys.argv[3]
PROMPT = ('Look at the lesions on this rice leaf. What is the main lesion shape? Reply with JSON only: {"shape": "spindle"} '
          'for long lesions pointed at both ends (diamond-like), {"shape": "round"} for circular to oval spots, '
          '{"shape": "none"} if no lesion is visible.')

gold = {r["image"]: r["gold"] for r in csv.DictReader((root / "Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8"))}
rows = [r for r in csv.DictReader((root / "Retrieval Benchmark/splits/dev_core.csv").open(encoding="utf-8"))
        if r["dataset"] not in SINGLE_SOURCE and gold[r["image"]] in SHAPES]
split = list(csv.DictReader((root / "Retrieval Benchmark/splits/images_split.csv").open(encoding="utf-8")))
rng = random.Random(0)
refs = []
for e, shape in SHAPES.items():
    pool = sorted((r for r in split if r["split"] == "train" and gold.get(r["image"]) == e
                   and r["dataset"] not in SINGLE_SOURCE), key=lambda r: r["image"])
    refs += [(root / r["url"], shape) for r in rng.sample(pool, 2)]


def ask(messages):
    body = {"model": VLM, "stream": False, "format": "json",
            "options": {"temperature": 0, "seed": 0, "num_predict": 30}, "messages": messages}
    if not VLM.startswith("qwen2.5vl"):  # newer models may reason first; ask for the answer only
        body["think"] = False
    req = urllib.request.Request(OLLAMA, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                raw = json.load(r)["message"]["content"]
            break
        except OSError:
            time.sleep(10 * (attempt + 1))
    else:
        raise RuntimeError("no answer")
    try:
        return str(json.loads(raw).get("shape"))
    except (ValueError, AttributeError):
        return "bad"


def tiles(path):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    for i in range(TILES):
        for j in range(TILES):
            crop = img.crop((w * i // TILES, h * j // TILES, w * (i + 1) // TILES, h * (j + 1) // TILES))
            crop.thumbnail((768, 768))
            buf = io.BytesIO()
            crop.save(buf, "JPEG", quality=90)
            yield base64.b64encode(buf.getvalue()).decode()


shots = []
for path, shape in refs:
    shots.append({"role": "user", "content": PROMPT, "images": [image_b64(path)]})
    shots.append({"role": "assistant", "content": json.dumps({"shape": shape})})

result = {"whole": collections.Counter(), "reference": collections.Counter()}
with out.open("w", encoding="utf-8") as f:
    for n, r in enumerate(rows):
        e = gold[r["image"]]
        crop = ask([{"role": "user", "content": PROMPT, "images": [image_b64(root / r["url"])]}])
        ref = ask(shots + [{"role": "user", "content": PROMPT, "images": [image_b64(root / r["url"])]}])
        result["whole"][(e, crop)] += 1
        result["reference"][(e, ref)] += 1
        f.write(json.dumps({"image": r["image"], "gold": e, "whole": crop, "reference": ref}) + "\n")
        f.flush()
        print(n, len(rows), flush=True)
for name, c in result.items():
    acc = [c[(e, s)] / sum(v for k, v in c.items() if k[0] == e) for e, s in SHAPES.items()]
    print(name, sorted(c.items()), "balanced", round(sum(acc) / 2, 3), "pass" if sum(acc) / 2 >= THRESHOLD else "fail", flush=True)
print("FINISHED", flush=True)
