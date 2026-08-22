#!/usr/bin/env python3
"""Revert 10 of the 34 SKOS alignments added 2026-08-22, which conflict with
decisions already recorded in the project's established alignment registers
(AGROVOC_alignment.md, NCBI_Taxonomy_alignment.md):

- Armyworm: register explicitly rejected this exact AGROVOC candidate
  (fall armyworms = a maize pest, false-positive risk).
- Bacterial_Leaf_Blight, Bacterial_Leaf_Streak, Brown_Spot, Sheath_Blight:
  disease-vs-pathogen substitution the register explicitly warns against
  ("Do not substitute the pathogen Xanthomonas oryzae; disease and
  pathogen are distinct entities") - Brown_Spot's c_34512 is also already
  used (correctly) for the Bipolaris_Oryzae Pathogen individual.
- Excessive_Nitrogen: register explicitly recorded "No candidate found"
  for this exact entity after a dedicated search round.
- Maturity_Stage, Resistant_Variety, Rice_Bug: register explicitly marks
  these "Needs domain review" / "Not applied", each for a specific
  documented reason (unconfirmed altLabel synonymy; trait-vs-practice
  category mismatch; unresolved species/spelling ambiguity) that a
  same-day agent lookup did not actually resolve.
- Panicle_Blast: reuses the AGROVOC concept already assigned to
  Rice_Blast_Disease (a Disease), conflating a Symptom with the disease
  concept itself.
"""
import argparse
from rdflib import Graph, Namespace, URIRef

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
AGROVOC = "http://aims.fao.org/aos/agrovoc/"

REVERTS = [
    ("Armyworm", "closeMatch", AGROVOC + "c_e6b223d7"),
    ("Bacterial_Leaf_Blight", "exactMatch", AGROVOC + "c_24383"),
    ("Bacterial_Leaf_Streak", "exactMatch", AGROVOC + "c_330601"),
    ("Brown_Spot", "closeMatch", AGROVOC + "c_34512"),
    ("Sheath_Blight", "closeMatch", AGROVOC + "c_33858"),
    ("Excessive_Nitrogen", "closeMatch", AGROVOC + "c_5193"),
    ("Maturity_Stage", "closeMatch", AGROVOC + "c_330756"),
    ("Resistant_Variety", "closeMatch", AGROVOC + "c_2328"),
    ("Rice_Bug", "exactMatch", AGROVOC + "c_30653"),
    ("Panicle_Blast", "closeMatch", AGROVOC + "c_152ac092"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    removed = 0
    for name, match_type, iri in REVERTS:
        s = RICE[name]
        p = SKOS[match_type]
        o = URIRef(iri)
        assert (s, p, o) in g, f"triple not found: {name} {match_type} {iri}"
        g.remove((s, p, o))
        removed += 1

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Reverted: {removed}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
