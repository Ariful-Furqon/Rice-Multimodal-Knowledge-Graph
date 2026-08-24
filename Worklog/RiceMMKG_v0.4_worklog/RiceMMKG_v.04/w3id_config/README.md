# Task 3.1 — w3id.org permanent identifier (Checkpoint C1)

**Not registered. Base IRI not rewritten.** Per the worklog: don't rewrite
the base IRI until the registration is confirmed.

w3id.org registration is a pull request against
[perma-id/w3id.org](https://github.com/perma-id/w3id.org) adding a
`.htaccess` redirect config under a directory named after the chosen path
segment.

## What's needed from you

A **path segment** — the string after `w3id.org/` that will identify this
ontology, e.g. `w3id.org/riceMMKG` or `w3id.org/rice-mmkg`. This becomes
part of a permanent, public identifier — pick carefully, it's meant to
never change once registered.

Also confirm: should it redirect to a specific GitHub raw URL / GitHub Pages
URL for the RDF file, or to a landing page that then links to the RDF? Most
OWL ontologies redirect content-negotiated: HTML for browsers, RDF/XML for
`Accept: application/rdf+xml`.

## Template (placeholder — do not use as-is)

`w3id_config/.htaccess.template` below assumes path segment `riceMMKG` and
redirect target `https://raw.githubusercontent.com/<owner>/<repo>/main/Ontology/Rice%20MMKG.rdf`
— both are placeholders pending your answer.
