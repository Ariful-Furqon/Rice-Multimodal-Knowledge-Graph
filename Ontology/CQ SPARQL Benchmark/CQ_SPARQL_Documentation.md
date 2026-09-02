# Rice MMKG v0.5 — SPARQL Competency Question Documentation

**Ontology:** `Rice MMKG.rdf` (owl:versionInfo 0.5)  
**Triples:** 66,873 asserted / 158,685 after OWL RL materialisation (+91,812 triples)  
**Benchmark Execution:** 2026-09-02  
**Overall Result:** 20 PASS / 1 PARTIAL / 3 FAIL / 1 DOCUMENTED (24 scored + 1 documented = 25 CQs)

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

## Master Result Matrix (25 Competency Questions)

| CQ ID | Depth | Dim | Mode | Result | Measurement | Summary |
|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **CQ-01** | L1 | D1 | `coverage`   | **PASS**       | 7/9 (78%)            | Rice diseases with causal pathogens |
| **CQ-02** | L1 | D1 | `coverage`   | **PASS**       | 15/16 (94%)          | Diseases/pests with observable symptoms |
| **CQ-03** | L1 | D1 | `coverage`   | **PASS**       | 15/16 (94%)          | Diseases/pests with control treatments |
| **CQ-04** | L1 | D1 | `coverage`   | **PASS**       | 28/28 (100%)         | Symptoms attached to domain entities (zero orphan) |
| **CQ-05** | L2 | D1 | `coverage`   | **PASS**       | 13/16 (81%)          | Co-occurrence: Growth stage + Env. risk factor (88 pairs) |
| **CQ-06** | L2 | D1 | `coverage`   | **PASS**       | 6/7 (86%)            | Growth stages with vulnerability profiles (`vulnerableTo`) |
| **CQ-07** | L2 | D1 | `negative`   | **PASS**       | 0 violations         | Consistency between `vulnerableTo` and `occursIn` |
| **CQ-08** | L2 | D1 | `coverage`   | **PASS**       | 1/2 (50%)            | Preventive treatments with growth-stage prerequisites |
| **CQ-09** | L3 | D1 | `coverage`   | **PASS**       | 1/1 (100%)           | Vector transmission chain: vector -> pathogen -> disease |
| **CQ-10** | L3 | D1 | `negative`   | **FAIL**       | 1 violation          | Vectors without control treatments (`Nephotettix_Virescens`) |
| **CQ-11** | L3 | D1 | `coverage`   | **PASS**       | 9/9 (100%)           | End-to-end DSS chain: env -> disease -> symptom -> treatment |
| **CQ-12** | L3 | D1 | `coverage`   | **PASS**       | 9/16 (56%)           | Diseases/pests recommending concrete `ManagementAction` |
| **CQ-13** | L2 | D1 | `coverage`   | **PASS**       | 4/4 (100%)           | Total triage: Every `SeverityLevel` maps to an action |
| **CQ-14** | L4 | D1 | `entailment` | **PASS**       | 0 -> 1,442 rows      | OWL classification: `SymptomaticObservation` defined class |
| **CQ-15** | L4 | D1 | `entailment` | **PASS**       | 0 -> 139 rows        | Bidirectional query capability via inverse properties |
| **CQ-16** | L3 | D2 | `coverage`   | **PASS**       | 8,643/8,643 (100%)   | Multimodal grounding: Image -> Class -> Symptom & Treatment |
| **CQ-17** | L2 | D2 | `coverage`   | **PASS**       | 10/10 (100%)         | Dataset annotation labels typed as OWL domain classes |
| **CQ-18** | L1 | D2 | `coverage`   | **PARTIAL**    | 1/28 (4%)            | Direct visual grounding of symptoms (`rice:captures`) |
| **CQ-19** | L1 | D2 | `negative`   | **PASS**       | 0 violations         | Media layer integrity: Content URL & dataset provenance |
| **CQ-20** | L1 | D2 | `documented` | **DOC**        | 0 individuals        | Sensor observation population (Phase 3 extension point) |
| **CQ-21** | L4 | D3 | `coverage`   | **PASS**       | 265/265 (100%)       | Reified domain axioms with source URI and citation |
| **CQ-22** | L4 | D3 | `negative`   | **PASS**       | 0 violations         | Reified axioms with incomplete provenance metadata |
| **CQ-23** | L4 | D3 | `coverage`   | **PASS**       | 18/24 (75%)          | Biological entities aligned to EPPO / AGROVOC / NCBI |
| **CQ-24** | L4 | D3 | `negative`   | **FAIL**       | 1 violation          | Literal hygiene: Uniform language tags (`@en`) on `evidenceType` |
| **CQ-25** | L4 | D1 | `negative`   | **FAIL**       | 1 violation          | Class disjointness: Entailed overlap between `Symptom` & `Disease` |

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

#### CQ-03 | L1 x D1 | coverage | PASS (15/16 disease/pest, 94%)
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
**Result:** 15 covered / 16 total (93.8%) — PASS  
**Uncovered entities (1):** `rice:Nephotettix_Virescens`

---

#### CQ-04 | L1 x D1 | coverage | PASS (28/28 symptoms, 100%)
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
**Result:** 28 covered / 28 total (100.0%) — PASS. Zero orphan vocabulary.

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
**Rationale:** Exercises the `vulnerableTo` relation (59 asserted triples in the KG).
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

#### CQ-10 | L3 x D1 | negative | FAIL (1 violation)
**Question:** Are there insect vectors for which no control treatment is recorded, leaving the transmission chain unbreakable?
**Rationale:** Actionability. A vector chain that cannot be interrupted has no advisory utility.
**Query:**
```sparql
SELECT DISTINCT ?v WHERE {
  ?v rice:transmits ?p .
  FILTER NOT EXISTS { ?v rice:controlledBy ?t } }
```
**Result:** 1 violation — **FAIL**  
**Violating Entity:** `rice:Nephotettix_Virescens` has no `controlledBy` assertion.  
> **Action Item:** Add `rice:Nephotettix_Virescens rice:controlledBy rice:Vector_Control`.

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

#### CQ-15 | L4 x D1 | entailment | PASS (0 asserted -> 139 entailed)
**Question:** Can the KG be queried in the inverse direction (e.g. `causedBy`, `indicates`, `controls`) via OWL inverse inference?
**Rationale:** Robustness under bidirectional query formulations without duplicate manual assertions.
**Query:**
```sparql
SELECT ?x ?y WHERE {
  { ?x rice:causedBy ?y } UNION { ?x rice:indicates ?y } UNION
  { ?x rice:hasOccurrenceOf ?y } UNION { ?x rice:controls ?y } }
```
**Result:** 0 on asserted graph -> **139 on materialised graph (+139 gain)** — PASS

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

#### CQ-18 | L1 x D2 | coverage | PARTIAL (1/28 symptoms, 4%)
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
**Result:** 1 covered / 28 total (3.6%) — **PARTIAL**  
> **Roadmap Target (Phase 3):** Populate per-symptom visual annotations for the remaining 27 symptoms.

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

#### CQ-21 | L4 x D3 | coverage | PASS (265/265 axioms, 100%)
**Question:** Which reified domain assertions carry both an authoritative source URI and a bibliographic citation?
**Rationale:** Scientific defensibility & provenance completeness.
**Numerator Query:**
```sparql
SELECT DISTINCT ?ax WHERE {
  ?ax a owl:Axiom ; dcterms:source ?src ; dcterms:bibliographicCitation ?cit }
```
**Denominator Query:**
```sparql
SELECT DISTINCT ?ax WHERE { ?ax a owl:Axiom }
```
**Result:** 265 covered / 265 total (100.0%) — PASS (CABI: 248, IRRI: 11, BBPOPT: 7).

---

#### CQ-22 | L4 x D3 | negative | PASS (0 violations)
**Question:** Are there reified axioms with incomplete provenance (missing source, citation, or evidence type)?
**Rationale:** Integrity constraint complementing CQ-21.
**Query:**
```sparql
SELECT ?ax WHERE {
  ?ax a owl:Axiom .
  FILTER ( NOT EXISTS { ?ax dcterms:source ?s } ||
           NOT EXISTS { ?ax dcterms:bibliographicCitation ?c } ||
           NOT EXISTS { ?ax rice:evidenceType ?e } ) }
```
**Result:** 0 violations — PASS.

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

#### CQ-24 | L4 x D3 | negative | FAIL (1 violation)
**Question:** Are annotation literals lexically consistent, i.e. is `rice:evidenceType` uniformly language-tagged?
**Rationale:** Literal hygiene. Untagged strings break `lang()` filters and split SPARQL `GROUP BY` aggregations.
**Query:**
```sparql
SELECT ?ax ?v WHERE {
  ?ax rice:evidenceType ?v . FILTER ( lang(?v) = "" ) }
```
**Result:** 1 violation — **FAIL** (`Nbfaed4dbd...` literal `"literature-curated"` lacks `@en`).  
> **Action Item:** Replace bare literals with `"literature-curated"@en` across all 265 axioms.

---

#### CQ-25 | L4 x D1 | negative | FAIL (1 violation)
**Question:** Under entailment, is any individual typed as both a `Symptom` and a `Disease`?
**Rationale:** Category discipline and class disjointness.
**Query (executed on OWL RL materialised graph):**
```sparql
SELECT DISTINCT ?x WHERE {
  ?x a rice:Symptom . ?x a rice:Disease }
```
**Result:** 1 violation — **FAIL** (`rice:Deadheart` inferred as both Symptom and Disease).  
> **Action Item:** Rename symptom individual to `rice:Deadheart_Symptom` and keep `rice:Deadheart` typed as Disease only.

---

## Action Items & Roadmap Summary

| CQ ID | Finding / Issue | Corrective Action / Milestone |
|:---:|---|---|
| **CQ-10** | `Nephotettix_Virescens` lacks control treatment | Add `rice:Nephotettix_Virescens rice:controlledBy rice:Vector_Control` (v0.5.1 fix) |
| **CQ-24** | Untagged literal on `rice:evidenceType` | Update literal to `"literature-curated"@en` across all axioms (v0.5.1 fix) |
| **CQ-25** | `rice:Deadheart` typed as Symptom & Disease | Disambiguate symptom as `rice:Deadheart_Symptom` (v0.5.1 fix) |
| **CQ-18** | Only 1/28 symptoms visually grounded | Annotate image dataset at symptom level (`captures` relation) (Phase 3) |
| **CQ-20** | 0 sensor observations | Ingest IoT sensor telemetry as `SensorObservation` instances (Phase 3) |

---

## Citation

```bibtex
@misc{ricemmkg_benchmark_2026,
  title  = {Rice MMKG v0.5: Competency Question SPARQL Benchmark},
  author = {Ariful et al.},
  year   = {2026},
  note   = {25 Competency Questions evaluated against OWL RL materialised Rice MMKG.rdf (66,873 asserted / 158,685 materialised triples)}
}
```
