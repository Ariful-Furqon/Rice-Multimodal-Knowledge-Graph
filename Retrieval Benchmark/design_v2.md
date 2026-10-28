# Design v2: what to take from OMGM and KGMEL

Week 2 output of the SIGIR 2027 plan ([`Ontology/riceMMKG_SIGIR_plan.md`](../Ontology/riceMMKG_SIGIR_plan.md), section 6). Written 2026-10-27 after reading the code of both papers.

Code read (not run):
- OMGM: [github.com/ChaoLinAViy/OMGM](https://github.com/ChaoLinAViy/OMGM), commit `400ec4b` (2025-12-30).
- KGMEL: [github.com/juyeonnn/KGMEL](https://github.com/juyeonnn/KGMEL), commit `c203765` (2025-06-12).

Local copies are in `D:\Software and Tools\ref-code\`.

## 1. What the code actually does

### OMGM (Yang et al., ACL 2025)

| Step | File | What happens |
|---|---|---|
| 1 Coarse entity search | `test/step1_img2sum.py`, `model/retriever.py` | The query image is encoded with EVA-CLIP-8B (or CLIP ViT-L/14). It is searched in a FAISS index of entity summary texts encoded by the same model, keeping the top 20 entities with their similarities. The question is not used here. |
| 2a Reranker training | `test/step2a_IT2IT_reranker_training.py` | A BLIP-2 Q-Former reranker is trained for 1 epoch on E-VQA. Each query (image + question) gets 15 hard negatives drawn from its step-1 top 20. |
| 2b Rerank | `test/step2b_IT2IT_rerank.py` | The query is (image, question) and each candidate is (one Wikipedia image of the entity, one section). Both become 32 Q-Former tokens. The score is late interaction: for each query token, the max similarity over candidate tokens, averaged. The entity score is its best section. The final score is `0.9 * step1 + 0.1 * step2`. |
| 3 Section selection | `test/step3_secaugmented_gen.py` | `bge-reranker-v2-m3` scores the question against every section of the top-1 entity. This is fused with the step-2 section score using weight `beta`, and the best section goes to the generator (LLaVA-1.5 or an LLM). |

**Takeaways:**
- **Step 1 is image against text summary**, not image against image. The text summary of an entity is the bridge.
- **The step-2 weight on the reranker is only 0.1.** Step 1 dominates.
- **Evidence is a section of the top-1 entity only.** If step 2 picks the wrong entity, the evidence is wrong too.

### KGMEL (Kim et al., SIGIR 2025)

| Step | File | What happens |
|---|---|---|
| 1 Triple generation | `module/generate.py` | A VLM (GPT-4o-mini or LLaVA-NeXT) is given the image and sentence. It writes the entity type, a description, then triples. Relations must come from a fixed list of 20 Wikidata relations (instance of, part of, has characteristic, …). |
| 2 Retrieval | `module/retrieve.py`, `utils/encoder.py` | Text, images and triples are encoded with CLIP ViT-B/32. Triples are pooled by attention, then text, image and triple vectors are combined by learned gates. The model is trained contrastively on the train split, and the top-k candidates are returned. |
| 3a Triple filtering | `utils/triple_filtering.py` | For each candidate, KGMEL keeps only the triples whose relation and tail are among the most similar (by embedding) to the relations and tails the VLM wrote for the mention. |
| 3b LLM rerank | `module/rerank.py` | A prompt lists the candidates with their filtered triples, plus the mention's generated triples. The LLM names the single best entity. |

**Takeaways:**
- **The VLM vocabulary is closed on relations but open on tails.** Matching is done by embedding similarity, not by identifier.
- **Reranking is an LLM choice of one entity**, not a score, so it yields a top-1 only.

## 2. Mapping to Rice MMKG

| Our step (plan, section 4) | Take from | Adaptation |
|---|---|---|
| 1 Coarse entity retrieval | OMGM step 1 | We have 19 conditions, not 100k entities, so recall@20 is trivially 1. **Step 1 must be judged by R@1 and MRR**, and passes its top 5 as soft scores, not a hard cut. We also have many train images per condition (OMGM has one Wikipedia image), so image-to-image kNN is available and is the strong baseline. |
| 2 KG re-ranking | KGMEL steps 1 and 3 | The relation list is replaced by our closed vocabulary: `indicatedBy` (symptom), `affectsPlantPart`, `occursIn` (growth stage), `increaseRiskOf` (field context). The VLM is local Qwen2.5-VL-7B, not GPT-4o-mini. Tails are linked to our symptom and part IRIs by label or embedding. Each candidate has only 3–7 symptoms, so KGMEL's triple filtering is not needed. The **score** is symptom and part overlap plus context match, fused with step 1 as in OMGM. If checkpoint 1 fails, we fall back to KGMEL's LLM rerank (plan, section 6). |
| 3 Evidence | OMGM step 3 | OMGM uses the same reranker (`bge-reranker-v2-m3`) over *all* sections of the top-1 entity. We route through provenance: matched facts → `hasEvidencePassage` → passages. **OMGM-style evidence on our data** (all passages of the top condition's fact sheet) is the direct ablation of the provenance route. |
| Reranker training | OMGM step 2a; Wen et al. 2024 | There are no (image, question) → section pairs yet. Distant supervision from train images and provenance passages is possible once question templates exist (week 3). |

## 3. Decisions

1. **OMGM and KGMEL as baselines: reimplement the core step on our data and say so.** Their released weights are trained on Wikipedia entities (E-VQA, WikiMEL) and their pipelines expect Wikipedia knowledge-base formats. Running them unchanged would measure domain shift, not the method. This follows the risk row "Adapting OMGM or KGMEL takes too long" in the plan.
   - **OMGM baseline:** CLIP image → entity summary (step 1), then `bge-reranker-v2-m3` over all passages of the top entity (step 3). The Q-Former reranker is left out, and this is stated as a limitation.
   - **KGMEL baseline:** VLM triples with an open vocabulary, then LLM rerank of the top 5 conditions.
2. **Encoders:** CLIP ViT-L/14, the OMGM `clip` option. EVA-CLIP-8B does not fit next to a 7B VLM on 24 GB; it can be checked once, alone.
3. **The stage-1 query is the image only.** Questions are added in week 3 and then enter step 2 and step 3, as in OMGM.

## 4. Stage-1 results (split v2, gold v1)

**Setup:**
- **Query:** the image only.
- **Candidates:** all 17 gold targets (section 5).
- **Encoder:** CLIP ViT-L/14.
- **Full tables:** [`results/stage1_results.md`](results/stage1_results.md).

**Two protocols:**
- **In-source:** the test split. The headline "main" subset leaves out the queries of the two single-source datasets, Netrokona and YUKE-WBC. Their images stay in the gallery and their targets stay candidates.
- **Cross-source:** leave one dataset out. The gallery and the probe use the train split of all *other* datasets. Queries are the held-out dataset's images, for targets that another dataset also has.

**In-source, main subset (2,883 test images; chance R@1 is 0.059):**

| System | R@1 | macro R@1 | MRR |
|---|---:|---:|---:|
| CLIP zero-shot, label prompt | 0.108 | 0.085 | 0.251 |
| CLIP zero-shot, label + KG symptom prompts | 0.035 | 0.043 | 0.208 |
| Image kNN over train (mean of top 5) | 0.473 | 0.466 | 0.636 |
| Linear probe on train (supervised reference) | 0.506 | 0.424 | 0.665 |

**Cross-source, leave one dataset out (pooled 14,093 queries):**

| System | R@1 | macro R@1 | R@3 | MRR |
|---|---:|---:|---:|---:|
| CLIP zero-shot, label prompt | 0.168 | 0.182 | 0.331 | 0.311 |
| CLIP zero-shot, label + KG symptom prompts | 0.056 | 0.065 | 0.252 | 0.232 |
| Image kNN | 0.366 | 0.287 | 0.593 | 0.534 |
| Linear probe | 0.400 | 0.306 | 0.609 | 0.546 |

**Per held-out dataset (R@1):**

| Held out | n | Targets | Label | KG prompts | kNN | Probe |
|---|---:|---|---:|---:|---:|---:|
| Dhan-Shomadhan | 606 | blast, brown spot, tungro | 0.094 | **0.157** | 0.089 | 0.116 |
| Netrokona | 500 | potassium | 0.000 | 0.000 | 0.000 | 0.002 |
| Nutrient Kaggle | 383 | potassium | 0.000 | 0.000 | 0.632 | 0.671 |
| Paddy Doctor | 10,508 | blast, brown spot, tungro, normal, stem borer | 0.219 | 0.065 | 0.411 | 0.432 |
| Stem Borer BD | 2,096 | normal, stem borer | 0.005 | 0.007 | 0.264 | 0.372 |

**Reading:**
1. **Split v1 leaked.** On v1, image kNN reached R@1 0.917, because burst photos sat in train and test. On v2 the main subset gives 0.473. Every number reported from now on uses split v2.
2. **Image memory is tied to the source.** The source dataset is predicted from the image with 0.993 accuracy (linear probe on CLIP features).
   - **Single-source datasets:** Netrokona scores R@1 1.000 in-source and 0.000 cross-source, so in-source it is solved by recognising the camera and background, not potassium deficiency. YUKE-WBC (brown planthopper, 66 images) has no second source and cannot be tested fairly. Both are reported but are not evidence.
   - **Gallery composition decides the answer:** with a Paddy Doctor-only gallery, kNN on Dhan-Shomadhan reaches 0.479. With all other datasets in the gallery it drops to 0.089, because Dhan's white-background leaf photos match the white-background nutrient datasets.
3. **Generic CLIP text does not know rice symptoms.** In-source, the KG symptom prompts lower zero-shot R@1, because blast and brown spot share "brown lesion", "leaf spot" and "wilting". Symptom matching belongs in step 2 (VLM, closed vocabulary), not in the CLIP text space.
4. **The one place KG text already leads is the hardest held-out set.** On Dhan-Shomadhan cross-source, KG prompts give R@1 0.157, the best of the four systems. Earlier, with a Paddy Doctor-only gallery, they raised R@3 from 0.201 to 0.474. This is the first sign that graph knowledge transfers where image memory does not.
5. **There is headroom for step 2.** Cross-source, the best image system has R@3 0.609 but R@1 0.400. Re-ranking a short list with symptoms and context is exactly step 2's job.
6. **Confusions to target (main):** Hispa ↔ Normal, Normal → Leaf folder, Blast ↔ Tungro, Downy mildew → Hispa.

**Implications for the paper:**
- **Headline:** report the main in-source subset *and* cross-source, with macro R@1 beside per-image R@1. Paddy Doctor is 82% of the test images.
- **Checkpoint 1 (15 Nov):** step 2 must raise cross-source R@1, not only in-source R@1.
- **Data gap:** a second brown planthopper image source is needed. IP102 is the first candidate to check.

## 5. Gold answer (gold v1, 2026-10-27)

`scripts/make_gold.py` writes [`splits/gold.csv`](splits/gold.csv).

1. **The gold is the cause to manage**, whether pest, pathogen disease or nutrient disorder, and not the symptom. In IPM the action follows the cause.
2. **All stem borer damage photos have gold `Stem_Borer`, as a group** (2,769 images remapped).
   - **Paddy Doctor:** names its folders by species (`yellow_`, `white_`, `black_stem_borer`). Version 1 mapped yellow to `Stem_Borer` and white and black to `Deadheart`, but all three folders show damage, mostly whiteheads.
   - **Species:** it cannot be told from the damage, and the management is the same.
3. **`Deadheart` and `White_Ear` are symptoms, not targets.** They are kept per image only where the source labels the symptom (Stem Borer BD: 439 deadheart, 551 white head). They serve as ground truth for the step-2 symptom check.
4. **Metrics:**
   - **Primary:** strict R@k and MRR against the gold.
   - **Graded nDCG@5:** relevance 2 for the gold, 1 for a target linked to it by `causes`. Among the 17 targets no such link exists today, so nDCG@5 currently adds nothing over strict ranking. It will matter for evidence passages.
5. **Pending expert confirmation:** `annotatedAs` in the ontology is unchanged. Two questions go to the expert: whether stem borers are one group, and whether Deadheart stays a Disease individual.

## 6. Stage 2: from photo and question to passages (first scores, 2026-10-27)

`scripts/stage2_passages.py` gives [`results/stage2_results.md`](results/stage2_results.md).

**Setup:**
- **Query:** a test image of the main subset plus a question of one of three intents:
  - cause: "What causes this problem on my rice?"
  - manage: "How can I control or prevent it?" (IRRI puts control and prevention in one section)
  - identify: "Which symptoms confirm it?"
- **Index:** the 296 IRRI passages, embedded with bge-m3 (local Ollama).

**Gold:**
- **Section gold (main):** the passages of the target's own IRRI fact sheet, in the section that answers the intent. The target → fact sheet map is written by hand, not taken from the graph. It is silver: no person has judged the passages yet.
- **Fact gold (strict):** the passages linked by `hasEvidencePassage` to the target's facts of that intent. It favours the KG route by construction, so it is reported for coverage only.

**Coverage (facts / facts with a linked sentence / section passages):**
- **Fact sheets:** 13 of 17 targets have an IRRI sheet. Bacterial panicle blight, downy mildew, leaf scald and normal have none.
- **Linked sentences:** they exist almost only for symptoms. For cause, 3 targets have one; for manage, only the three nutrient disorders.
- **Missing sections:** the nutrient sheets have no "identify" or "cause" section, and the leaffolder sheet has no "manage" section.
- **The gaps show which texts to add next:** CABI or other open sources for cause and control, and fact sheets for the four uncovered targets.

**Stage 1 on the main subset:** linear probe R@1 0.506. Fusing the KG symptom prompts does not help in-source; the weight tuned on dev is 0, so the "kg" stage 1 equals the probe. A real KG stage 1 needs step 2 (VLM symptoms) or graph embeddings (IKRL), not CLIP text prompts.

**Stage 2, section gold (MRR):**

| Stage 1 → stage 2 | cause | manage | identify |
|---|---:|---:|---:|
| probe → bge-m3 over all passages (no KG) | 0.479 | 0.316 | 0.416 |
| probe → KG route (facts → linked passages → cited documents) | 0.487 | 0.333 | 0.478 |
| gold condition → bge-m3 | 0.721 | 0.685 | 0.533 |
| gold condition → KG route | 0.731 | 0.706 | 0.757 |

**Reading:**
1. **Stage 1 is the bottleneck.** With the gold condition, MRR rises by 0.25 to 0.37 for every intent. A wrong condition sends the search to the wrong fact sheet.
2. **The KG route helps most where the graph has linked sentences.** That is "identify": MRR 0.533 → 0.757 with the gold condition, and 0.416 → 0.478 with the probe. For cause and manage the gain is small, because few cause or control facts have a linked sentence yet. The route then falls back to the documents their facts cite.
3. **Fact gold is not evidence.** With the gold condition the KG route scores 1.000 on it by construction. It is reported only to show coverage.
4. **Next:**
   - link cause and control facts to sentences, adding sources beyond IRRI;
   - add question text to stage 1 (week 3);
   - pool the top passages of both systems for human judging, which replaces the silver section gold.

## 7. Stage 2 with OMGM step 3 and top-k propagation (2026-10-28)

**What was added to `scripts/stage2_passages.py`:**
- **Reranker (OMGM step 3):** bge-reranker-v2-m3, a cross-encoder, re-orders the top 50 passages. The query is "<condition label>: <question>".
  - **Without the KG:** it re-orders the bge-m3 top 50.
  - **On the KG route:** it re-orders within each KG tier, so passages the graph links stay first.
  - **First attempt:** re-ordering the KG top 50 freely erased the graph's advantage; "identify" with the gold condition fell from 0.757 to 0.554.
- **Top-k propagation:** the stage-1 top-1 is not trusted. The top K conditions each bring their pool, and a passage scores max over conditions e of log p(e | image) + beta · (rerank + gamma · tier bonus). K, beta and gamma are tuned on dev (section gold, mean MRR over intents):
  - **No KG:** K = 5, beta = 0.2.
  - **KG:** K = 2, beta = 0.1, gamma = 1.

**Section gold, MRR on the main test subset:**

| Stage 1 → stage 2 | cause | manage | identify |
|---|---:|---:|---:|
| probe top-1 → bge-m3 (no KG) | 0.479 | 0.316 | 0.416 |
| probe top-1 → KG route | 0.487 | 0.333 | **0.478** |
| probe top-1 → bge-m3 + rerank | 0.518 | 0.321 | 0.301 |
| probe top-1 → KG route + rerank in tiers | 0.529 | 0.332 | 0.340 |
| probe top-k → bge-m3 + rerank | 0.533 | 0.376 | 0.310 |
| probe top-k → KG route + rerank in tiers | **0.536** | **0.389** | 0.326 |
| gold condition → bge-m3 | 0.721 | 0.685 | 0.533 |
| gold condition → KG route | 0.731 | 0.706 | **0.757** |
| gold condition → bge-m3 + rerank | 0.874 | 0.713 | 0.554 |
| gold condition → KG route + rerank in tiers | **0.889** | **0.726** | 0.745 |

**Reading:**
1. **The reranker helps cause and manage.**
   - **With the gold condition:** cause rises from 0.731 to 0.889.
   - **With the probe:** cause rises from 0.487 to 0.536, and manage from 0.333 to 0.389 once top-k propagation is added.
   - **Best on these two intents:** "KG route + rerank in tiers" is the best system with either stage 1.
2. **Top-k propagation mainly helps manage** (+0.06 over top-1 + rerank). Spreading over K conditions recovers some stage-1 errors.
3. **The reranker hurts "identify" with the probe**: 0.478 → 0.326 on the KG route. Part of this is the silver gold. With the gold condition, the reranker's top-1 for identify falls on 13 targets as follows:
   - **Gold:** 4 targets.
   - **Symptom descriptions under "What it does":** 4 targets (bacterial blight, bacterial leaf streak, planthopper, tungro). They answer the question, but the section gold only accepts "How to identify".
   - **Symptom lists under "How to manage":** the 3 nutrient disorders. These are outside the identify evaluation, which has no gold section for them.
   - **Real errors:** 2 targets. Blast goes to a rice bug passage and stem borer to a sheath blight passage. Both passages say "can be confused with ⟨the queried condition⟩", and the cross-encoder matches the name.
   - **With the probe's wrong conditions:** the reranker follows the wrong label more strictly than bge-m3 does, so it loses the near-misses that dense search still ranks high.
4. **Fact gold** is still circular; the KG rows keep 1.000 with the gold condition and are not evidence.

**Next:**
- **Judged gold for "identify":** pool the top passages of all systems and judge them, so that symptom passages outside "How to identify" count.
- **Per-intent stage 2:** use the KG route without the reranker for "identify" until the gold is judged.
- **Stage 1 stays the bottleneck:** about 0.35 MRR separates the probe from the gold condition. The VLM step 2 (week 4) targets this.
