# Ontology Requirements Specification: Rice Pests & Diseases Multimodal Knowledge Graph

## 1. Knowledge Graph Purpose and Scope
This Multimodal Knowledge Graph (MMKG) is designed to support early diagnosis, predictive modeling, and integrated pest management (IPM) for major rice (*Oryza sativa*) pests and diseases, with a primary focus on tropical lowland ecosystems (e.g., Southeast Asia). By semantically integrating unstructured text (literature/reports), visual evidence (field images), environmental time-series (IoT sensor data), and structured genomic/agronomic records, the KG serves agricultural extension officers, plant pathologists, and precision-agriculture system developers. Entities and relations are aligned where possible with existing standards, including AGROVOC, the Crop Ontology (CO), Plant Phenotype Ontology (PPO), and Plant Trait Ontology (PTO).

## 2. Competency Questions (CQs)

### A. Text-Grounded CQs
| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| **CQ-TXT-01** | What is the causal pathogen of Rice Blast disease? | Simple | `Disease`, `causedBy`, `Pathogen` | Verifies basic taxonomic and etiological facts extractable from literature. |
| **CQ-TXT-02** | Which chemical or biological treatments are recommended for managing the Brown Planthopper (*Nilaparvata lugens*)? | Relational | `Pest`, `hasTreatment`, `Treatment`, `TreatmentType` | Ensures the KG can retrieve agronomic management protocols from extension reports. |
| **CQ-TXT-03** | What are the primary textual descriptors of leaf symptoms caused by Bacterial Leaf Blight? | Relational | `Disease`, `hasSymptomDescription`, `PlantPart`, `TextDescriptor` | Maps qualitative expert descriptions to specific diseases and plant anatomy. |
| **CQ-TXT-04** | Which diseases share the symptom of "chlorotic streaks" on leaves based on published surveillance bulletins? | Complex-Inferential | `Symptom`, `associatedWith`, `Disease`, `hasSource`, `Bulletin` | Tests the KG's ability to group diseases by shared textual symptom patterns. |
| **CQ-TXT-05** | How has the recommended application rate of fungicide X changed in extension reports over the last decade? | Complex-Inferential | `Treatment`, `hasApplicationRate`, `TemporalValidity`, `Report` | Assesses temporal tracking of management practices within text sources. |

### B. Image-Grounded CQs
| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| **CQ-IMG-01** | Does the provided image exhibit spindle-shaped necrotic lesions indicative of Rice Blast? | Simple | `Image`, `depictsSymptom`, `LesionShape`, `Disease` | Confirms linking of visual phenotypic traits (spindle shape) to disease entities. |
| **CQ-IMG-02** | What plant parts (leaf, stem, panicle) are visibly affected in this image of a Tungro-infected crop? | Relational | `Image`, `depictsPlantPart`, `showsDisease`, `Disease` | Validates object-detection/segmentation metadata mapping to plant anatomy ontologies. |
| **CQ-IMG-03** | What is the average lesion area percentage on leaves photographed during the vegetative stage? | Complex-Inferential | `Image`, `hasLesionArea`, `GrowthStage`, `PlantPart` | Tests aggregation of quantitative visual metrics extracted from images across a specific growth stage. |
| **CQ-IMG-04** | Which images in the database depict healthy (asymptomatic) panicles of the IR64 variety? | Relational | `Image`, `depictsPhenotype`, `PlantPart`, `RiceVariety` | Ensures negative baselines (healthy states) are retrievable for machine learning training. |
| **CQ-IMG-05** | Based on bounding box annotations, which pest is visible in this close-up image of the rice stem? | Simple | `ImageAnnotation`, `depictsPest`, `PlantPart`, `Pest` | Verifies direct mapping of visual pest entities to taxonomic nodes. |

### C. Sensor/Environmental-Grounded CQs
| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| **CQ-ENV-01** | What was the average relative humidity recorded by sensor Node-A during the past 7 days? | Simple | `Sensor`, `recordsVariable`, `RelativeHumidity`, `TimeInterval` | Tests basic retrieval of time-series IoT data. |
| **CQ-ENV-02** | Which environmental sensors reported continuous leaf wetness durations exceeding 12 hours? | Relational | `Sensor`, `measuresVariable`, `LeafWetness`, `DurationThreshold` | Identifies specific microclimate conditions necessary for fungal pathogen infection. |
| **CQ-ENV-03** | How many days did the ambient temperature remain between 25°C and 30°C in field plot B during the tillering stage? | Complex-Inferential | `Temperature`, `SensorLocation`, `TimeInterval`, `GrowthStage` | Validates temporal aggregation of sensor data bounded by agronomic growth stages. |
| **CQ-ENV-04** | Which historical time periods show a rapid drop in soil moisture coupled with a spike in ambient temperature? | Complex-Inferential | `SoilMoisture`, `Temperature`, `TimeTrend`, `TimeInterval` | Tests complex event processing and identification of abiotic stress patterns. |
| **CQ-ENV-05** | What is the rainfall accumulation recorded prior to a specified date in region X? | Relational | `Rainfall`, `recordedIn`, `Location`, `TemporalBoundary` | Retrieves precursor environmental conditions relevant for disease forecasting. |

### D. Genomic/Tabular-Grounded CQs
| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| **CQ-GEN-01** | Which rice cultivars carry the *Xa21* resistance gene? | Simple | `RiceVariety`, `hasResistanceGene`, `Gene` | Validates basic lookup of genetic resistance profiles. |
| **CQ-GEN-02** | What is the reported average yield (tons/hectare) for variety Ciherang under irrigated conditions? | Relational | `RiceVariety`, `hasYield`, `AgronomicCondition`, `TabularRecord` | Connects cultivar entities to tabular agronomic performance metrics. |
| **CQ-GEN-03** | Which varieties express resistance to *Magnaporthe oryzae* but susceptibility to *Rhizoctonia solani*? | Complex-Inferential | `RiceVariety`, `hasResistanceTo`, `isSusceptibleTo`, `Pathogen` | Tests multi-hop comparative querying of phenotypic resistance across different pathogens. |
| **CQ-GEN-04** | What are the parent lineages of the high-yielding variety Swarna-Sub1? | Relational | `RiceVariety`, `hasParent`, `Lineage` | Retrieves pedigree information critical for breeding programs. |
| **CQ-GEN-05** | How many distinct genotypes in the database are classified as "early maturing"? | Simple | `RiceVariety`, `hasMaturityTrait`, `TraitCategory` | Groups tabular records by specific categorical agronomic traits. |

### E. Cross-Modal / Fusion CQs
| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| **CQ-MM-01** | Given a leaf image showing spindle-shaped lesions and sensor readings of >90% humidity and 26°C for 3 days, what is the most likely disease? | Complex-Inferential | `ImagePhenotype`, `SensorCondition`, `indicatesDisease`, `Disease` | Core diagnostic CQ linking visual evidence and environmental preconditions to infer disease. |
| **CQ-MM-02** | Which rice varieties carrying the *Bph14* gene have documented field images showing Brown Planthopper damage under drought stress conditions (sensor data)? | Complex-Inferential | `Gene`, `RiceVariety`, `Image`, `SensorCondition`, `PestDamage` | Links genomic (resistance), image (damage), and sensor (drought) modalities to evaluate real-world gene efficacy. |
| **CQ-MM-03** | Do text-based extension reports of Bacterial Leaf Blight outbreaks align temporally and spatially with periods of high rainfall recorded by local IoT sensors? | Complex-Inferential | `ReportDate`, `Location`, `DiseaseOutbreak`, `RainfallSensor` | Fuses text reports with time-series sensor data to validate disease forecasting models. |
| **CQ-MM-04** | For cultivars listed as "susceptible to sheath blight" (genomic/tabular), what is the correlation between average lesion size (from images) and cumulative nitrogen application (from text/agronomic logs)? | Complex-Inferential | `RiceVariety`, `Trait`, `ImageMetric`, `AgronomicLog` | Evaluates the interaction between host genetics, management practices (text), and visual severity (images). |
| **CQ-MM-05** | Are there images in the database showing Tungro virus symptoms in fields where sensor data indicates low temperatures, contradicting standard literature text describing it as a warm-climate disease? | Complex-Inferential | `ImageSymptom`, `Disease`, `TemperatureSensor`, `TextClaim` | Discovers anomalies or novel pathogen behavior by contrasting text-based knowledge with empirical (image/sensor) data. |
| **CQ-MM-06** | Which genomic traits (tabular) are shared by rice plants whose field images show robust panicle development despite text reports of severe stem borer infestations in the region? | Complex-Inferential | `Trait`, `RiceVariety`, `ImageFeature`, `PestReport` | Integrates tabular genetics, image-based yield proxies, and text-based pest pressure. |
| **CQ-MM-07** | Can the onset of "hopperburn" (identified via image sequence) be accurately predicted by tracking the population counts in text bulletins and temperature/humidity trends from sensors over the prior 14 days? | Complex-Inferential | `ImageSequence`, `PestDamage`, `TextBulletin`, `SensorTrend` | A highly complex temporal CQ testing the predictive integration of time-series images, text, and sensors. |
| **CQ-MM-08** | Retrieve all expert text descriptions of *Rhizoctonia solani* symptoms alongside representative images from fields where soil moisture exceeded 40%. | Relational | `Disease`, `TextDescription`, `Image`, `SensorCondition` | A retrieval CQ that curates multimodal educational materials for specific microclimates. |
| **CQ-MM-09** | Identify the top 3 rice varieties (tabular) that maintained high yields during the 2022 season, based on fields with confirmed blast lesions (images) and high rainfall (sensors). | Complex-Inferential | `RiceVariety`, `YieldData`, `ImageFeature`, `SensorData` | Integrates tabular yield, visual disease confirmation, and abiotic sensor data to find resilient cultivars. |
| **CQ-MM-10** | Map the geographic spread of Bacterial Leaf Blight by linking location-tagged textual news reports with geo-referenced images of infected leaves over the 2023 wet season. | Relational | `Location`, `Disease`, `TextReport`, `Image` | Fuses unstructured text and image metadata for spatiotemporal epidemiology. |

## 3. Modality-Pair Coverage Summary

The following table maps the cross-modal Competency Questions to the specific combinations of data modalities they evaluate, ensuring no integration pathways are overlooked.

| Modality Interaction | Relevant CQ IDs |
| :--- | :--- |
| **Image × Sensor** | CQ-MM-01, CQ-MM-08 |
| **Image × Genomic/Tabular** | CQ-IMG-04, CQ-MM-04 |
| **Text × Sensor** | CQ-MM-03 |
| **Text × Image** | CQ-MM-10 |
| **Text × Genomic/Tabular** | CQ-TXT-02 (implicitly via treatments), CQ-GEN-02 |
| **Genomic × Sensor** | CQ-MM-02 (partial), CQ-MM-09 (partial) |
| **Three-Way Fusion (Text/Img/Sens)** | CQ-MM-05, CQ-MM-07 |
| **Three-Way Fusion (Img/Sens/Gen)** | CQ-MM-02, CQ-MM-09 |
| **Three-Way Fusion (Text/Img/Gen)** | CQ-MM-04, CQ-MM-06 |
| **Four-Way Fusion** | Future expansion (Requires highly controlled trial data) |

## 4. Scope Boundary Note

**In Scope:** The MMKG strictly covers major tropical lowland rice pests (e.g., Brown Planthopper, Stem Borers) and diseases (e.g., Rice Blast, Bacterial Leaf Blight, Tungro, Sheath Blight). It is designed to model the relationships between macroscopic phenotypic symptoms (via images), environmental drivers (via localized sensors), genomic resistance profiles (via tabular data), and human-readable knowledge (via text reports/literature). 

**Out of Scope:** The KG currently excludes molecular-level multi-omics (transcriptomics, proteomics) and microscopic pathogen cellular imaging. Economic modeling, market pricing, and broad supply-chain logistics are also explicitly outside the ontology's boundaries. 

**Feasibility Flag:** CQs requiring high-frequency temporal alignment across all modalities simultaneously (e.g., predicting exact dates of hopperburn onset via CQ-MM-07) may be challenging to answer definitively due to the typical sparsity of continuous image time-series in real-world agricultural datasets. These queries will likely require relying on interpolated data or controlled greenhouse subsets.
