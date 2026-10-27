In-source: test split, 17 candidate targets. main = test without the single-source datasets (NetrokonaRiceDataset, YukeWbcDataset).

| System | main R@1 | main macro R@1 | main MRR | test_core R@1 | all test R@1 |
|---|---:|---:|---:|---:|---:|
| clip_label | 0.108 | 0.085 | 0.251 | 0.078 | 0.107 |
| clip_kg | 0.035 | 0.043 | 0.208 | 0.052 | 0.036 |
| knn_image | 0.473 | 0.466 | 0.636 | 0.536 | 0.488 |
| linear_probe | 0.506 | 0.424 | 0.665 | 0.513 | 0.519 |

Per dataset (test split, R@1):

| System | DhanShomadhanDataset | NetrokonaRiceDataset | NutrientDeficiencyKaggleDataset | PaddyDoctorDataset | StemBorerSymptomDataset | YukeWbcDataset |
|---|---:|---:|---:|---:|---:|---:|
| clip_label | 0.060 | 0.000 | 0.000 | 0.135 | 0.003 | 0.600 |
| clip_kg | 0.169 | 0.000 | 0.000 | 0.032 | 0.006 | 0.500 |
| knn_image | 0.663 | 1.000 | 0.855 | 0.361 | 0.956 | 1.000 |
| linear_probe | 0.512 | 1.000 | 0.838 | 0.420 | 0.930 | 0.600 |

Cross-source, leave one dataset out (pooled n = 14093):

| System | R@1 | macro R@1 | R@3 | MRR |
|---|---:|---:|---:|---:|
| clip_label | 0.168 | 0.182 | 0.331 | 0.311 |
| clip_kg | 0.056 | 0.065 | 0.252 | 0.232 |
| knn_image | 0.366 | 0.287 | 0.593 | 0.534 |
| linear_probe | 0.400 | 0.306 | 0.609 | 0.546 |

Per held-out dataset (R@1; targets tested):

| Held out | n | targets | clip_label | clip_kg | knn_image | linear_probe |
|---|---:|---|---:|---:|---:|---:|
| DhanShomadhanDataset | 606 | Brown_Spot, Rice_Blast_Disease, Rice_Tungro_Disease | 0.094 | 0.157 | 0.089 | 0.116 |
| NetrokonaRiceDataset | 500 | Potassium_Deficiency_Disorder | 0.000 | 0.000 | 0.000 | 0.002 |
| NutrientDeficiencyKaggleDataset | 383 | Potassium_Deficiency_Disorder | 0.000 | 0.000 | 0.632 | 0.671 |
| PaddyDoctorDataset | 10508 | Brown_Spot, Normal_Health, Rice_Blast_Disease, Rice_Tungro_Disease, Stem_Borer | 0.219 | 0.065 | 0.411 | 0.432 |
| StemBorerSymptomDataset | 2096 | Normal_Health, Stem_Borer | 0.005 | 0.007 | 0.264 | 0.372 |

Source dataset predicted from the image (linear probe): 0.993
