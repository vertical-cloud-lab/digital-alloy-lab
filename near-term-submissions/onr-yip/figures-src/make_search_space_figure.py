#!/usr/bin/env python3
"""Copper-alloy search space for the ONR YIP project description (blown-powder DED).

(a) Periodic-table background. The eight searched elements are filled on one
    sequential (log) scale by their upper bound in wt%, with copper as the balance.
    Red outline: on the 2025 U.S. list of critical minerals. Dashed outline: tested
    from Year 2 (no bound yet; La stands for "La or Ce"). Light gray: impurities
    not searched but capped at the welding-filler limits. Dagger: used only where Al
    is at most 3 wt% (Si above 0.1 wt% only with Nb, which needs Al at most 3 wt%). Below the colorbar, mini tiles on the same scale give the
    nominal compositions of the three reference alloys (C70600, C71500, C95800).
(b) The UNS alloys metallurgists know, at their nominal compositions in the Ni-Al
    plane, against the searched region: the designated alloys sit on its edges and
    the Cu-Ni-Al interior between the two families is open.

The design (graded periodic table plus UNS designations) follows a review
comment from Ames Laboratory.

Run:  /tmp/venv/bin/python make_search_space_figure.py
Out:  cu_search_space_periodic.pdf (vector, TrueType Times New Roman embedded) and
      cu_search_space_periodic.png (200-dpi preview), in ../figures-cu-ded/.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, LogNorm, to_hex
from matplotlib.patches import Rectangle
from matplotlib.textpath import TextToPath
from matplotlib.font_manager import FontProperties

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "figures-cu-ded" / "cu_search_space_periodic"

# ---------------------------------------------------------------------------------
# Type: Times New Roman throughout (the document's face), embedded as TrueType
# ---------------------------------------------------------------------------------
for ttf in sorted(Path("/usr/share/fonts/truetype/msttcorefonts").glob("Times_New_Roman*.ttf")):
    font_manager.fontManager.addfont(str(ttf))
plt.rcParams.update({
    "font.family": "Times New Roman",
    "mathtext.fontset": "custom",          # no math is used; keep any stray $...$ in Times
    "mathtext.rm": "Times New Roman",
    "mathtext.it": "Times New Roman:italic",
    "mathtext.bf": "Times New Roman:bold",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.size": 8,
    "axes.linewidth": 0.6,
    "lines.scale_dashes": False,           # dash patterns below are in points
})
PT = 1 / 72                                # one point, in inches

# ---------------------------------------------------------------------------------
# Color. Magnitude gets one blue ramp, light to dark (steps 150-700 of the dataviz
# reference blue), so it stays clear of the copper tile and the red outlines.
# ---------------------------------------------------------------------------------
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8984"   # primary, secondary, muted text
HAIR = "#cfcec8"                                       # neutral tile edge
COPPER = "#b87333"
RED = "#e34948"                                        # critical-mineral outline
DASH_INK = "#4a4946"                                   # Year-2 dashed outline
IMPURITY = "#e2e1dc"                                   # impurity: light gray
BLUE = ["#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
        "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
CMAP = LinearSegmentedColormap.from_list("blue150_700", BLUE)
NORM = LogNorm(vmin=0.5, vmax=30)


def _apca_y(hexcolor):
    r, g, b = (int(hexcolor[i:i + 2], 16) / 255 for i in (1, 3, 5))
    y = 0.2126729 * r ** 2.4 + 0.7151522 * g ** 2.4 + 0.0721750 * b ** 2.4
    return y if y >= 0.022 else y + (0.022 - y) ** 1.414


def apca(text, bg):
    """APCA 0.0.98G lightness contrast Lc of text on bg (negative: light on dark)."""
    t, b = _apca_y(text), _apca_y(bg)
    if abs(b - t) < 0.0005:
        return 0.0
    c = 1.14 * (b ** 0.56 - t ** 0.57 if b > t else b ** 0.65 - t ** 0.62)
    return 0.0 if abs(c) < 0.1 else 100 * (c - 0.027 if c > 0 else c + 0.027)


def ink_on(fill):
    """White or near-black label, whichever has the larger |Lc| on this fill."""
    return max(("#ffffff", INK), key=lambda t: abs(apca(t, fill)))


# ---------------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------------
# Standard 18-column layout, periods 1-6; "." is an empty cell. The lanthanide and
# actinide rows are omitted; La sits in the usual placeholder slot (period 6, group 3).
GRID = """
H  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  He
Li Be .  .  .  .  .  .  .  .  .  .  B  C  N  O  F  Ne
Na Mg .  .  .  .  .  .  .  .  .  .  Al Si P  S  Cl Ar
K  Ca Sc Ti V  Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr
Rb Sr Y  Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I  Xe
Cs Ba La Hf Ta W  Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn
"""
POS = {}                                   # symbol -> (period, group)
for period, row in enumerate(GRID.strip().splitlines(), start=1):
    cells = row.split()
    assert len(cells) == 18, row
    POS.update({s: (period, group) for group, s in enumerate(cells, start=1) if s != "."})
for s, pg in {"Cu": (4, 11), "Nb": (5, 5), "Bi": (6, 15), "Re": (6, 7), "Cd": (5, 12),
              "Zr": (5, 4), "B": (2, 13), "Ge": (4, 14), "Sn": (5, 14), "La": (6, 3)}.items():
    assert POS[s] == pg, (s, POS[s], pg)   # spot checks against a standard table

# Upper bounds (wt%) of the elements searched from the start (Table tab:space)
UPPER = {"Ni": 30, "Al": 9.5, "Fe": 4.5, "Mn": 4, "Nb": 0.8, "Cr": 0.7, "Si": 0.5, "Ti": 0.5}
CU_NI_ONLY = {"Cr", "Si", "Nb"}            # Cr, Nb only where Al <= 3 wt%; Si where Al < 7 wt% (Table 1 caption)
CRITICAL = set(UPPER) - {"Fe"}             # 2025 U.S. critical minerals (all but Fe)
YEAR2 = {"Zr", "B", "Sn", "Ge", "La"}      # tested from Year 2
IMPURITIES = {"Pb", "S", "P", "C", "Bi"}   # held at or below welding-grade limits

# UNS alloys at nominal composition: label, Ni, Al (wt%), hollow?, label offset (pt), ha
ALLOYS = [
    ("C70600", 10.0, 0.0, False, (0, -4.5), "center"),            # 90-10 Cu-Ni
    ("C72200", 16.5, 0.0, False, (0, -4.5), "center"),            # Cu-Ni-Cr
    ("C71500, C71640", 30.0, 0.0, False, (16, -4.5), "right"),    # 70-30 and its Fe-, Mn-rich grade
    ("C61400", 0.0, 7.0, False, (4.5, 0), "left"),                # aluminum bronze
    ("C95800, C63200 (NAB)", 4.45, 9.05, False, (4.5, 0), "left"),  # cast 4.5/9.0, wrought 4.4/9.1
    ("C95300", 0.0, 10.0, True, (4.5, 0), "left"),                # DED-qualified; Al > 9.5: outside
]
NI_MAX, AL_MAX, AL_CUNI = 30, 9.5, 3      # searched region and the Cu-Ni-only band

# Reference alloys at nominal composition (wt%, copper the balance), as in ../pycalphad-cu
REFERENCE = [
    ("C70600 · 90-10 Cu-Ni", [("Ni", "10"), ("Fe", "1.4"), ("Mn", "0.8")]),
    ("C71500 · 70-30 Cu-Ni", [("Ni", "30"), ("Fe", "0.6"), ("Mn", "0.6")]),
    ("C95800 · NAB", [("Al", "9.2"), ("Ni", "4.5"), ("Fe", "4.0"), ("Mn", "1.2")]),
]

# ---------------------------------------------------------------------------------
# Layout (inches). Panel (a) is drawn on an invisible axes whose data units are inches
# from the figure's lower-left corner, so tile sizes and stroke insets are exact.
# ---------------------------------------------------------------------------------
FIG_W, FIG_H = 6.5, 2.65
SPLIT = 0.63 * FIG_W                       # boundary between the panels
TOP = FIG_H - 0.19                         # top of period 1 = top of panel (b)'s axes
X0 = 0.01                                  # left edge of group 1
PITCH = (SPLIT - X0 - 0.03) / 18           # tile pitch
GAP = 0.6 * PT                             # white gap between tiles
S = PITCH - GAP                            # tile side
RED_W, DASH_W = 1.1 * PT, 0.75 * PT        # outline widths (drawn inside the tile)
SYM_PT, NUM_PT = 8, 7                      # symbol and number sizes
CAP, NUM_H = 0.662 * SYM_PT * PT, 0.676 * NUM_PT * PT   # Times cap and figure heights
LINE_GAP = 1.5 * PT                        # between number top and symbol baseline
DAGGER_RISE = 0.8 * PT                     # lift the dagger like a footnote mark

fig = plt.figure(figsize=(FIG_W, FIG_H))
axa = fig.add_axes((0, 0, SPLIT / FIG_W, 1))
axa.set(xlim=(0, SPLIT), ylim=(0, FIG_H))
axa.axis("off")


def corner(sym):
    period, group = POS[sym]
    return X0 + (group - 1) * PITCH + GAP / 2, TOP - period * PITCH + GAP / 2


def inset_box(x, y, side, lw, **kw):
    """Outline drawn wholly inside a square, so neighboring outlines never touch."""
    return Rectangle((x + lw / 2, y + lw / 2), side - lw, side - lw, fill=False,
                     lw=lw * 72, joinstyle="miter", clip_on=False, **kw)


_t2p = TextToPath()


def advance(text, size, weight="normal"):
    """Advance width of a string in inches (for placing the raised dagger)."""
    prop = FontProperties(family="Times New Roman", size=size, weight=weight)
    return _t2p.get_text_width_height_descent(text, prop, ismath=False)[0] * PT


def draw_tile(sym):
    x, y = corner(sym)
    cx = x + S / 2
    fill, edge, color, weight, sub = "#ffffff", HAIR, MUTED, "normal", None
    if sym == "Cu":
        fill, edge, color, weight, sub = COPPER, None, "#ffffff", "bold", "bal."
    elif sym in UPPER:
        fill = to_hex(CMAP(NORM(UPPER[sym])))
        edge, color, weight, sub = None, ink_on(fill), "bold", f"{UPPER[sym]:g}"
    elif sym in IMPURITIES:
        fill, edge, color = IMPURITY, None, INK2
    elif sym in YEAR2:
        edge, color = None, INK2
    axa.add_patch(Rectangle((x, y), S, S, facecolor=fill, edgecolor=edge or "none",
                            lw=0.4 if edge else 0, clip_on=False))
    if sym in CRITICAL:
        axa.add_patch(inset_box(x, y, S, RED_W, edgecolor=RED))
    if sym in YEAR2:
        axa.add_patch(inset_box(x, y, S, DASH_W, edgecolor=DASH_INK, ls=(0, (2.0, 1.2))))
    if sub is None:                        # symbol only, centered on its cap height
        axa.text(cx, y + (S - CAP) / 2, sym, ha="center", va="baseline",
                 fontsize=SYM_PT, color=color, fontweight=weight)
        return
    base = y + (S - (NUM_H + LINE_GAP + CAP)) / 2           # number baseline
    axa.text(cx, base + NUM_H + LINE_GAP, sym, ha="center", va="baseline",
             fontsize=SYM_PT, color=color, fontweight=weight)
    if sym in CU_NI_ONLY:                  # number + raised dagger, centered as a unit
        w_num, w_dag = advance(sub, NUM_PT), advance("†", NUM_PT)
        xs = cx + (w_num - w_dag) / 2
        axa.text(xs, base, sub, ha="right", va="baseline", fontsize=NUM_PT, color=color)
        axa.text(xs, base + DAGGER_RISE, "†", ha="left", va="baseline",
                 fontsize=NUM_PT, color=color)
    else:
        axa.text(cx, base, sub, ha="center", va="baseline", fontsize=NUM_PT, color=color)


for sym in POS:
    draw_tile(sym)

# Legend in the empty block above the transition metals: one row per period band.
# The longer row (impurity and the dagger note) goes in period 1, where only H and He
# sit; in period 2 it would run into B to O. The outlines go in period 2, centered
# between Be and B, and both rows start at the same x.
SW = 8.5 * PT                              # swatch side
SEP = 7 * PT                               # between the entries of a row
LEGEND = {1: [("impurity, capped (not searched)", "impurity"),
              ("only where Al ≤ 3%", "dagger")],
          2: [("2025 U.S. critical mineral", "critical"),
              ("tested from Year 2", "year2")]}


def entry_width(label):
    return SW + 3 * PT + advance(label, 7)


row2 = sum(entry_width(label) + SEP for label, _ in LEGEND[2]) - SEP
be_right, b_left = X0 + 2 * PITCH - GAP / 2, X0 + 12 * PITCH + GAP / 2
col1 = be_right + (b_left - be_right - row2) / 2


def legend_entry(xl, period, label, kind):
    yc = TOP - (period - 0.5) * PITCH      # vertical center of the period band
    xs, ys = xl, yc - SW / 2
    if kind == "dagger":
        axa.text(xs + SW / 2, yc - 0.33 * 7 * PT, "†", ha="center", va="baseline",
                 fontsize=8, color=INK)
    else:
        styles = {"critical": dict(facecolor="#ffffff", edgecolor="none"),
                  "year2": dict(facecolor="#ffffff", edgecolor="none"),
                  "impurity": dict(facecolor=IMPURITY, edgecolor="none")}
        axa.add_patch(Rectangle((xs, ys), SW, SW, lw=0, clip_on=False, **styles[kind]))
        if kind == "critical":
            axa.add_patch(inset_box(xs, ys, SW, RED_W, edgecolor=RED))
        if kind == "year2":
            axa.add_patch(inset_box(xs, ys, SW, DASH_W, edgecolor=DASH_INK, ls=(0, (2.0, 1.2))))
    axa.text(xs + SW + 3 * PT, yc - 0.33 * 7 * PT, label, ha="left", va="baseline",
             fontsize=7, color=INK)


for period, entries in LEGEND.items():
    xl = col1
    for label, kind in entries:
        legend_entry(xl, period, label, kind)
        xl += entry_width(label) + SEP

# Colorbar under the transition-metal block (groups 3-12)
cb_x0, cb_x1 = X0 + 2 * PITCH + GAP / 2, X0 + 12 * PITCH - GAP / 2
cb_top = TOP - 6 * PITCH - 0.12
cax = fig.add_axes((cb_x0 / FIG_W, (cb_top - 0.065) / FIG_H, (cb_x1 - cb_x0) / FIG_W, 0.065 / FIG_H))
cb = fig.colorbar(ScalarMappable(norm=NORM, cmap=CMAP), cax=cax, orientation="horizontal")
cb.set_ticks([0.5, 1, 3, 10, 30], labels=["0.5", "1", "3", "10", "30"])
cb.ax.minorticks_off()
cb.outline.set_visible(False)
cb.ax.tick_params(length=2.5, width=0.5, color=INK2, labelsize=7.5, labelcolor=INK, pad=1.5)
cb.set_label("Upper bound (wt%)", fontsize=8, color=INK, labelpad=2)

# Under the colorbar, across the panel: the reference alloys at nominal composition,
# each a 7 pt label over a row of mini tiles in the table's encoding (copper the
# balance, then each element filled on the upper-bound scale, with its wt%).
MS = 0.8 * S                               # mini-tile side
MSYM_PT, MNUM_PT = 6.5, 6                  # mini-tile symbol and number sizes
MCAP, MNUM_H = 0.662 * MSYM_PT * PT, 0.676 * MNUM_PT * PT
MLINE_GAP = 1.2 * PT
CARD_Y = 0.04                              # bottom of the mini tiles
LABEL_Y = CARD_Y + MS + 2.5 * PT           # card-label baseline
HEAD_Y = LABEL_Y + 9 * PT                  # heading baseline


def mini_tile(x, sym, sub, fill, color):
    axa.add_patch(Rectangle((x, CARD_Y), MS, MS, facecolor=fill, lw=0, clip_on=False))
    base = CARD_Y + (MS - (MNUM_H + MLINE_GAP + MCAP)) / 2  # number baseline
    axa.text(x + MS / 2, base + MNUM_H + MLINE_GAP, sym, ha="center", va="baseline",
             fontsize=MSYM_PT, color=color, fontweight="bold")
    axa.text(x + MS / 2, base, sub, ha="center", va="baseline", fontsize=MNUM_PT,
             color=color)


cards = [(label, [("Cu", "bal.", COPPER)]
          + [(sym, wt, to_hex(CMAP(NORM(float(wt))))) for sym, wt in elems])
         for label, elems in REFERENCE]
widths = [max(advance(label, 7), len(tiles) * (MS + GAP) - GAP) for label, tiles in cards]
x_left, x_right = X0 + GAP / 2, X0 + 18 * PITCH - GAP / 2      # groups 1 to 18
space = (x_right - x_left - sum(widths)) / (len(cards) - 1)
axa.text(x_left, HEAD_Y, "Nominal compositions (wt%)", ha="left", va="baseline",
         fontsize=7, style="italic", color=INK)
x = x_left
for (label, tiles), w in zip(cards, widths):
    axa.text(x, LABEL_Y, label, ha="left", va="baseline", fontsize=7, color=INK)
    for i, (sym, sub, fill) in enumerate(tiles):
        mini_tile(x + i * (MS + GAP), sym, sub, fill,
                  "#ffffff" if sym == "Cu" else ink_on(fill))
    x += w + space

# ---------------------------------------------------------------------------------
# Panel (b): the alloys metallurgists know, in the Ni-Al plane
# ---------------------------------------------------------------------------------
B_LEFT, B_RIGHT = SPLIT + 0.42, FIG_W - 0.06
B_BOTTOM = TOP - 1.93                      # axes 1.93 in tall, as in the 2.45 in figure
axb = fig.add_axes((B_LEFT / FIG_W, B_BOTTOM / FIG_H,
                    (B_RIGHT - B_LEFT) / FIG_W, (TOP - B_BOTTOM) / FIG_H))
# A strip below Al = 0 holds the labels of the Cu-Ni alloys that sit on that edge;
# the y spine is bounded to 0-11.5 so the axis still reads from zero.
STRIP = 12                                 # pt
h_pt = (TOP - B_BOTTOM) * 72
axb.set_xlim(0, 34)
axb.set_ylim(-STRIP * 11.5 / (h_pt - STRIP), 11.5)
for side in ("top", "right"):
    axb.spines[side].set_visible(False)
axb.spines["left"].set_bounds(0, 11.5)
axb.spines["left"].set_position(("outward", 5))
axb.spines["bottom"].set_bounds(0, 34)
for side in ("left", "bottom"):
    axb.spines[side].set_color(INK2)
axb.set_xticks([0, 10, 20, 30])
axb.set_yticks([0, 2, 4, 6, 8, 10])
axb.tick_params(length=2.5, width=0.6, color=INK2, labelsize=7.5, labelcolor=INK, pad=1.5)
axb.set_xlabel("Ni (wt%)", fontsize=8, labelpad=2)
axb.set_ylabel("Al (wt%)", fontsize=8, labelpad=3)

# Searched region (very light blue, border drawn) and the lighter Cu-Ni-only band
axb.add_patch(Rectangle((0, AL_CUNI), NI_MAX, AL_MAX - AL_CUNI, facecolor="#e3eefc", lw=0))
axb.add_patch(Rectangle((0, 0), NI_MAX, AL_CUNI, facecolor="#f3f8fe", lw=0))
axb.plot([0, NI_MAX], [AL_CUNI] * 2, color=BLUE[3], lw=0.5, solid_capstyle="butt")
axb.add_patch(Rectangle((0, 0), NI_MAX, AL_MAX, fill=False, edgecolor=BLUE[6], lw=0.8,
                        joinstyle="miter"))
axb.text(NI_MAX - 0.8, AL_CUNI - 0.25, "Al ≤ 3%: Cr†, Nb†, Si† allowed", ha="right", va="top",
         fontsize=7, color=INK2)

# Alloys: dark markers with a white ring; hollow where outside the searched region
for label, ni, al, hollow, (dx, dy), ha in ALLOYS:
    axb.plot(ni, al, "o", ms=4.6, mfc="#ffffff" if hollow else "#1a1a19",
             mec="#1a1a19" if hollow else "#ffffff", mew=0.9 if hollow else 0.7,
             zorder=5, clip_on=False)
    va = "top" if dy < 0 else "baseline"
    yoff = dy if dy < 0 else -0.5 * 0.676 * 7      # center caps on the marker
    axb.annotate(label, (ni, al), xytext=(dx, yoff), textcoords="offset points",
                 ha=ha, va=va, fontsize=7, color=INK, zorder=6)

# Family labels and the message
axb.text(23.3, 0.22, "copper-nickel", ha="center", va="baseline", fontsize=7,
         style="italic", color=INK2)
axb.annotate("nickel-aluminum bronze", (4.45, 9.05), xytext=(4.5, -11),
             textcoords="offset points", ha="left", va="baseline", fontsize=7,
             style="italic", color=INK2)
axb.text(17, 5.6, "Searched, including\nCu-Ni-Al alloys\nbetween the families", ha="center", va="center",
         fontsize=8, style="italic", color=INK, linespacing=1.15)

# Panel labels
for x, tag in ((0.0, "(a)"), (SPLIT + 0.02, "(b)")):
    fig.text(x / FIG_W, (FIG_H - 0.015) / FIG_H, tag, ha="left", va="top",
             fontsize=9, fontweight="bold", color=INK)

if __name__ == "__main__":
    fig.savefig(OUT.with_suffix(".pdf"), metadata={"CreationDate": None})
    fig.savefig(OUT.with_suffix(".png"), dpi=200)
    print("wrote", OUT.with_suffix(".pdf"), "and", OUT.with_suffix(".png"))
