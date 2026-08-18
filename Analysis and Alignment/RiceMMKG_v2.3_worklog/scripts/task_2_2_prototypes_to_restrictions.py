#!/usr/bin/env python3
"""Task 2.2 — convert four of the five class-as-instance prototype
individuals into owl:someValuesFrom restrictions, then delete all five
prototype individuals and their assertions.

rice:LeafImage is deliberately left WITHOUT a captures restriction: applying
`LeafImage subClassOf captures someValuesFrom Symptom` would assert every
leaf image captures some symptom, which is false for the 1,764 images
annotated as HealthStatus (healthy plants). See reports/task_2_2_caveat.md.
"""
import argparse
from rdflib import Graph, Namespace, BNode, RDF, RDFS, OWL

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

RESTRICTIONS = [
    # (target class, property, filler class)
    ("SensorReading", "captures", "EnvironmentalFactor"),
    ("FieldObservation", "detects", "Pest"),
    ("DiseaseReport", "detects", "Disease"),
    ("FarmerReport", "detects", "Disease"),
]

PROTOTYPES = [
    "Leaf_Image", "Sensor_Reading", "Field_Observation", "Farmer_Report", "Disease_Report",
]


def add_restrictions(g):
    added = 0
    for cls_name, prop_name, filler_name in RESTRICTIONS:
        cls = RICE[cls_name]
        prop = RICE[prop_name]
        filler = RICE[filler_name]

        # idempotency: skip if an equivalent restriction already exists
        exists = False
        for r in g.objects(cls, RDFS.subClassOf):
            if (r, OWL.onProperty, prop) in g and (r, OWL.someValuesFrom, filler) in g:
                exists = True
                break
        if exists:
            continue

        r = BNode()
        g.add((r, RDF.type, OWL.Restriction))
        g.add((r, OWL.onProperty, prop))
        g.add((r, OWL.someValuesFrom, filler))
        g.add((cls, RDFS.subClassOf, r))
        added += 1
    return added


def remove_prototypes(g):
    removed_triples = 0
    removed_individuals = 0
    for local in PROTOTYPES:
        ind = RICE[local]
        triples = list(g.triples((ind, None, None)))
        if not triples:
            continue
        for t in triples:
            g.remove(t)
            removed_triples += 1
        removed_individuals += 1
    return removed_individuals, removed_triples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")

    added = add_restrictions(g)
    removed_ind, removed_triples = remove_prototypes(g)

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")

    print(f"Restrictions added: {added}")
    print(f"Prototype individuals removed: {removed_ind}")
    print(f"Prototype triples removed: {removed_triples}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
