#!/usr/bin/env python3
"""Task 1.4 — apply a human-completed AGROVOC alignment CSV.

Reads reports/agrovoc_todo.csv (columns: individual, agrovoc_iri, match_type)
and asserts skos:exactMatch / skos:closeMatch accordingly. Rows with an empty
agrovoc_iri are skipped (still pending human lookup). match_type must be
exactly "exactMatch" or "closeMatch".
"""
import argparse
import csv
import sys
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import SKOS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
VALID_MATCH_TYPES = {"exactMatch": SKOS.exactMatch, "closeMatch": SKOS.closeMatch}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--csv", default="reports/agrovoc_todo.csv")
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    g = Graph()
    g.parse(args.input, format="xml")

    applied, skipped, errors = 0, 0, []
    for row in rows:
        iri = row.get("agrovoc_iri", "").strip()
        match_type = row.get("match_type", "").strip()
        individual = row.get("individual", "").strip()
        if not iri:
            skipped += 1
            continue
        if match_type not in VALID_MATCH_TYPES:
            errors.append(f"{individual}: invalid match_type '{match_type}'")
            continue
        g.add((RICE[individual], VALID_MATCH_TYPES[match_type], URIRef(iri)))
        applied += 1

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    g.bind("rice", RICE)
    g.bind("skos", SKOS)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Applied {applied} alignment triples, {skipped} rows still pending.")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
