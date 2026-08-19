#!/usr/bin/env python3
"""Task 2.1 — introduce the AnnotationLabel layer.

1. Create 10 AnnotationLabel individuals, rice:label_<paddy-doctor-string>.
2. fromSource -> PaddyDoctorDataset on each.
3. denotes from each label to the domain entity it currently points at,
   EXCEPT Hispa -> denotes the Hispa_Leaf_Damage Infestation (from Task 2.2),
   not the Hispa Pest individual itself.
4. Retarget all 10,407 annotatedAs assertions from domain entities to the
   corresponding label individual.
5. Move sourceDatasetLabel off the 10,407 image individuals and the 10
   domain individuals onto the 10 label individuals; set its rdfs:domain
   to AnnotationLabel.
"""
import argparse
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

# domain entity local name -> denotes target local name (differs from the
# entity itself only for Hispa, per Task 2.2's Infestation individual)
DENOTES_OVERRIDE = {
    "Hispa": "Hispa_Leaf_Damage",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    dataset = RICE.PaddyDoctorDataset
    images = set(g.subjects(RDF.type, RICE.ImageObservation))

    # Discover the 10 domain individuals that currently carry sourceDatasetLabel
    # (these are exactly the annotatedAs targets, per the v0.3 alignment convention).
    domain_label_pairs = [
        (s, str(o)) for s, p, o in g.triples((None, RICE.sourceDatasetLabel, None))
        if s not in images
    ]
    assert len(domain_label_pairs) == 10, f"expected 10, got {len(domain_label_pairs)}"

    label_individuals = {}  # domain_entity URIRef -> label URIRef
    for domain_entity, label_str in domain_label_pairs:
        label_ind = RICE[f"label_{label_str}"]
        label_individuals[domain_entity] = label_ind

        g.add((label_ind, RDF.type, OWL.NamedIndividual))
        g.add((label_ind, RDF.type, RICE.AnnotationLabel))
        g.add((label_ind, RDFS.label, Literal(f"Paddy Doctor label: {label_str}")))
        g.add((label_ind, RICE.fromSource, dataset))
        g.add((label_ind, RICE.sourceDatasetLabel, Literal(label_str)))

        domain_local = str(domain_entity).rsplit("#", 1)[1]
        denotes_local = DENOTES_OVERRIDE.get(domain_local, domain_local)
        g.add((label_ind, RICE.denotes, RICE[denotes_local]))

        # remove sourceDatasetLabel from the domain individual
        g.remove((domain_entity, RICE.sourceDatasetLabel, Literal(label_str)))

    # Retarget all annotatedAs assertions from domain entity -> label individual
    retargeted = 0
    for s, p, o in list(g.triples((None, RICE.annotatedAs, None))):
        if o in label_individuals:
            g.remove((s, p, o))
            g.add((s, p, label_individuals[o]))
            retargeted += 1

    # Move sourceDatasetLabel off the images entirely
    removed_from_images = 0
    for s, p, o in list(g.triples((None, RICE.sourceDatasetLabel, None))):
        if s in images:
            g.remove((s, p, o))
            removed_from_images += 1

    # sourceDatasetLabel domain -> AnnotationLabel
    g.remove((RICE.sourceDatasetLabel, RDFS.domain, None))
    g.add((RICE.sourceDatasetLabel, RDFS.domain, RICE.AnnotationLabel))

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")

    print(f"AnnotationLabel individuals created: {len(label_individuals)}")
    print(f"annotatedAs assertions retargeted: {retargeted}")
    print(f"sourceDatasetLabel removed from images: {removed_from_images}")
    print(f"Triple count before: {before}, after: {after}, delta: {after - before}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
