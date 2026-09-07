# CQ Screening

How 173 competency questions elicited from five large language models were
filtered down to the 23 that go to expert validation, and how to reproduce that
filtering from the source files.

The deliverable is **[`reports/CQ_Final_TierA.md`](reports/CQ_Final_TierA.md)**.
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
| 4 - Reconciliation | *not yet done* | | |
| 5 - Questionnaire sampling | *not yet done* | | |

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
├── scripts/                          run in order; each is self-contained
│   ├── stage0_build_pool.py          parse the five model outputs
│   ├── stage1_screen.py              structural validity triage
│   ├── stage2_cluster.py             automatic clustering (superseded)
│   └── stage3_scope_and_group.py     scope gate, grouping, final CQ set
├── data/                             machine-readable, one row per CQ
│   ├── cq_pool_stage0.csv|.jsonl     the 173-CQ pool
│   ├── cq_stage1_adjudication.csv    flags + blank screener columns
│   ├── cq_stage2_*.csv               provisional clusters, borderline pairs
│   ├── worksheet_tierA.csv           the 64 Tier A CQs, blank for adjudication
│   ├── worksheet_tierA_proposal.csv  the same, with decisions and groups
│   └── CQ_Final_TierA.csv            the 23 canonical CQs
└── reports/                          human-readable, for the paper
    ├── cq_pool_stage0.md             pool provenance and distribution
    ├── cq_stage1_proposal.md         rules, counts, every flagged CQ
    ├── cq_stage2_proposal.md         method and its stated limitation
    ├── worksheet_tierA.md            readable worksheet
    ├── worksheet_tierA_proposal.md   per-group breakdown, dropped CQs
    └── CQ_Final_TierA.md             ← the deliverable
```

Source material lives in `../LLM Prompt/`: one shared prompt
(`rice_mmkg_cq_prompt.md`) and the five model outputs. Nothing in this directory
edits those.

## Reproducing

```bash
python scripts/stage0_build_pool.py
python scripts/stage1_screen.py
python scripts/stage2_cluster.py
python scripts/stage3_scope_and_group.py
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

Eight were proposed by a single model. **Keep them.** Stage 5 needs
low-convergence CQs in the questionnaire, or the hypothesis that convergence
predicts expert-rated relevance cannot be tested - and that hypothesis is the
methodological contribution.

**20 of the 56 retained CQs cannot yet be answered by v0.6.** That is not a
defect: competency questions are requirements, and an ontology that answers all
of its CQs on day one had its CQs written to fit what was already built. The
gaps are itemised at the end of `reports/CQ_Final_TierA.md` and constitute the
v0.7 work plan - `PlantPart` is missing, `confidenceScore` is declared but never
used, `SeverityLevel` exists but is not linked to any image.

## Before the questionnaire goes out

- **Stage 4** - reconcile against the 25 CQs already in
  `../CQ_SPARQL_Benchmark_Report.md`. Three outcomes matter: benchmark CQs
  corroborated by the models, benchmark CQs no model proposed, and new CQs the
  benchmark misses.
- **Instantiate the parameterised CQs.** 54 of the 173 are templates (*a given
  disease*, *N days*). An expert cannot judge agronomic correctness of *"a given
  disease"* - substitute a concrete one.
- **Blind the questionnaire** to source model and convergence count, or the
  convergence signal is contaminated by the very thing being tested.
- **Second screener.** Stages 1 and 3 rest on the ontology engineer's own
  judgement. Have someone else screen ~20% independently and report agreement;
  it closes the most obvious objection to the whole procedure.
- **Two instruments, never merged.** Tier A rates the released resource; Tier B
  prioritises the roadmap. Tier B ratings must not enter the kappa that
  evaluates the resource.
