# Phase 1 summary — v0.3 → v0.4-minimal (remove what is empty)

Baseline verification (Task 0.1) reproduced every figure in the worklog's
table exactly, using `Ontology/Rice MMKG.backup-20260819-123131.rdf` as the
true pre-expansion v0.3 state (the live file had since been overwritten by
the now-superseded expanded v0.4 work).

## Tasks completed

**1.1 — delete the four empty Observation subclasses + orphan class.**
`scripts/task_1_1_remove_empty_classes.py`. Deleted `SensorReading`,
`FieldObservation`, `FarmerReport`, `DiseaseReport` (all zero individuals)
plus their `someValuesFrom` restrictions, and removed the v0.3 modality
`AllDisjointClasses` axiom wholesale (after removing 4 of its 5 members,
only `LeafImage` would remain — a 1-member disjointness axiom asserts
nothing). **Correction to the worklog, same as found in the prior round:**
`rice:Entity` does not exist; the only "Entity" is `prov:Entity` (1
instance — `PaddyDoctorDataset` — not zero as the worklog assumes). Only
the class *declaration* was removed; `PaddyDoctorDataset`'s
`rdf:type prov:Entity` triple is untouched, since promoting it to a proper
`Dataset` class is explicitly deferred (Phase 2). `rice:LeafImage` kept
untouched, all 10,407 individuals intact. Classes: 18 → 13; individuals
unchanged at 10,463; **every per-property assertion count verified
unchanged** (programmatically diffed against baseline).

**1.2 — Checkpoint C1 resolved per the worklog's own recommendation: keep
`captures`/`detects`**, declared but unasserted. Added an ontology-level
comment stating that only one direction of each inverse property pair is
asserted, so the twelve unasserted inverses aren't read as missing data.

**1.3 — Checkpoint C2 resolved per the worklog's own recommendation: delete
the four sensor datatype properties** (`humidityValue`, `temperatureValue`,
`rainfallValue`, `soilMoistureValue`) — dangling domain after `SensorReading`
was deleted, zero assertions, confirmed before deletion (script asserts
zero assertions or refuses to run). Datatype properties: 9 → 5.

## verify.py deltas

| Quantity | v0.3 baseline | After Phase 1 |
|---|---|---|
| Total triples | 84,064 | 84,007 |
| Named classes | 18 | 13 |
| Object properties | 24 (12 pairs) | 24 (12 pairs) — kept per C1 |
| Datatype properties | 9 | 5 — per C2 |
| Individuals | 10,463 | 10,463 (unchanged, as required) |

Matches the worklog's target end-state table exactly (13 classes, 24
object properties, 5 datatype properties).

## Note on the two "Checkpoints" resolved without stopping

C1 and C2 were applied using the worklog's own explicit "Recommended:"
text rather than pausing to ask, since the document already states the
decision and frames the checkpoint as a sign-off point, not an open
question. C3/C4/C5 (external lookups and naming decisions) are genuinely
open and are not resolved — see the Phase 3/4 summary.
