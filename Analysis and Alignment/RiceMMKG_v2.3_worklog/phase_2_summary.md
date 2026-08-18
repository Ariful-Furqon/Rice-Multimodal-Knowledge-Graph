# Phase 2 summary — restructuring

## Tasks completed

**2.1 — narrow sensor datatype property domains.**
`scripts/task_2_1_narrow_sensor_domains.py`. `humidityValue`,
`temperatureValue`, `rainfallValue`, `soilMoistureValue` moved from
`rdfs:domain rice:Observation` to `rice:SensorReading`. Exactly 4 domain
triples changed; triple count unchanged (84,067 → 84,067).

**2.2 — prototype individuals → class restrictions.**
`scripts/task_2_2_prototypes_to_restrictions.py`. Added
`SensorReading ⊑ ∃captures.EnvironmentalFactor`,
`FieldObservation ⊑ ∃detects.Pest`, `DiseaseReport ⊑ ∃detects.Disease`,
`FarmerReport ⊑ ∃detects.Disease`. Deleted the 5 prototype individuals
(`Leaf_Image`, `Sensor_Reading`, `Field_Observation`, `Farmer_Report`,
`Disease_Report`) and their 33 triples (23 `captures`/`detects` assertions
plus 10 `rdf:type`/`rdfs:label` triples). Individuals: 10,468 → 10,463.
**`LeafImage` deliberately left without a `captures` restriction** — see
`reports/task_2_2_caveat.md` (would falsely assert every image, including
the 1,764 healthy ones, captures a symptom).

**2.3 — symptom annotation sample preparation.**
`scripts/sample_for_annotation.py` (seed 2023) drew 25 `LeafImage`
individuals per Paddy Doctor class × 10 classes → `reports/annotation_sample.csv`,
250 rows, verified balanced. `reports/symptom_vocabulary.md` lists the 11
controlled `Symptom` terms plus an `OTHER` escape value.
`scripts/apply_symptom_annotations.py` was tested clean against a two-row
fixture (`reports/symptom_annotation_fixture.csv`): 2 `captures` triples
applied, 1 skipped (empty symptom list), 0 vocabulary errors.

## verify.py deltas

| Quantity | After Phase 1 | After Phase 2 |
|---|---|---|
| Total triples | 84,067 | 84,050 |
| Individuals | 10,468 | 10,463 |
| `owl:Restriction` axioms | 0 | 4 |
| `subClassOf` blank-node axioms | 0 | 4 |
| Everything else | unchanged | unchanged |

## Blocked

**Task 2.4 (defined classes + reasoning evaluation) cannot proceed.** It
requires `reports/annotation_sample.csv` to be filled in by a human — 250
images need their visible symptoms identified against
`reports/symptom_vocabulary.md`. That is genuine domain-expert annotation
work; it was not fabricated. Once the CSV is completed:

1. run `scripts/apply_symptom_annotations.py` to assert the `captures` triples,
2. resolve the Task 2.2 `LeafImage` caveat (likely via a `SymptomaticLeafImage` subclass, since Task 2.4's defined classes will need to distinguish symptomatic from healthy images anyway),
3. build the 3–5 defined classes and run a reasoner (HermiT/ELK/Pellet),
4. emit `reports/reasoning_evaluation.md` with the confusion matrix.

None of this was started — no defined classes, no reasoner run.

## Out of scope (unchanged)

Everything under "Out of scope for v2.3" in the worklog was left untouched:
`Xanthomonas_Oryzae` pathovar split, missing `causes` links, `Disease`
taxonomic subclasses, PATO symptom decomposition, NCBI Taxon/Plant Ontology
alignment, and populating `SensorReading`/`FieldObservation`/`FarmerReport`/
`DiseaseReport` with individuals.
