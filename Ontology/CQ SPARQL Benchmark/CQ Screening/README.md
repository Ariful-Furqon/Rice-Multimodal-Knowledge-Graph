# CQ Screening

How 173 competency questions elicited from five large language models were
filtered down to the 23 that go to expert validation, and how to reproduce that
filtering from the source files.

The deliverable is **[`reports/cq_stage3_final_tierA.md`](reports/cq_stage3_final_tierA.md)**.
Everything else in this directory exists to show how it was arrived at.

---

## The funnel

| Stage | What it decides | In | Out |
|---|---|---|---|
| 0 - Pool | nothing; verbatim extraction | 5 model outputs | **173** |
| 1 - Structural validity | is this a competency question at all? | 173 | 173, of which **8 flagged** |
| 2 - Deduplication | which CQs restate one requirement? | 173 | 148 provisional clusters *(superseded, see below)* |
| 3 - Scope gate | does it need a modality we do not have? | 173 | **64** Tier A, 109 Tier B |
| 3 - Adjudication | keep or drop, and grouping | 64 | **56** keep, 8 drop |
| 3 - Grouping | one canonical CQ per requirement | 56 | **23** |
| 4 - Reconciliation | how do these relate to the 25 benchmark CQs? | 23 vs 25 | 15 corroborated, **12 gaps** |
| 5 - Questionnaire | instantiate, blind, randomise | 23 | **23 items**, all included |

Stage 2's automatic clustering **did not survive**. Two independent similarity
signals were tried (TF-IDF cosine over question text, Jaccard over the
class/property signature) at many thresholds, and both conflate requirements
that are genuinely distinct: at every cut tried, *what pathogen causes blast*
clustered with *what symptoms are reported for blast*. Its output is kept for
the record, but the grouping that produced the final set was done by reading all
64 Tier A CQs. Stage 2's `n_models` figures are a lower bound and should not be
quoted.

## Two things to state in writing

**The scope decision.** Only text and image are claimed. RiceMMKG v0.6 holds
10,407 `ImageObservation` individuals, **zero** `SensorObservation` individuals,
and no variety, gene, document or region entities. The elicitation prompt
declared a four-modality KG as context to assume, so all five models wrote CQs
for a KG that does not exist yet: 45 of the 173 need sensor data, 39 need
genomic, 23 need both. Those become Tier B - a requirements-based justification
for the roadmap, not a claim about this release.

**The conflict of interest.** The Stage 3 grouping was drafted by Claude Opus 5,
which is *also one of the five models whose output forms the pool*. A model
graded its own work. It was reviewed and approved by M. A. Furqon on 2026-09-03.
Describe it as an LLM-assisted first pass, human-adjudicated - never as an
automatic result.

## Layout

```
CQ Screening/
├── README.md                         this file
├── CQ_Screening_Overview.pptx        15-slide deck explaining the funnel
├── make_slides.py                    builds that deck from data/ (not part
│                                     of the pipeline, hence not in scripts/)
├── scripts/                          run in order; each is self-contained
│   ├── stage0_build_pool.py          parse the five model outputs
│   ├── stage1_screen.py              structural validity triage
│   ├── stage2_cluster.py             automatic clustering (superseded)
│   ├── stage3_scope_and_group.py     scope gate, grouping, final CQ set
│   ├── stage4_reconcile.py           compare against the 25 benchmark CQs
│   └── stage5_questionnaire.py       build the blinded expert questionnaire
├── data/                             machine-readable, one row per CQ
│   ├── cq_stage0_pool.csv|.jsonl     the 173-CQ pool
│   ├── cq_stage1_adjudication.csv    flags + blank screener columns
│   ├── cq_stage2_*.csv               provisional clusters, borderline pairs
│   ├── cq_stage3_worksheet.csv       the 64 Tier A CQs, blank for adjudication
│   ├── cq_stage3_decisions.csv       the same, with decisions and groups
│   ├── cq_stage3_final_tierA.csv     the 23 canonical CQs
│   ├── cq_stage4_reconciliation.csv  one row per benchmark CQ
│   ├── cq_stage4_gaps.csv            elicited CQs the benchmark misses
│   ├── cq_stage5_items.csv           blinded items, presentation order
│   ├── cq_stage5_key.csv             unblinding key - never show to raters
│   └── cq_stage5_responses.csv       empty response template
└── reports/                          human-readable, for the paper
    ├── cq_stage0_pool.md             pool provenance and distribution
    ├── cq_stage1_proposal.md         rules, counts, every flagged CQ
    ├── cq_stage2_proposal.md         method and its stated limitation
    ├── cq_stage3_worksheet.md        readable worksheet
    ├── cq_stage3_decisions.md        per-group breakdown, dropped CQs
    ├── cq_stage3_final_tierA.md      ← the deliverable: the 23 CQs
    ├── cq_stage4_reconciliation.md   benchmark comparison and the 12 gaps
    └── cq_stage5_questionnaire.md    ← the form to hand to experts
```

Every artefact is named `cq_stage<N>_*`, so sorting either directory lays the
funnel out in order and no stage can look absent.

Source material lives in `../LLM Prompt/`: one shared prompt
(`rice_mmkg_cq_prompt.md`) and the five model outputs. Nothing in this directory
edits those.

## Reproducing

```bash
python scripts/stage0_build_pool.py
python scripts/stage1_screen.py
python scripts/stage2_cluster.py
python scripts/stage3_scope_and_group.py
python scripts/stage4_reconcile.py
python scripts/stage5_questionnaire.py
```

Requires Python 3 and numpy; no other dependencies, deliberately, so the
similarity method can be described exactly in a paper rather than deferred to a
library version. Scripts are idempotent and overwrite their own outputs.

Human decisions are not recomputed - they are recorded as the `LABELS` table in
`stage3_scope_and_group.py`, keyed by `pool_id`. Changing a filter therefore
cannot silently re-target a decision; the script asserts that its labels and its
Tier A set still correspond, and stops if they drift.

## What the 23 CQs look like

Six were proposed independently by four of the five models, and are effectively
the core of the ontology: pathogen causing a disease (`CQ-A01`), vector
transmission (`CQ-A02`), overlapping symptoms and what discriminates them
(`CQ-A04`), recommended control measures (`CQ-A07`), retrieving images by
condition (`CQ-A10`), and visual features separating confusable conditions
(`CQ-A17`).

Nine were proposed by a single model. **Keep them.** Stage 5 needs
low-convergence CQs in the questionnaire, or the hypothesis that convergence
predicts expert-rated relevance cannot be tested - and that hypothesis is the
methodological contribution.

**20 of the 56 retained CQs cannot yet be answered by v0.6.** That is not a
defect: competency questions are requirements, and an ontology that answers all
of its CQs on day one had its CQs written to fit what was already built. The
gaps are itemised at the end of `reports/cq_stage3_final_tierA.md` and constitute the
v0.7 work plan - `PlantPart` is missing, `confidenceScore` is declared but never
used, `SeverityLevel` exists but is not linked to any image.

## What Stage 4 found

The elicited set and the benchmark are **different instruments over the same
relations**, not competing formulations. Benchmark `CQ-01` asks *which rice
diseases have an identified causal pathogen* - a completeness ratio over
`causedBy`. Elicited `CQ-A01` asks *which pathogen causes a given rice disease* -
an answer about the domain. Both are legitimate; neither substitutes for the
other.

So 15 of 25 benchmark CQs are corroborated, and most of the remaining 10 are
graph-hygiene or description-logic checks no domain expert would pose. That is
the right division of labour. The one item to revisit is `CQ-20`, which counts
sensor observations - Tier B under the scope decision, and currently reported as
a passing benchmark item.

The actionable half is the other direction: **12 of the 23 elicited CQs have no
benchmark counterpart, and 9 of those 12 are image or cross-modal**. The
benchmark covers the symbolic layer thoroughly and the image layer barely.
Four are already answerable by v0.6 and could be implemented as SPARQL now:
`CQ-A04` (differential diagnosis), `CQ-A10`, `CQ-A16`, `CQ-A17`. `CQ-A04` is
the most striking - four of five models proposed it, it is the question a field
diagnostician actually asks, and the benchmark has no equivalent.

Detail in [`reports/cq_stage4_reconciliation.md`](reports/cq_stage4_reconciliation.md).

## Stage 5: the questionnaire

[`reports/cq_stage5_questionnaire.md`](reports/cq_stage5_questionnaire.md) is
ready to hand to experts. All 23 CQs are included - the planned size was 30-50
items, so nothing had to be sampled away, and the full convergence spread
survives (nine single-model CQs alongside six proposed by four models).

Every item is **instantiated** with an entity that exists in v0.6: not *"which
pathogen causes a given disease"* but *"which pathogen causes rice blast"*. An
expert cannot judge the former.

The form is **blinded**. Order is shuffled with a fixed seed, and no item shows
its source model, `n_models`, group id, or benchmark-corroboration flag. Those
live in `data/cq_stage5_key.csv`, which must never reach a rater - if it did,
the ratings would stop being independent evidence about convergence, which is
the one thing this instrument exists to test.

The form closes with five open slots. That section is not a courtesy: the list
was assembled from automatic sources, so what it omits is exactly what a
practitioner is positioned to notice.

### Analysing the returns

Record ratings in `data/cq_stage5_responses.csv`, laid out for three raters -
two is the minimum for an agreement coefficient, three makes a disagreement
interpretable. Both scales are ordinal, so use **quadratic-weighted Cohen's
kappa** for two raters or **Krippendorff's alpha (ordinal)** for three or more.
Plain unweighted kappa treats 4-vs-5 as badly as 1-vs-5 and will understate
agreement.

The convergence hypothesis is tested by joining ratings to the key afterwards:
does `n_models` predict mean relevance? Benchmark corroboration (Stage 4) is a
second, independent convergence signal - it can enter the same analysis. The key
also carries `level` and `dim`, so relevance can be broken down by reasoning
level and knowledge dimension.

## Reasoning level and knowledge dimension

The 23 CQs are classified on the same grid as the existing benchmark, so the two
sets can be reported side by side.

| | L1 | L2 | L3 | L4 | | D1 | D2 | D3 |
|---|---|---|---|---|---|---|---|---|
| Benchmark (25) | 7 | 6 | 5 | **7** | | **16** | 5 | 4 |
| Elicited (23) | 10 | 6 | 7 | **0** | | 9 | **12** | 2 |

**Nothing elicited lands in L4**, and that is a finding rather than a gap in the
classification. Entailment questions - does the defined class populate, does
inverse traversal work, is any individual typed both Symptom and Disease - are
an ontology engineer's concern. No agronomist poses them, so no domain-oriented
elicitation produces them.

This mirrors Stage 4 from the opposite direction. The benchmark is weighted to
the symbolic layer and to entailment: it tests the ontology. The elicited set is
weighted to cross-modal retrieval: it tests what a user would ask. Neither
covers the other, which is the argument for keeping both.

The assignment lives in the `GRID` table in `stage3_scope_and_group.py` and is
adjudicable like every other decision here. Two calls are genuinely arguable:
`CQ-A04` is L3 because differential diagnosis needs a self-join through symptoms
plus set operations, but L2 is defensible; and `CQ-A07` is D1 although its "on
which source authority" clause also exercises D3.

## Still outstanding

- **Second screener.** Stages 1, 3 and 4 rest on the ontology engineer's own
  judgement, on a first pass drafted by one of the source models. Have someone
  else screen ~20% independently and report agreement; it closes the most
  obvious objection to the whole procedure.
- **Tier B instrument.** Tier A rates the released resource; a separate
  instrument should prioritise the roadmap. The two must never merge - Tier B
  ratings must not enter the kappa that evaluates the resource.
- **Four SPARQL implementations.** `CQ-A04`, `CQ-A10`, `CQ-A16` and `CQ-A17`
  are answerable by v0.6 today and absent from the benchmark (Stage 4).
