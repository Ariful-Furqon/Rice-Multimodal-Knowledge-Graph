# Deferred design — classes and properties not built this round

None of these are implemented. Each is justified by a use case the
artefact does not yet have data for. This is the roadmap: introduce them
deliberately when the trigger condition below is met, not preemptively.

| Deferred | Introduce when | Cost at that point |
|---|---|---|
| `TextualReport`, `SensorObservation` | first text or sensor data is ingested | Low — classes are additive; `LeafImage` is untouched by their arrival. |
| `ObservationEvent` | first submission carries two media (e.g. a report with an attached photo) | Low — one new class, `hasPart`/`partOf` properties, no retargeting of existing data. |
| `Location` | sensor data needs to be matched to submissions by place | Low. Kabupaten/kota granularity is the likely fit (matches existing NASA POWER coverage), pending confirmation when the need arises. |
| `Agent` | observations start coming from more than one source type (farmer vs. extension officer vs. device) | Low — additive, no retargeting. |
| `AnnotationLabel`, `Dataset` | a second dataset with a different label vocabulary needs to be ingested | **High — retargets all 10,407 `annotatedAs` assertions** from domain entities to label individuals, plus moves `sourceDatasetLabel` off every image. This is the single most expensive deferred item, and it gets *more* expensive with every image added in the meantime. Its absence today is exactly why `annotatedAs` currently carries a range union of four unrelated classes (`Disease ⊔ HealthStatus ⊔ Pest ⊔ Symptom`) — that union is an honest description of what the Paddy Doctor label set actually mixes, not a defect, but it's also the seam where `AnnotationLabel` would eventually cut. |
| `Infestation` | pest damage needs to be modelled separately from the pest organism (e.g. once vector–pathogen relations or damage-specific treatment data arrive) | Medium — retargets ~43 assertions (`indicatedBy`, `increaseRiskOf`, `vulnerableTo`, `occursIn`, `controlledBy`, `recommends` currently pointing at `Pest` individuals) plus adds 6 new individuals and `causes` assertions. |

## Why this list, not a bigger one

An earlier round (see `Worklog/RiceMMKG_v0.4_worklog/`, now superseded)
built all seven of these plus `Infestation`'s retargeting in one pass. That
version is functionally correct but outran what the data supports — most
of the new classes were empty on arrival, and the `Infestation` retargeting
was itself an undocumented consequence of the range-narrowing rather than
something the worklog planned for. This list exists so the same expansion
can happen again, but staged, with each step's cost paid once and only when
there's data to justify it.
