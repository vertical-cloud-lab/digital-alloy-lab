#!/usr/bin/env python3
"""CALPHAD screen for the first-six seed candidates (#275): liquidus, primary phase, Scheil path, cracking indices.

Database: the MatCalc open aluminium database mc_al_v2.032 (Povoden-Karadeniz, TU Wien; Open Database
License), in the pycalphad-adapted copy from the Materials Genome Foundation workshop material. It covers
Al, Cr, Cu, Fe, Mg, Mn, Ni, Sc, Si, Ti, Zn and Zr. Ce, Er, Li and Sn are not in it. The file is not copied
into this repo; `--tdb` points at a local copy:

    https://github.com/materialsgenomefoundation/2025-calphad-workshop/blob/main/pycalphad/databases/mc_al_v2.032.pycalphad.tdb

What is computed for each composition (wt% of the additions, Al balance):
- equilibrium liquidus (the first solid of any kind) and which phase it is. The atomizer melt has to sit
  above this, or Zr-, Ti-, Cr- or Mn-rich crystals form in the crucible;
- the Scheil-Gulliver path from an own step-by-step loop. A step whose equilibrium fails to converge is
  retried a little lower and never counted as the end of freezing, and a step that reports no liquid left is
  re-checked with a finer search before the path is allowed to end. (The `scheil` package ends the path when
  a step returns no liquid, which ended several Mg-rich paths 50-100 K too early here.);
- where alpha-Al starts and how much primary intermetallic has formed by then;
- the terminal freezing range (fraction solid 0.90 to 0.99), the Kou index max|dT/d(fs^0.5)| over
  fs 0.87-0.94 (Kou 2015, 10.1016/j.actamat.2015.01.034) and the Clyne-Davies CSC;
- equilibrium phase fractions at ageing temperatures.

Scheil assumes no diffusion in the solid and equilibrium at the interface. Laser melting is faster than
that: primary intermetallics are partly suppressed and solute is trapped, so read these as rankings.

    python calphad_screen.py lists/named.json results/calphad/named.jsonl --tdb /path/to/mc_al.tdb --workers 2
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")

MASS = {"AL": 26.9815, "CR": 51.9961, "CU": 63.546, "FE": 55.845, "MG": 24.305, "MN": 54.938,
        "NI": 58.6934, "SC": 44.9559, "SI": 28.0855, "TI": 47.867, "ZN": 65.38, "ZR": 91.224}

# Stable phases that can appear in Al-rich alloys of these 12 elements (metastable precipitate phases and
# phases of the solute-rich corners are left out; that also makes each equilibrium several times faster).
AL_RICH = {
    "LIQUID", "FCC_A1", "SI_DIAMOND_A4", "MG2SI_B", "BETA_AL3MG2", "E_AL30MG23", "G_AL12MG17",
    "AL13FE4", "AL6MN", "AL12MN", "AL4MN", "AL11MN4", "AL4CR", "AL13CR2", "AL11CR2", "AL18CR2MG3", "AL12MG2CR",
    "ALMGMN_T", "AL3ZR", "AL3M_D022", "AL3TI_L", "AL3TI_H", "AL3SC", "AL3NI", "AL3NI2", "THETA_AL2CU", "S_PHASE",
    "LC14_ZN2MG", "MGALCUZN_T", "MGALZN_PHI", "AL7CU2FE", "AL23CUFE4", "ALCUMN_T1", "AL8FEMNSI2", "ALFEMNSI_B",
    "ALCRFEMNSI_A", "AL13CR4SI4", "AL9CR3SI", "ALFESI_T5", "ALFESI_T6", "PI_ALFEMGSI", "Q_PHASE_H", "Q_PHASE_L",
    "ALFENI_T1", "ALSIZR_T1", "ALSIZR_T2", "AL4SI5ZR3",
}

DB = None
TDB = os.environ.get("MC_AL_TDB", "/tmp/tdb/mc_al_v2.032.pycalphad.tdb")


def wt_to_x(wt):
    w = {k.upper(): float(v) for k, v in wt.items() if float(v) > 0}
    w["AL"] = 100.0 - sum(w.values())
    n = {k: v / MASS[k] for k, v in w.items()}
    tot = sum(n.values())
    return {k: v / tot for k, v in n.items()}


def phase_list(db, comps):
    cset = set(comps)
    out = []
    for name in AL_RICH:
        ph = db.phases.get(name)
        if ph is None:
            continue
        if all(({sp.name for sp in sub} & cset) for sub in ph.constituents):
            out.append(name)
    return sorted(out)


def eq_point(db, x, T, phases=None, pdens=120, drop=2e-7):
    """One equilibrium. Returns (phase fractions, liquid composition or None). Empty dict = did not converge."""
    from pycalphad import equilibrium, variables as v

    x = {k: val for k, val in x.items() if k == "AL" or val > drop}      # drop vanishing components
    tot = sum(x.values())
    x = {k: val / tot for k, val in x.items()}
    comps = sorted(x) + ["VA"]
    phases = [p for p in (phases or phase_list(db, comps)) if p in phase_list(db, comps)]
    conds = {v.P: 101325, v.T: float(T), v.N: 1}
    for k, val in x.items():
        if k != "AL":
            conds[v.X(k)] = val
    try:
        eq = equilibrium(db, comps, phases, conds, calc_opts={"pdens": pdens})
    except Exception:  # noqa: BLE001
        return {}, None
    names = [str(n) for n in eq.Phase.values.ravel()]
    amts = eq.NP.values.ravel()
    frac, xl = {}, None
    X = eq.X.values.reshape(-1, len(eq.component))
    comp_names = [str(c) for c in eq.component.values]
    for i, (nme, a) in enumerate(zip(names, amts)):
        if nme and not np.isnan(a) and a > 1e-9:
            frac[nme] = frac.get(nme, 0.0) + float(a)
            if nme == "LIQUID":
                xl = {c: float(val) for c, val in zip(comp_names, X[i]) if not np.isnan(val)}
    if frac and abs(sum(frac.values()) - 1.0) > 0.02:
        return {}, None
    return frac, xl


def bisect_T(test, lo, hi, tol=1.0):
    """Highest T in [lo, hi] at which test(T) is True, assuming True below and False above."""
    if test(hi):
        return hi
    if not test(lo):
        return float("nan")
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if test(mid):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def liquidus(db, x, phases):
    last = {}

    def any_solid(T):
        f, _ = eq_point(db, x, T, phases)
        sol = {k: a for k, a in f.items() if k != "LIQUID"}
        if sol:
            last.clear()
            last.update(sol)
        return bool(sol)

    T = bisect_T(any_solid, 850.0, 1750.0)
    return T, (max(last, key=last.get) if last else None)


def solidus(db, x, phases):
    """Highest T at which no liquid is left in equilibrium."""
    def no_liquid(T):
        f, _ = eq_point(db, x, T, phases)
        return bool(f) and f.get("LIQUID", 0.0) < 1e-6

    return bisect_T(no_liquid, 650.0, 950.0)


def scheil(db, x0, t_start, phases, step=1.0, stop=2e-3, t_min=700.0):
    """Scheil-Gulliver: at each step the liquid alone is re-equilibrated and its solid is set aside.

    The step adapts so that each one freezes roughly 0.5-1.5 % of the alloy (0.5 K to 6 K; 8 K before
    alpha-Al appears), and the first appearance of alpha-Al is resolved to `step`. A step that fails to
    converge is retried a little lower and is never taken as the end of freezing. If the solver gives up
    with less than 8 % liquid left, the path is kept and flagged; the liquid left is then counted as
    freezing at the last temperature, which understates the terminal range.
    """
    x_liq, f_liq, T = dict(x0), 1.0, float(t_start)
    Ts, fss, cum, starts = [], [], {}, {}
    fails, status, dT = 0, "ok", 8.0
    prev, dropped, rechecked = None, 0.0, 0
    while f_liq > stop:
        if T < t_min:
            status = "stopped at the lower temperature limit"
            break
        frac, xl = eq_point(db, x_liq, T, phases)
        if not frac:
            # the solver often trips on a component that is nearly used up: drop traces and try again
            for thr in (3e-5, 3e-4, 1.5e-3):
                frac, xl = eq_point(db, x_liq, T, phases, drop=thr)
                if frac:
                    dropped = max(dropped, thr)
                    break
        if not frac:
            fails += 1
            if fails == 3:
                frac, xl = eq_point(db, x_liq, T, phases, pdens=800, drop=3e-4)
            if not frac:
                if fails > 5:
                    status = "equilibrium did not converge"
                    break
                T -= 0.37 * max(dT, 0.5)
                continue
        fails = 0
        if "FCC_A1" in frac and "FCC_A1" not in starts and dT > step * 1.01 and prev is not None:
            x_liq, f_liq, T = prev                      # back up and resolve the alpha-Al start finely
            dT = step
            T -= dT
            prev = None
            continue
        npl = frac.get("LIQUID", 0.0)
        if npl <= 1e-9 and f_liq > 0.005:
            # "no liquid left" is only believed after a finer search: the coarse one sometimes misses the liquid
            frac2, xl2 = eq_point(db, x_liq, T, phases, pdens=900)
            if frac2 and frac2.get("LIQUID", 0.0) > 1e-9:
                frac, xl, npl = frac2, xl2, frac2["LIQUID"]
                rechecked += 1
        prev = (dict(x_liq), f_liq, T)
        f_before = f_liq
        for k, amt in frac.items():
            if k == "LIQUID" or amt <= 0:
                continue
            if k not in starts:
                starts[k] = [T - 273.15, 1.0 - f_liq]
            cum[k] = cum.get(k, 0.0) + f_liq * amt
        f_liq *= npl
        Ts.append(T)
        fss.append(1.0 - f_liq)
        if npl <= 1e-9 or xl is None:
            break
        x_liq = xl
        dfs = f_before - f_liq
        if "FCC_A1" in starts:
            if dfs < 0.005:
                dT = min(dT * 1.6, 6.0)
            elif dfs > 0.015:
                dT = max(dT * 0.5, 0.5)
        T -= dT
    if status != "ok" and f_liq < 0.08:
        status = "ok, solver stopped with %.1f %% liquid left" % (100 * f_liq)
    if dropped:
        status += "; liquid components below %.0e mole fraction dropped at some steps" % dropped
    return dict(T=np.array(Ts), fs=np.array(fss), cum=cum, starts=starts, status=status, f_liq_left=f_liq)


def indices(path):
    T, fs = path["T"], path["fs"]
    keep = np.concatenate([[True], np.diff(fs) > 1e-10])
    fs_s, T_s = fs[keep], T[keep]
    fmax = float(fs_s.max())

    def T_at(f):
        return float(np.interp(f, fs_s, T_s))

    out = dict(T_end_C=float(T.min() - 273.15), fs_end=fmax)
    st = path["starts"]
    if "FCC_A1" in st:
        out["T_fcc_start_C"], out["fs_at_fcc_start"] = float(st["FCC_A1"][0]), float(st["FCC_A1"][1])
    else:
        out["T_fcc_start_C"], out["fs_at_fcc_start"] = float("nan"), float("nan")
    out["dT_fcc"] = out["T_fcc_start_C"] - out["T_end_C"]
    for a, b in ((0.80, 0.95), (0.90, 0.99), (0.95, 0.99)):
        out[f"dT_{int(a * 100)}_{int(b * 100)}"] = T_at(a) - T_at(min(b, fmax)) if fmax > a else 0.0
    if fmax > 0.875:
        grid = np.linspace(0.87, min(0.94, fmax), 15)
        out["kou_index"] = float(np.max(np.abs(np.gradient(np.interp(grid, fs_s, T_s), np.sqrt(grid)))))
    else:
        out["kou_index"] = 0.0
    if fmax > 0.905:
        tv, tr = T_at(0.90) - T_at(min(0.99, fmax)), T_at(0.40) - T_at(0.90)
        out["csc"] = float(tv / tr) if tr > 1e-6 else float("inf")
    else:
        out["csc"] = 0.0
    # liquid that freezes in the last 2 K: a large value means a eutectic-like finish
    out["f_last_2K"] = float(fmax - np.interp(T.min() + 2.0, T_s[::-1], fs_s[::-1]))
    out["phases"] = {k: float(v) for k, v in path["cum"].items()}
    out["phase_start"] = {k: [round(a, 1), round(b, 4)] for k, (a, b) in st.items()}
    return out


FS_GRID = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.93, 0.95, 0.97, 0.98, 0.99, 1.0]


def work(item):
    global DB
    from pycalphad import Database

    if DB is None:
        DB = Database(TDB)
    wt = {k.upper(): float(v) for k, v in item["wt"].items() if float(v) > 0}
    out = {"name": item["name"], "wt": wt, "tags": item.get("tags", {})}
    t0 = time.time()
    try:
        x = wt_to_x(wt)
        ph = phase_list(DB, sorted(x) + ["VA"])
        TL, prim = liquidus(DB, x, ph)
        out["liquidus_C"], out["primary_phase"] = round(TL - 273.15, 1), prim
        if not item.get("liquidus_only"):
            path = scheil(DB, x, TL + 2.0, ph, step=float(item.get("step", 1.0)))
            idx = indices(path)
            out.update({k: (round(v, 4) if isinstance(v, float) else v) for k, v in idx.items()})
            out["scheil_status"] = path["status"]
            out["scheil_ok"] = path["status"].startswith("ok")
            out["f_liq_left"] = round(float(path["f_liq_left"]), 4)
            order = np.argsort(path["fs"])
            out["scheil_T_at_fs"] = [round(float(np.interp(f, path["fs"][order], path["T"][order]) - 273.15), 1) for f in FS_GRID]
            out["fs_grid"] = FS_GRID
            eqs = {}
            for Tc in item.get("eq_T", [400.0]):
                f, _ = eq_point(DB, x, Tc + 273.15, ph)
                eqs[str(int(Tc))] = {k: round(v, 5) for k, v in f.items()}
            out["eq"] = eqs
        out["ok"] = True
    except Exception as e:  # noqa: BLE001
        out["ok"], out["error"] = False, f"{type(e).__name__}: {str(e)[:300]}"
    out["seconds"] = round(time.time() - t0, 1)
    return out


def main():
    global TDB
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inp")
    ap.add_argument("out")
    ap.add_argument("--tdb", default=TDB)
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    TDB = a.tdb
    os.environ["MC_AL_TDB"] = a.tdb
    items = json.load(open(a.inp))
    done = set()
    if os.path.exists(a.out):
        done = {json.loads(line)["name"] for line in open(a.out) if line.strip()}
    todo = [it for it in items if it["name"] not in done]
    print(f"{len(items)} items, {len(done)} done, {len(todo)} to run, {a.workers} workers", flush=True)
    import multiprocessing as mp

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    t0 = time.time()
    with mp.get_context("spawn").Pool(a.workers, maxtasksperchild=20) as pool, open(a.out, "a") as fh:
        for i, r in enumerate(pool.imap_unordered(work, todo), 1):
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            print(f"[{i}/{len(todo)}] {r['name']} liq {r.get('liquidus_C')} {r.get('primary_phase')} end {r.get('T_end_C')} "
                  f"{r.get('scheil_status')} kou {r.get('kou_index')} {r['seconds']}s "
                  f"elapsed {(time.time() - t0) / 60:.1f} min" + ("" if r["ok"] else " ERR " + r.get("error", "")), flush=True)


if __name__ == "__main__":
    sys.exit(main())
