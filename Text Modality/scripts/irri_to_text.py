"""Turn saved IRRI Rice Knowledge Bank fact-sheet pages into plain-text documents
for the CropKG pipeline: title, "## " headings, paragraphs and "- " list items
from the page body (div.pos-description) only. Writes a manifest that maps each
document to its source URL, so that extractions can be scored against the
curated assertions citing that URL.

The pages are CC BY-NC-SA 3.0; the text stays in this gitignored folder.

    python -I irri_to_text.py <raw html folder> <corpus folder>
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

BASE = "http://www.knowledgebank.irri.org/training/fact-sheets/"
URLS = {
    "potassium-k": "nutrient-management/item/potassium-k",
    "phosphorus": "nutrient-management/item/phosphorus",
    "zinc-factsheet": "nutrient-management/item/zinc-factsheet",
    "salinity": "nutrient-management/deficiencies-and-toxicities-fact-sheet/item/salinity",
    "iron-toxicity": "nutrient-management/deficiencies-and-toxicities-fact-sheet/item/iron-toxicity",
    "nitrogen": "nutrient-management/item/nitrogen",
    "tungro": "pest-management/diseases/item/tungro",
    "brown-spot": "pest-management/diseases/item/brown-spot",
    "bacterial-blight": "pest-management/diseases/item/bacterial-blight",
    "planthopper": "pest-management/insects/item/planthopper",
    "rice-hispa": "pest-management/insects/item/rice-hispa",
    "sheath-blight": "pest-management/diseases/item/sheath-blight",
    "stem-borer": "pest-management/insects/item/stem-borer",
    "bacterial-leaf-streak": "pest-management/diseases/item/bacterial-leaf-streak",
    "blast-node-neck": "pest-management/diseases/item/blast-node-neck",
    "armyworms": "pest-management/insects/item/armyworms",
    "blast-leaf-collar": "pest-management/diseases/item/blast-leaf-collar",
    "rice-bug": "pest-management/insects/item/rice-bug",
    "rice-leaffolder": "pest-management/insects/item/rice-leaffolder",
}


class Body(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0          # div depth inside pos-description; 0 = outside
        self.out, self.buf, self.prefix = [], [], ""
        self.title, self.in_h1 = "", False

    def flush(self):
        t = " ".join("".join(self.buf).split())
        if t:
            self.out.append(self.prefix + t)
        self.buf, self.prefix = [], ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.in_h1 = True
        if tag == "div":
            if self.depth:
                self.depth += 1
            elif "pos-description" in (a.get("class") or ""):
                self.depth = 1
            return
        if not self.depth:
            return
        if tag in ("p", "li", "h2", "h3", "h4", "tr", "br"):
            self.flush()
            self.prefix = {"li": "- ", "h2": "## ", "h3": "## ", "h4": "## "}.get(tag, "")

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        if self.depth and tag == "div":
            self.depth -= 1
            if not self.depth:
                self.flush()
        elif self.depth and tag in ("p", "li", "h2", "h3", "h4", "td", "tr"):
            if tag == "td":
                self.buf.append(" | ")
            else:
                self.flush()

    def handle_data(self, data):
        if self.in_h1:
            self.title += data
        if self.depth:
            self.buf.append(data)


def main(raw, corpus):
    raw, corpus = Path(raw), Path(corpus)
    corpus.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for stem, path in URLS.items():
        p = Body()
        p.feed((raw / f"{stem}.html").read_text(encoding="utf-8", errors="replace"))
        text = "\n\n".join(p.out)
        text = re.sub(r"\n{3,}", "\n\n", text)
        title = " ".join(p.title.split()) or stem
        name = f"IRRI_{stem}"
        (corpus / f"{name}.txt").write_text(f"{title}\n\n{text}\n", encoding="utf-8")
        manifest[name] = BASE + path
        print(f"{name}: {len(text):,} chars")
    (corpus.parent / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(*sys.argv[1:3])
