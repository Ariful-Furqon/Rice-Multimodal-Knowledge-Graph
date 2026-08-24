# Phase 2, 3, 4 summary — v0.3 → v0.4-minimal

## Phase 2 — deferred design

`reports/deferred_design.md` written; **no ontology change**, as required.
Lists `TextualReport`, `SensorObservation`, `ObservationEvent`, `Location`,
`Agent`, `AnnotationLabel`+`Dataset`, and `Infestation` with trigger
condition and cost. Explicitly notes `AnnotationLabel`/`Dataset` gets more
expensive with every image added (would retarget all 10,407 `annotatedAs`
assertions), and that this is exactly why `annotatedAs`'s current range
union (`Disease ⊔ HealthStatus ⊔ Pest ⊔ Symptom`) exists — an honest
description of the data, not a defect.

## Phase 3 — populate what can be populated

**3.1 — Deadheart → captures.** `scripts/task_3_1_deadheart_captures.py`.
Exactly 1,442 `captures` triples added, all `LeafImage` → `rice:Deadheart`.
`annotatedAs` unchanged at 10,407. One symptom of eleven has instance
support — recorded here as the worklog requires.

**3.2 — the one defined class.** `scripts/task_3_2_symptomatic_observation.py`.
`SymptomaticObservation ≡ Observation ⊓ ∃captures.Symptom`. No reasoner
available in this environment (no Java) to formally confirm satisfiability;
membership was instead computed by direct graph query (exact for this
simple existential): **1,442 members**, matching the acceptance target.

**3.3 — alignment defects (Checkpoint C3).** Same two defects as the prior
round, reconfirmed present: `Fungicide_Application`/`Insecticide_Application`
share AGROVOC `c_27879`; `Rice_Blast_Disease`'s `c_152ac092` has an
oddly-shaped identifier. `reports/alignment_check.csv` (2 defect rows) and
`reports/unaligned_entities.csv` written. **Correction to the worklog:**
its "eight still-unaligned entities" list is a stale subset — the actual
count is **30** (the 8 named are all present in the 30, nothing was
resolved in between). `scripts/apply_alignments.py` written to consume
either file once a human fills in resolutions. Nothing applied yet.

## Phase 4 — availability

**4.1 — permanent identifier (Checkpoint C4).** Not registered, base IRI
not rewritten. `reports/w3id_config/README.md` + `.htaccess.template`.

**4.2 — version numbering (Checkpoint C5).** `owl:versionInfo`/`versionIRI`
still read `0.3`, not bumped. `reports/versioning.md` recommends `0.4` but
leaves the decision to you.

**4.3 — metadata, licence, maintenance.** `dcterms:description` added (the
one metadata field still missing — title/creator/license/issued/
preferredNamespacePrefix already existed on this backup from the prior
round's Phase 1.4 work). `reports/maintenance_plan.md` written, two TODOs
(cadence, issue-tracker URL) depending on C4/C5. `reports/zenodo_deposit_manifest.json`
and `reports/agroportal_submission.md` are templates, several fields
blocked on C4.

## Final verify.py snapshot vs. worklog's target end-state table

| Quantity | Worklog target | Actual |
|---|---|---|
| Named classes | 13 | **14** — see note below |
| Object properties | 24 | 24 |
| Datatype properties | 5 | 5 |
| Restriction axioms | 0 | 0 `someValuesFrom` remain from v0.3's four deleted-class restrictions; **1 new `someValuesFrom`** from Task 3.2's defined class (expected — defined classes use existentials by design, the worklog's "0" row is about the four *deleted* restrictions, not a ban on new ones) |
| Defined classes | 1 | 1 |
| Individuals | 10,463 | 10,463 |
| Empty classes | 0 | **2** (`Observation`, `SymptomaticObservation`) — see note below |
| Populated properties | 11 | matches (`annotatedAs`, `vulnerableTo`, `occursIn`, `controlledBy`, `indicatedBy`, `recommends`, `increaseRiskOf`, `requires`, `causes`, `preventedBy`, `captures`) |

**Named classes: 13 vs 14.** The worklog's table lists "Named classes: 13"
and "Defined classes: 1" as separate rows, but `SymptomaticObservation` (the
one defined class) is itself a named, IRI-bearing `owl:Class` — so any
literal count of `owl:Class` declarations is 14, not 13. This is a
bookkeeping quirk in how the worklog's own table is organized (primitive
vs. defined counted on different axes), not a deviation from what was
built.

**Empty classes: 0 target, 2 actual.** `Observation` has zero *direct*
`rdf:type` assertions — its individuals arrive entirely through the
`LeafImage` subclass (10,407 of them), which is only "empty" from
`Observation`'s own point of view without a reasoner doing subsumption.
`SymptomaticObservation` is a defined class — by construction, an OWL
reasoner would materialise 1,442 members, but no `rdf:type` triple is
literally asserted for any of them (matches how Task 3.2 computed and
reported its own count: by query, not by reasoner materialisation). The
"0 empty classes" target in the worklog's own table appears to describe
the *effective*, reasoner-classified state, which this environment can't
produce (no Java). Recorded honestly rather than forced by asserting
redundant direct types.

## Checkpoints outstanding

| | Decision | Status |
|---|---|---|
| C1 | keep or delete captures/detects | **resolved** — kept, per the worklog's own recommendation |
| C2 | sensor datatype properties | **resolved** — deleted, per the worklog's own recommendation |
| C3 | AGROVOC IRIs (duplicate + 30 missing) | **needs human lookup** |
| C4 | w3id namespace string | **needs your answer** |
| C5 | version numbering (0.4?) | **needs your answer** |
| — | Java/reasoner availability | same gap as the prior round — not installed here |
