"""Shop drawing of the thin-wall cup and its plug, for the top of the 4047 spread (#152, #160).

The spread's 22.5 and 30 wt% points (wf6g and k2ka in ../README.md, and Block B of the runs
plan) need more powder than the as-made cup holds.  The thin cup is the as-made cup with a
bigger hole: the same 3.000" blank faced to 2.750", but a 5/8" drill instead of 1/2" (a 1/16"
wall), closed by a .250" plug instead of a .5625" one.  Its sizes come from
../composition_spread.py, its sections from the profiles in charge_cad.py, and its plug fit
from fit_check(), so the sheet can't drift from the masses and doses in the README.  P4/P5 on
charge_parts.pdf are a different part: the short 1.25" cup for E7.

One US-Letter landscape sheet.  Printed at 100 %, the cups are 1:1 and the plug 3:1.

Usage:  python thin_cup_drawing.py      (writes drawings/thin_cup_plug.pdf and .png)
"""

from __future__ import annotations

import math
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

import charge_cad as cad
from drawings import FS, INK, INK2, OUT, View, fmt, full_outline

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import composition_spread as spread  # noqa: E402

IN = cad.IN
AIR = "#2a78d6"
POWDER = "#e9dcc3"

THIN = spread.CUPS["thin"]
L = spread.CUP_L_IN * IN  # 2.750, the as-made cup
DEPTH = spread.DEPTH_IN * IN  # 2.25 to full diameter, as on the process sheets (PR #179)
DRILL = 0.625 * IN  # 5/8" drill.  composition_spread.py allows .002" for it cutting oversize
PILOT = 0.500 * IN  # the as-made cup's 1/2" drill, here the pilot
PLUG_L = THIN["plug_l_in"] * IN
VENT = spread.VENT_D  # #60, as on the plugs made so far
AIM, LIMIT = 0.0007, 0.0010  # plug over its cup's measured bore, in
FITS = (0.0005, AIM, LIMIT, 0.0012)
POINT_IDS = {22.5: "wf6g", 30.0: "k2ka"}  # README, composition-spread table


def quill_depth_in(d: float) -> float:
    """Drill travel from first touch: depth to full diameter plus the 118 deg point."""
    return (DEPTH + cad.drill_point_h(d)) / IN


def level_z(powder_g: float) -> float:
    """Top of a tapped powder column in the thin cup, mm above the cup's base."""
    r = DRILL / 2
    cone = math.pi * r**2 * cad.drill_point_h(DRILL) / 3
    return L - DEPTH + (powder_g / spread.RHO_TAP * 1000 - cone) / (math.pi * r**2)


def full_g() -> float:
    """Tapped powder that fills the bore up to a flush plug."""
    r = DRILL / 2
    cyl = math.pi * r**2 * (DEPTH - PLUG_L)
    return (cyl + math.pi * r**2 * cad.drill_point_h(DRILL) / 3) / 1000 * spread.RHO_TAP


def shifted(profile, dz):
    return [(r, z + dz) for r, z in profile]


def leader(ax, text, tip, at, ha="left"):
    ax.annotate(text, xy=tip, xytext=at, fontsize=FS, color=INK, ha=ha, va="center", linespacing=1.2,
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.45, shrinkA=2, shrinkB=1))


def vent_arrow(ax, v, z_top):
    """Blue line up the vent and out of the top: the air the hole is for."""
    (x0, y0), (_, y1) = v.p(0, z_top - PLUG_L), v.p(0, z_top)
    ax.plot([x0, x0], [y0, y1 + 0.03], color=AIR, lw=0.9)
    ax.annotate("", xy=(x0, y1 + 0.16), xytext=(x0, y1 + 0.02),
                arrowprops=dict(arrowstyle="-|>", color=AIR, lw=0.9, mutation_scale=6))
    ax.text(x0 + 0.06, y1 + 0.15, "air out", fontsize=FS, color=AIR, ha="left", va="center")


def text_block(ax, x, y, title, lines, width_in):
    """A boxed list: bold heading, then lines at 0.111 in pitch."""
    h = 0.2 + 0.111 * len(lines)
    ax.add_patch(Rectangle((x, y - h), width_in, h, fill=False, lw=0.6, edgecolor=INK2))
    ax.text(x + 0.1, y - 0.1, title, fontsize=6.6, weight="bold", color=INK, va="center")
    for i, line in enumerate(lines):
        ax.text(x + 0.1, y - 0.22 - i * 0.111, line, fontsize=6.3, color=INK, va="center")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0.25, 0.25), 10.5, 8.0, fill=False, lw=0.9, edgecolor=INK))

    R, rb = cad.STOCK_D / 2, DRILL / 2
    cup = cad.std_cup_profile(length=L, bore=DRILL, depth=DEPTH)
    plug = cad.plug_profile(DRILL, PLUG_L, vent=VENT)
    cup_g = cad.turned(cup).volume / 1000 * cad.RHO["6063"]
    plug_g = cad.turned(plug).volume / 1000 * cad.RHO["6063"]
    ROW, T = 3.85, 7.55  # cup bases; view-title baseline

    # --- The cup, 1:1 ------------------------------------------------------
    v = View(ax, 1.95, ROW)
    v.section(cup)
    v.centreline(0, L)
    v.hdim(-R, R, L, 0.2, "Ø" + fmt(cad.STOCK_D) + " stock, as received")
    v.hdim(-rb, rb, L, 0.48, "Ø" + fmt(DRILL) + "  5/8 drill")
    v.vdim(0, L, R, 0.3, fmt(L))
    v.vdim(L - DEPTH, L, -R, -0.3, fmt(DEPTH) + "\nto full Ø")
    tip = L - DEPTH - cad.drill_point_h(DRILL)
    leader(ax, f"118° point reaches\n{quill_depth_in(DRILL):.2f} on the quill", v.p(0, tip),
           (v.p(-R, 0)[0] - 0.12, v.p(0, tip)[1] - 0.12), ha="right")
    v.title(T, "Thin cup   1:1", [f"6063-T52 · one 3.000 blank · ≈{cup_g:.0f} g",
                                  "1/16 wall (.0625): check it at the mouth, op 5"])

    # --- The plug, 3:1 -----------------------------------------------------
    v = View(ax, 5.35, 5.3, scale=3.0)
    v.section(plug)
    v.centreline(-0.5, PLUG_L + 0.5)
    vent_arrow(ax, v, PLUG_L)
    v.hdim(-rb, rb, PLUG_L, 0.42, f"Ø = its cup's bore + {AIM:.4f}".replace("0.", ".")
           + f"   (+.0005 to +{LIMIT:.4f})".replace("0.", "."))
    v.vdim(0, PLUG_L, rb, 0.3, fmt(PLUG_L))
    leader(ax, "15° × .060 lead-in:\nthe nose, goes in first", v.p(-rb + 0.35, 0.6),
           (v.p(-rb, 0)[0] - 0.15, v.p(0, 0)[1] - 0.35), ha="right")
    leader(ax, "#60 (Ø.040) hole,\nright through", v.p(VENT / 2, PLUG_L * 0.3),
           (v.p(rb, 0)[0] + 0.12, v.p(0, 0)[1] - 0.22))
    v.title(T, "Thin plug   3:1", [f"6063-T52 · one per cup · ≈{plug_g:.1f} g",
                                   "turned to fit its own cup: not interchangeable"])

    # Press fit, worked out rather than asserted (Lame + von Mises, charge_cad.fit_check)
    bore = THIN["bore_in"] * IN
    rows = [cad.fit_check(bore, cad.STOCK_D, PLUG_L, i) for i in FITS]
    verdict = {0.0005: "ok", AIM: "aim", LIMIT: "max", 0.0012: "too tight"}
    x0, y0, w = 4.15, 4.72, 3.35
    ax.add_patch(Rectangle((x0, y0 - 1.05), w, 1.05, fill=False, lw=0.6, edgecolor=INK2))
    ax.text(x0 + 0.1, y0 - 0.1, "HOW TIGHT THE PLUG CAN BE", fontsize=6.6, weight="bold", color=INK, va="center")
    cols = (x0 + 0.1, x0 + 0.78, x0 + 1.72, x0 + 2.42)
    for x, head in zip(cols, ("Over its bore", "Cup wall stress,\n× min. yield", "Press force", "")):
        ax.text(x, y0 - 0.3, head, fontsize=6.0, color=INK2, va="center", linespacing=1.1)
    for i, f in enumerate(rows):
        y = y0 - 0.5 - i * 0.12
        lo, hi = f["press_force_t"]
        bold = "bold" if f["interference_in"] == AIM else "normal"
        cells = (f"+{f['interference_in']:.4f}".replace("0.", "."), f"{f['frac_of_min_yield']:.2f}",
                 f"{lo:.1f}–{hi:.1f} t", verdict[f["interference_in"]])
        for x, c in zip(cols, cells):
            ax.text(x, y, c, fontsize=6.3, color=INK, va="center", weight=bold)
    ax.text(x0 + 0.1, y0 - 0.97, "Lamé + von Mises (fit_check() in charge_cad.py), µ 1.05–1.35",
            fontsize=5.6, color=INK2, va="center")

    # --- Filled, 1:1 (reference) ------------------------------------------
    v = View(ax, 8.55, ROW)
    al = spread.cup("thin")["al_6063_g"]
    doses = {pct: al * pct / (100 - pct) for pct, kind in spread.POINTS if kind == "thin"}
    top = max(doses.values())
    fill = cad.powder_profile(DRILL, L - DEPTH, level_z(top), point=True)
    ax.add_patch(Polygon([v.p(r, z) for r, z in full_outline(fill)], closed=True, fc=POWDER, ec="#b9a27a", lw=0,
                         hatch="...."))
    v.section(cup)
    v.section(shifted(plug, L - PLUG_L))
    v.centreline(0, L)
    vent_arrow(ax, v, L)
    for pct, g in sorted(doses.items()):
        (xl, yz), (xr, _) = v.p(-rb, level_z(g)), v.p(rb, level_z(g))
        if g != top:
            ax.plot([xl, xr], [yz, yz], color=INK, lw=0.6, ls=(0, (3, 2)))
        leader(ax, f"{g:.1f} g: {pct:g} wt% ({POINT_IDS[pct]})", (xr, yz), (xr + 0.45, yz))
    yz = v.p(0, L - PLUG_L)[1]
    leader(ax, f"≈{full_g():.0f} g fills it to the plug", v.p(rb, L - PLUG_L), (v.p(rb, 0)[0] + 0.45, yz))
    v.title(T, "Filled, plug pressed flush   1:1", ["for reference: stands plug-up in the crucible",
                                                  "levels at 1.60 g/cm³ tapped; weigh, don't fill to a line"])

    # --- How to make them ------------------------------------------------
    cup_ops = [
        "1  Face both ends of a 3.000 blank to 2.750 ±.005. Break the outside edges .020 × 45°.",
        f"2  Center drill. Drill 1/2 to {quill_depth_in(PILOT):.2f} on the quill (the pilot).",
        f"3  Drill 5/8 to {quill_depth_in(DRILL):.2f} on the quill: 2.25 deep to full Ø. Back out every 1/2 to",
        "    clear chips. Dry or light oil; no water-soluble coolant.",
        "4  Deburr the mouth, .015 max, so the plug starts square.",
        "5  Calipers on the wall at the mouth, 4 places: ≈.060. Note any reading under .050.",
        "6  Measure the bore 1/8 in from the mouth, twice 90° apart (telescoping gauge + mic).",
        "    Write the average on the record sheet: its plug is made to that number.",
        "7  Flush the bore with 99% IPA, swab, flush again. Dry 80 °C, 30 min. Weigh to 0.01 g.",
    ]
    plug_ops = [
        "1  Target Ø = its cup's average bore + .0007. Anything +.0005 to +.0010 is fine (table).",
        "2  Face the end of a blank: that face is the nose. Turn the OD to the target over .40.",
        "    Last passes .002 or less on Ø; let it cool before the last reading.",
        "3  15° lead-in on the nose, .060 long.",
        "4  Spot the center. Drill #60 (.040) .35 deep, so the part-off breaks into it.",
        "5  Part off at .250 ±.005. Deburr the top edge, .015 max. Light shows through the vent.",
        "6  Clean and weigh as for the cup. Bag it with its cup. Don't try it in the cup: it",
        "    goes in once, after filling. No files, emery, Scotch-Brite, marker or stamps.",
    ]
    fill_ops = [
        "1  Weigh the empty cup and its plug together: m.",
        f"2  Powder for 22.5 wt% ({POINT_IDS[22.5]}) = {22.5 / 77.5:.3f} × m.   For 30 wt% ({POINT_IDS[30.0]}) "
        f"= {30 / 70:.3f} × m.",
        "3  Tap it down, weigh the filled pair, then press the plug flush, nose first, in the arbor",
        "    press or a soft-jaw vise (under 0.7 t, table). It stands plug-up from then on.",
    ]
    text_block(ax, 0.45, 3.35, "THE CUP, FROM ONE 3.000 BLANK (lathe; no parting tool needed)", cup_ops, 4.75)
    text_block(ax, 5.3, 3.35, "ITS PLUG, AFTER THE CUP (lathe with a parting tool: CTB shop)", plug_ops, 5.25)
    text_block(ax, 0.45, 1.95, "FILLING AND CLOSING", fill_ops, 4.75)

    # --- Title block -------------------------------------------------------
    tb = [
        ("THIN-WALL CHARGE CUP AND PLUG, Ø3/4 6063", 9.0, "bold"),
        ("6063-T52, Ø3/4 bar (McMaster 1640T16), the 3.000 sawn blanks · OD as received", 6.3, "normal"),
        ("Inch [mm] · .XXX ±.005 unless noted · break sharp edges .005–.015", 6.3, "normal"),
        ("Cups 1:1, plug 3:1 when printed on Letter at 100 %", 6.3, "normal"),
        ("Rev A · 2026-10-27 · drawn by Claude (AI), PR #172 · checked: ________", 6.3, "normal"),
        ("Speeds and the record sheet: the process sheets, PR #179 (thin-wall variant)", 6.0, "normal"),
        ("Source: atomizer-charge/cad/thin_cup_drawing.py", 6.0, "normal"),
    ]
    ax.add_patch(Rectangle((5.3, 0.45), 5.25, 1.5, fill=False, lw=0.6, edgecolor=INK2))
    for i, (s, size, weight) in enumerate(tb):
        ax.text(5.4, 1.78 - i * 0.19, s, fontsize=size, weight=weight, color=INK if i < 5 else INK2, va="center")

    ax.text(0.45, 8.08, "Thin-wall cup and plug for the 22.5 and 30 wt% points of the 4047 spread", fontsize=12.5,
            weight="bold", color=INK, va="center")
    ax.text(0.45, 7.87, "The as-made cup (2.750 long, from a 3.000 blank) with a 5/8 hole instead of 1/2, closed by a "
            ".250 plug instead of .5625. Every part is cut through the middle; hatching is metal. #152 · #160",
            fontsize=7.0, color=INK2, va="center")

    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"thin_cup_plug.{ext}", dpi=200 if ext == "png" else None)
        print("wrote", (OUT / f"thin_cup_plug.{ext}").relative_to(pathlib.Path(__file__).resolve().parent))
    plt.close(fig)


if __name__ == "__main__":
    main()
