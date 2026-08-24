#!/usr/bin/env python3
"""Task A.2 — delete dcterms:source on image individuals only (redundant
with prov:wasDerivedFrom, which is kept). dcterms:source on the ontology
node and on PaddyDoctorDataset itself is untouched.
"""
import argparse
from rdflib import Graph, Namespace, RDF
from rdflib.namespace import DCTERMS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    images = set(g.subjects(RDF.type, RICE.LeafImage))
    removed = 0
    for s, p, o in list(g.triples((None, DCTERMS.source, None))):
        if s in images:
            g.remove((s, p, o))
            removed += 1

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"dcterms:source triples removed from images: {removed}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
