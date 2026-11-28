"""SOP 05 (draft): composition by ICP-OES and O/N/H by inert gas fusion, as an animated storyboard (#262, PR #263).

    xvfb-run -a python sop05_composition.py sop05_c1     # one chapter -> out/mp4/sop05_c1.mp4, out/sop05_c1.json
    python sop05_composition.py join                      # out/mp4/sop05.mp4, out/sop05.json, contact sheet, GIF
    PREVIEW=1 xvfb-run -a python sop05_composition.py sop05_c2   # last frame of each sub-step -> /tmp/preview_*.png

Chapters (one per SOP section or station):

* c1  Why it comes first: the measured composition for every Thermo-Calc / pycalphad number; EDS isn't accurate
      enough at 0.2-0.5 wt%; the AM Module's evaporation (Mg, Zn, Li); the powder's oxide.
* c2  What to send, row by row: the riffle-split powder (2-5 g, ICP-OES), powder sealed under Ar (1-2 g, O/N/H),
      a printed cube's dry-cut chips (~1 g), the feedstock (2 g), a certified reference material.
* c3  Handling: tools and containers, no paper envelopes, labels, the chain of custody in the run record (#159),
      a blind duplicate of every tenth sample, what to ask the lab, packing.
* c4  At the contract lab: digestion (HF for Si, or a fusion) and ICP-OES (Agilent 5900 + SPS 4).
* c5  At the contract lab: O, N and H by inert gas fusion (LECO ONH836).
* c6  Analysis (measured vs nominal, Scheil, evaporation loss, oxygen vs surface area) and the open questions.

Every data panel is badged: "synthetic example" (made-up numbers in the shape a lab report takes), "computed" (our
arithmetic on stated assumptions) or "illustrative". None of it is a measurement.
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import numpy as np

import stage as S
from stage import R, T

import models_chem as MC  # noqa: E402
import audit  # noqa: E402

HERE = Path(__file__).resolve().parent
ANALYSIS = HERE.parent / "analysis"
sys.path.insert(0, str(ANALYSIS))

TITLE = "SOP 05 · Composition (ICP-OES) and O/N/H (inert gas fusion)"
BH = S.BENCH_H

# ============================================================================================ panels (matplotlib)
INK, INK2, GRID = "#191919", "#666666", "#e4e4e4"
C1, C2, C3 = "#257de0", "#f47230", "#00b894"          # validated categorical slots 1-3 (dataviz skill palette)


def _fig(w=5.6, h=3.5):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5, "axes.edgecolor": "#9a9a9a",
                         "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "axes.linewidth": 0.8})
    fig = plt.figure(figsize=(w, h), dpi=150)
    fig.patch.set_facecolor("white")
    fig.patch.set_alpha(0.94)
    return fig, plt


def _badge(fig, text, color="#5a5f66"):
    fig.text(0.985, 0.975, text.upper(), ha="right", va="top", fontsize=8.5, color="white", weight="bold",
             bbox=dict(boxstyle="round,pad=0.35", fc=color, ec="none"))


def _ax_style(ax):
    ax.grid(True, color=GRID, lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def _img(fig):
    return S.fig_image(fig)


# synthetic compositions, wt% (6063 baseline powder A1; AlSi10Mg), in the shape a lab report takes
NOMINAL = {"Mg": 0.55, "Si": 0.45, "Fe": 0.20, "Cu": 0.05, "Mn": 0.05, "Zn": 0.05, "Ti": 0.05}
POWDER = {"Mg": 0.51, "Si": 0.44, "Fe": 0.17, "Cu": 0.04, "Mn": 0.03, "Zn": 0.048, "Ti": 0.02}
U_POWDER = {"Mg": 0.02, "Si": 0.02, "Fe": 0.01, "Cu": 0.005, "Mn": 0.005, "Zn": 0.005, "Ti": 0.003}
PRINT = {"Mg": 0.44, "Si": 0.44, "Fe": 0.17, "Cu": 0.04, "Mn": 0.03, "Zn": 0.039, "Ti": 0.02}


def panel_table(rows_hi: int | None):
    """The SOP's 'What to send' table, the current row highlighted."""
    rows = [("Powder, every run, 20-63 µm", "2-5 g", "ICP-OES: all + Fe, Si"),
            ("Powder, Ar-sealed in 48 h", "1-2 g", "O, N, H: gas fusion"),
            ("Printed cube, 1/alloy/build", "~1 g chips", "ICP-OES: Mg, Zn"),
            ("Feedstock: bar, master alloys", "2 g", "ICP-OES: mass balance"),
            ("Reference material (CRM)", "per lab", "the same: accuracy")]

    def fn(u):
        from PIL import Image, ImageDraw
        W, H = 760, 300
        im = Image.new("RGBA", (W, H), (255, 255, 255, 238))
        d = ImageDraw.Draw(im)
        fb, fr = S.font(20, bold=True), S.font(19)
        d.text((16, 10), "What to send (SOP 05)", font=S.font(23, bold=True), fill=(25, 25, 25))
        cols = [16, 330, 450]
        y = 48
        for c, h in zip(cols, ("Sample", "Mass", "Measure")):
            d.text((c, y), h, font=fb, fill=(102, 102, 102))
        y += 32
        for i, r in enumerate(rows):
            if rows_hi is not None and i == rows_hi:
                d.rounded_rectangle((8, y - 4, W - 8, y + 34), 6, fill=(37, 125, 224, 46), outline=(37, 125, 224, 255),
                                    width=2)
            col = (25, 25, 25) if rows_hi is None or i == rows_hi else (120, 120, 120)
            for c, t in zip(cols, r):
                d.text((c, y), t, font=fr, fill=col)
            y += 42
        d.rectangle((0, 0, W - 1, H - 1), outline=(190, 196, 204), width=2)
        return im
    return fn


def panel_eds_vs_icp(u):
    fig, plt = _fig(5.0, 3.0)
    ax = fig.add_axes([0.30, 0.22, 0.62, 0.56])
    _ax_style(ax)
    ys = [1, 0]
    ax.errorbar([0.50], [1], xerr=[[0.15], [0.15]], fmt="o", color=C2, ms=7, lw=2, capsize=5)
    ax.errorbar([0.50], [0], xerr=[[0.01], [0.01]], fmt="o", color=C1, ms=7, lw=2, capsize=5)
    ax.axvspan(0.2, 0.5, color="#f0f0f0", zorder=0)
    ax.text(0.35, 1.45, "0.2-0.5 wt%: the differences\nthe campaign needs", ha="center", fontsize=9, color=INK2)
    ax.set_yticks(ys)
    ax.set_yticklabels(["EDS (SEM)", "ICP-OES"])
    ax.set_ylim(-0.6, 1.9)
    ax.set_xlim(0.0, 0.9)
    ax.set_xlabel("Mg, wt% (± typical uncertainty)")
    fig.text(0.03, 0.92, "Why not EDS?", fontsize=12, weight="bold", color=INK)
    _badge(fig, "illustrative magnitudes")
    return _img(fig)


def panel_composition(u):
    fig, plt = _fig(5.8, 3.4)
    ax = fig.add_axes([0.0, 0.0, 1.0, 0.86])
    ax.axis("off")
    els = list(NOMINAL)
    cells = [[e, f"{NOMINAL[e]:.2f}", f"{POWDER[e]:.3f} ± {U_POWDER[e]:.3f}", f"{PRINT[e]:.3f}"] for e in els]
    tb = ax.table(cellText=cells, colLabels=["El.", "Nominal", "Powder (ICP-OES)", "Print"], loc="upper center",
                  cellLoc="center", colWidths=[0.12, 0.2, 0.36, 0.2])
    tb.auto_set_font_size(False)
    tb.set_fontsize(10)
    tb.scale(1, 1.35)
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor("#d0d0d0")
        if r == 0:
            cell.set_text_props(weight="bold", color=INK)
            cell.set_facecolor("#f3f5f8")
        if r > 0 and els[r - 1] in ("Mg", "Zn") and c in (2, 3):
            cell.set_facecolor("#fde9dc")
    fig.text(0.03, 0.93, "6063, run A1: nominal vs measured, wt%", fontsize=12, weight="bold", color=INK)
    _badge(fig, "synthetic example")
    return _img(fig)


def panel_scheil(u):
    import dsc_solidification as DS
    fig, plt = _fig(5.4, 3.4)
    ax = fig.add_axes([0.14, 0.17, 0.80, 0.66])
    _ax_style(ax)
    T = np.linspace(560, 665, 600)
    fs_nom = DS.scheil_fs(T, Tm=660.4, Tl=655.0, k=0.14, Te=577.0)
    fs_meas = DS.scheil_fs(T, Tm=660.4, Tl=656.2, k=0.14, Te=577.0)
    n = max(2, int(len(T) * min(1.0, 0.15 + u)))
    ax.plot(fs_nom[::-1][:n], T[::-1][:n], color=C1, lw=2)
    ax.plot(fs_meas[::-1][:n], T[::-1][:n], color=C2, lw=2, ls="--")
    ax.text(0.30, 652.5, "nominal", color=INK, fontsize=10)
    ax.text(0.55, 657.0, "measured", color=INK, fontsize=10)
    ax.set_xlabel("solid fraction")
    ax.set_ylabel("T, °C")
    ax.set_xlim(0, 1)
    ax.set_ylim(570, 664)
    fig.text(0.03, 0.92, "Scheil: nominal vs measured", fontsize=12, weight="bold", color=INK)
    _badge(fig, "illustrative (scheil_fs)")
    return _img(fig)


def panel_evaporation(u):
    fig, plt = _fig(5.4, 3.4)
    ax = fig.add_axes([0.14, 0.17, 0.80, 0.64])
    _ax_style(ax)
    els = ["Mg", "Zn", "Li"]
    meas = [(POWDER["Mg"] - PRINT["Mg"]) / POWDER["Mg"], (POWDER["Zn"] - PRINT["Zn"]) / POWDER["Zn"], 0.24]
    pred = [0.12, 0.21, 0.27]
    x = np.arange(3)
    k = min(1.0, u * 1.6)
    ax.bar(x - 0.19, [m * 100 * k for m in meas], 0.36, color=C2, label="measured ΔX/X")
    ax.bar(x + 0.19, [p_ * 100 * k for p_ in pred], 0.36, color=C1, label="AM Module (same P, v, hatch)")
    for i, (m, p_) in enumerate(zip(meas, pred)):
        if k > 0.95:
            ax.text(i - 0.19, m * 100 + 0.6, f"{m * 100:.0f}%", ha="center", fontsize=9, color=INK)
            ax.text(i + 0.19, p_ * 100 + 0.6, f"{p_ * 100:.0f}%", ha="center", fontsize=9, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(els)
    ax.set_ylabel("loss, % of the powder's")
    ax.set_ylim(0, 34)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.text(0.03, 0.92, "Evaporation: ΔX/X = (X_powder − X_print)/X_powder", fontsize=11, weight="bold", color=INK)
    _badge(fig, "synthetic example")
    return _img(fig)


RHO_AL, RHO_OX, T_OX = 2.70, 3.05, 4e-7          # g/cm3, g/cm3 (amorphous Al2O3, an assumption), cm (4 nm)
F_O = 3 * 15.999 / 101.961                       # mass fraction of O in Al2O3


def oxygen_ppm(d50_um):
    """Oxygen in a powder of spheres of diameter D50 with a uniform oxide skin t: w_O = 6/(rho_Al D) * t * rho_ox * f_O."""
    S_ = 6.0 / (RHO_AL * np.asarray(d50_um, float) * 1e-4)       # cm2/g
    return S_ * T_OX * RHO_OX * F_O * 1e6


def panel_oxygen(u):
    fig, plt = _fig(5.6, 3.6)
    ax = fig.add_axes([0.14, 0.30, 0.80, 0.52])
    _ax_style(ax)
    d = np.linspace(10, 80, 200)
    ax.plot(d, oxygen_ppm(d), color=C1, lw=2)
    ax.text(52, oxygen_ppm(52) + 40, "4 nm Al2O3 on spheres", color=INK, fontsize=9)
    if u > 0.4:
        ax.errorbar([38], [520], yerr=[[40], [40]], fmt="o", color=C2, ms=7, lw=2, capsize=4)
        ax.text(40.5, 540, "run A1 (synthetic):\n~1.6x the skin", color=INK, fontsize=9)
    ax.set_xlabel("D50, µm")
    ax.set_ylabel("O, ppm (wt)")
    ax.set_ylim(0, 1300)
    fig.text(0.03, 0.92, f"Oxygen vs surface area: {oxygen_ppm(38):.0f} ppm at D50 = 38 µm", fontsize=11.5,
             weight="bold", color=INK)
    fig.text(0.03, 0.06, "w_O = 6/(ρ_Al·D50) · t · ρ_ox · 3M_O/M_Al2O3;  ρ_Al 2.70, ρ_ox 3.05 g/cm³ (assumed), "
             "t = 4 nm (to check by XPS)", fontsize=8.2, color=INK2)
    _badge(fig, "computed + synthetic point")
    return _img(fig)


def panel_spectrum(u):
    fig, plt = _fig(5.4, 3.4)
    ax = fig.add_axes([0.12, 0.20, 0.38, 0.58])
    _ax_style(ax)
    wl = np.linspace(279.0, 280.6, 500)
    k = min(1.0, u * 1.5)
    peak = lambda c, a, w: a * np.exp(-0.5 * ((wl - c) / w) ** 2)
    y = 0.02 + peak(279.553, 1.0, 0.012) + peak(280.270, 0.55, 0.012) + 0.004 * np.sin(wl * 40)
    ax.plot(wl, y * k, color=C1, lw=1.6)
    ax.set_xlabel("wavelength, nm")
    ax.set_ylabel("intensity")
    ax.set_yticks([])
    ax.text(279.6, 0.95 * k, "Mg 279.553", fontsize=8.5, color=INK)
    ax2 = fig.add_axes([0.62, 0.20, 0.33, 0.58])
    _ax_style(ax2)
    c = np.array([0, 0.5, 1, 2, 5])
    ax2.plot(c, 0.2 * c, color=INK2, lw=1.4)
    ax2.plot(c, 0.2 * c, "o", color=C1, ms=5)
    if u > 0.5:
        ax2.plot([2.55], [0.51], "s", color=C2, ms=7)
        ax2.text(2.8, 0.42, "sample", fontsize=8.5, color=INK)
    ax2.set_xlabel("Mg in standard, mg/L")
    ax2.set_ylabel("net signal")
    fig.text(0.03, 0.92, "Mg emission and its calibration", fontsize=12, weight="bold", color=INK)
    _badge(fig, "synthetic example")
    return _img(fig)


def panel_digest(u):
    fig, plt = _fig(5.0, 3.1)
    ax = fig.add_axes([0.14, 0.20, 0.72, 0.60])
    _ax_style(ax)
    t = np.linspace(0, 45, 300)
    Tt = np.where(t < 15, 25 + (200 - 25) * t / 15, np.where(t < 30, 200, 200 - (175) * (t - 30) / 15))
    n = max(2, int(len(t) * u))
    ax.plot(t[:n], Tt[:n], color=C2, lw=2)
    ax.set_xlim(0, 45)
    ax.set_ylim(0, 230)
    ax.set_xlabel("time, min")
    ax.set_ylabel("vessel T, °C")
    ax.text(16, 208, "hold ~15 min at ~200 °C", fontsize=9, color=INK)
    fig.text(0.03, 0.92, "Microwave program (typical)", fontsize=12, weight="bold", color=INK)
    _badge(fig, "illustrative")
    return _img(fig)


def panel_onh(u):
    fig, plt = _fig(5.4, 3.4)
    ax = fig.add_axes([0.12, 0.20, 0.82, 0.58])
    _ax_style(ax)
    t = np.linspace(0, 60, 400)
    g = lambda c, w, a: a * np.exp(-0.5 * ((t - c) / w) ** 2) * (1 + np.tanh((t - c) / (0.6 * w))) / 2 * 2
    co = g(14, 4.0, 1.0)
    n2 = g(24, 6.0, 0.25)
    m = max(2, int(len(t) * min(1.0, u * 1.3)))
    ax.plot(t[:m], co[:m], color=C2, lw=2)
    ax.plot(t[:m], n2[:m], color=C1, lw=2)
    if u > 0.75:
        ax.text(17, 0.95, "O (as CO, CO2): IR", fontsize=9, color=INK)
        ax.text(30, 0.30, "N2: thermal conductivity", fontsize=9, color=INK)
    ax.set_xlabel("time after the drop, s")
    ax.set_ylabel("detector signal")
    ax.set_yticks([])
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 1.25)
    fig.text(0.03, 0.92, "O and N release (powder, 0.1 g)", fontsize=12, weight="bold", color=INK)
    _badge(fig, "synthetic example")
    return _img(fig)


def panel_text(title, lines, badge=None, w=760, line_h=32, wrap=None):
    def fn(u):
        from PIL import Image, ImageDraw
        H = 64 + line_h * len(lines) + 16
        im = Image.new("RGBA", (w, H), (255, 255, 255, 238))
        d = ImageDraw.Draw(im)
        d.text((18, 14), title, font=S.font(23, bold=True), fill=(25, 25, 25))
        y = 60
        for ln in lines:
            bold = ln.startswith("*")
            t = ln.lstrip("*")
            d.text((22, y), t, font=S.font(19, bold=bold), fill=(35, 35, 40) if not ln.startswith("-") else
                   (90, 94, 100))
            y += line_h
        if badge:
            f = S.font(14, bold=True)
            tw = d.textlength(badge.upper(), font=f)
            d.rounded_rectangle((w - tw - 30, 12, w - 10, 38), 7, fill=(90, 95, 102))
            d.text((w - tw - 20, 16), badge.upper(), font=f, fill=(255, 255, 255))
        d.rectangle((0, 0, w - 1, H - 1), outline=(190, 196, 204), width=2)
        return im
    return fn


# ============================================================================================ scene helpers
def put(sc, name, model, at, parent=None):
    """A small Model as its own group (named `name`), placed at `at`."""
    S.add_entries(sc, S.props(name, model), name, name, at=at, parent=parent)
    return name


def fade(sc, group, a0, a1):
    names = sc.members(group)

    def up(u):
        for n in names:
            sc.alpha[n] = a0 + (a1 - a0) * u
    return up


def show(sc, group, a):
    for n in sc.members(group):
        sc.alpha[n] = a


def pose_of(sc, group):
    return np.array(sc.world(group))


class Op:
    """The operator (people.Person) with the moves this SOP needs: walking in steps, reaching, following a held
    object."""

    def __init__(self, sc, x, y, hd=0.0):
        import people
        self.p = people.Person(sc, "op")
        self.sc = sc
        self.p.set(x=x, y=y, hd=hd, hands={"l": None, "r": None})

    def walk(self, x1, y1=None, hd_end=0.0):
        st = {}

        def up(u):
            p = self.p
            if not st:
                st.update(x=p.st["x"], y=p.st["y"], hd=p.st["hd"])
            x0, y0 = st["x"], st["y"]
            yy = y0 if y1 is None else y1
            dist = math.hypot(x1 - x0, yy - y0)
            hd_w = math.degrees(math.atan2(-(x1 - x0), (yy - y0))) if dist > 1 else st["hd"]
            if u < 0.2:
                hd = st["hd"] + (hd_w - st["hd"]) * S.ease(u / 0.2)
            elif u > 0.8:
                hd = hd_w + (hd_end - hd_w) * S.ease((u - 0.8) / 0.2)
            else:
                hd = hd_w
            amp = min(1.0, 5 * u, 5 * (1 - u))
            p.set(x=x0 + (x1 - x0) * u, y=y0 + (yy - y0) * u, hd=hd, amp=amp,
                  phase=2 * math.pi * dist * u / p.STRIDE, hands={"l": None, "r": None})
        return up

    def reach(self, side, target, lean=None, look=None, lift=90.0):
        """Move one hand from where it is to `target` (world xyz, or None: back to rest), in an arc `lift` mm high
        so it clears the bench's edge."""
        st = {}

        def up(u):
            p = self.p
            if not st:
                h = p.st["hands"][side]
                st["a"] = np.array(h if h is not None else p.rest_hand(side), float)
                st["lean"] = p.st["lean"]
            b = np.array(target if target is not None else p.rest_hand(side), float)
            pt = st["a"] + (b - st["a"]) * u + np.array([0.0, 0.0, lift * math.sin(math.pi * u)])
            kw = dict(hands={side: (None if (target is None and u >= 1.0) else tuple(pt))})
            if lean is not None:
                kw["lean"] = st["lean"] + (lean - st["lean"]) * u
            if look is not None:
                kw["look"] = look
            p.set(**kw)
        return up

    def follow(self, side, group, offset=(0.0, 0.0, 0.0)):
        """Keep a hand on `group` (at offset in the group's frame) while something else moves the group."""
        def up(u):
            M = self.sc.world(group)
            self.p.set(hands={side: tuple((M @ np.array([*offset, 1.0]))[:3])})
        return up


def mov(sc, group, b, a=None):
    """Move a group from its pose now (or a) to pose b (4x4)."""
    st = {}

    def up(u):
        if not st:
            st["a"] = np.array(sc.gmat[group] if a is None else a, float)
        sc.gmat[group] = S.blend(st["a"], np.asarray(b, float), u)
    return up


def path(sc, group, poses):
    """Move a group through poses (the first is where it is now)."""
    st = {}

    def up(u):
        if not st:
            st["p"] = [np.array(sc.gmat[group], float)] + [np.asarray(q, float) for q in poses]
        ps = st["p"]
        s_ = min(max(u, 0.0), 1.0) * (len(ps) - 1)
        i = min(int(s_), len(ps) - 2)
        sc.gmat[group] = S.blend(ps[i], ps[i + 1], s_ - i)
    return up


def gauge(sc, rows):
    def up(u):
        sc.gauges = rows
    return up


def panel_on(sc, key, fn, rect, u=0.0):
    sc.panel(key, fn, rect=rect, u=u, alpha=0.0)
    return sc.fade_panel(key, 0.0, 1.0)


def panel_off(sc, key):
    return sc.fade_panel(key, 1.0, 0.0)


def Tz(x, y, z, rz=0.0):
    return T((x, y, z)) @ R((0, 0, 1), rz)


def new_scene(name, x0, x1):
    sc = S.SOPScene(name, TITLE)
    S.room(sc, x0=x0, x1=x1)
    return sc


# ============================================================================================ our lab (c1-c3, c6)
# along the bench (x): the atomizer's powder jar and a build plate with cubes; the riffle splitter; the analytical
# balance; new vials; the argon line and the impulse sealer; the bench drill; the feedstock and the CRM; the CoC form
# and the shipper.
XJ, XR, XB, XV, XS, XD, XF, XC, XK = -1560, -1250, -930, -650, -330, 80, 420, 560, 980
YF = -380.0                                     # the bench's front edge
YOP = -640.0                                    # where the operator stands to work at the bench
YDR = -60.0                                     # the bench drill's centre (its feed handle within reach)
BAL_LIFT = 4.0                                  # the HR-202i model's feet reach 4 mm under its origin


def jar_model(fill=0.62):
    """A 250 mL wide-mouth jar (61 x 131 mm class, as the lab's), clear, black cap, grey powder."""
    import cadquery as cq  # noqa: F401
    from common import Model, cyl, tube
    m = Model("jar", "powder jar")
    m.add("jar", tube(64, 60, 112).union(cyl(64, 3)), "glass")
    m.add("powder", cyl(59, 108 * fill, z=3), "al_powder")
    m.add("cap", cyl(66, 20, z=112), "pp_black")
    m.add("label", tube(65, 64, 50, z=30).intersect(__import__("common").box(-40, -40, 0, 40, 0, 120)), "label_w")
    return m


def jar_open_model(fill=0.62):
    from common import Model, cyl, tube
    m = Model("jar_open", "powder jar, open")
    m.add("jar", tube(64, 60, 112).union(cyl(64, 3)), "glass")
    m.add("powder", cyl(59, 108 * fill, z=3), "al_powder")
    return m


def plate_model():
    """A build plate piece with four printed 10 mm cubes."""
    from common import Model, box
    m = Model("plate", "build plate with cubes")
    m.add("plate", box(-60, -45, 0, 60, 45, 12), "build_plate")
    for i, (x, y) in enumerate(((-30, -18), (0, -18), (30, -18), (-30, 15))):
        m.add(f"cube {i}", box(x - 5, y - 5, 12, x + 5, y + 5, 22), "al_part")
    return m


def envelope_model():
    from common import Model, box
    m = Model("envelope", "paper envelope")
    m.add("envelope", box(-60, -40, 0, 60, 40, 3), "kraft")
    m.add("cross", box(-70, -4, 3.2, 70, 4, 4).rotate((0, 0, 0), (0, 0, 1), 32).union(
        box(-70, -4, 3.2, 70, 4, 4).rotate((0, 0, 0), (0, 0, 1), -32)), "led_red")
    return m


def tongs_model():
    """Stainless crucible tongs / long tweezers, 200 mm, lying along x, jaws at +x."""
    from common import Model, box
    m = Model("tongs", "stainless tongs")
    m.add("tongs", box(-100, -4, 0, 95, -1.5, 2).union(box(-100, 1.5, 0, 95, 4, 2)).union(box(-100, -4, 0, -85, 4, 2)),
          "steel")
    return m


def our_lab(sc, person=True, x_op=-1250.0):
    """Build the bench (x -1900..1300) and its props; returns a dict of handles."""
    h = {}
    from lab_models import labware as LW  # noqa: F401
    import labware as LW2
    zb = BH
    h["jar"] = put(sc, "jar", jar_model(), Tz(XJ, -230, zb))
    h["plate"] = put(sc, "plate", plate_model(), Tz(XJ - 170, -80, zb))
    h["riffle"] = S.place(sc, "riffle_splitter", XR, -190)
    h["bal"] = put(sc, "balance", MC.prop_toploader(), Tz(XB, -60, zb))
    h["boat"] = put(sc, "boat", MC.prop_weigh_boat(), Tz(XB, -60 + 30, zb + 89))
    # new vials, capped, in a row; one open vial and its cap for the powder
    for i in range(3):
        put(sc, f"vialnew{i}", MC.prop_vial(label=False, fill=0.0), Tz(XV - 40 + 40 * i, 80, zb))
    h["vial"] = put(sc, "vial", MC.prop_vial_open(fill=0.0), Tz(XV, -180, zb))
    h["vialfill"] = put(sc, "vialfill", _vial_fill_model(), Tz(XV, -180, zb))
    show(sc, "vialfill", 0.0)
    h["cap"] = put(sc, "cap", MC.prop_vial_cap(), Tz(XV + 60, -200, zb))
    # the argon line: a regulator on the wall, its hose down to the nozzle on the bench
    h["reg"] = put(sc, "regulator", MC.prop_regulator(), Tz(XS - 30, 372, zb + 380) @ R((0, 0, 1), 180))
    h["nozzle"] = put(sc, "nozzle", MC.prop_ar_nozzle(), Tz(XS - 150, -130, zb + 6) @ R((0, 1, 0), 90))
    h["hose"] = LiveHose(sc, (XS - 30, 330, zb + 425), "nozzle", (0.0, 0.0, 90.0))
    h["sealer"] = S.place(sc, "heat_sealer", XS + 120, 20)
    h["bag"] = put(sc, "bag", MC.prop_bag(False), Tz(XS + 30, -250, zb))
    show(sc, "bag", 0.0)
    h["bag_sealed"] = put(sc, "bag_sealed", MC.prop_bag(True), Tz(XS + 30, -250, zb))
    show(sc, "bag_sealed", 0.0)
    h["drill"] = S.place(sc, "bench_drill", XD, YDR)
    dg = MC.drill_geom()
    h["cube"] = put(sc, "cube", MC.prop_cube(), Tz(XD + dg["bit_x"], YDR + dg["vise_y"], zb + dg["vise_top"]))
    h["boat2"] = put(sc, "boat2", MC.prop_weigh_boat(), Tz(XD - 190, -230, zb))
    h["chips2"] = put(sc, "chips2", MC.prop_chip_pile(30, 9), Tz(XD - 190, -230, zb + 1.0))
    show(sc, "chips2", 0.0)
    h["feed"] = put(sc, "feedstock", MC.prop_feedstock(), Tz(XF, -150, zb))
    h["master"] = put(sc, "master", MC.prop_master(), Tz(XF + 60, -150, zb))
    h["crm"] = put(sc, "crm", MC.prop_crm_bottle(), Tz(XC, -60, zb))
    h["coc"] = put(sc, "coc", MC.prop_coc_form(), Tz(XK - 220, -170, zb))
    h["box"] = S.place(sc, "ship_box", XK + 80, 0)
    if person:
        h["op"] = Op(sc, x_op, YOP)
    return h


def _vial_fill_model():
    from common import Model, cyl
    m = Model("vialfill", "powder in the vial")
    m.add("powder", cyl(25.6, 16, z=1.2), "al_powder")
    return m


class LiveHose:
    """The argon hose from the line's outlet to the nozzle's stub, re-drawn every frame so it follows the nozzle: a
    sagging spline, 7 mm across."""

    def __init__(self, sc, outlet, group, stub_local):
        import pyvista as pv
        self.sc, self.outlet, self.group, self.stub = sc, np.asarray(outlet, float), group, np.asarray(stub_local, float)
        self.pv = pv
        self.name = "hose/hose_black0"
        self.last = None
        sc.add(self.name, self._mesh(), S.MATS["hose_black"][:3] if S.MATS else (0.12, 0.12, 0.13), "hose",
               specular=0.2)
        sc.frame_hooks.insert(0, self)

    def _mesh(self):
        end = (self.sc.world(self.group) @ np.array([*self.stub, 1.0]))[:3]
        a = self.outlet
        mid1 = np.array([a[0], a[1] - 30, BH + 40.0])
        mid2 = np.array([(a[0] + end[0]) / 2, (a[1] + end[1]) / 2, BH + 3.5])
        pts = np.array([a, mid1, mid2, end])
        pts = pts[np.r_[True, np.linalg.norm(np.diff(pts, axis=0), axis=1) > 1.0]]
        return self.pv.Spline(pts, 60).tube(radius=3.5, n_sides=10)

    def __call__(self, sc):
        key = np.round(sc.world(self.group), 2).tobytes()
        if key != self.last:
            self.last = key
            sc.set_mesh(self.name, self._mesh())


def _hose_model(pts):
    from common import Model, hose
    m = Model("hose", "argon hose")
    m.add("hose", hose(pts, 7.0), "hose_black")
    return m


def overview_cam(x, dist=2600, az=-12, el=22, z=250):
    return S.look((x, 0, BH + z), dist=dist, az=az, el=el)


# ============================================================================================ c1: why first
def c1():
    sc = new_scene("sop05_c1", -1900, 1300)
    h = our_lab(sc, person=False)
    au = audit.Audit(sc, allow=[])
    sc.cam = overview_cam(-300, dist=3600, az=-8, el=24)
    sc.card("SOP 05 · Composition and O/N/H", [
        "ICP-OES for the alloying elements; inert gas fusion for O, N and H.",
        "Powder, printed parts and feedstock go out to a contract lab.",
        "Draft: a send-out procedure (#256 already plans \"O/ICP batch 1\")."], seconds=4.0, label="SOP 05",
        note="thermo-calc-measurements/sops/05-composition-interstitials.md (#262). Panels marked synthetic example, "
             "computed or illustrative are not measurements.")
    sc.step("Why", "Why it comes first: the model needs the measured composition",
            4.0, None, hold=1.5, cam_to=overview_cam(-900, dist=2300, az=-14, el=22),
            labels=[("atomized powder\n(run A1, 20-63 µm)", (XJ, -230, BH + 120), (0.30, 0.22)),
                    ("printed cubes\non the build plate", (XJ - 170, -80, BH + 22), (0.08, 0.30))])
    sc.step("Why 1", "Every Thermo-Calc and pycalphad number: measured composition | "
            "not the nominal one, which the atomizer and the laser change", 4.0, None, hold=2.0)
    sc.step("Why 2", "EDS isn't accurate enough at 0.2-0.5 wt% | #255 transcript, 10:36-11:29", 4.0,
            panel_on(sc, "eds", panel_eds_vs_icp, (0.67, 0.09, 0.31)), hold=2.5)
    sc.step("Why 3", "It also checks the AM Module's evaporation mode | Mg (and Zn, Li) lost between powder and print",
            4.0, panel_off(sc, "eds"), hold=2.0,
            cam_to=S.look((XJ - 170, -80, BH + 30), dist=620, az=-30, el=38),
            labels=[("10 mm cubes, as built", (XJ - 165, -95, BH + 22), (0.70, 0.30))])
    sc.step("Why 4", "And the powder's oxide | it drives lack of fusion and balling in Al", 4.0, None, hold=2.0,
            cam_to=S.look((XJ, -230, BH + 70), dist=600, az=-10, el=18),
            labels=[("every particle carries a native oxide\n(~4 nm assumed; check by XPS)", (XJ, -262, BH + 60),
                     (0.66, 0.30))])
    sc.step("Why", "So the chemistry goes out before the other measurements | "
            "ICP-OES and O/N/H of every powder, plus one print per alloy", 4.0, None, hold=1.5,
            cam_to=overview_cam(-300, dist=3200, az=-10, el=22))
    sc.save()
    au.save()


# ============================================================================================ c2: what to send
def body_fade(sc, op, a0, a1):
    """Fade the operator's body (not the gloves) for a close-up of the hands' work."""
    names = [n for n in op.p.names() if "glove" not in n]

    def up(u):
        for n in names:
            sc.alpha[n] = a0 + (a1 - a0) * u
    return up


def wpt(sc, group, local):
    return tuple((sc.world(group) @ np.array([*local, 1.0]))[:3])


def c2():
    sc = new_scene("sop05_c2", -1900, 1300)
    h = our_lab(sc, person=True, x_op=XR + 40)
    op = h["op"]
    rf = h["riffle"]
    au = audit.Audit(sc, allow=[("op/glove*", "jar/*"), ("op/glove*", "spatula/*"), ("op/glove*", "nozzle/*"),
                                ("op/glove*", "heat_sealer:arm*"), ("op/glove*", "bench_drill:*"), ("op/glove*", "crm/*"),
                                ("op/glove*", "boat/*"), ("op/glove*", "cap/*"), ("op/glove*", "bag*/*"),
                                ("nozzle/*", "bag/*"), ("bag*/*", "heat_sealer:*"), ("cube/*", "bench_drill:*"),
                                ("feedstock/*", "bench_drill:*"), ("spatula/*", "riffle_splitter:*"),
                                ("spatula/*", "boat*"), ("bench_drill:quill*", "bench_drill:body*"),
                                ("cap/*", "vial/*"), ("boat/*", "balance/*"), ("boatpowder/*", "boat/*"),
                                ("riffle_splitter:split*", "riffle_splitter:pan*"), ("riffle_splitter:feed*", "*"),
                                ("riffle_splitter:stream*", "*"), ("vialfill/*", "vial/*"), ("bag_sealed/*", "bag/*"),
                                ("hose/*", "*"), ("op/glove*", "vial*")])
    TAB = (0.665, 0.085, 0.32)
    sc.cam = overview_cam(-300, dist=3600, az=-8, el=24)
    sc.cam = overview_cam(-300, dist=3600, az=20, el=28)
    sc.step("Send", "What to send: five kinds of sample | powder, sealed powder, a printed cube, feedstock, a CRM", 4.0,
            panel_on(sc, "tab", panel_table(None), TAB), hold=2.0, cam_to=overview_cam(-700, dist=2600, az=35, el=30))
    # ---- row 1: the riffle split -------------------------------------------------------------------------------
    sc.panel("tab", panel_table(0), rect=TAB, alpha=1.0)
    jar0 = np.array(sc.gmat["jar"])
    hop = rf.world((0, 0, MCRF["hopper_rim"][2]))
    cam_r = S.look((XR - 150, -230, BH + 110), dist=1150, az=55, el=28)
    sc.step("Send 1", "Powder from every run: split the 20-63 µm cut | a riffle splitter halves it without bias",
            4.0, S.together(op.walk(XJ + 130, YOP), op.reach("r", None), body_fade(sc, op, 1.0, 0.25)), hold=1.0,
            cam_to=cam_r)
    grip = (0.0, -34.0, 60.0)                      # the jar's front, where the right hand holds it
    lift = Tz(XJ + 100, -250, BH + 120)
    over = Tz(hop[0] - 80, hop[1] - 5, hop[2] + 60)
    tilt = T((hop[0] - 15, hop[1] - 5, hop[2] + 40 - 112)) @ R((0, 1, 0), 105, pivot=(0, 0, 112))
    sc.step("Send 1", "Pour the powder into the hopper", 2.0,
            op.reach("r", wpt(sc, "jar", grip), lean=12, look=hop), hold=0.1)
    sc.step("Send 1", "Pour the powder into the hopper", 3.0,
            S.together(path(sc, "jar", [lift, over]), op.walk(XR - 170, YOP), op.follow("r", "jar", grip)), hold=0.1)
    sc.step("Send 1", "It runs through 16 chutes, half to each pan | split one half again until it is 2-5 g", 4.0,
            S.together(path(sc, "jar", [tilt]), op.follow("r", "jar", grip),
                       S.staged((0.3, 0.7, rf.move({"feed": (0, 1)})), (0.5, 1.0, rf.move({"stream": (0, 1)})),
                                (0.65, 1.0, rf.move({"split_l": (0, 1), "split_r": (0, 1)})))), hold=1.5)
    sc.step("Send 1", "It runs through 16 chutes, half to each pan | split one half again until it is 2-5 g", 3.0,
            S.together(path(sc, "jar", [over, lift, jar0]), op.walk(XJ + 130, YOP), op.follow("r", "jar", grip),
                       rf.move({"stream": (1, 0), "feed": (1, 0)})), hold=0.1)
    # weigh 2-5 g with the spatula into the boat on the balance
    spat = put(sc, "spatula", MC.prop_spatula(), Tz(XB - 170, -300, BH + 1.2) @ R((0, 0, 1), 90))
    cam_b = S.look((XB - 150, -160, BH + 90), dist=950, az=60, el=32)
    sc.step("Send 1", "Weigh 2-5 g on the balance | a stainless spatula into a weigh boat", 3.5,
            S.together(op.reach("r", None), op.walk(XB - 230, YOP), rf.move({"pan_r": (0, 1)})), hold=0.3,
            cam_to=cam_b)
    pan_r = rf.world(MCRF["pan_r_floor"], "pan_r")
    boat_c = wpt(sc, "boat", (0, 0, 0))
    sp_grip = (-60.0, 0.0, 22.0)
    rz90 = R((0, 0, 1), 90)
    pitch = R((0, 1, 0), 25)
    s_in = T((pan_r[0], pan_r[1] - 62 * math.cos(math.radians(25)), pan_r[2] + 30)) @ rz90 @ pitch
    s_up = T((pan_r[0] + 10, pan_r[1] - 80, pan_r[2] + 130)) @ rz90
    s_boat = T((boat_c[0], boat_c[1] - 62, boat_c[2] + 40)) @ rz90
    s_dump = T((boat_c[0], boat_c[1] - 62, boat_c[2] + 40)) @ rz90 @ R((1, 0, 0), 100)
    sc.step("Send 1", "Weigh 2-5 g on the balance | a stainless spatula into a weigh boat", 2.0,
            op.reach("r", wpt(sc, "spatula", sp_grip), lean=12), hold=0.1)
    sp0 = np.array(sc.gmat["spatula"])
    put(sc, "boatpowder", _boat_powder(), np.eye(4), parent="boat")
    show(sc, "boatpowder", 0.0)
    sc.step("Send 1", "Weigh 2-5 g on the balance | a stainless spatula into a weigh boat", 4.5,
            S.together(path(sc, "spatula", [s_up, s_in, s_up, s_boat, s_dump]), op.follow("r", "spatula", sp_grip),
                       S.staged((0.85, 1.0, fade(sc, "boatpowder", 0, 1)),
                                (0.85, 1.0, gauge(sc, [("balance", "3.214 g")])))), hold=1.5)
    sc.step("Send 1", "2-5 g into a new screw-cap vial | ICP-OES: all intended elements, plus Fe and Si", 2.5,
            S.together(path(sc, "spatula", [s_up, sp0]), op.follow("r", "spatula", sp_grip)), hold=0.1)
    v_c = wpt(sc, "vial", (0, 0, 0))
    b0 = np.array(sc.gmat["boat"])
    bgrip = (20.0, 0.0, 6.0)
    b_tilt = T((v_c[0] + 10, v_c[1], v_c[2] + 75)) @ R((0, 1, 0), -80, pivot=(-20, 0, 0))
    cam_v = S.look((v_c[0] - 60, v_c[1] - 20, BH + 70), dist=760, az=58, el=30)
    sc.step("Send 1", "2-5 g into a new screw-cap vial | ICP-OES: all intended elements, plus Fe and Si", 2.0,
            S.together(op.reach("r", wpt(sc, "boat", bgrip), lean=8), gauge(sc, [])), hold=0.1)
    sc.step("Send 1", "2-5 g into a new screw-cap vial | ICP-OES: all intended elements, plus Fe and Si", 4.0,
            S.together(path(sc, "boat", [T((v_c[0] + 40, v_c[1], v_c[2] + 110)) @ R((0, 1, 0), -20), b_tilt]),
                       op.walk(XV - 130, YOP), op.follow("r", "boat", bgrip),
                       S.staged((0.75, 1.0, fade(sc, "boatpowder", 1, 0)), (0.75, 1.0, fade(sc, "vialfill", 0, 1)))),
            hold=0.5, cam_to=cam_v)
    sc.step("Send 1", "Cap it", 3.0,
            S.together(path(sc, "boat", [T((v_c[0] + 40, v_c[1] - 40, v_c[2] + 110)), b0]),
                       op.walk(XV - 100, YOP), op.follow("r", "boat", bgrip)), hold=0.1)
    capg = (0.0, 0.0, 13.0)
    cap0 = wpt(sc, "cap", (0, 0, 0))
    sc.step("Send 1", "Cap it", 2.0, op.reach("r", wpt(sc, "cap", capg), lean=8), hold=0.1)
    sc.step("Send 1", "Cap it", 3.0,
            S.together(path(sc, "cap", [Tz(v_c[0], v_c[1], v_c[2] + 85), Tz(v_c[0], v_c[1], v_c[2] + 50, 170)]),
                       op.follow("r", "cap", capg)), hold=1.0)
    # ---- row 2: sealed under Ar for O/N/H --------------------------------------------------------------------
    sc.panel("tab", panel_table(1), rect=TAB, alpha=1.0)
    show(sc, "bag", 1.0)
    bag_c = wpt(sc, "bag", (0, 0, 0))
    cam_s = S.look((XS + 20, -160, BH + 80), dist=1000, az=-58, el=32)
    sc.step("Send 2", "Powder for O/N/H: 1-2 g of the same split | sealed under Ar within 48 h of atomizing", 4.0,
            S.together(op.walk(XS - 40, YOP), op.reach("r", None), gauge(sc, [("balance", "1.512 g")])), hold=1.5,
            cam_to=cam_s, labels=[("4-mil poly bag, 1.5 g of powder", (bag_c[0], bag_c[1] - 30, BH + 4), (0.12, 0.72))])
    noz0 = np.array(sc.gmat["nozzle"])
    noz_up = T((0, 0, 90)) @ noz0
    ngrip = (-20.0, 0.0, 35.0)
    tip = (bag_c[0], bag_c[1] + 50, BH + 4)
    n_in = T((tip[0], tip[1] + 30, tip[2] + 52)) @ R((1, 0, 0), -30)
    sc.step("Send 2", "Flush the bag with argon | low flow, a few seconds, from the lab's argon line", 2.0,
            S.together(gauge(sc, []), op.reach("r", wpt(sc, "nozzle", ngrip), lean=10)), hold=0.1,
            labels=[("argon regulator on the line", (XS - 30, 330, BH + 470), (0.80, 0.22))])
    sc.step("Send 2", "Flush the bag with argon | low flow, a few seconds, from the lab's argon line", 4.0,
            S.together(path(sc, "nozzle", [noz_up, n_in]), op.follow("r", "nozzle", ngrip)), hold=1.5)
    sg = MC.seal_geom()
    sx_, sy_ = XS + 120, 20
    jaw = (sx_ + 0.5 * (sg["jaw_x0"] + sg["jaw_x1"]), sy_ + sg["jaw_y"], BH + sg["jaw_z"])
    bag_seal = Tz(jaw[0], jaw[1] - 39.5, jaw[2] - 1.5)
    bg = (0.0, -46.0, 20.0)
    sc.step("Send 2", "Heat-seal it at once | an impulse sealer: a seal across the mouth", 3.0,
            S.together(path(sc, "nozzle", [noz_up, noz0]), op.follow("r", "nozzle", ngrip)), hold=0.1)
    sc.step("Send 2", "Heat-seal it at once | an impulse sealer: a seal across the mouth", 2.0,
            S.together(op.reach("l", wpt(sc, "bag", bg), lean=10), op.reach("r", None)), hold=0.1)
    sc.gmat["bag_sealed"] = np.array(sc.gmat["bag"])
    sc.step("Send 2", "Heat-seal it at once | an impulse sealer: a seal across the mouth", 3.0,
            S.together(mov(sc, "bag", bag_seal), mov(sc, "bag_sealed", bag_seal), op.follow("l", "bag", bg)), hold=0.1,
            cam_to=S.look((jaw[0] - 40, jaw[1] - 60, jaw[2]), dist=800, az=-60, el=30))
    arm_grip = tuple(h["sealer"].world((MC.SEAL["W"] / 2 - 30, 0, 104), "arm"))
    sc.step("Send 2", "Heat-seal it at once | an impulse sealer: a seal across the mouth", 3.0,
            S.together(op.reach("r", arm_grip), op.follow("l", "bag", bg),
                       S.staged((0.45, 1.0, h["sealer"].move({"arm": (1, 0)}))),
                       S.staged((0.45, 1.0, op.follow("r", "heat_sealer:arm",
                                                     (MC.SEAL["W"] / 2 - 30, 0, 104))))), hold=1.0)
    sc.step("Send 2", "Sealed: O, N and H by inert gas fusion | label it with the time it was sealed", 3.5,
            S.together(h["sealer"].move({"arm": (0, 1)}), op.follow("r", "heat_sealer:arm", (MC.SEAL["W"] / 2 - 30, 0, 104)),
                       fade(sc, "bag", 1, 0), fade(sc, "bag_sealed", 0, 1), op.follow("l", "bag_sealed", bg)), hold=0.5)
    sc.step("Send 2", "Sealed: O, N and H by inert gas fusion | label it with the time it was sealed", 2.5,
            S.together(mov(sc, "bag_sealed", Tz(XS - 10, -230, BH)), op.follow("l", "bag_sealed", bg),
                       op.reach("r", None)), hold=0.3)
    sc.step("Send 2", "Sealed: O, N and H by inert gas fusion | label it with the time it was sealed", 1.5,
            op.reach("l", None), hold=0.5)
    # ---- row 3: the printed cube, dry-cut chips ----------------------------------------------------------------
    sc.panel("tab", panel_table(2), rect=TAB, alpha=1.0)
    dr = h["drill"]
    dg = MC.drill_geom()
    handle = tuple(dr.world(dg["handle"]))
    cam_d = S.look((XD, YDR - 40, BH + 250), dist=1300, az=-55, el=22)
    sc.step("Send 3", "One printed cube per alloy per build | cut dry: no coolant, no oil", 4.0,
            S.together(op.walk(XD + 120, YOP), op.reach("r", None)), hold=1.0, cam_to=cam_d,
            labels=[("printed cube in the vise", (XD, YDR - 40, BH + 235), (0.16, 0.40))])
    sc.step("Send 3", "Drill about 1 g of chips | a clean bit, slowly", 4.5,
            S.together(op.reach("r", handle, lean=6), S.staged((0.35, 1.0, dr.move({"quill": (0, 1), "chips": (0, 1)})))),
            hold=1.0)
    sc.step("Send 3", "Chips into a new vial for ICP-OES | Mg, Zn and other volatiles: the evaporation check", 3.5,
            S.together(dr.move({"quill": (1, 0)}), fade(sc, "chips2", 0, 1), op.reach("r", None)), hold=1.5,
            labels=[("about 1 g of chips", (XD - 190, -230, BH + 8), (0.25, 0.70))])
    # ---- row 4: feedstock ------------------------------------------------------------------------------------
    sc.panel("tab", panel_table(3), rect=TAB, alpha=1.0)
    fz = Tz(XD, YDR + dg["vise_y"], BH + dg["vise_top"])
    sc.step("Send 4", "Feedstock: the bar and the master alloys, 2 g | ICP-OES: mass balance through the atomizer", 4.0,
            S.together(S.staged((0.0, 0.35, fade(sc, "cube", 1, 0)), (0.0, 0.35, dr.move({"chips": (1, 0)})),
                                (0.4, 1.0, path(sc, "feedstock", [T((0, 0, 120)) @ fz, fz])))), hold=1.0,
            labels=[("bar (the cups' and plugs' stock)", (XD, YDR - 40, BH + 245), (0.16, 0.40)),
                    ("master alloy pieces", (XF + 60, -150, BH + 9), (0.75, 0.70))])
    sc.step("Send 4", "The same: chips cut dry, into a new vial", 3.5,
            S.together(op.reach("r", handle), dr.move({"quill": (0, 1), "chips": (0, 1)})), hold=1.0)
    sc.step("Send 4", "The same: chips cut dry, into a new vial", 2.0,
            S.together(dr.move({"quill": (1, 0)}), op.reach("r", None)), hold=0.5)
    # ---- row 5: a CRM ----------------------------------------------------------------------------------------
    sc.panel("tab", panel_table(4), rect=TAB, alpha=1.0)
    crm_grip = (0.0, -30.0, 60.0)
    sc.step("Send 5", "A certified reference material of a similar alloy | e.g. Al casting alloy 356 millings",
            4.0, S.together(op.walk(XC - 40, YOP), op.reach("r", None)), hold=1.0,
            cam_to=S.look((XC - 150, -120, BH + 120), dist=1100, az=-55, el=25),
            labels=[("certified reference\nmaterial (chips)", (XC, -60, BH + 100), (0.75, 0.40))])
    sc.step("Send 5", "It goes with the samples, under its own ID | the lab's accuracy check", 2.0,
            op.reach("r", wpt(sc, "crm", crm_grip), lean=8), hold=0.1)
    sc.step("Send 5", "It goes with the samples, under its own ID | the lab's accuracy check", 3.0,
            S.together(path(sc, "crm", [Tz(XC - 40, -160, BH + 60), Tz(XC - 60, -260, BH)]),
                       op.follow("r", "crm", crm_grip)), hold=0.2)
    sc.step("Send", "Five kinds of sample, each in a new container", 3.5,
            S.together(op.reach("r", None), panel_off(sc, "tab"), body_fade(sc, op, 0.25, 1.0)), hold=2.0,
            cam_to=overview_cam(-300, dist=3400, az=-30, el=30))
    sc.save()
    au.save()


def _boat_powder():
    from common import Model, cyl
    m = Model("boatpowder", "powder in the boat")
    m.add("powder", cyl(18, 3, z=0.5), "al_powder")
    return m


try:
    from models_dsc import RIFFLE_POINTS as MCRF
except Exception:                      # noqa: BLE001
    MCRF = dict(hopper_rim=(0.0, 0.0, 150.0), pan_l_floor=(-38.0, 0.0, 0.8), pan_r_floor=(38.0, 0.0, 0.8))


# ============================================================================================ c3: handling
def label_panel(u):
    from PIL import Image, ImageDraw
    W, H = 640, 330
    im = Image.new("RGBA", (W, H), (255, 255, 255, 240))
    d = ImageDraw.Draw(im)
    d.text((18, 12), "The label (example)", font=S.font(23, bold=True), fill=(25, 25, 25))
    d.rounded_rectangle((20, 56, W - 20, H - 20), 10, fill=(252, 252, 248), outline=(60, 60, 60), width=3)
    rows = [("Run ID", "A1-6063-2026-11-12"), ("Sieve cut", "20-63 µm"), ("Atomized", "2026-11-12"),
            ("Sealed", "2026-11-13 10:40 (Ar)"), ("Analytes", "ICP-OES: Al Mg Si Fe Cu Mn Zn Ti"),
            ("Sample", "S-07 of 10")]
    y = 72
    for k, v in rows:
        d.text((40, y), k, font=S.font(18, bold=True), fill=(70, 70, 70))
        d.text((200, y), v, font=S.font(18), fill=(20, 20, 20))
        y += 38
    f = S.font(13, bold=True)
    d.rounded_rectangle((W - 196, 14, W - 12, 40), 7, fill=(90, 95, 102))
    d.text((W - 186, 18), "SYNTHETIC EXAMPLE", font=f, fill=(255, 255, 255))
    return im


def coc_panel(u):
    from PIL import Image, ImageDraw
    W, H = 760, 300
    im = Image.new("RGBA", (W, H), (255, 255, 255, 240))
    d = ImageDraw.Draw(im)
    d.text((18, 12), "Run record #159: chain of custody", font=S.font(23, bold=True), fill=(25, 25, 25))
    cols = [20, 120, 330, 520]
    hdr = ["Sample", "Released by", "Received by", "Date"]
    rows = [["S-01..10", "atomizer operator", "lab manager", "2026-11-13"],
            ["S-01..10", "lab manager", "courier", "2026-11-14"],
            ["S-01..10", "courier", "contract lab", "2026-11-16"]]
    y = 60
    for c, t in zip(cols, hdr):
        d.text((c, y), t, font=S.font(18, bold=True), fill=(102, 102, 102))
    y += 36
    for r in rows:
        for c, t in zip(cols, r):
            d.text((c, y), t, font=S.font(18), fill=(25, 25, 25))
        y += 40
    d.text((20, y + 6), "roles only: a signature and time at every hand-over", font=S.font(16), fill=(110, 110, 110))
    f = S.font(13, bold=True)
    d.rounded_rectangle((W - 196, 14, W - 12, 40), 7, fill=(90, 95, 102))
    d.text((W - 186, 18), "SYNTHETIC EXAMPLE", font=f, fill=(255, 255, 255))
    return im


def dup_panel(u):
    from PIL import Image, ImageDraw
    W, H = 640, 250
    im = Image.new("RGBA", (W, H), (255, 255, 255, 240))
    d = ImageDraw.Draw(im)
    d.text((18, 12), "Blind duplicates", font=S.font(23, bold=True), fill=(25, 25, 25))
    ids = [f"S-{k:02d}" for k in range(1, 11)]
    for i, s in enumerate(ids):
        x = 20 + (i % 5) * 120
        y = 60 + (i // 5) * 56
        hi = s == "S-10"
        d.rounded_rectangle((x, y, x + 104, y + 42), 6, fill=(253, 233, 220) if hi else (243, 245, 248),
                            outline=(244, 114, 48) if hi else (200, 200, 200), width=2)
        d.text((x + 18, y + 10), s, font=S.font(18, bold=hi), fill=(25, 25, 25))
    d.text((20, 186), "S-10 is a second split of S-03 under its own ID:", font=S.font(17), fill=(60, 60, 60))
    d.text((20, 212), "the key stays in the run record, not on the form", font=S.font(17), fill=(60, 60, 60))
    f = S.font(13, bold=True)
    d.rounded_rectangle((W - 196, 14, W - 12, 40), 7, fill=(90, 95, 102))
    d.text((W - 186, 18), "SYNTHETIC EXAMPLE", font=f, fill=(255, 255, 255))
    return im


def c3():
    sc = new_scene("sop05_c3", -1900, 1300)
    h = our_lab(sc, person=True, x_op=XV - 100)
    op = h["op"]
    # the state at the end of c2: the vial filled and capped, the bag sealed, the chips in the boat, the CRM forward
    show(sc, "vialfill", 1.0)
    vc = (sc.world("vial") @ np.array([0, 0, 0, 1.0]))[:3]
    sc.gmat["cap"] = Tz(vc[0], vc[1], vc[2] + 50)
    sc.gmat["bag_sealed"] = Tz(XS - 10, -200, BH)
    show(sc, "bag_sealed", 1.0)
    show(sc, "chips2", 1.0)
    sc.gmat["crm"] = Tz(XC - 120, -150, BH)
    env = put(sc, "envelope", envelope_model(), Tz(XV - 260, -200, BH))
    show(sc, "envelope", 0.0)
    au = audit.Audit(sc, allow=[("op/glove*", "vial*"), ("op/glove*", "coc/*"), ("op/glove*", "pen/*"),
                                ("vial*/*", "ship_box:*"), ("bag_sealed/*", "ship_box:*"), ("cap/*", "vial/*"),
                                ("pen/*", "coc/*")])
    sc.cam = overview_cam(-300, dist=3400, az=-8, el=24)
    cam_t = S.look((XV - 80, -120, BH + 60), dist=950, az=-10, el=30)
    spat = put(sc, "spatula", MC.prop_spatula(), Tz(XV - 180, -100, BH))
    sc.step("Handling", "Clean, dry plastic or stainless tools | new screw-cap vials, or heat-sealed bags flushed with Ar",
            4.5, None, hold=1.5, cam_to=cam_t,
            labels=[("stainless spatula", (XV - 180, -100, BH + 2), (0.12, 0.30)),
                    ("new HDPE screw-cap vial", (vc[0], vc[1], BH + 60), (0.62, 0.25)),
                    ("heat-sealed bag (Ar)", (XS - 10, -200, BH + 3), (0.80, 0.62))])
    sc.step("Handling", "No paper envelopes | only sealed vials or bags", 4.0, fade(sc, "envelope", 0, 1), hold=1.5,
            labels=[("paper envelope: no", (XV - 260, -200, BH + 4), (0.14, 0.62))])
    sc.step("Labels", "Label every container | run ID, sieve cut, date atomized, date sealed, analytes", 4.5,
            S.together(fade(sc, "envelope", 1, 0), panel_on(sc, "label", label_panel, (0.60, 0.10, 0.36))), hold=2.5,
            cam_to=S.look((vc[0], vc[1], BH + 40), dist=420, az=-5, el=14))
    pen = put(sc, "pen", _pen_model(), Tz(XK - 160, -230, BH + 3.5) @ R((0, 0, 1), 30))
    coc_c = (sc.world("coc") @ np.array([0, 0, 0, 1.0]))[:3]
    sc.step("Custody", "Log each sample in the run record (#159) | with its chain of custody", 4.0,
            S.together(panel_off(sc, "label"), op.walk(XK - 250), op.reach("r", None)), hold=0.5,
            cam_to=S.look((XK - 220, -170, BH + 60), dist=900, az=-12, el=35))
    pgrip = (0.0, 0.0, 8.0)
    sc.step("Custody", "Log each sample in the run record (#159) | with its chain of custody", 4.0,
            S.together(panel_on(sc, "coc", coc_panel, (0.56, 0.10, 0.42)),
                       S.staged((0.0, 0.3, op.reach("r", (sc.world("pen") @ np.array([*pgrip, 1.0]))[:3], lean=15)),
                                (0.3, 1.0, path(sc, "pen", [Tz(coc_c[0] - 40, coc_c[1] + 40, BH + 12) @ R((0, 0, 1), 30),
                                                             Tz(coc_c[0] + 40, coc_c[1] + 20, BH + 12) @ R((0, 0, 1), 30),
                                                             Tz(coc_c[0] - 40, coc_c[1], BH + 12) @ R((0, 0, 1), 30)])),
                                (0.3, 1.0, op.follow("r", "pen", pgrip)))), hold=1.5)
    # ten vials: the blind duplicate
    sc.step("Duplicates", "A blind duplicate of every tenth sample | a second split under its own ID", 4.5,
            S.together(panel_off(sc, "coc"), panel_on(sc, "dup", dup_panel, (0.60, 0.10, 0.36)), op.reach("r", None)),
            hold=2.5)
    ask = panel_text("Ask the lab for", [
        "the ICP-AES/OES method for Al alloys",
        "-   Edison q2 names ASTM E3061",
        "method detection limits",
        "the digestion: Si-bearing Al needs HF or a fusion",
        "-   to keep Si in solution (the open question in #255)",
        "the uncertainty of each element"], badge=None, w=760)
    sc.step("Ask the lab", "Ask the lab for its method, limits and digestion | and the uncertainty of each element", 5.0,
            S.together(panel_off(sc, "dup"), panel_on(sc, "ask", ask, (0.56, 0.10, 0.42))), hold=3.0)
    # pack: the vial, the sealed bag and the CRM into the shipper's foam
    bx = h["box"]
    sc.step("Pack", "Pack the vials and bags in the foam | the CoC form goes in the box", 3.5,
            S.together(panel_off(sc, "ask"), op.walk(XK - 50), bx.move({"lid": (1, 1)})), hold=0.3,
            cam_to=S.look((XK + 60, -80, BH + 80), dist=1100, az=-10, el=35))
    slot_v = bx.world((-90, -40, 25))
    slot_b = bx.world((0, 50, 25))
    sc.gmat["vial"] = Tz(slot_v[0] - 300, slot_v[1] - 120, BH)
    sc.gmat["vialfill"] = sc.gmat["vial"]
    sc.gmat["cap"] = sc.gmat["vial"] @ T((0, 0, 50))
    vg = (0.0, -16.0, 40.0)
    sc.step("Pack", "Pack the vials and bags in the foam | the CoC form goes in the box", 2.0,
            op.reach("r", (sc.world("vial") @ np.array([*vg, 1.0]))[:3], lean=12), hold=0.1)
    sc.parent["vialfill"] = "vial"
    sc.gmat["vialfill"] = np.eye(4)
    sc.parent["cap"] = "vial"
    sc.gmat["cap"] = T((0, 0, 50))
    sc.step("Pack", "Pack the vials and bags in the foam | the CoC form goes in the box", 3.0,
            S.together(path(sc, "vial", [Tz(slot_v[0], slot_v[1], BH + 120), Tz(slot_v[0], slot_v[1], slot_v[2])]),
                       op.follow("r", "vial", vg)), hold=0.3)
    sc.step("Pack", "Close the shipper | it leaves with the form; the run record logs it", 3.5,
            S.together(op.reach("r", None), bx.move({"lid": (1, 0)})), hold=2.0)
    sc.save()
    au.save()


def _pen_model():
    from common import Model, cyl
    m = Model("pen", "pen")
    m.add("pen", cyl(9, 140).rotate((0, 0, 0), (0, 1, 0), 90).translate((-70, 0, 4.5)), "pp_blue")
    return m


# ============================================================================================ c4: digest + ICP-OES
def c4():
    sc = new_scene("sop05_c4", -650, 2300)
    au = audit.Audit(sc, allow=[("op/glove*", "*vessel*"), ("op/glove*", "acid*"), ("op/glove*", "tube50*"),
                                ("op/glove*", "microwave_digester:door*"), ("op/glove*", "icp_oes:door*"),
                                ("*vessel*/*", "microwave_digester:*"), ("tube50*/*", "icp_oes:*"),
                                ("icp_oes:sps_probe*", "icp_oes:tubes*"), ("acid*/*", "*vessel*"),
                                ("icp_oes:torch*", "icp_oes:body*"), ("icp_oes:plasma*", "icp_oes:torch*"),
                                ("icp_oes:beam*", "*")])
    hood = S.place(sc, "fumehood", -1320, -100, z=0)
    mw = S.place(sc, "microwave_digester", -230, 40)
    icp = S.place(sc, "icp_oes", 780, 0)
    g = MC.icp_geom()
    mg = MC.mars_geom()
    op = Op(sc, -1250, -1050)
    op.p.set(hd=0)
    sc.cam = S.look((150, 0, BH + 300), dist=4600, az=-8, el=18)
    sc.card("At the contract lab: digestion and ICP-OES", [
        "What the lab does with the vials: its own validated method (ask for it).",
        "Typical steps for Al alloys, shown with an Agilent 5900 and a CEM MARS 6."],
        seconds=3.5, label="Lab", note="Masses, acids and programs here are typical, not the lab's: ask for theirs.")
    sc.step("Lab", "At the contract lab: digest, then ICP-OES | ASTM E3061: ICP-AES/OES for Al alloys", 4.5, None,
            hold=1.0, cam_to=S.look((-500, 0, BH + 300), dist=3600, az=-8, el=18),
            labels=[("fume hood", (-1320, -480, 1500), (0.10, 0.20)), ("CEM MARS 6", (-230, -300, BH + 660), (0.38, 0.18)),
                    ("Agilent 5900 ICP-OES\n+ SPS 4 autosampler", (780, -370, BH + 625), (0.70, 0.18))])
    # weigh into the vessel and add acids, in the hood
    ws = 932.0                                        # the hood's work surface (byu-vcl's fumehood: 900 + 32)
    vx, vy = -1320, -250
    ves = put(sc, "vessel", MC.prop_digest_vessel(open_=True), Tz(vx, vy, ws))
    acid = put(sc, "acid", MC.prop_bottle("pp_white", 70, 150), Tz(vx + 250, -150, ws))
    cam_h = S.look((vx + 80, -250, ws + 120), dist=1200, az=-8, el=18)
    sc.step("Digest", "Weigh ~0.2 g of powder or chips into a TFM vessel | typical: the lab's method sets the mass",
            4.0, S.together(op.walk(-1300, -800)), hold=1.5, cam_to=cam_h,
            labels=[("TFM vessel in its sleeve", (vx, vy - 20, ws + 112), (0.25, 0.35))])
    agrip = (0.0, -36.0, 90.0)
    sc.step("Digest", "Acids, in the hood: HCl and HNO3, with HF for Si | or a fusion: Si stays in solution", 2.5,
            op.reach("r", (sc.world("acid") @ np.array([*agrip, 1.0]))[:3], lean=10), hold=0.1)
    pour = Tz(vx + 60, vy - 10, ws + 200) @ R((0, 1, 0), -100, pivot=(0, 0, 150))
    sc.step("Digest", "Acids, in the hood: HCl and HNO3, with HF for Si | or a fusion: Si stays in solution", 4.0,
            S.together(path(sc, "acid", [Tz(vx + 150, vy - 40, ws + 120), pour]), op.follow("r", "acid", agrip)),
            hold=1.0)
    sc.step("Digest", "Acids, in the hood: HCl and HNO3, with HF for Si | or a fusion: Si stays in solution", 3.0,
            S.together(path(sc, "acid", [Tz(vx + 150, vy - 40, ws + 120), Tz(vx + 250, -150, ws)]),
                       op.follow("r", "acid", agrip)), hold=0.3)
    # the vessel into the microwave
    sc.step("Digest", "Cap the vessel; into the microwave | sealed vessels, many at a time", 4.0,
            S.together(op.reach("r", None), op.walk(-230 - 60, -700), mw.move({"door": (0, 1)})), hold=0.5,
            cam_to=S.look((-230, -100, BH + 250), dist=1500, az=-12, el=18))
    car = (mg["cx"] - 230 + 130, mg["cy"] + 40, BH + mg["cz"] + 10)
    sc.step("Digest", "Ramp to ~200 °C and hold | typical program; then cool", 4.5,
            S.together(mw.move({"door": (1, 0), "carousel": (0, 1), "vessels": (0, 1)}),
                       panel_on(sc, "mw", panel_digest, (0.60, 0.10, 0.36)), sc.drive_panel("mw", 0, 1)), hold=2.0)
    tb = put(sc, "tube50", MC.prop_tube50(0.8), Tz(-60, -260, BH))
    show(sc, "tube50", 0.0)
    sc.step("Digest", "Vent in the hood, dilute to 50 mL | boric acid ties up the fluoride if HF was used", 4.0,
            S.together(panel_off(sc, "mw"), fade(sc, "tube50", 0, 1)), hold=1.5,
            labels=[("50 mL PP tube", (-60, -260, BH + 120), (0.35, 0.40))])
    # the ICP-OES: the tube into the SPS 4 rack, then the probe takes it up
    tgt = g["tgt"]
    tube_pos = Tz(780 + tgt[0], tgt[1], BH + 66.0)
    tg = (0.0, -15.0, 80.0)
    sc.step("ICP-OES", "The tubes go in the autosampler's racks | blank, standards, samples, the CRM, duplicates", 3.0,
            S.together(op.walk(780 + g["sps_x"] - 220, -650), op.reach("r", None)), hold=0.2,
            cam_to=S.look((780 + 300, -150, BH + 250), dist=2000, az=-10, el=20))
    sc.gmat["tube50"] = Tz(780 + g["sps_x"] - 420, -300, BH + 0.0)
    sc.step("ICP-OES", "The tubes go in the autosampler's racks | blank, standards, samples, the CRM, duplicates", 2.0,
            op.reach("r", (sc.world("tube50") @ np.array([*tg, 1.0]))[:3], lean=10), hold=0.1)
    sc.step("ICP-OES", "The tubes go in the autosampler's racks | blank, standards, samples, the CRM, duplicates", 3.5,
            S.together(path(sc, "tube50", [Tz(780 + tgt[0], tgt[1], BH + 300), tube_pos]), op.follow("r", "tube50", tg)),
            hold=0.5)
    pr_path = icp.inst.joints["sps_probe"].path
    yseg = abs(pr_path[1][1])
    k_y = yseg / (yseg + abs(pr_path[2][2]))
    cam_icp = S.look((780 + 100, -150, BH + 330), dist=1800, az=-14, el=14)
    sc.step("ICP-OES", "The probe takes up the sample | a peristaltic pump feeds the nebulizer", 4.5,
            S.together(op.reach("r", None), op.walk(780 - 300, -900),
                       S.staged((0.0, 0.5, icp.move({"sps_arm": (0, 1), "sps_probe": (0, k_y)})),
                                (0.5, 1.0, icp.move({"sps_probe": (k_y, 1.0)}))),
                       icp.move({"pump_rotor": (0, 1)})), hold=0.5, cam_to=cam_icp,
            labels=[("peristaltic pump", (780 + g["px"], g["yf"], g["pzp"] + BH), (0.20, 0.75))])
    tx, ty = 780 + g["tx"], g["ty"]
    cam_t = S.look((tx, ty - 40, BH + g["zs"] + 120), dist=780, az=-12, el=8)
    sc.step("ICP-OES", "Nebulizer and spray chamber make a fine mist | only the finest droplets reach the torch", 4.5,
            S.together(icp.move({"pump_rotor": (1, 2), "door": (0, 1)})), hold=1.0, cam_to=cam_t,
            labels=[("concentric nebulizer", (tx + 60, ty - 14, BH + g["sz"] + 52), (0.80, 0.82)),
                    ("cyclonic spray chamber", (tx - 23, ty, BH + g["sz"] + 30), (0.18, 0.82)),
                    ("vertical quartz torch", (tx - 10, ty, BH + g["tz0"] + 120), (0.18, 0.40))])
    icp.set(**{"~shell": 0.0})
    sc.step("ICP-OES", "The argon plasma, about 6,000-10,000 K | each element emits at its own wavelengths", 4.5,
            S.together(icp.move({"plasma": (0, 1), "pump_rotor": (2, 3), "~shell": (0, 1)})), hold=1.5,
            labels=[("load coil (RF)", (tx + 17, ty, BH + g["tz0"] + 185), (0.80, 0.40)),
                    ("plasma", (tx, ty, BH + g["pz"] + 40), (0.20, 0.30))])
    sc.step("ICP-OES", "Two views: radial and axial | axial for low levels, radial for the majors", 4.5,
            S.together(icp.move({"beam": (0, 1), "pump_rotor": (3, 4)})), hold=1.5,
            labels=[("radial view", (tx + 80, ty, BH + g["rz"]), (0.80, 0.30)),
                    ("axial view", (tx, ty, BH + g["zs"] + 260), (0.30, 0.18))])
    sc.step("ICP-OES", "Line intensities against standards give wt% | Mg 279.553 nm shown; Si 251.611, Fe 238.204", 5.0,
            S.together(panel_on(sc, "spec", panel_spectrum, (0.58, 0.10, 0.40)), sc.drive_panel("spec", 0, 1),
                       icp.move({"pump_rotor": (4, 5)})), hold=2.5)
    res = panel_text("The lab's report", [
        "wt% of each element with its uncertainty",
        "method detection limits",
        "the digestion used, and how Si was kept",
        "QC: blank, CRM recovery, duplicate agreement"], badge=None, w=720)
    sc.step("ICP-OES", "The report: wt% with uncertainty and detection limits | and the CRM's recovery", 4.5,
            S.together(panel_off(sc, "spec"), panel_on(sc, "res", res, (0.58, 0.10, 0.40)),
                       icp.move({"~shell": (1, 0), "door": (1, 0), "plasma": (1, 1), "beam": (1, 0)})), hold=2.5,
            cam_to=S.look((780 + 200, -100, BH + 300), dist=2400, az=-10, el=16))
    sc.save()
    au.save()


# ============================================================================================ c5: O/N/H
def c5():
    sc = new_scene("sop05_c5", -1100, 900)
    au = audit.Audit(sc, allow=[("op/glove*", "tongs/*"), ("op/glove*", "capsule/*"), ("tongs/*", "newcru/*"),
                                ("tongs/*", "onh_analyzer:*"), ("newcru/*", "onh_analyzer:*"),
                                ("capsule/*", "onh_analyzer:*"), ("onh_analyzer:crucible*", "onh_analyzer:body*"),
                                ("onh_analyzer:glow*", "onh_analyzer:*"), ("onh_analyzer:sample*", "onh_analyzer:*"),
                                ("onh_analyzer:gas*", "*"), ("op/glove*", "onh_analyzer:*")])
    onh = S.place(sc, "onh_analyzer", 150, 0)
    g = MC.onh_geom()
    import labware as LW2
    bal = put(sc, "balance", LW2.balance_hr202i(), Tz(-650, 30, BH))
    tray = put(sc, "tray", _tray_model(), Tz(-330, -150, BH))
    tongs = put(sc, "tongs", tongs_model(), Tz(-330 + 150, -260, BH))
    cap = put(sc, "capsule", MC.prop_capsule_basket(), Tz(-650, 30 - 214 + 163, BH + 50))
    op = Op(sc, -400, -760)
    fx, fy = 150 + g["fx"], g["fy"]
    sc.cam = S.look((-100, 0, BH + 350), dist=3600, az=-10, el=18)
    sc.card("At the contract lab: O, N and H", ["Inert gas fusion: the sample melts in a graphite crucible;",
                                                 "O leaves as CO, N as N2, H as H2, swept to the detectors."],
            seconds=3.5, label="O/N/H", note="Masses, flux and power settings are typical: the lab's method sets them.")
    sc.step("O/N/H", "O, N and H by inert gas fusion | a LECO ONH836-class analyzer", 4.0, None, hold=1.0,
            cam_to=S.look((0, 0, BH + 350), dist=2600, az=-12, el=16),
            labels=[("LECO ONH836", (150 - g["W"] / 2, g["yf"], BH + g["H"] * 0.9), (0.40, 0.15)),
                    ("loading head", (fx, fy, BH + g["hz1"] + 20), (0.85, 0.20))])
    sc.step("O/N/H", "Weigh ~0.1 g of the sealed powder into a tin capsule | in a nickel basket, the flux (typical)", 4.5,
            S.together(op.walk(-650, -720)), hold=1.5, cam_to=S.look((-650, -120, BH + 80), dist=650, az=-10, el=24),
            labels=[("tin capsule in a\nnickel basket", (-650, 30 - 214 + 163, BH + 60), (0.70, 0.30))])
    # the crucible: open the electrode, set a new crucible with the tongs, close
    cam_f = S.look((fx - 20, fy - 40, BH + g["bz0"] + 120), dist=850, az=-14, el=10)
    sc.step("Crucible", "Open the furnace: the lower electrode drops", 3.5,
            S.together(op.walk(fx - 300, -760), onh.move({"lower_electrode": (1, 1), "crucible": (0, 0)})), hold=0.5,
            cam_to=cam_f)
    ncru = put(sc, "newcru", MC.prop_graphite_crucible(), Tz(-330, -150, BH + 10))
    tg = (-95.0, 0.0, 1.0)
    ped = onh.world((g["fx"], g["fy"], g["ped_top"]), "lower_electrode")
    sc.step("Crucible", "A new graphite crucible on the lower electrode | with clean tongs", 2.5,
            S.together(op.reach("r", (sc.world("tongs") @ np.array([*tg, 1.0]))[:3], lean=10)), hold=0.1)
    sc.parent["newcru"] = "tongs"
    sc.gmat["newcru"] = np.linalg.inv(sc.world("tongs")) @ sc.world("newcru")
    tong_at = lambda p: T((p[0] - 95, p[1], p[2] + 12))
    cru_rel = sc.gmat["newcru"]
    sc.gmat["tongs"] = np.array(sc.world("newcru") @ np.linalg.inv(cru_rel))
    sc.step("Crucible", "A new graphite crucible on the lower electrode | with clean tongs", 4.0,
            S.together(path(sc, "tongs", [T((fx - 140, fy - 80, BH + g["ped_top"] - g["travel"] + 120)) @ np.linalg.inv(cru_rel) @ cru_rel,
                                          T((ped[0], ped[1], ped[2] + 0.5)) @ np.linalg.inv(cru_rel)]),
                       op.follow("r", "tongs", tg)), hold=0.3)
    # hand the crucible over to the electrode: the drawn one (rides on the lower electrode) takes over
    sc.step("Crucible", "Close: the crucible is clamped between the electrodes", 3.5,
            S.together(fade(sc, "newcru", 1, 0), onh.move({"crucible": (0, 1)}),
                       path(sc, "tongs", [T((fx - 200, fy - 150, BH + g["bz0"] + 150)) @ np.linalg.inv(cru_rel)]),
                       op.follow("r", "tongs", tg), S.staged((0.4, 1.0, onh.move({"lower_electrode": (1, 0)})))),
            hold=0.5)
    sc.step("Outgas", "Outgas the empty crucible first | high power, swept by the carrier gas", 4.0,
            S.together(op.reach("r", None), path(sc, "tongs", [Tz(-330 + 150, -260, BH)]),
                       S.staged((0.2, 0.6, onh.move({"glow": (0, 1)})), (0.7, 1.0, onh.move({"glow": (1, 0.0)})))),
            hold=1.0)
    # the sample into the loading head, then dropped
    cg = (0.0, 0.0, 4.0)
    sc.step("Drop", "The capsule goes in the loading head | sealed against air before it drops", 3.5,
            S.together(op.walk(-650 + 80, -720)), hold=0.1, cam_to=S.look((-300, -100, BH + 400), dist=1600, az=-10, el=16))
    sc.step("Drop", "The capsule goes in the loading head | sealed against air before it drops", 2.0,
            op.reach("r", (sc.world("capsule") @ np.array([*cg, 1.0]))[:3], lean=10), hold=0.1)
    port = g["port"]
    sc.step("Drop", "The capsule goes in the loading head | sealed against air before it drops", 4.5,
            S.together(op.walk(fx - 330, -700), path(sc, "capsule", [Tz(-500, -300, BH + 400), Tz(150 + port[0], port[1], BH + port[2] + 40),
                                                                     Tz(150 + port[0], port[1], BH + g["smp_z0"])]),
                       op.follow("r", "capsule", cg)), hold=0.3, cam_to=cam_f)
    show(sc, "capsule", 0.0)
    onh.set(**{"~housing": 0.0})
    sc.step("Drop", "Dropped into the outgassed crucible | through the upper electrode", 3.5,
            S.together(op.reach("r", None), onh.move({"~housing": (0, 1), "sample": (0, 1)})), hold=0.8,
            labels=[("upper electrode", (fx, fy, BH + g["tip"] + 10), (0.80, 0.30)),
                    ("graphite crucible", (fx, fy - 11, BH + g["ped_top"] + 12), (0.20, 0.60))])
    sc.step("Fusion", "Fusion: well over 2,000 °C | O leaves as CO with the crucible's carbon; N as N2, H as H2", 4.5,
            S.together(onh.move({"glow": (0, 1), "sample": (1, 1)}), fade_sample(sc, onh)), hold=1.5)
    onh.set(**{"~shell": 0.0})
    sc.step("Detect", "Carrier gas sweeps them to the detectors | IR cells: CO and CO2; thermal conductivity: N2, H2", 5.0,
            S.together(onh.move({"~housing": (1, 0), "~shell": (0, 1), "gas": (0, 1)}),
                       panel_on(sc, "onh", panel_onh, (0.58, 0.10, 0.40)), sc.drive_panel("onh", 0, 1)), hold=2.0,
            cam_to=S.look((100, -100, BH + 420), dist=1900, az=-14, el=16),
            labels=[("IR cells (CO, CO2)", (150 - g["W"] / 2 + 190, 0, BH + g["H"] * 0.5 + 70), (0.15, 0.30)),
                    ("catalyst: CO to CO2", (150 - g["W"] / 2 + 390, 60, BH + g["H"] * 0.5 + 120), (0.30, 0.15)),
                    ("thermal-conductivity cell", (150 - g["W"] / 2 + 380, -110, BH + g["H"] * 0.5 - 115),
                     (0.15, 0.70))])
    rep = panel_text("Result (one powder, triplicate)", [
        "*O   0.052 ± 0.003 wt%  (520 ppm)",
        "*N   0.004 ± 0.001 wt%",
        "*H   0.0011 ± 0.0003 wt%",
        "-blank-corrected; checked against a reference"], badge="synthetic example", w=720)
    sc.step("Result", "O, N and H in wt% | each run blank-corrected; the electrode brushed clean", 4.5,
            S.together(panel_off(sc, "onh"), panel_on(sc, "rep", rep, (0.58, 0.10, 0.40)),
                       onh.move({"glow": (1, 0), "gas": (1, 0), "~shell": (1, 0), "lower_electrode": (0, 1)})),
            hold=2.5, cam_to=S.look((-100, 0, BH + 350), dist=2600, az=-12, el=16))
    sc.save()
    au.save()


def fade_sample(sc, rig):
    names = rig.names.get("sample", [])

    def up(u):
        for n in names:
            sc.alpha[n] = max(0.0, 1.0 - 1.6 * u)
    return up


def _tray_model():
    from common import Model, box, cyl, tube
    m = Model("tray", "consumables tray")
    m.add("tray", box(-110, -70, 0, 110, 70, 10).cut(box(-104, -64, 3, 104, 64, 11)), "pp_white")
    for i in range(4):
        m.add(f"crucible {i}", tube(22, 12, 25, x=-70 + 35 * i, y=30, z=3).union(cyl(22, 4, x=-70 + 35 * i, y=30, z=3)),
              "graphite_cr")
    for i in range(5):
        m.add(f"capsule {i}", cyl(7.6, 8, x=-70 + 20 * i, y=-30, z=3), "tin")
        m.add(f"basket {i}", tube(9.0, 8.4, 9, x=-70 + 20 * i, y=-5, z=3), "nickel")
    return m


# ============================================================================================ c6: analysis
def c6():
    sc = new_scene("sop05_c6", -1900, 1300)
    h = our_lab(sc, person=False)
    au = audit.Audit(sc, allow=[])
    sc.cam = overview_cam(-900, dist=2600, az=-12, el=22)
    sc.card("Analysis", ["Recalculate at the measured composition; keep both results.",
                         "Evaporation loss against the AM Module; oxygen against a surface-area estimate."],
            seconds=3.5, label="Analysis")
    sc.step("Recalculate", "Store both the nominal and the measured composition | the lab's wt% go in the run record",
            5.0, panel_on(sc, "comp", panel_composition, (0.50, 0.09, 0.48)), hold=2.5,
            cam_to=overview_cam(-1200, dist=2000, az=-14, el=22))
    sc.step("Recalculate", "Recalculate equilibrium and Scheil at the measured composition | Thermo-Calc / pycalphad",
            5.0, S.together(panel_off(sc, "comp"), panel_on(sc, "scheil", panel_scheil, (0.52, 0.09, 0.46)),
                            sc.drive_panel("scheil", 0, 1)), hold=2.5)
    sc.step("Evaporation", "Evaporation loss for each volatile element | against the AM Module at the same P, v, hatch",
            5.5, S.together(panel_off(sc, "scheil"), panel_on(sc, "evap", panel_evaporation, (0.52, 0.09, 0.46)),
                            sc.drive_panel("evap", 0, 1)), hold=3.0,
            cam_to=S.look((XJ + 20, 40, BH + 40), dist=900, az=-25, el=30))
    sc.step("Oxygen", "Oxygen against a surface-area estimate | D50 and a ~4 nm native oxide (check by XPS)", 5.5,
            S.together(panel_off(sc, "evap"), panel_on(sc, "oxy", panel_oxygen, (0.50, 0.09, 0.48)),
                       sc.drive_panel("oxy", 0, 1)), hold=3.0, cam_to=S.look((XJ, -170, BH + 70), dist=800, az=-10, el=18))
    sc.step("Oxygen", "A large excess points to oxide inclusions from the melt | not just the particles' skins", 4.0,
            None, hold=2.0)
    q1 = panel_text("Open questions", [
        "*An on-campus ICP-OES with HF or fusion digestion?",
        "-   BYU: Geological Sciences and the Environmental",
        "-   Analytical Lab run iCAP 7400s (README access table)",
        "-   If not, budget a commercial lab",
        "*Spark-OES or XRF on printed coupons, for speed",
        "-   only after validating against ICP-OES on 3-4 alloys"], w=760)
    sc.step("Open", "Open: an on-campus ICP-OES that digests Si-bearing Al? | else a commercial lab", 5.0,
            S.together(panel_off(sc, "oxy"), panel_on(sc, "q1", q1, (0.54, 0.10, 0.44))), hold=2.5,
            cam_to=overview_cam(-300, dist=3200, az=-10, el=22))
    sc.step("Open", "Faster routine checks: spark-OES or XRF | validated against ICP-OES on 3-4 alloys first", 4.5,
            None, hold=2.5)
    sc.save()
    au.save()


CHAPTERS = {"sop05_c1": c1, "sop05_c2": c2, "sop05_c3": c3, "sop05_c4": c4, "sop05_c5": c5, "sop05_c6": c6}


def join():
    parts = list(CHAPTERS)
    dst = S.join("sop05", parts)
    print(dst)
    print(S.contact_sheet("sop05"))
    print(S.preview_gif("sop05"))


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "sop05_c1"
    if arg == "join":
        join()
    else:
        CHAPTERS[arg]()
