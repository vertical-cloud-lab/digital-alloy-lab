# CrabNet-HP and Hard-Sphere Particle-Packing as BOFN Benchmark Problems

**Context:** Companion to `edison-trajectories/benchmark-representativeness-plan.md`
(PR #14 branch `copilot/explore-llms-function-networks-bo`). Resolves issue *"Consider
how crabnet hyperparameter or the physics-based particle packing simulations could be
used in the bofn benchmarking"*.

The current BOFN benchmark stack
(`benchmarks/bofn_pkgfn_demo.py` → `benchmarks/partial_kgfn/manufacturing_problem.py`)
is built on the GP-sampled "Manu" test from Buathong et al. (2024). Edison's diagnosis
in PR #14 already showed that DAG is *adversarial to p-KGFN* (information dams at
y1→y3, near-linear y4→y5, cheap-root R²<0.12). Two openly published, materials-flavored
multi-fidelity benchmarks from the AC group can be plugged in alongside the synthetic
DAG and the planned physics-anchored DAG to give a more representative picture before
the physics-anchored surrogates land.

## 1. The two candidate benchmarks

### 1.1 CrabNet hyperparameter benchmark

- **Refs:** Baird, Parikh, Sparks (2023), *Materials Science Optimization Benchmark
  Dataset for High-dimensional, Multi-objective, Multi-fidelity Optimization of CrabNet
  Hyperparameters*, ChemRxiv `10.26434/chemrxiv-2023-9s6r7`. Method paper: Baird,
  Sparks (2022), arXiv:2203.12597 (Ax + SAASBO on CrabNet HPs).
- **HF Space:** https://huggingface.co/spaces/AccelerationConsortium/crabnet-hyperparameter
- **What it is:** ~173k CrabNet models trained on Matbench experimental band gap, 23
  hyperparameters sampled quasi-randomly. The HF space exposes a callable surrogate.
- **Fidelity knob:** *one* continuous fidelity in `[0, 1]` realised as a percentile
  rank with calibrated heteroskedastic noise (low fidelity ⇒ noisier proxy of the same
  underlying objective). The dataset is single-stage in the sense that there is no
  algorithmic cascade — fidelity is a knob on the *evaluation noise / cost* of
  the same model-training step, not a sequence of distinct algorithms.
- **Objectives:** MAE / RMSE (minimize), runtime (minimize), model size (minimize) —
  natively multi-objective.
- **Existing harness:** `AccelerationConsortium/baybe-multi-task-bo`
  notebooks `HF-API-Ax300iter.ipynb` and `HF-API-BayBE300iter.ipynb` already wrap the
  HF callable in 300-iter ask-tell loops and serve as ground-truth for any new
  algorithm we drop in.

### 1.2 Hard-sphere particle-packing benchmark

- **Refs:** Baird, Issa, Sparks (2023), *Materials Science Optimization Benchmark
  Dataset for Multi-Objective, Multi-Fidelity Optimization of Hard-Sphere Packing
  Simulations*, *Data in Brief* (open access); ChemRxiv `10.26434/chemrxiv-2023-fjjk7-v2`;
  package/code in `sparks-baird/matsci-opt-benchmarks`; raw CSV snapshot on Zenodo
  `10.5281/zenodo.7513019`; surrogate-model snapshot on Zenodo
  `10.5281/zenodo.7696165`.
- **What it is:** 494,498 random hard-sphere packing simulations (~206 CPU-days). Two
  released datasets:
  1. **Failure-probability dataset** — maps inputs → P(simulation fails).
  2. **Regression dataset** — packing fraction φ, runtime t, with simulation repeats so
     heteroskedastic noise is empirically known.
- **Fidelity structure:** **two discrete fidelities** corresponding to *sequentially
  executed algorithms of increasing fidelity*, plus a continuous "number of particles"
  knob inside each. Concretely: a cheap initial packing pass feeds a more expensive
  refinement pass; the second pass cannot run without the first.
- **Constraints:** 9 input parameters with linear constraints; failure modes are real
  (not Gaussian noise around a smooth surface).
- **Objectives:** max φ (packing fraction), min runtime, min P(failure) — natively
  multi-objective with a non-trivial reliability axis.

### 1.3 Why particle packing is the better manufacturing analogue

The issue's framing is exactly right: the particle-packing simulation is a *sequential
cascade of algorithms* of increasing fidelity, optionally parameterised by problem
size (n_particles). That is structurally identical to FLAIME's pycalphad → TC-Python →
AM-Module → atomization → LPBF → HT/char cascade we are arguing for in the proposal:

| Property                             | CrabNet-HP            | Particle-packing       | FLAIME LPBF Al-alloy  |
|--------------------------------------|-----------------------|------------------------|-----------------------|
| Number of fidelity stages            | 1 (continuous knob)   | 2 stages × 3 discrete n_particles = 6 nodes | ≥4 (CALPHAD → AM → LPBF → char) |
| Stages must run **sequentially**     | no                    | **yes**                | **yes**               |
| Distinct algorithms per stage        | no                    | **yes**                | **yes**               |
| Problem-size knob inside a stage     | n/a                   | n_particles            | n_coupons, layer-count |
| Native simulation failures           | no (pure noise)       | **yes** (released as a P(fail) dataset) | **yes** (hot-tearing, smoke, recoater jams) |
| Heteroskedastic noise from repeats   | yes (rank-based)      | **yes (empirical)**    | yes                   |
| Multi-objective                      | yes (MAE, t, size)    | yes (φ, t, P_fail)     | yes (σ_y, ε_f, ρ, CSC)|

CrabNet-HP is the right *unit test* for high-D BO + a single fidelity knob (it stresses
SAASBO, MTBO, and the LLAMBO-warmstart arm of PR #14 directly). Particle-packing is the
right *system test* for p-KGFN and for the BOFN cascade as a whole, because its
sequential-algorithm structure is what p-KGFN's partial-eval cost amortisation was
designed to exploit.

## 2. Mapping each onto the existing BOFN code

The existing partial-eval interface
(`benchmarks/partial_kgfn/manufacturing_problem.py`) is a class with three contracts:

```python
n_nodes, parent_nodes, active_input_indices, node_dims, bounds, parent_bounds, node_costs
def evaluate_node(self, node_idx, X_node, parent_y) -> Tensor  # (n, 1)
```

Both benchmarks fit this interface with no change to `partial_kgfn.py`,
`thompson_sampling.py`, `dag.py`, or the `bofn_pkgfn_demo.py` driver — they just need
new `*_problem.py` modules under `benchmarks/partial_kgfn/`.

### 2.1 `crabnet_hp_problem.py` (proposed)

```
Node 0 (x[0:23], fidelity=φ_lo) → y0 = MAE_lo, runtime_lo, size_lo  # cheap noisy
Node 1 (y0_indices passed through, fidelity=φ_hi) → y1 = MAE_hi, runtime_hi, size_hi
```

- `parent_nodes = [[], [0]]`, two-node DAG (matches LowFid → HighFid eval cascade).
- `node_costs = [t_lo_mean, t_hi_mean]` from the empirical runtime distribution in the
  dataset (typically ~10–50× ratio).
- HF callable wrapped behind a thin `evaluate_node` adapter; offline cache of the
  released ChemRxiv table for CI (no network at test time — see §4).
- Bounds and types come straight from the 23-D HP table; integer/categorical HPs
  handled with `Normalize` + rounding inside `evaluate_node` (same trick the HF Space
  uses internally).

### 2.2 `particle_packing_problem.py` (proposed — 6-node, 3 discrete fidelities per stage)

To stress p-KGFN's partial-evaluation reasoning more aggressively, we expand
the original 2-node design into a **6-node DAG with three discrete fidelity
levels per stage**, treating each `(stage, n_particles)` pair as its own
node. This replaces the continuous `n_particles` knob with three calibrated
discrete settings per stage, giving p-KGFN a non-trivial fidelity-selection
problem on top of the cascade.

```
Stage 1 — FBA (force-biased)               Stage 2 — LS (Lubachevsky–Stillinger)
  Node 0  FBA-lo  (n_p =  128)     ───►      Node 3  LS-lo   (n_p =  128)
  Node 1  FBA-mid (n_p =  512)     ───►      Node 4  LS-mid  (n_p =  512)
  Node 2  FBA-hi  (n_p = 2048)     ───►      Node 5  LS-hi   (n_p = 2048)
```

- `parent_nodes = [[], [], [], [0], [1], [2]]`. Each LS-K node consumes the
  output of the same-fidelity FBA-K node — LS cannot run without an FBA
  pack at matched problem size.
- The 9 shared design variables (`mu1..3, std1..3, comp1..2, safety_factor`)
  enter every node; the per-node `n_particles` is **fixed** by the node
  identity, so a query is now a pair `(node_idx, x ∈ R^9)` instead of
  `(stage_idx, x ∈ R^9, n_particles ∈ R)`.
- `node_costs` use the empirical mean runtime per `(stage, n_particles)`
  cell from the released regression dataset. Smoke-test reference at
  `n_particles=128` is FBA ≈ 0.01 s, LS ≈ 1.6 s; on the full Zenodo
  snapshot the 2048-particle cell is two–three orders of magnitude slower
  than the 128-particle cell, giving p-KGFN a wide cost spread to exploit.
- Failure handling: `evaluate_node` returns `NaN` whenever the released
  `P(fail | x, n_particles)` head says fail. The fail rate rises sharply
  with `n_particles`, which keeps the high-fidelity nodes informative but
  unreliable — exactly the regime the partial-eval acquisition is meant
  to handle.
- Linear input constraints: pass through to the inner solver via
  `inequality_constraints` (BoTorch already supports this on
  `optimize_acqf`).

The original 2-node continuous-fidelity formulation is still available as a
simpler baseline (`--problem packing-2node`); the 6-node form above is the
default (`--problem packing`).

### 2.3 Multi-objective glue

For both, the terminal node returns ≥2 objectives. To keep the change minimal:

- Phase A: scalarize with a fixed Chebyshev weight at the terminal so the existing
  scalar `Y[..., -1].max()` reporting works unchanged; this is enough to A/B the
  cascade against Random/TSFN/p-KGFN.
- Phase B: swap to `qNEHVI` per representativeness-plan §3; same inner change for both
  benchmarks (and for the physics-anchored DAG).

### 2.4 Emulator verification (2026-04-30 smoke test)

I verified the particle-packing path against the published package and Zenodo snapshots
without committing any external artifacts:

1. Installed `matsci-opt-benchmarks==0.2.3` into `/tmp` with `--no-deps` and used the
   `matsci_opt_benchmarks.particle_packing.utils` modules from that wheel.
2. Downloaded the raw-data Zenodo snapshot `10.5281/zenodo.7513019`:
   - `sobol_probability_filter.csv` — 3,898,705 bytes,
     md5 `21063bee0ef0a00b218f3a4b7aed8290`
   - `sobol_regression.csv` — 157,696,522 bytes,
     md5 `3e6c2be63903fb4c8c6f99848a5b9f8c`
3. Downloaded the surrogate-metadata Zenodo snapshot `10.5281/zenodo.7696165`:
   - `model_metadata.json` — 78,018,456 bytes,
     md5 `99de50536770b78cf31d32f53eb392f2`
4. Replayed the `matsci-opt-benchmarks` notebook feature schema:
   - common features:
     `mu1_div_mu3`, `mu2_div_mu3`, `std1`, `std2`, `std3`, `comp1`, `comp2`,
     `num_particles`, `safety_factor`
   - probability-filter targets: `fba_isna_prob`, `ls_isna_prob`
   - regression targets with percentile-rank noise knobs: `fba`, `ls`,
     `fba_time_s`, `ls_time_s`
5. Trained a lightweight random-forest smoke emulator from the Zenodo CSVs
   (16 trees, small subsamples, same target decomposition as the published notebook)
   and ran one prediction:

   ```json
   {
     "fba_isna_prob": 0.1130,
     "ls_isna_prob": 0.3282,
     "fba": 0.6702,
     "ls": 0.7250,
     "fba_time_s": 0.1713,
     "ls_time_s": 7.5920
   }
   ```

   Smoke-test held-out MAEs were `0.0569` (`fba_isna_prob`), `0.1083`
   (`ls_isna_prob`), `0.0053` (`fba`), `0.0119` (`ls`), `0.0458 s`
   (`fba_time_s`), and `63.15 s` (`ls_time_s`). The production Zenodo emulator is
   the 3.97 GB `surrogate_models.pkl`; the notebook
   `notebooks/particle_packing/1.4-sgb-model-usage.ipynb` shows this artifact can be
   memory-heavy, so CI should use the lightweight smoke-emulator path above or cache a
   pruned model artifact rather than loading the full pickle on GitHub-hosted runners.
6. Separately smoke-tested the package's bundled two-stage executable wrapper
   (`PackingGeneration.exe`) at `num_particles=128`, confirming the sequential
   `fba → ls` cascade runs end-to-end:

   ```json
   {"fba": 0.5644, "fba_time_s": 0.0091, "ls": 0.7052, "ls_time_s": 1.6161}
   ```

This changes the recommendation slightly: `particle_packing_problem.py` should start
from the Zenodo CSV smoke-emulator path (fast, reproducible, CI-safe), then optionally
enable the full Zenodo `surrogate_models.pkl` when running on ORC or another runner
with enough disk and memory.

## 3. What each benchmark would actually answer

| Question                                                             | CrabNet-HP | Particle-packing |
|----------------------------------------------------------------------|:---------:|:----------------:|
| Does p-KGFN beat Random/TSFN at *equal cost* on a real high-D HP problem with a calibrated noise knob? | ✓ | (less direct) |
| Does the LLAMBO warmstart from PR #14 actually transfer outside the synthetic DAG? | ✓ (literature priors are abundant for HPs) | ✓ (priors are weaker; harder test) |
| Does p-KGFN's cheap-root scouting pay off when low-fid is a *separate algorithm*, not just a noisier eval? | n/a | ✓ — **the canonical test** |
| Does the framework handle native failure modes (sims that crash, not just bad outputs)? | n/a | ✓ |
| Does the framework handle a continuous "problem size" knob inside a discrete-fidelity node (mirror of n_coupons in FLAIME)? | n/a | ✓ |
| Does SAASBO baseline behave on a 23-D real problem (sanity check for FLAIME 16-D simplex + cardinality)? | ✓ | (only 9-D) |

The two are complementary: **CrabNet-HP for high-D + LLM warmstart, particle-packing
for sequential-cascade + p-KGFN + failure handling**. We should integrate both, not
pick one.

## 4. Concrete next steps (ordered by ROI)

1. **Cache the public datasets locally** under `benchmarks/data/` (gitignored heavy
   artifacts; commit a small README + checksums). For CrabNet-HP, also commit the
   ChemRxiv supplementary `.csv` because the HF Space requires network.
2. **Add `benchmarks/partial_kgfn/particle_packing_problem.py`** as the first
   integration — same interface as `manufacturing_problem.py`. Wrap a random-forest
   emulator fit to the released Zenodo CSVs using the exact target decomposition in
   `matsci-opt-benchmarks/notebooks/particle_packing/1.2-ri-surrogate.ipynb`
   (`P_fail` filters + percentile-rank-conditioned regressors for φ and runtime).
   Closes the "no real cascade in the benchmark" gap immediately.
3. **Add `benchmarks/partial_kgfn/crabnet_hp_problem.py`** with offline + HF-online
   modes. Offline mode reads the cached table and uses the same surrogate trick;
   online mode shells out to the HF Space (so the result matches the Ax/BayBE
   notebooks above for cross-validation).
4. **Wire both into `bofn_pkgfn_demo.py`** behind a `--problem {manu, packing,
   crabnet}` flag. Reuse the same algorithm panel
   (`Random`, `TSFN`, `pKGFN`, plus the LLAMBO arms when ready).
5. **Smoke-test on GHA**: 2 seeds × 3 algos × `--problem packing` should fit in
   <10 min; gate on a CI artifact json so regressions show up.
6. **Add a one-page README** under `benchmarks/` summarising the three problem
   families (synthetic Manu, particle-packing, CrabNet-HP) so the proposal narrative
   can cite them as the "benchmark battery" alongside the eventual physics-anchored
   FLAIME DAG.
7. **Cite both papers in the proposal narrative** (§ Activity 1 benchmarking
   subsection of `flaime-genesis-proposal.tex`) as the open-access multi-fidelity
   benchmarks against which p-KGFN + LLAMBO-warmstart will be validated *before*
   the FLAIME physics-anchored DAG is stood up. This is the same one-sentence reframe
   recommended in `benchmark-representativeness-plan.md` §9 and turns the current
   adversarial-DAG result into evidence of methodological breadth.

## 5. PR #58-style visualization design for particle packing

Two of the proposed artifacts are now committed alongside this doc and can
be regenerated with `python benchmarks/particle_packing_visualize.py` (see
`benchmarks/figures/particle_packing/README.md` for the data-cache recipe):

- `benchmarks/figures/particle_packing/particle_packing_dag.png` — the
  6-node DAG (FBA-lo/mid/hi → LS-lo/mid/hi at n_particles ∈ {128, 512,
  2048}), styled to sit next to PR #14's `pkgfn_dag.png`.
- `benchmarks/figures/particle_packing/particle_packing_emulator_diagnostics.png` —
  2×3 parity grid for the six emulator targets, trained on the verified
  Zenodo `7513019` snapshot.

The remaining files below are still design-stage and will be produced once
`particle_packing_problem.py` is wired into `bofn_pkgfn_demo.py`. Mirror the
recent PR #58 benchmark artifacts:
`benchmarks/bofn_pkgfn_visualize.py`,
`benchmarks/figures/actions_full/bofn_actions_cost_efficiency.png`,
`benchmarks/figures/actions_full/bofn_actions_summary.{csv,json}`, and
`benchmarks/figures/node_correlations.{png,json}`.

Proposed generated files:

| Artifact | Purpose |
|---|---|
| `benchmarks/figures/particle_packing/particle_packing_dag.png` | Two-node DAG: FBA cheap packing pass → LS refinement pass, with per-node outputs (φ, runtime, P_fail) and median runtime/cost labels from the Zenodo snapshot. |
| `benchmarks/figures/particle_packing/particle_packing_emulator_diagnostics.png` | 2×3 parity grid for the six emulator targets (`fba_isna_prob`, `ls_isna_prob`, `fba`, `ls`, `fba_time_s`, `ls_time_s`) with MAE annotations, matching the diagnostic role of PR #58's `node_correlations.png`. |
| `benchmarks/figures/particle_packing/particle_packing_cost_efficiency.png` | Equal-cost anytime curve, mean ± 1σ over paired seeds, for Random/Sobol, TSFN, HighFidOnly, and pKGFN; x-axis is cumulative wall-clock seconds (log scale), y-axis is best scalarized terminal score or hypervolume. |
| `benchmarks/figures/particle_packing/particle_packing_node_selection.png` | Stacked node-selection frequencies across seeds: FBA-only, LS-refinement, full cascade, failed-eval skips. This mirrors PR #58's node-selection plot and makes pKGFN's partial-evaluation behavior visible. |
| `benchmarks/figures/particle_packing/particle_packing_summary.{csv,json}` | Per-algorithm summary table: final mean ± std, average runtime budget consumed, average iterations, failure rate, and hypervolume/score gap to Random. |
| `benchmarks/figures/particle_packing/README.md` | One-page run card, same style as `actions_full/README.md`: workflow/run id (or ORC run id), algorithms × seeds, budget, source Zenodo checksums, and short interpretation. |

Recommended visual layout:

1. **Top-left:** compact DAG schematic, same visual hierarchy as `pkgfn_dag.png` but with
   explicit FBA and LS boxes and small gray cost/failure annotations.
2. **Top-right:** emulator diagnostics/parity panel; this is the most important
   difference from the synthetic Manu DAG because the benchmark now has a real
   surrogate-validation story.
3. **Bottom-left:** equal-cost convergence on log(runtime) x-axis, directly analogous
   to PR #58's cost-efficiency figure.
4. **Bottom-right:** node-selection histogram plus failure-rate inset, directly
   analogous to PR #58's node-selection artifact but with an added failure-mode channel.

Use the same algorithm ordering and summary-stat conventions as PR #58 so the particle
packing figure can sit next to `actions_full/bofn_actions_cost_efficiency.png` without
requiring a new interpretation frame.

## 6. What this does **not** change

- No edits to `partial_kgfn.py`, `dag.py`, `gp_network.py`, `thompson_sampling.py` —
  the partial-eval interface already accommodates both benchmarks.
- No new dependencies in `requirements.txt` for this design-document PR. The
  implementation PR should decide whether to add `scikit-learn` explicitly for the
  offline emulator path or to vendor a small precomputed smoke-model artifact.
- No change to the synthetic Manu DAG runs already on PR #14; both new benchmarks are
  additive comparators behind a CLI flag.
- No changes to the proposal page count — the citation hook is one sentence in §1
  Activity 1, which has room (see PR #52 thread audit, `flaime-genesis-proposal.tex`
  lines 775–800).

## 7. Open risks / things to watch

- **HF Space rate limits.** The CrabNet-HP space is community-hosted; treat the
  online path as a slow-cadence cross-check, not as the in-loop callable for 300-iter
  runs. Always run BO against the offline surrogate.
- **Failure-probability surrogate quality.** The packing-failure dataset is empirical
  and sparse in some corners; a poorly-calibrated `P(fail)` surrogate would
  artificially favour algorithms that explore conservatively. Use the same calibration
  set the data paper does (held-out 10% split).
- **Apples-to-apples cost units.** CrabNet-HP cost is wall-clock seconds; packing cost
  is wall-clock seconds; FLAIME cost is dollars. Report each problem on its native cost
  unit and never mix them on the same axis.
- **No cardinality / simplex constraints** in either benchmark. Neither stress-tests
  the FLAIME 16-D-simplex + at-most-K-active-elements setup
  (representativeness-plan §4). The physics-anchored DAG is still required for that.
