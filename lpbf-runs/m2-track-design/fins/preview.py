"""End and side views of the generated STLs at true scale, drawn from the files' own triangles.

Top: one whole part (W011), seen from its y = 0 end and from its +x side. Bottom: the top 0.3 mm of
the narrowest, W011 and the widest file, seen from the end, so the line's width can be compared.

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
CX = -0.07  # mm, the flange's centre line (the template's)


def faces(path, axis, at=None):
    """Triangles whose normal points along +axis, projected onto the other two axes (in order).
    With ``at``, only those lying in the plane axis = at."""
    data = path.read_bytes()
    n = struct.unpack("<I", data[80:84])[0]
    keep = [k for k in range(3) if k != axis]
    out = []
    for i in range(n):
        v = struct.unpack("<12fH", data[84 + 50 * i: 84 + 50 * (i + 1)])
        if v[axis] < 0.99:
            continue
        pts = [v[3 + 3 * j: 6 + 3 * j] for j in range(3)]
        if at is not None and any(abs(p[axis] - at) > 1e-6 for p in pts):
            continue
        out.append([(p[keep[0]], p[keep[1]]) for p in pts])
    return out


def draw(ax, tris):
    """Fill each triangle: blue if it is part of the line (z >= 0), grey if part of the flange."""
    for tri in tris:
        c = FIN if min(p[1] for p in tri) >= -1e-6 else FLANGE
        ax.add_patch(Polygon(tri, closed=True, facecolor=c, edgecolor=c, linewidth=0.6))


def style(ax, xlabel, ylabel=None):
    ax.set_facecolor(SURFACE)
    ax.set_aspect("equal")
    ax.set_xlabel(xlabel, fontsize=9, color=INK2)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9, color=INK2)
    ax.tick_params(colors=INK2, labelsize=8, length=3)
    for s in ax.spines.values():
        s.set_color(GRID)


def main():
    rows = {r["set_name"]: r for r in csv.DictReader(open(HERE / "fins.csv", newline="", encoding="utf-8"))}
    w011 = rows["W011_348W_705_140um_h130"]
    by_width = sorted(rows.values(), key=lambda r: float(r["spot_um"]))
    picks = [by_width[0], w011, by_width[-1]]
    titles = ["narrowest", "W011", "widest"]

    # axes placed by hand, in inches, so that every view is at true scale with no wasted space
    W, H = 11.0, 5.2
    end_x, side_x, z1 = (-1.05, 0.80), (-13.2, 0.6), (-2.30, 0.25)  # mm
    zoom_x, z2 = (-0.78, 0.64), (-0.30, 0.20)
    left, gap1, right = 0.65, 0.55, 0.15
    s1 = (W - left - gap1 - right) / ((end_x[1] - end_x[0]) + (side_x[1] - side_x[0]))  # in per mm
    gap2 = 0.3
    s2 = (W - left - 2 * gap2 - right) / (3 * (zoom_x[1] - zoom_x[0]))
    h1, h2 = s1 * (z1[1] - z1[0]), s2 * (z2[1] - z2[0])
    y2 = 0.5                    # bottom row, from the bottom edge
    y1 = y2 + h2 + 1.2          # top row
    fig = plt.figure(figsize=(W, H), facecolor=SURFACE)

    def axes_at(x_in, y_in, w_in, h_in):
        return fig.add_axes([x_in / W, y_in / H, w_in / W, h_in / H])

    # whole part, end view and side view
    w_end = s1 * (end_x[1] - end_x[0])
    ax_end = axes_at(left, y1, w_end, h1)
    draw(ax_end, faces(HERE / w011["file"], axis=1, at=0.0))
    ax_end.set_xlim(*end_x)
    ax_end.set_ylim(*z1)
    ax_end.set_xticks([-0.5, 0.0, 0.5])
    style(ax_end, "x (mm)", "z (mm)")
    ax_end.set_title("End view", fontsize=9.5, color=INK, loc="left")
    ax_end.text(CX, -2.17, "1.25 mm", ha="center", va="center", fontsize=8.5, color=INK2)
    ax_end.text(-0.87, -1.0, "2.00 mm", ha="center", va="center", rotation=90, fontsize=8.5, color=INK2)

    ax_side = axes_at(left + w_end + gap1, y1, s1 * (side_x[1] - side_x[0]), h1)
    draw(ax_side, faces(HERE / w011["file"], axis=0))
    ax_side.set_xlim(*side_x)
    ax_side.set_ylim(*z1)
    style(ax_side, "y (mm)")
    ax_side.set_title("Side view: the line (blue, 0.05 mm tall) runs the flange's whole 12.6 mm",
                      fontsize=9.5, color=INK, loc="left")
    ax_side.annotate("", xy=(-12.6, -2.15), xytext=(0.0, -2.15),
                     arrowprops=dict(arrowstyle="<->", color=INK2, linewidth=0.8, shrinkA=0, shrinkB=0))
    ax_side.text(-6.3, -2.10, "12.6 mm", ha="center", va="bottom", fontsize=8.5, color=INK2,
                 bbox=dict(boxstyle="square,pad=0.15", facecolor=FLANGE, edgecolor="none"))
    fig.text(0.1 / W, (y1 + h1 + 0.42) / H,
             f"{w011['set_name']}, whole part at true scale: flange {w011['flange_mm']} mm (w × d × h), "
             f"{w011['overall_height_mm']} mm tall with the line", fontsize=10, color=INK, ha="left", va="bottom")

    # top 0.3 mm of three files, end view
    w_zoom = s2 * (zoom_x[1] - zoom_x[0])
    for k, (r, t) in enumerate(zip(picks, titles)):
        ax = axes_at(left + k * (w_zoom + gap2), y2, w_zoom, h2)
        draw(ax, faces(HERE / r["file"], axis=1, at=0.0))
        ax.axvline(CX, color=INK2, linewidth=0.8, linestyle=(0, (4, 3)))
        hi = float(r["rectangle_x_to_mm"])
        ax.annotate(f"{float(r['spot_um']):.0f} µm wide\n0.05 mm tall", xy=(hi, 0.035), xytext=(0.13, 0.05),
                    va="bottom", color=INK, fontsize=9,
                    arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.8))
        ax.set_xlim(*zoom_x)
        ax.set_ylim(*z2)
        style(ax, "x (mm)", "z (mm)" if k == 0 else None)
        if k:
            ax.tick_params(labelleft=False)
        ax.set_title(f"{r['set_name']} ({t})", fontsize=9.5, color=INK, loc="left")
        ax.text(-0.755, -0.27, "flange, 1.25 mm wide", fontsize=8.5, color=INK2)
    fig.text(0.1 / W, (y2 + h2 + 0.4) / H,
             "Top 0.3 mm, end view at true scale: the line is the set's spot size wide, centred (dashed line)",
             fontsize=10, color=INK, ha="left", va="bottom")
    fig.savefig(HERE / "fins-preview.png", dpi=170, facecolor=SURFACE, bbox_inches="tight", pad_inches=0.12)


if __name__ == "__main__":
    main()
