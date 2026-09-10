# Competency Questions for a Rice Pest & Disease Multimodal Knowledge Graph

## Assumptions

The input fields of the prompt were left as placeholders; the following defaults were applied and are marked explicitly:

| Input field | Assumption used |
|---|---|
| Pests/diseases in scope | Major lowland-rice pests and diseases: rice blast (*Magnaporthe oryzae*), bacterial leaf blight (*Xanthomonas oryzae* pv. *oryzae*, Xoo), bacterial leaf streak (*X. oryzae* pv. *oryzicola*), sheath blight (*Rhizoctonia solani*), rice tungro (RTBV/RTSV, vectored by *Nephotettix virescens*), brown planthopper (*Nilaparvata lugens*), yellow stem borer (*Scirpophaga incertulas*), rice bug (*Leptocorisa* spp.) |
| Primary end users | Plant-pathology researchers, agricultural extension officers, and smart-farming/IoT system developers |
| Geographic scope | Indonesia / Southeast Asian tropical lowland irrigated rice |
| Datasets | TEXT: peer-reviewed literature, IRRI/national extension bulletins, surveillance reports. IMAGE: field and close-up photographs with expert annotations (disease/pest label, plant part, severity score, bounding box or mask). SENSOR: IoT nodes recording air temperature, RH, rainfall, leaf wetness, soil moisture and pH at 15–60 min resolution. GENOMIC/TABULAR: variety catalogue with resistance-gene presence (Pi, Xa/xa, Bph genes), variety-trial yield and disease-score tables |
| Target CQ count | 36 (within the ~30–40 default) |
| Existing ontology to align with | None fixed; alignment candidates flagged: AGROVOC, Crop Ontology, Plant Trait Ontology (TO), Plant Phenotype Ontology (PPO), NCBI Taxonomy, SOSA/SSN (sensors), Time Ontology (OWL-Time), GeoSPARQL, Plant Disease Ontology / IDO patterns |

Identifier scheme: `CQ-TXT` (text), `CQ-IMG` (image), `CQ-ENV` (sensor/environmental), `CQ-GEN` (genomic/tabular), `CQ-MM` (cross-modal/fusion). Complexity levels: **S** = Simple/factual, **R** = Relational (2–3 hops), **C** = Complex/inferential.

---

## 1. Purpose and Scope Restatement

The knowledge graph (KG) is intended to support early diagnosis and management decision-making for rice pests and diseases in Southeast Asian lowland rice by semantically integrating four modalities: textual knowledge (literature, extension and surveillance reports), annotated field imagery, IoT-collected agroclimatic time series, and structured variety/genotype/trial data. Its functional scope is defined by the 36 competency questions below, which prioritise cross-modal questions—those that can only be answered by traversing links between modalities—as the primary justification for a unified multimodal KG rather than four separate databases. The CQs are intended to serve as the ontology requirements specification and as the basis for SPARQL-based evaluation.

---

## 2. Competency Questions

### 2a. Text-grounded CQs (6)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal agent of bacterial leaf blight, and to which taxonomic group (bacterium, fungus, virus, insect) does it belong? | S | `Disease`, `hasCausalAgent`, `Pathogen`, `hasTaxonomicRank`, `TaxonomicGroup` (align: NCBI Taxonomy, AGROVOC) | Establishes the basic disease–agent backbone every diagnostic query traverses. |
| CQ-TXT-02 | Which plant parts and growth stages does the literature report as affected by rice blast (leaf, collar, node, neck, panicle blast)? | S | `Disease`, `affectsPlantPart`, `PlantPart` (align: Plant Ontology), `occursAtGrowthStage`, `GrowthStage` (align: Crop Ontology / BBCH) | Plant-part and stage constraints are the primary filters for narrowing candidate diagnoses in the field. |
| CQ-TXT-03 | Which insect vectors transmit rice tungro viruses (RTBV, RTSV), and which management practices do extension reports recommend against those vectors? | R | `Disease`, `hasCausalAgent`, `Virus`, `transmittedBy`, `Vector` (subclass of `Pest`), `controlledBy`, `ManagementPractice`, `recommendedIn`, `Document` | Tungro management is vector-mediated; the KG must link a disease to its vector and to vector-targeted interventions. |
| CQ-TXT-04 | Which diagnostic features are cited in the literature to distinguish bacterial leaf blight from bacterial leaf streak, and in which documents are those distinctions described? | R | `Disease`, `hasSymptom`, `Symptom`, `hasDiagnosticFeature`, `DiagnosticFeature`, `distinguishedFrom`, `describedIn`, `Document` | Look-alike diseases are a leading source of misdiagnosis; the KG must encode differential-diagnosis knowledge with provenance. |
| CQ-TXT-05 | According to surveillance bulletins for a given province, which diseases or pests were reported with increasing incidence over the last five cropping seasons, and which bulletins support the trend? | C | `SurveillanceReport`, `reportsOccurrence`, `OccurrenceRecord`, `ofDiseaseOrPest`, `inLocation`, `inSeason`, `incidenceValue`; temporal aggregation and ordering | Enables regional risk prioritisation from textual surveillance alone, with evidence traceability. |
| CQ-TXT-06 | Which management practices for brown planthopper are recommended by two or more independent sources, and do any sources report conflicting advice (e.g., insecticide-induced resurgence)? | C | `ManagementPractice`, `recommendedFor`, `Pest`, `recommendedIn`/`discouragedIn`, `Document`, `hasAuthor`/`hasPublisher`, `conflictsWith`; counting over distinct sources | Extension advice must be weighed by consensus; the KG should surface agreement and contradiction across documents. |

### 2b. Image-grounded CQs (6)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Which images depict lesions annotated as rice blast on the leaf blade, and what severity score was assigned to each? | S | `Image`, `hasAnnotation`, `Annotation`, `labelsDisease`, `Disease`, `onPlantPart`, `PlantPart`, `hasSeverityScore` | Core retrieval of labelled visual evidence per disease and plant part. |
| CQ-IMG-02 | Which images serve as healthy baselines for a given variety (e.g., IR64) at the tillering stage? | S | `Image`, `depicts`, `PlantSpecimen`, `ofVariety`, `Variety`, `atGrowthStage`, `GrowthStage`, `healthStatus = healthy` | Healthy baselines are required for symptom contrast and for training/evaluating visual classifiers. |
| CQ-IMG-03 | Which annotated visual features (lesion shape, colour, margin type, distribution on the leaf) are shared between images labelled sheath blight and images labelled bacterial leaf blight? | R | `Image`, `hasAnnotation`, `hasVisualFeature`, `VisualFeature` (with `shape`, `colour`, `margin`, `distribution` sub-properties), `labelsDisease` | Identifies visually confusable classes to guide differential-diagnosis rules and classifier error analysis. |
| CQ-IMG-04 | Which images show damage attributed to yellow stem borer (dead heart or whitehead), and at which growth stage of the crop were they captured? | R | `Image`, `hasAnnotation`, `labelsDamageSymptom`, `DamageSymptom` (`deadHeart`, `whitehead`), `causedBy`, `Pest`, `capturedAtGrowthStage`, `GrowthStage` | Stem borer damage type is stage-dependent; the KG must tie damage symptom, pest and phenology together in the image record. |
| CQ-IMG-05 | For images captured in the same field on consecutive capture dates, how does the mean annotated severity score of rice blast change over time? | C | `Image`, `capturedIn`, `Field`, `captureDate`, `hasSeverityScore`; grouping by field and date, temporal ordering, averaging | Supports disease-progression monitoring from imagery alone, a prerequisite for intervention timing. |
| CQ-IMG-06 | Which images from the same plot received different disease labels from different annotators, and what confidence did each annotator assign? | C | `Image`, `hasAnnotation`, `Annotation`, `annotatedBy`, `Annotator`, `labelsDisease`, `hasConfidence`, `capturedIn`, `Plot`; detection of label disagreement | Annotation quality and inter-annotator disagreement must be queryable for dataset curation and uncertainty-aware diagnosis. |

### 2c. Sensor/environmental-grounded CQs (5)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What was the daily mean relative humidity recorded by a given sensor node in a given field during a specified week? | S | `Sensor`/`Platform` (SOSA), `hostedIn`, `Field`, `madeObservation`, `Observation`, `observedProperty` (RH), `hasResult`, `resultTime`; daily aggregation | Baseline retrieval of environmental observations by location and time. |
| CQ-ENV-02 | Which fields recorded five or more consecutive days with leaf-wetness duration above 10 hours and night-time temperature between 20 °C and 28 °C in a given month? | R | `Field`, `Observation` (leaf wetness, temperature), `resultTime`, `EnvironmentalCondition`, `ConduciveWindow`; consecutive-day pattern detection | Identifies blast-conducive microclimate windows directly from sensor data. |
| CQ-ENV-03 | Which sensor nodes recorded cumulative rainfall above 100 mm in any 7-day window this season, and in which fields and districts are they located? | R | `Sensor`, `Observation` (rainfall), `hostedIn`, `Field`, `locatedIn`, `District` (GeoSPARQL), sliding-window summation | Heavy rainfall drives bacterial leaf blight spread and physical damage; spatial grouping enables district-level alerts. |
| CQ-ENV-04 | For each field, how many days per cropping season fell within the brown-planthopper-favourable envelope (air temperature 25–30 °C and RH > 80 %)? | C | `Field`, `Observation`, `CroppingSeason`, `EnvironmentalEnvelope`, `hasThreshold`; per-field per-season counting | Produces a seasonal exposure index for pest pressure comparable across fields. |
| CQ-ENV-05 | Which fields experienced a soil-moisture decline of more than 30 % relative to the seasonal mean coinciding with a temperature spike above the 90th percentile during the reproductive stage? | C | `Field`, `Observation` (soil moisture, temperature), `SeasonalBaseline`, `Anomaly`, `atGrowthStage`, `GrowthStage`; derived statistics | Abiotic stress events predispose plants to disease and must be detectable as derived indicators in the KG. |

### 2d. Genomic/tabular-grounded CQs (5)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which resistance genes (e.g., Xa4, xa5, Xa21) does variety IRBB21 carry, and against which pathogen does each confer resistance? | S | `Variety`, `carriesGene`, `ResistanceGene`, `confersResistanceTo`, `Pathogen` (align: Crop Ontology, Gramene/Oryzabase identifiers) | Basic genotype-to-resistance lookup needed for variety recommendation. |
| CQ-GEN-02 | What are the recorded maturity duration and mean grain yield of variety Ciherang in a given trial dataset? | S | `Variety`, `hasTraitValue`, `TraitValue`, `ofTrait`, `Trait` (align: Plant Trait Ontology), `measuredIn`, `Trial` | Agronomic performance must be retrievable alongside resistance data for trade-off decisions. |
| CQ-GEN-03 | Which varieties carry at least one Pi gene effective against the *Magnaporthe oryzae* races or lineages recorded in the study region? | R | `Variety`, `carriesGene`, `ResistanceGene`, `effectiveAgainst`, `PathogenRace`/`Lineage`, `recordedIn`, `Region` | Resistance is race-specific; the KG must model pathogen population structure, not only species. |
| CQ-GEN-04 | Which varieties carrying Bph genes were released after 2010 and are registered in the national variety catalogue of a given country? | R | `Variety`, `carriesGene`, `ResistanceGene` (Bph), `releaseYear`, `registeredIn`, `VarietyCatalogue`, `Country` | Practical recommendations must be restricted to varieties that farmers can legally and practically obtain. |
| CQ-GEN-05 | Rank varieties by mean yield across trials in which they were scored as resistant (score ≤ 3 on the SES scale) to sheath blight. | C | `Variety`, `Trial`, `hasDiseaseScore`, `DiseaseScore`, `ofDisease`, `hasYield`; filtering, grouping, averaging, ordering | Combines resistance phenotype and yield to support variety selection under disease pressure. |

### 2e. Cross-modal / fusion CQs (14)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 | Which images show symptoms whose annotated visual features match the textual diagnostic description of neck blast in the literature? (Text × Image) | R | `Document`, `describesSymptom`, `Symptom`, `hasDiagnosticFeature`; `Image`, `hasVisualFeature`; `matches`/`correspondsTo` alignment between `DiagnosticFeature` and `VisualFeature` | Validates that textual symptom knowledge and visual annotations share a common feature vocabulary. |
| CQ-MM-02 | Which extension-report management recommendations apply to the pest identified in a given damage image? (Text × Image) | R | `Image`, `hasAnnotation`, `labelsPest`, `Pest`, `controlledBy`, `ManagementPractice`, `recommendedIn`, `Document` | Turns a visual identification into actionable advice—the core extension-worker use case. |
| CQ-MM-03 | For images annotated as bacterial leaf blight captured in a given field on a given date, what were the mean temperature, RH and cumulative rainfall during the 14 days preceding capture? (Image × Sensor) | R | `Image`, `capturedIn`, `Field`, `captureDate`; `Sensor`, `hostedIn`, `Field`, `Observation`, `resultTime`; temporal window join | Attaches microclimatic context to visual diagnoses, enabling environment-conditioned interpretation. |
| CQ-MM-04 | Which varieties carrying Pi resistance genes nonetheless appear in images annotated with rice blast lesions of moderate or higher severity, suggesting resistance breakdown? (Image × Genomic) | C | `Image`, `depicts`, `PlantSpecimen`, `ofVariety`, `Variety`, `carriesGene`, `ResistanceGene`, `confersResistanceTo`, `Disease`; `labelsDisease`, `hasSeverityScore`; contradiction detection | Detects resistance erosion in the field—critical for breeders and pathologists. |
| CQ-MM-05 | Which varieties lacking any Bph gene are planted in fields whose sensors recorded brown-planthopper-favourable conditions for more than 20 days this season? (Sensor × Genomic) | R | `Field`, `plantedWith`, `Variety`, `carriesGene` (absence), `Observation`, `EnvironmentalEnvelope`, `CroppingSeason` | Identifies fields at combined genetic and environmental risk for targeted scouting. |
| CQ-MM-06 | Which environmental thresholds for green leafhopper (tungro vector) activity stated in the literature were exceeded in a given field during the vegetative stage? (Text × Sensor) | R | `Document`, `statesThreshold`, `EnvironmentalThreshold`, `forOrganism`, `Vector`; `Observation`, `exceeds`, `atGrowthStage` | Operationalises published thresholds as executable rules over live sensor streams. |
| CQ-MM-07 | Which resistance genes reported in the literature as overcome by Xoo pathotypes present in the region are carried by varieties released nationally? (Text × Genomic) | R | `Document`, `reportsVirulence`, `PathogenRace`, `overcomesGene`, `ResistanceGene`; `Variety`, `carriesGene`, `registeredIn`, `Country` | Flags varieties whose resistance is no longer reliable in the target region. |
| CQ-MM-08 | Given a leaf image annotated with elongated grey-centred lesions and sensor readings of 26 °C mean temperature and RH above 90 %, which disease is most likely, and which varieties in the KG carry resistance genes against it? (Image × Sensor × Genomic) | C | `VisualFeature`, `indicativeOf`, `Disease`; `EnvironmentalCondition`, `favours`, `Disease`; `Variety`, `carriesGene`, `confersResistanceTo`; scoring/ranking of candidate diseases | The canonical fusion query: diagnosis from combined evidence followed by a management recommendation. |
| CQ-MM-09 | For each outbreak confirmed in a surveillance report, which images and which sensor observations were recorded in the same field within ±7 days of the reported date? (Text × Image × Sensor) | C | `SurveillanceReport`, `reportsOccurrence`, `OccurrenceRecord`, `inLocation`, `Field`, `reportDate`; `Image`, `captureDate`; `Observation`, `resultTime`; spatio-temporal join | Assembles multimodal case files around confirmed events for retrospective analysis and model training. |
| CQ-MM-10 | Which combination of environmental conditions in the 10 days before the first blast-positive image best discriminates fields that developed blast from fields that did not, based on historical image annotations and confirmed diagnoses? (Image × Sensor, temporal/causal) | C | `Field`, `Image`, `labelsDisease`, `captureDate` (first positive), `Observation`, `resultTime`, `DiagnosisRecord`, `confirmedBy`; comparative aggregation across positive/negative cohorts | Supports data-driven derivation of predictive thresholds rather than relying only on literature values. |
| CQ-MM-11 | In variety-trial plots, how does image-derived blast severity relate to recorded grain yield, grouped by the resistance genes each variety carries? (Image × Genomic × Tabular) | C | `Plot`, `plantedWith`, `Variety`, `carriesGene`; `Image`, `capturedIn`, `Plot`, `hasSeverityScore`; `Trial`, `hasYield`; grouping and correlation | Links visual disease burden to yield loss and genotype—the evidence base for quantifying resistance value. |
| CQ-MM-12 | Which images annotated with a given disease were captured under environmental conditions the literature classifies as non-conducive for that disease, indicating possible mis-annotation or an alternative inoculum source? (Text × Image × Sensor) | C | `Document`, `statesThreshold`, `EnvironmentalThreshold`, `forDisease`; `Image`, `labelsDisease`, `capturedIn`, `captureDate`; `Observation`; negation of threshold satisfaction | Uses cross-modal consistency checking to improve annotation quality and surface anomalous cases. |
| CQ-MM-13 | Which varieties recommended in extension reports for a given province carry resistance to the diseases whose conducive conditions have been observed by that province's sensors in the current season? (Text × Genomic × Sensor) | C | `Document`, `recommendsVariety`, `Variety`, `forRegion`, `Province`; `carriesGene`, `confersResistanceTo`, `Disease`; `Observation`, `EnvironmentalEnvelope`, `favours`, `Disease` | Produces season-specific, region-specific variety advice that is both officially recommended and environmentally justified. |
| CQ-MM-14 | Rank the monitored fields by sheath-blight outbreak risk, combining (i) the planted variety's disease score from trial tables, (ii) the number of days this season within the literature-derived conducive envelope, and (iii) the severity of any sheath-blight annotations in images from the last 14 days. (Text × Image × Sensor × Genomic/Tabular) | C | `Field`, `plantedWith`, `Variety`, `hasDiseaseScore`; `Observation`, `EnvironmentalThreshold` (from `Document`), `ConduciveWindow`; `Image`, `hasSeverityScore`; `RiskScore`, `derivedFrom`; weighted aggregation and ordering | The four-way integration query that a precision-agriculture dashboard would issue; demonstrates the full value of the multimodal KG. |

---

## 3. Modality-Pair Coverage Table

| Modality combination | CQ IDs | Count |
|---|---|---|
| Text only | CQ-TXT-01 – CQ-TXT-06 | 6 |
| Image only | CQ-IMG-01 – CQ-IMG-06 | 6 |
| Sensor only | CQ-ENV-01 – CQ-ENV-05 | 5 |
| Genomic/tabular only | CQ-GEN-01 – CQ-GEN-05 | 5 |
| Text × Image | CQ-MM-01, CQ-MM-02 | 2 |
| Image × Sensor | CQ-MM-03, CQ-MM-10 | 2 |
| Image × Genomic/Tabular | CQ-MM-04 | 1 |
| Sensor × Genomic/Tabular | CQ-MM-05 | 1 |
| Text × Sensor | CQ-MM-06 | 1 |
| Text × Genomic/Tabular | CQ-MM-07 | 1 |
| Image × Sensor × Genomic | CQ-MM-08 | 1 |
| Text × Image × Sensor | CQ-MM-09, CQ-MM-12 | 2 |
| Image × Genomic × Tabular | CQ-MM-11 | 1 |
| Text × Genomic × Sensor | CQ-MM-13 | 1 |
| Four-way (Text × Image × Sensor × Genomic/Tabular) | CQ-MM-14 | 1 |
| **Total** | | **36** |

Distribution: text 16.7 %, image 16.7 %, sensor 13.9 %, genomic/tabular 13.9 %, cross-modal 38.9 %—within the target ranges. Every pairwise combination of the four modalities is exercised by at least one CQ; Text × Genomic × Image (without sensor) is the only three-way combination not directly covered and may be added if literature-to-genotype-to-image validation becomes a priority.

Complexity distribution: Simple 9, Relational 15, Complex-Inferential 12.

---

## 4. Scope Boundary Note

**In scope.** The KG covers the major fungal, bacterial, viral and insect pests of lowland irrigated rice in Southeast Asia; their causal agents, vectors, races/pathotypes, symptoms and diagnostic features with document provenance; annotated field imagery linked to plant part, growth stage, variety, field, date, severity and annotator; IoT-observed agroclimatic variables and derived conducive windows and anomalies at field and district granularity; and variety-level resistance genes, trial disease scores and yield. The ontology must therefore support spatio-temporal alignment (field, plot, date) as the primary integration axis, a shared symptom/visual-feature vocabulary bridging text and image, and literature-derived environmental thresholds encoded as executable constraints. **Out of scope** are pathogen molecular biology below the race/gene level (e.g., effector sequences), pest population dynamics modelling, economic optimisation of interventions, post-harvest storage pests, and non-rice hosts, none of which are required by any CQ above.

**Feasibility flags.** CQ-IMG-06 requires multi-annotator labelling, which many image datasets lack. CQ-ENV-05 and CQ-MM-10 depend on multi-season sensor history with co-located confirmed diagnoses, which is rarely available at launch. CQ-GEN-03 and CQ-MM-07 require regional pathogen race/pathotype surveys, which may be incomplete or outdated. CQ-MM-14 presupposes an agreed risk-weighting scheme that is a modelling decision rather than a KG fact; it should be treated as a target for later iterations. These CQs should be retained as requirements but revisited once data availability is confirmed.
