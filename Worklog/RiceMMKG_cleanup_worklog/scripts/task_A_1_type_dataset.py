#!/usr/bin/env python3
"""Task A.1 — type PaddyDoctorDataset as dcat:Dataset, and emit a CSV for
the three TODO metadata literals (title/license/source) rather than
guessing them.
"""
import argparse
import csv
import os
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL
from rdflib.namespace import DCTERMS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--csv", default="reports/dataset_metadata.csv")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    dataset = RICE.PaddyDoctorDataset

    if (DCAT.Dataset, RDF.type, OWL.Class) not in g:
        g.add((DCAT.Dataset, RDF.type, OWL.Class))
        g.add((DCAT.Dataset, RDFS.label, Literal("Dataset")))

    g.add((dataset, RDF.type, DCAT.Dataset))

    os.makedirs(os.path.dirname(args.csv), exist_ok=True)
    rows = []
    for prop in (DCTERMS.title, DCTERMS.license, DCTERMS.source):
        current = g.value(dataset, prop)
        rows.append((str(prop), str(current) if current is not None else "", ""))
    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["property", "current_value", "new_value"])
        w.writerows(rows)

    after = len(g)
    g.bind("rice", RICE)
    g.bind("dcat", DCAT)
    g.bind("dcterms", DCTERMS)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"PaddyDoctorDataset typed as dcat:Dataset")
    print(f"Wrote {args.csv} ({len(rows)} rows)")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
