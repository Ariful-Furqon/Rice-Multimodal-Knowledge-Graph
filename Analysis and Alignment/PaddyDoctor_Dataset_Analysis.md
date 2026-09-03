# Paddy Doctor Dataset Analysis for Rice MMKG

## Scope

This report profiles the **local** dataset at `Data/PaddyDoctor`. It describes
the 10,407-image collection available in this workspace and must not be treated
as a claim about the complete public Paddy Doctor release.

**Profile date:** 2026-08-03 (Updated 2026-09-03 for Rice MMKG v0.6)  
**Data access:** local files only; `/Data/` is excluded from Git  
**Purpose:** assess class coverage, data quality signals, semantic alignment, and multimodal ground-truth mapping for Rice MMKG.

## File-level profile

| Measure | Result |
|---|---:|
| Image files | 10,407 |
| Classes (folders) | 10 |
| File format | JPG only |
| Total size | 781.55 MB |
| Sampled image resolution | 480 × 640 pixels |
| Filename collisions across classes | 0 |
| Largest class | `normal`: 1,764 images (16.95%) |
| Smallest class | `bacterial_panicle_blight`: 337 images (3.24%) |
| Largest/smallest ratio | 5.23 |

The resolution is based on a 20-image sample. A full image-decoding validation
is a separate quality-control task before model training or full KG ingestion.

## Class distribution and semantic alignment

| Dataset label | Count | Share | Rice MMKG entity | Semantic type (v0.6) | Visual Grounding (`rice:captures`) |
|---|---:|---:|---|---|---|
| `bacterial_leaf_blight` | 479 | 4.60% | `Bacterial_Leaf_Blight` | Disease | — (class-level annotation) |
| `bacterial_leaf_streak` | 380 | 3.65% | `Bacterial_Leaf_Streak` | Disease | — (class-level annotation) |
| `bacterial_panicle_blight` | 337 | 3.24% | `Bacterial_Panicle_Blight` | Disease | — (class-level annotation) |
| `blast` | 1,738 | 16.70% | `Rice_Blast_Disease` | Disease | — (class-level annotation) |
| `brown_spot` | 965 | 9.27% | `Brown_Spot` | Disease | — (class-level annotation) |
| `dead_heart` | 1,442 | 13.86% | `Deadheart` | Disease (Damage condition) | `rice:captures rice:Dead_Tiller` (Symptom) |
| `downy_mildew` | 620 | 5.96% | `Downy_Mildew` | Disease | — (class-level annotation) |
| `hispa` | 1,594 | 15.32% | `Hispa` | Pest | — (class-level annotation) |
| `normal` | 1,764 | 16.95% | `Normal_Health` | HealthStatus | — (healthy reference baseline) |
| `tungro` | 1,088 | 10.45% | `Rice_Tungro_Disease` | Disease | — (class-level annotation) |
| **Total** | **10,407** | **100.00%** | — | — | — |

The collection is moderately imbalanced. A model evaluation split should be
stratified by label, and results should include macro-F1 or per-class recall in
addition to overall accuracy; otherwise, common labels such as `normal` and
`blast` can dominate the result.

## KG population readiness

The folder labels map without ambiguity to the local ontology: in v0.6, 7,049 images map
to `Disease` entities (including the 1,442 `dead_heart` damage-condition images), 1,594 to a `Pest`,
and 1,764 to a `HealthStatus`. Furthermore, the 1,442 `dead_heart` images formally capture the
`Dead_Tiller` symptom (`rice:captures rice:Dead_Tiller`), satisfying the `SymptomaticObservation`
defined class. The absence of filename collisions permits deterministic image
IRIs, but the class label should still be included in each IRI to make the
generation rule explicit.

### Proposed image identifier rule

```text
riceMMKG:PaddyDoctor_<dataset-label>_<filename-without-extension>
```

Example:

```text
riceMMKG:PaddyDoctor_blast_100023
```

### Minimum assertion pattern

```turtle
riceMMKG:PaddyDoctor_blast_100023
    a riceMMKG:ImageObservation ;
    rdfs:label "Paddy Doctor image: blast/100023.jpg"@en ;
    schema:contentUrl "Data/PaddyDoctor/blast/100023.jpg" ;
    prov:wasDerivedFrom riceMMKG:PaddyDoctorDataset ;
    riceMMKG:annotatedAs riceMMKG:Rice_Blast_Disease .

# For dead_heart images with symptom grounding (v0.6):
riceMMKG:PaddyDoctor_dead_heart_110232
    a riceMMKG:ImageObservation ;
    rdfs:label "Paddy Doctor image: dead_heart/110232.jpg"@en ;
    schema:contentUrl "Data/PaddyDoctor/dead_heart/110232.jpg" ;
    prov:wasDerivedFrom riceMMKG:PaddyDoctorDataset ;
    riceMMKG:annotatedAs riceMMKG:Deadheart ;
    riceMMKG:captures riceMMKG:Dead_Tiller .
```

> **Evolution note:** In initial prototypes, `ImageObservation` was formerly named `LeafImage`
and `annotatedAs` was named `classifiedAs`. These were cleaned up in v0.4 and v0.5 to adhere to
standard schema terminology (`ImageObservation` avoids inaccuracy for panicle and deadheart
images, and `annotatedAs` separates raw dataset labeling from verified domain detection). In v0.6,
`captures` was disambiguated to link `Dead_Tiller` directly. Correction to the original gap note below: at
review time the `detects` property's range had already been extended to
`Disease`/`Pest`/`Symptom` (not just `Disease`/`Pest` as first assumed), so
`dead_heart` alone was not actually blocked — `normal` (`HealthStatus`) was
the only class `detects` could not represent. `classifiedAs` was still added
as a separate property rather than folding `HealthStatus` into `detects`,
because it carries different semantics: `classifiedAs` records the raw,
unverified source-dataset label, while `detects`/`detectedBy` is reserved for
confirmed detections. Population can now proceed using `classifiedAs` for
all ten dataset labels.

## First population — completed 2026-08-05

| Graph component | Expected count | Actual count |
|---|---:|---:|
| New image observation individuals | 10,407 | 10,407 |
| Image-to-classification assertions (`classifiedAs`) | 10,407 | 10,407 |
| Image-to-dataset-label assertions (`sourceDatasetLabel`) | 10,407 | 10,407 |
| Canonical labelled entities reused | 10 | 10 |

Per-class counts matched the class-distribution table above exactly (verified
with an `rdflib` SPARQL query grouping by `sourceDatasetLabel`). Population
ran in 10 batches, one per dataset label, each validated (XML well-formedness
+ SPARQL count check) before moving to the next. Total `Observation`
individuals in the graph: 10,412 (10,407 Paddy Doctor + 5 pre-existing
example observations).

`Rice MMKG.rdf` grew from ~80 KB to ~6.9 MB as a result. No image bytes or
absolute local paths were inserted into the RDF or Git repository — only the
relative dataset label and filename stem, per the identifier rule above.

## Competency questions for validation

Answered 2026-08-05 by running SPARQL against the populated graph (Protégé's
SPARQL Query tab failed to render on this ontology's size — 10,412
individuals — so queries were run externally with `rdflib` and cross-checked
against the DL Query results already obtained in Protégé for CQ1/CQ2).

1. **Which Paddy Doctor images are classified as `Rice_Blast_Disease`, and
   what AGROVOC concept is aligned to that disease?**
   1,738 images (`?obs rice:classifiedAs rice:Rice_Blast_Disease`), matching
   the `blast` class count exactly. Aligned AGROVOC concept:
   [`rice blast disease`](http://aims.fao.org/aos/agrovoc/c_152ac092) via
   `skos:exactMatch`.
2. **How many images support each `Disease`, `Pest`, `Symptom`, and
   `HealthStatus` entity?**
   `Disease`: 5,607 · `Pest`: 1,594 · `Symptom`: 1,442 · `HealthStatus`: 1,764
   — matches the "KG population readiness" table above exactly.
3. **Which ontology entities have dataset evidence but no AGROVOC
   alignment?**
   7 entities: `Bacterial_Leaf_Blight`, `Bacterial_Leaf_Streak`,
   `Bacterial_Panicle_Blight`, `Brown_Spot` (Disease), `Deadheart` (Symptom),
   `Hispa` (Pest), `Normal_Health` (HealthStatus) — matches the "Local-only /
   gap" rows already recorded in `AGROVOC_alignment.md`, confirming that
   register is accurate against the populated data.
4. **Does a proposed train/validation/test split preserve the distribution
   of all ten labels?**
   Out of scope for the KG — no split is represented in the ontology. This is
   a data-science pipeline decision to make at model-training time, not a
   graph query.

### Querying note — updated after the Observation subclass restructure (2026-08-05)

`Observation` was split into five subclasses (`DiseaseReport`, `FarmerReport`,
`FieldObservation`, `LeafImage`, `SensorReading`); all 10,407 Paddy Doctor
images are now typed `LeafImage`, not `Observation` directly. A raw SPARQL
query with `?obs a rice:Observation` (no reasoner) **no longer matches them**
— only `rdfs:subClassOf*` traversal or an active reasoner resolves that. The
CQ1–CQ3 queries above were re-run and give identical counts either way,
because they were rewritten to avoid depending on the direct type:

```sparql
# CQ1 — no "a Observation" needed; classifiedAs already implies it via domain
PREFIX rice: <http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#>
SELECT (COUNT(?obs) AS ?n) WHERE {
  ?obs rice:classifiedAs rice:Rice_Blast_Disease .
}

# CQ2 — same idea, grouped by the classification's own type
SELECT ?type (COUNT(?obs) AS ?n) WHERE {
  ?obs rice:classifiedAs ?cls . ?cls a ?type .
  FILTER(?type IN (rice:Disease, rice:Pest, rice:Symptom, rice:HealthStatus))
} GROUP BY ?type

# CQ3 — must now exclude NamedIndividual explicitly AND walk subclasses of
# Observation, since Disease/Pest/Symptom/HealthStatus entities carry
# sourceDatasetLabel too but so do the (excluded) per-image LeafImage instances
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?entity ?type WHERE {
  ?entity rice:sourceDatasetLabel ?label ; a ?type .
  FILTER(?type != owl:NamedIndividual)
  FILTER NOT EXISTS { ?type rdfs:subClassOf* rice:Observation }
  FILTER NOT EXISTS { ?entity skos:exactMatch ?x }
  FILTER NOT EXISTS { ?entity skos:closeMatch ?x }
}
```

## Recommended next implementation task

1. ~~Add the `classifiedAs` object property.~~ Done 2026-08-04.
2. ~~Generate a 10-image pilot and validate the resulting triples.~~ Done
   2026-08-04 — one `Observation` individual per dataset label (first file in
   each class folder), IRIs following `PaddyDoctor_<label>_<filename>`.
   Validated with `rdflib`: the full graph parses cleanly (783 triples), a
   SPARQL query returns all 10 `classifiedAs` triples, and each target
   entity's `rdf:type` matches the property's range union (`Normal_Health` →
   `HealthStatus`, `Deadheart` → `Symptom`, `Hispa` → `Pest`,
   `Rice_Blast_Disease` → `Disease`). Total `Observation` individuals in the
   graph: 15 (5 pre-existing + 10 pilot).
3. ~~Populate the remaining 10,397 images using the same pattern, in
   batches.~~ Done 2026-08-05 — see "First population" above.
4. ~~Split `Observation` into channel subclasses (`DiseaseReport`,
   `FarmerReport`, `FieldObservation`, `LeafImage`, `SensorReading`) instead
   of leaving generic example individuals of that shape, and retype all
   10,407 Paddy Doctor images to `LeafImage`.~~ Done 2026-08-05. Added an
   `AllDisjointClasses` axiom over the five new subclasses. Re-validated:
   XML well-formed, no disjointness violations (old 12-class axiom or the new
   5-class one), 10,407/10,407 images confirmed `LeafImage`, CQ1–CQ3 give
   identical results under the corrected queries above. Not yet committed to
   Git as of this writing.


---

## Benchmark Validation (Rice MMKG v0.6)

As of Rice MMKG v0.6, the Paddy Doctor dataset mapping is formally validated by the **25 Competency Question SPARQL Benchmark**:

- **CQ-16 (Multimodal Grounding, L3/D2):** Validates that all **8,643 disease and pest images** ground through their annotated classes to actionable symptoms and control treatments (**100% PASS**).
- **CQ-17 (Label Ontology Typing, L2/D2):** Confirms that all **10 dataset annotation labels** resolve to valid OWL classes in the domain graph (**100% PASS**).
- **CQ-18 (Symptom Visual Grounding, L1/D2):** Highlights that while 1,442 images capture `Dead_Tiller` via `rice:captures`, the remaining 26 symptoms represent a visual grounding gap (**PARTIAL at 4%**, forming the roadmap target for Phase 3).
- **CQ-19 (Media Integrity, L1/D2):** Verifies that 100% of all **10,407 image individuals** possess resolvable relative content URLs and `prov:wasDerivedFrom` provenance to `PaddyDoctorDataset` (**0 violations, PASS**).
