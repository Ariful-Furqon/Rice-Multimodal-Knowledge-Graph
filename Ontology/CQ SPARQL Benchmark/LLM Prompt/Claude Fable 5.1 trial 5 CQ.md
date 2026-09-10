# Competency Questions for a Multimodal Knowledge Graph on Rice Pests and Diseases

*Ontology Requirements Specification — Competency Question Set (v1.0)*

---

## 0. Assumptions Adopted

All `[BRACKETED]` input fields in the source prompt were left unfilled; the following defaults were therefore applied and are **explicitly marked as assumptions** to be revised by the project team.

| Input field | Assumption used |
|---|---|
| Pests/diseases in scope | **Diseases:** rice blast (*Magnaporthe oryzae*), bacterial leaf blight/BLB (*Xanthomonas oryzae* pv. *oryzae*), sheath blight (*Rhizoctonia solani*), brown spot (*Bipolaris oryzae*), rice tungro disease (RTBV + RTSV). **Pests:** brown planthopper/BPH (*Nilaparvata lugens*), green leafhopper/GLH (*Nephotettix virescens*, tungro vector), yellow stem borer (*Scirpophaga incertulas*), rice leaffolder (*Cnaphalocrocis medinalis*), rice bug (*Leptocorisa oratorius*). |
| Primary end users | Plant pathology researchers; agricultural extension officers; smart-farming/IoT decision-support developers. |
| Geographic scope | Indonesia / Southeast Asian tropical lowland irrigated rice (wet- and dry-season cropping). |
| Text sources | IRRI Rice Knowledge Bank, peer-reviewed literature (CAB Abstracts / Scopus), national and provincial extension bulletins and pest surveillance reports. |
| Image sources | Public rice-leaf disease image datasets (e.g., Kaggle rice leaf disease, Mendeley rice disease collections) plus project field photographs with plot ID, GPS, and capture timestamp; expert labels and, where available, bounding-box annotations and IRRI Standard Evaluation System (SES) severity scores. |
| Sensor sources | Plot-level IoT weather/soil stations logging air temperature, relative humidity (RH), rainfall, wind speed, leaf wetness, soil moisture, and soil pH at ≤1-hour intervals. |
| Genomic/tabular sources | National variety release catalogues (e.g., Indonesian Inpari series, IR64, Ciherang, Mekongga), IRRI resistance-gene tables (e.g., *Xa4, xa5, xa13, Xa21, Xa23*; *Pi9, Pi-ta, Pib, Piz-t, Pi54*; *Bph3, Bph14, Bph18, Bph26, Bph32*), marker–gene linkage tables, and multi-location yield-trial data. |
| Target number of CQs | 36 (within the 30–40 default). |
| Existing ontology alignment | None yet; alignment opportunities are flagged inline (AGROVOC, Crop Ontology, Plant Trait Ontology (TO), Plant Phenotype Ontology (PPO), NCBI Taxonomy, EPPO codes, SOSA/SSN for sensor observations, Infectious Disease Ontology (IDO) patterns for host–pathogen–vector relations, and PROV-O for annotation provenance). |
| Previously drafted CQs | None supplied. |

---

## 1. Purpose and Scope Restatement

The knowledge graph (KG) is intended to support early diagnosis and management decision-making for major pests and diseases of tropical lowland rice by semantically integrating four modalities: textual domain knowledge (literature, extension bulletins, surveillance reports), field and close-up images of symptoms and damage, plot-level environmental sensor time series, and structured variety/genotype/resistance-gene and agronomic tables. Its primary users are plant pathology researchers, extension officers, and developers of IoT-based decision-support systems, with the Indonesian/Southeast Asian irrigated lowland rice system as the reference agroecology. The competency questions below define what the KG must be able to answer, and thereby drive ontology design, cross-modal alignment requirements, and SPARQL-based evaluation.

---

## 2. Competency Questions

Distribution: Text-only 6 (17%), Image-only 6 (17%), Sensor-only 5 (14%), Genomic/Tabular-only 5 (14%), Cross-modal/Fusion 14 (39%).

### 2a. Text-grounded CQs

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal agent of bacterial leaf blight, and what are its genus, species, and pathovar? | Simple | Disease, hasCausalAgent, Pathogen, hasTaxonRank, Taxon (align: NCBI Taxonomy, AGROVOC, EPPO code) | Establishes the core Disease–Pathogen backbone on which all diagnostic reasoning depends. |
| CQ-TXT-02 | Which insect species act as vectors of rice tungro disease, and which of the two tungro viruses (RTBV, RTSV) does each transmit? | Simple | Disease, causedBy, Virus, transmittedBy, InsectVector (align: IDO host–vector pattern) | Vector-borne diseases require a Pest–Disease link distinct from direct pathogenicity; this tests that modelling choice. |
| CQ-TXT-03 | Which management practices (cultural, biological, chemical) are recommended in extension bulletins for brown planthopper, and at which crop growth stage is each practice applied? | Relational | Pest, controlledBy, ManagementPractice, hasPracticeType, appliedAtStage, GrowthStage, recommendedIn, Document (align: Crop Ontology growth stages) | Extension officers need stage-specific, source-attributed recommendations rather than generic advice. |
| CQ-TXT-04 | Which pairs of diseases are described in the literature with at least one shared symptom term (e.g., "water-soaked lesion", "leaf yellowing"), making them candidates for field misdiagnosis? | Relational | Disease, hasSymptom, Symptom, hasSymptomTerm, describedIn, Document (align: PPO/TO) | Identifies confusable diseases, informing both image-annotation guidelines and differential-diagnosis logic. |
| CQ-TXT-05 | For a given district, which diseases and pests were reported in surveillance bulletins in each of the last five wet seasons, and how has the reported incidence (% area affected) trended over time? | Complex-Inferential | SurveillanceReport, reportsOccurrence, Occurrence, ofDisease/ofPest, hasLocation, AdministrativeRegion, hasSeason, incidenceValue | Temporal aggregation of textual reports gives the historical baseline against which sensor-derived risk is judged. |
| CQ-TXT-06 | For a given insecticide active ingredient (e.g., imidacloprid), which target pests have documented field resistance, in which countries, and from which year onward? | Complex-Inferential | ActiveIngredient, targetsPest, Pest, hasResistanceReport, ResistanceReport, reportedIn, Country, reportYear | Prevents the KG from recommending controls that literature shows to be failing regionally. |

### 2b. Image-grounded CQs

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Which images depict diamond- or spindle-shaped lesions with grey centres and brown margins on rice leaf blades? | Simple | Image, depicts, VisualSymptom, hasLesionShape, hasCentreColour, hasMarginColour, locatedOn, PlantOrgan | Tests that visual symptom attributes are modelled as queryable properties, not just free-text captions. |
| CQ-IMG-02 | Which images show healthy rice plants at the tillering stage that can serve as baselines for comparison? | Simple | Image, depicts, PlantSample, hasHealthStatus, atGrowthStage, GrowthStage | Healthy baselines are essential for both human comparison and classifier training-set retrieval. |
| CQ-IMG-03 | Which images showing "hopperburn" (circular patches of yellowing and drying plants) are attributed to brown planthopper, who annotated them, and at what growth stage was the crop? | Relational | Image, showsDamage, DamageType, causedBy, Pest, hasAnnotation, Annotation, annotatedBy, Agent, atGrowthStage (align: PROV-O) | Damage-type images must carry provenance so that expert vs. non-expert labels can be weighted. |
| CQ-IMG-04 | Among images labelled sheath blight, on which plant organs (leaf sheath, leaf blade, panicle) are lesions annotated, and what proportion of images show lesions at or above the flag leaf? | Relational | Image, hasAnnotation, BoundingBox, annotatesSymptom, locatedOn, PlantOrgan, hasCanopyPosition | Vertical lesion progression is the key severity criterion for sheath blight; the KG must expose it. |
| CQ-IMG-05 | Which sequences of images from the same plot show the same diagnosed disease at monotonically increasing SES severity scores across successive capture dates? | Complex-Inferential | Image, capturedAt, Plot, captureTimestamp, diagnosedAs, Disease, hasSeverityScore, SeverityScale | Enables temporal progression analysis purely from the image modality. |
| CQ-IMG-06 | Which images have conflicting labels between expert annotation and automated classifier prediction, and which pairs of diseases are most frequently confused? | Complex-Inferential | Image, hasExpertLabel, hasPredictedLabel, predictedBy, Classifier, hasConfidence, Disease | Supports KG-driven error analysis and active-learning loops for image classifiers. |

### 2c. Sensor/Environmental-grounded CQs

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What were the mean daily air temperature and relative humidity recorded by the sensor station serving plot P on date D? | Simple | SensorStation, serves, Plot, madeObservation, Observation, observedProperty, hasResult, resultTime (align: SOSA/SSN) | Baseline retrieval of atomic observations; validates the sensor schema. |
| CQ-ENV-02 | Which plots experienced at least three consecutive days with RH above 90% and mean temperature between 24 °C and 28 °C within the last 14 days? | Relational | Plot, hasSensorStation, Observation, temperature, relativeHumidity, dailyAggregate, consecutiveDayWindow | Tests windowed threshold queries, the building block of any environmental risk rule. |
| CQ-ENV-03 | Which sensor stations recorded cumulative rainfall above 100 mm together with wind speeds exceeding 5 m/s within any 7-day window this season? | Relational | SensorStation, Observation, rainfall, windSpeed, cumulativeAggregate, Season | Rain-plus-wind is the dispersal condition for water-borne bacterial pathogens; must be queryable independently of any disease label. |
| CQ-ENV-04 | For each plot, how many leaf-wetness hours accumulated between the booting and heading stages, and which plots rank in the top 10%? | Complex-Inferential | Plot, hasCropCalendar, GrowthStageInterval, Observation, leafWetnessDuration, aggregation, ranking | Growth-stage-aligned aggregation of a physiologically critical variable. |
| CQ-ENV-05 | Which sensor stations show data-quality anomalies (stuck values for >12 h, gaps >6 h, out-of-range readings) during the current season that should be excluded before risk inference? | Complex-Inferential | SensorStation, Observation, hasQualityFlag, DataGap, anomalyType | Environmental inference is only as trustworthy as the sensor stream; quality metadata must be first-class. |

### 2d. Genomic/Tabular-grounded CQs

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which resistance genes does the near-isogenic line IRBB21 carry, and against which pathogen races or strains are they effective? | Simple | Variety, carriesGene, ResistanceGene, confersResistanceTo, PathogenRace, ofPathogen | Core Variety–Gene–Race triple needed for any resistance recommendation. |
| CQ-GEN-02 | Which rice varieties released in Indonesia after 2015 are rated resistant or moderately resistant to brown planthopper biotype 3? | Simple | Variety, releasedIn, Country, releaseYear, hasResistanceRating, ResistanceRating, againstPest, PestBiotype | Extension officers need locally released, currently recommended options. |
| CQ-GEN-03 | Which varieties pyramid two or more BLB resistance genes (e.g., *Xa4* + *xa5* + *Xa21*), and what mean yield did they achieve in multi-location trials? | Relational | Variety, carriesGene, ResistanceGene, evaluatedIn, YieldTrial, meanYield, trialLocation | Links resistance stacking to agronomic performance, a common breeding trade-off question. |
| CQ-GEN-04 | Which resistance genes are tagged by a molecular marker (SSR/SNP), on which chromosome are they located, and which varieties are marker-confirmed carriers? | Relational | ResistanceGene, hasMarker, MolecularMarker, locatedOnChromosome, Chromosome, Variety, markerConfirmed | Distinguishes marker-verified from pedigree-inferred resistance claims. |
| CQ-GEN-05 | Among varieties with no known blast resistance gene, which combine the highest trial yield with the shortest maturity duration, ranked to prioritise them for introgression breeding? | Complex-Inferential | Variety, carriesGene (absence), maturityDays, meanYield, ranking, multi-criteria comparison | Requires negation and multi-criteria ranking over tabular data. |

### 2e. Cross-modal / Fusion CQs

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 *(Text×Image)* | Which extension bulletin describes the damage type shown in a given image (e.g., "deadheart" caused by yellow stem borer), and what management action does it recommend? | Simple | Image, showsDamage, DamageType, describedIn, Document, recommends, ManagementPractice | The minimal image-to-advice pathway an extension app must support. |
| CQ-MM-02 *(Text×Image)* | Given an image annotated with "yellow-orange discolouration from the leaf tip" and "stunting", which diseases in the literature list these symptoms, and which other confirmed-case images share the same symptom terms? | Relational | Image, depicts, VisualSymptom, alignedTo, Symptom, symptomOf, Disease, describedIn, Document | Tests the symptom-vocabulary alignment between visual annotations and textual descriptions (align: PPO/TO). |
| CQ-MM-03 *(Image×Sensor)* | For each image diagnosed with leaf blast, what were the temperature, RH, and leaf-wetness readings at the nearest sensor station during the 7 days before capture? | Relational | Image, capturedAt, Plot, nearestStation, SensorStation, Observation, temporalWindow(7d before captureTimestamp) | Spatio-temporal join of image and sensor data is the foundational fusion requirement. |
| CQ-MM-04 *(Sensor×Text)* | Which plots currently satisfy the literature-reported favourable conditions for sheath blight (e.g., 28–32 °C, RH >95%), and what is the cited source for each threshold? | Relational | Disease, favouredBy, EnvironmentalCondition, hasThreshold, hasSource, Document, Observation, Plot | Makes environmental risk rules transparent and citable rather than hard-coded. |
| CQ-MM-05 *(Sensor×Genomic)* | Which plots planted with varieties lacking any *Bph* resistance gene are experiencing conditions favourable for BPH population build-up (25–30 °C, RH >80%, high nitrogen application)? | Relational | Plot, plantedWith, Variety, carriesGene (absence), Observation, ManagementRecord, nitrogenRate | Combines host susceptibility with environmental pressure to target scouting effort. |
| CQ-MM-06 *(Text×Genomic)* | Which resistance genes reported in the literature as overcome by a pathogen race present in the target region are carried by currently recommended varieties? | Relational | ResistanceGene, overcomeBy, PathogenRace, occursIn, Region, reportedIn, Document, carriedBy, Variety, recommendationStatus | Flags resistance breakdown risk in official recommendations. |
| CQ-MM-07 *(Image×Genomic)* | Which varieties rated resistant to bacterial leaf blight have field images showing confirmed BLB lesions, and in which plots and seasons did this occur? | Relational | Image, diagnosedAs, Disease, capturedAt, Plot, plantedWith, Variety, hasResistanceRating, Season | Image evidence as an early-warning signal of resistance erosion. |
| CQ-MM-08 *(Image×Sensor)* | Which combination of sensor variables aggregated over the 10 days before capture best separates images later confirmed as leaf blast from those confirmed as brown spot? | Complex-Inferential | Image, confirmedDiagnosis, Observation, aggregated features, discriminative comparison across disease classes | Grounds an empirical, data-derived disease-discrimination rule in the KG. |
| CQ-MM-09 *(Sensor×Text)* | For each disease, how many days in the current season did each plot fall inside the literature-defined favourable envelope, and which plots exceeded the cumulative "risk-day" count that triggers an advisory? | Complex-Inferential | Disease, favouredBy, EnvironmentalCondition, Observation, Plot, riskDayCount, AdvisoryThreshold | Operationalises text-derived thresholds into an actionable seasonal risk index. |
| CQ-MM-10 *(Text×Image×Sensor)* | Given a leaf image with water-soaked, wavy-margined lesions and sensor readings of 30 °C, RH 85%, and 60 mm rain in the past 3 days, which disease is most likely, and which literature sources support the diagnosis? | Complex-Inferential | Image, VisualSymptom, Symptom, Disease, favouredBy, EnvironmentalCondition, Observation, supportedBy, Document | Prototype diagnostic query: visual evidence plus environment plus citable justification. |
| CQ-MM-11 *(Image×Sensor×Genomic)* | Given an image showing spindle-shaped grey lesions and a sensor record of 26 °C with RH >90% for 4 consecutive days, which disease is most likely, and which varieties in the KG carry resistance genes effective against the locally prevalent race of its pathogen? | Complex-Inferential | Image, VisualSymptom, Disease, favouredBy, Observation, hasCausalAgent, PathogenRace, occursIn, Region, ResistanceGene, confersResistanceTo, Variety | Closes the loop from diagnosis to variety recommendation, the core multimodal value proposition. |
| CQ-MM-12 *(Text×Image×Genomic)* | For varieties carrying a given blast resistance gene (e.g., *Pi9*), what proportion of their field images show confirmed blast lesions compared with varieties lacking it, restricted to seasons when literature reports the *Pi9*-virulent race as present? | Complex-Inferential | Variety, carriesGene, Image, diagnosedAs, proportion aggregation, PathogenRace, occursIn, Season, reportedIn, Document | Field-validates genomic resistance claims against observed image evidence, contextualised by race reports. |
| CQ-MM-13 *(Image×Sensor×Genomic)* | What was the time lag between the first sensor-detected favourable period and the first image-confirmed symptom in each plot, and do plots planted with resistant varieties show systematically longer lags than susceptible ones? | Complex-Inferential | Plot, Observation, favourableWindow, Image, captureTimestamp, firstSymptomDate, plantedWith, Variety, hasResistanceRating, temporal difference, group comparison | Temporal-causal reasoning across three modalities; supports evaluation of resistance durability in the field. |
| CQ-MM-14 *(Text×Image×Sensor×Genomic)* | Which plots simultaneously (a) contain images with tungro-like symptoms, (b) recorded conditions favourable for green leafhopper activity, (c) are planted with varieties without tungro tolerance, and (d) lie in districts with tungro reported in current-season surveillance bulletins — ranked by a combined risk score? | Complex-Inferential | Plot, Image, VisualSymptom, Observation, Pest (vector), Variety, hasResistanceRating, locatedIn, AdministrativeRegion, SurveillanceReport, riskScore | Four-way fusion query; demonstrates the KG does more than federate four separate databases. |

---

## 3. Modality-Pair Coverage Table

| Modality combination | CQs exercising it directly | CQs exercising it as part of a higher-order combination |
|---|---|---|
| Text × Image | CQ-MM-01, CQ-MM-02 | CQ-MM-10, CQ-MM-12, CQ-MM-14 |
| Image × Sensor | CQ-MM-03, CQ-MM-08 | CQ-MM-10, CQ-MM-11, CQ-MM-13, CQ-MM-14 |
| Sensor × Text | CQ-MM-04, CQ-MM-09 | CQ-MM-10, CQ-MM-14 |
| Sensor × Genomic | CQ-MM-05 | CQ-MM-11, CQ-MM-13, CQ-MM-14 |
| Text × Genomic | CQ-MM-06 | CQ-MM-12, CQ-MM-14 |
| Image × Genomic | CQ-MM-07 | CQ-MM-11, CQ-MM-12, CQ-MM-13, CQ-MM-14 |
| Three-way: Text × Image × Sensor | CQ-MM-10 | CQ-MM-14 |
| Three-way: Image × Sensor × Genomic | CQ-MM-11, CQ-MM-13 | CQ-MM-14 |
| Three-way: Text × Image × Genomic | CQ-MM-12 | CQ-MM-14 |
| Three-way: Text × Sensor × Genomic | — *(gap)* | CQ-MM-14 |
| Four-way | CQ-MM-14 | — |

**Observed gap:** no dedicated three-way Text × Sensor × Genomic CQ exists (e.g., "Which literature-recommended varieties for the current environmental risk profile carry marker-confirmed resistance?"). Sensor × Genomic is also covered by only one direct CQ. Both should be addressed if the project prioritises variety advisories that do not rely on image evidence.

---

## 4. Scope Boundary Note

**In scope.** The KG covers ten named pests and diseases of tropical lowland rice, their causal agents, vectors, races/biotypes, and literature-documented symptoms, favourable environmental conditions, and management practices; expert- and classifier-labelled images of symptoms, damage, and healthy baselines with organ-level and severity annotations linked to plots and timestamps; plot-level environmental observations with quality metadata modelled after SOSA/SSN; and variety records including resistance genes, markers, resistance ratings, release data, and trial yields. It explicitly supports spatio-temporal joins between images and sensor streams, alignment of visual and textual symptom vocabularies, and variety recommendation conditional on diagnosis and regional race prevalence.

**Out of scope.** The KG does not model rice abiotic stresses (nutrient deficiency, salinity, drought) except as differential-diagnosis distractors; it does not represent pesticide formulation chemistry, market prices, or farm economics; it does not store raw pixel data or full sensor streams (only annotations, derived features, and aggregated observations are first-class graph nodes); and it does not attempt whole-genome representation beyond named resistance loci and their markers. Pests and diseases outside the ten listed, and agroecologies outside Southeast Asian irrigated lowlands, are excluded from the initial release.

**Feasibility flags.** CQ-ENV-04 and CQ-MM-03 assume leaf-wetness sensors, which many low-cost IoT deployments lack; CQ-IMG-05, CQ-MM-08, and CQ-MM-13 require longitudinal, plot-registered image series co-located with sensors, which public image datasets do not provide and must be collected by the project; CQ-GEN-04 depends on marker–gene tables that may be incomplete for locally released varieties; CQ-TXT-06 and CQ-MM-06 depend on region-specific resistance-breakdown and race-survey literature that may be sparse. These CQs should be retained as target requirements but treated as provisional until the corresponding data sources are confirmed.
