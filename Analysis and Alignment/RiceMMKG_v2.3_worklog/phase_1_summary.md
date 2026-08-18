# Phase 1 summary — Rice MMKG v2.2 → v2.3

## Tasks completed

**0.1 — verification harness.** `scripts/verify.py`. Run against the actual
current ontology, it did **not** reproduce the worklog's baseline table (see
`reports/phase0_baseline_adopted.md`). Per user decision, the measured figures
were adopted as the corrected baseline and Phase 1 proceeded against them.

**1.1 — rename `classifiedAs`→`annotatedAs` / `classifies`→`annotationOf`.**
`scripts/task_1_1_rename_classifiedAs.py`. All 10,407 instance triples and the
property-level axioms (functional, subPropertyOf, domain, range union,
inverseOf) were renamed with identical subject–object pairs. Added the
range-union honesty comment. Added PROV-O + Dublin Core imports, a
`rice:PaddyDoctorDataset` `prov:Entity` individual (title/source/license left
`TODO`), and `prov:wasDerivedFrom` from all 10,407 `LeafImage` individuals to
that dataset entity. Zero `classifiedAs`/`classifies` remain.

**1.2 — image file pointers.** `scripts/build_image_manifest.py` +
`scripts/task_1_2_apply_image_manifest.py`. The Paddy Doctor dataset turned
out to be present locally at `Data/PaddyDoctor/<label>/<id>.jpg`, and all
10,407 `LeafImage` individual IRIs resolved to a verified file on disk via
the `PaddyDoctor_<label>_<id>` naming convention — no manifest CSV needed to
be hand-filled. `schema:contentUrl` (relative path) and `dcterms:source`
(→ `rice:PaddyDoctorDataset`) were added to every `LeafImage` individual.

**1.3 — EPPO codes.** `scripts/task_1_3_eppo_codes.py`. Added `rice:eppoCode`
(xsd:string) with exactly 3 verified assertions (`Brown_Planthopper`→NILALU,
`Magnaporthe_Oryzae`→PYRIOR, `Xanthomonas_Oryzae`→XANTOR), a
`skos:altLabel "Pyricularia oryzae"` on `Magnaporthe_Oryzae`, and 6 TODO
comments on the unverified organisms (`Bipolaris_Oryzae`, `Hispa`,
`Leaf_Folder`, `Stem_Borer`, `Rice_Bug`, `Armyworm`).

**1.4 — AGROVOC template + FAIR metadata.**
`scripts/task_1_4_metadata_and_agrovoc_template.py` + `scripts/apply_agrovoc.py`.
Ontology node now carries `dcterms:title`, `dcterms:creator` (ORCID
placeholder), `dcterms:license`, `dcterms:issued`, `owl:versionIRI`, and
`vann:preferredNamespacePrefix "riceMMKG"`; `owl:versionInfo` bumped to
`2.3`. `reports/agrovoc_todo.csv` emitted with **30 rows** (corrected list,
not the worklog's stale 10 — see baseline note) and empty
`agrovoc_iri`/`match_type` columns pending human lookup.

## verify.py deltas vs corrected baseline

| Quantity | Baseline | After Phase 1 |
|---|---|---|
| Total triples | 52,816 | 84,067 |
| Named classes | 17 | 17 |
| Object properties | 24 (12 pairs) | 24 (12 pairs) |
| Datatype properties | 9 | 9 |
| Annotation properties | 2 | 3 (+`eppoCode`) |
| Individuals | 10,467 | 10,468 (+`PaddyDoctorDataset`) |
| `owl:Restriction` | 0 | 0 |
| `skos:exactMatch` | 19 | 19 (unchanged — CSV not yet filled) |
| `skos:closeMatch` | 8 | 8 (unchanged) |
| Domain individuals w/o alignment | 30 | 30 (unchanged, expected) |

## Blockers / human-input-required items left in the ontology

- `rice:PaddyDoctorDataset`: `dcterms:title`, `dcterms:source`, `dcterms:license` = `TODO`
- Ontology node: `dcterms:creator` (ORCID), `dcterms:license`, `dcterms:issued` = `TODO`
- 6 organisms carry `rdfs:comment "TODO: verify EPPO code at gd.eppo.int"`
- `reports/agrovoc_todo.csv`: 30 rows pending AGROVOC IRI + match_type lookup
  (run `scripts/apply_agrovoc.py` once filled in)

## Acceptance checks relaxed

- **Task 1.4's "10 unaligned individuals" list** was superseded by the
  corrected 30-individual list. This is not a relaxation of the check itself
  (the check — emit a CSV covering every currently-unaligned domain
  individual — still holds), only of the specific count named in the
  worklog, which was stale. See `reports/phase0_baseline_adopted.md`.
- Task 1.2's manifest-CSV fallback path was not exercised because the
  dataset was found locally and every path was verified against a real file
  — a stronger guarantee than a hand-typed CSV, not a weaker one.
