"""Seeded (SEED=0) 5-iteration comparison of cGP / MTGP / DGP-iso from the DGP-BO repo.
Checks that the initial design is identical, then plots HV traces.
Usage: python -I DGP-BO-summarize-seeded.py <code_dir> <out_dir>"""
import json, pickle, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
code, out = sys.argv[1], sys.argv[2]
runs = {"cGP": "gp-tec-MO-11-seeded0", "MTGP": "mtgp-tec-MO-11-seeded0", "DGP-iso": "dgp-iso-tec-MO-11-seeded0"}
res, init = {}, {}
fig, ax = plt.subplots(figsize=(6, 4))
for (lab, stem), c in zip(runs.items(), ["#4C72B0", "#DD8452", "#55A868"]):
    hv = np.asarray(pickle.load(open(f"{code}/{stem}-hv.pl", "rb")), dtype=float).ravel()
    qx = np.asarray(pickle.load(open(f"{code}/{stem}-queryx1.pl", "rb")), dtype=float)
    init[lab] = np.round(qx[:2], 5).tolist()
    res[lab] = {"hv_trace": hv.round(3).tolist()}
    ax.plot(np.arange(hv.size), hv, "-o", ms=3, color=c, label=lab)
same = all(init[k] == init["cGP"] for k in init)
res["identical_initial_design"] = same
res["initial_design"] = init["cGP"]
ax.set_xlabel("BO iteration (0 = 2 initial alloys, SEED=0)")
ax.set_ylabel("hypervolume of observed Pareto front")
ax.set_title(f"DGP-BO repo, seeded comparison (identical start: {same})", fontsize=9)
ax.grid(alpha=0.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(f"{out}/figures/DGP-BO-hv-trace-seed0.png", dpi=110)
json.dump(res, open(f"{out}/data/DGP-BO-hv-traces-seed0.json", "w"), indent=1)
print(json.dumps(res))
