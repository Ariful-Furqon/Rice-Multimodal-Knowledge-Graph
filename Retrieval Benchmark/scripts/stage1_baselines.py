"""Stage-1 baselines for entity retrieval: photo -> ranked list of the gold
targets of Rice MMKG (splits/gold.csv, from make_gold.py: the cause to manage,
17 targets).

Plan: Ontology/riceMMKG_SIGIR_plan.md, section 4 (step 1) and 5.2.
Query = the image only; question templates come later (week 3).
Candidates = all targets, for every dataset (no per-dataset shortlist).
Metrics: strict R@k and MRR against the gold, per image and macro over targets;
nDCG@5 with graded relevance (gold 2; a target linked to the gold by `causes`
in either direction 1).

Two protocols:
- In-source: the test split. The headline ("main") leaves out the queries of
  the single-source datasets (Netrokona, YUKE-WBC): each holds one label and
  the source dataset is predictable from the image, so they can be solved by
  recognising the source. Their images stay in the gallery and their targets
  stay candidates.
- Cross-source, leave one dataset out: gallery and probe from the train split
  of all other datasets; queries are the held-out dataset's images of targets
  that another dataset also has.

Systems:
- clip_label:  CLIP zero-shot, one prompt per condition from its label.
- clip_kg:     CLIP zero-shot, label prompt + one prompt per symptom
               (indicatedBy), embeddings averaged. Entity "summary" as in
               OMGM step 1, built from the query-time graph.
- knn_image:   image-to-image search over the train split; a condition scores
               the mean of its 5 most similar train images.
- linear_probe: logistic regression on CLIP image features of the train split.
               Supervised reference, not a retrieval method.

Leakage: entity text comes from Data/retrieval/RiceMMKG_query_time.ttl, which
holds no dev or test image. kNN and the probe see train images only.

    <venv python> -I stage1_baselines.py <repo root> <out dir>
"""
import collections
import csv
import json
import sys
from pathlib import Path

import numpy as np
import rdflib
import torch
from PIL import Image
from sklearn.linear_model import LogisticRegression
from transformers import CLIPModel, CLIPProcessor

R = rdflib.Namespace("https://w3id.org/ricemmkg#")
MODEL = "openai/clip-vit-large-patch14"
KNN_K = 5
TOP_KS = (1, 3, 5)
BATCH = 64
# one label each: a model can score by recognising the source, not the condition
SINGLE_SOURCE = {"NetrokonaRiceDataset", "YukeWbcDataset"}


def local(term):
    return str(term).split("#")[-1]


def label_of(g, node):
    lab = g.value(node, rdflib.RDFS.label)
    return str(lab) if lab else local(node).replace("_", " ")


def entity_prompts(g, entities):
    """{entity: [prompt, ...]}; the first prompt is the label prompt."""
    prompts = {}
    for e in entities:
        node = R[e]
        name = label_of(g, node)
        first = ("a photo of a healthy rice plant" if e == "Normal_Health"
                 else f"a photo of a rice plant with {name}")
        symptoms = sorted(label_of(g, s) for s in g.objects(node, R.indicatedBy))
        prompts[e] = [first] + [f"a photo of a rice plant showing {s.lower()}" for s in symptoms]
    return prompts


@torch.no_grad()
def encode_images(model, proc, root, urls, cache):
    if cache.exists():
        data = np.load(cache, allow_pickle=True)
        if list(data["urls"]) == urls:
            return data["feats"]
    feats = []
    for i in range(0, len(urls), BATCH):
        imgs = [Image.open(root / u).convert("RGB") for u in urls[i:i + BATCH]]
        x = proc(images=imgs, return_tensors="pt").to("cuda")
        pooled = model.vision_model(pixel_values=x["pixel_values"].half()).pooler_output
        f = model.visual_projection(pooled)
        feats.append(torch.nn.functional.normalize(f.float(), dim=-1).cpu().numpy())
        if i % (BATCH * 40) == 0:
            print(f"  images {i}/{len(urls)}", flush=True)
    feats = np.concatenate(feats)
    np.savez(cache, feats=feats, urls=np.array(urls, dtype=object))
    return feats


@torch.no_grad()
def encode_texts(model, proc, texts):
    x = proc(text=texts, return_tensors="pt", padding=True, truncation=True).to("cuda")
    pooled = model.text_model(input_ids=x["input_ids"], attention_mask=x["attention_mask"]).pooler_output
    f = model.text_projection(pooled)
    return torch.nn.functional.normalize(f.float(), dim=-1).cpu().numpy()


def graded_relevance(g, entities):
    """(n, n) matrix: rel[gold, candidate] = 2 for the gold, 1 if linked by causes."""
    rel = 2 * np.eye(len(entities))
    for i, a in enumerate(entities):
        for j, b in enumerate(entities):
            if i != j and ((R[a], R.causes, R[b]) in g or (R[b], R.causes, R[a]) in g):
                rel[i, j] = 1
    return rel


def evaluate(scores, gold_idx, rel):
    """scores: (n, n_entities); returns recall@k, MRR and graded nDCG@5 (means over rows)."""
    order = np.argsort(-scores, axis=1)
    rank = np.argmax(order == gold_idx[:, None], axis=1) + 1
    out = {f"R@{k}": float(np.mean(rank <= k)) for k in TOP_KS}
    out["MRR"] = float(np.mean(1.0 / rank))
    out["macroR@1"] = float(np.mean([np.mean(rank[gold_idx == c] == 1) for c in np.unique(gold_idx)]))
    disc = 1.0 / np.log2(np.arange(2, 7))
    gains = (2 ** rel[gold_idx[:, None], order[:, :5]] - 1) @ disc
    ideal = (2 ** (-np.sort(-rel[gold_idx], axis=1)[:, :5]) - 1) @ disc
    out["nDCG@5"] = float(np.mean(gains / ideal))
    return out, rank, order[:, 0]


def main(root, out_dir):
    root, out_dir = Path(root), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with (root / "Retrieval Benchmark/splits/images_split.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with (root / "Retrieval Benchmark/splits/test_core.csv").open(encoding="utf-8") as f:
        core = {r["image"] for r in csv.DictReader(f)}
    with (root / "Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8") as f:
        gold_of = {r["image"]: r["gold"] for r in csv.DictReader(f)}
    entities = sorted(set(gold_of.values()))
    e_idx = {e: i for i, e in enumerate(entities)}

    g = rdflib.Graph()
    g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
    prompts = entity_prompts(g, entities)
    rel = graded_relevance(g, entities)
    print(f"{len(entities)} targets; graded pairs (relevance 1):",
          [(entities[i], entities[j]) for i, j in zip(*np.nonzero(rel == 1))])

    model = CLIPModel.from_pretrained(MODEL, torch_dtype=torch.float16).to("cuda").eval()
    proc = CLIPProcessor.from_pretrained(MODEL)
    urls = [r["url"] for r in rows]
    feats = encode_images(model, proc, root, urls, root / "Data/retrieval/feats_clip-l14.npz")

    label_emb = encode_texts(model, proc, [p[0] for e, p in prompts.items()])
    kg_emb = np.stack([encode_texts(model, proc, prompts[e]).mean(0) for e in entities])
    kg_emb /= np.linalg.norm(kg_emb, axis=1, keepdims=True)

    split = np.array([r["split"] for r in rows])
    gold = np.array([e_idx[gold_of[r["image"]]] for r in rows])
    train, test = split == "train", split == "test"

    def knn_scores(q, g_feats, g_gold):
        sims = q @ g_feats.T
        out = np.full((len(q), len(entities)), -1.0)
        for j in range(len(entities)):
            s = sims[:, g_gold == j]
            if s.shape[1]:
                k = min(KNN_K, s.shape[1])
                out[:, j] = np.sort(s, axis=1)[:, -k:].mean(1)
        return out

    def probe_scores(q, g_feats, g_gold):
        probe = LogisticRegression(max_iter=2000, C=1.0).fit(g_feats, g_gold)
        out = np.full((len(q), len(entities)), -np.inf)
        out[:, probe.classes_] = probe.predict_log_proba(q)
        return out

    def run_systems(q, g_feats, g_gold):
        return {
            "clip_label": q @ label_emb.T,
            "clip_kg": q @ kg_emb.T,
            "knn_image": knn_scores(q, g_feats, g_gold),
            "linear_probe": probe_scores(q, g_feats, g_gold),
        }

    q = feats[test]
    systems = run_systems(q, feats[train], gold[train])
    nearest = (q @ feats[train].T).max(1)
    leak = {f">={t}": float(np.mean(nearest >= t)) for t in (0.95, 0.98, 0.99)}
    print("test images with a train image at CLIP similarity", leak)

    dataset = np.array([r["dataset"] for r in rows])
    # shortcut check: how well the source dataset is predicted from the image
    ds_probe = LogisticRegression(max_iter=3000).fit(feats[train], dataset[train])
    dataset_id_acc = float(np.mean(ds_probe.predict(q) == dataset[test]))
    print(f"source dataset predicted from the image: {dataset_id_acc:.3f}")

    test_rows = [r for r, t in zip(rows, test) if t]
    datasets = sorted({r["dataset"] for r in test_rows})
    in_core = np.array([r["image"] in core for r in test_rows])
    ds = np.array([r["dataset"] for r in test_rows])
    main_q = ~np.isin(ds, list(SINGLE_SOURCE))
    g_test = gold[test]

    results, confusions = {}, {}
    for name, sc in systems.items():
        res = {}
        for subset, mask in [("main", main_q), ("test", np.ones(len(test_rows), bool)),
                             ("test_core", in_core & main_q)] + [(d, ds == d) for d in datasets]:
            res[subset] = evaluate(sc[mask], g_test[mask], rel)[0] | {"n": int(mask.sum())}
        results[name] = res
        _, _, top1 = evaluate(sc[main_q], g_test[main_q], rel)
        pairs = collections.Counter((entities[a], entities[b]) for a, b in zip(g_test[main_q], top1) if a != b)
        confusions[name] = [[a, b, n] for (a, b), n in pairs.most_common(8)]

    # cross-source, leave one dataset out: gallery and probe from the train split of
    # every other dataset; queries are all images of the held-out dataset whose
    # target the gallery has (a target seen in one source only cannot be tested)
    lodo, lodo_q, lodo_scores = {}, [], collections.defaultdict(list)
    for held in sorted(set(dataset)):
        gal = train & (dataset != held)
        qm = (dataset == held) & np.isin(gold, np.unique(gold[gal]))
        if not qm.any():
            continue
        sys_scores = run_systems(feats[qm], feats[gal], gold[gal])
        lodo[held] = {"n": int(qm.sum()), "targets": sorted({entities[j] for j in gold[qm]}),
                      "results": {n: evaluate(sc, gold[qm], rel)[0] for n, sc in sys_scores.items()}}
        lodo_q.append(gold[qm])
        for n, sc in sys_scores.items():
            lodo_scores[n].append(sc)
    lodo_gold = np.concatenate(lodo_q)
    lodo_all = {n: evaluate(np.concatenate(s), lodo_gold, rel)[0] | {"n": len(lodo_gold)}
                for n, s in lodo_scores.items()}

    (out_dir / "stage1_results.json").write_text(json.dumps(
        {"model": MODEL, "entities": entities, "prompts": prompts,
         "single_source_excluded_from_main": sorted(SINGLE_SOURCE),
         "results": results, "top_confusions_main": confusions,
         "test_near_duplicate_rate": leak, "dataset_id_accuracy": dataset_id_acc,
         "leave_one_dataset_out": {"pooled": lodo_all, "per_dataset": lodo}}, indent=1), encoding="utf-8")

    names = list(systems)
    lines = [f"In-source: test split, {len(entities)} candidate targets. "
             f"main = test without the single-source datasets ({', '.join(sorted(SINGLE_SOURCE))}).", "",
             "| System | main R@1 | main macro R@1 | main MRR | test_core R@1 | all test R@1 |",
             "|---|---:|---:|---:|---:|---:|"]
    for n in names:
        r = results[n]
        lines.append(f"| {n} | {r['main']['R@1']:.3f} | {r['main']['macroR@1']:.3f} | {r['main']['MRR']:.3f} "
                     f"| {r['test_core']['R@1']:.3f} | {r['test']['R@1']:.3f} |")
    lines += ["", "Per dataset (test split, R@1):", "",
              "| System | " + " | ".join(datasets) + " |", "|---|" + "---:|" * len(datasets)]
    for n in names:
        lines.append(f"| {n} | " + " | ".join(f"{results[n][d]['R@1']:.3f}" for d in datasets) + " |")
    lines += ["", f"Cross-source, leave one dataset out (pooled n = {len(lodo_gold)}):", "",
              "| System | R@1 | macro R@1 | R@3 | MRR |", "|---|---:|---:|---:|---:|"]
    for n in names:
        r = lodo_all[n]
        lines.append(f"| {n} | {r['R@1']:.3f} | {r['macroR@1']:.3f} | {r['R@3']:.3f} | {r['MRR']:.3f} |")
    lines += ["", "Per held-out dataset (R@1; targets tested):", "",
              "| Held out | n | targets | " + " | ".join(names) + " |", "|---|---:|---|" + "---:|" * len(names)]
    for held, v in lodo.items():
        lines.append(f"| {held} | {v['n']} | {', '.join(v['targets'])} | "
                     + " | ".join(f"{v['results'][n]['R@1']:.3f}" for n in names) + " |")
    lines += ["", f"Source dataset predicted from the image (linear probe): {dataset_id_acc:.3f}"]
    (out_dir / "stage1_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    for name, c in confusions.items():
        print(name, c[:4])


if __name__ == "__main__":
    main(*sys.argv[1:3])
