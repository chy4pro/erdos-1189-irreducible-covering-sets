#!/usr/bin/env python3
# v2: private-prime-power pruning + multiprocessing + internal time cap.
# LEMMA (irreducibility filter, proved in engine/harvest/erdos1189_notes.md): in an irreducible covering set,
# for every modulus n_i and every prime power p^e || n_i, some OTHER modulus is divisible by p^e.
import sys, math, time, os
from functools import reduce, lru_cache
from multiprocessing import Pool
from pysat.solvers import Cadical153
K=int(sys.argv[1]); CAP=float(sys.argv[2]) if len(sys.argv)>2 else 3600.0; NPROC=int(sys.argv[3]) if len(sys.argv)>3 else 8
HERE=os.path.dirname(os.path.abspath(__file__))
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
PP={n:ppows(n) for n in range(2,2**(K-1)+1)}
def private_ok(mods):
    for i,n in enumerate(mods):
        for q in PP[n]:
            if not any(j!=i and m%q==0 for j,m in enumerate(mods)): return False
    return True
@lru_cache(maxsize=None)
def can_cover(mods):
    L=reduce(lcm,mods,1)
    off=[0]; 
    for n in mods: off.append(off[-1]+n)
    var=lambda i,a: 1+off[i]+a
    s=Cadical153()
    for i,n in enumerate(mods):
        s.add_clause([var(i,a) for a in range(n)])
        for a in range(n):
            for b in range(a+1,n): s.add_clause([-var(i,a),-var(i,b)])
    s.add_clause([var(0,0)])
    for t in range(L): s.add_clause([var(i,t%n) for i,n in enumerate(mods)])
    ok=s.solve(); s.delete(); return ok
def irreducible(mods):
    return can_cover(mods) and not any(can_cover(mods[:i]+mods[i+1:]) for i in range(len(mods)))
def work(prefix):
    T0=time.time(); bound=2**(K-1); found=[]; checked=0; pruned=0; capped=False
    def rec(start, chosen, s):
        nonlocal checked, pruned, capped
        if capped: return
        if time.time()-T0>CAP: capped=True; return
        need=K-len(chosen)
        if need==0:
            if s>1+1e-12:
                if not private_ok(chosen): pruned+=1; return
                checked+=1
                if irreducible(tuple(chosen)): found.append(tuple(chosen))
            return
        for n in range(start,bound+1):
            if s+sum(1/(n+i) for i in range(need))<=1: break
            rec(n+1, chosen+[n], s+1/n)
    rec(prefix[-1]+1, list(prefix), sum(1/n for n in prefix))
    return prefix, found, checked, pruned, capped, time.time()-T0
if __name__=='__main__':
    T=time.time(); bound=2**(K-1)
    prefixes=[(a,b) for a in range(2,bound+1) for b in range(a+1,bound+1) if 1/a+1/b+sum(1/(b+1+i) for i in range(K-2))>1]
    out=open(os.path.join(HERE,f'v2_results_k{K}.txt'),'w'); total=0; chk=0; pr=0; anycap=False
    with Pool(NPROC) as pool:
        for prefix, found, checked, pruned, capped, dt in pool.imap_unordered(work, prefixes):
            total+=len(found); chk+=checked; pr+=pruned; anycap|=capped
            for f in found: out.write(f"{list(f)} sum={sum(1/n for n in f):.6f} lcm={reduce(lcm,f,1)}\n")
            out.flush()
    out.write(f"# k={K} complete={not anycap} I(k)={total} sat_checked={chk} pruned_private={pr} prefixes={len(prefixes)} elapsed={time.time()-T:.1f}s\n"); out.close()
    print(f"k={K} complete={not anycap} I(k)={total} sat_checked={chk} pruned_private={pr} elapsed={time.time()-T:.1f}s")
