# Competency Questions for a Rice Pest & Disease Multimodal Knowledge Graph

## 1. Purpose, Scope, and Working Assumptions

The proposed multimodal knowledge graph (MMKG) is intended to support early diagnosis, evidence integration, and decision-making for rice pest and disease management by plant pathology researchers, agricultural extension officers, and smart-farming/IoT system developers. Its functional scope covers semantically linked evidence from scientific and extension text, field imagery, environmental sensor observations, and genomic/tabular information on rice cultivars, resistance, agronomic traits, and yield outcomes.

Because project-specific input fields were not supplied, the following defaults are assumed:

- **Geographic/agroecological scope:** Indonesia and comparable tropical lowland rice systems in Southeast Asia.
- **Pests and diseases in scope:** major rice diseases and pests including rice blast (*Magnaporthe oryzae*), bacterial leaf blight (*Xanthomonas oryzae* pv. *oryzae*), sheath blight (*Rhizoctonia solani*), rice tungro disease, brown planthopper (*Nilaparvata lugens*), stem borers, and rice bug.
- **Text sources:** scientific literature, extension publications, surveillance reports, and expert-authored diagnostic descriptions.
- **Image sources:** field and close-up images of leaves, stems, panicles, whole plants, pest damage, disease symptoms, and healthy controls.
- **Sensor/environmental sources:** temperature, relative humidity, rainfall, soil moisture, soil pH, and related timestamped agroclimatic observations.
- **Genomic/tabular sources:** cultivar/variety records, genotype and resistance-gene annotations, agronomic trial tables, and yield observations.
- **Ontology alignment:** no project-specific ontology is assumed; where appropriate, concepts should be mapped to established resources such as AGROVOC, Crop Ontology, Plant Trait Ontology, Plant Phenotype Ontology, and compatible disease/phenotype modeling patterns.
- **Target CQ count:** 36 competency questions.
- **Existing CQs:** none supplied; therefore no exclusions for duplication are applied.

The questions below are designed so that each can, in principle, be translated into SPARQL or an equivalent graph-query formalism.

---

## 2. Text-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What pathogen is reported as the causal agent of rice blast, and what taxonomic name is associated with that pathogen in the literature? | Simple | Disease, Pathogen, `causedBy`, Taxon, `hasScientificName`, LiteratureSource | Establishes core disease–pathogen identity and supports terminology normalization across sources. |
| CQ-TXT-02 | Which symptoms are reported in the literature as characteristic of bacterial leaf blight, and on which rice plant organs are they observed? | Relational | Disease, Symptom, PlantOrgan, `hasSymptom`, `observedOn`, LiteratureSource | Defines symptom–organ relations needed for diagnostic reasoning and later image alignment. |
| CQ-TXT-03 | Which management practices are recommended for brown planthopper infestations, and which pest life stages or infestation conditions do those recommendations target? | Relational | Pest, ManagementPractice, LifeStage, InfestationCondition, `managedBy`, `targetsStage`, `recommendedUnder` | Supports evidence-based pest management recommendations and representation of contextual applicability. |
| CQ-TXT-04 | Which rice diseases are described as being favored by prolonged high relative humidity or leaf wetness, and what environmental thresholds or qualitative conditions are reported? | Relational | Disease, EnvironmentalCondition, RelativeHumidity, LeafWetness, Threshold, `favoredBy`, `hasThreshold`, LiteratureSource | Captures environmental risk knowledge expressed in textual sources for integration with sensor observations. |
| CQ-TXT-05 | Among rice blast, bacterial leaf blight, and sheath blight, which symptom descriptions share similar visual terms such as lesions, blighting, or discoloration, and which textual features distinguish them? | Complex-Inferential | Disease, SymptomDescription, DiagnosticFeature, `hasSymptom`, `distinguishedBy`, TextEvidence | Tests whether the KG can compare overlapping symptom descriptions and preserve discriminating textual evidence. |
| CQ-TXT-06 | Which pests or diseases are reported to cause measurable yield loss in tropical lowland rice, and what ranges of yield reduction are associated with documented outbreaks or severity levels? | Complex-Inferential | Pest, Disease, YieldLoss, SeverityLevel, Agroecosystem, `causesYieldLoss`, `observedAtSeverity`, `reportedIn` | Connects diagnostic entities to production impact and enables comparative prioritization of threats. |

---

## 3. Image-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Which disease labels are associated with leaf images that show spindle-shaped lesions with gray or whitish centers and darker margins? | Simple | Image, Disease, VisualSymptom, LesionShape, LesionColor, `depicts`, `hasVisualFeature`, `diagnosedAs` | Tests whether diagnostically meaningful image features can retrieve candidate disease labels. |
| CQ-IMG-02 | Which images depict bacterial leaf blight-like symptoms on rice leaves, and where on the leaf are the visible lesions or blighted regions located? | Relational | Image, Disease, PlantOrgan, LesionRegion, SpatialLocation, `depicts`, `observedOn`, `hasImageRegion` | Requires linking image-level diagnosis to localized visual evidence on plant organs. |
| CQ-IMG-03 | Which images show brown planthopper feeding damage or hopperburn, and what plant-level visual features distinguish these images from healthy-plant baselines? | Relational | Image, PestDamage, Pest, HealthyBaseline, VisualFeature, `depictsDamageBy`, `differsFrom`, `hasVisualFeature` | Supports pest-damage recognition and explicit healthy-vs-damaged comparison. |
| CQ-IMG-04 | Which stem or tiller images are consistent with stem borer damage such as deadheart or whitehead symptoms, and which growth-stage-specific visual cues are present? | Relational | Image, Pest, DamageSymptom, GrowthStage, PlantOrgan, `depictsDamageBy`, `hasSymptom`, `observedAtGrowthStage` | Encodes growth-stage-sensitive image interpretation for a common rice pest. |
| CQ-IMG-05 | Among images labeled as blast, sheath blight, and bacterial leaf blight, which visual feature combinations most consistently separate the three classes? | Complex-Inferential | Image, DiseaseClass, VisualFeature, FeatureCombination, `hasVisualFeature`, `supportsClassification`, `distinguishes` | Tests comparative image evidence and supports interpretable multimodal classification. |
| CQ-IMG-06 | For a set of repeated field images of the same plot, how does visible disease severity change over time, based on the proportion of affected plant area or symptom-bearing organs? | Complex-Inferential | ImageSeries, FieldPlot, Timestamp, DiseaseSeverity, AffectedArea, PlantOrgan, `capturedAt`, `observesPlot`, `hasSeverity` | Requires temporal ordering and aggregation of image-derived severity estimates. |

---

## 4. Sensor/Environmental-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What were the mean, minimum, and maximum temperature and relative humidity recorded for a specified rice field during a given 24-hour period? | Simple | FieldPlot, SensorObservation, Temperature, RelativeHumidity, Timestamp, `observedAt`, `hasValue` | Verifies basic retrieval and aggregation of environmental time-series observations. |
| CQ-ENV-02 | Which field plots experienced relative humidity above 90% for at least six consecutive hours during the previous seven days? | Complex-Inferential | FieldPlot, RelativeHumidityObservation, Timestamp, Duration, Threshold, `observedAt`, `exceedsThreshold` | Tests threshold detection and temporal-duration reasoning over sensor data. |
| CQ-ENV-03 | Which plots experienced simultaneous high soil moisture and recent rainfall, and how long did those combined conditions persist? | Relational | FieldPlot, SoilMoisture, Rainfall, EnvironmentalEpisode, Duration, `observedAt`, `coOccursWith`, `persistsFor` | Represents compound environmental conditions that may influence disease development. |
| CQ-ENV-04 | Which environmental variables changed most strongly in the 72 hours preceding an identified high-humidity field episode? | Complex-Inferential | SensorVariable, EnvironmentalEpisode, Timestamp, ChangeMagnitude, `precedes`, `measuredBy`, `hasTrend` | Supports temporal comparison and environmental episode characterization independent of diagnosis labels. |
| CQ-ENV-05 | Across multiple seasons, which field locations most frequently experienced combinations of temperature, humidity, and rainfall that satisfy predefined disease-risk thresholds? | Complex-Inferential | FieldLocation, Season, Temperature, RelativeHumidity, Rainfall, RiskThreshold, `satisfiesRiskCondition`, `occursInSeason` | Tests multi-season aggregation and identification of recurrent environmental risk hotspots. |

---

## 5. Genomic/Tabular-Grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which rice varieties in the KG are annotated as carrying resistance genes or loci associated with resistance to rice blast? | Simple | RiceVariety, ResistanceGene, Disease, `carriesGene`, `confersResistanceTo` | Establishes the basic variety–gene–disease resistance path needed for cultivar selection. |
| CQ-GEN-02 | Which rice varieties are recorded as resistant, moderately resistant, susceptible, or highly susceptible to bacterial leaf blight in available screening tables? | Simple | RiceVariety, Disease, ResistancePhenotype, ScreeningRecord, `hasResistancePhenotype`, `evaluatedFor` | Supports standardized retrieval of categorical resistance phenotypes from tabular data. |
| CQ-GEN-03 | Which varieties combine documented blast resistance with above-median yield performance in tropical lowland trial environments? | Complex-Inferential | RiceVariety, ResistanceTrait, YieldObservation, TrialEnvironment, `resistantTo`, `hasYield`, `evaluatedIn` | Tests integration and ranking within structured genomic/agronomic records. |
| CQ-GEN-04 | Which resistance genes or QTLs co-occur most frequently among varieties that show multi-disease resistance to blast, bacterial leaf blight, and/or tungro? | Complex-Inferential | ResistanceGene, QTL, RiceVariety, Disease, `carriesGene`, `associatedWithResistance`, `resistantTo` | Supports comparative genotype analysis and identification of candidate resistance combinations. |
| CQ-GEN-05 | For each rice variety, what agronomic traits and yield outcomes are recorded across trial locations, seasons, or management regimes, and which traits vary most across contexts? | Complex-Inferential | RiceVariety, AgronomicTrait, YieldObservation, Trial, Location, Season, ManagementRegime, `hasTrait`, `hasYield`, `evaluatedIn` | Verifies context-aware representation of tabular phenotypes and performance data. |

---

## 6. Cross-Modal / Fusion Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 | Given a rice leaf image showing spindle-shaped lesions and recent field humidity above 90%, which disease is most strongly supported by both visual evidence and environmental risk knowledge? | Complex-Inferential | Image, VisualSymptom, Disease, RelativeHumidityObservation, EnvironmentalCondition, `depicts`, `hasVisualFeature`, `favoredBy`, `supportsDiagnosis` | Demonstrates the diagnostic value of combining image evidence with environmental context. |
| CQ-MM-02 | For an image provisionally diagnosed as bacterial leaf blight, which literature-described symptoms match the visible features, and which symptoms expected from the literature are absent or unobserved? | Relational | Image, Disease, VisualSymptom, TextSymptomDescription, `depicts`, `matchesDescription`, `expectedFor`, `absentFromObservation` | Tests explicit alignment between textual diagnostic knowledge and observed image features. |
| CQ-MM-03 | Which rice varieties carry documented resistance to the disease most consistent with a submitted leaf image, and what resistance genes are recorded for those varieties? | Relational | Image, Disease, RiceVariety, ResistanceGene, `supportsDiagnosis`, `resistantTo`, `carriesGene` | Connects visual diagnosis directly to genomic resistance information for decision support. |
| CQ-MM-04 | For field plots with images showing increasing sheath blight severity, what temperature, humidity, rainfall, and soil-moisture patterns were recorded during the preceding seven days? | Complex-Inferential | FieldImage, DiseaseSeverity, FieldPlot, SensorObservation, Timestamp, `observesPlot`, `hasSeverity`, `precededBy`, `measuredAt` | Links temporal image progression to environmental histories relevant to outbreak analysis. |
| CQ-MM-05 | Which literature-reported environmental conditions for rice blast are also observed in sensor data from plots whose images were confirmed as blast-positive? | Complex-Inferential | LiteratureSource, Disease, EnvironmentalCondition, SensorObservation, Image, FieldPlot, `reportsRiskCondition`, `observedAt`, `confirmedByImage` | Evaluates whether empirical field conditions agree with textual disease-risk knowledge. |
| CQ-MM-06 | Among rice varieties planted in plots with high brown planthopper pressure, which varieties show less severe image-observed hopperburn under comparable environmental conditions? | Complex-Inferential | RiceVariety, FieldPlot, Pest, ImageDamageSeverity, SensorCondition, `plantedIn`, `infestedBy`, `hasDamageSeverity`, `observedUnder` | Supports comparative cultivar performance while controlling for field environment. |
| CQ-MM-07 | Given a suspected tungro case from plant images, which textual symptom descriptions support the diagnosis and which varieties in the affected field are recorded as resistant or susceptible to tungro? | Relational | Image, RiceTungroDisease, TextEvidence, RiceVariety, ResistancePhenotype, `supportsDiagnosis`, `matchesDescription`, `plantedIn`, `hasResistancePhenotype` | Combines visual, textual, and varietal evidence for field-level diagnosis and risk interpretation. |
| CQ-MM-08 | Which diseases have similar image-visible leaf symptoms but can be distinguished using environmental sensor conditions and pathogen descriptions from text sources? | Complex-Inferential | Disease, ImageFeature, SensorCondition, Pathogen, TextDescription, `sharesVisualFeature`, `favoredBy`, `causedBy`, `distinguishedBy` | Tests multimodal differential diagnosis when image evidence alone is ambiguous. |
| CQ-MM-09 | In historical field records, which combinations of temperature, relative humidity, rainfall, and soil moisture during the previous seven days are most strongly associated with subsequent increases in image-derived blast severity? | Complex-Inferential | HistoricalFieldRecord, SensorObservation, ImageSeries, BlastSeverity, TemporalWindow, `precedes`, `associatedWith`, `hasSeverityTrend` | Enables data-driven outbreak-risk analysis using synchronized sensor and image histories. |
| CQ-MM-10 | Which management practices recommended in extension literature were applied to plots with confirmed brown planthopper damage, and how did subsequent image-derived damage severity change? | Complex-Inferential | ExtensionSource, ManagementPractice, FieldPlot, PestDamageImage, Timestamp, `recommends`, `appliedTo`, `followedBy`, `hasDamageSeverity` | Links recommendations, interventions, and observed outcomes to assess practice effectiveness. |
| CQ-MM-11 | Which rice varieties carrying blast-resistance genes nevertheless showed blast symptoms in field images, and under what environmental conditions did those apparent resistance breakdowns occur? | Complex-Inferential | RiceVariety, ResistanceGene, Disease, Image, SensorObservation, `carriesGene`, `resistantTo`, `showsSymptom`, `observedUnder` | Supports investigation of genotype-by-environment interactions and possible resistance breakdown. |
| CQ-MM-12 | For plots affected by bacterial leaf blight, how do image-derived disease severity, cultivar resistance class, and yield loss relate across locations or seasons? | Complex-Inferential | FieldPlot, Disease, ImageSeverity, RiceVariety, ResistancePhenotype, YieldLoss, Location, Season, `hasSeverity`, `hasResistancePhenotype`, `hasYieldLoss` | Integrates phenotype, genotype/tabular, and outcome data for comparative epidemiological analysis. |
| CQ-MM-13 | Which visual symptoms, sensor conditions, and cultivar genotypes jointly characterize field cases with the highest observed yield losses from rice pests or diseases? | Complex-Inferential | ImageFeature, SensorCondition, RiceVariety, Genotype, YieldLoss, PestOrDisease, `hasVisualFeature`, `observedUnder`, `hasGenotype`, `causesYieldLoss` | Exercises multi-factor fusion and ranking across all major evidence types except text. |
| CQ-MM-14 | For each major disease, what combination of literature-supported symptoms, representative image features, environmental risk conditions, and resistance genes provides the most complete evidence profile in the KG? | Complex-Inferential | Disease, TextSymptom, ImageFeature, EnvironmentalCondition, ResistanceGene, `hasSymptom`, `depictedBy`, `favoredBy`, `hasResistanceGeneEvidence` | Provides a four-modal completeness test and exposes missing evidence dimensions for each disease. |

---

## 7. Modality-Pair and Fusion Coverage Summary

| Modality Combination | CQ IDs Exercising the Combination |
|---|---|
| Text × Image | CQ-MM-02, CQ-MM-05, CQ-MM-07, CQ-MM-08, CQ-MM-14 |
| Text × Sensor/Environmental | CQ-MM-05, CQ-MM-08, CQ-MM-14 |
| Text × Genomic/Tabular | CQ-MM-07, CQ-MM-14 |
| Image × Sensor/Environmental | CQ-MM-01, CQ-MM-04, CQ-MM-05, CQ-MM-06, CQ-MM-08, CQ-MM-09, CQ-MM-11, CQ-MM-12, CQ-MM-13, CQ-MM-14 |
| Image × Genomic/Tabular | CQ-MM-03, CQ-MM-06, CQ-MM-07, CQ-MM-11, CQ-MM-12, CQ-MM-13, CQ-MM-14 |
| Sensor/Environmental × Genomic/Tabular | CQ-MM-06, CQ-MM-11, CQ-MM-12, CQ-MM-13, CQ-MM-14 |
| Text × Image × Sensor | CQ-MM-05, CQ-MM-08, CQ-MM-14 |
| Text × Image × Genomic/Tabular | CQ-MM-07, CQ-MM-14 |
| Image × Sensor × Genomic/Tabular | CQ-MM-06, CQ-MM-11, CQ-MM-12, CQ-MM-13, CQ-MM-14 |
| Text × Sensor × Genomic/Tabular | CQ-MM-14 |
| Four-way: Text × Image × Sensor × Genomic/Tabular | CQ-MM-14 |

### Coverage Distribution

| Category | Number of CQs | Share of Total |
|---|---:|---:|
| Text-grounded | 6 | 16.7% |
| Image-grounded | 6 | 16.7% |
| Sensor/environmental-grounded | 5 | 13.9% |
| Genomic/tabular-grounded | 5 | 13.9% |
| Cross-modal/fusion | 14 | 38.9% |
| **Total** | **36** | **100%** |

This distribution intentionally gives the largest share to fusion questions while retaining sufficient unimodal questions to validate modality-specific ontology requirements.

---

## 8. Scope Boundary Note

**In scope** are rice pest and disease entities; causal pathogens and pests; diagnostic symptoms and damage phenotypes; plant organs and growth stages; field images and image-derived observations; timestamped environmental measurements; cultivar, genotype, resistance-gene, agronomic, and yield records; literature-derived claims; field plots, locations, seasons, and management interventions; and explicit provenance linking each assertion to its source or observation. The KG should support diagnostic retrieval, differential diagnosis, temporal and environmental risk analysis, cultivar-resistance queries, and multimodal evidence fusion, while aligning reusable terms with established agricultural and phenotype ontologies where practical.

**Out of scope**, unless additional data are explicitly added, are autonomous pesticide prescription, economic optimization, full farm-enterprise planning, molecular pathway simulation, pathogen genome assembly, remote-sensing modalities not represented in the input data, and causal claims that cannot be supported by observational or experimental provenance. Several complex CQs may be infeasible without sufficiently aligned longitudinal data: **CQ-MM-09** requires synchronized historical sensor and image series; **CQ-MM-10** requires intervention timestamps and follow-up imagery; **CQ-MM-11** requires verified cultivar/genotype identity plus field disease observations; **CQ-MM-12** and **CQ-MM-13** require plot-level linkage among images, cultivar records, environmental observations, and yield; and **CQ-MM-14** requires adequate coverage in all four modalities. These CQs should therefore also be treated as data-readiness tests during KG construction.

---

## 9. Ontology-Engineering Implications

The CQs imply that the ontology should distinguish at least the following high-level classes: `RicePlant`, `RiceVariety`, `Pest`, `Disease`, `Pathogen`, `Symptom`, `DamagePhenotype`, `PlantOrgan`, `GrowthStage`, `Image`, `ImageRegion`, `VisualFeature`, `Sensor`, `SensorObservation`, `EnvironmentalCondition`, `FieldPlot`, `Location`, `Season`, `ResistanceGene`, `QTL`, `ResistancePhenotype`, `AgronomicTrait`, `YieldObservation`, `ManagementPractice`, `LiteratureSource`, and `ProvenanceRecord`.

Core relations should include, or be alignable to, properties equivalent to: `causedBy`, `hasSymptom`, `observedOn`, `depicts`, `hasVisualFeature`, `observedAt`, `measuredAt`, `favoredBy`, `precedes`, `plantedIn`, `carriesGene`, `confersResistanceTo`, `hasResistancePhenotype`, `hasYield`, `managedBy`, `appliedTo`, `reportedIn`, `supportedBy`, and `derivedFrom`. Reified observation or assertion patterns will likely be necessary where confidence scores, timestamps, provenance, spatial scope, modality, or conflicting evidence must be represented explicitly.
