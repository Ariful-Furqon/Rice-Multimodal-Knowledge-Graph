# Ontology Requirements Specification: Competency Questions for a Rice Pest and Disease Multimodal Knowledge Graph (Rice-MMKG)

## 1. System Purpose and Scope Specification

The **Rice-MMKG** is designed as a domain-specific, multimodal semantic knowledge graph engineered to empower plant pathology researchers, agricultural extension specialists, and automated precision-agriculture IoT systems with multi-source diagnostic reasoning, risk forecasting, and resistant cultivar selection capabilities. The system semantically unifies unstructured scientific/extension literature (**Text**), ground-level and micro-phenotypic lesion photography (**Image**), in-situ agrometeorological IoT time-series streams (**Sensor/Environmental**), and structured cultivar genotype/phenotype resistance profiles (**Genomic/Tabular**). Geographically focused on tropical lowland and irrigated rice agroecosystems (representative of Southeast and South Asian ecologies such as Indonesia, the Philippines, India, and Vietnam), the knowledge graph provides formalized graph structures supporting formal semantic queries (e.g., SPARQL, multimodal graph embeddings) across five major pathosystems: *Magnaporthe oryzae* (Rice Blast), *Xanthomonas oryzae* pv. *oryzae* (Bacterial Leaf Blight), *Rhizoctonia solani* (Sheath Blight), Rice Tungro Spherical/Bacilliform Virus (RTSV/RTBV vector-borne complex), and *Nilaparvata lugens* (Brown Planthopper).

To ensure maximal interoperability and standard semantic web conformance, the entity classes and relation topologies align directly with international upper and domain ontologies: **AGROVOC**, **Crop Ontology (CO)**, **Plant Trait Ontology (TO)**, **Plant Phenotype Ontology (PPO)**, **Infectious Disease Ontology (IDO)**, and the **W3C Semantic Sensor Network / SOSA (Sensor, Observation, Sample, and Actuation)** ontology.

---

## 2. Itemized Competency Questions (CQs)

### 2.1 Category A: Text-Grounded Competency Questions
*Focus: Verified pathogen etiology, epidemiological cycles, chemical/cultural control protocols, and textual diagnostic rules derived from extension reports and scientific publications.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations Implied | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-TXT-01** | What is the primary causal pathogen, taxonomic classification, and infectious spore type of Rice Blast disease? | Simple | `Disease`, `causedByPathogen`, `PathogenTaxon`, `producesSporeType` | Validates fundamental core taxonomy and pathogen entity linking from literature baselines. |
| **CQ-TXT-02** | What are the recommended chemical active ingredients, spray intervals, and pre-harvest intervals for managing Bacterial Leaf Blight caused by *Xanthomonas oryzae* pv. *oryzae*? | Relational | `Disease`, `hasRecommendedControl`, `PesticideActiveIngredient`, `hasSprayInterval`, `hasPreHarvestInterval` | Formalizes agronomic intervention pathways documented in plant protection compendia. |
| **CQ-TXT-03** | Which alternative wild and weed host plant species serve as reservoirs for Rice Tungro Bacilliform Virus (RTBV) during fallow periods? | Relational | `Pathogen`, `hasAlternativeHost`, `WeedSpecies`, `persistsDuringGrowthStage` | Enables semantic tracing of inter-season disease carryover and reservoir vectors. |
| **CQ-TXT-04** | Which cultural management practices (e.g., nitrogen split-application, water drainage) suppress *Rhizoctonia solani* (Sheath Blight) canopy microclimate spread according to agronomy guidelines? | Relational | `Disease`, `mitigatedByPractice`, `CulturalPractice`, `targetsMicroclimateFactor` | Supports non-chemical integrated pest management (IPM) query pipelines. |
| **CQ-TXT-05** | According to published literature, how do excessive basal nitrogen fertilizer rates correlate with increased tissue susceptibility to *Magnaporthe oryzae* leaf and neck blast? | Complex-Inferential | `AgronomicInput`, `correlatedWithSusceptibility`, `PlantTissue`, `Disease`, `hasLiteratureEvidence` | Enables deductive reasoning over biochemical and physiological predisposition factors. |
| **CQ-TXT-06** | What are the sequential developmental instars and diagnostic morphological stages of the vector *Nilaparvata lugens* (Brown Planthopper) documented in entomological literature? | Simple | `InsectPest`, `hasLifeStage`, `DevelopmentalInstar`, `hasMorphologicalDescription` | Encodes ontologies of entomological life cycles needed for scouting protocol verification. |

---

### 2.2 Category B: Image-Grounded Competency Questions
*Focus: Visual feature grounding, lesion morphometry, anatomical tissue localization, visual symptom progression, and image-based diagnostic verification.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations Implied | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-IMG-01** | Which plant anatomical organs (e.g., leaf blade, leaf sheath, collar, panicle neck, spikelet) exhibit visible diagnostic lesion features in an annotated symptom image? | Simple | `Image`, `depictsOrgan`, `PlantAnatomicalEntity`, `exhibitsLesion`, `LesionPhenotype` | Establishes spatial anchoring of visual bounding boxes and masks to standardized plant anatomy. |
| **CQ-IMG-02** | What visual color distributions (e.g., grayish-white center with brown-reddish necrotic margins) and geometric lesion geometries (spindle-shaped vs. irregular wavy margins) distinguish Rice Blast from Bacterial Leaf Blight in field photos? | Relational | `Image`, `hasVisualFeature`, `ColorProfile`, `LesionGeometry`, `differentiatesDisease` | Enables direct mapping of computer vision feature maps to standardized phenotypic descriptors. |
| **CQ-IMG-03** | Does the leaf image exhibit characteristic ragged, serrated leaf margins or yellow-orange discoloration indicative of Tungro virus versus nutritional chlorosis? | Relational | `Image`, `manifestsSymptomPattern`, `VisualDiscoloration`, `indicatesPathology` | Supports disambiguation between viral symptom expressions and abiotic nutrient deficiencies. |
| **CQ-IMG-04** | What is the estimated visual severity grade (e.g., Standard Evaluation System 0–9 score) calculated from the ratio of necrotic lesion pixel area to total healthy leaf surface area in an input image? | Complex-Inferential | `Image`, `hasSegmentedMask`, `LesionSurfaceRatio`, `hasSeverityScaleRating` | Maps segmented visual outputs to international plant pathology phenotypic scoring scales. |
| **CQ-IMG-05** | Does the field-level canopy image exhibit circular patches of lodging and severe desiccation ("hopper burn") characteristic of high-density *Nilaparvata lugens* infestation? | Relational | `CanopyImage`, `exhibitsCanopyDamagePattern`, `DamageSymptom`, `attributedToPest` | Ground-truths macro-scale canopy field images to specific entomological damage archetypes. |
| **CQ-IMG-06** | In a close-up macro photograph of a rice stem base, are sclerotia bodies of *Rhizoctonia solani* present and visible on the outer sheath surface? | Simple | `MacroImage`, `detectsPhysicalSign`, `FungalSclerotium`, `locatedOnOrgan` | Captures physical pathogen sign detection distinct from host tissue reaction symptoms. |

---

### 2.3 Category C: Sensor- and Environmental-Grounded Competency Questions
*Focus: Micrometeorological time-series, soil biophysical properties, spore germination thresholds, IoT thermal/hygrometric aggregations, and canopy microclimate dynamics.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations Implied | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-ENV-01** | What were the mean, minimum, and maximum ambient temperature (°C) and relative humidity (%) registered by an in-situ IoT node over the preceding 72 hours? | Simple | `SensorNode`, `observesProperty`, `AirTemperature`, `RelativeHumidity`, `hasTemporalWindow` | Verifies basic SOSA/SSN sensor observation ingestion and aggregation semantics. |
| **CQ-ENV-02** | Did the cumulative continuous leaf wetness duration (LWD) exceed 14 consecutive hours while the canopy microclimate temperature remained between 24°C and 28°C? | Relational | `WeatherObservation`, `hasLeafWetnessDuration`, `AirTemperature`, `satisfiesPathogenInfectionThreshold` | Encodes physiological environmental gating rules necessary for fungal spore germination. |
| **CQ-ENV-03** | How many consecutive days within an observation window recorded daily rainfall exceeding 15 mm accompanied by wind gusts greater than 25 km/h? | Relational | `PrecipitationObservation`, `WindSpeedObservation`, `consecutiveDurationDays`, `fostersBacterialDissemination` | Detects physical weather conditions that actively spread splash-dispersed bacterial pathogens. |
| **CQ-ENV-04** | What is the computed hydrothermal disease pressure index for *Rhizoctonia solani* based on moving-window average canopy relative humidity (>85%) and temperature (28–32°C)? | Complex-Inferential | `MicroclimateStream`, `aggregatedMetric`, `HydrothermalIndex`, `computesDiseaseRisk` | Formalizes derived agroclimatic risk indices computed directly over live sensor streams. |
| **CQ-ENV-05** | How do soil moisture tension (kPa) and floodwater depth fluctuations over a 14-day drying cycle correlate with increased emergence of micro-nymphs of *Nilaparvata lugens*? | Complex-Inferential | `SoilMoistureObservation`, `WaterDepthObservation`, `temporalCorrelation`, `PestPopulationDynamic` | Semanticizes soil and hydrological sensors driving pest emergence dynamics. |

---

### 2.4 Category D: Genomic- and Tabular-Grounded Competency Questions
*Focus: Cultivar classifications, resistance gene (R-gene) loci, functional markers, quantitative trait loci (QTLs), germplasm pedigree, and agronomic yield metadata.*

| ID | Natural-Language Question | Complexity | Key Entities & Relations Implied | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **CQ-GEN-01** | Which major blast resistance genes (e.g., *Pita*, *Piz-t*, *Pib*, *Pi9*, *Pi54*) are officially introgressed into rice cultivar 'Ciherang' or 'IR64'? | Simple | `RiceCultivar`, `carriesResistanceGene`, `ResistanceGeneLocus`, `targetsPathogen` | Queries standardized cultivar-to-gene genomic annotations from breeding databases. |
| **CQ-GEN-02** | Which registered rice cultivars in Southeast Asia possess pyramided dual resistance containing both *Xa21* and *xa13* against *Xanthomonas oryzae*? | Relational | `RiceCultivar`, `hasPyramidedGenes`, `ResistanceGene`, `hasTargetPathogenStrain` | Allows breeders and extension agents to retrieve multi-gene durable cultivars. |
| **CQ-GEN-03** | Which brown planthopper biotype resistance genes (e.g., *Bph1*, *Bph2*, *Bph14*, *Bph18*) have documented breakdown or virulence adaptation by BPH Biotype 3? | Relational | `ResistanceGene`, `overcomeByPestBiotype`, `InsectBiotype`, `hasVirulenceStatus` | Tracks resistance breakdown across dynamic pest biotypes in tabular registries. |
| **CQ-GEN-04** | For a specific elite cultivar, what is the documented baseline grain yield potential (t/ha), maturation duration (days), and lodging resistance class under standard agronomic trials? | Simple | `RiceCultivar`, `hasPotentialYield`, `hasCropDuration`, `hasAgronomicTrait` | Integrates non-pathology agronomic performance metrics necessary for trade-off evaluations. |
| **CQ-GEN-05** | Which cultivars share ancestral parentage containing the durable sheath blight tolerance quantitative trait locus *qSBR11-1* within their documented breeding pedigree? | Complex-Inferential | `RiceCultivar`, `hasPedigreeAncestor`, `carriesQTL`, `confersQuantitativeResistance` | Enables recursive traversal across pedigree ancestry graphs to identify QTL inheritance lines. |

---

### 2.5 Category E: Cross-Modal / Multimodal Fusion Competency Questions
*Focus: Joint inference requiring non-trivial synthesis of Text, Image, Sensor, and Genomic modalities in unified query graphs.*

| ID | Natural-Language Question | Modalities Fused | Complexity | Key Entities & Relations Implied | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CQ-MM-01** | Given an uploaded leaf photograph exhibiting necrotic spindle lesions with chlorotic halos, and IoT sensor streams indicating 16 hours of continuous leaf wetness at 26°C over the past 48 hours, what is the confirmed disease diagnosis and the pathogen virulence probability? | **Image × Sensor × Text** | Relational | `Image`, `hasVisualLesion`, `MicroclimateStream`, `satisfiesEpidemicRule`, `confirmedDiseaseDiagnosis`, `hasConfidenceScore` | Fuses computer vision symptom detection with ambient micrometeorological infection models for verified field diagnosis. |
| **CQ-MM-02** | For a farmer field planting cultivar 'Inpari 32' (carrying *Xa21*), where automated field cameras detect progressive leaf-edge yellowing, but local weather sensors record only 40% RH and zero rain, does literature describe non-bacterial physiological leaf scorch or an aberrant *Xanthomonas* pathotype breakdown? | **Image × Sensor × Genomic × Text** | Complex-Inferential | `Image`, `RiceCultivar`, `carriesGene`, `WeatherObservation`, `inconsistentWithKnownEpidemiology`, `infersDiagnosticHypothesis` | Executes complete 4-way cross-modal contradiction resolution between visual signs, host genetics, weather, and literature. |
| **CQ-MM-03** | Given an aerial canopy drone image showing localized yellowing patches, combined with soil moisture sensors showing alternate wetting and drying, which pest or viral vector is suspected, and what extension scouting manual protocol should be deployed? | **Image × Sensor × Text** | Relational | `DroneCanopyImage`, `detectsPatchPattern`, `SoilSensorStream`, `indicatesVectorHabitation`, `hasExtensionProtocol` | Connects macro-imaging with hydrological dynamics to trigger authoritative, text-grounded extension actions. |
| **CQ-MM-04** | Based on verified image detections of neck blast in a district, combined with forecast meteorological conditions (continuous drizzle, overcast solar radiation, 24°C), which local cultivars in current production lack protective *Pi-* genes and require emergency fungicidal intervention? | **Image × Sensor × Genomic × Text** | Complex-Inferential | `ImageObservation`, `RegionalWeatherForecast`, `RiceCultivar`, `lacksResistanceGene`, `requiresEmergencyIntervention` | Enables predictive, precision-scale epidemiology by intersecting visual outbreak locations, weather forecasts, and cultivar vulnerability maps. |
| **CQ-MM-05** | Given close-up stem base photos confirming sheath blight lesion progression up to the flag leaf sheath, and historical sensor readings of 92% RH within the dense canopy, what is the estimated yield loss percentage predicted by published agronomic crop loss models? | **Image × Sensor × Text × Tabular** | Complex-Inferential | `Image`, `measuresLesionHeightFraction`, `CanopySensorData`, `appliesYieldLossModel`, `predictsEstimatedYieldLoss` | Quantifies economic impact by linking image-derived vertical lesion heights with canopy microclimate and empirical loss formulas. |
| **CQ-MM-06** | A field camera detects high-density planthopper clustering on stem bases in a region where sensor temperature averaged 29°C; cross-referencing regional cultivar registries, which nearby standing crops carry *Bph14* or *Bph18* to prevent catastrophic hopper burn? | **Image × Sensor × Genomic** | Relational | `Image`, `detectsInsectDensity`, `SensorStream`, `RiceCultivar`, `possessesBiotypeResistance` | Guides regional containment strategies by matching real-time visual insect pressure and temperatures with resistant cultivar deployment. |
| **CQ-MM-07** | Which scientific journal publications describe field trial validations where image-based severity classifications of Bacterial Leaf Blight under tropical monsoonal sensor regimes matched quantitative PCR pathogen titer measurements? | **Text × Image × Sensor × Genomic** | Complex-Inferential | `ScientificPublication`, `validatesImageMethod`, `underSensorEnvironment`, `correlatesWithMolecularTiter` | Serves meta-research queries evaluating the analytical validity of computer vision phenotyping against molecular ground truth. |
| **CQ-MM-08** | Given an ambiguous lesion image where visual classification confidence is tied between Rice Blast and Brown Spot, how can historical 7-day ambient temperature/humidity sensor series and cultivar resistance pedigree break the diagnostic tie? | **Image × Sensor × Genomic × Text** | Complex-Inferential | `Image`, `hasDiagnosticAmbiguity`, `SensorHistory`, `CultivarGenotype`, `resolvesDisambiguation` | Implements Bayesian or rules-based semantic tie-breaking when visual modalities alone lack sufficient discriminative power. |
| **CQ-MM-09** | For field image archives showing confirmed *Rhizoctonia solani* outbreaks, what were the exact microclimate sensor parameter distributions (box-plot quantiles of RH and temp) across all cultivars possessing partial quantitative sheath blight resistance? | **Image × Sensor × Genomic** | Complex-Inferential | `ImageArchive`, `hasConfirmedDiseaseEvent`, `SensorAggregateDistribution`, `CultivarQTLProfile` | Powers empirical agroclimatic envelope extraction for partially resistant breeding lines across multi-year trials. |
| **CQ-MM-10** | If a drone multispectral image indicates red-edge vegetative stress in an area planted with 'IR64-Sub1', and water level sensors confirm 10 days of complete submergence, what secondary fungal pathogens are documented in extension literature to infect the post-submergence weakened crop? | **Image × Sensor × Genomic × Text** | Complex-Inferential | `MultispectralImage`, `WaterSubmergenceSensor`, `CultivarSubmergenceGene`, `hasSecondaryPathogenRisk` | Evaluates abiotic-biotic disease interactions combining remote sensing, hydrological sensors, stress tolerance genetics, and agronomy manuals. |
| **CQ-MM-11** | Given a close-up leaf photograph displaying marginal bacterial leaf streak lesions, what temperature and relative humidity thresholds retrieved from literature must be verified against current IoT sensor data to issue an automatic regional disease forecast bulletin? | **Image × Text × Sensor** | Relational | `Image`, `identifiesDiseaseSymptom`, `LiteratureRule`, `hasEpidemiologicalThreshold`, `SensorObservation`, `triggersBulletin` | Automates extension early-warning advisory generation by linking visual detection to environmental rule verification. |
| **CQ-MM-12** | Which recommended bio-fungicides or bio-control agents (e.g., *Bacillus subtilis*, *Trichoderma harzianum*) documented in extension texts remain biocontrol-effective within the temperature and moisture ranges recorded by field IoT sensors during a blast outbreak detected via image scouting? | **Text × Sensor × Image** | Complex-Inferential | `ImageSymptom`, `confirmsActiveOutbreak`, `BiocontrolAgent`, `hasEfficacyEnvironmentalWindow`, `CurrentSensorReadings` | Recommends environmentally viable biological controls adapted to current real-time microclimate conditions. |

---

## 3. Modality-Pair Coverage and Traceability Matrix

The matrix below maps each bilateral and multilateral modality intersection to the corresponding Competency Question identifiers. This mapping verifies that no unimodal silos exist and guarantees comprehensive cross-modal integration across the ontology graph schema.

| Modality Combination | Covered Competency Questions | Cross-Modal Interoperability Justification |
| :--- | :--- | :--- |
| **Text × Image** | CQ-MM-01, CQ-MM-02, CQ-MM-03, CQ-MM-04, CQ-MM-05, CQ-MM-07, CQ-MM-08, CQ-MM-10, CQ-MM-11, CQ-MM-12 | Grounding visual lesion bounding boxes and segmentations to formal symptom vocabularies and IPM control handbooks. |
| **Text × Sensor** | CQ-MM-01, CQ-MM-02, CQ-MM-03, CQ-MM-04, CQ-MM-05, CQ-MM-07, CQ-MM-08, CQ-MM-10, CQ-MM-11, CQ-MM-12 | Linking empirical epidemiological infection threshold rules (from publications) to continuous SOSA sensor observation streams. |
| **Text × Genomic** | CQ-MM-02, CQ-MM-04, CQ-MM-07, CQ-MM-08, CQ-MM-10 | Mapping literature-reported pathogen physiological races/pathotypes against known cultivar R-gene resistance catalogs. |
| **Image × Sensor** | CQ-MM-01, CQ-MM-02, CQ-MM-03, CQ-MM-04, CQ-MM-05, CQ-MM-06, CQ-MM-07, CQ-MM-08, CQ-MM-09, CQ-MM-10, CQ-MM-11, CQ-MM-12 | Correlating visible phenotypic symptom manifestation and spatial canopy damage with real-time micrometeorological stress history. |
| **Image × Genomic** | CQ-MM-02, CQ-MM-04, CQ-MM-06, CQ-MM-07, CQ-MM-08, CQ-MM-09, CQ-MM-10 | Associating visual lesion phenotype dimensions, color metrics, and necrosis rates directly with host cultivar resistance genotypes. |
| **Sensor × Genomic** | CQ-MM-02, CQ-MM-04, CQ-MM-06, CQ-MM-07, CQ-MM-08, CQ-MM-09, CQ-MM-10 | Analyzing microclimatic trigger conditions leading to resistance breakdown or field performance limits of specific gene combinations. |
| **Three-Way Combinations** | | |
| *Image × Sensor × Text* | CQ-MM-01, CQ-MM-03, CQ-MM-11, CQ-MM-12 | Automated field diagnostics combining visual phenotypes, microclimate validation, and text-based extension intervention rules. |
| *Image × Sensor × Genomic* | CQ-MM-06, CQ-MM-09 | Multi-environment phenotype scoring linking canopy imagery, IoT sensor baselines, and cultivar genotype allocations. |
| *Image × Text × Genomic* | CQ-MM-08 | Visual lesion disambiguation guided by host cultivar resistance lineage and literature diagnostic keys. |
| **Four-Way Multimodal Core** | | |
| *Text × Image × Sensor × Genomic* | CQ-MM-02, CQ-MM-04, CQ-MM-05, CQ-MM-07, CQ-MM-08, CQ-MM-10 | Holistically integrated agroecological reasoning: resolving visual disease symptoms in specific cultivars under live weather regimes to trigger literature-grounded agronomic actions. |

---

## 4. Ontology Scope Boundary and Feasibility Analysis

### 4.1 In-Scope Boundary Statement
The Rice-MMKG boundary encompasses:
1. Taxonomic, etiological, and management descriptions of the five target rice pathogens and pests (*Magnaporthe oryzae*, *Xanthomonas oryzae* pv. *oryzae*, *Rhizoctonia solani*, Tungro RTSV/RTBV, *Nilaparvata lugens*);
2. Image-derived visual phenotypes including organ localization, segmented lesion geometry, RGB color distributions, and SES standard damage scoring;
3. Spatiotemporally indexed agrometeorological time series (air temperature, relative humidity, rainfall, leaf wetness duration, canopy microclimate, floodwater level) captured by IoT nodes and standardized via W3C SOSA/SSN patterns;
4. Cultivar germplasm registries documenting major introgressed resistance genes (*R-genes*), quantitative trait loci (*QTLs*), biotype breakdown history, parentage pedigrees, and tabular agronomic traits (yield potential, growth duration).

### 4.2 Out-of-Scope Boundary Statement
Explicitly excluded from the Rice-MMKG boundary are:
1. Whole-genome sequence (WGS) FASTA/BAM nucleotide alignment data, gene expression transcriptomics, and metabolomic mass-spectrometry arrays (these reside in external repositories such as NCBI GenBank or Gramene, to which the KG maintains only external URI cross-references);
2. Upstream farm machinery telemetry, logistics, post-harvest supply chain tracking, market grain price volatility, and macro-financial crop insurance policy underwriting;
3. General crop diseases outside *Oryza sativa* (e.g., maize rust, wheat blast), except where wild grass species function strictly as certified alternative biological reservoirs for the in-scope rice pathogens.

### 4.3 Data Feasibility and Engineering Risk Assessment
- **High Feasibility:** Text-based entity extraction, cultivar genomic gene lists, standard RGB lesion photographic classifications, and standard macro-weather sensor streams are robustly supported by mature public repositories (e.g., IRRI Germplasm Bank, Crop Ontology, Kaggle Rice Leaf Disease datasets).
- **Feasibility Caveats / Data Sparsity Flags:**
  - *Leaf Wetness Duration (LWD)* sensors (referenced in **CQ-ENV-02** and **CQ-MM-01**) are frequently absent in baseline agricultural IoT deployments; ontologists must implement synthetic LWD proxy estimations derived from relative humidity (>90%) and dew point calculations.
  - Continuous microclimate canopy-layer sensors (**CQ-MM-05**) differ significantly from regional ambient weather stations; the KG must model sensor installation height and exposure metadata in SOSA to prevent spurious disease trigger calculations.
  - Molecular pathogen titer correlations (**CQ-MM-07**) rely on specialized research trial literature where qPCR data are explicitly co-published with field imagery; this CQ represents a specialized scientific evaluation query rather than a ubiquitous extension production query.
