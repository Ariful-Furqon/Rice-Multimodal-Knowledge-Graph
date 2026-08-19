#!/usr/bin/env python3
"""Task 2.3 (part 3) — apply a human-completed symptom annotation CSV.

Reads reports/annotation_sample.csv (individual_iri, image_path,
ground_truth_label, symptom_iris) and asserts rice:captures triples from
each LeafImage to each listed Symptom individual. Rejects any symptom IRI
not in the controlled vocabulary (reports/symptom_vocabulary.md) or the
OTHER escape value. Rows with empty symptom_iris (e.g. healthy images) are
skipped without error.
"""
import argparse
import csv
import sys
from rdflib import Graph, Namespace, URIRef, RDF

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

VOCABULARY = {
    RICE.Brown_Lesion, RICE.Chewed_Leaf, RICE.Deadheart, RICE.Dry_Leaf_Tip,
    RICE.Empty_Grain, RICE.Hopper_Burn, RICE.Leaf_Rolling, RICE.Leaf_Spot,
    RICE.Stem_Rot_Symptom, RICE.Wilting, RICE.Yellow_Leaf,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="ontology RDF/XML file")
    ap.add_argument("output")
    ap.add_argument("--csv", required=True, help="completed annotation CSV")
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    g = Graph()
    g.parse(args.input, format="xml")

    applied, skipped, other_flagged, errors = 0, 0, 0, []
    for row in rows:
        raw = row.get("symptom_iris", "").strip()
        if not raw:
            skipped += 1
            continue
        img = URIRef(row["individual_iri"])
        for token in raw.split(";"):
            token = token.strip()
            if not token:
                continue
            if token == "OTHER":
                other_flagged += 1
                continue
            sym = URIRef(token)
            if sym not in VOCABULARY:
                errors.append(f"{row['individual_iri']}: '{token}' not in controlled vocabulary")
                continue
            g.add((img, RICE.captures, sym))
            applied += 1

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Applied {applied} captures triples; {skipped} rows with no symptom; "
          f"{other_flagged} OTHER-flagged (not applied, needs vocabulary review).")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
