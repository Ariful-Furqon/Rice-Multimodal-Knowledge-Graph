IKRL re-run on split v2, dev main subset (no single-source dataset), CLIP ViT-L/14 features, 5 seeds (mean ± sd). Early stopping on 10% of the train capture groups. Domain subgraph: 345 triples. Script: `scripts/dev_checks/ikrl_v2_dev.py`.

| Protocol | Head | n | R@1 | macro R@1 | MRR | gate λ |
|---|---|---:|---:|---:|---:|---:|
| in-source | A linear (stage-1 probe) | 2882 | 0.605 ± 0.003 | 0.587 ± 0.004 | 0.724 ± 0.002 |  |
| in-source | B IKRL, TransE class vectors | 2882 | 0.612 ± 0.004 | 0.592 ± 0.008 | 0.730 ± 0.002 | 0.85 |
| in-source | C same head, random class vectors | 2882 | 0.612 ± 0.003 | 0.591 ± 0.005 | 0.729 ± 0.002 | 0.88 |
| cross-source | A linear (stage-1 probe) | 1890 | 0.419 ± 0.004 | 0.408 ± 0.014 | 0.576 ± 0.005 |  |
| cross-source | B IKRL, TransE class vectors | 1890 | 0.418 ± 0.010 | 0.402 ± 0.021 | 0.571 ± 0.012 | 0.82 |
| cross-source | C same head, random class vectors | 1890 | 0.421 ± 0.009 | 0.408 ± 0.020 | 0.570 ± 0.012 | 0.83 |

KG effect = B − C (same parameters, only the class vectors differ); capacity effect = C − A. Per seed, paired MRR difference, and the share of seeds where it is positive:

| Protocol | B − C MRR | seeds > 0 | C − A MRR | seeds > 0 |
|---|---:|---:|---:|---:|
| in-source | +0.0005 ± 0.0008 | 4/5 | +0.0049 ± 0.0008 | 5/5 |
| cross-source | +0.0004 ± 0.0166 | 2/5 | -0.0055 ± 0.0102 | 1/5 |
