# Edison p-KGFN Visualization Review — Round 1

Task ID: `72150700-00fe-47e8-902a-86b11dec49c8`

## Response


# p-KGFN Benchmark Visualization Review

## OVERALL GRADE: B-

The figures demonstrate competent software engineering and solid visual design, but the benchmark reveals a fundamental scientific issue that undermines the comparison's validity.

---

## 1. SCIENTIFIC ACCURACY — Grade: B-

**Strengths:**
- DAG topology (4 nodes, edges 0→1, 1→3, 2→3), node costs ($5, $10, $10, $45), and decision variables correctly represent the Buathong et al. 2024 manufacturing function network.
- Equal-cost budget comparison ($1,190) is methodologically correct for algorithms with heterogeneous per-iteration costs.
- Linear interpolation to a common cost grid for the cost-efficiency plot is technically sound.
- Mean ± 1 std over 5 seeds is appropriate uncertainty reporting.

**Critical Weaknesses:**
- **p-KGFN never evaluates Node 1 (Forming) or Node 3 (Testing).** Of 361 total selections across 5 seeds, 163 (45%) go to Node 0 ($5) and 198 (55%) to Node 2 ($10). Zero selections for Node 3 means p-KGFN never observes the actual objective y₃ during BO iterations. Its "best observed" value is determined entirely by the 9 initialization full-network evaluations. This is either a bug in the acquisition function or a fundamental issue that must be discussed.
- The reported "average cost/iteration = $16.5" includes amortized initialization cost ($1,189 / 72.2 = $16.47). The true marginal BO cost per iteration is (163×$5 + 198×$10) / 361 = **$7.74** — this is misleading.
- 5 seeds provides essentially zero statistical power: minimum detectable difference at 80% power ≈ 0.50, while observed max difference is 0.06 (Cohen's d ≈ 0.21).

---

## 2. VISUAL QUALITY — Grade: B+

**Strengths:**
- Consistent, professional Tufte/Doumont-inspired styling: no top/right spines, subtle gridlines (alpha=0.25), desaturated color palette, centralized rcParams.
- High DPI (180) ensures crisp rendering.
- Color-coded DAG with cost badges is informative and visually appealing.
- Convergence legend includes iteration count — very useful.

**Weaknesses:**
- **Figure 3 (Convergence):** p-KGFN's enormous pink std band (spanning ~0.35 to 0.9+) dominates the plot and makes baseline traces unreadable. Baselines are compressed into the leftmost ~10% of the x-axis.
- **Figure 2 (Cost Efficiency):** The gray Random line is nearly indistinguishable from gridlines. TSFN's std band extends above 1.0 — unclear if the objective is bounded.
- **Figure 4 (Node Selection):** Right panel (40% of width) contains only interpretive text — poor space utilization. No per-seed error bars on the bar chart.
- **Figure 1 (DAG):** Editorial callout box ("p-KGFN insight:") is promotional rather than scientific. Subtitle text partially overlaps Node 1's cost label. Aspect ratio (11×4.5) may not fit standard journal column widths.
- No panel labels (a, b, c, d) for multi-figure layouts.
- No figure numbering for cross-referencing.

---

## 3. RESULTS INTERPRETATION — Grade: C+

**Reported results:** Random=+0.67±0.27, TSFN=+0.70±0.32, pKGFN=+0.64±0.26

**The similar performance is explained by four compounding factors:**

1. **Initialization dominance:** 9 init points × $70 = $630 consumes 53% of the $1,190 budget. With only $560 for BO, all algorithms start from nearly the same information base.

2. **p-KGFN's pathological node selection:** By exclusively evaluating Nodes 0 and 2, p-KGFN never produces a new objective observation. Its 72+ partial evaluations update upstream GP posteriors but the "best observed" metric cannot improve beyond the 9 initialization evaluations. This is the primary explanation for p-KGFN's slight underperformance (−0.06 vs TSFN) and narrow std band — it literally cannot improve.

3. **Extremely low BO iteration count:** 8 full-network iterations for baselines is insufficient for any acquisition function to differentiate. Standard BO benchmarks use 50–200+ iterations.

4. **Statistical noise:** With n=5 and std≈0.28, detecting the observed 0.06 difference would require >350 seeds per group at 80% power.

**Experimental design assessment:** NOT sound for drawing conclusions. The budget is initialization-dominated, iteration counts are too low, seed count provides no statistical power, and p-KGFN's behavior suggests a potential implementation issue.

---

## 4. ACTIONABLE IMPROVEMENTS — Top 3

### 1. Fix the p-KGFN Node Selection Pathology (Critical)
p-KGFN never selects Node 3 (Testing, $45), so it never observes the objective after initialization. Either:
- (a) Debug the acquisition function — the value-of-information calculation may underestimate downstream information gain from evaluating the output node.
- (b) Add a forced periodic full-network evaluation (e.g., every K iterations).
- (c) If this is expected behavior, add a secondary metric: "posterior mean of y₃ conditioned on partial observations," since the GP posterior over Node 3 IS updated by upstream data. The "best observed" metric structurally penalizes p-KGFN when it only evaluates non-output nodes.

### 2. Increase Experimental Scale (High Impact)
- Increase seeds from 5 → 30+ (minimum for reliable mean/std; ideally 50+).
- Increase budget so initialization is <25% of total (e.g., ≥$3,500 → 9 init + ~40 full-eval baseline iterations).
- Report 95% confidence intervals, not just ±1 std.
- Add formal statistical tests (e.g., Wilcoxon signed-rank on final values across seeds).

### 3. Restructure Figure 3 (Convergence vs Iteration)
The iteration-based comparison is inherently misleading when per-iteration costs differ by ~9× ($7.74 vs $70). Either:
- Replace with a dual-panel: (a) cost-efficiency as primary, (b) inset/zoom of the $630–$900 cost range where most improvement occurs.
- Use log-scaled x-axis so 8 and 93 iterations are both visible.
- Add horizontal reference lines at initialization performance.
- Or relegate to supplementary material with an explicit caveat about non-comparable iteration costs.

**Bonus fixes:** Add panel labels; remove editorial callout boxes; add per-seed error bars to Figure 4; report marginal cost/iteration ($7.74) not amortized ($16.5); darken the Random line color.

---

## Discretionary Analytical Decisions

- **Calculated Cohen's d using pooled standard deviation across all three groups** (0.285) rather than pairwise pooled std between specific pairs, which would give slightly different values.
- **Used approximate power analysis** (Cohen's d ≈ 1.8 for n=5 at 80% power) rather than exact power computation, which would require specifying the exact test and distributional assumptions.
- **Interpreted the "average cost/iteration = $16.5" as misleading** by comparing it to the marginal per-selection cost ($7.74); an alternative view is that including amortized init cost is valid for total-cost-per-decision accounting.
- **Assessed the node selection pattern (0% for Nodes 1, 3) as "pathological"** rather than "expected behavior" — this is a judgment call since p-KGFN is designed to select cost-efficient partial evaluations, and the cheap nodes may genuinely offer higher information-per-dollar in theory. However, the fact that the algorithm never observes its own objective suggests the value calculation is not accounting for the terminal node's unique role.
- **Graded the iteration-based convergence plot (Fig 3) as potentially misleading** rather than simply informative. Some researchers would argue it valuably illustrates the per-dollar iteration advantage of partial evaluation, while others (including this review) see it as an apples-to-oranges comparison.
- **Set the threshold for "sufficient seeds" at 30+** based on central limit theorem heuristics for approximate normality of the sampling distribution; some researchers might consider 20 adequate for a preliminary benchmark.

