#!/usr/bin/env python3
"""Task A.3 — delete image-side sourceDatasetLabel assertions (the label is
reachable via annotatedAs already) and declare its domain as the same
four-way union annotatedAs carries.
"""
import argparse
from rdflib import Graph, Namespace, BNode, RDF, RDFS, OWL
from rdflib.collection import Collection

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

DOMAIN_CLASSES = ["Disease", "HealthStatus", "Pest", "Symptom"]


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
    for s, p, o in list(g.triples((None, RICE.sourceDatasetLabel, None))):
        if s in images:
            g.remove((s, p, o))
            removed += 1

    prop = RICE.sourceDatasetLabel
    domain_node = BNode()
    g.add((domain_node, RDF.type, OWL.Class))
    coll = Collection(g, BNode(), [RICE[c] for c in DOMAIN_CLASSES])
    g.add((domain_node, OWL.unionOf, coll.uri))
    g.add((prop, RDFS.domain, domain_node))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"sourceDatasetLabel triples removed from images: {removed}")
    print(f"sourceDatasetLabel domain declared: Disease|HealthStatus|Pest|Symptom")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
