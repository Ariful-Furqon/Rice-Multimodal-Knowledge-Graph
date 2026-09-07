# Rice MMKG - Final Competency Question Set (Tier A)

Generated 2026-09-07 20:45 by `scripts/stage3_scope_and_group.py`.

**23 canonical competency questions**, distilled from 173 candidates elicited independently from five large language models against one shared prompt.

Scope is text + image: the modalities the released resource actually carries. CQs requiring sensor or genomic data are held as Tier B, a requirements-based roadmap rather than a claim about this release.

## Provenance

| Step | In | Out |
|---|---|---|
| Stage 0 - pool from 5 models | - | 173 |
| Stage 1 - structural validity | 173 | 173 (8 flagged) |
| Stage 3 - scope gate (text + image) | 173 | 64 |
| Stage 3 - adjudication | 64 | 56 (dropped 8) |
| Stage 3 - grouping | 56 | **23** |

Grouping was an LLM-assisted first pass reviewed and approved by M. A. Furqon on 2026-09-03. One of the five source models drafted it, so it is not an independent judgement.

## The competency questions

`n_models` counts how many of the five models proposed the question independently. It is a convergence signal, not a quality score; Stage 5 deliberately retains low-convergence CQs so that the hypothesis *convergence predicts expert-rated relevance* remains testable.

| ID | Level | Dim | n_models | Status vs v0.6 | Competency question |
|---|---|---|---|---|---|
| `CQ-A01` | L1 | D1 | 4 | answerable | Which pathogen causes a given rice disease, and to which taxonomic group does it belong? |
| `CQ-A02` | L3 | D1 | 4 | answerable | Which vector species transmits which pathogen or viral disease, and by which transmission mode? |
| `CQ-A03` | L2 | D1 | 2 | answerable | Which symptoms does a given disease produce, on which plant organ, and at which growth stage? |
| `CQ-A04` | L3 | D1 | 4 | answerable | Which diseases or pests share overlapping symptoms, and which symptoms discriminate between them? |
| `CQ-A05` | L1 | D1 | 1 | answerable | Which environmental conditions are reported to favour a given disease or pest? |
| `CQ-A06` | L1 | D1 | 1 | answerable | At which growth stages is a given disease or pest reported as most damaging? |
| `CQ-A07` | L2 | D1 | 4 | answerable | Which control measures are recommended for a given disease or pest, of which management category, and on which source authority? |
| `CQ-A08` | L1 | D1 | 1 | needs new schema/data | Which natural enemies are documented as predators or parasitoids of a given pest? |
| `CQ-A09` | L3 | D1 | 1 | needs new schema/data | Which features distinguish a nutritional disorder from a disease with similar visible symptoms? |
| `CQ-A10` | L1 | D2 | 4 | answerable | Which images are annotated as showing a given condition or visual symptom? |
| `CQ-A11` | L1 | D3 | 1 | needs new schema/data | Who or what produced a given image annotation, and with what confidence? |
| `CQ-A12` | L2 | D3 | 1 | needs new schema/data | Where do model-generated and expert image annotations disagree, and on which conditions and plant parts? |
| `CQ-A13` | L2 | D2 | 2 | answerable | How is the image corpus distributed across conditions, plant parts, and capture types? |
| `CQ-A14` | L1 | D2 | 3 | needs new schema/data | Which plant organ is depicted in a given image? |
| `CQ-A15` | L1 | D2 | 2 | answerable | Which visible symptoms are annotated in a given image? |
| `CQ-A16` | L3 | D2 | 3 | answerable | Which disease or pest is best supported by the visual evidence in a given image? |
| `CQ-A17` | L3 | D2 | 4 | answerable | Which visual features separate two visually confusable conditions? |
| `CQ-A18` | L1 | D2 | 2 | needs new schema/data | How severe is the damage recorded in a given image? |
| `CQ-A19` | L2 | D2 | 1 | needs new schema/data | Which symptoms co-occur on the same plant within a single image? |
| `CQ-A20` | L1 | D2 | 1 | needs new schema/data | Which growth stage is visually manifest in a whole-canopy image? |
| `CQ-A21` | L2 | D2 | 2 | answerable | Which literature-described symptoms have supporting image evidence, and which do not? |
| `CQ-A22` | L3 | D2 | 2 | answerable | Which literature-described disease matches the symptoms annotated in a given image? |
| `CQ-A23` | L3 | D2 | 1 | answerable | Which treatment does the literature prescribe for a condition identified from an image? |

### Distribution over the benchmark's grid

L1 factual (single-hop) · L2 contextual (multi-criteria join) · L3 causal (multi-hop, comparison, aggregation) · L4 inferential (entailment).  D1 agronomic/symbolic · D2 cross-modal · D3 provenance and alignment.

| | D1 | D2 | D3 | total |
|---|---|---|---|---|
| **L1** | 4 | 5 | 1 | 10 |
| **L2** | 2 | 3 | 1 | 6 |
| **L3** | 3 | 4 | 0 | 7 |
| **L4** | 0 | 0 | 0 | 0 |
| **total** | 9 | 12 | 2 | 23 |

**Nothing lands in L4.** That is a finding rather than an oversight: entailment questions are an ontology engineer's concern, and a domain-oriented elicitation does not produce them. It mirrors the Stage 4 result from the opposite direction - the benchmark's three L4 checks have no elicited counterpart, just as the elicited image questions have no benchmark counterpart.

For comparison, the 25 benchmark CQs sit at L1 7, L2 6, L3 5, L4 7 and D1 16, D2 5, D3 4 - weighted towards the symbolic layer and towards entailment, where this set is weighted towards cross-modal retrieval.


## Detail

### CQ-A01 - Pathogen causing a disease, and its taxonomy

> Which pathogen causes a given rice disease, and to which taxonomic group does it belong?

- **Category:** text
- **Convergence:** 4 of 5 models (Claude Fable 5.1; Claude Opus 5; GPT-5.6 Sol; Gemini Pro 3.1)
- **Source CQs:** 4 - `P031 P067 P169 P103`
- **Status against v0.6:** answerable

### CQ-A02 - Vector transmitting a pathogen or viral disease

> Which vector species transmits which pathogen or viral disease, and by which transmission mode?

- **Category:** text
- **Convergence:** 4 of 5 models (Claude Fable 5.1; Claude Opus 5; Gemini Flash 3.8; Gemini Pro 3.1)
- **Source CQs:** 4 - `P138 P170 P032 P070`
- **Status against v0.6:** answerable
- **Extensions required:** adds transmission mode - new property | also covers causation; overlaps G01

### CQ-A03 - Symptoms of a disease, by organ and growth stage

> Which symptoms does a given disease produce, on which plant organ, and at which growth stage?

- **Category:** text
- **Convergence:** 2 of 5 models (Claude Opus 5; GPT-5.6 Sol)
- **Source CQs:** 3 - `P104 P068 P106`
- **Status against v0.6:** answerable
- **Extensions required:** adds organ + growth stage

### CQ-A04 - Diseases sharing symptoms, and what discriminates them

> Which diseases or pests share overlapping symptoms, and which symptoms discriminate between them?

- **Category:** text
- **Convergence:** 4 of 5 models (Claude Fable 5.1; Claude Opus 5; GPT-5.6 Sol; Gemini Pro 3.1)
- **Source CQs:** 5 - `P108 P172 P105 P071 P035`
- **Status against v0.6:** answerable

### CQ-A05 - Environmental conditions favouring a disease or pest

> Which environmental conditions are reported to favour a given disease or pest?

- **Category:** text
- **Convergence:** 1 of 5 models (GPT-5.6 Sol)
- **Source CQs:** 1 - `P107`
- **Status against v0.6:** answerable

### CQ-A06 - Growth stage at which a pest or disease is most damaging

> At which growth stages is a given disease or pest reported as most damaging?

- **Category:** text
- **Convergence:** 1 of 5 models (Claude Fable 5.1)
- **Source CQs:** 1 - `P033`
- **Status against v0.6:** answerable

### CQ-A07 - Recommended control measures, by category and source

> Which control measures are recommended for a given disease or pest, of which management category, and on which source authority?

- **Category:** text
- **Convergence:** 4 of 5 models (Claude Fable 5.1; Claude Opus 5; Gemini Flash 3.8; Gemini Pro 3.1)
- **Source CQs:** 4 - `P139 P034 P171 P069`
- **Status against v0.6:** answerable
- **Extensions required:** adds growth stage | adds source document

### CQ-A08 - Natural enemies of a pest

> Which natural enemies are documented as predators or parasitoids of a given pest?

- **Category:** text
- **Convergence:** 1 of 5 models (Gemini Flash 3.8)
- **Source CQs:** 1 - `P141`
- **Status against v0.6:** needs new schema/data
- **Extensions required:** needs NaturalEnemy class - not in v0.6

### CQ-A09 - Distinguishing a nutritional disorder from a disease

> Which features distinguish a nutritional disorder from a disease with similar visible symptoms?

- **Category:** text
- **Convergence:** 1 of 5 models (Gemini Flash 3.8)
- **Source CQs:** 1 - `P142`
- **Status against v0.6:** needs new schema/data
- **Extensions required:** needs nutritional disorder (zinc deficiency) - not in v0.6

### CQ-A10 - Images showing a given condition or symptom

> Which images are annotated as showing a given condition or visual symptom?

- **Category:** image
- **Convergence:** 4 of 5 models (Claude Fable 5.1; Claude Opus 5; GPT-5.6 Sol; Gemini Pro 3.1)
- **Source CQs:** 4 - `P011 P083 P047 P150`
- **Status against v0.6:** answerable
- **Extensions required:** also asks annotation source, see G11

### CQ-A11 - Provenance and confidence of an image annotation

> Who or what produced a given image annotation, and with what confidence?

- **Category:** image
- **Convergence:** 1 of 5 models (Claude Opus 5)
- **Source CQs:** 1 - `P050`
- **Status against v0.6:** needs new schema/data
- **Extensions required:** needs annotator + confidence - confidenceScore unused in v0.6

### CQ-A12 - Disagreement between model and expert annotations

> Where do model-generated and expert image annotations disagree, and on which conditions and plant parts?

- **Category:** image
- **Convergence:** 1 of 5 models (Claude Fable 5.1)
- **Source CQs:** 1 - `P015`
- **Status against v0.6:** needs new schema/data
- **Extensions required:** needs both model and expert annotations - only dataset labels in v0.6

### CQ-A13 - Distribution of the image corpus

> How is the image corpus distributed across conditions, plant parts, and capture types?

- **Category:** image
- **Convergence:** 2 of 5 models (Claude Fable 5.1; Claude Opus 5)
- **Source CQs:** 2 - `P013 P048`
- **Status against v0.6:** answerable
- **Extensions required:** needs capture device + distance metadata

### CQ-A14 - Plant organ depicted in an image

> Which plant organ is depicted in a given image?

- **Category:** image
- **Convergence:** 3 of 5 models (Claude Fable 5.1; GPT-5.6 Sol; Gemini Flash 3.8)
- **Source CQs:** 3 - `P120 P082 P012`
- **Status against v0.6:** needs new schema/data
- **Extensions required:** needs PlantPart + visual symptom class | needs PlantPart class - not in v0.6

### CQ-A15 - Symptoms annotated in a given image

> Which visible symptoms are annotated in a given image?

- **Category:** image
- **Convergence:** 2 of 5 models (GPT-5.6 Sol; Gemini Flash 3.8)
- **Source CQs:** 2 - `P081 P118`
- **Status against v0.6:** answerable
- **Extensions required:** partial: 1,442 of 10,407 images carry a captures link (14%)

### CQ-A16 - Disease or pest supported by visual evidence

> Which disease or pest is best supported by the visual evidence in a given image?

- **Category:** image
- **Convergence:** 3 of 5 models (GPT-5.6 Sol; Gemini Flash 3.8; Gemini Pro 3.1)
- **Source CQs:** 4 - `P085 P148 P121 P151`
- **Status against v0.6:** answerable
- **Extensions required:** needs lesion shape/colour/distribution descriptors

### CQ-A17 - Visual features separating confusable conditions

> Which visual features separate two visually confusable conditions?

- **Category:** image
- **Convergence:** 4 of 5 models (Claude Opus 5; GPT-5.6 Sol; Gemini Flash 3.8; Gemini Pro 3.1)
- **Source CQs:** 4 - `P084 P051 P149 P122`
- **Status against v0.6:** answerable

### CQ-A18 - Severity of the damage in an image

> How severe is the damage recorded in a given image?

- **Category:** image
- **Convergence:** 2 of 5 models (Claude Fable 5.1; Gemini Flash 3.8)
- **Source CQs:** 2 - `P014 P119`
- **Status against v0.6:** needs new schema/data
- **Extensions required:** needs region-level lesion annotation - roadmap Phase 2 | needs severity grade per image - SeverityLevel unlinked in v0.6

### CQ-A19 - Symptoms co-occurring in one image

> Which symptoms co-occur on the same plant within a single image?

- **Category:** image
- **Convergence:** 1 of 5 models (Claude Opus 5)
- **Source CQs:** 1 - `P049`
- **Status against v0.6:** needs new schema/data
- **Extensions required:** needs multi-symptom annotation: every annotated image currently carries exactly one captures link

### CQ-A20 - Growth stage visible in a canopy image

> Which growth stage is visually manifest in a whole-canopy image?

- **Category:** image
- **Convergence:** 1 of 5 models (Gemini Flash 3.8)
- **Source CQs:** 1 - `P123`
- **Status against v0.6:** needs new schema/data
- **Extensions required:** needs growth stage annotation on images

### CQ-A21 - Literature symptoms with and without image support

> Which literature-described symptoms have supporting image evidence, and which do not?

- **Category:** crossmodal
- **Convergence:** 2 of 5 models (Claude Fable 5.1; Claude Opus 5)
- **Source CQs:** 2 - `P020 P061`
- **Status against v0.6:** answerable

### CQ-A22 - Literature disease matching an image

> Which literature-described disease matches the symptoms annotated in a given image?

- **Category:** crossmodal
- **Convergence:** 2 of 5 models (Claude Opus 5; GPT-5.6 Sol)
- **Source CQs:** 4 - `P087 P088 P086 P053`
- **Status against v0.6:** answerable

### CQ-A23 - Treatment prescribed for an imaged condition

> Which treatment does the literature prescribe for a condition identified from an image?

- **Category:** crossmodal
- **Convergence:** 1 of 5 models (Gemini Pro 3.1)
- **Source CQs:** 1 - `P153`
- **Status against v0.6:** answerable

---

## 8 CQs requiring schema or data extensions

These are legitimate requirements that v0.6 cannot yet answer. They constitute the v0.7 work plan.

| ID | Question | What is needed |
|---|---|---|
| `CQ-A08` | Natural enemies of a pest | needs NaturalEnemy class - not in v0.6 |
| `CQ-A09` | Distinguishing a nutritional disorder from a disease | needs nutritional disorder (zinc deficiency) - not in v0.6 |
| `CQ-A11` | Provenance and confidence of an image annotation | needs annotator + confidence - confidenceScore unused in v0.6 |
| `CQ-A12` | Disagreement between model and expert annotations | needs both model and expert annotations - only dataset labels in v0.6 |
| `CQ-A14` | Plant organ depicted in an image | needs PlantPart + visual symptom class | needs PlantPart class - not in v0.6 |
| `CQ-A18` | Severity of the damage in an image | needs region-level lesion annotation - roadmap Phase 2 | needs severity grade per image - SeverityLevel unlinked in v0.6 |
| `CQ-A19` | Symptoms co-occurring in one image | needs multi-symptom annotation: every annotated image currently carries exactly one captures link |
| `CQ-A20` | Growth stage visible in a canopy image | needs growth stage annotation on images |

## Still outstanding

- **Stage 4** - reconcile against the 25 CQs already in `CQ_SPARQL_Benchmark_Report.md`: which are corroborated, which are unique to the benchmark, which are new here.
- **Stage 5** - stratified sampling to questionnaire size, instantiating parameterised CQs with concrete diseases, and blinding the questionnaire to source model and convergence count.
