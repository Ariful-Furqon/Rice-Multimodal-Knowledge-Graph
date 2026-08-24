# Task 4.1 — w3id.org permanent identifier (Checkpoint C4)

**Not registered. Base IRI not rewritten** — per the worklog, don't rewrite
until registration is confirmed.

w3id.org registration is a pull request against
[perma-id/w3id.org](https://github.com/perma-id/w3id.org) adding a
`.htaccess` redirect config under a directory named after the chosen path
segment.

## What's needed from you

A **path segment** — the string after `w3id.org/` that identifies this
ontology, e.g. `w3id.org/riceMMKG`. This becomes part of a permanent,
public identifier — pick carefully, it's meant to never change once
registered.

Also confirm the redirect target: a specific GitHub raw URL / GitHub Pages
URL for the RDF file, or a landing page that links to it. Most OWL
ontologies redirect content-negotiated (HTML for browsers, RDF/XML for
`Accept: application/rdf+xml`).

Same open question as before — not re-decided here.
