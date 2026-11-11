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

**Modalities:** fixed at the data freeze of 2026-10-16 (v0.7.0): image and text are the strongest modalities; sensor, light-trap and multispectral data are thin; genomic data is not modelled. A new source is admitted only if it closes a gap listed in the README (Modality Coverage & Data Gaps). A declared class with no individuals is not described as a maintained modality.

## Identifiers

- **Namespace:** `https://w3id.org/ricemmkg#` — registered through [perma-id/w3id.org#6697](https://github.com/perma-id/w3id.org/pull/6697), merged 2026-09-16, and used by the ontology since 0.7.0-dev. Releases up to v0.6.2 used `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#`.
- **Version IRIs:** `https://w3id.org/ricemmkg/<version>` redirect to the ontology file at git tag `v<version>`.
- **Redirect configuration:** `w3id/ricemmkg/` in this repository mirrors the files registered at w3id.org; changes are made here first and then submitted to w3id.org.

## Versioning

Versions follow `MAJOR.MINOR.PATCH`, recorded in `owl:versionInfo` and appended to `owl:versionIRI`. The project is pre-1.0 while under active construction.

| Change | Bump | Examples |
|---|---|---|
| Corrections that change no modelling decision: provenance fixes, citations, source URIs, literal hygiene, a missing assertion restored with its source | **PATCH** (`0.6.1` → `0.6.2`) | v0.6.1 provenance gaps; v0.6.2 CABI DOIs |
| Completing a source already in the graph, with no new class or property and no changed modelling decision: more passages of a document already cited, the assertions that source states, the individuals and alternative labels they need (added 2026-11-11) | **PATCH** (`0.9.0` → `0.9.1`) | v0.9.1 cause and control text of IRRI (2018) *Rice Diseases* |
| New classes or properties, new populated modalities, new batches of annotations from a new source, removal or retyping of entities | **MINOR** (`0.6` → `0.7`) | Deadheart retyped as Disease (v0.6) |
| The release accompanying the paper submission | **1.0** | — |

Each version number names exactly one content state: a change is never folded silently into an already-tagged version.

## Release cadence

- **Release map** (revised 2026-11-07; it replaces the map of 2026-09-17, which tied the minor releases to the phases of the ESWC 2027 plan, dropped with that submission; the plan was removed on 2026-11-09 and is kept at tag `v0.9.0` (`Ontology/riceMMKG_ESWC_plan.md`)):
  - **v0.7.0:** scaffolding and modalities (image and text the strongest). Tagged on 2026-11-07 at the data-freeze commit of 2026-10-16 (same commit as `data-freeze-2026-10`; the file there reads `0.7.0-dev`). The 0.7.0-dev work after the freeze (text layer, `Deadheart` as a symptom) is in v0.8.0.
  - **v0.6.0:** tagged on 2026-11-07 at the v0.6 release of 2026-09-03 (same commit as `elicited-baseline-v0.6`). The descriptive tags are kept, because tags are never deleted and documents cite them.
  - **v0.8.0** (tagged 2026-11-07): the symptom inventory, and the visual symptoms of blast and brown spot.
  - **0.8 → v0.9: benchmark.** The changes the retrieval benchmark needs from the KG: the rest of the symptom inventory, its provenance fixes and the missing sources. **v0.9.0** tagged 2026-11-07 (changelog in `Ontology/Ontology_Overview.md`).
  - **v0.9.1** (2026-11-11, PATCH by the rule above; it was `0.9.1-dev` from 2026-11-09): post-release work on the KG (the management layer for CQ-12 and evidence passages for the cause, management and stage facts) and the cause and control text of IRRI (2018) for leaf scald, downy mildew and bacterial panicle blight, which the benchmark's pooling needs. v0.9.0 stays the release the retrieval benchmark starts from; results on later states are reported as separate KG versions.
  - **0.9 → v1.0: FAIR and finalisation.** Documentation at the PURL, FOOPS!/OOPS!, Zenodo DOI, AgroPortal, a smaller distribution file and expert validation of the elicited CQs.
  - Development between tags carries `-dev` (e.g. `0.9.0-dev`), as 0.7.0-dev did.
- **Patch releases are made whenever a verified correction is ready**, with no fixed schedule.
- After submission, releases continue as needed rather than on a fixed calendar.

## Release checklist

1. Bump `owl:versionInfo` and `owl:versionIRI`.
2. Add a dated entry to the changelog in `Ontology/Ontology_Overview.md` and update the statistics measured, not copied.
3. Check consistency with HermiT on a copy of the ontology in a path **without spaces** (spaces make the OWL API exit without loading the file, which looks like a pass), together with a control copy containing a deliberate contradiction that must be reported as inconsistent.
4. Run `cq_sparql_benchmark.py` and `elicited_cq_sparql.py`; compare against the previous tag and explain every change.
5. Commit, create an annotated tag `v<version>` on that commit, and push the commit and the tag.

**Tags are permanent.** Version IRIs resolve through them, so a tag is never moved, deleted or rewritten, and published history is not rewritten.

## Tag notes

Exceptions to the rules above, recorded on 2026-11-07. The tagged files cannot be changed, so each one is explained here instead.

| Tag | Commit | What differs | Why |
|---|---|---|---|
| `v0.6.0` | `a2bff71` (= `elicited-baseline-v0.6`) | The file reads `versionInfo 0.6` and `versionIRI http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG/0.6`, not `0.6.0` | Tagged on 2026-11-07 for the v0.6 release of 2026-09-03, which predates the three-part version numbers and the w3id namespace |
| `v0.7.0` | `3c99091` (= `data-freeze-2026-10`) | The file reads `versionInfo 0.7.0-dev`. The release checklist was not run as a release; the data-freeze baseline of both CQ instruments (changelog, 2026-10-17 to 2026-10-19) is its nearest equivalent | Tagged on 2026-11-07 at the data freeze of 2026-10-16, which closed the modality phase. The 0.7.0-dev work after the freeze (text layer, `Deadheart` as a symptom) is in `v0.8.0` |
| `v0.8.0` | `d2888bb` | The file names `owl:priorVersion` `https://w3id.org/ricemmkg/0.6.2`, not `…/0.7.0` | `v0.7.0` was tagged after `v0.8.0`. The prior version is `…/0.7.0`, not "0.7.0-dev": `owl:priorVersion` takes a version IRI that resolves to one fixed file, and 0.7.0-dev named many changing states. `…/0.7.0` resolves to the frozen one, whose file reads `0.7.0-dev` |

**Fixed in 0.8.1:**
- `owl:priorVersion` is now `0.8.0`;
- the ontology's `rdfs:comment` now names 0.6.0, 0.6.1 and 0.6.2, and says that every later tag `v<version>` resolves at `https://w3id.org/ricemmkg/<version>`.

**Descriptive tags:** `elicited-baseline-v0.6` and `data-freeze-2026-10` are kept next to `v0.6.0` and `v0.7.0`, because documents cite them. Their names do not match the version pattern, so they have no w3id IRI.

## Backups

The state before each patch is kept in `Ontology/Backup/` in addition to the git history. Superseded intermediate files are archived there rather than deleted (e.g. `provenance_axioms.archived-2026-09-14.rdf`) and must not be merged back into the ontology.
