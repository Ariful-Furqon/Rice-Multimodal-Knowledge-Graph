"""
Stage 4 of the CQ screening funnel: reconciliation with the existing benchmark.

Compares the 23 canonical Tier A competency questions (Stage 3) against the 25
CQs already implemented in ../cq_sparql_benchmark.py, and answers three
questions: which benchmark CQs are corroborated by the independently elicited
set, which benchmark CQs no model proposed, and which elicited CQs the
benchmark does not reach.

WHAT THE COMPARISON REVEALED. The two sets are not competing formulations of
the same thing; they are different instruments over largely the same relations.
A benchmark CQ such as "Which rice diseases have an identified causal
pathogen?" is a COVERAGE PROBE: it asks how completely `causedBy` is populated.
The elicited CQ-A01, "Which pathogen causes a given rice disease?", is a
RETRIEVAL QUESTION: it asks what the graph answers for one disease. Both are
legitimate and they are complementary, so a benchmark CQ without an elicited
counterpart is not automatically a defect -- ten of them are graph-hygiene or
entailment checks that no domain expert would ever pose.

The mapping below was made by reading both sets, not by string similarity;
Stage 2 established that lexical methods conflate neighbouring requirements
here. As in Stage 3 it is an LLM-assisted first pass for human adjudication,
and the adjudication columns are emitted blank.

Outputs:
  ../data/cq_stage4_reconciliation.csv   one row per benchmark CQ
  ../data/cq_stage4_gaps.csv             elicited CQs the benchmark misses
  ../reports/cq_stage4_reconciliation.md the readable finding
"""

import csv
import re
import datetime
import collections
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
BENCHMARK = ROOT.parent / "cq_sparql_benchmark.py"

# benchmark id -> (canonical CQ ids it probes, relationship, note)
#
#   coverage-form  the benchmark asks how completely the relation behind the
#                  elicited CQ is populated
#   chain          the benchmark traverses several relations at once, spanning
#                  more than one elicited CQ
#   integrity      a graph-hygiene check with no domain-level counterpart, and
#                  none is expected
#   entailment     a description-logic check, likewise with no counterpart
#   out-of-scope   concerns a modality held back as Tier B
MAPPING = {
    "CQ-01": (["CQ-A01"], "coverage-form", "how completely causedBy is populated"),
    "CQ-02": (["CQ-A03"], "coverage-form", "how completely indicatedBy is populated"),
    "CQ-03": (["CQ-A07"], "coverage-form", "how completely controlledBy is populated"),
    "CQ-04": (["CQ-A03"], "coverage-form", "same relation, read from the symptom side"),
    "CQ-05": (["CQ-A05", "CQ-A06"], "chain", "occursIn joined with increaseRiskOf"),
    "CQ-06": (["CQ-A06"], "coverage-form", "growth-stage vulnerability profile"),
    "CQ-07": ([], "integrity", "cross-checks vulnerableTo against occursIn"),
    "CQ-08": (["CQ-A07"], "coverage-form",
              "narrows to preventive treatments with a stage prerequisite"),
    "CQ-09": (["CQ-A02"], "chain", "vector -> pathogen -> disease traversal"),
    "CQ-10": (["CQ-A02", "CQ-A07"], "integrity",
              "finds vectors with no recorded treatment"),
    "CQ-11": (["CQ-A03", "CQ-A05", "CQ-A07"], "chain",
              "environmental factor -> disease -> symptom -> treatment"),
    "CQ-12": (["CQ-A07"], "coverage-form", "reach of the management layer"),
    "CQ-13": ([], "integrity", "every severity level maps to a management action"),
    "CQ-14": (["CQ-A15"], "entailment",
              "membership of the defined class SymptomaticObservation"),
    "CQ-15": ([], "entailment", "inverse-direction traversal works"),
    "CQ-16": (["CQ-A22", "CQ-A23"], "chain",
              "image -> annotated class -> symptom and treatment"),
    "CQ-17": ([], "integrity", "annotated classes are typed as domain entities"),
    "CQ-18": (["CQ-A21"], "coverage-form",
              "which symptoms have image support - the closest direct match "
              "between the two sets"),
    "CQ-19": (["CQ-A11"], "integrity",
              "images missing a content URL or provenance link"),
    "CQ-20": ([], "out-of-scope", "counts sensor observations; Tier B under the "
                                  "text+image scope decision"),
    "CQ-21": ([], "integrity", "reified assertions carrying source and citation"),
    "CQ-22": ([], "integrity", "reified axioms with incomplete provenance"),
    "CQ-23": ([], "integrity", "alignment to external vocabularies"),
    "CQ-24": ([], "integrity", "evidenceType literals uniformly language-tagged"),
    "CQ-25": ([], "entailment", "no individual typed both Symptom and Disease"),
}

ENTRY_RE = re.compile(
    r'\{\s*"id": "(CQ-\d+)", "level": "(L\d)", "dim": "(D\d)", "mode": "(\w+)",\s*'
    r'"question": (.*?),\s*"rationale"', re.S)


def read_benchmark():
    text = BENCHMARK.read_text(encoding="utf-8")
    out = []
    for cid, level, dim, mode, raw in ENTRY_RE.findall(text):
        question = " ".join(re.findall(r'"([^"]*)"', raw))
        question = re.sub(r"\s+", " ", question).strip()
        out.append({"benchmark_id": cid, "level": level, "dim": dim,
                    "mode": mode, "question": question})
    return out


def main():
    bench = read_benchmark()
    assert len(bench) == 25, f"expected 25 benchmark CQs, parsed {len(bench)}"
    assert set(MAPPING) == {b["benchmark_id"] for b in bench}, \
        "MAPPING out of sync with the benchmark"

    canonical = list(csv.DictReader(
        (DATA / "cq_stage3_final_tierA.csv").open(encoding="utf-8-sig")))
    canon_by_id = {c["cq_id"]: c for c in canonical}
    for ids, _, _ in MAPPING.values():
        for i in ids:
            assert i in canon_by_id, f"MAPPING references unknown CQ {i}"

    rows = []
    for b in bench:
        ids, rel, note = MAPPING[b["benchmark_id"]]
        rows.append({**b,
                     "maps_to": " ".join(ids),
                     "relationship": rel,
                     "note": note,
                     "corroborated": "yes" if ids else "no",
                     "you_agree": "",
                     "your_correction": ""})
    with (DATA / "cq_stage4_reconciliation.csv").open(
            "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    reached = {i for ids, _, _ in MAPPING.values() for i in ids}
    gaps = [c for c in canonical if c["cq_id"] not in reached]
    gfields = ["cq_id", "category", "n_models", "v06_status",
               "canonical_question", "short_label", "you_agree",
               "your_correction"]
    with (DATA / "cq_stage4_gaps.csv").open("w", encoding="utf-8-sig",
                                            newline="") as f:
        w = csv.DictWriter(f, fieldnames=gfields)
        w.writeheader()
        for c in gaps:
            w.writerow({**{k: c.get(k, "") for k in gfields},
                        "you_agree": "", "your_correction": ""})

    write_report(bench, rows, canonical, gaps, reached)
    by_rel = collections.Counter(r["relationship"] for r in rows)
    print(f"benchmark CQs: {len(bench)}  corroborated: "
          f"{sum(1 for r in rows if r['corroborated'] == 'yes')}")
    for k, v in by_rel.most_common():
        print(f"  {k:14s} {v}")
    print(f"elicited CQs not reached by the benchmark: {len(gaps)}/{len(canonical)}")


def write_report(bench, rows, canonical, gaps, reached):
    by_rel = collections.Counter(r["relationship"] for r in rows)
    corrob = [r for r in rows if r["corroborated"] == "yes"]
    img_gaps = [g for g in gaps if g["category"] in ("image", "crossmodal")]

    L = ["# Stage 4 - Reconciliation with the existing benchmark", "",
         f"Generated {datetime.datetime.now():%Y-%m-%d %H:%M} by "
         "`scripts/stage4_reconcile.py`.", "",
         "**23 elicited competency questions** (Stage 3) against **25 benchmark "
         "CQs** already implemented in `../cq_sparql_benchmark.py`.", "",
         "> LLM-assisted first pass for human adjudication. `you_agree` and "
         "`your_correction` in the two CSVs are blank. Mapping was done by "
         "reading both sets; Stage 2 showed that string similarity conflates "
         "neighbouring requirements in this material.", "",
         "## The headline: these are two different instruments", "",
         "The sets do not compete. A benchmark CQ asks how completely a "
         "relation is populated; an elicited CQ asks what the graph answers for "
         "a concrete case. Compare:", "",
         "| | Benchmark `CQ-01` | Elicited `CQ-A01` |", "|---|---|---|",
         "| Question | Which rice diseases have an identified causal pathogen? | "
         "Which pathogen causes a given rice disease? |",
         "| Asks about | the graph | the domain |",
         "| Answer | a completeness ratio | a pathogen |", "",
         "Both probe `causedBy`. Neither substitutes for the other, and a "
         "benchmark CQ with no elicited counterpart is not automatically a "
         "defect.", "",
         "## How the 25 benchmark CQs relate to the elicited set", "",
         "| Relationship | Count | Meaning |", "|---|---|---|",
         f"| `coverage-form` | {by_rel['coverage-form']} | measures how "
         "completely the relation behind an elicited CQ is populated |",
         f"| `chain` | {by_rel['chain']} | traverses several relations, "
         "spanning more than one elicited CQ |",
         f"| `integrity` | {by_rel['integrity']} | graph hygiene; no "
         "domain-level counterpart is expected |",
         f"| `entailment` | {by_rel['entailment']} | description-logic check; "
         "likewise no counterpart |",
         f"| `out-of-scope` | {by_rel['out-of-scope']} | concerns a modality "
         "held back as Tier B |", "",
         f"**{len(corrob)} of 25** benchmark CQs are corroborated by at least "
         "one independently elicited CQ. The remainder are, with one exception, "
         "checks no domain expert would pose - which is the correct division of "
         "labour, not a shortfall.", "",
         "### The one exception", "",
         "`CQ-20` (*How many sensor observations does the KG contain?*) counts "
         "a modality the resource does not populate. Under the text+image scope "
         "decision it belongs to Tier B and should be reframed or retired "
         "rather than reported as a passing benchmark item.", "",
         "## Detail", "",
         "| Benchmark | Mode | Maps to | Relationship | Note |",
         "|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| `{r['benchmark_id']}` | {r['mode']} | "
                 f"{r['maps_to'] or '-'} | `{r['relationship']}` | "
                 f"{r['note']} |")

    L += ["", "---", "",
          f"## What the benchmark does not reach: {len(gaps)} of "
          f"{len(canonical)} elicited CQs", "",
          "This is the actionable finding. The benchmark reaches the symbolic "
          "layer thoroughly and the image layer barely: "
          f"**{len(img_gaps)} of the {len(gaps)} unreached CQs are image or "
          "cross-modal**. Users ask about images; the current benchmark mostly "
          "asks whether images are linked at all.", "",
          "| ID | Category | n_models | Status vs v0.6 | Question |",
          "|---|---|---|---|---|"]
    for g in gaps:
        L.append(f"| `{g['cq_id']}` | {g['category']} | {g['n_models']} | "
                 f"{g['v06_status']} | {g['canonical_question']} |")

    strong = [g for g in gaps if int(g["n_models"]) >= 3
              and g["v06_status"] == "answerable"]
    L += ["", "### Priority additions", "",
          "Elicited by three or more models independently, and answerable by "
          "v0.6 as it stands - so they can be implemented as SPARQL now, "
          "without waiting for schema work:", ""]
    for g in strong:
        L.append(f"- **`{g['cq_id']}`** ({g['n_models']} models) - "
                 f"{g['canonical_question']}")
    L += ["",
          "`CQ-A04` deserves particular attention: differential diagnosis - "
          "which diseases share symptoms and what discriminates them - was "
          "proposed by four of five models and is the question a field "
          "diagnostician actually asks, yet the benchmark has no equivalent.",
          "", "## Consequences for Stage 5", "",
          "- The questionnaire should carry the **elicited** phrasing, not the "
          "coverage phrasing. An agronomist can judge whether *which pathogen "
          "causes blast* is a sensible question; they cannot judge whether "
          "*72% of diseases have a causal pathogen* is a sensible threshold.",
          "- Corroboration by the benchmark is a second convergence signal, "
          "independent of the five models. Record it alongside `n_models`, and "
          "keep it out of the questionnaire itself for the same reason - it "
          "would contaminate what the ratings are meant to test.", ""]

    (REPORTS / "cq_stage4_reconciliation.md").write_text("\n".join(L),
                                                         encoding="utf-8")


if __name__ == "__main__":
    main()
