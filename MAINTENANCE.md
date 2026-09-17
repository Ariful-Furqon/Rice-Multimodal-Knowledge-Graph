# Maintenance Plan — Rice MMKG

How Rice MMKG is maintained, versioned and released. Last updated 2026-09-15.

## Maintainers

| Name | Role | Affiliation | ORCID | GitHub |
|---|---|---|---|---|
| Muhammad Ariful Furqon | Maintainer, creator | Japan Advanced Institute of Science and Technology (JAIST) | [0000-0002-1031-3567](https://orcid.org/0000-0002-1031-3567) | [@Ariful-Furqon](https://github.com/Ariful-Furqon) |
| Natthawut Kertkeidkachorn | Creator | Japan Advanced Institute of Science and Technology (JAIST) | [0000-0003-4527-776X](https://orcid.org/0000-0003-4527-776X) | — |

## Contact and issue reporting

Report errors, questions and requests through **GitHub Issues**:
https://github.com/Ariful-Furqon/Rice-Multimodal-Knowledge-Graph/issues

Useful things to include: the IRI of the term involved, the version (`owl:versionInfo`, or the git tag), and — for a factual error in a domain assertion — the source that contradicts it.

## What is maintained

- **The ontology** — `Ontology/Rice MMKG.rdf`, the single source of truth for the schema, the domain assertions and their provenance. Every domain assertion carries an `owl:Axiom` with `dcterms:source`, `dcterms:bibliographicCitation` and `rice:evidenceType`; checked by benchmark CQ-21 and CQ-22.
- **Provenance and alignment registers** — `Analysis and Alignment/` (AGROVOC, NCBI Taxonomy, Planteome, and the provenance register). Any new external alignment is checked against these registers before it is applied, and every external identifier is looked up live before it is asserted.
- **The two competency-question instruments** — the 25-CQ benchmark (`cq_sparql_benchmark.py`) and the elicited-CQ queries (`elicited_cq_sparql.py`), with their reports.
- **Documentation** — `Ontology/Ontology_Overview.md` (statistics and changelog) and `CQ_SPARQL_Documentation.md`.

**Not maintained here:** the Paddy Doctor image dataset, which is third-party and referenced rather than redistributed (Petchiammal et al., 2022, CC BY 4.0).

**Modalities:** which further modalities (sensor, genomic) become part of the released resource is an open decision tracked in `Ontology/riceMMKG_ESWC_plan.md`. A declared class with no individuals is not described as a maintained modality.

## Identifiers

- **Namespace:** `https://w3id.org/ricemmkg#` — registered through [perma-id/w3id.org#6697](https://github.com/perma-id/w3id.org/pull/6697), merged 2026-09-16, and used by the ontology since 0.7.0-dev. Releases up to v0.6.2 used `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#`.
- **Version IRIs:** `https://w3id.org/ricemmkg/<version>` redirect to the ontology file at git tag `v<version>`.
- **Redirect configuration:** `w3id/ricemmkg/` in this repository mirrors the files registered at w3id.org; changes are made here first and then submitted to w3id.org.

## Versioning

Versions follow `MAJOR.MINOR.PATCH`, recorded in `owl:versionInfo` and appended to `owl:versionIRI`. The project is pre-1.0 while under active construction.

| Change | Bump | Examples |
|---|---|---|
| Corrections that change no modelling decision: provenance fixes, citations, source URIs, literal hygiene, a missing assertion restored with its source | **PATCH** (`0.6.1` → `0.6.2`) | v0.6.1 provenance gaps; v0.6.2 CABI DOIs |
| New classes or properties, new populated modalities, new batches of annotations, removal or retyping of entities | **MINOR** (`0.6` → `0.7`) | Deadheart retyped as Disease (v0.6) |
| The release accompanying the ESWC 2027 submission | **1.0** | — |

Each version number names exactly one content state: a change is never folded silently into an already-tagged version.

## Release cadence

- **Minor releases follow the phases of the ESWC plan** (decided 2026-09-17): **v0.7** closes Phase 2 (namespace and release scaffolding), **v0.8** closes Phase 3 (multimodal: modality checkpoint, grounding, schema), **v0.9** closes Phases 4 and 5 (expert validation and FAIR finalisation), and **v1.0** is the version submitted to ESWC 2027.
- **Patch releases are made whenever a verified correction is ready**, with no fixed schedule.
- After submission, releases continue as needed rather than on a fixed calendar.

## Release checklist

1. Bump `owl:versionInfo` and `owl:versionIRI`.
2. Add a dated entry to the changelog in `Ontology/Ontology_Overview.md` and update the statistics measured, not copied.
3. Check consistency with HermiT on a copy of the ontology in a path **without spaces** (spaces make the OWL API exit without loading the file, which looks like a pass), together with a control copy containing a deliberate contradiction that must be reported as inconsistent.
4. Run `cq_sparql_benchmark.py` and `elicited_cq_sparql.py`; compare against the previous tag and explain every change.
5. Commit, create an annotated tag `v<version>` on that commit, and push the commit and the tag.

**Tags are permanent.** Version IRIs resolve through them, so a tag is never moved, deleted or rewritten, and published history is not rewritten.

## Backups

The state before each patch is kept in `Ontology/Backup/` in addition to the git history. Superseded intermediate files are archived there rather than deleted (e.g. `provenance_axioms.archived-2026-09-14.rdf`) and must not be merged back into the ontology.
