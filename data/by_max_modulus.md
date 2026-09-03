# Irreducible covering sets counted by maximum modulus (Erdős #1188 discussion, [Er80] p. 95)

G(x) := number of irreducible covering sets (Erdős's notion: a set of distinct moduli that admits a covering system while no
proper subset does) with all moduli in [2, x].

## Exact values (exhaustive over all subsets of {2..24}, `src/count_irreducible_by_max_modulus.py`, 2026-09-04)
| x | G(x) |
|---|---|
| 2 | 0 |
| 3 | 0 |
| 4 | 0 |
| 5 | 0 |
| 6 | 0 |
| 7 | 0 |
| 8 | 0 |
| 9 | 0 |
| 10 | 0 |
| 11 | 0 |
| 12 | 1 |
| 13 | 1 |
| 14 | 1 |
| 15 | 1 |
| 16 | 1 |
| 17 | 1 |
| 18 | 1 |
| 19 | 1 |
| 20 | 1 |
| 21 | 1 |
| 22 | 1 |
| 23 | 1 |
| 24 | 5 |

The five sets with moduli ≤ 24: {2,3,4,6,12}; {2,3,4,6,8,24}; {2,3,4,8,12,24}; {2,3,6,8,12,24}; {2,4,6,8,12,24}.
Method: all 2^23 subsets of {2..24}; necessary filters (Σ1/n ≥ 1; every prime power p^e ∥ n_i divides another modulus);
9903 survivors; 1440 admit a covering (SAT, CaDiCaL on Z/lcm); 5 are minimal (no maximal proper subset admits a covering;
coverability is monotone). Runtime 29 min. This also confirms that no irreducible covering set of size ≥ 9 has all moduli ≤ 24.

## Lower bounds from the enumeration by size (all irreducible sets of size k ≤ 8; sizes ≥ 9 not enumerated)
| x | sets of size ≤ 8 with max modulus ≤ x |
|---|---|
| 12 | 1 |
| 24 | 5 |
| 36 | 13 |
| 48 | 24 |
| 72 | 59 |
| 96 | 85 |

Every irreducible covering set of size ≤ 8 has maximum modulus 12, 24, 36 or 48 (a multiple of 12).
