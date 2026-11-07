Source removal from CLIP ViT-L/14 features before the stage-1 image systems, dev main subset (no single-source dataset). Transforms: `project` removes the source subspace learned on the training images (3 rounds of nullspace projection); `center` subtracts each source's mean feature, for a held-out source the mean of its own unlabelled dev images (transductive); `both` is center then project; `project_cc` is project with the source classifier fitted on features minus their class mean (within-class source directions only). Δ MRR against `none`, 95% bootstrap interval over capture groups. Script: `scripts/dev_checks/debias_dev.py`.

**Source predictable from the features** (linear probe, train images of the training sources, half to fit and half to test; mean over folds):

| Protocol | none | project | center | both | project_cc |
|---|---:|---:|---:|---:|---:|
| in-source | 0.988 | 0.775 | 0.775 | 0.775 | 0.820 |
| cross-source | 0.989 | 0.737 | 0.734 | 0.733 | 0.872 |

| Protocol | System | Transform | n | R@1 | macro R@1 | R@3 | MRR | Δ MRR [95% CI] |
|---|---|---|---:|---:|---:|---:|---:|---|
| in-source | knn_image | none | 2882 | 0.505 | 0.484 | 0.749 | 0.658 |  |
| in-source | knn_image | project | 2882 | 0.495 | 0.471 | 0.730 | 0.645 | -0.0128 [-0.0266, -0.0017] |
| in-source | knn_image | center | 2882 | 0.506 | 0.472 | 0.744 | 0.655 | -0.0028 [-0.0169, +0.0098] |
| in-source | knn_image | both | 2882 | 0.500 | 0.478 | 0.734 | 0.651 | -0.0075 [-0.0217, +0.0077] |
| in-source | knn_image | project_cc | 2882 | 0.478 | 0.462 | 0.727 | 0.636 | -0.0218 [-0.0399, -0.0091] |
| in-source | linear_probe | none | 2882 | 0.566 | 0.449 | 0.807 | 0.707 |  |
| in-source | linear_probe | project | 2882 | 0.508 | 0.330 | 0.751 | 0.656 | -0.0502 [-0.0756, -0.0324] |
| in-source | linear_probe | center | 2882 | 0.578 | 0.481 | 0.770 | 0.700 | -0.0068 [-0.0416, +0.0227] |
| in-source | linear_probe | both | 2882 | 0.579 | 0.490 | 0.778 | 0.702 | -0.0048 [-0.0432, +0.0274] |
| in-source | linear_probe | project_cc | 2882 | 0.543 | 0.399 | 0.800 | 0.693 | -0.0138 [-0.0397, +0.0086] |
| cross-source | knn_image | none | 1890 | 0.378 | 0.355 | 0.631 | 0.552 |  |
| cross-source | knn_image | project | 1890 | 0.365 | 0.303 | 0.505 | 0.498 | -0.0542 [-0.0897, -0.0257] |
| cross-source | knn_image | center | 1890 | 0.313 | 0.220 | 0.495 | 0.471 | -0.0816 [-0.1199, -0.0476] |
| cross-source | knn_image | both | 1890 | 0.317 | 0.243 | 0.492 | 0.472 | -0.0798 [-0.1204, -0.0474] |
| cross-source | knn_image | project_cc | 1890 | 0.368 | 0.317 | 0.574 | 0.525 | -0.0273 [-0.0597, -0.0041] |
| cross-source | linear_probe | none | 1890 | 0.394 | 0.356 | 0.625 | 0.546 |  |
| cross-source | linear_probe | project | 1890 | 0.389 | 0.251 | 0.445 | 0.499 | -0.0469 [-0.0921, +0.0091] |
| cross-source | linear_probe | center | 1890 | 0.346 | 0.229 | 0.475 | 0.482 | -0.0636 [-0.0936, -0.0465] |
| cross-source | linear_probe | both | 1890 | 0.340 | 0.223 | 0.474 | 0.473 | -0.0730 [-0.1095, -0.0515] |
| cross-source | linear_probe | project_cc | 1890 | 0.378 | 0.315 | 0.534 | 0.521 | -0.0247 [-0.0490, +0.0057] |

**R@1 per dataset:**

| Protocol | System | Dataset | n | none | project | center | both | project_cc |
|---|---|---|---:|---:|---:|---:|---:|---:|
| in-source | knn_image | DhanShomadhanDataset | 166 | 0.681 | 0.645 | 0.687 | 0.675 | 0.651 |
| in-source | knn_image | NutrientDeficiencyKaggleDataset | 173 | 0.879 | 0.855 | 0.850 | 0.879 | 0.884 |
| in-source | knn_image | PaddyDoctorDataset | 2228 | 0.399 | 0.399 | 0.404 | 0.395 | 0.376 |
| in-source | knn_image | StemBorerSymptomDataset | 315 | 0.952 | 0.898 | 0.937 | 0.943 | 0.889 |
| in-source | linear_probe | DhanShomadhanDataset | 166 | 0.500 | 0.392 | 0.476 | 0.470 | 0.458 |
| in-source | linear_probe | NutrientDeficiencyKaggleDataset | 173 | 0.786 | 0.370 | 0.734 | 0.746 | 0.746 |
| in-source | linear_probe | PaddyDoctorDataset | 2228 | 0.503 | 0.496 | 0.531 | 0.531 | 0.481 |
| in-source | linear_probe | StemBorerSymptomDataset | 315 | 0.924 | 0.733 | 0.886 | 0.892 | 0.911 |
| cross-source | knn_image | DhanShomadhanDataset | 91 | 0.110 | 0.077 | 0.121 | 0.077 | 0.110 |
| cross-source | knn_image | NutrientDeficiencyKaggleDataset | 57 | 0.737 | 0.456 | 0.105 | 0.246 | 0.509 |
| cross-source | knn_image | PaddyDoctorDataset | 1427 | 0.409 | 0.402 | 0.347 | 0.353 | 0.399 |
| cross-source | knn_image | StemBorerSymptomDataset | 315 | 0.254 | 0.263 | 0.254 | 0.235 | 0.276 |
| cross-source | linear_probe | DhanShomadhanDataset | 91 | 0.099 | 0.242 | 0.176 | 0.198 | 0.110 |
| cross-source | linear_probe | NutrientDeficiencyKaggleDataset | 57 | 0.684 | 0.000 | 0.018 | 0.000 | 0.474 |
| cross-source | linear_probe | PaddyDoctorDataset | 1427 | 0.406 | 0.420 | 0.386 | 0.376 | 0.392 |
| cross-source | linear_probe | StemBorerSymptomDataset | 315 | 0.371 | 0.365 | 0.273 | 0.279 | 0.371 |
