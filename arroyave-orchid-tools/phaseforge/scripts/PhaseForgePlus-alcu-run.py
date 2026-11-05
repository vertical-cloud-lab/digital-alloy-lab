"""Tiny PhaseForgePlus tune of Al-Cu (Al-rich side) against one ORCHID assessed ZPF dataset.

Start: SGTE AlCu-04Wit.tdb (Witusiewicz et al. 2004 via Hallstedt's SGTE binary collection, CC BY 4.0),
reduced to LIQUID, FCC_A1, BCC_A2, AL2CU_C16. Four coefficients are exposed as PhaseForge-style VV
symbols (constant in kJ, VV*1000, plus a T coefficient):
  L(LIQUID,AL,CU;0)  = VV0000*1000 + VV0001*T     (start -67.094 kJ, 8.555)
  G(AL2CU_C16,AL:CU) = 2*GHSERAL + GHSERCU + VV0002*1000 + VV0003*T   (start -47.406 kJ, 6.75)
Objective and optimizer are PhaseForgePlus's (objective_function + scipy CG), capped by a budget.
"""
import argparse
import json
import re
import shutil
import time
from pathlib import Path

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--sgte", required=True, help="AlCu-04Wit.tdb")
ap.add_argument("--zpf", nargs="+", required=True, help="ORCHID ESPEI ZPF json file(s)")
ap.add_argument("--workdir", required=True, help="scratch dir for the ZPF copies (.yaml)")
ap.add_argument("--out", required=True, help="results dir (data/ subdir is used)")
ap.add_argument("--maxiter", type=int, default=10)
ap.add_argument("--budget", type=float, default=300.0)
ap.add_argument("--prefix", default="PhaseForgePlus-AlCu")
ap.add_argument("--perturb", nargs="*", default=[], help="e.g. VV0002=+5 (added to the start value)")
args = ap.parse_args()

from espei.utils import database_symbols_to_fit  # noqa: E402
from pycalphad import Database  # noqa: E402
from scipy import optimize as scipy_optimize  # noqa: E402
from tinydb import where  # noqa: E402

from phaseforgeplus import PhaseForgePlus  # noqa: E402
from phaseforgeplus.utils.objective import objective_function  # noqa: E402

out = Path(args.out) / "data"
out.mkdir(parents=True, exist_ok=True)
work = Path(args.workdir)
zdir = work / "zpf"
if zdir.exists():
    shutil.rmtree(zdir)
zdir.mkdir(parents=True)
for z in args.zpf:  # PhaseForgePlus only globs *.yaml; JSON is valid YAML
    shutil.copy(z, zdir / (Path(z).stem + ".yaml"))

# 1) expose the coefficients as VV symbols (text edit of a scratch copy)
txt = Path(args.sgte).read_text()
txt, n1 = re.subn(r"(L\(LIQUID,AL,CU;0\),,\s*)-67094\+8\.555\*T;", r"\1VV0000*1000+VV0001*T;", txt)
txt, n2 = re.subn(r"(G\(AL2CU_C16,AL:CU\),,\s*\+2\*GHSERAL\+GHSERCU\s*)-47406\+6\.75\*T;",
                  r"\1+VV0002*1000+VV0003*T;", txt)
assert n1 == 1 and n2 == 1, (n1, n2)
vv = {"VV0000": -67.094, "VV0001": 8.555, "VV0002": -47.406, "VV0003": 6.75}
sgte_vv = dict(vv)
for item in args.perturb:  # optional recovery test: start away from the SGTE values
    k, d = item.split("=")
    vv[k] = round(vv[k] + float(d), 6)
txt += "\n" + "\n".join(f" FUNCTION {k} 298.15 {val}; 6000 N !" for k, val in vv.items()) + "\n"
full_vv = work / f"{args.prefix}-full-VV.tdb"
full_vv.write_text(txt)

# 2) reduce to the phases needed for the Al-rich side + the dataset's BCC points
keep = ["LIQUID", "FCC_A1", "BCC_A2", "AL2CU_C16"]
dbf = Database(str(full_vv))
for ph in list(dbf.phases):
    if ph not in keep:
        dbf.phases.pop(ph)
        dbf._parameters.remove(where("phase_name") == ph)
start_tdb = out / f"{args.prefix}-start.tdb"
dbf.to_file(str(start_tdb), if_exists="overwrite")

summary = {"phases": sorted(Database(str(start_tdb)).phases), "sgte_vv": sgte_vv, "start_vv": vv,
           "perturb": args.perturb}
t = time.time()
pfp = PhaseForgePlus(db=str(start_tdb), zpf_path=str(zdir), points=[], pressure=101325, temperature=298.15)
summary["constructor_s"] = round(time.time() - t, 2)
syms = database_symbols_to_fit(pfp.db)
x0 = np.asarray(pfp.get_initial_values(), dtype=float)
summary["symbols"] = list(syms)
summary["zpf_datasets"] = len(pfp.db_zpf)
print(json.dumps(summary), flush=True)

func = objective_function(pfp.db, pfp.db_zpf, pfp.db_neq)
trace, best = [], {"f": np.inf, "x": x0.copy()}


class BudgetExceeded(Exception):
    pass


t_opt0 = time.time()


def wrapped(x):
    t1 = time.time()
    f, g = func(x)
    rec = {"eval": len(trace), "f": float(f), "grad": [float(a) for a in g], "x": [float(a) for a in x],
           "eval_s": round(time.time() - t1, 2), "elapsed_s": round(time.time() - t_opt0, 1)}
    trace.append(rec)
    print(json.dumps(rec), flush=True)
    if np.isfinite(f) and f < best["f"]:
        best["f"], best["x"] = float(f), np.array(x, dtype=float)
    if time.time() - t_opt0 > args.budget:
        raise BudgetExceeded
    return f, g


status = "finished"
try:
    res = scipy_optimize.minimize(wrapped, x0, jac=True, method="CG", options={"disp": True, "maxiter": args.maxiter})
    summary.update(scipy_message=str(res.message), scipy_nit=int(res.nit), scipy_success=bool(res.success))
except BudgetExceeded:
    status = f"stopped by wall-clock budget ({args.budget:.0f} s)"
summary.update(optimizer_status=status, optimizer_s=round(time.time() - t_opt0, 1), n_evals=len(trace),
               objective_x0=trace[0]["f"] if trace else None, objective_best=best["f"],
               best_vv={s: float(b) for s, b in zip(syms, best["x"])})
db_tuned = Database(str(start_tdb))  # fresh load (pfp.db had its VV symbols popped by ESPEI)
for s, val in zip(syms, best["x"]):
    db_tuned.symbols[s] = float(val)
tuned_tdb = out / f"{args.prefix}-tuned.tdb"
db_tuned.to_file(str(tuned_tdb), if_exists="overwrite")
summary["start_tdb"], summary["tuned_tdb"] = start_tdb.name, tuned_tdb.name
(out / f"{args.prefix}-trace.json").write_text(json.dumps(trace, indent=1))
(out / f"{args.prefix}-summary.json").write_text(json.dumps(summary, indent=1))
print(json.dumps(summary, indent=1), flush=True)
