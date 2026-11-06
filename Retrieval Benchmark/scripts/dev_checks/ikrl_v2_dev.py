"""IKRL-style KG fusion re-run on split v2, dev only (no test data).

The August run (Multimodal Fusion PoC/ikrl_vs_cnn.py) used a random 70/15/15 split of
Paddy Doctor, which leaks burst photos (split v1 problem), and compared a linear head
against a linear head + MLP projection, so part of its gain may be capacity, not the KG.
This re-run fixes both:

- split v2 (images_split.csv), CLIP ViT-L/14 features as in stage 1, all 17 conditions;
- early stopping on 10% of the train capture groups, never on dev;
- three heads, same features:
    A  linear                       (= stage-1 linear probe, trained in torch)
    B  linear + gate * -||g(x) - e_c||, e_c from TransE on the domain subgraph (IKRL)
    C  same as B, e_c random and frozen (capacity control: same parameters, no KG)
  The KG effect is B - C, not B - A.
- in-source (train on train) and cross-source (train on the other datasets' train);
  main subset of dev (no single-source dataset), as in step 2;
- 5 seeds; TransE is re-trained per seed.

Normal_Health has no domain triple, so in B it gets a fixed random vector, as in C.

    <venv python> -I ikrl_v2_dev.py <repo root> <out .md>
"""
import collections
import csv
import json
import sys
from pathlib import Path

import numpy as np
import rdflib
import torch
import torch.nn as nn

R = "https://w3id.org/ricemmkg#"
DOMAIN = ["vulnerableTo", "occursIn", "causes", "indicatedBy", "increaseRiskOf", "controlledBy", "recommends",
          "preventedBy", "requires", "transmits", "transmittedBy", "affectsPlantPart", "hasAffectedPart"]
SINGLE_SOURCE = {"NetrokonaRiceDataset", "YukeWbcDataset"}
SEEDS = range(5)
DIM = 64


def transe(triples, seed, epochs=500, margin=1.0):
    torch.manual_seed(seed)
    ents = sorted({x for s, _, o in triples for x in (s, o)})
    rels = sorted({p for _, p, _ in triples})
    e2i, r2i = {e: i for i, e in enumerate(ents)}, {r: i for i, r in enumerate(rels)}
    E, Rl = nn.Embedding(len(ents), DIM), nn.Embedding(len(rels), DIM)
    nn.init.xavier_uniform_(E.weight); nn.init.xavier_uniform_(Rl.weight)
    h = torch.tensor([e2i[s] for s, _, _ in triples]); r = torch.tensor([r2i[p] for _, p, _ in triples])
    t = torch.tensor([e2i[o] for _, _, o in triples])
    opt = torch.optim.Adam(list(E.parameters()) + list(Rl.parameters()), lr=0.01)

    def score(h, r, t):
        return torch.norm(nn.functional.normalize(E(h), dim=-1) + Rl(r) - nn.functional.normalize(E(t), dim=-1), dim=-1)

    for _ in range(epochs):
        neg = torch.randint(0, len(ents), (len(triples),))
        corrupt_head = torch.rand(len(triples)) < 0.5
        loss = torch.clamp(margin + score(h, r, t) - torch.where(corrupt_head, score(neg, r, t), score(h, r, neg)), min=0).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    return {e: nn.functional.normalize(E.weight[i].detach(), dim=0) for e, i in e2i.items()}


class Head(nn.Module):
    def __init__(self, d_in, n, class_emb=None):
        super().__init__()
        self.fc = nn.Linear(d_in, n)
        self.kg = class_emb is not None
        if self.kg:
            self.register_buffer("e", class_emb)
            self.g = nn.Sequential(nn.Linear(d_in, 128), nn.ReLU(), nn.Linear(128, DIM))
            self.log_lam = nn.Parameter(torch.tensor(0.0))

    def forward(self, x):
        out = self.fc(x)
        if self.kg:
            out = out - nn.functional.softplus(self.log_lam) * torch.cdist(nn.functional.normalize(self.g(x), dim=-1), self.e)
        return out


def fit(x_tr, y_tr, x_va, y_va, n, class_emb, seed, epochs=400):
    torch.manual_seed(seed)
    m = Head(x_tr.shape[1], n, class_emb)
    opt = torch.optim.Adam(m.parameters(), lr=1e-3, weight_decay=1e-4)
    best, state = -1.0, None
    for _ in range(epochs):
        m.train(); opt.zero_grad()
        nn.functional.cross_entropy(m(x_tr), y_tr).backward(); opt.step()
        m.eval()
        with torch.no_grad():
            acc = (m(x_va).argmax(1) == y_va).float().mean().item()
        if acc > best:
            best, state = acc, {k: v.clone() for k, v in m.state_dict().items()}
    m.load_state_dict(state); m.eval()
    gate = float(nn.functional.softplus(m.log_lam)) if m.kg else None
    return m, gate


def metrics(scores, gold):
    rank = (scores > scores[np.arange(len(gold)), gold][:, None]).sum(1) + 1
    return {"R@1": float(np.mean(rank == 1)), "MRR": float(np.mean(1 / rank)),
            "macroR@1": float(np.mean([np.mean(rank[gold == c] == 1) for c in np.unique(gold)]))}, 1.0 / rank


def main(root, out_md):
    root = Path(root)
    rows = list(csv.DictReader((root / "Retrieval Benchmark/splits/images_split.csv").open(encoding="utf-8")))
    ents = [str(e) for e in np.load(root / "Data/retrieval/stage1_scores.npz", allow_pickle=True)["entities"]]
    e_idx = {e: i for i, e in enumerate(ents)}
    feats = np.load(root / "Data/retrieval/feats_clip-l14.npz", allow_pickle=True)["feats"].astype(np.float32)
    split = np.array([r["split"] for r in rows]); ds = np.array([r["dataset"] for r in rows])
    with (root / "Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8") as f:
        gold_of = {r["image"]: r["gold"] for r in csv.DictReader(f)}
    group = np.array([r["group"] for r in rows]); gold = np.array([e_idx[gold_of[r["image"]]] for r in rows])

    g = rdflib.Graph(); g.parse(root / "Data/retrieval/RiceMMKG_query_time.ttl")
    triples = [(str(s), p, str(o)) for p in DOMAIN for s, o in g.subject_objects(rdflib.URIRef(R + p))
               if isinstance(o, rdflib.URIRef)]
    print(f"domain triples {len(triples)}", flush=True)

    rng = np.random.default_rng(0)
    ugroups = np.unique(group[split == "train"])
    val_groups = set(rng.choice(ugroups, size=len(ugroups) // 10, replace=False))
    is_val = np.isin(group, list(val_groups)) & (split == "train")
    fit_mask, dev_main = (split == "train") & ~is_val, (split == "dev") & ~np.isin(ds, list(SINGLE_SOURCE))

    protocols = {"in-source": [(fit_mask, is_val, dev_main)]}
    cross = []
    for held in sorted(set(ds[dev_main])):
        tr, va = fit_mask & (ds != held), is_val & (ds != held)
        q = dev_main & (ds == held) & np.isin(gold, np.unique(gold[tr]))
        if q.any():
            cross.append((tr, va, q))
    protocols["cross-source"] = cross

    res = collections.defaultdict(lambda: collections.defaultdict(list))
    rr_all = collections.defaultdict(lambda: collections.defaultdict(list))
    gates = collections.defaultdict(list)
    for seed in SEEDS:
        emb = transe(triples, seed)
        gen = torch.Generator().manual_seed(1000 + seed)
        rand = nn.functional.normalize(torch.randn(len(ents), DIM, generator=gen), dim=1)
        kg_emb = torch.stack([emb.get(R + e, rand[i]) for i, e in enumerate(ents)])
        for proto, parts in protocols.items():
            S = {k: [] for k in "ABC"}; G = []
            for tr, va, q in parts:
                mu, sd = feats[tr].mean(0), feats[tr].std(0) + 1e-6
                X = lambda m: torch.tensor((feats[m] - mu) / sd)
                seen = np.unique(gold[tr])
                for k, ce in (("A", None), ("B", kg_emb), ("C", rand)):
                    m, gate = fit(X(tr), torch.tensor(gold[tr]), X(va), torch.tensor(gold[va]), len(ents), ce, seed)
                    with torch.no_grad():
                        s = m(X(q)).numpy()
                    s[:, np.setdiff1d(np.arange(len(ents)), seen)] = -np.inf
                    S[k].append(s)
                    if gate is not None:
                        gates[(proto, k)].append(gate)
                G.append(gold[q])
            G = np.concatenate(G)
            for k in "ABC":
                mt, rr = metrics(np.concatenate(S[k]), G)
                for name, v in mt.items():
                    res[proto][(k, name)].append(v)
                rr_all[proto][k].append(rr)
            print(f"seed {seed} {proto}: " + "  ".join(f"{k} R@1 {res[proto][(k, 'R@1')][-1]:.3f}" for k in "ABC"), flush=True)

    names = {"A": "A linear (stage-1 probe)", "B": "B IKRL, TransE class vectors", "C": "C same head, random class vectors"}
    lines = ["IKRL re-run on split v2, dev main subset (no single-source dataset), CLIP ViT-L/14 features, "
             f"{len(SEEDS)} seeds (mean ± sd). Early stopping on 10% of the train capture groups. "
             f"Domain subgraph: {len(triples)} triples. Script: `scripts/dev_checks/ikrl_v2_dev.py`.", "",
             "| Protocol | Head | n | R@1 | macro R@1 | MRR | gate λ |", "|---|---|---:|---:|---:|---:|---:|"]
    for proto in protocols:
        n = len(rr_all[proto]["A"][0])
        for k in "ABC":
            f = lambda name: f"{np.mean(res[proto][(k, name)]):.3f} ± {np.std(res[proto][(k, name)]):.3f}"
            gt = f"{np.mean(gates[(proto, k)]):.2f}" if gates[(proto, k)] else ""
            lines.append(f"| {proto} | {names[k]} | {n} | {f('R@1')} | {f('macroR@1')} | {f('MRR')} | {gt} |")
    lines += ["", "KG effect = B − C (same parameters, only the class vectors differ); capacity effect = C − A. "
              "Per seed, paired MRR difference, and the share of seeds where it is positive:", "",
              "| Protocol | B − C MRR | seeds > 0 | C − A MRR | seeds > 0 |", "|---|---:|---:|---:|---:|"]
    summary = {}
    for proto in protocols:
        bc = [float(np.mean(b - c)) for b, c in zip(rr_all[proto]["B"], rr_all[proto]["C"])]
        ca = [float(np.mean(c - a)) for c, a in zip(rr_all[proto]["C"], rr_all[proto]["A"])]
        summary[proto] = {"B-C": bc, "C-A": ca}
        lines.append(f"| {proto} | {np.mean(bc):+.4f} ± {np.std(bc):.4f} | {sum(x > 0 for x in bc)}/{len(bc)} "
                     f"| {np.mean(ca):+.4f} ± {np.std(ca):.4f} | {sum(x > 0 for x in ca)}/{len(ca)} |")
    Path(out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    Path(out_md).with_suffix(".json").write_text(json.dumps(
        {p: {f"{k}|{n}": v for (k, n), v in d.items()} for p, d in res.items()} | {"diff": summary}, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:3])
