#!/usr/bin/env python3
"""Task 2.4 — add the two defined classes.

rice:SymptomaticObservation = Observation and (captures some Symptom)
rice:StemBorerCandidate     = Observation and (captures some
                               (Symptom and (indicates value Stem_Borer_Damage)))

Note: the worklog's own text says "indicates Stem_Borer", but Task 1.4
narrowed indicates' range to Disease|Infestation (dropping Pest), and per
the user-approved fix in task_2_2b, the existing Stem_Borer-indicatedBy-
Deadheart fact was retargeted to Stem_Borer_Damage (the Infestation this
worklog itself introduces). Stem_Borer_Damage is used here for the defined
class to stay consistent with that migration — targeting the bare Pest
Stem_Borer here would make the class unsatisfiable (indicates has no Pest
in its range) and would not match any asserted data.

Stem_Borer_Damage is a specific *individual*, not a class, so the
"indicates Stem_Borer_Damage" restriction uses owl:hasValue, not
owl:someValuesFrom. An earlier version of this script used someValuesFrom
with an individual as the filler, which is invalid OWL2 (someValuesFrom
expects a class expression) — rdflib serialized it without complaint, but
it caused Protege to display Stem_Borer_Damage as a class via punning, even
though its only declared types are NamedIndividual and Infestation. Fixed
directly in Ontology/Rice MMKG.rdf and here.

Materialised member counts require a reasoner (HermiT/ELK/Pellet), which
needs Java -- not installed in this environment. Counts are NOT computed
here; see reports/task_2_4_reasoner_blocked.md.
"""
import argparse
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


def make_restriction(g, prop, filler, kind=OWL.someValuesFrom):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, prop))
    g.add((r, kind, filler))
    return r


def make_intersection(g, members):
    from rdflib.collection import Collection
    node = BNode()
    g.add((node, RDF.type, OWL.Class))
    coll = Collection(g, BNode(), members)
    g.add((node, OWL.intersectionOf, coll.uri))
    return node


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    # SymptomaticObservation = Observation and (captures some Symptom)
    symptomatic = RICE.SymptomaticObservation
    g.add((symptomatic, RDF.type, OWL.Class))
    g.add((symptomatic, RDFS.label, Literal("Symptomatic Observation")))
    g.add((symptomatic, RDFS.comment, Literal(
        "Defined class: any Observation that captures at least one Symptom. "
        "Membership is inferred from captures assertions, not asserted "
        "directly -- replaces the SymptomaticLeafImage subclass that a "
        "someValuesFrom restriction on ImageObservation alone would have "
        "otherwise required."
    )))
    r1 = make_restriction(g, RICE.captures, RICE.Symptom)
    expr1 = make_intersection(g, [RICE.Observation, r1])
    g.add((symptomatic, OWL.equivalentClass, expr1))

    # StemBorerCandidate = Observation and (captures some (Symptom and (indicates some Stem_Borer_Damage)))
    candidate = RICE.StemBorerCandidate
    g.add((candidate, RDF.type, OWL.Class))
    g.add((candidate, RDFS.label, Literal("Stem Borer Candidate")))
    g.add((candidate, RDFS.comment, Literal(
        "Defined class: any Observation that captures a Symptom which "
        "indicates Stem_Borer_Damage. First runnable evaluation of the "
        "evidence chain (captures -> indicates) against the annotation "
        "chain (annotatedAs -> denotes), using the 1,442 Deadheart "
        "captures assertions from Task 2.3."
    )))
    r_indicates = make_restriction(g, RICE.indicates, RICE.Stem_Borer_Damage, kind=OWL.hasValue)
    symptom_and_indicates = make_intersection(g, [RICE.Symptom, r_indicates])
    r_captures = make_restriction(g, RICE.captures, symptom_and_indicates)
    expr2 = make_intersection(g, [RICE.Observation, r_captures])
    g.add((candidate, OWL.equivalentClass, expr2))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
