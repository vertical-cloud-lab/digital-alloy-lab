"""Run the clocked benchmark's experiments (pre-registered in PREREGISTRATION.md).

    python run.py optima                       # optima and screen ceilings of every truth -> optima.json
    python run.py e1 [--workers 4] [--seeds 0-9]
    python run.py one <kappa> <facility> <policy> <seed>     # one campaign, printed

Results: results/<experiment>/<tag>.json, one file per campaign.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from lab import Lab
from policies import POLICIES, sobol
from truth import Truth, optimum, screen_filter

HERE = Path(__file__).parent
OPT_FILE = HERE / "optima.json"
BUDGET = 250_000.0
HORIZON = {"auto": 365.0, "conv": 4 * 365.0}
T_FRAC = {"T1": 0.60, "T2": 0.80}

# the time-machine campaigns: same physics, different goals
TM_GOALS = [dict(lam=0.3, ln_rmax=0.95), dict(lam=0.6, ln_rmax=0.95), dict(lam=0.1, ln_rmax=0.75)]


def truth_for(kappa, goal=None, **kw):
    goal = goal or {}
    return Truth(kappa, lam=goal.get("lam", 0.3), ln_rmax=goal.get("ln_rmax", 0.95), **kw)


def optima():
    out = {}
    for k in (0.0, 0.5, 1.0):
        T = truth_for(k)
        v, x = optimum(T)
        sv, _ = optimum(T, comp_filter=screen_filter())
        out[f"k{k:g}"] = dict(opt=v, x=[round(float(t), 4) for t in x], screen=sv, screen_frac=sv / v)
    for i, g in enumerate(TM_GOALS):
        T = truth_for(1.0, g)
        v, x = optimum(T)
        out[f"tm{i}"] = dict(opt=v, x=[round(float(t), 4) for t in x], goal=g)
    json.dump(out, open(OPT_FILE, "w"), indent=1)
    print(json.dumps(out, indent=1))


def load_opt():
    return json.load(open(OPT_FILE))


def campaign(spec):
    """spec: dict(exp, kappa, fac, pol, seed, [goal_idx, prior, group_mode, cur_group, epoch_rho, epoch_U])."""
    t0 = time.time()
    O = load_opt()
    kappa, fac, pol, seed = spec["kappa"], spec["fac"], spec["pol"], spec["seed"]
    gi = spec.get("goal_idx")
    goal = TM_GOALS[gi] if gi is not None else None
    truth = truth_for(kappa, goal, epoch_rho=spec.get("epoch_rho"), epoch_U=spec.get("epoch_U"))
    opt = O[f"tm{gi}"]["opt"] if gi is not None else O[f"k{kappa:g}"]["opt"]
    targets = {k: f * opt for k, f in T_FRAC.items()}
    conv = fac.startswith("conv")
    lab = Lab(truth, fac, seed, spec.get("budget", BUDGET), HORIZON["conv" if conv else "auto"], targets,
              epoch=spec.get("epoch", 0))
    for c in sobol(256, truth.ncomp, 4000 + seed):  # CALPHAD on 256 compositions for every policy, paid, instant
        lab.calphad(c)
    route = "custom" if fac == "conv_lots" else "us"
    P = POLICIES[pol](seed, truth, group_mode=spec.get("group_mode"), prior=spec.get("prior"),
                      cur_group=spec.get("cur_group", 0), powder_route=route)
    res = lab.run(P, stop_at=spec.get("stop_at", "T2"))
    res["kg_flat"], res["kg_used"] = getattr(P, "kg_flat", 0), getattr(P, "kg_used", 0)
    res.update(exp=spec["exp"], kappa=kappa, fac=fac, pol=pol, seed=seed, opt=opt, targets=targets,
               budget=lab.budget, horizon=lab.horizon, seconds=round(time.time() - t0, 1),
               variant=spec.get("variant"), goal_idx=gi, campaign=spec.get("campaign"))
    if spec.get("keep_lab"):
        res["_lab"] = lab
    return res


def tag(spec):
    parts = [spec["fac"], spec["pol"]]
    if spec.get("variant"):
        parts.append(spec["variant"])
    if spec.get("campaign") is not None:
        parts.append(f"c{spec['campaign']}")
    return f"k{spec['kappa']:g}_" + "_".join(parts) + f"_s{spec['seed']}"


def save(res):
    d = HERE / "results" / res["exp"]
    d.mkdir(parents=True, exist_ok=True)
    spec = dict(kappa=res["kappa"], fac=res["fac"], pol=res["pol"], seed=res["seed"], variant=res.get("variant"),
                campaign=res.get("campaign"))
    res = {k: v for k, v in res.items() if not k.startswith("_")}
    json.dump(res, open(d / (tag(spec) + ".json"), "w"))


def _run_one(spec):
    try:
        res = campaign(spec)
        save(res)
        h = res["hit"]
        return f"{tag(spec):48s} T1 {h.get('T1', ['-'])[0]!s:>8.6} T2 {h.get('T2', ['-'])[0]!s:>8.6} spent {res['spent']:9.0f} {res['seconds']:6.1f}s"
    except Exception as e:  # keep the sweep going; report the failure
        import traceback
        return f"{tag(spec)} FAILED {e!r}\n{traceback.format_exc()}"


def specs_e1(seeds):
    out = []
    for kappa in (1.0, 0.0):
        for fac, pol in (("conv_lots", "conv"), ("conv_atomizer", "conv"), ("vertical", "tiered"), ("vertical", "gpbo"),
                         ("vertical", "bofn"), ("vertical", "pkgfn"), ("vertical", "random")):
            out += [dict(exp="e1", kappa=kappa, fac=fac, pol=pol, seed=s) for s in seeds]
    return out


def specs_e2(seeds):
    out = [dict(exp="e2", kappa=1.0, fac=fac, pol=pol, seed=s) for fac in ("nearterm", "vertical_ih")
           for pol in ("tiered", "bofn") for s in seeds]
    # E2b: the move to production powder, confirmed on the partner's machine (campaigns run to T2c)
    out += [dict(exp="e2b", kappa=1.0, fac="vertical", pol=pol, seed=s, stop_at="T2c")
            for pol in ("bofn_confirm", "bofn_confirm_early") for s in seeds]
    return out


def parse_seeds(arg):
    a, b = arg.split("-") if "-" in arg else (arg, arg)
    return list(range(int(a), int(b) + 1))


def sweep(specs, workers):
    t0 = time.time()
    # longest first: network policies, then the rest
    order = {"pkgfn": 0, "bofn_confirm": 1, "bofn_confirm_early": 1, "bofn": 1, "gpbo": 2, "tiered": 3, "random": 4, "conv": 5}
    specs = sorted(specs, key=lambda s: order.get(s["pol"], 9))
    with Pool(workers) as pool:
        for line in pool.imap_unordered(_run_one, specs):
            print(f"[{time.time() - t0:7.0f}s] {line}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    seeds = parse_seeds(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else list(range(10))
    if cmd == "optima":
        optima()
    elif cmd == "one":
        k, fac, pol, s = float(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5])
        r = campaign(dict(exp="one", kappa=k, fac=fac, pol=pol, seed=s))
        print(json.dumps({k: v for k, v in r.items() if k not in ("score_hist",)}, indent=1))
        print("score_hist", r["score_hist"][:20])
    elif cmd in ("e1", "e2"):
        sweep({"e1": specs_e1, "e2": specs_e2}[cmd](seeds), workers)
    else:
        import experiments  # provenance and stretch experiments

        experiments.main(cmd, seeds, workers)
