"""The CALPHAD node of the physics-based truth: an 864-composition pycalphad grid (open MatCalc mc_ni).

    python phys/calphad_grid.py                    # about 25 min on 3 cores; writes phys/calphad_grid.csv
    python phys/calphad_grid.py --fractions-only   # redo only the phase fractions (minutes), keeping the melting ranges

Grid (wt%, Cu balance): Ni 0 to 30 in 8 levels, Al 0 to 9.5 in 6, Fe 0 to 4.5 in 6, Mn 0, 2, 4,
which is 8 x 6 x 6 x 3 = 864 compositions spanning the benchmark's box. Per composition:

- the equilibrium liquidus and solidus (10 C scan, then bisection to 0.5 C) and the primary phase;
- equilibrium phase fractions (mole) one degree above the solidus (solids formed in the melt: the
  Fe-rich primary kappa that nucleates alpha), at 900 C (beta that fast cooling can retain) and at
  600 C (the precipitates an aged or slowly cooled deposit can hold), named as in the NAB literature
  by `run_calphad.label`;
- the composition of alpha at 600 C (the solid solution behind solid-solution strengthening).

Database handling, phases and labels are reused from
`near-term-submissions/onr-yip/pycalphad-cu/run_calphad.py` (mc_ni v2.036, sha256-checked; see its
README for the caveats: no Cu-Al-Ni ternary, NAB liquidus about 50 C high).
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import time
import warnings
from multiprocessing import Pool
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")
HERE = Path(__file__).parent
REPO = HERE.parents[2]
RC_PATH = REPO / "near-term-submissions" / "onr-yip" / "pycalphad-cu" / "run_calphad.py"
OUT = HERE / "calphad_grid.csv"

NI = [30 * k / 7 for k in range(8)]
AL = [0.0, 1.9, 3.8, 5.7, 7.6, 9.5]
FE = [0.0, 0.9, 1.8, 2.7, 3.6, 4.5]
MN = [0.0, 2.0, 4.0]
LABELS = {"liquid": "liquid", "alpha (fcc)": "alpha", "beta (Cu-rich bcc)": "beta", "kappa Fe-rich bcc": "kappa_fe", "fcc (Fe/Ni-rich)": "fcc_feni",
          "kappa NiAl (B2)": "nial", "kappa NiAl-type bcc": "nial", "gamma' Ni3Al": "gprime"}
# kappa_fe is the Fe-rich bcc (kappa_I/II/IV-like); fcc_feni the Fe/Ni-rich fcc that Cu-Ni-Fe alloys
# without Al form instead (a miscibility gap, not a kappa phase)
PHASE_COLS = ["liquid", "alpha", "beta", "kappa_fe", "fcc_feni", "nial", "gprime", "other"]
TEMPS = {"sol": None, "900": 900.0, "600": 600.0}

_rc = _db = None


def _load_rc():
    spec = importlib.util.spec_from_file_location("run_calphad", RC_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _init():
    global _rc, _db
    _rc = _load_rc()
    _db = _rc.load_db("mc_ni")


def one(wt4, known=None):
    ni, al, fe, mn = wt4
    t0 = time.time()
    row = {"Ni_wt": round(ni, 4), "Al_wt": al, "Fe_wt": fe, "Mn_wt": mn}
    try:
        wt = _rc.wt_with_cu({"NI": ni, "AL": al, "FE": fe, "MN": mn})
        comps, x, phases = _rc.setup(_db, "mc_ni", wt)
        if known is None:
            liq, sol, primary = _rc.melting_range(_db, comps, phases, x, t_hi=1550.0, t_lo=850.0, step=10.0, tol=0.5)
        else:  # --fractions-only: the melting range from the stored grid
            liq, sol, primary = float(known["liquidus_C"] or "nan"), float(known["solidus_C"] or "nan"), known["primary"]
        row.update(liquidus_C=round(liq, 2), solidus_C=round(sol, 2), range_C=round(liq - sol, 2), primary=primary)
        temps = [sol + 1.0 if np.isfinite(sol) else np.nan, 900.0, 600.0]
        Tk = [t + 273.15 for t in temps if np.isfinite(t)]
        pts = _rc.points(_rc.equilibrium_at(_db, comps, phases, x, Tk))
        if not np.isfinite(temps[0]):
            pts = [[]] + pts
        for key, pt in zip(TEMPS, pts):
            fr = {c: 0.0 for c in PHASE_COLS}
            for p, amt, xx in pt:
                fr[LABELS.get(_rc.label(p, xx), "other")] += amt
            for c in PHASE_COLS:
                row[f"{c}_{key}"] = round(fr[c], 5)
            if key == "600":
                al_sets = [(amt, xx) for p, amt, xx in pt if _rc.label(p, xx) == "alpha (fcc)"]
                tot = sum(a for a, _ in al_sets)
                for e in ("NI", "AL", "FE", "MN"):
                    row[f"alpha600_x{e.lower()}"] = round(sum(a * xx.get(e, 0.0) for a, xx in al_sets) / tot, 5) if tot > 0 else np.nan
        row["ok"] = 1
    except Exception as e:  # keep the grid rectangular; the truth interpolates over failures from neighbors
        row.update(ok=0, error=str(e)[:120])
    row["wall_s"] = round(time.time() - t0, 2)
    return row


def _one_known(args):
    return one(*args)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--fractions-only", action="store_true", help="keep the stored melting ranges, recompute the phase fractions")
    a = ap.parse_args()
    grid = list(itertools.product(NI, AL, FE, MN))
    known = [None] * len(grid)
    if a.fractions_only:
        stored = list(csv.DictReader(open(OUT)))
        assert len(stored) == len(grid)
        known = [r if r.get("ok") == "1" else None for r in stored]
    t0 = time.time()
    rows = []
    with Pool(a.workers, initializer=_init) as pool:
        for i, r in enumerate(pool.imap(_one_known, zip(grid, known), chunksize=4)):
            rows.append(r)
            if (i + 1) % 48 == 0:
                print(f"{i + 1}/{len(grid)} {time.time() - t0:.0f}s", flush=True)
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} ({len(rows)} compositions, {sum(r.get('ok', 0) for r in rows)} ok) in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
