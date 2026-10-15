"""
LPBF Processing Parameter Space Visualization (v5 — isometric + tiles)
======================================================================

Top-level assembly: large isometric overview of the 36-D parameter space
on top, with the 2D per-category tile strip below it. Each panel is also
runnable on its own (see ``figures/panels/panel_*.py``).

The previous v4 (donut + bar + network) is retained as ``lpbf_parameter_space.py``
so existing references remain valid; v5 is a fresh, isometric-first view
intended as the high-impact proposal centerpiece.

Run:
    python figures/lpbf_parameter_space_v5.py
"""

from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "panels"))

from shared import apply_rcparams, TOTAL_PARAMS  # noqa: E402
from panel_isometric_overview import draw_isometric_overview  # noqa: E402
from panel_category_tiles_2d import draw_category_tiles_2d  # noqa: E402


def create_figure():
    apply_rcparams()
    # The combined figure is two stacked sub-figures so the 3D axes and the
    # 2D grid don't interfere with each other's layout/legends.
    fig = plt.figure(figsize=(11.5, 10.0), dpi=300, facecolor="white")
    subfigs = fig.subfigures(2, 1, height_ratios=[1.05, 1.0],
                             hspace=0.04)

    # ── Top: isometric overview ───────────────────────────────────────────
    sf_top = subfigs[0]
    ax3d = sf_top.add_subplot(111, projection="3d")
    draw_isometric_overview(ax=ax3d, materials=(1, 2, 3),
                            show_legend=True, show_title=False)
    sf_top.suptitle(
        "LPBF practical control spans 36 dimensions per material — "
        "+31 D for every additional alloy",
        fontsize=14, fontweight="bold", y=0.98,
    )

    # ── Bottom: per-category 2D tiles ─────────────────────────────────────
    sf_bot = subfigs[1]
    draw_category_tiles_2d(fig=sf_bot, ncols=4)

    fig.text(
        0.5, 0.005,
        f"{TOTAL_PARAMS} controllable parameters · 7 categories · "
        "literature synthesis (38 studies)",
        ha="center", va="bottom",
        fontsize=8, color="#5A6B79", style="italic",
    )
    return fig


def main(out_path: str | None = None):
    fig = create_figure()
    if out_path is None:
        out_path = os.path.join(HERE, "lpbf_parameter_space_v5.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"wrote {out_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
