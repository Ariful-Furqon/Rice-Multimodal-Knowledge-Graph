Link prediction with the photo's own edges, dev main subset (no single-source dataset). CLIP ViT-L/14 features + binary edge features from `Ontology/Rice MMKG.rdf`; head C of `ikrl_v2_dev.py`; 5 seeds (mean ± sd). Plant age enters as its growth-stage band. Variant 3b is variant 3 trained, without early stopping, for the epochs at which variant 1 stopped. Script: `scripts/dev_checks/link_pred_dev.py`.

**Edge coverage on the dev main subset** (share of photos with at least one edge of the block):

| Block | DhanShomadhanDataset | NutrientDeficiencyKaggleDataset | PaddyDoctorDataset | StemBorerSymptomDataset |
|---|---:|---:|---:|---:|
| safe | 1.00 | 1.00 | 0.00 | 0.00 |
| context | 0.00 | 0.00 | 1.00 | 0.00 |
| dataset | 1.00 | 1.00 | 1.00 | 1.00 |
| leak | 1.00 | 1.00 | 1.00 | 1.00 |

**Lookup baseline, no model:** folder name in `contentUrl` → majority train gold (an unseen folder is a miss).

| Protocol | n | R@1 | folder seen in train |
|---|---:|---:|---:|
| in-source | 2882 | 1.000 | 1.000 |
| cross-source | 1890 | 0.000 | 0.000 |

| Protocol | Variant | n | R@1 | macro R@1 | MRR | Δ MRR vs 1 | seeds > 0 | stop epoch |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| in-source | 1 pixels | 2882 | 0.612 ± 0.005 | 0.592 ± 0.007 | 0.729 ± 0.002 |  |  | 341 |
| in-source | 2 safe | 2882 | 0.609 ± 0.010 | 0.587 ± 0.014 | 0.727 ± 0.005 | -0.0023 | 2/5 | 303 |
| in-source | 3 + age, variety | 2882 | 0.594 ± 0.015 | 0.561 ± 0.024 | 0.718 ± 0.008 | -0.0113 | 0/5 | 131 |
| in-source | 3b = 3, epochs of 1 | 2882 | 0.613 ± 0.003 | 0.591 ± 0.004 | 0.728 ± 0.002 | -0.0012 | 2/5 | 341 |
| in-source | 4 + dataset | 2882 | 0.608 ± 0.008 | 0.586 ± 0.011 | 0.727 ± 0.004 | -0.0020 | 1/5 | 286 |
| in-source | 5 + leaking edges | 2882 | 0.798 ± 0.002 | 0.778 ± 0.002 | 0.870 ± 0.001 | +0.1412 | 5/5 | 399 |
| cross-source | 1 pixels | 1890 | 0.421 ± 0.013 | 0.408 ± 0.025 | 0.572 ± 0.014 |  |  | 281 |
| cross-source | 2 safe | 1890 | 0.427 ± 0.017 | 0.404 ± 0.017 | 0.576 ± 0.014 | +0.0046 | 2/5 | 286 |
| cross-source | 3 + age, variety | 1890 | 0.417 ± 0.006 | 0.393 ± 0.013 | 0.572 ± 0.007 | +0.0009 | 3/5 | 167 |
| cross-source | 3b = 3, epochs of 1 | 1890 | 0.411 ± 0.009 | 0.378 ± 0.012 | 0.566 ± 0.011 | -0.0054 | 2/5 | 281 |
| cross-source | 4 + dataset | | n/a | | | | | |
| cross-source | 5 + leaking edges | 1890 | 0.422 ± 0.008 | 0.398 ± 0.018 | 0.576 ± 0.006 | +0.0047 | 3/5 | 367 |

Stop epoch: mean epoch of the kept model (of 400), over seeds and, cross-source, the held-out folds.

**R@1 per dataset** (mean over seeds):

| Protocol | Dataset | n | 1 pixels | 2 safe | 3 + age, variety | 3b = 3, epochs of 1 | 4 + dataset | 5 + leaking edges |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| in-source | DhanShomadhanDataset | 166 | 0.692 | 0.692 | 0.643 | 0.707 | 0.694 | 0.847 |
| in-source | NutrientDeficiencyKaggleDataset | 173 | 0.927 | 0.920 | 0.882 | 0.929 | 0.925 | 0.982 |
| in-source | PaddyDoctorDataset | 2228 | 0.530 | 0.526 | 0.517 | 0.528 | 0.524 | 0.752 |
| in-source | StemBorerSymptomDataset | 315 | 0.983 | 0.977 | 0.952 | 0.985 | 0.978 | 0.994 |
| cross-source | DhanShomadhanDataset | 91 | 0.073 | 0.075 | 0.073 | 0.075 | n/a | 0.077 |
| cross-source | NutrientDeficiencyKaggleDataset | 57 | 0.786 | 0.733 | 0.740 | 0.681 | n/a | 0.730 |
| cross-source | PaddyDoctorDataset | 1427 | 0.456 | 0.467 | 0.452 | 0.448 | n/a | 0.462 |
| cross-source | StemBorerSymptomDataset | 315 | 0.295 | 0.294 | 0.298 | 0.293 | n/a | 0.286 |
