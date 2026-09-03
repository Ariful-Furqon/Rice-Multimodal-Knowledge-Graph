import csv
import json
import re
import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SRC_DIR = SCRIPT_DIR.parent / "LLM Prompt"
PROMPT = SRC_DIR / "rice_mmkg_cq_prompt.md"

# Filename -> model label as it should appear in the paper.
MODELS = {
    "Claude Opus 5 CQ.md":    "Claude Opus 5",
    "Claude Fable 5.1 CQ.md": "Claude Fable 5.1",
    "GPT-5.6 Sol CQ.md":      "GPT-5.6 Sol",
    "Gemini Pro 3.1 CQ.md":   "Gemini Pro 3.1",
    "Gemini Flash 3.8 CQ.md": "Gemini Flash 3.8",
}

# The prompt asked for five categories. Models used slightly different ID
# prefixes for the sensor category; normalise, but keep the original ID intact.
CATEGORY = {
    "TXT": "text", "IMG": "image", "ENV": "sensor",
    "SEN": "sensor", "GEN": "genomic", "MM": "crossmodal",
}

HEADER_RE = re.compile(r"^\|\s*ID\s*\|\s*Question\s*\|", re.I)
SEP_RE = re.compile(r"^\|[\s:|-]+\|$")
HEADING_RE = re.compile(r"^#{2,4}\s+(.*)$")
ID_RE = re.compile(r"^CQ-([A-Z]+)-?(\d+)$")


def clean(cell):
    """Strip markdown emphasis and collapse whitespace, keep the text itself."""
    s = cell.strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


ESCAPED_PIPE = "\\|"
PIPE_SENTINEL = "\x00"


def split_row(line):
    """Split a markdown table row into cells, tolerating escaped pipes."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    body = body.replace(ESCAPED_PIPE, PIPE_SENTINEL)
    return [c.replace(PIPE_SENTINEL, "|") for c in body.split("|")]


def parse(path, model):
    lines = path.read_text(encoding="utf-8").split("\n")
    heading, in_table, rows = "", False, []
    for i, line in enumerate(lines):
        h = HEADING_RE.match(line)
        if h:
            heading, in_table = clean(h.group(1)), False
            continue
        if HEADER_RE.match(line):
            in_table = True
            continue
        if in_table:
            if SEP_RE.match(line):
                continue
            if not line.strip().startswith("|"):
                in_table = False
                continue
            cells = [clean(c) for c in split_row(line)]
            if len(cells) < 5 or not cells[0]:
                continue
            cq_id = cells[0]
            m = ID_RE.match(cq_id)
            if not m:
                continue
            rows.append({
                "source_model": model,
                "original_id": cq_id,
                "category": CATEGORY.get(m.group(1), "unknown"),
                "id_prefix": m.group(1),
                "question": cells[1],
                "complexity": cells[2],
                "entities": cells[3],
                "rationale": cells[4],
                "section": heading,
                "source_file": path.name,
                "source_line": i + 1,
            })
    return rows


def main():
    assert SRC_DIR.is_dir(), f"missing source dir: {SRC_DIR}"
    pool = []
    per_model = {}
    for fname, model in MODELS.items():
        path = SRC_DIR / fname
        assert path.exists(), f"missing source file: {path}"
        rows = parse(path, model)
        per_model[model] = len(rows)
        pool.extend(rows)

    pool.sort(key=lambda r: (r["source_model"], r["original_id"]))
    for k, row in enumerate(pool, start=1):
        row["pool_id"] = f"P{k:03d}"

    fields = ["pool_id", "source_model", "original_id", "category", "id_prefix",
              "complexity", "question", "entities", "rationale", "section",
              "source_file", "source_line"]

    with (SCRIPT_DIR / "cq_pool_stage0.csv").open("w", encoding="utf-8-sig",
                                                  newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows({k: r[k] for k in fields} for r in pool)

    with (SCRIPT_DIR / "cq_pool_stage0.jsonl").open("w", encoding="utf-8") as f:
        for r in pool:
            f.write(json.dumps({k: r[k] for k in fields}, ensure_ascii=False) + "\n")

    cat = {}
    cplx = {}
    for r in pool:
        cat.setdefault(r["category"], {}).setdefault(r["source_model"], 0)
        cat[r["category"]][r["source_model"]] += 1
        cplx[r["complexity"]] = cplx.get(r["complexity"], 0) + 1

    L = ["# Stage 0 - Raw Competency Question Pool", "",
         f"Generated {datetime.datetime.now():%Y-%m-%d %H:%M} by "
         "`stage0_build_pool.py`. No filtering, deduplication or rewording has "
         "been applied; every row reproduces its source verbatim.", "",
         f"**Prompt:** `LLM Prompt/{PROMPT.name}` (single shared prompt, "
         "identical for all five models).", "",
         f"**Pool size:** {len(pool)} candidate CQs from {len(MODELS)} models.",
         "", "## Yield per model", "",
         "| Model | Source file | CQs |", "|---|---|---|"]
    for fname, model in MODELS.items():
        L.append(f"| {model} | `{fname}` | {per_model[model]} |")
    L.append(f"| **Total** | | **{len(pool)}** |")

    cats = ["text", "image", "sensor", "genomic", "crossmodal", "unknown"]
    cats = [c for c in cats if c in cat]
    L += ["", "## Distribution by category", "",
          "| Model | " + " | ".join(cats) + " | Total |",
          "|---" * (len(cats) + 2) + "|"]
    for model in MODELS.values():
        row = [str(cat.get(c, {}).get(model, 0)) for c in cats]
        L.append(f"| {model} | " + " | ".join(row) + f" | {per_model[model]} |")
    tot = [str(sum(cat.get(c, {}).values())) for c in cats]
    L.append("| **Total** | " + " | ".join(f"**{t}**" for t in tot) +
             f" | **{len(pool)}** |")

    L += ["", "## Complexity labels as written by the models", "",
          "| Label | Count |", "|---|---|"]
    for k, v in sorted(cplx.items(), key=lambda x: -x[1]):
        L.append(f"| {k} | {v} |")
    L += ["", "Labels are reproduced verbatim; harmonising them is a Stage 2 task.", ""]

    (SCRIPT_DIR / "cq_pool_stage0.md").write_text("\n".join(L), encoding="utf-8")
    print(f"pool: {len(pool)} CQs")
    for m, c in per_model.items():
        print(f"  {m:20s} {c}")


if __name__ == "__main__":
    main()
