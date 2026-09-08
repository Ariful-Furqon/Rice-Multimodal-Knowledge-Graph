# Elicited Competency Questions - SPARQL Results

Generated 2026-09-08 21:44 by `elicited_cq_sparql.py` against `Rice MMKG.rdf`: 66,780 asserted triples, 161,416 after OWL RL materialisation (32.2s).

**15 of the 25 elicited Tier A CQs are implemented here** - every one that RiceMMKG v0.6 can answer. The remaining 10 need schema or data the release does not carry and are the v0.7 work plan; the status table at the end lists each with its reason.

**7 answer in full and 8 answer in part.** A partial is not a pass: the query returns what v0.6 supports, and the shortfall is named on the CQ. 8 of 15 coming back partial is itself the finding - competency questions are requirements, and requirements are supposed to outrun the release that exists.

**A partial comes in two kinds, and they are different pieces of work.** 7 are *partial - schema*: the ontology has no concept for what the question asks, so no amount of data would answer it and the remedy is modelling. 1 is *partial - data*: the concept exists and the query is correct, but few individuals carry it, so the remedy is annotation. Only the second kind is a coverage question at all - a relation that does not exist has no ratio to report, and calling that 0% would misdescribe it.

> **These results may not be used to edit the CQ set.** A question the graph answers poorly is a finding about the graph. Rewording CQs to fit what the ontology already does is the circularity this elicitation exists to avoid, and the expert ratings - the only legitimate ground for revising the set - are not in yet.

## Why these are reported separately from the benchmark

The benchmark asks *coverage* and *integrity* questions about the graph and scores them against a 50% population threshold. These ask for *answers* about rice. Scoring a retrieval question against a coverage threshold would be a category error, so the two instruments are kept apart - which is exactly what the Stage 4 reconciliation concluded.

A retrieval CQ answers if it returns at least one row. **A large row count is not a better result than a small one**: CQ-A16 returning exactly two candidate conditions is the correct answer, because the evidence genuinely supports two.

## Summary

| CQ | Level | Dim | Status | Question |
|---|---|---|---|---|
| `CQ-A01` | L1 | D1 | partial - schema | Which pathogen causes Rice Blast, and to which taxonomic group does it belong? |
| `CQ-A02` | L3 | D1 | partial - schema | Which vector species transmits Rice Tungro Bacilliform Virus, and by which transmission mode? |
| `CQ-A03` | L2 | D1 | partial - schema | Which symptoms does Bacterial Leaf Blight produce, on which plant organ, and at which growth stage? |
| `CQ-A04` | L3 | D1 | answers | Which diseases share symptoms with Brown Spot, and which symptoms discriminate between them? |
| `CQ-A05` | L1 | D1 | answers | Which environmental conditions are reported to favour Sheath Blight? |
| `CQ-A06` | L1 | D1 | partial - schema | At which growth stages is Brown Planthopper reported as most damaging? |
| `CQ-A07` | L2 | D1 | partial - schema | Which control measures are recommended for Stem Borer, of which management category, and on which source authority? |
| `CQ-A10` | L1 | D2 | answers | Which images are annotated as showing Hispa damage? |
| `CQ-A13` | L2 | D2 | partial - schema | How is the image corpus distributed across conditions and entity types? |
| `CQ-A15` | L1 | D2 | partial - data | Which visible symptoms are annotated in a given image? |
| `CQ-A16` | L3 | D2 | answers | Which disease or pest is best supported by the visual evidence in a given image? |
| `CQ-A17` | L3 | D2 | partial - schema | Which visual features separate Brown Spot from Rice Blast? |
| `CQ-A21` | L2 | D2 | answers | Which symptoms described in the literature have supporting image evidence, and which do not? |
| `CQ-A22` | L3 | D2 | answers | Which disease described in the literature matches the condition annotated in a given image? |
| `CQ-A23` | L3 | D2 | answers | Which treatment does the literature prescribe for a condition identified from an image? |

`partial` means the query answers the part of the question v0.6 can support, with the shortfall named. It is not a pass and is not counted as one.

---

## Results in detail

### CQ-A01 - Which pathogen causes Rice Blast, and to which taxonomic group does it belong?

**Level L1 · Dimension D1 · partial - schema**

The single most converged requirement: five of six models proposed it, and all five made it their own question number one. The benchmark asks the coverage form of the same relation - how many diseases have any pathogen - never the answer form.

> **Partial:** v0.6 types every pathogen as rice:Pathogen and nothing more, so there is no taxonomic group to return; the closest available identity is the external alignment

**Causal pathogen of Rice Blast, with its external identity**

```sparql
SELECT ?pathogen ?eppo_code ?external_alignment WHERE {
  rice:Rice_Blast_Disease rice:causedBy ?pathogen .
  OPTIONAL { ?pathogen rice:eppoCode ?eppo_code }
  OPTIONAL { ?pathogen skos:exactMatch ?external_alignment }
}
```

1 row(s) in 108.0 ms.

| pathogen | eppo_code | external_alignment |
|---|---|---|
| rice:Magnaporthe_Oryzae | PYRIOR | http://aims.fao.org/aos/agrovoc/c_16025 |

**Every disease with its causal pathogen - the answer form of benchmark CQ-01**

```sparql
SELECT ?disease ?pathogen WHERE {
  ?disease rice:causedBy ?pathogen .
}
ORDER BY ?disease
```

8 row(s) in 4.1 ms.

| disease | pathogen |
|---|---|
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae |
| rice:Bacterial_Leaf_Streak | rice:Xanthomonas_Oryzicola |
| rice:Bacterial_Panicle_Blight | rice:Burkholderia_Glumae |
| rice:Brown_Spot | rice:Bipolaris_Oryzae |
| rice:Downy_Mildew | rice:Sclerophthora_Macrospora |
| rice:Rice_Blast_Disease | rice:Magnaporthe_Oryzae |
| rice:Rice_Tungro_Disease | rice:Rice_Tungro_Bacilliform_Virus |
| rice:Rice_Tungro_Disease | rice:Rice_Tungro_Spherical_Virus |

### CQ-A02 - Which vector species transmits Rice Tungro Bacilliform Virus, and by which transmission mode?

**Level L3 · Dimension D1 · partial - schema**

A three-hop chain: vector -> agent -> disease. Proposed by five of six models.

> **Partial:** transmission mode is not a property in v0.6, so the mode cannot be returned

**Vector, the agent it transmits, and the disease that agent causes**

```sparql
SELECT ?vector ?agent ?disease WHERE {
  ?vector rice:transmits ?agent .
  OPTIONAL { ?disease rice:causedBy ?agent }
}
ORDER BY ?vector ?agent
```

2 row(s) in 6.9 ms.

| vector | agent | disease |
|---|---|---|
| rice:Nephotettix_Virescens | rice:Rice_Tungro_Bacilliform_Virus | rice:Rice_Tungro_Disease |
| rice:Nephotettix_Virescens | rice:Rice_Tungro_Spherical_Virus | rice:Rice_Tungro_Disease |

### CQ-A03 - Which symptoms does Bacterial Leaf Blight produce, on which plant organ, and at which growth stage?

**Level L2 · Dimension D1 · partial - schema**

The diagnostic question in its plainest form.

> **Partial:** plant organ is not modelled in v0.6; growth stage is attached to the disease, not to the individual symptom, so the two are returned as a cross product rather than a fact

**Symptoms of Bacterial Leaf Blight, with the stages at which the disease occurs**

```sparql
SELECT ?symptom ?stage_of_disease WHERE {
  rice:Bacterial_Leaf_Blight rice:indicatedBy ?symptom .
  OPTIONAL { rice:Bacterial_Leaf_Blight rice:occursIn ?stage_of_disease }
}
ORDER BY ?symptom ?stage_of_disease
```

12 row(s) in 5.8 ms.

| symptom | stage_of_disease |
|---|---|
| rice:Dry_Leaf_Tip | rice:Reproductive_Stage |
| rice:Dry_Leaf_Tip | rice:Tillering_Stage |
| rice:Dry_Leaf_Tip | rice:Vegetative_Stage |
| rice:Leaf_Rolling | rice:Reproductive_Stage |
| rice:Leaf_Rolling | rice:Tillering_Stage |
| rice:Leaf_Rolling | rice:Vegetative_Stage |
| rice:Wilting | rice:Reproductive_Stage |
| rice:Wilting | rice:Tillering_Stage |
| *… 4 more rows* | |

### CQ-A04 - Which diseases share symptoms with Brown Spot, and which symptoms discriminate between them?

**Level L3 · Dimension D1 · answers**

Differential diagnosis. Proposed independently by five of the six models and absent from the benchmark, which asks only whether symptoms are attached, never which conditions they fail to separate.

**Conditions sharing at least one symptom with Brown Spot**

```sparql
SELECT ?other (COUNT(DISTINCT ?shared) AS ?shared_symptoms)
WHERE {
  rice:Brown_Spot rice:indicatedBy ?shared .
  ?other rice:indicatedBy ?shared .
  FILTER (?other != rice:Brown_Spot)
}
GROUP BY ?other
ORDER BY DESC(?shared_symptoms)
```

4 row(s) in 9.9 ms.

| other | shared_symptoms |
|---|---|
| rice:Rice_Blast_Disease | 3 |
| rice:Bacterial_Panicle_Blight | 2 |
| rice:Sheath_Blight | 1 |
| rice:Bacterial_Leaf_Blight | 1 |

**Symptoms that discriminate Brown Spot from Rice Blast**

```sparql
SELECT ?symptom ?present_only_in WHERE {
  {
    rice:Brown_Spot rice:indicatedBy ?symptom .
    FILTER NOT EXISTS { rice:Rice_Blast_Disease rice:indicatedBy ?symptom }
    BIND ("Brown Spot" AS ?present_only_in)
  } UNION {
    rice:Rice_Blast_Disease rice:indicatedBy ?symptom .
    FILTER NOT EXISTS { rice:Brown_Spot rice:indicatedBy ?symptom }
    BIND ("Rice Blast" AS ?present_only_in)
  }
}
ORDER BY ?present_only_in ?symptom
```

3 row(s) in 9.6 ms.

| symptom | present_only_in |
|---|---|
| rice:Grain_Discoloration | Brown Spot |
| rice:Neck_Rot | Rice Blast |
| rice:Panicle_Blast | Rice Blast |

### CQ-A05 - Which environmental conditions are reported to favour Sheath Blight?

**Level L1 · Dimension D1 · answers**

Proposed by a single model, and kept for exactly that reason: the questionnaire needs low-convergence CQs or the hypothesis that convergence predicts expert-rated relevance cannot be tested. It turns out to be answerable and well populated.

**Conditions that increase the risk of Sheath Blight**

```sparql
SELECT ?condition WHERE {
  ?condition rice:increaseRiskOf rice:Sheath_Blight .
}
ORDER BY ?condition
```

2 row(s) in 2.7 ms.

| condition |
|---|
| rice:High_Humidity |
| rice:Poor_Soil_Drainage |

**Every condition-to-entity risk link in the graph**

```sparql
SELECT ?condition (COUNT(DISTINCT ?entity) AS ?entities) WHERE {
  ?condition rice:increaseRiskOf ?entity .
}
GROUP BY ?condition
ORDER BY DESC(?entities) ?condition
```

9 row(s) in 6.6 ms.

| condition | entities |
|---|---|
| rice:High_Humidity | 9 |
| rice:High_Temperature | 7 |
| rice:Low_Rainfall | 3 |
| rice:Poor_Soil_Drainage | 3 |
| rice:Dense_Canopy | 2 |
| rice:Excessive_Nitrogen | 2 |
| rice:High_Night_Temperature | 1 |
| rice:Presence_of_Leafhopper_Vector | 1 |
| *… 1 more rows* | |

### CQ-A06 - At which growth stages is Brown Planthopper reported as most damaging?

**Level L1 · Dimension D1 · partial - schema**

Also single-model, also answerable.

> **Partial:** v0.6 records that a pest occurs at a stage, not how damaging it is there, so the question's ranking cannot be answered - occurrence is returned instead

**Growth stages at which Brown Planthopper occurs**

```sparql
SELECT ?stage WHERE {
  rice:Brown_Planthopper rice:occursIn ?stage .
}
ORDER BY ?stage
```

2 row(s) in 2.5 ms.

| stage |
|---|
| rice:Flowering_Stage |
| rice:Vegetative_Stage |

### CQ-A07 - Which control measures are recommended for Stem Borer, of which management category, and on which source authority?

**Level L2 · Dimension D1 · partial - schema**

Actionability - the KG must not diagnose what it cannot advise on. Proposed by five of six models.

> **Partial:** management category (chemical / biological / cultural) and source authority are not modelled in v0.6; only the treatment itself and its prerequisites can be returned

**Treatments for Stem Borer and what each requires**

```sparql
SELECT ?treatment ?requires WHERE {
  rice:Stem_Borer rice:controlledBy ?treatment .
  OPTIONAL { ?treatment rice:requires ?requires }
}
ORDER BY ?treatment
```

2 row(s) in 3.8 ms.

| treatment | requires |
|---|---|
| rice:Biological_Control | None |
| rice:Insecticide_Application | None |

### CQ-A10 - Which images are annotated as showing Hispa damage?

**Level L1 · Dimension D2 · answers**

The most basic cross-modal retrieval there is. The benchmark checks that annotations are typed, never that they can be retrieved by condition.

**Images annotated as Hispa, with their retrievable URL**

```sparql
SELECT ?image ?url WHERE {
  ?image rice:annotatedAs rice:Hispa ;
         schema:contentUrl ?url .
}
ORDER BY ?image
```

1594 row(s) in 41.3 ms.

| image | url |
|---|---|
| rice:PaddyDoctor_hispa_100003 | Data/PaddyDoctor/hispa/100003.jpg |
| rice:PaddyDoctor_hispa_100005 | Data/PaddyDoctor/hispa/100005.jpg |
| rice:PaddyDoctor_hispa_100010 | Data/PaddyDoctor/hispa/100010.jpg |
| rice:PaddyDoctor_hispa_100051 | Data/PaddyDoctor/hispa/100051.jpg |
| rice:PaddyDoctor_hispa_100052 | Data/PaddyDoctor/hispa/100052.jpg |
| rice:PaddyDoctor_hispa_100061 | Data/PaddyDoctor/hispa/100061.jpg |
| rice:PaddyDoctor_hispa_100072 | Data/PaddyDoctor/hispa/100072.jpg |
| rice:PaddyDoctor_hispa_100077 | Data/PaddyDoctor/hispa/100077.jpg |
| *… 1,586 more rows* | |

### CQ-A13 - How is the image corpus distributed across conditions and entity types?

**Level L2 · Dimension D2 · partial - schema**

PARTIAL. The elicited question also asks for plant part and capture type. v0.6 models neither, so this implements the answerable half and the rest stays on the v0.7 plan. Reported as partial rather than passed.

> **Partial:** plant part and capture type are not modelled in v0.6

**Images per annotated condition and entity type**

```sparql
SELECT ?condition ?type (COUNT(?image) AS ?images) WHERE {
  ?image a rice:ImageObservation ;
         rice:annotatedAs ?condition .
  ?condition a ?type .
  FILTER (STRSTARTS(STR(?type), STR(rice:)))
}
GROUP BY ?condition ?type
ORDER BY DESC(?images)
```

10 row(s) in 6113.9 ms.

| condition | type | images |
|---|---|---|
| rice:Normal_Health | rice:HealthStatus | 1764 |
| rice:Rice_Blast_Disease | rice:Disease | 1738 |
| rice:Hispa | rice:Pest | 1594 |
| rice:Deadheart | rice:Disease | 1442 |
| rice:Rice_Tungro_Disease | rice:Disease | 1088 |
| rice:Brown_Spot | rice:Disease | 965 |
| rice:Downy_Mildew | rice:Disease | 620 |
| rice:Bacterial_Leaf_Blight | rice:Disease | 479 |
| *… 2 more rows* | | |

**Images per source dataset**

```sparql
SELECT ?dataset (COUNT(?image) AS ?images) WHERE {
  ?image a rice:ImageObservation ;
         prov:wasDerivedFrom ?dataset .
}
GROUP BY ?dataset
```

1 row(s) in 171.5 ms.

| dataset | images |
|---|---|
| rice:PaddyDoctorDataset | 10407 |

### CQ-A15 - Which visible symptoms are annotated in a given image?

**Level L1 · Dimension D2 · partial - data**

Reads the visual layer from the image side rather than the symptom side - which is what exposes how thin it is.

> **Partial:** only 1,442 of 10,407 images (14%) carry a captures link, and every one of them points at the same symptom

**Symptoms annotated in one image that has them**

```sparql
SELECT ?image ?symptom WHERE {
  { SELECT ?image WHERE { ?image rice:captures ?s } ORDER BY ?image LIMIT 1 }
  ?image rice:captures ?symptom .
}
```

1 row(s) in 34.2 ms.

| image | symptom |
|---|---|
| rice:PaddyDoctor_dead_heart_100008 | rice:Dead_Tiller |

**How many distinct symptoms the whole image corpus captures**

```sparql
SELECT ?symptom (COUNT(DISTINCT ?image) AS ?images) WHERE {
  ?image rice:captures ?symptom .
}
GROUP BY ?symptom
ORDER BY DESC(?images)
```

1 row(s) in 19.8 ms.

| symptom | images |
|---|---|
| rice:Dead_Tiller | 1442 |

### CQ-A16 - Which disease or pest is best supported by the visual evidence in a given image?

**Level L3 · Dimension D2 · answers**

The full cross-modal chain: image -> symptom it captures -> conditions that symptom indicates. The image is chosen by the query itself rather than hardcoded, so the test survives any re-import of the corpus.

**Candidate conditions for one annotated image, ranked by supporting symptoms**

```sparql
SELECT ?image ?candidate (COUNT(DISTINCT ?symptom) AS ?support)
WHERE {
  { SELECT ?image WHERE { ?image rice:captures ?s } ORDER BY ?image LIMIT 1 }
  ?image rice:captures ?symptom .
  ?candidate rice:indicatedBy ?symptom .
}
GROUP BY ?image ?candidate
ORDER BY DESC(?support) ?candidate
```

2 row(s) in 58.8 ms.

| image | candidate | support |
|---|---|---|
| rice:PaddyDoctor_dead_heart_100008 | rice:Deadheart | 1 |
| rice:PaddyDoctor_dead_heart_100008 | rice:Stem_Borer | 1 |

### CQ-A17 - Which visual features separate Brown Spot from Rice Blast?

**Level L3 · Dimension D2 · partial - schema**

The pair the models named most often as visually confusable. Answered from the symptom layer; v0.6 has no lesion shape/colour descriptors, so the separation is by symptom identity rather than by visual feature.

> **Partial:** separation is by symptom, not by lesion descriptors, which v0.6 does not carry

**Symptoms unique to each of the two conditions**

```sparql
SELECT ?condition ?distinguishing_symptom WHERE {
  {
    rice:Brown_Spot rice:indicatedBy ?distinguishing_symptom .
    FILTER NOT EXISTS {
      rice:Rice_Blast_Disease rice:indicatedBy ?distinguishing_symptom }
    BIND ("Brown Spot" AS ?condition)
  } UNION {
    rice:Rice_Blast_Disease rice:indicatedBy ?distinguishing_symptom .
    FILTER NOT EXISTS {
      rice:Brown_Spot rice:indicatedBy ?distinguishing_symptom }
    BIND ("Rice Blast" AS ?condition)
  }
}
ORDER BY ?condition ?distinguishing_symptom
```

3 row(s) in 13.0 ms.

| condition | distinguishing_symptom |
|---|---|
| Brown Spot | rice:Grain_Discoloration |
| Rice Blast | rice:Neck_Rot |
| Rice Blast | rice:Panicle_Blast |

**Symptoms the two share, which therefore cannot separate them**

```sparql
SELECT ?shared_symptom WHERE {
  rice:Brown_Spot rice:indicatedBy ?shared_symptom .
  rice:Rice_Blast_Disease rice:indicatedBy ?shared_symptom .
}
ORDER BY ?shared_symptom
```

3 row(s) in 3.3 ms.

| shared_symptom |
|---|
| rice:Brown_Lesion |
| rice:Leaf_Spot |
| rice:Wilting |

### CQ-A21 - Which symptoms described in the literature have supporting image evidence, and which do not?

**Level L2 · Dimension D2 · answers**

The multimodal grounding question asked as a partition rather than a ratio. Benchmark CQ-18 measures the same relation as a coverage percentage; this returns the two lists, which is a far blunter way of seeing the same thing.

**Symptoms partitioned by whether any image captures them**

```sparql
SELECT ?image_evidence (COUNT(DISTINCT ?symptom) AS ?symptoms)
WHERE {
  ?symptom a rice:Symptom .
  OPTIONAL { ?image rice:captures ?symptom }
  BIND (IF(BOUND(?image), "has image evidence", "no image evidence")
        AS ?image_evidence)
}
GROUP BY ?image_evidence
```

2 row(s) in 74.0 ms.

| image_evidence | symptoms |
|---|---|
| no image evidence | 26 |
| has image evidence | 1 |

**The symptoms with no image evidence at all**

```sparql
SELECT ?symptom WHERE {
  ?symptom a rice:Symptom .
  FILTER NOT EXISTS { ?image rice:captures ?symptom }
}
ORDER BY ?symptom
```

26 row(s) in 18.6 ms.

| symptom |
|---|
| rice:Brown_Leaf_Tip |
| rice:Brown_Lesion |
| rice:Chewed_Leaf |
| rice:Discolored_Panicle |
| rice:Dry_Leaf_Tip |
| rice:Empty_Grain |
| rice:Excessive_Tillering |
| rice:Grain_Discoloration |
| *… 18 more rows* |

### CQ-A22 - Which disease described in the literature matches the condition annotated in a given image?

**Level L3 · Dimension D2 · answers**

Joins through the annotated class rather than through captures, so it reaches all 10,407 images instead of the 1,442 that CQ-A16 can reach. Same cross-modal claim, different and much better populated join.

**Literature evidence for the condition annotated in one image**

```sparql
SELECT ?image ?condition ?symptom ?pathogen WHERE {
  { SELECT ?image WHERE { ?image rice:annotatedAs rice:Brown_Spot }
    ORDER BY ?image LIMIT 1 }
  ?image rice:annotatedAs ?condition .
  OPTIONAL { ?condition rice:indicatedBy ?symptom }
  OPTIONAL { ?condition rice:causedBy ?pathogen }
}
ORDER BY ?symptom
```

4 row(s) in 127.7 ms.

| image | condition | symptom | pathogen |
|---|---|---|---|
| rice:PaddyDoctor_brown_spot_100001 | rice:Brown_Spot | rice:Brown_Lesion | rice:Bipolaris_Oryzae |
| rice:PaddyDoctor_brown_spot_100001 | rice:Brown_Spot | rice:Grain_Discoloration | rice:Bipolaris_Oryzae |
| rice:PaddyDoctor_brown_spot_100001 | rice:Brown_Spot | rice:Leaf_Spot | rice:Bipolaris_Oryzae |
| rice:PaddyDoctor_brown_spot_100001 | rice:Brown_Spot | rice:Wilting | rice:Bipolaris_Oryzae |

**How many images reach a literature-described condition**

```sparql
SELECT (COUNT(DISTINCT ?image) AS ?images_with_literature)
WHERE {
  ?image rice:annotatedAs ?condition .
  ?condition rice:indicatedBy ?symptom .
}
```

1 row(s) in 251.8 ms.

| images_with_literature |
|---|
| 8643 |

### CQ-A23 - Which treatment does the literature prescribe for a condition identified from an image?

**Level L3 · Dimension D2 · answers**

The full multimodal claim of the resource, end to end: an image leads to an agronomic recommendation. Proposed by a single model.

**Image -> annotated condition -> recommended treatment**

```sparql
SELECT ?image ?condition ?treatment WHERE {
  { SELECT ?image WHERE {
      ?image rice:annotatedAs ?c . ?c rice:controlledBy ?t }
    ORDER BY ?image LIMIT 1 }
  ?image rice:annotatedAs ?condition .
  ?condition rice:controlledBy ?treatment .
}
ORDER BY ?treatment
```

4 row(s) in 896.0 ms.

| image | condition | treatment |
|---|---|---|
| rice:PaddyDoctor_bacterial_leaf_blight_100023 | rice:Bacterial_Leaf_Blight | rice:Crop_Rotation |
| rice:PaddyDoctor_bacterial_leaf_blight_100023 | rice:Bacterial_Leaf_Blight | rice:Crop_Sanitation |
| rice:PaddyDoctor_bacterial_leaf_blight_100023 | rice:Bacterial_Leaf_Blight | rice:Resistant_Variety |
| rice:PaddyDoctor_bacterial_leaf_blight_100023 | rice:Bacterial_Leaf_Blight | rice:Water_Management |

**How many images reach at least one treatment**

```sparql
SELECT (COUNT(DISTINCT ?image) AS ?images_with_treatment) WHERE {
  ?image rice:annotatedAs ?condition .
  ?condition rice:controlledBy ?treatment .
}
```

1 row(s) in 251.4 ms.

| images_with_treatment |
|---|
| 8643 |

---

## Status of all 25 elicited Tier A CQs

So that nothing looks hidden: every CQ, and why it is or is not implemented here.

| CQ | Lv | Dim | State | Requirement | Why |
|---|---|---|---|---|---|
| `CQ-A01` | L1 | D1 | implemented here | Pathogen causing a disease, and its taxonomy | answerable by v0.6; the benchmark probes the same relation in coverage form, this is the answer form |
| `CQ-A02` | L3 | D1 | implemented here | Vector transmitting a pathogen or viral disease | answerable by v0.6; the benchmark probes the same relation in coverage form, this is the answer form |
| `CQ-A03` | L2 | D1 | implemented here | Symptoms of a disease, by organ and growth stage | answerable by v0.6; the benchmark probes the same relation in coverage form, this is the answer form |
| `CQ-A04` | L3 | D1 | implemented here | Diseases sharing symptoms, and what discriminates them | answerable by v0.6; no benchmark counterpart |
| `CQ-A05` | L1 | D1 | implemented here | Environmental conditions favouring a disease or pest | answerable by v0.6; the benchmark probes the same relation in coverage form, this is the answer form |
| `CQ-A06` | L1 | D1 | implemented here | Growth stage at which a pest or disease is most damaging | answerable by v0.6; the benchmark probes the same relation in coverage form, this is the answer form |
| `CQ-A07` | L2 | D1 | implemented here | Recommended control measures, by category and source | answerable by v0.6; the benchmark probes the same relation in coverage form, this is the answer form |
| `CQ-A08` | L1 | D1 | v0.7 work plan | Natural enemies of a pest | needs NaturalEnemy class - not in v0.6 |
| `CQ-A09` | L3 | D1 | v0.7 work plan | Distinguishing a nutritional disorder from a disease | needs nutritional disorder (zinc deficiency) - not in v0.6 |
| `CQ-A10` | L1 | D2 | implemented here | Images showing a given condition or symptom | answerable by v0.6; no benchmark counterpart |
| `CQ-A11` | L1 | D3 | v0.7 work plan | Provenance and confidence of an image annotation | needs annotator + confidence - confidenceScore unused in v0.6 |
| `CQ-A12` | L2 | D3 | v0.7 work plan | Disagreement between model and expert annotations | needs both model and expert annotations - only dataset labels in v0.6 |
| `CQ-A13` | L2 | D2 | implemented here | Distribution of the image corpus | answerable by v0.6; no benchmark counterpart |
| `CQ-A14` | L1 | D2 | v0.7 work plan | Plant organ depicted in an image | needs PlantPart + visual symptom class; needs PlantPart class - not in v0.6; needs region-level organ ... |
| `CQ-A15` | L1 | D2 | implemented here | Symptoms annotated in a given image | answerable by v0.6; the benchmark probes the same relation in coverage form, this is the answer form |
| `CQ-A16` | L3 | D2 | implemented here | Disease or pest supported by visual evidence | answerable by v0.6; no benchmark counterpart |
| `CQ-A17` | L3 | D2 | implemented here | Visual features separating confusable conditions | answerable by v0.6; no benchmark counterpart |
| `CQ-A18` | L1 | D2 | v0.7 work plan | Severity of the damage in an image | needs lesion and leaf segmentation masks plus an area-percentage measurement; needs region-level lesion ... |
| `CQ-A19` | L2 | D2 | v0.7 work plan | Symptoms co-occurring in one image | needs image series grouped by the same plant - v0.6 images are independent; needs multi-symptom ... |
| `CQ-A20` | L1 | D2 | v0.7 work plan | Growth stage visible in a canopy image | needs growth stage annotation on images |
| `CQ-A21` | L2 | D2 | implemented here | Literature symptoms with and without image support | answerable by v0.6; the benchmark probes the same relation in coverage form, this is the answer form |
| `CQ-A22` | L3 | D2 | implemented here | Literature disease matching an image | answerable by v0.6; the benchmark probes the same relation in coverage form, this is the answer form |
| `CQ-A23` | L3 | D2 | implemented here | Treatment prescribed for an imaged condition | answerable by v0.6; the benchmark probes the same relation in coverage form, this is the answer form |
| `CQ-A24` | L1 | D2 | v0.7 work plan | Symptom-free baseline images, by organ and view | needs an explicit symptom-free assertion and a view type per image |
| `CQ-A25` | L3 | D3 | v0.7 work plan | Written and image-derived assessments in disagreement | needs written and image-derived measurements on one declared scale |

| State | CQs |
|---|---|
| implemented here | 15 |
| v0.7 work plan | 10 |

## What this changes for the roadmap

The queries above are small, and that is the point: the cross-modal questions the benchmark never asked turn out to be answerable with the graph as it stands. What they also expose is how thin the visual layer is - `captures` carries 1,442 assertions, all of them to a single symptom, so image-to-symptom grounding exists for one condition and no other. That is a v0.7 priority the coverage benchmark did not surface, because it counted symptoms with any visual grounding rather than images with any symptom.
