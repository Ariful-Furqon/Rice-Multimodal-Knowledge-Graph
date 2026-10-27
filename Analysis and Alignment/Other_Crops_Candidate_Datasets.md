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

| Crop | Dataset | Content | Link |
|---|---|---|---|
| Tomato | Real Field Crop Image Dataset (Karande & Garg) | Field images from 3 sites in Sangli and Satara, Maharashtra; leaf masks; 151 MB | [10.21227/5ytp-dr85](https://ieee-dataport.org/documents/real-field-crop-image-dataset) |
| Brinjal, castor, cumin, guava, papaya | Multi-Crop Leaf Disease Dataset | 1,720 field images, 41 classes | [link](https://ieee-dataport.org/documents/multi-crop-leaf-disease-dataset) |

**Not worth downloading:** [Annotated Maize Leaf Disease Image Dataset](https://ieee-dataport.org/documents/annotated-maize-leaf-disease-image-dataset-cnn-based-classification). It is derived from PlantVillage-related sources and has no capture metadata.

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
