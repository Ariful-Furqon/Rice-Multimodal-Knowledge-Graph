#!/usr/bin/env python3
"""Verification harness for Rice MMKG.

Usage: python verify.py <path-to-rdf> [--json-out PATH] [--txt-out PATH]

Reports:
 - total triples; counts of named classes, object properties, datatype properties, individuals
 - count of owl:Restriction axioms and rdfs:subClassOf axioms with a blank-node object
 - per-class individual counts
 - per-property assertion counts, and declared-but-never-asserted properties
 - count of skos:exactMatch / skos:closeMatch, and domain individuals with no alignment
 - individuals typed only as owl:NamedIndividual (prototype smell)
 - OWL profile / DL expressivity if obtainable, else skipped
"""
import argparse
import json
import sys
from collections import defaultdict

from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
from rdflib.namespace import SKOS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

# "Domain individuals" = individuals in the core domain classes (not LeafImage,
# not Observation-subclass instances used purely as data records).
DOMAIN_CLASSES = {
    "Disease", "Pest", "Pathogen", "Plant", "Symptom", "EnvironmentalFactor",
    "GrowthStage", "HealthStatus", "SeverityLevel", "Treatment", "ManagementAction",
}


def local_name(uri):
    s = str(uri)
    if "#" in s:
        return s.rsplit("#", 1)[1]
    return s.rsplit("/", 1)[1]


def load(path):
    g = Graph()
    g.parse(path, format="xml")
    return g


def named_classes(g):
    return sorted({c for c in g.subjects(RDF.type, OWL.Class) if isinstance(c, URIRef)})


def object_properties(g):
    return sorted({p for p in g.subjects(RDF.type, OWL.ObjectProperty) if isinstance(p, URIRef)})


def datatype_properties(g):
    return sorted({p for p in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(p, URIRef)})


def annotation_properties(g):
    return sorted({p for p in g.subjects(RDF.type, OWL.AnnotationProperty) if isinstance(p, URIRef)})


def all_individuals(g, classes):
    class_set = set(classes)
    inds = set()
    for c in class_set:
        for i in g.subjects(RDF.type, c):
            if isinstance(i, URIRef):
                inds.add(i)
    return inds


def named_individual_typed(g):
    return {i for i in g.subjects(RDF.type, OWL.NamedIndividual) if isinstance(i, URIRef)}


def per_class_counts(g, classes):
    counts = {}
    for c in classes:
        n = len({i for i in g.subjects(RDF.type, c) if isinstance(i, URIRef)})
        counts[local_name(c)] = n
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def per_property_counts(g, props):
    counts = {}
    for p in props:
        n = sum(1 for _ in g.triples((None, p, None)))
        counts[local_name(p)] = n
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def inverse_pairs(g, obj_props):
    pairs = []
    seen = set()
    for p in obj_props:
        for inv in g.objects(p, OWL.inverseOf):
            key = frozenset({p, inv})
            if key not in seen:
                seen.add(key)
                pairs.append((local_name(p), local_name(inv)))
    return pairs


def restriction_axioms(g):
    return len({r for r in g.subjects(RDF.type, OWL.Restriction)})


def subclassof_blanknode(g):
    n = 0
    for s, p, o in g.triples((None, RDFS.subClassOf, None)):
        if not isinstance(o, URIRef):
            n += 1
    return n


def alignment_counts(g):
    exact = sum(1 for _ in g.triples((None, SKOS.exactMatch, None)))
    close = sum(1 for _ in g.triples((None, SKOS.closeMatch, None)))
    return exact, close


def domain_individuals_no_alignment(g, domain_class_names):
    classes = [c for c in named_classes(g) if local_name(c) in domain_class_names]
    inds = all_individuals(g, classes)
    aligned = set()
    for s, _, _ in g.triples((None, SKOS.exactMatch, None)):
        aligned.add(s)
    for s, _, _ in g.triples((None, SKOS.closeMatch, None)):
        aligned.add(s)
    unaligned = sorted(local_name(i) for i in inds if i not in aligned)
    return unaligned


def try_expressivity(g):
    try:
        import owlready2  # noqa: F401
    except ImportError:
        return None
    return "owlready2 available (expressivity check not computed here)"


def build_report(path):
    g = Graph()
    g.parse(path, format="xml")

    total_triples = len(g)
    classes = named_classes(g)
    obj_props = object_properties(g)
    dtype_props = datatype_properties(g)
    ann_props = annotation_properties(g)

    all_typed_props = set(obj_props) | set(dtype_props)
    domain_inds = all_individuals(g, classes)

    prototype_only = set()
    for i in named_individual_typed(g):
        types = set(g.objects(i, RDF.type))
        if types == {OWL.NamedIndividual}:
            prototype_only.add(i)

    prop_counts = per_property_counts(g, sorted(all_typed_props, key=str))
    never_asserted = sorted(name for name, cnt in prop_counts.items() if cnt == 0)

    exact, close = alignment_counts(g)
    unaligned_domain = domain_individuals_no_alignment(g, DOMAIN_CLASSES)

    report = {
        "source": str(path),
        "total_triples": total_triples,
        "named_classes": len(classes),
        "object_properties": len(obj_props),
        "datatype_properties": len(dtype_props),
        "annotation_properties": len(ann_props),
        "inverse_pairs": inverse_pairs(g, obj_props),
        "inverse_pair_count": len(inverse_pairs(g, obj_props)),
        "individuals_total": len(domain_inds) + 0,  # filled below properly
        "owl_restriction_axioms": restriction_axioms(g),
        "subclassof_blanknode_axioms": subclassof_blanknode(g),
        "per_class_individual_counts": per_class_counts(g, classes),
        "per_property_assertion_counts": prop_counts,
        "declared_but_never_asserted_properties": never_asserted,
        "skos_exactMatch_count": exact,
        "skos_closeMatch_count": close,
        "domain_individuals_no_alignment": unaligned_domain,
        "domain_individuals_no_alignment_count": len(unaligned_domain),
        "prototype_individuals_named_individual_only": sorted(local_name(i) for i in prototype_only),
        "prototype_individuals_count": len(prototype_only),
        "owl_profile_expressivity": try_expressivity(g),
    }

    # Total individuals: union of all subjects typed as owl:NamedIndividual
    # or as any named class (covers individuals asserted with only a domain
    # class type and no explicit owl:NamedIndividual triple).
    all_inds = set(named_individual_typed(g)) | domain_inds
    report["individuals_total"] = len(all_inds)

    return report


def format_text(report):
    lines = []
    lines.append(f"Rice MMKG verification report — {report['source']}")
    lines.append("=" * 70)
    lines.append(f"Total triples:            {report['total_triples']}")
    lines.append(f"Named classes:            {report['named_classes']}")
    lines.append(f"Object properties:        {report['object_properties']} ({report['inverse_pair_count']} owl:inverseOf pairs)")
    lines.append(f"Datatype properties:      {report['datatype_properties']}")
    lines.append(f"Annotation properties:    {report['annotation_properties']}")
    lines.append(f"Individuals (total):      {report['individuals_total']}")
    lines.append(f"owl:Restriction axioms:   {report['owl_restriction_axioms']}")
    lines.append(f"subClassOf blank-node ax: {report['subclassof_blanknode_axioms']}")
    lines.append(f"skos:exactMatch:          {report['skos_exactMatch_count']}")
    lines.append(f"skos:closeMatch:          {report['skos_closeMatch_count']}")
    lines.append(f"Domain individuals w/o alignment ({report['domain_individuals_no_alignment_count']}):")
    for n in report["domain_individuals_no_alignment"]:
        lines.append(f"  - {n}")
    lines.append(f"Prototype individuals (owl:NamedIndividual only) ({report['prototype_individuals_count']}):")
    for n in report["prototype_individuals_named_individual_only"]:
        lines.append(f"  - {n}")
    lines.append(f"OWL profile/expressivity: {report['owl_profile_expressivity']}")
    lines.append("")
    lines.append("Per-class individual counts:")
    for name, cnt in report["per_class_individual_counts"].items():
        lines.append(f"  {name:30s} {cnt}")
    lines.append("")
    lines.append("Per-property assertion counts:")
    for name, cnt in report["per_property_assertion_counts"].items():
        lines.append(f"  {name:30s} {cnt}")
    lines.append("")
    lines.append("Declared but never-asserted properties:")
    for name in report["declared_but_never_asserted_properties"]:
        lines.append(f"  - {name}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rdf_path")
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--txt-out", default=None)
    args = ap.parse_args()

    report = build_report(args.rdf_path)
    text = format_text(report)
    print(text)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    if args.txt_out:
        with open(args.txt_out, "w", encoding="utf-8") as f:
            f.write(text)


if __name__ == "__main__":
    main()
