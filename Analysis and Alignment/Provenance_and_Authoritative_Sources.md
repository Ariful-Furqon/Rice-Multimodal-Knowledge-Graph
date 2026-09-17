# Provenance and Authoritative Sources Register (Dimension D3)

## 1. Purpose and Scope

This register documents the provenance architecture, literature grounding, and external vocabulary alignment of **Rice MMKG v0.6.2** (`owl:versionInfo 0.6.2`). All counts below were measured on `Ontology/Rice MMKG.rdf` with rdflib on 2026-09-14; v0.6.2 changed only source URIs and citation text, so they are unchanged.

In Semantic Web resource evaluations (such as the ESWC Resource Track), a key differentiator between an arbitrary graph and a published **scientific resource** is **defensibility and auditability**:
1. *Every domain assertion must be traceable to a citable authoritative source.*
2. *Raw dataset observations must be strictly distinguished from curated domain knowledge.*
3. *Biological entities must be anchored to canonical registries (EPPO, AGROVOC, NCBI Taxonomy).*

In Rice MMKG v0.6.1, **all 256 domain relation assertions are reified** via `owl:Axiom` with a source URI, a bibliographic citation, and an evidence type — 256 axioms, 0 orphans, 0 duplicates.

> **Correction (2026-09-14).** Earlier versions of this register stated "100% of domain relation assertions (265/265)". That figure was measured before the v0.6 inconsistency fix; the released v0.6 file had 253 axioms over 255 assertions, i.e. two assertions (`Stem_Borer indicatedBy Dead_Tiller` / `White_Ear`) had no provenance. They were reified in v0.6.1. See `Ontology/Ontology_Overview.md`, v0.6.1 entry.

---

## 2. Three-Layer Provenance Architecture

```
Layer 1: Dataset & Media Provenance (W3C PROV-O & Schema.org)
   └── 10,407 ImageObservations ──[prov:wasDerivedFrom]──> PaddyDoctorDataset (dcat:Dataset)
   └── 10,407 ImageObservations ──[schema:contentUrl]───> Relative image paths

Layer 2: Axiom-Level Literature Grounding (OWL 2 Axiom Reification)
   └── 256 Domain Triples ──[owl:Axiom]──┬──[dcterms:source]──────────────> Source URI (DOI where one exists)
                                         ├──[dcterms:bibliographicCitation]─> Formal citation
                                         └──[rice:evidenceType]────────────> "literature-curated"@en

Layer 3: Cross-Vocabulary Alignment (SKOS & Bio-Registries)
   └── Entities ──[skos:exactMatch 33 / closeMatch 17 / broadMatch 1]──> FAO AGROVOC / NCBI Taxonomy / PECO
   └── Organism Individuals ──[rice:eppoCode]──────────────────────────> EPPO Global Database (15 codes)
```

---

## 3. Inventory of Authoritative Sources

Counts are by the host of each axiom's `dcterms:source` URI. An axiom has exactly one source URI; its citation may additionally name a co-source (e.g. "… / IRRI (2020). Rice Doctor: Stem Borer."), which is not counted separately here.

| Source | Role in Rice MMKG | Source URI form | Axioms |
|---|---|---|:---:|
| **CABI Compendium** (formerly Crop Protection Compendium) | Pest/pathogen biology, host ranges, environmental risk factors, chemical/cultural control | `https://doi.org/10.1079/cabicompendium.<id>` (14 datasheets) | **242** |
| **BBPOPT Kementan RI** (Balai Besar Peramalan Organisme Pengganggu Tumbuhan) | National pest forecasting, surveillance, and intervention guidance | `https://bbpopt.tanamanpangan.pertanian.go.id/` | **7** in v0.6.2 — **0 since 0.7.0-dev (2026-09-15):** the cited "Pedoman … Tanaman Padi (2022)" was never found and the homepage returns 403. The six severity → action assertions were removed (no document supports them) and `Crop_Sanitation requires Harvest_Stage` now cites the IRRI tungro fact sheet. See §5.2. |
| **IRRI Rice Knowledge Bank** | Field symptomatology, growth stages, IPM guidance, nutrient and toxicity disorders, causal pathogens | `http://www.knowledgebank.irri.org/...` | **4** in v0.6.2; **89** in 0.7.0-dev |
| **IRAC** (Insecticide Resistance Action Committee) | Stem borer damage symptoms (deadheart, whitehead) | `https://irac-online.org/documents/yellow-rice-stem-borer-irm/` | **2** |
| **FAO / International Rice Commission** | Tungro vector management (resistant varieties) | `https://www.fao.org/4/y6159t/y6159t02.htm` | **1** |
| **Mackill & Khush (2018)**, Rice 11:18 | Variety reactions: IR64's resistances, its tungro and iron-toxicity susceptibility, and the Indonesian varieties Angke and Conde bred from it | `https://doi.org/10.1186/s12284-018-0208-3` | **3** (`varietyOf`; 12 on 2026-09-16, of which 9 became resistance assessments on 2026-09-17) + **10 assessments** |
| **Bagariang et al. (2021)**, SEAS 5(2):79–87 | Brown planthopper reaction of IR64, Ciherang, Inpari 32 and Inpari 33 against Javanese populations | `https://doi.org/10.22225/seas.5.2.3913.79-87` | **2** (`varietyOf`, 0.7.0-dev) + **4 assessments** |
| **Biswas et al. (2021)**, Plants 10:2048 | Ciherang's susceptibility to bacterial blight races | `https://doi.org/10.3390/plants10102048` | **1** (`varietyOf`, 0.7.0-dev) + **1 assessment** |
| **Wang et al. (2022)** | Vector transmission mode of both tungro viruses | DOI | **2** (0.7.0-dev) |
| **Total** | | | **256** in v0.6.2; **348** in 0.7.0-dev (IRRI rises to 89 with the fact-sheet rounds, AGROVOC 4 and Plant Ontology 2 join as `ontology-derived`), plus **15** `ResistanceAssessment` individuals that carry `dcterms:source`, citation and evidence type on themselves |

### CABI datasheets cited

Citation text for every CABI axiom is taken from the Crossref record of its DOI (rewritten 2026-09-14; previously every entry read "CABI (2022) … Crop Protection Compendium", which the DOI metadata does not support).

| Datasheet id | Citation (Crossref) |
|---|---|
| 14493 | CABI (2021). *Cnaphalocrocis medinalis* (rice leaf folder). CABI Compendium. |
| 14691 | Castell Miller, C. (2025). *Bipolaris oryzae* (brown leaf spot of rice). CABI Compendium. |
| 27270 | CABI (2021). *Dicladispa armigera* (rice hispa). CABI Compendium. |
| 30366 | CABI (2021). *Leptocorisa oratorius* (slender rice bug). CABI Compendium. |
| 36301 | CABI (2021). *Nilaparvata lugens* (brown planthopper). CABI Compendium. |
| 44964 | CABI (2021). *Burkholderia glumae* (bacterial grain rot). CABI Compendium. |
| 45093 | CABI (2021). *Mythimna separata* (paddy armyworm). CABI Compendium. |
| 46103 | CABI (2021). *Magnaporthe oryzae* (rice blast disease). CABI Compendium. |
| 47203 | Back, M. (2012). *Thanatephorus cucumeris* (many names, depending on host). CABI Compendium. |
| 47654 | CABI (2019). Rice tungro disease (rice tungro virus). CABI Compendium. |
| 49009 | CABI (2021). *Scirpophaga incertulas* (yellow stem borer). CABI Compendium. |
| 49243 | CABI (2019). *Sclerophthora macrospora* (downy mildew). CABI Compendium. |
| 56956 | CABI (2021). *Xanthomonas oryzae* pv. *oryzae* (rice leaf blight). CABI Compendium. |
| 56977 | CABI (2021). *Xanthomonas oryzae* pv. *oryzicola* (bacterial leaf streak of rice). CABI Compendium. |

All published by CABI Publishing; DOI `10.1079/cabicompendium.<id>`.

### Other literature cited
- **Ou, S.H. (1985).** *Rice Diseases* (2nd ed.). Commonwealth Mycological Institute, Kew, UK.
- **Hibino, H. (1996).** Biology and epidemiology of rice viruses. *Annual Review of Phytopathology*, 34, 249–274. *(Nephotettix virescens → RTBV/RTSV transmission.)*
- **Ham, J.H., Melanson, R.A., & Rush, M.C. (2011).** *Burkholderia glumae*: next major pathogen of rice? *Molecular Plant Pathology*, 12(4), 329–339.
- **Gallagher, K.D., Ooi, P.A.C., Mew, T.W., Borromeo, E. & Kenmore, P.E. (2002).** Integrated pest management in rice. *International Rice Commission Newsletter*. FAO. *(Resistant varieties for tungro/leafhopper management.)*
- **IRAC (2025).** *Rice Stem Borer, Scirpophaga incertulas (yellow rice stem borer): Sustainable Control Strategies in Asia.* Poster, version 2. *(Deadheart and whitehead symptoms.)*

---

## 4. Reified Domain Properties Breakdown

The 256 `owl:Axiom` records cover 10 domain object properties — every asserted domain relation in the graph:

| Property | Subject Class → Object Class | Axioms |
|---|---|:---:|
| `rice:vulnerableTo` | `Plant ⊔ GrowthStage` → `Disease ⊔ Pest ⊔ Pathogen` | **55** |
| `rice:indicatedBy` | `Disease ⊔ Pest` → `Symptom` | **43** |
| `rice:controlledBy` | `Disease ⊔ Pest` → `Treatment` | **42** |
| `rice:occursIn` | `Disease ⊔ Pest ⊔ HealthStatus` → `GrowthStage` | **41** |
| `rice:increaseRiskOf` | `EnvironmentalFactor` → `Disease ⊔ Pest` | **29** |
| `rice:recommends` | `Disease ⊔ Pest ⊔ SeverityLevel` → `ManagementAction` | **23** |
| `rice:causes` | `Pathogen` → `Disease` | **8** |
| `rice:preventedBy` | `Disease ⊔ Pest` → `Treatment` | **8** |
| `rice:requires` | `Treatment` → `GrowthStage` | **5** |
| `rice:transmits` | `Pest` → `Pathogen` | **2** |
| **Total** | | **256** |

---

## 5. Audit & Quality Assurance History

### 5.1 CABI source URIs
- **2026-08-25:** a provenance audit found that all 14 distinct CABI datasheet ids then in use redirected to unrelated species (e.g. the *Magnaporthe oryzae* citation resolved to an oak tree). Each was re-verified and corrected.
- **2026-09-14:** the 14 corrected ids were re-checked live. `https://www.cabi.org/isc/datasheet/<id>` now returns **301** to `cabidigitallibrary.org/doi/10.1079/cabicompendium.<id>`, so all 242 source URIs were replaced by the DOI form; each DOI resolves through doi.org and its Crossref title names the organism in the citation. Citation text was rewritten from Crossref at the same time (§3).
- *Correction:* an earlier version of this register listed "corrected" ids 46154, 49132 and 56947 and stated that "all 247 CABI assertions point to valid, 200-OK HTTP resources". Neither holds: the ids in the ontology are 46103, 49009 and 56956, the count was 247 only before the v0.6 fix, and the old URLs redirect rather than return 200.

### 5.2 BBPOPT domain update
- Legacy URL `bbpopt.ditlin.pertanian.go.id` updated to the active domain `bbpopt.tanamanpangan.pertanian.go.id`.
- **2026-09-15 (0.7.0-dev): BBPOPT source withdrawn.** The seven assertions citing "BBPOPT (2022). Pedoman Pengamatan dan Pengendalian OPT Tanaman Padi" could not be traced: no document of that title was found, and the homepage returns 403. Two official guidelines were read instead — *Petunjuk Teknis Pengamatan dan Pelaporan OPT dan DPI* (Kepdirjen TP No. 36/HK.310/C/3/2018) and its 2021 revision (Kepdirjen TP No. 127/HK.310/C/5/2021). Both define attack-intensity categories (ringan, sedang, berat, puso) with percentage bands and per-pest control thresholds, but neither maps a category to an action or mentions sanitation at harvest; "ringan" already lies above the control threshold, which contradicts `Low_Severity recommends No_Action_Needed`. Outcome: the six severity → ManagementAction assertions and their axioms were **removed** (kept as questions for the domain expert; see `Ontology_Overview.md` open items); the four `SeverityLevel` individuals carry the 2021 category and bands as `rdfs:comment` only, with disease and pest bands kept apart; `Crop_Sanitation requires Harvest_Stage` was **re-sourced** to the IRRI tungro fact sheet ("Plow infected stubbles immediately after harvest", checked live). The juknis is cited by SK number, not by URL: the only online copy found was an unofficial mirror.

### 5.3 EPPO codes (15)
- Pathogens: `PYRIOR` (*Magnaporthe oryzae*), `XANTOR` (*X. oryzae* pv. *oryzae*), `XANTTO` (*X. oryzae* pv. *oryzicola*), `COCHMI` (*Bipolaris oryzae*), `PSDMGM` (*Burkholderia glumae*), `SCPHMA` (*Sclerophthora macrospora*), `RTBV00` (RTBV), `RTSV00` (RTSV).
- Pests: `SCHOBI` (*Scirpophaga incertulas* / Stem Borer), `CNAPME` (*Cnaphalocrocis medinalis*), `NILALU` (*Nilaparvata lugens*), `PSEDSE` (*Mythimna separata*), `LEPROR` (*Leptocorisa oratorius*), `HISPAR` (*Dicladispa armigera*), `NEPHIM` (*Nephotettix virescens*).

### 5.4 v0.6.1 provenance gaps (2026-09-14)
- `Stem_Borer indicatedBy Dead_Tiller` and `Stem_Borer indicatedBy White_Ear` had been asserted since v0.6 without an axiom; now reified citing IRAC (2025).
- `Nephotettix_Virescens controlledBy Resistant_Variety` added with an axiom citing Gallagher et al. (2002).
- The one untagged `rice:evidenceType` literal is now `@en`.
- `Ontology/provenance_axioms.rdf`, an intermediate from the 2026-08-21 provenance pass that had drifted from the main file, was archived to `Ontology/Backup/`. `Rice MMKG.rdf` is the single source of truth.

### 5.5 Dataset source attribution
- `PaddyDoctorDataset` cites Petchiammal, A., Briskline Kiruba, S., Murugan, D. & Pandarasamy, A. (2022), *Paddy Doctor: A visual image dataset for automated paddy disease classification and benchmarking*, arXiv:2205.11108, CC BY 4.0, with the Kaggle competition URI as `dcterms:source`.

---

## 6. Competency Question (SPARQL) Verification

The provenance layer (Knowledge Dimension D3) is evaluated by the 25-CQ benchmark (`Ontology/CQ SPARQL Benchmark/cq_sparql_benchmark.py`).

### CQ-21 | L4 × D3 | Provenance completeness of existing axioms (PASS: 256/256)
```sparql
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT DISTINCT ?ax WHERE {
  ?ax a owl:Axiom ;
      dcterms:source ?src ;
      dcterms:bibliographicCitation ?cit .
}
```
*Scope limit:* the denominator is the set of axioms, so CQ-21 cannot see an assertion that has no axiom at all. CQ-22 covers that case.

### CQ-22 | L4 × D3 | Assertions without provenance, or axioms with incomplete provenance (PASS: 0 violations)
Extended 2026-09-14. Runs on the asserted graph.
```sparql
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rice:    <https://w3id.org/ricemmkg#>

SELECT ?item ?problem WHERE {
  {
    ?item a owl:Axiom .
    FILTER ( NOT EXISTS { ?item dcterms:source ?s } ||
             NOT EXISTS { ?item dcterms:bibliographicCitation ?c } ||
             NOT EXISTS { ?item rice:evidenceType ?e } )
    BIND ("axiom with incomplete provenance" AS ?problem)
  } UNION {
    VALUES ?p { rice:causes rice:transmits rice:indicatedBy rice:occursIn
                rice:controlledBy rice:preventedBy rice:increaseRiskOf
                rice:vulnerableTo rice:recommends rice:requires }
    ?s ?p ?o .
    FILTER NOT EXISTS { ?ax owl:annotatedSource ?s ;
                            owl:annotatedProperty ?p ;
                            owl:annotatedTarget ?o }
    BIND (CONCAT(STRAFTER(STR(?s), "#"), " ", STRAFTER(STR(?p), "#"), " ",
                 STRAFTER(STR(?o), "#")) AS ?item)
    BIND ("assertion without provenance" AS ?problem)
  }
}
```
*Result:* 0 violations on v0.6.1. On the released v0.6 file: 2 violations (the two `Stem_Borer indicatedBy` assertions); the original axiom-only form of this query reported 0 there.

### CQ-24 | L4 × D3 | Literal hygiene (PASS: 0 violations)
```sparql
PREFIX rice: <https://w3id.org/ricemmkg#>

SELECT ?ax ?v WHERE {
  ?ax rice:evidenceType ?v .
  FILTER ( lang(?v) = "" )
}
```
*Result:* 0 violations on v0.6.1 (v0.6: 1, fixed by tagging the literal `@en`).
