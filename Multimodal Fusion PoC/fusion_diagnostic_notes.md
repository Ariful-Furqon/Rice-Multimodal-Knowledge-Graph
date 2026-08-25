# Multimodal fusion — diagnostic findings

Companion notes for `fusion_diagnostic.py`. Written to be presented directly.

**Run:**

```bash
python fusion_diagnostic.py --rdf "Ontology/Rice MMKG.rdf" --data Data/PaddyDoctor
```

Parts 1, 2 and 4 need only `rdflib` and complete in seconds. Part 3 needs `torch`, `torchvision`, `pillow` and the image files; it is skipped cleanly if they are absent, so the graph-side diagnosis is always available.

All figures below were produced against the current ontology (64,990 triples, 43,784 URI–URI). **Last run: 2026-08-21.**

---

## The question being tested

The proof-of-concept concluded that fusion works mechanically but produced a uniformly high similarity matrix (0.73–0.93), and attributed that to insufficient tuning — too few TransE epochs, a generic ImageNet encoder.

That attribution is testable, and it turns out to be incomplete. Tuning is not the binding constraint.

---

## Finding 1 — The graph contains ten distinct images, not 10,407

Two images are indistinguishable to any embedding model if their triples are identical. Grouping all 10,407 image individuals by their outgoing URI-to-URI assertions gives:

| Distinct structural signatures | **10** |
|---|---|
| Images per signature | 1,041 on average |
| What distinguishes them | the `annotatedAs` target, and nothing else |

| Signature | Images |
|---|---|
| `annotatedAs = Normal_Health` | 1,764 |
| `annotatedAs = Rice_Blast_Disease` | 1,738 |
| `annotatedAs = Hispa` | 1,594 |
| `annotatedAs = Deadheart` | 1,442 |
| `annotatedAs = Rice_Tungro_Disease` | 1,088 |
| `annotatedAs = Brown_Spot` | 965 |
| `annotatedAs = Downy_Mildew` | 620 |
| `annotatedAs = Bacterial_Leaf_Blight` | 479 |
| `annotatedAs = Bacterial_Leaf_Streak` | 380 |
| `annotatedAs = Bacterial_Panicle_Blight` | 337 |

**What this means.** A graph embedding can place at most one distinct point per signature. Ten thousand images collapse onto ten positions, and those positions *are* the labels. The graph half of the fused vector encodes the annotation label and nothing further.

More epochs cannot change this. The information is not in the graph to be learned.

**The consequence that matters most.** The PoC's stated next step is to evaluate the fused representation on disease classification. Under the current graph that evaluation is circular: the target variable is one of the inputs. Accuracy would approach 100% for a trivial reason, and the result would be **label leakage**.

This is much better caught now than in review.

---

## Finding 2 — The properties that would fix this are declared and empty

Part 2 groups every property asserted on image individuals by how many distinct values it takes:

| Property | Assertions | Distinct values | Verdict |
|---|---|---|---|
| `rdf:type` | 20,814 | 2 | label-level only (2 values) |
| `annotatedAs` | 10,407 | 10 | label-level only |
| `contentUrl` | 10,407 | 10,407 | per-image signal |
| `rdfs:label` | 10,407 | 10,407 | per-image signal |
| `prov:wasDerivedFrom` | 10,407 | 1 | constant — no signal |
| `captures` | 1,442 | 1 | constant — no signal |

Only two properties vary per image, and both are identifiers rather than content.

Seventeen properties are declared but never asserted, including exactly the ones that would separate two images sharing a label: **`observationDate`**, **`severityScore`**, **`confidenceScore`**. A fourth candidate — location — is not modelled at all.

**This is the same gap the ontology review identified,** reached independently from the embedding side. That convergence is worth stating: the fusion experiment did not fail, it diagnosed.

---

## Finding 3 — The similarity range is a property of ResNet, not of fusion

Part 3 measures two things the original PoC did not.

**Norm imbalance.** A 64-dimensional TransE vector after 100 steps has a small norm (mean 0.547). A 512-dimensional ResNet penultimate feature is post-ReLU, non-negative, and much larger (mean 22.31). The graph's share of the squared norm is **0.062%**. Concatenating them without per-modality normalisation means cosine similarity over the result is determined almost entirely by the visual half.

**The missing control.** The script computes the same similarity matrix from the visual vectors alone and reports the maximum and mean absolute difference against the fused matrix:

| | Off-diagonal range |
|---|---|
| Fused | 0.731 – 0.930 |
| Visual-only | 0.732 – 0.931 |
| Graph-only | 0.111 – 0.553 |

Max \|fused − visual\| difference: **0.0006**. Mean: **0.0003**. The fused matrix is numerically indistinguishable from the visual-only matrix — the graph is present in the vector but absent from the result.

**Why 0.73–0.93 is not informative either way.** ResNet penultimate activations are non-negative, so cosine similarity between any two natural images is bounded well above zero. That range is what arbitrary image pairs produce. It is evidence of neither success nor failure, and should not be presented as either.

---

## Finding 4 — There is usable graph signal, at class level

The graph carries no per-image information, but it does relate the classes. Part 4 builds a class-similarity matrix from shared symptoms (`indicatedBy`) and shared environmental risk factors (`increaseRiskOf`).

Following domain graph enrichment, **9 of the 10 annotation targets now carry graph features** (with `Normal_Health` intentionally carrying zero disease features):

| Class | Graph features |
|---|---|
| `Bacterial_Leaf_Blight` | Excessive_Nitrogen, High_Humidity, Poor_Soil_Drainage, Dry_Leaf_Tip, Leaf_Rolling, Wilting, Yellow_Leaf |
| `Bacterial_Leaf_Streak` | High_Humidity, High_Temperature, Translucent_Stripe, Water_Soaked_Streak, Yellow_Leaf |
| `Bacterial_Panicle_Blight` | High_Humidity, High_Night_Temperature, High_Temperature, Discolored_Panicle, Empty_Grain, Grain_Discoloration, Wilting |
| `Brown_Spot` | High_Humidity, Low_Rainfall, Poor_Soil_Drainage, Brown_Lesion, Grain_Discoloration, Leaf_Spot, Wilting |
| `Deadheart` | Dense_Canopy, High_Humidity, High_Temperature, Dead_Tiller, Reduced_Tillering, White_Ear |
| `Downy_Mildew` | High_Humidity, Waterlogged_Soil, Excessive_Tillering, Sterile_Panicle, Stunted_Growth, Yellow_Stripe |
| `Hispa` | Dense_Canopy, High_Humidity, High_Temperature, Brown_Leaf_Tip, Leaf_Scratching, White_Streak |
| `Normal_Health` | *(none — intentionally healthy)* |
| `Rice_Blast_Disease` | High_Humidity, Low_Rainfall, Brown_Lesion, Leaf_Spot, Neck_Rot, Panicle_Blast, Wilting |
| `Rice_Tungro_Disease` | High_Temperature, Presence_of_Leafhopper_Vector, Reduced_Tillering, Stunted_Growth, Yellow_Leaf, Yellow_Orange_Discoloration |

From these, **34 non-zero similarity pairs** emerge (top pairs shown):

| Jaccard | Pair | Agronomic Rationale |
|---|---|---|
| **0.56** | `Brown_Spot` ↔ `Rice_Blast_Disease` | Shared: High_Humidity, Low_Rainfall, Brown_Lesion, Leaf_Spot, Wilting |
| **0.33** | `Deadheart` ↔ `Hispa` | Shared: Dense_Canopy, High_Humidity, High_Temperature |
| **0.27** | `Bacterial_Leaf_Blight` ↔ `Brown_Spot` | Shared: High_Humidity, Poor_Soil_Drainage, Wilting |
| **0.27** | `Bacterial_Panicle_Blight` ↔ `Brown_Spot` | Shared: High_Humidity, Grain_Discoloration, Wilting |
| **0.22** | `Bacterial_Leaf_Streak` ↔ `Deadheart` / `Hispa` / `Tungro` | Shared environmental & visual indicators |

**This is the graph's one testable prediction, and it is a good one.** The ontology says brown spot and blast share both of their recorded symptoms — brown lesions and leaf spots. It therefore predicts that a purely visual classifier will confuse those two classes more than any other pair.

That prediction can be checked against the confusion matrix of any CNN trained on the same ten classes. If it holds, the knowledge graph has demonstrably captured something real about the visual domain, derived from agronomy rather than from pixels.

---

## Two routes forward

### Route A — give the graph per-image content

Populate the properties that vary within a label: capture date, location, growth stage at capture, severity, and the specific symptoms visible in each image. Then two images of the same disease genuinely differ in the graph, image-level fusion becomes meaningful, and the leakage problem disappears because the graph no longer encodes the label alone.

Cost: this is data collection, not modelling. The 1,442 `Deadheart` images already carry a per-image `captures` assertion, which is a start, but it takes only one value.

### Route B — use the graph as a structured prior over classes

Do not embed the image individuals at all. Use the class-similarity matrix from Finding 4 to shape a visual classifier: as a cost-sensitive loss where confusing brown spot with blast is penalised less than confusing either with healthy, or as a regulariser on the classifier's output layer.

This needs no new data, uses precisely the agronomic knowledge already encoded, and has no leakage risk, because it relates labels to one another rather than identifying individual images.

**Route B is presentable now. Route A is the stronger long-term answer.** They are not alternatives — B is the interim result while A is being built.

---

## Suggested framing

> The proof-of-concept confirmed that graph and image representations join through a shared IRI without custom alignment logic. Diagnostic analysis then established that the graph currently distinguishes images only to the granularity of their annotation label — ten distinct structural signatures across 10,407 individuals — so image-level fusion cannot yet contribute information, and evaluating it on label prediction would constitute leakage. The properties that would carry per-image signal are declared in the schema and unpopulated. Class-level graph structure is usable today and yields one falsifiable prediction about visual confusability, which we test against a CNN confusion matrix.

That reads as a controlled finding rather than a failed experiment, which is what it is.

---

## Housekeeping

This diagnostic and `fusion_poc.py`'s `README.md` were both re-run against the current ontology on 2026-08-19: 64,662 total triples (up from an earlier 85,459 recorded in a prior draft of these notes, and up from the 31,634 in `README.md`'s original PoC run), 43,456 URI-to-URI triples, 10,564 entities, 22 relations. The property is `annotatedAs` (the PoC's `README.md` still called it `classifiedAs`); `README.md` has been updated to match. Re-run before presenting any number from this file, since the ontology is under active revision.

One methodological note for the re-run: the triple extraction feeds `rdf:type`, `rdfs:subClassOf`, `rdfs:domain`, `rdfs:range`, `owl:inverseOf` and `skos:exactMatch` into TransE alongside the domain assertions. Mixing schema axioms with facts is common practice but worth stating explicitly, since `rdf:type` alone accounts for 20,814 of the triples and will dominate the objective.
