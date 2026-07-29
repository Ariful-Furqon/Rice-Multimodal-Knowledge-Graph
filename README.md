# Rice MMKG — Rice Multimodal Knowledge Graph

An OWL ontology and knowledge graph modeling rice diseases, pests, pathogens, symptoms, environmental factors, growth stages, treatments, and management actions — populated from multimodal observations such as images, sensor readings, and field/farmer reports.

![Rice MMKG diagram](RiceMMKG.png)

## Overview

Rice MMKG links agronomic and entomological knowledge about rice cultivation into a single queryable graph, connecting what is *observed* (symptoms, sensor readings, images) to its *cause* (pathogens, pests, environmental stressors) and the *response* (treatments, management actions), scoped by growth stage and severity.

- **Namespace:** `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#`
- **Format:** OWL/XML (`.rdf`), editable in [Protégé](https://protege.stanford.edu/)
- **Version:** 2.0 — extended with domain/range axioms, inverse properties, and denser individual relations

## Ontology structure

### Classes (11)

| Class | Description |
|---|---|
| `Disease` | Rice diseases, e.g. Bacterial Leaf Blight, Rice Blast, Brown Spot, Sheath Blight |
| `Pest` | Insect pests, e.g. Brown Planthopper, Stem Borer, Leaf Folder, Armyworm, Rice Bug |
| `Pathogen` | Causal organisms, e.g. Magnaporthe Oryzae, Xanthomonas Oryzae, Bipolaris Oryzae |
| `Plant` | The crop (Rice) |
| `Symptom` | Observable signs, e.g. Leaf Spot, Leaf Rolling, Deadheart, Hopper Burn |
| `EnvironmentalFactor` | Conditions, e.g. High Humidity, High Temperature, Low Rainfall, Excessive Nitrogen |
| `GrowthStage` | Crop stages, e.g. Seedling, Vegetative, Flowering, Maturity, Harvest |
| `SeverityLevel` | Low, Medium, High, Critical |
| `Treatment` | Interventions, e.g. Fungicide/Insecticide Application, Biological Control, Resistant Variety |
| `ManagementAction` | Recommended actions, e.g. Field Inspection, Monitoring, Immediate Intervention |
| `Observation` | Multimodal evidence sources, e.g. Leaf Image, Sensor Reading, Field/Farmer/Disease Report |

### Object properties (22)

Relations connect the classes above, each with a defined inverse:

`causes`/`causedBy`, `threatens`, `indicates`/`indicatedBy`, `controls`/`controlledBy`, `prevents`/`preventedBy`, `recommends`/`recommendedFor`, `requires`/`requiredFor`, `captures`/`capturedBy`, `detects`/`detectedBy`, `occursIn`, `hasOccurrenceOf`, `increaseRiskOf`/`riskIncreasedBy`, `vulnerableTo`

### Data properties (8)

`confidenceScore`, `severityScore`, `interventionThreshold`, `observationDate`, `temperatureValue`, `humidityValue`, `rainfallValue`, `soilMoistureValue`

### Individuals

54 named individuals populate the schema across diseases, pests, pathogens, symptoms, environmental factors, treatments, and observations. Relations for `captures`, `detects`, `increaseRiskOf`, `occursIn`, `requires`, and `vulnerableTo` are illustrative examples based on general rice agronomy/entomology knowledge and should be verified against domain literature before being used for reasoning or publication.

## Repository contents

```
Ontology/
  Rice MMKG.rdf          # the ontology (OWL/XML)
  Rice MMKG.properties    # Protégé project settings
RiceMMKG.png / .jpg       # ontology diagram
```

## Usage

Open `Ontology/Rice MMKG.rdf` in [Protégé](https://protege.stanford.edu/) to browse, edit, or reason over the ontology, or load it with any RDF/OWL library (e.g. `rdflib`, Apache Jena, OWL API) for programmatic querying.

```python
from rdflib import Graph

g = Graph()
g.parse("Ontology/Rice MMKG.rdf", format="xml")
print(f"{len(g)} triples loaded")
```
