#!/usr/bin/env python3
# Irreducibility pass (DFS/bitmask engine, independent of SAT) over one survivor file. Internal cap.
import sys, math, time
from functools import reduce, lru_cache
fn=sys.argv[1]; CAP=float(sys.argv[2]) if len(sys.argv)>2 else 2400
def lcm(a,b): return a*b//math.gcd(a,b)
@lru_cache(maxsize=None)
def can_cover(mods):
    L=reduce(lcm,mods,1); full=(1<<L)-1; order=sorted(mods); masks={}
    for n in order:
        base=sum(1<<r for r in range(0,L,n)); masks[n]=[((base<<a)&full)|(base>>(L-a)) if a else base for a in range(n)]
    dens=[1/n for n in order]; suf=[sum(dens[j:]) for j in range(len(order)+1)]
    def dfs(j,cov):
        if cov==full: return True
        if j==len(order): return False
        if (L-bin(cov).count('1'))/L > suf[j]+1e-12: return False
        n=order[j]; seen=set()
        for a in ([0] if j==0 else range(n)):
            nc=cov|masks[n][a]
            if nc in seen: continue
            seen.add(nc)
            if dfs(j+1,nc): return True
        return False
    return dfs(0,0)
T0=time.time(); found=[]; n=0; capped=False
for line in open(fn):
    if time.time()-T0>CAP: capped=True; break
    p=list(map(int,line.split())); m=tuple(p[:-1]); n+=1
    if can_cover(m) and not any(can_cover(m[:i]+m[i+1:]) for i in range(len(m))): found.append(m)
out=open(fn.replace('k8_surv_','k8_irr_'),'w')
for f in found: out.write(f"{list(f)} sum={sum(1/x for x in f):.6f} lcm={reduce(lcm,f,1)}\n")
out.write(f"# file={fn} checked={n} irreducible={len(found)} complete={not capped} t={time.time()-T0:.0f}s\n"); out.close()
print(f"{fn}: checked={n} irreducible={len(found)} complete={not capped} t={time.time()-T0:.0f}s")
