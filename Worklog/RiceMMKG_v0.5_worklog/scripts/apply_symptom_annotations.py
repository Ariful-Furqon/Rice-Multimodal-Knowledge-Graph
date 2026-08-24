#!/usr/bin/env python3
"""Task B.3 step 3 — read a human-completed annotation_sample.csv
(symptom_iris filled in) and assert rice:captures triples, each with an
owl:Axiom provenance record carrying rice:evidenceType
"expert-annotated" (distinct from the literature-curated domain
assertions elsewhere in the ontology).

Any symptom_iris entry that isn't a code from symptom_vocabulary.md is
rejected — either it's a typo, or it's a genuine "OTHER: ..." escape
that needs a human vocabulary decision before it can become an
assertion, not a script's job to invent.
"""
import argparse
import csv

from rdflib import Graph, Namespace, RDF, OWL, URIRef, Literal, BNode

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


def load_vocabulary(g):
    return {s.split("#")[-1] for s in g.subjects(RDF.type, RICE.Symptom)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("csv_path")
    ap.add_argument("--annotator", default="unspecified")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input)

    vocabulary = load_vocabulary(g)
    asserted = 0
    skipped_empty = 0
    other_flagged = []

    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            raw = row["symptom_iris"].strip()
            if not raw:
                skipped_empty += 1
                continue

            img = URIRef(row["individual_iri"])
            for code in (c.strip() for c in raw.split(";") if c.strip()):
                if code.upper().startswith("OTHER:"):
                    other_flagged.append((row["individual_iri"], code))
                    continue
                if code not in vocabulary:
                    raise ValueError(
                        f"{row['individual_iri']}: symptom code '{code}' is not in the "
                        f"28-term vocabulary and is not an OTHER: escape — check for a typo."
                    )
                symptom = RICE[code]
                triple = (img, RICE.captures, symptom)
                if triple in g:
                    continue  # idempotent re-run
                g.add(triple)
                ax = BNode()
                g.add((ax, RDF.type, OWL.Axiom))
                g.add((ax, OWL.annotatedSource, img))
                g.add((ax, OWL.annotatedProperty, RICE.captures))
                g.add((ax, OWL.annotatedTarget, symptom))
                g.add((ax, DCTERMS.source, Literal(f"expert annotation: {args.annotator}")))
                g.add((ax, RICE.evidenceType, Literal("expert-annotated")))
                asserted += 1

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Asserted {asserted} captures triples ({skipped_empty} rows still blank, "
          f"{len(other_flagged)} OTHER: escapes flagged for vocabulary review).")
    for iri, code in other_flagged:
        print(f"  OTHER: {iri} -> {code}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
