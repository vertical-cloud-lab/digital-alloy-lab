"""Cu-Ni checks for start/tuned TDBs: solidus/liquidus at x(Ni)=0.5, the FCC+L tie line at the ORCHID point
(1559.7 K, x(Ni)=0.4968; ORCHID tie line L 0.4274 / FCC 0.5456), and the FCC miscibility-gap top (no 3-phase
invariants exist in Cu-Ni with FCC + liquid only)."""
import argparse
import json

import numpy as np
from pycalphad import Database, equilibrium
from pycalphad import variables as v

ap = argparse.ArgumentParser()
ap.add_argument("--tdb", nargs="+", required=True)
ap.add_argument("--labels", nargs="+", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()
comps, phases = ["CU", "NI", "VA"], ["FCC_A1", "LIQUID"]
res = {}
for path, label in zip(args.tdb, args.labels):
    dbf = Database(path)
    r = {"tdb": path.split("/")[-1]}
    # solidus / liquidus at x(Ni) = 0.5
    T = np.arange(1400, 2000.01, 0.5)
    eq = equilibrium(dbf, comps, phases, {v.X("NI"): 0.5, v.T: T, v.P: 101325, v.N: 1})
    ph = eq.Phase.values.squeeze()
    npf = eq.NP.values.squeeze()
    liq = np.array([np.nansum(np.where(ph[i] == "LIQUID", npf[i], 0)) for i in range(len(T))])
    some, full = liq > 1e-6, liq > 1 - 1e-6  # None if not reached inside 1400-2000 K
    r["solidus_K_x0.5"] = float(T[np.argmax(some)]) if some.any() and not some[0] else None
    r["liquidus_K_x0.5"] = float(T[np.argmax(full)]) if full.any() and not full[0] else None
    # tie line at the ORCHID two-phase point
    eq = equilibrium(dbf, comps, phases, {v.X("NI"): 0.496770402, v.T: 1559.697474, v.P: 101325, v.N: 1})
    ph = eq.Phase.values.squeeze()
    xs = eq.X.sel(component="NI").values.squeeze()
    r["tie_1559.7K"] = {str(p): round(float(x), 4) for p, x in zip(ph, xs) if p != ""}
    # miscibility-gap top: highest T with two FCC composition sets on a grid
    T2 = np.arange(400, 900.01, 5)
    X2 = np.arange(0.30, 0.901, 0.05)
    eq = equilibrium(dbf, comps, ["FCC_A1"], {v.X("NI"): X2, v.T: T2, v.P: 101325, v.N: 1})
    ph = eq.Phase.values.squeeze()  # (T, X, vertex)
    two = (ph == "FCC_A1").sum(axis=-1) >= 2
    r["fcc_gap_top_K_grid5K"] = float(T2[np.where(two.any(axis=1))[0].max()]) if two.any() else None
    res[label] = r
    print(label, json.dumps(r), flush=True)
with open(args.out, "w") as fh:
    json.dump(res, fh, indent=1)
