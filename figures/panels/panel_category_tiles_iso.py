"""
Panel: Per-category isometric tiles (small multiples).

Renders one small isometric tile per LPBF parameter category, each showing
the parameters in that category as colored unit cubes arranged in a short
row. Stacked layers (n=1, 2, 3 materials) reuse the language of
``panel_isometric_overview`` so the tiles read as zoomed-in views of the
overview "skyline".

Run standalone:
    python figures/panels/panel_category_tiles_iso.py
"""

from __future__ import annotations

import os
import sys
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import (  # noqa: E402
    apply_rcparams, CATEGORIES, STATUS_COLORS, STATUS_LABELS,
)


def _draw_one_tile(ax, cat_name, params, materials=(1, 2, 3),
                   col_w=0.85, col_d=0.85, layer_h=1.0):
    """Render a single category tile in 3D iso view."""
    n = len(params)
    for i, (pname, status) in enumerate(params):
        x = i * (col_w + 0.10)
        for li, _m in enumerate(materials):
            z0 = li * (layer_h + 0.08)
            alpha = 1.0 if li == 0 else 0.55
            ax.bar3d(
                x, 0.0, z0,
                col_w, col_d, layer_h,
                color=STATUS_COLORS[status],
                edgecolor="#2A2A2A", linewidth=0.35,
                alpha=alpha, shade=True,
            )

    x_max = max((n - 1) * (col_w + 0.10) + col_w, col_w)
    z_top = len(materials) * (layer_h + 0.08) - 0.08

    ax.set_proj_type("ortho")
    ax.view_init(elev=22, azim=-58)
    ax.set_box_aspect((x_max + 0.5, 1.6, z_top + 0.6))
    ax.set_xlim(-0.2, x_max + 0.2)
    ax.set_ylim(-0.2, 1.6)
    ax.set_zlim(0, z_top + 0.4)

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        axis.line.set_color((1, 1, 1, 0))
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.grid(False)

    ax.set_title(
        f"{cat_name}  ({n})",
        fontsize=9.5, fontweight="bold", color="#1A1A1A", pad=4,
    )


def draw_category_tiles_iso(fig=None, materials=(1, 2, 3),
                            ncols: int = 4):
    """Build a small-multiples grid (one iso tile per category).

    Returns the figure used.
    """
    apply_rcparams()
    n_cats = len(CATEGORIES)
    nrows = math.ceil(n_cats / ncols)

    if fig is None:
        fig = plt.figure(
            figsize=(2.6 * ncols, 2.4 * nrows + 0.8),
            dpi=300, facecolor="white",
        )

    for idx, (cat_name, _ck, params) in enumerate(CATEGORIES):
        ax = fig.add_subplot(nrows, ncols, idx + 1, projection="3d")
        _draw_one_tile(ax, cat_name, params, materials=materials)

    # Shared legend at the bottom
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

    fig.suptitle(
        "Each category, in isometric — stacked layers show n = 1 → 2 → 3 materials",
        fontsize=12, fontweight="bold", y=0.98,
    )
    fig.subplots_adjust(left=0.02, right=0.98, top=0.92,
                        bottom=0.10, wspace=0.05, hspace=0.20)
    return fig


def main(out_path: str | None = None):
    fig = draw_category_tiles_iso()
    if out_path is None:
        out_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "out", "panel_category_tiles_iso.png",
        )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"wrote {out_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
