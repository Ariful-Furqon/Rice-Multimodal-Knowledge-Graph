| System | test R@1 | test_core R@1 | DhanShomadhanDataset R@1 | NetrokonaRiceDataset R@1 | NutrientDeficiencyKaggleDataset R@1 | PaddyDoctorDataset R@1 | StemBorerSymptomDataset R@1 | YukeWbcDataset R@1 | test MRR | test nDCG@5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| clip_label | 0.107 | 0.089 | 0.060 | 0.000 | 0.000 | 0.135 | 0.003 | 0.600 | 0.249 | 0.225 |
| clip_kg | 0.036 | 0.062 | 0.169 | 0.000 | 0.000 | 0.032 | 0.006 | 0.500 | 0.206 | 0.196 |
| knn_image | 0.488 | 0.568 | 0.663 | 1.000 | 0.855 | 0.361 | 0.956 | 1.000 | 0.647 | 0.685 |
| linear_probe | 0.519 | 0.535 | 0.512 | 1.000 | 0.838 | 0.420 | 0.930 | 0.600 | 0.673 | 0.716 |

Cross-dataset: Paddy Doctor train -> Dhan-Shomadhan (Brown_Spot, Rice_Blast_Disease, Rice_Tungro_Disease), n = 606, candidates = all 17 targets

| System | R@1 | R@3 | MRR | nDCG@5 |
|---|---:|---:|---:|---:|
| clip_label | 0.094 | 0.201 | 0.221 | 0.197 |
| clip_kg | 0.157 | 0.474 | 0.402 | 0.500 |
| knn_image | 0.479 | 0.832 | 0.665 | 0.724 |
| linear_probe | 0.436 | 0.790 | 0.635 | 0.696 |
