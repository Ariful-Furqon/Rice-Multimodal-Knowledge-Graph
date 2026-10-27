# Retrieval Benchmark

Data splits and query-time graph for the SIGIR 2027 retrieval experiments. Design: [`Ontology/riceMMKG_SIGIR_plan.md`](../Ontology/riceMMKG_SIGIR_plan.md), section 5, and [`design_v2.md`](design_v2.md).

## Image split, version 2 (2026-10-27)

[`splits/images_split.csv`](splits/images_split.csv) assigns each of the 21,149 `ImageObservation` individuals at the data freeze to train, dev or test.

| Split | Images |
|---|---:|
| train | 15,214 |
| dev | 2,967 |
| test | 2,968 |
| test_core ([`splits/test_core.csv`](splits/test_core.csv)) | 370 |

**Rules:**
- **Stratification:** by source dataset × `annotatedAs`, 70/15/15, seed 0. This is the same ratio and seed as `Multimodal Fusion PoC/ikrl_vs_cnn.py`.
- **Capture groups:** images from one capture session or burst stay in one split ([`splits/capture_groups.csv`](splits/capture_groups.csv), built by `scripts/capture_groups.py`, 4,659 groups):
  - **Paddy Doctor:** one group per (label, variety, age) from its `metadata.csv`, giving 170 sessions. 96% of nearest-neighbour image pairs share this key; random same-label pairs share it 19% of the time.
  - **Other datasets:** these have no capture metadata. Images with CLIP ViT-L/14 similarity ≥ 0.98 within one dataset and label are joined.
  - **Exact copies:** byte-identical files (same MD5) are joined. There are 144 MD5 groups.
- **Label conflicts:** one Paddy Doctor file is labelled both Downy Mildew (`downy_mildew/PDD06425.jpg`) and Rice Tungro Disease (`tungro/PDD12798.jpg`). It has no single gold answer, so both copies stay in train.
- **test_core:** a class-balanced sample of the test split, with at most 15 images per stratum, for the expensive methods (VLM triple generation).

**Why version 2:**
- **Version 1 (2026-10-26) leaked.** It grouped exact copies only, so burst photos of one plant sat in train and test.
- **Measured leak:** 32% of test images had a train image at CLIP similarity ≥ 0.99, and image kNN reached R@1 0.917.
- **Version 2:** that share is 2.9%, and kNN R@1 is 0.439.
- **Backup:** version 1 is kept outside the repository and is not used.

**Not covered:**
- **Dataset shortcut:** Netrokona (potassium only) and YUKE-WBC (brown planthopper only) each carry one label. A model can recognise the dataset's camera and background instead of the condition, so their in-dataset scores are not evidence of diagnosis.
- **Dhan-Shomadhan backgrounds:** it mixes white-background and field photos. The split is not stratified by background.
- **Multispectral images:** the 472 multispectral captures (`RemoteSensingObservation`) are not in this split.

## Gold answers

[`splits/gold.csv`](splits/gold.csv) (`scripts/make_gold.py`) gives each image its gold target: the cause to manage, not the symptom. There are 17 targets, and all stem borer damage photos are gold `Stem_Borer`. Deadheart and white-head labels are kept as symptoms. The rule and its reasons are in [`design_v2.md`](design_v2.md), section 5.

## Query-time graph

`Data/retrieval/RiceMMKG_query_time.ttl` is gitignored and rebuilt by the script.
- **What it removes:** every triple whose subject or object is a dev or test image. That is 49,557 triples, leaving 275,144.
- **What it keeps:** all 384 provenance axioms.
- **Leakage rule:** dev and test images are queries, not graph content. This is the leakage rule of the plan.

## Stage-1 baselines

`scripts/stage1_baselines.py` gives the results in [`results/stage1_results.md`](results/stage1_results.md); see [`design_v2.md`](design_v2.md), section 4.

## Rebuild

`make_split.py` needs `rdflib` only. The other two scripts need the GPU environment (`D:\venvs\ricemmkg-retrieval`: torch with CUDA 12.8, transformers, scikit-learn).

```bash
python -I "Retrieval Benchmark/scripts/make_split.py" . Data/retrieval        # first run: v1 groups, also writes the MD5 cache
<venv>/python -I "Retrieval Benchmark/scripts/stage1_baselines.py" . "Retrieval Benchmark/results"   # caches CLIP features
<venv>/python -I "Retrieval Benchmark/scripts/capture_groups.py" .
python -I "Retrieval Benchmark/scripts/make_split.py" . Data/retrieval        # v2, using capture_groups.csv
python -I "Retrieval Benchmark/scripts/make_gold.py" .
<venv>/python -I "Retrieval Benchmark/scripts/stage1_baselines.py" . "Retrieval Benchmark/results"
```

The first run hashes every image. Files that OneDrive keeps online only are downloaded first. The hashes are cached in `Data/retrieval/md5_cache.csv` and the CLIP features in `Data/retrieval/feats_clip-l14.npz`.
