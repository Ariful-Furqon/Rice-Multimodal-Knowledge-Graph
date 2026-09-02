# Rice MMKG - Competency Question SPARQL Benchmark

**Generated:** 2026-09-02 11:42  
**Ontology:** `Rice MMKG.rdf`  
**Asserted triples:** 66,873  
**After OWL RL materialisation:** 158,685 (+91,812, 23.6s)  
**Coverage threshold:** 50%

## 1. Evaluation design

Competency Questions are organised on **two independent axes** rather than a single ladder. Reasoning depth and knowledge dimension are orthogonal: provenance and cross-modal grounding are *dimensions* a query ranges over, not a deeper form of inference.

| Reasoning depth | Meaning |
|---|---|
| **L1** | Factual - single-hop retrieval |
| **L2** | Contextual - multi-criteria join |
| **L3** | Causal - multi-hop chain |
| **L4** | Inferential - requires entailment |

| Dimension | Meaning |
|---|---|
| **D1** | Agronomic / symbolic |
| **D2** | Cross-modal (image to concept) |
| **D3** | Provenance and external alignment |

### Evaluation contract

Each CQ declares in advance what counts as a correct answer. A query returning rows is *not* by itself evidence of competency.

| Mode | PASS criterion | Purpose |
|---|---|---|
| `coverage` | covered / total >= 50% | how much of a class the relation actually reaches; uncovered members are listed |
| `negative` | exactly 0 rows | integrity constraint - rows are violations |
| `entailment` | entailed > asserted | proves OWL reasoning contributes answers SPARQL alone cannot |
| `documented` | not scored | declared extension point, recorded to keep the gap visible |

All mandatory hops are expressed **without `OPTIONAL`**. This is the decisive rule of the benchmark: `OPTIONAL` on a hop under test makes a CQ unfalsifiable.

## 2. Summary

| Outcome | Count | Share |
|---|---|---|
| PASS | 20 | 83% |
| PARTIAL | 1 | 4% |
| FAIL | 3 | 12% |
| ERROR | 0 | 0% |
| **Scored total** | **24** | **100%** |
| *(documented, unscored)* | *1* | - |

### Result matrix

| CQ | Depth | Dim | Mode | Outcome | Measurement |
|---|---|---|---|---|---|
| CQ-01 | L1 | D1 | `coverage` | **PASS** | 7/9 disease (78%) |
| CQ-02 | L1 | D1 | `coverage` | **PASS** | 15/16 disease/pest (94%) |
| CQ-03 | L1 | D1 | `coverage` | **PASS** | 15/16 disease/pest (94%) |
| CQ-04 | L1 | D1 | `coverage` | **PASS** | 28/28 symptom (100%) |
| CQ-05 | L2 | D1 | `coverage` | **PASS** | 13/16 disease/pest (81%) |
| CQ-06 | L2 | D1 | `coverage` | **PASS** | 6/7 growth stage (86%) |
| CQ-07 | L2 | D1 | `negative` | **PASS** | 0 violation(s) |
| CQ-08 | L2 | D1 | `coverage` | **PASS** | 1/2 preventive treatment (50%) |
| CQ-09 | L3 | D1 | `coverage` | **PASS** | 1/1 declared vector (100%) |
| CQ-09b | L3 | D1 | `negative` | **FAIL** | 1 violation(s) |
| CQ-10 | L3 | D1 | `coverage` | **PASS** | 9/9 disease (100%) |
| CQ-11 | L3 | D1 | `coverage` | **PASS** | 9/16 disease/pest (56%) |
| CQ-11b | L2 | D1 | `coverage` | **PASS** | 4/4 severity level (100%) |
| CQ-12 | L4 | D1 | `entailment` | **PASS** | 0 asserted -> 1442 entailed |
| CQ-13 | L4 | D1 | `entailment` | **PASS** | 0 asserted -> 139 entailed |
| CQ-14 | L3 | D2 | `coverage` | **PASS** | 8643/8643 diagnostic image (100%) |
| CQ-15 | L2 | D2 | `coverage` | **PASS** | 10/10 annotated class (100%) |
| CQ-16 | L1 | D2 | `coverage` | **PARTIAL** | 1/28 symptom (4%) |
| CQ-17 | L1 | D2 | `negative` | **PASS** | 0 violation(s) |
| CQ-18 | L1 | D2 | `documented` | **DOCUMENTED** | 0 individual(s) |
| CQ-19 | L4 | D3 | `coverage` | **PASS** | 265/265 reified axiom (100%) |
| CQ-20 | L4 | D3 | `negative` | **PASS** | 0 violation(s) |
| CQ-21 | L4 | D3 | `coverage` | **PASS** | 18/24 biological entity (75%) |
| CQ-22 | L4 | D3 | `negative` | **FAIL** | 1 violation(s) |
| CQ-23 | L4 | D1 | `negative` | **FAIL** | 1 violation(s) |

## 3. Results in detail

### CQ-01 - Factual - single-hop retrieval / Agronomic / symbolic - **PASS**

**Question.** Which rice diseases have an identified causal pathogen?

**Why this CQ.** Aetiological completeness. A disease without a causal agent cannot support any downstream causal query.

**Measurement.** 7 of 9 disease covered - 77.8% (221.5 ms).

**Not covered (2).** `rice:Deadheart`, `rice:Sheath_Blight`

---

### CQ-02 - Factual - single-hop retrieval / Agronomic / symbolic - **PASS**

**Question.** Which diseases and pests have at least one observable symptom?

**Why this CQ.** Diagnosability. Without a symptom link an entity is invisible to field-observation-driven inference.

**Measurement.** 15 of 16 disease/pest covered - 93.8% (7.9 ms).

**Not covered (1).** `rice:Nephotettix_Virescens`

---

### CQ-03 - Factual - single-hop retrieval / Agronomic / symbolic - **PASS**

**Question.** Which diseases and pests have at least one control treatment?

**Why this CQ.** Actionability. The KG must not diagnose what it cannot advise on.

**Measurement.** 15 of 16 disease/pest covered - 93.8% (6.3 ms).

**Not covered (1).** `rice:Nephotettix_Virescens`

---

### CQ-04 - Factual - single-hop retrieval / Agronomic / symbolic - **PASS**

**Question.** Which symptoms are attached to at least one disease or pest?

**Why this CQ.** Detects orphan symptoms - vocabulary declared but never used in a diagnostic pattern.

**Measurement.** 28 of 28 symptom covered - 100.0% (3.7 ms).

---

### CQ-05 - Contextual - multi-criteria join / Agronomic / symbolic - **PASS**

**Question.** For which diseases/pests can we state both the growth stage of occurrence and an environmental factor raising their risk?

**Why this CQ.** Multi-criteria contextualisation. Both joins are mandatory (no OPTIONAL), so the CQ measures real co-population of occursIn and increaseRiskOf.

**Measurement.** 13 of 16 disease/pest covered - 81.2% (26.1 ms).

**Not covered (3).** `rice:Leaf_Folder`, `rice:Nephotettix_Virescens`, `rice:Rice_Bug`

**Instantiations** (88 total, first 12 shown):

| stage | e | f |
|---|---|---|
| rice:Flowering_Stage | rice:Bacterial_Leaf_Streak | rice:High_Humidity |
| rice:Flowering_Stage | rice:Bacterial_Leaf_Streak | rice:High_Temperature |
| rice:Flowering_Stage | rice:Bacterial_Panicle_Blight | rice:High_Humidity |
| rice:Flowering_Stage | rice:Bacterial_Panicle_Blight | rice:High_Night_Temperature |
| rice:Flowering_Stage | rice:Bacterial_Panicle_Blight | rice:High_Temperature |
| rice:Flowering_Stage | rice:Brown_Planthopper | rice:High_Temperature |
| rice:Flowering_Stage | rice:Brown_Planthopper | rice:Excessive_Nitrogen |
| rice:Flowering_Stage | rice:Rice_Blast_Disease | rice:High_Humidity |
| rice:Flowering_Stage | rice:Rice_Blast_Disease | rice:Low_Rainfall |
| rice:Flowering_Stage | rice:Sheath_Blight | rice:High_Humidity |
| rice:Flowering_Stage | rice:Sheath_Blight | rice:Poor_Soil_Drainage |
| rice:Maturity_Stage | rice:Bacterial_Panicle_Blight | rice:High_Humidity |

---

### CQ-06 - Contextual - multi-criteria join / Agronomic / symbolic - **PASS**

**Question.** Which growth stages have a documented vulnerability profile naming a concrete disease or pest?

**Why this CQ.** vulnerableTo is the most frequently asserted domain relation in the KG (59 triples), so it must be exercised directly.

**Measurement.** 6 of 7 growth stage covered - 85.7% (6.5 ms).

**Not covered (1).** `rice:Harvest_Stage`

---

### CQ-07 - Contextual - multi-criteria join / Agronomic / symbolic - **PASS**

**Question.** Is the stage-vulnerability view consistent with the occurrence view (vulnerableTo without a matching occursIn)?

**Why this CQ.** Integrity constraint. If stage G is vulnerableTo entity E, then E should occursIn G. Any row is an inconsistency.

**Measurement.** 0 violation(s) (5.7 ms). Constraint holds.

---

### CQ-08 - Contextual - multi-criteria join / Agronomic / symbolic - **PASS**

**Question.** Which preventive treatments carry an explicit growth-stage prerequisite for their application?

**Why this CQ.** Prevention advice without a timing constraint is not operationalisable in the field.

**Measurement.** 1 of 2 preventive treatment covered - 50.0% (3.1 ms).

**Not covered (1).** `rice:Seed_Treatment`

---

### CQ-09 - Causal - multi-hop chain / Agronomic / symbolic - **PASS**

**Question.** For which declared insect vectors is the transmission chain vector -> pathogen -> disease fully traversable?

**Why this CQ.** The canonical multi-hop epidemiological query. The denominator is the set of pests asserted to transmit something (not all pests), so the measure is chain completeness, not vector prevalence.

**Measurement.** 1 of 1 declared vector covered - 100.0% (5.2 ms).

**Instantiations** (2 total, first 2 shown):

| v | p | d |
|---|---|---|
| rice:Nephotettix_Virescens | rice:Rice_Tungro_Bacilliform_Virus | rice:Rice_Tungro_Disease |
| rice:Nephotettix_Virescens | rice:Rice_Tungro_Spherical_Virus | rice:Rice_Tungro_Disease |

---

### CQ-09b - Causal - multi-hop chain / Agronomic / symbolic - **FAIL**

**Question.** Are there insect vectors for which no control treatment is recorded, leaving the transmission chain unbreakable?

**Why this CQ.** A vector chain that cannot be interrupted has no advisory value. Splitting this from CQ-09 separates 'the chain exists' from 'the chain is actionable'.

**Measurement.** 1 violation(s) (2.3 ms). Constraint is broken.

**Violating rows (sample):**

- `rice:Nephotettix_Virescens`

---

### CQ-10 - Causal - multi-hop chain / Agronomic / symbolic - **PASS**

**Question.** For which diseases is the full risk-to-remedy chain traversable: environmental factor -> disease -> symptom -> treatment?

**Why this CQ.** End-to-end decision-support path. This is the query an advisory application actually needs to answer.

**Measurement.** 9 of 9 disease covered - 100.0% (375.7 ms).

**Instantiations** (277 total, first 12 shown):

| d | f | s | t |
|---|---|---|---|
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Wilting | rice:Crop_Rotation |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Wilting | rice:Crop_Sanitation |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Wilting | rice:Resistant_Variety |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Wilting | rice:Water_Management |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Dry_Leaf_Tip | rice:Crop_Rotation |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Dry_Leaf_Tip | rice:Crop_Sanitation |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Dry_Leaf_Tip | rice:Resistant_Variety |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Dry_Leaf_Tip | rice:Water_Management |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Yellow_Leaf | rice:Crop_Rotation |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Yellow_Leaf | rice:Crop_Sanitation |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Yellow_Leaf | rice:Resistant_Variety |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity | rice:Yellow_Leaf | rice:Water_Management |

---

### CQ-11 - Causal - multi-hop chain / Agronomic / symbolic - **PASS**

**Question.** For which diseases and pests does the KG reach the management layer, i.e. recommend a concrete ManagementAction?

**Why this CQ.** Tests that diagnosis terminates in an operational decision. Note the direction of rice:recommends in this KG is entity -> action, not action -> treatment.

**Measurement.** 9 of 16 disease/pest covered - 56.2% (5.4 ms).

**Not covered (7).** `rice:Armyworm`, `rice:Brown_Planthopper`, `rice:Leaf_Folder`, `rice:Nephotettix_Virescens`, `rice:Rice_Bug`, `rice:Sheath_Blight`, `rice:Stem_Borer`

---

### CQ-11b - Contextual - multi-criteria join / Agronomic / symbolic - **PASS**

**Question.** Does every severity level map to a recommended management action, so that triage advice is total?

**Why this CQ.** Severity-driven triage is the decision layer of the KG. A severity level with no action is a hole in the advisory logic.

**Measurement.** 4 of 4 severity level covered - 100.0% (5.0 ms).

**Instantiations** (6 total, first 6 shown):

| sev | m |
|---|---|
| rice:Critical_Severity | rice:Immediate_Intervention |
| rice:High_Severity | rice:Preventive_Action |
| rice:High_Severity | rice:Immediate_Intervention |
| rice:Low_Severity | rice:No_Action_Needed |
| rice:Medium_Severity | rice:Field_Inspection |
| rice:Medium_Severity | rice:Monitoring |

---

### CQ-12 - Inferential - requires entailment / Agronomic / symbolic - **PASS**

**Question.** Which observations are SymptomaticObservations, i.e. members of the defined class 'Observation that captures some Symptom'?

**Why this CQ.** The one genuine defined class in the ontology. Asserted membership is zero by construction; a non-zero entailed count proves the OWL axiomatisation does work SPARQL alone cannot.

**Measurement.** 0 answer(s) on the asserted graph, 1442 after OWL RL materialisation (**+1442** contributed by reasoning, 14.0 ms).

---

### CQ-13 - Inferential - requires entailment / Agronomic / symbolic - **PASS**

**Question.** Can the KG be queried in the inverse direction, e.g. disease -> causedBy -> pathogen and symptom -> indicates -> disease?

**Why this CQ.** 14 of 26 object properties are declared as owl:inverseOf but never asserted. Query robustness depends on materialising them.

**Measurement.** 0 answer(s) on the asserted graph, 139 after OWL RL materialisation (**+139** contributed by reasoning, 6.3 ms).

---

### CQ-14 - Causal - multi-hop chain / Cross-modal (image to concept) - **PASS**

**Question.** Which image observations can be grounded all the way to an agronomic recommendation: image -> annotated class -> symptom and treatment?

**Why this CQ.** The central multimodal claim of the KG. The denominator is restricted to images annotated with a Disease or Pest: images labelled with a HealthStatus (healthy plants) correctly have no symptom or treatment, and including them would understate grounding by a fixed 17%.

**Measurement.** 8643 of 8643 diagnostic image covered - 100.0% (2007.6 ms).

---

### CQ-15 - Contextual - multi-criteria join / Cross-modal (image to concept) - **PASS**

**Question.** Which annotated classes of the image corpus are typed as a domain entity (Disease, Pest or HealthStatus)?

**Why this CQ.** Checks that dataset labels were reconciled with the ontology rather than left as free-floating individuals.

**Measurement.** 10 of 10 annotated class covered - 100.0% (445.6 ms).

---

### CQ-16 - Factual - single-hop retrieval / Cross-modal (image to concept) - **PARTIAL**

**Question.** Which symptoms are grounded in visual evidence, i.e. captured by at least one image observation?

**Why this CQ.** Symptom-level visual grounding is what distinguishes an MMKG from a text ontology with images bolted on. Expected to expose the sharpest gap in the current release.

**Measurement.** 1 of 28 symptom covered - 3.6% (18.5 ms).

**Not covered (27).** `rice:Brown_Leaf_Tip`, `rice:Brown_Lesion`, `rice:Chewed_Leaf`, `rice:Dead_Tiller`, `rice:Discolored_Panicle`, `rice:Dry_Leaf_Tip`, `rice:Empty_Grain`, `rice:Excessive_Tillering`, `rice:Grain_Discoloration`, `rice:Hopper_Burn`, `rice:Leaf_Rolling`, `rice:Leaf_Scratching`, `rice:Leaf_Spot`, `rice:Neck_Rot`, `rice:Panicle_Blast`, `rice:Reduced_Tillering`, `rice:Stem_Rot_Symptom`, `rice:Sterile_Panicle`, `rice:Stunted_Growth`, `rice:Translucent_Stripe`, `rice:Water_Soaked_Streak`, `rice:White_Ear`, `rice:White_Streak`, `rice:Wilting`, `rice:Yellow_Leaf` ...

---

### CQ-17 - Factual - single-hop retrieval / Cross-modal (image to concept) - **PASS**

**Question.** Are there image observations lacking a content URL or a source dataset provenance link?

**Why this CQ.** Integrity constraint on the media layer. Any row means an image cannot be retrieved or attributed.

**Measurement.** 0 violation(s) (897.4 ms). Constraint holds.

---

### CQ-18 - Factual - single-hop retrieval / Cross-modal (image to concept) - **DOCUMENTED**

**Question.** How many sensor observations does the KG contain?

**Why this CQ.** Declared extension point. Recorded as a measurement, not scored, so the roadmap gap stays visible without inflating or deflating the pass rate.

**Measurement.** 0 individual(s) (1.4 ms). Recorded, not scored.

---

### CQ-19 - Inferential - requires entailment / Provenance and external alignment - **PASS**

**Question.** Which reified domain assertions carry both an authoritative source URI and a bibliographic citation?

**Why this CQ.** Provenance completeness - the scientific-defensibility claim of the KG.

**Measurement.** 265 of 265 reified axiom covered - 100.0% (11.3 ms).

---

### CQ-20 - Inferential - requires entailment / Provenance and external alignment - **PASS**

**Question.** Are there reified axioms with incomplete provenance (missing source, citation or evidence type)?

**Why this CQ.** Integrity constraint complementing CQ-19.

**Measurement.** 0 violation(s) (37.1 ms). Constraint holds.

---

### CQ-21 - Inferential - requires entailment / Provenance and external alignment - **PASS**

**Question.** Which biological entities (disease, pathogen, pest) are aligned to an external vocabulary (EPPO, AGROVOC or NCBI Taxonomy)?

**Why this CQ.** Interoperability. Written as a coverage measure rather than an OPTIONAL projection, which would report success even when every alignment column is null.

**Measurement.** 18 of 24 biological entity covered - 75.0% (7.4 ms).

**Not covered (6).** `rice:Bacterial_Leaf_Blight`, `rice:Bacterial_Leaf_Streak`, `rice:Bacterial_Panicle_Blight`, `rice:Brown_Spot`, `rice:Deadheart`, `rice:Sheath_Blight`

---

### CQ-22 - Inferential - requires entailment / Provenance and external alignment - **FAIL**

**Question.** Are annotation literals lexically consistent, i.e. is rice:evidenceType uniformly language-tagged?

**Why this CQ.** Literal-hygiene constraint. An untagged duplicate of a tagged value silently splits GROUP BY and breaks lang() filters.

**Measurement.** 1 violation(s) (10.6 ms). Constraint is broken.

**Violating rows (sample):**

- `Nbfaed4dbd7b44b53bd1f94cabfb4cac5` / `literature-curated`

---

### CQ-23 - Inferential - requires entailment / Agronomic / symbolic - **FAIL**

**Question.** Under entailment, is any individual typed as both a Symptom and a Disease?

**Why this CQ.** Category discipline. Symptom and Disease are intended to be disjoint; an overlap means either a mistyped individual or a property domain that is declared too narrowly. This constraint is checked on the materialised graph, because the conflict is produced by inference and is invisible in the asserted triples.

**Measurement.** 1 violation(s) (1.8 ms). Constraint is broken.

**Violating rows (sample):**

- `rice:Deadheart`

---
