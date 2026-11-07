"""Pt-W phase diagram, start vs tuned TDB (pycalphad BinaryStrategy), with the example's ZPF data points."""
import argparse
import glob
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import yaml  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from pycalphad import Database  # noqa: E402
from pycalphad import variables as v  # noqa: E402
from pycalphad.mapping import BinaryStrategy  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--start", required=True)
ap.add_argument("--tuned", required=True)
ap.add_argument("--zpf-dir", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

COL = {"FCC_A1": "#2a78d6", "BCC_A2": "#eb6834", "LIQUID": "#1baf7a"}  # validated categorical slots 1-3
INK, MUTED, GRID = "#1f1f1e", "#5f5e5a", "#e4e3df"

pts = []
for f in sorted(glob.glob(f"{args.zpf_dir}/zpf_*.yaml")):
    d = yaml.safe_load(open(f))
    for T, row in zip(d["conditions"]["T"], d["values"]):
        for ph, _, (x,) in row:
            if ph in COL and x is not None:
                pts.append((ph, x, T))

fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True, dpi=130)
for ax, (path, title) in zip(axes, [(args.start, "start: example/data/pt-w.tdb (MLIP-only)"),
                                    (args.tuned, "tuned: 16 CG evaluations, 583 s")]):
    st = BinaryStrategy(Database(path), ["PT", "W", "VA"], sorted(COL),
                        {v.X("W"): (0, 1, 0.02), v.T: (500, 3900, 20), v.P: 101325, v.N: 1})
    st.do_map()
    for region in st.get_tieline_data(x=v.X("W"), y=v.T):
        for d in region.data:
            ax.plot(d.x, d.y, color=COL[d.phase], lw=2, solid_capstyle="round")
    for inv in st.get_invariant_data(x=v.X("W"), y=v.T):
        xs = [float(x) for x in inv.x]
        T = float(inv.y[0])
        ax.plot([min(xs), max(xs)], [T, T], color=INK, lw=2)
        ax.annotate(f"invariant {T:.0f} K", (0.97, T), xytext=(0, -13), textcoords="offset points", color=INK,
                    fontsize=9, ha="right", bbox={"boxstyle": "square,pad=0.15", "fc": "white", "ec": "none"})
    for ph in COL:
        sel = [(x, T) for p, x, T in pts if p == ph]
        ax.scatter([s[0] for s in sel], [s[1] for s in sel], s=22, facecolors="none", edgecolors=COL[ph], linewidths=1.2,
                   zorder=3)
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    ax.set_xlim(0, 1)
    ax.set_ylim(500, 3900)
    ax.set_xlabel("x(W)", color=MUTED)
    ax.grid(color=GRID, lw=0.6)
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ax.spines.values():
        s.set_color(GRID)
axes[0].set_ylabel("T (K)", color=MUTED)
handles = [Line2D([], [], color=COL[p], lw=2, label=p) for p in COL]
handles += [Line2D([], [], color=INK, lw=2, label="three-phase invariant"),
            Line2D([], [], ls="", marker="o", mfc="none", mec=MUTED, label="ZPF data, example/data (ASM 2008)")]
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=9)
fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.savefig(args.out)
print("wrote", args.out, json.dumps({"n_data_points": len(pts)}))
