"""Draw where the deck keys go: the PandaDeck's slot grid in Ben's CubOS frame, each keyed part's footprint
(projected from its STL, in the deck frame it is drawn in), the slots its keys drop into, and a to-scale
section through one key. Writes deck-keys.png. Reads deck_keys.json, so run deck_keys.py first.

    python plot_deck_keys.py

Needs trimesh, shapely, matplotlib and numpy.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import trimesh  # noqa: E402
from matplotlib.patches import Polygon as MplPolygon, Rectangle  # noqa: E402
from shapely.geometry import LineString  # noqa: E402
from trimesh.path.polygons import projected  # noqa: E402

HERE = Path(__file__).resolve().parent
AC = HERE.parents[1]

SURF, INK, INK2, MUTED, SLOT, PART = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#d8d6cf", "#e9e7e1"
KEY, BEN = "#eb6834", "#2a78d6"   # categorical slots 2 and 1 of the dataviz default palette

LABELS = {"coupon_tray": "coupon tray (P06)", "cup_block_3": "cup block (P08)", "tube_rack_2x8": "tube rack (P10)",
          "tip_waste_cup": "tip waste (P09)", "tip_rack_2x15": "tip rack 2 (P11)\nnot on the H2D plate"}

# Ben's own keyed items, for context only (positions from ../../stirrers/deck_stir.py and Ben's deck files)
STIRRERS = [(76.0, y) for y in (45.0, 90.0, 135.0, 180.0)]
RACK1 = (277.1, 85.0, 297.1, 212.0)
HOLDER = (301.3, 18.3, 334.7, 315.7)  # the plan's x 318


def pill(cx, cy, w, l):
    return LineString([(cx, cy - (l - w) / 2), (cx, cy + (l - w) / 2)]).buffer(w / 2, resolution=24)


def add_poly(ax, geom, **kw):
    for g in getattr(geom, "geoms", [geom]):
        ax.add_patch(MplPolygon(np.asarray(g.exterior.coords), closed=True, **kw))


def tri(cx, cy, r_sharp, r_round, corner_deg):
    pts = [(cx + r_sharp * math.cos(math.radians(corner_deg + 120 * k)), cy + r_sharp * math.sin(math.radians(corner_deg + 120 * k)))
           for k in range(3)]
    from shapely.geometry import Polygon
    return Polygon(pts).buffer(r_round, resolution=16)


def plan(ax, d):
    deck = d["deck"]
    px, py = deck["slot_pitch_x"], deck["slot_pitch_y"]
    x0 = 12.5
    ax.set_facecolor(SURF)
    for i in range(-1, 18):
        for j in range(0, 7):
            add_poly(ax, pill(x0 + i * px, j * py, deck["slot_w"], deck["slot_l"]), fc="none", ec=SLOT, lw=0.7, zorder=1)
    ax.add_patch(Rectangle((0, 0), 361, 278, fill=False, ec=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1))
    # Ben's items, outlines only
    for sx, sy in STIRRERS:
        ax.add_patch(Rectangle((sx - 24.5, sy - 22), 49, 44, fill=False, ec=BEN, lw=1.0, zorder=2))
    ax.text(76, 205, "stir modules A-D", ha="center", fontsize=7, color=INK2)
    ax.add_patch(Rectangle(RACK1[:2], RACK1[2] - RACK1[0], RACK1[3] - RACK1[1], fill=False, ec=BEN, lw=1.0, zorder=2))
    ax.text(287, 150, "tip rack 1", rotation=90, ha="center", va="center", fontsize=7, color=INK2)
    ax.add_patch(Rectangle(HOLDER[:2], HOLDER[2] - HOLDER[0], HOLDER[3] - HOLDER[1], fill=False, ec=BEN, lw=1.0, ls=(0, (3, 2)), zorder=2))
    ax.text(318, 150, "9-vial holder\n(plan's x 318)", rotation=90, ha="center", va="center", fontsize=7, color=INK2)
    # the keyed parts and their keys
    for name, rec in d["parts"].items():
        m = trimesh.load(AC / rec["file"].replace(".step", ".stl"), force="mesh")
        outline = projected(m, normal=[0, 0, 1], ignore_sign=True, rpad=1e-4, apad=1e-4)
        dashed = name == "tip_rack_2x15"
        add_poly(ax, outline, fc=PART, ec=INK, lw=0.9, ls=(0, (3, 2)) if dashed else "-", zorder=3)
        for pk in rec["pockets"]:
            add_poly(ax, pill(pk["x"], pk["y"], 9.8, 24.8), fc=KEY, ec="none", alpha=0.35, zorder=4)
            add_poly(ax, tri(pk["x"], pk["y"], 3.1, 1.1, pk["corner_deg"]), fc=KEY, ec=INK, lw=0.5, zorder=5)
        b = m.bounds
        cx, cy = (b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2
        dy = {"coupon_tray": 9, "cup_block_3": 9, "tube_rack_2x8": 9, "tip_waste_cup": 8, "tip_rack_2x15": -30}.get(name, 0)
        ax.text(cx, cy + dy, LABELS[name], ha="center", va="center", fontsize=7.5, color=INK, zorder=6,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
    ax.set_xlim(-12, 420)
    ax.set_ylim(-16, 292)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(0, 401, 50))
    ax.set_yticks(np.arange(0, 281, 45))
    ax.tick_params(labelsize=7, colors=INK2)
    for s in ax.spines.values():
        s.set_color(SLOT)
    ax.set_xlabel("deck x, mm (CubOS frame of Ben's 2026-10-02 calibration)", fontsize=8, color=INK2)
    ax.set_ylabel("deck y, mm", fontsize=8, color=INK2)
    ax.set_title("A  Where each part's keys drop in", loc="left", fontsize=10, fontweight="bold", color=INK)
    ax.text(2, -12, "Slots: X = 12.5 + 25n, Y = 45m, a best estimate (about ±1 mm in X, ±2 mm in Y). Dashed box: capper reach.",
            fontsize=6.8, color=MUTED)


def section(ax, d):
    """Through a key along X: deck plate with its slot, the pill, the nub in the part's pocket. To scale."""
    ax.set_facecolor(SURF)
    T = d["deck"]["plate_t_in_step"]
    ax.add_patch(Rectangle((-16, -T), 11, T, fc="#cfd8e3", ec=INK2, lw=0.8))
    ax.add_patch(Rectangle((5, -T), 11, T, fc="#cfd8e3", ec=INK2, lw=0.8))
    ax.text(-10.5, -T / 2, "deck\nplate\n10", ha="center", va="center", fontsize=7, color=INK2)
    ax.add_patch(Rectangle((-4.9, -T), 9.8, T, fc=KEY, ec=INK, lw=0.8, alpha=0.55))
    ax.text(0, -T / 2, "pill\n9.8 in a\n10 slot", ha="center", va="center", fontsize=7, color=INK)
    # nub: B = 7.67 across, 2.0 tall, 0.3 lead-in
    b = d["key"]["files"]["deck_key"]["B_across_corners_mm"] / 2
    ax.add_patch(MplPolygon([(-b, 0), (b, 0), (b, 1.7), (b - 0.3, 2.0), (-b + 0.3, 2.0), (-b, 1.7)], closed=True,
                            fc=KEY, ec=INK, lw=0.8))
    pb = d["pocket"]["B_across_corners_mm"] / 2
    ax.add_patch(MplPolygon([(-16, 0), (-pb, 0), (-pb, 2.1), (pb, 2.1), (pb, 0), (16, 0), (16, 6), (-16, 6)], closed=True,
                            fc=PART, ec=INK, lw=0.8))
    ax.text(0, 4.2, "printed part", ha="center", fontsize=7.5, color=INK)
    ax.annotate("pocket", xy=(pb - 0.2, 2.0), xytext=(8.0, 2.4), fontsize=7, color=INK, va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK2))
    ax.annotate("nub", xy=(-b + 0.6, 1.0), xytext=(-12.5, 1.6), fontsize=7, color=INK, va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK2))
    ax.set_xlim(-16.5, 16.5)
    ax.set_ylim(-21, 7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("B  One key, cut across (mm, to scale)", loc="left", fontsize=10, fontweight="bold", color=INK)
    ax.text(-16, -11.5, "Pocket 2.1 deep, R1.1 corners. Nub 2.0 tall with a\n0.3 lead-in, R1.15: 0.05 mm bigger all round, a press\n"
            "fit. Pill 9.8 x 24.8 in a 10 x 25 slot: 0.1 play a side.\n\nThe part rests on the deck and the key only locates\n"
            "it: keys don't hold a part down.", fontsize=7, color=INK2, va="top")


def main():
    d = json.loads((HERE / "deck_keys.json").read_text())
    plt.rcParams.update({"font.family": "DejaVu Sans"})
    fig = plt.figure(figsize=(13.0, 6.6), dpi=110)
    fig.patch.set_facecolor(SURF)
    gs = fig.add_gridspec(1, 2, width_ratios=(3.0, 1.05), left=0.05, right=0.985, top=0.83, bottom=0.09, wspace=0.06)
    plan(fig.add_subplot(gs[0, 0]), d)
    section(fig.add_subplot(gs[0, 1]), d)
    n = sum(d["keys_needed"].values())
    fig.suptitle(f"Deck keys for the corrosion parts: {n} keys in {len(d['parts'])} parts, each pocket at a PandaDeck slot centre",
                 x=0.05, ha="left", y=0.975, fontsize=12, fontweight="bold", color=INK)
    handles = [Rectangle((0, 0), 1, 1, fc=PART, ec=INK), Rectangle((0, 0), 1, 1, fc=KEY, ec=INK),
               Rectangle((0, 0), 1, 1, fill=False, ec=BEN), Rectangle((0, 0), 1, 1, fill=False, ec=SLOT)]
    fig.legend(handles, ["printed part (keyed)", "key: pill in the slot, nub in the part", "Ben's keyed items, for context",
                         "PandaDeck slot (10 x 25)"], loc="upper left", bbox_to_anchor=(0.045, 0.94), ncol=4, fontsize=7.5,
               frameon=False)
    fig.savefig(HERE / "deck-keys.png", facecolor=SURF)
    plt.close(fig)


if __name__ == "__main__":
    main()
