# Rice MMKG — description, statistics, and changelog

Status snapshot as of **2026-09-15** (Rice MMKG `0.7.0-dev`, in development
after the `v0.6.2` release).
Covers `Ontology/Rice MMKG.rdf` from its first commit through the current
state. Numbers below were re-measured with rdflib on 2026-09-15. The v0.6
figures this document first carried (66,874 triples, 265 axioms) had been
measured before the same-day inconsistency fix and did not describe the
released file; see the v0.6.1 changelog entry.

---

## 1. Description

Rice MMKG is an OWL 2 knowledge graph for rice disease and pest diagnosis,
built around the [Paddy Doctor](https://www.kaggle.com/competitions/paddy-disease-classification)
image dataset. It links rice diseases, pests, pathogens, symptoms,
environmental factors, growth stages, treatments, and management actions,
and keeps two things deliberately separate:

- **Raw dataset annotation** (`rice:annotatedAs`) — what the Paddy Doctor
  label folder says an image is, asserted on all 10,407 image individuals.
- **Domain-knowledge evidence** (`rice:captures` → `rice:indicates`) — a
  narrower, independently-populated chain from observed symptom to
  diagnosed condition. In v0.6, `Deadheart` is disambiguated as a `Disease`
  (damage syndrome caused by yellow stem borer *Scirpophaga incertulas*),
  while the 1,442 dead-heart images capture the `Dead_Tiller` symptom
  (`rice:captures rice:Dead_Tiller`, which has rdfs:label "dead heart"@en and
  is typed `Symptom`). This cleanly satisfies the `SymptomaticObservation`
  defined class while eliminating class disjointness collisions with `Disease`.

**Namespace:** `https://w3id.org/ricemmkg#` (prefix `rice:`) — a w3id.org permanent identifier, registered
on 2026-09-16 (perma-id/w3id.org#6697) and used since 0.7.0-dev. Releases up to v0.6.2
used `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#`; their version IRIs `https://w3id.org/ricemmkg/0.6.1` and `/0.6.2` resolve to those files.

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

**License:** CC BY 4.0. **Creator:** Muhammad Ariful Furqon (ORCID 0000-0002-1031-3567), Natthawut Kertkeidkachorn (ORCID 0000-0003-4527-776X). **Version:** `0.7.0-dev` (in development since 2026-09-15; last release `0.6.2`; pre-release progression: `v0.1` → `v0.2` → `v0.3` → `v0.4` → `v0.5` → `v0.6` → `v0.6.1` → `v0.6.2`; git tags `elicited-baseline-v0.6`, `v0.6.1`, `v0.6.2`).

---

## 2. Statistics (current state)

| Quantity | Value | Notes |
|---|---|---|
| **Total triples** | **67,861** (asserted) / **163,297** (OWL RL) | 0.7.0-dev. +95,436 triples derived via OWL RL materialisation. v0.6.1/v0.6.2: 66,802 / 161,447; released v0.6: 66,780 / 161,416 |
| **Named classes** | 21 | 18 primitive (incl. `PlantPart`, `TransmissionMode`, `ManagementCategory`, `AbioticFactor` and `Variety`, 0.7.0-dev) + 1 scaffolding + 1 `dcat:Dataset` + 1 defined class (`SymptomaticObservation`) |
| **Object properties** | 35 | All declared with explicit domain and range, and every inverse pair checked for matching domain/range; includes `affectsPlantPart`, transitive `partOf`, `hasTransmissionMode`, `hasManagementCategory`, and `varietyOf`/`hasVariety`, `resistantTo`/`resistedBy`, `moderatelyResistantTo` (0.7.0-dev) |
| **Datatype properties** | 5 | All declared with explicit domain and range |
| **Annotation properties** | 14 | Includes `rice:evidenceType`, PROV-O, DCTERMS, SKOS, Schema.org, EPPO |
| **Named individuals** | **10,541** | 10,407 image individuals + 1 dataset metadata + 133 domain entities (10 `PlantPart`, 1 `TransmissionMode`, 4 `ManagementCategory`, 6 `AbioticFactor`, 3 `Variety`) |
| **`owl:Axiom` (provenance)** | **353** | **353 domain assertions, all reified with sources & evidenceType — 1:1, no duplicates, no orphans** (0.7.0-dev). v0.6.1/v0.6.2: 256; released v0.6: 253 axioms over 255 assertions |
| **`owl:Restriction` axioms** | 1 | Inside `SymptomaticObservation` defined class |
| **`AllDisjointClasses` axioms** | 2 | Disjointness among observation channels & core domain categories (17 classes; `PlantPart`, `TransmissionMode`, `ManagementCategory`, `AbioticFactor` and `Variety` added in 0.7.0-dev) |
| **Reasoner Consistency** | **Consistent** | 0.7.0-dev checked in **HermiT** on 2026-09-15 with `-k` on a space-free copy, with injected-contradiction controls (`Rice` as Plant + Disease; `Leaf_Blade` as PlantPart + Disease; `Semi_Persistent` as TransmissionMode + Disease; `Chemical_Control_Category` as ManagementCategory + Disease; `Zinc_Deficiency` as AbioticFactor + Pathogen; `Salinity` as AbioticFactor + Pathogen; `IR64` as Variety + Disease) that all report inconsistent; v0.6 verified in HermiT & Pellet |
| **Competency Questions (CQ)** | **21 PASS / 2 PARTIAL / 1 FAIL / 1 DOC** | **87.5% pass rate** across 24 scored CQs (25 total). CQ-13 FAIL: the unsourced severity → action triage was removed. CQ-12 PARTIAL: six abiotic disorders entered its denominator. CQ-01 denominator corrected to exclude abiotic disorders (7/9; uncorrected 7/15). v0.6.1/v0.6.2: 23 / 1 / 0 / 1; released v0.6: 21 / 1 / 2 / 1 |
| **`skos:exactMatch` / `closeMatch` / `broadMatch`** | 42 / 23 / 1 | Mapped to AGROVOC / NCBI Taxonomy / Planteome (PECO, PO) and BFO, verified against live APIs |
| **`TODO` literals remaining** | **0** | **100% resolved (dataset metadata & EPPO codes verified)** |
| **Properties with no declared domain/range** | 0 / 0 | 100% coverage |

---

### Per-class individual counts

The 10,531 individuals in the knowledge graph are categorized by domain layer:

| Domain Category | Class Name | Count | Type / Description |
|---|---|---:|---|
| **Observation Modality** | `ImageObservation` | 10,407 | Paddy Doctor field image instances |
| | `SensorObservation` | 0 | Scaffolding for multimodal sensor feeds |
| | `Observation` | 0 | Abstract root observation superclass |
| **Defined Class** | `SymptomaticObservation` | *(1,442)* | Defined class (`captures some Symptom`), populated via OWL reasoning |
| **Dataset Metadata** | `Dataset` (`dcat:Dataset`) | 1 | `PaddyDoctorDataset` metadata individual |
| **Biotic Agents & Host** | `Pathogen` | 8 | Viral, bacterial, fungal, oomycete agents |
| | `Pest` | 7 | Insect pests and vector organisms (`Scirpophaga_Incertulas` merged into `Stem_Borer`) |
| | `TransmissionMode` | 1 | `Semi_Persistent` (vector transmission mode of both tungro viruses); 0.7.0-dev |
| | `Disease` | 15 | Biotic disease & damage condition classes (including `Deadheart`), plus 4 nutrient-deficiency disorders and the iron toxicity and salinity disorders (0.7.0-dev) |
| | `AbioticFactor` | 6 | Nitrogen, phosphorus, potassium and zinc deficiency; iron toxicity; salinity — abiotic causes of the six disorders; 0.7.0-dev |
| | `Variety` | 3 | Rice cultivars: `IR64` and the Indonesian varieties `Angke` and `Conde` bred from it; 0.7.0-dev |
| | `HealthStatus` | 1 | `Normal_Health` (healthy reference baseline) |
| | `Plant` | 1 | `Rice` (*Oryza sativa*) host individual |
| **Phenotype & Environment** | `Symptom` | 39 | Visual symptoms (lesions, streaks, rotting, discoloration, dead tiller); 9 added in 0.7.0-dev for nutrient deficiencies, 3 for iron toxicity and salinity |
| | `PlantPart` | 10 | Organs on which symptoms appear (Whole_Plant, Tiller, Leaf, Leaf_Blade, Leaf_Sheath, Panicle, Panicle_Neck, Grain, Root, Stem); 0.7.0-dev |
| | `GrowthStage` | 7 | Rice phenological stages (Seedling, Tillering, Flowering, etc.) |
| | `EnvironmentalFactor` | 9 | Predisposing weather, canopy, and soil conditions |
| **Agronomic Management** | `Treatment` | 13 | Chemical, biological, genetic, and cultural practices; `Zinc_Fertilizer_Application` added in 0.7.0-dev |
| | `ManagementAction` | 5 | Operational actions (Immediate Intervention, Monitoring, etc.) |
| | `ManagementCategory` | 4 | Control-method categories from AGROVOC: chemical, biological, cultural, host plant resistance; 0.7.0-dev |
| | `SeverityLevel` | 4 | Low, Medium, High, and Critical; each annotated with the matching attack-intensity category (ringan, sedang, berat, puso) of the 2021 Indonesian pest-observation juknis. No severity → action mapping since 0.7.0-dev |
| **Total Named Individuals** | | **10,541** | *(10,407 images + 1 dataset + 133 domain entities)* |

---

### Per-property assertion counts (populated only)

All domain assertions are formally backed by `owl:Axiom` provenance records (`dcterms:source` and `dcterms:bibliographicCitation`):

| Category | Property | Assertions | Domain → Range | Provenance Backing |
|---|---|---:|---|---|
| **Dataset & Observation Layer** | `annotatedAs` | 10,407 | `ImageObservation` → `Disease ⊔ Pest ⊔ HealthStatus` | Raw dataset labels |
| | `captures` | 1,442 | `ImageObservation` → `Symptom` | Visual evidence links |
| | `sourceDatasetLabel` | 10 | `Disease ⊔ Pest ⊔ HealthStatus` → `xsd:string` | Dataset vocabulary mapping |
| **Etiology & Susceptibility** | `vulnerableTo` | 57 | `Plant ⊔ GrowthStage ⊔ Variety` → `Disease ⊔ Pest` | CABI CPC (55); Mackill & Khush (2018) for IR64 (2, 0.7.0-dev) |
| | `occursIn` | 41 | `Disease ⊔ Pest ⊔ HealthStatus` → `GrowthStage` | IRRI RKB / Ou (1985) |
| | `causes` | 14 | `Pathogen ⊔ AbioticFactor` → `Disease` | CABI / Ham / Hibino; IRRI nutrient and toxicity fact sheets (6, 0.7.0-dev) |
| | `transmits` | 2 | `Pest` → `Pathogen` | CABI / Hibino (1996) |
| | `hasTransmissionMode` | 2 | `Pathogen` → `TransmissionMode` | Wang et al. (2022); 0.7.0-dev |
| **Symptomatology & Risk Factors**| `indicatedBy` | 70 | `Disease ⊔ Pest` → `Symptom` | IRRI Rice Doctor / CABI / IRAC (2025); IRRI nutrient fact sheets (19) and toxicity fact sheets (8), 0.7.0-dev |
| | `increaseRiskOf` | 34 | `EnvironmentalFactor` → `Disease ⊔ Pest` | CABI CPC (29) / IRRI RKB (5) |
| **Plant Anatomy** | `affectsPlantPart` | 39 | `Symptom` → `PlantPart` | IRRI Rice Knowledge Bank fact sheets (13 pest/disease + 4 nutrient + 3 toxicity) |
| | `partOf` | 2 | `PlantPart` → `PlantPart` | Plant Ontology via EBI OLS4 (`ontology-derived`) |
| **Control & Management** | `controlledBy` | 44 | `Disease ⊔ Pest` → `Treatment` | CABI (41) / Gallagher et al. (2002, FAO) (1); IRRI zinc fact sheet (2) |
| | `recommends` | 17 | `Disease ⊔ Pest ⊔ SeverityLevel` → `ManagementAction` | CABI; the 6 severity → action assertions were removed in 0.7.0-dev (unsourced) |
| | `preventedBy` | 10 | `Disease ⊔ Pest` → `Treatment` | CABI (8); IRRI toxicity fact sheets (2, 0.7.0-dev) |
| | `requires` | 5 | `Treatment` → `GrowthStage` | IRRI RKB (`Crop_Sanitation requires Harvest_Stage` re-sourced from BBPOPT to the IRRI tungro sheet in 0.7.0-dev) |
| | `hasManagementCategory` | 6 | `Treatment` → `ManagementCategory` | IRRI RKB (2) / AGROVOC definitions (4, `ontology-derived`); 0.7.0-dev |
| **Variety** | `varietyOf` | 3 | `Variety` → `Plant` | Mackill & Khush (2018); 0.7.0-dev |
| | `resistantTo` | 5 | `Variety` → `Disease ⊔ Pest` | Mackill & Khush (2018); 0.7.0-dev |
| | `moderatelyResistantTo` | 2 | `Variety` → `Disease ⊔ Pest` | Mackill & Khush (2018); sub-property of `resistantTo`; 0.7.0-dev |
| **Total domain assertions** | | **353** | *(0.7.0-dev, measured 2026-09-16 with rdflib; plus 10,407 `annotatedAs`, 1,442 `captures`, 10 `sourceDatasetLabel`, 15 `eppoCode`)* | **353 / 353 reified** |

> *Note on inverse properties:* All twelve inverse directions (`indicates`, `detectedBy`, `causedBy`, `prevents`, `controls`, `threatens`, etc.) and `detects` are declared in the schema for reasoning/querying symmetry.

### Trajectory across major versions

| Version | Milestone Date | Triples | Named Classes | Object Props | Individuals | Domain Assertions |
|---|---|---|---|---|---|---|
| v0.0 (initial commit) | 2026-07-28 | — | — | — | — | — |
| v0.1 (early prototype) | 2026-07-28 | — | 12 | 22 | 60 | ~30 |
| v0.2 (AGROVOC alignment) | 2026-08-06 | 52,806–52,816 | 17 | 24 | 10,467 | ~50 |
| v0.3 (EPPO/Planteome Enrichment) | 2026-08-13 | 84,064 | 18 | 24 | 10,463 | ~80 |
| v0.4 (domain enrichment + provenance) | 2026-08-20 | 66,882 | 16 | 24 | 10,499 | 329 |
| v0.5 (vector transmission + benchmark design) | 2026-08-25 | 66,873 | 16 | 26 | 10,498 | 265 axioms |
| v0.6 (Deadheart disambiguation, DL consistency, 25 CQs) | 2026-09-03 | 66,780 (161,416 OWL RL) | 16 | 26 | 10,498 | 253 axioms / 255 assertions |
| v0.6.1 (provenance gaps closed, CQ-10/CQ-24 fixed) | 2026-09-14 | 66,802 (161,447 OWL RL) | 16 | 26 | 10,498 | 256 axioms / 256 assertions |
| v0.6.2 (CABI DOIs, Crossref citations) | 2026-09-15 | 66,802 (161,447 OWL RL) | 16 | 26 | 10,498 | 256 axioms / 256 assertions |
| 0.7.0-dev (PlantPart) | 2026-09-15 | 67,090 (161,861 OWL RL) | 17 | 28 | 10,506 | 285 axioms / 285 assertions |
| 0.7.0-dev (+ TransmissionMode) | 2026-09-15 | 67,120 (161,916 OWL RL) | 18 | 29 | 10,507 | 287 axioms / 287 assertions |
| 0.7.0-dev (+ ManagementCategory, label/mapping fixes) | 2026-09-15 | 67,200 (162,043 OWL RL) | 19 | 30 | 10,511 | 293 axioms / 293 assertions |
| 0.7.0-dev (+ AbioticFactor, literal hygiene) | 2026-09-15 | 67,588 (162,775 OWL RL) | 20 | 30 | 10,531 | 330 axioms / 330 assertions |
| 0.7.0-dev (BBPOPT source resolved, + iron toxicity, salinity) | 2026-09-15 | 67,708 (163,011 OWL RL) | 20 | 30 | 10,538 | 341 axioms / 341 assertions |
| 0.7.0-dev (+ `Variety`: IR64, Angke, Conde) | 2026-09-16 | 67,859 (163,293 OWL RL) | 21 | 35 | 10,541 | 353 axioms / 353 assertions |
| **0.7.0-dev (w3id namespace — in development)** | **2026-09-17** | **67,861** (163,297 OWL RL) | **21** | **35** | **10,541** | **353 axioms / 353 assertions** |

---

## 3. Changelog

<!-- Newest first. -->

### 2026-09-17: 0.7.0-dev — language tags on labels and comments; two stale labels removed

Pre-patch file: `Backup/Rice MMKG.backup-0.7.0-dev-pre-langtags.rdf`.

- **Tagged `@en`:** 45 literals that had no language tag — 29 `rdfs:comment` and 7 `rdfs:label` on `rice:` terms, and 9 `rdfs:label` on imported vocabulary terms declared in the file (`dcterms:source`, `dcat:Dataset`, `prov:wasDerivedFrom`, …). Every `rdfs:label` and `rdfs:comment` in the file now carries `@en`.
- **Removed:** `rdfs:label "classified as"@en` on `annotatedAs` and `"classifies"@en` on `annotationOf`. They were left over from the property's former name `classifiedAs` (renamed in v2.3), so each property carried two labels, one naming the old property. `"annotated as"@en` and `"annotation of"@en` remain.
- **Left untagged on purpose:** the two `skos:altLabel` scientific names (`Scirpophaga incertulas` on `Stem_Borer`, `Pyricularia oryzae` on `Magnaporthe_Oryzae`); a Latin binomial belongs to no single language.
- **CQ-24 unchanged.** Its question names `rice:evidenceType` only, so it was neither extended nor re-scored; it still passes (0 violations).
- **Checks:** 67,861 asserted triples (−2, the removed labels) / 163,297 OWL RL; all other structural checks pass (353 axioms = 353 assertions, 15 inverse pairs matched, no domain/range violation); HermiT consistent, control inconsistent. Both CQ instruments give identical answers (21 PASS / 2 PARTIAL / 1 FAIL / 1 DOC; 9 / 8 / 2).

### 2026-09-17: 0.7.0-dev — `Stem_Rot_Symptom` renamed `Leaf_Sheath_Lesion`

Pre-rename file: `Backup/Rice MMKG.backup-0.7.0-dev-pre-rename.rdf`.

- **Why now:** the individual was relabelled "leaf sheath lesion" on 2026-09-15, because stem rot is a different disease, but its IRI kept the old name pending a deprecation policy. The namespace rewrite had just replaced every IRI, and nothing had been published under `https://w3id.org/ricemmkg#` yet, so no one can hold a reference to `https://w3id.org/ricemmkg#Stem_Rot_Symptom`: the IRI was renamed outright, with no `owl:deprecated` stub. Releases up to v0.6.2 keep the old name in the old namespace.
- **Changed:** 4 IRI occurrences — the individual, `Sheath_Blight indicatedBy` it, and the two axioms that reify its assertions (that one and its `affectsPlantPart`); the individual's comment now records the former IRI; the AGROVOC register rows; the Open item is closed.
- **Checks:** triple counts unchanged (67,863 / 163,301); no IRI named `Stem_Rot_Symptom` left; all structural checks and HermiT as for the namespace rewrite. Both CQ instruments give identical answers once the old name is mapped to the new one — the name appears only in CQ-18's list of symptoms without a grounded image.

### 2026-09-17: 0.7.0-dev — namespace moved to `https://w3id.org/ricemmkg#`

The w3id.org registration (perma-id/w3id.org#6697) was merged on 2026-09-16 and its redirects were checked with `curl` on 2026-09-17, so the namespace was rewritten, as a commit of its own. Pre-rewrite file: `Backup/Rice MMKG.backup-0.7.0-dev-pre-namespace.rdf`.

- **Rewritten:** every term IRI `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#X` → `https://w3id.org/ricemmkg#X` (44,959 occurrences); the ontology IRI → `https://w3id.org/ricemmkg`; `owl:versionIRI` → `https://w3id.org/ricemmkg/0.7.0`, the IRI the release will carry, which resolves once tag `v0.7.0` exists (`…/0.7.0-dev` would never resolve: the redirect rule accepts numeric versions only). `owl:versionInfo` stays `0.7.0-dev`.
- **Added:** `owl:priorVersion <https://w3id.org/ricemmkg/0.6.2>`, which already resolves; `vann:preferredNamespaceUri`, declared as an annotation property; one sentence in the header comment that names the old namespace — now its only occurrence in the file.
- **Method:** text substitution with the expected count of every target checked before writing — not a load-and-re-serialise — so the diff touches only lines that carry an IRI, and the two CRLF documents kept their line endings.
- **Also updated:** `RICE_NS` in both CQ scripts; the SPARQL/Turtle prefix lines in five documents; the namespace descriptions in `README.md`, `MAINTENANCE.md` and this file; the ESWC plan.
- **Not rewritten:** `Backup/` (historical snapshots), `patch_assertions.rdf` (a rejected draft), and the gitignored `Worklog/` — its annotation-sample scripts need the new namespace when the image annotation is run.
- **Checks:** 67,863 asserted triples (+4, all in the header: `owl:priorVersion`, `vann:preferredNamespaceUri`, and the property's two-triple declaration) / 163,301 OWL RL; no IRI left in the old namespace; 353 axioms = 353 domain assertions, none unreified, orphaned, duplicated or incomplete; 15 inverse pairs with matching domain and range; 0 domain/range violations; 0 individuals in two disjoint core classes. HermiT consistent, `-U` lists only `owl:Nothing`, control (`IR64` as Variety + Disease) inconsistent.
- **Answers unchanged:** both CQ instruments were compared field by field with the committed results — identical, apart from timings and the order of truncated row samples. Benchmark **21 PASS / 2 PARTIAL / 1 FAIL / 1 DOC**; elicited 9 / 8 / 2.
- **Redirect limitations** carried to Open items: GitHub raw serves the file as `text/plain`, and the root IRI resolves to the development file on `main`.

### 2026-09-16: 0.7.0-dev — `Variety`: IR64 and two Indonesian varieties bred from it

Answers the domain expert's variety point (2026-09-14: treatment differs per variety; "cek varietas IR64") for the part literature can settle. Pre-patch file: `Backup/Rice MMKG.backup-0.7.0-dev-pre-variety.rdf`.

- **Source:** Mackill, D.J. & Khush, G.S. (2018). *IR64: a high-quality and high-yielding mega variety*. Rice, 11, 18 — open access, DOI checked live, full text read on 2026-09-16; a review by one of IR64's own breeders. The official Indonesian variety descriptions (*Deskripsi Varietas Unggul Baru Padi*) were the first choice, but `repository.pertanian.go.id` returns 403 to automated clients and `bbpadi.litbang.pertanian.go.id` does not resolve — see Open items for round 2.
- **Class `Variety`** with `IR64`, `Angke` and `Conde`, each `varietyOf` `Rice`. `Variety` joined the core `AllDisjointClasses` axiom (now 17 classes).
- **Properties (5):** `varietyOf`/`hasVariety`, `resistantTo`/`resistedBy`, and `moderatelyResistantTo` as a sub-property of `resistantTo`, so a query for resistance also returns the moderate grades. `vulnerableTo` records the opposite direction, its domain widened to `Plant ⊔ GrowthStage ⊔ Variety`.
- **IR64 (8 assertions):** `resistantTo` brown planthopper, green leafhopper and bacterial leaf blight; `moderatelyResistantTo` rice blast and stem borer ("moderate resistance to blast, BPH biotype 2, and stem borer"); `vulnerableTo` rice tungro disease ("IR64 is susceptible to tungro disease", the reason it was replaced in the Philippines and Indonesia) and iron toxicity ("It is also susceptible to Fe toxicity"), which the 0.7.0-dev iron-toxicity disorder now makes expressible. **Not modelled:** whitebacked planthopper, grassy stunt virus, BPH biotypes, drought and submergence — no entity exists for them, and none was invented.
- **Angke and Conde (2 each):** Indonesian varieties "developed by pyramiding BB resistance genes into IR64", so each is `resistantTo` bacterial leaf blight.
- **Logic trap found and fixed — an inverse's range.** Widening `vulnerableTo`'s domain was not enough: its inverse `threatens` still had the range `GrowthStage ⊔ Plant`, so `IR64 vulnerableTo …` entailed that IR64 is a growth stage or a plant, which contradicts `Variety` being disjoint from both. **HermiT reported the file inconsistent**; Pellet named the axioms. The range of `threatens` was widened to match. A new audit now compares every inverse pair's domain with its partner's range: **15 pairs, 0 mismatches.**
- **Checks:** HermiT consistent with `-k`; `-U` lists only `owl:Nothing`; control (`IR64` as Variety + Disease) inconsistent. 353 axioms = 353 domain assertions, 0 unreified, orphan, duplicate or incomplete; 0 domain/range violations under OWL RL; 0 individuals in two disjoint core classes.
- **Benchmark:** unchanged at **21 PASS / 2 PARTIAL / 1 FAIL / 1 DOC**; CQ-21 341/341 → **353/353**. A variety is neither a Disease nor a Pest, so no coverage denominator moved. `varietyOf`, `resistantTo` and `moderatelyResistantTo` were added to CQ-22's checked list, so the extension could not pass by omission. Elicited CQs unchanged (9 / 8 / 2).
- **Result:** 67,859 asserted / 163,293 OWL RL triples.

### 2026-09-15: 0.7.0-dev — unverified BBPOPT source resolved; iron toxicity and salinity

Closes the BBPOPT open item and adds the excess side of `AbioticFactor` that the domain expert asked for. Decisions approved 2026-09-15. Pre-patch file: `Backup/Rice MMKG.backup-0.7.0-dev-pre-sourcefix.rdf`.

- **Severity triage removed (6 assertions, 6 axioms):** `Low_Severity recommends No_Action_Needed`, `Medium_Severity recommends Monitoring` and `Field_Inspection`, `High_Severity recommends Preventive_Action` and `Immediate_Intervention`, `Critical_Severity recommends Immediate_Intervention`. They cited "BBPOPT (2022)", which was never found. The two official guidelines that were read — *Petunjuk Teknis Pengamatan dan Pelaporan OPT dan DPI* 2018 (Kepdirjen TP No. 36/HK.310/C/3/2018) and its 2021 revision (Kepdirjen TP No. 127/HK.310/C/5/2021) — define attack-intensity categories but map none to an action. The 2021 version also contradicts the first assertion: its lightest category, *ringan*, already lies above the control threshold. The six are kept as questions for the domain expert (Open items). **CQ-13 falls from 4/4 to 0/4 (FAIL)**; the CQ was not edited and no replacement mapping was made up.
- **`SeverityLevel` aligned to the 2021 juknis, as comments only:** Low/Medium/High/Critical ↔ ringan/sedang/berat/puso. Disease bands: above the control threshold up to 10%, >10–25%, >25–85%, >85%. Pest bands: up to 25%, >25–50%, >50–85%, >85%. The two band sets are kept apart. The comments say the correspondence is a modelling choice. No `skos` mapping was added, because the juknis has no IRIs. The class comment no longer says the levels drive management actions, and the ontology header no longer lists BBPOPT as a source.
- **Re-sourced:** `Crop_Sanitation requires Harvest_Stage` now cites the IRRI tungro fact sheet ("Plow infected stubbles immediately after harvest to reduce inoculum sources…", checked live). **No axiom cites BBPOPT any more.** The juknis is cited by SK number, not URL: the only online copy found was an unofficial mirror.
- **Iron toxicity and salinity (17 assertions):**
  - **Sources:** the IRRI Rice Knowledge Bank fact sheets *Iron (Fe) toxicity* and *Salinity* (deficiencies and toxicities), read in full on 2026-09-15. Both conditions are also listed in the 2021 juknis (Tabel 11: keracunan Fe, "asem-aseman"; keracunan garam, Na and Cl), which the individuals' comments name. Assertions cite IRRI, whose pages are live.
  - **Individuals:** `Iron_Toxicity` and `Salinity` (`AbioticFactor`) `causes` `Iron_Toxicity_Disorder` and `Salinity_Disorder`.
  - **Symptoms, from each sheet's "How to identify" list only:**
    - Iron toxicity: `Leaf_Bronzing` (new), `Stunted_Growth`, `Reduced_Tillering` ("extremely limited tillering") and `Black_Root` ("many black roots").
    - Salinity: `White_Leaf_Tip` (new), `Chlorotic_Leaf_Patch` (new), `Stunted_Growth` and `Reduced_Tillering`.
    - **Left out:** "leaves narrow but often remain green"; "purple-brown if severe" (a grade); orange-yellow drying tips "in some varieties"; "patchy field growth" (a field pattern).
    - **Not reused:** `Yellow_Orange_Discoloration` (the tungro symptom) and `Dry_Leaf_Tip`/`Brown_Leaf_Tip` (a different colour).
  - **Prevention only:** `preventedBy Water_Management` for both. For iron toxicity the sheet says "use intermittent irrigation and avoid continuous flooding"; for salinity, "submerge the field … leach the soil after planting under intermittent submergence". No `controlledBy`: both sheets say "There is currently no practical field management option to treat" the condition. Tolerant varieties were not mapped to `Resistant_Variety`, because tolerance of a soil stress is not host-plant resistance to a pest or pathogen.
  - **Risk factors:** `Waterlogged_Soil` → iron toxicity ("lowland rice soils with permanent flooding during crop growth"); `Low_Rainfall` → salinity ("insufficient irrigation water in seasons/years with low rainfall").
- **Checks:**
  - **HermiT:** consistent with `-k`; `-U` lists only `owl:Nothing`; the control (`Salinity` as AbioticFactor + Pathogen) is inconsistent.
  - **Provenance:** 341 axioms = 341 domain assertions, with 0 unreified, orphan, duplicate or incomplete axioms. Evidence types: 335 literature-curated, 6 ontology-derived.
  - **OWL RL:** both new causes are typed only `AbioticFactor`.
- **Result:** 67,708 asserted / 163,011 OWL RL triples. Benchmark **20 PASS / 3 PARTIAL / 1 FAIL / 1 DOC** (was 22 / 2 / 0 / 1).
  - **CQ-13:** 0/4, FAIL.
  - **CQ-01:** 7/15 (47%), PARTIAL. The two new disorders entered the Disease denominator, and an abiotic disorder has no pathogen by construction.
  - **CQ-12:** 9/22 (41%).
  - **Other figures:** CQ-02 21/22, CQ-03 17/22, CQ-04 39/39, CQ-05 13/22, CQ-11 10/15, CQ-15 169, CQ-18 1/39, CQ-21 341/341, CQ-23 18/30.
  - **CQ-08:** 2/3 (was 1/2). `Water_Management` became a preventive treatment, and it already had growth-stage prerequisites.
  - **Elicited CQs:** statuses unchanged (9 / 8 / 2). The CQ-A18 gap note was updated because it described the removed `recommends` links; the note text only, not the CQ or its queries.
- **CQ-01 denominator corrected (approved 2026-09-15, after the run above):** the denominator now excludes diseases caused by an `AbioticFactor` (`FILTER NOT EXISTS { ?a rice:causes ?d . ?a a rice:AbioticFactor }`). An abiotic disorder cannot have a causal pathogen, so counting it as a gap measured the modelling pattern rather than missing knowledge; this is the counterpart of the earlier numerator fix. Because it also restores the verdict, both figures are reported: **7/9 PASS** (corrected) and 7/15 PARTIAL (original). Only CQ-01 was corrected; CQ-03, CQ-11 and CQ-12 still include abiotic disorders, since their questions apply to them. **Final benchmark: 21 PASS / 2 PARTIAL / 1 FAIL / 1 DOC.**

### 2026-09-15: 0.7.0-dev — full consistency and provenance audit; literal and label hygiene

Audit of the whole file after the abiotic patch. Pre-patch file: `Backup/Rice MMKG.backup-0.7.0-dev-pre-hygiene.rdf`. No assertion added or removed.

- **Logic:** HermiT consistent (`-k`), no unsatisfiable class (`-U` lists only `owl:Nothing`), control (`Black_Root` as Symptom + Disease) inconsistent.
- **Provenance:** 330 domain assertions = 330 axioms, no assertion without an axiom, no duplicate or orphan axiom; every axiom has exactly one source, citation and evidence type; every URL inside a citation equals its `dcterms:source`; no domain or range violation (including the widened `causes`); no undeclared `rice:` IRI or property; no individual in two disjoint core classes.
- **Sources checked live (41 unique):** all IRRI (23), IRAC and FAO pages 200; AGROVOC and PO IRIs resolve (301/303 → 200); the 14 CABI DOIs and the Wang et al. DOI resolve at doi.org (the CABI landing site refuses automated clients). **The BBPOPT homepage returns 403** — see Open items.
- **Fixed (4):** the citation on `Crop_Sanitation requires Harvest_Stage` had no language tag (v0.6.1 tagged only its evidence type; CQ-24 checks evidence types only, so it passed) → `@en`; the `PaddyDoctorDataset` label → `@en`; `Empty_Grain` carried two labels, "Empty Grain" and "empty grain" → "empty grain" kept; `Biological_Control_Category` shared the label "biological control" with the Treatment `Biological_Control` → "biological control (category)".
- **Result:** 67,588 asserted / 162,775 OWL RL triples; 330 axioms; HermiT consistent; benchmark (22 / 2 / 0 / 1) and elicited (9 / 8 / 2) unchanged.
- **BBPOPT source investigated:** see the Open item — the cited 2022 guideline was not found, and the closest official juknis does not support the severity → action mapping.

### 2026-09-15: 0.7.0-dev — `AbioticFactor`: nutrient deficiencies as causes of disease

Follows domain-expert feedback on the conceptual schema (2026-09-14): causes are biotic or abiotic (deficiency or excess of a substance), and abiotic factors, pests and pathogens all end at Disease; the ontology had no abiotic class. Design approved 2026-09-15 (an abiotic factor `causes` a Disease, mirroring `Pathogen causes Disease`). Pre-patch file: `Backup/Rice MMKG.backup-0.7.0-dev-pre-abiotic.rdf`.

- **Source:** the four IRRI Rice Knowledge Bank nutrient-management fact sheets — *Nitrogen (N)*, *Phosphorus (P)*, *Potassium (K)*, *Zinc (Zn)* — read in full on 2026-09-15. Every new assertion (37) cites the sheet its sentence comes from.
- **Class `AbioticFactor`** with `Nitrogen_Deficiency`, `Phosphorus_Deficiency`, `Potassium_Deficiency`, `Zinc_Deficiency`, each `causes` a new `Disease` (`…_Deficiency_Disorder`). IRRI names a deficiency and its disorder with one term; the split into cause and disorder is the modelling pattern, stated in the individuals' comments. **Excess** is not modelled: the sheets describe deficiencies only.
- **Logic fix required by the pattern:** `causes` had `rdfs:domain Pathogen` (and `causedBy` the matching range), so an abiotic cause would have been inferred to be a Pathogen and — with `AbioticFactor` disjoint from `Pathogen` — made the ontology inconsistent. Domain and range are now `Pathogen ⊔ AbioticFactor`. Checked: under OWL RL each deficiency is typed only `AbioticFactor`, and a HermiT control typing `Zinc_Deficiency` as Pathogen is inconsistent. `AbioticFactor` joined the core `AllDisjointClasses` axiom (now 16 classes).
- **Symptoms (19 `indicatedBy`)**, taken from each sheet's "deficiency symptoms" sentence and nothing else: N — stunted growth, yellowish-green leaves, reduced tillering; P — stunted growth, dark green erect leaves, reduced tillering, thin spindly stems, delayed maturity, unfilled grains; K — stunted growth, yellowish-brown leaf margins, necrotic leaf tips and margins, black roots, lodging, unfilled grains; Zn — stunted growth, dusty brown spots on upper leaves, empty grains, delayed maturity. Existing symptoms were reused only where the meaning is the same (`Stunted_Growth`, `Reduced_Tillering`, `Empty_Grain`); 9 are new, each with `affectsPlantPart` from the same sentence. `Yellow_Leaf` and `Dry_Leaf_Tip` were deliberately not reused (a different colour; dry is not necrotic). Yield figures and field patterns ("patches of poorly established plants") are not symptoms and were left out.
- **Plant parts:** `Root` = PO:0009005 and `Stem` = PO:0009047 (culm is an exact synonym) added for the new symptoms.
- **Control only where the source ties it to the deficiency:** `Zinc_Deficiency_Disorder controlledBy Zinc_Fertilizer_Application` (new Treatment; "If Zn deficiency symptoms are observed in the field, apply…") and `controlledBy Water_Management` ("Rice plants can recover from Zn deficiency if the field is drained"). The N, P and K sheets give fertilizer rates by yield target, not as a remedy for the deficiency, so no control was asserted for them.
- **Risk factors from the "occurrence" paragraphs**, only where an existing `EnvironmentalFactor` matches: `Poor_Soil_Drainage` → zinc ("very poorly drained soils") and nitrogen ("poorly drained … soils"); `Waterlogged_Soil` → zinc ("continuously flooded paddy soils"). Potassium's "high levels of N and P application" is a fertilizer rate, not `Excessive_Nitrogen`, and was not mapped.
- **Two CQ queries corrected so they match their own question.** Benchmark CQ-01 ("…identified causal **pathogen**?") counted any `causes`; after this change it reported 11/13 by counting abiotic causes as pathogens. Its numerator now also requires `?p a rice:Pathogen`. The same filter was added to elicited CQ-A01's answer-form query, which had begun listing deficiencies in its *pathogen* column. The CQ texts are unchanged; before this change the unfiltered and filtered queries returned the same result, because only pathogens could `causes`.
- **Result:** 67,589 asserted / 162,778 OWL RL triples; 330 axioms = 330 domain assertions, 0 unreified; HermiT consistent with `-k` (controls inconsistent). Benchmark **22 PASS / 2 PARTIAL / 0 FAIL / 1 DOC** (was 23 / 1 / 0 / 1): CQ-01 7/13, CQ-02 19/20, CQ-03 17/20, CQ-04 36/36, CQ-05 13/20, CQ-11 10/13, **CQ-12 9/20 (45%) → PARTIAL**, CQ-15 159, CQ-18 1/36, CQ-21 330/330, CQ-23 18/28. CQ-12 was not lifted by adding `recommends`: IRRI does not use the ManagementAction vocabulary, and adding an assertion to clear a threshold is what this project refused for CQ-10. Elicited statuses unchanged (9 / 8 / 2).

### 2026-09-15: 0.7.0-dev — two open items closed (symptom label, AGROVOC mapping)

Pre-patch file: `Backup/Rice MMKG.backup-0.7.0-dev-pre-openitems-patch.rdf`. No assertion added or removed.

- **`Stem_Rot_Symptom` relabelled "leaf sheath lesion"** and given an `rdfs:comment`. The individual is the symptom of `Sheath_Blight`, which IRRI's sheath blight fact sheet describes as oval or ellipsoidal greenish-grey lesions on the leaf sheath; stem rot is a separate disease in IRRI's list (sclerotia inside the culm, lodging), although its first lesions on the outer leaf sheath look similar — IRRI itself warns that "sheath blight has symptoms similar to stem rot", the likely origin of the old label. **The IRI is unchanged:** it was published in tags v0.6.1 and v0.6.2, and renaming needs a deprecation policy that has not been decided.
- **`Biological_Control` (Treatment) mapping to AGROVOC c_918 downgraded from `exactMatch` to `closeMatch`.** c_918 is the control-method category, now matched exactly by `Biological_Control_Category`; the Treatment is the practice.
- **Result:** 67,200 asserted / 162,043 OWL RL triples (+1: the comment); 293 axioms = 293 domain assertions; SKOS exact/close/broad 40 / 23 / 1; HermiT consistent with `-k` (control `Stem_Rot_Symptom` as Symptom + Disease inconsistent); benchmark and elicited results unchanged (23 / 1 / 0 / 1; 9 / 8 / 2).

### 2026-09-15: 0.7.0-dev — `ManagementCategory` for treatments; control sources made queryable

Third literature-backed schema item of Phase 3 (elicited CQ-A07). Pre-patch file: `Backup/Rice MMKG.backup-0.7.0-dev-pre-managementcategory.rdf`.

- **Source authority needed no schema.** Every `controlledBy` assertion already carries an `owl:Axiom` with `dcterms:source` and a citation; CQ-A07's earlier note that source authority was "not modelled" was wrong — only the query did not read the axiom. The query now does.
- **Class `ManagementCategory`** (`closeMatch` AGROVOC *control methods*, c_5728) with 4 individuals whose names follow AGROVOC's narrower concepts, checked live: `Chemical_Control_Category` = c_1514, `Biological_Control_Category` = c_918, `Cultural_Control_Category` = c_2020 (`exactMatch`); `Host_Plant_Resistance_Category` ~ c_331556 (`closeMatch`: the definition — "intentional use of resistant crop cultivars" — is a control tactic, but AGROVOC files the concept under *biological properties*). AGROVOC's *genetic control* (c_3216) was deliberately not used for resistant varieties: it means sterile-insect and pest-genome tactics. Individual IRIs carry a `_Category` suffix because `Biological_Control` already names a Treatment.
- **`hasManagementCategory`** (`Treatment` → `ManagementCategory`), 6 assertions. AGROVOC supplies the category names but does not place the treatment concepts under them (crop rotation sits under *cropping systems*, pesticide application and seed treatment under *activities*), so each membership has its own source:
  - `Insecticide_Application` → chemical and `Biological_Control` → biological: IRRI Rice Knowledge Bank *Planthopper* fact sheet, whose management section is headed "Biological control" (natural enemies) and "Chemical control" (insecticides) — `literature-curated`.
  - `Trichoderma_Application` → biological (AGROVOC c_918 definition: "use of biological agents (e.g. insects, micro-organisms…)"), `Resistant_Variety` → host plant resistance (c_331556), `Crop_Rotation` and `Crop_Sanitation` → cultural (c_2020: "manipulation of abiotic and biotic components of the agroecosystem…"; scope note "changed cropping patterns") — `ontology-derived`, citing the AGROVOC concept and the source of its definition.
- **Not categorised, on purpose:** `Fungicide_Application` (IRRI labels pesticide use "chemical control" but never names fungicides under that heading — evidence judged indirect), `Water_Management` (IRRI files seedbed flooding under "Mechanical & physical measures", AGROVOC would make it cultural), `Seed_Treatment` (IRRI gives both a fungicide and a hot-water treatment), `Neem_Based_Pesticide` (AGROVOC places botanical pesticides under *biopesticides* but defines them as plant-derived chemicals), `Vector_Control` (an objective spanning insecticides and resistant varieties, not a single tactic), and `Good_Agricultural_Practice` (no `controlledBy` uses it). See Open items.
- **Disjointness:** `ManagementCategory` added to the core `AllDisjointClasses` axiom (now 15 classes).
- **CQ instruments:** `hasManagementCategory` added to CQ-22's property list. Elicited CQ-A07 now returns, for Stem Borer, `Biological_Control` (biological control) and `Insecticide_Application` (chemical control), each with the CABI 49009 source of its `controlledBy` assertion; status *partial - schema* → **answers** (CQ text unchanged).
- **Result:** 67,199 asserted / 162,041 OWL RL triples; 293 axioms = 293 domain assertions, 0 unreified; HermiT consistent with `-k` (controls `Chemical_Control_Category` as ManagementCategory + Disease and `Rice` as Plant + Disease both inconsistent); benchmark **23 PASS / 1 PARTIAL / 0 FAIL / 1 DOC** (CQ-21 293/293, CQ-22 0); elicited **9 answers / 8 partial / 2 NO ANSWER**.

### 2026-09-15: 0.7.0-dev — `TransmissionMode` for vector-borne pathogens

Second literature-backed schema item of Phase 3 (elicited CQ-A02). Pre-patch file: `Backup/Rice MMKG.backup-0.7.0-dev-pre-transmissionmode.rdf`.

- **Class `TransmissionMode`** with one individual, `Semi_Persistent`. Other modes (non-persistent, persistent) are not created until a pathogen in the graph needs them. No AGROVOC or OLS concept for "semi-persistent transmission" exists (AGROVOC has only *virus transmission*, c_81a342e6, a process rather than a mode), so the individual is local.
- **`hasTransmissionMode`** (`Pathogen` → `TransmissionMode`): `Rice_Tungro_Bacilliform_Virus` and `Rice_Tungro_Spherical_Virus` → `Semi_Persistent`, both citing Wang et al. (2022), *A Review of Vector-Borne Rice Viruses*, Viruses 14(10):2258 (doi:10.3390/v14102258, CC BY 4.0). Its table "Transmission biology of distinct rice viruses" lists both viruses as semi-persistent, with *Nephotettix virescens* among the vectors; full text read from PMC9609659. Consistent with ICTV's Secoviridae profile (Thompson et al. 2017: "Field transmission is semi-persistent by aphids or leafhoppers") and with IRRI's tungro fact sheet, which describes the behaviour without naming the mode.
- **Asserted per pathogen, not per vector–pathogen pair** — valid while the source gives one mode for all of a pathogen's vectors, as it does for both tungro viruses. A pathogen whose mode differs by vector would need the pair modelled instead; recorded in the property's `rdfs:comment`.
- **Retention period not asserted.** Wang et al. give 4–5 days for RTBV and 2–4 for RTSV, while IRRI says a leafhopper can transmit within 5–7 days; the sources disagree, so neither figure was chosen.
- **Disjointness:** `TransmissionMode` added to the core `AllDisjointClasses` axiom (now 14 classes).
- **CQ instruments:** `hasTransmissionMode` added to CQ-22's property list; elicited CQ-A02's query now returns the mode and its status moves from *partial - schema* to **answers** (CQ text unchanged).
- **Result:** 67,120 asserted / 161,916 OWL RL triples; 287 axioms = 287 domain assertions, 0 unreified; HermiT consistent with `-k` (controls `Semi_Persistent` as TransmissionMode + Disease and `Rice` as Plant + Disease both inconsistent); benchmark **23 PASS / 1 PARTIAL / 0 FAIL / 1 DOC** (CQ-21 287/287, CQ-22 0); elicited **8 answers / 9 partial / 2 NO ANSWER**.

### 2026-09-15: 0.7.0-dev — `PlantPart`, symptom → organ, `partOf`

First schema extension of Phase 3 (literature-backed, no expert data needed). Commit `a331769`; not a release, so `owl:versionInfo` and `owl:versionIRI` read `0.7.0-dev` rather than reusing the tagged `0.6.2`. Pre-patch file: `Backup/Rice MMKG.backup-v0.6.2-pre-plantpart.rdf`.

- **Class `PlantPart`** with 8 individuals, aligned to the Plant Ontology (checked live via EBI OLS4 on 2026-09-15): `Whole_Plant` = PO:0000003, `Leaf` = PO:0025034, `Leaf_Blade` = PO:0020039 *leaf lamina*, `Leaf_Sheath` = PO:0020104, `Panicle` = PO:0030123 *panicle inflorescence* (all `exactMatch`); `Tiller` ~ PO:0005001 *basal axillary shoot system* ("tiller" is only a narrow synonym) and `Grain` ~ PO:0030104 *caryopsis fruit* (PO denotes the dehulled grain) as `closeMatch`; `Panicle_Neck` local only — PO has no term for it.
- **`affectsPlantPart`** (`Symptom` → `PlantPart`): 27 assertions on 26 of the 27 symptoms, asserted per symptom rather than per disease–symptom pair (only `Brown_Lesion` has two organs: leaf blade and leaf sheath). Every assertion cites an IRRI Rice Knowledge Bank fact sheet (13 pages, read on 2026-09-15). The CABI datasheets behind the existing `indicatedBy` assertions return 403, so organ claims could not be verified against them. `Excessive_Tillering` is left without an organ: its only disease (downy mildew) has no IRRI fact sheet, and the candidate article (Lee et al. 2003, doi:10.5423/rpd.2003.9.1.052) could not be read.
- **`partOf`** (transitive, `PlantPart` → `PlantPart`, `closeMatch` BFO:0000050): only the 2 relations the Plant Ontology records — leaf lamina part_of leaf and leaf sheath part_of vascular leaf (is_a leaf). PO records no part_of for panicle, grain or tiller, so none is asserted. Provenance is the PO term with `evidenceType` `ontology-derived`, a new value alongside `literature-curated`.
- **Disjointness:** `PlantPart` added to the `AllDisjointClasses` axiom of the core domain classes. Without it an organ typed as `Disease` went undetected — the first HermiT control injected exactly that and was not reported.
- **Plant Ontology (via OLS) was the source, not a commercial library.** Plantix was considered and rejected as a source: its terms of use (PEAT GmbH) prohibit scraping and data mining, and its pages carry no citable references.
- **CQ instruments:** CQ-22's property list now includes `affectsPlantPart` and `partOf`, so the new assertions are held to the same provenance check. Elicited CQ-A03's query now returns the organ per symptom; the CQ text is unchanged and its status stays *partial - schema*, because growth stage is still attached to the disease, not the symptom.
- **Result:** 67,090 asserted / 161,861 OWL RL triples; 285 axioms = 285 domain assertions, 0 unreified; HermiT consistent with `-k` (both controls inconsistent); benchmark **23 PASS / 1 PARTIAL / 0 FAIL / 1 DOC** (CQ-21 285/285, CQ-22 0); elicited CQ statuses unchanged (7 answers / 10 partial / 2 NO ANSWER).
- **Found while reading IRRI, not changed:** `Stem_Rot_Symptom` is asserted on `Sheath_Blight`, but IRRI describes sheath-blight lesions on the leaf sheath and treats stem rot as a separate disease, so the label is misleading. `Wilting` on `Sheath_Blight`, `Rice_Blast_Disease` and `Bacterial_Panicle_Blight` is not mentioned by IRRI; the assertions cite CABI, which cannot be read, so they are not shown to be wrong. See Open items.

### 2026-09-15: v0.6.2 — CABI sources as DOIs, citations from Crossref, stale provenance file archived

No triple added or removed and no assertion changed: 66,802 asserted / 161,447 OWL RL triples, 256 axioms = 256 domain assertions, benchmark 23 PASS / 1 PARTIAL / 0 FAIL / 1 DOC, HermiT consistent, elicited CQ results unchanged. Only source URIs, citation text and the version changed. The work was done on 2026-09-14 after `v0.6.1` had been committed, and is released separately so that each version number names exactly one content state. `owl:versionInfo` and `owl:versionIRI` bumped to `0.6.2`.

- **`provenance_axioms.rdf` archived** to `Backup/provenance_axioms.archived-2026-09-14.rdf`. It was an intermediate from the 2026-08-21 provenance pass that had drifted: 306 axioms, of which 55 are the spurious `subPropertyOf`/SKOS citations removed from `Rice MMKG.rdf` on 2026-08-22, 1 is for the merged-away `Rice vulnerableTo Scirpophaga_Incertulas`, and the other 250 lack `rice:evidenceType`; it was also missing 6 axioms the main file has. No script read it. Re-syncing would only duplicate the main file, and merging it would be harmful, because a reified axiom re-asserts its triple and would resurrect the deleted assertions. `Rice MMKG.rdf` is the single source of truth.
- **CABI source URIs replaced by DOIs.** All 242 `https://www.cabi.org/isc/datasheet/<id>` URIs (14 distinct datasheets) now read `https://doi.org/10.1079/cabicompendium.<id>`. Each id was checked live: the old URL returns 301 to the matching `cabicompendium` DOI page, the DOI resolves through doi.org, and the Crossref title names the same organism as the citation text.
- **CABI citations rewritten from Crossref.** All 242 CABI citation segments read "CABI (2022). … Crop Protection Compendium. CAB International" — a year, a compendium name and, for two datasheets, an author that the DOI metadata does not support. Each is now built from the Crossref record of its DOI: `<author> (<year>). <datasheet title>. CABI Compendium. CABI Publishing. https://doi.org/10.1079/cabicompendium.<id>`. Years are 2021 for 10 datasheets, 2019 for 47654 (rice tungro) and 49243 (*S. macrospora*), 2025 for 14691 and 2012 for 47203. Two datasheets have personal authors and are no longer attributed to CABI: 14691 *Bipolaris oryzae* → Castell Miller, C. (2025); 47203 *Thanatephorus cucumeris* → Back, M. (2012). Datasheet titles follow Crossref, so some common names changed (e.g. *Burkholderia glumae* "bacterial grain rot", not "bacterial panicle blight"). Only the CABI segment was replaced; co-citations such as "/ IRRI (2020). Rice Doctor: …" are untouched.
- **`elicited_cq_sparql.py`** now labels its report from `owl:versionInfo` instead of a hardcoded "v0.6".

### 2026-09-14: v0.6.1 — provenance gaps closed, CQ-10 and CQ-24 fixed, v0.6 figures corrected

- **The published v0.6 figures described the wrong file.** This document, the root README, the ESWC plan, `CQ_SPARQL_Documentation.md` and the original benchmark report all quoted 66,874 asserted / 161,568 materialised triples and 265 axioms. Those were measured at commit `19d632d` (10:43). Commit `103c5ed` "Fix inconsistency" (12:04 the same day) then removed 11 domain assertions — 6× `Normal_Health occursIn`, `Normal_Health controlledBy Good_Agricultural_Practice`, and 4× `Rice vulnerableTo` (`Burkholderia_Glumae`, `Rice_Tungro_Bacilliform_Virus`, `Sclerophthora_Macrospora`, `Xanthomonas_Oryzicola`) — together with their 12 axioms (84 triples). **The released v0.6 file measures 66,780 / 161,416 triples, 253 axioms over 255 domain assertions.** Benchmark verdicts were unaffected (21 / 1 / 2 / 1), but CQ-15 is 133 not 140 and CQ-21 is 253/253 not 265/265. The released file is preserved as git tag `elicited-baseline-v0.6`.
- **v0.6 did not have 100% provenance.** `Stem_Borer indicatedBy Dead_Tiller` and `Stem_Borer indicatedBy White_Ear`, added in the v0.6 Deadheart disambiguation, never received an `owl:Axiom`. Neither provenance CQ could see it: CQ-21 divides by the number of axioms, and CQ-22 only inspected axioms that exist. Both now carry axioms citing IRAC (2025), *Rice Stem Borer, Scirpophaga incertulas: Sustainable Control Strategies in Asia* — the only source that could be read directly on the day (CABI and Plantwise returned 403, the IRRI Knowledge Bank refused connections).
- **CQ-10 fixed differently from the plan.** The v0.6 action item was `Nephotettix_Virescens controlledBy Vector_Control`. Gallagher et al. (2002, FAO/IRC) state that "controlling the vector population with insecticide does not always result in tungro control" and recommend resistant varieties where synchronous planting is impossible; IRRI's tungro fact sheet says the same. Asserting vector control only to make the CQ pass would not have been supported by the literature, so `Nephotettix_Virescens controlledBy Resistant_Variety` was added instead, with its axiom citing Gallagher et al. (2002).
- **CQ-24 fixed.** The one untagged `rice:evidenceType` literal (axiom on `Crop_Sanitation requires Harvest_Stage`) is now `"literature-curated"@en`.
- **CQ-22 extended** to also flag domain assertions with no reified axiom; the CQ count stays at 25. Control-tested: 2 violations on the released v0.6 file, 0 on v0.6.1.
- **Result:** 66,802 asserted / 161,447 OWL RL triples; 256 axioms = 256 domain assertions, 0 orphans, 0 duplicates; HermiT consistent (run on a space-free copy, with an injected-contradiction control that correctly reports inconsistent); benchmark **23 PASS / 1 PARTIAL / 0 FAIL / 1 DOC (95.8%)**; the 19 queried elicited CQs return exactly the same results as on v0.6. `owl:versionInfo` and `owl:versionIRI` bumped to `0.6.1`. Released as git tag `v0.6.1` (commit `1d13542`).
- **Backup:** `Ontology/Backup/Rice MMKG.backup-v0.6-pre-v0.6.1.rdf`.

### 2026-09-03: v0.6 — Deadheart Disambiguation, DL Reasoner Consistency, and 25 CQ Benchmark

- **Disambiguated `Deadheart` class collision:** In v0.5, `Deadheart` was asserted as a `Symptom` while simultaneously carrying domain relations belonging to `Disease` (`preventedBy`, `indicatedBy`, `occursIn`, `controlledBy`, `increaseRiskOf`), causing HermiT and Pellet reasoners to produce 33 inconsistency explanations due to `AllDisjointClasses {Disease, Symptom, ...}`. In v0.6:
  - `Deadheart` is retyped as `Disease` (rice damage condition/syndrome caused by yellow stem borer *Scirpophaga incertulas*).
  - All 1,442 Paddy Doctor dead-heart images now target the actual symptom individual: `Dead_Tiller` (`rice:captures rice:Dead_Tiller`), which has `rdfs:label "dead heart"@en` and is typed `Symptom`.
  - `Stem_Borer` connects to its true symptoms: `Dead_Tiller` and `White_Ear`.
  - Reasoner result: **100% Consistent** in HermiT and Pellet with 0 unsatisfiable classes and 0 disjointness conflicts.
- **Sequential 25 CQ SPARQL Benchmark Suite:**
  - Implemented automated benchmark runner (`cq_sparql_benchmark.py`) covering 25 Competency Questions structured across Reasoning Depth (L1–L4) and Knowledge Dimensions (D1–D3) with 4 formal evaluation modes (`coverage`, `negative`, `entailment`, `documented`).
  - Achieved **21 PASS (87.5% pass rate)**, 1 PARTIAL (CQ-18 visual grounding gap at 4%), 2 FAIL (CQ-10 vector control triple, CQ-24 literal `@en` tag), and 1 DOCUMENTED (CQ-20 sensor observations).
  - Evaluated on OWL RL materialised graph: expands from 66,874 asserted triples to **161,568 materialised triples (+94,694 triples in 24.0s)**. CQ-14 verifies 1,442 entailed members in `SymptomaticObservation`, and CQ-15 derives 140 inverse assertions.
  - *Correction (2026-09-14): the figures in the two bullets above were measured before "Fix inconsistency" (`103c5ed`) later the same day. On the released v0.6 file they are 66,780 / 161,416 triples, CQ-15 = 133 and CQ-21 = 253/253; the verdicts (21 / 1 / 2 / 1) are unchanged. See the v0.6.1 entry.*
- **Backup preserved:** Pre-fix state saved as `Ontology/Backup/Rice MMKG.backup-v.05.rdf`.

### 2026-09-01: v0.5 — Vector Transmission Relations & CQ Evaluation Framework

- Added `rice:transmits` and `rice:transmittedBy` object properties with explicit domain (`Pest`) and range (`Pathogen`) to formally represent insect vector epidemiology (Green leafhopper transmitting Tungro viruses).
- Formulated initial 25 Competency Questions for Phase 1 functional and reasoning evaluation toward ESWC 2027.

### 2026-08-25: full external-identifier audit — EPPO codes and dataset citation fixed

Follow-up to the CABI provenance fix below: every external identifier
asserted anywhere in `Rice MMKG.rdf` was independently re-verified
(live lookup, not re-trusted) — all 33 `skos:exactMatch`/`closeMatch`/
`broadMatch` AGROVOC concepts, all 10 `NCBITaxon` IDs, all 4 `PECO`
terms, all 15 `rice:eppoCode` literals, and the dataset-level
`dcterms:source`/`bibliographicCitation` on `PaddyDoctorDataset`. AGROVOC,
NCBITaxon, and PECO all checked out (33/33, 10/10, 4/4) — the live-API
verification process from the 2026-08-22 alignment round held up. Two
new problems found and fixed:

- **7 of 15 EPPO codes were wrong** (`Rice MMKG.rdf` only —
  `provenance_axioms.rdf` doesn't carry this property), the same
  fabrication pattern as the CABI IDs — a plausible 6-letter code, never
  looked up. One (`Rice_Bug`'s `LEPTOR`) didn't just fail to resolve, it
  silently resolved to the *wrong organism*: `LEPTOR` is EPPO's code for
  a fungus, *Leptosphaeria orthrosanthi*, not for `Leptocorisa oratorius`
  (the rice bug this individual actually represents) — a case where a
  fabricated ID happened to collide with a real, unrelated EPPO record,
  the same failure shape as the CABI→*Quercus brantii* collision.
  Corrected: `Hispa` `DCLPAR`→`HISPAR`, `Armyworm` `LEUCOM`→`PSEDSE`,
  `Stem_Borer` `SCPIIN`→`SCHOBI`, `Rice_Bug` `LEPTOR`→`LEPROR`,
  `Burkholderia_Glumae` `BURBGL`→`PSDMGM`, `Sclerophthora_Macrospora`
  `SCLPMA`→`SCPHMA`, `Nephotettix_Virescens` `NEPHVI`→`NEPHIM`. The
  other 8 (`CNAPME`, `NILALU`, `PYRIOR`, `XANTTO`, `XANTOR`, `COCHMI`,
  `RTBV00`, `RTSV00`) were already correct.
- **`PaddyDoctorDataset`'s own source citation was wrong on both fields.**
  `dcterms:source` pointed to `kaggle.com/datasets/petmod/riceleafs`,
  which 404s — no such dataset/user exists. `dcterms:bibliographicCitation`
  credited "P. Selvaraj, et al. (2022)," but the dataset's real authors
  (arXiv:2205.11108) are Petchiammal A., Briskline Kiruba S., D. Murugan,
  and Pandarasamy A. — "Selvaraj" appears nowhere on the paper. The
  10,407-image train split cited in that paper matches this ontology's
  own `ImageObservation` count exactly, confirming it's the right source
  once correctly identified. Fixed to the live Kaggle competition URL
  (`kaggle.com/competitions/paddy-disease-classification`) and the
  correct author list, in both `Rice MMKG.rdf` and this document's §1.
- **Noted, not changed:** `Ontology/patch_assertions.rdf` (451 lines,
  never merged into `Rice MMKG.rdf` — confirmed none of its triples are
  present in the live file) turns out to be the *rejected* version of
  the "9 more fabricated AGROVOC identifiers" episode from the
  2026-08-22 entry below — one of its concepts resolves to "Tonga,"
  matching that entry's own example verbatim. It's correctly inert, but
  worth deleting or clearly labelling as a rejected draft so a future
  session doesn't mistake it for a pending patch to apply.

### 2026-08-25: false CABI datasheet IDs in `dcterms:source`, fixed

A provenance audit of `provenance_axioms.rdf` found that all 14 distinct
CABI Compendium `dcterms:source` URLs used across the file's 320 reified
axioms (259 of the 320 assertions) pointed to the wrong datasheet — the
numeric ID redirected to an unrelated species (e.g. `Magnaporthe_oryzae`'s
citation resolved to *Quercus brantii*, an oak tree; `Nilaparvata_lugens`'s
to *Podisus nigrispinus*, an unrelated predatory bug). The
`dcterms:bibliographicCitation` text (species name, disease name, "CABI
2022") was correct in every case — only the numeric ID in the URL was
wrong, a pattern consistent with the ID having been fabricated rather than
looked up, the same failure mode already seen twice with AGROVOC
identifiers (see the two 2026-08-22 entries below). Each of the 14 was
independently re-verified by web search against the CABI Digital Library
and corrected. Also fixed: the BBPOPT source URL
(`bbpopt.ditlin.pertanian.go.id`, 7 assertions) pointed to a subdomain
that no longer resolves — corrected to the site's current domain
(`bbpopt.tanamanpangan.pertanian.go.id`). The two IRRI Rice Knowledge Bank
URLs (55 assertions) were checked and are still correct, unchanged.
Applied identically to both `provenance_axioms.rdf` and `Rice MMKG.rdf`
(the merged ontology carries its own copy of the same reified axioms).
No triples added or removed, no assertion structure changed — `dcterms:
source` object values only. **Process note:** external identifiers in
this project's provenance layer still need a live lookup before
assertion — a plausible-looking ID number is not evidence of one.

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
- ~~**Permanent identifier**~~ — `https://w3id.org/ricemmkg` registered 2026-09-16 and the namespace rewritten in 0.7.0-dev (see changelog). **Still open:** raw.githubusercontent.com serves the ontology as `text/plain` rather than `application/rdf+xml`, and the root IRI resolves to the development file on `main` rather than the latest release; both are to be settled with the HTML documentation in Phase 5.
- **Version status:** `0.7.0-dev` in `Rice MMKG.rdf` (as of 2026-09-15). Tags `v0.6.1` (commit `1d13542`) and `v0.6.2` mark the last two releases; the final number of the next release is set when it is tagged.
- **Competency Questions (CQs) Benchmark:** 25 CQs benchmarked via `cq_sparql_benchmark.py`: 0.7.0-dev scores 87.5% (21 PASS / 2 PARTIAL / 1 FAIL / 1 DOC); v0.6.1/v0.6.2 scored 95.8% (23 / 1 / 0 / 1). Full documentation in `CQ_SPARQL_Documentation.md`.
- **Automated Reasoner verified:** OWL RL deductive closure via Python `owlrl` (+95,187 triples) and HermiT consistency on 0.7.0-dev (with verified control cases).
- **Varieties, round 2.** Only IR64 and its two Indonesian derivatives are modelled, all from one source. The varieties Indonesian farmers actually grow (Ciherang, the Inpari series, Situbagendit) need their own sources: the official *Deskripsi Varietas Unggul Baru Padi* is served from `repository.pertanian.go.id`, which returns 403 to automated clients, and `bbpadi.litbang.pertanian.go.id` does not resolve, so a copy has to be obtained another way or replaced by peer-reviewed sources (e.g. the Ciherang bacterial-blight introgression work in PMC). Note the temporal problem such sources raise: Ciherang and Inpari 13 are reported to have *lost* their bacterial-blight resistance, so a plain `resistantTo` assertion would be wrong without a date. Decide how to record a resistance that has broken down before asserting any of them.
- **Variety-specific treatment needs the expert.** The expert asked for treatment that differs per variety. Round 1 covers only which variety resists what. Whether they meant "choose a resistant variety" (already expressible) or "different dosage or method per variety" (needs new modelling and a source) is still unanswered.
- ~~**Language tags on labels and comments**~~ — resolved 2026-09-17: all `rdfs:label` and `rdfs:comment` literals tagged `@en`, the two stale labels removed; CQ-24 left as defined (see changelog). Original note: 36 `rice:` literals carry no `@en` (mostly class and individual `rdfs:comment`, plus 6 labels), and 9 more sit on imported vocabulary terms. Two properties also carry two labels each, one tagged and one not: `annotatedAs` ("annotated as", "classified as"@en) and `annotationOf` ("annotation of", "classifies"@en). CQ-24 checks `evidenceType` only, so it passes. Fixing this is cheap and helps the FOOPS! score; the open question is whether CQ-24 should then be extended to all literals, with both the old and new figures reported, as CQ-22's extension was.
- **Severity → action triage: questions for the domain expert.** The six assertions removed on 2026-09-15 (see changelog) are open questions, not facts. Which action does each juknis category warrant? In particular, does *ringan* (already above the control threshold) call for monitoring or for control? Does the answer differ between diseases and pests? If the expert confirms a mapping, re-add it with `rice:evidenceType "expert-elicited"` and the elicitation date (identity kept in the gitignored notes). CQ-13 stays FAIL until then.
- ~~**CQ-01 denominator includes abiotic disorders**~~ — resolved 2026-09-15: denominator corrected to exclude diseases with an abiotic cause; 7/9 PASS, uncorrected 7/15 reported alongside (see changelog and `CQ_SPARQL_Documentation.md`).
- ~~**BBPOPT (2022) citation could not be verified**~~ — resolved 2026-09-15: triage removed, `Crop_Sanitation requires Harvest_Stage` re-sourced to IRRI, SeverityLevel aligned to the 2021 juknis as comments (see changelog). Original note: 7 assertions (the severity → ManagementAction triage: `Low_Severity recommends No_Action_Needed`, `Medium_Severity recommends Monitoring` and `Field_Inspection`, `High_Severity recommends Preventive_Action` and `Immediate_Intervention`, `Critical_Severity recommends Immediate_Intervention`; and `Crop_Sanitation requires Harvest_Stage`) cite "BBPOPT (2022). Pedoman Pengamatan dan Pengendalian OPT Tanaman Padi" with the BBPOPT homepage as source, which returns 403. Searched 2026-09-15: no document of that title was found. The closest official document, *Petunjuk Teknis Pengamatan dan Pelaporan OPT dan DPI* (Direktorat Perlindungan Tanaman Pangan, 2018; Kepdirjen TP No. 36/HK.310/C/3/2018), defines attack-intensity categories — ringan, sedang, berat, puso, with percentage bands (Tables 4–5) — and control thresholds per pest (Lampiran 3), but **does not map a category to a specific action** and does not mention sanitation at harvest. The triage assertions are therefore unsupported by any document found so far; decision pending (re-source, remodel on the juknis categories, or remove).
- **Abiotic disorders are thinly connected** — no growth stage, no ManagementAction, and control only for zinc (iron toxicity and salinity have prevention only; IRRI states no practical treatment exists); this is what moved CQ-12 to PARTIAL (9/22). Each link needs a source that states it; the N, P and K sheets give fertilizer rates by yield target rather than as a remedy.
- ~~**Nutrient excess and toxicity not modelled**~~ — iron toxicity and salinity added 2026-09-15 from the IRRI toxicity fact sheets (see changelog). IRRI lists further toxicities (aluminum, boron, manganese, sulfide, nitrogen excess) not yet modelled; add only if a source or the expert makes them relevant to Indonesian rice.
- **Potassium deficiency vs tungro** — IRRI warns the leaf symptoms can be confused (tungro occurs in patches, with more pronounced yellow-orange leaves). The two now share `Stunted_Growth`; the distinguishing field pattern is not modelled.
- **Tungro virus retention period** — Wang et al. (2022) give 4–5 days (RTBV) and 2–4 days (RTSV); IRRI says transmission within 5–7 days. Not asserted until the discrepancy is resolved.
- **Six treatments without a management category** — `Fungicide_Application` (only indirect evidence for "chemical"), `Water_Management` (physical per IRRI vs cultural per AGROVOC), `Seed_Treatment` (chemical or physical depending on method), `Neem_Based_Pesticide` (biopesticide vs plant-derived chemical), `Vector_Control` (spans categories), `Good_Agricultural_Practice` (unused). Each needs a source that places it, or — for the mixed ones — a split into separate treatments.
- ~~**`Biological_Control` (Treatment) and `Biological_Control_Category` both map to AGROVOC c_918**~~ — resolved 2026-09-15: the Treatment's mapping downgraded to `closeMatch`; only the category keeps `exactMatch`.
- **`Excessive_Tillering` has no organ** — waiting for a readable source on rice downy mildew (IRRI has no fact sheet; Lee et al. 2003 could not be read).
- ~~**`Stem_Rot_Symptom` on `Sheath_Blight`**~~ — relabelled "leaf sheath lesion" on 2026-09-15 (see changelog). The IRI was renamed to `Leaf_Sheath_Lesion` on 2026-09-17, right after the namespace rewrite and before anything was published under the new namespace, so no deprecation was needed (see changelog).
- **`Wilting` on `Sheath_Blight`, `Rice_Blast_Disease`, `Bacterial_Panicle_Blight`** — not mentioned by IRRI; the cited CABI datasheets return 403. Re-check when a readable source is found; not shown to be wrong.
- ~~**Immediate Action Items for v0.6.1**~~ — done 2026-09-14; see the v0.6.1 changelog entry.
- ~~**`provenance_axioms.rdf` has drifted**~~ — archived 2026-09-14 to `Backup/provenance_axioms.archived-2026-09-14.rdf`. `Rice MMKG.rdf` is the single source of truth; do not merge the archived file back (see the v0.6.2 entry).
- ~~**CABI source URIs redirect**~~ — replaced 2026-09-14 by DOIs (`https://doi.org/10.1079/cabicompendium.<id>`), each checked live.
- ~~**CABI citation years**~~ — resolved 2026-09-14: all CABI citation segments rewritten from Crossref metadata (see the v0.6.2 entry).
