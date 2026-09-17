# Rice MMKG - Competency Question SPARQL Benchmark

**Generated:** 2026-09-17 14:59  
**Ontology:** `Rice MMKG.rdf`  
**Asserted triples:** 67,861  
**After OWL RL materialisation:** 163,297 (+95,436, 34.1s)  
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
| PASS | 21 | 88% |
| PARTIAL | 2 | 8% |
| FAIL | 1 | 4% |
| ERROR | 0 | 0% |
| **Scored total** | **24** | **100%** |
| *(documented, unscored)* | *1* | - |

### Result matrix

| CQ | Depth | Dim | Mode | Outcome | Measurement |
|---|---|---|---|---|---|
| CQ-01 | L1 | D1 | `coverage` | **PASS** | 7/9 disease (78%) |
| CQ-02 | L1 | D1 | `coverage` | **PASS** | 21/22 disease/pest (95%) |
| CQ-03 | L1 | D1 | `coverage` | **PASS** | 17/22 disease/pest (77%) |
| CQ-04 | L1 | D1 | `coverage` | **PASS** | 39/39 symptom (100%) |
| CQ-05 | L2 | D1 | `coverage` | **PASS** | 13/22 disease/pest (59%) |
| CQ-06 | L2 | D1 | `coverage` | **PASS** | 6/7 growth stage (86%) |
| CQ-07 | L2 | D1 | `negative` | **PASS** | 0 violation(s) |
| CQ-08 | L2 | D1 | `coverage` | **PASS** | 2/3 preventive treatment (67%) |
| CQ-09 | L3 | D1 | `coverage` | **PASS** | 1/1 declared vector (100%) |
| CQ-10 | L3 | D1 | `negative` | **PASS** | 0 violation(s) |
| CQ-11 | L3 | D1 | `coverage` | **PASS** | 10/15 disease (67%) |
| CQ-12 | L3 | D1 | `coverage` | **PARTIAL** | 9/22 disease/pest (41%) |
| CQ-13 | L2 | D1 | `coverage` | **FAIL** | 0/4 severity level (0%) |
| CQ-14 | L4 | D1 | `entailment` | **PASS** | 0 asserted -> 1442 entailed |
| CQ-15 | L4 | D1 | `entailment` | **PASS** | 0 asserted -> 169 entailed |
| CQ-16 | L3 | D2 | `coverage` | **PASS** | 8643/8643 diagnostic image (100%) |
| CQ-17 | L2 | D2 | `coverage` | **PASS** | 10/10 annotated class (100%) |
| CQ-18 | L1 | D2 | `coverage` | **PARTIAL** | 1/39 symptom (3%) |
| CQ-19 | L1 | D2 | `negative` | **PASS** | 0 violation(s) |
| CQ-20 | L1 | D2 | `documented` | **DOCUMENTED** | 0 individual(s) |
| CQ-21 | L4 | D3 | `coverage` | **PASS** | 353/353 reified axiom (100%) |
| CQ-22 | L4 | D3 | `negative` | **PASS** | 0 violation(s) |
| CQ-23 | L4 | D3 | `coverage` | **PASS** | 18/30 biological entity (60%) |
| CQ-24 | L4 | D3 | `negative` | **PASS** | 0 violation(s) |
| CQ-25 | L4 | D1 | `negative` | **PASS** | 0 violation(s) |

## 3. Results in detail

### CQ-01 - Factual - single-hop retrieval / Agronomic / symbolic - **PASS**

**Question.** Which rice diseases have an identified causal pathogen?

**Why this CQ.** Aetiological completeness. A disease without a causal agent cannot support any downstream causal query.

**Measurement.** 7 of 9 disease covered - 77.8% (184.9 ms).

**Not covered (2).** `rice:Deadheart`, `rice:Sheath_Blight`

---

### CQ-02 - Factual - single-hop retrieval / Agronomic / symbolic - **PASS**

**Question.** Which diseases and pests have at least one observable symptom?

**Why this CQ.** Diagnosability. Without a symptom link an entity is invisible to field-observation-driven inference.

**Measurement.** 21 of 22 disease/pest covered - 95.5% (14.6 ms).

**Not covered (1).** `rice:Nephotettix_Virescens`

---

### CQ-03 - Factual - single-hop retrieval / Agronomic / symbolic - **PASS**

**Question.** Which diseases and pests have at least one control treatment?

**Why this CQ.** Actionability. The KG must not diagnose what it cannot advise on.

**Measurement.** 17 of 22 disease/pest covered - 77.3% (8.6 ms).

**Not covered (5).** `rice:Iron_Toxicity_Disorder`, `rice:Nitrogen_Deficiency_Disorder`, `rice:Phosphorus_Deficiency_Disorder`, `rice:Potassium_Deficiency_Disorder`, `rice:Salinity_Disorder`

---

### CQ-04 - Factual - single-hop retrieval / Agronomic / symbolic - **PASS**

**Question.** Which symptoms are attached to at least one disease or pest?

**Why this CQ.** Detects orphan symptoms - vocabulary declared but never used in a diagnostic pattern.

**Measurement.** 39 of 39 symptom covered - 100.0% (4.9 ms).

---

### CQ-05 - Contextual - multi-criteria join / Agronomic / symbolic - **PASS**

**Question.** For which diseases/pests can we state both the growth stage of occurrence and an environmental factor raising their risk?

**Why this CQ.** Multi-criteria contextualisation. Both joins are mandatory (no OPTIONAL), so the CQ measures real co-population of occursIn and increaseRiskOf.

**Measurement.** 13 of 22 disease/pest covered - 59.1% (40.5 ms).

**Not covered (9).** `rice:Iron_Toxicity_Disorder`, `rice:Leaf_Folder`, `rice:Nephotettix_Virescens`, `rice:Nitrogen_Deficiency_Disorder`, `rice:Phosphorus_Deficiency_Disorder`, `rice:Potassium_Deficiency_Disorder`, `rice:Rice_Bug`, `rice:Salinity_Disorder`, `rice:Zinc_Deficiency_Disorder`

**Instantiations** (88 total, first 12 shown):

| stage | e | f |
|---|---|---|
| rice:Flowering_Stage | rice:Bacterial_Leaf_Streak | rice:High_Temperature |
| rice:Flowering_Stage | rice:Bacterial_Leaf_Streak | rice:High_Humidity |
| rice:Flowering_Stage | rice:Bacterial_Panicle_Blight | rice:High_Night_Temperature |
| rice:Flowering_Stage | rice:Bacterial_Panicle_Blight | rice:High_Temperature |
| rice:Flowering_Stage | rice:Bacterial_Panicle_Blight | rice:High_Humidity |
| rice:Flowering_Stage | rice:Brown_Planthopper | rice:Excessive_Nitrogen |
| rice:Flowering_Stage | rice:Brown_Planthopper | rice:High_Temperature |
| rice:Flowering_Stage | rice:Rice_Blast_Disease | rice:Low_Rainfall |
| rice:Flowering_Stage | rice:Rice_Blast_Disease | rice:High_Humidity |
| rice:Flowering_Stage | rice:Sheath_Blight | rice:Poor_Soil_Drainage |
| rice:Flowering_Stage | rice:Sheath_Blight | rice:High_Humidity |
| rice:Maturity_Stage | rice:Bacterial_Panicle_Blight | rice:High_Night_Temperature |

---

### CQ-06 - Contextual - multi-criteria join / Agronomic / symbolic - **PASS**

**Question.** Which growth stages have a documented vulnerability profile naming a concrete disease or pest?

**Why this CQ.** vulnerableTo is the most frequently asserted domain relation in the KG (59 triples), so it must be exercised directly.

**Measurement.** 6 of 7 growth stage covered - 85.7% (6.3 ms).

**Not covered (1).** `rice:Harvest_Stage`

---

### CQ-07 - Contextual - multi-criteria join / Agronomic / symbolic - **PASS**

**Question.** Is the stage-vulnerability view consistent with the occurrence view (vulnerableTo without a matching occursIn)?

**Why this CQ.** Integrity constraint. If stage G is vulnerableTo entity E, then E should occursIn G. Any row is an inconsistency.

**Measurement.** 0 violation(s) (7.8 ms). Constraint holds.

---

### CQ-08 - Contextual - multi-criteria join / Agronomic / symbolic - **PASS**

**Question.** Which preventive treatments carry an explicit growth-stage prerequisite for their application?

**Why this CQ.** Prevention advice without a timing constraint is not operationalisable in the field.

**Measurement.** 2 of 3 preventive treatment covered - 66.7% (4.3 ms).

**Not covered (1).** `rice:Seed_Treatment`

---

### CQ-09 - Causal - multi-hop chain / Agronomic / symbolic - **PASS**

**Question.** For which declared insect vectors is the transmission chain vector -> pathogen -> disease fully traversable?

**Why this CQ.** The canonical multi-hop epidemiological query. The denominator is the set of pests asserted to transmit something (not all pests), so the measure is chain completeness, not vector prevalence.

**Measurement.** 1 of 1 declared vector covered - 100.0% (7.2 ms).

**Instantiations** (2 total, first 2 shown):

| v | p | d |
|---|---|---|
| rice:Nephotettix_Virescens | rice:Rice_Tungro_Bacilliform_Virus | rice:Rice_Tungro_Disease |
| rice:Nephotettix_Virescens | rice:Rice_Tungro_Spherical_Virus | rice:Rice_Tungro_Disease |

---

### CQ-10 - Causal - multi-hop chain / Agronomic / symbolic - **PASS**

**Question.** Are there insect vectors for which no control treatment is recorded, leaving the transmission chain unbreakable?

**Why this CQ.** A vector chain that cannot be interrupted has no advisory value. Splitting this from CQ-09 separates 'the chain exists' from 'the chain is actionable'.

**Measurement.** 0 violation(s) (2.8 ms). Constraint holds.

---

### CQ-11 - Causal - multi-hop chain / Agronomic / symbolic - **PASS**

**Question.** For which diseases is the full risk-to-remedy chain traversable: environmental factor -> disease -> symptom -> treatment?

**Why this CQ.** End-to-end decision-support path. This is the query an advisory application actually needs to answer.

**Measurement.** 10 of 15 disease covered - 66.7% (1177.2 ms).

**Not covered (5).** `rice:Iron_Toxicity_Disorder`, `rice:Nitrogen_Deficiency_Disorder`, `rice:Phosphorus_Deficiency_Disorder`, `rice:Potassium_Deficiency_Disorder`, `rice:Salinity_Disorder`

**Instantiations** (293 total, first 12 shown):

| d | f | s | t |
|---|---|---|---|
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Wilting | rice:Water_Management |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Wilting | rice:Resistant_Variety |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Wilting | rice:Crop_Sanitation |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Wilting | rice:Crop_Rotation |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Yellow_Leaf | rice:Water_Management |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Yellow_Leaf | rice:Resistant_Variety |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Yellow_Leaf | rice:Crop_Sanitation |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Yellow_Leaf | rice:Crop_Rotation |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Leaf_Rolling | rice:Water_Management |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Leaf_Rolling | rice:Resistant_Variety |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Leaf_Rolling | rice:Crop_Sanitation |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen | rice:Leaf_Rolling | rice:Crop_Rotation |

---

### CQ-12 - Causal - multi-hop chain / Agronomic / symbolic - **PARTIAL**

**Question.** For which diseases and pests does the KG reach the management layer, i.e. recommend a concrete ManagementAction?

**Why this CQ.** Tests that diagnosis terminates in an operational decision. Note the direction of rice:recommends in this KG is entity -> action, not action -> treatment.

**Measurement.** 9 of 22 disease/pest covered - 40.9% (9.4 ms).

**Not covered (13).** `rice:Armyworm`, `rice:Brown_Planthopper`, `rice:Iron_Toxicity_Disorder`, `rice:Leaf_Folder`, `rice:Nephotettix_Virescens`, `rice:Nitrogen_Deficiency_Disorder`, `rice:Phosphorus_Deficiency_Disorder`, `rice:Potassium_Deficiency_Disorder`, `rice:Rice_Bug`, `rice:Salinity_Disorder`, `rice:Sheath_Blight`, `rice:Stem_Borer`, `rice:Zinc_Deficiency_Disorder`

---

### CQ-13 - Contextual - multi-criteria join / Agronomic / symbolic - **FAIL**

**Question.** Does every severity level map to a recommended management action, so that triage advice is total?

**Why this CQ.** Severity-driven triage is the decision layer of the KG. A severity level with no action is a hole in the advisory logic.

**Measurement.** 0 of 4 severity level covered - 0.0% (7.8 ms).

**Not covered (4).** `rice:Critical_Severity`, `rice:High_Severity`, `rice:Low_Severity`, `rice:Medium_Severity`

---

### CQ-14 - Inferential - requires entailment / Agronomic / symbolic - **PASS**

**Question.** Which observations are SymptomaticObservations, i.e. members of the defined class 'Observation that captures some Symptom'?

**Why this CQ.** The one genuine defined class in the ontology. Asserted membership is zero by construction; a non-zero entailed count proves the OWL axiomatisation does work SPARQL alone cannot.

**Measurement.** 0 answer(s) on the asserted graph, 1442 after OWL RL materialisation (**+1442** contributed by reasoning, 25.6 ms).

---

### CQ-15 - Inferential - requires entailment / Agronomic / symbolic - **PASS**

**Question.** Can the KG be queried in the inverse direction, e.g. disease -> causedBy -> pathogen and symptom -> indicates -> disease?

**Why this CQ.** 14 of 26 object properties are declared as owl:inverseOf but never asserted. Query robustness depends on materialising them.

**Measurement.** 0 answer(s) on the asserted graph, 169 after OWL RL materialisation (**+169** contributed by reasoning, 9.6 ms).

---

### CQ-16 - Causal - multi-hop chain / Cross-modal (image to concept) - **PASS**

**Question.** Which image observations can be grounded all the way to an agronomic recommendation: image -> annotated class -> symptom and treatment?

**Why this CQ.** The central multimodal claim of the KG. The denominator is restricted to images annotated with a Disease or Pest: images labelled with a HealthStatus (healthy plants) correctly have no symptom or treatment, and including them would understate grounding by a fixed 17%.

**Measurement.** 8643 of 8643 diagnostic image covered - 100.0% (3382.3 ms).

---

### CQ-17 - Contextual - multi-criteria join / Cross-modal (image to concept) - **PASS**

**Question.** Which annotated classes of the image corpus are typed as a domain entity (Disease, Pest or HealthStatus)?

**Why this CQ.** Checks that dataset labels were reconciled with the ontology rather than left as free-floating individuals.

**Measurement.** 10 of 10 annotated class covered - 100.0% (882.8 ms).

---

### CQ-18 - Factual - single-hop retrieval / Cross-modal (image to concept) - **PARTIAL**

**Question.** Which symptoms are grounded in visual evidence, i.e. captured by at least one image observation?

**Why this CQ.** Symptom-level visual grounding is what distinguishes an MMKG from a text ontology with images bolted on. Expected to expose the sharpest gap in the current release.

**Measurement.** 1 of 39 symptom covered - 2.6% (27.7 ms).

**Not covered (38).** `rice:Black_Root`, `rice:Brown_Leaf_Tip`, `rice:Brown_Lesion`, `rice:Chewed_Leaf`, `rice:Chlorotic_Leaf_Patch`, `rice:Dark_Green_Erect_Leaf`, `rice:Delayed_Maturity`, `rice:Discolored_Panicle`, `rice:Dry_Leaf_Tip`, `rice:Dusty_Brown_Spot`, `rice:Empty_Grain`, `rice:Excessive_Tillering`, `rice:Grain_Discoloration`, `rice:Hopper_Burn`, `rice:Leaf_Bronzing`, `rice:Leaf_Rolling`, `rice:Leaf_Scratching`, `rice:Leaf_Sheath_Lesion`, `rice:Leaf_Spot`, `rice:Lodging`, `rice:Neck_Rot`, `rice:Necrotic_Leaf_Tip_Margin`, `rice:Panicle_Blast`, `rice:Reduced_Tillering`, `rice:Sterile_Panicle` ...

---

### CQ-19 - Factual - single-hop retrieval / Cross-modal (image to concept) - **PASS**

**Question.** Are there image observations lacking a content URL or a source dataset provenance link?

**Why this CQ.** Integrity constraint on the media layer. Any row means an image cannot be retrieved or attributed.

**Measurement.** 0 violation(s) (1435.1 ms). Constraint holds.

---

### CQ-20 - Factual - single-hop retrieval / Cross-modal (image to concept) - **DOCUMENTED**

**Question.** How many sensor observations does the KG contain?

**Why this CQ.** Declared extension point. Recorded as a measurement, not scored, so the roadmap gap stays visible without inflating or deflating the pass rate.

**Measurement.** 0 individual(s) (2.0 ms). Recorded, not scored.

---

### CQ-21 - Inferential - requires entailment / Provenance and external alignment - **PASS**

**Question.** Which reified domain assertions carry both an authoritative source URI and a bibliographic citation?

**Why this CQ.** Provenance completeness - the scientific-defensibility claim of the KG.

**Measurement.** 353 of 353 reified axiom covered - 100.0% (23.5 ms).

---

### CQ-22 - Inferential - requires entailment / Provenance and external alignment - **PASS**

**Question.** Are there domain assertions with missing or incomplete provenance - either no reified axiom at all, or an axiom missing its source, citation or evidence type?

**Why this CQ.** Integrity constraint complementing CQ-21. Extended on 2026-09-14: the original form checked only axioms that exist, so an assertion with no axiom at all was invisible to both CQ-21 and CQ-22, and v0.6 carried two such assertions while both reported full provenance. Runs on the asserted graph, since materialised inverses are never reified and would all count as violations.

**Measurement.** 0 violation(s) (290.5 ms). Constraint holds.

---

### CQ-23 - Inferential - requires entailment / Provenance and external alignment - **PASS**

**Question.** Which biological entities (disease, pathogen, pest) are aligned to an external vocabulary (EPPO, AGROVOC or NCBI Taxonomy)?

**Why this CQ.** Interoperability. Written as a coverage measure rather than an OPTIONAL projection, which would report success even when every alignment column is null.

**Measurement.** 18 of 30 biological entity covered - 60.0% (11.4 ms).

**Not covered (12).** `rice:Bacterial_Leaf_Blight`, `rice:Bacterial_Leaf_Streak`, `rice:Bacterial_Panicle_Blight`, `rice:Brown_Spot`, `rice:Deadheart`, `rice:Iron_Toxicity_Disorder`, `rice:Nitrogen_Deficiency_Disorder`, `rice:Phosphorus_Deficiency_Disorder`, `rice:Potassium_Deficiency_Disorder`, `rice:Salinity_Disorder`, `rice:Sheath_Blight`, `rice:Zinc_Deficiency_Disorder`

---

### CQ-24 - Inferential - requires entailment / Provenance and external alignment - **PASS**

**Question.** Are annotation literals lexically consistent, i.e. is rice:evidenceType uniformly language-tagged?

**Why this CQ.** Literal-hygiene constraint. An untagged duplicate of a tagged value silently splits GROUP BY and breaks lang() filters.

**Measurement.** 0 violation(s) (15.5 ms). Constraint holds.

---

### CQ-25 - Inferential - requires entailment / Agronomic / symbolic - **PASS**

**Question.** Under entailment, is any individual typed as both a Symptom and a Disease?

**Why this CQ.** Category discipline. Symptom and Disease are intended to be disjoint; an overlap means either a mistyped individual or a property domain that is declared too narrowly. This constraint is checked on the materialised graph, because the conflict is produced by inference and is invisible in the asserted triples.

**Measurement.** 0 violation(s) (4.7 ms). Constraint holds.

---
