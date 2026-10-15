# Scaling Strategy: Hundreds of Thousands of Thermo-Calc Simulations with BOFN

*Revised after Edison review (Round 1, B+). See `thermocalc-scaling-edison-r1.md` for full review.*

## Problem Statement

We can run potentially **hundreds of thousands** of Thermo-Calc (TC) simulations via BYU HPC:
- Compute is essentially **free** (BYU fairshare rate-limited, not dollar-limited)
- TC-Python on BYU HPC is already operational
- We can selectively choose what to run based on all other data available

**Key constraint**: Standard GPs scale as O(n³) in training data. Whether we actually need a scalable surrogate depends critically on the composition bounds (see §Dimensionality Analysis below).

## Composition Bounds & Dimensionality Analysis

For Al-Mn-Cr-Zr (Al = balance), the practical dimensionality is **3 free composition variables + temperature = 4D**.

The required number of TC simulations depends on composition bounds:

| Scenario | Compositions | × Temps | Total | Surrogate needed? |
|:---|---:|---:|---:|:---|
| Full simplex, 1 at.% | 176,851 | 10 | 1,768,510 | Yes — scalable |
| Full simplex, 2 at.% | 23,426 | 10 | 234,260 | Yes — scalable |
| **Al-rich (Al ≥ 85%), 1 at.%** | **816** | **10** | **8,160** | **No — exact GP suffices** |
| Al-rich, 0.5 at.% | 5,456 | 10 | 54,560 | Borderline |
| Al-rich, 0.5 at.% × 50 temps | 5,456 | 50 | 272,800 | Yes — scalable |

**Critical decision**: If this is Al-rich alloy design (Al ≥ 85 at.%), the restricted region is small enough that standard exact GP may suffice (n < 5K at 1 at.% resolution). If exploring the broader simplex (e.g., high-entropy Al-Mn-Cr-Zr compositions), scalable surrogates are essential.

**Recommendation**: Start with the Al-rich region using exact GP. Expand to scalable surrogates only when the composition range demands it.

## Core Architecture: Heterogeneous-Scale Function Network

The CALPHAD node will accumulate data 100× faster than downstream experimental nodes. This creates a **heterogeneous-scale network** where each node needs a different surrogate strategy. The BOFN framework supports this naturally — each DAG node has its own model class.

## Tiered Surrogate Strategy

### Tier 1: Thermo-Calc Node — Surrogate Selection

**Decision tree** (choose based on dataset size):

1. **n < 5K**: Use standard `SingleTaskGP` (exact GP). No approximation needed.
2. **5K < n < 50K**: Use **SVDKL** (Stochastic Variational Deep Kernel Learning, Wilson et al. NeurIPS 2016, arXiv:1611.00336). Neural network feature extractor + inducing-point GP. Handles phase boundary non-stationarity via learned features while preserving GP posterior interface.
3. **n > 50K**: Use **SVDKL** with minibatch training, or fall back to **RF + conformal prediction** for fast-track initial surrogate.

**Why SVDKL over plain SVGP**: CALPHAD data has sharp phase boundaries (derivative discontinuities) that stationary kernels (Matérn, RBF) capture poorly. SVDKL learns a nonlinear feature map that smooths these boundaries before the GP layer.

**Fast-track alternative**: Random Forest + conformal prediction intervals. Published CALPHAD ML literature (npj Comp. Mat. 2024, DOI:10.1038/s41524-024-01335-1) shows RF trained on 480M CALPHAD data points outperforms DNNs for interpolation. For an initial Phase 1 surrogate, this is the fastest path.

**"Two-Shot" alternative** (if compute truly unlimited): Run TC exhaustively on the full Al-rich grid first (~5K points, trivially parallelizable), then use the complete dataset as a **deterministic lookup table** for Node 0 — no surrogate needed. Apply BO only to downstream experimental nodes. (Paramore et al. 2024, arXiv:2405.07130.)

### Tier 2: Downstream Nodes — Standard GPs

Powder production, LPBF printing, and characterization will have at most hundreds to low thousands of physical experiments. Standard `SingleTaskGP` is fine here:
- O(n³) with n < 1000 is fast
- Exact posteriors
- No approximation error

### Tier 3: Multi-Fidelity Bridge (CALPHAD → Experiment)

**Important caveats** (per Edison review):

1. **CALPHAD is deterministic**: Standard MF-GPs assume noise at all fidelity levels. For TC, use the Kennedy-O'Hagan autoregressive model: `y_exp(x) = ρ·y_TC(x) + δ(x) + ε`. In BoTorch, set `train_Yvar ≈ 1e-8` for the TC fidelity to encode near-zero noise.

2. **Physics mismatch, not just noise**: The "fidelity gap" between TC and experiments is not merely resolution — it's fundamentally different physics (equilibrium thermodynamics vs. far-from-equilibrium rapid solidification in LPBF). MFBO benefits depend critically on correlation between fidelities (Sabanza Gil et al., Nature Comp. Sci. 2025, DOI:10.1038/s43588-025-00822-9). If TC equilibrium predictions don't correlate with as-built LPBF microstructure, MF may not help.

3. **Scheil solidification** (non-equilibrium) may be a better proxy than equilibrium TC for LPBF outcomes. Consider using Scheil outputs as the TC node's primary quantities.

## TC Output Handling: Multi-Output Surrogates

TC produces **multiple outputs** per composition × temperature query. Rather than building one surrogate per output, reduce to 2–3 key scalar quantities most relevant to downstream nodes:

| Output | Description | Downstream use |
|:---|:---|:---|
| **ΔT_solidification** | Liquidus − solidus | Cracking susceptibility proxy |
| **f_primary_phase** | FCC fraction at solidification end | Printability predictor |
| **CSC (Cracking Susceptibility Criterion)** | Kou's criterion from Scheil path | Direct LPBF quality predictor |

Additional outputs (full phase fractions, enthalpies, driving forces) can be stored but need not all have surrogates. Use separate `SingleTaskGP` per scalar output, or a `MultiOutputGP` if correlations are strong.

## Ramp-Up Strategy: Leveraging Free Compute

### Phase 1: Dense Grid (weeks 1–2)
Run TC on a **space-filling design** (Sobol or Latin Hypercube) over the Al-rich composition region × temperature range:
- 3D simplex (Mn, Cr, Zr fractions; Al = balance, Al ≥ 85 at.%) × temperature (500–2500K)
- ~8K–55K points depending on resolution (1 at.% → 816 compositions × 10 temps; 0.5 at.% → 5,456 × 10 temps)
- Store outputs in structured Parquet dataset with composition + temperature index and provenance metadata
- For the Al-rich region, this may constitute **exhaustive coverage** — enabling the Two-Shot approach

### Phase 2: Adaptive Infill via Asynchronous BO (weeks 3+)
**Asynchronous BO is the primary strategy** (not synchronous batching) because:
- TC simulations have **variable runtime** (seconds to hours depending on phase complexity)
- Synchronous batching wastes time waiting for the slowest job
- The constraint is wall-clock time, not budget

Implementation:
- Treat pending evaluations as **fantasies** via `model.fantasize()`, conditioning on both completed and fantasized observations
- As each TC job completes, immediately update the surrogate and submit the next-best query
- Reference: Alvi et al. (ICML 2019) — async batch BO with improved local penalization
- Reference: aphBO-2GP-3B (arXiv:2003.09436) — specifically designed for HPC batch BO with fairshare constraints

### Phase 3: Targeted Expansion
Once the Al-rich region is well-covered:
- Use acquisition function to identify high-value compositions **outside** the initial bounds
- Gradually expand composition range if promising regions are found
- Switch to SVDKL surrogate when data exceeds exact GP capacity

## TC Failure Handling

TC simulation failures are **systematic, not random** — they cluster at complex phase boundaries (exactly where the surrogate needs to be most accurate).

**Do NOT impute with nearest-neighbor** (masks the most physically interesting regions).

Instead:
- Model TC convergence as a **separate binary classifier** (converged vs. failed)
- Use the classifier's uncertainty to identify regions needing finer resolution or different solver settings
- Flag failed compositions for manual inspection or alternative solver parameters

## Simplex Handling for Compositions

Standard approach: **drop-one-variable** (Al = 1 − Mn − Cr − Zr), optimize over Mn, Cr, Zr directly.

Alternatives to consider:
- **ILR (Isometric Log-Ratio) transform** (Egozcue et al. 2003): Maps simplex to unconstrained ℝ^(d-1), eliminating boundary effects. Worth testing as an ablation for 4+ component systems.
- **Ax/BoTorch linear constraints**: Native support for Σᵢ xᵢ ≤ 1, most practical BoTorch-native approach.
- **Feature gradient approach** (Xian et al., Digital Discovery 2025, DOI:10.1039/D5DD00080G): Scales linearly with component count for acquisition function optimization on composition spaces.

## Validation Protocol

- **10% held-out test set**: Randomly held out from initial space-filling design, never used for training
- **Calibration metrics**: CRPS (Continuous Ranked Probability Score), 90% prediction interval coverage (target: 85–95%)
- **Retraining triggers**: Retrain when coverage drops below 80% or when >1000 new observations added
- **Fresh-evaluation checks**: Periodically run TC on 50 randomly selected test points to verify surrogate hasn't drifted

## Integration with Existing BOFN Code

The current `benchmarks/bofn_demo.py` and `benchmarks/partial_kgfn/` code uses `SingleTaskGP` per node. To swap in a scalable surrogate for the TC node:

```python
# Current (small data):
model_calphad = SingleTaskGP(train_X, train_Y, ...)

# Scalable (100K+ data) — SVDKL example:
from gpytorch.models import ApproximateGP
from gpytorch.variational import CholeskyVariationalDistribution, VariationalStrategy

class SVDKLModel(ApproximateGP):
    def __init__(self, inducing_points, feature_extractor):
        variational_distribution = CholeskyVariationalDistribution(inducing_points.size(0))
        variational_strategy = VariationalStrategy(self, inducing_points, variational_distribution)
        super().__init__(variational_strategy)
        self.feature_extractor = feature_extractor  # nn.Sequential(...)
        self.mean_module = gpytorch.means.ConstantMean()
        self.covar_module = gpytorch.kernels.ScaleKernel(
            gpytorch.kernels.MaternKernel(nu=2.5, ard_num_dims=feature_dim)
        )

    def forward(self, x):
        features = self.feature_extractor(x)
        mean = self.mean_module(features)
        covar = self.covar_module(features)
        return gpytorch.distributions.MultivariateNormal(mean, covar)
```

The DAG structure, acquisition functions, and cost accounting remain unchanged — only the node-level surrogate changes.

## Key Literature

| Reference | Relevance |
|:---|:---|
| npj Comp. Mat. (2024), DOI:10.1038/s41524-024-01335-1 | 480M CALPHAD data points: RF > DNN for phase fraction prediction |
| Sundar et al. (2025), DOI:10.1557/s43578-024-01489-0 | CALPHAD + BO for alloy discovery |
| Liu, An & Sun (2023), arXiv:2311.07174 | "Large CALPHAD Model" — 97% accuracy for FeNiCrMn |
| Conway & Ghassemali (2022), DOI:10.3389/fmats.2022.889771 | HT-CALPHAD review with grid sizing |
| Klaver et al. (2018), DOI:10.3390/e20120911 | Brute-force CALPHAD scanning with Thermo-Calc |
| Wilson et al. (NeurIPS 2016), arXiv:1611.00336 | SVDKL — scalable deep kernel learning |
| Sabanza Gil et al. (Nature Comp. Sci. 2025), DOI:10.1038/s43588-025-00822-9 | When MFBO helps (and when it doesn't) |
| Alvi et al. (ICML 2019) | Async batch BO with local penalization |
| Kudva & Paulson (2025), arXiv:2510.03893 | BONSAI: Thompson sampling for networked systems |

## Risk Mitigation

| Risk | Mitigation |
|:---|:---|
| Surrogate calibration degrades | Monitor CRPS + coverage on held-out set; retrain trigger at 80% coverage |
| TC simulation failures at phase boundaries | Binary convergence classifier; flag for manual review, do NOT impute |
| Fairshare throttling limits throughput | Async BO + off-peak submission; prioritize high-acquisition-value queries |
| Phase boundaries cause non-stationarity | SVDKL (learned features smooth boundaries); anisotropic kernels for T vs. composition |
| TC database (TCAL) coverage gaps | Document gaps; fall back to pycalphad with COST507 for missing systems |
| Equilibrium TC ≠ rapid solidification | Use Scheil outputs as primary; validate MF correlation before deploying MFBO |

## Summary

1. **Start by defining composition bounds** — Al-rich (≥85%) may need only ~5K TC sims (exact GP suffices)
2. **Two-Shot approach first** — if Al-rich, run TC exhaustively, use as lookup table, apply BO only to experiments
3. **Scale up with SVDKL** when composition range expands beyond exact GP capacity
4. **Async BO for rate-limited HPC** — don't wait for batches, update continuously
5. **Multi-fidelity with caution** — validate TC↔experiment correlation before committing to MFBO
6. **BOFN framework stays the same** — only swap the node-level surrogate model class
