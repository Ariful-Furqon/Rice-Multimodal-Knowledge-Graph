#!/usr/bin/env python3
"""Task A.2 — merge rice:Scirpophaga_Incertulas into rice:Stem_Borer.

Run task_a0_remove_fabricated_exactmatch.py BEFORE this script — it
removes Scirpophaga_Incertulas's fabricated `rice:exactMatch c_6911`
triple (see that script's docstring) as part of a wider defect covering
9 individuals, not just this one.

Checkpoint C5 result (verified 2026-08-22 against the live AGROVOC REST
API): the task spec assumed agrovoc:c_6911 = "Scirpophaga incertulas".
It does not — c_6911 resolves to "seasons", an unrelated concept (see
task_a0). Per the checkpoint instruction ("if either does not [resolve
as assumed], emit to reports/alignment_check.csv and stop"), c_6911 is
NOT used. A search of the same live API found the concept AGROVOC
actually uses for this species: c_30329, prefLabel "Scirpophaga
incertulas" (verified: exact literal English label, species-level
taxonomic rank, broader concept "Scirpophaga" the genus). c_30329 is
applied as Stem_Borer's `skos:exactMatch` instead, logged to
alignment_check.csv for human sign-off — a factual correction to the
task spec, not a silent guess: both the rejection and the replacement
are independently checked against the API response, not invented.

c_7389 ("stem eating insects") was independently verified and matches
what the task assumed, so its closeMatch -> broadMatch demotion proceeds
as specified.
"""
import argparse
import csv
from rdflib import Graph, Namespace, RDF, OWL, URIRef, Literal

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

AGROVOC_C6911_ASSUMED = URIRef("http://aims.fao.org/aos/agrovoc/c_6911")  # wrong, see docstring
AGROVOC_C30329_VERIFIED = URIRef("http://aims.fao.org/aos/agrovoc/c_30329")  # correct replacement
AGROVOC_C7389 = URIRef("http://aims.fao.org/aos/agrovoc/c_7389")
NCBITAXON_72366 = URIRef("http://purl.obolibrary.org/obo/NCBITaxon_72366")


def find_axiom_for_triple(g, s, p, o):
    for ax in g.subjects(RDF.type, OWL.Axiom):
        if (g.value(ax, OWL.annotatedSource) == s
                and g.value(ax, OWL.annotatedProperty) == p
                and g.value(ax, OWL.annotatedTarget) == o):
            return ax
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--alignment-check-csv", default="reports/alignment_check.csv")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input)

    stem_borer = RICE.Stem_Borer
    scirpo = RICE.Scirpophaga_Incertulas

    if (scirpo, RDF.type, None) not in g:
        print("Scirpophaga_Incertulas already absent; merge already applied.")
        g.bind("rice", RICE)
        g.serialize(destination=args.output, format="pretty-xml")
        return

    # 1. Move exactMatch NCBITaxon_72366 onto Stem_Borer.
    assert (scirpo, SKOS.exactMatch, NCBITAXON_72366) in g
    g.remove((scirpo, SKOS.exactMatch, NCBITAXON_72366))
    g.add((stem_borer, SKOS.exactMatch, NCBITAXON_72366))

    # 2. c_6911 checkpoint: verified NOT to denote Scirpophaga incertulas
    #    (see task_a0, which already removed the fabricated triple this
    #    was asserted on). Apply the verified replacement c_30329 to
    #    Stem_Borer instead, and log the substitution for human sign-off.
    g.add((stem_borer, SKOS.exactMatch, AGROVOC_C30329_VERIFIED))

    with open(args.alignment_check_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Stem_Borer", str(AGROVOC_C6911_ASSUMED), "exactMatch (as specified in worklog Task A.2)",
            "REJECTED per checkpoint C5: c_6911 resolves to prefLabel 'seasons' via live "
            "AGROVOC REST API (agrovoc.fao.org/browse/rest/v1/data), not 'Scirpophaga "
            "incertulas' — see task_a0's wider finding. Applied c_30329 to Stem_Borer instead "
            "(verified: prefLabel 'Scirpophaga incertulas', species-level taxonomic rank, "
            "broader concept 'Scirpophaga'). Human sign-off requested on the substitution.",
        ])

    # closeMatch c_7389 -> broadMatch (verified: prefLabel "stem eating
    # insects", altLabel "stem borers" — a genuinely broader pest-group
    # concept, matches the task's assumption).
    assert (stem_borer, SKOS.closeMatch, AGROVOC_C7389) in g
    g.remove((stem_borer, SKOS.closeMatch, AGROVOC_C7389))
    g.add((stem_borer, SKOS.broadMatch, AGROVOC_C7389))

    # 3. altLabel + keep existing comment.
    g.add((stem_borer, SKOS.altLabel, Literal("Scirpophaga incertulas")))

    # 4. Redirect the one incoming vulnerableTo from Scirpophaga_Incertulas
    #    to Stem_Borer, carrying provenance, unless it duplicates an
    #    existing assertion (it does here: Rice vulnerableTo Stem_Borer
    #    already exists) — in that case drop it and delete the orphaned
    #    provenance record instead of duplicating.
    for s, p, o in list(g.triples((None, RICE.vulnerableTo, scirpo))):
        ax = find_axiom_for_triple(g, s, p, o)
        if (s, p, stem_borer) in g:
            # duplicate: drop the Scirpophaga_Incertulas triple and its
            # provenance record entirely.
            g.remove((s, p, o))
            if ax is not None:
                g.remove((ax, None, None))
        else:
            g.remove((s, p, o))
            g.add((s, p, stem_borer))
            if ax is not None:
                g.remove((ax, OWL.annotatedTarget, scirpo))
                g.add((ax, OWL.annotatedTarget, stem_borer))

    # 5 & 6. Drop "Scirpophaga_Incertulas causes Deadheart" (and its
    #    provenance) and delete the individual entirely — its own
    #    remaining triples (type, eppoCode, label, comment) go with it.
    #    Stem_Borer indicatedBy Deadheart already records the fact
    #    correctly (see Task B.1 for the broader causes/transmits fix).
    for s, p, o in list(g.triples((scirpo, None, None))):
        ax = find_axiom_for_triple(g, s, p, o)
        if ax is not None:
            g.remove((ax, None, None))
        g.remove((s, p, o))
    for s, p, o in list(g.triples((None, None, scirpo))):
        ax = find_axiom_for_triple(g, s, p, o)
        if ax is not None:
            g.remove((ax, None, None))
        g.remove((s, p, o))

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
