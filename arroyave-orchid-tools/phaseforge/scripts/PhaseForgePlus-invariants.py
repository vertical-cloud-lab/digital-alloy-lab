"""Binary invariant reactions (3-phase nodes) of one or more TDBs with pycalphad's BinaryStrategy mapper."""
import argparse
import json
import time

import numpy as np
from pycalphad import Database
from pycalphad import variables as v
from pycalphad.mapping import BinaryStrategy

ap = argparse.ArgumentParser()
ap.add_argument("--tdb", nargs="+", required=True)
ap.add_argument("--labels", nargs="+", required=True)
ap.add_argument("--comps", nargs="+", required=True, help="e.g. PT W VA")
ap.add_argument("--xel", required=True, help="element on the x axis")
ap.add_argument("--phases", nargs="*", default=None, help="default: all phases in the TDB")
ap.add_argument("--tmin", type=float, default=300)
ap.add_argument("--tmax", type=float, default=4000)
ap.add_argument("--tstep", type=float, default=20)
ap.add_argument("--xstep", type=float, default=0.02)
ap.add_argument("--out", required=True)
args = ap.parse_args()

result = {}
for path, label in zip(args.tdb, args.labels):
    t0 = time.time()
    dbf = Database(path)
    phases = args.phases or sorted(dbf.phases)
    conds = {v.X(args.xel): (0, 1, args.xstep), v.T: (args.tmin, args.tmax, args.tstep), v.P: 101325, v.N: 1}
    st = BinaryStrategy(dbf, args.comps, phases, conds)
    st.do_map()
    rows = []
    for d in st.get_invariant_data(x=v.X(args.xel), y=v.T):
        ts = [float(np.atleast_1d(y)[0]) for y in d.y]
        xs = [float(np.atleast_1d(x)[0]) for x in d.x]
        rows.append({"phases": list(d.phases), "T_K": round(float(np.mean(ts)), 2),
                     f"X({args.xel})": [round(x, 4) for x in xs]})
    rows.sort(key=lambda r: -r["T_K"])
    result[label] = {"tdb": path.split("/")[-1], "phases": phases, "invariants": rows,
                     "map_s": round(time.time() - t0, 1)}
    print(label, json.dumps(result[label]), flush=True)
with open(args.out, "w") as fh:
    json.dump(result, fh, indent=1)
