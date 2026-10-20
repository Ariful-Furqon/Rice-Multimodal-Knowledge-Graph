# Rice MMKG: SIGIR 2027 Plan

Drafted 2026-10-20. It replaces the ESWC plan ([riceMMKG_ESWC_plan.md](riceMMKG_ESWC_plan.md)) as the working schedule. The order of work in that plan still holds.

## 1. Venue

| | Date | Source |
|---|---|---|
| Abstract deadline | probably about 2027-01-07 | **unconfirmed**; SIGIR usually sets one about a week before the paper deadline |
| Paper submission | 2027-01-14 | conference-tracker page; **check the official CFP** |
| Notification | 2027-04-05 | same |
| Conference | 2027-07-18, San Jose, California | same |

**Track: to be decided with the supervisor.** Each track may have its own deadline.

- **Resource & Reproducibility track (recommended).** The contribution is a resource: the KG, the CQ benchmark and a retrieval test collection, with baselines. This fits what already exists.
- **Full paper track.** This would need a new retrieval method that wins clearly over strong baselines. The risk is higher with about 10 working weeks left.

## 2. Contribution claim (draft)

Rice MMKG is a multimodal knowledge graph for rice health that links image, sensor, trap and remote-sensing observations to curated domain knowledge. Every curated assertion traces to its source document, and the Phase B text work extends this to the source passage. It ships with a retrieval test collection and shows where the graph helps retrieval and where it does not.

The gap, from [Related_Work_Text_Modality.md](../Analysis%20and%20Alignment/Related_Work_Text_Modality.md):
- Crop GraphRAG is text only.
- AgriDoctor is multimodal but has no KG.
- Sentence-level evidence exists in other domains only.
- No agricultural KG was found that combines all three with a retrieval evaluation.

## 3. Use case

The supervisor asked for a use case and test cases. The question was whether the test should be embedding classification or QA. **Answer: one use case with two stages.** Embedding classification is stage 1 and QA retrieval is stage 2.

### 3.1 Evidence-based diagnosis and advice

A farmer or extension worker has a photo of a rice plant and a question. For example: *"My leaves have grey, diamond-shaped spots. What is it and how do I treat it?"* The system should do two things:
1. say what the problem most likely is;
2. return the evidence for its cause and management, each item traceable to its source.

| Stage | What the system does | Framed as | Metrics |
|---|---|---|---|
| **1. Identification** | Photo and/or description → ranked list of candidate diseases and pests | Classification framed as ranking; image embedding fused with KG class embeddings (IKRL-style, as in `Multimodal Fusion PoC/ikrl_vs_cnn.py`) | MRR, Hit@1, Hit@3, macro-F1 |
| **2. Evidence retrieval** | Candidates + question → KG facts and source passages on cause, management and prevention | QA as retrieval | nDCG@10, Recall@k, MRR |
| *3. Answer (optional)* | An LLM writes the answer from the stage-2 evidence only | Retrieval-augmented generation | Citation accuracy: is each claim supported by the retrieved evidence |

**Research question:** does the KG improve each stage over the same system without the KG?

**Why not either option alone:**
- *Classification alone* is not information retrieval. A SIGIR reviewer would ask where the retrieval is. The existing result (KG fusion 71.1% vs plain ResNet-18 62.6% accuracy, `ikrl_vs_cnn_results.md`) supports stage 1 but cannot carry the paper.
- *Generative QA alone* is hard to judge and does not show what is distinctive about Rice MMKG. Rice MMKG's strength is traceable evidence, so the main test measures whether the right evidence is found. The quality of the wording is secondary.

### 3.2 Test cases

One test case has:
- a held-out photo, whose `annotatedAs` link is removed from the KG at query time;
- a farmer-style question;
- gold answers: (a) the true disease or pest for stage 1; (b) the relevant facts and passages, graded 0/1/2, for stage 2.

Example:

| Field | Value |
|---|---|
| Photo | held-out Rice Blast image |
| Question | "What is this and how do I control it?" |
| Gold, stage 1 | `Rice_Blast_Disease` |
| Gold, stage 2 | its `controlledBy` / `preventedBy` / `increaseRiskOf` facts, and the IRRI blast passages that state them (grade 2); general blast passages (grade 1) |

Sizes:
- stage 1: several hundred test images, stratified by class and dataset; gold comes from dataset labels, so no judges are needed;
- stage 2: about 50 test cases, judged by humans.

Stage 2 is scored twice: once given the true class (oracle) and once given the stage-1 output (end to end). This shows how much error each stage adds.

## 4. Retrieval evaluation design

This is the main new work. The CQ benchmark measures coverage, not ranking quality, so it stays as a secondary evaluation.

### 4.1 Tasks

The three tasks map onto the stages of the use case: T1 and T2 cover stage 1 and the input of stage 2, and T3 is stage 2.

| Task | Stage | Query | Collection | Relevance |
|---|---|---|---|---|
| **T1: Text → image** | 1 (description only) | A symptom description or a farmer-style question ("leaves with grey, diamond-shaped lesions") | Image observations at the data freeze | Graded. 2 = image of the target disease or pest; 1 = image showing a symptom the query names. Taken from dataset labels, not from the KG |
| **T2: Image → knowledge** | 1 (photo) → 2 | A held-out image | Classes, then curated assertions and text passages | Class rank from the dataset label. Evidence graded 2 = about the true class and answers the need (cause, management); 1 = about the class but not the need |
| **T3: Question → evidence** | 2 | The use-case questions (3.2), the elicited CQs, and new extension-worker questions | IRRI passages + KG facts | Pooled human judgements, 0/1/2 |

**Leakage rule (from `Multimodal Fusion PoC/ikrl_vs_cnn.py`):**
- The graph used at query time must not contain the `annotatedAs` link of any test image.
- Test images are split off before any KG-based method sees them.
- Without this, KG methods win trivially, because the qrels for T1 and T2 come from the same labels.

### 4.2 Systems

| Group | Systems |
|---|---|
| Lexical | BM25 over passages and over labels and comments of entities |
| Dense text | bge-m3 (already running locally through Ollama) |
| Image | CLIP or SigLIP zero-shot; the frozen ResNet-18 from the PoC as a supervised reference |
| **KG-augmented (ours)** | (a) query expansion along `indicatedBy`, `affectsPlantPart`, `causes`; (b) graph re-ranking of first-stage results; (c) entity-linked hybrid: link the query to entities, then retrieve their images and passages |
| Ablations | Remove KG, text or image; remove provenance; asserted graph vs OWL RL graph |

### 4.3 Metrics and statistics

- Main metrics: nDCG@10, Recall@100 and MRR. MAP is reported for T3.
- Significance: paired randomisation test or bootstrap per query, with Holm correction across systems.
- Judge agreement on T3: Cohen's κ for two annotators, plus expert E1 on a subset.

### 4.4 Query set size (target)

| Task | Queries | How |
|---|---|---|
| T1 | 50–80 | Written from symptom descriptions in IRRI fact sheets and expert input; paraphrased so they do not copy labels |
| T2 | 200+ images | Stratified sample of held-out images across classes and datasets |
| T3 | 50 | The about 50 use-case test cases of 3.2, written to cover the 19 elicited Tier A CQs; judgements pooled from the top 10 of every system |

**Judging budget for T3:** about 50 queries × about 40 pooled items = about 2,000 judgements. Two annotators are needed, about 6–8 hours each. Ask E1 and the two other raters early (week 4).

## 5. Schedule

Weeks start on Monday. Holidays fall in weeks 10–11.

| Week | Dates | Work | Output |
|---|---|---|---|
| 1 | Oct 19–25 | Finish the text pilot; confirm track, CFP and the use case (section 3) with the supervisor | Pilot scores; track and use-case decision |
| 2 | Oct 26–Nov 1 | `TextPassage` and NC-SA module; read related work; **freeze this evaluation design** | Text layer in KG; design v1 |
| 3 | Nov 2–8 | Build the test split; write the use-case test cases and T1 queries; index for BM25, bge-m3 and CLIP; stage-1 baseline (ResNet/CLIP) and KG fusion re-run on the frozen data | Test cases; baseline runs; stage-1 results |
| 4 | Nov 9–15 | KG-augmented methods (a)–(c); send the judging request | First KG runs |
| 5 | Nov 16–22 | Pooling; judges at work | Pools |
| 6 | Nov 23–29 | Judgements back; agreement; fix the qrels | qrels v1, κ |
| 7 | Nov 30–Dec 6 | Full runs; significance tests | Results tables |
| 8 | Dec 7–13 | Ablations; error analysis; release prep (w3id docs, Zenodo DOI, licence of each module) | Release candidate v0.9 |
| 9 | Dec 14–20 | Full draft | Draft 1 → supervisor |
| 10–11 | Dec 21–Jan 3 | Supervisor review; buffer (holidays) | Comments |
| 12 | Jan 4–10 | Revise; submit abstract (about Jan 7, if required) | Abstract |
| 13 | Jan 11–14 | Final checks, reproducibility package, submit | **Submission** |

**Checkpoints:**
- **End of week 4:** if no KG-augmented method beats the best baseline on any task, change the claim from "KG improves retrieval" to "resource + analysis of when it helps". This only works for the Resource track.
- **End of week 6:** if the T3 judgements are late, submit with T1 and T2 only. Their qrels come from labels and need no judges.

## 6. Risks

| Risk | Mitigation |
|---|---|
| Label leakage makes KG results look too good | Leakage rule in 4.1; report it in the paper |
| Not enough judges | T1 and T2 do not need judges; keep T3 at 50 queries |
| IRRI text is CC BY-NC-SA | Release passages as a separate module; the core and qrels refer to passages by pointer |
| Image classes are unbalanced across datasets | Stratified test sample; report results per dataset |
| Only CPU is available | Frozen encoders; precompute embeddings once |

## 7. Decisions for the supervisor

1. Which track: Resource & Reproducibility, or full paper?
2. Is the two-stage use case (identification, then evidence retrieval; section 3) the right answer to "embedding classification or QA"? Should the optional stage 3 (LLM answer) be included?
3. Who judges T3: E1 and the two raters, or lab members?
4. Is an author-written query set acceptable, or is an external source needed (for example extension-service question logs)?
