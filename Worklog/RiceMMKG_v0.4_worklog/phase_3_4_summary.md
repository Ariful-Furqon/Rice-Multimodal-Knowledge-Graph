# Phase 3 (Availability) & Phase 4 (Evaluation) summary

Phase 3 is almost entirely checkpoint-gated by design (the worklog's own
words: "The run will stop at these. They are decisions, not blockers to
work around."). Everything answerable without a human decision was done;
everything else is prepared and stopped.

## Task 3.1 — permanent identifier (Checkpoint C1)

**Not registered, base IRI not rewritten** (per the worklog's own
instruction not to rewrite until registration is confirmed).
`reports/w3id_config/README.md` explains what's needed — specifically, the
`w3id.org` path segment — and `reports/w3id_config/.htaccess.template` is a
placeholder redirect config, not something to submit as-is.

## Task 3.2 — version numbering (Checkpoint C2)

`owl:versionInfo`/`owl:versionIRI` still read `0.3` — not bumped. The
worklog frames this as an open 0.3-vs-2.2 question, but that was already
resolved in the prior session (deliberate 0.x pre-release track, per your
explicit decision). What's actually open now is only the next number
(`0.4`, presumably). See `reports/versioning.md`.

## Task 3.3 — alignment defects (Checkpoint C3)

`reports/alignment_check.csv`: the two flagged defects (`Fungicide_Application`
/`Insecticide_Application` sharing AGROVOC `c_27879`; `Rice_Blast_Disease`'s
oddly-shaped `c_152ac092`), confirmed present exactly as the worklog
describes. `reports/agrovoc_todo_v0.4.csv`: **36 rows**, not the worklog's
stated 8 — the worklog's list is the same kind of stale snapshot found in
the v0.3 round (30 individuals were already unaligned then; the 6 new
`Infestation` individuals from this round add to that, none subtracted).
Nothing was resolved automatically; both files are empty templates for
human lookup.

## Task 3.4 — metadata, licence, maintenance

`dcterms:description` added to the ontology node (the one metadata
predicate from the worklog's list that was still missing — title, creator,
license, issued, preferredNamespacePrefix were already set in the prior
session). `reports/maintenance_plan.md` written, with two fields left
`TODO` (release cadence, issue-tracker URL — both depend on C1/C2).
`reports/zenodo_deposit_manifest.json` and `reports/agroportal_submission.md`
are templates; several fields are blocked on the C1 permanent identifier.

## Task 4.1 — agreement study

Computed (no reasoner — see below): the inference path
(`captures→indicates`) and annotation path (`annotatedAs→denotes`) agree
100% over the 1,442 `StemBorerCandidate` members — **but this is a
tautology, not a validation result**, because Task 2.3 built the
`captures` assertions directly from the `annotatedAs` labels rather than
from independent evidence. Full explanation and what a real test would
need in `reports/agreement.md`.

## Cross-cutting blocker: no reasoner available

Java is not installed in this environment; `owlready2` (now installed) needs
it for HermiT/Pellet. This blocks: Task 1.5's "no unsatisfiable classes"
check, Task 2.4's proper DL-classified membership counts (worked around by
direct graph query — exact for these two simple existentials, not a general
substitute), and any deeper consistency check ahead of the agreement study.
If this ontology is going to be reasoned over for the paper's evaluation
section, a JRE needs to be available somewhere before that work continues.

## Checkpoints outstanding

| | Decision | Status |
|---|---|---|
| C1 | w3id namespace string | **needs your answer** — `reports/w3id_config/README.md` |
| C2 | version numbering | **needs your answer** — `reports/versioning.md` |
| C3 | AGROVOC IRIs (duplicate + 36 missing) | **needs human lookup** — `reports/alignment_check.csv`, `reports/agrovoc_todo_v0.4.csv` |
| C4 | Location granularity | **not started** — no Location individuals created, per the worklog |
| C5 | broaden symptom annotation beyond Deadheart | **not started** — same 250-image sample from v0.3 exists but was never annotated |
| C6 | vector–pathogen pairs | **needs human lookup** — `reports/vector_todo.csv`, `reports/task_2_2_vector_notes.md` |
| — | Java/reasoner availability | **needs a decision** — install a JRE, or accept direct-query workarounds as the ceiling for this environment |
