"""Yield strength vs elongation for LPBF AlSi10Mg and Scalmalloy, with the first-campaign gates.

Reads property-window.csv and writes property-window.png (1600 x 1000 px, white
background), both in this folder.

Each shaded rectangle is the bounding box of the datasheet points in one series; the
points themselves are drawn on top. Target rows are open-ended windows (YS >= y_min and
EL >= x_min), drawn as hatched regions out to the plot edge.

Run: python property-window.py
"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = Path(__file__).resolve().parent
CSV = HERE / "property-window.csv"
OUT = HERE / "property-window.png"

BLUE = "#257de0"  # AlSi10Mg (categorical slot 1)
ORANGE = "#f47230"  # Scalmalloy (categorical slot 2)
INK = "#191919"
INK2 = "#666666"
GATE = "#7a7a7a"

X_MAX, Y_MIN, Y_MAX = 26.0, 100.0, 560.0

# series -> (color, marker, fill alpha, direct label, label xy, label alignment)
STYLE = {
    "AlSi10Mg as-built": (BLUE, "o", 0.30, "AlSi10Mg\nas-built (machined)", (10.9, 318), "left"),
    "AlSi10Mg heat-treated": (BLUE, "s", 0.18, "AlSi10Mg heat-treated\n(T6 or stress relief)", (17.6, 150), "left"),
    "Scalmalloy as-built": (ORANGE, "o", 0.30, "Scalmalloy\nas-built", (21.0, 325), "left"),
    "Scalmalloy aged": (ORANGE, "s", 0.22, "Scalmalloy aged\n325 °C, 4 h", (16.6, 520), "left"),
}


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    rows = load(CSV)
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.edgecolor": INK2,
        "axes.labelcolor": INK,
        "xtick.color": INK2,
        "ytick.color": INK2,
    })
    fig, ax = plt.subplots(figsize=(8, 5), dpi=200, facecolor="white")
    ax.set_facecolor("white")

    # Target windows first (bottom layer): open-ended hatched regions.
    gates = [r for r in rows if r["series"] == "target"]
    hatches = ["///", "\\\\\\"]
    gate_handles = []
    for r, h in zip(gates, hatches):
        x0, y0 = float(r["elongation_pct"]), float(r["yield_MPa"])
        ax.add_patch(Rectangle((x0, y0), X_MAX - x0, Y_MAX - y0, facecolor="none",
                               edgecolor=GATE, hatch=h, linewidth=0, alpha=0.45, zorder=1))
        ax.plot([x0, x0, X_MAX], [Y_MAX, y0, y0], color=GATE, linestyle="--", linewidth=1.2, zorder=2)
        name = r["alloy"].replace(" family", "")
        gate_handles.append(Patch(facecolor="white", edgecolor=GATE, hatch=h,
                                  label=f"{name} gate"))
    # Corner labels for the two gates.
    ax.annotate("Al-Mn-Cr-Zr gate\nYS ≥ 250 MPa, EL ≥ 5%", xy=(5, 250), xytext=(0.6, 335),
                fontsize=9.5, color=INK, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=GATE, lw=0.9))
    ax.annotate("Al-Zr gate\nYS ≥ 200 MPa, EL ≥ 8%", xy=(8, 200), xytext=(0.6, 182),
                fontsize=9.5, color=INK, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=GATE, lw=0.9))

    # Alloy boxes and points.
    for series, (color, marker, alpha, label, (lx, ly), ha) in STYLE.items():
        pts = [r for r in rows if r["series"] == series]
        xs = [float(r["elongation_pct"]) for r in pts]
        ys = [float(r["yield_MPa"]) for r in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        pad_x, pad_y = 0.25, 4.0  # keep single-value spans visible
        ax.add_patch(Rectangle((x0 - pad_x, y0 - pad_y), (x1 - x0) + 2 * pad_x, (y1 - y0) + 2 * pad_y,
                               facecolor=color, alpha=alpha, edgecolor=color, linewidth=1.4, zorder=3))
        ax.scatter(xs, ys, s=34, marker=marker, color=color, edgecolor="white", linewidth=1.2, zorder=5)
        ax.text(lx, ly, label, fontsize=10, color=INK, ha=ha, va="center", zorder=6)

    # As-printed (unmachined) surface point: open marker plus a short note.
    for r in rows:
        if r["series"] == "AlSi10Mg as-built unmachined":
            x, y = float(r["elongation_pct"]), float(r["yield_MPa"])
            ax.scatter([x], [y], s=40, marker="o", facecolor="white", edgecolor=BLUE, linewidth=1.6, zorder=5)
            ax.annotate("as-printed surface,\nvertical (min. 1%)", xy=(x, y), xytext=(0.4, 226),
                        fontsize=9, color=INK2, ha="left", va="center",
                        arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))

    ax.set_xlim(0, X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_xlabel("Elongation at break (%)")
    ax.set_ylabel("Yield strength (MPa)")
    ax.grid(True, color="#e6e6e6", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_title("LPBF aluminum at room temperature: datasheet ranges vs first-campaign gates",
                 fontsize=12, color=INK, loc="left", pad=10)

    handles = [
        Line2D([], [], marker="o", color="none", markerfacecolor=BLUE, markeredgecolor="white",
               markersize=8, label="AlSi10Mg"),
        Line2D([], [], marker="o", color="none", markerfacecolor=ORANGE, markeredgecolor="white",
               markersize=8, label="Scalmalloy"),
        Line2D([], [], marker="o", color="none", markerfacecolor=INK2, markeredgecolor="white",
               markersize=7, label="as-built"),
        Line2D([], [], marker="s", color="none", markerfacecolor=INK2, markeredgecolor="white",
               markersize=7, label="heat-treated or aged"),
    ] + gate_handles
    ax.legend(handles=handles, loc="upper left", fontsize=8, frameon=True, framealpha=1.0,
              edgecolor="#d0d0d0", ncol=1, bbox_to_anchor=(0.0, 1.0))

    fig.text(0.01, 0.012,
             "Sources: vendor datasheets (EOS, Nikon SLM, Colibrium, 3D Systems); typical or mean values, "
             "machined unless noted. Gates: FLAIME proposal draft @0ddc928 L636.",
             fontsize=7, color=INK2, ha="left", va="bottom")
    fig.subplots_adjust(left=0.085, right=0.985, top=0.92, bottom=0.14)
    fig.savefig(OUT, dpi=200, facecolor="white")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
