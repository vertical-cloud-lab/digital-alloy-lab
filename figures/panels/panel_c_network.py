"""
Panel C: Parameter Interaction Network
=======================================
Qualitative coupling map showing cross-category parameter interactions
with labeled edges (VED, spread, plume, ΔT) and VED insufficiency callout.

Can be run standalone: python panel_c_network.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared import apply_rcparams, CAT_COLORS


def draw_interaction_network(ax, show_title=False):
    """Qualitative coupling map with labeled key edges and path-effect contrast."""
    apply_rcparams()
    # Wider bounds to prevent node/callout clipping
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.6, 3.6)
    ax.axis('off')

    if show_title:
        ax.set_title(
            "Cross-category couplings make 1D surrogates\n"
            "like VED insufficient",
            fontsize=10, fontweight='bold', color='#1D3557', pad=8,
        )

    nodes = {
        "Laser\npower":       (0.4, 3.0, "beam"),
        "Scan\nspeed":        (1.8, 3.0, "beam"),
        "Spot\nsize":         (3.2, 3.0, "beam"),
        "Hatch\nspacing":     (0.4, 1.8, "scan"),
        "Layer\nthick.":      (1.8, 1.8, "layer"),
        "Beam\nprofile":      (3.2, 1.8, "beam"),
        "PSD":                (0.4, 0.5, "powder"),
        "Gas\nflow":          (1.8, 0.5, "atmosphere"),
        "Preheat\ntemp":      (3.2, 0.5, "thermal"),
        "Recoater":           (4.0, 1.2, "machine"),
    }

    edges = [
        ("Laser\npower", "Scan\nspeed", "VED", 2.5),
        ("Laser\npower", "Spot\nsize", "", 1.5),
        ("Laser\npower", "Hatch\nspacing", "VED", 1.8),
        ("Scan\nspeed", "Hatch\nspacing", "", 1.5),
        ("Hatch\nspacing", "Layer\nthick.", "VED", 1.8),
        ("Laser\npower", "Layer\nthick.", "", 1.5),
        ("Spot\nsize", "Beam\nprofile", "", 1.0),
        ("Layer\nthick.", "PSD", "spread", 1.5),
        ("PSD", "Recoater", "", 1.0),
        ("Gas\nflow", "Scan\nspeed", "plume", 1.0),
        ("Preheat\ntemp", "Laser\npower", "\u0394T", 1.0),
        ("Preheat\ntemp", "Layer\nthick.", "", 0.8),
        ("Gas\nflow", "Hatch\nspacing", "", 0.8),
    ]

    # Draw edges
    for n1, n2, elabel, lw in edges:
        x1, y1, _ = nodes[n1]
        x2, y2, _ = nodes[n2]
        alpha = min(0.15 + lw * 0.12, 0.55)
        ax.plot([x1, x2], [y1, y2], '-', color='#627D98',
                lw=lw * 0.7, alpha=alpha, zorder=1)
        if elabel:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my + 0.12, elabel, ha='center', va='center',
                    fontsize=7.0, color='#486581', fontstyle='italic',
                    path_effects=[pe.withStroke(linewidth=2.5,
                                               foreground='white')])

    # Draw nodes — larger for label readability (iter 6 fix #3)
    # Edison R12: all nodes use dark text + white stroke for universal WCAG AA compliance
    # (white mask removed — it was defeating contrast on dark nodes)
    for label, (x, y, cat) in nodes.items():
        color = CAT_COLORS[cat]
        circle = plt.Circle((x, y), 0.35, facecolor=color, edgecolor='white',
                             linewidth=1.8, alpha=0.88, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=7.5,
                color='#1D3557', fontweight='bold', zorder=3, linespacing=0.9,
                path_effects=[pe.withStroke(linewidth=3.0, foreground='white',
                                           alpha=0.85)])

    # VED callout — repositioned to avoid Spot size node overlap
    # (was at xytext=(3.6, 2.65) which overlapped Spot size at (3.2, 3.0))
    ax.annotate(
        "VED = P/(v\u00b7h\u00b7t)\ncollapses 4D \u2192 1D\n"
        "Same VED \u2260 same outcome",
        xy=(1.1, 2.4), xytext=(4.2, 2.35),
        fontsize=7.0, color='#B84D00', fontstyle='italic',
        fontweight='medium',
        arrowprops=dict(arrowstyle='->', color='#B84D00', lw=0.9),
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF7ED',
                  edgecolor='#B84D00', alpha=0.85))

    # Qualitative note — positioned near Recoater node area
    ax.text(4.8, -0.35, "Schematic coupling map;\nedge weight is qualitative",
            fontsize=7.0, color='#6B859B', ha='right', va='center',
            fontstyle='italic')


def create_standalone_figure():
    """Generate Panel C as a standalone figure."""
    apply_rcparams()
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300, facecolor='white')
    draw_interaction_network(ax, show_title=True)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = create_standalone_figure()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panel_c.png")
    fig.savefig(out, dpi=300, bbox_inches='tight', facecolor='white',
                pad_inches=0.15)
    print(f"Saved: {out}")
    plt.close(fig)
