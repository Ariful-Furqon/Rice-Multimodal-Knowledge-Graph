# Ontology Requirements Specification: Rice Pest & Disease Multimodal Knowledge Graph

*(Generated based on the expert prompt provided in `rice_mmkg_cq_prompt.md`)*

## 1. Purpose and Scope Restatement
The purpose of this Multimodal Knowledge Graph (KG) is to support early diagnosis, predictive monitoring, and precision management of major rice pests and diseases (e.g., Rice Blast, Bacterial Leaf Blight, Tungro Virus, Brown Planthopper). By semantically integrating scientific literature (Text), field symptom photography (Image), agroclimatic IoT time-series (Sensor/Environmental), and varietal resistance profiles (Genomic/Tabular), this KG empowers agricultural researchers, extension officers, and smart-farming systems to make comprehensive, cross-modal decisions. 
*Assumptions Made:* As specific inputs were left open, we have targeted major common tropical lowland rice pests/diseases, assumed access to standard IoT, imaging, and genomic datasets (e.g., IRRI varietal data), and targeted alignment with AGROVOC, Crop Ontology (CO), and Plant Phenotype Ontology (PPO).

## 2. Competency Questions (CQs)

### A. Text-Grounded CQs
| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal pathogen of Rice Blast? | Simple | `Disease`, `causedBy`, `Pathogen` | Establishes baseline taxonomic knowledge from scientific literature. |
| CQ-TXT-02 | Which pest species act as vectors for the Rice Tungro Virus? | Relational | `Pest`, `vectorFor`, `Virus` | Identifies epidemiological pathways based on entomological texts. |
| CQ-TXT-03 | What are the recommended chemical and cultural treatments for sheath blight documented in recent extension reports? | Simple | `Disease`, `hasTreatment`, `Treatment`, `Document` | Connects diagnosis to actionable management practices. |
| CQ-TXT-04 | Which diseases share overlapping early-stage leaf lesion descriptions in plant pathology bulletins? | Relational | `Disease`, `hasSymptomDescription`, `Symptom` | Highlights potential textual ambiguities requiring disambiguation via other modalities. |
| CQ-TXT-05 | Based on historical surveillance texts, what is the typical temporal progression of symptoms for Bacterial Leaf Blight? | Complex | `Disease`, `hasSymptomProgression`, `TemporalStage` | Enables reasoning over time based on narrative textual reporting. |

### B. Image-Grounded CQs
| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Does the provided leaf image exhibit the spindle-shaped spots characteristic of Rice Blast? | Simple | `Image`, `depictsSymptom`, `SymptomFeature` | Tests baseline image-classification/retrieval mapping in the KG. |
| CQ-IMG-02 | Which field images show simultaneous occurrence of Brown Planthopper damage and healthy panicles? | Relational | `Image`, `depictsDamage`, `Pest`, `PlantPart` | Tests multi-object localization and relation extraction within a single image. |
| CQ-IMG-03 | What percentage of the leaf area in image X shows visible chlorosis or necrotic tissue? | Simple | `Image`, `hasAffectedArea`, `QuantitativeValue` | Extracts quantitative severity metrics directly from visual evidence. |
| CQ-IMG-04 | Retrieve all close-up images that exhibit both yellowing of the leaf tip and leaf rolling. | Relational | `Image`, `depictsPhenotype`, `LeafTrait` | Allows researchers to query a visual database using specific morphological constraints. |
| CQ-IMG-05 | Rank the provided set of historical field images by the severity of sheath blight symptoms based on lesion area coverage. | Complex | `Image`, `hasSeverityRank`, `Disease` | Enables visual severity progression tracking over a dataset. |

### C. Sensor/Environmental-Grounded CQs
| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What was the average relative humidity recorded by Node_A over the past 7 days? | Simple | `SensorNode`, `recordsMeasurement`, `Humidity` | Validates retrieval of time-series aggregations. |
| CQ-ENV-02 | During which intervals did temperature exceed 30°C concurrently with soil moisture dropping below 20%? | Relational | `TimeInterval`, `hasTemperature`, `hasSoilMoisture` | Identifies compound environmental stressors. |
| CQ-ENV-03 | Which IoT nodes recorded continuous rainfall for more than 48 hours? | Relational | `SensorNode`, `recordsWeatherEvent`, `Duration` | Queries extended weather patterns linked to disease outbreaks. |
| CQ-ENV-04 | Identify sensor locations exhibiting a time-series trend historically associated with increased fungal disease pressure. | Complex | `SensorNode`, `exhibitsTrend`, `DiseaseRisk` | Connects raw sensor streams to predictive environmental profiling. |

### D. Genomic/Tabular-Grounded CQs
| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which rice varieties in the tabular dataset carry the Pi9 resistance gene? | Simple | `RiceVariety`, `hasResistanceGene`, `Gene` | Validates basic lookup of genetic profiles. |
| CQ-GEN-02 | What is the average documented yield reduction for variety X when subjected to pest Y? | Relational | `RiceVariety`, `hasYieldPenalty`, `Pest` | Links variety data to structured agronomic performance metrics. |
| CQ-GEN-03 | List cultivars possessing both drought tolerance traits and genetic resistance to Xanthomonas oryzae. | Relational | `RiceVariety`, `hasTrait`, `DroughtTolerance`, `Pathogen` | Queries combined genetic traits for breeding or planting recommendations. |
| CQ-GEN-04 | Which combination of resistance genes provides the broadest spectrum of protection against the recorded Brown Planthopper biotypes? | Complex | `GeneSet`, `confersResistanceTo`, `Biotype` | Enables complex analysis for genetic stack efficacy. |

### E. Cross-Modal / Fusion CQs (Core Requirement)
| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 | Does the visual symptom in Image_X match the textual description of Tungro Virus symptoms found in extension manual Doc_Y? | Relational | `Image`, `Text`, `depictsSymptom`, `describesSymptom` | Validates Image-Text alignment for diagnostic confirmation. |
| CQ-MM-02 | Given a leaf image showing Bacterial Leaf Blight, what were the average temperature and humidity readings in that field for the 14 days prior to capture? | Relational | `Image`, `SensorData`, `capturedAt`, `recordedDuring` | Correlates visual disease manifestation with preceding environmental drivers. |
| CQ-MM-03 | Which rice varieties are described in literature as highly susceptible to stem borers, and what are their corresponding genotypes in the tabular database? | Relational | `Text`, `RiceVariety`, `TabularData`, `hasGenotype` | Links unstructured textual claims to structured genomic records. |
| CQ-MM-04 | Under high-humidity sensor conditions (>85% RH), which genetically resistant cultivars show the least yield penalty in the tabular data? | Relational | `SensorData`, `RiceVariety`, `TabularData`, `hasYield` | Combines environmental context with agronomic performance tables. |
| CQ-MM-05 | Retrieve images of plants belonging to the IR64 variety that exhibit visual signs of sheath blight. | Relational | `Image`, `RiceVariety`, `depictsSymptom` | Allows phenotype-genotype visual inspection. |
| CQ-MM-06 | Based on text reports of pest outbreaks, what is the most common time-series pattern of temperature and soil moisture immediately preceding these events? | Complex | `Text`, `SensorData`, `OutbreakEvent`, `precededBy` | Mines multimodal correlations for predictive modeling. |
| CQ-MM-07 | Given an environmental forecast of sustained high humidity (>90%), which rice varieties have the lowest historical incidence of Rice Blast as evidenced by field images? | Complex | `SensorData`, `RiceVariety`, `Image`, `hasIncidence` | Supports preventative variety selection based on image-confirmed historical data and climate. |
| CQ-MM-08 | Identify the disease most likely affecting Field_Z if the latest sensor readings show high rainfall, current images show water-soaked lesions, and local texts report BLB outbreaks. | Complex | `SensorData`, `Image`, `Text`, `Disease` | Simulates a full multimodal diagnostic recommendation engine. |
| CQ-MM-09 | Which resistance genes are most frequently mentioned in literature alongside images demonstrating successful recovery from Brown Planthopper infestation? | Complex | `Gene`, `Text`, `Image`, `mentionedWith` | Discovers novel phenotype-genotype relationships from combined literature and visual evidence. |
| CQ-MM-10 | For cultivars with the Xa21 gene, is there a correlation between soil pH levels and the severity of leaf yellowing observed in close-up images? | Complex | `RiceVariety`, `Gene`, `SensorData`, `Image` | Investigates GxE (Genotype x Environment) interactions affecting phenotypes visually. |
| CQ-MM-11 | How do the optimal growth temperatures described in agronomy reports for drought-tolerant genotypes compare to the actual sensor readings recorded during the last dry season? | Complex | `Text`, `RiceVariety`, `Gene`, `SensorData` | Compares theoretical textual knowledge with empirical sensor observations. |
| CQ-MM-12 | Given a sudden temperature drop, a text alert for rice bug migration, and images showing early panicle damage, which locally cultivated varieties lacking pest-resistance genes are at highest immediate risk? | Complex | `SensorData`, `Text`, `Image`, `RiceVariety`, `Gene` | Represents the ultimate multimodal decision-support query for precision agriculture. |

## 3. Modality-Pair Coverage Traceability

| Modality Pairing | Covering Competency Question IDs |
|---|---|
| **Text × Image** | CQ-MM-01, CQ-MM-08, CQ-MM-09, CQ-MM-12 |
| **Text × Sensor** | CQ-MM-06, CQ-MM-08, CQ-MM-11, CQ-MM-12 |
| **Text × Genomic** | CQ-MM-03, CQ-MM-09, CQ-MM-11, CQ-MM-12 |
| **Image × Sensor** | CQ-MM-02, CQ-MM-07, CQ-MM-08, CQ-MM-10, CQ-MM-12 |
| **Image × Genomic** | CQ-MM-05, CQ-MM-07, CQ-MM-09, CQ-MM-10, CQ-MM-12 |
| **Sensor × Genomic** | CQ-MM-04, CQ-MM-07, CQ-MM-10, CQ-MM-11, CQ-MM-12 |
| **Three-way / Four-way Fusion** | CQ-MM-07, CQ-MM-08, CQ-MM-09, CQ-MM-10, CQ-MM-11, CQ-MM-12 |

## 4. Scope Boundary Note

**IN SCOPE:** This ontology and knowledge graph are strictly bounded to the diagnosis, environmental etiology, phenotypic expression, and genetic resistance profiling of major rice pests and diseases (e.g., Rice Blast, Bacterial Leaf Blight, Tungro Virus, Brown Planthopper, Stem Borer). Entities modeled include diagnostic imaging traits, agroclimatic variables directly impacting pathogen/pest lifecycles, and specific resistance genes mapped to rice varieties. Alignments with established ontologies (Crop Ontology, AGROVOC, PPO) are prioritized for interoperability. 

**OUT OF SCOPE:** The KG will *not* model downstream agricultural economics (e.g., market pricing, supply chain logistics), broad weed management unrelated to host-vectors, or non-rice cropping systems. 

**FEASIBILITY FLAG:** CQs requiring precise temporal alignment between discrete field images and high-frequency sensor data (e.g., CQ-MM-02, CQ-MM-10) may face data sparsity challenges. Real-world field photography is rarely time-stamped continuously with IoT weather nodes. These queries may require relaxed temporal reasoning windows (e.g., "within 14 days of capture") rather than exact point-in-time alignments.
