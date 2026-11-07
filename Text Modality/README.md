# Text Modality

Text sources of Rice MMKG and the modules that hold their wording.

## Licence

| File | Licence | Why |
|---|---|---|
| `RiceMMKG_IRRI_text.ttl` | **CC BY-NC-SA 3.0** | Wording of IRRI Rice Knowledge Bank fact sheets, © International Rice Research Institute. Attribute IRRI; non-commercial use only; share alike. |
| `RiceMMKG_IRRI_RD2018_text.ttl` | **CC BY-NC-SA 4.0** | Wording of IRRI (2018) *Rice Diseases: Biology and Selected Management Practices*, © International Rice Research Institute. Attribute IRRI; non-commercial use only; share alike. |
| `scripts/` | MIT, like the rest of the tooling | — |
| Pointers in `Ontology/Rice MMKG.rdf` | CC BY 4.0, like the core | Offsets, hashes, titles, section headings and links only; no wording |

The core graph stays CC BY 4.0 because it holds facts and pointers, not the IRRI wording. Anyone who needs only CC BY content can drop the two modules, and every pointer still resolves to the public source.

## What is in the graph

- **`rice:TextDocument`:** 22 documents, each with URL (`dcterms:source`), title and licence:
  - 19 IRRI Rice Knowledge Bank fact sheets (`IRRI_RKB_*`);
  - 3 disease sections of IRRI (2018) *Rice Diseases* (`IRRI_RD2018_*`, added 2026-11-07): downy mildew and leaf scald from chapter 2, grain rot (bacterial panicle blight) from chapter 4. Each covers the introduction and the Symptoms subsection.
- **`rice:TextPassage`:** 311 passages (296 + 15), each a paragraph or list item.
  - `inDocument`, `startOffset`, `endOffset` and `textSha256` locate the passage.
  - `sectionTitle` gives its section, and `mentions` the domain individuals named in it.
  - The offsets play the role of a W3C Web Annotation `TextPositionSelector`.
- **Evidence on curated assertions:** `rice:hasEvidencePassage` on the `owl:Axiom` of 271 curated assertions points to the passage that states the assertion. `rice:evidencePassageCheck` says how the link was checked: `human-reviewed` (234) or `LLM-reviewed` (37). Counted 2026-11-07 on 0.9.0-dev. The count includes:
  - the 49 blast and brown spot assertions of 0.8.0;
  - the 0.8.1 corrections: one wrong link removed and two added (inventory §6.4);
  - the 32 tungro and bacterial leaf blight assertions of 0.9.0-dev;
  - the 38 assertions of the third batch of 0.9.0-dev (six more conditions);
  - the 63 leaf scald, downy mildew and bacterial panicle blight assertions of 0.9.0-dev, linked to `IRRI_RD2018_*` passages;
  - 4 older assertions (`Zonate_Leaf_Lesion` of leaf scald; `Empty_Grain`, `Wilting` and `Grain_Discoloration` of bacterial panicle blight). These got IRRI (2018) as a second source, with its passage.
- **These modules:** `rice:passageText` for each passage. Load them together with the core to get the wording.

## How the offsets are defined

**Rice Knowledge Bank.** Offsets count characters in the plain text that `scripts/irri_to_text.py` builds from a saved fact-sheet page:
- title line;
- `## ` headings;
- paragraphs and `- ` list items of the page body (`div.pos-description`).

Pages were saved on 2026-10-20.

**Rice Diseases (2018).** Offsets count characters in the plain text that `scripts/rd2018_to_text.py` builds from the chapter PDFs. The PDFs are linked from https://rice-diseases.irri.org/contents and were downloaded on 2026-11-07.
- Text is extracted with pypdf 6.19.0.
- Page-number lines are dropped, and words broken across lines are joined.
- A line that starts with a space starts a new paragraph.
- `N.N. <name>` subsections become `## <name>` headings.
- The text before the first subsection gets the heading `## Introduction`. The book has no heading there; it is added so that the first paragraph is not merged into the title line.

In both cases `textSha256` lets you check that a re-derived passage is the same text. If IRRI changes a page or a PDF, the hash shows it.

## Rebuild

```bash
# Rice Knowledge Bank
python -I "Text Modality/scripts/irri_to_text.py" <saved html folder> <corpus folder>
python -I "Text Modality/scripts/passages.py" <data folder>   # corpus/ + manifest.json + entities.json -> passages.jsonl
python -I "Text Modality/scripts/build_text_module.py" <passages.jsonl> "Text Modality/RiceMMKG_IRRI_text.ttl"

# Rice Diseases (2018)
python -I "Text Modality/scripts/rd2018_to_text.py" Data/irri-rice-diseases-2018/raw_2026-11-07 Data/irri-rice-diseases-2018/corpus
python -I "Text Modality/scripts/rd2018_passages.py" Data/irri-rice-diseases-2018 "Ontology/Rice MMKG.rdf" \
    "Text Modality/RiceMMKG_IRRI_RD2018_text.ttl" <core pointer draft .ttl>
```

The saved pages and PDFs are kept outside the repository, because they are IRRI content:
- `Data/irri-rkb/raw_2026-10-20/`;
- `Data/irri-rice-diseases-2018/raw_2026-11-07/`.

Both folders are gitignored.

The second command for the 2018 book writes the core pointers as a Turtle draft. They were merged into `Rice MMKG.rdf` on 2026-11-07. When the script is run on the merged graph, mentions are matched against the current labels, so they can differ from the merged pointers once new symptoms exist.

## How the evidence links were made

The method and its evaluation are in the text pilot (2026-10-20 to 2026-10-22):

1. **Rank** the passages of the cited fact sheet against a verbalised assertion with bge-m3.
2. **Verify** with qwen2.5:32b:
   - few-shot examples taken from topics outside the corpus;
   - the quote must occur in the passage.
3. **Review:** keep only links judged correct, against a review of all 88 assertions. A human checked 62 of them, including all supported ones; human and LLM agreed on 60 of 62.

On the reviewed set the verifier reached recall 0.93 and precision 0.94.

The symptom-inventory links (0.8.0 and 0.9.0-dev) were made differently. Each row of the inventory quotes the passage that states the symptom. A script checks that each quote occurs in its passage, and the curator reviews the draft before it is merged.

**Comparison with forward extraction.** The CropKG pipeline (Wu et al. 2026) with the Rice MMKG schema recovered only 2 of 86 curated assertions. The fact sheets state plant parts at the disease level, while the graph models them per symptom; `hasAffectedPart` (2026-10-21) bridges the two levels.
