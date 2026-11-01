import csv,json,sys,collections,urllib.request
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root/"Retrieval Benchmark/scripts"))
from step2_vlm_triples import image_b64,OLLAMA,VLM
from step2_rerank import SINGLE_SOURCE
gold={r["image"]:r["gold"] for r in csv.DictReader((root/"Retrieval Benchmark/splits/gold.csv").open(encoding="utf-8"))}
rows=[r for r in csv.DictReader((root/"Retrieval Benchmark/splits/dev_core.csv").open(encoding="utf-8")) if r["dataset"] not in SINGLE_SOURCE and gold[r["image"]] in("Rice_Blast_Disease","Brown_Spot")]
P='Look at the lesions on this rice leaf. What is the main lesion shape? Reply with JSON only: {"shape": "spindle"} for long lesions pointed at both ends (diamond-like), {"shape": "round"} for circular to oval spots, {"shape": "none"} if no lesion is visible.'
c=collections.Counter()
for r in rows:
    body={"model":VLM,"stream":False,"format":"json","options":{"temperature":0,"seed":0,"num_predict":30},"messages":[{"role":"user","content":P,"images":[image_b64(root/r["url"])]}]}
    req=urllib.request.Request(OLLAMA,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
    raw=json.load(urllib.request.urlopen(req,timeout=300))["message"]["content"]
    try:s=str(json.loads(raw).get("shape"))
    except Exception:s="bad"
    c[(gold[r["image"]],s)]+=1
print(len(rows));[print(k,v) for k,v in sorted(c.items())]
b=c[("Rice_Blast_Disease","spindle")];bn=sum(v for k,v in c.items() if k[0]=="Rice_Blast_Disease")
s=c[("Brown_Spot","round")];sn=sum(v for k,v in c.items() if k[0]=="Brown_Spot")
print("blast spindle",b,bn,"brown round",s,sn,"balanced",round((b/bn+s/sn)/2,3))
