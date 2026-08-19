#!/usr/bin/env python3
"""Task A.4 — rewrite schema:contentUrl by prefixing a base URL onto the
existing relative path (Checkpoint C2: which base URL is not yet decided,
see reports/contenturl_base.md). Also supports moving the value to a
different local property instead (Option C), via --local-property.
"""
import argparse
from rdflib import Graph, Namespace, URIRef, Literal, RDF

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
SCHEMA = Namespace("http://schema.org/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--base-url", help="e.g. https://zenodo.org/record/<id>/files/")
    ap.add_argument("--local-property", help="e.g. rice:imagePath -- Option C, keep relative, "
                     "rename off schema:contentUrl instead of rewriting it")
    args = ap.parse_args()

    if not args.base_url and not args.local_property:
        raise SystemExit("Provide either --base-url (rewrite) or --local-property (rename)")
    if args.base_url and args.local_property:
        raise SystemExit("Choose one: --base-url or --local-property, not both")

    g = Graph()
    g.parse(args.input, format="xml")

    images = set(g.subjects(RDF.type, RICE.LeafImage))
    changed = 0
    for img in images:
        rel_path = g.value(img, SCHEMA.contentUrl)
        if rel_path is None:
            continue
        if args.base_url:
            new_url = args.base_url.rstrip("/") + "/" + str(rel_path).lstrip("/")
            g.remove((img, SCHEMA.contentUrl, rel_path))
            g.add((img, SCHEMA.contentUrl, URIRef(new_url)))
        else:
            local_prop = RICE[args.local_property.split(":")[-1]]
            g.remove((img, SCHEMA.contentUrl, rel_path))
            g.add((img, local_prop, rel_path))
        changed += 1

    g.bind("rice", RICE)
    g.bind("schema", SCHEMA)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"contentUrl rewritten/moved for {changed} images.")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
