#!/usr/bin/env python3
# k=8 pre-scan: count lemma-surviving candidates and their lcm distribution (no SAT). Split by (a,b) prefix, one process each.
import sys, math, time
from functools import reduce
K=8; bound=2**(K-1); a,b=int(sys.argv[1]),int(sys.argv[2]); CAP=float(sys.argv[3]) if len(sys.argv)>3 else 2400
def lcm(x,y): return x*y//math.gcd(x,y)
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
PP={n:ppows(n) for n in range(2,bound+1)}
def private_ok(m): return all(any(j!=i and x%q==0 for j,x in enumerate(m)) for i,n in enumerate(m) for q in PP[n])
T0=time.time(); cnt=0; surv=0; buckets={}; capped=False; out=open(f'k8_surv_{a}_{b}.txt','w')
def rec(start,ch,s):
    global cnt,surv,capped
    if capped or time.time()-T0>CAP: capped=True; return
    need=K-len(ch)
    if need==0:
        if s>1+1e-12:
            cnt+=1
            if private_ok(ch):
                surv+=1; L=reduce(lcm,ch,1); e=len(str(L)); buckets[e]=buckets.get(e,0)+1
                out.write(' '.join(map(str,ch))+f' {L}\n')
        return
    for n in range(start,bound+1):
        if s+sum(1/(n+i) for i in range(need))<=1: break
        rec(n+1,ch+[n],s+1/n)
rec(b+1,[a,b],1/a+1/b); out.close()
print(f"prefix ({a},{b}): candidates={cnt} lemma_survivors={surv} lcm_digits={dict(sorted(buckets.items()))} complete={not capped} t={time.time()-T0:.0f}s")
