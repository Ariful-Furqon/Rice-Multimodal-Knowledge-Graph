#!/usr/bin/env python3
"""Task B.3 step 1 — draw a stratified, seeded, reproducible sample of 25
ImageObservation individuals per annotation target (10 targets x 25 = 250
rows) for human symptom annotation.

Emits reports/annotation_sample.csv with columns:
individual_iri, content_url, annotated_as, symptom_iris (empty,
semicolon-separated for the annotator to fill in).
"""
import argparse
import csv
import random

import rdflib
from rdflib import Namespace, RDF

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
SEED = 20260822  # fixed for reproducibility
PER_TARGET = 25


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output_csv")
    args = ap.parse_args()

    g = rdflib.Graph()
    g.parse(args.input)

    by_target = {}
    for img, target in g.subject_objects(RICE.annotatedAs):
        by_target.setdefault(target, []).append(img)

    rows = []
    for target in sorted(by_target, key=str):
        images = sorted(by_target[target], key=str)  # deterministic order before sampling
        rng = random.Random(f"{SEED}:{target}")
        chosen = rng.sample(images, min(PER_TARGET, len(images)))
        for img in sorted(chosen, key=str):
            content_url = g.value(img, rdflib.URIRef("http://schema.org/contentUrl"))
            rows.append({
                "individual_iri": str(img),
                "content_url": str(content_url) if content_url else "",
                "annotated_as": target.split("#")[-1],
                "symptom_iris": "",
            })

    with open(args.output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["individual_iri", "content_url", "annotated_as", "symptom_iris"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} rows across {len(by_target)} targets ({PER_TARGET} each) -> {args.output_csv}")


if __name__ == "__main__":
    main()
