# AgroPortal submission package — DRAFT (Task C.3)

**Not submitted.** AgroPortal (https://agroportal.lirmm.fr/) is the
community registry for agricultural ontologies/vocabularies (built on
the NCBO BioPortal technology), and running O'FAIRe gives a second,
independent FAIRness score alongside FOOPS!'s.

## Submission checklist

AgroPortal submission is done through its web UI (no public API for new
submissions) at **Submit an Ontology**, requiring:

| Field | Value | Status |
|---|---|---|
| Ontology acronym | `RICEMMKG` (suggested — short, uppercase, matches AgroPortal convention) | proposed, not confirmed |
| Ontology name | Rice MMKG — Rice Multimodal Knowledge Graph | from `dcterms:title` |
| Description | (same text as `dcterms:description`) | ready |
| Homepage | TODO — needs Task C.2's PURL, or the GitHub repo URL as an interim value | **blocked on C.2** |
| Ontology file location | Upload `Rice_MMKG_v0.5.rdf` directly, or point at a URL once one is dereferenceable | ready once hosting exists |
| Format | OWL/RDF-XML | ready |
| Contact name / email | TODO — confirm what to list publicly | needs human input |
| Categories | Plant Science / Plant Pathology (AgroPortal's own category list — confirm exact term at submission time) | proposed |
| Visibility | Public | proposed |

## Why this is still just a checklist, not a submission

Two blockers, both already tracked elsewhere:

1. **No dereferenceable homepage yet** — AgroPortal's form wants a
   homepage URL; the GitHub repository URL works as an interim value,
   but the PURL from Task C.2 is the better answer once it exists.
2. **Contact details** — the acronym and description can be filled from
   the ontology's own metadata, but AgroPortal's contact field is a
   human decision (whether to list a personal email, an institutional
   one, or a GitHub-issues pointer instead — same question as the
   maintenance plan below).

## O'FAIRe

Once submitted, AgroPortal runs O'FAIRe automatically and publishes a
FAIRness score on the ontology's AgroPortal page — no separate action
needed beyond the submission itself. Worth citing alongside the
OOPS!/FOOPS! scores in Task C.1 once available, as a second independent
FAIR assessment using a different rubric.
