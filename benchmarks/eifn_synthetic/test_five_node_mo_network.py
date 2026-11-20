"""Tests for the 5-node multi-objective function network (issue #265).

Run from the repository root:

    python -m pytest benchmarks/eifn_synthetic -q
"""

from __future__ import annotations

import math
import warnings

import numpy as np
import pytest
import torch
from botorch.optim.parameter_constraints import evaluate_feasibility
from botorch.utils.multi_objective.hypervolume import Hypervolume
from botorch.utils.multi_objective.pareto import is_non_dominated
from botorch.utils.sampling import draw_sobol_samples

from benchmarks.eifn_synthetic import five_node_mo_network as fnm
from benchmarks.eifn_synthetic.five_node_mo_network import (
    ZDT4,
    FiveNodeMOFunctionNetwork,
)

warnings.filterwarnings("ignore")


@pytest.fixture(scope="module")
def problem():
    return FiveNodeMOFunctionNetwork()


@pytest.fixture(scope="module")
def X_feasible(problem):
    """Sobol points in the feasible box plus its 2 extreme corners and 64
    random corners (the corners are where the scaling bounds are tightest)."""
    X = draw_sobol_samples(problem.feasible_bounds, n=4096, q=1, seed=0).squeeze(-2)
    lo, hi = problem.feasible_bounds
    gen = torch.Generator().manual_seed(0)
    mask = torch.rand(64, problem.dim, generator=gen, dtype=lo.dtype) < 0.5
    corners = torch.where(mask, hi, lo)
    return torch.cat([X, lo.unsqueeze(0), hi.unsqueeze(0), corners])


def _extremes(fn, lo, hi, n=200_001):
    """Min and max of a smooth 1-D function: dense grid + golden section."""
    xs = np.linspace(lo, hi, n)
    ys = fn(xs)
    step = (hi - lo) / (n - 1)
    out = []
    for sign in (1.0, -1.0):
        i = int(np.argmin(sign * ys))
        a, b = max(lo, xs[i] - step), min(hi, xs[i] + step)
        f = lambda x: sign * float(fn(np.array([x]))[0])  # noqa: E731
        r = (math.sqrt(5) - 1) / 2
        for _ in range(200):
            c, d = b - r * (b - a), a + r * (b - a)
            if f(c) < f(d):
                b = d
            else:
                a = c
        best = min([(a + b) / 2, lo, hi], key=f)
        out.append(sign * f(best))
    return out  # [min, max]


def test_scaling_constants_are_the_per_coordinate_extremes():
    st = lambda x: 0.5 * (x**4 - 16 * x**2 + 5 * x)  # noqa: E731
    ras = lambda x: x**2 + 10 * (1 - np.cos(2 * np.pi * x))  # noqa: E731
    zdt4 = lambda x: x**2 + 10 * (1 - np.cos(4 * np.pi * x))  # noqa: E731
    assert _extremes(st, 0, 1) == pytest.approx([fnm._ST_MIN_01, fnm._ST_MAX_01], abs=1e-9)
    assert _extremes(st, -5, 5) == pytest.approx([fnm._ST_MIN_55, fnm._ST_MAX_55], abs=1e-9)
    assert _extremes(ras, 0, 1)[1] == pytest.approx(fnm._RAS_MAX_01, abs=1e-9)
    assert _extremes(ras, -5, 5)[1] == pytest.approx(fnm._RAS_MAX_55, abs=1e-9)
    assert _extremes(ras, -5.12, 5.12)[1] == pytest.approx(fnm._RAS_MAX_55, abs=1e-9)
    assert _extremes(zdt4, 0, 1)[1] == pytest.approx(fnm._ZDT4_MAX_01, abs=1e-9)
    assert _extremes(zdt4, -5, 5)[1] == pytest.approx(fnm._ZDT4_MAX_55, abs=1e-9)
    assert zdt4(np.array([fnm._ZDT4_ARGMAX_01]))[0] == pytest.approx(fnm._ZDT4_MAX_01, abs=1e-9)
    assert zdt4(np.array([fnm._ZDT4_ARGMAX_55]))[0] == pytest.approx(fnm._ZDT4_MAX_55, abs=1e-9)


def test_structure(problem):
    p = problem
    assert p.dim == 20 and p.n_nodes == 8 and p.n_groups == 5
    assert p.dag.get_n_nodes() == 8 and p.dag.get_root_nodes() == [0]
    assert sorted(k for g in p.node_groups for k in g) == list(range(8))
    # chain 1 -> 2 -> 3 -> 4 -> 5 between groups
    for g in range(1, 5):
        for k in p.node_groups[g]:
            assert p.parent_nodes[k] == p.node_groups[g - 1]
    # each scalar node's input = its active inputs + its parents
    for k in range(8):
        assert p.node_dims[k] == len(p.active_input_indices[k]) + len(p.parent_nodes[k])
    # the inputs the issue asks for
    assert p.active_input_indices[0] == list(range(20))  # node 1: all 20
    assert p.active_input_indices[1] == list(range(10))  # node 2: x1..x10 (+ node 1)
    assert p.active_input_indices[3] == list(range(20))  # node 3: all 20 (+ node 2)
    assert p.active_input_indices[4] == list(range(20))  # node 4: all 20 (+ node 3)
    assert p.active_input_indices[6] == []  # node 5: node 4's outputs only
    # nodes 2, 4 and 5 are multi-output
    assert [len(g) for g in p.node_groups] == [1, 2, 1, 2, 2]
    # input domain: [-5, 5]^20 bounds, x1..x10 cut to [0, 1]
    assert torch.equal(p.bounds, torch.tensor([[-5.0] * 20, [5.0] * 20], dtype=p.bounds.dtype))
    assert torch.equal(p.feasible_bounds[:, :10], torch.tensor([[0.0] * 10, [1.0] * 10], dtype=p.bounds.dtype))
    assert torch.equal(p.feasible_bounds[:, 10:], p.bounds[:, 10:])


def test_node_input_domains_are_within_literature_domains(problem):
    """Each node's input box (feasible inputs + parent ranges) lies in the
    literature domain of the function it evaluates."""
    for box, fn in zip(problem.node_input_bounds, problem.node_functions):
        assert box.shape == fn.bounds.shape
        assert (box[0] >= fn.bounds[0]).all() and (box[1] <= fn.bounds[1]).all()
    # and the literature domains are the published ones
    st, dtlz2, ras, zdt4_21, zdt4_2 = problem.node_functions
    assert (st.bounds == torch.tensor([[-5.0], [5.0]], dtype=st.bounds.dtype)).all()
    assert (dtlz2.bounds == torch.tensor([[0.0], [1.0]], dtype=st.bounds.dtype)).all()
    assert (ras.bounds == torch.tensor([[-5.12], [5.12]], dtype=st.bounds.dtype)).all()
    for z in (zdt4_21, zdt4_2):
        assert z.bounds[:, 0].tolist() == [0.0, 1.0]
        assert (z.bounds[:, 1:] == torch.tensor([[-5.0], [5.0]], dtype=st.bounds.dtype)).all()


def test_outputs_lie_in_the_next_nodes_domain(problem, X_feasible):
    Y = problem.evaluate(X_feasible)
    assert Y.shape == (X_feasible.shape[0], 8)
    assert torch.isfinite(Y).all()
    for k in range(8):
        for child in range(8):
            if k not in problem.parent_nodes[child]:
                continue
            j = problem.parent_nodes[child].index(k)
            lo, hi = problem.parent_bounds[child][:, j]
            assert (Y[:, k] >= lo).all() and (Y[:, k] <= hi).all(), (k, child)


def test_node_by_node_evaluation_matches_full_network(problem, X_feasible):
    X = X_feasible[:256]
    Y = problem.evaluate(X)
    for group in problem.node_groups:
        k = group[0]
        Z = torch.cat([X[:, problem.active_input_indices[k]], Y[:, problem.parent_nodes[k]]], -1)
        assert Z.shape[-1] == problem.node_dims[k]
        torch.testing.assert_close(problem.evaluate(Z, idx=group), Y[:, group])
        for m in group:  # single members and int indices work too
            torch.testing.assert_close(problem.evaluate(Z, idx=[m]), Y[:, [m]])
            torch.testing.assert_close(problem.evaluate(Z, idx=m), Y[:, [m]])
    # batch shapes
    Xb = X[:24].reshape(4, 6, 20)
    assert problem.evaluate(Xb).shape == (4, 6, 8)
    assert problem(Xb).shape == (4, 6, 2)


def test_input_constraints(problem):
    p = problem
    cons = p.inequality_constraints
    assert len(cons) == 20
    for idx, coef, rhs in cons:
        assert idx.dtype == torch.long and idx.ndim == 1 and int(idx) < 10
        assert coef.shape == idx.shape and isinstance(rhs, float)
    X = draw_sobol_samples(p.bounds, n=2048, q=1, seed=1).squeeze(-2)
    X[:512, :10] = X[:512, :10].abs() / 5  # make a quarter of them feasible
    in_box = ((X >= p.feasible_bounds[0]) & (X <= p.feasible_bounds[1])).all(-1)
    assert in_box.any() and (~in_box).any()
    feasible = evaluate_feasibility(X.unsqueeze(-2), inequality_constraints=cons)
    assert torch.equal(feasible, in_box)
    # the unit-cube version describes the same set
    Z = (X - p.bounds[0]) / (p.bounds[1] - p.bounds[0])
    cons_n = p.get_inequality_constraints(normalized=True)
    assert torch.equal(evaluate_feasibility(Z.unsqueeze(-2), inequality_constraints=cons_n), in_box)


def test_infeasible_inputs_are_rejected_and_tiny_violations_clamped(problem):
    X = problem.gen_pareto_set(3)
    bad = X.clone()
    bad[0, 3] = -0.5  # x4 < 0
    with pytest.raises(ValueError, match="outside its domain"):
        problem.evaluate(bad)
    with pytest.raises(ValueError):
        problem(bad)
    with pytest.raises(ValueError, match="Mismatch dimension"):
        problem.evaluate(X[:, :19])
    with pytest.raises(ValueError, match="Invalid node index"):
        problem.evaluate(X, idx=[3, 4])
    nudged = X.clone()
    nudged[:, 2] = -1e-9  # SLSQP-sized violation of x3 >= 0
    clean = X.clone()
    clean[:, 2] = 0.0
    torch.testing.assert_close(problem.evaluate(nudged), problem.evaluate(clean))


def test_forward_negate_and_reference_point(X_feasible):
    p = FiveNodeMOFunctionNetwork()
    pn = FiveNodeMOFunctionNetwork(negate=True)
    X = X_feasible[:128]
    torch.testing.assert_close(p(X), p.evaluate(X)[:, p.objective_indices])
    torch.testing.assert_close(pn(X), -p(X))
    Yn = pn.evaluate(X)
    torch.testing.assert_close(Yn[:, :6], p.evaluate(X)[:, :6])  # intermediates not negated
    torch.testing.assert_close(pn.network_to_objective(Yn), pn(X))
    torch.testing.assert_close(pn.get_objective()(Yn), pn(X))
    assert p.ref_point.tolist() == [11.0, 11.0] and pn.ref_point.tolist() == [-11.0, -11.0]
    assert p.max_hv == pn.max_hv == pytest.approx(120 + 2 / 3)
    torch.testing.assert_close(pn.gen_pareto_front(5), -p.gen_pareto_front(5))
    # noise only in forward
    pnoise = FiveNodeMOFunctionNetwork(noise_std=0.1)
    assert not torch.equal(pnoise(X), p(X))
    torch.testing.assert_close(pnoise.evaluate(X), p.evaluate(X))


def test_node_costs():
    assert FiveNodeMOFunctionNetwork().node_costs == [1.0] * 8
    p = FiveNodeMOFunctionNetwork(node_costs=[1, 2, 3, 4, 5])
    assert p.group_costs == [1, 2, 3, 4, 5]
    assert [p.node_costs[g[0]] for g in p.node_groups] == [1, 2, 3, 4, 5]
    assert FiveNodeMOFunctionNetwork(node_costs=p.node_costs).group_costs == [1, 2, 3, 4, 5]
    with pytest.raises(ValueError):
        FiveNodeMOFunctionNetwork(node_costs=[1, 2, 3])
    with pytest.raises(ValueError):
        FiveNodeMOFunctionNetwork(node_costs=[1, 2, 9, 3, 4, 4, 5, 5])


def test_no_input_beats_the_known_front(problem, X_feasible):
    F = problem(X_feasible)
    assert (F[:, 0] >= 0).all() and (F[:, 0] <= 1).all()
    assert (F[:, 1] >= 1 - F[:, 0].sqrt() - 1e-12).all()


def test_pareto_set_attains_the_known_front(problem):
    n = 101
    X = problem.gen_pareto_set(n)
    assert ((X >= problem.feasible_bounds[0]) & (X <= problem.feasible_bounds[1])).all()
    # x2..x10 end up strictly inside (0, 1)
    assert (X[:, 1:10] > 0).all() and (X[:, 1:10] < 1).all()
    F = problem(X)
    torch.testing.assert_close(F, problem.gen_pareto_front(n), atol=1e-10, rtol=0)
    # every point is non-dominated
    assert is_non_dominated(-F).all()


def test_max_hypervolume(problem):
    pn = FiveNodeMOFunctionNetwork(negate=True)
    front = pn.gen_pareto_front(20_001)
    hv = Hypervolume(ref_point=pn.ref_point).compute(front)
    assert hv == pytest.approx(pn.max_hv, abs=1e-3) and hv <= pn.max_hv
    for ref in ([-1.1, -1.1], [-0.5, -0.8], [-3.0, -0.2], [-0.04, -2.0]):
        hv = Hypervolume(ref_point=torch.tensor(ref, dtype=front.dtype)).compute(front)
        assert hv == pytest.approx(pn.max_hv_for_ref_point(ref), abs=1e-3)
    assert problem.max_hv_for_ref_point([11.0, 11.0]) == pytest.approx(120 + 2 / 3)
    assert problem.max_hv_for_ref_point([1.1, 1.1]) == pytest.approx(1.21 - 1 / 3)


def test_zdt4_matches_the_published_formula():
    z = ZDT4(dim=10)
    X = draw_sobol_samples(z.bounds, n=64, q=1, seed=2).squeeze(-2)
    g = 1 + 10 * 9 + (X[:, 1:] ** 2 - 10 * torch.cos(4 * math.pi * X[:, 1:])).sum(-1)
    f2 = g * (1 - (X[:, 0] / g).sqrt())
    torch.testing.assert_close(z(X), torch.stack([X[:, 0], f2], -1))
    X_opt = torch.zeros(5, 10, dtype=X.dtype)
    X_opt[:, 0] = torch.linspace(0, 1, 5, dtype=X.dtype)
    torch.testing.assert_close(z(X_opt), z.gen_pareto_front(5))


def test_runs_with_an_eifn_gp_network_and_constrained_optimize_acqf():
    """One multi-objective EIFN-style step: GP network over the 8 scalar nodes,
    qLogEHVI on network samples, constrained optimize_acqf."""
    from botorch.acquisition.multi_objective.logei import (
        qLogExpectedHypervolumeImprovement,
    )
    from botorch.optim import optimize_acqf
    from botorch.sampling import StochasticSampler
    from botorch.utils.multi_objective.box_decompositions.non_dominated import (
        FastNondominatedPartitioning,
    )

    from benchmarks.partial_kgfn.gp_network import GaussianProcessNetwork, fit_gp_network
    from benchmarks.partial_kgfn.utils import construct_obs_set

    torch.manual_seed(0)
    p = FiveNodeMOFunctionNetwork(negate=True)
    X = draw_sobol_samples(p.feasible_bounds, n=21, q=1, seed=0).squeeze(-2)
    Y = p.evaluate(X)
    train_X, train_Y = construct_obs_set(X, Y, p.parent_nodes, p.active_input_indices)
    model = GaussianProcessNetwork(
        train_X=train_X,
        train_Y=train_Y,
        dag=p.dag,
        active_input_indices=p.active_input_indices,
        node_groups=p.node_groups,
        node_dims=p.node_dims,
    )
    fit_gp_network(model)
    acqf = qLogExpectedHypervolumeImprovement(
        model=model,
        ref_point=p.ref_point.tolist(),
        partitioning=FastNondominatedPartitioning(
            ref_point=p.ref_point, Y=p.network_to_objective(Y)
        ),
        sampler=StochasticSampler(torch.Size([32])),
        objective=p.get_objective(),
    )
    candidate, _ = optimize_acqf(
        acqf,
        bounds=p.bounds,
        q=1,
        num_restarts=2,
        raw_samples=32,
        inequality_constraints=p.inequality_constraints,
        options={"maxiter": 20},
    )
    assert evaluate_feasibility(candidate.unsqueeze(0), p.inequality_constraints).all()
    assert torch.isfinite(p.evaluate(candidate)).all()
