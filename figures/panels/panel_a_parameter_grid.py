"""
Panel A: LPBF Parameter Taxonomy — Tile Grid
=============================================
Each of 36 LPBF parameters shown as a labeled tile, organized by category rows,
color-coded by optimization prevalence. Replaces the previous sunburst for
improved readability and immediate parameter countability.

Design targets 6.5–7.5" final width per Edison Scientific feedback (iter 1):
- All labels ≥9pt at print scale
- Tile gaps ≥20% of tile width (Gestalt proximity, Ware 2012)
- WCAG AA contrast ratios on all text
- Prominent "36" count badge at full opacity

Can be run standalone: python panel_a_parameter_grid.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from shared import (
    apply_rcparams, CATEGORIES, CAT_COLORS, STATUS_COLORS,
    STATUS_LABELS, TOTAL_PARAMS,
)

# Short category display names for tile grid (avoids truncation)
_CAT_SHORT = {
    "Beam / Energy": "Beam",
    "Scan Strategy": "Scan",
    "Layer / Build": "Layer",
    "Powder / Feedstock": "Powder",
    "Atmosphere": "Atmos.",
    "Thermal Mgmt": "Thermal",
    "Machine-Specific": "Machine",
}

# Short 2-line labels that fit tiles (≤8 chars per line for left-aligned layout)
_SHORT_NAMES = {
    "Spot size": "Spot\nsize",
    "Beam profile": "Beam\nprofile",
    "Wavelength": "Wave-\nlength",
    "CW / Pulsed": "CW/\nPulsed",
    "Pulse params": "Pulse\nparams",
    "Beam oscillation": "Beam\noscill.",
    "Hatch spacing": "Hatch\nspacing",
    "Scan pattern": "Scan\npattern",
    "Rotation angle": "Rotation\nangle",
    "Vector length": "Vector\nlength",
    "Contour params": "Contour\nparams",
    "Contour passes": "Contour\npasses",
    "Skywriting": "Sky-\nwriting",
    "Scan vs. gas flow": "Scan vs.\ngas flow",
    "Layer thickness": "Layer\nthick.",
    "Build orientation": "Build\norient.",
    "Support strategy": "Support\nstrategy",
    "Plate location": "Plate\nlocation",
    "Morphology": "Morpho-\nlogy",
    "Flowability": "Flowa-\nbility",
    "Packing density": "Packing\ndensity",
    "Moisture content": "Moisture\ncontent",
    "Recycling state": "Recycling\nstate",
    "Gas type": "Gas\ntype",
    "Gas flow rate": "Gas flow\nrate",
    "O\u2082 content": "O\u2082\ncontent",
    "Chamber pressure": "Chamber\npressure",
    "Baseplate preheat": "Baseplate\npreheat",
    "Inter-layer dwell": "Inter-lyr\ndwell",
    "Build height": "Build\nheight",
    "Recoater type": "Recoater\ntype",
    "Recoater speed": "Recoater\nspeed",
    "Dosing factor": "Dosing\nfactor",
    "Laser power": "Laser\npower",
    "Scan speed": "Scan\nspeed",
}


def draw_parameter_grid(ax, show_title=False):
    """Draw the parameter taxonomy as a tile grid on the given axes.

    Each category is a row with a colored background band. Parameters are
    rounded-rectangle tiles with colored left accent bars encoding
    optimization status. A bold "36" badge anchors the visual message.

    Edison iter 3 fixes: enlarged tiles + fonts (≥8pt at print), wider
    accent bars (2× for visibility), stronger row bands (18% alpha),
    differentiated red vs gold accents, consistent tile spacing.
    """
    apply_rcparams()
    ax.axis('off')

    # --- Layout constants ---
    # Iter 5 restructure: Panel A now spans full 8.5" canvas width,
    # so tiles have room. Target: 8pt labels at ~88% print (→7pt).
    # Tiles widened and gaps tightened per subloop 2 to prevent text spillover.
    tile_h = 0.88
    tile_w = 1.18           # Wider tiles for left-aligned text
    gap_x = 0.14            # Tighter gaps to compensate for wider tiles
    gap_y = 0.22
    corner_r = 0.06
    cat_header_w = 1.40     # Slightly narrower category column
    gutter = 0.15           # Fixed gutter between category label and first tile

    max_params = max(len(p) for _, _, p in CATEGORIES)
    total_width = cat_header_w + gutter + max_params * (tile_w + gap_x) + 0.3
    total_height = len(CATEGORIES) * (tile_h + gap_y)

    for row_idx, (cat_name, cat_key, params) in enumerate(reversed(CATEGORIES)):
        y = row_idx * (tile_h + gap_y)

        # Row background band — 18% alpha for print survival (was 12%)
        row_bg = mpatches.FancyBboxPatch(
            (-0.15, y - 0.05),
            total_width + 0.4, tile_h + 0.10,
            boxstyle="round,pad=0.04",
            facecolor=CAT_COLORS[cat_key], edgecolor='none',
            alpha=0.18, zorder=0,
        )
        ax.add_patch(row_bg)

        # Category color dot
        dot = plt.Circle(
            (0.15, y + tile_h / 2), 0.15,
            facecolor=CAT_COLORS[cat_key], edgecolor='white',
            linewidth=0.8, alpha=0.9, zorder=1,
        )
        ax.add_patch(dot)

        # Category label — strict left alignment, short name to avoid truncation
        display_cat = _CAT_SHORT.get(cat_name, cat_name)
        ax.text(
            0.38, y + tile_h / 2 + 0.08, display_cat,
            ha='left', va='center', fontsize=9, fontweight='bold',
            color='#1D3557',
        )
        # Count badge
        ax.text(
            0.38, y + tile_h / 2 - 0.20,
            f"{len(params)} params",
            ha='left', va='center', fontsize=7.0, color='#627D98',
            fontstyle='italic',
        )

        for col_idx, (param_name, status) in enumerate(params):
            x = cat_header_w + gutter + col_idx * (tile_w + gap_x)

            is_neglected = (status == 'neglected')

            # Light tile body for guaranteed WCAG AA text contrast
            if is_neglected:
                tile_fc = '#E8F0FE'   # Very light blue
            elif status == 'optimized':
                tile_fc = '#FFE8E8'   # Very light red (was peach)
            elif status == 'selective':
                tile_fc = '#FFF8E6'   # Very light amber
            else:
                tile_fc = '#F0F2F5'   # Neutral light gray

            ec = '#B0BEC5'
            lw = 0.6

            tile = mpatches.FancyBboxPatch(
                (x, y), tile_w, tile_h,
                boxstyle=f"round,pad={corner_r}",
                facecolor=tile_fc, edgecolor=ec, linewidth=lw,
                alpha=1.0, zorder=2,
            )
            if is_neglected:
                tile.set_hatch('////')
            ax.add_patch(tile)

            # Colored left accent border — 0.13 data units ≈ 1.4mm at print
            # (doubled from 0.07 per Edison iter 3: "0.7mm at print too thin")
            accent_w = 0.13
            accent = mpatches.FancyBboxPatch(
                (x - 0.01, y + 0.06), accent_w, tile_h - 0.12,
                boxstyle="round,pad=0.02",
                facecolor=STATUS_COLORS[status],
                edgecolor='#33333320' if status == 'fixed' else 'none',
                linewidth=0.4 if status == 'fixed' else 0,
                alpha=1.0, zorder=3,
            )
            ax.add_patch(accent)

            # Parameter label — left-aligned per Doumont (Trees, Maps, Theorems)
            # Position just right of accent bar for clean visual hierarchy
            # Font reduced to 7.5pt for 2-line / 8pt for 1-line to fit within tiles
            display_name = _SHORT_NAMES.get(param_name, param_name)
            text_color = '#1D3557'
            fontw = 'bold' if status in ('optimized', 'neglected') else 'medium'
            fs = 7.5 if '\n' in display_name else 8.0

            text_x = x + accent_w + 0.08  # Left edge after accent bar + pad
            ax.text(
                text_x, y + tile_h / 2,
                display_name, ha='left', va='center',
                fontsize=fs, fontweight=fontw, color=text_color,
                zorder=4, linespacing=0.95,
            )

    # "36 parameters" badge — positioned in whitespace right of Machine row
    # (Machine row has only 3 tiles, leaving ample empty space)
    # Shifted per Edison iter 8, Issue 2 to avoid tile/legend overlap
    machine_row_y = 0 * (tile_h + gap_y)  # Machine is first row (reversed order)
    badge_x = cat_header_w + gutter + 4 * (tile_w + gap_x)  # After ~4 tiles
    badge_y = machine_row_y + tile_h / 2 + 0.15
    ax.text(
        badge_x, badge_y, str(TOTAL_PARAMS),
        ha='left', va='center', fontsize=24, fontweight='bold',
        color='#C92A2A', alpha=0.65, zorder=5,
    )
    ax.text(
        badge_x, badge_y - 0.40, "parameters",
        ha='left', va='center', fontsize=8, color='#627D98',
        fontweight='medium', zorder=5,
    )

    ax.set_xlim(-0.3, total_width + 0.7)
    ax.set_ylim(-0.3, total_height + 0.8)


def create_standalone_figure():
    """Generate Panel A as a standalone figure."""
    apply_rcparams()
    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=300, facecolor='white')
    draw_parameter_grid(ax, show_title=True)

    # Add legend
    handles = [
        mpatches.Patch(facecolor=STATUS_COLORS[k], edgecolor='#B0BEC5',
                       label=f"{STATUS_LABELS[k]} ({_count_status(k)})",
                       hatch='////' if k == 'neglected' else None)
        for k in ['optimized', 'selective', 'fixed', 'neglected']
    ]
    fig.legend(
        handles=handles, loc='lower center', ncol=4,
        fontsize=8, frameon=True, fancybox=True,
        edgecolor='#BCCCDC', facecolor='white',
        bbox_to_anchor=(0.5, -0.02),
        title="Optimization prevalence", title_fontsize=8,
    )

    fig.tight_layout(rect=[0, 0.06, 1, 1])
    return fig


def _count_status(status):
    """Count parameters with the given optimization status."""
    return sum(
        1 for _, _, params in CATEGORIES
        for _, s in params if s == status
    )


if __name__ == "__main__":
    fig = create_standalone_figure()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panel_a.png")
    fig.savefig(out, dpi=300, bbox_inches='tight', facecolor='white',
                pad_inches=0.15)
    print(f"Saved: {out}")
    plt.close(fig)
