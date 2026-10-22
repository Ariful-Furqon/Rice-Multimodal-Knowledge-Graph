"""Cut the corpus into passages with character offsets, and record which domain
individuals each passage mentions (exact label match after normalisation).

A passage is one paragraph or bullet of a section; pieces shorter than MIN
characters are merged with the next piece of the same section. Offsets refer to
the corpus text file (data/corpus/<doc>.txt); sha256 lets a consumer check that
the text it re-derives from the source is the same.

    python -I passages.py <data dir>
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

MIN = 120


def norm(s):
    s = re.sub(r"[_\-]", " ", s.lower())
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    words = s.split()
    return " ".join(w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w for w in words)


def cut(text):
    """Yield (section, start, end) for each passage."""
    section, pending = "", None
    for m in re.finditer(r"[^\n]+(?:\n(?!\n)[^\n]+)*", text):
        block = m.group()
        if block.startswith("## "):
            if pending:
                yield pending
            section, pending = block[3:].strip(), None
            continue
        if pending and pending[0] == section and pending[2] - pending[1] < MIN:
            pending = (section, pending[1], m.end())
            continue
        if pending:
            yield pending
        pending = (section, m.start(), m.end())
    if pending:
        yield pending


def main(data):
    data = Path(data)
    manifest = json.loads((data / "manifest.json").read_text(encoding="utf-8"))
    ents = json.loads((data / "entities.json").read_text(encoding="utf-8"))
    labels = collections.defaultdict(set)
    for n, e in ents.items():
        for lab in e["labels"]:
            if len(norm(lab)) > 3:
                labels[norm(lab)].add(n)
    rows = []
    for f in sorted((data / "corpus").glob("*.txt")):
        doc = f.stem
        text = f.read_text(encoding="utf-8")
        title = text.split("\n", 1)[0].strip()
        for i, (section, a, b) in enumerate(cut(text)):
            if a == 0:  # the title line
                continue
            body = text[a:b]
            nb = f" {norm(body)} "
            mentions = sorted({n for lab, ns in labels.items() if f" {lab} " in nb for n in ns})
            rows.append({"id": f"{doc}#p{i}", "doc": doc, "url": manifest.get(doc), "title": title,
                         "section": section, "start": a, "end": b,
                         "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
                         "text": body, "mentions": mentions})
    (data / "passages.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
    n_m = collections.Counter(len(r["mentions"]) > 0 for r in rows)
    lens = sorted(r["end"] - r["start"] for r in rows)
    print(f"{len(rows)} passages over {len(set(r['doc'] for r in rows))} documents; "
          f"median {lens[len(lens) // 2]} chars, max {lens[-1]}; {n_m[True]} mention at least one individual; "
          f"{len({m for r in rows for m in r['mentions']})} distinct individuals mentioned")


if __name__ == "__main__":
    main(sys.argv[1])
