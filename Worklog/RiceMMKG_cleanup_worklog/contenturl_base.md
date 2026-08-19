# Task A.4 — contentUrl base URL (Checkpoint C2)

`schema:contentUrl` currently holds relative paths, e.g.
`Data/PaddyDoctor/brown_spot/100890.jpg`. These can't be dereferenced by a
reviewer — there is no base to resolve them against. Not fixed here; three
options, not decided:

**A — Rewrite against a Zenodo deposit DOI once minted.** E.g.
`https://zenodo.org/record/<id>/files/PaddyDoctor/brown_spot/100890.jpg`.
Correct long-term answer if the images themselves get deposited alongside
the ontology, but blocked until a deposit exists (also gated behind the
w3id/versioning decisions tracked separately, out of scope here).

**B — Rewrite against the upstream Paddy Doctor distribution.** The
dataset is public (Kaggle/other mirror) — if a stable per-file URL scheme
exists there, point at it directly. Avoids depositing 10,407 images
ourselves, but ties `contentUrl`'s resolvability to a third party's
hosting choices and file layout, and needs that URL scheme confirmed
before use (the current filenames were derived from local folder
structure, not verified against the upstream distribution's own path
convention).

**C — Keep relative paths, but stop promising dereferenceability.** Move
the value to a differently-named local property (e.g. `rice:imagePath`)
that doesn't carry `schema:contentUrl`'s implication of a resolvable URL,
and document the base path assumption in the ontology's
`dcterms:description`. Cheapest, but the artefact's images stay
unreachable from outside this repository.

**Not implemented pending your answer.** `scripts/rewrite_contenturl.py`
is written and tested against a two-row fixture, but was not run against
the full ontology — the base URL argument it needs doesn't exist yet.
