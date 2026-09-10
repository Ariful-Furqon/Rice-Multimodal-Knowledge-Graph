# Competency Questions for a Multimodal Knowledge Graph of Rice Pests and Diseases

## 0. Assumptions Made (all user input fields were left as placeholders)

| Input field | Default adopted |
|---|---|
| Pests/diseases in scope | Rice blast (*Magnaporthe oryzae* / *Pyricularia oryzae*), bacterial leaf blight (BLB, *Xanthomonas oryzae* pv. *oryzae*, Xoo), sheath blight (*Rhizoctonia solani*), rice tungro disease (RTBV + RTSV, vectored by *Nephotettix virescens*), brown planthopper (BPH, *Nilaparvata lugens*), yellow stem borer (YSB, *Scirpophaga incertulas*), rice bug (*Leptocorisa oratorius*) |
| Primary end users | Plant pathology researchers, agricultural extension officers, smart-farming/IoT system developers |
| Geographic scope | Indonesia / Southeast Asian tropical lowland irrigated rice |
| Text sources | Peer-reviewed literature (abstracts/full text), IRRI Rice Knowledge Bank–style fact sheets, national extension bulletins, pest surveillance reports |
| Image sources | Field and close-up photographs with disease/pest labels, plant-organ labels, optional severity scores (IRRI Standard Evaluation System scale), capture date and field/plot ID |
| Sensor sources | Field weather stations and IoT loggers reporting air temperature, relative humidity (RH), rainfall, leaf wetness duration, soil moisture and soil pH at hourly–daily resolution, geolocated |
| Genomic/tabular sources | Variety catalogue (e.g., IR64, Ciherang, Inpari 32, IR72, Swarna, TN1) with pedigree, resistance-gene loci (e.g., *Xa4*, *xa5*, *xa13*, *Xa21*; *Pi9*, *Pita*, *Pib*, *Pi54*; *Bph3*, *Bph14*, *Bph18*), resistance ratings by pathotype/biotype, and trial yield tables |
| Target CQ count | 35 |
| Ontology alignment | None mandated; alignment targets flagged where relevant: Crop Ontology (CO_320 Rice), AGROVOC, Plant Phenotype Ontology (PPO), Plant Trait Ontology (TO), NCBI Taxonomy, ENVO, W3C SOSA/SSN (sensor observations), OWL-Time, IDO-Plant patterns, and IRRI SES severity scales |
| Pre-existing CQs | None |

---

## 1. Purpose and Scope Statement (for confirmation)

The knowledge graph (KG) is intended to support early diagnosis and management decisions for the major pests and diseases of tropical lowland rice in Southeast Asia by semantically integrating four modalities: textual domain knowledge, symptom/damage imagery, field environmental sensor observations, and variety-level genomic and agronomic tables. Its core value proposition is that a diagnostic or advisory query can traverse from a visual observation, through environmental context and literature-encoded epidemiological rules, to variety-level resistance information within a single graph query. The competency questions below define the classes, relations and cross-modal links the ontology must support, and double as the evaluation criteria against which the constructed KG will be tested via SPARQL.

---

## 2. Competency Questions

### 2a. Text-grounded CQs (6)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal agent of rice blast, and to which taxonomic kingdom and genus does it belong? | Simple | Disease, causedBy, Pathogen, hasTaxonomicRank (align: NCBI Taxonomy, AGROVOC) | Anchors every disease node to a formally identified pathogen, a prerequisite for linking diagnoses to literature and genomic resistance. |
| CQ-TXT-02 | Which insect vector transmits rice tungro disease, and which of the two tungro viruses depends on the other for transmission? | Simple | Disease, hasCausalAgent, Virus; Virus, transmittedBy, Vector(Pest); Virus, dependsOnForTransmission, Virus | Captures the vector-borne, two-virus structure of tungro, which distinguishes its management (vector control) from fungal/bacterial diseases. |
| CQ-TXT-03 | Which management practices (cultural, chemical, biological) are recommended for brown planthopper control, and which source document recommends each? | Relational | Pest, controlledBy, ManagementPractice; ManagementPractice, hasCategory; ManagementPractice, recommendedIn, Document | Provides provenance-tracked recommendations that extension officers can cite, and tests the Document→Claim provenance pattern. |
| CQ-TXT-04 | At which rice growth stages is yellow stem borer damage reported, and which damage symptom term (deadheart, whitehead) is associated with each stage? | Relational | Pest, causesSymptom, Symptom; Symptom, occursAtStage, GrowthStage (align: Crop Ontology / BBCH rice scale) | Establishes the stage-conditioned symptom vocabulary that image annotations must later reuse. |
| CQ-TXT-05 | For which diseases do surveillance bulletins report increasing incidence in a given province over two or more consecutive seasons, and which bulletins support each trend? | Complex-Inferential | SurveillanceReport, reportsIncidence, IncidenceRecord; IncidenceRecord, ofDisease, Disease; locatedIn, Region; inSeason, Season; temporal ordering | Enables retrospective trend queries over textual surveillance data, supporting regional prioritisation. |
| CQ-TXT-06 | Which Xoo pathotypes or *M. oryzae* races are reported in the literature to have overcome a named resistance gene, and in which country and year was the breakdown first documented? | Complex-Inferential | Pathotype, overcomes, ResistanceGene; ReportedIn, Publication; Publication, hasYear, hasCountry | Encodes resistance-breakdown knowledge that is essential for interpreting genomic resistance data in a regional context. |

### 2b. Image-grounded CQs (6)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Which images depict bacterial leaf blight lesions on rice leaves? | Simple | Image, depicts, SymptomInstance; SymptomInstance, manifestationOf, Disease; SymptomInstance, onPlantPart, PlantPart | Basic retrieval of labelled visual evidence, the entry point for image-based diagnosis. |
| CQ-IMG-02 | For a given image, which plant organ (leaf, leaf sheath, stem, panicle, whole plant) is shown, and is the sample annotated as healthy or symptomatic? | Simple | Image, showsOrgan, PlantPart (align: PPO/Plant Ontology); Image, hasHealthStatus | Ensures healthy baselines and organ-level context are first-class, which classifiers and human reviewers both require. |
| CQ-IMG-03 | Which visual features (e.g., diamond-shaped lesions with grey centres, water-soaked lesions with wavy yellow margins, hopperburn) are annotated as distinguishing rice blast images from bacterial leaf blight images? | Relational | Symptom, hasVisualFeature, VisualFeature; VisualFeature, discriminates, Disease pair | Makes the discriminating visual cues explicit so that the KG can explain, not merely return, a diagnosis. |
| CQ-IMG-04 | Which images show damage attributed to insect pests rather than pathogens, and which pest is annotated for each? | Relational | Image, depictsDamage, DamageInstance; DamageInstance, causedBy, Pest; Pest disjointWith Pathogen | Tests the pest/pathogen disjointness in the ontology and supports pest-specific image retrieval. |
| CQ-IMG-05 | Across all annotated sheath blight images, what is the distribution of severity scores (IRRI SES 0–9) by growth stage at capture? | Complex-Inferential | Image, hasSeverityScore, SeverityScore; Image, capturedAtStage, GrowthStage; aggregation (COUNT/GROUP BY) | Quantifies severity progression, needed for both epidemiological analysis and balanced training-set construction. |
| CQ-IMG-06 | Which images carry conflicting disease labels from different annotators or models, and what confidence value is attached to each label? | Complex-Inferential | Image, hasAnnotation, Annotation; Annotation, assignedBy, Agent; Annotation, hasLabel, Disease; hasConfidence | Surfaces uncertain or disputed evidence, so that downstream fusion queries can weight image evidence appropriately. |

### 2c. Sensor/environmental-grounded CQs (5)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What were the daily mean air temperature and relative humidity recorded at station S on date D? | Simple | Station (sosa:Sensor/Platform), madeObservation, Observation; observedProperty, hasResult, resultTime (align: SOSA/SSN, ENVO) | Baseline retrieval that validates the observation model against the SOSA pattern. |
| CQ-ENV-02 | Which monitored fields experienced at least three consecutive days with RH above 90 % and mean temperature between 25 °C and 28 °C during the tillering stage of season X? | Relational | Field, monitoredBy, Station; Observation thresholds; Field, hasCrop, CropCycle; CropCycle, atStage, GrowthStage; temporal windowing | Expresses the kind of condition-run query that underlies most disease-risk rules. |
| CQ-ENV-03 | Which sensor stations lie within 5 km of field F, and which environmental variables does each measure? | Relational | Station, hasLocation, Geometry; spatial proximity; Station, observes, ObservableProperty | Ensures the KG can assign the most representative station to a field when no on-field sensor exists. |
| CQ-ENV-04 | For each monitored field, how many days with rainfall above 10 mm or leaf wetness duration above 10 h occurred in the 14 days preceding a given date, ranked in descending order? | Complex-Inferential | Field, Observation, aggregation over a sliding temporal window; ranking | Produces the wetness-pressure indicator used by most blast and sheath blight forecasting heuristics. |
| CQ-ENV-05 | Which stations show an increasing trend in mean night-time temperature across three consecutive wet seasons, and by how much per season? | Complex-Inferential | Station, Observation, Season; aggregation by season; comparison across ordered seasons | Supports climate-shift analysis relevant to shifts in pest (e.g., BPH) pressure over time. |

### 2d. Genomic/tabular-grounded CQs (5)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which resistance genes does variety IR64 carry, and against which disease or pest does each confer resistance? | Simple | Variety, carriesGene, ResistanceGene; ResistanceGene, confersResistanceTo, Disease/Pest (align: TO, Crop Ontology) | Core lookup that all cross-modal variety-recommendation queries depend on. |
| CQ-GEN-02 | What is the recorded resistance rating of variety Ciherang against Xoo pathotype IV, and from which trial or catalogue does the rating come? | Simple | Variety, hasResistanceRating, ResistanceRating; ResistanceRating, againstPathotype, Pathotype; derivedFrom, Dataset | Distinguishes gene presence from phenotypic rating, which are frequently conflated in tabular sources. |
| CQ-GEN-03 | Which varieties carry at least two blast resistance genes (e.g., *Pi9*, *Pita*, *Pib*, *Pi54*) and have a recorded trial yield of at least 6 t/ha? | Relational | Variety, carriesGene (COUNT ≥ 2); Variety, hasYieldRecord, YieldRecord; YieldRecord, hasValue, inTrial | Supports breeding and recommendation queries that balance resistance stacking with productivity. |
| CQ-GEN-04 | Which varieties share a parent with IR64 in their recorded pedigree, and which of those also carry a *Bph* resistance gene? | Relational | Variety, hasParent, Variety (pedigree graph); carriesGene, ResistanceGene | Tests pedigree traversal, which is needed to reason about likely inherited resistance in under-characterised varieties. |
| CQ-GEN-05 | Which resistance genes confer resistance to BPH biotypes 1–3 in the largest number of catalogued varieties, ranked by variety count? | Complex-Inferential | ResistanceGene, effectiveAgainst, Biotype; Variety, carriesGene; aggregation and ranking | Identifies the most widely deployed genes, which informs vulnerability analysis if a biotype overcomes them. |

### 2e. Cross-modal / fusion CQs (13)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 | *(Text × Image)* For an image annotated with the symptom "whitehead", which pest does the literature identify as the cause, and which additional symptoms of that pest does the same source describe? | Relational | Image, depicts, Symptom; Symptom, describedIn, Document; Pest, causesSymptom, Symptom | Validates that image labels and textual symptom vocabulary resolve to the same Symptom nodes rather than parallel label sets. |
| CQ-MM-02 | *(Image × Sensor)* For images captured at field F on date D that show lesion symptoms, what were the daily temperature, RH and rainfall at the nearest station over the seven days preceding capture? | Relational | Image, capturedAt, Field; Image, captureDate; Field, nearestStation, Station; Observation within window | Attaches environmental context to every visual observation, the basic step for context-aware diagnosis. |
| CQ-MM-03 | *(Sensor × Genomic)* Which fields planted with varieties lacking any *Bph* resistance gene experienced five or more consecutive days with RH above 85 % and mean temperature of 28–30 °C in the current season? | Relational | Field, plantedWith, Variety; Variety, carriesGene (NOT EXISTS); Field, Observation thresholds | Produces an at-risk field list combining host susceptibility with pest-conducive weather. |
| CQ-MM-04 | *(Text × Genomic)* Which catalogued varieties rely solely on resistance genes that the literature reports as already overcome by Xoo pathotypes present in Indonesia? | Relational | Variety, carriesGene; Pathotype, overcomes, ResistanceGene; Pathotype, reportedIn, Region; Publication provenance | Flags varieties whose tabular "resistant" status is regionally obsolete, a critical safeguard for recommendations. |
| CQ-MM-05 | *(Image × Genomic)* For image I, which variety was photographed, and is that variety recorded as resistant, moderately resistant or susceptible to the disease annotated in the image? | Relational | Image, ofPlant, PlantSample; PlantSample, ofVariety, Variety; Variety, hasResistanceRating, Disease | Links visual evidence to host genotype, enabling detection of unexpected symptom expression on nominally resistant hosts. |
| CQ-MM-06 | *(Text × Sensor)* Which sensor time windows and fields satisfy the conducive-condition set for rice blast as encoded from literature (e.g., night temperature 17–23 °C, RH ≥ 90 %, leaf wetness ≥ 10 h)? | Relational | ConduciveConditionSet, forDisease, Disease; ConduciveConditionSet, derivedFrom, Document; ConditionThreshold, onProperty, ObservableProperty; Observation matching | Converts textual epidemiological rules into executable graph constraints over sensor data, the core of rule-based early warning. |
| CQ-MM-07 | *(Image × Sensor × Genomic)* Given a leaf image showing diamond-shaped lesions with grey centres, and readings of 24 °C and 92 % RH at the field over the previous week, which disease is most likely, and which varieties in the KG carry resistance genes against it? | Complex-Inferential | VisualFeature, indicates, Disease; ConduciveConditionSet matching; Disease, resistedBy, ResistanceGene; Variety, carriesGene; ranking by evidence agreement | The canonical diagnostic-to-advisory query that justifies a multimodal rather than federated design. |
| CQ-MM-08 | *(Image × Text × Sensor)* Which image-confirmed sheath blight diagnoses occurred in fields whose preceding 10-day environmental record matched literature-derived conducive conditions, and which fields show the highest frequency of such matched events per season? | Complex-Inferential | Diagnosis, confirmedBy, Image; Diagnosis, atField; ConduciveConditionSet, derivedFrom, Document; Observation window; aggregation | Empirically validates textual epidemiological rules against observed outbreaks, supporting rule refinement. |
| CQ-MM-09 | *(Text × Image × Sensor × Genomic)* Which fields planted with varieties lacking *Xa21*, exposed to literature-defined BLB-conducive conditions, also contain images annotated with BLB lesions in the same season, and what proportion of at-risk fields does this represent? | Complex-Inferential | Field, plantedWith, Variety, carriesGene; ConduciveConditionSet, derivedFrom, Document; Observation; Image, capturedAt, depicts; proportion aggregation | Four-way validation of a risk model: host susceptibility × weather × textual rule × visual confirmation. |
| CQ-MM-10 | *(Text × Sensor × Genomic)* Which varieties recommended by extension bulletins for region R carry resistance genes against the diseases whose conducive conditions occurred most frequently in R's sensor records over the last three seasons? | Complex-Inferential | Document, recommends, Variety, forRegion; Variety, carriesGene, confersResistanceTo, Disease; ConduciveConditionSet frequency aggregation by Region | Delivers a data-driven variety recommendation that reconciles extension advice with observed local climate. |
| CQ-MM-11 | *(Image × Text)* For each disease, what proportion of image annotation labels correspond to symptom terms defined in the textual controlled vocabulary, and which image labels lack any text-grounded definition? | Complex-Inferential | Annotation, hasLabel; Symptom, hasDefinitionIn, Document; SKOS/AGROVOC alignment; coverage aggregation | Audits vocabulary alignment between modalities, a KG quality metric reviewers will expect. |
| CQ-MM-12 | *(Image × Sensor)* For fields with time-series imagery, how many days elapsed between the first occurrence of blast-conducive conditions and the first image showing blast symptoms, per field and season? | Complex-Inferential | Field, Observation (first match); Image series ordered by captureDate; temporal difference; grouping by Field and Season | Estimates observed latent periods, which calibrates the lead time of the early-warning function. |
| CQ-MM-13 | *(Genomic × Image × Text)* Which varieties rated resistant in the tabular data nonetheless have field images showing symptoms of the corresponding disease, and does the literature report breakdown of the relevant resistance gene by a pathotype present in that region? | Complex-Inferential | Variety, hasResistanceRating; Image, ofPlant, ofVariety, depicts, Disease; Pathotype, overcomes, ResistanceGene; reportedIn, Region | Detects discordance between genomic expectation and visual reality and explains it via textual evidence. |

---

## 3. Modality-Pair Coverage Table

| Modality combination | CQ IDs |
|---|---|
| Text × Image | CQ-MM-01, CQ-MM-11 (also within CQ-MM-08, CQ-MM-09, CQ-MM-13) |
| Text × Sensor | CQ-MM-06 (also within CQ-MM-08, CQ-MM-09, CQ-MM-10) |
| Text × Genomic | CQ-MM-04 (also within CQ-MM-09, CQ-MM-10, CQ-MM-13) |
| Image × Sensor | CQ-MM-02, CQ-MM-12 (also within CQ-MM-07, CQ-MM-08, CQ-MM-09) |
| Image × Genomic | CQ-MM-05 (also within CQ-MM-07, CQ-MM-09, CQ-MM-13) |
| Sensor × Genomic | CQ-MM-03 (also within CQ-MM-07, CQ-MM-09, CQ-MM-10) |
| Three-way: Image × Sensor × Genomic | CQ-MM-07 |
| Three-way: Image × Text × Sensor | CQ-MM-08 |
| Three-way: Text × Sensor × Genomic | CQ-MM-10 |
| Three-way: Genomic × Image × Text | CQ-MM-13 |
| Four-way: Text × Image × Sensor × Genomic | CQ-MM-09 |

Every pairwise combination is exercised by at least one dedicated CQ, all four three-way combinations are covered, and one four-way CQ is included. Distribution: 6 text (17 %), 6 image (17 %), 5 sensor (14 %), 5 genomic (14 %), 13 fusion (37 %) — 35 CQs in total.

---

## 4. Scope Boundary Note

**In scope.** The KG represents seven major pests and diseases of tropical lowland rice in Southeast Asia, their causal agents, vectors, symptoms and visual features, stage-specific damage, management practices with document provenance, field-level environmental observations modelled after SOSA/SSN, literature-derived conducive-condition rules, and variety-level pedigree, resistance-gene, pathotype-rating and yield data; it supports diagnosis, risk assessment, variety recommendation and rule validation queries that traverse any combination of these modalities. **Out of scope** are weed and nematode problems, abiotic disorders (nutrient deficiency, salinity, drought stress) except as confounders of visual diagnosis, molecular-level sequence data beyond named resistance loci, post-harvest storage pests, economic and market data, and the training or hosting of image classification models themselves (the KG stores their outputs and provenance, not the models).

**Feasibility flags.** CQ-IMG-06 requires multi-annotator or multi-model labels, which most public rice-disease image datasets lack. CQ-MM-05, CQ-MM-09, CQ-MM-12 and CQ-MM-13 require images that are linked to a known variety, field and capture date, together with longitudinal capture at the same field; this metadata is rarely present in crowd-sourced or benchmark image sets and will likely require a dedicated field campaign. CQ-ENV-04 and CQ-MM-06 assume leaf-wetness sensors, which are less common than temperature/RH loggers and may need to be proxied from RH and rainfall. CQ-TXT-06 and CQ-MM-04 depend on curated regional pathotype surveys, which exist for Xoo in Indonesia but are sparser for *M. oryzae* races. These CQs should be retained in the requirements specification but marked as conditional on data acquisition.
