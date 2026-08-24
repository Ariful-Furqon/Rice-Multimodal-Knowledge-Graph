#!/usr/bin/env python3
"""Task B.2 — restore AllDisjointClasses {ImageObservation, SensorObservation}.
SymptomaticObservation is deliberately excluded -- it's a defined subclass
of Observation and overlaps ImageObservation by design.
"""
import argparse
from rdflib import Graph, Namespace, BNode, RDF, OWL
from rdflib.collection import Collection

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

MEMBERS = ["ImageObservation", "SensorObservation"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    ax = BNode()
    g.add((ax, RDF.type, OWL.AllDisjointClasses))
    coll = Collection(g, BNode(), [RICE[c] for c in MEMBERS])
    g.add((ax, OWL.members, coll.uri))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"AllDisjointClasses added: {MEMBERS}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
