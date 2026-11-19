"""End views of three of the generated STLs, drawn from the files' own end-face triangles.

    pip install matplotlib
    python preview.py         # writes fins-preview.png
"""

import csv
import struct
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

HERE = Path(__file__).resolve().parent
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#d9d8d2"
FLANGE, FIN = "#c3c2b7", "#2a78d6"


def end_face(path):
    """Triangles of the y = 0 end face (normal +y): the part's cross-section, as stored."""
    data = path.read_bytes()
    n = struct.unpack("<I", data[80:84])[0]
    out = []
    for i in range(n):
        v = struct.unpack("<12fH", data[84 + 50 * i: 84 + 50 * (i + 1)])
        if v[1] > 0.99 and all(abs(v[k]) < 1e-6 for k in (4, 7, 10)):
            out.append([(v[3], v[5]), (v[6], v[8]), (v[9], v[11])])
    return out


def main():
    rows = {r["set_name"]: r for r in csv.DictReader(open(HERE / "fins.csv", newline="", encoding="utf-8"))}
    by_width = sorted(rows.values(), key=lambda r: float(r["spot_um"]))
    picks = [by_width[0], rows["W011_348W_705_140um_h130"], by_width[-1]]
    titles = ["narrowest", "W011, the template", "widest"]
    fig, axes = plt.subplots(1, 3, figsize=(11, 2.75), facecolor=SURFACE, sharey=True)
    for ax, r, t in zip(axes, picks, titles):
        ax.set_facecolor(SURFACE)
        for tri in end_face(HERE / r["file"]):
            fin = min(p[1] for p in tri) >= -1e-6
            ax.add_patch(Polygon(tri, closed=True, facecolor=FIN if fin else FLANGE,
                                 edgecolor=FIN if fin else FLANGE, linewidth=0.6))
        ax.axvline(-0.07, color=INK2, linewidth=0.8, linestyle=(0, (4, 3)))
        lo, hi = float(r["rectangle_x_from_mm"]), float(r["rectangle_x_to_mm"])
        ax.annotate(f"{float(r['spot_um']):.0f} µm wide\n0.05 mm tall", xy=(hi, 0.035), xytext=(0.12, 0.11),
                    color=INK, fontsize=9, arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.8))
        ax.set_xlim(-0.80, 0.66)
        ax.set_ylim(-0.30, 0.20)
        ax.set_aspect("equal")
        ax.set_title(f"{r['set_name']}\n({t})", fontsize=9.5, color=INK, loc="left")
        ax.set_xlabel("x (mm)", fontsize=9, color=INK2)
        ax.tick_params(colors=INK2, labelsize=8, length=3)
        for s in ax.spines.values():
            s.set_color(GRID)
        ax.text(-0.775, -0.27, "flange, 1.27 mm wide", fontsize=8.5, color=INK2)
    axes[0].set_ylabel("z (mm)", fontsize=9, color=INK2)
    fig.suptitle("End view at true scale (looking along the flange): the rectangle is the set's spot size wide, "
                 "centred (dashed line)", fontsize=10, color=INK, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(HERE / "fins-preview.png", dpi=170, facecolor=SURFACE, bbox_inches="tight", pad_inches=0.12)


if __name__ == "__main__":
    main()
