# Elicited Competency Questions - SPARQL Results

Generated 2026-09-08 20:49 by `elicited_cq_sparql.py` against `Rice MMKG.rdf` (66,780 triples).

**5 of the 25 elicited Tier A CQs are implemented here.** They are the ones Stage 4 found to be answerable by v0.6 and absent from the SPARQL benchmark, so they close the sharpest gap the reconciliation exposed.

All 5 return answers.

> **These results may not be used to edit the CQ set.** A question the graph answers poorly is a finding about the graph. Rewording CQs to fit what the ontology already does is the circularity this elicitation exists to avoid, and the expert ratings - the only legitimate ground for revising the set - are not in yet.

## Why these are reported separately from the benchmark

The benchmark asks *coverage* and *integrity* questions about the graph and scores them against a 50% population threshold. These ask for *answers* about rice. Scoring a retrieval question against a coverage threshold would be a category error, so the two instruments are kept apart - which is exactly what the Stage 4 reconciliation concluded.

A retrieval CQ answers if it returns at least one row. **A large row count is not a better result than a small one**: CQ-A16 returning exactly two candidate conditions is the correct answer, because the evidence genuinely supports two.

## Summary

| CQ | Level | Dim | Status | Question |
|---|---|---|---|---|
| `CQ-A04` | L3 | D1 | answers | Which diseases share symptoms with Brown Spot, and which symptoms discriminate between them? |
| `CQ-A10` | L1 | D2 | answers | Which images are annotated as showing Hispa damage? |
| `CQ-A13` | L2 | D2 | partial | How is the image corpus distributed across conditions and entity types? |
| `CQ-A16` | L3 | D2 | answers | Which disease or pest is best supported by the visual evidence in a given image? |
| `CQ-A17` | L3 | D2 | partial | Which visual features separate Brown Spot from Rice Blast? |

`partial` means the query answers the part of the question v0.6 can support, with the shortfall named. It is not a pass and is not counted as one.

---

## Results in detail

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

4 row(s) in 82.8 ms.

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

3 row(s) in 7.0 ms.

| symptom | present_only_in |
|---|---|
| rice:Grain_Discoloration | Brown Spot |
| rice:Neck_Rot | Rice Blast |
| rice:Panicle_Blast | Rice Blast |

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

1594 row(s) in 32.6 ms.

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

**Level L2 · Dimension D2 · partial**

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

10 row(s) in 722.4 ms.

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

1 row(s) in 131.4 ms.

| dataset | images |
|---|---|
| rice:PaddyDoctorDataset | 10407 |

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

2 row(s) in 41.8 ms.

| image | candidate | support |
|---|---|---|
| rice:PaddyDoctor_dead_heart_100008 | rice:Deadheart | 1 |
| rice:PaddyDoctor_dead_heart_100008 | rice:Stem_Borer | 1 |

### CQ-A17 - Which visual features separate Brown Spot from Rice Blast?

**Level L3 · Dimension D2 · partial**

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

3 row(s) in 7.4 ms.

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

3 row(s) in 2.1 ms.

| shared_symptom |
|---|
| rice:Brown_Lesion |
| rice:Leaf_Spot |
| rice:Wilting |

---

## Status of all 25 elicited Tier A CQs

So that nothing looks hidden: every CQ, and why it is or is not implemented here.

| CQ | Lv | Dim | State | Requirement | Why |
|---|---|---|---|---|---|
| `CQ-A01` | L1 | D1 | covered by the benchmark | Pathogen causing a disease, and its taxonomy | the benchmark probes the same relation in coverage form |
| `CQ-A02` | L3 | D1 | covered by the benchmark | Vector transmitting a pathogen or viral disease | the benchmark probes the same relation in coverage form |
| `CQ-A03` | L2 | D1 | covered by the benchmark | Symptoms of a disease, by organ and growth stage | the benchmark probes the same relation in coverage form |
| `CQ-A04` | L3 | D1 | implemented here | Diseases sharing symptoms, and what discriminates them | answerable by v0.6, no benchmark counterpart |
| `CQ-A05` | L1 | D1 | covered by the benchmark | Environmental conditions favouring a disease or pest | the benchmark probes the same relation in coverage form |
| `CQ-A06` | L1 | D1 | covered by the benchmark | Growth stage at which a pest or disease is most damaging | the benchmark probes the same relation in coverage form |
| `CQ-A07` | L2 | D1 | covered by the benchmark | Recommended control measures, by category and source | the benchmark probes the same relation in coverage form |
| `CQ-A08` | L1 | D1 | v0.7 work plan | Natural enemies of a pest | needs NaturalEnemy class - not in v0.6 |
| `CQ-A09` | L3 | D1 | v0.7 work plan | Distinguishing a nutritional disorder from a disease | needs nutritional disorder (zinc deficiency) - not in v0.6 |
| `CQ-A10` | L1 | D2 | implemented here | Images showing a given condition or symptom | answerable by v0.6, no benchmark counterpart |
| `CQ-A11` | L1 | D3 | v0.7 work plan | Provenance and confidence of an image annotation | needs annotator + confidence - confidenceScore unused in v0.6 |
| `CQ-A12` | L2 | D3 | v0.7 work plan | Disagreement between model and expert annotations | needs both model and expert annotations - only dataset labels in v0.6 |
| `CQ-A13` | L2 | D2 | implemented here | Distribution of the image corpus | answerable by v0.6, no benchmark counterpart |
| `CQ-A14` | L1 | D2 | v0.7 work plan | Plant organ depicted in an image | needs PlantPart + visual symptom class; needs PlantPart class - not in v0.6; needs region-level organ ... |
| `CQ-A15` | L1 | D2 | covered by the benchmark | Symptoms annotated in a given image | the benchmark probes the same relation in coverage form |
| `CQ-A16` | L3 | D2 | implemented here | Disease or pest supported by visual evidence | answerable by v0.6, no benchmark counterpart |
| `CQ-A17` | L3 | D2 | implemented here | Visual features separating confusable conditions | answerable by v0.6, no benchmark counterpart |
| `CQ-A18` | L1 | D2 | v0.7 work plan | Severity of the damage in an image | needs lesion and leaf segmentation masks plus an area-percentage measurement; needs region-level lesion ... |
| `CQ-A19` | L2 | D2 | v0.7 work plan | Symptoms co-occurring in one image | needs image series grouped by the same plant - v0.6 images are independent; needs multi-symptom ... |
| `CQ-A20` | L1 | D2 | v0.7 work plan | Growth stage visible in a canopy image | needs growth stage annotation on images |
| `CQ-A21` | L2 | D2 | covered by the benchmark | Literature symptoms with and without image support | the benchmark probes the same relation in coverage form |
| `CQ-A22` | L3 | D2 | covered by the benchmark | Literature disease matching an image | the benchmark probes the same relation in coverage form |
| `CQ-A23` | L3 | D2 | covered by the benchmark | Treatment prescribed for an imaged condition | the benchmark probes the same relation in coverage form |
| `CQ-A24` | L1 | D2 | v0.7 work plan | Symptom-free baseline images, by organ and view | needs an explicit symptom-free assertion and a view type per image |
| `CQ-A25` | L3 | D3 | v0.7 work plan | Written and image-derived assessments in disagreement | needs written and image-derived measurements on one declared scale |

| State | CQs |
|---|---|
| covered by the benchmark | 10 |
| v0.7 work plan | 10 |
| implemented here | 5 |

## What this changes for the roadmap

The queries above are small, and that is the point: the cross-modal questions the benchmark never asked turn out to be answerable with the graph as it stands. What they also expose is how thin the visual layer is - `captures` carries 1,442 assertions, all of them to a single symptom, so image-to-symptom grounding exists for one condition and no other. That is a v0.7 priority the coverage benchmark did not surface, because it counted symptoms with any visual grounding rather than images with any symptom.
