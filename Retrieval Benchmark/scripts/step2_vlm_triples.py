"""Step 2, part 1 (KGMEL step 1): a local VLM reads each photo and writes symptom
triples. Plan: Ontology/riceMMKG_SIGIR_plan.md, section 4; design_v2.md, section 2.

Images: splits/test_core.csv to report and splits/dev_core.csv to tune the fusion.
dev_core is drawn from the dev split by the rule of test_core (at most
CORE_PER_STRATUM per stratum, seed 0) and written on the first run.

Two vocabularies:
- closed: the VLM must pick symptoms and plant parts from the labels in the KG.
  No condition name appears in the prompt, so the VLM cannot answer the label.
  Prompt v2: v1 offered a "healthy" field and the VLM took it on most photos, sick
  ones too, so the prompt now asks for the marks first and has no such field. The
  choice was made on a sample of dev_core (design_v2.md, section 8).
- open:   free text, for the KGMEL baseline (design_v2.md, section 3).

The output is one JSON line per image, appended as it goes, so a stopped run resumes.

    <venv python> -I step2_vlm_triples.py <repo root> <closed|open> <out.jsonl>
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

import rdflib
from PIL import Image

R = rdflib.Namespace("https://w3id.org/ricemmkg#")
OLLAMA = "http://localhost:11434/api/chat"
VLM = "qwen2.5vl:7b"
SEED = 0
CORE_PER_STRATUM = 15
MAX_SIDE = 768
CLOSED = """You are a rice plant pathologist. First describe the colour, shape and position of any marks on the plant in this photo. Then match them to the list.

Symptoms you may report (use these exact words):
{symptoms}

Plant parts you may report (use these exact words):
{parts}

Reply with JSON only:
{{"marks": "colour, shape and position of the marks, or none", "triples": [{{"symptom": "...", "part": "...", "confidence": 0.0 to 1.0}}]}}

Use at most 4 triples, and none if there are no marks. Do not name a disease or a pest."""
OPEN = """You are a rice plant pathologist. Look at this photo and report only what is clearly visible.

Reply with JSON only:
{"description": "one sentence", "triples": [{"subject": "...", "relation": "...", "object": "..."}]}

Use at most 6 triples. Each relation must be one of: has symptom, located on, has color, has shape. Do not name a disease or a pest."""


def label(g, node):
    return str(g.value(node, rdflib.RDFS.label) or str(node).split("#")[-1].replace("_", " "))


def core_rows(root):
    here = root / "Retrieval Benchmark/splits"
    with (here / "test_core.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    path = here / "dev_core.csv"
    if not path.exists():
        with (here / "images_split.csv").open(encoding="utf-8") as f:
            split = list(csv.DictReader(f))
        rng, per, core = random.Random(SEED), collections.defaultdict(list), []
        for r in split:
            if r["split"] == "dev":
                per[(r["dataset"], r["annotatedAs"])].append(r)
        for key in sorted(per):
            pick = sorted(per[key], key=lambda r: r["image"])
            rng.shuffle(pick)
            core += pick[:CORE_PER_STRATUM]
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(split[0]))
            w.writeheader()
            w.writerows(sorted(core, key=lambda r: (r["dataset"], r["annotatedAs"], r["image"])))
    with path.open(encoding="utf-8") as f:
        return rows + list(csv.DictReader(f))


def image_b64(path):
    img = Image.open(path).convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


def ask(prompt, path):
    body = {"model": VLM, "stream": False, "format": "json",
            "options": {"temperature": 0, "seed": SEED, "num_predict": 400},
            "messages": [{"role": "user", "content": prompt, "images": [image_b64(path)]}]}
    req = urllib.request.Request(OLLAMA, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)["message"]["content"]


def main(root, mode, out):
    root, out = Path(root), Path(out)
    g = rdflib.Graph()
    g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
    symptoms = sorted(label(g, s) for s in g.subjects(rdflib.RDF.type, R.Symptom))
    parts = sorted(label(g, p) for p in g.subjects(rdflib.RDF.type, R.PlantPart))
    prompt = CLOSED.format(symptoms=", ".join(symptoms), parts=", ".join(parts)) if mode == "closed" else OPEN

    done = set()
    if out.exists():
        done = {json.loads(line)["image"] for line in out.read_text(encoding="utf-8").splitlines()}
    rows = [r for r in core_rows(root) if r["image"] not in done]
    print(f"{len(done)} done, {len(rows)} to do", flush=True)
    t0 = time.time()
    with out.open("a", encoding="utf-8") as f:
        for i, r in enumerate(rows):
            raw = ask(prompt, root / r["url"])
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = None
            f.write(json.dumps({"image": r["image"], "split": r["split"], "parsed": parsed, "raw": raw}) + "\n")
            f.flush()
            if i % 20 == 0:
                print(f"  {i}/{len(rows)} {(time.time() - t0) / (i + 1):.1f} s/image", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
