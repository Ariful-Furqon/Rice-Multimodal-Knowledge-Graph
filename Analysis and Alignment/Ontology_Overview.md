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
0000-0002-1031-3567). **Version:** `0.4` (live as of 2026-08-21; pre-release progression: `v0.1` → `v0.2` → `v0.3` → `v0.4`).

---

## 2. Statistics (current state)

| Quantity | Value | Notes |
|---|---|---|
| **Total triples** | **67,236** | Up from 64,662 (+2,574 via enrichment, provenance & metadata polish) |
| **Named classes** | 16 | 13 primitive + 1 scaffolding + 1 `dcat:Dataset` + 1 defined class |
| **Object properties** | 24 | All declared with explicit domain and range |
| **Datatype properties** | 5 | All declared with explicit domain and range |
| **Annotation properties** | 14 | + `rice:evidenceType`, PROV-O, DCTERMS, SKOS, Schema.org, EPPO |
| **Named individuals** | **10,499** | 10,407 image individuals + 92 domain entities |
| **`owl:Axiom` (provenance)** | **320** | **100% of domain assertions reified with sources & evidenceType** |
| **`owl:Restriction` axioms** | 1 | Inside `SymptomaticObservation` defined class |
| **`AllDisjointClasses` axioms** | 2 | Disjointness among observation channels & entity types |
| **`skos:exactMatch` / `closeMatch`** | 24 / 8 | Mapped to AGROVOC concept URIs |
| **`TODO` literals remaining** | **0** | **100% resolved (dataset metadata & EPPO codes verified)** |
| **Properties with no declared domain/range** | 0 / 0 | 100% coverage |

---

### Per-class individual counts

The 10,499 individuals in the knowledge graph are categorized by domain layer:

| Domain Category | Class Name | Count | Type / Description |
|---|---|---:|---|
| **Observation Modality** | `ImageObservation` | 10,407 | Paddy Doctor field image instances |
| | `SensorObservation` | 0 | Scaffolding for multimodal sensor feeds |
| | `Observation` | 0 | Abstract root observation superclass |
| **Defined Class** | `SymptomaticObservation` | *(1,442)* | Defined class (`captures some Symptom`), populated via reasoner |
| **Dataset Metadata** | `Dataset` (`dcat:Dataset`) | 1 | `PaddyDoctorDataset` metadata individual |
| **Biotic Agents & Host** | `Pathogen` | 8 | Viral, bacterial, fungal, oomycete agents |
| | `Pest` | 8 | Insect pests and vector organisms |
| | `Disease` | 8 | Biotic disease diagnostic classes |
| | `HealthStatus` | 1 | `Normal_Health` (healthy reference baseline) |
| | `Plant` | 1 | `Rice` (*Oryza sativa*) host individual |
| **Phenotype & Environment** | `Symptom` | 28 | Visual symptoms (lesions, streaks, rotting, discoloration) |
| | `GrowthStage` | 7 | Rice phenological stages (Seedling, Tillering, Flowering, etc.) |
| | `EnvironmentalFactor` | 9 | Predisposing weather, canopy, and soil conditions |
| **Agronomic Management** | `Treatment` | 12 | Chemical, biological, genetic, and cultural practices |
| | `ManagementAction` | 5 | Operational actions (Immediate Intervention, Monitoring, etc.) |
| | `SeverityLevel` | 4 | Low, Medium, High, and Critical severity scales |
| **Total Named Individuals** | | **10,499** | *(10,407 images + 92 domain entities)* |

---

### Per-property assertion counts (populated only)

All domain assertions are formally backed by `owl:Axiom` provenance records (`dcterms:source` and `dcterms:bibliographicCitation`):

| Category | Property | Assertions | Domain → Range | Provenance Backing |
|---|---|---:|---|---|
| **Dataset & Observation Layer** | `annotatedAs` | 10,407 | `ImageObservation` → `Disease ⊔ Pest ⊔ HealthStatus` | Raw dataset labels |
| | `captures` | 1,442 | `ImageObservation` → `Symptom` | Visual evidence links |
| | `sourceDatasetLabel` | 10 | `Disease ⊔ Pest ⊔ HealthStatus` → `xsd:string` | Dataset vocabulary mapping |
| **Etiology & Susceptibility** | `vulnerableTo` | 60 | `Plant ⊔ GrowthStage` → `Disease ⊔ Pest ⊔ Pathogen` | IRRI RKB / CABI CPC |
| | `occursIn` | 47 | `Disease ⊔ Pest ⊔ HealthStatus` → `GrowthStage` | IRRI RKB / Ou (1985) |
| | `causes` | 10 | `Pathogen ⊔ Pest` → `Disease` | CABI / Ham / Hibino |
| **Symptomatology & Risk Factors**| `indicatedBy` | 42 | `Disease ⊔ Pest` → `Symptom` | IRRI Rice Doctor / CABI |
| | `increaseRiskOf` | 29 | `EnvironmentalFactor` → `Disease ⊔ Pest` | CABI CPC / IRRI RKB |
| **Control & Management** | `controlledBy` | 42 | `Disease ⊔ Pest` → `Treatment` | CABI / BBPOPT (2022) |
| | `recommends` | 23 | `Disease ⊔ Pest ⊔ SeverityLevel` → `ManagementAction` | BBPOPT / IRRI |
| | `preventedBy` | 8 | `Disease ⊔ Pest` → `Treatment` | IRRI RKB / CABI |
| | `requires` | 4 | `Treatment` → `GrowthStage` | BBPOPT / IRRI GAP |
| **Total Populated Triples** | | **12,124** | *(11,859 image/dataset + 265 direct domain relations)* | **100% domain triples reified** |

> *Note on inverse properties:* All twelve inverse directions (`indicates`, `detectedBy`, `causedBy`, `prevents`, `controls`, `threatens`, etc.) and `detects` are declared in the schema for reasoning/querying symmetry.

### Trajectory across major versions

| Version | Milestone Date | Triples | Named Classes | Object Props | Individuals | Domain Assertions |
|---|---|---|---|---|---|---|
| Initial commit | 2026-07-28 | — | — | — | — | — |
| v0.1 (early prototype) | ~2026-08-05 | — | 12 | 22 | 60 | ~30 |
| v0.2 (post-AGROVOC alignment) | 2026-08-17 | 52,806–52,816 | 17 | 24 | 10,467 | ~50 |
| v0.3 (post-provenance/EPPO/rename) | 2026-08-18 | 84,064 | 18 | 24 | 10,463 | ~80 |
| v0.4-expanded (superseded same day) | 2026-08-19 | 75,309 | 22 | 32 | 10,482 | ~90 |
| v0.4-minimal (post-cleanup baseline)| 2026-08-19 | 64,662 | 16 | 24 | 10,463 | 101 |
| **v0.4 (enriched & provenance)** | **2026-08-21** | **67,236** | **16** | **24** | **10,499** | **328 (320 with `owl:Axiom`, 0 TODOs)** |

The v0.4-expanded row is included for the record but was reverted the same
day — see §3 below. Early prototype commits that were originally labelled
with arbitrary 2.x tags (e.g. "v2.0"–"v2.3") were normalized to the `0.x`
pre-release series (`v0.1`–`v0.4`) to maintain a clean monotonic version
progression before the 1.0 publication release.

---

## 3. Changelog

### 2026-07-28 — 2026-08-06: initial schema and population (v0.1 prototype)

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

### 2026-08-17: cross-vocabulary alignment (v0.2)

- `ab3c1c5` **Add NCBI Taxonomy cross-check, multimodal fusion PoC, and an ontology backup**
- `25e9a7b` **Resolve four EnvironmentalFactor category mismatches via Planteome**

### 2026-08-18: v0.1 → v0.3 — provenance, EPPO, versioning normalization, cleanup

- `456d0c8` **Rice MMKG: rename classifiedAs, add provenance/EPPO/image links, restructure prototypes** — renamed `classifiedAs`→`annotatedAs`; added PROV-O provenance (`PaddyDoctorDataset`, `wasDerivedFrom`) to all 10,407 images; added `schema:contentUrl` image paths (the Paddy Doctor dataset was found locally, so paths were verified against real files rather than left as a template); added 3 verified EPPO codes; added ontology FAIR metadata; converted 4 prototype "class-as-instance" individuals into `owl:Restriction`s and deleted them; narrowed sensor property domains.
- `c78ca80` **Use v0.3 versioning for Rice MMKG since it has not been publicly released** — normalized legacy 2.x prototype labels to the `0.x` pre-release sequence (`v0.1` → `v0.2` → `v0.3`).
- `38e5d8e` **Stop importing full PROV-O/DCTERMS vocabularies, declare only used terms** — fixed `owl:imports` pulling the entire external DCTERMS/PROV-O class hierarchies into Protégé's view; switched to declaring only the ~7 terms actually used.
- `8e70498` **Fill in dcterms:license, creator, and issued metadata** — CC BY 4.0, ORCID, issue date.

### 2026-08-19: v0.4 expansion, built and then reverted the same day

- `6d12903` **Rice MMKG v0.4: three-layer schema restructuring** — expanded to 22 classes (`Agent`, `Dataset`, `AnnotationLabel`, `Infestation`, `Location`, `ObservationEvent`, `TextualReport`, etc.), 32 object properties, retargeted `Pest`→`Infestation` across 45 assertions, introduced `SymptomaticObservation` and `StemBorerCandidate` defined classes.
- `6ff9d51` **Fix StemBorerCandidate: use owl:hasValue instead of someValuesFrom** — corrected an invalid restriction (an individual filler in a class-position slot) that was causing `Stem_Borer_Damage` to be punned into the class hierarchy in Protégé.
- `8feba7e` **Remove StemBorerCandidate defined class** — removed per request; `SymptomaticObservation` kept.
- `e8ab8ec` **Rice MMKG v0.4-minimal: shrink schema to what the data actually supports** — reverted the expansion. Rebuilt from the true v0.3 baseline instead: deleted the four empty `Observation` subclasses and the orphan `prov:Entity` declaration (18→13 classes); kept `captures`/`detects` declared but unasserted; deleted the four unused sensor datatype properties (9→5); converted the 1,442 `Deadheart`-annotated images into `captures` evidence; added the single `SymptomaticObservation` defined class; wrote `deferred_design.md` recording what was deliberately not built and why.
- `a968b62` **Add SensorObservation as an Observation subclass, matching the conceptual schema** — empty on arrival (0 individuals), scaffolding for future sensor data, per a conceptual-schema diagram. Incidentally picked up a Protégé auto-save that dropped 4 `owl:Restriction` blank nodes orphaned by a bug in the v0.4-minimal Task 1.1 script, and removed `PaddyDoctorDataset`'s legacy `prov:Entity` type.
- `c37dcf8` **Rice MMKG cleanup: dataset typing, provenance/label redundancy, naming, detects range** — the largest single-commit triple-count drop in the project's history (85,459 → 64,662). `PaddyDoctorDataset` typed `dcat:Dataset` (was the last individual typed only `owl:NamedIndividual`); deleted 10,407 redundant `dcterms:source` triples on images (kept `prov:wasDerivedFrom`); deleted 10,407 redundant `sourceDatasetLabel` triples on images and gave the property a declared domain (was the only property in the ontology without one); renamed `LeafImage`→`ImageObservation` (10,407 individuals retyped); restored `AllDisjointClasses {ImageObservation, SensorObservation}`; narrowed `detects`' range to `Pest ⊔ Pathogen` (removing `Disease`, closing an evidence/conclusion conflation the `annotatedAs` rename had left open in the property's still-unused declaration). Three checkpoints emitted as CSVs/reports, none resolved: Paddy Doctor dataset metadata, `contentUrl` base URL, and two AGROVOC alignment defects plus 30 unaligned entities (regrouped from a stale worklog count).

### 2026-08-21: v0.4 domain graph enrichment and OWL axiom provenance (ESWC priorities #1 & #2)

- **Domain Graph Enrichment (101 → 328 assertions)**:
  - Addressed all 7 low-degree entities (`Hispa`, `Rice_Tungro_Disease`, `Downy_Mildew`, `Bacterial_Leaf_Streak`, `Bacterial_Panicle_Blight`, `Deadheart`, and `Normal_Health`).
  - Added 37 new named individuals: 5 pathogens (*Rice Tungro Bacilliform Virus*, *Rice Tungro Spherical Virus*, *Sclerophthora macrospora*, *Xanthomonas oryzae pv. oryzicola*, *Burkholderia glumae*), 2 pests (*Scirpophaga incertulas*, *Nephotettix virescens* as Tungro vector), 18 symptoms (*Panicle_Blast*, *Neck_Rot*, *White_Streak*, *Leaf_Scratching*, *Dead_Tiller*, *White_Ear*, *Yellow_Orange_Discoloration*, *Stunted_Growth*, etc.), 2 growth stages (*Tillering_Stage*, *Reproductive_Stage*), 4 environmental factors (*Dense_Canopy*, *Waterlogged_Soil*, *High_Night_Temperature*, *Presence_of_Leafhopper_Vector*), and 6 treatments/GAP.
  - Re-anchored class-level multimodal signal: non-zero feature pairs jumped from 2 to 34 (top prediction: `Brown_Spot` ↔ `Rice_Blast_Disease` at Jaccard 0.56).
- **OWL Axiom Provenance (100% domain assertions reified)**:
  - Added 320 `owl:Axiom` reifications carrying `dcterms:source`, `dcterms:bibliographicCitation`, and `rice:evidenceType "literature-curated"` across all domain relations (`causes`, `indicatedBy`, `occursIn`, `controlledBy`, `preventedBy`, `increaseRiskOf`, `vulnerableTo`, `recommends`, `requires`).
  - Grounded in IRRI Rice Doctor Knowledge Bank (2020), CABI Crop Protection Compendium (2022), EPPO Global Database, BBPOPT Kementan RI (2022), and seminal peer-reviewed literature (Ou 1985; Hibino 1996; Ham et al. 2011).
  - Replaced legacy ontology header disclaimer ("illustrative examples") with a certified statement of literature grounding.
  - Resolved all 9 remaining `TODO` literals: completed `PaddyDoctorDataset` metadata (`dcterms:title`, `dcterms:license`, `dcterms:source`, `dcterms:bibliographicCitation`) and verified 6 EPPO codes (`COCHMI`, `DCLPAR`, `SCPIIN`, `CNAPME`, `LEUCOM`, `LEPTOR`).
  - Set `owl:versionInfo "0.4"` and `owl:versionIRI <.../riceMMKG/0.4>`.
  - Overall triples: 64,662 → 64,990 (enrichment) → 66,909 (provenance) → **67,236** (with metadata polish).

---

## 4. Open items

- **AGROVOC:** 2 conflicting/suspicious matches (`Fungicide_Application`/
  `Insecticide_Application` sharing one concept IRI; `Rice_Blast_Disease`'s
  oddly-shaped identifier) + 30 unaligned domain individuals, grouped
  8 disease/pest · 9 symptom · 13 management/severity/stage. See
  `Worklog/RiceMMKG_cleanup_worklog/alignment_check.csv` and
  `agrovoc_todo.csv`.
- **Image URL resolvability:** `schema:contentUrl` holds relative paths
  that don't dereference. Three options written up, none chosen. See
  `Worklog/RiceMMKG_cleanup_worklog/contenturl_base.md`.
- **Permanent identifier:** `w3id.org` path segment to be registered for PURL minting.
- **Version status:** `0.4` is officially live in `Rice MMKG.rdf` (as of 2026-08-21).
- **Competency Questions (CQs) Benchmark:** Formalization as executable SPARQL queries (next development priority).
- **No reasoner available** in the working environment (no Java) — several
  acceptance checks across sessions (consistency, DL-classified defined-
  class membership) were substituted with direct graph queries, exact for
  the simple cases involved but not a general substitute.
