# Rice MMKG 0.7.0-dev — SPARQL Competency Question Documentation

**Ontology:** `Rice MMKG.rdf` (owl:versionInfo 0.7.0-dev; last release v0.6.2)  
**Triples:** 68,064 asserted / 163,715 after OWL RL materialisation (+95,651 triples)  
**Benchmark Execution:** 2026-09-17  
**Overall Result:** 21 PASS / 2 PARTIAL / 1 FAIL / 1 DOCUMENTED (24 scored + 1 documented = 25 CQs)
**Pass Rate:** 87.5% (21/24 scored CQs); v0.6.2: 95.8% (23/24)

> **0.7.0-dev Note (2026-09-15):**  
> `PlantPart` (8 individuals), `affectsPlantPart` (27 assertions, citing IRRI Rice Knowledge Bank fact sheets) and `partOf` (2 assertions, from the Plant Ontology) were added. Verdicts are unchanged. Two measurements move because the new assertions are reified: CQ-21 256/256 → **285/285**, and CQ-22 now also checks `affectsPlantPart` and `partOf` (still 0 violations). The new property was added to CQ-22's list rather than left out, so that the extension could not pass CQ-22 by omission. All other results are identical to v0.6.2. See the 0.7.0-dev entry in `Ontology_Overview.md`.  
> **Then** `TransmissionMode` (1 individual) and `hasTransmissionMode` (2 assertions, citing Wang et al. 2022) were added; CQ-21 → **287/287**, `hasTransmissionMode` added to CQ-22's list (0 violations), verdicts unchanged.  
> **Then** `ManagementCategory` (4 individuals, AGROVOC) and `hasManagementCategory` (6 assertions, citing IRRI or AGROVOC definitions) were added; CQ-21 → **293/293**, `hasManagementCategory` added to CQ-22's list (0 violations), verdicts unchanged.  
> **Then** `AbioticFactor` was added: four nutrient deficiencies (N, P, K, Zn) that `causes` four new disorder individuals typed `Disease`, citing the IRRI nutrient fact sheets. The Disease and Disease ∪ Pest denominators grew (9 → 13, 16 → 20), so several coverage figures moved, and **CQ-12 fell to PARTIAL (9/20)** because no source gives the disorders a ManagementAction. **CQ-01's numerator was corrected** to require `?p a rice:Pathogen`: `causes` now also has abiotic subjects, and the unfiltered query reported 11/13 by counting them as pathogens. On every earlier version the two forms return identical results. The matrix and the per-CQ sections show 0.7.0-dev figures (sections brought up to date 2026-09-17, with the v0.6.2 values kept as history lines); the generated `CQ_SPARQL_Benchmark_Report.md` has the current values and uncovered entities for all 25.  
> **Then** the unverified BBPOPT source was resolved and iron toxicity and salinity were added:
> - **CQ-13 → FAIL (0/4).** The six severity → ManagementAction assertions were removed: no document supports them, and the 2021 Indonesian juknis contradicts one of them. The CQ was not edited.
> - **CQ-01 fell to PARTIAL (7/15), then its denominator was corrected (approved 2026-09-15).** The two new disorders had entered the Disease denominator, and an abiotic disorder has no pathogen by construction. The denominator now excludes any disease caused by an `AbioticFactor` (a criterion, not a list of names). Result: **7/9, PASS**; the uncorrected form gives 7/15 (PARTIAL), and both are reported. Only CQ-01 was corrected: CQ-03, CQ-11 and CQ-12 still count abiotic disorders, because control, risk-to-remedy and management actions do apply to them.
> - **Other figures:** CQ-12 9/22, CQ-08 2/3, CQ-21 **341/341**.
> **Then** `Variety` was added (IR64, Angke, Conde; 12 assertions citing Mackill & Khush 2018), with `varietyOf`, `resistantTo` and `moderatelyResistantTo` added to CQ-22's checked list. CQ-21 → **353/353**; all verdicts unchanged (21 / 2 / 1 / 1). Varieties are neither diseases nor pests, so no coverage denominator moved.
> **Then** the namespace moved to `https://w3id.org/ricemmkg#` (2026-09-17). Every answer of both instruments is identical to the previous run, compared field by field (timings and truncated row samples aside); only the triple counts moved (+4, all in the ontology header).
> **Then** varietal resistance became `ResistanceAssessment` individuals (2026-09-17): `resistantTo` and `moderatelyResistantTo` were removed from the schema and from CQ-22's property list, 9 round-1 axioms left and 3 `varietyOf` axioms came in, so CQ-21 → **347/347**. CQ-22 gained a third branch for assessments missing their source, citation or evidence type, since an assessment carries its provenance on itself rather than on an axiom; it reports 0 violations in both the previous and the extended form, and a control file with one source removed reports exactly 1. All verdicts unchanged (21 / 2 / 1 / 1).
> **Then** `Rhizoctonia_Solani` was added as the pathogen of sheath blight (IRRI fact sheet; 2026-09-17): CQ-01 7/9 → **8/9**, CQ-15 → 170, CQ-21 → **348/348**, CQ-23 → 19/31. Verdicts unchanged; at the 80% sensitivity threshold PASS rises from 15 to 16.

> **v0.6.1 Patch Note (2026-09-14):**  
> Three domain assertions gained or received provenance and one literal was tagged: `Stem_Borer indicatedBy Dead_Tiller` and `Stem_Borer indicatedBy White_Ear` (present since v0.6 but never reified) now carry `owl:Axiom` records citing IRAC (2025); `Nephotettix_Virescens controlledBy Resistant_Variety` was added, citing Gallagher et al. (2002); and the one untagged `rice:evidenceType` literal is now `@en`. CQ-10 and CQ-24 move from FAIL to PASS. The CQ-10 fix deliberately departs from the action item planned in v0.6 (`controlledBy Vector_Control`): FAO and IRRI both report that insecticide control of the green leafhopper often fails to control tungro and recommend resistant varieties instead, so asserting vector control only to satisfy the CQ would not have been supported by the literature. Pre-patch file: `Ontology/Backup/Rice MMKG.backup-v0.6-pre-v0.6.1.rdf`.

> **Correction to previously published v0.6 figures:**  
> The v0.6 numbers originally reported here (66,874 asserted / 161,568 materialised triples, 265 axioms, CQ-15 = 140, CQ-21 = 265/265) were measured at commit `19d632d`, before the same-day inconsistency fix (`103c5ed`) removed 11 domain assertions and their 12 axioms. Re-measured on the released v0.6 file (git tag `elicited-baseline-v0.6`): 66,780 asserted / 161,416 materialised triples, 253 axioms over 255 domain assertions, verdicts unchanged at 21 PASS / 1 PARTIAL / 2 FAIL / 1 DOC, CQ-15 = 133, CQ-21 = 253/253.

> **CQ-22 extended (2026-09-14):**  
> CQ-21 divides by the number of axioms, so an assertion with no axiom at all is invisible to it, and the original CQ-22 checked only axioms that exist. v0.6 therefore reported full provenance while two assertions had none. CQ-22 now also flags domain assertions without a reified axiom. Against the released v0.6 file the extended CQ-22 reports **2 violations (FAIL)**, where the original form reported 0; against v0.6.1 it reports 0. The CQ count stays at 25.

> **v0.6 Release Note:**  
> Version 0.6 resolves the `Deadheart` class collision identified in v0.5. `Deadheart` is now formally classified as a `Disease` (damage syndrome), while `Dead_Tiller` represents the observed `Symptom`. All 1,442 dead-heart images now capture `Dead_Tiller`, fully satisfying `SymptomaticObservation` while clearing all disjointness conflicts (CQ-25 now **PASS** with 0 violations). Pre-fix v0.5 is preserved in `Ontology/Backup/Rice MMKG.backup-v.05.rdf`.

---

## Prefix Block

```sparql
PREFIX rice:    <https://w3id.org/ricemmkg#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX prov:    <http://www.w3.org/ns/prov#>
PREFIX schema:  <http://schema.org/>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
```

---

## Evaluation Framework: Two Orthogonal Axes

Each CQ is positioned along two orthogonal axes: **Reasoning Depth (L1–L4)** and **Knowledge Dimension (D1–D3)**.

| Reasoning Depth | Focus | Evaluation Method |
|---|---|---|
| **L1 (Factual)** | Direct 1-hop relation & property retrieval | SPARQL `SELECT` over classes |
| **L2 (Contextual)** | Multi-criteria joins (e.g., stage + climate) | SPARQL `JOIN` + negative constraints |
| **L3 (Causal)** | Multi-hop chains (e.g., vector -> pathogen -> disease) | SPARQL multi-hop graph traversal |
| **L4 (Inferential)** | Defined-class membership, inverse relations, disjointness | Asserted vs. OWL RL Materialised Graph |

| Knowledge Dimension | Scope & Domain Layer | Key Entities & Relations |
|---|---|---|
| **D1 (Agronomic/Symbolic)** | Core agronomy domain & decision support | `Disease`, `Pest`, `Symptom`, `Treatment`, `GrowthStage`, `EnvFactor` |
| **D2 (Cross-modal)** | Image observations & multimodal grounding | `ImageObservation`, `SensorObservation`, `annotatedAs`, `captures` |
| **D3 (Provenance/Alignment)** | Traceability & external interoperability | `owl:Axiom`, `EPPO`, `AGROVOC`, `NCBI Taxonomy` |

### Pass Criteria (4 Modes)

| Mode | PASS Criterion | Purpose |
|---|---|---|
| `coverage` | covered / total >= 50% | Measures relational population completeness; missing members listed |
| `negative` | exactly 0 rows | Integrity constraint & anti-pattern detection; rows represent violations |
| `entailment` | entailed > asserted | Proves OWL RL reasoning contributes answers invisible in raw RDF |
| `documented` | (not scored) | Declared extension point (e.g. sensor data), kept visible |

> **Key rule:** Mandatory hops are written **without `OPTIONAL`**. Using `OPTIONAL` on tested hops makes CQs unfalsifiable by always returning rows from anchor classes.

### Sensitivity to the Coverage Threshold (added 2026-09-17)

The 50% threshold is an **author-set convention** — a majority of the class is reached — not a published standard; CQ-based evaluation methods treat a CQ as answered or not and give no numeric cut-off to cite. The runner therefore also reports every `coverage` verdict at 40–80% (`SENSITIVITY_THRESHOLDS` in `cq_sparql_benchmark.py`, written to the report and to `sensitivity` in the JSON). The headline result stays at 50%. Only the 16 `coverage` CQs can change; the other modes keep their verdicts.

| CQ | Coverage | 40% | 50% | 60% | 70% | 80% |
|---|---|---|---|---|---|---|
| CQ-01 | 8/9 (89%) | PASS | PASS | PASS | PASS | PASS |
| CQ-02 | 21/22 (95%) | PASS | PASS | PASS | PASS | PASS |
| CQ-03 | 17/22 (77%) | PASS | PASS | PASS | PASS | PARTIAL |
| CQ-04 | 39/39 (100%) | PASS | PASS | PASS | PASS | PASS |
| CQ-05 | 13/22 (59%) | PASS | PASS | PARTIAL | PARTIAL | PARTIAL |
| CQ-06 | 6/7 (86%) | PASS | PASS | PASS | PASS | PASS |
| CQ-08 | 2/3 (67%) | PASS | PASS | PASS | PARTIAL | PARTIAL |
| CQ-09 | 1/1 (100%) | PASS | PASS | PASS | PASS | PASS |
| CQ-11 | 10/15 (67%) | PASS | PASS | PASS | PARTIAL | PARTIAL |
| CQ-12 | 9/22 (41%) | PASS | PARTIAL | PARTIAL | PARTIAL | PARTIAL |
| CQ-13 | 0/4 (0%) | FAIL | FAIL | FAIL | FAIL | FAIL |
| CQ-16 | 8643/8643 (100%) | PASS | PASS | PASS | PASS | PASS |
| CQ-17 | 10/10 (100%) | PASS | PASS | PASS | PASS | PASS |
| CQ-18 | 1/39 (3%) | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL |
| CQ-21 | 348/348 (100%) | PASS | PASS | PASS | PASS | PASS |
| CQ-23 | 19/31 (61%) | PASS | PASS | PASS | PARTIAL | PARTIAL |
| **PASS (24 scored)** | | **22** (91.7%) | **21** (87.5%) | **20** (83.3%) | **17** (70.8%) | **16** (66.7%) |

**Reading.** Between 40% and 60% the pass rate moves by one CQ either way (CQ-12 at 41%, CQ-05 at 59%). At 70% three more CQs drop to PARTIAL (CQ-08 and CQ-11 at 67%, CQ-23 at 60%), and at 80% CQ-03 follows (CQ-01 held at 80% from 2026-09-17, when sheath blight got its pathogen: 8/9 = 89%). Small denominators make single verdicts fragile — CQ-08 has 3 members and CQ-09 one — so the raw ratio should be read alongside each label.

---

## Master Result Matrix (25 Competency Questions — 0.7.0-dev)

| CQ ID | Depth | Dim | Mode | Result | Measurement | Summary |
|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **CQ-01** | L1 | D1 | `coverage`   | **PASS**       | 8/9 (89%)            | Rice diseases with causal pathogens (numerator and denominator corrected in 0.7.0-dev; uncorrected denominator: 7/15; v0.6.2: 7/9) |
| **CQ-02** | L1 | D1 | `coverage`   | **PASS**       | 21/22 (95%)          | Diseases/pests with observable symptoms (v0.6.2: 15/16) |
| **CQ-03** | L1 | D1 | `coverage`   | **PASS**       | 17/22 (77%)          | Diseases/pests with control treatments (v0.6.2: 16/16; v0.6: 15/16) |
| **CQ-04** | L1 | D1 | `coverage`   | **PASS**       | 39/39 (100%)         | Symptoms attached to domain entities (zero orphan; v0.6.2: 27/27) |
| **CQ-05** | L2 | D1 | `coverage`   | **PASS**       | 13/22 (59%)          | Co-occurrence: Growth stage + Env. risk factor (v0.6.2: 13/16) |
| **CQ-06** | L2 | D1 | `coverage`   | **PASS**       | 6/7 (86%)            | Growth stages with vulnerability profiles (`vulnerableTo`) |
| **CQ-07** | L2 | D1 | `negative`   | **PASS**       | 0 violations         | Consistency between `vulnerableTo` and `occursIn` |
| **CQ-08** | L2 | D1 | `coverage`   | **PASS**       | 2/3 (67%)            | Preventive treatments with growth-stage prerequisites (v0.6.2: 1/2) |
| **CQ-09** | L3 | D1 | `coverage`   | **PASS**       | 1/1 (100%)           | Vector transmission chain: vector -> pathogen -> disease |
| **CQ-10** | L3 | D1 | `negative`   | **PASS**       | 0 violations         | Vectors without control treatments (v0.6: 1, `Nephotettix_Virescens`) |
| **CQ-11** | L3 | D1 | `coverage`   | **PASS**       | 10/15 (67%)          | End-to-end DSS chain: env -> disease -> symptom -> treatment (v0.6.2: 9/9) |
| **CQ-12** | L3 | D1 | `coverage`   | **PARTIAL**    | 9/22 (41%)           | Diseases/pests recommending concrete `ManagementAction` (v0.6.2: 9/16, PASS) |
| **CQ-13** | L2 | D1 | `coverage`   | **FAIL**       | 0/4 (0%)             | Total triage: Every `SeverityLevel` maps to an action (unsourced mapping removed in 0.7.0-dev; v0.6.2: 4/4) |
| **CQ-14** | L4 | D1 | `entailment` | **PASS**       | 0 -> 1,442 rows      | OWL classification: `SymptomaticObservation` defined class |
| **CQ-15** | L4 | D1 | `entailment` | **PASS**       | 0 -> 170 rows        | Bidirectional query capability via inverse properties (v0.6: 133) |
| **CQ-16** | L3 | D2 | `coverage`   | **PASS**       | 8,643/8,643 (100%)   | Multimodal grounding: Image -> Class -> Symptom & Treatment |
| **CQ-17** | L2 | D2 | `coverage`   | **PASS**       | 10/10 (100%)         | Dataset annotation labels typed as OWL domain classes |
| **CQ-18** | L1 | D2 | `coverage`   | **PARTIAL**    | 1/39 (3%)            | Direct visual grounding of symptoms (`rice:captures`) |
| **CQ-19** | L1 | D2 | `negative`   | **PASS**       | 0 violations         | Media layer integrity: Content URL & dataset provenance |
| **CQ-20** | L1 | D2 | `documented` | **DOC**        | 0 individuals        | Sensor observation population (Phase 3 extension point) |
| **CQ-21** | L4 | D3 | `coverage`   | **PASS**       | 348/348 (100%)       | Reified domain axioms with source URI and citation (v0.6.2: 256/256; v0.6: 253/253) |
| **CQ-22** | L4 | D3 | `negative`   | **PASS**       | 0 violations         | Domain assertions without an axiom, or axioms with incomplete provenance (extended 2026-09-14; v0.6: 2) |
| **CQ-23** | L4 | D3 | `coverage`   | **PASS**       | 19/31 (61%)          | Biological entities aligned to EPPO / AGROVOC / NCBI |
| **CQ-24** | L4 | D3 | `negative`   | **PASS**       | 0 violations         | Literal hygiene: Uniform language tags (`@en`) on `evidenceType` (v0.6: 1) |
| **CQ-25** | L4 | D1 | `negative`   | **PASS**       | 0 violations         | Class disjointness: Entailed overlap between `Symptom` & `Disease` |

---

## Detailed CQ Specifications & SPARQL Queries

### Section A: Agronomic / Symbolic Domain (D1)

#### CQ-01 | L1 x D1 | coverage | PASS (8/9 diseases, 89%)
**Question:** Which rice diseases have an identified causal pathogen?
**Rationale:** Aetiological completeness. A disease without a causal agent cannot support downstream causal inference.
**Numerator Query (corrected 2026-09-15, 0.7.0-dev):**
```sparql
SELECT DISTINCT ?d WHERE { ?d a rice:Disease . ?p rice:causes ?d . ?p a rice:Pathogen }
```
**Numerator Query (original, v0.6 – v0.6.2):**
```sparql
SELECT DISTINCT ?d WHERE { ?d a rice:Disease . ?p rice:causes ?d }
```
**Why corrected:** `AbioticFactor` became a second possible subject of `causes`. The original form then reported 11/13, counting the four nutrient-deficiency disorders as having a causal *pathogen*. The question text is unchanged; on every version before 0.7.0-dev the two forms return the same set, because only pathogens could `causes`.
**Denominator Query (corrected 2026-09-15, 0.7.0-dev):**
```sparql
SELECT DISTINCT ?d WHERE { ?d a rice:Disease .
  FILTER NOT EXISTS { ?a rice:causes ?d . ?a a rice:AbioticFactor } }
```
**Denominator Query (original, v0.6 – 0.7.0-dev before this correction):**
```sparql
SELECT DISTINCT ?d WHERE { ?d a rice:Disease }
```
**Why corrected:** the question asks for a causal *pathogen*, which cannot exist for a disorder caused by an abiotic factor. With the original denominator, every abiotic disorder counted as a gap: 7/13 after the four nutrient disorders, and 7/15 (PARTIAL) after iron toxicity and salinity. That figure measured the modelling pattern, not missing knowledge. The exclusion is a criterion, so future abiotic disorders are excluded without naming them. The question text is unchanged. CQ-03, CQ-11 and CQ-12 were deliberately not corrected: their questions (control, risk-to-remedy chain, management action) apply to abiotic disorders too.  
**Result (0.7.0-dev, corrected):** 8 covered / 9 total (88.9%) — PASS (7/9 before `Rhizoctonia_Solani causes Sheath_Blight` was added on 2026-09-17)  
**Result (0.7.0-dev, original denominator):** 8 covered / 15 total (53.3%) — PASS (7/15, PARTIAL, before that addition)  
**Uncovered entities (1):** `rice:Deadheart` (a damage syndrome caused by a pest, so it has no pathogen by nature).  
**v0.6.2:** 7/9 (77.8%), uncovered `Deadheart`, `Sheath_Blight`; both forms of the denominator give the same set on v0.6.x, because no `AbioticFactor` existed.

---

#### CQ-02 | L1 x D1 | coverage | PASS (21/22 disease/pest, 95%)
**Question:** Which diseases and pests have at least one observable symptom?
**Rationale:** Diagnosability. Without a symptom link, an entity is invisible to symptom-driven diagnostic inference.
**Numerator Query:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:indicatedBy ?s . ?s a rice:Symptom }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```
**Result (0.7.0-dev):** 21 covered / 22 total (95.5%) — PASS  
**Uncovered entities (1):** `rice:Nephotettix_Virescens`  
**v0.6.2:** 15/16 (93.8%), same uncovered entity; the six abiotic disorders entered with their symptoms.

---

#### CQ-03 | L1 x D1 | coverage | PASS (17/22 disease/pest, 77%)
**Question:** Which diseases and pests have at least one control treatment?
**Rationale:** Actionability. The KG must not diagnose what it cannot advise on.
**Numerator Query:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:controlledBy ?t . ?t a rice:Treatment }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```
**Result (0.7.0-dev):** 17 covered / 22 total (77.3%) — PASS  
**Uncovered entities (5):** `Iron_Toxicity_Disorder`, `Nitrogen_Deficiency_Disorder`, `Phosphorus_Deficiency_Disorder`, `Potassium_Deficiency_Disorder`, `Salinity_Disorder` — IRRI gives fertilizer rates or prevention (`preventedBy Water_Management`) for these, not a control treatment; only zinc deficiency has one (`Zinc_Fertilizer_Application`).  
**v0.6.2:** 16/16 (100%).  
**v0.6:** 15/16 (93.8%), uncovered `rice:Nephotettix_Virescens`; closed in v0.6.1 by `controlledBy Resistant_Variety` (see CQ-10).

---

#### CQ-04 | L1 x D1 | coverage | PASS (39/39 symptoms, 100%)
**Question:** Which symptoms are attached to at least one disease or pest?
**Rationale:** Detects orphan symptoms — vocabulary declared but never utilized in diagnostic patterns.
**Numerator Query:**
```sparql
SELECT DISTINCT ?s WHERE { ?s a rice:Symptom . ?e rice:indicatedBy ?s }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?s WHERE { ?s a rice:Symptom }
```
**Result (0.7.0-dev):** 39 covered / 39 total (100.0%) — PASS. Zero orphan vocabulary; the 12 symptoms added for the abiotic disorders are all attached. **v0.6.2:** 27/27.

---

#### CQ-05 | L2 x D1 | coverage | PASS (13/22 disease/pest, 59%)
**Question:** For which diseases/pests can we state both the growth stage of occurrence AND an environmental factor raising their risk?
**Rationale:** Multi-criteria contextualisation. Both joins are mandatory (no `OPTIONAL`), measuring true co-population.
**Numerator Query:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:occursIn ?stage . ?stage a rice:GrowthStage .
  ?f rice:increaseRiskOf ?e . ?f a rice:EnvironmentalFactor }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```
**Result (0.7.0-dev):** 13 covered / 22 total (59.1%) — PASS (88 instantiations); PARTIAL from a 60% threshold (see the sensitivity table)  
**Uncovered entities (9):** `rice:Leaf_Folder`, `rice:Nephotettix_Virescens`, `rice:Rice_Bug`, and the six abiotic disorders (`Iron_Toxicity_Disorder`, `Nitrogen_Deficiency_Disorder`, `Phosphorus_Deficiency_Disorder`, `Potassium_Deficiency_Disorder`, `Salinity_Disorder`, `Zinc_Deficiency_Disorder`), which have no growth stage of occurrence  
**v0.6.2:** 13/16 (81.2%), uncovered `Leaf_Folder`, `Nephotettix_Virescens`, `Rice_Bug`.

---

#### CQ-06 | L2 x D1 | coverage | PASS (6/7 growth stages, 86%)
**Question:** Which growth stages have a documented vulnerability profile naming a concrete disease or pest?
**Rationale:** Exercises the `vulnerableTo` relation (55 asserted triples in v0.6.1).
**Numerator Query:**
```sparql
SELECT DISTINCT ?g WHERE {
  ?g a rice:GrowthStage . ?g rice:vulnerableTo ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?g WHERE { ?g a rice:GrowthStage }
```
**Result:** 6 covered / 7 total (85.7%) — PASS  
**Uncovered entities (1):** `rice:Harvest_Stage`

---

#### CQ-07 | L2 x D1 | negative | PASS (0 violations)
**Question:** Is the stage-vulnerability view consistent with the occurrence view (`vulnerableTo` without matching `occursIn`)?
**Rationale:** Integrity constraint. If stage G is `vulnerableTo` entity E, then E must `occursIn` G.
**Query:**
```sparql
SELECT DISTINCT ?g ?e WHERE {
  ?g a rice:GrowthStage . ?g rice:vulnerableTo ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  FILTER NOT EXISTS { ?e rice:occursIn ?g } }
```
**Result:** 0 violations — PASS. The two ontological views are fully consistent.

---

#### CQ-08 | L2 x D1 | coverage | PASS (2/3 preventive treatments, 67%)
**Question:** Which preventive treatments carry an explicit growth-stage prerequisite for application?
**Rationale:** Operational validity. Preventive advice without stage timing cannot be executed in the field.
**Numerator Query:**
```sparql
SELECT DISTINCT ?t WHERE {
  ?e rice:preventedBy ?t . ?t rice:requires ?g . ?g a rice:GrowthStage }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?t WHERE { ?e rice:preventedBy ?t }
```
**Result (0.7.0-dev):** 2 covered / 3 total (66.7%) — PASS; PARTIAL from a 70% threshold. With three members, one assertion moves the verdict.  
**Uncovered entities (1):** `rice:Seed_Treatment`  
**v0.6.2:** 1/2 (50.0%) — PASS exactly at the threshold.

---

#### CQ-09 | L3 x D1 | coverage | PASS (1/1 declared vector, 100%)
**Question:** For which declared insect vectors is the transmission chain vector -> pathogen -> disease fully traversable?
**Rationale:** Multi-hop epidemiological query measuring vector-pathogen-disease chain completeness.
**Numerator Query:**
```sparql
SELECT DISTINCT ?v WHERE {
  ?v rice:transmits ?p . ?p rice:causes ?d . ?d a rice:Disease }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?v WHERE { ?v rice:transmits ?p }
```
**Detail Query:**
```sparql
SELECT DISTINCT ?v ?p ?d WHERE {
  ?v rice:transmits ?p . ?p rice:causes ?d . ?d a rice:Disease
} ORDER BY ?v
```
**Result:** 1 covered / 1 total (100.0%) — PASS (2 full paths: `Nephotettix_Virescens` -> `RTBV`/`RTSV` -> `Rice_Tungro_Disease`)

---

#### CQ-10 | L3 x D1 | negative | PASS (0 violations)
**Question:** Are there insect vectors for which no control treatment is recorded, leaving the transmission chain unbreakable?
**Rationale:** Actionability. A vector chain that cannot be interrupted has no advisory utility.
**Query:**
```sparql
SELECT DISTINCT ?v WHERE {
  ?v rice:transmits ?p .
  FILTER NOT EXISTS { ?v rice:controlledBy ?t } }
```
**Result:** 0 violations — **PASS**  
**v0.6:** 1 violation — `rice:Nephotettix_Virescens` had no `controlledBy` assertion.  
> **Resolved in v0.6.1, not as planned.** The v0.6 action item was `controlledBy Vector_Control`. Gallagher et al. (2002, FAO/IRC) report that "controlling the vector population with insecticide does not always result in tungro control" and recommend resistant varieties, as does IRRI's tungro fact sheet. v0.6.1 therefore asserts `rice:Nephotettix_Virescens rice:controlledBy rice:Resistant_Variety`, reified with that citation. A CQ is a requirement on the graph, not a licence to assert whatever makes it pass.

---

#### CQ-11 | L3 x D1 | coverage | PASS (10/15 diseases, 67%)
**Question:** For which diseases is the full risk-to-remedy chain traversable: env factor -> disease -> symptom -> treatment?
**Rationale:** Complete 4-hop decision-support path required by advisory applications.
**Numerator Query:**
```sparql
SELECT DISTINCT ?d WHERE {
  ?d a rice:Disease .
  ?f rice:increaseRiskOf ?d . ?f a rice:EnvironmentalFactor .
  ?d rice:indicatedBy ?s . ?s a rice:Symptom .
  ?d rice:controlledBy ?t . ?t a rice:Treatment }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?d WHERE { ?d a rice:Disease }
```
**Result (0.7.0-dev):** 10 covered / 15 total (66.7%) — PASS (293 instantiations); PARTIAL from a 70% threshold  
**Uncovered entities (5):** `Iron_Toxicity_Disorder`, `Nitrogen_Deficiency_Disorder`, `Phosphorus_Deficiency_Disorder`, `Potassium_Deficiency_Disorder`, `Salinity_Disorder` — each lacks at least the control treatment the chain ends in (see CQ-03); zinc deficiency is the one abiotic disorder that completes it.  
**v0.6.2:** 9/9 (100%), 277 instantiations.

---

#### CQ-12 | L3 x D1 | coverage | PARTIAL (9/22 disease/pest, 41%)
**Question:** For which diseases and pests does the KG reach the management layer, i.e. recommend a concrete `ManagementAction`?
**Rationale:** Verifies that diagnostic entities terminate in operational management actions.
**Numerator Query:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:recommends ?m . ?m a rice:ManagementAction }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```
**Result (0.7.0-dev):** 9 covered / 22 total (40.9%) — **PARTIAL**  
**Uncovered entities (13):** `Armyworm`, `Brown_Planthopper`, `Leaf_Folder`, `Nephotettix_Virescens`, `Rice_Bug`, `Sheath_Blight`, `Stem_Borer`, the four nutrient-deficiency disorders (`Nitrogen_`, `Phosphorus_`, `Potassium_`, `Zinc_Deficiency_Disorder`), `Iron_Toxicity_Disorder` and `Salinity_Disorder`.  
**Why it fell:** the numerator is unchanged; the denominator grew by the six abiotic disorders added from the IRRI nutrient and toxicity fact sheets, which give fertilizer or water guidance but no ManagementAction (monitoring, intervention, …). No `recommends` was added to clear the threshold.  
**v0.6.2:** 9/16 (56.2%) — PASS, uncovered `Armyworm`, `Brown_Planthopper`, `Leaf_Folder`, `Nephotettix_Virescens`, `Rice_Bug`, `Sheath_Blight`, `Stem_Borer`.

---

#### CQ-13 | L2 x D1 | coverage | FAIL (0/4 severity levels, 0%)
**Question:** Does every severity level map to a recommended management action, ensuring total triage coverage?
**Rationale:** Severity-driven triage completeness.
**Numerator Query:**
```sparql
SELECT DISTINCT ?sev WHERE { ?sev a rice:SeverityLevel . ?sev rice:recommends ?m }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?sev WHERE { ?sev a rice:SeverityLevel }
```
**Result (0.7.0-dev):** 0 covered / 4 total (0.0%) — **FAIL**  
**Why it fails:** the six `recommends` links from severity levels to actions cited "BBPOPT (2022)", a guideline that was never found. The two official Indonesian pest-observation juknis (2018, 2021) define the attack-intensity categories ringan/sedang/berat/puso but map none of them to an action, and the 2021 version places *ringan* above the control threshold, contradicting `Low_Severity recommends No_Action_Needed`. The links were removed on 2026-09-15 rather than kept under an unverifiable citation. They are open questions for the domain expert; a confirmed mapping would be re-added as `expert-elicited`. The CQ text and queries are unchanged.  
**v0.6.2:** 4/4 (100%) — PASS, on the unverified links.

---

#### CQ-14 | L4 x D1 | entailment | PASS (0 asserted -> 1,442 entailed)
**Question:** Which observations are `SymptomaticObservation`s (defined class: *Observation that captures some Symptom*)?
**Rationale:** Proves that OWL RL axiomatisation derives inferences that cannot be retrieved by SPARQL alone.
**Query:**
```sparql
SELECT DISTINCT ?o WHERE { ?o a rice:SymptomaticObservation }
```
**Result:** 0 on asserted graph -> **1,442 on materialised graph (+1,442 gain)** — PASS

---

#### CQ-15 | L4 x D1 | entailment | PASS (0 asserted -> 170 entailed)
**Question:** Can the KG be queried in the inverse direction (e.g. `causedBy`, `indicates`, `controls`) via OWL inverse inference?
**Rationale:** Robustness under bidirectional query formulations without duplicate manual assertions.
**Query:**
```sparql
SELECT ?x ?y WHERE {
  { ?x rice:causedBy ?y } UNION { ?x rice:indicates ?y } UNION
  { ?x rice:hasOccurrenceOf ?y } UNION { ?x rice:controls ?y } }
```
**Result (0.7.0-dev):** 0 on asserted graph -> **170 on materialised graph (+170 gain)** — PASS; the gain grows with the 0.7.0-dev assertions on properties that have a declared inverse. **v0.6.1/v0.6.2:** 134 (v0.6: 133; the added `controlledBy` contributes one `controls` inverse).

---

### Section B: Multimodal Integration Layer (D2)

#### CQ-16 | L3 x D2 | coverage | PASS (8,643/8,643 images, 100%)
**Question:** Which image observations can be grounded to agronomic recommendations: image -> class -> symptom & treatment?
**Rationale:** Core multimodal grounding. Denominator restricted to images labelled with Disease or Pest.
**Numerator Query:**
```sparql
SELECT DISTINCT ?img WHERE {
  ?img a rice:ImageObservation . ?img rice:annotatedAs ?e .
  ?e rice:indicatedBy ?s . ?e rice:controlledBy ?t }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?img WHERE {
  ?img a rice:ImageObservation . ?img rice:annotatedAs ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```
**Result:** 8,643 covered / 8,643 total (100.0%) — PASS

---

#### CQ-17 | L2 x D2 | coverage | PASS (10/10 classes, 100%)
**Question:** Which annotated classes of the image corpus are typed as domain entities (Disease, Pest, or HealthStatus)?
**Rationale:** Reconciles image dataset labels with the ontology schema.
**Numerator Query:**
```sparql
SELECT DISTINCT ?e WHERE {
  ?img rice:annotatedAs ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest } UNION { ?e a rice:HealthStatus } }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?e WHERE { ?img rice:annotatedAs ?e }
```
**Result:** 10 covered / 10 total (100.0%) — PASS

---

#### CQ-18 | L1 x D2 | coverage | PARTIAL (1/39 symptoms, 3%)
**Question:** Which symptoms are grounded in direct visual evidence (`captures` relation)?
**Rationale:** Distinguishes an MMKG from a text ontology with images attached. Highlights the symptom-level grounding gap.
**Numerator Query:**
```sparql
SELECT DISTINCT ?s WHERE { ?s a rice:Symptom . ?o rice:captures ?s }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?s WHERE { ?s a rice:Symptom }
```
**Result (0.7.0-dev):** 1 covered / 39 total (2.6%) — **PARTIAL** (grounded symptom: `Dead_Tiller`); the denominator grew with the 12 abiotic-disorder symptoms. **v0.6.2:** 1/27 (3.7%).  
> **Roadmap Target (Phase 3):** Populate per-symptom visual annotations for the remaining 38 symptoms, from the expert image annotation.

---

#### CQ-19 | L1 x D2 | negative | PASS (0 violations)
**Question:** Are there image observations lacking a content URL or a source dataset provenance link?
**Rationale:** Media layer integrity constraint.
**Query:**
```sparql
SELECT ?img WHERE {
  ?img a rice:ImageObservation .
  FILTER ( NOT EXISTS { ?img schema:contentUrl ?u } ||
           NOT EXISTS { ?img prov:wasDerivedFrom ?ds } ) }
```
**Result:** 0 violations — PASS (all 10,407 images fully attributed).

---

#### CQ-20 | L1 x D2 | documented | DOCUMENTED (0 sensor observations)
**Question:** How many sensor observations does the KG contain?
**Rationale:** Declared extension point for IoT/weather telemetry in Phase 3.
**Query:**
```sparql
SELECT DISTINCT ?o WHERE { ?o a rice:SensorObservation }
```
**Result:** 0 individuals — DOCUMENTED (extension point recorded).

---

### Section C: Provenance & Alignment Layer (D3)

#### CQ-21 | L4 x D3 | coverage | PASS (348/348 axioms, 100%)
**Question:** Which reified domain assertions carry both an authoritative source URI and a bibliographic citation?
**Rationale:** Scientific defensibility & provenance completeness.
**Scope limit:** the denominator is the set of axioms, so CQ-21 measures whether existing axioms carry a source — never whether every assertion has an axiom. An unreified assertion is invisible to it; CQ-22 covers that case.
**Numerator Query:**
```sparql
SELECT DISTINCT ?ax WHERE {
  ?ax a owl:Axiom ; dcterms:source ?src ; dcterms:bibliographicCitation ?cit }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?ax WHERE { ?ax a owl:Axiom }
```
**Result:** 348 covered / 348 total (100.0%) — PASS. Source URIs by host: CABI (doi.org) 242, IRRI Rice Knowledge Bank 89, Mackill & Khush 2018 (doi.org) 3, AGROVOC 4, IRAC 2, Plant Ontology 2, Wang et al. 2022 (doi.org) 2, Bagariang et al. 2021 (doi.org) 2, Biswas et al. 2021 (doi.org) 1, FAO 1. The 15 `ResistanceAssessment` individuals are not axioms and are outside this count; CQ-22 checks them. BBPOPT 0 (the 7 BBPOPT axioms of v0.6.2 were removed or re-sourced in 0.7.0-dev).  
**v0.6.2:** 256/256 (CABI 242, BBPOPT 7, IRRI 4, IRAC 2, FAO 1).  
**v0.6:** 253/253 (100%) — which hid the two unreified `Stem_Borer` assertions reported by CQ-22.

---

#### CQ-22 | L4 x D3 | negative | PASS (0 violations)
**Question:** Are there domain assertions with missing or incomplete provenance — either no reified axiom at all, or an axiom missing its source, citation or evidence type?
**Rationale:** Integrity constraint complementing CQ-21. **Extended 2026-09-14.** The original form (below) inspected only axioms that exist, so an assertion with no axiom was invisible to both provenance CQs. Runs on the asserted graph: materialised inverses are never reified and would all count as violations. **Extended again 2026-09-17:** a third branch reports `ResistanceAssessment` individuals missing their source, citation or evidence type, because an assessment carries its provenance on itself; `rice:varietyOf` is in the property list, and `rice:resistantTo`/`rice:moderatelyResistantTo` left it with the properties themselves.
**Query (current):**
```sparql
SELECT ?item ?problem WHERE {
  {
    ?item a owl:Axiom .
    FILTER ( NOT EXISTS { ?item dcterms:source ?s } ||
             NOT EXISTS { ?item dcterms:bibliographicCitation ?c } ||
             NOT EXISTS { ?item rice:evidenceType ?e } )
    BIND ("axiom with incomplete provenance" AS ?problem)
  } UNION {
    VALUES ?p { rice:causes rice:transmits rice:indicatedBy rice:occursIn
                rice:controlledBy rice:preventedBy rice:increaseRiskOf
                rice:vulnerableTo rice:recommends rice:requires
                rice:affectsPlantPart rice:partOf rice:hasTransmissionMode
                rice:hasManagementCategory rice:varietyOf }
    ?s ?p ?o .
    FILTER NOT EXISTS { ?ax owl:annotatedSource ?s ;
                            owl:annotatedProperty ?p ;
                            owl:annotatedTarget ?o }
    BIND (CONCAT(STRAFTER(STR(?s), "#"), " ", STRAFTER(STR(?p), "#"), " ",
                 STRAFTER(STR(?o), "#")) AS ?item)
    BIND ("assertion without provenance" AS ?problem)
  } UNION {
    ?a a rice:ResistanceAssessment .
    FILTER ( NOT EXISTS { ?a dcterms:source ?s } ||
             NOT EXISTS { ?a dcterms:bibliographicCitation ?c } ||
             NOT EXISTS { ?a rice:evidenceType ?e } )
    BIND (STRAFTER(STR(?a), "#") AS ?item)
    BIND ("assessment with incomplete provenance" AS ?problem)
  }
}
```
**Query (original, v0.6):**
```sparql
SELECT ?ax WHERE {
  ?ax a owl:Axiom .
  FILTER ( NOT EXISTS { ?ax dcterms:source ?s } ||
           NOT EXISTS { ?ax dcterms:bibliographicCitation ?c } ||
           NOT EXISTS { ?ax rice:evidenceType ?e } ) }
```
**Result:** 0 violations — PASS. `rice:affectsPlantPart`, `rice:partOf`, `rice:hasTransmissionMode` and `rice:hasManagementCategory` were added to the property list in 0.7.0-dev together with the properties themselves.  
**Assessment branch (2026-09-17):** 0 violations on 0.7.0-dev; a control copy with the `dcterms:source` of `RA_Inpari_33_Brown_Planthopper_Java_2021` removed reports exactly that assessment.  
**On the released v0.6 file:** original query 0 violations (PASS); current query **2 violations (FAIL)** — `Stem_Borer indicatedBy Dead_Tiller` and `Stem_Borer indicatedBy White_Ear`, both reified in v0.6.1 citing IRAC (2025). Both results are reported; the original is not retracted.

---

#### CQ-23 | L4 x D3 | coverage | PASS (19/31 entities, 61%)
**Question:** Which biological entities are aligned to external vocabularies (EPPO, AGROVOC, or NCBI Taxonomy)?
**Rationale:** Semantic interoperability & FAIR data compliance.
**Numerator Query:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pathogen } UNION { ?e a rice:Pest }
  { ?e rice:eppoCode ?c } UNION { ?e skos:exactMatch ?m } UNION { ?e skos:closeMatch ?m2 } }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pathogen } UNION { ?e a rice:Pest } }
```
**Result (0.7.0-dev):** 19 covered / 31 total (61.3%) — PASS; PARTIAL from a 70% threshold. `Rhizoctonia_Solani` (2026-09-17) entered covered, with EPPO, AGROVOC and NCBI identifiers; before it, 18/30.  
**Uncovered entities (12):** `Bacterial_Leaf_Blight`, `Bacterial_Leaf_Streak`, `Bacterial_Panicle_Blight`, `Brown_Spot`, `Deadheart`, `Sheath_Blight`, and the six abiotic disorders (`Iron_Toxicity_Disorder`, `Nitrogen_Deficiency_Disorder`, `Phosphorus_Deficiency_Disorder`, `Potassium_Deficiency_Disorder`, `Salinity_Disorder`, `Zinc_Deficiency_Disorder`), which carry no `eppoCode`, `skos:exactMatch` or `skos:closeMatch`  
**v0.6.2:** 18/24 (75.0%), the first six uncovered.

---

#### CQ-24 | L4 x D3 | negative | PASS (0 violations)
**Question:** Are annotation literals lexically consistent, i.e. is `rice:evidenceType` uniformly language-tagged?
**Rationale:** Literal hygiene. Untagged strings break `lang()` filters and split SPARQL `GROUP BY` aggregations.
**Query:**
```sparql
SELECT ?ax ?v WHERE {
  ?ax rice:evidenceType ?v . FILTER ( lang(?v) = "" ) }
```
**Result:** 0 violations — **PASS**.  
**v0.6:** 1 violation — the axiom on `Crop_Sanitation requires Harvest_Stage` carried an untagged `"literature-curated"`. Tagged `@en` in v0.6.1; it was the only untagged literal, so no other axiom changed.

---

#### CQ-25 | L4 x D1 | negative | PASS (0 violations)
**Question:** Under entailment, is any individual typed as both a `Symptom` and a `Disease`?
**Rationale:** Category discipline and class disjointness. In v0.5 this failed due to `Deadheart`. In v0.6, `Deadheart` is disambiguated as Disease and `Dead_Tiller` as Symptom, resolving the conflict completely.
**Query (executed on OWL RL materialised graph):**
```sparql
SELECT DISTINCT ?x WHERE {
  ?x a rice:Symptom . ?x a rice:Disease }
```
**Result:** 0 violations — **PASS** (Zero class disjointness conflicts under full entailment).

---

## Action Items & Roadmap Summary (0.7.0-dev)

| CQ ID | Status | Finding / Issue | Corrective Action / Milestone |
|:---:|:---:|---|---|
| **CQ-25** | ✅ **RESOLVED** | `Deadheart` typed as Symptom & Disease | Resolved in v0.6 (`Deadheart` as Disease, `Dead_Tiller` as Symptom) |
| **CQ-10** | ✅ **RESOLVED** | `Nephotettix_Virescens` lacked a control treatment | v0.6.1: `controlledBy Resistant_Variety`, citing Gallagher et al. (2002) — not the planned `Vector_Control`, which the literature does not support for tungro |
| **CQ-22** | ✅ **RESOLVED** | Extended query found 2 domain assertions with no provenance axiom | v0.6.1: `Stem_Borer indicatedBy Dead_Tiller` / `White_Ear` reified, citing IRAC (2025) |
| **CQ-24** | ✅ **RESOLVED** | One untagged literal on `rice:evidenceType` | v0.6.1: tagged `"literature-curated"@en` |
| **CQ-12** | ⚠️ **PARTIAL**| 9/22 after the six abiotic disorders (four deficiencies, iron toxicity, salinity) entered the denominator (0.7.0-dev) | Add `recommends` only where a source states a management action for the disorder; not added to clear the threshold |
| **CQ-01** | ✅ **CORRECTED** | Numerator counted abiotic causes as pathogens once `AbioticFactor` could `causes` | 0.7.0-dev: numerator requires `?p a rice:Pathogen`; denominator excludes diseases with an `AbioticFactor` cause (7/9, PASS; uncorrected 7/15). Sheath blight's pathogen added 2026-09-17: 8/9 (uncorrected 8/15) |
| **CQ-18** | ⚠️ **PARTIAL**| Only 1/39 symptoms visually grounded | Annotate image dataset at symptom level (`captures` relation) (Phase 3) |
| **CQ-20** | 📋 **DOC** | 0 sensor observations | Ingest IoT sensor telemetry as `SensorObservation` instances (Phase 3) |

---
