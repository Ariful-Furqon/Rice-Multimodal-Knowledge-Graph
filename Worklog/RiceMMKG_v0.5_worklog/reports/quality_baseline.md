# Quality baseline — OOPS! and FOOPS! (Task C.1)

Both tools were run 2026-08-22 against **Rice_MMKG_v0.5_schema_only.rdf**
— the schema plus the 92 domain individuals, with the 10,407
`rice:ImageObservation` instances stripped out
(`scripts/extract_schema_for_scan.py`). Both tools evaluate ontology
*modelling* pitfalls and metadata, not instance-data volume, and the
full 7.3 MB file with all image instances is impractical to submit as a
raw POST body; the 329 KB schema-only extract is the meaningful and
practical scan target. Raw outputs: `baseline_oops.json` /
`baseline_oops.xml` (native RDF/XML response) and `baseline_foops.json`.

This is a v0.5 baseline only — the "before" half of the before/after
comparison the worklog calls for. The "after" run happens once Task C.2
(persistent identifier) is done, since several FOOPS checks below are
about exactly that.

## OOPS! — 2 pitfalls found, both Minor

| Code | Pitfall | Importance | Affected elements |
|---|---|---|---|
| P04 | Creating unconnected ontology elements | Minor | 1 (`dcat:Dataset`) |
| P08 | Missing annotations | Minor | 28 (mostly object properties: `causes`, `vulnerableTo`, `occursIn`, `controlledBy`, `transmits`/`transmittedBy` added in Task B.1, etc. — missing `rdfs:comment` even though they have `rdfs:label`) |

No IMPORTANT or CRITICAL pitfalls. Disposition:

- **P04 (`dcat:Dataset` unconnected)**: fix later. `PaddyDoctorDataset`
  is linked from every `ImageObservation` via `wasDerivedFrom`, so it
  isn't actually isolated in the full graph — OOPS! only sees this in
  the schema-only extract because the 10,407 individuals that connect it
  were stripped out for this scan. Re-check against the full file once
  Task C.2's PURL migration makes a full-graph scan practical to host.
- **P08 (missing `rdfs:comment` on 28 properties)**: fix later, cheap.
  Every affected element already has an `rdfs:label`; adding one
  sentence of `rdfs:comment` to each of the ~14 object properties (the
  inverse-pair duplicates roughly halve the real count) is a half-day
  task, not a modelling decision — good candidate for the first thing
  done in the weeks-3–4 formalisation block.

## FOOPS! — overall score 0.7275 (comparable metric to gUFO's 92%)

15 checks across the four FAIR dimensions, `ok`/`error` per check
(`error` here means "did not pass", not a tool malfunction):

| Category | Check | Result | Title |
|---|---|---|---|
| Findable | PURL1 | 0/1 | Ontology has a persistent URL |
| Findable | OM1 | 5/6 | Minimum metadata is declared |
| Findable | FIND1 | 1/1 | Ontology prefix is declared |
| Findable | VER1 | 2/2 | A version IRI is declared |
| Interoperable | RDF1 | 1/1 | Available in RDF (RDF/XML) |
| Interoperable | VOC1 | 1/1 | Reuses existing vocabularies for metadata annotations |
| Interoperable | VOC2 | 1/1 | Imports/reuses well-established vocabularies |
| Reusable | OM2 | 2/4 | Recommended metadata declared |
| Reusable | OM3 | 1/6 | Detailed metadata declared |
| Reusable | OM4_1 | 1/1 | License available |
| Reusable | OM4_2 | 1/1 | License resolvable |
| Reusable | OM5_1 | 1/2 | Basic provenance metadata declared |
| Reusable | OM5_2 | 1/2 | Detailed provenance metadata declared |
| Reusable | VOC3 | 46/46 | All terms have labels |
| Reusable | VOC4 | 19/46 | All terms have definitions |

Disposition:

- **PURL1 (0/1) — fix now, this is Task C.2.** The `semanticweb.org`
  namespace doesn't match any known persistent-identifier scheme
  (w3id.org, purl.org, DOI, W3C, perma.cc...). This single check is
  almost certainly the largest lever on the overall score — it also
  gates OM3's detailed-metadata check in practice, since several of
  those sub-tests dereference the ontology URI.
- **OM1 (5/6), OM2 (2/4), OM3 (1/6) — fix later, availability block
  (week 5).** Metadata-completeness gaps (likely missing
  `dcterms:created`, `dcterms:modified`-style fields, contributor
  metadata, etc.) — needs the actual failing sub-tests inspected
  (`GET /assess/test/OM1` etc. would list them) before writing more
  metadata, so as not to guess at what's missing.
- **OM5_1/OM5_2 (1/2 each) — accept partially, note in the paper.**
  Rice MMKG's provenance strength is at the *assertion* level
  (`owl:Axiom` + `dcterms:source`/`bibliographicCitation` on all 265
  domain relations, not something FOOPS checks for) rather than the
  *ontology-metadata* level FOOPS is checking here (e.g.
  `prov:wasGeneratedBy` on the ontology document itself). Worth adding
  the missing ontology-level provenance annotations, but also worth
  stating explicitly in the paper that the resource's real provenance
  contribution is per-assertion, which no comparator does and this
  metric doesn't capture at all.
- **VOC4 (19/46) — fix later, cheap, same fix as OOPS! P08.** 27 terms
  have a label but no `rdfs:comment`/definition. Doing the P08 fix above
  will move this number too.
- **RDF1, VOC1, VOC2, VOC3, FIND1, VER1, OM4_1, OM4_2 — already passing.**
  No action needed on the license, prefix, versioning, vocabulary-reuse,
  or full-label-coverage checks.

## Comparator note

gUFO reports a 92% FOOPS score, with the residual gap attributed to a
single metadata-property choice — a much smaller category of gap than
Rice MMKG's current 72.75%, most of which is one structural blocker
(PURL1) plus a cluster of metadata-completeness items. Closing PURL1
alone (Task C.2) should move the score meaningfully; re-run after that
and report both numbers together, as planned.
