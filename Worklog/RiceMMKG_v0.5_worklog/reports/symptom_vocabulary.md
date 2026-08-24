# Symptom vocabulary for expert annotation (Task B.3)

The 28 `rice:Symptom` individuals currently in the ontology, for the
annotator to pick from when completing `reports/annotation_sample.csv`.
Put one or more of the identifiers below (the bold code, not the label)
into the `symptom_iris` column, semicolon-separated for multiple symptoms
visible in one image.

**If none of these 28 fit what you see in the image, do not force a
match** — write `OTHER: <your own short description>` in the
`symptom_iris` cell instead. That is the explicit escape this vocabulary
needs: forcing an annotator to pick the closest existing term would
silently hide real gaps in symptom coverage rather than surface them.

| Code | Label | Description |
|---|---|---|
| `Brown_Leaf_Tip` | brown leaf tip | Browning confined to leaf tips; occurs in hispa damage where larvae mine leaf tissue. |
| `Brown_Lesion` | Brown Lesion | *(no description on record)* |
| `Chewed_Leaf` | Chewed Leaf | *(no description on record)* |
| `Dead_Tiller` | dead heart | Central tiller dies and turns brown while surrounding tillers remain green; caused by stem borer larva cutting internal stem tissue at vegetative stage. |
| `Deadheart` | Deadheart | Paddy Doctor includes this as an image class. It remains a Symptom in the ontology, rather than being incorrectly promoted to a Disease. |
| `Discolored_Panicle` | discolored panicle | Browning or blackening of panicle rachis and grains; caused by *Burkholderia glumae* in bacterial panicle blight. |
| `Dry_Leaf_Tip` | Dry Leaf Tip | *(no description on record)* |
| `Empty_Grain` | Empty Grain | Grain that fails to fill (chaffy grain); a primary yield loss symptom in bacterial panicle blight. |
| `Excessive_Tillering` | excessive tillering | Abnormally high number of thin, erect tillers; 'crazy top' appearance caused by *Sclerophthora macrospora*. |
| `Grain_Discoloration` | grain discoloration | Brown to black discoloration of individual grains; associated with bacterial panicle blight and fungal diseases. |
| `Hopper_Burn` | Hopper Burn | *(no description on record)* |
| `Leaf_Rolling` | Leaf Rolling | *(no description on record)* |
| `Leaf_Scratching` | leaf scratching | Irregular scratching damage on upper leaf surface; characteristic of hispa (*Dicladispa armigera*) adult feeding. |
| `Leaf_Spot` | Leaf Spot | *(no description on record)* |
| `Neck_Rot` | neck rot | Rotting of the panicle neck caused by *Magnaporthe oryzae*; leads to empty or partially filled grain. |
| `Panicle_Blast` | panicle blast | Brown to grayish lesion at the base of panicle (neck), causing partial or complete panicle death; a severe form of rice blast. |
| `Reduced_Tillering` | reduced tillering | Fewer tillers produced than in healthy plants; associated with tungro and stem borer damage. |
| `Stem_Rot_Symptom` | Stem Rot Symptom | *(no description on record)* |
| `Sterile_Panicle` | sterile panicle | Panicles that fail to set grain; result of downy mildew infection at reproductive stage. |
| `Stunted_Growth` | stunted growth | Reduction in plant height; a hallmark of tungro infection in early growth stages. |
| `Translucent_Stripe` | translucent stripe | Narrow translucent stripes on leaves, later turning yellow-brown with wavy margins; diagnostic for bacterial leaf streak. |
| `Water_Soaked_Streak` | water-soaked streak | Initial water-soaked, translucent streaks on leaves between veins; early symptom of bacterial leaf streak. |
| `White_Ear` | white ear | Panicle that emerges white and sterile because stem borer larva has cut the stem internally at reproductive stage. |
| `White_Streak` | white streak | White or silvery linear marks on leaf surface caused by hispa beetle scraping the leaf epidermis. |
| `Wilting` | Wilting | *(no description on record)* |
| `Yellow_Leaf` | Yellow Leaf | *(no description on record)* |
| `Yellow_Orange_Discoloration` | yellow-orange leaf discoloration | Characteristic yellowing-to-orange discoloration of leaves in rice tungro disease. |
| `Yellow_Stripe` | yellow stripe | Yellow to pale-green stripes running parallel to leaf veins; characteristic of downy mildew (crazy top). |

**Observation, not a Task B.3 action item:** `Dead_Tiller` ("dead heart")
and `Deadheart` are two separate individuals describing what reads as the
same visible symptom, distinguished only by `Deadheart`'s comment noting
it exists because Paddy Doctor uses it as an image-class label. Worth a
modelling decision at some point (merge, like `Stem_Borer` /
`Scirpophaga_Incertulas` in Task A.2, or keep separate and say why) — not
resolved here since it isn't one of the six worklog tasks and touches the
same `captures`/`indicatedBy` assertions this task is trying to grow, not
shrink.
