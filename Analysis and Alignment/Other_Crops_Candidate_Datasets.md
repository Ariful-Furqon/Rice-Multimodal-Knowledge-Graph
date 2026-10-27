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

1. **Subscription-only sets first**, while the IEEE DataPort subscription lasts.
2. **Tier 1 crops:** two or more independent field sources.
3. **Tier 2:** one usable source, or field status unclear.

## Download now: IEEE DataPort (subscription required)

These were found through web search and the DataPort keyword pages "agriculture" and "plant-disease-detection". DataPort's own search needs a login, so a logged-in search for "plant disease", "leaf", "pest" and each crop name may find more.

| Priority | Crop | Dataset | Content | Size | Link |
|---|---|---|---|---|---|
| 1 | Tomato | Real Field Crop Image Dataset (Karande & Garg) | Field images, 3 sites in Sangli and Satara, Maharashtra; leaf masks | 151 MB | [10.21227/5ytp-dr85](https://ieee-dataport.org/documents/real-field-crop-image-dataset) |
| 1 | Cotton | A Comprehensive Dataset of Cotton Plant Diseases … Treatment Guidance | **Text, not images** (CSV): 14 classes with symptoms, favourable conditions, prevention, and physical, biological and chemical controls, curated from Indian agriculture and government sites. A ready text layer for a cotton KG | small | [link](https://ieee-dataport.org/documents/comprehensive-dataset-cotton-plant-diseases-national-disease-identification-and-treatment) |
| 1 | Cotton | COT-AD: Cotton Analysis Dataset (ICIP 2025, arXiv 2507.18532) | More than 25,000 images, 5,000 annotated; leaf disease (yellowish leaf, bacterial blight leaf spot, leaf reddening, fresh), boll (boll rot, damaged, healthy), bugs (mealy bug, red cotton bug); plus drone flights over 2 farms | **308 GB**: download only the leaf, boll and bug parts if the files are split | [link](https://ieee-dataport.org/documents/cot-adcotton-analysis-dataset) |
| 2 | Brinjal, castor, cumin, guava, papaya | Multi-Crop Leaf Disease Dataset | 1,720 field images, 41 classes | | [link](https://ieee-dataport.org/documents/multi-crop-leaf-disease-dataset) |
| 2 | Chili (guajillo) | Guajillo chili leaves under field conditions | 100 field images, 2025 season, San Luis Potosí, Mexico; fungal, bacterial, viral | 89 MB | [link](https://ieee-dataport.org/documents/image-dataset-guajillo-chili-leaves-visual-classification-fungal-bacterial-and-viral) |
| 2 | Safflower | FieldCropLeaf | Field leaf images; image count unclear on the page | 30 MB | [link](https://ieee-dataport.org/documents/fieldcropleaf-dataset-safflower-plant-leaf-images-disease-detection-and-classification) |
| 3 | Mixed pests | Dataset for Agriculture Pest Images | Aphids, leafhoppers, beetles, caterpillars; crops and field status not stated | 17.5 GB | [link](https://ieee-dataport.org/documents/dataset-agriculture-pest-images) |

**Not worth downloading:**
- **[Annotated Maize Leaf Disease](https://ieee-dataport.org/documents/annotated-maize-leaf-disease-image-dataset-cnn-based-classification):** derived from PlantVillage, no metadata.
- **[CoSEV cotton](https://ieee-dataport.org/documents/cosev-cotton-disease-dataset-detection-and-classification-severity-stages-and-multiple):** the page says the files have not been uploaded.
- **PlantVillage copies:** lab photos.
- **Ridge gourd:** 600 originals, augmented.
- **Rose:** 596 images, augmented.
- **Fruit-only sets:** mango, guava, apple fruitlet, grape frost.
- **IP102:** also free on GitHub.

**Possibly useful as text only:** [Context-Aware Multimodal Augmented PlantVillage](https://ieee-dataport.org/documents/context-aware-multimodal-augmented-plantvillage-dataset). It has more than 3,900 expert text descriptions for 38 PlantVillage classes; the images are lab photos.

### IEEE DataPort by modality (second search, 2026-10-27)

**Rice:** these add sources and modalities to Rice MMKG itself.

| Modality | Dataset | Content | Size | Link |
|---|---|---|---|---|
| Field image | Indian Rice Disease Dataset (IRDD) | Brown spot and healthy, West Bengal, expert-verified; "full dataset available soon" | 24 MB | [link](https://ieee-dataport.org/documents/indian-rice-disease-dataset-irdd) |
| UAV RGB + multispectral | IMPaCT-UAV-MsRGB | Paddy fields in Andhra Pradesh over the full growth cycle; RGB plus 4 bands (G, R, RE, NIR), about 1 cm/pixel | to check | [link](https://ieee-dataport.org/documents/indian-multi-stage-paddy-crop-tracking-based-uav-multispectral-and-rgb-image-dataset) |
| UAV multispectral (indices) | Multi-temporal UAV multispectral, paddy | DJI Mavic 3M, 7 dates, 3 plots, Kharif 2025, West Bengal; NDVI, NDRE, GNDVI per frame; no disease labels | 1.6 MB (CSV) | [link](https://ieee-dataport.org/documents/multi-temporal-uav-multispectral-dataset-solar-illumination-aware-vegetation-index) |
| Field image | Paddy Doctor | Already in Rice MMKG | | [link](https://ieee-dataport.org/documents/paddy-doctor-visual-image-dataset-automated-paddy-disease-classification-and-benchmarking) |

**IRDD adds a third independent brown-spot source** (with Paddy Doctor and Dhan-Shomadhan) for cross-source tests.

**Other crops and modalities:**

| Modality | Crop | Dataset | Content | Size | Link |
|---|---|---|---|---|---|
| UAV and ground image | Soybean | MH-SoyaHealthVision | Rust, mosaic, healthy, semilooper/caterpillar; Maharashtra; 2 seasons | 4.2 GB | [link](https://ieee-dataport.org/documents/mh-soyahealthvision-uav-dataset-disease-monitoring-and-severity-assessment) |
| Soil sensor (IoT) | none (field) | Rural IoT soil data | 7 LoRaWAN nodes near Gdańsk, 2023 season: soil moisture, temperature, pH, irradiance | small | [link](https://ieee-dataport.org/documents/rural-iot-soil-data) |
| Text | Cotton | Cotton diseases … treatment guidance | See the table above | | |

**Searched for but not found on DataPort:**
- **Light-trap or pheromone-trap pest time series.** The closest open set is outside DataPort: the [Kenyan maize lepidopteran pests and microclimate dataset 2021–2024](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12433461/) (IRD Dataverse). It pairs pheromone-trap counts with microclimate sensors at five sites, which makes it a strong match for a maize KG's sensor and pest layer.
- **Hyperspectral disease sets.** These appear in papers (wheat co-infection, tomato time series, soybean charcoal rot), but none was found as a DataPort download.

**Coverage of this search:**
- **What was used:** web search restricted to ieee-dataport.org, plus the public keyword pages "agriculture" (3 pages), "plant-disease-detection", "multispectral-imaging" and the paddy keyword page.
- **What it misses:**
  - DataPort's own search needs a login, so it may hold more.
  - Datasets of IEEE Access papers are often on GitHub or Mendeley instead of DataPort; IEEE Xplore was not searched.

**Cotton as a candidate crop:**
- **What DataPort gives:** an image set (COT-AD) and a text set with symptoms, conditions and controls, the two layers Rice MMKG has.
- **What is missing:** a second, independent cotton image source for cross-source tests.

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
