"""Draw the synthetic alloy function network of the BOFN benchmark as a DAG.

    python network_dag.py            # writes every view as PNG plus a contact sheet

The graph is read from `bofn_alloy.py` one directory up (`SPEC`, `GROUPS`,
`COSTS`, `LAMBDA`), so the picture cannot drift from the code that ran the
benchmark. Views:

- network:        the function network in the FLAIME-DAG style (rounded gray
                  boxes, a column per stage, cost chips, Aptos, red as the only
                  highlight); `symbols=True` adds the code's node letters
- paper:          the same graph the way Astudillo & Frazier (2021) and
                  Buathong et al. (2024) draw function networks: circles f_k,
                  inputs x_i, intermediate outputs y_k on the edges (the figure
                  in the Utah deck)
- partial/<grp>:  one evaluation at a time: what one action buys and costs
- chain:          what a full-pipeline policy buys per design
- missed-effect:  the edge the CALPHAD screen cannot see (kappa)
- posteriors:     one GP per node; each child sees its parents' outputs
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path as MPath

HERE = Path(__file__).resolve().parent


def load_graph():
    """SPEC, GROUPS, COSTS, LAMBDA from ../bofn_alloy.py without importing torch.

    The graph is defined there as plain literals; this executes only those
    assignments, so the figure always matches the code that ran the benchmark."""
    import ast

    src = (HERE.parent / "bofn_alloy.py").read_text()
    tree = ast.parse(src)
    wanted = {"D", "COMP", "IA", "IPV", "COSTS", "FULL_COST", "LAMBDA", "SPEC", "ORDER", "GROUPS", "GROUP_OF"}

    def names(target):  # `A = ...` and `A, B = ...`
        return [target.id] if isinstance(target, ast.Name) else [e.id for e in getattr(target, "elts", []) if isinstance(e, ast.Name)]

    keep = [n for n in tree.body if isinstance(n, ast.Assign) and any(set(names(t)) & wanted for t in n.targets)]
    ns = {}
    exec(compile(ast.Module(body=keep, type_ignores=[]), "bofn_alloy.py", "exec"), ns)
    return ns


_G = load_graph()
COSTS, FULL_COST, GROUPS, LAMBDA, SPEC = _G["COSTS"], _G["FULL_COST"], _G["GROUPS"], _G["LAMBDA"], _G["SPEC"]

for f in (Path.home() / ".local/share/fonts/aptos").glob("Aptos*.ttf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams.update({"font.family": "Aptos", "mathtext.fontset": "cm", "savefig.dpi": 220})

# deck palette (same as scripts/slides/dag_drilldown.py)
INK, GRAY, LIGHT, FAINT = "#1A1A1A", "#7F7F7F", "#BFBFBF", "#D9D9D9"
RED, RED_FADED = "#FF0000", "#FF9999"
NODE_FILL, NODE_LINE, EDGE = "#F4F4F4", "#595959", "#404040"
WHITE = "#FFFFFF"

# --------------------------------------------------------------------------- the graph
# node -> (label, column, row centre in inches from the top)
NODES = {
    "s": ("Strengthening\nphase fraction", "C", 1.75),
    "f": ("Freezing\nrange", "C", 2.85),
    "g": ("Nucleant\nfraction", "C", 3.95),
    "q": ("Powder\nquality", "A", 5.35),
    "rho": ("Dense,\ncrack-free\nfraction", "L", 4.45),
    "U": ("Strength", "T", 3.05),
}
INPUTS = {  # design variables: label, column, row centre, which side of the node they enter
    "comp": ("Composition\nZn+Mg, Cu, Zr, Sc", "I", 2.85, "right"),
    "a": ("Atomizer\nsetting", "A", 6.42, "up"),
    "pv": ("Laser power,\nscan speed", "L", 5.78, "up"),
}
OBJ = ("Strength\n− 0.3 × burden", "O", 3.05)
COLS = ["I", "C", "A", "L", "T", "O"]
HEADERS = {"I": "Inputs", "C": "CALPHAD", "A": "Atomize", "L": "Print", "T": "Test", "O": "Objective"}
GROUP_NAMES = {"C": "Simulate", "A": "Atomize", "L": "Print", "T": "Test"}
SYMBOL = {"s": "s", "f": "f", "g": "g", "q": "q", "rho": "ρ", "U": "U"}
INPUT_SYMBOL = {"comp": "c", "a": "a", "pv": "P, v"}

# edges straight from the benchmark's SPEC: parent node -> child node
EDGES = [(p, n) for n, (_, parents) in SPEC.items() for p in parents]
EDGES += [("U", "OBJ")]
INPUT_EDGES = [("comp", "s"), ("comp", "f"), ("comp", "g"), ("a", "q"), ("pv", "rho")]
GROUP_OF = {n: g for g, ns in GROUPS.items() for n in ns}

W, H = 13.333, 6.95
BOX_W, BOX_H, IN_H = 1.76, 0.95, 0.6
MARGIN = 0.32
GAP = (W - 2 * MARGIN - len(COLS) * BOX_W) / (len(COLS) - 1)
COL_X = {c: MARGIN + i * (BOX_W + GAP) for i, c in enumerate(COLS)}
HEADER_Y, BYPASS_Y = 0.40, 0.95


def rect_of(key):
    """(x, y, w, h) in inches, y from the top."""
    if key == "OBJ":
        _, col, yc = OBJ
        return COL_X[col], yc - BOX_H / 2, BOX_W, BOX_H
    if key in NODES:
        _, col, yc = NODES[key]
        return COL_X[col], yc - BOX_H / 2, BOX_W, BOX_H
    _, col, yc, _ = INPUTS[key]
    return COL_X[col], yc - IN_H / 2, BOX_W, IN_H


def fmt_cost(c):
    return f"${c:,.0f}"


# --------------------------------------------------------------------------- drawing
def new_canvas(w=W, h=H):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)  # y grows downward, like the slide
    ax.axis("off")
    return fig, ax


def box(ax, rect, fill=NODE_FILL, line=NODE_LINE, lw=1.3, dashed=False, radius=0.1, z=3):
    x, y, w, h = rect
    p = FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
        fc=fill if fill else "none", ec=line, lw=lw, ls=(0, (4, 2.5)) if dashed else "-", zorder=z,
    )
    ax.add_patch(p)
    return p


def bezier(ax, p0, p1, color=EDGE, lw=1.5, head=True, dashed=False, z=2, head_scale=13):
    """Left-to-right cubic with horizontal tangents, the FLAIME figure's edge."""
    (x0, y0), (x1, y1) = p0, p1
    d = 0.5 * (x1 - x0)
    path = MPath([(x0, y0), (x0 + d, y0), (x1 - d, y1), (x1, y1)], [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
    arr = FancyArrowPatch(
        path=path, arrowstyle="-|>" if head else "-", mutation_scale=head_scale, color=color, lw=lw,
        shrinkA=0, shrinkB=0, zorder=z, ls=(0, (4, 3)) if dashed else "-", capstyle="round",
    )
    ax.add_patch(arr)
    return arr


def bezier_point(p0, p1, t):
    (x0, y0), (x1, y1) = p0, p1
    d = 0.5 * (x1 - x0)
    P = np.array([(x0, y0), (x0 + d, y0), (x1 - d, y1), (x1, y1)])
    b = np.array([(1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3])
    return tuple(b @ P)


def straight(ax, p0, p1, color=EDGE, lw=1.5, head=True, dashed=False, z=2, head_scale=13):
    arr = FancyArrowPatch(
        p0, p1, arrowstyle="-|>" if head else "-", mutation_scale=head_scale, color=color, lw=lw,
        shrinkA=0, shrinkB=0, zorder=z, ls=(0, (4, 3)) if dashed else "-",
    )
    ax.add_patch(arr)
    return arr


def callout(ax, anchor, text_xy, text, color=RED, line_color=RED_FADED, size=15, ha="left", va="center", lw=1.1):
    """Sterling's callout: the words, joined to the thing by a plain thin line in a faded tint."""
    ax.plot([anchor[0], text_xy[0]], [anchor[1], text_xy[1]], color=line_color, lw=lw, zorder=6, solid_capstyle="round")
    ax.text(text_xy[0] + (0.06 if ha == "left" else -0.06 if ha == "right" else 0), text_xy[1], text, ha=ha, va=va,
            fontsize=size, color=color, linespacing=1.05, zorder=7)


def spread(n, lo=0.3, hi=0.7):
    return [0.5] if n == 1 else list(np.linspace(lo, hi, n))


def side_anchors():
    """Spread the edge end points along the left/right sides of every box."""
    out_count, in_count = {}, {}
    for s, d in EDGES + [(a, b) for a, b in INPUT_EDGES if INPUTS[a][3] == "right"]:
        out_count.setdefault(s, []).append(d)
        in_count.setdefault(d, []).append(s)
    pts = {}
    for key, dsts in out_count.items():
        x, y, w, h = rect_of(key)
        # order the outgoing edges by the target's row, so the curves do not cross at the source
        dsts = sorted(dsts, key=lambda k: rect_of(k)[1])
        for fr, dk in zip(spread(len(dsts)), dsts):
            pts[(key, dk, "out")] = (x + w, y + fr * h)
    for key, srcs in in_count.items():
        x, y, w, h = rect_of(key)
        srcs = sorted(srcs, key=lambda k: rect_of(k)[1])
        for fr, sk in zip(spread(len(srcs)), srcs):
            pts[(sk, key, "in")] = (x, y + fr * h)
    return pts


TONE_LINE = {"red": RED, "faint": FAINT, "normal": NODE_LINE}
TONE_TEXT = {"red": INK, "faint": LIGHT, "normal": INK}
TONE_CHIP = {"red": RED, "faint": LIGHT, "normal": INK}
TONE_EDGE = {"red": RED, "faint": FAINT, "normal": EDGE}


COST_UNITS = {"C": "per composition", "A": "per run", "L": "per build", "T": "per bar"}


def centred_runs(ax, x, y, runs, size, z=5):
    """Draw [(text, color, bold), ...] as one line centred on x (measured with the renderer)."""
    fig = ax.figure
    texts = []
    cursor = x
    for text, color, bold in runs:
        t = ax.text(cursor, y, text, ha="left", va="center", fontsize=size, color=color,
                    fontweight="bold" if bold else "normal", zorder=z)
        fig.canvas.draw()
        bb = t.get_window_extent().transformed(ax.transData.inverted())
        texts.append((t, bb.x1 - bb.x0))
        cursor = bb.x1
    total = cursor - x
    for t, _ in texts:
        px, py = t.get_position()
        t.set_position((px - total / 2, py))


def draw_network(ax, highlight=None, dim_rest=False, symbols=False, costs=True, headers=True,
                 red_edges=(), glyphs=False, bypass=True, node_size=17, header_size=20,
                 input_size=15, edge_lw=1.5, cost_units=False):
    """The network. `highlight`: node groups / input keys drawn in red; with `dim_rest`
    everything else goes faint. `red_edges`: (src, dst) pairs drawn red. Costs sit in
    the column headers: each column is one stage, and one stage is one priced action."""
    highlight = set(highlight or ())
    anchors = side_anchors()

    def tone(key):
        if key in highlight or GROUP_OF.get(key) in highlight:
            return "red"
        return "faint" if dim_rest else "normal"

    if headers:
        hy = HEADER_Y - (0.07 if cost_units else 0)
        for c in COLS:
            t = tone(c) if c in COSTS else ("faint" if dim_rest else "normal")
            name_col = {"red": RED, "faint": LIGHT, "normal": INK}[t]
            runs = [(HEADERS[c], name_col, False)]
            if costs and c in COSTS:
                runs.append(("  " + fmt_cost(COSTS[c]), name_col, True))
            centred_runs(ax, COL_X[c] + BOX_W / 2, hy, runs, header_size)
            if cost_units and c in COSTS:
                ax.text(COL_X[c] + BOX_W / 2, hy + 0.25, COST_UNITS[c], ha="center", va="center",
                        fontsize=input_size - 2, color=LIGHT if t == "faint" else GRAY, zorder=5)

    # CALPHAD group box: one $10 call returns all three outputs
    cx, cy0, _, _ = rect_of("s")
    _, cy1, _, ch = rect_of("g")
    pad = 0.11
    grp_rect = (cx - pad, cy0 - pad, BOX_W + 2 * pad, cy1 + ch - cy0 + 2 * pad + 0.26)
    gt = tone("C")
    box(ax, grp_rect, fill=None, line={"red": RED, "faint": FAINT, "normal": LIGHT}[gt], lw=1.8 if gt == "red" else 1.1,
        dashed=True, radius=0.16, z=1)
    ax.text(grp_rect[0] + grp_rect[2] - 0.12, grp_rect[1] + grp_rect[3] - 0.07, "one call", ha="right", va="bottom",
            fontsize=input_size - 2, color={"red": RED, "faint": LIGHT, "normal": GRAY}[gt], zorder=4)

    # nodes
    for key, (label, col, yc) in NODES.items():
        t = tone(key)
        x, y, w, h = rect_of(key)
        box(ax, (x, y, w, h), fill=NODE_FILL if t != "faint" else "#FAFAFA", line=TONE_LINE[t], lw=2.2 if t == "red" else 1.3)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=node_size - (1 if label.count("\n") == 2 else 0), color=TONE_TEXT[t], linespacing=1.0, zorder=5)
        if symbols:
            ax.text(x + 0.09, y + 0.06, SYMBOL[key], ha="left", va="top", fontsize=node_size - 2, fontstyle="italic",
                    color=LIGHT if t == "faint" else GRAY, zorder=5)

    # objective: a known function of strength and composition, not a GP
    t = tone("OBJ")
    x, y, w, h = rect_of("OBJ")
    box(ax, (x, y, w, h), fill=WHITE, line={"red": RED, "faint": FAINT, "normal": INK}[t], lw=1.5)
    ax.text(x + w / 2, y + h / 2, OBJ[0], ha="center", va="center", fontsize=node_size - 1, color=TONE_TEXT[t],
            linespacing=1.05, zorder=5)

    # inputs
    for key, (label, col, yc, side) in INPUTS.items():
        t = tone(key)
        x, y, w, h = rect_of(key)
        box(ax, (x, y, w, h), fill=WHITE, line={"red": RED, "faint": FAINT, "normal": LIGHT}[t],
            lw=1.8 if t == "red" else 1.1, radius=0.08)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=input_size,
                color={"red": INK, "faint": LIGHT, "normal": "#404040"}[t], linespacing=1.0, zorder=5)
        if symbols:  # corner that the centred label leaves free
            top = key == "comp"
            ax.text(x + 0.09, y + (0.05 if top else h - 0.04), INPUT_SYMBOL[key], ha="left", va="top" if top else "bottom",
                    fontsize=input_size - 2, fontstyle="italic", color=LIGHT if t == "faint" else GRAY, zorder=5)

    def edge_tone(s, d):
        if (s, d) in red_edges:
            return "red"
        if GROUP_OF.get(d) in highlight or d in highlight:
            return "red"
        return "faint" if dim_rest else "normal"

    glyph_pts = []
    for s, d in EDGES:
        p0, p1 = anchors[(s, d, "out")], anchors[(s, d, "in")]
        et = edge_tone(s, d)
        bezier(ax, p0, p1, color=TONE_EDGE[et], lw=edge_lw * (1.6 if et == "red" else 1.0), z=2.5 if et == "red" else 2)
        if glyphs and d != "OBJ":
            glyph_pts.append((*bezier_point(p0, p1, 0.5), et))

    for s, d in INPUT_EDGES:
        et = edge_tone(s, d)
        lw = edge_lw * (1.6 if et == "red" else 1.0)
        if INPUTS[s][3] == "right":
            bezier(ax, anchors[(s, d, "out")], anchors[(s, d, "in")], color=TONE_EDGE[et], lw=lw)
        else:  # vertical, from the input box up into the node
            x, y, w, h = rect_of(s)
            nx, ny, nw, nh = rect_of(d)
            straight(ax, (x + w / 2, y), (nx + nw / 2, ny + nh), color=TONE_EDGE[et], lw=lw)

    # the known, free term: composition -> objective, routed above everything
    if bypass:
        t = "faint" if dim_rest and "OBJ" not in highlight else "normal"
        col = {"normal": GRAY, "faint": FAINT}[t]
        x, y, w, h = rect_of("comp")
        ox, oy, ow, oh = rect_of("OBJ")
        pts = [(x + w * 0.5, y), (x + w * 0.5, BYPASS_Y), (ox + ow * 0.5, BYPASS_Y), (ox + ow * 0.5, oy)]
        for a, b in zip(pts[:-1], pts[1:]):
            straight(ax, a, b, color=col, lw=1.2, head=(b == pts[-1]), dashed=True, z=1, head_scale=11)
        ax.text((x + w + ox) / 2, BYPASS_Y - 0.08, "critical-mineral burden: known from the composition, costs nothing",
                ha="center", va="bottom", fontsize=input_size - (2.5 if cost_units else 1), color=col, zorder=5)

    if glyphs:
        for gx, gy, et in glyph_pts:
            posterior_glyph(ax, gx, gy, color=TONE_EDGE[et])
    return anchors


def posterior_glyph(ax, cx, cy, size=0.36, color=EDGE):
    w, h = size, size * 0.72
    box(ax, (cx - w / 2, cy - h / 2, w, h), fill=WHITE, line=color, lw=0.9, radius=0.05, z=6)
    t = np.linspace(-2.2, 2.2, 40)
    ax.plot(cx + t * (w * 0.2), cy + h * 0.3 - np.exp(-t * t) * h * 0.6, color=color, lw=1.0, zorder=7)


# --------------------------------------------------------------------------- views
# Messages are not baked into the figures (the slide headline carries them); the
# suggested headline for each view is in HEADLINES and in the README.
HEADLINES = {
    "network": "Four priced stages, six surrogate nodes: the benchmark network",
    "symbols": "Four priced stages, six surrogate nodes: the benchmark network",
    "posteriors": "One Gaussian process per node; each child sees its parents' outputs",
    "paper": "The same network the way the BOFN papers draw it",
    "paper_words": "The same network the way the BOFN papers draw it",
    "missed": "The effect a CALPHAD screen cannot see: nucleants suppress hot cracking",
    "partial_simulate": "Simulate one composition for $10; nothing has to exist first",
    "partial_atomize": "Atomize one powder lot for $1,500; it can be printed many times",
    "partial_print": "Print one build for $2,500 from a powder that exists",
    "partial_test": "Test one bar for $200 from a build that exists",
    "chain": f"Or run the whole chain for {fmt_cost(FULL_COST)}: what the full-pipeline policies buy per design",
}


def view_network(out, symbols=False, cost_units=False):
    fig, ax = new_canvas()
    draw_network(ax, symbols=symbols, cost_units=cost_units)
    fig.savefig(out)
    plt.close(fig)
    return out


def view_partial(out, group):
    """One action: the stage it evaluates (header, nodes, incoming edges, chosen input) in red, the rest faint."""
    fig, ax = new_canvas()
    chosen = {"C": {"comp"}, "A": {"a"}, "L": {"pv"}, "T": set()}[group]
    draw_network(ax, highlight={group} | chosen, dim_rest=True, bypass=False)
    fig.savefig(out)
    plt.close(fig)
    return out


def view_chain(out):
    """A full-pipeline evaluation: every stage, every input."""
    fig, ax = new_canvas()
    draw_network(ax, highlight={"C", "A", "L", "T", "comp", "a", "pv"}, dim_rest=True, bypass=False)
    fig.savefig(out)
    plt.close(fig)
    return out


def view_missed_effect(out):
    """The g -> rho edge: inoculants suppress hot cracking; a freezing-range screen cannot see it."""
    fig, ax = new_canvas()
    anchors = draw_network(ax, red_edges={("g", "rho")})
    p0, p1 = anchors[("g", "rho", "out")], anchors[("g", "rho", "in")]
    # label in the pocket under the edge, between the nucleant -> powder edge and the powder box
    lx = COL_X["A"] + BOX_W * 0.4
    t = (lx - p0[0]) / (p1[0] - p0[0])
    ex, ey = bezier_point(p0, p1, t)
    callout(ax, (ex, ey + 0.05), (lx, ey + 0.3), "nucleant suppresses\nhot cracking", ha="center", va="top", size=14.5)
    fig.savefig(out)
    plt.close(fig)
    return out


def view_posteriors(out):
    fig, ax = new_canvas()
    draw_network(ax, glyphs=True)
    fig.savefig(out)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- paper style
def view_paper(out, words=False):
    """Circles f_k, inputs x_i, outputs y_k on the edges: the convention of the BOFN papers."""
    w, h = 10.8, 6.1
    fig, ax = new_canvas(w, h)
    R = 0.42
    pos = {"s": (2.7, 1.2), "f": (2.7, 2.6), "g": (2.7, 4.0), "q": (4.9, 4.75), "rho": (6.9, 3.0), "U": (8.8, 1.8)}
    idx = {"s": 1, "f": 2, "g": 3, "q": 4, "rho": 5, "U": 6}
    for k, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), R, fc=WHITE, ec=INK, lw=1.4, zorder=3))
        ax.text(x, y, f"$f_{idx[k]}$", ha="center", va="center", fontsize=26, color=INK, zorder=4)

    def trim(p, q, r0=R, r1=R):
        (x0, y0), (x1, y1) = p, q
        d = np.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / d, (y1 - y0) / d
        return (x0 + ux * r0, y0 + uy * r0), (x1 - ux * (r1 + 0.02), y1 - uy * (r1 + 0.02)), (ux, uy)

    def edge(p, q, label=None, r0=R, r1=R):
        a, b, (ux, uy) = trim(p, q, r0, r1)
        straight(ax, a, b, color=INK, lw=1.4, head_scale=14)
        if label:  # above the midpoint, as the papers place y_k
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            nx, ny = uy, -ux  # one normal; pick the one that points up (smaller y)
            if ny > 0:
                nx, ny = -nx, -ny
            ax.text(mx + nx * 0.22, my + ny * 0.22, label, ha="center", va="center", fontsize=20, color=INK, zorder=5)

    labelled = set()
    for s_, d_ in EDGES:
        if d_ == "OBJ":
            continue
        lab = None
        if s_ not in labelled:  # one y_k per source node, on its first edge
            lab = f"$y_{idx[s_]}$"
            labelled.add(s_)
        edge(pos[s_], pos[d_], lab)
    # inputs: bare labels, as in the papers
    ax.text(0.95, 2.6, "$x_1$", ha="center", va="center", fontsize=26, color=INK)
    for k in ("s", "f", "g"):
        edge((0.95, 2.6), pos[k], r0=0.4)
    ax.text(4.9, 5.78, "$x_2$", ha="center", va="center", fontsize=26, color=INK)
    straight(ax, (4.9, 5.45), (4.9, pos["q"][1] + R + 0.02), color=INK, lw=1.4, head_scale=14)
    ax.text(6.9, 4.62, "$x_3$", ha="center", va="center", fontsize=26, color=INK)
    straight(ax, (6.9, 4.3), (6.9, pos["rho"][1] + R + 0.02), color=INK, lw=1.4, head_scale=14)
    ux, uy = pos["U"]
    straight(ax, (ux + R + 0.02, uy), (ux + R + 0.95, uy), color=INK, lw=1.4, head_scale=14)
    ax.text(ux + R + 1.05, uy, "$y_6$", ha="left", va="center", fontsize=26, color=INK)
    ax.text(w - 0.3, h - 0.5, r"objective $= y_6 - 0.3\,B(x_1)$,  $B$ known", ha="right", va="center", fontsize=18, color=GRAY)
    if words:
        s = dict(fontsize=13.5, color=GRAY, zorder=5)
        ax.text(2.7, pos["s"][1] - R - 0.12, "strengthening phase", ha="center", va="bottom", **s)
        ax.text(2.7 + R + 0.12, pos["f"][1] + 0.42, "freezing range", ha="left", va="center", **s)
        ax.text(2.7, pos["g"][1] + R + 0.12, "nucleant fraction", ha="center", va="top", **s)
        ax.text(2.7, pos["g"][1] + R + 0.42, "CALPHAD, $10 for all three", ha="center", va="top", **s)
        ax.text(4.9 + R + 0.12, pos["q"][1] + 0.3, "powder quality, $1,500", ha="left", va="center", **s)
        ax.text(6.9 + R + 0.12, pos["rho"][1] + 0.5, "dense, crack-free fraction, $2,500", ha="left", va="center", **s)
        ax.text(8.8, pos["U"][1] - R - 0.12, "strength, $200", ha="center", va="bottom", **s)
        ax.text(0.95, 2.6 + 0.42, "composition", ha="center", va="top", **s)
        ax.text(4.9 + 0.4, 5.78, "atomizer setting", ha="left", va="center", **s)
        ax.text(6.9 + 0.4, 4.62, "laser power, scan speed", ha="left", va="center", **s)
    fig.savefig(out)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- contact sheet
def contact_sheet(items, out, cols=3, label_px=44):
    from PIL import Image, ImageDraw, ImageFont

    ims = [(lab, Image.open(p).convert("RGB")) for lab, p in items]
    tw = 1200
    rows = -(-len(ims) // cols)
    scaled = []
    for lab, im in ims:
        s = tw / im.width
        scaled.append((lab, im.resize((tw, int(im.height * s)), Image.LANCZOS)))
    row_h = [max(im.height for _, im in scaled[r * cols:(r + 1) * cols]) + label_px + 20 for r in range(rows)]
    sheet = Image.new("RGB", (cols * (tw + 20) + 20, sum(row_h) + 20), "white")
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(str(Path.home() / ".local/share/fonts/aptos/Aptos-Bold.ttf"), 34)
    except OSError:
        font = ImageFont.load_default()
    y = 20
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            if i >= len(scaled):
                break
            lab, im = scaled[i]
            x = 20 + c * (tw + 20)
            d.text((x, y), lab, fill="black", font=font)
            sheet.paste(im, (x, y + label_px))
            d.rectangle([x - 1, y + label_px - 1, x + tw, y + label_px + im.height], outline="#CCCCCC")
        y += row_h[r]
    sheet.save(out, quality=88)
    return out


def flipbook(paths, out, seconds=1.6, width=1600):
    """Animated GIF that introduces the information gradually: the network, then one action at a time."""
    from PIL import Image

    frames = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
        frames.append(im.quantize(colors=64, method=Image.Quantize.MEDIANCUT))
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=int(seconds * 1000), loop=0, optimize=False)
    return out


def main():
    outs = []
    outs.append(("A1  the network, FLAIME style", view_network(HERE / "bofn_dag_network.png")))
    outs.append(("A2  with the code's node letters and cost units", view_network(HERE / "bofn_dag_network_symbols.png", symbols=True, cost_units=True)))
    outs.append(("A3  one GP per node", view_posteriors(HERE / "bofn_dag_posteriors.png")))
    outs.append(("B1  paper style (Astudillo & Frazier)", view_paper(HERE / "bofn_dag_paper_style.png")))
    outs.append(("B2  paper style with words", view_paper(HERE / "bofn_dag_paper_style_words.png", words=True)))
    outs.append(("B3  the effect the screen misses", view_missed_effect(HERE / "bofn_dag_missed_effect.png")))
    for i, (grp, slug) in enumerate((("C", "simulate"), ("A", "atomize"), ("L", "print"), ("T", "test")), 1):
        outs.append((f"C{i}  one action: {GROUP_NAMES[grp].lower()}", view_partial(HERE / f"bofn_dag_partial_{slug}.png", grp)))
    outs.append(("C5  the whole chain", view_chain(HERE / "bofn_dag_full_chain.png")))
    for lab, p in outs:
        print(lab, "->", p.name)
    contact_sheet(outs, HERE / "contact-sheet.jpg")
    print("contact sheet ->", HERE / "contact-sheet.jpg")
    seq = [HERE / "bofn_dag_network.png"] + [HERE / f"bofn_dag_partial_{s}.png" for s in ("simulate", "atomize", "print", "test")] + [HERE / "bofn_dag_full_chain.png"]
    print("flipbook ->", flipbook(seq, HERE / "bofn_dag_partial_evaluation.gif"))


if __name__ == "__main__":
    main()
