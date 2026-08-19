# Task 2.2 — vector/pathogen notes (Checkpoint C6)

`reports/vector_todo.csv` lists all 6 `Pest` individuals with empty
`transmits_pathogen` / `source_citation` columns. None were filled in —
vector–pathogen relationships require literature verification and were not
guessed, per the worklog's explicit instruction.

**Rice tungro disease is the motivating case, and it needs a new individual
first.** Rice tungro is caused by two viruses (Rice Tungro Bacilliform Virus
and Rice Tungro Spherical Virus) transmitted by the green leafhopper
(*Nephotettix virescens* and related species). **Neither the viruses nor the
leafhopper currently exist as individuals in this ontology** — `Pathogen`
has only `Magnaporthe_Oryzae`, `Xanthomonas_Oryzae`, `Bipolaris_Oryzae`, and
`Pest` has no leafhopper. Before `transmits` can be asserted for the tungro
case:

1. A new `Pest` individual for the leafhopper vector needs to be created (not done here — out of scope for this script, and the exact species-level identity needs literature confirmation).
2. New `Pathogen` individual(s) for the tungro virus/viruses need to be created.
3. Only then can `transmits` be asserted from the leafhopper to the virus pathogen(s), and `causes` from the virus to `Rice_Tungro_Disease`.

None of this was done. `scripts/apply_vectors.py` will refuse to assert a
`transmits` triple against any pathogen local name not already declared in
the ontology — it will not create one from a bare CSV string, since that
would mean guessing the pathogen's identity.
