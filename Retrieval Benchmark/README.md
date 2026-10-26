# Retrieval Benchmark

Data splits and query-time graph for the SIGIR 2027 retrieval experiments. Design: [`Ontology/riceMMKG_SIGIR_plan.md`](../Ontology/riceMMKG_SIGIR_plan.md), section 5.

## Image split (2026-10-26)

[`splits/images_split.csv`](splits/images_split.csv) assigns each of the 21,149 `ImageObservation` individuals at the data freeze to train, dev or test.

| Split | Images |
|---|---:|
| train | 14,802 |
| dev | 3,173 |
| test | 3,174 |
| test_core ([`splits/test_core.csv`](splits/test_core.csv)) | 370 |

**Rules:**
- **Stratification:** by source dataset × `annotatedAs`, 70/15/15, seed 0. This is the same ratio and seed as `Multimodal Fusion PoC/ikrl_vs_cnn.py`.
- **Duplicates:** byte-identical files (same MD5) stay in one split. There are 144 such groups (301 files), all within a single dataset.
- **Label conflicts:** one Paddy Doctor file is labelled both Downy Mildew (`downy_mildew/PDD06425.jpg`) and Rice Tungro Disease (`tungro/PDD12798.jpg`). It has no single gold answer, so both copies stay in train.
- **test_core:** a class-balanced sample of the test split, with at most 15 images per stratum. It is used by the expensive methods, such as VLM triple generation. YUKE-WBC has only 10 test images, so all 10 are in it.

**Not covered:**
- Near-duplicates (the same plant photographed twice) are not detected; MD5 finds exact copies only.
- Dhan-Shomadhan mixes white-background and field photos. The split is not stratified by background.
- The 472 multispectral captures (`RemoteSensingObservation`) are not in this split.

## Query-time graph

`Data/retrieval/RiceMMKG_query_time.ttl` is gitignored and rebuilt by the script.
- **What it removes:** every triple whose subject or object is a dev or test image. That is 53,044 of 324,701 triples, leaving 271,657.
- **What it keeps:** all 384 provenance axioms.
- **Check:** no dev or test image IRI occurs in it. Dev and test images are queries, not graph content. This is the leakage rule of the plan.

## Rebuild

```bash
python -I "Retrieval Benchmark/scripts/make_split.py" . Data/retrieval
```

The first run hashes every image. Files that OneDrive keeps online only are downloaded first. The hashes are cached in `Data/retrieval/md5_cache.csv`.
