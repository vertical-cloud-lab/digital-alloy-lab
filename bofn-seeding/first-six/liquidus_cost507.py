#!/usr/bin/env python3
"""Liquidus and primary phase from the COST 507 light-alloy database, as a second opinion (#275).

Why a second database: the MatCalc open Al database used for the Scheil paths (calphad_screen.py) is built
for precipitation in wrought alloys and has no Al3Zr liquidus. In it, Al-1 wt% Zr shows no solid down to
667 C, while the assessed Al-Zr diagram and COST 507 put the Al3Zr liquidus near 890-905 C. The melt
setpoint for a Zr-bearing charge has to come from a database that has this right.

COST 507 (Ansara, Dinsdale and Rand 1998) covers Al, B, C, Ce, Cr, Cu, Fe, Li, Mg, Mn, N, Nd, Ni, Si, Sn, Ti,
V, Y, Zn and Zr. It has no Sc and no Er, so those are left out of the composition here; the Al3Sc liquidus
comes from the MatCalc database. The copy used is the one distributed with OpenCalphad
(https://github.com/sundmanbo/opencalphad, examples/macros/cost507R.TDB); it is not copied into this repo.

    python liquidus_cost507.py lists/named.json results/calphad/liquidus_cost507.jsonl --tdb /path/to/cost507R.TDB
"""
from __future__ import annotations

import argparse
import json
import os
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")

MASS = {"AL": 26.9815, "CE": 140.116, "CR": 51.9961, "CU": 63.546, "FE": 55.845, "LI": 6.94, "MG": 24.305,
        "MN": 54.938, "NI": 58.6934, "SI": 28.0855, "SN": 118.71, "TI": 47.867, "ZN": 65.38, "ZR": 91.224}
DB = None
TDB = os.environ.get("COST507_TDB", "/tmp/tdb/cost507R.TDB")


def work(item):
    global DB
    from pycalphad import Database, equilibrium, variables as v

    if DB is None:
        DB = Database(TDB)
    wt_all = {k.upper(): float(val) for k, val in item["wt"].items() if float(val) > 0}
    left_out = sorted(k for k in wt_all if k not in MASS)
    wt = {k: val for k, val in wt_all.items() if k in MASS}
    out = {"name": item["name"], "wt": wt_all, "left_out": left_out, "tags": item.get("tags", {})}
    t0 = time.time()
    try:
        w = dict(wt)
        w["AL"] = 100.0 - sum(wt_all.values())
        n = {k: val / MASS[k] for k, val in w.items()}
        tot = sum(n.values())
        x = {k: val / tot for k, val in n.items()}
        comps = sorted(x) + ["VA"]
        cset = set(comps)
        phases = [name for name, ph in DB.phases.items()
                  if all(({sp.name for sp in sub} & cset) for sub in ph.constituents)]
        conds = {v.P: 101325, v.N: 1}
        for k, val in x.items():
            if k != "AL":
                conds[v.X(k)] = val

        def solids(T):
            eq = equilibrium(DB, comps, phases, {**conds, v.T: float(T)}, calc_opts={"pdens": 300})
            names = [str(nm) for nm in eq.Phase.values.ravel()]
            amts = eq.NP.values.ravel()
            return {nm: float(a) for nm, a in zip(names, amts) if nm and nm != "LIQUID" and not np.isnan(a) and a > 1e-9}

        lo, hi, last = 880.0, 1650.0, {}
        s_lo = solids(lo)
        if not s_lo:
            out.update(liquidus_C=None, primary_phase=None, note="no solid at 607 C")
        else:
            last = s_lo
            if solids(hi):
                out.update(liquidus_C=round(hi - 273.15, 1), primary_phase=max(last, key=last.get), note="above 1377 C")
            else:
                while hi - lo > 2.0:
                    mid = 0.5 * (lo + hi)
                    s = solids(mid)
                    if s:
                        lo, last = mid, s
                    else:
                        hi = mid
                out.update(liquidus_C=round(0.5 * (lo + hi) - 273.15, 1), primary_phase=max(last, key=last.get))
        out["ok"] = True
    except Exception as e:  # noqa: BLE001
        out["ok"], out["error"] = False, f"{type(e).__name__}: {str(e)[:200]}"
    out["seconds"] = round(time.time() - t0, 1)
    return out


def main():
    global TDB
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inp", nargs="+")
    ap.add_argument("out")
    ap.add_argument("--tdb", default=TDB)
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    TDB = a.tdb
    os.environ["COST507_TDB"] = a.tdb
    items = [it for p in a.inp for it in json.load(open(p))]
    done = set()
    if os.path.exists(a.out):
        done = {json.loads(line)["name"] for line in open(a.out) if line.strip()}
    todo = [it for it in items if it["name"] not in done]
    print(f"{len(items)} items, {len(todo)} to run", flush=True)
    import multiprocessing as mp

    with mp.get_context("spawn").Pool(a.workers, maxtasksperchild=40) as pool, open(a.out, "a") as fh:
        for i, r in enumerate(pool.imap_unordered(work, todo), 1):
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            print(f"[{i}/{len(todo)}] {r['name']} liquidus {r.get('liquidus_C')} {r.get('primary_phase')} {r['seconds']}s {r.get('error', '')}", flush=True)


if __name__ == "__main__":
    main()
