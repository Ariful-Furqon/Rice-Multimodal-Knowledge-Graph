"""Question layer of the benchmark (plan, section 5.1).

Writes to splits/:
- question_templates.csv: one farmer-style question per intent. They name no condition
  and no symptom, so they carry no information about the entity.
- questions_dev.csv: dev_core main subset, each photo with a template and a SIMULATED
  field observation at several noise levels.
- test_cases_draft.csv: 20 unseen test photos (outside test_core) with a template and
  an empty observation.

The simulated observation is drawn from the gold condition's KG symptoms, so it is
circular unless noise is reported with it: with probability `noise` it comes from
another condition. Scores on it are a sensitivity analysis, not a result. Test
observations must be written by a person looking at the photo, so this script leaves
them empty and nothing here looks at a test photo.

    python -I make_questions.py <repo root>
"""
import collections
import csv
import random
import sys
from pathlib import Path

import rdflib

R = rdflib.Namespace("https://w3id.org/ricemmkg#")
SEED = 0
SINGLE_SOURCE = {"NetrokonaRiceDataset", "YukeWbcDataset"}
NOISES = (0.0, 0.3, 0.5)
N_CASES = 20
HEALTHY = "the crop looks fine to me"
TEMPLATES = [("cause", "CQ-A01", "What is causing this on my rice?"),
             ("control", "CQ-A07", "How can I control this problem?"),
             ("symptom", "CQ-A03", "What other signs should I check for?"),
             ("environment", "CQ-A05", "Which weather or field conditions make this worse?"),
             ("stage", "CQ-A06", "At which crop stage does this do the most damage?")]
# plain words on purpose: not the KG labels, so matching them is not a string lookup
LAY = {"Chewed_Leaf": "something has been eating the leaves", "Dry_Leaf_Tip": "the leaf tips are drying out",
       "Leaf_Rolling": "the leaves are curling up", "Wilting": "the plants are drooping",
       "Yellow_Leaf": "the leaves have gone yellow", "Translucent_Stripe": "thin see-through lines between the veins",
       "Water_Soaked_Streak": "wet-looking streaks on the leaves", "Discolored_Panicle": "the heads have changed colour",
       "Empty_Grain": "many of the grains are empty", "Grain_Discoloration": "the grains are stained",
       "Hopper_Burn": "patches of the field look burnt and dry", "Brown_Lesion": "brown marks on the leaves",
       "Leaf_Spot": "spots on the leaves", "Excessive_Tillering": "far too many thin shoots",
       "Sterile_Panicle": "the heads set no seed", "Stunted_Growth": "the plants stay short",
       "Yellow_Stripe": "yellow lines along the leaves", "Brown_Leaf_Tip": "the leaf tips turned brown",
       "Leaf_Scratching": "the leaves look scraped", "White_Streak": "white lines on the leaves",
       "Black_Root": "the roots have turned black", "Leaf_Bronzing": "the leaves look bronze",
       "Reduced_Tillering": "very few shoots per plant", "Zonate_Leaf_Lesion": "large patches with bands on the leaves",
       "Yellowish_Green_Leaf": "the leaves are pale and light green", "Dark_Green_Erect_Leaf": "the leaves are very dark and stand straight up",
       "Delayed_Maturity": "the crop is ripening late", "Thin_Spindly_Stem": "the stems are thin and weak",
       "Lodging": "the plants have fallen over", "Necrotic_Leaf_Tip_Margin": "the leaf tips and edges are dead",
       "Yellowish_Brown_Leaf_Margin": "the leaf edges are yellow-brown", "Neck_Rot": "the stalk under the head has rotted",
       "Node_Lesion": "dark marks at the stem joints", "Panicle_Blast": "the head snaps at its base",
       "White_Ear": "the heads turned white and empty", "Yellow_Orange_Discoloration": "the leaves are turning orange",
       "Chlorotic_Leaf_Patch": "pale patches on the leaves", "White_Leaf_Tip": "the leaf tips turned white",
       "Leaf_Sheath_Lesion": "grey-green blotches low on the stem", "Tiller_Death": "whole shoots are dying",
       "Dead_Tiller": "some shoots are dead", "Deadheart": "the centre shoot has dried up",
       "Dusty_Brown_Spot": "dusty brown specks on the top leaves"}


def local(term):
    return str(term).split("#")[-1]


def read(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main(root):
    root = Path(root)
    here = root / "Retrieval Benchmark/splits"
    g = rdflib.Graph()
    g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
    sym = {local(e): sorted(local(s) for s in g.objects(e, R.indicatedBy)) for e in set(g.subjects(R.indicatedBy, None))}
    assert {s for v in sym.values() for s in v} == set(LAY)
    gold = {r["image"]: r["gold"] for r in read(here / "gold.csv")}
    write(here / "question_templates.csv", [{"intent": i, "cq": c, "question": q} for i, c, q in TEMPLATES])

    rng = random.Random(SEED)
    conditions = sorted(sym)
    out = []
    for r in read(here / "dev_core.csv"):
        if r["dataset"] in SINGLE_SOURCE:
            continue
        e = gold[r["image"]]
        intent, _, question = rng.choice(TEMPLATES)
        row = {"image": r["image"], "gold": e, "intent": intent, "question": question}
        draw, other = rng.random(), rng.choice([c for c in conditions if c != e])
        wrong = LAY[rng.choice(sym[other])]
        right = LAY[rng.choice(sym[e])] if e in sym else HEALTHY
        for noise in NOISES:
            row[f"observation_{noise}"] = wrong if draw < noise else right
        out.append(row)
    write(here / "questions_dev.csv", out)

    core = {r["image"] for r in read(here / "test_core.csv")}
    per = collections.defaultdict(list)
    for r in sorted(read(here / "images_split.csv"), key=lambda r: r["image"]):
        if r["split"] == "test" and r["image"] not in core and r["dataset"] not in SINGLE_SOURCE:
            per[gold[r["image"]]].append(r)
    names = sorted(per)
    rng.shuffle(names)
    cases = []
    for k in range(N_CASES):
        e = names[k % len(names)]
        r = rng.choice(per[e])
        intent, cq, question = TEMPLATES[k % len(TEMPLATES)]
        cases.append({"case": k + 1, "image": r["image"], "url": r["url"], "gold": e, "intent": intent, "cq": cq,
                      "question": question, "observation": ""})
    write(here / "test_cases_draft.csv", cases)
    print(len(out), "dev questions;", len(cases), "test cases;", collections.Counter(c["gold"] for c in cases).most_common(3))


if __name__ == "__main__":
    main(sys.argv[1])
