#!/usr/bin/env python3
"""Task 3.3 — apply a human-completed reports/alignment_check.csv and/or
reports/unaligned_entities.csv.

Both files share the same shape (individual/entity, agrovoc_iri or
resolution_agrovoc_iri, match_type or resolution_match_type). Rows with an
empty resolution are skipped. match_type must be exactly "exactMatch" or
"closeMatch". For alignment_check.csv rows (the two defects), applying a
resolution replaces the existing (defective) match rather than adding a
second one.
"""
import argparse
import csv
import sys
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import SKOS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
VALID = {"exactMatch": SKOS.exactMatch, "closeMatch": SKOS.closeMatch}


def entity_col(row):
    return row.get("entity") or row.get("individual")


def iri_col(row):
    return (row.get("resolution_agrovoc_iri") or row.get("agrovoc_iri") or "").strip()


def match_col(row):
    return (row.get("resolution_match_type") or row.get("match_type") or "").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--csv", action="append", required=True,
                     help="one or more completed CSVs; pass --csv multiple times")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")

    applied, skipped, errors = 0, 0, []
    for csv_path in args.csv:
        with open(csv_path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        is_defect_file = "current_agrovoc_iri" in rows[0] if rows else False

        for row in rows:
            entity = entity_col(row)
            iri = iri_col(row)
            match_type = match_col(row)
            if not iri:
                skipped += 1
                continue
            if match_type not in VALID:
                errors.append(f"{entity}: invalid match_type '{match_type}'")
                continue
            subj = RICE[entity]
            if is_defect_file:
                old_iri = row.get("current_agrovoc_iri", "").strip()
                old_type = row.get("match_type", "").strip()
                if old_iri and old_type in VALID:
                    g.remove((subj, VALID[old_type], URIRef(old_iri)))
            g.add((subj, VALID[match_type], URIRef(iri)))
            applied += 1

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Applied {applied} alignment triples, {skipped} rows still pending.")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
