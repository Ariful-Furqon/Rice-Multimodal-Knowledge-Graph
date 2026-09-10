# Competency Questions for a Multimodal Knowledge Graph of Rice Pests and Diseases

*Ontology Requirements Specification — Competency Questions*
*Generated from `rice_mmkg_cq_prompt.md` using the prompt's stated defaults; all assumptions are marked in Section 1.1.*

---

## 1. Purpose and Scope (for confirmation)

The proposed Rice Pest and Disease Multimodal Knowledge Graph (working name: RPD-MMKG) semantically integrates textual, image, sensor/environmental, and genomic/tabular data to support early diagnosis and evidence-based management of the major biotic constraints of lowland rice (*Oryza sativa*). Its intended users are plant pathology researchers, agricultural extension officers, and developers of smart-farming decision-support systems, with tropical lowland rice in Southeast Asia (Indonesia as the reference case) as the default agroecological scope. The competency questions (CQs) below define what the KG must be able to answer and thereby fix its ontology design, its cross-modal alignment requirements, and its SPARQL-based evaluation criteria.

### 1.1 Assumptions adopted (input placeholders were not supplied)

| ID | Input field | Default assumption adopted |
|---|---|---|
| A1 | Pests and diseases in scope | **Diseases:** rice blast (*Magnaporthe oryzae*, anamorph *Pyricularia oryzae*); bacterial leaf blight, BLB (*Xanthomonas oryzae* pv. *oryzae*, Xoo); sheath blight (*Rhizoctonia solani* AG1-IA); brown spot (*Bipolaris oryzae*); rice tungro disease (rice tungro bacilliform virus, RTBV, and rice tungro spherical virus, RTSV); grassy stunt and ragged stunt (RGSV, RRSV). **Pests:** brown planthopper, BPH (*Nilaparvata lugens*); green leafhopper, GLH (*Nephotettix virescens*); yellow stem borer (*Scirpophaga incertulas*); white stem borer (*S. innotata*); rice bug (*Leptocorisa oratorius*); rice leaffolder (*Cnaphalocrocis medinalis*). Healthy plants and nutrient deficiencies are included only as baseline or differential (look-alike) classes. |
| A2 | Geographic scope | Irrigated and rainfed tropical lowland rice in Southeast Asia, Indonesia as reference case; two principal cropping seasons (wet and dry). |
| A3 | End users | Plant pathology researchers, agricultural extension officers, and smart-farming/IoT system developers. |
| A4 | Available datasets | **Text:** peer-reviewed articles, extension leaflets, and national pest/disease surveillance bulletins, processed by entity and relation extraction with provenance to source text spans. **Image:** georeferenced, timestamped field and close-up photographs with expert annotations (diagnostic label, plant organ, growth stage, IRRI SES severity score, bounding boxes or masks) and automated classifier predictions, including healthy baselines. **Sensor:** in-field IoT stations (air temperature, relative humidity, rainfall, leaf wetness, soil moisture, soil pH) at hourly or finer resolution, automated insect light-trap counts where available, and gridded weather data. **Genomic/tabular:** variety registry, resistance genes and QTLs with positions on the IRGSP-1.0 reference, marker genotype calls, resistance screening trials (SES scores), multi-location yield trials, and plot-level planting records. |
| A5 | Target number of CQs | 40 (within the default range of 30–40). |
| A6 | Existing ontology/schema | None yet; alignment targets are proposed in Appendix A and flagged with "→" in the CQ tables. |
| A7 | Previously drafted CQs | None. |
| A8 | Representation assumption | Image content is queried through annotations and model-derived labels, not raw pixels. Sensor streams are represented as SOSA/SSN observations plus materialised daily and episodic aggregates. Machine-learning outputs and extracted literature claims are reified as first-class entities carrying confidence and PROV-O provenance. |

**Notation.** In the "Key Entities & Relations" column, classes are written in UpperCamelCase and properties in lowerCamelCase; "→" marks a proposed alignment target (e.g., `PlantStructure → PO`). Bracketed terms such as [P], [D], or [N] are query parameters to be bound at query time.

---

## 2. Competency Questions

### Distribution summary

| Category | Count | Share | Simple | Relational | Complex-Inferential |
|---|---|---|---|---|---|
| Text-grounded (TXT) | 7 | 17.5 % | 2 | 3 | 2 |
| Image-grounded (IMG) | 7 | 17.5 % | 2 | 3 | 2 |
| Sensor/environmental-grounded (ENV) | 6 | 15.0 % | 2 | 2 | 2 |
| Genomic/tabular-grounded (GEN) | 6 | 15.0 % | 2 | 2 | 2 |
| Cross-modal/fusion (MM) | 14 | 35.0 % | 2 | 4 | 8 |
| **Total** | **40** | **100 %** | **10** | **14** | **16** |

### 2.1 Text-grounded CQs

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-TXT-01 | What is the causal agent of a given rice disease (e.g., bacterial leaf blight), specified to species and, where applicable, to pathovar or anastomosis group? | Simple | `Disease`, `hasCausalAgent`, `Pathogen` (→ NCBITaxon), `infraspecificRank` (pathovar, AG) | Establishes the disease–pathogen backbone to which all other modalities attach; infraspecific resolution matters because, e.g., Xoo and Xoc differ in epidemiology and host response. |
| CQ-TXT-02 | Which insect species are reported as vectors of RTBV and RTSV, and what transmission mode is reported for each? | Simple | `Virus` (→ NCBITaxon), `transmittedBy`, `VectorInsect`, `TransmissionMode`, `hasSource`, `SourceDocument` | Tungro management targets the vector rather than the virus, so vector relations are a prerequisite for any tungro reasoning. |
| CQ-TXT-03 | Which symptoms of rice blast are described in the literature for each affected plant organ (leaf blade, leaf collar, node, neck, panicle), and in which source documents? | Relational | `Disease`, `hasSymptom`, `Symptom` (qualities → PATO), `manifestsOn`, `PlantStructure` (→ PO), `describedIn`, `SourceDocument`, `TextSpan` | Organ-resolved textual symptom descriptions provide the reference vocabulary against which image annotations are aligned (CQ-MM-01, CQ-MM-07). |
| CQ-TXT-04 | Which control measures (cultural, biological, chemical) are recommended in extension documents for brown planthopper, and which of these measures are reported to induce pest resurgence? | Relational | `Pest`, `hasRecommendedControl`, `ControlMeasure` {`CulturalControl`, `BiologicalControl`, `ChemicalControl`} (→ AGROVOC), `hasActiveIngredient`, `reportedEffect`, `Resurgence`, `hasSource` | Insecticide-induced BPH resurgence is well documented; decision support must surface contraindications, not only recommendations. |
| CQ-TXT-05 | Which environmental conditions are reported as favourable for sheath blight development, with what numeric thresholds and units, and in which sources? | Relational | `Disease`, `favouredBy`, `EnvironmentalCondition` (→ PECO / ENVO), `onVariable`, `thresholdMin`, `thresholdMax`, `unit` (→ QUDT), `hasSource` | Machine-readable thresholds extracted from text form the knowledge-side bridge to sensor observations (CQ-MM-05, CQ-MM-13). |
| CQ-TXT-06 | For each disease and pest in scope, how many distinct sources report a quantitative yield-loss estimate, and what is the reported range (minimum–maximum %) per agroecosystem (irrigated vs. rainfed lowland)? | Complex-Inferential | `Disease` / `Pest`, `YieldLossReport`, `lossPercent`, `inAgroecosystem`, `hasSource`; COUNT, MIN, MAX, GROUP BY | Supports evidence-weighted prioritisation of surveillance and research targets. |
| CQ-TXT-07 | For which pest/disease–control-measure pairs do sources report conflicting efficacy outcomes, and what are the publication years, study locations, and study types of the conflicting sources? | Complex-Inferential | `EfficacyClaim` (reified, nanopublication pattern), `aboutControlMeasure`, `targets`, `efficacyOutcome`, `studyLocation`, `studyType`, `publicationYear`, `prov:wasDerivedFrom` | Exposes contested evidence explicitly, which is essential for trustworthy recommendations and requires claim-level provenance in the ontology. |

### 2.2 Image-grounded CQs

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-IMG-01 | Which images depict a specified symptom or damage type on a specified plant organ (e.g., spotted or unfilled grains attributed to rice bug feeding on the panicle)? | Simple | `Image`, `hasAnnotation`, `SymptomAnnotation`, `symptomType`, `onPlantStructure` (→ PO), `attributedTo` | Retrieval of visual evidence by symptom and organ is the entry point for every image-based diagnostic workflow. |
| CQ-IMG-02 | How many images are available per diagnostic class (each disease, each pest-damage type, and healthy baseline), broken down by image type (field vs. close-up)? | Simple | `Image`, `hasDiagnosticLabel`, `DiagnosticClass`, `HealthyBaseline`, `imageType`; COUNT … GROUP BY | Class balance determines whether downstream classifiers can be trained and evaluated fairly and exposes under-represented classes. |
| CQ-IMG-03 | Which images contain annotated regions of stem borer damage (yellow or white stem borer) distinguished as deadheart or whitehead, and at what growth stage was each image captured? | Relational | `Image`, `hasRegion`, `RegionOfInterest` (→ W3C Web Annotation selector), `damageType` {`Deadheart`, `Whitehead`}, `attributedTo`, `Pest`, `capturedAtGrowthStage`, `GrowthStage` (→ BBCH-rice / PO) | Stem borer symptoms are stage-dependent, so region-level visual evidence must be coupled to crop phenology. |
| CQ-IMG-04 | Which images carry two or more concurrent diagnostic labels (e.g., blast and brown spot lesions, or blast lesions and leaffolder feeding damage on the same leaf), and which label combinations occur? | Relational | `Image`, `hasDiagnosticLabel` (multi-valued), `DiagnosticClass`, `onPlantStructure` | Mixed infections and infestations are common in the field and must be representable to avoid forcing single-label diagnoses. |
| CQ-IMG-05 | For a given diseased image, which healthy-baseline images exist of the same plant organ, at the same growth stage, and from the same field plot or capture campaign? | Relational | `Image`, `HealthyBaseline`, `onPlantStructure`, `capturedAtGrowthStage`, `capturedInPlot`, `partOfCampaign` | Matched healthy controls are required for symptom-contrast learning and for expert visual comparison. |
| CQ-IMG-06 | Which pairs of diagnostic classes are most frequently confused by automated image classifiers (e.g., stem borer whitehead vs. neck blast; tungro yellowing vs. nitrogen deficiency), measured as images whose expert label differs from the model-predicted label? | Complex-Inferential | `Image`, `hasExpertLabel`, `hasPrediction`, `Prediction` (`predictedClass`, `confidence`, `prov:wasGeneratedBy` `Model`, `modelVersion`); GROUP BY (expert, predicted) | Identifies look-alike classes where visual evidence alone is insufficient, directly motivating the fusion CQs in Section 2.5. |
| CQ-IMG-07 | For which images do independent expert annotators disagree on the diagnostic label, or differ by two or more classes on the IRRI SES severity scale, and what is the inter-annotator agreement rate per diagnostic class? | Complex-Inferential | `Image`, `hasAnnotation`, `Annotation` (`label`, `sesScore`), `annotatedBy`, `Annotator` (→ `prov:Agent`), `SeverityScale` (→ IRRI SES via CO_320 scale); agreement aggregation | Quantifies label reliability, which bounds the achievable accuracy of any image-based diagnosis and informs the evaluation design. |

### 2.3 Sensor/environmental-grounded CQs

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-ENV-01 | What were the daily mean air temperature, maximum relative humidity, and cumulative rainfall recorded at station [S] on date [D]? | Simple | `Platform` (→ `sosa:Platform`), `Sensor`, `Observation` (→ `sosa:Observation`), `observedProperty`, `hasSimpleResult`, `resultTime` (→ OWL-Time), `unit` (→ QUDT) | The most basic environmental lookup; validates that sensor streams are ingested with correct units and timestamps. |
| CQ-ENV-02 | Which sensors are deployed in field plot [P], which environmental properties does each observe, and at what sampling interval and installation height or depth? | Simple | `FieldPlot` (→ `sosa:FeatureOfInterest`), `Sensor`, `isHostedBy`, `Platform`, `observes`, `ObservableProperty`, `samplingInterval`, `installationHeightOrDepth` | Deployment metadata are a precondition for aligning observations spatially and temporally with images and plots. |
| CQ-ENV-03 | For field plot [P], on how many hours per day was relative humidity ≥ 90 % or leaf wetness detected between dates [D1] and [D2]? | Relational | `FieldPlot`, `hasSensor`, `Observation`, `observedProperty` {`RelativeHumidity`, `LeafWetness`}, `resultTime`; FILTER + daily aggregation | Leaf-wetness duration and near-saturation humidity are principal drivers of blast infection and must be derivable as daily indicators. |
| CQ-ENV-04 | Which field plots in administrative district [X] recorded a daily mean temperature above 28 °C together with a daily mean relative humidity above 85 % on at least one day in month [M]? | Relational | `AdministrativeArea` (→ GADM / GeoNames), `geo:sfContains`, `FieldPlot`, `Platform`, `DailySummary`, `meanTemperature`, `meanRelativeHumidity` | District-level aggregation matches the spatial unit at which extension services plan interventions. |
| CQ-ENV-05 | Which field plots experienced three or more consecutive nights with minimum temperature between 20 and 26 °C and relative humidity above 90 % during the current season, and when did each such episode begin and end? | Complex-Inferential | `DailySummary`, `minTemperature`, `nightRelativeHumidity`, `ConditionEpisode` (derived; → `time:ProperInterval`), `hasBeginning`, `hasEnd`, `FieldPlot`, `Season` | Multi-day episode detection is the temporal primitive underlying disease-risk rules and must be materialised as first-class entities to be queryable. |
| CQ-ENV-06 | How do cumulative rainfall and mean soil moisture recorded during the wet season of year [Y] deviate from the multi-year seasonal mean for the same plots, and which plots show the largest anomalies? | Complex-Inferential | `FieldPlot`, `Season`, `SeasonalAggregate`, `cumulativeRainfall`, `meanSoilMoisture`, `baselinePeriod`; comparison and ranking | Seasonal anomalies contextualise outbreak years and help distinguish climatic from management drivers. |

### 2.4 Genomic/tabular-grounded CQs

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-GEN-01 | Which bacterial leaf blight resistance genes are carried by variety [V] (e.g., IR64, Ciherang, Inpari 32 HDB), and is each gene dominant or recessive? | Simple | `Variety` (→ CO_320 germplasm / AGROVOC), `carriesGene`, `ResistanceGene`, `confersResistanceTo`, `Disease`, `inheritanceMode` | Variety–gene lookup is the most frequent query from breeders and extension officers selecting varieties. |
| CQ-GEN-02 | On which chromosome and within which mapped interval of the reference assembly (e.g., IRGSP-1.0) is resistance gene [G] (e.g., Xa21, Pi9) located, and which reference-genome locus identifier or flanking markers define that position? | Simple | `Gene` (→ SO), `locatedOn`, `Chromosome`, `mappedInterval`, `referenceAssembly`, `locusIdentifier` (RAP-DB, MSU), `flankedBy`, `Marker` | Several major R genes were introgressed from wild relatives and are absent from the Nipponbare reference, so the ontology must support positions expressed as marker-defined intervals as well as locus IDs. |
| CQ-GEN-03 | Which released varieties carry at least one major brown planthopper resistance gene (e.g., Bph3, Bph14, Bph17, Bph32), and against which BPH biotypes or virulent populations is resistance reported for each gene? | Relational | `Variety`, `releaseStatus`, `carriesGene`, `ResistanceGene`, `effectiveAgainst`, `PestPopulation` / `PestBiotype`, `Pest` (→ NCBITaxon) | BPH resistance is population-specific, so gene–population relations are needed to anticipate resistance breakdown. |
| CQ-GEN-04 | Which molecular markers are diagnostic for resistance gene [G] (e.g., xa5, Xa21, Pi-ta), and which varieties or breeding lines have been genotyped as carrying the resistance allele at those markers? | Relational | `Marker` (SSR, SNP, functional), `diagnosticFor`, `Gene`, `GenotypeCall`, `calledAllele`, `Variety` / `BreedingLine` | Supports marker-assisted selection and verifies that gene–variety assertions rest on genotype evidence rather than pedigree inference alone. |
| CQ-GEN-05 | Which varieties pyramid two or more bacterial leaf blight resistance genes (e.g., Xa4 + xa5 + Xa21), and how does their mean grain yield in multi-location trials compare with that of varieties carrying a single resistance gene? | Complex-Inferential | `Variety`, `carriesGene` (COUNT ≥ 2), `YieldTrial` (→ AgrO), `trialSite`, `Season`, `grainYield` (t ha⁻¹); aggregation and comparison | Tests for a yield penalty associated with gene pyramiding, a key trade-off in variety recommendation. |
| CQ-GEN-06 | For which resistance genes do screening-trial records show declining effectiveness over time, i.e., an increasing proportion of susceptible-class SES scores among carrier varieties across successive trial years? | Complex-Inferential | `ResistanceGene`, `Variety`, `ScreeningTrial`, `challengeIsolate` / `PathogenRace`, `trialYear`, `sesScore`, `SeverityScale`; temporal trend aggregation | Detects resistance breakdown from structured phenotyping data; the tabular counterpart of the field-image evidence in CQ-MM-06. |

### 2.5 Cross-modal/fusion CQs

Modality codes: **T** = Text, **I** = Image, **S** = Sensor/environmental, **G** = Genomic/tabular.

| ID | Question | Complexity | Key Entities & Relations | Rationale |
|---|---|---|---|---|
| CQ-MM-01 (T×I) | For a given annotated field image, which literature sources describe the symptom class assigned to it, and which text passages contain those descriptions? | Simple | `Image`, `hasDiagnosticLabel`, `Symptom`, `describedIn`, `SourceDocument`, `TextSpan` (→ Web Annotation `TextQuoteSelector` / NIF) | Grounds each visual diagnosis in citable textual evidence, providing explainability to end users. |
| CQ-MM-02 (I×S) | Which sensor stations lie within [R] m of the capture location of image [I], and what were their temperature, relative humidity, and leaf-wetness readings at the observation nearest to the capture timestamp? | Relational | `Image`, `capturedAt` (→ GeoSPARQL `geo:Point`), `capturedOn`, `Platform`, `geof:distance`, `Observation`, `resultTime` | Tests the elementary spatio-temporal join on which all image–sensor fusion depends. |
| CQ-MM-03 (I×G) | Which variety is recorded for the plant depicted in image [I], and which resistance genes does that variety carry? | Simple | `Image`, `depictsPlantOf`, `Variety`, `carriesGene`, `ResistanceGene` | Links visual observations to host genotype, the minimal alignment required for resistance-aware diagnosis. |
| CQ-MM-04 (T×G) | According to the literature, which *M. oryzae* avirulence (AVR) effector is recognised by each blast resistance gene recorded in the KG (e.g., Pi-ta–AVR-Pita, Pik–AVR-Pik), and which varieties carry those genes? | Relational | `ResistanceGene`, `recognises`, `AvirulenceGene` (→ PHI-base), `Pathogen`, `hasSource`, `Variety`, `carriesGene` | Encodes gene-for-gene relationships from literature and connects them to germplasm, enabling reasoning about which pathogen populations a variety can resist. |
| CQ-MM-05 (T×S) | Which field plots currently satisfy the literature-reported favourable conditions for bacterial leaf blight (temperatures within the reported optimum range combined with high humidity and recent heavy rainfall or strong wind), and which sources define those conditions? | Relational | `EnvironmentalCondition` (text-derived thresholds), `hasSource`, `FieldPlot`, `DailySummary`, `satisfiesCondition` (derived) | Operationalises textual epidemiological knowledge as sensor-evaluable alert rules with traceable provenance. |
| CQ-MM-06 (I×G) | Which images with an expert-confirmed diagnosis of disease [D] depict plants of varieties recorded as carrying a resistance gene against [D], and in which plots and seasons were they captured? | Relational | `Image`, `hasExpertLabel`, `Disease`, `depictsPlantOf`, `Variety`, `carriesGene`, `ResistanceGene`, `confersResistanceTo`, `capturedInPlot`, `Season` | Flags candidate field cases of resistance breakdown (or misdiagnosis) that warrant pathogen sampling. |
| CQ-MM-07 (T×I) | Which automated image-based diagnoses are inconsistent with textual domain knowledge, i.e., the predicted disease or pest is not documented to affect the plant organ, or to occur at the growth stage, annotated for that image (e.g., a neck-blast prediction on a vegetative-stage image)? | Complex-Inferential | `Prediction`, `predictedClass`, `Image`, `onPlantStructure`, `capturedAtGrowthStage`, `Disease`, `affectsOrgan`, `occursDuringStage` (text-derived); FILTER NOT EXISTS | Uses the KG as a knowledge-based consistency check on machine-learning outputs, a core benefit of fusing text with images. |
| CQ-MM-08 (I×S) | Which environmental conditions over the 7–14 days preceding image capture are most strongly associated with image-confirmed sheath blight occurrences, compared with healthy-baseline images from the same plots and growth stages? | Complex-Inferential | `Image`, `hasExpertLabel`, `HealthyBaseline`, `capturedInPlot`, `capturedOn`, `DailySummary`, `ConditionEpisode`, `time:before`, `AssociationFinding` (materialised: `variable`, `effectSize`, `method`) | Derives empirically grounded risk indicators from the KG's own observations rather than from literature alone. |
| CQ-MM-09 (I×G) | What is the mean image-derived leaf-blast SES severity score for varieties carrying Pi9 or Pi2 compared with varieties carrying no known major blast resistance gene, per season and site? | Complex-Inferential | `Image`, `hasSeverityScore`, `depictsPlantOf`, `Variety`, `carriesGene`, `Season`, `Site`; AVG … GROUP BY | Provides field-level, image-based validation of resistance-gene performance under natural infection. |
| CQ-MM-10 (S×G) | Which varieties planted in plot–seasons with at least [N] days of relative humidity ≥ 95 % between maximum tillering and heading nevertheless received resistant-class sheath blight SES scores in the agronomic records, and which resistance QTLs do they carry? | Complex-Inferential | `Variety`, `PlantingRecord`, `FieldPlot`, `Season`, `GrowthStageInterval`, `DailySummary`, `SheathBlightScore`, `carriesQTL`, `QTL` | Identifies germplasm performing well under documented high disease pressure, which is more informative than screening under unrecorded conditions. |
| CQ-MM-11 (T×I×S) | For each outbreak reported in surveillance bulletins for district [X], were there earlier image-confirmed symptoms and sensor-recorded favourable conditions in that district, and what was the lead time between the first image evidence and the official report? | Complex-Inferential | `OutbreakReport` (text-derived), `reportedFor`, `reportedIn` `AdministrativeArea`, `publicationDate`, `Image`, `capturedOn`, `ConditionEpisode`, OWL-Time temporal ordering | Quantifies the early-warning value of the multimodal KG relative to conventional text-based surveillance. |
| CQ-MM-12 (T×S×G) | Which plots recorded green leafhopper light-trap counts above the literature-reported action threshold during the past [N] days and are planted with varieties lacking tungro resistance, and which management measures (e.g., synchronous planting, resistant-variety rotation) does the literature recommend for such situations? | Complex-Inferential | `TrapObservation` (→ `sosa:Observation`), `VectorInsect`, `ActionThreshold` (text-derived), `FieldPlot`, `PlantingRecord`, `Variety`, `lacksResistanceTo`, `Disease`, `ControlMeasure`, `hasSource` | Couples vector monitoring with host susceptibility and textual management knowledge, reflecting how tungro is managed in practice. |
| CQ-MM-13 (T×I×S×G) | Given an image confirming brown planthopper hopperburn in plot [P], which plots within [R] km are planted with varieties lacking any BPH resistance gene reported as effective against the locally documented BPH population, and which of these plots recorded conditions favourable to BPH population growth, as defined in the literature, during the past 14 days? | Complex-Inferential | `Image`, `hasExpertLabel` (`Hopperburn`), `capturedInPlot`, `geof:distance`, `FieldPlot`, `PlantingRecord`, `Variety`, `carriesGene`, `effectiveAgainst`, `PestPopulation`, `EnvironmentalCondition` (text-derived), `DailySummary` | Supports area-wide, spatially explicit BPH risk assessment, including exposure to BPH-transmitted grassy stunt and ragged stunt viruses, which no single modality can deliver. |
| CQ-MM-14 (T×I×S×G) | Given a new field image from plot [P] showing yellowish-white leaf lesions progressing from the leaf tip with wavy margins, together with the preceding 7-day sensor record for [P], which disease hypothesis is best supported by the combined image, sensor, and literature evidence, and which varieties adapted to the same agroecosystem carry resistance genes effective against the pathogen races reported in that region? | Complex-Inferential | `Image`, `Prediction`, `DiagnosticHypothesis` (reified: `supportedBy` `ImageEvidence` / `SensorEvidence` / `TextEvidence`, `confidence`), `Disease`, `PathogenRace`, `reportedInRegion`, `Variety`, `adaptedTo` `Agroecosystem`, `carriesGene`, `effectiveAgainst` | The end-to-end diagnosis-to-recommendation chain; the exemplary CQ justifying a multimodal KG rather than federated unimodal databases. |

---

## 3. Modality-Pair Coverage

"Dedicated" CQs target exactly the listed combination; "higher-order" CQs exercise the combination as part of a larger fusion.

| Modality combination | Dedicated CQs | Also exercised by (higher-order) | Coverage assessment |
|---|---|---|---|
| T × I | CQ-MM-01, CQ-MM-07 | CQ-MM-11, CQ-MM-13, CQ-MM-14 | Adequate |
| T × S | CQ-MM-05 | CQ-MM-11, CQ-MM-12, CQ-MM-13, CQ-MM-14 | Adequate through higher-order CQs; one dedicated pairwise CQ |
| T × G | CQ-MM-04 | CQ-MM-12, CQ-MM-13, CQ-MM-14 | Adequate through higher-order CQs; one dedicated pairwise CQ |
| I × S | CQ-MM-02, CQ-MM-08 | CQ-MM-11, CQ-MM-13, CQ-MM-14 | Adequate |
| I × G | CQ-MM-03, CQ-MM-06, CQ-MM-09 | CQ-MM-13, CQ-MM-14 | Strong |
| S × G | CQ-MM-10 | CQ-MM-12, CQ-MM-13, CQ-MM-14 | Thin; one dedicated CQ |
| T × I × S | CQ-MM-11 | CQ-MM-13, CQ-MM-14 | Adequate |
| T × S × G | CQ-MM-12 | CQ-MM-13, CQ-MM-14 | Adequate |
| T × I × G | — | CQ-MM-13, CQ-MM-14 | **Gap:** no dedicated CQ |
| I × S × G | — | CQ-MM-13, CQ-MM-14 | **Gap:** no dedicated CQ |
| T × I × S × G | CQ-MM-13, CQ-MM-14 | — | Adequate |

**Optional candidate CQs to close the gaps** (not counted in the 40 above):

| Candidate ID | Combination | Question |
|---|---|---|
| CQ-MM-C1 | T × I × G | For images of varieties carrying resistance gene [G] that nevertheless show symptoms of the target disease, which pathogen races reported in the literature to overcome [G] have been documented in the region of capture? |
| CQ-MM-C2 | I × S × G | Under comparable sensor-recorded humidity regimes, how does image-derived lesion severity differ between varieties carrying and lacking resistance gene [G] (genotype × environment interaction)? |
| CQ-MM-C3 | S × G | Which resistance genes show temperature-dependent effectiveness, i.e., differing proportions of resistant-class screening scores between trials whose sensor-recorded mean temperature falls above versus below [T] °C? |

---

## 4. Scope Boundary Note

On the basis of the CQs above, the KG is in scope for the taxonomic, symptomatic, epidemiological, and management knowledge of the listed rice diseases and pests; annotated image evidence at image and region level, including expert labels, severity scores, and reified classifier predictions; sensor-derived environmental and insect-trap observations together with their derived daily, episodic, and seasonal aggregates; and variety-level resistance genes, QTLs, markers, screening, and yield-trial records, as well as the spatial, temporal, and provenance links that connect these modalities. Out of scope are raw pixel data and embedding vectors as queryable KG objects, raw sequence data (reads, whole-genome assemblies, and variant files beyond marker calls), the training of predictive models (only their outputs, with provenance, are represented), socio-economic and market data, post-harvest and storage pests, and vertebrate pests such as rodents and birds. Nutrient deficiencies and abiotic stresses are represented only as differential classes that support disambiguation (CQ-IMG-06), not as primary modelling targets. Because several CQs depend on derived analytic results rather than on stored facts alone, the ontology must treat condition episodes, association findings, diagnostic hypotheses, and literature claims as first-class, provenance-bearing entities.

### 4.1 CQs flagged for potential infeasibility

| CQ(s) | Feasibility risk | Suggested mitigation |
|---|---|---|
| CQ-MM-02, -06, -08, -09, -11, -13, -14 | Require georeferenced, timestamped images linked to plots and varieties; many public rice-disease image datasets lack GPS, date, and variety metadata. | Collect a dedicated field campaign with mandatory capture metadata; treat metadata-less public images as unimodal training data only. |
| CQ-ENV-05, CQ-MM-08, CQ-MM-11 | SPARQL alone is poorly suited to consecutive-event detection and statistical association. | Materialise `DailySummary`, `ConditionEpisode`, and `AssociationFinding` entities in an ETL/analytics layer; SPARQL then retrieves the results. |
| CQ-TXT-07 | Claim-level extraction with efficacy polarity is error-prone on agronomic text. | Restrict to a curated subset or expert-verified nanopublications. |
| CQ-IMG-07 | Multiple independent annotations per image are rarely available. | Double-annotate a stratified subsample. |
| CQ-GEN-06, CQ-MM-14 | Require multi-year screening with consistent differential isolates and regional pathogen race/pathotype surveys, which are sparse. | Restrict to genes with documented screening histories; allow CQ-MM-14 to degrade to a gene-level answer when race data are absent. |
| CQ-MM-10 | Sheath blight resistance is largely quantitative; QTL evidence is sparse and population-specific. | Represent QTLs with source population, effect size, and confidence. |
| CQ-MM-12 | Automated light-trap counts are not standard in IoT deployments. | Accept manual trap counts as tabular observations mapped to SOSA. |
| CQ-MM-13 | Local BPH virulence data are scarce, and the classical biotype concept describes field populations imperfectly. | Model `PestPopulation` with virulence-assay results rather than fixed biotype labels. |

---

## Appendix A. Proposed Ontology Alignment Targets

| KG element | Proposed alignment target(s) | Exercised by |
|---|---|---|
| Organisms (pathogens, pests, vectors, rice) | NCBI Taxonomy; AGROVOC for common names | CQ-TXT-01, -02; CQ-GEN-03 |
| Diseases and infection processes | AGROVOC; Infectious Disease Ontology (IDO) core patterns for infection and disposition | Throughout |
| Plant structures and growth stages | Plant Ontology (PO); BBCH-rice scale; Plant Phenology Ontology (PPO) for phenological observations | CQ-TXT-03; CQ-IMG-03, -05; CQ-MM-07 |
| Traits, phenotypes, severity scales | Crop Ontology Rice Trait Ontology (CO_320, trait–method–scale); Plant Trait Ontology (TO); PATO; IRRI SES | CQ-IMG-07; CQ-GEN-06; CQ-MM-09, -10 |
| Genes, loci, markers, effectors | Sequence Ontology (SO); Gene Ontology (GO); RAP-DB and MSU locus IDs; Oryzabase gene symbols; PHI-base | CQ-GEN-02, -04; CQ-MM-04 |
| Sensors and observations | W3C/OGC SOSA/SSN; QUDT units; OWL-Time | CQ-ENV-01 to -06; CQ-MM-02, -12 |
| Environmental context | ENVO; Plant Experimental Conditions Ontology (PECO) | CQ-TXT-05; CQ-MM-05 |
| Space | GeoSPARQL; GADM or GeoNames for administrative units | CQ-ENV-04; CQ-MM-02, -11, -13 |
| Image regions and text anchors | W3C Web Annotation Data Model (selectors); NIF (optional) | CQ-IMG-03; CQ-MM-01 |
| Provenance, predictions, claims | PROV-O; nanopublication pattern | CQ-TXT-07; CQ-IMG-06; CQ-MM-07, -14 |
| Trials and management | Agronomy Ontology (AgrO); AGROVOC | CQ-TXT-04; CQ-GEN-05 |

**Note on "PPO".** The source prompt expands PPO as "Plant Phenotype Ontology". The published PPO is the *Plant Phenology Ontology* (Stucky et al., 2018), which models phenological stages and observations. Plant phenotypes and traits are better covered by TO, CO_320, and PATO. It is recommended that the acronym be corrected in the manuscript and that PPO be cited for phenology only.

---

## Appendix B. Methodological References

*Bibliographic details should be verified against the original sources before submission.*

- Bezerra, C., Freitas, F., & Santana, F. (2013). Evaluating ontologies with competency questions. *Proceedings of the 2013 IEEE/WIC/ACM International Joint Conferences on Web Intelligence and Intelligent Agent Technologies (WI-IAT)*.
- Grüninger, M., & Fox, M. S. (1995). Methodology for the design and evaluation of ontologies. *Proceedings of the IJCAI-95 Workshop on Basic Ontological Issues in Knowledge Sharing*.
- Haller, A., Janowicz, K., Cox, S. J. D., Lefrançois, M., Taylor, K., Le Phuoc, D., Lieberman, J., García-Castro, R., Atkinson, R., & Stadler, C. (2019). The modular SSN ontology: A joint W3C and OGC standard specifying the semantics of sensors, observations, sampling, and actuation. *Semantic Web*, 10(1), 9–32.
- IRRI. (2013). *Standard Evaluation System (SES) for Rice* (5th ed.). International Rice Research Institute.
- Ren, Y., Parvizi, A., Mellish, C., Pan, J. Z., van Deemter, K., & Stevens, R. (2014). Towards competency question-driven ontology authoring. In *The Semantic Web: Trends and Challenges (ESWC 2014)*, LNCS 8465. Springer.
- Stucky, B. J., Guralnick, R., Deck, J., Denny, E. G., Bolmgren, K., & Walls, R. (2018). The Plant Phenology Ontology: A new informatics resource for large-scale integration of plant phenology data. *Frontiers in Plant Science*, 9, 517.
- Suárez-Figueroa, M. C., Gómez-Pérez, A., Motta, E., & Gangemi, A. (Eds.). (2012). *Ontology Engineering in a Networked World*. Springer.
- Uschold, M., & King, M. (1995). Towards a methodology for building ontologies. *Proceedings of the IJCAI-95 Workshop on Basic Ontological Issues in Knowledge Sharing*.
