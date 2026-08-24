#!/usr/bin/env python3
"""Task A.0 (found during A.2, not in the original worklog) — remove 9
rice:exactMatch triples introduced in the 2026-08-21 "Provenance per
Assertion" commit.

These use an UNDECLARED property `rice:exactMatch` (never declared as an
owl:AnnotationProperty, distinct from `skos:exactMatch`) and every one of
the 9 AGROVOC codes was checked against the live AGROVOC REST API
(agrovoc.fao.org/browse/rest/v1/data) on 2026-08-22:

    Individual                       IRI       Verified result
    Scirpophaga_Incertulas   c_6911   "seasons"
    Burkholderia_Glumae      c_36808  404 Not Found
    Xanthomonas_Oryzicola    c_37992  404 Not Found
    Sclerophthora_Macrospora c_6907   404 Not Found
    Rice_Tungro_Bacilliform_Virus c_25919 404 Not Found
    Rice_Tungro_Spherical_Virus   c_25920 404 Not Found
    Nephotettix_Virescens    c_5160   "New Jersey"
    Tillering_Stage          c_7808   "Tonga"
    Reproductive_Stage       c_6562   "rhizobitoxine"

None resolve to anything related to the individual they're asserted on.
This looks like fabricated/hallucinated output from whatever process
produced that commit, not a real AGROVOC lookup. All 9 are removed here.

This does not touch the correct `skos:exactMatch`/`skos:closeMatch`
alignments already on these same individuals (added and independently
API-verified in the 2026-08-22 SKOS alignment session) - those stay.
"""
import argparse
import csv
from rdflib import Graph, Namespace, URIRef

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

FABRICATED = [
    ("Scirpophaga_Incertulas", "c_6911", "seasons"),
    ("Burkholderia_Glumae", "c_36808", "404 Not Found"),
    ("Xanthomonas_Oryzicola", "c_37992", "404 Not Found"),
    ("Sclerophthora_Macrospora", "c_6907", "404 Not Found"),
    ("Rice_Tungro_Bacilliform_Virus", "c_25919", "404 Not Found"),
    ("Rice_Tungro_Spherical_Virus", "c_25920", "404 Not Found"),
    ("Nephotettix_Virescens", "c_5160", "New Jersey"),
    ("Tillering_Stage", "c_7808", "Tonga"),
    ("Reproductive_Stage", "c_6562", "rhizobitoxine"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--alignment-check-csv", default="reports/alignment_check.csv")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input)

    removed = 0
    rows = []
    for name, code, resolved_to in FABRICATED:
        s = RICE[name]
        o = URIRef(f"http://aims.fao.org/aos/agrovoc/{code}")
        t = (s, RICE.exactMatch, o)
        if t in g:
            g.remove(t)
            removed += 1
            rows.append([name, str(o), "rice:exactMatch (undeclared property, 2026-08-21 commit)",
                         f"REMOVED: verified via live AGROVOC REST API to resolve to "
                         f"'{resolved_to}', unrelated to {name}. Fabricated/hallucinated "
                         f"identifier, not a real match."])
        else:
            print(f"Already removed or absent: {name} rice:exactMatch {o}")

    if rows:
        with open(args.alignment_check_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Removed {removed} fabricated rice:exactMatch triples")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
