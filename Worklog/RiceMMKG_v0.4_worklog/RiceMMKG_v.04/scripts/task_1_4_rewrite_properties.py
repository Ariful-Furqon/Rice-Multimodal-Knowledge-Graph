#!/usr/bin/env python3
"""Task 1.4 — rewrite property domains/ranges and add five new property pairs.
"""
import argparse
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL
from rdflib.collection import Collection

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


def remove_class_expr(g, node):
    """Remove a (possibly blank-node unionOf) class expression node entirely."""
    if node is None or not isinstance(node, BNode):
        return
    union = g.value(node, OWL.unionOf)
    if union is not None:
        # remove the rdf:List cells
        cur = union
        while cur is not None and cur != RDF.nil:
            nxt = g.value(cur, RDF.rest)
            for t in list(g.triples((cur, None, None))):
                g.remove(t)
            cur = nxt
    for t in list(g.triples((node, None, None))):
        g.remove(t)


def make_class_expr(g, locals_):
    """Return a URIRef if locals_ has one class, else build a unionOf blank node."""
    if len(locals_) == 1:
        return RICE[locals_[0]]
    node = BNode()
    g.add((node, RDF.type, OWL.Class))
    coll = Collection(g, BNode(), [RICE[l] for l in locals_])
    g.add((node, OWL.unionOf, coll.uri))
    return node


def set_domain(g, prop, locals_):
    old = g.value(prop, RDFS.domain)
    g.remove((prop, RDFS.domain, old))
    remove_class_expr(g, old)
    g.add((prop, RDFS.domain, make_class_expr(g, locals_)))


def set_range(g, prop, locals_):
    old = g.value(prop, RDFS.range)
    g.remove((prop, RDFS.range, old))
    remove_class_expr(g, old)
    g.add((prop, RDFS.range, make_class_expr(g, locals_)))


# (property, new domain classes or None, new range classes or None)
DOMAIN_RANGE_CHANGES = [
    ("annotatedAs", None, ["AnnotationLabel"]),
    ("annotationOf", ["AnnotationLabel"], None),
    ("detects", None, ["Pest", "Pathogen"]),
    ("detectedBy", ["Pest", "Pathogen"], None),
    ("indicates", None, ["Disease", "Infestation"]),
    ("indicatedBy", ["Disease", "Infestation"], None),
    ("causes", ["Pathogen", "Pest"], ["Disease", "Infestation"]),
    ("causedBy", ["Disease", "Infestation"], ["Pathogen", "Pest"]),
    ("increaseRiskOf", None, ["Disease", "Infestation"]),
    ("riskIncreasedBy", ["Disease", "Infestation"], None),
    ("vulnerableTo", None, ["Disease", "Infestation"]),
    ("threatens", ["Disease", "Infestation"], None),
    ("occursIn", ["Disease", "Infestation"], None),
    ("hasOccurrenceOf", None, ["Disease", "Infestation"]),
    ("controlledBy", ["Disease", "Infestation"], None),
    ("controls", None, ["Disease", "Infestation"]),
    ("preventedBy", ["Disease", "Infestation"], None),
    ("prevents", None, ["Disease", "Infestation"]),
    ("recommends", ["Disease", "Infestation", "SeverityLevel"], None),
    ("recommendedFor", None, ["Disease", "Infestation", "SeverityLevel"]),
]

# (forward name, inverse name-or-None, domain locals, range locals, functional)
NEW_PROPERTIES = [
    ("transmits", "transmittedBy", ["Pest"], ["Pathogen"], False),
    ("denotes", "denotedBy", ["AnnotationLabel"], ["Disease", "Infestation", "Symptom", "HealthStatus"], False),
    ("fromSource", None, ["AnnotationLabel"], ["Dataset", "Agent"], False),
    ("hasPart", "partOf", ["ObservationEvent"], ["Observation"], False),
    ("observedAt", None, ["Observation"], ["Location"], False),
]

PROPERTY_COMMENTS = {
    "transmits": "A Pest may act as a vector, transmitting a Pathogen rather than "
        "causing a Disease directly.",
    "denotes": "The domain entity an AnnotationLabel stands for. Range is a union "
        "because the Paddy Doctor label set genuinely mixes levels: disease names, "
        "a pest-damage name, a symptom name, and a health state.",
    "fromSource": "The dataset or agent an AnnotationLabel originates from.",
    "hasPart": "Groups Observation individuals arising from one submission event.",
    "observedAt": "Where an Observation was made.",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    changed = 0
    for name, dom, rng in DOMAIN_RANGE_CHANGES:
        prop = RICE[name]
        if dom is not None:
            set_domain(g, prop, dom)
            changed += 1
        if rng is not None:
            set_range(g, prop, rng)
            changed += 1

    added_props = 0
    for fwd_name, inv_name, dom, rng, functional in NEW_PROPERTIES:
        fwd = RICE[fwd_name]
        g.add((fwd, RDF.type, OWL.ObjectProperty))
        g.add((fwd, RDFS.label, Literal(fwd_name)))
        if fwd_name in PROPERTY_COMMENTS:
            g.add((fwd, RDFS.comment, Literal(PROPERTY_COMMENTS[fwd_name])))
        g.add((fwd, RDFS.domain, make_class_expr(g, dom)))
        g.add((fwd, RDFS.range, make_class_expr(g, rng)))
        added_props += 1
        if inv_name:
            inv = RICE[inv_name]
            g.add((inv, RDF.type, OWL.ObjectProperty))
            g.add((inv, RDFS.label, Literal(inv_name)))
            g.add((inv, OWL.inverseOf, fwd))
            g.add((inv, RDFS.domain, make_class_expr(g, rng)))
            g.add((inv, RDFS.range, make_class_expr(g, dom)))
            added_props += 1

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Domain/range triples changed: {changed}")
    print(f"New properties added: {added_props}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
