"""Computational verification of the combinatorial claims in
``composition-scaling-analysis.md``.

Setup (same as the document)
----------------------------
* Palette: Al + P=15 non-Al elements.
* Resolution: 1 at.% steps.
* Al-rich constraint: Al >= 85 at.%, so the minor-element budget is
  sum_{i in S} x_i <= 15 at.%.
* For a fixed support pattern S of size k (k of the 15 non-Al slots):

  - *strict* compositions require x_i >= 1 for every i in S (``‖x_S‖_0 = k``)
  - *loose*  compositions allow  x_i >= 0 for every i in S (includes
    degenerate lower-support compositions)

Closed-form claims
------------------
* Per pattern, strict: N_strict(k) = C(15, k)      [via stars-and-bars with
  substitution z_i = x_i - 1, slack y_0 = 15 - sum(x), giving k+1 non-negative
  variables summing to 15-k, i.e. C((15-k)+(k+1)-1, (k+1)-1) = C(15, k)].
* Per pattern, loose: N_loose(k) = C(15 + k, k).
* Total strict (union over patterns of size k, disjoint supports):
  N_total_strict(k) = C(15, k) * C(15, k) = C(15, k)^2.
* Global feasible region, union over k = 2..8 (disjoint support sizes):
  sum_{k=2}^{8} C(15, k)^2 = 118,967,759 (~119 M).
* Vandermonde / hockey-stick cross-check:
  sum_{k=0}^{15} C(15, k)^2 = C(30, 15) = 155,117,520.

Running this file
-----------------
``python edison-trajectories/composition-scaling-verify.py`` reproduces all
the numbers in the headline table of ``composition-scaling-analysis.md``
and compares brute-force enumeration against the closed forms for small k.
"""

from __future__ import annotations

import itertools
from math import comb

P = 15      # non-Al palette size
BUDGET = 15 # (100 - 85) at.% budget at 1 at.% resolution


def strict_per_pattern_enum(k: int, budget: int = BUDGET) -> int:
    """Count strict compositions (x_i >= 1 for all i in the k-slot support).

    Enumerates integer tuples (x_1, ..., x_k) with x_i >= 1 and sum(x) <= budget.
    """
    count = 0

    def rec(i: int, remaining: int) -> None:
        nonlocal count
        if i == k:
            count += 1
            return
        max_val = remaining - (k - 1 - i)  # leave at least 1 for each remaining slot
        for v in range(1, max_val + 1):
            rec(i + 1, remaining - v)

    rec(0, budget)
    return count


def loose_per_pattern_enum(k: int, budget: int = BUDGET) -> int:
    """Count loose compositions (x_i >= 0 for the k-slot support)."""
    count = 0

    def rec(i: int, remaining: int) -> None:
        nonlocal count
        if i == k:
            count += 1
            return
        for v in range(0, remaining + 1):
            rec(i + 1, remaining - v)

    rec(0, budget)
    return count


def main() -> None:
    print(f"Palette non-Al size P = {P}, minor-element budget = {BUDGET} at.% (1 at.% steps)\n")

    # Per-pattern verification
    print("Per-pattern counts (one fixed support pattern of size k):")
    header = f"{'k':>3}  {'strict_enum':>12}  {'C(15,k)':>10}  {'loose_enum':>12}  {'C(15+k,k)':>12}  {'strict':>7}  {'loose':>6}"
    print(header)
    all_ok = True
    for k in range(1, 9):
        s_enum = strict_per_pattern_enum(k)
        l_enum = loose_per_pattern_enum(k)
        s_cf = comb(P, k)
        l_cf = comb(P + k, k)
        ok_s = s_enum == s_cf
        ok_l = l_enum == l_cf
        all_ok &= ok_s and ok_l
        print(
            f"{k:>3}  {s_enum:>12}  {s_cf:>10}  {l_enum:>12}  {l_cf:>12}  "
            f"{'OK' if ok_s else 'FAIL':>7}  {'OK' if ok_l else 'FAIL':>6}"
        )

    # End-to-end: enumerate (support, composition) pairs for small k
    print("\nGlobal strict totals, brute-forced over all patterns (tractable for k<=4):")
    print(f"{'k':>3}  {'total_enum':>12}  {'C(15,k)^2':>12}  {'match':>6}")
    for k in range(1, 5):
        total = 0
        for _ in itertools.combinations(range(P), k):
            total += strict_per_pattern_enum(k)
        cf = comb(P, k) ** 2
        all_ok &= total == cf
        print(f"{k:>3}  {total:>12}  {cf:>12}  {'YES' if total == cf else 'NO':>6}")

    # Binomial decomposition: loose(k) = sum_s C(k, s) * strict(s)
    print("\nConsistency: loose(k) = sum_{s=0..k} C(k,s) * strict(s)")
    for k in range(1, 9):
        lhs = loose_per_pattern_enum(k)
        rhs = sum(
            comb(k, s) * (strict_per_pattern_enum(s) if s > 0 else 1)
            for s in range(0, k + 1)
        )
        all_ok &= lhs == rhs
        print(f"  k={k}: loose={lhs}, sum_decomp={rhs}  {'OK' if lhs == rhs else 'MISMATCH'}")

    # Headline table reproduction
    print("\nHeadline table (matches composition-scaling-analysis.md):")
    print(f"{'k':>3}  {'C(15,k)':>8}  {'strict = C(15,k)^2':>20}  {'old (loose overcount) = C(15,k)C(23..,k)':>44}")
    for k in range(2, 9):
        strict = comb(P, k) ** 2
        loose_over = comb(P, k) * comb(P + k, k)
        print(f"{k:>3}  {comb(P,k):>8,}  {strict:>20,}  {loose_over:>44,}")

    total_strict_2_8 = sum(comb(P, k) ** 2 for k in range(2, 9))
    print(f"\nUnion over k=2..8 (strict, disjoint support sizes): {total_strict_2_8:,}")

    # Vandermonde identity cross-check
    vander_cf = comb(2 * P, P)
    vander_enum = sum(comb(P, k) ** 2 for k in range(0, P + 1))
    print("\nVandermonde / hockey-stick cross-check:")
    print(f"  sum_{{k=0..{P}}} C({P},k)^2 = {vander_enum:,}")
    print(f"  C({2*P},{P})              = {vander_cf:,}")
    all_ok &= vander_cf == vander_enum

    # At k=8: overcount ratio
    print("\nAt k=8:")
    k = 8
    print(f"  C(15,8)          = {comb(P, k):,}")
    print(f"  C(15,8)^2        = {comb(P, k)**2:,}  (strict, ~41.4 M)")
    print(f"  C(15,8) * C(23,8)= {comb(P, k) * comb(P + k, k):,}  (old loose, ~3.16 B)")
    print(f"  Overcount ratio  = {comb(P, k) * comb(P + k, k) / comb(P, k)**2:.1f}x")

    print("\nAll checks passed." if all_ok else "\nSOME CHECKS FAILED — see output above.")
    raise SystemExit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
