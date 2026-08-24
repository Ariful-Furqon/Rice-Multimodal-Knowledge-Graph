#!/usr/bin/env python3
"""Task B.1 — Checkpoint C3, applying the worklog's recommendation:
rename LeafImage -> ImageObservation (names the medium; LeafImage is
factually wrong for panicle/tiller symptoms in part of the corpus).
"""
import argparse
from rdflib import Graph, Namespace, RDFS, Literal

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


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

    old, new = RICE.LeafImage, RICE.ImageObservation
    n_before = sum(1 for _ in g.triples((None, None, old))) + sum(1 for _ in g.triples((old, None, None)))
    rename_uri(g, old, new)

    g.remove((new, RDFS.label, Literal("Leaf Image")))
    g.add((new, RDFS.label, Literal("Image Observation")))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"LeafImage -> ImageObservation: {n_before} triples touched")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
