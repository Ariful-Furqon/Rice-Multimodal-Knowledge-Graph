#!/usr/bin/env python3
"""Task 1.2 — rename LeafImage -> ImageObservation, SensorReading -> SensorObservation."""
import argparse
from rdflib import Graph, Namespace

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

RENAMES = {
    "LeafImage": "ImageObservation",
    "SensorReading": "SensorObservation",
}


def rename_uri(g, old, new):
    for s, p, o in list(g.triples((old, None, None))):
        g.remove((s, p, o))
        g.add((new, p, o))
    for s, p, o in list(g.triples((None, old, None))):
        g.remove((s, p, o))
        g.add((s, new, o))
    for s, p, o in list(g.triples((None, None, old))):
        g.remove((s, p, o))
        g.add((s, p, new))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    for old_local, new_local in RENAMES.items():
        old = RICE[old_local]
        new = RICE[new_local]
        n_before = sum(1 for _ in g.triples((None, None, old)))
        rename_uri(g, old, new)
        print(f"{old_local} -> {new_local}: {n_before} references retargeted")

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
