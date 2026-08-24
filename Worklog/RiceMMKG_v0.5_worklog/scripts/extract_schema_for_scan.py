#!/usr/bin/env python3
"""Task C.1 helper — extract a schema + domain-individuals-only copy of
the ontology (drop the 10,407 rice:ImageObservation instances and their
annotatedAs/captures/wasDerivedFrom triples) for submission to OOPS!/
FOOPS!, both of which evaluate ontology *modelling* pitfalls, not
instance-data volume. The full 7+ MB file is impractical to POST and the
image instances contribute nothing to either tool's checks.
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
    g.parse(args.input)

    images = set(g.subjects(RDF.type, RICE.ImageObservation))
    removed = 0
    for img in images:
        for t in list(g.triples((img, None, None))):
            g.remove(t)
            removed += 1
        for t in list(g.triples((None, None, img))):
            g.remove(t)
            removed += 1

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Removed {len(images)} ImageObservation individuals ({removed} triples). "
          f"Remaining: {len(g)} triples.")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
