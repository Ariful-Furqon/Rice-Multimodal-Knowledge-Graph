# Multimodal Fusion Proof-of-Concept

## Purpose and scope

This folder demonstrates, end-to-end, the mechanism for combining Rice
MMKG's two representations — the symbolic graph and the raw Paddy Doctor
images — into a single fused vector. It is a **proof of mechanism, not a
trained or validated model**: the goal is to confirm the architecture built
in `Ontology/Rice MMKG.rdf` (deterministic `PaddyDoctor_<label>_<filename>`
IRIs linking `LeafImage` individuals to their source image files) actually
supports downstream multimodal fusion, before investing in a full training
pipeline.

**Run:** `python fusion_poc.py` (from anywhere; paths resolve relative to
this file). Requires `rdflib`, `torch`, `torchvision`, `pillow`.

**Last run:** 2026-08-07.

## What it does

1. **Graph embedding** — loads `Rice MMKG.rdf`, extracts all URI–URI
   triples (31,634 triples, 10,550 entities, 20 relations), and trains a
   minimal TransE model from scratch (pure PyTorch, 64-dimensional, 100
   epochs, margin ranking loss with random negative sampling). No external
   graph-embedding library — the implementation is small enough to read
   directly in `fusion_poc.py`.
2. **Visual embedding** — loads a pretrained ResNet-18 (ImageNet weights,
   `torchvision`), strips the classification head, and extracts a 512-d
   feature vector per image. No fine-tuning.
3. **Fusion** — for the 10 pilot images (one per Paddy Doctor label, the
   same ones populated first in the KG), concatenates the entity's graph
   embedding (64-d) with its image's visual embedding (512-d) into a
   single 576-d vector. The join key between the two vector spaces is the
   image's `LeafImage` IRI — no additional alignment logic was needed,
   which is the main point of the demonstration.
4. **Sanity check** — prints a 10×10 cosine-similarity matrix over the
   fused vectors.

## Result and interpretation

The pipeline runs successfully and produces well-formed 576-d fused
vectors for all 10 samples — **this confirms the mechanism works**: the
graph and image representations can be joined and combined without any
custom glue code beyond the shared IRI.

The similarity matrix, however, shows uniformly high similarity (roughly
0.73–0.93) across all class pairs, with no clear block structure by
disease/pest/symptom/health-status label. **This does not mean the
approach doesn't work — it means this particular PoC was not tuned to
produce discriminative embeddings**, for two expected reasons:

- The TransE model was trained for only 100 epochs with no hyperparameter
  search, and most `LeafImage` individuals have very few graph
  connections (`rdf:type` + `classifiedAs`), so the graph signal per image
  is thin.
- The visual encoder is generic ImageNet ResNet-18 with no fine-tuning on
  rice leaf imagery, so its features are not yet specialized for this
  domain.

**Conclusion to report:** the fusion mechanism is technically validated
end-to-end; embedding quality is a separate, unstarted piece of future
work (longer/tuned graph-embedding training, a fine-tuned or
domain-specific visual encoder, and a proper train/val/test evaluation —
none of which are in scope for a schema-level proof of concept).

## Next steps (not yet done)

- Fine-tune or replace the visual encoder with one trained on rice leaf
  disease imagery.
- Train the graph embedding for longer with a validated hyperparameter
  search, ideally using a maintained library (e.g. PyKEEN) rather than the
  from-scratch implementation here.
- Scale from the 10-image pilot to the full 10,407-image population.
- Evaluate the fused representation on a concrete downstream task (e.g.
  disease classification) rather than just eyeballing cosine similarity.
