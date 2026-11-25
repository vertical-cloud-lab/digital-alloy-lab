"""
Panel: Isometric overview of the 36-D LPBF parameter space.

Renders the full parameter space as an isometric "skyline" of unit cubes:
each parameter is one column, grouped into 7 category bays along the x-axis,
and stacked along the z-axis to show how the dimensionality compounds with
each additional material in a multi-material build (n = 1 → 2 → 3).

Color encodes optimization-status prevalence (Actively / Selectively /
Typically fixed / Often neglected). The single panel doubles as a
"this is what you're searching" centerpiece for the proposal figure.

Run standalone:
    python figures/panels/panel_isometric_overview.py
"""

from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import (  # noqa: E402
    apply_rcparams,
    CATEGORIES,
    STATUS_COLORS,
    STATUS_LABELS,
    TOTAL_PARAMS,
)


# ───────────────────────────── layout helpers ────────────────────────────────

# Short labels to keep tile/leader text legible in 3D
SHORT_CATEGORY = {
    "Beam / Energy":      "Beam",
    "Scan Strategy":      "Scan",
    "Layer / Build":      "Layer",
    "Powder / Feedstock": "Powder",
    "Atmosphere":         "Atmos.",
    "Thermal Mgmt":       "Thermal",
    "Machine-Specific":   "Machine",
}


def _layout_columns(bay_gap: float = 0.6, col_w: float = 0.85):
    """Assign (x, label, status, category_index) for every parameter.

    Categories are laid out left-to-right along x. Within each category,
    parameters are arranged in a single row of unit columns.
    Returns (placements, bay_centers, bay_widths).
    """
    placements = []
    bay_centers = []
    bay_widths = []
    cursor = 0.0
    for ci, (cat_name, _ckey, params) in enumerate(CATEGORIES):
        start = cursor
        for (pname, status) in params:
            placements.append({
                "x": cursor,
                "name": pname,
                "status": status,
                "cat_idx": ci,
                "cat_name": cat_name,
            })
            cursor += col_w + 0.06   # tight columns within bay
        end = cursor - 0.06
        bay_centers.append((start + end) / 2.0)
        bay_widths.append(end - start)
        cursor += bay_gap            # gap between bays
    return placements, bay_centers, bay_widths


def _draw_skyline(ax, placements, materials=(1, 2, 3), col_w=0.85,
                  col_d=0.85, layer_h=1.0, edgecolor="#2A2A2A"):
    """Draw isometric stacks: one column per parameter, repeated per material.

    Each material adds another translucent layer on top of the previous,
    making the +31 per-material scaling visually concrete.
    """
    n_materials = len(materials)
    for layer_i, n in enumerate(materials):
        z0 = layer_i * (layer_h + 0.08)
        # Solid bottom layer, translucent layers above
        alpha = 1.0 if layer_i == 0 else 0.55
        for p in placements:
            color = STATUS_COLORS[p["status"]]
            ax.bar3d(
                p["x"], 0.0, z0,
                col_w, col_d, layer_h,
                color=color,
                edgecolor=edgecolor,
                linewidth=0.35,
                alpha=alpha,
                shade=True,
            )


def _draw_bay_labels(ax, bay_centers, bay_widths, z_top, col_d=0.85):
    """Draw category labels above each bay, in 3D coords."""
    for (cat_name, _ck, _p), cx, w in zip(CATEGORIES, bay_centers, bay_widths):
        ax.text(
            cx, col_d / 2.0, z_top + 0.45,
            SHORT_CATEGORY[cat_name],
            ha="center", va="bottom",
            fontsize=9, fontweight="bold", color="#1A1A1A",
            zorder=10,
        )


def _add_status_legend(ax, anchor=(0.01, 0.04)):
    handles = [
        mpatches.Patch(facecolor=STATUS_COLORS[k], edgecolor="#2A2A2A",
                       linewidth=0.5, label=f"{STATUS_LABELS[k]}")
        for k in ("optimized", "selective", "fixed", "neglected")
    ]
    leg = ax.legend(
        handles=handles,
        loc="lower left",
        bbox_to_anchor=anchor,
        ncol=4,
        frameon=True,
        fontsize=8,
        handlelength=1.1,
        columnspacing=1.0,
        borderpad=0.4,
    )
    leg.get_frame().set_edgecolor("#BBBBBB")
    leg.get_frame().set_linewidth(0.6)


def draw_isometric_overview(
    ax=None,
    materials=(1, 2, 3),
    show_legend: bool = True,
    show_title: bool = True,
):
    """Draw the isometric overview into a 3D axes (creates one if None).

    Returns the axes used.
    """
    apply_rcparams()
    if ax is None:
        fig = plt.figure(figsize=(11.0, 5.6), dpi=300, facecolor="white")
        ax = fig.add_subplot(111, projection="3d")
    else:
        fig = ax.figure

    placements, bay_centers, bay_widths = _layout_columns()
    layer_h = 1.0
    z_top = len(materials) * (layer_h + 0.08) - 0.08

    _draw_skyline(ax, placements, materials=materials, layer_h=layer_h)
    _draw_bay_labels(ax, bay_centers, bay_widths, z_top)

    # Per-material side annotation
    x_max = max(p["x"] for p in placements) + 1.0
    for i, n in enumerate(materials):
        z = i * (layer_h + 0.08) + layer_h / 2.0
        ax.text(
            x_max + 0.6, 0.0, z,
            f"n = {n}  →  {5 + 31 * n} D",
            ha="left", va="center",
            fontsize=9, color="#1A1A1A", fontweight="bold",
            zorder=12,
        )

    # Axes cosmetics — true isometric, hide grid clutter
    ax.set_proj_type("ortho")
    ax.view_init(elev=22, azim=-58)
    ax.set_box_aspect((x_max + 2.5, 2.4, z_top + 1.4))

    ax.set_xlim(-0.5, x_max + 2.0)
    ax.set_ylim(-0.2, 1.8)
    ax.set_zlim(0, z_top + 0.6)

    # Strip default 3D chrome
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        axis.line.set_color((1, 1, 1, 0))
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.grid(False)

    if show_title:
        ax.set_title(
            "LPBF practical control spans 36 dimensions per material — "
            "+31 D for every additional alloy",
            pad=10, fontsize=12, fontweight="bold",
        )

    if show_legend:
        # Single legend on the parent figure (3D axes legends render
        # inconsistently, so we attach to the figure for both standalone and
        # assembled use).
        handles = [
            mpatches.Patch(facecolor=STATUS_COLORS[k], edgecolor="#2A2A2A",
                           linewidth=0.5, label=STATUS_LABELS[k])
            for k in ("optimized", "selective", "fixed", "neglected")
        ]
        leg = fig.legend(
            handles=handles,
            loc="lower center",
            bbox_to_anchor=(0.5, 0.01),
            ncol=4,
            frameon=True,
            fontsize=8.5,
            handlelength=1.1,
            columnspacing=1.4,
            borderpad=0.5,
        )
        leg.get_frame().set_edgecolor("#BBBBBB")
        leg.get_frame().set_linewidth(0.6)

    # Footer: data provenance + total
    fig.text(
        0.99, 0.01,
        f"{TOTAL_PARAMS} controllable parameters · 7 categories · "
        "literature synthesis (38 studies)",
        ha="right", va="bottom", fontsize=7.5, color="#5A6B79", style="italic",
    )

    return ax


def main(out_path: str | None = None):
    apply_rcparams()
    fig = plt.figure(figsize=(11.0, 5.8), dpi=300, facecolor="white")
    ax = fig.add_subplot(111, projection="3d")
    draw_isometric_overview(ax=ax, materials=(1, 2, 3),
                            show_legend=True, show_title=True)

    fig.subplots_adjust(left=0.0, right=1.0, top=0.92, bottom=0.10)

    if out_path is None:
        out_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "out", "panel_isometric_overview.png",
        )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"wrote {out_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
