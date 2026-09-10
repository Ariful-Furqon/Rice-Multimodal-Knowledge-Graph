# Competency Questions for a Rice Pest & Disease Multimodal Knowledge Graph (Rice MMKG)

**Version:** 1.0 — 3 September 2026
**Status:** Draft for ontology requirements specification (ORSD)

## 0. Assumptions

The input fields of the elicitation prompt were left as placeholders, so the following defaults were applied and are marked explicitly:

| Field | Assumption |
|---|---|
| Pests/diseases in scope | Major tropical lowland rice pests and diseases: rice blast (*Magnaporthe oryzae*), bacterial leaf blight (*Xanthomonas oryzae* pv. *oryzae*), sheath blight (*Rhizoctonia solani*), rice tungro disease (RTBV/RTSV, vectored by *Nephotettix virescens*), brown spot (*Bipolaris oryzae*), brown planthopper (*Nilaparvata lugens*), yellow stem borer (*Scirpophaga incertulas*), rice bug (*Leptocorisa oratorius*), golden apple snail (*Pomacea canaliculata*), and rat (*Rattus argentiventer*) |
| End users | Plant pathology researchers, agricultural extension officers (PPL / POPT), smart-farming/IoT system developers |
| Geographic scope | Indonesia, with East Java as the primary agroecological reference (irrigated tropical lowland rice, two–three cropping seasons per year) |
| Datasets per modality | TEXT: IRRI Rice Knowledge Bank, Indonesian BB Padi / Balitbangtan extension materials, peer-reviewed literature; IMAGE: public rice leaf disease datasets plus field photographs; SENSOR: station and IoT time-series (temperature, RH, rainfall, soil moisture, soil pH); GENOMIC/TABULAR: variety release descriptors (Inpari, Ciherang, IR64, etc.), resistance gene records (*Xa*, *Pi*, *Bph* loci), yield and planting-date tables |
| Target CQ count | 36 |
| Ontology alignment | Existing Rice MMKG classes are assumed (Observation with three medium-axis subclasses, `annotatedAs`, `Infestation` as a condition class alongside `Disease`); external alignment targets: AGROVOC, Crop Ontology (rice trait dictionary), Plant Trait Ontology (TO), Plant Phenotype Ontology (PPO), Plant Ontology (PO) for anatomical parts, Environment Ontology (ENVO), SOSA/SSN for sensor observations, PROV-O for provenance, and RiceDO v2 as the closest domain comparator |
| Previously drafted CQs | None supplied |

## 1. Purpose and Scope (for confirmation)

The Rice MMKG is a multimodal knowledge graph that semantically links textual knowledge, field and close-up imagery, environmental sensor time-series, and variety/genotype records about pests and diseases of *Oryza sativa* in Indonesian tropical lowland systems. Its purpose is to support early diagnosis, outbreak risk assessment, and management decision-making by researchers, extension officers, and precision-agriculture systems, and to serve as a reusable, standards-aligned resource for the international community. The competency questions below define what the KG must be able to answer, with the largest share devoted to cross-modal questions that justify integration over four separate unimodal databases.

## 2. Competency Questions

### 2a. Text-grounded CQs (CQ-TXT)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal agent of a given rice disease (e.g., bacterial leaf blight), and to which taxonomic group (fungus, bacterium, virus) does it belong? | Simple | Disease, causedBy, Pathogen, hasTaxonomicRank/Taxon | Basic diagnostic lookup; anchors every disease node to AGROVOC/NCBI Taxon identifiers. |
| CQ-TXT-02 | Which insect species act as vectors for rice tungro disease, and which viruses (RTBV, RTSV) do they transmit? | Relational | Disease, hasVirus, Virus, transmittedBy, Pest (Vector) | Tungro control targets the vector, not the virus; the vector–virus–disease chain must be traversable. |
| CQ-TXT-03 | At which rice growth stages (e.g., seedling, tillering, booting, heading, ripening) is a given pest or disease reported as most damaging? | Relational | Condition (Disease/Infestation), damagesAt, GrowthStage (BBCH / IRRI stage) | Growth-stage susceptibility windows drive timing of scouting and intervention. |
| CQ-TXT-04 | Which management practices (cultural, biological, chemical) are recommended in extension literature for a given condition, and which active ingredients or biocontrol agents do they involve? | Relational | Condition, managedBy, ManagementPractice, hasType, usesAgent, ActiveIngredient/BiocontrolAgent, source (PROV-O) | Extension officers need provenance-traceable recommendations; recommendations must be attributable to a source document. |
| CQ-TXT-05 | Which symptom descriptors (e.g., "diamond-shaped lesion with grey centre") are associated with more than one condition in the literature, and thus constitute ambiguous diagnostic evidence? | Complex-Inferential | Symptom, indicativeOf, Condition, affectsPart (PO), aggregation over symptom→condition counts | Identifies confusable conditions (e.g., blast vs. brown spot) that require image or environmental evidence to disambiguate. |
| CQ-TXT-06 | Which conditions have been reported in a given Indonesian province (e.g., East Java) in surveillance bulletins within a given year, ranked by reported affected area? | Complex-Inferential | SurveillanceReport, reportsCondition, Condition, hasLocation, AdministrativeRegion, reportedAffectedArea, reportingPeriod | Establishes regional prevalence priors for diagnosis and enables temporal comparison across seasons. |

### 2b. Image-grounded CQs (CQ-IMG)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Which images in the KG are annotated as showing a given condition (e.g., sheath blight), and what is the annotation source (expert, model, dataset label)? | Simple | ImageObservation, annotatedAs, Condition, hasAnnotation, Annotation, annotatedBy (Agent), confidence | Core retrieval of visual evidence per condition with provenance; supports the `annotatedAs` design decision. |
| CQ-IMG-02 | Which plant part (leaf, sheath, stem, panicle, whole plant) is depicted in a given image, and what visual symptom class (lesion, discolouration, wilting, hopperburn, deadheart, whitehead) is annotated? | Simple | ImageObservation, depictsPart (PO term), showsVisualSymptom, VisualSymptomClass | Links images to anatomical and phenotypic vocabularies (PO, PPO) rather than flat labels. |
| CQ-IMG-03 | How many images per condition exist for each plant part and image type (field vs. close-up), and which condition–part combinations have fewer than N images? | Relational | ImageObservation, annotatedAs, Condition, depictsPart, hasImageType, aggregation (COUNT, GROUP BY) | Exposes class imbalance and coverage gaps in the visual corpus before model training or evaluation. |
| CQ-IMG-04 | For a given image, which other images depict the same condition at the same growth stage but a different severity grade? | Relational | ImageObservation, annotatedAs, Condition, hasSeverityGrade (e.g., IRRI SES scale), atGrowthStage, sameCondition path | Enables severity progression series for training and for illustrating symptom development. |
| CQ-IMG-05 | Which pairs of conditions are most frequently confused in model-generated image annotations relative to expert annotations, and on which plant parts does this confusion concentrate? | Complex-Inferential | ImageObservation, hasAnnotation ×2, Annotation, annotatedBy (Model vs Expert), annotatedAs, depictsPart, disagreement aggregation | Quantifies where visual evidence alone is insufficient; motivates fusion with text and sensor modalities. |
| CQ-IMG-06 | Which images depicting healthy plants of a given variety serve as baselines for a given growth stage and image type? | Simple | ImageObservation, annotatedAs (HealthyState), ofVariety, Variety, atGrowthStage, hasImageType | Healthy baselines are required for contrastive diagnosis and for validating symptom annotations. |

### 2c. Sensor/environmental-grounded CQs (CQ-ENV)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What were the daily mean temperature, relative humidity, and rainfall recorded at a given sensor station over a given date range? | Simple | SensorObservation (SOSA), madeBySensor, Sensor, hasFeatureOfInterest, Plot/Station, observedProperty, hasResult, resultTime | Foundational time-series retrieval; validates SOSA/SSN alignment. |
| CQ-ENV-02 | Which monitored plots experienced a continuous period of at least N days with relative humidity above X% and mean temperature within [Tmin, Tmax]? | Relational | SensorObservation, observedProperty (RH, Temp), hasFeatureOfInterest, Plot, temporal window aggregation | Such windows are the canonical conducive-condition definitions for blast and sheath blight. |
| CQ-ENV-03 | What is the seasonal (wet/dry) distribution of leaf-wetness-proxy hours (RH > 90%) per plot across the last M cropping seasons? | Complex-Inferential | SensorObservation, Plot, CroppingSeason, hasSeasonType, aggregation by season | Seasonal disease pressure profiles are needed for planting-date and variety advisories. |
| CQ-ENV-04 | Which plots show a soil pH or soil moisture trajectory outside a specified agronomic range during the tillering stage of the current season? | Relational | SensorObservation, observedProperty (SoilpH, SoilMoisture), Plot, hasCropCycle, CropCycle, atGrowthStage, GrowthStage | Soil stress predisposes plants to brown spot and weakens tolerance to planthopper feeding. |
| CQ-ENV-05 | For each station, which sensors have data gaps or out-of-range readings within a date range, and what proportion of the period is affected? | Complex-Inferential | Sensor, SensorObservation, resultTime, hasResult, quality flag, gap detection aggregation | Data-quality awareness is necessary before environmental evidence is fused into any diagnostic inference. |

### 2d. Genomic/tabular-grounded CQs (CQ-GEN)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which resistance genes or QTLs (e.g., *Xa21*, *Pi9*, *Bph26*) does a given released variety (e.g., Inpari 32) carry, according to its release descriptor or published genotype record? | Simple | Variety, carriesGene, ResistanceGene/QTL, confersResistanceTo, Condition, source | Direct lookup that the genomic modality must satisfy; aligns to Crop Ontology / Gramene identifiers. |
| CQ-GEN-02 | Which varieties are documented as resistant, moderately resistant, or susceptible to a given pathogen race or pest biotype (e.g., BPH biotype 3)? | Relational | Variety, hasResistanceRating, ResistanceRating, againstStrain, PathogenRace/PestBiotype, isStrainOf, Pathogen/Pest | Resistance is race/biotype-specific; the KG must not collapse ratings to the species level. |
| CQ-GEN-03 | Which varieties released after a given year combine resistance to at least two of {bacterial leaf blight, blast, brown planthopper} and have a recorded average yield above Y t/ha? | Complex-Inferential | Variety, releaseYear, carriesGene, confersResistanceTo, Condition, hasTrait, YieldTrait, aggregation/filter | Multi-criteria variety selection is a recurring extension question. |
| CQ-GEN-04 | What are the pedigree relationships (parents, donor lines) of a given variety, and which resistance genes were inherited from which parent? | Relational | Variety, hasParent, Variety, carriesGene, ResistanceGene, donorOf | Supports breeding-informed explanations of resistance and cross-referencing with IRRI germplasm records. |
| CQ-GEN-05 | For a given district and season, which varieties were planted on which proportion of the recorded area, and what maturity duration does each have? | Relational | PlantingRecord, ofVariety, Variety, hasMaturityDuration, inRegion, AdministrativeRegion, inSeason, plantedArea | Tabular planting data underpins regional exposure estimates when combined with outbreak data. |

### 2e. Cross-modal / fusion CQs (CQ-MM)

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 | Given a leaf image annotated with a visual symptom class and a co-located sensor record showing RH > 90% for the preceding 5 days and temperatures of 24–28 °C, which conditions in the KG are consistent with both the visual symptom and the environmental window? | Complex-Inferential | ImageObservation, showsVisualSymptom, Condition, favouredBy, EnvironmentalCondition (threshold ranges), SensorObservation, Plot, co-location, temporal window | Prototype fusion query (Image×Sensor): visual evidence narrowed by conducive-condition constraints. |
| CQ-MM-02 | For a condition diagnosed from an image at a given plot, which varieties recorded as planted in the same district carry resistance genes against the causal pathogen, and which are susceptible? | Complex-Inferential | ImageObservation, annotatedAs, Condition, causedBy, Pathogen, Variety, carriesGene, confersResistanceTo, PlantingRecord, inRegion | Image×Genomic×Tabular: translates a diagnosis into a variety-level risk map for extension advice. |
| CQ-MM-03 | Which images of a given condition were captured at plots where the preceding 7-day environmental record did *not* satisfy the literature-reported conducive conditions for that condition? | Complex-Inferential | ImageObservation, annotatedAs, Condition, favouredBy (from literature, with source), SensorObservation, Plot, temporal window, negation | Text×Image×Sensor: flags annotation errors or anomalous outbreaks that violate textual domain knowledge. |
| CQ-MM-04 | Which textual symptom descriptors for a condition correspond to which visual symptom classes and plant parts in the annotated image corpus, and for which descriptors is there no supporting image? | Relational | Symptom (text), indicativeOf, Condition, correspondsTo, VisualSymptomClass, ImageObservation, depictsPart | Text×Image alignment; the missing-image case directly informs image acquisition priorities. |
| CQ-MM-05 | Given an image annotated as brown planthopper hopperburn on a known variety, is the variety documented as susceptible to the BPH biotype prevalent in the region, and what does the extension literature recommend for that variety–biotype combination? | Complex-Inferential | ImageObservation, annotatedAs, Infestation, ofVariety, Variety, hasResistanceRating, againstStrain, PestBiotype, prevalentIn, Region, managedBy, ManagementPractice, source | Image×Genomic×Text: end-to-end diagnosis-to-recommendation chain across three modalities. |
| CQ-MM-06 | For each variety planted in a district, which conditions (a) are favoured by the environmental conditions recorded there during the current season and (b) are ones the variety lacks documented resistance to? | Complex-Inferential | Variety, PlantingRecord, Plot/Region, SensorObservation, EnvironmentalCondition, favours, Condition, confersResistanceTo, set difference | Sensor×Genomic×Tabular: produces a per-variety exposure list without any image evidence — the early-warning use case. |
| CQ-MM-07 | Which sensor-derived conducive windows in the last N days at a plot were followed within K days by an image-confirmed diagnosis, and for which windows was no confirming image recorded? | Complex-Inferential | SensorObservation, Plot, EnvironmentalCondition window, ImageObservation, annotatedAs, Condition, temporal ordering, negation | Image×Sensor with temporal reasoning: supplies the labelled event pairs needed to evaluate outbreak prediction. |
| CQ-MM-08 | For a given resistance gene (e.g., *Pi9*), which images show blast symptoms on varieties that carry that gene, and at which plots and dates were they taken? | Relational | ResistanceGene, carriedBy, Variety, ImageObservation, ofVariety, annotatedAs, Condition (blast), atPlot, captureTime | Image×Genomic: surfaces possible resistance breakdown, which is scientifically high-value evidence. |
| CQ-MM-09 | Which literature-reported growth-stage susceptibility windows for a condition coincide with observed conducive environmental windows at plots where the same condition was later imaged, and what is the typical lag between window onset and first imaged symptom? | Complex-Inferential | Condition, damagesAt, GrowthStage (text), CropCycle, atGrowthStage (sensor/plot), EnvironmentalCondition window, ImageObservation, captureTime, lag aggregation | Text×Sensor×Image with temporal inference: bridges textual knowledge to empirically observed latency. |
| CQ-MM-10 | Which management recommendations from the literature apply to a condition that has been image-confirmed on a plot, and are any of the recommended active ingredients contraindicated by the plot's recorded soil pH or the variety's documented sensitivity? | Complex-Inferential | ImageObservation, annotatedAs, Condition, managedBy, ManagementPractice, usesAgent, ActiveIngredient, contraindicatedUnder, SoilCondition, SensorObservation, Variety, hasSensitivity | Text×Image×Sensor×Genomic four-way fusion: the decision-support end point of the KG. |
| CQ-MM-11 | For images whose model-generated and expert annotations disagree, does the co-located environmental record favour one of the two candidate conditions, and does the variety's resistance profile exclude either? | Complex-Inferential | ImageObservation, Annotation ×2, annotatedAs, Condition ×2, favouredBy, SensorObservation, Variety, confersResistanceTo, arbitration logic | Image×Sensor×Genomic: uses non-visual modalities to resolve visual ambiguity, directly addressing the fusion proof-of-concept. |
| CQ-MM-12 | Which sensor stations are co-located with plots that have both a planting record (variety, planting date) and at least one annotated image, and thus form complete multimodal observation units? | Relational | Sensor/Station, coLocatedWith, Plot, hasPlantingRecord, Variety, hasImageObservation, ImageObservation | Identifies the four-way linked subgraph; its size is a key resource-paper statistic. |
| CQ-MM-13 | Which conditions reported in surveillance bulletins for a district in a given season are corroborated by image evidence from that district and season, and which are reported but have no image evidence (or vice versa)? | Complex-Inferential | SurveillanceReport, reportsCondition, Condition, hasLocation, reportingPeriod, ImageObservation, annotatedAs, atPlot, inRegion, captureTime, set comparison | Text×Image at population scale: measures agreement between official reporting and field imagery. |
| CQ-MM-14 | Which vector species for tungro have been imaged or trapped at plots where susceptible varieties are planted and where the temperature record over the last N days falls within the vector's literature-reported activity range? | Complex-Inferential | Disease (tungro), transmittedBy, Pest (vector), hasActivityRange, EnvironmentalCondition, ImageObservation/TrapObservation, atPlot, PlantingRecord, Variety, hasResistanceRating, SensorObservation | Text×Image×Sensor×Genomic: vector-borne disease risk requires all four modalities simultaneously. |

## 3. Modality-Pair Coverage

| Modality combination | CQ IDs |
|---|---|
| Text × Image | CQ-MM-04, CQ-MM-13 |
| Image × Sensor | CQ-MM-01, CQ-MM-07 |
| Image × Genomic/Tabular | CQ-MM-02, CQ-MM-08 |
| Text × Sensor | (covered only within three-way CQs: CQ-MM-03, CQ-MM-09) |
| Text × Genomic/Tabular | (covered only within three-way CQs: CQ-MM-05) |
| Sensor × Genomic/Tabular | CQ-MM-06 |
| Text × Image × Sensor | CQ-MM-03, CQ-MM-09 |
| Image × Sensor × Genomic | CQ-MM-11 |
| Image × Genomic × Text | CQ-MM-05 |
| Sensor × Genomic × Tabular | CQ-MM-06 |
| Four-way (Text × Image × Sensor × Genomic) | CQ-MM-10, CQ-MM-14 |
| Structural linkage (all modalities, no inference) | CQ-MM-12 |

**Coverage gaps visible at a glance.** No CQ exercises Text×Sensor or Text×Genomic as a *pure* pair. If the paper's evaluation needs each pair to be tested in isolation, two CQs should be added: e.g., "Which literature-reported conducive thresholds for a condition are currently exceeded at a plot?" (Text×Sensor) and "Which resistance genes cited in the literature as effective against Indonesian *Xoo* races are carried by locally released varieties?" (Text×Genomic).

## 4. Scope Boundary Note

**In scope.** The KG covers the ten named pests and diseases of tropical lowland rice in Indonesia (East Java reference), their causal agents, vectors, races/biotypes, symptoms (textual and visual), affected plant parts and growth stages, conducive environmental conditions expressed as threshold windows over station/IoT time-series, plot-level planting records, released varieties with pedigree, resistance genes/QTLs and race-specific resistance ratings, and provenance-traceable management recommendations; every image, sensor reading, and report is an Observation individual linked to a plot, time, and (where known) variety.

**Out of scope.** The KG does not model weeds, nutrient deficiencies, or abiotic stress as first-class conditions (they appear only as confounders in CQ-TXT-05), does not represent pesticide regulatory status or pricing, does not store raw pixel data or raw genomic sequences (only annotations, descriptors, and identifiers pointing to external resources), and does not attempt yield-loss economic modelling.

**Feasibility flags.** CQ-MM-07, CQ-MM-09, and CQ-MM-11 require dated, geolocated images co-registered with sensor stations and variety records; with current public image datasets this four-way linkage exists only for a small proof-of-concept subgraph (cf. CQ-MM-12), so these CQs may need to be evaluated on synthetic or curated field campaign data. CQ-GEN-02 and CQ-MM-05 depend on race/biotype-level resistance data that is sparsely published for Indonesian varieties; where absent, ratings must be recorded at species level with an explicit uncertainty flag. CQ-MM-10 presupposes contraindication knowledge (active ingredient × soil condition × variety sensitivity) that is not consistently available in extension literature and may need to be scoped down to a recommendation-lookup without contraindication checking.
