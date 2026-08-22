#!/usr/bin/env python3
"""Remove owl:Axiom reifications (and their dcterms:source/bibliographicCitation/
rice:evidenceType annotations) that were mistakenly attached to non-domain triples
(rdfs:subPropertyOf schema declarations and skos:exactMatch/closeMatch alignments)
during the 2026-08-21 provenance enrichment. Only the 9 domain relations
(causes, indicatedBy, occursIn, controlledBy, preventedBy, increaseRiskOf,
vulnerableTo, recommends, requires) should carry literature-citation provenance.
"""
import argparse
from rdflib import Graph, Namespace, RDF, OWL

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

DOMAIN_PROPS = [
    "vulnerableTo", "occursIn", "causes", "indicatedBy", "increaseRiskOf",
    "controlledBy", "recommends", "preventedBy", "requires",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    domain_prop_uris = {RICE[p] for p in DOMAIN_PROPS}

    axioms = list(g.subjects(RDF.type, OWL.Axiom))
    removed_axioms = 0
    removed_triples = 0
    for ax in axioms:
        p = g.value(ax, OWL.annotatedProperty)
        if p in domain_prop_uris:
            continue
        # Remove every triple with this axiom node as subject.
        for t in list(g.triples((ax, None, None))):
            g.remove(t)
            removed_triples += 1
        removed_axioms += 1

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Spurious owl:Axiom nodes removed: {removed_axioms}")
    print(f"Triples removed: {removed_triples}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
