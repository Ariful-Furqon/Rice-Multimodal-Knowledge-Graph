# Phase 0 — baseline reconciliation

The worklog's baseline table (measured against an earlier state of `Rice_MMKG.rdf`)
does not match the ontology's current state. Three alignment-focused commits landed
after that baseline was captured:

- `06f3c49` update alignment
- `ab3c1c5` Add NCBI Taxonomy cross-check, multimodal fusion PoC, and an ontology backup
- `25e9a7b` Resolve four EnvironmentalFactor category mismatches via Planteome

Per user decision (2026-08-18), the measured numbers below are adopted as the
corrected v2.2 baseline for all subsequent phase acceptance checks. The worklog
document itself is not edited; this file is the authoritative correction.

| Quantity | Worklog value | Corrected baseline |
|---|---|---|
| Total triples | 52,806 | **52,816** |
| `skos:exactMatch` | 14 | **19** |
| `skos:closeMatch` | 5 | **8** |
| Domain individuals with no alignment | 10 | **30** |

All other baseline figures were reproduced exactly and are unchanged: 17 named
classes, 24 object properties (12 `owl:inverseOf` pairs), 9 datatype properties
(all functional), 0 `owl:Restriction` axioms, 10,467 individuals, 10,407
`rice:LeafImage` individuals, 55 domain individuals, 5 prototype individuals with
no class assertion.

## Corrected Task 1.4 target list

Task 1.4 originally named 10 unaligned individuals. The corrected list of 30
domain individuals with no `skos:exactMatch`/`closeMatch` is:

Armyworm, Bacterial_Leaf_Blight, Bacterial_Leaf_Streak, Bacterial_Panicle_Blight,
Brown_Lesion, Brown_Spot, Chewed_Leaf, Critical_Severity, Deadheart,
Dry_Leaf_Tip, Empty_Grain, Excessive_Nitrogen, Field_Inspection, Harvest_Stage,
High_Severity, Hispa, Hopper_Burn, Immediate_Intervention, Leaf_Rolling,
Low_Severity, Maturity_Stage, Medium_Severity, No_Action_Needed, Normal_Health,
Preventive_Action, Resistant_Variety, Rice_Bug, Sheath_Blight, Stem_Rot_Symptom,
Yellow_Leaf

`reports/agrovoc_todo.csv` (Task 1.4) will be emitted against this corrected
30-row list instead of the worklog's 10-row list.
