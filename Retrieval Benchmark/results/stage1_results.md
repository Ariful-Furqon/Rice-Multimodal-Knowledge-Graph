| System | test R@1 | test_core R@1 | DhanShomadhanDataset R@1 | NetrokonaRiceDataset R@1 | NutrientDeficiencyKaggleDataset R@1 | PaddyDoctorDataset R@1 | StemBorerSymptomDataset R@1 | YukeWbcDataset R@1 | test MRR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| clip_label | 0.098 | 0.116 | 0.060 | 0.000 | 0.000 | 0.087 | 0.257 | 0.600 | 0.235 |
| clip_kg | 0.048 | 0.078 | 0.169 | 0.000 | 0.000 | 0.033 | 0.117 | 0.500 | 0.211 |
| knn_image | 0.439 | 0.524 | 0.663 | 1.000 | 0.855 | 0.297 | 0.949 | 1.000 | 0.614 |
| linear_probe | 0.483 | 0.500 | 0.512 | 1.000 | 0.832 | 0.373 | 0.933 | 0.600 | 0.653 |

Cross-dataset: Paddy Doctor train -> Dhan-Shomadhan (Brown_Spot, Rice_Blast_Disease, Rice_Tungro_Disease), n = 606, candidates = all 19 conditions

| System | R@1 | R@3 | MRR |
|---|---:|---:|---:|
| clip_label | 0.094 | 0.201 | 0.219 |
| clip_kg | 0.157 | 0.474 | 0.401 |
| knn_image | 0.483 | 0.832 | 0.668 |
| linear_probe | 0.436 | 0.782 | 0.633 |
