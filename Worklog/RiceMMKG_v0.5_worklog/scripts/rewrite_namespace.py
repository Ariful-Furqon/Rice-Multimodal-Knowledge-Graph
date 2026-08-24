#!/usr/bin/env python3
"""Task C.2 — rewrite every subject/predicate/object in the local
Rice MMKG namespace to a new base IRI (e.g. after w3id.org registration
is confirmed).

DO NOT RUN AGAINST THE REAL ONTOLOGY UNTIL THE w3id.org REGISTRATION IS
CONFIRMED (Checkpoint C1 — see reports/w3id_config/README.md). This
script is prepared and tested against a fixture only.

Rewrites literal-URI membership in the old namespace wholesale — this
naturally includes every owl:Axiom's owl:annotatedSource/
annotatedTarget, since those are just IRIs like any other triple
position, not a separate mechanism needing special-casing.
"""
import argparse
from rdflib import Graph, URIRef


def rewrite(g, old_base, new_base):
    old_len = len(old_base)
    mapping = {}
    for s in set(g.subjects()) | set(g.objects()):
        if isinstance(s, URIRef) and str(s).startswith(old_base):
            mapping[s] = URIRef(new_base + str(s)[old_len:])
    for p in set(g.predicates()):
        if isinstance(p, URIRef) and str(p).startswith(old_base):
            mapping[p] = URIRef(new_base + str(p)[old_len:])

    new_g = Graph()
    for prefix, ns in g.namespaces():
        new_g.bind(prefix, ns)

    def m(term):
        return mapping.get(term, term)

    for s, p, o in g:
        new_g.add((m(s), m(p), m(o)))

    return new_g, len(mapping)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old_base", help="e.g. http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
    ap.add_argument("new_base", help="e.g. https://w3id.org/rice-mmkg#")
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input)
    before = len(g)

    new_g, n_rewritten = rewrite(g, args.old_base, args.new_base)
    after = len(new_g)

    assert before == after, f"triple count changed: {before} -> {after}"

    new_g.serialize(destination=args.output, format="pretty-xml")
    print(f"Rewrote {n_rewritten} distinct IRIs from {args.old_base} to {args.new_base}")
    print(f"Triple count unchanged: {before}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
