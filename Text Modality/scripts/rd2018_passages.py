"""Cut the IRRI Rice Diseases (2018) documents into passages and write
(1) passages.jsonl next to the corpus,
(2) the text module with the wording (CC BY-NC-SA 4.0, like the source), and
(3) a draft of the core pointers (rice:TextDocument and rice:TextPassage with offsets,
    sha256, section and mentions; no wording), to be merged into Rice MMKG.rdf.

Passages are cut with passages.cut(), the same rule as the IRRI Rice Knowledge Bank passages;
mentions use passages.norm() against the labels and altLabels of the domain individuals in the
ontology.

    python -I rd2018_passages.py <data dir> <Rice MMKG.rdf> <module .ttl> <core draft .ttl>
"""
import collections
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from passages import cut, norm  # noqa: E402
from rdflib import Graph, Namespace, RDF, RDFS  # noqa: E402
from rdflib.namespace import SKOS  # noqa: E402

R = Namespace("https://w3id.org/ricemmkg#")
LICENCE = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
DOMAIN = ["Disease", "Pest", "Pathogen", "Symptom", "PlantPart", "GrowthStage", "EnvironmentalFactor",
          "Treatment", "ManagementAction", "AbioticFactor", "Plant", "Variety"]


def lit(s, triple=False):
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return ('"""' + s + '"""@en') if triple else ('"' + s + '"@en')


def main(data, onto, module_out, core_out):
    data = Path(data)
    manifest = json.loads((data / "manifest.json").read_text(encoding="utf-8"))
    g = Graph(); g.parse(onto, format="xml")
    labels = collections.defaultdict(set)
    for cls in DOMAIN:
        for e in set(g.subjects(RDF.type, R[cls])):
            for p in (RDFS.label, SKOS.altLabel):
                for lab in g.objects(e, p):
                    if len(norm(str(lab))) > 3:
                        labels[norm(str(lab))].add(e.split("#")[-1])
    rows = []
    for f in sorted((data / "corpus").glob("IRRI_RD2018_*.txt")):
        doc = f.stem
        text = f.read_text(encoding="utf-8")
        for i, (section, a, b) in enumerate(cut(text)):
            if a == 0:
                continue
            body = text[a:b]
            nb = f" {norm(body)} "
            rows.append({"id": f"{doc}_p{i}", "doc": doc, "title": manifest[doc]["title"], "url": manifest[doc]["url"],
                         "section": section, "start": a, "end": b,
                         "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(), "text": body,
                         "mentions": sorted({n for lab, ns in labels.items() if f" {lab} " in nb for n in ns})})
    (data / "passages.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")

    module = ["""@prefix rice: <https://w3id.org/ricemmkg#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

<https://w3id.org/ricemmkg/text/irri-rice-diseases-2018> a owl:Ontology ;
    dcterms:title "Rice MMKG text module: IRRI Rice Diseases online resource (2018) passages"@en ;
    dcterms:license <%s> ;
    dcterms:rightsHolder "International Rice Research Institute (IRRI)" ;
    dcterms:source <%s> ;
    dcterms:description "Wording of the rice:TextPassage individuals IRRI_RD2018_* declared in Rice MMKG.rdf, taken from IRRI (2018) Rice Diseases: Biology and Selected Management Practices (chapter PDFs downloaded 2026-11-07). Licensed CC BY-NC-SA 4.0 like the source: attribute IRRI, non-commercial use only, share alike. Offsets and sha256 in the core graph refer to the plain text produced by Text Modality/scripts/rd2018_to_text.py (pypdf %s)."@en .
""" % (LICENCE, manifest["_contents"], manifest["_pypdf"])]
    module += [f"rice:IRRI_RD2018_{r['id'][len('IRRI_RD2018_'):]} rice:passageText {lit(r['text'], True)} ." for r in rows]
    Path(module_out).write_text("\n".join(module) + "\n", encoding="utf-8")

    core = ["""# DRAFT, not merged. Core pointers for the IRRI Rice Diseases (2018) text layer: TextDocument and
# TextPassage individuals with offsets, sha256, section and mentions. No wording: that is in
# Text Modality/RiceMMKG_IRRI_RD2018_text.ttl (CC BY-NC-SA 4.0).
@prefix rice: <https://w3id.org/ricemmkg#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
"""]
    for doc, m in sorted((k, v) for k, v in manifest.items() if not k.startswith("_")):
        core.append(f"""rice:{doc} a owl:NamedIndividual, rice:TextDocument ;
    rdfs:label {lit("IRRI Rice Diseases online resource (2018): " + m["title"])} ;
    dcterms:title {lit(m["title"])} ;
    dcterms:source <{m["url"]}> ;
    dcterms:license <{LICENCE}> ;
    rdfs:comment {lit(f"Section of {m['pdf']} from IRRI (2018) Rice Diseases: Biology and Selected Management Practices, {manifest['_contents']} (downloaded 2026-11-07): the introduction and the Symptoms subsection. Plain text by Text Modality/scripts/rd2018_to_text.py, which the passage offsets refer to. Wording in Text Modality/RiceMMKG_IRRI_RD2018_text.ttl.")} .
""")
    for r in rows:
        n = r["id"].rsplit("_p", 1)[1]
        props = [f"rdfs:label {lit(r['title'] + ', passage ' + n)}", f"rice:inDocument rice:{r['doc']}",
                 f'rice:startOffset "{r["start"]}"^^xsd:integer', f'rice:endOffset "{r["end"]}"^^xsd:integer',
                 f'rice:textSha256 "{r["sha256"]}"']
        if r["section"]:
            props.append(f'rice:sectionTitle "{r["section"]}"')
        if r["mentions"]:
            props.append("rice:mentions " + ", ".join(f"rice:{x}" for x in r["mentions"]))
        core.append(f"rice:{r['id']} a owl:NamedIndividual, rice:TextPassage ;\n    " + " ;\n    ".join(props) + " .\n")
    Path(core_out).write_text("\n".join(core), encoding="utf-8")
    print(len(rows), "passages;", sum(1 for r in rows if r["mentions"]), "with mentions")
    for r in rows:
        print(f"  {r['id']:28} [{r['section'] or '-'}] {r['end'] - r['start']:5} chars  {r['text'][:70]!r}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
