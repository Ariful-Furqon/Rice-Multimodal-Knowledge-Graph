"""Where the scripts find the Rice MMKG files, given the repository root.

Two layouts are supported:
- the ontology repository, with the files at the root (`Ontology/`, `Text Modality/`);
- the benchmark repository, where the ontology repository is the git submodule `kg/`,
  pinned to the commit the experiments use.
`Data/` (gitignored) is at the root in both.
"""
from pathlib import Path


def kg_root(root):
    root = Path(root)
    return root / "kg" if (root / "kg" / "Ontology").is_dir() else root


def ontology(root):
    return kg_root(root) / "Ontology" / "Rice MMKG.rdf"


def text_module(root):
    return kg_root(root) / "Text Modality" / "RiceMMKG_IRRI_text.ttl"
