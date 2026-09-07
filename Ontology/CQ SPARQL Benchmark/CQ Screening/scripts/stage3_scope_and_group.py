"""
Stage 3 of the CQ screening funnel: scope gate, grouping, and the final CQ set.

Two things happen here.

SCOPE GATE. The ESWC resource claim was narrowed to text + image on 2026-09-03
(RiceMMKG v0.6 has 10,407 ImageObservation individuals, zero SensorObservation
individuals, and no variety/gene/document/region entities at all). A CQ whose
question or entity list needs sensor or genomic data is therefore Tier B --
kept as a requirements-based roadmap justification, but not put to experts as
evidence about the released resource.

GROUPING. The Stage 2 automatic clustering under-merged paraphrases and
over-merged neighbouring requirements, so the grouping below was done by
reading all 64 Tier A CQs. That first pass was produced by Claude Opus 5, which
is ALSO one of the five models that generated the pool -- a model grading its
own output. It was reviewed and approved by the ontology engineer (M. A. Furqon)
on 2026-09-03. The paper must describe it as an LLM-assisted first pass,
human-adjudicated, not as an automatic result.

Outputs:
  ../data/cq_stage3_worksheet.csv     the 64 Tier A CQs, ordered by similarity
  ../data/cq_stage3_decisions.csv     the same, with decisions and groups
  ../data/cq_stage3_final_tierA.csv   the 23 canonical CQs
  ../reports/cq_stage3_worksheet.md   readable worksheet
  ../reports/cq_stage3_decisions.md   per-group breakdown and dropped CQs
  ../reports/cq_stage3_final_tierA.md the deliverable CQ set
"""

import csv
import re
import collections
import datetime
import importlib.util
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

ADJUDICATED_BY = "M. A. Furqon"
ADJUDICATED_ON = "2026-09-03"

# A CQ mentioning any of these needs a modality the released resource does not
# have, and is held back as Tier B.
SENSOR_RE = re.compile(
    r"sensor|temperature|humidit|rainfall|soil|weather|agroclimat|iot|"
    r"leaf wetness|degree.?day|climate|telemetry|ndvi|wind|\bstations?\b", re.I)
GENOMIC_RE = re.compile(
    r"genom|variet|cultivar|\bgene\b|\bgenes\b|genotype|snp|allele|qtl|"
    r"locus|loci|biotype|breeding|yield|pedigree|release year", re.I)

# pool_id -> (decision, group, note). Keyed by pool_id, not worksheet row
# number, so that changing the scope filter cannot silently re-target a label.
# See the module docstring for how these were arrived at and who approved them.
LABELS = {
    "P031": ("keep", "G01", ""),
    "P067": ("keep", "G01", ""),
    "P169": ("keep", "G01", ""),
    "P103": ("keep", "G01", ""),
    "P138": ("keep", "G02", "also covers causation; overlaps G01"),
    "P170": ("keep", "G02", ""),
    "P032": ("keep", "G02", ""),
    "P070": ("keep", "G02", "adds transmission mode - new property"),
    "P104": ("keep", "G03", ""),
    "P068": ("keep", "G03", "adds organ + growth stage"),
    "P106": ("keep", "G03", ""),
    "P108": ("keep", "G04", ""),
    "P172": ("keep", "G04", ""),
    "P105": ("keep", "G04", ""),
    "P071": ("keep", "G04", ""),
    "P035": ("keep", "G04", ""),
    "P107": ("keep", "G05", ""),
    "P033": ("keep", "G06", ""),
    "P139": ("keep", "G07", "adds growth stage"),
    "P034": ("keep", "G07", ""),
    "P171": ("keep", "G07", ""),
    "P069": ("keep", "G07", "adds source document"),
    "P141": ("keep", "G08", "needs NaturalEnemy class - not in v0.6"),
    "P142": ("keep", "G09", "needs nutritional disorder (zinc deficiency) - not in v0.6"),
    "P011": ("keep", "G10", "also asks annotation source, see G11"),
    "P083": ("keep", "G10", ""),
    "P047": ("keep", "G10", ""),
    "P150": ("keep", "G10", ""),
    "P050": ("keep", "G11",
             "needs annotator + confidence - confidenceScore unused in v0.6"),
    "P015": ("keep", "G12",
             "needs both model and expert annotations - only dataset labels in v0.6"),
    "P013": ("keep", "G13", ""),
    "P048": ("keep", "G13", "needs capture device + distance metadata"),
    "P120": ("keep", "G14", "needs PlantPart class - not in v0.6"),
    "P082": ("keep", "G14", "needs PlantPart class - not in v0.6"),
    "P012": ("keep", "G14", "needs PlantPart + visual symptom class"),
    "P081": ("keep", "G15",
             "partial: 1,442 of 10,407 images carry a captures link (14%)"),
    "P118": ("keep", "G15", ""),
    "P085": ("keep", "G16", "needs lesion shape/colour/distribution descriptors"),
    "P148": ("keep", "G16", ""),
    "P121": ("keep", "G16", ""),
    "P151": ("keep", "G16", ""),
    "P084": ("keep", "G17", ""),
    "P051": ("keep", "G17", ""),
    "P149": ("keep", "G17", ""),
    "P122": ("keep", "G17", ""),
    "P014": ("keep", "G18",
             "needs severity grade per image - SeverityLevel unlinked in v0.6"),
    "P119": ("keep", "G18", "needs region-level lesion annotation - roadmap Phase 2"),
    "P049": ("keep", "G19",
             "needs multi-symptom annotation: every annotated image currently "
             "carries exactly one captures link"),
    "P123": ("keep", "G20", "needs growth stage annotation on images"),
    "P020": ("keep", "G21", ""),
    "P061": ("keep", "G21", ""),
    "P087": ("keep", "G22", ""),
    "P088": ("keep", "G22", ""),
    "P086": ("keep", "G22", ""),
    "P053": ("keep", "G22", ""),
    "P153": ("keep", "G23", ""),
    "P140": ("drop", "", "R3: incubation period not recorded in any source"),
    "P173": ("drop", "", "R3: latency period not recorded in any source"),
    "P072": ("drop", "", "needs province-level surveillance statistics - no such data"),
    "P036": ("drop", "", "needs province-level surveillance statistics - no such data"),
    "P143": ("drop", "", "needs quarantine policy corpus - no such data"),
    "P052": ("drop", "",
             "needs repeated photography of one plot over a season - no such data"),
    "P152": ("drop", "", "needs plot-linked image time series - no such data"),
    "P029": ("drop", "", "needs district surveillance records - no such data"),
}
# Canonical question per group, plus the short label used in tables.
GROUPS = {
    "G01": ("Which pathogen causes a given rice disease, and to which taxonomic "
            "group does it belong?",
            "Pathogen causing a disease, and its taxonomy"),
    "G02": ("Which vector species transmits which pathogen or viral disease, and "
            "by which transmission mode?",
            "Vector transmitting a pathogen or viral disease"),
    "G03": ("Which symptoms does a given disease produce, on which plant organ, "
            "and at which growth stage?",
            "Symptoms of a disease, by organ and growth stage"),
    "G04": ("Which diseases or pests share overlapping symptoms, and which "
            "symptoms discriminate between them?",
            "Diseases sharing symptoms, and what discriminates them"),
    "G05": ("Which environmental conditions are reported to favour a given "
            "disease or pest?",
            "Environmental conditions favouring a disease or pest"),
    "G06": ("At which growth stages is a given disease or pest reported as most "
            "damaging?",
            "Growth stage at which a pest or disease is most damaging"),
    "G07": ("Which control measures are recommended for a given disease or pest, "
            "of which management category, and on which source authority?",
            "Recommended control measures, by category and source"),
    "G08": ("Which natural enemies are documented as predators or parasitoids of "
            "a given pest?",
            "Natural enemies of a pest"),
    "G09": ("Which features distinguish a nutritional disorder from a disease "
            "with similar visible symptoms?",
            "Distinguishing a nutritional disorder from a disease"),
    "G10": ("Which images are annotated as showing a given condition or visual "
            "symptom?",
            "Images showing a given condition or symptom"),
    "G11": ("Who or what produced a given image annotation, and with what "
            "confidence?",
            "Provenance and confidence of an image annotation"),
    "G12": ("Where do model-generated and expert image annotations disagree, and "
            "on which conditions and plant parts?",
            "Disagreement between model and expert annotations"),
    "G13": ("How is the image corpus distributed across conditions, plant parts, "
            "and capture types?",
            "Distribution of the image corpus"),
    "G14": ("Which plant organ is depicted in a given image?",
            "Plant organ depicted in an image"),
    "G15": ("Which visible symptoms are annotated in a given image?",
            "Symptoms annotated in a given image"),
    "G16": ("Which disease or pest is best supported by the visual evidence in a "
            "given image?",
            "Disease or pest supported by visual evidence"),
    "G17": ("Which visual features separate two visually confusable conditions?",
            "Visual features separating confusable conditions"),
    "G18": ("How severe is the damage recorded in a given image?",
            "Severity of the damage in an image"),
    "G19": ("Which symptoms co-occur on the same plant within a single image?",
            "Symptoms co-occurring in one image"),
    "G20": ("Which growth stage is visually manifest in a whole-canopy image?",
            "Growth stage visible in a canopy image"),
    "G21": ("Which literature-described symptoms have supporting image evidence, "
            "and which do not?",
            "Literature symptoms with and without image support"),
    "G22": ("Which literature-described disease matches the symptoms annotated in "
            "a given image?",
            "Literature disease matching an image"),
    "G23": ("Which treatment does the literature prescribe for a condition "
            "identified from an image?",
            "Treatment prescribed for an imaged condition"),
}


def load_stage2_module():
    spec = importlib.util.spec_from_file_location(
        "s2", SCRIPT_DIR / "stage2_cluster.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tier_a(rows):
    out = []
    for r in rows:
        blob = r["question"] + " " + r["entities"]
        if SENSOR_RE.search(blob) or GENOMIC_RE.search(blob):
            continue
        out.append(r)
    return out


def similarity_order(s2, rows):
    """Order CQs so that similar ones sit next to each other, within category."""
    M = s2.vectorise(rows)
    C = M @ M.T
    np.fill_diagonal(C, 0.0)
    S = (C + s2.jaccard_matrix(rows)) / 2
    by_cat = collections.defaultdict(list)
    for i, r in enumerate(rows):
        by_cat[r["category"]].append(i)
    order = []
    for cat in ["text", "image", "crossmodal"]:
        idx = list(by_cat.get(cat, []))
        if not idx:
            continue
        remaining = set(idx)
        cur = idx[0]
        remaining.discard(cur)
        order.append(cur)
        while remaining:
            nxt = max(remaining, key=lambda j: S[cur, j])
            order.append(nxt)
            remaining.discard(nxt)
            cur = nxt
    assert len(order) == len(rows)
    return order


def main():
    pool = list(csv.DictReader((DATA / "cq_stage0_pool.csv").open(
        encoding="utf-8-sig")))
    flags = {r["pool_id"]: (r["auto_codes"], r["parameterised"])
             for r in csv.DictReader((DATA / "cq_stage1_adjudication.csv").open(
                 encoding="utf-8-sig"))}
    s2 = load_stage2_module()

    rows = tier_a(pool)
    order = similarity_order(s2, rows)
    sheet = []
    for n, i in enumerate(order, start=1):
        r = dict(rows[i])
        r["no"] = n
        r["stage1_flag"], r["parameterised"] = flags.get(r["pool_id"], ("", ""))
        sheet.append(r)

    with (DATA / "cq_stage3_worksheet.csv").open("w", encoding="utf-8-sig",
                                             newline="") as f:
        cols = ["no", "pool_id", "category", "question", "source_model",
                "stage1_flag", "parameterised", "KEEP_or_DROP", "GROUP_ID",
                "notes"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sheet:
            w.writerow({**{c: "" for c in cols},
                        **{c: r[c] for c in cols if c in r}})

    missing = {r["pool_id"] for r in sheet} - set(LABELS)
    extra = set(LABELS) - {r["pool_id"] for r in sheet}
    assert not missing and not extra, f"LABELS out of sync: {missing=} {extra=}"
    for r in sheet:
        d, g, note = LABELS[r["pool_id"]]
        r["KEEP_or_DROP"] = d
        r["GROUP_ID"] = g
        r["group_label"] = GROUPS[g][1] if g else ""
        r["reason_or_gap"] = note

    with (DATA / "cq_stage3_decisions.csv").open(
            "w", encoding="utf-8-sig", newline="") as f:
        cols = ["no", "pool_id", "category", "source_model", "KEEP_or_DROP",
                "GROUP_ID", "group_label", "reason_or_gap", "question",
                "stage1_flag", "parameterised"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows({c: r.get(c, "") for c in cols} for r in sheet)

    keep = [r for r in sheet if r["KEEP_or_DROP"] == "keep"]
    dropped = [r for r in sheet if r["KEEP_or_DROP"] == "drop"]
    grouped = collections.defaultdict(list)
    for r in keep:
        grouped[r["GROUP_ID"]].append(r)

    # ---- final CQ set -------------------------------------------------------
    final = []
    for n, g in enumerate(sorted(grouped), start=1):
        members = grouped[g]
        models = sorted({m["source_model"] for m in members})
        gaps = [m["reason_or_gap"] for m in members if m["reason_or_gap"]]
        answerable = any(not m["reason_or_gap"] for m in members)
        final.append({
            "cq_id": f"CQ-A{n:02d}",
            "group_id": g,
            "category": members[0]["category"],
            "canonical_question": GROUPS[g][0],
            "short_label": GROUPS[g][1],
            "n_models": len(models),
            "n_source_cqs": len(members),
            "models": "; ".join(models),
            "source_pool_ids": " ".join(m["pool_id"] for m in members),
            "v06_status": "answerable" if answerable else "needs new schema/data",
            "extensions_required": " | ".join(sorted(set(gaps))),
        })

    ffields = list(final[0])
    with (DATA / "cq_stage3_final_tierA.csv").open("w", encoding="utf-8-sig",
                                            newline="") as f:
        w = csv.DictWriter(f, fieldnames=ffields)
        w.writeheader()
        w.writerows(final)

    write_worksheet_md(sheet)
    write_proposal_md(grouped, dropped, keep)
    write_final_md(final, len(pool), len(rows), len(keep), len(dropped))

    print(f"pool {len(pool)} -> tier A {len(rows)} -> keep {len(keep)} "
          f"(drop {len(dropped)}) -> {len(final)} canonical CQs")


def write_worksheet_md(sheet):
    L = ["# Worksheet: Tier A competency questions (text + image)", "",
         "Every CQ here needs neither sensor nor genomic data, so all of them "
         "bear on the resource actually being released. Ordering places similar "
         "CQs next to each other.", "",
         "Fill two columns in `data/cq_stage3_worksheet.csv`:", "",
         "- **KEEP_or_DROP** - `keep` or `drop`",
         "- **GROUP_ID** - any number; CQs asking the same thing share a number",
         "", "---", ""]
    last = None
    for r in sheet:
        if r["category"] != last:
            n = sum(1 for x in sheet if x["category"] == r["category"])
            L += ["", f"## {r['category'].upper()} ({n} CQs)", ""]
            last = r["category"]
        tag = []
        if r["stage1_flag"]:
            tag.append(r["stage1_flag"])
        if r["parameterised"]:
            tag.append("parameterised")
        suffix = f" - {', '.join(tag)}" if tag else ""
        L += [f"**{r['no']}.** `{r['pool_id']}` - {r['source_model']}{suffix}",
              f"> {r['question']}", ""]
    (REPORTS / "cq_stage3_worksheet.md").write_text("\n".join(L), encoding="utf-8")


def write_proposal_md(grouped, dropped, keep):
    L = ["# Stage 3 - Scope gate and grouping", "",
         f"Generated {datetime.datetime.now():%Y-%m-%d %H:%M}. "
         f"**65 Tier A CQs in -> {len(keep)} keep, {len(dropped)} drop, "
         f"{len(grouped)} groups.**", "",
         "> **Declared conflict of interest.** This grouping was drafted by "
         "Claude Opus 5, one of the five models whose output forms the pool, so "
         "a model graded its own work. It was reviewed and approved by "
         f"{ADJUDICATED_BY} on {ADJUDICATED_ON}. Describe it in writing as an "
         "LLM-assisted first pass, human-adjudicated.", "",
         "## Groups", "",
         "`n_models` = how many of the five models proposed this group "
         "independently.", "",
         "| Group | n_models | CQs | Question |", "|---|---|---|---|"]
    for g in sorted(grouped):
        models = {r["source_model"] for r in grouped[g]}
        L.append(f"| `{g}` | {len(models)} | {len(grouped[g])} | "
                 f"{GROUPS[g][1]} |")
    L += ["", "---", "", "## Group contents", ""]
    for g in sorted(grouped):
        models = sorted({r["source_model"] for r in grouped[g]})
        L += [f"### {g} - {GROUPS[g][1]}", "",
              f"> {GROUPS[g][0]}", "",
              f"*{len(models)} models: {', '.join(models)}*", ""]
        for r in grouped[g]:
            gap = f" - **{r['reason_or_gap']}**" if r["reason_or_gap"] else ""
            L += [f"- **{r['no']}.** `{r['pool_id']}` ({r['source_model']}){gap}",
                  f"  > {r['question']}"]
        L.append("")
    L += ["---", "", f"## {len(dropped)} CQs dropped", "",
          "| # | pool_id | Reason | Question |", "|---|---|---|---|"]
    for r in dropped:
        L.append(f"| {r['no']} | `{r['pool_id']}` | {r['reason_or_gap']} | "
                 f"{r['question'][:110].replace('|', '/')} |")
    (REPORTS / "cq_stage3_decisions.md").write_text("\n".join(L),
                                                         encoding="utf-8")


def write_final_md(final, n_pool, n_tier_a, n_keep, n_drop):
    ext = [f for f in final if f["v06_status"] != "answerable"]
    L = ["# Rice MMKG - Final Competency Question Set (Tier A)", "",
         f"Generated {datetime.datetime.now():%Y-%m-%d %H:%M} by "
         "`scripts/stage3_scope_and_group.py`.", "",
         f"**{len(final)} canonical competency questions**, distilled from "
         f"{n_pool} candidates elicited independently from five large language "
         "models against one shared prompt.", "",
         "Scope is text + image: the modalities the released resource actually "
         "carries. CQs requiring sensor or genomic data are held as Tier B, a "
         "requirements-based roadmap rather than a claim about this release.",
         "", "## Provenance", "",
         "| Step | In | Out |", "|---|---|---|",
         f"| Stage 0 - pool from 5 models | - | {n_pool} |",
         f"| Stage 1 - structural validity | {n_pool} | {n_pool} (8 flagged) |",
         f"| Stage 3 - scope gate (text + image) | {n_pool} | {n_tier_a} |",
         f"| Stage 3 - adjudication | {n_tier_a} | {n_keep} (dropped {n_drop}) |",
         f"| Stage 3 - grouping | {n_keep} | **{len(final)}** |",
         "",
         "Grouping was an LLM-assisted first pass reviewed and approved by "
         f"{ADJUDICATED_BY} on {ADJUDICATED_ON}. One of the five source models "
         "drafted it, so it is not an independent judgement.", "",
         "## The competency questions", "",
         "`n_models` counts how many of the five models proposed the question "
         "independently. It is a convergence signal, not a quality score; "
         f"Stage 5 deliberately retains low-convergence CQs so that the "
         "hypothesis *convergence predicts expert-rated relevance* remains "
         "testable.", "",
         "| ID | Category | n_models | Status vs v0.6 | Competency question |",
         "|---|---|---|---|---|"]
    for f in final:
        L.append(f"| `{f['cq_id']}` | {f['category']} | {f['n_models']} | "
                 f"{f['v06_status']} | {f['canonical_question']} |")
    L += ["", "## Detail", ""]
    for f in final:
        L += [f"### {f['cq_id']} - {f['short_label']}", "",
              f"> {f['canonical_question']}", "",
              f"- **Category:** {f['category']}",
              f"- **Convergence:** {f['n_models']} of 5 models "
              f"({f['models']})",
              f"- **Source CQs:** {f['n_source_cqs']} - "
              f"`{f['source_pool_ids']}`",
              f"- **Status against v0.6:** {f['v06_status']}"]
        if f["extensions_required"]:
            L.append(f"- **Extensions required:** {f['extensions_required']}")
        L.append("")
    L += ["---", "", f"## {len(ext)} CQs requiring schema or data extensions", "",
          "These are legitimate requirements that v0.6 cannot yet answer. They "
          "constitute the v0.7 work plan.", "",
          "| ID | Question | What is needed |", "|---|---|---|"]
    for f in ext:
        L.append(f"| `{f['cq_id']}` | {f['short_label']} | "
                 f"{f['extensions_required']} |")
    L += ["", "## Still outstanding", "",
          "- **Stage 4** - reconcile against the 25 CQs already in "
          "`CQ_SPARQL_Benchmark_Report.md`: which are corroborated, which are "
          "unique to the benchmark, which are new here.",
          "- **Stage 5** - stratified sampling to questionnaire size, "
          "instantiating parameterised CQs with concrete diseases, and blinding "
          "the questionnaire to source model and convergence count.", ""]
    (REPORTS / "cq_stage3_final_tierA.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
