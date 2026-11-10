"""Liquidus and solidus of the two alloys in our in-house Thermo-Calc AM-module runs, from MatCalc mc_al (#235).

The AM-module printability maps (consolidation-2 branch, figures/thermo-calc-am-module-prelim-results/)
were run for stock AlSi10Mg (Al 89.675, Si 10.0, Mg 0.325 wt%) and the BYU AA1100 + Si + AlSi10Mg
blend (Al 75.56, Si 24.30, Mg 0.14 wt%). eagar-tsai needs one isotherm for the melt-pool edge, and
for the hypereutectic blend the liquidus and the eutectic are far apart. This computes both with
the same open database and helpers as pycalphad_al_cu_open_db.py (equilibrium, coarse scan then
bisection to 0.1 K).

Usage:  OPEN_TDB_ROOT=<dir holding binder/mc_al_v2.032.pycalphad.tdb> python am_module_alloys_mc_al.py
"""
import os
import sys
import time

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pycalphad_al_cu_open_db as base  # noqa: E402

ALLOYS = [
    ("AlSi10Mg, as sent to Thermo-Calc", {"SI": 10.0, "MG": 0.325}),
    ("BYU AA1100+Si+AlSi10Mg blend", {"SI": 24.30, "MG": 0.14}),
]


def main():
    db = base.load_mc_al()
    rows = []
    for name, wt in ALLOYS:
        t0 = time.time()
        wt = base.with_balance(wt, "AL")
        x = base.wt_to_x(wt)
        comps = sorted(wt) + ["VA"]
        phases = base.phases_for(db, comps, base.METASTABLE_MC_AL)
        calc = base.EqCalc(db, comps, phases, "AL")
        ev = base.find_events(calc, x, 1250.0, 780.0, 4.0, track=["FCC_A1", "SI_DIAMOND_A4", "MG2SI_B"])
        primary = [p for p in ("FCC_A1", "SI_DIAMOND_A4") if abs(ev.get(p, float("nan")) - ev["liquidus"]) < 0.3]
        row = dict(alloy=name, composition_wt=" ".join(f"{k}{wt[k]:.3f}" for k in sorted(wt)),
                   database="mc_al v2.032", liquidus_K=round(ev["liquidus"], 1), solidus_K=round(ev["solidus"], 1),
                   liquidus_C=round(base.T_C(ev["liquidus"]), 1), solidus_C=round(base.T_C(ev["solidus"]), 1),
                   primary_phase="+".join(primary),
                   FCC_A1_start_K=round(ev.get("FCC_A1", float("nan")), 1),
                   SI_DIAMOND_A4_start_K=round(ev.get("SI_DIAMOND_A4", float("nan")), 1),
                   MG2SI_B_start_K=round(ev.get("MG2SI_B", float("nan")), 1),
                   wall_s=round(time.time() - t0, 1))
        print(row, flush=True)
        rows.append(row)
    out = os.path.join(base.DATA, "am_module_alloys_mc_al.csv")
    pd.DataFrame(rows).to_csv(out, index=False)
    print("wrote", out)


if __name__ == "__main__":
    main()
