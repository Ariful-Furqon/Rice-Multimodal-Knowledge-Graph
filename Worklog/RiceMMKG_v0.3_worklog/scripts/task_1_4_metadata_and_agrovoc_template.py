#!/usr/bin/env python3
"""Task 1.4 — ontology FAIR metadata + AGROVOC alignment TODO template.

Change A (alignment): emit reports/agrovoc_todo.csv listing every domain
individual with no skos:exactMatch/closeMatch, for human lookup. Uses the
corrected 30-individual list from reports/phase0_baseline_adopted.md (the
worklog's own list of 10 was stale against the actual ontology state).

Change B (metadata): add dcterms:title, dcterms:creator (ORCID placeholder),
dcterms:license, dcterms:issued, owl:versionIRI, vann:preferredNamespacePrefix
to the owl:Ontology node, and bump owl:versionInfo to 2.3.
"""
import argparse
import csv
import os
from rdflib import Graph, Namespace, URIRef, Literal, RDF, OWL, XSD
from rdflib.namespace import SKOS, DCTERMS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
VANN = Namespace("http://purl.org/vocab/vann/")
ONTOLOGY_IRI = URIRef("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG")

# Corrected list — see reports/phase0_baseline_adopted.md
UNALIGNED_INDIVIDUALS = [
    "Armyworm", "Bacterial_Leaf_Blight", "Bacterial_Leaf_Streak",
    "Bacterial_Panicle_Blight", "Brown_Lesion", "Brown_Spot", "Chewed_Leaf",
    "Critical_Severity", "Deadheart", "Dry_Leaf_Tip", "Empty_Grain",
    "Excessive_Nitrogen", "Field_Inspection", "Harvest_Stage", "High_Severity",
    "Hispa", "Hopper_Burn", "Immediate_Intervention", "Leaf_Rolling",
    "Low_Severity", "Maturity_Stage", "Medium_Severity", "No_Action_Needed",
    "Normal_Health", "Preventive_Action", "Resistant_Variety", "Rice_Bug",
    "Sheath_Blight", "Stem_Rot_Symptom", "Yellow_Leaf",
]


def apply_metadata(g):
    g.remove((ONTOLOGY_IRI, OWL.versionInfo, None))
    g.add((ONTOLOGY_IRI, OWL.versionInfo, Literal("2.3")))

    g.remove((ONTOLOGY_IRI, DCTERMS.title, None))
    g.add((ONTOLOGY_IRI, DCTERMS.title, Literal("Rice MMKG — Rice Multimodal Knowledge Graph")))

    g.remove((ONTOLOGY_IRI, DCTERMS.creator, None))
    g.add((ONTOLOGY_IRI, DCTERMS.creator, Literal("TODO (ORCID: https://orcid.org/TODO)")))

    g.remove((ONTOLOGY_IRI, DCTERMS.license, None))
    g.add((ONTOLOGY_IRI, DCTERMS.license, Literal("TODO")))

    g.remove((ONTOLOGY_IRI, DCTERMS.issued, None))
    g.add((ONTOLOGY_IRI, DCTERMS.issued, Literal("TODO")))

    g.remove((ONTOLOGY_IRI, OWL.versionIRI, None))
    g.add((ONTOLOGY_IRI, OWL.versionIRI, URIRef(
        "http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG/2.3")))

    g.remove((ONTOLOGY_IRI, VANN.preferredNamespacePrefix, None))
    g.add((ONTOLOGY_IRI, VANN.preferredNamespacePrefix, Literal("riceMMKG")))


def emit_agrovoc_csv(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["individual", "agrovoc_iri", "match_type"])
        for name in UNALIGNED_INDIVIDUALS:
            w.writerow([name, "", ""])
    print(f"Wrote {path} ({len(UNALIGNED_INDIVIDUALS)} rows)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--agrovoc-csv", default="reports/agrovoc_todo.csv")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    apply_metadata(g)
    g.bind("rice", RICE)
    g.bind("dcterms", DCTERMS)
    g.bind("vann", VANN)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Wrote {args.output}")

    emit_agrovoc_csv(args.agrovoc_csv)


if __name__ == "__main__":
    main()
