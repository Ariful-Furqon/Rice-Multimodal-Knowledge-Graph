#!/usr/bin/env python3
"""Task 3.1 — for every LeafImage whose annotatedAs target is typed
Symptom, add captures to that same symptom. The only Symptom-typed
annotatedAs target is Deadheart (1,442 images).
"""
import argparse
from rdflib import Graph, Namespace, RDF

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    symptoms = set(g.subjects(RDF.type, RICE.Symptom))

    added = 0
    for img, _, target in g.triples((None, RICE.annotatedAs, None)):
        if target in symptoms:
            triple = (img, RICE.captures, target)
            if triple not in g:
                g.add(triple)
                added += 1

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"captures triples added: {added}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
