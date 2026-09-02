"""
Rice MMKG - Competency Question SPARQL Benchmark

Design principles
  * A CQ is scored against a pass criterion declared BEFORE the run (see MODES).
    "The query returned at least one row" is not evidence of competency: combined
    with OPTIONAL it makes every CQ unfalsifiable, since any populated anchor
    class produces rows whether or not the relation under test exists.
  * Mandatory hops are therefore written WITHOUT OPTIONAL, and patterns quantify
    over classes rather than enumerating individuals in FILTER ... IN (...).
  * CQs are placed on two orthogonal axes - reasoning depth (L1-L4) and knowledge
    dimension (D1-D3). Provenance and cross-modal grounding are dimensions a
    query ranges over, not deeper forms of inference.
  * A real OWL RL materialisation is run, so the L4 CQs test entailment rather
    than asserted triples.

MODES
  coverage    numerator query / denominator query -> ratio vs threshold.
              PASS >= threshold, PARTIAL if 0 < ratio < threshold, FAIL if 0.
              Un-covered members are listed: the gap is the finding.
  negative    integrity constraint; PASS iff 0 rows. Violations are listed.
  entailment  same query on asserted vs materialised graph;
              PASS iff entailed > asserted and entailed >= expect min_entailed.
  documented  expected-empty extension point; records the value, never scored.
"""

import time
import json
import datetime
from pathlib import Path

from rdflib import Graph
import owlrl

# -- Paths ---------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
ONTOLOGY   = SCRIPT_DIR.parent / "Rice MMKG.rdf"
REPORT_OUT = SCRIPT_DIR / "CQ_SPARQL_Benchmark_Report.md"
JSON_OUT   = SCRIPT_DIR / "cq_sparql_benchmark_results.json"

assert ONTOLOGY.exists(), f"Ontology not found: {ONTOLOGY}"

RICE_NS = "http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#"

PREFIX = f"""
PREFIX rice: <{RICE_NS}>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX schema: <http://schema.org/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
"""

# Coverage threshold above which a relation is considered adequately populated.
# Stated as an explicit design decision so results are reproducible.
COVERAGE_THRESHOLD = 0.50

LEVELS = {
    "L1": "Factual - single-hop retrieval",
    "L2": "Contextual - multi-criteria join",
    "L3": "Causal - multi-hop chain",
    "L4": "Inferential - requires entailment",
}
DIMENSIONS = {
    "D1": "Agronomic / symbolic",
    "D2": "Cross-modal (image to concept)",
    "D3": "Provenance and external alignment",
}

CQS = [
    # ============================ L1 x D1 =====================================
    {
        "id": "CQ-01", "level": "L1", "dim": "D1", "mode": "coverage",
        "question": "Which rice diseases have an identified causal pathogen?",
        "rationale": "Aetiological completeness. A disease without a causal agent "
                     "cannot support any downstream causal query.",
        "num": PREFIX + "SELECT DISTINCT ?d WHERE { ?d a rice:Disease . ?p rice:causes ?d }",
        "den": PREFIX + "SELECT DISTINCT ?d WHERE { ?d a rice:Disease }",
        "unit": "disease",
    },
    {
        "id": "CQ-02", "level": "L1", "dim": "D1", "mode": "coverage",
        "question": "Which diseases and pests have at least one observable symptom?",
        "rationale": "Diagnosability. Without a symptom link an entity is invisible "
                     "to field-observation-driven inference.",
        "num": PREFIX + """SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:indicatedBy ?s . ?s a rice:Symptom }""",
        "den": PREFIX + "SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }",
        "unit": "disease/pest",
    },
    {
        "id": "CQ-03", "level": "L1", "dim": "D1", "mode": "coverage",
        "question": "Which diseases and pests have at least one control treatment?",
        "rationale": "Actionability. The KG must not diagnose what it cannot advise on.",
        "num": PREFIX + """SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:controlledBy ?t . ?t a rice:Treatment }""",
        "den": PREFIX + "SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }",
        "unit": "disease/pest",
    },
    {
        "id": "CQ-04", "level": "L1", "dim": "D1", "mode": "coverage",
        "question": "Which symptoms are attached to at least one disease or pest?",
        "rationale": "Detects orphan symptoms - vocabulary declared but never used "
                     "in a diagnostic pattern.",
        "num": PREFIX + "SELECT DISTINCT ?s WHERE { ?s a rice:Symptom . ?e rice:indicatedBy ?s }",
        "den": PREFIX + "SELECT DISTINCT ?s WHERE { ?s a rice:Symptom }",
        "unit": "symptom",
    },

    # ============================ L2 x D1 =====================================
    {
        "id": "CQ-05", "level": "L2", "dim": "D1", "mode": "coverage",
        "question": "For which diseases/pests can we state both the growth stage "
                    "of occurrence and an environmental factor raising their risk?",
        "rationale": "Multi-criteria contextualisation. Both joins are mandatory "
                     "(no OPTIONAL), so the CQ measures real co-population of "
                     "occursIn and increaseRiskOf.",
        "num": PREFIX + """SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:occursIn ?stage . ?stage a rice:GrowthStage .
  ?f rice:increaseRiskOf ?e . ?f a rice:EnvironmentalFactor }""",
        "den": PREFIX + "SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }",
        "unit": "disease/pest",
        "detail": PREFIX + """SELECT DISTINCT ?stage ?e ?f WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:occursIn ?stage . ?stage a rice:GrowthStage .
  ?f rice:increaseRiskOf ?e . ?f a rice:EnvironmentalFactor } ORDER BY ?stage ?e""",
    },
    {
        "id": "CQ-06", "level": "L2", "dim": "D1", "mode": "coverage",
        "question": "Which growth stages have a documented vulnerability profile "
                    "naming a concrete disease or pest?",
        "rationale": "vulnerableTo is the most frequently asserted domain relation "
                     "in the KG (59 triples), so it must be exercised directly.",
        "num": PREFIX + """SELECT DISTINCT ?g WHERE {
  ?g a rice:GrowthStage . ?g rice:vulnerableTo ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest } }""",
        "den": PREFIX + "SELECT DISTINCT ?g WHERE { ?g a rice:GrowthStage }",
        "unit": "growth stage",
    },
    {
        "id": "CQ-07", "level": "L2", "dim": "D1", "mode": "negative",
        "question": "Is the stage-vulnerability view consistent with the "
                    "occurrence view (vulnerableTo without a matching occursIn)?",
        "rationale": "Integrity constraint. If stage G is vulnerableTo entity E, "
                     "then E should occursIn G. Any row is an inconsistency.",
        "num": PREFIX + """SELECT DISTINCT ?g ?e WHERE {
  ?g a rice:GrowthStage . ?g rice:vulnerableTo ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  FILTER NOT EXISTS { ?e rice:occursIn ?g } }""",
    },
    {
        "id": "CQ-08", "level": "L2", "dim": "D1", "mode": "coverage",
        "question": "Which preventive treatments carry an explicit growth-stage "
                    "prerequisite for their application?",
        "rationale": "Prevention advice without a timing constraint is not "
                     "operationalisable in the field.",
        "num": PREFIX + """SELECT DISTINCT ?t WHERE {
  ?e rice:preventedBy ?t . ?t rice:requires ?g . ?g a rice:GrowthStage }""",
        "den": PREFIX + "SELECT DISTINCT ?t WHERE { ?e rice:preventedBy ?t }",
        "unit": "preventive treatment",
    },

    # ============================ L3 x D1 =====================================
    {
        "id": "CQ-09", "level": "L3", "dim": "D1", "mode": "coverage",
        "question": "For which declared insect vectors is the transmission chain "
                    "vector -> pathogen -> disease fully traversable?",
        "rationale": "The canonical multi-hop epidemiological query. The denominator "
                     "is the set of pests asserted to transmit something (not all "
                     "pests), so the measure is chain completeness, not vector "
                     "prevalence.",
                    "is the set of pests asserted to transmit something (not all "
                    "pests), so the measure is chain completeness, not vector "
                    "prevalence.",
        "num": PREFIX + """SELECT DISTINCT ?v WHERE {
  ?v rice:transmits ?p . ?p rice:causes ?d . ?d a rice:Disease }""",
        "den": PREFIX + "SELECT DISTINCT ?v WHERE { ?v rice:transmits ?p }",
        "unit": "declared vector",
        "detail": PREFIX + """SELECT DISTINCT ?v ?p ?d WHERE {
  ?v rice:transmits ?p . ?p rice:causes ?d . ?d a rice:Disease } ORDER BY ?v""",
    },
    {
        "id": "CQ-09b", "level": "L3", "dim": "D1", "mode": "negative",
        "id": "CQ-10", "level": "L3", "dim": "D1", "mode": "negative",
        "question": "Are there insect vectors for which no control treatment is "
                    "recorded, leaving the transmission chain unbreakable?",
        "rationale": "A vector chain that cannot be interrupted has no advisory "
                     "value. Splitting this from CQ-09 separates 'the chain exists' "
                     "from 'the chain is actionable'.",
                    "value. Splitting this from CQ-09 separates 'the chain exists' "
                    "from 'the chain is actionable'.",
        "num": PREFIX + """SELECT DISTINCT ?v WHERE {
  ?v rice:transmits ?p .
  FILTER NOT EXISTS { ?v rice:controlledBy ?t } }""",
    },
    {
        "id": "CQ-10", "level": "L3", "dim": "D1", "mode": "coverage",
        "id": "CQ-11", "level": "L3", "dim": "D1", "mode": "coverage",
        "question": "For which diseases is the full risk-to-remedy chain traversable: "
                    "environmental factor -> disease -> symptom -> treatment?",
        "rationale": "End-to-end decision-support path. This is the query an "
                     "advisory application actually needs to answer.",
                    "advisory application actually needs to answer.",
        "num": PREFIX + """SELECT DISTINCT ?d WHERE {
  ?d a rice:Disease .
  ?f rice:increaseRiskOf ?d . ?f a rice:EnvironmentalFactor .
  ?d rice:indicatedBy ?s . ?s a rice:Symptom .
  ?d rice:controlledBy ?t . ?t a rice:Treatment }""",
        "den": PREFIX + "SELECT DISTINCT ?d WHERE { ?d a rice:Disease }",
        "unit": "disease",
        "detail": PREFIX + """SELECT DISTINCT ?d ?f ?s ?t WHERE {
  ?d a rice:Disease .
  ?f rice:increaseRiskOf ?d . ?f a rice:EnvironmentalFactor .
  ?d rice:indicatedBy ?s . ?s a rice:Symptom .
  ?d rice:controlledBy ?t . ?t a rice:Treatment } ORDER BY ?d""",
    },
    {
        "id": "CQ-11", "level": "L3", "dim": "D1", "mode": "coverage",
        "id": "CQ-12", "level": "L3", "dim": "D1", "mode": "coverage",
        "question": "For which diseases and pests does the KG reach the management "
                    "layer, i.e. recommend a concrete ManagementAction?",
        "rationale": "Tests that diagnosis terminates in an operational decision. "
                     "Note the direction of rice:recommends in this KG is "
                     "entity -> action, not action -> treatment.",
                    "Note the direction of rice:recommends in this KG is "
                    "entity -> action, not action -> treatment.",
        "num": PREFIX + """SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pest }
  ?e rice:recommends ?m . ?m a rice:ManagementAction }""",
        "den": PREFIX + "SELECT DISTINCT ?e WHERE { { ?e a rice:Disease } UNION { ?e a rice:Pest } }",
        "unit": "disease/pest",
    },
    {
        "id": "CQ-11b", "level": "L2", "dim": "D1", "mode": "coverage",
        "id": "CQ-13", "level": "L2", "dim": "D1", "mode": "coverage",
        "question": "Does every severity level map to a recommended management "
                    "action, so that triage advice is total?",
        "rationale": "Severity-driven triage is the decision layer of the KG. A "
                     "severity level with no action is a hole in the advisory logic.",
                    "severity level with no action is a hole in the advisory logic.",
        "num": PREFIX + """SELECT DISTINCT ?sev WHERE {
  ?sev a rice:SeverityLevel . ?sev rice:recommends ?m }""",
        "den": PREFIX + "SELECT DISTINCT ?sev WHERE { ?sev a rice:SeverityLevel }",
        "unit": "severity level",
        "detail": PREFIX + """SELECT DISTINCT ?sev ?m WHERE {
  ?sev a rice:SeverityLevel . ?sev rice:recommends ?m } ORDER BY ?sev""",
    },

    # ============================ L4 x D1 =====================================
    {
        "id": "CQ-12", "level": "L4", "dim": "D1", "mode": "entailment",
        "id": "CQ-14", "level": "L4", "dim": "D1", "mode": "entailment",
        "question": "Which observations are SymptomaticObservations, i.e. members "
                    "of the defined class 'Observation that captures some Symptom'?",
        "rationale": "The one genuine defined class in the ontology. Asserted "
                     "membership is zero by construction; a non-zero entailed count "
                     "proves the OWL axiomatisation does work SPARQL alone cannot.",
                    "membership is zero by construction; a non-zero entailed count "
                    "proves the OWL axiomatisation does work SPARQL alone cannot.",
        "num": PREFIX + "SELECT DISTINCT ?o WHERE { ?o a rice:SymptomaticObservation }",
        "expect": {"min_entailed": 1},
    },
    {
        "id": "CQ-13", "level": "L4", "dim": "D1", "mode": "entailment",
        "id": "CQ-15", "level": "L4", "dim": "D1", "mode": "entailment",
        "question": "Can the KG be queried in the inverse direction, e.g. "
                    "disease -> causedBy -> pathogen and symptom -> indicates -> disease?",
        "rationale": "14 of 26 object properties are declared as owl:inverseOf but "
                     "never asserted. Query robustness depends on materialising them.",
                    "never asserted. Query robustness depends on materialising them.",
        "num": PREFIX + """SELECT ?x ?y WHERE {
  { ?x rice:causedBy ?y } UNION { ?x rice:indicates ?y } UNION
  { ?x rice:hasOccurrenceOf ?y } UNION { ?x rice:controls ?y } }""",
        "expect": {"min_entailed": 1},
    },

    # ============================ D2 - cross-modal ============================
    {
        "id": "CQ-14", "level": "L3", "dim": "D2", "mode": "coverage",
        "id": "CQ-16", "level": "L3", "dim": "D2", "mode": "coverage",
        "question": "Which image observations can be grounded all the way to an "
                    "agronomic recommendation: image -> annotated class -> symptom "
                    "and treatment?",
        "rationale": "The central multimodal claim of the KG. The denominator is "
                     "restricted to images annotated with a Disease or Pest: images "
                     "labelled with a HealthStatus (healthy plants) correctly have "
                     "no symptom or treatment, and including them would understate "
                     "grounding by a fixed 17%.",
                    "restricted to images annotated with a Disease or Pest: images "
                    "labelled with a HealthStatus (healthy plants) correctly have "
                    "no symptom or treatment, and including them would understate "
                    "grounding by a fixed 17%.",
        "num": PREFIX + """SELECT DISTINCT ?img WHERE {
  ?img a rice:ImageObservation . ?img rice:annotatedAs ?e .
  ?e rice:indicatedBy ?s . ?e rice:controlledBy ?t }""",
        "den": PREFIX + """SELECT DISTINCT ?img WHERE {
  ?img a rice:ImageObservation . ?img rice:annotatedAs ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest } }""",
        "unit": "diagnostic image",
    },
    {
        "id": "CQ-15", "level": "L2", "dim": "D2", "mode": "coverage",
        "id": "CQ-17", "level": "L2", "dim": "D2", "mode": "coverage",
        "question": "Which annotated classes of the image corpus are typed as a "
                    "domain entity (Disease, Pest or HealthStatus)?",
        "rationale": "Checks that dataset labels were reconciled with the ontology "
                     "rather than left as free-floating individuals.",
                    "rather than left as free-floating individuals.",
        "num": PREFIX + """SELECT DISTINCT ?e WHERE {
  ?img rice:annotatedAs ?e .
  { ?e a rice:Disease } UNION { ?e a rice:Pest } UNION { ?e a rice:HealthStatus } }""",
        "den": PREFIX + "SELECT DISTINCT ?e WHERE { ?img rice:annotatedAs ?e }",
        "unit": "annotated class",
    },
    {
        "id": "CQ-16", "level": "L1", "dim": "D2", "mode": "coverage",
        "id": "CQ-18", "level": "L1", "dim": "D2", "mode": "coverage",
        "question": "Which symptoms are grounded in visual evidence, i.e. captured "
                    "by at least one image observation?",
        "rationale": "Symptom-level visual grounding is what distinguishes an MMKG "
                     "from a text ontology with images bolted on. Expected to expose "
                     "the sharpest gap in the current release.",
                    "from a text ontology with images bolted on. Expected to expose "
                    "the sharpest gap in the current release.",
        "num": PREFIX + "SELECT DISTINCT ?s WHERE { ?s a rice:Symptom . ?o rice:captures ?s }",
        "den": PREFIX + "SELECT DISTINCT ?s WHERE { ?s a rice:Symptom }",
        "unit": "symptom",
    },
    {
        "id": "CQ-17", "level": "L1", "dim": "D2", "mode": "negative",
        "id": "CQ-19", "level": "L1", "dim": "D2", "mode": "negative",
        "question": "Are there image observations lacking a content URL or a source "
                    "dataset provenance link?",
        "rationale": "Integrity constraint on the media layer. Any row means an "
                     "image cannot be retrieved or attributed.",
                    "image cannot be retrieved or attributed.",
        "num": PREFIX + """SELECT ?img WHERE {
  ?img a rice:ImageObservation .
  FILTER ( NOT EXISTS { ?img schema:contentUrl ?u } ||
           NOT EXISTS { ?img prov:wasDerivedFrom ?ds } ) }""",
    },
    {
        "id": "CQ-18", "level": "L1", "dim": "D2", "mode": "documented",
        "id": "CQ-20", "level": "L1", "dim": "D2", "mode": "documented",
        "question": "How many sensor observations does the KG contain?",
        "rationale": "Declared extension point. Recorded as a measurement, not "
                     "scored, so the roadmap gap stays visible without inflating "
                     "or deflating the pass rate.",
                    "scored, so the roadmap gap stays visible without inflating "
                    "or deflating the pass rate.",
        "num": PREFIX + "SELECT DISTINCT ?o WHERE { ?o a rice:SensorObservation }",
    },

    # ============================ D3 - provenance and alignment ===============
    {
        "id": "CQ-19", "level": "L4", "dim": "D3", "mode": "coverage",
        "id": "CQ-21", "level": "L4", "dim": "D3", "mode": "coverage",
        "question": "Which reified domain assertions carry both an authoritative "
                    "source URI and a bibliographic citation?",
        "rationale": "Provenance completeness - the scientific-defensibility claim "
                     "of the KG.",
                    "of the KG.",
        "num": PREFIX + """SELECT DISTINCT ?ax WHERE {
  ?ax a owl:Axiom ; dcterms:source ?src ; dcterms:bibliographicCitation ?cit }""",
        "den": PREFIX + "SELECT DISTINCT ?ax WHERE { ?ax a owl:Axiom }",
        "unit": "reified axiom",
    },
    {
        "id": "CQ-20", "level": "L4", "dim": "D3", "mode": "negative",
        "id": "CQ-22", "level": "L4", "dim": "D3", "mode": "negative",
        "question": "Are there reified axioms with incomplete provenance "
                    "(missing source, citation or evidence type)?",
        "rationale": "Integrity constraint complementing CQ-19.",
        "num": PREFIX + """SELECT ?ax WHERE {
  ?ax a owl:Axiom .
  FILTER ( NOT EXISTS { ?ax dcterms:source ?s } ||
           NOT EXISTS { ?ax dcterms:bibliographicCitation ?c } ||
           NOT EXISTS { ?ax rice:evidenceType ?e } ) }""",
    },
    {
        "id": "CQ-21", "level": "L4", "dim": "D3", "mode": "coverage",
        "id": "CQ-23", "level": "L4", "dim": "D3", "mode": "coverage",
        "question": "Which biological entities (disease, pathogen, pest) are aligned "
                    "to an external vocabulary (EPPO, AGROVOC or NCBI Taxonomy)?",
        "rationale": "Interoperability. Written as a coverage measure rather than an "
                     "OPTIONAL projection, which would report success even when "
                     "every alignment column is null.",
                    "OPTIONAL projection, which would report success even when "
                    "every alignment column is null.",
        "num": PREFIX + """SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pathogen } UNION { ?e a rice:Pest }
  { ?e rice:eppoCode ?c } UNION { ?e skos:exactMatch ?m } UNION { ?e skos:closeMatch ?m2 } }""",
        "den": PREFIX + """SELECT DISTINCT ?e WHERE {
  { ?e a rice:Disease } UNION { ?e a rice:Pathogen } UNION { ?e a rice:Pest } }""",
        "unit": "biological entity",
    },
    {
        "id": "CQ-22", "level": "L4", "dim": "D3", "mode": "negative",
        "id": "CQ-24", "level": "L4", "dim": "D3", "mode": "negative",
        "question": "Are annotation literals lexically consistent, i.e. is "
                    "rice:evidenceType uniformly language-tagged?",
        "rationale": "Literal-hygiene constraint. An untagged duplicate of a tagged "
                     "value silently splits GROUP BY and breaks lang() filters.",
                    "value silently splits GROUP BY and breaks lang() filters.",
        "num": PREFIX + """SELECT ?ax ?v WHERE {
  ?ax rice:evidenceType ?v . FILTER ( lang(?v) = "" ) }""",
    },
    {
        "id": "CQ-23", "level": "L4", "dim": "D1", "mode": "negative",
        "id": "CQ-25", "level": "L4", "dim": "D1", "mode": "negative",
        "question": "Under entailment, is any individual typed as both a Symptom "
                    "and a Disease?",
        "rationale": "Category discipline. Symptom and Disease are intended to be "
                     "disjoint; an overlap means either a mistyped individual or a "
                     "property domain that is declared too narrowly. This constraint "
                     "is checked on the materialised graph, because the conflict is "
                     "produced by inference and is invisible in the asserted triples.",
                    "disjoint; an overlap means either a mistyped individual or a "
                    "property domain that is declared too narrowly. This constraint "
                    "is checked on the materialised graph, because the conflict is "
                    "produced by inference and is invisible in the asserted triples.",
        "num": PREFIX + """SELECT DISTINCT ?x WHERE {
  ?x a rice:Symptom . ?x a rice:Disease }""",
        "on_entailed": True,
    },
]


# -- Engine --------------------------------------------------------------------
def short(term) -> str:
    if term is None:
        return "-"
    return str(term).replace(RICE_NS, "rice:")


def select(graph: Graph, query: str):
    return list(graph.query(query))


def first_col(rows):
    return {short(r[0]) for r in rows}


def evaluate(cq, g_asserted, g_entailed):
    t0 = time.perf_counter()
    out = {"id": cq["id"], "level": cq["level"], "dim": cq["dim"],
           "mode": cq["mode"], "question": cq["question"],
           "rationale": cq["rationale"]}
    try:
        if cq["mode"] == "coverage":
            num = select(g_entailed, cq["num"])
            den = select(g_entailed, cq["den"])
            have, total = first_col(num), first_col(den)
            ratio = len(have) / len(total) if total else 0.0
            out.update(covered=len(have), total=len(total), ratio=ratio,
                       missing=sorted(total - have), unit=cq.get("unit", "item"))
            out["status"] = ("PASS" if ratio >= COVERAGE_THRESHOLD
                             else "FAIL" if ratio == 0 else "PARTIAL")
            if "detail" in cq:
                rows = select(g_entailed, cq["detail"])
                out["detail_rows"] = [[short(c) for c in r] for r in rows[:12]]
                out["detail_vars"] = [str(v) for v in rows[0].labels] if rows else []
                out["detail_total"] = len(rows)

        elif cq["mode"] == "negative":
            graph = g_entailed if cq.get("on_entailed") else g_asserted
            rows = select(graph, cq["num"])
            out.update(violations=len(rows),
                       examples=[[short(c) for c in r] for r in rows[:8]])
            out["status"] = "PASS" if len(rows) == 0 else "FAIL"

        elif cq["mode"] == "entailment":
            a = len(select(g_asserted, cq["num"]))
            e = len(select(g_entailed, cq["num"]))
            out.update(asserted=a, entailed=e, gain=e - a)
            out["status"] = ("PASS" if e > a and e >= cq["expect"]["min_entailed"]
                             else "FAIL")

        elif cq["mode"] == "documented":
            n = len(select(g_entailed, cq["num"]))
            out.update(count=n, status="DOCUMENTED")

        out["ms"] = round((time.perf_counter() - t0) * 1000, 1)
    except Exception as exc:
        out.update(status="ERROR", error=str(exc),
                   ms=round((time.perf_counter() - t0) * 1000, 1))
    return out


def write_report(meta, results):
    scored = [r for r in results if r["status"] != "DOCUMENTED"]
    tally = {st: sum(1 for r in scored if r["status"] == st)
             for st in ("PASS", "PARTIAL", "FAIL", "ERROR")}

    L = []
    A = L.append
    A("# Rice MMKG - Competency Question SPARQL Benchmark")
    A("")
    A(f"**Generated:** {meta['generated']}  ")
    A(f"**Ontology:** `{meta['ontology']}`  ")
    A(f"**Asserted triples:** {meta['asserted_triples']:,}  ")
    A(f"**After OWL RL materialisation:** {meta['entailed_triples']:,} "
      f"(+{meta['entailed_triples']-meta['asserted_triples']:,}, "
      f"{meta['reasoning_seconds']}s)  ")
    A(f"**Coverage threshold:** {meta['coverage_threshold']:.0%}")
    A("")
    A("## 1. Evaluation design")
    A("")
    A("Competency Questions are organised on **two independent axes** rather than a "
      "single ladder. Reasoning depth and knowledge dimension are orthogonal: "
      "provenance and cross-modal grounding are *dimensions* a query ranges over, "
      "not a deeper form of inference.")
    A("")
    A("| Reasoning depth | Meaning |")
    A("|---|---|")
    for k, v in LEVELS.items():
        A(f"| **{k}** | {v} |")
    A("")
    A("| Dimension | Meaning |")
    A("|---|---|")
    for k, v in DIMENSIONS.items():
        A(f"| **{k}** | {v} |")
    A("")
    A("### Evaluation contract")
    A("")
    A("Each CQ declares in advance what counts as a correct answer. A query "
      "returning rows is *not* by itself evidence of competency.")
    A("")
    A("| Mode | PASS criterion | Purpose |")
    A("|---|---|---|")
    A(f"| `coverage` | covered / total >= {meta['coverage_threshold']:.0%} | how much of a "
      "class the relation actually reaches; uncovered members are listed |")
    A("| `negative` | exactly 0 rows | integrity constraint - rows are violations |")
    A("| `entailment` | entailed > asserted | proves OWL reasoning contributes "
      "answers SPARQL alone cannot |")
    A("| `documented` | not scored | declared extension point, recorded to keep "
      "the gap visible |")
    A("")
    A("All mandatory hops are expressed **without `OPTIONAL`**. This is the "
      "decisive rule of the benchmark: `OPTIONAL` on a hop under test makes a CQ "
      "unfalsifiable.")
    A("")
    A("## 2. Summary")
    A("")
    A("| Outcome | Count | Share |")
    A("|---|---|---|")
    for st in ("PASS", "PARTIAL", "FAIL", "ERROR"):
        A(f"| {st} | {tally[st]} | {tally[st]/len(scored)*100:.0f}% |")
    A(f"| **Scored total** | **{len(scored)}** | **100%** |")
    A(f"| *(documented, unscored)* | *{len(results)-len(scored)}* | - |")
    A("")
    A("### Result matrix")
    A("")
    A("| CQ | Depth | Dim | Mode | Outcome | Measurement |")
    A("|---|---|---|---|---|---|")
    for r in results:
        if r["status"] == "ERROR":
            m = r.get("error", "")[:60]
        elif r["mode"] == "coverage":
            m = f"{r['covered']}/{r['total']} {r['unit']} ({r['ratio']*100:.0f}%)"
        elif r["mode"] == "negative":
            m = f"{r['violations']} violation(s)"
        elif r["mode"] == "entailment":
            m = f"{r['asserted']} asserted -> {r['entailed']} entailed"
        else:
            m = f"{r['count']} individual(s)"
        A(f"| {r['id']} | {r['level']} | {r['dim']} | `{r['mode']}` | "
          f"**{r['status']}** | {m} |")
    A("")
    A("## 3. Results in detail")
    A("")
    for r in results:
        A(f"### {r['id']} - {LEVELS[r['level']]} / {DIMENSIONS[r['dim']]} "
          f"- **{r['status']}**")
        A("")
        A(f"**Question.** {r['question']}")
        A("")
        A(f"**Why this CQ.** {r['rationale']}")
        A("")
        if r["status"] == "ERROR":
            A(f"**Error.** `{r['error']}`")
            A("")
            A("---")
            A("")
            continue
        if r["mode"] == "coverage":
            A(f"**Measurement.** {r['covered']} of {r['total']} {r['unit']} "
              f"covered - {r['ratio']*100:.1f}% ({r['ms']} ms).")
            A("")
            if r["missing"]:
                A(f"**Not covered ({len(r['missing'])}).** " +
                  ", ".join(f"`{m}`" for m in r["missing"][:25]) +
                  (" ..." if len(r["missing"]) > 25 else ""))
                A("")
            if r.get("detail_rows"):
                A(f"**Instantiations** ({r['detail_total']} total, first "
                  f"{len(r['detail_rows'])} shown):")
                A("")
                A("| " + " | ".join(r["detail_vars"]) + " |")
                A("|" + "---|" * len(r["detail_vars"]))
                for row in r["detail_rows"]:
                    A("| " + " | ".join(row) + " |")
                A("")
        elif r["mode"] == "negative":
            A(f"**Measurement.** {r['violations']} violation(s) ({r['ms']} ms). "
              f"Constraint {'holds' if r['violations'] == 0 else 'is broken'}.")
            A("")
            if r["examples"]:
                A("**Violating rows (sample):**")
                A("")
                for ex in r["examples"]:
                    A("- " + " / ".join(f"`{c}`" for c in ex))
                A("")
        elif r["mode"] == "entailment":
            A(f"**Measurement.** {r['asserted']} answer(s) on the asserted graph, "
              f"{r['entailed']} after OWL RL materialisation "
              f"(**+{r['gain']}** contributed by reasoning, {r['ms']} ms).")
            A("")
        else:
            A(f"**Measurement.** {r['count']} individual(s) ({r['ms']} ms). "
              f"Recorded, not scored.")
            A("")
        A("---")
        A("")
    REPORT_OUT.write_text("\n".join(L), encoding="utf-8")


def main():
    print(f"Loading ontology:\n  {ONTOLOGY}")
    g_asserted = Graph()
    g_asserted.parse(str(ONTOLOGY), format="xml")
    n_asserted = len(g_asserted)
    print(f"  {n_asserted:,} asserted triples.")

    print("Materialising OWL RL closure ...", end=" ", flush=True)
    t0 = time.perf_counter()
    g_entailed = Graph()
    g_entailed += g_asserted
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics,
                           axiomatic_triples=False,
                           datatype_axioms=False).expand(g_entailed)
    reason_s = time.perf_counter() - t0
    n_entailed = len(g_entailed)
    print(f"{n_entailed:,} triples (+{n_entailed - n_asserted:,}) in {reason_s:.1f}s\n")

    results = []
    for cq in CQS:
        print(f"  {cq['id']} [{cq['level']}/{cq['dim']}] ...", end=" ", flush=True)
        r = evaluate(cq, g_asserted, g_entailed)
        results.append(r)
        extra = ""
        if r["status"] == "ERROR":
            extra = r["error"][:70]
        elif r["mode"] == "coverage":
            extra = f"{r['covered']}/{r['total']} ({r['ratio']*100:.0f}%)"
        elif r["mode"] == "negative":
            extra = f"{r['violations']} violation(s)"
        elif r["mode"] == "entailment":
            extra = f"asserted {r['asserted']} -> entailed {r['entailed']}"
        elif r["mode"] == "documented":
            extra = f"count {r['count']}"
        print(f"{r['status']:<10} {extra}")

    meta = {"generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "ontology": ONTOLOGY.name,
            "asserted_triples": n_asserted,
            "entailed_triples": n_entailed,
            "reasoning_seconds": round(reason_s, 1),
            "coverage_threshold": COVERAGE_THRESHOLD}
    JSON_OUT.write_text(json.dumps({"meta": meta, "results": results},
                                   indent=2, ensure_ascii=False), encoding="utf-8")
    write_report(meta, results)

    scored = [r for r in results if r["status"] != "DOCUMENTED"]
    print("\n" + "=" * 64)
    for st in ("PASS", "PARTIAL", "FAIL", "ERROR"):
        n = sum(1 for r in scored if r["status"] == st)
        print(f"  {st:<9} {n}/{len(scored)}")
    print("=" * 64)
    print(f"Report: {REPORT_OUT}")


if __name__ == "__main__":
    main()
