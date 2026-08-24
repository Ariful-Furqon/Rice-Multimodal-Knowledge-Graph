#!/usr/bin/env python3
"""Task 1.2 — Checkpoint C1 resolved per the worklog's own recommendation:
keep rice:captures and rice:detects declared (unasserted) rather than
delete them, since Task 3.1 populates captures from data that already
exists.

Also states in an ontology-level comment that only one direction of each
inverse pair is asserted, so the twelve unasserted inverse properties
(annotationOf, capturedBy, causedBy, controls, detectedBy, hasOccurrenceOf,
indicates, prevents, recommendedFor, requiredFor, riskIncreasedBy,
threatens) are not mistaken for missing data.
"""
import argparse
from rdflib import Graph, Namespace, URIRef, Literal, RDFS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
ONTOLOGY_IRI = URIRef("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG")

INVERSE_NOTE = Literal(
    "Object properties are declared in inverse pairs, but only one direction "
    "of each pair is asserted in the data (the reasoner derives the other). "
    "This is a modelling choice, not missing data -- e.g. indicatedBy is "
    "populated while its inverse indicates is not."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    if (ONTOLOGY_IRI, RDFS.comment, INVERSE_NOTE) not in g:
        g.add((ONTOLOGY_IRI, RDFS.comment, INVERSE_NOTE))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print("captures/detects: kept declared, unasserted (Checkpoint C1 -> keep)")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
