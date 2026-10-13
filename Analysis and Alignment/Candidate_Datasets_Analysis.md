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

## BRIN data repository (RIN Dataverse, data.brin.go.id), searched 2026-10-09

The repository is a Dataverse 6.3 instance with an open search API. 42 queries in Indonesian and English (padi, hama padi, penyakit padi, wereng, blas, tungro, penggerek batang, walang sangit, citra satelit, NDVI, drone, sensor tanah, genom padi, and others) returned 2,135 distinct datasets; 155 mention rice in the title, description or keywords. About 100 of those are 2018 deposits of LIPI publications (a PDF plus its tables and figures). Metadata and licence were read through the API for ten datasets; two were sampled.

| Dataset (handle `20.500.12690/RIN/…`) | Modality | Content | Licence | Possible mapping | Recommendation |
|---|---|---|---|---|---|
| **Alat Pengidentifikasi Wereng Batang Coklat, YUKE-WBC** (`Y9TDVS`) | Image | Suwarningsih, BRIN, 2025. 297 photos (189 MB) of brown planthopper, *Nilaparvata lugens*, on rice stems; taken Feb–May 2025 in Sleman, Bantul and Kulon Progo, Yogyakarta. No per-image label file: the whole set is one class | CC0 1.0, files open | `ImageObservation` `annotatedAs` `Brown_Planthopper`, the first images for that pest (pests with images 3/7 → 4/7) | **Imported 2026-10-13**: 66 images, one per shooting sequence (see the local check below) |
| **Dataset Fenologi Padi Kabupaten Indramayu, Sentinel-1, 2024** (`QPZZVX`) | Remote sensing (SAR) + field survey | Hendriawan Nur, BRIN, 2025. One table, 5,007 rows × 26 columns: 353 surveyed field points in 26 sub-districts, each with coordinates, planting date, visit date, variety, land type, days after planting, phenology phase, and Sentinel-1 values (VV, VH, RPI, RVI, NDPI, API) on 36 ten-day image dates in 2024 | "Custom", no text given | `RemoteSensingObservation` + `FieldLocation`, with a field-level link to `GrowthStage` and to `Variety` (Ciherang 174 points, Inpari 32 72 points — both already in the graph) | **Best remote-sensing candidate**: the first one with a link into the domain layer. Blocked on the licence; ask the author |
| Analisis Ketahanan Padi Gogo dan Padi Sawah terhadap Empat Ras Blas (`1KEJYI`) | Tabular + paper | LIPI, 2018. Reaction of 22 lines and varieties to blast races 033, 073, 133 and 173; PDF and three tables | CC0 1.0 | `ResistanceAssessment` against `Rice_Blast_Disease`, with the race in `testedPopulation` | Later: fits the existing pattern, but most lines are local accessions that would be new `Variety` individuals |
| Pleiades Neo Klaten, segmentasi fenologi sawah (`LZLZBO`) | Satellite image patches | BRIN, 2026. 56 patches of 512 × 512 at 30 cm, Klaten 2022, pixel masks for vegetative and generative phase | Research and non-commercial use, attribution to BRIN | `RemoteSensingObservation` with a two-phase label | Later: non-commercial terms do not fit a CC BY 4.0 graph |
| Sentinel-1 komposit 15-harian, fase pertumbuhan padi nasional 2025 (`DBPYL5`) | Satellite rasters | BRIN, 2025. Three national composites, 511 MB | CC BY-NC-ND 4.0, files restricted | — | Drop: restricted and no-derivatives |
| Penggunaan Atraktan … Walang Sangit (`GD0DZY`) and other 2018 LIPI deposits on rice pests and diseases (stem borer bioassay `UFAVE8`, anti-*Xanthomonas* bacteria `OAOUCB` / `1DNX7A`, stem borer mtDNA `W71PED`) | Text (paper PDF) + tables | Indonesian-language papers with their tables | CC0 1.0 | Source text for the planned extraction from research papers; `Rice_Bug` and `Stem_Borer` are covered | Later: add to the paper pool of the extraction pilot |
| Pleiades Subang / Yogyakarta paddy-field sets (`OUHCXF`, `EQI8DR`, `9M5DU2`), seed image sets (five, 2023), rice yield gap (`QAPWFQ`), nitrogen-rate data (`5WHYLN`) | Image / tabular | Land-cover masks, seed photos, yield and fertiliser data | mixed | none: no pest, disease, symptom or growth-stage link | Drop |

### YUKE-WBC, sample check
Ten of the 297 files were downloaded to the scratchpad and viewed. They are phone photos (720 × 1280 to 4000 × 2250), most with EXIF, showing one to about ten planthoppers on the lower stem and leaf sheath of rice plants; several plants stand in buckets or pots, so "field" in the description is not true of every photo. File names fall into four groups (`IMG_2025…` 186, `20250217_…` 73, `WhatsApp Image…` 22, `wbc_N` 16); one file is a resized copy of another. Species identity rests on the dataset description; nothing in the files confirms it per image.

### Indramayu phenology table, profile
- No missing values. 353 distinct points; a point has between 1 and 169 rows (median 13).
- Phase is a function of days after planting: Early Vegetative 0–19, Vegetative 1 20–39, Vegetative 2 40–64, Generative 1 65–90, Generative 2 91–120, Bare / Harvest 121–130. Days after planting come from the surveyed planting date, so the phase is field-level, not a regional calendar.
- Varieties: Ciherang, Inpari 32 HDB, Inpari 42, Gilirang and "Lain-lain" (other, 105 points).
- Values are SAR backscatter and indices, not NDVI, so `hasNDVI` does not apply; new measurement properties would be needed.
- The accompanying `.docx` holds only a link line, no description.

## Local check of four BRIN datasets (2026-10-13)

Downloaded by the user to `D:\MMKG Data\` and inspected there. Record pages open at `https://data.brin.go.id/dataset.xhtml?persistentId=hdl:20.500.12690/RIN/<code>`; the `hdl.handle.net` form of the six 2018 LIPI deposits redirects to the retired `data.lipi.go.id` and fails.

### YUKE-WBC (`D:\MMKG Data\YUKE-WBC\`)
- **Files (verified):** 297 JPEG, 189 MB, no byte-identical duplicates. One file (`20250217_103139_resized.jpg`) is a crop of its neighbour.
- **Four groups by origin:**
  - 186 `IMG_2025…` — Xiaomi M2103K19G, 4, 14 and 15 Feb 2025, no GPS.
  - 73 `20250217_…` — Samsung SM-A515F, 17 Feb 2025, all with GPS at one spot, 7.8333 °S, 110.4057 °E (Yogyakarta).
  - 22 `WhatsApp Image 2025-05-05…` — no EXIF.
  - 16 `wbc_N.jpeg` — no EXIF. Three carry a burnt-in caption naming farmer groups in Karanglewas, Banyumas (Central Java), with coordinates near 7.40 °S, 109.19 °E and 2024 dates.
- **Bursts:** the 259 timestamped photos fall into about 30 sequences (gap over 30 s) or 51 (gap over 10 s). Within a sequence the same insect is photographed repeatedly from one position; 596 photo pairs are near-identical by perceptual hash. The set holds a few dozen distinct scenes, not 297.
- **Content (90 photos viewed on three contact sheets):** every photo viewed shows at least one planthopper. Most are on the lower stem or leaf sheath of rice standing in a tub, tyre planter or bucket; one sequence shows the insect on cloth and on the planter rim, two photos on a mesh screen. Several `wbc_N` photos show pale nymphs in groups.
- **Mismatch with the description:** it says the data were collected in paddy fields across Sleman, Bantul and Kulon Progo. The GPS-tagged photos come from a single point, the plants are mostly in containers, and three photos are captioned Banyumas, 2024.
- **Species:** nothing in the files identifies the insects per image. The nymph photos and the captioned Banyumas photos in particular cannot be assigned to *N. lugens* from the files.
- **Licence:** CC0 1.0 on the dataset. The captioned photos look like third-party field reports; whether the depositor could release them is not stated.
- **Recommendation:** import, with three conditions — keep the burst structure visible (either one photo per sequence, or all photos with a sequence identifier); leave out or flag the 16 `wbc_N` files until their origin is clear; and record that species identity is as asserted by the depositor.
- **Status: IMPORTED 2026-10-13** (decision of the same day: one photo per sequence, `wbc_N` files held out).
  - Sequences: photos from one camera no more than 10 s apart, with neighbouring sequences merged when their frames are near-identical; the 22 message-app copies have no timestamp and each counts as its own sequence. 280 photos → 72 sequences; the sharpest photo of each was taken.
  - Six sequences were left out after viewing at full size: two show a plant base with no insect, one a shed skin, one a dark insect that is not recognisably a planthopper, one a spider-like arthropod, one a stem base in water.
  - Result: 66 `ImageObservation` individuals `annotatedAs Brown_Planthopper`, files in `Data/yuke-wbc/`; 44 carry `recordedAtDate`, 30 a location. The GPS position is stored as one `FieldLocation` rounded to 0.01° (7.83 °S, 110.41 °E), because all tagged photos come from a single spot that is not a field.
  - `YukeWbcDataset` is a `dcat:Dataset` with the CC0 licence, the `data.brin.go.id` record as source, and a comment stating the selection rule, the exclusions and the mismatch with the depositor's description.
  - Pests with images: 3/7 → 4/7. Scripts: `Worklog/2026-10-13_yuke_wbc_import/scripts/` (`select_yuke_wbc.py`, `import_yuke_wbc.py`).

### Fenologi padi Indramayu (`…\Fenologi padi Indramayu, Sentinel-1, 2024\`)
- Same table as profiled on 2026-10-09 (5,007 × 26, here as `.csv`), plus the `.docx` that holds only a link line. Nothing new; still blocked on the "Custom" licence.

### Ketahanan padi terhadap empat ras blas (`…\Ketahanan padi terhadap empat ras blas\`)
- **Files:** the paper (PDF), one figure, three tables as `.xlsx`.
- **Content:** Table 1 lists 21 entries with origin (breeding lines of BB Padi Bogor, national varieties such as Situ Patenggang and Danau Gaung, and local varieties from Lampung, Sukabumi, Banten, Garut, Cianjur and Bali). Table 2 gives 18 upland entries and Table 3 four lowland entries, each with a score and a reaction (T resistant, AT moderately resistant, R susceptible) against blast races 033, 073, 133 and 173.
- **Quality:** the tables are OCR output. Names differ between tables (`Bll908F-TB-2` / `B1190SF-TB-2`), four rows of Table 2 are collapsed into one cell, and digits are misread (`I`, `s`). They must be re-read against the PDF before use.
- **Mapping:** up to 88 `ResistanceAssessment` individuals against `Rice_Blast_Disease`, race in `testedPopulation`; the three grades match the three `ResistanceLevel` individuals. All 22 entries would be new `Variety` individuals.
- **Recommendation:** later. CC0 and a good fit for the pattern, but it needs manual transcription and adds varieties that nothing else in the graph refers to.

### Pleiades Neo Klaten (`…\Pleiades Neo Klaten, segmentasi fenologi sawah\`)
- 56 image patches and 56 masks as GeoTIFF (2.1 MB each), plus one `.aux.xml`. The rasters could not be opened with the Python libraries installed here, so band layout, georeferencing and class shares were not checked.
- **Recommendation:** later, unchanged: the terms allow research and non-commercial use only.

## Mendeley Data search (2026-10-13)

Searched through the site's own search API (`https://data.mendeley.com/api/research-data/search?query=…&type=DATASET`), limited to datasets hosted on Mendeley Data. 60 queries (diseases, each pest, each abiotic disorder, spectral, UAV, thermal, sensor, weather, soil, audio, video, text, QA, growth stage, variety), first 30 to 50 results each; from the first 40 queries, 241 distinct records mention rice or paddy, 180 of them in the title. Records are at `https://data.mendeley.com/datasets/<id>`. Every record below is CC BY 4.0. `Dhan-Shomadhan` (`znsxdctwtt`), already imported, is hosted here.

Three archives were downloaded and inspected; the others were judged from the record and its small files only.

### Inspected locally

| Dataset | Id | Finding | Recommendation |
|---|---|---|---|
| Paddy Field Pest Image Dataset | `y5hwbhrn5m` | Record says 22,108 smartphone photos from Bangladesh, labelled by entomologists. The archive holds 2,557 "raw" images (416 × 416) plus two augmented copies. The images are collected from the web: site watermarks (a stock-photo agency, Chinese portals), museum specimens, studio shots. The `Rice Bug` folder shows weevils, not *Leptocorisa*; `Green Leafhoppers` mixes several leafhopper species. | **Drop.** Labels do not match the ontology's pests and the depositor cannot license third-party photos. |
| Nitrogen Deficiency of Rice Crop | `gzm5pxntyv` | 5,790 images in four leaf-colour-chart classes (`swap1`–`swap4`). Each is a leaf segment of about 100 × 100 px on white; one class has 63 distinct files among 1,203. | **Drop.** Colour patches, no plant or field context; the classes are colour levels, not a diagnosis. |
| Rice Disease Image Dataset (Netrokona University) | `jw7hp6r5gj` | 4,000 images, 224 × 224, 500 per class, detached leaves on white paper. The `Potassium_Fertilizer_Deficiency` class shows yellow-orange margins and tip necrosis, consistent with the disorder. Other labels are doubtful: the README describes "Bacterial Blight" by discoloured grains, and `Rice_Ear_Borer` shows leaves with chewed margins. No expert validation is stated. | **Candidate, potassium class only**, and only after an expert confirms it. It is the only image source found for any of the six abiotic disorders. |

### Judged from the record (not downloaded)

| Dataset | Id | Size | What it would add | Recommendation |
|---|---|---|---|---|
| Proximal multispectral dataset for brown spot (Colombia) | `nz8bhz7j9t` | 6.2 GB | 2,772 captures of five bands plus RGB (DJI P4 Multispectral, 30–45 cm above the canopy), labelled healthy or brown spot by agronomists. A new modality tied to a disease already in the graph. | **Best candidate.** Download and check; needs band-level properties. The README describes the authors' code, not the files. |
| Symptom-labelled stem borer images (Bangladesh) | `hnfjs42d5g` | 1.7 GB | 2,096 original field photos labelled Healthy, Dead Heart or White Head, confirmed by an agricultural expert, with two named locations and a collection period. Labels are symptoms, and `Deadheart` exists as a `Symptom`. | **Candidate.** Would be the first images annotated with a symptom rather than a disease or pest. |
| RiceLeafDiseaseBD | `86s4jzj2m4` | 5.6 GB | 9,769 photos, six classes, 21,460 lesion boxes, varieties BRRI dhan28 and dhan29. The record promises variety, severity and growth stage per image, but the metadata table published beside the archive has only file names and sizes. | Later. Classes are already covered; boxes have no place in the schema yet. |
| Sheath blight severity | `489spnkhp5` | 4.4 GB | Field photos in six severity levels. | Later. `SeverityLevel` exists; the grading scale is not named in the record. |
| Rice leaf disease, nine classes | `n8jpkpfz5p` | 2.1 GB | 6,758 images incl. Leaf Scald, Narrow Brown Spot, Neck Blast, Sheath Blight. | Later. More images for covered classes only. |
| MINCERnet temperature and humidity in paddies | `9wjgpxbns8` | 3 MB | Canopy micro-meteorology from several countries. | Not suitable. No disease or pest observation attached. |
| Bengali QA for rice cultivation and disease | `nt8wgnk2jk` | 2 MB | 4,848 rows, 3,348 of them disease questions. Checked: Bengali only, and rows are paraphrases of a smaller set of questions. | Not suitable. |
| Visible-thermal rice field, multispectral Sri Lanka, UAV yield Vietnam, RiceTagosodes, bird acoustics | `9xg52j8tmw`, `h8s5mn52j6`, `j9v6bxbg7z`, `rpth9tp4rh`, `p6m5tmr477` | — | New modalities, but none carries a link to a disease, pest or growth stage in the graph (*Tagosodes orizicolus* is an American pest that is not in the ontology). | Not suitable. |

### What the search did not find

- No image set for `Armyworm`, `Nephotettix_Virescens` or `Rice_Bug` that can be used; queries for *Leptocorisa* and *Nephotettix* return nothing.
- No images for nitrogen, phosphorus or zinc deficiency, iron toxicity or salinity apart from the two sets above.
- No audio, video or English text resource linked to rice diseases.

## Zenodo search for other modalities (2026-10-13)

A second pass on Mendeley Data with 22 queries for non-image data (incidence surveys, light traps, pest counts with weather, resistance screening, pathogen isolates, field trials) returned nothing usable. Zenodo was then searched through its API (`https://zenodo.org/api/records`, datasets with rice or paddy in the title, 18 queries by modality). Records are at `https://zenodo.org/records/<id>`. Five small records were downloaded to `D:\MMKG Data\` (folders ending in "(Zenodo)") and inspected.

### Inspected locally

| Dataset | Id | Licence | Finding | Recommendation |
|---|---|---|---|---|
| Brown planthopper light-trap catches, China | `7630245` | CC0 | 11,567 rows: 229 trap sites with coordinates (109.98–122.06 °E, 24.14–34.89 °N), 1977–2019, six periods of five or six days in July, number caught. Source: national plant protection network (NATESC). No zero counts, so periods without a catch are probably absent rather than zero. A second sheet gives 42 annual totals for two regions. | **Best candidate.** A new kind of observation (trap count) for a pest that has images since today. Needs one count property and a period instead of a date. |
| Weekly pest surveillance, Midsayap, Philippines | `21972083` | CC BY 4.0 | 366 weekly rows, 2018–2024, one station: light-trap counts of rice black bug (*Scotinophara coarctata*) and white stemborer (*Scirpophaga innotata*), with temperature, humidity, rainfall, wind and soil wetness from NASA POWER, and moon phase. Some dates disagree with their month and week columns. | **Candidate.** Weather columns match `hasTemperature`, `hasHumidity`, `hasRainfall`. White stemborer maps to `Stem_Borer`; rice black bug is not in the ontology (`Rice_Bug` is *Leptocorisa oratorius*). Weather is reanalysis, not measured at the trap. |
| Landraces screened for brown planthopper resistance | `4450234` | CC BY 4.0 | 218 landraces plus checks Swarna and Ptb33: damage scores (0–9) in free-choice, no-choice and field screening over 2016–2018, insects per plant, and biochemical values for 42 of them. | Later. Fits `ResistanceAssessment`, but against a pest, and adds 220 varieties nothing else refers to. |
| Hyperspectral index for bacterial leaf blight severity | `20805751` | CC BY 4.0 | About 90 plots: disease index, a spectral index and band values. No coordinates, dates or varieties per row. | Later. Too little context per row. |
| Rice Pest Dataset (Vietnam) | `10442124` | CC BY 4.0 | 3,159 images; class names and five-digit file names are those of IP102. Adds life-stage folders (adult, egg, larva). | **Drop.** A subset of IP102, see section 4. |

### Judged from the record (not downloaded)

| Dataset | Id | Size | What it would add | Recommendation |
|---|---|---|---|---|
| RGB and NDVI images for nitrogen deficiency across growth stages (Tanzania) | `17983378` | 19.6 GB | 5,000 RGB and 5,000 NDVI images, four nitrogen rates (T0 none, T1 half, T2 recommended, T3 150 %), 40–90 days after planting, variety SARO 5. | **Candidate.** First images for an abiotic disorder with a growth stage. T0 with its NDVI set is 5.7 GB. The label is the treatment, not a diagnosis. |
| Light-trap images of rice black bug and white stemborer | `20066074` | 1.0 GB | Annotated trap images, four classes (species by sex). Same authors as the Midsayap table. | Later, together with the Midsayap table if rice black bug is added. |
| Hyperspectral images under salinity stress | `6515000` | 39.4 GB | Whole-plant hyperspectral images of four lines at EC 9 dS/m, CC0. | Later. Laboratory phenotyping; very large. |
| Proximal sensing of bacterial blight resistance | `10398370` | — | The record holds a poster only. | Not suitable. |

Not found on Zenodo either: audio, video, text or question-answer data on rice diseases, and images of `Armyworm`, `Nephotettix_Virescens` or `Rice_Bug`.

## Local check of three downloads (2026-10-13)

Downloaded by the user to `D:\MMKG Data\`; folder names are the record titles, cut short by the browser.

### Symptom-labelled stem borer images (Mendeley `hnfjs42d5g`)
- **Files (verified):** 2,096 original JPEG, 475 × 635, no two identical: Healthy 1,106, Dead Heart 439, White Head 551. The archive also holds 14,672 augmented copies, which were not unpacked.
- **Metadata:** no EXIF on any file. Date (January–March 2025) and the two locations (Magura and Jessore, Bangladesh) exist only in the record text, not per image.
- **Content (64 photos viewed):** field photos. Dead Heart shows a dried central shoot among green tillers; White Head shows erect, white, unfilled panicles. Both match the symptom.
- **Mapping:** Dead Heart → `Deadheart`, which already has 1,779 images from Paddy Doctor. White Head → `White_Ear`, a `Symptom` with no image; `annotatedAs` already admits symptoms in its range.
- **Recommendation: import.** The 551 White Head photos would be the first images annotated with a symptom individual. Dead Heart and Healthy add a second source for classes already covered.
- **Status: IMPORTED 2026-10-13**, all three classes, originals only. 2,096 `ImageObservation` individuals in `Data/stem-borer-bd/`: 551 `annotatedAs White_Ear`, 439 `Deadheart`, 1,106 `Normal_Health`. `StemBorerSymptomDataset` records the licence, the DOI, the citation, and that date and site are known for the collection only, not per image. No schema change. Script: `Worklog/2026-10-13_stem_borer_import/scripts/import_stem_borer.py`.

### Proximal multispectral brown spot (Mendeley `nz8bhz7j9t`)
- **Files (verified):** 236 captures per class, 472 in all, each one RGB JPEG and five 16-bit TIFF bands (1600 × 1300), readable with PIL. The record states 2,772 sets and over 13,000 TIFF files; the archives hold 2,360 TIFF files.
- **Metadata:** every capture is from 25 October 2025. Diseased: 11:58–12:28, a strip about 70 m long at 5.159 °N, 72.400 °W. Healthy: 12:30–12:53, 192 captures from a second plot about 170 m away and 44 from the end of the first strip.
- **Content (20 captures viewed, one pair at full size):** canopy views from close range. Brown lesions are visible on the leaves of the diseased capture. The diseased plot is a dense ripening crop; the healthy plot is a younger, flooded crop at heading with standing water in the frame.
- **Limits:** the class is the plot. Disease is confounded with growth stage and background, so band differences between the classes cannot be read as an effect of the disease (raw NIR/red ratio is higher in the diseased sample because the healthy frames contain water). The TIFF values are raw digital numbers, not reflectance.
- **Mapping:** would be the first individuals of `RemoteSensingObservation`, `annotatedAs Brown_Spot` or the healthy status, with date and one `FieldLocation` per plot. The schema has `hasNDVI` but no way to point at band files.
- **Recommendation: candidate.** Sound as a small, dated, located multispectral record of brown spot; not sound as evidence of a spectral signature. Needs a decision on how band files are referenced.

### RGB and NDVI images for nitrogen deficiency (Zenodo `17983378`), T0 only
- **Files (verified):** `T0` 1,467 JPEG; `T0_NDVI` 1,288 JPEG plus macOS resource files.
- **Metadata:** RGB photos come from a Google Pixel 6 (819) and a GoPro HERO9 (648) on three days, 6, 7 and 16 September 2025, at 6.848 °S, 37.655 °E (Morogoro, Tanzania); the record names a GoPro Hero 10 and a span of 40–90 days after planting. The near-infrared files carry a camera clock that was never set (January and February 2021) and GPS 0, 0.
- **Content (48 photos viewed):** single hills from above on dry red soil. The plants are green; no yellowing is evident at thumbnail size. The second set is raw red-green-NIR frames from a MAPIR Survey3, not NDVI values.
- **Limits:** the label is the fertiliser treatment (no nitrogen applied). Nothing in the files shows that a given plant is deficient, and no growth stage can be attached per image.
- **Recommendation: not suitable.** The remaining treatments (T1–T3, 14 GB) do not need to be downloaded.

## Search for abiotic disorders (2026-10-13)

Target: images or other observations for the six abiotic disorders (nitrogen, phosphorus, potassium and zinc deficiency, iron toxicity, salinity), none of which has an image in the graph. Twelve queries each on Zenodo (full text, not title only), Figshare, Harvard Dataverse, DataCite and Hugging Face, and on Kaggle through its public listing API; one web search. Nothing was downloaded.

### Images

| Dataset | Where | Licence | Covers | Finding | Recommendation |
|---|---|---|---|---|---|
| Nutrient-Deficiency-Symptoms-in-Rice (W. Raksarikon) | Kaggle `guy007/nutrientdeficiencysymptomsinrice`, 1.0 GB | **Unknown** (as listed by Kaggle) | N, P, K | The set used by most papers on the topic; a 2024 IEEE Access paper reports 1,155 leaf images in three classes. Deficiency was produced by withholding one nutrient. | **Blocked on licence.** Worth asking the owner; nothing else covers phosphorus. |
| Rice Disease Image Dataset (Netrokona) | Mendeley `jw7hp6r5gj` | CC BY 4.0 | K | Checked above: 500 photos of detached leaves, plausible symptoms, no expert validation. | Candidate after expert confirmation. |
| Nitrogen deficiency for rice crop | Kaggle `myominhtet/…` | CC BY 4.0 | N | A copy of the Sambalpur University leaf-colour-chart patches (Mendeley `gzm5pxntyv`), already dropped. | Drop. |
| RGB and NDVI, four nitrogen rates (Tanzania) | Zenodo `17983378` | CC BY 4.0 | N | Checked above: label is the treatment; no visible symptom. | Not suitable. |
| Hyperspectral images under salinity | Zenodo `6515000`, 39 GB | CC0 | Salinity | Whole plants of four lines in the laboratory. | Later. |

No image set was found for zinc deficiency or iron toxicity.

### Other kinds of data

| Dataset | Where | Licence | Covers | Content | Recommendation |
|---|---|---|---|---|---|
| Abiotic stress maps for rice (STRASA / AfricaRice) | Harvard Dataverse `10.7910/DVN/SPDA4S`, `TVDZ4Q`, `SBQ9OJ`, `XZYV58` | CC0 | Iron toxicity, salinity | Tables and rasters for Africa: area of rainfed lowland rice on soils with high iron content, probability of saline or sodic soil. | Candidate for a later risk-map layer; regional, not per field. |
| Salinity tolerance loci, high-throughput phenotyping | Zenodo `4936155`, 154 MB | CC0 | Salinity | Growth and transpiration of 553 genotypes under salt, with genotype data. | Later. Fits variety tolerance, not observation. |
| Leaf colour chart and SPAD against leaf nitrogen, jasmine rice (Thailand) | Harvard Dataverse `10.7910/DVN/XK5NOP` | CC0 | N | Field experiment files from 2003 in several formats. | Later. Supports a threshold for nitrogen status, no images. |
| Phenotyping for zinc deficiency tolerance (JIRCAS) | Harvard Dataverse `10.7910/DVN/M7KJWA` | CC0 stated | Zn | One table; the file itself is access-restricted (HTTP 403). | Blocked on access. |
| Raman spectroscopy of salinity and N, P, K deficiency; of aluminium and iron toxicity | Figshare `13127093`, `19770646` | CC BY 4.0 | N, P, K, salinity, iron toxicity | Supplementary PDF of each paper; no spectra as data files. | Not suitable as data; the papers are sources for the text pilot. |
| Thermal imaging of rice drip-irrigated with saline water | Figshare `21545945` | CC BY 4.0 | Salinity | Figures of the article, not an image set. | Not suitable. |

### Local check and import of the Kaggle N/P/K set (2026-10-13)

- **Files (verified):** 1,156 JPEG, no two identical: nitrogen 440, phosphorus 333, potassium 383. Each is a crop of one leaf (long, narrow frames).
- **Metadata:** every photo is from an Apple iPhone 11 on 30 May, 1, 2, 4 or 18 June 2020; 906 carry GPS, all at one position (14.565 N, 100.499 E, central Thailand).
- **Content (64 photos viewed):** leaves on the plant, with yellowing (nitrogen) or drying and discoloured tips and margins (phosphorus, potassium).
- **Status: IMPORTED 2026-10-13 on the user's decision, with the licence open.** Kaggle lists the licence as "Unknown"; the user is asking the owner. `NutrientDeficiencyKaggleDataset` has no `dcterms:license` and states the situation in `dcterms:rights`; the files are in the local `Data/nutrient-deficiency-kaggle/` only. All photos carry `recordedAtDate`, 906 a location rounded to 0.01 degree. **To be removed if permission is refused.**
- **Netrokona potassium class: IMPORTED 2026-10-13 on the user's decision, without expert confirmation.** 500 photos in `Data/netrokona-rice/`, `annotatedAs Potassium_Deficiency_Disorder`; `NetrokonaRiceDataset` states that the label is not validated and why the other seven classes were left out.
- Diseases with images: 10/16 to 13/16. Script: `Worklog/2026-10-13_abiotic_import/scripts/import_abiotic.py`.

### Result

An openly licensed image set for the abiotic disorders does not exist in these repositories. The realistic routes are: the licence of the Kaggle N/P/K set (three disorders at once), expert confirmation of the Netrokona potassium class, or symptom figures taken from CC BY papers during the text pilot.
