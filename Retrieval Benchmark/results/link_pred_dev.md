Link prediction with the photo's own edges, dev main subset (no single-source dataset). CLIP ViT-L/14 features + binary edge features from `Ontology/Rice MMKG.rdf`; head C of `ikrl_v2_dev.py`; 5 seeds (mean ± sd). Script: `scripts/dev_checks/link_pred_dev.py`.

**Edge coverage by dataset** (share of photos with at least one edge of the block):

| Block | DhanShomadhanDataset | NetrokonaRiceDataset | NutrientDeficiencyKaggleDataset | PaddyDoctorDataset | StemBorerSymptomDataset | YukeWbcDataset |
|---|---:|---:|---:|---:|---:|---:|
| safe | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.67 |
| context | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| dataset | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| leak | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

| Protocol | Variant | n | R@1 | macro R@1 | MRR | Δ MRR vs 1 | seeds > 0 |
|---|---|---:|---:|---:|---:|---:|---:|
| in-source | 1 pixels | 2882 | 0.612 ± 0.003 | 0.591 ± 0.005 | 0.729 ± 0.002 |  |  |
| in-source | 2 safe | 2882 | 0.608 ± 0.009 | 0.585 ± 0.014 | 0.726 ± 0.005 | -0.0030 | 1/5 |
| in-source | 3 + age, variety | 2882 | 0.582 ± 0.005 | 0.540 ± 0.013 | 0.711 ± 0.004 | -0.0181 | 0/5 |
| in-source | 4 + dataset | 2882 | 0.608 ± 0.007 | 0.586 ± 0.011 | 0.727 ± 0.004 | -0.0022 | 1/5 |
| in-source | 5 + leaking edges | 2882 | 0.798 ± 0.002 | 0.779 ± 0.001 | 0.870 ± 0.001 | +0.1413 | 5/5 |
| cross-source | 1 pixels | 1890 | 0.421 ± 0.009 | 0.408 ± 0.020 | 0.570 ± 0.012 |  |  |
| cross-source | 2 safe | 1890 | 0.427 ± 0.018 | 0.403 ± 0.020 | 0.576 ± 0.015 | +0.0052 | 2/5 |
| cross-source | 3 + age, variety | 1890 | 0.424 ± 0.006 | 0.409 ± 0.012 | 0.576 ± 0.003 | +0.0058 | 3/5 |
| cross-source | 4 + dataset | 1890 | 0.428 ± 0.012 | 0.406 ± 0.013 | 0.579 ± 0.006 | +0.0087 | 4/5 |
| cross-source | 5 + leaking edges | 1890 | 0.422 ± 0.008 | 0.397 ± 0.018 | 0.576 ± 0.006 | +0.0057 | 3/5 |

**R@1 per dataset** (mean over seeds):

| Protocol | Dataset | n | 1 pixels | 2 safe | 3 + age, variety | 4 + dataset | 5 + leaking edges |
|---|---|---:|---:|---:|---:|---:|---:|
| in-source | DhanShomadhanDataset | 166 | 0.690 | 0.684 | 0.606 | 0.693 | 0.849 |
| in-source | NutrientDeficiencyKaggleDataset | 173 | 0.926 | 0.919 | 0.861 | 0.924 | 0.982 |
| in-source | PaddyDoctorDataset | 2228 | 0.530 | 0.526 | 0.508 | 0.525 | 0.752 |
| in-source | StemBorerSymptomDataset | 315 | 0.984 | 0.977 | 0.937 | 0.978 | 0.994 |
| cross-source | DhanShomadhanDataset | 91 | 0.073 | 0.075 | 0.066 | 0.073 | 0.077 |
| cross-source | NutrientDeficiencyKaggleDataset | 57 | 0.800 | 0.737 | 0.793 | 0.758 | 0.726 |
| cross-source | PaddyDoctorDataset | 1427 | 0.457 | 0.467 | 0.463 | 0.466 | 0.462 |
| cross-source | StemBorerSymptomDataset | 315 | 0.294 | 0.294 | 0.284 | 0.296 | 0.286 |
