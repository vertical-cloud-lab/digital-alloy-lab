Question: This is a follow-up review of a BOFN (Bayesian Optimization of Function Networks) framework for 
alloy discovery via LPBF. I have incorporated ALL critical and high-priority recommendations from the 
previous Edison review (task 98edd2c3). Please verify the changes are correct and provide remaining feedback.

## Changes Made (from previous review)
### Critical fixes implemented:
1. Scan strategy node now receives both melt-pool width AND depth (d=5). LOF/remelting physics.
2. Physics-informed constraints: keyholing (aspect ratio delta>0.8), balling (pi*w/l<1), LOF (H^2/W^2+L^2/D^2>1).
3. CALPHAD CSC output added: cracking susceptibility coefficient.
4. Composition simplex normalization in place.

### High-priority improvements:
5. Apparent density replaces flowability in energy delivery node.
6. Melt-pool depth added to thermal management node (d=4).
7. Training data increased to 50 points for d=5 nodes.
8. Powder PSD now receives solidification range from CALPHAD.
9. Multi-output characterization: yield_strength + elongation.
10. Fully Bayesian verification: SaasFullyBayesianSingleTaskGP works on v2 DAG (0.2% error).

## Updated DAG Architecture (v2)
Node 0 CALPHAD: d=3 -> 3 (phase_frac + solid_range + CSC)
Node 1a PSD: d=4 -> 1 (+solid_range input)
Node 1b Flowability: d=3 -> 1
Node 1c Density: d=3 -> 1
Node 2a Energy: d=5 -> 2 (apparent_density replaces flowability)
Node 2b Scan: d=5 -> 1 (+depth, CRITICAL fix)
Node 2c Thermal: d=4 -> 1 (+depth)
Node 2d Integration: d=3 -> 1
Node 3 Mech: d=1 -> 2 (+elongation)

## Questions:
1. Is the LOF constraint H^2/W^2+L^2/D^2>1 correctly formulated? H=hatch, W=melt_pool_width, L=layer_thickness (fixed 0.3), D=melt_pool_depth.
2. For keyhole constraint, is delta=depth/width>0.8 the right threshold?
3. Does PSD receiving solidification range make physical sense for atomization modeling?
4. Is the strength-ductility tradeoff (inverse relationship) in characterization node physically reasonable?
5. What are remaining gaps before Tier 2 benchmarking (CALPHAD-grounded)?
6. Should we add uncertainty propagation through the DAG?

## Verification Results
- All 9 nodes fit correctly, predictions within 0.2% of ground truth
- 66% cost savings from multi-stage screening (50 candidates)
- Physics-informed constraints produce realistic feasible/infeasible regions

## Key Code:
```python
illo & Frazier (2021), "Bayesian Optimization of Function Networks", NeurIPS
  - Buathong & Frazier (2025), "Fast Bayesian Optimization of Function Networks"
  - Eriksson & Jankowiak (2021), "SAASBO", UAI (290 citations)
  - Wang et al. (2021), "Analytical Prediction of Balling, LOF, Keyholing", Appl Sci
  - Bergmueller et al. (2023), "Systematic Approach to Process Parameter Optimization"
  - Edison tasks d0ad1eea, 6025bdcf, 98edd2c3

Usage:
  python benchmarks/bofn_expanded_demo.py
"""

import torch
from botorch.models import SingleTaskGP
from botorch.models.transforms.input import Normalize
from botorch.models.transforms.outcome import Standardize
from botorch.fit import fit_gpytorch_mll
from gpytorch.mlls import ExactMarginalLogLikelihood

torch.manual_seed(42)
DTYPE = torch.double
DEVICE = torch.device("cpu")

# ---------------------------------------------------------------------------
# Per-node costs (USD) — from VCL pipeline estimates
# ---------------------------------------------------------------------------
NODE_COSTS = {
    "calphad": 1.0,       # Node 0: CALPHAD evaluation
    "powder_psd": 50.0,   # Node 1a: PSD measurement
    "powder_flow": 30.0,  # Node 1b: Flowability test
    "powder_dens": 20.0,  # Node 1c: Apparent density
    "energy": 100.0,      # Node 2a: Single-track experiments
    "scan": 100.0,        # Node 2b: Multi-track pads
    "thermal": 50.0,      # Node 2c: Thermal monitoring
    "density": 200.0,     # Node 2d: Density cube
    "mech": 300.0,        # Node 3: Tensile testing
}
ATOMIZATION_COST = 200.0  # Ultrasonic atomization per composition
FULL_PIPELINE_COST = sum(NODE_COSTS.values()) + ATOMIZATION_COST


# ---------------------------------------------------------------------------
# Synthetic ground-truth functions for each node
# ---------------------------------------------------------------------------

def calphad_fn(composition):
    """Node 0: CALPHAD screening.
    composition (n, 3) → [phase_fraction, solidification_range, CSC] (n, 3).

    CSC = cracking susceptibility coefficient (Clyne-Davies style).
    Low CSC = low cracking risk = good printability.
    Edison review 98edd2c3 Q8: CALPHAD should output printability-relevant
    thermodynamic descriptors including CSC.
    """
    center = torch.tensor([0.7, 0.2, 0.1], dtype=DTYPE, device=DEVICE)
    dist_sq = ((composition - center) ** 2).sum(dim=-1, keepdim=True)
    phase_frac = torch.exp(-8.0 * dist_sq)
    # Solidification range: narrower near optimal composition
    solid_range = 0.3 + 0.7 * (1.0 - phase_frac)
    # CSC: cracking susceptibility (lower = better, correlates with narrow freezing range)
    csc = 0.2 + 0.6 * solid_range + 0.1 * torch.sin(5.0 * composition[..., 1:2])
    return torch.cat([phase_frac, solid_range, csc], dim=-1)


def powder_psd_fn(phase_frac, solid_range, atom_params):
    """Node 1a: Powder PSD D50.
    phase_frac (n,1) + solid_range (n,1) + atomization_params (n,2) → D50 (n,1).
    D50 in normalized [0,1] range (0=fine, 1=coarse).

    Edison review: include solidification range because alloy thermodynamics
    influence atomization response and particle-size behavior.
    """
    x = torch.cat([phase_frac, solid_range, atom_params], dim=-1)
    return torch.sigmoid(0.5 * x[..., 0:1] + 0.3 * x[..., 1:2]
                         + 0.8 * x[..., 2:3] - 0.3 * x[..., 3:4])


def powder_flow_fn(phase_frac, atom_params):
    """Node 1b: Powder flowability (Hausner ratio proxy).
    phase_frac (n,1) + atomization_params (n,2) → flowability (n,1).
    Higher = better flowability (normalized [0,1]).
    """
    x = torch.cat([phase_frac, atom_params], dim=-1)
    return 0.4 + 0.3 * torch.cos(x[..., 1:2]) + 0.2 * x[..., 0:1] + 0.1 * x[..., 2:3]


def powder_density_fn(phase_frac, atom_params):
    """Node 1c: Powder apparent density.
    phase_frac (n,1) + atomization_params (n,2) → apparent_density (n,1).
    Normalized [0,1].
    """
    x = torch.cat([phase_frac, atom_params], dim=-1)
    return 0.5 + 0.2 * x[..., 0:1] + 0.15 * x[..., 1:2] + 0.1 * torch.sin(3 * x[..., 2:3])


def energy_delivery_fn(d50, apparent_density, power, speed, spot_size):
    """Node 2a: Energy delivery → melt pool geometry.
    d50 (n,1) + apparent_density (n,1) + power (n,1) + speed (n,1) + spot_size (n,1)
    → [melt_pool_width, melt_pool_depth] (n,2).

    Edison review Q1: swap flowability for apparent_density as packing/absorptivity
    proxy. Powder-bed state changes effective absorptivity and layer thickness.
    """
    # Melt pool width: primarily power/speed/spot dependent
    width = torch.sigmoid(2.0 * power - 1.5 * speed + 0.8 * spot_size
                          - 0.3 * d50 + 0.2 * apparent_density)
    # Melt pool depth: power/speed dominant, packing density affects coupling
    depth = torch.sigmoid(2.5 * power - 2.0 * speed + 0.3 * spot_size
                          - 0.1 * d50 + 0.15 * apparent_density)
    return torch.cat([width, depth], dim=-1)


def scan_strategy_fn(melt_pool_width, melt_pool_depth, hatch, rotation, contour):
    """Node 2b: Scan strategy → layer quality.
    melt_pool_width (n,1) + melt_pool_depth (n,1) + hatch (n,1) + rotation (n,1)
    + contour (n,1) → layer_quality (n,1).

    Edison review Q2 (CRITICAL): LOF criteria depend on both width AND depth.
    Wang et al. (2021): H²/W² + L²/D² ≤ 1 for lack-of-fusion avoidance.
    Bergmueller et al. (2023): aspect ratio δ=depth/width governs process regime.
    """
    # Layer quality depends on overlap (width vs hatch) and remelting (depth-dependent)
    overlap = melt_pool_width / hatch.clamp(min=0.01)
    penetration = melt_pool_depth  # proxy for remelting capability
    quality = torch.sigmoid(overlap - 0.5 + 0.4 * penetration
                            + 0.3 * rotation + 0.2 * contour)
    return quality


def thermal_mgmt_fn(layer_quality, melt_pool_depth, preheat, dwell):
    """Node 2c: Thermal management → residual stress.
    layer_quality (n,1) + melt_pool_depth (n,1) + preheat (n,1) + dwell (n,1)
    → residual_stress (n,1). Lower stress is better (normalized [0,1]).

    Edison review Q3 (HIGH): Add melt-pool depth as proxy for thermal intensity.
    Residual stress depends on thermal gradients governed by melt-pool geometry.
    """
    # Residual stress reduced by preheat and dwell time, increased by deep melt pools
    stress = torch.sigmoid(1.0 - 0.5 * preheat - 0.3 * dwell
                           - 0.4 * layer_quality + 0.3 * melt_pool_depth + 0.2)
    return stress


def integration_fn(melt_pool_depth, layer_quality, stress):
    """Node 2d: Integration → part density.
    melt_pool_depth (n,1) + layer_quality (n,1) + stress (n,1) → part_density (n,1).
    """
    # Part density depends on all upstream LPBF factors
    density = torch.sigmoid(1.5 * melt_pool_depth + 1.0 * layer_quality
                            - 0.8 * stress)
    return density


def characterization_fn(part_density):
    """Node 3: Characterization.
    part_density (n,1) → [yield_strength, elongation] (n,2).

    Edison review Q8: multi-output characterization for strength-ductility
    tradeoff — single strength output is too narrow for alloy discovery.
    """
    ys = 0.7 * part_density + 0.3 * torch.sin(4.0 * part_density)
    # Elongation: generally inverse relationship with strength (tradeoff)
    el = 0.8 * (1.0 - part_density) + 0.2 * torch.cos(3.0 * part_density)
    return torch.cat([ys, el], dim=-1)


# ---------------------------------------------------------------------------
# Constraint functions for LPBF physical limits
# ---------------------------------------------------------------------------

def keyhole_constraint(melt_pool_geom):
    """Keyholing constraint: aspect ratio depth/width.

    Edison review Q5 (CRITICAL): Use aspect ratio as proxy for normalized enthalpy.
    Bergmueller et al. (2023): δ=0.8 is conduction-to-keyhole transition threshold.
    Returns: negative = feasible, positive = infeasible.
    """
    width = melt_poo
```

## Raw Results:
{
  "dag_nodes": 9,
  "global_dim": 14,
  "max_per_node_dim": 5,
  "n_training": 30,
  "n_screening": 50,
  "screening_result": {
    "n_total": 50,
    "stages": [
      {
        "name": "CALPHAD screening",
        "n_in": 50,
        "n_out": 19,
        "cost": 50.0
      },
      {
        "name": "Powder + LPBF",
        "n_in": 19,
        "n_out": 19,
        "cost": 14250.0
      },
      {
        "name": "Mechanical characterization",
        "n_in": 19,
        "n_out": 19,
        "cost": 5700.0
      }
    ],
    "total_cost": 20000.0,
    "naive_cost": 52550.0,
    "savings": 32550.0,
    "savings_pct": 61.94100856327307
  },
  "node_costs": {
    "calphad": 1.0,
    "powder_psd": 50.0,
    "powder_flow": 30.0,
    "powder_dens": 20.0,
    "energy": 100.0,
    "scan": 100.0,
    "thermal": 50.0,
    "density": 200.0,
    "mech": 300.0
  },
  "full_pipeline_cost": 1051.0
}


# Follow-Up Review: BOFN Framework for LPBF Alloy Discovery (v2 DAG)

## 1. Summary Assessment

The v2 DAG architecture represents substantial progress in addressing the critical and high-priority recommendations from the previous Edison review. Of the 10 claimed changes, 5 are fully verified as correct, 4 are partially correct with remaining issues, and 1 is inconsistent with the reported results. The overall DAG structure is sound, but several physics and implementation gaps must be resolved before Tier 2 (CALPHAD-grounded) benchmarking is viable.

The following table provides a detailed verification of each claimed change:

| Change # | Description | Verification Status | Notes / Issues |
|---|---|---|---|
| 1 | Scan strategy receives melt-pool width **and** depth (d=5) | ✅ Correct | This critical fix is implemented in the updated DAG (`Node 2b Scan: d=5`) and is physically appropriate because LOF/remelting depend on both width and depth, not width alone (wang2021analyticalpredictionof pages 4-6, harkin2023evaluationofthe pages 2-3). |
| 2 | Physics-informed constraints: keyholing (`δ > 0.8`), balling (`π·w/l < 1`), LOF (`H²/W² + L²/D² > 1`) | ⚠️ Partially Correct | LOF formulation is correct as an **infeasible-region** criterion (`> 1` means LOF) (wang2021analyticalpredictionof pages 4-6, gordon2020defectstructureprocess pages 4-5). Keyhole threshold `δ = depth/width > 0.8` is valid per Bergmueller but conservative; some literature uses onset near `0.5` with `0.5–0.8` as transition (bergmueller2023systematicapproachto pages 4-6, bergmueller2023systematicapproachto pages 6-8, gordon2020defectstructureprocess pages 4-5). Balling criterion is standard, but your DAG does **not** provide melt-pool length `l`, so it cannot be evaluated consistently from current node outputs (wang2021analyticalpredictionof pages 4-6, taylor2026analyticalmodelfor pages 4-6). |
| 3 | CALPHAD CSC output added | ⚠️ Partially Correct | Adding CSC is directionally correct and addresses the earlier gap, but the provided implementation is synthetic (`csc = 0.2 + 0.6 * solid_range + 0.1 * sin(...)`) rather than a CALPHAD-grounded cracking metric such as Clyne-Davies/Kou. Good placeholder, not yet benchmark-ready. |
| 4 | Composition simplex normalization in place | ⚠️ Partially Correct | Not verifiable from the provided code snippet. You state it is implemented, but no normalization logic is shown, so this remains unconfirmed in review. |
| 5 | Apparent density replaces flowability in energy delivery node | ✅ Correct | This is a physically better upstream variable for absorptivity/packing effects in the powder bed. The updated energy node definition reflects this change and is more defensible than using flowability alone. |
| 6 | Melt-pool depth added to thermal management node (d=4) | ✅ Correct | This is a meaningful improvement. Residual stress and thermal history are more plausibly linked to melt-pool depth than to layer quality alone, and the new node signature reflects that. |
| 7 | Training data increased to 50 points for d=5 nodes | ❌ Incorrect | This conflicts with the raw results, which report `"n_training": 30`. Until the results and code are updated consistently, this claim is not verified. |
| 8 | Powder PSD now receives solidification range from CALPHAD | ✅ Correct | This is physically reasonable as a secondary thermodynamic influence on atomization response and premature solidification behavior, even though PSD is still driven primarily by nozzle/gas/superheat variables (unal1987effectofprocessing pages 5-6, unal1987effectofprocessing pages 6-7, si2017characteristicsof7055al pages 3-3). |
| 9 | Multi-output characterization: `yield_strength + elongation` | ⚠️ Partially Correct | Adding a second output is a strong improvement, but the implemented inverse relationship is not physically reliable for LPBF alloys. In AM, strength and ductility can improve together, and density/defects often reduce **both**, with elongation usually more sensitive (wang2018additivelymanufacturedhierarchical pages 5-8, liu2022highpowerlaser pages 6-7, weaver2021understandinganisotropictensile pages 19-22). |
| 10 | Fully Bayesian verification: `SaasFullyBayesianSingleTaskGP` on v2 DAG (0.2% error) | ✅ Correct | As reported, this is a positive verification step and aligns with the goal of fully Bayesian node models. However, this verifies node-level GP fit quality, not full BOFN uncertainty propagation or EI-FN benchmarking, which still remains to be implemented for Tier 2 (astudillo2021bayesianoptimizationof pages 4-6, astudillo2021bayesianoptimizationof pages 1-2). |


*Table: This table checks each claimed revision against the updated DAG, code, and literature-supported physics. It highlights which changes are fully correct versus only partially resolved or still inconsistent before Tier 2 benchmarking.*

## 2. Answers to Specific Questions

### Q1: LOF Constraint Formulation

The LOF constraint H²/W² + L²/D² > 1 is **correctly formulated**. This is the Tang et al. geometric criterion, confirmed by Wang et al. (2021) who present it as H²/W² + L²/D² ≤ 1 for LOF avoidance (wang2021analyticalpredictionof pages 4-6), Gordon et al. (2020) who use ((H/W)² + (L/D)²) = 1 as the LOF boundary (gordon2020defectstructureprocess pages 4-5), and Harkin et al. (2023) who present it as (H/W)² + (T/D)² ≤ 1 with values inside the unit circle being LOF-free (harkin2023evaluationofthe pages 2-3). Your convention (> 1 = infeasible/LOF) is correct. One important caveat: Harkin et al. recommend applying a correction factor R_c² = 0.7 (R_c = 0.83) when using analytically derived melt-pool geometries, as the Rosenthal-based predictions can overestimate dimensions and cause the criterion to fail (harkin2023evaluationofthe pages 3-5, harkin2023evaluationofthe pages 1-2). Since your DAG uses GP surrogates rather than direct measurements, incorporating this correction factor is advisable.

### Q2: Keyhole Threshold δ = depth/width > 0.8

The threshold δ = 0.8 is **correct per Bergmueller et al. (2023)**, who explicitly classify conduction mode as δ_c < 0.5, transition mode as 0.5 ≤ δ_c < 0.8, and keyhole mode as δ_c ≥ 0.8 (bergmueller2023systematicapproachto pages 4-6, bergmueller2023systematicapproachto pages 6-8). However, this is a **conservative** choice. Other literature reports keyhole onset at lower aspect ratios: Gordon et al. (2020) cite D/W > 0.5 as indicative of keyholing (gordon2020defectstructureprocess pages 4-5), and Katagiri et al. (2023) report keyholing observed at D/W > 0.5–0.83 (katagiri2023meltpoolshape pages 1-2). Using 0.8 avoids false positives from the transition zone but may miss some keyhole porosity occurring in the 0.5–0.8 range. A recommended improvement is to parameterize the threshold or define a soft transition penalty for 0.5 < δ < 0.8.

### Q3: PSD Receiving Solidification Range

This connection is **physically justified** but represents a secondary effect. The primary drivers of particle size distribution in gas atomization are gas-to-metal ratio, nozzle geometry, and melt superheat. However, solidification range influences PSD through several mechanisms: (a) premature solidification during flight can coarsen PSD, as Ünal (1987) demonstrated that lower melt temperatures produced abruptly coarser powder due to incomplete break-up before freezing (unal1987effectofprocessing pages 5-6, unal1987effectofprocessing pages 6-7); (b) alloy thermodynamic properties (surface tension, viscosity) vary with composition and affect droplet disintegration (unal1987effectofprocessing pages 5-6); (c) the competition between droplet spheroidization time and solidification time determines particle morphology and effective PSD (si2017characteristicsof7055al pages 3-3); and (d) solidification range ΔT_LS controls microstructure within particles, which affects downstream processability (golod2017theevolutionof pages 3-5, tourret2011gasatomizationof pages 2-5). The inclusion is appropriate for a surrogate model that aims to capture composition-dependent atomization response.

### Q4: Strength-Ductility Tradeoff

The current inverse relationship in `characterization_fn` (where `el = 0.8*(1 - part_density) + ...`) is **physically incorrect** for LPBF alloys. This is a **critical issue** that must be corrected before benchmarking. The literature shows:

- Wang et al. (2018, Nature Materials, 2705 citations) demonstrated that LPBF 316L stainless steel achieves a combination of yield strength and ductility that "surpasses that of conventional 316L steels," falling "far outside the crescent-shaped domains" that characterize the conventional inverse tradeoff (wang2018additivelymanufacturedhierarchical pages 5-8, wang2018additivelymanufacturedhierarchical pages 1-5).
- Liu et al. (2022) showed AlSi10Mg under HP-LPBF exhibits a V-shaped relationship where both UTS and elongation decrease together as defect density increases up to a threshold, then both recover (liu2022highpowerlaser pages 6-7).
- Weaver et al. (2021) found that porosity and lack-of-fusion defects reduce both strength and ductility, with elongation being more severely affected, and that the relationship is alloy- and process-dependent (weaver2021understandinganisotropictensile pages 19-22, weaver2021understandinganisotropictensile pages 8-10).

The physically correct model should have both YS and elongation increase monotonically with part density, but with elongation exhibiting steeper sensitivity to density/defects.

### Q5: Remaining Gaps Before Tier 2 Benchmarking

The following table identifies all remaining gaps, prioritized by impact:

| Priority | Gap Description | Recommendation | Effort estimate |
|---|---|---|---|
| Critical | Characterization node physics is incorrect: current inverse strength-ductility mapping is not physically consistent for LPBF alloys; in AM, lower density / more defects generally reduce both YS and elongation, with elongation more sensitive to defects than YS (wang2018additivelymanufacturedhierarchical pages 5-8, liu2022highpowerlaser pages 6-7, weaver2021understandinganisotropictensile pages 19-22) | Replace with monotonic increasing functions of part density for both outputs, e.g. `ys = f(density)` and `el = g(density)`, with `g` steeper than `f`; ideally add composition / microstructure covariates later | Medium |
| Critical | Balling constraint cannot be evaluated consistently because no node outputs melt-pool length `l`, yet the implemented criterion requires `π·w/l < 1` or equivalent `L/W > π` (wang2021analyticalpredictionof pages 4-6, taylor2026analyticalmodelfor pages 4-6) | Add melt-pool length as a third output of `energy_delivery_fn`, or replace with an empirically calibrated `L/D`-based balling model if length is estimated from process parameters | Medium |
| Critical | Training-data claim is inconsistent: review text says d=5 nodes were increased to 50 points, but raw results still report `n_training = 30` | Update the code, config, and reported metrics so the benchmark actually uses `n=50` for d=5 nodes, then regenerate all reported fit and screening numbers | Low |
| High | EI-FN acquisition not integrated into our demo; current code fits per-node GPs but does not perform BOFN acquisition over the implied non-Gaussian posterior of the DAG output. Note: Astudillo & Frazier's reference implementation exists at [github.com/RaulAstudillo06/BOFN](https://github.com/RaulAstudillo06/BOFN) (astudillo2021bayesianoptimizationof pages 1-2, astudillo2021bayesianoptimizationof pages 4-6) | Adapt EI-FN from Astudillo's BOFN repo with reparameterized sampling through the DAG and QMC / Sobol sampling (`M≈128`) | High |
| High | No multi-objective acquisition for `yield_strength + elongation`; current setup adds two outputs but not Pareto-aware optimization | Use a multi-objective acquisition such as `qNEHVI` in BoTorch on the final objective layer, or a BOFN-compatible EHVI-style formulation for Pareto front discovery | High |
| High | CSC is added but not CALPHAD-grounded; current `CSC` output is synthetic and not a real cracking susceptibility model | Replace the synthetic CSC with a pycalphad / Thermo-Calc-derived metric using a literature-grounded cracking criterion such as Clyne-Davies or Kou | High |
| High | LOF physics is cited correctly, but `scan_strategy_fn` does not implement the actual LOF inequality; it uses a sigmoid quality proxy instead of explicit geometric feasibility (wang2021analyticalpredictionof pages 4-6, harkin2023evaluationofthe pages 2-3) | Add LOF as an explicit constraint function using `H²/W² + L²/D² ≤ 1` (or calibrated `≤ Rc²`) rather than embedding it only indirectly in `scan_strategy_fn` | Low |
| Medium | Composition simplex normalization is claimed but not visible in the provided code, so it is not review-verifiable | Add explicit normalization code and unit tests showing composition vectors are projected / normalized onto the simplex before CALPHAD evaluation | Low |
| Medium | Keyhole threshold `δ = depth/width > 0.8` is valid but conservative; literature also uses `~0.5` as lower onset with `0.5–0.8` as transition (bergmueller2023systematicapproachto pages 4-6, bergmueller2023systematicapproachto pages 6-8, gordon2020defectstructureprocess pages 4-5) | Parameterize the keyhole regime as conduction `<0.5`, transition `0.5–0.8`, keyhole `≥0.8`, or treat threshold as alloy / machine dependent | Low |
| Medium | Screening balance appears imbalanced: CALPHAD rejects 62% of candidates, while the LPBF stage rejects none, suggesting poor stage selectivity calibration | Recalibrate stage thresholds so intermediate LPBF nodes also contribute meaningful pruning, or report why CALPHAD-only triage is intended | Medium |
| Medium | Analytical LOF predictions may need calibration; Harkin et al. suggest a correction factor `Rc² = 0.7` (`Rc = 0.83`) when using analytically derived melt-pool geometries (harkin2023evaluationofthe pages 3-5, harkin2023evaluationofthe pages 1-2) | Add an option to apply `Rc² = 0.7` in the LOF constraint when geometry comes from analytical / surrogate predictions rather than measured melt-pool dimensions | Low |


*Table: This table summarizes the remaining issues before Tier 2 BOFN benchmarking, prioritized by impact on physical validity and benchmarking readiness. It pairs each gap with a concrete recommendation and rough implementation effort.*

### Q6: Uncertainty Propagation Through the DAG

BOFN **inherently propagates GP posterior uncertainty** through the DAG, so explicit additional uncertainty propagation is not required when using the full BOFN framework. Astudillo & Frazier (2021) show that each node k has a reparameterized output b̃h_k(x, Z) = μ_{n,k}(...) + σ_{n,k}(...)·z_k, where z_k is standard normal, composed recursively through the DAG in topological order (astudillo2021bayesianoptimizationof pages 16-19, astudillo2021bayesianoptimizationof pages 4-6). The resulting implied posterior on g(x) is non-Gaussian due to function composition, and the expected improvement (EI-FN) is approximated via sample average approximation using M = 128 scrambled Sobol quasi-Monte Carlo samples (astudillo2021bayesianoptimizationof pages 19-21, astudillo2021bayesianoptimizationof pages 13-16).

However, the **current implementation does not use EI-FN**. The code fits per-node GPs independently using `SingleTaskGP` and `fit_gpytorch_mll`, which provides accurate node-level surrogates but does not perform the recursive compositional sampling that constitutes BOFN's uncertainty propagation. For Tier 2 benchmarking, implementing the full EI-FN acquisition with reparameterized sampling is essential (astudillo2021bayesianoptimizationof pages 1-2, astudillo2021bayesianoptimizationof pages 2-4).

## 3. Code-Level Issues

Several implementation issues were identified beyond the physics concerns:

1. **Truncated function**: The `keyhole_constraint` function is cut off at `melt_poo` and is incomplete in the provided code.
2. **Training data inconsistency**: The raw results report `n_training = 30`, contradicting the claimed increase to 50 points for d=5 nodes.
3. **Characterization node dimensionality**: Node 3 takes only `part_density` (d=1 input), which is insufficient for predicting mechanical properties that also depend on composition, thermal history, and microstructure.
4. **Missing melt pool length**: The balling constraint π·w/l < 1 requires melt pool length, but `energy_delivery_fn` outputs only [width, depth]. No node provides length.
5. **Screening imbalance**: CALPHAD rejects 62% of candidates (50→19), but Stage 2 passes all 19 through with no rejection, suggesting the constraint thresholds need rebalancing.
6. **LOF not directly implemented**: The `scan_strategy_fn` uses a sigmoid quality approximation rather than the actual geometric H²/W² + L²/D² ≤ 1 criterion.

## 4. Overall Verdict

The v2 DAG demonstrates meaningful progress: the scan strategy correctly receives depth, apparent density replaces flowability, thermal management includes melt pool depth, CALPHAD outputs CSC, PSD receives solidification range, and multi-output characterization is added. The reported 62% cost savings from multi-stage screening and 0.2% per-node GP fit accuracy are encouraging. However, three critical issues remain before Tier 2 readiness: (a) the characterization node's inverse strength-ductility relationship must be corrected, (b) the balling constraint lacks a necessary melt pool length input, and (c) the training data discrepancy must be resolved. Additionally, the transition from per-node GP fitting to full EI-FN acquisition is the key step needed to realize BOFN's value proposition of uncertainty-aware network optimization.

References

1. (wang2021analyticalpredictionof pages 4-6): Wenjia Wang, Jinqiang Ning, and Steven Y. Liang. Analytical prediction of balling, lack-of-fusion and keyholing thresholds in powder bed fusion. Applied Sciences, 11:12053, Dec 2021. URL: https://doi.org/10.3390/app112412053, doi:10.3390/app112412053. This article has 36 citations.

2. (harkin2023evaluationofthe pages 2-3): Ryan Harkin, Hao Wu, Sagar Nikam, Shuo Yin, Rocco Lupoi, Patrick Walls, Wilson McKay, and Shaun McFadden. Evaluation of the role of hatch-spacing variation in a lack-of-fusion defect prediction criterion for laser-based powder bed fusion processes. The International Journal of Advanced Manufacturing Technology, 126:659-673, Mar 2023. URL: https://doi.org/10.1007/s00170-023-11163-0, doi:10.1007/s00170-023-11163-0. This article has 23 citations.

3. (gordon2020defectstructureprocess pages 4-5): Jerard V. Gordon, Sneha P. Narra, Ross W. Cunningham, He Liu, Hangman Chen, Robert M. Suter, Jack L. Beuth, and Anthony D. Rollett. Defect structure process maps for laser powder bed fusion additive manufacturing. Additive Manufacturing, 36:101552, Dec 2020. URL: https://doi.org/10.1016/j.addma.2020.101552, doi:10.1016/j.addma.2020.101552. This article has 453 citations and is from a highest quality peer-reviewed journal.

4. (bergmueller2023systematicapproachto pages 4-6): Simon Bergmueller, Lukas Gerhold, Lorenz Fuchs, Lukas Kaserer, and Gerhard Leichtfried. Systematic approach to process parameter optimization for laser powder bed fusion of low-alloy steel based on melting modes. The International Journal of Advanced Manufacturing Technology, 126:4385-4398, Apr 2023. URL: https://doi.org/10.1007/s00170-023-11377-2, doi:10.1007/s00170-023-11377-2. This article has 45 citations.

5. (bergmueller2023systematicapproachto pages 6-8): Simon Bergmueller, Lukas Gerhold, Lorenz Fuchs, Lukas Kaserer, and Gerhard Leichtfried. Systematic approach to process parameter optimization for laser powder bed fusion of low-alloy steel based on melting modes. The International Journal of Advanced Manufacturing Technology, 126:4385-4398, Apr 2023. URL: https://doi.org/10.1007/s00170-023-11377-2, doi:10.1007/s00170-023-11377-2. This article has 45 citations.

6. (taylor2026analyticalmodelfor pages 4-6): Zane Taylor, Tharun Reddy, Maureen Fitzpatrick, Kwan Kim, Wei Li, C. L. Leung, Peter D. Lee, K.M. Bertsch, and L. Dresselhaus-Marais. Analytical model for balling defects in laser melting using rivulet theory and solidification. Journal of Applied Physics, Jan 2026. URL: https://doi.org/10.1063/5.0263633, doi:10.1063/5.0263633. This article has 1 citations and is from a peer-reviewed journal.

7. (unal1987effectofprocessing pages 5-6): A. Ünal. Effect of processing variables on particle size in gas atomization of rapidly solidified aluminium powders. Materials Science and Technology, 3:1029-1039, Dec 1987. URL: https://doi.org/10.1179/mst.1987.3.12.1029, doi:10.1179/mst.1987.3.12.1029. This article has 195 citations and is from a peer-reviewed journal.

8. (unal1987effectofprocessing pages 6-7): A. Ünal. Effect of processing variables on particle size in gas atomization of rapidly solidified aluminium powders. Materials Science and Technology, 3:1029-1039, Dec 1987. URL: https://doi.org/10.1179/mst.1987.3.12.1029, doi:10.1179/mst.1987.3.12.1029. This article has 195 citations and is from a peer-reviewed journal.

9. (si2017characteristicsof7055al pages 3-3): Chaorun Si, Xingling Tang, Xianjie Zhang, Junbiao Wang, and Weichao Wu. Characteristics of 7055al alloy powders manufactured by gas-solid two-phase atomization: a comparison with gas atomization process. Materials & Design, 118:66-74, Mar 2017. URL: https://doi.org/10.1016/j.matdes.2017.01.028, doi:10.1016/j.matdes.2017.01.028. This article has 74 citations and is from a highest quality peer-reviewed journal.

10. (wang2018additivelymanufacturedhierarchical pages 5-8): Y. Morris Wang, Thomas Voisin, Joseph T. McKeown, Jianchao Ye, Nicholas P. Calta, Zan Li, Zhi Zeng, Yin Zhang, Wen Chen, Tien Tran Roehling, Ryan T. Ott, Melissa K. Santala, Philip J. Depond, Manyalibo J. Matthews, Alex V. Hamza, and Ting Zhu. Additively manufactured hierarchical stainless steels with high strength and ductility. Nature materials, 17 1:63-71, Oct 2018. URL: https://doi.org/10.1038/nmat5021, doi:10.1038/nmat5021. This article has 2705 citations and is from a highest quality peer-reviewed journal.

11. (liu2022highpowerlaser pages 6-7): Mengna Liu, Kaiwen Wei, and Xiaoyan Zeng. High power laser powder bed fusion of alsi10mg alloy: effect of layer thickness on defect, microstructure and mechanical property. Materials Science and Engineering: A, 842:143107, May 2022. URL: https://doi.org/10.1016/j.msea.2022.143107, doi:10.1016/j.msea.2022.143107. This article has 84 citations.

12. (weaver2021understandinganisotropictensile pages 19-22): JS Weaver, JS Weaver, and I Rosenthal. Understanding anisotropic tensile properties of laser powder bed fusion additive metals: a detailed review of select examples. ArXiv, Nov 2021. URL: https://doi.org/10.6028/nist.ams.100-44, doi:10.6028/nist.ams.100-44. This article has 38 citations.

13. (astudillo2021bayesianoptimizationof pages 4-6): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

14. (astudillo2021bayesianoptimizationof pages 1-2): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

15. (harkin2023evaluationofthe pages 3-5): Ryan Harkin, Hao Wu, Sagar Nikam, Shuo Yin, Rocco Lupoi, Patrick Walls, Wilson McKay, and Shaun McFadden. Evaluation of the role of hatch-spacing variation in a lack-of-fusion defect prediction criterion for laser-based powder bed fusion processes. The International Journal of Advanced Manufacturing Technology, 126:659-673, Mar 2023. URL: https://doi.org/10.1007/s00170-023-11163-0, doi:10.1007/s00170-023-11163-0. This article has 23 citations.

16. (harkin2023evaluationofthe pages 1-2): Ryan Harkin, Hao Wu, Sagar Nikam, Shuo Yin, Rocco Lupoi, Patrick Walls, Wilson McKay, and Shaun McFadden. Evaluation of the role of hatch-spacing variation in a lack-of-fusion defect prediction criterion for laser-based powder bed fusion processes. The International Journal of Advanced Manufacturing Technology, 126:659-673, Mar 2023. URL: https://doi.org/10.1007/s00170-023-11163-0, doi:10.1007/s00170-023-11163-0. This article has 23 citations.

17. (katagiri2023meltpoolshape pages 1-2): Jun Katagiri, Masahiro Kusano, Satoshi Minamoto, Houichi Kitano, Koyo Daimaru, Masakazu Tsujii, and Makoto Watanabe. Melt pool shape evaluation by single-track experiments and finite-element thermal analysis: balling and lack of fusion criteria for generating process window of inconel738lc. Materials, 16:1729, Feb 2023. URL: https://doi.org/10.3390/ma16041729, doi:10.3390/ma16041729. This article has 21 citations.

18. (golod2017theevolutionof pages 3-5): V M Golod and V Sh Sufiiarov. The evolution of structural and chemical heterogeneity during rapid solidification at gas atomization. IOP Conference Series: Materials Science and Engineering, 192:012009, Apr 2017. URL: https://doi.org/10.1088/1757-899x/192/1/012009, doi:10.1088/1757-899x/192/1/012009. This article has 43 citations.

19. (tourret2011gasatomizationof pages 2-5): D. Tourret, G. Reinhart, Ch.-A. Gandin, G.N. Iles, U. Dahlborg, M. Calvo-Dahlborg, and C.M. Bao. Gas atomization of al-ni powders: solidification modeling and neutron diffraction analysis. Acta Materialia, 59:6658-6669, Oct 2011. URL: https://doi.org/10.1016/j.actamat.2011.07.023, doi:10.1016/j.actamat.2011.07.023. This article has 64 citations and is from a highest quality peer-reviewed journal.

20. (wang2018additivelymanufacturedhierarchical pages 1-5): Y. Morris Wang, Thomas Voisin, Joseph T. McKeown, Jianchao Ye, Nicholas P. Calta, Zan Li, Zhi Zeng, Yin Zhang, Wen Chen, Tien Tran Roehling, Ryan T. Ott, Melissa K. Santala, Philip J. Depond, Manyalibo J. Matthews, Alex V. Hamza, and Ting Zhu. Additively manufactured hierarchical stainless steels with high strength and ductility. Nature materials, 17 1:63-71, Oct 2018. URL: https://doi.org/10.1038/nmat5021, doi:10.1038/nmat5021. This article has 2705 citations and is from a highest quality peer-reviewed journal.

21. (weaver2021understandinganisotropictensile pages 8-10): JS Weaver, JS Weaver, and I Rosenthal. Understanding anisotropic tensile properties of laser powder bed fusion additive metals: a detailed review of select examples. ArXiv, Nov 2021. URL: https://doi.org/10.6028/nist.ams.100-44, doi:10.6028/nist.ams.100-44. This article has 38 citations.

22. (astudillo2021bayesianoptimizationof pages 16-19): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

23. (astudillo2021bayesianoptimizationof pages 19-21): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

24. (astudillo2021bayesianoptimizationof pages 13-16): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

25. (astudillo2021bayesianoptimizationof pages 2-4): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.