# Rice MMKG — maintenance plan

**Maintainer.** Muhammad Ariful Furqon (ORCID: 0000-0002-1031-3567).

**Cadence.** No fixed release schedule yet. Changes are made per research
milestone, tracked as v0.x pre-release versions; each version bump gets its
own `owl:versionIRI`. TODO: confirm a target cadence once past pre-release
status — left open pending Checkpoint C5.

**Issue tracking.** GitHub Issues on the repository hosting this ontology.
TODO: confirm the public repository URL once decided (see Task 4.1, w3id /
Checkpoint C4 — the repository this redirects to is the same one issues
should be filed against).

**Change process.** Structural changes go through a scripted migration
(rdflib, one idempotent script per task) with `scripts/verify.py` run
before and after, and a `reports/phase_N_summary.md` written per phase.
This keeps every change auditable against a stated baseline rather than
hand-edited in Protégé. This round additionally enforces: no class is
introduced without individuals to populate it, and no class is deleted
without first counting and reporting the assertions it would silently
take with it.

**Backups.** Each major revision is snapshotted under `Ontology/Rice
MMKG.backup-<timestamp>.rdf` before being overwritten, in addition to git
history.

**This document is incomplete.** Cadence and issue-tracker URL are marked
TODO above and need your input.
