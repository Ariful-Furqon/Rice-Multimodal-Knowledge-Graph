"""Split the image observations of Rice MMKG into train, dev and test, and write
the query-time graph that holds no dev or test image.

Rules (Ontology/riceMMKG_SIGIR_plan.md, section 5.1):
- Stratified by (source dataset, annotatedAs), 70/15/15, seed 0, as in
  Multimodal Fusion PoC/ikrl_vs_cnn.py.
- Byte-identical files (same MD5) form one group and go to the same split, so a
  duplicate cannot sit in train and test at once.
- A stratum with fewer than MIN_STRATUM images goes to train only.
- A file that carries two different labels stays in train: it has no single gold.
- test_core: a class-balanced sample of the test split (at most CORE_PER_STRATUM
  per stratum) for the expensive methods (VLM re-ranking).
- The query-time graph drops every triple whose subject or object is a dev or
  test image. Test images are queries, not graph content.

    python -I make_split.py <repo root> <out dir for the graph>
"""
import collections
import csv
import hashlib
import random
import sys
from pathlib import Path

import rdflib
from rdflib.namespace import RDF

R = rdflib.Namespace("https://w3id.org/ricemmkg#")
CONTENT_URL = rdflib.URIRef("http://schema.org/contentUrl")
DERIVED = rdflib.URIRef("http://www.w3.org/ns/prov#wasDerivedFrom")
SEED = 0
FRACTIONS = {"train": 0.70, "dev": 0.15, "test": 0.15}
MIN_STRATUM = 7
CORE_PER_STRATUM = 15


def local(term):
    return str(term).split("#")[-1]


def md5_with_cache(root, urls, cache_path):
    cache = {}
    if cache_path.exists():
        with cache_path.open(encoding="utf-8") as f:
            cache = {r["url"]: r["md5"] for r in csv.DictReader(f)}
    for i, url in enumerate(urls):
        if url not in cache:
            cache[url] = hashlib.md5((root / url).read_bytes()).hexdigest()
        if i % 2000 == 0:
            print(f"  md5 {i}/{len(urls)}", flush=True)
    with cache_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url", "md5"])
        w.writerows(sorted(cache.items()))
    return cache


def split_groups(groups, rng):
    """groups: list of lists of rows in one stratum -> {split: [group, ...]}"""
    rng.shuffle(groups)
    n = sum(len(g) for g in groups)
    target = {"test": round(n * FRACTIONS["test"]), "dev": round(n * FRACTIONS["dev"])}
    out = {"train": [], "dev": [], "test": []}
    filled = {"test": 0, "dev": 0}
    for grp in groups:
        for name in ("test", "dev"):
            if filled[name] + len(grp) <= target[name]:
                out[name].append(grp)
                filled[name] += len(grp)
                break
        else:
            out["train"].append(grp)
    return out


def main(root, graph_out):
    root, graph_out = Path(root), Path(graph_out)
    graph_out.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent.parent / "splits"
    here.mkdir(exist_ok=True)

    g = rdflib.Graph()
    g.parse(root / "Ontology" / "Rice MMKG.rdf", format="xml")
    rows = []
    for s in g.subjects(RDF.type, R.ImageObservation):
        labels = sorted(local(o) for o in g.objects(s, R.annotatedAs))
        rows.append({
            "image": local(s),
            "dataset": ";".join(sorted(local(o) for o in g.objects(s, DERIVED))),
            "annotatedAs": ";".join(labels),
            "url": str(next(g.objects(s, CONTENT_URL))),
        })
    print(f"{len(rows)} image observations")

    md5 = md5_with_cache(root, [r["url"] for r in rows], graph_out / "md5_cache.csv")
    for r in rows:
        r["md5"] = md5[r["url"]]

    strata = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        strata[(r["dataset"], r["annotatedAs"])][r["md5"]].append(r)
    # a duplicate group spanning strata is assigned once, in its first stratum
    seen = set()
    rng = random.Random(SEED)
    for key in sorted(strata):
        groups = [grp for h, grp in sorted(strata[key].items()) if h not in seen]
        seen.update(h for h in strata[key])
        n = sum(len(grp) for grp in groups)
        parts = split_groups(groups, rng) if n >= MIN_STRATUM else {"train": groups, "dev": [], "test": []}
        for name, grps in parts.items():
            for grp in grps:
                for r in grp:
                    r["split"] = name
    by_md5 = {}
    for r in rows:
        if "split" in r:
            by_md5.setdefault(r["md5"], r["split"])
    # one file with two labels has no single gold answer: keep it out of dev and test
    labels_per_md5 = collections.defaultdict(set)
    for r in rows:
        labels_per_md5[r["md5"]].add(r["annotatedAs"])
    for h, labels in labels_per_md5.items():
        if len(labels) > 1:
            by_md5[h] = "train"
            print(f"  label conflict, kept in train: {sorted(labels)}")
    for r in rows:
        r["split"] = by_md5[r["md5"]]

    rows.sort(key=lambda r: (r["dataset"], r["annotatedAs"], r["image"]))
    fields = ["image", "dataset", "annotatedAs", "split", "md5", "url"]
    with (here / "images_split.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    core_rng = random.Random(SEED)
    core = []
    per = collections.defaultdict(list)
    for r in rows:
        if r["split"] == "test":
            per[(r["dataset"], r["annotatedAs"])].append(r)
    for key in sorted(per):
        pick = sorted(per[key], key=lambda r: r["image"])
        core_rng.shuffle(pick)
        core += pick[:CORE_PER_STRATUM]
    with (here / "test_core.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(core, key=lambda r: (r["dataset"], r["annotatedAs"], r["image"])))

    held = {R[r["image"]] for r in rows if r["split"] != "train"}
    q = rdflib.Graph()
    for prefix, ns in g.namespaces():
        q.bind(prefix, ns)
    dropped = 0
    for t in g:
        if t[0] in held or t[2] in held:
            dropped += 1
        else:
            q.add(t)
    q.serialize(graph_out / "RiceMMKG_query_time.ttl", format="turtle")

    count = collections.Counter(r["split"] for r in rows)
    print("split sizes:", dict(count), "| test_core:", len(core))
    print(f"query-time graph: {len(q)} triples ({dropped} dropped)")
    dups = sum(1 for grp in collections.Counter(r["md5"] for r in rows).values() if grp > 1)
    print(f"duplicate md5 groups: {dups}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
