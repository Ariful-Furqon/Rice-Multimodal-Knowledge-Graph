# AGROVOC Alignment Register

## Purpose and scope

This register records proposed semantic links between Rice MMKG entities and the
FAO AGROVOC controlled vocabulary. It is a **review register**, not an imported
copy of AGROVOC. Rice MMKG remains responsible for multimodal observations,
causal relations, symptoms, treatments, and dataset provenance; AGROVOC is used
to improve shared agricultural terminology and interoperability.

**Source queried:** AGROVOC official SPARQL endpoint, `https://agrovoc.fao.org/sparql`  
**Query method:** English `skos:prefLabel` candidate search (see below)  
**Checked:** 2026-08-03 (initial round), 2026-08-04 (rounds 2–4)

## Query method

Four reusable SPARQL templates against `https://agrovoc.fao.org/sparql`,
used in this order for every candidate lookup in this register.

**1. Find candidate concepts by label** — the first step for every entity.
Swap the term in `regex(...)` for the local entity's label or a plausible
synonym.

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?s ?label WHERE {
  ?s skos:prefLabel ?label .
  FILTER(lang(?label) = "en")
  FILTER(regex(?label, "downy mildew", "i"))
}
LIMIT 20
```

**2. Inspect a candidate concept's full detail** — prefLabel, altLabel,
`skos:broader`, external `skos:exactMatch` (e.g. to NALT). This is what
decides `exactMatch` vs. `closeMatch`: an altLabel matching the local term
supports `exactMatch`; a broader/generic concept with no matching altLabel
supports `closeMatch` or local-only.

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?p ?o WHERE {
  <http://aims.fao.org/aos/agrovoc/c_10450> ?p ?o
  FILTER(lang(?o) = "en" || lang(?o) = "")
}
```

**3. Check for a narrower (more specific) term** — used to confirm whether
a generic-looking candidate is really the most specific concept available,
before accepting it as `closeMatch` (e.g. `downy_mildew`, `stem_borer`).

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?s ?label WHERE {
  ?s skos:broader <http://aims.fao.org/aos/agrovoc/c_10450> ;
     skos:prefLabel ?label .
  FILTER(lang(?label) = "en")
}
```

**4. Batch-check altLabels across several candidates at once** — a
shortcut once multiple candidates are shortlisted from step 1, to avoid
repeating step 2 one-by-one.

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?s ?p ?o WHERE {
  VALUES ?s { <http://aims.fao.org/aos/agrovoc/c_25204> <http://aims.fao.org/aos/agrovoc/c_7389> }
  ?s ?p ?o .
  FILTER(?p IN (skos:altLabel, skos:prefLabel))
  FILTER(lang(?o) = "en")
}
```

**Decision rule applied consistently across all rounds:**
`exactMatch` requires an identical prefLabel or altLabel with matching
scope; `closeMatch` is used when the candidate is correct in meaning but
broader, narrower, or a different grammatical form (singular/plural,
common name/scientific name); a missing or category-mismatched candidate
is recorded as local-only rather than guessed.

## Mapping policy

- Preserve the Rice MMKG IRI as the canonical local identifier.
- Add `skos:exactMatch` only after the local and AGROVOC concepts are confirmed
  to have identical meaning and scope.
- Use `skos:closeMatch` where the candidate is similar but has a different
  scope, level of specificity, or grammatical form.
- Do not use `owl:sameAs` for vocabulary alignment.
- A missing candidate is valid evidence to keep an entity local; it is not a
  reason to create a guessed external URI.

## Initial alignment table

| Paddy Doctor label | Rice MMKG entity | Type | AGROVOC candidate | Proposed relation | Status | Decision note |
|---|---|---|---|---|---|---|
| — | `Rice` | Plant | [`rice`](http://aims.fao.org/aos/agrovoc/c_6599) | `skos:exactMatch` | Implemented in v2.2 | Same English concept label. |
| `bacterial_leaf_blight` | `Bacterial_Leaf_Blight` | Disease | No exact English concept found | — | Local-only / gap | Do not substitute the pathogen `Xanthomonas oryzae`; disease and pathogen are distinct entities. |
| `bacterial_leaf_streak` | `Bacterial_Leaf_Streak` | Disease | No exact English concept found | — | Local-only / gap | Retain local disease entity. |
| `bacterial_panicle_blight` | `Bacterial_Panicle_Blight` | Disease | No exact English concept found | — | Local-only / gap | Retain local disease entity. |
| `blast` | `Rice_Blast_Disease` | Disease | [`rice blast disease`](http://aims.fao.org/aos/agrovoc/c_152ac092) | `skos:exactMatch` | Implemented in v2.2 | Direct terminology match. |
| `brown_spot` | `Brown_Spot` | Disease | No exact English concept found | — | Local-only / gap | A generic phrase match must not be used as a rice-disease match. |
| `downy_mildew` | `Downy_Mildew` | Disease | [`downy mildews`](http://aims.fao.org/aos/agrovoc/c_10450) | `skos:closeMatch` | Implemented in v2.3 | Reviewed hierarchy: `skos:broader` is `c_4825` ("mildews"), no `skos:narrower` exists under `c_10450`, and no `skos:scopeNote` restricts it to a host plant. AGROVOC has no rice-specific downy mildew concept, so `closeMatch` (not `exactMatch`) is the ceiling given the local entity's rice-only scope. |
| `tungro` | `Rice_Tungro_Disease` | Disease | [`tungro disease`](http://aims.fao.org/aos/agrovoc/c_34137) | `skos:exactMatch` | Implemented in v2.2 | Terminology match; retain the mapping register for future review. |
| `hispa` | `Hispa` | Pest | No relevant English concept found | — | Local-only / gap | Search hits for *hispanica* are not valid matches. |
| `dead_heart` | `Deadheart` | Symptom | No exact English concept found | — | Local-only / gap | Remains a symptom, not a disease. |
| `normal` | `Normal_Health` | HealthStatus | No concept selected | — | Local-only by design | Dataset-specific non-disease class. |

## Pathogen and Pest alignment (round 2)

Extending beyond the Paddy Doctor label set to the `Pathogen` and `Pest`
individuals already in `Rice MMKG.rdf`. Checked 2026-08-04.

| Rice MMKG entity | Type | AGROVOC candidate | Proposed relation | Status | Decision note |
|---|---|---|---|---|---|
| `Magnaporthe_Oryzae` | Pathogen | [`Pyricularia oryzae`](http://aims.fao.org/aos/agrovoc/c_16025) | `skos:exactMatch` | Implemented in v2.4 | AGROVOC prefLabel is the anamorph name; `Magnaporthe oryzae` is a `skos:altLabel` on the same concept. |
| `Xanthomonas_Oryzae` | Pathogen | [`Xanthomonas oryzae`](http://aims.fao.org/aos/agrovoc/c_24383) | `skos:exactMatch` | Implemented in v2.4 | Direct label match. |
| `Bipolaris_Oryzae` | Pathogen | [`Cochliobolus miyabeanus`](http://aims.fao.org/aos/agrovoc/c_34512) | Not applied | Needs domain review | Same fungus under dual mycological nomenclature, but AGROVOC's `skos:altLabel` list for this concept only has `Helminthosporium oryzae` and `Drechslera oryzae` — `Bipolaris oryzae` itself is not present as any label. Do not assert `exactMatch` without a cited taxonomic source confirming the synonymy. |
| `Brown_Planthopper` | Pest | [`Nilaparvata lugens`](http://aims.fao.org/aos/agrovoc/c_25204) | `skos:exactMatch` | Implemented in v2.4 | AGROVOC prefLabel is the scientific name; `brown planthopper` is a `skos:altLabel` on the same concept — direct common-name confirmation. |
| `Stem_Borer` | Pest | [`stem eating insects`](http://aims.fao.org/aos/agrovoc/c_7389) | `skos:closeMatch` | Implemented in v2.4 | Generic pest-group concept (`skos:altLabel` "stem borers"); AGROVOC also has narrower species terms (e.g. `Scirpophaga incertulas`, yellow stem borer) but the local entity is generic, so the generic group is the better-scoped match — same pattern as the `Downy_Mildew` review. |
| `Leaf_Folder` | Pest | [`Cnaphalocrocis medinalis`](http://aims.fao.org/aos/agrovoc/c_30305) | Not applied | Needs domain review | This species is the internationally recognized "rice leaf folder," but AGROVOC has no `skos:altLabel` confirming the common name on this concept — matching requires an external taxonomic citation before asserting equivalence. |
| `Rice_Bug` | Pest | [`Leptocorisa oratorius`](http://aims.fao.org/aos/agrovoc/c_30653) or genus [`Leptocorisa`](http://aims.fao.org/aos/agrovoc/c_4277) | Not applied | Needs domain review | Local entity is generic; AGROVOC only has species-level terms (`Leptocorisa acuta` is also a common rice bug elsewhere), no common-name `altLabel` on either candidate. Decide species vs. genus scope before mapping. |
| `Armyworm` | Pest | No suitable candidate found | — | Local-only / gap | AGROVOC's `fall armyworms` (`Spodoptera frugiperda`, c_e6b223d7) is a maize pest, not a rice pest — a false-positive risk, not a match. `Mythimna separata`/`Mythimna unipuncta` (common rice armyworm species) carry no `armyworm` altLabel in AGROVOC. Do not guess; keep local-only. |

## GrowthStage, Treatment, and ManagementAction alignment (round 3)

Checked 2026-08-04.

| Rice MMKG entity | Type | AGROVOC candidate | Proposed relation | Status | Decision note |
|---|---|---|---|---|---|
| `Seedling_Stage` | GrowthStage | [`seedling stage`](http://aims.fao.org/aos/agrovoc/c_330777) | `skos:exactMatch` | Implemented in v2.5 | Direct label match. |
| `Vegetative_Stage` | GrowthStage | [`vegetative stage`](http://aims.fao.org/aos/agrovoc/c_330636) | `skos:exactMatch` | Implemented in v2.5 | Direct label match. |
| `Flowering_Stage` | GrowthStage | [`flowering stage`](http://aims.fao.org/aos/agrovoc/c_330768) | `skos:exactMatch` | Implemented in v2.5 | Direct label match. |
| `Maturity_Stage` | GrowthStage | [`ripening stage`](http://aims.fao.org/aos/agrovoc/c_330756) or generic [`maturity`](http://aims.fao.org/aos/agrovoc/c_4656) | Not applied | Needs domain review | No AGROVOC concept literally named "maturity stage." `ripening stage` is in the same phenological-stage series as the three exact matches above (same `c_3307xx` batch) and is agronomically close to physiological maturity, but no `skos:altLabel` confirms the two terms are synonymous — needs a cited source before choosing `ripening stage` over generic `maturity`. |
| `Harvest_Stage` | GrowthStage | No phenological-stage concept found | — | Local-only / gap | AGROVOC's `harvesting` (c_3500) is a process/activity concept, not a growth-stage/phenological concept — mapping would conflate an action with a plant life-stage, the same category error the mapping policy warns against for disease-vs-pathogen. |
| `Biological_Control` | Treatment | [`biological control`](http://aims.fao.org/aos/agrovoc/c_918) | `skos:exactMatch` | Implemented in v2.5 | Direct label match. |
| `Crop_Rotation` | Treatment | [`crop rotation`](http://aims.fao.org/aos/agrovoc/c_6662) | `skos:exactMatch` | Implemented in v2.5 | Direct label match. |
| `Water_Management` | Treatment | [`water management`](http://aims.fao.org/aos/agrovoc/c_8320) | `skos:exactMatch` | Implemented in v2.5 | Direct label match; AGROVOC also has narrower `water management in lowland` (c_330634), relevant if rice-paddy specificity is wanted later. |
| `Fungicide_Application` | Treatment | [`pesticide application`](http://aims.fao.org/aos/agrovoc/c_27879) | `skos:closeMatch` | Implemented in v2.5 | AGROVOC concept is the generic activity covering all pesticide types; `fungicides` (c_3146) was rejected as a candidate because it names the substance, not the application action. |
| `Insecticide_Application` | Treatment | [`pesticide application`](http://aims.fao.org/aos/agrovoc/c_27879) | `skos:closeMatch` | Implemented in v2.5 | Same generic-activity rationale as `Fungicide_Application`; `insecticides` (c_3887) rejected for the same substance-vs-action reason. |
| `Resistant_Variety` | Treatment | [`disease resistance`](http://aims.fao.org/aos/agrovoc/c_2328) | Not applied | Needs domain review | AGROVOC concept is the resistance trait/property; the local entity is a management strategy (choosing a resistant cultivar). Related but not the same category — decide whether to map at all before implementing. |
| `Monitoring` | ManagementAction | [`monitoring`](http://aims.fao.org/aos/agrovoc/c_4911) | `skos:exactMatch` | Implemented in v2.5 | Direct label match. |
| `Preventive_Action` | ManagementAction | No suitable candidate found | — | Local-only / gap | No AGROVOC concept for "preventive action" or "prevention" found. |
| `No_Action_Needed` | ManagementAction | Not searched | — | Local-only by design | Internal decision-support state, not an agricultural vocabulary term. |
| `Immediate_Intervention` | ManagementAction | Not searched | — | Local-only by design | Internal decision-support state, not an agricultural vocabulary term. |

## Symptom and EnvironmentalFactor alignment (round 4)

Checked 2026-08-04. As anticipated, this set has the highest gap rate of any
round so far — most local symptom/factor labels are compound descriptive
phrases with no single-concept AGROVOC equivalent.

| Rice MMKG entity | Type | AGROVOC candidate | Proposed relation | Status | Decision note |
|---|---|---|---|---|---|
| `Leaf_Spot` | Symptom | [`leaf spots`](http://aims.fao.org/aos/agrovoc/c_12119) | `skos:closeMatch` | Implemented in v2.6 | Same term, singular vs. plural grammatical form — the policy's textbook case for `closeMatch`. |
| `Wilting` | Symptom | [`wilting`](http://aims.fao.org/aos/agrovoc/c_8390) | `skos:exactMatch` | Implemented in v2.6 | Direct label match. |
| `Brown_Lesion` | Symptom | [`lesions`](http://aims.fao.org/aos/agrovoc/c_4283) | Not applied | Needs domain review | AGROVOC concept is a generic plant-pathology symptom with no color or leaf-location specificity; broader than the local entity, similar to the `Downy_Mildew` scope pattern but for a symptom rather than a disease. |
| `Chewed_Leaf` | Symptom | No candidate found | — | Local-only / gap | — |
| `Dry_Leaf_Tip` | Symptom | No candidate found | — | Local-only / gap | Searched "leaf tip" and "tip burn"; no match. |
| `Empty_Grain` | Symptom | No candidate found | — | Local-only / gap | Searched "grain sterility," "unfilled grain," "empty grain"; no match. |
| `Hopper_Burn` | Symptom | No candidate found | — | Local-only / gap | Searched "hopperburn" and "hopper burn"; no match. |
| `Leaf_Rolling` | Symptom | No candidate found | — | Local-only / gap | — |
| `Stem_Rot_Symptom` | Symptom | No candidate found | — | Local-only / gap | — |
| `Yellow_Leaf` | Symptom | No candidate found | — | Local-only / gap | Searched "leaf yellowing" and "yellowing"; no match. |
| `Excessive_Nitrogen` | EnvironmentalFactor | No candidate found | — | Local-only / gap | — |
| `High_Humidity` | EnvironmentalFactor | [`relative humidity`](http://aims.fao.org/aos/agrovoc/c_6496) | Not applied | Needs domain review | AGROVOC concept is the measured climate quantity (altLabels "air moisture," "atmospheric moisture"); the local entity is a qualitative state ("high"). Mapping a state to a quantity is a category mismatch — decide whether to keep local-only or accept the mismatch explicitly. |
| `High_Temperature` | EnvironmentalFactor | [`heat stress`](http://aims.fao.org/aos/agrovoc/c_11488) | Not applied | Needs domain review | AGROVOC concept is the plant's physiological stress response to heat, not the environmental condition itself — same category mismatch as `High_Humidity`. |
| `Low_Rainfall` | EnvironmentalFactor | [`drought`](http://aims.fao.org/aos/agrovoc/c_2391) | Not applied | Needs domain review | "Drought" typically implies more severity/duration than "low rainfall"; confirm the local entity's intended scope before mapping. |
| `Poor_Soil_Drainage` | EnvironmentalFactor | [`waterlogging`](http://aims.fao.org/aos/agrovoc/c_8333) | Not applied | Needs domain review | Waterlogging is the effect of poor drainage, not the drainage condition itself (cause vs. effect) — plausible in a rice-paddy context but should be a deliberate choice, not an automatic one. |

## Implemented mapping pattern

The three rows marked **Implemented in v2.2** are now present in
`Rice MMKG.rdf`. Keep the mapping triple separate from the dataset label:

```turtle
@prefix riceMMKG: <http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

riceMMKG:Rice_Blast_Disease
    skos:exactMatch <http://aims.fao.org/aos/agrovoc/c_152ac092> .
```

The **Implemented in v2.3** row uses `skos:closeMatch` instead, because the
AGROVOC candidate is broader in scope than the local entity:

```turtle
riceMMKG:Downy_Mildew
    skos:closeMatch <http://aims.fao.org/aos/agrovoc/c_10450> .
```

Do **not** infer disease-to-pathogen, disease-to-symptom, or treatment relations
from these vocabulary mappings. Those assertions require their own agricultural
literature evidence and provenance.

## Mapping decision log

| Entity | Relation | Reviewer | Source | Date |
|---|---|---|---|---|
| `Rice` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-03 |
| `Rice_Blast_Disease` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-03 |
| `Rice_Tungro_Disease` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-03 |
| `Downy_Mildew` | `skos:closeMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint (`skos:broader`/`skos:narrower` check on `c_10450`) | 2026-08-04 |
| `Magnaporthe_Oryzae` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-04 |
| `Xanthomonas_Oryzae` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-04 |
| `Brown_Planthopper` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint (`skos:altLabel` check) | 2026-08-04 |
| `Stem_Borer` | `skos:closeMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint (`skos:altLabel`/generic-group check on `c_7389`) | 2026-08-04 |
| `Seedling_Stage` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-04 |
| `Vegetative_Stage` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-04 |
| `Flowering_Stage` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-04 |
| `Biological_Control` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-04 |
| `Crop_Rotation` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-04 |
| `Water_Management` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-04 |
| `Fungicide_Application` | `skos:closeMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint (generic `pesticide application`, substance-vs-action check) | 2026-08-04 |
| `Insecticide_Application` | `skos:closeMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint (generic `pesticide application`, substance-vs-action check) | 2026-08-04 |
| `Monitoring` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-04 |
| `Leaf_Spot` | `skos:closeMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint (singular/plural grammatical-form check) | 2026-08-04 |
| `Wilting` | `skos:exactMatch` | Muhammad Ariful Furqon | AGROVOC SPARQL endpoint | 2026-08-04 |

## Next review actions

1. ~~Review the implemented mappings for `Rice`, `rice blast disease`, and
   `tungro disease`.~~ Done at initial mapping (2026-08-03); revisit only if a
   scope issue is discovered later.
2. ~~Manually inspect the hierarchy for `downy mildews` before selecting a
   `skos:closeMatch` or leaving the local entity unmapped.~~ Done 2026-08-04 —
   see decision log and updated table row above.
3. Continue recording source, reviewer, and date in the decision log above for
   every new mapping decision.
4. The seven remaining `Local-only / gap` entities from the Paddy Doctor set
   (`Bacterial_Leaf_Blight`, `Bacterial_Leaf_Streak`,
   `Bacterial_Panicle_Blight`, `Brown_Spot`, `Hispa`, `Deadheart`,
   `Normal_Health`) have no AGROVOC candidate on record. Re-attempt only if a
   new search strategy (alternate labels, broader terms) is worth trying;
   otherwise they remain local-only by design.
5. Three Pest/Pathogen candidates need a literature citation before they can
   move from "Needs domain review" to "Implemented": `Bipolaris_Oryzae`
   (confirm `Bipolaris oryzae` = `Cochliobolus miyabeanus` synonymy),
   `Leaf_Folder` (confirm `Cnaphalocrocis medinalis` = "rice leaf folder"),
   and `Rice_Bug` (decide species-level `Leptocorisa oratorius` vs.
   genus-level `Leptocorisa` scope).
6. `Armyworm` remains local-only; no rice-relevant AGROVOC candidate was
   found. Do not map it to `fall armyworms` (a maize pest).
7. Two GrowthStage/Treatment candidates need a citation before moving from
   "Needs domain review" to "Implemented": `Maturity_Stage` (choose between
   `ripening stage` and generic `maturity`) and `Resistant_Variety` (decide
   whether a trait concept, `disease resistance`, is an acceptable match for
   a cultivar-choice treatment strategy).
8. `Harvest_Stage`, `Preventive_Action`, `No_Action_Needed`, and
   `Immediate_Intervention` remain local-only; no suitable AGROVOC concept of
   the right category was found for any of them.
9. ~~Remaining unreviewed individuals in `Symptom` and `EnvironmentalFactor`.~~
   Checked 2026-08-04 — see round 4 table above.
10. Five candidates from round 4 need a scope decision before implementing:
    `Brown_Lesion` (`lesions`, generic-vs-specific), `High_Humidity`
    (`relative humidity`, state-vs-quantity), `High_Temperature`
    (`heat stress`, condition-vs-response), `Low_Rainfall` (`drought`,
    severity mismatch), and `Poor_Soil_Drainage` (`waterlogging`,
    cause-vs-effect).
11. Seven Symptom individuals have no AGROVOC candidate at all and stay
    local-only: `Chewed_Leaf`, `Dry_Leaf_Tip`, `Empty_Grain`, `Hopper_Burn`,
    `Leaf_Rolling`, `Stem_Rot_Symptom`, `Yellow_Leaf`. `Excessive_Nitrogen`
    (EnvironmentalFactor) is also local-only.
12. All individuals in `Disease`, `EnvironmentalFactor`, `GrowthStage`,
    `ManagementAction`, `Pathogen`, `Pest`, `Plant`, `Symptom`, and
    `Treatment` have now been checked at least once. Remaining classes
    (`HealthStatus`, `Observation`, `SeverityLevel`) are process/provenance
    or internal-scale types not expected to have AGROVOC equivalents.
