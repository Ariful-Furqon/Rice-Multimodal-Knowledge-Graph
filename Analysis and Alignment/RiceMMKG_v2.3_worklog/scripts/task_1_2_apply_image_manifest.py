#!/usr/bin/env python3
"""Task 1.2 (part 2) — apply the verified image manifest to the ontology.

For every rice:LeafImage individual with a non-empty relative_path in the
manifest, assert schema:contentUrl (the path) and dcterms:source (pointing
to rice:PaddyDoctorDataset, added in Task 1.1). Refuses to run if the
manifest has any unresolved (empty-path) rows — partial application is a
failure per the worklog.
"""
import argparse
import csv
import sys
from rdflib import Graph, Namespace, URIRef, Literal, RDF

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
SCHEMA = Namespace("http://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--manifest", default="reports/image_manifest.csv")
    args = ap.parse_args()

    with open(args.manifest, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    unresolved = [r for r in rows if not r["relative_path"].strip()]
    if unresolved:
        print(
            f"{len(unresolved)} manifest rows have no relative_path. "
            "Refusing partial application.",
            file=sys.stderr,
        )
        sys.exit(1)

    g = Graph()
    g.parse(args.input, format="xml")

    dataset = RICE.PaddyDoctorDataset
    n = 0
    for row in rows:
        ind = URIRef(row["individual_iri"])
        path = row["relative_path"].strip()
        g.add((ind, SCHEMA.contentUrl, Literal(path)))
        g.add((ind, DCTERMS.source, dataset))
        n += 1

    g.bind("rice", RICE)
    g.bind("schema", SCHEMA)
    g.bind("dcterms", DCTERMS)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Applied contentUrl + dcterms:source to {n} LeafImage individuals.")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
