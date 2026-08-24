# Maintenance plan (Task C.3)

FOOPS!'s OM5_1/OM5_2 checks and the ESWC resources-track criteria both
score a maintenance statement's presence — its absence is a scored
deficiency, not just good practice. This draft covers what can be
answered from repo state; two fields need the maintainer's own decision
(marked TODO) rather than being inferred.

## Maintainer

Muhammad Ariful Furqon (ORCID: [0000-0002-1031-3567](https://orcid.org/0000-0002-1031-3567)),
per the ontology's `dcterms:creator`. TODO — confirm whether this should
also list an institutional affiliation for the paper/deposit metadata.

## Where issues are filed

GitHub Issues on this repository:
`https://github.com/Ariful-Furqon/Rice-Multimodal-Knowledge-Graph`
(current canonical location per the repo's own move-notice; the local
git remote still points at the pre-move URL, so `git remote -v` shows
the old address — worth updating the remote to avoid the redirect
warning on every push).

## Release cadence

TODO — no cadence has been stated anywhere in the repo's history. Options
worth considering rather than guessing one: (a) tied to ESWC submission
milestones (draft/camera-ready/post-acceptance), which is the most
concrete near-term driver; (b) a lighter "patch as errors are found"
cadence long-term once the paper is submitted, similar to how v0.4 → v0.5
happened (a batch of verified-defect corrections, not a fixed schedule).

## Versioning scheme

Already established and consistent: `owl:versionInfo` /
`owl:versionIRI` follow `MAJOR.MINOR` (`0.1` → `0.5` so far, pre-1.0
while still in active construction), with the version segment appended
to the versionIRI path (e.g. `.../riceMMKG/0.5`). Each bump corresponds
to a batch of changes documented in a dated worklog
(`Worklog/RiceMMKG_*_worklog/`) and a changelog entry in
`Ontology/Ontology_Overview.md` — that pairing is the de facto process
already in use across this project's history and is the one to keep.

## Scope of what's maintained

- The ontology file (`Ontology/Rice MMKG.rdf`) and its schema/domain
  assertions, including provenance records.
- The three alignment registers (`AGROVOC_alignment.md`,
  `NCBI_Taxonomy_alignment.md`, `Planteome_alignment.md`) as the source
  of truth for any external vocabulary mapping — any future alignment
  work should be checked against these before being applied (a process
  gap that caused a real correction earlier in this project's history;
  see `Ontology/Ontology_Overview.md`'s 2026-08-22 changelog entries).
- **Not maintained as part of this scope**: the underlying Paddy Doctor
  image dataset itself (third-party, referenced not redistributed) and
  the sensor/text modality classes, which remain declared-but-empty
  extension points by design.

## What's explicitly not decided here

- TODO: institutional affiliation string for formal deposits (Zenodo,
  AgroPortal).
- TODO: fixed release cadence beyond "tied to paper milestones, then
  as-needed."
