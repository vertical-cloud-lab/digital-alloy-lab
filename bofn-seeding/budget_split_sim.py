#!/usr/bin/env python3
"""Toy check of how to split 25 design runs between seeds and optimizer rounds (#275).

This is a deliberately small, flat-GP simulation. It is not a model of the alloy campaign; it
only asks how the split behaves under assumptions we can state:

- 6-D unit box (a normalized composition space). The response depends mostly on 3 hidden
  "active" dimensions, like an alloy whose strength is driven by a few additions.
- A "known family" bump of height 0.7 where the baselines sit (AlSi10Mg-like: good, not best),
  a better bump of height 1.0 somewhere else, and a smaller decoy. Observation noise sd 0.02.
- One free weak point (the 6063 A-block runs), which doesn't count toward the 25.
- Baseline seeds sit in the known-family bump. Agent seeds are drawn around a guess with
  sd 0.2 in the active dimensions. The guess is the better bump ("agent right") or the known
  family ("agent wrong": the literature points back at what is already known).
- Space-filling seeds are scrambled Sobol points. The remaining runs go to batches of 3
  picked by qLogEI over a 2048-point Sobol candidate set (the last batch may be smaller).

Every split is run on the same problem instances (same seeds), so differences are paired.

    python bofn-seeding/budget_split_sim.py --reps 30 --workers 4
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import warnings
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import torch

HERE = pathlib.Path(__file__).resolve().parent
D, D_ACTIVE, BUDGET, BATCH, NOISE = 6, 3, 25, 3, 0.02

# (name, baselines, agent seeds, space-filling seeds). Everything else in the 25 is BO.
SPLITS = [
    ("3+3+3 (proposed)", 3, 3, 3),
    ("2+2+2", 2, 2, 2),
    ("2+3+1", 2, 3, 1),
    ("2+0+1", 2, 0, 1),
    ("2+0+4", 2, 0, 4),
    ("2+4+0", 2, 4, 0),
    ("3+3+6", 3, 3, 6),
    ("all 25 Sobol (no BO)", 2, 0, 23),
]
SCENARIOS = ["agent right", "agent wrong"]


def make_problem(rng):
    active = rng.choice(D, D_ACTIVE, replace=False)
    while True:
        c_opt, c_known, c_decoy = rng.uniform(0.15, 0.85, size=(3, D_ACTIVE))
        if np.linalg.norm(c_opt - c_known) > 0.5 and np.linalg.norm(c_decoy - c_known) > 0.3:
            break
    tilt = rng.normal(0, 0.05, D)

    def f(X):
        X = np.atleast_2d(X)
        A = X[:, active]
        g = lambda c, h, s: h * np.exp(-((A - c) ** 2).sum(1) / (2 * s**2))
        return g(c_opt, 1.0, 0.18) + g(c_known, 0.7, 0.25) + g(c_decoy, 0.4, 0.15) + X @ tilt * 0.5

    return dict(f=f, active=active, c_opt=c_opt, c_known=c_known)


def around(rng, prob, centre, n, sd):
    X = rng.uniform(0, 1, size=(n, D))
    X[:, prob["active"]] = np.clip(centre + rng.normal(0, sd, size=(n, D_ACTIVE)), 0, 1)
    return X


def run_one(job):
    rep, scenario, split = job
    from botorch.acquisition.logei import qLogExpectedImprovement
    from botorch.fit import fit_gpytorch_mll
    from botorch.models import SingleTaskGP
    from botorch.optim import optimize_acqf_discrete
    from botorch.sampling import SobolQMCNormalSampler
    from gpytorch.mlls import ExactMarginalLogLikelihood
    from scipy.stats import qmc

    warnings.filterwarnings("ignore")
    torch.set_num_threads(1)
    name, n_base, n_agent, n_sf = split
    prob_rng = np.random.default_rng(1000 + rep)  # same problem for every split and scenario
    prob = make_problem(prob_rng)
    f = prob["f"]
    rng = np.random.default_rng(5000 + rep)
    weak = rng.uniform(0, 1, size=(1, D))  # 6063: random point, free
    base = around(rng, prob, prob["c_known"], 3, 0.05)[:n_base]
    centre = prob["c_opt"] if scenario == "agent right" else prob["c_known"]
    agent = around(rng, prob, centre, 4, 0.2)[:n_agent]
    sob = qmc.Sobol(D, scramble=True, seed=7000 + rep).random(32)[:n_sf]
    X = np.vstack([weak, base, agent, sob])
    tags = ["free"] + ["seed"] * (len(X) - 1)
    pool = torch.tensor(qmc.Sobol(D, scramble=True, seed=9000 + rep).random(2048), dtype=torch.double)
    noise_rng = np.random.default_rng(11000 + rep)
    Y = f(X) + noise_rng.normal(0, NOISE, len(X))
    while len(X) - 1 < BUDGET:
        q = min(BATCH, BUDGET - (len(X) - 1))
        tx, ty = torch.tensor(X), torch.tensor(Y).unsqueeze(-1)
        gp = SingleTaskGP(tx, ty)
        try:
            fit_gpytorch_mll(ExactMarginalLogLikelihood(gp.likelihood, gp))
        except Exception:
            pass
        acq = qLogExpectedImprovement(gp, best_f=ty.max(), sampler=SobolQMCNormalSampler(torch.Size([128])))
        cand, _ = optimize_acqf_discrete(acq, q=q, choices=pool, unique=True)
        Xn = cand.numpy()
        X = np.vstack([X, Xn])
        Y = np.concatenate([Y, f(Xn) + noise_rng.normal(0, NOISE, len(Xn))])
        tags += ["bo"] * len(Xn)
    truth = f(X)[1:]  # the 25 design runs, noise-free
    grid = np.vstack([pool.numpy(), around(np.random.default_rng(rep), prob, prob["c_opt"], 4000, 0.03)])
    f_max = f(grid).max()
    best_base = f(base).max() if n_base else f(around(np.random.default_rng(rep), prob, prob["c_known"], 3, 0.05)).max()
    curve = np.maximum.accumulate(truth)
    return dict(
        rep=rep, scenario=scenario, split=name,
        best=float(curve[-1]), regret=float(f_max - curve[-1]),
        best_at_12=float(curve[11]), beat_baseline=bool(curve[-1] > best_base + 0.05),
        found_better_bump=bool(curve[-1] > 0.8),
    )


def summarize(rows):
    out = []
    for sc in SCENARIOS:
        for name, *_ in SPLITS:
            r = [x for x in rows if x["scenario"] == sc and x["split"] == name]
            if not r:
                continue
            best = np.array([x["best"] for x in r])
            out.append(dict(
                scenario=sc, split=name, n=len(r),
                mean_best=best.mean(), se_best=best.std(ddof=1) / np.sqrt(len(r)),
                mean_best_at_12=np.mean([x["best_at_12"] for x in r]),
                p_beat_baseline=np.mean([x["beat_baseline"] for x in r]),
                p_better_bump=np.mean([x["found_better_bump"] for x in r]),
            ))
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--reps", type=int, default=30)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--out", type=pathlib.Path, default=HERE / "results" / "budget_split")
    a = p.parse_args()
    jobs = [(r, sc, s) for r in range(a.reps) for sc in SCENARIOS for s in SPLITS]
    with ProcessPoolExecutor(a.workers) as ex:
        rows = list(ex.map(run_one, jobs, chunksize=4))
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "runs.json").write_text(json.dumps(rows, indent=0) + "\n")
    summary = summarize(rows)
    with open(a.out / "summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary[0]))
        w.writeheader()
        w.writerows({k: (round(v, 4) if isinstance(v, float) else v) for k, v in s.items()} for s in summary)
    for sc in SCENARIOS:
        print(f"\n{sc}: mean best of 25 (+/- 1 se), best after 12, P(beat best baseline by 0.05), P(found the better bump)")
        for s in summary:
            if s["scenario"] == sc:
                print(f"  {s['split']:<22} {s['mean_best']:.3f} +/- {s['se_best']:.3f}   {s['mean_best_at_12']:.3f}"
                      f"   {s['p_beat_baseline']:.2f}   {s['p_better_bump']:.2f}")


if __name__ == "__main__":
    main()
