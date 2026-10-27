Coverage (main test photos; facts / facts with a linked sentence / section passages per intent)

| Target | Test photos | Fact sheet | cause | manage | identify |
|---|---:|---|---|---|---|
| Bacterial_Leaf_Blight | 97 | IRRI_RKB_bacterial-blight | 1 / 0 / 4 | 6 / 0 / 4 | 4 / 0 / 7 |
| Bacterial_Leaf_Streak | 68 | IRRI_RKB_bacterial-leaf-streak | 1 / 0 / 4 | 5 / 0 / 5 | 3 / 0 / 7 |
| Bacterial_Panicle_Blight | 61 | none | 1 / 0 / 0 | 5 / 0 / 0 | 4 / 0 / 0 |
| Brown_Planthopper | 0 | IRRI_RKB_planthopper | 0 / 0 / 4 | 3 / 0 / 10 | 2 / 0 / 4 |
| Brown_Spot | 208 | IRRI_RKB_brown-spot | 1 / 0 / 5 | 7 / 0 / 5 | 4 / 0 / 7 |
| Downy_Mildew | 125 | none | 1 / 0 / 0 | 6 / 0 / 0 | 4 / 0 / 0 |
| Hispa | 320 | IRRI_RKB_rice-hispa | 0 / 0 / 4 | 4 / 0 / 3 | 3 / 0 / 5 |
| Leaf_Folder | 156 | IRRI_RKB_rice-leaffolder | 0 / 0 / 4 | 3 / 0 / 0 | 1 / 0 / 5 |
| Leaf_Scald | 33 | none | 1 / 0 / 0 | 4 / 0 / 0 | 1 / 0 / 0 |
| Nitrogen_Deficiency_Disorder | 66 | IRRI_RKB_nitrogen | 1 / 0 / 0 | 1 / 1 / 4 | 3 / 3 / 0 |
| Normal_Health | 414 | none | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Phosphorus_Deficiency_Disorder | 50 | IRRI_RKB_phosphorus | 1 / 1 / 0 | 1 / 1 / 4 | 6 / 6 / 0 |
| Potassium_Deficiency_Disorder | 57 | IRRI_RKB_potassium-k | 1 / 1 / 0 | 1 / 1 / 4 | 6 / 6 / 0 |
| Rice_Blast_Disease | 383 | IRRI_RKB_blast-leaf-collar, IRRI_RKB_blast-node-neck | 1 / 0 / 7 | 7 / 0 / 13 | 7 / 2 / 11 |
| Rice_Tungro_Disease | 299 | IRRI_RKB_tungro | 2 / 0 / 10 | 5 / 0 / 6 | 6 / 2 / 6 |
| Sheath_Blight | 42 | IRRI_RKB_sheath-blight | 1 / 1 / 4 | 1 / 0 / 5 | 3 / 1 / 6 |
| Stem_Borer | 504 | IRRI_RKB_stem-borer | 0 / 0 / 6 | 3 / 0 / 5 | 2 / 0 / 5 |

Stage 1 R@1 on the main test subset: no_kg 0.506, kg 0.506, oracle 1.000 (KG weight 0, tuned on dev)

Stage 2, section gold

| System | Intent | n | MRR | Hit@1 | Hit@3 | Hit@10 | nDCG@10 | Recall@10 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| no_kg | cause | 2077 | 0.479 | 0.403 | 0.469 | 0.632 | 0.239 | 0.227 |
| no_kg | manage | 2094 | 0.316 | 0.225 | 0.328 | 0.493 | 0.144 | 0.132 |
| no_kg | identify | 2077 | 0.416 | 0.351 | 0.373 | 0.617 | 0.208 | 0.181 |
| kg | cause | 2077 | 0.487 | 0.418 | 0.468 | 0.631 | 0.244 | 0.230 |
| kg | manage | 2094 | 0.333 | 0.241 | 0.358 | 0.491 | 0.184 | 0.184 |
| kg | identify | 2077 | 0.478 | 0.390 | 0.494 | 0.642 | 0.244 | 0.214 |
| no_kg_stage1+kg_route | cause | 2077 | 0.487 | 0.418 | 0.468 | 0.631 | 0.244 | 0.230 |
| no_kg_stage1+kg_route | manage | 2094 | 0.333 | 0.241 | 0.358 | 0.491 | 0.184 | 0.184 |
| no_kg_stage1+kg_route | identify | 2077 | 0.478 | 0.390 | 0.494 | 0.642 | 0.244 | 0.214 |
| oracle+dense | cause | 2077 | 0.721 | 0.604 | 0.846 | 1.000 | 0.445 | 0.471 |
| oracle+dense | manage | 2094 | 0.685 | 0.638 | 0.681 | 0.759 | 0.286 | 0.207 |
| oracle+dense | identify | 2077 | 0.533 | 0.450 | 0.571 | 0.816 | 0.297 | 0.272 |
| oracle+kg_route | cause | 2077 | 0.731 | 0.624 | 0.846 | 1.000 | 0.452 | 0.476 |
| oracle+kg_route | manage | 2094 | 0.706 | 0.661 | 0.713 | 0.759 | 0.334 | 0.269 |
| oracle+kg_route | identify | 2077 | 0.757 | 0.614 | 0.900 | 1.000 | 0.406 | 0.360 |

Stage 2, fact gold

| System | Intent | n | MRR | Hit@1 | Hit@3 | Hit@10 | nDCG@10 | Recall@10 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| no_kg | cause | 149 | 0.085 | 0.000 | 0.000 | 0.544 | 0.171 | 0.544 |
| no_kg | manage | 173 | 0.094 | 0.000 | 0.000 | 0.358 | 0.154 | 0.358 |
| no_kg | identify | 897 | 0.375 | 0.315 | 0.376 | 0.470 | 0.340 | 0.426 |
| kg | cause | 149 | 0.768 | 0.765 | 0.765 | 0.765 | 0.765 | 0.765 |
| kg | manage | 173 | 0.839 | 0.838 | 0.838 | 0.838 | 0.838 | 0.838 |
| kg | identify | 897 | 0.508 | 0.475 | 0.475 | 0.593 | 0.504 | 0.548 |
| no_kg_stage1+kg_route | cause | 149 | 0.768 | 0.765 | 0.765 | 0.765 | 0.765 | 0.765 |
| no_kg_stage1+kg_route | manage | 173 | 0.839 | 0.838 | 0.838 | 0.838 | 0.838 | 0.838 |
| no_kg_stage1+kg_route | identify | 897 | 0.508 | 0.475 | 0.475 | 0.593 | 0.504 | 0.548 |
| oracle+dense | cause | 149 | 0.103 | 0.000 | 0.000 | 0.664 | 0.210 | 0.664 |
| oracle+dense | manage | 173 | 0.099 | 0.000 | 0.000 | 0.382 | 0.164 | 0.382 |
| oracle+dense | identify | 897 | 0.558 | 0.526 | 0.573 | 0.573 | 0.482 | 0.573 |
| oracle+kg_route | cause | 149 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| oracle+kg_route | manage | 173 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| oracle+kg_route | identify | 897 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
