# Phase 2 summary — Rice MMKG v0.3 → v0.4 (data migration)

## Tasks completed, in execution order

**2.2 — populate Infestation (run before 2.1, since 2.1 needs it).**
`scripts/task_2_2_populate_infestation.py`. Created 6 `Infestation`
individuals named from the damage, not the organism (`Hispa_Leaf_Damage`,
`Armyworm_Defoliation`, `Brown_Planthopper_Infestation`,
`Leaf_Folder_Damage`, `Rice_Bug_Grain_Damage`, `Stem_Borer_Damage`), and 6
`causes` assertions from the corresponding `Pest`. `transmits` left at zero
assertions; `reports/vector_todo.csv` emitted (6 rows, empty) plus
`reports/task_2_2_vector_notes.md` flagging that the tungro case needs a new
leafhopper `Pest` and virus `Pathogen` individual before it can even be
filled in — neither exists yet and neither was created here.

**2.2b — retarget Pest→Infestation in narrowed properties (not in the
worklog; required for internal consistency, done after explicit user
confirmation).** `scripts/task_2_2b_retarget_pest_to_infestation.py`.
Task 1.4 narrowed `indicatedBy`/`increaseRiskOf`/`vulnerableTo`/`occursIn`/
`controlledBy`/`recommends` (and their inverses) to `Disease ⊔ Infestation`,
dropping `Pest` — but 45 existing individual-level assertions still pointed
a `Pest` individual into those now-invalid positions (e.g.
`Stem_Borer indicatedBy Deadheart`, `High_Temperature increaseRiskOf
Stem_Borer`), which the worklog never states a migration step for. Since
`Pest`/`Infestation` are also disjoint after Task 1.6, this would have left
the ontology inconsistent. All 45 were retargeted 1:1 to the matching
`Infestation` individual (e.g. → `Stem_Borer_Damage indicatedBy Deadheart`),
consistent with the Infestation split's own logic. Full before/after list
in the script's stdout log. `causes` (Pest→Infestation) and the evidence-path
properties (`detects`/`transmits`, which correctly target the organism)
were untouched.

**2.1 — annotation label layer.** `scripts/task_2_1_annotation_labels.py`.
10 `AnnotationLabel` individuals created (`rice:label_<paddy-doctor-string>`),
each with exactly one `fromSource` (→ `PaddyDoctorDataset`) and one
`denotes`. `Hispa`'s label denotes `Hispa_Leaf_Damage` (the Infestation),
not the `Hispa` Pest itself, per the worklog. All 10,407 `annotatedAs`
assertions retargeted from domain entities to the label individuals.
`sourceDatasetLabel` moved off all 10,407 images and the 10 domain
individuals onto the 10 label individuals (net −10,356 triples); its
`rdfs:domain` is now `AnnotationLabel`.

**2.3 — Deadheart → captures.** `scripts/task_2_3_deadheart_captures.py`.
Exactly 1,442 `captures` triples added, all `ImageObservation` →
`rice:Deadheart`. `annotatedAs` count unchanged at 10,407.

**2.4 — defined classes.** `scripts/task_2_4_defined_classes.py`.
`SymptomaticObservation ≡ Observation ⊓ ∃captures.Symptom` and
`StemBorerCandidate ≡ Observation ⊓ ∃captures.(Symptom ⊓
∃indicates.Stem_Borer_Damage)`. **Deviation from the worklog's literal
text:** it says "indicates Stem_Borer", but per the 2.2b fix that target is
now `Stem_Borer_Damage` (targeting the bare Pest would be unsatisfiable
under the Task 1.4 range and wouldn't match any data). No reasoner
available (see below) — membership was instead computed by direct graph
query, documented in `reports/task_2_4_reasoner_blocked.md`:
`SymptomaticObservation` materialises 1,442 members, `StemBorerCandidate`
also 1,442 (same underlying set — `Deadheart` is currently the only
`Symptom` with `captures` instance data at all).

## verify.py deltas

| Quantity | After Phase 1 | After Phase 2 |
|---|---|---|
| Total triples | 84,177 | 75,328 |
| Named classes | 21 | 23 (+2 defined classes) |
| Individuals | 10,466 | 10,482 (+6 Infestation, +10 AnnotationLabel) |
| `captures` (→Deadheart) | 0 | 1,442 |
| `sourceDatasetLabel` | 10,417 | 10 |

## Blocked / not checked

- **Reasoner-based satisfiability check** — not run, no Java in this
  environment. `SymptomaticObservation`/`StemBorerCandidate` membership was
  computed by hand-written graph query instead (exact for these two simple
  existentials, since no additional subsumption reasoning is needed beyond
  inverse-property closure — but this is not a substitute for a real
  consistency check across the whole ontology).
- **Task 2.2's vector–pathogen relations** — CSV emitted, nothing filled in
  (Checkpoint C6). The rice tungro case additionally needs a new `Pest`
  (leafhopper) and `Pathogen` (virus) individual before it's even fillable.
