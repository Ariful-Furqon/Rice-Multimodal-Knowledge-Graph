# Ontology Requirements Specification: Competency Questions for a Rice Pest and Disease Multimodal Knowledge Graph (Rice-MMKG)

## 1. System Purpose, Scope, and Context Confirmation

The **Rice Pest and Disease Multimodal Knowledge Graph (Rice-MMKG)** is designed to provide an integrated semantic data infrastructure supporting precision diagnostics, epidemiological surveillance, and agronomic decision-support for major rice (*Oryza sativa*) pests and diseases. The primary target users include plant pathology researchers, agricultural extension officers, and developers of IoT-enabled smart-farming advisory systems, with an initial agroecological focus on Southeast Asian tropical lowland irrigated rice systems. 

To bridge disparate scientific disciplines and data silos, the KG harmonizes four core modalities:
1. **Unstructured Text**: Scientific literature, extension bulletins, and standard diagnostic keys.
2. **Visual Imagery**: In-field macro/micro photographs capturing foliar, culm, and panicle lesions and insect pest manifestations.
3. **Environmental and Microclimate Sensors**: High-resolution time-series of canopy temperature, relative humidity, leaf wetness duration, and precipitation.
4. **Genomic and Tabular Cultivar Records**: Lineage, resistance genes (*R*-genes / QTLs), biotype/pathotype resistance profiles, and phenotypic reaction scores.

Ontological entities and relations are aligned where applicable with international semantic standards, including **AGROVOC**, the **Crop Ontology (CO)**, the **Plant Phenotype Ontology (PPO)**, the **Plant Trait Ontology (TO)**, and the **Infectious Disease Ontology (IDO)** core patterns.

---

## 2. Competency Questions Specification

### 2.1 Category A: Text-Grounded Competency Questions
*Focus: Verified botanical, pathological, epidemiological, and chemical/biological management knowledge extracted from scientific literature and extension guides.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-TXT-01** | Which fungal, bacterial, or viral pathogens are established causal agents of rice blast, bacterial leaf blight (BLB), and sheath blight? | Simple | `Disease`, `causedBy`, `Pathogen`, `Taxon` | Establishes foundational taxonomic linkage between pathological conditions and microbiological etiology. |
| **CQ-TXT-02** | What are the recommended chemical active ingredients, biological control agents, and application intervals for managing Brown Planthopper (*Nilaparvata lugens*) infestations? | Relational | `Pest`, `controlledBy`, `ManagementPractice`, `ActiveIngredient`, `BiologicalControlAgent`, `applicationInterval` | Essential for agronomic advisory pipelines prescribing verified curative or preventive field interventions. |
| **CQ-TXT-03** | How do the standard diagnostic descriptions distinguish early physiological zinc deficiency from early-stage Tungro spherical virus infection in terms of chlorosis progression? | Relational | `AbioticDisorder`, `Disease`, `manifestsSymptom`, `Symptom`, `PlantAnatomy`, `progressionStage` | Enables unambiguous differential diagnosis between physiological nutritional disorders and viral pathologies in literature text mining. |
| **CQ-TXT-04** | Which alternate weed hosts or volunteer vegetation serve as primary overwintering/inter-season reservoirs for *Rhizoctonia solani* and Rice Grassy Stunt Virus? | Relational | `Pathogen`, `Virus`, `persistsInHost`, `WeedHost`, `Taxon`, `TransmissionVector` | Critical for off-season epidemiology and area-wide integrated pest management (IPM) sanitation protocols. |
| **CQ-TXT-05** | What documented agronomic practices (e.g., nitrogen over-fertilization, high planting density) statistically increase crop vulnerability to Sheath Blight and False Smut (*Ustilaginoidea virens*)? | Complex-Inferential | `AgronomicPractice`, `NitrogenRegime`, `exacerbates`, `Disease`, `PlantingDensity`, `RiskFactor` | Required for risk-factor auditing and modeling causal agronomic contributions to disease severity. |
| **CQ-TXT-06** | Which insect vectors are capable of transmitting Rice Tungro Bacilliform Virus (RTBV) versus Rice Tungro Spherical Virus (RTSV), and what are their respective transmission retention dynamics? | Complex-Inferential | `Virus`, `vectoredBy`, `InsectVector`, `transmissionType`, `retentionTime`, `VectorEfficiency` | Necessary for epidemiological vector modeling and tracing viral transmission mechanisms. |

---

### 2.2 Category B: Image-Grounded Competency Questions
*Focus: Visual phenotypes, spatial distributions of lesions, anatomical organ involvement, and morphological pest identification.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-IMG-01** | Does an input leaf photograph depict spindle-shaped, elliptical lesions with necrotic gray centers and reddish-brown borders diagnostic of *Magnaporthe oryzae* foliar blast? | Simple | `Image`, `depicts`, `LesionMorphology`, `ColorProfile`, `diagnosticOf`, `Disease` | Underpins computer vision verification and bounding-box validation against standardized disease symptom definitions. |
| **CQ-IMG-02** | On which specific anatomical structures (e.g., leaf blade, leaf sheath, collar, panicle neck) are the pathological lesions located in a given diagnostic photograph? | Relational | `Image`, `localizesAt`, `PlantAnatomicalEntity`, `PPO:hasPart`, `Symptom` | Drives fine-grained organ-specific classification (e.g., differentiating leaf blast from neck blast or sheath blight). |
| **CQ-IMG-03** | What estimated percentage of total leaf surface area in an annotated canopy image exhibits water-soaked lesions or chlorotic blighting? | Complex-Inferential | `Image`, `hasPhenotypicSymptom`, `LesionAreaRatio`, `Quantification`, `DiseaseSeverityScore` | Required for automated Standard Evaluation System (SES) disease severity scoring and grading from computer vision models. |
| **CQ-IMG-04** | Which physical developmental instar or morphotype of Brown Planthopper (*Nilaparvata lugens*—brachypterous vs. macropterous adult, or nymphal stages) is visible in a stem-base macro photo? | Relational | `Image`, `showsOrganism`, `InsectVector`, `hasLifeStage`, `hasMorphotype` | Morphotype identification directly indicates whether the population is migratory or stationary/resident, critical for hopperburn forecasting. |
| **CQ-IMG-05** | How do lesion margin characteristics (wavy/undulating vs. distinct margin) in a close-up image differentiate early Bacterial Leaf Streak (*Xanthomonas oryzae* pv. *oryzicola*) from narrow brown leaf spot (*Cercospora janseana*)? | Complex-Inferential | `Image`, `exhibitsPattern`, `LesionBoundary`, `differentiates`, `Disease` | Enables visual differential diagnosis between phenotypically overlapping foliar pathologies. |
| **CQ-IMG-06** | What is the visually determined density of Whitebacked Planthopper (*Sogatella furcifera*) individuals per rice hill across a series of segmented quadrate images? | Complex-Inferential | `ImageCollection`, `depictsOrganismCount`, `RiceHill`, `AggregationMetric`, `InfestationThreshold` | Automates visual pest counting to determine if pest pressure has exceeded economic injury thresholds (EIL). |

---

### 2.3 Category C: Sensor and Environmental-Grounded Competency Questions
*Focus: Temporal microclimate data, canopy sensors, moisture thresholds, degree-day calculations, and disease-conducive weather patterns.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-ENV-01** | What was the continuous duration (in hours) where microclimate canopy relative humidity exceeded 90% alongside ambient air temperatures between 24°C and 28°C over the past 7 days? | Simple | `SensorObservation`, `observedVariable`, `CanopyRelativeHumidity`, `AirTemperature`, `TemporalDuration` | Quantifies the fundamental physical microclimate envelope required for *Magnaporthe oryzae* conidial sporulation and infection. |
| **CQ-ENV-02** | Did the cumulative rain precipitation and daily average wind velocity in a given farm cluster exceed historical thresholds associated with canopy mechanical wounding during the past 48 hours? | Relational | `SensorStream`, `PrecipitationAccumulation`, `WindVelocity`, `exceedsThreshold`, `WoundingEvent` | Identifies abiotic preconditions that create ingress avenues for *Xanthomonas oryzae* pv. *oryzae* infection. |
| **CQ-ENV-03** | What is the cumulative growing degree-days (GDD) accumulated since transplanting date based on daily sensor data, and what pest generational turnover stage does this indicate? | Relational | `SensorObservation`, `hasGDD`, `CalculatedPhenology`, `correspondsTo`, `PestLifecycleStage` | Models temperature-dependent development rates of insect pests (e.g., Yellow Stem Borer, *Scirpophaga incertulas*). |
| **CQ-ENV-04** | Which specific geographic sensor nodes recorded sudden declines in soil volumetric water content below permanent wilting point alongside prolonged high vapor pressure deficits (VPD)? | Relational | `IoTNode`, `spatialLocation`, `SoilMoisture`, `VaporPressureDeficit`, `DroughtStress` | Detects severe abiotic drought stress episodes that predispose rice stands to opportunistic blast infection. |
| **CQ-ENV-05** | Has the rolling 72-hour moving average of canopy wetness duration and minimum nighttime temperatures fulfilled the epidemiological threshold required to trigger an automated Sheath Blight advisory warning? | Complex-Inferential | `TimeWindowAggregate`, `LeafWetnessDuration`, `NightTemperature`, `triggersAdvisory`, `EpidemiologicalModel` | Validates sensor-based automated early warning triggers without requiring manual scouting. |

---

### 2.4 Category D: Genomic, Cultivar, and Tabular-Grounded Competency Questions
*Focus: Cultivar identity, pedigree, major R-genes, quantitative trait loci (QTLs), pathotype virulence/avirulence matrices, and historical yield impacts.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-GEN-01** | Which documented major resistance genes (e.g., *Pi-ta*, *Piz-t*, *Pib*, *Pi2*, *Pi9*) are introgressed into rice cultivar 'IR64' or 'Ciherang'? | Simple | `RiceCultivar`, `carriesGene`, `ResistanceGene`, `GeneSymbol` | Direct lookup of cultivar genomic resistance profiles against fungal blast. |
| **CQ-GEN-02** | What are the known broad-spectrum bacterial leaf blight resistance genes present in released hybrid cultivars, and are they dominant (*Xa21*, *Xa4*) or recessive (*xa5*, *xa13*) alleles? | Simple | `ResistanceGene`, `hasAlleleType`, `ResistanceSpectrum`, `confersProtectionAgainst`, `Pathogen` | Crucial for gene-pyramiding analysis and predicting breakdown durability against bacterial races. |
| **CQ-GEN-03** | Which rice varieties possess dual resistance alleles conferring tolerance against both Brown Planthopper biotype 2 (*Bph3*, *bph4*) and Green Leafhopper? | Relational | `RiceCultivar`, `hasPyramidedGenes`, `InsectBiotype`, `ResistanceProfile` | Guides cultivar recommendation engines when multiple insect vector pressures co-occur in the same locality. |
| **CQ-GEN-04** | What was the documented average historical percentage yield loss in replicated regional trial datasets for cultivar 'Inpari 32' when exposed to bacterial blight pathotype IV? | Relational | `CultivarTrial`, `evaluatedCultivar`, `PathotypeStrain`, `YieldReductionScore`, `SESScore` | Supports economic impact modeling and yield gap assessments under specified pathogen pressures. |
| **CQ-GEN-05** | Which specific blast resistance genes have overcome durability (broken resistance) due to the emergence of virulent local isolates matching avirulence gene mutations (*AvrPita*)? | Complex-Inferential | `PathogenIsolate`, `hasAvirulenceLocus`, `overcomesResistance`, `ResistanceGene`, `DurabilityStatus` | Evaluates gene durability over time and tracks pathogen co-evolution across cropping seasons. |

---

### 2.5 Category E: Cross-Modal and Fusion Competency Questions
*Focus: Coordinated semantic reasoning across Text, Image, Sensor, and Genomic modalities to deliver multimodal diagnostic and agronomic decisions.*

| ID | Natural-Language Question | Complexity | Modalities Fused | Key Entities & Relations | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CQ-MM-01** | Given a field photograph depicting foliar necrotic lesions on cultivar 'IR64' and IoT sensor records showing 85+ continuous hours of >92% relative humidity at 26°C, which pathogen is diagnosed, and does 'IR64' harbor active resistance genes (*Pi-ta*) effective against current local isolates? | Complex-Inferential | **Image + Sensor + Genomic + Text** | `Image`, `depicts`, `Symptom`; `SensorRecord`, `corroborates`, `MicroclimateEnvelope`; `RiceCultivar`, `carriesGene`, `ResistanceGene`; `Pathogen`, `breaksResistance` | The quintessential multimodal KG diagnostic question: integrates visual symptom, microclimate trigger, cultivar resistance genetics, and pathogen virulence. |
| **CQ-MM-02** | A field image shows yellow-orange leaf discoloration accompanied by stunted tillering; sensor data indicates normal water and nutrient status, and historical survey texts note high Green Leafhopper populations. Is Tungro Virus the probable causal agent, and what urgent IPM action is recommended by extension guidelines? | Complex-Inferential | **Image + Sensor + Text** | `Image`, `showsSymptom`, `Chlorosis`; `SensorRecord`, `rulesOutAbioticStress`, `SoilCondition`; `SurveyReport`, `reportsVectorPresence`, `InsectVector`; `ExtensionProtocol`, `recommends` | Fuses visual pathology with sensor-based exclusion of abiotic drought/deficiency and textual pest trap records to trigger timely interventions. |
| **CQ-MM-03** | Based on segmented drone canopy images revealing irregular lodging patches ("hopperburn") and stem-base sensor readings of elevated relative humidity, what is the estimated *Nilaparvata lugens* population pressure, and which nearby plots growing varieties lacking the *Bph* gene cluster are at immediate secondary risk? | Complex-Inferential | **Image + Sensor + Genomic** | `AerialImage`, `detectsDamagePattern`, `Hopperburn`; `SensorStream`, `MicroclimateIndex`; `AdjacentPlot`, `growsCultivar`, `RiceCultivar`, `lacksGene`, `ResistanceGene` | Connects macro-scale visual damage patterns with microclimate sensors and surrounding field genetic vulnerability to forecast pest dispersal. |
| **CQ-MM-04** | When an uploaded smartphone photo of panicle neck lesions matches blast symptoms, but the farmer notes in text that the cultivar planted is certified 'Inpari 48' (possessing *Pi9*), does the KG infer a diagnostic false-positive image classification, an environmental abiotic neck rot, or a novel *Magnaporthe* pathotype breakout? | Complex-Inferential | **Image + Text + Genomic** | `Image`, `classifiedAs`, `Disease`; `TextAnnotation`, `identifiesVariety`, `RiceCultivar`; `Cultivar`, `carriesImmuneGene`, `ResistanceGene`; `InferenceEngine`, `hypothesizesPathotypeEvolution` | Performs semantic discrepancy detection between deep learning visual classifiers and cultivar genetic immunity records to catch misdiagnoses or pathotype shifts. |
| **CQ-MM-05** | Which chemical intervention listed in agronomic extension bulletins is legally authorized and biologically effective against Bacterial Leaf Blight on a crop currently at the panicle initiation stage (determined from cumulative sensor GDD), and does the chemical label text warn against phytotoxicity under current forecast temperatures (>35°C)? | Complex-Inferential | **Text + Sensor** | `AgronomicBulletin`, `authorizesChemical`, `Pesticide`; `SensorObservation`, `derivesPhenologyStage`, `CropGrowthStage`; `LabelText`, `contraindicatedAtTemperature`, `WeatherMetric` | Bridges dynamic environmental telemetry with static regulatory text and chemical safety contraindications for context-aware pesticide advisory. |
| **CQ-MM-06** | For a specific field block where sensors recorded over 12 hours of leaf wetness daily for 5 consecutive days and photos show diamond-shaped lesions, what are the top 3 alternative rice cultivars in regional seed catalog tables that (a) express verified resistance against this disease, (b) match the current season's maturity group (days to harvest), and (c) have historical yield penalties under 5% in wet-season trials? | Complex-Inferential | **Sensor + Image + Genomic/Tabular** | `SensorRecord`, `detectsRiskConditions`; `Image`, `confirmsDiagnosis`; `CultivarCatalog`, `recommendsVariety`, `ResistanceGene`, `MaturityDays`, `YieldTrialData` | Delivers cultivar replacement recommendations by linking real-time diagnosed outbreak conditions with historical agronomic trial performance. |
| **CQ-MM-07** | A high-resolution image depicts brown discoloration at the panicle neck and glumes. Does the KG synthesize textual diagnostic keys, local sensor dew-point data, and cultivar heading dates to reliably differentiate between Neck Blast (*Magnaporthe oryzae*), Bacterial Panicle Blight (*Burkholderia gladioli*), and Brown Spot (*Bipolaris oryzae*)? | Complex-Inferential | **Image + Text + Sensor + Genomic/Tabular** | `Image`, `showsOrganPart`, `Panicle`; `TextDiagnosticKey`, `differentialFeatures`; `SensorRecord`, `evaluatesDewPoint`; `CultivarTable`, `tracksDaysToHeading` | Solves the classic multi-etiology visual confusion problem at the critical panicle developmental stage through multimodal evidence fusion. |
| **CQ-MM-08** | By analyzing time-series of vegetative vigor index (NDVI) images alongside weekly soil-nitrogen sensor logs and published epidemiological text tables, what is the predicted risk score for Sheath Blight spread across a 10-hectare cooperative farm block over the next 14 days? | Complex-Inferential | **Image + Sensor + Text** | `MultispectralImage`, `tracksMetric`, `NDVI`; `SensorLog`, `quantifiesNitrogen`, `SoilNitrogenLevel`; `LiteratureModel`, `computesDiseaseSpreadRisk` | Enables spatial-temporal epidemiological risk prediction by combining remote-sensed vegetative density, micro-nutrient sensors, and literature infection dynamics. |
| **CQ-MM-09** | Given a farmer-submitted photo of irregular reddish-brown culm lesions at the waterline, does cross-referencing field water depth sensor data and extension management tables determine whether draining the paddy is recommended or if pesticide application is urgently required? | Relational | **Image + Sensor + Text** | `Image`, `localizesLesion`, `StemBase`; `SensorData`, `WaterDepth`; `ExtensionGuide`, `recommendsAction`, `WaterManagement` | Translates visual symptom severity and physical water sensor levels into actionable, non-chemical water control interventions. |
| **CQ-MM-10** | When image recognition models predict Rice Tungro Disease with an uncertainty score exceeding 0.40, can the KG leverage tabular vector trap counts (*Nephotettix virescens*), cultivar susceptibility tables (*tsb* loci), and recent rainfall data to compute a Bayesian posterior disease probability? | Complex-Inferential | **Image + Tabular + Genomic + Sensor** | `ImageModel`, `hasUncertaintyScore`; `PestTrapTable`, `VectorAbundance`; `CultivarTable`, `lacksResistanceLocus`; `BayesianReasoning`, `computesPosteriorProbability` | Demonstrates multimodal reasoning under visual diagnostic uncertainty, leveraging tabular surveillance and sensor evidence to refine decision confidence. |
| **CQ-MM-11** | Which genomic loci in regional rice cultivars are associated with reduced visual leaf necrosis scores under severe Sheath Blight pressure observed during high-temperature/high-humidity sensor regimes in multi-environment trial datasets? | Complex-Inferential | **Genomic/Tabular + Image + Sensor** | `CultivarTrial`, `recordsPhenotypicSES`, `NecrosisScore`; `SensorStream`, `documentsHeatHumidityStress`; `QTLMapping`, `identifiesLocus`, `ToleranceQTL` | Enables plant breeders to discover quantitative resistance traits by co-analyzing field phenotyping imagery, environmental stress logs, and genomic markers. |
| **CQ-MM-12** | A field photo captures grain discoloration ("dirty panicle"). Can the KG evaluate grain moisture sensor data, harvest date schedules from farm records, and literature on secondary mycotoxigenic fungi (*Fusarium* / *Curvularia*) to output grain post-harvest safety recommendations? | Complex-Inferential | **Image + Sensor + Tabular + Text** | `Image`, `showsPanicleDiscoloration`; `SensorRecord`, `GrainMoisture`; `FarmLog`, `HarvestDate`; `LiteratureText`, `evaluatesMycotoxinRisk`, `SafetyStandard` | Extends multimodal diagnostics past field boundaries into post-harvest grain quality and human/animal health safety preservation. |

---

## 3. Modality-Pair Cross-Coverage Matrix

This matrix provides traceability ensuring all bilateral and higher-order multimodal intersections are thoroughly tested and exercised by the competency questions.

| Modality Combination | Target Modality Intersections | Exercising Competency Question IDs | Coverage Status |
| :--- | :--- | :--- | :--- |
| **Text × Image** | Unstructured literature/keys + Visual symptoms | `CQ-MM-02`, `CQ-MM-04`, `CQ-MM-07`, `CQ-MM-09` | Comprehensive |
| **Image × Sensor** | Visual lesions/damage + Environmental telemetry | `CQ-MM-01`, `CQ-MM-02`, `CQ-MM-03`, `CQ-MM-06`, `CQ-MM-07`, `CQ-MM-08`, `CQ-MM-09`, `CQ-MM-10`, `CQ-MM-11`, `CQ-MM-12` | Exhaustive |
| **Sensor × Genomic / Tabular** | Microclimate + Variety traits / R-genes / Trials | `CQ-MM-01`, `CQ-MM-03`, `CQ-MM-05`, `CQ-MM-06`, `CQ-MM-07`, `CQ-MM-10`, `CQ-MM-11`, `CQ-MM-12` | Comprehensive |
| **Text × Genomic / Tabular** | Literature reports + Cultivar / Pathotype data | `CQ-MM-01`, `CQ-MM-04`, `CQ-MM-07`, `CQ-MM-12` | Robust |
| **Text × Sensor** | Agronomic/advisory guides + Microclimate logs | `CQ-MM-01`, `CQ-MM-02`, `CQ-MM-05`, `CQ-MM-07`, `CQ-MM-08`, `CQ-MM-09`, `CQ-MM-12` | Comprehensive |
| **Image × Genomic / Tabular** | Visual phenotypes + Cultivar genotypes / Trials | `CQ-MM-01`, `CQ-MM-03`, `CQ-MM-04`, `CQ-MM-06`, `CQ-MM-10`, `CQ-MM-11` | Robust |
| **Three-Way Fusion** | Combinations of any 3 distinct modalities | `CQ-MM-02`, `CQ-MM-03`, `CQ-MM-04`, `CQ-MM-05`, `CQ-MM-06`, `CQ-MM-08`, `CQ-MM-09`, `CQ-MM-11` | Exhaustive |
| **Four-Way Full Fusion** | **Text + Image + Sensor + Genomic/Tabular** | `CQ-MM-01`, `CQ-MM-07`, `CQ-MM-10`, `CQ-MM-12` | Fully Integrated |

---

## 4. Formal Scope Boundary Note (Ontology Scoping Statement)

### 4.1 In-Scope Capabilities
In accordance with the Grüninger & Fox and NeOn ontology engineering methodologies, the **Rice-MMKG** formally encompasses:
1. Taxonomic, morphological, and biological representations of major fungal, bacterial, and viral rice pathologies (*Magnaporthe oryzae*, *Xanthomonas oryzae* pv. *oryzae*, *Rhizoctonia solani*, Tungro RTBV/RTSV) and critical insect vectors/pests (*Nilaparvata lugens*, *Nephotettix virescens*, *Scirpophaga incertulas*).
2. Semantic annotations linking localized visual symptom phenotypes (lesion shape, color, organ distribution) from field imagery to formal ontology concepts (PPO, Plant Trait Ontology).
3. Continuous temporal environmental modeling linking sensor streams (temperature, RH%, leaf wetness duration, rainfall) to pathogen epidemiological incubation thresholds.
4. Genetic resistance architectures, including documented rice cultivar genotypes, named *R*-genes/QTLs, allelic dominance, and pathogen race-specific virulence/avirulence relationships.
5. Actionable agronomic and extension rules matching diagnosed stress events to legal chemical, biological, and cultural management recommendations.

### 4.2 Out-of-Scope Elements
The following domains are explicitly **out of scope**:
1. Deep mechanistic intracellular metabolic modeling (e.g., transcriptomic RNA-seq networks, enzymatic biochemical cascades).
2. End-to-end computer vision neural network architecture and feature weight storage (the KG stores image metadata, bounding annotations, and extracted semantic features, not neural model weights).
3. Farm machinery robotics control, GPS guidance, and automated tractor steering logic.
4. Real-time agricultural commodity market price trading and macroeconomic supply-chain economics.

### 4.3 Data Feasibility and Implementation Risk Assessment
- **High Feasibility**: Questions relying on Text (`CQ-TXT-01` to `06`), Image diagnostics (`CQ-IMG-01` to `06`), and Cultivar lookup (`CQ-GEN-01` to `03`) are immediately operationalizable using open datasets (IRRI Rice Knowledge Bank, Kaggle/Mendeley rice disease image sets, and Gramene/Oryzabase).
- **Medium Feasibility / Implementation Watchpoint**: Fully automated resolution of `CQ-MM-01`, `CQ-MM-07`, and `CQ-MM-10` requires tight spatial and temporal alignment between IoT sensor logs and timestamped field photos. In field scenarios lacking in-situ canopy IoT nodes, microclimate conditions may need to be interpolated from gridded meteorological reanalysis datasets (e.g., ERA5-Land or NASA POWER) rather than physical in-situ sensors.
