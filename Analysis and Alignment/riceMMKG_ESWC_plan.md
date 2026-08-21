# Rice MMKG — ESWC preparation plan

Construction-focused plan for the resource paper. Assumes an abstract deadline around December; check the CFP when it appears.

---

## Where the resource stands

| | Current | Comparator |
|---|---|---|
| Image individuals | 10,407 | none in any comparator |
| Domain-level assertions | **101** | RiceDO: 18 diseases fully axiomatised |
| Assertions with a cited source | **0** | — |
| Evaluation reported | **none** | RiceDO: 95.2%, 5 ontology experts |
| Dereferenceable IRI | **no** | RiceDO: `purl.org/ricedo` |
| Registry presence | **none** | RiceDO: IEEE DataPort |
| Competency questions published | not yet | RiceDO: CQ-driven throughout |

The image layer is the differentiator and it is genuinely strong. Everything else in this table is a gap a reviewer can see in five minutes.

---

## Five improvements, in priority order

### 1. Provenance per assertion — the one that changes the paper's category

The ontology comment currently states that the populated relations are illustrative examples based on general agronomy knowledge, to be verified before use. Left in place, that sentence tells a reviewer the assertions are unvalidated. Removed without doing the work, it becomes a silent overclaim.

What distinguishes a *resource* from a knowledge graph is that its assertions are traceable. Every domain assertion should carry a citation.

**Mechanism.** Use OWL axiom annotation — reify the axiom with `owl:Axiom` and attach `dcterms:source` (a DOI or IRI), `dcterms:bibliographicCitation`, and optionally a confidence or evidence-type note. This survives round-tripping through Protégé and reasoners, and does not disturb the logical content. RDF-star is more elegant but tooling support in the OWL ecosystem is still uneven.

**Scope.** All 101 existing assertions plus whatever is added in improvement 2. Sources: IRRI Rice Knowledge Bank, CABI Crop Protection Compendium, EPPO datasheets, and Indonesian sources such as BBPOPT for locally specific practice.

**Why this first.** It is the difference between "we built an ontology" and "we built a resource others can trust". It also converts your existing honesty about unverified relations from a liability into a documented method.

### 2. Grow the domain graph from 101 to 400–600 assertions

Ten thousand images resting on 101 triples is the structural imbalance running through everything — it is why the fusion PoC collapsed to ten points, why IKRL is blocked, and why reasoning cannot be demonstrated.

**Immediate target: the seven entities with degree 0 or 1.** `Normal_Health`, `Hispa`, `Rice_Tungro_Disease`, `Downy_Mildew`, `Bacterial_Leaf_Streak`, `Bacterial_Panicle_Blight` appear in no assertion at all; `Deadheart` appears in one. Six of these are among the classes with the most images.

For each of the ten annotation targets, assert: symptoms (`indicatedBy`), causal agent (`causes`), susceptible growth stages (`occursIn`), control measures (`controlledBy`), and environmental risk factors (`increaseRiskOf`). That is 40–60 triples and roughly doubles the domain graph on its own.

**Then extend.** Complete the five diseases still lacking a pathogen. Add the vector chain — tungro needs its leafhopper vector, which is not yet an individual. Broaden treatments and management actions. 400–600 well-sourced assertions is a defensible size for a single-crop resource.

`Normal_Health` will remain degree-zero and that is correct — a healthy plant has no symptoms or pathogens. Say so explicitly rather than leaving it looking incomplete.

### 3. Evaluation — currently the largest single gap

Every comparator reports one. Build it in four layers, cheapest first.

**Automated, one afternoon.** Run OOPS! (`oops.linkeddata.es`) — it checks 33 of 41 catalogued pitfalls and returns them with importance levels. Then FOOPS! (`w3id.org/foops/`) — 24 checks across the four FAIR dimensions with a normalised score. Both are free web services, both produce a number and a defect list you can report and act on. For calibration, gUFO reports a 92% FOOPS score, with the remaining gap attributed to a metadata-property choice rather than a real deficiency.

Report the before-and-after score. A resource that measurably improved during development reads better than one that was simply asserted to be good.

**Competency-question based.** Formalise the CQs from your ORSD as SPARQL queries, run them, and report which return correct answers. This is the standard functional evaluation for an ontology and it doubles as documentation of what the resource is for.

**Reasoning.** Add three to five defined classes and materialise their members. `SymptomaticObservation` already exists and materialises 1,442. Once improvement 2 is done, per-disease candidate classes become populated too.

**Expert validation.** RiceDO used five ontology experts plus agronomists. You need something comparable — even three to five domain experts rating a sample of assertions for correctness, with an agreement statistic, changes the evaluation section from absent to present.

### 4. Availability — cheap, and scored directly

The ESWC resources track grades on persistent identifiers, licensing, public availability, registry findability, and a sustainability plan. None of this is about axiomatic depth, and all of it is currently missing or partial.

- **w3id.org PURL.** Free, pull-request based. The current `semanticweb.org/arifu/...` namespace is a Protégé default and cannot be dereferenced. FOOPS! checks this directly.
- **Version numbering.** `versionInfo` currently reads `0.3`, down from `2.2`. Settle it before the PURL is minted — version IRIs are meant to be immutable once published.
- **Licence.** CC-BY 4.0 is in place on the ontology; the dataset individual still carries `TODO`.
- **Zenodo deposit** for a citable DOI, and **AgroPortal submission** as the community registry for agricultural ontologies. AgroPortal also runs O'FAIRe, giving a second independent FAIRness score.
- **Maintenance plan.** A short statement of who maintains it, on what cadence, where issues are filed. Its absence is a scored deficiency.

### 5. Documentation

Generate HTML documentation with pyLODE or Widoco and host it at the PURL. Publish the ORSD and the competency questions alongside. A reviewer who can read the ontology in a browser forms a better impression than one who has to open Protégé.

---

## Workflow

Twelve weeks, ordered so that nothing waits on anything unnecessarily.

### Weeks 1–2 — Domain graph and provenance

Close the seven low-degree entities, then extend outward. Every new assertion gets its citation at the moment it is made; retrofitting provenance later costs several times more. Retrofit the existing 101 in parallel.

Deliverable: 400+ assertions, all sourced. This unblocks weeks 5–8.

### Weeks 3–4 — Formalisation

Competency questions written as SPARQL. Defined classes added. Reasoner run and consistency confirmed. Restrictions reviewed — universal rather than existential, so that populating a modality later does not violate an axiom.

Run OOPS! and FOOPS! at the start of this block to get a baseline score, then again at the end.

Deliverable: a formalised, consistent ontology with a documented query set and two baseline scores.

### Week 5 — Availability

w3id registration, version numbering settled, Zenodo deposit, AgroPortal submission, pyLODE documentation, maintenance plan. Roughly two working days of actual effort; the calendar week accounts for w3id and AgroPortal turnaround.

Do this before the evaluation block so the FAIRness scores you report are the final ones.

### Weeks 6–8 — Evaluation

Expert validation on a sample of assertions with an agreement statistic. CQ query results. Reasoning materialisation counts. Final OOPS!/FOOPS! scores with the before-and-after comparison.

If the fusion work continues in parallel, the image-to-entity retrieval evaluation belongs here too — but it is a second contribution, not the resource evaluation, and the paper should not depend on it.

### Weeks 9–12 — Writing

Draft against the resource-track criteria explicitly: what the resource is, why it is needed, how it was built, how it was evaluated, where it lives, who maintains it, and who else could use it.

The comparison table and the RiceDO positioning are already written. The evaluation section is the one that does not exist yet, which is why weeks 6–8 cannot be compressed.

---

## Framing to settle early

The strongest available claim is not "a multimodal knowledge graph for rice". It is closer to:

> the first rice pest and disease ontology to link a large public image collection to a semantically grounded, externally aligned domain model, separating what was observed from what was concluded, with every domain assertion traceable to a cited source

That claim is defensible, it does not overstate the sensor and text modalities that remain unpopulated, and it explains why the artefact is a resource rather than a dataset with a schema attached.

**Complementarity with RiceDO, not competition.** RiceDO is more heavily axiomatised, published, and expert-evaluated. Its own evaluation asked whether it could be extended to cover symptom images — the experts agreed at 88%, and the authors named multimodal monitoring as future work. Rice MMKG occupies exactly that space. Saying so directly is stronger than any claim of superiority, and it pre-empts the comparison a reviewer would make anyway.

**Naming.** Until sensor and text modalities hold individuals, "image-anchored" is more defensible than "multimodal" in the title and abstract. The multimodal schema can still be presented as designed and extensible — that is a legitimate contribution — but the populated artefact should be described as what it is.

---

## What to keep out of scope

- SOSA/SSN alignment. Worth doing, likely valuable for an ESWC audience, but a deliberate design decision rather than something to fold into a deadline.
- Populating the sensor and text modalities. Without data, the classes stay declared and the naming stays image-anchored.
- IKRL implementation as a dependency of the resource paper. It is a separate contribution and it is blocked on improvement 2 anyway.
- Splitting `Xanthomonas_Oryzae` into pathovars, PATO symptom decomposition, taxonomic subclasses under `Disease`. All defensible, none load-bearing.
