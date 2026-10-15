# Edison p-KGFN Visualization Review — Round 2

Task ID: `62018f47-9d97-4773-a633-1d8ee7b27609`
Elapsed: 154s

## Changes Applied

Round 2 review of p-KGFN benchmark figures. Changes from Round 1 (B-):
- Darkened Random line color (#546E7A vs #90A4AE)
- Added panel labels (a), (b), (c) 
- Removed editorial callout box from DAG
- Added init cost reference line ($630) on cost efficiency plot
- Y-axis relabeled "GP posterior mean" (clarifying tracking method)
- Convergence plot now shows marginal cost/iteration in legend
- Node selection panel reports marginal cost ($7.7/iter) not amortized ($16.5)
- Cost analysis notes Node 1/3 posteriors updated indirectly via DAG

Evaluate: Did the changes address Round 1 issues? What remains for publication readiness? Grade A-F.

## Response


# Round 2 Review: p-KGFN Benchmark Figures

## Grade: B

**Improvement from Round 1: B- → B (clear, meaningful progress)**

---

## Round 1 Change Verification (7/8 fully addressed, 1 partial)

| # | Requested Change | Status |
|---|---|---|
| 1 | Darkened Random line color | ✅ Fully addressed — darker blue-grey, clearly distinct from TSFN |
| 2 | Added panel labels (a), (b), (c) | ✅ Fully addressed — all three results panels labeled |
| 3 | Removed editorial callout from DAG | ✅ Fully addressed — clean schematic |
| 4 | Added init cost reference line ($630) | ⚠️ Partially — "Init $630" text exists but is small, grey, at plot edge; no actual vertical reference line drawn |
| 5 | Y-axis relabeled "GP posterior mean" | ✅ Fully addressed — reads "Best network output (GP posterior mean)" |
| 6 | Convergence legend shows marginal cost/iter | ✅ Fully addressed — legend entries include iter count and $/iter |
| 7 | Node selection reports marginal cost ($7.7) | ✅ Fully addressed — "p-KGFN: 7.7±2.5" in cost analysis box |
| 8 | Node 1/3 posteriors updated indirectly noted | ✅ Fully addressed — explicit statement in cost analysis box |

---

## Remaining Issues

### Critical (must fix before publication)

**C1. Iteration count discrepancy between panels (b) and (c).**
Panel (b) legend says "pKGFN (93 iters, ~$8/iter)" but panel (c) implies ~72 partial evaluations per seed (361 total selections / 5 seeds = 72.2). If 93 includes initialization evaluations, this must be clarified. If these are different quantities, the labeling is confusing. Budget arithmetic: $630 init + 72 × $7.7 ≈ $1,184 (close to stated $1,189), but $630 + 93 × $7.7 ≈ $1,346 (exceeds budget). This factual inconsistency must be resolved.

**C2. The init cost reference in panel (a) is effectively invisible.**
At publication print scale, the small grey "Init $630" text in the lower-left corner will be illegible. A proper vertical dashed line with annotation is needed.

**C3. pKGFN variance band is enormous and undermines the central visual comparison.**
The ±1 std band for pKGFN spans roughly 0.38–0.90 throughout panels (a) and (b), far wider than the baselines. With only 5 seeds, the pKGFN mean (~0.64) is actually *lower* than TSFN (~0.68) and comparable to Random (~0.66) at the same total budget in the cost-equalized panel (a). Either: (i) run more seeds to tighten the bands, (ii) report median ± IQR for robustness, or (iii) explicitly frame the advantage as exploratory efficiency rather than performance superiority, and note the high variance as a limitation in the figure caption.

### Moderate (should fix for final version)

**M1. Budget inconsistency: $1,190 (panel a) vs $1,189 (panel c).** Pick one and use it consistently.

**M2. Panel (b) iteration-axis comparison is inherently misleading.** Plotting 93 pKGFN iterations alongside 8 baseline iterations on the same x-axis, despite 9× cost differences, visually overstates pKGFN's advantage. The subtitle caveat helps but should be more prominent, or consider an inset/dual-axis.

**M3. Node selection bar totals need clarification.** 163 + 198 = 361 across 5 seeds; adding "(summed across 5 seeds)" to the y-axis or annotation would prevent confusion.

**M4. Confidence bands exceed [0,1].** If the GP posterior mean is a bounded output, clip bands to valid range. If unbounded, note this.

### Minor (polish)

- m1. DAG lacks a panel label; if part of a composite figure, add one (e.g., panel d).
- m2. pKGFN hot pink/magenta is visually dominant; consider a more muted color for journal aesthetics.
- m3. Cost analysis box uses monospace font, clashing with other panels' font family.
- m4. Panel (b) two-line title is heavy; move parenthetical details to figure caption.

---

## Numerical Cross-Checks

- DAG total: $5 + $10 + $10 + $45 = $70/full eval ✅ (matches legend)
- Init cost: $630 / $70 = 9 full initialization evaluations (plausible) ✅
- Marginal cost: 0.45×$5 + 0.55×$10 = $7.75 ≈ $7.7 ✅
- Baseline budget: $630 + 8×$70 = $1,190 ✅
- pKGFN budget: $630 + 72×$7.7 ≈ $1,184 (close to $1,189) ✅, but $630 + 93×$7.7 ≈ $1,346 ❌ (exceeds budget → 93 iters is inconsistent)

---

## Path to A-Range

1. Resolve the 93-vs-72 iteration discrepancy (critical factual error)
2. Make the init cost reference visually prominent (dashed vertical line)
3. Unify budget figure ($1,190 vs $1,189)
4. Address the high variance: more seeds, alternative summary statistics, or explicit caption discussion
5. Minor polish items above

---

## Discretionary Analytical Decisions

- Treated the DAG schematic as a separate reference figure rather than requiring a panel label, since it is not a results panel
- Evaluated the init cost annotation as "partially addressed" rather than "not addressed" because the text is present even though no reference line is drawn
- Verified cost arithmetic using weighted average of node costs (0.45×$5 + 0.55×$10) rather than simple average, based on observed selection frequencies
- Flagged the 93-vs-72 iteration discrepancy as critical rather than moderate, because it affects budget arithmetic and core claims
- Assessed the wide variance band as a critical issue based on the observation that pKGFN mean performance does not exceed baselines in the cost-equalized comparison (panel a)
- Graded at B rather than B+ because the iteration count discrepancy represents a new factual inconsistency not present in Round 1

