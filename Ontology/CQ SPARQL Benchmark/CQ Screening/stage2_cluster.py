"""
Stage 2 of the CQ screening funnel: cross-model deduplication.

The five models answered one shared prompt independently, so the same
competency question recurs in different wording. This stage groups those
restatements into canonical CQs and records how many distinct models proposed
each one (n_models) -- the convergence signal Stage 5 needs.

Method (deliberately dependency-free and fully described, so the paper can
state it exactly). Two independent similarity signals are computed and a merge
is proposed only where BOTH exceed their threshold:
  A. Wording. TF-IDF over question tokens plus "Key Entities & Relations"
     tokens (the latter weighted x2), L2-normalised, cosine similarity. A
     domain synonym map folds label variants onto one token (Magnaporthe /
     Pyricularia / rice blast -> blast; symptom / lesion / sign -> symptom).
  B. Requirement signature. Jaccard overlap of the normalised set of classes
     and properties named in the entities cell. Two statements of one
     requirement share presupposed vocabulary even when their wording diverges.
Clustering is agglomerative with AVERAGE linkage -- single linkage chains
unrelated CQs through one accidental bridge -- and is confined within a
category, so a text CQ and an image CQ are never merged.

KNOWN LIMITATION, stated because it governs how the output must be used.
Automatic clustering is triage here, not measurement. These CQs share domain
vocabulary heavily (disease, pathogen, symptom occur almost everywhere), so
both signals conflate requirements that are genuinely distinct: at every cut
tried, "what pathogen causes blast" and "what symptoms are reported for blast"
land together. Thresholds are therefore set to favour precision, which leaves
paraphrases unmerged; n_models from this script is a LOWER BOUND on
convergence, not a measurement of it. The manual pass over
cq_stage2_borderline.csv is required, not optional polish.

As in Stage 1 this script decides nothing. Clusters are proposals and the
adjudication columns are blank.

Outputs (in this directory):
  cq_stage2_clusters.csv     one row per CQ, with its proposed cluster
  cq_stage2_canonical.csv    one row per cluster, with n_models
  cq_stage2_borderline.csv   near-miss pairs for manual review
  cq_stage2_proposal.md      method, counts, and the convergent clusters
"""

import csv
import re
import math
import datetime
import collections
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
POOL = SCRIPT_DIR / "cq_pool_stage0.csv"

# A merge is proposed only when both signals clear their threshold.
TAU_COSINE = 0.40
TAU_JACCARD = 0.40
# Any unmerged same-category pair clearing either of these goes to manual review.
BORDERLINE_COSINE = 0.28
BORDERLINE_JACCARD = 0.30
ENTITY_WEIGHT = 2.0

STOP = set("""a an the of for in on at to and or is are was were which what who when how do
does did with by from that this these those given each any all some its their there be been
being as if per over under within into can could may might will would shall should must not
no than then also more most least very such other others between among across during after
before""".split())

# Label variants folded onto one token. Order matters: species names first.
SYNONYMS = [
    (r"\b(?:magnaporthe|pyricularia)\b", "blast"),
    (r"\brice blast\b|\bblast\b", "blast"),
    (r"\bxanthomonas oryzae pv\.? oryzicola\b|\bbacterial leaf streak\b|\bbls\b",
     "bacterialleafstreak"),
    (r"\bxanthomonas\b|\bbacterial leaf blight\b|\bbacterial blight\b|\bblb\b",
     "bacterialleafblight"),
    (r"\brhizoctonia\b|\bsheath blight\b", "sheathblight"),
    (r"\bbipolaris\b|\bbrown spot\b", "brownspot"),
    (r"\btungro\b|\brtbv\b|\brtsv\b", "tungro"),
    (r"\bnilaparvata\b|\bbrown planthopper\b|\bbph\b|\bhopperburn\b", "brownplanthopper"),
    (r"\bscirpophaga\b|\bstem borer\b|\bdeadheart\b|\bwhite ?ear\b", "stemborer"),
    (r"\bnephotettix\b|\bleafhopper\b", "leafhopper"),
    (r"\bsymptoms?\b|\blesions?\b|\bsigns?\b", "symptom"),
    (r"\bpathogens?\b|\bcaus\w+ agents?\b", "pathogen"),
    (r"\bcausedby\b|\bcauses?\b|\bcausal\b|\bcausative\b", "cause"),
    (r"\bvarieties\b|\bvariety\b|\bcultivars?\b", "variety"),
    (r"\bimages?\b|\bphotos?\b|\bphotographs?\b|\bimagery\b", "image"),
    (r"\bsensors?\b|\biot\b|\btelemetry\b", "sensor"),
    (r"\bgrowth ?stages?\b|\bphenolog\w+\b", "growthstage"),
    (r"\btreatments?\b|\bcontrol measures?\b|\bmanagement practices?\b", "treatment"),
    (r"\bresistance ?genes?\b|\bgenes?\b|\bqtl\b|\bloci\b|\blocus\b", "gene"),
    (r"\btaxonom\w+\b", "taxon"),
    (r"\bliterature\b|\bpublications?\b|\bbulletins?\b", "literature"),
    (r"\bdiseases?\b", "disease"),
    (r"\bpests?\b", "pest"),
    (r"\bplant parts?\b|\borgans?\b", "plantpart"),
]


def tokens(text):
    s = re.sub(r"[*_`]", " ", text.lower())
    for pat, rep in SYNONYMS:
        s = re.sub(pat, rep, s)
    return [t for t in re.findall(r"[a-z]+", s) if t not in STOP and len(t) > 2]


def entity_tokens(text):
    s = re.sub(r"\(align[^)]*\)", "", text, flags=re.I)
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", s)      # split camelCase properties
    return tokens(s)


def vectorise(rows):
    docs = []
    for r in rows:
        c = collections.Counter(tokens(r["question"]))
        for t in entity_tokens(r["entities"]):
            c[t] += ENTITY_WEIGHT
        docs.append(c)
    vocab = {}
    for d in docs:
        for t in d:
            vocab.setdefault(t, len(vocab))
    n = len(docs)
    df = np.zeros(len(vocab))
    for d in docs:
        for t in d:
            df[vocab[t]] += 1
    idf = np.log((n + 1) / (df + 1)) + 1
    M = np.zeros((n, len(vocab)))
    for i, d in enumerate(docs):
        for t, f in d.items():
            M[i, vocab[t]] = (1 + math.log(f)) * idf[vocab[t]]
    M /= (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
    return M


def jaccard_matrix(rows):
    """Overlap of the normalised class/property sets each CQ presupposes."""
    sigs = [set(entity_tokens(r["entities"])) for r in rows]
    n = len(sigs)
    J = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if sigs[i] and sigs[j]:
                v = len(sigs[i] & sigs[j]) / len(sigs[i] | sigs[j])
                J[i, j] = J[j, i] = v
    return J


def average_linkage(S, tau):
    """Agglomerative clustering with average linkage, cut at tau."""
    n = S.shape[0]
    clusters = {i: [i] for i in range(n)}
    while len(clusters) > 1:
        best, pair = -np.inf, None
        keys = sorted(clusters)
        for ai in range(len(keys)):
            for bi in range(ai + 1, len(keys)):
                a, b = keys[ai], keys[bi]
                v = S[np.ix_(clusters[a], clusters[b])].mean()
                if v > best:
                    best, pair = v, (a, b)
        if pair is None or best < tau:
            break
        a, b = pair
        clusters[a] = clusters[a] + clusters[b]
        del clusters[b]
    return list(clusters.values())


def main():
    assert POOL.exists(), f"run stage0 first: {POOL} missing"
    rows = list(csv.DictReader(POOL.open(encoding="utf-8-sig")))
    M = vectorise(rows)
    C = M @ M.T
    np.fill_diagonal(C, 0.0)
    J = jaccard_matrix(rows)

    # Agreement score: >= 1 exactly when both signals clear their threshold, so
    # the linkage cut is a plain 1.0 and each signal keeps its own scale.
    S = np.minimum(C / TAU_COSINE, J / TAU_JACCARD)

    cats = np.array([r["category"] for r in rows])
    assignment = {}
    cid = 0
    for cat in sorted(set(cats)):
        idx = [i for i in range(len(rows)) if cats[i] == cat]
        sub = S[np.ix_(idx, idx)]
        for members in average_linkage(sub, 1.0):
            cid += 1
            for m in members:
                assignment[idx[m]] = cid

    clusters = collections.defaultdict(list)
    for i, c in assignment.items():
        clusters[c].append(i)

    # Representative = member with the highest mean similarity to its cluster.
    canonical = {}
    for c, members in clusters.items():
        if len(members) == 1:
            canonical[c] = members[0]
        else:
            sub = S[np.ix_(members, members)]
            canonical[c] = members[int(np.argmax(sub.mean(axis=1)))]

    for i, r in enumerate(rows):
        c = assignment[i]
        members = clusters[c]
        r["cluster_id"] = f"C{c:03d}"
        r["cluster_size"] = len(members)
        r["n_models"] = len({rows[m]["source_model"] for m in members})
        r["is_representative"] = "yes" if canonical[c] == i else ""
        r["cluster_members"] = " ".join(rows[m]["pool_id"] for m in members)
        r["merge_ok"] = ""        # adjudication: blank on purpose
        r["split_into"] = ""
        r["notes"] = ""

    fields = ["pool_id", "cluster_id", "cluster_size", "n_models",
              "is_representative", "source_model", "original_id", "category",
              "complexity", "question", "cluster_members", "merge_ok",
              "split_into", "notes"]
    with (SCRIPT_DIR / "cq_stage2_clusters.csv").open(
            "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows({k: r[k] for k in fields} for r in rows)

    cfields = ["cluster_id", "category", "n_models", "cluster_size", "models",
               "representative_pool_id", "representative_question",
               "cluster_members", "confirmed", "notes"]
    canon_rows = []
    for c in sorted(clusters):
        members = clusters[c]
        rep = rows[canonical[c]]
        canon_rows.append({
            "cluster_id": f"C{c:03d}",
            "category": rep["category"],
            "n_models": len({rows[m]["source_model"] for m in members}),
            "cluster_size": len(members),
            "models": "; ".join(sorted({rows[m]["source_model"] for m in members})),
            "representative_pool_id": rep["pool_id"],
            "representative_question": rep["question"],
            "cluster_members": " ".join(rows[m]["pool_id"] for m in members),
            "confirmed": "",
            "notes": "",
        })
    canon_rows.sort(key=lambda r: (-r["n_models"], r["category"], r["cluster_id"]))
    with (SCRIPT_DIR / "cq_stage2_canonical.csv").open(
            "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cfields)
        w.writeheader()
        w.writerows(canon_rows)

    # Near-miss pairs: same category, not merged, but one signal says look.
    border = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if cats[i] != cats[j] or assignment[i] == assignment[j]:
                continue
            if C[i, j] >= BORDERLINE_COSINE or J[i, j] >= BORDERLINE_JACCARD:
                border.append((round(float(max(C[i, j], J[i, j])), 3),
                               round(float(C[i, j]), 3),
                               round(float(J[i, j]), 3), rows[i], rows[j]))
    border.sort(key=lambda x: -x[0])
    with (SCRIPT_DIR / "cq_stage2_borderline.csv").open(
            "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["max_signal", "cosine", "jaccard", "category",
                    "pool_id_a", "model_a", "question_a",
                    "pool_id_b", "model_b", "question_b",
                    "should_merge", "notes"])
        for _, c_, j_, a, b in border:
            w.writerow([max(c_, j_), c_, j_, a["category"],
                        a["pool_id"], a["source_model"], a["question"],
                        b["pool_id"], b["source_model"], b["question"], "", ""])

    dist = collections.Counter(r["n_models"] for r in canon_rows)
    L = ["# Stage 2 - Cross-model Deduplication (proposal)", "",
         f"Generated {datetime.datetime.now():%Y-%m-%d %H:%M} by "
         "`stage2_cluster.py` from `cq_pool_stage0.csv`.", "",
         f"**In:** {len(rows)} CQs &nbsp;&nbsp; **Out:** {len(canon_rows)} "
         "canonical CQs (provisional) &nbsp;&nbsp; **Merge rule:** cosine >= "
         f"{TAU_COSINE} AND Jaccard >= {TAU_JACCARD}, average linkage, within "
         "category.", "",
         "> **Read this before using the numbers.** Automatic clustering is "
         "triage, not measurement. These CQs share domain vocabulary heavily, "
         "so both signals conflate genuinely distinct requirements -- at every "
         "cut tried, *what pathogen causes blast* and *what symptoms are "
         "reported for blast* land in one cluster. Thresholds therefore favour "
         "precision, which leaves paraphrases unmerged. **`n_models` below is "
         "a lower bound on convergence, not a measurement of it**, and the "
         "manual pass over `cq_stage2_borderline.csv` is required rather than "
         "optional.", "",
         "Clusters are proposals. `merge_ok` in `cq_stage2_clusters.csv` and "
         "`confirmed` in `cq_stage2_canonical.csv` are blank.", "",
         "## Convergence: how many models proposed each canonical CQ", "",
         "| Models agreeing | Canonical CQs |", "|---|---|"]
    for k in sorted(dist, reverse=True):
        L.append(f"| {k} | {dist[k]} |")
    L += ["",
          "A CQ proposed independently by several models is evidence that it "
          "is a natural requirement of the domain rather than one model's "
          "invention. Stage 5 must nevertheless keep some n_models = 1 CQs in "
          "the questionnaire, or the hypothesis that convergence predicts "
          "expert-rated relevance cannot be tested.", "",
          "## Canonical CQs proposed by two or more models", ""]
    for r in canon_rows:
        if r["n_models"] < 2:
            continue
        L += [f"**{r['cluster_id']}** &middot; {r['category']} &middot; "
              f"**{r['n_models']} models** ({r['cluster_size']} CQs: "
              f"{r['cluster_members']})", "",
              f"> {r['representative_question']}", ""]
    L += ["## Borderline pairs for manual review", "",
          f"{len(border)} same-category pairs were left unmerged although one "
          f"signal flagged them (cosine >= {BORDERLINE_COSINE} or Jaccard >= "
          f"{BORDERLINE_JACCARD}). Each row in `cq_stage2_borderline.csv` "
          "carries both scores and a blank `should_merge` column. This list is "
          "where the convergence count actually gets settled.", ""]

    (SCRIPT_DIR / "cq_stage2_proposal.md").write_text("\n".join(L),
                                                      encoding="utf-8")
    print(f"in: {len(rows)}  canonical: {len(canon_rows)}  "
          f"borderline pairs: {len(border)}")
    for k in sorted(dist, reverse=True):
        print(f"  n_models={k}: {dist[k]}")


if __name__ == "__main__":
    main()
