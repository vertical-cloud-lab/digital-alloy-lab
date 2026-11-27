"""Figures for the first-principles keyhole model, version 2 (PR #249). Called by
`python scripts/keyhole_first_principles_v2.py figures`, after `all` and `explore` have written their CSVs."""

from __future__ import annotations

import json
import math
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import keyhole_first_principles as fp  # noqa: E402
import keyhole_first_principles_v2 as v2  # noqa: E402

INK, INK2, GRIDC = fp.INK, fp.INK2, fp.GRIDC
BLUE, ORANGE, GREEN, GREY, PURPLE = "#2a78d6", "#eb6834", "#1baf7a", "#b9b8b2", "#8e5cc7"
CLASS_COLOURS = {"keyhole": BLUE, "lof": ORANGE, "lof_hatch": GREEN, "none": GREY}
CLASS_LABELS = fp.CLASS_LABELS
_style = fp._style


def fig_maps(out: pathlib.Path):
    d = pd.read_csv(out / "v2-map-classes.csv")
    bnd = pd.read_csv(out / "v2-keyhole-boundary-vs-am.csv")
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), layout="constrained")
    for ax, key in zip(axes, fp.ALLOYS):
        g = d[d["alloy"] == key]
        bb = bnd[bnd["alloy"] == key].sort_values("v_m_s")
        x = bb["v_m_s"] * 1000
        ax.fill_between(x, bb["P_keyhole_branch_appears_W"], bb["P_dimple_runs_away_W"], color=BLUE, alpha=0.12,
                        lw=0, label="both a dimple and a keyhole are stable")
        ax.plot(x, bb["P_surface_boils_W"], color=INK2, lw=1.2, ls=":", label="surface first boils")
        ax.plot(x, bb["P_keyhole_branch_appears_W"], color=BLUE, lw=2.0,
                label="v2: a keyhole with Wk/Dk ≤ 0.7 becomes stable")
        ax.plot(x, bb["P_dimple_runs_away_W"], color=BLUE, lw=1.4, ls="--", label="v2: the dimple runs away")
        b = pd.read_csv(fp.AM_DIR / f"{fp.ALLOYS[key]['slug']}-am-module-boundaries.csv").dropna(subset=["P_keyhole_W"])
        ax.plot(b["speed_mm_s"], b["P_keyhole_W"], color=INK, lw=2, label="AM module keyhole boundary")
        for cls, col in CLASS_COLOURS.items():
            sel = g[g["v2_class_deep_branch"] == cls]
            ax.scatter(sel["v_m_s"] * 1000, sel["P_W"], s=110, color=col, edgecolor="white", lw=0.8, zorder=3,
                       label=f"v2: {CLASS_LABELS[cls]}")
        dis = g[g["v2_class_deep_branch"] != g["am_class"]]
        ax.scatter(dis["v_m_s"] * 1000, dis["P_W"], s=26, marker="x", color=INK, lw=1.1, zorder=4,
                   label="AM module disagrees")
        ax.set_xlabel("scan speed (mm/s)", color=INK)
        ax.set_ylabel("laser power (W)", color=INK)
        ax.set_title(fp.ALLOYS[key]["label"], fontsize=10, color=INK)
        _style(ax)
    h, lab = axes[0].get_legend_handles_labels()
    fig.legend(h, lab, loc="outside lower center", ncol=3, frameon=False, fontsize=8)
    fig.savefig(out / "v2-maps-vs-am-module.png", dpi=140)
    plt.close(fig)


def fig_gan(out: pathlib.Path):
    t = pd.read_csv(out / "v2-gan2021-xray-keyhole-depths.csv")
    ex = out / "v2-explore-free-shape-gan2021.csv"
    panels = [(t, "v1_own_A_depth_um", "Version 1: straight cone"),
              (t, "own_A_depth_um", "Version 2: tilted cone, sourced optics")]
    if ex.exists():
        panels.append((pd.read_csv(ex), "own_A_depth_um", "Exploration: free shape (funnel)"))
    fig, axes = plt.subplots(1, len(panels), figsize=(4.6 * len(panels), 4.8), layout="constrained", sharey=True)
    for ax, (df, col, title) in zip(np.atleast_1d(axes), panels):
        for mat in ("Ti64", "Al6061", "SS316"):
            g = df[df["material"] == mat]
            ax.scatter(g["keyhole_depth_measured_um"], g[col], s=26, marker=fp.MAT_MARKERS[mat],
                       color=fp.MAT_COLOURS[mat], edgecolor="white", lw=0.6, label=mat, zorder=3)
        lim = [5, 2000]
        ax.plot(lim, lim, color=INK2, lw=1)
        ax.fill_between(lim, [x / 1.5 for x in lim], [x * 1.5 for x in lim], color=GRIDC, alpha=0.5, lw=0)
        ax.set_xscale("log"), ax.set_yscale("log"), ax.set_xlim(lim), ax.set_ylim(lim)
        med = {m: float((df.loc[df["material"] == m, col] / df.loc[df["material"] == m, "keyhole_depth_measured_um"]).median())
               for m in ("Ti64", "Al6061", "SS316")}
        ax.set_title(title + "\nmedian ratio " + ", ".join(f"{m} {v:.2f}×" for m, v in med.items()), fontsize=9,
                     color=INK)
        ax.set_xlabel("measured keyhole depth (µm, X-ray)", color=INK)
        _style(ax)
    np.atleast_1d(axes)[0].set_ylabel("predicted keyhole depth (µm), own absorptance", color=INK)
    np.atleast_1d(axes)[0].legend(frameon=False, fontsize=8.5, loc="upper left")
    fig.suptitle("Gan et al. 2021 X-ray keyhole depths; the grey band is within a factor 1.5", fontsize=10,
                 color=INK)
    fig.savefig(out / "v2-gan2021-xray-depths.png", dpi=130)
    plt.close(fig)


def _section(ax, al, P, v, r0, T0, A_override, title, cfd=None):
    res, sol = v2.solve_point_v2(al, P, v, r0, T0, A_override=A_override, powder=v2._powder(True))
    th = sol.get("th") if sol else fp.thermal_state(al.m, T0, res.T_onset)
    xs = np.linspace(-max(1.1 * res.pool_length_solidus_um * 1e-6, 4 * r0), 2.5 * r0, 260)
    zs = np.linspace(0, max(1.3 * res.pool_depth_solidus_um * 1e-6, 2 * r0), 140)
    X, Z = np.meshgrid(xs, zs)
    if sol:
        field = v2.keyhole_field(sol, th, v)
    else:
        def field(x, y, z):
            return fp.gaussian_field(x, y, z, res.A * P, r0, th.k, th.kappa, v)
    F = field(X.ravel(), np.zeros(X.size), Z.ravel()).reshape(X.shape)
    ax.contour(X * 1e6, Z * 1e6, F, levels=[th.theta_s], colors=[INK2], linewidths=1.0, linestyles=":")
    ax.contour(X * 1e6, Z * 1e6, F, levels=[th.theta_l], colors=[INK], linewidths=1.6)
    if sol:
        zn, xcn, rn = sol["zn"], sol["xcn"], sol["rn"]
        ax.fill_betweenx(zn * 1e6, (xcn - rn) * 1e6, (xcn + rn) * 1e6, color=BLUE, alpha=0.35, lw=0)
        ax.plot((xcn + rn) * 1e6, zn * 1e6, color=BLUE, lw=1.5)
        ax.plot((xcn - rn) * 1e6, zn * 1e6, color=BLUE, lw=1.5)
    if cfd is not None:
        ax.axhline(cfd, color=ORANGE, lw=1.2, ls="--")
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_title(f"{title}\nA {res.A:.2f}, keyhole {res.d_um:.0f} µm, front wall {res.front_wall_deg:.0f}°; "
                 f"pool {res.pool_depth_um:.0f} × {res.pool_width_um:.0f} × {res.pool_length_um:.0f} µm",
                 fontsize=8.5, color=INK)
    ax.set_xlabel("x, along the scan (µm; beam at 0, moving right)", color=INK, fontsize=8.5)
    ax.set_ylabel("depth (µm)", color=INK, fontsize=8.5)
    _style(ax)
    return res


def fig_sections(out: pathlib.Path):
    cases = [("alsi10mg", 250.0, 0.9, None, "AlSi10Mg 250 W, 0.9 m/s (AM: no defect)"),
             ("alsi10mg", 350.0, 0.9, None, "AlSi10Mg 350 W, 0.9 m/s (AM: keyhole)"),
             ("blend", 375.0, 0.4, None, "Blend 375 W, 0.4 m/s (AM: keyhole, pool 349 deep)"),
             ("blend", 375.0, 0.4, 0.3841, "Blend 375 W, 0.4 m/s, A fixed at the AM module's 0.38")]
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.6), layout="constrained")
    for ax, (key, P, v, Aov, title) in zip(axes.ravel(), cases):
        a = fp.ALLOYS[key]
        _section(ax, v2.make_alloy(key), P, v, a["r0"], a["T0"], Aov, title)
    fig.suptitle("Longitudinal sections at y = 0: keyhole (blue), liquidus (solid) and solidus (dotted)",
                 fontsize=10, color=INK)
    fig.savefig(out / "v2-keyhole-sections.png", dpi=130)
    plt.close(fig)


def fig_mg(out: pathlib.Path):
    t = pd.read_csv(out / "v2-mg-vapour.csv")
    base = t[~t["mg_in_vapour"]].set_index("alloy")["T_wall_K"]
    labels = {"alsi10mg": "AlSi10Mg (0.36 at% Mg)", "blend": "Blend (0.16 at% Mg)", "al5182": "Al 5182 (5.0 at% Mg)"}
    fig, ax = plt.subplots(figsize=(7.6, 4.2), layout="constrained")
    keys = list(labels)
    w = 0.36
    for i, (ff, col, lab) in enumerate([(1.0, BLUE, "melt passes the wall at the scan speed"),
                                        (10.0, ORANGE, "melt passes 10× faster")]):
        sel = t[t["mg_in_vapour"] & (t["melt_speed_over_scan_speed"] == ff)].set_index("alloy")
        drops = [base[k] - sel.loc[k, "T_wall_K"] for k in keys]
        xs = np.arange(len(keys)) + (i - 0.5) * w
        ax.bar(xs, drops, width=w - 0.04, color=col, label=lab)
        for x_, k, dr in zip(xs, keys, drops):
            ax.text(x_, dr + 1, f"{dr:.0f} K\nwall Mg {100 * sel.loc[k, 'mg_wall_over_bulk']:.1f} %", ha="center",
                    va="bottom", fontsize=7.5, color=INK2)
    ax.set_xticks(np.arange(len(keys)), [labels[k] for k in keys])
    ax.set_ylabel("keyhole wall cooler by (K)", color=INK)
    ax.set_title("Mg in the vapour: how much cooler the keyhole wall is (wall Mg as % of the bulk)", fontsize=9.5,
                 color=INK)
    ax.set_ylim(0, max(80, ax.get_ylim()[1] * 1.25))
    _style(ax)
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(out / "v2-mg-vapour.png", dpi=140)
    plt.close(fig)


def fig_meltflow(out: pathlib.Path):
    """Pool depth, width and length: analytic (no flow), the solver with flow off and on, and the reference."""
    t = pd.read_csv(out / "v2-meltflow-runs.csv")
    cases = [("blend-375W-0.4-own", "Blend 375 W, 0.4 m/s, own absorptance (0.87)", ("AM module", 349, 462, 1470)),
             ("blend-375W-0.4-A_am", "Blend 375 W, 0.4 m/s, A fixed at the AM module's 0.384", ("AM module", 349, 462, 1470)),
             ("al5182-473W-0.7-A_measured", "Al 5182 473 W, 0.7 m/s, A fixed at the measured 0.43",
              ("measured (NIST)", 88.8, 326, None))]
    cases = [c for c in cases if (t["case"] == c[0]).any()]
    fig, axes = plt.subplots(1, len(cases), figsize=(5.0 * len(cases), 4.6), layout="constrained")
    dims = [("depth", "pool_depth_liquidus_um", "analytic_pool_depth_um"),
            ("width", "pool_width_liquidus_um", "analytic_pool_width_um"),
            ("length", "pool_length_liquidus_um", "analytic_pool_length_um")]
    series = [("analytic, no flow", GREY), ("solver, flow off", BLUE), ("solver, Marangoni flow", ORANGE),
              (None, INK)]
    for ax, (label, title, ref) in zip(np.atleast_1d(axes), cases):
        g = t[t["case"] == label]
        off, on = g[~g["flow"].astype(bool)].iloc[0], g[g["flow"].astype(bool)].iloc[0]
        vals = [[off[a] for _, _, a in dims], [off[c] for _, c, _ in dims], [on[c] for _, c, _ in dims],
                [ref[1], ref[2], ref[3]]]
        w = 0.2
        for i, ((name, col), vv) in enumerate(zip(series, vals)):
            xs = np.arange(3) + (i - 1.5) * w
            name = name or ref[0]
            for x_, val in zip(xs, vv):
                if val is None or (isinstance(val, float) and np.isnan(val)):
                    continue
                ax.bar(x_, val, width=w - 0.03, color=col, label=name if x_ == xs[0] else None)
        ax.set_xticks(np.arange(3), [d[0] for d in dims])
        ax.set_ylabel("pool size at the liquidus (µm)", color=INK)
        ax.set_title(title, fontsize=9, color=INK)
        _style(ax)
        h, lab = ax.get_legend_handles_labels()
        seen = {}
        for hh, ll in zip(h, lab):
            seen.setdefault(ll, hh)
        ax.legend(seen.values(), seen.keys(), frameon=False, fontsize=7.5, loc="upper left")
    fig.savefig(out / "v2-meltflow-pools.png", dpi=140)
    plt.close(fig)


def main(out: pathlib.Path):
    for f in (fig_maps, fig_gan, fig_sections, fig_mg, fig_meltflow):
        try:
            f(out)
            print("wrote", f.__name__)
        except FileNotFoundError as e:
            print("skipped", f.__name__, e)
