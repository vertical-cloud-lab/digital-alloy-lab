"""SOP 02 (#262, PR #263): single tracks, their cross-sections, and the heat-source calibration, step by step in 3-D.

    xvfb-run -a python sop02_tracks.py sop02_c1      # one chapter -> out/mp4/sop02_c1.mp4 (PREVIEW=1: a contact sheet)
    python sop02_tracks.py data                      # the synthetic tracks and the fit (out/sop02_data.json)
    python sop02_tracks.py join                      # out/mp4/sop02.mp4, out/sop02.json, contact sheet, preview GIF

Chapters: c1 Samples (the LPBF build area), c2 Preparation 1 (top views on the VHX), c3 Preparation 2 (the strip,
the VC50 cut at mid-length, the hot mount), c4 Preparation 3 (grind and polish on the PX500), c5 Preparation 4
(Keller's etch in the hood, with the HF precautions), c6 Preparation 5 (images at a fixed magnification, measuring,
the second plane, the time estimates), c7 Analysis, Acceptance and the open questions.

Every number on a data panel comes from ``../analysis/melt_pool_calibration.py`` run on synthetic tracks made here
(``data()``), and every such panel is badged "synthetic example". The plate, the layer and the tracks are drawn at
their real sizes; the inside of the build chamber is a typical layout (Aconity publishes no drawing of it).
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage as S  # noqa: E402
from stage import BENCH_H, R, T  # noqa: E402

ANALYSIS = HERE.parent / "analysis"
DATA = S.OUT / "sop02_data.json"
TITLE = "SOP 02 · Single tracks: melt-pool size and the heat-source fit"

# the reference palette's first three categorical slots (dataviz skill: validated all-pairs) and text inks
C1, C2, C3 = "#257de0", "#f47230", "#00b894"
INK, INK2, GRID = "#191919", "#666666", "#d9d9d9"


# ============================================================================================ synthetic data
def _fast_field(mp):
    """melt_pool_calibration.TrackField on a coarser grid (same pool to 0.1 um at 200 W, 0.8 m/s): 0.25 s a field."""
    base = mp.TrackField

    class FastField(base):
        def __init__(self, v_m_s, r0_m, k, rho, cp, **kw):
            kw.setdefault("x_range", (-1.2e-3, 0.25e-3))
            kw.setdefault("dx", 5e-6)
            kw.setdefault("ymax", 600e-6)
            kw.setdefault("dy", 3e-6)
            kw.setdefault("n_s", 320)
            super().__init__(v_m_s, r0_m, k, rho, cp, **kw)
    return FastField


def data(rebuild: bool = False) -> dict:
    """72 synthetic tracks (4 Sobol blocks of 16 + 2 controls each) and 18 bare-plate tracks, their widths and depths
    from the Eagar-Tsai field with an absorptivity that rises with the keyhole number and a keyhole deepening above
    Ke ~ 8 (so the fit has conduction, transition and keyhole tracks to sort), with 2 % / 5 % noise; then the repo's
    own fit_eta on the conduction tracks, the width-only absorptivity, Ke, a synthetic 'AM Module' set (Eagar-Tsai at
    eta = 0.36) for bias and RMSE, leave-one-out eta, the control spread and a single Ke threshold. Cached in
    out/sop02_data.json."""
    if DATA.exists() and not rebuild:
        return json.loads(DATA.read_text())
    sys.path.insert(0, str(ANALYSIS))
    import melt_pool_calibration as mp
    from scipy.stats import qmc
    mp.TrackField = _fast_field(mp)
    mat = dict(mp.DEMO_MATERIAL)
    dT = mat["T_liquidus_K"] - mat["T0_K"]
    r0 = mat["r0_um"] * 1e-6
    k, rho, cp = mat["k_W_mK"], mat["rho_kg_m3"], mat["cp_J_kgK"]
    rng = np.random.default_rng(262)
    sob = qmc.Sobol(d=2, scramble=True, seed=262).random(64)
    P = 100.0 + (370.0 - 100.0) * sob[:, 0]
    v = np.exp(np.log(400.0) + (np.log(3000.0) - np.log(400.0)) * sob[:, 1])
    ctrl = (300.0, 1300.0)
    fields = {}

    def field(vv):
        key = round(float(vv), 2)
        if key not in fields:
            fields[key] = mp.TrackField(vv * 1e-3, r0, k, rho, cp)
        return fields[key]

    def make(PP, vv, sigma_w=0.018, bare=False):
        ke0 = mp.keyhole_number(0.30, PP, vv * 1e-3, r0, k, rho, cp, dT)
        eta_eff = 0.30 + 0.26 / (1.0 + math.exp(-(ke0 - 10.0) / 2.0))
        if bare:
            eta_eff *= 0.92                              # a ground plate takes a little less than a powder bed
        W, D = field(vv).pool(eta_eff, PP, dT)
        kh = 1.0 + 0.28 * max(0.0, ke0 - 8.0)
        W = W * 1e6 * (1 + sigma_w * rng.standard_normal())
        D = D * 1e6 * kh * (1 + 0.05 * rng.standard_normal())
        H = (0.0 if bare else 0.55 * 40.0) * (1 + 0.15 * rng.standard_normal()) + 0.04 * W * (not bare)
        balling = bool(vv > 1900 and PP < 200)
        return dict(P_W=round(float(PP), 1), v_mm_s=round(float(vv), 1), width_um=round(float(W), 1),
                    depth_um=round(float(D), 1), height_um=round(float(max(H, 0.0)), 1), ke0=round(ke0, 2),
                    balling=balling)

    tracks = []
    for b in range(4):
        pts = [(P[i], v[i], f"S{i:02d}") for i in range(16 * b, 16 * b + 16)] + [(*ctrl, "C1"), (*ctrl, "C2")]
        order = rng.permutation(len(pts))
        for pos, j in enumerate(order):
            PP, vv, sid = pts[j]
            t = make(PP, vv)
            t.update(track_id=f"{'ABCD'[b]}{pos + 1:02d}", block="ABCD"[b], pos=int(pos), set=sid,
                     control=sid.startswith("C"))
            tracks.append(t)
    bare = []
    bsel = rng.permutation(64)[:16]
    pts = [(P[i], v[i], f"S{i:02d}") for i in bsel] + [(*ctrl, "C1"), (*ctrl, "C2")]
    order = rng.permutation(len(pts))
    for pos, j in enumerate(order):
        PP, vv, sid = pts[j]
        t = make(PP, vv, bare=True)
        t.update(track_id=f"B{pos + 1:02d}", block="bare", pos=int(pos), set=sid, control=sid.startswith("C"))
        bare.append(t)
    rows = [dict(track_id=t["track_id"], P_W=t["P_W"], v_mm_s=t["v_mm_s"], width_um=t["width_um"],
                 depth_um=t["depth_um"]) for t in tracks]
    eta, rms, out = mp.fit_eta([dict(r) for r in rows], mat, fit_on="conduction")
    byid = {o["track_id"]: o for o in out}
    for t in tracks:
        o = byid[t["track_id"]]
        t.update(regime=o["regime_measured"], d_over_w=o["d_over_w"], used=o["used_in_fit"],
                 W_model=o["width_model_um"], D_model=o["depth_model_um"], eta_w=o["eta_from_width_alone"],
                 Ke=o["Ke_at_fitted_eta"])
    # a synthetic "AM Module": Eagar-Tsai at eta 0.36 (as if calibrated elsewhere), for the bias and RMSE panel
    am = []
    for t in tracks:
        W, D = field(t["v_mm_s"]).pool(0.36, t["P_W"], dT)
        am.append(dict(track_id=t["track_id"], width_um=round(W * 1e6, 1), depth_um=round(D * 1e6, 1)))
    cmp = mp.compare_am_module(out, am)
    amd = {a["track_id"]: a for a in am}
    for t in tracks:
        t.update(W_am=amd[t["track_id"]]["width_um"], D_am=amd[t["track_id"]]["depth_um"])
    # leave one out (conduction tracks)
    cond = [r for r, t in zip(rows, tracks) if t["regime"] == "conduction"]
    loo = []
    for i in range(len(cond)):
        sub = [dict(r) for j, r in enumerate(cond) if j != i]
        e, _, _ = mp.fit_eta(sub, mat, fit_on="conduction")
        loo.append(round(e, 4))
    # controls: spread about their mean
    cw = [t["width_um"] for t in tracks if t["control"]]
    cdev = [round(100 * (w / np.mean(cw) - 1), 2) for w in cw]
    # a single Ke threshold for keyhole onset (D/W >= 0.75): the cut that misclassifies fewest tracks
    ke = np.array([t["Ke"] for t in tracks])
    kh = np.array([t["regime"] == "keyhole" for t in tracks])
    cands = np.sort(ke)
    errs = [int(np.sum((ke >= c) != kh)) for c in cands]
    i0 = int(np.argmin(errs))
    ke_th = float(0.5 * (cands[i0] + cands[max(i0 - 1, 0)]))
    counts = {r: sum(t["regime"] == r for t in tracks) for r in ("conduction", "transition", "keyhole")}
    out_d = dict(material=mat, eta_fit=round(eta, 4), rms_rel=round(rms, 4), tracks=tracks, bare=bare,
                 am_vs_measured=cmp, loo=loo, controls_dev_pct=cdev, ke_threshold=round(ke_th, 2),
                 ke_errors=int(errs[i0]), counts=counts, control_set=dict(P_W=ctrl[0], v_mm_s=ctrl[1]),
                 window=dict(P_W=[100, 370], v_mm_s=[400, 3000]))
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(out_d, indent=1) + "\n")
    return out_d


# ================================================================================================ panels
def _fig(w=5.2, h=3.4):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": "#888888",
                         "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "axes.linewidth": 0.8})
    fig = plt.figure(figsize=(w, h), dpi=150)
    fig.patch.set_facecolor("white")
    fig.patch.set_alpha(0.94)
    return fig, plt


def _badge(fig, text="synthetic example", sub=""):
    fig.text(0.985, 0.975, text, ha="right", va="top", fontsize=8.5, color="white", weight="bold",
             bbox=dict(boxstyle="round,pad=0.3", fc="#b3541e", ec="none"))
    if sub:
        fig.text(0.015, 0.012, sub, ha="left", va="bottom", fontsize=7.2, color=INK2)


def _axes(ax):
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)


def panel_design(d, u=1.0):
    """The P-v design: four scrambled-Sobol blocks of 16 (marker shape = block) and the repeated control."""
    fig, plt = _fig(5.0, 3.6)
    ax = fig.add_axes([0.14, 0.15, 0.62, 0.70])
    marks = {"A": "o", "B": "s", "C": "^", "D": "D"}
    n_show = int(round(4 * u + 0.49))
    for b in "ABCD"[:max(1, n_show)]:
        pts = [(t["v_mm_s"], t["P_W"]) for t in d["tracks"] if t["block"] == b and not t["control"]]
        ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=26, marker=marks[b], c=C1, edgecolors="white",
                   linewidths=0.8, label=f"block {b}: 16 settings", zorder=3)
    c = d["control_set"]
    ax.scatter([c["v_mm_s"]], [c["P_W"]], s=90, marker="*", c=C2, edgecolors="white", linewidths=0.8,
               label="control, 2 per block", zorder=4)
    ax.set_xscale("log")
    ax.set_xlabel("scan speed v (mm/s)")
    ax.set_ylabel("laser power P (W)")
    ax.set_xticks([400, 700, 1000, 2000, 3000])
    ax.set_xticklabels(["400", "700", "1000", "2000", "3000"])
    _axes(ax)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=7.5, frameon=False)
    fig.text(0.02, 0.95, "Power-speed design: scrambled Sobol, not a grid", fontsize=10.5, weight="bold", color=INK)
    _badge(fig, "design, illustrative window", "window 100-370 W, 400-3000 mm/s (log); set it from the AM Module map")
    return S.fig_image(fig)


def _track_strip(ax, kind, W_um, y0, rng):
    """A top view of one track (12 mm long along x here) at 50-100x: the track, its ripples, the denuded band."""
    from matplotlib.patches import Rectangle, Circle
    L = 3000.0                                        # um shown
    den = 2.6 * W_um
    ax.add_patch(Rectangle((0, y0 - den / 2), L, den, fc="#a9abae", ec="none"))
    if kind == "continuous":
        ax.add_patch(Rectangle((0, y0 - W_um / 2), L, W_um, fc="#dfe1e3", ec="#8d9094", lw=0.6))
        for x in np.arange(40, L, 55):
            ax.plot([x, x + 25], [y0 - W_um * 0.42, y0], color="#b9bcc0", lw=0.5)
            ax.plot([x + 25, x], [y0, y0 + W_um * 0.42], color="#b9bcc0", lw=0.5)
    else:
        x = 60.0
        while x < L:
            r = W_um * (0.45 + 0.35 * rng.random())
            ax.add_patch(Circle((x, y0 + 0.15 * W_um * rng.standard_normal()), r, fc="#dfe1e3", ec="#8d9094", lw=0.6))
            x += 2.2 * r + 90 * rng.random()
    return den


def panel_topview(d, u=1.0):
    fig, plt = _fig(5.2, 3.5)
    ax = fig.add_axes([0.03, 0.10, 0.94, 0.72])
    rng = np.random.default_rng(5)
    ax.set_facecolor("#7d8085")                       # loose powder around the tracks
    for i in range(600):
        ax.plot(rng.uniform(0, 3000), rng.uniform(-200, 1700), ".", color="#9a9da1", ms=1.2)
    cont = [t for t in d["tracks"] if t["regime"] == "conduction" and not t["balling"]][0]
    ball = [t for t in d["tracks"] if t["balling"]] or [d["tracks"][0]]
    den1 = _track_strip(ax, "continuous", cont["width_um"], 300, rng)
    den2 = _track_strip(ax, "balling", ball[0]["width_um"], 1150, rng)
    ax.annotate("", xy=(2700, 300 - den1 / 2), xytext=(2700, 300 + den1 / 2),
                arrowprops=dict(arrowstyle="<->", color="white", lw=1.0))
    ax.text(2740, 300, f"denuded\n{den1:.0f} um", color="white", fontsize=7.5, va="center")
    ax.text(40, 300 + den1 / 2 + 40, f"continuous: {cont['P_W']:.0f} W, {cont['v_mm_s']:.0f} mm/s", color="white",
            fontsize=8)
    ax.text(40, 1150 + den2 / 2 + 40, f"balling: {ball[0]['P_W']:.0f} W, {ball[0]['v_mm_s']:.0f} mm/s", color="white",
            fontsize=8)
    ax.plot([2300, 2800], [-120, -120], color="white", lw=2)
    ax.text(2550, -90, "500 um", color="white", fontsize=7.5, ha="center", va="bottom")
    ax.set_xlim(0, 3000)
    ax.set_ylim(-200, 1700)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.text(0.02, 0.95, "Top view at 75x: continuity, balling, denudation", fontsize=10.5, weight="bold", color=INK)
    _badge(fig, "synthetic example", "drawn from the synthetic track widths; a real top view replaces it")
    return S.fig_image(fig)


def panel_section(d, u=1.0, which=None):
    """An etched cross-section of one track with W (at the original surface), D below it, H above it and the fused
    area, as measured in Fiji."""
    fig, plt = _fig(5.2, 3.6)
    ax = fig.add_axes([0.04, 0.10, 0.92, 0.72])
    t = which or [x for x in d["tracks"] if x["regime"] == "conduction"][3]
    W, D, H = t["width_um"], t["depth_um"], max(t["height_um"], 18.0)
    xs = np.linspace(-W / 2, W / 2, 200)
    ax.set_facecolor("#c7c9cc")
    ax.fill_between([-W, W], [0, 0], [-1.6 * D, -1.6 * D], color="#b5b8bc")            # substrate, etched
    bottom = -D * np.sqrt(np.clip(1 - (2 * xs / W) ** 2, 0, 1))
    top = H * np.sqrt(np.clip(1 - (2 * xs / (0.92 * W)) ** 2, 0, 1))
    ax.fill_between(xs, bottom, top, color="#e3e1dc", ec="#55585c", lw=0.9)               # the fused zone
    for k in range(-5, 6):                                                                # columnar grains
        x0 = k * W / 12
        yb = -D * math.sqrt(max(1 - (2 * x0 / W) ** 2, 0))
        ax.plot([x0, x0 * 0.35], [yb, 0.4 * H], color="#c9c6bf", lw=0.6)
    ax.plot([-W, W], [0, 0], color=INK2, lw=0.8, ls="--")
    ax.annotate("", xy=(-W / 2, 0), xytext=(W / 2, 0), arrowprops=dict(arrowstyle="<->", color=C1, lw=1.4))
    ax.text(0, 6, f"W = {W:.0f} um", color=INK, ha="center", va="bottom", fontsize=8.5,
            bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
    ax.annotate("", xy=(0, 0), xytext=(0, -D), arrowprops=dict(arrowstyle="<->", color=C2, lw=1.4))
    ax.text(6, -D * 0.6, f"D = {D:.0f} um", color=INK, ha="left", fontsize=8.5,
            bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
    ax.annotate("", xy=(W * 0.34, 0), xytext=(W * 0.34, H), arrowprops=dict(arrowstyle="<->", color=C3, lw=1.2))
    ax.text(W * 0.37, H * 0.9, f"H = {H:.0f} um", color=INK, ha="left", fontsize=8.5,
            bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
    area = np.trapezoid(top - bottom, xs) / 1e6 if hasattr(np, "trapezoid") else np.trapz(top - bottom, xs) / 1e6
    ax.text(-W * 0.95, -1.45 * D, f"fused area {area * 1e3:.1f} x 10^-3 mm^2", color=INK, fontsize=8.5)
    ax.text(-W * 0.95, H + 10, "original surface", color=INK2, fontsize=7.5)
    ax.set_xlim(-W, W)
    ax.set_ylim(-1.6 * D, max(H * 2.2, 0.55 * D))
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    fig.text(0.02, 0.95, f"Track {t['track_id']} at 200x: {t['P_W']:.0f} W, {t['v_mm_s']:.0f} mm/s", fontsize=10.5,
             weight="bold", color=INK)
    _badge(fig, "synthetic example", "measured in Fiji: W at the original surface, D below it, H above it, area")
    return S.fig_image(fig)


def panel_fit(d, u=1.0):
    fig, plt = _fig(5.2, 3.6)
    ax = fig.add_axes([0.14, 0.15, 0.56, 0.68])
    used = [t for t in d["tracks"] if t["used"]]
    other = [t for t in d["tracks"] if not t["used"]]
    lim = [0, max(max(t["width_um"] for t in d["tracks"]), 400)]
    ax.plot(lim, lim, color=INK2, lw=0.8)
    ax.scatter([t["width_um"] for t in used], [t["W_model"] for t in used], s=22, c=C1, edgecolors="white",
               linewidths=0.6, label="width, conduction", zorder=3)
    ax.scatter([t["depth_um"] for t in used], [t["D_model"] for t in used], s=22, c=C2, marker="s",
               edgecolors="white", linewidths=0.6, label="depth, conduction", zorder=3)
    ax.scatter([t["depth_um"] for t in other], [t["D_model"] for t in other], s=10, c="#bbbbbb", marker="s",
               label="depth, not fitted", zorder=2)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("measured (um)")
    ax.set_ylabel("Eagar-Tsai at fitted eta (um)")
    _axes(ax)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=7.5, frameon=False)
    fig.text(0.73, 0.40, f"eta = {d['eta_fit']:.3f}", fontsize=13, weight="bold", color=INK)
    fig.text(0.73, 0.33, f"{len(used)} conduction tracks\n(D/W < 0.5)", fontsize=8, color=INK2, va="top")
    fig.text(0.02, 0.95, "Absorptivity fit on conduction tracks only", fontsize=10.5, weight="bold", color=INK)
    _badge(fig, "synthetic example", "melt_pool_calibration.py --fit-on conduction (the model has no keyhole)")
    return S.fig_image(fig)


def panel_eta_w(d, u=1.0):
    fig, plt = _fig(5.2, 3.6)
    ax = fig.add_axes([0.14, 0.15, 0.56, 0.68])
    cols = {"conduction": C1, "transition": C2, "keyhole": C3}
    for r, c in cols.items():
        ts = [t for t in d["tracks"] if t["regime"] == r and t["eta_w"] is not None]
        ax.scatter([t["P_W"] / t["v_mm_s"] for t in ts], [t["eta_w"] for t in ts], s=20, c=c, edgecolors="white",
                   linewidths=0.6, label=r, zorder=3)
    ax.axhline(d["eta_fit"], color=INK2, lw=0.9, ls="--")
    ax.text(0.02, d["eta_fit"] + 0.008, "fitted eta", color=INK2, fontsize=7.5, transform=ax.get_yaxis_transform())
    ax.set_xscale("log")
    ax.set_xlabel("P/v (J/mm)")
    ax.set_ylabel("eta from width alone")
    _axes(ax)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=7.5, frameon=False, title="regime (D/W)",
              title_fontsize=7.5)
    fig.text(0.02, 0.95, "Width-only absorptivity per track rises with P/v", fontsize=10.5, weight="bold", color=INK)
    _badge(fig, "synthetic example", "eta_from_width_alone, one value per track")
    return S.fig_image(fig)


def panel_ke(d, u=1.0):
    fig, plt = _fig(5.2, 3.6)
    ax = fig.add_axes([0.14, 0.15, 0.56, 0.68])
    cols = {"conduction": C1, "transition": C2, "keyhole": C3}
    for r, c in cols.items():
        ts = [t for t in d["tracks"] if t["regime"] == r]
        ax.scatter([t["Ke"] for t in ts], [t["d_over_w"] for t in ts], s=20, c=c, edgecolors="white", linewidths=0.6,
                   label=f"{r} ({len(ts)})", zorder=3)
    ax.axvline(d["ke_threshold"], color=INK, lw=1.0)
    ax.text(d["ke_threshold"] * 1.04, 0.05, f"Ke* = {d['ke_threshold']:.1f}", color=INK, fontsize=8.5,
            transform=ax.get_xaxis_transform())
    for yv in (0.5, 0.75):
        ax.axhline(yv, color=INK2, lw=0.7, ls=":")
    ax.set_xscale("log")
    ax.set_xlabel("keyhole number Ke (Gan et al. 2021)")
    ax.set_ylabel("depth / width")
    _axes(ax)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=7.5, frameon=False)
    fig.text(0.02, 0.95, "Ke per track, and one threshold for keyhole onset", fontsize=10.5, weight="bold", color=INK)
    _badge(fig, "synthetic example", f"threshold misclassifies {d['ke_errors']} of {len(d['tracks'])} tracks (#249)")
    return S.fig_image(fig)


def panel_am(d, u=1.0):
    fig, plt = _fig(5.2, 3.6)
    ax = fig.add_axes([0.14, 0.15, 0.50, 0.68])
    lim = [0, max(max(t["depth_um"] for t in d["tracks"]), max(t["width_um"] for t in d["tracks"])) * 1.05]
    ax.plot(lim, lim, color=INK2, lw=0.8)
    ax.scatter([t["width_um"] for t in d["tracks"]], [t["W_am"] for t in d["tracks"]], s=16, c=C1,
               edgecolors="white", linewidths=0.5, label="width", zorder=3)
    ax.scatter([t["depth_um"] for t in d["tracks"]], [t["D_am"] for t in d["tracks"]], s=16, c=C2, marker="s",
               edgecolors="white", linewidths=0.5, label="depth", zorder=3)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("measured (um)")
    ax.set_ylabel("AM Module predicted (um)")
    _axes(ax)
    ax.legend(loc="lower right", fontsize=7.5, frameon=False)
    c = d["am_vs_measured"]
    fig.text(0.67, 0.78, "AM Module - measured", fontsize=8.5, weight="bold", color=INK)
    fig.text(0.67, 0.70, f"width bias {c['width_bias_um']:+.0f} um\nwidth RMSE {c['width_rmse_um']:.0f} um\n\n"
                         f"depth bias {c['depth_bias_um']:+.0f} um\ndepth RMSE {c['depth_rmse_um']:.0f} um",
             fontsize=8.5, color=INK, va="top")
    fig.text(0.02, 0.95, "The AM Module against the measured tracks", fontsize=10.5, weight="bold", color=INK)
    _badge(fig, "synthetic example", "the 'AM Module' here is Eagar-Tsai at eta 0.36, a stand-in for its CSV export")
    return S.fig_image(fig)


def panel_table(title, rows, badge="", sub="", w=5.2, h=3.2, col=0.46):
    fig, plt = _fig(w, h)
    fig.text(0.03, 0.92, title, fontsize=11, weight="bold", color=INK)
    y = 0.80
    for a, b in rows:
        fig.text(0.04, y, a, fontsize=9, color=INK, va="top")
        fig.text(col, y, b, fontsize=9, color=INK2, va="top")
        y -= 0.125 if "\n" not in b and "\n" not in a else 0.19
    if badge:
        _badge(fig, badge, sub)
    elif sub:
        fig.text(0.015, 0.012, sub, ha="left", va="bottom", fontsize=7.2, color=INK2)
    return S.fig_image(fig)


def panel_acceptance(d, u=1.0):
    c = d["counts"]
    loo = d["loo"]
    dev = d["controls_dev_pct"]
    ok = lambda b: "PASS" if b else "FAIL"                 # noqa: E731
    rows = [("Conduction tracks (>= 3)", f"{c['conduction']}   {ok(c['conduction'] >= 3)}"),
            ("Keyhole tracks (>= 3)", f"{c['keyhole']}   {ok(c['keyhole'] >= 3)}"),
            ("Controls repeat within +-5 % (width)",
             f"{min(dev):+.1f} to {max(dev):+.1f} %   {ok(max(abs(x) for x in dev) <= 5)}"),
            ("eta stable within +-0.03,\nleaving any one track out",
             f"{min(loo):.3f} to {max(loo):.3f}\n(fit {d['eta_fit']:.3f})   "
             f"{ok(max(abs(x - d['eta_fit']) for x in loo) <= 0.03)}")]
    return panel_table("Acceptance, per alloy and substrate condition", rows, "synthetic example",
                       "one-powder-layer tracks; repeat for the bare-plate tracks", col=0.58)


def _cached(fn, *a):
    """A panel function -> f(u) returning one cached image (the panels here are static)."""
    box_ = {}

    def f(u):
        if "im" not in box_:
            box_["im"] = fn(*a)
        return box_["im"]
    return f


# ============================================================================================ scene helpers
def cam_hold(sc, cam):
    sc.cam = [tuple(map(float, c)) for c in cam]


def box_mesh(x0, x1, y0, y1, z0, z1):
    import pyvista as pv
    return pv.Box(bounds=(x0, x1, y0, y1, z0, z1)).triangulate()


def add_mesh(sc, name, mesh, mat, group, at=None, parent=None, opacity=None, shown=True):
    r, g, b, a, spec = S.MATS[mat]
    kw = dict(specular=spec)
    if mat in S.GLOWY:
        kw.update(ambient=0.9, diffuse=0.25)
    sc.add(name, mesh, (r, g, b), group, opacity=a if opacity is None else opacity, shown=shown, **kw)
    if at is not None:
        sc.gmat[group] = at
    if parent is not None:
        sc.parent[group] = parent
    return name


def fade(sc, names, a0, a1):
    def up(u):
        for n in names:
            sc.alpha[n] = a0 + (a1 - a0) * u
    return up


def person(sc, name="op", **kw):
    import people
    p = people.Person(sc, name)
    p.set(**kw)
    return p


def walk(p, x0, y0, x1, y1, hd=None):
    """update(u): walk in steps from (x0, y0) to (x1, y1), one gait cycle per 1016 mm."""
    dist = math.hypot(x1 - x0, y1 - y0)
    hd = math.degrees(math.atan2(-(x1 - x0), (y1 - y0))) if hd is None else hd
    cycles = max(1.0, round(dist / p.STRIDE * 2) / 2)

    def up(u):
        amp = min(1.0, 4 * u, 4 * (1 - u))
        p.set(x=x0 + (x1 - x0) * u, y=y0 + (y1 - y0) * u, hd=hd, phase=2 * math.pi * cycles * u, amp=amp)
    return up


def reach(p, side, a, b, grip=None, look=None, lean=None):
    """update(u): one hand from a to b (world xyz; None = at rest)."""
    a = None if a is None else np.asarray(a, float)
    b = None if b is None else np.asarray(b, float)
    l0 = p.st["lean"]

    def up(u):
        if a is None and b is None:
            tgt = None
        else:
            aa = p.rest_hand(side) if a is None else a
            bb = p.rest_hand(side) if b is None else b
            tgt = tuple(aa + (bb - aa) * u)
        kw = dict(hands={side: tgt})
        if grip is not None:
            kw["grip"] = {side: grip[0] + (grip[1] - grip[0]) * u}
        if look is not None:
            kw["look"] = look
        if lean is not None:
            kw["lean"] = l0 + (lean - l0) * u
        p.set(**kw)
    return up


def label_pt(rig, xyz, piece="body"):
    return tuple(float(v) for v in rig.world(xyz, piece))


def run(chapter: str):
    fn = CHAPTERS[chapter]
    fn()


CHAPTERS: dict = {}


def chapter(name):
    def deco(f):
        CHAPTERS[name] = f
        return f
    return deco


def audit_for(sc, allow=()):
    import audit
    return audit.Audit(sc, allow=list(allow))


# ================================================================================= chapter 1: the samples
TRACK_L, PITCH, GAP = 12.0, 2.0, 10.0
ROW_Y = {"bare": 46.0, "A": 23.0, "B": 0.0, "C": -23.0, "D": -46.0}


def row_x(pos: int) -> float:
    """x of track `pos` (0-17) in a row: two groups of nine at 2 mm pitch, 10 mm apart; position 0 is at the outlet
    side (+x), so the exposure order runs toward the inlet (-x)."""
    g, k = divmod(pos, 9)
    x_from_out = k * PITCH + g * (8 * PITCH + GAP)
    return 21.0 - x_from_out


def track_mesh(t, z0, length=TRACK_L, pos_x=None, y_mid=0.0, frac=1.0):
    """A solidified track (real width; its top H over the surface, at least 15 um so it shows), from y_mid - L/2 to
    y_mid - L/2 + frac * L; balling tracks as a chain of beads."""
    import pyvista as pv
    w = t["width_um"] / 1000.0
    h = max(t.get("height_um", 0.0), 15.0) / 1000.0
    x = pos_x
    y0 = y_mid - length / 2
    y1 = y0 + max(frac, 0.002) * length
    if t.get("balling"):
        beads = []
        rng = np.random.default_rng(int(abs(hash(t["track_id"])) % 1000))
        y = y0 + 0.1
        while y < y1:
            r = w * (0.45 + 0.3 * rng.random())
            beads.append(pv.Sphere(radius=r, center=(x, y, z0 + 0.4 * r), theta_resolution=10, phi_resolution=8))
            y += 2.4 * r + 0.08 * rng.random()
        if beads:
            return S.merge(beads)
        return pv.Sphere(radius=w / 2, center=(x, y0, z0))
    m = pv.Cylinder(center=(x, (y0 + y1) / 2, z0), direction=(0, 1, 0), radius=0.5, height=y1 - y0,
                    resolution=16).triangulate()
    m.points[:, 0] = x + (m.points[:, 0] - x) * w
    m.points[:, 2] = z0 + np.maximum(m.points[:, 2] - z0, -0.0) * 2 * h
    m.points[:, 2] = np.maximum(m.points[:, 2], z0 - 0.004)
    return m


@chapter("sop02_c1")
def c1():
    d = data()
    sc = S.SOPScene("sop02_c1", TITLE)
    sc.panels = {}
    # the printer, for context, on the floor; the build area close-up far to its right (a cut, not a walk)
    ext = S.place(sc, "lpbf_exterior", -2600.0, 0.0, z=0.0, shadow=True)
    CX, CY, CZ = 4000.0, 0.0, 1000.0                    # the close-up's chamber floor centre
    ch = S.place(sc, "lpbf_chamber", CX, CY, z=CZ, shadow=False)
    floor_z = CZ
    import pyvista as pv
    # the powder layer as 34 strips across y (they appear behind the recoater)
    layer = 0.040
    strips = []
    ys = np.linspace(-85, 85, 35)
    for i in range(34):
        y0, y1 = ys[i], ys[i + 1]
        hw = math.sqrt(max(85.0 ** 2 - max(abs(y0), abs(y1)) ** 2, 0.0)) if abs(y0) < 85 and abs(y1) < 85 else 0
        hw = max(hw, 6.0)
        m = box_mesh(CX - hw, CX + hw, CY + y0, CY + y1, floor_z - 0.002, floor_z + layer)
        strips.append(add_mesh(sc, f"powder/strip{i}", m, "lpbf_powder", "powder", shown=False))
    # tracks: the bare-plate row (drawn one at a time) and rows A-D (A one at a time; B-D a row at a time)
    tr_names = {}

    def add_track(t, row, frac=1.0, shown=False):
        z0 = floor_z + (layer if row != "bare" else 0.0)
        m = track_mesh(t, z0, pos_x=CX + row_x(t["pos"]), y_mid=CY + ROW_Y[row], frac=frac)
        n = add_mesh(sc, f"track/{t['track_id']}", m, "track_al", f"tracks_{row}", shown=shown)
        tr_names[t["track_id"]] = n
        return n

    for t in d["bare"]:
        add_track(t, "bare")
    for t in d["tracks"]:
        add_track(t, t["block"])
    # denuded bands beside the powder tracks: the plate shows through, a little darker than the bare plate
    den = {}
    for t in d["tracks"]:
        w = 2.6 * t["width_um"] / 1000.0
        x = CX + row_x(t["pos"])
        y = CY + ROW_Y[t["block"]]
        den[t["track_id"]] = add_mesh(sc, f"denuded/{t['track_id']}",
                                      box_mesh(x - w / 2, x + w / 2, y - TRACK_L / 2 - 0.2, y + TRACK_L / 2 + 0.2,
                                               floor_z + layer - 0.001, floor_z + layer + 0.0015),
                                      "denuded", f"den_{t['block']}", shown=False)
    # the target plane (mid-length line) of each row, and the scan arrow: thin markers, shown when named
    marks = []
    for row, yv in ROW_Y.items():
        m = box_mesh(CX - 23.5, CX + 23.5, CY + yv - 0.06, CY + yv + 0.06, floor_z + 0.09, floor_z + 0.10)
        marks.append(add_mesh(sc, f"mark/plane_{row}", m, "hf_label", "marks", shown=False))
    # the beam spot follows a group: the cone (from the model) is re-parented to it
    beam_grp = "beam_spot"
    sc.gmat[beam_grp] = T((CX + 21.0, CY + ROW_Y["bare"] - 6.0, floor_z))
    sc.parent[ch.group("beam")] = beam_grp
    sc.gmat[ch.group("beam")] = T((-CX, -CY, -floor_z))  # the cone is modelled at the chamber's origin
    pool = add_mesh(sc, "beam/pool", pv.Sphere(radius=0.12, center=(0, 0, 0.0)).scale((1.0, 1.8, 0.35)),
                    "track_hot", beam_grp, shown=False)
    au = audit_for(sc, allow=[("track/*", "lpbf_chamber:plate*"), ("powder/*", "lpbf_chamber:*"),
                              ("denuded/*", "*"), ("mark/*", "*"), ("beam/*", "*"), ("lpbf_chamber:beam*", "*"),
                              ("track/*", "powder/*"), ("lpbf_chamber:recoater*", "powder/*"),
                              ("lpbf_chamber:gas*", "*")])

    def beam_on(a):
        def up(u):
            for n in ch.names.get("beam", []):
                sc.alpha[n] = a if u > 0 else sc.alpha[n]
            sc.alpha[pool] = a if u > 0 else sc.alpha[pool]
        return up

    def scan_row(row, tracks, one_by_one=True):
        """update(u): the beam draws the row's tracks in exposure order (outlet side first), each in +y."""
        order = sorted(tracks, key=lambda t: t["pos"])
        n = len(order)

        def up(u):
            s = min(max(u, 0.0), 0.99999) * n
            i = int(s)
            f = s - i
            for j, t in enumerate(order):
                nm = tr_names[t["track_id"]]
                if j < i:
                    if sc.alpha[nm] < 1.0 or sc.__dict__.get("_partial_" + nm):
                        sc.set_mesh(nm, track_mesh(t, floor_z + (layer if row != "bare" else 0.0),
                                                   pos_x=CX + row_x(t["pos"]), y_mid=CY + ROW_Y[row]))
                        sc.__dict__["_partial_" + nm] = False
                    sc.alpha[nm] = 1.0
                    if t["track_id"] in den:
                        sc.alpha[den[t["track_id"]]] = 1.0
                elif j == i:
                    sc.set_mesh(nm, track_mesh(t, floor_z + (layer if row != "bare" else 0.0),
                                               pos_x=CX + row_x(t["pos"]), y_mid=CY + ROW_Y[row], frac=f))
                    sc.__dict__["_partial_" + nm] = True
                    sc.alpha[nm] = 1.0
                    if t["track_id"] in den:
                        sc.alpha[den[t["track_id"]]] = min(1.0, f * 1.5)
                    zs = layer if row != "bare" else 0.0
                    sc.gmat[beam_grp] = T((CX + row_x(t["pos"]), CY + ROW_Y[row] - TRACK_L / 2 + f * TRACK_L,
                                           floor_z + zs))
                else:
                    sc.alpha[nm] = 0.0
            if u >= 1.0:
                for t in order:
                    nm = tr_names[t["track_id"]]
                    sc.set_mesh(nm, track_mesh(t, floor_z + (layer if row != "bare" else 0.0),
                                               pos_x=CX + row_x(t["pos"]), y_mid=CY + ROW_Y[row]))
                    sc.alpha[nm] = 1.0
                    if t["track_id"] in den:
                        sc.alpha[den[t["track_id"]]] = 1.0
        return up

    def show_row(row, a0, a1):
        names = [tr_names[t["track_id"]] for t in (d["bare"] if row == "bare" else
                                                  [x for x in d["tracks"] if x["block"] == row])]
        if row != "bare":
            names += [den[t["track_id"]] for t in d["tracks"] if t["block"] == row]
        return fade(sc, names, a0, a1)

    # ------------------------------------------------------------------------------------- the story
    sc.card("SOP 02 · Single tracks and the heat-source fit",
            ["Melt-pool width, depth and depth/width ratio; the conduction, transition or keyhole regime; balling.",
             "They calibrate the Thermo-Calc AM Module's heat source (absorptivity, beam radius) and the open models "
             "of #238 and #249."],
            seconds=4.0, label="SOP 02",
            note="Draft SOP. Plate layout, cutting and mounting follow the M2 plan of PR #243. Equipment drawn from "
                 "makers' specs and photos; data panels are synthetic examples.")
    # 1. the printer
    top = (-2600.0 - 290.0, -150.0, 1300.0)
    cam_hold(sc, S.look((-2600.0, 0.0, 1150.0), 5600.0, -28.0, 14.0))
    sc.step("Samples", "Utah's Aconity MIDI prints the first Al tracks | P1, Dec 2-3; else the desktop LPBF (#260) "
            "or BYU's M2 (#243)", 4.5, hold=1.5,
            cam_to=S.look((-2600.0 - 290.0, -150.0, 1150.0), 3400.0, -24.0, 13.0),
            labels=[("Aconity MIDI\n2450 x 1500 x 2320 mm", (-2600.0 + 400.0, -750.0, 1900.0), (0.80, 0.18)),
                    ("process chamber\n170 mm build platform", top, (0.18, 0.30))])
    # 2. cut to the build area: backed off, then in
    cam_hold(sc, S.look((CX, CY + 20.0, CZ), 1250.0, -20.0, 38.0))
    sc.step("Samples", "Inside the chamber: the 170 mm build platform | the plate, a recoater, gas from inlet to "
            "outlet", 4.0, hold=1.2, cam_to=S.look((CX, CY + 10.0, CZ), 900.0, -22.0, 40.0),
            update=ch.move({"gas": (0.0, 1.0)}),
            labels=[("gas inlet", label_pt(ch, (-275.0, 0.0, 50.0)), (0.10, 0.30)),
                    ("gas outlet", label_pt(ch, (275.0, 0.0, 70.0)), (0.90, 0.30)),
                    ("recoater blade", label_pt(ch, (-60.0, -300.0, 40.0)), (0.18, 0.80)),
                    ("powder supply", label_pt(ch, (60.0, -215.0, 0.0)), (0.70, 0.86))])
    sc.step("Samples · substrate", "Substrate: a 6061 plate for Al | 6063 too; a Cu alloy for Cu; or a printed pad "
            "of the alloy", 3.5, hold=1.5, cam_to=S.look((CX, CY, CZ), 420.0, -18.0, 52.0),
            update=ch.move({"gas": (1.0, 0.35)}),
            labels=[("6061 plate, 170 mm x 15 mm", label_pt(ch, (-60.0, -50.0, 0.0)), (0.16, 0.25))])
    # 3. bare-plate tracks, one at a time, from the outlet side toward the inlet, each in +y
    row_c = (CX, CY + ROW_Y["bare"], CZ)
    sc.step("Samples · bare-plate tracks", "Bare-plate tracks first: absorptivity of dense metal | no powder yet",
            3.0, hold=0.6, cam_to=S.look(row_c, 95.0, -10.0, 48.0), update=beam_on(1.0),
            labels=[("beam: 1/e2 radius r0 ~40 um", (CX + 21.0, CY + ROW_Y["bare"] - 6.0, CZ + 8.0), (0.80, 0.22))])
    sc.step("Samples · bare-plate tracks", "18 tracks, 12 mm long at 2 mm pitch | exposed outlet side first, "
            "all scanned in +y", 9.0, hold=1.0, update=scan_row("bare", d["bare"]),
            labels=[("gas flow, inlet -> outlet (+x)", (CX + 30.0, CY + ROW_Y["bare"] + 8.0, CZ), (0.82, 0.18)),
                    ("first track: outlet side", (CX + 21.0, CY + ROW_Y["bare"] + 6.0, CZ), (0.86, 0.40))])
    sc.step("Samples · bare-plate tracks", "Each track scanned across the gas flow, never with it | spatter "
            "blows onto finished tracks", 3.5, hold=1.2, update=beam_on(0.0),
            cam_to=S.look(row_c, 80.0, -2.0, 60.0),
            labels=[("12 mm", (CX + 21.0 + 0.6, CY + ROW_Y["bare"], CZ), (0.88, 0.50)),
                    ("2 mm pitch", (CX + 20.0, CY + ROW_Y["bare"] - 6.0, CZ), (0.80, 0.80)),
                    ("10 mm gap between groups of nine", (CX + 0.0, CY + ROW_Y["bare"] - 6.0, CZ), (0.30, 0.82))])
    sc.step("Samples · target plane", "Mid-lengths on one line: the target plane | every section comes from "
            "that line", 3.0, hold=1.2, update=fade(sc, [marks[0]], 0.0, 1.0),
            labels=[("target plane (mid-length)", (CX - 22.0, CY + ROW_Y["bare"], CZ), (0.16, 0.30))])
    # 4. one powder layer
    rec0 = ch.v["recoater"]

    def spread(u):
        ch.v["recoater"] = u
        ch.apply()
        yb = -300.0 + 490.0 * u + 9.5                    # the blade's edge, chamber frame
        for i, n in enumerate(strips):
            sc.alpha[n] = 1.0 if (ys[i + 1]) < yb else 0.0
        sc.alpha[marks[0]] = 0.0 if yb > ROW_Y["bare"] else sc.alpha[marks[0]]
    sc.step("Samples · powder layer", "Then one powder layer, 30-50 um | the recoater spreads a few grams",
            6.0, hold=1.0, update=spread, cam_to=S.look((CX, CY - 40.0, CZ), 650.0, -25.0, 42.0),
            labels=[("one layer, 40 um", (CX - 40.0, CY - 30.0, CZ + 0.04), (0.20, 0.72))])
    _ = rec0
    mass = math.pi * 0.085 ** 2 * 40e-6 * 2700 * 0.5 * 1000
    sc.step("Samples · powder", f"About {mass:.1f} g covers the 170 mm plate | the ~100-300 g atomized per alloy "
            "is plenty", 3.5, hold=1.2, cam_to=S.look((CX, CY, CZ), 380.0, -18.0, 55.0),
            update=ch.move({"recoater": (1.0, 0.0)}))
    # 5. Sobol blocks on the powder: row A drawn track by track, B-D a row at a time
    sc.panel("design", _cached(panel_design, d), rect=(0.60, 0.11, 0.38), alpha=0.0)
    sc.step("Samples · Sobol blocks", "Scrambled-Sobol power-speed blocks, not a grid | 16 settings + 2 controls "
            "per row", 4.0, hold=1.5, update=sc.fade_panel("design", 0.0, 1.0),
            cam_to=S.look((CX - 25.0, CY, CZ), 260.0, -10.0, 58.0))
    rowA = (CX, CY + ROW_Y["A"], CZ)
    sc.step("Samples · Sobol blocks", "Block A: random positions, controls included | one layer, outlet side "
            "first", 8.0, hold=0.8, update=S.together(beam_on(1.0), scan_row("A", [t for t in d["tracks"]
                                                                                  if t["block"] == "A"])),
            cam_to=S.look(rowA, 110.0, -12.0, 50.0),
            labels=[("control set (2 per row)", (CX + row_x([t for t in d["tracks"] if t["block"] == "A"
                                                               and t["control"]][0]["pos"]),
                                                  CY + ROW_Y["A"] + 6.0, CZ), (0.82, 0.22))])
    sc.step("Samples · Sobol blocks", "Blocks B, C and D: 72 tracks on the plate | denuded powder beside each track",
            5.0, hold=1.5, update=S.together(beam_on(0.0), S.staged((0.0, 0.33, show_row("B", 0, 1)),
                                                                     (0.33, 0.66, show_row("C", 0, 1)),
                                                                     (0.66, 1.0, show_row("D", 0, 1)))),
            cam_to=S.look((CX, CY + 5.0, CZ), 210.0, -14.0, 62.0),
            labels=[("bare-plate row", (CX - 21.0, CY + ROW_Y["bare"], CZ), (0.14, 0.20)),
                    ("Sobol blocks A-D", (CX - 21.0, CY + ROW_Y["C"], CZ + 0.04), (0.14, 0.75))])
    sc.step("Samples · two kinds", "Per alloy: bare-plate tracks, and one-layer tracks | the second reproduces LPBF",
            4.0, hold=2.0, update=sc.fade_panel("design", 1.0, 0.0),
            cam_to=S.look((CX, CY, CZ), 330.0, -20.0, 50.0))
    sc.save()
    au.save()


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "sop02_c1"
    if arg == "data":
        dd = data(rebuild=True)
        print(json.dumps({k: dd[k] for k in ("eta_fit", "rms_rel", "counts", "ke_threshold", "am_vs_measured")},
                         indent=1))
    elif arg == "join":
        parts = [c for c in sorted(CHAPTERS) if (S.OUT / "mp4" / f"{c}.mp4").exists()]
        print(S.join("sop02", parts))
        print(S.contact_sheet("sop02"))
        print(S.preview_gif("sop02"))
    else:
        run(arg)
