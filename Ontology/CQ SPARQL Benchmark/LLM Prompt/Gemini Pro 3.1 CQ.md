# Ontology Requirements Specification: Competency Questions for a Rice Pest & Disease Multimodal Knowledge Graph

## 1. Purpose and Scope Statement
The proposed multimodal knowledge graph (KG) aims to support early diagnosis, epidemiological tracking, and decision-making for rice pest and disease management. By semantically integrating diverse data modalities—scientific literature (Text), field diagnostics (Image), IoT agroclimatic readings (Sensor), and rice cultivar genetics (Genomic/Tabular)—the KG provides a unified framework for researchers, agricultural extension officers, and precision-agriculture developers, with a primary focus on tropical lowland rice ecosystems (e.g., Southeast Asia).

---

## 2. Competency Questions (CQs)

*Assumption Note: As specific datasets were not supplied, these CQs assume the integration of standard major rice diseases (e.g., Rice Blast, Bacterial Leaf Blight, Tungro) and common resistance genes (e.g., Xa21, Pi9) commonly found in ontologies like the Crop Ontology (CO) and Plant Phenotype Ontology (PPO).*

### A. Text-Grounded CQs
*Answerable from literature, report facts, and textual symptom descriptions alone.*

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-TXT-01** | What is the causal pathogen of Rice Blast? | Simple | `Disease`, `causedBy`, `Pathogen` | Verifies basic taxonomic and pathological lookup capabilities. |
| **CQ-TXT-02** | Which rice diseases are documented as being transmitted by the vector *Nilaparvata lugens* (Brown Planthopper)? | Relational | `Disease`, `transmittedBy`, `Vector` | Ensures the KG can traverse vector-pathogen-disease relationships described in literature. |
| **CQ-TXT-03** | What are the recommended chemical or biological control agents for managing Sheath Blight (*Rhizoctonia solani*)? | Relational | `Disease`, `hasTreatment`, `ControlAgent` | Tests retrieval of actionable agronomic management data from extension reports. |
| **CQ-TXT-04** | Which diseases share overlapping textual symptom descriptions regarding "leaf chlorosis" or "yellowing"? | Complex | `Disease`, `hasSymptomDescription`, `Symptom` | Validates the KG's ability to cluster or compare entities based on shared phenotypic text traits. |
| **CQ-TXT-05** | Based on surveillance bulletins, what is the typical latency period for Bacterial Leaf Blight before symptoms become visible? | Simple | `Disease`, `hasLatencyPeriod`, `TemporalDuration` | Ensures extraction and structuring of temporal pathological parameters from unstructured text. |

### B. Image-Grounded CQs
*Answerable from visual symptom/damage evidence alone.*

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-IMG-01** | Which specific disease is characterized by images showing spindle-shaped or diamond-shaped lesions with grey centers on leaves? | Simple | `Image`, `depictsSymptom`, `LesionShape`, `Disease` | Connects visual morphological features (extracted from images) to specific disease classifications. |
| **CQ-IMG-02** | What visual features in close-up images distinguish Stem Borer "whitehead" damage from healthy rice panicles? | Relational | `Image`, `showsPlantPart`, `Panicle`, `hasVisualFeature` | Ensures structural bounding/segmentation of plant parts is mapped to pest damage. |
| **CQ-IMG-03** | Are there authenticated field images depicting early-stage symptoms of the Rice Tungro Virus on whole plants? | Simple | `Image`, `depictsDiseaseStage`, `EarlyStage`, `Disease` | Verifies the KG tracks disease progression stages explicitly tied to visual evidence. |
| **CQ-IMG-04** | Which pests are associated with whole-field images showing "hopperburn" (large circular patches of dried/browning plants)? | Relational | `Image`, `depictsFieldScaleDamage`, `Pest` | Tests the hierarchy of image scales (leaf level vs. field scale) and associated pest inferences. |
| **CQ-IMG-05** | Given a time-series of close-up leaf images from a single plot, rank the progression severity of Bacterial Leaf Blight lesions over time. | Complex | `Image`, `capturedAt`, `Time`, `hasSeverityScore` | Demands temporal sorting and severity scaling of visual data entities. |

### C. Sensor/Environmental-Grounded CQs
*Answerable from environmental time-series alone.*

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-SEN-01** | What is the optimal temperature and relative humidity range for the proliferation of *Magnaporthe oryzae*? | Simple | `Pathogen`, `thrivesIn`, `TemperatureRange`, `HumidityRange` | Links environmental thresholds to pathogen biology. |
| **CQ-SEN-02** | Which specific days in the last month recorded relative humidity above 90% for more than 4 consecutive hours? | Relational | `SensorReading`, `hasValue`, `recordedOn`, `TimeInterval` | Verifies the KG can query granular, aggregated time-series IoT data. |
| **CQ-SEN-03** | What are the historical rainfall patterns (e.g., cumulative weekly precipitation) associated with recorded Sheath Blight outbreaks? | Complex | `DiseaseOutbreak`, `correlatesWith`, `PrecipitationMetric` | Requires aggregating historical sensor data around specific event nodes. |
| **CQ-SEN-04** | Which monitored agroclimatic plots maintain an average soil moisture level conducive to Brown Planthopper reproduction? | Relational | `Plot`, `hasSensor`, `SoilMoisture`, `conduciveTo` | Bridges spatial entities (plots/fields) with environmental data and pest life cycles. |

### D. Genomic/Tabular-Grounded CQs
*Answerable from variety/genotype/resistance data alone.*

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-GEN-01** | Which rice varieties (cultivars) documented in the KG possess the *Xa21* resistance gene? | Simple | `Cultivar`, `hasGene`, `ResistanceGene` | Tests basic retrieval of genetic metadata for crop varieties. |
| **CQ-GEN-02** | What is the average historical yield penalty (in tons/hectare) for variety IR64 when susceptible to Brown Planthopper infestation? | Relational | `Cultivar`, `hasYieldPenalty`, `Pest` | Links tabular agronomic performance data to specific pest susceptibilities. |
| **CQ-GEN-03** | Which commercial cultivars have documented genetic resistance to *both* Rice Blast and Bacterial Leaf Blight? | Relational | `Cultivar`, `resistantTo`, `Disease` | Ensures the ability to perform intersection queries across multiple resistance profiles. |
| **CQ-GEN-04** | How do the maturity rates (days to harvest) of drought-tolerant varieties compare to those of standard tropical lowland varieties? | Complex | `Cultivar`, `hasTrait`, `MaturityRate`, `DroughtTolerance` | Requires comparative analysis of tabular phenotypic traits across cultivar categories. |

### E. Cross-Modal / Fusion CQs
*Requires combining two or more modalities in a single answer. (Primary KG Justification)*

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-MM-01** | **[Img × Txt]** Given a leaf image showing spindle-shaped lesions, what are the corresponding chemical treatment protocols documented in extension literature? | Relational | `Image`, `depictsSymptom`, `Disease`, `hasTreatmentProtocol` | Bridges computer vision outputs (symptom classification) directly to actionable text retrieval. |
| **CQ-MM-02** | **[Img × Sen]** Do field images showing advanced "hopperburn" correlate spatially and temporally with periods of recorded drought stress (low soil moisture) in the preceding 14 days? | Complex | `Image`, `showsDamage`, `SensorReading`, `SoilMoisture`, `Location` | Tests spatio-temporal reasoning across visual phenotypes and IoT environmental stress indicators. |
| **CQ-MM-03** | **[Sen × Gen]** Which rice plots planted with varieties carrying the *Pi9* blast resistance gene experienced blast outbreaks when average relative humidity exceeded 85%? | Complex | `Cultivar`, `hasGene`, `SensorReading`, `DiseaseOutbreak` | Investigates the breakdown of genetic resistance under specific environmental pressures. |
| **CQ-MM-04** | **[Txt × Gen]** What does recent scientific literature report regarding the field efficacy of the *Xa4* gene against newly emerged *Xanthomonas oryzae* strains? | Relational | `Literature`, `reportsEfficacy`, `Gene`, `PathogenStrain` | Connects structured genetic entities with unstructured NLP extractions from research papers. |
| **CQ-MM-05** | **[Img × Txt × Sen]** If IoT sensors indicate 3 days of heavy rain and user-uploaded leaf images show water-soaked stripes, what causal pathogen is most likely according to agronomic bulletins? | Complex | `SensorReading`, `Image`, `Literature`, `Pathogen` | Simulates a real-world multi-evidence diagnostic query mimicking an expert's reasoning. |
| **CQ-MM-06** | **[Sen × Gen × Txt]** Are there textual reports detailing how temperature spikes above 35°C (Sensor) affect the resistance expression of the *Bph14* gene (Genomic)? | Complex | `SensorReading`, `Temperature`, `Gene`, `Literature` | Identifies GxE (Genotype x Environment) interactions documented in text. |
| **CQ-MM-07** | **[Img × Gen]** Given whole-plant images showing severe stunting and yellowing, which varieties in the affected plot lack genetic resistance to the Tungro virus? | Relational | `Image`, `depictsSymptom`, `Plot`, `Cultivar`, `resistantTo` | Combines visual symptom severity with underlying genetic susceptibility profiles. |
| **CQ-MM-08** | **[Img × Sen × Gen]** For fields recording continuous high humidity, do images of cultivar 'Swarna-Sub1' show Sheath Blight symptoms despite its general hardiness? | Complex | `SensorReading`, `Cultivar`, `Image`, `depictsSymptom` | Validates phenotype manifestation (Image) against genotype (Genomic) under specific conditions (Sensor). |
| **CQ-MM-09** | **[Txt × Img × Gen]** Based on text symptom descriptions and field imagery, how does the visual severity of blast lesions differ between varieties with and without the *Pi54* gene? | Complex | `TextDescription`, `Image`, `Cultivar`, `Gene` | Requires comparative multimodal phenotypic analysis based on genotypic presence. |
| **CQ-MM-10** | **[All 4 Modalities]** Which fields planted with varieties lacking the *Xa21* gene (Genomic) showed water-soaked lesions (Image) following a typhoon event (Sensor), and what are the recommended quarantine steps (Text)? | Complex | `Cultivar`, `Gene`, `Image`, `SensorReading`, `Literature` | The ultimate stress-test of the KG: integrating genetics, vision, IoT weather events, and textual protocols. |
| **CQ-MM-11** | **[Img × Sen × Txt]** Can historical models (Text) explain the prevalence of Stem Borer "whitehead" symptoms (Image) during recent periods of low rainfall (Sensor)? | Complex | `Literature`, `Image`, `SensorReading`, `EnvironmentalCondition` | Connects historical text-based epidemiological models with real-time multimodal evidence. |
| **CQ-MM-12** | **[Txt × Sen]** Which extension bulletins explicitly describe pest management protocols for growing seasons affected by El Niño-driven low rainfall patterns? | Relational | `Literature`, `hasProtocol`, `WeatherPattern`, `SensorTrend` | Links unstructured advisory documents to macro-level environmental sensor classifications. |

---

## 3. Traceability Summary: Modality-Pair Coverage
*This table maps modality interactions to their corresponding Cross-Modal CQs to ensure comprehensive integration testing.*

| Modality Combination | Covering CQ IDs | Coverage Status |
| :--- | :--- | :--- |
| **Text × Image** | CQ-MM-01, CQ-MM-09 | Adequately covered |
| **Text × Sensor** | CQ-MM-12, CQ-MM-05, CQ-MM-11 | Adequately covered |
| **Text × Genomic** | CQ-MM-04, CQ-MM-06 | Adequately covered |
| **Image × Sensor** | CQ-MM-02, CQ-MM-05, CQ-MM-08 | Adequately covered |
| **Image × Genomic** | CQ-MM-07, CQ-MM-09 | Adequately covered |
| **Sensor × Genomic** | CQ-MM-03, CQ-MM-06, CQ-MM-08 | Adequately covered |
| **Three-Way Fusion** | CQ-MM-05, CQ-MM-06, CQ-MM-08, CQ-MM-09, CQ-MM-11 | Strongly covered |
| **Four-Way Fusion** | CQ-MM-10 | Covered |

---

## 4. Scope Boundary Note

This Knowledge Graph is **IN SCOPE** for explicitly representing linkages between rice pathogens, visual morphological symptoms (phenotypes), environmental drivers (IoT weather/soil metrics), host genetic resistance (specific genes/cultivars), and documented agronomic management practices. It is designed to act as a diagnostic and epidemiological reasoning engine. 

However, it is **OUT OF SCOPE** for handling raw genomic sequence data (e.g., base-pair level DNA alignments) or real-time agricultural market pricing and supply chain logistics. Furthermore, the KG is restricted to *Oryza sativa* and its specific pests/diseases; weeds, other crop types, and generalized farm machinery ontologies are excluded. *Note: CQs requiring highly granular historical weather data tied to specific legacy image datasets (e.g., CQ-MM-02, CQ-MM-11) may be temporarily infeasible depending on the availability of geolocated, timestamped image metadata, and should be flagged for data-availability review during implementation.*
