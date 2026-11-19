"""Expanded LPBF manufacturing function network (9-node physics-based DAG).

Realistic test problem for the p-KGFN framework, modeling a complete LPBF
alloy development pipeline with physics-informed synthetic functions.

Physical nodes (7 distinct experiments):
  CALPHAD:    composition → phase_frac, solid_range          (2 outputs, $1)
  Powder PSD: atom_params + CALPHAD → D50                    (1 output, $6)
  Pow. dens.: atom_params + CALPHAD → apparent_density        (1 output, $2)
  Energy:     D50 + density + LPBF → melt_pool_width, depth  (2 outputs, $12)
  Scan:       melt_pool + scan params → layer_quality         (1 output, $12)
  Thermal:    layer_q + depth + thermal → residual_stress     (1 output, $6)
  Integration: depth + layer_q + stress → part_density        (1 output, $24)
  Mech:       part_density → yield_strength                   (1 output, $37)

Multi-output nodes are decomposed into single-output computational nodes
(10 total) for compatibility with the GaussianProcessNetwork framework.
Grouped nodes are co-evaluated at the physical experiment's cost.

Global decision vector (d=13):
  [comp_Al, comp_Si, comp_Mg,           # indices 0-2  (composition)
   atom_gas_pressure, atom_melt_temp,    # indices 3-4  (atomization)
   power, speed, spot_size,              # indices 5-7  (energy delivery)
   hatch, rotation, contour,             # indices 8-10 (scan strategy)
   preheat, dwell]                       # indices 11-12 (thermal mgmt)

Computational node layout:
  Node 0  (pf):        CALPHAD → phase_fraction      root  [0,1,2]  d=3
  Node 1  (sr):        CALPHAD → solid_range          root  [0,1,2]  d=3
  Node 2  (D50):       PSD → D50                      [0,1] [3,4]    d=4
  Node 3  (dens):      Density → apparent_density     [0]   [3,4]    d=3
  Node 4  (mp_w):      Energy → melt_pool_width       [2,3] [5,6,7]  d=5
  Node 5  (mp_d):      Energy → melt_pool_depth       [2,3] [5,6,7]  d=5
  Node 6  (lq):        Scan → layer_quality           [4,5] [8,9,10] d=5
  Node 7  (stress):    Thermal → residual_stress      [6,5] [11,12]  d=4
  Node 8  (part_dens): Integration → part_density     [5,6,7] []     d=3
  Node 9  (ys):        Mech → yield_strength          [8]   []       d=1

References:
  - Astudillo & Frazier (2021), "Bayesian Optimization of Function Networks"
  - Buathong & Frazier (2025), "Fast Bayesian Optimization of Function Networks"
  - Edison Scientific reviews: d0ad1eea, 6025bdcf, 98edd2c3
"""

from __future__ import annotations

import torch
from torch import Tensor

from benchmarks.partial_kgfn.dag import DAG

DTYPE = torch.double
DEVICE = torch.device("cpu")


# ---------------------------------------------------------------------------
# Ground truth node functions
# ---------------------------------------------------------------------------
# Each function takes the node's full input tensor (active_globals + parents)
# in the order produced by construct_obs_set:
#   [active_input_0, ..., parent_output_0, ...]
# ---------------------------------------------------------------------------


def _calphad_phase_frac(X: Tensor) -> Tensor:
    """Node 0: CALPHAD → phase fraction. (n,3) → (n,1)."""
    center = torch.tensor([0.7, 0.2, 0.1], dtype=DTYPE, device=DEVICE)
    dist_sq = ((X - center) ** 2).sum(dim=-1, keepdim=True)
    return torch.exp(-8.0 * dist_sq)


def _calphad_solid_range(X: Tensor) -> Tensor:
    """Node 1: CALPHAD → solidification range. (n,3) → (n,1)."""
    pf = _calphad_phase_frac(X)
    return 0.3 + 0.7 * (1.0 - pf)


def _powder_psd(X: Tensor) -> Tensor:
    """Node 2: PSD → D50. Input [atom_gas, atom_temp, pf, sr] (n,4) → (n,1)."""
    return torch.sigmoid(
        0.5 * X[..., 2:3] + 0.3 * X[..., 3:4] + 0.8 * X[..., 0:1] - 0.3 * X[..., 1:2]
    )


def _powder_density(X: Tensor) -> Tensor:
    """Node 3: Powder density → apparent_density.
    Input [atom_gas, atom_temp, pf] (n,3) → (n,1).
    """
    return (
        0.5 + 0.2 * X[..., 2:3] + 0.15 * X[..., 0:1] + 0.1 * torch.sin(3 * X[..., 1:2])
    )


def _energy_width(X: Tensor) -> Tensor:
    """Node 4: Energy delivery → melt pool width.
    Input [power, speed, spot_size, D50, app_dens] (n,5) → (n,1).
    """
    power, speed, spot = X[..., 0:1], X[..., 1:2], X[..., 2:3]
    d50, dens = X[..., 3:4], X[..., 4:5]
    return torch.sigmoid(
        2.0 * power - 1.5 * speed + 0.8 * spot - 0.3 * d50 + 0.2 * dens
    )


def _energy_depth(X: Tensor) -> Tensor:
    """Node 5: Energy delivery → melt pool depth.
    Input [power, speed, spot_size, D50, app_dens] (n,5) → (n,1).
    """
    power, speed, spot = X[..., 0:1], X[..., 1:2], X[..., 2:3]
    d50, dens = X[..., 3:4], X[..., 4:5]
    return torch.sigmoid(
        2.5 * power - 2.0 * speed + 0.3 * spot - 0.1 * d50 + 0.15 * dens
    )


def _scan_strategy(X: Tensor) -> Tensor:
    """Node 6: Scan strategy → layer quality.
    Input [hatch, rotation, contour, mp_width, mp_depth] (n,5) → (n,1).
    """
    hatch, rot, contour = X[..., 0:1], X[..., 1:2], X[..., 2:3]
    width, depth = X[..., 3:4], X[..., 4:5]
    overlap = width / hatch.clamp(min=0.01)
    return torch.sigmoid(overlap - 0.5 + 0.4 * depth + 0.3 * rot + 0.2 * contour)


def _thermal_mgmt(X: Tensor) -> Tensor:
    """Node 7: Thermal management → residual stress (lower better).
    Input [preheat, dwell, lq, mp_depth] (n,4) → (n,1).
    """
    preheat, dwell = X[..., 0:1], X[..., 1:2]
    lq, depth = X[..., 2:3], X[..., 3:4]
    return torch.sigmoid(
        1.0 - 0.5 * preheat - 0.3 * dwell - 0.4 * lq + 0.3 * depth + 0.2
    )


def _integration(X: Tensor) -> Tensor:
    """Node 8: Integration → part density.
    Input [mp_depth, lq, stress] (n,3) → (n,1).
    """
    depth, lq, stress = X[..., 0:1], X[..., 1:2], X[..., 2:3]
    return torch.sigmoid(1.5 * depth + 1.0 * lq - 0.8 * stress)


def _mech_ys(X: Tensor) -> Tensor:
    """Node 9: Mechanical → yield strength (terminal objective).
    Input [part_density] (n,1) → (n,1).
    """
    return 0.3 + 0.5 * torch.sigmoid(6.0 * (X - 0.5))


# Ordered list of node functions for dispatch
_NODE_FUNCTIONS = [
    _calphad_phase_frac,  # 0
    _calphad_solid_range,  # 1
    _powder_psd,  # 2
    _powder_density,  # 3
    _energy_width,  # 4
    _energy_depth,  # 5
    _scan_strategy,  # 6
    _thermal_mgmt,  # 7
    _integration,  # 8
    _mech_ys,  # 9
]


# ---------------------------------------------------------------------------
# Problem class
# ---------------------------------------------------------------------------


class ExpandedLPBFProblem:
    """10-node LPBF function network test problem for p-KGFN.

    Compatible with the ManufacturingGPNetwork interface expected by the
    p-KGFN benchmark runner.
    """

    n_nodes = 10
    dim = 13

    # DAG structure (computational nodes)
    parent_nodes = [
        [],  # 0: CALPHAD pf (root)
        [],  # 1: CALPHAD sr (root)
        [0, 1],  # 2: PSD (parents: pf, sr)
        [0],  # 3: Density (parent: pf)
        [2, 3],  # 4: Energy width (parents: D50, dens)
        [2, 3],  # 5: Energy depth (parents: D50, dens)
        [4, 5],  # 6: Scan (parents: mp_w, mp_d)
        [6, 5],  # 7: Thermal (parents: lq, mp_d)
        [5, 6, 7],  # 8: Integration (parents: mp_d, lq, stress)
        [8],  # 9: Mech YS (parent: part_dens)
    ]

    dag = DAG(parent_nodes=parent_nodes)

    # Which global decision variables each node uses directly
    active_input_indices = [
        [0, 1, 2],  # 0: composition
        [0, 1, 2],  # 1: composition
        [3, 4],  # 2: atomization params
        [3, 4],  # 3: atomization params
        [5, 6, 7],  # 4: power, speed, spot_size
        [5, 6, 7],  # 5: power, speed, spot_size
        [8, 9, 10],  # 6: hatch, rotation, contour
        [11, 12],  # 7: preheat, dwell
        [],  # 8: no global inputs (only parents)
        [],  # 9: no global inputs (only parents)
    ]

    # Total input dimension per node (active + parent outputs)
    node_dims = [3, 3, 4, 3, 5, 5, 5, 4, 3, 1]

    # Physical experiment grouping (nodes co-evaluated)
    node_groups = [[0, 1], [2], [3], [4, 5], [6], [7], [8], [9]]

    # Cost per computational node (= physical experiment cost for the group).
    # When p-KGFN selects any node in a group, ALL group nodes are evaluated
    # and the group cost is charged once.
    _group_costs = [1, 6, 2, 12, 12, 6, 24, 37]  # total $100
    node_costs = [1, 1, 6, 2, 12, 12, 12, 6, 24, 37]

    # Map from node index → group index
    _node_to_group = [0, 0, 1, 2, 3, 3, 4, 5, 6, 7]

    # Descriptive node names (for visualization)
    node_names = [
        "CALPHAD:pf",
        "CALPHAD:sr",
        "PSD:D50",
        "Powder:dens",
        "Energy:width",
        "Energy:depth",
        "Scan:lq",
        "Thermal:stress",
        "Integration:dens",
        "Mech:YS",
    ]

    # Physical experiment names (for DAG figure)
    experiment_names = [
        "CALPHAD",
        "PSD",
        "Powder Density",
        "Energy Delivery",
        "Scan Strategy",
        "Thermal Mgmt",
        "Integration",
        "Mech Testing",
    ]

    # Per-node observation noise standard deviations (physically motivated).
    # Cheap simulations (CALPHAD) are noisier/less reliable than expensive
    # physical experiments (mechanical testing).  Set to 0.0 for noise-free.
    node_noise_std = [
        0.15,   # 0: CALPHAD pf — fast simulation, approximate
        0.15,   # 1: CALPHAD sr — fast simulation, approximate
        0.10,   # 2: PSD D50 — moderate measurement noise
        0.10,   # 3: Powder dens — moderate measurement noise
        0.05,   # 4: Energy width — controlled LPBF experiment
        0.05,   # 5: Energy depth — controlled LPBF experiment
        0.05,   # 6: Scan lq — controlled experiment
        0.05,   # 7: Thermal stress — moderate precision
        0.03,   # 8: Integration dens — high-precision measurement
        0.02,   # 9: Mech YS — tensile test, highest precision
    ]

    # Per-group fidelity discount in (0, 1].
    # Reflects how well the group's observations predict the final objective.
    # Lower = less informative about YS → higher effective cost for pKGFN.
    # Tunable by the user based on domain knowledge.
    #   effective_cost = base_cost / fidelity
    # Index order matches node_groups: CALPHAD, PSD, Powder, Energy, Scan,
    #                                  Thermal, Integration, Mech
    group_fidelity = [0.2, 0.4, 0.4, 0.6, 0.6, 0.6, 0.85, 1.0]

    def __init__(self, seed: int = 0, noisy: bool = False) -> None:
        self.seed = seed
        self.noisy = noisy
        # Separate RNG for observation noise (independent of global torch seed)
        self._noise_rng = torch.Generator(device=DEVICE).manual_seed(seed + 2**16)
        self.bounds = torch.tensor(
            [[0.0] * self.dim, [1.0] * self.dim], dtype=DTYPE, device=DEVICE
        )
        # Parent-space bounds for intermediate node candidate generation.
        # Shape: (2, node_dim) covering [active_inputs, parent_outputs].
        # All outputs are roughly in [0, 1] (sigmoid functions).
        self.parent_bounds = [
            None,  # 0: root
            None,  # 1: root
            torch.tensor([[0, 0, 0, 0.3], [1, 1, 1, 1.0]], dtype=DTYPE),  # 2
            torch.tensor([[0, 0, 0], [1, 1, 1]], dtype=DTYPE),  # 3
            torch.tensor([[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]], dtype=DTYPE),  # 4
            torch.tensor([[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]], dtype=DTYPE),  # 5
            torch.tensor([[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]], dtype=DTYPE),  # 6
            torch.tensor([[0, 0, 0, 0], [1, 1, 1, 1]], dtype=DTYPE),  # 7
            torch.tensor([[0, 0, 0], [1, 1, 1]], dtype=DTYPE),  # 8
            torch.tensor([[0.0], [1.0]], dtype=DTYPE),  # 9
        ]

        # Compute optimal value by grid search
        self._optimal = None

    @property
    def optimal_value(self) -> float:
        """Approximate optimal YS via dense grid search (cached).

        Uses a dedicated Generator (not the global torch seed) so this
        computation is independent of the BO loop random state.
        """
        if self._optimal is None:
            n_grid = 500_000
            gen = torch.Generator(device=DEVICE)
            gen.manual_seed(42)
            X = torch.rand(n_grid, self.dim, dtype=DTYPE, device=DEVICE,
                           generator=gen)
            # Normalize compositions to simplex
            X[:, :3] = X[:, :3] / X[:, :3].sum(dim=1, keepdim=True)
            # Bias half the samples toward parameters known to be near-optimal
            half = n_grid // 2
            X[:half, 5].uniform_(0.9, 1.0, generator=gen)   # power near max
            X[:half, 6].uniform_(0.0, 0.1, generator=gen)   # speed near min
            X[:half, 8].uniform_(0.0, 0.02, generator=gen)  # hatch near zero
            Y = self.evaluate(X, noisy=False)
            self._optimal = Y[:, -1].max().item()
        return self._optimal

    def get_group_for_node(self, node_idx: int) -> tuple[int, list[int]]:
        """Return (group_cost, list_of_nodes_in_group) for a selected node."""
        g = self._node_to_group[node_idx]
        return self._group_costs[g], self.node_groups[g]

    def evaluate(
        self,
        X: Tensor,
        idx: list[int] | None = None,
        noisy: bool | None = None,
    ) -> Tensor:
        """Evaluate the function network.

        Args:
            X: Input tensor.
                - Full evaluation (idx=None): (n, 13) global decision vector.
                - Single node (idx=[k]): (n, node_dims[k]) node input.
            idx: Node index [k] for partial evaluation, or None for full.
            noisy: Add observation noise.  None → use self.noisy default.

        Returns:
            Full: (n, 10) all node outputs (+ noise if enabled).
            Partial: (n, 1) selected node output (+ noise if enabled).
        """
        use_noise = self.noisy if noisy is None else noisy

        if idx is not None:
            k = idx[0]
            result = _NODE_FUNCTIONS[k](X).detach()
            if use_noise and self.node_noise_std[k] > 0:
                noise = torch.randn(
                    result.shape, generator=self._noise_rng,
                    dtype=DTYPE, device=DEVICE,
                ) * self.node_noise_std[k]
                result = result + noise
            return result

        # Full evaluation: propagate through the DAG
        n = X.shape[0]
        output = torch.empty(n, self.n_nodes, dtype=DTYPE, device=DEVICE)

        # Node 0: CALPHAD pf
        comp = X[:, :3]
        output[:, 0] = _calphad_phase_frac(comp).squeeze(-1)

        # Node 1: CALPHAD sr
        output[:, 1] = _calphad_solid_range(comp).squeeze(-1)

        # Node 2: PSD D50 — input: [atom_gas, atom_temp, pf, sr]
        psd_in = torch.cat([X[:, 3:5], output[:, 0:1], output[:, 1:2]], dim=-1)
        output[:, 2] = _powder_psd(psd_in).squeeze(-1)

        # Node 3: Density — input: [atom_gas, atom_temp, pf]
        dens_in = torch.cat([X[:, 3:5], output[:, 0:1]], dim=-1)
        output[:, 3] = _powder_density(dens_in).squeeze(-1)

        # Node 4: Energy width — input: [power, speed, spot, D50, dens]
        ew_in = torch.cat([X[:, 5:8], output[:, 2:3], output[:, 3:4]], dim=-1)
        output[:, 4] = _energy_width(ew_in).squeeze(-1)

        # Node 5: Energy depth — input: [power, speed, spot, D50, dens]
        ed_in = torch.cat([X[:, 5:8], output[:, 2:3], output[:, 3:4]], dim=-1)
        output[:, 5] = _energy_depth(ed_in).squeeze(-1)

        # Node 6: Scan lq — input: [hatch, rot, contour, mp_w, mp_d]
        scan_in = torch.cat([X[:, 8:11], output[:, 4:5], output[:, 5:6]], dim=-1)
        output[:, 6] = _scan_strategy(scan_in).squeeze(-1)

        # Node 7: Thermal stress — input: [preheat, dwell, lq, mp_d]
        therm_in = torch.cat([X[:, 11:13], output[:, 6:7], output[:, 5:6]], dim=-1)
        output[:, 7] = _thermal_mgmt(therm_in).squeeze(-1)

        # Node 8: Integration part_dens — input: [mp_d, lq, stress]
        integ_in = torch.cat([output[:, 5:6], output[:, 6:7], output[:, 7:8]], dim=-1)
        output[:, 8] = _integration(integ_in).squeeze(-1)

        # Node 9: Mech YS — input: [part_dens]
        output[:, 9] = _mech_ys(output[:, 8:9]).squeeze(-1)

        # Add observation noise (after noiseless propagation through the DAG)
        if use_noise:
            for k in range(self.n_nodes):
                if self.node_noise_std[k] > 0:
                    noise = torch.randn(
                        n, generator=self._noise_rng,
                        dtype=DTYPE, device=DEVICE,
                    ) * self.node_noise_std[k]
                    output[:, k] = output[:, k] + noise

        return output.detach()
