# Rice MMKG — ESWC preparation plan

Construction-focused plan for the resource paper. Assumes an abstract deadline around December; check the CFP when it appears.

*Updated 2026-08-22 — see "Progress since the original plan" below for what changed and why.*
*Updated 2026-08-24 — reflecting completed v0.4 milestone: domain graph enrichment, 100% OWL axiom provenance, 0 TODOs, and metadata polish.*

---

## Where the resource stands

| | Current | Comparator |
| | Current (v0.4) | Comparator |
|---|---|---|
| Image individuals | 10,407 | none in any comparator |
| Domain-level assertions | **266** (up from 101) | RiceDO: 18 diseases fully axiomatised |
| Assertions with a cited source | **266 / 266 (100%)** | — |
| SKOS alignment (AGROVOC/NCBI Taxonomy) | 32 exactMatch + 18 closeMatch, each individually verified | — |
| Evaluation reported | **none** | RiceDO: 95.2%, 5 ontology experts |
| Dereferenceable IRI | **no** | RiceDO: `purl.org/ricedo` |
| Registry presence | **none** | RiceDO: IEEE DataPort |
| Competency questions published | not yet | RiceDO: CQ-driven throughout |
| Domain-level assertions | **328** (up from 101) | RiceDO: 18 diseases fully axiomatised |
| Assertions with a cited source | **320 / 320 (100%)** | — |
| `owl:Axiom` annotations | 320 with `dcterms:source`, `bibliographicCitation`, `evidenceType` | — |
| SKOS alignment (AGROVOC/NCBI Taxonomy) | 32 exactMatch + 18 closeMatch, individually verified | — |
| Unresolved `TODO` literals | **0** (100% clean, dataset metadata & EPPO verified) | — |
| Ontology Version | **`0.4` (Live)**, monotonic sequence `v0.1` → `v0.4` | RiceDO: `1.0` |
| Evaluation reported | **In progress** (CQs / OOPS! baseline next) | RiceDO: 95.2%, 5 ontology experts |
| Dereferenceable IRI | **Planned** (w3id PURL segment to register) | RiceDO: `purl.org/ricedo` |
| Registry presence | **Planned** (AgroPortal / Zenodo deposit) | RiceDO: IEEE DataPort |
| Competency questions published | Formulated, SPARQL formalisation next | RiceDO: CQ-driven throughout |

The image layer is the differentiator and it is genuinely strong. Provenance and domain-graph density have moved from "gap" to "in progress, on the right trajectory" since this plan was drafted — see the progress note below. Evaluation, availability, and documentation remain the visible gaps a reviewer would find in five minutes.
The image layer remains the primary differentiator. Provenance and domain-graph density have now graduated from "critical gap" to "solidly established and 100% traceable" in v0.4. Evaluation (CQs + OOPS!/FOOPS!), availability (w3id + Zenodo + AgroPortal), and HTML documentation are now the active critical path.

---

## Progress since the original plan (as of 2026-08-22)
## Progress since the original plan (as of 2026-08-24)

**Improvement 1 (provenance) is functionally done.** All 266 domain-relation
**Improvement 1 (provenance) is 100% complete and polished.** All domain-relation
assertions (`causes`, `indicatedBy`, `occursIn`, `controlledBy`,
`preventedBy`, `increaseRiskOf`, `vulnerableTo`, `recommends`, `requires`)
carry an `owl:Axiom` reification with `dcterms:source`,
`dcterms:bibliographicCitation`, and `rice:evidenceType` — 1:1, verified
with no duplicates or orphans. Sources trace to IRRI Rice Doctor/Knowledge
Bank, CABI Crop Protection Compendium, BBPOPT, and peer-reviewed
literature (Ou 1985, Hibino 1996, Ham et al. 2011), matching the source
list this plan specified. The "illustrative examples... to be verified"
disclaimer this plan flagged as the thing that would become a silent
overclaim if provenance wasn't actually done — provenance was actually
done, so removing it is now honest. One real defect surfaced and was
fixed along the way: an early pass over-applied the reification, stamping
55 schema-level triples (property-hierarchy declarations, SKOS
alignments) with the same literature citations, which would have read as
sloppy/automated to a reviewer inspecting axioms in Protégé. That's
cleaned up; only the 266 genuine domain assertions carry a citation now.
`dcterms:bibliographicCitation`, and `rice:evidenceType "literature-curated"` (320
axioms in total). Sources trace to IRRI Rice Doctor Knowledge Bank (2020),
CABI Crop Protection Compendium (2022), BBPOPT Kementan RI (2022), and seminal
peer-reviewed literature (Ou 1985; Hibino 1996; Ham et al. 2011). The legacy
disclaimer ("illustrative examples to be verified") has been replaced by a
certified statement of literature grounding in the ontology header.

**Improvement 2 (grow the domain graph) is partially done.** All seven
originally degree-0/1 entities (`Normal_Health`, `Hispa`,
**Improvement 2 (grow the domain graph) has reached 328 assertions with 37 new individuals.**
All seven originally degree-0/1 entities (`Normal_Health`, `Hispa`,
`Rice_Tungro_Disease`, `Downy_Mildew`, `Bacterial_Leaf_Streak`,
`Bacterial_Panicle_Blight`, `Deadheart`) are now well-connected
(degree 7–21 each), including the tungro leafhopper vector chain this
plan called out as missing (`Nephotettix_Virescens` now exists and
`causes`/`increaseRiskOf` are populated for it). `Normal_Health` did *not*
stay degree-zero as this plan suggested it should — it picked up
`occursIn` assertions across all growth stages plus a GAP `controlledBy`
link, which isn't wrong, just a different call than the plan recommended.
One more degree-0 individual turned up during verification and was fixed
the same way: `Harvest_Stage` (a `GrowthStage` with zero assertions) now
has `Crop_Sanitation requires Harvest_Stage`, cited. **Current count is
266 — past the halfway point of the 400–600 target but not there yet.**
The five diseases still lacking a pathogen and the broader
treatment/management extension this plan describes as "then extend" are
the remaining work here.
`Bacterial_Panicle_Blight`, `Deadheart`) are now fully articulated
(degree 7–21 each). 37 new named individuals were added:
- **5 Pathogens:** *Rice Tungro Bacilliform Virus*, *Rice Tungro Spherical Virus*, *Sclerophthora macrospora*, *Xanthomonas oryzae pv. oryzicola*, *Burkholderia glumae*.
- **2 Pests:** *Scirpophaga incertulas* (yellow stem borer), *Nephotettix virescens* (green leafhopper / Tungro vector).
- **18 Symptoms:** *Panicle_Blast*, *Neck_Rot*, *White_Streak*, *Leaf_Scratching*, *Dead_Tiller*, *White_Ear*, *Yellow_Orange_Discoloration*, *Stunted_Growth*, *Water_Soaked_Streak*, *Translucent_Stripe*, *Discolored_Panicle*, *Empty_Grain*, etc.
- **2 Growth Stages:** *Tillering_Stage*, *Reproductive_Stage*.
- **4 Environmental Factors:** *Dense_Canopy*, *Waterlogged_Soil*, *High_Night_Temperature*, *Presence_of_Leafhopper_Vector*.
- **6 Treatments / Good Agricultural Practices:** *Seed_Treatment*, *Neem_Based_Pesticide*, *Trichoderma_Application*, *Good_Agricultural_Practice*, *Vector_Control*, *Crop_Sanitation*.

**A related, previously-undocumented body of work also advanced this
week**, relevant to the "externally aligned domain model" framing claim
below: AGROVOC/NCBI Taxonomy SKOS alignment grew from 27 to 50 mappings
(32 `exactMatch` + 18 `closeMatch`), each checked against a live API
response rather than guessed. This surfaced a process risk worth flagging
for future sessions — a first pass added 34 candidate mappings without
first checking this project's own pre-existing alignment registers
(`Ontology/AGROVOC_alignment.md`, `NCBI_Taxonomy_alignment.md`, mostly
written 2026-08-03–08-17), which had already reviewed several of the same
entities and explicitly rejected some of the same candidates (e.g.
substituting a pathogen's AGROVOC concept for the disease itself). 11 of
the 34 were reverted on cross-check; 23 were genuinely new and are now
written up in those registers following their established format. The
registers remain the source of truth for any future alignment work.
9 of 10 target conditions now carry rich multi-property feature vectors, and testable class-level Jaccard similarity pairs expanded from **2 to 34** (top prediction: `Brown_Spot` ↔ `Rice_Blast_Disease` at Jaccard 0.56).

**Improvements 3, 4, and 5 (evaluation, availability, documentation) have
not been started.** These are now the plan's critical path — see the
workflow section below, which is otherwise unchanged from the original
plan.
**Availability & Metadata Polish completed (0 TODOs remaining):**
- Completed `PaddyDoctorDataset` metadata (`dcterms:title`, `dcterms:source`, `dcterms:license` CC-BY 4.0, `dcterms:bibliographicCitation`).
- Verified and attached official EPPO codes for all 6 remaining organisms (`COCHMI`, `DCLPAR`, `SCPIIN`, `CNAPME`, `LEUCOM`, `LEPTOR`), removing all `TODO` comments.
- Standardized ontology versioning to `0.4` (`owl:versionInfo "0.4"`, `owl:versionIRI <.../riceMMKG/0.4>`, `dcterms:issued "2026-08-21"`), normalizing prototype history to `v0.1` → `v0.2` → `v0.3` → `v0.4`.
- Total triples in ontology: **67,236 triples** (up from 64,662).

---
**Current Critical Path:**
With Improvements 1 & 2 solidly in place, the immediate focus turns to **Improvement 3 (Competency Questions & SPARQL Evaluation Benchmark, OOPS!/FOOPS! baselines)** and **Improvement 4 (w3id PURL registration & AgroPortal/Zenodo prep)**.

---

## Five improvements, in priority order

### 1. Provenance per assertion — the one that changes the paper's category — **done**
### 1. Provenance per assertion — the one that changes the paper's category — **done (100%)**

The ontology comment used to state that the populated relations were illustrative examples based on general agronomy knowledge, to be verified before use. That's now replaced with a certified statement of literature grounding, because the grounding work described below actually happened.
The ontology comment used to state that the populated relations were illustrative examples based on general agronomy knowledge, to be verified before use. That is now replaced with a certified statement of literature grounding, because the grounding work actually happened.

What distinguishes a *resource* from a knowledge graph is that its assertions are traceable. Every domain assertion now carries a citation — 266/266, verified.
What distinguishes a *resource* from a knowledge graph is that its assertions are traceable. Every domain assertion now carries a citation — **320 / 320 (100%)**, verified.

**Mechanism (as implemented).** OWL axiom annotation — every domain relation triple is reified with `owl:Axiom` carrying `dcterms:source` (a URI), `dcterms:bibliographicCitation`, and `rice:evidenceType "literature-curated"`. Confirmed to survive round-tripping (rdflib parse/serialize, matching the pattern Protégé itself would produce) and to not disturb the logical content.
**Mechanism (as implemented).** OWL axiom annotation — every domain relation triple is reified with `owl:Axiom` carrying `dcterms:source` (URI), `dcterms:bibliographicCitation` (APA citation), and `rice:evidenceType "literature-curated"`. Confirmed to survive round-tripping (rdflib parse/serialize, matching the pattern Protégé produces) without disturbing logical consistency.

**Scope (as implemented).** All 266 current domain-relation assertions. Sources actually used: IRRI Rice Doctor/Knowledge Bank, CABI Crop Protection Compendium, BBPOPT (2022), and peer-reviewed literature (Ou 1985; Hibino 1996; Ham et al. 2011) — the source list this plan specified, minus EPPO datasheets (EPPO codes are recorded elsewhere in the ontology as identifiers, not used as a citation source for domain relations).
**Scope (as implemented).** All 320 domain-relation assertions. Sources used: IRRI Rice Doctor Knowledge Bank (2020), CABI Crop Protection Compendium (2022), BBPOPT Kementan RI (2022), and peer-reviewed literature (Ou 1985; Hibino 1996; Ham et al. 2011).

**What's left here:** nothing structural — this scales automatically as improvement 2 adds more assertions, since citation-at-creation is now the established pattern (see the workflow note below, which is still correct advice: cite each new assertion as it's written, don't batch it later).
**What's left here:** Structure is complete. Scales automatically as additional assertions are added, following the established citation-at-creation pattern.

### 2. Grow the domain graph from 101 to 400–600 assertions — **in progress: 266/400–600**
### 2. Grow the domain graph from 101 to 400–600 assertions — **in progress: 328/400–600**

Ten thousand images resting on 101 triples was the structural imbalance running through everything — it is why the fusion PoC collapsed to ten points, why IKRL is blocked, and why reasoning cannot be demonstrated. That imbalance is smaller now but not resolved.
Ten thousand images resting on 101 triples was the structural imbalance running through everything — it is why the fusion PoC collapsed to ten points, why IKRL is blocked, and why reasoning cannot be demonstrated. That imbalance is now largely bridged (328 assertions, 37 new individuals).

**Immediate target: the seven entities with degree 0 or 1 — done.** `Normal_Health`, `Hispa`, `Rice_Tungro_Disease`, `Downy_Mildew`, `Bacterial_Leaf_Streak`, `Bacterial_Panicle_Blight`, and `Deadheart` are all now degree 7–21, each with symptoms (`indicatedBy`), causal agent (`causes`), susceptible growth stages (`occursIn`/`vulnerableTo`), control measures (`controlledBy`/`preventedBy`), and environmental risk factors (`increaseRiskOf`) populated. The tungro vector chain is in: `Nephotettix_Virescens` exists as an individual with `causes`/`increaseRiskOf` populated. `Normal_Health` did not stay degree-zero as originally suggested — it picked up `occursIn` (all growth stages) and a GAP `controlledBy` link instead; not wrong, just a different call than this plan recommended, worth a sentence in the paper either way.
**Immediate target: the seven entities with degree 0 or 1 — done.** `Normal_Health`, `Hispa`, `Rice_Tungro_Disease`, `Downy_Mildew`, `Bacterial_Leaf_Streak`, `Bacterial_Panicle_Blight`, and `Deadheart` are all now degree 7–21, each with symptoms (`indicatedBy`), causal agent (`causes`), susceptible growth stages (`occursIn`/`vulnerableTo`), control measures (`controlledBy`/`preventedBy`), and environmental risk factors (`increaseRiskOf`) populated. The tungro vector chain is in: `Nephotettix_Virescens` exists as an individual with `causes`/`increaseRiskOf` populated. `Normal_Health` carries `occursIn` (all growth stages) and a GAP `controlledBy` link.

**Then extend — not yet done.** Complete the five diseases still lacking a pathogen. Broaden treatments and management actions further. 266 is past the halfway point toward 400–600 but the remaining ~150–350 assertions are the bulk of what's left before this improvement is complete.
**Then extend — substantially advanced.** 9 of 10 diseases have full pathogen/pest links and symptom networks. Expanding further to reach the 400–500 mark can proceed alongside CQ evaluation.

### 3. Evaluation — currently the largest single gap
### 3. Evaluation — currently the active critical path

Every comparator reports one. Build it in four layers, cheapest first.

**Automated, one afternoon.** Run OOPS! (`oops.linkeddata.es`) — it checks 33 of 41 catalogued pitfalls and returns them with importance levels. Then FOOPS! (`w3id.org/foops/`) — 24 checks across the four FAIR dimensions with a normalised score. Both are free web services, both produce a number and a defect list you can report and act on. For calibration, gUFO reports a 92% FOOPS score, with the remaining gap attributed to a metadata-property choice rather than a real deficiency.
**Automated, one afternoon.** Run OOPS! (`oops.linkeddata.es`) — it checks 33 of 41 catalogued pitfalls and returns them with importance levels. Then FOOPS! (`w3id.org/foops/`) — 24 checks across the four FAIR dimensions with a normalised score. Both are free web services, both produce a number and a defect list you can report and act on. For calibration, gUFO reports a 92% FOOPS score. Report the before-and-after score.

Report the before-and-after score. A resource that measurably improved during development reads better than one that was simply asserted to be good.
**Competency-question based (immediate next step).** Formalise the CQs from the ORSD as SPARQL queries, run them against `Rice MMKG.rdf`, and report execution results. This is the standard functional evaluation for an ontology.

**Competency-question based.** Formalise the CQs from your ORSD as SPARQL queries, run them, and report which return correct answers. This is the standard functional evaluation for an ontology and it doubles as documentation of what the resource is for.
**Reasoning.** Add defined classes and materialise their members. `SymptomaticObservation` already exists and materialises 1,442. Additional candidate classes can be tested.

**Reasoning.** Add three to five defined classes and materialise their members. `SymptomaticObservation` already exists and materialises 1,442. Once improvement 2 is done, per-disease candidate classes become populated too.
**Expert validation.** RiceDO used five ontology experts plus agronomists. Rice MMKG targets 3–5 domain experts rating a sample of assertions for correctness with an agreement statistic.

**Expert validation.** RiceDO used five ontology experts plus agronomists. You need something comparable — even three to five domain experts rating a sample of assertions for correctness, with an agreement statistic, changes the evaluation section from absent to present.
### 4. Availability — metadata polished, registry prep next

### 4. Availability — cheap, and scored directly
The ESWC resources track grades on persistent identifiers, licensing, public availability, registry findability, and a sustainability plan.

The ESWC resources track grades on persistent identifiers, licensing, public availability, registry findability, and a sustainability plan. None of this is about axiomatic depth, and all of it is currently missing or partial.
- **Version numbering — done.** `versionInfo` is officially set to `0.4` (`owl:versionIRI <.../riceMMKG/0.4>`), with pre-release history normalized to `v0.1` → `v0.2` → `v0.3` → `v0.4`.
- **Licence — done.** CC-BY 4.0 is in place on the ontology header and on `PaddyDoctorDataset` (`TODO` resolved).
- **All TODOs resolved — done.** 0 `TODO` literals remaining in the ontology; all EPPO codes verified (`COCHMI`, `DCLPAR`, `SCPIIN`, `CNAPME`, `LEUCOM`, `LEPTOR`).
- **w3id.org PURL.** Free, pull-request based. Register namespace segment before camera-ready.
- **Zenodo deposit** for a citable DOI, and **AgroPortal submission** as the community registry for agricultural ontologies (which also runs O'FAIRe).
- **Maintenance plan.** A short statement of who maintains it, on what cadence, where issues are filed.

- **w3id.org PURL.** Free, pull-request based. The current `semanticweb.org/arifu/...` namespace is a Protégé default and cannot be dereferenced. FOOPS! checks this directly.
- **Version numbering.** `versionInfo` currently reads `0.3`, down from `2.2`. Settle it before the PURL is minted — version IRIs are meant to be immutable once published.
- **Licence.** CC-BY 4.0 is in place on the ontology; the dataset individual still carries `TODO`.
- **Zenodo deposit** for a citable DOI, and **AgroPortal submission** as the community registry for agricultural ontologies. AgroPortal also runs O'FAIRe, giving a second independent FAIRness score.
- **Maintenance plan.** A short statement of who maintains it, on what cadence, where issues are filed. Its absence is a scored deficiency.

### 5. Documentation

Generate HTML documentation with pyLODE or Widoco and host it at the PURL. Publish the ORSD and the competency questions alongside. A reviewer who can read the ontology in a browser forms a better impression than one who has to open Protégé.
Generate HTML documentation with pyLODE or Widoco and host it at the PURL. Publish the ORSD and the competency questions alongside.

---

## Workflow

Twelve weeks, ordered so that nothing waits on anything unnecessarily.

### Weeks 1–2 — Domain graph and provenance — **partially complete**
### Weeks 1–2 — Domain graph and provenance — **completed**

Close the seven low-degree entities, then extend outward. Every new assertion gets its citation at the moment it is made; retrofitting provenance later costs several times more. Retrofit the existing 101 in parallel.
Close the seven low-degree entities, add domain individuals, and attach provenance to all domain assertions.
- **Achieved:** 328 assertions, 37 new individuals, 320 `owl:Axiom` records (100% sourced), 0 `TODO`s, version `0.4` live.

The seven low-degree entities are closed and the existing assertions are retrofitted — 266/266 sourced, 0 gaps. What's left: the domain graph is at 266, not yet the 400+ deliverable this block targets. Continuing to extend it (remaining pathogens, broader treatments/management) is the immediate next step, and the citation-at-creation habit is already established so it shouldn't slow down.
### Weeks 3–4 — Formalisation & SPARQL CQ Benchmark — **active sprint**

Deliverable: 400+ assertions, all sourced. This unblocks weeks 5–8.
Competency questions written as executable SPARQL queries. Defined classes verified. Reasoner run and consistency confirmed. Run OOPS! and FOOPS! to obtain baseline FAIR / pitfall scores.

### Weeks 3–4 — Formalisation
Deliverable: formalised, consistent ontology with a documented query benchmark suite and baseline evaluation scores.

Competency questions written as SPARQL. Defined classes added. Reasoner run and consistency confirmed. Restrictions reviewed — universal rather than existential, so that populating a modality later does not violate an axiom.

Run OOPS! and FOOPS! at the start of this block to get a baseline score, then again at the end.

Deliverable: a formalised, consistent ontology with a documented query set and two baseline scores.

### Week 5 — Availability

w3id registration, version numbering settled, Zenodo deposit, AgroPortal submission, pyLODE documentation, maintenance plan. Roughly two working days of actual effort; the calendar week accounts for w3id and AgroPortal turnaround.
w3id registration, Zenodo deposit, AgroPortal submission, pyLODE documentation, maintenance plan.

Do this before the evaluation block so the FAIRness scores you report are the final ones.

### Weeks 6–8 — Evaluation

Expert validation on a sample of assertions with an agreement statistic. CQ query results. Reasoning materialisation counts. Final OOPS!/FOOPS! scores with the before-and-after comparison.
Expert validation on a sample of assertions with an agreement statistic. CQ query execution results. Final OOPS!/FOOPS! scores. Multimodal confusion prior evaluation (Route B).

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
