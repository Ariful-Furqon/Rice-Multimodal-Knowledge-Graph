# Candidate Datasets Analysis

## Summary Table

| Dataset | Modality | Access | Licence | Redistribution allowed? | Gap closed | Recommendation |
|---|---|---|---|---|---|---|
| Paddy Doctor full (IEEE DataPort) | image + metadata (variety, age) | Downloaded (`Data/paddy-doctor-diseases/`) | CC BY 4.0 | Yes | Pests: 1/7 → 3/7 (+ variety & age metadata) | **Import** (revised 2026-10-03) |
| Paddy Doctor pest set | image | Open | Unverified (assumed open) | Unverified | Pests: 1/7 → 3/7 | Import |
| IP102 | image | Open (Kaggle/GitHub) | Not stated (research only) | No | Pests: 1/7 → 5/7 | Later |
| Dhan-Shomadhan | image | Open (Mendeley) | CC BY 4.0 | Yes | Diseases: 8/15 → 9/15 | Import |
| Roboflow Rice Nutrient Deficiency | image | Registration (Roboflow/Kaggle) | Unverified | Unverified | Diseases: 9/15 → 12/15 | Later |

## 1. Paddy Doctor full + metadata.csv (IEEE DataPort)
> **Revised 2026-10-03** after inspecting the local download. Earlier verdict ("Gap closed: 0 → Drop") was based on the abstract only and is wrong.

- **Identity:** Paddy Doctor: A Visual Image Dataset for Automated Paddy Disease Classification and Benchmarking (IEEE DataPort, DOI: 10.21227/hz4v-af08). Authors: Petchiammal A, Briskline Kiruba S, Murugan D, Pandarasamy Arjunan.
- **Access:** Downloaded to `Data/paddy-doctor-diseases/` (4.76 GB).
- **Licence:** CC BY 4.0 (Redistribution allowed).
- **Content (verified):** 16,225 images, 1080×1440, 13 classes. `metadata.csv` (`image_id,label,variety,age`) has 16,225 rows, one per image.
  - Diseases: blast 2,351 · tungro 1,951 · brown_spot 1,257 · downy_mildew 868 · bacterial_leaf_blight 648 · bacterial_leaf_streak 505 · bacterial_panicle_blight 450
  - Pests: hispa 2,151 · white_stem_borer 1,273 · leaf_roller 1,095 · yellow_stem_borer 765 · black_stem_borer 506
  - normal 2,405
  - Varieties (10): `45` 10,978 (68%) · KarnatakaPonni 1,404 · Ponni 975 · AtchayaPonni 706 · Zonal 649 · AndraPonni 615 · Onthanel 585 · IR20 235 · Surya 42 · RR 36
  - Age: 45–80 days (17 distinct values)
- **Overlap with Kaggle subset (already in ontology as `PaddyDoctor_*`, 10,407 images):** no byte-identical files (Kaggle is re-encoded). A dHash check matched **7,505** IEEE images to Kaggle images. Kaggle `dead_heart` (1,442) = IEEE black + white + yellow stem borer merged. **11** matches have different labels in the two releases (`Worklog/PaddyDoctor_IEEE_import/output/kaggle_label_conflicts.csv`).
- **Mapping to Rice MMKG:**
  - 7 diseases + hispa + normal → same targets as the Kaggle import (exact)
  - black/white/yellow_stem_borer → `Stem_Borer` (broad) + `captures Dead_Tiller`
  - leaf_roller → `Leaf_Folder` (close; confirm with expert)
  - variety → new `Variety` individuals (none exist yet). `45` is assumed to be ADT 45 (UNVERIFIED). Zonal, Onthanel and RR are unresolved.
  - age → `plantAgeDays` (proposed property). Not mapped to `GrowthStage`, because stage depends on variety duration.
- **Gap closed:** Pests with images 1/7 → 3/7 (`Stem_Borer`, `Leaf_Folder`, plus existing `Hispa`). Adds variety and age context to every image. No new diseases.
- **Issues:** Taxonomy granularity (3 stem borers → 1 individual); variety codes need verification; class imbalance across varieties (variety 45 dominates).
- **Artefacts:** `Worklog/PaddyDoctor_IEEE_import/` (`scripts/map_paddydoctor_ieee.py`, `scripts/phash_overlap.py`, `output/label_mapping.csv`, `output/variety_mapping.csv`, `output/paddydoctor_ieee.ttl`). The TTL is a separate module and has not been merged into `Rice MMKG.rdf`.

## 2. Paddy Doctor pest set
- **Identity:** Paddy Doctor: Open Dataset and Automated Pest Identification Using Pre-trained Deep Learning Models (ICLR 2024 Workshop). Authors: Petchiammal A., Pandarasamy Arjunan.
- **Access:** Open download (GitHub repository cloned).
- **Licence:** UNVERIFIED (assumed open source based on paper, but exact licence text not found).
- **Content:** 6,062 images, 17 classes (16 pest + 1 normal).
- **Mapping to Rice MMKG:**
  - Black/White/Yellow Stem Borer -> `Stem_Borer` (close)
  - Hispa -> `Hispa` (exact)
  - Leaf Roller -> `Leaf_Folder` (close)
- **Gap closed:** Pests with images: 1/7 → 3/7.
- **Issues:** Taxonomy mismatches ("3 stem borers" vs one `Stem_Borer` individual, "leaf roller" vs `Leaf_Folder`).

## 4. IP102
- **Identity:** IP102: A Large-Scale Benchmark Dataset for Insect Pest Recognition (CVPR 2019). Authors: Wu, X., et al.
- **Access:** Open download (via Kaggle/GitHub, but typically requires Kaggle registration).
- **Licence:** Not stated (distributed for research purposes, no explicit open licence). Redistribution allowed: No.
- **Content:** 75,000 images, 102 pest categories, including multiple rice pests. Hierarchical taxonomy.
- **Mapping to Rice MMKG:**
  - Rice leaf roller -> `Leaf_Folder` (close)
  - Brown plant hopper -> `Brown_Planthopper` (exact)
  - Asiatic rice borer / Yellow rice borer -> `Stem_Borer` (close)
  - Rice leafhopper -> `Nephotettix_Virescens` (close)
- **Gap closed:** Pests with images: 1/7 → 5/7.
- **Issues:** Web-scraped dataset (label noise, duplicates), long-tailed distribution, no explicit open licence for redistribution.

## Priority 2. Dhan-Shomadhan
- **Identity:** Dhan-Shomadhan dataset (Mendeley Data).
- **Access:** Open download (registration may be required on Mendeley).
- **Licence:** CC BY 4.0. Redistribution allowed: Yes.
- **Content:** 1,106 images across 5 diseases (Brown Spot, Leaf Scald, Rice Blast, Rice Tungro, Sheath Blight). Field and white backgrounds.
- **Mapping to Rice MMKG:**
  - Sheath Blight -> `Sheath_Blight` (exact)
- **Gap closed:** Diseases with images: 8/15 → 9/15.
- **Issues:** Small class sizes (~200 images for Sheath Blight).

## Priority 2. Roboflow / Kaggle Rice Nutrient Deficiency
- **Identity:** Rice Disease and Nutrient Deficiency Dataset (Roboflow Universe / Kaggle).
- **Access:** Registration-gated.
- **Licence:** UNVERIFIED (depends on uploader). Redistribution allowed: UNVERIFIED.
- **Content:** Images covering Nitrogen, Potassium, Magnesium, Manganese, and Zinc deficiencies.
- **Mapping to Rice MMKG:**
  - Nitrogen -> `Nitrogen_Deficiency_Disorder` (exact)
  - Potassium -> `Potassium_Deficiency_Disorder` (exact)
  - Zinc -> `Zinc_Deficiency_Disorder` (exact)
- **Gap closed:** Diseases with images: 9/15 → 12/15.
- **Issues:** UNVERIFIED licence, potential synthetic data or poor label quality.

## Updated Coverage Table
| Category | Images Before | Images After (Recommended Imports) |
|---|---|---|
| Pests | 1/7 | 3/7 |
| Diseases | 8/15 | 9/15 |


