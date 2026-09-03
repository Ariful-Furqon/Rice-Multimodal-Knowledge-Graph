# Competency Questions for a Rice Pest & Disease Multimodal Knowledge Graph

## 1. Purpose and Scope

The proposed Rice Pest & Disease Multimodal Knowledge Graph (Rice-MMKG) is intended to support early diagnosis and decision-making for rice pest and disease management by integrating textual knowledge, field and close-up imagery, environmental/sensor observations, and genomic/tabular information. The knowledge graph is designed for researchers, plant pathologists, agricultural extension personnel, and precision-agriculture systems, with an initial agroecological focus on tropical rice production systems in Indonesia and Southeast Asia.

### Assumptions Used

Because no project-specific values were supplied for the bracketed input fields in the expert prompt, the following defaults are used:

- **Rice pests/diseases in scope:** rice blast, bacterial leaf blight, sheath blight, tungro disease, brown planthopper, stem borer, and rice bug.
- **Text sources:** scientific publications, extension/agronomy reports, surveillance bulletins, and expert-authored symptom descriptions.
- **Image sources:** field and close-up images of rice leaves, stems, panicles, and whole plants, including healthy baselines.
- **Sensor/environmental sources:** temperature, relative humidity, rainfall, soil moisture, and soil pH time series or aggregated field observations.
- **Genomic/tabular sources:** rice variety/cultivar records, resistance genes, resistance traits, and agronomic/yield records.
- **Target number of competency questions:** 36.
- **Ontology alignment:** no project-specific ontology is assumed yet; candidate alignment should later be evaluated against Crop Ontology, AGROVOC, Plant Trait Ontology, Plant Phenotype Ontology-related resources, and suitable plant disease/pathogen vocabularies.
- **Previously drafted CQs:** none are treated as fixed inputs for this execution.

---

# 2. Text-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What causal pathogens are associated with rice blast, bacterial leaf blight, and sheath blight? | Simple | Disease, Pathogen, `causedBy` | Establishes core disease–pathogen knowledge required for diagnosis and ontology construction. |
| CQ-TXT-02 | What symptoms are reported in scientific and extension literature for rice blast caused by *Magnaporthe oryzae*? | Relational | Disease, Pathogen, Symptom, `causedBy`, `hasSymptom` | Supports literature-grounded symptom modeling and diagnostic reasoning. |
| CQ-TXT-03 | Which rice diseases are reported to share visually similar leaf symptoms? | Relational | Disease, Symptom, `hasSymptom`, `similarTo` | Identifies sources of diagnostic ambiguity that the KG must represent. |
| CQ-TXT-04 | Which plant organs are reported to be affected by rice blast, bacterial leaf blight, sheath blight, tungro disease, stem borer, and rice bug? | Relational | Disease/Pest, PlantOrgan, `affectsOrgan` | Supports organ-specific diagnosis and multimodal image alignment. |
| CQ-TXT-05 | Which environmental conditions are reported to favor outbreaks of rice blast, bacterial leaf blight, and brown planthopper infestation? | Relational | Disease/Pest, EnvironmentalCondition, `favoredBy` | Links documented epidemiological knowledge to later sensor observations. |
| CQ-TXT-06 | Which rice diseases or pests have overlapping symptoms but different causal agents and management recommendations? | Complex-Inferential | Disease/Pest, Symptom, Pathogen, ManagementPractice, `hasSymptom`, `causedBy`, `managedBy` | Enables differential diagnosis and reduces the risk of selecting management based on symptoms alone. |

---

# 3. Image-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | What visible symptoms or damage patterns are annotated in a given rice image? | Simple | ImageObservation, Symptom, VisualFeature, `depictsSymptom`, `hasVisualFeature` | Establishes a machine-queryable representation of visual evidence. |
| CQ-IMG-02 | Which plant organ is depicted in an image containing disease symptoms or pest damage? | Simple | ImageObservation, PlantOrgan, `depictsOrgan` | Supports organ-aware diagnosis and image retrieval. |
| CQ-IMG-03 | Which annotated images depict spindle-shaped lesions consistent with rice blast symptoms? | Relational | ImageObservation, VisualFeature, Symptom, Disease, `hasVisualFeature`, `depictsSymptom` | Supports retrieval of disease-relevant image evidence. |
| CQ-IMG-04 | Which rice diseases or pest damage classes exhibit visually similar lesion, discoloration, wilting, or tissue-damage patterns in the image collection? | Relational | ImageObservation, VisualFeature, Disease/Pest, `hasVisualFeature`, `evidenceFor` | Identifies visually confusable conditions that require additional modalities. |
| CQ-IMG-05 | Which disease or pest class is best supported by the combination of lesion shape, lesion color, spatial distribution, and affected plant organ annotated in an image? | Complex-Inferential | ImageObservation, VisualFeature, PlantOrgan, Disease/Pest, `hasVisualFeature`, `depictsOrgan`, `evidenceFor` | Tests whether multiple visual characteristics can jointly support a diagnosis. |

---

# 4. Sensor / Environmental-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What temperature, relative humidity, rainfall, soil moisture, and soil pH values were recorded at a specified rice field during a given observation period? | Simple | RiceField, SensorObservation, EnvironmentalVariable, TimeInterval, `observedAt`, `measures`, `observedDuring` | Establishes access to field environmental observations. |
| CQ-ENV-02 | Which observation periods had relative humidity, temperature, or rainfall values above or below specified thresholds? | Simple | SensorObservation, EnvironmentalVariable, TimeInterval, `numericValue` | Supports threshold-based environmental querying. |
| CQ-ENV-03 | Which rice fields experienced environmental conditions represented in the KG as favorable for rice blast, bacterial leaf blight, or brown planthopper infestation? | Relational | RiceField, SensorObservation, EnvironmentalCondition, Disease/Pest, `favoredBy`, `observedAt` | Connects raw sensor observations with domain risk knowledge. |
| CQ-ENV-04 | Which combinations of temperature, humidity, rainfall, and soil moisture most frequently occurred in the N days preceding confirmed rice disease outbreaks? | Complex-Inferential | SensorObservation, DiseaseOutbreak, EnvironmentalVariable, TimeInterval, `preceded`, `occurredAt` | Supports temporal aggregation and outbreak-risk analysis. |

---

# 5. Genomic / Tabular-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which resistance genes are associated with a given rice variety or cultivar? | Simple | RiceVariety, ResistanceGene, `hasResistanceGene` | Establishes genotype-level variety information. |
| CQ-GEN-02 | Which rice varieties are recorded as resistant or susceptible to rice blast? | Relational | RiceVariety, ResistanceTrait, Disease, `hasResistanceTrait`, `resistanceAgainst` | Supports variety selection and resistance-aware diagnosis. |
| CQ-GEN-03 | Which rice varieties carry genes reported to confer resistance to bacterial leaf blight? | Relational | RiceVariety, ResistanceGene, Disease, `hasResistanceGene`, `confersResistanceTo` | Connects variety genotype with disease resistance. |
| CQ-GEN-04 | Which rice varieties provide resistance to the largest number of diseases represented in the KG? | Complex-Inferential | RiceVariety, ResistanceGene/ResistanceTrait, Disease, `confersResistanceTo`, `resistanceAgainst` | Supports ranking varieties by breadth of resistance. |

---

# 6. Cross-Modal / Fusion Competency Questions

## 6.1 Text × Image

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 | Which diseases or pests described in the literature have symptoms matching those annotated in a given rice image? | Relational | ImageObservation, Symptom, Document, Disease/Pest, `depictsSymptom`, `reportsSymptom` | Aligns visual evidence with textual domain knowledge. |
| CQ-MM-02 | Does the lesion morphology visible in an image correspond to published descriptions of rice blast, bacterial leaf blight, or another candidate disease? | Relational | ImageObservation, VisualFeature, Document, Disease, `hasVisualFeature`, `reportsSymptom` | Tests semantic agreement between image observations and literature. |
| CQ-MM-03 | Which candidate diseases should be included in a differential diagnosis when an image contains symptoms that the literature reports for multiple diseases? | Complex-Inferential | ImageObservation, Symptom, Document, Disease, `depictsSymptom`, `reportsSymptom`, `evidenceFor` | Requires cross-modal candidate generation rather than single-label lookup. |

## 6.2 Image × Sensor

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-04 | Given an image showing blast-like lesions, were the temperature and humidity conditions at the observation site compatible with conditions associated with rice blast? | Relational | ImageObservation, Disease, SensorObservation, EnvironmentalCondition, RiceField, `observedAt`, `favoredBy` | Adds environmental context to image-based diagnosis. |
| CQ-MM-05 | Which disease or pest is best supported when visual symptoms in an image are evaluated together with recent temperature, humidity, rainfall, and soil-moisture measurements? | Complex-Inferential | ImageObservation, SensorObservation, Disease/Pest, Symptom, EnvironmentalCondition, `evidenceFor`, `favoredBy` | Tests two-modal evidence fusion for diagnosis. |
| CQ-MM-06 | Do similar symptom images collected at different rice fields occur under similar environmental conditions? | Complex-Inferential | ImageObservation, Symptom, RiceField, SensorObservation, EnvironmentalCondition, `observedAt`, `depictsSymptom` | Supports cross-location pattern discovery between phenotype and environment. |

## 6.3 Image × Genomic / Tabular

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-07 | Given an image-supported diagnosis of rice blast, does the observed rice variety carry genes or traits associated with blast resistance? | Relational | ImageObservation, Diagnosis, Disease, RiceVariety, ResistanceGene/ResistanceTrait, `diagnoses`, `hasResistanceGene`, `confersResistanceTo` | Connects observed phenotype with expected genotype-derived resistance. |
| CQ-MM-08 | Which rice varieties show disease symptoms in field images despite being recorded as resistant to the same disease? | Complex-Inferential | ImageObservation, RiceVariety, Disease, ResistanceTrait, `depictsSymptom`, `resistanceAgainst` | Identifies phenotype–resistance inconsistencies and possible resistance breakdown. |

## 6.4 Sensor × Genomic / Tabular

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-09 | Which rice varieties with known resistance to a target disease were grown under environmental conditions favorable to that disease? | Relational | RiceVariety, Disease, ResistanceTrait, RiceField, SensorObservation, EnvironmentalCondition, `resistanceAgainst`, `favoredBy` | Measures resistance under meaningful environmental exposure. |
| CQ-MM-10 | Under disease-favorable environmental conditions, which rice varieties exhibit the lowest frequency of confirmed disease cases? | Complex-Inferential | RiceVariety, SensorObservation, Diagnosis, Disease, EnvironmentalCondition, `observedAt`, `diagnoses` | Supports field-level comparison of variety performance under disease pressure. |

## 6.5 Text × Genomic / Tabular

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-11 | Which resistance genes reported in scientific literature are present in rice varieties represented in the KG? | Relational | Document, ResistanceGene, RiceVariety, `reportsGene`, `hasResistanceGene` | Grounds genomic records in documented evidence. |
| CQ-MM-12 | Which rice varieties contain genes or resistance traits that published sources associate with resistance to pathogens represented in the KG? | Relational | Document, RiceVariety, ResistanceGene/ResistanceTrait, Pathogen, Disease, `reportsGene`, `confersResistanceTo`, `causedBy` | Connects literature, genotype, pathogen, and disease knowledge. |

## 6.6 Text × Sensor

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-13 | Do recent field temperature and humidity observations fall within environmental conditions reported in the literature as favorable for a target disease or pest? | Relational | Document, EnvironmentalCondition, SensorObservation, Disease/Pest, `reportsCondition`, `favoredBy` | Grounds sensor interpretation in documented epidemiological knowledge. |

## 6.7 Three-Way Fusion

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-14 | Given an image showing blast-like lesions and recent high humidity, which candidate diseases are jointly supported by the image evidence, sensor observations, and published symptom/environment descriptions? | Complex-Inferential | ImageObservation, SensorObservation, Document, Symptom, EnvironmentalCondition, Disease, `supportedBy`, `reportsSymptom`, `favoredBy` | Tests three-modal evidence integration for explainable diagnosis. |
| CQ-MM-15 | For a field image showing symptoms consistent with bacterial leaf blight, which rice varieties represented in the KG possess relevant resistance genes or traits when the environmental conditions at the field are also considered? | Complex-Inferential | ImageObservation, SensorObservation, RiceVariety, ResistanceGene/ResistanceTrait, Disease, `hasResistanceGene`, `confersResistanceTo`, `observedAt` | Supports diagnosis combined with resistance-aware variety analysis. |
| CQ-MM-16 | Which rice varieties repeatedly exhibit disease symptoms in field images under disease-favorable environmental conditions despite carrying reported resistance genes or traits? | Complex-Inferential | ImageObservation, SensorObservation, RiceVariety, ResistanceGene/ResistanceTrait, Disease, `depictsSymptom`, `favoredBy`, `confersResistanceTo` | Detects possible resistance breakdown or genotype–phenotype inconsistencies. |

## 6.8 Four-Way Fusion

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-17 | Given a field image showing disease or pest symptoms, environmental observations from the preceding N days, the rice variety or genotype grown at the field, and relevant knowledge extracted from literature, which diagnosis is best supported by the combined evidence and what management options are documented for it? | Complex-Inferential | ImageObservation, SensorObservation, RiceVariety, ResistanceGene/ResistanceTrait, Document, Disease/Pest, Diagnosis, ManagementPractice, `supportedBy`, `diagnoses`, `managedBy` | Tests the central four-modal reasoning capability that justifies construction of a unified multimodal KG. |

---

# 7. Modality-Pair and Fusion Coverage Summary

| Modality Combination | CQ IDs |
|---|---|
| Text only | CQ-TXT-01 – CQ-TXT-06 |
| Image only | CQ-IMG-01 – CQ-IMG-05 |
| Sensor/environment only | CQ-ENV-01 – CQ-ENV-04 |
| Genomic/tabular only | CQ-GEN-01 – CQ-GEN-04 |
| Text × Image | CQ-MM-01, CQ-MM-02, CQ-MM-03 |
| Image × Sensor | CQ-MM-04, CQ-MM-05, CQ-MM-06 |
| Image × Genomic/Tabular | CQ-MM-07, CQ-MM-08 |
| Sensor × Genomic/Tabular | CQ-MM-09, CQ-MM-10 |
| Text × Genomic/Tabular | CQ-MM-11, CQ-MM-12 |
| Text × Sensor | CQ-MM-13 |
| Text × Image × Sensor | CQ-MM-14 |
| Image × Sensor × Genomic/Tabular | CQ-MM-15, CQ-MM-16 |
| Text × Image × Sensor × Genomic/Tabular | CQ-MM-17 |

### Distribution

| Category | Number of CQs | Share |
|---|---:|---:|
| Text-grounded | 6 | 16.7% |
| Image-grounded | 5 | 13.9% |
| Sensor/environment-grounded | 4 | 11.1% |
| Genomic/tabular-grounded | 4 | 11.1% |
| Cross-modal/fusion | 17 | 47.2% |
| **Total** | **36** | **100%** |

The cross-modal share is intentionally the largest because the research value of the MMKG depends on its ability to semantically integrate evidence across modalities rather than merely store four independent datasets.

---

# 8. Implied Core Ontology Requirements

The competency questions imply at least the following classes:

```text
Disease
Pest
Pathogen
Symptom
VisualFeature
RicePlant
RiceVariety
PlantOrgan
GrowthStage
ResistanceGene
ResistanceTrait
ImageObservation
SensorObservation
FieldObservation
EnvironmentalCondition
RiceField
Document
Diagnosis
DiseaseOutbreak
ManagementPractice
Evidence
TimeInstant
TimeInterval
```

Core relations include:

```text
Disease --causedBy--> Pathogen
Disease/Pest --hasSymptom--> Symptom
Disease/Pest --affectsOrgan--> PlantOrgan
Disease/Pest --favoredBy--> EnvironmentalCondition
Disease/Pest --managedBy--> ManagementPractice

ImageObservation --depictsSymptom--> Symptom
ImageObservation --depictsOrgan--> PlantOrgan
ImageObservation --hasVisualFeature--> VisualFeature
ImageObservation --observedAt--> RiceField

SensorObservation --observedAt--> RiceField
SensorObservation --measures--> EnvironmentalCondition
SensorObservation --observedDuring--> TimeInterval

RicePlant --hasVariety--> RiceVariety
RiceVariety --hasResistanceGene--> ResistanceGene
ResistanceGene --confersResistanceTo--> Disease
RiceVariety --hasResistanceTrait--> ResistanceTrait
ResistanceTrait --resistanceAgainst--> Disease

Document --reportsDisease--> Disease
Document --reportsSymptom--> Symptom
Document --reportsCondition--> EnvironmentalCondition

Diagnosis --diagnoses--> Disease/Pest
Diagnosis --supportedBy--> Evidence
```

---

# 9. Testability and Evaluation Implications

Each CQ is intentionally phrased so that its answer can, in principle, be retrieved from the KG through SPARQL or an equivalent graph-query language. Simple CQs require direct lookup or one-hop traversal; relational CQs generally require two- to three-hop graph traversal; complex-inferential CQs require aggregation, ranking, temporal filtering, cross-modal evidence comparison, or graph reasoning.

The CQ set can therefore support at least three evaluation dimensions:

1. **CQ answerability:** whether the ontology and populated KG contain the classes, relations, and values necessary to answer each CQ.
2. **CQ correctness:** whether query results agree with expert-reviewed or source-grounded expected answers.
3. **Cross-modal coverage:** whether each required modality combination has actual linked data rather than isolated modality-specific records.

---

# 10. Scope Boundary Note

The Rice-MMKG is **in scope** for semantic representation and integration of rice diseases, major rice pests, symptoms and damage, causal pathogens, plant organs, rice varieties and resistance information, environmental observations, field images, documented management practices, diagnosis evidence, spatial context, and temporal context. It is also in scope to support formal querying, differential diagnosis, multimodal evidence fusion, and resistance-aware decision support.

The KG is **out of scope** for autonomous pesticide prescription, economic optimization of entire farming systems, real-time robotic actuation, whole-genome sequence interpretation at raw nucleotide level, or causal claims that cannot be supported by the available evidence. CQs CQ-ENV-04, CQ-MM-06, CQ-MM-08, CQ-MM-10, CQ-MM-14, CQ-MM-15, CQ-MM-16, and especially CQ-MM-17 may be infeasible or only partially answerable unless image, environmental, variety/genotype, location, time, and diagnosis records can be aligned at compatible field and observation levels. These questions should therefore be treated as priority targets during the subsequent data-source feasibility assessment.

---

# 11. Recommended Next Step

The next research artifact should be a **CQ-to-Data-Source Feasibility Matrix** with columns such as:

| CQ ID | Required Modality | Required Entities | Required Relations | Spatial Link Required | Temporal Link Required | Candidate Dataset | Feasibility |
|---|---|---|---|---|---|---|---|
| CQ-MM-04 | Image + Sensor | ImageObservation, SensorObservation, Disease, RiceField | `observedAt`, `favoredBy` | Yes | Yes | TBD | A/B/C |
| CQ-MM-07 | Image + Genomic | ImageObservation, RiceVariety, ResistanceGene, Disease | `hasResistanceGene`, `confersResistanceTo` | Preferable | Preferable | TBD | A/B/C |
| CQ-MM-17 | Text + Image + Sensor + Genomic | All core multimodal entities | Evidence-fusion relations | Yes | Yes | TBD | A/B/C |

Recommended feasibility coding:

- **A — Immediately feasible**
- **B — Feasible after entity/time/location alignment**
- **C — Currently infeasible or aspirational**

This feasibility audit should be completed before committing to full four-modal implementation.
