# AGROVOC Alignment Register

## Purpose and scope

This register records proposed semantic links between Rice MMKG entities and the
FAO AGROVOC controlled vocabulary. It is a **review register**, not an imported
copy of AGROVOC. Rice MMKG remains responsible for multimodal observations,
causal relations, symptoms, treatments, and dataset provenance; AGROVOC is used
to improve shared agricultural terminology and interoperability.

**Source queried:** AGROVOC official SPARQL endpoint, `https://agrovoc.fao.org/sparql`  
**Query method:** English `skos:prefLabel` candidate search  
**Checked:** 2026-08-03

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
| `downy_mildew` | `Downy_Mildew` | Disease | [`downy mildews`](http://aims.fao.org/aos/agrovoc/c_10450) | `skos:closeMatch` | Needs domain review | Plural/generic AGROVOC concept may be broader than the local rice image class. |
| `tungro` | `Rice_Tungro_Disease` | Disease | [`tungro disease`](http://aims.fao.org/aos/agrovoc/c_34137) | `skos:exactMatch` | Implemented in v2.2 | Terminology match; retain the mapping register for future review. |
| `hispa` | `Hispa` | Pest | No relevant English concept found | — | Local-only / gap | Search hits for *hispanica* are not valid matches. |
| `dead_heart` | `Deadheart` | Symptom | No exact English concept found | — | Local-only / gap | Remains a symptom, not a disease. |
| `normal` | `Normal_Health` | HealthStatus | No concept selected | — | Local-only by design | Dataset-specific non-disease class. |

## Implemented mapping pattern

The three rows marked **Implemented in v2.2** are now present in
`Rice MMKG.rdf`. Keep the mapping triple separate from the dataset label:

```turtle
@prefix riceMMKG: <http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

riceMMKG:Rice_Blast_Disease
    skos:exactMatch <http://aims.fao.org/aos/agrovoc/c_152ac092> .
```

Do **not** infer disease-to-pathogen, disease-to-symptom, or treatment relations
from these vocabulary mappings. Those assertions require their own agricultural
literature evidence and provenance.

## Next review actions

1. Review the implemented mappings for `Rice`, `rice blast disease`, and
   `tungro disease`, and retain or revise them if a scope issue is discovered.
2. Manually inspect the hierarchy for `downy mildews` before selecting a
   `skos:closeMatch` or leaving the local entity unmapped.
3. Record source, reviewer, and date for every new mapping decision.
