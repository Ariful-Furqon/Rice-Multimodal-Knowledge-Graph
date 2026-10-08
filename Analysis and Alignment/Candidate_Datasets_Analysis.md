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
| AgriVision Maharashtra (`AgriVision_Maharashtra_ML_Features_GSMaP_2017_2025.csv` + sampling points + `DATA_DICTIONARY.csv`) | weekly NDVI (satellite), GSMaP rainfall, temperature at 167 points | **not stated** | No (cropland points, crop not recorded) | `RemoteSensingObservation` + `FieldLocation` | Later. Source found 2026-10-06: IEEE DataPort record `agrivision-maharashtra-agricultural-vegetation-and-climate-dataset-next-week-ndvi`; licence still to be checked |
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
| Multi-Temporal UAV Multispectral Dataset, paddy rice (10.21227/xq3a-8n91) | UAV multispectral, tabular | Boruah, IIT Kharagpur, 2026. One CSV (1.63 MB): 3,901 frame-level observations over 7 flight dates, Kharif 2025, Debra and IIT Kharagpur, West Bengal. NDVI, NDRE, GNDVI, reflectance, flight attitude, solar geometry. No disease or pest label | `RemoteSensingObservation` (`hasNDVI`, `recordedAtDate`); rice-specific, unlike AgriVision | **Deferred (decision 2026-10-06): kept as a candidate, not imported.** Profiled below. Revisit if the licence is confirmed and something links the flights to the domain layer (e.g. growth stage per flight date) |
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

## IEEE DataPort search, round 2: other modalities (2026-10-06)

All 24 listing pages of the DataPort *Agriculture* topic tag (about 230 records) were read on 2026-10-06, looking for rice data in a modality the graph does not hold yet (text, remote sensing, pest counts, weather series). Record pages only; nothing was downloaded. Every record below is *subscription required* and states no licence.

| Dataset (DOI) | Modality | Content, per the record page | Possible mapping | Recommendation |
|---|---|---|---|---|
| ROSE, Real Observation SITS Evaluation (10.21227/h63f-wd44) | Satellite time series (Sentinel-2) | Gao, AIR-CAS, 2026. 1,271 georeferenced 128 × 128 chips on the 10 m grid, Jiangsu, autumn crop season 2025; 10 bands with acquisition dates; labels rice / maize / other; "phenology metadata" provided. 13.95 GB | `RemoteSensingObservation` + `FieldLocation`; the phenology metadata could tie an observation to a `GrowthStage`, which the UAV file cannot | **Checked locally 2026-10-07: not suitable for now** (see below). Phenology is a county-level calendar, not per sample |
| LeafNet (10.21227/epxf-hr31) | Image + text | Nguyen Quoc et al., 2025. 186,000+ leaf images, 97 disease classes, 22 crop species, with disease symptom descriptions "curated from reputable sources". 10.95 GB. The page does not list the species | Text modality: symptom descriptions per disease class, comparable with the `indicatedBy` assertions | **Checked locally 2026-10-07: not a text modality** (see below). Rice is included, but the text is one sentence per class |
| Solar Insecticidal Lamps IoT (10.21227/9mqx-vd10) | Sensor + pest counts | Li, Shu et al., Nanjing Agricultural University. 16.7 M rows, Nov 2023 – Feb 2024: insect-kill pulse counts, air temperature, humidity, light. Crop, location and insect species not stated | `SensorObservation`; kill counts would need a new property and name no `Pest` | Later: ask the authors for crop and site. Winter months, so few rice pests expected |
| Insecticidal Counting, one lamp and two cameras (10.21227/p189-v183) | Video + counts | Same group. Aug – Oct 2021, about 178 GB of video plus a count table. Crop and species not stated | as above | Drop: size, and no species |
| RMPS, Rupnagar Maize Paddy Sugarcane (10.21227/rfed-3z84) | Satellite (PlanetScope, 3 m) | 32 scenes, May – Nov 2023, Rupnagar, Punjab; crop-type ground truth. 23.79 GB | `RemoteSensingObservation`, crop type only | Drop: raw scenes, PlanetScope redistribution terms, no label beyond crop |
| Dataset for Smart Precision Agriculture System in Bangladesh (10.21227/5j31-8a73) | Tabular | District, crop, season, area, production, min/max temperature and humidity; survey-based. 259 KB | none without a pest or disease variable | Drop |
| Paddy Field, Palakkad (10.21227/bs7k-vq76) | JPEG archive | 639 MB; described as geospatial data on paddy cultivation; no period, no schema; same submitter as the empty "Paddy Disease Effected Images" record | unclear | Drop |
| Information on soil samples (10.21227/y1jt-7z38) | Tabular | One 14 KB sheet: acquisition date, colour, paddy region flag, soil organic matter. No coordinates or location | none | Drop |
| Dataset for Agriculture Pest Images (10.21227/xmfd-k187) | Image | 17.46 GB; aphids, leafhoppers, beetles, caterpillars "across different plants"; no class list, origin not stated | none confirmed | Drop unless a rice class list appears |
| IP102 (10.21227/xmzb-r507) | Image | Third-party upload, two zips of 21 MB and 9.5 MB, so not the full image set | none | Drop: use the original IP102 release |
| AgriSense DataHub (10.21227/3z1c-6k42) | Weather series | 25 Indian stations, 30 days at 5-minute steps; no coordinates | none | Drop |
| AI-Based Crop Disease Prediction and Farm Advisory Platform (10.21227/w4dv-qs59) | Synthetic | Its file is `AgriSense_Synthetic_Dataset.zip`, the synthetic set already dropped and deleted on 2026-10-06 | none | Dropped |

Two records already held locally were identified by this pass: AgriVision Maharashtra, and the ridge-segmentation UAV set (dropped).

**Result:** no DataPort record supplies a new modality that maps into the domain layer as it stands. Two are worth a closer look, ROSE (remote sensing with phenology) and LeafNet (image + text), and both depend on a detail the record page does not give. DataPort has no rice text corpus, no pest occurrence series with species, and no weather series tied to a rice disease.

## Local check of ROSE and LeafNet (2026-10-07)

Both were downloaded outside the repository, to `D:\MMKG Data\` (not on OneDrive), and inspected there. Neither was imported.

### LeafNet (`D:\MMKG Data\LeafNet\`)
- **Content (verified):** 97 class folders and `class_description.json` (97 entries: class name, crop, disease name, one description).
- **Rice:** 8 classes, 13,107 images — Healthy 3,347 · Leaf Blast 3,005 · Brown Spot 2,897 · Hispa 1,981 · Bacterial Blight 827 · Leaf Scald 358 · Narrow Brown Spot 353 · Leaf Smut 339.
- **Text:** one short sentence per class, so 8 sentences for rice (e.g. leaf scald: "zonate lesions of alternating light tan and dark brown from tips or edges…"). There is no per-image text. The record says the descriptions were curated from "UME, NIH, and published studies"; no sentence carries its own source.
- **Images:** file names follow a `<class> (<n>).jpg` pattern, which points to a re-packaged public collection, not an original field campaign. No per-image origin, date, location or licence. Overlap with Paddy Doctor and Dhan-Shomadhan was not tested (the local copies of those are OneDrive placeholders).
- **Fit:**
  - As a text modality: no. Eight class-level sentences are not a corpus, and without a traceable source they cannot back an `indicatedBy` assertion under the provenance rule.
  - As images: six of the eight classes are already covered. Leaf Smut and Narrow Brown Spot would be new `Disease` individuals, each needing a sourced pathogen and symptoms first.
- **Recommendation:** do not import. Useful only as a pointer: if Narrow Brown Spot or Leaf Smut are wanted, find the original image release.

### ROSE (`D:\MMKG Data\ROSE\`)
- **Content (verified from the core archive):** 1,271 chips of 1.28 km × 1.28 km in 21 Jiangsu counties (31.40–34.81 °N, 116.45–120.76 °E); 1,176 contain rice pixels and 898 are rice-majority. 79,256 sample–overpass pairs on 129 dates, 2025-05-15 to 2025-11-29. Ten Sentinel-2 L2A bands as real surface reflectance (scale 0.0001), with cloud validity masks. The 12 tile archives (about 14 GB) were not opened.
- **Phenology:** `county_crop_broad_phenology_calendar.csv` is per county and per ten-day period, with four phases (sowing, growth, maturity, harvest). The data card states it is "not … plot-level phenology ground truth".
- **Fit:**
  - `RemoteSensingObservation` + `FieldLocation` would work, and reflectance is properly calibrated, unlike the UAV file. NDVI would have to be computed per chip and date over rice pixels only.
  - `GrowthStage`: only by joining a chip's county and date to the calendar. "maturity" and "harvest" match `Maturity_Stage` and `Harvest_Stage`; "growth" spans seedling to flowering and matches no single stage. The link would be a derived estimate, not something the source asserts per field.
  - No disease, pest or stress label.
- **Licence:** not stated; the data card says "follow the final license inserted by the authors before publication".
- **Recommendation:** do not import now. It is the better remote-sensing candidate (rice-specific, calibrated, dated, georeferenced), but it would still sit apart from the disease layer. Keep as a candidate alongside the UAV file.

## IEEE DataPort search, round 3: site search (2026-10-07)

DataPort's own full-text search was run for `rice`, `paddy`, `oryza`, `planthopper`, `stem borer`, `rice blast` and `rice pest`, across all categories and not only the *Agriculture* tag. It returned 188 distinct records; those not already listed above were read on their record pages. All are *subscription required* with no licence stated. `planthopper` returns nothing.

| Dataset (DOI) | Modality | Content, per the record page | Possible mapping | Recommendation |
|---|---|---|---|---|
| Paddy Crop RGB Drone Data (10.21227/jzw5-hk19) | UAV RGB image | Boruah, IIT Kharagpur, 2025 — the author of the UAV multispectral file, and the same two sites (IIT Kharagpur campus and a second West Bengal field). 224 × 224 tiles, 793 MB, labelled `healthy` / `unhealthy` by leaf colour, canopy density and texture; three folders (Internal, Ext1, Ext2). Image count, dates and georeferencing not stated | `ImageObservation` at canopy scale. `healthy` → `Normal_Health`; `unhealthy` names no disease, so it would stay a source label | **Checked locally 2026-10-07: not suitable** (see below). Tiles carry no date, coordinate or frame reference, so they cannot be matched to the multispectral flights |
| Data_Tanaman_Padi_Indonesia_2018-2023 (10.21227/xqkt-z292) | Tabular | Erlin, 2024. Province × year: harvested area, production, rainfall, humidity, temperature; from BPS and BMKG. 8.58 KB | none: no pest, disease or variety variable | Drop. For Indonesian context, BPS and BMKG are the sources to cite directly |
| RiceDO Version 2 (10.21227/5ndq-4222) and TreatO Version 2 (10.21227/5016-aw09) | OWL ontology | Jearanaiwongkul, Anutariya, Racharak, Andres, 2021. These are the two `*.owl.zip` files already in `Data/candidates/` | comparator (task item A4) | Keep. Origin of the local files now identified; licence not stated on either record |
| IP102_3CLASS (10.21227/62dp-k165) | Image | Subset of IP102: rice leaf roller, grub, *Prodenia litura*. 98 MB | `Leaf_Folder` only, already covered | Drop |
| Rice and Wheat crop yield prophesy (10.21227/bcpj-af28) | Tabular | Water level, temperature, humidity, nitrogen, yield; no place, period or source | none | Drop: provenance unknown |
| Zizania and Apple Image Dataset (10.21227/xaqb-kc20) | Image | Zizania (wild rice stem, a vegetable) quality grading | none | Drop: not *Oryza* |

**Result:** the search is now exhausted for these terms. DataPort holds no further rice dataset with a disease, pest or symptom label beyond Paddy Doctor, IRDD and the blocked YOLO-RLD record.

### Paddy Crop RGB Drone Data (checked 2026-10-07, `D:\MMKG Data\Paddy Crop RGB Drone Data\`)
- **Content (verified, archives read without extracting):** 11,650 unique JPEG tiles of 224 × 224 pixels in three sets, each split into `Healthy` and `Unhealthy`: InternalData 4,494 / 4,166 · EXT1 873 / 931 · EXT2 595 / 591. `EXT1.zip` contains all three sets; `InternalData.zip` and `EXT2.zip` are byte-identical subsets of it. No file is in both a `Healthy` and an `Unhealthy` folder.
- **Metadata:** none. The archives hold no README, no table, and the tiles have no EXIF (no date, no GPS). File names are running numbers (`h_image01.jpg`, `u_image997.jpg`). The README listed on the record page is not in the download.
- **What the labels show (48 random tiles viewed):** `Unhealthy` covers sparse canopy with soil or water visible, weed patches and uneven stands, as well as yellowing; `Healthy` covers dense canopy of varying colour, including yellow-green and heading canopy. The label is a canopy-condition judgement, not a diagnosis. Neighbouring tiles of one frame are present, so many tiles are near-duplicates.
- **Fit:**
  - Link to the UAV multispectral file: not possible. Nothing ties a tile to a field, flight date or frame.
  - `Healthy` → `Normal_Health` would be the only mapping; `Unhealthy` names no `Disease`, `Pest` or `Symptom`, and mixes crop stage and weeds with stress.
  - Canopy tiles are a different scale from the leaf images in the graph, but without location or date they add no context either.
- **Recommendation:** do not import. Useful only if the author can supply the tile-to-frame mapping and the flight dates.

## IEEE DataPort search, round 4: by modality (2026-10-08)

DataPort's full-text search was run again with 23 modality terms (hyperspectral, thermal, SAR, Sentinel, genome, weather, soil, phenology, yield, acoustic, video, text, question answering, pest sound, pest trap, light trap, sensor, IoT, nitrogen, spectral, lidar, point cloud), each paired with `rice`, `paddy`, `pest` or `agriculture`. The search matches any of the words, so it returned 1,978 records; 119 had an agriculture-related title, and the six not seen in earlier rounds were read on their record pages. All are *subscription required* with no licence stated.

| Modality | Dataset (DOI) | Content, per the record page | Recommendation |
|---|---|---|---|
| Text | AgriSci-QA (10.21227/9te6-dv79) | 11,099 question–answer pairs generated by an LLM pipeline from 348 agricultural research papers; 2.3 MB. Crops and topics not stated | **Checked locally 2026-10-08: not suitable** (see below). Rice appears, but not rice diseases or pests |
| Image + video (insects) | WF-DTS Insect dataset (10.21227/q7k4-fe73) | 8 insect species × 200 images, from a trap device; includes *Cnaphalocrocis medinalis* (rice leaf folder). 1.83 GB | Drop: `Leaf_Folder` already has 1,095 images, and none of the four pests without images is in it |
| Audio | Solar insecticidal lamp discharge sound and voltage (10.21227/53yv-c339) | 4,000 five-second recordings labelled by number of insects killed (1–4). No species, crop or place | Drop |
| Sensor | AgriField-Manipur (10.21227/kbpa-7d35) | Daily temperature, humidity, soil moisture, pH and rainfall; "field-level values are synthetically generated" | Drop: synthetic |
| Image | Eight-category leaf disease dataset (10.21227/83vs-0b86) | Corn, grape, apple, potato | Drop: no rice |
| Sensor + image | PMCS-phenology-data (10.21227/9ae9-y173) | *Dianthus* flowers | Drop: no rice |

**Result by modality:** hyperspectral, thermal, SAR, lidar, genomic, acoustic and video searches return no rice dataset. Remote sensing stays at the three candidates already listed (ROSE, UAV multispectral, AgriVision). Text has one unverified lead (AgriSci-QA).

### AgriSci-QA (checked 2026-10-08, `D:\MMKG Data\AgriSci-QA\`)
- **Content (verified, archive read without extracting):** one zip, 2.3 MB, 630 files in seven folders: `generated_qa` (100 files), `validated_qa` (132), `adversarial_qa` (91), `causal_claims` (100), `temporal_chains` (70), `critiques` (134) and two training files (`train` 2,573 and `val` 286 chat-format records). The per-paper files hold 499 question–answer pairs with a reasoning type and difficulty, 274 deliberately flawed answers, about 690 causal claims and paper-to-paper comparisons. File names give 171 distinct papers, not the 348 of the record page, and the 11,099 pairs it states are not all in this download.
- **Source papers:** mostly 2025 articles from *Smart Agricultural Technology* and *Journal of Agriculture and Food Research*, some IEEE papers and a 2017 journal issue. The subject is agricultural engineering and methods: remote sensing, machine learning, food processing, life-cycle assessment.
- **Rice:** six papers have rice in the title — transplantation detection from SAR, above-ground biomass, grain starch, seedling counting from UAV, a rice transplanter, red rice flour. None is about a rice disease or pest. 149 per-paper records and 210 training records mention rice.
- **Rice diseases and pests:** searching every record for rice blast, planthopper, stem borer, tungro, bacterial blight, sheath blight, brown spot, leaf folder, leafhopper, hispa and the pathogen genera finds only fall armyworm (a pesticide-exposure study covering rice and corn, 8 mentions) and one mention of *Rhizoctonia*. A 2024 survey of paddy disease classification is in the set, but only as a paper compared with others, about deep-learning methods.
- **Text quality:** questions and answers are machine-generated. Evidence is given as chunk identifiers (`<paper>__<section>__s7_e7`), and the source text of those chunks is not in the per-paper files; some training records carry `[TEXT NOT FOUND]` in place of evidence.
- **Fit:** none. The text is about research methods, not about symptoms, causes or treatments, so it overlaps none of the domain relations. Generated answers could not serve as a source in any case.
- **Recommendation:** do not import. This closes the text modality on DataPort: there is no rice disease or pest text there.
