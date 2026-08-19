# Rice MMKG — description, statistics, and changelog

Status snapshot as of **2026-08-19**, commit `c37dcf8` (post-cleanup).
Covers `Ontology/Rice MMKG.rdf` from its first commit through the current
state. Numbers below were measured with rdflib 7.6.0 via
`Worklog/RiceMMKG_cleanup_worklog/scripts/verify.py`.

---

## 1. Description

Rice MMKG is an OWL 2 knowledge graph for rice disease and pest diagnosis,
built around the [Paddy Doctor](https://www.kaggle.com/datasets/petmod/riceleafs)
image dataset. It links rice diseases, pests, pathogens, symptoms,
environmental factors, growth stages, treatments, and management actions,
and keeps two things deliberately separate:

- **Raw dataset annotation** (`rice:annotatedAs`) — what the Paddy Doctor
  label folder says an image is, asserted on all 10,407 image individuals.
- **Domain-knowledge evidence** (`rice:captures` → `rice:indicates`) — a
  narrower, independently-populated chain from observed symptom to
  diagnosed condition. Currently populated only for the `Deadheart` symptom
  (1,442 images), since that's the one place the dataset's own label
  happens to already coincide with a `Symptom`-typed entity rather than a
  `Disease`, `Pest`, or `HealthStatus` one.

**Namespace:** `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#`
(prefix `rice:`) — not yet dereferenceable; a `w3id.org` permanent
identifier is planned but not registered.

**Design philosophy (current, post-cleanup):** every class holds
individuals and every asserted property holds assertions, with one
deliberate exception — `SensorObservation` is kept empty as declared
scaffolding, matching a conceptual-schema diagram, ahead of sensor data
ever being ingested. Beyond that, classes and properties that would be
justified by data the ontology doesn't have yet (a second annotation
dataset, textual reports, pest damage modelled separately from the pest
organism, geolocation) are deliberately deferred rather than built ahead
of time — see `Worklog/RiceMMKG_v0.4-minimal_worklog/deferred_design.md`
for the full list and what would trigger building each one. The image
modality class is named `ImageObservation` (not `LeafImage`) since the
2026-08-19 cleanup round — the old name was factually wrong for the part
of the corpus that isn't a leaf (panicle blight, deadheart).

**License:** CC BY 4.0. **Creator:** Muhammad Ariful Furqon (ORCID
0000-0002-1031-3567). **Version:** `0.3` (see the open versioning
checkpoint below — `0.4` is proposed but not yet applied).

---

## 2. Statistics (current state)

| Quantity | Value |
|---|---|
| Total triples | 64,662 |
| Named classes | 16 (13 primitive + 1 empty-by-design + 1 dcat:Dataset + 1 defined) |
| Object properties | 24 |
| Datatype properties | 5 |
| Annotation properties | 13 |
| Individuals | 10,463 |
| `owl:Restriction` axioms | 1 (inside the one defined class) |
| `AllDisjointClasses` axioms | 2 |
| `skos:exactMatch` / `closeMatch` | 19 / 8 |
| Domain individuals with no AGROVOC alignment | 30 |
| `TODO` literals remaining | 9 |
| Individuals typed only `owl:NamedIndividual` | 0 |
| Properties with no declared domain/range | 0 / 0 |

### Per-class individual counts

| Class | Individuals |
|---|---|
| `ImageObservation` | 10,407 |
| `Symptom` | 11 |
| `Disease` | 8 |
| `Pest` | 6 |
| `Treatment` | 6 |
| `EnvironmentalFactor` | 5 |
| `GrowthStage` | 5 |
| `ManagementAction` | 5 |
| `SeverityLevel` | 4 |
| `Pathogen` | 3 |
| `Dataset` (`dcat:Dataset`) | 1 |
| `HealthStatus` | 1 |
| `Plant` | 1 |
| `Observation` (abstract superclass) | 0 direct |
| `SensorObservation` (empty by design, scaffolding) | 0 |
| `SymptomaticObservation` (defined class) | 0 direct — 1,442 by query/reasoner |

### Per-property assertion counts (populated only)

| Property | Assertions |
|---|---|
| `annotatedAs` | 10,407 |
| `captures` | 1,442 |
| `vulnerableTo` | 23 |
| `controlledBy` | 16 |
| `occursIn` | 16 |
| `indicatedBy` | 14 |
| `recommends` | 13 |
| `increaseRiskOf` | 10 |
| `sourceDatasetLabel` | 10 |
| `requires` | 4 |
| `causes` | 3 |
| `preventedBy` | 2 |

`sourceDatasetLabel` moved from 10,417 (10,407 redundant image-side copies
+ 10 on domain entities) down to just the 10 in the 2026-08-19 cleanup —
the raw label string is reachable from an image via `annotatedAs` already,
so repeating it per-image was redundant. `dcterms:source` was similarly
removed from all 10,407 images (redundant with `prov:wasDerivedFrom`,
kept).

All twelve inverse directions (`indicates`, `detectedBy`, `causedBy`, etc.)
and `detects` are declared but intentionally unasserted — only one
direction of each pair is populated; the ontology comment says so
explicitly, so this isn't missing data.

### Trajectory across major versions

| Version | Date | Triples | Classes | Object props | Individuals |
|---|---|---|---|---|---|
| Initial commit | 2026-07-28 | — | — | — | — |
| v2.0 (README label) | ~2026-08-05 | — | 12 | 22 | 60 |
| v0.2 (post-AGROVOC alignment) | 2026-08-17 | 52,806–52,816 | 17 | 24 | 10,467 |
| v0.3 (post-provenance/EPPO/rename) | 2026-08-18 | 84,064 | 18 | 24 | 10,463 |
| v0.4-expanded (superseded same day) | 2026-08-19 | 75,309 | 22 | 32 | 10,482 |
| v0.4-minimal | 2026-08-19 | 85,465 | 14 | 24 | 10,463 |
| + `SensorObservation` added | 2026-08-19 | 85,459 | 15 | 24 | 10,463 |
| **post-cleanup (current)** | **2026-08-19** | **64,662** | **16** | **24** | **10,463** |

The v0.4-expanded row is included for the record but was reverted the same
day — see §3 below. The "v2.0" row is from `README.md`'s own version label
at the time, not a `verify.py` measurement — no triple count is available
for it. The drop from 85,459 to 64,662 in the cleanup round is redundancy
removal (20,814 triples), not data loss — see §3.

---

## 3. Changelog

### 2026-07-28 — 2026-08-06: initial schema and population

- `7fc55b5` **MMKG Ontology** — first commit.
- `015ee12` **update ontology**
- `6058a9e` **update schema from paddy doctor**
- `cb6a4e2` **paddy doctor dataset analysis**
- `4928079` **review downy mildew**
- `021f93b` **align rest of ontology**
- `ed98c73` **add classified as** — introduces the `classifiedAs` property that later becomes `annotatedAs`.
- `2cfa864` **Populate Rice MMKG with Paddy Doctor image observations** — the 10,407 `LeafImage` individuals enter the graph.
- `bc63509` **Finalize alignment and answer CQ**
- `e5f6f09` **Formalize schema: fix consistency bug, add functional properties, split Observation into channel subclasses** — introduces `LeafImage`/`SensorReading`/`FieldObservation`/`FarmerReport`/`DiseaseReport` as `Observation` subclasses.
- `06f3c49` **update alignment**

### 2026-08-17: cross-vocabulary alignment

- `ab3c1c5` **Add NCBI Taxonomy cross-check, multimodal fusion PoC, and an ontology backup**
- `25e9a7b` **Resolve four EnvironmentalFactor category mismatches via Planteome**

### 2026-08-18: v2.3 → v0.3 — provenance, EPPO, versioning, cleanup

- `456d0c8` **Rice MMKG v2.3: rename classifiedAs, add provenance/EPPO/image links, restructure prototypes** — renamed `classifiedAs`→`annotatedAs`; added PROV-O provenance (`PaddyDoctorDataset`, `wasDerivedFrom`) to all 10,407 images; added `schema:contentUrl` image paths (the Paddy Doctor dataset was found locally, so paths were verified against real files rather than left as a template); added 3 verified EPPO codes + 6 TODO markers; added ontology FAIR metadata; converted 4 prototype "class-as-instance" individuals into `owl:Restriction`s and deleted them; narrowed sensor property domains.
- `c78ca80` **Use v0.3 versioning for Rice MMKG since it has not been publicly released** — `owl:versionInfo`/`versionIRI` moved from `2.3` to `0.3`, continuing the pre-existing 0.x pre-release scheme instead of jumping to a 2.x number.
- `38e5d8e` **Stop importing full PROV-O/DCTERMS vocabularies, declare only used terms** — fixed `owl:imports` pulling the entire external DCTERMS/PROV-O class hierarchies into Protégé's view; switched to declaring only the ~7 terms actually used.
- `8e70498` **Fill in dcterms:license, creator, and issued metadata** — CC BY 4.0, ORCID, issue date.

### 2026-08-19: v0.4 expansion, built and then reverted the same day

- `6d12903` **Rice MMKG v0.4: three-layer schema restructuring** — expanded to 22 classes (`Agent`, `Dataset`, `AnnotationLabel`, `Infestation`, `Location`, `ObservationEvent`, `TextualReport`, etc.), 32 object properties, retargeted `Pest`→`Infestation` across 45 assertions, introduced `SymptomaticObservation` and `StemBorerCandidate` defined classes.
- `6ff9d51` **Fix StemBorerCandidate: use owl:hasValue instead of someValuesFrom** — corrected an invalid restriction (an individual filler in a class-position slot) that was causing `Stem_Borer_Damage` to be punned into the class hierarchy in Protégé.
- `8feba7e` **Remove StemBorerCandidate defined class** — removed per request; `SymptomaticObservation` kept.
- `e8ab8ec` **Rice MMKG v0.4-minimal: shrink schema to what the data actually supports** — reverted the expansion. Rebuilt from the true v0.3 baseline instead: deleted the four empty `Observation` subclasses and the orphan `prov:Entity` declaration (18→13 classes); kept `captures`/`detects` declared but unasserted; deleted the four unused sensor datatype properties (9→5); converted the 1,442 `Deadheart`-annotated images into `captures` evidence; added the single `SymptomaticObservation` defined class; wrote `deferred_design.md` recording what was deliberately not built and why.
- `a968b62` **Add SensorObservation as an Observation subclass, matching the conceptual schema** — empty on arrival (0 individuals), scaffolding for future sensor data, per a conceptual-schema diagram. Incidentally picked up a Protégé auto-save that dropped 4 `owl:Restriction` blank nodes orphaned by a bug in the v0.4-minimal Task 1.1 script, and removed `PaddyDoctorDataset`'s legacy `prov:Entity` type.
- `c37dcf8` **Rice MMKG cleanup: dataset typing, provenance/label redundancy, naming, detects range** — the largest single-commit triple-count drop in the project's history (85,459 → 64,662). `PaddyDoctorDataset` typed `dcat:Dataset` (was the last individual typed only `owl:NamedIndividual`); deleted 10,407 redundant `dcterms:source` triples on images (kept `prov:wasDerivedFrom`); deleted 10,407 redundant `sourceDatasetLabel` triples on images and gave the property a declared domain (was the only property in the ontology without one); renamed `LeafImage`→`ImageObservation` (10,407 individuals retyped); restored `AllDisjointClasses {ImageObservation, SensorObservation}`; narrowed `detects`' range to `Pest ⊔ Pathogen` (removing `Disease`, closing an evidence/conclusion conflation the `annotatedAs` rename had left open in the property's still-unused declaration). Three checkpoints emitted as CSVs/reports, none resolved: Paddy Doctor dataset metadata, `contentUrl` base URL, and two AGROVOC alignment defects plus 30 unaligned entities (regrouped from a stale worklog count).

### Recurring pattern across sessions

Three separate rounds (`v2.3`, `v0.4`-expanded, `v0.4`-minimal) each found
that a worklog's stated "baseline" or "unaligned entity count" was stale
relative to the ontology's actual state — most often because AGROVOC/EPPO
alignment work landed between when a plan was written and when it was
executed. Each time, the actual measured numbers were adopted in place of
the stale ones, with the discrepancy documented rather than silently
absorbed. The AGROVOC-unaligned count has stayed close to 30 throughout
(the "30 vs. a smaller stated number" pattern shows up in `v2.3`, `v0.4`,
and `v0.4-minimal`'s worklogs alike).

---

## 4. Open items

- **AGROVOC:** 2 conflicting/suspicious matches (`Fungicide_Application`/
  `Insecticide_Application` sharing one concept IRI; `Rice_Blast_Disease`'s
  oddly-shaped identifier) + 30 unaligned domain individuals, grouped
  8 disease/pest · 9 symptom · 13 management/severity/stage. See
  `Worklog/RiceMMKG_cleanup_worklog/alignment_check.csv` and
  `agrovoc_todo.csv`.
- **Paddy Doctor dataset metadata:** `dcterms:title`/`license`/`source` on
  `PaddyDoctorDataset` still `TODO`. See
  `Worklog/RiceMMKG_cleanup_worklog/dataset_metadata.csv`.
- **Image URL resolvability:** `schema:contentUrl` holds relative paths
  that don't dereference. Three options written up, none chosen. See
  `Worklog/RiceMMKG_cleanup_worklog/contenturl_base.md`.
- **Permanent identifier:** `w3id.org` path segment not yet chosen; base
  IRI not yet rewritten.
- **Version number:** `0.3` still live; `0.4` proposed, not applied.
- **EPPO codes:** 3 of 9 organisms verified; 6 still `TODO`.
- **No reasoner available** in the working environment (no Java) — several
  acceptance checks across sessions (consistency, DL-classified defined-
  class membership) were substituted with direct graph queries, exact for
  the simple cases involved but not a general substitute.
