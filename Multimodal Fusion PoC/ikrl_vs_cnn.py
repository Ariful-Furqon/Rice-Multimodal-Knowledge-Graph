"""
IKRL-style KG fusion vs. plain CNN baseline, on full-dataset disease classification.

Requested comparison: a "plain ResNet CNN" classifier vs. an IKRL
(Image-embodied Knowledge Representation Learning, Xie et al. 2017)-style
fusion classifier that combines visual features with Rice MMKG structure
embeddings, on the 10-class Paddy Doctor label task (10,407 images).

Why this is NOT the same design as fusion_poc.py's concatenation, and why
that matters
----------------------------------------------------------------------------
fusion_diagnostic_notes.md (Finding 1) established that every image
individual's graph signature collapses onto its `annotatedAs` class --
10,407 images produce only 10 distinct graph embeddings. Feeding a
per-IMAGE graph embedding into a classifier that predicts the image's class
is therefore circular: the "feature" already IS the label, looked up from
an oracle the classifier isn't supposed to have at test time.

This script avoids that leak structurally, not just procedurally:
  1. The structure-based representation is trained ONLY on the domain
     subgraph (Disease/Pest/HealthStatus <-> Symptom/EnvironmentalFactor/
     GrowthStage/Treatment/... via indicatedBy, increaseRiskOf, occursIn,
     controlledBy, causes, vulnerableTo, recommends, preventedBy, requires,
     transmits -- 265 assertions, 90 entities). No ImageObservation
     individual and no `annotatedAs` edge is in this graph at all, so the
     10 class embeddings it produces encode real agronomic relational
     structure (shared symptoms, shared risk factors), not image identity.
  2. At inference, a test image never gets to look up "its" class
     embedding -- the model only ever has all 10 (fixed, precomputed)
     class embeddings available, the same way for every image, and has to
     figure out via a learned projection which one its visual features are
     closest to. This is the IKRL mechanism applied to classification: a
     projection g() maps the image into the structure-embedding space, and
     the class whose structure embedding is nearest is the KG-side vote --
     exactly analogous to IKRL scoring a candidate (image, entity) pair by
     distance in the shared embedding space, just repurposed for
     classification instead of link prediction.

Two models are compared, sharing the identical frozen ResNet-18
(ImageNet-pretrained, no fine-tuning -- see README for the CPU-only compute
justification) visual features, differing only in the classifier head:

  Model A (plain CNN baseline): logits = Linear(512 -> 10)(visual_feat)

  Model B (IKRL fusion): logits = Linear(512 -> 10)(visual_feat)
                                   + softplus(lambda) * (-||g(visual_feat) - e_c||_2)_{c=1..10}
    where g: 512 -> 64 is an MLP projection into the TransE structure space,
    e_c are the 10 frozen class structure embeddings, and lambda is a
    learned scalar gate (so the model can down-weight the KG term to ~0 if
    it doesn't help -- the comparison is not rigged to force fusion to win).

Also reports, after training, a cosine-similarity matrix over Model B's
LEARNED projection g(visual_feat) for one sample image per class -- the
same style of sanity check fusion_poc.py ran over raw concatenated vectors,
but now over the trained, non-circular projection, to see whether the
class-block structure fusion_poc.py's PoC failed to find actually emerges
once the projection is fit to something (the classifier objective) instead
of read off an untrained embedding table.

Run: `python "ikrl_vs_cnn.py"` from anywhere; paths resolve relative to
this file. Requires rdflib, torch, torchvision, pillow, scikit-learn.
Visual feature extraction over the full 10,407 images is cached to
`resnet18_features_cache.pt` in this folder after the first run.
"""
import os
import json
import random
import time

import rdflib
import torch
import torch.nn as nn
import torchvision
from PIL import Image

SEED = 0
random.seed(SEED)
torch.manual_seed(SEED)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
RDF_PATH = os.path.join(BASE, "Ontology", "Rice MMKG.rdf")
DATA_DIR = os.path.join(BASE, "Data", "PaddyDoctor")
CACHE_PATH = os.path.join(SCRIPT_DIR, "resnet18_features_cache.pt")
NS = "http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#"

# label folder name -> ontology individual local name (verified against
# rice:sourceDatasetLabel assertions in Rice MMKG.rdf, not guessed)
LABEL_TO_CLASS = {
    "bacterial_leaf_blight": "Bacterial_Leaf_Blight",
    "bacterial_leaf_streak": "Bacterial_Leaf_Streak",
    "bacterial_panicle_blight": "Bacterial_Panicle_Blight",
    "blast": "Rice_Blast_Disease",
    "brown_spot": "Brown_Spot",
    "dead_heart": "Deadheart",
    "downy_mildew": "Downy_Mildew",
    "hispa": "Hispa",
    "normal": "Normal_Health",
    "tungro": "Rice_Tungro_Disease",
}
CLASSES = sorted(LABEL_TO_CLASS)  # fixed class order used everywhere below
LABEL_TO_IDX = {lbl: i for i, lbl in enumerate(CLASSES)}

# same 10 sample images fusion_poc.py used, reused here for the
# similarity-matrix sanity check so the two reports are directly comparable
SAMPLE_IMAGES = {
    "bacterial_leaf_blight": "100023.jpg",
    "bacterial_leaf_streak": "100042.jpg",
    "bacterial_panicle_blight": "100043.jpg",
    "blast": "100004.jpg",
    "brown_spot": "100001.jpg",
    "dead_heart": "100008.jpg",
    "downy_mildew": "100017.jpg",
    "hispa": "100003.jpg",
    "normal": "100002.jpg",
    "tungro": "100011.jpg",
}

DOMAIN_PROPERTIES = {
    "vulnerableTo", "occursIn", "causes", "indicatedBy", "increaseRiskOf",
    "controlledBy", "recommends", "preventedBy", "requires",
    "transmits", "transmittedBy",
}

# ---------------------------------------------------------------------------
# 1. Structure-based representation: TransE on the domain-only subgraph
# ---------------------------------------------------------------------------

def load_domain_triples(rdf_path):
    g = rdflib.Graph()
    g.parse(rdf_path, format="xml")
    triples = []
    for s, p, o in g:
        if not (isinstance(s, rdflib.URIRef) and isinstance(o, rdflib.URIRef)):
            continue
        if not str(p).startswith(NS):
            continue
        local = str(p)[len(NS):]
        if local in DOMAIN_PROPERTIES:
            triples.append((str(s), local, str(o)))
    return triples


class TransE(nn.Module):
    def __init__(self, n_entities, n_relations, dim=64):
        super().__init__()
        self.ent_emb = nn.Embedding(n_entities, dim)
        self.rel_emb = nn.Embedding(n_relations, dim)
        nn.init.xavier_uniform_(self.ent_emb.weight)
        nn.init.xavier_uniform_(self.rel_emb.weight)

    def score(self, h, r, t):
        h_e = nn.functional.normalize(self.ent_emb(h), dim=-1)
        t_e = nn.functional.normalize(self.ent_emb(t), dim=-1)
        r_e = self.rel_emb(r)
        return torch.norm(h_e + r_e - t_e, p=2, dim=-1)


def train_transe(triples, ent2id, rel2id, dim=64, epochs=500, lr=0.01, margin=1.0):
    n_e, n_r = len(ent2id), len(rel2id)
    model = TransE(n_e, n_r, dim=dim)
    opt = torch.optim.Adam(model.parameters(), lr=lr)

    hs = torch.tensor([ent2id[s] for s, p, o in triples])
    rs = torch.tensor([rel2id[p] for s, p, o in triples])
    ts = torch.tensor([ent2id[o] for s, p, o in triples])
    n_triples = len(triples)

    for epoch in range(epochs):
        neg_ts = torch.randint(0, n_e, (n_triples,))
        pos_score = model.score(hs, rs, ts)
        neg_score = model.score(hs, rs, neg_ts)
        loss = torch.clamp(margin + pos_score - neg_score, min=0).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if (epoch + 1) % 100 == 0:
            print(f"    epoch {epoch + 1:4d}/{epochs}  loss={loss.item():.4f}")
    return model


def build_structure_embeddings():
    print("[1/4] Building domain-only subgraph and training TransE...")
    triples = load_domain_triples(RDF_PATH)
    entities = sorted({s for s, p, o in triples} | {o for s, p, o in triples})
    relations = sorted({p for s, p, o in triples})
    ent2id = {e: i for i, e in enumerate(entities)}
    rel2id = {r: i for i, r in enumerate(relations)}
    print(f"    domain triples: {len(triples)}  entities: {len(entities)}  relations: {len(relations)}")
    for c in CLASSES:
        assert f"{NS}{LABEL_TO_CLASS[c]}" in ent2id, f"{LABEL_TO_CLASS[c]} missing from domain subgraph"

    model = train_transe(triples, ent2id, rel2id, dim=64, epochs=500)
    class_emb = torch.stack([
        model.ent_emb.weight[ent2id[f"{NS}{LABEL_TO_CLASS[c]}"]].detach()
        for c in CLASSES
    ])  # (10, 64)
    return nn.functional.normalize(class_emb, dim=-1)


# ---------------------------------------------------------------------------
# 2. Visual features: frozen ResNet-18, full 10,407-image dataset, cached
# ---------------------------------------------------------------------------

def extract_all_features():
    if os.path.exists(CACHE_PATH):
        print(f"[2/4] Loading cached visual features from {CACHE_PATH}")
        cache = torch.load(CACHE_PATH)
        return cache["features"], cache["labels"], cache["paths"]

    print("[2/4] Extracting ResNet-18 (frozen, ImageNet weights) features for all images...")
    weights = torchvision.models.ResNet18_Weights.IMAGENET1K_V1
    model = torchvision.models.resnet18(weights=weights)
    model.fc = nn.Identity()
    model.eval()
    preprocess = weights.transforms()

    paths, labels = [], []
    for label in CLASSES:
        d = os.path.join(DATA_DIR, label)
        for fname in sorted(os.listdir(d)):
            paths.append(os.path.join(d, fname))
            labels.append(LABEL_TO_IDX[label])
    print(f"    {len(paths)} images across {len(CLASSES)} classes")

    features = torch.zeros(len(paths), 512)
    batch_size = 64
    t0 = time.time()
    with torch.no_grad():
        for start in range(0, len(paths), batch_size):
            end = min(start + batch_size, len(paths))
            imgs = [preprocess(Image.open(p).convert("RGB")) for p in paths[start:end]]
            batch = torch.stack(imgs)
            features[start:end] = model(batch)
            if start % (batch_size * 20) == 0:
                elapsed = time.time() - t0
                print(f"    {end}/{len(paths)}  ({elapsed:.0f}s elapsed)")
    labels = torch.tensor(labels)
    torch.save({"features": features, "labels": labels, "paths": paths}, CACHE_PATH)
    print(f"    done in {time.time() - t0:.0f}s, cached to {CACHE_PATH}")
    return features, labels, paths


# ---------------------------------------------------------------------------
# 3. Stratified split
# ---------------------------------------------------------------------------

def stratified_split(labels, train_frac=0.7, val_frac=0.15, seed=SEED):
    g = torch.Generator().manual_seed(seed)
    train_idx, val_idx, test_idx = [], [], []
    for c in range(len(CLASSES)):
        idx = (labels == c).nonzero(as_tuple=True)[0]
        perm = idx[torch.randperm(len(idx), generator=g)]
        n = len(perm)
        n_train = int(n * train_frac)
        n_val = int(n * val_frac)
        train_idx.append(perm[:n_train])
        val_idx.append(perm[n_train:n_train + n_val])
        test_idx.append(perm[n_train + n_val:])
    return (torch.cat(train_idx), torch.cat(val_idx), torch.cat(test_idx))


# ---------------------------------------------------------------------------
# 4. Model A (plain CNN baseline) and Model B (IKRL fusion)
# ---------------------------------------------------------------------------

class PlainCNNHead(nn.Module):
    def __init__(self, visual_dim=512, n_classes=10):
        super().__init__()
        self.fc = nn.Linear(visual_dim, n_classes)

    def forward(self, visual_feat):
        return self.fc(visual_feat)


class IKRLFusionHead(nn.Module):
    """Structure embeddings e_c are fixed; only the projection, the visual
    linear head, and the gate are trained."""

    def __init__(self, class_struct_emb, visual_dim=512, struct_dim=64, n_classes=10):
        super().__init__()
        self.register_buffer("class_struct_emb", class_struct_emb)  # (n_classes, struct_dim), frozen
        self.fc_visual = nn.Linear(visual_dim, n_classes)
        self.project = nn.Sequential(
            nn.Linear(visual_dim, 128), nn.ReLU(),
            nn.Linear(128, struct_dim),
        )
        self.log_lambda = nn.Parameter(torch.tensor(0.0))  # gate, softplus'd -> >= 0

    def forward(self, visual_feat):
        visual_logits = self.fc_visual(visual_feat)
        projected = nn.functional.normalize(self.project(visual_feat), dim=-1)
        dist = torch.cdist(projected, self.class_struct_emb)  # (B, n_classes)
        struct_logits = -dist
        gate = nn.functional.softplus(self.log_lambda)
        return visual_logits + gate * struct_logits, gate.item()


def train_and_eval(model_name, model, feats, labels, train_idx, val_idx, test_idx,
                    epochs=200, lr=1e-3, is_fusion=False):
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    x_train, y_train = feats[train_idx], labels[train_idx]
    x_val, y_val = feats[val_idx], labels[val_idx]
    x_test, y_test = feats[test_idx], labels[test_idx]

    best_val_acc, best_state = -1, None
    for epoch in range(epochs):
        model.train()
        opt.zero_grad()
        out = model(x_train)
        logits = out[0] if is_fusion else out
        loss = nn.functional.cross_entropy(logits, y_train)
        loss.backward()
        opt.step()

        model.eval()
        with torch.no_grad():
            out = model(x_val)
            logits = out[0] if is_fusion else out
            val_acc = (logits.argmax(-1) == y_val).float().mean().item()
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        if (epoch + 1) % 50 == 0:
            gate_str = f"  gate(lambda)={out[1]:.4f}" if is_fusion else ""
            print(f"    [{model_name}] epoch {epoch + 1:3d}/{epochs}  train_loss={loss.item():.4f}  val_acc={val_acc:.4f}{gate_str}")

    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        out = model(x_test)
        logits = out[0] if is_fusion else out
        gate = out[1] if is_fusion else None
        preds = logits.argmax(-1)
    test_acc = (preds == y_test).float().mean().item()
    cm = confusion_matrix(y_test, preds, len(CLASSES))
    macro_f1 = macro_f1_score(cm)
    return {
        "model": model_name,
        "best_val_acc": best_val_acc,
        "test_acc": test_acc,
        "macro_f1": macro_f1,
        "confusion_matrix": cm.tolist(),
        "gate_lambda": gate,
    }


def confusion_matrix(y_true, y_pred, n_classes):
    cm = torch.zeros(n_classes, n_classes, dtype=torch.long)
    for t, p in zip(y_true.tolist(), y_pred.tolist()):
        cm[t, p] += 1
    return cm


def macro_f1_score(cm):
    n = cm.shape[0]
    f1s = []
    for c in range(n):
        tp = cm[c, c].item()
        fp = cm[:, c].sum().item() - tp
        fn = cm[c, :].sum().item() - tp
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        f1s.append(f1)
    return sum(f1s) / n


def print_confusion(cm):
    header = "              " + " ".join(f"{c[:6]:>6s}" for c in CLASSES)
    print(header)
    for i, row in enumerate(cm):
        print(f"{CLASSES[i]:14s}" + " ".join(f"{v:6d}" for v in row))


# ---------------------------------------------------------------------------
# 5. Similarity-matrix sanity check on Model B's trained projection
# ---------------------------------------------------------------------------

def sample_projection_similarity(model_b, paths, feats):
    """Cosine-similarity matrix over g(visual_feat) for one sample image per
    class -- fusion_poc.py's exact style of sanity check, but over Model B's
    TRAINED projection instead of an untrained per-image embedding lookup."""
    path_to_idx = {p: i for i, p in enumerate(paths)}
    sample_idx, sample_labels = [], []
    for label in CLASSES:
        fname = SAMPLE_IMAGES[label]
        p = os.path.join(DATA_DIR, label, fname)
        if p not in path_to_idx:
            print(f"  WARNING: sample image for {label} not found in feature cache, skipping")
            continue
        sample_idx.append(path_to_idx[p])
        sample_labels.append(label)

    model_b.eval()
    with torch.no_grad():
        x = feats[torch.tensor(sample_idx)]
        projected = nn.functional.normalize(model_b.project(x), dim=-1)  # (10, 64)
    sim = projected @ projected.T
    return sim, sample_labels


def print_similarity_matrix(sim, labels, title):
    print(f"\n{title}")
    header = "              " + " ".join(f"{l[:8]:>8s}" for l in labels)
    print(header)
    for i, l in enumerate(labels):
        row = " ".join(f"{sim[i, j].item():8.3f}" for j in range(len(labels)))
        print(f"{l:14s}{row}")


def main():
    class_struct_emb = build_structure_embeddings()

    feats, labels, paths = extract_all_features()

    print("[3/4] Stratified 70/15/15 train/val/test split...")
    train_idx, val_idx, test_idx = stratified_split(labels)
    print(f"    train={len(train_idx)}  val={len(val_idx)}  test={len(test_idx)}")

    print("[4/4] Training and evaluating both models...")
    model_a = PlainCNNHead()
    result_a = train_and_eval("PlainCNN", model_a, feats, labels, train_idx, val_idx, test_idx, is_fusion=False)

    model_b = IKRLFusionHead(class_struct_emb)
    result_b = train_and_eval("IKRLFusion", model_b, feats, labels, train_idx, val_idx, test_idx, is_fusion=True)

    print()
    print("=" * 70)
    print(f"Model A (plain ResNet-18 + linear head):")
    print(f"  test accuracy = {result_a['test_acc']:.4f}   macro-F1 = {result_a['macro_f1']:.4f}")
    print(f"Model B (IKRL-style KG fusion):")
    print(f"  test accuracy = {result_b['test_acc']:.4f}   macro-F1 = {result_b['macro_f1']:.4f}   learned gate={result_b['gate_lambda']:.4f}")
    print("=" * 70)

    print("\nModel A confusion matrix (rows=true, cols=pred):")
    print_confusion(result_a["confusion_matrix"])
    print("\nModel B confusion matrix (rows=true, cols=pred):")
    print_confusion(result_b["confusion_matrix"])

    # Similarity-matrix sanity check on Model B's trained projection --
    # same 10 sample images and same style of report as fusion_poc.py, to
    # see whether class-block structure emerges once the projection is
    # actually fit to something.
    class_sim = class_struct_emb @ class_struct_emb.T
    print_similarity_matrix(class_sim, CLASSES,
                             "Class structure-embedding similarity (e_c, TransE, domain-only subgraph):")
    sample_sim, sample_labels = sample_projection_similarity(model_b, paths, feats)
    print_similarity_matrix(sample_sim, sample_labels,
                             "Model B learned projection g(visual) similarity, one sample image per class:")

    # Check the diagnostic notes' falsifiable prediction (Finding 4):
    # Brown_Spot <-> Rice_Blast_Disease should be confused more than most
    # other pairs, since the KG says they share the most symptoms/risk
    # factors of any pair in the dataset.
    bs, bl = LABEL_TO_IDX["brown_spot"], LABEL_TO_IDX["blast"]
    cm_a = result_a["confusion_matrix"]
    n_bs = sum(cm_a[bs])
    n_bl = sum(cm_a[bl])
    confusion_rate = (cm_a[bs][bl] + cm_a[bl][bs]) / max(n_bs + n_bl, 1)
    print(f"\nBrown_Spot<->Rice_Blast_Disease confusion rate in Model A: {confusion_rate:.4f}")

    out = {"class_order": CLASSES, "model_a": result_a, "model_b": result_b,
           "brown_spot_blast_confusion_rate": confusion_rate,
           "class_struct_similarity": class_sim.tolist(),
           "model_b_sample_projection_similarity": sample_sim.tolist()}
    out_path = os.path.join(SCRIPT_DIR, "ikrl_vs_cnn_results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nFull results written to {out_path}")


if __name__ == "__main__":
    main()
