#!/usr/bin/env python3
"""Task 1.1 — rename classifiedAs/classifies to annotatedAs/annotationOf,
add an rdfs:comment explaining the range union, and add PaddyDoctor dataset
provenance (PROV-O + Dublin Core terms).

Idempotent: safe to re-run against its own output.
"""
import argparse
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
PROV = Namespace("http://www.w3.org/ns/prov#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
ONTOLOGY_IRI = URIRef("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG")

RANGE_COMMENT = Literal(
    "The range is a union of Disease, HealthStatus, Pest, and Symptom because "
    "this property carries ground-truth annotations from the Paddy Doctor "
    "dataset, whose label set mixes diseases, pests, symptoms, and a healthy "
    "class in a single flat vocabulary. It records what the dataset asserts, "
    "not a classification conclusion drawn by this ontology."
)


def rename_uri(g, old, new):
    """Replace every occurrence of `old` (as subject, predicate, or object)
    with `new`, in place."""
    for s, p, o in list(g.triples((old, None, None))):
        g.remove((s, p, o))
        g.add((new, p, o))
    for s, p, o in list(g.triples((None, old, None))):
        g.remove((s, p, o))
        g.add((s, new, o))
    for s, p, o in list(g.triples((None, None, old))):
        g.remove((s, p, o))
        g.add((s, p, new))


def apply(g):
    before = len(g)

    classified_as = RICE.classifiedAs
    classifies = RICE.classifies
    annotated_as = RICE.annotatedAs
    annotation_of = RICE.annotationOf

    n_instance_before = sum(1 for _ in g.triples((None, classified_as, None)))

    already_done = n_instance_before == 0 and any(
        g.triples((None, annotated_as, None))
    )
    if already_done:
        print("classifiedAs already renamed; skipping rename step.")
    else:
        rename_uri(g, classified_as, annotated_as)
        rename_uri(g, classifies, annotation_of)

        # Fix up labels that were carried over verbatim from the old names.
        g.remove((annotated_as, RDFS.label, Literal("classified as")))
        g.add((annotated_as, RDFS.label, Literal("annotated as")))
        g.remove((annotation_of, RDFS.label, Literal("classifies")))
        g.add((annotation_of, RDFS.label, Literal("annotation of")))

    # Range-union comment (idempotent: remove any prior copy first).
    g.remove((annotated_as, RDFS.comment, None))
    # Preserve the original comment about raw source-dataset labels by
    # appending the new explanation as a second rdfs:comment triple? The
    # task asks specifically for a comment on the range union — keep the
    # original provenance comment too since it is still accurate.
    original_comment = Literal(
        "Records the raw source-dataset label assigned to an Observation "
        "(e.g. a Paddy Doctor image), independent of the detects/detectedBy "
        "relation used for confirmed field or literature-backed detections."
    )
    g.add((annotated_as, RDFS.comment, original_comment))
    g.add((annotated_as, RDFS.comment, RANGE_COMMENT))

    # --- PROV-O / Dublin Core imports ---
    g.add((ONTOLOGY_IRI, OWL.imports, URIRef("http://www.w3.org/ns/prov-o#")))
    g.add((ONTOLOGY_IRI, OWL.imports, URIRef("http://purl.org/dc/terms/")))

    # --- Dataset provenance entity ---
    dataset = RICE.PaddyDoctorDataset
    if (dataset, RDF.type, PROV.Entity) not in g:
        g.add((dataset, RDF.type, PROV.Entity))
        g.add((dataset, RDF.type, OWL.NamedIndividual))
        g.add((dataset, DCTERMS.title, Literal("TODO")))
        g.add((dataset, DCTERMS.source, Literal("TODO")))
        g.add((dataset, DCTERMS.license, Literal("TODO")))
        g.add((dataset, RDFS.label, Literal("Paddy Doctor Dataset")))

    # --- wasDerivedFrom on every LeafImage individual ---
    added_derived = 0
    for img in g.subjects(RDF.type, RICE.LeafImage):
        triple = (img, PROV.wasDerivedFrom, dataset)
        if triple not in g:
            g.add(triple)
            added_derived += 1

    after = len(g)
    print(f"classifiedAs instance triples renamed: {n_instance_before}")
    print(f"prov:wasDerivedFrom triples added: {added_derived}")
    print(f"Triple count before: {before}, after: {after}, delta: {after - before}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    apply(g)
    g.bind("rice", RICE)
    g.bind("prov", PROV)
    g.bind("dcterms", DCTERMS)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
