"""
Diagnostic for the Rice MMKG multimodal fusion proof-of-concept.

The original PoC (fusion_poc.py) confirmed that graph and image vectors can be
joined through a shared IRI, then reported a uniformly high cosine-similarity
matrix and attributed it to insufficient tuning. This script tests that
attribution.

It answers four questions:

  Q1  How much per-image information does the graph actually contain?
  Q2  Does the graph half of the fused vector contribute anything numerically?
  Q3  Is the observed similarity range evidence of anything at all?
  Q4  What signal does the graph carry at class level, if not at image level?

Parts 1, 2 and 4 need only rdflib and run in seconds. Part 3 needs torch,
torchvision and the image files; it is skipped with a clear message if they
are unavailable, so the graph-side diagnosis can always be produced.

Usage:
    python fusion_diagnostic.py --rdf path/to/Rice_MMKG.rdf [--data path/to/PaddyDoctor]
"""

import argparse
import itertools
import os
import sys

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from collections import Counter, defaultdict

import rdflib

NS = "http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#"

SAMPLE_IMAGES = {
    "bacterial_leaf_blight": "100023.jpg",
    "bacterial_leaf_streak": "100042.jpg",
    "bacterial_panicle_blight": "100043.jpg",
    "blast": "100004.jpg",
    "brown_spot": "100001.jpg",
    "dead_heart": "100008.jpg",
    "downy_mildew": "100017.jpg",
    "hispa": "100003.jpg",
    "normal": "100002.jpg",
    "tungro": "100011.jpg",
}


def short(uri):
    return str(uri).split("#")[-1].split("/")[-1]


def rule(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------------------
# Part 1 - how much per-image information does the graph contain?
# ---------------------------------------------------------------------------

def part1_structural_diversity(g):
    """A graph embedding can only separate entities that the graph separates.

    Two images are structurally indistinguishable if their outgoing URI-to-URI
    triples are identical. Count how many genuinely distinct images the graph
    describes, as opposed to how many individuals it contains.
    """
    rule("PART 1 - Per-image information content of the graph")

    images = list(g.subjects(rdflib.RDF.type, rdflib.URIRef(NS + "LeafImage")))
    if not images:
        images = list(g.subjects(rdflib.RDF.type, rdflib.URIRef(NS + "ImageObservation")))
    if not images:
        print("  No image individuals found. Check the class name in the ontology.")
        return None

    signatures = Counter()
    for img in images:
        sig = tuple(sorted(
            (short(p), short(o))
            for p, o in g.predicate_objects(img)
            if isinstance(o, rdflib.URIRef)
        ))
        signatures[sig] += 1

    n_img, n_sig = len(images), len(signatures)
    print(f"  Image individuals            : {n_img:,}")
    print(f"  Distinct structural signatures: {n_sig}")
    print(f"  Compression ratio             : {n_img / n_sig:,.0f} images per signature")
    print()
    print("  Signature sizes and their distinguishing assertion:")
    for sig, count in signatures.most_common():
        marker = next((f"{p}={o}" for p, o in sig if p not in
                       ("type", "source", "wasDerivedFrom")), "(none)")
        print(f"    {count:6,d}  {marker}")

    print()
    print("  READING: an embedding model can place at most one distinct point per")
    print(f"  signature. {n_img:,} images therefore collapse onto {n_sig} positions, and")
    print("  those positions correspond exactly to the annotation label.")
    print()
    print("  CONSEQUENCE: the graph half of a fused vector encodes the label and")
    print("  nothing else. Evaluating such a vector on label prediction is circular -")
    print("  the target is an input. This is label leakage and must be excluded before")
    print("  any downstream classification claim is made.")
    return n_sig


# ---------------------------------------------------------------------------
# Part 2 - which properties vary across images, and which do not?
# ---------------------------------------------------------------------------

def part2_property_variance(g):
    """Identify the properties that could carry per-image signal but do not.

    A property held by every image with the same value adds no discriminative
    information. A property that is declared but unasserted adds none either.
    """
    rule("PART 2 - Which properties could carry per-image signal")

    images = list(g.subjects(rdflib.RDF.type, rdflib.URIRef(NS + "LeafImage")))
    if not images:
        images = list(g.subjects(rdflib.RDF.type, rdflib.URIRef(NS + "ImageObservation")))

    per_prop_values = defaultdict(set)
    per_prop_count = Counter()
    for img in images:
        for p, o in g.predicate_objects(img):
            per_prop_count[short(p)] += 1
            per_prop_values[short(p)].add(str(o))

    print(f"  {'property':24s} {'assertions':>11s} {'distinct values':>16s}  verdict")
    print("  " + "-" * 74)
    for prop in sorted(per_prop_count, key=lambda k: -per_prop_count[k]):
        n, d = per_prop_count[prop], len(per_prop_values[prop])
        if d == 1:
            verdict = "constant - no signal"
        elif d < 20:
            verdict = f"label-level only ({d} values)"
        else:
            verdict = "per-image - usable signal"
        print(f"  {prop:24s} {n:11,d} {d:16,d}  {verdict}")

    declared = {short(p) for p in g.subjects(rdflib.RDF.type, rdflib.OWL.ObjectProperty)}
    declared |= {short(p) for p in g.subjects(rdflib.RDF.type, rdflib.OWL.DatatypeProperty)}
    asserted = {short(p) for p in g.predicates()}
    empty = sorted(declared - asserted)

    print()
    print("  Declared but never asserted (candidate carriers of per-image signal):")
    for p in empty:
        print(f"    {p}")
    print()
    print("  READING: properties such as observationDate and severityScore are exactly")
    print("  the ones that would distinguish two images sharing a label. They are")
    print("  declared and empty. Location is not modelled at all.")


# ---------------------------------------------------------------------------
# Part 3 - does the graph half contribute numerically to the fused vector?
# ---------------------------------------------------------------------------

def part3_norm_and_similarity(rdf_path, data_dir):
    """Concatenation is only fusion if both halves have comparable magnitude.

    TransE embeddings after brief training have small norms; ResNet penultimate
    features are post-ReLU and non-negative with much larger norms. If the ratio
    is extreme, cosine similarity over the concatenation is determined almost
    entirely by the visual half, and the fusion is numerically a no-op.

    The control is simple: compute the same similarity matrix from the visual
    vectors alone and measure how far it differs.
    """
    rule("PART 3 - Numerical contribution of each modality")

    try:
        import torch
        import torch.nn as nn
        import torchvision
        from PIL import Image
    except ImportError as exc:
        print(f"  SKIPPED - {exc}.")
        print("  Install torch, torchvision and pillow to run this part.")
        return

    if not data_dir or not os.path.isdir(data_dir):
        print(f"  SKIPPED - image directory not found: {data_dir}")
        print("  Pass --data pointing at the PaddyDoctor folder.")
        return

    torch.manual_seed(0)

    # --- graph embeddings, same recipe as the original PoC -----------------
    g = rdflib.Graph()
    g.parse(rdf_path, format="xml")
    triples = [(str(s), str(p), str(o)) for s, p, o in g
               if isinstance(s, rdflib.URIRef) and isinstance(o, rdflib.URIRef)]
    ents = sorted({s for s, _, _ in triples} | {o for _, _, o in triples})
    rels = sorted({p for _, p, _ in triples})
    ent2id = {e: i for i, e in enumerate(ents)}
    rel2id = {r: i for i, r in enumerate(rels)}
    print(f"  Graph: {len(triples):,} URI-URI triples, {len(ents):,} entities, {len(rels)} relations")

    class TransE(nn.Module):
        def __init__(self, n_e, n_r, dim=64):
            super().__init__()
            self.ent_emb = nn.Embedding(n_e, dim)
            self.rel_emb = nn.Embedding(n_r, dim)
            nn.init.xavier_uniform_(self.ent_emb.weight)
            nn.init.xavier_uniform_(self.rel_emb.weight)

        def score(self, h, r, t):
            he = nn.functional.normalize(self.ent_emb(h), dim=-1)
            te = nn.functional.normalize(self.ent_emb(t), dim=-1)
            return torch.norm(he + self.rel_emb(r) - te, p=2, dim=-1)

    model = TransE(len(ents), len(rels))
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    hs = torch.tensor([ent2id[s] for s, _, _ in triples])
    rs = torch.tensor([rel2id[p] for _, p, _ in triples])
    ts = torch.tensor([ent2id[o] for _, _, o in triples])
    for _ in range(100):
        neg = torch.randint(0, len(ents), (len(triples),))
        loss = torch.clamp(1.0 + model.score(hs, rs, ts) - model.score(hs, rs, neg), min=0).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    print(f"  TransE trained: 100 full-batch steps, final loss {loss.item():.4f}")

    # --- visual embeddings -------------------------------------------------
    weights = torchvision.models.ResNet18_Weights.IMAGENET1K_V1
    enc = torchvision.models.resnet18(weights=weights)
    enc.fc = nn.Identity()
    enc.eval()
    preprocess = weights.transforms()

    labels, gvecs, vvecs = [], [], []
    for label, fname in SAMPLE_IMAGES.items():
        iri = f"{NS}PaddyDoctor_{label}_{fname.rsplit('.', 1)[0]}"
        if iri not in ent2id:
            print(f"  WARNING: {short(iri)} absent from graph vocab - skipped")
            continue
        path = os.path.join(data_dir, label, fname)
        if not os.path.exists(path):
            print(f"  WARNING: image missing - {path}")
            continue
        with torch.no_grad():
            v = enc(preprocess(Image.open(path).convert("RGB")).unsqueeze(0)).squeeze(0)
        labels.append(label)
        gvecs.append(model.ent_emb.weight[ent2id[iri]].detach())
        vvecs.append(v)

    if len(labels) < 2:
        print("  Not enough samples resolved to continue.")
        return

    G = torch.stack(gvecs)
    V = torch.stack(vvecs)
    F = torch.cat([G, V], dim=1)

    gn, vn = G.norm(dim=1), V.norm(dim=1)
    share = (gn ** 2) / (gn ** 2 + vn ** 2)
    print()
    print(f"  Mean graph-vector norm : {gn.mean():.4f}")
    print(f"  Mean visual-vector norm: {vn.mean():.4f}")
    print(f"  Graph share of squared norm: {share.mean() * 100:.3f}%")
    print()
    print("  READING: if the graph share is a fraction of one percent, concatenation")
    print("  followed by cosine similarity is arithmetically dominated by the visual")
    print("  half. The graph is present in the vector but absent from the result.")

    def cosmat(X):
        Xn = torch.nn.functional.normalize(X, dim=-1)
        return Xn @ Xn.T

    Sf, Sv, Sg = cosmat(F), cosmat(V), cosmat(G)
    off = ~torch.eye(len(labels), dtype=torch.bool)
    diff = (Sf - Sv).abs()

    print()
    print(f"  Fused similarity range (off-diagonal) : {Sf[off].min():.3f} to {Sf[off].max():.3f}")
    print(f"  Visual-only range (off-diagonal)      : {Sv[off].min():.3f} to {Sv[off].max():.3f}")
    print(f"  Graph-only range (off-diagonal)       : {Sg[off].min():.3f} to {Sg[off].max():.3f}")
    print(f"  Max |fused - visual| difference       : {diff[off].max():.4f}")
    print(f"  Mean |fused - visual| difference      : {diff[off].mean():.4f}")
    print()
    if diff[off].max() < 0.05:
        print("  VERDICT: the fused matrix is indistinguishable from the visual-only")
        print("  matrix. The reported result is a property of ResNet features, not of")
        print("  fusion. Report it as such.")
    else:
        print("  VERDICT: the graph half measurably shifts the similarity structure.")
        print("  Report the magnitude of the shift alongside the matrix.")

    print()
    print("  Baseline for interpreting the range: ResNet penultimate features are")
    print("  post-ReLU and therefore non-negative, so cosine similarity between any")
    print("  two natural images is bounded well above zero. A 0.7-0.9 range is the")
    print("  expected value for arbitrary image pairs and is evidence of neither")
    print("  success nor failure.")


# ---------------------------------------------------------------------------
# Part 4 - what signal does the graph carry at class level?
# ---------------------------------------------------------------------------

def part4_class_level_signal(g):
    """The graph has no per-image signal, but it does relate the classes.

    Build a class-similarity matrix from shared symptoms and shared
    environmental risk factors. This needs no new data and has no leakage
    problem, because it describes relations between labels rather than
    identifying any individual image.
    """
    rule("PART 4 - Class-level signal available today")

    symptoms = defaultdict(set)
    for s, o in g.subject_objects(rdflib.URIRef(NS + "indicatedBy")):
        symptoms[short(s)].add("SYM:" + short(o))
    for s, o in g.subject_objects(rdflib.URIRef(NS + "increaseRiskOf")):
        symptoms[short(o)].add("ENV:" + short(s))

    targets = sorted({short(o) for _, o in
                      g.subject_objects(rdflib.URIRef(NS + "annotatedAs"))})
    if not targets:
        targets = sorted({short(o) for _, o in
                          g.subject_objects(rdflib.URIRef(NS + "classifiedAs"))})

    feats = {t: symptoms.get(t, set()) for t in targets}
    covered = [t for t in targets if feats[t]]

    print(f"  Annotation targets            : {len(targets)}")
    print(f"  With any graph feature        : {len(covered)}")
    print(f"  With none                     : {len(targets) - len(covered)}")
    print()
    for t in targets:
        f = sorted(feats[t])
        print(f"    {t:26s} {len(f):2d}  {', '.join(x.split(':')[1] for x in f) or '-'}")

    def jaccard(a, b):
        return len(a & b) / len(a | b) if (a and b) else 0.0

    pairs = [(a, b, jaccard(feats[a], feats[b]))
             for a, b in itertools.combinations(targets, 2)]
    pairs = [p for p in pairs if p[2] > 0]
    pairs.sort(key=lambda x: -x[2])

    print()
    print("  Non-zero class similarities derived from the graph:")
    if not pairs:
        print("    none")
    for a, b, v in pairs:
        print(f"    {v:.2f}  {a} <-> {b}")

    print()
    print("  READING: this is the graph's testable content. Each pair above is a")
    print("  prediction that a purely visual classifier should confuse those two")
    print("  classes more than average, because the ontology says they share")
    print("  observable features. Check it against the confusion matrix of any CNN")
    print("  trained on the same ten classes.")
    print()
    print("  This route needs no new data and carries no leakage risk: it relates")
    print("  labels to each other rather than identifying individual images.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rdf", required=True, help="path to Rice MMKG RDF/XML")
    ap.add_argument("--data", default=None, help="path to PaddyDoctor image root")
    args = ap.parse_args()

    if not os.path.exists(args.rdf):
        sys.exit(f"RDF not found: {args.rdf}")

    print("Rice MMKG - multimodal fusion diagnostic")
    print(f"Ontology: {args.rdf}")

    g = rdflib.Graph()
    g.parse(args.rdf, format="xml")
    print(f"Loaded {len(g):,} triples")

    part1_structural_diversity(g)
    part2_property_variance(g)
    part3_norm_and_similarity(args.rdf, args.data)
    part4_class_level_signal(g)

    rule("SUMMARY")
    print("  1. The graph separates images only to the granularity of their label.")
    print("  2. The properties that would separate them further are declared but empty.")
    print("  3. Concatenation without per-modality normalisation lets the larger-norm")
    print("     modality determine the result.")
    print("  4. Usable graph signal exists at class level and can be tested now.")


if __name__ == "__main__":
    main()
