# Symptom controlled vocabulary — for annotation_sample.csv

For each row in `reports/annotation_sample.csv`, fill `symptom_iris` with one
or more of the IRIs below (semicolon-separated for multiple symptoms visible
in one image). If the image shows a genuine symptom not covered by any of
these 11 terms, use the escape value `OTHER` instead of forcing it into the
nearest existing term, and note what you saw in a separate column/comment —
this surfaces real gaps in the vocabulary rather than hiding them.

| Label | IRI |
|---|---|
| Brown Lesion | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Brown_Lesion` |
| Chewed Leaf | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Chewed_Leaf` |
| Deadheart | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Deadheart` |
| Dry Leaf Tip | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Dry_Leaf_Tip` |
| Empty Grain | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Empty_Grain` |
| Hopper Burn | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Hopper_Burn` |
| Leaf Rolling | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Leaf_Rolling` |
| Leaf Spot | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Leaf_Spot` |
| Stem Rot Symptom | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Stem_Rot_Symptom` |
| Wilting | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Wilting` |
| Yellow Leaf | `http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#Yellow_Leaf` |
| *(not listed)* | `OTHER` — escape value, do not force into an existing term |

Images annotated `normal` (healthy) in `ground_truth_label` should generally
get an empty `symptom_iris` — there is no symptom to capture.
