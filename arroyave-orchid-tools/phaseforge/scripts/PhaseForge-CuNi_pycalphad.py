"""Build a Cu-Ni TDB with the GRACE-2L-OMAT FCC_A1 mixing energy (PhaseForge lv=1 equivalent: L0 only)
on top of the open SGTE CuNi-07Tur file (unaries, magnetic terms, LIQUID kept), then compare with SGTE using pycalphad.
Usage: python PhaseForge-CuNi_pycalphad.py <sgte.tdb> <energies.json> <outdir>"""
import json, sys, re
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pycalphad import Database, equilibrium, variables as v

sgte, ejs, out = sys.argv[1:4]
e = json.load(open(ejs))
Ecu = e["sqs_lev=0_a_Cu=1"]["E_eV_per_atom"]; Eni = e["sqs_lev=0_a_Ni=1"]["E_eV_per_atom"]
Emix = e["sqs_lev=1_a_Cu=0.5,a_Ni=0.5"]["E_eV_per_atom"]
dH = (Emix - 0.5 * Ecu - 0.5 * Eni) * 96485.33          # J/mol-atom at x=0.5
L0 = 4 * dH
txt = open(sgte).read()
txt = re.sub(r"PAR  L\(FCC_A1,CU,NI:VA;0\),,\s+\+6877\.12\+4\.6\*T;", f"PAR  L(FCC_A1,CU,NI:VA;0),,  {L0:+.2f};", txt)
txt = re.sub(r"PAR  L\(FCC_A1,CU,NI:VA;1\),,\s+-2450\.1\+1\.87\*T;", "PAR  L(FCC_A1,CU,NI:VA;1),,  0;", txt)
assert f"{L0:+.2f}" in txt
open(f"{out}/PhaseForge-CuNi-GRACE-FCC-L0-on-SGTE07Tur.tdb", "w").write(
    "$ Generated in this test: FCC_A1 L0 from GRACE-2L-OMAT SQS energies (lv=1); everything else CuNi-07Tur (SGTE, Hallstedt 2025, CC BY 4.0)\n" + txt)
dbs = {"SGTE CuNi-07Tur": Database(sgte), "GRACE FCC L0 (PhaseForge lv1) + SGTE liquid": Database(f"{out}/PhaseForge-CuNi-GRACE-FCC-L0-on-SGTE07Tur.tdb")}
comps = ["CU", "NI", "VA"]
xs = np.round(np.arange(0.05, 0.951, 0.1), 3)
res = {"dHmix_x0.5_J_per_mol": dH, "L0_FCC_J_per_mol": L0, "rows": {}}
fig, ax = plt.subplots(figsize=(6.4, 4.8))
for (name, db), col in zip(dbs.items(), ["#1f5f99", "#c2571a"]):
    eq = equilibrium(db, comps, ["LIQUID", "FCC_A1"], {v.X("NI"): (0.05, 0.951, 0.1), v.T: (1300, 1900, 4), v.P: 101325, v.N: 1})
    T = eq.T.values; ph = eq.Phase.values[0, 0]; npf = eq.NP.values[0, 0]
    liq = np.nansum(np.where(ph == "LIQUID", npf, 0), axis=-1)   # (T, x)
    sol, liqd = [], []
    for j, x in enumerate(eq.X_NI.values):
        f = liq[:, j]; sol.append(float(T[np.argmax(f > 1e-6)])); liqd.append(float(T[np.argmax(f > 1 - 1e-6)]))
    eqm = equilibrium(db, comps, ["FCC_A1"], {v.X("NI"): (0.05, 0.951, 0.05), v.T: (300, 900, 10), v.P: 101325, v.N: 1})
    nfcc = (eqm.Phase.values[0, 0] == "FCC_A1").sum(axis=-1)       # (T, x)
    two = nfcc >= 2
    Tm = eqm.T.values; xm = eqm.X_NI.values
    mg_top = float(Tm[np.where(two.any(axis=1))[0].max()]) if two.any() else None
    mg_x = [float(Tm[np.where(two[:, j])[0].max()]) if two[:, j].any() else np.nan for j in range(len(xm))]
    res["rows"][name] = {"x_Ni": [float(x) for x in eq.X_NI.values], "solidus_K": sol, "liquidus_K": liqd, "fcc_gap_top_K": mg_top,
                         "fcc_gap_x": [float(x) for x in xm], "fcc_gap_Tmax_K": mg_x}
    ax.plot(eq.X_NI.values, liqd, "-", color=col, label=f"{name}: liquidus"); ax.plot(eq.X_NI.values, sol, "--", color=col, label="solidus")
    ax.plot(xm, mg_x, ":", color=col, marker=".", label="FCC miscibility gap (upper T)")
    print(name, "solidus", sol, "liquidus", liqd, "gap top", mg_top, flush=True)
ax.set_xlabel("x(Ni)"); ax.set_ylabel("T (K)"); ax.set_xlim(0, 1); ax.set_title("Cu-Ni: SGTE vs GRACE-2L-OMAT FCC mixing (L0 only)")
ax.legend(fontsize=7, loc="center right"); fig.tight_layout(); fig.savefig(f"{out}/../figures/PhaseForge-CuNi-SGTE-vs-GRACE.png", dpi=120)
json.dump(res, open(f"{out}/PhaseForge-CuNi-pycalphad-comparison.json", "w"), indent=1)
