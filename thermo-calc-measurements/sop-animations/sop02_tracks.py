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
    v = np.exp(np.log(500.0) + (np.log(3000.0) - np.log(500.0)) * sob[:, 1])
    ctrl = (300.0, 1300.0)
    fields = {}

    def field(vv):
        key = round(float(vv), 2)
        if key not in fields:
            fields[key] = mp.TrackField(vv * 1e-3, r0, k, rho, cp)
        return fields[key]

    def make(PP, vv, sigma_w=0.018, bare=False):
        ke0 = mp.keyhole_number(0.30, PP, vv * 1e-3, r0, k, rho, cp, dT)
        eta_eff = 0.30 + 0.24 / (1.0 + math.exp(-(ke0 - 12.0) / 2.5))
        if bare:
            eta_eff *= 0.92                              # a ground plate takes a little less than a powder bed
        W, D = field(vv).pool(eta_eff, PP, dT)
        kh = min(1.0 + 0.16 * max(0.0, ke0 - 8.5), 2.8)
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
                 window=dict(P_W=[100, 370], v_mm_s=[500, 3000]))
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
    fig.text(0.985, 0.895, text, ha="right", va="top", fontsize=8.5, color="white", weight="bold",
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
    fig, plt = _fig(5.2, 3.6)
    ax = fig.add_axes([0.13, 0.15, 0.52, 0.64])
    marks = {"A": "o", "B": "s", "C": "^", "D": "D"}
    n_show = int(round(4 * u + 0.49))
    for b in "ABCD"[:max(1, n_show)]:
        pts = [(t["v_mm_s"], t["P_W"]) for t in d["tracks"] if t["block"] == b and not t["control"]]
        ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=26, marker=marks[b], c=C1, edgecolors="white",
                   linewidths=0.8, label=f"block {b}: 16", zorder=3)
    c = d["control_set"]
    ax.scatter([c["v_mm_s"]], [c["P_W"]], s=90, marker="*", c=C2, edgecolors="white", linewidths=0.8,
               label="control,\n2 per block", zorder=4)
    ax.set_xscale("log")
    ax.set_xlabel("scan speed v (mm/s)")
    ax.set_ylabel("laser power P (W)")
    ax.set_xticks([500, 1000, 2000, 3000])
    ax.set_xticklabels(["500", "1000", "2000", "3000"])
    ax.minorticks_off()
    _axes(ax)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=7.5, frameon=False)
    fig.text(0.02, 0.95, "Power-speed design: scrambled Sobol, not a grid", fontsize=10.5, weight="bold", color=INK)
    _badge(fig, "design, illustrative window", "window 100-370 W, 500-3000 mm/s (log); set it from the AM Module map")
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
    ax = fig.add_axes([0.03, 0.10, 0.94, 0.68])
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
    ax = fig.add_axes([0.04, 0.10, 0.92, 0.68])
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
    ax = fig.add_axes([0.14, 0.15, 0.54, 0.64])
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
    ax = fig.add_axes([0.14, 0.15, 0.54, 0.64])
    cols = {"conduction": C1, "transition": C2, "keyhole": C3}
    for r, c in cols.items():
        ts = [t for t in d["tracks"] if t["regime"] == r and t["eta_w"] is not None]
        ax.scatter([t["P_W"] / t["v_mm_s"] for t in ts], [t["eta_w"] for t in ts], s=20, c=c, edgecolors="white",
                   linewidths=0.6, label=r, zorder=3)
    ax.axhline(d["eta_fit"], color=INK2, lw=0.9, ls="--")
    ax.text(0.02, d["eta_fit"] + 0.008, "fitted eta", color=INK2, fontsize=7.5, transform=ax.get_yaxis_transform())
    ax.set_xscale("log")
    ax.set_xticks([0.05, 0.1, 0.2, 0.5, 1.0])
    ax.set_xticklabels(["0.05", "0.1", "0.2", "0.5", "1"])
    ax.minorticks_off()
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
    ax = fig.add_axes([0.14, 0.15, 0.54, 0.64])
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
    ax.set_xticks([3, 5, 10, 20, 30])
    ax.set_xticklabels(["3", "5", "10", "20", "30"])
    ax.minorticks_off()
    ax.set_xlabel("keyhole number Ke (Gan et al. 2021)")
    ax.set_ylabel("depth / width")
    _axes(ax)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=7.5, frameon=False)
    fig.text(0.02, 0.95, "Ke per track, and one threshold for keyhole onset", fontsize=10.5, weight="bold", color=INK)
    _badge(fig, "synthetic example", f"threshold misclassifies {d['ke_errors']} of {len(d['tracks'])} tracks (#249)")
    return S.fig_image(fig)


def panel_am(d, u=1.0):
    fig, plt = _fig(5.2, 3.6)
    ax = fig.add_axes([0.14, 0.15, 0.50, 0.64])
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


def disc_band(cx, cy, r, y0, y1, z0, z1, n=8):
    """The part of a disc (centre cx, cy; radius r) between y0 and y1 (relative), as a slab from z0 to z1."""
    import pyvista as pv
    yy = np.linspace(max(y0, -r + 1e-6), min(y1, r - 1e-6), n)
    xr = np.sqrt(np.maximum(r * r - yy ** 2, 0.0))
    pts = [(cx + x, cy + y) for x, y in zip(xr, yy)] + [(cx - x, cy + y) for x, y in zip(xr[::-1], yy[::-1])]
    poly = pv.PolyData(np.array([(x, y, z0) for x, y in pts]), faces=np.r_[len(pts), np.arange(len(pts))])
    return poly.triangulate().extrude((0, 0, z1 - z0), capping=True).triangulate().clean()


def drop(sc, names):
    """Take actors out of the scene for good (Rig.apply() would otherwise bring a hidden piece back)."""
    for n in list(names):
        a = sc.actors.pop(n, None)
        if a is None:
            continue
        sc.pl.remove_actor(a)
        for dct in (sc.group_of, sc.alpha, sc.base_alpha):
            dct.pop(n, None)
        sc.__dict__.get("_keep", {}).pop(n, None)
        sc.__dict__.get("_sent", {}).pop(n, None)


def drop_pieces(rig, pieces=(), match=None):
    """Drop a rig's pieces, or (match) any of its actors whose name contains one of the strings."""
    for pc in pieces:
        drop(rig.sc, rig.names.get(pc, []))
        rig.names[pc] = []
    if match:
        for pc, ns in rig.names.items():
            gone = [n for n in ns if any(m in n for m in match)]
            drop(rig.sc, gone)
            rig.names[pc] = [n for n in ns if n not in gone]


def vhx_clear(vhx):
    """The VHX as a plain microscope: no loading slide, bar or readout (byu-vcl's additions for the arm)."""
    drop_pieces(vhx, ("carrier", "sample", "bar", "lift", "readout"), match=("turntable/r8c_steel",))


def person(sc, name="op", **kw):
    import people
    p = people.Person(sc, name)
    p.set(**kw)
    return p


def walk(p, x0, y0, x1, y1, hd=None, carry=None, turn=True):
    """update(u): walk in steps from (x0, y0) to (x1, y1), one gait cycle per 1016 mm, turning to the way it goes
    and back to face the bench (hd 0) at the end; carry=(dx, dy, z): the right hand held there in the body's frame
    (something carried in front)."""
    dist = math.hypot(x1 - x0, y1 - y0)
    hd_go = math.degrees(math.atan2(-(x1 - x0), (y1 - y0))) if hd is None else hd
    cycles = max(1.0, round(dist / p.STRIDE * 2) / 2)

    def up(u):
        amp = min(1.0, 4 * u, 4 * (1 - u))
        h = hd_go
        if turn and hd is None:
            k = min(1.0, u / 0.15, (1.0 - u) / 0.15)
            h = hd_go * ease_(k)
        p.set(x=x0 + (x1 - x0) * u, y=y0 + (y1 - y0) * u, hd=h, phase=2 * math.pi * cycles * u, amp=amp)
        if carry is not None:
            F = p.frame()
            p.set(hands={"r": tuple((F @ np.r_[carry[0], carry[1], carry[2], 1.0])[:3])})
    return up


def ease_(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


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
        m = disc_band(CX, CY, 84.5, ys[i], ys[i + 1], floor_z - 0.002, floor_z + layer)
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
    cam_hold(sc, S.look((-2600.0, 0.0, 1150.0), 9000.0, -28.0, 12.0))
    sc.step("Samples", "First Al tracks: Utah's Aconity MIDI, or the desktop LPBF | P1 at Utah, Dec 2-3; the "
            "desktop machine is #260; the layout follows BYU's M2 plan (#243)", 4.5, hold=1.5,
            cam_to=S.look((-2600.0 - 150.0, -150.0, 1150.0), 6200.0, -24.0, 12.0),
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
            update=ch.move({"gas": (1.0, 0.0)}),
            labels=[("6061 plate, 170 mm x 15 mm", label_pt(ch, (-60.0, -50.0, 0.0)), (0.16, 0.25))])
    # 3. bare-plate tracks, one at a time, from the outlet side toward the inlet, each in +y
    row_c = (CX, CY + ROW_Y["bare"], CZ)
    sc.step("Samples · bare-plate tracks", "Bare-plate tracks first: absorptivity of dense metal | no powder yet",
            3.0, hold=0.6, cam_to=S.look(row_c, 95.0, -10.0, 48.0), update=beam_on(1.0),
            labels=[("beam: ~70 um spot at focus (r0 ~35 um)", (CX + 21.0, CY + ROW_Y["bare"] - 6.0, CZ + 8.0),
                     (0.78, 0.22))])
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
    sc.panel("design", _cached(panel_design, d), rect=(0.68, 0.09, 0.30), alpha=0.0)
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
                                                  CY + ROW_Y["A"] + 6.0, CZ), (0.40, 0.16))])
    sc.step("Samples · Sobol blocks", "Blocks B, C and D: 72 tracks on the plate | denuded powder beside each track",
            5.0, hold=1.5, update=S.together(beam_on(0.0), S.staged((0.0, 0.33, show_row("B", 0, 1)),
                                                                     (0.33, 0.66, show_row("C", 0, 1)),
                                                                     (0.66, 1.0, show_row("D", 0, 1)))),
            cam_to=S.look((CX, CY + 5.0, CZ), 210.0, -14.0, 62.0),
            labels=[("bare-plate row (under the powder now)", (CX - 21.0, CY + ROW_Y["bare"], CZ), (0.14, 0.20)),
                    ("Sobol blocks A-D", (CX - 21.0, CY + ROW_Y["C"], CZ + 0.04), (0.14, 0.75))])
    sc.step("Samples · two kinds", "Per alloy: bare-plate tracks, and one-layer tracks | the second reproduces LPBF",
            4.0, hold=2.0, update=sc.fade_panel("design", 1.0, 0.0),
            cam_to=S.look((CX, CY, CZ), 330.0, -20.0, 50.0))
    sc.save()
    au.save()



# ================================================================================= shared props for c2-c7
PLATE_D, PLATE_T, LAYER = 170.0, 15.0, 0.040


def plate_meshes(d, cx, cy, z, powder=True, rows=("bare", "A", "B", "C", "D")):
    """{name: (mesh, material)}: the printed plate with its tracks (and its one layer of powder), centred (cx, cy),
    standing on z."""
    import pyvista as pv
    out = {}
    out["plate"] = (pv.Cylinder(center=(cx, cy, z + PLATE_T / 2), direction=(0, 0, 1), radius=PLATE_D / 2,
                                height=PLATE_T, resolution=96).triangulate(), "plate_6061")
    zt = z + PLATE_T
    if powder:
        # the layer, with a window cut out round each powder row (the denuded bands and tracks show there)
        out["powder"] = (pv.Cylinder(center=(cx, cy, zt + LAYER / 2), direction=(0, 0, 1), radius=PLATE_D / 2 - 0.5,
                                     height=LAYER, resolution=96).triangulate(), "lpbf_powder")
    tr = []
    dn = []
    for t in d["bare"]:
        if "bare" in rows:
            tr.append(track_mesh(t, zt, pos_x=cx + row_x(t["pos"]), y_mid=cy + ROW_Y["bare"]))
    for t in d["tracks"]:
        if t["block"] in rows:
            tr.append(track_mesh(t, zt + (LAYER if powder else 0.0), pos_x=cx + row_x(t["pos"]),
                                 y_mid=cy + ROW_Y[t["block"]]))
            if powder:
                w = 2.6 * t["width_um"] / 1000.0
                x = cx + row_x(t["pos"])
                y = cy + ROW_Y[t["block"]]
                dn.append(box_mesh(x - w / 2, x + w / 2, y - TRACK_L / 2 - 0.2, y + TRACK_L / 2 + 0.2,
                                   zt + LAYER - 0.001, zt + LAYER + 0.0015))
    out["tracks"] = (S.merge(tr), "track_al")
    if dn:
        out["denuded"] = (S.merge(dn), "denuded")
    return out


def piece_meshes(d, row, half, origin, tracks_up=True):
    """A piece of nine tracks cut from the strip: 22 mm along its row (local y), 10 mm along the tracks (local x,
    the target plane 3 mm from the +x face), 10 mm deep (local z, the tracks on top). Local origin: the piece's
    centre on its top face. Returns {name: (mesh, material)} placed by the 4x4 `origin`."""
    out = {}
    body = box_mesh(-7.0, 3.0, -11.0, 11.0, -10.0, 0.0)
    tr = []
    ts = sorted([t for t in d["tracks"] if t["block"] == row], key=lambda t: t["pos"])[9 * half: 9 * half + 9]
    for k, t in enumerate(ts):
        m = track_mesh(t, 0.0, length=9.0, pos_x=0.0, y_mid=0.0)
        m = m.rotate_z(90.0, point=(0, 0, 0), inplace=False).translate((-1.5, -8.0 + 2.0 * k, 0.0), inplace=False)
        tr.append(m)
    out["piece"] = (body, "plate_6061")
    out["tracks"] = (S.merge(tr), "track_al")
    for k, (m, mat) in out.items():
        out[k] = (m.transform(np.asarray(origin, float), inplace=False), mat)
    return out


def mount_meshes(face_up=True):
    """The conductive hot mount (38.1 mm, 20 mm tall: the MX400's 1.5 in mould) with the two pieces of one row
    in its face, local origin at the centre of its base; face_up puts the polished face on top."""
    import pyvista as pv
    out = {}
    out["mount"] = (pv.Cylinder(center=(0, 0, 10.0), direction=(0, 0, 1), radius=38.1 / 2, height=20.0,
                                resolution=72).triangulate(), "mount")
    z = 20.0 if face_up else 0.0
    faces = []
    for dx in (-5.6, 5.6):
        faces.append(box_mesh(dx - 5.0, dx + 5.0, -11.0, 11.0, z - 0.05 if face_up else -0.05,
                              z + 0.06 if face_up else 0.06))
    out["faces"] = (S.merge(faces), "sample")
    return out


def add_set(sc, meshes: dict, prefix: str, group: str, at=None, parent=None, shown=True):
    names = []
    for k, (m, mat) in meshes.items():
        names.append(add_mesh(sc, f"{prefix}/{k}", m, mat, group, shown=shown))
    if at is not None:
        sc.gmat[group] = at
    if parent is not None:
        sc.parent[group] = parent
    return names


# ================================================================================= chapter 2: top views
@chapter("sop02_c2")
def c2():
    d = data()
    sc = S.SOPScene("sop02_c2", TITLE)
    S.room(sc, x0=-1100.0, x1=1100.0)
    vhx = S.place(sc, "vhx", 0.0, 0.0)
    vhx_clear(vhx)
    zs = BENCH_H + 232.0                                # the stage disk's top
    plate = add_set(sc, plate_meshes(d, 0.0, 0.0, 0.0), "plate", "plate",
                    at=T((0.0, -40.0, 232.0)), parent=vhx.group("turntable"))
    vhx.set(table=0.10)                                 # the plate's top at the focal point
    au = audit_for(sc, allow=[("plate/*", "vhx:turntable*"), ("plate/*", "vhx:table*"),
                              ("vhx:table*", "vhx:turntable*"), ("vhx:body*", "vhx:table*")])
    stage_c = (0.0, -40.0, zs + PLATE_T)
    sc.card("Preparation 1 · Image first", ["Top views of every track at 50-100x, before any cutting: continuity, "
                                             "balling and the denuded band."], seconds=2.5, label="Preparation 1")
    cam_hold(sc, S.look((0.0, 0.0, BENCH_H + 250.0), 3600.0, -30.0, 14.0))
    sc.step("Preparation 1", "Image first: top views of every track | Keyence VHX-7000 digital microscope", 4.0,
            hold=1.2, cam_to=S.look((0.0, -20.0, BENCH_H + 280.0), 1900.0, -34.0, 18.0),
            labels=[("printed plate, 170 mm, on the XY stage", (60.0, -100.0, zs + PLATE_T), (0.72, 0.70)),
                    ("VH-ZST zoom lens, 20-2000x", (27.0, -40.0, zs + 160.0), (0.70, 0.20))])
    sc.step("Preparation 1", "Lifted out flat, powder layer left on | before any cutting", 3.5, hold=1.0,
            cam_to=S.look(stage_c, 420.0, -55.0, 28.0))
    sc.panel("top", _cached(panel_topview, d), rect=(0.68, 0.09, 0.30), alpha=0.0)

    def tour(u):
        # the motorized stage brings each row under the lens: a few stops along the rows (ours: no XY joint drawn)
        stops = [(-21.0, ROW_Y["bare"]), (21.0, ROW_Y["bare"]), (21.0, ROW_Y["A"]), (-21.0, ROW_Y["A"]),
                 (-21.0, ROW_Y["B"]), (21.0, ROW_Y["C"]), (0.0, 0.0)]
        s = min(u, 0.9999) * (len(stops) - 1)
        i = int(s)
        f = s - i
        x = stops[i][0] + (stops[i + 1][0] - stops[i][0]) * f
        y = stops[i][1] + (stops[i + 1][1] - stops[i][1]) * f
        sc.gmat["plate"] = T((-x, -40.0 - y, 232.0))
    sc.step("Preparation 1", "Each track at 50-100x | continuity, balling, denudation width", 6.0, hold=1.0,
            update=S.together(tour, sc.fade_panel("top", 0.0, 1.0)),
            cam_to=S.look((0.0, -40.0, zs + PLATE_T), 260.0, -62.0, 30.0))
    sc.step("Preparation 1", "Denuded band beside each track | sets the pitch: 2 mm now, 1.5-2.5 mm later",
            4.0, hold=1.5)
    pw = [n for n in plate if "/powder" in n or "/denuded" in n]
    sc.step("Preparation 1", "Then the loose powder off | the bare-plate row shows again", 3.5, hold=1.0,
            update=S.together(fade(sc, pw, 1.0, 0.0), sc.fade_panel("top", 1.0, 0.0)),
            cam_to=S.look((0.0, -40.0, zs + PLATE_T), 330.0, -40.0, 42.0))

    def tour2(u):
        x = -21.0 + 42.0 * u
        sc.gmat["plate"] = T((-x, -40.0 - ROW_Y["bare"], 232.0))
    sc.step("Preparation 1", "Bare-plate tracks: continuity and width | every one logged by row and position",
            4.0, hold=1.0, update=tour2, cam_to=S.look((0.0, -40.0, zs + PLATE_T), 240.0, -62.0, 30.0))
    sc.step("Preparation 1", "All 90 tracks imaged | before the plate is cut", 3.0, hold=1.0,
            update=lambda u: sc.gmat.__setitem__("plate", T((0.0, -40.0, 232.0))) if u > 0.5 else None,
            cam_to=S.look((0.0, -20.0, BENCH_H + 260.0), 1100.0, -30.0, 22.0))
    sc.save()
    au.save()


# ================================================================================= chapter 3: section and mount
@chapter("sop02_c3")
def c3():
    import models_track as MT
    d = data()
    sc = S.SOPScene("sop02_c3", TITLE)
    S.room(sc, x0=-1300.0, x1=1300.0)
    saw = S.place(sc, "precision_saw", -120.0, -10.0)
    press = S.place(sc, "mount_press", 620.0, 40.0)
    sp = MT.saw_points()
    drop_pieces(press, ("specimen",))
    saw.set(specimen=0.0, slice=0.0)
    # the plate on a mat at the left; row A's strip: 3 mm on one side of the target plane, 7 mm on the other
    mat_c = (-620.0, -140.0)
    add_mesh(sc, "mat", box_mesh(mat_c[0] - 150, mat_c[0] + 150, mat_c[1] - 120, mat_c[1] + 120, BENCH_H,
                                 BENCH_H + 3.0), "rubber", "mat")
    pz = BENCH_H + 3.0
    plate_names = add_set(sc, plate_meshes(d, mat_c[0], mat_c[1], pz, powder=False), "plate", "plate")
    ya = mat_c[1] + ROW_Y["A"]
    sx0, sx1 = mat_c[0] - 24.0, mat_c[0] + 24.0
    cut_lines = [add_mesh(sc, f"cutline/{k}", box_mesh(sx0 - 4, sx1 + 4, yy - 0.4, yy + 0.4, pz + PLATE_T + 0.05,
                                                       pz + PLATE_T + 0.12), "hf_label", "cutlines", shown=False)
                 for k, yy in enumerate((ya - 7.0, ya + 3.0))]
    strip = add_mesh(sc, "strip/block", box_mesh(sx0, sx1, ya - 7.0, ya + 3.0, pz, pz + PLATE_T), "plate_6061",
                     "strip", shown=False)
    strip_tr = [add_mesh(sc, "strip/tracks", S.merge([
        track_mesh(t, pz + PLATE_T, pos_x=mat_c[0] + row_x(t["pos"]), y_mid=ya)
        for t in d["tracks"] if t["block"] == "A"]).clip_box((-1e5, 1e5, ya - 7.0, ya + 3.0, -1e5, 1e5),
                                                            invert=False), "track_al", "strip", shown=False)]
    # the two pieces of nine tracks (22 x 10 x 10 mm) on the mat: local x across the tracks' target plane
    # (+x = the 3 mm side, toward -y on the plate), local y along the row (world x), tracks on top
    pieces = {}
    for h in (0, 1):
        at = T((mat_c[0] - 12.0 + 24.0 * h, ya - 4.0, pz + 10.0)) @ R((0, 0, 1), -90.0)
        pieces[h] = add_set(sc, piece_meshes(d, "A", h, np.eye(4)), f"piece{h}", f"piece{h}", at=at, shown=False)
    op = person(sc, "op", x=-40.0, y=-650.0, hd=0.0)
    au = audit_for(sc, allow=[("op/*glove*", "piece*"), ("piece*", "precision_saw:arm*"),
                              ("op/*glove*", "precision_saw:arm*"), ("op/*glove*", "precision_saw:weight*"),
                              ("precision_saw:arm*", "precision_saw:specimen*"),
                              ("precision_saw:weight*", "precision_saw:arm*"), ("op/*glove*", "precision_saw:specimen*"),
                              ("mount_press:pour*", "mount_press:*"), ("mount_press:charge*", "mount_press:stopper*"),
                              ("mount_press:doser*", "mount_press:body*"),
                              ("mount_press:charge*", "mount_press:closure*"),
                              ("piece*", "mat*"), ("strip/*", "*"), ("plate/*", "mat*"), ("cutline/*", "*"),
                              ("precision_saw:slice*", "*"), ("precision_saw:specimen*", "precision_saw:wheel*"),
                              ("precision_saw:wheel*", "precision_saw:tank*"), ("pair*", "mount_press:*"), ("op/*glove*", "pair*"),
                              ("op/*glove*", "precision_saw:cover*"), ("op/*glove*", "precision_saw:carriage*"),
                              ("op/*glove*", "precision_saw:body*"), ("op/*glove*", "mount_press:*")])
    # -------------------------------------------------------------------------- the strip
    sc.card("Preparation 2 · Section and hot-mount", ["Each track is cut at mid-length and mounted in conductive "
                                                       "compound (#243 section 3)."], seconds=2.5, label="Preparation 2")
    cam_hold(sc, S.look((-200.0, 0.0, BENCH_H + 300.0), 4200.0, -22.0, 14.0))
    pc = (mat_c[0], mat_c[1], pz + PLATE_T)
    sc.step("Preparation 2", "Section every track at mid-length | the rows are cut out of the plate first", 4.0,
            hold=1.0, cam_to=S.look(pc, 560.0, -30.0, 46.0),
            labels=[("printed plate, depowdered", (mat_c[0] + 60.0, mat_c[1] - 60.0, pz + PLATE_T), (0.75, 0.75))])
    sc.step("Preparation 2 · strip", "A 10 mm strip holds row A's mid-lengths | 3 mm one side of the plane, 7 mm "
            "the other", 4.0, hold=1.2, update=fade(sc, cut_lines, 0.0, 1.0),
            cam_to=S.look((mat_c[0], ya, pz + PLATE_T), 160.0, -20.0, 55.0),
            labels=[("bandsaw cut lines", (sx1 + 4.0, ya + 3.0, pz + PLATE_T), (0.80, 0.25)),
                    ("target plane", (sx0, ya, pz + PLATE_T), (0.18, 0.35))])
    sc.step("Preparation 2 · strip", "Cut out on a bandsaw (not drawn) | no bandsaw cut within 3 mm of the plane",
            3.5, hold=1.0, update=S.together(fade(sc, plate_names + cut_lines, 1.0, 0.0),
                                             fade(sc, [strip] + strip_tr, 0.0, 1.0)),
            cam_to=S.look((mat_c[0], ya, pz + 10.0), 200.0, -25.0, 45.0))
    sc.step("Preparation 2 · strip", "Two pieces of nine tracks, about 22 mm each | cut ~10 mm below the tracks",
            3.0, hold=1.2, update=S.together(fade(sc, [strip] + strip_tr, 1.0, 0.0),
                                             fade(sc, pieces[0] + pieces[1], 0.0, 1.0)),
            labels=[("piece: 22 x 10 x 10 mm, nine tracks", (mat_c[0] - 12.0, ya - 4.0, pz + 10.0), (0.22, 0.25))])
    # -------------------------------------------------------------------------- the saw
    vise = np.array(label_pt(saw, sp["strip"]))
    saw_view = S.look(vise + np.array([0.0, 0.0, 20.0]), 620.0, 58.0, 30.0)
    cam_hold(sc, S.look((-120.0, -10.0, BENCH_H + 200.0), 2300.0, 35.0, 18.0))
    sc.step("Preparation 2 · saw", "The fine cut: a low-speed diamond saw | LECO VC50, 127 mm blade, 0-500 rpm",
            3.5, hold=1.0, cam_to=S.look((-60.0, -40.0, BENCH_H + 170.0), 1250.0, 40.0, 22.0),
            labels=[("LECO VC50, 432 x 457 x 330 mm", label_pt(saw, (-120.0, -220.0, 168.0)), (0.20, 0.22)),
                    ("micrometer", label_pt(saw, (250.0, 125.0, 220.0)), (0.86, 0.30)),
                    ("coolant tank: cutting oil", label_pt(saw, (125.0, -235.0, 60.0)), (0.80, 0.82))])
    gx0, gx1, gy0, gy1, gz0, gz1 = sp["guard"]
    cf_local = ((gx0 + gx1) / 2, gy0 - 10.0, gz1 + 30.0)          # the cover's front, where a hand lifts it
    cov_front = np.array(label_pt(saw, cf_local, "cover"))

    def cover_by_hand(a, b, lean=None):
        """update(u): the cover from a to b, the right hand on its front edge all the way (it follows the arc)."""
        l0 = {}

        def up(u):
            saw.v["cover"] = a + (b - a) * u
            saw.apply()
            kw = dict(hands={"r": tuple(label_pt(saw, cf_local, "cover"))}, grip={"r": 0.7})
            if lean is not None:
                l0.setdefault("l", op.st["lean"])
                kw["lean"] = l0["l"] + (lean - l0["l"]) * u
            op.set(**kw)
        return up
    sc.step("Preparation 2 · saw", "Cover up | the arm and its vise over the blade", 3.0, hold=0.4,
            update=S.staged((0.0, 0.4, reach(op, "r", None, cov_front, grip=(0.3, 0.7), look=tuple(vise), lean=14.0)),
                            (0.4, 1.0, cover_by_hand(0.0, 1.0))),
            cam_to=saw_view)
    cov_up = np.array(label_pt(saw, cf_local, "cover"))
    # to the mat for the first piece, and back
    g1 = "piece0"
    pick = np.array(sc.world(g1)[:3, 3]) + np.array([0.0, -2.0, 34.0])
    xm = float(pick[0]) - 170.0                               # the right shoulder over the piece
    sc.step("Preparation 2 · saw", "Fetch the first piece from the mat", 3.5, hold=0.0,
            update=S.together(S.staged((0.0, 0.3, reach(op, "r", cov_up, None, grip=(0.7, 0.3), lean=0.0))),
                              S.staged((0.25, 1.0, walk(op, -40.0, -650.0, xm, -650.0)))),
            cam_to=S.look(((xm - 40.0) / 2, -300.0, BENCH_H + 200.0), 2400.0, 28.0, 20.0))
    op.set(hd=0.0, amp=0.0)
    pick = pick + np.array([0.0, 0.0, 58.0])
    sc.step("Preparation 2 · saw", "Pick it up by its ends", 2.0, hold=0.2,
            update=reach(op, "r", None, pick, grip=(0.3, 0.6), look=tuple(pick), lean=22.0),
            cam_to=S.look(pick + np.array([-60.0, 0.0, 120.0]), 1400.0, 58.0, 28.0))
    op.hold("r", g1)
    carry = (230.0, 330.0, 1060.0)
    sc.step("Preparation 2 · saw", "Back to the saw", 3.5, hold=0.0,
            update=S.together(S.staged((0.0, 0.12, reach(op, "r", pick, pick + np.array([0.0, 0.0, 120.0]),
                                                         grip=(0.8, 0.8), lean=8.0)),
                                       (0.12, 0.25, reach(op, "r", pick + np.array([0.0, 0.0, 120.0]),
                                                          (op.frame() @ np.r_[carry, 1.0])[:3], grip=(0.8, 0.8),
                                                          lean=0.0))),
                              S.staged((0.25, 1.0, walk(op, xm, -650.0, -40.0, -650.0, carry=carry)))),
            cam_to=S.look(((xm - 40.0) / 2, -300.0, BENCH_H + 200.0), 2400.0, 28.0, 20.0))
    op.set(hd=0.0, amp=0.0)
    # into the vise: the piece's final pose is the saw's own specimen (arm up for loading); the hand ends over it
    saw.set(arm=-1.0)
    spec_pose = sc.world(saw.group("specimen"))
    vise_hand = np.array(label_pt(saw, (sp["strip"][0], sp["strip"][1], sp["strip"][2] + 60.0), "arm"))
    over = vise_hand + np.array([-30.0, -70.0, 180.0])
    start_pose = sc.world(g1)
    hand_now = op.hand_point("r")
    up_first = hand_now + np.array([0.0, 0.0, 150.0])
    sc.step("Preparation 2 · saw", "Into the vise, the 3 mm side toward the blade | tracks up", 3.5, hold=0.2,
            update=S.staged((0.0, 0.3, reach(op, "r", hand_now, up_first, grip=(0.8, 0.8), look=tuple(vise))),
                            (0.3, 0.7, reach(op, "r", up_first, over, grip=(0.8, 0.8), lean=16.0)),
                            (0.7, 1.0, reach(op, "r", over, vise_hand, grip=(0.8, 0.6)))), cam_to=saw_view)
    op.let_go("r")

    bt = sp["blade_top"]
    seat_tgt = sc.world(saw.group("arm")) @ T((bt[0] - 0.5, bt[1], bt[2] + 15.0))
    seat_from = {}

    def seat(u):
        # the piece settles into the jaws (the hand's last few mm), then the saw's own specimen takes over
        if "m" not in seat_from:
            seat_from["m"] = sc.world(g1).copy()
        sc.gmat[g1] = S.blend(seat_from["m"], seat_tgt, u)
        if u >= 0.999:
            for n in pieces[0]:
                sc.alpha[n] = 0.0
            saw.set(specimen=1.0, slice=1.0)
    _ = start_pose
    sc.gmat[g1] = sc.world(g1)
    sc.parent.pop(g1, None)
    knob = np.array(label_pt(saw, (sp["strip"][0] - 12.0, sp["strip"][1] - 78.0, sp["strip"][2] + 16.0), "arm"))
    sc.step("Preparation 2 · saw", "Tighten the vise's knurled screw", 2.5, hold=0.3,
            update=S.together(S.staged((0.0, 0.6, seat)),
                              reach(op, "r", vise_hand, knob, grip=(0.8, 0.9), look=tuple(vise))),
            labels=[("piece in the vise", tuple(vise), (0.20, 0.30))])
    mic = np.array(label_pt(saw, (sp["pivot"][0] + 170.0, sp["pivot"][1] + 6.0, sp["pivot"][2] - 40.0)))
    sc.step("Preparation 2 · saw", "Micrometer: cut 0.5 mm from the target plane | on the 3 mm side",
            3.0, hold=0.6, update=S.together(reach(op, "r", knob, mic, grip=(0.9, 0.8), look=tuple(mic)),
                                             S.staged((0.5, 1.0, saw.move({"arm": (-1.0, 0.0)})))),
            labels=[("micrometer, 0.01 mm divisions", tuple(mic), (0.84, 0.30))])
    start_btn = np.array(label_pt(saw, (-178.0 + 0.13 * 247.0 + 39.0, -224.0, 17.0 + 0.72 * 151.0 + 8.0)))
    clear_front = start_btn + np.array([0.0, -120.0, 60.0])
    sc.step("Preparation 2 · saw", "Cover down, START | the sliding weight sets the load", 3.5, hold=0.4,
            update=S.together(S.staged((0.0, 0.2, saw.move({"weight": (0.0, 0.4)}))),
                              S.staged((0.0, 0.25, reach(op, "r", mic, cov_up, grip=(0.8, 0.7))),
                                       (0.25, 0.55, cover_by_hand(1.0, 0.0)),
                                       (0.55, 0.75, reach(op, "r", cov_front, clear_front, grip=(0.7, 0.4))),
                                       (0.75, 1.0, reach(op, "r", clear_front, start_btn, grip=(0.4, 0.2),
                                                         lean=12.0)))),
            cam_to=S.look(vise + np.array([-150.0, -120.0, -20.0]), 1350.0, 66.0, 22.0))

    def cutting(u):
        saw.v["wheel"] = 3.0 * u
        saw.v["arm"] = min(1.0, 1.15 * u)
        saw.apply()
    sc.step("Preparation 2 · saw", "~300 rpm, blade dipping in cutting oil | the arm feeds the piece through", 7.0,
            hold=0.3, update=S.together(cutting, S.staged((0.0, 0.3, reach(op, "r", start_btn, clear_front,
                                                                           grip=(0.2, 0.3))),
                                                          (0.3, 0.7, reach(op, "r", clear_front, None, grip=(0.3, 0.3),
                                                                           lean=0.0)))),
            cam_to=S.look(vise, 320.0, 62.0, 18.0),
            labels=[("5 in diamond blade, 0.36 mm", label_pt(saw, (sp["blade_centre"][0] + 2.0, sp["blade_centre"][1] -
                                                                   40.0, sp["blade_centre"][2] + 20.0)), (0.80, 0.70)),
                    ("piece", tuple(vise), (0.22, 0.24))])
    slice_names = saw.names.get("slice", [])
    J = saw.inst.joints

    def fall(u):
        saw.v["wheel"] = 3.0 + 0.4 * u
        saw.v["slice"] = 1.0 - u
        saw.apply()
        # the sliver drops off the +x side into the tank (it rides on the arm until it's free)
        sc.gmat[saw.group("slice")] = T((4.0 * u, 0.0, -40.0 * u * u)) @ J["slice"].matrix(1.0)
    sc.step("Preparation 2 · saw", "The 2 mm sliver falls into the tank; auto shut-off | grinding takes the last "
            "0.5 mm", 3.0, hold=1.0, update=fall)
    # both cut pieces, section faces down, side by side on the bench beside the saw (the second was cut the same way);
    # the operator carries them, as one 22 x 22 mm pair, to the press
    pair_at = T((150.0, -300.0, BENCH_H))
    pair = []
    for h, dx in ((0, -6.0), (1, 6.0)):
        pair += add_set(sc, piece_meshes(d, "A", h, T((dx, 0.0, 3.0)) @ R((0, 1, 0), 90.0)), f"pair{h}", "pair",
                        shown=False)
    sc.gmat["pair"] = pair_at
    sc.step("Preparation 2 · saw", "The second piece the same way | both on the bench, section faces down", 2.5,
            hold=0.8, update=S.together(saw.move({"arm": (1.0, -0.6), "cover": (0.0, 1.0), "specimen": (1.0, 0.0)}),
                                        fade(sc, pieces[1], 1.0, 0.0), S.staged((0.5, 1.0, fade(sc, pair, 0.0, 1.0)))),
            cam_to=S.look((60.0, -250.0, BENCH_H + 80.0), 900.0, 50.0, 30.0),
            labels=[("both pieces: 18 tracks, one mount", (150.0, -300.0, BENCH_H + 12.0), (0.78, 0.30))])
    # -------------------------------------------------------------------------- the hot mount
    pr = press
    grab = np.array([150.0, -300.0, BENCH_H + 12.0 + 58.0])
    sc.step("Preparation 2 · mount", "Pick up the pair", 2.0, hold=0.2,
            update=S.together(saw.move({"cover": (1.0, 0.0)}),
                              reach(op, "r", None, grab, grip=(0.3, 0.6), look=tuple(grab), lean=16.0)))
    op.hold("r", "pair")
    xp = 620.0 - 25.0 - 150.0
    carry2 = (230.0, 330.0, 1080.0)
    sc.step("Preparation 2 · mount", "Hot-mount both pieces in one mould | LECO MX400, 1.5 in (38 mm)", 4.0,
            hold=0.4, update=S.together(S.staged((0.0, 0.2, reach(op, "r", grab, grab + np.array([0.0, 0.0, 120.0]),
                                                                  grip=(0.6, 0.6), lean=6.0)),
                                                 (0.2, 1.0, walk(op, -40.0, -650.0, xp, -650.0, carry=carry2))),
                                        pr.move({"closure": (0.0, 1.0)})),
            cam_to=S.look(label_pt(pr, (0.0, -40.0, 420.0)), 1900.0, 62.0, 22.0))
    op.set(hd=0.0, amp=0.0)
    pr.set(ram=1.0)
    ram_tgt = sc.world(pr.group("ram")) @ T((-25.0, -40.0, 405.0))
    pr.set(ram=0.0)
    hand_c = op.hand_point("r")
    hover = np.array(ram_tgt[:3, 3]) + np.array([0.0, -20.0, 58.0 + 110.0])
    down = np.array(ram_tgt[:3, 3]) + np.array([0.0, 0.0, 58.0])
    seat2 = {}

    def seat_pair(u):
        if "m" not in seat2:
            op.let_go("r")
            seat2["m"] = sc.world("pair").copy()
        sc.gmat["pair"] = S.blend(seat2["m"], ram_tgt, u)
        if u >= 0.999:
            sc.parent["pair"] = pr.group("ram")
            sc.gmat["pair"] = np.linalg.inv(sc.world(pr.group("ram"))) @ ram_tgt
    sc.step("Preparation 2 · mount", "Ram up; both pieces on it, section face down", 3.5, hold=0.4,
            update=S.together(S.staged((0.0, 0.55, pr.move({"ram": (0.0, 1.0)}))),
                              S.staged((0.0, 0.45, reach(op, "r", hand_c, hover, grip=(0.6, 0.6), look=tuple(down),
                                                         lean=16.0)),
                                       (0.45, 0.7, reach(op, "r", hover, down, grip=(0.6, 0.6))),
                                       (0.7, 0.8, seat_pair),
                                       (0.8, 0.9, reach(op, "r", down, hover, grip=(0.6, 0.3))),
                                       (0.9, 1.0, reach(op, "r", hover, None, grip=(0.3, 0.3), lean=0.0)))),
            cam_to=S.look(label_pt(pr, (-25.0, -40.0, 470.0)), 800.0, 62.0, 34.0))
    sc.step("Preparation 2 · mount", "Ram down; conductive (carbon-filled) phenolic in | so the SEM won't charge",
            4.0, hold=0.6, update=S.staged((0.0, 0.4, pr.move({"ram": (1.0, 0.0)})),
                                           (0.4, 0.7, pr.move({"doser": (1.0, 0.0), "pour": (0.0, 1.0),
                                                               "charge": (0.0, 1.0)})),
                                           (0.7, 1.0, pr.move({"doser": (0.0, 1.0), "pour": (1.0, 0.0)}))))
    sc.step("Preparation 2 · mount", "Stopper, closure; heat under pressure | 150-180 C, cool under pressure",
            5.0, hold=0.8, update=S.staged((0.0, 0.15, pr.move({"stopper": (0.0, 1.0)})),
                                           (0.15, 0.3, pr.move({"closure": (1.0, 0.0)})),
                                           (0.3, 0.8, pr.move({"glow": (0.0, 1.0), "ram": (0.0, 0.47),
                                                               "charge": (1.0, 0.0), "mount": (0.0, 1.0)})),
                                           (0.8, 1.0, pr.move({"glow": (1.0, 0.0)}))),
            labels=[("~6 min heat, 3 min cool (25 mm mould)", label_pt(pr, (100.0, -230.0, 300.0)), (0.80, 0.30))])
    sc.step("Preparation 2 · mount", "Out comes the mount: 18 tracks in its face | label it: plate, row, side",
            3.5, hold=1.5, update=S.together(S.staged((0.0, 0.35, pr.move({"closure": (0.0, 1.0)})),
                                                      (0.35, 0.6, pr.move({"stopper": (1.0, 0.0)})),
                                                      (0.6, 1.0, pr.move({"ram": (0.47, 1.0)}))),
                                             S.staged((0.0, 0.3, reach(op, "r", None, None, lean=0.0))),
                                             fade(sc, pair, 1.0, 0.0)))
    sc.save()
    au.save()


# ================================================================================= chapter 4: grind and polish
@chapter("sop02_c4")
def c4():
    sc = S.SOPScene("sop02_c4", TITLE)
    S.room(sc, x0=-1100.0, x1=1100.0)
    pol = S.place(sc, "polisher", 0.0, 0.0)
    # our mounts are conductive (black), not the lab's maroon Bakelite
    for n in pol.names.get("holder", []):
        if "mount_red" in n:
            sc.color[n] = S.MATS["mount"][:3]
    # the head's column telescopes into its housing, and the platen's hub turns in the bowl (byu-vcl's model)
    au = audit_for(sc, allow=[("polisher:holder*", "polisher:paper*"), ("polisher:holder*", "polisher:cloth*"),
                              ("polisher:holder*", "polisher:alumina*"), ("polisher:glow*", "*"),
                              ("polisher:powder*", "*"), ("polisher:head*", "polisher:body/inst_grey*"),
                              ("polisher:platen*", "polisher:body/inst_grey*")])
    hold_pt = label_pt(pol, (-82.0, -94.5, 300.0))
    sc.card("Preparation 3 · Grind and polish", ["SiC 320, 800, 1200; 3 and 1 um diamond; 0.05 um colloidal silica "
                                                  "for Al."], seconds=2.5, label="Preparation 3")
    cam_hold(sc, S.look((0.0, 0.0, BENCH_H + 300.0), 3400.0, -28.0, 14.0))
    sc.step("Preparation 3", "Grind and polish on the LECO PX500 | six mounts in the holder", 3.5, hold=1.0,
            cam_to=S.look((-50.0, -60.0, BENCH_H + 330.0), 1700.0, -32.0, 18.0),
            labels=[("12 in platen", label_pt(pol, (-53.0 + 140.0, -129.5, 279.0)), (0.80, 0.70)),
                    ("6-position holder", hold_pt, (0.18, 0.40))])
    steps = [("SiC 320, water", "platen 300 rpm, head 150 rpm, 25 N per mount, to the plane", "paper", 3.0),
             ("SiC 800, water", "150 rpm, 25 N, 0.5-1 min", "paper", 2.6),
             ("SiC 1200, water", "150 rpm, 25 N, 0.5-1 min", "paper", 2.6),
             ("3 um diamond, napless cloth", "150 rpm, 25 N, 3-4 min", "cloth", 3.0),
             ("1 um diamond, napped cloth", "150 rpm, 20 N, 3-4 min", "cloth", 3.0),
             ("Al: 0.05 um colloidal silica", "contra-rotation, 15 N, 1-2 min", "cloth", 3.4)]
    k = 0.0
    for i, (what, how, ab, secs) in enumerate(steps):
        lay = pol.move({ab: (0.0, 1.0), ("paper" if ab == "cloth" else "cloth"): (None, 0.0)})
        sc.step("Preparation 3", f"{what} | {how}", 1.6, hold=0.2, update=lay,
                cam_to=S.look((-60.0, -120.0, BENCH_H + 300.0), 1000.0, -48.0, 16.0)
                if i == 0 else None)
        wet = "glow" if ab == "paper" else "powder"
        film = {"alumina": (0.0, 1.0)} if ab == "cloth" else {}
        sc.step("Preparation 3", f"{what} | {how}", secs, hold=0.3,
                update=pol.move({"head": (0.0, 1.0), "platen": (k, k + 1.0), "holder": (k, k + 1.0),
                                 wet: (0.0, 1.0), **film}),
                cam_to=S.look((-70.0, -120.0, BENCH_H + 300.0), 760.0, -52.0, 12.0) if i == 0 else None)
        k += 1.0
        sc.step("Preparation 3", f"Head up, rinse the mounts | {'next grit' if i < 5 else 'done: rinse, ethanol, dry'}",
                1.4, hold=0.2, update=pol.move({"head": (1.0, 0.0), wet: (1.0, 0.0),
                                                **({"alumina": (1.0, 0.0)} if ab == "cloth" else {})}))
    sc.step("Preparation 3", "Mirror finish; etch straight away | Al oxidises and the etch dulls if it waits",
            3.0, hold=1.2, update=pol.move({"cloth": (1.0, 0.0)}),
            cam_to=S.look((-50.0, -60.0, BENCH_H + 330.0), 1200.0, -30.0, 22.0))
    sc.save()
    au.save()


# ================================================================================= chapter 5: etch
@chapter("sop02_c5")
def c5():
    import people
    import models_track as MT
    sc = S.SOPScene("sop02_c5", TITLE)
    S.room(sc, x0=700.0, x1=1900.0, wall=True)
    hood = S.place(sc, "fumehood", 0.0, 0.0, z=0.0)
    z0 = 932.0
    # the hood's own beakers and bottle make way for ours (PTFE and PP, no glass with HF)
    drop_pieces(hood, ("load",), match=("body/r7_pc", "body/r7_keller", "body/water", "body/inst_white",
                                        "body/inst_red"))
    props = MT.etch_props()
    place = {"keller": (-430.0, -110.0), "ptfe_dish": (-170.0, -270.0), "rinse_dish": (20.0, -270.0),
             "wash_water": (190.0, -210.0), "wash_ethanol": (290.0, -120.0), "aps": (390.0, -230.0)}
    pn = {}
    for k, (x, y) in place.items():
        pn[k] = S.add_entries(sc, S.props(k, props[k]), f"prop/{k}", f"prop_{k}", at=T((x, y, z0)))
    # the dryer and the calcium gluconate gel on the side bench, right of the hood: at hand, outside the acid
    pn["hot_air_dryer"] = S.add_entries(sc, S.props("hot_air_dryer", props["hot_air_dryer"]), "prop/hot_air_dryer",
                                        "prop_dryer", at=T((1000.0, -80.0, BENCH_H)) @ R((0, 0, 1), 180.0))
    gel_at = (790.0, -250.0, BENCH_H)
    pn["ca_gluconate"] = S.add_entries(sc, S.props("ca_gluconate", props["ca_gluconate"]), "prop/ca_gluconate",
                                       "prop_gel", at=T(gel_at))
    # plastic tongs (the mount is 38 mm across) and the mount, polished face down
    from common import Model, box
    tg = Model("tongs", "PP tongs, 200 mm")
    for s_ in (-1, 1):
        tg.add(f"leg{s_}", box(0, -2.0 + s_ * 3.0, -3, 140, 2.0 + s_ * 3.0, 3).union(
            box(140, -2.0 + s_ * 21.0, -3, 200, 2.0 + s_ * 21.0, 3)).union(
            box(135, min(s_ * 3.0, s_ * 21.0) - 2.0, -3, 145, max(s_ * 3.0, s_ * 21.0) + 2.0, 3)), "tweezer_pp")
    tg.add("hinge", box(-8, -7, -4, 8, 7, 4), "tweezer_pp")
    S.add_entries(sc, S.props("tongs", tg), "prop/tongs", "tongs")
    add_set(sc, mount_meshes(face_up=False), "mount", "mountg")
    # the operator: HF-rated (neoprene) gloves over nitrile, a face shield over the safety glasses
    op = person(sc, "op", x=-120.0, y=-790.0, hd=0.0)
    for n in op.names():
        if n.endswith("/glove"):
            sc.color[n] = S.MATS["neoprene"][:3]
    S.add_entries(sc, S.props("face_shield", props["face_shield"]), "prop/face_shield", "shield")
    hp = op.H("head")

    def shield_on(sc_):
        Mh = sc_.gmat[op.group] @ op.S[op.bi["head"]]
        sc_.gmat["shield"] = Mh @ T((hp[0], hp[1] + 18.0, hp[2] - 95.0))
    sc.frame_hooks.append(shield_on)
    shield_on(sc)
    au = audit_for(sc, allow=[("prop/*", "fumehood:body/r7_epoxy*"), ("mount/*", "prop/*dish/keller*"),
                              ("mount/*", "prop/*dish/water*"), ("prop/tongs*", "mount/*"),
                              ("prop/tongs*", "op/*glove*"), ("prop/face_shield*", "op/*")])
    hood.set(sash=1.0)
    dish = np.array([place["ptfe_dish"][0], place["ptfe_dish"][1], z0])
    rinse = np.array([place["rinse_dish"][0], place["rinse_dish"][1], z0])
    # the mount, face down in the tongs; the tongs in the right hand (200 mm long, tipped 25 deg down). The tongs
    # follow a planned path and the hand holds their handle, so the mount goes exactly where it is drawn
    tip_rel = np.array([0.0, 181.3, -84.5])
    tongs_R = R((0, 0, 1), 90.0) @ R((0, 1, 0), 25.0)
    sc.gmat["mountg"] = T((200.0, 0.0, 0.0)) @ R((0, 1, 0), -25.0) @ T((0.0, 0.0, -10.0))
    sc.parent["mountg"] = "tongs"
    grip_off = np.array([0.0, 30.0, 14.0])             # the palm on the legs, 30 mm past the hinge

    def tongs_at(tip):
        tip = np.asarray(tip, float)
        hinge = tip - tip_rel
        sc.gmat["tongs"] = T(hinge) @ tongs_R
        return hinge + grip_off

    def move_tip(a, b, look):
        a, b = np.asarray(a, float), np.asarray(b, float)

        def up(u):
            hand = tongs_at(a + (b - a) * u)
            op.set(hands={"r": tuple(hand)}, grip={"r": 0.8}, look=tuple(look))
        return up
    tip0 = dish + np.array([0.0, -70.0, 130.0])
    op.set(hands={"r": tuple(tongs_at(tip0))}, grip={"r": 0.8}, lean=4.0, look=tuple(dish + np.array([0, 0, 30.0])))
    sc.card("Preparation 4 · Etch", ["Al: Keller's reagent, 10-20 s. It contains HF.",
                                      "Cu alloys: ammonium persulfate or ferric chloride."], seconds=2.5,
            label="Preparation 4")
    cam_hold(sc, S.look((300.0, -200.0, 1350.0), 4800.0, 30.0, 12.0))
    sc.step("Preparation 4", "Etch right after polishing, in the fume hood | Labconco XStream, sash at its 18 in "
            "stop", 4.0, hold=1.0, cam_to=S.look((150.0, -250.0, 1300.0), 3200.0, 36.0, 14.0))
    sc.step("Preparation 4 · HF", "Keller's reagent contains HF | 2 mL HF, 3 HCl, 5 HNO3, 190 water",
            3.5, hold=1.2, cam_to=S.look((-150.0, -220.0, z0 + 60.0), 900.0, 35.0, 34.0),
            labels=[("Keller's reagent (HF)", (place["keller"][0], place["keller"][1], z0 + 150.0), (0.20, 0.22)),
                    ("PTFE dish: no glass with HF", (dish[0], dish[1], z0 + 25.0), (0.22, 0.72)),
                    ("water rinse (PP dish)", (rinse[0], rinse[1], z0 + 25.0), (0.78, 0.72))])
    sc.step("Preparation 4 · HF", "HF-rated gloves over nitrile, face shield | calcium gluconate gel at hand",
            3.5, hold=1.5, cam_to=S.look((200.0, -620.0, 1250.0), 1700.0, 62.0, 14.0),
            labels=[("face shield", (-120.0, -680.0, 1640.0), (0.30, 0.18)),
                    ("neoprene gloves over nitrile", tuple(op.hand_point("r")), (0.22, 0.62)),
                    ("2.5 % calcium gluconate gel", (gel_at[0], gel_at[1], gel_at[2] + 28.0), (0.84, 0.70))])
    above = dish + np.array([0.0, 0.0, 85.0])
    inside = dish + np.array([0.0, 0.0, 21.0])
    close = S.look(dish + np.array([20.0, 0.0, 50.0]), 480.0, 48.0, 12.0)
    sc.step("Preparation 4 · Al", "Polished face down into Keller's | plastic tongs", 3.0, hold=0.2,
            update=move_tip(tip0, above, dish), cam_to=close)
    sc.step("Preparation 4 · Al", "10-20 s, then straight out | 15 s here", 4.0, hold=0.3,
            update=S.staged((0.0, 0.2, move_tip(above, inside, dish)), (0.8, 1.0, move_tip(inside, above, dish))),
            labels=[("Keller's, 10-20 s", tuple(dish + np.array([0, 0, 12.0])), (0.20, 0.30))])
    above_r = rinse + np.array([0.0, 0.0, 85.0])
    in_r = rinse + np.array([0.0, 0.0, 25.0])
    sc.step("Preparation 4 · rinse", "Rinse in water at once | then a stream from the wash bottle", 4.0, hold=0.3,
            update=S.staged((0.0, 0.45, move_tip(above, above_r, rinse)), (0.45, 0.65, move_tip(above_r, in_r, rinse)),
                            (0.8, 1.0, move_tip(in_r, above_r, rinse))),
            cam_to=S.look(rinse + np.array([0.0, 0.0, 50.0]), 520.0, 48.0, 12.0))
    sc.step("Preparation 4 · rinse", "Ethanol, then the hot-air dryer | on the side bench", 3.0,
            hold=1.0, cam_to=S.look((450.0, -250.0, z0 + 80.0), 1700.0, 40.0, 18.0),
            labels=[("ethanol", (place["wash_ethanol"][0], place["wash_ethanol"][1], z0 + 160.0), (0.56, 0.20)),
                    ("hot-air dryer", (1000.0, -80.0, BENCH_H + 160.0), (0.86, 0.35))])
    sc.step("Preparation 4 · Cu", "Cu alloys: ammonium persulfate or ferric chloride | instead of Keller's", 3.5,
            hold=1.5, cam_to=S.look((place["aps"][0], place["aps"][1], z0 + 60.0), 750.0, -20.0, 28.0),
            labels=[("ammonium persulfate: 10 g in 90 mL water", (place["aps"][0], place["aps"][1], z0 + 120.0),
                     (0.30, 0.22))])
    sc.save()
    au.save()


# ================================================================================= chapter 6: image and measure
@chapter("sop02_c6")
def c6():
    d = data()
    sc = S.SOPScene("sop02_c6", TITLE)
    S.room(sc, x0=-1300.0, x1=1300.0)
    vhx = S.place(sc, "vhx", -450.0, 0.0)
    sem = S.place(sc, "sem", 520.0, 20.0)
    vhx_clear(vhx)
    drop_pieces(sem, ("readout",))
    sem.set(stub=1.0)                                    # a mount of the same row, already in the SEM's cup
    zs = 232.0
    mnt = add_set(sc, mount_meshes(face_up=True), "mount", "mountg", at=T((0.0, -40.0, zs)),
                  parent=vhx.group("turntable"))
    vhx.set(table=0.0)
    au = audit_for(sc, allow=[("mount/*", "vhx:turntable*"), ("mount/*", "vhx:table*"),
                              ("sem:stub*", "sem:drawer*"), ("sem:drawer*", "sem:body*"), ("vhx:table*", "vhx:turntable*"), ("vhx:body*", "vhx:table*")])
    stage_w = (-450.0, -40.0, BENCH_H + zs + 20.0)
    sc.card("Preparation 5 · Image and measure", ["Every track at one fixed magnification; width, depth, height and "
                                                   "fused area in Fiji."], seconds=2.5, label="Preparation 5")
    cam_hold(sc, S.look((0.0, 0.0, BENCH_H + 250.0), 3000.0, -20.0, 15.0))
    sc.step("Preparation 5", "Image each track at one fixed magnification | optical, 200x", 4.0, hold=1.0,
            cam_to=S.look(stage_w, 900.0, -40.0, 22.0),
            labels=[("etched mount, face up", stage_w, (0.22, 0.70))])
    sc.panel("sec", _cached(panel_section, d), rect=(0.68, 0.09, 0.30), alpha=0.0)
    sc.step("Preparation 5 · measure", "Fiji: W at the original surface | D below it, H above it, fused area",
            5.0, hold=2.0, update=sc.fade_panel("sec", 0.0, 1.0), cam_to=S.look(stage_w, 330.0, -55.0, 30.0))
    sc.step("Preparation 5 · measure", "Set the scale once; trace each pool | three spots in the steady part",
            3.5, hold=1.5)
    sc.step("Preparation 5 · SEM", "Or SEM-BSE at a fixed magnification | Hitachi TM4000PlusII", 4.0, hold=0.5,
            update=S.together(sc.fade_panel("sec", 1.0, 0.0), sem.move({"drawer": (0.0, 1.0)})),
            cam_to=S.look((520.0, -150.0, BENCH_H + 200.0), 1100.0, 30.0, 22.0))
    sc.step("Preparation 5 · SEM", "The conductive mount doesn't charge | door in, evacuate, image", 3.5, hold=1.0,
            update=sem.move({"drawer": (1.0, 0.0)}))
    sc.panel("plane2", _cached(panel_planes, d), rect=(0.68, 0.09, 0.30), alpha=0.0)
    sc.step("Preparation 5 · second plane", "On one plate: grind 1.5 mm further, image again | the along-track "
            "scatter", 4.5, hold=2.0, update=sc.fade_panel("plane2", 0.0, 1.0),
            cam_to=S.look(stage_w, 700.0, -30.0, 24.0))
    sc.panel("time", _cached(panel_table, "Time per run (the M2 plan's estimates)",
                             [("Tracks per mount", "about 18 (one row)"),
                              ("Preparation, per batch of mounts", "3-4 h"),
                              ("Measuring 72 tracks by hand", "about 2 h"),
                              ("Our own times", "log them; they replace these")],
                             "estimate", "DAL PR #243, run sheet", 5.2, 2.6, 0.50),
             rect=(0.68, 0.09, 0.30), alpha=0.0)
    sc.step("Preparation 5 · time", "About 18 tracks per mount, 3-4 h per batch | ~2 h to measure 72 tracks",
            4.0, hold=2.0, update=S.together(sc.fade_panel("plane2", 1.0, 0.0), sc.fade_panel("time", 0.0, 1.0)),
            cam_to=S.look((0.0, 0.0, BENCH_H + 250.0), 2200.0, -20.0, 16.0))
    sc.save()
    au.save()


def panel_planes(d, u=1.0):
    """Plane 1 against plane 2 (1.5 mm further along the tracks): width and depth, one point per track."""
    fig, plt = _fig(5.2, 3.6)
    ax = fig.add_axes([0.14, 0.15, 0.54, 0.64])
    rng = np.random.default_rng(15)
    ts = [t for t in d["tracks"] if t["block"] == "A"]
    w1 = np.array([t["width_um"] for t in ts])
    d1 = np.array([t["depth_um"] for t in ts])
    w2 = w1 * (1 + 0.035 * rng.standard_normal(len(ts)))
    d2 = d1 * (1 + 0.07 * rng.standard_normal(len(ts)))
    lim = [0, max(w1.max(), d1.max()) * 1.08]
    ax.plot(lim, lim, color=INK2, lw=0.8)
    ax.scatter(w1, w2, s=20, c=C1, edgecolors="white", linewidths=0.6, label="width", zorder=3)
    ax.scatter(d1, d2, s=20, c=C2, marker="s", edgecolors="white", linewidths=0.6, label="depth", zorder=3)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("plane 1, mid-length (um)")
    ax.set_ylabel("plane 2, +1.5 mm (um)")
    _axes(ax)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=7.5, frameon=False)
    sw = 100 * np.std((w2 - w1) / w1)
    sd = 100 * np.std((d2 - d1) / d1)
    fig.text(0.73, 0.45, f"scatter\nwidth {sw:.1f} %\ndepth {sd:.1f} %", fontsize=9, color=INK, va="top")
    fig.text(0.02, 0.95, "Along-track scatter: two planes 1.5 mm apart", fontsize=10.5, weight="bold", color=INK)
    _badge(fig, "synthetic example", "the model comparison takes this as its noise level")
    return S.fig_image(fig)


# ================================================================================= chapter 7: analysis
@chapter("sop02_c7")
def c7():
    d = data()
    sc = S.SOPScene("sop02_c7", TITLE)
    S.room(sc, x0=-1100.0, x1=1100.0)
    vhx = S.place(sc, "vhx", -150.0, 0.0)
    vhx_clear(vhx)
    add_set(sc, mount_meshes(face_up=True), "mount", "mountg", at=T((0.0, -40.0, 232.0)),
            parent=vhx.group("turntable"))
    au = audit_for(sc, allow=[("mount/*", "vhx:turntable*"), ("vhx:table*", "vhx:turntable*"),
                              ("vhx:body*", "vhx:table*")])
    m = d["material"]
    rect = (0.64, 0.09, 0.34)
    sc.card("Analysis and acceptance", ["melt_pool_calibration.py: absorptivity from conduction tracks, Ke for "
                                         "every track, the AM Module's bias."], seconds=2.5, label="Analysis")
    cam_hold(sc, S.look((-150.0, 0.0, BENCH_H + 280.0), 1900.0, -24.0, 14.0))
    sc.panel("inputs", _cached(panel_table, "Inputs, from our own measurements",
                               [("T_liquidus", "SOP 01 (DSC)"), ("k, thermal conductivity",
                                                                 "SOP 04: eddy current + Smith-Palmer,\nor laser flash"),
                                ("rho, density", "SOP 03"), ("cp", "DSC"),
                                ("r0, beam 1/e2 radius", "the machine's beam profile")],
                               "", "melt_pool_calibration.py tracks.csv --material alloy.json --fit-on conduction",
                               5.2, 3.0, 0.42), rect=rect, alpha=0.0)
    sc.step("Analysis", "Inputs: T_liquidus, k, rho, cp and the beam radius | each from our own measurements",
            4.0, hold=2.0, update=sc.fade_panel("inputs", 0.0, 1.0),
            cam_to=S.look((-250.0, 0.0, BENCH_H + 280.0), 1500.0, -30.0, 14.0))
    seq = [("fit", panel_fit, "Analysis · fit", f"Fit on conduction tracks only (D/W < 0.5) | eta = {d['eta_fit']:.2f}: "
                                                 "the model has no keyhole"),
           ("etaw", panel_eta_w, "Analysis · per track", "Width-only absorptivity for each track | rises with P/v"),
           ("ke", panel_ke, "Analysis · keyhole", f"Ke for each track; one threshold for keyhole onset | "
                                                  f"Ke* = {d['ke_threshold']:.1f} (#249)"),
           ("am", panel_am, "Analysis · AM Module", "The AM Module's bias and RMSE | against the measured tracks"),
           ("acc", panel_acceptance, "Acceptance", "Acceptance: 3+ conduction and 3+ keyhole tracks | controls "
                                                   "within 5 %; eta within 0.03 leaving one out")]
    prev = "inputs"
    for i, (key, fn, label, cap) in enumerate(seq):
        sc.panel(key, _cached(fn, d), rect=rect, alpha=0.0)
        sc.step(label, cap, 4.5, hold=2.5, update=S.together(sc.fade_panel(prev, 1.0, 0.0),
                                                              sc.fade_panel(key, 0.0, 1.0)),
                cam_to=S.look((-250.0, 0.0, BENCH_H + 280.0), 1500.0 - 40.0 * i, -30.0 + 5.0 * i, 14.0 + 1.0 * i))
        prev = key
    sc.step("Acceptance", "Bare-plate tracks get the same checks | per alloy and substrate condition", 3.0, hold=1.5,
            update=sc.fade_panel(prev, 1.0, 0.0), cam_to=S.look((-150.0, 0.0, BENCH_H + 280.0), 1900.0, -24.0, 14.0))
    sc.card("Open questions",
            ["Is the desktop LPBF (#260) running, or do the first tracks come from Utah's Aconity MIDI "
             "(P1, Dec 2-3)?",
             "Ask Thermo-Calc's account manager for the AM Module grid export as CSV; #238 and #249 asked for "
             "it first."], seconds=6.0, label="Open questions",
            note="Equipment: LECO VC50, MX400, PX500; Keyence VHX-7000; Hitachi TM4000PlusII; Labconco XStream. "
                 "Every data panel is a synthetic example from melt_pool_calibration.py.")
    sc.save()
    au.save()



# ================================================================================= notes/sop02.md
SOP_MAP = [
    ("Checks: width, depth, D/W, regime, balling; calibrates the AM Module heat source (#238, #249)",
     ["SOP 02 · Single tracks and the heat-source fit"]),
    ("Plate layout, cutting and mounting follow the M2 plan of PR #243", ["SOP 02 · Single tracks and the heat-source fit",
                                                                         "A 10 mm strip"]),
    ("Samples: which machine (desktop #260, Utah MIDI P1, BYU M2 #243)", ["Utah's Aconity MIDI"]),
    ("Samples: tracks 12 mm long at 2 mm spacing", ["18 tracks, 12 mm long"]),
    ("Samples: all scanned in one direction across or into the gas flow", ["Each track scanned across the gas flow",
                                                                           "18 tracks, 12 mm long"]),
    ("Samples: exposed from the outlet side toward the inlet", ["18 tracks, 12 mm long", "Block A: random positions"]),
    ("Samples: scrambled-Sobol power-speed blocks, not a grid", ["Scrambled-Sobol power-speed blocks"]),
    ("Samples: repeated control sets on every plate", ["Scrambled-Sobol power-speed blocks", "Block A: random positions"]),
    ("Samples: substrate 6061/6063 for Al, a Cu alloy for Cu, or a printed pad", ["Substrate: a 6061 plate"]),
    ("Samples: bare-plate tracks calibrate the absorptivity of dense metal", ["Bare-plate tracks first"]),
    ("Samples: one-powder-layer tracks (30-50 um) reproduce LPBF", ["Then one powder layer", "Per alloy: bare-plate"]),
    ("Samples: a few grams of powder for one layer; fits the 100-300 g atomized", ["About 1.2 g covers"]),
    ("Preparation 1: top views of every track at 50-100x: continuity, balling, denudation width",
     ["Image first", "Each track at 50-100x", "Denuded band", "Bare-plate tracks: continuity"]),
    ("Preparation 2: section at mid-length", ["Section every track at mid-length", "The fine cut",
                                              "Micrometer: cut 0.5 mm", "~300 rpm"]),
    ("Preparation 2: hot-mount in conductive compound (#243 section 3)", ["Hot-mount both pieces",
                                                                          "Ram down; conductive"]),
    ("Preparation 3: SiC 320 -> 800 -> 1200", ["SiC 320, water", "SiC 800, water", "SiC 1200, water"]),
    ("Preparation 3: then 3 um and 1 um diamond", ["3 um diamond", "1 um diamond"]),
    ("Preparation 3: for Al, 0.05 um colloidal silica", ["Al: 0.05 um colloidal silica"]),
    ("Preparation 4: Al: Keller's reagent, 10-20 s", ["Keller's reagent contains HF", "10-20 s, then straight out"]),
    ("Preparation 4: HF: fume hood, HF-rated gloves, calcium gluconate gel at hand",
     ["Etch right after polishing, in the fume hood", "HF-rated gloves over nitrile"]),
    ("Preparation 4: Cu alloys: ammonium persulfate or ferric chloride", ["Cu alloys: ammonium persulfate"]),
    ("Preparation 4: etch right after polishing", ["Mirror finish; etch straight away", "Etch right after polishing"]),
    ("Preparation 5: image each track at a fixed magnification (optical 200x or SEM-BSE)",
     ["Image each track at one fixed magnification", "Or SEM-BSE"]),
    ("Preparation 5: measure in Fiji W, D, H, fused area", ["Fiji: W at the original surface", "Set the scale once"]),
    ("Preparation 5: on one plate grind 1.5 mm further and section again (along-track scatter)",
     ["On one plate: grind 1.5 mm further"]),
    ("Time: ~18 tracks per mount, 3-4 h per batch, ~2 h to measure 72 tracks", ["About 18 tracks per mount"]),
    ("Analysis: inputs T_liquidus (SOP 01), k (SOP 04 / LFA), rho (SOP 03), cp (DSC), r0 (beam profile)",
     ["Inputs: T_liquidus"]),
    ("Analysis: fit on conduction-mode tracks only (D/W < 0.5); the fitted absorptivity",
     ["Fit on conduction tracks only"]),
    ("Analysis: width-only absorptivity per track, rising with P/v", ["Width-only absorptivity"]),
    ("Analysis: Ke per track", ["Ke for each track"]),
    ("Analysis: the AM Module's bias and RMSE", ["The AM Module's bias and RMSE"]),
    ("Analysis: a single Ke threshold for keyhole onset (#249)", ["Ke for each track"]),
    ("Acceptance: >= 3 conduction and >= 3 keyhole tracks per alloy and substrate condition",
     ["Acceptance: 3+ conduction", "Bare-plate tracks get the same checks"]),
    ("Acceptance: controls repeat within +-5 % in width", ["Acceptance: 3+ conduction"]),
    ("Acceptance: absorptivity stable within +-0.03 leaving any one track out", ["Acceptance: 3+ conduction"]),
    ("Open questions: desktop machine (#260) or Utah MIDI (P1, Dec 2-3)?; AM Module grid export as CSV",
     ["Open questions"]),
]


def write_notes() -> Path:
    meta = json.loads((S.OUT / "sop02.json").read_text())
    fps = meta["fps"]
    subs = meta["substeps"]

    def t(fr):
        sec = fr / fps
        return f"{int(sec // 60)}:{sec % 60:04.1f}"
    rows = []
    for line, keys in SOP_MAP:
        hits = []
        for k in keys:
            for s_ in subs:
                if s_["caption"].startswith(k) or (s_.get("card") and k in s_["caption"]):
                    hits.append(f"{t(s_['start_frame'])}-{t(s_['end_frame'])} ({s_['chapter'][-2:]}, "
                                f"\"{s_['caption'][:48]}\")")
                    break
        rows.append(f"| {line} | {'; '.join(hits) if hits else '**not found**'} |")
    out = HERE / "notes" / "sop02.md"
    body = NOTES_HEAD + "\n".join(rows) + "\n" + NOTES_TAIL.format(
        dur=f"{meta['n_frames'] / fps:.0f}", n=len(subs), chapters=", ".join(meta["chapters"]))
    out.write_text(body)
    return out


NOTES_HEAD = """# SOP 02 in 3-D: what each line of the SOP maps to

The video: `out/mp4/sop02.mp4` (chapters `sop02_c1` ... `sop02_c7`), its sub-steps on the joined clock in
`out/sop02.json`, a contact sheet `out/sop02_steps.jpg` and a preview `out/sop02_preview.gif`. Script:
`sop02_tracks.py`. Times below are on the joined clock (m:ss).

| SOP line | Sub-step(s) that show it |
|---|---|
"""

NOTES_TAIL = """
Length: {dur} s, {n} sub-steps, chapters {chapters}.

## Equipment and what it rests on

| Station | Model | Validation |
|---|---|---|
| Build area at the plate | `lpbf_chamber` (ours) | plate, layer and tracks at real size (DAL PR #169, #243); the chamber's inside a typical layout (notes/lpbf_chamber.md) |
| Printer, context | `lpbf_exterior`: byu-vcl's Aconity MIDI | Aconity's configurator data and photos (byu-vcl) |
| Section | `precision_saw`: LECO VC50 (ours) | registered: two views fitted (5.9, 11.5 px), two held out (30, 28 px); notes/precision_saw.md |
| Hot mount | `mount_press`: LECO MX400 (byu-vcl) | the lab's own video |
| Grind and polish | `polisher`: LECO PX500 (byu-vcl) | fitted to the lab's SOP videos |
| Etch | `fumehood`: Labconco XStream (byu-vcl); etching props (ours, `models_track.etch_props`) | catalogue sizes |
| Top views, sections | `vhx`: Keyence VHX-7000 (byu-vcl) | fitted to Keyence's video |
| SEM-BSE | `sem`: Hitachi TM4000PlusII (byu-vcl) | fitted |

## Sources for the details on screen

- The SOP (`../sops/02-single-track-melt-pool.md`) and PR #243's `lpbf-runs/m2-single-track-schedule.md` (§3 cutting
  without wire EDM, §4 the track layout, the order and direction of exposure, the second plane).
- Edison literature answer `edison/v2-metallography-density/answer.md` (and artifacts 00-02): the 40 um layer for
  AlSi10Mg single tracks (Aboulkhair et al.), ~70 um spot at focus on Aconity systems (Maddison 2022), argon cross-flow
  at 2.5-4 m/s, top views by stereo/digital microscope; hot mounting at 150-180 C with 6 min heat and 3 min cool on a
  25 mm mould, graphite-filled phenolic for SEM; the Al sequence (ASTM MNL46 method C-42: SiC to P1200 and beyond, 3 and
  1 um diamond, colloidal silica at 15 N, contra-rotation, 1-2 min; platen 300/150 rpm, 25 N per specimen); Keller's
  reagent (2 mL HF, 3 mL HCl, 5 mL HNO3, 190 mL water; 10-20 s; rinse at once), HF precautions (fume hood, HF-rated
  neoprene or nitrile gloves, face shield, 2.5 % calcium gluconate gel at the workstation); Cu etchants (FeCl3 / HCl,
  ammonium persulfate 10 g in 90 mL water); Fiji: Set Scale, line tool for W, D, H, freehand selection for the area,
  three or more spots in the steady part of each track.
- LECO VC50 brochure (form 200-952) for the saw; byu-vcl's notes for the reused models.

## Data on screen

Every plot is drawn from `out/sop02_data.json`, made by `sop02_tracks.data()`: 72 synthetic one-layer tracks (four
scrambled-Sobol blocks of 16, 100-370 W and 500-3000 mm/s, plus two controls at 300 W and 1300 mm/s per block) and 18
bare-plate tracks, their widths and depths from the repo's Eagar-Tsai field (`melt_pool_calibration.TrackField`, on a
coarser grid that agrees to 0.1 um) with an absorptivity that rises with Ke and a keyhole deepening, plus 2-5 % noise.
The fit, the width-only absorptivity, Ke and the AM Module comparison are the repo's own `fit_eta`,
`keyhole_number` and `compare_am_module`; the "AM Module" is Eagar-Tsai at eta = 0.36 standing in for its CSV export.
Every panel says "synthetic example" (the design panel: "design, illustrative window"; the time panel: "estimate").

## Left out, and why

- The bandsaw that cuts the strip out of the plate (#243 §3) is not modelled; the strip appears cut, and the caption
  says so.
- Paper and cloth changes on the polisher are fades, as in byu-vcl's PX500 clip; the operator is not drawn there.
- The second piece of each row is cut the same way as the first; the video shows the first and says so.
- The machine's own steps (job file, inerting, the laser's parameters in the software) belong to the printing SOP, not
  this one.
"""

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
        print(write_notes())
    elif arg == "notes":
        print(write_notes())
    else:
        run(arg)
