"""Plot BO vs paired random baseline (fraction of oracle hypervolume) from rhea_mobo.toy runs."""
import sys, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import vizstyle, matplotlib.pyplot as plt
vizstyle.apply()
runs = [(Path(p), lab) for p, lab in zip(sys.argv[1:-1:2], sys.argv[2:-1:2])]
out = Path(sys.argv[-1])
fig, axes = plt.subplots(1, len(runs), figsize=(4.2 * len(runs), 3.4), sharey=True)
rows_all = []
for ax, (d, lab) in zip(axes, runs):
    rows = list(csv.DictReader(open(d / "comparison.csv")))
    n = [int(r["total_evaluations"]) for r in rows]
    bo = [float(r["bo_oracle_fraction"]) for r in rows]
    rnd = [float(r["random_oracle_fraction"]) for r in rows]
    ax.plot(n, bo, color=vizstyle.SERIES[0], marker="o", label="BO (EHVI / supply risk)")
    ax.plot(n, rnd, color=vizstyle.SERIES[1], marker="s", label="Random (paired)")
    hi, lo = (0.012, -0.012) if bo[-1] >= rnd[-1] else (-0.012, 0.012)
    ax.text(n[-1] + 0.4, bo[-1] + hi, f"BO {bo[-1]:.3f}", color=vizstyle.TEXT, ha="left", va="center", fontsize=9)
    ax.text(n[-1] + 0.4, rnd[-1] + lo, f"rand {rnd[-1]:.3f}", color=vizstyle.TEXT2, ha="left", va="center", fontsize=9)
    ax.set_xlim(n[0] - 0.5, n[-1] + 4.5)
    ax.set_title(lab); ax.set_xlabel("objective evaluations (8 initial + accepted)")
    for r in rows:
        rows_all.append({"run": lab, **r})
axes[0].set_ylabel("hypervolume / oracle hypervolume")
fig.legend(*axes[0].get_legend_handles_labels(), loc="upper center", ncol=2, bbox_to_anchor=(0.5, 0.93))
fig.suptitle("rhea-mobo synthetic toy: 5-objective EHVI on 1,716-point Mo-Nb-Ta-W-Co-Hf grid", fontsize=10, color=vizstyle.TEXT2)
fig.tight_layout(rect=(0, 0, 1, 0.86)); fig.savefig(out, dpi=130)
print("wrote", out)
