# Rice MMKG v0.6.2 — SPARQL Competency Question Documentation

**Ontology:** `Rice MMKG.rdf` (owl:versionInfo 0.6.2; results identical to v0.6.1, which differs only in source URIs and citation text)  
**Triples:** 66,802 asserted / 161,447 after OWL RL materialisation (+94,645 triples)  
**Benchmark Execution:** 2026-09-14  
**Overall Result:** 23 PASS / 1 PARTIAL / 0 FAIL / 1 DOCUMENTED (24 scored + 1 documented = 25 CQs)
**Pass Rate:** 95.8% (23/24 scored CQs)

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
PREFIX rice:    <http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#>
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

---

## Master Result Matrix (25 Competency Questions — v0.6.1)

| CQ ID | Depth | Dim | Mode | Result | Measurement | Summary |
|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **CQ-01** | L1 | D1 | `coverage`   | **PASS**       | 7/9 (78%)            | Rice diseases with causal pathogens |
| **CQ-02** | L1 | D1 | `coverage`   | **PASS**       | 15/16 (94%)          | Diseases/pests with observable symptoms |
| **CQ-03** | L1 | D1 | `coverage`   | **PASS**       | 16/16 (100%)         | Diseases/pests with control treatments (v0.6: 15/16) |
| **CQ-04** | L1 | D1 | `coverage`   | **PASS**       | 27/27 (100%)         | Symptoms attached to domain entities (zero orphan) |
| **CQ-05** | L2 | D1 | `coverage`   | **PASS**       | 13/16 (81%)          | Co-occurrence: Growth stage + Env. risk factor (88 pairs) |
| **CQ-06** | L2 | D1 | `coverage`   | **PASS**       | 6/7 (86%)            | Growth stages with vulnerability profiles (`vulnerableTo`) |
| **CQ-07** | L2 | D1 | `negative`   | **PASS**       | 0 violations         | Consistency between `vulnerableTo` and `occursIn` |
| **CQ-08** | L2 | D1 | `coverage`   | **PASS**       | 1/2 (50%)            | Preventive treatments with growth-stage prerequisites |
| **CQ-09** | L3 | D1 | `coverage`   | **PASS**       | 1/1 (100%)           | Vector transmission chain: vector -> pathogen -> disease |
| **CQ-10** | L3 | D1 | `negative`   | **PASS**       | 0 violations         | Vectors without control treatments (v0.6: 1, `Nephotettix_Virescens`) |
| **CQ-11** | L3 | D1 | `coverage`   | **PASS**       | 9/9 (100%)           | End-to-end DSS chain: env -> disease -> symptom -> treatment |
| **CQ-12** | L3 | D1 | `coverage`   | **PASS**       | 9/16 (56%)           | Diseases/pests recommending concrete `ManagementAction` |
| **CQ-13** | L2 | D1 | `coverage`   | **PASS**       | 4/4 (100%)           | Total triage: Every `SeverityLevel` maps to an action |
| **CQ-14** | L4 | D1 | `entailment` | **PASS**       | 0 -> 1,442 rows      | OWL classification: `SymptomaticObservation` defined class |
| **CQ-15** | L4 | D1 | `entailment` | **PASS**       | 0 -> 134 rows        | Bidirectional query capability via inverse properties (v0.6: 133) |
| **CQ-16** | L3 | D2 | `coverage`   | **PASS**       | 8,643/8,643 (100%)   | Multimodal grounding: Image -> Class -> Symptom & Treatment |
| **CQ-17** | L2 | D2 | `coverage`   | **PASS**       | 10/10 (100%)         | Dataset annotation labels typed as OWL domain classes |
| **CQ-18** | L1 | D2 | `coverage`   | **PARTIAL**    | 1/27 (4%)            | Direct visual grounding of symptoms (`rice:captures`) |
| **CQ-19** | L1 | D2 | `negative`   | **PASS**       | 0 violations         | Media layer integrity: Content URL & dataset provenance |
| **CQ-20** | L1 | D2 | `documented` | **DOC**        | 0 individuals        | Sensor observation population (Phase 3 extension point) |
| **CQ-21** | L4 | D3 | `coverage`   | **PASS**       | 256/256 (100%)       | Reified domain axioms with source URI and citation (v0.6: 253/253) |
| **CQ-22** | L4 | D3 | `negative`   | **PASS**       | 0 violations         | Domain assertions without an axiom, or axioms with incomplete provenance (extended 2026-09-14; v0.6: 2) |
| **CQ-23** | L4 | D3 | `coverage`   | **PASS**       | 18/24 (75%)          | Biological entities aligned to EPPO / AGROVOC / NCBI |
| **CQ-24** | L4 | D3 | `negative`   | **PASS**       | 0 violations         | Literal hygiene: Uniform language tags (`@en`) on `evidenceType` (v0.6: 1) |
| **CQ-25** | L4 | D1 | `negative`   | **PASS**       | 0 violations         | Class disjointness: Entailed overlap between `Symptom` & `Disease` |

---

## Detailed CQ Specifications & SPARQL Queries

### Section A: Agronomic / Symbolic Domain (D1)

#### CQ-01 | L1 x D1 | coverage | PASS (7/9 diseases, 78%)
**Question:** Which rice diseases have an identified causal pathogen?
**Rationale:** Aetiological completeness. A disease without a causal agent cannot support downstream causal inference.
**Numerator Query:**
```sparql
SELECT DISTINCT ?d WHERE { ?d a rice:Disease . ?p rice:causes ?d }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?d WHERE { ?d a rice:Disease }
```
**Result:** 7 covered / 9 total (77.8%) — PASS (threshold 50%)  
**Uncovered entities (2):** `rice:Deadheart`, `rice:Sheath_Blight`

---

#### CQ-02 | L1 x D1 | coverage | PASS (15/16 disease/pest, 94%)
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
**Result:** 15 covered / 16 total (93.8%) — PASS  
**Uncovered entities (1):** `rice:Nephotettix_Virescens`

---

#### CQ-03 | L1 x D1 | coverage | PASS (16/16 disease/pest, 100%)
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
**Result:** 16 covered / 16 total (100.0%) — PASS  
**v0.6:** 15/16 (93.8%), uncovered `rice:Nephotettix_Virescens`; closed in v0.6.1 by `controlledBy Resistant_Variety` (see CQ-10).

---

#### CQ-04 | L1 x D1 | coverage | PASS (27/27 symptoms, 100%)
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
**Result:** 27 covered / 27 total (100.0%) — PASS. Zero orphan vocabulary.

---

#### CQ-05 | L2 x D1 | coverage | PASS (13/16 disease/pest, 81%)
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
**Result:** 13 covered / 16 total (81.2%) — PASS (88 instantiations)  
**Uncovered entities (3):** `rice:Leaf_Folder`, `rice:Nephotettix_Virescens`, `rice:Rice_Bug`

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

#### CQ-08 | L2 x D1 | coverage | PASS (1/2 preventive treatments, 50%)
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
**Result:** 1 covered / 2 total (50.0%) — PASS  
**Uncovered entities (1):** `rice:Seed_Treatment`

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

#### CQ-11 | L3 x D1 | coverage | PASS (9/9 diseases, 100%)
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
**Result:** 9 covered / 9 total (100.0%) — PASS (277 instantiations)

---

#### CQ-12 | L3 x D1 | coverage | PASS (9/16 disease/pest, 56%)
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
**Result:** 9 covered / 16 total (56.2%) — PASS  
**Uncovered entities (7):** `Armyworm`, `Brown_Planthopper`, `Leaf_Folder`, `Nephotettix_Virescens`, `Rice_Bug`, `Sheath_Blight`, `Stem_Borer`

---

#### CQ-13 | L2 x D1 | coverage | PASS (4/4 severity levels, 100%)
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
**Result:** 4 covered / 4 total (100.0%) — PASS

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

#### CQ-15 | L4 x D1 | entailment | PASS (0 asserted -> 134 entailed)
**Question:** Can the KG be queried in the inverse direction (e.g. `causedBy`, `indicates`, `controls`) via OWL inverse inference?
**Rationale:** Robustness under bidirectional query formulations without duplicate manual assertions.
**Query:**
```sparql
SELECT ?x ?y WHERE {
  { ?x rice:causedBy ?y } UNION { ?x rice:indicates ?y } UNION
  { ?x rice:hasOccurrenceOf ?y } UNION { ?x rice:controls ?y } }
```
**Result:** 0 on asserted graph -> **134 on materialised graph (+134 gain)** — PASS (v0.6: 133; the added `controlledBy` contributes one `controls` inverse)

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

#### CQ-18 | L1 x D2 | coverage | PARTIAL (1/27 symptoms, 4%)
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
**Result:** 1 covered / 27 total (3.7%) — **PARTIAL** (grounded symptom: `Dead_Tiller`)  
> **Roadmap Target (Phase 3):** Populate per-symptom visual annotations for the remaining 26 symptoms.

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

#### CQ-21 | L4 x D3 | coverage | PASS (256/256 axioms, 100%)
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
**Result:** 256 covered / 256 total (100.0%) — PASS. Source URIs by host: CABI 242, BBPOPT 7, IRRI 4, IRAC 2, FAO 1.  
**v0.6:** 253/253 (100%) — which hid the two unreified `Stem_Borer` assertions reported by CQ-22.

---

#### CQ-22 | L4 x D3 | negative | PASS (0 violations)
**Question:** Are there domain assertions with missing or incomplete provenance — either no reified axiom at all, or an axiom missing its source, citation or evidence type?
**Rationale:** Integrity constraint complementing CQ-21. **Extended 2026-09-14.** The original form (below) inspected only axioms that exist, so an assertion with no axiom was invisible to both provenance CQs. Runs on the asserted graph: materialised inverses are never reified and would all count as violations.
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
                rice:vulnerableTo rice:recommends rice:requires }
    ?s ?p ?o .
    FILTER NOT EXISTS { ?ax owl:annotatedSource ?s ;
                            owl:annotatedProperty ?p ;
                            owl:annotatedTarget ?o }
    BIND (CONCAT(STRAFTER(STR(?s), "#"), " ", STRAFTER(STR(?p), "#"), " ",
                 STRAFTER(STR(?o), "#")) AS ?item)
    BIND ("assertion without provenance" AS ?problem)
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
**Result:** 0 violations — PASS.  
**On the released v0.6 file:** original query 0 violations (PASS); current query **2 violations (FAIL)** — `Stem_Borer indicatedBy Dead_Tiller` and `Stem_Borer indicatedBy White_Ear`, both reified in v0.6.1 citing IRAC (2025). Both results are reported; the original is not retracted.

---

#### CQ-23 | L4 x D3 | coverage | PASS (18/24 entities, 75%)
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
**Result:** 18 covered / 24 total (75.0%) — PASS  
**Uncovered entities (6):** `Bacterial_Leaf_Blight`, `Bacterial_Leaf_Streak`, `Bacterial_Panicle_Blight`, `Brown_Spot`, `Deadheart`, `Sheath_Blight`

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

## Action Items & Roadmap Summary (v0.6.1)

| CQ ID | Status | Finding / Issue | Corrective Action / Milestone |
|:---:|:---:|---|---|
| **CQ-25** | ✅ **RESOLVED** | `Deadheart` typed as Symptom & Disease | Resolved in v0.6 (`Deadheart` as Disease, `Dead_Tiller` as Symptom) |
| **CQ-10** | ✅ **RESOLVED** | `Nephotettix_Virescens` lacked a control treatment | v0.6.1: `controlledBy Resistant_Variety`, citing Gallagher et al. (2002) — not the planned `Vector_Control`, which the literature does not support for tungro |
| **CQ-22** | ✅ **RESOLVED** | Extended query found 2 domain assertions with no provenance axiom | v0.6.1: `Stem_Borer indicatedBy Dead_Tiller` / `White_Ear` reified, citing IRAC (2025) |
| **CQ-24** | ✅ **RESOLVED** | One untagged literal on `rice:evidenceType` | v0.6.1: tagged `"literature-curated"@en` |
| **CQ-18** | ⚠️ **PARTIAL**| Only 1/27 symptoms visually grounded | Annotate image dataset at symptom level (`captures` relation) (Phase 3) |
| **CQ-20** | 📋 **DOC** | 0 sensor observations | Ingest IoT sensor telemetry as `SensorObservation` instances (Phase 3) |

---
