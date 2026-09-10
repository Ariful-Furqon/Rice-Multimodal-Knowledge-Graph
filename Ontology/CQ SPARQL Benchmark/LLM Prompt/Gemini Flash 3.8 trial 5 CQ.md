# Competency Question Specification for a Rice Pest & Disease Multimodal Knowledge Graph (Rice-MMKG)

## 1. System Purpose and Scope Confirmation

The **Rice-MMKG** is a multimodal knowledge graph engineered to empower plant pathology researchers, agricultural extension officers, and precision-agriculture / IoT decision-support systems in diagnosing, monitoring, and managing major rice (*Oryza sativa*) pests and diseases. By semantically unifying unstructured scientific text/extension bulletins, field and macro-symptom imagery, agroclimatic IoT sensor streams, and structured cultivar/genomic resistance datasets, the KG supports evidence-backed diagnosis, epidemiological risk prediction, and cultivar recommendation. 

**Assumed Baseline Context:**
- **Pests & Diseases in Scope:** Rice blast (*Magnaporthe oryzae*), Bacterial leaf blight (*Xanthomonas oryzae* pv. *oryzae*), Sheath blight (*Rhizoctonia solani*), Tungro virus (RTBV / RTSV transmitted by *Nephotettix virescens*), Brown planthopper (*Nilaparvata lugens*), Yellow stem borer (*Scirpophaga incertulas*), and Rice bug (*Leptocorisa oratorius*).
- **Target Agroecosystem:** Tropical lowland and irrigated rice systems (e.g., Southeast Asia / South Asia).
- **Standards & Ontology Alignments:** Crop Ontology (CO), AGROVOC, Plant Trait Ontology (TO), Plant Phenotype Ontology (PPO), Environment Ontology (ENVO), and Infectious Disease Ontology (IDO) design patterns.

---

## 2. Competency Questions by Modality Category

### Category A: Text-Grounded Competency Questions (Unimodal: Text)
*Synthesized from peer-reviewed plant pathology literature, extension bulletins, and authoritative disease compendia.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-TXT-01** | What is the primary taxonomic pathogen, taxonomic family, and transmission vector (if applicable) for Rice Tungro Disease? | Simple | `Disease`, `hasCausalAgent`, `Pathogen`, `hasVector`, `InsectVector` | Establishes core taxonomic and vector-pathogen relationship foundations for viral diseases. |
| **CQ-TXT-02** | Which registered chemical fungicides or biocontrol agents are recommended for controlling *Rhizoctonia solani* during the panicle initiation stage? | Relational | `Disease`, `recommendedTreatment`, `ControlAgent`, `applicableGrowthStage`, `PlantGrowthStage` | Supports clinical decision-support systems for timely agronomic interventions. |
| **CQ-TXT-03** | What are the known secondary host plants and overwintering/off-season habitats of *Nilaparvata lugens* in irrigated lowland ecosystems? | Relational | `Pest`, `hasAlternativeHost`, `PlantSpecies`, `survivesInHabitat`, `HabitatType` | Informs pest reservoir tracking and landscape-level integrated pest management (IPM). |
| **CQ-TXT-04** | How does excessive nitrogen fertilization affect the physiological susceptibility of rice leaves to *Magnaporthe oryzae* infection? | Complex-Inferential | `NutrientApplication`, `modulatesSusceptibility`, `HostPhysiology`, `predisposesTo`, `Disease` | Enables knowledge extraction regarding nutritional predisposition to blast epidemics. |
| **CQ-TXT-05** | Which diagnostic differential text criteria distinguish early bacterial leaf streak (*Xanthomonas oryzae* pv. *oryzicola*) from bacterial leaf blight (*Xanthomonas oryzae* pv. *oryzae*)? | Relational | `Disease`, `hasSymptomDescription`, `DiagnosticSign`, `differentialDiagnosisWith`, `Pathogen` | Prevents diagnostic conflation between closely related xanthomonad pathovars. |
| **CQ-TXT-06** | What economic threshold levels (ETL) in pest population counts per hill justify chemical intervention against *Scirpophaga incertulas* at the tillering stage? | Complex-Inferential | `Pest`, `hasEconomicThreshold`, `PopulationDensity`, `evaluatedAtStage`, `GrowthStage` | Defines quantitative trigger thresholds for IPM spraying rules. |

---

### Category B: Image-Grounded Competency Questions (Unimodal: Image)
*Derived from visual symptom morphology, macro-photography, and bounding-box / semantic segmentation annotations.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-IMG-01** | Which plant anatomical parts (leaf blade, leaf sheath, collar, node, or panicle neck) display lesion symptoms in a given field photograph? | Simple | `FieldImage`, `depictsAnatomicalPart`, `PlantAnatomicalEntity`, `exhibitsSymptom`, `Lesion` | Verifies fine-grained organ-level spatial localization in visual diagnostics. |
| **CQ-IMG-02** | Does the lesion depicted on the leaf blade exhibit characteristic spindle-shaped (elliptical) margins with a grey-white center and brown-red halo? | Relational | `Image`, `showsLesionPattern`, `LesionShape`, `hasMarginColor`, `ColorEntity`, `hasCenterColor` | Captures explicit phenotypic feature extraction for differential visual blast identification. |
| **CQ-IMG-03** | What is the visually estimated percentage of diseased leaf area (defoliation/necrosis severity score) across a segmented canopy image? | Complex-Inferential | `CanopyImage`, `hasSegmentedRegion`, `DiseasedAreaRatio`, `mapsToSeverityScale`, `SeverityScore` | Automates quantitative disease severity index scoring per Standard Evaluation System (SES). |
| **CQ-IMG-04** | In an image of a rice hill displaying "hopperburn", are visible adult brachypterous planthoppers clustered at the base of the tillers? | Relational | `Image`, `depictsDamageSymptom`, `Hopperburn`, `containsPestMorphotype`, `InsectMorph` | Links whole-plant damage phenotypes with proximate morphological evidence of the pest. |
| **CQ-IMG-05** | How do visual symptoms of physiological zinc deficiency (bronzing) differentiate from Tungro virus orange-yellow discoloration in leaf imagery? | Complex-Inferential | `FieldImage`, `exhibitsDiscoloration`, `PhenotypicPattern`, `differentiatesDiseaseFromDisorder`, `AbioticStress` | Mitigates visual misclassification between nutritional disorders and viral pathophenotypes. |
| **CQ-IMG-06** | Does an image of a damaged panicle exhibit "whitehead" (empty bleached panicle) caused by stem borer tunneling versus neck blast breakage? | Complex-Inferential | `PanicleImage`, `exhibitsSymptom`, `WhiteheadSign`, `indicativeOfStemDamage`, `BorerDamage` | Distinguishes visual damage mimicry between internal pest feeding and fungal neck infection. |

---

### Category C: Sensor/Environmental-Grounded Competency Questions (Unimodal: Sensor/IoT)
*Grounded in in-situ microclimate sensors, automatic weather stations, and soil probe time-series.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-ENV-01** | What was the average canopy temperature, relative humidity, and continuous leaf wetness duration (hours) recorded in Field Station X over the past 48 hours? | Simple | `WeatherStation`, `recordedVariable`, `Temperature`, `RelativeHumidity`, `LeafWetnessDuration`, `TimeInterval` | Validates fundamental IoT time-series retrieval and observational telemetry aggregation. |
| **CQ-ENV-02** | Have continuous relative humidity levels exceeded 90% in combination with nighttime temperatures between 17°C and 23°C for at least 3 consecutive days? | Relational | `SensorStream`, `satisfiesConditionWindow`, `MicroclimateWindow`, `associatedWithInfectionIndex`, `EnvironmentalThreshold` | Encodes epidemiologically validated sporulation and infection threshold rules for blast. |
| **CQ-ENV-03** | What is the cumulative rainfall (mm) and solar radiation deficit observed over a 14-day rolling window preceding historical bacterial blight surges? | Complex-Inferential | `RainfallSensor`, `aggregatedSum`, `SolarRadiationSensor`, `temporalWindow`, `EpidemicSpike` | Evaluates environmental precursors and storm-induced physical micro-injury dynamics. |
| **CQ-ENV-04** | How do diurnal temperature fluctuations (DTR) within a densely planted canopy compare against ambient ambient weather station observations? | Relational | `CanopySensor`, `hasDeltaWith`, `AmbientStationSensor`, `measuresParameter`, `DiurnalTemperatureRange` | Models microclimatic buffering within dense stands conducive to sheath blight. |
| **CQ-ENV-05** | Which sensor nodes detected sudden microclimate drops in soil moisture and elevated canopy temperature indicative of early root/stem lodging stress? | Complex-Inferential | `SensorNode`, `detectsAnomalyPattern`, `SoilMoistureDepletion`, `CanopyHeatStress`, `TemporalSequence` | Detects abiotic stress signatures that lower plant basal resistance to opportunistic pathogens. |

---

### Category D: Genomic/Tabular-Grounded Competency Questions (Unimodal: Genotype/Agronomy)
*Derived from rice cultivar registries, gene banks, QTL mapping datasets, and agronomic trial tables.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-GEN-01** | Which specific major resistance genes (e.g., *Pita*, *Piz-t*, *Pi2*, *Pi9*) are introgressed into cultivar 'IR64' and 'Swarna-Sub1'? | Simple | `RiceCultivar`, `carriesResistanceGene`, `GeneLocus`, `confersResistanceTo`, `Pathogen` | Enables genetic lookup of documented resistance alleles in popular foundation cultivars. |
| **CQ-GEN-02** | Which rice cultivars carry broad-spectrum *Xa* genes (*Xa21*, *xa13*, *xa5*) effective against circulating virulent pathotypes of *Xanthomonas oryzae*? | Relational | `RiceCultivar`, `hasAllele`, `ResistanceGene`, `protectsAgainstPathotype`, `BacterialPathotype` | Directs resistant cultivar selection against regional bacterial blight pathotypes. |
| **CQ-GEN-03** | Which cultivars possess the *Bph1*, *Bph2*, or *Bph3* resistance loci conferring anti-xenosis or antibiosis to the Brown Planthopper? | Relational | `RiceCultivar`, `exhibitsTrait`, `InsectResistanceMechanism`, `governedByLocus`, `BphLocus` | Identifies genetic protection lines against biotypes of *Nilaparvata lugens*. |
| **CQ-GEN-04** | What is the historical yield penalty, maturity duration (days), and average plant height recorded in multi-location agronomic trials for cultivar 'Ciherang'? | Simple | `RiceCultivar`, `hasMaturityDuration`, `DaysToMaturity`, `hasAgronomicTrait`, `YieldTrialData` | Ensures that disease resistance advice does not compromise baseline agronomic suitability. |
| **CQ-GEN-05** | Which gene pyramided lines (possessing ≥3 distinct functional blast resistance genes) are currently cataloged in the knowledge graph? | Complex-Inferential | `RiceCultivar`, `hasPyramidedGenes`, `GeneSet`, `cardinalityGreaterThan`, `IntegerThreshold` | Pinpoints durable, multi-gene resistance resources to mitigate boom-and-bust cycles. |

---

### Category E: Cross-Modal / Multimodal Fusion Competency Questions
*Synergistic reasoning requiring simultaneous synthesis across 2, 3, or all 4 modalities. This constitutes the core rationale for Rice-MMKG.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Modalities | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CQ-MM-01** | Given an image showing diamond-shaped leaf lesions and a continuous 72-hr sensor record showing relative humidity >92% and temperature 20–25°C, is the diagnosis *Magnaporthe oryzae*, and what textual literature confirms this infection window? | Relational | `Image`, `depictsLesion`, `MicroclimateRecord`, `triggersRiskRule`, `Disease`, `corroboratedByLiterature`, `Publication` | **Image × Sensor × Text** | Combines morphological image evidence with microclimatic incubation criteria and verified literature. |
| **CQ-MM-02** | A field image shows typical bacterial leaf blight lesions on cultivar 'IR64'; cross-referencing IR64’s genomic profile (*xa5* absent) and regional extension surveillance texts, what is the inferred pathogen pathotype? | Complex-Inferential | `Image`, `identifiesSymptom`, `Cultivar`, `lacksResistanceGene`, `PathogenPathotype`, `reportedInBulletin`, `SurveillanceText` | **Image × Genomic × Text** | Deduce pathogen strain identity from cultivar gene vulnerability and visual symptom manifestation. |
| **CQ-MM-03** | When sensor microclimate data indicates high sheath blight infection pressure (*Rhizoctonia solani*), which recommended fungicides in extension texts are approved for the specific vegetative growth stage identified in field photos? | Relational | `SensorStream`, `predictsDiseaseRisk`, `Disease`, `GrowthStage`, `derivedFromImage`, `recommendedPesticide`, `ExtensionText` | **Sensor × Image × Text** | Synchronizes real-time microclimate disease alerts with visual crop phenology to prescribe treatment. |
| **CQ-MM-04** | In a farm plot planted with a cultivar carrying only *Bph1*, if canopy imagery exhibits initial hopperburn and IoT acoustic/visual trap counters detect planthopper surges, what resistant replacement cultivars in the genomic catalog should be recommended for subsequent planting? | Complex-Inferential | `Cultivar`, `hasGene`, `FieldImage`, `exhibitsHopperburn`, `IoTTrapSensor`, `detectsSurge`, `AlternativeCultivar`, `carriesGene`, `Bph3` | **Image × Sensor × Genomic** | Informs long-term agronomic adaptation when monogenic cultivar resistance collapses under pest surge. |
| **CQ-MM-05** | Given historical weather sensor series, field-scouting images taken across tillering to booting stages, and literature pest phenology models, which upcoming 14-day window represents peak *Scirpophaga incertulas* adult oviposition risk? | Complex-Inferential | `HistoricalWeatherSeries`, `ScoutingImage`, `identifiesCropStage`, `PhenologyModel`, `predictsBroodEmergence`, `CalendarWindow` | **Sensor × Image × Text** | Forecasts pest brood emergence using environmental thermal sum models and visual phenological stage. |
| **CQ-MM-06** | Does a segmented leaf image show characteristic Tungro symptoms (interveinal chlorosis/stunting), and do ambient vector trap sensors and extension texts confirm *Nephotettix virescens* presence in that district? | Relational | `LeafImage`, `showsChlorosis`, `VectorTrapSensor`, `recordsPopulation`, `InsectVector`, `surveillanceConfirmedBy`, `ExtensionBulletin` | **Image × Sensor × Text** | Eliminates visual confusion between Tungro and physiological disorders by confirming vector presence. |
| **CQ-MM-07** | Which rice cultivars documented in trial tables exhibit blast-resistant phenotypes under high natural disease pressure (verified by sensor-confirmed high leaf wetness (>10 hrs/day) and low lesion-area ratios in drone canopy images)? | Complex-Inferential | `Cultivar`, `evaluatedUnder`, `SensorRecord`, `LeafWetnessDuration`, `DroneImage`, `calculatedLesionRatio`, `FieldTrial` | **Genomic × Sensor × Image** | Enables objective, multimodal field phenotyping of disease resistance under natural infection pressure. |
| **CQ-MM-08** | Given a uploaded smartphone photo of severe sheath blight advancing to the upper canopy, sensor records showing RH >95%, and cultivar metadata indicating high tillering density, what harvest yield loss range does literature predict if left untreated? | Complex-Inferential | `Image`, `measuresVerticalProgression`, `SensorStream`, `RelativeHumidity`, `Cultivar`, `hasTilleringDensity`, `YieldLossPrediction`, `LiteratureStudy` | **Image × Sensor × Genomic × Text** | Comprehensive 4-way fusion for quantitative yield loss risk assessment and clinical triage. |
| **CQ-MM-09** | Identify all historical field cases where a cultivar carrying gene *Xa4* showed visual breakdown of bacterial blight resistance (confirmed by diagnostic lesions in images) under storm/heavy rainfall sensor patterns. | Relational | `Cultivar`, `hasResistanceGene`, `Xa4`, `FieldImage`, `showsBacterialBlight`, `SensorData`, `indicatesStormWind`, `DiseaseBreakdownEvent` | **Genomic × Image × Sensor** | Audits environmental stress conditions causing physical tissue damage that bypasses genetic resistance. |
| **CQ-MM-10** | A farmer uploads a photo of dead tillers ("deadheart"); cross-referencing soil pH sensor data, local extension reports of stem borer outbreaks, and variety resistance profiles, what is the probability ranking between stem borer vs. salinity damage? | Complex-Inferential | `FieldImage`, `depictsDeadheart`, `SoilSensor`, `measuresSalinity`, `ExtensionReport`, `alertsOutbreak`, `DifferentialDiagnosisProbability` | **Image × Sensor × Text × Genomic** | Multi-modal differential diagnosis resolving symptom mimicry between abiotic and biotic stresses. |
| **CQ-MM-11** | Which scientific publications describe chemical resistance in *Nilaparvata lugens* populations in regions where local IoT pest light traps recorded persistent pest densities above economic threshold despite registered insecticide usage? | Complex-Inferential | `ScientificPublication`, `documentsPesticideResistance`, `Pest`, `IoTLightTrap`, `recordsDensityAboveETL`, `ManagementLog`, `InsecticideApplication` | **Text × Sensor** | Pinpoints emerging pesticide resistance hot-spots by linking field sensor anomalies with peer-reviewed literature. |
| **CQ-MM-12** | For an unidentified disease image showing circular lesions with yellow margins, what are the top-3 candidate diseases whose symptom text matches the image and whose microclimatic incubation range matches the local sensor stream over the last 5 days? | Complex-Inferential | `Image`, `hasVisualPattern`, `TextCorpus`, `describesSymptomMorphology`, `SensorStream`, `matchesMicroclimaticEnvelope`, `RankedCandidateDisease` | **Image × Text × Sensor** | Powers similarity-based multimodal reasoning for zero-shot or rare disease triage. |
| **CQ-MM-13** | Which cultivars carrying blast resistance genes (*Pi* loci) demonstrated effective resistance in historical image databases across locations where ambient sensor records show at least 50 hours of blast-conducive microclimate? | Relational | `Cultivar`, `carriesGene`, `PiLocus`, `HistoricalImage`, `showsNoBlastSymptom`, `SensorRecord`, `exceedsInfectionThreshold` | **Genomic × Image × Sensor** | Validates field durability of resistance genes under verified real-world pathogen pressure. |
| **CQ-MM-14** | Given a smartphone photo of panicle neck discoloration, does the genomic resistance of the planted cultivar (*Pita* present) and sensor records of continuous dry conditions favor a diagnosis of Brown Spot or drought necrosis rather than Neck Blast? | Complex-Inferential | `PanicleImage`, `depictsDiscoloration`, `Cultivar`, `carriesGene`, `Pita`, `SensorData`, `showsDroughtStress`, `DifferentialDiagnosis` | **Image × Genomic × Sensor** | Synthesizes negative genetic susceptibility and unfavorable pathogen climate to reject false positive visual diagnoses. |

---

## 3. Modality-Pair Coverage and Traceability Matrix

The matrix below maps each pairing and combination of modalities to the specific Competency Questions that test and enforce semantic linkage across them.

| Modality Combination | Covered Competency Questions (CQ IDs) | Primary Semantic Bridges & Properties |
| :--- | :--- | :--- |
| **Text Only** | CQ-TXT-01, CQ-TXT-02, CQ-TXT-03, CQ-TXT-04, CQ-TXT-05, CQ-TXT-06 | `hasCausalAgent`, `recommendedTreatment`, `hasVector`, `hasEconomicThreshold` |
| **Image Only** | CQ-IMG-01, CQ-IMG-02, CQ-IMG-03, CQ-IMG-04, CQ-IMG-05, CQ-IMG-06 | `depictsAnatomicalPart`, `showsLesionPattern`, `mapsToSeverityScale`, `exhibitsSymptom` |
| **Sensor / IoT Only** | CQ-ENV-01, CQ-ENV-02, CQ-ENV-03, CQ-ENV-04, CQ-ENV-05 | `recordedVariable`, `satisfiesConditionWindow`, `measuresParameter`, `detectsAnomalyPattern` |
| **Genomic / Tabular Only**| CQ-GEN-01, CQ-GEN-02, CQ-GEN-03, CQ-GEN-04, CQ-GEN-05 | `carriesResistanceGene`, `protectsAgainstPathotype`, `hasAgronomicTrait`, `hasPyramidedGenes` |
| **Text × Image** | CQ-MM-01, CQ-MM-02, CQ-MM-03, CQ-MM-06, CQ-MM-10, CQ-MM-12 | `hasSymptomDescription` ↔ `showsVisualPattern`, `depictsDamage` ↔ `documentedInReport` |
| **Text × Sensor** | CQ-MM-01, CQ-MM-03, CQ-MM-05, CQ-MM-06, CQ-MM-11, CQ-MM-12 | `hasConduciveRange` ↔ `recordedObservation`, `thresholdRule` ↔ `sensorStream` |
| **Text × Genomic** | CQ-MM-02, CQ-MM-08, CQ-MM-10 | `literatureYieldModel` ↔ `cultivarAgronomicProfile`, `pathotypeSusceptibility` ↔ `geneCatalog` |
| **Image × Sensor** | CQ-MM-01, CQ-MM-03, CQ-MM-04, CQ-MM-05, CQ-MM-06, CQ-MM-07, CQ-MM-08, CQ-MM-09, CQ-MM-10, CQ-MM-12, CQ-MM-13, CQ-MM-14 | `imageObservationTimestamp` ↔ `sensorTimeInterval`, `visualPhenotype` ↔ `environmentalStressIndex` |
| **Image × Genomic** | CQ-MM-02, CQ-MM-04, CQ-MM-07, CQ-MM-08, CQ-MM-09, CQ-MM-10, CQ-MM-13, CQ-MM-14 | `exhibitedLesionSeverity` ↔ `introgressionStatus`, `fieldPhenotypeImage` ↔ `cultivarGenotype` |
| **Sensor × Genomic** | CQ-MM-04, CQ-MM-07, CQ-MM-08, CQ-MM-09, CQ-MM-10, CQ-MM-13, CQ-MM-14 | `environmentalPressureThreshold` ↔ `geneBreakdownRisk`, `microclimateHistory` ↔ `cultivarTolerance` |
| **Three-Way Combinations**| CQ-MM-01 (Img×Sen×Txt), CQ-MM-02 (Img×Gen×Txt), CQ-MM-03 (Sen×Img×Txt), CQ-MM-04 (Img×Sen×Gen), CQ-MM-05 (Sen×Img×Txt), CQ-MM-06 (Img×Sen×Txt), CQ-MM-07 (Gen×Sen×Img), CQ-MM-09 (Gen×Img×Sen), CQ-MM-12 (Img×Txt×Sen), CQ-MM-13 (Gen×Img×Sen), CQ-MM-14 (Img×Gen×Sen) | Multi-hop join across phenotypic image features, microclimatic telemetry, and genomic locus identifiers |
| **Four-Way Full Fusion** | **CQ-MM-08, CQ-MM-10** | Unified cross-modal reasoning binding visual symptom segmentation, environmental time series, genomic resistance profiles, and literature/extension rules |

---

## 4. Scope Boundary & Feasibility Statement

### In Scope
- **Domain Coverage:** Pathological diagnosis, visual symptom identification, microclimatic environmental triggers, vector entomology, and cultivar resistance genetics for the seven specified major rice pests and diseases (*M. oryzae*, *X. oryzae*, *R. solani*, Rice Tungro Virus, *N. lugens*, *S. incertulas*, and *L. oratorius*).
- **Multimodal Integration:** Explicit semantic joins connecting image entities (bounding boxes, lesion traits), IoT sensor observations (temperature, relative humidity, leaf wetness), genomic loci/cultivars, and text assertions (treatment recommendations, epidemiology rules).
- **Standards Compliance:** Re-use of ontological URIs and patterns from AGROVOC (taxa, chemicals), Crop Ontology (traits, anatomy), ENVO (environmental parameters), and W3C SSN/SOSA (sensor telemetry and observations).

### Out of Scope
- **Post-Harvest & Storage Pathology:** Storage pests (e.g., *Sitophilus oryzae*) and mycotoxin storage rots are excluded.
- **Upstream Molecular Biology / Raw Sequencing:** Raw genomic reads (FASTQ/BAM), high-throughput transcriptome pipelines, and detailed protein-protein interaction (PPI) networks are excluded; genetic data is scoped to cultivar, locus, gene symbol, and validated phenotype resistance traits.
- **Automated Actuator Hardware Control:** Direct machine-to-machine industrial automation protocols (e.g., opening irrigation sluice gates or variable-rate sprayer PWM nozzles) are out of scope; the KG provides prescriptive recommendations rather than autonomous robotics execution.

### Data Feasibility and Implementation Risks
1. **Continuous Leaf Wetness Telemetry (CQ-ENV-01, CQ-ENV-02, CQ-MM-01, CQ-MM-07):** Physical leaf wetness sensors are prone to drift and calibration artifacts in open tropical paddy fields; proxy modeling based on ambient RH (>90%) and dew point depression may be required where physical grid sensors are unavailable.
2. **Dense Canopy vs. Ambient Weather Alignment (CQ-ENV-04):** Many historical rice datasets only provide regional open-air synoptic weather data rather than within-canopy microclimate readings. For legacy datasets, empirical microclimate translation models must be incorporated.
3. **Genomic Coverage of Local Landraces (CQ-GEN-01 to CQ-GEN-05, CQ-MM-04):** While elite mega-varieties (IR64, Swarna, Ciherang) possess comprehensively sequenced resistance loci, smaller local varieties and landraces may lack documented *Pi* or *Xa* gene annotations in national registry tables.
