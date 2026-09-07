# Worksheet: Tier A competency questions (text + image)

Every CQ here needs neither sensor nor genomic data, so all of them bear on the resource actually being released. Ordering places similar CQs next to each other.

Fill two columns in `data/worksheet_tierA.csv`:

- **KEEP_or_DROP** - `keep` or `drop`
- **GROUP_ID** - any number; CQs asking the same thing share a number

---


## TEXT (29 CQs)

**1.** `P031` - Claude Fable 5.1 - parameterised
> What is the causal agent of a given rice disease (e.g., bacterial leaf blight), and to which taxonomic group (fungus, bacterium, virus) does it belong?

**2.** `P067` - Claude Opus 5
> What is the causal agent of rice blast, under which accepted taxonomic name and which recorded synonyms (e.g., *Magnaporthe oryzae* / *Pyricularia oryzae*), and to which pathogen type (fungus, bacterium, virus, insect) does it belong?

**3.** `P104` - GPT-5.6 Sol
> What symptoms are reported in scientific and extension literature for rice blast caused by *Magnaporthe oryzae*?

**4.** `P169` - Gemini Pro 3.1
> What is the causal pathogen of Rice Blast?

**5.** `P103` - GPT-5.6 Sol
> What causal pathogens are associated with rice blast, bacterial leaf blight, and sheath blight?

**6.** `P138` - Gemini Flash 3.8
> Which causal pathogen, taxonomic rank, and primary transmission vectors are associated with Rice Tungro Disease?

**7.** `P170` - Gemini Pro 3.1
> Which rice diseases are documented as being transmitted by the vector *Nilaparvata lugens* (Brown Planthopper)?

**8.** `P032` - Claude Fable 5.1
> Which insect species act as vectors for rice tungro disease, and which viruses (RTBV, RTSV) do they transmit?

**9.** `P070` - Claude Opus 5
> Which arthropod species are reported as vectors of which viral rice diseases, and by which transmission mode (persistent, semi-persistent, non-persistent)?

**10.** `P108` - GPT-5.6 Sol
> Which rice diseases or pests have overlapping symptoms but different causal agents and management recommendations?

**11.** `P172` - Gemini Pro 3.1
> Which diseases share overlapping textual symptom descriptions regarding "leaf chlorosis" or "yellowing"?

**12.** `P105` - GPT-5.6 Sol
> Which rice diseases are reported to share visually similar leaf symptoms?

**13.** `P071` - Claude Opus 5
> Which pairs of diseases share the largest number of textually described leaf symptoms, and what are the discriminating symptoms that separate each pair?

**14.** `P068` - Claude Opus 5
> Which symptoms are described for bacterial leaf blight, on which plant organs, and at which crop growth stages?

**15.** `P106` - GPT-5.6 Sol
> Which plant organs are reported to be affected by rice blast, bacterial leaf blight, sheath blight, tungro disease, stem borer, and rice bug?

**16.** `P107` - GPT-5.6 Sol
> Which environmental conditions are reported to favor outbreaks of rice blast, bacterial leaf blight, and brown planthopper infestation?

**17.** `P033` - Claude Fable 5.1 - parameterised
> At which rice growth stages (e.g., seedling, tillering, booting, heading, ripening) is a given pest or disease reported as most damaging?

**18.** `P139` - Gemini Flash 3.8
> What chemical active ingredients and recommended cultural sanitation practices are prescribed for managing Sheath Blight (*Rhizoctonia solani*) across different rice growth stages?

**19.** `P034` - Claude Fable 5.1 - parameterised
> Which management practices (cultural, biological, chemical) are recommended in extension literature for a given condition, and which active ingredients or biocontrol agents do they involve?

**20.** `P171` - Gemini Pro 3.1
> What are the recommended chemical or biological control agents for managing Sheath Blight (*Rhizoctonia solani*)?

**21.** `P141` - Gemini Flash 3.8
> Which biological control agents (e.g., *Trichogramma chilonis*, *Cyrtorhinus lividipennis*) exhibit documented predation or parasitism on Brown Planthopper (*Nilaparvata lugens*) egg masses or nymphs?

**22.** `P069` - Claude Opus 5
> Which control measures are recommended for brown planthopper, of which management category (chemical, biological, cultural, host resistance), at which growth stage, and in which source document?

**23.** `P140` - Gemini Flash 3.8 - R3-NOSOURCE
> How do excessive nitrogen fertilizer application rates influence the incubation period and lesion expansion rate of Bacterial Leaf Blight (*Xanthomonas oryzae* pv. *oryzae*) according to extension publications?

**24.** `P173` - Gemini Pro 3.1 - R3-NOSOURCE
> Based on surveillance bulletins, what is the typical latency period for Bacterial Leaf Blight before symptoms become visible?

**25.** `P072` - Claude Opus 5 - parameterised
> For each disease in scope, how did reported incidence or affected area in surveillance bulletins for a given province change across seasons from 2019 to 2024, and which seasons exceeded the long-term reported mean?

**26.** `P036` - Claude Fable 5.1 - parameterised
> Which conditions have been reported in a given Indonesian province (e.g., East Java) in surveillance bulletins within a given year, ranked by reported affected area?

**27.** `P143` - Gemini Flash 3.8
> What quarantine regulations, surveillance protocols, and statutory notification thresholds are established by regional agricultural authorities for False Smut (*Ustilaginoidea virens*) outbreaks?

**28.** `P142` - Gemini Flash 3.8
> What secondary symptoms and physiological changes differentiate acute physiological zinc deficiency ("Khaira disease") from early-stage Rice Blast foliar lesions?

**29.** `P035` - Claude Fable 5.1
> Which symptom descriptors (e.g., "diamond-shaped lesion with grey centre") are associated with more than one condition in the literature, and thus constitute ambiguous diagnostic evidence?


## IMAGE (27 CQs)

**30.** `P011` - Claude Fable 5.1 - parameterised
> Which images in the KG are annotated as showing a given condition (e.g., sheath blight), and what is the annotation source (expert, model, dataset label)?

**31.** `P050` - Claude Opus 5
> For each image annotation, who or what produced it (expert annotator, crowd worker, automated model), with what confidence score, and which annotations carry independent expert verification?

**32.** `P015` - Claude Fable 5.1
> Which pairs of conditions are most frequently confused in model-generated image annotations relative to expert annotations, and on which plant parts does this confusion concentrate?

**33.** `P013` - Claude Fable 5.1
> How many images per condition exist for each plant part and image type (field vs. close-up), and which condition–part combinations have fewer than N images?

**34.** `P120` - Gemini Flash 3.8
> Which anatomical plant organs (e.g., leaf sheath, collar, panicle neck, glume) exhibit localized visible lesions or discoloration in an annotated multi-organ plant photograph?

**35.** `P082` - GPT-5.6 Sol
> Which plant organ is depicted in an image containing disease symptoms or pest damage?

**36.** `P085` - GPT-5.6 Sol
> Which disease or pest class is best supported by the combination of lesion shape, lesion color, spatial distribution, and affected plant organ annotated in an image?

**37.** `P084` - GPT-5.6 Sol
> Which rice diseases or pest damage classes exhibit visually similar lesion, discoloration, wilting, or tissue-damage patterns in the image collection?

**38.** `P081` - GPT-5.6 Sol - parameterised
> What visible symptoms or damage patterns are annotated in a given rice image?

**39.** `P083` - GPT-5.6 Sol
> Which annotated images depict spindle-shaped lesions consistent with rice blast symptoms?

**40.** `P148` - Gemini Pro 3.1
> Which specific disease is characterized by images showing spindle-shaped or diamond-shaped lesions with grey centers on leaves?

**41.** `P047` - Claude Opus 5
> How many annotated images depict spindle-shaped lesions with grey centres and brown margins on the leaf blade, and which disease label is assigned to them?

**42.** `P051` - Claude Opus 5
> Which visual descriptors (lesion shape, lesion colour, halo presence, lesion distribution on the blade) most strongly separate brown spot from rice blast across the annotated image corpus?

**43.** `P012` - Claude Fable 5.1 - parameterised
> Which plant part (leaf, sheath, stem, panicle, whole plant) is depicted in a given image, and what visual symptom class (lesion, discolouration, wilting, hopperburn, deadheart, whitehead) is annotated?

**44.** `P149` - Gemini Pro 3.1
> What visual features in close-up images distinguish Stem Borer "whitehead" damage from healthy rice panicles?

**45.** `P118` - Gemini Flash 3.8
> Which visual symptom patterns (e.g., spindle-shaped / elliptical lesions with gray centers and reddish-brown borders) are present on the leaf blade regions of the uploaded specimen image?

**46.** `P121` - Gemini Flash 3.8
> Does the image depict mechanical feeding punctures, sooty mold residue, and "hopperburn" drying patterns characteristic of delphacid planthopper infestations?

**47.** `P151` - Gemini Pro 3.1
> Which pests are associated with whole-field images showing "hopperburn" (large circular patches of dried/browning plants)?

**48.** `P150` - Gemini Pro 3.1
> Are there authenticated field images depicting early-stage symptoms of the Rice Tungro Virus on whole plants?

**49.** `P052` - Claude Opus 5 - parameterised
> For a given field plot photographed repeatedly during one season, how did the annotated severity score and the estimated proportion of affected leaf area progress over time, and what was the interval of steepest increase?

**50.** `P152` - Gemini Pro 3.1 - parameterised
> Given a time-series of close-up leaf images from a single plot, rank the progression severity of Bacterial Leaf Blight lesions over time.

**51.** `P048` - Claude Opus 5
> Which images serve as healthy-plant baselines, and how are they distributed across growth stage, capture distance (canopy vs. close-up), and acquisition device?

**52.** `P014` - Claude Fable 5.1 - parameterised
> For a given image, which other images depict the same condition at the same growth stage but a different severity grade?

**53.** `P119` - Gemini Flash 3.8
> What is the calculated percentage of leaf area affected by necrotic lesions (foliar severity index) across annotated regions in an image collection?

**54.** `P049` - Claude Opus 5
> Which images contain two or more distinct symptom types annotated on the same plant, and which symptom combinations co-occur most frequently?

**55.** `P122` - Gemini Flash 3.8
> How do lesion edge contours (water-soaked, wavy margin vs. sharp necrotic border) in leaf macro-photographs differentiate Bacterial Leaf Streak (*Xanthomonas oryzae* pv. *oryzicola*) from Narrow Brown Leaf Spot (*Cercospora janseana*)?

**56.** `P123` - Gemini Flash 3.8
> What developmental growth stage (e.g., vegetative tillering, panicle initiation, physiological maturity) is visually manifest based on visible canopy morphology and floral emergence in the whole-canopy photograph?


## CROSSMODAL (8 CQs)

**57.** `P020` - Claude Fable 5.1
> Which textual symptom descriptors for a condition correspond to which visual symptom classes and plant parts in the annotated image corpus, and for which descriptors is there no supporting image?

**58.** `P087` - GPT-5.6 Sol
> Does the lesion morphology visible in an image correspond to published descriptions of rice blast, bacterial leaf blight, or another candidate disease?

**59.** `P088` - GPT-5.6 Sol
> Which candidate diseases should be included in a differential diagnosis when an image contains symptoms that the literature reports for multiple diseases?

**60.** `P086` - GPT-5.6 Sol - parameterised
> Which diseases or pests described in the literature have symptoms matching those annotated in a given rice image?

**61.** `P153` - Gemini Pro 3.1 - parameterised
> [Img × Txt] Given a leaf image showing spindle-shaped lesions, what are the corresponding chemical treatment protocols documented in extension literature?

**62.** `P053` - Claude Opus 5 - parameterised
> Given an image annotated with elongated water-soaked lesions with wavy yellow margins beginning at the leaf tip, which textually described diseases match that symptom profile, and what are their causal pathogens and recommended control measures?

**63.** `P061` - Claude Opus 5
> Which symptom phenotypes present in the annotated image corpus have no corresponding textual symptom description in the KG, and conversely which literature-described symptoms are entirely unillustrated?

**64.** `P029` - Claude Fable 5.1 - parameterised
> Which conditions reported in surveillance bulletins for a district in a given season are corroborated by image evidence from that district and season, and which are reported but have no image evidence (or vice versa)?
