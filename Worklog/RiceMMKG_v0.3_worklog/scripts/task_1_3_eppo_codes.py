#!/usr/bin/env python3
"""Task 1.3 — add rice:eppoCode annotation property with three verified codes,
an altLabel for Magnaporthe_Oryzae, and TODO comments for the remaining six
organisms whose EPPO codes have not been verified.
"""
import argparse
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD
from rdflib.namespace import SKOS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

VERIFIED_CODES = {
    "Brown_Planthopper": "NILALU",
    "Magnaporthe_Oryzae": "PYRIOR",
    "Xanthomonas_Oryzae": "XANTOR",
}

TODO_ORGANISMS = [
    "Bipolaris_Oryzae", "Hispa", "Leaf_Folder", "Stem_Borer", "Rice_Bug", "Armyworm",
]

TODO_TEXT = Literal("TODO: verify EPPO code at gd.eppo.int")


def apply(g):
    eppo_code = RICE.eppoCode
    if (eppo_code, RDF.type, OWL.AnnotationProperty) not in g:
        g.add((eppo_code, RDF.type, OWL.AnnotationProperty))
        g.add((eppo_code, RDFS.label, Literal("EPPO code")))
        g.add((eppo_code, RDFS.range, XSD.string))

    for local, code in VERIFIED_CODES.items():
        ind = RICE[local]
        g.remove((ind, eppo_code, None))
        g.add((ind, eppo_code, Literal(code, datatype=XSD.string)))

    alt = Literal("Pyricularia oryzae")
    g.remove((RICE.Magnaporthe_Oryzae, SKOS.altLabel, None))
    g.add((RICE.Magnaporthe_Oryzae, SKOS.altLabel, alt))

    for local in TODO_ORGANISMS:
        ind = RICE[local]
        if (ind, RDFS.comment, TODO_TEXT) not in g:
            g.add((ind, RDFS.comment, TODO_TEXT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    apply(g)
    g.bind("rice", RICE)
    g.bind("skos", SKOS)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
