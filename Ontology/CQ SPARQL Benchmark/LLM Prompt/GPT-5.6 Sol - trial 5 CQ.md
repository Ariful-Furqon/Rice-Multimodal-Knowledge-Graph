# Competency Questions for a Rice Pest & Disease Multimodal Knowledge Graph

## Purpose and Assumptions

The proposed multimodal knowledge graph (MMKG) is intended to support early diagnosis, evidence-based risk assessment, and management decision-making for major rice pests and diseases by semantically integrating textual knowledge, field imagery, agro-environmental sensor observations, and genomic/tabular cultivar data. Its functional scope emphasizes tropical lowland rice systems in Indonesia and Southeast Asia while remaining reusable by the international research community through alignment, where appropriate, with resources such as AGROVOC, Crop Ontology, Plant Phenotype Ontology (PPO), Plant Trait Ontology, and relevant infectious-disease ontology patterns.

Because the input fields in the source prompt were left unspecified, the following assumptions are used:

- **Primary end users:** plant pathology researchers, agricultural extension officers, rice breeders, and smart-farming/IoT system developers.
- **Pests and diseases in scope:** rice blast (*Magnaporthe oryzae*), bacterial leaf blight (BLB; *Xanthomonas oryzae* pv. *oryzae*), sheath blight (*Rhizoctonia solani*), rice tungro disease, brown planthopper (BPH; *Nilaparvata lugens*), stem borers, and rice bug, with healthy-plant observations retained as baselines.
- **Text sources:** peer-reviewed literature, extension documents, surveillance bulletins, and expert-authored symptom/management descriptions.
- **Image sources:** georeferenced and time-stamped field or close-up photographs of leaves, stems, panicles, and whole plants, including healthy controls where available.
- **Sensor sources:** timestamped temperature, relative humidity, rainfall, soil moisture, soil pH, and related agroclimatic measurements linked to field plots or observation sites.
- **Genomic/tabular sources:** cultivar identifiers, resistance genes/alleles or markers, genotype annotations, trial observations, and agronomic/yield tables.
- **Target quantity:** 38 CQs.
- **Existing ontology/schema:** none mandated; standards alignment is treated as a design requirement rather than a pre-existing constraint.

## Text-grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What causal pathogen or pest taxon is reported for each named rice disease or damage syndrome represented in the KG? | Simple | Disease; Pest; Pathogen; causedBy; hasCausalAgent; taxonIdentifier | Establishes the core etiological relations needed for diagnostic and explanatory queries. |
| CQ-TXT-02 | Which symptom descriptions reported in authoritative sources distinguish rice blast from bacterial leaf blight on rice leaves? | Relational | Disease; Symptom; PlantOrgan; describedIn; hasSymptom; distinguishesFrom | Supports differential diagnosis by ensuring that discriminative textual symptom knowledge is explicitly represented. |
| CQ-TXT-03 | Which damage symptoms, life stages, and disease-vector roles are reported for brown planthopper (*Nilaparvata lugens*)? | Relational | Pest; LifeStage; DamageSymptom; Disease; hasLifeStage; causesDamage; vectors | Captures biologically important links between pest identity, visible damage, and pathogen transmission. |
| CQ-TXT-04 | What management interventions are recommended for sheath blight, and at which crop growth stages or disease severities are they recommended? | Relational | Disease; ManagementAction; GrowthStage; SeverityClass; recommendedFor; appliedAtStage; indicatedAtSeverity | Defines the representation needed for stage- and severity-aware management support. |
| CQ-TXT-05 | Which environmental drivers are most consistently reported in the literature as increasing rice blast or sheath blight pressure? | Complex-Inferential | Disease; EnvironmentalFactor; LiteratureSource; associatedWithRisk; evidenceStrength; sourceProvenance | Requires evidence aggregation across sources rather than a single fact lookup. |
| CQ-TXT-06 | Which rice tissues and crop growth stages are reported as being attacked by stem borers and rice bug, and what named damage syndromes are associated with each? | Relational | Pest; PlantOrgan; GrowthStage; DamageSyndrome; attacks; occursAtStage; causesDamage | Ensures the ontology can encode pest–tissue–stage–damage relationships important for field diagnosis. |
| CQ-TXT-07 | Where extension recommendations for bacterial leaf blight management differ across sources, what recommendations are given, by whom, and under what stated conditions? | Complex-Inferential | Disease; ManagementAction; Source; Recommendation; conditionOfUse; assertedBy; publicationDate; provenance | Tests provenance-aware representation of potentially non-identical recommendations without forcing premature reconciliation. |

## Image-grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Which stored rice images show spindle-shaped or diamond-shaped lesions with gray centers and brown margins that are visually compatible with leaf blast? | Simple | Image; Lesion; Shape; ColorPattern; PlantOrgan; depicts; hasVisualFeature | Tests whether image-level symptom annotations can support retrieval by diagnostic visual phenotype. |
| CQ-IMG-02 | For a given field image, what rice organ is visible and which annotated symptom morphology—lesion, chlorosis, wilting, hopperburn, deadheart, whitehead, or other damage—is present? | Simple | Image; PlantOrgan; SymptomMorphology; depictsOrgan; exhibitsVisualSymptom | Supports structured conversion of visual observations into ontology-linked phenotypes. |
| CQ-IMG-03 | Which images visually distinguish bacterial leaf blight from rice blast based on lesion position, shape, color, and progression along the leaf blade? | Relational | Image; DiseaseLabel; LesionFeature; LeafRegion; hasVisualFeature; visuallySupports; visuallyDistinguishes | Defines the image annotations needed for visual differential diagnosis. |
| CQ-IMG-04 | Which whole-plant images show hopperburn-like patches consistent with severe brown planthopper feeding damage, and what visual severity class is assigned to each image? | Relational | Image; PestDamage; SeverityClass; WholePlant; depictsDamage; hasSeverity | Supports severity-aware retrieval of pest-damage imagery. |
| CQ-IMG-05 | What percentage of visible leaf area is symptomatic in each annotated close-up image, and which images exceed a specified severity threshold? | Complex-Inferential | Image; LeafArea; SymptomaticArea; SeverityMetric; hasAffectedAreaFraction; exceedsThreshold | Tests quantitative visual measurements and threshold-based image queries. |
| CQ-IMG-06 | Across a time-ordered image sequence from the same rice plot or plant, how does symptom severity change between observations? | Complex-Inferential | Image; ObservationTime; PlantOrPlot; SeverityMetric; follows; observesSameSubject; severityChange | Requires temporal linkage and comparison across image observations. |
| CQ-IMG-07 | Which previously annotated images are most visually similar to a new query image, and what symptom or damage labels are shared among the nearest matches? | Complex-Inferential | Image; VisualEmbedding; SimilarityScore; SymptomLabel; similarTo; hasAnnotation | Tests whether the MMKG can expose image-similarity evidence while preserving semantic links to expert labels. |

## Sensor / Environmental-grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | Which field plots experienced at least 12 consecutive hours with relative humidity above 90% and air temperature between 24°C and 30°C during the previous seven days? | Relational | FieldPlot; SensorObservation; Temperature; RelativeHumidity; timestamp; observedAt; consecutiveDuration | Tests temporal windowing and threshold queries over environmental observations. |
| CQ-ENV-02 | Which plots had the highest cumulative duration of high-humidity conditions during the last 14 days? | Complex-Inferential | FieldPlot; RelativeHumidity; SensorObservation; duration; aggregateDuration; rank | Requires temporal aggregation and ranking across sensor streams. |
| CQ-ENV-03 | After major rainfall events, what is the median lag time until soil-moisture readings reach their local maximum in each monitored field? | Complex-Inferential | RainfallObservation; SoilMoistureObservation; FieldPlot; timestamp; peakValue; lagTime | Tests event detection, cross-variable temporal alignment, and aggregation. |
| CQ-ENV-04 | Which monitoring periods simultaneously satisfy predefined warm, humid, and wet-field conditions—for example temperature above 27°C, relative humidity above 85%, and elevated soil moisture? | Relational | SensorObservation; EnvironmentalConditionProfile; Temperature; RelativeHumidity; SoilMoisture; satisfiesCondition | Supports reusable representation of multivariate environmental condition profiles. |
| CQ-ENV-05 | Which sensor stations show the largest week-to-week change in temperature, relative humidity, rainfall, or soil moisture, and are those changes outside their historical ranges? | Complex-Inferential | SensorStation; EnvironmentalVariable; TimeWindow; HistoricalRange; changeMagnitude; anomalyScore | Tests comparative and anomaly-oriented reasoning over environmental time series. |

## Genomic / Tabular-grounded Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which rice varieties in the KG carry annotated *Pi* resistance genes or alleles associated with blast resistance? | Simple | RiceVariety; ResistanceGene; Allele; hasGene; hasAllele; resistanceAnnotation | Supports direct cultivar-to-resistance-genotype retrieval. |
| CQ-GEN-02 | Which rice varieties contain annotated *Xa/xa* genes, alleles, or markers associated with resistance to bacterial leaf blight? | Simple | RiceVariety; ResistanceGene; MolecularMarker; hasGene; taggedByMarker; resistanceAnnotation | Tests representation of BLB resistance information at gene and marker levels. |
| CQ-GEN-03 | Which cultivars combine annotations for resistance to more than one major rice disease or pest, and which resistance determinants co-occur in each cultivar? | Relational | RiceVariety; ResistanceTrait; ResistanceGene; resistantTo; hasGene; coOccursWith | Supports multi-resistance breeding and cultivar selection queries. |
| CQ-GEN-04 | Among varieties with recorded resistance annotations, which have the highest mean grain yield across the available tabular trials? | Complex-Inferential | RiceVariety; Trial; YieldMeasurement; ResistanceAnnotation; evaluatedIn; hasYield; meanValue; rank | Tests integration and aggregation within structured genotype–phenotype–agronomic tables. |
| CQ-GEN-05 | For each resistance-gene record, what cultivar accession, allele or marker identifier, evidence source, and curation provenance are stored? | Relational | ResistanceGene; Allele; Marker; Accession; EvidenceRecord; hasProvenance; derivedFrom; identifier | Ensures genomic assertions are traceable and reusable rather than stored as unsupported labels. |

## Cross-modal / Fusion Competency Questions

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 | Given a leaf image with blast-like lesions and sensor data showing prolonged warm, humid conditions around the observation time, which disease diagnosis is most strongly supported by the combined visual and environmental evidence? | Complex-Inferential | Image; Disease; VisualFeature; SensorObservation; EnvironmentalCondition; visuallySupports; temporallyAlignedWith; supportsDiagnosis | Demonstrates fusion of visual evidence with local environmental context for early diagnosis. |
| CQ-MM-02 | For an image showing an unknown leaf lesion, which literature-described symptom profiles best match the annotated visual features, and which candidate diseases do those profiles support? | Relational | Image; VisualFeature; TextDescription; Symptom; Disease; matchesDescription; hasSymptom; supportsCandidate | Links field imagery to textual diagnostic knowledge rather than treating image labels as isolated metadata. |
| CQ-MM-03 | When a field's sensor observations satisfy blast-risk environmental conditions, which rice varieties in the genomic/tabular data carry blast-resistance genes suitable for consideration in that environment? | Relational | FieldPlot; SensorObservation; DiseaseRiskProfile; RiceVariety; ResistanceGene; satisfiesRiskProfile; resistantTo; hasGene | Connects observed field risk with resistance information for cultivar-oriented decision support. |
| CQ-MM-04 | Which rice varieties have resistance genes that are explicitly supported by literature assertions for blast, bacterial leaf blight, or other diseases represented in the KG? | Relational | RiceVariety; ResistanceGene; Disease; LiteratureSource; hasGene; resistantTo; supportedBy | Tests evidence-backed linkage between genomic records and textual scientific claims. |
| CQ-MM-05 | Which sensor observation windows meet environmental thresholds reported in the literature as conducive to sheath blight or rice blast development? | Relational | LiteratureSource; Disease; EnvironmentalThreshold; SensorObservation; reportsThreshold; satisfiesThreshold | Operationalizes published risk knowledge against real environmental observations. |
| CQ-MM-06 | For images visually diagnosed as bacterial leaf blight, which varieties in the genomic/tabular data contain annotated BLB-resistance genes or markers? | Relational | Image; Disease; RiceVariety; ResistanceGene; MolecularMarker; visuallySupports; resistantTo; hasGene | Links image-based diagnosis directly to resistance-oriented cultivar information. |
| CQ-MM-07 | Across repeated observations of the same plot, how does image-derived symptom severity change in relation to temperature, humidity, rainfall, and soil-moisture conditions during the preceding three to seven days? | Complex-Inferential | Image; SeverityMetric; FieldPlot; SensorObservation; TimeWindow; precedes; temporallyAlignedWith; severityChange; correlation | Tests temporal fusion between symptom progression and environmental exposure. |
| CQ-MM-08 | For a symptomatic rice image, which differential diagnoses are supported jointly by visual features, textual symptom descriptions, and the local sensor history, and what evidence supports each candidate? | Complex-Inferential | Image; TextDescription; SensorObservation; Disease; Evidence; VisualFeature; hasSymptom; satisfiesRiskProfile; supportsDiagnosis | Requires transparent three-way evidence fusion for explainable differential diagnosis. |
| CQ-MM-09 | Given a visually suspected blast case and sensor-confirmed conducive conditions, which locally represented varieties carry blast-resistance genes and therefore warrant higher priority for future planting trials? | Complex-Inferential | Image; SensorObservation; Disease; RiceVariety; ResistanceGene; visuallySupports; satisfiesRiskProfile; hasGene; candidateForTrial | Links diagnosis and current environmental pressure to genomic decision support. |
| CQ-MM-10 | Which rice varieties combine resistance genes documented in the literature with favorable yield performance in tabular trials conducted under sensor-observed environments similar to the target field? | Complex-Inferential | RiceVariety; ResistanceGene; LiteratureSource; Trial; YieldMeasurement; SensorObservation; supportedBy; evaluatedIn; environmentSimilarity | Tests evidence-backed cultivar ranking across text, sensor, and genomic/tabular modalities. |
| CQ-MM-11 | For a disease confirmed from annotated field images, which resistance genes are supported by literature evidence and which stored cultivars carry those genes? | Relational | Image; Disease; LiteratureSource; ResistanceGene; RiceVariety; confirms; supportedBy; hasGene; resistantTo | Connects visual diagnosis to scientific evidence and actionable cultivar genetics. |
| CQ-MM-12 | For a newly observed symptomatic field, what diagnosis is best supported by the image, recent environmental sensor history, and textual diagnostic knowledge, and which resistant varieties in the genomic data are relevant to that diagnosis? | Complex-Inferential | Image; SensorObservation; TextDescription; Disease; RiceVariety; ResistanceGene; supportsDiagnosis; temporallyAlignedWith; supportedBy; resistantTo | Exercises the full four-modality chain that motivates construction of a multimodal rather than siloed KG. |
| CQ-MM-13 | Across historical field episodes with confirmed disease labels, which combinations of pre-observation sensor conditions and image-derived severity are associated with the largest disease burden, and do susceptible versus resistant cultivar groups show different patterns? | Complex-Inferential | DiseaseEpisode; Image; SeverityMetric; SensorObservation; RiceVariety; ResistanceTrait; precedes; hasSeverity; resistantTo; susceptibleTo; aggregate | Tests longitudinal multimodal analysis for outbreak characterization and genotype-by-environment comparison. |
| CQ-MM-14 | For a current field episode, which management actions documented in extension or scientific text are applicable to the visually supported diagnosis, observed disease severity, recent environmental conditions, and planted cultivar's resistance profile? | Complex-Inferential | FieldEpisode; Image; SeverityClass; SensorObservation; Disease; ManagementAction; RiceVariety; ResistanceTrait; recommendedFor; applicableUnder; hasResistanceProfile | Tests whether the KG can support explainable management recommendations conditioned on four complementary evidence sources. |

## Modality-pair Coverage and Traceability

| Modality combination | CQ IDs | Coverage purpose |
|---|---|---|
| Text × Image | CQ-MM-02, CQ-MM-08, CQ-MM-11, CQ-MM-12, CQ-MM-14 | Connects visual observations to published symptom, diagnosis, and management knowledge. |
| Text × Sensor | CQ-MM-05, CQ-MM-08, CQ-MM-10, CQ-MM-12, CQ-MM-14 | Matches literature-defined environmental risk or management conditions with observed field data. |
| Text × Genomic/Tabular | CQ-MM-04, CQ-MM-10, CQ-MM-11, CQ-MM-12, CQ-MM-14 | Links resistance genes, cultivars, and trial results to explicit scientific or extension evidence. |
| Image × Sensor | CQ-MM-01, CQ-MM-07, CQ-MM-08, CQ-MM-09, CQ-MM-12, CQ-MM-13, CQ-MM-14 | Fuses visible disease evidence with temporally aligned environmental exposure. |
| Image × Genomic/Tabular | CQ-MM-06, CQ-MM-09, CQ-MM-11, CQ-MM-12, CQ-MM-13, CQ-MM-14 | Links visual diagnosis or severity to cultivar resistance and susceptibility information. |
| Sensor × Genomic/Tabular | CQ-MM-03, CQ-MM-09, CQ-MM-10, CQ-MM-12, CQ-MM-13, CQ-MM-14 | Connects field risk environments with cultivar genotype, resistance, or performance data. |
| Text × Image × Sensor | CQ-MM-08, CQ-MM-12, CQ-MM-14 | Supports explainable diagnosis by combining visual, environmental, and textual evidence. |
| Image × Sensor × Genomic/Tabular | CQ-MM-09, CQ-MM-12, CQ-MM-13, CQ-MM-14 | Supports genotype-aware interpretation of disease observations under measured environments. |
| Text × Image × Genomic/Tabular | CQ-MM-11, CQ-MM-12, CQ-MM-14 | Links image-supported disease identity to literature-supported resistance genes and cultivars. |
| Text × Sensor × Genomic/Tabular | CQ-MM-10, CQ-MM-12, CQ-MM-14 | Supports evidence-backed cultivar selection under measured or comparable environments. |
| Text × Image × Sensor × Genomic/Tabular | CQ-MM-12, CQ-MM-14 | Exercises end-to-end multimodal diagnosis and management decision support. |


## Scope Boundary Note

**In scope** are rice pest and disease entities, causal agents, visual symptoms and damage phenotypes, field observations, environmental sensor measurements, cultivar/genotype and resistance information, agronomic trial measurements, textual evidence and provenance, and management recommendations needed to answer the CQs above. The KG must support entity alignment, temporal and spatial linkage of observations, multimodal evidence provenance, threshold and aggregation queries, and explainable traversal from field evidence to diagnosis, resistance, and management knowledge. **Out of scope** are autonomous pesticide application, economic optimization beyond represented agronomic tables, full farm-enterprise management, mechanistic crop-growth simulation, and causal claims that cannot be supported by represented evidence.

Some CQs may be infeasible unless the corresponding source data exist at adequate quality and granularity. In particular, **CQ-IMG-07** requires image embeddings or an equivalent visual-similarity representation; **CQ-MM-07**, **CQ-MM-13**, and **CQ-MM-14** require reliable temporal and field-level alignment across modalities; and **CQ-MM-10**, **CQ-MM-12**, and **CQ-MM-14** require sufficiently curated gene–disease evidence, cultivar identifiers, and environmental or trial metadata. These questions should therefore be treated both as evaluation targets and as explicit data-acquisition requirements during MMKG construction.

## Distribution Summary

| Category | Count | Share of 38 CQs |
|---|---:|---:|
| Text-grounded | 7 | 18.4% |
| Image-grounded | 7 | 18.4% |
| Sensor / Environmental-grounded | 5 | 13.2% |
| Genomic / Tabular-grounded | 5 | 13.2% |
| Cross-modal / Fusion | 14 | 36.8% |
| **Total** | **38** | **100%** |

The distribution keeps cross-modal/fusion questions as the largest category while maintaining substantial unimodal coverage for ontology requirements, data integration testing, and later SPARQL-based evaluation.
