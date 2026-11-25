#!/usr/bin/env python3
"""Top view (x-y) of the coaxial branch as proposed in monitoring/optics.md §2, at the cube positions of cad/monitoring_spec.COAX,
with the free boxes monitoring_views.py found (analysis/out/monitoring/fits.json). A schematic for the CAD layout: lengths are
estimated from focal lengths and housing sizes, not drawn parts. Writes analysis/out/monitoring/optics/branch.png.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "cad"))
import monitoring_spec as MS  # noqa: E402

OUT = ROOT / "analysis" / "out" / "monitoring" / "optics"
C = MS.COAX
y0 = C["beam_y"]
x1, x2, x3 = C["cube1"]["x"], C["cube2"]["x"], C["cube3"]["x"]
CUBE = 41.9

fig, ax = plt.subplots(figsize=(11, 6.2))
fits = ROOT / "analysis" / "out" / "monitoring" / "fits.json"
if fits.exists():
    for b in json.loads(fits.read_text())["boxes"]:
        if b["hits"]:
            continue
        xa, xb, ya, yb = b["box"][:4]
        ax.add_patch(Rectangle((xa, ya), xb - xa, yb - ya, fill=False, ls="--", ec="0.6", lw=0.8))
        ax.text(xa + 2, yb - 6, "free: " + b["what"][:46], fontsize=6.5, color="0.45", va="top")


def cube(x, y, label, sub):
    ax.add_patch(Rectangle((x - CUBE / 2, y - CUBE / 2), CUBE, CUBE, fc="#e8eef7", ec="#3b5b92"))
    ax.plot([x - CUBE / 2 + 4, x + CUBE / 2 - 4], [y - CUBE / 2 + 4, y + CUBE / 2 - 4], color="#3b5b92", lw=2)
    ax.text(x, y + CUBE / 2 + 2, label, ha="center", va="bottom", fontsize=7.5, weight="bold")
    ax.text(x, y + CUBE / 2 + 15, sub, ha="center", va="bottom", fontsize=6.2, rotation=0, wrap=True)


def part(x, y, w, h, label, color="#f3e6c8"):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=color, ec="0.3", lw=0.8))
    ax.text(x, y, label, ha="center", va="center", fontsize=6.5)


def arrow(xa, ya, xb, yb, color, lw=1.6, text=None, tx=None, ty=None):
    ax.annotate("", xy=(xb, yb), xytext=(xa, ya), arrowprops=dict(arrowstyle="->", color=color, lw=lw))
    if text:
        ax.text(tx if tx is not None else (xa + xb) / 2, ty if ty is not None else (ya + yb) / 2, text, fontsize=6.8, color=color)


red, pink, nir, swir = "#c0392b", "#e67e22", "#8e44ad", "#16a085"
# laser: from the fold mirror and shutter (+y), reflected to the galvo (+x)
arrow(x1, y0 + 80, x1, y0 + 4, red, 2.2, "500 W, 1070 nm from the shutter", x1 + 4, y0 + 60)
arrow(x1 + 4, y0, x1 + 90, y0, red, 2.2, "to the galvo (+x)", x1 + 30, y0 + 5)
arrow(x1, y0 - 4, x1, y0 - 45, red, 1.0)
part(x1 + 2, y0 - 52, 34, 10, "beam trap\n(0.3-0.6 W)", "#f5c6c6")
cube(x1, y0, "cube1\nDMSP1000", "")
# return light along -x
arrow(x1 + 70, y0 - 8, x1 + 24, y0 - 8, "0.2", 1.0, "melt-pool light back from the galvo", x1 + 26, y0 - 18)
part((x1 + x2) / 2, y0, 8, 26, "FESH\n1000")
cube(x2, y0, "cube2\nDMSP950", "")
# camera arm along -y
cam = [(-48, "FESH1000"), (-62, "AC254-075-B\ntube lens"), (-138, "IMX296 mono\n7.4 um/px")]
for dy, lab in cam:
    part(x2, y0 + dy, 34 if "IMX" in lab else 26, 12 if "IMX" not in lab else 18, lab, "#d9f0d9" if "IMX" in lab else "#f3e6c8")
arrow(x2, y0 - 22, x2, y0 - 128, nir, 1.4, "955-990 nm", x2 + 15, y0 - 100)
cube(x3, y0, "cube3\nDMLP805", "")
arrow(x2 - 22, y0, x3 + 22, y0, pink, 1.4, "520-930 nm", (x2 + x3) / 2 - 12, y0 + 4)
# PD-B along -x
pdb = [(-34, "FBH\n900-40"), (-48, "AC254\n-050-B"), (-98, "P500K"), (-112, "PDA36A2\n(B)")]
for dx, lab in pdb:
    part(x3 + dx, y0, 10 if "P500" not in lab else 6, 26, lab, "#d9f0d9" if "PDA" in lab else "#f3e6c8")
arrow(x3 - 22, y0 - 12, x3 - 106, y0 - 12, nir, 1.2, "880-920 nm", x3 - 80, y0 - 22)
# PD-A side arm (shown folded along -y; it does not fit the free box's +/-35 mm unfolded)
pda = [(-34, "FBH700-40"), (-48, "AC254-050-B"), (-98, "P500K"), (-112, "PDA36A2 (A)")]
for dy, lab in pda:
    part(x3, y0 + dy, 30, 9 if "P500" not in lab else 5, lab, "#d9f0d9" if "PDA" in lab else "#f3e6c8")
arrow(x3 + 8, y0 - 22, x3 + 8, y0 - 106, red, 1.2, "680-720 nm", x3 + 12, y0 - 80)
ax.text(x3 - 140, y0 - 152, "PD-A's arm (~115 mm along -y) leaves the -x box and uses the box\nchecked for a folded Chronos arm; the strip y -60..-70 between them\nwas not checked", fontsize=6.8, color="#b03a2e")
ax.text(x2 - 70, y0 - 190, "InGaAs option: a 4th cube in the camera arm (~1180 nm dichroic),\n"
        "2 x FELH1250, AC254-100-C, P1000K, PDA20CS2 (needs a fold too)", fontsize=7, color=swir)
ax.set_aspect("equal")
ax.set_xlim(-430, -20)
ax.set_ylim(-230, 80)
ax.set_xlabel("x (mm, model frame)")
ax.set_ylabel("y (mm)")
ax.set_title("Coaxial branch, top view (schematic; cube positions from monitoring_spec.COAX, z 271.1)", fontsize=10)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "branch.png", dpi=140)
print("wrote", OUT / "branch.png")
