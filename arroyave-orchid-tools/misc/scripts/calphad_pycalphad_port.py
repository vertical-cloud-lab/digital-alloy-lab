"""Sketch of pointing ArroyaveLab/CALPHAD's TC_Equilibrium.py at pycalphad instead of TC-Python.

Keeps the repo's own orchestration (thermocalc_library: check_single_system, divide_up_cores,
create_parallelization_list, concatenate_divided_data; one worker per division) and swaps only
the body of Equilibrium(): a pycalphad equilibrium per composition and temperature. Liquidus /
solidus are found by a temperature scan, standing in for TC's "Liquidus and Solidus Temperature"
property model. Output columns use PhaseFrac_* (phase MOLE fraction, pycalphad NP) instead of
VolFra_*, because open TDBs usually carry no molar-volume parameters.

Usage: python -I calphad_pycalphad_port.py <dir with thermocalc_library.py> <TDB> <out_dir>
"""
import concurrent.futures
import functools
import json
import os
import sys
import time

import numpy as np
import pandas as pd

lib_dir, tdb_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, lib_dir)
from thermocalc_library import (check_single_system, concatenate_divided_data,  # noqa: E402
                                create_parallelization_list, divide_up_cores)


def Equilibrium(tdb, phases_wanted, temperatures_in_celsius, folder, elements, model_input):
    from pycalphad import Database, equilibrium, variables as v
    db = Database(tdb)
    comps = [e.upper() for e in elements] + ["VA"]
    phases = [p for p in db.phases if any(p.startswith(w) for w in phases_wanted)]
    t0 = time.monotonic()
    for i in model_input.index:
        x = {v.X(e.upper()): float(model_input.at[i, e]) for e in elements[:-1]}
        for temp in temperatures_in_celsius:
            eq = equilibrium(db, comps, phases, {v.T: temp + 273.15, v.P: 101325, v.N: 1, **x})
            names = eq.Phase.values.squeeze()
            fr = eq.NP.values.squeeze()
            for ph, f in zip(names, fr):
                if ph:
                    model_input.loc[i, f"PhaseFrac_{ph}_at_{temp}"] = float(f)
        # liquidus/solidus by a 1 K scan (stand-in for TC's property model)
        Ts = np.arange(700.0, 1300.0, 1.0)
        eq = equilibrium(db, comps, phases, {v.T: Ts, v.P: 101325, v.N: 1, **x})
        ph = eq.Phase.values.squeeze()  # (nT, vertex)
        npf = np.nan_to_num(eq.NP.values.squeeze())
        fl = np.array([npf[k][ph[k] == "LIQUID"].sum() for k in range(len(Ts))])
        liq = Ts[np.argmax(fl > 0.999)] if (fl > 0.999).any() else np.nan
        sol = Ts[np.argmax(fl > 1e-3)] - 1 if (fl > 1e-3).any() else np.nan
        model_input.loc[i, "Liquidus_temperature_(C)"] = liq - 273.15
        model_input.loc[i, "Solidus_temperature_(C)"] = sol - 273.15
        model_input.to_csv(f"{folder}/EQUIL_OUT_{model_input.index[0]}.csv", index=False)
    print(f"Completed: EQUIL_OUT_{model_input.index[0]}.csv in {time.monotonic() - t0:.1f} s", flush=True)


if __name__ == "__main__":
    os.makedirs(out, exist_ok=True)
    xsi = [0.02, 0.05, 0.096, 0.122, 0.20]  # 0.096 at.% ~ AlSi10Mg's Si; 0.122 ~ eutectic
    data_input = pd.DataFrame({"Material": range(1, len(xsi) + 1), "Si": xsi, "Al": [1 - s for s in xsi]})
    check_single_system(data_input)
    elements = [c for c in data_input.columns if len(c) <= 2 and data_input.iloc[0][c] > 0]
    rows, total = divide_up_cores(data_input, 2)
    chunks = create_parallelization_list(data_input, rows)
    t1 = time.monotonic()
    f = functools.partial(Equilibrium, tdb_path, ["LIQUID", "FCC_A1", "DIAMOND_A4"], [500, 600], out, elements)
    with concurrent.futures.ProcessPoolExecutor(2) as ex:
        list(ex.map(f, chunks))
    concatenate_divided_data(folder=out, file_start="EQUIL_OUT_")
    res = pd.read_csv(os.path.join(out, "All_data.csv")).sort_values("Material")
    pd.set_option("display.width", 250, "display.max_columns", 30)
    print(res.round(4).to_string(index=False))
    print(json.dumps({"wall_s": round(time.monotonic() - t1, 1), "rows": total}))
