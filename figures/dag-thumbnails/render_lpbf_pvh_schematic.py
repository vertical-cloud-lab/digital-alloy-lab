"""Render an isometric P-V-H schematic for the LPBF process node (`inp_p`).

Uses a manual isometric projection on a 2D matplotlib axes (avoids mpl3d
depth-sort headaches). Draws build plate, parallel hatch tracks, melt-pool
ellipse, laser column, and side cutaway exposing layer thickness.

Annotates only P, v, h, t (no commentary, no equations).

Saves to figures/dag-thumbnails/lpbf_pvh_schematic.png.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Polygon

OUT = Path(__file__).resolve().parent / "lpbf_pvh_schematic.png"

# -- Isometric projection ------------------------------------------------------
# Standard isometric: x-axis goes down-right, y-axis goes down-left,
# z-axis goes straight up.  Tweak angle for a slightly elevated camera.
ANGLE_X = math.radians(28)   # x-axis dip
ANGLE_Y = math.radians(20)   # y-axis dip


def iso(p):
    """Project a 3D world coord (x, y, z) to 2D screen coord."""
    x, y, z = p
    sx = x * math.cos(ANGLE_X) - y * math.cos(ANGLE_Y)
    sy = -x * math.sin(ANGLE_X) - y * math.sin(ANGLE_Y) + z
    return (sx, sy)


def iso_poly(verts3d):
    return [iso(v) for v in verts3d]


# -- Geometry ------------------------------------------------------------------
PLATE_X = 6.0   # along scan direction
PLATE_Y = 4.0   # transverse (hatch) direction
PLATE_Z = 0.55  # plate thickness
N_TRACKS = 5
HATCH = PLATE_Y / (N_TRACKS + 1)
TRACK_HALFW = 0.16
TRACK_RISE = 0.07  # how much each track stands proud of plate top
LASER_TIP_X = PLATE_X * 0.62
LASER_TIP_Y = HATCH  # front-most track Y (smallest y)
LASER_HEIGHT = 3.4
LASER_R_TOP = 0.55
LASER_R_TIP = 0.10

LASER_FILL = "#f5b03e"
LASER_EDGE = "#b87b1c"
PLATE_TOP = "#dde2e8"
PLATE_SIDE = "#9aa3ad"
PLATE_FRONT = "#aab2bb"
TRACK_FILL = "#3d6fb1"
TRACK_EDGE = "#1f3a66"
MELT_FILL = "#d63a2a"
MELT_EDGE = "#7a1f15"
LABEL_COLOR = "#1a1a1a"
CAPTION_COLOR = "#5a5a5a"
CAL_COLOR = "#1a1a1a"


def add_face(ax, verts3d, **kw):
    poly = Polygon(iso_poly(verts3d), closed=True, **kw)
    ax.add_patch(poly)
    return poly


def draw_plate(ax):
    z0, z1 = 0.0, PLATE_Z
    cut_x0 = PLATE_X * 0.78
    cut_z = z1 - 0.18
    # Left face (x=0) -- visible at back-left
    add_face(
        ax,
        [(0, 0, z0), (0, PLATE_Y, z0), (0, PLATE_Y, z1), (0, 0, z1)],
        facecolor=PLATE_SIDE,
        edgecolor="#3a3f44",
        linewidth=0.7,
        zorder=1.0,
    )
    # Back face (y=PLATE_Y)
    add_face(
        ax,
        [(0, PLATE_Y, z0), (PLATE_X, PLATE_Y, z0), (PLATE_X, PLATE_Y, z1), (0, PLATE_Y, z1)],
        facecolor="#8a929c",
        edgecolor="#3a3f44",
        linewidth=0.7,
        zorder=1.0,
    )
    # Right face (x=PLATE_X)
    add_face(
        ax,
        [(PLATE_X, 0, z0), (PLATE_X, PLATE_Y, z0), (PLATE_X, PLATE_Y, z1), (PLATE_X, 0, z1)],
        facecolor=PLATE_SIDE,
        edgecolor="#3a3f44",
        linewidth=0.7,
        zorder=1.5,
    )
    # Front face (y=0) -- with cutaway on right exposing layer thickness t.
    # Lower full-width band (z0 -> cut_z)
    add_face(
        ax,
        [(0, 0, z0), (PLATE_X, 0, z0), (PLATE_X, 0, cut_z), (0, 0, cut_z)],
        facecolor=PLATE_FRONT,
        edgecolor="#3a3f44",
        linewidth=0.7,
        zorder=2.0,
    )
    # Upper band of front face, ONLY left of cut_x0 (cut_z -> z1)
    add_face(
        ax,
        [(0, 0, cut_z), (cut_x0, 0, cut_z), (cut_x0, 0, z1), (0, 0, z1)],
        facecolor=PLATE_FRONT,
        edgecolor="#3a3f44",
        linewidth=0.7,
        zorder=2.0,
    )
    # Cutaway step (vertical wall at x=cut_x0, from cut_z to z1, recessed in y)
    add_face(
        ax,
        [(cut_x0, 0, cut_z), (cut_x0, 0, z1), (cut_x0, 0.20, z1), (cut_x0, 0.20, cut_z)],
        facecolor="#7c848e",
        edgecolor="#3a3f44",
        linewidth=0.6,
        zorder=2.2,
    )
    # Cutaway floor (recessed top at cut_z)
    add_face(
        ax,
        [(cut_x0, 0, cut_z), (PLATE_X, 0, cut_z), (PLATE_X, 0.20, cut_z), (cut_x0, 0.20, cut_z)],
        facecolor="#c5ccd3",
        edgecolor="#3a3f44",
        linewidth=0.6,
        zorder=2.4,
    )
    # Top face (whole plate). Tracks render on top of this.
    add_face(
        ax,
        [(0, 0, z1), (PLATE_X, 0, z1), (PLATE_X, PLATE_Y, z1), (0, PLATE_Y, z1)],
        facecolor=PLATE_TOP,
        edgecolor="#3a3f44",
        linewidth=0.7,
        zorder=3.0,
    )
    return cut_z, cut_x0


def draw_tracks(ax):
    z_bot = PLATE_Z
    z_top = PLATE_Z + TRACK_RISE
    for i in range(1, N_TRACKS + 1):
        y = i * HATCH
        x0, x1 = 0.20, PLATE_X - 0.20
        y0, y1 = y - TRACK_HALFW, y + TRACK_HALFW
        # Front face (y=y0) -- visible from camera
        add_face(
            ax,
            [(x0, y0, z_bot), (x1, y0, z_bot), (x1, y0, z_top), (x0, y0, z_top)],
            facecolor=TRACK_FILL,
            edgecolor=TRACK_EDGE,
            linewidth=0.4,
            zorder=4.0 + 0.01 * i,
        )
        # Right face (x=x1) -- visible from camera
        add_face(
            ax,
            [(x1, y0, z_bot), (x1, y1, z_bot), (x1, y1, z_top), (x1, y0, z_top)],
            facecolor="#2f5a94",
            edgecolor=TRACK_EDGE,
            linewidth=0.4,
            zorder=4.05 + 0.01 * i,
        )
        # Top face -- the visible scan ribbon
        add_face(
            ax,
            [(x0, y0, z_top), (x1, y0, z_top), (x1, y1, z_top), (x0, y1, z_top)],
            facecolor=TRACK_FILL,
            edgecolor=TRACK_EDGE,
            linewidth=0.4,
            zorder=4.10 + 0.01 * i,
        )


def draw_melt_pool(ax):
    """Red ellipse on the front-most track at the laser tip."""
    y0 = LASER_TIP_Y
    z = PLATE_Z + TRACK_RISE + 0.005
    theta = np.linspace(0, 2 * np.pi, 60)
    a, b = 0.55, 0.20
    pts3d = [(LASER_TIP_X + a * math.cos(t), y0 + b * math.sin(t), z) for t in theta]
    poly = Polygon(iso_poly(pts3d), closed=True,
                   facecolor=MELT_FILL, edgecolor=MELT_EDGE,
                   linewidth=1.0, zorder=5.0)
    ax.add_patch(poly)


def draw_laser(ax):
    """Translucent tapered square frustum from above the bed down to the laser tip."""
    x0 = LASER_TIP_X
    y0 = LASER_TIP_Y
    z_top_world = PLATE_Z + LASER_HEIGHT
    z_tip = PLATE_Z + TRACK_RISE + 0.01
    rt, rb = LASER_R_TOP, LASER_R_TIP
    top = [
        (x0 - rt, y0 - rt, z_top_world),
        (x0 + rt, y0 - rt, z_top_world),
        (x0 + rt, y0 + rt, z_top_world),
        (x0 - rt, y0 + rt, z_top_world),
    ]
    bot = [
        (x0 - rb, y0 - rb, z_tip),
        (x0 + rb, y0 - rb, z_tip),
        (x0 + rb, y0 + rb, z_tip),
        (x0 - rb, y0 + rb, z_tip),
    ]
    # Render the four side faces with descending alpha for a glow look.
    for i in range(4):
        j = (i + 1) % 4
        add_face(
            ax,
            [top[i], top[j], bot[j], bot[i]],
            facecolor=LASER_FILL,
            edgecolor=LASER_EDGE,
            linewidth=0.4,
            alpha=0.45,
            zorder=6.0 + 0.05 * i,
        )
    # Top cap (opaque)
    add_face(
        ax, top,
        facecolor=LASER_EDGE, edgecolor=LASER_EDGE, linewidth=0.4,
        alpha=0.95, zorder=6.5,
    )


def draw_arrow_2d(ax, p0_3d, p1_3d, color=CAL_COLOR, lw=1.7, mut=14, style="-|>", zorder=10):
    p0 = iso(p0_3d)
    p1 = iso(p1_3d)
    arr = FancyArrowPatch(
        p0, p1, arrowstyle=style, color=color,
        lw=lw, mutation_scale=mut, zorder=zorder,
    )
    ax.add_patch(arr)


def draw_label(ax, p3d, text, dx=0.0, dy=0.0, fontsize=14, weight="bold", color=LABEL_COLOR, zorder=12, italic=False):
    sx, sy = iso(p3d)
    ax.text(
        sx + dx, sy + dy, text,
        ha="center", va="center",
        fontsize=fontsize, fontweight=weight,
        style="italic" if italic else "normal",
        color=color, zorder=zorder,
    )


def main():
    fig, ax = plt.subplots(figsize=(7.0, 4.0), dpi=600)

    cut_z, cut_x0 = draw_plate(ax)
    draw_tracks(ax)
    draw_melt_pool(ax)
    draw_laser(ax)

    # ---- Annotations ----

    # P: along laser column, mid-height. Place label to the right of the column.
    P_anchor = (LASER_TIP_X + LASER_R_TOP + 0.30, LASER_TIP_Y, PLATE_Z + LASER_HEIGHT * 0.55)
    draw_label(ax, P_anchor, r"$P$", dx=0.40, dy=0.0, fontsize=34)

    # v: along front-most track, arrow forward (positive x)
    v_z = PLATE_Z + TRACK_RISE + 0.02
    v_p0 = (LASER_TIP_X + 0.65, LASER_TIP_Y, v_z)
    v_p1 = (LASER_TIP_X + 2.10, LASER_TIP_Y, v_z)
    draw_arrow_2d(ax, v_p0, v_p1, lw=2.4, mut=22, zorder=11)
    v_label_anchor = (LASER_TIP_X + 1.30, LASER_TIP_Y, v_z)
    draw_label(ax, v_label_anchor, r"$v$", dx=0.0, dy=0.75, fontsize=34, italic=True)

    # h: caliper spanning two adjacent tracks at left edge (made wider for legibility)
    h_x = 0.55
    z_cal = PLATE_Z + TRACK_RISE + 0.01
    y_a = 2 * HATCH
    y_b = 4 * HATCH
    h_p0 = (h_x, y_a, z_cal)
    h_p1 = (h_x, y_b, z_cal)
    draw_arrow_2d(ax, h_p0, h_p1, lw=2.2, mut=22, style="<|-|>", zorder=11)
    h_anchor = (h_x, (y_a + y_b) / 2, z_cal)
    draw_label(ax, h_anchor, r"$h$", dx=-0.65, dy=0.10, fontsize=32, italic=True)

    # t: caliper on side cutaway (front face), measuring from cut_z up to PLATE_Z
    t_x = (cut_x0 + PLATE_X) / 2
    t_p0 = (t_x, 0, cut_z)
    t_p1 = (t_x, 0, PLATE_Z)
    draw_arrow_2d(ax, t_p0, t_p1, lw=2.0, mut=18, style="<|-|>", zorder=11)
    t_anchor = (t_x, 0, (cut_z + PLATE_Z) / 2)
    draw_label(ax, t_anchor, r"$t$", dx=0.55, dy=0.10, fontsize=30, italic=True)

    # ---- Axes / cleanup ----
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.autoscale_view()

    # Add a little padding around content
    xs, ys = zip(*[iso(p) for p in [
        (0, 0, 0), (PLATE_X, 0, 0), (PLATE_X, PLATE_Y, 0), (0, PLATE_Y, 0),
        (LASER_TIP_X, LASER_TIP_Y, PLATE_Z + LASER_HEIGHT + 0.2),
        (LASER_TIP_X + 2.6, LASER_TIP_Y, PLATE_Z + TRACK_RISE),
    ]])
    pad_x = 0.6
    pad_y = 0.6
    ax.set_xlim(min(xs) - pad_x, max(xs) + pad_x + 0.8)
    ax.set_ylim(min(ys) - pad_y, max(ys) + pad_y + 0.4)

    plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
    fig.savefig(OUT, dpi=600, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
