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
**Checked:** 2026-08-17, verified 2026-09-03 (Rice MMKG v0.6); PlantPart round 2026-09-15 (Rice MMKG 0.7.0-dev)

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

## PlantPart alignment (round 2)

Checked 2026-09-15 against the **Plant Ontology (PO)** for the new `PlantPart` individuals (Rice MMKG 0.7.0-dev). Unlike round 1, these entities were created together with their alignment, so there is no AGROVOC candidate column.

**Query method:** same as round 1 — free-text search restricted to `ontology=po`; where the label search found nothing, `queryFields=label,synonym` was used to reach synonym-only terms (this is how PO:0005001 was found for "tiller"). Part-of relations were read from `GET https://www.ebi.ac.uk/ols4/api/ontologies/po/terms/<double-encoded-iri>/graph`, which lists the term's `part of` edges.

| Rice MMKG entity | Planteome candidate | Relation | Status | Decision note |
|---|---|---|---|---|
| `Whole_Plant` | [`whole plant`](http://purl.obolibrary.org/obo/PO_0000003) (PO:0000003) | `skos:exactMatch` | Implemented | Same meaning and category. |
| `Leaf` | [`leaf`](http://purl.obolibrary.org/obo/PO_0025034) (PO:0025034) | `skos:exactMatch` | Implemented | Needed only as the whole in `partOf`. PO's leaf lamina is part_of this term; leaf sheath is part_of its subclass `vascular leaf` (PO:0009025). |
| `Leaf_Blade` | [`leaf lamina`](http://purl.obolibrary.org/obo/PO_0020039) (PO:0020039) | `skos:exactMatch` | Implemented | "leaf blade" is a listed synonym; lamina and blade name the same organ. |
| `Leaf_Sheath` | [`leaf sheath`](http://purl.obolibrary.org/obo/PO_0020104) (PO:0020104) | `skos:exactMatch` | Implemented | Exact label match; PO notes the term is typical of Poaceae. |
| `Panicle` | [`panicle inflorescence`](http://purl.obolibrary.org/obo/PO_0030123) (PO:0030123) | `skos:exactMatch` | Implemented | "panicle" is an exact synonym. |
| `Tiller` | [`basal axillary shoot system`](http://purl.obolibrary.org/obo/PO_0005001) (PO:0005001) | `skos:closeMatch` | Implemented | "tiller" is only a *narrow* synonym here, and a label search for "tiller" returns growth stages, not an anatomy term. No more specific term exists. |
| `Grain` | [`caryopsis fruit`](http://purl.obolibrary.org/obo/PO_0030104) (PO:0030104) | `skos:closeMatch` | Implemented | PO's synonyms ("brown rice", "dehulled grain") show the term is the dehulled grain, whereas a rice grain in the field carries its hull. Scope mismatch, not category. |
| `Panicle_Neck` | none | — | Local only | Searches for "neck" and "panicle neck" return only bryophyte terms (archegonium/sporangium neck). |

`partOf` (itself `skos:closeMatch` to [BFO:0000050 *part of*](http://purl.obolibrary.org/obo/BFO_0000050)) is asserted only where PO records the relation: `Leaf_Blade partOf Leaf` (PO:0020039 part_of PO:0025034) and `Leaf_Sheath partOf Leaf` (PO:0020104 part_of PO:0009025, which is_a PO:0025034). The graph endpoint returned no part_of edge for panicle inflorescence, caryopsis fruit or basal axillary shoot system, so no `partOf` is asserted for `Panicle`, `Grain` or `Tiller`. Both assertions carry an `owl:Axiom` whose source is the PO term and whose `evidenceType` is `ontology-derived`.

## Decision log

| Entity | Relation | Reviewer | Source | Date |
|---|---|---|---|---|
| `High_Humidity` | `skos:closeMatch` | Muhammad Ariful Furqon | EBI OLS4 search (PECO), children-check on PECO:0007197 | 2026-08-17 |
| `High_Temperature` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 search (PECO) | 2026-08-17 |
| `Low_Rainfall` | `skos:closeMatch` | Muhammad Ariful Furqon | EBI OLS4 search (PECO) | 2026-08-17 |
| `Poor_Soil_Drainage` | `skos:closeMatch` | Muhammad Ariful Furqon | EBI OLS4 search (PECO) | 2026-08-17 |
| `Whole_Plant`, `Leaf`, `Leaf_Blade`, `Leaf_Sheath`, `Panicle` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 search (PO) | 2026-09-15 |
| `Tiller` | `skos:closeMatch` | Muhammad Ariful Furqon | EBI OLS4 synonym search (PO) | 2026-09-15 |
| `Grain` | `skos:closeMatch` | Muhammad Ariful Furqon | EBI OLS4 search (PO) | 2026-09-15 |
| `Panicle_Neck` | local only | Muhammad Ariful Furqon | EBI OLS4 search (PO), no candidate | 2026-09-15 |
| `Leaf_Blade partOf Leaf`, `Leaf_Sheath partOf Leaf` | `rice:partOf` | Muhammad Ariful Furqon | EBI OLS4 term graph (PO part_of edges) | 2026-09-15 |

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
