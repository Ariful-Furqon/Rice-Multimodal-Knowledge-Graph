#!/usr/bin/env python3
"""Task B.2 apply step — read a human-completed reports/alignment_refine.csv
back and retarget each row's skos:<current_match> to skos:<proposed_match>.

A row with an empty proposed_match is left untouched (not yet decided).
A row with a non-empty proposed_match is validated against the allowed
set (exactMatch/closeMatch/broadMatch/narrowMatch) before being applied.
Nothing is guessed: this script only ever does what the completed CSV
says.
"""
import argparse
import csv
from rdflib import Graph, Namespace, URIRef

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
ALLOWED = {"exactMatch", "closeMatch", "broadMatch", "narrowMatch"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("csv_path")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input)

    applied = 0
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            proposed = row["proposed_match"].strip()
            if not proposed:
                continue
            if proposed not in ALLOWED:
                raise ValueError(
                    f"{row['individual']}: proposed_match '{proposed}' is not one of {ALLOWED}"
                )
            s = RICE[row["individual"]]
            o = URIRef(row["current_iri"])
            current_prop = SKOS[row["current_match"].strip()]
            new_prop = SKOS[proposed]
            old_triple = (s, current_prop, o)
            if old_triple not in g:
                print(f"Skip {row['individual']}: {old_triple} not found (already applied?)")
                continue
            g.remove(old_triple)
            g.add((s, new_prop, o))
            applied += 1
            print(f"{row['individual']}: {row['current_match']} -> {proposed}")

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Applied {applied} refinements. Wrote {args.output}")


if __name__ == "__main__":
    main()
