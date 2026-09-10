# Ontology Requirements Specification: Competency Questions for Rice Pest & Disease Multimodal Knowledge Graph

## 1. Purpose and Scope Statement
The purpose of this Multimodal Knowledge Graph (KG) is to support early diagnosis, predictive modeling, and decision-making for rice pest and disease management in agroecosystems. By semantically integrating text (literature/reports), imagery (field symptoms), sensor data (environmental/IoT time-series), and genomic/tabular records (cultivar resistance), the KG serves plant pathologists, agricultural extension officers, and precision-agriculture system developers. The entities and relations are designed to align with international standards such as the Crop Ontology (CO), Plant Trait Ontology (TO), AGROVOC, and standard Infectious Disease Ontology patterns.

*Assumptions made:* Since specific inputs were omitted, common major rice pests and diseases (e.g., Rice Blast / *Magnaporthe oryzae*, Bacterial Leaf Blight / *Xanthomonas oryzae*, Brown Planthopper / *Nilaparvata lugens*, Tungro Virus) were used. The target CQ count is approximately 32.

---

## 2. Competency Questions (CQs)

### 2.1 Text-Grounded CQs (15-20%)
*Answerable from literature, reports, and expert symptom descriptions alone.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal pathogen of Rice Blast disease? | Simple | `Disease`, `causedBy`, `Pathogen` | Establishes baseline etiology for major diseases. |
| CQ-TXT-02 | What are the documented field symptoms of Bacterial Leaf Blight in the vegetative stage? | Relational | `Disease`, `hasSymptom`, `Symptom`, `occursDuring`, `GrowthStage` | Necessary for matching diagnostic descriptions to diseases. |
| CQ-TXT-03 | Which chemical or cultural management practices are recommended for controlling the Brown Planthopper? | Relational | `Pest`, `hasTreatment`, `ManagementPractice` | Provides actionable agronomic advice to extension workers. |
| CQ-TXT-04 | What are the known alternate host plants for the Rice Tungro Spherical Virus (RTSV)? | Relational | `Virus`, `hasAlternateHost`, `PlantSpecies` | Critical for ecological management and crop rotation planning. |
| CQ-TXT-05 | How do the literature descriptions of Sheath Blight lesions differ from Stem Borer damage? | Complex | `Disease`, `Pest`, `hasSymptom`, `DamagePattern`, `hasDifference` | Enables differential diagnosis based on textual evidence. |
| CQ-TXT-06 | Which diagnostic surveillance bulletins report an outbreak of Rice Blast in the last 6 months? | Relational | `Report`, `mentionsDisease`, `Disease`, `hasPublicationDate` | Tracks historical and textual epidemiological trends. |

### 2.2 Image-Grounded CQs (15-20%)
*Answerable from visual symptom/damage evidence alone.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Does this leaf image exhibit spindle-shaped lesions with gray centers? | Simple | `Image`, `showsFeature`, `VisualSymptom` | Translates visual pathology features into queryable states. |
| CQ-IMG-02 | What anatomical plant part (e.g., leaf, stem, panicle) is the primary focus of the given image? | Simple | `Image`, `depictsAnatomy`, `PlantPart` (PO) | Ensures spatial localization of symptoms for accurate diagnosis. |
| CQ-IMG-03 | Can the image be classified as showing a "healthy" plant baseline or a "diseased" state? | Relational | `Image`, `hasHealthStatus`, `PlantStatus` | Supports fundamental binary classification for CV systems. |
| CQ-IMG-04 | What is the estimated percentage of lesion area relative to total leaf area in the provided image? | Complex | `Image`, `hasMeasurement`, `LesionAreaRatio` | Enables automated disease severity scoring. |
| CQ-IMG-05 | Which images in the dataset show evidence of panicle blanking or discoloration? | Relational | `Image`, `showsSymptom`, `PanicleSymptom` | Supports retrieval of specific visual exemplars for training. |
| CQ-IMG-06 | Rank the severity of pest damage across a set of stem images from lowest to highest structural degradation. | Complex | `Image`, `showsSeverityLevel`, `DamageSeverity` | Useful for quantifying pest pressure thresholds visually. |

### 2.3 Sensor / Environmental-Grounded CQs (10-15%)
*Answerable from environmental time-series alone.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What was the average relative humidity and temperature for field plot X over the last 7 days? | Simple | `Sensor`, `measuresProperty`, `Humidity`, `Temperature`, `TimePeriod` | Retrieves basic agroclimatic baseline data. |
| CQ-ENV-02 | Identify periods where continuous leaf wetness exceeded 12 hours while temperature was between 25°C and 28°C. | Relational | `SensorReading`, `hasValue`, `Duration`, `meetsCondition` | Identifies microclimatic windows conducive to fungal sporulation. |
| CQ-ENV-03 | Which sensor deployments recorded soil moisture dropping below the optimal threshold for lowland rice? | Relational | `SensorNode`, `measuresProperty`, `SoilMoisture`, `belowThreshold` | Tracks abiotic stress that may compound disease vulnerability. |
| CQ-ENV-04 | Based on the historical time-series, what is the frequency of high-wind events (>10 m/s) during the monsoon season? | Complex | `EnvironmentalData`, `hasWindSpeed`, `TimeSeriesAggregation` | Assesses risk factors for the spread of bacterial blight. |

### 2.4 Genomic / Tabular-Grounded CQs (10-15%)
*Answerable from variety/genotype/resistance data alone.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which known resistance genes (R-genes) are present in the rice variety IR64? | Simple | `Cultivar`, `hasResistanceGene`, `Gene` | Fundamental lookup for breeding and variety selection. |
| CQ-GEN-02 | Which cultivated varieties are listed as highly susceptible to the Xa21-virulent strain of Xanthomonas oryzae? | Relational | `Cultivar`, `hasSusceptibilityTo`, `PathogenStrain` | Crucial for avoiding high-risk plantings in endemic areas. |
| CQ-GEN-03 | What is the recorded yield penalty (in tons/hectare) associated with Nilaparvata lugens infestation in susceptible varieties? | Relational | `Cultivar`, `hasYieldRecord`, `YieldPenalty`, `Pest` | Quantifies the economic impact of pest susceptibility. |
| CQ-GEN-04 | Identify diverse cultivars that possess stacked resistance to both Rice Blast (e.g., Pi9) and Bacterial Leaf Blight (e.g., Xa21). | Complex | `Cultivar`, `hasResistanceGene`, `Gene`, `providesResistanceTo` | Supports recommendations for resilient agriculture. |
| CQ-GEN-05 | What are the maturity durations (days to harvest) of varieties that carry the tungro resistance trait? | Relational | `Cultivar`, `hasPhenotype`, `MaturityDuration`, `ResistanceTrait` | Helps align disease-resistant varieties with local growing seasons. |

### 2.5 Cross-Modal / Fusion CQs (30-40%)
*Require combining two or more modalities to answer.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 | (Text+Image) Does the literature description of "spindle-shaped lesions" (Text) match the visual features extracted from Image ID X (Image)? | Complex | `ImageSymptom`, `matchesDescription`, `TextSymptom` | Validates computer vision outputs against formal domain definitions. |
| CQ-MM-02 | (Image+Sensor) Given an image showing early blast symptoms (Image), what were the temperature and humidity readings in that exact field over the prior 14 days (Sensor)? | Relational | `Image`, `takenInField`, `SensorNode`, `measuresProperty` | Links visual evidence of disease onset to precipitating weather. |
| CQ-MM-03 | (Sensor+Genomic) Which cultivated varieties showed the lowest yield loss (Genomic/Tabular) during seasons where average humidity exceeded 85% (Sensor)? | Complex | `Cultivar`, `hasYield`, `YieldRecord`, `recordedDuring`, `EnvCondition` | Identifies robust varieties under specific climatic stressors. |
| CQ-MM-04 | (Image+Genomic) Does the severity of sheath blight observed in field images (Image) correlate with the absence of specific quantitative trait loci (QTLs) in the planted varieties (Genomic)? | Complex | `Image`, `showsSeverity`, `Cultivar`, `lacksQTL` | Facilitates genotype-to-phenotype mapping in real-world fields. |
| CQ-MM-05 | (Text+Sensor) Retrieve extension reports on Tungro virus outbreaks (Text) and correlate them with historical temperature anomaly data (Sensor) for the reported regions. | Complex | `Report`, `reportsOutbreak`, `Region`, `hasEnvData` | Enables epidemiological analysis of climate drivers for outbreaks. |
| CQ-MM-06 | (Image+Text+Genomic) Recommend a blast-resistant variety (Genomic) based on symptom images from the field (Image) and management guidelines for the local region (Text). | Complex | `Cultivar`, `hasResistance`, `Image`, `diagnosedAs`, `Report` | Acts as a complete diagnostic-to-intervention decision support query. |
| CQ-MM-07 | (Sensor+Text+Genomic) If current sensors detect conditions optimal for Brown Planthopper (Sensor), which susceptible varieties (Genomic) are flagged in recent surveillance bulletins (Text) as high-risk? | Complex | `EnvCondition`, `optimalFor`, `Pest`, `Cultivar`, `Report` | Enables proactive, multi-modal early warning systems. |
| CQ-MM-08 | (Image+Sensor) Classify the likelihood of a false positive visual diagnosis for bacterial blight (Image) based on historically non-conducive environmental data (Sensor). | Complex | `Diagnosis`, `basedOnImage`, `EnvData`, `supportsDiagnosis` | Acts as a multimodal confidence-scoring mechanism. |
| CQ-MM-09 | (Text+Genomic) Extract novel resistance gene candidates mentioned in recent literature (Text) and map them to existing germplasm records (Genomic). | Relational | `Document`, `mentionsGene`, `Gene`, `presentInGermplasm` | Keeps the genomic knowledge base updated via NLP literature mining. |
| CQ-MM-10 | (Image+Sensor+Genomic+Text) Given leaf images with yellowing (Image), recent temperatures >30°C (Sensor), and planting of susceptible variety TN1 (Genomic), retrieve the top recommended chemical/cultural interventions (Text). | Complex | Multiple entities across all 4 modalities. | Represents the ultimate "holy grail" multimodal precision agriculture query. |
| CQ-MM-11 | (Text+Image) Which images (Image) serve as best-case exemplars for the earliest stage of Rice Blast as described in the IRRI management manuals (Text)? | Relational | `Image`, `exemplifiesStage`, `DiseaseStage`, `describedIn` | Links standard reference materials with field-acquired imagery. |

---

## 3. Modality-Pair Coverage Table

The table below maps cross-modal intersections to the specific CQ IDs that exercise those linkages, ensuring comprehensive multimodal coverage.

| Modality Combination | Associated CQs |
|---|---|
| **Text × Image** | CQ-MM-01, CQ-MM-11 |
| **Image × Sensor** | CQ-MM-02, CQ-MM-08 |
| **Sensor × Genomic** | CQ-MM-03 |
| **Image × Genomic** | CQ-MM-04 |
| **Text × Sensor** | CQ-MM-05 |
| **Text × Genomic** | CQ-MM-09 |
| **Image × Text × Genomic** | CQ-MM-06 |
| **Sensor × Text × Genomic** | CQ-MM-07 |
| **Image × Sensor × Text × Genomic** | CQ-MM-10 |

---

## 4. Scope Boundary Note

**In Scope:** The KG is designed to represent and link diagnostic visual features (lesions, plant damage), meteorological time-series conditions (temperature, humidity, wetness), core taxonomic entities (pathogens, pests, rice varieties), genomic resistance profiles, and textual knowledge (management practices, outbreak reports). It explicitly supports queries that bridge phenotype (images), environment (sensors), genotype (tables), and human knowledge (text).

**Out of Scope:** The KG does *not* cover broader agricultural economics (e.g., market pricing, supply chain logistics), detailed molecular/cellular mechanisms of infection (e.g., protein folding, RNA sequences), or granular farm management operations (e.g., tractor routing, labor scheduling). Furthermore, CQ-MM-04 and CQ-MM-09 rely on highly advanced data availability (e.g., automated extraction of novel QTLs from literature); they may be technically infeasible to implement fully with legacy datasets and are flagged here for early evaluation by the data engineering team.
