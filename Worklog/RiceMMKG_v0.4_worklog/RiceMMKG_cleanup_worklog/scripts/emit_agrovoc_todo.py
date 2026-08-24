#!/usr/bin/env python3
"""Task C.2 — emit reports/agrovoc_todo.csv, grouped by type, for every
domain individual currently lacking skos:exactMatch/closeMatch. Computed
from the live ontology rather than the worklog's stated grouping, which
undercounts (it says all 11 Symptom individuals are unaligned; only 9
actually are -- Leaf_Spot and Wilting already have alignment).
"""
import argparse
import csv
from rdflib import Graph, Namespace, RDF, OWL
from rdflib.namespace import SKOS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

GROUP_BY_TYPE = {
    "Disease": "Diseases and pests",
    "Pest": "Diseases and pests",
    "Symptom": "Symptoms",
    "SeverityLevel": "Management, severity, stages",
    "ManagementAction": "Management, severity, stages",
    "GrowthStage": "Management, severity, stages",
    "HealthStatus": "Management, severity, stages",
    "Treatment": "Management, severity, stages",
    "EnvironmentalFactor": "Management, severity, stages",
}

DOMAIN_CLASSES = set(GROUP_BY_TYPE) | {"Pathogen", "Plant"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--csv", default="reports/agrovoc_todo.csv")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")

    classes = [c for c in g.subjects(RDF.type, OWL.Class) if str(c).rsplit("#", 1)[-1] in DOMAIN_CLASSES]
    inds = set()
    for c in classes:
        for i in g.subjects(RDF.type, c):
            inds.add(i)
    aligned = set()
    for s, _, _ in g.triples((None, SKOS.exactMatch, None)):
        aligned.add(s)
    for s, _, _ in g.triples((None, SKOS.closeMatch, None)):
        aligned.add(s)
    unaligned = sorted(inds - aligned, key=str)

    rows = []
    for i in unaligned:
        local = str(i).rsplit("#", 1)[1]
        types = [str(t).rsplit("#", 1)[1] for t in g.objects(i, RDF.type) if t != OWL.NamedIndividual]
        group = GROUP_BY_TYPE.get(types[0], "Other") if types else "Other"
        rows.append((local, group))

    rows.sort(key=lambda r: (r[1], r[0]))

    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["individual", "group", "candidate_iri", "match_type"])
        w.writerows([(r[0], r[1], "", "") for r in rows])

    print(f"Wrote {args.csv}: {len(rows)} rows")
    from collections import Counter
    for group, cnt in Counter(r[1] for r in rows).items():
        print(f"  {group}: {cnt}")


if __name__ == "__main__":
    main()
