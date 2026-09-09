# CQ Screening

How 213 competency questions elicited from six large language models were
filtered down to the 25 that go to expert validation, and how to reproduce that
filtering from the source files.

The deliverable is `reports/cq_stage3_final_tierA.md`.
Everything else in this directory exists to show how it was arrived at.

---

## The funnel

| Stage | What it decides | In | Out |
|---|---|---|---|
| 0 - Pool | nothing; verbatim extraction | 6 model outputs | **213** |
| 1 - Structural validity | is this a competency question at all? | 213 | 213, of which **9 flagged** |
| 2 - Deduplication | which CQs restate one requirement? | 213 | 182 provisional clusters *(superseded, see below)* |
| 3 - Scope gate | does it need a modality we do not have? | 213 | **80** Tier A, 133 Tier B |
| 3 - Adjudication | keep or drop, and grouping | 80 | **70** keep, 10 drop |
| 3 - Grouping | one canonical CQ per requirement | 70 | **25** |
| 4 - Reconciliation | how do these relate to the 25 benchmark CQs? | 25 vs 25 | 15 corroborated, **14 gaps** |
| 5 - Questionnaire | instantiate, blind, randomise | 25 | **25 items**, all included |
| 6 - Analysis | agreement, and does convergence predict relevance? | ratings | *awaiting returns* |

Stage 2's automatic clustering **did not survive**. Two independent similarity
signals were tried (TF-IDF cosine over question text, Jaccard over the
class/property signature) at many thresholds, and both conflate requirements
that are genuinely distinct: at every cut tried, *what pathogen causes blast*
clustered with *what symptoms are reported for blast*. Its output is kept for
the record, but the grouping that produced the final set was done by reading
every Tier A CQ. Stage 2's `n_models` figures are a lower bound and should not
be quoted.

## Three things to state in writing

**The elicitation was done in two rounds.** Five models were prompted first
(pool of 173, adjudicated 2026-09-03). A sixth, GPT-6 Astra, was prompted later
with the *same* prompt file and folded into one pool on 2026-09-08, bringing it
to 213. Merging two rounds into a single pool is defensible because the prompt
did not change, but it must be reported as what it is: the six outputs were not
collected simultaneously, and the sixth model's 40 CQs were adjudicated after
the grouping vocabulary (G01-G23) already existed, which makes it easier for its
CQs to land in an existing group than to found a new one. Two did found new
groups (`G24`, `G25`).

**The scope decision.** Only text and image are claimed. RiceMMKG v0.6 holds
10,407 `ImageObservation` individuals, **zero** `SensorObservation` individuals,
and no variety, gene, document or region entities. The elicitation prompt
declared a four-modality KG as context to assume, so all six models wrote CQs
for a KG that does not exist yet: 82 of the 213 need sensor data, 77 need
genomic, 26 need both. Those become Tier B - a requirements-based justification
for the roadmap, not a claim about this release.

Quote all four numbers together, because they have to reconcile: 82 + 77 - 26 =
133 = 213 - 80. An earlier version of this table gave 45 / 39 / 23 against a
Tier B of 109, which does not add up - those three were computed over the
question text alone while the gate also reads the entity list. Any restatement
of the split must be recomputed with the same predicate the gate uses.

**The conflict of interest.** The Stage 3 grouping was drafted by Claude Opus 5,
which is *also one of the models whose output forms the pool*. A model graded
its own work. It was reviewed and approved by M. A. Furqon on 2026-09-03, and
the sixth model's CQs on 2026-09-08. Describe it as an LLM-assisted first pass,
human-adjudicated - never as an automatic result.

## Reproducing

```bash
python scripts/stage0_build_pool.py
python scripts/stage1_screen.py
python scripts/stage2_cluster.py
python scripts/stage3_scope_and_group.py
python scripts/stage4_reconcile.py
python scripts/stage5_questionnaire.py
python scripts/stage6_analyse_responses.py   # only once the forms come back
python scripts/make_deck.py
python scripts/make_benchmark_deck.py
```

The two deck scripts read every count from `data/` and from the benchmark
result JSONs, so the slides cannot drift from what was actually run:
`make_deck.py` covers the screening funnel, `make_benchmark_deck.py` the
elicited-CQ SPARQL results. Both need `python-pptx`, which the six pipeline
stages do not; the second also needs `../elicited_cq_sparql.py` to have been
run first. Slides identify a CQ by source model and that model's own id, never
by `pool_id`, for the reason given below.

Requires Python 3 and numpy; no other dependencies, deliberately, so the
similarity method can be described exactly in a paper rather than deferred to a
library version. Scripts are idempotent and overwrite their own outputs.

Human decisions are not recomputed - they are recorded as the `LABELS` table in
`stage3_scope_and_group.py`, keyed by **`(source_model, original_id)`**: the
model that wrote the CQ and the identifier that model gave it.

That key was originally `pool_id`, and it was wrong. `pool_id` is assigned after
sorting the whole pool, so adding a model renumbers everything alphabetically
after it. Inserting GPT-6 Astra moved 23 of the 64 existing labels onto
*different questions* while every id remained valid, which the sync assertion
could not see. The `(model, id)` pair cannot move. Re-keying was verified by
re-running the five-model pool and confirming byte-identical output; the first
six-model run then reported 0 stale labels and 17 unlabelled ones - exactly the
17 new CQs that survived the scope gate.

## What the 25 CQs look like

Five were proposed independently by five of the six models, and are effectively
the core of the ontology: pathogen causing a disease (`CQ-A01`), vector
transmission (`CQ-A02`), overlapping symptoms and what discriminates them
(`CQ-A04`), recommended control measures (`CQ-A07`), and retrieving images by
condition (`CQ-A10`).

Ten were proposed by a single model. **Keep them.** Stage 5 needs
low-convergence CQs in the questionnaire, or the hypothesis that convergence
predicts expert-rated relevance cannot be tested - and that hypothesis is the
methodological contribution.

**32 of the 70 retained CQs cannot yet be answered by v0.6**, and 10 of the 25
canonical CQs have no answerable member at all. That is not a defect: competency
questions are requirements, and an ontology that answers all of its CQs on day
one had its CQs written to fit what was already built. The gaps are itemised at
the end of `reports/cq_stage3_final_tierA.md` and constitute the v0.7 work plan -
`PlantPart` is missing, `confidenceScore` is declared but never used,
`SeverityLevel` exists but is not linked to any image, and region-level image
annotation does not exist at all.

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

The actionable half is the other direction: **14 of the 25 elicited CQs have no
benchmark counterpart, and 11 of those 14 are image or cross-modal**. The
benchmark covers the symbolic layer thoroughly and the image layer barely.
Five are already answerable by v0.6 and could be implemented as SPARQL now:
`CQ-A04` (differential diagnosis), `CQ-A10`, `CQ-A13`, `CQ-A16`, `CQ-A17`.
`CQ-A04` is the most striking - five of six models proposed it, it is the
question a field diagnostician actually asks, and the benchmark has no
equivalent.

Detail in `reports/cq_stage4_reconciliation.md`.

## Stage 5: the questionnaire

`reports/cq_stage5_questionnaire.md` is ready to hand to experts. All 25 CQs are
included - the planned size was 30-50 items, so nothing had to be sampled away,
and the full convergence spread survives (ten single-model CQs alongside five
proposed by five of the six models).

Every item is **instantiated** with an entity that exists in v0.6: not *"which
pathogen causes a given disease"* but *"which pathogen causes rice blast"*. An
expert cannot judge the former.

The introduction states plainly that the project is at the formalisation stage,
that no system exists yet, and that the expert is asked to rate the *questions*,
not to answer them. Anything else would misdescribe what is being evaluated.

The form is **blinded**. Order is shuffled with a fixed seed, and no item shows
its source model, `n_models`, group id, or benchmark-corroboration flag. Those
live in `data/cq_stage5_key.csv`, which must never reach a rater - if it did,
the ratings would stop being independent evidence about convergence, which is
the one thing this instrument exists to test.

That file was tracked in git until 2026-09-09, and this repository is public,
so it is **still readable in the history** even though it no longer appears in
the tree. Removing it from the tip stops a rater stumbling over it; it does not
undo publication. If a rater is given the repository URL before answering,
either rewrite the history for those three commits or treat the blinding as
compromised and say so - do not quietly assume nobody looked.

The form closes with five open slots. That section is not a courtesy: the list
was assembled from automatic sources, so what it omits is exactly what a
practitioner is positioned to notice.

### Distributing it through Google Forms

`reports/cq_stage5_google_form.js` is an Apps Script generated from the same
item table, so it cannot drift from the printable form. Open script.google.com,
paste it into a new project, run `createValidationForm()` once; the execution
log prints the form URL. Item numbers match `cq_stage5_items.csv`, which is how
responses join back to the key.

Three settings matter. **Do not enable the built-in question shuffling** - the
order is already randomised once with a fixed seed and documented; reshuffling
per respondent discards that for little gain at this sample size. **Set
`COLLECT_EMAIL`** deliberately: agreement coefficients cannot be computed
without attributing ratings to raters, but that is a consent decision, so the
script leaves it off and asks for a name instead. And the sections of six items
exist for pacing only - they deliberately do **not** group by category, which
would expose the structure the blinding is meant to hide.

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

`scripts/stage6_analyse_responses.py` does all of that. It picks the
coefficient the design supports - weighted kappa at two raters, ordinal alpha
at three or more, the latter also tolerating the cells a real return will leave
blank - and reports Spearman's rho between `n_models` and mean relevance with a
permutation p-value. Both coefficients and both tests are computed from first
principles on numpy alone, like every other stage, so the method can be written
out rather than deferred to a library version; there is no scipy here, which is
why the p-values are permuted (20,000 draws, seed 20260907) rather than
approximated.

Run against the untouched template it exits with a message and writes nothing.
Outputs are `data/cq_stage6_item_scores.csv` (one row per CQ, ratings joined to
the key), `data/cq_stage6_agreement.csv` and `reports/cq_stage6_analysis.md`.

Two things it deliberately will not do: drop a rater, an item or a scale to
improve a coefficient, and admit Tier B ratings into the same analysis. A low
alpha is a result about the instrument, not a defect to tune away - and the
same applies to a CQ that rates poorly, which is a finding about the question,
not a licence to rewrite it.

## Reasoning level and knowledge dimension

The 25 CQs are classified on the same grid as the existing benchmark, so the two
sets can be reported side by side.

| | L1 | L2 | L3 | L4 | | D1 | D2 | D3 |
|---|---|---|---|---|---|---|---|---|
| Benchmark (25) | 7 | 6 | 5 | **7** | | **16** | 5 | 4 |
| Elicited (25) | 11 | 6 | 8 | **0** | | 9 | **13** | 3 |

**Nothing elicited lands in L4**, and that is a finding rather than a gap in the
classification. Entailment questions - does the defined class populate, does
inverse traversal work, is any individual typed both Symptom and Disease - are
an ontology engineer's concern. No agronomist poses them, so no domain-oriented
elicitation produces them. Adding a sixth model did not change this: 40 further
CQs from a model that was never asked for entailment produced none.

This mirrors Stage 4 from the opposite direction. The benchmark is weighted to
the symbolic layer and to entailment: it tests the ontology. The elicited set is
weighted to cross-modal retrieval: it tests what a user would ask. Neither
covers the other, which is the argument for keeping both.

The assignment lives in the `GRID` table in `stage3_scope_and_group.py` and is
adjudicable like every other decision here. Two calls are genuinely arguable:
`CQ-A04` is L3 because differential diagnosis needs a self-join through symptoms
plus set operations, but L2 is defensible; and `CQ-A07` is D1 although its "on
which source authority" clause also exercises D3.

## The scope gate has two parts

A CQ is Tier B if its text matches the sensor or genomic keyword patterns, **or**
if the model that wrote it filed it under the sensor or genomic category. The
second test was added on 2026-09-08 and is retrospectively a no-op on the
five-model pool. It exists because GPT-6 Astra `CQ-GEN-02` asks about Xoo
inoculation assays of IRBB5 and IRBB21 - unmistakably a germplasm question,
written without a single term in the keyword list. Trusting the source model's
own filing catches what keywords miss. The keyword list also gained
`accession`, `isolate` and `inoculation`, which likewise catch nothing in the
original pool.

## Still outstanding

- **Second screener.** Stages 1, 3 and 4 rest on the ontology engineer's own
  judgement, on a first pass drafted by one of the source models. Have someone
  else screen ~20% independently and report agreement; it closes the most
  obvious objection to the whole procedure.
- **Tier B instrument.** Tier A rates the released resource; a separate
  instrument should prioritise the roadmap. The two must never merge - Tier B
  ratings must not enter the kappa that evaluates the resource.
- ~~**Five SPARQL implementations.**~~ **Done 2026-09-08.** `CQ-A04`, `CQ-A10`,
  `CQ-A13`, `CQ-A16` and `CQ-A17` are implemented in
  `../elicited_cq_sparql.py`, reported in `../Elicited_CQ_SPARQL_Report.md`.
  All five return answers; `CQ-A13` and `CQ-A17` are recorded as *partial*
  because v0.6 carries no plant part, capture type or lesion descriptors. Kept
  separate from `cq_sparql_benchmark.py` on purpose: those are coverage
  questions scored against a threshold, these are retrieval questions that
  answer or do not. The run also surfaced a v0.7 priority the coverage
  benchmark could not: `captures` holds 1,442 assertions and **every one of
  them points at a single symptom**, so image-to-symptom grounding exists for
  one condition and no other.
- **The 50% coverage threshold** used in the SPARQL benchmark has no external
  source. State it as an author convention; do not cite it.
