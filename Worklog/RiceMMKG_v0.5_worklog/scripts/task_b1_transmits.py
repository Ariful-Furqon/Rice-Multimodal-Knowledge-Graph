#!/usr/bin/env python3
"""Task B.1 — separate vector transmission from causation.

Checkpoint C3 (confirm the two tungro viruses against the cited source):
verified 2026-08-22. Nephotettix_Virescens's existing `causes
Rice_Tungro_Disease` assertion is cited to CABI (2022) Rice tungro
disease datasheet + Hibino (1996) Annu. Rev. Phytopathol. 34:249-274. An
independent web search confirms both RTBV and RTSV are transmitted by
N. virescens in a semipersistent manner, with RTBV requiring RTSV's
assistance for transmission (Hibino 1983, and consistent across CABI
datasheets for both viruses) — the cited source supports both viruses,
so both get a `transmits` assertion carrying the existing provenance.

Declares rice:transmits (domain Pest, range Pathogen) with inverse
rice:transmittedBy, following the exact declaration pattern already
used for rice:causes/causedBy.
"""
import argparse
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input)

    vector = RICE.Nephotettix_Virescens
    disease = RICE.Rice_Tungro_Disease
    rtbv = RICE.Rice_Tungro_Bacilliform_Virus
    rtsv = RICE.Rice_Tungro_Spherical_Virus

    if (RICE.transmits, RDF.type, OWL.ObjectProperty) in g:
        print("transmits already declared; task already applied.")
        g.bind("rice", RICE)
        g.serialize(destination=args.output, format="pretty-xml")
        return

    # 1. Declare rice:transmits / rice:transmittedBy.
    g.add((RICE.transmits, RDF.type, OWL.ObjectProperty))
    g.add((RICE.transmits, RDFS.subPropertyOf, OWL.topObjectProperty))
    g.add((RICE.transmits, RDFS.domain, RICE.Pest))
    g.add((RICE.transmits, RDFS.range, RICE.Pathogen))
    g.add((RICE.transmits, RDFS.label, Literal("transmits")))

    g.add((RICE.transmittedBy, RDF.type, OWL.ObjectProperty))
    g.add((RICE.transmittedBy, RDFS.subPropertyOf, OWL.topObjectProperty))
    g.add((RICE.transmittedBy, OWL.inverseOf, RICE.transmits))
    g.add((RICE.transmittedBy, RDFS.domain, RICE.Pathogen))
    g.add((RICE.transmittedBy, RDFS.range, RICE.Pest))
    g.add((RICE.transmittedBy, RDFS.label, Literal("transmitted by")))

    # 2. Replace Nephotettix_Virescens causes Rice_Tungro_Disease with
    #    transmits assertions to both viruses, carrying the existing
    #    provenance record's source/citation/evidenceType onto each.
    old_triple = (vector, RICE.causes, disease)
    assert old_triple in g, "expected causes triple not found"

    old_axiom = None
    for ax in g.subjects(RDF.type, OWL.Axiom):
        if (g.value(ax, OWL.annotatedSource) == vector
                and g.value(ax, OWL.annotatedProperty) == RICE.causes
                and g.value(ax, OWL.annotatedTarget) == disease):
            old_axiom = ax
            break
    assert old_axiom is not None, "expected provenance axiom not found"

    DCTERMS = Namespace("http://purl.org/dc/terms/")
    src = g.value(old_axiom, DCTERMS.source)
    citation = g.value(old_axiom, DCTERMS.bibliographicCitation)
    evidence_type = g.value(old_axiom, RICE.evidenceType)

    g.remove(old_triple)
    g.remove((old_axiom, None, None))

    from rdflib import BNode
    for virus in (rtbv, rtsv):
        new_triple = (vector, RICE.transmits, virus)
        g.add(new_triple)
        ax = BNode()
        g.add((ax, RDF.type, OWL.Axiom))
        g.add((ax, OWL.annotatedSource, vector))
        g.add((ax, OWL.annotatedProperty, RICE.transmits))
        g.add((ax, OWL.annotatedTarget, virus))
        g.add((ax, DCTERMS.source, src))
        g.add((ax, DCTERMS.bibliographicCitation, citation))
        g.add((ax, RICE.evidenceType, evidence_type))

    # 3. causes range: already just rice:Disease (single class, not a
    #    union) — no change needed, confirmed by verify.py's range check.
    #    Left as-is; this comment documents that the step was checked,
    #    not skipped.

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print("Declared rice:transmits/transmittedBy; replaced Nephotettix_Virescens "
          "causes Rice_Tungro_Disease with 2 transmits assertions (RTBV, RTSV), "
          "provenance carried over.")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
