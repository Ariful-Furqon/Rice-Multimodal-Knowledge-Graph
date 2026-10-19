# SOSA Alignment Register

## Purpose and scope

This register records semantic links between the **observation layer** of
Rice MMKG and **SOSA** (Sensor, Observation, Sample, and Actuator; W3C
Recommendation, 2017), plus one term of the W3C Basic Geo (WGS84) vocabulary.
It is kept separate from
[`AGROVOC_alignment.md`](AGROVOC_alignment.md),
[`NCBI_Taxonomy_alignment.md`](NCBI_Taxonomy_alignment.md) and
[`Planteome_alignment.md`](Planteome_alignment.md) for the same reason as
those: each source has its own method and provenance.

The other registers align domain individuals (diseases, pathogens, plant
parts). This one aligns schema terms: classes and properties of the
observation layer, which had four links before this round
(`Observation`, `FieldLocation`, `recordedAtDate`, `hasLatitude`/`hasLongitude`).

**Sources read:** `https://www.w3.org/ns/sosa/` (Turtle) and
`http://www.w3.org/2003/01/geo/wgs84_pos` (RDF/XML), fetched 2026-10-19; every
target term below was found declared in them.  
**Applied:** 2026-10-19 by
`Worklog/2026-10-19_sosa_alignment/scripts/align_sosa.py`; pre-edit file
`Ontology/Backup/Rice MMKG.backup-0.7.0-dev-pre-sosa-alignment.rdf`.

## Method and decision rule

SKOS mapping properties only. SOSA is **not imported**, and no
`rdfs:subClassOf` or `rdfs:subPropertyOf` to a SOSA term is asserted, so the
reasoner inherits none of SOSA's axioms and the OWL RL closure does not change.

- `closeMatch`: same role, usable interchangeably in most applications.
- `broadMatch`: the SOSA term is more general; the Rice MMKG term is one kind of it.
- Local only: no SOSA term plays the same role; the reason is recorded.

**The structural difference.** SOSA describes one observed property per
observation: `sosa:observedProperty` names the quantity (soil pH) and
`sosa:hasSimpleResult` holds the value (6.2). Rice MMKG puts several values on
one observation, each in its own property (`hasSoilPH`, `hasTemperature`, …),
so the quantity is implied by the property name. Such a property is therefore
a `broadMatch` of `sosa:hasSimpleResult`, never an exact one.

## Links (round 1, 2026-10-19)

### Classes

| Rice MMKG | Relation | Target | Reason |
|---|---|---|---|
| `ImageObservation` | `broadMatch` | `sosa:Observation` | A photograph whose label is the result of an act of observation |
| `SensorObservation` | `broadMatch` | `sosa:Observation` | Soil and weather values measured at a plot |
| `TrapObservation` | `broadMatch` | `sosa:Observation` | A catch counted over a window at a fixed point |
| `RemoteSensingObservation` | `broadMatch` | `sosa:Observation` | A capture by an optical sensor without touching the crop |
| `BandImage` | `broadMatch` | `sosa:Result` | One file holding one band: a part of the result of a capture |

### Properties

| Rice MMKG | Relation | Target | Reason |
|---|---|---|---|
| `hasSpatialLocation` | `closeMatch` | `geo:location` | WGS84 "where it is"; the range, `FieldLocation`, is already `closeMatch geo:Point` |
| `hasBandImage` | `broadMatch` | `sosa:hasResult` | Links an observation to (part of) its result |
| `hasCatchCount` | `broadMatch` | `sosa:hasSimpleResult` | Result value; quantity: individuals caught |
| `hasNDVI` | `broadMatch` | `sosa:hasSimpleResult` | Result value; quantity: NDVI (declared, not yet used) |
| `hasSoilPH`, `hasElectricalConductivity`, `hasOrganicCarbon`, `hasNitrogenLevel`, `hasPhosphorusLevel`, `hasPotassiumLevel`, `hasTemperature`, `hasHumidity`, `hasRainfall` | `broadMatch` | `sosa:hasSimpleResult` | Result values; the quantity is in the property name |

18 triples in all (1 `closeMatch`, 17 `broadMatch`).

### Existing link reviewed: `recordedAtDate` closeMatch `sosa:resultTime`

Kept, with its comment extended. SOSA separates the time a phenomenon took
place (`sosa:phenomenonTime`) from the time its result became available
(`sosa:resultTime`). For an instantaneous capture (an image, a multispectral
shot) they coincide, and the mapping holds. For a trap catch over a window,
`recordedAtDate` is the start of the window, which SOSA would model as part of
the phenomenon time, with the end of the window as result time. Decided
2026-10-19 to keep `closeMatch` rather than weaken it to `relatedMatch`,
because most observations in the graph are instantaneous; the caveat is in the
property comment.

## Left local, with the reason

| Rice MMKG | Reason |
|---|---|
| `annotatedAs`, `captures`, `detects` | SOSA splits what is observed into a feature of interest (a plot, a population) and an observable property. These three properties merge both, so any SOSA link would mislead. |
| `SpectralBand`, `ofBand`, `centreWavelengthNm` | SOSA has no notion of a spectral band. A band is a capability of the sensor, the domain of the SSN System module, which is too heavy to adopt for one concept. |
| `recordedUntilDate` | End of a window; SOSA expresses windows through `phenomenonTime` with OWL-Time intervals, an object structure with no datatype counterpart. |
| `plantAgeDays`, `environmentCondition`, `sourceLabel`, `ofVariety` | Metadata of the source or of the sampled plant; no SOSA counterpart. |
| `SymptomaticObservation` | Defined class over `captures`; no counterpart. |

## Not done in this round

- No `sosa:Sensor` individuals (camera, light trap, soil sensor) and no
  `sosa:madeBySensor` links: the datasets name their instruments only in prose.
- No `sosa:FeatureOfInterest` or `sosa:ObservableProperty` individuals. Adding
  them would restructure the observation layer, not align it.

## Effect

| | Before | After |
|---|---:|---:|
| Classes with an external link | 4 / 28 | 9 / 28 |
| Properties with an external link | 4 / 68 | 17 / 68 |
| `skos:closeMatch` | 28 | 29 |
| `skos:broadMatch` | 1 | 18 |
