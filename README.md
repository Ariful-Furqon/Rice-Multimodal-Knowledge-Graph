# Rice MMKG — Rice Multimodal Knowledge Graph

An OWL 2 ontology and multimodal knowledge graph modeling rice diseases, pests, pathogens, symptoms, environmental factors, growth stages, treatments, and management actions — populated from a large public image dataset, with sensor and text modalities designed in as declared extension points.

![Rice MMKG diagram](RiceMMKG.png)

## Overview

Rice MMKG links agronomic, pathological, and entomological knowledge about rice cultivation into a single queryable graph, connecting what is *observed* (currently: 10,407 field images; sensor readings and field/text reports are declared extension points) to its *cause* (pathogens, pests, environmental stressors) and the *response* (treatments, management actions), contextualised by crop growth stage and severity level.

### Core Design Principles

- **Observation is kept separate from domain knowledge.** An `ImageObservation`'s raw dataset label (`annotatedAs`) is never conflated with curated symptom/cause/treatment relations (`captures`, `causes`, `indicatedBy`, ...) — what was recorded by computer vision is distinct from what is concluded by domain knowledge.
- **Every domain-level assertion is traceable.** All 347 populated domain triples (`causes`, `indicatedBy`, `occursIn`, `controlledBy`, `preventedBy`, `increaseRiskOf`, `vulnerableTo`, `recommends`, `requires`, `transmits`, `affectsPlantPart`, `partOf`, `hasTransmissionMode`, `hasManagementCategory`, `varietyOf`) are reified with `owl:Axiom` and carry `dcterms:source`, `dcterms:bibliographicCitation`, and `rice:evidenceType` — **100% provenance coverage as of v0.6.1**, checked by CQ-22 (assertions without an axiom) as well as CQ-21 (axioms without a source). v0.6 fell two assertions short of this; see the v0.6.1 note in [`Ontology_Overview.md`](Ontology/Ontology_Overview.md).
- **Formal reasoning & falsifiable Competency Questions.** Evaluated under automated Description Logic (HermiT/Pellet) and rule-based (OWL RL) reasoning across 25 schema-level Competency Questions without permissive `OPTIONAL` clauses.

### Metadata Snapshot

- **Namespace:** `https://w3id.org/ricemmkg#` — permanent identifier, live since 2026-09-16; version IRIs `https://w3id.org/ricemmkg/<version>` (releases up to v0.6.2 used `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#`)
- **Format:** OWL/XML (`.rdf`), fully compatible with [Protégé](https://protege.stanford.edu/)
- **Version:** `0.7.0-dev` on `main` (in development; last release `v0.6.2`, 2026-09-15; git tags `v0.6.1`, `v0.6.2`; v0.6 released 2026-09-03) — actively progressing toward the **ESWC 2027 Resource Track** (see [`Ontology/riceMMKG_ESWC_plan.md`](Ontology/riceMMKG_ESWC_plan.md))
- **Triples:** **68,049** asserted triples / **163,684** materialised triples under OWL RL (+95,635 inferred triples); v0.6.2: 66,802 / 161,447
- **Reasoner Consistency:** **100% Consistent** in HermiT & Pellet (0 unsatisfiable classes, 0 disjointness conflicts)

---

## Ontology Structure

### Classes (16)

| Class | Individuals | Description |
|---|---:|---|
| `ImageObservation` | 10,407 | Paddy Doctor field image instances |
| `SymptomaticObservation` | *(1,442 materialised)* | Defined class (`Observation that captures some Symptom`) — populated via OWL reasoning |
| `SensorObservation` | 0 | Declared scaffolding for microclimate & IoT sensor telemetry (Phase 3) |
| `Observation` | 0 | Abstract root observation superclass |
| `Dataset` (`dcat:Dataset`) | 1 | Metadata individual for the Paddy Doctor image collection |
| `Disease` | 9 | Diagnostic entities & damage conditions (including `Deadheart`, Bacterial Leaf Blight, Rice Blast, Tungro) |
| `Pest` | 7 | Insect pests and vectors (Stem Borer, Leaf Folder, Brown Planthopper, Armyworm, Rice Bug, Hispa, Green Leafhopper) |
| `Pathogen` | 8 | Microbial causal agents (Magnaporthe Oryzae, Xanthomonas pathovars, RTBV, RTSV) |
| `Plant` | 1 | The host crop (*Oryza sativa*) |
| `HealthStatus` | 1 | Non-disease reference baseline (`Normal_Health`) |
| `Symptom` | 27 | Visual symptoms (Leaf Rolling, Dead Tiller, White Ear, Brown Lesion, Wilting, etc.) |
| `GrowthStage` | 7 | Rice phenological stages (Seedling, Tillering, Vegetative, Reproductive, Flowering, Maturity, Harvest) |
| `EnvironmentalFactor` | 9 | Predisposing weather & field conditions (High Humidity, Waterlogged Soil, Dense Canopy, etc.) |
| `SeverityLevel` | 4 | Severity levels (Low, Medium, High, Critical), each annotated with the matching attack-intensity category of the 2021 Indonesian pest-observation guideline; no severity → action mapping is asserted (0.7.0-dev) |
| `Treatment` | 12 | Practical interventions (Fungicide/Insecticide Application, Biological Control, Resistant Variety, Crop Rotation) |
| `ManagementAction` | 5 | Operational actions (Field Inspection, Monitoring, Immediate Intervention, Preventive Action, No Action Needed) |

### Object Properties (26)

Relations connect the domain entities with defined domains, ranges, and inverse pairs:
`causes`/`causedBy`, `transmits`/`transmittedBy`, `threatens`, `indicates`/`indicatedBy`, `controls`/`controlledBy`, `prevents`/`preventedBy`, `recommends`/`recommendedFor`, `requires`/`requiredFor`, `captures`/`capturedBy`, `detects`/`detectedBy`, `occursIn`, `hasOccurrenceOf`, `increaseRiskOf`/`riskIncreasedBy`, `vulnerableTo`, `annotatedAs`/`annotationOf`.

*Epidemiological distinction:* `causes` is strictly scoped to `Pathogen → Disease`, while insect vector transmission is modeled through `transmits`/`transmittedBy` (`Pest → Pathogen`), enabling explicit graph traversal from vector to pathogen to disease.

### Datatype Properties (5)

`confidenceScore`, `severityScore`, `interventionThreshold`, `observationDate`, `sourceDatasetLabel`

### Individuals & Provenance

- **10,562 named individuals**: 10,407 `ImageObservation` instances, 1 dataset metadata individual, plus 154 domain entities (0.7.0-dev).
- **347 reified domain axioms** over 347 domain assertions: every assertion backed by an `owl:Axiom` record with `dcterms:source`, `dcterms:bibliographicCitation`, and `rice:evidenceType`. Source URIs: CABI Compendium 242 (as `doi.org/10.1079/cabicompendium.*` DOIs), IRRI Rice Knowledge Bank 88, Mackill & Khush (2018) 3, AGROVOC 4, IRAC 2, Plant Ontology 2, Wang et al. (2022) 2, Bagariang et al. (2021) 2, Biswas et al. (2021) 1, FAO 1. The 15 resistance assessments carry the same three annotations on the assessment itself.
- **Vector transmission mode (0.7.0-dev):** both tungro viruses are recorded as semi-persistently transmitted (`hasTransmissionMode`), citing Wang et al. (2022).
- **Abiotic causes (0.7.0-dev):** nitrogen, phosphorus, potassium and zinc deficiency, and on the excess side iron toxicity and salinity, are modelled as `AbioticFactor`s that cause disorders, with symptoms from the IRRI Rice Knowledge Bank fact sheets — so abiotic factors, like pathogens, end at a Disease.
- **Varieties (0.7.0-dev):** `IR64`, `Angke` and `Conde` (bred from IR64), `Ciherang`, `Inpari_32` and `Inpari_33`. Each reported grade is a `ResistanceAssessment` naming the variety, the disease or pest, the grade (resistant, moderately resistant, susceptible), the tested biotype, race or population, the year and its own source — 15 assessments from Mackill & Khush (2018), Bagariang et al. (2021) and Biswas et al. (2021). Conflicting grades stay side by side, and a resistance that broke down shows as assessments from different years.
- **Management categories (0.7.0-dev):** treatments are classed as chemical, biological, cultural or host-plant-resistance control (`hasManagementCategory`, categories from AGROVOC) where a source places them unambiguously.
- **Plant anatomy (0.7.0-dev):** 8 `PlantPart` individuals aligned to the Plant Ontology; each symptom linked to the organ it affects (`affectsPlantPart`), with `partOf` where the Plant Ontology records it.
- **External Alignment**: 33 `skos:exactMatch`, 17 `skos:closeMatch`, 1 `skos:broadMatch` to AGROVOC, NCBI Taxonomy, and EPPO identifiers, verified via live API checks.

### Paddy Doctor Dataset Alignment

The local Paddy Doctor image dataset is excluded from Git (`/Data/`). Folder labels are cleanly preserved via `sourceDatasetLabel`/`annotatedAs`.

| Paddy Doctor Label | Rice MMKG Entity | Semantic Type in v0.6 | Observed Symptom (`captures`) |
|---|---|---|---|
| `bacterial_leaf_blight` | `Bacterial_Leaf_Blight` | Disease | — (class-level annotation) |
| `bacterial_leaf_streak` | `Bacterial_Leaf_Streak` | Disease | — (class-level annotation) |
| `bacterial_panicle_blight` | `Bacterial_Panicle_Blight` | Disease | — (class-level annotation) |
| `blast` | `Rice_Blast_Disease` | Disease | — (class-level annotation) |
| `brown_spot` | `Brown_Spot` | Disease | — (class-level annotation) |
| `downy_mildew` | `Downy_Mildew` | Disease | — (class-level annotation) |
| `tungro` | `Rice_Tungro_Disease` | Disease | — (class-level annotation) |
| `hispa` | `Hispa` | Pest | — (class-level annotation) |
| `dead_heart` | `Deadheart` | Disease (Damage condition) | `Dead_Tiller` (Symptom, 1,442 images) |
| `normal` | `Normal_Health` | HealthStatus | — (reference baseline) |

---

## Competency Question (CQ) SPARQL Benchmark

Rice MMKG incorporates an automated verification harness (`cq_sparql_benchmark.py`) based on **25 Competency Questions** structured across:
- **Reasoning Depth (L1–L4):** L1 Factual (1-hop), L2 Contextual (multi-criteria joins), L3 Causal (multi-hop chains), L4 Inferential (OWL RL deduction).
- **Knowledge Dimensions (D1–D3):** D1 Agronomic/Symbolic, D2 Cross-modal Grounding, D3 Provenance & External Alignment.
- **Evaluation Modes:** `coverage` (≥ 50%), `negative` (0 violations), `entailment` (entailed > asserted), `documented` (declared extension point).

### Benchmark Summary (0.7.0-dev)

```
================================================================
  PASS      22 / 24  (91.7% Pass Rate)
  PARTIAL    2 / 24  (CQ-12 Management Layer: 45%; CQ-18 Symptom Visual Grounding: 3%)
  FAIL       0 / 24
  DOC        1 / 25  (CQ-20 Sensor Observation Extension Point)
================================================================
```

v0.6.1 and v0.6.2 score 23 PASS / 1 PARTIAL / 0 FAIL / 1 DOC. In 0.7.0-dev CQ-12 fell to PARTIAL when four nutrient-deficiency disorders — sourced, but with no ManagementAction in their source — joined its denominator; it was not lifted by adding unsupported assertions. The released v0.6 file scores 21 PASS / 1 PARTIAL / 2 FAIL / 1 DOC (CQ-10, CQ-24). Under the extended CQ-22 (2026-09-14), which also flags domain assertions carrying no provenance axiom, v0.6 has a third failure: two `Stem_Borer indicatedBy` assertions were never reified. v0.6.1 fixes all three.

- Complete documentation with exact SPARQL queries: [`Ontology/CQ SPARQL Benchmark/CQ_SPARQL_Documentation.md`](Ontology/CQ%20SPARQL%20Benchmark/CQ_SPARQL_Documentation.md)
- Automated execution report: [`Ontology/CQ SPARQL Benchmark/CQ_SPARQL_Benchmark_Report.md`](Ontology/CQ%20SPARQL%20Benchmark/CQ_SPARQL_Benchmark_Report.md)

---

## Roadmap Toward ESWC 2027

Our six-phase development roadmap toward the **ESWC 2027 Resource Track** is detailed in [`Ontology/riceMMKG_ESWC_plan.md`](Ontology/riceMMKG_ESWC_plan.md) (revised 2026-09-14):

1. **Phase 1: Functional & Reasoning Evaluation (Weeks 1–2, Sept) — [done: v0.6.1]**  
   25 benchmark CQs (95.8% pass rate, 0 FAIL), 19 of 25 elicited CQs queried against a frozen baseline, HermiT consistency, OWL RL materialisation.
2. **Phase 2: Namespace & Release Scaffolding → v0.7 (Weeks 3–4, Sept)**  
   Register the w3id PURL and rewrite the namespace early, before more artefacts embed the old IRIs; close the maintenance plan; send the expert questionnaire and image annotation sample; release v0.7.0.
3. **Phase 3: Modality Checkpoint, Grounding & Schema → v0.8 (Weeks 5–8, Late Sept & Oct)**  
   Decide whether sensor and genomic data enter the submission (open decision); symptom-level image grounding from expert annotation; literature-backed schema (plant part, transmission mode, management category).
4. **Phase 4: Expert Validation & Analysis → v0.9 with Phase 5 (Late Oct & Early Nov)**  
   Ordinal agreement (weighted κ / Krippendorff's α) on the elicited CQs, independent second screener, separate roadmap-tier instrument.
5. **Phase 5: Availability & FAIR Finalisation → v0.9 (Early–Mid Nov)**  
   pyLODE/Widoco documentation at the PURL, FOOPS!/OOPS!, Zenodo DOI and AgroPortal for the final release.
6. **Phase 6: Resource Paper & Submission → v1.0 (Mid Nov – Early Dec)**  
   Manuscript, reproducibility package, submission to ESWC 2027.

---

## Repository Contents

```
MAINTENANCE.md                   # Maintainers, contact, versioning and release process
w3id/ricemmkg/                   # w3id.org redirect files (.htaccess, README.md)
Ontology/
  Rice MMKG.rdf                  # Master ontology file (OWL/XML), 0.7.0-dev
  Rice MMKG.properties           # Protégé project preferences
  Ontology_Overview.md           # Comprehensive structure, statistics, and full changelog
  riceMMKG_ESWC_plan.md          # 5-phase master roadmap toward ESWC 2027 submission
  Backup/                        # Preserved backups (v0.2 through v0.6 pre-v0.6.1)
  CQ SPARQL Benchmark/
    cq_sparql_benchmark.py       # Automated Python/rdflib/owlrl benchmark runner
    cq_sparql_benchmark_results.json # Full machine-readable test results
    CQ_SPARQL_Benchmark_Report.md    # Formatted execution benchmark report
    CQ_SPARQL_Documentation.md      # Standalone CQ documentation with all 25 SPARQL queries
Analysis and Alignment/
    AGROVOC_alignment.md         # Vocabulary alignment to FAO AGROVOC
    NCBI_Taxonomy_alignment.md   # Organism-level alignment to NCBI Taxonomy
    Planteome_alignment.md       # Environmental factor alignment to Plant Ontologies
    PaddyDoctor_Dataset_Analysis.md # Dataset profile and ingestion strategy
Data/                            # Local image dataset (gitignored)
Worklog/                         # Internal cleanup and task logs (gitignored)
```

---

## Quick Start & Verification

### In Protégé
1. Open `Ontology/Rice MMKG.rdf` in Protégé 5.x.
2. Select **`Reasoner` → `HermiT`** (or `Pellet`).
3. Press **`Ctrl + R`** (`Start reasoner`). The reasoner will confirm global consistency (0 unsatisfiable classes) and classify 1,442 images under `SymptomaticObservation`.

### Programmatic SPARQL Benchmark via Python
Run the automated benchmark suite with OWL RL deductive closure:

```bash
python "Ontology/CQ SPARQL Benchmark/cq_sparql_benchmark.py"
```

```python
import rdflib

g = rdflib.Graph()
g.parse("Ontology/Rice MMKG.rdf", format="xml")
print(f"Asserted triples loaded: {len(g)}")
```

---

## Citation & License

- **License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- **Author:** Muhammad Ariful Furqon (ORCID: [0000-0002-1031-3567](https://orcid.org/0000-0002-1031-3567)), Natthawut Kertkeidkachorn (ORCID: [0000-0003-4527-776X](https://orcid.org/0000-0003-4527-776X))
Rice MMKG is released under a **Dual-Licensing** framework:
- **Software, Benchmark Scripts, & Tooling:** [MIT License](LICENSE#part-1-mit-license-software-scripts-and-benchmark-tooling) — open and permissive for programmatic reuse and automation.
- **Ontology Specification & Knowledge Graph Data:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE#part-2-creative-commons-attribution-4-0-international-cc-by-40) — adhering to FAIR data principles for academic and agronomic research.

- **Authors & Curators:** Muhammad Ariful Furqon (ORCID: [0000-0002-1031-3567](https://orcid.org/0000-0002-1031-3567)), Natthawut Kertkeidkachorn (ORCID: [0000-0003-4527-776X](https://orcid.org/0000-0003-4527-776X))
<!-- - **Cite as:**
  ```bibtex
  @misc{ricemmkg_2026,
    title  = {Rice MMKG: A Multimodal Knowledge Graph and Domain Ontology for Rice Disease and Pest Diagnosis},
    author = {Muhammad Ariful Furqon and Natthawut Kertkeidkachorn},
    year   = {2026},
    note   = {Version 0.6, evaluated with 25 Competency Questions and OWL RL reasoning}
  }
  ``` -->
