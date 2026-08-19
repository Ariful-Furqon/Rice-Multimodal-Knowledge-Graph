#!/usr/bin/env python3
"""Task 1.5 — convert observation-modality restrictions from someValuesFrom
to allValuesFrom, and add the five allValuesFrom restrictions from the
design doc's S5.1.

Also cleans up three orphaned owl:Restriction blank nodes left dangling by
Task 1.1's deletion of FieldObservation/FarmerReport/DiseaseReport (their
subClassOf triple was removed, but the restriction node's own triples were
not, since those triples have the blank node as subject, not the deleted
class).
"""
import argparse
from rdflib import Graph, Namespace, BNode, RDF, RDFS, OWL
from rdflib.collection import Collection

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


def remove_orphan_restrictions(g):
    referenced = set(g.objects(None, RDFS.subClassOf))
    removed = 0
    for r in list(g.subjects(RDF.type, OWL.Restriction)):
        if r not in referenced:
            for t in list(g.triples((r, None, None))):
                g.remove(t)
                removed += 1
    return removed


def make_class_expr(g, locals_):
    if len(locals_) == 1:
        return RICE[locals_[0]]
    coll = Collection(g, BNode(), [RICE[l] for l in locals_])
    node = BNode()
    g.add((node, RDF.type, OWL.Class))
    g.add((node, OWL.unionOf, coll.uri))
    return node


def add_all_values_restriction(g, cls_local, prop_local, range_locals):
    cls = RICE[cls_local]
    prop = RICE[prop_local]
    filler = make_class_expr(g, range_locals)
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, prop))
    g.add((r, OWL.allValuesFrom, filler))
    g.add((cls, RDFS.subClassOf, r))


NEW_RESTRICTIONS = [
    ("ImageObservation", "captures", ["Symptom"]),
    ("ImageObservation", "detects", ["Pest"]),
    ("SensorObservation", "captures", ["EnvironmentalFactor"]),
    ("TextualReport", "captures", ["Symptom"]),
    ("TextualReport", "detects", ["Pest", "Pathogen"]),
]

TEXTUAL_REPORT_COMMENT = (
    "TextualReport is deliberately the least constrained modality: a "
    "written report can both describe appearance (captures a Symptom) and "
    "name an organism (detects a Pest or Pathogen)."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    orphans_removed = remove_orphan_restrictions(g)

    # Remove the one live someValuesFrom restriction (SensorObservation captures
    # EnvironmentalFactor) -- it's superseded by the allValuesFrom version below.
    some_removed = 0
    for r in list(g.subjects(RDF.type, OWL.Restriction)):
        if any(g.triples((r, OWL.someValuesFrom, None))):
            for s in list(g.subjects(RDFS.subClassOf, r)):
                g.remove((s, RDFS.subClassOf, r))
            for t in list(g.triples((r, None, None))):
                g.remove(t)
                some_removed += 1

    for cls_local, prop_local, range_locals in NEW_RESTRICTIONS:
        add_all_values_restriction(g, cls_local, prop_local, range_locals)

    g.add((RICE.TextualReport, RDFS.comment, __import__("rdflib").Literal(TEXTUAL_REPORT_COMMENT)))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Orphaned restriction triples removed: {orphans_removed}")
    print(f"someValuesFrom restriction triples removed: {some_removed}")
    print(f"allValuesFrom restrictions added: {len(NEW_RESTRICTIONS)}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
