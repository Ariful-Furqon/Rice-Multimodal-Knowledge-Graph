# Related Work: Text Modality

Reading list for the text modality of Rice MMKG (text-pilot of 2026-10-20). It was collected from one round of web search on 2026-10-20. **Status: not yet read in full.** Verify each paper's claims from the full text before citing it.

The design this list supports is recorded in the text-modality notes: facts and passage pointers in the CC BY core, IRRI passage text in a separate CC BY-NC-SA module, and matched extractions attached as evidence to the existing `owl:Axiom`.

## 1. LLM text extraction in the rice and crop domain

| Paper | What it does | Relevance |
|---|---|---|
| Crop GraphRAG ([PMC12812888](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12812888/)) | Builds a crop pest and disease KG from text, then uses it for retrieval-augmented QA | Direct baseline for the SIGIR retrieval story. Text only, no images |
| KG for crop diseases and pests in China ([PMC11802884](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11802884/)) | Large pest and disease KG built from text | Domain KG built from text, for comparison of scale and schema |
| Rice trait ontology curation with LLM and PubAnnotation ([PMC12670841](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12670841/)) | Links LLM extractions to sentence-level evidence in the literature | Closest to our `hasEvidencePassage` idea |
| LLM bioregulatory event extraction on rice literature ([Genomics & Informatics 2024](https://genomicsinform.biomedcentral.com/articles/10.1186/s44342-024-00022-3)) | Compares LLMs with a deep-learning pipeline | Reports that LLMs have higher precision and lower recall; expect the same pattern in the pilot |
| Rice pest and disease LLM + KG (Chinese journal, [aeeisp.com](https://www.aeeisp.com/nygcxb/cn/article/id/5e47e172-a5d8-4450-9a8a-72ac78bceb3a)) | Keeps established attributes separate from new extractions | Similar to our rule that new relations stay candidates |
| Thai rice disease KG ([ISJET](https://ph02.tci-thaijo.org/index.php/isjet/article/download/258104/172467/986495)) | Rice disease KG | Regional rice KG for comparison |
| CropKG, Wu et al. 2026, *Computers and Electronics in Agriculture* 250, 111970 | Schema induction, chunking, evidence-constrained extraction, alignment | The pipeline the pilot reuses, with a fixed Rice MMKG schema replacing schema induction |

## 2. Schema-constrained extraction evaluated against a gold standard

| Paper | What it does | Relevance |
|---|---|---|
| Text2KGBench, 2023 ([arXiv 2308.02357](https://arxiv.org/abs/2308.02357)) | Benchmark of ontology-driven fact extraction | Found LLMs comply with the ontology but have only moderate fact accuracy. Main method reference for the pilot |
| KEO ([arXiv 2510.05524](https://arxiv.org/pdf/2510.05524)) | Separates strict evaluation (both entities already in the graph) from loose evaluation | Useful for reporting entity-linking quality |
| Other schema-constrained extraction work | [arXiv 2507.03829](https://arxiv.org/html/2507.03829v1), [arXiv 2509.00140](https://arxiv.org/pdf/2509.00140v1), [SWJ 4014](https://semantic-web-journal.net/system/files/swj4014.pdf), LREC 2026 framework by Ilves, Barbu and Übi ([ACL Anthology](https://aclanthology.org/people/jaan-ubi/)) | To be screened |

## 3. Linking assertions to their evidence text

| Paper | What it does | Relevance |
|---|---|---|
| Extended nanopublications with knowledge provenance, Giachelle et al. 2025 ([Springer](https://link.springer.com/article/10.1007/s00799-025-00431-x)) | Notes that standard provenance points to a document, not a text fragment, and adds a knowledge-provenance component | The gap that `TextPassage` with offsets fills |
| Micropublications ([arXiv 1305.3506](https://arxiv.org/pdf/1305.3506)) | Semantic model of claims, evidence and annotation in biomedical publications | Model for claim and evidence structure |
| PubAnnotation fragments as nanopublication evidence ([FAIR Data Team wiki](https://fairdatateam.atlassian.net/wiki/x/BYAV)) | Records the URI of a text fragment as evidence | Nearest example of fragment-level linking |
| Corpus provenance via nanopublications ([arXiv 2006.06341](https://ar5iv.labs.arxiv.org/html/2006.06341)) | Provenance for corpus-derived statements | Background |
| EvidenceNet ([arXiv 2603.28325](https://www.alphaxiv.org/abs/2603.28325)) | Biomedical evidence graph | Background |

## 4. Multimodal (image, text and KG) in agriculture

| Paper | What it does | Relevance |
|---|---|---|
| AgriDoctor ([arXiv 2509.17044](https://arxiv.org/html/2509.17044v1)) | Multimodal agent for crop disease diagnosis | Agent pipeline, not a KG |
| AgriChat / AgriMM ([arXiv 2603.16934](https://arxiv.org/html/2603.16934v1)) | Multimodal agricultural assistant | Not a KG |
| Frontiers in Plant Science 2025 ([fpls.2025.1696872](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2025.1696872/full)) | To be screened | — |
| Patent CN122021845A ([goveda](https://www.goveda.com/patent/CN-122021845-A)) | Multimodal agricultural KG with image, text and sensor data | The only image + text + sensor KG found. It is a patent, not an evaluated paper |

## Gap for Rice MMKG

The search found:

- agricultural KGs built from text (Crop GraphRAG);
- multimodal agents without a KG (AgriDoctor);
- sentence-level evidence in other domains (rice traits, biomedicine).

It found no agricultural KG that combines multimodal observations, per-assertion provenance down to the source passage, and a retrieval evaluation. This is the positioning argument for SIGIR 2027.

## Still to search

- W3C Web Annotation selectors (`TextPositionSelector`, `TextQuoteSelector`) used to anchor KG assertions to text. These could give the passage offsets a W3C-standard representation.
