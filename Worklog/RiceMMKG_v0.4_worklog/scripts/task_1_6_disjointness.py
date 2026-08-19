#!/usr/bin/env python3
"""Task 1.6 — rebuild the two AllDisjointClasses axioms.

1. Modality axiom: {ImageObservation, SensorObservation, TextualReport}
   (Task 1.1 removed the old, now-invalid v0.3 modality axiom wholesale.)
2. Domain axiom: extend the existing 12-member axiom with Dataset,
   DatasetLabel, AnnotationLabel, Agent, Location, ObservationEvent,
   Infestation. (Note: the design doc's own class list is "DatasetLabel" in
   S5.2 but the class is actually named AnnotationLabel per S2.1/Task 1.3 —
   DatasetLabel does not exist in this ontology. Included as AnnotationLabel,
   which is presumably what was meant; DatasetLabel is skipped since no such
   class exists.)
"""
import argparse
from rdflib import Graph, Namespace, BNode, RDF, OWL
from rdflib.collection import Collection

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

MODALITY_CLASSES = ["ImageObservation", "SensorObservation", "TextualReport"]

DOMAIN_EXTENSION_CLASSES = [
    "Dataset", "AnnotationLabel", "Agent", "Location", "ObservationEvent", "Infestation",
]


def find_domain_axiom(g):
    """The existing 12-member AllDisjointClasses axiom (Disease, Pest, ...)."""
    for ax in g.subjects(RDF.type, OWL.AllDisjointClasses):
        head = g.value(ax, OWL.members)
        items = list(g.items(head)) if head is not None else []
        if RICE.Disease in items:
            return ax, head, items
    return None, None, None


def remove_collection(g, head):
    node = head
    while node is not None and node != RDF.nil:
        nxt = g.value(node, RDF.rest)
        for t in list(g.triples((node, None, None))):
            g.remove(t)
        node = nxt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    # 1. Modality axiom
    modality_ax = BNode()
    g.add((modality_ax, RDF.type, OWL.AllDisjointClasses))
    coll = Collection(g, BNode(), [RICE[c] for c in MODALITY_CLASSES])
    g.add((modality_ax, OWL.members, coll.uri))

    # 2. Extend domain axiom
    ax, head, items = find_domain_axiom(g)
    if ax is None:
        raise SystemExit("Could not find the existing domain AllDisjointClasses axiom")
    new_items = items + [RICE[c] for c in DOMAIN_EXTENSION_CLASSES]
    remove_collection(g, head)
    g.remove((ax, OWL.members, head))
    new_coll = Collection(g, BNode(), new_items)
    g.add((ax, OWL.members, new_coll.uri))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Modality axiom created with {len(MODALITY_CLASSES)} members")
    print(f"Domain axiom extended from {len(items)} to {len(new_items)} members")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
