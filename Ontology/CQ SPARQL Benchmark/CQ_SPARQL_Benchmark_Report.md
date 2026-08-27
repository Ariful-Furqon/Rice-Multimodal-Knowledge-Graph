# Rice MMKG v0.5 — Competency Question (CQ) SPARQL Benchmark Report

**Generated:** 2026-08-27 12:35  
**Ontology:** `Rice MMKG.rdf` (`owl:versionInfo 0.5`)  
**Total Triples:** 66,873  
**Total CQs:** 16  

## Methodology

Competency Questions are formulated as **general-pattern queries** following:
- Gruninger & Fox (1995). *Methodology for the Design and Evaluation of Ontologies.*
- Suárez-Figueroa et al. (2012). *The NeOn Methodology for Ontology Engineering.* Springer.
- Poveda-Villalón et al. (2022). *LOT: An industrial oriented ontology engineering framework.* Engineering Applications of Artificial Intelligence, 111, 104755.

Each CQ is written at the **schema/pattern level** (returns results for all matching entities,
not just one) so that a single SPARQL execution validates the relational coverage of the
entire ontology, not a single hand-picked triple.

### CQ Levels

| Level | Focus | Evaluated via |
|---|---|---|
| **L1 — Factual** | Direct 1-hop pattern retrieval | SPARQL SELECT |
| **L2 — Contextual** | Multi-criteria: growth stage + environmental factor | SPARQL JOIN + FILTER |
| **L3 — Causal** | Multi-hop epidemiological chain (vector tracing) | SPARQL multi-hop |
| **L4 — Inference** | Defined-class membership, provenance, alignment | SPARQL + OWL Axiom inspection |

---

## Summary Dashboard

| Result | Count | % |
|---|---|---|
| ✅ PASS (non-empty result set) | 16 | 100% |
| ⚠️ EMPTY (query ran, 0 rows) | 0 | 0% |
| ❌ ERROR (SPARQL parse/runtime error) | 0 | 0% |
| **Total** | **16** | **100%** |

---

## Results by CQ

### CQ-01 — Factual / Single-hop `[✅ PASS]`

**Question:** For every rice disease in the ontology, what is its causal pathogen or pest, and what are all observable symptoms that indicate it?

**Result:** 34 row(s) returned in 90.6 ms

| disease | pathogenOrPest | symptom |
| --- | --- | --- |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Yellow_Leaf |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Wilting |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Leaf_Rolling |
| rice:Bacterial_Leaf_Streak | rice:Xanthomonas_Oryzicola | rice:Yellow_Leaf |
| rice:Bacterial_Leaf_Streak | rice:Xanthomonas_Oryzicola | rice:Water_Soaked_Streak |
| rice:Bacterial_Leaf_Streak | rice:Xanthomonas_Oryzicola | rice:Translucent_Stripe |
| rice:Bacterial_Panicle_Blight | rice:Burkholderia_Glumae | rice:Empty_Grain |
| rice:Bacterial_Panicle_Blight | rice:Burkholderia_Glumae | rice:Grain_Discoloration |
| rice:Bacterial_Panicle_Blight | rice:Burkholderia_Glumae | rice:Discolored_Panicle |
| *... 24 more rows (truncated for readability)* |

---

### CQ-02 — Factual / Single-hop `[✅ PASS]`

**Question:** For every pest in the ontology, what symptoms does its infestation produce, and which treatments control it?

**Result:** 21 row(s) returned in 5.4 ms

| pest | symptom | treatment |
| --- | --- | --- |
| rice:Armyworm | rice:Chewed_Leaf | rice:Biological_Control |
| rice:Armyworm | rice:Chewed_Leaf | rice:Insecticide_Application |
| rice:Brown_Planthopper | rice:Hopper_Burn | rice:Biological_Control |
| rice:Brown_Planthopper | rice:Hopper_Burn | rice:Insecticide_Application |
| rice:Brown_Planthopper | rice:Yellow_Leaf | rice:Biological_Control |
| rice:Brown_Planthopper | rice:Yellow_Leaf | rice:Insecticide_Application |
| rice:Hispa | rice:Brown_Leaf_Tip | rice:Neem_Based_Pesticide |
| rice:Hispa | rice:Brown_Leaf_Tip | rice:Biological_Control |
| rice:Hispa | rice:Brown_Leaf_Tip | rice:Insecticide_Application |
| rice:Hispa | rice:White_Streak | rice:Neem_Based_Pesticide |
| *... 11 more rows (truncated for readability)* |

---

### CQ-03 — Factual / Single-hop `[✅ PASS]`

**Question:** What are all the symptoms currently defined in the ontology, and which disease or pest does each indicate?

**Result:** 42 row(s) returned in 5.1 ms

| symptom | diseaseOrPest |
| --- | --- |
| rice:Brown_Leaf_Tip | rice:Hispa |
| rice:Brown_Lesion | rice:Brown_Spot |
| rice:Brown_Lesion | rice:Rice_Blast_Disease |
| rice:Chewed_Leaf | rice:Armyworm |
| rice:Dead_Tiller | rice:Deadheart |
| rice:Deadheart | rice:Stem_Borer |
| rice:Discolored_Panicle | rice:Bacterial_Panicle_Blight |
| rice:Dry_Leaf_Tip | rice:Bacterial_Leaf_Blight |
| rice:Empty_Grain | rice:Bacterial_Panicle_Blight |
| rice:Empty_Grain | rice:Rice_Bug |
| *... 32 more rows (truncated for readability)* |

---

### CQ-04 — Factual / Single-hop `[✅ PASS]`

**Question:** For every treatment available in the ontology, which diseases or pests does it control, and which management action recommends it?

**Result:** 69 row(s) returned in 12.0 ms

| treatment | diseaseOrPest | managementAction |
| --- | --- | --- |
| rice:Biological_Control | rice:Hispa | rice:Leaf_Folder |
| rice:Biological_Control | rice:Deadheart | rice:Leaf_Folder |
| rice:Biological_Control | rice:Rice_Blast_Disease | rice:Leaf_Folder |
| rice:Biological_Control | rice:Armyworm | rice:Leaf_Folder |
| rice:Biological_Control | rice:Stem_Borer | rice:Leaf_Folder |
| rice:Biological_Control | rice:Leaf_Folder | rice:Leaf_Folder |
| rice:Biological_Control | rice:Brown_Planthopper | rice:Leaf_Folder |
| rice:Crop_Rotation | rice:Brown_Spot | — |
| rice:Crop_Rotation | rice:Rice_Blast_Disease | — |
| rice:Crop_Rotation | rice:Bacterial_Leaf_Blight | — |
| *... 59 more rows (truncated for readability)* |

---

### CQ-05 — Contextual / Multi-criteria `[✅ PASS]`

**Question:** Which diseases and pests affect rice at the Tillering growth stage, and what environmental factors increase their risk?

**Result:** 17 row(s) returned in 8.0 ms

| diseaseOrPest | envFactor |
| --- | --- |
| rice:Bacterial_Leaf_Blight | rice:High_Humidity |
| rice:Bacterial_Leaf_Blight | rice:Poor_Soil_Drainage |
| rice:Bacterial_Leaf_Blight | rice:Excessive_Nitrogen |
| rice:Bacterial_Leaf_Streak | rice:High_Humidity |
| rice:Bacterial_Leaf_Streak | rice:High_Temperature |
| rice:Brown_Spot | rice:High_Humidity |
| rice:Brown_Spot | rice:Poor_Soil_Drainage |
| rice:Brown_Spot | rice:Low_Rainfall |
| rice:Downy_Mildew | rice:High_Humidity |
| rice:Downy_Mildew | rice:Waterlogged_Soil |
| *... 7 more rows (truncated for readability)* |

---

### CQ-06 — Contextual / Multi-criteria `[✅ PASS]`

**Question:** For every environmental factor in the ontology, which diseases or pests does it increase the risk of, and across which growth stages?

**Result:** 88 row(s) returned in 11.3 ms

| envFactor | diseaseOrPest | stage |
| --- | --- | --- |
| rice:Dense_Canopy | rice:Deadheart | rice:Reproductive_Stage |
| rice:Dense_Canopy | rice:Deadheart | rice:Tillering_Stage |
| rice:Dense_Canopy | rice:Deadheart | rice:Vegetative_Stage |
| rice:Dense_Canopy | rice:Hispa | rice:Vegetative_Stage |
| rice:Dense_Canopy | rice:Hispa | rice:Tillering_Stage |
| rice:Excessive_Nitrogen | rice:Bacterial_Leaf_Blight | rice:Vegetative_Stage |
| rice:Excessive_Nitrogen | rice:Bacterial_Leaf_Blight | rice:Tillering_Stage |
| rice:Excessive_Nitrogen | rice:Bacterial_Leaf_Blight | rice:Reproductive_Stage |
| rice:Excessive_Nitrogen | rice:Brown_Planthopper | rice:Flowering_Stage |
| rice:Excessive_Nitrogen | rice:Brown_Planthopper | rice:Vegetative_Stage |
| *... 78 more rows (truncated for readability)* |

---

### CQ-07 — Contextual / Multi-criteria `[✅ PASS]`

**Question:** Which diseases cause symptoms specifically affecting the panicle or grain at the Reproductive growth stage, and what is the recommended treatment?

**Result:** 21 row(s) returned in 13.9 ms

| disease | symptom | treatment |
| --- | --- | --- |
| rice:Bacterial_Panicle_Blight | rice:Empty_Grain | rice:Seed_Treatment |
| rice:Bacterial_Panicle_Blight | rice:Empty_Grain | rice:Crop_Rotation |
| rice:Bacterial_Panicle_Blight | rice:Empty_Grain | rice:Crop_Sanitation |
| rice:Bacterial_Panicle_Blight | rice:Grain_Discoloration | rice:Seed_Treatment |
| rice:Bacterial_Panicle_Blight | rice:Grain_Discoloration | rice:Crop_Rotation |
| rice:Bacterial_Panicle_Blight | rice:Grain_Discoloration | rice:Crop_Sanitation |
| rice:Bacterial_Panicle_Blight | rice:Discolored_Panicle | rice:Seed_Treatment |
| rice:Bacterial_Panicle_Blight | rice:Discolored_Panicle | rice:Crop_Rotation |
| rice:Bacterial_Panicle_Blight | rice:Discolored_Panicle | rice:Crop_Sanitation |
| rice:Brown_Spot | rice:Grain_Discoloration | rice:Crop_Rotation |
| *... 11 more rows (truncated for readability)* |

---

### CQ-08 — Contextual / Multi-criteria `[✅ PASS]`

**Question:** Which preventive measures are recommended for rice diseases that require a specific growth-stage-based prerequisite action?

**Result:** 7 row(s) returned in 4.2 ms

| disease | prevention | prerequisite |
| --- | --- | --- |
| rice:Bacterial_Leaf_Blight | rice:Resistant_Variety | rice:Seedling_Stage |
| rice:Bacterial_Leaf_Streak | rice:Resistant_Variety | rice:Seedling_Stage |
| rice:Bacterial_Panicle_Blight | rice:Resistant_Variety | rice:Seedling_Stage |
| rice:Brown_Spot | rice:Resistant_Variety | rice:Seedling_Stage |
| rice:Downy_Mildew | rice:Seed_Treatment | — |
| rice:Rice_Blast_Disease | rice:Resistant_Variety | rice:Seedling_Stage |
| rice:Rice_Tungro_Disease | rice:Resistant_Variety | rice:Seedling_Stage |

---

### CQ-09 — Causal / Multi-hop Epidemiological `[✅ PASS]`

**Question:** For every insect vector in the ontology, which pathogens does it transmit, what disease does that pathogen cause, and what management actions are recommended to break the transmission chain?

**Result:** 2 row(s) returned in 3.9 ms

| vector | pathogen | disease | treatment |
| --- | --- | --- | --- |
| rice:Nephotettix_Virescens | rice:Rice_Tungro_Bacilliform_Virus | rice:Rice_Tungro_Disease | — |
| rice:Nephotettix_Virescens | rice:Rice_Tungro_Spherical_Virus | rice:Rice_Tungro_Disease | — |

---

### CQ-10 — Causal / Multi-hop Epidemiological `[✅ PASS]`

**Question:** Which diseases are caused by viral pathogens transmitted by insect vectors, distinguishing them from diseases caused directly by fungal or bacterial pathogens?

**Result:** 8 row(s) returned in 4.0 ms

| disease | pathogen | vector |
| --- | --- | --- |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | — |
| rice:Bacterial_Leaf_Streak | rice:Xanthomonas_Oryzicola | — |
| rice:Bacterial_Panicle_Blight | rice:Burkholderia_Glumae | — |
| rice:Brown_Spot | rice:Bipolaris_Oryzae | — |
| rice:Downy_Mildew | rice:Sclerophthora_Macrospora | — |
| rice:Rice_Blast_Disease | rice:Magnaporthe_Oryzae | — |
| rice:Rice_Tungro_Disease | rice:Rice_Tungro_Bacilliform_Virus | rice:Nephotettix_Virescens |
| rice:Rice_Tungro_Disease | rice:Rice_Tungro_Spherical_Virus | rice:Nephotettix_Virescens |

---

### CQ-11 — Causal / Multi-hop Epidemiological `[✅ PASS]`

**Question:** For every disease in the ontology, what is the complete diagnostic profile: causal agent, associated symptoms, environmental risk factors, vulnerable growth stages, and recommended interventions?

**Result:** 994 row(s) returned in 66.5 ms

| disease | causalAgent | symptom | envFactor | stage | treatment |
| --- | --- | --- | --- | --- | --- |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip | rice:High_Humidity | rice:Vegetative_Stage | rice:Crop_Rotation |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip | rice:High_Humidity | rice:Vegetative_Stage | rice:Water_Management |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip | rice:High_Humidity | rice:Vegetative_Stage | rice:Resistant_Variety |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip | rice:High_Humidity | rice:Vegetative_Stage | rice:Crop_Sanitation |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip | rice:High_Humidity | rice:Tillering_Stage | rice:Crop_Rotation |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip | rice:High_Humidity | rice:Tillering_Stage | rice:Water_Management |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip | rice:High_Humidity | rice:Tillering_Stage | rice:Resistant_Variety |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip | rice:High_Humidity | rice:Tillering_Stage | rice:Crop_Sanitation |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip | rice:High_Humidity | rice:Reproductive_Stage | rice:Crop_Rotation |
| rice:Bacterial_Leaf_Blight | rice:Xanthomonas_Oryzae | rice:Dry_Leaf_Tip | rice:High_Humidity | rice:Reproductive_Stage | rice:Water_Management |
| *... 984 more rows (truncated for readability)* |

---

### CQ-12 — Inference / Provenance `[✅ PASS]`

**Question:** For every domain-level assertion in the ontology, what is the authoritative source (URI) and bibliographic citation that backs it?

**Result:** 265 row(s) returned in 39.2 ms

| subject | property | object | source | citation | evidenceType |
| --- | --- | --- | --- | --- | --- |
| rice:Armyworm | rice:controlledBy | rice:Insecticide_Application | https://www.cabi.org/isc/datasheet/45093 | CABI (2022). Mythimna separata (oriental armyworm). Crop Protection Compendium. CAB International, Wallingford, UK. / IRRI (2020). Rice Doctor: Armyworm. | literature-curated |
| rice:Armyworm | rice:controlledBy | rice:Biological_Control | https://www.cabi.org/isc/datasheet/45093 | CABI (2022). Mythimna separata (oriental armyworm). Crop Protection Compendium. CAB International, Wallingford, UK. / IRRI (2020). Rice Doctor: Armyworm. | literature-curated |
| rice:Armyworm | rice:indicatedBy | rice:Chewed_Leaf | https://www.cabi.org/isc/datasheet/45093 | CABI (2022). Mythimna separata (oriental armyworm). Crop Protection Compendium. CAB International, Wallingford, UK. / IRRI (2020). Rice Doctor: Armyworm. | literature-curated |
| rice:Armyworm | rice:occursIn | rice:Vegetative_Stage | https://www.cabi.org/isc/datasheet/45093 | CABI (2022). Mythimna separata (oriental armyworm). Crop Protection Compendium. CAB International, Wallingford, UK. / IRRI (2020). Rice Doctor: Armyworm. | literature-curated |
| rice:Armyworm | rice:occursIn | rice:Seedling_Stage | https://www.cabi.org/isc/datasheet/45093 | CABI (2022). Mythimna separata (oriental armyworm). Crop Protection Compendium. CAB International, Wallingford, UK. / IRRI (2020). Rice Doctor: Armyworm. | literature-curated |
| rice:Armyworm | rice:recommends | rice:Insecticide_Application | https://www.cabi.org/isc/datasheet/45093 | CABI (2022). Mythimna separata (oriental armyworm). Crop Protection Compendium. CAB International, Wallingford, UK. / IRRI (2020). Rice Doctor: Armyworm. | literature-curated |
| rice:Bacterial_Leaf_Blight | rice:controlledBy | rice:Resistant_Variety | https://www.cabi.org/isc/datasheet/56956 | CABI (2022). Xanthomonas oryzae pv. oryzae (bacterial blight of rice). Crop Protection Compendium. CAB International, Wallingford, UK. / IRRI (2020). Rice Doctor: Bacterial Blight. | literature-curated |
| rice:Bacterial_Leaf_Blight | rice:controlledBy | rice:Crop_Rotation | https://www.cabi.org/isc/datasheet/56956 | CABI (2022). Xanthomonas oryzae pv. oryzae (bacterial blight of rice). Crop Protection Compendium. CAB International, Wallingford, UK. / IRRI (2020). Rice Doctor: Bacterial Blight. | literature-curated |
| rice:Bacterial_Leaf_Blight | rice:controlledBy | rice:Crop_Sanitation | https://www.cabi.org/isc/datasheet/56956 | CABI (2022). Xanthomonas oryzae pv. oryzae (bacterial blight of rice). Crop Protection Compendium. CAB International, Wallingford, UK. / IRRI (2020). Rice Doctor: Bacterial Blight. | literature-curated |
| rice:Bacterial_Leaf_Blight | rice:controlledBy | rice:Water_Management | https://www.cabi.org/isc/datasheet/56956 | CABI (2022). Xanthomonas oryzae pv. oryzae (bacterial blight of rice). Crop Protection Compendium. CAB International, Wallingford, UK. / IRRI (2020). Rice Doctor: Bacterial Blight. | literature-curated |
| *... 255 more rows (truncated for readability)* |

---

### CQ-13 — Inference / Provenance `[✅ PASS]`

**Question:** Which image observations in the ontology qualify as SymptomaticObservations (i.e., capture at least one symptom), and what symptom do they capture?

**Result:** 20 row(s) returned in 1743.7 ms

| observation | symptom |
| --- | --- |
| rice:PaddyDoctor_dead_heart_100008 | rice:Deadheart |
| rice:PaddyDoctor_dead_heart_100015 | rice:Deadheart |
| rice:PaddyDoctor_dead_heart_100020 | rice:Deadheart |
| rice:PaddyDoctor_dead_heart_100026 | rice:Deadheart |
| rice:PaddyDoctor_dead_heart_100027 | rice:Deadheart |
| rice:PaddyDoctor_dead_heart_100029 | rice:Deadheart |
| rice:PaddyDoctor_dead_heart_100030 | rice:Deadheart |
| rice:PaddyDoctor_dead_heart_100033 | rice:Deadheart |
| rice:PaddyDoctor_dead_heart_100036 | rice:Deadheart |
| rice:PaddyDoctor_dead_heart_100047 | rice:Deadheart |
| *... 10 more rows (truncated for readability)* |

---

### CQ-14 — Inference / Provenance `[✅ PASS]`

**Question:** For every biological entity (disease, pathogen, pest) that has been aligned to an external vocabulary, what are its EPPO code, AGROVOC concept, and NCBI Taxonomy identifiers?

**Result:** 23 row(s) returned in 15.4 ms

| entity | eppoCode | agrovocMatch | ncbiMatch |
| --- | --- | --- | --- |
| rice:Armyworm | PSEDSE | — | — |
| rice:Bacterial_Leaf_Blight | — | — | — |
| rice:Bacterial_Leaf_Streak | — | — | — |
| rice:Bacterial_Panicle_Blight | — | — | — |
| rice:Bipolaris_Oryzae | COCHMI | http://aims.fao.org/aos/agrovoc/c_34512 | http://purl.obolibrary.org/obo/NCBITaxon_101162 |
| rice:Brown_Planthopper | NILALU | http://aims.fao.org/aos/agrovoc/c_25204 | — |
| rice:Brown_Spot | — | — | — |
| rice:Burkholderia_Glumae | PSDMGM | — | http://purl.obolibrary.org/obo/NCBITaxon_337 |
| rice:Downy_Mildew | — | — | — |
| rice:Hispa | HISPAR | — | http://purl.obolibrary.org/obo/NCBITaxon_111238 |
| *... 13 more rows (truncated for readability)* |

---

### CQ-15 — Inference / Provenance `[✅ PASS]`

**Question:** Which Good Agricultural Practices (GAP) or biological treatments are available as non-chemical alternatives for managing rice diseases or pests?

**Result:** 1 row(s) returned in 8.7 ms

| entity | treatment |
| --- | --- |
| rice:Downy_Mildew | rice:Seed_Treatment |

---

### CQ-16 — Inference / Provenance `[✅ PASS]`

**Question:** What is the complete ontology statistics summary: total number of individuals per class, object properties, and provenance axiom coverage?

**Result:** 9 row(s) returned in 224.0 ms

| class | count |
| --- | --- |
| rice:ImageObservation | 10407 |
| rice:Symptom | 28 |
| rice:Treatment | 12 |
| rice:EnvironmentalFactor | 9 |
| rice:Disease | 8 |
| rice:Pathogen | 8 |
| rice:Pest | 7 |
| rice:GrowthStage | 7 |
| rice:ManagementAction | 5 |

---

## Observations & Next Steps

### Provenance Coverage
CQ-12 verifies that all domain-level assertions carry `owl:Axiom` metadata.
The result set count from CQ-12 must equal the total `owl:Axiom` record
count reported by `verify.py` (currently 265). Any discrepancy flags a gap.

### SensorObservation (CQ-16)
CQ-16 confirms that `rice:SensorObservation` currently has 0 individuals.
This is an expected and documented extension point (v0.5). Populating it
is scoped to Phase 3 of the ESWC 2027 roadmap.

### SymptomaticObservation (CQ-13)
Results are limited to 20 rows; the full count is available by removing `LIMIT 20`.
The reasoner-materialised superset (`SymptomaticObservation`) requires running
HermiT/Pellet — SPARQL alone returns only explicitly asserted `captures` triples.

### Empty / Error CQs
Any EMPTY result must be reviewed to determine whether:
  (a) the ontology genuinely lacks data for this pattern (a gap to document), or
  (b) the query references an IRI that needs adjustment.
EMPTY results are not automatically failures — they are honest measurements.

---

## Citation

If reporting these results in a paper, cite as:

```
Rice MMKG v0.5 Competency Question Benchmark.
Evaluated against Rice MMKG.rdf (owl:versionInfo 0.5,
http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG).
Methodology: Gruninger & Fox (1995); Suárez-Figueroa et al. (2012);
Poveda-Villalón et al. (2022).
```
