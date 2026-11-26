"""Equilibrium enthalpy H(T) of AlSi10Mg and the BYU blend from MatCalc mc_al with pycalphad (PR #249).

The first-principles keyhole model (scripts/keyhole_first_principles.py) needs each alloy's enthalpy from
the plate temperature to above the liquidus, with the latent heat spread over the freezing range as the
phase diagram spreads it. This computes the molar enthalpy HM at 1 atm and fixed composition, every 5 K
from 290 to 1400 K, with the same open database, phase set and helpers as
arroyave-orchid-tools/pycalphad-al-cu/scripts/pycalphad_al_cu_open_db.py, and converts it to J/kg.

Usage (pycalphad 0.11.2; the database comes from a checkout of orchid-calphad/orchid-project.org):

    OPEN_TDB_ROOT=<checkout>/data/databases python scripts/keyhole_fp_enthalpy_mc_al.py
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "arroyave-orchid-tools", "pycalphad-al-cu", "scripts"))
import pycalphad_al_cu_open_db as base  # noqa: E402

ALLOYS = {
    "alsi10mg": {"SI": 10.0, "MG": 0.325},   # as sent to Thermo-Calc
    "blend": {"SI": 24.30, "MG": 0.14},      # BYU AA1100 + Si + AlSi10Mg blend
}
OUT = os.path.join(REPO, "arroyave-orchid-tools", "keyhole-alternatives", "first-principles",
                   "mc_al-enthalpy-vs-T.csv")


def main():
    db = base.load_mc_al()
    T = np.arange(290.0, 1400.0 + 1e-9, 5.0)
    rows = []
    for key, wt in ALLOYS.items():
        wt = base.with_balance(wt, "AL")
        x = base.wt_to_x(wt)
        comps = sorted(wt) + ["VA"]
        phases = base.phases_for(db, comps, base.METASTABLE_MC_AL)
        calc = base.EqCalc(db, comps, phases, "AL")
        molar_mass = sum(x[e] * base.MW[e] for e in x) / 1000.0  # kg/mol
        from pycalphad import equilibrium, variables as v
        conds = {v.T: [float(t) for t in T], v.P: base.P0, v.N: 1.0}
        conds.update({v.X(e): x[e] for e in sorted(x) if e != "AL"})
        eq = equilibrium(db, comps, phases, conds, model=calc.models, phase_records=calc.prf, output="HM")
        hm = eq.HM.values.reshape(-1)
        ph = eq.Phase.values.reshape(-1, eq.Phase.shape[-1])
        npv = eq.NP.values.reshape(-1, eq.NP.shape[-1])
        for i, t in enumerate(T):
            f_liq = float(sum(npv[i][j] for j, p in enumerate(ph[i]) if p == "LIQUID" and np.isfinite(npv[i][j])))
            rows.append({"alloy": key, "T_K": t, "H_J_per_kg": hm[i] / molar_mass, "liquid_mole_fraction": f_liq,
                         "molar_mass_kg_mol": molar_mass})
        print(key, "molar mass", round(molar_mass, 6), flush=True)
    d = pd.DataFrame(rows)
    d.to_csv(OUT, index=False, float_format="%.6g")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
