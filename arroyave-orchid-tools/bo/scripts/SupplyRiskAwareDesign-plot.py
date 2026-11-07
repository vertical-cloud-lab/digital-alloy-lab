"""HV fraction and Pareto-set mean supply risk vs evaluations for the two SRAD scenarios (seed 0)."""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import vizstyle, matplotlib.pyplot as plt
vizstyle.apply()
D = Path("/tmp/arroyave/results/bo/data")
sc = [("with_SR", "objectives YS, Pugh, SR (with SR)"), ("without_SR", "objectives YS, Pugh (without SR)")]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 3.6))
for (s, lab), c in zip(sc, vizstyle.SERIES):
    h = pd.read_csv(D / f"SupplyRiskAwareDesign-s0-history_{s}.csv")
    a1.plot(h.n_eval, h.hv_frac, color=c, marker="o", label=lab)
    a1.text(h.n_eval.iloc[-1] + 0.5, h.hv_frac.iloc[-1], f"{h.hv_frac.iloc[-1]:.3f}", color=vizstyle.TEXT, va="center", fontsize=9)
    a2.plot(h.n_eval, h.pareto_mean_SR, color=c, marker="o", label=lab)
    a2.text(h.n_eval.iloc[-1] + 0.5, h.pareto_mean_SR.iloc[-1], f"{h.pareto_mean_SR.iloc[-1]:.1f}", color=vizstyle.TEXT, va="center", fontsize=9)
a1.set_xlabel("alloys evaluated (10 random + batches of 5)"); a1.set_ylabel("HV / HV of full-grid Pareto front")
a1.set_title("Batch EHVI convergence (own objective set)"); a1.set_xlim(8, 34)
a2.set_xlabel("alloys evaluated"); a2.set_ylabel("mean supply-risk index of Pareto set")
a2.set_title("Supply risk of the found Pareto set"); a2.set_xlim(8, 34)
fig.legend(*a1.get_legend_handles_labels(), loc="upper center", ncol=2, fontsize=9, bbox_to_anchor=(0.5, 1.0))
fig.suptitle("")
fig.tight_layout(rect=(0, 0, 1, 0.9)); fig.savefig("/tmp/arroyave/results/bo/figures/SupplyRiskAwareDesign-mobbo.png", dpi=130)
print("ok")
