# Text Modality

Text sources of Rice MMKG and the module that holds their wording.

## Licence

| File | Licence | Why |
|---|---|---|
| `RiceMMKG_IRRI_text.ttl` | **CC BY-NC-SA 3.0** | Wording of IRRI Rice Knowledge Bank fact sheets, © International Rice Research Institute. Attribute IRRI; non-commercial use only; share alike. |
| `scripts/` | MIT, like the rest of the tooling | — |
| Pointers in `Ontology/Rice MMKG.rdf` | CC BY 4.0, like the core | Offsets, hashes, titles, section headings and links only; no wording |

The core graph stays CC BY 4.0 because it holds facts and pointers, not the IRRI wording. Anyone who needs only CC BY content can drop `RiceMMKG_IRRI_text.ttl`, and every pointer still resolves to the public page.

## What is in the graph

- **`rice:TextDocument`:** 19 IRRI Rice Knowledge Bank fact sheets, with URL (`dcterms:source`), title and licence.
- **`rice:TextPassage`:** 296 passages, each a paragraph or list item.
  - `inDocument`, `startOffset`, `endOffset` and `textSha256` locate the passage.
  - `sectionTitle` gives its section, and `mentions` the domain individuals named in it.
  - The offsets play the role of a W3C Web Annotation `TextPositionSelector`.
- **Evidence on curated assertions:** `rice:hasEvidencePassage` on the `owl:Axiom` of 77 curated assertions points to the passage that states the assertion. `rice:evidencePassageCheck` says how the link was checked: `human-reviewed` (42) or `LLM-reviewed` (35).
- **This module:** `rice:passageText` for each passage. Load it together with the core to get the wording.

## How the offsets are defined

Offsets count characters in the plain text that `scripts/irri_to_text.py` builds from a saved fact-sheet page:
- title line;
- `## ` headings;
- paragraphs and `- ` list items of the page body (`div.pos-description`).

Pages were saved on 2026-10-20. `textSha256` lets you check that a re-derived passage is the same text. If IRRI changes a page, the hash shows it.

## Rebuild

```bash
python -I "Text Modality/scripts/irri_to_text.py" <saved html folder> <corpus folder>
python -I "Text Modality/scripts/passages.py" <data folder>   # corpus/ + manifest.json + entities.json -> passages.jsonl
python -I "Text Modality/scripts/build_text_module.py" <passages.jsonl> "Text Modality/RiceMMKG_IRRI_text.ttl"
```

The saved pages are kept outside the repository (`Data/irri-rkb/raw_2026-10-20/`, gitignored), because they are IRRI content.

## How the evidence links were made

The method and its evaluation are in the text pilot (2026-10-20 to 2026-10-22):

1. **Rank** the passages of the cited fact sheet against a verbalised assertion with bge-m3.
2. **Verify** with qwen2.5:32b:
   - few-shot examples taken from topics outside the corpus;
   - the quote must occur in the passage.
3. **Review:** keep only links judged correct, against a review of all 88 assertions. A human checked 62 of them, including all supported ones; human and LLM agreed on 60 of 62.

On the reviewed set the verifier reached recall 0.93 and precision 0.94.

**Comparison with forward extraction.** The CropKG pipeline (Wu et al. 2026) with the Rice MMKG schema recovered only 2 of 86 curated assertions. The fact sheets state plant parts at the disease level, while the graph models them per symptom; `hasAffectedPart` (2026-10-21) bridges the two levels.
