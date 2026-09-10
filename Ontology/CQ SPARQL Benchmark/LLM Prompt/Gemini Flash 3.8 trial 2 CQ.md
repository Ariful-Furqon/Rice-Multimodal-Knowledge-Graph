# Competency Question Specification for a Rice Pest & Disease Multimodal Knowledge Graph (Rice-MMKG)

## 1. Specification Overview & System Context

**Purpose and Scope:**  
The Rice Pest and Disease Multimodal Knowledge Graph (Rice-MMKG) is designed to support plant pathologists, digital agriculture systems, and agricultural extension services in early diagnosis, risk forecasting, and precision cultivar deployment. The system semantically unifies four foundational modalities: unstructured domain texts and surveillance reports, visual symptom imagery (leaf, stem, panicle), high-resolution agroclimatic sensor time series (temperature, relative humidity, leaf wetness), and tabular/genomic resistance records.

**Assumed Baseline Context & Alignment:**
- **Agroecological Scope:** Tropical and subtropical lowland irrigated and rainfed rice (*Oryza sativa* L.) systems (e.g., Southeast Asia and South Asia).
- **Core Pathogens & Pests Grounded:**
  - *Fungal / Oomycete:* Rice Blast (*Magnaporthe oryzae* / *Pyricularia oryzae*), Sheath Blight (*Rhizoctonia solani*), Brown Spot (*Bipolaris oryzae*), False Smut (*Ustilaginoidea virens*).
  - *Bacterial:* Bacterial Leaf Blight (*Xanthomonas oryzae* pv. *oryzae* - Xoo), Bacterial Leaf Streak (*Xanthomonas oryzae* pv. *oryzicola*).
  - *Viral:* Rice Tungro Spherical Virus & Rice Tungro Bacilliform Virus (RTSV/RTBV; vector: *Nephotettix virescens*).
  - *Insect Pests:* Brown Planthopper (*Nilaparvata lugens* - BPH), Yellow Stem Borer (*Scirpophaga incertulas*), Rice Gall Midge (*Orseolia oryzae*).
- **Ontology Standards for Semantic Grounding:** Alignment with Crop Ontology (CO_320), AGROVOC, Plant Trait Ontology (TO), Plant Phenotype Ontology (PPO), Environment Ontology (ENVO), and Infectious Disease Ontology (IDO) core patterns.

---

## 2. Itemized Competency Questions by Modality

### 2.1 Category A: Text-Grounded Competency Questions (Scientific Literature & Agronomic Reports)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-TXT-01** | Which pathogen causes bacterial leaf blight in rice, and what are its primary taxonomic classifications? | Simple | `Pathogen`, `Disease`, `hasTaxon`, `causesDisease` | Grounding baseline taxonomic identity and canonical etiology from literature sources. |
| **CQ-TXT-02** | Which registered chemical and biological control agents are recommended in extension literature for controlling *Rhizoctonia solani* at the maximum tillering stage? | Relational | `CropGrowthStage`, `Disease`, `ControlAgent`, `recommendedForStage`, `targetsPathogen` | Enables retrieval of actionable, stage-specific pest management interventions extracted from unstructured text. |
| **CQ-TXT-03** | What are the literature-reported alternate weed hosts and overwintering reservoirs for *Xanthomonas oryzae* pv. *oryzae* and *Nilaparvata lugens*? | Relational | `Pathogen`, `InsectPest`, `HostPlant`, `WeedSpecies`, `actsAsReservoirFor` | Supports agroecological epidemiological modeling and non-crop vegetation management strategies. |
| **CQ-TXT-04** | Which agronomic management practices (e.g., nitrogen over-fertilization, dense planting) are reported to significantly exacerbate rice blast epidemic severity? | Complex-Inferential | `AgronomicPractice`, `FertilizerRegime`, `DiseaseSeverity`, `exacerbatesRisk`, `reportedInPublication` | Encodes causal agronomic interactions required for holistic integrated pest management (IPM). |
| **CQ-TXT-05** | What documented biotypes of Brown Planthopper (*Nilaparvata lugens*) have been reported to overcome specific *Bph* resistance genes across Southeast Asian regions? | Complex-Inferential | `InsectBiotyping`, `ResistanceGene`, `GeographicRegion`, `overcomesResistance`, `surveillanceReport` | Tracks historical biotype shifts and resistance breakdown events extracted from longitudinal surveillance literature. |

---

### 2.2 Category B: Image-Grounded Competency Questions (Visual Symptoms & Phenotypic Evidence)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-IMG-01** | Which visual symptom types (e.g., spindle-shaped lesion with necrotic center vs. water-soaked streak) are manifested on leaf blades affected by rice blast? | Simple | `Image`, `PlantAnatomicalEntity`, `LesionPhenotype`, `depictsSymptom`, `manifestedOn` | Evaluates fine-grained bounding box/segmentation annotation alignment for pathognomonic diagnostic visual traits. |
| **CQ-IMG-02** | Which field images exhibit leaf discoloration patterns indicative of Rice Tungro Disease (yellow-orange leaf discoloration starting from tips) rather than nutritional nitrogen deficiency? | Relational | `Image`, `LeafColorPattern`, `DiseaseSymptom`, `NutritionalDisorder`, `differentiatesFrom` | Verifies the KG's capability to ground differential visual diagnosis between biotic viral infection and abiotic stress. |
| **CQ-IMG-03** | What anatomical plant parts (leaf blade, leaf sheath, collar, panicle neck, spikelet) exhibit visible necrosis in images tagged with *Magnaporthe oryzae* at the reproductive stage? | Relational | `Image`, `PlantStructure`, `GrowthStage`, `PathologicalStructure`, `displaysLesionAt` | Required to distinguish between leaf blast, collar rot, and neck blast visually and structurally. |
| **CQ-IMG-04** | How does the visual severity index (percentage leaf area infected / lesion coalescence) compare across time-series field canopy photographs taken at 5-day intervals? | Complex-Inferential | `ImageSeries`, `TemporalSequence`, `CanopyCoverage`, `SeverityMetric`, `tracksProgression` | Supports computer vision-based temporal disease tracking and lesion expansion dynamics from image sequences. |
| **CQ-IMG-05** | Which insect damage morphology (e.g., deadheart, whitehead, hopperburn) is present in an image, and what spatial distribution pattern does it display across the crop canopy? | Complex-Inferential | `Image`, `DamagePhenotype`, `CanopySpatialPattern`, `indicatesInfestation`, `exhibitsSymptom` | Enables image-based spatial mapping of insect feeding damage morphology across canopy regions. |

---

### 2.3 Category C: Sensor- & Environmental-Grounded Competency Questions (Agroclimatic Time Series)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-ENV-01** | What was the average diurnal canopy temperature and cumulative rainfall recorded by in-field IoT nodes during the heading stage of the current cropping cycle? | Simple | `IoTSensorNode`, `CanopyTemperature`, `Rainfall`, `CropStage`, `hasReadingAt` | Verifies basic aggregation, temporal slicing, and ingestion of ambient physical sensor telemetry. |
| **CQ-ENV-02** | How many consecutive hours did relative humidity exceed 90% while canopy temperature remained between 24°C and 28°C over the past 14 days? | Relational | `MicroclimateSensor`, `RelativeHumidity`, `TemperatureMetric`, `DurationThreshold`, `satisfiesMicroclimaticCondition` | Directly models the established empirical epidemiological microclimatic window for *M. oryzae* conidial sporulation and infection. |
| **CQ-ENV-03** | Which sensor nodes located within a 5 km radius detected continuous leaf wetness duration (LWD) exceeding 10 hours accompanied by persistent wind speeds < 2 m/s? | Relational | `LeafWetnessSensor`, `AnemometerSensor`, `SpatialLocation`, `ThresholdObservation`, `coOccursWithinWindow` | Critical for identifying micro-environmental conditions that favor pathogen spore retention and germination. |
| **CQ-ENV-04** | What is the historical anomaly score of current soil moisture tension and floodwater depth relative to the 5-year seasonal baseline for this plot? | Complex-Inferential | `HydrologicalSensor`, `SoilMoisture`, `HistoricalBaseline`, `computesAnomaly`, `hasDeviation` | Identifies extreme water management regimes (e.g., prolonged deep flooding vs. AWD stress) affecting root health and disease predisposition. |

---

### 2.4 Category D: Genomic & Tabular-Grounded Competency Questions (Cultivars, Genotypes & Resistance Loci)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-GEN-01** | Which specific major resistance genes (e.g., *Pi-ta*, *Piz-t*, *Pib*, *Pi9*) are introgressed into the rice cultivar 'IR64'? | Simple | `RiceCultivar`, `ResistanceLocus`, `GeneSymbol`, `carriesGene` | Standard genotype-to-gene mapping indispensable for varietal pedigree and trait cataloging. |
| **CQ-GEN-02** | Which rice accessions in the germplasm registry harbor functional alleles for both bacterial leaf blight resistance (*Xa21*, *xa13*) and brown planthopper resistance (*Bph14*, *Bph15*)? | Relational | `GermplasmAccession`, `ResistanceGene`, `GenePyramid`, `possessesDualResistance` | Identifies elite breeding lines and parent donors possessing multi-stress resistance gene pyramids. |
| **CQ-GEN-03** | Which cultivars classified as 'resistant' in tabular multi-location national yield trials experienced a disease score shift from scale 1–3 to scale 7–9 within three seasons? | Relational | `CultivarTrialRecord`, `EvaluationScale`, `PhenotypicScore`, `recordedShiftAcrossSeasons` | Evaluates tabular longitudinal performance data to detect prospective breakdown of field resistance. |
| **CQ-GEN-04** | What is the correlation between specific single nucleotide polymorphism (SNP) marker profiles at the *Xa4* locus and broad-spectrum resistance against local *Xanthomonas oryzae* races? | Complex-Inferential | `GenotypicMarker`, `PathogenRace`, `HaplotypeAllele`, `confersBroadSpectrumResistanceTo` | Links marker-assisted genomic data with pathotype differential virulence reaction tables. |

---

### 2.5 Category E: Cross-Modal / Multimodal Fusion Competency Questions

| ID | Question | Complexity | Modality Synthesis | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CQ-MM-01** | Given a field photograph showing elliptical leaf lesions and continuous sensor logs of relative humidity >90% and temperature 25–28°C for 3 days, what is the most probable disease, and does literature document high epidemic risk under these conditions? | Complex-Inferential | **Image × Sensor × Text** | `Image`, `SensorReading`, `TextualGuideline`, `identifiesDiagnosis`, `corroboratesRiskProfile` | Direct multimodal diagnostic triage: visual symptom + ambient microclimatic trigger confirmed by epidemiological literature. |
| **CQ-MM-02** | Given an image showing diamond-shaped lesions with grey centers on cultivar 'Ciherang' in a plot recording high leaf wetness, which avirulence genes (*Avr*) in *M. oryzae* correspond to the resistance genes (*Pi*) missing in this cultivar? | Complex-Inferential | **Image × Sensor × Genomic × Text** | `Image`, `MicroclimateSensor`, `RiceCultivar`, `ResistanceGene`, `AvrGene`, `lacksResistanceTo` | End-to-end 4-way fusion: visual lesion + microclimate + host genomics + gene-for-gene literature matching. |
| **CQ-MM-03** | For a farm plot where IoT sensors predict imminent Brown Planthopper (*N. lugens*) resurgence, which cultivars in the regional database carry un-broken *Bph* genes and match the plot's soil pH and seasonal maturity group? | Complex-Inferential | **Sensor × Genomic × Tabular** | `IoTSensorLog`, `PestOutbreakPredictor`, `RiceCultivar`, `BphGeneLocus`, `SoilParameter`, `recommendsVariety` | Precision varietal selection aligning real-time sensor outbreak alerts with genotype resistance catalogs and agronomic matrices. |
| **CQ-MM-04** | Which historical field images in the KG demonstrate severe false smut (*Ustilaginoidea virens*) symptoms during seasons where weather station logs show heavy rainfall during the heading stage? | Relational | **Image × Sensor** | `Image`, `WeatherObservation`, `PhenologicalStage`, `exhibitsSymptomDuringClimateCondition` | Validates retrospective visual-climatic correlation for wet-weather favored fungal reproductive diseases. |
| **CQ-MM-05** | Given an extension diagnosis text describing "crease-like neck lesions and failing grain fill" alongside a canopy photograph showing neck rot, which fungicide active ingredients cited in extension texts are validated for application at heading? | Relational | **Text × Image** | `DiagnosticText`, `Image`, `PlantPart`, `ChemicalActiveIngredient`, `recommendsTreatmentForPhenotype` | Text-guided image confirmation with downstream extraction of stage-appropriate therapeutic interventions. |
| **CQ-MM-06** | Given a drone multispectral image showing localized canopy depression and NDVI drop, combined with soil moisture sensor logs indicating prolonged flooding, does extension literature associate this pattern with stem borer 'deadheart' or sheath rot? | Complex-Inferential | **Image × Sensor × Text** | `RemoteSensingImage`, `VegetationIndex`, `SoilMoistureSensor`, `LiteratureSyndrome`, `disambiguatesCause` | Multimodal spatial anomaly disambiguation between abiotic waterlogging stress and biotic boring insect damage. |
| **CQ-MM-07** | Which rice cultivars documented in trial tables as carrying *Xa21* continue to show healthy visual canopy phenotypes in field photographs despite sensor logs registering optimal bacterial blight infection windows (temperature 28–34°C, driving rain)? | Complex-Inferential | **Genomic/Tabular × Image × Sensor** | `CultivarGenotype`, `ResistanceGene`, `CanopyImage`, `HealthyBaseline`, `SensorWindow`, `validatesFieldEfficacy` | Cross-validates functional genetic resistance in real-world production environments under verified infectious microclimates. |
| **CQ-MM-08** | In plots where drone thermal/RGB imagery identified emerging "hopperburn" circular patches, what did ground pest trap counts (tabular) and humidity sensors record in the preceding 7 days? | Relational | **Image × Sensor × Tabular** | `AerialImage`, `HopperburnPatch`, `TrapCensusTable`, `HumiditySensor`, `precededByVectorSurge` | Reconstructs microclimatic and vector-density trajectories leading up to macroscopic field damage symptoms. |
| **CQ-MM-09** | Given text notes reporting pesticide spray failure against rice blast, does the cultivar's genomic resistance profile (*Pi2*) align with literature reports of newly emerged pathogen virulent lineages in that district? | Relational | **Text × Genomic** | `FieldSprayLog`, `ResistanceGene`, `PathogenLineage`, `reportsEfficacyLoss`, `matchesLineageBreakdown` | Diagnoses whether apparent chemical control failure or management breakdown is driven by host resistance gene obsolescence. |
| **CQ-MM-10** | Based on multi-season image sequences showing lesion spread rates under varying sensor humidity regimes, which mathematical epidemiology model in the literature best predicts time to 50% canopy defoliation? | Complex-Inferential | **Image × Sensor × Text** | `ImageSequence`, `LesionSpreadRate`, `SensorHumidity`, `EpidemiologicalModel`, `predictsDefoliationTrajectory` | Evaluates multimodal temporal analytics for predictive disease forecasting and epidemiological simulation. |
| **CQ-MM-11** | Which genomic loci are associated with tolerant visual phenotypes (minimal leaf tip necrosis in photographs) under sensor-verified extreme high-temperature and drought conditions during anthesis? | Complex-Inferential | **Genomic × Image × Sensor** | `QTL_Locus`, `ImagePhenotype`, `TemperatureSensor`, `DroughtStress`, `exhibitsResiliencePhenotype` | Bridges phenomic computer vision scoring with environmental sensor streams and genetic mapping data. |
| **CQ-MM-12** | Given a close-up image of sheath blight lesions on lower culms, what chemical dosage in agronomic extension bulletins is recommended if IoT sensors show relative humidity staying below 75% over the coming 48 hours? | Relational | **Image × Text × Sensor** | `CulmImage`, `DiseaseSeverity`, `WeatherForecastSensor`, `BulletinGuideline`, `prescribesDosageThreshold` | Enables context-aware precision spraying recommendations modulated by microclimate risk forecasts. |

---

## 3. Multimodal Traceability & Cross-Modal Coverage Matrix

This matrix demonstrates how the 32 Competency Questions comprehensively span all single modalities and multi-way multimodal combinations, ensuring no semantic silos exist within the graph schema.

| Modality Combination | Participating Modalities | Associated CQ IDs | Coverage Assessment |
| :--- | :--- | :--- | :--- |
| **Unimodal: Text** | Text (Literature, Extension, Reports) | CQ-TXT-01, CQ-TXT-02, CQ-TXT-03, CQ-TXT-04, CQ-TXT-05 | Full coverage of taxonomy, interventions, reservoirs, etiology, and biotypes. |
| **Unimodal: Image** | Image (RGB, Macroscopic, Microscopy) | CQ-IMG-01, CQ-IMG-02, CQ-IMG-03, CQ-IMG-04, CQ-IMG-05 | Covers lesion morphology, differential visual diagnosis, organs, and severity. |
| **Unimodal: Sensor** | Sensor (Time Series, IoT, Microclimate) | CQ-ENV-01, CQ-ENV-02, CQ-ENV-03, CQ-ENV-04 | Covers direct telemetry, temporal thresholding, spatial proximity, and anomaly baselines. |
| **Unimodal: Genomic**| Genomic & Tabular (Cultivars, Loci, Trials) | CQ-GEN-01, CQ-GEN-02, CQ-GEN-03, CQ-GEN-04 | Covers gene mapping, gene pyramiding, trial longitudinal scoring, and marker-pathotype links. |
| **Bimodal: Text × Image** | Text + Image | CQ-MM-05 | Validates symptom terminology against diagnostic visual evidence. |
| **Bimodal: Text × Genomic** | Text + Genomic | CQ-MM-09 | Correlates cultivar genotype catalogs with literature-documented resistance breakdown. |
| **Bimodal: Image × Sensor** | Image + Sensor | CQ-MM-04 | Links visual disease manifestation directly to recorded microclimatic triggers. |
| **Bimodal: Sensor × Tabular**| Sensor + Tabular | CQ-MM-08 (Image component secondary to Sensor×Tabular trend) | Ground sensor microclimate correlated with tabular pest surveillance census counts. |
| **Trimodal: Image × Sensor × Text** | Image + Sensor + Text | CQ-MM-01, CQ-MM-06, CQ-MM-10, CQ-MM-12 | Robust cross-validation of visual pathology, microclimatic drivers, and agronomic guidelines. |
| **Trimodal: Sensor × Genomic × Tabular** | Sensor + Genomic + Tabular | CQ-MM-03 | Dynamic varietal advisory matching live sensor risk to genomic cultivar matrices. |
| **Trimodal: Genomic × Image × Sensor** | Genomic + Image + Sensor | CQ-MM-07, CQ-MM-11 | Real-world phenotypic validation of genomic resistance under measured ambient infection stress. |
| **Four-Way Fusion** | Text + Image + Sensor + Genomic | **CQ-MM-02** | Complete cross-modal synthesis: symptom vision + sensor microclimate + cultivar genome + gene-for-gene literature. |

---

## 4. Scope Boundary Specification & Feasibility Statement

### In-Scope Functional Boundaries
Following the Grüninger & Fox methodology, the Rice-MMKG is scoped to formally represent and query:
1. Canonical etiologies, pathogen-pest taxonomies, and literature-derived intervention guidelines for major rice biotic stresses.
2. Image annotations associating visual symptom manifestations, anatomical plant structures, and severity scales with specific diseases and pests.
3. Spatio-temporal microclimatic observation events (temperature, relative humidity, leaf wetness duration, rainfall) and their thresholded infection incubation windows.
4. Rice cultivar entities, mapped resistance genes (*R*-genes / *QTLs*), pathogen race interactions, and multi-environment phenotypic trial tables.
5. Multimodal inference paths that link real-time sensor observations and visual field evidence to genomic varietal vulnerability and targeted agronomic recommendations.

### Out-of-Scope Boundaries
The following dimensions are explicitly defined as out-of-scope for the Rice-MMKG core schema:
1. End-to-end biochemical pathway modeling and intra-cellular gene expression / transcriptomic regulatory dynamics.
2. General macroeconomic market price fluctuations, national commodity supply chain logistics, and grain trade policy.
3. Non-rice plant species, except in their direct ecological capacity as verified alternate weed hosts or vector over-seasoning reservoirs.
4. Heavy raw binary data storage (e.g., raw TIFF/JPEG images or raw millivolt sensor streams directly stored inside RDF triples); the KG stores semantic annotations, feature vectors, embeddings, and dereferenceable URI references to raw binary repositories.

### Feasibility Flag & Risk Mitigation Note
- **Feasibility Warning on CQ-GEN-04 & CQ-MM-02:** Full realization of four-way and deep genomic queries requires granular, curated race-specific *Avr* pathogen gene catalogs and cultivar-specific *R*-gene introgression tables. Where fine-grained sequencing data is incomplete in regional extension registries, the KG must instantiate proxy relations (e.g., `hasReportedToleranceLevel` via Crop Ontology terms) to maintain query solvability without producing dead-end graph traversals.
- **Sensor Timestamp Alignment on CQ-MM-01 & CQ-MM-08:** Queries spanning sensor time-series and field photos depend on precise GPS location and ISO-8601 UTC timestamp alignment. Sensor graphs must incorporate explicit spatial geometry (`geo:SpatialThing`) and temporal interval patterns (`time:ProperInterval`) to prevent alignment failures.
