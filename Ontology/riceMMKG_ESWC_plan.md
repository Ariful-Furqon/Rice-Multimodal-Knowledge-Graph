# Rice MMKG — Master Plan Toward ESWC 2027

Construction, evaluation, and publication roadmap for the **ESWC 2027 Resource Track**.  
**Current Milestone:** Rice MMKG **v0.6.1** (2026-09-14; v0.6 released 2026-09-03).  
**Abstract / Paper Deadline:** Late November – early December.  
**Plan revised:** 2026-09-14 — phases re-ordered and re-scoped; see §2.

> **Figures corrected 2026-09-14.** The v0.6 numbers first recorded in this plan (66,874 / 161,568 triples, 265 axioms, "100% cited") were measured before the v0.6 inconsistency fix. The released v0.6 file measures 66,780 / 161,416 triples with 253 axioms over 255 domain assertions. The snapshot below is v0.6.1.

> **Modality scope — open decision (2026-09-14).** The submission is **not** limited to text + image. Sensor data stays in the plan if it can be obtained, and expert feedback has raised **genomic** data as a further modality. Neither is decided yet: the decision point is in Phase 3. What is released today is a text-curated domain layer plus 10,407 image observations; `SensorObservation` is declared but empty, and no genomic entities exist. Whatever is decided, a declared-but-empty modality cannot be claimed as part of the resource. The CQ screening's Tier A / Tier B split (CQs without / with sensor or genomic requirements) stays as an instrument design, and the two tiers are never pooled into one agreement statistic.

---

## 1. Executive Summary & Resource Snapshot

| Metric / Dimension | Current State (v0.6.1) | Comparator (RiceDO) | Target for Submission |
|---|---|---|---|
| **Ontology Version** | **`0.6.1`** | `1.0` | `1.0` (release tagged for submission) |
| **Asserted Triples** | **66,802** | ~1,200 | Grows with symptom-level image grounding; no fixed triple target |
| **Materialised Triples (OWL RL)** | **161,447** (+94,645 triples) | — | Re-measured at release |
| **Modalities** | Populated: text-curated domain layer + **10,407** image observations. Declared but empty: `SensorObservation`. Not modelled: genomic | Text only | **Open — decided at the Phase 3 checkpoint.** Candidates: sensor (if data can be obtained), genomic (raised by expert feedback) |
| **Symptom-level image grounding** | `captures` on 1,442 images, all to one symptom (CQ-18: 1/27) | 0 | Multiple symptoms grounded from expert annotation (see Phase 3) |
| **Domain-Level Assertions** | **256 assertions, 256 reified axioms (100% cited)** | 18 diseases | 100% literature-grounded, checked by CQ-21 + extended CQ-22 |
| **Reasoner Consistency** | **Consistent (HermiT, 2026-09-14, with an injected-contradiction control)** | Verified | Consistent at release, re-checked after every schema change |
| **Competency Questions** | **25 benchmark CQs** (23 PASS / 1 PARTIAL / 0 FAIL / 1 DOC); **19 of 25 elicited CQs** queried (7 answer, 10 partial, 2 no answer) | Qualitative CQs | Both instruments re-run against the tagged v0.6 baseline |
| **Permanent URI (PURL)** | Local namespace (`.../riceMMKG#`) | `purl.org/ricedo` | `w3id.org/<segment>` live — **segment to confirm** (`ricemmkg` or `rice-mmkg`) |
| **FAIR Score (FOOPS!)** | 0.7275 (v0.5 schema-only baseline, 2026-08-22; main gap: no PURL) | — | **> 0.85**, measured once on the release |
| **Registry Findability** | GitHub repository | IEEE DataPort | **AgroPortal** entry + **Zenodo DOI** for the release |
| **Online Documentation** | Markdown documentation | — | **pyLODE / Widoco** at the PURL |
| **Expert Validation** | Stage 5 CQ questionnaire ready (25 items, Indonesian); 250-image annotation sample prepared | 5 experts (95.2%) | Returns analysed with weighted κ (2 raters) or ordinal Krippendorff's α (3+) |

---

## 2. Six-Phase Workflow Toward ESWC 2027

**Why the order changed (2026-09-14).** The original Phase 2 bundled everything FAIR-related into late September. Most of it — HTML documentation, the Zenodo DOI, AgroPortal, the FOOPS! score — describes a *finished* release, so doing it before the modality and schema work means redoing it. The exception is the **namespace**: every IRI is embedded in both SPARQL scripts, their reports, the questionnaire data, any new image annotations, embeddings, and the paper's examples, and w3id registration waits on an external pull-request review. That part gets *more* expensive the longer it waits, so it stays early; the rest moves to just before submission. Phase 3 now starts with the work that is needed whichever modalities are chosen (image grounding, literature-backed schema) and puts an explicit **modality checkpoint** on sensor and genomic data at its start, since those depend on data sources that are not yet secured.

Expert-facing work starts now even though its analysis comes later, because expert turnaround is the longest wait in the plan.

```
Phase 1: Functional & Reasoning Evaluation (Weeks 1–2, Sept) — [DONE: v0.6.1]
   ├── 25 benchmark CQs + automated runner, 4 evaluation modes            [DONE]
   ├── 25 elicited CQs (6 LLMs, screened, human-adjudicated), 19 queried   [DONE]
   ├── HermiT consistency + OWL RL materialisation                         [DONE]
   └── Frozen baseline: git tag elicited-baseline-v0.6                     [DONE]
          │
          ▼
Phase 2: Namespace & Release Scaffolding (Weeks 3–4, Sept: 15–28 Sep) — [NEXT]
   ├── Confirm w3id segment; open w3id.org pull request
   ├── Rewrite namespace as its own commit; re-run HermiT + both benchmarks
   ├── Close maintenance-plan TODOs (affiliation, release cadence)
   └── Send Stage 5 questionnaire + 250-image annotation sample to experts   (starts Phase 4 clock)
          │
          ▼
Phase 3: Modality Checkpoint, Grounding & Schema → v0.7 (Weeks 5–8: 29 Sep – 26 Oct)
   ├── Checkpoint (start of Phase 3): sensor and genomic — data source secured? in or roadmap?
   ├── Schema from literature: PlantPart, transmission mode, management category
   ├── Ingest expert image annotations: captures (more symptoms), organ, severity
   ├── If chosen: sensor and/or genomic module (schema + real data + CQs)
   ├── Re-run both CQ instruments against the v0.6 baseline tag
   └── Optional: embedding experiment across the populated modalities
          │
          ▼
Phase 4: Expert Validation & Analysis (returns by late Oct; analysis Weeks 9–10: 27 Oct – 9 Nov)
   ├── Stage 7 re-proposal rate wired into Stage 6 before returns are analysed
   ├── Stage 6: weighted κ / ordinal α, convergence vs relevance
   ├── Independent second screener on ~20% of Stages 1, 3, 4
   └── Tier B roadmap instrument, reported separately
          │
          ▼
Phase 5: Availability & FAIR Finalisation (Weeks 10–11: 3 – 16 Nov)
   ├── pyLODE / Widoco documentation at the PURL, content negotiation live
   ├── FOOPS! + OOPS! on the release
   └── Zenodo DOI + AgroPortal submission for the tagged release
          │
          ▼
Phase 6: Resource Paper & Submission (Weeks 11–14: mid Nov – early Dec)
   ├── Manuscript per ESWC Resource Track criteria
   ├── Reproducibility package (scripts un-ignored, runner, lockfile)
   └── Internal/advisor review and submission
```

---

## 3. Detailed Phase Breakdown & Deliverables

### Phase 1: Functional & Reasoning Evaluation — DONE
*Status: **v0.6.1 patch done 2026-09-14** (23/24 benchmark CQs passing, 0 FAIL; HermiT consistent with a verified control case).*

- **Completed:**
  1. 25 benchmark CQs across L1–L4 × D1–D3, executable runner with `coverage` / `negative` / `entailment` / `documented` modes, no `OPTIONAL` on mandatory hops.
  2. 25 elicited Tier A CQs from six LLMs, screened and human-adjudicated (`CQ Screening/`); 19 queried against the ontology, answerability measured rather than predicted.
  3. DL consistency (HermiT) and OWL RL materialisation.
  4. v0.6.1: `Nephotettix_Virescens controlledBy Resistant_Variety` (not the planned `Vector_Control`, which FAO and IRRI do not support for tungro), `@en` on the one untagged `evidenceType`, provenance axioms for the two unreified `Stem_Borer indicatedBy` assertions found by the extended CQ-22; `provenance_axioms.rdf` archived; CABI sources moved to DOIs with Crossref citations.
- **Deliverables:** `cq_sparql_benchmark.py` + report + `CQ_SPARQL_Documentation.md`; `elicited_cq_sparql.py` + `Elicited_CQ_SPARQL_Report.md`; baseline tag `elicited-baseline-v0.6`.

---

### Phase 2: Namespace & Release Scaffolding (15–28 Sep)
*Objective: fix the identifiers everything else will cite, and start every long external wait.*

- **Activities:**
  1. **Decide the w3id segment** (`ricemmkg` or `rice-mmkg`) — it cannot change after anything is published under it.
  2. **w3id PURL registration:** pull request to `github.com/perma-id/w3id.org` using the prepared `.htaccess` (`Worklog/RiceMMKG_v0.5_worklog/reports/w3id_config/`). Content negotiation can point at the GitHub raw file until Phase 5 documentation exists.
  3. **Namespace rewrite:** run `rewrite_namespace.py` as a **separate commit**. It re-serialises the whole file, so its diff is unreadable by design; verify instead by triple count, HermiT, and both CQ instruments returning the same results as before the rewrite. Update the `PREFIX` blocks in both scripts and in `CQ_SPARQL_Documentation.md`.
  4. **Maintenance plan:** resolve the two open TODOs (institutional affiliation; release cadence) in `Worklog/RiceMMKG_v0.5_worklog/reports/maintenance_plan.md` and publish it in the repository.
  5. **Start the expert clock:** send the Stage 5 questionnaire (`CQ Screening/reports/cq_stage5_questionnaire.md`) and the 250-image stratified annotation sample. Keep `cq_stage5_key.csv` away from raters; the repository history still contains it.
- **Deliverables:** merged w3id PR; namespace-rewritten ontology with unchanged verification results; published maintenance plan; questionnaire and annotation sample sent.

---

### Phase 3: Modality Checkpoint, Grounding & Schema → v0.7 (29 Sep – 26 Oct)
*Objective: decide which further modalities enter the submission, and close the gaps the two CQ instruments measured.*

- **Modality checkpoint (start of Phase 3):** for **sensor** and **genomic** data separately, answer: is a real data source secured and linkable to the existing entities (varieties, diseases, growth stages, images)? Can it be modelled, populated and covered by CQs before the Phase 5 freeze? If yes, it enters the submission as a populated module; if not, it stays roadmap and is described as such in the paper. A modality with a declared but empty class is never claimed. Genomic scope should follow the expert's input — to be recorded here once clarified.
- **Activities:**
  1. **Literature-backed schema** (no expert data needed; each assertion needs a live-checked source and an `owl:Axiom`):
     - `PlantPart` and symptom → organ (elicited CQ-A03, part of CQ-A14);
     - transmission mode for vectors (CQ-A02);
     - management category and source authority for control measures (CQ-A07).
  2. **Expert image annotation → graph:** from the 250-image sample, add `captures` to further symptoms (CQ-18, CQ-A15, A16, A21), organ per image (CQ-A14), and severity per image (CQ-A18). None of these can be derived from Paddy Doctor labels or literature — they must come from annotators.
  3. **Re-measure:** run `cq_sparql_benchmark.py` and `elicited_cq_sparql.py`, compare against `elicited-baseline-v0.6`, re-check HermiT. Never edit a CQ because its query returns little.
  4. **If the checkpoint admits sensor and/or genomic data:** model the module, ingest the real data, link it to existing entities, add or activate the relevant CQs (Tier B elicited CQs become measurable; benchmark CQ-20 stops being `documented`), re-check HermiT.
  5. **Optional:** an embedding experiment across whichever modalities are populated. Useful as a usage demonstration, not required by the resource claim; drop it first if time runs short.
- **Waits for expert ratings:** the six elicited CQs with no concept in the ontology (A08, A09, A12, A14 in part, A20, A25) are not modelled until their relevance is rated.
- **Deliverables:** v0.7 ontology; before/after tables for both CQ instruments; consistency log.

---

### Phase 4: Expert Validation & Analysis (returns by late Oct; analysis 27 Oct – 9 Nov)
*Objective: independent human evidence for the CQ set and the screening procedure.*

- **Activities:**
  1. **Before analysing returns:** wire the Stage 7 per-CQ re-proposal rate into `stage6_analyse_responses.py` — running it afterwards forces Stage 6 to be redone.
  2. **Stage 6 analysis:** quadratic-weighted Cohen's κ (2 raters) or ordinal Krippendorff's α (3+ raters) on relevance and clarity; Spearman ρ of convergence (`n_models`, re-proposal rate) against mean relevance; permutation p-values.
  3. **Second screener:** an independent person screens ~20% of Stages 1, 3 and 4; report agreement. The first pass was drafted by one of the source models, so this is the most obvious objection to close.
  4. **Tier B instrument:** rate sensor/genomic roadmap CQs separately; Tier B ratings never enter the κ/α that evaluates the released resource.
  5. **Optional, not yet designed:** a sample of domain axioms rated for correctness by the same experts.
- **Deliverables:** anonymised rating matrix; agreement statistics; second-screener agreement; Tier B prioritisation.

---

### Phase 5: Availability & FAIR Finalisation (3 – 16 Nov)
*Objective: publish the release the paper describes, once its content is final.*

- **Activities:**
  1. Generate **pyLODE** or **Widoco** documentation from the release and serve it at the PURL; switch content negotiation from the interim target to HTML / RDF.
  2. Run **FOOPS!** and **OOPS!** on the release; target FOOPS! > 0.85 (baseline 0.7275, mostly lost on the missing PURL, which Phase 2 fixes).
  3. Tag the release; deposit to **Zenodo** (DOI) from the prepared manifest; submit to **AgroPortal** from the prepared draft.
- **Deliverables:** live documentation at the PURL; FOOPS!/OOPS! reports; Zenodo DOI; AgroPortal entry.

---

### Phase 6: Resource Paper & Submission (mid Nov – early Dec)
*Objective: prepare and submit the manuscript.*

- **Activities:**
  1. **Manuscript** per ESWC Resource Track criteria:
     - *Impact & value* — image grounding plus agronomic decision support, with vector transmission modelled explicitly.
     - *Reusability & FAIR* — w3id PURL, documentation, Zenodo DOI, AgroPortal, maintenance plan, FOOPS! score.
     - *Evaluation* — benchmark CQs, elicited CQs with measured answerability against a frozen baseline, DL consistency, expert agreement.
  2. **Reproducibility package:** the `CQ Screening/scripts/` and `reports/` directories are currently gitignored, which undercuts the reproducibility claim — publish them; add a single runner and an environment lockfile.
  3. **Method statements the paper must make:** the two elicitation rounds; LLM-assisted, human-adjudicated grouping (and the source-model conflict of interest); the 50% coverage threshold as an author convention; CQ-22's 2026-09-14 extension with both results reported; the correction of the originally published v0.6 figures.
  4. Internal and advisor review; submission.
- **Deliverables:** submitted manuscript; release-tagged public repository.

---

## 4. Key Differences and Framing vs. Comparator (RiceDO)

| Feature | RiceDO (Comparator) | Rice MMKG (Our Contribution) | Strategic Narrative |
|---|---|---|---|
| **Visual Modality** | None (Text only) | **10,407 field images** linked to domain concepts | Complementary expansion: RiceDO explicitly requested image grounding in their future work |
| **Observation / Evidence Separation** | Conflated | `annotatedAs` (dataset label) vs. `captures` (evidence) | Prevents noisy ML labels from corrupting domain truths |
| **Traceable Provenance** | Unreified | **256/256 domain assertions reified with `owl:Axiom`**, CABI sources as DOIs | Auditable to CABI, IRRI, BBPOPT, FAO and IRAC literature |
| **Interoperability** | Partial | Mapped to **EPPO, AGROVOC, NCBI Taxonomy and PECO** | FAIR cross-linking across biological registries |
| **Decision Support** | High-level advice | **End-to-end 4-hop DSS chain** + severity triage | Practical farm-level advisory utility |
| **Requirements basis** | Qualitative CQs | Benchmark CQs **and** LLM-elicited, expert-rated CQs with measured answerability | Requirements not written to fit the existing graph |

---

## 5. Active Sprint Checklist (Weeks 3–4, Sept)

- [x] **v0.6.1 patch** (2026-09-14) — CQ-10, CQ-22, CQ-24 fixed; figures corrected across documentation.
- [x] **Provenance clean-up** (2026-09-14) — `provenance_axioms.rdf` archived; 242 CABI sources as DOIs with Crossref citations.
- [ ] **Record the expert's genome input** (what data, which entities, which questions) — needed before the Phase 3 modality checkpoint.
- [ ] **Scout sensor and genomic data sources** (availability, licence, linkability to existing entities) so the Phase 3 checkpoint can decide on evidence.
- [ ] **Decide w3id segment** (`ricemmkg` / `rice-mmkg`).
- [ ] **Open w3id.org pull request.**
- [ ] **Namespace rewrite** as a separate commit; re-run HermiT and both CQ instruments.
- [ ] **Maintenance plan:** affiliation and release cadence.
- [ ] **Send to experts:** Stage 5 questionnaire and 250-image annotation sample.
- [ ] **Re-check presentation slides** — they still quote pre-fix v0.6 figures.
