import json,sys,math,hashlib,collections,numpy as np,rdflib
sys.path.insert(0,"Retrieval Benchmark/scripts")
from step2_rerank import R,label,sign_flip
SP=sys.argv[1]
recs=[json.loads(x) for x in open(SP+"/verify_dev.jsonl",encoding="utf-8")]
g=rdflib.Graph();g.parse("Data/retrieval/RiceMMKG_query_time.ttl")
ents=None
TRIAL={"Rice_Blast_Disease":["spindle-shaped or diamond-shaped lesion, pointed at both ends"],"Brown_Spot":["circular to oval lesion"]}
base={}
for e,_ in g.subject_objects(R.indicatedBy): base.setdefault(str(e).split("#")[-1],set())
for e in base: base[e]={label(g,s) for s in g.objects(R[e],R.indicatedBy)}
def yes(r):
    a=r["answers"] or {}
    return {x for k,x in enumerate(r["items"],1) if a.get(str(k)) is True}
print("parsed",np.mean([r["answers"] is not None for r in recs]),"mean yes share",np.mean([len(yes(r))/max(len(r["items"]),1) for r in recs]))
def run(proto,trial):
    sym={e:set(v)|set(TRIAL.get(e,[]) if trial else []) for e,v in base.items()}
    df=collections.Counter(s for v in sym.values() for s in v);n=len(sym)
    idf={s:math.log(n/c)+1e-3 for s,c in df.items()}
    data=[]
    for r in recs:
        if proto not in r["candidates"]:continue
        c=r["candidates"][proto];s=np.array(r["stage1"][proto]);y=yes(r);act=[v for v in r["stage1"][proto]]
        z={};fin=s[np.isfinite(s)]
        data.append((r,c,fin,y))
    def rr(lam,sub):
        out=[]
        for r,c,fin,y in sub:
            allv=dict(zip(range(len(r["stage1"][proto])),r["stage1"][proto]))
            order=sorted(allv,key=lambda k:-allv[k])[:3]
            m,sd=fin.mean(),fin.std()
            sc=[]
            anyyes=sum(idf.get(x,0) for x in y if any(x in sym.get(e,()) for e in c))
            for e,k in zip(c,order):
                ss=sym.get(e,set());t=sum(idf[x] for x in ss if x in y)/max(sum(idf[x] for x in ss),1e-9) if ss else (1.0 if anyyes==0 else 0.0)
                sc.append((allv[k]-m)/sd+lam*t)
            new=[c[i] for i in np.argsort(-np.array(sc))]
            out.append(1 if new[0]==r["gold"] else 0)
        return np.array(out)
    a=[d for d in data if int(hashlib.md5(d[0]["image"].encode()).hexdigest(),16)%2==0]
    b=[d for d in data if int(hashlib.md5(d[0]["image"].encode()).hexdigest(),16)%2==1]
    res=[]
    for tune,conf in ((a,b),(b,a)):
        L=(0,.5,1,2,3,5,8)
        lam=max(L,key=lambda l:(rr(l,tune).mean(),-l))
        res.append((lam,rr(0,conf).sum(),rr(lam,conf).sum(),len(conf)))
    tot=[sum(x[i] for x in res) for i in (1,2,3)]
    print(proto,"trial" if trial else "KG only",[x[0] for x in res],"stage1 R@1",round(tot[0]/tot[2],3),"verify",round(tot[1]/tot[2],3),"n",tot[2])
for p in ("in-source","cross-source"):
    run(p,False);run(p,True)
hit=collections.defaultdict(lambda:[0,0])
for r in recs:
    y=yes(r)
    for e in ("Rice_Blast_Disease","Brown_Spot"):
        for t in TRIAL[e]:
            if t in r["items"]:
                k=("gold" if r["gold"]==e else "other",t[:12]);hit[k][0]+=t in y;hit[k][1]+=1
print({k:v for k,v in hit.items()})
