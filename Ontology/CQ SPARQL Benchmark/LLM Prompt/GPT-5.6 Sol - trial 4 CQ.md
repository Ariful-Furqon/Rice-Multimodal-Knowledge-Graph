# Competency Questions for a Rice Pest & Disease Multimodal Knowledge Graph

## 1. Purpose, Scope, and Assumptions

The proposed multimodal knowledge graph (MMKG) is intended to support early diagnosis, evidence integration, and decision-making for rice pest and disease management by semantically linking textual knowledge, field imagery, environmental sensor observations, and genomic/tabular cultivar data. Its functional scope is defined through competency questions (CQs) that can, in principle, be translated into formal graph queries and used to drive ontology design, multimodal alignment, and evaluation.

Because the input template did not specify project-specific values, the following defaults are assumed:

- **Primary end users:** plant pathology researchers, agricultural extension officers, and smart-farming/IoT system developers.
- **Geographic/agroecological scope:** Indonesia and comparable Southeast Asian tropical lowland rice-production systems.
- **Pests and diseases in scope:** major rice diseases and insect pests including rice blast (*Magnaporthe oryzae*), bacterial leaf blight (*Xanthomonas oryzae* pv. *oryzae*), sheath blight (*Rhizoctonia solani*), rice tungro disease, brown planthopper (*Nilaparvata lugens*), yellow stem borer (*Scirpophaga incertulas*), and rice bug (*Leptocorisa* spp.).
- **Available modality classes:** scientific/extension text, symptom and damage imagery, agroclimatic sensor time series, and cultivar/genotype/resistance plus agronomic tabular data.
- **Target number of CQs:** 40.
- **Ontology alignment:** align, where semantically appropriate, with resources such as AGROVOC, Crop Ontology, Plant Trait Ontology, Plant Phenotype Ontology (PPO), and relevant disease/phenotype ontology design patterns.
- **Previously drafted CQs:** none supplied.

---

## 2. Text-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What pathogen is reported as the causal agent of rice blast? | Simple | Disease, Pathogen, `causedBy`, ScientificName | Tests the KG's ability to represent canonical disease–pathogen causation. |
| CQ-TXT-02 | Which symptoms are reported in the literature as characteristic of bacterial leaf blight on rice leaves? | Simple | Disease, Symptom, PlantOrgan, `hasSymptom`, `affectsOrgan`, TextSource | Supports symptom-based diagnostic knowledge grounded in textual evidence. |
| CQ-TXT-03 | Which rice pests are reported to cause hopperburn, deadheart, whitehead, or grain-sucking damage, and which damage type is associated with each pest? | Relational | Pest, DamageSymptom, PlantOrgan, `causesDamage`, `affectsOrgan` | Requires explicit pest-to-damage mappings useful for differential diagnosis. |
| CQ-TXT-04 | Which management practices are recommended for sheath blight, and what disease stage or field condition is each practice intended to address? | Relational | Disease, ManagementPractice, DiseaseStage, FieldCondition, `managedBy`, `recommendedUnder` | Captures actionable extension knowledge rather than diagnosis alone. |
| CQ-TXT-05 | Which environmental conditions are described in scientific or extension sources as favoring brown planthopper population increase or outbreak development? | Relational | Pest, EnvironmentalCondition, `favoredBy`, TextSource, EvidenceStatement | Connects narrative agronomic knowledge to formally represented pest ecology. |
| CQ-TXT-06 | Across the textual sources in the KG, which symptoms are shared by two or more rice diseases, and which additional textual signs or contextual features are reported to distinguish them? | Complex-Inferential | Disease, Symptom, DiagnosticFeature, TextSource, `hasSymptom`, `distinguishedBy` | Tests aggregation across sources and supports explainable differential diagnosis. |
| CQ-TXT-07 | Which rice diseases or pests have conflicting management recommendations across literature or extension sources, and what source, location, crop stage, or production context explains the difference? | Complex-Inferential | Disease/Pest, ManagementPractice, TextSource, Location, CropStage, `recommends`, `appliesInContext` | Tests provenance-aware reconciliation of heterogeneous textual knowledge. |

---

## 3. Image-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | What visible lesion shapes, colors, margins, and center patterns are present on the rice leaf in a given field image? | Simple | Image, VisualFeature, Lesion, Color, Shape, `depicts`, `hasVisualFeature` | Establishes explicit representation of low-level diagnostic visual evidence. |
| CQ-IMG-02 | Which rice plant organ—leaf, sheath, stem, panicle, or whole plant—is visibly affected in a given image? | Simple | Image, PlantOrgan, DamageRegion, `depictsOrgan`, `showsAffectedRegion` | Tests localization of symptoms to plant anatomy. |
| CQ-IMG-03 | Does an image show deadheart, whitehead, hopperburn, leaf streaking, spindle-shaped lesions, or sheath lesions, and where is the pattern located? | Relational | Image, VisualSymptom, PlantOrgan, `showsSymptom`, `locatedOn` | Supports structured visual phenotyping needed for diagnosis. |
| CQ-IMG-04 | Which images in the KG depict symptom patterns visually similar to a query image based on lesion morphology and affected plant organ? | Relational | Image, VisualEmbedding/Feature, Symptom, PlantOrgan, `visuallySimilarTo`, `depicts` | Tests image-to-image retrieval and visual similarity links within the graph. |
| CQ-IMG-05 | Among images captured from the same field plot over time, how did the visible severity or spatial extent of symptoms change between observations? | Complex-Inferential | Image, Plot, ObservationTime, Severity, `capturedAt`, `observedOn`, `hasSeverity` | Requires temporal comparison of image-derived disease or damage evidence. |
| CQ-IMG-06 | Which symptom class is most consistently represented across multiple images of the same plant or plot when observations from different viewpoints are aggregated? | Complex-Inferential | ImageSet, Plant/Plot, VisualSymptom, Viewpoint, Confidence, `depicts`, `sameSubjectAs` | Tests multi-image aggregation rather than single-image classification. |
| CQ-IMG-07 | Which images should be treated as healthy-plant baselines for a given growth stage because they show no annotated visible lesion, discoloration, deformation, or pest-damage pattern? | Complex-Inferential | Image, HealthyBaseline, GrowthStage, VisualFeature, `hasGrowthStage`, `lacksVisibleSymptom` | Provides a formal negative-evidence baseline for multimodal comparison and evaluation. |

---

## 4. Sensor / Environmental-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What were the mean, minimum, and maximum temperature and relative humidity recorded for a specified field plot during a given observation window? | Simple | SensorObservation, Temperature, RelativeHumidity, Plot, TimeInterval, `observedAt`, `hasValue` | Tests basic retrieval and aggregation of environmental time-series data. |
| CQ-ENV-02 | During which time intervals did relative humidity remain above a specified threshold for at least a specified number of consecutive hours? | Relational | SensorObservation, RelativeHumidity, Threshold, TimeInterval, `hasValue`, `withinInterval` | Requires temporal continuity reasoning over sensor observations. |
| CQ-ENV-03 | Which field plots experienced the combination of high nighttime humidity, moderate temperature, and recent rainfall during the same multi-day period? | Relational | Plot, Temperature, RelativeHumidity, Rainfall, TimeInterval, `observedAt`, `coOccursWith` | Tests multi-variable environmental condition matching across plots and time. |
| CQ-ENV-04 | Which environmental variable showed the strongest change from its local baseline during the seven days preceding a specified field observation date? | Complex-Inferential | SensorVariable, Baseline, TimeSeries, ObservationDate, `deviatesFrom`, `measuredAt` | Supports anomaly-oriented environmental reasoning without requiring another modality. |
| CQ-ENV-05 | Which plots exhibit recurring microclimatic patterns—such as prolonged leaf-wetness proxies, high humidity, or persistently moist soil—across multiple cropping periods? | Complex-Inferential | Plot, CroppingPeriod, SoilMoisture, Humidity, Rainfall/LeafWetnessProxy, `recursDuring`, `observedAt` | Tests longitudinal environmental pattern discovery relevant to disease-pressure modeling. |

---

## 5. Genomic / Tabular-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which rice varieties in the KG are recorded as carrying a named blast-resistance gene or locus? | Simple | RiceVariety, ResistanceGene/Locus, DiseaseResistance, `carriesGene`, `confersResistanceTo` | Tests direct genotype-to-resistance representation. |
| CQ-GEN-02 | What resistance or susceptibility phenotype is recorded for each rice variety against bacterial leaf blight, blast, brown planthopper, or tungro? | Simple | RiceVariety, Pest/Disease, ResistancePhenotype, `hasResistancePhenotype`, `testedAgainst` | Supports variety selection and genotype–phenotype retrieval. |
| CQ-GEN-03 | Which varieties combine resistance to more than one target pest or disease, and which resistance genes, loci, or scored phenotypes support that classification? | Relational | RiceVariety, ResistanceGene, ResistancePhenotype, Disease/Pest, `carriesGene`, `resistantTo` | Tests multi-trait resistance profiles across structured records. |
| CQ-GEN-04 | Which varieties share the same resistance gene but show different recorded field-resistance scores or yield outcomes? | Relational | RiceVariety, ResistanceGene, ResistanceScore, YieldTrait, `carriesGene`, `hasPhenotype`, `hasYield` | Captures genotype–phenotype and genotype–agronomic discrepancies. |
| CQ-GEN-05 | Which rice varieties provide the best combined profile of multi-disease resistance and yield performance under the available tabular evaluation records? | Complex-Inferential | RiceVariety, DiseaseResistance, YieldTrait, TrialRecord, Ranking, `resistantTo`, `hasYield` | Tests aggregation and ranking across genotype and agronomic performance data. |

---

## 6. Cross-Modal / Fusion Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 | Given a leaf image showing spindle-shaped lesions, which diseases described in text have matching symptom morphology, and what pathogens are associated with those diseases? | Relational | Image, VisualSymptom, TextSymptom, Disease, Pathogen, `showsSymptom`, `matchesDescription`, `causedBy` | Exercises Text×Image fusion for explainable diagnosis. |
| CQ-MM-02 | For an image showing leaf-edge yellowing and blight-like lesions, which textual symptom descriptions best match the image and what alternative diseases share those features? | Complex-Inferential | Image, VisualFeature, SymptomDescription, Disease, DifferentialDiagnosis, `matchesDescription`, `hasSymptom` | Tests ambiguity-aware image–text retrieval for differential diagnosis. |
| CQ-MM-03 | When field images show increasing sheath-lesion severity, what temperature, humidity, rainfall, and soil-moisture conditions were recorded before and during the increase? | Relational | Image, Severity, SensorObservation, Plot, TimeInterval, `capturedAt`, `precededBy`, `observedAt` | Exercises Image×Sensor temporal alignment for outbreak analysis. |
| CQ-MM-04 | Which historical field-image episodes of severe blast symptoms were preceded by the most similar temperature–humidity–rainfall patterns to the current sensor window? | Complex-Inferential | ImageEpisode, BlastSymptom, SensorTimeSeries, Similarity, Plot, `precededBy`, `environmentallySimilarTo` | Supports case-based risk assessment using visual and environmental history. |
| CQ-MM-05 | For plots where hopperburn-like damage is visible in images, do associated textual surveillance reports mention brown planthopper, and do sensor records show environmental conditions reported to favor its population increase? | Complex-Inferential | Image, Hopperburn, SurveillanceReport, BrownPlanthopper, SensorObservation, `mentions`, `showsDamage`, `favoredBy` | Triangulates image, text, and environmental evidence for pest diagnosis. |
| CQ-MM-06 | Given a suspected blast diagnosis supported by image and text evidence, which rice varieties in the KG carry resistance genes or phenotypes associated with blast resistance? | Relational | Image, TextSource, Disease, RiceVariety, ResistanceGene, `supportsDiagnosis`, `carriesGene`, `resistantTo` | Connects diagnosis evidence to genomic decision support. |
| CQ-MM-07 | Which varieties planted in fields with highly blast-favorable environmental conditions nevertheless show low image-observed blast severity, and what resistance genes or phenotypes do those varieties possess? | Complex-Inferential | RiceVariety, Plot, SensorObservation, ImageSeverity, ResistanceGene, `plantedIn`, `exposedTo`, `showsSeverity`, `carriesGene` | Integrates Sensor×Image×Genomic evidence to identify field-effective resistance. |
| CQ-MM-08 | Which varieties show severe disease symptoms in field images despite being recorded as resistant in genomic or tabular data, and under what environmental conditions did those observations occur? | Complex-Inferential | RiceVariety, ResistancePhenotype, ImageSeverity, EnvironmentalCondition, Plot, `recordedAsResistantTo`, `showsSeverity`, `observedUnder` | Detects genotype–field phenotype discordance and possible environmental override. |
| CQ-MM-09 | For a rice plot with suspected bacterial leaf blight, what combination of image features, textual symptom descriptions, and recent sensor conditions supports or weakens the diagnosis? | Complex-Inferential | Plot, Image, TextSymptom, SensorObservation, Disease, Evidence, `supports`, `contradicts`, `observedAt` | Enables explainable multimodal diagnostic evidence synthesis. |
| CQ-MM-10 | Which pest or disease best explains a case where images show whiteheads, text records describe stem-borer injury, and field observations identify damage during the reproductive stage? | Relational | Image, Whitehead, TextSource, StemBorer, GrowthStage, `showsSymptom`, `describes`, `observedAtStage` | Tests fusion of visual, textual, and crop-stage evidence. |
| CQ-MM-11 | Across historical plots, which environmental patterns are statistically associated with subsequent increases in image-derived blast or sheath-blight severity? | Complex-Inferential | SensorTimeSeries, ImageSeverity, Disease, Plot, TimeLag, Association, `precedes`, `associatedWith` | Tests temporal cross-modal aggregation for risk-model evaluation. |
| CQ-MM-12 | Which textual management recommendations are applicable to a currently observed disease case when the diagnosis is supported by images and the field's current environmental conditions are known? | Complex-Inferential | ImageDiagnosis, Disease, SensorObservation, ManagementPractice, TextSource, `recommendedFor`, `applicableUnder` | Links diagnosis and current field context to actionable text-derived management knowledge. |
| CQ-MM-13 | For each rice variety, how does image-observed disease severity compare across fields with similar environmental exposure, and is the ranking consistent with its recorded resistance phenotype? | Complex-Inferential | RiceVariety, ImageSeverity, EnvironmentalExposure, ResistancePhenotype, Plot, `plantedIn`, `hasSeverity`, `hasResistancePhenotype` | Supports fair phenotype comparison while controlling for environmental differences. |
| CQ-MM-14 | Which field cases have concordant evidence across text reports, images, and sensor data for a tungro or brown-planthopper event, and which cases contain conflicting evidence between modalities? | Complex-Inferential | FieldCase, TextReport, ImageEvidence, SensorEvidence, Pest/Disease, Concordance, `supports`, `conflictsWith` | Tests explicit multimodal evidence concordance and conflict representation. |
| CQ-MM-15 | Given a new field image and the previous seven days of sensor data, which historical diagnosed cases are most similar across both visual and environmental features, and what diagnoses were confirmed in their reports? | Complex-Inferential | QueryImage, SensorWindow, HistoricalCase, Similarity, DiagnosisReport, `visuallySimilarTo`, `environmentallySimilarTo`, `confirmedAs` | Provides a realistic retrieval task that justifies joint multimodal representations. |
| CQ-MM-16 | For a disease identified from image and text evidence under the current field's sensor-recorded conditions, which resistant varieties meet a user-specified minimum yield threshold and have evaluation records from comparable environmental conditions? | Complex-Inferential | Disease, ImageEvidence, TextEvidence, SensorObservation, RiceVariety, ResistancePhenotype, YieldTrait, TrialEnvironment, `supportsDiagnosis`, `observedUnder`, `resistantTo`, `hasYield`, `evaluatedUnder` | Exercises all four modalities to connect diagnosis, current environment, genetic resistance, and agronomic performance to context-aware variety selection. |

---

## 7. Modality-Pair and Fusion Coverage Traceability

| Modality Combination | CQ IDs Exercising the Combination |
|---|---|
| Text × Image | CQ-MM-01, CQ-MM-02, CQ-MM-05, CQ-MM-06, CQ-MM-09, CQ-MM-10, CQ-MM-12, CQ-MM-14, CQ-MM-15, CQ-MM-16 |
| Text × Sensor/Environmental | CQ-MM-05, CQ-MM-09, CQ-MM-12, CQ-MM-14, CQ-MM-16 |
| Text × Genomic/Tabular | CQ-MM-06, CQ-MM-16 |
| Image × Sensor/Environmental | CQ-MM-03, CQ-MM-04, CQ-MM-05, CQ-MM-07, CQ-MM-08, CQ-MM-09, CQ-MM-11, CQ-MM-13, CQ-MM-14, CQ-MM-15 |
| Image × Genomic/Tabular | CQ-MM-06, CQ-MM-07, CQ-MM-08, CQ-MM-13, CQ-MM-16 |
| Sensor/Environmental × Genomic/Tabular | CQ-MM-07, CQ-MM-08, CQ-MM-13, CQ-MM-16 |
| Text × Image × Sensor/Environmental | CQ-MM-05, CQ-MM-09, CQ-MM-12, CQ-MM-14, CQ-MM-15, CQ-MM-16 |
| Text × Image × Genomic/Tabular | CQ-MM-06, CQ-MM-16 |
| Image × Sensor/Environmental × Genomic/Tabular | CQ-MM-07, CQ-MM-08, CQ-MM-13 |
| Text × Sensor/Environmental × Genomic/Tabular | CQ-MM-16 |
| Text × Image × Sensor/Environmental × Genomic/Tabular | CQ-MM-16 |

### Distribution Summary

| Category | Count | Share |
|---|---:|---:|
| Text-grounded | 7 | 17.5% |
| Image-grounded | 7 | 17.5% |
| Sensor/environmental-grounded | 5 | 12.5% |
| Genomic/tabular-grounded | 5 | 12.5% |
| Cross-modal/fusion | 16 | 40.0% |
| **Total** | **40** | **100%** |

---

## 8. Scope Boundary Note

**In scope** are formal representations of rice pests and diseases, pathogens, symptoms and damage phenotypes, plant organs and crop stages, field images and image-derived observations, environmental sensor measurements and temporal windows, rice varieties and resistance genes/phenotypes, agronomic/yield records, diagnostic evidence, provenance, and management recommendations. The KG must support both unimodal retrieval and cross-modal linkage at the level of field plot, plant/crop instance, observation time, disease or pest hypothesis, variety, and supporting evidence.

**Out of scope** are autonomous pesticide prescription, economic optimization, farm-finance decisions, mechanistic crop-growth simulation, genomic sequence analysis from raw reads, and direct causal claims that cannot be supported by represented evidence or a specified analytic model. Several complex CQs—especially CQ-ENV-04, CQ-ENV-05, CQ-MM-04, CQ-MM-07, CQ-MM-08, CQ-MM-11, CQ-MM-13, CQ-MM-15, and CQ-MM-16—may be infeasible unless the project has sufficiently dense time-aligned sensor histories, repeated field images, reliable plot/variety identifiers, confirmed diagnoses, and consistent severity annotations. These should therefore be treated as both competency questions and data-readiness checks during ontology and dataset design.
