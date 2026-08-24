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
| **Total triples** | **66,873** | v0.5. Down 9 from v0.4's 66,882 — see §3, 2026-08-22 (v0.5 worklog) for the merge/retarget that caused the net decrease despite two new properties being added |
| **Named classes** | 16 | 13 primitive + 1 scaffolding + 1 `dcat:Dataset` + 1 defined class |
| **Object properties** | 26 | All declared with explicit domain and range; `transmits`/`transmittedBy` added in v0.5 |
| **Datatype properties** | 5 | All declared with explicit domain and range |
| **Annotation properties** | 14 | + `rice:evidenceType`, PROV-O, DCTERMS, SKOS, Schema.org, EPPO |
| **Named individuals** | **10,498** | 10,407 image individuals + 91 domain entities (`Scirpophaga_Incertulas` merged into `Stem_Borer` in v0.5) |
| **`owl:Axiom` (provenance)** | **265** | **100% of domain assertions reified with sources & evidenceType — 1:1, no duplicates, no orphans** |
| **`owl:Restriction` axioms** | 1 | Inside `SymptomaticObservation` defined class |
| **`AllDisjointClasses` axioms** | 2 | Disjointness among observation channels & entity types |
| **`skos:exactMatch` / `closeMatch` / `broadMatch`** | 33 / 17 / 1 | Mapped to AGROVOC / NCBI Taxonomy concept URIs, each verified against a live API response and cross-checked against the project's own alignment registers (see §3, 2026-08-22) |
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
| | `requires` | 5 | `Treatment` → `GrowthStage` | BBPOPT / IRRI GAP |
| **Total Populated Triples** | | **12,125** | *(11,859 image/dataset + 266 direct domain relations)* | **100% domain triples reified** |

> *Note on inverse properties:* All twelve inverse directions (`indicates`, `detectedBy`, `causedBy`, `prevents`, `controls`, `threatens`, etc.) and `detects` are declared in the schema for reasoning/querying symmetry.

### Trajectory across major versions

| Version | Milestone Date | Triples | Named Classes | Object Props | Individuals | Domain Assertions |
|---|---|---|---|---|---|---|
| v0.0 (initial commit) | 2026-07-28 | — | — | — | — | — |
| v0.1 (early prototype) | 2026-07-28 | — | 12 | 22 | 60 | ~30 |
| v0.2 (AGROVOC alignment) | 2026-08-06 | 52,806–52,816 | 17 | 24 | 10,467 | ~50 |
| v0.3 (EPPO/Planteome Enrichment) | 2026-08-13 | 84,064 | 18 | 24 | 10,463 | ~80 |
| v0.4 (domain enrichment + provenance) | 2026-08-20 | 66,882 | 16 | 24 | 10,499 | 329 |
| **v0.5 (verified-defect + modelling corrections)** | **2026-08-22** | **66,873** | **16** | **26** | **10,498** | **328** |

`v0.4-rc` is included for the record but was reverted the same day — see
§3 below. `v0.4.0`–`v0.4.4` are same-day intermediate states within the
`0.4` line (only `v0.4.0` and the final `v0.4.4` state were ever asserted
as `owl:versionInfo "0.4"` in the file itself — the `.1`–`.4` suffixes
here are this document's own bookkeeping for what changed same-day
between them, not a versioning scheme the ontology file uses). Early
prototype commits that were originally labelled with arbitrary 2.x tags
(e.g. "v2.0"–"v2.3") were normalized to the `0.x` pre-release series
(`v0.1`–`v0.5`) to maintain a clean monotonic version progression before
the 1.0 publication release.

---

## 3. Changelog

<!-- Newest first. -->

### 2026-08-22: v0.4 → v0.5, a six-task correction worklog

Full detail, all scripts, and the complete before/after data are in
`Worklog/RiceMMKG_v0.5_worklog/` (task spec, `reports/v0.5_summary.md`).
Summary here:

- **Fixed**: `Xanthomonas_Oryzicola`'s EPPO code (`XANTOX` → the correct
  `XANTTO`). `Stem_Borer`/`Scirpophaga_Incertulas` — a duplicated
  individual for the same organism, diverged in different directions —
  merged into `Stem_Borer`, carrying over its NCBITaxon alignment,
  redirecting its one non-duplicate incoming assertion, and dropping the
  `causes Deadheart` triple it was left with in favour of the correct
  `Stem_Borer indicatedBy Deadheart`.
- **Found beyond the task list, and fixed**: 9 more fabricated/
  hallucinated AGROVOC identifiers, asserted via an undeclared
  `rice:exactMatch` property (not `skos:exactMatch`) in the 2026-08-21
  "Provenance per Assertion" commit — none resolved to anything related
  to the individual they were on (one was "Tonga," another
  "rhizobitoxine," several 404s). This is the **second** time in this
  project's history that unverified external identifiers were asserted
  as if checked (the first was the same-day SKOS-alignment episode
  documented below) — every external identifier needs a live lookup
  before assertion, no exceptions.
- **Modelling fix**: `Nephotettix_Virescens causes Rice_Tungro_Disease`
  was wrong — a leafhopper vector doesn't *cause* tungro, it
  *transmits* the two viruses that do. New `rice:transmits`/
  `transmittedBy` properties (domain `Pest`, range `Pathogen`) replace
  it with two cited assertions (CABI 2022 + Hibino 1996, independently
  corroborated). `rice:causes` is now exclusively `Pathogen → Disease`
  across all 8 remaining assertions. No comparator ontology models
  vector-borne transmission explicitly — worth stating as a
  contribution in the paper, not just leaving in the file.
- **Prepared, not yet applied** (each needs a human decision the
  worklog deliberately didn't make): `alignment_refine.csv` (6 rows,
  whether 3 AGROVOC-IRI-sharing groups should get more precise
  `broadMatch` typing); a 250-image stratified sample plus a 28-term
  symptom vocabulary for expert annotation of `captures` (currently
  1,442 assertions, all pointing at one symptom); a w3id.org PURL
  registration package (namespace segment not yet chosen) and a tested
  `rewrite_namespace.py` that must not run until that's decided; Zenodo/
  AgroPortal submission drafts and a maintenance plan (two fields —
  institutional affiliation, release cadence — flagged as needing a
  human answer rather than guessed).
- **Actually run**: OOPS! and FOOPS! against a schema-only extract (the
  10,407 image instances excluded — both tools evaluate modelling
  pitfalls, not instance volume). OOPS!: 2 Minor pitfalls, nothing
  IMPORTANT/CRITICAL. FOOPS!: overall score **0.7275**, with one
  structural blocker (`PURL1`, no persistent URL — exactly what the w3id
  registration above would fix) accounting for most of the gap to
  gUFO's 92% comparator score. "After" measurement is correctly blocked
  on that same unresolved registration.
- **Net effect**: 266 → 265 domain assertions (one dropped as a
  duplicate during the merge, one retargeted from `causes` to
  `transmits` — both still land inside the 265, not a loss of coverage),
  provenance held at 100% through every intermediate step, not just
  checked at the end. `owl:versionInfo`/`versionIRI` bumped to `0.5`.

### 2026-08-22: reconciled against the AGROVOC/NCBI alignment registers

The 34 SKOS matches added earlier the same day (see the next entry below)
were added by an AI-assisted lookup pass working directly against live
AGROVOC/OLS4 API responses, without first checking this project's own
pre-existing alignment registers (`AGROVOC_alignment.md`,
`NCBI_Taxonomy_alignment.md`, both largely written 2026-08-03–08-17,
well before this session). Those registers had already reviewed several
of the same entities and explicitly recorded *why* a plausible-looking
candidate should not be used. Cross-checking the 34 against both
registers found **11 conflicts**, all reverted:

- `Armyworm` — the register already rejected this exact AGROVOC candidate
  (`fall armyworms` = *Spodoptera frugiperda*, a maize pest, not a rice
  one — a false-positive risk, not a match).
- `Bacterial_Leaf_Blight`, `Bacterial_Leaf_Streak`, `Brown_Spot`,
  `Sheath_Blight` — each substitutes the *pathogen's* AGROVOC concept for
  a *disease* individual, exactly the conflation the register's mapping
  policy forbids ("Do not substitute the pathogen ...; disease and
  pathogen are distinct entities"). `Brown_Spot`'s candidate concept
  (`Cochliobolus miyabeanus`, c_34512) and `Bacterial_Leaf_Streak`'s
  (`Xanthomonas oryzae pv. oryzicola`, c_330601) are also each already
  correctly assigned to their respective `Pathogen` individual
  (`Bipolaris_Oryzae`, `Xanthomonas_Oryzicola`) — reusing them for the
  disease would have made two differently-typed local entities point to
  the same external concept.
- `Panicle_Blast` — same conflation, but Symptom-vs-Disease: its
  candidate concept (`rice blast disease`, c_152ac092) is already
  assigned to `Rice_Blast_Disease`.
- `Brown_Lesion`, `Maturity_Stage`, `Resistant_Variety` — each already
  marked "Needs domain review" in the register for a specific unresolved
  reason (generic-vs-specific scope; no confirmed synonymy; trait-vs-
  practice category mismatch) that the new pass did not actually resolve.
- `Excessive_Nitrogen` — the register already recorded "no candidate
  found" for this exact entity after a dedicated search round.
- `Rice_Bug` — both registers already leave this open pending an
  unresolved species-vs-genus scope question and an AGROVOC/NCBI spelling
  discrepancy (`oratorius` vs. `oratoria`); the new pass applied
  `exactMatch` without resolving either.

The remaining **23 of 34** were genuinely new — mostly organisms and
domain entities added in the 2026-08-21 enrichment that predate every
existing register — and have been written up properly in
`AGROVOC_alignment.md` (round 5) and `NCBI_Taxonomy_alignment.md`
(round 2), including decision-log entries, following this project's
established format. `skos:exactMatch`: 19 → 32. `skos:closeMatch`: 8 → 18.
Total triples: 66,893 → 66,882.

**Process note for future sessions:** before adding any AGROVOC/NCBI/
Planteome alignment, check the three registers in `Analysis and
Alignment/` (now `Ontology/`) first — they hold prior review decisions,
including explicit rejections, that a fresh API lookup will not
reproduce on its own.

### 2026-08-22: Harvest_Stage assertion and verified SKOS alignments

Checking for remaining bare individuals found two gaps beyond the axiom
scoping fix in the entry below:

- **`Harvest_Stage`** (`GrowthStage`) had zero property assertions of any
  kind — a leftover from the growth-stage schema that was never populated.
  Added `Crop_Sanitation rice:requires Harvest_Stage`, reified with the
  same BBPOPT (2022) citation already backing `Crop_Sanitation`'s
  `rdfs:comment` ("removal and destruction of infected plant debris to
  reduce inoculum carry-over between seasons"). Domain-relation count:
  265 → 266.
- **66 of 91 domain individuals** (mostly the pathogens, pests, symptoms,
  and environmental factors added in the 2026-08-21 enrichment) had no
  `skos:exactMatch`/`closeMatch` alignment at all. Each was checked
  against AGROVOC (REST search), NCBI Taxonomy (via OLS4), and PECO (via
  OLS4) with a live API call per candidate — no URI was accepted without
  seeing the vocabulary's own returned label. 34 got a confident match:
  8 `NCBITaxon` exactMatch for pathogen/pest binomials, 8 AGROVOC
  exactMatch, 18 AGROVOC closeMatch. 32 were deliberately left
  unaligned — mostly specific colloquial symptom phrasing (dead heart,
  hopperburn, whitehead, leaf tip, streak/stripe symptoms), severity
  levels, and generic management actions with no equivalent concept in
  any of the three vocabularies. Full per-individual record, including
  the exact query and returned label used to justify or reject each
  candidate, is in
  `Worklog/RiceMMKG_provenance_fix_worklog/agrovoc_alignment_verified.csv`.
  `skos:exactMatch`: 19 → 35. `skos:closeMatch`: 8 → 26.

  *(These counts were revised downward the same day — see the "reconciled
  against the AGROVOC/NCBI alignment registers" entry above, which comes
  later in time despite sitting above this one in this newest-first list.)*

### 2026-08-22: provenance scope fix

Verification of the 2026-08-21 provenance enrichment found that the
reification pass had not been scoped to the 9 intended domain relations —
it also reified all 28 `rdfs:subPropertyOf` schema declarations and all
27 `skos:exactMatch`/`closeMatch` AGROVOC/PECO/NCBITaxon alignment triples,
attaching the same agronomy-literature citations (e.g. "IRRI (2020) Rice
Doctor Fact Sheets") to axioms like `causes rdfs:subPropertyOf
owl:topObjectProperty` — a citation that makes no sense for a property-
hierarchy declaration or a vocabulary alignment. Removed all 55 spurious
`owl:Axiom` reifications (385 triples: the axiom node plus its
`owl:annotatedSource/Property/Target`, `dcterms:source`,
`dcterms:bibliographicCitation`, `rice:evidenceType`). The underlying
`rdfs:subPropertyOf` and `skos:exactMatch`/`closeMatch` triples themselves
are untouched — only their incorrect literature-citation annotations were
removed. `owl:Axiom` count: 320 → 265, now exactly 1:1 with the 265 domain
assertions, verified with no duplicates and no orphans. Triples: 67,236 →
66,851.

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

### 2026-08-19: v0.4 expansion, built and then reverted the same day

- `6d12903` **Rice MMKG v0.4: three-layer schema restructuring** — expanded to 22 classes (`Agent`, `Dataset`, `AnnotationLabel`, `Infestation`, `Location`, `ObservationEvent`, `TextualReport`, etc.), 32 object properties, retargeted `Pest`→`Infestation` across 45 assertions, introduced `SymptomaticObservation` and `StemBorerCandidate` defined classes.
- `6ff9d51` **Fix StemBorerCandidate: use owl:hasValue instead of someValuesFrom** — corrected an invalid restriction (an individual filler in a class-position slot) that was causing `Stem_Borer_Damage` to be punned into the class hierarchy in Protégé.
- `8feba7e` **Remove StemBorerCandidate defined class** — removed per request; `SymptomaticObservation` kept.
- `e8ab8ec` **Rice MMKG v0.4-minimal: shrink schema to what the data actually supports** — reverted the expansion. Rebuilt from the true v0.3 baseline instead: deleted the four empty `Observation` subclasses and the orphan `prov:Entity` declaration (18→13 classes); kept `captures`/`detects` declared but unasserted; deleted the four unused sensor datatype properties (9→5); converted the 1,442 `Deadheart`-annotated images into `captures` evidence; added the single `SymptomaticObservation` defined class; wrote `deferred_design.md` recording what was deliberately not built and why.
- `a968b62` **Add SensorObservation as an Observation subclass, matching the conceptual schema** — empty on arrival (0 individuals), scaffolding for future sensor data, per a conceptual-schema diagram. Incidentally picked up a Protégé auto-save that dropped 4 `owl:Restriction` blank nodes orphaned by a bug in the v0.4-minimal Task 1.1 script, and removed `PaddyDoctorDataset`'s legacy `prov:Entity` type.
- `c37dcf8` **Rice MMKG cleanup: dataset typing, provenance/label redundancy, naming, detects range** — the largest single-commit triple-count drop in the project's history (85,459 → 64,662). `PaddyDoctorDataset` typed `dcat:Dataset` (was the last individual typed only `owl:NamedIndividual`); deleted 10,407 redundant `dcterms:source` triples on images (kept `prov:wasDerivedFrom`); deleted 10,407 redundant `sourceDatasetLabel` triples on images and gave the property a declared domain (was the only property in the ontology without one); renamed `LeafImage`→`ImageObservation` (10,407 individuals retyped); restored `AllDisjointClasses {ImageObservation, SensorObservation}`; narrowed `detects`' range to `Pest ⊔ Pathogen` (removing `Disease`, closing an evidence/conclusion conflation the `annotatedAs` rename had left open in the property's still-unused declaration). Three checkpoints emitted as CSVs/reports, none resolved: Paddy Doctor dataset metadata, `contentUrl` base URL, and two AGROVOC alignment defects plus 30 unaligned entities (regrouped from a stale worklog count).

### 2026-08-18: v0.1 → v0.3 — provenance, EPPO, versioning normalization, cleanup

- `456d0c8` **Rice MMKG: rename classifiedAs, add provenance/EPPO/image links, restructure prototypes** — renamed `classifiedAs`→`annotatedAs`; added PROV-O provenance (`PaddyDoctorDataset`, `wasDerivedFrom`) to all 10,407 images; added `schema:contentUrl` image paths (the Paddy Doctor dataset was found locally, so paths were verified against real files rather than left as a template); added 3 verified EPPO codes; added ontology FAIR metadata; converted 4 prototype "class-as-instance" individuals into `owl:Restriction`s and deleted them; narrowed sensor property domains.
- `c78ca80` **Use v0.3 versioning for Rice MMKG since it has not been publicly released** — normalized legacy 2.x prototype labels to the `0.x` pre-release sequence (`v0.1` → `v0.2` → `v0.3`).
- `38e5d8e` **Stop importing full PROV-O/DCTERMS vocabularies, declare only used terms** — fixed `owl:imports` pulling the entire external DCTERMS/PROV-O class hierarchies into Protégé's view; switched to declaring only the ~7 terms actually used.
- `8e70498` **Fill in dcterms:license, creator, and issued metadata** — CC BY 4.0, ORCID, issue date.

### 2026-08-17: cross-vocabulary alignment (v0.2)

- `ab3c1c5` **Add NCBI Taxonomy cross-check, multimodal fusion PoC, and an ontology backup**
- `25e9a7b` **Resolve four EnvironmentalFactor category mismatches via Planteome**

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

---

## 4. Open items

- **AGROVOC:** 2 conflicting/suspicious matches (`Fungicide_Application`/
  `Insecticide_Application` sharing one concept IRI; `Rice_Blast_Disease`'s
  oddly-shaped identifier) — still unresolved, predates the 2026-08-22
  alignment round. See `Worklog/RiceMMKG_cleanup_worklog/alignment_check.csv`.
  43 domain individuals remain without any SKOS alignment after the
  2026-08-22 verification pass — 32 with no matching concept found in
  AGROVOC/NCBITaxon/PECO after multiple query variants, plus 11 where a
  candidate exists but was reverted for conflicting with this project's
  own alignment registers (disease-vs-pathogen conflation, category
  mismatches, or an already-open "needs domain review" item — see
  `AGROVOC_alignment.md` round 5 and `NCBI_Taxonomy_alignment.md` round 2
  for the reasoning on each). Full record in
  `Worklog/RiceMMKG_provenance_fix_worklog/agrovoc_alignment_verified.csv`.
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
