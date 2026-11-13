"""Generate the FLAIME pipeline DAG figure (vertical / top-to-bottom).

Structure (top-to-bottom; BOFN/pKGFN acquisition graph, no orchestration nodes):

  Inputs (composition + LPBF process)
    -> CALPHAD partial-eval nodes (TC-Python Scheil + AM Module)
    -> Atomization siblings (Ultrasonic rePOWDER  ||  Gas Valimet)  -- categorical
       fidelity dimension #1; cost-aware acquisition picks the expensive Valimet
       branch sparingly.
    -> Powder QC (PSD, ICP-MS, SEM/EDS, O/N)
    -> AM platform siblings (BYU LPBF || Partner LPBF || DED || Binder Jet)  --
       categorical fidelity dimension #2; cross-platform/cross-modality
       validation network. Any (powder source x platform) combination admissible
       to pKGFN; expensive combos selected rarely.
    -> LPBF MVS ladder (4 nodes: single tracks, cubes, ISO 52902, ASTM E8)
    -> As-built characterization (4 nodes: density, microstructure, Vickers,
       tensile)
    -> Qualified alloy candidate(s) -> Phase II  (dashed = future)

Cost chips (~$X per evaluation) on every evaluable node visualize the relative
per-eval costs that drive cost-aware pKGFN acquisition. Composition/process
input boxes and the Phase II milestone get no chip (not GP-modeled).

Routing notes:
  - Posterior-forwarded edges (those carrying p(y_k | D_n) per BOFN/pKGFN)
    are drawn as a single FancyArrowPatch whose Path is a composite
    cubic-Bezier flowing through a small bell-curve glyph centered in the
    inter-row gap. Tangent at glyph top/bottom is vertical so the arrow
    reads as one fluid spline.
  - Platform -> MVS routing uses a horizontal "platform bus" so each
    platform's posterior conceptually feeds every MVS GP without drawing
    16 individual edges.
  - Glyph dimensions reduced 30% from the previous revision for tighter
    visual density.
  - A compact TRL roadmap is included in the top corner to distinguish the
    Phase I target from the follow-on Phase II scale-up path.
  - A horizontal version of this figure is preserved as
    flaime_pipeline_dag_horizontal.py.
"""

from pathlib import Path as FilePath

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path

HERE = FilePath(__file__).resolve().parent
OUT_PNG = HERE / "flaime_pipeline_dag.png"
OUT_PDF = HERE / "flaime_pipeline_dag.pdf"

# Category colors (colorblind-safe Okabe-Ito palette, muted)
COLORS = {
    "input":   "#E8E8E8",
    "calphad": "#A6CFE5",
    "atom":    "#BEE3B3",
    "char":    "#FFD0A8",
    "lpbf":    "#E6C9E6",
    "scale":   "#D8D8D8",
}

TRL_ROADMAP_TEXT = (
    "TRL roadmap: Phase I TRL 2$\\to$4 (lab closed loop)  |  "
    "Phase II TRL 5--6 (scale-up validation)"
)

# 4-up rows (platform, char) span 0.0..10.0; four box centers at
# 1.5, 4.0, 6.5, 9.0 with width 2.0
QUAD_CENTERS = [1.5, 4.0, 6.5, 9.0]
QUAD_W, QUAD_H = 2.0, 1.30

# 5-up MVS row (single tracks, thin-wall pillars, density cubes,
# ISO 52902, ASTM E8) spans the same x range with narrower boxes.
MVS_CENTERS = [1.0, 3.0, 5.0, 7.0, 9.0]
MVS_W, MVS_H = 1.7, 1.30

# Single-band node defaults
WIDE_W, WIDE_H = 4.5, 1.45

# Two side-by-side boxes per row (atomization siblings, CALPHAD, inputs)
PAIR_W, PAIR_H = 4.0, 1.45

# Row pitches: glyph rows need vertical headroom; tall multi-line boxes need
# extra room when the gap carries no glyph.
PITCH_G = 2.20        # row-to-row gap with bell-curve glyph
PITCH_S_TALL = 2.05   # no-glyph gap when adjacent rows have tall (multi-line) boxes
BUS_GAP = 0.75        # short stem from platform row down to bus

ROW_Y = {}
ROW_Y["inputs"]   = 18.50                                # composition + LPBF
ROW_Y["calphad"]  = ROW_Y["inputs"]   - PITCH_S_TALL     # no glyph (tall boxes)
ROW_Y["atom"]     = ROW_Y["calphad"]  - PITCH_G          # glyph
ROW_Y["pqc"]      = ROW_Y["atom"]     - PITCH_G          # glyph (atom -> pqc)
ROW_Y["plat"]     = ROW_Y["pqc"]      - PITCH_G          # glyph (pqc -> platform)
ROW_Y["bus"]      = ROW_Y["plat"]     - BUS_GAP          # routing only
ROW_Y["mvs"]      = ROW_Y["bus"]      - PITCH_G + 0.10   # glyph (bus -> mvs)
ROW_Y["char"]     = ROW_Y["mvs"]      - PITCH_G          # glyph (mvs -> char, colored)
ROW_Y["ph2"]      = ROW_Y["char"]     - PITCH_G          # glyph dashed

NODES = [
    # --- Inputs (two side-by-side; matched heights) ---
    ("inp_c", "Composition vector\n(Al + 15 elements,\nper-element bounds)",
     "input", (0.5, ROW_Y["inputs"] - PAIR_H/2), (PAIR_W, PAIR_H), None),
    ("inp_p", "LPBF process (20+ params:\nP, v, h, layer, spot, scan,\ngas flow, plate temp, $\\ldots$)",
     "input", (5.5, ROW_Y["inputs"] - PAIR_H/2), (PAIR_W, PAIR_H), None),

    # --- CALPHAD (two side-by-side) ---
    ("tc1", "TC-Python + TCAl10\n$\\sim$1--5 CPU-min/eval; Scheil,\nfreezing range, hot-cracking susc.",
     "calphad", (0.5, ROW_Y["calphad"] - PAIR_H/2), (PAIR_W, PAIR_H), "$\\sim$\\$1"),
    ("tc2", "TC AM Module\n$\\sim$0.5--2 CPU-hr/eval; LPBF\nsolidification map, crack susc.",
     "calphad", (5.5, ROW_Y["calphad"] - PAIR_H/2), (PAIR_W, PAIR_H), "$\\sim$\\$1"),

    # --- Atomization siblings (Ultrasonic | Gas/Valimet) ---
    ("atom_us", "AMAZEMET rePOWDER\nultrasonic atomization\n(100--1000 g, Ar)",
     "atom", (0.5, ROW_Y["atom"] - PAIR_H/2), (PAIR_W, PAIR_H), "$\\sim$\\$300"),
    ("atom_gas", "Valimet gas atomization\n(distributed scale-up,\n$\\geq$50 kg/run)",
     "atom", (5.5, ROW_Y["atom"] - PAIR_H/2), (PAIR_W, PAIR_H), "$\\sim$\\$8k"),

    # --- Powder QC (single, centered) ---
    ("pqc", "Powder QC: PSD (laser diff.), ICP-MS, SEM/EDS, O/N analyzer",
     "char", (2.5, ROW_Y["pqc"] - PAIR_H/2), (5.0, PAIR_H), "$\\sim$\\$500"),

    # --- AM platform siblings (4 in a row) ---
    ("plat_byu", "BYU LPBF\n(in-house)",
     "lpbf", (QUAD_CENTERS[0] - QUAD_W/2, ROW_Y["plat"] - QUAD_H/2),
     (QUAD_W, QUAD_H), "$\\sim$\\$1k"),
    ("plat_par", "Partner LPBF\n(distributed val.)",
     "lpbf", (QUAD_CENTERS[1] - QUAD_W/2, ROW_Y["plat"] - QUAD_H/2),
     (QUAD_W, QUAD_H), "$\\sim$\\$3k"),
    ("plat_ded", "DED\n(partner sites)",
     "lpbf", (QUAD_CENTERS[2] - QUAD_W/2, ROW_Y["plat"] - QUAD_H/2),
     (QUAD_W, QUAD_H), "$\\sim$\\$5k"),
    ("plat_bj",  "Binder Jet\n(partner sites)",
     "lpbf", (QUAD_CENTERS[3] - QUAD_W/2, ROW_Y["plat"] - QUAD_H/2),
     (QUAD_W, QUAD_H), "$\\sim$\\$4k"),

    # --- MVS ladder (5 in a row, shared) ---
    ("mvs1", "Single tracks\n(melt-pool W/D)",
     "lpbf", (MVS_CENTERS[0] - MVS_W/2, ROW_Y["mvs"] - MVS_H/2),
     (MVS_W, MVS_H), "$\\sim$\\$50"),
    ("mvs_pillars", "Thin-wall pillars\nhot-cracking screen",
     "lpbf", (MVS_CENTERS[1] - MVS_W/2, ROW_Y["mvs"] - MVS_H/2),
     (MVS_W, MVS_H), "$\\sim$\\$80"),
    ("mvs2", "5$\\times$5$\\times$5\nmm cubes",
     "lpbf", (MVS_CENTERS[2] - MVS_W/2, ROW_Y["mvs"] - MVS_H/2),
     (MVS_W, MVS_H), "$\\sim$\\$200"),
    ("mvs3", "ISO 52902\nbenchmark geom.",
     "lpbf", (MVS_CENTERS[3] - MVS_W/2, ROW_Y["mvs"] - MVS_H/2),
     (MVS_W, MVS_H), "$\\sim$\\$500"),
    ("mvs4", "ASTM E8 sub-size\ntensile bars",
     "lpbf", (MVS_CENTERS[4] - MVS_W/2, ROW_Y["mvs"] - MVS_H/2),
     (MVS_W, MVS_H), "$\\sim$\\$1k"),

    # --- Char ladder (4 in a row, shared) ---
    ("ch1", "Density\n($\\geq$99% rel.)",
     "char", (QUAD_CENTERS[0] - QUAD_W/2, ROW_Y["char"] - QUAD_H/2),
     (QUAD_W, QUAD_H), "$\\sim$\\$20"),
    ("ch2", "Microstructure\nSEM/EDS, EBSD, XRD",
     "char", (QUAD_CENTERS[1] - QUAD_W/2, ROW_Y["char"] - QUAD_H/2),
     (QUAD_W, QUAD_H), "$\\sim$\\$100"),
    ("ch3", "Vickers\nmicrohardness",
     "char", (QUAD_CENTERS[2] - QUAD_W/2, ROW_Y["char"] - QUAD_H/2),
     (QUAD_W, QUAD_H), "$\\sim$\\$30"),
    ("ch4", "Tensile $\\sigma_y$,\nUTS, elong.",
     "char", (QUAD_CENTERS[3] - QUAD_W/2, ROW_Y["char"] - QUAD_H/2),
     (QUAD_W, QUAD_H), "$\\sim$\\$200"),

    # --- Phase II milestone ---
    ("ph2", "Qualified alloy candidate(s) $\\to$ Phase II (TRL 6)",
     "scale", (2.5, ROW_Y["ph2"] - PAIR_H/2), (5.0, PAIR_H), None),
]

# Per-node imagery: (image, logo) -- both optional, paths relative to repo root.
# Image is rendered inside the node body (lower portion); logo is a small
# corner badge placed at the top-right of the node outline.
REPO_ROOT = HERE.parent
NODE_ASSETS = {
    "inp_c":     {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "periodic-table" / "periodic_table_bounds.png",                 "logo": None},
    "inp_p":     {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "lpbf_pvh_schematic.png",                                          "logo": None},
    "tc1":       {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "scheil_susceptibility_combo.png",                                "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "thermocalc-logo.png"},
    "tc2":       {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "printability-map-plus-melt-pool.png",                            "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "thermocalc-logo.png"},
    "atom_us":   {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "amazemet_combo.png",                                            "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "amazemet-logo.png"},
    "atom_gas":  {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "atom_gas_combo.png",                                 "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "valimet-logo.png"},
    "pqc":       {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "pqc_combo.png",                                                   "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "byu-logo.png"},
    "plat_byu":  {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "lpbf_byu_combo.png",                                              "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "byu-logo.png"},
    "plat_par":  {"image": REPO_ROOT / "genesis-mission-proposal" / "figures" / "equipment" / "aconity-midi.png",                        "logo": [
        REPO_ROOT / "figures" / "dag-thumbnails" / "utah-logo.png",
        REPO_ROOT / "figures" / "dag-thumbnails" / "gatech-logo.png",
        REPO_ROOT / "figures" / "dag-thumbnails" / "cmu-logo.png",
        REPO_ROOT / "figures" / "dag-thumbnails" / "unt-logo.png",
        REPO_ROOT / "figures" / "dag-thumbnails" / "uwmadison-logo.png",
        REPO_ROOT / "figures" / "dag-thumbnails" / "ucf-logo.png",
        REPO_ROOT / "figures" / "dag-thumbnails" / "ncsu-logo.png",
        REPO_ROOT / "figures" / "dag-thumbnails" / "utep-logo.png",
        REPO_ROOT / "figures" / "dag-thumbnails" / "mines-logo.png",
    ]},
    "plat_ded":  {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "ded_photo.jpeg",                          "logo": [
        REPO_ROOT / "figures" / "dag-thumbnails" / "gatech-logo.png",
        REPO_ROOT / "figures" / "dag-thumbnails" / "uwmadison-logo.png",
    ]},
    "plat_bj":   {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "binder_jet_combo.png", "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "byu-logo.png"},
    "mvs1":      {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "single_tracks.png", "logo": None},
    "mvs_pillars": {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "thin_walls.png",  "logo": None},
    "mvs2":      {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "density_cubes.png", "logo": None},
    "mvs3":      {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "iso52902.png",      "logo": None},
    "mvs4":      {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "tensile_bars_combo.png",  "logo": None},
    "ch1":       {"image": REPO_ROOT / "figures" / "archimedes-method.jpeg", "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "byu-logo.png"},
    "ch2":       {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "microstructure_combo.png",                                       "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "byu-logo.png"},
    "ch3":       {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "vickers-indent.jpg",                          "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "byu-logo.png"},
    "ch4":       {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "stress_strain_tensile_combo.png",                     "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "byu-logo.png"},
    "ph2":       {"image": REPO_ROOT / "figures" / "dag-thumbnails" / "phase2_applications_combo.png", "logo": REPO_ROOT / "figures" / "dag-thumbnails" / "ames-lab-logo.png"},
}

# Edge spec: (src, dst, src_side, src_frac, dst_side, dst_frac, posterior?)
# Sides: 'L', 'R', 'T', 'B'.
EDGES = [
    # Inputs -> CALPHAD (root inputs, no glyph since not GP-modeled)
    ("inp_c", "tc1",   "B", 0.5, "T", 0.5, False),
    ("inp_c", "tc2",   "B", 0.85, "T", 0.35, False),
    ("inp_p", "tc2",   "B", 0.5, "T", 0.55, False),

    # CALPHAD -> Atomization siblings (BOFN posterior forwarding).
    # Color-coded by source: tc1 = purple, tc2 = teal. Each TC feeds
    # both atom siblings. All 4 glyphs sit on the SAME y (row midpoint,
    # gy_bias=0.5); crosses use gx_offset to spread sideways so the
    # 4 glyphs read as a horizontal row, not stacked.
    # Tuple: (src, dst, ss, sf, ds, df, posterior, gy_bias, color, gx_offset)
    ("tc1",  "atom_us",  "B", 0.5,  "T", 0.5,  True, 0.50, "#7e3f9c", 0.0),
    ("tc1",  "atom_gas", "B", 0.85, "T", 0.25, True, 0.50, "#7e3f9c", -0.45),
    ("tc2",  "atom_us",  "B", 0.15, "T", 0.75, True, 0.50, "#17a2a2", 0.45),
    ("tc2",  "atom_gas", "B", 0.5,  "T", 0.5,  True, 0.50, "#17a2a2", 0.0),

    # Atomization siblings -> Powder QC (BOFN: both sources feed shared QC GP
    # with source as a categorical input)
    ("atom_us",  "pqc", "B", 0.6, "T", 0.25, True),
    ("atom_gas", "pqc", "B", 0.4, "T", 0.75, True),

    # Powder QC -> AM platform siblings (fan-out; each platform GP receives
    # the QC-conditioned posterior. Phase I scope includes all four.)
    ("pqc", "plat_byu", "B", 0.10, "T", 0.5, True),
    ("pqc", "plat_par", "B", 0.40, "T", 0.5, True),
    ("pqc", "plat_ded", "B", 0.60, "T", 0.5, True),
    ("pqc", "plat_bj",  "B", 0.90, "T", 0.5, True),

    # MVS ladder -> Char ladder: direct colored edges (one color per
    # MVS source). All glyphs on SAME y (row midpoint, gy_bias=0.5);
    # gx_offset spreads them horizontally so crossing-edge glyphs sit
    # side-by-side rather than overlapping.
    # Tuple: (src, dst, ss, sf, ds, df, posterior, gy_bias, color, gx_offset)
    ("mvs1",        "ch2",  "B", 0.65, "T", 0.10, True, 0.50, "#1f77b4", -0.45),
    ("mvs_pillars", "ch2",  "B", 0.55, "T", 0.30, True, 0.50, "#9467bd", -0.15),
    ("mvs2",        "ch1",  "B", 0.30, "T", 0.85, True, 0.50, "#d62728",  0.30),
    ("mvs2",        "ch2",  "B", 0.5,  "T", 0.5,  True, 0.50, "#d62728",  0.0),
    ("mvs2",        "ch3",  "B", 0.70, "T", 0.15, True, 0.50, "#d62728", -0.30),
    ("mvs3",        "ch2",  "B", 0.30, "T", 0.90, True, 0.50, "#2ca02c",  0.30),
    ("mvs4",        "ch4",  "B", 0.5,  "T", 0.5,  True, 0.50, "#ff7f0e",  0.0),

    # Char -> Phase II (dashed; terminal posterior)
    ("ch1", "ph2",  "B", 0.5, "T", 0.15, True),
    ("ch2", "ph2",  "B", 0.5, "T", 0.40, True),
    ("ch3", "ph2",  "B", 0.5, "T", 0.60, True),
    ("ch4", "ph2",  "B", 0.5, "T", 0.85, True),
]

# Edges that are dashed (Phase II contingent)
DASHED_EDGES = {("ch1", "ph2"), ("ch2", "ph2"), ("ch3", "ph2"), ("ch4", "ph2")}

# Bus routing for platform <-> MVS: each platform sends a stem down to a
# horizontal bus (no glyph, no arrowhead); the bus then sends a glyphed arrow
# up to each MVS node. This visually encodes the any-platform-x-any-MVS
# admissibility without drawing 16 individual edges.
BUS_PLATFORMS = ["plat_byu", "plat_par", "plat_ded", "plat_bj"]
BUS_MVS       = ["mvs1", "mvs_pillars", "mvs2", "mvs3", "mvs4"]


def anchor(box, side, frac):
    x, y, w, h = box
    if side == "L":
        return (x, y + frac * h)
    if side == "R":
        return (x + w, y + frac * h)
    if side == "T":
        return (x + frac * w, y + h)
    if side == "B":
        return (x + frac * w, y)
    raise ValueError(side)


def draw_posterior_glyph(ax, mid_xy, half_w=0.28, half_h=0.196,
                         color="#222222", edge_color=None):
    """Small Gaussian bell-curve glyph on a white background patch.
    Indicates the parent edge carries a forwarded GP posterior
    p(y_k | D_n) per BOFN/pKGFN. Glyph dims 30% smaller than r1.
    """
    cx, cy = mid_xy
    if edge_color is None:
        edge_color = "#555555" if color == "#222222" else color
    bg = FancyBboxPatch(
        (cx - half_w, cy - half_h), 2 * half_w, 2 * half_h,
        boxstyle="round,pad=0.015,rounding_size=0.07",
        linewidth=0.4, edgecolor=edge_color, facecolor="white",
        zorder=4,
    )
    ax.add_patch(bg)
    import numpy as np
    xs = np.linspace(-1.8, 1.8, 25)
    ys = np.exp(-xs ** 2)
    px = cx + xs * (half_w * 0.55)
    py = (cy - half_h * 0.55) + ys * (half_h * 1.25)
    ax.plot(px, py, color=color, linewidth=0.6, zorder=5,
            solid_capstyle="round")


def draw_posterior_arrow(ax, p0, p1, glyph_xy, glyph_half_h, style,
                         color="#222222"):
    """Smooth cubic-Bezier arrow p0 -> glyph_top -> hidden -> glyph_bottom -> p1.
    Vertical tangent at glyph entry/exit so the curve looks continuous.
    """
    gx, gy = glyph_xy
    top = (gx, gy + glyph_half_h)
    bot = (gx, gy - glyph_half_h)
    h0 = max(0.4 * abs(p0[1] - top[1]), 0.30)
    h1 = max(0.4 * abs(bot[1] - p1[1]), 0.30)
    verts = [
        p0,
        (p0[0], p0[1] - h0),
        (top[0], top[1] + h0),
        top,
        bot,
        (bot[0], bot[1] - h1),
        (p1[0], p1[1] + h1),
        p1,
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
    ]
    path = Path(verts, codes)
    arrow = FancyArrowPatch(
        path=path, arrowstyle="-|>", mutation_scale=8.5, linewidth=0.95,
        linestyle=style, color=color, zorder=1, shrinkA=0, shrinkB=0,
    )
    ax.add_patch(arrow)


def draw_simple_arrow(ax, p0, p1, style, color="#222222"):
    """Downward arrow. Vertical when endpoints aligned; otherwise S-curve
    with vertical tangents at both ends.
    """
    dx = p1[0] - p0[0]
    if abs(dx) < 0.05:
        arrow = FancyArrowPatch(
            p0, p1, arrowstyle="-|>", mutation_scale=8.5, linewidth=0.95,
            linestyle=style, color=color, zorder=1, shrinkA=0, shrinkB=0,
            connectionstyle="arc3,rad=0.0",
        )
    else:
        dy = abs(p0[1] - p1[1])
        h = max(0.55 * abs(dx), 0.6 * dy, 0.6)
        verts = [
            p0,
            (p0[0], p0[1] - h),
            (p1[0], p1[1] + h),
            p1,
        ]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        path = Path(verts, codes)
        arrow = FancyArrowPatch(
            path=path, arrowstyle="-|>", mutation_scale=8.5, linewidth=0.95,
            linestyle=style, color=color, zorder=1, shrinkA=0, shrinkB=0,
        )
    ax.add_patch(arrow)


def draw_stem(ax, p0, p1):
    """Plain vertical line segment, no arrowhead (used for platform->bus stems).
    """
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]],
            color="#222222", linewidth=0.95, zorder=1, solid_capstyle="round")


def draw_node_thumbnail(ax, box, image_path):
    """Render a thumbnail (or gray placeholder) inside the lower portion of a
    node box. Image is fit while preserving aspect ratio and centered.
    """
    x, y, w, h = box
    pad_x = 0.10
    pad_top = 0.50   # leaves room for title at top of box
    pad_bot = 0.18   # leaves room for cost chip
    inner_x0 = x + pad_x
    inner_x1 = x + w - pad_x
    inner_y0 = y + pad_bot
    inner_y1 = y + h - pad_top
    inner_w = inner_x1 - inner_x0
    inner_h = inner_y1 - inner_y0
    if inner_w <= 0 or inner_h <= 0:
        return
    if image_path is None or not FilePath(image_path).exists():
        # gray placeholder
        ax.add_patch(plt.Rectangle(
            (inner_x0, inner_y0), inner_w, inner_h,
            facecolor="#e8e8e8", edgecolor="#bbbbbb",
            linewidth=0.4, zorder=2.5,
        ))
        ax.text(inner_x0 + inner_w/2, inner_y0 + inner_h/2,
                "(placeholder)", ha="center", va="center",
                fontsize=5.0, color="#888888", style="italic", zorder=2.6)
        return
    try:
        img = mpimg.imread(str(image_path))
    except Exception:
        return
    ih, iw = img.shape[0], img.shape[1]
    img_ar = iw / ih
    box_ar = inner_w / inner_h
    if img_ar > box_ar:
        # image wider; fit width
        draw_w = inner_w
        draw_h = inner_w / img_ar
    else:
        draw_h = inner_h
        draw_w = inner_h * img_ar
    cx = inner_x0 + inner_w / 2
    cy = inner_y0 + inner_h / 2
    extent = (cx - draw_w/2, cx + draw_w/2, cy - draw_h/2, cy + draw_h/2)
    ax.imshow(img, extent=extent, zorder=2.5, aspect="auto",
              interpolation="bilinear", cmap="gray" if img.ndim == 2 else None)


def draw_node_logo(ax, box, logo_path):
    """Render partner logo(s) as small corner badge(s).

    Single logo: anchored top-LEFT, overlapping the border slightly.
    List of logos: stacked vertically along the LEFT edge, top-down,
    each in its own white rounded backer for legibility.
    """
    if logo_path is None:
        return
    if isinstance(logo_path, (list, tuple)):
        paths = [p for p in logo_path if p is not None and FilePath(p).exists()]
    else:
        if not FilePath(logo_path).exists():
            return
        paths = [logo_path]
    if not paths:
        return
    x, y, w, h = box
    n = len(paths)
    if n == 1:
        try:
            img = mpimg.imread(str(paths[0]))
        except Exception:
            return
        ih, iw = img.shape[0], img.shape[1]
        ar = iw / ih
        badge_h = 0.22
        badge_w = badge_h * ar
        max_w = 0.65
        if badge_w > max_w:
            badge_w = max_w
            badge_h = badge_w / ar
        bx0 = x - 0.04
        bx1 = bx0 + badge_w
        by1 = y + h + 0.08
        by0 = by1 - badge_h
        ax.add_patch(FancyBboxPatch(
            (bx0 - 0.04, by0 - 0.04), badge_w + 0.08, badge_h + 0.08,
            boxstyle="round,pad=0.0,rounding_size=0.06",
            linewidth=0.5, edgecolor="#666666", facecolor="white",
            zorder=4.5,
        ))
        ax.imshow(img, extent=(bx0, bx1, by0, by1), zorder=4.6,
                  aspect="auto", interpolation="bilinear")
        return

    # Multi-logo: vertical stack along left edge.
    badge_h = 0.16
    badge_w = 0.42
    v_gap = 0.04
    # Anchor strip just inside the left edge, starting slightly above box top.
    bx0 = x - 0.04
    bx1 = bx0 + badge_w
    by_top_first = y + h + 0.08  # top edge of the first (topmost) badge
    # If stack would extend below the box bottom, scale down uniformly.
    total_h = n * badge_h + (n - 1) * v_gap
    avail = h + 0.08
    if total_h > avail:
        scale = avail / total_h
        badge_h *= scale
        badge_w *= scale
        v_gap *= scale
    cursor_top = by_top_first
    for p in paths:
        try:
            img = mpimg.imread(str(p))
        except Exception:
            continue
        ih, iw = img.shape[0], img.shape[1]
        ar = iw / ih
        # Fit image within the badge box preserving aspect ratio.
        if ar >= badge_w / badge_h:
            draw_w = badge_w
            draw_h = badge_w / ar
        else:
            draw_h = badge_h
            draw_w = badge_h * ar
        cx = bx0 + badge_w / 2
        cy = cursor_top - badge_h / 2
        # White rounded backer
        ax.add_patch(FancyBboxPatch(
            (bx0 - 0.025, cursor_top - badge_h - 0.025),
            badge_w + 0.05, badge_h + 0.05,
            boxstyle="round,pad=0.0,rounding_size=0.04",
            linewidth=0.5, edgecolor="#666666", facecolor="white",
            zorder=4.5,
        ))
        ax.imshow(img, extent=(cx - draw_w/2, cx + draw_w/2,
                                cy - draw_h/2, cy + draw_h/2),
                  zorder=4.6, aspect="auto", interpolation="bilinear")
        cursor_top -= (badge_h + v_gap)


def draw_cost_chip(ax, box, text):
    """Render an italic gray cost chip (~$X) at the bottom-right corner of
    a node box.
    """
    if text is None:
        return
    x, y, w, h = box
    ax.text(x + w - 0.08, y + 0.08, text,
            ha="right", va="bottom", fontsize=5.8,
            style="italic", color="#444444", zorder=4,
            bbox=dict(boxstyle="round,pad=0.10", facecolor="white",
                      edgecolor="none", alpha=0.85))


# Stable node identifiers for cross-references in the narrative, captions,
# and risk register. Row-major top-to-bottom; bus row carries no glyph.
NODE_LABEL = {
    "inp_c": "1a", "inp_p": "1b",
    "tc1":   "2a", "tc2":   "2b",
    "atom_us": "3a", "atom_gas": "3b",
    "pqc": "4",
    "plat_byu": "5a", "plat_par": "5b",
    "plat_ded": "5c", "plat_bj":  "5d",
    "mvs1": "6a", "mvs_pillars": "6b",
    "mvs2": "6c", "mvs3": "6d", "mvs4": "6e",
    "ch1": "7a", "ch2": "7b", "ch3": "7c", "ch4": "7d",
    "ph2": "8",
}


def draw_node_label(ax, box, text):
    """Render the row-letter node ID at the bottom-left corner of a node
    box, mirroring the cost-chip styling.
    """
    if text is None:
        return
    x, y, w, h = box
    ax.text(x + 0.08, y + 0.08, text,
            ha="left", va="bottom", fontsize=5.8,
            style="italic", color="#444444", zorder=4,
            bbox=dict(boxstyle="round,pad=0.10", facecolor="white",
                      edgecolor="none", alpha=0.85))


def draw_phase_trl_roadmap_callout(ax):
    x, y = 0.55, 19.55
    w, h = 9.00, 0.45
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.10",
        linewidth=0.7, edgecolor="#666666",
        facecolor="white", alpha=0.94, zorder=5,
    ))
    ax.text(
        x + w / 2, y + h / 2, TRL_ROADMAP_TEXT,
        ha="center", va="center", fontsize=5.9, color="#222222", zorder=6,
    )


def draw():
    fig, ax = plt.subplots(figsize=(8.0, 13.0))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(1.5, 19.6)
    ax.set_aspect("equal")
    ax.axis("off")

    # Draw nodes (now with optional 6th tuple element = cost chip text)
    boxes = {}
    for nid, label, cat, (x, y), (w, h), cost in NODES:
        color = COLORS[cat]
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.03,rounding_size=0.12",
            linewidth=0.9, edgecolor="#333333",
            facecolor=color, zorder=2,
        )
        ax.add_patch(box)
        boxes[nid] = (x, y, w, h)
        # Title strip at top of box
        ax.text(x + w / 2, y + h - 0.10, label,
                ha="center", va="top", fontsize=6.6, zorder=3,
                linespacing=1.05)
        # Thumbnail (or placeholder) in the body
        assets = NODE_ASSETS.get(nid, {})
        draw_node_thumbnail(ax, boxes[nid], assets.get("image"))
        # Cost chip on top of everything bottom-right
        draw_cost_chip(ax, boxes[nid], cost)
        # Stable node ID at bottom-left for narrative cross-references
        draw_node_label(ax, boxes[nid], NODE_LABEL.get(nid))
        # Partner logo as corner badge
        draw_node_logo(ax, boxes[nid], assets.get("logo"))

    # Draw declared edges
    glyph_half_w, glyph_half_h = 0.28, 0.196
    # Slightly smaller glyphs for colored side-by-side rows (TC->atom,
    # MVS->char) so they fit horizontally without crowding.
    cglyph_half_w, cglyph_half_h = 0.22, 0.155
    for edge in EDGES:
        if len(edge) == 7:
            src, dst, ss, sf, ds, df, posterior = edge
            gy_bias = 0.5
            color = "#222222"
            gx_offset = 0.0
        elif len(edge) == 8:
            src, dst, ss, sf, ds, df, posterior, gy_bias = edge
            color = "#222222"
            gx_offset = 0.0
        elif len(edge) == 9:
            src, dst, ss, sf, ds, df, posterior, gy_bias, color = edge
            gx_offset = 0.0
        else:
            (src, dst, ss, sf, ds, df, posterior, gy_bias, color,
             gx_offset) = edge
        is_colored = color != "#222222"
        gw = cglyph_half_w if is_colored else glyph_half_w
        gh = cglyph_half_h if is_colored else glyph_half_h
        p0 = anchor(boxes[src], ss, sf)
        p1 = anchor(boxes[dst], ds, df)
        style = "dashed" if (src, dst) in DASHED_EDGES else "solid"
        if posterior:
            sx, sy, sw, sh = boxes[src]
            dx_box, dy_box, dw, dh = boxes[dst]
            gx = (1 - gy_bias) * p0[0] + gy_bias * p1[0] + gx_offset
            src_y = sy
            dst_y = dy_box + dh
            gy = (1 - gy_bias) * src_y + gy_bias * dst_y
            draw_posterior_arrow(ax, p0, p1, (gx, gy), gh, style,
                                 color=color)
            draw_posterior_glyph(ax, (gx, gy), half_w=gw,
                                 half_h=gh,
                                 color=color, edge_color=color)
        else:
            draw_simple_arrow(ax, p0, p1, style)

    # --- Platform -> bus -> MVS routing ---
    bus_y = ROW_Y["bus"]
    # Bus horizontal line spans the platform/mvs column range with small inset
    bus_x0 = min(QUAD_CENTERS[0], MVS_CENTERS[0]) - 0.20
    bus_x1 = max(QUAD_CENTERS[-1], MVS_CENTERS[-1]) + 0.20
    ax.plot([bus_x0, bus_x1], [bus_y, bus_y],
            color="#222222", linewidth=1.4, zorder=1, solid_capstyle="round")
    # Stems from each platform bottom-center down to the bus
    for pid in BUS_PLATFORMS:
        px, py, pw, ph = boxes[pid]
        stem_top = (px + pw / 2, py)
        stem_bot = (px + pw / 2, bus_y)
        draw_stem(ax, stem_top, stem_bot)
    # Glyphed arrows from bus down to each MVS top (with bell-curve glyph
    # in the gap, indicating posterior forwarding from the platform-conditioned
    # signal into the MVS GP)
    for mid in BUS_MVS:
        mx, my, mw, mh = boxes[mid]
        bus_pt = (mx + mw / 2, bus_y)
        mvs_top = (mx + mw / 2, my + mh)
        gx = mx + mw / 2
        gy = 0.5 * (bus_y + mvs_top[1])
        draw_posterior_arrow(ax, bus_pt, mvs_top, (gx, gy),
                             glyph_half_h, "solid")
        draw_posterior_glyph(ax, (gx, gy), half_w=glyph_half_w,
                             half_h=glyph_half_h)

    # Small bus annotation (any platform x any MVS test)
    ax.text(bus_x1 + 0.15, bus_y, "any platform $\\times$ any MVS",
            ha="left", va="center", fontsize=5.8,
            style="italic", color="#444444", zorder=4)

    plt.tight_layout(pad=0.4)
    fig.savefig(OUT_PNG, dpi=600, bbox_inches="tight")
    fig.savefig(OUT_PDF, bbox_inches="tight")
    print(f"Wrote {OUT_PNG}")
    print(f"Wrote {OUT_PDF}")


if __name__ == "__main__":
    draw()
