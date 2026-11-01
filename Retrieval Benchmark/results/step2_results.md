Step 2 on test_core, main subset. 740 VLM runs (test_core + dev_core): parsed 1.000, triples in vocabulary 0.856, no triples 0.168.

| Protocol | System | n | R@1 | macro R@1 | R@3 | MRR | p (MRR) |
|---|---|---:|---:|---:|---:|---:|---:|
| in-source | stage 1 | 345 | 0.513 | 0.435 | 0.783 | 0.667 |  |
| in-source | stage 1 + KG triples | 345 | 0.528 | 0.453 | 0.788 | 0.677 | 0.164 |
| in-source | KGMEL baseline | 345 | 0.258 | 0.212 | 0.768 | 0.531 | 0.000 |
| cross-source | stage 1 | 195 | 0.354 | 0.331 | 0.579 | 0.512 |  |
| cross-source | stage 1 + KG triples | 195 | 0.354 | 0.331 | 0.579 | 0.512 | 1.000 |
| cross-source | KGMEL baseline | 195 | 0.246 | 0.244 | 0.585 | 0.471 | 0.088 |

Lambda tuned on dev_core: in-source 0.2, cross-source 0

Confusable pairs (R@1, photos of the two conditions only):

| Protocol | Pair | n | Stage 1 | Stage 1 + KG triples | KGMEL baseline |
|---|---|---:|---:|---:|---:|
| in-source | blast / brown spot | 60 | 0.250 | 0.283 | 0.367 |
| in-source | BLB / BLS | 30 | 0.000 | 0.000 | 0.067 |
| cross-source | blast / brown spot | 60 | 0.017 | 0.017 | 0.183 |

Per dataset (R@1):

| Protocol | Dataset | n | Stage 1 | Stage 1 + KG triples | KGMEL baseline |
|---|---|---:|---:|---:|---:|
| in-source | DhanShomadhanDataset | 75 | 0.440 | 0.453 | 0.267 |
| in-source | NutrientDeficiencyKaggleDataset | 45 | 0.889 | 0.889 | 0.311 |
| in-source | PaddyDoctorDataset | 180 | 0.344 | 0.372 | 0.211 |
| in-source | StemBorerSymptomDataset | 45 | 0.933 | 0.911 | 0.378 |
| cross-source | DhanShomadhanDataset | 45 | 0.089 | 0.089 | 0.178 |
| cross-source | NutrientDeficiencyKaggleDataset | 15 | 0.667 | 0.667 | 0.067 |
| cross-source | PaddyDoctorDataset | 90 | 0.411 | 0.411 | 0.278 |
| cross-source | StemBorerSymptomDataset | 45 | 0.400 | 0.400 | 0.311 |
