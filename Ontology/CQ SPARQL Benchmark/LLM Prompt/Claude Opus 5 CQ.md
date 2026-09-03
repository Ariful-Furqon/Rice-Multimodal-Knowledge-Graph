# Ontology Requirements Specification: Competency Questions for a Multimodal Knowledge Graph on Rice Pests and Diseases

*Prepared following the competency-question (CQ) elicitation tradition of Grüninger & Fox (1995) and Uschold & King (1995), the NeOn Methodology's Ontology Requirements Specification Document (ORSD) template, and CQ-pattern/SPARQL-verification guidance (Ren et al.; Bezerra et al.).*

---

## 0. Assumptions Adopted

The source specification left several input fields as bracketed placeholders. The following defaults have been adopted and are **explicitly flagged as assumptions**; each should be confirmed or overridden before the CQ set is frozen as a requirements baseline.

| Field | Assumed value | Status |
|---|---|---|
| Primary end users | (i) Plant-pathology and breeding researchers, (ii) agricultural extension officers / field scouts, (iii) precision-agriculture and IoT system developers building decision-support services | **Assumption** |
| Geographic / agroecological scope | Indonesian and broader Southeast Asian tropical lowland irrigated and rainfed-lowland rice systems | **Assumption** |
| Pests/diseases in scope | Rice blast (*Pyricularia oryzae* / *Magnaporthe oryzae*), bacterial leaf blight (*Xanthomonas oryzae* pv. *oryzae*), sheath blight (*Rhizoctonia solani*), brown spot (*Bipolaris oryzae*), false smut (*Ustilaginoidea virens*), rice tungro disease (RTBV + RTSV, vectored by *Nephotettix virescens*), brown planthopper (*Nilaparvata lugens*), yellow stem borer (*Scirpophaga incertulas*), rice bug (*Leptocorisa oratorius*), plus healthy-plant baselines | **Assumption ("common major rice pests/diseases")** |
| Text sources | Peer-reviewed literature; IRRI Rice Knowledge Bank and equivalent extension material; national/provincial pest-surveillance bulletins (e.g., Ditlin/BBPOPT-style *laporan OPT*) | **Assumption** |
| Image sources | Field and close-up photographs with expert disease/pest labels and, where available, lesion-level region annotations; public benchmark sets of the Paddy Doctor / rice-leaf-disease type; healthy controls | **Assumption** |
| Sensor sources | Plot- or station-level IoT time series: air temperature, relative humidity, rainfall, leaf wetness, wind speed, soil moisture, soil pH; sub-daily to daily resolution | **Assumption** |
| Genomic / tabular sources | Released-variety registries (e.g., Inpari/IR/Ciherang series); curated resistance-gene records (*Pi*, *Xa*/*xa*, *Bph*, *qSB* loci; *tsv1*); genotype resources of the Rice SNP-Seek type; multi-location trial yield and agronomic tables | **Assumption** |
| Target number of CQs | **36** | **Assumption (default range 30–40)** |
| Ontologies to align with | AGROVOC, Crop Ontology (CO_320 rice), Plant Ontology (PO), Plant Trait Ontology (TO), Plant Phenology/Phenotype Ontology (PPO), Infectious Disease Ontology (IDO) patterns, NCBITaxon, ENVO, SOSA/SSN, PROV-O, Sequence Ontology / Gene Ontology, IAO | **Assumption ("none supplied")** |
| Pre-existing CQs to avoid duplicating | None supplied | — |

**Distribution actually produced:** Text-only 6 (16.7%), Image-only 6 (16.7%), Sensor-only 5 (13.9%), Genomic/tabular-only 5 (13.9%), Cross-modal/fusion 14 (38.9%).

---

## 1. Purpose and Scope (for confirmation)

The knowledge graph (KG) is intended to represent, and make jointly queryable, evidence about the major pests and diseases of tropical lowland rice by semantically integrating four modalities: textual scientific and extension knowledge, annotated field imagery of symptoms and damage, agroclimatic sensor time series, and tabular varietal/genotypic resistance data. Its purpose is to support early diagnosis, risk assessment, and varietal and management decision-making by plant-pathology researchers, extension officers, and developers of precision-agriculture systems. The competency questions below define the functional boundary of that KG: each is intended to be answerable, in principle, by a single formal (SPARQL or equivalent) query over the integrated graph, and the set as a whole constitutes both the design requirement for the ontology's classes and relations and the evaluation criterion against which the populated KG will be tested.

---

## 2. Competency Questions

### 2.a Text-Grounded Competency Questions

Answerable from assertions extracted from literature, extension material, and surveillance bulletins alone.

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal agent of rice blast, under which accepted taxonomic name and which recorded synonyms (e.g., *Magnaporthe oryzae* / *Pyricularia oryzae*), and to which pathogen type (fungus, bacterium, virus, insect) does it belong? | Simple | `Disease`, `causedBy`, `Pathogen`, `hasTaxonomicName`, `hasSynonym`, `hasPathogenType` (align: NCBITaxon, AGROVOC) | Establishes the minimal disease–pathogen backbone and the synonym handling without which literature, image labels, and gene records cannot be reconciled. |
| CQ-TXT-02 | Which symptoms are described for bacterial leaf blight, on which plant organs, and at which crop growth stages? | Simple | `Disease`, `hasSymptom`, `Symptom`, `manifestsOnPlantPart`, `PlantPart`, `observedAtGrowthStage`, `GrowthStage` (align: PO, PPO, TO) | Symptom–organ–stage triples are the anchor to which image annotations must later be aligned. |
| CQ-TXT-03 | Which control measures are recommended for brown planthopper, of which management category (chemical, biological, cultural, host resistance), at which growth stage, and in which source document? | Relational | `Pest`, `hasControlMeasure`, `ControlMeasure`, `hasManagementCategory`, `applicableAtGrowthStage`, `assertedIn`, `Document` (align: PROV-O, IAO) | Extension officers require actionable, source-attributable recommendations rather than descriptive facts alone. |
| CQ-TXT-04 | Which arthropod species are reported as vectors of which viral rice diseases, and by which transmission mode (persistent, semi-persistent, non-persistent)? | Relational | `Pest`, `isVectorOf`, `Disease`, `hasTransmissionMode`, `Pathogen` (align: IDO transmission patterns) | Vector-mediated diseases such as tungro cannot be modelled by a simple disease–pathogen link; this CQ forces an explicit vector relation. |
| CQ-TXT-05 | Which pairs of diseases share the largest number of textually described leaf symptoms, and what are the discriminating symptoms that separate each pair? | Complex-Inferential | `Disease`, `hasSymptom`, `Symptom`, set intersection/difference, ranking | Differential diagnosis is the core reasoning task for field diagnosticians and defines confusable-class handling for downstream image classifiers. |
| CQ-TXT-06 | For each disease in scope, how did reported incidence or affected area in surveillance bulletins for a given province change across seasons from 2019 to 2024, and which seasons exceeded the long-term reported mean? | Complex-Inferential | `SurveillanceReport`, `reportsIncidenceOf`, `Disease`, `hasAffectedArea`, `hasReportingPeriod`, `AdministrativeRegion`, temporal aggregation | Tests whether text-derived quantities are modelled as measurable, time-indexed observations rather than as opaque strings. |

### 2.b Image-Grounded Competency Questions

Answerable from annotated visual evidence alone.

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | How many annotated images depict spindle-shaped lesions with grey centres and brown margins on the leaf blade, and which disease label is assigned to them? | Simple | `Image`, `hasRegionOfInterest`, `SymptomObservation`, `hasLesionShape`, `hasLesionColour`, `depictsPlantPart`, `hasDiagnosticLabel` | Requires lesion morphology to be a first-class annotated property, not an unstructured caption. |
| CQ-IMG-02 | Which images serve as healthy-plant baselines, and how are they distributed across growth stage, capture distance (canopy vs. close-up), and acquisition device? | Simple | `Image`, `hasHealthStatus`, `capturedAtGrowthStage`, `hasCaptureScale`, `hasAcquisitionDevice` | Baseline coverage and acquisition metadata determine whether the image layer can support unbiased model training and evaluation. |
| CQ-IMG-03 | Which images contain two or more distinct symptom types annotated on the same plant, and which symptom combinations co-occur most frequently? | Relational | `Image`, `hasRegionOfInterest`, `annotatedWith`, `Symptom`, co-occurrence counting | Mixed infections are common in the field; the KG must not assume one image equals one disease. |
| CQ-IMG-04 | For each image annotation, who or what produced it (expert annotator, crowd worker, automated model), with what confidence score, and which annotations carry independent expert verification? | Relational | `Annotation`, `wasAttributedTo`, `Agent`, `hasConfidence`, `hasVerificationStatus` (align: PROV-O) | Provenance and confidence are prerequisites for trustworthy multimodal fusion and for auditing model-generated content. |
| CQ-IMG-05 | Which visual descriptors (lesion shape, lesion colour, halo presence, lesion distribution on the blade) most strongly separate brown spot from rice blast across the annotated image corpus? | Complex-Inferential | `SymptomObservation`, descriptor properties, `hasDiagnosticLabel`, grouping and contrastive frequency analysis | Encodes the image-side counterpart of CQ-TXT-05 and supplies evidence weights for cross-modal disambiguation. |
| CQ-IMG-06 | For a given field plot photographed repeatedly during one season, how did the annotated severity score and the estimated proportion of affected leaf area progress over time, and what was the interval of steepest increase? | Complex-Inferential | `Image`, `hasCaptureTimestamp`, `depictsFieldPlot`, `FieldPlot`, `hasSeverityScore`, `hasAffectedAreaFraction`, temporal ordering | Epidemic progression is a temporal property of a plot, not of an isolated photograph; this forces plot-level image series modelling. |

### 2.c Sensor / Environmental Competency Questions

Answerable from agroclimatic observations alone.

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What were the daily mean, minimum, and maximum air temperature and relative humidity recorded by station S over the last 14 days, and in which units? | Simple | `Sensor`, `Observation`, `observedProperty`, `hasResult`, `hasUnit`, `resultTime`, `madeBySensor` (align: SOSA/SSN, QUDT) | Establishes the observation pattern and explicit units, without which cross-site and cross-modal comparison is unsound. |
| CQ-ENV-02 | Which monitoring sites recorded at least five consecutive days with relative humidity ≥ 90% and night-time minimum temperature ≥ 22 °C during the 2024 wet season? | Simple | `Observation`, threshold filtering, consecutive-day window, `hasFeatureOfInterest`, `Site`, `Season` | Encodes the canonical conducive-condition query pattern that risk services will reuse for several pathogens. |
| CQ-ENV-03 | Which field plots are covered by which sensors and stations, at what spatial distance, and what is the completeness and last-calibration status of each sensor's series for a given season? | Relational | `FieldPlot`, `isMonitoredBy`, `Sensor`, `hasSpatialDistance`, `hasDataCompleteness`, `hasCalibrationDate` | Without an explicit plot–sensor coverage relation, every image-to-environment join in Section 2.e is unverifiable. |
| CQ-ENV-04 | For each plot, what were the cumulative growing-degree-days, total rainfall, and total leaf-wetness hours in the 30 days preceding a specified date, and how do plots rank on each aggregate? | Complex-Inferential | `Observation`, temporal window aggregation, derived variables `GrowingDegreeDay`, `LeafWetnessDuration`, ranking | Derived agroclimatic aggregates, not raw readings, are the quantities that actually drive epidemiological inference. |
| CQ-ENV-05 | Which micro-climatic episodes in a given agroecological zone deviated by more than two standard deviations from the ten-year baseline for the same calendar window, and in which variables? | Complex-Inferential | `Observation`, `ClimateBaseline`, `AgroecologicalZone`, anomaly detection, `deviatesFrom` | Anomaly detection supports early-warning use cases and requires the KG to hold reference baselines alongside current series. |

### 2.d Genomic / Tabular Competency Questions

Answerable from varietal, genotypic, and agronomic tabular records alone.

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which resistance genes or QTLs are recorded for variety Inpari 32, on which chromosomes, and from which donor source or mapping study? | Simple | `RiceVariety`, `carriesGene`, `ResistanceGene`, `locatedOnChromosome`, `hasDonorSource`, `assertedIn` (align: Sequence Ontology, Crop Ontology) | The variety–gene link is the entry point for every resistance-based recommendation in the cross-modal section. |
| CQ-GEN-02 | Which resistance genes confer resistance to *Xanthomonas oryzae* pv. *oryzae*, and against which reported races or pathotypes is each gene effective or defeated? | Simple | `ResistanceGene`, `confersResistanceTo`, `Pathogen`, `PathogenRace`, `hasResistanceStatus` | Race-specific resistance must be modelled explicitly, otherwise the KG will overstate protection. |
| CQ-GEN-03 | Which released varieties pyramid two or more bacterial-leaf-blight resistance genes, and what are their release year, releasing institution, and recommended agroecology? | Relational | `RiceVariety`, `carriesGene` (cardinality ≥ 2), `hasReleaseYear`, `releasedBy`, `Institution`, `recommendedFor`, `AgroecologicalZone` | Gene pyramiding is the main durable-resistance strategy and requires counting over the variety–gene relation. |
| CQ-GEN-04 | For varieties carrying *Bph3* or *Bph32*, what mean grain yield, maturity duration, and plant height are reported in multi-location trials, disaggregated by trial location and season? | Relational | `RiceVariety`, `carriesGene`, `TrialRecord`, `hasYield`, `hasMaturityDuration`, `conductedAt`, `Location` (align: TO, Crop Ontology traits) | Resistance is only adopted when agronomic performance is acceptable; this joins genotype to trial phenotype. |
| CQ-GEN-05 | Which varieties provide the broadest resistance spectrum — the greatest number of distinct pests and pathogens covered by their recorded resistance genes — while also achieving mean yield above 6 t ha⁻¹ and maturity below 115 days? | Complex-Inferential | `RiceVariety`, `carriesGene`, `confersResistanceTo`, distinct-count aggregation, numeric filtering, ranking | Combines resistance breadth with agronomic constraints, the realistic form of a varietal shortlist query. |

### 2.e Cross-Modal / Fusion Competency Questions

**Priority category.** Each question below is unanswerable from any single modality and therefore constitutes the substantive justification for a multimodal KG rather than four separate databases.

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 | Given an image annotated with elongated water-soaked lesions with wavy yellow margins beginning at the leaf tip, which textually described diseases match that symptom profile, and what are their causal pathogens and recommended control measures? | Relational | `Image`→`SymptomObservation`→`Symptom`←`hasSymptom`←`Disease`→`causedBy`→`Pathogen`; `hasControlMeasure` | The foundational Text×Image alignment: visual annotations must resolve to the same `Symptom` individuals used in literature assertions. |
| CQ-MM-02 | For every image with an expert-confirmed rice blast diagnosis, what were the mean relative humidity, night temperature, and leaf-wetness duration recorded by the nearest covering sensor in the seven days before capture? | Relational | `Image`, `hasCaptureTimestamp`, `depictsFieldPlot`, `isMonitoredBy`, `Observation`, temporal window join | Establishes the spatio-temporal join between visual evidence and environment that all risk modelling depends upon. |
| CQ-MM-03 | Given a leaf image showing grey-centred spindle-shaped lesions and a co-located sensor record of relative humidity above 90% with night temperatures of 20–25 °C sustained for at least five days, which disease is most probable, and on what combined textual, visual, and environmental evidence is that ranking based? | Complex-Inferential | `Image`, `SymptomObservation`, `Observation`, `Disease`, `hasConduciveCondition`, `EnvironmentalCondition`, evidence weighting and ranking | The canonical diagnostic fusion query and the primary demonstration of multimodal added value. |
| CQ-MM-04 | For the disease indicated by image evidence in a given plot, which varieties actually planted in that plot carry resistance genes against the causal pathogen, and which do not? | Relational | `Image`→`FieldPlot`, `PlantingRecord`, `plantedWithVariety`, `RiceVariety`, `carriesGene`, `confersResistanceTo`, `Pathogen` | Links observed field reality to genotype, exposing whether an outbreak occurred on nominally resistant material. |
| CQ-MM-05 | For a specified agroecological zone and the coming season, which varieties should be shortlisted, given (i) the diseases with the highest image-confirmed incidence in that zone last season, (ii) the environmental risk profile derived from sensor baselines, (iii) recorded resistance genes, and (iv) trial yield performance in comparable locations? | Complex-Inferential | Four-way join: `Image`/`Diagnosis`, `Observation`/`ClimateBaseline`, `RiceVariety`/`ResistanceGene`, `TrialRecord`; multi-criteria ranking | The flagship decision-support query; if the KG answers only this one well, the multimodal design is justified. |
| CQ-MM-06 | Which resistance genes reported in the literature as effective against the *Xanthomonas oryzae* races recorded in a given region are actually present in varieties currently released for that region? | Relational | `Document`/`assertedIn`, `ResistanceGene`, `confersResistanceTo`, `PathogenRace`, `recordedInRegion`, `RiceVariety`, `recommendedFor` | Exposes deployment gaps between published resistance knowledge and the varietal portfolio available to farmers. |
| CQ-MM-07 | Which environmental thresholds stated in the literature as conducive to sheath blight development were in fact exceeded at a given station during a specified season, and for how many days? | Relational | `Disease`, `hasConduciveCondition`, `EnvironmentalCondition` (threshold, variable, operator), `Observation`, threshold evaluation | Requires literature-stated thresholds to be modelled as machine-comparable quantities rather than prose, a common failure point in agricultural KGs. |
| CQ-MM-08 | Among plots that exceeded brown-planthopper-conducive conditions for a comparable number of days, did plots planted with *Bph*-resistant varieties record lower scouting damage scores than plots with susceptible varieties, and by how much on average? | Complex-Inferential | `FieldPlot`, `Observation`, `PlantingRecord`, `carriesGene`, `ScoutingRecord`, `hasDamageScore`, stratified comparison | Tests the KG's ability to support quasi-experimental comparison across sensor and genomic layers, not merely retrieval. |
| CQ-MM-09 | Which symptom phenotypes present in the annotated image corpus have no corresponding textual symptom description in the KG, and conversely which literature-described symptoms are entirely unillustrated? | Complex-Inferential | `Symptom`, `annotatedWith` vs. `hasSymptom`, set difference, coverage counting | A self-evaluation query: it makes cross-modal alignment gaps visible and directly serves KG quality assessment. |
| CQ-MM-10 | Across historical records, which combination of environmental variables in the 14 days preceding observation best discriminates plots that subsequently showed image-confirmed blast outbreaks from those that did not? | Complex-Inferential | `Observation` windows, `Diagnosis`/`hasDiagnosticLabel`, `FieldPlot`, contrastive aggregation over labelled cases | Converts the KG from a retrieval store into an evidence base for predictive early-warning models. |
| CQ-MM-11 | For each disease, which varieties are described in the literature as susceptible, and do field images exist of those varieties exhibiting that disease — with what severity distribution and in which seasons? | Complex-Inferential | `Disease`, `hasSusceptibleVariety`, `RiceVariety`, `PlantingRecord`, `Image`, `hasSeverityScore`, grouping | Cross-validates textual susceptibility claims against observed field evidence, a form of assertion triangulation. |
| CQ-MM-12 | Which currently monitored plots simultaneously satisfy the conducive-condition profile for a given disease over the last seven days **and** contain at least one image annotated with early-stage symptoms of that same disease in the same window? | Relational | `FieldPlot`, `Observation`, `hasConduciveCondition`, `Image`, `SymptomObservation`, `hasSymptomStage`, conjunctive temporal filtering | The operational alerting query for extension officers and IoT decision-support services. |
| CQ-MM-13 | Which plots planted with varieties carrying resistance genes against a given pathogen nevertheless show image-confirmed moderate-to-severe symptoms of the corresponding disease, and what were the environmental conditions during those events? | Complex-Inferential | `PlantingRecord`, `carriesGene`, `confersResistanceTo`, `Image`, `hasSeverityScore`, `Observation`, contradiction detection | Surfaces candidate resistance-breakdown or misidentification events, a high-value signal for breeders and pathologists. |
| CQ-MM-14 | For a given diagnosis event, what is the complete evidence chain — the images, sensor observations, literature assertions, and varietal records supporting it — with the provenance, timestamp, and confidence of each element, and are any two evidence items mutually contradictory? | Complex-Inferential | `DiagnosisEvent`, `isSupportedByEvidence`, `Evidence` (image, observation, document, record), `wasAttributedTo`, `hasConfidence`, `contradicts` (align: PROV-O, IAO) | Explainability and auditability: without a modelled evidence chain, fused answers cannot be defended to a domain expert. |

---

## 3. Modality-Pair Coverage Matrix (Requirement 7)

| Modality combination | CQ IDs | Count | Coverage assessment |
|---|---|---|---|
| Text only | CQ-TXT-01 … CQ-TXT-06 | 6 | Adequate |
| Image only | CQ-IMG-01 … CQ-IMG-06 | 6 | Adequate |
| Sensor only | CQ-ENV-01 … CQ-ENV-05 | 5 | Adequate |
| Genomic/tabular only | CQ-GEN-01 … CQ-GEN-05 | 5 | Adequate |
| Text × Image | CQ-MM-01, CQ-MM-09 | 2 | Adequate; CQ-MM-09 doubles as an alignment-gap audit |
| Text × Sensor | CQ-MM-07 | 1 | **Thin** — consider adding a CQ on region-specific outbreak reports vs. recorded seasonal anomalies |
| Text × Genomic | CQ-MM-06 | 1 | **Thin** — consider adding a CQ on literature-reported resistance durability vs. release cohorts |
| Image × Sensor | CQ-MM-02, CQ-MM-10, CQ-MM-12 (partial) | 2–3 | Strong; the KG's most exercised pairing |
| Image × Genomic | CQ-MM-04 | 1 | Thin as a pure pair, but reinforced within three-way CQ-MM-13 |
| Sensor × Genomic | CQ-MM-08 | 1 | Adequate; note that CQ-MM-08 also draws on tabular scouting records |
| Text × Image × Sensor | CQ-MM-03, CQ-MM-12 | 2 | Strong; core diagnostic and alerting pathways |
| Text × Image × Genomic | CQ-MM-11 | 1 | Adequate |
| Image × Sensor × Genomic | CQ-MM-13 | 1 | Adequate |
| Text × Sensor × Genomic | — | 0 | **Gap** — no CQ currently exercises this triple without image evidence; a candidate would ask which literature-conducive conditions co-occur with the deployment footprint of susceptible varieties |
| Four-way (Text × Image × Sensor × Genomic) | CQ-MM-05, CQ-MM-14 | 2 | Adequate; these are the integration stress tests |

**Complexity distribution:** Simple 10, Relational 12, Complex-Inferential 14.

---

## 4. Scope Boundary Note (Ontology Scope Statement)

**In scope.** The ontology must represent rice pests, pathogens and the diseases they cause; symptoms and damage signs, resolved to plant part and growth stage; annotated images and their lesion-level regions, capture metadata, and annotation provenance; agroclimatic observations with explicit sensors, features of interest, units, timestamps, and derived aggregates; rice varieties with their resistance genes, QTLs, race-specific efficacy, and multi-location trial phenotypes; field plots with planting and scouting records that act as the spatial hinge joining all four modalities; and diagnosis events with modelled evidence chains, confidence, and provenance.

**Out of scope.** The KG will not model rice physiology or metabolic pathways beyond resistance loci; it will not represent full genome sequences, variant-level SNP calls, or breeding pedigrees beyond the donor-source attribution needed for CQ-GEN-01; it will not encode pesticide product registrations, prices, market or supply-chain data, farm economics, or land-tenure information; it will not store the trained machine-learning models themselves, only their outputs as provenance-bearing annotations; and it will not extend to crops other than *Oryza sativa* or to abiotic stress diagnosis except where required to exclude look-alike nutrient-deficiency symptoms.

**Feasibility flags.** Three groups of CQs should be revisited against actual data availability. First, every image–sensor join (CQ-MM-02, CQ-MM-10, CQ-MM-12, CQ-MM-13) presupposes that images carry reliable geolocation and timestamps and that CQ-ENV-03's plot–sensor coverage relation is populated; public benchmark image sets typically lack both, so these CQs may be answerable only over a purpose-collected field subset. Second, CQ-MM-04, CQ-MM-08, CQ-MM-11 and CQ-MM-13 additionally require plot-level planting records linking a specific variety to a specific photographed plot, which is rarely present in existing corpora and may need primary data collection. Third, CQ-MM-10 and CQ-ENV-05 require a historical record of sufficient length and label quality — several seasons of confirmed diagnoses and a ten-year climate baseline respectively — and should be treated as aspirational until that history accumulates. CQ-MM-05 sits at the boundary between knowledge retrieval and decision support: the KG can supply and rank the evidence, but the weighting scheme itself is a modelling choice that should be documented outside the ontology.

---

*Note on alignment.* Where existing vocabularies cover a class, reuse is preferred over minting: NCBITaxon and AGROVOC for pathogens and pests, PO for plant parts, PPO and Crop Ontology for growth stages, TO and Crop Ontology for agronomic traits, SOSA/SSN with QUDT for observations and units, ENVO for agroecological zones, Sequence Ontology for genomic locations, IDO patterns for transmission and host–pathogen relations, and PROV-O with IAO for annotation, document, and evidence provenance. Relations without an established equivalent — notably `hasConduciveCondition`, `isSupportedByEvidence`, and the lesion-morphology descriptors — are candidates for new terms in the domain ontology.
