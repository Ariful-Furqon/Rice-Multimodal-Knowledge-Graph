#!/usr/bin/env python3
"""Task 2.2b (not in the worklog, required to make it self-consistent) —
retarget existing condition-relation assertions from Pest individuals to
their Infestation counterparts.

Task 1.4 narrowed indicatedBy/increaseRiskOf/vulnerableTo/occursIn/
controlledBy/recommends to Disease |_| Infestation (dropping Pest), and
Task 1.6 made Pest and Infestation disjoint. But 43 existing individual-
level assertions still pointed a Pest individual into those now-invalid
positions (e.g. "Stem_Borer indicatedBy Deadheart",
"High_Temperature increaseRiskOf Stem_Borer") — the worklog never states a
migration step for this data. Per user decision, they are retargeted to
the matching Infestation individual created in Task 2.2, consistent with
the Infestation split's own logic: damage/risk/control/co-occurrence
relations describe the condition, not the organism.

rice:causes (Pest -> Infestation, from Task 2.2) and the evidence-path
properties (detects/detectedBy, transmits/transmittedBy, which correctly
target the organism) are untouched.
"""
import argparse
from rdflib import Graph, Namespace, RDF

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

PEST_TO_INFESTATION = {
    "Hispa": "Hispa_Leaf_Damage",
    "Armyworm": "Armyworm_Defoliation",
    "Brown_Planthopper": "Brown_Planthopper_Infestation",
    "Leaf_Folder": "Leaf_Folder_Damage",
    "Rice_Bug": "Rice_Bug_Grain_Damage",
    "Stem_Borer": "Stem_Borer_Damage",
}

# properties whose domain or range was narrowed to Disease|Infestation
AFFECTED_PROPERTIES = [
    "indicatedBy", "indicates",
    "increaseRiskOf", "riskIncreasedBy",
    "vulnerableTo", "threatens",
    "occursIn", "hasOccurrenceOf",
    "controlledBy", "controls",
    "preventedBy", "prevents",
    "recommends", "recommendedFor",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    pest_map = {RICE[k]: RICE[v] for k, v in PEST_TO_INFESTATION.items()}

    retargeted = []
    for prop_name in AFFECTED_PROPERTIES:
        prop = RICE[prop_name]
        for s, p, o in list(g.triples((None, prop, None))):
            new_s = pest_map.get(s, s)
            new_o = pest_map.get(o, o)
            if new_s != s or new_o != o:
                g.remove((s, p, o))
                g.add((new_s, p, new_o))
                retargeted.append((prop_name, str(s).split("#")[-1], str(o).split("#")[-1],
                                    str(new_s).split("#")[-1], str(new_o).split("#")[-1]))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")

    print(f"Assertions retargeted: {len(retargeted)}")
    for prop_name, os_, oo, ns, no in retargeted:
        print(f"  {prop_name}: {os_} -> {oo}   becomes   {ns} -> {no}")
    print(f"Triple count before: {before}, after: {after} (retargeting is 1:1, no net change expected)")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
