# Task 3.2 — version numbering (Checkpoint C2)

`owl:versionInfo` and `owl:versionIRI` currently read `0.3` (set deliberately
in the previous session, per your explicit decision — the ontology "belum
pernah rilis" / has never been publicly released, so the pre-existing 0.x
scheme from early Protégé edits was continued rather than jumping to a 2.x
number inherited from an informal README version label).

This v0.4 worklog was written assuming a different history — it says
"`owl:versionInfo` and `owl:versionIRI` both read `0.3`, down from `2.2`"
and frames the choice as still open. That framing is now stale: the 0.3→2.2
question was already resolved in the prior session. What's actually open for
this round is only the **next** number.

## Options

**A — Continue the 0.x pre-release track (recommended, consistent with the
prior decision).** This becomes `0.4`. Signals pre-1.0 / not-yet-stable to
anyone consuming the ontology, and matches the versioning already committed
for v0.3.

**B — Something else.** State what, and why — e.g. if this migration is
judged substantial enough to be a first "real" release (`1.0`), or if a
different scheme (date-based, etc.) is preferred.

**Not implemented pending your answer.** `owl:versionInfo` /
`owl:versionIRI` in `Rice_MMKG_v0.4.rdf` still read `0.3` — the version bump
itself is one line each and will be applied once you pick.
