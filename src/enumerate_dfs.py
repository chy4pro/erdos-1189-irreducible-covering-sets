#!/usr/bin/env python3
# Independent (non-SAT) re-verification of the k<=7 enumeration: exact DFS over residues with bitmask over Z_L,
# density pruning, first residue fixed to 0. Same candidate generation + private-prime-power lemma. Internal cap.
import sys, math, time
from functools import reduce, lru_cache
K=int(sys.argv[1]); CAP=float(sys.argv[2]) if len(sys.argv)>2 else 1800
def lcm(a,b): return a*b//math.gcd(a,b)
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
@lru_cache(maxsize=None)
def can_cover(mods):
    L=reduce(lcm,mods,1); full=(1<<L)-1
    order=sorted(mods)
    masks={}
    for n in order:
        base=sum(1<<r for r in range(0,L,n))
        masks[n]=[((base<<a)&full)|(base>>(L-a)) if a else base for a in range(n)]
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
def private_ok(mods):
    return all(any(j!=i and m%q==0 for j,m in enumerate(mods)) for i,n in enumerate(mods) for q in ppows(n))
def irreducible(m): return can_cover(m) and not any(can_cover(m[:i]+m[i+1:]) for i in range(len(m)))
T0=time.time(); bound=2**(K-1); found=[]; checked=0; capped=False
def rec(start,chosen,s):
    global checked,capped
    if capped or time.time()-T0>CAP: capped=True; return
    need=K-len(chosen)
    if need==0:
        if s>1+1e-12 and private_ok(chosen):
            checked+=1
            if irreducible(tuple(chosen)): found.append(tuple(chosen))
        return
    for n in range(start,bound+1):
        if s+sum(1/(n+i) for i in range(need))<=1: break
        rec(n+1,chosen+[n],s+1/n)
assert can_cover((2,3,4,6,12)) and not can_cover((2,3,4,12)) and not can_cover((2,3,4,6))
rec(2,[],0.0)
sat=[eval(l.split(' sum=')[0]) for l in open(f'v2_results_k{K}.txt') if l.startswith('[')]
same=sorted(map(list,found))==sorted(sat)
print(f"k={K} DFS: complete={not capped} I(k)={len(found)} checked={checked} elapsed={time.time()-T0:.1f}s  AGREES_WITH_SAT={same}")
if not same: print("  DFS-only:", [f for f in found if list(f) not in sat], " SAT-only:", [s for s in sat if tuple(s) not in found])
