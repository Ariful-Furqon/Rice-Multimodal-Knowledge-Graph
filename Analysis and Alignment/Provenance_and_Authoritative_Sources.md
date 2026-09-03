# Provenance and Authoritative Sources Register (Dimension D3)

## 1. Purpose and Scope

This register documents the formal provenance architecture, authoritative literature grounding, and external vocabulary alignment implemented in **Rice MMKG v0.6**. 

In Semantic Web resource evaluations (such as the ESWC Resource Track), a key differentiator between an arbitrary graph and a published **scientific resource** is **defensibility and auditability**:
1. *Every domain assertion must be traceable to a citable authoritative source.*
2. *Raw dataset observations must be strictly distinguished from curated domain knowledge.*
3. *Biological entities must be anchored to canonical registries (EPPO, AGROVOC, NCBI Taxonomy).*

In Rice MMKG, **100% of domain relation assertions (265/265)** are formally reified via `owl:Axiom` with complete bibliographic citations, source URIs, and evidence typing.

---

## 2. Three-Layer Provenance Architecture

```
Layer 1: Dataset & Media Provenance (W3C PROV-O & Schema.org)
   └── 10,407 ImageObservations ──[prov:wasDerivedFrom]──> PaddyDoctorDataset (dcat:Dataset)
   └── 10,407 ImageObservations ──[schema:contentUrl]───> Verified relative image paths

Layer 2: Axiom-Level Literature Grounding (OWL 2 Axiom Reification)
   └── 265 Domain Triples ──[owl:Axiom]──┬──[dcterms:source]──────────────> Authoritative Source URI
                                         ├──[dcterms:bibliographicCitation]─> Formal Academic Citation
                                         └──[rice:evidenceType]────────────> "literature-curated"

Layer 3: Cross-Vocabulary Alignment (SKOS & Bio-Registries)
   └── Biological Entities ──[skos:exactMatch / closeMatch]──> FAO AGROVOC / NCBI Taxonomy
   └── Organism Individuals ──[rice:eppoCode]───────────────> EPPO Global Database (15 validated codes)
```

---

## 3. Inventory of Authoritative Sources

All 265 reified domain axioms trace back to three authoritative institutional bodies and seminal peer-reviewed agronomic literature:

| Source Institution / Body | Role in Rice MMKG | Domain URL / PURL | Axiom Count |
|---|---|---|:---:|
| **CABI Compendium** (Crop Protection Compendium) | Primary reference for global pest/pathogen biology, host ranges, environmental risk factors, and chemical/cultural control | `https://www.cabi.org/isc/datasheet/...` | **247** |
| **IRRI Rice Knowledge Bank** (International Rice Research Institute) | Authoritative reference for diagnostic field symptomatology, rice growth stages, and Integrated Pest Management (IPM) guidelines | `http://www.knowledgebank.irri.org/...` | **11** |
| **BBPOPT Kementan RI** (Balai Besar Peramalan Organisme Pengganggu Tumbuhan) | National standard for tropical rice pest forecasting, crop surveillance, and emergency intervention thresholds | `http://bbpopt.tanamanpangan.pertanian.go.id/...` | **7** |
| **Total Reified Domain Axioms** | | | **265 (100%)** |

### Seminal Peer-Reviewed Literature Cited
- **Ou, S.H. (1985).** *Rice Diseases* (2nd ed.). Commonwealth Mycological Institute, Kew, Surrey, UK. *(Standard international treatise for rice fungal and bacterial pathologies).*
- **Hibino, H. (1996).** Biology and epidemiology of rice viruses. *Annual Review of Phytopathology*, 34(1), 249-274. *(Foundation for the Nephotettix virescens → RTBV/RTSV vector transmission chain).*
- **Ham, J.H., Melanson, R.A., & Rush, M.C. (2011).** *Burkholderia glumae*: next major pathogen of rice? *Molecular Plant Pathology*, 12(4), 329-339. *(Foundation for bacterial panicle blight etiology and temperature risk).*

---

## 4. Reified Domain Properties Breakdown

The 265 `owl:Axiom` records cover 10 distinct domain object properties, representing 100% of all direct domain assertions in the knowledge graph:

| Property | Subject Class → Object Class | Axiom Count | Primary Literature Sources |
|---|---|:---:|---|
| `rice:vulnerableTo` | `Plant ⊔ GrowthStage` → `Disease ⊔ Pest` | **59** | IRRI Rice Knowledge Bank, CABI Compendium |
| `rice:occursIn` | `Disease ⊔ Pest` → `GrowthStage` | **47** | IRRI RKB, Ou (1985), CABI |
| `rice:controlledBy` | `Disease ⊔ Pest` → `Treatment` | **42** | CABI Compendium, BBPOPT Kementan (2022) |
| `rice:indicatedBy` | `Disease ⊔ Pest` → `Symptom` | **42** | IRRI Rice Doctor, CABI Compendium |
| `rice:increaseRiskOf` | `EnvironmentalFactor` → `Disease ⊔ Pest` | **29** | CABI Compendium, Ham et al. (2011) |
| `rice:recommends` | `Disease ⊔ Pest ⊔ SeverityLevel` → `ManagementAction` | **23** | BBPOPT Technical Bulletins, IRRI GAP |
| `rice:causes` | `Pathogen` → `Disease` | **8** | CABI, Ou (1985), Hibino (1996) |
| `rice:preventedBy` | `Disease` → `Treatment` | **8** | IRRI Rice Knowledge Bank, CABI |
| `rice:requires` | `Treatment` → `GrowthStage` | **5** | BBPOPT, IRRI GAP Standard Protocols |
| `rice:transmits` | `Pest` → `Pathogen` | **2** | Hibino (1996), CABI CPC (Leafhopper vector) |
| **Total** | | **265** | **100% Reified with Sources** |

---

## 5. Audit & Quality Assurance History

### 1. CABI Datasheet Numeric ID Audit
In earlier drafts, several CABI Compendium numeric IDs suffered from generic redirection or legacy ID drift. An exhaustive verification audit checked every URL against the live CABI Digital Library:
- Corrected 14 distinct datasheet URLs to authoritative species/disease records (e.g., *Magnaporthe oryzae* datasheet 46154, *Scirpophaga incertulas* datasheet 49132, *Xanthomonas oryzae pv. oryzae* datasheet 56947).
- Verified that all 247 CABI assertions point to valid, 200-OK HTTP resources.

### 2. Indonesian Ministry of Agriculture (BBPOPT) Domain Update
The institutional web portal for BBPOPT underwent a national domain migration:
- Legacy URL `bbpopt.ditlin.pertanian.go.id` was updated to the active government domain `bbpopt.tanamanpangan.pertanian.go.id`.

### 3. EPPO Global Database Audit (15 Verified Codes)
All 15 biological organisms in the ontology carry validated 6-letter EPPO codes:
- Pathogens: `PYRIOR` (*Magnaporthe oryzae*), `XANTOR` (*Xanthomonas oryzae pv. oryzae*), `XANTTO` (*X. oryzae pv. oryzicola*), `COCHMI` (*Bipolaris oryzae*), `PSDMGM` (*Burkholderia glumae*), `SCPHMA` (*Sclerophthora macrospora*), `RTBV00` (RTBV), `RTSV00` (RTSV).
- Pests: `SCHOBI` (*Scirpophaga incertulas* / Stem Borer), `CNAPME` (*Cnaphalocrocis medinalis* / Leaf Folder), `NILALU` (*Nilaparvata lugens* / Brown Planthopper), `PSEDSE` (*Mythimna separata* / Armyworm), `LEPROR` (*Leptocorisa oratorius* / Rice Bug), `HISPAR` (*Dicladispa armigera* / Hispa), `NEPHIM` (*Nephotettix virescens* / Green Leafhopper).

### 4. Dataset Source Attribution
- `PaddyDoctorDataset` metadata explicitly cites Petchiammal et al. (2022), *Paddy Doctor: A Large-Scale Image Dataset for Plant Disease Classification*, arXiv:2205.11108, with CC-BY 4.0 license and live Kaggle benchmark repository URI.

---

## 6. Formal Competency Question (SPARQL) Verification

The provenance layer (Knowledge Dimension D3) is evaluated under the automated **Rice MMKG 25 CQ Benchmark**:

### CQ-21 | L4 × D3 | Provenance Completeness (PASS: 265/265, 100%)
Verifies that 100% of reified domain axioms possess both an authoritative source URI and a complete bibliographic citation:
```sparql
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT DISTINCT ?ax WHERE {
  ?ax a owl:Axiom ;
      dcterms:source ?src ;
      dcterms:bibliographicCitation ?cit .
}
```

### CQ-22 | L4 × D3 | Integrity Constraint against Incomplete Provenance (PASS: 0 violations)
Enforces that no orphaned or partial axiom exists in the ontology lacking essential metadata:
```sparql
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rice:    <http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#>

SELECT ?ax WHERE {
  ?ax a owl:Axiom .
  FILTER ( NOT EXISTS { ?ax dcterms:source ?s } ||
           NOT EXISTS { ?ax dcterms:bibliographicCitation ?c } ||
           NOT EXISTS { ?ax rice:evidenceType ?e } )
}
```
*Result: Exactly 0 violations.*

### CQ-24 | L4 × D3 | Literal Hygiene (FAIL: 1 violation -> Scheduled Fix for v0.6.1)
Verifies that all `rice:evidenceType` annotations carry explicit language tags (`@en`) to ensure uniform SPARQL grouping and filtering:
```sparql
PREFIX rice: <http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#>

SELECT ?ax ?v WHERE {
  ?ax rice:evidenceType ?v .
  FILTER ( lang(?v) = "" )
}
```
*Status: Scheduled for uniform `@en` tagging in v0.6.1.*
