#!/usr/bin/env python3
"""Task 2.2 — apply a human-completed reports/vector_todo.csv.

Columns: pest, transmits_pathogen (a rice:<local> IRI local name, or the
IRI itself), source_citation (required whenever transmits_pathogen is set).
Rows with an empty transmits_pathogen are skipped. If transmits_pathogen
names a Pathogen not yet in the ontology (e.g. the rice tungro virus /
leafhopper case — see reports/task_2_2_vector_notes.md), the pathogen
individual must be created first; this script does not create pathogens
from a bare string, since that would mean guessing its identity.
"""
import argparse
import csv
import sys
from rdflib import Graph, Namespace, URIRef, RDF

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


def resolve(value):
    value = value.strip()
    if not value:
        return None
    if value.startswith("http://") or value.startswith("https://"):
        return URIRef(value)
    return RICE[value]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--csv", default="reports/vector_todo.csv")
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    g = Graph()
    g.parse(args.input, format="xml")

    applied, skipped, errors = 0, 0, []
    for row in rows:
        pathogen_raw = row.get("transmits_pathogen", "").strip()
        citation = row.get("source_citation", "").strip()
        pest_local = row.get("pest", "").strip()
        if not pathogen_raw:
            skipped += 1
            continue
        if not citation:
            errors.append(f"{pest_local}: transmits_pathogen set without source_citation")
            continue
        pest = RICE[pest_local]
        pathogen = resolve(pathogen_raw)
        if (pathogen, RDF.type, RICE.Pathogen) not in g:
            errors.append(
                f"{pest_local}: '{pathogen_raw}' is not a declared rice:Pathogen individual "
                "in this ontology — create it first, do not guess."
            )
            continue
        g.add((pest, RICE.transmits, pathogen))
        applied += 1

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Applied {applied} transmits triples, {skipped} rows still pending.")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
