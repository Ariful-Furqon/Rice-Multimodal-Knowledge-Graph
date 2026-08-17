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
**Checked:** 2026-08-07

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
| `Rice_Bug` | Pest | [Leptocorisa oratoria, TaxID 2724160](http://purl.obolibrary.org/obo/NCBITaxon_2724160) | Not applied | Needs domain review | The species exists in NCBI, but under the spelling **"Leptocorisa oratoria"**; AGROVOC's candidate spelling `Leptocorisa oratorius` is recorded in NCBI as a `<Misspelling>` of this same species. No `<GenbankCommonName>` ("rice bug" or similar) is present. Two open questions before mapping: (1) species (`Leptocorisa oratoria`) vs. genus (`Leptocorisa`) scope, since the local entity is generic; (2) which spelling to standardize on across both registers. |

## Decision log

| Entity | Relation | Reviewer | Source | Date |
|---|---|---|---|---|
| `Bipolaris_Oryzae` | `skos:exactMatch` | Muhammad Ariful Furqon | NCBI Taxonomy E-utils (TaxID 101162, synonym check) | 2026-08-07 |
| `Leaf_Folder` | `skos:exactMatch` | Muhammad Ariful Furqon | NCBI Taxonomy E-utils (TaxID 437488, GenbankCommonName check) | 2026-08-07 |

## Next review actions

1. Resolve `Rice_Bug`: decide species-vs-genus scope, and reconcile the
   `Leptocorisa oratoria` (NCBI) vs. `Leptocorisa oratorius` (AGROVOC)
   spelling discrepancy — flag the discrepancy back to the AGROVOC register
   if AGROVOC's own concept label turns out to need a correction request.
2. This register currently only covers the three Pest/Pathogen entities
   that AGROVOC could not resolve on its own. Other `Pathogen`/`Pest`
   individuals already have a clean AGROVOC `exactMatch` (see
   `AGROVOC_alignment.md`) and were not re-checked here — a full NCBI
   cross-check of all `Pathogen`/`Pest` individuals has not been done and
   is optional future work, not a known gap.
3. `GrowthStage`, `Treatment`, `ManagementAction`, `Symptom`, and
   `EnvironmentalFactor` entities are out of scope for NCBI Taxonomy (it
   only covers organisms) — their "needs domain review" items remain
   tracked in `AGROVOC_alignment.md` only.
