"""pycalphad (MatCalc mc_ni v2.036, open) over the benchmark's composition box, for the physics-based truth.

    python physics/calphad_grid.py            # writes physics/calphad_grid.csv (resumable; about 25 min on 4 cores)

Reuses the database handling and the equilibrium/Scheil helpers of
near-term-submissions/onr-yip/pycalphad-cu/run_calphad.py (same database, sha256-checked).
Per composition (wt%, Cu balance): equilibrium liquidus and solidus, the first solid,
Scheil solidification (2 C steps), equilibrium phase fractions from 1,000 to 600 C, and the
composition of the copper-rich fcc (alpha) at 900 and 700 C.
"""

from __future__ import annotations

import csv
import itertools
import os
import sys
import time
import warnings
from multiprocessing import Pool
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")
HERE = Path(__file__).parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "near-term-submissions" / "onr-yip" / "pycalphad-cu"))
import run_calphad as rc  # noqa: E402

OUT = HERE / "calphad_grid.csv"
GRID = {"NI": [0, 2.5, 5, 7.5, 10, 15, 20, 25, 30], "AL": [0, 1.5, 3, 4.5, 6, 7, 8, 9.5], "FE": [0, 1.5, 3, 4.5], "MN": [0, 2, 4]}
T_SCAN = [1000, 950, 900, 850, 800, 750, 700, 600]
PH = ["liquid", "alpha", "fcc_feni", "beta", "kappa_fe", "kappa_nial", "gprime"]
LABEL = {"liquid": "liquid", "alpha (fcc)": "alpha", "fcc (Fe/Ni-rich)": "fcc_feni", "beta (Cu-rich bcc)": "beta", "kappa Fe-rich bcc": "kappa_fe",
         "kappa NiAl (B2)": "kappa_nial", "kappa NiAl-type bcc": "kappa_nial", "gamma' Ni3Al": "gprime"}
EL = ["NI", "AL", "FE", "MN"]
COLS = (["Ni", "Al", "Fe", "Mn", "Cu", "T_liq", "T_sol", "eq_range", "primary", "sch_first", "sch_T90", "sch_T99", "sch_end", "sch_range99", "sch_term", "kou", "sch_conv"]
        + [f"{p}_{t}" for t in T_SCAN for p in PH] + [f"a{t}_{e}" for t in (900, 700) for e in EL] + [f"sol1_{p}" for p in PH] + ["wall_s"])
_DB = None


def _init():
    global _DB
    _DB = rc.load_db("mc_ni")


def fractions(pt):
    d = {p: 0.0 for p in PH}
    alpha = None
    for p, a, xx in pt:
        k = LABEL.get(rc.label(p, xx))
        if k is None:
            continue
        d[k] += a
        if k == "alpha" and (alpha is None or a > alpha[0]):
            alpha = (a, xx)
    return d, alpha


def x_to_wt(xx):
    m = {e: xx.get(e, 0.0) * rc.MW[e] for e in rc.MW}
    s = sum(m.values())
    return {e: 100 * m[e] / s for e in m}


def one(c):
    ni, al, fe, mn = c
    t0 = time.time()
    wt = rc.wt_with_cu({k: v for k, v in zip(EL, c) if v > 0})
    comps, x, phases = rc.setup(_DB, "mc_ni", wt)
    row = dict(Ni=ni, Al=al, Fe=fe, Mn=mn, Cu=round(wt["CU"], 3))
    liq, sol, prim = rc.melting_range(_DB, comps, phases, x, tol=0.5)
    row.update(T_liq=round(liq, 1), T_sol=round(sol, 1), eq_range=round(liq - sol, 1), primary=prim)
    pts = rc.points(rc.equilibrium_at(_DB, comps, phases, x, np.array(T_SCAN, float) + 273.15))
    for t, pt in zip(T_SCAN, pts):
        d, alpha = fractions(pt)
        for p in PH:
            row[f"{p}_{t}"] = round(d[p], 5)
        if t in (900, 700):
            w = x_to_wt(alpha[1]) if alpha else {e: np.nan for e in rc.MW}
            for e in EL:
                row[f"a{t}_{e}"] = round(w[e], 4)
    d, _ = fractions(rc.points(rc.equilibrium_at(_DB, comps, phases, x, [sol + 273.15 + 1.0]))[0])
    for p in PH:
        row[f"sol1_{p}"] = round(d[p], 5)
    try:
        from pycalphad import variables as v
        from scheil import simulate_scheil_solidification

        res = simulate_scheil_solidification(_DB, comps, phases, {v.X(e): x[e] for e in x if e != "CU"}, liq + 273.15 + 10, step_temperature=2.0)
        T = np.array(res.temperatures) - 273.15
        fl = np.array(res.fraction_liquid)
        fs = 1 - fl
        first = T[np.argmax(fl < 0.9999)]
        t90 = T[np.argmax(fs >= 0.90)] if (fs >= 0.90).any() else np.nan
        t99 = T[np.argmax(fs >= 0.99)] if (fs >= 0.99).any() else np.nan
        # Kou's index: steepest |dT / d(fs^1/2)| for fs^1/2 in [0.87, 0.94] (K)
        r = np.sqrt(np.clip(fs, 0, 1))
        sel = (r >= 0.87) & (r <= 0.94)
        kou = np.nan
        if sel.sum() >= 2:
            dT = np.abs(np.diff(T[sel])) ; dr = np.diff(r[sel])
            ok = dr > 1e-6
            kou = float((dT[ok] / dr[ok]).max()) if ok.any() else np.nan
        row.update(sch_first=round(first, 1), sch_T90=round(t90, 1), sch_T99=round(t99, 1), sch_end=round(T[-1], 1), sch_range99=round(first - t99, 1),
                   sch_term=round(t90 - t99, 1), kou=round(kou, 1) if np.isfinite(kou) else np.nan, sch_conv=bool(res.converged))
    except Exception as e:  # recorded, not fatal
        row.update(sch_conv=f"error: {type(e).__name__}")
    row["wall_s"] = round(time.time() - t0, 1)
    return row


def main():
    done = set()
    if OUT.exists():
        with open(OUT) as f:
            for r in csv.DictReader(f):
                done.add(tuple(float(r[k]) for k in ("Ni", "Al", "Fe", "Mn")))
    todo = [c for c in itertools.product(*GRID.values()) if tuple(float(v) for v in c) not in done]
    # skip compositions outside the box's own physical limit (copper below 50 wt% cannot occur here; all kept)
    print(f"{len(done)} done, {len(todo)} to go", flush=True)
    new = not OUT.exists()
    with open(OUT, "a", newline="") as f, Pool(int(os.environ.get("NPROC", os.cpu_count())), initializer=_init) as pool:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        if new:
            w.writeheader()
        for i, row in enumerate(pool.imap_unordered(one, todo, chunksize=2)):
            w.writerow(row)
            f.flush()
            if i % 25 == 0:
                print(time.strftime("%H:%M:%S"), i, row["Ni"], row["Al"], row["Fe"], row["Mn"], row["T_liq"], row.get("sch_range99"), row["wall_s"], flush=True)


if __name__ == "__main__":
    main()
