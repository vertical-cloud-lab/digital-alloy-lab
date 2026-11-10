"""Collect the hypervolume traces (<script><index>-hv.pl pickles) written by the scaled-down
DGP-BO runs and plot them. Usage: python -I DGP-BO-summarize.py <code_dir> <out_dir>"""
import json, pickle, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
code, out = sys.argv[1], sys.argv[2]
runs = {"cGP-BO (gp-tec-MO-11)": "gp-tec-MO-11-cpusmall1", "MTGP-BO (mtgp-tec-MO-11)": "mtgp-tec-MO-11-cpusmall1",
        "DGP-BO (dgp-iso-tec-MO-11)": "dgp-iso-tec-MO-11-cpusmall1",
        "DGP-het (capsule entry, CPU)": "dgp-het-tec-MO-11-cpu1"}
res = {}
fig, ax = plt.subplots(figsize=(6, 4))
for (lab, stem), c in zip(runs.items(), ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]):
    hv = np.asarray(pickle.load(open(f"{code}/{stem}-hv.pl", "rb")), dtype=float).ravel()
    qy1 = np.asarray(pickle.load(open(f"{code}/{stem}-queryy1.pl", "rb")), dtype=float).ravel()
    res[lab] = {"hv_trace": hv.round(5).tolist(), "n_hv_points": int(hv.size), "n_queries_obj1": int(qy1.size)}
    ax.plot(np.arange(hv.size), hv, "-o", ms=3, color=c, label=lab)
ax.set_xlabel("BO iteration (0 = 2 random initial alloys)")
ax.set_ylabel("hypervolume of observed Pareto front")
ax.set_title("DGP-BO repo, FeCrNiCoCu 5-space, 1 unseeded run each", fontsize=9)
ax.grid(alpha=0.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(f"{out}/figures/DGP-BO-hv-trace.png", dpi=110)
json.dump(res, open(f"{out}/data/DGP-BO-hv-traces.json", "w"), indent=1)
print(json.dumps(res, indent=1))
