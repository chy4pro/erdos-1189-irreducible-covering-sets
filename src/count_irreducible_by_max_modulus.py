#!/usr/bin/env python3
"""Exhaustive count of irreducible covering sets with all moduli in [2, x] (x <= 24) by iterating over all subsets of
{2..x} with cheap filters (sum 1/n >= 1; private-prime-power condition), then SAT coverability and minimality
(coverability of every maximal proper subset). Usage: python3 count_bitmask.py X [SECONDS]"""
import sys, math, time, itertools
from functools import lru_cache
from pysat.solvers import Cadical153
X = int(sys.argv[1]); CAP = float(sys.argv[2]) if len(sys.argv) > 2 else 1200.0; T0 = time.time()
mods_all = list(range(2, X + 1)); N = len(mods_all)
def ppows(n):
    out = []; d = 2
    while d * d <= n:
        if n % d == 0:
            e = 1
            while n % d == 0: n //= d; e *= d
            out.append(e)
        d += 1
    if n > 1: out.append(n)
    return out
PP = {n: ppows(n) for n in mods_all}
def private_ok(mods):
    for i, n in enumerate(mods):
        for q in PP[n]:
            if not any(j != i and m % q == 0 for j, m in enumerate(mods)): return False
    return True
@lru_cache(maxsize=None)
def can_cover(mods):
    L = 1
    for n in mods: L = L * n // math.gcd(L, n)
    var = lambda i, a: 1 + sum(mods[:i]) + a
    s = Cadical153()
    for i, n in enumerate(mods):
        s.add_clause([var(i, a) for a in range(n)])
        for a in range(n):
            for b in range(a + 1, n): s.add_clause([-var(i, a), -var(i, b)])
    s.add_clause([var(0, 0)])
    for t in range(L): s.add_clause([var(i, t % n) for i, n in enumerate(mods)])
    r = s.solve(); s.delete(); return r
found = []; checked = 0; sat_calls = 0
inv = [1.0 / n for n in mods_all]
try:
    for mask in range(1, 1 << N):
        if (mask & (mask - 1)) == 0: continue
        h = 0.0; mods = []
        for i in range(N):
            if mask >> i & 1: h += inv[i]; mods.append(mods_all[i])
        if h < 1 - 1e-12 or len(mods) < 5: continue
        if not private_ok(mods): continue
        checked += 1
        if checked % 500 == 0:
            print(f"progress: survivors={checked} coverable={sat_calls} irreducible={len(found)} t={time.time()-T0:.0f}s", flush=True)
            if time.time() - T0 > CAP: raise TimeoutError
        t = tuple(mods)
        if not can_cover(t): continue
        sat_calls += 1
        if all(not can_cover(t[:i] + t[i + 1:]) for i in range(len(t))):
            found.append(t)
    status = "complete"
except TimeoutError:
    status = "INCOMPLETE (time cap)"
print(status, f"X={X} time={time.time()-T0:.0f}s private_ok-survivors={checked} coverable={sat_calls} irreducible={len(found)}")
from collections import Counter
bym = Counter(max(t) for t in found); cum = 0
for x in range(2, X + 1):
    cum += bym.get(x, 0)
    if bym.get(x, 0): print(f"x={x}: exactly-max {bym[x]}; G(x)={cum}")
print("G(%d) = %d" % (X, len(found)))
for t in sorted(found, key=lambda t: (max(t), len(t), t)): print("  ", t)
