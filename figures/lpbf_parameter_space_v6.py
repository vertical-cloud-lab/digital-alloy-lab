"""
LPBF Processing Parameter Space Visualization (v6 — process block drafts)
========================================================================

Assembles the large dimensionality overview with the new process-representative
block drafts.  The block drafts are deliberately modular: each LPBF process
domain can be rendered on its own via ``panel_process_block_drafts.py``.

Run:
    python figures/lpbf_parameter_space_v6.py
"""

from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "panels"))

from shared import apply_rcparams, TOTAL_PARAMS  # noqa: E402
from panel_isometric_overview import draw_isometric_overview  # noqa: E402
from panel_process_block_drafts import draw_process_block_grid  # noqa: E402


def create_figure():
    apply_rcparams()
    fig = plt.figure(figsize=(11.5, 9.3), dpi=300, facecolor="white")
    subfigs = fig.subfigures(2, 1, height_ratios=[0.86, 1.0], hspace=0.02)

    sf_top = subfigs[0]
    ax3d = sf_top.add_subplot(111, projection="3d")
    draw_isometric_overview(ax=ax3d, materials=(1, 2, 3),
                            show_legend=True, show_title=False)
    sf_top.suptitle(
        "LPBF process windows are high-dimensional — and each domain is a distinct physical control block",
        fontsize=13.5, weight="semibold", color="#172B4D", y=0.98,
    )

    sf_bot = subfigs[1]
    draw_process_block_grid(fig=sf_bot, ncols=4)

    fig.text(
        0.5, 0.004,
        f"{TOTAL_PARAMS} controllable parameters · 7 process domains · literature synthesis (38 studies)",
        ha="center", va="bottom", fontsize=8, color="#5A6B79", style="italic",
    )
    return fig


def main(out_path: str | None = None):
    fig = create_figure()
    if out_path is None:
        out_path = os.path.join(HERE, "lpbf_parameter_space_v6.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"wrote {out_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
