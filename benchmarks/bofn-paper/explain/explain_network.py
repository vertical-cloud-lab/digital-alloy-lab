"""Explain the synthetic alloy function network one node at a time, as a GIF.

    python explain/explain_network.py      # from bofn-prelim/

Writes explain/frames/NN-*.png, explain/synthetic_network.gif and
explain/contact-sheet.jpg. Every curve is evaluated with AlloyTruth.node()
from ../bofn_alloy.py, so the pictures are the benchmark's own truth
functions, and the optimum is found here by multi-start L-BFGS-B (the
400,000-sample random search in analyze.optimum() lands within 0.1% of it).

Frames: the network; the six node functions (strengthening phase, freezing
range, nucleant, powder quality, the print window, cracking, strength); the
mineral penalty; the optimum; why the CALPHAD screen rejects it; and how the
optimum moves with kappa.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from matplotlib import font_manager
from PIL import Image
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from bofn_alloy import COMP, D, LAMBDA, AlloyTruth, burden  # noqa: E402
from policies import F_SAFE  # noqa: E402

for f in (Path.home() / ".local/share/fonts/aptos").glob("Aptos*.ttf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams.update({"font.family": "Aptos", "mathtext.fontset": "cm", "savefig.dpi": 100})

INK, GRAY, LIGHT, FAINT = "#1A1A1A", "#7F7F7F", "#BFBFBF", "#E6E6E6"
RED, RED_FADED = "#C00000", "#E39A9A"
W, H = 16, 9  # inches at 100 dpi -> 1600 x 900
STAGES = [("Inputs", None), ("CALPHAD", "$10"), ("Atomize", "$1,500"), ("Print", "$2,500"), ("Test", "$200"), ("Objective", None)]
INPUT_NAMES = ["Zn+Mg", "Cu", "Zr", "Sc", "atomizer setting", "laser power", "scan speed"]
FRAMES = HERE / "frames"


# --------------------------------------------------------------------------- the optimum
def optimum(kappa: float):
    """Multi-start L-BFGS-B from the 50 best of 400,000 random designs."""
    t = AlloyTruth(kappa)
    g = torch.Generator().manual_seed(0)
    X = torch.rand(400_000, D, generator=g)
    y = t.objective(X)
    best = None
    for x0 in X[y.topk(50).indices].numpy():
        r = minimize(lambda z: -float(t.objective(torch.tensor(z))), x0, method="L-BFGS-B", bounds=[(0, 1)] * D)
        if best is None or r.fun < best.fun:
            best = r
    x = torch.tensor(best.x)
    return x, -best.fun, {k: float(v) for k, v in t.full(x).items()}, X, y


def envelope(X, t, y, width=0.02):
    """Best objective among random designs, binned by freezing range."""
    f = t.full(X)["f"].numpy()
    yy = y.numpy()
    edges = np.arange(0, f.max() + width, width)
    idx = np.digitize(f, edges) - 1
    top = np.full(len(edges) - 1, np.nan)
    for i in range(len(top)):
        m = idx == i
        if m.sum() > 20:
            top[i] = yy[m].max()
    mid = edges[:-1] + width / 2
    ok = ~np.isnan(top)
    return mid[ok], top[ok]


# --------------------------------------------------------------------------- frame scaffolding
def new_frame(headline, sub, stage=None):
    fig = plt.figure(figsize=(W, H), facecolor="white")
    fig.text(0.05, 0.915, headline, fontsize=30, color=INK, va="baseline")
    fig.text(0.05, 0.862, sub, fontsize=22, color=GRAY, va="baseline")
    xs = np.linspace(0.05, 0.95, len(STAGES))
    for (name, cost), x in zip(STAGES, xs):
        on = name == stage
        fig.text(x, 0.79, name, fontsize=18, color=RED if on else LIGHT, ha="left" if name == "Inputs" else ("right" if name == "Objective" else "center"))
        if cost:
            fig.text(x, 0.76, cost, fontsize=15, color=RED_FADED if on else FAINT, ha="center")
    fig.add_artist(plt.Line2D([0.05, 0.95], [0.735, 0.735], color=FAINT, lw=1))
    return fig


def style(ax, xticks, yticks, xlabel, ylabel, xlim=(0, 1), ylim=(0, 1)):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRAY)
        ax.spines[s].set_linewidth(0.8)
    ax.spines["bottom"].set_bounds(min(xticks), max(xticks))
    ax.spines["left"].set_bounds(min(yticks), max(yticks))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xticklabels([f"{v:g}" for v in xticks])
    ax.set_yticklabels([f"{v:g}" for v in yticks])
    ax.tick_params(colors=GRAY, labelsize=17, length=0, pad=6)
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_color(GRAY)
    ax.set_xlabel(xlabel, fontsize=19, color=INK, labelpad=8)
    ax.text(0, 1.02, ylabel, transform=ax.transAxes, ha="left", va="bottom", fontsize=19, color=INK)


def callout(ax, xy, text, xytext, color, size=18, ha="left", va="center"):
    """Plain faded leader line (no arrowhead) from a point to its label."""
    ax.plot([xy[0], xytext[0]], [xy[1], xytext[1]], color=color, lw=1, alpha=0.55, zorder=2, clip_on=False)
    ax.text(xytext[0], xytext[1], text, color=color, fontsize=size, ha=ha, va=va, zorder=3, clip_on=False)


def side(fig, lines, y0=0.62, size=19, x=0.60):
    y = y0
    for text, color, kind in lines:
        s = {"eq": 22, "note": size, "small": 17}[kind]
        fig.text(x, y, text, fontsize=s, color=color, va="top", ha="left", wrap=False)
        y -= {"eq": 0.082, "note": 0.058, "small": 0.05}[kind]


def plot_ax(fig):
    return fig.add_axes([0.08, 0.14, 0.42, 0.54])


def save(fig, name):
    FRAMES.mkdir(exist_ok=True)
    path = FRAMES / f"{name}.png"
    fig.savefig(path, dpi=100, facecolor="white")
    plt.close(fig)
    return path


# --------------------------------------------------------------------------- frames
def frames():
    t = AlloyTruth(1.0)
    xo, yo, no, X, y = optimum(1.0)
    c1o, c2o, c3o, c4o, ao, Po, vo = (float(v) for v in xo)
    out = []
    grays = [INK, GRAY, LIGHT]

    # 0 network -------------------------------------------------------------
    fig = new_frame("The benchmark is six hand-written functions, wired the way the lab is",
                    "One closed-form equation per node, chosen to mirror the metallurgy. Nothing is fitted to data.")
    ax = fig.add_axes([0.04, 0.02, 0.92, 0.70])
    ax.imshow(Image.open(HERE.parent / "dag" / "bofn_dag_network.png"))
    ax.axis("off")
    out.append(("00-network", save(fig, "00-network"), 4.0))

    # 1 strengthening phase ---------------------------------------------------
    c1 = torch.linspace(0, 1, 200)
    fig = new_frame("Solute strengthens with diminishing returns, and Zn+Mg and Cu reinforce each other",
                    "The strengthening-phase fraction s, one of CALPHAD's three outputs (here with Zr = 1, Sc = 0).", "CALPHAD")
    ax = plot_ax(fig)
    for c2, col, lab in zip((0.0, 0.5, 1.0), grays[::-1], ("Cu = 0", "Cu = 0.5", "Cu = 1")):
        inp = torch.stack([c1, torch.full_like(c1, c2), torch.full_like(c1, c3o), torch.full_like(c1, c4o)], -1)
        s = t.node("s", inp)
        ax.plot(c1, s, color=col, lw=2.5)
        callout(ax, (1.0, float(s[-1])), lab, (1.04, float(s[-1])), col)
    ax.plot([c1o], [no["s"]], "o", color=RED, ms=11, zorder=5)
    callout(ax, (c1o, no["s"]), f"optimum: s = {no['s']:.2f}", (c1o - 0.02, no["s"] + 0.16), RED, ha="right")
    style(ax, [0, round(c1o, 2), 1], [0, round(no["s"], 2), 1], "Zn+Mg level", "strengthening-phase fraction s")
    side(fig, [(r"$s = \frac{1 - e^{-(1.4\,c_1 + 0.9\,c_2 + 1.5\,c_1 c_2)} + 0.1\,c_3 + 0.3\,c_4}{1.2}$", INK, "eq"),
               ("c₁ Zn+Mg, c₂ Cu, c₃ Zr, c₄ Sc, each on [0, 1]", GRAY, "note"),
               ("The exponential saturates; c₁c₂ is the synergy.", GRAY, "note"),
               ("Zr and Sc add a little strength of their own.", GRAY, "note")])
    out.append(("01-strengthening", save(fig, "01-strengthening"), 4.5))

    # 2 freezing range -------------------------------------------------------
    fig = new_frame("The same solute widens the freezing range, which is all the screen reads",
                    "Tiered screening keeps only compositions with f ≤ 0.25. The optimum has f = 0.70.", "CALPHAD")
    ax = plot_ax(fig)
    for c2, col, lab in zip((0.0, 0.5, 1.0), grays[::-1], ("Cu = 0", "Cu = 0.5", "Cu = 1")):
        inp = torch.stack([c1, torch.full_like(c1, c2), torch.full_like(c1, c3o), torch.full_like(c1, c4o)], -1)
        f = t.node("f", inp)
        ax.plot(c1, f, color=col, lw=2.5)
        callout(ax, (1.0, float(f[-1])), lab, (1.04, float(f[-1])), col)
    ax.axhline(F_SAFE, color=RED_FADED, lw=1.5, ls=(0, (4, 3)))
    ax.text(0.99, F_SAFE - 0.02, "screen cutoff: predicted crack-free below 0.25", color=RED_FADED, fontsize=17, va="top", ha="right")
    ax.plot([c1o], [no["f"]], "o", color=RED, ms=11, zorder=5)
    callout(ax, (c1o, no["f"]), f"optimum: f = {no['f']:.2f}, rejected", (c1o - 0.02, no["f"] + 0.17), RED, ha="right")
    style(ax, [0, round(c1o, 2), 1], [0, F_SAFE, round(no["f"], 2), 1], "Zn+Mg level", "freezing-range index f")
    side(fig, [(r"$f = 0.65\,c_1 + 0.55\,c_2 - 0.25\,c_1 c_2 + 0.05\,c_3 + 0.03\,c_4$", INK, "eq"),
               ("A Scheil-style index: more solute, wider", GRAY, "note"),
               ("freezing range, more hot cracking. That is the", GRAY, "note"),
               ("physics the screen uses, and on its own it is right.", GRAY, "note")])
    out.append(("02-freezing-range", save(fig, "02-freezing-range"), 4.5))

    # 3 nucleant ---------------------------------------------------------------
    c3 = torch.linspace(0, 1, 200)
    fig = new_frame("Zr and Sc form Al₃Zr and Al₃Sc nucleants",
                    "Sc is the stronger nucleant, but it carries five times Zr's critical-mineral burden.", "CALPHAD")
    ax = plot_ax(fig)
    for c4, col, lab in zip((0.0, 0.5, 1.0), grays[::-1], ("Sc = 0", "Sc = 0.5", "Sc = 1")):
        inp = torch.stack([torch.full_like(c3, c1o), torch.full_like(c3, c2o), c3, torch.full_like(c3, c4)], -1)
        g = t.node("g", inp)
        ax.plot(c3, g, color=col, lw=2.5)
        callout(ax, (1.0, float(g[-1])), lab, (1.04, float(g[-1])), col)
    ax.plot([c3o], [no["g"]], "o", color=RED, ms=11, zorder=5)
    callout(ax, (c3o, no["g"]), f"optimum: Zr = 1, Sc = 0, g = {no['g']:.2f}", (c3o - 0.06, no["g"] - 0.2), RED, ha="right")
    style(ax, [0, 1], [0, round(no["g"], 2), 1], "Zr level", "nucleant fraction g")
    side(fig, [(r"$g = \frac{(0.6\,c_3^{1.5} + 0.9\,c_4^{1.2})(1 + 0.2\,c_1)}{1.8}$", INK, "eq"),
               ("Zr counts a little more than linearly, Sc a little less.", GRAY, "note"),
               ("More Zn+Mg helps the nucleants form (1 + 0.2 c₁).", GRAY, "note"),
               ("The screen ignores g: it checks f only.", GRAY, "note")])
    out.append(("03-nucleant", save(fig, "03-nucleant"), 4.5))

    # 4 powder quality ------------------------------------------------------------
    a = torch.linspace(0, 1, 200)
    fig = new_frame("Powder quality peaks at an atomizer setting that shifts with the nucleant content",
                    "More nucleant needs a higher setting, and the peak drops a little.", "Atomize")
    ax = plot_ax(fig)
    for g, col, lab, pos in zip((0.0, no["g"], 0.8), grays[::-1], ("g = 0", f"g = {no['g']:.2f} (optimum's)", "g = 0.8"), ((0.04, 1.08), (0.40, 1.08), (0.80, 1.08))):
        q = t.node("q", torch.stack([a, torch.full_like(a, g)], -1))
        ax.plot(a, q, color=col, lw=2.5)
        i = int(q.argmax())
        callout(ax, (float(a[i]), float(q[i])), lab, pos, col, ha="left")
    ax.plot([ao], [no["q"]], "o", color=RED, ms=11, zorder=5)
    callout(ax, (ao, no["q"]), f"optimum: a = {ao:.2f}, q = {no['q']:.2f}", (ao + 0.3, 0.45), RED)
    style(ax, [0, round(ao, 2), 1], [0, 1], "atomizer setting a", "powder quality q", ylim=(0, 1.1))
    side(fig, [(r"$q = e^{-\left(\frac{a - a^*}{0.28}\right)^2}\,(0.9 + 0.1\,(1 - g))$", INK, "eq"),
               (r"$a^* = 0.3 + 0.45\,g$", INK, "eq"),
               ("One bump per powder: the setting (think superheat", GRAY, "note"),
               ("or frequency) has a sweet spot that moves with the alloy.", GRAY, "note"),
               ("At $1,500 a run, the optimizer learns a* from few runs.", GRAY, "note")])
    out.append(("04-powder-quality", save(fig, "04-powder-quality"), 4.5))

    # 5 print window ----------------------------------------------------------------
    P = torch.linspace(0, 1, 201)
    V = torch.linspace(0, 1, 201)
    PP, VV = torch.meshgrid(P, V, indexing="xy")
    inp = torch.stack([PP, VV, torch.full_like(PP, no["f"]), torch.full_like(PP, no["g"]), torch.full_like(PP, no["q"])], -1)
    rho = t.node("rho", inp)
    fig = new_frame("Dense parts lie on a constant energy-density ridge in laser power and scan speed",
                    "The ridge shifts with the freezing range, and too much power keyholes. The optimum is a ridge, not a point.", "Print")
    ax = plot_ax(fig)
    ax.imshow(rho.numpy(), origin="lower", extent=[0, 1, 0, 1], cmap="Greys", vmin=0, vmax=1.15, aspect="auto", interpolation="bilinear")
    # ridge: for each v, the P with the highest rho, where that rho is within 0.5% of the best
    best_v = rho.max(1).values
    ridge_v = V[best_v >= 0.995 * rho.max()]
    ridge_P = P[rho.argmax(1)][best_v >= 0.995 * rho.max()]
    ax.plot(ridge_P, ridge_v, color=RED, lw=3, solid_capstyle="round")
    ax.plot([Po], [vo], "o", color=RED, ms=11, zorder=5)
    callout(ax, (float(ridge_P[len(ridge_P) // 2]), float(ridge_v[len(ridge_v) // 2])), f"within 0.5% of the best:\nP − v ≈ {Po - vo:.2f}", (0.62, 0.18), RED)
    callout(ax, (Po, vo), f"optimum: ρ = {no['rho']:.2f}", (0.36, 0.04), RED)
    ax.text(0.86, 0.5, "keyholing", color=GRAY, fontsize=17, rotation=90, ha="center", va="center")
    style(ax, [0, round(Po, 2), 1], [0, 1], "laser power P", "dense, crack-free fraction ρ at the optimum's alloy (dark = dense)")
    side(fig, [(r"$\rho = \mathrm{window} \cdot q^{0.3} \cdot (1 - 0.75\,\mathrm{crack})$", INK, "eq"),
               (r"$\mathrm{window} = e^{-(u/0.2)^2}\left(1 - 0.35\,\sigma\left(\frac{P - 0.85}{0.05}\right)\right)$", INK, "eq"),
               (r"$u = P - v - (0.05 + 0.25\,f)$", INK, "eq"),
               ("A Gaussian around u = 0: wider freezing range,", GRAY, "note"),
               ("higher power needed. Poor powder thins it a little.", GRAY, "note"),
               ("Cracking is the next frame.", GRAY, "note")])
    out.append(("05-print-window", save(fig, "05-print-window"), 5.0))

    # 6 cracking ---------------------------------------------------------------------
    fgrid = torch.linspace(0, 1, 300)
    fig = new_frame("Hot cracking follows the effective freezing range, which nucleants cut by up to 85%",
                    "CALPHAD sees f. The print sees f_eff. κ sets the size of that gap, and the screen cannot see it.", "Print")
    ax = plot_ax(fig)
    # density factor from cracking alone, on the ridge with q = 1
    for g, kappa, col, lab, at, pos in ((0.0, 1.0, LIGHT, "no nucleant (or κ = 0)", 0.45, (0.50, 0.14)), (no["g"], 0.5, GRAY, f"g = {no['g']:.2f}, κ = 0.5", 0.56, (0.62, 0.60)), (no["g"], 1.0, RED, f"g = {no['g']:.2f}, κ = 1", 0.84, (0.86, 0.90))):
        tk = AlloyTruth(kappa)
        ff = fgrid
        inp = torch.stack([0.05 + 0.25 * ff, torch.zeros_like(ff), ff, torch.full_like(ff, g), torch.ones_like(ff)], -1)
        r = tk.node("rho", inp)
        ax.plot(ff, r, color=col, lw=2.5)
        i = int((ff - at).abs().argmin())
        callout(ax, (float(ff[i]), float(r[i])), lab, pos, col)
    ax.axvline(no["f"], color=RED_FADED, lw=1.2, ls=(0, (4, 3)))
    ax.text(no["f"] + 0.01, 0.02, "optimum's f", color=RED_FADED, fontsize=17)
    ax.axvline(F_SAFE, color=LIGHT, lw=1.2, ls=(0, (4, 3)))
    ax.text(F_SAFE - 0.01, 0.02, "screen cutoff", color=LIGHT, fontsize=17, ha="right")
    style(ax, [0, F_SAFE, round(no["f"], 2), 1], [0, 1], "freezing-range index f", "dense, crack-free fraction ρ on the ridge (q = 1)", ylim=(0, 1.05))
    side(fig, [(r"$f_\mathrm{eff} = f\left(1 - \kappa\,0.85\,\frac{g}{g + 0.12}\right)$", INK, "eq"),
               (r"$\mathrm{crack} = \sigma\left(\frac{f_\mathrm{eff} - 0.38}{0.05}\right)$", INK, "eq"),
               ("Zr-inoculated 7075 printing crack-free", GRAY, "note"),
               ("(Martin et al., Nature 2017) is the real version.", GRAY, "note"),
               ("At the optimum: f = 0.70 but f_eff = 0.25.", GRAY, "note")])
    out.append(("06-cracking", save(fig, "06-cracking"), 5.0))

    # 7 strength ----------------------------------------------------------------------
    s = torch.linspace(0, 1, 200)
    fig = new_frame("Strength is the strengthening phase times the dense fraction",
                    "A cracked part is weak no matter how good the alloy. Tensile testing costs $200 a bar.", "Test")
    ax = plot_ax(fig)
    for r, col, lab in zip((0.5, 0.75, 1.0), grays[::-1], ("ρ = 0.5", "ρ = 0.75", "ρ = 1")):
        U = t.node("U", torch.stack([s, torch.full_like(s, r)], -1))
        ax.plot(s, U, color=col, lw=2.5)
        callout(ax, (1.0, float(U[-1])), lab, (1.04, float(U[-1])), col)
    ax.plot([no["s"]], [no["U"]], "o", color=RED, ms=11, zorder=5)
    callout(ax, (no["s"], no["U"]), f"optimum: s = {no['s']:.2f}, ρ = {no['rho']:.2f}, U = {no['U']:.2f}", (no["s"] - 0.03, no["U"] + 0.17), RED, ha="right")
    style(ax, [0, round(no["s"], 2), 1], [0, round(no["U"], 2), 1], "strengthening-phase fraction s", "strength U")
    side(fig, [(r"$U = (0.25 + 0.75\,s)\,\rho$", INK, "eq"),
               ("With no strengthening phase the matrix keeps a", GRAY, "note"),
               ("quarter of full strength; cracks scale it down.", GRAY, "note")])
    out.append(("07-strength", save(fig, "07-strength"), 4.0))

    # 8 objective ------------------------------------------------------------------------
    fig = new_frame("The objective charges for critical minerals, so the optimum uses all the Zr and no Sc",
                    "Sc's burden weight is 1.0 against Zr's 0.2, and both buy the same thing: nucleant.", "Objective")
    ax = plot_ax(fig)
    lv = torch.linspace(0, 1, 200)
    base = xo.clone()
    for dim, col, lab in ((2, RED, "vary Zr (Sc = 0)"), (3, GRAY, "vary Sc (Zr = 1)")):
        Xs = base.expand(200, D).clone()
        Xs[:, dim] = lv
        obj = t.objective(Xs)
        ax.plot(lv, obj, color=col, lw=2.5)
        if dim == 2:
            callout(ax, (0.1, float(obj[20])), lab, (0.14, float(obj[20]) + 0.16), col)
        else:
            callout(ax, (0.9, float(obj[180])), lab, (0.70, float(obj[180]) - 0.16), col)
    ax.plot([c3o], [yo], "o", color=RED, ms=11, zorder=5)
    callout(ax, (c3o, yo), f"optimum: {yo:.2f}", (c3o - 0.02, yo + 0.12), RED, ha="right")
    style(ax, [0, 1], [0, round(yo, 2), 1], "level of the varied element", "objective = U − 0.3 × burden", ylim=(0, 1))
    side(fig, [(r"$\mathrm{objective} = U - 0.3\,B(c)$", INK, "eq"),
               (r"$B = 0.15\,c_1 + 0.1\,c_2 + 0.2\,c_3 + 1.0\,c_4$", INK, "eq"),
               ("B is a USGS-style burden: known from the", GRAY, "note"),
               ("composition, free to compute, no GP.", GRAY, "note"),
               ("Sc is the critical mineral.", GRAY, "note")])
    out.append(("08-objective", save(fig, "08-objective"), 4.5))

    # 9 the optimum -----------------------------------------------------------------------
    fig = new_frame("The optimum: a high-solute alloy, fully Zr-inoculated, printed on the ridge",
                    f"Objective {yo:.2f} = strength {no['U']:.2f} − 0.3 × burden {float(burden(xo)):.2f}, at κ = 1. Found by multi-start L-BFGS-B.", "Objective")
    ax = fig.add_axes([0.22, 0.12, 0.40, 0.56])
    ys = np.arange(D)[::-1]
    for yy_, v, name in zip(ys, xo.tolist(), INPUT_NAMES):
        ax.plot([0, 1], [yy_, yy_], color=FAINT, lw=1.2)
        ax.plot([v], [yy_], "o", color=RED if name in ("Zn+Mg", "Cu", "Zr") else INK, ms=12)
        ax.text(-0.04, yy_, name, ha="right", va="center", fontsize=20, color=INK)
        ax.text(v + (0.04 if v < 0.85 else -0.05), yy_, f"{v:.2f}", ha="left" if v < 0.85 else "right", va="center", fontsize=18, color=GRAY)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, D - 0.4)
    ax.axis("off")
    ax.text(0, D - 0.3, "0", ha="center", fontsize=16, color=GRAY)
    ax.text(1, D - 0.3, "1", ha="center", fontsize=16, color=GRAY)
    side(fig, [("What each node returns there", INK, "note"),
               (f"s {no['s']:.2f}    f {no['f']:.2f}    g {no['g']:.2f}", GRAY, "note"),
               (f"q {no['q']:.2f}    ρ {no['rho']:.2f}    U {no['U']:.2f}", GRAY, "note"),
               ("", GRAY, "small"),
               ("Scan speed is free: any (P, v) with", GRAY, "note"),
               (f"P − v ≈ {Po - vo:.2f} and P below about 0.6", GRAY, "note"),
               ("is within 0.5% of the top.", GRAY, "note")], x=0.66, y0=0.66)
    out.append(("09-optimum", save(fig, "09-optimum"), 5.5))

    # 10 the trap ------------------------------------------------------------------------------
    fm, top = envelope(X, t, y)
    feas = y[t.full(X)["f"] <= F_SAFE]
    fig = new_frame("The screen rejects the optimum, and the alloys it keeps top out at 65% of it",
                    "Best objective among 400,000 random designs, binned by freezing range (κ = 1).", "Objective")
    ax = plot_ax(fig)
    ax.axvspan(0, F_SAFE, color=FAINT, zorder=0)
    ax.text(F_SAFE / 2, 0.95, "passes the\nCALPHAD screen", ha="center", va="top", fontsize=17, color=GRAY)
    ax.plot(fm, top, color=GRAY, lw=2.5)
    ax.plot([no["f"]], [yo], "o", color=RED, ms=11, zorder=5)
    callout(ax, (no["f"], yo), f"optimum {yo:.2f} at f = {no['f']:.2f}", (no["f"] - 0.03, yo + 0.14), RED, ha="right")
    fb = float(feas.max())
    ax.plot([F_SAFE], [fb], "o", color=INK, ms=10, zorder=5)
    callout(ax, (F_SAFE, fb), f"best that passes: {fb:.2f} = {fb / yo:.0%} of the optimum", (F_SAFE + 0.05, fb - 0.14), INK)
    style(ax, [0, F_SAFE, round(no["f"], 2), 1], [0, round(fb, 2), round(yo, 2), 1], "freezing-range index f", "best objective found")
    side(fig, [("Tiered screening plateaued at 63% at $100k:", GRAY, "note"),
               ("it was searching the gray strip.", GRAY, "note"),
               ("", GRAY, "small"),
               ("Any policy that prints high-solute, Zr-rich", GRAY, "note"),
               ("alloys can reach the red point. The screen", GRAY, "note"),
               ("never prints one.", GRAY, "note")], y0=0.64)
    out.append(("10-screen-trap", save(fig, "10-screen-trap"), 5.5))

    # 11 kappa -----------------------------------------------------------------------------------
    fig = new_frame("Turn the nucleant effect off and the optimum moves to a lean alloy that nearly passes",
                    "κ is the one knob that makes the screen wrong. Each level is its own benchmark, with its own optimum.", "Objective")
    ax = plot_ax(fig)
    ax.axvspan(0, F_SAFE, color=FAINT, zorder=0)
    ax.text(F_SAFE / 2, 0.95, "passes the\nCALPHAD screen", ha="center", va="top", fontsize=17, color=GRAY)
    ticks_f, ticks_y = {0, F_SAFE, 1}, {0, 1}
    for kappa, col, pos in ((0.0, LIGHT, (0.02, 0.70)), (0.5, GRAY, (0.60, 0.36)), (1.0, RED, (0.74, 0.86))):
        tk = AlloyTruth(kappa)
        xk, yk, nk, Xk, yyk = optimum(kappa)
        fm, top = envelope(Xk, tk, yyk)
        ax.plot(fm, top, color=col, lw=2.5)
        ax.plot([nk["f"]], [yk], "o", color=col, ms=11, zorder=5)
        zr = f"Zr = {float(xk[2]):.0f}"
        callout(ax, (nk["f"], yk), f"κ = {kappa:g}: optimum {yk:.2f}\nat f = {nk['f']:.2f}, {zr}", pos, col, size=17)
        if kappa != 0.0:
            ticks_f.add(round(nk["f"], 2))
            ticks_y.add(round(yk, 2))
    style(ax, sorted(ticks_f), sorted(ticks_y), "freezing-range index f", "best objective found", ylim=(0, 1))
    side(fig, [("κ = 0: CALPHAD's crack criterion is right. The", GRAY, "note"),
               ("optimum is a lean alloy with no nucleant, and", GRAY, "note"),
               ("the screen keeps 90% of it. Tiered screening", GRAY, "note"),
               ("did well there (85% at $100k).", GRAY, "note"),
               ("", GRAY, "small"),
               ("κ = 1: the optimum needs the effect the", GRAY, "note"),
               ("screen cannot see.", GRAY, "note")], y0=0.64)
    out.append(("11-kappa", save(fig, "11-kappa"), 6.0))
    return out


def contact_sheet(paths, cols=3, out=HERE / "contact-sheet.jpg"):
    ims = [Image.open(p).convert("RGB").resize((800, 450)) for p in paths]
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 800 + (cols + 1) * 10, rows * 450 + (rows + 1) * 10), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (10 + (i % cols) * 810, 10 + (i // cols) * 460))
    sheet.save(out, quality=88)


def main():
    fr = frames()
    ims = [Image.open(p).convert("RGB").quantize(colors=200, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for _, p, _ in fr]
    ims[0].save(HERE / "synthetic_network.gif", save_all=True, append_images=ims[1:], duration=[int(d * 1000) for _, _, d in fr], loop=0, optimize=False)
    contact_sheet([p for _, p, _ in fr])
    print("frames:", len(fr), " gif:", (HERE / "synthetic_network.gif").stat().st_size // 1024, "kB")


if __name__ == "__main__":
    main()
