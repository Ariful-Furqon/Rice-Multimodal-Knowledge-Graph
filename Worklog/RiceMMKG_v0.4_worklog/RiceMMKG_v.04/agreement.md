# Task 4.1 — agreement study

## Result, as measured

| | |
|---|---|
| `StemBorerCandidate` members (inference path) | 1,442 |
| Images `annotatedAs` the `dead_heart` label (annotation path) | 1,442 |
| Set equality | **exact — the two sets are identical** |
| Precision / Recall (inference vs. annotation, over N=1,442) | 1.0 / 1.0 |

## This is not the validation result it looks like

The two paths agree perfectly, but **not because the reasoning chain was
independently verified against the annotations — it's because Task 2.3
built the evidence path directly from the annotation labels.** The 1,442
`captures Deadheart` triples were asserted *for exactly the images already
`annotatedAs` the `dead_heart` label* (worklog Task 2.3: "For every image
individual whose `annotatedAs` label denotes a `Symptom`, add `captures` to
that symptom" — the only `Symptom`-denoting label is `dead_heart`). So:

- Inference path: image → `captures` → `Deadheart` → `indicates` → `Stem_Borer_Damage`
- Annotation path: image → `annotatedAs` → `label_dead_heart` → `denotes` → `Deadheart`

Both paths pass through the same `Deadheart` node, and the first edge of
the inference path was constructed *from* the second edge of the annotation
path. There was never an independent image-level judgement that could have
disagreed. A perfect score here demonstrates the axioms are wired
correctly, not that the `captures → indicates` reasoning chain reliably
recovers ground truth from evidence collected independently of the label.

**A real test of the inference chain requires evidence that wasn't derived
from the label being tested against** — i.e. genuine symptom annotation
across images whose `captures` assertions come from looking at the image,
not from copying the Paddy Doctor class folder. That is exactly Checkpoint
C5 (broadening symptom annotation beyond `Deadheart`) and the 250-image
stratified sample already prepared in the v0.3 round
(`Analysis and Alignment/RiceMMKG_v2.3_worklog/annotation_sample.csv`) but
never filled in by a human annotator. Until that happens, this evaluation
cell has no meaningful number to report beyond the tautology above.

## What would make this a real evaluation

1. A human (or independently-sourced) annotator labels the `captures`
   relation for a sample of images *without* looking at the Paddy Doctor
   class folder name.
2. Compare the reasoner-inferred condition (via `indicates`) against the
   dataset's `annotatedAs`/`denotes` ground truth for that same sample.
3. Report precision/recall as measured — including if it's low, which
   per the worklog's own framing is "a valid and publishable result":
   `indicates` is defeasible domain knowledge, and one symptom mapping to
   several conditions is expected behaviour, not a bug.

## Not done

No reasoner ran (no Java in this environment — see
`reports/task_2_4_reasoner_blocked.md`); the numbers above were computed by
direct graph query, which is exact for this narrow, single-symptom case but
is not a general substitute for DL classification.
