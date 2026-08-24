#!/usr/bin/env python3
"""Task 3.2 — the single defined class:
rice:SymptomaticObservation = Observation and (captures some Symptom)
"""
import argparse
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL
from rdflib.collection import Collection

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    cls = RICE.SymptomaticObservation
    g.add((cls, RDF.type, OWL.Class))
    g.add((cls, RDFS.label, Literal("Symptomatic Observation")))
    g.add((cls, RDFS.comment, Literal(
        "Defined class: any Observation that captures at least one Symptom. "
        "Membership is inferred from captures assertions, not asserted "
        "directly. The minimum defined class needed to demonstrate that "
        "reasoning does something over this data."
    )))

    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, RICE.captures))
    g.add((r, OWL.someValuesFrom, RICE.Symptom))

    expr = BNode()
    g.add((expr, RDF.type, OWL.Class))
    coll = Collection(g, BNode(), [RICE.Observation, r])
    g.add((expr, OWL.intersectionOf, coll.uri))

    g.add((cls, OWL.equivalentClass, expr))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
