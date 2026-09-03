# Stage 1 - Structural Validity Triage (proposal)

Generated 2026-09-03 20:16 by `stage1_screen.py` from `cq_pool_stage0.csv`.

**Nothing has been rejected.** The rules below propose flags; the decision columns in `cq_stage1_adjudication.csv` are blank and are the actual filter. Two screener columns are provided so inter-screener agreement can be computed from the same file.

**Pool in:** 173 &nbsp;&nbsp; **Auto-flagged:** 8 &nbsp;&nbsp; **Unflagged:** 165

## Rules applied

| Code | Flags a CQ whose answer... | Hits |
|---|---|---|
| `R1-NONQUERY` | asks for an evaluative judgement rather than a retrievable result set | 0 |
| `R2-PREDICTIVE` | answer requires inference by a model, not retrieval from the graph | 2 |
| `R3-NOSOURCE` | presupposes a quantity none of the declared sources records | 7 |
| `R4-UNBOUNDED` | no bounding entity, so no query result could ever be complete | 0 |

## Flagged CQs, in full

Each row shows the phrase that triggered the flag. A flag is a prompt to look, not a verdict.

**P040** &middot; Claude Opus 5 &middot; `CQ-ENV-04` &middot; sensor &middot; **R3-NOSOURCE** (evidence: "degree-days")

> For each plot, what were the cumulative growing-degree-days, total rainfall, and total leaf-wetness hours in the 30 days preceding a specified date, and how do plots rank on each aggregate?

**P044** &middot; Claude Opus 5 &middot; `CQ-GEN-03` &middot; genomic &middot; **R3-NOSOURCE** (evidence: "releasing institution")

> Which released varieties pyramid two or more bacterial-leaf-blight resistance genes, and what are their release year, releasing institution, and recommended agroecology?

**P125** &middot; Gemini Flash 3.8 &middot; `CQ-MM-010` &middot; crossmodal &middot; **R3-NOSOURCE** (evidence: "degree-day")

> For a specific rice plot, integrate: (1) leaf lesion boundary segmentation (Image), (2) past 14-day degree-day and humidity accumulations (Sensor), (3) the planted cultivar's *Pi* gene stack (Genomic), and (4) extension fungicide timing tables (Text) to determine whether emergency systemic fungicide application is economically justified.

**P129** &middot; Gemini Flash 3.8 &middot; `CQ-MM-014` &middot; crossmodal &middot; **R2-PREDICTIVE; R3-NOSOURCE** (evidence: "predict"; "degree-day")

> When field photos indicate yellow stem borer "deadheart" symptoms during tillering (Image) and sensor degree-day models predict peak egg hatch within 48 hours (Sensor), what pheromone lure and chemical threshold recommendations are mandated by national integrated pest management manuals (Text)?

**P136** &middot; Gemini Flash 3.8 &middot; `CQ-MM-08` &middot; crossmodal &middot; **R3-NOSOURCE** (evidence: "yield loss")

> Given high-throughput UAV multispectral imagery showing depressed NDVI patches (Image) and soil moisture telemetry below wilting point (Sensor), what yield loss projections are calculated from tabular agronomic crop-loss models (Tabular)?

**P140** &middot; Gemini Flash 3.8 &middot; `CQ-TXT-03` &middot; text &middot; **R3-NOSOURCE** (evidence: "incubation period")

> How do excessive nitrogen fertilizer application rates influence the incubation period and lesion expansion rate of Bacterial Leaf Blight (*Xanthomonas oryzae* pv. *oryzae*) according to extension publications?

**P157** &middot; Gemini Pro 3.1 &middot; `CQ-MM-05` &middot; crossmodal &middot; **R2-PREDICTIVE** (evidence: "most likely")

> [Img × Txt × Sen] If IoT sensors indicate 3 days of heavy rain and user-uploaded leaf images show water-soaked stripes, what causal pathogen is most likely according to agronomic bulletins?

**P173** &middot; Gemini Pro 3.1 &middot; `CQ-TXT-05` &middot; text &middot; **R3-NOSOURCE** (evidence: "latency period")

> Based on surveillance bulletins, what is the typical latency period for Bacterial Leaf Blight before symptoms become visible?

## Parameterised CQs

54 of 173 CQs are templates containing an unbound parameter (a given plot, N days, above X%). This is **not** a defect -- a parameterised CQ maps to a parameterised SPARQL query -- but Stage 5 needs to know which ones they are, because an expert cannot judge agronomic correctness without seeing a concrete instantiation.
