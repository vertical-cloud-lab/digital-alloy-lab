# Edison response: bofn-pkgfn-implementation-spotcheck-vs-published-papers

- Task ID: `7b1ba7ec-65b7-4ea9-a00b-61471c2fd5ad`
- Status: `success`

---

I have reviewed your implementation of the extended Manufacturing DAG benchmark, the `partial_kgfn` module, and the baseline loops. Comparing your code against the original Buathong et al. (2024, 2025) papers and the `frazier-lab/partial_kgfn` repository, I found several important deviations, subtle gotchas, and correctness concerns.

Here is the itemized review based on your questions:

### 1. Cost Normalization in the Acquisition Step
**Gotcha:** Your implementation correctly normalizes by cost, but it does so in the outer loop, **exactly matching the upstream reference implementation**.
In `bofn_pkgfn_demo.py` (lines 287-296), you compute `cost_adjusted = acq_val / problem.node_costs[k]`. This matches `run_one_trial.py` in the `frazier-lab` repo, which divides the node's best KG value by its cost *after* the inner optimization finishes. The original `PartialKnowledgeGradientFN.forward()` intentionally ignores the `cost_aware_utility` argument and expects the caller to handle cost. So your cost-amortization is structurally correct.

### 2. Parent Sampling for KG (Reachable Manifold)
**Gotcha:** You are using a "reachable manifold" heuristic (`bofn_pkgfn_demo.py` lines 103-187) that the upstream implementation does **not** use, and it introduces a dangerous bias.
- The original ICML 2024 code enforces an `impose_assump=True` flag where parent candidates are strictly restricted to the discrete Cartesian product of *previously evaluated* parent outputs (via `retrieve_available_evaluations`). It does not sample the unobserved manifold.
- Your code constructs a "reachable manifold" by propagating a Sobol design grid through the `node.posterior(X).mean` of each GP (line 160). But because you use the posterior *mean*, you are sampling a deterministically collapsed skeleton of the parent space. You never query parent `y` values in the high-variance tails where the GP is uncertain, which starves the inner KG of exploration value on downstream nodes. If you want to sample the true unobserved manifold, you must use Thompson-style path draws (`get_matheron_path_model`) to sample parent outputs, not `posterior.mean`.

### 3. Inner-KG Quadrature (Posterior Mean Propagation)
**Gotcha (Critical):** Your inner KG computation uses a biased, deterministic forward pass instead of the upstream Monte Carlo integration.
- In `partial_kgfn.py` (lines 33-82), `_network_posterior_mean` propagates `model.node_GPs[k].posterior(X_k).mean` step-by-step through the DAG. You are computing $g(\mathbb{E}[f(x)])$.
- Because the downstream functions are nonlinear, Jensen's inequality guarantees $g(\mathbb{E}[f(x)]) \neq \mathbb{E}[g(f(x))]$.
- The upstream code computes `values = self.inner_sampler(fantasy_post_at_X)` and averages over `n_SAA` (Sample Average Approximation) MC samples drawn from the fantasy network posterior. By discarding the inner MC sampler and using deterministic means, you drastically underestimate uncertainty in the inner maximization, making your KG values artificially brittle.

### 4. Per-node GP Fits: Transforms and Conditioning
**Gotcha (Critical Bug):** There is a hidden inconsistency between how your code and BoTorch handle input normalization during fantasy conditioning.
- In `gp_network.py` (lines 124-126), your comment states: `"Do NOT call transform_inputs() here — condition_on_observations() applies the input transform internally..."`.
- I ran a live check in BoTorch 0.17.2: conditioning on raw un-transformed inputs using `SingleTaskGP` *does* correctly auto-apply the transform. Your local fix is **correct** for modern BoTorch.
- However, your fantasy observations (`partial_kgfn.py` lines 229-230) do **not** include observation noise. `post_k = self.model.node_GPs[k].posterior(x_i)` yields a noiseless posterior. Upstream explicitly passes `observation_noise=True` to `fantasize()`. Because your problem now includes `noise_std=0.05`, your KG outer expectation is drawing noiseless fantasies, causing pKGFN to over-value observations.

### 5. Node 4/5 Bounds and Wiring
**Gotcha:** The wiring in `manufacturing_problem.py` is correct, but the GP bounds-handling masks a scaling issue.
- Node 4's input is correctly wired as `[active_x4, parent_y3]` in both problem evaluation and `construct_obs_set`.
- However, your `_initialize_gp` (lines 326-342) initializes `Normalize(d=dim)` without passing explicit bounds. It therefore infers bounds dynamically from the `train_X` min/max. Because `train_X` for Node 4 contains `y3` values (which can drift from roughly `[-2, 2]` up to `[-4, 4]` as you sample extreme points), the normalization bounds for the Node 4 GP shift on every iteration. This causes non-stationary lengthscale learning. You should pass explicit known bounds to `Normalize`.

### 6. DAG Coupling Artifact
**Gotcha:** Your additive parent passthrough makes the DAG trivially linear.
- You specified `coupling=[0,0,0,0.6,0.8,0.7]` with variance normalization. Edison warned this makes `y5` nearly deterministic.
- This **does** bias the ranking. Because `y5` is essentially a linear sum of `y3` and `y4`, the complex network factorization of BOFN is overkill. A vanilla `HighFidOnly` GP on `y5` will easily learn the smooth, near-linear macro-function. By making the problem too easy for a standard GP, you compress the performance gap between pKGFN and the baselines, artificially deflating pKGFN's relative advantage.

### 7. Cost Accounting
**Gotcha:** Your accounting correctly avoids double-billing for downstream partial evaluations.
- In `bofn_pkgfn_demo.py` (lines 423-435), when a partial evaluation queries an intermediate node, it feeds the `node_input` (which contains the selected parent candidate) directly to `problem.evaluate(idx=[node_selected])`. It updates only that node's `train_X` and charges only that node's cost. You are not accidentally running or billing the upstream nodes.

### 8. Random/Sobol Baseline Fairness
**Gotcha:** Standard protocol requires full-pipeline evaluations for standard baselines.
- Your baselines (`Random`, `Sobol`, `HighFidOnly`) are forced to evaluate the full pipeline ($120) and get ~20 iterations, while pKGFN gets ~68 iterations heavily weighted toward cheap nodes (averaging ~$35/iter). This is the exact premise of the ICML 2024 paper. The cost convention is correct and fair for evaluating cost-amortized acquisition against vanilla BO.

### Summary of required fixes before submission:
1. Re-introduce `observation_noise=True` when drawing fantasy `y` values in `PartialKnowledgeGradientFN.forward`.
2. Replace `_network_posterior_mean` with MC sample-average approximation (SAA) integration over the inner network posterior to avoid Jensen-inequality bias.
3. Pass explicit `bounds` to `Normalize` in `_initialize_gp` to prevent normalization drift on intermediate nodes.
4. Replace the linear-additive `_couple` passthrough with a nonlinear surrogate (e.g. Eagar-Tsai) to restore the problem difficulty and allow BOFN/pKGFN to demonstrate their true advantage over vanilla `HighFidOnly`.

***

- Discretionary analytical decisions made during the analysis:
  - Re-implemented and tested BoTorch `condition_on_observations` behavior locally in the workspace to verify whether the upstream pre-transform or the local raw-input approach was correct for modern BoTorch 0.17+ (concluding the local raw-input approach was correct).
  - Traced the cost of pKGFN node selections using the raw `pkgfn-fant64-*` JSON files to verify that pKGFN was successfully amortizing budget (finding an average step cost of ~$35 vs the $120 full pipeline).
  - Assessed the impact of the `_network_posterior_mean` propagation theoretically (Jensen's inequality bias) rather than running a full regression benchmark, as the structural deviation from upstream's MC sampler was definitively clear.
  - Determined that dynamic `Normalize` bounds on intermediate GPs constitute a risk of non-stationary learning, choosing to flag this as a required fix rather than a harmless BoTorch default.