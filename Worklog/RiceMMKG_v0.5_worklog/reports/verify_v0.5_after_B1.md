# Verification report — v0.5-after-B1

## Baseline figures

- Total triples: 66873
- Named classes: 16
- Object properties: 26
- Datatype properties: 5
- Annotation properties: 14
- Individuals: 10498
- ImageObservation individuals: 10407
- Domain individuals: 91
- owl:Axiom provenance records: 265
- Domain-level assertions: 265
    - causes: 8
    - controlledBy: 42
    - increaseRiskOf: 29
    - indicatedBy: 42
    - occursIn: 47
    - preventedBy: 8
    - recommends: 23
    - requires: 5
    - transmits: 2
    - vulnerableTo: 59
- skos:exactMatch / closeMatch / broadMatch / narrowMatch: 33 / 17 / 1 / 0
- eppoCode assertions: 15
- Individuals typed only NamedIndividual: 0
- TODO literals: 0

## Provenance coverage

- Coverage: 265/265
- Assertions missing provenance: 0
- Assertions with duplicate provenance records: 0
- Orphan owl:Axiom records (base triple not asserted): 0

## Duplicate identifiers

- Duplicate eppoCode values: 0
- Alignment IRIs used by more than one individual: 3
    - http://aims.fao.org/aos/agrovoc/c_4911: Monitoring (exactMatch), Field_Inspection (closeMatch)
    - http://aims.fao.org/aos/agrovoc/c_7773: Tillering_Stage (closeMatch), Reduced_Tillering (closeMatch), Excessive_Tillering (closeMatch)
    - http://aims.fao.org/aos/agrovoc/c_27879: Fungicide_Application (closeMatch), Insecticide_Application (closeMatch)

## Range conformance

- Violations: 11
    - High_Humidity increaseRiskOf Deadheart — types ['NamedIndividual', 'Symptom'] not in range
    - Dense_Canopy increaseRiskOf Deadheart — types ['NamedIndividual', 'Symptom'] not in range
    - High_Temperature increaseRiskOf Deadheart — types ['NamedIndividual', 'Symptom'] not in range
    - Rice vulnerableTo Sclerophthora_Macrospora — types ['NamedIndividual', 'Pathogen'] not in range
    - Rice vulnerableTo Burkholderia_Glumae — types ['NamedIndividual', 'Pathogen'] not in range
    - Rice vulnerableTo Deadheart — types ['NamedIndividual', 'Symptom'] not in range
    - Vegetative_Stage vulnerableTo Deadheart — types ['NamedIndividual', 'Symptom'] not in range
    - Tillering_Stage vulnerableTo Deadheart — types ['NamedIndividual', 'Symptom'] not in range
    - Reproductive_Stage vulnerableTo Deadheart — types ['NamedIndividual', 'Symptom'] not in range
    - Rice vulnerableTo Rice_Tungro_Bacilliform_Virus — types ['NamedIndividual', 'Pathogen'] not in range
    - Rice vulnerableTo Xanthomonas_Oryzicola — types ['NamedIndividual', 'Pathogen'] not in range
