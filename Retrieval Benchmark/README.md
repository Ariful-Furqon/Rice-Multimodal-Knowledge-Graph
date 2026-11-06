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
- **Stratification:** by source dataset × `annotatedAs`, 70/15/15, seed 0. This is the same ratio and seed as the August 2026 IKRL prototype, which is kept locally and is not in this repository.
- **Capture groups:** images from one capture session or burst stay in one split ([`splits/capture_groups.csv`](splits/capture_groups.csv), built by `scripts/capture_groups.py`, 4,659 groups):
  - **Paddy Doctor:** one group per (label, variety, age) from its `metadata.csv`, giving 170 sessions. 96% of nearest-neighbour image pairs share this key; random same-label pairs share it 19% of the time.
  - **Other datasets:** these have no capture metadata. Images with CLIP ViT-L/14 similarity ≥ 0.98 within one dataset and label are joined.
    - **The threshold is not critical** ([`results/split_threshold_sensitivity.md`](results/split_threshold_sensitivity.md), 5 split seeds each):
      - **0.97 to 0.99, or no similarity grouping:** leak and kNN R@1 are equal within seed noise; kNN is 0.455 ± 0.025 at 0.98.
      - **Below 0.98, groups chain:** the largest group has 498 photos at 0.97, 661 at 0.96 and 703 at 0.95, against 81 at 0.98.
      - **Outside Paddy Doctor, the leak is about 0** at every threshold. The 2 to 4% that remains is inside Paddy Doctor and depends on the seed.
    - **The range matches CLIP deduplication practice:**
      - SemDeDup (Abbas et al., 2023): cosine ≥ 1 − ε, ε = 0.03 to 0.001.
      - DataComp (Gadre et al., 2023): CLIP at 0.96 gives precision 0.9.
  - **Exact copies:** byte-identical files (same MD5) are joined. There are 144 MD5 groups.
- **Label conflicts:** one Paddy Doctor file is labelled both Downy Mildew (`downy_mildew/PDD06425.jpg`) and Rice Tungro Disease (`tungro/PDD12798.jpg`). It has no single gold answer, so both copies stay in train.
- **test_core:** a class-balanced sample of the test split, with at most 15 images per stratum, for the expensive methods (VLM triple generation).

**Why version 2:**
- **Version 1 (2026-10-26) leaked.** It grouped exact copies only, so burst photos of one plant sat in train and test.
- **Measured leak:** 32% of test images had a train image at CLIP similarity ≥ 0.99, and image kNN reached R@1 0.917.
- **Version 2:** that share is 2.9%, and kNN R@1 is 0.439.
- **Backup:** version 1 is kept outside the repository and is not used.

**Not covered:**
- **Dataset shortcut:** the source dataset is predictable from the image (0.993). Netrokona (potassium only) and YUKE-WBC (brown planthopper only) each carry one label, so their test queries are left out of the headline "main" subset, and cross-source results come from leave-one-dataset-out (`stage1_baselines.py`).
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

## Stage 2 and coverage

`scripts/stage2_passages.py` gives the coverage table and the passage-retrieval scores, with and without the KG, in [`results/stage2_results.md`](results/stage2_results.md); see [`design_v2.md`](design_v2.md), sections 6 and 7. It needs Ollama with `bge-m3` and the reranker `BAAI/bge-reranker-v2-m3` (Hugging Face, about 2.3 GB, set `HF_HOME`).

## Step 2

`scripts/step2_vlm_triples.py` writes the VLM triples (`results/vlm_triples_closed.jsonl`, `results/vlm_triples_open.jsonl`) and `splits/dev_core.csv`. `scripts/step2_rerank.py` gives [`results/step2_results.md`](results/step2_results.md); see [`design_v2.md`](design_v2.md), section 8. They need Ollama with `qwen2.5vl:7b` and `qwen2.5:7b`.

## Dev checks

The scripts in `scripts/dev_checks/` use dev data only and never touch test. Their results are in `design_v2.md`, sections 8 and 9.

| Script | What it checks | Output |
|---|---|---|
| `verify_dev.py`, `verify_eval.py` | Yes/no symptom list over the stage-1 top 3 | `results/verify_dev.jsonl` |
| `shape_dev.py`, `shape_crops.py`, `shape_model.py` | Blast vs brown spot lesion shape: whole photo, crops, reference photos, five VLMs | `results/shape_*.jsonl` |
| `lambda_dev.py` | Step-2 λ: fine grid, R@1 vs MRR, bootstrap stability | Printed; summary in `design_v2.md` 9.1 |
| `ikrl_v2_dev.py` | IKRL on split v2, with a random-class-vector capacity control | [`results/ikrl_v2_dev.md`](results/ikrl_v2_dev.md) |

| `link_pred_dev.py` | Link prediction with the photo's own edges: safe, age and variety, dataset, leaking | [`results/link_pred_dev.md`](results/link_pred_dev.md) |
| `zsl_dev.py` | KG-based generalized zero-shot, leave one condition out; KG vs shuffled control vs CLIP text | [`results/zsl_dev.md`](results/zsl_dev.md) |

## Rebuild

**Requirements:**
- `make_split.py` needs `rdflib` only.
- The other scripts need a GPU environment with torch, transformers, scikit-learn and rdflib:
  - Windows / RTX 5090: `D:\venvs\ricemmkg-retrieval`, torch with CUDA 12.8;
  - macOS: the conda environment `mmkg-rag`, torch with MPS or CPU.
- `Data/retrieval/` is not in Git. Copy it, or let OneDrive sync it, before running.

```bash
python -I "Retrieval Benchmark/scripts/make_split.py" . Data/retrieval        # first run: v1 groups, also writes the MD5 cache
<venv>/python -I "Retrieval Benchmark/scripts/stage1_baselines.py" . "Retrieval Benchmark/results"   # caches CLIP features
<venv>/python -I "Retrieval Benchmark/scripts/capture_groups.py" .
python -I "Retrieval Benchmark/scripts/make_split.py" . Data/retrieval        # v2, using capture_groups.csv
python -I "Retrieval Benchmark/scripts/make_gold.py" .
<venv>/python -I "Retrieval Benchmark/scripts/stage1_baselines.py" . "Retrieval Benchmark/results"
<venv>/python -I "Retrieval Benchmark/scripts/stage2_passages.py" . "Retrieval Benchmark/results"
<venv>/python -I "Retrieval Benchmark/scripts/step2_vlm_triples.py" . closed "Retrieval Benchmark/results/vlm_triples_closed.jsonl"
<venv>/python -I "Retrieval Benchmark/scripts/step2_vlm_triples.py" . open "Retrieval Benchmark/results/vlm_triples_open.jsonl"
<venv>/python -I "Retrieval Benchmark/scripts/step2_rerank.py" . "Retrieval Benchmark/results/vlm_triples_closed.jsonl" "Retrieval Benchmark/results/vlm_triples_open.jsonl" "Retrieval Benchmark/results"
python -I "Retrieval Benchmark/scripts/make_questions.py" .
<venv>/python -I "Retrieval Benchmark/scripts/step1_question.py" . "Retrieval Benchmark/results/step1_question_dev.md"
<venv>/python -I "Retrieval Benchmark/scripts/step2_llm_gate.py" . "Retrieval Benchmark/results/vlm_triples_open.jsonl" "Retrieval Benchmark/results"
<venv>/python -I "Retrieval Benchmark/scripts/step2_field_context.py" . "Retrieval Benchmark/results/step2_field_context_dev.md"
<venv>/python -I "Retrieval Benchmark/scripts/dev_checks/lambda_dev.py" .
<venv>/python -I "Retrieval Benchmark/scripts/dev_checks/ikrl_v2_dev.py" . "Retrieval Benchmark/results/ikrl_v2_dev.md"
```

The first run hashes every image. Files that OneDrive keeps online only are downloaded first. The hashes are cached in `Data/retrieval/md5_cache.csv` and the CLIP features in `Data/retrieval/feats_clip-l14.npz`.
