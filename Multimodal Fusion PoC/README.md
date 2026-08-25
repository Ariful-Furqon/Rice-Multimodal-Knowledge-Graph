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

**Last run:** 2026-08-19.

**See also:** `fusion_diagnostic.py` and `fusion_diagnostic_notes.md` in
this folder. They test the "insufficient tuning" attribution below and
find it incomplete — read them before citing the similarity matrix in any
report. `ikrl_vs_cnn.py` and `ikrl_vs_cnn_results.md` are the follow-up
that acts on that diagnosis: a leakage-safe IKRL-style fusion classifier
compared against a plain-CNN baseline on the full dataset.

## What it does

1. **Graph embedding** — loads `Rice MMKG.rdf`, extracts all URI–URI
   triples (43,456 triples, 10,564 entities, 22 relations), and trains a
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
disease/pest/symptom/health-status label. This was originally attributed
to insufficient tuning (too few TransE epochs, a generic ImageNet
encoder). **`fusion_diagnostic.py` tested that attribution directly and
found it incomplete** — see `fusion_diagnostic_notes.md` for the full
analysis. In short:

- Every `LeafImage` individual is structurally identical to every other
  one sharing its `annotatedAs` label — 10,407 images collapse onto just
  10 distinct graph signatures. No amount of training can recover
  per-image signal that isn't in the graph to begin with.
- The graph embedding's norm is ~0.06% of the fused vector's squared
  norm, so concatenation is arithmetically dominated by the visual half;
  the fused similarity matrix is within 0.0006 of the visual-only matrix.
  The 0.73–0.93 range is a property of ResNet features on natural images,
  not a measurement of fusion quality.
- More epochs or a fine-tuned encoder would not change either finding —
  the binding constraint is that per-image graph properties
  (`observationDate`, `severityScore`, `confidenceScore`) are declared in
  the schema but never asserted.

**Conclusion to report:** the fusion mechanism is technically validated
end-to-end. Embedding quality is not yet a meaningful question at
image level, because the graph does not yet carry per-image content to
embed — that is a data-population gap, not a tuning gap. Usable graph
signal does exist at class level (shared symptom/risk-factor structure)
and can be used as a classifier prior today without new data; see
`fusion_diagnostic_notes.md` for both routes forward.

## Next steps

- **Done (2026-08-25):** Route B, evaluated on the full 10,407-image
  population against a concrete downstream task, as an IKRL-style fusion
  classifier vs. a plain-CNN baseline — see `ikrl_vs_cnn.py` and
  `ikrl_vs_cnn_results.md`. Fusion wins by +8.5 points test accuracy
  (71.1% vs. 62.6%), with the class-level structure embedding trained on a
  domain-only subgraph that excludes every `ImageObservation` individual,
  so the leakage risk flagged below does not apply to that result. That
  same script also re-runs this PoC's similarity-matrix sanity check, but
  over Model B's trained projection instead of an untrained per-image
  embedding lookup — see the results doc's last section for whether
  class-block structure emerges once the projection is fit to something.
- Still open — Route A: populate the per-image properties that are
  declared but empty (`observationDate`, `severityScore`,
  `confidenceScore`, and location, which isn't modelled at all) so that
  image-level fusion has non-label signal to combine.
- Still open: re-run `ikrl_vs_cnn.py` across multiple seeds/splits before
  treating the +8.7-point gap as a stable result, and add a fine-tuned
  (not frozen) ResNet-18 baseline for a stronger CNN comparison point —
  see the caveats in `ikrl_vs_cnn_results.md`.
- Normalize graph and visual vectors to comparable magnitude before any
  future *concatenation*-style fusion (the IKRL-style comparison above
  sidesteps this by using a learned gate instead of raw concatenation).
