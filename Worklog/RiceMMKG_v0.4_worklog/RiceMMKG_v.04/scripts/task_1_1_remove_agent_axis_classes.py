#!/usr/bin/env python3
"""Task 1.1 — remove the agent-axis Observation subclasses and the orphan
Entity class.

Note: rice:Entity does not exist in the ontology. The only "Entity" present
is prov:Entity (declared as owl:Class in v0.3 so PaddyDoctorDataset's
rdf:type had a first-class member of the hierarchy). This is what the
design doc's S2.8 "Removed: Entity" refers to. Unlike the worklog's claim,
it is not instance-free (PaddyDoctorDataset is typed prov:Entity) — so
this script removes only the class *declaration* (rdf:type owl:Class +
label), not the individual's type triple. Task 1.3 removes that legacy
type triple when it promotes PaddyDoctorDataset to rice:Dataset.
"""
import argparse
from rdflib import Graph, Namespace, RDF, RDFS, OWL

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
PROV = Namespace("http://www.w3.org/ns/prov#")

CLASSES_TO_REMOVE = ["FieldObservation", "FarmerReport", "DiseaseReport"]


def remove_collection(g, head):
    """Remove every rdf:first/rdf:rest triple in an RDF list starting at head."""
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
    before_triples = len(g)

    removed_triples = 0
    for local in CLASSES_TO_REMOVE:
        cls = RICE[local]
        triples = list(g.triples((cls, None, None)))
        for t in triples:
            g.remove(t)
            removed_triples += 1

    # The v0.3 modality AllDisjointClasses axiom names exactly the three
    # agent-axis classes plus LeafImage/SensorReading. It is superseded by
    # Task 1.6's rebuilt axiom (after the 1.2 renames and 1.3 new classes),
    # so remove it wholesale here rather than surgically edit its list.
    for ax in list(g.subjects(RDF.type, OWL.AllDisjointClasses)):
        members_head = g.value(ax, OWL.members)
        item_list = list(g.items(members_head)) if members_head is not None else []
        if any(RICE[c] in item_list for c in CLASSES_TO_REMOVE):
            removed_triples += remove_collection(g, members_head)
            for t in list(g.triples((ax, None, None))):
                g.remove(t)
                removed_triples += 1

    # prov:Entity: remove only the class declaration, not instance typing
    ent = PROV.Entity
    ent_triples = list(g.triples((ent, RDF.type, OWL.Class))) + list(g.triples((ent, RDFS.label, None)))
    for t in ent_triples:
        g.remove(t)
        removed_triples += 1

    after_triples = len(g)
    g.bind("rice", RICE)
    g.bind("prov", PROV)
    g.serialize(destination=args.output, format="pretty-xml")

    print(f"Triples removed: {removed_triples}")
    print(f"Triple count before: {before_triples}, after: {after_triples}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
