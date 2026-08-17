"""
Multimodal fusion proof-of-concept for Rice MMKG.

Demonstrates the mechanism (not a production pipeline):
1. Train a minimal TransE graph embedding on Rice MMKG.rdf.
2. Extract visual features for 10 sample Paddy Doctor images (one per
   dataset label, the same pilot images populated in the Observation
   population batch) using a pretrained ResNet-18 (ImageNet weights, no
   fine-tuning).
3. Fuse (concatenate) the graph embedding and visual embedding for each
   sample image's LeafImage individual.
4. Show a cosine-similarity matrix over the fused vectors as a sanity check.

Run from anywhere; paths are resolved relative to this file's location.
"""
import os
import random
import rdflib
import torch
import torch.nn as nn
import torchvision
from PIL import Image

random.seed(0)
torch.manual_seed(0)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
RDF_PATH = os.path.join(BASE, "Ontology", "Rice MMKG.rdf")
DATA_DIR = os.path.join(BASE, "Data", "PaddyDoctor")
NS = "http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#"

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

def load_triples(rdf_path):
    g = rdflib.Graph()
    g.parse(rdf_path, format="xml")
    triples = []
    for s, p, o in g:
        if isinstance(s, rdflib.URIRef) and isinstance(o, rdflib.URIRef):
            triples.append((str(s), str(p), str(o)))
    return triples


def build_vocab(triples):
    entities, relations = set(), set()
    for s, p, o in triples:
        entities.add(s)
        entities.add(o)
        relations.add(p)
    ent2id = {e: i for i, e in enumerate(sorted(entities))}
    rel2id = {r: i for i, r in enumerate(sorted(relations))}
    return ent2id, rel2id


class TransE(nn.Module):
    def __init__(self, n_entities, n_relations, dim=64):
        super().__init__()
        self.ent_emb = nn.Embedding(n_entities, dim)
        self.rel_emb = nn.Embedding(n_relations, dim)
        nn.init.xavier_uniform_(self.ent_emb.weight)
        nn.init.xavier_uniform_(self.rel_emb.weight)

    def score(self, h, r, t):
        h_e, r_e, t_e = self.ent_emb(h), self.rel_emb(r), self.ent_emb(t)
        h_e = nn.functional.normalize(h_e, dim=-1)
        t_e = nn.functional.normalize(t_e, dim=-1)
        return torch.norm(h_e + r_e - t_e, p=2, dim=-1)


def train_transe(triples, ent2id, rel2id, dim=64, epochs=100, lr=0.01, margin=1.0):
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
        if (epoch + 1) % 20 == 0:
            print(f"  epoch {epoch + 1:3d}/{epochs}  loss={loss.item():.4f}")

    return model



def load_visual_encoder():
    weights = torchvision.models.ResNet18_Weights.IMAGENET1K_V1
    model = torchvision.models.resnet18(weights=weights)
    model.fc = nn.Identity()  # strip classification head -> 512-d feature
    model.eval()
    return model, weights.transforms()


def extract_visual_embedding(model, preprocess, image_path):
    img = Image.open(image_path).convert("RGB")
    x = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        feat = model(x).squeeze(0)
    return feat


def main():
    print("Loading RDF and extracting URI-URI triples...")
    triples = load_triples(RDF_PATH)
    print(f"  {len(triples)} triples loaded")

    ent2id, rel2id = build_vocab(triples)
    print(f"  {len(ent2id)} entities, {len(rel2id)} relations")

    print("Training minimal TransE (100 epochs, dim=64)...")
    model = train_transe(triples, ent2id, rel2id, dim=64, epochs=100)

    print("Loading pretrained ResNet-18 for visual features...")
    visual_model, preprocess = load_visual_encoder()

    print("Building fused representations for 10 sample images...")
    fused = {}
    graph_dim = None
    visual_dim = None
    for label, filename in SAMPLE_IMAGES.items():
        iri = f"{NS}PaddyDoctor_{label}_{filename.rsplit('.', 1)[0]}"
        if iri not in ent2id:
            print(f"  WARNING: {iri} not found in graph vocab, skipping")
            continue
        graph_vec = model.ent_emb.weight[ent2id[iri]].detach()
        graph_dim = graph_vec.shape[0]

        img_path = os.path.join(DATA_DIR, label, filename)
        visual_vec = extract_visual_embedding(visual_model, preprocess, img_path)
        visual_dim = visual_vec.shape[0]

        fused_vec = torch.cat([graph_vec, visual_vec])
        fused[label] = fused_vec
        print(f"  {label:25s} graph={tuple(graph_vec.shape)} visual={tuple(visual_vec.shape)} fused={tuple(fused_vec.shape)}")

    print()
    print(f"Graph embedding dim: {graph_dim}, Visual embedding dim: {visual_dim}, Fused dim: {graph_dim + visual_dim}")

    print()
    print("Cosine similarity matrix over fused vectors (10x10):")
    labels = list(fused.keys())
    vecs = torch.stack([fused[l] for l in labels])
    vecs_norm = nn.functional.normalize(vecs, dim=-1)
    sim = vecs_norm @ vecs_norm.T

    header = "                          " + " ".join(f"{l[:8]:>8s}" for l in labels)
    print(header)
    for i, l in enumerate(labels):
        row = " ".join(f"{sim[i, j].item():8.3f}" for j in range(len(labels)))
        print(f"{l:25s} {row}")


if __name__ == "__main__":
    main()
