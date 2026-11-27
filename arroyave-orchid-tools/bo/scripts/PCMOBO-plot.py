"""Cumulative feasible discoveries per iteration for PCMOBO HEA campaigns (one seed each)."""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import vizstyle, matplotlib.pyplot as plt
vizstyle.apply()
R = Path("/tmp/arroyave/work/pcmobo/runs/hea_design")
pols = [("pof", "PoF (fixed)"), ("pehvi", "pEHVI (fixed)"), ("bandit_ucb_switch", "bandit-UCB switch (adaptive)")]
fig, ax = plt.subplots(figsize=(6.4, 3.8))
rows = []
for (p, lab), c in zip(pols, vizstyle.SERIES):
  for seed, ls, mk in [(1, "-", "o"), (2, "--", "s")]:
    d = pd.read_csv(R / f"cmp_{p}/campaign_{seed}.csv")
    x = [0] + d["Iteration"].tolist(); y = [0] + d["CumulativeFeasibleCount"].tolist()
    ax.plot(x, y, color=c, marker=mk, ls=ls, markersize=4, label=f"{lab}, seed {seed}")
    ax.text(x[-1] + 0.3, y[-1] + (0.35 if seed == 2 else -0.35) * (y[-1] > 0), f"{y[-1]}", color=vizstyle.TEXT, va="center", fontsize=9)
    for _, r in d.iterrows():
        rows.append({"policy": p, "seed": seed, "iteration": r["Iteration"], "selected_acq": r["SelectedAcq"],
                     "cum_feasible": r["CumulativeFeasibleCount"], "hv_scaled": r["HypervolumeScaledFixedRange"]})
ax.set_xlabel("BO iteration (after 10 random initial alloys, q = 1)")
ax.set_ylabel("cumulative feasible alloys found")
ax.set_title("PCMOBO HEA pool (40,553 Nb-Mo-Ta-V-W-Cr alloys), 2 seeds")
ax.legend(loc="upper left", fontsize=8)
fig.tight_layout(); fig.savefig("/tmp/arroyave/results/bo/figures/PCMOBO-hea-feasible.png", dpi=130)
pd.DataFrame(rows).to_csv("/tmp/arroyave/results/bo/data/PCMOBO-hea-campaigns.csv", index=False)
print("ok")
