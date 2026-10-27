# Other crops: candidate datasets

The supervisor asked to explore crops other than rice (noted 2026-10-27). This list comes from web searches on 2026-10-27.

**Status: not downloaded.** Image counts, classes and licences are as the hosting pages or search summaries state them, and need checking on download.

**Download location:**
- Raw downloads go to `D:\MMKG Data\other-crops\<crop>\<dataset>\`, following the rice convention.
- Nothing goes into the repository until a dataset is imported.

## Selection criteria (from the rice retrieval benchmark)

1. **Field photos, not lab photos.** Plain-background leaf photos teach the source, not the disease. On rice, the source dataset could be predicted from the image with 0.993 accuracy.
2. **The same condition in at least two independent sources,** so that leave-one-dataset-out can be run.
3. **Capture metadata** (date, plot, device), so that burst photos stay in one split.
4. **An open text source per condition** for the evidence layer: CABI datasheets, PlantwisePlus factsheets, extension sheets.

## Priority for this week

1. **IEEE DataPort sets first**, while the subscription lasts (sections A–D, about 2 GB).
2. **Tier 1 crops:** two or more independent field sources.
3. **Tier 2:** one usable source, or field status unclear.

## IEEE DataPort: full screening (2026-10-27)

**How the list was built:**
- **Searches:** DataPort's public search (`/datasets?search_api_fulltext=…`) for plant disease, leaf disease, crop disease, pest, insect trap, soil sensor, hyperspectral, and the crop names rice, paddy, maize, wheat, tomato, potato, banana, cassava, cotton, soybean, sugarcane, tea, coffee, chili, citrus and mango.
- **Pages read:** the first one to three result pages per query.
- **Checks:** each candidate's own page, for size, field status and access.
- **Access:** every entry below needs the IEEE DataPort subscription unless noted.
- **Licences:** none stated, unless noted.

**Size rule:** "small" is up to about 1 GB. Larger sets are listed separately.

### A. For Rice MMKG itself (download first)

| Dataset | Content | Size | Use | Link |
|---|---|---|---|---|
| Indian Rice Disease Dataset (IRDD) | Field photos, West Bengal; brown spot and healthy; expert-verified; CSV labels | 24 MB | Third independent brown-spot source for cross-source tests | [link](https://ieee-dataport.org/documents/indian-rice-disease-dataset-irdd) |
| Rice Disease Risk Assessment Dataset v1.0 | Tabular: 236 records, 13 fields (soil chemistry, coordinates, climate) → disease risk; Odisha; **CC BY 4.0** | 0.2 MB | Context → risk links (`increaseRiskOf`) | [link](https://ieee-dataport.org/documents/rice-disease-risk-assessment-dataset-v10zip) |
| Data_Tanaman_Padi_Indonesia_2018-2023 | Provincial harvested area and production (BPS), rainfall, humidity, temperature (BMKG) | 9 KB | Indonesian context layer | [link](https://ieee-dataport.org/documents/datatanamanpadiindonesia2018-2023) |
| RiceDO v2 / TreatO v2 | The rice disease and control ontologies already aligned to | small | Their IRIs do not resolve today; the v2 files may fix the alignment | [RiceDO](https://ieee-dataport.org/documents/ricedo-version-2-rice-disease-ontology) · [TreatO](https://ieee-dataport.org/documents/treato-version-2-rice-disease-control-ontology) |
| Multi-temporal UAV multispectral, paddy | NDVI, NDRE, GNDVI per frame; 7 dates, 3 plots, West Bengal 2025; no disease labels | 1.6 MB | Remote-sensing observations, if wanted | [link](https://ieee-dataport.org/documents/multi-temporal-uav-multispectral-dataset-solar-illumination-aware-vegetation-index) |
| Paddy Crop RGB Drone Data (optional) | UAV RGB tiles 224×224, healthy or unhealthy only; West Bengal | 793 MB | Weak labels | [link](https://ieee-dataport.org/documents/paddy-crop-rgb-drone-data) |
| Paddy Field (optional) | Kerala; JPEG; content unclear on the page | 639 MB | Check after download | [link](https://ieee-dataport.org/documents/paddy-field) |

**Skipped:**
- **[IMPaCT-UAV-MsRGB](https://ieee-dataport.org/documents/indian-multi-stage-paddy-crop-tracking-based-uav-multispectral-and-rgb-image-dataset):** 415 GB, no disease labels, CC BY 4.0.
- **[Paddy crop and weeds](https://ieee-dataport.org/documents/paddy-crop-and-weeds-digital-image-dataset):** 7.8 GB, weeds only.
- **[RMPS](https://ieee-dataport.org/documents/rmps-rupnagar-maize-paddy-sugarcane-dataset):** 23.8 GB of satellite crop-type data.
- **[Paddy Disease Effected Images](https://ieee-dataport.org/documents/paddy-disease-effected-images):** no files uploaded.

### B. Text knowledge for a crop KG (tiny, download all)

| Dataset | Content | Size | Link |
|---|---|---|---|
| Tomato plant diseases (VIIT Pune) | CSV with 9 diseases and pests plus healthy: symptoms, favourable conditions, physical, biological and chemical control with dosages, prevention; from more than 40 government and scientific sources; Mendeley copy linked | 27 KB | [link](https://ieee-dataport.org/documents/comprehensive-dataset-tomato-plant-diseases-national-predictive-analytics-and-crop-health) |
| Cotton plant diseases (same authors) | CSV with 14 classes, the same fields | small | [link](https://ieee-dataport.org/documents/comprehensive-dataset-cotton-plant-diseases-national-disease-identification-and-treatment) |

**Caveat:** these files hold facts without per-sentence sources, so in Rice MMKG terms they are candidate facts, not provenance.

### C. Field image sets, small (up to about 1 GB)

| Crop | Dataset | Content | Size | Link |
|---|---|---|---|---|
| Soybean | Soybean disease data set in natural scenes | 1,620 field images, 6 diseases, 3 farms in Heilongjiang, June–Sept 2019 | 19 MB | [link](https://ieee-dataport.org/documents/soybean-disease-data-set-natural-scenes) |
| Safflower | FieldCropLeaf | Field leaf images | 30 MB | [link](https://ieee-dataport.org/documents/fieldcropleaf-dataset-safflower-plant-leaf-images-disease-detection-and-classification) |
| Dragon fruit | PitayaLeaf | About 400 field images, 5 classes (anthracnose, brown spot, stem canker, stress, healthy), Satara; metadata CSV | 40 MB | [link](https://ieee-dataport.org/documents/pitayaleaf-real-world-dragon-fruit-plant-disease-image-dataset) |
| Chili | Guajillo chili leaves | 100 field images, 2025 season, Mexico; fungal, bacterial, viral | 89 MB | [link](https://ieee-dataport.org/documents/image-dataset-guajillo-chili-leaves-visual-classification-fungal-bacterial-and-viral) |
| Mango | Field-captured mango leaf diseases | Anthracnose, sooty mould, bacterial canker, cutting weevil, gall midge, powdery mildew, rust…; Konkan | 99 MB | [link](https://ieee-dataport.org/documents/comprehensive-field-captured-image-dataset-mango-plant-diseases-deep-learning) |
| Tomato | Real Field Crop Image Dataset | Field images, 3 sites in Sangli and Satara, leaf masks | 151 MB | [link](https://ieee-dataport.org/documents/real-field-crop-image-dataset) |
| Tea | Common diseases in Indian tea plants | 416 raw field images (healthy, diseased), Tinsukia, Assam; download the raw archive only | 176 MB | [link](https://ieee-dataport.org/documents/image-based-dataset-identification-common-diseases-indian-tea-plants) |
| Arecanut | Arecanut disease detection | About 300 field images (handheld, smartphone, drone), 6 classes, Chikkamagaluru | 254 MB | [link](https://ieee-dataport.org/documents/arecanut-disease-detection-dataset-6-classes-field-images-karnataka-india) |
| Coffee | Coffee Leaf Rust Dataset | 3-month time series from a camera system, rust severity 0–4 labelled by biologists (EAFIT); also on GitHub (tidusdavid/clr-dataset) | 511 MB | [link](https://ieee-dataport.org/documents/coffee-leaf-rust-dataset) |
| Cotton | Cotton aphids and diseases | 1,399 originals (brown spot, Verticillium wilt, aphids, healthy) augmented to 4,000; field status not stated | 812 MB | [link](https://ieee-dataport.org/documents/cotton-aphids-and-diseases-dataset) |
| Citrus | Orange fruit and leaf diseases | Black spot, greening, scab, canker, melanose, healthy; field status not stated | 64 MB | [link](https://ieee-dataport.org/documents/orange-fruit-and-leaf-diseases) |
| Citrus | Lemon leaf disease dataset | 9 classes, YOLO boxes; field status not stated | 229 MB | [link](https://ieee-dataport.org/documents/lemon-leaf-disease-dataset) |

### D. Pest trap and sensor time series (small)

| Dataset | Content | Size | Link |
|---|---|---|---|
| Adapted Hartstack pheromone traps | Corn earworm trap counts with timestamps plus weather (temperature, RH, wind, pressure); 4 fields in North Carolina | 12 MB | [link](https://ieee-dataport.org/documents/adapted-hartstack-pheromone-traps-automated-moth-counting-dataset) |
| Solar insecticidal lamp IoT | Light-trap analogue: insect-kill pulse counts plus air temperature, humidity, light, device status; Nov 2023 – Feb 2024; 16.7 M rows; crop and location not named | 332 MB | [link](https://ieee-dataport.org/documents/dataset-farmland-environmental-data-insecticidal-information-and-equipment-status-solar) |
| Rural IoT soil data | 7 LoRaWAN nodes near Gdańsk, 2023: soil moisture, temperature, pH, irradiance | small | [link](https://ieee-dataport.org/documents/rural-iot-soil-data) |

### E. Larger field sets (1–7 GB), download if space allows

| Crop | Dataset | Content | Size | Link |
|---|---|---|---|---|
| Wheat | Wheat_Rust_HLSS | Raw field photos, healthy and stem, leaf and stripe rust, Maharashtra, several growth stages | 1.3 GB | [link](https://ieee-dataport.org/documents/wheatrusthlss) |
| Banana | Banana plants across growth stages | 1,090 unlabelled field photos, Solapur; free Mendeley copy (10.17632/428ysdybvd.1) | ~3 GB | [link](https://ieee-dataport.org/documents/field-captured-dataset-banana-plants-across-growth-stages-and-early-disease-conditions) |
| Brinjal, castor, cumin, guava, papaya | Multi-Crop Leaf Disease | 1,720 field images, 41 classes | 3.0 GB | [link](https://ieee-dataport.org/documents/multi-crop-leaf-disease-dataset) |
| Soybean | MH-SoyaHealthVision | UAV and ground, rust, mosaic, semilooper; 2 seasons | 4.2 GB | [link](https://ieee-dataport.org/documents/mh-soyahealthvision-uav-dataset-disease-monitoring-and-severity-assessment) |
| Loofah | Loofah pests and diseases | 2,929 field images, Guangdong; downy mildew, 2 pests, healthy | 7.0 GB | [link](https://ieee-dataport.org/documents/loofahpestsdiseasesimage) |

### Not recommended

**Too large:**
- [COT-AD](https://ieee-dataport.org/documents/cot-adcotton-analysis-dataset): 308 GB.
- [Cherry](https://ieee-dataport.org/documents/cherry-tree-disease-detection-dataset): 39 GB, and [Peach](https://ieee-dataport.org/documents/peach-tree-disease-detection-dataset): 60 GB. Both are otherwise excellent multimodal orchard sets, with UAV, ground and multispectral images and per-tree expert labels.
- [Insecticidal lamp video](https://ieee-dataport.org/documents/insecticidal-counting-dataset-based-one-solar-insecticidal-lamp-and-two-cameras): 179 GB.

**Lab, web, PlantVillage or augmented:**
- [Raw citrus leaf](https://ieee-dataport.org/documents/raw-citrus-leaf-images): from PlantVillage.
- [Potato Disease Classification](https://ieee-dataport.org/documents/potato-disease-classification-dataset): merged from open sources.
- [Annotated Maize](https://ieee-dataport.org/documents/annotated-maize-leaf-disease-image-dataset-cnn-based-classification).
- [Bean ibean augmented](https://ieee-dataport.org/documents/bean-leaf-disease-augmented-ibean-dataset): 2.2 GB. The original iBean is free on GitHub.
- [INDTomatoMSTD](https://ieee-dataport.org/documents/indtomatomstd-multi-scale-tomato-disease-dataset-tiny-and-large-lesion-detection-using): fruit, augmented.
- [Banana anthracnose](https://ieee-dataport.org/documents/real-time-dataset-banana-anthracnose-caused-colletotrichum-spp-decay-and-disease): fruit, controlled, no redistribution.
- PlantVillage copies, ridge gourd, rose.

**Other reasons:**
- [LeafNet](https://ieee-dataport.org/documents/leafnet-large-scale-dataset-training-image-text-models-leaf-disease-identification): 11 GB, 186k images of 22 crops, image source unclear. Its per-class symptom JSON could be useful text.
- [AgriSense](https://ieee-dataport.org/documents/ai-based-crop-disease-prediction-and-farm-advisory-platform): synthetic.
- [CoSEV](https://ieee-dataport.org/documents/cosev-cotton-disease-dataset-detection-and-classification-severity-stages-and-multiple): no files uploaded.
- [Agriculture Pest Images](https://ieee-dataport.org/documents/dataset-agriculture-pest-images): 17.5 GB, crops and field status not stated.

**Download plan:**
- **A + B + C + D:** about 2 GB in total.
- **Adding E:** about 18 GB more.

## Tier 1: two or more independent field sources

### Maize
| Dataset | Origin | Content | Link |
|---|---|---|---|
| CCMT (maize part) | Ghana | 5,389 raw images; fall armyworm, grasshopper, healthy, leaf beetle, leaf blight, leaf spot, streak virus | [Mendeley bwh3zbpkpv](https://data.mendeley.com/datasets/bwh3zbpkpv) · [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10285554/) |
| TOM2024 (maize part) | Burkina Faso | Maize pests and diseases, fieldwork | [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11871477/) |
| CD&S | USA | 2,112 field images; northern leaf blight, gray leaf spot, northern leaf spot (with severity) | [arXiv 2110.12084](https://arxiv.org/abs/2110.12084v1), OSF osf.io/s6ru5 |
| Diseases of maize in the field | South Africa | Field disease images | [Univ. Pretoria](https://researchdata.up.ac.za/articles/dataset/Diseases_of_maize_in_the_field/20237613) |
| Multi-format maize leaf dataset | to check | Maize leaf diseases | [Mendeley sb4wwjs8bz](https://data.mendeley.com/datasets/sb4wwjs8bz) |

### Tomato
| Dataset | Origin | Content | Link |
|---|---|---|---|
| CCMT (tomato part) | Ghana | 5,435 raw images; healthy, leaf blight, leaf curl, septoria leaf spot, verticillium wilt | as above |
| TOM2024 (tomato part) | Burkina Faso | Tomato pests and diseases | as above |
| Real Field Crop Image Dataset | India | Field images (IEEE DataPort, above) | as above |
| Tomato Leaf Disease Classification Dataset | Pakistan | Smartphone, natural light, no controlled background; includes early and late blight | [Mendeley 3mbnb82mxd](https://data.mendeley.com/datasets/3mbnb82mxd/1) |

### Cassava
| Dataset | Origin | Content | Link |
|---|---|---|---|
| CCMT (cassava part) | Ghana | 7,508 raw images; bacterial blight, brown spot, green mite, healthy, mosaic | as above |
| iCassava 2019 (Makerere AI Lab, NaCRRI) | Uganda | 9,436 labelled and 12,595 unlabelled images, 5 classes; crowdsourced field photos | [arXiv 1908.02900](https://arxiv.org/pdf/1908.02900) (Kaggle challenge) |

### Banana
| Dataset | Origin | Content | Link |
|---|---|---|---|
| Banana Leaves Imagery Dataset | Tanzania | Healthy, Black Sigatoka, Fusarium wilt race 1; 11,767 images (Sci. Data; an earlier Harvard release has 16,092) | [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11928457/), Zenodo |
| Banana Leaf Disease Dataset of Bangladesh | Bangladesh | 2,638 raw images; healthy, Panama disease, Sigatoka | [Mendeley wzshm7ky49](https://data.mendeley.com/datasets/wzshm7ky49/1) |
| Banana Leaf Disease Images | Ethiopia | 1,288 images; healthy, Xanthomonas, Sigatoka | [Mendeley rjykr62kdh](https://data.mendeley.com/datasets/rjykr62kdh/1) |

### Coffee
| Dataset | Origin | Content | Link |
|---|---|---|---|
| RoCoLe (robusta) | Ecuador | Field, one plantation, smartphone; healthy, red spider mite, 4 rust severity levels | [Mendeley c5yvn32dzg](https://data.mendeley.com/datasets/c5yvn32dzg/2) · [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6727496/) |
| BRACOL (arabica) | Brazil | 1,747 images; leaf miner, rust, brown leaf spot, cercospora | [Mendeley yy2k5y8mxg](https://data.mendeley.com/datasets/yy2k5y8mxg) |

Shared class: leaf rust.

### Sugarcane
| Dataset | Origin | Content | Link |
|---|---|---|---|
| Sugarcane Leaf Image Dataset (2023) | field survey | 7,134 images, 12 classes (10 diseases, healthy, dried) | [Mendeley 9twjtv92vk](https://data.mendeley.com/datasets/9twjtv92vk) |
| Sugarcane Disease Dataset v2 (2024) | field, several angles | 3,358 images, 7 classes | [Mendeley 7fbnxcbnhp](https://data.mendeley.com/datasets/7fbnxcbnhp/2) |
| Sugarcane Leaf Disease Dataset (2022) | smartphone | 2,569 images; healthy, mosaic, red rot, rust, yellow | [Mendeley 9424skmnrk](https://data.mendeley.com/datasets/9424skmnrk/1) |

**Caution:** check that these are independent collections. The 2023 and 2024 sets may build on the 2022 one.

### Wheat
| Dataset | Origin | Content | Link |
|---|---|---|---|
| John Innes Centre field and glasshouse | UK | Yellow rust, brown rust, powdery mildew, Septoria, healthy; 999-image public subset (full 19,172 on request) | [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10953319/) · [Zenodo](https://zenodo.org/records/7573133) |
| FoMo4Wheat benchmark | compilation | About 4,000 images from five public sets (CerealConv, WFD, AWDD, MSWDD, LWDCD) | Hugging Face PheniX-Lab/FoMo4Wheat |
| Wheat Leaf Dataset | to check | 208 stripe rust, 97 Septoria, 102 healthy | [Mendeley wgd66f8n6h](https://data.mendeley.com/datasets/wgd66f8n6h/1) |

## Tier 2: one usable source, or field status unclear

| Crop | Dataset | Note | Link |
|---|---|---|---|
| Potato | Potato Leaf (Healthy and Late Blight), Ethiopia | Real farm, uncontrolled; small (63 late blight, 363 healthy) | [Mendeley v4w72bsts5](https://data.mendeley.com/datasets/v4w72bsts5/2) |
| Potato | Potato Leaf Disease Dataset, BARI Bangladesh | 804 original field images, 6 classes | [Mendeley d5b3fzpw3g](https://data.mendeley.com/datasets/d5b3fzpw3g/1) |
| Potato | Potato disease classification (Daffodil) | Mixed field and controlled | [Mendeley ttgtfp3vjb](https://data.mendeley.com/datasets/ttgtfp3vjb/1) |
| Apple | Plant Pathology 2020/2021 (FGVC, Kaggle) | Orchard photos, multi-label; check competition licence | Kaggle |
| Apple | AppleScab-LT | Longitudinal real-field apple scab; has time metadata | [arXiv 2608.14235](https://arxiv.org/pdf/2608.14235) |
| Cashew | CCMT (cashew part) | 6,549 raw images; one source only | as above |
| Onion | TOM2024 (onion part) | One source only | as above |
| Many | FieldPlant (IEEE Access 2023) | 5,170 plantation images, 27 classes; crops to check | [IEEE Xplore](https://ieeexplore.ieee.org/document/10086516/) |
| Many | PlantDoc | About 2,600 web-scraped images, 13 species, CC BY 4.0. Not field-collected, but usable as an extra "web" source in cross-source tests | [arXiv 1911.10317](https://arxiv.org/pdf/1911.10317) |
| Many | In-the-wild segmentation (Sci. Data 2025) | 34 hosts | [link](https://www.nature.com/articles/s41597-025-06513-4) |

## Not suitable

- **PlantVillage and its derivatives:** lab photos on a plain background, so a classifier learns the background.

## Text sources for the evidence layer

- **CABI Crop Protection Compendium datasheets:** Rice MMKG already cites CABI by DOI.
- **PlantwisePlus Knowledge Bank factsheets:** described as open access, but no licence was found; ask plantwise@cabi.org.

## What carries over from Rice MMKG

- **Carries over:**
  - the schema (Disease, Pest, Symptom, PlantPart, `indicatedBy`, `affectsPlantPart`, `controlledBy`, provenance axioms);
  - the alignment targets (AGROVOC, EPPO, NCBI Taxonomy);
  - the retrieval rules (capture groups, gold as the cause to manage, in-source and cross-source).
- **Crop-specific:** growth stages (BBCH scales exist for most of these crops) and the fact sheets.
