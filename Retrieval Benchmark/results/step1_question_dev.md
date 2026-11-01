Step 1 with a SIMULATED farmer observation, dev_core main subset (sensitivity analysis, not a result).

| Protocol | Noise | n | Stage 1 R@1 | + words R@1 | Stage 1 MRR | + words MRR | p (MRR) | Blast / brown spot R@1 | lambda (folds) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| in-source | 0.0 | 345 | 0.536 | 0.652 | 0.681 | 0.758 | 0.0001 | 0.217 → 0.267 | [0.5, 0.5] |
| in-source | 0.3 | 345 | 0.536 | 0.591 | 0.681 | 0.718 | 0.0003 | 0.217 → 0.217 | [0.25, 0.25] |
| in-source | 0.5 | 345 | 0.536 | 0.565 | 0.681 | 0.700 | 0.0632 | 0.217 → 0.200 | [0.25, 0.25] |
| cross-source | 0.0 | 195 | 0.354 | 0.405 | 0.509 | 0.552 | 0.0020 | 0.000 → 0.033 | [2, 0.25] |
| cross-source | 0.3 | 195 | 0.354 | 0.374 | 0.509 | 0.526 | 0.2871 | 0.000 → 0.033 | [2, 0.25] |
| cross-source | 0.5 | 195 | 0.354 | 0.390 | 0.509 | 0.535 | 0.0714 | 0.000 → 0.033 | [1, 0.25] |
