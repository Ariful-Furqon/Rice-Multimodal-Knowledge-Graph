# Ontology Requirements Specification: Rice Pest & Disease Multimodal Knowledge Graph

*Based on the expert prompt from `rice_mmkg_cq_prompt.md`.*

## 1. Knowledge Graph Purpose and Scope
The purpose of this Multimodal Knowledge Graph (MMKG) is to support early diagnosis, predictive monitoring, and precision decision-making for rice pest and disease management in Southeast Asian tropical lowland rice systems. By semantically linking text-based agronomic reports, phenotypic field images, environmental IoT sensor streams, and genomic/tabular cultivar data, the KG enables researchers, agricultural extension officers, and smart-farming systems to query complex, cross-modal interactions that drive outbreaks. 

*Assumptions made:* 
- Focus on major common rice pests/diseases: Rice Blast (*Magnaporthe oryzae*), Bacterial Leaf Blight (*Xanthomonas oryzae*), Rice Tungro Virus (RTV), Brown Planthopper (*Nilaparvata lugens*), and Sheath Blight (*Rhizoctonia solani*).
- Ontological alignment targeted for: Crop Ontology (CO), Plant Trait Ontology (TO), Agronomy Ontology (AGRO), and Plant Phenotype Ontology (PPO).
- Target size: 30 Competency Questions (CQs).

---

## 2. Competency Questions (CQs)

### A. Text-Grounded CQs
*Answerable purely from scientific literature, extension reports, and symptom descriptions.*

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-TXT-01** | What is the causal pathogen of bacterial leaf blight (BLB)? | Simple | `Disease`, `causedBy`, `Pathogen` | Establishes baseline taxonomic knowledge of diseases and their biological agents. |
| **CQ-TXT-02** | Which agronomic management practices are recommended in extension bulletins for controlling brown planthopper (BPH) outbreaks? | Relational | `Pest`, `hasRecommendedManagement`, `AgronomicPractice`, `Document` | Links biological threats to actionable mitigation strategies found in literature. |
| **CQ-TXT-03** | What are the primary morphological symptoms of rice tungro spherical virus (RTSV) described in regional surveillance reports? | Simple | `Pathogen`, `hasSymptom`, `MorphologicalTrait`, `Document` | Provides the textual ground truth for disease symptomology. |
| **CQ-TXT-04** | Which diseases are reported to frequently co-occur with sheath blight during the maximum tillering stage? | Relational | `Disease`, `coOccursWith`, `Disease`, `GrowthStage` | Tests the graph's ability to model complex temporal disease interactions. |
| **CQ-TXT-05** | Based on historical literature, what is the chronological progression of rice blast symptoms across seedling, tillering, and heading stages? | Complex-Inferential | `Disease`, `hasSymptomProgression`, `Symptom`, `GrowthStage` | Enables temporal reasoning about disease development based on text rules. |

### B. Image-Grounded CQs
*Answerable purely from visual evidence in field/close-up photographs.*

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-IMG-01** | Does this close-up leaf image exhibit spindle-shaped lesions with grey centers? | Simple | `Image`, `depictsSymptom`, `LesionFeature` | Tests the fundamental capacity to query annotated visual phenotypic traits. |
| **CQ-IMG-02** | Which field-level photographs show generalized chlorosis (yellowing) and stunting characteristic of Tungro? | Relational | `Image`, `showsPhenotype`, `Chlorosis`, `Stunting` | Validates retrieval of macroscopic crop-scale disease indicators. |
| **CQ-IMG-03** | What annotated bounding-box features distinguish the lesions of bacterial leaf blight from bacterial leaf streak on panicle images? | Relational | `Image`, `hasAnnotation`, `BoundingBox`, `LesionType` | Supports computer vision training by retrieving distinct visual differentials. |
| **CQ-IMG-04** | Can the severity of sheath blight damage be ranked (scale 1-9) based on the vertical progression of lesions up the stem in a given image set? | Complex-Inferential | `ImageSet`, `hasSeverityScore`, `LesionProgression` | Evaluates the graph's utility in automating or supporting disease severity scoring. |
| **CQ-IMG-05** | Are there healthy-plant baseline images available that match the exact developmental growth stage of a provided diseased plant image? | Simple | `Image`, `hasHealthStatus`, `GrowthStage`, `matchesStage` | Ensures the KG can provide healthy baselines for comparative diagnostics. |

### C. Sensor/Environmental-Grounded CQs
*Answerable purely from IoT environmental time-series data.*

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-ENV-01** | Which sensor nodes recorded relative humidity exceeding 92% for more than 48 consecutive hours? | Simple | `SensorNode`, `recordsObservation`, `RelativeHumidity`, `Duration` | Retrieves basic microclimatic threshold events critical for fungal outbreaks. |
| **CQ-ENV-02** | What was the average daily temperature and cumulative rainfall in Region X during the two weeks preceding date Y? | Relational | `Region`, `hasSensor`, `Temperature`, `Rainfall`, `TimeWindow` | Extracts aggregated agroclimatic context for a specific geospatial window. |
| **CQ-ENV-03** | Which environmental time-series patterns structurally match the known optimal incubation conditions for *Magnaporthe oryzae*? | Relational | `TimeSeriesData`, `matchesPattern`, `IncubationCondition` | Enables pattern matching against epidemiological risk models. |
| **CQ-ENV-04** | Are there anomalous soil moisture and pH readings that correlate temporally with known stress-induced susceptibility periods? | Complex-Inferential | `SoilMoisture`, `SoilPH`, `hasAnomaly`, `TemporalCorrelation` | Detects underlying abiotic stressors that predispose plants to infection. |

### D. Genomic/Tabular-Grounded CQs
*Answerable purely from variety, genotype, and agronomic tabular records.*

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-GEN-01** | Which rice varieties or cultivars possess the *Xa21* resistance gene? | Simple | `RiceVariety`, `hasResistanceGene`, `Gene` | Fundamental lookup for breeding and deployment of resistant lines. |
| **CQ-GEN-02** | What is the expected baseline yield (tons/ha) for variety IR64 under standard lowland irrigated conditions? | Simple | `RiceVariety`, `hasBaselineYield`, `AgroecologicalZone` | Provides baseline agronomic performance metrics from tabular data. |
| **CQ-GEN-03** | Which cultivars share a genetic lineage indicating broad susceptibility to *Nilaparvata lugens* (BPH) biotype 3? | Relational | `Cultivar`, `hasLineage`, `SusceptibilityProfile`, `Biotype` | Traces shared vulnerabilities through crop pedigree data. |
| **CQ-GEN-04** | How do the maturity durations (days to harvest) of varieties carrying the *Pi9* blast resistance gene compare? | Relational | `RiceVariety`, `hasMaturityDuration`, `hasResistanceGene` | Allows agronomists to select resistant varieties that fit specific seasonal windows. |

### E. Cross-Modal / Fusion CQs
*Requires combining two or more modalities to answer. (Primary focus of the MMKG).*

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-MM-01** | Given a leaf image (Image) showing water-soaked stripes, which pathogens match this visual symptom according to expert diagnostic texts (Text)? | Relational | `Image`, `depictsSymptom`, `matchesTextDescription`, `Pathogen` | Bridges raw visual phenotypes to established textual diagnostic ontologies. |
| **CQ-MM-02** | Which text-reported outbreaks of BPH (Text) occurred in zones where local sensor networks recorded temperatures above 28°C and low rainfall (Sensor)? | Relational | `OutbreakReport`, `locatedIn`, `SensorObservation`, `Temperature` | Correlates documented epidemiological events with raw environmental drivers. |
| **CQ-MM-03** | For the variety 'Ciherang' (Genomic), what historical text bulletins (Text) report vulnerability breakdown to emerging strains of BLB? | Relational | `RiceVariety`, `mentionedIn`, `VulnerabilityReport`, `PathogenStrain` | Tracks the real-world durability of genetic resistance via textual evidence. |
| **CQ-MM-04** | Given an image showing early-stage blast lesions (Image), what were the recorded temperature and humidity readings from the nearest sensor in the preceding 7 days (Sensor)? | Relational | `Image`, `hasLocation`, `nearSensor`, `SensorObservation`, `TimeWindow` | Links phenotypic expression directly to preceding microclimatic conditions. |
| **CQ-MM-05** | Which leaf images (Image) show severe disease symptoms on plants genetically verified as carrying the *Xa4* resistance gene (Genomic)? | Relational | `Image`, `depictsSeverity`, `ofPlant`, `hasGenotype` | Identifies visual evidence of potential gene breakdown or misdiagnosis. |
| **CQ-MM-06** | Which rice genotypes (Genomic) exhibit the least yield penalty in tabular data when grown in environments with consistently high temperature and low soil moisture (Sensor)? | Complex-Inferential | `Genotype`, `hasYieldPenalty`, `correlatedWith`, `SensorProfile` | Discovers resilient genotypes by fusing phenotypic yield data with abiotic sensor histories. |
| **CQ-MM-07** | Based on expert rules (Text), if relative humidity > 92% (Sensor) and field images show dense canopy closure (Image), what is the calculated probability of sheath blight onset? | Complex-Inferential | `TextRule`, `evaluatedAgainst`, `SensorData`, `ImageFeature`, `DiseaseRisk` | Fuses semantic rules, visual canopy state, and microclimate to predict risk. |
| **CQ-MM-08** | If a plant with the *Pi-ta* gene (Genomic) shows atypical blast lesions (Image) under highly favorable blast conditions (Sensor), is it flagged as a potential resistance breakdown? | Complex-Inferential | `Genotype`, `expressesPhenotype`, `Image`, `underCondition`, `Flag` | High-level diagnostic query combining genetic expectation, visual reality, and environment. |
| **CQ-MM-09** | Which literature reports (Text) validate the hypothesis that *Xa21* (Genomic) effectiveness decreases when daytime temperatures exceed 35°C (Sensor)? | Complex-Inferential | `Document`, `validatesHypothesis`, `GeneEfficacy`, `SensorThreshold` | Validates complex Gene × Environment interactions against published literature. |
| **CQ-MM-10** | Can textual descriptions of "moderate resistance" to tungro (Text/Genomic) be correlated with a specific range of visual stunting severity measured in field images (Image)? | Complex-Inferential | `TextDescriptor`, `mapsTo`, `ResistanceClass`, `correlatesWith`, `ImageSeverity` | Quantifies subjective textual resistance ratings using objective visual metrics. |
| **CQ-MM-11** | Which combinations of environmental conditions (Sensor) recorded in the last 14 days best predict a visual outbreak of BPH (Image), matching historically confirmed diagnoses (Text)? | Complex-Inferential | `SensorPattern`, `predicts`, `VisualOutbreak`, `confirmedBy`, `TextDiagnosis` | Supports training predictive machine learning models across three data streams. |
| **CQ-MM-12** | Given a field image showing a specific lesion type (Image) and local temperature/humidity readings (Sensor), which disease is most likely based on text rules (Text), and which varieties in the KG carry resistance genes against it (Genomic)? | Complex-Inferential | `ImageFeature`, `SensorData`, `TextRule`, `diagnosesDisease`, `treatableBy`, `Variety` | The ultimate end-to-end precision agriculture query traversing all four modalities. |

---

## 3. Modality-Pair Coverage Traceability

The following table summarizes the coverage of multi-modal intersections across the CQs to ensure no functional gaps exist in the ontology design.

| Modality Combination | Covered by CQ IDs |
| :--- | :--- |
| **Text × Image** | CQ-MM-01 |
| **Text × Sensor** | CQ-MM-02 |
| **Text × Genomic/Tabular** | CQ-MM-03 |
| **Image × Sensor** | CQ-MM-04 |
| **Image × Genomic/Tabular** | CQ-MM-05 |
| **Sensor × Genomic/Tabular** | CQ-MM-06 |
| **Text × Image × Sensor** | CQ-MM-07, CQ-MM-11 |
| **Image × Sensor × Genomic** | CQ-MM-08 |
| **Text × Sensor × Genomic** | CQ-MM-09 |
| **Text × Image × Genomic** | CQ-MM-10 |
| **All 4 Modalities (Text × Image × Sensor × Genomic)** | CQ-MM-12 |

---

## 4. Scope Boundary Note

This Knowledge Graph focuses strictly on the biological, agronomic, phenotypic, and environmental dimensions of major rice pests and diseases (e.g., Rice Blast, Bacterial Leaf Blight, Tungro, BPH) within tropical/subtropical agroecosystems. It heavily integrates multimodal indicators—phenotypic images, micrometeorological sensor data, genomic resistance profiling, and text-based literature—to support diagnostic and predictive queries. **OUT OF SCOPE** are socio-economic factors (e.g., market prices for rice, farmer demographics, supply chain logistics, pesticide pricing) and non-pest agricultural stresses (e.g., heavy metal toxicity, weed management). *Note for KG Engineers:* Some complex inferential CQs requiring high-frequency multimodal correlation (e.g., CQ-MM-08, CQ-MM-12) may be partially infeasible if high-resolution, geolocated alignments between genomic test plots and continuous sensor arrays are unavailable in current legacy datasets; these CQs serve as functional targets for future integrated data collection.
