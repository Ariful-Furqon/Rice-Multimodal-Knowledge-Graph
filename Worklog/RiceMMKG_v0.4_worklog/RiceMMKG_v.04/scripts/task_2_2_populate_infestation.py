#!/usr/bin/env python3
"""Task 2.2 — one Infestation individual per Pest, named from the damage
rather than the organism, plus a causes assertion from each pest. Also
emits reports/vector_todo.csv for the human-verified transmits relations
(Checkpoint C6) — none are asserted here.
"""
import argparse
import csv
import os
from rdflib import Graph, Namespace, Literal, RDF, RDFS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

# (Pest local name, Infestation local name, Infestation label, comment)
INFESTATIONS = [
    ("Hispa", "Hispa_Leaf_Damage", "Hispa Leaf Damage",
     "Whitish parallel scraping streaks on leaves left by hispa beetle feeding."),
    ("Armyworm", "Armyworm_Defoliation", "Armyworm Defoliation",
     "Leaf tissue consumed by armyworm larvae, ranging from partial to total defoliation."),
    ("Brown_Planthopper", "Brown_Planthopper_Infestation", "Brown Planthopper Infestation",
     "Plant condition produced by sustained Brown Planthopper feeding, distinct from the "
     "Hopper_Burn symptom it produces."),
    ("Leaf_Folder", "Leaf_Folder_Damage", "Leaf Folder Damage",
     "Longitudinally folded/rolled leaves with scraped tissue left by leaf folder larvae."),
    ("Rice_Bug", "Rice_Bug_Grain_Damage", "Rice Bug Grain Damage",
     "Discoloured, empty, or shrivelled grains caused by rice bug feeding on developing panicles."),
    ("Stem_Borer", "Stem_Borer_Damage", "Stem Borer Damage",
     "Larval boring damage to rice stems/tillers, distinct from the Deadheart symptom it produces."),
]


def apply(g):
    added_individuals = 0
    added_causes = 0
    for pest_local, inf_local, label, comment in INFESTATIONS:
        pest = RICE[pest_local]
        inf = RICE[inf_local]
        if (inf, RDF.type, RICE.Infestation) not in g:
            g.add((inf, RDF.type, __import__("rdflib").OWL.NamedIndividual))
            g.add((inf, RDF.type, RICE.Infestation))
            g.add((inf, RDFS.label, Literal(label)))
            g.add((inf, RDFS.comment, Literal(comment)))
            added_individuals += 1
        if (pest, RICE.causes, inf) not in g:
            g.add((pest, RICE.causes, inf))
            added_causes += 1
    return added_individuals, added_causes


def emit_vector_csv(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pests = [p for p, *_ in INFESTATIONS]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pest", "transmits_pathogen", "source_citation"])
        for p in pests:
            w.writerow([p, "", ""])
    print(f"Wrote {path} ({len(pests)} rows)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--vector-csv", default="reports/vector_todo.csv")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)
    added_ind, added_causes = apply(g)
    after = len(g)

    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Infestation individuals added: {added_ind}")
    print(f"causes assertions added: {added_causes}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")

    emit_vector_csv(args.vector_csv)


if __name__ == "__main__":
    main()
