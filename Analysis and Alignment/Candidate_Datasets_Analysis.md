# Candidate Datasets Analysis

## Summary Table

| Dataset | Modality | Access | Licence | Redistribution allowed? | Gap closed | Recommendation |
|---|---|---|---|---|---|---|
| Paddy Doctor full (IEEE DataPort) | image + metadata (variety, age) | Downloaded (`Data/paddy-doctor-diseases/`) | CC BY 4.0 | Yes | Pests: 1/7 → 3/7 (+ variety & age metadata) | **Import** (revised 2026-10-03) |
| Paddy Doctor pest set | image | **Not downloaded.** `Data/candidates/paddydoctor_pest_set/` is the paddydoc GitHub *code* repository (notebooks, Apache-2.0 for code), with no pest images (checked 2026-10-05) | UNVERIFIED for the images | UNVERIFIED | Pests: no change until the images are found (its three stem borers and leaf roller duplicate classes already imported from the IEEE release) | Later: locate the image release |
| IP102 | image | Open (Kaggle/GitHub) | Not stated (research only) | No | Pests: 1/7 → 5/7 | Later |
| Dhan-Shomadhan | image | Downloaded (`Data/dhan-shomadhan/`) | CC BY 4.0 (Mendeley page, checked 2026-10-05) | Yes | Diseases with images: 8/15 → 10/16 (`Sheath_Blight`, and the new `Leaf_Scald`) | **Imported 2026-10-04**, completed 2026-10-05 |
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
- **Overlap with the former Kaggle subset (10,407 images):** no byte-identical files (Kaggle is re-encoded). A dHash crosswalk matched 10,065 of the Kaggle images to IEEE images. 2 have label conflicts and 340 have no IEEE match. Kaggle `dead_heart` (1,442) = IEEE black + white + yellow stem borer merged.
- **Status: IMPORTED 2026-10-03.** All Kaggle ImageObservations were replaced by the 16,225 IEEE images (see `Worklog/PaddyDoctor_IEEE_import/SUMMARY.md`). HermiT: consistent.
- **Mapping applied:**
  - 7 diseases + hispa + normal → same targets as the Kaggle import
  - yellow_stem_borer → `Stem_Borer` (= *S. incertulas*) + `captures Dead_Tiller`
  - black / white_stem_borer → NOT mapped to `Stem_Borer` (species differ; group-vs-individual decision still open). They keep `annotatedAs Deadheart` + `captures Dead_Tiller`.
  - leaf_roller → `Leaf_Folder` (accepted)
  - variety → `ofVariety` for 6 resolved names (Karnataka/Atchaya/Andhra Ponni, Ponni, IR20, Surya; 3,977 images). Codes `45`, Zonal, Onthanel and RR are not implemented.
  - age → `plantAgeDays` on all images. Not mapped to `GrowthStage`.
- **Gap closed:** Pests with images 1/7 → 3/7 (`Hispa`, `Stem_Borer`, `Leaf_Folder`). No new diseases.
- **Issues:** Variety code `45` (68% of images) is unresolved; 9 images in the expert package have no IEEE counterpart; class imbalance across varieties.
- **Artefacts:** `Worklog/PaddyDoctor_IEEE_import/` (`SUMMARY.md`, `scripts/apply_replace_kaggle.py`, `scripts/build_crosswalk.py`, `output/kaggle_to_ieee_crosswalk.csv`).

## 2. Paddy Doctor pest set
- **Identity:** Paddy Doctor: Open Dataset and Automated Pest Identification Using Pre-trained Deep Learning Models (ICLR 2024 Workshop). Authors: Petchiammal A., Pandarasamy Arjunan.
- **Access:** UNVERIFIED. The folder `Data/candidates/paddydoctor_pest_set/` turned out on 2026-10-05 to be the paddydoc GitHub *code* repository: notebooks (`cnn.ipynb`, `vgg16.ipynb`, …), Jekyll site pages and an Apache-2.0 `LICENSE` for the code. It contains no pest images, and its `dataset.md` describes the 13-class disease dataset, not the pest set. The 6,062 / 17-class figures below are from the paper and were not checked against data.
- **Licence:** UNVERIFIED for the images. Apache-2.0 covers only the repository code.
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
- **Identity:** Hossain, M. F., Abujar, S., Noori, S. R. H., & Hossain, S. A. (2021). *Dhan-Shomadhan: A Dataset of Rice Leaf Disease Classification for Bangladeshi Local Rice.* Mendeley Data, V1, 6 April 2021. DOI 10.17632/znsxdctwtt.1. Daffodil International University; images from the Dhaka Division, Bangladesh.
- **Access:** Open download. Local copy: `Data/candidates/dhan_shomadhan/` (source) and `Data/dhan-shomadhan/` (renamed per class).
- **Licence:** CC BY 4.0, read on the Mendeley page on 2026-10-05. Redistribution allowed: Yes.
- **Content:** 1,106 images across 5 diseases, on field and white backgrounds. Class folder names are misspelled in the source ("Browon Spot", "Leaf Scaled", "Rice Turgro", "Shath Blight").
- **Mapping to Rice MMKG (applied):**

  | Source class | Images | `annotatedAs` |
  |---|---:|---|
  | Rice Blast | 272 | `Rice_Blast_Disease` (exact) |
  | Rice Tungro | 195 | `Rice_Tungro_Disease` (exact) |
  | Brown Spot | 139 | `Brown_Spot` (exact) |
  | Sheath Blight | 283 | `Sheath_Blight` (exact) |
  | Leaf Scald | 217 | `Leaf_Scald` (new individual, exact) |

  The background goes in `environmentCondition` ("Field Background" / "White Background").
- **Gap closed:** Diseases with images: 8/15 → 10/16. `Sheath_Blight` gets its first images. `Leaf_Scald` is a disease the ontology did not have, so the denominator also grows.
- **Status: IMPORTED 2026-10-04** (commit `0307244`), completed 2026-10-05: dataset metadata (DOI, citation, licence URI), `environmentCondition` declared, and `Leaf_Scald` given its pathogen, symptom, controls and provenance. See `Worklog/2026-10-05_antigravity_review/SUMMARY.md`.
- **Issues:** Small classes (139–283 images). No overlap check with Paddy Doctor was run; overlap is unlikely, since the two datasets come from different countries.

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
| Category | Before (Kaggle only) | Now (2026-10-05: Paddy Doctor IEEE + Dhan-Shomadhan) |
|---|---|---|
| Pests | 1/7 | 3/7 (`Hispa`, `Stem_Borer`, `Leaf_Folder`) |
| Diseases | 8/15 | 10/16 (adds `Sheath_Blight` and the new `Leaf_Scald`) |

Black and white stem borer images (1,779) stay `annotatedAs Deadheart` until decision 5 of the 2026-09-30 meeting.

## Candidates uploaded to `Data/candidates/` (reviewed 2026-10-05)

These files were in `Data/candidates/` but had no entry above. They were profiled locally on 2026-10-05. None closes an image gap. Three of them could feed the sensor / remote-sensing / field schema added on 2026-10-04.

| Dataset (local file) | Modality | Licence (as found locally) | Rice-specific? | Fits Rice MMKG | Recommendation |
|---|---|---|---|---|---|
| Rice Disease Risk Assessment v1.0 (`Rice Disease Risk Assessment Dataset v1.0.zip`) | tabular soil + weather, georeferenced plots | CC BY 4.0 (`LICENSE.txt`, DataPort page) | Yes | `SensorObservation` + `FieldLocation` | **Imported 2026-10-05**: 186 real rows; 50 CTGAN-synthetic rows excluded |
| AgriVision Maharashtra (`AgriVision_Maharashtra_ML_Features_GSMaP_2017_2025.csv` + sampling points + `DATA_DICTIONARY.csv`) | weekly NDVI (satellite), GSMaP rainfall, temperature at 167 points | **not stated** | No (cropland points, crop not recorded) | `RemoteSensingObservation` + `FieldLocation` | Later: ask for source and licence |
| IRDD (`Main Folder.zip`) | image | **not stated** in the zip | Yes | `Brown_Spot` only | Dropped; local file deleted 2026-10-06 |
| RidgeNet public subset (`RidgeDataset.zip`) | UAV RGB + segmentation masks | per IEEE DataPort record (not in zip) | No (farmland ridges, China) | none | Dropped; local file deleted 2026-10-06 |
| Crop Classification (`Crop_Classification_dataset.xlsx`) | tabular Sentinel-2 bands + indices + soil | **not stated** | Partly (¼ rice) | weak | Dropped (provenance unknown, likely synthetic); local file deleted 2026-10-06 |
| Crop Recommendation (`Crop_recommendation.xlsx`, `Crop Recommendation dataset.zip`) | tabular N, P, K, pH, weather → crop | **not stated** | No (22 crops) | none | Dropped; local files deleted 2026-10-06 |
| Fertilizer Prediction (`Fertilizer Prediction.csv`) | tabular | **not stated** | No (11 crops) | none | Dropped (synthetic); local file deleted 2026-10-06 |
| AgriSense Synthetic (`AgriSense_Synthetic_Dataset.zip`) | tabular, synthetic by its own README | — | No (tomato, potato, wheat, cotton) | none | Dropped; local file deleted 2026-10-06 |
| RiceDO v2 + TreatO v2 (`*.owl.zip`) | OWL ontologies (OWL/XML) | not stated in the files | Yes | comparator, not data | Use for alignment / comparison (task item A4) |

### Rice Disease Risk Assessment v1.0
- **Identity:** Tripathy, S. K. (2026). *Rice Disease Risk Assessment Dataset v1.0.* IEEE DataPort, published 21 July 2026, DOI 10.21227/jdj9-x485 (resolved 2026-10-05). KIIT Deemed to be University, Bhubaneswar. DataPort access is *subscription required*, although the licence is CC BY 4.0; the local copy came from the zip.
- **Licence:** CC BY 4.0, from the bundled `LICENSE.txt`.
- **Content (verified):** 236 rows, one per plot, from 3 farms (Riverdale 117, Sunrise 66, Greenfield 53) around 18.72–18.81 °N, 84.12–84.20 °E (Ganjam district, Odisha). Columns: plot ID, farm, lat/long, pH (5.50–7.13), EC (0.20–0.89 dS/m), organic carbon (0.40–0.75 %), available N (169–312 kg/ha), P (7.8–33.8 kg/ha), K (289–346 kg/ha), temperature (26.2–33.8 °C), humidity (58–95 %), rainfall (20–276 mm), and `Disease_Risk` (Low 89 / Medium 76 / High 71).
- **Mapping:** each row → one `SensorObservation` with `hasSpatialLocation` to a `FieldLocation` (`hasLatitude`, `hasLongitude`). The values map to `hasSoilPH`, `hasNitrogenLevel`, `hasPhosphorusLevel`, `hasPotassiumLevel`, `hasTemperature`, `hasHumidity` and `hasRainfall`; the units match the property definitions. EC and organic carbon have no property yet.
- **Synthetic rows (found 2026-10-05):** 50 of the 236 rows have a Plot_ID containing `CTGAN` (Greenfield 3, Riverdale 32, Sunrise 15), i.e. generated with a conditional tabular GAN. Neither the README, the description PDF nor the DataPort page says so. 15 of the real rows merge two or three plots (`Riverdale_10,11`, `Riverdale_57,58,59`, …), and three plots share one coordinate.
- **Status: IMPORTED 2026-10-05.** 186 non-synthetic rows → 186 `SensorObservation` + 184 `FieldLocation`; new properties `hasElectricalConductivity`, `hasOrganicCarbon`; risk class in `sourceLabel`. Script: `Worklog/2026-10-05_antigravity_review/scripts/import_rice_disease_risk.py`. CQ-20 0 → 186.
- **Issues:**
  - `Disease_Risk` does not name a disease, so it cannot link to any `Disease` individual. Keep it as a literal or leave it out.
  - No observation date.
  - EC ≤ 0.89 dS/m, so no row is saline: the dataset does not give `Salinity_Disorder` any evidence.

### AgriVision Maharashtra
- **Content (verified):** 33,655 weekly rows, 2017-01-01 to 2025-12-17, at 167 points in 31 Maharashtra districts. The points were chosen by agricultural grid sampling at ≥ 50 % cropland. Per week: NDVI, GSMaP rainfall (mm) and temperature (°C), plus lag, rolling and seasonal features engineered for an NDVI-forecast model.
- **Issues:**
  - The crop at each point is not recorded, so nothing ties a row to rice.
  - No author, source or licence in the files.
  - Most columns are model features, not observations. Only NDVI, rainfall and temperature are raw.
- **Mapping if cleared:** `RemoteSensingObservation` (`hasNDVI`, `recordedAtDate` = `Week_Start`) and `SensorObservation` (`hasRainfall`, `hasTemperature`), each with a `FieldLocation`.

### IRDD (Indian Rice Disease Dataset), local `Main Folder.zip`
- **Content (verified):** `CSV_File.xlsx` lists 73 images, all `BrownSpot`, with capture time (Morning 27, Noon 25, Evening 21). The zip holds 72 JPEGs: 68 unique and 3 groups of byte-identical duplicates. One listed image is missing.
- **Issues:** single class already well covered (1,396 brown spot images); no licence in the zip; duplicates.

### Other files
- **RidgeNet subset:** 200 UAV images (2048 × 2048) + 200 ridge masks, labelled by field type, season and flight altitude. The README defers licence and citation to the IEEE DataPort record. There are no rice or disease labels.
- **Crop Classification:** 50,020 rows with four perfectly balanced crops (rice, maize, coconut, sugarcane, ≈12,500 each) and stress levels. Band values mix reflectance (0–1) with raw digital numbers (up to 5,762) in the same columns, and the source is unknown. Treat as synthetic.
- **Crop Recommendation:** 2,200 rows, exactly 100 per crop for 22 crops. The second zip is a train/test split of another crop table. Neither has a disease or rice-specific signal.
- **Fertilizer Prediction:** 100,000 rows over 11 crops (9,103 "Paddy") with near-uniform class counts, consistent with a synthetic set.
- **AgriSense:** its README states it is synthetic ("This is not real farm data") and covers no rice.
- **RiceDO v2 / TreatO v2:** OWL/XML, ontology IRIs `http://purl.org/ricedo` and `http://purl.org/treato` (dated 20-03-2021), 250 and 104 declarations, with opaque IDs (`RiceDO_000001`, …). They are the comparator listed as task item A4. rdflib cannot read OWL/XML, so a comparison needs owlready2 or the OWL API.

## IEEE DataPort search (2026-10-06)

Searched IEEE DataPort for rice datasets that could close the open gaps (pest images, abiotic disorders, remote sensing, text). Record pages were read on 2026-10-06; no file was downloaded, so contents are as described on each page. Every record below is *subscription required*, and none states a licence on its page.

| Dataset (DOI) | Modality | Content, per the record page | Fits Rice MMKG | Recommendation |
|---|---|---|---|---|
| Multi-Temporal UAV Multispectral Dataset, paddy rice (10.21227/xq3a-8n91) | UAV multispectral, tabular | Boruah, IIT Kharagpur, 2026. One CSV (1.63 MB): 3,901 frame-level observations over 7 flight dates, Kharif 2025, Debra and IIT Kharagpur, West Bengal. NDVI, NDRE, GNDVI, reflectance, flight attitude, solar geometry. No disease or pest label | `RemoteSensingObservation` (`hasNDVI`, `recordedAtDate`); rice-specific, unlike AgriVision | **Downloaded and profiled 2026-10-06** (see below); import pending a decision on granularity and on the NDVI values |
| YOLO-RLD (10.21227/dgvk-me89) | image + lesion bounding boxes | Zhang. Paddy Doctor images re-annotated in YOLO format; bacterial leaf blight, bacterial leaf streak, blast, brown spot, tungro, plus healthy negatives. Record page returned 403; details from the search index only | Lesion boxes for images already in the graph (CQ-18 symptom grounding), if file names match Paddy Doctor IDs | Blocked: the record page and its DOI return HTTP 403 while other DataPort records return 200 (checked 2026-10-06), so the record is not publicly viewable. Ask the submitter, or re-check later |
| IMPaCT-UAV-MsRGB | UAV multispectral + RGB | 42,430 raw images (≈415 GB), Vijayawada, Andhra Pradesh, nursery to harvest. No disease labels | `RemoteSensingObservation`, but raw imagery only | Later: too large, and index values would have to be computed |
| Karnataka Soil (10.21227/nqjf-7784) | tabular soil + climate | 5.31 MB; rice, maize, finger millet, sugarcane; "gathered from different sources" | weak | Drop: provenance unclear, a crop-recommendation table like those already dropped |
| Semantic-Aware IoT Dataset for Smart Agriculture (10.21227/xnk1-yn46) | tabular | 60,000 *simulated* samples; crop not named | none | Drop: synthetic |
| Paddy Disease Effected Images (10.21227/xzhf-tk14) | image | "Files have not been uploaded for this dataset" | none | Drop: empty record |
| Paddy Leaf Disease Detection Project Report (10.21227/xgeh-7321) | PDF report | One PDF; images taken from Kaggle | none | Drop |
| Paddy crop and weeds digital image dataset (10.21227/w4r4-wg46) | image | 7.77 GB; paddy, grass weeds, broadleaved weeds, sedges; no disease or pest label | none (weeds are not modelled) | Drop: out of scope |
| Context-Aware Multimodal Augmented PlantVillage (10.21227/9jat-r836) | image + text | 3,900 symptom text prompts, 38 classes, 14 crops; the page does not list the crops, and PlantVillage itself has no rice class | none expected | Drop unless rice is confirmed |

**Result:** IEEE DataPort has no rice pest image set beyond Paddy Doctor, no image set for abiotic disorders, and no rice text corpus. The one new usable lead is the West Bengal UAV multispectral CSV. Pest images for `Brown_Planthopper`, `Armyworm`, `Rice_Bug` and `Nephotettix_Virescens` still have to come from outside DataPort (IP102, or the rice pest dataset of PMC10828557).

### Multi-Temporal UAV Multispectral Dataset (profiled 2026-10-06)
- **Local copy:** `Data/candidates/Multi-Temporal UAV Multispectral, paddy rice/DJIM3Mspatiotemporaldata.csv` (1.71 MB).
- **Content (verified):** 3,901 rows × 40 columns, one row per image frame, no missing values, no duplicate rows. Each frame has its own WGS84 coordinate and a UTC timestamp (frames about 2.4 s apart).
- **Fields and dates:** 3 fields, 11 flights, 7 dates (2025-08-26 to 2025-10-17).
  - `debra` / `field1` (22.3836 N, 87.5201 E): 2025-09-09 (446), 09-18 (402), 10-09 (409), 10-17 (83)
  - `debra` / `field2` (22.3839 N, 87.5182 E): 2025-09-09 (501), 09-18 (557), 09-26 (563), 10-09 (530), 10-17 (66)
  - `nalanda` / `field3` (22.3147 N, 87.3156 E, IIT Kharagpur campus): 2025-08-26 (171), 09-08 (173)
- **Columns:** band means as digital numbers and as `REF_*` values (NIR, red, green, red edge); NDVI, NDRE and GNDVI from each; per-frame slope and intercept; flight and gimbal attitude; relative height; solar zenith and azimuth.
- **Flight height:** about 3–4.5 m above take-off for nine flights; the two 2025-10-17 flights are at 30 m (149 frames, 148 of them with an oblique gimbal).
- **Issues:**
  - NDVI is low for a rice canopy: `NDVI_Reflectance` 0.12–0.32 (mean 0.23), flight means 0.19–0.26. Red edge exceeds NIR in most frames, so NDRE is mostly negative. `REF_*` values are in the hundreds to thousands, not 0–1 reflectance. The values are internally usable as a time series but are not comparable with satellite NDVI.
  - `NDVI_Reflectance` equals `NDVI_DN` × `NDVI_Slope` + `NDVI_Intercept` exactly, i.e. it is a per-frame linear rescaling of the digital-number index, not an index computed from calibrated reflectance. `NDVI_DN` itself is not the band-mean formula applied to the stored `DN_*` columns (difference up to 0.08), so it was computed some other way, probably per pixel; the file does not say.
  - No crop growth stage, variety, plot treatment, disease or pest label. Nothing links a frame to a `Disease`, `Pest` or `EnvironmentalFactor`.
  - No licence on the record page; DataPort access is subscription required.
- **Mapping if imported:** `RemoteSensingObservation` with `hasNDVI` (= `NDVI_Reflectance`), `recordedAtDate` (= `Timestamp`), `hasSpatialLocation` → `FieldLocation`. NDRE and GNDVI have no property yet.
- **Granularity options:** (a) one observation per frame, 3,901 observations and 3,901 locations; (b) one per field and date, 11 observations and 3 locations, NDVI as the flight mean. Option (b) matches the comment on `RemoteSensingObservation` ("a value … over a field or monitoring point") and keeps the graph small.
