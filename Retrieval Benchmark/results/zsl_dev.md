Generalized zero-shot, leave one condition out, dev main subset. Unseen metrics are the mean over the 16 held-out conditions (each condition weighted equally); the unseen class competes with the 16 seen ones, without calibration. Chance MRR over 17 classes is 0.202. 3 seeds for trained methods. KG vectors: 108 features. Script: `scripts/dev_checks/zsl_dev.py`.

| Method | Unseen R@1 | Unseen R@3 | Unseen MRR | Seen R@1 |
|---|---:|---:|---:|---:|
| zero-shot label-text | 0.066 | 0.173 | 0.206 | 0.124 |
| zero-shot kg-text | 0.071 | 0.240 | 0.225 | 0.109 |
| kg | 0.000 | 0.066 | 0.156 | 0.597 |
| kg-shuffled | 0.000 | 0.013 | 0.129 | 0.600 |
| label-text | 0.001 | 0.231 | 0.176 | 0.594 |
| kg-text | 0.023 | 0.161 | 0.181 | 0.558 |
| kg + label | 0.000 | 0.146 | 0.167 | 0.601 |

**Unseen MRR per held-out condition:**

| Condition | n | zero-shot label-text | zero-shot kg-text | kg | kg-shuffled | label-text | kg-text | kg + label |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bacterial_Leaf_Blight | 83 | 0.119 | 0.079 | 0.163 | 0.138 | 0.144 | 0.166 | 0.156 |
| Bacterial_Leaf_Streak | 46 | 0.166 | 0.088 | 0.130 | 0.109 | 0.288 | 0.301 | 0.157 |
| Bacterial_Panicle_Blight | 62 | 0.104 | 0.081 | 0.114 | 0.100 | 0.097 | 0.077 | 0.116 |
| Brown_Spot | 209 | 0.598 | 0.242 | 0.197 | 0.145 | 0.116 | 0.194 | 0.180 |
| Downy_Mildew | 125 | 0.146 | 0.506 | 0.152 | 0.117 | 0.115 | 0.118 | 0.146 |
| Hispa | 323 | 0.165 | 0.204 | 0.142 | 0.114 | 0.184 | 0.170 | 0.146 |
| Leaf_Folder | 162 | 0.125 | 0.062 | 0.164 | 0.185 | 0.204 | 0.208 | 0.176 |
| Leaf_Scald | 33 | 0.126 | 0.257 | 0.106 | 0.087 | 0.177 | 0.450 | 0.113 |
| Nitrogen_Deficiency_Disorder | 66 | 0.110 | 0.122 | 0.202 | 0.176 | 0.314 | 0.246 | 0.306 |
| Normal_Health | 459 | 0.665 | 0.128 | 0.120 | 0.120 | 0.088 | 0.082 | 0.115 |
| Phosphorus_Deficiency_Disorder | 50 | 0.134 | 0.075 | 0.237 | 0.109 | 0.321 | 0.188 | 0.308 |
| Potassium_Deficiency_Disorder | 57 | 0.118 | 0.081 | 0.240 | 0.117 | 0.322 | 0.264 | 0.281 |
| Rice_Blast_Disease | 386 | 0.117 | 0.358 | 0.122 | 0.161 | 0.122 | 0.117 | 0.119 |
| Rice_Tungro_Disease | 255 | 0.210 | 0.234 | 0.128 | 0.118 | 0.105 | 0.114 | 0.110 |
| Sheath_Blight | 42 | 0.309 | 0.510 | 0.150 | 0.131 | 0.083 | 0.099 | 0.105 |
| Stem_Borer | 524 | 0.080 | 0.578 | 0.130 | 0.139 | 0.130 | 0.096 | 0.133 |
