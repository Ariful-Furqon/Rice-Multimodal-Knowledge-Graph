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
| CLIP zero-shot, label + KG symptom prompts | 0.128 | 0.076 | 0.289 |
| Image kNN over train (mean of top 5) | 0.473 | 0.466 | 0.636 |
| Linear probe on train (supervised reference) | 0.506 | 0.424 | 0.665 |

**Cross-source, leave one dataset out (pooled 14,093 queries):**

| System | R@1 | macro R@1 | R@3 | MRR |
|---|---:|---:|---:|---:|
| CLIP zero-shot, label prompt | 0.168 | 0.182 | 0.331 | 0.311 |
| CLIP zero-shot, label + KG symptom prompts | 0.165 | 0.136 | 0.381 | 0.333 |
| Image kNN | 0.366 | 0.287 | 0.593 | 0.534 |
| Linear probe | 0.400 | 0.306 | 0.609 | 0.546 |

**Per held-out dataset (R@1):**

| Held out | n | Targets | Label | KG prompts | kNN | Probe |
|---|---:|---|---:|---:|---:|---:|
| Dhan-Shomadhan | 606 | blast, brown spot, tungro | 0.094 | **0.157** | 0.089 | 0.116 |
| Netrokona | 500 | potassium | 0.000 | 0.000 | 0.000 | 0.002 |
| Nutrient Kaggle | 383 | potassium | 0.000 | 0.000 | 0.632 | 0.671 |
| Paddy Doctor | 10,508 | blast, brown spot, tungro, normal, stem borer | 0.219 | 0.205 | 0.411 | 0.432 |
| Stem Borer BD | 2,096 | normal, stem borer | 0.005 | 0.034 | 0.264 | 0.372 |

*KG-prompt rows re-measured 2026-10-28, after `Deadheart` became a symptom of `Stem_Borer` and stem borer gained the symptoms deadheart and reduced tillering. Before: in-source 0.035 / 0.043 / 0.208, cross-source 0.056 / 0.065 / 0.252 / 0.232, Paddy Doctor 0.065, Stem Borer BD 0.007. The other systems do not read the graph and did not change.*

**Reading:**
1. **Split v1 leaked.** On v1, image kNN reached R@1 0.917, because burst photos sat in train and test. On v2 the main subset gives 0.473. Every number reported from now on uses split v2.
2. **Image memory is tied to the source.** The source dataset is predicted from the image with 0.993 accuracy (linear probe on CLIP features).
   - **Single-source datasets:** Netrokona scores R@1 1.000 in-source and 0.000 cross-source, so in-source it is solved by recognising the camera and background, not potassium deficiency. YUKE-WBC (brown planthopper, 66 images) has no second source and cannot be tested fairly. Both are reported but are not evidence.
   - **Gallery composition decides the answer:** with a Paddy Doctor-only gallery, kNN on Dhan-Shomadhan reaches 0.479. With all other datasets in the gallery it drops to 0.089, because Dhan's white-background leaf photos match the white-background nutrient datasets.
3. **Generic CLIP text does not know rice symptoms well.** Blast and brown spot share "brown lesion", "leaf spot" and "wilting", so symptom prompts blur them.
   - **Before the deadheart fix:** the KG symptom prompts lowered zero-shot R@1.
   - **After it:** stem borer, the largest target, has the right symptoms. In-source R@1 rises above the label prompt (0.128 vs 0.108), though macro R@1 stays lower (0.076 vs 0.085). Cross-source, the two are level (0.165 vs 0.168), and R@3 is higher with the KG (0.381 vs 0.331).
   - **The prompts are only as good as the graph's symptom lists.** Correcting one modelling error moved them more than any prompt change.
   - **Symptom matching still belongs in step 2** (VLM, closed vocabulary), not in the CLIP text space.
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
5. **Expert confirmation:**
   - **Deadheart (answered 2026-10-28):** a domain expert said deadheart (*sundep*) is a symptom of stem borer, not a disease. The ontology now types `Deadheart` as `Symptom` ([`Analysis and Alignment/Expert_Input_2026-10-28_Deadheart.md`](../Analysis%20and%20Alignment/Expert_Input_2026-10-28_Deadheart.md)), which matches gold v1. `annotatedAs` is unchanged.
   - **Still open:** whether the stem borer labels form one group.

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

## 8. Step 2: VLM triples and first scores (2026-11-01)

`scripts/step2_vlm_triples.py` and `scripts/step2_rerank.py` give [`results/step2_results.md`](results/step2_results.md).

**Setup:**
- **VLM:** Qwen2.5-VL-7B through Ollama, 3 to 4 seconds per photo.
- **Images:** 740 in all. `test_core` (370) reports, and `splits/dev_core.csv` (370, same rule as `test_core`) tunes the fusion. On the main subset, 345 test images are in-source and 195 are cross-source.
- **Closed vocabulary (ours):** the VLM picks from the 43 symptom labels and 10 plant parts. No condition name is in the prompt.
- **Score:** matched symptoms weighted by confidence and idf, with a penalty if the KG does not link the symptom to the reported part. It is fused with stage 1 over the top 5, and lambda is tuned on dev.
- **KGMEL baseline:** open-vocabulary triples, then Qwen2.5:7b names one of the top 5 from the KG symptoms.

**Prompt change, made on dev:** prompt v1 had a `healthy` field and 76% of the first 412 photos took it, sick ones too. It was stopped and replaced by v2, which asks for the marks first. On a sample of 46 dev images, photos of sick plants with no triples fell to 2 of 42, and all 4 healthy photos stayed empty. The partial v1 run printed test scores, which were not used to choose the prompt. The v2 test scores were computed once.

**Results, `test_core` main subset:**

| Protocol | System | n | R@1 | macro R@1 | MRR | p (MRR, vs stage 1) |
|---|---|---:|---:|---:|---:|---:|
| In-source | Stage 1 (probe) | 345 | 0.513 | 0.435 | 0.667 | |
| In-source | Stage 1 + KG triples (lambda 0.2) | 345 | 0.528 | 0.453 | 0.677 | 0.164 |
| In-source | KGMEL baseline | 345 | 0.258 | 0.212 | 0.531 | < 0.001 (worse) |
| Cross-source | Stage 1 (probe) | 195 | 0.354 | 0.331 | 0.512 | |
| Cross-source | Stage 1 + KG triples (lambda 0) | 195 | 0.354 | 0.331 | 0.512 | 1.000 |
| Cross-source | KGMEL baseline | 195 | 0.246 | 0.244 | 0.471 | 0.088 (worse) |

**Reading:**
1. **Checkpoint 1 is not met yet.** In-source the gain is +0.015 R@1 and not significant. Cross-source, dev chose lambda 0, so step 2 is switched off and the row equals stage 1. The in-source lambda is also fragile: only 0.2 beats 0 on dev (0.548 vs 0.536), and larger weights fall below it.
2. **The bottleneck is the VLM's symptoms, not the fusion.** On 345 dev photos:
   - Only 24% of the photos of sick plants have a triple that matches a symptom of their gold condition.
   - Six conditions score 0%: bacterial leaf blight, leaf folder, leaf scald, nitrogen deficiency, phosphorus deficiency and sheath blight.
   - One label dominates: "yellow stripe" appears on 131 of 345 photos.
   - On stem borer photos whose source labels the symptom, the VLM reports deadheart on 0 of 15 and white ear on 1 of 15.
   - 25 of 30 healthy photos correctly get no triples.
3. **The KGMEL baseline is worse overall and over-picks.** It discards the stage-1 ranking: it moves the answer away from stage 1's top 1 on 215 of 345 images, and picks Normal_Health 87 times against 30 gold photos.
4. **Its gain on blast / brown spot is only partly real.** R@1 on those photos rises from 0.250 to 0.367 in-source and 0.017 to 0.183 cross-source, but it picks blast 63 times against 30 gold photos, so part of this is bias towards the two classes. Of the 60 in-source photos, 22 are correct, 14 go to the other member of the pair and 24 go outside it.

5. **On leaf photos the KG cannot separate blast from brown spot.** Both list `Brown Lesion`, `Leaf Spot` and `Wilting`, and their other symptoms are on the panicle, neck, node or grain. So on a leaf photo they get the same KG score, however good the VLM is. The feature that farmers use, lesion shape, is not in the graph.

**Next, all tuned on dev:**
- **Better symptoms before better fusion:** few-shot prompts with reference photos, or per-symptom yes/no questions, and normalising near-labels ("brown lesions" against "Brown Lesion"; 86% of triples are in vocabulary).
- **Keep stage 1 in the LLM rerank:** give the LLM the stage-1 confidence, or let it act only when stage 1 is unsure.
- **Add discriminative symptoms to the KG:** tried on dev, see below. Not done.
- **Add the question:** the farmer's words are the cheapest symptom source, and they are not in stage 1 yet.

**Dev checks after the first scores (2026-11-01, dev_core main, no test data):**
- **Ceiling:** the gold is in the stage-1 top 3 on 0.771 of photos in-source and 0.595 cross-source, so a rerank has room. Blast and brown spot make 13 of 160 in-source errors.
- **Yes/no list over the top 3,** with two trial symptoms from the IRRI blast and brown spot sheets (spindle or diamond lesion; circular to oval lesion). One VLM call per photo, weights tuned by two-fold cross-fitting. The tuned weight was 0 in every fold, with and without the trial symptoms: R@1 stays 0.536 in-source and 0.354 cross-source. The VLM said yes to 6.9% of items.
- **Direct lesion-shape question** on the 60 blast and brown spot photos: blast spindle 22, none 8; brown spot spindle 21, none 9, round 0.

**Decision:** the KG stays unchanged. The gap is real, but this VLM cannot read the shape at 768 px, so adding the symptoms would change nothing. Crops and reference photos were then tested and failed too (below). Scripts are in `scripts/dev_checks/`, answers in `results/verify_dev.jsonl`.

**Next steps run on dev (2026-11-01, dev_core main, no test data):**
- **Lesion shape with crops or reference photos,** stop rule set before the run: balanced accuracy of at least 0.7, against 0.367 for the whole photo. Crops 0.500 (spindle on all 30 blast and 26 of 30 brown spot photos), reference photos 0.567 (round on 14 of 30 brown spot and 7 of 30 blast photos). Both fail, so this route stops. The four reference photos were drawn at random from train, so better ones might do a little more.
- **LLM rerank that keeps stage 1** (top 3, shown the stage-1 confidence, used only below a margin): the cross-fitted threshold is 0 in both protocols, so nothing changes. `results/step2_llm_gate_dev.md`.
- **Question layer:** `make_questions.py` writes five templates tied to Tier A CQs. They name no symptom, so they carry no entity information.
- **Farmer's words, simulated:** an observation in plain words is drawn from the gold condition's KG symptoms, with noise, and matched to KG symptom labels with bge-m3. In-source R@1 0.536 to 0.652 / 0.591 / 0.565 at noise 0 / 0.3 / 0.5; cross-source 0.354 to 0.405 / 0.374 / 0.390, and only noise 0 is clearly above stage 1 there. Blast and brown spot do not gain (in-source 0.217 to 0.217 at noise 0.3). `results/step1_question_dev.md`. **This is circular by construction, so it is a sensitivity analysis and not a result.**
- **20 test cases:** `splits/test_cases_draft.csv`, outside test_core, chosen without looking at the photos. The observation column is empty: a person must write it from the photo.
- **Final evaluation:** 2,538 main test photos outside test_core have not been used by step 2.

- **Field context:** plant age is the only context on the photos, on Paddy Doctor only (180 of 345). Age bands fixed before the run map to growth stages, then to candidates through `occursIn`. In-source 0.406 unchanged (lambda 0); cross-source 0.433 to 0.467 on 90 photos, p 0.324. Dev ages run only from 45 to 75 days, so age separates few candidates. `results/step2_field_context_dev.md`.
- **Larger VLM (`qwen2.5vl:32b`)** on the same 60 photos, same stop rule: whole photo 0.400, reference photos 0.333. It fails, and does no better than the 7B model. Crops were skipped.

- **Three more open-weight VLMs (2026-11-03),** same 60 photos, prompt, reference photos and stop rule (`scripts/dev_checks/shape_model.py`; newer models are asked not to reason first, and the JSON is cut out of the reply because one model appends an end token). Balanced accuracy, whole photo / with reference photos: `gemma4:31b` 0.417 / 0.433; `muse-glimmer:30b` 0.250 / 0.300; `qwen3.8:27b` 0.400 / 0.333. All fail. Every model answers spindle on most brown spot photos. With `qwen2.5vl` 7B and 32B, five models from three vendors fail, the best at 0.567. Images were 768 px on the long side for all of them.

**Checkpoint 1 is still not met.** Nothing has raised R@1 significantly with real data. Not tried: a stronger stage-1 encoder, which would not be a KG contribution.

## 9. λ re-check, IKRL on split v2, and the link-prediction design (2026-11-06)

All on dev, no test data.

### 9.1 λ tuning (step 2)

`scripts/dev_checks/lambda_dev.py`, dev_core main. Finer grid (0 plus 40 log-spaced values, 0.01–10), R@1 and MRR as criteria, 2,000 bootstrap resamples.
- **In-source (345):** both criteria choose λ ≈ 0.2, as the 8-value grid did. Dev MRR 0.682 → 0.690. λ = 0.2 beats λ = 0 in 88% of resamples, below 95%. Above about 0.35 the scores fall steeply.
- **Cross-source (195):** flat. R@1 chooses 0. MRR chooses λ ≈ 4 for +0.002, which wins in 52% of resamples. The bootstrap choices range from 0.01 to 3.5.
- **Decision:** `step2_rerank.py` is unchanged. MRR argmax would switch on noise cross-source. The dev curve goes into the paper as a sensitivity figure. The failure of step 2 lies in the symptoms (section 8), not the weight.

### 9.2 IKRL on split v2

`scripts/dev_checks/ikrl_v2_dev.py` → `results/ikrl_v2_dev.md`.

**Why it was re-run.** The August run (`Multimodal Fusion PoC/ikrl_vs_cnn.py`: 71.1% vs 62.6%) had two flaws:
- it used a random split of Paddy Doctor, which leaks burst photos (the split v1 problem, section 4);
- the IKRL head had an extra MLP that the linear baseline lacked, so capacity was not controlled.

**Setup:**
- Split v2, CLIP ViT-L/14 features, 17 conditions, gold from `gold.csv`.
- Early stopping on 10% of the train capture groups. Dev main subset, 5 seeds.
- Three heads on the same features:
  - **A:** linear;
  - **B:** linear + gate · −‖g(x) − e_c‖, with e_c from TransE on the 345 domain triples;
  - **C:** the same as B, with random frozen class vectors.
- The KG effect is B − C.

| Protocol | n | A R@1 | B R@1 | C R@1 | A MRR | B MRR | C MRR |
|---|---:|---:|---:|---:|---:|---:|---:|
| In-source | 2,882 | 0.605 | 0.612 | 0.612 | 0.724 | 0.730 | 0.729 |
| Cross-source | 1,890 | 0.419 | 0.418 | 0.421 | 0.576 | 0.571 | 0.570 |

**Reading:**
1. **The KG effect is zero.** B − C MRR is +0.0005 in-source (4 of 5 seeds above zero) and +0.0004 ± 0.017 cross-source (2 of 5). TransE class vectors do no better than random ones.
2. **The small in-source gain over A is capacity, not the KG.** C − A is +0.005 MRR in 5 of 5 seeds. The gate is about 0.85 in both B and C, so the distance term acts as extra learned prototypes.
3. **The August 71.1% vs 62.6% should not be cited.** It mixes a leaky split, uncontrolled capacity and weak ResNet features.
4. **Why the KG has no effect:** the domain triples reach a photo only through its class, and there is no edge from a photo to a symptom. The KG adds no information that the pixels do not already give. This is the same bottleneck as step 2.

### 9.3 Link prediction with photo edges (run 2026-11-06)

The supervisor's idea: keep the photo node, cut `annotatedAs`, and predict it from the pixels and the photo's other edges.

**Edges of the photo nodes** (query-time graph, sample of 3,000 photos):

| Edge | Coverage | Treatment |
|---|---:|---|
| `rdfs:label`, `schema:contentUrl`, `sourceLabel` | ~100% | **Leaking:** the folder name and label are in the string |
| `captures` | ~12% | Leaking |
| `prov:wasDerivedFrom` (dataset) | 100% | Dataset prior; tested separately |
| `plantAgeDays` | ~76% | Field context, mostly Paddy Doctor; tested separately |
| `ofVariety` | ~19% | Field context; tested separately |
| `recordedAtDate`, `hasSpatialLocation`, `environmentCondition`, `hasBandImage` | 5–14% | Safe |

**Variants:**
- Head C from 9.2 (B is no better), with the edge features concatenated to the standardised CLIP features.
- A missing edge is a zero plus an indicator.
- Same split, early stopping, 5 seeds, in-source and cross-source, dev main subset.

| Variant | Added input | Question |
|---|---|---|
| 1 | None (pixels only) | Baseline; should match 9.2 C |
| 2 | Safe edges | Does photo context help? |
| 3 | 2 + plant age (bands as in `step2_field_context.py`) + variety | Field context |
| 4 | 2 + dataset one-hot | How large is the dataset shortcut? |
| 5 | 2 + leaking edges (`sourceLabel` token, label and path tokens, `captures`) | **How much does leakage inflate a KG-augmented result?** |

**Expected:**
- Variants 2 and 3: little or no gain. The safe edges are sparse, and the dev ages run only from 45 to 75 days (section 8).
- Variant 4: a gain in-source. It is not defined cross-source, where the query's dataset is never seen in training.
- Variant 5: close to 1.0. It is reported as the leakage table of the analysis (SIGIR plan, section 2, claim 3).
- Any gain in variants 4 and 5 is a dataset prior or leakage, not domain knowledge.

**Run (2026-11-06, CPU):** `scripts/dev_checks/link_pred_dev.py` → `results/link_pred_dev.md`. Edges come from `Ontology/Rice MMKG.rdf`, because the query-time graph has none for dev photos. Dev main subset, 5 seeds; Δ MRR is against variant 1. Plant age enters as its growth-stage band (the `BANDS` of `step2_field_context.py`). A first run with one-hot raw days gave the same picture (variant 3: −0.018 MRR); the numbers below are the re-run with bands, which reproduces variants 1, 2, 4 and 5 of the first run to within 0.002 MRR.

Two additions to the design:
- **3b:** variant 3 trained without early stopping, for exactly the epochs at which variant 1 stopped (same seed and fold). It separates the effect of the inputs from that of the stopping point.
- **Lookup baseline:** no model, folder name in `contentUrl` → majority train gold.

| Variant | In-source R@1 | Δ MRR | Seeds > 0 | Stop epoch | Cross-source R@1 | Δ MRR | Seeds > 0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 Pixels | 0.612 | | | 341 | 0.421 | | |
| 2 Safe edges | 0.609 | −0.002 | 2/5 | 303 | 0.427 | +0.005 | 2/5 |
| 3 + age, variety | 0.594 | −0.011 | 0/5 | 131 | 0.417 | +0.001 | 3/5 |
| 3b = 3, epochs of 1 | 0.613 | −0.001 | 2/5 | 341 | 0.411 | −0.005 | 2/5 |
| 4 + dataset | 0.608 | −0.002 | 1/5 | 286 | n/a | | |
| 5 + leaking edges | 0.798 | +0.141 | 5/5 | 399 | 0.422 | +0.005 | 3/5 |
| Lookup, folder name | 1.000 | | | | 0.000 | | |

Variant 4 is not run cross-source: the held-out dataset's one-hot column is never set in training, so it would equal variant 2.

**Reading:**
1. **No photo edge helps.** In-source, variants 2–4 are at or below pixels only. Cross-source, the gains are below 0.01 MRR and not consistent across seeds.
2. **The "safe" edges are dataset markers.**
   - Each one occurs in one or two datasets only: date and location in Kaggle and YUKE-WBC, background in Dhan-Shomadhan, age and variety in Paddy Doctor.
   - Its presence alone tells the dataset, which the pixels already give (0.993, section 4).
3. **Age and variety cost accuracy only through early stopping.**
   - Variant 3 is lower in-source (−0.011 MRR, 0 of 5 seeds), and the loss falls mostly on the datasets that have *no* age or variety edge: Dhan-Shomadhan 0.692 → 0.643, Kaggle 0.927 → 0.882, Stem Borer BD 0.983 → 0.952, against Paddy Doctor 0.530 → 0.517. Their input is unchanged, so the cause is the training, not the features.
   - With these inputs, validation accuracy peaks early (epoch 131 on average, against 341 for pixels), and the kept model is under-trained for every dataset.
   - Trained for variant 1's epochs (3b), the loss disappears (−0.001 MRR, 0.613 R@1, every dataset back at its pixels-only level). Age and variety are neutral, not harmful, and they add nothing.
   - A likely reason for the early peak: the Paddy Doctor capture groups are defined by (label, variety, age), so in train these values identify a session and with it the label. The head fits that shortcut first, and it does not carry over to the validation groups.
4. **Leakage is large in-source.**
   - With the leaking edges the head reaches 0.798 R@1 (+0.14 MRR).
   - This underestimates the leak: the lookup from the folder name in `contentUrl` to the majority train gold gives **R@1 1.000** on all 2,882 dev photos (computed in the same script). The head does not fully use the one-hot features next to 768 CLIP dimensions.
   - Every dataset except Dhan-Shomadhan has `sourceLabel`, and it maps one-to-one to the gold.
5. **Cross-source the leak does not transfer.** The label strings differ between datasets ("blast" vs "Rice_Blast"), so an unseen dataset's strings mean nothing to the model: no held-out folder occurs in training, and the lookup scores 0.000. A cross-source result therefore cannot be inflated in this way. An in-source result can be.
6. **Conclusion for the supervisor's idea:**
   - Link prediction on the photo node gains nothing from the graph once `annotatedAs` and its string copies are cut.
   - The domain triples do not reach the photo (9.2), and the photo's own edges are dataset or session markers.
   - Its value for the paper is the leakage analysis: an in-source KG-augmented model that keeps `sourceLabel` or `contentUrl` can report anything up to 1.0.
7. **Prior work** ([`Related_Work_Leakage_and_Dataset_Bias.md`](../Analysis%20and%20Alignment/Related_Work_Leakage_and_Dataset_Bias.md)):
   - The closest analogue is test leakage through inverse relations in FB15k and WN18 (Dettmers et al. 2018; Akrami et al. 2020).
   - The dataset shortcut matches source detection in chest radiographs (Zech et al. 2018) and capture bias in PlantVillage (Noyan 2022).
   - No reference has been found yet for the early-stopping effect in reading 3.

### 9.4 KG-based generalized zero-shot: first run (2026-11-06, no calibration)

`scripts/dev_checks/zsl_dev.py` → `results/zsl_dev.md`.

**Question:** does the KG help for a condition that has no training photo? For conditions without photos (armyworm, rice bug, Zn deficiency, …), the KG is the only source of knowledge.

**Setup:**
- Leave one condition out: train on the other 16, score all 17 on dev main.
- Model: s(x, c) = (Wx) · φ(c).
- Class representations φ(c):
  - KG multi-hot: domain triples, symptom → plant part, and type; 108 features;
  - the same, shuffled among classes (control);
  - CLIP text of the label;
  - CLIP text of the label plus the KG symptoms.
- Also CLIP zero-shot with no training. Chance MRR over 17 classes is 0.202.

| Method | Unseen R@1 | Unseen R@3 | Unseen MRR | Seen R@1 |
|---|---:|---:|---:|---:|
| CLIP zero-shot, label text | 0.066 | 0.173 | 0.206 | 0.124 |
| CLIP zero-shot, label + KG symptom text | 0.071 | 0.240 | 0.225 | 0.109 |
| Trained, KG multi-hot | 0.000 | 0.066 | 0.156 | 0.597 |
| Trained, KG shuffled (control) | 0.000 | 0.013 | 0.129 | 0.600 |
| Trained, label text | 0.001 | 0.231 | 0.176 | 0.594 |
| Trained, label + KG symptom text | 0.023 | 0.161 | 0.181 | 0.558 |

**Reading:**
1. **The KG structure carries real, if small, signal.**
   - KG multi-hot beats its shuffled control on 12 of 16 conditions (3 losses, 1 tie), with MRR 0.156 vs 0.129.
   - The largest gains are on the nutrient disorders (P 0.237 vs 0.109, K 0.240 vs 0.117), brown spot and downy mildew.
   - This is the first test where the KG beats a matched control; IKRL (9.2) and link prediction (9.3) gave zero.
2. **Without calibration, the trained models never put the unseen class first.** Unseen R@1 is about 0, and MRR is below chance. This is the known seen-class bias of generalized ZSL, so the absolute numbers are not yet meaningful.
3. **In CLIP zero-shot, the KG symptoms help on average, but not everywhere.**
   - MRR rises from 0.206 to 0.225, and R@3 from 0.173 to 0.240.
   - The symptom text wins on 8 of 16 conditions. The gains are on conditions with a distinctive, non-leaf or named symptom:
     - stem borer 0.578 vs 0.080 (deadheart, white ear);
     - downy mildew 0.506 vs 0.146;
     - sheath blight 0.510 vs 0.309;
     - blast 0.358 vs 0.117;
     - leaf scald 0.257 vs 0.126.
   - It loses on brown spot (0.242 vs 0.598) and healthy plants (0.128 vs 0.665). Healthy has no symptom prompt, so it loses ground when the other classes gain prompts.
4. **The KG works better read as text than as a multi-hot vector.** CLIP's language encoder knows what "deadheart" looks like; a one-hot column does not.

**Next:**
- **A calibration-free metric:** the area under the seen–unseen accuracy curve (AUSUC; Chao et al., 2016) over a calibration constant γ, plus the harmonic mean at a γ chosen on held-out *seen* classes only.
- **Run speed:** save the raw scores so calibration needs no retraining, and run on MPS. This run took about 70 minutes on CPU.
- **Hybrid:** a trained model for the seen classes and KG-text prototypes for the unseen ones.

### 9.5 Removing the source dataset from the image features (2026-11-07, negative)

`scripts/dev_checks/debias_dev.py` → `results/debias_dev.md`.

**Question:** the source dataset is decodable from the CLIP features (0.993), and a source that is visible in the pixels can confound the label (Zech et al. 2018; [`Related_Work_Leakage_and_Dataset_Bias.md`](../Analysis%20and%20Alignment/Related_Work_Leakage_and_Dataset_Bias.md), section 3). If the stage-1 image systems lean on the source, does removing it raise cross-source R@1, the checkpoint-1 target?

**Setup:**
- Stage-1 knn_image and linear_probe as in `stage1_baselines.py` (C = 1, k = 5), on transformed and re-normalised CLIP ViT-L/14 features.
- Dev main subset, in-source and cross-source (leave one dataset out). Deterministic.
- Δ MRR against no transform, with a 95% bootstrap interval over capture groups.
- Transforms:
  - **project:** remove the source subspace, i.e. the weight directions of a linear source classifier on the training images, in 3 rounds of nullspace projection;
  - **center:** subtract each source's mean feature. A held-out source uses the mean of all its own dev images, without labels. This is transductive: it needs a batch of unlabelled photos from the new source;
  - **both:** center, then project;
  - **project_cc:** as project, but the source classifier is fitted on features minus their class mean, so only within-class source directions are removed. It was added after `project` failed (reading 2).

| Transform | Source acc. (cross) | knn R@1 | knn Δ MRR [95% CI] | probe R@1 | probe Δ MRR [95% CI] |
|---|---:|---:|---|---:|---|
| none | 0.989 | 0.378 | | 0.394 | |
| project | 0.737 | 0.365 | −0.054 [−0.090, −0.026] | 0.389 | −0.047 [−0.093, +0.005] |
| center | 0.734 | 0.313 | −0.082 [−0.125, −0.045] | 0.346 | −0.064 [−0.093, −0.048] |
| both | 0.733 | 0.317 | −0.080 [−0.121, −0.046] | 0.340 | −0.073 [−0.110, −0.051] |
| project_cc | 0.872 | 0.368 | −0.027 [−0.060, −0.004] | 0.378 | −0.025 [−0.049, +0.006] |

Cross-source, n = 1,890. In-source, no transform helps either (best: probe with center or both, R@1 0.578–0.579 against 0.566, but MRR −0.005 to −0.007 with intervals that include zero).

**Reading:**
1. **Removing the source does not help cross-source.** Every transform lowers MRR, and most intervals exclude zero. The source subspace cannot be removed without removing label information.
2. **Source and label are confounded by construction.**
   - With `project`, Nutrient Kaggle (potassium) drops from 0.684 to 0.000 R@1 (probe).
   - In training, potassium comes only from Netrokona, so the direction that marks Netrokona is the direction that marks potassium.
   - `center` fails for the same reason: a source's mean carries its class mix. Stem Borer BD holds only stem borer and healthy plants, and Kaggle only nutrient disorders.
3. **Within-class removal is milder but still negative.** `project_cc` keeps most of Kaggle (0.474 probe, 0.509 kNN) and leaves source accuracy at 0.872. So most of the source signal is not separable from the class with linear tools on these datasets.
4. **One partial exception:** with `project`, the probe raises Dhan-Shomadhan cross-source from 0.099 to 0.242 R@1 (n = 91). This fits the white-background confusion of section 4, but it costs more elsewhere than it gains.
5. **Consequence for the paper:** the cross-source gap is not a feature-space bias that a projection can remove. Each class is covered by too few sources. Two things follow:
   - The remedy is data, i.e. a second source per target (the data-gap item of section 4; Mohanty et al. 2016).
   - The knowledge must come from outside the pixels, as in step 2 and the KG-text prototypes of 9.4.
   - Report this as a negative control: the obvious debiasing does not close the gap.
