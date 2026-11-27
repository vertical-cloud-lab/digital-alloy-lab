# spotcheck-q4-synthetic-problem

_task_id: c1fc4e5b-f769-46ec-aeba-71d2d4107305; status: success_

I exercised the code and did a static audit. Short version: the calibration is deterministic and frozen at `__init__`, the Matheron path draw is reused consistently within a problem instance, the declared `noise_std=0.05` is applied once in the simulator and fantasy posteriors add only the GP’s learned observation noise, but the 6-node problem is still too close to a deterministic chain at the tail. Also, node 2 is not an independent root process right now; it contains an explicit transformed copy of node 0’s latent draw.

Findings, with line references:

1. `parent_bounds` wiring is internally consistent with the implemented node inputs.
- Node 4 is declared as active `x4` plus parent `y3` at `manufacturing_problem.py:197-198`, and full-network evaluation constructs `node4_in = torch.cat([X[..., [4]], output[..., [3]]], dim=-1)` at `manufacturing_problem.py:430-435`. That matches the bound order.
- Node 5 is declared as parents `(y3, y4)` at `manufacturing_problem.py:199-200`, and evaluation constructs `node5_in = torch.cat([output[..., [3]], output[..., [4]]], dim=-1)` at `manufacturing_problem.py:436-440`. That also matches.
- Those bounds are not estimated from a presample. They are hard-coded constants. What is estimated from a Sobol presample is `_parent_scales`, not `parent_bounds`.
- Consistency across train / predict / fantasy depends on those bounds being passed into the GP input normalization. In `gp_network.py:80-88` those per-node bounds feed `_initialize_gp`, and `gp_network.py:362-372` uses `Normalize(d=dim, bounds=bounds)`. So if the caller passes these `parent_bounds` into `node_input_bounds`, normalization is fixed and consistent across refits/fantasies. If not passed, it falls back to dynamic normalization.

2. `_calibrate_parent_scales` is deterministic and effectively frozen at construction.
- It is called once from `__init__` at `manufacturing_problem.py:246-247`.
- It uses a fixed Sobol seed default `seed=0` at `manufacturing_problem.py:249` and `270-272`.
- During calibration, coupling is temporarily zeroed at `263-268`, and noiseless evaluation is used at `273-279`, so calibration is based on the pure latent GP network, not noisy outputs.
- I instantiated the same problem twice with the same seed and got identical `_parent_scales` for nodes 1, 3, 4, 5. So no drift across train/eval from reconstruction alone.
- There is one code smell: the `finally` block at `282-287` checks `saved_scales` and then does nothing. It does not restore old scales. That is not breaking `__init__`, but it means a later manual call to `_calibrate_parent_scales(...)` would overwrite scales silently.

3. The Matheron path draw is reused within an instance. It is not freshly redrawn on each `evaluate()`.
- Each node function is created once and stored on `self.function0` ... `self.function5` in `_build_node_functions` at `manufacturing_problem.py:68-99` and `296-316`.
- `evaluate()` calls those stored path models directly at `123-126`, `419-440`, etc.
- I checked repeated `evaluate(..., noiseless=True)` calls on the same `ExtendedManufacturingGPNetwork` instance and got exactly identical outputs. Reconstructing a second instance with the same seed also gave exactly identical outputs.
- So the simulator “truth” is a fixed sampled function per problem instance. That part is good.
- Important caveat: the training labels for the fitted GP network are only consistent with that truth if the benchmark code reuses one problem instance when generating data. If downstream scripts reconstruct the problem object repeatedly with different seeds, then all bets are off. I did not audit those external benchmark loops here.

4. Noise model: simulator noise is applied once in `evaluate()`. Fantasy posteriors use GP observation noise, not a second explicit simulator noise injection.
- Simulator noise is added only in `_add_noise` at `manufacturing_problem.py:318-321`, and gated at the return in `464`.
- `compute_true_max` correctly bypasses noise by calling `evaluate(..., noiseless=True)` at `477-478`.
- In p-KGFN fantasies, `partial_kgfn.py:211-214` calls `posterior(..., observation_noise=True)`. That means fantasies include the GP likelihood noise of the fitted node GP.
- In `gp_network.py`, node GPs are `SingleTaskGP`s created at `367-372`, so observation noise is learned by the model from the training data; it is not hard-fixed to 0.05. The default `train_Yvar` of `1e-6` in `71-73` is mostly irrelevant unless explicitly passed through conditioning.
- So: yes, noise exists in two places conceptually, but not as the same `0.05` added twice to the same datum. The simulator adds measurement noise to observed labels; the fitted GP then learns an observation-noise term; fantasy draws include that learned noise. That is the standard setup, not obvious double-counting.

5. Node 2 currently reuses node 0’s latent draw directly. Edison’s concern was correct.
- In `_evaluate_node2`, `y2_gp` is computed from `self.function2(...)` at `manufacturing_problem.py:397`.
- Then `y0_proxy = self.function0(X[..., self.NODE2_COMPOSITION_INDICES]).detach()` at `400-402`.
- `NODE2_COMPOSITION_INDICES = [0, 1]` at `165`, which are exactly node 0’s active inputs, and node 0 itself is evaluated as `self.function0(X[..., [0, 1]])` at `419`.
- So this is not just “correlated with node 0”. It is literally the same sampled latent function `function0` evaluated on the same two coordinates. I confirmed numerically that `self.function0(X[:, [0,1]])` used for node 0 and `y0_proxy` used inside node 2 are identical pointwise.
- Current formula is `y2 = function2(process vars) + 0.25 * function0(comp vars) / scale_y0` at `397-407`.
- On a Sobol sample of 4096 points, I got:
  - `std(y2_gp_only) = 0.417`
  - `std(composition contribution) = 0.249`
  - `R²(y0, y2) = 0.265`
  So the copy is not dominant, but it is real and substantial.
- Proposed fix: give node 2 its own independent composition-conditioned latent function instead of calling `function0` directly. The cleanest minimal repair is to add a new sampled GP, e.g. `function2_comp`, over the composition coordinates and use
  `y2 = function2_proc(x2,x3) + beta * function2_comp(x0,x1)`.
  That preserves composition awareness without making node 2 partly a duplicate of node 0’s latent truth.
- If you want shared composition influence but not exact latent reuse, another option is a deterministic low-dimensional transform of composition inputs, not of `y0`, or a correlated multi-output prior if you want explicit shared structure.

6. The tail of the chain is still too near-linear in node space.
- The stored correlation summary already shows `R²(y0, y5)=0.669` and `R²(y4, y5)=0.995` in `node_correlations.json`.
- I reproduced the same qualitative result. With coupling `[0,0,0,0.5,0.8,0.7]`, I decomposed node 5 exactly as
  `y5 = function5(y3,y4) + 0.7 * mean(([y3,y4] / scale5))` using `_couple` from `manufacturing_problem.py:323-386`.
- On a 4096-point Sobol set, I got:
  - `var(y5) = 3.7394`
  - `var(function5 part) = 0.0252` which is only `0.7%` of total variance
  - `var(deterministic passthrough term) = 3.2207` which is `86.1%` of total variance
  - the covariance term contributes another `13.2%` of total variance
  - `var(pass term) + 2cov` accounts for `99.3%` of `var(y5)`
- That matches Edison’s earlier “~98% from passthrough” diagnosis. The exact split depends on whether you count shared covariance as part of the passthrough effect.
- I also observed `R²(y4, y5) = 0.994` and `R²(y3, y5) = 0.948` in one fresh run. That is a near-deterministic terminal mapping.
- Conclusion: yes, the chain is too close to linear in node space at the tail. That weakens the value of per-node decomposition because the final node is nearly recoverable from immediate upstream nodes.

7. Tiny execution smoke test for p-KGFN.
- `pip install` succeeded for `botorch==0.17.2`, `torch==2.10.0`, `gpytorch`, `numpy`, `scipy`, `matplotlib`.
- The repo snapshot in this sandbox did not include `benchmarks/partial_kgfn/dag.py`, so I could not import the package layout as-is. I created a minimal local `DAG` shim only to exercise the code paths. The audited source files themselves were not edited.
- I built a tiny 4-node ManufacturingGPNetwork smoke setup with 2 Sobol initial points, fit a `GaussianProcessNetwork`, and evaluated `PartialKnowledgeGradientFN` on a few candidates.
- Result:
  - Code ran without shape errors.
  - Training labels had expected shapes, e.g. full simulator output shape `(2, 4)`.
  - Acquisition output shape was correct, e.g. `(5,)` for 5 candidates.
  - KG values were not guaranteed non-negative in finite-sample MC use. With one inconsistent `current_value` choice they were systematically negative (~ -0.027). When I recomputed `current_value` on the same candidate grid used by the inner max, values became small and mostly non-negative, but some small negatives still appeared for some nodes due to MC approximation error.
- So the smoke outcome is: shapes match and the code runs, but “KG values monotone non-negative” is not something this implementation guarantees numerically. If you need non-negativity as a sanity condition, you should compare the fantasy value against the no-fantasy value on the exact same `X_fantasies_candidates` grid and maybe clamp tiny negatives from MC noise.

Concrete recommendations:
- Fix node 2 first. Replace direct reuse of `function0` in `manufacturing_problem.py:400-407` with an independent composition latent component.
- Reduce tail coupling, especially node 5. The current `[... ,0.8,0.7]` combined with parent-scale normalization makes node 5 almost deterministic from parents. Try lowering node 5 coupling sharply or adding more nonlinearity / larger GP variance at node 5.
- If you keep `_calibrate_parent_scales`, make the frozen-once behavior explicit. Either document it clearly or store the calibration seed as an attribute and guard against accidental recalibration.
- In benchmark code using p-KGFN, compute `current_value` on the same `X_fantasies_candidates` grid used in the inner max. Otherwise you can manufacture negative KG values for bookkeeping reasons rather than model reasons.
- Consider making node-5 passthrough exclude one parent or use a nonlinear bounded transform rather than a normalized mean, because the current additive normalized passthrough is doing most of the work.

Citations:
- Astudillo, R., & Frazier, P. I. (2021). Bayesian Optimization of Function Networks. arXiv:2112.15311.
- Buathong, P., Poloczek, M., & Frazier, P. I. (2024). Bayesian Optimization of Function Networks with Partial Evaluations. ICML. arXiv:2311.02146.
- Buathong, P., & Frazier, P. I. (2025). Fast Partial Knowledge Gradient for Function Networks. arXiv:2506.11456.

- Discretionary analytical decisions made during the analysis
- Installed the requested package versions and ran a minimal smoke test after installation succeeded, rather than stopping at static audit.
- Created a minimal local `DAG` shim solely to exercise the code because the sandbox snapshot lacked `benchmarks/partial_kgfn/dag.py`; I did not treat that shim as part of the audited source.
- Used 4096-point Sobol grids for variance and correlation spot-checks to keep runtime short while still stabilizing the estimates.
- Interpreted Edison’s “variance from passthrough” both as raw passthrough variance alone and as passthrough plus covariance with the GP term, since both are scientifically defensible decompositions and they differ materially here.
- Treated small negative p-KGFN values in smoke tests as Monte Carlo / reference-grid effects unless they were systematic under mismatched `current_value`, rather than declaring any negative value an implementation failure.
- Evaluated KG non-negativity using the same inner fantasy grid for `current_value` in a second pass, because that is the theoretically aligned comparison for knowledge-gradient sanity checking.
