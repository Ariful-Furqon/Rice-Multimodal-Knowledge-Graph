# Rice MMKG — maintenance plan

**Maintainer.** Muhammad Ariful Furqon (ORCID: 0000-0002-1031-3567).

**Cadence.** No fixed release schedule yet. Changes are made per research
milestone (currently tracked as v0.x pre-release versions); each version
bump gets its own `owl:versionIRI`. TODO: confirm a target cadence once the
ontology moves past pre-release status (e.g. tied to publication or thesis
chapter milestones) — left open pending Checkpoint C2.

**Issue tracking.** GitHub Issues on the repository hosting this ontology
(`Ontology/Rice MMKG.rdf` in this working tree). TODO: confirm the public
repository URL once decided (see Task 3.1, w3id / Checkpoint C1 — the
repository this redirects to is the same one issues should be filed
against).

**Change process.** Structural changes go through a scripted migration
(rdflib, one script per task, idempotent) with a `scripts/verify.py`
regression check run before and after, and a `reports/phase_N_summary.md`
written per phase — the pattern used for the v0.3 and v0.4 revisions. This
keeps every change auditable against a stated baseline rather than
hand-edited in Protégé.

**Backups.** Each major revision is snapshotted under `Ontology/Rice
MMKG.backup-<timestamp>.rdf` before being overwritten, in addition to git
history.

**This document is incomplete.** Cadence and issue-tracker URL are marked
TODO above and need your input — a maintenance plan with placeholders in it
is still a scored deficiency per the worklog; these two items are what's
left before it's not.
