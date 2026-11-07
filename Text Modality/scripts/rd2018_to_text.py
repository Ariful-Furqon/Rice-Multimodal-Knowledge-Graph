"""Turn the disease sections of IRRI's online book "Rice Diseases: Biology & Selected
Management Practices" (2018, https://rice-diseases.irri.org, CC BY-NC-SA 4.0) into plain-text
documents in the same format as irri_to_text.py: title line, "## " headings, and paragraphs
separated by blank lines. Passage offsets in the core graph refer to this text.

Each document is one disease section of a chapter PDF, from the disease heading up to (not
including) its "Causal organism" subsection: the introduction and the Symptoms subsection.

Text is extracted with pypdf (version recorded in the manifest). Clean-up rules:
- lines that hold only a page number are dropped;
- a line that ends in "-" after a letter, followed by a line that starts with a lower-case
  letter, is joined without the hyphen (a word broken across lines); other lines are joined
  with a space;
- a line that starts with a space, or follows a heading, starts a new paragraph;
- "N.N. <name>" subsection headings become "## <name>";
- the text before the first subsection gets the heading "## Introduction". The book has no
  heading there; it is added so that passages.cut() does not merge the first paragraph into
  the title line, which it skips.

The PDFs are CC BY-NC-SA 4.0; they and the derived text stay in the gitignored Data folder.

    python -I rd2018_to_text.py <raw pdf folder> <corpus folder>
"""
import json
import re
import sys
from pathlib import Path

import pypdf

CONTENTS = "https://rice-diseases.irri.org/contents"
# chapter PDFs as linked from the contents page (the site has no chapter pages). The core graph uses
# CONTENTS as dcterms:source; the Drive link is kept in the TextDocument comment only.
CH2 = ("chapter2_foliar_fungal_diseases.pdf", "https://drive.google.com/file/d/1FecmYWgUMk_-UIjNA6_TyPKBjUn_oQ81/view?usp=sharing",
       "Part II, Section 1: Fungal Diseases. Chapter 2. Foliar fungal diseases")
CH4 = ("chapter4_grain_diseases.pdf", "https://drive.google.com/file/d/1T0FEK70qH64wQUT0uIvEH6uuv6tqHVcw/view?usp=sharing",
       "Part II, Section 2: Bacterial Diseases. Chapter 4. Grain diseases")
# doc id: (chapter, heading that starts the section, heading that ends it, document title)
DOCS = {
    "downy-mildew": (CH2, r"^2\. Downy mildew \(DM\)\s*$", r"^2\.2\. Causal organism", "Downy mildew (DM)"),
    "leaf-scald": (CH2, r"^6\. Leaf Scald \(LSc\)\s*$", r"^6\.2\. Causal organism", "Leaf scald (LSc)"),
    "grain-rot": (CH4, r"^1\. Grain rot \(GnR\)\s*$", r"^1\.2\. Causal organism", "Grain rot (GnR)"),
}


def section_lines(text, start, end):
    lines = text.split("\n")
    a = next(i for i, l in enumerate(lines) if re.match(start, l))
    b = next(i for i, l in enumerate(lines) if i > a and re.match(end, l))
    return lines[a + 1:b]


def to_blocks(lines):
    blocks, cur = [], ""
    for raw in lines:
        if re.fullmatch(r"\s*\d+\s*", raw):
            continue
        line = raw.rstrip()
        h = re.match(r"^\d+\.\d+\.\s+(.+?)\s*$", line)
        if h:
            if cur:
                blocks.append(cur)
            blocks.append("## " + h.group(1))
            cur = ""
            continue
        if line.startswith(" ") and cur:
            blocks.append(cur)
            cur = ""
        line = line.strip()
        if not line:
            continue
        if not cur:
            cur = line
        elif re.search(r"[A-Za-z]-$", cur) and line[:1].islower():
            cur = cur[:-1] + line
        else:
            cur = cur + " " + line
    if cur:
        blocks.append(cur)
    return [re.sub(r"\s{2,}", " ", b) for b in blocks]


def main(raw, corpus):
    raw, corpus = Path(raw), Path(corpus)
    corpus.mkdir(parents=True, exist_ok=True)
    texts, manifest = {}, {"_contents": CONTENTS, "_pypdf": pypdf.__version__}
    for doc, ((pdf, url, chapter), start, end, title) in DOCS.items():
        if pdf not in texts:
            texts[pdf] = "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(str(raw / pdf)).pages)
        blocks = to_blocks(section_lines(texts[pdf], start, end))
        (corpus / f"IRRI_RD2018_{doc}.txt").write_text(title + "\n\n## Introduction\n\n" + "\n\n".join(blocks) + "\n", encoding="utf-8")
        manifest[f"IRRI_RD2018_{doc}"] = {"url": CONTENTS, "pdf_url": url, "pdf": pdf, "chapter": chapter, "title": title}
        print(doc, len(blocks), "blocks")
    (corpus.parent / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(*sys.argv[1:3])
