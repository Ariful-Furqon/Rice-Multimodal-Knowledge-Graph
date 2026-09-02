# Rice MMKG v0.5 - SPARQL Competency Question Documentation

**Ontology:** `Rice MMKG.rdf` (owl:versionInfo 0.5)  
**Triples:** 66,873 asserted / 158,685 after OWL RL materialisation  
**Benchmark Run:** 2026-09-02  
**Overall:** 20 PASS / 1 PARTIAL / 3 FAIL / 1 DOCUMENTED (24 scored CQs)

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

## Evaluation Design

CQs sit on **two orthogonal axes**: reasoning depth (L1-L4) and knowledge dimension (D1-D3).

| Depth | Meaning |
|---|---|
| **L1** | Factual - single-hop retrieval |
| **L2** | Contextual - multi-criteria join |
| **L3** | Causal - multi-hop chain |
| **L4** | Inferential - requires OWL entailment |

| Dimension | Meaning |
|---|---|
| **D1** | Agronomic / symbolic |
| **D2** | Cross-modal (image to concept) |
| **D3** | Provenance and external alignment |

| Mode | PASS when | Purpose |
|---|---|---|
| `coverage` | covered / total >= 50% | How much of a class the relation reaches |
| `negative` | exactly 0 rows | Integrity constraint - rows are violations |
| `entailment` | entailed > asserted | Proves OWL reasoning contributes answers |
| `documented` | (not scored) | Declared extension point, kept visible |

> **Key rule:** mandatory hops are written **without** OPTIONAL.
> OPTIONAL on a tested hop makes the CQ unfalsifiable.

---

## Result Matrix

| CQ | Depth | Dim | Mode | Result | Measurement |
|---|---|---|---|---|---|
| CQ-01  | L1 | D1 | coverage   | **PASS**       | 7/9 disease (78%)           |
| CQ-02  | L1 | D1 | coverage   | **PASS**       | 15/16 disease/pest (94%)    |
| CQ-03  | L1 | D1 | coverage   | **PASS**       | 15/16 disease/pest (94%)    |
| CQ-04  | L1 | D1 | coverage   | **PASS**       | 28/28 symptom (100%)        |
| CQ-05  | L2 | D1 | coverage   | **PASS**       | 13/16 disease/pest (81%)    |
| CQ-06  | L2 | D1 | coverage   | **PASS**       | 6/7 growth stage (86%)      |
| CQ-07  | L2 | D1 | negative   | **PASS**       | 0 violation                 |
| CQ-08  | L2 | D1 | coverage   | **PASS**       | 1/2 treatment (50%)         |
| CQ-09  | L3 | D1 | coverage   | **PASS**       | 1/1 vector (100%)           |
| CQ-09b | L3 | D1 | negative   | **FAIL**       | 1 violation                 |
| CQ-10  | L3 | D1 | coverage   | **PASS**       | 9/9 disease (100%)          |
| CQ-11  | L3 | D1 | coverage   | **PASS**       | 9/16 disease/pest (56%)     |
| CQ-11b | L2 | D1 | coverage   | **PASS**       | 4/4 severity level (100%)   |
| CQ-12  | L4 | D1 | entailment | **PASS**       | 0 -> 1,442 entailed         |
| CQ-13  | L4 | D1 | entailment | **PASS**       | 0 -> 139 entailed           |
| CQ-14  | L3 | D2 | coverage   | **PASS**       | 8,643/8,643 image (100%)    |
| CQ-15  | L2 | D2 | coverage   | **PASS**       | 10/10 class (100%)          |
| CQ-16  | L1 | D2 | coverage   | **PARTIAL**    | 1/28 symptom (4%)           |
| CQ-17  | L1 | D2 | negative   | **PASS**       | 0 violation                 |
| CQ-18  | L1 | D2 | documented | **DOCUMENTED** | 0 sensor observation        |
| CQ-19  | L4 | D3 | coverage   | **PASS**       | 265/265 axiom (100%)        |
| CQ-20  | L4 | D3 | negative   | **PASS**       | 0 violation                 |
| CQ-21  | L4 | D3 | coverage   | **PASS**       | 18/24 entity (75%)          |
| CQ-22  | L4 | D3 | negative   | **FAIL**       | 1 violation (literal tag)   |
| CQ-23  | L4 | D1 | negative   | **FAIL**       | 1 violation (Deadheart)     |

---

## L1 x D1 - Factual / Agronomic

### CQ-01 | L1 x D1 | coverage | PASS - 7/9 diseases (78%)

**Question:** Which rice diseases have an identified causal pathogen?

**Rationale:** Aetiological completeness. A disease without a causal agent cannot support any downstream causal query.

**Numerator** (diseases that have a cause):
```sparql
SELECT DISTINCT ?d WHERE { ?d a rice:Disease . ?p rice:causes ?d }
```
**Denominator** (all diseases):
```sparql
SELECT DISTINCT ?d WHERE { ?d a rice:Disease }
```

**Result:** 7/9 (77.8%) - PASS  
**Not covered (2):** `rice:Deadheart`, `rice:Sheath_Blight`

---

### CQ-02 | L1 x D1 | coverage | PASS - 15/16 disease/pest (94%)

**Question:** Which diseases and pests have at least one observable symptom?

**Rationale:** Diagnosability. Without a symptom link an entity is invisible to field-observation-driven inference.

**Numerator:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:indicatedBy ?s . ?s a rice:Symptom }
```
**Denominator:**
```sparql
SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```

**Result:** 15/16 (93.8%) - PASS  
**Not covered (1):** `rice:Nephotettix_Virescens`

---

### CQ-03 | L1 x D1 | coverage | PASS - 15/16 disease/pest (94%)

**Question:** Which diseases and pests have at least one control treatment?

**Rationale:** Actionability. The KG must not diagnose what it cannot advise on.

**Numerator:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:controlledBy ?t . ?t a rice:Treatment }
```
**Denominator:**
```sparql
SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```

**Result:** 15/16 (93.8%) - PASS  
**Not covered (1):** `rice:Nephotettix_Virescens`

---

### CQ-04 | L1 x D1 | coverage | PASS - 28/28 symptoms (100%)

**Question:** Which symptoms are attached to at least one disease or pest?

**Rationale:** Detects orphan symptoms - vocabulary declared but never used in a diagnostic pattern.

**Numerator:**
```sparql
SELECT DISTINCT ?s WHERE { ?s a rice:Symptom . ?e rice:indicatedBy ?s }
```
**Denominator:**
```sparql
SELECT DISTINCT ?s WHERE { ?s a rice:Symptom }
```

**Result:** 28/28 (100%) - PASS. Zero orphan symptoms.

---

## L2 x D1 - Contextual / Agronomic

### CQ-05 | L2 x D1 | coverage | PASS - 13/16 disease/pest (81%)

**Question:** For which diseases/pests can we state both the growth stage of occurrence AND an environmental factor raising their risk?

**Rationale:** Multi-criteria contextualisation. Both joins are mandatory (no OPTIONAL), so the CQ measures real co-population of `occursIn` and `increaseRiskOf`.

**Numerator:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:occursIn ?stage . ?stage a rice:GrowthStage .
  ?f rice:increaseRiskOf ?e . ?f a rice:EnvironmentalFactor }
```
**Denominator:**
```sparql
SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```
**Detail query** (all instantiations, sample):
```sparql
SELECT DISTINCT ?stage ?e ?f WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:occursIn ?stage . ?stage a rice:GrowthStage .
  ?f rice:increaseRiskOf ?e . ?f a rice:EnvironmentalFactor
} ORDER BY ?stage ?e
```

**Result:** 13/16 (81.2%) - PASS, 88 instantiations  
**Not covered (3):** `rice:Leaf_Folder`, `rice:Nephotettix_Virescens`, `rice:Rice_Bug`

---

### CQ-06 | L2 x D1 | coverage | PASS - 6/7 growth stages (86%)

**Question:** Which growth stages have a documented vulnerability profile naming a concrete disease or pest?

**Rationale:** `vulnerableTo` is the most frequently asserted domain relation in the KG (59 triples), so it must be exercised directly.

**Numerator:**
```sparql
SELECT DISTINCT ?g WHERE {
  ?g a rice:GrowthStage . ?g rice:vulnerableTo ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```
**Denominator:**
```sparql
SELECT DISTINCT ?g WHERE { ?g a rice:GrowthStage }
```

**Result:** 6/7 (85.7%) - PASS  
**Not covered (1):** `rice:Harvest_Stage`

---

### CQ-07 | L2 x D1 | negative | PASS - 0 violations

**Question:** Is the stage-vulnerability view consistent with the occurrence view?

**Rationale:** Integrity constraint. If stage G is `vulnerableTo` entity E, then E must `occursIn` G. Any returned row is an inconsistency.

**Query:**
```sparql
SELECT DISTINCT ?g ?e WHERE {
  ?g a rice:GrowthStage . ?g rice:vulnerableTo ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  FILTER NOT EXISTS { ?e rice:occursIn ?g } }
```

**Result:** 0 violations - PASS. The two views are mutually consistent.

---

### CQ-08 | L2 x D1 | coverage | PASS - 1/2 preventive treatments (50%)

**Question:** Which preventive treatments carry an explicit growth-stage prerequisite for their application?

**Rationale:** Prevention advice without a timing constraint is not operationalisable in the field.

**Numerator:**
```sparql
SELECT DISTINCT ?t WHERE {
  ?e rice:preventedBy ?t . ?t rice:requires ?g . ?g a rice:GrowthStage }
```
**Denominator:**
```sparql
SELECT DISTINCT ?t WHERE { ?e rice:preventedBy ?t }
```

**Result:** 1/2 (50.0%) - PASS (exactly at threshold)  
**Not covered (1):** `rice:Seed_Treatment`

---

## L3 x D1 - Causal / Multi-hop / Agronomic

### CQ-09 | L3 x D1 | coverage | PASS - 1/1 declared vector (100%)

**Question:** For which declared insect vectors is the transmission chain vector -> pathogen -> disease fully traversable?

**Rationale:** The canonical multi-hop epidemiological query. Denominator = pests that assert `transmits` (not all pests), measuring chain completeness, not vector prevalence.

**Numerator:**
```sparql
SELECT DISTINCT ?v WHERE {
  ?v rice:transmits ?p . ?p rice:causes ?d . ?d a rice:Disease }
```
**Denominator:**
```sparql
SELECT DISTINCT ?v WHERE { ?v rice:transmits ?p }
```
**Detail query** (full chain instantiation):
```sparql
SELECT DISTINCT ?v ?p ?d WHERE {
  ?v rice:transmits ?p . ?p rice:causes ?d . ?d a rice:Disease
} ORDER BY ?v
```

**Result:** 1/1 (100%) - PASS

| vector | pathogen | disease |
|---|---|---|
| rice:Nephotettix_Virescens | rice:Rice_Tungro_Bacilliform_Virus | rice:Rice_Tungro_Disease |
| rice:Nephotettix_Virescens | rice:Rice_Tungro_Spherical_Virus   | rice:Rice_Tungro_Disease |

---

### CQ-09b | L3 x D1 | negative | **FAIL** - 1 violation

**Question:** Are there insect vectors for which no control treatment is recorded, leaving the transmission chain unbreakable?

**Rationale:** A vector chain that cannot be interrupted has no advisory value. Separates 'the chain exists' (CQ-09) from 'the chain is actionable' (CQ-09b).

**Query:**
```sparql
SELECT DISTINCT ?v WHERE {
  ?v rice:transmits ?p .
  FILTER NOT EXISTS { ?v rice:controlledBy ?t } }
```

**Result:** 1 violation - **FAIL**  
**Violating individual:** `rice:Nephotettix_Virescens` has no `controlledBy` triple.

> **Fix:** Add `rice:Nephotettix_Virescens rice:controlledBy rice:Vector_Control` to the ontology.

---

### CQ-10 | L3 x D1 | coverage | PASS - 9/9 diseases (100%)

**Question:** For which diseases is the full risk-to-remedy chain traversable: environmental factor -> disease -> symptom -> treatment?

**Rationale:** End-to-end decision-support path. This is the query an advisory application actually needs to answer.

**Numerator:**
```sparql
SELECT DISTINCT ?d WHERE {
  ?d a rice:Disease .
  ?f rice:increaseRiskOf ?d . ?f a rice:EnvironmentalFactor .
  ?d rice:indicatedBy ?s . ?s a rice:Symptom .
  ?d rice:controlledBy ?t . ?t a rice:Treatment }
```
**Denominator:**
```sparql
SELECT DISTINCT ?d WHERE { ?d a rice:Disease }
```
**Detail query:**
```sparql
SELECT DISTINCT ?d ?f ?s ?t WHERE {
  ?d a rice:Disease .
  ?f rice:increaseRiskOf ?d . ?f a rice:EnvironmentalFactor .
  ?d rice:indicatedBy ?s . ?s a rice:Symptom .
  ?d rice:controlledBy ?t . ?t a rice:Treatment
} ORDER BY ?d
```

**Result:** 9/9 (100%) - PASS, 277 instantiations  
Example: `Bacterial_Leaf_Blight | High_Humidity | Wilting | Crop_Rotation`

---

### CQ-11 | L3 x D1 | coverage | PASS - 9/16 disease/pest (56%)

**Question:** For which diseases and pests does the KG reach the management layer, i.e. recommend a concrete ManagementAction?

**Rationale:** Tests that diagnosis terminates in an operational decision. Direction of `rice:recommends` in this KG is entity -> action.

**Numerator:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:recommends ?m . ?m a rice:ManagementAction }
```
**Denominator:**
```sparql
SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```

**Result:** 9/16 (56.2%) - PASS  
**Not covered (7):** `rice:Armyworm`, `rice:Brown_Planthopper`, `rice:Leaf_Folder`,
`rice:Nephotettix_Virescens`, `rice:Rice_Bug`, `rice:Sheath_Blight`, `rice:Stem_Borer`

---

### CQ-11b | L2 x D1 | coverage | PASS - 4/4 severity levels (100%)

**Question:** Does every severity level map to a recommended management action, so that triage advice is total?

**Rationale:** Severity-driven triage is the decision layer of the KG. A severity level with no action is a hole in the advisory logic.

**Numerator:**
```sparql
SELECT DISTINCT ?sev WHERE { ?sev a rice:SeverityLevel . ?sev rice:recommends ?m }
```
**Denominator:**
```sparql
SELECT DISTINCT ?sev WHERE { ?sev a rice:SeverityLevel }
```
**Detail query:**
```sparql
SELECT DISTINCT ?sev ?m WHERE {
  ?sev a rice:SeverityLevel . ?sev rice:recommends ?m
} ORDER BY ?sev
```

**Result:** 4/4 (100%) - PASS

| severity | management action |
|---|---|
| rice:Critical_Severity | rice:Immediate_Intervention |
| rice:High_Severity     | rice:Preventive_Action      |
| rice:High_Severity     | rice:Immediate_Intervention |
| rice:Low_Severity      | rice:No_Action_Needed       |
| rice:Medium_Severity   | rice:Field_Inspection       |
| rice:Medium_Severity   | rice:Monitoring             |

---

## L4 x D1 - Inferential / Agronomic (requires OWL materialisation)

### CQ-12 | L4 x D1 | entailment | PASS - 0 asserted -> 1,442 entailed

**Question:** Which observations are SymptomaticObservations (defined class: Observation that captures some Symptom)?

**Rationale:** The one genuine defined class in the ontology. Asserted membership is zero by construction; a non-zero entailed count proves the OWL axiomatisation does work SPARQL alone cannot.

**Query** (run on both asserted and OWL RL materialised graph):
```sparql
SELECT DISTINCT ?o WHERE { ?o a rice:SymptomaticObservation }
```

**Result:** 0 on asserted -> **1,442 on materialised graph** - PASS

> OWL reasoning contributes 1,442 answers invisible in the raw RDF.

---

### CQ-13 | L4 x D1 | entailment | PASS - 0 asserted -> 139 entailed

**Question:** Can the KG be queried in the inverse direction (disease -> `causedBy` -> pathogen; symptom -> `indicates` -> disease)?

**Rationale:** 14 of 26 object properties are declared as `owl:inverseOf` but never explicitly asserted. Query robustness depends on materialising them.

**Query** (run on both asserted and OWL RL materialised graph):
```sparql
SELECT ?x ?y WHERE {
  { ?x rice:causedBy ?y } UNION { ?x rice:indicates ?y } UNION
  { ?x rice:hasOccurrenceOf ?y } UNION { ?x rice:controls ?y } }
```

**Result:** 0 on asserted -> **139 on materialised graph** - PASS

> Inverse properties `causedBy`, `indicates`, `controls`, `hasOccurrenceOf` are materialised
> by the reasoner, never manually asserted.

---

## L3-L2 x D2 - Cross-modal (Image to Concept)

### CQ-14 | L3 x D2 | coverage | PASS - 8,643/8,643 images (100%)

**Question:** Which image observations can be grounded all the way to an agronomic recommendation: image -> annotated class -> symptom and treatment?

**Rationale:** The central multimodal claim of the KG. Denominator restricted to images annotated with Disease or Pest (HealthStatus images correctly have no symptom/treatment - including them would understate grounding by 17%).

**Numerator:**
```sparql
SELECT DISTINCT ?img WHERE {
  ?img a rice:ImageObservation . ?img rice:annotatedAs ?e .
  ?e rice:indicatedBy ?s . ?e rice:controlledBy ?t }
```
**Denominator:**
```sparql
SELECT DISTINCT ?img WHERE {
  ?img a rice:ImageObservation . ?img rice:annotatedAs ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest } }
```

**Result:** 8,643/8,643 (100%) - PASS

---

### CQ-15 | L2 x D2 | coverage | PASS - 10/10 annotated classes (100%)

**Question:** Which annotated classes of the image corpus are typed as a domain entity (Disease, Pest or HealthStatus)?

**Rationale:** Checks that dataset labels were reconciled with the ontology rather than left as free-floating individuals.

**Numerator:**
```sparql
SELECT DISTINCT ?e WHERE {
  ?img rice:annotatedAs ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest } UNION { ?e a rice:HealthStatus } }
```
**Denominator:**
```sparql
SELECT DISTINCT ?e WHERE { ?img rice:annotatedAs ?e }
```

**Result:** 10/10 (100%) - PASS. All image labels are typed OWL individuals.

---

### CQ-16 | L1 x D2 | coverage | **PARTIAL** - 1/28 symptoms (4%)

**Question:** Which symptoms are grounded in visual evidence, i.e. captured by at least one image observation?

**Rationale:** Symptom-level visual grounding distinguishes an MMKG from a text ontology with images bolted on. Expected to expose the sharpest current gap.

**Numerator:**
```sparql
SELECT DISTINCT ?s WHERE { ?s a rice:Symptom . ?o rice:captures ?s }
```
**Denominator:**
```sparql
SELECT DISTINCT ?s WHERE { ?s a rice:Symptom }
```

**Result:** 1/28 (3.6%) - **PARTIAL** (below 50% threshold)

**Not covered (27):** Brown_Leaf_Tip, Brown_Lesion, Chewed_Leaf, Dead_Tiller, Discolored_Panicle,
Dry_Leaf_Tip, Empty_Grain, Excessive_Tillering, Grain_Discoloration, Hopper_Burn, Leaf_Rolling,
Leaf_Scratching, Leaf_Spot, Neck_Rot, Panicle_Blast, Reduced_Tillering, Stem_Rot_Symptom,
Sterile_Panicle, Stunted_Growth, Translucent_Stripe, Water_Soaked_Streak, White_Ear,
White_Streak, Wilting, Yellow_Leaf, Yellow_Orange_Discoloration, Yellow_Streak

> **Phase 3 target:** Add `rice:captures rice:Symptom` triples to ImageObservation individuals.
> Currently only class-level annotation (`annotatedAs Disease`) exists.

---

### CQ-17 | L1 x D2 | negative | PASS - 0 violations

**Question:** Are there image observations lacking a content URL or a source dataset provenance link?

**Rationale:** Integrity constraint on the media layer. Any row means an image cannot be retrieved or attributed.

**Query:**
```sparql
SELECT ?img WHERE {
  ?img a rice:ImageObservation .
  FILTER ( NOT EXISTS { ?img schema:contentUrl ?u } ||
           NOT EXISTS { ?img prov:wasDerivedFrom ?ds } ) }
```

**Result:** 0 violations - PASS. All 10,407 images have a content URL and dataset provenance.

---

### CQ-18 | L1 x D2 | documented | DOCUMENTED - 0 sensor observations

**Question:** How many sensor observations does the KG contain?

**Rationale:** Declared extension point. Recorded as a measurement, not scored, so the roadmap gap stays visible without inflating or deflating the pass rate.

**Query:**
```sparql
SELECT DISTINCT ?o WHERE { ?o a rice:SensorObservation }
```

**Result:** 0 individuals - DOCUMENTED (not scored)

> `rice:SensorObservation` is a declared class with no current population.
> Populating it is scoped to Phase 3 of the ESWC 2027 roadmap.

---

## L4 x D3 - Inferential / Provenance and Alignment

### CQ-19 | L4 x D3 | coverage | PASS - 265/265 axioms (100%)

**Question:** Which reified domain assertions carry both an authoritative source URI and a bibliographic citation?

**Rationale:** Provenance completeness - the scientific-defensibility claim of the KG.

**Numerator:**
```sparql
SELECT DISTINCT ?ax WHERE {
  ?ax a owl:Axiom ; dcterms:source ?src ; dcterms:bibliographicCitation ?cit }
```
**Denominator:**
```sparql
SELECT DISTINCT ?ax WHERE { ?ax a owl:Axiom }
```

**Result:** 265/265 (100%) - PASS  
Sources: CABI (248), IRRI (11), BBPOPT (7).

---

### CQ-20 | L4 x D3 | negative | PASS - 0 violations

**Question:** Are there reified axioms with incomplete provenance (missing source, citation or evidence type)?

**Rationale:** Integrity constraint complementing CQ-19.

**Query:**
```sparql
SELECT ?ax WHERE {
  ?ax a owl:Axiom .
  FILTER ( NOT EXISTS { ?ax dcterms:source ?s } ||
           NOT EXISTS { ?ax dcterms:bibliographicCitation ?c } ||
           NOT EXISTS { ?ax rice:evidenceType ?e } ) }
```

**Result:** 0 violations - PASS. All 265 axioms have complete provenance.

---

### CQ-21 | L4 x D3 | coverage | PASS - 18/24 entities (75%)

**Question:** Which biological entities (disease, pathogen, pest) are aligned to an external vocabulary (EPPO, AGROVOC or NCBI Taxonomy)?

**Rationale:** Interoperability. Written as a coverage measure (not an OPTIONAL projection, which would report success even when every alignment column is null).

**Numerator:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pathogen } UNION { ?e a rice:Pest }
  { ?e rice:eppoCode ?c } UNION { ?e skos:exactMatch ?m } UNION { ?e skos:closeMatch ?m2 } }
```
**Denominator:**
```sparql
SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pathogen } UNION { ?e a rice:Pest } }
```

**Result:** 18/24 (75%) - PASS  
**Not covered (6):** `rice:Bacterial_Leaf_Blight`, `rice:Bacterial_Leaf_Streak`,
`rice:Bacterial_Panicle_Blight`, `rice:Brown_Spot`, `rice:Deadheart`, `rice:Sheath_Blight`

---

### CQ-22 | L4 x D3 | negative | **FAIL** - 1 violation

**Question:** Are annotation literals lexically consistent, i.e. is `rice:evidenceType` uniformly language-tagged?

**Rationale:** Literal-hygiene constraint. An untagged duplicate of a tagged value silently splits GROUP BY and breaks `lang()` filters.

**Query:**
```sparql
SELECT ?ax ?v WHERE {
  ?ax rice:evidenceType ?v . FILTER ( lang(?v) = "" ) }
```

**Result:** 1 violation - **FAIL**  
**Violating axiom:** `Nbfaed4dbd7b44b53bd1f94cabfb4cac5` - literal `"literature-curated"` has no language tag.

> **Fix:** Replace `"literature-curated"` with `"literature-curated"@en` on all `rice:evidenceType` annotations.

---

### CQ-23 | L4 x D1 | negative | **FAIL** - 1 violation

**Question:** Under entailment, is any individual typed as both a Symptom and a Disease?

**Rationale:** Category discipline. Symptom and Disease are intended to be disjoint; an overlap means a mistyped individual or a property domain declared too narrowly. The conflict is produced by inference - invisible in asserted triples.

**Query** (executed on OWL RL materialised graph):
```sparql
SELECT DISTINCT ?x WHERE {
  ?x a rice:Symptom . ?x a rice:Disease }
```

**Result:** 1 violation - **FAIL**  
**Violating individual:** `rice:Deadheart`

> **Fix:** Rename the symptom individual to `rice:Deadheart_Symptom` and keep
> `rice:Deadheart` typed as Disease only; or merge into a single Disease with
> `rice:Dead_Tiller` as the associated Symptom individual.

---

## Action Items from FAIL Results

| CQ | Issue | Recommended Fix |
|---|---|---|
| **CQ-09b** | `Nephotettix_Virescens` has no `controlledBy` triple | Add `rice:Nephotettix_Virescens rice:controlledBy rice:Vector_Control` |
| **CQ-22** | `rice:evidenceType` literal without `@en` tag | Replace all bare literals with `"literature-curated"@en` |
| **CQ-23** | `rice:Deadheart` typed as Symptom and Disease under entailment | Rename symptom to `rice:Deadheart_Symptom`; keep Disease as-is |

## Extension Point from PARTIAL Result

| CQ | Gap | Phase 3 Task |
|---|---|---|
| **CQ-16** | Only 1/28 symptoms visually grounded via `rice:captures` | Add symptom-level `captures` annotation to ImageObservation individuals |

---

## Citation

```
Rice MMKG v0.5 - CQ SPARQL Benchmark.
Executed: 2026-09-02 against Rice MMKG.rdf (owl:versionInfo 0.5).
OWL RL materialisation: owlrl 6.x / rdflib 7.x / Python 3.x.
Methodology: Gruninger & Fox (1995); Suarez-Figueroa et al. (2012);
Poveda-Villalon et al. (2022).
Result: 20 PASS / 1 PARTIAL / 3 FAIL / 1 DOCUMENTED (24 scored CQs).
```
