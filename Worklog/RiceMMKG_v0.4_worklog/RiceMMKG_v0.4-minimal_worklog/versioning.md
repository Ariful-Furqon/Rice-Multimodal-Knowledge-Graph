# Task 4.2 — version numbering (Checkpoint C5)

`owl:versionInfo` and `owl:versionIRI` currently read `0.3` — carried over
from the pre-existing decision (this ontology has never been publicly
released, so the pre-existing 0.x scheme from early Protégé edits was
continued rather than jumping to a 2.x number inherited from an informal
README label).

This worklog's framing ("both read 0.3, down from 2.2") describes an
earlier point in the history and is stale now — that question was already
settled. What's actually open is only the **next** number, now that this
round produces a distinct artefact (the minimal schema) from the one that
was briefly live as v0.4-expanded.

## Options

**A — `0.4` (recommended, continues the 0.x pre-release track).** Simple
increment consistent with the versioning already committed.

**B — Something else** — e.g. if you want to distinguish this minimal
schema from the abandoned expanded one with a different marker (`0.4-min`,
etc.), or reset numbering for another reason. State what, and why.

**Not implemented pending your answer.** `owl:versionInfo`/`owl:versionIRI`
in `Rice_MMKG_v0.4.rdf` still read `0.3`.
