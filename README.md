# Rice MMKG — Rice Multimodal Knowledge Graph

An OWL ontology and knowledge graph modeling rice diseases, pests, pathogens, symptoms, environmental factors, growth stages, treatments, and management actions — populated from a large public image dataset, with sensor and text modalities designed in but not yet populated.

![Rice MMKG diagram](RiceMMKG.png)

## Overview

Rice MMKG links agronomic and entomological knowledge about rice cultivation into a single queryable graph, connecting what is *observed* (currently: images; sensor readings and field/text reports are declared extension points) to its *cause* (pathogens, pests, environmental stressors) and the *response* (treatments, management actions), scoped by growth stage and severity.

Two design principles run through the whole model:

- **Observation is kept separate from domain knowledge.** An `ImageObservation`'s raw dataset label (`annotatedAs`) is never conflated with the curated symptom/cause/treatment relations (`captures`, `causes`, `indicatedBy`, ...) that constitute the actual domain knowledge — what was recorded is not the same claim as what is concluded.
- **Every domain-level assertion is traceable.** All 265 populated `causes`/`indicatedBy`/`occursIn`/`controlledBy`/`preventedBy`/`increaseRiskOf`/`vulnerableTo`/`recommends`/`requires`/`transmits` triples are reified with `owl:Axiom` and carry `dcterms:source`, `dcterms:bibliographicCitation`, and `rice:evidenceType` — 100% coverage, verified by an automated harness, not asserted.

- **Namespace:** `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#`
- **Format:** OWL/XML (`.rdf`), editable in [Protégé](https://protege.stanford.edu/)
- **Version:** `0.5` — pre-1.0, actively under construction toward an ESWC resource-track submission (see `Ontology/riceMMKG_ESWC_plan.md`)

## Ontology structure

### Classes (16)

| Class | Individuals | Description |
|---|---:|---|
| `ImageObservation` | 10,407 | Paddy Doctor field image instances |
| `SymptomaticObservation` | *(1,442 materialised)* | Defined class (`captures some Symptom`) — populated by a reasoner, not directly asserted |
| `SensorObservation` | 0 | Declared extension point for a future sensor modality |
| `Observation` | 0 | Abstract root observation superclass |
| `Dataset` (`dcat:Dataset`) | 1 | Dataset-level metadata individual for the source image collection |
| `Disease` | 8 | e.g. Bacterial Leaf Blight, Rice Blast, Brown Spot, Sheath Blight, Rice Tungro Disease |
| `Pest` | 7 | e.g. Stem Borer, Leaf Folder, Brown Planthopper, Armyworm, Rice Bug, Hispa |
| `Pathogen` | 8 | Causal organisms, e.g. Magnaporthe Oryzae, Xanthomonas Oryzae, the two tungro viruses |
| `Plant` | 1 | The crop (*Oryza sativa*) |
| `HealthStatus` | 1 | Non-disease reference condition (Normal / Healthy) |
| `Symptom` | 28 | Observable signs, e.g. Leaf Rolling, Deadheart, White Ear, Water-Soaked Streak |
| `GrowthStage` | 7 | Seedling, Tillering, Vegetative, Reproductive, Flowering, Maturity, Harvest |
| `EnvironmentalFactor` | 9 | e.g. High Humidity, High Temperature, Waterlogged Soil, Presence of Leafhopper Vector |
| `SeverityLevel` | 4 | Low, Medium, High, Critical |
| `Treatment` | 12 | Interventions, e.g. Fungicide/Insecticide Application, Biological Control, Resistant Variety |
| `ManagementAction` | 5 | Recommended actions, e.g. Field Inspection, Monitoring, Immediate Intervention |

### Object properties (26)

Relations connect the classes above, each with a defined inverse:

`causes`/`causedBy`, `transmits`/`transmittedBy`, `threatens`, `indicates`/`indicatedBy`, `controls`/`controlledBy`, `prevents`/`preventedBy`, `recommends`/`recommendedFor`, `requires`/`requiredFor`, `captures`/`capturedBy`, `detects`/`detectedBy`, `occursIn`, `hasOccurrenceOf`, `increaseRiskOf`/`riskIncreasedBy`, `vulnerableTo`, `annotatedAs`/`annotationOf`

`causes` is scoped to `Pathogen → Disease` only; vector-borne transmission (e.g. a leafhopper transmitting the tungro viruses, rather than "causing" the disease itself) is modeled separately through `transmits`/`transmittedBy` (`Pest → Pathogen`) — a distinction none of the comparator rice ontologies make.

### Datatype properties (5)

`confidenceScore`, `severityScore`, `interventionThreshold`, `observationDate`, `sourceDatasetLabel`

### Individuals

**10,498 named individuals**: 10,407 `ImageObservation` instances from the Paddy Doctor dataset, plus 91 domain-level individuals (diseases, pests, pathogens, symptoms, environmental factors, growth stages, treatments, management actions).

**265 domain-level relation assertions**, 100% provenance-backed: every one carries an `owl:Axiom` reification citing its source (IRRI Rice Doctor / Knowledge Bank, CABI Crop Protection Compendium, EPPO Global Database, BBPOPT, and peer-reviewed literature — Ou 1985, Hibino 1996, Ham et al. 2011). Nothing in the populated relations is asserted without a citation; where the literature didn't support a claim, the relation was left unpopulated rather than guessed.

**External alignment**: 33 `skos:exactMatch`, 17 `skos:closeMatch`, 1 `skos:broadMatch` to AGROVOC and NCBI Taxonomy concept URIs, each individually checked against a live API response — see `Ontology/AGROVOC_alignment.md` and `Ontology/NCBI_Taxonomy_alignment.md` for the full review trail (query method, decision rule, and a logged decision for every mapping, including rejected candidates).

### Paddy Doctor alignment

The local Paddy Doctor image dataset is deliberately excluded from Git (`/Data/`). Its folder labels are preserved in the ontology through `sourceDatasetLabel`/`annotatedAs`, so data ingestion can create traceable KG assertions without relying on folder names as ontology identifiers.

| Paddy Doctor label | Rice MMKG entity | Semantic type |
|---|---|---|
| `bacterial_leaf_blight` | `Bacterial_Leaf_Blight` | Disease |
| `bacterial_leaf_streak` | `Bacterial_Leaf_Streak` | Disease |
| `bacterial_panicle_blight` | `Bacterial_Panicle_Blight` | Disease |
| `blast` | `Rice_Blast_Disease` | Disease |
| `brown_spot` | `Brown_Spot` | Disease |
| `downy_mildew` | `Downy_Mildew` | Disease |
| `tungro` | `Rice_Tungro_Disease` | Disease |
| `hispa` | `Hispa` | Pest |
| `dead_heart` | `Deadheart` | Symptom |
| `normal` | `Normal_Health` | HealthStatus |

## Repository contents

```
Ontology/
  Rice MMKG.rdf              # the ontology (OWL/XML), v0.5
  Ontology_Overview.md       # structure, statistics, and a dated changelog of every revision
  riceMMKG_ESWC_plan.md      # construction plan toward an ESWC resource-track submission
  Backup/                    # dated snapshots of the ontology file
Analysis and Alignment/
  AGROVOC_alignment.md       # reviewed AGROVOC vocabulary alignment, with full query/decision trail
  NCBI_Taxonomy_alignment.md # organism-level alignment to NCBI Taxonomy
  Planteome_alignment.md     # environmental-factor alignment to PO/TO/PECO/PSO
  PaddyDoctor_Dataset_Analysis.md # local dataset profile and KG population plan
Worklog/
  RiceMMKG_v0.3_worklog/     # dated task specs, scripts, and reports for each ontology revision
  RiceMMKG_v0.4_worklog/
  RiceMMKG_v0.5_worklog/
Data/                        # local dataset (gitignored, not versioned)
Multimodal Fusion PoC/       # local experimentation (gitignored, not versioned)
RiceMMKG.png / .jpg          # ontology diagram
```

## Usage

Open `Ontology/Rice MMKG.rdf` in [Protégé](https://protege.stanford.edu/) to browse, edit, or reason over the ontology, or load it with any RDF/OWL library (e.g. `rdflib`, Apache Jena, OWL API) for programmatic querying.

```python
from rdflib import Graph

g = Graph()
g.parse("Ontology/Rice MMKG.rdf", format="xml")
print(f"{len(g)} triples loaded")
```

Each `Worklog/RiceMMKG_v*_worklog/` directory includes a `verify.py` harness that reproduces the ontology's key statistics (triple/class/individual counts, provenance coverage, duplicate-identifier and range-conformance checks) — the most reliable way to confirm the file's current state without re-deriving it by hand.
