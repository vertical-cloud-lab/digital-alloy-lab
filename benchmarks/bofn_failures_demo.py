#!/usr/bin/env python3
"""Toy study for issue #274: what should a BOFN campaign do with a failed run?

The problem is a two-node function network:

    node 0 ("atomize"):  y0 = f0(x_1..x_D)   an intermediate, e.g. powder coarseness (D = --dim0, 2 by default)
    node 1 ("print"):    y1 = y0 * g(x_D+1)  the objective; needs node 0's output

and two kinds of failure:

    transient      each node evaluation fails with probability P_TRANSIENT, whatever its
                   inputs (a dirty crucible, an empty argon bottle)
    deterministic  node 1 fails whenever y0 > TAU (powder too coarse to spread). The rule is
                   about the intermediate y0; in x it covers curved blobs (D = 2) or slabs (D > 2).

y1 rises with y0, so the best feasible runs sit on the boundary y0 = TAU (f* = TAU), and an
optimizer that learns nothing from a failure keeps getting pulled back into the blobs.

Every strategy uses the same GP network (one SingleTaskGP per node) and the same EIFN-style
Monte Carlo expected improvement, evaluated jointly with any pending points on a fixed
candidate set. They differ only in what they do with a failed run, named for the Ax behaviour
each one mimics (see bofn-failed-vs-abandoned.md):

    drop            Ax 1.0-1.2.3: complete_trial with a missing metric marked the trial FAILED,
                    so the whole run is discarded and the arm can be suggested again.
    abandon         every failure ABANDONED: the run is discarded and its arm is pending for good.
    partial         Ax >= 1.2.4: complete_trial leaves the trial COMPLETED with incomplete
                    metrics, so node 0's data is fit and the arm stays pending.
    viability_x     Ax >= 1.3 as intended: transient -> FAILED (discarded, retryable),
                    deterministic -> ABANDONED (discarded, pending), plus AddExecutionViability:
                    a GP on 0/1 labels over x, with P(viable) >= 0.8 once 3 runs are abandoned.
    viability_node  the note's proposal: keep node 0's data, and give node 1 a viability node, a
                    GP on 0/1 labels over node 1's own inputs (x_D+1, measured y0), with the same 0.8
                    bound and 3-failure trigger. Transient failures are left out of the labels,
                    and nothing is pending.

Run:
    python benchmarks/bofn_failures_demo.py           # node 0 takes 2 inputs; ~4 min on 4 cores
    python benchmarks/bofn_failures_demo.py --dim0 6 --out benchmarks/bofn_failures_results_dim6.json  # ~7 min
    python benchmarks/bofn_failures_demo.py --quick   # smoke test, writes nothing
Writes benchmarks/bofn_failures_results.json; bofn_failures_visualize.py draws the figure.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import botorch
import torch
from botorch.fit import fit_gpytorch_mll
from botorch.models import SingleTaskGP
from botorch.models.transforms.input import Normalize
from botorch.models.transforms.outcome import Standardize
from gpytorch.mlls import ExactMarginalLogLikelihood
from torch.quasirandom import SobolEngine

torch.set_default_dtype(torch.double)

TAU = 0.7  # node 1 fails when y0 > TAU
F_STAR = TAU  # max of y0 * g(x3) with y0 <= TAU, at g(0.4) = 1
P_TRANSIENT = 0.15  # chance that any one node evaluation fails for reasons unrelated to its inputs
VIABLE_BOUND = 0.8  # AddExecutionViability's default feasibility_threshold
MIN_FAILURES = 3  # AddExecutionViability's default min_abandoned_trials
ETA = 1e-3  # BoTorch's default temperature for the sigmoid on outcome constraints
N_INIT_MIN = 6  # Sobol runs before BO (at least 2 per input), the same for every strategy
N_ITER = 30  # BO runs
N_MC = 64  # Monte Carlo samples through the network
N_SOBOL = 1024  # global candidates per iteration
N_LOCAL = 256  # candidates around the incumbent per iteration
CHUNK = 256  # candidates per acquisition batch (bounds memory)
NEAR = 0.1  # a deterministic failure this close (in x) to an earlier one counts as a repeat failure
STRATEGIES = ("drop", "abandon", "partial", "viability_x", "viability_node")
HERE = Path(__file__).resolve().parent


def f0(x: torch.Tensor, dim0: int) -> torch.Tensor:
    """Node 0: an intermediate in [0.05, 0.95]. With dim0 = 2 it is high in three blobs over
    (x1, x2); with more inputs, u and v are the means of the two halves of x_1..x_dim0."""
    k = max(1, dim0 // 2)
    u, v = x[..., :k].mean(-1), x[..., k:dim0].mean(-1)
    return 0.5 + 0.45 * torch.sin(2.5 * math.pi * u + 0.3) * torch.cos(1.5 * math.pi * v - 0.4)


def g(x3: torch.Tensor) -> torch.Tensor:
    return torch.exp(-((x3 - 0.4) ** 2) / 0.05)


def run_lab(x: torch.Tensor, u: torch.Tensor, dim0: int) -> dict:
    """One run of the network at x. u holds this run's two uniform draws for transient faults."""
    rec = {"x": x.tolist(), "y0": None, "y1": None, "node0": "COMPLETED", "node1": None}
    if u[0] < P_TRANSIENT:
        rec["node0"] = "FAILED"
        return rec
    y0 = float(f0(x, dim0))
    rec["y0"] = y0
    if u[1] < P_TRANSIENT:
        rec["node1"] = "FAILED"
    elif y0 > TAU:
        rec["node1"] = "ABANDONED"
    else:
        rec["node1"] = "COMPLETED"
        rec["y1"] = float(y0 * g(x[dim0]))
    return rec


def build_data(ledger: list[dict], strategy: str, dim0: int) -> dict:
    """Node datasets, viability labels and pending points, following the strategy's rules."""
    X0, Y0, X1, Y1, VX, VY, pending = [], [], [], [], [], [], []
    keep_partial = strategy in ("partial", "viability_node")
    for r in ledger:
        x = r["x"]
        full = r["node1"] == "COMPLETED"
        det = r["node1"] == "ABANDONED"
        transient = "FAILED" in (r["node0"], r["node1"])
        if full or (keep_partial and r["node0"] == "COMPLETED"):
            X0.append(x[:dim0])
            Y0.append(r["y0"])
        if full:
            X1.append([x[dim0], r["y0"]])
            Y1.append(r["y1"])
        if strategy in ("abandon", "partial") and not full:
            pending.append(x)
        if strategy == "viability_x":
            if det:
                pending.append(x)  # ABANDONED arms stay pending
            if not transient:  # FAILED trials carry no data, so no label
                VX.append(x)
                VY.append(0.0 if det else 1.0)
        if strategy == "viability_node" and (full or det):
            VX.append([x[dim0], r["y0"]])
            VY.append(0.0 if det else 1.0)
    use_viability = VY.count(0.0) >= MIN_FAILURES and VY.count(1.0) >= 1
    return {
        "X0": X0, "Y0": Y0, "X1": X1, "Y1": Y1,
        "VX": VX if use_viability else [], "VY": VY if use_viability else [],
        "pending": pending,
    }


def fit_gp(X: list, Y: list) -> SingleTaskGP:
    tX = torch.tensor(X)
    tY = torch.tensor(Y).unsqueeze(-1)
    gp = SingleTaskGP(
        tX, tY, input_transform=Normalize(d=tX.shape[-1]), outcome_transform=Standardize(m=1)
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fit_gpytorch_mll(ExactMarginalLogLikelihood(gp.likelihood, gp))
    gp.eval()
    return gp


@torch.no_grad()
def acquisition(cands, gp0, gp1, gpv, viability_on_x, X_pending, best_f, base, dim0):
    """MC expected improvement through the network, joint with the pending points.

    cands: b x (dim0 + 1). base: N_MC x 1 x Qmax x 3 standard normals for (node 0, node 1, viability),
    shared by every candidate (common random numbers); single-output posteriors take base
    samples without a trailing output dimension (BoTorch >= 0.17). An MC sample counts as an improvement
    only if its viability sample clears VIABLE_BOUND, as BoTorch does for outcome constraints.
    """
    b = cands.shape[0]
    Xq = cands.unsqueeze(1)
    if X_pending is not None:
        Xq = torch.cat([Xq, X_pending.unsqueeze(0).expand(b, -1, -1)], dim=1)
    q = Xq.shape[1]
    S = base.shape[0]
    z = base[:, :, :q, :].expand(S, b, q, 3)
    y0 = gp0.posterior(Xq[..., :dim0]).rsample_from_base_samples(torch.Size([S]), z[..., 0])[..., 0]
    X1 = torch.cat([Xq[..., dim0 : dim0 + 1].unsqueeze(0).expand(S, b, q, 1), y0.unsqueeze(-1)], dim=-1)
    y1 = gp1.posterior(X1).rsample_from_base_samples(
        torch.Size([1]), z[..., 1].unsqueeze(0)
    )[0, ..., 0]
    improvement = (y1 - best_f).clamp_min(0.0)
    if gpv is not None:
        if viability_on_x:
            v = gpv.posterior(Xq).rsample_from_base_samples(torch.Size([S]), z[..., 2])[..., 0]
        else:
            v = gpv.posterior(X1).rsample_from_base_samples(
                torch.Size([1]), z[..., 2].unsqueeze(0)
            )[0, ..., 0]
        improvement = improvement * torch.sigmoid((v - VIABLE_BOUND) / ETA)
    return improvement.max(dim=-1).values.mean(dim=0)


def suggest(ledger: list[dict], strategy: str, gen: torch.Generator, it: int, seed: int, dim0: int) -> torch.Tensor:
    d = build_data(ledger, strategy, dim0)
    sobol = SobolEngine(dim0 + 1, scramble=True, seed=10_000 * seed + it)
    if len(d["Y0"]) < 2 or len(d["Y1"]) < 2:
        return sobol.draw(1)[0]  # not enough data for a network yet
    gp0 = fit_gp(d["X0"], d["Y0"])
    gp1 = fit_gp(d["X1"], d["Y1"])
    gpv = fit_gp(d["VX"], d["VY"]) if d["VY"] else None
    best_f = max(d["Y1"])
    best_x = next(r["x"] for r in ledger if r["y1"] == best_f)
    local = (torch.tensor(best_x) + 0.05 * torch.randn(N_LOCAL, dim0 + 1, generator=gen)).clamp(0, 1)
    cands = torch.cat([sobol.draw(N_SOBOL), local])
    X_pending = torch.tensor(d["pending"]) if d["pending"] else None
    q_max = 1 + (0 if X_pending is None else X_pending.shape[0])
    base = torch.randn(N_MC, 1, q_max, 3, generator=gen)
    values = torch.cat([
        acquisition(c, gp0, gp1, gpv, strategy == "viability_x", X_pending, best_f, base, dim0)
        for c in cands.split(CHUNK)
    ])
    return cands[values.argmax()]


def run_one(strategy: str, seed: int, n_iter: int, dim0: int) -> dict:
    torch.set_num_threads(1)
    warnings.filterwarnings("ignore")  # jitter notices from near-duplicate GP inputs
    n_init = max(N_INIT_MIN, 2 * (dim0 + 1))
    gen = torch.Generator().manual_seed(seed)
    u = torch.rand(n_init + n_iter, 2, generator=torch.Generator().manual_seed(1000 + seed))
    X_init = SobolEngine(dim0 + 1, scramble=True, seed=seed).draw(n_init)
    ledger, best_curve, t0 = [], [], time.time()
    det_bo = repeats = 0
    for i in range(n_init + n_iter):
        x = X_init[i] if i < n_init else suggest(ledger, strategy, gen, i, seed, dim0)
        rec = run_lab(x, u[i], dim0)
        if i >= n_init and rec["node1"] == "ABANDONED":
            det_bo += 1
            earlier = [r["x"] for r in ledger if r["node1"] == "ABANDONED"]
            if earlier and torch.cdist(x[None], torch.tensor(earlier)).min() < NEAR:
                repeats += 1
        ledger.append(rec)
        ys = [r["y1"] for r in ledger if r["y1"] is not None]
        best_curve.append(max(ys) if ys else None)
    return {
        "strategy": strategy, "seed": seed,
        "best_curve": best_curve,
        "regret_curve": [None if b is None else F_STAR - b for b in best_curve],
        "n_init": n_init,
        "deterministic_failures_bo": det_bo,
        "transient_failures": sum("FAILED" in (r["node0"], r["node1"]) for r in ledger),
        "repeat_failures": repeats,
        "seconds": round(time.time() - t0, 1),
        "ledger": ledger,
    }


def _round(obj, nd: int = 5):
    """Round floats for a compact results file."""
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, dict):
        return {k: _round(v, nd) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_round(v, nd) for v in obj]
    return obj


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--iters", type=int, default=N_ITER)
    ap.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    ap.add_argument("--dim0", type=int, default=2, help="number of inputs to node 0")
    ap.add_argument("--quick", action="store_true", help="2 seeds x 3 BO runs, no file written")
    ap.add_argument("--out", type=Path, default=HERE / "bofn_failures_results.json")
    args = ap.parse_args()
    if args.quick:
        args.seeds, args.iters = 2, 3

    # how much of node 0's input space fails at node 1
    pts = SobolEngine(args.dim0, scramble=True, seed=0).draw(2**16)
    frac = float((f0(pts, args.dim0) > TAU).double().mean())
    print(f"dim0 = {args.dim0}: node 1 fails on {frac:.1%} of node 0's input space; f* = {F_STAR}")

    jobs = [(s, k, args.iters, args.dim0) for k in range(args.seeds) for s in STRATEGIES]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(run_one, *zip(*jobs)))
    print(f"{len(results)} runs in {time.time() - t0:.0f} s")

    summary = {}
    for s in STRATEGIES:
        rs = [r for r in results if r["strategy"] == s]
        final = torch.tensor([r["regret_curve"][-1] for r in rs])
        det = torch.tensor([float(r["deterministic_failures_bo"]) for r in rs])
        rep = torch.tensor([float(r["repeat_failures"]) for r in rs])
        n = len(rs)
        se = lambda t: float(t.std(unbiased=True) / math.sqrt(n)) if n > 1 else float("nan")
        summary[s] = {
            "final_regret_mean": float(final.mean()), "final_regret_se": se(final),
            "final_regret_median": float(torch.quantile(final, 0.5)),
            "solved_within_0.02": int((final <= 0.02).sum()),
            "deterministic_failures_bo_mean": float(det.mean()), "deterministic_failures_bo_se": se(det),
            "repeat_failures_mean": float(rep.mean()),
            "n_seeds": n,
        }
        print(
            f"{s:15s} final regret {summary[s]['final_regret_mean']:.3f} ± {summary[s]['final_regret_se']:.3f}"
            f" (median {summary[s]['final_regret_median']:.3f}, {summary[s]['solved_within_0.02']}/{n} within 0.02)"
            f" | failures in BO {summary[s]['deterministic_failures_bo_mean']:.1f} of {args.iters}"
            f" | repeat failures {summary[s]['repeat_failures_mean']:.1f}"
        )
    if args.quick:
        return
    out = {
        "settings": {
            "TAU": TAU, "F_STAR": F_STAR, "P_TRANSIENT": P_TRANSIENT, "VIABLE_BOUND": VIABLE_BOUND,
            "MIN_FAILURES": MIN_FAILURES, "dim0": args.dim0, "N_INIT": results[0]["n_init"],
            "N_ITER": args.iters, "N_MC": N_MC,
            "N_SOBOL": N_SOBOL, "N_LOCAL": N_LOCAL, "NEAR": NEAR, "seeds": args.seeds,
            "failure_fraction_node0_inputs": frac,
            "torch": torch.__version__, "botorch": botorch.__version__,
        },
        "summary": summary,
        "runs": results,
    }
    args.out.write_text(json.dumps(_round(out), separators=(",", ":")) + "\n")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
