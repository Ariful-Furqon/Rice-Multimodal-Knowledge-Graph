#!/usr/bin/env python3
"""Task 1.3 — add the seven new classes, three Agent individuals, and
promote PaddyDoctorDataset from prov:Entity to rice:Dataset.
"""
import argparse
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
PROV = Namespace("http://www.w3.org/ns/prov#")

NEW_CLASSES = {
    "TextualReport": "A textual account of a disease/pest finding submitted by an "
        "agent (farmer, extension officer, etc.), the third Observation modality "
        "alongside ImageObservation and SensorObservation. Replaces the v0.3 "
        "agent-axis classes FieldObservation, FarmerReport, and DiseaseReport.",
    "ObservationEvent": "Groups the Observation individuals arising from one "
        "submission (e.g. a report with an attached photograph).",
    "Location": "Where an observation was made. No individuals populated yet — "
        "administrative granularity is a pending human decision (Checkpoint C4).",
    "Agent": "Who or what made an observation: a person, role, or device.",
    "Dataset": "A source dataset behind one or more AnnotationLabel individuals.",
    "AnnotationLabel": "A label as asserted by a dataset, distinct from the domain "
        "entity it denotes. Introduced to separate the annotation layer from the "
        "domain layer: annotatedAs now targets a label, and the label denotes the "
        "domain entity, rather than annotatedAs pointing at the domain entity "
        "directly.",
    "Infestation": "The condition produced by a Pest, parallel to how a Pathogen "
        "causes a Disease. Introduced because Pest previously did double duty as "
        "both the organism and the damage it produces.",
}

AGENT_INDIVIDUALS = ["Farmer", "ExtensionOfficer", "SensorDevice"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    for local, comment in NEW_CLASSES.items():
        cls = RICE[local]
        if (cls, RDF.type, OWL.Class) not in g:
            g.add((cls, RDF.type, OWL.Class))
            g.add((cls, RDFS.label, Literal(local.replace("_", " "))))
            g.add((cls, RDFS.comment, Literal(comment)))

    for local in AGENT_INDIVIDUALS:
        ind = RICE[local]
        if (ind, RDF.type, RICE.Agent) not in g:
            g.add((ind, RDF.type, OWL.NamedIndividual))
            g.add((ind, RDF.type, RICE.Agent))
            g.add((ind, RDFS.label, Literal(local.replace("_", " "))))

    # Promote PaddyDoctorDataset: drop the legacy prov:Entity typing (the
    # class declaration for prov:Entity was removed in Task 1.1), add
    # rice:Dataset.
    dataset = RICE.PaddyDoctorDataset
    g.remove((dataset, RDF.type, PROV.Entity))
    g.add((dataset, RDF.type, RICE.Dataset))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
