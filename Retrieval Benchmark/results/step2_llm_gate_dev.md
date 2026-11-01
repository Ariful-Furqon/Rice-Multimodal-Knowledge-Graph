LLM rerank gated on stage-1 confidence, top 3, dev_core main subset, thresholds cross-fitted.

| Protocol | n | Stage 1 R@1 | Gated R@1 | Stage 1 MRR | Gated MRR | p (MRR) | Threshold (folds) | Photos changed |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| in-source | 345 | 0.536 | 0.536 | 0.681 | 0.681 | 1.0000 | [0, 0] | 0 |
| cross-source | 195 | 0.354 | 0.354 | 0.509 | 0.509 | 1.0000 | [0, 0] | 0 |
