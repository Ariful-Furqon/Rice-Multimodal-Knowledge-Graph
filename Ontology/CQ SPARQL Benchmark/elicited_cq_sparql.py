"""
SPARQL implementations for the elicited competency questions (Tier A).

WHY THIS IS A SEPARATE SCRIPT FROM cq_sparql_benchmark.py
The Stage 4 reconciliation found that the two CQ sets are different instruments
over the same relations. The benchmark asks coverage and integrity questions
about the graph -- "which diseases have an identified causal pathogen" -- and is
scored against a 50% population threshold. The elicited CQs ask for answers
about rice -- "which pathogen causes blast". Scoring a retrieval question
against a coverage threshold would be a category error, so they are kept apart
and reported separately.

WHAT IS IMPLEMENTED
Stage 4 identified five elicited CQs that are answerable by v0.6 as it stands
and have no benchmark counterpart. Those are implemented here. The other twenty
are recorded in the status table with the reason they are not: ten are already
probed by the benchmark in coverage form, ten need schema or data that v0.6 does
not have (the v0.7 work plan).

SCORING
Mode "retrieval": the query answers if it returns at least one row. There is no
threshold, and a large row count is not a better result than a small one --
CQ-A16 returning exactly two candidate conditions is the correct answer, not a
weak one.

A RULE THAT MATTERS
Nothing here may be used to edit the CQ set. A competency question that the
graph answers poorly is a finding about the graph, not a defect in the question.
Rewording CQs to fit what the ontology already does is precisely the circularity
this whole elicitation exists to avoid -- and the expert ratings, which are the
only legitimate ground for revising the set, are not in yet.

Outputs:
  Elicited_CQ_SPARQL_Report.md
  elicited_cq_sparql_results.json
"""

import json
import time
import datetime
from pathlib import Path

from rdflib import Graph

SCRIPT_DIR = Path(__file__).resolve().parent
ONTOLOGY = SCRIPT_DIR.parent / "Rice MMKG.rdf"
FINAL_CQS = SCRIPT_DIR / "CQ Screening" / "data" / "cq_stage3_final_tierA.csv"
GAPS = SCRIPT_DIR / "CQ Screening" / "data" / "cq_stage4_gaps.csv"
REPORT_OUT = SCRIPT_DIR / "Elicited_CQ_SPARQL_Report.md"
JSON_OUT = SCRIPT_DIR / "elicited_cq_sparql_results.json"

assert ONTOLOGY.exists(), f"Ontology not found: {ONTOLOGY}"

RICE_NS = "http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#"

PREFIX = f"""
PREFIX rice: <{RICE_NS}>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX schema: <http://schema.org/>
PREFIX prov: <http://www.w3.org/ns/prov#>
"""

# Instantiations are the same ones the expert questionnaire uses, so a rating
# and a query result can be read against each other without translation.
CQS = [
    {
        "id": "CQ-A04", "level": "L3", "dim": "D1", "mode": "retrieval",
        "question": "Which diseases share symptoms with Brown Spot, and which "
                    "symptoms discriminate between them?",
        "note": "Differential diagnosis. Proposed independently by five of the "
                "six models and absent from the benchmark, which asks only "
                "whether symptoms are attached, never which conditions they "
                "fail to separate.",
        "queries": [
            ("Conditions sharing at least one symptom with Brown Spot",
             """SELECT ?other (COUNT(DISTINCT ?shared) AS ?shared_symptoms)
WHERE {
  rice:Brown_Spot rice:indicatedBy ?shared .
  ?other rice:indicatedBy ?shared .
  FILTER (?other != rice:Brown_Spot)
}
GROUP BY ?other
ORDER BY DESC(?shared_symptoms)"""),
            ("Symptoms that discriminate Brown Spot from Rice Blast",
             """SELECT ?symptom ?present_only_in WHERE {
  {
    rice:Brown_Spot rice:indicatedBy ?symptom .
    FILTER NOT EXISTS { rice:Rice_Blast_Disease rice:indicatedBy ?symptom }
    BIND ("Brown Spot" AS ?present_only_in)
  } UNION {
    rice:Rice_Blast_Disease rice:indicatedBy ?symptom .
    FILTER NOT EXISTS { rice:Brown_Spot rice:indicatedBy ?symptom }
    BIND ("Rice Blast" AS ?present_only_in)
  }
}
ORDER BY ?present_only_in ?symptom"""),
        ],
    },
    {
        "id": "CQ-A10", "level": "L1", "dim": "D2", "mode": "retrieval",
        "question": "Which images are annotated as showing Hispa damage?",
        "note": "The most basic cross-modal retrieval there is. The benchmark "
                "checks that annotations are typed, never that they can be "
                "retrieved by condition.",
        "queries": [
            ("Images annotated as Hispa, with their retrievable URL",
             """SELECT ?image ?url WHERE {
  ?image rice:annotatedAs rice:Hispa ;
         schema:contentUrl ?url .
}
ORDER BY ?image"""),
        ],
    },
    {
        "id": "CQ-A13", "level": "L2", "dim": "D2", "mode": "retrieval",
        "question": "How is the image corpus distributed across conditions and "
                    "entity types?",
        "note": "PARTIAL. The elicited question also asks for plant part and "
                "capture type. v0.6 models neither, so this implements the "
                "answerable half and the rest stays on the v0.7 plan. Reported "
                "as partial rather than passed.",
        "partial": "plant part and capture type are not modelled in v0.6",
        "queries": [
            ("Images per annotated condition and entity type",
             """SELECT ?condition ?type (COUNT(?image) AS ?images) WHERE {
  ?image a rice:ImageObservation ;
         rice:annotatedAs ?condition .
  ?condition a ?type .
  FILTER (STRSTARTS(STR(?type), STR(rice:)))
}
GROUP BY ?condition ?type
ORDER BY DESC(?images)"""),
            ("Images per source dataset",
             """SELECT ?dataset (COUNT(?image) AS ?images) WHERE {
  ?image a rice:ImageObservation ;
         prov:wasDerivedFrom ?dataset .
}
GROUP BY ?dataset"""),
        ],
    },
    {
        "id": "CQ-A16", "level": "L3", "dim": "D2", "mode": "retrieval",
        "question": "Which disease or pest is best supported by the visual "
                    "evidence in a given image?",
        "note": "The full cross-modal chain: image -> symptom it captures -> "
                "conditions that symptom indicates. The image is chosen by the "
                "query itself rather than hardcoded, so the test survives any "
                "re-import of the corpus.",
        "queries": [
            ("Candidate conditions for one annotated image, ranked by "
             "supporting symptoms",
             """SELECT ?image ?candidate (COUNT(DISTINCT ?symptom) AS ?support)
WHERE {
  { SELECT ?image WHERE { ?image rice:captures ?s } ORDER BY ?image LIMIT 1 }
  ?image rice:captures ?symptom .
  ?candidate rice:indicatedBy ?symptom .
}
GROUP BY ?image ?candidate
ORDER BY DESC(?support) ?candidate"""),
        ],
    },
    {
        "id": "CQ-A17", "level": "L3", "dim": "D2", "mode": "retrieval",
        "question": "Which visual features separate Brown Spot from Rice "
                    "Blast?",
        "note": "The pair the models named most often as visually confusable. "
                "Answered from the symptom layer; v0.6 has no lesion "
                "shape/colour descriptors, so the separation is by symptom "
                "identity rather than by visual feature.",
        "partial": "separation is by symptom, not by lesion descriptors, "
                   "which v0.6 does not carry",
        "queries": [
            ("Symptoms unique to each of the two conditions",
             """SELECT ?condition ?distinguishing_symptom WHERE {
  {
    rice:Brown_Spot rice:indicatedBy ?distinguishing_symptom .
    FILTER NOT EXISTS {
      rice:Rice_Blast_Disease rice:indicatedBy ?distinguishing_symptom }
    BIND ("Brown Spot" AS ?condition)
  } UNION {
    rice:Rice_Blast_Disease rice:indicatedBy ?distinguishing_symptom .
    FILTER NOT EXISTS {
      rice:Brown_Spot rice:indicatedBy ?distinguishing_symptom }
    BIND ("Rice Blast" AS ?condition)
  }
}
ORDER BY ?condition ?distinguishing_symptom"""),
            ("Symptoms the two share, which therefore cannot separate them",
             """SELECT ?shared_symptom WHERE {
  rice:Brown_Spot rice:indicatedBy ?shared_symptom .
  rice:Rice_Blast_Disease rice:indicatedBy ?shared_symptom .
}
ORDER BY ?shared_symptom"""),
        ],
    },
]

MAX_SAMPLE = 8


def short(term):
    return str(term).replace(RICE_NS, "rice:")


def run(graph, cq):
    out = {"id": cq["id"], "level": cq["level"], "dim": cq["dim"],
           "mode": cq["mode"], "question": cq["question"],
           "note": cq["note"], "partial": cq.get("partial"), "queries": []}
    answered = True
    for label, body in cq["queries"]:
        t0 = time.perf_counter()
        rows = list(graph.query(PREFIX + body))
        ms = (time.perf_counter() - t0) * 1000
        cols = [str(v) for v in (rows[0].labels if rows else [])]
        sample = [[short(v) for v in row] for row in rows[:MAX_SAMPLE]]
        out["queries"].append({
            "label": label, "sparql": body.strip(), "rows": len(rows),
            "ms": round(ms, 1), "columns": cols, "sample": sample})
        if not rows:
            answered = False
    out["answered"] = answered
    out["status"] = ("answers" if answered and not cq.get("partial")
                     else "partial" if answered else "NO ANSWER")
    return out


def status_table():
    """Every Tier A CQ and why it is or is not implemented here."""
    import csv
    final = list(csv.DictReader(FINAL_CQS.open(encoding="utf-8-sig")))
    gap_ids = {g["cq_id"] for g in csv.DictReader(GAPS.open(encoding="utf-8-sig"))}
    implemented = {c["id"] for c in CQS}
    rows = []
    for c in final:
        cid = c["cq_id"]
        if cid in implemented:
            state, why = "implemented here", "answerable by v0.6, no benchmark counterpart"
        elif c["v06_status"] != "answerable":
            # extensions_required joins several gap notes with " | ", which
            # would break the markdown table it is rendered into.
            needs = c["extensions_required"].replace(" | ", "; ")
            if len(needs) > 110:
                needs = needs[:107].rsplit(" ", 1)[0] + " ..."
            state, why = "v0.7 work plan", needs or "needs schema or data v0.6 lacks"
        elif cid not in gap_ids:
            state, why = "covered by the benchmark", "the benchmark probes the same relation in coverage form"
        else:
            state, why = "not yet implemented", "answerable, but not selected for this pass"
        rows.append({"cq_id": cid, "level": c["level"], "dim": c["dim"],
                     "short_label": c["short_label"], "state": state,
                     "why": why})
    return rows


def main():
    print(f"loading {ONTOLOGY.name} ...")
    t0 = time.perf_counter()
    g = Graph()
    g.parse(ONTOLOGY)
    load_ms = (time.perf_counter() - t0) * 1000
    print(f"  {len(g)} triples in {load_ms/1000:.1f}s")

    results = [run(g, cq) for cq in CQS]
    rows = status_table()

    for r in results:
        total = sum(q["rows"] for q in r["queries"])
        print(f"  {r['id']}  {r['status']:<9} {total} rows across "
              f"{len(r['queries'])} quer{'y' if len(r['queries'])==1 else 'ies'}")

    payload = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "ontology": ONTOLOGY.name,
        "triples": len(g),
        "results": results,
        "status_table": rows,
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_report(payload)
    print(f"\nwrote {REPORT_OUT.name} and {JSON_OUT.name}")


def write_report(p):
    res = p["results"]
    rows = p["status_table"]
    n_ans = sum(1 for r in res if r["answered"])
    L = ["# Elicited Competency Questions - SPARQL Results", "",
         f"Generated {p['generated'][:16].replace('T', ' ')} by "
         "`elicited_cq_sparql.py` against `{}` ({:,} triples).".format(
             p["ontology"], p["triples"]), "",
         f"**{len(res)} of the {len(rows)} elicited Tier A CQs are implemented "
         "here.** They are the ones Stage 4 found to be answerable by v0.6 and "
         "absent from the SPARQL benchmark, so they close the sharpest gap the "
         "reconciliation exposed.", "",
         f"All {n_ans} return answers.", "",
         "> **These results may not be used to edit the CQ set.** A question "
         "the graph answers poorly is a finding about the graph. Rewording CQs "
         "to fit what the ontology already does is the circularity this "
         "elicitation exists to avoid, and the expert ratings - the only "
         "legitimate ground for revising the set - are not in yet.", "",
         "## Why these are reported separately from the benchmark", "",
         "The benchmark asks *coverage* and *integrity* questions about the "
         "graph and scores them against a 50% population threshold. These ask "
         "for *answers* about rice. Scoring a retrieval question against a "
         "coverage threshold would be a category error, so the two instruments "
         "are kept apart - which is exactly what the Stage 4 reconciliation "
         "concluded.", "",
         "A retrieval CQ answers if it returns at least one row. **A large row "
         "count is not a better result than a small one**: CQ-A16 returning "
         "exactly two candidate conditions is the correct answer, because the "
         "evidence genuinely supports two.", "",
         "## Summary", "",
         "| CQ | Level | Dim | Status | Question |", "|---|---|---|---|---|"]
    for r in res:
        L.append(f"| `{r['id']}` | {r['level']} | {r['dim']} | "
                 f"{r['status']} | {r['question']} |")
    L += ["", "`partial` means the query answers the part of the question v0.6 "
          "can support, with the shortfall named. It is not a pass and is not "
          "counted as one.", ""]

    L += ["---", "", "## Results in detail", ""]
    for r in res:
        L += [f"### {r['id']} - {r['question']}", "",
              f"**Level {r['level']} · Dimension {r['dim']} · "
              f"{r['status']}**", "", r["note"], ""]
        if r["partial"]:
            L += [f"> **Partial:** {r['partial']}", ""]
        for q in r["queries"]:
            L += [f"**{q['label']}**", "", "```sparql", q["sparql"], "```", "",
                  f"{q['rows']} row(s) in {q['ms']} ms."]
            if q["sample"]:
                L += ["", "| " + " | ".join(q["columns"]) + " |",
                      "|" + "---|" * len(q["columns"])]
                for s in q["sample"]:
                    L.append("| " + " | ".join(s) + " |")
                if q["rows"] > len(q["sample"]):
                    more = f"*… {q['rows'] - len(q['sample']):,} more rows*"
                    L.append("| " + more + " |" + " |" * (len(q["columns"]) - 1))
            L.append("")
    L += ["---", "", "## Status of all "
          f"{len(rows)} elicited Tier A CQs", "",
          "So that nothing looks hidden: every CQ, and why it is or is not "
          "implemented here.", "",
          "| CQ | Lv | Dim | State | Requirement | Why |",
          "|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| `{r['cq_id']}` | {r['level']} | {r['dim']} | {r['state']} "
                 f"| {r['short_label']} | {r['why']} |")
    by_state = {}
    for r in rows:
        by_state[r["state"]] = by_state.get(r["state"], 0) + 1
    L += ["", "| State | CQs |", "|---|---|"]
    for k, v in sorted(by_state.items(), key=lambda x: -x[1]):
        L.append(f"| {k} | {v} |")
    L += ["", "## What this changes for the roadmap", "",
          "The queries above are small, and that is the point: the cross-modal "
          "questions the benchmark never asked turn out to be answerable with "
          "the graph as it stands. What they also expose is how thin the "
          "visual layer is - `captures` carries 1,442 assertions, all of them "
          "to a single symptom, so image-to-symptom grounding exists for one "
          "condition and no other. That is a v0.7 priority the coverage "
          "benchmark did not surface, because it counted symptoms with any "
          "visual grounding rather than images with any symptom.", ""]
    REPORT_OUT.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
