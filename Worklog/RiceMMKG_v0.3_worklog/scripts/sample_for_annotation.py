#!/usr/bin/env python3
"""Task 2.3 (part 1) — draw a stratified, seeded sample of 25 LeafImage
individuals per Paddy Doctor class (10 classes -> 250 rows) for human
symptom annotation.
"""
import argparse
import csv
import os
import random
from collections import defaultdict
from rdflib import Graph, Namespace, RDF

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
SCHEMA = Namespace("http://schema.org/")
SEED = 2023
PER_CLASS = 25


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", default="reports/annotation_sample.csv")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")

    by_label = defaultdict(list)
    for img in g.subjects(RDF.type, RICE.LeafImage):
        label = g.value(img, RICE.sourceDatasetLabel)
        if label is not None:
            by_label[str(label)].append(img)

    rng = random.Random(SEED)
    rows = []
    for label in sorted(by_label):
        pool = sorted(by_label[label], key=str)
        rng.shuffle(pool)
        chosen = pool[:PER_CLASS]
        if len(chosen) < PER_CLASS:
            raise SystemExit(
                f"Class '{label}' has only {len(chosen)} images, need {PER_CLASS}"
            )
        for img in chosen:
            path = g.value(img, SCHEMA.contentUrl)
            rows.append({
                "individual_iri": str(img),
                "image_path": str(path) if path is not None else "",
                "ground_truth_label": label,
                "symptom_iris": "",
            })

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "individual_iri", "image_path", "ground_truth_label", "symptom_iris",
        ])
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {args.out}: {len(rows)} rows across {len(by_label)} classes "
          f"({PER_CLASS} each), seed={SEED}")


if __name__ == "__main__":
    main()
