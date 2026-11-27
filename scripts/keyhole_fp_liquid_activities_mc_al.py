"""Activities of Al, Mg and Si in the liquid alloys, from MatCalc mc_al with pycalphad (PR #249).

The first-principles keyhole model's wall temperature is where the alloy's total vapour pressure,
sum_i a_i p_i°(T), equals the keyhole pressure. The pure-element vapour pressures p_i° come from NIST-JANAF;
this script supplies the activity coefficients gamma_i = a_i / x_i of each element in the LIQUID phase,
relative to the pure liquid, at each alloy's bulk composition and in the dilute-Mg limit (for a wall depleted
of Mg). Above about 2000 K this is an extrapolation of the database's liquid description, which is fitted to
data near the liquidus; the README says so.

Usage (pycalphad 0.11.2; the database comes from a checkout of orchid-calphad/orchid-project.org):

    OPEN_TDB_ROOT=<checkout>/data/databases python scripts/keyhole_fp_liquid_activities_mc_al.py
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "arroyave-orchid-tools", "pycalphad-al-cu", "scripts"))
import pycalphad_al_cu_open_db as base  # noqa: E402

R = 8.314462618
ALLOYS = {
    "alsi10mg": {"SI": 10.0, "MG": 0.325},
    "blend": {"SI": 24.30, "MG": 0.14},
    "al5182": {"MG": 4.5},
    "al6061": {"SI": 0.6, "MG": 1.0},
}
OUT = os.path.join(REPO, "arroyave-orchid-tools", "keyhole-alternatives", "first-principles", "v2",
                   "mc_al-liquid-activity-coefficients.csv")


def main():
    from pycalphad import calculate, equilibrium, variables as v
    db = base.load_mc_al()
    T = np.arange(1000.0, 3600.0 + 1e-9, 100.0)
    rows = []
    g_pure = {}
    for el in ("AL", "MG", "SI"):
        res = calculate(db, [el, "VA"], "LIQUID", T=[float(t) for t in T], P=base.P0, N=1, output="GM")
        g_pure[el] = res.GM.values.reshape(len(T), -1)[:, 0]
    for key, wt in ALLOYS.items():
        for variant in ("bulk", "dilute_mg"):
            w = dict(wt)
            if variant == "dilute_mg":
                if "MG" not in w:
                    continue
                w["MG"] = 1e-4
            w = base.with_balance(w, "AL")
            x = base.wt_to_x(w)
            comps = sorted(w) + ["VA"]
            conds = {v.T: [float(t) for t in T], v.P: base.P0, v.N: 1.0}
            conds.update({v.X(e): x[e] for e in sorted(x) if e != "AL"})
            eq = equilibrium(db, comps, ["LIQUID"], conds, output="GM")
            mu = eq.MU.values.reshape(len(T), -1)
            els = list(eq.component.values)
            for i, t in enumerate(T):
                row = {"alloy": key, "variant": variant, "T_K": t}
                for el in ("AL", "MG", "SI"):
                    if el not in els:
                        continue
                    a = float(np.exp((mu[i, els.index(el)] - g_pure[el][i]) / (R * t)))
                    row[f"x_{el.lower()}"] = x[el]
                    row[f"a_{el.lower()}"] = a
                    row[f"gamma_{el.lower()}"] = a / x[el]
                rows.append(row)
            print(key, variant, {k: round(val, 4) for k, val in rows[-1].items() if k.startswith("gamma")}, flush=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False, float_format="%.6g")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
