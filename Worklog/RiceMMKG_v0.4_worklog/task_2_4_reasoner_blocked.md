# Task 2.4 — reasoner unavailable, membership computed by direct query instead

No Java runtime is installed in this environment, so HermiT/ELK/Pellet
(via owlready2, which *is* installed) cannot run. Two acceptance items are
therefore not verified the way the worklog specifies:

- "reasoner reports no unsatisfiable classes" (also required by Task 1.5) — **not checked**.
- Materialised member counts for `SymptomaticObservation` / `StemBorerCandidate` — computed by a **direct graph query** instead of DL classification, since both defined classes are simple existentials over already-asserted `captures`/`indicates` triples (no additional subsumption reasoning is needed to compute membership correctly — only inverse-property closure, which the query below computes by hand):

```python
symptoms = { Symptom individuals }
SymptomaticObservation members = { x : x captures y, y in symptoms }
# = 1,442

stem_borer_symptoms = { y : y indicates Stem_Borer_Damage OR Stem_Borer_Damage indicatedBy y }
StemBorerCandidate members = { x : x captures y, y in stem_borer_symptoms }
# = 1,442 (same underlying set: Deadheart is the only symptom with instance
#   support, and it indicates Stem_Borer_Damage)
```

Both classes are non-empty and both counts match the 1,442 `Deadheart`
`captures` assertions from Task 2.3 — expected, since `Deadheart` is
currently the only `Symptom` with any `captures` instance data at all.

**Consistency (satisfiability) was not formally checked.** If a reasoner
becomes available later, run it and confirm no unsatisfiable classes before
relying on this ontology for the Task 4.1 agreement study.
