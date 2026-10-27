"""Write the gold answer of each image for entity retrieval: the cause to
manage (pest, pathogen disease, nutrient disorder), not the symptom.

Decision 2026-10-27 (see design_v2.md, section 5):
- All stem borer damage photos have gold Stem_Borer, as the stem borer group.
  Paddy Doctor names its three borer folders by species (yellow, white,
  black), but the photos show the damage, mostly whiteheads, and the species
  cannot be told from it; management is the same.
- Deadheart and White_Ear are symptoms, not retrieval targets. They are kept
  per image only where the source labels the symptom (Stem Borer BD), as
  ground truth for the step-2 symptom check.
- annotatedAs in the ontology is not changed here; that waits for the expert.

    python -I make_gold.py <repo root>
"""
import collections
import csv
import sys
from pathlib import Path

# (dataset folder, class folder) -> (gold, symptom); "*" matches any class folder ending
RULES = {
    ("stem-borer-bd", "Dead_Heart"): ("Stem_Borer", "Deadheart"),
    ("stem-borer-bd", "White_Head"): ("Stem_Borer", "White_Ear"),
    ("paddy-doctor-diseases", "*_stem_borer"): ("Stem_Borer", ""),
}


def rule_for(url):
    parts = url.split("/")
    folder, cls = parts[1], parts[2]
    for (f, c), target in RULES.items():
        if f == folder and (c == cls or (c.startswith("*") and cls.endswith(c[1:]))):
            return target, f"{f}/{c}"
    return None, ""


def main(root):
    splits = Path(root) / "Retrieval Benchmark" / "splits"
    with (splits / "images_split.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        target, rule = rule_for(r["url"])
        gold, symptom = target if target else (r["annotatedAs"], "")
        out.append({"image": r["image"], "annotatedAs": r["annotatedAs"],
                    "gold": gold, "symptom": symptom, "rule": rule})
    with (splits / "gold.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["image", "annotatedAs", "gold", "symptom", "rule"])
        w.writeheader()
        w.writerows(out)
    changed = collections.Counter((o["annotatedAs"], o["gold"]) for o in out if o["annotatedAs"] != o["gold"])
    print(f"{len({o['gold'] for o in out})} gold targets; remapped:", dict(changed))


if __name__ == "__main__":
    main(sys.argv[1])
