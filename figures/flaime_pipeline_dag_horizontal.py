"""Generate the FLAIME pipeline DAG figure (simulation + experimental workflow).

Structure (left-to-right DAG, no acquisition/orchestration nodes):

  Inputs (composition + LPBF process)
    -> CALPHAD partial-eval nodes (TC-Python Scheil + AM Module)
    -> AMAZEMET rePOWDER ultrasonic atomization
    -> Powder QC #1 (in-house powder)
    -> LPBF MVS ladder #1 (single tracks -> density cubes -> ISO 52902 -> ASTM E8)
    -> As-built characterization #1 (density, microstructure, hardness, tensile)
    -> Valimet distributed-validation gas-atomization scale-up (>=50 kg x 6)
    -> Powder QC #2 (scale-up powder, same QC battery as #1)
    -> LPBF MVS ladder #2 (validate scale-up powder behaves like in-house)
    -> As-built characterization #2 (same gates as #1, on scale-up powder)
    -> Qualified alloy candidate(s) -> Phase II  (dashed = future)

Routing notes:
  - Long skip arrows (e.g., LPBF process -> first MVS node) route over the top
    of the figure as elbow polylines so they don't disappear behind nodes.
  - Multiple arrows hitting the same destination are staggered along the dst
    edge (different dst_frac) so they don't overplot.
  - Multiple arrows fanning out from the same source are staggered along the
    src edge (different src_frac).
"""

from pathlib import Path as FilePath

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path

HERE = FilePath(__file__).resolve().parent
OUT_PNG = HERE / "flaime_pipeline_dag.png"
OUT_PDF = HERE / "flaime_pipeline_dag.pdf"

# Category colors (colorblind-safe Okabe-Ito palette, muted)
COLORS = {
    "input":   "#E8E8E8",  # light gray   - inputs
    "calphad": "#A6CFE5",  # pale blue    - CALPHAD partial-eval
    "atom":    "#BEE3B3",  # pale green   - atomization
    "char":    "#FFD0A8",  # pale orange  - characterization
    "lpbf":    "#E6C9E6",  # pale lavender- LPBF/MVS
    "scale":   "#D8D8D8",  # gray         - Phase II milestone
}

# Layout grid: x in [0, 28.2], y in [1.8, 7.6]; equal column stride = 3.2
# All node coords are (x, y, w, h) with (x, y) = lower-left corner.

NODES = [
    # ---- Col 0: Inputs ----
    ("inp_c", "Composition vector\n(Al + 15 elements,\nper-element bounds)",
     "input",   (0.2, 5.4), (2.0, 1.2)),
    ("inp_p", "LPBF process\n(20+ params: P, v, h,\nlayer thickness, spot,\nscan strategy, gas\nflow, plate temp, $\\ldots$)",
     "input",   (0.2, 3.0), (2.0, 1.8)),

    # ---- Col 1: CALPHAD partial-eval ----
    ("tc1",   "TC-Python + TCAl10\n$\\sim$1--5 CPU-min/eval\nScheil, freezing range,\nhot-cracking susc.",
     "calphad", (3.4, 5.2), (2.4, 1.3)),
    ("tc2",   "TC AM Module\n$\\sim$0.5--2 CPU-hr/eval\nLPBF solidification map,\ncrack susceptibility",
     "calphad", (3.4, 3.5), (2.4, 1.3)),

    # ---- Col 2: AMAZEMET + Powder QC #1 ----
    ("atom",  "AMAZEMET rePOWDER\nultrasonic atomization\n(100--1000 g, Ar)",
     "atom",    (6.6, 5.2), (2.4, 1.3)),
    ("pqc",   "Powder QC #1\nPSD (laser diff.),\nICP-MS, SEM/EDS,\nO/N analyzer",
     "char",    (6.6, 3.5), (2.4, 1.3)),

    # ---- Col 3: LPBF MVS ladder #1 ----
    ("mvs1",  "Single tracks\n(melt-pool W/D)",
     "lpbf",    (9.8, 6.3),  (2.0, 0.85)),
    ("mvs2",  "5$\\times$5$\\times$5 mm\ndensity cubes",
     "lpbf",    (9.8, 5.15), (2.0, 0.85)),
    ("mvs3",  "ISO 52902\nbenchmark geom.",
     "lpbf",    (9.8, 4.0),  (2.0, 0.85)),
    ("mvs4",  "ASTM E8 sub-size\ntensile bars",
     "lpbf",    (9.8, 2.85), (2.0, 0.85)),

    # ---- Col 4: As-built characterization #1 ----
    ("ch1",   "Density\n(Archimedes / $\\mu$CT)\ngate $\\geq$99% rel.",
     "char",    (13.0, 6.3),  (2.2, 0.95)),
    ("ch2",   "Microstructure\nSEM/EDS, EBSD, XRD\n(phases, texture)",
     "char",    (13.0, 5.05), (2.2, 1.05)),
    ("ch3",   "Vickers\nmicrohardness",
     "char",    (13.0, 3.95), (2.2, 0.85)),
    ("ch4",   "Tensile $\\sigma_y$,\nUTS, elongation\n(ASTM E8 sub-size)",
     "char",    (13.0, 2.7),  (2.2, 1.05)),

    # ---- Col 5: Valimet scale-up + Powder QC #2 ----
    ("vali",  "Valimet\ndistributed validation\ngas atomization\n6 $\\times$ $\\geq$50 kg",
     "atom",    (16.2, 5.2), (2.4, 1.3)),
    ("pqc2",  "Powder QC #2\n(scale-up powder)\nPSD, ICP-MS,\nSEM/EDS, O/N",
     "char",    (16.2, 3.5), (2.4, 1.3)),

    # ---- Col 6: LPBF MVS ladder #2 (scale-up powder) ----
    ("mvs1b", "Single tracks\n(scale-up powder)",
     "lpbf",    (19.4, 6.3),  (2.0, 0.85)),
    ("mvs2b", "5$\\times$5$\\times$5 mm\ndensity cubes",
     "lpbf",    (19.4, 5.15), (2.0, 0.85)),
    ("mvs3b", "ISO 52902\nbenchmark geom.",
     "lpbf",    (19.4, 4.0),  (2.0, 0.85)),
    ("mvs4b", "ASTM E8 sub-size\ntensile bars",
     "lpbf",    (19.4, 2.85), (2.0, 0.85)),

    # ---- Col 7: As-built characterization #2 ----
    ("ch1b",  "Density\n(Archimedes / $\\mu$CT)\ngate $\\geq$99% rel.",
     "char",    (22.6, 6.3),  (2.2, 0.95)),
    ("ch2b",  "Microstructure\nSEM/EDS, EBSD, XRD\n(phases, texture)",
     "char",    (22.6, 5.05), (2.2, 1.05)),
    ("ch3b",  "Vickers\nmicrohardness",
     "char",    (22.6, 3.95), (2.2, 0.85)),
    ("ch4b",  "Tensile $\\sigma_y$,\nUTS, elongation\n(ASTM E8 sub-size)",
     "char",    (22.6, 2.7),  (2.2, 1.05)),

    # ---- Col 8: Phase II milestone (far right, contingent) ----
    ("ph2",   "Qualified alloy\ncandidate(s)\n$\\rightarrow$ Phase II",
     "scale",   (25.8, 4.3), (2.2, 1.3)),
]

# y-coordinate of the top "highway" used by elbow_over routing
Y_HIGHWAY_TOP = 7.45

# --- Edge spec ----------------------------------------------------------
# Tuple: (src, dst, src_side, src_frac, dst_side, dst_frac, route, style)
#   src_side / dst_side: 'L', 'R', 'T', 'B'  (which side of the box)
#   src_frac / dst_frac: 0..1 along that side (0 = lower/left, 1 = upper/right)
#   route: 'straight', 'curve_up', 'curve_down', or 'elbow_over'
#   style: 'solid' or 'dashed'

EDGES = [
    # Inputs -> CALPHAD
    ("inp_c", "tc1",   "R", 0.5, "L", 0.5, "straight",   "solid"),
    ("inp_c", "tc2",   "R", 0.2, "L", 0.85, "curve_down","solid"),
    ("inp_p", "tc2",   "R", 0.7, "L", 0.3, "curve_up",   "solid"),

    # LPBF process params -> top of MVS ladder (long skip; route over the top)
    ("inp_p", "mvs1",  "T", 0.7, "T", 0.5, "elbow_over", "solid"),

    # CALPHAD -> AMAZEMET
    ("tc1",  "atom",   "R", 0.5, "L", 0.5,  "straight",  "solid", True),
    ("tc2",  "atom",   "R", 0.7, "L", 0.15, "curve_up",  "solid", True),

    # AMAZEMET -> Powder QC #1 (vertical)
    ("atom", "pqc",    "B", 0.5, "T", 0.5,  "straight",  "solid"),

    # Powder QC #1 -> top of MVS ladder #1
    ("pqc",  "mvs1",   "R", 0.7, "L", 0.2,  "curve_up",  "solid", True),

    # MVS ladder #1 progression (vertical)
    ("mvs1", "mvs2",   "B", 0.5, "T", 0.5,  "straight",  "solid"),
    ("mvs2", "mvs3",   "B", 0.5, "T", 0.5,  "straight",  "solid"),
    ("mvs3", "mvs4",   "B", 0.5, "T", 0.5,  "straight",  "solid"),

    # MVS #1 -> Char #1 (staggered src_frac to fan out cleanly)
    ("mvs2", "ch1",    "R", 0.85, "L", 0.4,  "curve_up",   "solid", True),
    ("mvs2", "ch2",    "R", 0.5,  "L", 0.7,  "straight",   "solid", True),
    ("mvs2", "ch3",    "R", 0.15, "L", 0.6,  "curve_down", "solid", True),
    ("mvs4", "ch4",    "R", 0.5,  "L", 0.6,  "curve_up",   "solid", True),
    ("mvs4", "ch2",    "R", 0.85, "L", 0.2,  "curve_up",   "solid", True),

    # Char #1 -> Valimet (gates passed; staggered dst_frac so arrows don't merge)
    ("ch1",  "vali",   "R", 0.4, "L", 0.85, "curve_down", "solid", True),
    ("ch4",  "vali",   "R", 0.6, "L", 0.15, "curve_up",   "solid", True),

    # Valimet -> Powder QC #2 (vertical)
    ("vali", "pqc2",   "B", 0.5, "T", 0.5,  "straight",   "solid"),

    # Powder QC #2 -> top of MVS ladder #2
    ("pqc2", "mvs1b",  "R", 0.7, "L", 0.2,  "curve_up",   "solid", True),

    # MVS ladder #2 progression
    ("mvs1b", "mvs2b", "B", 0.5, "T", 0.5,  "straight",   "solid"),
    ("mvs2b", "mvs3b", "B", 0.5, "T", 0.5,  "straight",   "solid"),
    ("mvs3b", "mvs4b", "B", 0.5, "T", 0.5,  "straight",   "solid"),

    # MVS #2 -> Char #2 (same fan-out pattern as round #1)
    ("mvs2b", "ch1b",  "R", 0.85, "L", 0.4,  "curve_up",   "solid", True),
    ("mvs2b", "ch2b",  "R", 0.5,  "L", 0.7,  "straight",   "solid", True),
    ("mvs2b", "ch3b",  "R", 0.15, "L", 0.6,  "curve_down", "solid", True),
    ("mvs4b", "ch4b",  "R", 0.5,  "L", 0.6,  "curve_up",   "solid", True),
    ("mvs4b", "ch2b",  "R", 0.85, "L", 0.2,  "curve_up",   "solid", True),

    # Char #2 -> Phase II milestone (dashed = contingent / future)
    ("ch1b", "ph2",    "R", 0.4, "L", 0.85, "curve_down", "dashed", True),
    ("ch4b", "ph2",    "R", 0.6, "L", 0.15, "curve_up",   "dashed", True),
]


def anchor(box, side, frac):
    x, y, w, h = box
    if side == "L":
        return (x,        y + frac * h)
    if side == "R":
        return (x + w,    y + frac * h)
    if side == "T":
        return (x + frac * w, y + h)
    if side == "B":
        return (x + frac * w, y)
    raise ValueError(side)


def draw_posterior_glyph(ax, mid_xy, half_w=0.14, half_h=0.10):
    """Draw a tiny Gaussian bell-curve glyph on a white background patch.

    Indicates that the parent edge carries a forwarded GP posterior
    p(y_k | D_n) per BOFN/pKGFN (Astudillo & Frazier 2021;
    Buathong et al. 2023, 2025).
    """
    cx, cy = mid_xy
    bg = FancyBboxPatch(
        (cx - half_w, cy - half_h), 2 * half_w, 2 * half_h,
        boxstyle="round,pad=0.01,rounding_size=0.05",
        linewidth=0.4, edgecolor="#555555", facecolor="white",
        zorder=4,
    )
    ax.add_patch(bg)
    import numpy as np
    xs = np.linspace(-1.8, 1.8, 25)
    ys = np.exp(-xs ** 2)
    px = cx + xs * (half_w * 0.55)
    py = (cy - half_h * 0.55) + ys * (half_h * 1.25)
    ax.plot(px, py, color="#222222", linewidth=0.7, zorder=5,
            solid_capstyle="round")


def edge_midpoint(p0, p1, route):
    """Return (x, y) midpoint of the drawn arrow path for glyph placement."""
    import numpy as np
    if route == "elbow_over":
        return (0.5 * (p0[0] + p1[0]), Y_HIGHWAY_TOP)
    mid = (0.5 * (p0[0] + p1[0]), 0.5 * (p0[1] + p1[1]))
    if route == "straight":
        return mid
    rad = -0.18 if route == "curve_up" else 0.18
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    chord = (dx * dx + dy * dy) ** 0.5
    if chord < 1e-9:
        return mid
    # arc3 quadratic Bezier: control point offset perpendicular to chord by rad*chord;
    # midpoint of the curve is offset from chord midpoint by 0.5*rad*chord.
    perp = (-dy / chord, dx / chord)
    return (mid[0] + 0.5 * rad * chord * perp[0],
            mid[1] + 0.5 * rad * chord * perp[1])


def draw_posterior_arrow(ax, p0, p1, glyph_xy, glyph_half_w, style):
    """Draw a smooth cubic-Bezier arrow from p0 to p1 that passes
    horizontally through the glyph (entering LHS, exiting RHS).

    The path is one continuous matplotlib Path with two CURVE4 segments
    flanking a hidden LINETO across the glyph interior, drawn as a
    single FancyArrowPatch so the arrowhead lands cleanly at p1.
    Control points enforce a horizontal tangent at the glyph entry/exit
    so the arrow looks like one fluid spline rather than two stitched arcs.
    """
    gx, gy = glyph_xy
    left = (gx - glyph_half_w, gy)
    right = (gx + glyph_half_w, gy)
    h0 = max(0.4 * abs(left[0] - p0[0]), 0.25)   # tangent handle (in)
    h1 = max(0.4 * abs(p1[0] - right[0]), 0.25)  # tangent handle (out)
    verts = [
        p0,                                     # MOVETO
        (p0[0] + h0, p0[1]),                    # CURVE4 control 1
        (left[0] - h0, left[1]),                # CURVE4 control 2 (horizontal at glyph)
        left,                                   # CURVE4 endpoint
        right,                                  # LINETO (hidden by glyph bg)
        (right[0] + h1, right[1]),              # CURVE4 control 1 (horizontal at glyph)
        (p1[0] - h1, p1[1]),                    # CURVE4 control 2
        p1,                                     # CURVE4 endpoint
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
    ]
    path = Path(verts, codes)
    arrow = FancyArrowPatch(
        path=path, arrowstyle="-|>", mutation_scale=9, linewidth=0.95,
        linestyle=style, color="#222222", zorder=1, shrinkA=0, shrinkB=0,
    )
    ax.add_patch(arrow)


def draw_arrow(ax, p0, p1, route, style, with_head=True):
    common = dict(
        arrowstyle="-|>" if with_head else "-",
        mutation_scale=9,
        linewidth=0.95,
        linestyle=style,
        color="#222222",
        zorder=1,
        shrinkA=0,
        shrinkB=0,
    )
    if route == "straight":
        arrow = FancyArrowPatch(p0, p1, connectionstyle="arc3,rad=0.0", **common)
    elif route == "curve_up":
        arrow = FancyArrowPatch(p0, p1, connectionstyle="arc3,rad=-0.18", **common)
    elif route == "curve_down":
        arrow = FancyArrowPatch(p0, p1, connectionstyle="arc3,rad=0.18", **common)
    elif route == "elbow_over":
        verts = [p0, (p0[0], Y_HIGHWAY_TOP), (p1[0], Y_HIGHWAY_TOP), p1]
        codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO]
        path = Path(verts, codes)
        arrow = FancyArrowPatch(path=path, **common)
    else:
        raise ValueError(route)
    ax.add_patch(arrow)


def draw():
    fig, ax = plt.subplots(figsize=(24.5, 6.0))
    ax.set_xlim(0, 28.2)
    ax.set_ylim(1.8, 7.7)
    ax.set_aspect("equal")
    ax.axis("off")

    # Draw nodes
    boxes = {}
    for nid, label, cat, (x, y), (w, h) in NODES:
        color = COLORS[cat]
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.03,rounding_size=0.12",
            linewidth=0.9, edgecolor="#333333",
            facecolor=color, zorder=2,
        )
        ax.add_patch(box)
        ax.text(x + w / 2, y + h / 2, label,
                ha="center", va="center", fontsize=7.3, zorder=3)
        boxes[nid] = (x, y, w, h)

    # Draw edges
    glyph_half_w = 0.14
    for edge in EDGES:
        src, dst, ss, sf, ds, df, route, style = edge[:8]
        posterior = edge[8] if len(edge) > 8 else False
        p0 = anchor(boxes[src], ss, sf)
        p1 = anchor(boxes[dst], ds, df)
        if posterior and route in ("straight", "curve_up", "curve_down"):
            # Place glyph horizontally centered in the gap between
            # source-node right edge and destination-node left edge.
            sx, sy, sw, sh = boxes[src]
            dx_box, dy_box, dw, dh = boxes[dst]
            gx = 0.5 * (sx + sw + dx_box)
            gy = 0.5 * (p0[1] + p1[1])
            draw_posterior_arrow(ax, p0, p1, (gx, gy), glyph_half_w, style)
            draw_posterior_glyph(ax, (gx, gy), half_w=glyph_half_w)
        else:
            draw_arrow(ax, p0, p1, route, style)
            if posterior:
                draw_posterior_glyph(ax, edge_midpoint(p0, p1, route),
                                     half_w=glyph_half_w)

    plt.tight_layout(pad=0.4)
    fig.savefig(OUT_PNG, dpi=220, bbox_inches="tight")
    fig.savefig(OUT_PDF, bbox_inches="tight")
    print(f"Wrote {OUT_PNG}")
    print(f"Wrote {OUT_PDF}")


if __name__ == "__main__":
    draw()
