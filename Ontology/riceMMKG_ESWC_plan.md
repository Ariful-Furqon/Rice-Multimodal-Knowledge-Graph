# Rice MMKG — Master Plan Toward ESWC 2027

Construction, evaluation, and publication roadmap for the **ESWC 2027 Resource Track**.  
**Current Milestone:** Rice MMKG **v0.6** (live as of 2026-09-03).  
**Abstract / Paper Deadline:** Late November – early December.

---

## 1. Executive Summary & Resource Snapshot

| Metric / Dimension | Current State (v0.6) | Comparator (RiceDO) | Target for Submission |
|---|---|---|---|
| **Ontology Version** | **`0.6` (Live)** | `1.0` | `1.0` (Production release) |
| **Asserted Triples** | **66,874** | ~1,200 | ~70,000–80,000 (with sensor & text) |
| **Materialised Triples (OWL RL)** | **161,568** (+94,694 triples) | — | > 175,000 |
| **Image Observations** | **10,407** | 0 | 10,407 (with symptom bounding boxes) |
| **Sensor & Text Modalities** | Scaffolding (`SensorObservation`) | 0 | Ingested telemetry & advisory text |
| **Domain-Level Assertions** | **265 reified axioms (100% cited)** | 18 diseases | 100% literature-grounded |
| **Reasoner Consistency** | **100% Consistent (HermiT / Pellet)** | Verified | 100% Consistent (0 unsatisfiable classes) |
| **Competency Questions** | **25 CQs** (87.5% Pass Rate, 21 PASS) | Qualitative CQs | 25 CQs (> 95% Pass Rate) |
| **Permanent URI (PURL)** | Local namespace (`.../riceMMKG#`) | `purl.org/ricedo` | `w3id.org/ricemmkg` (Live redirection) |
| **FAIR Score (FOOPS!)** | Pending execution | — | **FOOPS! score > 0.85** |
| **Registry Findability** | Local repository | IEEE DataPort | **AgroPortal** entry + **Zenodo DOI** |
| **Online Documentation** | Markdown documentation | — | **pyLODE / Widoco** live at w3id PURL |
| **Expert Validation** | Planned (Phase 4) | 5 experts (95.2%) | 3–5 plant pathologists (Fleiss' κ) |

---

## 2. Five-Phase Master Workflow Toward ESWC 2027

```
Phase 1: Functional & Reasoning Evaluation (Weeks 1–2, Sept) — [IN PROGRESS: 90% COMPLETE]
   ├── Formulate 25 Agronomic CQs (Schema-level, L1–L4 × D1–D3) [DONE]
   ├── Implement Automated SPARQL Benchmark Suite (cq_sparql_benchmark.py) [DONE]
   ├── Run Automated DL Reasoner (HermiT / Pellet) for Consistency & Entailment [DONE]
   └── Deliverables: Benchmark Script, Pass Rate Report (87.5%), Reasoner Consistency Log [DONE]
          │
          ▼
Phase 2: Availability, PURL & FAIR Polish (Weeks 3–4, Sept)
   ├── Register w3id.org Permanent Namespace (w3id.org/ricemmkg)
   ├── Execute URI Namespace Rewrite Script on Ontology Triples
   ├── Deploy Responsive HTML Documentation via pyLODE / Widoco
   ├── Deposit Citable Release to Zenodo (DOI) and AgroPortal Registry
   └── Target: FOOPS! FAIR score > 0.85, Live Content Negotiation
          │
          ▼
Phase 3: Multimodal Experimentation (Weeks 5–8, Late Sept & Oct)
   ├── Sensor Modality: Populate SensorObservation with microclimate/weather telemetry
   ├── Textual Modality: Ingest unstructured advisory reports into TextualObservation
   ├── Cross-modal Grounding: Annotate images at symptom level (rice:captures for 27 symptoms)
   └── Tri-Modal Fusion: Extend IKRL / representation learning benchmark across Image + Sensor + Text + Graph
          │
          ▼
Phase 4: Domain Expert Validation (Weeks 9–10, Late Oct & Early Nov)
   ├── Prepare 30–50 Assertion & CQ Validation Questionnaire
   ├── Survey Panel of Professional Agronomists & Plant Pathologists
   └── Compute Inter-Rater Reliability (Cohen's / Fleiss' Kappa)
          │
          ▼
Phase 5: Resource Paper Drafting & Camera-Ready Submission (Weeks 11–14, Nov – Early Dec)
   ├── Draft Manuscript according to ESWC Resource Track Guidelines
   ├── Finalize Public Reproducibility GitHub Repo (Docker / automated runner)
   └── Internal Academic Review & Final Submission
```

---

## 3. Detailed Phase Breakdown & Deliverables

### Phase 1: Functional & Reasoning Evaluation (Weeks 1–2, Sept)
*Status: **90% Completed** (v0.6 released, 21/24 CQs passing, Protégé HermiT 100% clean).*

- **Target Milestones & Activities:**
  1. Formulate 25 agronomic Competency Questions (CQs) spanning 4 reasoning levels (L1–L4) and 3 knowledge dimensions (D1–D3).
  2. Implement executable SPARQL query runner with 4 strict evaluation modes (`coverage`, `negative`, `entailment`, `documented`) without `OPTIONAL` on mandatory hops.
  3. Execute automated DL Reasoner (HermiT/Pellet in Protégé, OWL RL in Python) for defined class materialization and disjointness verification.
  4. Fix remaining minor failures for v0.6.1 (`Nephotettix_Virescens` control treatment and literal `@en` language tagging).
- **Key Deliverables & Outputs:**
  1. `cq_sparql_benchmark.py` & `cq_sparql_benchmark_results.json`.
  2. Auto-generated `CQ_SPARQL_Benchmark_Report.md` and complete documentation `CQ_SPARQL_Documentation.md`.
  3. Protégé Reasoner consistency log (0 unsatisfiable classes, 1,442 entailed `SymptomaticObservation` individuals).

---

### Phase 2: Availability, PURL & FAIR Polish (Weeks 3–4, Sept)
*Objective: Transform Rice MMKG into a certified, FAIR-compliant permanent Semantic Web resource.*

- **Target Milestones & Activities:**
  1. **w3id PURL Registration:** Submit a pull request to `github.com/perma-id/w3id.org` to reserve `https://w3id.org/ricemmkg` with Apache `.htaccess` content negotiation (redirecting browser requests to HTML documentation and RDF clients to raw Turtle/RDF-XML).
  2. **Namespace Rewrite:** Run an automated rewrite script across `Rice MMKG.rdf` and all SPARQL queries, replacing `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#` with `https://w3id.org/ricemmkg#`.
  3. **Automated Documentation Deployment:** Generate interactive HTML documentation using **pyLODE** or **Widoco**, including class diagrams, schema visualization, and cross-reference links, hosted via GitHub Pages at the PURL.
  4. **FAIR & Pitfall Auditing:** Run **FOOPS!** (`w3id.org/foops/`) and **OOPS!** (`oops.linkeddata.es`) to achieve a verified FAIR metric score **> 0.85**.
  5. **Registry Submissions:**
     - Deposit dataset and ontology snapshot to **Zenodo** to mint a citable DOI.
     - Register the ontology in **AgroPortal** (the primary FAO/INRAE repository for agronomical ontologies).
- **Key Deliverables & Outputs:**
  1. Live `https://w3id.org/ricemmkg` redirection with content negotiation.
  2. FOOPS! assessment certificate with score > 0.85.
  3. AgroPortal catalog entry and official Zenodo DOI.
  4. Public online HTML specification.

---

### Phase 3: Multimodal Experimentation (Weeks 5–8, Late Sept & Oct)
*Objective: Populate non-image modalities and prove multimodal representation learning.*

- **Target Milestones & Activities:**
  1. **Sensor Modality Population (`SensorObservation`):** Ingest real-world environmental/microclimate telemetry (temperature, relative humidity, soil moisture) linked to rice phenology stages and environmental factors (`increaseRiskOf`).
  2. **Textual Modality Population (`TextualObservation`):** Extract and ingest unstructured field advisory notes, expert diagnostic transcripts, and extension service reports.
  3. **Granular Visual Grounding (Closing CQ-18):** Expand image annotations from class-level (`annotatedAs Disease`) to bounding-box / symptom-level (`captures Symptom`) across all 27 declared symptoms.
  4. **Tri-Modal Fusion Benchmark:** Implement knowledge graph representation learning (e.g., Image-embodied KG embedding, IKRL) combining Image + Sensor + Text + Graph embeddings for disease prediction.
- **Key Deliverables & Outputs:**
  1. Populated `SensorObservation` graph module.
  2. Populated `TextualObservation` graph module.
  3. Benchmarked tri-modal multimodal fusion pipeline and comparative baseline evaluation.

---

### Phase 4: Domain Expert Validation (Weeks 9–10, Late Oct & Early Nov)
*Objective: Rigorous human-in-the-loop qualitative and quantitative agronomic validation.*

- **Target Milestones & Activities:**
  1. Design a formal validation protocol and 5-point Likert scale questionnaire sampling 30–50 representative axioms (pathogen causality, symptom associations, stage vulnerability, and management triage).
  2. Recruit 3–5 professional plant pathologists and agricultural extension specialists (e.g., from BBPOPT, IRRI alumni, or university agricultural faculties).
  3. Measure statistical consensus using **Fleiss' Kappa** ($\kappa$) or **Cohen's Weighted Kappa** for inter-rater agreement.
  4. Collate expert qualitative critique into an actionable improvement appendix.
- **Key Deliverables & Outputs:**
  1. Anonymized expert evaluation dataset and rating matrix.
  2. Statistical inter-rater agreement score ($\kappa \ge 0.75$).
  3. Qualitative agronomic validation report.

---

### Phase 5: Resource Paper Drafting & Camera-Ready Submission (Weeks 11–14, Nov – Early Dec)
*Objective: Prepare, polish, and submit the full manuscript to ESWC 2027 (Resource Track).*

- **Target Milestones & Activities:**
  1. **Manuscript Drafting:** Write the full 15-page LNCS paper following the official ESWC Resource Track review criteria:
     - *Potential impact & value to the community* (image grounding + agronomic decision support).
     - *Reusability, design rigor, and FAIR compliance* (FOOPS! > 0.85, w3id PURL, AgroPortal, Zenodo).
     - *Evaluation rigor* (25 CQs with > 95% pass rate, DL consistency, expert validation $\kappa$, multimodal fusion benchmark).
  2. **Reproducibility Package:** Package a clean GitHub repository containing:
     - One-click benchmark runner (`python run_benchmark.py`).
     - Dockerfile / virtual environment lockfile.
     - Zenodo-hosted image datasets and pre-computed embeddings.
  3. **Internal Review:** Conduct peer review and advisor revisions prior to final submission.
- **Key Deliverables & Outputs:**
  1. Complete 15-page camera-ready PDF manuscript.
  2. Public, reproducible, release-tagged GitHub repository.
  3. Official ESWC 2027 conference submission.

---

## 4. Key Differences and Framing vs. Comparator (RiceDO)

| Feature | RiceDO (Comparator) | Rice MMKG (Our Contribution) | Strategic Narrative |
|---|---|---|---|
| **Visual Modality** | None (Text only) | **10,407 field images** grounded to concepts | Complementary expansion: RiceDO explicitly requested image grounding in their future work |
| **Observation / Evidence Separation** | Conflated | Rigorous: `annotatedAs` (dataset) vs. `captures` (evidence) | Prevents noisy ML labels from corrupting domain truths |
| **Traceable Provenance** | Unreified | **100% domain assertions reified with `owl:Axiom`** | Full auditability to CABI, IRRI, and BBPOPT literature |
| **Interoperability** | Partial | Formally mapped to **EPPO, AGROVOC, and NCBI Taxonomy** | Seamless FAIR cross-linking across biological registries |
| **Decision Support** | High-level advice | **End-to-end 4-hop DSS chain** + severity triage | Practical farm-level advisory utility |

---

## 5. Active Sprint Checklist (Current Week)

- [x] **v0.6 Ontology Release:** Disambiguate `Deadheart` (Disease) and `Dead_Tiller` (Symptom).
- [x] **Reasoner Consistency:** Verify 100% clean consistency in Protégé HermiT & Pellet (0 unsatisfiable classes).
- [x] **25 CQ SPARQL Suite:** Execute automated benchmark with 87.5% pass rate (21 PASS / 1 PARTIAL / 2 FAIL / 1 DOC).
- [x] **Synchronize Documentation:** Update `Ontology_Overview.md`, `CQ_SPARQL_Documentation.md`, and presentation slides.
- [ ] **v0.6.1 Minor Patch:**
  - [ ] Add `rice:Nephotettix_Virescens rice:controlledBy rice:Vector_Control` (CQ-10 fix).
  - [ ] Add `@en` language tag to `rice:evidenceType "literature-curated"` (CQ-24 fix).
  - [ ] Re-run benchmark to reach **23 PASS / 1 PARTIAL / 0 FAIL / 1 DOC (96% Pass Rate)**.
- [ ] **Kick off Phase 2:** Prepare w3id PURL pull request and generate pyLODE HTML preview.
