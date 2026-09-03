"""
Stage 1 of the CQ screening funnel: structural validity triage.

Reads cq_pool_stage0.csv and flags CQs that may not be admissible as
competency questions on structural grounds -- independently of whether the
current ontology happens to answer them (that is Stage 3's job).

IMPORTANT: this script does not reject anything. It proposes flags with the
exact matched evidence so a human can adjudicate. The adjudication columns are
emitted blank, one per screener, so inter-screener agreement can be computed
from the same file.

Reason codes
  R1-NONQUERY    asks for a judgement, not a result set
  R2-PREDICTIVE  requires a predictive model rather than retrieval
  R3-NOSOURCE    presupposes an attribute no declared source supplies
  R4-UNBOUNDED   scope so open that no query could be complete

Outputs (in this directory):
  cq_stage1_adjudication.csv  173 rows, with blank decision columns
  cq_stage1_proposal.md       counts, rules, and every flagged CQ in full
"""

import csv
import re
import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
POOL = SCRIPT_DIR / "cq_pool_stage0.csv"

# Each rule is (code, compiled pattern, why it matters). Patterns are
# deliberately narrow: over-flagging wastes the adjudicator's attention, and
# recall is recoverable because the adjudicator reads every row anyway.
RULES = [
    ("R1-NONQUERY", re.compile(
        r"how (?:important|effective|useful|beneficial|well)\b"
        r"|is it worth\b|how reliable\b|how accurate\b",
        re.I),
     "asks for an evaluative judgement rather than a retrievable result set"),

    ("R2-PREDICTIVE", re.compile(
        r"\bpredict(?:s|ed|ing|ion|ive)?\b|\bforecast\w*\b|most likely\b"
        r"|\blikelihood\b|\bprobabilit\w+\b|early warning\b|\banticipat\w+\b"
        r"|will (?:occur|develop|emerge)\b",
        re.I),
     "answer requires inference by a model, not retrieval from the graph"),

    ("R3-NOSOURCE", re.compile(
        r"\blatency period\b|\bincubation period\b|degree.?days?\b"
        r"|economic threshold\b|action threshold\b|\byield loss\b"
        r"|\bmarket price\b|\badoption rate\b|releasing institution\b",
        re.I),
     "presupposes a quantity none of the declared sources records"),

    ("R4-UNBOUNDED", re.compile(
        r"\ball (?:available )?(?:information|knowledge|data)\b"
        r"|\beverything (?:known|recorded)\b|\bany information\b",
        re.I),
     "no bounding entity, so no query result could ever be complete"),
]

# Not a reason to reject -- recorded because Stage 5 needs to know which CQs
# are parameterised templates (N days, X%, a given plot) rather than concrete.
PARAM_RE = re.compile(
    r"\bgiven (?:a|an|the) \w+|\bN days?\b|\bK days?\b|\babove [XY]\b"
    r"|\b[XY]%|\[T\w+, ?T\w+\]|\bspecified \w+|\ba given\b", re.I)


def screen(row):
    text = row["question"]
    hits = []
    for code, pat, _ in RULES:
        m = pat.search(text)
        if m:
            hits.append((code, m.group(0)))
    return hits


def main():
    assert POOL.exists(), f"run stage0 first: {POOL} missing"
    rows = list(csv.DictReader(POOL.open(encoding="utf-8-sig")))

    flagged, counts = [], {}
    for r in rows:
        hits = screen(r)
        r["auto_flag"] = "FLAG" if hits else ""
        r["auto_codes"] = "; ".join(c for c, _ in hits)
        r["auto_evidence"] = "; ".join(f'"{e}"' for _, e in hits)
        r["parameterised"] = "yes" if PARAM_RE.search(r["question"]) else ""
        # Adjudication columns, deliberately blank.
        r["screener1_keep"] = ""
        r["screener1_code"] = ""
        r["screener2_keep"] = ""
        r["screener2_code"] = ""
        r["notes"] = ""
        if hits:
            flagged.append(r)
            for c, _ in hits:
                counts[c] = counts.get(c, 0) + 1

    fields = ["pool_id", "source_model", "original_id", "category", "complexity",
              "question", "auto_flag", "auto_codes", "auto_evidence",
              "parameterised", "screener1_keep", "screener1_code",
              "screener2_keep", "screener2_code", "notes"]
    out = SCRIPT_DIR / "cq_stage1_adjudication.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows({k: r[k] for k in fields} for r in rows)

    n_param = sum(1 for r in rows if r["parameterised"])
    L = ["# Stage 1 - Structural Validity Triage (proposal)", "",
         f"Generated {datetime.datetime.now():%Y-%m-%d %H:%M} by "
         "`stage1_screen.py` from `cq_pool_stage0.csv`.", "",
         "**Nothing has been rejected.** The rules below propose flags; the "
         "decision columns in `cq_stage1_adjudication.csv` are blank and are "
         "the actual filter. Two screener columns are provided so "
         "inter-screener agreement can be computed from the same file.", "",
         f"**Pool in:** {len(rows)} &nbsp;&nbsp; **Auto-flagged:** "
         f"{len(flagged)} &nbsp;&nbsp; **Unflagged:** {len(rows) - len(flagged)}",
         "", "## Rules applied", "",
         "| Code | Flags a CQ whose answer... | Hits |", "|---|---|---|"]
    for code, _, why in RULES:
        L.append(f"| `{code}` | {why} | {counts.get(code, 0)} |")

    L += ["", "## Flagged CQs, in full", "",
          "Each row shows the phrase that triggered the flag. A flag is a "
          "prompt to look, not a verdict.", ""]
    if flagged:
        for r in flagged:
            L += [f"**{r['pool_id']}** &middot; {r['source_model']} "
                  f"&middot; `{r['original_id']}` &middot; {r['category']} "
                  f"&middot; **{r['auto_codes']}** (evidence: "
                  f"{r['auto_evidence']})", "",
                  f"> {r['question']}", ""]
    else:
        L.append("_No CQ triggered any rule._")

    L += ["## Parameterised CQs", "",
          f"{n_param} of {len(rows)} CQs are templates containing an "
          "unbound parameter (a given plot, N days, above X%). This is **not** "
          "a defect -- a parameterised CQ maps to a parameterised SPARQL query "
          "-- but Stage 5 needs to know which ones they are, because an expert "
          "cannot judge agronomic correctness without seeing a concrete "
          "instantiation.", ""]

    (SCRIPT_DIR / "cq_stage1_proposal.md").write_text("\n".join(L),
                                                      encoding="utf-8")
    print(f"in: {len(rows)}  auto-flagged: {len(flagged)}  "
          f"parameterised: {n_param}")
    for code, _, _ in RULES:
        print(f"  {code:16s} {counts.get(code, 0)}")


if __name__ == "__main__":
    main()
