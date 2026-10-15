# Making the BOFN Benchmark Fair & Representative of FLAIME

**Status as of 2026-04-30:** post-fix pKGFN (both 32/64 and 64/128 hedges) lands at ≈ Random/Sobol on the current synthetic DAG, while TSFN/HighFidOnly dominate. Edison's diagnosis already showed the synthetic DAG is *unusually adversarial to pKGFN* (information dams at y1→y3, y3→y4; near-linear y4→y5; cheap roots with R²<0.12 to the terminal). That is **not** representative of the real FLAIME pipeline, where CALPHAD descriptors do gate downstream printability.

This file lists the concrete changes that would make the benchmark a fair stand-in for the FLAIME proposal's downstream problem (DE-FOA-0003612 Topic 3-B, Al-alloy LPBF discovery).

## 1. Physics-anchored node functions (replace Matheron toy)

Current `manufacturing_problem.py:202-229` builds each node as a 5-point GP draw with lengthscale `[2.0, 2.0]`. This is what produces the "information dams" + linear y4→y5.

Replace with **closed-form physics surrogates fit to public Al-alloy LPBF data**:

| Node | Surrogate | Anchor data |
|---|---|---|
| y0 (CALPHAD pycalphad) | Solidification range ΔT, liquidus T_L, predicted Mg₂Si fraction from `pycalphad` over the 16-D simplex | TDB-derived, no fit needed |
| y1 (TC-Python AM Mod.) | ΔT_Scheil, freezing-range susceptibility (Kou criterion `|dT/df_s|`) | Mishra & Thuillier 2014; Wang et al. 2019 |
| y2 (powder/atomization) | log-normal PSD parameters from gas-atomizer Plateau-Rayleigh model + Mg loss vs. melt T | Sun et al. 2017; AMAZEMET datasheet |
| y3 (LPBF melt-pool) | Eagar–Tsai melt-pool depth/width vs. `(P, v, h, t)` + porosity from V*E/E_threshold | Tang et al. 2017; King et al. 2014 |
| y4 (HT/aging) | JMAK kinetics on (T_ag, t_ag) for Al₃Zr/Al₆Mn precipitation; Orowan strengthening | Knipling et al. 2008; Polmear |
| y5 (mech char) | Hall-Petch + Orowan + solid-solution sum from y4 outputs; ductility from porosity (y3) | Rosenthal et al. 2017 |

**Effect on R² to terminal:** published correlations give roughly R²(ΔT, hot-cracking)≈0.5-0.7; R²(porosity, UTS)≈0.4-0.6; R²(precipitate fraction, YS)≈0.7-0.85. Cheap CALPHAD nodes would explain ~50% of variance in y5, not <12%. That makes pKGFN's cost-amortization a real lever instead of a trap.

### 1a. Interim fix already landed (y5-relative coupling tuning, 2026-04-30)

Pending the full physics-surrogate rebuild (Section 1), `ExtendedManufacturingGPNetwork` now includes an interim composition-aware node-2 root: y2 still uses the legacy LPBF-process GP draw, but its active input includes the composition/CALPHAD coordinates and a modest normalized node-0 passthrough (`node2_composition_coupling = 0.25`). This removes the previous independent-root pathology where y2 had little terminal relevance. The class also accepts a **per-node** `coupling` list (length 6, root entries ignored), normalizes additive parent passthrough by each parent column's empirical std (`_calibrate_parent_scales`), and slightly weights the node-3 passthrough toward y2 (`[0.8, 1.0]`) so both upstream roots remain informative. Default `coupling = [0.0, 0.0, 0.0, 0.6, 0.8, 0.7]` produces the following R² values (4096 noiseless Sobol samples, seed=0):

| Quantity | R² | Tier |
|---|---:|---|
| y0 → y5 | 0.669 | early-terminal |
| y1 → y5 | 0.750 | early-terminal |
| y2 → y5 | 0.667 | early-terminal |
| y3 → y5 | 0.978 | middle-terminal |
| y4 → y5 | 0.995 | late-terminal |
| y2 → y3 | 0.708 | diagnostic edge |

This now satisfies the PI directive in the intended sense: early-node R² is measured relative to the final node y5 and lands in the 0.6–0.75 band, while middle/late nodes are higher. The previously unacceptable y2→y3 edge is also repaired (0.708), but this remains an interim synthetic fix; Section 1's Eagar–Tsai melt-pool surrogate is still the right physics-grounded replacement for the Matheron node-3 draw.

## 2. Cost ratios — calibrated, not extreme

Earlier draft proposed 6-orders-of-magnitude real FLAIME costs (`[$0.01, $0.10, $1, $200, $400, $250]`). PI guidance (2026-04-30): pushing the cheapest node that low bogs down pKGFN's inner KG, which over-spends acquisition compute on the cheapest node. **Reverted node 0 from $1 → $5**, restoring the original Buathong 2024 4-node "5_10_10_45" cheap:expensive ratio (1:9 vs the 1:45 we had briefly). Final defaults: `node_costs = [5, 10, 10, 45, 20, 30]`.

Use a `log(cost)` axis on the budget-curve plot to keep the visual room for future "real-cost" sub-experiments without the inner-KG cost.

## 3. Multi-objective terminal (Pareto, not scalar)

Replace single `y5` scalar with a 4-D objective:
- yield strength σ_y (max)
- ductility ε_f (max)
- relative density ρ_rel (max)
- hot-tear susceptibility CSC (min, Kou)

Switch acquisition family: `qNEHVI` for the BOFN baselines, `pKGFN-HV` for the cost-aware variant. This matches what FLAIME actually delivers (Pareto front of printable Al-alloys, not a single scalar).

## 4. Real composition space

Move from the toy 2-D box to **Al + 15 alloying elements** with the bounded simplex constraint already documented in the proposal (Mn 0–4, Cr 0–2, Zr 0–1.5, Mg 0–6, …) — 16-D, sum-to-1, with at-most-K active elements per design (K=5 cardinality constraint, like SLAYER/BoTorch's `OneHotToNumeric` + L0 ball).

Adds:
- Sparsity → SAASBO becomes a meaningful baseline.
- Cardinality → tests acquisition behavior under combinatorial constraints (FLAIME's actual setting).

## 5. Realistic measurement noise

Inject noise on each observation matching FLAIME instrumentation:
- y0/y1/y2: 0 (deterministic CALPHAD)
- y3 porosity: σ = 0.05 % (Archimedes)
- y4 precipitate fraction: σ = 5 % rel. (XRD Rietveld)
- y5 σ_y: σ = 3 % rel. (1.5 ksi on a 50 ksi alloy, per ASTM E8)
- y5 ε_f: σ = 8 % rel.

Currently noise=0 (or σ=0.05 across the board). Real noise levels make the GP heteroscedastic and stress the inner-KG quality differently per node.

## 6. Cross-system generalization (two-DAG benchmark)

Use **Al-Mn-Cr-Zr** and **Al-Zr** as the two FLAIME baseline systems (not anchors — see PR #52 review threads 24-28). Same node skeleton, different physics surrogates fit per system. Reported metric: **algorithm regret summed over both systems**, with paired-seed pairing.

This catches algorithms that overfit to one DAG topology (the current single-DAG benchmark cannot).

## 7. Algorithm panel

Drop `LowFidOnly`/`Node2Only` (they're already dominated and don't represent real FLAIME baselines). Add:

- **Sobol-Random** (current Random renamed for clarity)
- **qNEHVI-TSFN** (BOFN composite + multi-obj acquisition)
- **qNEHVI-HighFidOnly** (no DAG, just terminal node multi-obj)
- **SAASBO** (high-D sparse single-output, per dimension of objective then ε-constraint)
- **pKGFN-HV** (cost-aware partial-eval, multi-obj inner KG)
- **LLAMBO-warmstart + qNEHVI-TSFN** (LLM-prior init only; isolates "Phase 0" cost from acquisition)
- **LLAMBO-warmstart + pKGFN-HV** (the proposed FLAIME stack)

## 8. Reporting changes

- **Bootstrap-paired CI** on (algo − Random) hypervolume gap-closing rather than raw final mean — current single-number reporting hides the pairing structure already present in the seeds.
- **Anytime budget curve** on log(cost) x-axis with shaded ±1.96·SE bands.
- **Node-selection histograms** as a panel (we have these in the JSONs but they aren't surfaced in the figure).
- **Failure-mode audit row**: % of seeds that hit walltime / `error_fallback` / NaN gradient — pKGFN's apparent variance often hides outright failures.

## 9. Deferred-but-cheap proposal-narrative wins

These don't require new code, just a paragraph in the proposal narrative:

- Frame the current synthetic-DAG numbers as "**adversarial unit test**" (DAG was constructed to *minimize* low-fidelity correlation per Edison analysis), and the planned physics-anchored DAG as the "**representative FLAIME-system benchmark**" — a one-sentence reframe that turns the unflattering current results into evidence the team understands the failure modes.
- Cite Edison task `d0d3b9e3` recommendations once those land.

## 10. Priority order (estimated effort)

1. **Cost ratios** — 5 min code change in `bofn_actions_benchmark.py`. Highest ROI.
2. **Pareto / qNEHVI terminal** — 1-2 days. Largest representativeness gain.
3. **Physics-anchored y0/y1 surrogates** — 2-3 days using `pycalphad` for Al-Mn-Cr-Zr. Closes the R²<0.12 hole.
4. **16-D simplex composition space** — 1 day if we keep the rest of the DAG synthetic.
5. **Noise calibration** — 1 hr.
6. **Two-DAG / cross-system** — 1 week (depends on (3)).
7. **SAASBO, LLAMBO baselines** — 2-3 days each.

(1)+(2)+(5) alone (≈3 days) would make the benchmark representative enough for proposal narrative; (3)+(4) make it credible against an external reviewer who knows Al-alloy LPBF.
