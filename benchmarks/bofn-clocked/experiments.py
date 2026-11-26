"""E3 (provenance) and E5 (stretch: one search across alloy families), as pre-registered.

    python run.py e3a [--workers 4] [--seeds 0-9]
    python run.py e3b [--workers 4] [--seeds 0-7]
    python run.py e5  [--workers 4] [--seeds 0-7]
"""
from __future__ import annotations

import json
import time
from multiprocessing import Pool

import numpy as np

import run as R
from lab import Lab
from model import records
from policies import POLICIES, sobol
from truth import FAMILIES, SIG_BUILD, SIG_COUPON, SIG_Q, CrossTruth, Truth, optimum

NC = 4
# E3a: the other lab's printer runs on a shifted ridge and reads a little less dense; its frames read high
OTHER = dict(shift=0.08, rho=-0.03, U=0.04)
# two reference alloys both labs have made (and that the time-machine campaigns re-make): a lean screened alloy and
# a Zr-inoculated high-solute one, each at a reasonable laser setting
REFS = [np.array([0.30, 0.20, 0.10, 0.0, 0.35, 0.22, 0.05]), np.array([0.60, 0.45, 0.80, 0.0, 0.45, 0.32, 0.10])]


# --------------------------------------------------------------------------- E3a: another lab's data
def lab_records(truth, designs, rng, site, ext, pv_seed, bars_on=2):
    """Records of one powder + one six-coupon build per design (+ bars on the densest coupons), at a site."""
    out = {"q": [], "rho": [], "U": [], "corr": []}
    for i, x in enumerate(designs):
        c, a = x[:NC], float(x[NC])
        s, f, g = (float(t) for t in truth.calphad(c))
        q_true = float(truth.q(a, g))
        q_meas = q_true + rng.normal(0, SIG_Q)
        out["q"].append(dict(a=a, g=g, gas=0.0, y=q_meas, site=site))
        pv = [(x[NC + 1], x[NC + 2])] if len(x) > NC + 1 else []
        pv += [tuple(p) for p in sobol(8, 2, pv_seed + i)[: 6 - len(pv)]]
        off = rng.normal(0, SIG_BUILD)
        rows = []
        for P, v in pv:
            rho_true = float(truth.rho(P, v, f, g, q_true, "ih", "us", site)) + off
            rho_meas = float(np.clip(rho_true + rng.normal(0, SIG_COUPON), 0, 1))
            out["rho"].append(dict(P=float(P), v=float(v), f=f, g=g, q=q_meas, pt=0.0, gas=0.0, y=rho_meas, site=site,
                                   ext=ext))
            rows.append((rho_meas, rho_true))
        for rho_meas, rho_true in sorted(rows)[-bars_on:]:
            out["U"].append(dict(s=s, rho=rho_meas, y=truth.measure_U(s, rho_true, rng, site), site=site))
    return out


def merge(*recs):
    return {k: sum((list(r.get(k, [])) for r in recs), []) for k in ("q", "rho", "U", "corr")}


def specs_e3a(seeds):
    out = []
    for s in seeds:
        rng = np.random.default_rng(70_000 + s)
        sign = 1.0 if rng.random() < 0.5 else -1.0
        site_kw = dict(site_shift={"other": sign * OTHER["shift"]}, site_rho={"other": OTHER["rho"]},
                       site_U={"other": OTHER["U"]})
        T = Truth(1.0, **site_kw)
        other_designs = sobol(8, NC + 1, 60_000 + s)  # the other lab's own campaign: 8 alloys, 6 coupons each
        own_refs = lab_records(T, REFS, rng, "own", 0.0, 80_000 + s)
        other_refs = lab_records(T, REFS, rng, "other", 1.0, 81_000 + s)
        other = lab_records(T, other_designs, rng, "other", 1.0, 82_000 + s)
        naive_other = merge(other_refs, other)
        for part in ("rho",):  # naive pooling: provenance dropped, the other printer looks like ours
            naive_other[part] = [dict(r, ext=0.0, site="own") for r in naive_other[part]]
        naive_other["U"] = [dict(r, site="own") for r in naive_other["U"]]
        naive_other["q"] = [dict(r, site="own") for r in naive_other["q"]]
        variants = {"separate": (own_refs, None), "naive": (merge(own_refs, naive_other), None),
                    "site": (merge(own_refs, other_refs, other), "site")}
        for v, (prior, gm) in variants.items():
            out.append(dict(exp="e3a", kappa=1.0, fac="vertical", pol="bofn", seed=s, variant=v, prior=prior,
                            group_mode=gm, truth_kw=site_kw))
    return out


# --------------------------------------------------------------------------- E3b: a time machine
def poor(recs):
    """The same experiments recorded the usual way: process settings not written down (nominal values filled in),
    no campaign labels, only the parts that worked (dense coupons and their bars), final corrosion results only."""
    keep = [r for r in recs["rho"] if r["y"] >= 0.8]
    out = {"q": [dict(r, a=0.5, epoch=0) for r in recs["q"]],
           "rho": [dict(r, P=0.35, v=0.10, epoch=0) for r in keep],
           "U": [dict(r, epoch=0) for r in recs["U"] if r["rho"] >= 0.8],
           "corr": [dict(r) for r in recs["corr"] if r.get("final")]}
    return out


def tm_records(lab):
    rec = records(lab)
    for r in rec["corr"]:
        r["final"] = r["noise"] <= 0.05 ** 2
    for k in rec:
        for r in rec[k]:
            r["epoch"] = r.get("epoch", lab.epoch)
    return rec


def tm_campaign(seed, e, prior, group_mode, drift_rho, drift_U):
    goal = R.TM_GOALS[e]
    T = Truth(1.0, lam=goal["lam"], ln_rmax=goal["ln_rmax"], epoch_rho=drift_rho, epoch_U=drift_U)
    opt = R.load_opt()[f"tm{e}"]["opt"]
    targets = {k: f * opt for k, f in R.T_FRAC.items()}
    lab = Lab(T, "vertical", 1000 * e + seed, R.BUDGET, R.HORIZON["auto"], targets, epoch=e)
    for c in sobol(256, NC, 4000 + seed):
        lab.calphad(c)
    rng = np.random.default_rng(90_000 + 10 * seed + e)
    refs = [(float(rng.uniform(0, 30)), x) for x in REFS]  # repeats shuffled over time
    P = POLICIES["bofn"](1000 * e + seed, T, group_mode=group_mode, prior=prior, cur_group=e, refs=refs)
    t0 = time.time()
    res = lab.run(P, stop_at="T2")
    res.update(opt=opt, targets=targets, seconds=round(time.time() - t0, 1))
    return res, lab


def tm_chain(seed):
    """Campaign 0 once, then campaigns 1 and 2 under each history."""
    rng = np.random.default_rng(95_000 + seed)
    drift_rho = {0: 0.0, 1: float(rng.normal(0, 0.03)), 2: float(rng.normal(0, 0.03))}
    drift_U = {0: 0.0, 1: float(rng.normal(0, 0.03)), 2: float(rng.normal(0, 0.03))}
    rows = []
    r0, lab0 = tm_campaign(seed, 0, None, None, drift_rho, drift_U)
    rows.append(dict(history="all", campaign=0, **{k: r0[k] for k in ("hit", "spent", "t_end", "opt", "targets", "seconds", "counts")}))
    rec0 = tm_records(lab0)
    for hist in ("none", "documented", "poor"):
        hist_recs = [rec0]
        for e in (1, 2):
            if hist == "none":
                prior, gm = None, None
            elif hist == "documented":
                prior, gm = merge(*hist_recs), "epoch"
            else:
                prior, gm = merge(*[poor(h) for h in hist_recs]), None
            r, lab = tm_campaign(seed, e, prior, gm, drift_rho, drift_U)
            rows.append(dict(history=hist, campaign=e, **{k: r[k] for k in ("hit", "spent", "t_end", "opt", "targets", "seconds", "counts")}))
            hist_recs.append(tm_records(lab))
    out = dict(exp="e3b", seed=seed, drift_rho=drift_rho, drift_U=drift_U, rows=rows)
    d = R.HERE / "results" / "e3b"
    d.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(d / f"chain_s{seed}.json", "w"))
    return f"e3b seed {seed}: " + "; ".join(f"{r['history']}/c{r['campaign']} T1 {r['hit'].get('T1', ['-'])[0]!s:.5} T2 {r['hit'].get('T2', ['-'])[0]!s:.5}" for r in rows)


# --------------------------------------------------------------------------- E5: across alloy families
def cross_opt():
    O = R.load_opt()
    if "cross" not in O:
        v, x = optimum(CrossTruth(1.0), n=300_000)
        O["cross"] = dict(opt=v, x=[round(float(t), 4) for t in x])
        json.dump(O, open(R.OPT_FILE, "w"), indent=1)
    return O["cross"]["opt"]


def e5_campaign(spec):
    seed, variant = spec["seed"], spec["variant"]
    T = CrossTruth(1.0)
    opt = cross_opt()
    targets = {k: f * opt for k, f in R.T_FRAC.items()}
    dims = FAMILIES.get(variant)
    budget = R.BUDGET if dims is None else R.BUDGET / 3
    lab = Lab(T, "vertical", seed, budget, 240.0, targets)
    C = sobol(256, 6, 4000 + seed)
    if dims is not None:
        C[:, [j for j in range(6) if j not in dims]] = 0.0
    for c in C:
        lab.calphad(c)
    P = POLICIES["bofn"](seed, T, comp_dims=dims, wip=None if dims is None else (1, 2))
    t0 = time.time()
    res = lab.run(P, stop_at=None)
    res.update(exp="e5", seed=seed, variant=variant, opt=opt, targets=targets, seconds=round(time.time() - t0, 1),
               kappa=1.0, fac="vertical", pol="bofn")
    d = R.HERE / "results" / "e5"
    d.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(d / f"{variant}_s{seed}.json", "w"))
    return f"e5 {variant:7s} s{seed}: hit {res['hit']} final {res['score_hist'][-1]} {res['seconds']}s"


def _e3a_one(spec):
    T = Truth(1.0, **spec.pop("truth_kw"))
    s = dict(spec)
    res = campaign_with_truth(s, T)
    R.save(res)
    return f"e3a {spec['variant']:9s} s{spec['seed']}: hit {res['hit']} spent {res['spent']:.0f} {res['seconds']}s"


def campaign_with_truth(spec, T):
    opt = R.load_opt()["k1"]["opt"]
    targets = {k: f * opt for k, f in R.T_FRAC.items()}
    lab = Lab(T, spec["fac"], spec["seed"], R.BUDGET, R.HORIZON["auto"], targets)
    for c in sobol(256, NC, 4000 + spec["seed"]):
        lab.calphad(c)
    P = POLICIES[spec["pol"]](spec["seed"], T, group_mode=spec.get("group_mode"), prior=spec.get("prior"))
    t0 = time.time()
    res = lab.run(P, stop_at="T2")
    res.update(exp=spec["exp"], kappa=1.0, fac=spec["fac"], pol=spec["pol"], seed=spec["seed"], opt=opt,
               targets=targets, budget=lab.budget, horizon=lab.horizon, seconds=round(time.time() - t0, 1),
               variant=spec["variant"], goal_idx=None, campaign=None)
    return res


def main(cmd, seeds, workers):
    t0 = time.time()
    if cmd == "e3a":
        jobs, fn = specs_e3a(seeds), _e3a_one
    elif cmd == "e3b":
        jobs, fn = list(seeds), tm_chain
    elif cmd == "e5":
        cross_opt()
        jobs = [dict(seed=s, variant=v) for s in seeds for v in ("global", "7xxx", "AlSi", "AlMgSc")]
        fn = e5_campaign
    else:
        raise KeyError(cmd)
    with Pool(workers) as pool:
        for line in pool.imap_unordered(fn, jobs):
            print(f"[{time.time() - t0:7.0f}s] {line}", flush=True)
