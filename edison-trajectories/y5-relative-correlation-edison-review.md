# Edison Review: y5-Relative Node Correlation Fix

- **Task ID**: `84928290-3424-4e99-b7f5-6607c95aa549`
- **Job**: `job-futurehouse-data-analysis-crow-high`
- **Submitted**: 2026-04-30T09:20:54Z
- **Retrieved**: 2026-04-30T18:10:00Z (approx)
- **Status**: `success`
- **Addresses**: PR comment 4351069085 (sgbaird-yolo: "y2->y3 R^2 unacceptable; report relative to final node; use edison")

## Query (excerpt)

We just revised the synthetic BOFN benchmark DAG after reviewer/PI feedback. The requirement is that correlations be measured relative to the final node y5, not only immediate parent-child edges. Earlier nodes y0/y1/y2 should each have R^2 to y5 in roughly the 0.6-0.75 range, while middle/late nodes y3/y4 should be higher. The previous version had y2->y3 R^2 around 0.29 and y2->y5 around 0.27, which was unacceptable.

Current interim fix in ExtendedManufacturingGPNetwork:
- keep node0 cost at $5 (avoid extreme cheap-root pKGFN bog-down)
- make node2 (LPBF-in/process root) composition-aware by giving it active inputs [x0,x1,x2,x3] and adding a modest normalized node0/CALPHAD composition gate with node2_composition_coupling=0.25
- keep per-node coupling [0,0,0,0.6,0.8,0.7]
- normalize parent passthrough scales and weight node3 parent passthrough [y1,y2]=[0.8,1.0]

New noiseless Sobol R^2 results (n=4096, seed=0):
- y0 -> y5: 0.669
- y1 -> y5: 0.750
- y2 -> y5: 0.667
- y3 -> y5: 0.978
- y4 -> y5: 0.995
- diagnostic edge y2 -> y3: 0.707

Please review this as an interim synthetic benchmark fix. Questions:
1. Is making LPBF-in node2 composition-aware a reasonable proxy for real LPBF Al-alloy printability/processing response, given that processability depends on composition/CALPHAD descriptors as well as scan parameters?
2. Is the R^2 hierarchy (early y0/y1/y2 to final y5 in 0.6-0.75, middle/late higher) plausible for a benchmark intended to build confidence before FLAIME deployment, or should the early band be lower/higher?
3. Does the weighted additive passthrough introduce any benchmark artifact that would unfairly favor pKGFN over TSFN/HighFidOnly?
4. What physics surrogate should replace this interim composition gate in the next version (e.g., Eagar-Tsai melt-pool or Kou hot-cracking/freezing-range terms), and which public Al LPBF data should calibrate it?
5. Any concrete code-level concerns in manufacturing_problem.py / bofn_node_correlations.py that would invalidate the interpretation of the R^2 grid?

## Answer

Short version: the interim fix does solve the reviewer-facing problem you named. The y5-relative hierarchy now matches the intended story: y0/y1/y2 each carry substantial terminal information, and y3/y4 are stronger. The specific Sobol-grid values reproduce exactly from the current code: R²(y0,y5)=0.669, R²(y1,y5)=0.750, R²(y2,y5)=0.666, R²(y3,y5)=0.978, R²(y4,y5)=0.995, with diagnostic R²(y2,y3)=0.707.

But there is one important caveat: the current additive, variance-normalized passthrough makes the downstream chain very close to deterministic linear readout in node space. In my audit, about 97.9% of var(y5) is coming from the node-5 passthrough term rather than the node-5 GP residual, and a joint linear fit of y5 on just (y0,y1,y2) already gives R²=0.980. Likewise y3 is almost a linear function of (y1,y2): joint linear R²=0.999. So this is acceptable as an interim benchmark repair, but it is not yet a physics-grounded surrogate. The artifact risk is less “this unfairly favors pKGFN specifically” and more “this makes the DAG too linear in node space.”

1. Is making LPBF-in node2 composition-aware reasonable?

Yes, as an interim proxy, this is reasonable.

Why it passes the smell test:
- LPBF processability in Al alloys is not a pure scan-parameter problem. It depends on alloy thermodynamics and solidification behavior: freezing range, crack susceptibility, absorptivity-related behavior, oxide behavior, vaporization losses, and melt-pool stability all depend on composition.
- Using shared composition/CALPHAD coordinates between y0 and y2 is directionally right. It removes the old pathology where LPBF-in was effectively an independent root unrelated to the final property.
- Your current gate is modest, not dominant at node 2. In the current realization, R²(y0,y2)=0.262, so the composition gate is present but not overwhelming.

What it is not:
- It is not yet a mechanistic LPBF surrogate. Right now node2 is still a legacy 2-D GP in process space plus a normalized y0 proxy term. That is a statistical coupling device, not a melt-pool or cracking model.
- Using y0 itself as the gate source may blur the semantic distinction between CALPHAD outputs and LPBF-relevant derived descriptors. In the next version, node2 should depend on explicit physical descriptors, not on another synthetic node output.

My call: reasonable interim fix, yes. Reasonable long-term surrogate, no.

2. Is the R² hierarchy plausible, or should the early band be lower/higher?

For a confidence-building benchmark before FLAIME deployment, the current hierarchy is plausible.

What the current hierarchy says:
- Early nodes to terminal: 0.666 to 0.750
- Mid/late nodes to terminal: 0.978 and 0.995

That is a strong monotone information flow, which is exactly what you wanted after reviewer feedback.

Would I move the early band?
- I would not push it much higher than this. If y0/y1/y2 were all >0.8 to y5, partial evaluation becomes almost too easy and the benchmark starts to look pre-solved.
- I would not push it much lower than ~0.5 if the stated purpose is “build confidence before FLAIME deployment.” Below that, you drift back toward the earlier complaint: cheap or early nodes feel weakly relevant to the terminal objective.

So the current 0.6-0.75 band is a good interim target.

The thing I would change is not the band itself, but how it is achieved. Right now the target is hit by normalized additive passthrough, which linearizes the chain. Better to preserve roughly this band while replacing the mechanism with a more physical nonlinear surrogate.

3. Does the weighted additive passthrough unfairly favor pKGFN over TSFN/HighFidOnly?

Not obviously over TSFN. More over the whole class of DAG-aware methods than over pKGFN specifically.

What my audit found:
- y5 is almost entirely passthrough-driven. Estimated fraction of var(y5) from the node-5 passthrough term is 0.979.
- The node-5 GP residual is tiny: var ≈ 0.0218 versus total var ≈ 5.94.
- Linear regression of y5 on (y3,y4) gives R²=0.996.
- Linear regression of y5 on (y0,y1,y2) gives R²=0.980.
- Linear regression of y3 on (y1,y2) gives R²=0.999.

Interpretation:
- In node space, the downstream mapping is nearly linear and nearly deterministic.
- That does create a benchmark artifact.
- But the artifact is not especially “pro-pKGFN versus TSFN,” because TSFN also benefits from an easy composite structure.
- The bigger distortion is versus HighFidOnly, since DAG-aware methods get very informative intermediate observations that are almost linearly propagated to y5.

So my answer is:
- Unfairly favor pKGFN over TSFN: probably no, not specifically.
- Introduce a benchmark artifact: yes.
- Artifact type: excessive linearization and variance domination by passthrough in y3/y4/y5.

Concrete mitigation if you keep this interim form:
- Cap the downstream deterministic variance contribution. A decent practical rule would be to keep the deterministic passthrough contribution below about 50-70% of total variance at each non-root node.
- Right now node4 is already passthrough-heavy and node5 is extreme.
- You can test this directly by tracking var(passthrough)/var(node output) in the correlation script.

4. What physics surrogate should replace the interim composition gate next, and what public Al LPBF data should calibrate it?

Best next replacement: Eagar-Tsai-style melt-pool surrogate for the LPBF stage, augmented with a cracking-related composition term.

If you want one next step, do this:
- Replace the current y2/y3 synthetic coupling with a simplified LPBF process map driven by laser power, scan speed, hatch spacing, layer thickness, plus composition-derived thermal descriptors.
- Predict melt-pool geometry / volumetric energy density proxy / lack-of-fusion tendency / keyholing tendency.
- Add a hot-cracking susceptibility term based on freezing range or a Kou-like solidification metric from composition-derived thermodynamic descriptors.

Why this is the right next step:
- It directly connects composition and process variables in the way reviewers will expect.
- It fixes the exact semantic hole in the interim node2 gate.
- It gives you nonlinear coupling without resorting to a generic additive passthrough.

Recommended division of labor across nodes:
- y0: CALPHAD/Scheil descriptors such as liquidus, solidus, freezing range, phase fractions, maybe partitioning-related features.
- y2 or y3: processability/melt-pool surrogate using Eagar-Tsai or a reduced energy-density model.
- cracking susceptibility term: derived from freezing range / terminal solidification sensitivity, potentially Kou-inspired.

Which public data to calibrate against:
- Public LPBF Al datasets reporting porosity, crack density, density, or printability maps across power and scan speed for known alloys.
- Datasets/papers from groups publishing process maps for AlSi10Mg, Scalmalloy-type alloys, Al-Mg-Zr, Al-Cu-Mg, and crack-prone wrought alloys adapted for LPBF are the most practical starting point.
- If you need one calibration strategy rather than one perfect dataset: calibrate melt-pool geometry / dense-processing regime on abundant AlSi10Mg LPBF process-map data, then calibrate composition/cracking modifiers separately from alloy-specific literature reporting crack sensitivity versus freezing range or composition class.

Between the two candidate physics families you named:
- Eagar-Tsai is the better immediate replacement for node2/node3 because it ties directly to scan parameters and gives a process surrogate.
- Kou/freezing-range terms are the better composition gate, but not sufficient alone for LPBF-in/process response.
- So the best next version is not either/or. Use Eagar-Tsai for process physics plus Kou/freezing-range-like descriptors as composition-dependent modifiers.

5. Concrete code-level concerns in manufacturing_problem.py / bofn_node_correlations.py?

Yes. None of these invalidate the reported grid numerically, but a few matter for interpretation.

A. Main interpretation concern: downstream outputs are dominated by the additive passthrough
This is the big one.
- In manufacturing_problem.py, `_couple()` adds normalized parent passthrough directly to the GP output.
- Because parent inputs are standardized by empirical SD and then reused recursively, downstream nodes can accumulate large deterministic variance.
- In this realization, y5 is dominated by that term.

This does not make the R² grid wrong. It does mean the grid is mostly measuring the designed passthrough scaffold, not the GP-sampled node nonlinearities.

B. `bofn_node_correlations.py` reports Pearson-correlation-squared, not full regression-model R²
- `r_squared()` computes corr(x,y)^2.
- For simple linear relation with intercept, that equals OLS R², so the label is fine in practice.
- But if you later introduce nonlinear surrogates, this number becomes a limited summary. It is still useful, just not the whole dependence story.
- I would relabel in comments/output as “Pearson R²” or “squared Pearson correlation” to avoid over-claiming.

C. The y5-relative grid is fine, but the matrix is symmetric and does not encode direction
- `r2_matrix[i,j]` is symmetric by construction.
- For the DAG interpretation, “y2->y3” is being read off from a symmetric association measure, not a directional effect estimate.
- That is okay for your stated reviewer requirement, since the ask is terminal relevance, not causal effect.
- But in writeups, avoid language implying directional explained variance from this matrix alone.

D. `_calibrate_parent_scales()` uses the same evaluate() machinery with coupling temporarily disabled
This is okay, but note:
- The scales are calibrated from one Sobol sample of size 1024.
- That introduces a small Monte Carlo dependence of the normalization constants on calibration sample and seed.
- It is not a bug, just a discretionary modeling choice.
- If you want cleaner reproducibility in papers, either fix and report that calibration seed or precompute/store the scales.

E. Node-2 composition gate uses `function0(X[..., [0,1]])` directly
- This creates a synthetic dependence of node2 on node0's latent GP draw, not just on shared composition descriptors.
- Again, acceptable interimly, but semantically it means y2 is partly a transformed copy of y0, not an independently modeled process response to the same physical descriptors.
- That can inflate coherence in a way real pipelines would achieve through shared descriptors, not shared latent draw.

F. Output scales are drifting strongly across downstream nodes
From the reproduced Sobol run, node SDs were approximately:
- y0: 0.415
- y1: 0.125
- y2: 0.486
- y3: 0.310
- y4: 1.387
- y5: 2.437

That downstream inflation is another sign that the additive coupling is setting the geometry more than the GP priors are.

My bottom line

As an interim synthetic benchmark fix, this is defensible and much better than the earlier version. It satisfies the stated reviewer/PI requirement cleanly:
- early nodes are meaningfully predictive of y5,
- middle/late nodes are stronger,
- y2 is no longer an irrelevant root.

I would approve it as an interim repair.

I would also put one sentence in the manuscript/notes saying the current version is a calibrated synthetic proxy, not yet a physics-grounded LPBF surrogate.

If you want the one most important next action: replace the node2/node3 synthetic coupling with an Eagar-Tsai-based process surrogate modulated by composition-derived freezing-range / cracking descriptors. That will preserve the desired R² hierarchy without the current near-linear passthrough artifact.

- Discretionary analytical decisions made during the analysis:
  - Treated the provided noiseless Sobol grid result (n=4096, seed=0) as the primary benchmark summary and reproduced it directly from the current code before interpreting the benchmark.
  - Used squared Pearson correlation as the operative R² metric because that is what `bofn_node_correlations.py` computes.
  - Added post hoc variance decomposition of downstream nodes into GP residual plus deterministic passthrough term to assess artifact risk, since this is not reported by the existing script.
  - Used joint linear regression diagnostics on node outputs, including y5 on (y0,y1,y2) and y5 on (y3,y4), to evaluate whether the current coupling makes the DAG nearly linear in node space.
  - Interpreted benchmark fairness mainly in terms of relative advantage for DAG-aware methods versus HighFidOnly, and separately considered whether any artifact would favor pKGFN over TSFN specifically.
  - Recommended Eagar-Tsai plus composition-derived cracking/freezing-range modifiers as the next surrogate family, rather than choosing a pure cracking-only term, because the user’s stated concern is LPBF-in/process response rather than only alloy crack susceptibility.
