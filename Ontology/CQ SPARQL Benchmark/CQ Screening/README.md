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
| 0a - Provenance | how was each output obtained, and is it unaltered? | 6 runs | 6 verified |
| 1 - Structural validity | is this a competency question at all? | 213 | 213, of which **9 flagged** |
| 2 - Deduplication | which CQs restate one requirement? | 213 | 182 provisional clusters *(superseded, see below)* |
| 3 - Scope gate | does it need a modality we do not have? | 213 | **80** Tier A, 133 Tier B |
| 3 - Adjudication | keep or drop, and grouping | 80 | **70** keep, 10 drop |
| 3 - Grouping | one canonical CQ per requirement | 70 | **25** |
| 4 - Reconciliation | how do these relate to the 25 benchmark CQs? | 25 vs 25 | 15 corroborated, **14 gaps** |
| 5 - Questionnaire | instantiate, blind, randomise | 25 | **25 items**, all included |
| 6 - Analysis | agreement, and does convergence predict relevance? | ratings | *awaiting returns* |
| 7 - Stability | how often does a repeated run of the prompt return each CQ? | 25 x 20 runs | **2 always, 2 never** |

## Execution order

**A stage number is a permanent label, not a position.** They are not
consecutive already — `0a` is a side check, `2` is superseded and retained only
for the record, and `3` covers three decisions — and they are referenced by
every filename in `data/` and `reports/`, by both decks, and by notes outside
this repository. Renumbering them would silently change what an existing
reference means, which is the failure this project already had once when
`pool_id` was renumbered by the arrival of a sixth model and moved 23 labels
onto different questions while every id stayed valid. Read the numbers as names
and take the running order from here.

### Presentations name the steps; they do not number them

A slide funnel and this pipeline number different things. This pipeline numbers
**scripts**: one script is one stage, which is why Stage 3 performs three
decisions and why Stage 2 exists at all — it ran, it failed, and the failure is
part of the record. A slide funnel numbers **count reductions**: every box has
to lower a number, 213 to 80 to 70 to 25.

Neither can adopt the other. Renumbering this pipeline to match a slide would
mean deleting Stage 1 (which removes nothing) and Stage 2 (which failed) from
the record, and Stage 2's failure is one of the stronger parts of the
methodology — automatic clustering was tried, it conflated distinct
requirements at every threshold, and the evidence is kept. Renumbering the
slide to match this pipeline would put a 213 -> 213 box and a "superseded" box
in a funnel graphic.

So slides and papers refer to the steps **by name and never by number** — Pool,
Scope gate, Adjudication, Grouping, Reconciliation. The arrows and counts
already carry the order. A number on a slide adds nothing except a second
scheme that competes with this one, and on 2026-09-10 a progress deck did
exactly that: its Stage 1 was the scope gate, its Stage 3 the grouping.

### What depends on what

```
        [six LLM outputs]                 [expert returns]     [20 replication runs]
               |                                  |                      |
   0 Pool -- 0a Provenance                        |                      |
               |                                  |                      |
        1 Structural validity                     |                      |
               |                                  |                      |
        (2 Deduplication - superseded)            |                      |
               |                                  |                      |
        3 Scope gate + adjudication + grouping    |                      |
               |            |                     |                      |
      4 Reconciliation   5 Questionnaire          |                      |
                            |                     |                      |
                            +-------------------- 6 Analysis <---- 7 Stability
```

Stages 0-5 are a chain: each consumes the previous one's output, and all of
them are **done**. Everything remaining hangs off two inputs that do not exist
yet, and those two are independent of each other:

- **Stage 6** needs the questionnaire back from the experts. It reads only
  `cq_stage5_key.csv`, `cq_stage5_items.csv` and `cq_stage5_responses.csv`.
- **Stage 7** needed 20 new LLM runs and has them. It reads only Stage 3's
  canonical set and those runs, and did **not** wait for the experts.

### The running order

1. **Send the questionnaire out.** Stage 5 is ready
   (`reports/cq_stage5_questionnaire.md`, or the Google Form built from the
   same table). Nothing downstream can start until the experts have it, so it
   goes first and then runs in the background for weeks.
2. ~~**Run Stage 7 while waiting.**~~ **Done 2026-09-10** — 20 runs, a 500-row
   checklist derived from 266 per-CQ labels, reported in
   `reports/cq_stage7_stability.md`. The labels are an LLM first pass and still
   need human adjudication before any rate is quoted.
3. **Wire the Stage 7 rate into Stage 6** *before* any returns are analysed.
   Stage 6 currently tests `n_models` — a 0-to-6 count, granular to the point
   of bluntness — against expert relevance. The re-proposal rate over 20 runs
   measures the same construct far more finely, and belongs in that analysis
   alongside `n_models` and the benchmark-corroboration flag. Choosing
   predictors after seeing the ratings is choosing them from the answer.
4. **Run Stage 6 once the returns are in.** One pass, three convergence signals
   against the same ratings.

Steps 2 and 3 must both finish before step 4, which is the whole reason Stage 7
is worth starting now rather than after. Run it afterwards and Stage 6 has to
be redone.

The cost of this order is knowing which CQs are unstable before seeing the
ratings. That is a temptation, not a contamination — the raters never see any
of this — but it is a real one. Do not revise the set on it; see *How to read
this* in the Stage 7 report for why that would make the Stage 6 hypothesis
unfalsifiable.

### If a second screener becomes available

The outstanding second-screener work (below) attaches to Stages 1, 3 and 4,
which are already done, and to the Stage 7 checklist, which is not. A screener
who is available now is better spent auditing a sample of the Stage 7 checklist
as it is filled than re-screening Stage 1 afterwards, because Stage 7's rates
are a fresh single-adjudicator judgement and Stage 1's have at least been
stable for months.

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

## What "reproducible" means for an LLM elicitation

Two different things, and the paper has to separate them.

**The screening reproduces exactly.** Everything downstream of the six model
outputs is deterministic Python over files in this repository. Re-running it
returns every number byte for byte, and the human decisions inside it are
recorded as tables rather than recomputed, so a reader can inspect and disagree
with each one.

**The elicitation does not, and cannot.** Commercial chat models are sampled,
are updated without notice, and the interfaces used here expose no temperature
or seed. Sending the same prompt tomorrow returns a different set of CQs. This
is a property of the instrument; documentation does not remove it.

What is defensible is to freeze the prompt, record the runs, and then *measure*
the instability rather than leave it to the reader's imagination.

- **The prompt is frozen and hashed.** `LLM Prompt/rice_mmkg_cq_prompt.payload.txt`
  is the exact text that was pasted into each interface — the fenced block, not
  the whole markdown file, since the surrounding prose is operator guidance that
  was never sent. Its SHA-256 is `0e3207a1...`, computed over LF-normalised
  bytes so it does not depend on which machine did the checkout.
- **The two sittings provably used the same bytes.** The prompt file was
  committed once, in `97d2986` on 2026-09-03, and never modified, so GPT-6 Astra
  on 2026-09-08 received what the first five models received. `git rev-parse`
  on both commits returns the same blob. That is evidence, not an assertion.
- **The placeholders were deliberately left unfilled.** The prompt's closing
  instruction tells the model to proceed with the stated defaults and mark its
  own assumptions, which is why the Fable and Astra outputs carry "Assumptions"
  sections. Filling them in now would be a *different* protocol whose runs would
  not replicate this pool.
- **Each run is recorded.** `LLM Prompt/runs/run_manifest.csv`, verified by
  `stage0a_provenance.py`, which exits non-zero if any output file has been
  edited since its digest was taken.

**Three facts about the original runs were never captured and cannot be
recovered:** the exact date each prompt was sent, the model version string the
interface displayed, and which interface features (web search, memory, custom
instructions) were active. Those cells read `not-recorded` and must stay that
way — reconstructing them from commit dates would turn an upper bound into a
fabricated observation. State the limitation in the paper; a reviewer who spots
it first will trust everything else less.

The full procedure, including how to run round 2, is
`LLM Prompt/ELICITATION_PROTOCOL.md`.

## Reproducing

Re-deriving everything that is already done, in dependency order:

```bash
python scripts/stage0_build_pool.py
python scripts/stage0a_provenance.py         # verifies the run manifest
python scripts/stage1_screen.py
python scripts/stage2_cluster.py             # superseded; kept for the record
python scripts/stage3_scope_and_group.py
python scripts/stage4_reconcile.py
python scripts/stage5_questionnaire.py
python scripts/make_deck.py
python scripts/make_benchmark_deck.py
```

The two stages that are not done yet wait on inputs that do not exist. Both
exit with a message and write nothing if run early, so running them costs
nothing but tells you nothing either. **Stage 7 before Stage 6** — see
*Execution order* above:

```bash
python scripts/stage7_stability.py --checklist   # once the 30 runs are saved
python scripts/stage7_stability.py               # once the checklist is filled
python scripts/stage6_analyse_responses.py       # once the forms come back
```

The two deck scripts read every count from `data/` and from the benchmark
result JSONs, so the slides cannot drift from what was actually run:
`make_deck.py` covers the screening funnel, `make_benchmark_deck.py` the
elicited-CQ SPARQL results. Both need `python-pptx`, which no pipeline stage
does; the second also needs `../elicited_cq_sparql.py` to have been
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

### `v06_status` is a prediction, not a measurement

The `v06_status` column in `cq_stage3_final_tierA.csv` was assigned during
Stage 3 grouping, **before any SPARQL had been written**. It records what the
adjudicator expected v0.6 to answer. It is not evidence that v0.6 answers
anything.

The measurement is `../elicited_cq_sparql_results.json`, and the two disagree
on **8 of the 15 CQs that have since been implemented** — always in the same
direction: Stage 3 predicted `answerable`, the query came back `partial`. That
direction is not a coincidence. Reading a schema and judging that it *could*
answer a question is systematically more optimistic than writing the query and
finding out.

**Anything that reports answerability must read the JSON, not this column** —
a slide deck built off `v06_status` on 2026-09-10 presented all 15 as
answerable. The column is kept because Stage 3's reasoning is part of the
record, not because it is current.

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
Five *looked* answerable by v0.6 and were implemented as SPARQL first:
`CQ-A04` (differential diagnosis), `CQ-A10`, `CQ-A13`, `CQ-A16`, `CQ-A17` — of
which `CQ-A13` and `CQ-A17` turned out to answer only in part once the query
was actually written. See the warning below about `v06_status`.
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

### A prediction recorded before the first expert rated anything

Stage 7 found nine requirements that twenty replication runs raised and the
canonical 25 do not cover. Two were raised by five runs each:

- **`NEW-02`** — which agronomic practices (nitrogen over-fertilisation, dense
  planting) are reported to aggravate a disease, and by what cited mechanism.
- **`NEW-03`** — which weeds or volunteer plants act as off-season reservoirs
  for a pathogen or pest.

The questionnaire closes by asking the expert which questions are missing. If a
practitioner independently names either of these, that is convergent evidence
from a source with nothing in common with the elicitation — the models had only
the prompt, the expert has only field practice.

**This is written down on 2026-09-10, before any expert has seen the form**, so
that it is a prediction rather than something noticed afterwards in the
returns. Two conditions make it worth anything:

- **Do not prompt the expert with these.** Naming them in the meeting, or
  adding them to the form, destroys exactly the independence that would make a
  match informative. The open box stays open.
- **A miss is also a result.** If no expert raises them, the honest reading is
  that five runs of a language model agreed on something practitioners do not
  prioritise — which is a finding about the elicitation instrument, and belongs
  in the paper next to the hits.

The remaining seven (`NEW-01`, `NEW-04` to `NEW-09`) were raised by one or two
runs each and are recorded in `data/cq_stage7_new_requirements.csv`; they are
too thin to predict from, but check them against the returns too.

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

### A third failure mode, found in Stage 7

The gate misses a CQ that asks about *measured* environmental conditions
without using any gated term. Six of the 704 replication CQs read like *"which
plots currently satisfy the literature-reported favourable conditions for
sheath blight"* or *"how many days did each plot fall inside the favourable
envelope"* — they need environmental time series, and they reached Tier A
because they say "environmental conditions" and "conducive window" rather than
temperature, humidity or sensor.

**Round 1 is not affected, and this was checked rather than assumed.** Exactly
one round-1 Tier A CQ matches that phrasing — GPT-5.6 Sol `CQ-TXT-05`, *"which
environmental conditions are reported to favor outbreaks..."* — and it is
correctly Tier A: it asks what the literature reports, not what a sensor
measured, which is canonical group `G05`. So the 82 / 77 / 26 / 133 / 80 split
stands as published.

The distinction the gate cannot see is **reported versus measured**: the same
noun phrase is Tier A when a document is the source and Tier B when a sensor
is. Tightening the regex is not obviously the fix, since "environmental
condition" alone would wrongly pull `G05` into Tier B. What did catch all six
was the adjudication step reading them — which is the argument for keeping the
gate as a coarse filter with a human pass behind it, rather than treating it as
the decision.

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

- **The replication runs.** `stage7_stability.py` is written and tested but has
  nothing to read: the prompt has not been sent again. Until it is, the 25 CQs
  rest on a single sample and the paper can say only that the prompt is frozen,
  not how stable the set is. The design is fixed at **five runs of each of the
  six models, 30 runs**, and it is fixed *before* any output is seen — choosing
  the number of runs after seeing how the first ones went turns a stability
  estimate into a selected one. Procedure in
  `LLM Prompt/ELICITATION_PROTOCOL.md`.

  Five per model is what buys the decomposition. One replication round
  conflates two sources of variation; a run x model matrix separates them, and
  Stage 7 tests the difference between within-model and between-model Jaccard
  by permuting the model label across runs. If the two are indistinguishable,
  then model identity carries no information and `n_models` is closer to a run
  count than to a cross-model agreement measure — which would not invalidate
  the canonical set, but would change what convergence across models can be
  claimed to show.

  Round 1 is **not** one of the five. The grouping vocabulary G01-G25 was
  derived from the round-1 outputs, so round 1 re-proposes 100% of it by
  construction; it is carried in the manifest as `replicate` 0 and excluded
  from every rate.

  Budget the adjudication honestly: 30 runs produce roughly a thousand CQs, and
  the checklist is 750 run x group decisions. It is filled one run at a time,
  and every `yes` must name the CQ that supports it or the script rejects it.

  This does not wait for the expert returns, and is best done while waiting.
- **Stability rate as a Stage 6 predictor.** Once Stage 7 has run, its per-CQ
  re-proposal rate should enter the Stage 6 analysis alongside `n_models` and
  the benchmark-corroboration flag — three convergence signals against the same
  expert ratings. `stage6_analyse_responses.py` does not read it yet; wiring it
  in is a small change, but it has to happen before the returns are analysed,
  not after.
- **Second screener.** Stages 1, 3 and 4 rest on the ontology engineer's own
  judgement, on a first pass drafted by one of the source models. Have someone
  else screen ~20% independently and report agreement; it closes the most
  obvious objection to the whole procedure.
- **Tier B instrument.** Tier A rates the released resource; a separate
  instrument should prioritise the roadmap. The two must never merge - Tier B
  ratings must not enter the kappa that evaluates the resource.
- ~~**Five SPARQL implementations.**~~ **Done 2026-09-08, and since extended to
  15.** `../elicited_cq_sparql.py` implements 15 of the 25 elicited CQs and
  reports them in `../Elicited_CQ_SPARQL_Report.md`. **7 answer in full and 8
  answer in part** - `CQ-A01`, `A02`, `A03`, `A06`, `A07`, `A13` and `A17` are
  *partial - schema* (the ontology has no concept for what is asked, so no
  amount of data would answer it), and `CQ-A15` is *partial - data* (the
  concept exists, few individuals carry it). A partial is not a pass and is
  never counted as one. Kept
  separate from `cq_sparql_benchmark.py` on purpose: those are coverage
  questions scored against a threshold, these are retrieval questions that
  answer or do not. The run also surfaced a v0.7 priority the coverage
  benchmark could not: `captures` holds 1,442 assertions and **every one of
  them points at a single symptom**, so image-to-symptom grounding exists for
  one condition and no other.
- **The 50% coverage threshold** used in the SPARQL benchmark has no external
  source. State it as an author convention; do not cite it.
