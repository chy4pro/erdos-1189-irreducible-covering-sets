# Irreducible covering sets of size k ≤ 8 (Erdős Problem #1189)

**Definitions.** A finite set of integers 1 < n_1 < … < n_k is a *covering set* if residues a_i can be chosen so that
every integer satisfies x ≡ a_i (mod n_i) for at least one i. It is *irreducible* if no proper subset is a covering set
(Erdős, 1980; see [erdosproblems.com/1189](https://www.erdosproblems.com/1189)). Note the difference from a *minimal
covering system*: the modulus set of a minimal covering system need not be irreducible, because a proper subset might
cover with *different* residues.

**Results (exhaustive, machine-verified).** Let I(k) be the number of irreducible covering sets of size k.

| k | I(k) | min n_k | max n_k | Simpson bound 2^(k−1) | max Σ 1/n_i | lcm range |
|---|---|---|---|---|---|---|
| ≤4 | 0 | – | – | – | – | – |
| 5 | 1 | 12 | 12 | 16 | 4/3 | 12..12 |
| 6 | 4 | 24 | 24 | 32 | 17/12 | 24..24 |
| 7 | 15 | 36 | 48 | 64 | 35/24 | 36..48 |
| 8 | 65 | 36 | 96 | 128 | 14/9 | 72..96 |

- I(k) = 0, 0, 0, 0, 1, 4, 15, 65 for k = 1..8. The unique irreducible covering set of size 5 is {2, 3, 4, 6, 12}.
- Every irreducible covering set with k ≤ 8 contains the modulus 2, and Simpson's bound n_k ≤ 2^(k−1) is never attained
  for 6 ≤ k ≤ 8.
- The full lists, each with an explicit covering witness (residues), are in `data/`.

**Lemma (no private prime power).** In an irreducible covering set, for every modulus n_i and every prime power
p^e exactly dividing n_i, some *other* modulus is divisible by p^e.

*Proof.* Suppose p^e ∥ n_i and v_p(n_j) ≤ e−1 for all j ≠ i. Let U be the union of the classes a_j (mod n_j), j ≠ i;
U contains every integer not ≡ a_i (mod p^e). Take x ≡ a_i (mod p^e), put m = ∏_{j≠i} n_j / p^{v_p(n_j)} (coprime to
p) and x' = x + p^{e−1} m. Then x' ≡ x modulo n_j / p^{v_p(n_j)} and modulo p^{e−1} for every j ≠ i, while
x' ≢ a_i (mod p^e). So x' ∈ U, i.e. x' ≡ a_j (mod n_j) for some j ≠ i, and since n_j divides x' − x, also
x ≡ a_j (mod n_j). Hence the classes j ≠ i already cover ℤ, contradicting irreducibility. ∎

**Method.** Simpson (1985) proved n_k ≤ 2^(k−1) for irreducible covering sets, and Σ 1/n_i > 1 is necessary for
distinct moduli, so each I(k) is a finite computation. We enumerate all k-sets satisfying both, discard those violating
the lemma above (for k = 8 this cuts ≈ 2.2 × 10^9 candidates to ≈ 2.2 × 10^6), decide coverability exactly
(SAT via CaDiCaL/python-sat, and independently an exact DFS over residue choices with density pruning), and test
irreducibility on the k subsets of size k−1. For k ≤ 7 the SAT and DFS enumerations were run in full and agree
set-for-set; for k = 8 the DFS enumeration was run in full and the SAT engine re-confirmed all 65 positives and a random
sample of 3000 negatives.

**Reproduce / verify.**
```
python3 src/verify_witnesses.py           # standard library only: checks every listed set (witness covers, no proper
                                          # subset covers, lemma holds); exit code 0 iff all pass
python3 src/enumerate_dfs.py 7            # re-enumerate k=7 from scratch (≈30 s); k=8: see prescan_k8_*.py + irreducibility_dfs.py
python3 src/enumerate_sat.py 7 3600 8     # SAT-based enumeration (needs python-sat)
```

**References.** P. Erdős, problems in *Combinatorial number theory* (1980), p. 95; T. Bloom, Erdős Problem #1189,
erdosproblems.com/1189; R. J. Simpson, *Regular coverings of the integers by arithmetic progressions*, Acta Arith. 45
(1985); Z.-W. Sun, on irreducible covering sets formed by divisors (2007); P. Balister, B. Bollobás, R. Morris,
J. Sahasrabudhe, M. Tiba, on the number of minimal covering systems (2024).

Produced by an automated AI mathematics pipeline (chy4pro). Everything needed to re-verify or falsify the tables is in
this repository.


## Addendum (2026-09-04): counting by maximum modulus (Erdős Problem #1188 discussion)
Erdős [Er80, p. 95] also asked to estimate the number of irreducible covering sets with all moduli in [1, x]. Exhaustively
over all subsets of {2..24}: the count is 0 for x < 12, 1 for 12 ≤ x < 24, and 5 for x = 24 (no irreducible set of size ≥ 9
has all moduli ≤ 24). From the enumeration by size (k ≤ 8) the counts are at least 13, 24, 59, 85 for x = 36, 48, 72, 96.
See `data/by_max_modulus.md` and `src/count_irreducible_by_max_modulus.py`.

## Status note (2026-09-04): k = 9 not enumerated
An attempt to extend the enumeration to k = 9 with the same program (`irreducible_covering_sets_v2.py 9 18000 6`, six worker processes) found
9 irreducible covering sets in about six hours of wall time before its time limit, far from completion; the partial list is not included
and no value of I(9) is claimed. A different algorithm (e.g. modulus-set pruning by the 2-adic and 3-adic structure) would be needed.
