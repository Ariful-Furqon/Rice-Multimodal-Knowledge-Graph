# w3id.org/rice-mmkg — DRAFT registration package (Task C.2)

**Not submitted.** This is prepared material for a future PR to
[github.com/perma-id/w3id.org](https://github.com/perma-id/w3id.org),
withheld per the worklog's Checkpoint C1: *"Do not run the rewrite until
the registration is confirmed."*

## What's decided vs. not (Checkpoint C1)

| | Status |
|---|---|
| Path segment `rice-mmkg` | **Proposed, not confirmed.** Matches the GitHub repo name; free to pick something else (e.g. `riceMMKG`, `rice-multimodal-kg`) as long as it's still free on w3id.org. |
| Hosting URL (`PLACEHOLDER-HOST` in `.htaccess`) | **Not decided.** Needs a stable place to serve the actual files the redirects point to — GitHub Pages off this repo is the natural choice (free, already has the ontology under version control) but requires enabling Pages and picking a serialisation-conversion step (RDF/XML is already the native format; Turtle/N-Triples/JSON-LD would need generating via `rdflib`, e.g. `g.serialize(format="turtle")`, as a small addition to the release process). |
| New base IRI to migrate to | **Not decided**, follows directly from the above two: `https://w3id.org/rice-mmkg#` (or `/rice-mmkg/` for a slash-based scheme) once confirmed. |

## What happens once C1 is confirmed

1. Fill in `PLACEHOLDER-HOST` and the path segment in `.htaccess` (this
   directory) to match the confirmed decision.
2. Fork `perma-id/w3id.org`, add this directory as
   `w3id.org/<path-segment>/`, open a PR per their contribution guide.
3. Once the PR is merged and the redirect resolves, run
   `scripts/rewrite_namespace.py <old-base-iri> <new-base-iri>
   Rice_MMKG_v0.5.rdf Rice_MMKG_v0.6.rdf` to rewrite every subject,
   predicate, and object in the local namespace — including inside all
   265+ `owl:Axiom` provenance records, which reference local IRIs via
   `owl:annotatedSource`/`owl:annotatedTarget`.
4. Re-run `scripts/verify.py` on the rewritten file: triple count and
   every other figure must be identical to the pre-rewrite file, only
   the namespace changes.
5. Re-run FOOPS! (`PURL1` check) to confirm it now passes and to get the
   "after" score for the Task C.1 before/after comparison.

## Files in this directory

- `.htaccess` — draft Apache redirect/content-negotiation config,
  adapted from the official w3id.org example template.
