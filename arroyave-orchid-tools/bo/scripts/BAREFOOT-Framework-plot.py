"""Best truth value found vs truth-model evaluations: BAREFOOT batch-only vs reification+batch (single node, 1 seed)."""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import vizstyle, matplotlib.pyplot as plt
vizstyle.apply()
D = Path("/tmp/arroyave/results/bo/data")
runs = [("BAREFOOT-Framework-batch-it4-hp100-iterationData.csv", "batch only (truth batch 10 / iter)"),
        ("BAREFOOT-Framework-full-med-iterationData.csv", "reification + batch (3 cheap models, truth batch 5)")]
fig, ax = plt.subplots(figsize=(6.6, 3.8))
for (f, lab), c in zip(runs, vizstyle.SERIES):
    d = pd.read_csv(D / f)
    ax.step(d["Truth Model"], d["Max Found"], where="post", color=c, label=lab)
    ax.plot(d["Truth Model"], d["Max Found"], "o", color=c)
    ax.text(d["Truth Model"].iloc[-1] + 0.8, d["Max Found"].iloc[-1], f"{d['Max Found'].iloc[-1]:.2f}", color=vizstyle.TEXT, va="center", fontsize=9)
ax.axhline(5.719, color=vizstyle.TEXT2, lw=1, ls="--"); ax.text(1, 5.6, "grid maximum 5.72", color=vizstyle.TEXT2, fontsize=8, va="top")
ax.set_xlabel("truth-model evaluations"); ax.set_ylabel("best truth value found (maximize)")
ax.set_title("BAREFOOT 2D demo function, single node, seed 0"); ax.set_xlim(0, 60)
ax.legend(loc="lower right", fontsize=8)
fig.tight_layout(); fig.savefig("/tmp/arroyave/results/bo/figures/BAREFOOT-Framework-batch-vs-fusion.png", dpi=130)
print("ok")
