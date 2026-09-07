# Stage 3 - Scope gate and grouping

Generated 2026-09-07 20:45. **65 Tier A CQs in -> 56 keep, 8 drop, 23 groups.**

> **Declared conflict of interest.** This grouping was drafted by Claude Opus 5, one of the five models whose output forms the pool, so a model graded its own work. It was reviewed and approved by M. A. Furqon on 2026-09-03. Describe it in writing as an LLM-assisted first pass, human-adjudicated.

## Groups

`n_models` = how many of the five models proposed this group independently.

| Group | n_models | CQs | Question |
|---|---|---|---|
| `G01` | 4 | 4 | Pathogen causing a disease, and its taxonomy |
| `G02` | 4 | 4 | Vector transmitting a pathogen or viral disease |
| `G03` | 2 | 3 | Symptoms of a disease, by organ and growth stage |
| `G04` | 4 | 5 | Diseases sharing symptoms, and what discriminates them |
| `G05` | 1 | 1 | Environmental conditions favouring a disease or pest |
| `G06` | 1 | 1 | Growth stage at which a pest or disease is most damaging |
| `G07` | 4 | 4 | Recommended control measures, by category and source |
| `G08` | 1 | 1 | Natural enemies of a pest |
| `G09` | 1 | 1 | Distinguishing a nutritional disorder from a disease |
| `G10` | 4 | 4 | Images showing a given condition or symptom |
| `G11` | 1 | 1 | Provenance and confidence of an image annotation |
| `G12` | 1 | 1 | Disagreement between model and expert annotations |
| `G13` | 2 | 2 | Distribution of the image corpus |
| `G14` | 3 | 3 | Plant organ depicted in an image |
| `G15` | 2 | 2 | Symptoms annotated in a given image |
| `G16` | 3 | 4 | Disease or pest supported by visual evidence |
| `G17` | 4 | 4 | Visual features separating confusable conditions |
| `G18` | 2 | 2 | Severity of the damage in an image |
| `G19` | 1 | 1 | Symptoms co-occurring in one image |
| `G20` | 1 | 1 | Growth stage visible in a canopy image |
| `G21` | 2 | 2 | Literature symptoms with and without image support |
| `G22` | 2 | 4 | Literature disease matching an image |
| `G23` | 1 | 1 | Treatment prescribed for an imaged condition |

---

## Group contents

### G01 - Pathogen causing a disease, and its taxonomy

> Which pathogen causes a given rice disease, and to which taxonomic group does it belong?

*4 models: Claude Fable 5.1, Claude Opus 5, GPT-5.6 Sol, Gemini Pro 3.1*

- **1.** `P031` (Claude Fable 5.1)
  > What is the causal agent of a given rice disease (e.g., bacterial leaf blight), and to which taxonomic group (fungus, bacterium, virus) does it belong?
- **2.** `P067` (Claude Opus 5)
  > What is the causal agent of rice blast, under which accepted taxonomic name and which recorded synonyms (e.g., *Magnaporthe oryzae* / *Pyricularia oryzae*), and to which pathogen type (fungus, bacterium, virus, insect) does it belong?
- **4.** `P169` (Gemini Pro 3.1)
  > What is the causal pathogen of Rice Blast?
- **5.** `P103` (GPT-5.6 Sol)
  > What causal pathogens are associated with rice blast, bacterial leaf blight, and sheath blight?

### G02 - Vector transmitting a pathogen or viral disease

> Which vector species transmits which pathogen or viral disease, and by which transmission mode?

*4 models: Claude Fable 5.1, Claude Opus 5, Gemini Flash 3.8, Gemini Pro 3.1*

- **6.** `P138` (Gemini Flash 3.8) - **also covers causation; overlaps G01**
  > Which causal pathogen, taxonomic rank, and primary transmission vectors are associated with Rice Tungro Disease?
- **7.** `P170` (Gemini Pro 3.1)
  > Which rice diseases are documented as being transmitted by the vector *Nilaparvata lugens* (Brown Planthopper)?
- **8.** `P032` (Claude Fable 5.1)
  > Which insect species act as vectors for rice tungro disease, and which viruses (RTBV, RTSV) do they transmit?
- **9.** `P070` (Claude Opus 5) - **adds transmission mode - new property**
  > Which arthropod species are reported as vectors of which viral rice diseases, and by which transmission mode (persistent, semi-persistent, non-persistent)?

### G03 - Symptoms of a disease, by organ and growth stage

> Which symptoms does a given disease produce, on which plant organ, and at which growth stage?

*2 models: Claude Opus 5, GPT-5.6 Sol*

- **3.** `P104` (GPT-5.6 Sol)
  > What symptoms are reported in scientific and extension literature for rice blast caused by *Magnaporthe oryzae*?
- **14.** `P068` (Claude Opus 5) - **adds organ + growth stage**
  > Which symptoms are described for bacterial leaf blight, on which plant organs, and at which crop growth stages?
- **15.** `P106` (GPT-5.6 Sol)
  > Which plant organs are reported to be affected by rice blast, bacterial leaf blight, sheath blight, tungro disease, stem borer, and rice bug?

### G04 - Diseases sharing symptoms, and what discriminates them

> Which diseases or pests share overlapping symptoms, and which symptoms discriminate between them?

*4 models: Claude Fable 5.1, Claude Opus 5, GPT-5.6 Sol, Gemini Pro 3.1*

- **10.** `P108` (GPT-5.6 Sol)
  > Which rice diseases or pests have overlapping symptoms but different causal agents and management recommendations?
- **11.** `P172` (Gemini Pro 3.1)
  > Which diseases share overlapping textual symptom descriptions regarding "leaf chlorosis" or "yellowing"?
- **12.** `P105` (GPT-5.6 Sol)
  > Which rice diseases are reported to share visually similar leaf symptoms?
- **13.** `P071` (Claude Opus 5)
  > Which pairs of diseases share the largest number of textually described leaf symptoms, and what are the discriminating symptoms that separate each pair?
- **29.** `P035` (Claude Fable 5.1)
  > Which symptom descriptors (e.g., "diamond-shaped lesion with grey centre") are associated with more than one condition in the literature, and thus constitute ambiguous diagnostic evidence?

### G05 - Environmental conditions favouring a disease or pest

> Which environmental conditions are reported to favour a given disease or pest?

*1 models: GPT-5.6 Sol*

- **16.** `P107` (GPT-5.6 Sol)
  > Which environmental conditions are reported to favor outbreaks of rice blast, bacterial leaf blight, and brown planthopper infestation?

### G06 - Growth stage at which a pest or disease is most damaging

> At which growth stages is a given disease or pest reported as most damaging?

*1 models: Claude Fable 5.1*

- **17.** `P033` (Claude Fable 5.1)
  > At which rice growth stages (e.g., seedling, tillering, booting, heading, ripening) is a given pest or disease reported as most damaging?

### G07 - Recommended control measures, by category and source

> Which control measures are recommended for a given disease or pest, of which management category, and on which source authority?

*4 models: Claude Fable 5.1, Claude Opus 5, Gemini Flash 3.8, Gemini Pro 3.1*

- **18.** `P139` (Gemini Flash 3.8) - **adds growth stage**
  > What chemical active ingredients and recommended cultural sanitation practices are prescribed for managing Sheath Blight (*Rhizoctonia solani*) across different rice growth stages?
- **19.** `P034` (Claude Fable 5.1)
  > Which management practices (cultural, biological, chemical) are recommended in extension literature for a given condition, and which active ingredients or biocontrol agents do they involve?
- **20.** `P171` (Gemini Pro 3.1)
  > What are the recommended chemical or biological control agents for managing Sheath Blight (*Rhizoctonia solani*)?
- **22.** `P069` (Claude Opus 5) - **adds source document**
  > Which control measures are recommended for brown planthopper, of which management category (chemical, biological, cultural, host resistance), at which growth stage, and in which source document?

### G08 - Natural enemies of a pest

> Which natural enemies are documented as predators or parasitoids of a given pest?

*1 models: Gemini Flash 3.8*

- **21.** `P141` (Gemini Flash 3.8) - **needs NaturalEnemy class - not in v0.6**
  > Which biological control agents (e.g., *Trichogramma chilonis*, *Cyrtorhinus lividipennis*) exhibit documented predation or parasitism on Brown Planthopper (*Nilaparvata lugens*) egg masses or nymphs?

### G09 - Distinguishing a nutritional disorder from a disease

> Which features distinguish a nutritional disorder from a disease with similar visible symptoms?

*1 models: Gemini Flash 3.8*

- **28.** `P142` (Gemini Flash 3.8) - **needs nutritional disorder (zinc deficiency) - not in v0.6**
  > What secondary symptoms and physiological changes differentiate acute physiological zinc deficiency ("Khaira disease") from early-stage Rice Blast foliar lesions?

### G10 - Images showing a given condition or symptom

> Which images are annotated as showing a given condition or visual symptom?

*4 models: Claude Fable 5.1, Claude Opus 5, GPT-5.6 Sol, Gemini Pro 3.1*

- **30.** `P011` (Claude Fable 5.1) - **also asks annotation source, see G11**
  > Which images in the KG are annotated as showing a given condition (e.g., sheath blight), and what is the annotation source (expert, model, dataset label)?
- **39.** `P083` (GPT-5.6 Sol)
  > Which annotated images depict spindle-shaped lesions consistent with rice blast symptoms?
- **41.** `P047` (Claude Opus 5)
  > How many annotated images depict spindle-shaped lesions with grey centres and brown margins on the leaf blade, and which disease label is assigned to them?
- **48.** `P150` (Gemini Pro 3.1)
  > Are there authenticated field images depicting early-stage symptoms of the Rice Tungro Virus on whole plants?

### G11 - Provenance and confidence of an image annotation

> Who or what produced a given image annotation, and with what confidence?

*1 models: Claude Opus 5*

- **31.** `P050` (Claude Opus 5) - **needs annotator + confidence - confidenceScore unused in v0.6**
  > For each image annotation, who or what produced it (expert annotator, crowd worker, automated model), with what confidence score, and which annotations carry independent expert verification?

### G12 - Disagreement between model and expert annotations

> Where do model-generated and expert image annotations disagree, and on which conditions and plant parts?

*1 models: Claude Fable 5.1*

- **32.** `P015` (Claude Fable 5.1) - **needs both model and expert annotations - only dataset labels in v0.6**
  > Which pairs of conditions are most frequently confused in model-generated image annotations relative to expert annotations, and on which plant parts does this confusion concentrate?

### G13 - Distribution of the image corpus

> How is the image corpus distributed across conditions, plant parts, and capture types?

*2 models: Claude Fable 5.1, Claude Opus 5*

- **33.** `P013` (Claude Fable 5.1)
  > How many images per condition exist for each plant part and image type (field vs. close-up), and which condition–part combinations have fewer than N images?
- **51.** `P048` (Claude Opus 5) - **needs capture device + distance metadata**
  > Which images serve as healthy-plant baselines, and how are they distributed across growth stage, capture distance (canopy vs. close-up), and acquisition device?

### G14 - Plant organ depicted in an image

> Which plant organ is depicted in a given image?

*3 models: Claude Fable 5.1, GPT-5.6 Sol, Gemini Flash 3.8*

- **34.** `P120` (Gemini Flash 3.8) - **needs PlantPart class - not in v0.6**
  > Which anatomical plant organs (e.g., leaf sheath, collar, panicle neck, glume) exhibit localized visible lesions or discoloration in an annotated multi-organ plant photograph?
- **35.** `P082` (GPT-5.6 Sol) - **needs PlantPart class - not in v0.6**
  > Which plant organ is depicted in an image containing disease symptoms or pest damage?
- **43.** `P012` (Claude Fable 5.1) - **needs PlantPart + visual symptom class**
  > Which plant part (leaf, sheath, stem, panicle, whole plant) is depicted in a given image, and what visual symptom class (lesion, discolouration, wilting, hopperburn, deadheart, whitehead) is annotated?

### G15 - Symptoms annotated in a given image

> Which visible symptoms are annotated in a given image?

*2 models: GPT-5.6 Sol, Gemini Flash 3.8*

- **38.** `P081` (GPT-5.6 Sol) - **partial: 1,442 of 10,407 images carry a captures link (14%)**
  > What visible symptoms or damage patterns are annotated in a given rice image?
- **45.** `P118` (Gemini Flash 3.8)
  > Which visual symptom patterns (e.g., spindle-shaped / elliptical lesions with gray centers and reddish-brown borders) are present on the leaf blade regions of the uploaded specimen image?

### G16 - Disease or pest supported by visual evidence

> Which disease or pest is best supported by the visual evidence in a given image?

*3 models: GPT-5.6 Sol, Gemini Flash 3.8, Gemini Pro 3.1*

- **36.** `P085` (GPT-5.6 Sol) - **needs lesion shape/colour/distribution descriptors**
  > Which disease or pest class is best supported by the combination of lesion shape, lesion color, spatial distribution, and affected plant organ annotated in an image?
- **40.** `P148` (Gemini Pro 3.1)
  > Which specific disease is characterized by images showing spindle-shaped or diamond-shaped lesions with grey centers on leaves?
- **46.** `P121` (Gemini Flash 3.8)
  > Does the image depict mechanical feeding punctures, sooty mold residue, and "hopperburn" drying patterns characteristic of delphacid planthopper infestations?
- **47.** `P151` (Gemini Pro 3.1)
  > Which pests are associated with whole-field images showing "hopperburn" (large circular patches of dried/browning plants)?

### G17 - Visual features separating confusable conditions

> Which visual features separate two visually confusable conditions?

*4 models: Claude Opus 5, GPT-5.6 Sol, Gemini Flash 3.8, Gemini Pro 3.1*

- **37.** `P084` (GPT-5.6 Sol)
  > Which rice diseases or pest damage classes exhibit visually similar lesion, discoloration, wilting, or tissue-damage patterns in the image collection?
- **42.** `P051` (Claude Opus 5)
  > Which visual descriptors (lesion shape, lesion colour, halo presence, lesion distribution on the blade) most strongly separate brown spot from rice blast across the annotated image corpus?
- **44.** `P149` (Gemini Pro 3.1)
  > What visual features in close-up images distinguish Stem Borer "whitehead" damage from healthy rice panicles?
- **55.** `P122` (Gemini Flash 3.8)
  > How do lesion edge contours (water-soaked, wavy margin vs. sharp necrotic border) in leaf macro-photographs differentiate Bacterial Leaf Streak (*Xanthomonas oryzae* pv. *oryzicola*) from Narrow Brown Leaf Spot (*Cercospora janseana*)?

### G18 - Severity of the damage in an image

> How severe is the damage recorded in a given image?

*2 models: Claude Fable 5.1, Gemini Flash 3.8*

- **52.** `P014` (Claude Fable 5.1) - **needs severity grade per image - SeverityLevel unlinked in v0.6**
  > For a given image, which other images depict the same condition at the same growth stage but a different severity grade?
- **53.** `P119` (Gemini Flash 3.8) - **needs region-level lesion annotation - roadmap Phase 2**
  > What is the calculated percentage of leaf area affected by necrotic lesions (foliar severity index) across annotated regions in an image collection?

### G19 - Symptoms co-occurring in one image

> Which symptoms co-occur on the same plant within a single image?

*1 models: Claude Opus 5*

- **54.** `P049` (Claude Opus 5) - **needs multi-symptom annotation: every annotated image currently carries exactly one captures link**
  > Which images contain two or more distinct symptom types annotated on the same plant, and which symptom combinations co-occur most frequently?

### G20 - Growth stage visible in a canopy image

> Which growth stage is visually manifest in a whole-canopy image?

*1 models: Gemini Flash 3.8*

- **56.** `P123` (Gemini Flash 3.8) - **needs growth stage annotation on images**
  > What developmental growth stage (e.g., vegetative tillering, panicle initiation, physiological maturity) is visually manifest based on visible canopy morphology and floral emergence in the whole-canopy photograph?

### G21 - Literature symptoms with and without image support

> Which literature-described symptoms have supporting image evidence, and which do not?

*2 models: Claude Fable 5.1, Claude Opus 5*

- **57.** `P020` (Claude Fable 5.1)
  > Which textual symptom descriptors for a condition correspond to which visual symptom classes and plant parts in the annotated image corpus, and for which descriptors is there no supporting image?
- **63.** `P061` (Claude Opus 5)
  > Which symptom phenotypes present in the annotated image corpus have no corresponding textual symptom description in the KG, and conversely which literature-described symptoms are entirely unillustrated?

### G22 - Literature disease matching an image

> Which literature-described disease matches the symptoms annotated in a given image?

*2 models: Claude Opus 5, GPT-5.6 Sol*

- **58.** `P087` (GPT-5.6 Sol)
  > Does the lesion morphology visible in an image correspond to published descriptions of rice blast, bacterial leaf blight, or another candidate disease?
- **59.** `P088` (GPT-5.6 Sol)
  > Which candidate diseases should be included in a differential diagnosis when an image contains symptoms that the literature reports for multiple diseases?
- **60.** `P086` (GPT-5.6 Sol)
  > Which diseases or pests described in the literature have symptoms matching those annotated in a given rice image?
- **62.** `P053` (Claude Opus 5)
  > Given an image annotated with elongated water-soaked lesions with wavy yellow margins beginning at the leaf tip, which textually described diseases match that symptom profile, and what are their causal pathogens and recommended control measures?

### G23 - Treatment prescribed for an imaged condition

> Which treatment does the literature prescribe for a condition identified from an image?

*1 models: Gemini Pro 3.1*

- **61.** `P153` (Gemini Pro 3.1)
  > [Img × Txt] Given a leaf image showing spindle-shaped lesions, what are the corresponding chemical treatment protocols documented in extension literature?

---

## 8 CQs dropped

| # | pool_id | Reason | Question |
|---|---|---|---|
| 23 | `P140` | R3: incubation period not recorded in any source | How do excessive nitrogen fertilizer application rates influence the incubation period and lesion expansion ra |
| 24 | `P173` | R3: latency period not recorded in any source | Based on surveillance bulletins, what is the typical latency period for Bacterial Leaf Blight before symptoms  |
| 25 | `P072` | needs province-level surveillance statistics - no such data | For each disease in scope, how did reported incidence or affected area in surveillance bulletins for a given p |
| 26 | `P036` | needs province-level surveillance statistics - no such data | Which conditions have been reported in a given Indonesian province (e.g., East Java) in surveillance bulletins |
| 27 | `P143` | needs quarantine policy corpus - no such data | What quarantine regulations, surveillance protocols, and statutory notification thresholds are established by  |
| 49 | `P052` | needs repeated photography of one plot over a season - no such data | For a given field plot photographed repeatedly during one season, how did the annotated severity score and the |
| 50 | `P152` | needs plot-linked image time series - no such data | Given a time-series of close-up leaf images from a single plot, rank the progression severity of Bacterial Lea |
| 64 | `P029` | needs district surveillance records - no such data | Which conditions reported in surveillance bulletins for a district in a given season are corroborated by image |