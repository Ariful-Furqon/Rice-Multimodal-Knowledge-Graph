#!/usr/bin/env python3
"""Task A.1 — correct rice:Xanthomonas_Oryzicola's eppoCode from the
wrong XANTOX to the EPPO-datasheet/EU-2019-2072-Annex-II-confirmed
XANTTO. Idempotent: safe to re-run once corrected.
"""
import argparse
from rdflib import Graph, Namespace, Literal

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input)

    s = RICE.Xanthomonas_Oryzicola
    old = Literal("XANTOX")
    new = Literal("XANTTO")

    if (s, RICE.eppoCode, new) in g:
        print("Already corrected (XANTTO present); nothing to do.")
    else:
        assert (s, RICE.eppoCode, old) in g, "expected XANTOX not found"
        g.remove((s, RICE.eppoCode, old))
        g.add((s, RICE.eppoCode, new))
        print("Corrected Xanthomonas_Oryzicola eppoCode: XANTOX -> XANTTO")

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
