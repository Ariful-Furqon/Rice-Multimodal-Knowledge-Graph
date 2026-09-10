# Competency Questions for a Rice Pest & Disease Multimodal Knowledge Graph

*Ontology Requirements Specification — Competency Question Set (v1.0)*

---

## 0. Assumptions Made

All `INPUT FROM USER` fields were left as placeholders, so the following defaults were applied. Each is marked **[ASSUMED]** and should be revised if the project specifics differ.

| Field | Default applied |
|---|---|
| Primary end users | **[ASSUMED]** Plant pathology researchers, agricultural extension officers, and smart-farming/IoT system developers |
| Geographic scope | **[ASSUMED]** Indonesia / Southeast Asian tropical lowland irrigated rice |
| Pests/diseases in scope | **[ASSUMED]** Rice blast (*Magnaporthe oryzae*), bacterial leaf blight/BLB (*Xanthomonas oryzae* pv. *oryzae*, Xoo), sheath blight (*Rhizoctonia solani*), brown spot (*Bipolaris oryzae*), rice tungro disease (RTBV + RTSV, vectored by *Nephotettix virescens*), brown planthopper/BPH (*Nilaparvata lugens*), yellow stem borer (*Scirpophaga incertulas*), rice bug (*Leptocorisa oratorius*) |
| Text sources | **[ASSUMED]** Peer-reviewed literature, IRRI Rice Knowledge Bank / extension fact sheets, provincial pest-surveillance bulletins |
| Image sources | **[ASSUMED]** Public rice-disease image datasets plus project field photographs, annotated with disease/pest label, plant organ, growth stage, severity (IRRI Standard Evaluation System, SES), capture date, and field/plot ID |
| Sensor sources | **[ASSUMED]** IoT field stations recording air temperature, relative humidity (RH), rainfall, leaf wetness, soil moisture, and soil pH at hourly/daily resolution, geo-referenced to fields |
| Genomic/tabular sources | **[ASSUMED]** Cultivar registry (Indonesian released varieties such as the Inpari series, Ciherang, IR64), resistance-gene records (Xa/xa, Pi, Bph, qSB loci), pedigree records, and multi-season yield trial tables |
| Target number of CQs | **[ASSUMED]** 35 (within the default 30–40 range) |
| Existing ontology to align with | **[ASSUMED]** None yet; alignment candidates flagged in Section 5 |
| Pre-drafted CQs to avoid | None supplied |

---

## 1. Restatement of KG Purpose and Scope

The knowledge graph is intended to support early diagnosis and management decision-making for the major pests and diseases of tropical lowland rice, serving plant pathology researchers, extension officers, and precision-agriculture systems. It semantically links four modalities — textual domain knowledge, symptom/damage imagery, field-level environmental sensor streams, and cultivar/genotype/trial tables — so that a single formal query can combine, for example, a visual observation, the recent microclimate of the field where it was taken, and the resistance profile of the variety planted there. The competency questions below define what the KG must represent, how modalities must be aligned, and against what criteria the resulting graph will be evaluated.

---

## 2. Competency Questions

Complexity levels: **S** = Simple/factual · **R** = Relational (2–3 hops) · **C** = Complex/inferential (aggregation, ranking, temporal, or causal reasoning).

### 2a. Text-grounded CQs (CQ-TXT)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal agent of bacterial leaf blight, and to which taxonomic group (bacterium, fungus, virus, insect) does it belong? | S | Disease, hasCausalAgent, Pathogen, hasTaxonomicRank, TaxonGroup | Establishes the core disease–pathogen backbone every diagnostic query depends on. |
| CQ-TXT-02 | Which insect vector transmits the two viruses (RTBV and RTSV) responsible for rice tungro disease, and which of the two is required for vector acquisition? | S | Disease, causedBy, Virus, transmittedBy, InsectVector, requiresHelperVirus | Vector-borne diseases need an explicit vector relation so that pest and disease sub-graphs interconnect. |
| CQ-TXT-03 | Which management practices (cultural, chemical, biological) are recommended for brown planthopper control, and which document supports each recommendation? | R | Pest, hasManagementPractice, ManagementPractice, hasCategory, supportedBy, Document | Extension officers need provenance-tracked recommendations, not just labels. |
| CQ-TXT-04 | At which rice growth stages is yellow stem borer damage reported, and which symptom term (e.g., deadheart, whitehead) is associated with each stage? | R | Pest, damagesAtStage, GrowthStage, producesSymptom, Symptom, hasTerm | Symptom terms are stage-dependent; this drives the Symptom class design and links to image annotation vocabularies. |
| CQ-TXT-05 | Which pests or diseases were reported in surveillance bulletins for a given province in each of the last five wet seasons, ranked by number of reports? | C | SurveillanceReport, reportsOccurrence, Occurrence, ofPest/Disease, atLocation, inSeason, count | Enables regional prioritisation and provides the "confirmed outbreak" ground truth for cross-modal evaluation. |
| CQ-TXT-06 | Where do literature sources disagree on the temperature range favourable for *Magnaporthe oryzae* infection, and what range does each source assert? | C | Pathogen, hasFavourableCondition, ConditionRange, assertedIn, Document, conflictsWith | Threshold conflicts must be represented explicitly so that sensor-based inference can expose its assumptions. |

### 2b. Image-grounded CQs (CQ-IMG)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Which images depict diamond-shaped lesions with grey centres and brown margins on the leaf blade? | S | Image, depicts, VisualSymptom, hasShape, hasColour, onPlantPart | Tests whether visual symptom attributes are modelled as queryable properties rather than opaque labels. |
| CQ-IMG-02 | For a given image, which plant organ (leaf, sheath, stem, panicle, whole plant) and which growth stage are shown? | S | Image, depictsOrgan, PlantPart, atGrowthStage, GrowthStage | Organ and stage are minimal metadata for interpreting any image. |
| CQ-IMG-03 | Which images annotated as sheath blight show lesions on the leaf sheath and were captured at the tillering or booting stage? | R | Image, annotatedWith, Disease, depictsOrgan, atGrowthStage | Verifies that annotation, organ, and stage can be jointly filtered to build stage-specific training or reference sets. |
| CQ-IMG-04 | Which disease pairs have visually confusable leaf symptoms (e.g., BLB vs. bacterial leaf streak; blast vs. brown spot), and what distinguishing visual cues are recorded for each pair? | R | Disease, visuallySimilarTo, Disease, distinguishedBy, DistinguishingFeature | Differential diagnosis is the main failure mode in image-based tools; the KG must encode the cues. |
| CQ-IMG-05 | For images of rice blast, how is the distribution of SES severity scores different between field-level photographs and close-up photographs? | C | Image, hasSeverityScore, SeverityScale, hasCaptureType, count/group by | Reveals annotation bias between capture types before images are used as evidence. |
| CQ-IMG-06 | For a sequence of images of the same plot captured over 14 days, how did the assigned severity score change over time? | C | Image, ofPlot, Plot, hasCaptureDate, hasSeverityScore, temporal ordering | Longitudinal image linkage is required for progression and early-warning use cases. |

### 2c. Sensor/environmental-grounded CQs (CQ-ENV)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What were the daily mean air temperature and relative humidity recorded at station S on date D? | S | SensorStation, madeObservation, Observation, observedProperty, hasResult, phenomenonTime | Basic observation retrieval; aligns with SOSA/SSN. |
| CQ-ENV-02 | Which stations recorded night-time relative humidity above 90% on at least five consecutive nights during the 2025/26 wet season? | R | Station, Observation, RelativeHumidity, threshold, consecutive temporal window, Season | Prolonged high humidity is the canonical driver for blast and sheath blight. |
| CQ-ENV-03 | Which fields received cumulative rainfall exceeding 100 mm in the seven days preceding date D? | R | Field, servedByStation, Station, Rainfall, sum over window | Fields must be linkable to their nearest/assigned station for any field-level inference. |
| CQ-ENV-04 | At which field did the combination of leaf-wetness duration ≥ 10 h, temperature 24–28 °C, and RH ≥ 90% hold for the longest continuous window this season? | C | Field, Observation, LeafWetness, Temperature, RH, ConditionPattern, duration ranking | Multi-variable condition windows are what disease models actually consume. |
| CQ-ENV-05 | How do mean and variance of temperature and RH differ between two fields in the same district over one season? | C | Field, District, Observation, aggregate (mean, variance), comparison | Microclimate heterogeneity explains why neighbouring fields diverge in disease outcome. |

### 2d. Genomic/tabular-grounded CQs (CQ-GEN)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which resistance genes (e.g., *Xa4*, *xa5*, *Xa21*, *Pi9*, *Bph14*) does the variety IR64 carry? | S | Cultivar, carriesGene, ResistanceGene | Core cultivar–gene link. |
| CQ-GEN-02 | Against which pathogen race, pathotype, or insect biotype does *Bph14* confer resistance? | S | ResistanceGene, confersResistanceTo, Pest/Pathogen, Biotype/Race | Resistance is race-specific; the KG must not collapse genes to disease-level labels. |
| CQ-GEN-03 | Which varieties released in Indonesia carry at least two BLB resistance genes and mature in fewer than 115 days? | R | Cultivar, releasedIn, Country, carriesGene, ResistanceGene, targetsDisease, hasMaturityDuration | Typical variety-recommendation query combining genotype and agronomic traits. |
| CQ-GEN-04 | Which varieties share a parent with Ciherang in the pedigree records yet differ from it in blast resistance profile? | R | Cultivar, hasParent, Cultivar, hasResistanceProfile, comparison | Pedigree traversal supports breeding-oriented users and explains resistance inheritance. |
| CQ-GEN-05 | Across multi-season trials, what is the mean yield of varieties scored resistant vs. susceptible to sheath blight in trials where a sheath blight score was recorded? | C | Trial, evaluatesCultivar, Cultivar, hasDiseaseScore, hasYield, group by resistance class, mean | Quantifies the economic value of resistance from tabular data alone. |

### 2e. Cross-modal / fusion CQs (CQ-MM)

| ID | Question | Complexity | Modalities | Key Entities & Relations | Rationale |
|---|---|---|---|---|---|
| CQ-MM-01 | Which images depict the symptom described in the literature as *kresek* (the seedling-wilt phase of BLB)? | R | Text × Image | Symptom (text-defined), hasSynonym, describedIn, Document, Image, depicts, VisualSymptom | Tests that textual symptom terminology and image annotations resolve to the same Symptom individuals. |
| CQ-MM-02 | For images annotated as blast at field F on date D, what were the mean temperature and RH at the field's assigned station during the preceding seven days? | R | Image × Sensor | Image, ofField, Field, servedByStation, Observation, window aggregate | The minimal image–environment join that every outbreak-context query builds on. |
| CQ-MM-03 | Which variety is depicted in images showing hopperburn, and does that variety carry any *Bph* resistance gene? | R | Image × Genomic | Image, depicts, DamageSymptom, ofPlot, plantedWith, Cultivar, carriesGene | Links observed damage to the genotype of the plant damaged. |
| CQ-MM-04 | Which fields are currently within the literature-reported favourable range for sheath blight (temperature 28–32 °C, RH > 95%) according to their latest sensor readings? | R | Text × Sensor | Disease, hasFavourableCondition, ConditionRange, assertedIn, Document, Field, Observation, range match | Turns textual thresholds into live field-level risk flags. |
| CQ-MM-05 | Which resistance genes reported in the literature as effective against Xoo races prevalent in Southeast Asia are present in the varieties recorded in the cultivar table? | R | Text × Genomic | Document, reportsEfficacy, ResistanceGene, effectiveAgainst, Race, prevalentIn, Region, Cultivar, carriesGene | Bridges published race–gene knowledge with the local variety inventory. |
| CQ-MM-06 | Which fields planted with varieties lacking any *Bph* gene experienced temperature and humidity favourable for brown planthopper population build-up during the last 30 days? | R | Sensor × Genomic | Field, plantedWith, Cultivar, NOT carriesGene, Observation, ConditionPattern | Identifies genetically unprotected fields under conducive conditions — a direct advisory output. |
| CQ-MM-07 | Given a leaf image showing elongated water-soaked lesions along the leaf margins, a field reading of 30 °C and 85% RH, and the variety planted, which disease is most likely and does the variety carry resistance against it? | C | Image × Sensor × Genomic | VisualSymptom, indicativeOf, Disease, hasFavourableCondition, Observation, Cultivar, carriesGene, confersResistanceTo, ranking | The archetypal multimodal diagnostic query; its answer cannot be obtained from any single modality. |
| CQ-MM-08 | For blast outbreaks confirmed both by image annotations and by surveillance bulletins for the same district and month, which environmental windows preceded them, and how consistent are these windows with literature thresholds? | C | Text × Image × Sensor | SurveillanceReport, Image, Occurrence, atLocation, inMonth, Observation, window, ConditionRange, consistency measure | Validates literature thresholds against locally observed outbreaks — a core research use case. |
| CQ-MM-09 | Which visually confirmed disease cases (images with severity ≥ 5) have no corresponding entry in surveillance bulletins for the same district and month? | C | Text × Image | Image, hasSeverityScore, ofField, inDistrict, SurveillanceReport, NOT EXISTS reportsOccurrence | Detects under-reporting; demonstrates that image evidence adds information beyond text. |
| CQ-MM-10 | Which varieties described in the literature as blast-resistant nevertheless appear in field images annotated with blast at severity ≥ 5, suggesting resistance breakdown or a new race? | C | Text × Image × Genomic | Document, describesResistance, Cultivar, carriesGene, Image, annotatedWith, hasSeverityScore, contradiction | Surfaces resistance-breakdown signals early, a key concern for breeders and pathologists. |
| CQ-MM-11 | Rank the monitored fields by tungro outbreak risk for the next 14 days, considering green leafhopper images or trap counts, current sensor conditions, the resistance status of the planted variety, and literature-based vector-activity thresholds. | C | Text × Image × Sensor × Genomic | Field, VectorObservation (Image/TrapCount), Observation, ConditionRange, Cultivar, carriesGene, RiskScore, ranking | Four-way fusion query representing the full decision-support ambition of the KG. |
| CQ-MM-12 | In trial records, how does sheath blight yield loss differ between varieties with and without *qSB* QTL across seasons classified as high- vs. low-humidity from sensor data? | C | Sensor × Genomic/Tabular | Trial, inSeason, Season, classifiedBy, Observation aggregate, Cultivar, carriesLocus, hasYieldLoss, group comparison | Couples genotype-by-environment analysis with observed microclimate rather than assumed season labels. |
| CQ-MM-13 | Over a 14-day image sequence at one field, how does image-derived severity progression correlate with cumulative leaf-wetness hours at that field? | C | Image × Sensor | Image sequence, hasSeverityScore, hasCaptureDate, Field, Observation, LeafWetness, cumulative sum, correlation | Provides the empirical basis for progression models and early-warning calibration. |

**Total: 35 CQs** — 6 text (17%), 6 image (17%), 5 sensor (14%), 5 genomic/tabular (14%), 13 cross-modal (37%).

---

## 3. Modality-Pair Coverage Table

| Modality combination | CQ IDs | Coverage note |
|---|---|---|
| Text × Image | CQ-MM-01, CQ-MM-09 | Terminology alignment and report/image reconciliation |
| Text × Sensor | CQ-MM-04 | Literature thresholds applied to live readings |
| Text × Genomic | CQ-MM-05 | Published race–gene efficacy joined to cultivar inventory |
| Image × Sensor | CQ-MM-02, CQ-MM-13 | Environmental context of observations; progression vs. wetness |
| Image × Genomic | CQ-MM-03 | Observed damage linked to planted genotype |
| Sensor × Genomic/Tabular | CQ-MM-06, CQ-MM-12 | Genetically unprotected fields under conducive conditions; G×E on trials |
| Text × Image × Sensor | CQ-MM-08 | Threshold validation against confirmed outbreaks |
| Text × Image × Genomic | CQ-MM-10 | Resistance-breakdown detection |
| Image × Sensor × Genomic | CQ-MM-07 | Multimodal differential diagnosis |
| Text × Image × Sensor × Genomic | CQ-MM-11 | Full-fusion outbreak risk ranking |

All six pairwise combinations and four higher-order combinations are exercised. The thinnest pairings are **Text × Sensor**, **Text × Genomic**, and **Image × Genomic** (one CQ each); if the project emphasises variety recommendation, adding a second Image × Genomic CQ is advisable.

---

## 4. Scope Boundary Note

**In scope.** The KG covers the eight named pests and diseases of tropical lowland rice, their causal agents and vectors, stage-specific symptoms and visual attributes, provenance-tracked management recommendations, field-level environmental observations and derived condition windows, cultivar identity, resistance genes/QTL, pedigree, and multi-season trial outcomes, together with the field–plot–station–cultivar linkages that make cross-modal queries possible. **Out of scope** are weed management, nutrient disorders and abiotic stresses (except as differential-diagnosis distractors), post-harvest pests, pesticide chemistry and dosage calculation, economic/market data, remote-sensing imagery (satellite/UAV) at scales beyond the individual field, and the training or execution of image classifiers themselves — the KG stores classifier *outputs* as annotations but does not model the classifiers.

**Feasibility flags.** CQ-IMG-06 and CQ-MM-13 require longitudinal, plot-linked image series that most public datasets do not provide; CQ-ENV-04 requires leaf-wetness sensors, which are not always deployed; CQ-GEN-04 depends on pedigree records that may be incomplete for locally released varieties; CQ-MM-09 and CQ-MM-08 presuppose surveillance bulletins with district-and-month granularity; CQ-MM-11 requires trap counts or vector-detection images and a defined risk-scoring function, so it should be treated as an aspirational evaluation target rather than a first-release requirement; and CQ-MM-12 depends on trials that are co-located with sensor stations. These should be revisited once dataset inventories are confirmed.

---

## 5. Suggested Standard/Ontology Alignments

| KG component | Candidate alignment |
|---|---|
| Pathogens, pests, vectors | NCBI Taxonomy; AGROVOC concepts |
| Diseases and symptoms | Plant Disease Ontology / IDO patterns for infectious disease; Plant Phenotype Ontology (PPO) and Plant Trait Ontology (TO) for symptom phenotypes |
| Growth stages, plant parts | Plant Ontology (PO); Crop Ontology (rice) |
| Sensor observations | SOSA/SSN (Observation, ObservedProperty, FeatureOfInterest); QUDT units |
| Field, plot, station geometry | GeoSPARQL |
| Documents, reports, annotation provenance | PROV-O; Web Annotation Data Model for image annotations |
| Cultivars, genes, QTL | Crop Ontology rice trait dictionary; Gramene / Oryzabase gene identifiers |
| Severity scales | IRRI Standard Evaluation System (SES) modelled as an ordinal scale class |
