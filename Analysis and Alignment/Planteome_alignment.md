# Planteome Alignment Register

## Purpose and scope

This register records semantic links between Rice MMKG entities and the
**Planteome** ontology suite (Plant Ontology / PO, Plant Trait Ontology / TO,
Plant Experimental Conditions Ontology / PECO, Plant Stress Ontology / PSO),
kept separate from
[`AGROVOC_alignment.md`](AGROVOC_alignment.md) and
[`NCBI_Taxonomy_alignment.md`](NCBI_Taxonomy_alignment.md) for the same
reason as those two: each source has its own query method and provenance,
and mixing them into one file would blur which source justified which
mapping decision.

Planteome was checked specifically for `EnvironmentalFactor` entities that
AGROVOC could not resolve without a category mismatch (state vs. quantity,
condition vs. response, cause vs. effect — see `AGROVOC_alignment.md` rounds
2–4). PECO in particular models environmental factors as **"exposure"**
concepts (a treatment/condition a plant is exposed to), which is a much
closer semantic fit to this class than AGROVOC's candidates were.

**Source queried:** EBI Ontology Lookup Service (OLS4), `https://www.ebi.ac.uk/ols4/api/`  
**Query method:** free-text search across `peco,eo,po,to,pso`, no registration or API key required  
**Checked:** 2026-08-17, verified 2026-09-03 (Rice MMKG v0.6)

## Query method

**1. Free-text search across the Planteome ontologies:**

```
GET https://www.ebi.ac.uk/ols4/api/search?q=<term>&ontology=peco,eo,po,to,pso&rows=15
```

Read each result's `label`, `obo_id`, `iri`, and `description` (OLS4 returns
the OBO `def` as description). Unlike AGROVOC, most PECO/TO terms carry a
full definition, so the decision is usually made directly from the search
result rather than needing a second detail query.

**2. Check for a narrower/child term** (used to confirm a generic
candidate is the most specific one available, same reasoning as the
AGROVOC register's step 3):

```
GET https://www.ebi.ac.uk/ols4/api/ontologies/peco/terms/<url-encoded-iri>/children
```

**Decision rule** (same as the other two registers): `exactMatch` requires
matching meaning *and* category (state vs. quantity, condition vs.
response, cause vs. effect all count as category mismatches, not just
scope differences); `closeMatch` when the candidate is a leaf term with no
more specific option and the mismatch is scope/severity rather than
category; local-only when no plausible candidate exists at all.

**Identifier used for alignment:** the OBO PURL form
(`http://purl.obolibrary.org/obo/<ONTOLOGY>_<id>`), matching the convention
already used for NCBI Taxonomy in this project.

## EnvironmentalFactor alignment (round 1)

Checked 2026-08-17. All four candidates AGROVOC had flagged as category
mismatches were re-searched here.

| Rice MMKG entity | AGROVOC candidate (rejected/closeMatch) | Planteome candidate | Proposed relation | Status | Decision note |
|---|---|---|---|---|---|
| `High_Humidity` | [`relative humidity`](http://aims.fao.org/aos/agrovoc/c_6496) — state-vs-quantity mismatch | [`humidity exposure`](http://purl.obolibrary.org/obo/PECO_0007197) (PECO:0007197) | `skos:closeMatch` | Implemented | PECO models this as the *treatment/exposure* category, matching `EnvironmentalFactor`'s intent much better than AGROVOC's measured quantity. No narrower "high humidity" term exists under PECO:0007197 (checked — zero children), so generic `closeMatch` is the ceiling, same reasoning as `Downy_Mildew`/`Stem_Borer` in the AGROVOC register. |
| `High_Temperature` | [`heat stress`](http://aims.fao.org/aos/agrovoc/c_11488) — condition-vs-response mismatch | [`high temperature exposure`](http://purl.obolibrary.org/obo/PECO_0007173) (PECO:0007173) | `skos:exactMatch` | Implemented | Definition: "The treatment involving an exposure to above optimal temperature" — near word-for-word match to the local label, and correctly models the *condition* rather than the plant's stress *response* (the category mismatch that blocked the AGROVOC candidate). |
| `Low_Rainfall` | [`drought`](http://aims.fao.org/aos/agrovoc/c_2391) — severity mismatch | [`drought exposure`](http://purl.obolibrary.org/obo/PECO_0007404) (PECO:0007404) | `skos:closeMatch` | Implemented | Definition: "exposure of plants to a prolonged dry period" — same severity/duration nuance as the AGROVOC candidate (drought implies more than just "low"), but the exposure framing is the correct category. Considered the more generic `rainfall exposure` (PECO:0007181, no low/high qualifier) as an alternative; `drought exposure` is the closer match in intent. |
| `Poor_Soil_Drainage` | [`waterlogging`](http://aims.fao.org/aos/agrovoc/c_8333) — cause-vs-effect mismatch | [`flood water exposure`](http://purl.obolibrary.org/obo/PECO_0007172) (PECO:0007172) | `skos:closeMatch` | Implemented | Same cause-vs-effect nuance as the AGROVOC candidate (standing water is the *effect* of poor drainage, not the drainage condition itself); no direct "soil drainage" term exists in Planteome (search returned zero results). Kept as the best available proxy rather than left unmapped, since the semantic distance is no worse than the AGROVOC alternative already accepted for `Downy_Mildew`-style broader matches. |

## Decision log

| Entity | Relation | Reviewer | Source | Date |
|---|---|---|---|---|
| `High_Humidity` | `skos:closeMatch` | Muhammad Ariful Furqon | EBI OLS4 search (PECO), children-check on PECO:0007197 | 2026-08-17 |
| `High_Temperature` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 search (PECO) | 2026-08-17 |
| `Low_Rainfall` | `skos:closeMatch` | Muhammad Ariful Furqon | EBI OLS4 search (PECO) | 2026-08-17 |
| `Poor_Soil_Drainage` | `skos:closeMatch` | Muhammad Ariful Furqon | EBI OLS4 search (PECO) | 2026-08-17 |

## Next review actions

1. `Poor_Soil_Drainage`'s match is the weakest of the four (cause-vs-effect,
   same caveat as its rejected AGROVOC candidate) — worth a second look if a
   more specific soil-drainage term turns up in a future PECO release.
2. Planteome has not yet been checked for the other open "needs domain
   review" items in `AGROVOC_alignment.md`: `Maturity_Stage` (Plant Ontology
   likely has a standardized growth-stage term), `Resistant_Variety`,
   `Brown_Lesion`, and the seven gap `Symptom` individuals — a first probe
   during this round already surfaced `TO:0000085` "leaf rolling response"
   as a promising candidate for `Leaf_Rolling` (currently local-only with no
   AGROVOC candidate at all), not yet formally reviewed or implemented.
3. `Excessive_Nitrogen` was not checked against Planteome in this round.


---

## Competency Question Validation (v0.6)

The four Planteome-aligned environmental factor entities (`High_Humidity`, `High_Temperature`, `Low_Rainfall`, `Poor_Soil_Drainage`) are actively evaluated in the **Rice MMKG 25 CQ Benchmark**:

- **CQ-05 (Contextual Multi-criteria, L2/D1):** Validates co-occurrence joins between growth stages and these environmental factors across 88 validated agronomic pairs (**81.2% PASS**).
- **CQ-11 (End-to-End Decision Support Chain, L3/D1):** Tests 4-hop traversals: `EnvironmentalFactor` → `Disease` → `Symptom` → `Treatment` across 277 full instantiations (**100% PASS**).
- **CQ-23 (External Alignment, L4/D3):** Verifies semantic interoperability with external bio-ontologies (**75% PASS**).
