"""
LPBF Processing Parameter Space Visualization (v4 — modular)
=============================================================
High-impact proposal figure showing the full dimensionality of the LPBF
parameter space (36 parameters across 7 categories) and the compounding
effect for multi-material additive manufacturing.

Modular architecture: each panel is a standalone module in figures/panels/
that can be generated independently and assembled here.

v4: Replaced sunburst (Panel A) with tile grid for improved readability.
    Each panel is independently runnable and reusable.

References: Edison Scientific LITERATURE_HIGH (38 citations) + two ANALYSIS
feedback cycles (12 citations total), including Oliveira et al. 2020 (1057 cit.),
Buhairi et al. 2023 (204 cit.), Ferro et al. 2020 (142 cit.)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import os
import sys

# Add panels directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'panels'))
from shared import apply_rcparams, STATUS_COLORS, STATUS_LABELS, CAT_COLORS, CATEGORIES
from panel_a_parameter_grid import draw_parameter_grid
from panel_b_dimensionality import draw_dimensionality_scaling
from panel_c_network import draw_interaction_network


def _count_status(status):
    return sum(1 for _, _, params in CATEGORIES for _, s in params if s == status)


def create_figure():
    """Assemble the full proposal figure with GridSpec layout.

    Layout restructured per Edison iter 5: Panel A spans full width on top
    (needs ~8" for 8-param rows), B and C side-by-side below.
    Canvas: 8.5×7.0" for full-width A-on-top layout.
    """
    apply_rcparams()
    fig = plt.figure(figsize=(8.5, 7.0), dpi=300, facecolor='white')  # Full-width A-on-top

    gs = GridSpec(
        2, 2, figure=fig,
        width_ratios=[1.0, 1.0], height_ratios=[1.0, 0.75],
        left=0.02, right=0.98, top=0.90, bottom=0.14,
        wspace=0.15, hspace=0.16
    )

    ax_grid = fig.add_subplot(gs[0, :])   # Panel A: full width top row
    ax_bar = fig.add_subplot(gs[1, 0])    # Panel B: bottom left
    ax_net = fig.add_subplot(gs[1, 1])    # Panel C: bottom right

    # Argumentative title + subtitle (consolidated per iter 7 fix #1)
    fig.suptitle("LPBF optimization is not a 2-parameter problem",
                 y=0.975, color='#1D3557', fontsize=13, fontweight='bold')
    fig.text(0.5, 0.935,
             "Power/scan-speed studies explore 2\u20134 variables,"
             " while practical LPBF control spans 36+ dimensions"
             " \u2014 and grows with each added material",
             ha='center', va='center', fontsize=8, color='#627D98',
             fontstyle='italic')

    # Panel labels with takeaway subtitles — offset A subtitle to avoid collision
    ax_grid.text(-0.02, 1.04, "A", transform=ax_grid.transAxes,
                fontsize=11, fontweight='bold', color='#1D3557',
                ha='left', va='bottom')
    ax_grid.text(0.04, 1.00,
                "36 controllable variables across beam, scan, powder, environment, and machine domains",
                transform=ax_grid.transAxes,
                fontsize=7.0, color='#486581', ha='left', va='bottom')

    for ax, label, takeaway in [
        (ax_bar, "B",
         "Published studies explore 2\u20134 dimensions;\n"
         "real search spaces are an order of magnitude larger"),
        (ax_net, "C",
         "Cross-category couplings make 1D surrogates\n"
         "like VED insufficient"),
    ]:
        ax.text(-0.02, 1.06, label, transform=ax.transAxes,
                fontsize=11, fontweight='bold', color='#1D3557',
                ha='left', va='bottom')
        ax.text(0.04, 1.01, takeaway, transform=ax.transAxes,
                fontsize=7.0, color='#486581', ha='left', va='bottom',
                linespacing=1.2)

    draw_parameter_grid(ax_grid)
    draw_dimensionality_scaling(ax_bar)
    draw_interaction_network(ax_net)

    # BO callout — below panels, above legend (Edison iter 8 Issue 1 fix)
    fig.text(
        0.50, 0.080,
        "36\u201398D search spaces with strong coupling are intractable\n"
        "for conventional DoE \u2192 autonomous Bayesian optimization is well-suited",
        ha='center', va='center', fontsize=7.5, color='#7C2D12',
        fontweight='medium',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF7ED',
                  edgecolor='#E69F00', alpha=0.9, linewidth=1.0))

    # ─── Legends (separated vertically per iter 6 fix #2) ───

    # Primary legend: optimization prevalence — centered bottom
    status_handles = [
        mpatches.Patch(facecolor=STATUS_COLORS[k],
                       label=f"{STATUS_LABELS[k]} ({_count_status(k)})",
                       edgecolor='white',
                       hatch='////' if k == 'neglected' else None)
        for k in ['optimized', 'selective', 'fixed', 'neglected']
    ]
    fig.legend(handles=status_handles, loc='lower center', ncol=4,
               fontsize=7.5, frameon=True, fancybox=True,
               edgecolor='#BCCCDC', facecolor='white',
               bbox_to_anchor=(0.52, -0.005), handlelength=1.2,
               title="Optimization prevalence (Panel A accent color)",
               title_fontsize=7.5)

    # Secondary legend: category colors — upper right of figure, near Panel A
    cat_handles = [
        mpatches.Patch(facecolor=CAT_COLORS[k], edgecolor='none',
                       label=name.split('/')[0].strip())
        for (name, k, _) in CATEGORIES
    ]
    fig.legend(handles=cat_handles, loc='upper right',
               bbox_to_anchor=(0.98, 0.895), ncol=7,
               frameon=True, fancybox=True,
               edgecolor='#BCCCDC', facecolor='white',
               fontsize=7.0, handlelength=1.0,
               title="Category (A dots / C nodes)",
               title_fontsize=7.0)

    # Source attribution — positioned below legend
    fig.text(0.98, -0.020,
             "Literature synthesis (38 studies)"
             " | Oliveira et al. 2020, Buhairi et al. 2023, Ferro et al. 2020",
             fontsize=7.0, ha='right', va='bottom', color='#9FB3C8',
             fontstyle='italic')

    return fig


if __name__ == "__main__":
    fig = create_figure()
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_base = os.path.join(out_dir, "lpbf_parameter_space")
    fig.savefig(out_base + ".png", dpi=300, bbox_inches='tight',
                facecolor='white', pad_inches=0.12)
    fig.savefig(out_base + ".pdf", bbox_inches='tight',
                facecolor='white', pad_inches=0.12,
                metadata={"Title": "LPBF parameter space",
                          "Author": "BYU Vertical Cloud Lab"})
    print(f"Saved: {out_base}.png and .pdf")
    plt.close(fig)
