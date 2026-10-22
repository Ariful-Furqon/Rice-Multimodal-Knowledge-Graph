"""Write the IRRI text module: the wording of each passage, keyed by the passage
IRI that the core graph declares (rice:TextPassage with offsets and sha256).

The wording is IRRI Rice Knowledge Bank text under CC BY-NC-SA 3.0, so it lives in
this separate module and never in Rice MMKG.rdf (CC BY 4.0).

    python -I build_text_module.py <passages.jsonl> <out .ttl>
"""
import json
import sys
from pathlib import Path

R = "https://w3id.org/ricemmkg#"
HEADER = """@prefix rice: <https://w3id.org/ricemmkg#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

<https://w3id.org/ricemmkg/text/irri-rkb> a owl:Ontology ;
    dcterms:title "Rice MMKG text module: IRRI Rice Knowledge Bank passages"@en ;
    dcterms:license <https://creativecommons.org/licenses/by-nc-sa/3.0/> ;
    dcterms:rightsHolder "International Rice Research Institute (IRRI)" ;
    dcterms:source <http://www.knowledgebank.irri.org/training/fact-sheets> ;
    dcterms:description "Wording of the rice:TextPassage individuals declared in Rice MMKG.rdf, taken from IRRI Rice Knowledge Bank fact sheets (pages saved 2026-10-20). Licensed CC BY-NC-SA 3.0 like the source: attribute IRRI, non-commercial use only, share alike. Offsets and sha256 in the core graph refer to the plain text produced by Text Modality/scripts/irri_to_text.py."@en .

"""


def lit(s):
    return '"""' + s.replace("\\", "\\\\").replace('"', '\\"') + '"""@en'


def main(passages, out):
    rows = [json.loads(l) for l in Path(passages).read_text(encoding="utf-8").splitlines()]
    body = [f"rice:{pid(r)} rice:passageText {lit(r['text'])} ." for r in rows]
    Path(out).write_text(HEADER + "\n".join(body) + "\n", encoding="utf-8")
    print(f"{len(rows)} passages written to {out}")


def pid(r):
    doc, n = r["id"].split("#p")
    return f"{doc.replace('IRRI_', 'IRRI_RKB_')}_p{n}"


if __name__ == "__main__":
    main(*sys.argv[1:3])
