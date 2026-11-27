# spotcheck-q6-overview

_task_id: 92f2f351-ee50-49bb-b51d-08f42dc0f60d; status: success_

I have reviewed the 5 focused spot-check queries, the previous Edison PR and literature reviews, and the workspace source code. I performed a small 2-node p-KGFN executable smoke test to verify execution paths and cost-handling.

The overriding conclusion is that **the current pKGFN results in your benchmark artifact are completely invalid**. The attached pKGFN results are mathematically identical to the Random baseline because pKGFN experienced a 100% `error_fallback` failure rate across all iterations and seeds. The code silently reverted to random full-pipeline evaluations at $120 each. 

Consequently, any comparison of pKGFN against HighFidOnly or TSFN using this artifact is meaningless, and no claims about pKGFN's acceleration can be made to the DOE.

Here is the integrative overview.

### 1. Cross-Referenced Root Causes (Outstanding vs. Fixed)

Several seemingly distinct issues surface the same underlying statistical mechanisms.

**Root Cause A: Missing Common Random Numbers (CRN) in Inner SAA**
*   **Flagged by:** Q1 (inner SAA MC noise), Q3 (negative KG values).
*   **Code Location:** `partial_kgfn.py:33-60` (`_network_posterior_mean`).
*   **Status: OUTSTANDING.** Fix A2 removed Jensen bias but introduced fresh SAA randomness on every evaluation. Because `_network_posterior_mean` does not use paired base samples, closely competing nodes have their KG rankings shuffled by MC noise. This directly explains the small negative KG increments observed in Q1 and Q3, and it causes erratic node selection (winner's curse under cost division).
*   **To fix:** Thread a `base_samples` or fixed sampler into `_network_posterior_mean` so repeated candidate evaluations use the same integration path.

**Root Cause B: Base-Sample Dropping in QMC Network Propagation**
*   **Flagged by:** Q2 (GP network propagation), Prior Edison Review (QMC variance reduction broken).
*   **Code Location:** `gp_network.py:330-332`.
*   **Status: OUTSTANDING.** When downstream non-root nodes are sampled, the code calls `rsample` instead of `rsample_from_base_samples`. This silently breaks quasi-Monte Carlo (QMC) variance reduction for any downstream node.

**Root Cause C: Exact Latent GP Reuse at Node 2**
*   **Flagged by:** Q4 (Synthetic Problem).
*   **Code Location:** `manufacturing_problem.py:400-407`.
*   **Status: OUTSTANDING.** The current interim fix attempts to make node 2 "composition-aware" by literally re-evaluating node 0's sampled truth function `function0` on the active inputs. This makes node 2 explicitly dependent on node 0's unobserved latent state, artificially inflating parent-child dependence. Node 2 needs its own independent composition surrogate.

**Root Cause D: Near-Linear Tail Coupling / "Passthrough Domination"**
*   **Flagged by:** Q4 (Synthetic Problem), Edison y5-Review, Prior PR Review.
*   **Code Location:** `manufacturing_problem.py:355-386` (additive normalized coupling).
*   **Status: OUTSTANDING.** The additive coupling mechanism makes the tail nodes nearly deterministic functions of their parents. 98% of $y_5$ variance comes from the $y_4$ passthrough. $R^2(y_4, y_5) = 0.995$.
*   **Impact:** This linearizes the DAG in node space, which severely compresses the performance gap between DAG-aware methods (pKGFN, TSFN) and black-box methods (HighFidOnly), because a standard GP on the final objective can easily learn the near-linear terminal mapping.

**Root Cause E: Hard-coded Noiseless Fantasies**
*   **Flagged by:** Q2 (GP network propagation), Prior PR Review.
*   **Code Location:** `gp_network.py:122-126` and `partial_kgfn.py:212`.
*   **Status: OUTSTANDING.** Fantasies are drawn with `observation_noise=True` but conditioned with a hardcoded `Yvar=1e-6`. On noisy problems, this over-tightens the fantasy GPs and over-values the Knowledge Gradient.

**False Alarms (Debunked / Correct Behavior):**
*   *Cost Double-Counting:* **DEBUNKED (Q3).** Intermediate nodes are correctly charged only their marginal cost (`$45` for node 4), not the cumulative path cost.
*   *Double Standardization:* **DEBUNKED (Q2).** The BoTorch `SingleTaskGP` un-standardizes its posterior outputs correctly before they feed into downstream `Normalize` transforms.
*   *Cost Normalization / Rounding Artifacts:* **DEBUNKED (Q1, Q3).** Normalization is plain float division (`acq_val / cost`). Node-0 over-selection is caused by variance-driven winner's curse (Root Cause A), not integer rounding.

### 2. Prioritization & Expected Impact on Cost-Matched Ranking

**Current Artifact Ranking:** `HighFidOnly (17.596) ≈ TSFN (17.530) > Sobol (17.368) > Random (17.313) == pKGFN (17.313) > Node2Only (17.116) > LowFidOnly (17.023)`.
*(Note: HighFidOnly and TSFN are statistically tied; pKGFN is mathematically tied with Random).*

To flip pKGFN above HighFidOnly on the *existing* DAG, you must fix the optimization failures and variance issues:

1. **High Impact: Fix the 100% `error_fallback` crash.** pKGFN is currently not running. It is crashing inside `pkgfn_step` and defaulting to random full evaluations. The specific exception was swallowed by `bofn_actions_benchmark.py:508`, but given earlier PR notes, it is highly likely a shape mismatch in the mixed-node (node 4) reconstruction block or an OOM from the discrete candidate grids.
2. **High Impact: Implement CRN in `_network_posterior_mean`.** Once pKGFN is running again, the noisy SAA evaluations will severely degrade its ability to discriminate between low-cost nodes.
3. **Medium Impact: Fix `rsample_from_base_samples` dropping at non-root nodes.**
4. **Cosmetic/Repro: Increase the Sobol tracker grid size.** The current 200-point tracking grid is unconverged in 5D, injecting ~0.26 standard deviation noise into the final reported metrics (Q5).

### 3. Executable Smoke Test Results

I installed the requested stack (`botorch 0.17.2`, `torch 2.10.0`) and successfully exercised `PartialKnowledgeGradientFN` on a minimal 2-node mock DAG.
*   **(i) Ranking matches intuition:** Yes. Under unequal costs ($1 vs $100), the cost-adjusted KGFN correctly favored the cheap node despite the expensive node having slightly higher raw KGFN.
*   **(ii) Checkpoint matches memory:** Yes. I verified statically that `bofn_actions_benchmark.py:597-625` writes a dictionary structurally identical to the final completion dict, differing only by a `partial: True` flag which is correctly stripped at loop completion.

### 4. Recommendation for the PI (`@sgbaird-yolo`)

Before re-running the ORC sweep or citing these results for the FLAIME proposal, you must take the following steps:

1. **Top 3 Code Changes:**
   *   **Unmask the Exception:** Remove the bare `except Exception` in `bofn_actions_benchmark.py:508`. Let the benchmark crash once locally so you can see exactly why pKGFN is failing on the 6-node extended problem, then fix the underlying shape/OOM error.
   *   **Implement CRN:** Plumb `base_samples` into `_network_posterior_mean` so the SAA Monte Carlo noise does not shuffle the Knowledge Gradient rankings.
   *   **Filter partials:** Ensure `combine()` strictly filters out runs with `"partial": True`, otherwise SLURM walltime kills will bias the reported means downward.

2. **Replace the Synthetic DAG:**
   *   The current DAG is **insufficient** to demonstrate pKGFN's relative cost-efficiency. The additive passthrough creates a near-linear tail chain ($R^2=0.995$) that compresses the performance gap between DAG-aware methods (TSFN, pKGFN) and standard BO (HighFidOnly). 
   *   **Yes**, replace nodes 2/3 with an Eagar-Tsai melt-pool surrogate, and remove the explicit exact-GP-reuse at Node 2. You need a physically grounded, non-linear bottleneck in the graph to prove the value of partial evaluation.

3. **FLAIME Proposal Claims:**
   *   **You must heavily soften the proposal claims.** Claiming "≥3× AI acceleration" or "pKGFN demonstrates convergence superior to standard BO baselines" is a violation of scientific integrity given current evidence.
   *   Even before the 100% crash bug, earlier Edison post-fix projections indicated pKGFN would likely asymptote around $1.26 - 1.30$ vs TSFN at $1.35$.
   *   Reframe the proposal: Focus on the *system architecture* and the capability to execute cost-aware partial routing, citing TSFN as the reliable baseline, rather than making definitive quantitative superiority claims about pKGFN on this specific alloy testbed.

---
* Discretionary analytical decisions made during the analysis:
  * Treated the attached `bofn_actions_summary.json` as the ground-truth benchmark state for performance rankings, acknowledging that it contradicts the prompt's stated expectation (HighFid > TSFN, not TSFN > HighFid), to avoid fabricating alignment.
  * Extracted the 100% `error_fallback` rate for pKGFN dynamically from the spotcheck reports (Q3/Q5), prioritizing this catastrophic failure over statistical nuances in the final review.
  * Conducted an unpaired two-sample t-test to assess the HighFidOnly vs TSFN gap ($p=0.415$), concluding they are statistically tied at the current budget, despite the lack of seed-paired tabular data.
  * Grouped the isolated code-level findings from Q1-Q5 into 5 synthetic "Root Causes" to provide the PI with an actionable, system-level mental model rather than a disjointed line-item list.
