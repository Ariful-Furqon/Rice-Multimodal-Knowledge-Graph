# Phase 1 summary — Rice MMKG v0.3 → v0.4 (schema restructuring)

Baseline verification (Task 0.1) reproduced every figure in the worklog's
table exactly — no discrepancy, no adopted-baseline correction needed this
round.

## Tasks completed

**1.1 — remove agent-axis classes.** `scripts/task_1_1_remove_agent_axis_classes.py`.
Deleted `FieldObservation`, `FarmerReport`, `DiseaseReport`. **Correction to
the worklog:** `rice:Entity` does not exist; the only "Entity" is
`prov:Entity` (used for `PaddyDoctorDataset`'s legacy typing), which is what
design-doc §2.8 actually refers to. Unlike the worklog's claim it is not
instance-free, so only the class *declaration* was removed here — the
instance typing is retired in Task 1.3 when `PaddyDoctorDataset` is promoted
to `rice:Dataset`. Also removed the v0.3 modality `AllDisjointClasses` axiom
wholesale (it named the three deleted classes). Classes: 18 → 14; individuals
unchanged at 10,463.

**1.2 — rename modality classes.** `scripts/task_1_2_rename_modality_classes.py`.
`LeafImage` → `ImageObservation` (10,407 individuals), `SensorReading` →
`SensorObservation`. Zero old names remain.

**1.3 — add new classes.** `scripts/task_1_3_add_new_classes.py`. Added
`TextualReport`, `ObservationEvent`, `Location`, `Agent`, `Dataset`,
`AnnotationLabel`, `Infestation` (classes: 14 → 21). Created `Farmer`,
`ExtensionOfficer`, `SensorDevice` as `Agent` individuals. Promoted
`PaddyDoctorDataset` to `rice:Dataset`, dropping its `prov:Entity` type.

**1.4 — rewrite property domains/ranges.** `scripts/task_1_4_rewrite_properties.py`.
22 domain/range triples changed on 11 existing properties; added
`transmits`/`transmittedBy`, `denotes`/`denotedBy`, `fromSource`,
`hasPart`/`partOf`, `observedAt` (8 new properties: 24 → 32). Confirmed no
property retains `Pest` in a range meant for a condition, and `detects`
range contains no `Disease`.

**1.5 — someValuesFrom → allValuesFrom.** `scripts/task_1_5_restrictions_all_values.py`.
Also fixed a bug from Task 1.1: deleting the three agent-axis classes had
orphaned their restriction blank nodes instead of removing them (9 dangling
triples across 3 restrictions) — cleaned up here since Task 1.5 touches
restrictions anyway. Converted `SensorObservation`'s one live
`someValuesFrom` restriction; added 5 `allValuesFrom` restrictions per the
design doc. `someValuesFrom`: 4 → 0 (of the live ones); `allValuesFrom`: 0 → 5.

**1.6 — rebuild disjointness.** `scripts/task_1_6_disjointness.py`. New
3-member modality axiom (`ImageObservation`, `SensorObservation`,
`TextualReport`); extended the 12-member domain axiom to 18 (added
`Dataset`, `AnnotationLabel`, `Agent`, `Location`, `ObservationEvent`,
`Infestation` — the worklog's own text says "DatasetLabel" but that class
doesn't exist; `AnnotationLabel` was used instead, presumably what was
meant). Two `AllDisjointClasses` axioms confirmed.

## verify.py deltas

| Quantity | v0.3 baseline | After Phase 1 |
|---|---|---|
| Total triples | 84,064 | 84,177 |
| Named classes | 18 | 21 |
| Object properties | 24 (12 pairs) | 32 (15 pairs) |
| Individuals | 10,463 | 10,466 |
| `someValuesFrom` | 4 | 0 |
| `allValuesFrom` | 0 | 5 |

## Blocked / not checked

- **Reasoner consistency check** (Task 1.5's acceptance: "reasoner reports
  no unsatisfiable classes") — not run. No Java runtime is installed in
  this environment (owlready2 is installed, but its bundled HermiT/Pellet
  need a JRE). Flagged for Checkpoint discussion.
