#!/usr/bin/env python3
"""
Schematic illustrations of standard metal AM validation test structures.

Creates a labeled figure showing representative geometries for each stage
of the LPBF validation progression: single tracks → thin walls → density cubes
→ tensile bars → geometric benchmark artifact → build plate layout.

Author: Generated programmatically for FLAIME proposal (DOE Genesis Mission Topic 3B)
Refined with 7 rounds of Edison Scientific ANALYSIS feedback (R1: B+/A- → R7: A grade).
Improvements: global color legend, XYZ triad, flow arrows, standardized dims, color-diff orientations.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc
import numpy as np

# Systematic color scheme: one color per validation stage (ColorBrewer Set2)
SC = {
    1: '#66C2A5',  # Stage 1: Single tracks - teal
    2: '#FC8D62',  # Stage 2: Thin walls - orange
    3: '#8DA0CB',  # Stage 3-4: Density cubes/DoE - periwinkle
    5: '#E78AC3',  # Stage 5: Tensile bars - pink
    6: '#A6D854',  # Stage 6: Geometric artifact - lime green
    'L': '#FFD92F',  # Build plate layout - gold
}
# Dark accent per stage
SD = {1: '#3A8A75', 2: '#C06030', 3: '#5A6EA0', 5: '#B0609A', 6: '#6A8830', 'L': '#B09820'}
# Orientation colors for tensile bars
OC = {'XY': '#4477AA', 'XZ': '#EE6677', '45': '#CCBB44'}

C = {
    'sub': '#C0C0C0', 'melt': '#EE6677', 'laser': '#CCBB44',
    'crack': '#CC3366', 'flow': '#228833', 'dim': '#444444',
    'bg': ['#F0FAF7', '#FFF5EE', '#F0F3FA', '#FFF0F8', '#F5FAF0', '#FFFBE6'],
}


def draw_single_tracks(ax, commentary=True):
    """Stage 1: Single tracks on substrate with melt pool cross-section."""
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-3, 5)
    ax.set_aspect('equal')

    # Substrate
    ax.add_patch(mpatches.Rectangle((-0.5, -2.5), 11, 2.5, color=C['sub'], ec='#888', lw=1))
    ax.text(5, -1.8, 'Substrate', ha='center', fontsize=9, color='#555')

    # 5 single tracks
    labels = ['Stable', 'Wide\n(keyhole)', 'Narrow', 'Stable', 'Balling']
    widths = [0.6, 0.8, 0.35, 0.55, 0.4]
    heights = [0.45, 0.6, 0.3, 0.5, 0.25]
    depths = [0.5, 0.9, 0.3, 0.45, 0.3]

    for i, (lbl, w, h, d) in enumerate(zip(labels, widths, heights, depths)):
        x = 1 + i * 2
        theta = np.linspace(0, np.pi, 50)
        ax.fill(x + w * np.cos(theta), h * np.sin(theta), color=SC[1], ec=SD[1], lw=1.2, zorder=3)
        pt = np.linspace(np.pi, 2 * np.pi, 50)
        ax.fill(x + w * 0.8 * np.cos(pt), d * np.sin(pt), color=C['melt'], alpha=0.25, zorder=2)
        ax.plot(x + w * 0.8 * np.cos(pt), d * np.sin(pt), color=C['melt'], lw=0.8, ls='--', zorder=2)
        if lbl == 'Balling':
            for bx in [x - 0.3, x + 0.3]:
                ax.add_patch(plt.Circle((bx, 0.12), 0.12, color=SC[1], ec=SD[1], lw=0.8, zorder=4))
        ax.text(x, -0.6, lbl, ha='center', fontsize=6.5, color='#555')

    # Laser
    ax.annotate('', xy=(5, 0.6), xytext=(5, 3.8), arrowprops=dict(arrowstyle='->', color=C['laser'], lw=3))
    ax.text(5, 4.2, 'Laser beam', ha='center', fontsize=9, color='#886600', fontweight='bold')

    # Dimension: W
    ax.annotate('', xy=(0.4, 0), xytext=(1.6, 0), arrowprops=dict(arrowstyle='<->', color=C['dim'], lw=1))
    ax.text(1.0, 0.2, 'W', ha='center', fontsize=9, fontweight='bold', fontstyle='italic', color=C['dim'])
    # Dimension: D
    ax.annotate('', xy=(2.6, 0), xytext=(2.6, -0.9), arrowprops=dict(arrowstyle='<->', color=C['dim'], lw=1))
    ax.text(2.3, -0.45, 'D', ha='right', fontsize=9, fontweight='bold', fontstyle='italic', color=C['dim'])

    if commentary:
        ax.text(5, -2.8, 'Bead width ~0.1–0.3 mm  |  Screen: balling, keyholing, LOF',
                ha='center', fontsize=7.5, color='#666', fontstyle='italic')

    # Sub-legend for melt pool color
    ax.add_patch(mpatches.Rectangle((8, 3.5), 0.4, 0.25, color=C['melt'], alpha=0.4, ec=C['melt'], lw=0.8))
    ax.text(8.6, 3.6, 'Melt pool', fontsize=6.5, va='center', color=C['melt'])

    ax.axis('off')


def draw_thin_walls(ax, commentary=True):
    """Stage 2: Thin walls for crack screening."""
    ax.set_xlim(-1, 11)
    ax.set_ylim(-2.5, 8.5)
    ax.set_aspect('equal')

    ax.add_patch(mpatches.Rectangle((-0.5, -1), 11, 1, color=C['sub'], ec='#888', lw=1))
    ax.text(5, -0.7, 'Base Plate', ha='center', fontsize=7, color='#555')

    # Wall 1 - vertical
    ax.add_patch(mpatches.Rectangle((1.5, 0), 0.5, 6, color=SC[2], ec=SD[2], lw=1.2, zorder=3))
    for y in np.arange(0.25, 6, 0.25):
        ax.plot([1.5, 2.0], [y, y], color='white', lw=0.3, alpha=0.5, zorder=4)
    ax.text(1.75, 6.5, 'XZ plane', ha='center', fontsize=8, fontweight='bold', color=SD[2])

    # Wall 2 - angled overhang
    pts = np.array([[5, 0], [5.5, 0],
                    [5.5 + 4 * np.sin(np.radians(20)), 4 * np.cos(np.radians(20))],
                    [5 + 4 * np.sin(np.radians(20)), 4 * np.cos(np.radians(20))]])
    ax.add_patch(plt.Polygon(pts, color=SC[2], ec=SD[2], lw=1.2, zorder=3))
    ax.text(6.2, 5.2, '20° overhang', ha='center', fontsize=7, fontweight='bold', color=SD[2])

    # Wall 3 - with hot crack
    ax.add_patch(mpatches.Rectangle((8.5, 0), 0.5, 6, color=SC[2], ec=SD[2], lw=1.2, zorder=3))
    cy = np.linspace(1.5, 4.5, 30)
    cx = 8.75 + 0.15 * np.sin(cy * 5)
    ax.plot(cx, cy, color=C['crack'], lw=2.5, zorder=5)
    if commentary:
        ax.annotate('Hot crack\n(2xxx/7xxx Al)', xy=(8.8, 3), xytext=(6.2, 7),
                    fontsize=8, color=C['crack'], fontweight='bold', ha='center',
                    arrowprops=dict(arrowstyle='->', color=C['crack'], lw=1.2))

    # Dimensions
    ax.annotate('', xy=(0.5, 0), xytext=(0.5, 6),
                arrowprops=dict(arrowstyle='<->', color=C['dim'], lw=1))
    ax.text(0, 3, '5–10\nmm', ha='right', fontsize=7.5, color=C['dim'])
    ax.annotate('', xy=(1.5, -0.3), xytext=(2.0, -0.3),
                arrowprops=dict(arrowstyle='<->', color=C['dim'], lw=0.8))
    ax.text(1.75, -0.7, '~0.5 mm', ha='center', fontsize=6.5, color=C['dim'])

    if commentary:
        ax.text(5, -2.2, 'Crack screening critical for high-strength Al  |  2–3 walls per orientation',
                ha='center', fontsize=7.5, color='#666', fontstyle='italic')
    ax.axis('off')


def draw_density_cubes(ax, commentary=True):
    """Stage 3-4: Density cubes / DoE parameter matrix."""
    ax.set_xlim(-2.5, 11)
    ax.set_ylim(-2.5, 8.5)
    ax.set_aspect('equal')

    def draw_cube(cx, cy, s, shade=1.0):
        rgb = np.array(plt.matplotlib.colors.to_rgb(SC[3]))
        ax.add_patch(mpatches.Rectangle((cx, cy), s, s, color=rgb * shade, ec=SD[3], lw=1, zorder=3))
        off = s * 0.3
        ax.fill([cx, cx + s, cx + s + off, cx + off],
                [cy + s, cy + s, cy + s + off * 0.6, cy + s + off * 0.6],
                color=rgb * shade * 0.9, ec=SD[3], lw=1, zorder=4)
        ax.fill([cx + s, cx + s + off, cx + s + off, cx + s],
                [cy, cy + off * 0.6, cy + s + off * 0.6, cy + s],
                color=rgb * shade * 0.75, ec=SD[3], lw=1, zorder=4)
        # Pores
        np.random.seed(int(cx * 10 + cy))
        for _ in range(3):
            px = cx + np.random.uniform(0.2 * s, 0.8 * s)
            py = cy + np.random.uniform(0.2 * s, 0.8 * s)
            ax.add_patch(plt.Circle((px, py), s * 0.04, color='white', ec='#888', lw=0.5, zorder=5))

    # 3×2 grid
    for i in range(3):
        for j in range(2):
            draw_cube(0.5 + i * 3.2, 0.5 + j * 3.5, 2.2, shade=0.85 + i * 0.05 + j * 0.03)

    # Axis labels
    for i, lbl in enumerate(['200 W', '250 W', '300 W']):
        ax.text(1.6 + i * 3.2, -0.5, lbl, ha='center', fontsize=7.5, color=SD[3], fontweight='bold')
    for j, lbl in enumerate(['800\nmm/s', '1000\nmm/s']):
        ax.text(-1.0, 1.6 + j * 3.5, lbl, ha='center', fontsize=7, color=SD[3])

    ax.annotate('', xy=(9.5, -0.5), xytext=(0.5, -0.5),
                arrowprops=dict(arrowstyle='->', color=SD[3], lw=1))
    ax.text(5, -1.2, 'Laser Power →', ha='center', fontsize=7.5, color=SD[3])
    ax.annotate('', xy=(-1.3, 7.5), xytext=(-1.3, 0.5),
                arrowprops=dict(arrowstyle='->', color=SD[3], lw=1))

    # Cube dimension
    ax.annotate('', xy=(0.5, 0.5), xytext=(2.7, 0.5),
                arrowprops=dict(arrowstyle='<->', color=C['dim'], lw=0.8))
    ax.text(1.6, 0.1, '~10 mm', ha='center', fontsize=7, color=C['dim'])

    if commentary:
        ax.text(5, -2.0, 'Archimedes density ≥99.5%  |  DoE: Power × Speed × Hatch',
                ha='center', fontsize=7.5, color='#666', fontstyle='italic')
    ax.axis('off')


def draw_tensile_bars(ax, commentary=True):
    """Stage 5: Three tensile bars on a single LPBF build plate, shown
    in isometric view with three distinct print orientations (XY flat,
    XZ upright, 45° tilted) — emphasizing that all orientations are
    printed in parallel on a single build plate, not stacked along Z."""
    ax.set_xlim(-3.5, 14.0)
    ax.set_ylim(-3.5, 8.5)
    ax.set_aspect('equal')

    # --- Isometric helpers (flat top-down plate -> 2D screen coords) ---
    # Plate XY are mapped via a simple oblique projection; Z is straight up.
    KX = np.array([1.0, 0.0])           # plate-X -> screen
    KY = np.array([0.55, 0.32])         # plate-Y -> screen (oblique)
    KZ = np.array([0.0, 1.0])           # build-Z -> screen

    def iso(p):  # p = (x_plate, y_plate, z)
        s = p[0] * KX + p[1] * KY + p[2] * KZ
        return s

    def poly(verts, **kw):
        pts = np.array([iso(v) for v in verts])
        ax.fill(pts[:, 0], pts[:, 1], **kw)

    # --- Build plate (250×250 mm, drawn as 8×8 plate units) ---
    PX0, PY0 = 0.0, 0.0
    PSZ = 8.0
    PT = 0.5  # plate thickness (visible side)

    # Plate top (powder bed surface)
    plate_top = [
        (PX0,        PY0,        0),
        (PX0 + PSZ,  PY0,        0),
        (PX0 + PSZ,  PY0 + PSZ,  0),
        (PX0,        PY0 + PSZ,  0),
    ]
    poly(plate_top, color='#ece9e1', ec='#9d9683', lw=1.0, zorder=2)

    # Subtle powder texture (faint dots)
    rng = np.random.default_rng(0)
    for _ in range(180):
        px = PX0 + rng.uniform(0.05, PSZ - 0.05)
        py = PY0 + rng.uniform(0.05, PSZ - 0.05)
        sx, sy = iso((px, py, 0))
        ax.plot(sx, sy, marker='.', markersize=0.8,
                color='#b8b09b', zorder=2.1)

    # Plate front-side (thickness panel)
    front = [
        (PX0,        PY0, 0),
        (PX0 + PSZ,  PY0, 0),
        (PX0 + PSZ,  PY0, -PT),
        (PX0,        PY0, -PT),
    ]
    poly(front, color='#cbc6b6', ec='#7a755f', lw=0.8, zorder=2)

    # Plate right-side
    rside = [
        (PX0 + PSZ, PY0,        0),
        (PX0 + PSZ, PY0 + PSZ,  0),
        (PX0 + PSZ, PY0 + PSZ,  -PT),
        (PX0 + PSZ, PY0,        -PT),
    ]
    poly(rside, color='#b6b09e', ec='#7a755f', lw=0.8, zorder=2)

    # --- Dogbone footprint (top-down outline used for XY-flat bars) ---
    def dogbone_outline(scale=1.0):
        gw, guw = 1.1 * scale, 0.45 * scale
        gl, sl, gul = 1.2 * scale, 0.6 * scale, 2.2 * scale
        tl = 2 * gl + 2 * sl + gul
        x = [0, gl, gl + sl, gl + sl + gul, gl + 2 * sl + gul, tl,
             tl, gl + 2 * sl + gul, gl + sl + gul, gl + sl, gl, 0]
        y = [-gw/2, -gw/2, -guw/2, -guw/2, -gw/2, -gw/2,
             gw/2, gw/2, guw/2, guw/2, gw/2, gw/2]
        return np.array([x, y]) - np.array([[tl/2], [0]])

    def place_xy(cx, cy, angle_deg=0, scale=0.5,
                 color=OC['XY'], ec='#224466', z=4):
        """XY-flat dogbone lying on plate; rotates in plate-XY."""
        outline = dogbone_outline(scale=scale)
        rad = np.radians(angle_deg)
        rot = np.array([[np.cos(rad), -np.sin(rad)],
                        [np.sin(rad), np.cos(rad)]])
        outline = rot @ outline
        verts = [(cx + ox, cy + oy, 0.05) for ox, oy in zip(outline[0], outline[1])]
        poly(verts, color=color, ec=ec, lw=1.2, zorder=z)

    def place_upright(cx, cy, color=OC['XZ'], ec='#AA3344', z=5):
        """XZ-upright bar: standing on the plate, gauge axis along Z."""
        bx, by, bz = 0.5, 0.8, 0
        slab_top = [
            (cx - bx/2, cy - by/2, 2.6),
            (cx + bx/2, cy - by/2, 2.6),
            (cx + bx/2, cy + by/2, 2.6),
            (cx - bx/2, cy + by/2, 2.6),
        ]
        front_face = [
            (cx - bx/2, cy - by/2, 0),
            (cx + bx/2, cy - by/2, 0),
            (cx + bx/2, cy - by/2, 2.6),
            (cx - bx/2, cy - by/2, 2.6),
        ]
        right_face = [
            (cx + bx/2, cy - by/2, 0),
            (cx + bx/2, cy + by/2, 0),
            (cx + bx/2, cy + by/2, 2.6),
            (cx + bx/2, cy - by/2, 2.6),
        ]
        from matplotlib.colors import to_rgb
        base = np.array(to_rgb(color))
        def tint(f):
            return tuple(np.clip(base * f + (1 - f), 0, 1))
        poly(front_face, color=tint(0.65), ec=ec, lw=1.0, zorder=z)
        poly(right_face, color=tint(0.80), ec=ec, lw=1.0, zorder=z)
        poly(slab_top,   color=tint(0.95), ec=ec, lw=1.0, zorder=z)
        # Dogbone silhouette painted onto front face (gauge axis vertical)
        outline = dogbone_outline(scale=0.45)
        outline = np.array([[0, -1], [1, 0]]) @ outline
        sx0, sy0 = iso((cx, cy - by/2, 1.3))
        pts = np.array([[sx0 + ox*0.7 for ox in outline[0]],
                        [sy0 + oy*0.7 for oy in outline[1]]])
        ax.fill(pts[0], pts[1], color=color, ec=ec, lw=0.6, zorder=z + 0.3)

    def place_45(cx, cy, scale=0.55, color=OC['45'], ec='#998833', z=5):
        """45° tilted bar (gauge axis 45° in plate-X / Z plane)."""
        outline = dogbone_outline(scale=scale)
        rad = np.radians(45)
        rot = np.array([[np.cos(rad), -np.sin(rad)],
                        [np.sin(rad), np.cos(rad)]])
        outline = rot @ outline
        from matplotlib.colors import to_rgb
        base = np.array(to_rgb(color))
        def tint(f):
            return tuple(np.clip(base * f + (1 - f), 0, 1))
        verts_front = []
        verts_back = []
        for ox, oy in zip(outline[0], outline[1]):
            verts_front.append((cx + ox, cy - 0.14, 0.05 + max(0, oy + 0.7)))
            verts_back.append((cx + ox,  cy + 0.14, 0.05 + max(0, oy + 0.7)))
        poly(verts_back, color=tint(0.85), ec=ec, lw=0.8, zorder=z)
        poly(verts_front, color=tint(0.65), ec=ec, lw=1.0, zorder=z + 0.2)
        # Small support stub under low end
        sx, sy = cx - scale * 1.4, cy
        stub = [
            (sx - 0.20, sy - 0.18, 0),
            (sx + 0.20, sy - 0.18, 0),
            (sx + 0.20, sy + 0.18, 0),
            (sx - 0.20, sy + 0.18, 0),
        ]
        poly(stub, color='#888', ec='#444', lw=0.5, zorder=z - 0.1)

    # --- Place the three bars side-by-side on the plate (no overlap) ---
    # Use distinct plate positions so screen-space iso projections do not collide.
    place_xy(2.0, 1.5, angle_deg=0, scale=0.5, color=OC['XY'])  # front-left
    place_upright(6.0, 1.5, color=OC['XZ'])                      # front-right
    place_45(2.0, 5.5, scale=0.55, color=OC['45'])               # back-left

    # --- Build direction Z arrow (out of plate, upper-left corner) ---
    az0 = iso((PX0 - 0.4, PY0 + PSZ + 0.3, 0))
    az1 = iso((PX0 - 0.4, PY0 + PSZ + 0.3, 3.2))
    ax.annotate('', xy=az1, xytext=az0,
                arrowprops=dict(arrowstyle='-|>', color=C['flow'],
                                lw=2.6, mutation_scale=18))
    ax.text(az1[0] - 0.2, az1[1] + 0.1, 'Build\ndir. (Z)',
            fontsize=9, ha='right', va='center',
            fontweight='bold', color=C['flow'])

    # --- XYZ triad (front-right corner, in plate's local frame) ---
    tx, ty = PX0 + PSZ + 0.4, PY0 - 0.5
    for vec, lbl, col in [
        ((1.2, 0, 0), 'X', '#333'),
        ((0, 1.2, 0), 'Y', '#333'),
        ((0, 0, 1.2), 'Z', '#333'),
    ]:
        a0 = iso((tx, ty, 0))
        a1 = iso((tx + vec[0], ty + vec[1], vec[2]))
        ax.annotate('', xy=a1, xytext=a0,
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.3))
        ax.text(a1[0] + 0.08 * np.sign(a1[0] - a0[0] + 1e-3),
                a1[1] + 0.10, lbl,
                fontsize=8, fontweight='bold', color=col, ha='center')

    # --- Right-margin labels ---
    LABEL_X = 11.0
    LABEL_FS = 12
    ax.text(LABEL_X, 6.5, 'XY (flat)',     fontsize=LABEL_FS,
            color=OC['XY'], fontweight='bold', va='center')
    ax.text(LABEL_X, 4.5, '45°',            fontsize=LABEL_FS,
            color=OC['45'], fontweight='bold', va='center')
    ax.text(LABEL_X, 2.5, 'XZ (upright)',  fontsize=LABEL_FS,
            color=OC['XZ'], fontweight='bold', va='center')

    if commentary:
        ax.text(5, -3.0,
                'All three orientations on one build plate (parallel, not stacked)\n'
                'YS, UTS, elongation by build orientation  |  ASTM E8/E8M sub-size',
                ha='center', fontsize=7.5, color='#666', fontstyle='italic')
    ax.axis('off')


def draw_geometric_artifact(ax, commentary=True):
    """Stage 6: ISO/ASTM 52902 geometric benchmark artifact."""
    ax.set_xlim(-1.5, 11.5)
    ax.set_ylim(-2.5, 8.5)
    ax.set_aspect('equal')

    # Base
    ax.add_patch(mpatches.Rectangle((0.5, 0), 9, 1.2, color=SC[6], ec=SD[6], lw=1.2, zorder=3))

    # Pin
    ax.fill_between([1.5, 2.3], 1.2, 4.5, color=SC[6], ec=SD[6], lw=1, zorder=4)
    t = np.linspace(0, 2 * np.pi, 50)
    ax.fill(1.9 + 0.4 * np.cos(t), 4.5 + 0.12 * np.sin(t),
            color=np.array(plt.matplotlib.colors.to_rgb(SC[6])) * 0.9, ec=SD[6], lw=0.8, zorder=5)
    ax.text(1.9, 2.8, 'Pin\nØ0.8 mm', ha='center', fontsize=7, color='white', fontweight='bold', zorder=6)

    # Z-steps
    for i, h in enumerate([1.2, 1.8, 2.4, 3.0, 3.6, 4.2]):
        ax.add_patch(mpatches.Rectangle((3.2 + i * 0.6, 1.2), 0.6, h - 1.2,
                                         color=SC[6], ec=SD[6], lw=0.6, zorder=4))
    ax.text(4.7, 4.8, 'Z-steps\n(0.5 mm each)', ha='center', fontsize=7, color=SD[6], fontweight='bold')

    # Overhang
    ax.fill([6.5, 8, 8, 7.5, 6.5], [1.2, 1.2, 4.5, 4.5, 3], color=SC[6], ec=SD[6], lw=1, zorder=4)
    ax.add_patch(Arc((6.5, 1.2), 1.6, 1.6, angle=0, theta1=0, theta2=68, color=C['crack'], lw=1.2))
    ax.text(7.4, 2.0, '45°\noverhang', fontsize=7, color=C['crack'], fontweight='bold')

    # Hole
    ax.add_patch(mpatches.Rectangle((8.5, 1.2), 1.2, 3, color=SC[6], ec=SD[6], lw=0.8, zorder=4))
    ax.add_patch(plt.Circle((9.1, 2.7), 0.35, color=C['sub'], ec='#555', lw=1, zorder=5))
    ax.text(9.1, 4.5, 'Hole\nØ0.7 mm', ha='center', fontsize=7, color=SD[6], fontweight='bold')

    # Overall dim
    ax.annotate('', xy=(0.5, 5.5), xytext=(9.5, 5.5),
                arrowprops=dict(arrowstyle='<->', color=C['dim'], lw=1))
    ax.text(5, 5.9, '~100 mm', ha='center', fontsize=8, color=C['dim'], fontweight='bold')
    ax.annotate('', xy=(0, 0), xytext=(0, 4.5),
                arrowprops=dict(arrowstyle='<->', color=C['dim'], lw=0.8))
    ax.text(-0.5, 2.2, '~30\nmm', ha='center', fontsize=7, color=C['dim'])

    if commentary:
        ax.text(5, -1.8, 'CMM / 3D scan → RMSE <25 µm  |  Pins, holes, overhangs, Z-steps',
                ha='center', fontsize=7.5, color='#666', fontstyle='italic')
    ax.axis('off')


def draw_build_plate(ax):
    """Overview build plate layout."""
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-1.5, 11.5)
    ax.set_aspect('equal')

    ax.add_patch(mpatches.Rectangle((0, 0), 10, 10, color='#F0F0F0', ec='#333', lw=2.5))

    # Tracks
    for i in range(5):
        ax.plot([0.5, 3.5], [0.6 + i * 0.35, 0.6 + i * 0.35], color=SC[1], lw=2.5, zorder=3)
    ax.text(2, 2.6, 'Tracks (5)', ha='center', fontsize=7.5, color=SD[1], fontweight='bold')

    # Walls
    for i in range(3):
        ax.add_patch(mpatches.Rectangle((0.5 + i * 1.2, 3.2), 0.15, 2.2,
                                         color=SC[2], ec=SD[2], lw=0.8, zorder=3))
    ax.text(2, 5.7, 'Walls (3)', ha='center', fontsize=7.5, color=SD[2], fontweight='bold')

    # Cubes
    for i in range(3):
        for j in range(3):
            ax.add_patch(mpatches.Rectangle((0.3 + i * 1.1, 6.5 + j * 1.1), 0.8, 0.8,
                                             color=SC[3], ec=SD[3], lw=0.8, zorder=3))
    ax.text(2, 6.0, 'Cubes (9)', ha='center', fontsize=7.5, color=SD[3], fontweight='bold')

    # Tensile bars
    for i in range(3):
        gy = 7.5 + i * 0.8
        ax.add_patch(mpatches.Rectangle((4.5, gy - 0.15), 0.6, 0.3, color=SC[5], ec=SD[5], lw=0.6, zorder=3))
        ax.add_patch(mpatches.Rectangle((5.1, gy - 0.08), 2.2, 0.16, color=SC[5], ec=SD[5], lw=0.6, zorder=3))
        ax.add_patch(mpatches.Rectangle((7.3, gy - 0.15), 0.6, 0.3, color=SC[5], ec=SD[5], lw=0.6, zorder=3))
    ax.text(6.2, 7.0, 'Tensile (3)', ha='center', fontsize=7.5, color=SD[5], fontweight='bold')

    # Artifact
    ax.add_patch(mpatches.Rectangle((4.5, 1), 5, 4.5, color=SC[6], ec=SD[6], lw=1.2, zorder=3, alpha=0.7))
    ax.add_patch(plt.Circle((6, 2.5), 0.3, color='#F0F0F0', ec='#555', lw=0.6, zorder=4))
    for k in range(4):
        ax.add_patch(mpatches.Rectangle((5 + k * 0.6, 4), 0.35, 0.2 + k * 0.15,
                                         color=np.array(plt.matplotlib.colors.to_rgb(SC[6])) * 0.9,
                                         ec=SD[6], lw=0.4, zorder=4))
    ax.text(7, 5.8, 'Geometric\nartifact (1)', ha='center', fontsize=7.5, color=SD[6], fontweight='bold')

    ax.text(5, -1.2, '250 × 250 mm build plate', ha='center', fontsize=8.5, color='#555', fontstyle='italic')
    ax.text(5, 10.5, 'Total: ~21 features (typical 15–40 per composition)',
            ha='center', fontsize=8, color='#333')
    ax.axis('off')


def main():
    fig = plt.figure(figsize=(18, 13))

    # 2×3 grid
    gs = fig.add_gridspec(2, 3, hspace=0.30, wspace=0.22,
                           left=0.03, right=0.97, top=0.89, bottom=0.06)
    axes = [fig.add_subplot(gs[r, c]) for r in range(2) for c in range(3)]

    # Title
    fig.suptitle('Standard Metal AM Validation Test Structures\n'
                 'Staged Progression: Single Tracks → Production Qualification',
                 fontsize=16, fontweight='bold', y=0.97)

    # ─── GLOBAL COLOR LEGEND (top strip) ───
    legend_items = [
        (SC[1], 'Stage 1: Single tracks'),
        (SC[2], 'Stage 2: Thin walls'),
        (SC[3], 'Stage 3–4: Density cubes / DoE'),
        (SC[5], 'Stage 5: Tensile bars'),
        (SC[6], 'Stage 6: Geometric artifact'),
        (SC['L'], 'Build plate layout'),
    ]
    for i, (col, lbl) in enumerate(legend_items):
        x = 0.05 + i * 0.158
        fig.patches.append(mpatches.FancyBboxPatch(
            (x, 0.915), 0.018, 0.018, transform=fig.transFigure,
            boxstyle='round,pad=0.002', facecolor=col, edgecolor='#333', lw=1.2))
        fig.text(x + 0.023, 0.924, lbl, fontsize=9.5, va='center', color='#222', fontweight='bold')

    # Draw panels
    titles = ['Stage 1: Single Tracks', 'Stage 2: Thin Walls',
              'Stage 3–4: Density Cubes / DoE', 'Stage 5: Tensile Bars (ASTM E8)',
              'Stage 6: Geometric Artifact\n(ISO/ASTM 52902)',
              'Example Build Plate Layout\n(~40 features / composition)']
    funcs = [draw_single_tracks, draw_thin_walls, draw_density_cubes,
             draw_tensile_bars, draw_geometric_artifact, draw_build_plate]

    for i, (func, title) in enumerate(zip(funcs, titles)):
        func(axes[i])
        axes[i].set_title(title, fontsize=12, fontweight='bold', pad=8, color='#333')
        axes[i].text(-0.03, 1.10, f'({chr(97 + i)})', transform=axes[i].transAxes,
                     fontsize=14, fontweight='bold', va='top')
        axes[i].set_facecolor(C['bg'][i])

    # ─── FLOW ARROWS between panels (a→b→c→d→e→f) ───
    arrow_kw = dict(arrowstyle='->', color=C['flow'], lw=1.8,
                     connectionstyle='arc3,rad=0', mutation_scale=12)
    # Row 1: a→b, b→c
    for x in [0.335, 0.655]:
        fig.patches.append(FancyArrowPatch((x, 0.68), (x + 0.02, 0.68),
                                            transform=fig.transFigure, **arrow_kw, zorder=10))
    # c→d (wrap: right end of row 1 → left start of row 2, routed above/below)
    fig.patches.append(FancyArrowPatch(
        (0.97, 0.52), (0.04, 0.44),
        transform=fig.transFigure, arrowstyle='->', color=C['flow'], lw=1.8,
        connectionstyle='arc3,rad=-0.5', mutation_scale=12, zorder=10, alpha=0.6))
    # Row 2: d→e, e→f
    for x in [0.335, 0.655]:
        fig.patches.append(FancyArrowPatch((x, 0.28), (x + 0.02, 0.28),
                                            transform=fig.transFigure, **arrow_kw, zorder=10))

    # Citation footer
    fig.text(0.5, 0.01,
             'Schematic representations (not to scale). Standards: ISO/ASTM 52902, 52904, 52907; '
             'ASTM E8/E8M.  |  Gheysen et al. 2021 Materials & Design; '
             'Moylan et al. 2014 JRES 119.017; Brenner et al. 2025',
             ha='center', fontsize=8, color='#888', fontstyle='italic')

    plt.savefig('edison-trajectories/fig-am-test-structures-schematics.png',
                dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Saved: edison-trajectories/fig-am-test-structures-schematics.png")


if __name__ == '__main__':
    main()
