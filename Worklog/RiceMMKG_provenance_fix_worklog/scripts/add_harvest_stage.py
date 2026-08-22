#!/usr/bin/env python3
"""Give Harvest_Stage its first domain-property assertion: Crop_Sanitation
requires Harvest_Stage, reified with the same BBPOPT citation already used
for Crop_Sanitation's rdfs:comment ("reduce inoculum carry-over between
seasons"), matching the existing rice:requires axiom pattern.
"""
import argparse
from rdflib import Graph, Namespace, RDF, OWL, BNode, Literal

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    s, p, o = RICE.Crop_Sanitation, RICE.requires, RICE.Harvest_Stage
    assert (s, p, o) not in g, "triple already present"
    g.add((s, p, o))

    ax = BNode()
    g.add((ax, RDF.type, OWL.Axiom))
    g.add((ax, OWL.annotatedSource, s))
    g.add((ax, OWL.annotatedProperty, p))
    g.add((ax, OWL.annotatedTarget, o))
    from rdflib import URIRef
    g.add((ax, DCTERMS.source, URIRef("https://bbpopt.ditlin.pertanian.go.id/")))
    g.add((ax, DCTERMS.bibliographicCitation, Literal(
        "BBPOPT (2022). Pedoman Pengamatan dan Pengendalian Organisme "
        "Pengganggu Tumbuhan Tanaman Padi. Balai Besar Peramalan Organisme "
        "Pengganggu Tumbuhan, Kementerian Pertanian Republik Indonesia."
    )))
    g.add((ax, RICE.evidenceType, Literal("literature-curated")))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
