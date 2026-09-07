# Stage 4 - Reconciliation with the existing benchmark

Generated 2026-09-07 21:41 by `scripts/stage4_reconcile.py`.

**23 elicited competency questions** (Stage 3) against **25 benchmark CQs** already implemented in `../cq_sparql_benchmark.py`.

> LLM-assisted first pass for human adjudication. `you_agree` and `your_correction` in the two CSVs are blank. Mapping was done by reading both sets; Stage 2 showed that string similarity conflates neighbouring requirements in this material.

## The headline: these are two different instruments

The sets do not compete. A benchmark CQ asks how completely a relation is populated; an elicited CQ asks what the graph answers for a concrete case. Compare:

| | Benchmark `CQ-01` | Elicited `CQ-A01` |
|---|---|---|
| Question | Which rice diseases have an identified causal pathogen? | Which pathogen causes a given rice disease? |
| Asks about | the graph | the domain |
| Answer | a completeness ratio | a pathogen |

Both probe `causedBy`. Neither substitutes for the other, and a benchmark CQ with no elicited counterpart is not automatically a defect.

## How the 25 benchmark CQs relate to the elicited set

| Relationship | Count | Meaning |
|---|---|---|
| `coverage-form` | 8 | measures how completely the relation behind an elicited CQ is populated |
| `chain` | 4 | traverses several relations, spanning more than one elicited CQ |
| `integrity` | 9 | graph hygiene; no domain-level counterpart is expected |
| `entailment` | 3 | description-logic check; likewise no counterpart |
| `out-of-scope` | 1 | concerns a modality held back as Tier B |

**15 of 25** benchmark CQs are corroborated by at least one independently elicited CQ. The remainder are, with one exception, checks no domain expert would pose - which is the correct division of labour, not a shortfall.

### The one exception

`CQ-20` (*How many sensor observations does the KG contain?*) counts a modality the resource does not populate. Under the text+image scope decision it belongs to Tier B and should be reframed or retired rather than reported as a passing benchmark item.

## Detail

| Benchmark | Mode | Maps to | Relationship | Note |
|---|---|---|---|---|
| `CQ-01` | coverage | CQ-A01 | `coverage-form` | how completely causedBy is populated |
| `CQ-02` | coverage | CQ-A03 | `coverage-form` | how completely indicatedBy is populated |
| `CQ-03` | coverage | CQ-A07 | `coverage-form` | how completely controlledBy is populated |
| `CQ-04` | coverage | CQ-A03 | `coverage-form` | same relation, read from the symptom side |
| `CQ-05` | coverage | CQ-A05 CQ-A06 | `chain` | occursIn joined with increaseRiskOf |
| `CQ-06` | coverage | CQ-A06 | `coverage-form` | growth-stage vulnerability profile |
| `CQ-07` | negative | - | `integrity` | cross-checks vulnerableTo against occursIn |
| `CQ-08` | coverage | CQ-A07 | `coverage-form` | narrows to preventive treatments with a stage prerequisite |
| `CQ-09` | coverage | CQ-A02 | `chain` | vector -> pathogen -> disease traversal |
| `CQ-10` | negative | CQ-A02 CQ-A07 | `integrity` | finds vectors with no recorded treatment |
| `CQ-11` | coverage | CQ-A03 CQ-A05 CQ-A07 | `chain` | environmental factor -> disease -> symptom -> treatment |
| `CQ-12` | coverage | CQ-A07 | `coverage-form` | reach of the management layer |
| `CQ-13` | coverage | - | `integrity` | every severity level maps to a management action |
| `CQ-14` | entailment | CQ-A15 | `entailment` | membership of the defined class SymptomaticObservation |
| `CQ-15` | entailment | - | `entailment` | inverse-direction traversal works |
| `CQ-16` | coverage | CQ-A22 CQ-A23 | `chain` | image -> annotated class -> symptom and treatment |
| `CQ-17` | coverage | - | `integrity` | annotated classes are typed as domain entities |
| `CQ-18` | coverage | CQ-A21 | `coverage-form` | which symptoms have image support - the closest direct match between the two sets |
| `CQ-19` | negative | CQ-A11 | `integrity` | images missing a content URL or provenance link |
| `CQ-20` | documented | - | `out-of-scope` | counts sensor observations; Tier B under the text+image scope decision |
| `CQ-21` | coverage | - | `integrity` | reified assertions carrying source and citation |
| `CQ-22` | negative | - | `integrity` | reified axioms with incomplete provenance |
| `CQ-23` | coverage | - | `integrity` | alignment to external vocabularies |
| `CQ-24` | negative | - | `integrity` | evidenceType literals uniformly language-tagged |
| `CQ-25` | negative | - | `entailment` | no individual typed both Symptom and Disease |

---

## What the benchmark does not reach: 12 of 23 elicited CQs

This is the actionable finding. The benchmark reaches the symbolic layer thoroughly and the image layer barely: **9 of the 12 unreached CQs are image or cross-modal**. Users ask about images; the current benchmark mostly asks whether images are linked at all.

| ID | Category | n_models | Status vs v0.6 | Question |
|---|---|---|---|---|
| `CQ-A04` | text | 4 | answerable | Which diseases or pests share overlapping symptoms, and which symptoms discriminate between them? |
| `CQ-A08` | text | 1 | needs new schema/data | Which natural enemies are documented as predators or parasitoids of a given pest? |
| `CQ-A09` | text | 1 | needs new schema/data | Which features distinguish a nutritional disorder from a disease with similar visible symptoms? |
| `CQ-A10` | image | 4 | answerable | Which images are annotated as showing a given condition or visual symptom? |
| `CQ-A12` | image | 1 | needs new schema/data | Where do model-generated and expert image annotations disagree, and on which conditions and plant parts? |
| `CQ-A13` | image | 2 | answerable | How is the image corpus distributed across conditions, plant parts, and capture types? |
| `CQ-A14` | image | 3 | needs new schema/data | Which plant organ is depicted in a given image? |
| `CQ-A16` | image | 3 | answerable | Which disease or pest is best supported by the visual evidence in a given image? |
| `CQ-A17` | image | 4 | answerable | Which visual features separate two visually confusable conditions? |
| `CQ-A18` | image | 2 | needs new schema/data | How severe is the damage recorded in a given image? |
| `CQ-A19` | image | 1 | needs new schema/data | Which symptoms co-occur on the same plant within a single image? |
| `CQ-A20` | image | 1 | needs new schema/data | Which growth stage is visually manifest in a whole-canopy image? |

### Priority additions

Elicited by three or more models independently, and answerable by v0.6 as it stands - so they can be implemented as SPARQL now, without waiting for schema work:

- **`CQ-A04`** (4 models) - Which diseases or pests share overlapping symptoms, and which symptoms discriminate between them?
- **`CQ-A10`** (4 models) - Which images are annotated as showing a given condition or visual symptom?
- **`CQ-A16`** (3 models) - Which disease or pest is best supported by the visual evidence in a given image?
- **`CQ-A17`** (4 models) - Which visual features separate two visually confusable conditions?

`CQ-A04` deserves particular attention: differential diagnosis - which diseases share symptoms and what discriminates them - was proposed by four of five models and is the question a field diagnostician actually asks, yet the benchmark has no equivalent.

## Consequences for Stage 5

- The questionnaire should carry the **elicited** phrasing, not the coverage phrasing. An agronomist can judge whether *which pathogen causes blast* is a sensible question; they cannot judge whether *72% of diseases have a causal pathogen* is a sensible threshold.
- Corroboration by the benchmark is a second convergence signal, independent of the five models. Record it alongside `n_models`, and keep it out of the questionnaire itself for the same reason - it would contaminate what the ratings are meant to test.
