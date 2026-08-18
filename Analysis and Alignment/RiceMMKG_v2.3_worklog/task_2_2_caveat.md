# Task 2.2 caveat — LeafImage left without a `captures` restriction

`rice:LeafImage` was **not** given the restriction
`LeafImage ⊑ ∃captures.Symptom`, even though the deleted `Leaf_Image`
prototype individual asserted `captures` against 9 `Symptom` individuals.

**Why.** That restriction would state that *every* `LeafImage` captures some
symptom. 1,764 of the 10,407 `LeafImage` individuals are annotated
(`rice:annotatedAs`) with `HealthStatus` — i.e. healthy-plant images with no
symptom to capture. Applying the restriction as stated would make the
ontology inconsistent (or force a reasoner to infer a phantom symptom for
every healthy image) the moment a reasoner is run over asserted individuals,
which is precisely the reasoning-chain evaluation planned for Task 2.4.

**Pending decision.** Introduce a `rice:SymptomaticLeafImage` subclass of
`rice:LeafImage` (defined as images annotated with `Disease`, `Pest`, or
`Symptom` — i.e. NOT `HealthStatus`) and attach the `∃captures.Symptom`
restriction to that subclass instead. This is deferred pending confirmation
that it doesn't conflict with the Task 2.4 defined-class design, which will
also need to distinguish symptomatic from healthy images.

The other four restrictions (`SensorReading`, `FieldObservation`,
`DiseaseReport`, `FarmerReport`) were applied as specified — none of them
have a populated-but-exception-bearing individual set like `LeafImage` does.
