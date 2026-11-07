# Symptom inventory for the 17 benchmark conditions (phase 1)

**Date:** 2026-11-07. **KG state:** `Ontology/Rice MMKG.rdf`, `owl:versionInfo` 0.7.0-dev, commit `a91126a`. **Status:** read-only inventory for maintainer review. No file other than this one was changed.

**Update 2026-11-07:** the blast and brown spot rows (§3.1, §3.3) were added to the KG in **0.8.0**; see the changelog in `Ontology/Ontology_Overview.md`. The rest of this document describes the 0.7.0-dev state it was written on. The other conditions are still open.

**Update 2026-11-07 (0.8.1):** the four provenance issues of §6.4, items 1–4, are fixed.
- **Fixed by adding a passage:**
  - item 2, `Brown_Lesion → leaf blade`: now linked to `blast-leaf-collar_p8`;
  - item 3, `Discolored_Panicle → panicle`: now linked to `brown-spot_p10`.
  - Both links are `LLM-reviewed` until the curator confirms them.
- **Fixed by removal:**
  - item 1, `Brown_Leaf_Tip → leaf blade`;
  - item 4, `Yellow_Stripe → leaf blade`.
  - No IRRI passage states either, and the CABI datasheets that could support them returned 403. Both are now questions X10 and X11 in §7.4.
- **Labels:** three symptom labels that contained a condition's name were also changed (`Pinhead_Brown_Spot`, `Panicle_Blast`, `Dusty_Brown_Spot`).
- §6.4 items 5–8 are unchanged.

**Update 2026-11-07 (0.9.0-dev):** the tungro and bacterial leaf blight rows (§3.4, §3.9) were added to the KG.
- **Tungro:** 7 new symptoms, plus `Grain_Discoloration` reused.
- **Bacterial leaf blight:** 8 new symptoms, plus `Seedling_Death` reused.
- **Left out, as in 0.8.0:** signs, field patterns and ambiguous rows.

**Update 2026-11-07 (0.9.0-dev, batch 3):** the rows of the remaining six conditions with an IRRI sheet were added (§3.10, §3.5, §3.14, §3.15, §3.12, §3.17).
- **New symptoms:** 16 in total, plus `Leaf_Drying`, `Leaf_Death` and `Empty_Grain` reused.
  - bacterial leaf streak 1; sheath blight 4; hispa 5; leaffolder 3; stem borer 1; brown planthopper 2.
- **`Hopper_Burn`:** now has a comment describing what it looks like.
- **Left out:**
  - signs, field patterns and ambiguous rows;
  - details already in the comment of an existing symptom: candidates for label refinement, not new symptoms.

**Update 2026-11-07 (0.9.0-dev, IRRI 2018):** the rows of §4.1 were added to the KG for leaf scald, downy mildew and bacterial panicle blight, the three conditions without an IRRI fact sheet. Their source is IRRI (2018) *Rice Diseases*.
- **Text layer:** 3 new text documents with 15 passages, whose wording is in `Text Modality/RiceMMKG_IRRI_RD2018_text.ttl` (CC BY-NC-SA 4.0).
- **New symptoms:** 28 in total (leaf scald 11, downy mildew 6, bacterial panicle blight 11).
- **Reused:** 7 existing symptoms.
- **Left out:** signs (DM3, DM4) and ambiguous rows. Rows already linked from CABI keep their CABI source only.
- **Regional rows:** the leaf scald rows that the source reports only from Japan, Korea or Costa Rica were added, and their comments say so.
- **X11:** still open. The source gives oospores only in its "Causal organism" section.
- **Second source:** rows LS1, GR3, GR10 and GR14 were already linked from CABI or IRRI Rice Doctor. Their axioms now also cite IRRI (2018), with its passage as evidence.
- **Status:** every condition with an IRRI fact sheet is now covered. Still open:
  - the three diseases without a sheet (§4);
  - Normal_Health (§5);
  - decisions M4, M6 and M7.

Phase 2 (editing) follows MAINTENANCE.md: a provenance axiom for each assertion, a MINOR version bump, a HermiT check on a copy in a path without spaces, and the CQ benchmarks.

## 1. Scope and method

**Sources read:**
- **KG:** `Ontology/Rice MMKG.rdf`, parsed with rdflib 7.6.0. For each condition this inventory lists:
  - `rice:indicatedBy` → Symptom (`rdfs:label`);
  - `rice:affectsPlantPart` of each symptom;
  - for both, the `owl:Axiom` with `dcterms:source` and `rice:hasEvidencePassage`.
- **IRRI passages:** `Text Modality/RiceMMKG_IRRI_text.ttl`, the `rice:passageText` of the 14 fact sheets that cover a benchmark condition:
  - diseases: brown-spot, blast-leaf-collar, blast-node-neck, tungro, sheath-blight, bacterial-blight, bacterial-leaf-streak;
  - nutrient disorders: nitrogen, phosphorus, potassium-k;
  - pests: stem-borer, rice-hispa, rice-leaffolder, planthopper.
- **Raw pages:** `Data/irri-rkb/raw_2026-10-20/*.html`, checked for content outside the passages.
  - Image `alt` texts are file names only (e.g. `blast-leaf-1`), and the image captions are already inside the passages.
  - `rice-doctor.html` is a landing page with no symptom text.
  - The other five sheets (armyworms, iron-toxicity, rice-bug, salinity, zinc) cover none of the 17 conditions. One sentence from them is used: the tungro and potassium contrast in `potassium-k_p3`.

**Rule against tuning:**
- Every visual statement in the sheet of each condition is listed, whether the condition did well or badly in the benchmark.
- The benchmark documents (design_v2 §9.4 and §9.6, plan §0.1–0.2) were read for context only. They did not decide which rows are included.

**Quotes:**
- Every quote is copied from `rice:passageText`.
- A script checked each one as an exact substring of its passage: 137 quotes in the tables and 22 in §6.3, with 0 mismatches.
- IRRI writes ranges with a minus sign (U+2212, e.g. "5−14 mm"). The quotes keep it.

**The "In KG?" column:**
- **exact:** a symptom already linked to this condition by `indicatedBy` has an `rdfs:label` that states the feature.
- **partial:** the feature is covered only by the `rdfs:comment` of a linked symptom, or only by a broader label (e.g. `Leaf Spot` for "circular to oval lesion"). This matters because the benchmark reads `rdfs:label` only, not comments (`stage1_baselines.py`, `step2_rerank.py`, `zsl_dev.py`).
- **missing:** nothing linked to this condition states it.
- **missing (reuse `X`?):** an existing individual `X` would fit, but it is not linked to this condition. Whether to reuse it is a phase-2 decision; see open question M3.

**Tags on rows:**
- no tag: a symptom on the plant;
- **[sign]:** the organism or its products (ooze, sclerotia, eggs, insects, frass, silk). These are visual, but they are not plant symptoms under the current definition of `rice:Symptom` ("An observable sign on the plant that indicates the presence of a Disease or Pest");
- **[field]:** a pattern seen at field or stand scale;
- **[⚠ ambiguous]:** visual only in time, as an absence, or as a count. Also listed in §6.3.

**Proposed labels:**
- Written in the style of the newer lower-case labels.
- A label in parentheses names the existing individual that already covers the row.
- "(NEW)" in the plant-part column marks a part that is not yet a `PlantPart` individual. The ten existing ones are: grain, leaf, leaf blade, leaf sheath, panicle, panicle neck, root, stem, tiller and whole plant.

**Current coverage of the 17 conditions:**
- 61 `indicatedBy` assertions over 38 distinct symptoms. 20 of the 61 have an evidence passage.
- 39 `affectsPlantPart` assertions on those symptoms. 31 of the 39 have an evidence passage.
- Most `indicatedBy` assertions without a passage cite the CABI Compendium, which is not in the text module.

## 2. A finding that changes the blast and brown spot premise

The task states that blast and brown spot are separated by "diamond or spindle with a grey centre, vs round or oval and evenly brown". The IRRI wording only partly supports this:
- **Brown spot also has a grey centre.**
  - `IRRI_RKB_brown-spot_p8`: "Fully developed lesions are circular to oval with a light brown to gray center, surrounded by a reddish brown margin caused by the toxin produced by the fungi."
  - `IRRI_RKB_brown-spot_p12` gives the same check: "have a gray center surrounded by a reddish margin".
- **The margins overlap.**
  - Blast: "red to brownish or necrotic border" (`blast-leaf-collar_p5`).
  - Brown spot: "reddish brown margin".
- **The separators IRRI states:**
  - shape: blast "elongated and pointed at each end", spindle or diamond; brown spot "more round", circular to oval;
  - the yellow halo, stated for brown spot only (`blast-leaf-collar_p8`);
  - the early lesion colour: blast "white to gray-green … with dark green borders"; brown spot "dark brown to purple-brown";
  - size: brown spot lesions are 5−14 mm on susceptible varieties and pinhead-sized on resistant ones.

"Evenly brown" is not IRRI's wording. If it is used in a prompt or a question, it needs another source or the domain expert's confirmation (question X1).

## 3. Inventory by condition

Each condition has two tables:
1. **KG now:** what the KG asserts today.
2. **Inventory:** every visual statement in the IRRI source.

Notes on the KG and on scope follow each pair of tables.

### 3.1 Brown_Spot

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Brown_Lesion` "Brown Lesion" | CABI 14691 | none | leaf blade | IRRI blast-leaf-collar | none |
| ″ | ″ | ″ | leaf sheath | IRRI brown-spot | brown-spot_p10 (human-reviewed) |
| `Grain_Discoloration` "grain discoloration" | CABI 14691 | none | grain | IRRI brown-spot | brown-spot_p11 (human-reviewed) |
| `Leaf_Spot` "Leaf Spot" | CABI 14691 | none | leaf blade | IRRI brown-spot | brown-spot_p10 (human-reviewed) |
| `Wilting` "Wilting" | CABI 14691 | none | whole plant | IRRI bacterial-blight | bacterial-blight_p5 (human-reviewed) |

**Inventory** (sources: `brown-spot.html`; one comparison sentence in `blast-leaf-collar.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Numerous big spots on leaves | partial | numerous large leaf spots | leaf blade | `brown-spot.html`, `IRRI_RKB_brown-spot_p2`: "Its most observable damage is the numerous big spots on the leaves which can kill the whole leaf."<br>_Note: Leaf Spot is broader_ |
| 2 | Spots kill the whole leaf | **missing** | leaf death from spots | leaf blade | `brown-spot.html`, `IRRI_RKB_brown-spot_p2`: "which can kill the whole leaf" |
| 3 | Seedling: small circular yellow-brown or brown lesions on the coleoptile | **missing** | circular brown lesion on coleoptile | coleoptile (NEW) | `brown-spot.html`, `IRRI_RKB_brown-spot_p6`: "Infected seedlings have small, circular, yellow brown or brown lesions that may girdle the coleoptile and distort primary and secondary leaves." |
| 4 | Seedling: coleoptile girdled | **missing** | girdled coleoptile | coleoptile (NEW) | `brown-spot.html`, `IRRI_RKB_brown-spot_p6`: "lesions that may girdle the coleoptile" |
| 5 | Seedling: primary and secondary leaves distorted | **missing** | distorted seedling leaves | leaf | `brown-spot.html`, `IRRI_RKB_brown-spot_p6`: "distort primary and secondary leaves" |
| 6 | Young lesion small, circular, dark brown to purple-brown | **missing** | small dark brown to purple-brown circular lesion | leaf blade | `brown-spot.html`, `IRRI_RKB_brown-spot_p7`: "Starting at tillering stage, lesions can be observed on the leaves. They are initially small, circular, and dark brown to purple-brown."<br>_Note: from tillering_ |
| 7 | Mature lesion circular to oval | partial | circular to oval lesion | leaf blade | `brown-spot.html`, `IRRI_RKB_brown-spot_p8`: "Fully developed lesions are circular to oval with a light brown to gray center, surrounded by a reddish brown margin caused by the toxin produced by the fungi."<br>`blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p8`: "brown spot lesions tend to be more round"<br>_Note: Leaf Spot names no shape_ |
| 8 | Mature lesion centre light brown to gray | **missing** | lesion with light brown to grey centre | leaf blade | `brown-spot.html`, `IRRI_RKB_brown-spot_p8`: "with a light brown to gray center"<br>`brown-spot.html`, `IRRI_RKB_brown-spot_p12`: "To confirm, check if spots are circular, brownish, and have a gray center surrounded by a reddish margin."<br>_Note: a grey centre is also stated for blast_ |
| 9 | Mature lesion margin reddish brown | partial | reddish-brown lesion margin | leaf blade | `brown-spot.html`, `IRRI_RKB_brown-spot_p8`: "surrounded by a reddish brown margin"<br>_Note: Brown Lesion gives the colour of the lesion, not of its margin_ |
| 10 | Yellow halo around the lesion | **missing** | yellow halo around lesion | leaf blade | `blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p8`: "brown spot lesions tend to be more round, brown in color and have a yellow halo surrounding the lesion."<br>_Note: stated in the blast sheet only_ |
| 11 | Lesions 5-14 mm long on susceptible varieties | **missing** | lesion 5-14 mm long | leaf blade | `brown-spot.html`, `IRRI_RKB_brown-spot_p9`: "On susceptible varieties, lesions are 5−14 mm long which can cause leaves to wilt." |
| 12 | Leaves wilt | partial | leaf wilting | leaf | `brown-spot.html`, `IRRI_RKB_brown-spot_p9`: "which can cause leaves to wilt"<br>_Note: KG Wilting is asserted on whole plant_ |
| 13 | Pinhead-sized brown lesions on resistant varieties | **missing** | pinhead-sized brown lesion | leaf blade | `brown-spot.html`, `IRRI_RKB_brown-spot_p9`: "On resistant varieties, the lesions are brown and pinhead-sized." |
| 14 | Sheath lesions like leaf lesions | exact | (Brown Lesion, leaf sheath) | leaf sheath | `brown-spot.html`, `IRRI_RKB_brown-spot_p10`: "Lesions on leaf sheaths are similar to those on the leaves."<br>_Note: already the evidence passage of Brown_Lesion affectsPlantPart leaf sheath_ |
| 15 | Dark brown to black oval spots on glumes and panicle branches | **missing** (reuse `Discolored_Panicle`?) | dark brown to black oval spots on glumes | glume, panicle branch (NEW) | `brown-spot.html`, `IRRI_RKB_brown-spot_p10`: "Infected glumes and panicle branches have dark brown to black oval spots or discoloration on the entire surface."<br>_Note: Discolored_Panicle is linked only to Bacterial_Panicle_Blight_ |
| 16 | Unfilled or incompletely filled grains | **missing** (reuse `Empty_Grain`?) | (empty grain) | grain | `brown-spot.html`, `IRRI_RKB_brown-spot_p2`: "When infection occurs in the seed, unfilled grains or spotted or discolored seeds are formed."<br>`brown-spot.html`, `IRRI_RKB_brown-spot_p11`: "Infection of florets leads to incomplete or disrupted grain filling and a reduction in grain quality." |
| 17 | Spotted or discoloured grains ('pecky rice') | exact | (grain discoloration); altLabel 'pecky rice' | grain | `brown-spot.html`, `IRRI_RKB_brown-spot_p11`: "The disease-causing fungi can also penetrate grains, causing 'pecky rice', a term used to describe spotting and discoloration of grains." |

**Notes:**
- The four current symptoms are all sourced to CABI, with no passage.
- `Brown Lesion` and `Leaf Spot` state no shape, centre, margin or halo, so they cannot separate brown spot from blast.
- IRRI lists the infected parts as "the coleoptile, leaves, leaf sheath, panicle branches, glumes, and spikelets" (`brown-spot_p1`). Coleoptile, glume, spikelet and panicle branch are not `PlantPart` individuals.

### 3.2 Leaf_Scald — no IRRI fact sheet

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Zonate_Leaf_Lesion` "zonate leaf lesion" | Rice Doctor (Lucid) Scald | none | leaf blade | Rice Doctor (Lucid) Scald | none |

- The label "zonate leaf lesion" carries only the pattern. The comment adds the rest: "alternating light tan and dark brown starting from leaf tips or edges; affected areas dry out, giving the leaf a scalded appearance".
- The source is IRRI Rice Doctor, a Lucid key. It is not one of the saved fact sheets and is not in the text module.
- See §4 for sources.

### 3.3 Rice_Blast_Disease

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Brown_Lesion` "Brown Lesion" | CABI 46103 | none | leaf blade | IRRI blast-leaf-collar | none |
| ″ | ″ | ″ | leaf sheath | IRRI brown-spot | brown-spot_p10 (human-reviewed) |
| `Leaf_Spot` "Leaf Spot" | CABI 46103 | none | leaf blade | IRRI brown-spot | brown-spot_p10 (human-reviewed) |
| `Neck_Rot` "neck rot" | CABI 46103 | none | panicle neck | IRRI blast-node-neck | blast-node-neck_p6 (human-reviewed) |
| `Node_Lesion` "node lesion" | IRRI blast-node-neck | blast-node-neck_p5 (human-reviewed) | stem | IRRI blast-node-neck | blast-node-neck_p5 (human-reviewed) |
| `Panicle_Blast` "panicle blast" | CABI 46103 | none | panicle neck | IRRI blast-node-neck | blast-node-neck_p6 (human-reviewed) |
| `White_Ear` "white ear" | IRRI blast-node-neck | blast-node-neck_p8 (human-reviewed) | panicle | IRRI stem-borer | stem-borer_p9 (LLM-reviewed) |
| `Wilting` "Wilting" | CABI 46103 | none | whole plant | IRRI bacterial-blight | bacterial-blight_p5 (human-reviewed) |

**Inventory** (sources: `blast-leaf-collar.html`, `blast-node-neck.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Initial lesions white to gray-green with dark green borders | **missing** | white to grey-green lesion with dark green border | leaf blade; leaf collar (NEW) | `blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p4`: "Initial symptoms appear as white to gray-green lesions or spots, with dark green borders." |
| 2 | Older lesions elliptical or spindle-shaped, pointed at each end | **missing** | spindle-shaped lesion | leaf blade | `blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p5`: "Older lesions on the leaves are elliptical or spindle-shaped and whitish to gray centers with red to brownish or necrotic border."<br>`blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p8`: "Leaf blast lesions are usually elongated and pointed at each end" |
| 3 | Lesion centre whitish to gray | **missing** | lesion with whitish to grey centre | leaf blade | `blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p5`: "whitish to gray centers"<br>_Note: a grey centre is also stated for brown spot_ |
| 4 | Lesion border red to brownish or necrotic | partial | red-brown or necrotic lesion border | leaf blade | `blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p5`: "with red to brownish or necrotic border"<br>_Note: Brown Lesion is nearest; it calls the whole lesion brown_ |
| 5 | Diamond-shaped lesions, wide in the centre, pointed at the ends | **missing** | diamond-shaped lesion | leaf blade | `blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p6`: "Some resemble diamond shape, wide in the center and pointed toward either ends." |
| 6 | Lesions enlarge and coalesce, killing whole leaves | **missing** | coalescing lesions killing the leaf | leaf blade | `blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p6`: "Lesions can enlarge and coalesce, growing together, to kill the entire leaves." |
| 7 | Lesions on the collar (collar blast) | **missing** | collar lesion | leaf collar (NEW) | `blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p4`: "Check the leaf and collar for lesions:"<br>`blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p7`: "Collar blast"<br>_Note: second quote is an image caption_ |
| 8 | Seedlings or young plants killed | **missing** | seedling death | whole plant | `blast-leaf-collar.html`, `IRRI_RKB_blast-leaf-collar_p9`: "A leaf blast infection can kill seedlings or plants up to the tillering stage."<br>_Note: visible, not specific_ |
| 9 | Node lesions in banded pattern | partial | banded node lesion | node (NEW; KG uses stem) | `blast-node-neck.html`, `IRRI_RKB_blast-node-neck_p5`: "Node infection occurs in banded pattern."<br>_Note: in the comment of node lesion, not its label_ |
| 10 | Node lesions blackish to grayish brown | partial | blackish to greyish-brown node lesion | node (NEW; KG uses stem) | `blast-node-neck.html`, `IRRI_RKB_blast-node-neck_p5`: "Lesions on the node are blackish to grayish brown."<br>_Note: comment only_ |
| 11 | Culm breaks at infected node | partial | broken culm at node | stem | `blast-node-neck.html`, `IRRI_RKB_blast-node-neck_p6`: "Infected nodes can cause the culm or the part of the plant that holds the panicle to break."<br>_Note: comment of node lesion only_ |
| 12 | Neck lesions grayish brown | partial | greyish-brown neck lesion | panicle neck | `blast-node-neck.html`, `IRRI_RKB_blast-node-neck_p6`: "Lesions on the neck are grayish brown and can cause girdling, making the neck and the panicle fall over."<br>_Note: labels panicle blast / neck rot give no colour_ |
| 13 | Neck girdled; neck and panicle fall over | **missing** | girdled neck with fallen panicle | panicle neck | `blast-node-neck.html`, `IRRI_RKB_blast-node-neck_p6`: "can cause girdling, making the neck and the panicle fall over" |
| 14 | Few or no grains formed | **missing** (reuse `Empty_Grain`?) | (empty grain) | grain | `blast-node-neck.html`, `IRRI_RKB_blast-node-neck_p2`: "When a node or neck blast infection is present, it can cause plants to develop few or no grains at all."<br>`blast-node-neck.html`, `IRRI_RKB_blast-node-neck_p7`: "If infection of the neck occurs before milky stage, no grain is formed" |
| 15 | Whiteheads or white panicles | exact | (white ear); altLabel 'whitehead' | panicle | `blast-node-neck.html`, `IRRI_RKB_blast-node-neck_p8`: "Neck and node blast can also cause whiteheads or white panicles, similar to stem borer infection." |

**Notes:**
- **Leaf symptoms:** `Brown Lesion`, `Leaf Spot` and `Wilting` cite CABI 46103.
  - The IRRI blast sheets do not state wilting.
  - They describe leaf lesions with whitish to grey centres, not brown lesions.
  - These assertions are not wrong because they have another source, but the expert should check them (X2).
- **Parts:** IRRI says blast "can affect all above ground parts of a rice plant: leaf, collar, node, neck, parts of panicle, and sometimes leaf sheath" (`blast-leaf-collar_p1`). Collar and node are not parts in the KG; `Node_Lesion` uses stem.

### 3.4 Rice_Tungro_Disease

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Empty_Grain` "empty grain" | IRRI tungro | tungro_p1 (human-reviewed) | grain | IRRI rice-bug | rice-bug_p5 (human-reviewed) |
| `Reduced_Tillering` "reduced tillering" | CABI 47654 | none | tiller | IRRI tungro | tungro_p14 (human-reviewed) |
| `Sterile_Panicle` "sterile panicle" | IRRI tungro | tungro_p14 (human-reviewed) | panicle | IRRI tungro | tungro_p14 (LLM-reviewed) |
| `Stunted_Growth` "stunted growth" | CABI 47654 | none | whole plant | IRRI tungro | tungro_p14 (LLM-reviewed) |
| `Yellow_Leaf` "Yellow Leaf" | CABI 47654 | none | leaf blade | IRRI tungro | tungro_p13 (LLM-reviewed) |
| `Yellow_Orange_Discoloration` "yellow-orange leaf discoloration" | CABI 47654 | none | leaf blade | IRRI tungro | tungro_p13 (human-reviewed) |

**Inventory** (source: `tungro.html`; row 14 from `potassium-k.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Yellow or orange-yellow leaf discoloration | exact | (yellow-orange leaf discoloration; Yellow Leaf) | leaf blade | `tungro.html`, `IRRI_RKB_tungro_p13`: "Yellow or orange-yellow discoloration is noticeable in tungro-infected plants." |
| 2 | Discoloration starts at the leaf tip and extends down | **missing** | discoloration spreading from leaf tip downward | leaf blade | `tungro.html`, `IRRI_RKB_tungro_p13`: "Discoloration begins from the leaf tip and extends down to the blade or the lower leaf portion." |
| 3 | Mottled appearance | **missing** | mottled leaf | leaf blade | `tungro.html`, `IRRI_RKB_tungro_p13`: "Infected leaves may also show mottled or striped appearance, rust-colored spots, and inter-veinal necrosis." |
| 4 | Striped appearance | **missing** | striped leaf | leaf blade | `tungro.html`, `IRRI_RKB_tungro_p13`: "mottled or striped appearance"<br>_Note: stripe colour not stated; do not reuse Yellow_Stripe unchecked_ |
| 5 | Rust-coloured spots | **missing** | rust-coloured leaf spots | leaf blade | `tungro.html`, `IRRI_RKB_tungro_p13`: "rust-colored spots" |
| 6 | Interveinal necrosis | **missing** | interveinal necrosis | leaf blade | `tungro.html`, `IRRI_RKB_tungro_p13`: "inter-veinal necrosis" |
| 7 | Stunting | exact | (stunted growth) | whole plant | `tungro.html`, `IRRI_RKB_tungro_p14`: "Tungro-infected plants also show symptoms of stunting, delayed flowering which may delay maturity, reduced number of tillers, small and not completely exserted panicles, as well as a higher than normal percentage of sterile panicles or partially filled grains, covered with dark brown blotches." |
| 8 | Reduced number of tillers | exact | (reduced tillering) | tiller | `tungro.html`, `IRRI_RKB_tungro_p14`: "reduced number of tillers" |
| 9 | Small, not completely exserted panicles | **missing** | small, incompletely exserted panicle | panicle | `tungro.html`, `IRRI_RKB_tungro_p14`: "small and not completely exserted panicles" |
| 10 | Sterile panicles | exact | (sterile panicle) | panicle | `tungro.html`, `IRRI_RKB_tungro_p14`: "a higher than normal percentage of sterile panicles" |
| 11 | Partially filled grains | partial | partially filled grain | grain | `tungro.html`, `IRRI_RKB_tungro_p14`: "partially filled grains"<br>`tungro.html`, `IRRI_RKB_tungro_p1`: "sterile or partly filled grains"<br>_Note: empty grain is nearest; 'partly filled' is not 'empty'_ |
| 12 | Grains covered with dark brown blotches | **missing** (reuse `Grain_Discoloration`?) | dark brown blotches on grain | grain | `tungro.html`, `IRRI_RKB_tungro_p14`: "partially filled grains, covered with dark brown blotches" |
| 13 | Delayed flowering, may delay maturity [⚠ ambiguous] | **missing** (reuse `Delayed_Maturity`?) | delayed flowering | whole plant | `tungro.html`, `IRRI_RKB_tungro_p14`: "delayed flowering which may delay maturity"<br>_Note: temporal; not visible in one photo_ |
| 14 | Occurs in patches in a field [field] | **missing** | patchy occurrence in field | field / stand (NEW) | `potassium-k.html`, `IRRI_RKB_potassium-k_p3`: "Tungro occurs in patches in a field (not in the whole field) and usually has more pronounced yellow and orange leaves and plant stunting"<br>_Note: stated in the potassium sheet_ |
| 15 | Leafhoppers (vector) present [sign] | **missing** | green leafhopper on plant | whole plant | `tungro.html`, `IRRI_RKB_tungro_p13`: "Check for presence of leafhoppers."<br>_Note: vector, not the cause_ |

**Notes:**
- IRRI says severity varies: "In varieties that carry some resistance to the disease, infected plants exhibit no discoloration or only a mild discoloration that may disappear as the plants mature" (`tungro_p15`).
- So a resistant-variety photo may show none of the leaf symptoms above.

### 3.5 Sheath_Blight

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Leaf_Sheath_Lesion` "leaf sheath lesion" | CABI 47203 | none | leaf sheath | IRRI sheath-blight | sheath-blight_p10 (human-reviewed) |
| `Tiller_Death` "tiller death" | IRRI sheath-blight | sheath-blight_p1 (human-reviewed) | tiller | IRRI sheath-blight | sheath-blight_p1 (human-reviewed) |
| `Wilting` "Wilting" | CABI 47203 | none | whole plant | IRRI bacterial-blight | bacterial-blight_p5 (human-reviewed) |

**Inventory** (source: `sheath-blight.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Oval or ellipsoidal greenish-gray sheath lesions | partial | oval greenish-grey sheath lesion | leaf sheath | `sheath-blight.html`, `IRRI_RKB_sheath-blight_p5`: "oval or ellipsoidal greenish gray lesions, usually 1-3 cm long, on the leaf sheath, initially just above the soil or water level in the case of conventionally flooded rice."<br>_Note: shape and colour in the comment of leaf sheath lesion only_ |
| 2 | Lesions 1-3 cm long | **missing** | sheath lesion 1-3 cm long | leaf sheath | `sheath-blight.html`, `IRRI_RKB_sheath-blight_p5`: "usually 1-3 cm long" |
| 3 | Lesions first just above soil or water level | partial | lesion near water line | leaf sheath | `sheath-blight.html`, `IRRI_RKB_sheath-blight_p5`: "initially just above the soil or water level"<br>_Note: comment only_ |
| 4 | Lesions initially water-soaked | **missing** | water-soaked sheath lesion | leaf sheath | `sheath-blight.html`, `IRRI_RKB_sheath-blight_p10`: "To confirm the cause of disease, check for irregular lesions usually found on the leaf sheaths (initially water-soaked to greenish gray and later becomes grayish white with brown margin)." |
| 5 | Sheath lesions later grayish white with brown margin | partial | grey-white sheath lesion with brown margin | leaf sheath | `sheath-blight.html`, `IRRI_RKB_sheath-blight_p10`: "later becomes grayish white with brown margin"<br>_Note: comment only_ |
| 6 | Lesions expand upward to upper sheaths and leaves, then to neighbouring tillers | **missing** | lesions spreading upward from sheath to leaves | leaf sheath, leaf blade, tiller | `sheath-blight.html`, `IRRI_RKB_sheath-blight_p6`: "under favorable conditions, these initial lesions multiply and expand to the upper part of the sheaths, the leaves, and then spread to neighboring tillers belonging to different hills (transplanted rice) or plants (direct-seeded rice)."<br>_Note: progression_ |
| 7 | Irregular leaf lesions with gray-white centres and brown margins | **missing** | irregular leaf lesion with grey-white centre and brown margin | leaf blade | `sheath-blight.html`, `IRRI_RKB_sheath-blight_p7`: "lesions on the leaves usually have irregular lesions, often with gray-white centers and brown margins as they grow older." |
| 8 | Leaves senesce or dry out early | **missing** | premature leaf drying | leaf | `sheath-blight.html`, `IRRI_RKB_sheath-blight_p1`: "Infected leaves senesce or dry out and die more rapidly, young tillers can also be destroyed." |
| 9 | Young tillers destroyed | exact | (tiller death) | tiller | `sheath-blight.html`, `IRRI_RKB_sheath-blight_p1`: "young tillers can also be destroyed" |
| 10 | Sclerotia present [sign] | **missing** | sclerotia on sheath | leaf sheath | `sheath-blight.html`, `IRRI_RKB_sheath-blight_p10`: "Also check for presence of sclerotia."<br>`sheath-blight.html`, `IRRI_RKB_sheath-blight_p4`: "sclerotia or infection bodies floating on the water"<br>_Note: the sheet does not say what sclerotia look like_ |

**Notes:**
- `Wilting` (CABI 47203) is not stated in the IRRI sheet.
- Most of the sheet's description already sits in the comment of `Leaf_Sheath_Lesion`, so it does not reach the benchmark, which reads labels only. Hence the many "partial" rows.

### 3.6 Potassium_Deficiency_Disorder

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Black_Root` "black roots" | IRRI potassium-k | potassium-k_p3 (human-reviewed) | root | IRRI potassium-k | potassium-k_p3 (human-reviewed) |
| `Empty_Grain` "empty grain" | IRRI potassium-k | potassium-k_p3 (human-reviewed) | grain | IRRI rice-bug | rice-bug_p5 (human-reviewed) |
| `Lodging` "lodging" | IRRI potassium-k | potassium-k_p3 (human-reviewed) | whole plant | IRRI potassium-k | potassium-k_p3 (human-reviewed) |
| `Necrotic_Leaf_Tip_Margin` "necrotic leaf tips and margins" | IRRI potassium-k | potassium-k_p3 (LLM-reviewed) | leaf | IRRI potassium-k | potassium-k_p3 (human-reviewed) |
| `Stunted_Growth` "stunted growth" | IRRI potassium-k | potassium-k_p3 (human-reviewed) | whole plant | IRRI tungro | tungro_p14 (LLM-reviewed) |
| `Yellowish_Brown_Leaf_Margin` "yellowish-brown leaf margins" | IRRI potassium-k | potassium-k_p3 (human-reviewed) | leaf | IRRI potassium-k | potassium-k_p3 (LLM-reviewed) |

**Inventory** (source: `potassium-k.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Stunted plants | exact | (stunted growth) | whole plant | `potassium-k.html`, `IRRI_RKB_potassium-k_p3`: "Stunted dark green plants with yellowish brown leaf margins and/or older leaves with necrotic tips and margins" |
| 2 | Dark green plants | **missing** | dark green plant | whole plant | `potassium-k.html`, `IRRI_RKB_potassium-k_p3`: "Stunted dark green plants"<br>_Note: dark green erect leaves (P) adds 'erect', not stated for K_ |
| 3 | Yellowish brown leaf margins | exact | (yellowish-brown leaf margins) | leaf | `potassium-k.html`, `IRRI_RKB_potassium-k_p3`: "yellowish brown leaf margins" |
| 4 | Necrotic leaf tips and margins | exact | (necrotic leaf tips and margins) | leaf | `potassium-k.html`, `IRRI_RKB_potassium-k_p3`: "older leaves with necrotic tips and margins" |
| 5 | Symptoms on older leaves | partial | on older leaves | leaf (position) | `potassium-k.html`, `IRRI_RKB_potassium-k_p3`: "older leaves with necrotic tips and margins"<br>_Note: position in comment only_ |
| 6 | Unhealthy or black roots | exact | (black roots) | root | `potassium-k.html`, `IRRI_RKB_potassium-k_p3`: "unhealthy or black roots"<br>_Note: not visible above ground_ |
| 7 | Greater lodging | exact | (lodging) | whole plant | `potassium-k.html`, `IRRI_RKB_potassium-k_p3`: "greater lodging" |
| 8 | Unfilled grains | exact | (empty grain) | grain | `potassium-k.html`, `IRRI_RKB_potassium-k_p3`: "higher level of unfilled grains" |

**Notes:**
- The IRRI sheet is one sentence, and the KG already covers almost all of it.
- More visual detail, such as the progression on older leaves or the colour of the margins in different stages, would need another source. See §6.1 and question M10.

### 3.7 Nitrogen_Deficiency_Disorder

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Reduced_Tillering` "reduced tillering" | IRRI nitrogen | nitrogen_p3 (LLM-reviewed) | tiller | IRRI tungro | tungro_p14 (human-reviewed) |
| `Stunted_Growth` "stunted growth" | IRRI nitrogen | nitrogen_p3 (LLM-reviewed) | whole plant | IRRI tungro | tungro_p14 (LLM-reviewed) |
| `Yellowish_Green_Leaf` "yellowish-green leaves" | IRRI nitrogen | nitrogen_p3 (human-reviewed) | leaf | IRRI nitrogen | nitrogen_p3 (LLM-reviewed) |

**Inventory** (source: `nitrogen.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Stunted plants | exact | (stunted growth) | whole plant | `nitrogen.html`, `IRRI_RKB_nitrogen_p3`: "Stunted plants with small yellowish green leaves and fewer tillers" |
| 2 | Small leaves | partial | small leaves | leaf | `nitrogen.html`, `IRRI_RKB_nitrogen_p3`: "small yellowish green leaves"<br>_Note: 'small' is in the comment of yellowish-green leaves, not its label_ |
| 3 | Yellowish green leaves | exact | (yellowish-green leaves) | leaf | `nitrogen.html`, `IRRI_RKB_nitrogen_p3`: "small yellowish green leaves" |
| 4 | Fewer tillers | exact | (reduced tillering) | tiller | `nitrogen.html`, `IRRI_RKB_nitrogen_p3`: "fewer tillers" |
| 5 | Fewer panicles per unit area [⚠ ambiguous] | **missing** | fewer panicles per area | field / stand (NEW) | `nitrogen.html`, `IRRI_RKB_nitrogen_p3`: "lower yield due to less panicles per unit area and less grains per panicle."<br>_Note: a count, not a look_ |

**Notes:**
- The sheet's only other visual statement is general: "Leaf color and crop appearance indicate the plant N status" (`nitrogen_p6`). It refers to the Leaf Color Chart fact sheet, which is not in the corpus.
- The tungro sheet says tungro yellowing and stunting "can be confused as nitrogen and zinc deficiencies and water stress" (`tungro_p16`). See §6.2.

### 3.8 Phosphorus_Deficiency_Disorder

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Dark_Green_Erect_Leaf` "dark green erect leaves" | IRRI phosphorus | phosphorus_p2 (human-reviewed) | leaf | IRRI phosphorus | phosphorus_p2 (LLM-reviewed) |
| `Delayed_Maturity` "delayed maturity" | IRRI phosphorus | phosphorus_p2 (human-reviewed) | whole plant | IRRI phosphorus | none |
| `Empty_Grain` "empty grain" | IRRI phosphorus | phosphorus_p2 (LLM-reviewed) | grain | IRRI rice-bug | rice-bug_p5 (human-reviewed) |
| `Reduced_Tillering` "reduced tillering" | IRRI phosphorus | phosphorus_p2 (LLM-reviewed) | tiller | IRRI tungro | tungro_p14 (human-reviewed) |
| `Stunted_Growth` "stunted growth" | IRRI phosphorus | phosphorus_p2 (LLM-reviewed) | whole plant | IRRI tungro | tungro_p14 (LLM-reviewed) |
| `Thin_Spindly_Stem` "thin, spindly stems" | IRRI phosphorus | phosphorus_p2 (human-reviewed) | stem | IRRI phosphorus | phosphorus_p2 (human-reviewed) |

**Inventory** (source: `phosphorus.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Stunted plants | exact | (stunted growth) | whole plant | `phosphorus.html`, `IRRI_RKB_phosphorus_p2`: "Stunted dark green plants with erect leaves and reduced tillering; thin and spindly stems; delayed maturity (and no flowering at all with severe P deficiency); and high levels of unfilled grains" |
| 2 | Dark green plants with erect leaves | exact | (dark green erect leaves) | leaf | `phosphorus.html`, `IRRI_RKB_phosphorus_p2`: "dark green plants with erect leaves" |
| 3 | Reduced tillering | exact | (reduced tillering) | tiller | `phosphorus.html`, `IRRI_RKB_phosphorus_p2`: "reduced tillering" |
| 4 | Thin and spindly stems | exact | (thin, spindly stems) | stem | `phosphorus.html`, `IRRI_RKB_phosphorus_p2`: "thin and spindly stems" |
| 5 | Delayed maturity [⚠ ambiguous] | exact | (delayed maturity) | whole plant | `phosphorus.html`, `IRRI_RKB_phosphorus_p2`: "delayed maturity"<br>_Note: temporal_ |
| 6 | No flowering when severe [⚠ ambiguous] | **missing** | no flowering | panicle | `phosphorus.html`, `IRRI_RKB_phosphorus_p2`: "no flowering at all with severe P deficiency"<br>_Note: an absence; visible only at the right stage_ |
| 7 | Unfilled grains | exact | (empty grain) | grain | `phosphorus.html`, `IRRI_RKB_phosphorus_p2`: "high levels of unfilled grains" |

**Note:** the sheet is one sentence, and the KG covers all of it except "no flowering".

### 3.9 Bacterial_Leaf_Blight

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Dry_Leaf_Tip` "Dry Leaf Tip" | CABI 56956 | none | leaf blade | IRRI bacterial-blight | none |
| `Leaf_Rolling` "Leaf Rolling" | CABI 56956 | none | leaf blade | IRRI rice-leaffolder | rice-leaffolder_p5 (LLM-reviewed) |
| `Wilting` "Wilting" | CABI 56956 | none | whole plant | IRRI bacterial-blight | bacterial-blight_p5 (human-reviewed) |
| `Yellow_Leaf` "Yellow Leaf" | CABI 56956 | none | leaf blade | IRRI tungro | tungro_p13 (LLM-reviewed) |

**Inventory** (source: `bacterial-blight.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Wilting of seedlings (kresek) | exact | (Wilting); altLabel 'kresek' | whole plant | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p5`: "Check for wilting and yellowing of leaves, or wilting of seedlings (also called kresek)." |
| 2 | Yellowing of leaves | exact | (Yellow Leaf) | leaf blade | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p1`: "It causes wilting of seedlings and yellowing and drying of leaves." |
| 3 | Drying of leaves | partial | leaf drying | leaf blade | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p1`: "yellowing and drying of leaves"<br>_Note: Dry Leaf Tip covers the tip only_ |
| 4 | Seedling leaves turn grayish green | **missing** | greyish-green seedling leaves | leaf | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p5`: "On seedlings, infected leaves turn grayish green and roll up." |
| 5 | Seedling leaves roll up | exact | (Leaf Rolling) | leaf blade | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p5`: "infected leaves turn grayish green and roll up" |
| 6 | Leaves turn yellow to straw-coloured and wilt | **missing** | straw-coloured leaves | leaf | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p5`: "As the disease progresses, the leaves turn yellow to straw-colored and wilt, leading whole seedlings to dry up and die." |
| 7 | Whole seedlings dry up and die | **missing** | seedling death | whole plant | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p5`: "leading whole seedlings to dry up and die" |
| 8 | Water-soaked to yellow-orange stripes on blades or tips | **missing** | water-soaked to yellow-orange stripe | leaf blade | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p7`: "On older plants, lesions usually develop as water-soaked to yellow-orange stripes on leaf blades or leaf tips or on mechanically injured parts of leaves."<br>_Note: this passage is the plant-part evidence of Yellow_Stripe, which is linked only to Downy_Mildew_ |
| 9 | Lesions have a wavy margin | **missing** | wavy lesion margin | leaf blade | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p7`: "Lesions have a wavy margin and progress toward the leaf base." |
| 10 | Lesions progress from tip toward leaf base | **missing** | lesion advancing from tip to leaf base | leaf blade | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p7`: "progress toward the leaf base"<br>_Note: progression_ |
| 11 | Milky dew-drop ooze on young lesions [sign] | **missing** | milky bacterial ooze droplets | leaf blade | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p8`: "On young lesions, bacterial ooze resembling a milky dew drop can be observed early in the morning."<br>_Note: early morning only_ |
| 12 | Dried ooze: small yellowish beads under the leaf [sign] | **missing** | dried yellowish ooze beads | leaf blade | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p8`: "The bacterial ooze later on dries up and becomes small yellowish beads underneath the leaf." |
| 13 | Old lesions yellow to grayish white with black dots | **missing** | greyish-white lesion with black dots | leaf blade | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p9`: "Old lesions turn yellow to grayish white with black dots due to the growth of various saprophytic fungi." |
| 14 | Lesions extend to the leaf sheath | **missing** | lesions on leaf sheath | leaf sheath | `bacterial-blight.html`, `IRRI_RKB_bacterial-blight_p9`: "On severely infected leaves, lesions may extend to the leaf sheath." |

**Notes:**
- **Yellow_Stripe:** its `affectsPlantPart` evidence is `bacterial-blight_p7`, which describes BLB stripes, but the symptom is linked only to Downy_Mildew.
  - Its comment ("Yellow to pale-green stripes running parallel to leaf veins; characteristic of downy mildew") does not describe the BLB stripe ("water-soaked to yellow-orange", "wavy margin").
  - Reusing it for BLB would merge two different looks.
- **Dry_Leaf_Tip → leaf blade:** cites the IRRI bacterial-blight sheet with no passage.

### 3.10 Bacterial_Leaf_Streak

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Translucent_Stripe` "translucent stripe" | CABI 56977 | none | leaf blade | IRRI bacterial-leaf-streak | bacterial-leaf-streak_p6 (LLM-reviewed) |
| `Water_Soaked_Streak` "water-soaked streak" | CABI 56977 | none | leaf blade | IRRI bacterial-leaf-streak | bacterial-leaf-streak_p5 (human-reviewed) |
| `Yellow_Leaf` "Yellow Leaf" | CABI 56977 | none | leaf blade | IRRI tungro | tungro_p13 (LLM-reviewed) |

**Inventory** (source: `bacterial-leaf-streak.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Browning and drying of leaves | **missing** | leaf browning and drying | leaf | `bacterial-leaf-streak.html`, `IRRI_RKB_bacterial-leaf-streak_p1`: "Infected plants show browning and drying of leaves." |
| 2 | Small, water-soaked, linear lesions | exact | (water-soaked streak) | leaf blade | `bacterial-leaf-streak.html`, `IRRI_RKB_bacterial-leaf-streak_p5`: "Symptoms initially appear as small, water-soaked, linear lesions between leaf veins." |
| 3 | Lesions between leaf veins | partial | interveinal streak | leaf blade | `bacterial-leaf-streak.html`, `IRRI_RKB_bacterial-leaf-streak_p5`: "linear lesions between leaf veins"<br>_Note: comment only_ |
| 4 | Streaks initially dark green | **missing** | dark green streak | leaf blade | `bacterial-leaf-streak.html`, `IRRI_RKB_bacterial-leaf-streak_p5`: "These streaks are initially dark green and later become light brown to yellowish gray." |
| 5 | Streaks later light brown to yellowish gray | partial | light brown to yellowish-grey streak | leaf blade | `bacterial-leaf-streak.html`, `IRRI_RKB_bacterial-leaf-streak_p5`: "later become light brown to yellowish gray"<br>_Note: comment of translucent stripe says 'yellow-brown'_ |
| 6 | Lesions translucent against the light | exact | (translucent stripe) | leaf blade | `bacterial-leaf-streak.html`, `IRRI_RKB_bacterial-leaf-streak_p6`: "The lesions are translucent when held against the light."<br>_Note: needs back-lighting_ |
| 7 | Entire leaves become brown and die | **missing** | whole leaf brown and dead | leaf | `bacterial-leaf-streak.html`, `IRRI_RKB_bacterial-leaf-streak_p6`: "Entire leaves may become brown and die when the disease is very severe." |
| 8 | Yellow droplets of bacterial ooze on leaves [sign] | **missing** | yellow bacterial ooze droplets | leaf blade | `bacterial-leaf-streak.html`, `IRRI_RKB_bacterial-leaf-streak_p7`: "Under humid conditions, yellow droplets of bacterial ooze, which contain masses of bacterial cells, may be observed on the surface of leaves."<br>_Note: humid conditions only_ |
| 9 | Lesions thinner than those of narrow brown spot | partial | narrow streak | leaf blade | `bacterial-leaf-streak.html`, `IRRI_RKB_bacterial-leaf-streak_p9`: "leaf streak lesions are usually thinner than those of narrow brown spot"<br>_Note: comment of translucent stripe says 'narrow'_ |

**Notes:**
- `Yellow Leaf` (CABI 56977) is not stated in the IRRI sheet, which mentions yellow only for the ooze and for "yellowish gray" streaks.
- The image captions read "Linear lesions \| Enlarged lesions \| Water-soaked lesions" (`bacterial-leaf-streak_p8`): a progression from narrow to enlarged lesions that no label carries.

### 3.11 Bacterial_Panicle_Blight — no IRRI fact sheet

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Discolored_Panicle` "discolored panicle" | CABI 44964 | none | panicle | IRRI brown-spot | none |
| `Empty_Grain` "empty grain" | CABI 44964 | none | grain | IRRI rice-bug | rice-bug_p5 (human-reviewed) |
| `Grain_Discoloration` "grain discoloration" | CABI 44964 | none | grain | IRRI brown-spot | brown-spot_p11 (human-reviewed) |
| `Wilting` "Wilting" | CABI 44964 | none | whole plant | IRRI bacterial-blight | bacterial-blight_p5 (human-reviewed) |

**Notes:**
- All four `indicatedBy` assertions cite CABI 44964 and have no passage.
- `Discolored_Panicle → panicle` cites the IRRI **brown-spot** sheet and has no passage. The brown-spot sheet describes brown spot on glumes and panicle branches, not bacterial panicle blight.
- See §4 and §6.4.

### 3.12 Stem_Borer

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Dead_Tiller` "dead tiller" | IRAC YSB, CABI 49009 | none | tiller | IRRI stem-borer | stem-borer_p8 (LLM-reviewed) |
| `Deadheart` "deadheart" | IRAC YSB | none | leaf | IRAC YSB | none |
| `Reduced_Tillering` "reduced tillering" | CABI 49009 | none | tiller | IRRI tungro | tungro_p14 (human-reviewed) |
| `White_Ear` "white ear" | IRAC YSB, CABI 49009 | none | panicle | IRRI stem-borer | stem-borer_p9 (LLM-reviewed) |

**Inventory** (source: `stem-borer.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Deadhearts (drying of the central tiller) | exact | (deadheart) | leaf (KG); central shoot | `stem-borer.html`, `IRRI_RKB_stem-borer_p2`: "They feed upon tillers and causes deadhearts or drying of the central tiller, during vegetative stage; and causes whiteheads at reproductive stage." |
| 2 | Whiteheads at reproductive stage | exact | (white ear); altLabel 'whitehead' | panicle | `stem-borer.html`, `IRRI_RKB_stem-borer_p2`: "causes whiteheads at reproductive stage" |
| 3 | Dead tillers | exact | (dead tiller) | tiller | `stem-borer.html`, `IRRI_RKB_stem-borer_p8`: "Deadhearts or dead tillers that can be easily pulled from the base during the vegetative stages"<br>_Note: 'easily pulled' is a test, not a look_ |
| 4 | Emerging panicles whitish and unfilled or empty | **missing** (reuse `Empty_Grain`?) | (empty grain) | panicle, grain | `stem-borer.html`, `IRRI_RKB_stem-borer_p9`: "Whiteheads during reproductive stage where the emerging panicles are whitish and unfilled or empty"<br>_Note: white ear covers 'whitish'_ |
| 5 | Tiny holes on stems and tillers | **missing** | bore holes in stem | stem, tiller | `stem-borer.html`, `IRRI_RKB_stem-borer_p9`: "Tiny holes on the stems and tillers" |
| 6 | Frass inside damaged stems [sign] | **missing** | frass inside stem | stem | `stem-borer.html`, `IRRI_RKB_stem-borer_p10`: "Frass or fecal matters inside the damaged stems"<br>_Note: visible only when the stem is opened_ |
| 7 | Larvae and pupae inside stems [sign] | **missing** | larva inside stem | stem | `stem-borer.html`, `IRRI_RKB_stem-borer_p11`: "Stems can be pulled and dissected for larvae and pupae for confirmation of stem borer damage."<br>_Note: dissection_ |
| 8 | Fewer reproductive tillers | exact | (reduced tillering) | tiller | `stem-borer.html`, `IRRI_RKB_stem-borer_p13`: "Its damage can reduce the number of reproductive tillers." |
| 9 | Egg masses on lower parts of the plant [sign] | **missing** | egg mass on leaf | leaf | `stem-borer.html`, `IRRI_RKB_stem-borer_p16`: "At seedbed and transplanting, handpick and destroy egg masses"<br>`stem-borer.html`, `IRRI_RKB_stem-borer_p16`: "submerge the eggs deposited on the lower parts of the plant"<br>_Note: stated in the management section_ |
| 10 | Larvae in leaf-wrapping tubes [sign] | **missing** | larval leaf tube | leaf | `stem-borer.html`, `IRRI_RKB_stem-borer_p4`: "Second instar larvae enclose themselves in body leaf wrappings to make tubes and detach themselves from the leaf and falls onto the water surface."<br>_Note: yellow stem borer_ |

**Notes:**
- **Scope:**
  - The IRRI sheet covers yellow, white, striped, gold-fringed and pink stem borers.
  - `Stem_Borer` is Scirpophaga incertulas (yellow stem borer) by its comment and `exactMatch` NCBITaxon_72366.
  - Rows 1–8 are stated for stem borers in general; row 10 is stated for the yellow stem borer.
  - The pink stem borer's "bare eggs between the leaf sheath and the stem" (`stem-borer_p6`) is left out, because that species is out of scope.
- **Deadheart → leaf** cites IRAC, with no passage. IRRI says "drying of the central tiller" (`stem-borer_p2`), which points to tiller rather than leaf; see §6.4.

### 3.13 Downy_Mildew — no IRRI fact sheet

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Excessive_Tillering` "excessive tillering" | CABI 49243 | none | tiller | CABI 49243 | none |
| `Sterile_Panicle` "sterile panicle" | CABI 49243 | none | panicle | IRRI tungro | tungro_p14 (LLM-reviewed) |
| `Stunted_Growth` "stunted growth" | CABI 49243 | none | whole plant | IRRI tungro | tungro_p14 (LLM-reviewed) |
| `Yellow_Stripe` "yellow stripe" | CABI 49243 | none | leaf blade | IRRI bacterial-blight | bacterial-blight_p7 (human-reviewed) |

**Notes:**
- All four `indicatedBy` assertions cite CABI 49243 and have no passage.
- `Yellow_Stripe → leaf blade` takes its evidence from the bacterial-blight sheet (see 3.9).
- See §4.

### 3.14 Hispa

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Brown_Leaf_Tip` "brown leaf tip" | CABI 27270 | none | leaf blade | IRRI rice-hispa | none |
| `Leaf_Scratching` "leaf scratching" | CABI 27270 | none | leaf blade | IRRI rice-hispa | rice-hispa_p5 (human-reviewed) |
| `White_Streak` "white streak" | CABI 27270 | none | leaf blade | IRRI rice-hispa | rice-hispa_p5 (human-reviewed) |

**Inventory** (source: `rice-hispa.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Upper leaf surface scraped, lower epidermis left | exact | (leaf scratching) | leaf blade | `rice-hispa.html`, `IRRI_RKB_rice-hispa_p1`: "Rice hispa scrapes the upper surface of leaf blades leaving only the lower epidermis."<br>_Note: 'scrapes' in the source, 'scratching' in the KG_ |
| 2 | White streaks parallel to the midrib, between veins | exact | (white streak) | leaf blade | `rice-hispa.html`, `IRRI_RKB_rice-hispa_p5`: "scraping of the upper surface of the leaf blade leaving only the lower epidermis as white streaks parallel to the midrib"<br>`rice-hispa.html`, `IRRI_RKB_rice-hispa_p9`: "white streaks of uneaten lower epidermis between the parallel leaf veins"<br>_Note: orientation in comment only ('linear')_ |
| 3 | Larvae tunnel through leaf tissue (mines) | **missing** | leaf mine | leaf blade | `rice-hispa.html`, `IRRI_RKB_rice-hispa_p1`: "It also tunnels through the leaf tissues."<br>_Note: Hispa's own comment mentions mining; no symptom does_ |
| 4 | Irregular translucent white patches parallel to veins | **missing** | irregular translucent white patch | leaf blade | `rice-hispa.html`, `IRRI_RKB_rice-hispa_p6`: "irregular translucent white patches that are parallel to the leaf veins caused by tunneling of larvae through leaf tissue causes" |
| 5 | Withering of damaged leaves | **missing** | withered leaf | leaf | `rice-hispa.html`, `IRRI_RKB_rice-hispa_p7`: "withering of damaged leaves" |
| 6 | Whitish, membranous leaves | **missing** | whitish membranous leaf | leaf | `rice-hispa.html`, `IRRI_RKB_rice-hispa_p7`: "whitish and membranous leaves" |
| 7 | Field appears burnt [field] | **missing** | burnt-looking field | field / stand (NEW) | `rice-hispa.html`, `IRRI_RKB_rice-hispa_p7`: "Rice field appears burnt when severely infested." |
| 8 | Elongated, clear feeding marks | partial | elongated clear feeding mark | leaf blade | `rice-hispa.html`, `IRRI_RKB_rice-hispa_p9`: "elongated, clear feeding marks"<br>_Note: white streak is nearest_ |
| 9 | Insect present [sign] | **missing** | hispa beetle on leaf | leaf | `rice-hispa.html`, `IRRI_RKB_rice-hispa_p8`: "To confirm cause of damage, check for insect presence, and the characteristic feeding marks:"<br>_Note: the sheet does not describe the insect_ |

**Notes:**
- **Brown leaf tips:** the IRRI hispa sheet does not mention them. The word "brown" does not occur in the passages or in the raw HTML.
  - Yet `Brown_Leaf_Tip → leaf blade` cites `IRRI rice-hispa`, with no passage.
  - The `indicatedBy` assertion itself cites CABI 27270, which may support it.
  - See §6.4.

### 3.15 Leaf_Folder

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Leaf_Rolling` "Leaf Rolling" | CABI 14493 | none | leaf blade | IRRI rice-leaffolder | rice-leaffolder_p5 (LLM-reviewed) |

**Inventory** (source: `rice-leaffolder.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Leaf folded around the larva, margins tied | partial | folded leaf | leaf blade | `rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p1`: "Leaffolder caterpillars fold a rice leaf around themselves and attach the leaf margins together with silk strands."<br>_Note: Leaf Rolling: rolling is not folding_ |
| 2 | Silk strands joining the leaf margins [sign] | **missing** | silk strands on leaf | leaf blade | `rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p1`: "attach the leaf margins together with silk strands" |
| 3 | Longitudinal white, transparent streaks | **missing** (reuse `White_Streak`?) | longitudinal white transparent streak | leaf blade | `rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p1`: "They feed inside the folded leaf creating longitudinal white and transparent streaks on the blade."<br>`rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p5`: "longitudinal and transparent whitish streaks on damaged leaves"<br>_Note: White_Streak's comment ties it to hispa scraping; reuse needs a decision_ |
| 4 | Tubular folded leaves | partial | tubular folded leaf | leaf blade | `rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p5`: "tubular folded leaves"<br>_Note: Leaf Rolling is nearest_ |
| 5 | Leaf tips fastened to the basal part of the leaf | **missing** | leaf tip fastened to leaf base | leaf blade | `rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p6`: "leaf tips sometimes fastened to the basal part of leaf" |
| 6 | Field looks scorched, with many folded leaves [field] | **missing** | scorched-looking field | field / stand (NEW) | `rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p6`: "heavily infested fields appear scorched with many folded leaves" |
| 7 | Disc-shaped ovoid eggs, laid singly [sign] | **missing** | single disc-shaped egg | leaf | `rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p8`: "disc-shaped ovoid eggs laid singly," |
| 8 | Young larvae at the base of the youngest unopened leaves [sign] | **missing** | larva at base of young leaf | leaf | `rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p8`: "young larvae feeding on the base of the youngest unopened leaves," |
| 9 | Folded leaves enclosing larvae [sign] | partial | folded leaf with larva | leaf blade | `rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p8`: "folded leaves enclosing the feeding larvae, and" |
| 10 | Fecal matter present [sign] | **missing** | larval frass on leaf | leaf | `rice-leaffolder.html`, `IRRI_RKB_rice-leaffolder_p9`: "present fecal matter."<br>_Note: location not stated_ |

**Notes:**
- `Leaf Rolling` is shared with Bacterial_Leaf_Blight, but the two looks differ:
  - BLB seedling leaves "roll up";
  - leaffolder leaves are folded lengthwise and tied with silk ("tubular folded leaves").
- One individual for both makes Leaf_Folder's current symptom set a subset of BLB's (§6.2).

### 3.16 Normal_Health — no source, no symptoms

_No `indicatedBy` symptom._ See §5.

### 3.17 Brown_Planthopper

**KG now**

| KG symptom | indicatedBy source | evidence passage (indicatedBy) | plant part | part source | evidence passage (part) |
|---|---|---|---|---|---|
| `Hopper_Burn` "Hopper Burn" | CABI 36301 | none | whole plant | IRRI planthopper | planthopper_p9 (human-reviewed) |
| `Yellow_Leaf` "Yellow Leaf" | CABI 36301 | none | leaf blade | IRRI tungro | tungro_p13 (LLM-reviewed) |

**Inventory** (source: `planthopper.html`)

| # | Symptom in the source | In KG? | Proposed label | Plant part | Source file and quote |
|---|---|---|---|---|---|
| 1 | Hopperburn: leaves orange-yellow, then brown and dry; plant dies | partial | hopperburn (orange-yellow to brown, dry) | whole plant | `planthopper.html`, `IRRI_RKB_planthopper_p1`: "High population of planthoppers cause leaves to initially turn orange-yellow before becoming brown and dry and this is a condition called hopperburn that kills the plant."<br>_Note: Hopper Burn exists but has no comment; the colour sequence is nowhere in the KG_ |
| 2 | Yellowing of plants | partial | yellowing plant | whole plant | `planthopper.html`, `IRRI_RKB_planthopper_p9`: "The feeding damage caused by planthoppers results in the yellowing of the plants."<br>`planthopper.html`, `IRRI_RKB_planthopper_p6`: "hopperburn or yellowing, browning and drying of plant"<br>_Note: Yellow Leaf is asserted at leaf blade_ |
| 3 | Complete drying of plants | exact | (Hopper Burn) | whole plant | `planthopper.html`, `IRRI_RKB_planthopper_p9`: "At high population density, hopperburn or complete drying of the plants is observed." |
| 4 | Crescent-shaped white eggs in midrib or sheath [sign] | **missing** | crescent-shaped white eggs in midrib | midrib (NEW), leaf sheath | `planthopper.html`, `IRRI_RKB_planthopper_p5`: "crescent-shaped white eggs inserted into the midrib or leaf sheath" |
| 5 | White to brown nymphs [sign] | **missing** | planthopper nymphs | tiller | `planthopper.html`, `IRRI_RKB_planthopper_p5`: "white to brown nymphs" |
| 6 | Brown or white adults near the base of tillers [sign] | **missing** | planthoppers at tiller base | tiller | `planthopper.html`, `IRRI_RKB_planthopper_p6`: "brown or white adults feeding near the base of tillers"<br>_Note: 'white' adults: WBPH, see scope_ |
| 7 | Ovipositional marks [⚠ ambiguous] | **missing** | oviposition marks | leaf sheath | `planthopper.html`, `IRRI_RKB_planthopper_p7`: "ovipositional marks exposing the plant to fungal and bacterial infections"<br>_Note: appearance not described_ |
| 8 | Honeydew and sooty moulds at the plant base | **missing** | sooty mould at plant base | tiller, leaf sheath | `planthopper.html`, `IRRI_RKB_planthopper_p7`: "presence of honeydew and sooty molds in the bases of areas infected"<br>`planthopper.html`, `IRRI_RKB_planthopper_p8`: "To confirm hopperburn caused by planthoppers, check for the presence of sooty molds at the base of the plant."<br>_Note: IRRI's own test against bugburn_ |

**Notes:**
- **Scope:** the sheet covers the brown planthopper (BPH) and the white-backed planthopper (WBPH). "White adults" and the WBPH sentences (`planthopper_p11`) refer to WBPH.
- **Hopper_Burn** has no `rdfs:comment`, so the orange-yellow → brown → dry sequence is nowhere in the KG.
- **Indirect symptoms:** the sheet notes that BPH transmits ragged stunt and grassy stunt. Their symptoms are not BPH symptoms and are not listed.

## 4. Conditions without an IRRI fact sheet: proposed open sources (not fetched)

Nothing below has been fetched or added. Each source needs a licence check before any wording enters the text module. Under the current design, wording goes into a separate module under the source's licence, and the core holds facts and pointers.

| Condition | Current source in the KG | Proposed sources to check |
|---|---|---|
| Leaf_Scald | IRRI Rice Doctor (Lucid key), Scald page | (1) the same Rice Doctor key: one source for all three diseases if it has pages for them, licence to confirm; (2) CABI Compendium datasheet for *Microdochium albescens* / *M. oryzae*; (3) open-access papers on rice leaf scald (PMC, DOAJ search) |
| Downy_Mildew | CABI 49243 (*Sclerophthora macrospora*) | (1) the CABI datasheet already cited: add its URL and quote as a passage if the licence allows; (2) a Rice Doctor page for downy mildew or crazy top, if one exists; (3) open-access papers on *S. macrospora* in rice |
| Bacterial_Panicle_Blight | CABI 44964 (*Burkholderia glumae*) | (1) the CABI datasheet already cited; (2) the review by Ham, Melanson and Rush (2011, *Molecular Plant Pathology*) on *B. glumae* in rice, open-access status to confirm; (3) open-access field-symptom papers |
| Normal_Health | none | No symptom source is proposed, because the task rules out inventing symptoms. See §5 for what option (a) would need. |

**CABI Compendium:** check its reuse terms before quoting. The KG already cites its DOIs, so a facts-and-pointers link needs no wording.

### 4.1 Inventory from IRRI (2018) *Rice Diseases: Biology & Selected Management Practices* (added 2026-11-07)

**Source**
- **Book:** IRRI's online book at https://rice-diseases.irri.org, © 2018 IRRI, **CC BY-NC-SA 4.0** (licence link in the page footer).
- **Chapters:** Chapter 2 (foliar fungal diseases: leaf scald, downy mildew) and Chapter 4 (grain diseases: grain rot), as PDFs.

**Bacterial panicle blight = grain rot.** Chapter 4 says *Burkholderia glumae* and *B. gladioli* cause "a disease syndrome known as 'bacterial panicle blight' in the U.S", and: "In the United States, the disease is called bacterial panicle blight but in other countries the disease is known as grain rot."

**Passages**
- **Scope:** the introduction and the Symptoms subsection of each disease, cut into passages `IRRI_RD2018_*`.
- **Wording:** in `Text Modality/RiceMMKG_IRRI_RD2018_text.ttl`, CC BY-NC-SA 4.0.
- **Scripts:** `Text Modality/scripts/rd2018_to_text.py` and `rd2018_passages.py`.

Every quote below was checked as an exact substring of its passage.

**Not answered by this source:**
- **Question X11:** the only statement about yellowish lines along the veins concerns mature oospores and sits in the "Causal organism" subsection, outside the passages.
- **CABI-sourced downy mildew symptoms:** the book does not state stunting or excessive tillering, which the KG has from CABI.

#### Leaf_Scald

| # | Symptom in the source | In KG? | Label | Plant part | Passage and quote |
|---|---|---|---|---|---|
| LS1 | Zonate lesions starting from the leaf tip or edges | exact | (zonate leaf lesion) | Leaf_Blade | `IRRI_RD2018_leaf-scald_p4`: "The lesions are characterized by zonation starting from the leaf tip or edges"<br>_Note: tip/edge start is in the comment of Zonate_Leaf_Lesion_ |
| LS2 | Usually on mature leaves [⚠ ambiguous] | partial | — | Leaf | `IRRI_RD2018_leaf-scald_p4`: "and usually occur on mature leaves"<br>_Note: leaf age, not a look_ |
| LS3 | Lesions more or less oblong | **missing** | oblong leaf lesion | Leaf_Blade | `IRRI_RD2018_leaf-scald_p4`: "They are more or less oblong with light brown halos." |
| LS4 | Light brown halo around the lesion | **missing** | light brown halo around lesion | Leaf_Blade | `IRRI_RD2018_leaf-scald_p4`: "They are more or less oblong with light brown halos."<br>_Note: brown spot has a yellow halo (Yellow_Lesion_Halo)_ |
| LS5 | Lesions 1-5 cm long, 0.5-1 cm wide (up to 25 cm) | **missing** | leaf lesion 1-5 cm long | Leaf_Blade | `IRRI_RD2018_leaf-scald_p4`: "Individual lesions are 1-5 cm long, 0.5-1 cm wide."<br>`IRRI_RD2018_leaf-scald_p4`: "lesions as long as 25 cm have been observed" |
| LS6 | Lesions enlarge and coalesce | **missing** (reuse `Coalescing_Leaf_Lesions`) | (coalescing leaf lesions) | Leaf_Blade | `IRRI_RD2018_leaf-scald_p4`: "The continuous enlargement and coalescing of lesions may result in blight on a large part of the leaf blade" |
| LS7 | A large part of the leaf blade dies | **missing** | large dead area of the leaf blade | Leaf_Blade | `IRRI_RD2018_leaf-scald_p4`: "may result in blight on a large part of the leaf blade"<br>_Note: label avoids 'blight' and 'scald' (condition names)_ |
| LS8 | Zonation fades with age; lesion without zonation = leaf tip drying | **missing** (reuse `Dry_Leaf_Tip`) | (Dry Leaf Tip) | Leaf_Blade | `IRRI_RD2018_leaf-scald_p4`: "The zonation fades as the lesions become old."<br>`IRRI_RD2018_leaf-scald_p4`: "Lesion without distinct zonation is called leaf tip blight in Japan, and leaf tip drying in China" |
| LS9 | Small, scattered reddish-brown spots with indistinct margin | **missing** | small scattered reddish-brown flecks | Leaf_Blade | `IRRI_RD2018_leaf-scald_p5`: "In Japan, brown leaf blight typically shows small, scattered, reddish-brown spots without necrotic tissues and with an indistinct margin."<br>`IRRI_RD2018_leaf-scald_p6`: "small, reddish-brown spots on the leaves (brown leaf blight)"<br>_Note: regional report (Japan, Korea); only occasionally in the tropics. Label avoids 'brown spot'_ |
| LS10 | Large brown patches on the leaf sheath | **missing** | large brown patches on leaf sheath | Leaf_Sheath | `IRRI_RD2018_leaf-scald_p5`: "Leaf sheath browning is characterized by relatively large patches of brown lesions without necrosis and indistinct margins."<br>_Note: regional report (Japan); only occasionally in the tropics; easily confused with other diseases_ |
| LS11 | Long, elliptical or rectangular, purplish-brown or light grey lesions | **missing** | long elliptical purplish-brown or light grey lesion | Leaf_Blade | `IRRI_RD2018_leaf-scald_p6`: "long, elliptical or rectangular, purplish-brown or light grey were also described"<br>_Note: regional report (Korea); the sentence names no organ, leaf assumed from context_ |
| LS12 | Lesions on the panicle neck, like the sheath lesions | **missing** | brown patch on panicle neck | Panicle_Neck | `IRRI_RD2018_leaf-scald_p6`: "Lesions on the neck of the panicles, similar to those on the leaf sheath, have also been observed"<br>_Note: regional report (Korea)_ |
| LS13 | Sterility in a head blight | **missing** (reuse `Sterile_Panicle`) | (sterile panicle) | Panicle | `IRRI_RD2018_leaf-scald_p6`: "De Gutierrez (1960) reported a head blight causing considerable sterility, flower deformation and discoloration of glumes in Costa Rica."<br>_Note: regional report (Costa Rica)_ |
| LS14 | Flower deformation | **missing** | deformed florets | Panicle | `IRRI_RD2018_leaf-scald_p6`: "flower deformation"<br>_Note: regional report (Costa Rica)_ |
| LS15 | Discoloration of glumes | **missing** (reuse `Grain_Discoloration`) | (grain discoloration) | Grain | `IRRI_RD2018_leaf-scald_p6`: "discoloration of glumes"<br>_Note: regional report (Costa Rica)_ |
| LS16 | Decay of coleoptiles with red-brown infection | **missing** | red-brown coleoptile decay | Coleoptile | `IRRI_RD2018_leaf-scald_p6`: "She described the fungus as causing decay of coleoptiles with red brown infection and root rot."<br>_Note: regional report (Costa Rica)_ |
| LS17 | Root rot | **missing** | root rot | Root | `IRRI_RD2018_leaf-scald_p6`: "and root rot"<br>_Note: regional report (Costa Rica); not visible above ground_ |
| LS18 | Grains infected [⚠ ambiguous] | partial | — | Grain | `IRRI_RD2018_leaf-scald_p6`: "indicated that the grains were infected"<br>_Note: no look described_ |

#### Downy_Mildew

| # | Symptom in the source | In KG? | Label | Plant part | Passage and quote |
|---|---|---|---|---|---|
| DM1 | Chlorotic whitish spots or patches on new leaf blades | **missing** (reuse `Chlorotic_Leaf_Patch`) | (chlorotic leaf patches) | Leaf_Blade | `IRRI_RD2018_downy-mildew_p3`: "In the earlier stage of the disease, new leaves of infected plants produce chlorotic whitish spots or patches on the leaf blades, sometimes reducing them in size."<br>_Note: Chlorotic_Leaf_Patch is so far a salinity symptom; its label is generic_ |
| DM2 | Leaf blades reduced in size | **missing** | reduced leaf size | Leaf_Blade | `IRRI_RD2018_downy-mildew_p3`: "sometimes reducing them in size" |
| DM3 | Fluffy white to grey fungal growth on the leaf underside [sign] | **missing** | — | Leaf_Blade | `IRRI_RD2018_downy-mildew_p3`: "At times, fluffy white to grey fungal growth may be seen on the under surface of the leaf blades."<br>_Note: sign of the pathogen (decision M4)_ |
| DM4 | White fungal coating on young shoots and seeds [sign] | **missing** | — | Tiller, Grain | `IRRI_RD2018_downy-mildew_p3`: "Infected young shoots and seeds may also show white coating of fungal growth."<br>_Note: sign (M4)_ |
| DM5 | Leaves distorted or twisted | **missing** | distorted or twisted leaf | Leaf | `IRRI_RD2018_downy-mildew_p4`: "In severe cases, the leaves may be distorted or twisted."<br>_Note: severe cases_ |
| DM6 | Panicles irregular, partly emerged from the sheath | **missing** (reuse `Incompletely_Exserted_Panicle`) | (small, incompletely exserted panicle) | Panicle | `IRRI_RD2018_downy-mildew_p4`: "The panicles appear irregular, partially emerged from the leaf sheath freely and become contorted and, sometimes, spiral (DM Figure 1)."<br>_Note: the source also says the panicle is reduced in size_ |
| DM7 | Panicles contorted, sometimes spiral | **missing** | contorted or spiral panicle | Panicle | `IRRI_RD2018_downy-mildew_p4`: "become contorted and, sometimes, spiral" |
| DM8 | Leaf sheath twisted | **missing** | twisted leaf sheath | Leaf_Sheath | `IRRI_RD2018_downy-mildew_p4`: "The leaf sheath may also be twisted." |
| DM9 | Floral parts turned into twisted tubular structures | **missing** | florets turned into twisted tubes | Panicle | `IRRI_RD2018_downy-mildew_p4`: "The emerged panicle is reduced in size with part of its floral parts modified into twisted tubular structures and usually remains green longer than normal." |
| DM10 | Panicle stays green longer than normal | **missing** | panicle staying green longer than normal | Panicle | `IRRI_RD2018_downy-mildew_p4`: "usually remains green longer than normal" |
| DM11 | Symptoms more pronounced at flowering [⚠ ambiguous] | partial | — | Panicle | `IRRI_RD2018_downy-mildew_p4`: "The symptoms are more pronounced at flowering time."<br>_Note: timing_ |

#### Bacterial_Panicle_Blight

| # | Symptom in the source | In KG? | Label | Plant part | Passage and quote |
|---|---|---|---|---|---|
| GR1 | Small tan lesions 1-5 mm with brown margins on leaf blades, especially flag leaves | **missing** | small tan leaf lesion with brown margin | Leaf_Blade | `IRRI_RD2018_grain-rot_p3`: "On leaf blades, especially flag leaves, the disease appears as small tan lesions measuring 1 to 5 mm with brown margins." |
| GR2 | Sheath lesion several cm long, tan centre, reddish-brown margin | **missing** | long sheath lesion with tan centre and reddish-brown margin | Leaf_Sheath | `IRRI_RD2018_grain-rot_p3`: "On the leaf sheath, the lesion may be several centimeters long with a tan center and reddish brown margins on individual flag leaf sheaths of infected tillers." |
| GR3 | Kernel abortion before filling | exact | (empty grain) | Grain | `IRRI_RD2018_grain-rot_p3`: "Infection occurs on spikelets causing kernel abortion before the kernels are completely filled."<br>_Note: already linked (CABI)_ |
| GR4 | Florets with dark grey or brown bases | **missing** | floret with dark grey or brown base | Panicle | `IRRI_RD2018_grain-rot_p3`: "Infected florets may show dark gray or brown bases, but the rachis of the panicles remains green." |
| GR5 | Panicle rachis stays green | **missing** | panicle rachis staying green | Panicle | `IRRI_RD2018_grain-rot_p3`: "but the rachis of the panicles remains green" |
| GR6 | Panicles stay erect instead of bending | **missing** | panicle staying erect at maturity | Panicle | `IRRI_RD2018_grain-rot_p3`: "Panicles of infected tillers remain erect instead of bending due to loss of grain weight." |
| GR7 | Brown lesions on the coleoptile of seedlings | **missing** | brown coleoptile lesion | Coleoptile | `IRRI_RD2018_grain-rot_p4`: "The symptoms on seedlings caused by inoculum from rotting seeds usually develop into brown lesions on the coleoptile (Uematsu et al 1976a,b), which can cause seedling mortality."<br>_Note: nursery boxes_ |
| GR8 | Seedling mortality | **missing** (reuse `Seedling_Death`) | (seedling death) | Whole_Plant | `IRRI_RD2018_grain-rot_p4`: "which can cause seedling mortality" |
| GR9 | Brown, water-soaked soft rot of the leaf sheath (seedlings) | **missing** | brown water-soaked soft rot of leaf sheath | Leaf_Sheath | `IRRI_RD2018_grain-rot_p4`: "Lesions on infected and developed seedlings show brown, water-soaked soft rot of the leaf sheath accompanied by wilting or soft rot of the leaves (GnR Figure 1)." |
| GR10 | Wilting | exact | (Wilting) | Whole_Plant | `IRRI_RD2018_grain-rot_p4`: "accompanied by wilting or soft rot of the leaves"<br>_Note: already linked (CABI)_ |
| GR11 | Soft rot of the leaves | **missing** | soft rot of leaves | Leaf | `IRRI_RD2018_grain-rot_p4`: "accompanied by wilting or soft rot of the leaves" |
| GR12 | Panicles shrunken, pale green, then dirty yellow to brown and dry | partial | shrunken panicle turning dirty yellow to brown | Panicle | `IRRI_RD2018_grain-rot_p5`: "On grain rot, the panicles are shrunken and pale green, becoming dirty yellow to brown and dry."<br>_Note: Discolored_Panicle is broader_ |
| GR13 | Hulls fade from the base: greenish white, then pale pink to yellowish brown | **missing** | grain hull fading from the base | Grain | `IRRI_RD2018_grain-rot_p5`: "The hulls of infected grains on young panicles rapidly fade in color from the base, turning greenish white at first and then pale pink to yellowish brown." |
| GR14 | Grains sterile, or brown rice with dark-brown discoloration at the base | exact | (empty grain; grain discoloration) | Grain | `IRRI_RD2018_grain-rot_p5`: "The infected grains are either sterile or carry brown rice with dark-brown discoloration at the base."<br>_Note: already linked (CABI)_ |
| GR15 | Brown margin between infected and healthy parts of the grain (diagnostic) | **missing** | brown boundary line across the grain | Grain | `IRRI_RD2018_grain-rot_p5`: "A brown margin between the infected and healthy parts of the grain is a diagnostic feature of the disease (GnR Figure 2)."<br>_Note: the source calls it diagnostic_ |
| GR16 | Mild rot of the flag leaf sheath at the collar [⚠ ambiguous] | **missing** | — | Leaf_Sheath | `IRRI_RD2018_grain-rot_p5`: "The bacterium may cause mild rot of the flag leaf sheath of the leaf sheath collar."<br>_Note: wording unclear_ |
| GR17 | Seeds fail to germinate (damping off) in nursery boxes [⚠ ambiguous] | **missing** | — | Grain | `IRRI_RD2018_grain-rot_p4`: "Preemergence “damping off” causes GnR where the seeds fail to germinate"<br>_Note: an absence, nursery boxes_ |


## 5. Normal_Health: two modelling options (not decided)

**Constraint found in the ontology:**
- `rice:indicatedBy` has domain `Disease ⊔ Pest` and range `Symptom`.
- `HealthStatus`, `Disease`, `Pest` and `Symptom` are members of one `owl:AllDisjointClasses` axiom.
- So `Normal_Health indicatedBy X` would make Normal_Health a Disease or Pest. HermiT would report the ontology inconsistent.
- Neither option can therefore simply reuse `indicatedBy`.

**Current state:**
- The comment of Normal_Health says its lack of symptoms "is semantically meaningful, not an omission".
- The benchmark scripts already hard-code at least four different stand-ins for it:
  - `step1_question.py`: `"healthy rice plant with no symptoms"`;
  - `stage1_baselines.py` and `zsl_dev.py`: `"a photo of a healthy rice plant"`;
  - `step2_rerank.py`: `"healthy plant, no symptoms"` in the prompt and the mean idf in the score.

### (a) A new property or individual for normal appearance

**What it means:**
- a new class, e.g. `rice:PlantAppearance`, kept out of `Symptom`, or added to the disjointness axiom as a separate class;
- a new object property, e.g. `rice:hasTypicalAppearance`, with domain `HealthStatus` and range that class;
- individuals such as a typical leaf colour or habit per growth stage, each with `dcterms:source` from a citable description.

**Consequences:**
- **Version:** MINOR bump (new class and property) and a provenance axiom on every assertion. CQ-21 and CQ-22 check every domain assertion, so the new ones must pass.
- **Comment:** the Normal_Health comment has to be rewritten. Its "absence of assertions" stance would no longer hold.
- **Benchmark:** no effect until the scripts read the new property; today they read only `indicatedBy`. The zero-shot multi-hot vector gets new columns used by one class only.
- **Sources:** needs a source for normal appearance. IRRI has no such sheet; the Leaf Color Chart sheet that `nitrogen_p6` refers to is the closest IRRI candidate, not fetched. Without a source this becomes invented content.
- **Overlap:**
  - A positive description such as "green, upright leaves" overlaps with the nutrient disorders: P is "dark green … erect leaves", K is "dark green plants".
  - Under the open-world assumption, having a normal appearance does not exclude a disease.
- **Variant (a′):** widen the domain of `indicatedBy` to include HealthStatus. This changes what `Symptom` means ("indicates the presence of a Disease or Pest"). Through the `hasAffectedPart` chain it would also give Normal_Health affected parts. Listed for completeness.

### (b) No KG change; a fixed prompt in the benchmark script

**What it means:**
- one constant prompt for Normal_Health, defined once and imported by every script, in place of the four stand-ins above;
- the prompt is stated in the paper as a benchmark design choice, not KG content.

**Consequences:**
- **KG:** no change, no version bump, and the "absence is meaningful" stance is kept.
- **Claims:** Normal_Health is the only class whose text does not come from the KG. Any "the KG helps" claim must report it separately or exclude it.
- **Tuning:** to avoid tuning, the prompt must be fixed before a run, not chosen on dev. Today the scripts use different texts, so they are not comparable for this class.
- **Field:** the KG cannot then answer "what does a healthy plant look like" for the field.

## 6. Flags

### 6.1 Conditions with no IRRI sheet

- Leaf_Scald, Downy_Mildew, Bacterial_Panicle_Blight and Normal_Health, as expected. Sources for the first three are proposed in §4.
- **Nutrient disorders:** they have IRRI sheets, but each sheet is one sentence of symptoms, and the KG already covers it (K: 6 of 8 exact, P: 6 of 7, N: 3 of 5).
  - The IRRI inventory cannot add visual detail for N, P or K.
  - Any more would need another source. The handbook "Rice: Nutrient disorders & nutrient management" (Dobermann and Fairhurst 2000) is cited by the IRRI iron-toxicity and salinity sheets (`iron-toxicity_p18`); its licence must be checked.
  - This is noted because the sheets are short, not because of benchmark scores.

### 6.2 Pairs that stay indistinguishable

The comparison is by script and uses symptom labels.
- **Scenario:** all rows tagged as symptom or field are added; partial rows add their proposed label; "reuse" rows add the existing individual (the worst case for overlap).
- **Scope "all":** a pair whose whole symptom sets are equal or nested.
- **Other scopes:** a pair whose symptoms on one part group are identical. The groups are leaf, sheath, panicle/grain and plant/stand.

**Now (KG as it is):**

| Condition A | Condition B | Scope | Relation | Shared symptoms |
|---|---|---|---|---|
| Brown_Spot | Rice_Blast_Disease | leaf | identical | brown lesion, leaf spot |
| Brown_Spot | Rice_Blast_Disease | sheath | identical | brown lesion |
| Brown_Spot | Bacterial_Leaf_Blight | plant/stand | identical | wilting |
| Brown_Spot | Bacterial_Panicle_Blight | plant/stand | identical | wilting |
| Rice_Tungro_Disease | Nitrogen_Deficiency_Disorder | plant/stand | identical | reduced tillering, stunted growth |
| Potassium_Deficiency_Disorder | Phosphorus_Deficiency_Disorder | panicle/grain | identical | empty grain |
| Bacterial_Leaf_Blight | Bacterial_Panicle_Blight | plant/stand | identical | wilting |
| Bacterial_Leaf_Blight | Leaf_Folder | all | Leaf_Folder ⊂ Bacterial_Leaf_Blight | leaf rolling |

**After all proposed additions:**

| Condition A | Condition B | Scope | Relation | Shared symptoms |
|---|---|---|---|---|
| Brown_Spot | Rice_Blast_Disease | sheath | identical | brown lesion |
| Brown_Spot | Bacterial_Panicle_Blight | all | Bacterial_Panicle_Blight ⊂ Brown_Spot | discolored panicle, empty grain, grain discoloration, wilting |
| Brown_Spot | Bacterial_Panicle_Blight | panicle/grain | identical | discolored panicle, empty grain, grain discoloration |
| Brown_Spot | Bacterial_Panicle_Blight | plant/stand | identical | wilting |
| Potassium_Deficiency_Disorder | Phosphorus_Deficiency_Disorder | panicle/grain | identical | empty grain |

**Reading:**
1. **Blast and brown spot on leaves are no longer identical** once shape, halo, early colour and size are added. On the sheath both keep only `Brown Lesion`: IRRI says blast affects the sheath "sometimes", but describes no sheath lesion.
2. **Bacterial_Panicle_Blight stays inside Brown_Spot.**
   - Brown spot gains `Empty_Grain`, and its glume spots reuse `Discolored_Panicle`, so every BPB symptom becomes a brown spot symptom.
   - If a new label is used for the glume spots, BPB keeps only `discolored panicle` as its own symptom.
   - Either way, BPB cannot be separated until it has its own source (§4).
3. **K and P share only `empty grain` on the panicle.** This is expected; their whole sets differ.
4. **Not caught by label comparison: pairs the IRRI sheets themselves call look-alikes.** Their labels differ, but the sheets say they look the same, or can be told apart only by a test:

| Pair | Source quote | Separator stated by IRRI | Visual? |
|---|---|---|---|
| Bacterial_Leaf_Blight vs Bacterial_Leaf_Streak | `bacterial-leaf-streak_p11`: "Blight and streak symptoms look the same at the early stage of infection, particularly if lesions of both diseases occur on the same leaf." | "Tests (i.e., biochemical, pathogenicity, or serological)" | No, at the early stage |
| Rice_Blast_Disease (neck/node) vs Stem_Borer (whiteheads) | `blast-node-neck_p8`: "Neck and node blast can also cause whiteheads or white panicles, similar to stem borer infection." | Pull test (`blast-node-neck_p9`, `p10`); a neck or node lesion is visible for blast only | Partly: the lesion |
| Bacterial_Leaf_Blight (kresek) vs Stem_Borer | `bacterial-blight_p6`: "Kresek on seedlings may sometimes be confused with early rice stem borer damage." | Squeeze test for ooze; kresek plants "are not easily pulled out from soil" | No |
| Rice_Tungro_Disease vs Nitrogen_Deficiency_Disorder | `tungro_p16`: "the yellowing of the plant and its stunted height can be confused as nitrogen and zinc deficiencies and water stress," | Serology (`tungro_p18`); "yellow or orange-yellow" vs "yellowish green" | Weak: colour shade only |
| Rice_Tungro_Disease vs Potassium_Deficiency_Disorder | `potassium-k_p3`: "leaf symptoms of K deficiency can be confused with that of Tungro disease" | Tungro "occurs in patches in a field" and has "more pronounced yellow and orange leaves and plant stunting" | Field scale only |
| Sheath_Blight vs Stem_Borer (and stem rot) | `sheath-blight_p10`: "Sheath blight has symptoms similar to stem rot and stemborer infestation." | Irregular sheath lesions; sclerotia | Yes |
| Hispa vs Leaf_Folder | Both sheets: white streaks along the leaf (`rice-hispa_p5`, `rice-leaffolder_p1`) | Leaf folding and silk (leaffolder); scraping and mines (hispa) | Yes, if `White_Streak` is not shared |

### 6.3 Ambiguous, non-visual or test-only statements

These are excluded from the tables (or tagged ⚠ there). Every quote was checked against its passage. No statement about smell occurs in these sheets.

| Condition | Passage | Quote | Kind | Why not in the tables |
|---|---|---|---|---|
| Brown_Spot | `IRRI_RKB_brown-spot_p13` | "On average, the disease causes 5% yield loss across all lowland rice production in South and Southeast Asia." | non-visual | yield |
| Brown_Spot | `IRRI_RKB_brown-spot_p14` | "Heavily infected seeds cause seedling blight and lead to 10−58% seedling mortality." | ambiguous | 'seedling blight' is not described; mortality is a rate |
| Brown_Spot | `IRRI_RKB_brown-spot_p14` | "It also affects the quality and the number of grains per panicle, and reduces the kernel weight." | non-visual | quality, count, weight |
| Rice_Blast_Disease | `IRRI_RKB_blast-leaf-collar_p9` | "At later growth stages, a severe leaf blast infection reduces leaf area for grain fill, reducing grain yield." | non-visual | yield |
| Rice_Blast_Disease | `IRRI_RKB_blast-node-neck_p7` | "if infection occurs later, poor quality grains are formed." | ambiguous | quality not described |
| Rice_Blast_Disease | `IRRI_RKB_blast-node-neck_p10` | "With neck and node blast, tugging on the stem will not result in removal." | test | pull test |
| Rice_Tungro_Disease | `IRRI_RKB_tungro_p10` | "they can die rapidly after transplanting." | ambiguous | seedling death, not specific |
| Rice_Tungro_Disease | `IRRI_RKB_tungro_p15` | "In varieties that carry some resistance to the disease, infected plants exhibit no discoloration or only a mild discoloration that may disappear as the plants mature." | ambiguous | modifier: symptoms may be absent |
| Rice_Tungro_Disease | `IRRI_RKB_tungro_p18` | "Where available, Tungro can be confirmed using serological tools such as Latex agglutination test, Enzyme Linked Immunosorbent Assays (ELISA) and Rapid Immunofilter Paper Assays (RIPA)." | test | serology |
| Sheath_Blight | `IRRI_RKB_sheath-blight_p2` | "the leaf area of the canopy can significantly be reduced by the disease." | ambiguous | canopy-level, not a look |
| Sheath_Blight | `IRRI_RKB_sheath-blight_p9` | "its dispersal is essentially dependent on hyphae running on plant tissues and producing new infections" | ambiguous | hyphae: a sign, appearance not described |
| Potassium_Deficiency_Disorder | `IRRI_RKB_potassium-k_p3` | "leaf symptoms often appear in late growth stages" | ambiguous | timing |
| Potassium_Deficiency_Disorder | `IRRI_RKB_potassium-k_p3` | "lower grain weight" | non-visual | weight |
| Nitrogen_Deficiency_Disorder | `IRRI_RKB_nitrogen_p6` | "Leaf color and crop appearance indicate the plant N status and help determine the need for N fertilizer application." | ambiguous | general; no specific symptom |
| Bacterial_Leaf_Blight | `IRRI_RKB_bacterial-blight_p6` | "Kresek symptoms should show yellowish bacterial ooze coming out of the cut ends. Unlike plants infested with stem borer, rice plants with kresek are not easily pulled out from soil." | test | squeeze and pull tests |
| Bacterial_Leaf_Blight | `IRRI_RKB_bacterial-blight_p11` | "after a few minutes, hold the container against light and observe for thick or turbid liquid coming from the cut end of the leaf" | test | glass-of-water test |
| Bacterial_Leaf_Blight | `IRRI_RKB_bacterial-blight_p14` | "When plants are infected at booting stage, bacterial blight does not affect yield but results in poor quality grains and a high proportion of broken kernels." | non-visual | milled-grain quality |
| Bacterial_Leaf_Streak | `IRRI_RKB_bacterial-leaf-streak_p10` | "When the advancing part of the streaks are cut and placed in a glass with water, a mass of bacterial cells can usually be seen oozing out of the leaf, which makes the water turbid after five minutes." | test | glass-of-water test |
| Bacterial_Leaf_Streak | `IRRI_RKB_bacterial-leaf-streak_p1` | "this could lead to reduced grain weight due to loss of photosynthetic area." | non-visual | weight |
| Hispa | `IRRI_RKB_rice-hispa_p1` | "When damage is severe, plants become less vigorous." | ambiguous | vigour not described |
| Leaf_Folder | `IRRI_RKB_rice-leaffolder_p10` | "The damage caused by leaffolders may be important when it affects more than half of the flag leaf and the next two youngest leaves in each tiller." | ambiguous | damage threshold, not a symptom |
| Brown_Planthopper | `IRRI_RKB_planthopper_p15` | "For older rice plants, grasp the plant, bend it over slightly, and gently tap it near the base to see if planthoppers fall onto the water surface." | test | tap test (scouting) |

### 6.4 KG issues found along the way (not fixed)

1. **`Brown_Leaf_Tip → leaf blade`** cites `IRRI rice-hispa`, but that sheet never mentions browning (§3.14).
2. **`Brown_Lesion → leaf blade`** cites `IRRI blast-leaf-collar` with no passage. That sheet describes lesions with whitish to grey centres and a "red to brownish" border, not brown lesions.
3. **`Discolored_Panicle → panicle`** cites `IRRI brown-spot` with no passage. The symptom is linked only to Bacterial_Panicle_Blight.
4. **`Yellow_Stripe → leaf blade`** takes its evidence from the BLB passage (`bacterial-blight_p7`), but Yellow_Stripe is linked only to Downy_Mildew, and its comment describes a different stripe.
5. **`Deadheart → leaf`** (IRAC): IRRI says "drying of the central tiller", which suggests tiller. The domain expert's definition in the comment ("the youngest, innermost leaf whorl") fits leaf.
6. **Symptoms with no `rdfs:comment`:** `Brown_Lesion`, `Leaf_Spot`, `Wilting`, `Yellow_Leaf`, `Dry_Leaf_Tip`, `Leaf_Rolling`, `Hopper_Burn`, `Chewed_Leaf`. They are the most generic labels and the most shared ones.
7. **Shared symptoms:** `affectsPlantPart` is asserted per symptom, not per condition–symptom pair, so a shared individual gives the same part to every condition that uses it.
   - `Wilting`'s whole-plant part comes from the BLB sheet and applies to blast, brown spot, sheath blight and BPB.
   - `Empty_Grain`'s part comes from the rice-bug sheet.
   - Reusing individuals in phase 2 extends this.
8. **Scope mismatches:** the Stem_Borer and Brown_Planthopper sheets cover several species (§3.12, §3.17).

## 7. Summary

### 7.1 Visual symptoms stated by IRRI and their KG status

| Condition | Visual items stated by IRRI | exact | partial | missing: symptom or field | missing: sign | missing: ambiguous | of which reuse an existing individual |
|---|---:|---:|---:|---:|---:|---:|---:|
| Brown_Spot | 17 | 2 | 4 | 11 | 0 | 0 | 2 |
| Leaf_Scald | no IRRI sheet | – | – | – | – | – | – |
| Rice_Blast_Disease | 15 | 1 | 5 | 9 | 0 | 0 | 1 |
| Rice_Tungro_Disease | 15 | 4 | 1 | 8 | 1 | 1 | 2 |
| Sheath_Blight | 10 | 1 | 3 | 5 | 1 | 0 | 0 |
| Potassium_Deficiency_Disorder | 8 | 6 | 1 | 1 | 0 | 0 | 0 |
| Nitrogen_Deficiency_Disorder | 5 | 3 | 1 | 0 | 0 | 1 | 0 |
| Phosphorus_Deficiency_Disorder | 7 | 6 | 0 | 0 | 0 | 1 | 0 |
| Bacterial_Leaf_Blight | 14 | 3 | 1 | 8 | 2 | 0 | 0 |
| Bacterial_Leaf_Streak | 9 | 2 | 3 | 3 | 1 | 0 | 0 |
| Bacterial_Panicle_Blight | no IRRI sheet | – | – | – | – | – | – |
| Stem_Borer | 10 | 4 | 0 | 2 | 4 | 0 | 1 |
| Downy_Mildew | no IRRI sheet | – | – | – | – | – | – |
| Hispa | 9 | 2 | 1 | 5 | 1 | 0 | 0 |
| Leaf_Folder | 10 | 0 | 3 | 3 | 4 | 0 | 1 |
| Normal_Health | no IRRI sheet | – | – | – | – | – | – |
| Brown_Planthopper | 8 | 1 | 2 | 1 | 3 | 1 | 0 |
| **Total** | **137** | **35** | **25** | **56** | **17** | **4** | **7** |

Reading:
- **Missing in total:** 77 items: 56 symptom or field rows, 17 signs and 4 ambiguous rows. 7 of the 77 could reuse an existing individual.
- **Partial:** 25 more items are only partly covered. Most are details that sit in an `rdfs:comment` but not in a label.
- **Most missing symptoms:** brown spot (11), blast (9), tungro (8) and BLB (8).
- **Few missing:** the nutrient disorders (0–1 each), because their IRRI sheets are one sentence long.
- **Four conditions** have no IRRI sheet.

### 7.2 Pairs still indistinguishable after the additions

- **Bacterial_Panicle_Blight ⊂ Brown_Spot.** BPB is identical to brown spot on panicle and grain, and on whole plant (`wilting`). It stays so until BPB has its own source.
- **Brown_Spot = Rice_Blast_Disease on the leaf sheath** (`brown lesion` only).
- **K = P on panicle and grain** (`empty grain` only). Their whole sets differ.
- **Look-alikes by the source's own statement** (§6.2, table): BLB vs BLS at the early stage, neck/node blast vs stem borer whiteheads, kresek vs stem borer, and tungro vs N deficiency. IRRI separates these by tests or by field pattern, not by a visual feature of the leaf.

### 7.3 Open questions for the maintainer

- **M1. Granularity:** one composite symptom per lesion description (e.g. "circular to oval lesion with grey centre and reddish-brown margin"), or atomic features (shape, centre, margin, halo, size)? Composite phrases suit CLIP prompts; atomic features suit the information-gain question route.
- **M2. Label or comment:** the benchmark reads labels only. Should details move from comments into labels or new individuals, or should the benchmark also read comments?
- **M3. Reuse or new individuals:** reuse `Empty_Grain`, `Grain_Discoloration`, `Discolored_Panicle`, `Delayed_Maturity` and `White_Streak`, or create condition-specific individuals? Reuse spreads plant parts across conditions (§6.4.7) and creates the BPB ⊂ brown spot overlap.
- **M4. Signs:** model ooze, sclerotia, eggs, insects, frass, silk and sooty mould as `Symptom`, or as a new class (e.g. `rice:Sign`) with its own property? The current definition of `Symptom` covers signs "on the plant", not the organism.
- **M5. New plant parts:** coleoptile, leaf collar, node, glume, panicle branch, spikelet, midrib. Check them against the Planteome register (`Analysis and Alignment/Planteome_alignment.md`) before adding.
- **M6. Field-scale patterns:** "patches", "burnt" and "scorched" are about the stand, not a plant part. Model them, and if so with which part?
- **M7. Ambiguous rows:** include the 4 ambiguous rows and the §6.3 items (temporal, absence, count), or exclude them?
- **M8. Scope:** Stem_Borer (yellow stem borer only) and Brown_Planthopper (BPH only) against sheets that cover several species.
- **M9. KG issues:** fix the four provenance issues in §6.4 (items 1–4) in phase 2, as a PATCH before the MINOR bump or within it?
- **M10. Sources:** which sources to use for the three diseases without a sheet (§4), and whether to add a fuller nutrient-disorder source (§6.1). Licences have to be checked first.
- **M11. Normal_Health:** option (a) or (b) (§5).

### 7.4 Open questions for the domain expert

- **X1. Blast and brown spot:** IRRI gives both a grey centre and a reddish or brownish margin. Are shape and the yellow halo the reliable separators in the field? Is "evenly brown" right for brown spot?
- **X2. CABI-sourced symptoms:** IRRI does not state `Wilting` for blast and sheath blight, `Brown Lesion` and `Leaf Spot` for blast, or `Yellow Leaf` for BLS. Are these right in the field?
- **X3. Hispa:** are brown leaf tips a symptom of hispa?
- **X4. BLB and BLS:** is there any visual separator at the early stage?
- **X5. Tungro and N deficiency:** is there a separator beyond patchiness and colour shade?
- **X6. Whiteheads:** without pulling the stem, can stem borer whiteheads be told from neck blast by the neck lesion alone?
- **X7. Hispa and leaffolder streaks:** the same symptom, or two?
- **X8. Signs:** which signs are visible in ordinary farmer photos (morning ooze, sclerotia, eggs, sooty mould)?
- **X9. Healthy plants:** only if option (a) is chosen, how would a normal plant be described by growth stage, and from which source?
- **X10. Brown leaf tips (added 0.8.1):** do hispa-damaged leaves show brown tips on the leaf blade, and which readable source states it? The plant part was removed in 0.8.1: the IRRI hispa sheet does not mention browning, and the CABI datasheet (27270) could not be read.
- **X11. Downy mildew stripes (added 0.8.1):** do the yellow to pale-green stripes of downy mildew appear on the leaf blade, and which readable source states it? The plant part was removed in 0.8.1: its only passage described bacterial blight stripes, and the CABI datasheet (49243) could not be read.
