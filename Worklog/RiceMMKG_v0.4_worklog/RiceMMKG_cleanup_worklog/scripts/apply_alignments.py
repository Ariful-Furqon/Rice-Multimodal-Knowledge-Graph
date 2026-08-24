#!/usr/bin/env python3
"""Tasks C.1/C.2 — apply human-completed alignment CSVs.

Supports both shapes:
- alignment_check.csv: individual, current_iri, verified_iri, match_type, resolves
  (resolves is a free-text note, not consumed; verified_iri replaces current_iri)
- agrovoc_todo.csv: individual, group, candidate_iri, match_type
  (adds a new match; group is metadata, not consumed)

Rejects any row whose match_type isn't exactly "exactMatch" or "closeMatch",
and any row whose IRI doesn't look like a resolvable http(s) URI.
"""
import argparse
import csv
import sys
import urllib.request
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import SKOS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
VALID = {"exactMatch": SKOS.exactMatch, "closeMatch": SKOS.closeMatch}


def check_resolves(iri, no_network):
    if no_network:
        return True
    try:
        req = urllib.request.Request(iri, method="HEAD")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return 200 <= resp.status < 400
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--csv", action="append", required=True)
    ap.add_argument("--no-network", action="store_true",
                     help="skip live IRI resolution check (offline/CI use)")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")

    applied, skipped, errors = 0, 0, []
    for csv_path in args.csv:
        with open(csv_path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        is_check_file = rows and "current_iri" in rows[0]

        for row in rows:
            individual = row["individual"]
            new_iri = (row.get("verified_iri") or row.get("candidate_iri") or "").strip()
            match_type = row.get("match_type", "").strip()
            if not new_iri:
                skipped += 1
                continue
            if match_type not in VALID:
                errors.append(f"{individual}: invalid match_type '{match_type}'")
                continue
            if not new_iri.startswith(("http://", "https://")):
                errors.append(f"{individual}: '{new_iri}' is not an http(s) IRI")
                continue
            if not check_resolves(new_iri, args.no_network):
                errors.append(f"{individual}: '{new_iri}' does not resolve")
                continue

            subj = RICE[individual]
            if is_check_file:
                old_iri = row.get("current_iri", "").strip()
                if old_iri:
                    g.remove((subj, SKOS.exactMatch, URIRef(old_iri)))
                    g.remove((subj, SKOS.closeMatch, URIRef(old_iri)))
            g.add((subj, VALID[match_type], URIRef(new_iri)))
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
