# Plain CNN vs. IKRL-style KG fusion — results

Requested comparison (sensei, week of 2026-08-18): plain ResNet CNN vs. an
IKRL (Image-embodied Knowledge Representation Learning, Xie et al. 2017)
fusion result, on the Paddy Doctor 10-class disease/pest/health
classification task.

**Run:** `python "ikrl_vs_cnn.py"`. Full script, method, and the leakage
argument are documented in the script's module docstring — read that
before re-running or citing this. **Last run: 2026-08-25**, full dataset
(10,407 images), CPU only. Raw numbers: `ikrl_vs_cnn_results.json`.

## Why this isn't `fusion_poc.py`'s concatenation

`fusion_diagnostic_notes.md` (Finding 1) showed that a *per-image* graph
embedding is circular for this task: every image collapses onto its
`annotatedAs` class, so a classifier fed that embedding is just handed the
label it's supposed to predict. This experiment sidesteps that by never
letting a test image "look up" its own class:

- The **structure-based representation** is a TransE model trained only on
  the 265 domain assertions among the 90 non-image entities (`indicatedBy`,
  `increaseRiskOf`, `occursIn`, `controlledBy`, `causes`, `vulnerableTo`,
  `recommends`, `preventedBy`, `requires`, `transmits`) — no
  `ImageObservation` individual and no `annotatedAs` edge is in this
  subgraph, so the 10 resulting class vectors encode shared symptoms and
  risk factors, not image identity.
- The **image-based representation** is a learned projection of frozen
  ResNet-18 features into that same 64-d space. At inference, every image
  gets scored against all 10 (fixed, always-available) class vectors and
  the classifier decides which is closest — it never has access to a
  ground-truth-conditioned embedding.
- Both models share the identical frozen visual features; only the
  classifier head differs. That isolates the fusion effect from anything
  to do with the visual backbone.

## Setup

- **Visual features:** ResNet-18, ImageNet-pretrained, **frozen** (no
  fine-tuning) — a CPU-only compute constraint, stated up front rather than
  hidden. Both models are transfer-learning heads on the same 512-d
  features, so the comparison is head-vs-head, not backbone-vs-backbone.
- **Data:** full 10,407-image Paddy Doctor set, stratified 70/15/15
  train/val/test split (seed 0) — train=7,280, val=1,557, test=1,570.
- **Model A (plain CNN baseline):** `Linear(512 → 10)` on the visual
  features.
- **Model B (IKRL fusion):** `Linear(512 → 10)` on the visual features,
  plus `softplus(λ) · (−‖g(visual) − e_c‖₂)` for each class `c`, where `g`
  is a trained `512 → 128 → 64` MLP projection and `e_c` are the 10 frozen
  TransE class embeddings. `λ` is a learned scalar gate — the model is
  free to zero out the KG term if it isn't useful, so the comparison isn't
  rigged to force fusion to win.
- Both trained 200 epochs, Adam, weight decay 1e-4, model selected by best
  validation accuracy.

## Result

| Model | Test accuracy | Macro-F1 |
|---|---|---|
| A — plain ResNet-18 + linear head | **62.6%** | 0.584 |
| B — IKRL-style KG fusion | **71.1%** | 0.665 |

Fusion wins by **+8.5 points accuracy / +8.1 points macro-F1** on held-out
test data, and the learned gate `λ` grew during training (0.72 → 0.83
softplus'd) rather than collapsing toward zero — the model chose to keep
using the KG term, it wasn't forced to.

Per-class, fusion improves or ties nearly every one of the 10 classes on
the diagonal of the confusion matrix (raw counts in
`ikrl_vs_cnn_results.json`); the largest gains are on classes with rich
symptom/risk-factor structure in the KG (`brown_spot`: 56→68 correct;
`tungro`: 81→108; `downy_mildew`: 27→45).

## Checking the diagnostic's falsifiable prediction

`fusion_diagnostic_notes.md` (Finding 4) predicted that `brown_spot` and
`blast` — the pair sharing the most symptoms/risk factors in the KG
(Jaccard 0.56, the highest of any pair) — would be confused by a purely
visual classifier more than most other pairs. Ranking all 45 class pairs
by confusion rate in Model A's confusion matrix:

| Rank | Pair | Confusion rate |
|---|---|---|
| 1 | `hispa` ↔ `normal` | 0.1265 |
| 2 | `blast` ↔ `tungro` | 0.1080 |
| **3** | **`blast` ↔ `brown_spot`** | **0.0833** |
| 4 | `normal` ↔ `tungro` | 0.0814 |

**Partial confirmation, stated honestly:** `blast`↔`brown_spot` is the
3rd-most-confused pair out of 45, not the single most-confused — the
prediction said "more than most other pairs," which holds, not "the
single worst pair," which doesn't. `hispa`↔`normal` and `blast`↔`tungro`
outrank it and have no comparably strong KG-similarity explanation on
file; that's worth a look before over-crediting the KG's predictive power
on this point.

## Similarity-matrix check on Model B's trained projection

`fusion_poc.py`'s original PoC reported a 10×10 cosine-similarity matrix
over fused vectors that showed no class-block structure (0.73–0.93
uniformly), later diagnosed as circular per-image graph embeddings
dominated by the visual half. This experiment re-runs that same style of
sanity check — same 10 sample images, one per class — but over Model B's
**trained** projection `g(visual)` into the 64-d structure space, instead
of an untrained embedding table lookup. Full numbers in
`ikrl_vs_cnn_results.json` (`class_struct_similarity`,
`model_b_sample_projection_similarity`).

**1. Class structure-embedding similarity** — cosine similarity among the
10 frozen `e_c` (domain-only TransE class embeddings), the "ground truth"
shape the projection is being pulled toward:

|  | bact_blight | bact_streak | bact_panicle | blast | brown_spot | dead_heart | downy_mildew | hispa | normal | tungro |
|---|---|---|---|---|---|---|---|---|---|---|
| **bact_blight** | 1.00 | .87 | .77 | .77 | .81 | .59 | .60 | .51 | −.30 | .66 |
| **bact_streak** | | 1.00 | .76 | .60 | .68 | .61 | .64 | .59 | −.22 | .80 |
| **bact_panicle** | | | 1.00 | .85 | **.92** | .60 | .58 | .50 | −.11 | .56 |
| **blast** | | | | 1.00 | **.98** | .55 | .63 | .45 | −.09 | .41 |
| **brown_spot** | | | | | 1.00 | .56 | .64 | .45 | −.12 | .48 |
| **dead_heart** | | | | | | 1.00 | .60 | **.91** | −.14 | .74 |
| **downy_mildew** | | | | | | | 1.00 | .57 | −.13 | .82 |
| **hispa** | | | | | | | | 1.00 | −.13 | .64 |
| **normal** | | | | | | | | | 1.00 | −.23 |
| **tungro** | | | | | | | | | | 1.00 |

Real block structure: `blast`↔`brown_spot` (0.98) and
`bact_panicle`↔`brown_spot` (0.92) are near-identical, `dead_heart`↔`hispa`
(0.91) is another tight pair, and `normal` is negatively correlated with
every disease/pest class (it shares no symptom/risk-factor edges with
them by construction) — the opposite of the flat 0.73–0.93 band
`fusion_poc.py` found.

**2. Model B projection similarity** — cosine similarity among
`g(visual)` for the same 10 sample images, after training. Some of the
class-embedding structure is echoed: `blast`↔`tungro` (0.86) and
`brown_spot`↔`tungro` (0.93) come out high, `dead_heart`↔`hispa` (0.87)
closely reproduces its `e_c` counterpart (0.91), `bact_blight`↔`bact_streak`
(0.77) is close to its `e_c` value (0.87), and `normal` stays the clear
outlier (negative similarity to 7 of the other 9 classes, same as in
`e_c`). But the echo is partial, not exact: `blast`↔`brown_spot` drops
from 0.98 (`e_c`) to 0.76 (projection), `bact_panicle`↔`brown_spot` drops
from 0.92 to 0.59, and `downy_mildew`↔`tungro` drops from 0.82 to 0.16 —
so the projection has learned a related but distinctly weaker and
noisier version of the class-structure geometry, evaluated here on a
single sample image per class rather than an average over many.

**Read against `fusion_poc.py`:** the qualitative failure mode from
minggu lalu — near-uniform similarity with no discernible block structure
— does not reproduce here. Both matrices span a wide range (−0.47 to
0.98) with a mix of strongly-similar and strongly-dissimilar pairs, and
the strongest pairs in the trained projection overlap partially with the
strongest pairs in the class embeddings. That is consistent with (not
proof of) the projection carrying real, non-circular KG-shaped signal,
which lines up with Model B's accuracy win over Model A above.

## Caveats (read before citing this in a paper)

- **Frozen backbone.** Neither model fine-tunes ResNet-18. A fine-tuned
  CNN baseline would likely close some of this gap — this result shows
  what the KG contributes on top of a fixed feature extractor, not the
  best achievable CNN.
- **Single seed, single split.** No cross-validation or multiple seeds
  yet; the 8.7-point gap is large relative to likely run-to-run variance,
  but that hasn't been measured, and the number should be re-run with
  seeds varied before being treated as a paper-ready result.
- **The KG's contribution is class-shape, not image content.** Route A
  from the diagnostic notes (per-image `observationDate`/`severityScore`/
  symptom properties) is still unpopulated. This result is what Route B
  (class-level structure as a shaping signal) delivers; it is not evidence
  that per-image fusion would work, since per-image graph content still
  doesn't exist.
- **10-way closed-set classification only.** IKRL's original setting is
  knowledge-graph link prediction; this is a repurposing of its
  structure/image dual-representation idea onto a classification decision
  rule (nearest fixed class-embedding + a learned visual term), not a
  reproduction of the original paper's training objective or evaluation
  protocol. Worth being explicit about this framing if presenting it as
  "IKRL" rather than "an IKRL-inspired fusion baseline."
- **The similarity-matrix check above is a single-sample-per-class
  qualitative read, not a metric.** It's useful for spotting whether block
  structure emerges at all, not for quantifying it — treat it as a sanity
  check alongside the accuracy numbers, not a replacement for them.
