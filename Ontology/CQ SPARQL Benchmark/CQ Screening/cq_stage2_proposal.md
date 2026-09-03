# Stage 2 - Cross-model Deduplication (proposal)

Generated 2026-09-03 20:36 by `stage2_cluster.py` from `cq_pool_stage0.csv`.

**In:** 173 CQs &nbsp;&nbsp; **Out:** 148 canonical CQs (provisional) &nbsp;&nbsp; **Merge rule:** cosine >= 0.4 AND Jaccard >= 0.4, average linkage, within category.

> **Read this before using the numbers.** Automatic clustering is triage, not measurement. These CQs share domain vocabulary heavily, so both signals conflate genuinely distinct requirements -- at every cut tried, *what pathogen causes blast* and *what symptoms are reported for blast* land in one cluster. Thresholds therefore favour precision, which leaves paraphrases unmerged. **`n_models` below is a lower bound on convergence, not a measurement of it**, and the manual pass over `cq_stage2_borderline.csv` is required rather than optional.

Clusters are proposals. `merge_ok` in `cq_stage2_clusters.csv` and `confirmed` in `cq_stage2_canonical.csv` are blank.

## Convergence: how many models proposed each canonical CQ

| Models agreeing | Canonical CQs |
|---|---|
| 2 | 7 |
| 1 | 141 |

A CQ proposed independently by several models is evidence that it is a natural requirement of the domain rather than one model's invention. Stage 5 must nevertheless keep some n_models = 1 CQs in the questionnaire, or the hypothesis that convergence predicts expert-rated relevance cannot be tested.

## Canonical CQs proposed by two or more models

**C002** &middot; crossmodal &middot; **2 models** (2 CQs: P018 P056)

> For a condition diagnosed from an image at a given plot, which varieties recorded as planted in the same district carry resistance genes against the causal pathogen, and which are susceptible?

**C071** &middot; genomic &middot; **2 models** (3 CQs: P077 P144 P079)

> Which resistance genes are associated with a given rice variety or cultivar?

**C106** &middot; sensor &middot; **2 models** (2 CQs: P001 P037)

> What were the daily mean temperature, relative humidity, and rainfall recorded at a given sensor station over a given date range?

**C125** &middot; text &middot; **2 models** (2 CQs: P031 P067)

> What is the causal agent of a given rice disease (e.g., bacterial leaf blight), and to which taxonomic group (fungus, bacterium, virus) does it belong?

**C126** &middot; text &middot; **2 models** (2 CQs: P032 P170)

> Which insect species act as vectors for rice tungro disease, and which viruses (RTBV, RTSV) do they transmit?

**C130** &middot; text &middot; **2 models** (2 CQs: P036 P072)

> Which conditions have been reported in a given Indonesian province (e.g., East Java) in surveillance bulletins within a given year, ranked by reported affected area?

**C135** &middot; text &middot; **2 models** (3 CQs: P103 P169 P104)

> What is the causal pathogen of Rice Blast?

## Borderline pairs for manual review

304 same-category pairs were left unmerged although one signal flagged them (cosine >= 0.28 or Jaccard >= 0.3). Each row in `cq_stage2_borderline.csv` carries both scores and a blank `should_merge` column. This list is where the convergence count actually gets settled.
