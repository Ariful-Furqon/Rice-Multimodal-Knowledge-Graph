#!/usr/bin/env python3
"""Task 2.3 — for every ImageObservation whose annotatedAs label denotes
Deadheart (a Symptom), add rice:captures rice:Deadheart.
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

    # Find the AnnotationLabel(s) that denote Deadheart
    deadheart_labels = {s for s in g.subjects(RICE.denotes, RICE.Deadheart)}
    assert len(deadheart_labels) == 1, f"expected exactly one label denoting Deadheart, got {len(deadheart_labels)}"

    added = 0
    for img, _, label in g.triples((None, RICE.annotatedAs, None)):
        if label in deadheart_labels:
            triple = (img, RICE.captures, RICE.Deadheart)
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
