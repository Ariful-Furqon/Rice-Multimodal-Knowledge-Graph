#!/usr/bin/env python3
"""Add verified skos:exactMatch/closeMatch triples from
agrovoc_alignment_verified.csv (rows with a non-empty candidate_iri).
Matches the existing bare-triple pattern used by the ontology's prior
AGROVOC alignments - no owl:Axiom reification for SKOS mappings.
"""
import argparse
import csv
from rdflib import Graph, Namespace, URIRef

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("csv_path")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    added = 0
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            iri = row["candidate_iri"].strip()
            if not iri:
                continue
            match_type = row["match_type"].strip()
            assert match_type in ("exactMatch", "closeMatch"), row
            s = RICE[row["individual"]]
            p = SKOS[match_type]
            o = URIRef(iri)
            assert (s, None, None) in g, f"unknown individual {row['individual']}"
            if (s, p, o) in g:
                continue
            g.add((s, p, o))
            added += 1

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"SKOS triples added: {added}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
