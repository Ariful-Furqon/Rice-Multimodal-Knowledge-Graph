# Competency Questions for a Multimodal Knowledge Graph of Rice Pests and Diseases

*Ontology Requirements Specification — Competency Questions*

---

## 0. Assumptions (defaults applied to unfilled input fields)

Because the input fields of the prompt were left as placeholders, the following defaults were adopted. Each is marked with an identifier so it can be revised before the CQs are finalised.

- **[A1] End users.** Plant pathology researchers, agricultural extension officers, rice breeders, and developers of smart-farming/IoT decision-support systems.
- **[A2] Geographic and agroecological scope.** Irrigated and rainfed tropical lowland rice in Indonesia and wider Southeast Asia, with two cropping seasons per year (wet season and dry season).
- **[A3] Pests and diseases in scope.** Rice blast (*Pyricularia oryzae*, syn. *Magnaporthe oryzae*); bacterial leaf blight (*Xanthomonas oryzae* pv. *oryzae*, Xoo); sheath blight (*Rhizoctonia solani* AG1-IA); rice tungro disease (rice tungro bacilliform virus and rice tungro spherical virus, vectored by the green leafhopper *Nephotettix virescens*); brown spot (*Bipolaris oryzae*); brown planthopper (*Nilaparvata lugens*); yellow stem borer (*Scirpophaga incertulas*); rice leaffolder (*Cnaphalocrocis medinalis*); and rice bug (*Leptocorisa oratorius*). Common abiotic disorders (e.g., nitrogen or zinc deficiency) are included only as differential diagnoses.
- **[A4] Data sources (illustrative).**
  *Text:* peer-reviewed literature, the IRRI Rice Knowledge Bank, the CABI Crop Protection Compendium, and national pest surveillance and forecasting bulletins.
  *Image:* public labelled rice disease image datasets, supplemented by geo-referenced, time-stamped field images captured by smartphone and UAV.
  *Sensor:* in-field IoT stations (air temperature, relative humidity, rainfall, leaf wetness, wind, soil moisture, soil pH), national meteorological agency records, and automated insect light traps.
  *Genomic/tabular:* 3,000 Rice Genomes Project data (via SNP-Seek), RAP-DB gene models on the IRGSP-1.0 reference, Oryzabase, QTL databases, national variety release descriptions, and multi-location yield trial records.
- **[A5] Target number of CQs.** 40.
- **[A6] Ontology alignment.** No existing schema is assumed. Candidate alignment targets are flagged inline with "→" (e.g., → SOSA). Note that the acronym **PPO** in the prompt refers to the *Plant Phenology Ontology*, not a plant phenotype ontology; phenotype and trait terms are better aligned with the **Plant Trait Ontology (TO)**, the **Crop Ontology rice trait dictionary (CO_320)**, and **PATO**.
- **[A7] Pre-existing CQs.** None supplied; no de-duplication against prior drafts was performed.
- **[A8] Measurement conventions.** Disease severity follows the IRRI Standard Evaluation System (SES, 0–9 scale); growth stages follow IRRI stage codes or the BBCH scale for rice.

**Notation.** † marks a CQ with a data-availability or feasibility risk, discussed in Section 4. Class and property names in the "Key Entities & Relations" column are proposed working names, not final ontology IRIs.

---

## 1. Purpose and Scope (for confirmation)

The Rice Pest and Disease Multimodal Knowledge Graph (RiceMMKG) aims to support early diagnosis of, and evidence-based decision-making about, major biotic stresses of tropical lowland rice by semantically integrating textual domain knowledge, field images, agroclimatic sensor observations, and varietal genomic and agronomic records. Its intended users are plant pathologists, extension officers, breeders, and precision-agriculture systems, who require answers that are traceable to their source evidence. The competency questions below define the entities and relations the KG must represent, the cross-modal alignments it must support, and the queries against which it will be evaluated.

---

## 2. Competency Questions

### 2.1 Text-grounded CQs (7 CQs; 17.5%)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal agent of rice bacterial leaf blight, and what is its full taxonomic lineage down to species and pathovar? | Simple | `Disease`, `hasCausalAgent`, `Pathogen`, `taxonomicParent`, `pathovar` (→ NCBITaxon, AGROVOC) | Establishes the disease–pathogen backbone to which all other modalities ultimately link. |
| CQ-TXT-02 | Which viruses cause rice tungro disease, which leafhopper species are reported to transmit them, and in which transmission mode? | Relational | `Disease`, `hasCausalAgent`, `Virus`, `transmittedBy`, `Vector`, `transmissionMode` (→ NCBITaxon, IDO) | Vector-borne diseases require explicit vector modelling because management often targets the vector rather than the pathogen. |
| CQ-TXT-03 | What symptoms are described for the neck (panicle) blast phase of rice blast, on which plant organ do they occur, and at which growth stage? | Simple | `Disease`, `hasSymptom`, `Symptom`, `occursOn` `PlantStructure` (→ PO), `occursAtStage` `GrowthStage` (→ PO, BBCH) | Organ- and stage-specific symptom descriptions are the textual anchors against which images are later validated. |
| CQ-TXT-04 | Which control measures are recommended for brown planthopper in extension sources, and which of those measures are reported to induce pest resurgence when misapplied? | Relational | `ManagementPractice`, `recommendedFor`, `Pest`, `hasAdverseOutcome`, `Resurgence`, `statedIn` `Document` (→ PROV-O, AGROVOC) | Decision support must represent contraindications as well as recommendations, so that advice does not aggravate outbreaks. |
| CQ-TXT-05 | Which diseases and pests are reported to be aggravated by high nitrogen fertilisation, and what mechanism is cited for each? | Relational | `Disease` / `Pest`, `aggravatedBy`, `AgronomicFactor`, `hasProposedMechanism`, `supportedBy` `Document` | Links agronomic practice to biotic risk, a core explanatory relation in integrated crop management. |
| CQ-TXT-06 † | For each disease in scope, which relative-humidity and temperature ranges favouring infection are reported across sources, how many independent sources support each range, and where do the reported values conflict? | Complex | `Claim` (nanopublication-style), `assertsFavourableRange`, `EnvironmentalVariable`, `minValue` / `maxValue`, `unit` (→ UO, QUDT), `source`, `conflictsWith` | Literature thresholds are later operationalised against sensor data (CQ-MM-04, -08, -10), so their provenance and consistency must be queryable. |
| CQ-TXT-07 † | Which provinces reported the largest cumulative area affected by yellow stem borer in national surveillance bulletins in each wet and dry season of the past five years, ranked in descending order? | Complex | `SurveillanceReport`, `reportsInfestation`, `Pest`, `affectedArea` (ha), `AdministrativeUnit` (→ GADM, GeoNames), `Season`, `temporalCoverage` (→ OWL-Time) | Historical spatio-temporal outbreak records supply the ground truth for evaluating early-warning reasoning. |

### 2.2 Image-grounded CQs (7 CQs; 17.5%)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Which images are annotated as depicting rice blast leaf lesions, and at which growth stage was each image captured? | Simple | `Image`, `hasAnnotation`, `diagnosisLabel` → `Disease`, `capturedAtStage` `GrowthStage` | Retrieval of labelled visual evidence per disease is the foundation of image-based diagnosis. |
| CQ-IMG-02 | Which plant organ does a given image depict, and is the depicted plant annotated as healthy or symptomatic? | Simple | `Image`, `depictsStructure` (→ PO), `hasHealthStatus` {Healthy, Symptomatic} | Healthy-plant baselines are needed as negative evidence for both diagnosis and classifier evaluation. |
| CQ-IMG-03 | Which images contain annotated regions showing spindle-shaped lesions with grey centres and brown margins, and which disease labels were assigned to those regions by expert annotators as opposed to automated classifiers? | Relational | `Image`, `hasRegion` (→ W3C Web Annotation selectors), `hasVisualFeature` (`LesionShape`, `LesionColour`), `annotatedBy` `Agent` {Expert, Model}, `confidence` | Separating human from machine provenance is essential for trust and for measuring model–expert agreement. |
| CQ-IMG-04 | Which pairs of diagnostic classes, including abiotic disorders such as nitrogen or zinc deficiency, share one or more annotated visual features and are therefore flagged as visually confusable (e.g., brown spot versus early blast lesions)? | Relational | `DiagnosticClass`, `exhibitsFeature` `VisualFeature`, `confusableWith` (symmetric) | Explicit confusability links support differential diagnosis and indicate when additional, non-visual evidence is required. |
| CQ-IMG-05 | Which images show hopperburn, and for each, what was the capture platform (UAV, smartphone, or fixed camera) and the spatial scale (canopy, hill, or organ)? | Relational | `Image`, `depicts` `DamageSymptom` (Hopperburn), `acquiredBy` `Platform` (→ SOSA), `spatialScale` | Some damage types are recognisable only at canopy scale, so scale and platform determine which images constitute valid evidence. |
| CQ-IMG-06 | What is the distribution of expert-assigned SES severity scores (0–9) across images labelled with bacterial leaf blight, grouped by growth stage? | Complex | `Image`, `hasSeverityScore` (SES scale), `diagnosisLabel`, `capturedAtStage`, aggregation (COUNT, GROUP BY) | Severity distributions reveal dataset bias, such as over-representation of late-stage symptoms, that limits early diagnosis. |
| CQ-IMG-07 † | Which images carry conflicting diagnosis labels from two or more annotators, and what is the level of inter-annotator agreement for each diagnostic class? | Complex | `Annotation`, `annotatesImage`, `annotatedBy`, `diagnosisLabel`, derived `agreementScore` (agreement statistic computed post-query) | Class-level label reliability must be known before image evidence is weighted in cross-modal inference. |

### 2.3 Sensor/Environmental-grounded CQs (5 CQs; 12.5%)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What were the daily mean air temperature, mean relative humidity, cumulative rainfall, and mean volumetric soil moisture recorded at field station S on date D? | Simple | `sosa:Observation`, `madeBySensor`, `observedProperty`, `hasResult`, `resultTime`, `hasFeatureOfInterest` `FieldPlot` (→ SOSA/SSN, QUDT, OWL-Time) | A point lookup of agroclimatic state is the atomic operation underlying all environmental reasoning. |
| CQ-ENV-02 | Which sensors are hosted at field plot P, which properties does each observe, at what sampling interval, and when was each last calibrated? | Simple | `sosa:Sensor`, `isHostedBy` `Platform`, `observes` `ObservableProperty`, `samplingInterval`, `lastCalibrationDate` (→ SSN) | Sensor metadata determines which environmental questions can be answered for a given plot, and with what reliability. |
| CQ-ENV-03 | Which field stations recorded, on the same night, a mean relative humidity of at least 90% together with a mean air temperature between 22 °C and 28 °C during month M? | Relational | Two `Observation`s with `observedProperty` {RelativeHumidity, AirTemperature}, shared `FeatureOfInterest`, `resultTime` within a night `Interval` | Conjunctive, time-aligned conditions across properties are the basic pattern for defining disease-favourable weather windows. |
| CQ-ENV-04 | For each station, how many periods of three or more consecutive days with daily rainfall above 20 mm occurred during the last wet season, and what was the longest such period? | Complex | `Observation`, `dailyRainfall`, `Interval`, `intervalMeets` (→ OWL-Time), derived `WetSpellEvent` materialised at ingestion, aggregation | Persistent wet spells are a recognised driver of bacterial and fungal disease spread, so run-length temporal patterns must be computable. |
| CQ-ENV-05 | Which sensor time series contain gaps longer than six hours, physically implausible values (e.g., relative humidity above 100%), or flat-lined readings persisting for more than 24 hours, and over which intervals? | Complex | `Observation`, `qualityFlag` (→ W3C DQV), derived `DataGap`, `Interval`, `ObservableProperty` | Automated quality screening prevents faulty readings from propagating into diagnostic or predictive inferences. |

### 2.4 Genomic/Tabular-grounded CQs (6 CQs; 15%)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which blast resistance (*Pi*) genes are documented as being carried by a given variety (e.g., IR64)? | Simple | `Variety` (→ CO_320), `carriesGene`, `ResistanceGene`, `confersResistanceTo` `Disease` | Variety–gene lookup is the most frequent genomic query in varietal recommendation. |
| CQ-GEN-02 | On which chromosome and at which physical coordinates on the IRGSP-1.0 reference is the resistance gene *Xa21* located, what are its RAP-DB and MSU identifiers, and what class of protein does it encode? | Simple | `Gene`, `locatedOn` `Chromosome`, `hasLocation` (→ FALDO), `hasIdentifier`, `encodes` `Protein`, `proteinClass` (→ SO, GO) | Genomic coordinates enable interoperability with external rice genome resources and support marker design. |
| CQ-GEN-03 | Which released varieties carry at least one brown planthopper resistance gene (e.g., *Bph3*, *Bph14*, *Bph17*, *Bph26*) and are also rated resistant or moderately resistant to bacterial leaf blight? | Relational | `Variety`, `carriesGene`, `ResistanceGene`, `targetsPest`, `hasResistanceRating` (→ TO, SES), `Disease` | Multi-stress resistance is the primary criterion when recommending varieties where pests and diseases co-occur. |
| CQ-GEN-04 | Which varieties with IR64 in their pedigree carry the *xa5* allele, and what is their mean grain yield (t/ha) across recorded multi-location yield trials? | Relational | `Variety`, `hasParent` (transitive), `carriesAllele`, `YieldTrial`, `grainYield`, `trialLocation` (→ TO, CO_320) | Linking pedigree, resistance alleles, and yield supports breeders' analyses of resistance–productivity trade-offs. |
| CQ-GEN-05 † | Which combinations of two or more *Xa* genes confer resistance to the greatest number of characterised Xoo races or pathotypes, ranked by the number of races resisted? | Complex | `GenePyramid`, `hasComponentGene`, `Pathotype`, `resistanceReaction` {R, MR, S}, aggregation and ranking | Gene pyramiding is a principal strategy for durable resistance, and ranking pyramids requires race-specific reaction data. |
| CQ-GEN-06 | Which QTLs for sheath blight resistance are reported, what proportion of phenotypic variance does each explain, and which varieties carry favourable alleles at two or more of them? | Complex | `QTL`, `associatedWithTrait` (→ TO), `phenotypicVarianceExplained`, `hasFlankingMarker`, `carriesAllele`, `Variety`, COUNT ≥ 2 | Because sheath blight lacks well-characterised major resistance genes, quantitative resistance must be modelled explicitly. |

### 2.5 Cross-modal / Fusion CQs (15 CQs; 37.5%)

Modality codes: **T** = Text, **I** = Image, **S** = Sensor/Environmental, **G** = Genomic/Tabular.

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 (T×I) | For a given image, which causal agent and expert-authored symptom description are linked to its diagnosis label, and from which source documents do they originate? | Simple | `Image`, `diagnosisLabel` `Disease`, `hasCausalAgent`, `hasSymptomDescription`, `wasDerivedFrom` `Document` (→ PROV-O) | Grounding every visual diagnosis in citable textual knowledge makes image-based outputs explainable. |
| CQ-MM-02 (T×I) | Which symptoms described in the literature as diagnostic for a disease are depicted by fewer than N expert-verified images in the KG? | Complex | `Symptom`, `describedIn` `Document`, `depictedBy` `Image`, `verifiedBy` Expert, COUNT < N | Identifies visual coverage gaps that should direct future image-collection campaigns. |
| CQ-MM-03 (I×S) | For each sheath blight image captured at plot P, what were the mean canopy relative humidity and air temperature recorded by co-located sensors during the seven days preceding image capture? | Relational | `Image`, `capturedAt` (→ GeoSPARQL), `captureTime`, `sosa:Observation`, `colocatedWith`, `precedingInterval` (→ OWL-Time) | Spatiotemporal alignment of images with sensor windows is the fundamental join operation of the multimodal KG. |
| CQ-MM-04 (T×S) | On which dates during the current season did sensor readings at station S satisfy the literature-reported favourable conditions for rice blast infection, in terms of leaf-wetness duration, relative humidity, and night temperature? | Relational | `Claim` `assertsFavourableRange` (from CQ-TXT-06), `EnvironmentalVariable` mapped to `ObservableProperty`, `Observation`, `resultTime`, range filters | Operationalises textual agronomic knowledge as machine-checkable rules over sensor streams, which requires an explicit mapping between text-derived and sensor-observed variables. |
| CQ-MM-05 (S×G) | Which varieties planted in plots that recorded at least five days with mean relative humidity above 90% during the booting stage showed a susceptible blast reaction in the associated field-trial records? | Complex | `FieldPlot`, `plantedWith` `Variety`, `Observation`, `CropStageInterval`, `FieldTrialRecord`, `hasReaction`, COUNT ≥ 5 | Reveals how varietal resistance performs under specific environmental pressure rather than in the abstract. |
| CQ-MM-06 (T×G) | Which resistance genes reported in the literature as having been overcome by pathogen populations in region R are carried by varieties that are still recommended for R in current extension bulletins? | Relational | `ResistanceGene`, `reportedBreakdownIn` `Region`, `Claim`, `Variety`, `carriesGene`, `recommendedFor` `Region`, `statedIn` `ExtensionBulletin` | Flags recommendations at risk of failure, directly supporting resistance-stewardship decisions. |
| CQ-MM-07 † (I×G) | For each variety, what proportion of its geo-referenced field images show blast symptoms, and how does this proportion vary with the number of *Pi* genes the variety carries? | Complex | `Image`, `depictsPlantOf` `Variety` (via `FieldPlot`), `diagnosisLabel`, `carriesGene`, aggregation | Provides field-level visual evidence to validate or challenge genotype-based expectations of resistance. |
| CQ-MM-08 (T×I×S) | Given a new leaf image classified as showing spindle-shaped lesions, together with the preceding five days of sensor readings from the same plot, which candidate diseases are consistent with both the visual features and the literature-reported favourable environmental ranges, ranked by the number of criteria satisfied? | Complex | `Image`, `hasVisualFeature`, `VisualFeature` `indicativeOf` `Disease`, `Claim` `assertsFavourableRange`, `Observation`, ranking | This flagship early-diagnosis query demonstrates that fused evidence narrows the differential diagnosis beyond what any single modality achieves. |
| CQ-MM-09 † (T×I×S×G) | Given an image from plot P showing yellow-orange leaf discolouration with stunting, automated light-trap counts of green leafhopper at P over the preceding 14 days, and the tungro resistance rating of the planted variety, how many evidence items support rice tungro disease compared with a literature-listed abiotic differential diagnosis such as nitrogen deficiency? | Complex | `Image`, `hasVisualFeature`, `confusableWith`, `DifferentialDiagnosis` (text), `InsectTrapObservation` (→ SOSA), `Vector`, `Variety` `hasResistanceRating`, evidence tally per candidate | Tests the KG's ability to combine all four modalities to disambiguate a visually confusable, vector-borne disease. |
| CQ-MM-10 (T×S×G) | Given the environmental conditions recorded in region R during the current season, which diseases have their literature-reported favourable ranges met, and which varieties both carry resistance to those diseases and are recommended for R in extension sources? | Complex | `Observation`, `Region`, `Claim` `assertsFavourableRange`, `Disease`, `ResistanceGene`, `Variety`, `recommendedFor` | Supports proactive, weather-informed varietal choice for the following planting. |
| CQ-MM-11 (I×S) | Across all geo-referenced images with confirmed hopperburn, what were the mean air temperature and relative humidity in the 30 days before capture, and how do these values compare with the same periods at plots imaged without hopperburn? | Complex | `Image`, `depicts` Hopperburn, `hasHealthStatus`, `FieldPlot`, `Observation`, AVG, case–control grouping | Provides locally grounded empirical evidence on the environmental drivers of planthopper outbreaks. |
| CQ-MM-12 † (T×I×S) | Which combinations of environmental conditions in the ten days preceding blast outbreaks that were both image-verified and reported in surveillance bulletins recur most frequently across seasons? | Complex | `OutbreakEvent`, `confirmedBy` `Image`, `reportedIn` `SurveillanceReport`, `Observation`, discretised `ConditionPattern` materialised at ingestion, COUNT, ORDER BY | Mines historical multimodal evidence to derive candidate early-warning rules for outbreak forecasting. |
| CQ-MM-13 † (I×S×G) | Following storm events (defined by user-set thresholds, e.g., wind gusts above 15 m/s with daily rainfall above 50 mm), is the image-based bacterial leaf blight severity (SES score) higher in varieties carrying only *Xa4* than in varieties carrying pyramided *Xa* genes? | Complex | derived `WeatherEvent` (from `Observation`), `Image`, `hasSeverityScore`, `FieldPlot`, `Variety`, `carriesGene`, AVG by group | Tests whether gene pyramiding confers practical protection under wound-inducing weather that favours Xoo entry. |
| CQ-MM-14 (T×I×G) | For the pest or disease diagnosed in a given image, which management practices are recommended at the observed severity or damage level, which literature-reported action thresholds are exceeded, and how does the planted variety's resistance status modify the recommendation? | Relational | `Image`, `diagnosisLabel`, `hasSeverityScore`, `ActionThreshold`, `ManagementPractice` `recommendedFor`, `applicableWhen`, `Variety` `carriesGene` | Converts a diagnosis into actionable, context-sensitive advice for extension officers. |
| CQ-MM-15 (T×I×S×G) | For a diagnosis of rice blast at plot P on date D, which KG assertions from each modality (image features, preceding sensor conditions, variety resistance profile, and literature claims) support or contradict the diagnosis, and what is the provenance of each assertion? | Complex | `Diagnosis`, `supportedBy` / `contradictedBy` `EvidenceItem`, `hasModality`, `wasDerivedFrom`, `wasAttributedTo` (→ PROV-O) | Delivers an auditable, explainable evidence chain, which is the principal justification for a multimodal KG over siloed databases. |

### 2.6 Distribution Summary

| Category | Count | Share | Simple | Relational | Complex-Inferential |
|---|---|---|---|---|---|
| Text (TXT) | 7 | 17.5% | 2 | 3 | 2 |
| Image (IMG) | 7 | 17.5% | 2 | 3 | 2 |
| Sensor/Environmental (ENV) | 5 | 12.5% | 2 | 1 | 2 |
| Genomic/Tabular (GEN) | 6 | 15.0% | 2 | 2 | 2 |
| Cross-modal (MM) | 15 | 37.5% | 1 | 4 | 10 |
| **Total** | **40** | **100%** | **9** | **13** | **18** |

---

## 3. Modality-Pair Coverage (Traceability)

The second column lists every cross-modal CQ that exercises a given combination, including higher-order CQs that subsume it. The third column lists CQs that exercise *exactly* that combination and no other modality.

| Modality combination | All CQs exercising it | Exactly this combination |
|---|---|---|
| Text × Image | MM-01, MM-02, MM-08, MM-09, MM-12, MM-14, MM-15 | MM-01, MM-02 |
| Text × Sensor | MM-04, MM-08, MM-09, MM-10, MM-12, MM-15 | MM-04 |
| Text × Genomic | MM-06, MM-09, MM-10, MM-14, MM-15 | MM-06 |
| Image × Sensor | MM-03, MM-08, MM-09, MM-11, MM-12, MM-13, MM-15 | MM-03, MM-11 |
| Image × Genomic | MM-07, MM-09, MM-13, MM-14, MM-15 | MM-07 |
| Sensor × Genomic | MM-05, MM-09, MM-10, MM-13, MM-15 | MM-05 |
| Text × Image × Sensor | MM-08, MM-09, MM-12, MM-15 | MM-08, MM-12 |
| Text × Image × Genomic | MM-09, MM-14, MM-15 | MM-14 |
| Text × Sensor × Genomic | MM-09, MM-10, MM-15 | MM-10 |
| Image × Sensor × Genomic | MM-09, MM-13, MM-15 | MM-13 |
| Text × Image × Sensor × Genomic | MM-09, MM-15 | MM-09, MM-15 |

**Coverage observations.** Every one of the six modality pairs is exercised by at least five CQs, and every three-way combination by at least one dedicated CQ, so no pairing is untested. The thinnest areas are the dedicated Text × Sensor, Text × Genomic, Image × Genomic, and Sensor × Genomic pairings (one CQ each), and each three-way combination other than Text × Image × Sensor. If the evaluation design requires balanced coverage, these are the first places to add CQs.

---

## 4. Scope Boundary Note

**Scope statement.** On the basis of the CQs above, the RiceMMKG is in scope for representing the causal agents, vectors, symptoms, and damage types of the named rice pests and diseases (with abiotic disorders only as differential diagnoses); expert- and machine-annotated RGB field images with their capture context and severity scores; time-stamped, geo-located agroclimatic and insect-trap observations with quality metadata; and varietal pedigree, resistance genes, QTLs, pathotype reactions, and yield-trial records, all linked through shared field plots, time intervals, and provenance-bearing claims. It is out of scope for pesticide chemistry and formulation, market and economic data, crops other than rice, pathogen genome sequences beyond race or pathotype identity, and hyperspectral or multispectral remote-sensing products. The KG stores the inputs and outputs of predictive and machine-learning models, together with their provenance, but not the models themselves. Statistical inference (e.g., significance testing in CQ-MM-13 or agreement statistics in CQ-IMG-07) is performed on query results outside the KG; the KG's obligation is to return the correctly grouped evidence.

**Feasibility flags.** The following CQs may be infeasible with currently available data and should be revisited once data sources are confirmed.

| CQ(s) | Risk | Possible mitigation |
|---|---|---|
| TXT-06; dependent MM-04, MM-08, MM-10 | Requires claim-level extraction of quantitative thresholds with units and provenance, which is error-prone from unstructured text. | Curate thresholds manually for the diseases in scope; use NLP extraction with expert validation. |
| TXT-07 | Surveillance bulletins may be available only as PDFs in the national language, with inconsistent units and administrative boundaries. | Parse a limited historical window first; normalise to a single administrative gazetteer. |
| IMG-07 | Most public image datasets carry a single label per image, so inter-annotator disagreement is not observable. | Commission multi-annotator labelling on a stratified subset. |
| GEN-05 | Race- and pathotype-specific reaction data for Xoo are sparse and region-specific. | Restrict to pathotypes characterised in the target region; report coverage explicitly. |
| MM-07, MM-09, MM-11, MM-12, MM-13 | Require geo-referenced, time-stamped images linked to the planted variety and to co-located sensors; public image datasets generally lack this metadata. | A dedicated field campaign with synchronised image capture, IoT stations, and plot-level variety records. |
| MM-09 | Automated insect light traps are not widely deployed. | Accept manual trap counts as `InsectTrapObservation` with an explicit method attribute. |
| ENV-04, ENV-05, MM-12, MM-13 | Run-length and pattern detection are cumbersome in pure SPARQL. | Materialise derived events (`WetSpellEvent`, `DataGap`, `WeatherEvent`, `ConditionPattern`) during ingestion and query those. |
