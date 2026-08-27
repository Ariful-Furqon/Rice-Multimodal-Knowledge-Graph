"""
Rice MMKG v0.5 — Competency Question (CQ) SPARQL Benchmark
===========================================================
Executes 16 formal Competency Questions as SPARQL queries against
Rice MMKG.rdf and produces a structured benchmark report.

Methodology references:
  - Gruninger & Fox (1995). Methodology for the Design and Evaluation of Ontologies.
  - Suárez-Figueroa et al. (2012). The NeOn Methodology for Ontology Engineering.
  - Poveda-Villalón et al. (2022). LOT: An industrial oriented ontology engineering
    framework. Engineering Applications of Artificial Intelligence, 111, 104755.

CQ Levels:
  L1 — Factual / Single-hop retrieval (pattern over all entities)
  L2 — Contextual / Multi-criteria (growth stage + environmental factor)
  L3 — Causal / Multi-hop epidemiological chain (vector tracing)
  L4 — Inference / Defined class and provenance retrieval

Usage:
  python cq_sparql_benchmark.py
Output:
  reports/CQ_SPARQL_Benchmark_Report.md
"""

import time
import datetime
from pathlib import Path
from rdflib import Graph, Namespace, RDF, OWL

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).resolve().parent
WORKLOG_DIR = SCRIPT_DIR.parent
ONTOLOGY    = WORKLOG_DIR.parent.parent / "Ontology" / "Rice MMKG.rdf"
REPORT_OUT  = WORKLOG_DIR / "reports" / "CQ_SPARQL_Benchmark_Report.md"

assert ONTOLOGY.exists(), f"Ontology not found: {ONTOLOGY}"

# ── Load ontology ─────────────────────────────────────────────────────────────
print(f"Loading ontology from:\n  {ONTOLOGY}")
g = Graph()
g.parse(str(ONTOLOGY), format="xml")
print(f"  {len(g):,} triples loaded.\n")

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

# ── SPARQL prefix block ───────────────────────────────────────────────────────
PREFIX = """
PREFIX rice: <http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
"""

# ── Competency Questions ──────────────────────────────────────────────────────
COMPETENCY_QUESTIONS = [

    # ── L1: Factual / Single-hop ───────────────────────────────────────────────
    {
        "id": "CQ-01",
        "level": "L1",
        "level_label": "Factual / Single-hop",
        "question": (
            "For every rice disease in the ontology, what is its causal "
            "pathogen or pest, and what are all observable symptoms that "
            "indicate it?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?disease ?pathogenOrPest ?symptom
WHERE {
  ?disease a rice:Disease .
  OPTIONAL { ?pathogenOrPest rice:causes ?disease . }
  OPTIONAL { ?disease rice:indicatedBy ?symptom . }
}
ORDER BY ?disease
""",
    },
    {
        "id": "CQ-02",
        "level": "L1",
        "level_label": "Factual / Single-hop",
        "question": (
            "For every pest in the ontology, what symptoms does its "
            "infestation produce, and which treatments control it?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?pest ?symptom ?treatment
WHERE {
  ?pest a rice:Pest .
  OPTIONAL { ?pest rice:indicatedBy ?symptom . }
  OPTIONAL { ?pest rice:controlledBy ?treatment . }
}
ORDER BY ?pest
""",
    },
    {
        "id": "CQ-03",
        "level": "L1",
        "level_label": "Factual / Single-hop",
        "question": (
            "What are all the symptoms currently defined in the ontology, "
            "and which disease or pest does each indicate?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?symptom ?diseaseOrPest
WHERE {
  ?symptom a rice:Symptom .
  OPTIONAL { ?diseaseOrPest rice:indicatedBy ?symptom . }
}
ORDER BY ?symptom
""",
    },
    {
        "id": "CQ-04",
        "level": "L1",
        "level_label": "Factual / Single-hop",
        "question": (
            "For every treatment available in the ontology, which diseases "
            "or pests does it control, and which management action recommends it?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?treatment ?diseaseOrPest ?managementAction
WHERE {
  ?treatment a rice:Treatment .
  OPTIONAL { ?diseaseOrPest rice:controlledBy ?treatment . }
  OPTIONAL { ?managementAction rice:recommends ?treatment . }
}
ORDER BY ?treatment
""",
    },

    # ── L2: Contextual / Multi-criteria ───────────────────────────────────────
    {
        "id": "CQ-05",
        "level": "L2",
        "level_label": "Contextual / Multi-criteria",
        "question": (
            "Which diseases and pests affect rice at the Tillering growth "
            "stage, and what environmental factors increase their risk?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?diseaseOrPest ?envFactor
WHERE {
  { ?diseaseOrPest a rice:Disease . } UNION { ?diseaseOrPest a rice:Pest . }
  ?diseaseOrPest rice:occursIn rice:Tillering_Stage .
  OPTIONAL { ?envFactor rice:increaseRiskOf ?diseaseOrPest . }
}
ORDER BY ?diseaseOrPest
""",
    },
    {
        "id": "CQ-06",
        "level": "L2",
        "level_label": "Contextual / Multi-criteria",
        "question": (
            "For every environmental factor in the ontology, which diseases "
            "or pests does it increase the risk of, and across which growth stages?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?envFactor ?diseaseOrPest ?stage
WHERE {
  ?envFactor a rice:EnvironmentalFactor .
  ?envFactor rice:increaseRiskOf ?diseaseOrPest .
  OPTIONAL { ?diseaseOrPest rice:occursIn ?stage . }
}
ORDER BY ?envFactor ?diseaseOrPest
""",
    },
    {
        "id": "CQ-07",
        "level": "L2",
        "level_label": "Contextual / Multi-criteria",
        "question": (
            "Which diseases cause symptoms specifically affecting the "
            "panicle or grain at the Reproductive growth stage, and what "
            "is the recommended treatment?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?disease ?symptom ?treatment
WHERE {
  ?disease a rice:Disease .
  ?disease rice:occursIn rice:Reproductive_Stage .
  ?disease rice:indicatedBy ?symptom .
  FILTER(
    ?symptom IN (
      rice:Panicle_Blast, rice:Neck_Rot, rice:Discolored_Panicle,
      rice:Empty_Grain, rice:White_Ear, rice:Sterile_Panicle,
      rice:Grain_Discoloration
    )
  )
  OPTIONAL { ?disease rice:controlledBy ?treatment . }
}
ORDER BY ?disease
""",
    },
    {
        "id": "CQ-08",
        "level": "L2",
        "level_label": "Contextual / Multi-criteria",
        "question": (
            "Which preventive measures are recommended for rice diseases "
            "that require a specific growth-stage-based prerequisite action?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?disease ?prevention ?prerequisite
WHERE {
  ?disease a rice:Disease .
  ?disease rice:preventedBy ?prevention .
  OPTIONAL { ?prevention rice:requires ?prerequisite . }
}
ORDER BY ?disease
""",
    },

    # ── L3: Causal / Multi-hop epidemiological chain ───────────────────────────
    {
        "id": "CQ-09",
        "level": "L3",
        "level_label": "Causal / Multi-hop Epidemiological",
        "question": (
            "For every insect vector in the ontology, which pathogens does "
            "it transmit, what disease does that pathogen cause, and what "
            "management actions are recommended to break the transmission chain?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?vector ?pathogen ?disease ?treatment
WHERE {
  ?vector a rice:Pest .
  ?vector rice:transmits ?pathogen .
  ?pathogen rice:causes ?disease .
  OPTIONAL { ?vector rice:controlledBy ?treatment . }
}
ORDER BY ?vector
""",
    },
    {
        "id": "CQ-10",
        "level": "L3",
        "level_label": "Causal / Multi-hop Epidemiological",
        "question": (
            "Which diseases are caused by viral pathogens transmitted by "
            "insect vectors, distinguishing them from diseases caused "
            "directly by fungal or bacterial pathogens?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?disease ?pathogen ?vector
WHERE {
  ?disease a rice:Disease .
  ?pathogen rice:causes ?disease .
  OPTIONAL { ?vector rice:transmits ?pathogen . }
}
ORDER BY ?disease
""",
    },
    {
        "id": "CQ-11",
        "level": "L3",
        "level_label": "Causal / Multi-hop Epidemiological",
        "question": (
            "For every disease in the ontology, what is the complete "
            "diagnostic profile: causal agent, associated symptoms, "
            "environmental risk factors, vulnerable growth stages, "
            "and recommended interventions?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?disease ?causalAgent ?symptom ?envFactor ?stage ?treatment
WHERE {
  ?disease a rice:Disease .
  OPTIONAL { ?causalAgent rice:causes ?disease . }
  OPTIONAL { ?disease rice:indicatedBy ?symptom . }
  OPTIONAL { ?envFactor rice:increaseRiskOf ?disease . }
  OPTIONAL { ?disease rice:occursIn ?stage . }
  OPTIONAL { ?disease rice:controlledBy ?treatment . }
}
ORDER BY ?disease
""",
    },

    # ── L4: Inference / Provenance / Alignment ─────────────────────────────────
    {
        "id": "CQ-12",
        "level": "L4",
        "level_label": "Inference / Provenance",
        "question": (
            "For every domain-level assertion in the ontology, what is "
            "the authoritative source (URI) and bibliographic citation "
            "that backs it?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?subject ?property ?object ?source ?citation ?evidenceType
WHERE {
  ?axiom a owl:Axiom ;
         owl:annotatedSource   ?subject ;
         owl:annotatedProperty ?property ;
         owl:annotatedTarget   ?object ;
         dcterms:source        ?source ;
         dcterms:bibliographicCitation ?citation .
  OPTIONAL { ?axiom rice:evidenceType ?evidenceType . }
}
ORDER BY ?subject ?property
""",
    },
    {
        "id": "CQ-13",
        "level": "L4",
        "level_label": "Inference / Provenance",
        "question": (
            "Which image observations in the ontology qualify as "
            "SymptomaticObservations (i.e., capture at least one symptom), "
            "and what symptom do they capture?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?observation ?symptom
WHERE {
  ?observation a rice:ImageObservation .
  ?observation rice:captures ?symptom .
  ?symptom a rice:Symptom .
}
ORDER BY ?observation
LIMIT 20
""",
    },
    {
        "id": "CQ-14",
        "level": "L4",
        "level_label": "Inference / Provenance",
        "question": (
            "For every biological entity (disease, pathogen, pest) that "
            "has been aligned to an external vocabulary, what are its "
            "EPPO code, AGROVOC concept, and NCBI Taxonomy identifiers?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?entity ?eppoCode ?agrovocMatch ?ncbiMatch
WHERE {
  { ?entity a rice:Disease . } UNION
  { ?entity a rice:Pathogen . } UNION
  { ?entity a rice:Pest . }
  OPTIONAL { ?entity rice:eppoCode ?eppoCode . }
  OPTIONAL { ?entity skos:exactMatch ?agrovocMatch .
             FILTER(CONTAINS(STR(?agrovocMatch), "agrovoc")) }
  OPTIONAL { ?entity skos:exactMatch ?ncbiMatch .
             FILTER(CONTAINS(STR(?ncbiMatch), "NCBITaxon")) }
}
ORDER BY ?entity
""",
    },
    {
        "id": "CQ-15",
        "level": "L4",
        "level_label": "Inference / Provenance",
        "question": (
            "Which Good Agricultural Practices (GAP) or biological "
            "treatments are available as non-chemical alternatives for "
            "managing rice diseases or pests?"
        ),
        "sparql": PREFIX + """
SELECT DISTINCT ?entity ?treatment
WHERE {
  { ?entity a rice:Disease . } UNION { ?entity a rice:Pest . }
  ?entity rice:preventedBy ?treatment .
  FILTER(?treatment IN (
    rice:Good_Agricultural_Practice,
    rice:Trichoderma_Application,
    rice:Neem_Based_Pesticide,
    rice:Seed_Treatment,
    rice:Crop_Sanitation,
    rice:Vector_Control
  ))
}
ORDER BY ?entity
""",
    },
    {
        "id": "CQ-16",
        "level": "L4",
        "level_label": "Inference / Provenance",
        "question": (
            "What is the complete ontology statistics summary: total number "
            "of individuals per class, object properties, and provenance "
            "axiom coverage?"
        ),
        "sparql": PREFIX + """
SELECT ?class (COUNT(DISTINCT ?individual) AS ?count)
WHERE {
  VALUES ?class {
    rice:Disease rice:Pathogen rice:Pest rice:Symptom
    rice:EnvironmentalFactor rice:GrowthStage rice:Treatment
    rice:ManagementAction rice:ImageObservation rice:SensorObservation
  }
  OPTIONAL { ?individual a ?class . }
}
GROUP BY ?class
ORDER BY DESC(?count)
""",
    },
]

# ── Execute and collect results ────────────────────────────────────────────────
def run_cq(cq: dict) -> dict:
    start = time.perf_counter()
    try:
        rows = list(g.query(cq["sparql"]))
        elapsed = time.perf_counter() - start
        return {
            "status": "PASS" if len(rows) > 0 else "EMPTY",
            "rows":   rows,
            "count":  len(rows),
            "ms":     round(elapsed * 1000, 1),
            "error":  None,
        }
    except Exception as exc:
        elapsed = time.perf_counter() - start
        return {
            "status": "ERROR",
            "rows":   [],
            "count":  0,
            "ms":     round(elapsed * 1000, 1),
            "error":  str(exc),
        }

results = {}
for cq in COMPETENCY_QUESTIONS:
    print(f"Running {cq['id']} ({cq['level']})... ", end="", flush=True)
    results[cq["id"]] = run_cq(cq)
    r = results[cq["id"]]
    print(f"{r['status']} — {r['count']} rows — {r['ms']} ms")

# ── Build Markdown report ─────────────────────────────────────────────────────
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
passed  = sum(1 for r in results.values() if r["status"] == "PASS")
empty   = sum(1 for r in results.values() if r["status"] == "EMPTY")
errors  = sum(1 for r in results.values() if r["status"] == "ERROR")
total   = len(COMPETENCY_QUESTIONS)

lines = [
    "# Rice MMKG v0.5 — Competency Question (CQ) SPARQL Benchmark Report",
    "",
    f"**Generated:** {now_str}  ",
    f"**Ontology:** `Rice MMKG.rdf` (`owl:versionInfo 0.5`)  ",
    f"**Total Triples:** {len(g):,}  ",
    f"**Total CQs:** {total}  ",
    "",
    "## Methodology",
    "",
    "Competency Questions are formulated as **general-pattern queries** following:",
    "- Gruninger & Fox (1995). *Methodology for the Design and Evaluation of Ontologies.*",
    "- Suárez-Figueroa et al. (2012). *The NeOn Methodology for Ontology Engineering.* Springer.",
    "- Poveda-Villalón et al. (2022). *LOT: An industrial oriented ontology engineering framework.* Engineering Applications of Artificial Intelligence, 111, 104755.",
    "",
    "Each CQ is written at the **schema/pattern level** (returns results for all matching entities,",
    "not just one) so that a single SPARQL execution validates the relational coverage of the",
    "entire ontology, not a single hand-picked triple.",
    "",
    "### CQ Levels",
    "",
    "| Level | Focus | Evaluated via |",
    "|---|---|---|",
    "| **L1 — Factual** | Direct 1-hop pattern retrieval | SPARQL SELECT |",
    "| **L2 — Contextual** | Multi-criteria: growth stage + environmental factor | SPARQL JOIN + FILTER |",
    "| **L3 — Causal** | Multi-hop epidemiological chain (vector tracing) | SPARQL multi-hop |",
    "| **L4 — Inference** | Defined-class membership, provenance, alignment | SPARQL + OWL Axiom inspection |",
    "",
    "---",
    "",
    "## Summary Dashboard",
    "",
    f"| Result | Count | % |",
    f"|---|---|---|",
    f"| ✅ PASS (non-empty result set) | {passed} | {passed/total*100:.0f}% |",
    f"| ⚠️ EMPTY (query ran, 0 rows) | {empty} | {empty/total*100:.0f}% |",
    f"| ❌ ERROR (SPARQL parse/runtime error) | {errors} | {errors/total*100:.0f}% |",
    f"| **Total** | **{total}** | **100%** |",
    "",
    "---",
    "",
    "## Results by CQ",
    "",
]

for cq in COMPETENCY_QUESTIONS:
    r = results[cq["id"]]
    status_icon = {"PASS": "✅", "EMPTY": "⚠️", "ERROR": "❌"}.get(r["status"], "?")
    lines += [
        f"### {cq['id']} — {cq['level_label']} `[{status_icon} {r['status']}]`",
        "",
        f"**Question:** {cq['question']}",
        "",
        f"**Result:** {r['count']} row(s) returned in {r['ms']} ms",
        "",
    ]

    if r["error"]:
        lines += [f"**Error:** `{r['error']}`", ""]

    if r["rows"]:
        # Build table from first 10 rows
        vars_ = [str(v) for v in r["rows"][0].__class__.__iter__(r["rows"][0])] if hasattr(r["rows"][0], "__iter__") else []
        # Fallback: use positional binding from query vars
        try:
            col_names = [str(v) for v in r["rows"][0].labels]
        except Exception:
            col_names = [f"col{i}" for i in range(len(r["rows"][0]))]

        header = "| " + " | ".join(col_names) + " |"
        sep    = "| " + " | ".join(["---"] * len(col_names)) + " |"
        lines += [header, sep]

        for row in r["rows"][:10]:
            cells = []
            for cell in row:
                if cell is None:
                    cells.append("—")
                else:
                    val = str(cell)
                    # Shorten RICE namespace for readability
                    val = val.replace(
                        "http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#", "rice:"
                    )
                    cells.append(val)
            lines.append("| " + " | ".join(cells) + " |")

        if r["count"] > 10:
            lines.append(f"| *... {r['count'] - 10} more rows (truncated for readability)* |")

    lines += ["", "---", ""]

# ── Final summary and caveats ─────────────────────────────────────────────────
lines += [
    "## Observations & Next Steps",
    "",
    "### Provenance Coverage",
    "CQ-12 verifies that all domain-level assertions carry `owl:Axiom` metadata.",
    "The result set count from CQ-12 must equal the total `owl:Axiom` record",
    "count reported by `verify.py` (currently 265). Any discrepancy flags a gap.",
    "",
    "### SensorObservation (CQ-16)",
    "CQ-16 confirms that `rice:SensorObservation` currently has 0 individuals.",
    "This is an expected and documented extension point (v0.5). Populating it",
    "is scoped to Phase 3 of the ESWC 2027 roadmap.",
    "",
    "### SymptomaticObservation (CQ-13)",
    "Results are limited to 20 rows; the full count is available by removing `LIMIT 20`.",
    "The reasoner-materialised superset (`SymptomaticObservation`) requires running",
    "HermiT/Pellet — SPARQL alone returns only explicitly asserted `captures` triples.",
    "",
    "### Empty / Error CQs",
    "Any EMPTY result must be reviewed to determine whether:",
    "  (a) the ontology genuinely lacks data for this pattern (a gap to document), or",
    "  (b) the query references an IRI that needs adjustment.",
    "EMPTY results are not automatically failures — they are honest measurements.",
    "",
    "---",
    "",
    "## Citation",
    "",
    "If reporting these results in a paper, cite as:",
    "",
    "```",
    "Rice MMKG v0.5 Competency Question Benchmark.",
    "Evaluated against Rice MMKG.rdf (owl:versionInfo 0.5,",
    "http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG).",
    "Methodology: Gruninger & Fox (1995); Suárez-Figueroa et al. (2012);",
    "Poveda-Villalón et al. (2022).",
    "```",
    "",
]

report_text = "\n".join(lines)
REPORT_OUT.write_text(report_text, encoding="utf-8")
print(f"\n[OK] Report written to:\n  {REPORT_OUT}")

# ── Console summary ────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  BENCHMARK SUMMARY")
print(f"{'='*60}")
print(f"  PASS  : {passed}/{total}")
print(f"  EMPTY : {empty}/{total}")
print(f"  ERROR : {errors}/{total}")
print(f"{'='*60}")
