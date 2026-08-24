# Rice MMKG v0.4 → v0.5 — correction worklog

Task specification for Claude Code. Six corrections, none large. Phase A is verified defects, Phase B is modelling precision, Phase C prepares the evaluation and availability evidence the ESWC resource track scores on.

---

## 0. Context

**Input:** `Rice_MMKG.rdf`, `owl:versionInfo` `0.4`
**Base IRI:** `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#`, prefix `rice:`

**Verified v0.4 baseline** (rdflib 7.6.0) — the regression reference:

| Quantity | Value |
|---|---|
| Total triples | 66,882 |
| Named classes | 16 (incl. 1 defined) |
| Object properties | 24 |
| Datatype properties | 5 |
| Annotation properties | 14 |
| Individuals | 10,499 |
| `rice:ImageObservation` individuals | 10,407 |
| Domain individuals | 92 |
| `owl:Axiom` provenance records | 266 |
| Domain-level assertions | 266 |
| `skos:exactMatch` / `closeMatch` | 32 / 18 |
| `rice:eppoCode` assertions | 16 |
| Individuals typed only `NamedIndividual` | 0 |
| `TODO` literals | 0 |

**Domain assertion counts:** `vulnerableTo` 60 · `occursIn` 47 · `controlledBy` 42 · `indicatedBy` 42 · `increaseRiskOf` 29 · `recommends` 23 · `causes` 10 · `preventedBy` 8 · `requires` 5. **Every one of the 266 carries provenance.** Do not break that invariant.

### Environment

```bash
pip install rdflib --break-system-packages
```

```
work/
  Rice_MMKG_v0.4.rdf      # read-only copy
  Rice_MMKG_v0.5.rdf      # output
  scripts/
  reports/
```

### Ground rules

- One idempotent script per task under `scripts/`.
- Re-run `scripts/verify.py` after every task; append to `reports/`.
- All changes through rdflib; never hand-edit RDF/XML.
- **Provenance invariant: every domain-level assertion must have a matching `owl:Axiom` record.** If a task adds or retargets an assertion, its provenance record moves with it. `verify.py` must fail if any assertion lacks one.
- **Never invent an EPPO code, AGROVOC IRI, NCBITaxon ID, or vector–pathogen pair.** Anything not given explicitly below goes to a CSV for human completion.
- Serialise `format="pretty-xml"`, prefixes bound.

## Task 0.1 — Extend the verification harness

Add to `scripts/verify.py`, on top of the existing checks:

- **Provenance coverage**: for each domain-level assertion, whether a matching `owl:Axiom` exists. Report any orphans in both directions — assertions without provenance, and provenance records pointing at assertions that no longer exist.
- **Duplicate identifier detection**: any `eppoCode` value used by more than one individual; any alignment IRI used by more than one individual, broken down by match type.
- **Range conformance**: for each object property, whether every asserted target is an instance of a class in its declared range.

**Acceptance:** reproduces every baseline figure. Reports 266/266 provenance coverage, one duplicate EPPO code, and three shared alignment IRIs.

---

# Phase A — Verified defects

## Task A.1 — Correct the EPPO code for *X. oryzae* pv. *oryzicola*

`rice:Xanthomonas_Oryzicola` carries `eppoCode "XANTOX"`. The correct code is **`XANTTO`**. This is confirmed by the EPPO Global Database datasheet and by EU Regulation 2019/2072 Annex II, which lists *Xanthomonas oryzae* pv. *oryzicola* (Fang et al.) Swings et al. as [XANTTO].

`rice:Xanthomonas_Oryzae` carrying `XANTOR` is correct and must not be changed.

**Change.** One literal.

**Acceptance:** exactly one `eppoCode` triple changed; `XANTOX` absent; `XANTTO` present once.

## Task A.2 — Merge the duplicated stem borer

`rice:Stem_Borer` and `rice:Scirpophaga_Incertulas` are the same organism. `Stem_Borer`'s own `rdfs:comment` reads "Scirpophaga incertulas (yellow stem borer)", and both carry `eppoCode SCPIIN`. They have diverged:

| | `Stem_Borer` | `Scirpophaga_Incertulas` |
|---|---|---|
| AGROVOC | `c_7389` (closeMatch) | `c_6911` (exactMatch) |
| NCBITaxon | — | `NCBITaxon_72366` (exactMatch) |
| Outgoing | `controlledBy` ×2, `indicatedBy Deadheart`, `occursIn` ×2, `recommends` | `causes Deadheart` |
| Incoming | `vulnerableTo` ×3, `increaseRiskOf` ×1 | `vulnerableTo` ×1 |

**Change.** Merge into `rice:Stem_Borer`, which carries almost all the relations and is the label the dataset uses.

1. Move `exactMatch NCBITaxon_72366` onto `Stem_Borer`.
2. Move `exactMatch agrovoc:c_6911` onto `Stem_Borer`. Demote the existing `closeMatch agrovoc:c_7389` to `skos:broadMatch` — `c_7389` denotes stem borers as a group, which is broader than this species. Verify both AGROVOC IRIs resolve to what this assumes before applying; if either does not, emit to `reports/alignment_check.csv` and stop.
3. Add `skos:altLabel "Scirpophaga incertulas"` and keep the existing comment.
4. Redirect the one incoming `vulnerableTo` from `Scirpophaga_Incertulas` to `Stem_Borer`, carrying its provenance record with it. Drop it if it duplicates an existing assertion, and delete the orphaned provenance record.
5. Drop `causes Deadheart` — see Task B.1. `Stem_Borer indicatedBy Deadheart` already records the same fact in the correct direction.
6. Delete `rice:Scirpophaga_Incertulas` and any provenance records referencing it.

**Acceptance:** `Scirpophaga_Incertulas` absent; `SCPIIN` used once; `Stem_Borer` carries NCBITaxon and both AGROVOC links at the correct match strengths; individual count 10,499 → 10,498; provenance coverage still 100%.

---

# Phase B — Modelling precision

## Task B.1 — Separate vector transmission from causation

`rice:causes` currently carries three different semantics:

| Assertion | Reading |
|---|---|
| `Magnaporthe_Oryzae causes Rice_Blast_Disease` | pathogen causes disease — correct |
| `Nephotettix_Virescens causes Rice_Tungro_Disease` | **vector, not cause** |
| `Scirpophaga_Incertulas causes Deadheart` | **pest causes a symptom, not a disease** |

A leafhopper does not cause tungro; it transmits the viruses that do. The ontology already asserts `Rice_Tungro_Bacilliform_Virus causes Rice_Tungro_Disease` and `Rice_Tungro_Spherical_Virus causes Rice_Tungro_Disease`, and `Nephotettix_Virescens`'s own comment describes it as the primary vector for both. The knowledge is present; only the relation is wrong.

**Change.**

1. Declare `rice:transmits` with inverse `rice:transmittedBy`, domain `rice:Pest`, range `rice:Pathogen`.
2. Replace `Nephotettix_Virescens causes Rice_Tungro_Disease` with `transmits` assertions to the two tungro viruses. **Do not assume which viruses** — the comment names them, but confirm against the cited source before asserting. Carry the existing provenance record onto the new assertions, or emit to `reports/vector_todo.csv` if the source does not support both.
3. Narrow `rice:causes` range to `rice:Disease` once the two non-conforming assertions are gone.

The third case is resolved by Task A.2.

**Acceptance:** `causes` has 9 assertions, all `Pathogen → Disease`, all range-conformant; `transmits` has assertions only where the cited source supports them; provenance coverage 100%.

**Note for the paper.** None of the eight comparator ontologies models vector-borne transmission explicitly. Tungro is among the most important rice diseases in Southeast Asia and cannot be modelled correctly without it. This is a contribution, not a detail — state it in the paper rather than leaving it in the file for a reader to notice.

## Task B.2 — Refine over-broad alignments

Three AGROVOC IRIs are each used by more than one individual:

| IRI | Individuals | Match type |
|---|---|---|
| `c_27879` | `Fungicide_Application`, `Insecticide_Application` | both closeMatch |
| `c_4911` | `Monitoring` (exact), `Field_Inspection` (close) | mixed |
| `c_7773` | `Tillering_Stage`, `Reduced_Tillering`, `Excessive_Tillering` | all closeMatch |

**These are not errors.** `skos:closeMatch` asserts sufficient similarity for interchangeable use in some applications, so several narrower concepts pointing at one broader concept is legitimate. An earlier review of this file called them wrong; that judgement was too strong.

They are, however, imprecise. Where the AGROVOC concept is genuinely broader than the local individual, `skos:broadMatch` states the relationship exactly and costs nothing.

**Change.** Emit `reports/alignment_refine.csv` listing the three groups with columns `individual,current_iri,current_match,proposed_match,verified`. Do not resolve AGROVOC IRIs programmatically and do not guess what each denotes. Write `scripts/apply_alignment_refine.py` to read the completed file back, validating that the proposed match is one of `exactMatch`, `closeMatch`, `broadMatch`, `narrowMatch`.

The `c_7773` group most likely needs attention: a growth stage and two symptoms sharing one concept suggests `Tillering_Stage` should hold the match while the two symptoms are modelled as qualities of it.

**Acceptance:** the CSV exists with six rows; the ontology is unchanged until it is completed.

## Task B.3 — Broaden the evidence layer

`rice:captures` holds 1,442 assertions, all pointing at `rice:Deadheart`. The symptom vocabulary has grown from 11 to 28 individuals, but the instance-level evidence layer still has exactly one value.

This is the narrowest remaining part of the artefact and it limits the reasoning evaluation: `SymptomaticObservation` materialises 1,442 members, all of one kind.

**Change.** This needs human annotation and cannot be automated. Prepare the ground:

1. `scripts/sample_for_annotation.py` — draw a stratified sample of 25 `ImageObservation` individuals per annotation target, seeded and reproducible, emitting `reports/annotation_sample.csv` with `individual_iri`, `content_url`, `annotated_as`, and an empty semicolon-separated `symptom_iris` column.
2. `reports/symptom_vocabulary.md` — the 28 `Symptom` individuals with labels and comments, as the controlled vocabulary the annotator picks from, plus an explicit "other / not listed" escape so genuinely new symptoms surface rather than being forced into an existing term.
3. `scripts/apply_symptom_annotations.py` — reads the completed CSV, asserts `captures`, rejects any IRI outside the vocabulary, and attaches a provenance record with `evidenceType "expert-annotated"` to distinguish these from the literature-curated assertions.

**Acceptance:** sample CSV has 250 rows balanced across the ten targets; vocabulary file lists 28 symptoms; the apply script runs clean against a two-row fixture.

---

# Phase C — Evaluation and availability

## Task C.1 — Baseline quality scores

Two free services produce quantitative evaluation evidence with no new modelling.

- **OOPS!** (`oops.linkeddata.es`) — checks 33 of 41 catalogued pitfalls, returning each with an importance level.
- **FOOPS!** (`w3id.org/foops/`) — 24 checks across the four FAIR dimensions with a normalised score. An API is available at `w3id.org/foops/api`.

Run both now, before the PURL migration, and save the raw output to `reports/baseline_oops.json` and `reports/baseline_foops.json`. Run them again after Task C.2 and report both figures.

Reporting a before-and-after is stronger than reporting a final number alone: it shows the resource measurably improved during development rather than being asserted to be good.

For calibration, gUFO reports a 92% FOOPS score, with the residual gap attributed to a metadata-property choice rather than a real deficiency.

**Acceptance:** both raw outputs saved; `reports/quality_baseline.md` summarises the scores and lists every pitfall flagged as IMPORTANT or CRITICAL with a disposition — fix now, fix later, or accept with reason.

## Task C.2 — Persistent identifier

The namespace is a Protégé default and cannot be dereferenced. FOOPS! checks this directly under its findability tests, which assess compliance with persistent identifier registries such as w3id.org and purl.org.

**Change.** Prepare a `w3id.org` registration — it is pull-request based and free — and emit the redirect configuration to `reports/w3id_config/`. Write `scripts/rewrite_namespace.py` taking the new base IRI as an argument and rewriting every subject, predicate, and object in the local namespace, including inside the 266 provenance records.

**Do not run the rewrite until the registration is confirmed.** Checkpoint C1.

**Acceptance:** the script exists and is tested against a fixture; the ontology is unchanged by this task.

## Task C.3 — Deposit and registry

Prepare, do not submit:

- A Zenodo deposit manifest for a citable DOI.
- An AgroPortal submission package. AgroPortal is not an alignment target — it was correctly dropped from the anchor layer — but as the community registry for agricultural ontologies it is what the availability criterion asks for. It also runs O'FAIRe, giving a second independent FAIRness score.
- `reports/maintenance_plan.md` — who maintains the resource, on what cadence, where issues are filed. Its absence is a scored deficiency.
- HTML documentation via pyLODE or Widoco, to be hosted at the PURL.

**Acceptance:** all four artefacts exist under `reports/`; nothing submitted.

---

# Target end state

| | v0.4 | v0.5 |
|---|---|---|
| Duplicate EPPO codes | 1 | **0** |
| Incorrect EPPO codes | 1 | **0** |
| Duplicate individuals | 1 pair | **0** |
| `causes` assertions with non-conformant range | 2 | **0** |
| Vector transmission modelled | no | **yes** |
| Provenance coverage | 100% | **100%** |
| Distinct symptoms in `captures` | 1 | 1, with 250 annotations prepared |
| OOPS!/FOOPS! scores | unmeasured | **measured, twice** |

---

# Human checkpoints

| | Decision | Blocks |
|---|---|---|
| C1 | w3id namespace string | Task C.2 rewrite |
| C2 | AGROVOC match-type refinements, six rows | Task B.2 |
| C3 | confirm the two tungro viruses against the cited source | Task B.1 |
| C4 | whether to run the 250-image symptom annotation | Task B.3 |
| C5 | verify `c_7389` and `c_6911` denote what Task A.2 assumes | Task A.2 |

---

# Explicitly out of scope

- `Sheath_Blight` still lacks a pathogen — one remaining of the original five, worth doing but not blocking
- The 44 unaligned domain individuals, mostly symptoms; symptom vocabulary is poorly covered by any standard vocabulary and that absence is itself worth reporting
- `SensorObservation` remains empty; keep it as a declared extension point with an explanatory comment
- `detects` remains unasserted
- Modality restrictions on `ImageObservation` and `SensorObservation`
- SOSA/SSN alignment
- IKRL implementation — a separate contribution, and not a dependency of the resource paper

---

# Reporting

Write `reports/v0.5_summary.md` at the end: tasks completed, `verify.py` deltas against the v0.4 baseline, checkpoints hit, provenance coverage, and the OOPS!/FOOPS! before-and-after. Flag any acceptance check that was relaxed and say why. A silently skipped check is worse than a failed one.
