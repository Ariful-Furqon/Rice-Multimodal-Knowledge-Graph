# Verification report — v0.5-after-A

## Baseline figures

- Total triples: 66854
- Named classes: 16
- Object properties: 24
- Datatype properties: 5
- Annotation properties: 14
- Individuals: 10498
- ImageObservation individuals: 10407
- Domain individuals: 91
- owl:Axiom provenance records: 264
- Domain-level assertions: 264
    - causes: 9
    - controlledBy: 42
    - increaseRiskOf: 29
    - indicatedBy: 42
    - occursIn: 47
    - preventedBy: 8
    - recommends: 23
    - requires: 5
    - vulnerableTo: 59
- skos:exactMatch / closeMatch / broadMatch / narrowMatch: 33 / 17 / 1 / 0
- eppoCode assertions: 15
- Individuals typed only NamedIndividual: 0
- TODO literals: 0

## Provenance coverage

- Coverage: 264/264
- Assertions missing provenance: 0
- Assertions with duplicate provenance records: 0
- Orphan owl:Axiom records (base triple not asserted): 0

## Duplicate identifiers

- Duplicate eppoCode values: 0
- Alignment IRIs used by more than one individual: 3
    - http://aims.fao.org/aos/agrovoc/c_4911: Monitoring (exactMatch), Field_Inspection (closeMatch)
    - http://aims.fao.org/aos/agrovoc/c_7773: Tillering_Stage (closeMatch), Excessive_Tillering (closeMatch), Reduced_Tillering (closeMatch)
    - http://aims.fao.org/aos/agrovoc/c_27879: Fungicide_Application (closeMatch), Insecticide_Application (closeMatch)

## Range conformance

- Violations: 11
    - Tillering_Stage vulnerableTo Deadheart — types ['Symptom', 'NamedIndividual'] not in range
    - Rice vulnerableTo Deadheart — types ['Symptom', 'NamedIndividual'] not in range
    - Vegetative_Stage vulnerableTo Deadheart — types ['Symptom', 'NamedIndividual'] not in range
    - Reproductive_Stage vulnerableTo Deadheart — types ['Symptom', 'NamedIndividual'] not in range
    - Rice vulnerableTo Sclerophthora_Macrospora — types ['Pathogen', 'NamedIndividual'] not in range
    - Rice vulnerableTo Burkholderia_Glumae — types ['Pathogen', 'NamedIndividual'] not in range
    - Rice vulnerableTo Rice_Tungro_Bacilliform_Virus — types ['Pathogen', 'NamedIndividual'] not in range
    - Rice vulnerableTo Xanthomonas_Oryzicola — types ['Pathogen', 'NamedIndividual'] not in range
    - High_Humidity increaseRiskOf Deadheart — types ['Symptom', 'NamedIndividual'] not in range
    - High_Temperature increaseRiskOf Deadheart — types ['Symptom', 'NamedIndividual'] not in range
    - Dense_Canopy increaseRiskOf Deadheart — types ['Symptom', 'NamedIndividual'] not in range
