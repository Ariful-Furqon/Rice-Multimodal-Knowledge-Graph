#!/usr/bin/env python3
"""Verification harness for Rice MMKG v0.3 -> v0.4-minimal."""
import argparse
import json
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal
from rdflib.namespace import SKOS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

DOMAIN_CLASSES = {
    "Disease", "Pest", "Pathogen", "Plant", "Symptom", "EnvironmentalFactor",
    "GrowthStage", "HealthStatus", "SeverityLevel", "Treatment", "ManagementAction",
}


def local_name(uri):
    s = str(uri)
    if "#" in s:
        return s.rsplit("#", 1)[1]
    return s.rsplit("/", 1)[1]


def named_classes(g):
    return sorted({c for c in g.subjects(RDF.type, OWL.Class) if isinstance(c, URIRef)})


def object_properties(g):
    return sorted({p for p in g.subjects(RDF.type, OWL.ObjectProperty) if isinstance(p, URIRef)})


def datatype_properties(g):
    return sorted({p for p in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(p, URIRef)})


def annotation_properties(g):
    return sorted({p for p in g.subjects(RDF.type, OWL.AnnotationProperty) if isinstance(p, URIRef)})


def all_individuals(g, classes):
    inds = set()
    for c in classes:
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
    pairs, seen = [], set()
    for p in obj_props:
        for inv in g.objects(p, OWL.inverseOf):
            key = frozenset({p, inv})
            if key not in seen:
                seen.add(key)
                pairs.append((local_name(p), local_name(inv)))
    return pairs


def restriction_axioms(g):
    some_vals, all_vals, has_val = 0, 0, 0
    for r in g.subjects(RDF.type, OWL.Restriction):
        if any(g.triples((r, OWL.someValuesFrom, None))):
            some_vals += 1
        if any(g.triples((r, OWL.allValuesFrom, None))):
            all_vals += 1
        if any(g.triples((r, OWL.hasValue, None))):
            has_val += 1
    return some_vals, all_vals, has_val


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
    return sorted(local_name(i) for i in inds if i not in aligned)


def todo_literals(g):
    hits = []
    for s, p, o in g:
        if isinstance(o, Literal) and "TODO" in str(o):
            hits.append((str(s), str(p), str(o)))
    return sorted(hits)


def build_report(path):
    g = Graph()
    g.parse(path, format="xml")

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
    some_vals, all_vals, has_val = restriction_axioms(g)

    all_inds = set(named_individual_typed(g)) | domain_inds

    empty_classes = [name for name, cnt in per_class_counts(g, classes).items() if cnt == 0]

    report = {
        "source": str(path),
        "total_triples": len(g),
        "named_classes": len(classes),
        "object_properties": len(obj_props),
        "datatype_properties": len(dtype_props),
        "annotation_properties": len(ann_props),
        "inverse_pairs": inverse_pairs(g, obj_props),
        "inverse_pair_count": len(inverse_pairs(g, obj_props)),
        "individuals_total": len(all_inds),
        "owl_restriction_someValuesFrom": some_vals,
        "owl_restriction_allValuesFrom": all_vals,
        "owl_restriction_hasValue": has_val,
        "per_class_individual_counts": per_class_counts(g, classes),
        "empty_classes": empty_classes,
        "empty_class_count": len(empty_classes),
        "per_property_assertion_counts": prop_counts,
        "declared_but_never_asserted_properties": never_asserted,
        "skos_exactMatch_count": exact,
        "skos_closeMatch_count": close,
        "domain_individuals_no_alignment": unaligned_domain,
        "domain_individuals_no_alignment_count": len(unaligned_domain),
        "prototype_individuals_named_individual_only": sorted(local_name(i) for i in prototype_only),
        "prototype_individuals_count": len(prototype_only),
        "todo_literals": todo_literals(g),
        "todo_literal_count": len(todo_literals(g)),
    }
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
    lines.append(f"owl:Restriction someValuesFrom: {report['owl_restriction_someValuesFrom']}")
    lines.append(f"owl:Restriction allValuesFrom:  {report['owl_restriction_allValuesFrom']}")
    lines.append(f"owl:Restriction hasValue:       {report['owl_restriction_hasValue']}")
    lines.append(f"skos:exactMatch:          {report['skos_exactMatch_count']}")
    lines.append(f"skos:closeMatch:          {report['skos_closeMatch_count']}")
    lines.append(f"Empty classes ({report['empty_class_count']}): {report['empty_classes']}")
    lines.append(f"Domain individuals w/o alignment ({report['domain_individuals_no_alignment_count']}):")
    for n in report["domain_individuals_no_alignment"]:
        lines.append(f"  - {n}")
    lines.append(f"Prototype individuals (owl:NamedIndividual only) ({report['prototype_individuals_count']}):")
    for n in report["prototype_individuals_named_individual_only"]:
        lines.append(f"  - {n}")
    lines.append(f"TODO literals ({report['todo_literal_count']}):")
    for s, p, o in report["todo_literals"]:
        lines.append(f"  - {s} | {p} | {o}")
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
