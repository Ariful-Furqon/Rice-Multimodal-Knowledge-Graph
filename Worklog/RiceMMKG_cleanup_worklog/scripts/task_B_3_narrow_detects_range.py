#!/usr/bin/env python3
"""Task B.3 — narrow detects' range to Pest|Pathogen (was Disease|Pest|
Symptom), removing the evidence/conclusion conflation the annotatedAs
rename was meant to eliminate. A Disease is a condition, never directly
observed; what's observable is the organism.
"""
import argparse
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL
from rdflib.collection import Collection

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

COMMENT = Literal(
    "Range deliberately excludes Disease: a disease is a condition and is "
    "never directly observed -- no modality perceives a fungus in a field. "
    "What can be observed directly is the organism (a pest by eye, a "
    "pathogen by lab confirmation). A claim like \"this image detects "
    "blast\" is a conclusion and belongs on the annotation path "
    "(annotatedAs/denotes), not here."
)


def make_class_expr(g, locals_):
    if len(locals_) == 1:
        return RICE[locals_[0]]
    node = BNode()
    g.add((node, RDF.type, OWL.Class))
    coll = Collection(g, BNode(), [RICE[l] for l in locals_])
    g.add((node, OWL.unionOf, coll.uri))
    return node


def remove_class_expr(g, node):
    if not isinstance(node, BNode):
        return
    union = g.value(node, OWL.unionOf)
    if union is not None:
        cur = union
        while cur is not None and cur != RDF.nil:
            nxt = g.value(cur, RDF.rest)
            for t in list(g.triples((cur, None, None))):
                g.remove(t)
            cur = nxt
    for t in list(g.triples((node, None, None))):
        g.remove(t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    detects = RICE.detects
    detectedBy = RICE.detectedBy

    old_range = g.value(detects, RDFS.range)
    g.remove((detects, RDFS.range, old_range))
    remove_class_expr(g, old_range)
    g.add((detects, RDFS.range, make_class_expr(g, ["Pest", "Pathogen"])))
    g.add((detects, RDFS.comment, COMMENT))

    old_domain = g.value(detectedBy, RDFS.domain)
    g.remove((detectedBy, RDFS.domain, old_domain))
    remove_class_expr(g, old_domain)
    g.add((detectedBy, RDFS.domain, make_class_expr(g, ["Pest", "Pathogen"])))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"detects range -> Pest|Pathogen; detectedBy domain -> Pest|Pathogen")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
