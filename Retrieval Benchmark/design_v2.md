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

## 4. Stage-1 results (split version 2)

Query: the image only. Candidates: all 19 conditions. Encoder: CLIP ViT-L/14. Full table, including per dataset: [`results/stage1_results.md`](results/stage1_results.md).

**In-distribution test split (2,968 images):**

| System | R@1 | MRR | Paddy Doctor R@1 |
|---|---:|---:|---:|
| CLIP zero-shot, label prompt | 0.098 | 0.235 | 0.087 |
| CLIP zero-shot, label + KG symptom prompts | 0.048 | 0.211 | 0.033 |
| Image kNN over train (mean of top 5) | 0.439 | 0.614 | 0.297 |
| Linear probe on train (supervised reference) | 0.483 | 0.653 | 0.373 |

Chance R@1 is 0.053.

**Cross-dataset (train on Paddy Doctor, query Dhan-Shomadhan blast, brown spot and tungro; 606 images):**

| System | R@1 | R@3 | MRR |
|---|---:|---:|---:|
| CLIP zero-shot, label prompt | 0.094 | 0.201 | 0.219 |
| CLIP zero-shot, label + KG symptom prompts | 0.157 | 0.474 | 0.401 |
| Image kNN over Paddy Doctor train | 0.483 | 0.832 | 0.668 |
| Linear probe on Paddy Doctor train | 0.436 | 0.782 | 0.633 |

**Reading:**
1. **Split v1 leaked.** On v1, kNN R@1 was 0.917 (Paddy Doctor 0.924), because burst photos were in train and test. On v2 it is 0.439 (Paddy Doctor 0.297). Every number reported from now on uses v2.
2. **Generic CLIP text does not know rice symptoms.** Zero-shot is near chance in-distribution. Adding the KG symptom prompts lowers it, because blast and brown spot share "brown lesion", "leaf spot" and "wilting". Symptom matching must therefore happen in step 2 with a VLM and the closed vocabulary, not in the CLIP text space.
3. **The KG text helps across datasets.** In the cross-dataset test, symptom prompts raise R@3 from 0.201 to 0.474. This is the first sign that graph knowledge transfers where image memory does not.
4. **There is headroom for step 2.** Image kNN places the right condition in its top 3 for 83% of the cross-dataset queries, but at rank 1 for only 48%. Re-ranking within a short list is exactly step 2's job.
5. **Confusions to target:** Hispa ↔ Normal, Stem borer ↔ Deadheart (a pest and its own symptom), Blast ↔ Tungro, and Downy mildew → Hispa. The pest–symptom pair is a modelling question, not only a retrieval one: is "Deadheart" a correct answer for a stem borer photo?
6. **Dataset shortcut:** Netrokona and YUKE-WBC each hold one label and score up to 1.000. They are reported but not used as evidence.
