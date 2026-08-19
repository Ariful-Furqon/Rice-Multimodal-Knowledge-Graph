#!/usr/bin/env python3
"""Task 1.1 — delete the four empty Observation subclasses and the orphan
Entity class declaration.

Note: rice:Entity does not exist in the ontology. The only "Entity" is
prov:Entity, used for PaddyDoctorDataset's rdf:type (it has 1 instance, not
zero as the worklog assumes). Only the class *declaration* is removed here
(rdf:type owl:Class + its label) — PaddyDoctorDataset's rdf:type prov:Entity
triple is left untouched, since Task 1.3's promotion to rice:Dataset is
explicitly deferred in this minimal plan (Phase 2).

Keeps rice:LeafImage untouched (10,407 individuals). Removes the v0.3
modality AllDisjointClasses axiom wholesale, since after removing 4 of its
5 members only LeafImage would remain — a 1-member disjointness axiom
asserts nothing, so it's deleted rather than left vacuous.
"""
import argparse
from rdflib import Graph, Namespace, RDF, RDFS, OWL

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
PROV = Namespace("http://www.w3.org/ns/prov#")

CLASSES_TO_REMOVE = ["SensorReading", "FieldObservation", "FarmerReport", "DiseaseReport"]


def remove_collection(g, head):
    n = 0
    node = head
    while node is not None and node != RDF.nil:
        rest = g.value(node, RDF.rest)
        for t in list(g.triples((node, None, None))):
            g.remove(t)
            n += 1
        node = rest
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    removed = 0
    for local in CLASSES_TO_REMOVE:
        cls = RICE[local]
        for t in list(g.triples((cls, None, None))):
            g.remove(t)
            removed += 1

    # the modality AllDisjointClasses axiom names all 4 removed classes plus LeafImage
    for ax in list(g.subjects(RDF.type, OWL.AllDisjointClasses)):
        members_head = g.value(ax, OWL.members)
        items = list(g.items(members_head)) if members_head is not None else []
        if any(RICE[c] in items for c in CLASSES_TO_REMOVE):
            removed += remove_collection(g, members_head)
            for t in list(g.triples((ax, None, None))):
                g.remove(t)
                removed += 1

    # prov:Entity: class declaration only, not PaddyDoctorDataset's instance typing
    ent = PROV.Entity
    for t in list(g.triples((ent, RDF.type, OWL.Class))) + list(g.triples((ent, RDFS.label, None))):
        g.remove(t)
        removed += 1

    after = len(g)
    g.bind("rice", RICE)
    g.bind("prov", PROV)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Triples removed: {removed}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
