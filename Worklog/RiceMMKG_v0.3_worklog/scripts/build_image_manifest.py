#!/usr/bin/env python3
"""Task 1.2 (part 1) — build the LeafImage -> image file manifest.

The Paddy Doctor dataset lives locally at Data/PaddyDoctor/<label>/<id>.jpg,
and every rice:LeafImage individual IRI follows the pattern
PaddyDoctor_<label>_<id>. This script derives the relative path for each
individual from that naming convention and *verifies the file exists on
disk* before writing it to the manifest — it does not fabricate paths for
anything it can't confirm.

If the dataset directory is absent, or any individual's file can't be
verified, this script instead emits a template CSV (individual_iri,
relative_path) with empty paths for the unresolved rows and stops, per the
worklog's fallback instruction — never guessing an unverified path.
"""
import argparse
import csv
import os
import re
import sys
from rdflib import Graph, Namespace, RDF

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
PATTERN = re.compile(r"^PaddyDoctor_(.+)_(\d+)$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="ontology RDF/XML file")
    ap.add_argument("--data-root", default="../Data/PaddyDoctor")
    ap.add_argument("--out", default="reports/image_manifest.csv")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    imgs = sorted(g.subjects(RDF.type, RICE.LeafImage), key=str)

    rows = []
    unresolved = 0
    for i in imgs:
        local = str(i).rsplit("#", 1)[1]
        m = PATTERN.match(local)
        rel_path = ""
        if m:
            label, num = m.group(1), m.group(2)
            candidate = os.path.join(args.data_root, label, f"{num}.jpg")
            if os.path.isfile(candidate):
                # store as a forward-slash relative path rooted at Data/PaddyDoctor
                rel_path = f"Data/PaddyDoctor/{label}/{num}.jpg"
        if not rel_path:
            unresolved += 1
        rows.append((str(i), rel_path))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["individual_iri", "relative_path"])
        w.writerows(rows)

    print(f"Manifest rows: {len(rows)}; unresolved: {unresolved}")
    print(f"Wrote {args.out}")

    if unresolved:
        print(
            f"{unresolved} individuals could not be resolved to a verified "
            "file on disk. Their relative_path is left empty — fill them in "
            "by hand before running task_1_2_apply_image_manifest.py.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
