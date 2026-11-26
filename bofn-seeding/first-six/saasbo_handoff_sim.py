#!/usr/bin/env python3
"""Does SAASBO explore well enough when it starts from six hand-picked alloys? (#275)

A semi-physical toy on the campaign's own 15-element palette. It is not a model of the campaign.
It asks one question under stated assumptions: with 25 runs in batches of 3, is it better to

    A  hand the optimizer the six hand-picked seeds and let it choose the other 19,
    B  add three sparse Sobol points first (nine seeds), or
    C  add three hand-picked "axis-covering" alloys first (nine seeds), each switching on
       elements that none of the six contains,

and does the answer change between SAASBO (fully Bayesian GP with the SAAS prior) and a standard GP?
Controls: nine Sobol seeds with no hand-picked ones, and pure random search.

Ground truth
------------
"Strength" is a sum of saturating terms (solid solution, L1_2 precipitation, grain refinement,
eutectic network, Mg-Si / Zn-Mg / Cu age hardening), multiplied by a printability factor that
drops when a crack-prone solute mix has neither a grain refiner nor enough eutectic, minus a
penalty for too much intermetallic and a fixed mineral-burden charge on Sc, Er, Ce and Li (so the
objective is "strong and lean", as in #277, and the optimum is not simply "add scandium"). Every coefficient is redrawn per instance (lognormal, sd 0.25),
so no single guess of mine decides the result. In half of the instances a hidden two-element
synergy (60-140 MPa) is added for a pair of elements that no seed contains together; that is the
case where exploration should pay. Observation noise is 10 MPa.

Observations arrive one batch late by default (`--delay 1`): the batch chosen now is still pending
when the next one is chosen, as in the campaign, where strength comes back weeks after a run.

    python bofn-seeding/first-six/saasbo_handoff_sim.py --reps 16 --workers 2
    python bofn-seeding/first-six/saasbo_handoff_sim.py --reps 30 --models gp random --workers 2
    python bofn-seeding/first-six/saasbo_handoff_sim.py --summarize
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import time
import warnings

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "results" / "saasbo_handoff"

EL = ["Mn", "Cr", "Zr", "Mg", "Si", "Cu", "Ti", "Fe", "Ni", "Ce", "Sc", "Li", "Er", "Zn", "Sn"]
# Design box (wt%). PR #72's recommended caps, with Fe, Ni, Zr, Ti, Er, Mg and Sn opened to the levels
# of the published LPBF alloys the seeds come from (Al-Fe-Zr, Al-Mg-Zr, Al-Ni eutectics, high-Mg Al-Mg-Si).
UB = dict(Mn=5.0, Cr=3.0, Zr=1.5, Mg=7.0, Si=12.0, Cu=4.0, Ti=1.0, Fe=2.5, Ni=3.0, Ce=6.0, Sc=0.8, Li=2.0,
          Er=1.0, Zn=8.0, Sn=0.5)
FLOOR = dict(Mn=0.3, Cr=0.2, Zr=0.2, Mg=0.3, Si=0.5, Cu=0.3, Ti=0.1, Fe=0.3, Ni=0.3, Ce=0.5, Sc=0.1, Li=0.2,
             Er=0.1, Zn=0.5, Sn=0.05)
D = len(EL)
UBV = np.array([UB[e] for e in EL])
BUDGET, BATCH, NOISE = 25, 3, 10.0

# The six seeds proposed in README.md, and the three optional extras (wt%).
SIX = {
    "D1 AlSi10Mg": dict(Si=10.0, Mg=0.35),
    "D2 Scalmalloy-type": dict(Mg=4.6, Sc=0.66, Zr=0.42, Mn=0.49),
    "S1 Al-Mn-Cr-Zr": dict(Mn=5.0, Cr=0.8, Zr=0.6),
    "S2 Al-Fe-Mg-Zr": dict(Fe=1.9, Mg=1.0, Zr=1.0),
    "S3 AlSi3.5Mg2.5": dict(Si=3.5, Mg=2.5),
    "S4 Al-Mg-Zr": dict(Mg=3.6, Zr=1.2),
}
EXTRA_AXIS = {
    "E1 Al-Zn-Mg-Cu-Zr": dict(Zn=5.5, Mg=2.3, Cu=1.5, Zr=1.0),
    "E2 Al-Mg-Mn-Er-Zr": dict(Mg=4.5, Mn=0.5, Er=0.8, Zr=0.5),
    "E3 Al-Ni-Mn-Ti": dict(Ni=3.0, Mn=2.0, Ti=0.5),
}
FREE = {"6063": dict(Mg=0.55, Si=0.40, Fe=0.20)}  # the A-block runs: a point that costs no design run


def vec(d: dict) -> np.ndarray:
    v = np.zeros(D)
    for k, val in d.items():
        v[EL.index(k)] = val
    return v


# ---------------------------------------------------------------- ground truth
def make_problem(rng: np.random.Generator, seeds_wt: np.ndarray, synergy: bool):
    """One random instance of the toy strength function. Inputs are wt% arrays of shape (n, 15)."""
    j = lambda: float(np.exp(rng.normal(0.0, 0.25)))  # noqa: E731  coefficient jitter
    k = {name: j() for name in (
        "ss_mg", "ss_mn", "ss_cr", "ss_cu", "ss_zn", "ss_li", "ppt", "gb", "eu_si", "eu_fe", "eu_ni", "eu_ce",
        "mgsi", "znmg", "cu", "culi", "crack", "brittle", "sn")}
    pot = dict(Sc=1.0, Zr=0.33 * j(), Er=0.30 * j(), Ti=0.12 * j())      # L1_2 potency per wt%
    ref = dict(Sc=1.0, Zr=0.6 * j(), Ti=0.5 * j(), Er=0.4 * j())          # grain-refining potency per wt%
    pair = None
    if synergy:
        present = seeds_wt > 0
        together = (present[:, :, None] & present[:, None, :]).any(0)
        cands = [(a, b) for a in range(D) for b in range(a + 1, D) if not together[a, b] and EL[a] != "Sn" and EL[b] != "Sn"]
        a, b = cands[rng.integers(len(cands))]
        pair = dict(a=a, b=b, ca=rng.uniform(0.35, 0.8), cb=rng.uniform(0.35, 0.8), h=rng.uniform(60.0, 140.0))

    def f(W: np.ndarray, parts: bool = False):
        W = np.atleast_2d(W).astype(float)
        c = {e: W[:, i] for i, e in enumerate(EL)}
        ss = (18 * k["ss_mg"] * c["Mg"] ** 0.67 + 26 * k["ss_mn"] * c["Mn"] ** 0.9 + 28 * k["ss_cr"] * c["Cr"] ** 0.9
              + 18 * k["ss_cu"] * c["Cu"] ** 0.67 + 6 * k["ss_zn"] * c["Zn"] ** 0.67 + 25 * k["ss_li"] * c["Li"])
        L = sum(pot[e] * c[e] for e in pot)
        ppt = 260 * k["ppt"] * (1 - np.exp(-L / 0.45))
        R = sum(ref[e] * c[e] for e in ref)
        gb = 90 * k["gb"] * (1 - np.exp(-R / 0.25))
        eut = (150 * k["eu_si"] * (1 - np.exp(-c["Si"] / 4.0)) + 70 * k["eu_fe"] * (1 - np.exp(-c["Fe"] / 1.2))
               + 45 * k["eu_ni"] * (1 - np.exp(-c["Ni"] / 2.0)) + 40 * k["eu_ce"] * (1 - np.exp(-c["Ce"] / 4.0)))
        age = (90 * k["mgsi"] * np.minimum(np.minimum(c["Mg"] / 1.0, c["Si"] / 0.6), 1.0)
               + 180 * k["znmg"] * np.minimum(np.minimum(c["Zn"] / 5.5, c["Mg"] / 2.3), 1.0)
               + 110 * k["cu"] * np.minimum(c["Cu"] / 4.0, 1.0)
               + 60 * k["culi"] * np.minimum(np.minimum(c["Cu"] / 3.0, c["Li"] / 1.0), 1.0))
        total = ss + ppt + gb + eut + age
        strength = 35.0 + 650.0 * np.tanh(total / 650.0)
        if pair is not None:
            xa, xb = W[:, pair["a"]] / UBV[pair["a"]], W[:, pair["b"]] / UBV[pair["b"]]
            strength = strength + pair["h"] * np.exp(-((xa - pair["ca"]) ** 2 + (xb - pair["cb"]) ** 2) / (2 * 0.22**2))
        # hot-cracking: crack-prone solute mix, mitigated by grain refiners or a large eutectic fraction
        h_mg = np.exp(-(((c["Mg"] - 2.0) / 1.6) ** 2)) * (c["Mg"] > 0.2)
        h = (1.0 * h_mg + 1.2 * np.minimum(c["Zn"] / 5.0, 1.0) * (c["Mg"] > 0.5) + 0.9 * np.minimum(c["Cu"] / 3.0, 1.0)
             + 0.4 * np.minimum(c["Li"] / 1.0, 1.0)
             + 0.8 * ((c["Mg"] + c["Si"] > 0.8) & (c["Si"] < 2.5) & (c["Si"] > 0.2) & (c["Mg"] > 0.2)))
        mit = 2.2 * np.minimum(R / 0.5, 1.0) + c["Si"] / 4.0 + c["Fe"] / 2.0 + c["Ni"] / 4.0 + c["Ce"] / 6.0 + c["Mn"] / 8.0
        p_crack = 1.0 / (1.0 + np.exp(-(k["crack"] * h - mit - 0.35) / 0.18))
        brittle = np.maximum(0.0, c["Fe"] / 2.5 + c["Ni"] / 3.0 + c["Ce"] / 6.0 + c["Cr"] / 3.0 + c["Mn"] / 6.0 + c["Si"] / 14.0 - 1.2)
        y = strength * (1.0 - 0.6 * p_crack) - 100.0 * k["brittle"] * brittle - 40.0 * k["sn"] * c["Sn"] / 0.5
        # mineral-burden charge (fixed, not jittered): Scalmalloy's 0.66 wt% Sc costs about 113 MPa
        burden = 120.0 * c["Sc"] / 0.7 + 40.0 * c["Er"] / 0.8 + 20.0 * c["Ce"] / 6.0 + 30.0 * c["Li"] / 2.0
        y = y - burden
        if parts:
            return dict(y=y, p_crack=p_crack, strength=strength, brittle=brittle, burden=burden)
        return y

    return f, pair


# ---------------------------------------------------------------- candidates
def sparse_pool(rng: np.random.Generator, n: int, anchors: np.ndarray | None = None) -> np.ndarray:
    """Sparse compositions: 1-5 additions, each between its floor and cap, at most 15 wt% in total."""
    out = []
    while len(out) < n:
        kk = rng.choice([1, 2, 3, 4, 5], p=[0.05, 0.25, 0.35, 0.25, 0.10])
        idx = rng.choice(D, size=kk, replace=False)
        w = np.zeros(D)
        for i in idx:
            e = EL[i]
            w[i] = FLOOR[e] + rng.random() ** 1.2 * (UB[e] - FLOOR[e])
        if w.sum() <= 15.0:
            out.append(w)
    P = np.array(out)
    if anchors is not None and len(anchors):
        # local moves around every anchor: scale, drop or add one element (lets the optimizer exploit)
        loc = []
        for a in anchors:
            on = np.nonzero(a)[0]
            for _ in range(60):
                w = a * np.exp(rng.normal(0, 0.25, D))
                if rng.random() < 0.35 and len(on) > 1:
                    w[rng.choice(on)] = 0.0
                if rng.random() < 0.5:
                    i = rng.integers(D)
                    w[i] = FLOOR[EL[i]] + rng.random() * (UB[EL[i]] - FLOOR[EL[i]]) * 0.6
                w = np.minimum(w, UBV)
                w[(w > 0) & (w < np.array([FLOOR[e] for e in EL]))] = 0.0
                if 0.5 < w.sum() <= 15.0 and (w > 0).sum() <= 5:
                    loc.append(w)
        P = np.vstack([P, np.array(loc)])
    return np.round(P, 2)


def sobol_sparse(seed: int, n: int) -> np.ndarray:
    """First n feasible sparse points of a scrambled Sobol sequence.

    One sequence in 2 * 15 + 1 dimensions: the first drives how many additions (2-4), the next 15 rank
    the elements (the lowest keys are switched on), and the last 15 set their levels.
    """
    from scipy.stats import qmc

    U = qmc.Sobol(2 * D + 1, scramble=True, seed=seed).random(256)
    out = []
    for u in U:
        kk = 2 + min(int(u[0] * 3), 2)
        idx = np.argsort(u[1:D + 1])[:kk]
        w = np.zeros(D)
        for i in idx:
            e = EL[i]
            w[i] = FLOOR[e] + u[D + 1 + i] * (UB[e] - FLOOR[e])
        if w.sum() <= 15.0:
            out.append(np.round(w, 2))
        if len(out) == n:
            break
    return np.array(out)


# ---------------------------------------------------------------- one run
STRATEGIES = ["six", "six+3sobol", "six+3axis", "nine-sobol"]


def initial_design(strategy: str, rep: int) -> np.ndarray:
    six = np.array([vec(v) for v in SIX.values()])
    if strategy == "six":
        return six
    if strategy == "six+3sobol":
        return np.vstack([six, sobol_sparse(7000 + rep, 3)])
    if strategy == "six+3axis":
        return np.vstack([six, np.array([vec(v) for v in EXTRA_AXIS.values()])])
    if strategy == "nine-sobol":
        return sobol_sparse(7000 + rep, 9)
    raise ValueError(strategy)


def run_one(job):
    rep, strategy, model_name, delay, nuts = job
    import torch

    warnings.filterwarnings("ignore")
    torch.set_num_threads(1)
    torch.manual_seed(20000 + rep)
    t0 = time.time()
    six = np.array([vec(v) for v in SIX.values()])
    all_hand = np.vstack([six, np.array([vec(v) for v in EXTRA_AXIS.values()])])
    prob_rng = np.random.default_rng(1000 + rep)          # same instance for every strategy and model
    f, pair = make_problem(prob_rng, all_hand, synergy=(rep % 2 == 1))
    pool = sparse_pool(np.random.default_rng(9000 + rep), 3500, anchors=all_hand)
    free = np.array([vec(v) for v in FREE.values()])
    X0 = initial_design(strategy, rep)
    noise_rng = np.random.default_rng(11000 + rep)
    X = np.vstack([free, X0])
    Y = f(X) + noise_rng.normal(0, NOISE, len(X))
    seen_elements = (X > 0).any(0)
    n_seed = len(X0)
    pending: list[np.ndarray] = []      # batches chosen but not yet observed
    new_el_runs = 0                      # optimizer runs that switch on an element absent from every seed
    picks = []
    tpool = torch.tensor(pool / UBV, dtype=torch.double)
    used = np.zeros(len(pool), dtype=bool)
    rng = np.random.default_rng(13000 + rep)

    def n_design():
        return len(X) - 1 + sum(len(p) for p in pending)

    while n_design() < BUDGET:
        q = min(BATCH, BUDGET - n_design())
        avail = np.nonzero(~used)[0]
        if model_name == "random":
            choice = rng.choice(avail, size=q, replace=False)
        else:
            from botorch.acquisition.logei import qLogNoisyExpectedImprovement
            from botorch.models.transforms.outcome import Standardize
            from botorch.optim import optimize_acqf_discrete
            from botorch.sampling import SobolQMCNormalSampler

            tx = torch.tensor(X / UBV, dtype=torch.double)
            ty = torch.tensor(Y, dtype=torch.double).unsqueeze(-1)
            if model_name == "saasbo":
                from botorch.fit import fit_fully_bayesian_model_nuts
                from botorch.models.fully_bayesian import SaasFullyBayesianSingleTaskGP

                gp = SaasFullyBayesianSingleTaskGP(tx, ty, outcome_transform=Standardize(m=1))
                fit_fully_bayesian_model_nuts(gp, warmup_steps=nuts[0], num_samples=nuts[1], thinning=nuts[2],
                                              disable_progbar=True)
            else:
                from botorch.fit import fit_gpytorch_mll
                from botorch.models import SingleTaskGP
                from gpytorch.mlls import ExactMarginalLogLikelihood

                gp = SingleTaskGP(tx, ty, outcome_transform=Standardize(m=1))
                try:
                    fit_gpytorch_mll(ExactMarginalLogLikelihood(gp.likelihood, gp))
                except Exception:  # noqa: BLE001
                    pass
            xp = torch.tensor(np.vstack(pending) / UBV, dtype=torch.double) if pending else None
            acq = qLogNoisyExpectedImprovement(gp, X_baseline=tx, X_pending=xp, prune_baseline=True,
                                               sampler=SobolQMCNormalSampler(torch.Size([64])))
            cand, _ = optimize_acqf_discrete(acq, q=q, choices=tpool[avail], max_batch_size=512, unique=True)
            # map the chosen rows back to pool indices
            d2 = torch.cdist(cand, tpool[avail])
            choice = avail[d2.argmin(1).numpy()]
        used[choice] = True
        Xn = pool[choice]
        new_el_runs += int(((Xn > 0) & ~seen_elements).any(1).sum())
        picks.append(Xn)
        pending.append(Xn)
        # observations arrive `delay` batches late
        while len(pending) > delay:
            Xo = pending.pop(0)
            X = np.vstack([X, Xo])
            Y = np.concatenate([Y, f(Xo) + noise_rng.normal(0, NOISE, len(Xo))])
    for Xo in pending:
        X = np.vstack([X, Xo])
        Y = np.concatenate([Y, f(Xo) + noise_rng.normal(0, NOISE, len(Xo))])
    design = X[1:]                                   # the 25 design runs
    parts = f(design, parts=True)
    truth = parts["y"]
    curve = np.maximum.accumulate(truth)
    f_pool = f(pool)
    best_six = float(f(six).max())
    bo_rows = design[n_seed:]
    bo_parts = f(bo_rows, parts=True)
    found_pair = False
    if pair is not None:
        found_pair = bool(((bo_rows[:, pair["a"]] > 0) & (bo_rows[:, pair["b"]] > 0)).any())
    return dict(
        rep=rep, strategy=strategy, model=model_name, delay=delay, synergy=pair is not None,
        best=float(curve[-1]), best_seed=float(truth[:n_seed].max()), best_six=best_six,
        pool_max=float(f_pool.max()), regret=float(f_pool.max() - curve[-1]),
        gain_over_six=float(curve[-1] - best_six), beat_six_by_20=bool(curve[-1] > best_six + 20.0),
        curve=[float(c) for c in curve], n_seed=n_seed, n_bo=int(len(bo_rows)),
        bo_new_element_runs=new_el_runs, bo_mean_p_crack=float(bo_parts["p_crack"].mean()),
        bo_frac_cracked=float((bo_parts["p_crack"] > 0.5).mean()),
        bo_mean_n_elements=float((bo_rows > 0).sum(1).mean()), found_pair=found_pair,
        bo_elements=[EL[i] for i in np.nonzero((bo_rows > 0).any(0))[0]],
        seconds=round(time.time() - t0, 1),
    )


# ---------------------------------------------------------------- driver
def summarize():
    import csv
    import statistics as st

    rows = [json.loads(line) for p in sorted(OUT.glob("runs_*.jsonl")) for line in open(p)]
    if not rows:
        print("no runs yet")
        return
    keys = sorted({(r["model"], r["strategy"], r["delay"]) for r in rows})
    # paired differences against six -> same model, same rep, same delay
    by = {(r["model"], r["strategy"], r["delay"], r["rep"]): r for r in rows}
    out = []
    for model, strat, delay in keys:
        rr = [r for r in rows if (r["model"], r["strategy"], r["delay"]) == (model, strat, delay)]
        n = len(rr)

        def m(key, sel=lambda r: True):
            vals = [r[key] for r in rr if sel(r)]
            return (st.mean(vals), st.stdev(vals) / len(vals) ** 0.5 if len(vals) > 1 else float("nan")) if vals else (float("nan"), float("nan"))

        diffs = [r["best"] - by[(model, "six", delay, r["rep"])]["best"] for r in rr if (model, "six", delay, r["rep"]) in by]
        dm = st.mean(diffs) if diffs else float("nan")
        dse = st.stdev(diffs) / len(diffs) ** 0.5 if len(diffs) > 1 else float("nan")
        out.append(dict(
            model=model, strategy=strat, delay=delay, n=n,
            best=round(m("best")[0], 1), best_se=round(m("best")[1], 1),
            best_no_synergy=round(m("best", lambda r: not r["synergy"])[0], 1),
            best_synergy=round(m("best", lambda r: r["synergy"])[0], 1),
            gain_over_six_seeds=round(m("gain_over_six")[0], 1),
            paired_diff_vs_six=round(dm, 1), paired_diff_se=round(dse, 1),
            p_beat_six_by_20=round(st.mean([r["beat_six_by_20"] for r in rr]), 2),
            regret=round(m("regret")[0], 1),
            bo_new_element_runs=round(m("bo_new_element_runs")[0], 2), n_bo=round(m("n_bo")[0], 1),
            bo_frac_cracked=round(m("bo_frac_cracked")[0], 2),
            found_hidden_pair=round(st.mean([r["found_pair"] for r in rr if r["synergy"]]) if any(r["synergy"] for r in rr) else float("nan"), 2),
            mean_seconds=round(m("seconds")[0], 1),
        ))
    with open(OUT / "summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for o in out:
        print(o)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reps", type=int, default=16)
    ap.add_argument("--rep-start", type=int, default=0)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--models", nargs="+", default=["saasbo"], choices=["saasbo", "gp", "random"])
    ap.add_argument("--strategies", nargs="+", default=STRATEGIES)
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--nuts", type=int, nargs=3, default=[96, 96, 12], help="warmup, samples, thinning")
    ap.add_argument("--summarize", action="store_true")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.summarize:
        summarize()
        return
    path = OUT / f"runs_{'-'.join(a.models)}_delay{a.delay}{a.tag}.jsonl"
    done = set()
    if path.exists():
        for line in open(path):
            r = json.loads(line)
            done.add((r["rep"], r["strategy"], r["model"]))
    jobs = []
    for rep in range(a.rep_start, a.rep_start + a.reps):       # rep-major order, so partial output stays paired
        for mdl in a.models:
            for s in (["random"] if mdl == "random" else a.strategies):
                key = (rep, "six" if mdl == "random" else s, mdl)
                if key in done:
                    continue
                jobs.append((rep, "six" if mdl == "random" else s, mdl, a.delay, tuple(a.nuts)))
    print(f"{len(jobs)} jobs -> {path}", flush=True)
    import multiprocessing as mp

    t0 = time.time()
    with mp.get_context("spawn").Pool(a.workers) as pool, open(path, "a") as fh:
        for i, r in enumerate(pool.imap_unordered(run_one, jobs), 1):
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            print(f"[{i}/{len(jobs)}] rep {r['rep']} {r['model']} {r['strategy']}: best {r['best']:.0f} "
                  f"(six {r['best_six']:.0f}, pool max {r['pool_max']:.0f}) new-el runs {r['bo_new_element_runs']} "
                  f"{r['seconds']}s  elapsed {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    main()
