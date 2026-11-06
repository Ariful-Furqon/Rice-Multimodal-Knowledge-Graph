# Rice MMKG: SIGIR 2027 Plan

Drafted 2026-10-20 and revised 2026-10-26 after the supervisor's feedback that the retrieval side was too weak. The paper now targets the **full paper track with a retrieval method**. It replaces the ESWC plan ([riceMMKG_ESWC_plan.md](riceMMKG_ESWC_plan.md)) as the working schedule.

**Update 2026-11-05:** the venue is under review and next week's work has changed; see section 0. Sections 1–8 still describe the SIGIR plan.

**Update 2026-11-06:** a dev-only re-check of the λ tuning, and a diagnosis of why step 2 fails. Two items are added to next week (section 0.1).

## 0. Status and next week (2026-11-05)

**Venue proposal: IEEE Access.**
- The supervisor suggested IEEE Access for Rice MMKG. SIGIR stays possible only with a new method evaluated on OMGM's benchmark datasets, which would be a different project.
- The article fee would come from lab funds.
- To confirm at the weekly meeting on 2026-11-06. If confirmed, sections 1, 2 and 6 are rewritten for a journal paper:
  - the KG's contribution becomes evidence retrieval;
  - disease re-ranking becomes an analysis section.

**Done in week 3 (Nov 2–8).** Details are in [design_v2.md](../Retrieval%20Benchmark/design_v2.md), sections 6–8.
- **Split v2 and query-time graph.** The split is by photo, with capture groups. The query-time graph drops 49,557 triples of 5,935 dev and test photos and keeps 275,144.
- **Questions.** Templates, dev questions with simulated observations, and 20 draft test cases with empty observations ([splits/](../Retrieval%20Benchmark/splits/)).
- **Step 2 on test_core.**
  - In-source, KG triples raise R@1 from 0.513 to 0.528, which is not significant (MRR p = 0.164).
  - Cross-source, dev chose λ = 0.
  - The KGMEL baseline reaches 0.258.
- **Five step-2 experiments, on dev only:**
  - yes/no symptoms;
  - gated LLM;
  - lesion shape with five open-weight VLMs (best 0.567 against a 0.7 stop rule);
  - plant age;
  - simulated farmer's words.

  None gives a real gain. Only the simulated words help, with in-source R@1 from 0.536 to 0.652 at noise 0, and they are an upper bound because they are drawn from the answer. The KG was not changed.
- **Step 3 (OMGM reranker inside KG tiers, stage-1 top 2), on the full main test set:**
  - Cause MRR is 0.536 end to end and 0.889 with the gold condition.
  - The KG route beats the route without the KG in every column.
  - "Identify" falls with the reranker, partly because the section gold accepts one section only.

**Checkpoint 1 (15 Nov): not met.** The fallback named in section 6, LLM re-ranking as in KGMEL, was tried and is worse (0.258). Step 2 is therefore reported as analysis, not as the method's gain.

### 0.1 Step-2 diagnosis (2026-11-06, dev only, no test data)

**λ tuning is not the problem.**
- The current tuning is a grid search over 8 values of λ, with R@1 on dev_core as the criterion and ties going to the smaller λ (`step2_rerank.py`).
- It was re-run with a finer grid (0 plus 40 log-spaced values, 0.01–10), with R@1 and MRR as criteria, and with 2,000 bootstrap resamples of dev.
- **In-source:** both criteria choose λ ≈ 0.2, as before. Dev MRR rises only from 0.682 to 0.690. λ = 0.2 beats λ = 0 in 88% of resamples, below 95%. Above λ ≈ 0.35 the scores fall steeply.
- **Cross-source:** the curve is flat. R@1 chooses λ = 0. MRR chooses λ ≈ 4 for +0.002, which wins in only 52% of resamples, so it is noise. The bootstrap choices range from 0.01 to 3.5.
- **Decision:** the script is left unchanged. MRR argmax would switch on a noisy λ cross-source. The dev curve of R@1 and MRR against λ goes into the paper as a sensitivity figure.

**The bottleneck is symptom perception, plus a gap in the KG for look-alike diseases.**
- **The VLM misses symptoms in general, not only look-alikes** (design_v2.md, section 8):
  - only 24% of the photos of sick plants have a triple that matches their gold condition;
  - six conditions are never matched;
  - "yellow stripe" appears on 131 of 345 photos;
  - deadheart is reported on 0 of 15 stem borer photos.
- **Blast vs brown spot fails twice:**
  - on leaf photos the KG gives both the same symptoms (`Brown Lesion`, `Leaf Spot`, `Wilting`), so their KG scores are equal whatever the VLM says;
  - the feature that separates them, lesion shape, cannot be read by any of the five open-weight VLMs (best 0.567, near chance).
- **The fusion works when the symptoms are right.** With simulated farmer's words, in-source R@1 rises from 0.536 to 0.652. This is an upper bound, because the words are drawn from the answer.

**Options considered:**

| Option | Decision |
|---|---|
| Closed frontier VLM via a paid API, as an upper bound | **Not pursued**, at the author's choice |
| Symptom detector trained from the disease labels | **Rejected.** With disease labels only, it collapses into stage 1 and adds no KG information. Real symptom annotations would be needed |
| Higher resolution with the local VLMs: all runs so far used 768 px | **Run next week.** It is the last untested perception variable, and reviewers will ask about it |
| KG-chosen clarifying question: the farmer is the sensor, and the KG picks the question | **Design next week.** It is the KG contribution that does not depend on the VLM |
| Main claim on evidence retrieval (step 3), with step 2 as a controlled negative result | **Adopted for the paper**, in line with the IEEE Access rewrite (item 6 below) |

**The question option:**
- Stage 1 gives the top-k candidates.
- The KG picks the symptom that best separates them, by information gain over the candidates. Example: *"Are the spots diamond-shaped with a grey centre, or round and evenly brown?"*
- The answer is fused with the stage-1 score.
- **Needs:**
  - discriminative symptoms added to the KG, such as lesion shape from the IRRI sheets. In this route they help, because a person supplies the observation, not the VLM;
  - the question selection;
  - an evaluation with a simulated user on dev, reported as a sensitivity analysis because it is circular, plus expert answers on the 20 draft test cases (item 2 below).

**Next week (Nov 9–15):**

| # | Work | Output |
|---|---|---|
| 1 | **Link prediction, the supervisor's idea:** keep the photo node, cut `annotatedAs` and the leaking edges (`rdfs:label`, `contentUrl`, `sourceLabel`, `captures`; variety + age and `wasDerivedFrom` tested separately), predict the label from the pixels and the safe edges. Dev first | Dev table, with and without the leaking edges |
| 2 | **Expert package:** a form for pooled passage judgements (0/1/2), observations for the 20 draft test cases, and a label check. Sent only after the supervisor agrees | Form ready to send |
| 3 | **Text coverage:** open texts for the three diseases without an IRRI sheet (bacterial panicle blight, downy mildew, leaf scald), and cause and control texts (CABI or open papers). Must be done before pooling, by Nov 22 | New passages linked to facts |
| 4 | **Reranker pool size:** recall@k and MRR for k = 20, 50 and 100 on dev; k = 50 is a default so far, not a tuned value | One dev table |
| 5 | **Significance of the evidence table:** paired sign-flip test per query, KG vs no KG and before vs after the reranker | p-values for the step-3 table |
| 6 | **Plan rewrite**, if IEEE Access is confirmed | Revised sections 1, 2 and 6 |
| 7 | **High-resolution lesion shape:** the same 60 blast and brown spot photos at about 1536 px, or 2×2 tiles with a vote. Local Ollama models (`qwen2.5vl`, `gemma4`) with `shape_model.py`. Same stop rule (balanced accuracy ≥ 0.7). If it fails, the perception route is closed | One dev row per model |
| 8 | **KG-chosen clarifying question, design (section 0.1):** discriminative symptoms to add to the KG, the information-gain selection, and the protocol for a simulated user. Observations for the 20 test cases come from the expert package (item 2) | Design note; dev run if time allows |
| 9 | **λ sensitivity figure:** R@1 and MRR against λ on dev, per protocol, as in the 2026-11-06 check; the script moves to `scripts/dev_checks/` | Figure for the analysis section |

**After next week (draft):**
- **Nov 16–22:** pool the top passages of all systems and send the judging request.
- **Nov 23–Dec 6:** expert judgements, κ and the 20 observations.
- **December:**
  - final evaluation on the 2,538 main test photos outside test_core, with test_core used once more at the end;
  - writing.

## 1. Venue

| | Date (AoE) | Source |
|---|---|---|
| Abstract | 2027-01-14 | official call for full papers, sigir2027.org, marked *proposed* |
| Full paper | 2027-01-21 | same; no paper without an abstract |
| Notification | 2027-04-05 | same |
| Camera-ready | 2027-04-30 | same |
| Conference | 2027-07-18 to 24, San Jose, California | same |

**Track: full paper** (decided with the supervisor, 2026-10-26).
- As of late October only the full-paper call is published. The other tracks will be announced separately.
- SIGIR 2024 and 2025 had a combined Resource & Reproducibility track. Its deadline came about four weeks after the full papers (2025: 18 Feb).
- **Fallback, not a parallel submission:** the same paper cannot go to two tracks. If by the abstract deadline (14 Jan) the method does not beat the best baseline, skip the full paper. Then submit a resource paper (benchmark and analysis) to the Resource & Reproducibility track, if that track is announced.

## 2. Contribution claim (draft)

> We propose a knowledge-graph-grounded, coarse-to-fine retrieval method for knowledge-based visual question answering in crop protection. It ranks candidate diseases from a photo, re-ranks them with symptom-level knowledge-graph triples, and reaches evidence sentences through per-fact provenance. We release Rice KB-VQA, a benchmark whose answers are traceable to source sentences, and analyse when the graph helps.

1. **Method:** coarse-to-fine multimodal retrieval:
   - symptom-level KG triples are used for re-ranking, which separates visually similar diseases;
   - provenance links take each fact to its evidence sentence (section 4).
2. **Benchmark:** Rice KB-VQA, built in the style of InfoSeek and Encyclopedic-VQA. Each item has a photo, a question, a gold entity and gold passages (section 5.1).
3. **Analysis:**
   - when KG triples help: confusable classes, context and missing modalities;
   - how much label leakage inflates KG-augmented results.

**Model papers recommended by the supervisor:**
- **OMGM** (Yang et al., ACL 2025): coarse-to-fine retrieval for knowledge-based VQA, in three steps:
  - entity-level cross-modal retrieval;
  - multimodal fusion re-ranking;
  - section-level text re-ranking.
- **Wen et al. 2024** (arXiv 2407.12277): a multimodal reranker between retriever and generator, trained with distant supervision. Noisier training candidates help.
- **KGMEL** (Kim et al., SIGIR 2025 short): uses KG triples for multimodal entity linking, in three steps:
  - a VLM generates triples for the mention;
  - contrastive retrieval over text, image and triples;
  - LLM re-ranking with the candidates' KG triples.

**The gap:** these methods work on encyclopedic knowledge bases (Wikipedia), where entities are visually distinct and evidence means a page section. In crop protection:
- diseases look alike, and they are told apart by their symptoms, the plant part affected and the field conditions;
- the evidence must be traceable to an authoritative source.

Neither problem is addressed by the model papers, by Crop GraphRAG (text only) or by AgriDoctor (no KG). See [Related_Work_Text_Modality.md](../Analysis%20and%20Alignment/Related_Work_Text_Modality.md).

## 3. Task: Rice KB-VQA

A farmer or extension worker has a photo of a rice plant, a question and, optionally, field context. Example:
- **Question:** *"My leaves have grey, diamond-shaped spots. What is it and how do I treat it?"*
- **Context:** rainy season, tillering stage.

The system must:
1. rank the likely diseases or pests (entity retrieval);
2. return the passages that answer the question, each traceable to its source (evidence retrieval);
3. optionally, write an answer that cites them.

| Stage | Output | Metrics |
|---|---|---|
| Entity retrieval | Ranked diseases and pests | Recall@1/5, MRR |
| Evidence retrieval | Ranked passages and KG facts | nDCG@10, Recall@10, MRR |
| *Answer (optional)* | Answer with citations | Answer accuracy, faithfulness, citation accuracy, hallucination rate |

Evidence retrieval is scored twice:
- **Oracle:** given the true entity.
- **End to end:** given the stage-1 output.

The difference shows how much error each stage adds.

## 4. Method: KG-grounded coarse-to-fine retrieval

| Step | What it does | Based on | Rice MMKG part used |
|---|---|---|---|
| **1. Coarse entity retrieval** | Photo + question → top-k candidate diseases and pests. Each entity is represented by its training images plus a text built from its KG description | OMGM step 1 | `annotatedAs` (training split only), labels, comments |
| **2. KG triple re-ranking** | A VLM (Qwen2.5-VL-7B) reads the photo and writes symptom triples, constrained to the KG vocabulary (e.g. *brown lesion – on – leaf sheath*). These are matched against each candidate's triples. Field context adds or removes support for each candidate. Scores are fused with step 1 | KGMEL; Wen et al. | `indicatedBy`, `affectsPlantPart`, `hasAffectedPart`, `increaseRiskOf`, `occursIn`, `vulnerableTo` |
| **3. Evidence via provenance** | Top entities + question intent (cause, control, prevention, symptom) → facts of the matching relations → `hasEvidencePassage` → passages. These are fused with dense passage retrieval and re-ranked with a cross-encoder (bge-reranker) | OMGM step 3, with provenance as an exact route to evidence | `causes`, `controlledBy`, `preventedBy`, `recommends`; `owl:Axiom` → `TextPassage` |
| *4. Answer* | An LLM answers from the step-3 evidence only and cites passage IRIs | RAG | IRRI text module |

**Design choices:**
- **Soft linking.** The candidate distribution from step 1 is carried into steps 2 and 3, instead of committing to a single label. This makes the method robust when the photo is misidentified.
- **Closed vocabulary for the VLM.** Generated triples must use the symptom and plant-part labels in the KG. This limits hallucinated symptoms.
- **Little training.** Steps 1 and 3 use frozen encoders. Step 2 trains a small fusion weight on the training split, with distant supervision from dataset labels, as in Wen et al.

## 5. Evaluation

### 5.1 Benchmark construction

| Part | Size (target) | How | Gold |
|---|---|---|---|
| Entity queries | 200+ held-out photos | Stratified across classes and datasets | Dataset label |
| Training and dev questions | Several thousand | Templates per relation (cause, control, prevention, symptom) over training images; paraphrased with an LLM | Entity from the label; **silver** passages from provenance |
| Test cases | About 50 | Photo + farmer-style question (+ context), written to cover the 19 elicited Tier A CQs | Entity from the label; passages from **pooled human judgements**, 0/1/2 |

**Two rules against circularity:**
- **Leakage:** the graph used at query time holds no `annotatedAs` link of a test image. Test images are split off before any KG-based method sees them.
- **No silver qrels in the test set:** the method uses provenance links, so qrels derived from them would favour it by construction. Test qrels come only from pooled human judgements. The silver passages are used for training and development only.

### 5.2 Systems

| Group | Systems |
|---|---|
| Lexical and dense | BM25; bge-m3 |
| Image and multimodal | CLIP or SigLIP zero-shot; frozen ResNet-18; IKRL fusion (`Multimodal Fusion PoC/`) |
| Model papers | OMGM (code public), KGMEL (code public), a Wen-style multimodal reranker, each adapted to Rice KB-VQA |
| GraphRAG | MegaRAG (reproduced in July 2026); LightRAG; a graph extracted by an LLM from the same IRRI text (CropKG-style) |
| **Ours** | Full method (section 4) |
| Ablations | Without step 2; without field context; hard vs soft linking; provenance vs text re-ranking only; curated KG vs LLM-extracted KG; asserted vs OWL RL graph |

### 5.3 Metrics and statistics

- **Entity retrieval:** Recall@1/5 and MRR, also reported for confusable pairs (blast vs brown spot; bacterial leaf blight vs bacterial leaf streak).
- **Evidence retrieval:** nDCG@10, Recall@10 and MRR, oracle and end to end.
- **Answers:** answer accuracy, faithfulness and hallucination rate, the metrics named in the JSPS research proposal.
- **Significance:** paired randomisation test or bootstrap per query, with Holm correction.
- **Judge agreement:** Cohen's κ; expert E1 on a subset.

**Judging budget:** about 50 queries × about 40 pooled passages = about 2,000 judgements. This needs two annotators, about 6–8 hours each.

## 6. Schedule

Weeks start on Monday. Holidays fall in weeks 10–11.

| Week | Dates | Work | Output |
|---|---|---|---|
| 1 | Oct 19–25 | Text pilot; text layer in KG | Done |
| 2 | Oct 26–Nov 1 | Revise this plan; read the code of OMGM and KGMEL; test split with the leakage rule | Design v2 |
| 3 | Nov 2–8 | Questions: templates, training and dev sets, first 20 test cases. Indexes for BM25, bge-m3 and CLIP. Stage-1 baselines and IKRL re-run on the frozen data | Done, with step 2 and step 3 brought forward (section 0) |
| 4 | Nov 9–15 | ~~VLM triple generation; step 2 re-ranking; OMGM and KGMEL adapted~~ Done in week 3. Now: link prediction; expert package; text coverage (section 0) | **Checkpoint 1: not met** (section 0) |
| 5 | Nov 16–22 | Step 3 evidence; end to end; remaining test cases; pooling; send the judging request | Pools |
| 6 | Nov 23–29 | Judges at work; Wen-style reranker; MegaRAG and LightRAG runs | Baseline runs |
| 7 | Nov 30–Dec 6 | qrels and κ; full runs; significance tests | Results tables |
| 8 | Dec 7–13 | Ablations; error analysis on confusable pairs; answer quality | Analysis |
| 9 | Dec 14–20 | Full draft; release preparation (w3id docs, Zenodo DOI, licence of each module) | Draft 1 → supervisor |
| 10–11 | Dec 21–Jan 3 | Supervisor review; buffer (holidays) | Comments |
| 12 | Jan 4–10 | Revise | Draft 2 |
| 13 | Jan 11–14 | **Abstract, 14 Jan**; decide full paper vs fallback | **Checkpoint 2** |
| 14 | Jan 15–21 | Final checks, reproducibility package | **Submission, 21 Jan** |

**Checkpoints:**
- **Checkpoint 1, 15 Nov.** Step 2 must raise entity Recall@1 over step 1 alone, at least on the confusable pairs. If it does not, change the matching: use LLM re-ranking as in KGMEL instead of triple overlap.
  - **Status 2026-11-05: not met.** The KGMEL fallback is worse, and five more experiments on dev gave no real gain (section 0).
  - **2026-11-06:** finer λ tuning changes nothing. The cause is symptom perception and a KG gap for look-alike diseases (section 0.1).
- **Week 6.** If the judgements are late, report entity retrieval and oracle evidence retrieval on the judged subset, and keep the full set for the camera-ready version.
- **Checkpoint 2, 14 Jan.** If the method does not beat the best baseline on evidence retrieval, do not submit the full paper. Move to the Resource & Reproducibility fallback (section 1).

## 7. Risks

| Risk | Mitigation |
|---|---|
| Label leakage makes KG results look too good | Leakage rule in 5.1; report it in the paper |
| Qrels favour the method (circularity) | Test qrels from pooled human judgements only (5.1) |
| The VLM invents symptoms | Closed KG vocabulary; ablation without step 2 |
| The VLM cannot see the symptoms (observed: 24% match; lesion shape near chance for five models) | High-resolution check (section 0, item 7); KG-chosen question to the farmer (section 0.1); step 2 reported as analysis |
| Adapting OMGM or KGMEL takes too long | Reimplement their core step on our data, and say so |
| Not enough judges | Entity retrieval needs no judges; keep the judged set at about 50 queries |
| IRRI text is CC BY-NC-SA | Passages are released as a separate module; the core and qrels refer to passages by pointer |
| Image classes are unbalanced across datasets | Stratified test sample; report results per dataset |
| GPU memory | RTX 5090 (24 GB): a 7B VLM and frozen encoders fit; embeddings are precomputed once |

## 8. Decisions for the supervisor

1. Is the method in section 4 strong enough as the full-paper contribution?
2. May the training and dev questions be generated from KG templates, with only the about 50 test cases written and judged by people?
3. Who judges: E1 and the two raters, or lab members?
4. Include the optional answer stage, or stop at evidence retrieval?
