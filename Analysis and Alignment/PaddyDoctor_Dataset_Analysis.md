# Paddy Doctor Dataset Analysis for Rice MMKG

## Scope

This report profiles the **local** dataset at `Data/PaddyDoctor`. It describes
the 10,407-image collection available in this workspace and must not be treated
as a claim about the complete public Paddy Doctor release.

**Profile date:** 2026-08-03  
**Data access:** local files only; `/Data/` is excluded from Git  
**Purpose:** assess class coverage, data quality signals, and the viable first
instance-population plan for Rice MMKG.

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

| Dataset label | Count | Share | Rice MMKG entity | Semantic type | AGROVOC status |
|---|---:|---:|---|---|---|
| `bacterial_leaf_blight` | 479 | 4.60% | `Bacterial_Leaf_Blight` | Disease | Local-only / gap |
| `bacterial_leaf_streak` | 380 | 3.65% | `Bacterial_Leaf_Streak` | Disease | Local-only / gap |
| `bacterial_panicle_blight` | 337 | 3.24% | `Bacterial_Panicle_Blight` | Disease | Local-only / gap |
| `blast` | 1,738 | 16.70% | `Rice_Blast_Disease` | Disease | `skos:exactMatch` candidate added |
| `brown_spot` | 965 | 9.27% | `Brown_Spot` | Disease | Local-only / gap |
| `dead_heart` | 1,442 | 13.86% | `Deadheart` | Symptom | Local-only / gap |
| `downy_mildew` | 620 | 5.96% | `Downy_Mildew` | Disease | `skos:closeMatch` implemented (v2.3) |
| `hispa` | 1,594 | 15.32% | `Hispa` | Pest | Local-only / gap |
| `normal` | 1,764 | 16.95% | `Normal_Health` | HealthStatus | Local-only by design |
| `tungro` | 1,088 | 10.45% | `Rice_Tungro_Disease` | Disease | `skos:exactMatch` candidate added |
| **Total** | **10,407** | **100.00%** | — | — | — |

The collection is moderately imbalanced. A model evaluation split should be
stratified by label, and results should include macro-F1 or per-class recall in
addition to overall accuracy; otherwise, common labels such as `normal` and
`blast` can dominate the result.

## KG population readiness

The folder labels map without ambiguity to the local ontology: 5,607 images map
to `Disease` entities, 1,594 to a `Pest`, 1,442 to a `Symptom`, and 1,764 to a
`HealthStatus`. The absence of filename collisions permits deterministic image
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
    a riceMMKG:Observation ;
    rdfs:label "Paddy Doctor image: blast/100023.jpg"@en ;
    riceMMKG:sourceDatasetLabel "blast" ;
    riceMMKG:classifiedAs riceMMKG:Rice_Blast_Disease .
```

**Implemented 2026-08-04.** `classifiedAs` (domain `Observation`, range union
`Disease`/`Pest`/`Symptom`/`HealthStatus`, inverse `classifies`) is now
declared in `Rice MMKG.rdf`. Correction to the original gap note below: at
review time the `detects` property's range had already been extended to
`Disease`/`Pest`/`Symptom` (not just `Disease`/`Pest` as first assumed), so
`dead_heart` alone was not actually blocked — `normal` (`HealthStatus`) was
the only class `detects` could not represent. `classifiedAs` was still added
as a separate property rather than folding `HealthStatus` into `detects`,
because it carries different semantics: `classifiedAs` records the raw,
unverified source-dataset label, while `detects`/`detectedBy` is reserved for
confirmed detections. Population can now proceed using `classifiedAs` for
all ten dataset labels.

## Expected first population

| Graph component | Expected count |
|---|---:|
| New image observation individuals | 10,407 |
| Image-to-classification assertions | 10,407 |
| Image-to-dataset-label assertions | 10,407 |
| Canonical labelled entities reused | 10 |

No image bytes or absolute local paths should be inserted into the RDF or Git
repository. Store only a relative filename/identifier if a source-location
property is later approved.

## Competency questions for validation

1. Which Paddy Doctor images are classified as `Rice_Blast_Disease`, and what
   AGROVOC concept is aligned to that disease?
2. How many images support each `Disease`, `Pest`, `Symptom`, and
   `HealthStatus` entity?
3. Which ontology entities have dataset evidence but no AGROVOC alignment?
4. Does a proposed train/validation/test split preserve the distribution of all
   ten labels?

## Recommended next implementation task

1. ~~Add the `classifiedAs` object property.~~ Done 2026-08-04.
2. Generate RDF image instances in batches. Start with a 10-image pilot,
   validate the resulting triples in Protégé/SPARQL, and only then populate
   all 10,407 images.
