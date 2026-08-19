#!/usr/bin/env python3
"""Task A.1 (part 2) — apply a human-completed reports/dataset_metadata.csv,
replacing the TODO literal for each property with its new_value.
"""
import argparse
import csv
from rdflib import Graph, Namespace, URIRef, Literal

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--csv", default="reports/dataset_metadata.csv")
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    g = Graph()
    g.parse(args.input, format="xml")

    dataset = RICE.PaddyDoctorDataset
    applied, skipped = 0, 0
    for row in rows:
        prop = URIRef(row["property"])
        new_value = row["new_value"].strip()
        if not new_value:
            skipped += 1
            continue
        g.remove((dataset, prop, None))
        g.add((dataset, prop, Literal(new_value)))
        applied += 1

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Applied {applied} metadata values, {skipped} still pending.")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
