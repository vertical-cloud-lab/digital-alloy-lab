#!/usr/bin/env python3
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

r"""
A 5-node, multi-objective function network test problem for EIFN-style
Bayesian optimization (issue #265).

The network is a chain, 1 -> 2 -> 3 -> 4 -> 5, built from literature test
functions, each evaluated on its literature domain:

=====  ================================  =========================  ====================
Node   Function (literature domain)      Inputs                     Outputs
=====  ================================  =========================  ====================
1      Styblinski-Tang, 20-D, [-5, 5]    x1..x20                    1, scaled to [0, 1]
2      DTLZ2, 11-D, 2 obj., [0, 1]       x1..x10, node 1            2, scaled to
                                                                    [-5.12, 5.12]
3      Rastrigin, 22-D, [-5.12, 5.12]    x1..x20, node 2 (2)        1, scaled to [-5, 5]
4      ZDT4, 21-D, 2 obj.,               x1..x20, node 3            2: f1 in [0, 1] as is,
       x1 in [0, 1], rest in [-5, 5]                                f2 scaled to [-5, 5]
5      ZDT4, 2-D, 2 obj.                 node 4 (2)                 the 2 objectives
=====  ================================  =========================  ====================

Every edge passes the parent's output through a fixed min-max map onto the
child's literature domain for that input, using the exact (node 1) or a
rigorous (nodes 2 to 4) range of the parent over the feasible inputs. So
every node's output lies in the domain of the node it feeds, and each node's
function is only ever evaluated on its literature domain. The BoTorch
implementations of Styblinski-Tang, DTLZ2 and Rastrigin raise if they get an
input outside that domain, so this is checked on every call.

Input domain. ``bounds`` is ``[-5, 5]^20``, the domain of Styblinski-Tang and of
ZDT4's distance variables. x1..x10 also feed node 2 (DTLZ2, domain ``[0, 1]``)
and x1 is ZDT4's position variable (domain ``[0, 1]``), so x1..x10 are
constrained to ``[0, 1]``. Those 20 one-variable constraints are stored in
``inequality_constraints`` in the ``(indices, coefficients, rhs)`` form that
``botorch.optim.optimize_acqf`` takes, meaning
``sum_i X[indices[i]] * coefficients[i] >= rhs``. BoTorch's constraints are
non-strict, so ``0 < x < 1`` is stored as ``0 <= x <= 1``.

Known Pareto front. The two objectives are node 5's ZDT4 outputs,
``f1 = u1`` and ``f2 = g(u2) * (1 - sqrt(u1 / g(u2)))`` with
``g(u2) = 1 + u2^2 + 10 (1 - cos(4 pi u2)) >= 1`` and ``(u1, u2)`` node 4's
outputs, so ``u1 = x1``. Since ``g >= 1`` and ``g - sqrt(t g)`` increases with
``g``, no input does better than ``f2 = 1 - sqrt(f1)``. That curve is reached for
every ``f1 = t`` in ``[0, 1]``: fix ``x1 = t`` and move x2..x20 from 0 towards
the maximisers of ZDT4's distance term. Node 4's scaled f2 output ``u2`` then
goes from below 0 to above 0 continuously, so by the intermediate value theorem
some input gives ``u2 = 0``, where ``g = 1``. The network's Pareto front is
therefore exactly the ZDT1/ZDT4 front ``f2 = 1 - sqrt(f1)``, ``f1`` in
``[0, 1]``. ``gen_pareto_set`` finds such inputs by bisection, and
``gen_pareto_front`` returns the front.

Reference point. ``(11, 11)``, BoTorch's reference point for the ZDT problems,
from Yang et al. (2019). The maximum hypervolume is then ``11 * 11 - 1/3 =
120 + 2/3``, the same as BoTorch's ZDT1. ``max_hv_for_ref_point`` gives the
maximum hypervolume for any other reference point.

Representation. Each scalar output is one network node, so the problem has
``n_nodes = 8`` scalar nodes in ``5`` groups (``node_groups``): node 1 is
``[0]``, node 2 is ``[1, 2]``, node 3 is ``[3]``, node 4 is ``[4, 5]`` and
node 5 is ``[6, 7]``. A group's outputs are evaluated together, from the same
input. This is the layout the EIFN ``GaussianProcessNetwork`` (one GP per
scalar node) and p-KGFN (``node_groups``) expect.

References:
    Styblinski & Tang (1990), Neural Networks 3(4):467-483 (domain [-5, 5]).
    Deb, Thiele, Laumanns & Zitzler (2005), Scalable test problems for
        evolutionary multiobjective optimization (DTLZ2, domain [0, 1]).
    Rastrigin (1974); Muehlenbein et al. (1991) (domain [-5.12, 5.12]).
    Zitzler, Deb & Thiele (2000), Evolutionary Computation 8(2):173-195
        (ZDT4: x1 in [0, 1], x2..xn in [-5, 5]).
    Yang, Emmerich, Deutz & Baeck (2019), Swarm and Evolutionary Computation
        44:945-956 (reference point (11, 11) for ZDT, as used by BoTorch).
    Astudillo & Frazier (2021), Bayesian Optimization of Function Networks,
        NeurIPS (EIFN).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple, Union

import torch
from botorch.acquisition.multi_objective.objective import (
    GenericMCMultiOutputObjective,
)
from botorch.test_functions.base import MultiObjectiveTestProblem
from botorch.test_functions.multi_objective import DTLZ2
from botorch.test_functions.synthetic import Rastrigin, StyblinskiTang
from torch import Tensor

try:  # layout of frazier-lab/partial_kgfn, which the issue's template uses
    from partial_kgfn.models.dag import DAG
except ImportError:  # pragma: no cover - depends on the environment
    try:  # layout of RaulAstudillo06/BOFN (EIFN)
        from bofn.utils.dag import DAG
    except ImportError:

        class DAG:
            """Directed acyclic graph of a function network.

            Same interface as ``partial_kgfn.models.dag.DAG`` and
            ``bofn.utils.dag.DAG``; used when neither package is installed.
            """

            def __init__(self, parent_nodes: List[List[int]]) -> None:
                self.parent_nodes = parent_nodes
                self.n_nodes = len(parent_nodes)
                self.root_nodes = [
                    k for k in range(self.n_nodes) if len(parent_nodes[k]) == 0
                ]

            def get_n_nodes(self) -> int:
                return self.n_nodes

            def get_parent_nodes(self, k: int) -> List[int]:
                return self.parent_nodes[k]

            def get_root_nodes(self) -> List[int]:
                return self.root_nodes


# ---------------------------------------------------------------------------
# Per-coordinate extremes used for the output scaling. All node functions used
# here are sums of one-variable terms, so the range of a node over a box is the
# sum of the per-coordinate ranges. The values below are the minima / maxima of
# each one-variable term on the stated interval (dense grid, then golden-section
# refinement; ``test_five_node_mo_network.py`` recomputes and checks them).
# ---------------------------------------------------------------------------

# Styblinski-Tang term s(x) = (x^4 - 16 x^2 + 5 x) / 2
_ST_MIN_01, _ST_MAX_01 = -5.0, 0.195612359055358  # on [0, 1] (max at 0.156731)
_ST_MIN_55, _ST_MAX_55 = -39.1661657037714, 125.0  # on [-5, 5] (min at -2.903534)

# Rastrigin term r(x) = x^2 + 10 (1 - cos(2 pi x)), min 0 at x = 0
_RAS_MAX_01 = 20.2512729909901  # on [0, 1], at x = 0.502546
_RAS_MAX_55 = 40.353290193839  # on [-5, 5] and on [-5.12, 5.12], at x = +-4.522994

# ZDT4 distance term z(x) = x^2 + 10 (1 - cos(4 pi x)), min 0 at x = 0
_ZDT4_MAX_01 = 20.5632133265025  # on [0, 1]
_ZDT4_ARGMAX_01 = 0.750951112627
_ZDT4_MAX_55 = 42.5911256798873  # on [-5, 5]
_ZDT4_ARGMAX_55 = 4.75602934755  # (and -4.756..., the term is even)

# Node output ranges over the feasible inputs (x1..x10 in [0, 1], x11..x20 in
# [-5, 5]); these are the ranges the min-max maps send onto the child domains.
#  node 1: Styblinski-Tang over [0, 1]^10 x [-5, 5]^10 (exact: attained)
_NODE1_LO = 10 * _ST_MIN_01 + 10 * _ST_MIN_55
_NODE1_HI = 10 * _ST_MAX_01 + 10 * _ST_MAX_55
#  node 2: each DTLZ2 output is (1 + g) * cos or sin, g = sum of 10 terms
#  (z - 0.5)^2 <= 0.25, so each output is in [0, 3.5] (a bound: 3.5 needs
#  node 1 at an extreme and x1 = 0 at once, which the network can't reach)
_NODE2_LO, _NODE2_HI = 0.0, 1.0 + 10 * 0.25
#  node 3: Rastrigin over [0, 1]^10 x [-5, 5]^10 x [-5.12, 5.12]^2 (upper end is
#  the box maximum, a rigorous bound)
_NODE3_LO = 0.0
_NODE3_HI = 10 * _RAS_MAX_01 + 10 * _RAS_MAX_55 + 2 * _RAS_MAX_55
#  node 4: ZDT4's f2 = g - sqrt(x1 g) lies in [0, g] and g <= 1 + sum of the 20
#  distance-term maxima (x2..x10 in [0, 1]; x11..x20 and node 3 in [-5, 5])
_NODE4_F2_LO = 0.0
_NODE4_F2_HI = 1.0 + 9 * _ZDT4_MAX_01 + 11 * _ZDT4_MAX_55

# Literature domains of the child inputs the parents are mapped onto
_DTLZ2_DOMAIN = (0.0, 1.0)
_RASTRIGIN_DOMAIN = (-5.12, 5.12)
_ZDT4_DISTANCE_DOMAIN = (-5.0, 5.0)
_ZDT4_POSITION_DOMAIN = (0.0, 1.0)

# How far outside the feasible inputs (absolute) an input may be and still be
# clamped back instead of rejected (SLSQP in optimize_acqf can step ~1e-9 out).
_INPUT_TOL = 1e-6


def _minmax(y: Tensor, lo: float, hi: float, new_lo: float, new_hi: float) -> Tensor:
    """Affine map of ``[lo, hi]`` onto ``[new_lo, new_hi]``, clamped to absorb
    floating-point rounding at the ends."""
    out = new_lo + (new_hi - new_lo) * (y - lo) / (hi - lo)
    return out.clamp(min=new_lo, max=new_hi)


class ZDT4(MultiObjectiveTestProblem):
    r"""ZDT4 test problem (Zitzler, Deb & Thiele, 2000). Not in BoTorch.

    ``d``-dimensional, on ``[0, 1] x [-5, 5]^(d-1)``:

        f_0(x) = x_0
        f_1(x) = g(x) * (1 - sqrt(x_0 / g(x)))
        g(x) = 1 + 10 (d - 1) + sum_{i=1}^{d-1} (x_i^2 - 10 cos(4 pi x_i))

    ``g`` has ``21^(d-1)`` local minima on the box, so the problem has many local
    Pareto fronts. The global Pareto front is the ZDT1 front
    ``f_1 = 1 - sqrt(f_0)``, ``f_0`` in ``[0, 1]``, at ``x_1 = ... = x_{d-1} = 0``.
    Both objectives are minimised. The reference point and maximum hypervolume
    are BoTorch's for ZDT1, which has the same front.
    """

    num_objectives = 2
    _ref_point = [11.0, 11.0]
    _max_hv = 120 + 2 / 3

    def __init__(
        self,
        dim: int,
        noise_std: Union[None, float, List[float]] = None,
        negate: bool = False,
        dtype: torch.dtype = torch.double,
    ) -> None:
        if dim < 2:
            raise ValueError(f"ZDT4 needs dim >= 2, got {dim}.")
        self.dim = dim
        self.continuous_inds = list(range(dim))
        self._bounds = [(0.0, 1.0)] + [(-5.0, 5.0) for _ in range(dim - 1)]
        super().__init__(noise_std=noise_std, negate=negate, dtype=dtype)

    @staticmethod
    def _g(X: Tensor) -> Tensor:
        # 1 + 10 (d - 1) + sum(x^2 - 10 cos(4 pi x)), written as a sum of
        # non-negative terms so that g = 1 is exact at the optimum
        X_d = X[..., 1:]
        return 1 + (X_d.pow(2) + 10 * (1 - torch.cos(4 * math.pi * X_d))).sum(dim=-1)

    def _evaluate_true(self, X: Tensor) -> Tensor:
        f_0 = X[..., 0]
        g = self._g(X)
        f_1 = g * (1 - (f_0 / g).sqrt())
        return torch.stack([f_0, f_1], dim=-1)

    def gen_pareto_front(self, n: int) -> Tensor:
        f_0 = torch.linspace(0, 1, n, dtype=self.bounds.dtype, device=self.bounds.device)
        f_X = torch.stack([f_0, 1 - f_0.sqrt()], dim=-1)
        return -f_X if self.negate else f_X


class FiveNodeMOFunctionNetwork(MultiObjectiveTestProblem):
    r"""5-node chain function network with a known Pareto front (see module doc).

    Two ways to evaluate it:

    * ``evaluate(X, idx=None)`` is the function-network interface of the
      template (``ackley_sin.py``), for EIFN / p-KGFN. With ``idx=None`` it
      returns all ``n_nodes = 8`` outputs, ``X.shape[:-1] + (8,)``. With ``idx``
      a node group (e.g. ``[4, 5]``, or any subset of one, or an int scalar-node
      index), ``X`` is that node's input (its ``active_input_indices`` columns of
      the network input, then its parents' outputs) and the group's selected
      outputs are returned.
    * ``problem(X)`` (BoTorch ``forward``) returns just the 2 objectives, so the
      problem can also be optimised as an ordinary black-box multi-objective
      problem, e.g. as a baseline for EIFN.

    Signs: the objectives are minimised, as in BoTorch's ZDT/DTLZ problems. With
    ``negate=True`` (the usual choice for BoTorch's maximising acquisition
    functions) the objectives, ``ref_point`` and ``gen_pareto_front`` are negated,
    and so are the final node's outputs from ``evaluate`` (columns
    ``objective_indices``). The intermediate outputs are never negated, because
    the next node needs them in its domain.

    ``evaluate`` is noise-free; ``forward`` adds ``noise_std`` noise to the
    objectives as in any BoTorch test problem.
    """

    dim = 20
    num_objectives = 2
    continuous_inds = list(range(20))
    _bounds = [(-5.0, 5.0) for _ in range(20)]
    _ref_point = [11.0, 11.0]
    _max_hv = 120 + 2 / 3

    # function-network structure, one entry per scalar node
    n_nodes = 8
    impose_assumption = True
    node_groups = [[0], [1, 2], [3], [4, 5], [6, 7]]
    parent_nodes = [[], [0], [0], [1, 2], [3], [3], [4, 5], [4, 5]]
    dag = DAG(parent_nodes=parent_nodes)
    active_input_indices = [
        list(range(20)),  # node 1: x1..x20
        list(range(10)),  # node 2, output a: x1..x10
        list(range(10)),  # node 2, output b: x1..x10
        list(range(20)),  # node 3: x1..x20
        list(range(20)),  # node 4, output a: x1..x20
        list(range(20)),  # node 4, output b: x1..x20
        [],  # node 5, objective 1: node 4 only
        [],  # node 5, objective 2: node 4 only
    ]
    # input dimension of each scalar node: active inputs + parent outputs
    node_dims = [20, 11, 11, 22, 21, 21, 2, 2]
    objective_indices = [6, 7]
    node_names = [
        "Styblinski-Tang (20-D)",
        "DTLZ2 (11-D, 2 objectives)",
        "Rastrigin (22-D)",
        "ZDT4 (21-D, 2 objectives)",
        "ZDT4 (2-D, 2 objectives)",
    ]
    constrained_input_indices = list(range(10))  # x1..x10 in [0, 1]

    def __init__(
        self,
        node_costs: Optional[Sequence[Union[float, int]]] = None,
        noise_std: Union[None, float, List[float]] = None,
        negate: bool = False,
        dtype: torch.dtype = torch.double,
    ) -> None:
        """Initialize the function network.

        Args:
            node_costs: Cost of evaluating each node, either one per node group
                (5 values) or one per scalar node (8 values, equal within a
                group). Defaults to 1 per group. ``self.node_costs`` is stored
                per scalar node, so ``node_costs[group[0]]`` is a group's cost.
            noise_std: Observation noise added by ``forward`` to the objectives.
            negate: If True, negate the objectives (for maximisation).
            dtype: dtype of the bounds, constraints and reference point.
        """
        super().__init__(noise_std=noise_std, negate=negate, dtype=dtype)
        self.n_groups = len(self.node_groups)
        self._set_node_costs(node_costs)

        # the literature test functions, each with its literature domain
        self.node_functions = torch.nn.ModuleList(
            [
                StyblinskiTang(dim=20, dtype=dtype),  # [-5, 5]^20
                DTLZ2(dim=11, num_objectives=2, dtype=dtype),  # [0, 1]^11
                Rastrigin(dim=22, dtype=dtype),  # [-5.12, 5.12]^22
                ZDT4(dim=21, dtype=dtype),  # [0, 1] x [-5, 5]^20
                ZDT4(dim=2, dtype=dtype),  # [0, 1] x [-5, 5]
            ]
        )

        # feasible network inputs: the bounds with x1..x10 cut to [0, 1]
        feasible_bounds = self.bounds.clone()
        feasible_bounds[0, self.constrained_input_indices] = 0.0
        feasible_bounds[1, self.constrained_input_indices] = 1.0
        self.register_buffer("feasible_bounds", feasible_bounds)

        # 0 <= x_i <= 1 for i = 1..10, in optimize_acqf's format
        self.inequality_constraints = self.get_inequality_constraints()

        # ranges of each scalar node's parent outputs (p-KGFN's parent_bounds)
        def box(lo: Sequence[float], hi: Sequence[float]) -> Tensor:
            return torch.tensor([list(lo), list(hi)], dtype=dtype)

        d2, ras, zd, zp = (
            _DTLZ2_DOMAIN,
            _RASTRIGIN_DOMAIN,
            _ZDT4_DISTANCE_DOMAIN,
            _ZDT4_POSITION_DOMAIN,
        )
        self.parent_bounds = [
            None,
            box([d2[0]], [d2[1]]),
            box([d2[0]], [d2[1]]),
            box([ras[0]] * 2, [ras[1]] * 2),
            box([zd[0]], [zd[1]]),
            box([zd[0]], [zd[1]]),
            box([zp[0], zd[0]], [zp[1], zd[1]]),
            box([zp[0], zd[0]], [zp[1], zd[1]]),
        ]
        # full input box of each node group: active inputs, then parent outputs
        self.node_input_bounds = []
        for group in self.node_groups:
            k = group[0]
            parts = [self.feasible_bounds[:, self.active_input_indices[k]]]
            if self.parent_bounds[k] is not None:
                parts.append(self.parent_bounds[k])
            self.node_input_bounds.append(torch.cat(parts, dim=-1))

        # min-max maps on each edge, (parent range) -> (child domain)
        self.output_scaling = {
            "node 1 -> DTLZ2 input": ((_NODE1_LO, _NODE1_HI), _DTLZ2_DOMAIN),
            "node 2 -> Rastrigin inputs": ((_NODE2_LO, _NODE2_HI), _RASTRIGIN_DOMAIN),
            "node 3 -> ZDT4 distance input": ((_NODE3_LO, _NODE3_HI), _ZDT4_DISTANCE_DOMAIN),
            "node 4 f1 -> ZDT4 position input": ((0.0, 1.0), _ZDT4_POSITION_DOMAIN),
            "node 4 f2 -> ZDT4 distance input": (
                (_NODE4_F2_LO, _NODE4_F2_HI),
                _ZDT4_DISTANCE_DOMAIN,
            ),
        }

    # ------------------------------------------------------------------ setup

    def _set_node_costs(self, node_costs: Optional[Sequence[Union[float, int]]]) -> None:
        if node_costs is None:
            node_costs = [1.0] * self.n_groups
        node_costs = list(node_costs)
        if len(node_costs) == self.n_groups:
            group_costs = node_costs
        elif len(node_costs) == self.n_nodes:
            group_costs = []
            for group in self.node_groups:
                costs = {node_costs[k] for k in group}
                if len(costs) != 1:
                    raise ValueError(
                        f"Nodes {group} are evaluated together, so they need the "
                        f"same cost; got {[node_costs[k] for k in group]}."
                    )
                group_costs.append(node_costs[group[0]])
        else:
            raise ValueError(
                f"node_costs needs {self.n_groups} values (one per node group) or "
                f"{self.n_nodes} (one per scalar node), got {len(node_costs)}."
            )
        self.group_costs = group_costs
        self.node_costs = [
            group_costs[g] for g, group in enumerate(self.node_groups) for _ in group
        ]

    def get_inequality_constraints(
        self, normalized: bool = False
    ) -> List[Tuple[Tensor, Tensor, float]]:
        r"""The input constraints ``0 <= x_i <= 1``, ``i = 1..10``, for BoTorch.

        Each tuple ``(indices, coefficients, rhs)`` encodes
        ``sum_i X[indices[i]] * coefficients[i] >= rhs``, the format of
        ``optimize_acqf(..., inequality_constraints=...)``.

        Args:
            normalized: If True, return the constraints for inputs normalised to
                the unit cube with ``self.bounds`` (``x = lb + (ub - lb) * z``),
                for optimisers that work on ``[0, 1]^20`` (as the BOFN code does).
                Then ``x_i`` in ``[0, 1]`` becomes ``z_i`` in ``[0.5, 0.6]``.
        """
        dtype = self.bounds.dtype
        constraints = []
        for i in self.constrained_input_indices:
            idx = torch.tensor([i], dtype=torch.long)
            if normalized:
                lb, ub = float(self.bounds[0, i]), float(self.bounds[1, i])
                width = ub - lb
                # x_i >= 0  <=>  width * z_i >= -lb
                constraints.append((idx, torch.tensor([width], dtype=dtype), -lb))
                # x_i <= 1  <=>  -width * z_i >= lb - 1
                constraints.append((idx, torch.tensor([-width], dtype=dtype), lb - 1.0))
            else:
                constraints.append((idx, torch.tensor([1.0], dtype=dtype), 0.0))  # x_i >= 0
                constraints.append((idx, torch.tensor([-1.0], dtype=dtype), -1.0))  # x_i <= 1
        return constraints

    # ------------------------------------------------------------- the nodes

    def _node1(self, Z: Tensor) -> Tensor:
        # Z = x1..x20; Styblinski-Tang, mapped onto DTLZ2's domain [0, 1]
        y = self.node_functions[0].evaluate_true(Z)
        return _minmax(y, _NODE1_LO, _NODE1_HI, *_DTLZ2_DOMAIN).unsqueeze(-1)

    def _node2(self, Z: Tensor) -> Tensor:
        # Z = (x1..x10, node 1); DTLZ2 (position x1), mapped onto Rastrigin's domain
        y = self.node_functions[1].evaluate_true(Z)
        return _minmax(y, _NODE2_LO, _NODE2_HI, *_RASTRIGIN_DOMAIN)

    def _node3(self, Z: Tensor) -> Tensor:
        # Z = (x1..x20, node 2a, node 2b); Rastrigin, mapped onto ZDT4's [-5, 5]
        y = self.node_functions[2].evaluate_true(Z)
        return _minmax(y, _NODE3_LO, _NODE3_HI, *_ZDT4_DISTANCE_DOMAIN).unsqueeze(-1)

    def _node4(self, Z: Tensor) -> Tensor:
        # Z = (x1..x20, node 3); ZDT4 with position x1. f1 = x1 is already in
        # ZDT4's position domain [0, 1]; f2 is mapped onto its distance domain.
        y = self.node_functions[3].evaluate_true(Z)
        f1 = _minmax(y[..., 0], 0.0, 1.0, *_ZDT4_POSITION_DOMAIN)
        f2 = _minmax(y[..., 1], _NODE4_F2_LO, _NODE4_F2_HI, *_ZDT4_DISTANCE_DOMAIN)
        return torch.stack([f1, f2], dim=-1)

    def _node5(self, Z: Tensor) -> Tensor:
        # Z = (node 4a, node 4b); ZDT4, the two objectives (raw, minimised)
        return self.node_functions[4].evaluate_true(Z)

    def _group_functions(self):
        return [self._node1, self._node2, self._node3, self._node4, self._node5]

    def _check_inputs(self, X: Tensor, box: Tensor, what: str) -> Tensor:
        """Reject inputs outside ``box`` by more than ``_INPUT_TOL``; clamp the rest."""
        if X.shape[-1] != box.shape[-1]:
            raise ValueError(
                f"Mismatch dimension: {what} has input dimension {box.shape[-1]}, "
                f"got {X.shape[-1]}."
            )
        lo, hi = box[0].to(X), box[1].to(X)
        if (X < lo - _INPUT_TOL).any() or (X > hi + _INPUT_TOL).any():
            raise ValueError(
                f"{what}: input outside its domain. Network inputs must satisfy "
                f"the bounds and 0 <= x_i <= 1 for i = 1..10: draw initial designs "
                f"in `feasible_bounds` and pass `inequality_constraints` to "
                f"optimize_acqf."
            )
        return torch.maximum(torch.minimum(X, hi), lo)

    def _evaluate_network(self, X: Tensor) -> Tensor:
        """All 8 node outputs, objectives not negated."""
        X = self._check_inputs(X, self.feasible_bounds, "The network")
        y1 = self._node1(X)
        y2 = self._node2(torch.cat([X[..., self.active_input_indices[1]], y1], dim=-1))
        y3 = self._node3(torch.cat([X[..., self.active_input_indices[3]], y2], dim=-1))
        y4 = self._node4(torch.cat([X[..., self.active_input_indices[4]], y3], dim=-1))
        y5 = self._node5(y4)
        return torch.cat([y1, y2, y3, y4, y5], dim=-1)

    def _resolve_idx(self, idx: Union[int, Sequence[int]]) -> Tuple[int, List[int]]:
        """Node group containing ``idx`` and the positions of ``idx`` within it."""
        members = [idx] if isinstance(idx, int) else list(idx)
        for g, group in enumerate(self.node_groups):
            if members and set(members) <= set(group):
                return g, [group.index(k) for k in members]
        raise ValueError(
            f"Invalid node index {idx}: give a node group from {self.node_groups}, "
            f"a subset of one, or a scalar node index."
        )

    # ------------------------------------------------------------ interfaces

    def evaluate(
        self,
        X: Tensor,
        idx: Optional[Union[int, Sequence[int]]] = None,
    ) -> Tensor:
        """Evaluate the function network (noise-free).

        Args:
            X: With ``idx=None``, network inputs, ``(batch_shape) x 20``. Otherwise
                the input of the node group containing ``idx``: its active
                network inputs followed by its parents' outputs,
                ``(batch_shape) x node_dims[idx]``.
            idx: Node to evaluate. ``None`` evaluates the whole network. A node
                group from ``node_groups`` (e.g. ``[1, 2]``), a subset of one, or
                an int scalar-node index evaluates that node only.

        Returns:
            ``X.shape[:-1] + (n_nodes,)`` if ``idx`` is None, otherwise
            ``X.shape[:-1] + (len(idx),)`` (``(1,)`` for an int). Columns
            ``objective_indices`` are negated if ``negate=True``.
        """
        if idx is None:
            Y = self._evaluate_network(X)
            if self.negate:
                Y = torch.cat([Y[..., :6], -Y[..., 6:]], dim=-1)
            return Y
        g, cols = self._resolve_idx(idx)
        Z = self._check_inputs(X, self.node_input_bounds[g], f"Node group {self.node_groups[g]}")
        out = self._group_functions()[g](Z)
        if self.negate and g == self.n_groups - 1:
            out = -out
        return out[..., cols]

    def _evaluate_true(self, X: Tensor) -> Tensor:
        # the objectives, not negated (BaseTestProblem.forward negates)
        return self._evaluate_network(X)[..., self.objective_indices]

    def network_to_objective(self, Y: Tensor) -> Tensor:
        """Objectives from network outputs ``Y`` (as returned by ``evaluate``)."""
        return Y[..., self.objective_indices]

    def get_objective(self) -> GenericMCMultiOutputObjective:
        """MC objective that picks the objectives out of network samples, for
        multi-objective acquisition functions on a GP network (use with
        ``negate=True`` so that larger is better)."""
        indices = list(self.objective_indices)
        return GenericMCMultiOutputObjective(lambda Y, X=None: Y[..., indices])

    # --------------------------------------------------------- Pareto front

    def gen_pareto_front(self, n: int) -> Tensor:
        """``n`` points on the network's Pareto front ``f2 = 1 - sqrt(f1)``."""
        f_0 = torch.linspace(0, 1, n, dtype=self.bounds.dtype, device=self.bounds.device)
        f_X = torch.stack([f_0, 1 - f_0.sqrt()], dim=-1)
        return -f_X if self.negate else f_X

    def gen_pareto_set(self, n: int, n_bisect: int = 100) -> Tensor:
        """``n`` feasible network inputs whose objectives lie on the Pareto front.

        For ``x1 = t`` on an even grid over ``[0, 1]``, moves x2..x20 along
        ``s * (a, ..., a, b, ..., b)``, ``s`` in ``[0, 1]``, where ``a`` and ``b``
        maximise ZDT4's distance term on ``[0, 1]`` and ``[-5, 5]``, and bisects
        on ``s`` for node 4's scaled f2 output to be 0 (so node 5's ``g = 1``).
        The Pareto set is not unique; this returns one input per ``t``.
        """
        dtype, device = self.bounds.dtype, self.bounds.device
        t = torch.linspace(0, 1, n, dtype=dtype, device=device)
        start = torch.zeros(n, self.dim, dtype=dtype, device=device)
        start[:, 0] = t
        direction = torch.zeros(self.dim, dtype=dtype, device=device)
        direction[1:10] = _ZDT4_ARGMAX_01
        direction[10:20] = _ZDT4_ARGMAX_55

        def u2(s: Tensor) -> Tensor:
            return self._evaluate_network(start + s.unsqueeze(-1) * direction)[..., 5]

        lo = torch.zeros(n, dtype=dtype, device=device)
        hi = torch.ones(n, dtype=dtype, device=device)
        if not ((u2(lo) < 0).all() and (u2(hi) > 0).all()):  # pragma: no cover
            raise RuntimeError("No sign change to bisect on; check the constants.")
        for _ in range(n_bisect):
            mid = (lo + hi) / 2
            below = u2(mid) < 0
            lo = torch.where(below, mid, lo)
            hi = torch.where(below, hi, mid)
        return start + ((lo + hi) / 2).unsqueeze(-1) * direction

    def max_hv_for_ref_point(self, ref_point: Union[Sequence[float], Tensor]) -> float:
        """Maximum hypervolume for another reference point.

        ``ref_point`` uses the same sign convention as ``self.ref_point``
        (negative when ``negate=True``). For a minimisation reference point
        ``(r1, r2)`` with ``r1, r2 >= 1`` this is ``r1 * r2 - 1/3``.
        """
        r = [float(v) for v in ref_point]
        if self.negate:
            r = [-v for v in r]
        r1, r2 = r
        if r1 <= 0 or r2 <= 0:
            return 0.0

        # HV = integral over f1 in [0, r1] of max(0, r2 - (1 - sqrt(min(f1, 1))))
        def antiderivative(a: float) -> float:
            if a <= 1:
                return (r2 - 1) * a + 2 / 3 * a**1.5
            return (r2 - 1) * a + 2 / 3 + (a - 1)

        a0 = (1 - r2) ** 2 if r2 < 1 else 0.0
        if r1 <= a0:
            return 0.0
        return antiderivative(r1) - antiderivative(a0)
