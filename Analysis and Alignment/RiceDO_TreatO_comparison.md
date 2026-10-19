# RiceDO v2 and TreatO v2: measured comparison and candidate mappings

**Status:** analysis only (2026-10-19). Nothing has been added to `Rice MMKG.rdf`; the
candidate mappings below await a decision.

## Sources

| | RiceDO v2 | TreatO v2 |
|---|---|---|
| DOI | 10.21227/5ndq-4222 (IEEE DataPort) | 10.21227/5016-aw09 (IEEE DataPort) |
| File | `Data/Candidates/RiceDO-Version2.owl.zip` | `Data/Candidates/TreatO-Version2.owl.zip` |
| Format | OWL/XML, saved 2021-03-20 | OWL/XML, saved 2021-03-20 |
| Ontology IRI | `http://purl.org/ricedo` | `http://purl.org/treato` |
| Licence | **not stated in the file**; to be read on the DataPort page | same |

Read with owlready2 0.51 on 2026-10-19 from a copy extracted to a scratch folder;
reasoned with HermiT (Java 21).

## Measured profile

| | RiceDO v2 | TreatO v2 | Rice MMKG 0.7.0-dev |
|---|---:|---:|---:|
| Classes | 164 | 66 (4 from RiceDO) | 29 |
| Object properties | 13 | 8 | 41 |
| Datatype properties | 0 | 0 | 27 |
| Named individuals | **0** | **0** | 36,303 |
| `SubClassOf` axioms | 276 | 134 | — |
| …with an axiom-level source | **0** | **0** | 377 of 377 domain assertions reified with source and evidence type |
| Definitions (`IAO_0000115`) | 173 | 68 | — |
| HermiT | consistent, 0 unsatisfiable | consistent, 0 unsatisfiable | consistent, 0 unsatisfiable |
| IRIs resolve (2026-10-19) | no: `purl.org/ricedo` → `riceman.info/ricedo/`, connection fails; disease IRIs `purl.obolibrary.org/obo/PDO_…` → 404 | no: `purl.org/treato` → `riceman.info/treato/`, connection fails | yes: `w3id.org/ricemmkg#` |
| Observation data | none | none | images, sensor, light-trap, multispectral |

### How the knowledge is modelled

- **Everything is class-level.** A disease is a class; its symptoms, colours,
  shapes, growth stages and plant parts are existential restrictions on it
  (`abnormalityGroup some (spot on leaf and hasColor some brown and hasGrowthstage some tillering)`).
  Rice MMKG states the same kind of knowledge as individual-level assertions
  (`Brown_Spot indicatedBy Dusty_Brown_Spot`), each with a cited source.
- **Symptoms are post-coordinated.** RiceDO builds a symptom from primitives:
  29 abnormality types (spot, lesion, wilt, …), 28 colours, 12 shapes and 23
  plant parts. Rice MMKG has 40 pre-coordinated symptoms (`Zonate_Leaf_Lesion`).
- **Colour sets use intersection, never union.** 167 `ObjectIntersectionOf`,
  0 `ObjectUnionOf`; e.g. brown spot `hasColor some (brown and dark brown and gray)`.
  Read literally this asks for one colour that is all three at once. HermiT
  finds no contradiction because only 2 colour pairs are declared disjoint
  and none of them meets in one intersection; the intended reading is almost
  certainly a union.
- **Treatments are agents.** TreatO lists 18 chemical agents (13 fungicides,
  4 insecticides, 1 bactericide) and 11 bacterial biological control agents,
  each linked to diseases or pest damage (`Validamycin isChemicalControlAgentOf some rice sheath blight fungal disease`).
  Rice MMKG treatments are practices (`Fungicide_Application`), not products.
  The fungal and viral biological control agent classes in TreatO are empty.

## Coverage against Rice MMKG

### Diseases: 7 of Rice MMKG's 16 have a RiceDO class

| Rice MMKG | RiceDO | Candidate |
|---|---|---|
| `Bacterial_Leaf_Blight` | `PDO_0000014` rice bacterial blight disease (def.: caused by *X. oryzae* pv. *oryzae*) | `exactMatch` |
| `Bacterial_Leaf_Streak` | `PDO_0000019` rice bacterial leaf streak disease (pv. *oryzicola*) | `exactMatch` |
| `Brown_Spot` | `PDO_0000033` rice brown spot fungal disease (*Bipolaris oryzae*) | `exactMatch` |
| `Leaf_Scald` | `PDO_0000047` rice leaf scald fungal disease | `exactMatch` |
| `Rice_Blast_Disease` | `PDO_0000031` rice blast fungal disease | `exactMatch` |
| `Rice_Tungro_Disease` | `PDO_0000131` rice tungro viral disease | `exactMatch` |
| `Sheath_Blight` | `PDO_0000051` rice sheath blight fungal disease (*Rhizoctonia solani*) | `exactMatch` |

Not in RiceDO: `Bacterial_Panicle_Blight`, `Downy_Mildew`, `Deadheart`, and all
six abiotic disorders (RiceDO has no abiotic disease).

In RiceDO, not in Rice MMKG (11): grassy stunt, ragged stunt, gall dwarf (viral);
false smut, narrow brown leaf spot, sheath rot, stem rot, bakanae, dirty panicle
(fungal); yellow dwarf, orange leaf (phytoplasma).

Effect on alignment: diseases with an external link **3/16 → 8/16** (blast and
tungro already have AGROVOC links; downy mildew keeps its AGROVOC `closeMatch`).

### Pests: 2 of 7

| Rice MMKG | RiceDO | Candidate |
|---|---|---|
| `Brown_Planthopper` | `RiceDO_000121` brown planthopper | `exactMatch` |
| `Nephotettix_Virescens` | `RiceDO_000122` green rice leafhopper | `exactMatch` |

`Rice_Bug` (*Leptocorisa*) is **not** RiceDO's rice black bug (*Scotinophara*).
RiceDO has no stem borer, leaf folder, hispa or armyworm; Rice MMKG has no
zigzag leafhopper or rice black bug. RiceDO's pest scope is the insect vectors
of viral and phytoplasma diseases.

### Plant parts and growth stages

| Rice MMKG | RiceDO | Candidate |
|---|---|---|
| `Leaf`, `Panicle`, `Root`, `Stem`, `Tiller` | leaf, panicle, root, stem, tiller | `exactMatch` |
| `Leaf_Sheath` | sheath leaf | `closeMatch` |
| `Panicle_Neck` | neck | `closeMatch` |
| `Flowering_Stage`, `Maturity_Stage`, `Tillering_Stage` | flowering, maturity, tillering | `exactMatch` |

RiceDO files *seedling* under plant parts, not growth stages.

### Symptoms: no one-to-one mapping proposed

RiceDO's symptom vocabulary is compositional, so a Rice MMKG symptom matches a
*combination* of RiceDO classes, not one class. A few primitives line up
(`Wilting` ≈ wilt, `Stunted_Growth` ≈ stunt, `Empty_Grain` ≈ unfill,
`Leaf_Spot` ≈ spot on leaf, `Leaf_Sheath_Lesion` ≈ lesion on sheath), but
mapping them alone would lose colour and shape. Left for a decision.

### Treatments (TreatO)

No `exactMatch` is possible: Rice MMKG names practices, TreatO names products.
Candidate `relatedMatch` only: `Chemical_Control_Category` ↔ chemical control
agent, `Biological_Control_Category` ↔ biological control agent,
`Fungicide_Application` ↔ fungicide chemical control agent,
`Insecticide_Application` ↔ insecticide chemical control agent.

TreatO's product-to-disease links are the one body of knowledge Rice MMKG lacks.
They carry no source per axiom, so under Rice MMKG's rule (every domain
assertion reified with its source) they could enter only with evidence type
"ontology-derived" citing the TreatO DOI, or after each is checked against a
fact sheet.

## Candidate mappings, if approved

| Kind | Count |
|---|---:|
| Diseases `exactMatch` | 7 |
| Pests `exactMatch` | 2 |
| Plant parts `exactMatch` / `closeMatch` | 5 / 2 |
| Growth stages `exactMatch` | 3 |
| Treatment categories `relatedMatch` | 4 |
| **Total** | **23** |

## Decisions needed

1. Apply the 23 SKOS mappings (or only the 19 exact/close ones).
2. Whether RiceDO IRIs may be used although they do not resolve today.
3. Whether to import TreatO's product–disease links, and under which evidence rule.
4. Licence of both files, from the DataPort pages, before any content is reused.
