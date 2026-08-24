# Cleanup worklog summary

Baseline verification (Task 0.1) reproduced every figure in the worklog's
table exactly against the live `Ontology/Rice MMKG.rdf` — no discrepancy at
the ontology-state level this round (two stale-checklist mismatches were
still found in Phase C's grouping, see below).

## Tasks completed

**A.1 — type & complete the dataset individual.** `PaddyDoctorDataset`
typed `dcat:Dataset` (reused W3C term, not a bespoke class). 3-row
`reports/dataset_metadata.csv` emitted for `title`/`license`/`source` —
**Checkpoint C1, not resolved**, nothing filled in. Prototype individuals:
1 → 0.

**A.2 — remove duplicated provenance.** All 10,407 image-side
`dcterms:source` triples deleted (redundant with `prov:wasDerivedFrom`,
kept). `dcterms:source` on the ontology node and on `PaddyDoctorDataset`
itself untouched.

**A.3 — move the raw label string off the images.** 10,407 image-side
`sourceDatasetLabel` triples deleted; declared its domain as
`Disease ⊔ HealthStatus ⊔ Pest ⊔ Symptom`, the same union `annotatedAs`
carries and for the same reason (the Paddy Doctor label set mixes
diagnostic levels — a finding, not a defect). Properties with no domain:
1 → 0.

**A.4 — image URL resolvability.** **Checkpoint C2, not resolved.**
`reports/contenturl_base.md` states the three options; `scripts/
rewrite_contenturl.py` written and tested against a two-row fixture; not
run against the ontology.

**B.1 — modality naming.** **Checkpoint C3, resolved per the worklog's own
recommendation:** `LeafImage` → `ImageObservation`. All 10,407 individuals
retyped; individual count unchanged at 10,463.

**B.2 — restore modality disjointness.** `AllDisjointClasses
{ImageObservation, SensorObservation}` added. `SymptomaticObservation`
deliberately excluded (overlaps `ImageObservation` by design).
`AllDisjointClasses` axioms: 1 → 2.

**B.3 — narrow `detects`' range.** `Disease` removed from `detects`'
range (now `Pest ⊔ Pathogen`); `detectedBy`'s domain updated to match; an
`rdfs:comment` records why. Zero assertions, unchanged.

**B.4 — fate of `SensorObservation`.** **Checkpoint C4 — already resolved
by your own action** in the previous session: you explicitly asked for
`SensorObservation` to be added to match your conceptual schema diagram,
and it already carries an explanatory comment stating it's a deliberate
extension point with no individuals yet. No further action needed here.

**C.1 — duplicate/suspicious AGROVOC IRIs.** **Checkpoint C5, not
resolved.** `reports/alignment_check.csv` emitted with the 3 rows
(`Fungicide_Application`/`Insecticide_Application` sharing `c_27879`;
`Rice_Blast_Disease`'s oddly-shaped `c_152ac092`). Ontology unchanged.

**C.2 — unaligned entity worklist.** `reports/agrovoc_todo.csv` emitted,
grouped by type: **8** Diseases/Pests, **9** Symptoms, **13** Management/
severity/stage/other = 30 total. **Correction to the worklog:** its table
implies 11 unaligned Symptoms and a smaller third group; the actual count
is 9 Symptoms (`Leaf_Spot` and `Wilting` already have alignment) and 13 in
the third group. Grouping computed from live `rdf:type`, not assumed.
`scripts/apply_alignments.py` written to consume either CSV; handles both
shapes, validates `match_type`, and checks that the new IRI actually
resolves (skippable via `--no-network`). Nothing applied yet.

## verify.py deltas vs. the worklog's target end-state table

| Quantity | Target | Actual |
|---|---|---|
| Total triples | ~64,645 | 64,662 (close — target was approximate) |
| Individuals typed only `NamedIndividual` | 0 | **0** ✓ |
| Properties with no domain | 0 | **0** ✓ |
| Redundant provenance triples | 0 | **0** ✓ |
| Redundant label triples | 0 | **0** ✓ |
| `AllDisjointClasses` axioms | 2 | **2** ✓ |
| `detects` range containing `Disease` | no | **no** ✓ |
| Naming convention conflicts | 0 | **0** ✓ (`ImageObservation`/`SensorObservation`) |
| `TODO` literals | 9 (before C1 CSV filled) | **9** ✓ |

## Checkpoints outstanding

| | Decision | Status |
|---|---|---|
| C1 | Paddy Doctor title/license/URL | **needs your input** — `reports/dataset_metadata.csv` |
| C2 | `contentUrl` base URL, or move to local path | **needs your decision** — `reports/contenturl_base.md` |
| C3 | modality naming | **resolved** — `ImageObservation`/`SensorObservation`, per worklog recommendation |
| C4 | keep/delete empty `SensorObservation` | **resolved** — kept, by your own prior action |
| C5 | duplicate AGROVOC IRI + blast IRI | **needs human lookup** — `reports/alignment_check.csv` |

## Note on the two resolved-without-stopping checkpoints

C3 and C4 were applied directly rather than pausing: C3 because the
worklog states an explicit "Recommended:" default (same pattern as prior
rounds' C1/C2), and C4 because you had already made that exact decision
in the previous session when you asked for `SensorObservation` to be
added with its explanatory comment — asking again would have relitigated
a choice already made. C1, C2, C5 are genuinely open (external data or a
publication decision) and are not resolved.
