# Competency Questions for a Rice Pest & Disease Multimodal Knowledge Graph

## Assumptions (input placeholders resolved with defaults)

| Input field | Value used | Status |
|---|---|---|
| Pests/diseases in scope | Rice blast (*Magnaporthe oryzae*, syn. *Pyricularia oryzae*), bacterial leaf blight (*Xanthomonas oryzae* pv. *oryzae*), sheath blight (*Rhizoctonia solani*), brown spot (*Bipolaris oryzae*), rice tungro disease (RTBV + RTSV, vector *Nephotettix virescens*), brown planthopper (*Nilaparvata lugens*), yellow stem borer (*Scirpophaga incertulas*), rice bug (*Leptocorisa oratorius*) | ASSUMED – common major taxa |
| End users | Plant pathology researchers, agricultural extension officers (incl. pest observers / POPT), smart-farming system developers | ASSUMED |
| Geographic scope | Indonesian tropical lowland rice, with East Java as the primary study area | ASSUMED |
| Text sources | Scientific literature, extension guides, pest surveillance bulletins | ASSUMED |
| Image sources | Field and close-up photographs with expert/model annotations | ASSUMED |
| Sensor sources | IoT field stations and gridded weather data (temperature, RH, rainfall, soil moisture/pH) | ASSUMED |
| Genomic/tabular sources | Variety registry, resistance-gene records, planting records, yield-trial tables | ASSUMED |
| Target number | 36 CQs | DEFAULT (30–40) |
| Existing schema | Terms from the current Rice MMKG draft are reused where known (`annotatedAs`, `Infestation`); all other property names are indicative | PARTIAL |
| Previously drafted CQs | None supplied | – |

**Alignment targets flagged throughout:** AGROVOC; Crop Ontology rice trait dictionary (CO_320); Plant Ontology (PO) for organs and growth stages; Plant Trait Ontology (TO); PATO for phenotypic qualities; NCBITaxon for organisms; SOSA/SSN for sensor observations; OWL-Time; GeoSPARQL; PROV-O for provenance; QUDT for units; PECO for experimental conditions; IDO patterns for infection/disposition.

> Note on the prompt: "PPO" is the *Plant Phenology* Ontology, not a plant *phenotype* ontology. Phenotypic symptoms are better aligned with PATO/TO (and PPO only for phenological stages). This is corrected in the alignment list above.

---

## 1. Purpose and Scope (for confirmation)

The Rice MMKG is intended to support early diagnosis and management decisions for rice pests and diseases in Indonesian lowland rice systems by semantically linking literature-derived knowledge, annotated field imagery, agroclimatic sensor observations, and variety/resistance-gene records. Its scope is defined by the 36 competency questions below, which specify the entities, relations, and cross-modal links the KG must represent and against which it will be evaluated through formal (SPARQL) queries.

---

## 2. Competency Questions

### 2a. Text-grounded CQs (6)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal pathogen of rice blast, and what is its taxonomic identity (including synonyms)? | Simple | `Disease`, `causedBy`, `Pathogen`, `taxonRank`, `altLabel`; NCBITaxon, AGROVOC | Anchors every disease to a taxonomically resolvable agent, enabling cross-source entity alignment. |
| CQ-TXT-02 | Which viruses constitute rice tungro disease, and which insect species are documented as their vectors? | Simple | `Disease`, `causedBy`, `Virus`, `transmittedBy`, `Vector`; NCBITaxon, IDO | Vector relations are essential for vector-borne diseases, whose management targets the insect rather than the pathogen. |
| CQ-TXT-03 | Which symptoms of bacterial leaf blight are described for the tillering stage versus the booting stage, and on which plant organs? | Relational | `Disease`, `hasSymptom`, `Symptom`, `manifestsAtStage`, `GrowthStage`, `onOrgan`, `PlantOrgan`; PO, PATO | Stage- and organ-specific symptoms are the basis for field diagnosis and for linking text to image evidence. |
| CQ-TXT-04 | Which management practices (cultural, biological, chemical) are documented for brown planthopper, and which source documents support each practice? | Relational | `Pest`, `hasManagementPractice`, `ManagementPractice`, `practiceType`, `prov:wasDerivedFrom`, `Document` | Extension users need actionable recommendations with traceable evidence. |
| CQ-TXT-05 | Which diseases share at least one documented symptom with brown spot and should therefore be considered in differential diagnosis? | Relational | `Disease`, `hasSymptom`, `Symptom`, shared-symptom join (optionally `confusableWith`) | Supports diagnostic disambiguation, a known failure point for both human observers and image classifiers. |
| CQ-TXT-06 | Across surveillance bulletins for East Java, which pests or diseases show an increasing reported affected area over the last five planting seasons? | Complex-Inferential | `SurveillanceReport`, `reports`, `Infestation`, `affectedArea`, `Season`, `Region`; OWL-Time, GeoSPARQL | Tests temporal aggregation over report-derived facts to identify emerging threats. |

### 2b. Image-grounded CQs (6)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Which condition label is assigned to image *I*, and was it asserted by a human expert or a model? | Simple | `Image`, `annotatedAs`, `Condition`, `prov:wasAttributedTo`, `Annotator` (`HumanExpert` / `Model`) | Separates verified ground truth from machine predictions, a prerequisite for trustworthy reuse. |
| CQ-IMG-02 | Which plant organ does image *I* depict, and at what capture scale (close-up organ, whole plant, canopy/field)? | Simple | `Image`, `depictsOrgan`, `PlantOrgan`, `captureScale`; PO | Organ and scale metadata determine which symptoms are observable and which images are comparable. |
| CQ-IMG-03 | Which images annotated as sheath blight depict lesions on the leaf sheath at the maximum tillering stage? | Relational | `Image`, `annotatedAs`, `depictsSymptom`, `onOrgan`, `atGrowthStage`; PO | Enables retrieval of stage-specific visual exemplars for training and extension material. |
| CQ-IMG-04 | Which images carry conflicting condition annotations (different labels from different annotators, or between an expert and a model)? | Relational | `Image`, `hasAnnotation`, `Annotation`, `annotatedAs`, `prov:wasAttributedTo` | Surfaces label noise and hard cases, supporting dataset curation and classifier evaluation. |
| CQ-IMG-05 | For each disease, how many expert-verified images exist per growth stage and per organ, and which disease × stage combinations have fewer than *N* images? | Complex-Inferential | `Image`, `annotatedAs`, `atGrowthStage`, `depictsOrgan`, `verificationStatus`; aggregation | Quantifies coverage gaps in visual evidence, guiding further data collection. |
| CQ-IMG-06 | What is the distribution of annotated blast severity scores (IRRI Standard Evaluation System, 0–9) per region and season? | Complex-Inferential | `Image`, `annotatedAs`, `hasSeverityScore`, `SeverityScale`, `capturedIn` `Region`, `Season` | Severity, not only presence, drives yield-loss estimation and management thresholds. |

### 2c. Sensor/Environmental-grounded CQs (5)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What were the daily mean temperature, mean relative humidity, and cumulative rainfall recorded by station *S* on date *D*? | Simple | `sosa:Observation`, `sosa:madeBySensor`, `sosa:observedProperty`, `sosa:hasResult`, `sosa:resultTime`; QUDT | Basic retrieval of environmental facts that all fusion CQs depend on. |
| CQ-ENV-02 | Which sensor stations are associated with which fields, and which observable properties (with units) does each station measure? | Relational | `sosa:Sensor`, `sosa:isHostedBy`, `sosa:Platform`, `locatedIn`, `Field`, `sosa:observes`, `qudt:unit` | Establishes the spatial anchoring needed to join sensor data with field-level observations. |
| CQ-ENV-03 | Which fields recorded at least *N* consecutive hours of relative humidity ≥ 90% with temperature between 24 and 28 °C during week *W*? | Relational | `sosa:Observation`, `observedProperty`, `resultTime`, `Field`; OWL-Time intervals | Retrieves condition windows of the type associated with fungal infection (e.g., leaf wetness for blast). |
| CQ-ENV-04 | What was the monthly rainfall anomaly, relative to the multi-year mean, for each district in the study area during the last wet season? | Complex-Inferential | `sosa:Observation`, `Region`, `Season`, aggregation over time series | Captures seasonal deviations that precede planthopper and disease outbreaks at landscape scale. |
| CQ-ENV-05 | Which sensor streams contain gaps longer than 24 hours or physically implausible values in a given season? | Complex-Inferential | `sosa:Sensor`, `sosa:Observation`, `resultTime`, `dataQualityFlag`, PROV-O | Data quality must be queryable before sensor evidence is used in diagnosis. |

### 2d. Genomic/Tabular-grounded CQs (5)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which blast resistance genes (e.g., *Pi9*, *Pita*, *Pib*) are documented as carried by variety *V* (e.g., IR64)? | Simple | `Variety`, `carriesGene`, `ResistanceGene`, `confersResistanceTo`, `Disease` | The core genotype-to-resistance link used in variety recommendation. |
| CQ-GEN-02 | What are the parental lines, releasing institution, and release year of variety *V*? | Simple | `Variety`, `hasParent`, `releasedBy`, `releaseYear` | Pedigree explains shared resistance profiles and supports provenance of variety records. |
| CQ-GEN-03 | Which lowland irrigated varieties carry at least one bacterial leaf blight resistance gene (e.g., *Xa4*, *xa5*, *Xa7*, *Xa21*)? | Relational | `Variety`, `ecosystemType`, `carriesGene`, `ResistanceGene`, `confersResistanceTo` | Filters recommendable varieties by both agroecosystem and resistance. |
| CQ-GEN-04 | Which resistance genes are reported to confer resistance to which brown planthopper biotypes? | Relational | `ResistanceGene`, `confersResistanceTo`, `PestBiotype`, `biotypeOf`, `Pest` | Biotype-specific resistance is necessary because BPH resistance is frequently overcome by biotype shifts. |
| CQ-GEN-05 | Among varieties with yield-trial records in East Java, which rank highest in mean yield (t/ha) while carrying resistance genes against both blast and bacterial leaf blight? | Complex-Inferential | `Variety`, `hasYieldTrial`, `YieldTrial`, `meanYield`, `Region`, `carriesGene`; aggregation, ranking | Combines agronomic performance and resistance, reflecting real variety-selection decisions. |

### 2e. Cross-modal / Fusion CQs (14)

| ID | Question | Modalities | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|---|
| CQ-MM-01 | Which literature-documented symptoms of rice blast (e.g., spindle-shaped lesions with grey centres) are exemplified by at least one expert-verified image, and which documented symptoms have no image evidence? | Text × Image | Complex-Inferential | `Disease`, `hasSymptom`, `Symptom`, `describedIn`, `Image`, `depictsSymptom`; negation (`FILTER NOT EXISTS`) | Measures how well visual evidence covers textual knowledge, exposing symptom-level gaps. |
| CQ-MM-02 | For image *I* annotated as tungro, which vector species and which management practices are documented in the literature? | Text × Image | Relational | `Image`, `annotatedAs`, `Disease`, `transmittedBy`, `Vector`, `hasManagementPractice` | Turns an image-level diagnosis into actionable, evidence-backed advice. |
| CQ-MM-03 | What were the temperature and relative humidity conditions in the seven days preceding the capture of each blast-annotated image from field *F*? | Image × Sensor | Complex-Inferential | `Image`, `capturedAt`, `Field`, `captureTime`, `sosa:Observation`, `resultTime`; OWL-Time window | Links visual outcomes to their antecedent environment, the basis for early-warning modelling. |
| CQ-MM-04 | Which varieties appear in images annotated as bacterial leaf blight, and which of those varieties carry a documented BLB resistance gene? | Image × Genomic | Relational | `Image`, `annotatedAs`, `ofVariety`, `Variety`, `carriesGene`, `confersResistanceTo` | Identifies candidate cases of resistance breakdown in the field. |
| CQ-MM-05 | For fields planted with variety *V*, what were the seasonal temperature and rainfall profiles, and how does recorded yield vary across them? | Sensor × Genomic/Tabular | Complex-Inferential | `PlantingRecord`, `Field`, `Variety`, `Season`, `sosa:Observation`, `hasYield`; aggregation | Supports genotype × environment analysis of variety performance. |
| CQ-MM-06 | Which pathogen races or pest biotypes are reported in the literature to overcome resistance gene *G*, and which varieties in the KG rely on *G* as their only documented resistance gene against that threat? | Text × Genomic | Complex-Inferential | `ResistanceGene`, `overcomeBy`, `PathogenRace`/`PestBiotype`, `describedIn`, `Variety`, `carriesGene`; counting | Flags varieties with fragile single-gene resistance. |
| CQ-MM-07 | Which pests or diseases have literature-documented favourable environmental ranges that were met in field *F* during the last 14 days? | Text × Sensor | Complex-Inferential | `Condition`, `favouredBy`, `EnvironmentalCondition` (property, min, max, duration), `sosa:Observation`, `Field` | Operationalises textual epidemiological knowledge against live sensor data. |
| CQ-MM-08 | Given an image annotated with symptom *S* (e.g., water-soaked lesions with wavy margins on the leaf blade) and the recent temperature/RH readings from its field, which candidate conditions are consistent with both the symptom and the documented favourable environment, ranked by the number of matching criteria? | Text × Image × Sensor | Complex-Inferential | `Image`, `depictsSymptom`, `Condition`, `hasSymptom`, `favouredBy`, `EnvironmentalCondition`, `sosa:Observation`; ranking | The prototypical multimodal diagnosis query that no single modality can answer. |
| CQ-MM-09 | For the top-ranked candidate condition from CQ-MM-08, which varieties planted within the same district carry resistance genes against it, and which management practices are recommended for the observed growth stage? | Text × Image × Sensor × Genomic | Complex-Inferential | CQ-MM-08 entities + `PlantingRecord`, `Variety`, `carriesGene`, `hasManagementPractice`, `applicableAtStage`, `Region` | End-to-end decision support spanning all four modalities. |
| CQ-MM-10 | Under comparable humidity conditions, how do annotated blast severity scores differ between varieties carrying blast resistance genes and varieties without them? | Image × Sensor × Genomic | Complex-Inferential | `Image`, `hasSeverityScore`, `ofVariety`, `carriesGene`, `sosa:Observation`, `Field`; grouping, comparison | Tests whether documented resistance is reflected in field-observed severity. |
| CQ-MM-11 | Which outbreaks reported in surveillance bulletins are corroborated by image evidence from the same district and period, and were preceded by sensor-recorded favourable conditions? | Text × Image × Sensor | Complex-Inferential | `SurveillanceReport`, `reports`, `Infestation`, `Image`, `annotatedAs`, `Region`, `Season`, `favouredBy`, `sosa:Observation` | Triangulates evidence across sources, strengthening the reliability of outbreak records. |
| CQ-MM-12 | Which images and which text passages jointly support the diagnosis recorded in `Infestation` record *R*, and who asserted each piece of evidence? | Text × Image | Relational | `Infestation`, `hasEvidence`, `Image`, `TextPassage`, `prov:wasDerivedFrom`, `prov:wasAttributedTo` | Makes every diagnosis explainable and auditable through provenance. |
| CQ-MM-13 | At which growth stage was the crop in field *F* on date *D* (derived from planting date and variety duration), and which diseases does the literature report as most damaging at that stage? | Genomic/Tabular × Text | Relational | `PlantingRecord`, `plantingDate`, `Variety`, `growthDuration`, `GrowthStage`, `Disease`, `mostDamagingAt`; PO | Stage-aware risk assessment requires combining agronomic records with stage-specific literature. |
| CQ-MM-14 | Which historical combinations of environmental conditions over the preceding *N* days, variety resistance profile, and growth stage co-occurred with image-verified outbreaks of disease *X*? | Image × Sensor × Genomic/Tabular | Complex-Inferential | `Infestation`, `Image`, `verificationStatus`, `Field`, `sosa:Observation`, `PlantingRecord`, `Variety`, `carriesGene`, `GrowthStage`; temporal windows | Produces the feature table for outbreak prediction; the KG retrieves co-occurrences, while prediction is performed downstream. |

**Distribution:** Text 6 (16.7%), Image 6 (16.7%), Sensor 5 (13.9%), Genomic/Tabular 5 (13.9%), Cross-modal 14 (38.9%). Complexity across all 36: Simple 9, Relational 13, Complex-Inferential 14.

---

## 3. Modality-Pair Coverage

| Modality combination | CQ IDs | Count | Note |
|---|---|---|---|
| Text × Image | MM-01, MM-02, MM-08, MM-09, MM-11, MM-12 | 6 | Well covered |
| Text × Sensor | MM-07, MM-08, MM-09, MM-11 | 4 | Adequate |
| Text × Genomic/Tabular | MM-06, MM-09, MM-13 | 3 | Thinnest pair |
| Image × Sensor | MM-03, MM-08, MM-09, MM-10, MM-11, MM-14 | 6 | Well covered |
| Image × Genomic/Tabular | MM-04, MM-09, MM-10, MM-14 | 4 | Adequate |
| Sensor × Genomic/Tabular | MM-05, MM-09, MM-10, MM-14 | 4 | Adequate |
| Text × Image × Sensor | MM-08, MM-11 | 2 | |
| Image × Sensor × Genomic/Tabular | MM-10, MM-14 | 2 | |
| Text × Image × Genomic/Tabular | – | 0 | **Gap** |
| Text × Sensor × Genomic/Tabular | – | 0 | **Gap** |
| Four-way | MM-09 | 1 | |

Candidate gap-filling CQs: (i) *Text × Image × Genomic*: "Which images of variety *V* show symptoms of a disease against which *V* is documented in the literature as resistant?"; (ii) *Text × Sensor × Genomic*: "Which varieties carry resistance against diseases whose documented favourable conditions occurred most frequently in district *R* over the last three seasons?"

---

## 4. Scope Boundary Note

The KG is in scope for representing major rice pests and diseases, their causal agents and vectors, stage- and organ-specific symptoms, documented management practices and favourable environmental conditions, annotated images with provenance and severity, spatially anchored sensor observations, and variety records with resistance genes, pedigree, planting, and yield data for Indonesian lowland rice. It is out of scope for raw pixel-level image analysis, sequence-level genomics (e.g., SNP genotypes or QTL mapping), pesticide registration and regulation, market or price data, and predictive modelling itself; the KG retrieves the evidence on which such models operate but does not perform prediction. Several CQs may be infeasible with currently available data: CQ-MM-03, MM-08 to MM-11 and MM-14 require images with reliable GPS coordinates and timestamps co-located with sensor stations, which most public rice disease image datasets lack; CQ-IMG-06 and MM-10 require SES severity annotations that are rarely provided; CQ-GEN-01, GEN-03 and MM-06 depend on gene-presence records for Indonesian varieties, which are sparse and scattered across the literature; and CQ-GEN-04 and MM-06 depend on biotype/race reporting that may be outdated. These CQs should be retained as design requirements but reported separately in evaluation as "schema-supported, data-limited" until the corresponding data sources are secured.
