# NCBI Taxonomy Alignment Register

## Purpose and scope

This register records semantic links between Rice MMKG `Pathogen`/`Pest`
individuals and **NCBI Taxonomy**, kept separate from
[`AGROVOC_alignment.md`](AGROVOC_alignment.md) even though both use the same
`skos:exactMatch`/`skos:closeMatch` mechanism, because the two sources serve
different roles:

- **AGROVOC** — primary vocabulary for agricultural/vernacular terminology
  and interoperability (see the AGROVOC register).
- **NCBI Taxonomy** — citable authority for scientific names and
  synonyms, used specifically to supply the taxonomic evidence AGROVOC's own
  `skos:altLabel` data could not provide for a handful of organism-level
  entities. Every mapping in this register exists *because* the AGROVOC
  register flagged a "needs domain review" candidate that this source
  resolved (or, for `Rice_Bug`, did not fully resolve).

**Source queried:** NCBI E-utils, `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`  
**Query method:** scientific-name search → TaxID → full record inspection (see below)  
**Checked:** 2026-08-07, updated 2026-09-03 (Rice MMKG v0.6)

## Query method

Free public API; no registration or API key needed at this query volume.

**1. Find the TaxID for a scientific name:**

```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
    ?db=taxonomy&term=Bipolaris+oryzae&retmode=json
```

**2. Fetch the full record** (scientific name, rank, synonyms, common
names) for a TaxID:

```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
    ?db=taxonomy&id=101162&retmode=xml
```

Look at the `OtherNames` block in the response:

- A `<Synonym>` matching the AGROVOC candidate's prefLabel supports
  `exactMatch` on both sources at once.
- A `<GenbankCommonName>` matching the local entity's vernacular label is
  direct confirmation on its own.
- A `<Misspelling>` entry is worth recording even when it doesn't resolve
  the mapping — see `Rice_Bug` below, where it surfaced a spelling
  discrepancy with AGROVOC itself.

**Identifier used for alignment:** the OBO Foundry PURL form
(`http://purl.obolibrary.org/obo/NCBITaxon_<taxid>`), the standard
cross-referenced identifier for NCBI taxa in the semantic web / bio-ontology
community, rather than the plain `ncbi.nlm.nih.gov` web page URL.

## Mapping policy

Same rule as the AGROVOC register: `exactMatch` requires an identical
scientific name or a listed synonym/common name with matching scope;
`closeMatch` for a correct-but-broader/narrower candidate; a missing or
unconfirmed candidate stays local-only (or, here, stays open in AGROVOC's
"needs domain review" state) rather than being guessed.

## Alignment table

| Rice MMKG entity | Type | NCBI candidate | Proposed relation | Status | Decision note |
|---|---|---|---|---|---|
| `Bipolaris_Oryzae` | Pathogen | [Bipolaris oryzae, TaxID 101162](http://purl.obolibrary.org/obo/NCBITaxon_101162) | `skos:exactMatch` | Implemented in v2.7 | NCBI's `OtherNames` for TaxID 101162 lists `Cochliobolus miyabeanus` (the AGROVOC `c_34512` prefLabel) and `Helminthosporium oryzae` as `<Synonym>` entries for the same organism whose accepted scientific name is "Bipolaris oryzae" — this independently confirms the synonymy AGROVOC's own altLabel list could not. AGROVOC's `c_34512` mapping was upgraded from "needs domain review" to `exactMatch` on the strength of this citation; see `AGROVOC_alignment.md`. |
| `Leaf_Folder` | Pest | [Cnaphalocrocis medinalis, TaxID 437488](http://purl.obolibrary.org/obo/NCBITaxon_437488) | `skos:exactMatch` | Implemented in v2.7 | `GenbankCommonName` = "rice leaffolder" for TaxID 437488 — direct common-name confirmation. AGROVOC's `c_30305` mapping was likewise upgraded to `exactMatch`. |
| `Rice_Bug` | Pest | [Leptocorisa oratoria, TaxID 2724160](http://purl.obolibrary.org/obo/NCBITaxon_2724160) | Not applied | Needs domain review | The species exists in NCBI, but under the spelling **"Leptocorisa oratoria"**; AGROVOC's candidate spelling `Leptocorisa oratorius` is recorded in NCBI as a `<Misspelling>` of this same species. No `<GenbankCommonName>` ("rice bug" or similar) is present. Two open questions before mapping: (1) species (`Leptocorisa oratoria`) vs. genus (`Leptocorisa`) scope, since the local entity is generic; (2) which spelling to standardize on across both registers. Still open as of 2026-08-22 — a same-day AI-assisted lookup proposed applying the AGROVOC `oratorius` spelling as `exactMatch` without resolving either open question; not accepted, this entity remains local-only pending proper review. |

## New-organism alignment (round 2)

Checked 2026-08-22, via EBI OLS4 (`https://www.ebi.ac.uk/ols4/api/search?ontology=ncbitaxon`)
rather than NCBI's own E-utils, against the `Pathogen`/`Pest` individuals
added in the 2026-08-21 domain-graph enrichment. Each row's TaxID and label
were read directly from the OLS4 response, with binomial spelling checked
against that response rather than assumed.

| Rice MMKG entity | Type | NCBI candidate | Proposed relation | Status | Decision note |
|---|---|---|---|---|---|
| `Burkholderia_Glumae` | Pathogen | [Burkholderia glumae, TaxID 337](http://purl.obolibrary.org/obo/NCBITaxon_337) | `skos:exactMatch` | Implemented | Exact literal label match; distinguished from strain-specific entries (e.g. TaxID 626418, "BGR1") also returned by the search. |
| `Nephotettix_Virescens` | Pest | [Nephotettix virescens, TaxID 1032906](http://purl.obolibrary.org/obo/NCBITaxon_1032906) | `skos:exactMatch` | Implemented | Exact literal label match; distinguished from the unrelated "Wolbachia endosymbiont of Nephotettix virescens" entry. |
| `Rice_Tungro_Bacilliform_Virus` | Pathogen | [Rice tungro bacilliform virus, TaxID 10654](http://purl.obolibrary.org/obo/NCBITaxon_10654) | `skos:exactMatch` | Implemented | Exact literal label match. |
| `Rice_Tungro_Spherical_Virus` | Pathogen | [Rice tungro spherical virus, TaxID 35287](http://purl.obolibrary.org/obo/NCBITaxon_35287) | `skos:exactMatch` | Implemented | Exact literal label match. |
| `Stem_Borer` (`Scirpophaga_Incertulas`) | Pest | [Scirpophaga incertulas, TaxID 72366](http://purl.obolibrary.org/obo/NCBITaxon_72366) | `skos:exactMatch` | Implemented | Exact literal label match. In v0.5/v0.6, `Scirpophaga_Incertulas` was merged into canonical `Stem_Borer` as altLabel, with TaxID 72366 attached directly. |
| `Sclerophthora_Macrospora` | Pathogen | [Sclerophthora macrospora, TaxID 467176](http://purl.obolibrary.org/obo/NCBITaxon_467176) | `skos:exactMatch` | Implemented | Exact literal label match; carefully distinguished from the unrelated "Sclerophthora macrospora virus A/B" entries also returned. |
| `Xanthomonas_Oryzicola` | Pathogen | [Xanthomonas oryzae pv. oryzicola, TaxID 129394](http://purl.obolibrary.org/obo/NCBITaxon_129394) | `skos:exactMatch` | Implemented | Exact literal label match, pathovar spelling verified. AGROVOC's `c_330601` (same organism, prefLabel "Xanthomonas oryzae pv. oryzicola") is available too but is *not* used to align the `Bacterial_Leaf_Streak` **disease** individual — see `AGROVOC_alignment.md` round 5's reconfirmed-local-only note on that entity. |
| `Hispa` | Pest | [Dicladispa armigera, TaxID 111238](http://purl.obolibrary.org/obo/NCBITaxon_111238) | `skos:exactMatch` | Implemented | AGROVOC's initial round found no relevant concept for "hispa" (search hits for *hispanica* were rejected as invalid) — same NCBI-as-fallback pattern already established for `Bipolaris_Oryzae`/`Leaf_Folder`. Common name "rice hispa" confirmed via species identity, binomial spelling verified against the OLS4 response. |

## Decision log

| Entity | Relation | Reviewer | Source | Date |
|---|---|---|---|---|
| `Bipolaris_Oryzae` | `skos:exactMatch` | Muhammad Ariful Furqon | NCBI Taxonomy E-utils (TaxID 101162, synonym check) | 2026-08-07 |
| `Leaf_Folder` | `skos:exactMatch` | Muhammad Ariful Furqon | NCBI Taxonomy E-utils (TaxID 437488, GenbankCommonName check) | 2026-08-07 |
| `Burkholderia_Glumae` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 (ncbitaxon) | 2026-08-22 |
| `Nephotettix_Virescens` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 (ncbitaxon) | 2026-08-22 |
| `Rice_Tungro_Bacilliform_Virus` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 (ncbitaxon) | 2026-08-22 |
| `Rice_Tungro_Spherical_Virus` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 (ncbitaxon) | 2026-08-22 |
| `Scirpophaga_Incertulas` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 (ncbitaxon) | 2026-08-22 |
| `Sclerophthora_Macrospora` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 (ncbitaxon) | 2026-08-22 |
| `Xanthomonas_Oryzicola` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 (ncbitaxon) | 2026-08-22 |
| `Hispa` | `skos:exactMatch` | Muhammad Ariful Furqon | EBI OLS4 (ncbitaxon) | 2026-08-22 |

## Next review actions

1. Resolve `Rice_Bug`: decide species-vs-genus scope, and reconcile the
   `Leptocorisa oratoria` (NCBI) vs. `Leptocorisa oratorius` (AGROVOC)
   spelling discrepancy — flag the discrepancy back to the AGROVOC register
   if AGROVOC's own concept label turns out to need a correction request.
2. As of round 2 (2026-08-22) this register covers ten Pest/Pathogen
   entities: the original three AGROVOC could not resolve on its own, plus
   seven organisms added in the 2026-08-21 domain-graph enrichment that
   had no prior alignment of any kind. Other `Pathogen`/`Pest` individuals
   already have a clean AGROVOC `exactMatch` (see `AGROVOC_alignment.md`)
   and were not re-checked here — a full NCBI cross-check of all
   `Pathogen`/`Pest` individuals has not been done and is optional future
   work, not a known gap.
3. `GrowthStage`, `Treatment`, `ManagementAction`, `Symptom`, and
   `EnvironmentalFactor` entities are out of scope for NCBI Taxonomy (it
   only covers organisms) — their "needs domain review" items remain
   tracked in `AGROVOC_alignment.md` only.
