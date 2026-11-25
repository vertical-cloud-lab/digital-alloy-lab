"""
Panel B: Dimensionality Scaling Bar Chart
==========================================
Horizontal bar chart showing the jump from typical 2-4 parameter studies
to 36 (single material) → 67 → 98 (multi-material), with shaded
"typical literature search space" band and D(n) partition equation.

Can be run standalone: python panel_b_dimensionality.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared import apply_rcparams, STATUS_COLORS


def draw_dimensionality_scaling(ax, show_title=False):
    """Bar chart with shaded literature band, labeled 36-line, and D(n) equation."""
    apply_rcparams()

    scenarios = [
        "Typical study\n(P, v)",
        "Typical study\n(P, v, h, t)",
        "Single material\n(all 36 params)",
        "2-material\nbuild",
        "3-material\nbuild",
    ]
    counts = [2, 4, 36, 67, 98]
    colors_bar = ["#C8D5E0", "#C8D5E0", "#C92A2A", "#E69F00", "#0072B2"]

    if show_title:
        ax.set_title(
            "Published studies explore 2\u20134 dimensions;\n"
            "real search spaces are an order of magnitude larger",
            fontsize=10, fontweight='bold', color='#1D3557', pad=8,
        )

    # Shaded band for typical literature search space
    ax.axvspan(0, 4.5, color="#E9EEF5", alpha=0.95, zorder=0)

    bars = ax.barh(range(len(scenarios)), counts, color=colors_bar,
                   edgecolor='white', height=0.6, alpha=0.9, zorder=2)

    for bar, val in zip(bars, counts):
        xpos = bar.get_width() + 1.5
        ax.text(xpos, bar.get_y() + bar.get_height() / 2,
                f"{val}", va='center', ha='left',
                fontsize=9.5, fontweight='bold', color='#1D3557')

    ax.set_yticks(range(len(scenarios)))
    ax.set_yticklabels(scenarios, fontsize=8, color='#1D3557')
    ax.set_xlabel("Number of independent parameters",
                  fontsize=8.5, color='#546E88')
    ax.set_xlim(0, 135)
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)

    # Labeled dashed line at 36
    ax.axvline(36, color='#52606D', lw=1.2, ls='--', alpha=0.85, zorder=1)
    ax.text(37.5, -0.35, "full single-\nmaterial space",
            fontsize=7.0, color='#52606D', va='top', ha='left',
            fontstyle='italic')

    # Multi-material bracket — shifted right to clear "98" label (Edison R10 residual)
    ax.annotate("", xy=(110, 3), xytext=(110, 4),
                arrowprops=dict(arrowstyle="<->", color="#0072B2", lw=1.5))
    ax.text(113, 3.5, "+31\nper\nmaterial", fontsize=7.0, color="#0072B2",
            ha='left', va='center', fontstyle='italic')

    # D(n) equation — positioned in Panel B whitespace using axes coordinates
    # (Edison R12: y=-0.85 overlapped subtitle; use axes transform to place above bars)
    ax.text(0.55, -0.12,
            r"Illustrative partition:  $D(n) = D_{\mathrm{shared}} + n \cdot D_{\mathrm{material}}$"
            r"   (shared: 5, per-material: 31)",
            fontsize=7.0, color='#1D3557', ha='center', va='top',
            transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#F7FAFC",
                      edgecolor="#BCCCDC", alpha=0.9))


def create_standalone_figure():
    """Generate Panel B as a standalone figure."""
    apply_rcparams()
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300, facecolor='white')
    draw_dimensionality_scaling(ax, show_title=True)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = create_standalone_figure()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panel_b.png")
    fig.savefig(out, dpi=300, bbox_inches='tight', facecolor='white',
                pad_inches=0.15)
    print(f"Saved: {out}")
    plt.close(fig)
