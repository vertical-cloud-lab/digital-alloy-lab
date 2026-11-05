"""Best-so-far and cumulative wall time per BO iteration for tamubo example logs (2D test function)."""
import json, sys, csv
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import vizstyle, matplotlib.pyplot as plt
vizstyle.apply()
W = Path("/tmp/arroyave/work/tamubo/examples")
runs = [("exactbo (numpy, 10 partitions)", W / "exactbo/logs/cpu_exactbo_it6_p10.json"),
        ("botorch_optimize_ei", W / "bo/logs/cpu_botorch_optimize_ei.json"),
        ("botorch_grid_ei (101x101)", W / "bo/logs/cpu_botorch_grid_ei.json"),
        ("sklearn_grid_ei (101x101)", W / "bo/logs/cpu_sklearn_grid_ei.json")]
colors = vizstyle.SERIES + ["#eda100"]
# dense-grid reference minimum of the example objective
g = np.linspace(0, 1, 2001); X, Y = np.meshgrid(g, g)
v = 0.1 * (X**2 + Y**2) + 2
for A, B, (cx, cy) in zip([4, 3, 2], [0.08, 0.05, 0.02], [(0.9, 0.3), (0.1, 0.8), (0.6, 0.7)]):
    v = v - A * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / B)
fmin = float(v.min())
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 3.6))
rows = []
for (lab, f), c in zip(runs, colors):
    d = json.load(open(f)); its = sorted(d, key=lambda k: int(k[1:]))
    best = [min(d["i0"]["y"])]; t = [0.0]
    for k in its:
        best.append(min(best[-1], d[k]["yn"][0])); t.append(t[-1] + d[k].get("time", float("nan")))
    n = list(range(len(best)))
    a1.plot(n, best, color=c, marker="o", label=lab)
    a2.plot(n[1:], t[1:], color=c, marker="o", label=lab)
    for i, (b, tt) in enumerate(zip(best, t)):
        rows.append({"framework": lab, "iteration": i, "best_y": b, "cum_time_s": tt})
a1.axhline(fmin, color=vizstyle.TEXT2, lw=1, ls="--"); a1.text(0.2, fmin + 0.05, f"grid minimum {fmin:.4f}", color=vizstyle.TEXT2, fontsize=8)
a1.set_xlabel("BO iteration (0 = 4-point initial design)"); a1.set_ylabel("best objective so far (minimize)")
a1.set_title("Convergence, 2D three-well test function")
a2.set_yscale("log"); a2.set_xlabel("BO iteration"); a2.set_ylabel("cumulative acquisition+fit time [s]")
a2.set_title("Cost per run on 1 CPU thread")
fig.legend(*a1.get_legend_handles_labels(), loc="upper center", ncol=4, fontsize=8, bbox_to_anchor=(0.5, 1.0))
fig.tight_layout(rect=(0, 0, 1, 0.9))
fig.savefig("/tmp/arroyave/results/bo/figures/tamubo-convergence.png", dpi=130)
with open("/tmp/arroyave/results/bo/data/tamubo-convergence.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("fmin", fmin)
for lab, _ in runs:
    r = [x for x in rows if x["framework"] == lab][-1]; print(lab, r)
