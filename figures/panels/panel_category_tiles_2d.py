"""
Panel: Per-category 2D tiles (small multiples).

A 2D companion to ``panel_category_tiles_iso``: one flat tile per LPBF
category, each parameter shown as a labeled, accent-bordered chip.
Typography follows Doumont's left-alignment principle.

Run standalone:
    python figures/panels/panel_category_tiles_2d.py
"""

from __future__ import annotations

import os
import sys
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import (  # noqa: E402
    apply_rcparams, CATEGORIES, STATUS_COLORS, STATUS_LABELS,
)


def _draw_chip(ax, x, y, w, h, label, status):
    """Accent-border chip: light body + colored left bar + left-aligned text."""
    color = STATUS_COLORS[status]
    # Body
    body = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.04",
        facecolor="#FAFBFC", edgecolor="#C7CDD3", linewidth=0.6,
    )
    ax.add_patch(body)
    # Accent bar (left)
    bar_w = w * 0.10
    accent = Rectangle(
        (x, y), bar_w, h,
        facecolor=color, edgecolor="none",
    )
    ax.add_patch(accent)
    ax.text(
        x + bar_w + 0.04, y + h / 2.0, label,
        ha="left", va="center",
        fontsize=8.0, color="#1A1A1A",
    )


def _draw_one_tile(ax, cat_name, params, ncols=2):
    n = len(params)
    nrows = math.ceil(n / ncols)
    chip_w = 1.0 / ncols - 0.04
    chip_h = 0.18

    pad_top = 0.18
    available = 1.0 - pad_top - 0.04
    row_h = max(chip_h + 0.04, available / max(nrows, 1))

    for i, (pname, status) in enumerate(params):
        col = i % ncols
        row = i // ncols
        x = col * (chip_w + 0.04) + 0.02
        y = 1.0 - pad_top - (row + 1) * row_h + (row_h - chip_h) / 2.0
        _draw_chip(ax, x, y, chip_w, chip_h, pname, status)

    ax.text(
        0.02, 1.0 - 0.04, f"{cat_name}",
        ha="left", va="top",
        fontsize=10, fontweight="bold", color="#1A1A1A",
        transform=ax.transAxes,
    )
    ax.text(
        0.98, 1.0 - 0.04, f"{n}",
        ha="right", va="top",
        fontsize=10, fontweight="bold", color="#5A6B79",
        transform=ax.transAxes,
    )

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def draw_category_tiles_2d(fig=None, ncols: int = 4):
    """Build a 2D small-multiples grid (one tile per category)."""
    apply_rcparams()
    n_cats = len(CATEGORIES)
    nrows = math.ceil(n_cats / ncols)

    if fig is None:
        fig = plt.figure(
            figsize=(2.6 * ncols, 2.0 * nrows + 0.8),
            dpi=300, facecolor="white",
        )

    for idx, (cat_name, _ck, params) in enumerate(CATEGORIES):
        ax = fig.add_subplot(nrows, ncols, idx + 1)
        _draw_one_tile(ax, cat_name, params)

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
        "Each category, in 2D — accent-bordered chips for at-a-glance scanning",
        fontsize=12, fontweight="bold", y=0.98,
    )
    fig.subplots_adjust(left=0.03, right=0.97, top=0.92,
                        bottom=0.10, wspace=0.18, hspace=0.30)
    return fig


def main(out_path: str | None = None):
    fig = draw_category_tiles_2d()
    if out_path is None:
        out_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "out", "panel_category_tiles_2d.png",
        )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"wrote {out_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
