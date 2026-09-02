#!/usr/bin/env python3
"""Independent verification of data/irreducible_covering_sets_k5_k8.json (standard library only).
For every listed set: (1) the given residues cover every integer (checked modulo lcm); (2) no proper subset of
the moduli is a covering set (exact DFS over residue choices with density pruning); (3) the private-prime-power
lemma holds. Exit code 0 iff everything checks."""
import json, math, sys, os
from functools import reduce, lru_cache
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
def ppows(n):
    out=[]; d=2
    while d*d<=n:
        if n%d==0:
            e=1
            while n%d==0: n//=d; e*=d
            out.append(e)
        d+=1
    if n>1: out.append(n)
    return out
here=os.path.dirname(os.path.abspath(__file__))
data=json.load(open(os.path.join(here,'..','data','irreducible_covering_sets_k5_k8.json')))
bad=0
for o in data:
    m=tuple(o['moduli']); r=o['residues']; L=reduce(lcm,m,1)
    covers=all(any((t-a)%n==0 for a,n in zip(r,m)) for t in range(L))
    irreducible=not any(can_cover(m[:i]+m[i+1:]) for i in range(len(m)))
    lemma=all(any(j!=i and x%q==0 for j,x in enumerate(m)) for i,n in enumerate(m) for q in ppows(n))
    if not (covers and irreducible and lemma): bad+=1; print("FAIL", o)
counts={}
for o in data: counts[o['k']]=counts.get(o['k'],0)+1
print("sets verified:", len(data), "per k:", counts, "failures:", bad)
sys.exit(1 if bad else 0)
