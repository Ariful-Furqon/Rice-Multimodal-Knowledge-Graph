#!/usr/bin/env python3
"""Rice MMKG verification harness (Task 0.1).

Reproduces the v0.4 baseline figures and adds three new checks:
provenance coverage, duplicate identifier detection, and object-property
range conformance.

Usage: python verify.py <path-to-rdf> [--report reports/verify_<label>.md]
"""
import argparse
import sys
from collections import defaultdict

import rdflib
from rdflib import RDF, RDFS, OWL, Namespace
from rdflib.collection import Collection

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCAT = Namespace("http://www.w3.org/ns/dcat#")

DOMAIN_PROPS = [
    "vulnerableTo", "occursIn", "causes", "indicatedBy", "increaseRiskOf",
    "controlledBy", "recommends", "preventedBy", "requires",
    "transmits",  # added by Task B.1 (v0.5)
]

SKOS_MATCH_PROPS = [SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch, SKOS.narrowMatch]


def load(path):
    g = rdflib.Graph()
    g.parse(path)
    return g


def domain_prop_uris(g):
    return {RICE[p] for p in DOMAIN_PROPS}


def baseline_stats(g):
    stats = {}
    stats["total_triples"] = len(g)
    stats["named_classes"] = len({c for c in g.subjects(RDF.type, OWL.Class)
                                   if isinstance(c, rdflib.URIRef)})
    stats["object_properties"] = len(set(g.subjects(RDF.type, OWL.ObjectProperty)))
    stats["datatype_properties"] = len(set(g.subjects(RDF.type, OWL.DatatypeProperty)))
    stats["annotation_properties"] = len(set(g.subjects(RDF.type, OWL.AnnotationProperty)))

    all_ind = set(g.subjects(RDF.type, OWL.NamedIndividual))
    images = set(g.subjects(RDF.type, RICE.ImageObservation))
    datasets = set(g.subjects(RDF.type, DCAT.Dataset))
    # "Domain individuals" per the v0.4 baseline = everything that is not
    # an ImageObservation (includes the one dcat:Dataset individual).
    domain_ind = all_ind - images

    stats["individuals"] = len(all_ind)
    stats["image_individuals"] = len(images)
    stats["domain_individuals"] = len(domain_ind)

    stats["owl_axiom_count"] = len(set(g.subjects(RDF.type, OWL.Axiom)))

    dprops = domain_prop_uris(g)
    domain_assertions = [(s, p, o) for s, p, o in g if p in dprops]
    stats["domain_assertions"] = len(domain_assertions)

    per_prop = defaultdict(int)
    for s, p, o in domain_assertions:
        per_prop[p.split("#")[-1]] += 1
    stats["domain_assertions_by_prop"] = dict(per_prop)

    stats["skos_exactMatch"] = len(list(g.triples((None, SKOS.exactMatch, None))))
    stats["skos_closeMatch"] = len(list(g.triples((None, SKOS.closeMatch, None))))
    stats["skos_broadMatch"] = len(list(g.triples((None, SKOS.broadMatch, None))))
    stats["skos_narrowMatch"] = len(list(g.triples((None, SKOS.narrowMatch, None))))

    stats["eppo_code_assertions"] = len(list(g.triples((None, RICE.eppoCode, None))))

    # individuals typed ONLY NamedIndividual (no other rdf:type)
    only_named = 0
    for ind in all_ind:
        types = set(g.objects(ind, RDF.type))
        if types == {OWL.NamedIndividual}:
            only_named += 1
    stats["individuals_only_named"] = only_named

    todo_literals = 0
    for s, p, o in g:
        if isinstance(o, rdflib.Literal) and "TODO" in str(o):
            todo_literals += 1
    stats["todo_literals"] = todo_literals

    return stats, domain_ind, images, datasets, dprops, domain_assertions


def check_provenance(g, domain_assertions):
    """Every domain assertion must have exactly one owl:Axiom; every
    owl:Axiom reifying a domain-property triple must point at an
    asserted triple."""
    dprops = domain_prop_uris(g)

    axiom_by_triple = defaultdict(list)
    orphan_axioms = []  # axiom exists but base triple not asserted
    for ax in g.subjects(RDF.type, OWL.Axiom):
        s = g.value(ax, OWL.annotatedSource)
        p = g.value(ax, OWL.annotatedProperty)
        o = g.value(ax, OWL.annotatedTarget)
        if p not in dprops:
            continue
        axiom_by_triple[(s, p, o)].append(ax)
        if (s, p, o) not in g:
            orphan_axioms.append((ax, s, p, o))

    missing_provenance = []
    duplicate_provenance = []
    for triple in domain_assertions:
        axioms = axiom_by_triple.get(triple, [])
        if len(axioms) == 0:
            missing_provenance.append(triple)
        elif len(axioms) > 1:
            duplicate_provenance.append((triple, len(axioms)))

    covered = len(domain_assertions) - len(missing_provenance)
    return {
        "coverage": f"{covered}/{len(domain_assertions)}",
        "missing_provenance": missing_provenance,
        "duplicate_provenance": duplicate_provenance,
        "orphan_axioms": orphan_axioms,
    }


def check_duplicate_identifiers(g):
    eppo_by_value = defaultdict(list)
    for s, o in g.subject_objects(RICE.eppoCode):
        eppo_by_value[str(o)].append(s)
    dup_eppo = {v: subs for v, subs in eppo_by_value.items() if len(subs) > 1}

    align_by_iri_and_type = defaultdict(list)
    for match_prop in SKOS_MATCH_PROPS:
        for s, o in g.subject_objects(match_prop):
            align_by_iri_and_type[(str(o), match_prop.split("#")[-1])].append(s)
    # "shared alignment IRI" = same external IRI used by >1 individual,
    # regardless of match type, per the task 0.1 acceptance wording
    align_by_iri = defaultdict(list)
    for match_prop in SKOS_MATCH_PROPS:
        for s, o in g.subject_objects(match_prop):
            align_by_iri[str(o)].append((s, match_prop.split("#")[-1]))
    dup_align = {iri: rows for iri, rows in align_by_iri.items() if len(rows) > 1}

    return {"duplicate_eppo": dup_eppo, "duplicate_alignment_iris": dup_align}


def _range_classes(g, prop):
    """Return the set of class URIs in a property's rdfs:range, expanding
    owl:unionOf if present. Returns None if no range declared."""
    ranges = list(g.objects(prop, RDFS.range))
    if not ranges:
        return None
    classes = set()
    for r in ranges:
        union = g.value(r, OWL.unionOf)
        if union is not None:
            classes.update(Collection(g, union))
        else:
            classes.add(r)
    return classes


def _all_superclasses(g, cls, cache):
    if cls in cache:
        return cache[cls]
    seen = {cls}
    frontier = [cls]
    while frontier:
        c = frontier.pop()
        for sup in g.objects(c, RDFS.subClassOf):
            if sup not in seen and isinstance(sup, rdflib.URIRef):
                seen.add(sup)
                frontier.append(sup)
    cache[cls] = seen
    return seen


def check_range_conformance(g, dprops):
    sup_cache = {}
    violations = []
    for p in dprops:
        range_classes = _range_classes(g, p)
        if not range_classes:
            continue
        for s, o in g.subject_objects(p):
            o_types = set(g.objects(o, RDF.type))
            if not o_types:
                violations.append((s, p, o, "no rdf:type on target"))
                continue
            ok = False
            for t in o_types:
                if t in range_classes:
                    ok = True
                    break
                if _all_superclasses(g, t, sup_cache) & range_classes:
                    ok = True
                    break
            if not ok:
                violations.append((s, p, o, f"types {[t.split('#')[-1] for t in o_types]} not in range"))
    return violations


def format_report(label, stats, prov, dupes, range_violations):
    lines = [f"# Verification report — {label}\n"]
    lines.append("## Baseline figures\n")
    lines.append(f"- Total triples: {stats['total_triples']}")
    lines.append(f"- Named classes: {stats['named_classes']}")
    lines.append(f"- Object properties: {stats['object_properties']}")
    lines.append(f"- Datatype properties: {stats['datatype_properties']}")
    lines.append(f"- Annotation properties: {stats['annotation_properties']}")
    lines.append(f"- Individuals: {stats['individuals']}")
    lines.append(f"- ImageObservation individuals: {stats['image_individuals']}")
    lines.append(f"- Domain individuals: {stats['domain_individuals']}")
    lines.append(f"- owl:Axiom provenance records: {stats['owl_axiom_count']}")
    lines.append(f"- Domain-level assertions: {stats['domain_assertions']}")
    for prop, count in sorted(stats["domain_assertions_by_prop"].items()):
        lines.append(f"    - {prop}: {count}")
    lines.append(f"- skos:exactMatch / closeMatch / broadMatch / narrowMatch: "
                  f"{stats['skos_exactMatch']} / {stats['skos_closeMatch']} / "
                  f"{stats['skos_broadMatch']} / {stats['skos_narrowMatch']}")
    lines.append(f"- eppoCode assertions: {stats['eppo_code_assertions']}")
    lines.append(f"- Individuals typed only NamedIndividual: {stats['individuals_only_named']}")
    lines.append(f"- TODO literals: {stats['todo_literals']}")

    lines.append("\n## Provenance coverage\n")
    lines.append(f"- Coverage: {prov['coverage']}")
    lines.append(f"- Assertions missing provenance: {len(prov['missing_provenance'])}")
    for s, p, o in prov["missing_provenance"]:
        lines.append(f"    - {s.split('#')[-1]} {p.split('#')[-1]} {str(o).split('#')[-1]}")
    lines.append(f"- Assertions with duplicate provenance records: {len(prov['duplicate_provenance'])}")
    for (s, p, o), n in prov["duplicate_provenance"]:
        lines.append(f"    - {s.split('#')[-1]} {p.split('#')[-1]} {str(o).split('#')[-1]} (x{n})")
    lines.append(f"- Orphan owl:Axiom records (base triple not asserted): {len(prov['orphan_axioms'])}")
    for ax, s, p, o in prov["orphan_axioms"]:
        sn = s.split('#')[-1] if s else s
        pn = p.split('#')[-1] if p else p
        on = str(o).split('#')[-1] if o else o
        lines.append(f"    - {sn} {pn} {on}")

    lines.append("\n## Duplicate identifiers\n")
    lines.append(f"- Duplicate eppoCode values: {len(dupes['duplicate_eppo'])}")
    for val, subs in dupes["duplicate_eppo"].items():
        names = ", ".join(s.split("#")[-1] for s in subs)
        lines.append(f"    - {val}: {names}")
    lines.append(f"- Alignment IRIs used by more than one individual: {len(dupes['duplicate_alignment_iris'])}")
    for iri, rows in dupes["duplicate_alignment_iris"].items():
        names = ", ".join(f"{s.split('#')[-1]} ({mt})" for s, mt in rows)
        lines.append(f"    - {iri}: {names}")

    lines.append("\n## Range conformance\n")
    lines.append(f"- Violations: {len(range_violations)}")
    for s, p, o, reason in range_violations:
        lines.append(f"    - {s.split('#')[-1]} {p.split('#')[-1]} {str(o).split('#')[-1]} — {reason}")

    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--label", default=None)
    ap.add_argument("--report", default=None)
    args = ap.parse_args()

    label = args.label or args.input
    g = load(args.input)
    stats, domain_ind, images, datasets, dprops, domain_assertions = baseline_stats(g)
    prov = check_provenance(g, domain_assertions)
    dupes = check_duplicate_identifiers(g)
    range_violations = check_range_conformance(g, dprops)

    report = format_report(label, stats, prov, dupes, range_violations)
    print(report)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nWrote {args.report}", file=sys.stderr)

    # exit non-zero if provenance invariant is broken
    if prov["missing_provenance"] or prov["orphan_axioms"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
