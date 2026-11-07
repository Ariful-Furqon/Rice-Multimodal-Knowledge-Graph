# Related Work: Leakage and Dataset Bias

Reading list for the link prediction and IKRL checks of the retrieval benchmark ([`design_v2.md`](../Retrieval%20Benchmark/design_v2.md), sections 9.2 and 9.3). It was collected from one round of web search on 2026-11-07. **Status: checked against abstracts and publisher pages only, not read in full.** Verify each number from the full text before citing it.

The findings this list supports:
- In-source, edges that copy the label (`sourceLabel`, the folder name in `schema:contentUrl`) raise link prediction R@1 from 0.612 to 0.798. A lookup from the folder name alone gives 1.000.
- Cross-source, the leak does not transfer: the lookup gives 0.000.
- The "safe" photo edges, plant age and variety are dataset or session markers. The pixels already identify the dataset (0.993).
- Domain triples do not reach the photo, so IKRL with TransE class vectors is no better than random class vectors.

## 1. Leakage in link prediction benchmarks

| Paper | What it does | Relevance |
|---|---|---|
| Toutanova & Chen 2015, *Observed versus latent features for knowledge base and text inference*, CVSC workshop, pp. 57–66 ([ACL Anthology W15-4007](https://aclanthology.org/W15-4007/)) | A simple observed-features model is surprisingly strong on FB15k and WN18. The work is linked to FB15k-237 | Origin of the cleaned Freebase benchmark. Check in the full text what it says about inverse relations |
| Dettmers et al. 2018, *Convolutional 2D Knowledge Graph Embeddings*, AAAI ([AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/11573/), [arXiv 1707.01476](https://arxiv.org/abs/1707.01476)) | Shows test-set leakage through inverse relations in WN18 and FB15k: a simple rule-based model reaches state of the art | Closest analogue to our folder-name lookup, which needs no model at all |
| Akrami et al. 2020, *Realistic Re-evaluation of Knowledge Graph Completion Methods*, SIGMOD ([arXiv 2003.08001](https://arxiv.org/abs/2003.08001)) | Removes redundancy-driven test cases from FB15k, WN18 and YAGO3-10; performance drops sharply. Also flags Cartesian product relations | Same lesson for a KG with photo nodes: the string copies of the label play the role of inverse relations |

## 2. Leakage in machine learning in general

| Paper | What it does | Relevance |
|---|---|---|
| Kaufman et al. 2012, *Leakage in data mining: formulation, detection, and avoidance*, ACM TKDD 6(4), art. 15 ([DOI 10.1145/2382577.2382579](https://www.doi.org/10.1145/2382577.2382579)) | Formal definition of leakage; learn–predict separation; detection when data collection is not under the modeller's control | Formal frame for why `sourceLabel` must be cut at query time |
| Kapoor & Narayanan 2023, *Leakage and the reproducibility crisis in machine-learning-based science*, Patterns 4, 100804 ([PMC10499856](https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856)) | Leakage in at least 294 papers across 17 fields; a taxonomy of eight leakage types; model info sheets | Use the taxonomy to name our cases (a feature that is a proxy for the label; non-independent train and test photos within a capture session) |

## 3. Dataset bias and shortcut learning

| Paper | What it does | Relevance |
|---|---|---|
| Torralba & Efros 2011, *Unbiased Look at Dataset Bias*, CVPR ([CMU RI](https://ri.cmu.edu/?p=7313)) | The "Name That Dataset" game; cross-dataset generalization | Our source dataset is predicted from CLIP features with 0.993 accuracy |
| Liu & He 2025, *A Decade's Battle on Dataset Bias: Are We There Yet?*, ICLR 2025 oral ([proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/66772e6aa61e54ae16443ae1d78a7319-Abstract-Conference.html), [arXiv 2403.08632](https://arxiv.org/abs/2403.08632)) | Modern networks tell YFCC, CC and DataComp apart with 84.7% accuracy | Dataset identity remains easy to learn even for large, diverse web datasets |
| Geirhos et al. 2020, *Shortcut learning in deep neural networks*, Nature Machine Intelligence 2:665–673 ([MPI](https://is.mpg.de/publications/geirhosetal20), DOI 10.1038/s42256-020-00257-z) | Shortcuts do well on standard benchmarks and fail under harder test conditions; recommendations for benchmarking | Conceptual frame for in-source vs cross-source |
| Zech et al. 2018, *Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs*, PLOS Medicine ([PMC6219764](https://pmc.ncbi.nlm.nih.gov/articles/PMC6219764)) | A CNN identifies the hospital system of a radiograph (99.95% NIH, 99.98% Mount Sinai). Sorting by hospital alone gives AUC 0.861, and external performance drops | Closest analogue outside agriculture: the source is visible in the pixels and confounds the label, as with our datasets |

## 4. Bias in plant disease image datasets

| Paper | What it does | Relevance |
|---|---|---|
| Mohanty et al. 2016, *Using Deep Learning for Image-Based Plant Disease Detection*, Frontiers in Plant Science ([PMC5032846](https://pmc.ncbi.nlm.nih.gov/articles/PMC5032846)) | 99.35% on held-out PlantVillage, 31.4% on images from other sources | The standard citation for the in-source vs cross-source gap in plant disease recognition |
| Noyan 2022, *Uncovering bias in the PlantVillage dataset*, arXiv preprint ([arXiv 2206.04374](https://arxiv.org/abs/2206.04374)) | 8 background pixels give 49% accuracy (chance 2.6%); attributed to capture bias | Same mechanism as Dhan-Shomadhan matching the white-background nutrient datasets. Preprint, not peer reviewed |
| Barbedo 2018, *Factors influencing the use of deep learning for plant disease recognition*, Biosystems Engineering 172:84–91 (DOI 10.1016/j.biosystemseng.2018.05.013) | Nine factors behind misclassification, including background and capture conditions | Background for the data-gap discussion |

## 5. Methods and datasets used in the checks

| Paper | What it does | Relevance |
|---|---|---|
| Xie et al. 2017, *Image-embodied Knowledge Representation Learning* (IKRL), IJCAI, pp. 3140–3146 ([IJCAI](https://www.ijcai.org/proceedings/2017/438)) | Entity representations from triples and images, with attention over an entity's images | Basis of heads B and C in section 9.2 |
| Petchiammal et al. 2023, *Paddy Doctor: A Visual Image Dataset for Automated Paddy Disease Classification and Benchmarking*, CODS-COMAD, pp. 203–207 ([arXiv 2205.11108](https://arxiv.org/abs/2205.11108)) | 16,225 field images, 13 classes, with variety and age recorded per image | Source of the `plantAgeDays` and `ofVariety` edges that identify a capture session |

## Gap for Rice MMKG

- Leakage through inverse or redundant triples is well documented for text KG benchmarks (section 1). For a multimodal KG whose photo nodes carry the source label as a string, we found no study that measures it.
- Dataset bias in plant disease images is documented (section 4), but not in combination with a KG whose edges are themselves dataset markers.
- Our contribution in the analysis: a leakage table (in-source up to 1.0 with a folder lookup, 0.0 cross-source) and the rule that KG-augmented image results must be reported cross-source.

## Still to search

- Early stopping chosen on a shortcut feature: validation accuracy peaks early and the model stays under-trained for groups that lack the feature (design_v2.md 9.3, reading 3). Candidate areas are spurious features and simplicity bias.
- Leakage or shortcut studies on multimodal KG completion benchmarks (FB15k-237-IMG, WN9-IMG, MMKG).
