#!/usr/bin/env python3
"""Figures for the first-six seed plan (#275), from the result files in results/.

    python bofn-seeding/first-six/make_figures.py            # writes figures/*.png (light) and *-dark.png

Colours are the first slots of a validated categorical palette (blue, orange, aqua, yellow, magenta,
green), used in a fixed order. Every series is also named in a legend or a direct label, and the numbers
behind each figure are in the CSV files next to it.
"""
from __future__ import annotations

import csv
import json
import math
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
RES = HERE / "results"
FIG = HERE / "figures"

THEMES = {
    "light": dict(surface="#ffffff", ink="#191919", ink2="#666666", grid="#e7e7e7", axis="#c2c2c2",
                  series=["#257de0", "#f47230", "#00b894", "#f2a600", "#ee7fac", "#008a17"], neutral="#9a9a9a",
                  ramp=["#cce3fd", "#9dc8f7", "#6aabf1", "#338ced", "#2370cd", "#1757ac", "#0e3d7e"]),
    "dark": dict(surface="#191919", ink="#efefef", ink2="#9c9c9c", grid="#303030", axis="#474747",
                 series=["#338ced", "#e76624", "#00a888", "#d28e05", "#e24d8b", "#0aac23"], neutral="#7a7a7a",
                 ramp=["#0e3d7e", "#1757ac", "#2370cd", "#338ced", "#6aabf1", "#9dc8f7", "#cce3fd"]),
}


def style(th):
    plt.rcParams.update({
        "figure.facecolor": th["surface"], "axes.facecolor": th["surface"], "savefig.facecolor": th["surface"],
        "text.color": th["ink"], "axes.labelcolor": th["ink2"], "xtick.color": th["ink2"], "ytick.color": th["ink2"],
        "axes.edgecolor": th["axis"], "axes.linewidth": 0.8, "grid.color": th["grid"], "grid.linewidth": 0.8,
        "axes.grid": True, "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False,
        "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "legend.frameon": False, "lines.linewidth": 2.0, "lines.solid_capstyle": "round", "lines.solid_joinstyle": "round",
        "xtick.major.size": 0, "ytick.major.size": 0, "figure.dpi": 150,
    })


def save(fig, name, mode):
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / (name + ("" if mode == "light" else "-dark") + ".png"), bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def read_csv(path):
    return list(csv.DictReader(open(path))) if path.exists() else []


def read_jsonl(path):
    return [json.loads(line) for line in open(path) if line.strip()] if path.exists() else []


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


# ------------------------------------------------------------------ A. Scheil paths, two bases
NINE = [("D1", "D1", "Al-10Si-0.35Mg"), ("D2", "D2", "Al-4.6Mg-0.66Sc-0.42Zr-0.49Mn"), ("S1", "S1", "Al-4.8Mn-0.9Cr-1.1Zr-1.2Mg"),
        ("S2", "S2", "Al-1.9Fe-1.0Mg-1.0Zr"), ("S3", "S3", "Al-3.5Si-2.5Mg"), ("X1", "X1", "Al-6Mg-2.5Si-0.7Ti"),
        ("O1", "S4", "Al-3.6Mg-1.2Zr"), ("O2", "O2-noEr", "Al-6.4Mg-0.7Mn-1.1Zr (Er left out)"), ("O3", "E1", "Al-4.8Mn-0.8Cr")]


def fig_scheil(th, mode):
    paths = {r["name"]: r for r in read_jsonl(RES / "calphad" / "scheil_paths.jsonl")}
    if not paths:
        return
    fig, axes = plt.subplots(3, 3, figsize=(10.5, 8.2), sharex=True, sharey=True)
    for ax, (sid, cid, label) in zip(axes.ravel(), NINE):
        for base, col, nm in (("pureAl", th["series"][0], "high-purity Al base"), ("6063", th["series"][1], "6063 base")):
            r = paths.get(f"{cid}|{base}")
            if not r:
                continue
            fs, T = np.array(r["fs_grid"]), np.array(r["scheil_T_at_fs"])
            ax.plot(fs, T, color=col, label=nm)
            ax.plot([fs[-1]], [T[-1]], "o", ms=6, color=col, mec=th["surface"], mew=1.5)
        ax.set_title(f"{sid}  {label}", fontsize=9)
        ax.set_ylim(430, 680)
        ax.set_xlim(0, 1.02)
    for ax in axes[-1]:
        ax.set_xlabel("fraction solid (Scheil)")
    for ax in axes[:, 0]:
        ax.set_ylabel("temperature (°C)")
    h, lab = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, lab, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 0.955))
    fig.suptitle("Where each seed finishes freezing, on two base metals", x=0.06, ha="left", fontsize=12, fontweight="bold", y=0.995)
    fig.text(0.06, 0.965, "MatCalc open Al database; the path starts where alpha-Al appears. A long tail to low temperature is the hot-tearing risk.",
             ha="left", fontsize=8.5, color=th["ink2"])
    fig.subplots_adjust(top=0.9, hspace=0.28, wspace=0.08)
    save(fig, "scheil_paths", mode)


# ------------------------------------------------------------------ B. cracking index against what experiments found
OUTCOME = {  # id -> (class, label). Classes: 0 crack-free without a grain refiner, 1 crack-free with Zr/Sc/Ti, 2 cracks
    "D1": (0, "AlSi10Mg"), "A357": (0, "AlSi7Mg0.6"), "S3": (0, "AlSi3.5Mg2.5"), "AlMg9.6Si4.9": (0, "Al-9.6Mg-4.9Si"),
    "E1": (0, "Al-4.8Mn-0.8Cr (no Zr)"), "S1b": (0, "Al-5Mn-0.8Cr-0.6Zr (columnar)"), "Fe2.5": (0, "Al-2.5Fe"),
    "Fe2.5Mn2": (0, "Al-2.5Fe-2Mn"),
    "D2": (1, "Scalmalloy"), "S1": (1, "Al-4.8Mn-0.9Cr-1.1Zr-1.2Mg"), "ChalmersD": (1, "Al-4.7Mn-0.8Cr-1.2Zr"),
    "Mair": (1, "Al-4.8Mn-0.8Ti-0.7Zr"), "CP1": (1, "Al-1Fe-1Zr"), "S2": (1, "Al-1.9Fe-1Mg-1Zr"), "S4": (1, "Al-3.6Mg-1.2Zr"),
    "5083-0.7Zr": (1, "5083 + 0.7Zr"), "AlMnSc": (1, "Al-4.5Mn-1.3Mg-0.8Sc-0.7Zr"), "6061-1Zr": (1, "6061 + 1Zr"),
    "X1": (1, "Al-6Mg-2.5Si-0.7Ti"), "AlMg8Si1.3ScZr": (1, "Al-8Mg-1.3Si-Sc-Zr"),
    "7075": (2, "7075"), "6061": (2, "6061"), "2024": (2, "2024"), "Mg3": (2, "Al-3Mg"), "Mg6": (2, "Al-6Mg"),
    "ChalmersE-cracked": (2, "Al-4.7Mn-0.8Cr-0.7Zr-1.0Mg"), "MnMgZr-Yu": (2, "Al-5.8Mn-2.7Mg-0.5Zr (+Er)"),
}


def fig_cracking(th, mode):
    rows = {(r["id"], r["base"]): r for r in read_csv(RES / "calphad" / "named.csv")}
    pts = []
    for cid, (cls, label) in OUTCOME.items():
        r = rows.get((cid, "pureAl"))
        if r and not math.isnan(num(r["kou_index_K"])):
            pts.append((cls, max(num(r["kou_index_K"]), 0.5), label))
    if not pts:
        return
    names = ["prints crack-free without a grain refiner", "prints crack-free with Zr, Sc or Ti", "cracks in published builds"]
    order = sorted(pts, key=lambda p: (p[0], p[1]))
    fig, ax = plt.subplots(figsize=(8.6, 0.27 * len(order) + 1.6))
    for i, (cls, k, label) in enumerate(order):
        ax.plot([k], [i], "o", ms=9, color=th["series"][cls], mec=th["surface"], mew=2, zorder=3)
        ax.text(k * 1.25, i, label, va="center", fontsize=8.5, color=th["ink"])
    for cls in range(3):
        ax.plot([], [], "o", ms=9, color=th["series"][cls], label=names[cls])
    ax.set_xscale("log")
    ax.set_xlim(0.3, 60000)
    ax.set_yticks([])
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Kou index, max |dT/d(fs^0.5)| for fs 0.87-0.94 (K), Scheil, pure-Al base")
    ax.legend(loc="lower right", fontsize=8.5)
    ax.set_title("A solidification index alone does not say which alloys print")
    save(fig, "cracking_index", mode)


# ------------------------------------------------------------------ C. SAASBO hand-off
def fig_saasbo(th, mode):
    runs = [r for p in sorted((RES / "saasbo_handoff").glob("runs_*.jsonl")) for r in read_jsonl(p)]
    if not runs:
        return
    strat = [("six", "six seeds, then the optimizer"), ("six+3sobol", "six + 3 Sobol"), ("six+3axis", "six + 3 hand-picked"),
             ("nine-sobol", "nine Sobol, no hand-picked")]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharey=True)
    for ax, model, title in zip(axes, ("saasbo", "gp"), ("SAASBO", "Standard GP")):
        for j, (key, label) in enumerate(strat):
            cur = [r["curve"] for r in runs if r["model"] == model and r["strategy"] == key and r["delay"] == 1]
            if not cur:
                continue
            m = np.mean(np.array(cur), axis=0)
            x = np.arange(1, len(m) + 1)
            ax.plot(x, m, color=th["series"][j], label=f"{label} (n={len(cur)})")
            ax.plot([x[-1]], [m[-1]], "o", ms=6, color=th["series"][j], mec=th["surface"], mew=1.5)
        rnd = [r["curve"] for r in runs if r["model"] == "random"]
        if rnd:
            m = np.mean(np.array(rnd), axis=0)
            ax.plot(np.arange(1, len(m) + 1), m, color=th["neutral"], lw=1.5, label=f"six seeds, then random (n={len(rnd)})")
        ax.set_title(title)
        ax.set_xlabel("design run")
        ax.set_xlim(1, 25.5)
        ax.legend(loc="lower right", fontsize=8)
    axes[0].set_ylabel("best toy objective so far (MPa)")
    fig.suptitle("Toy campaign of 25 runs: six seeds then the optimizer, against nine seeds first", x=0.06, ha="left",
                 fontsize=12, fontweight="bold", y=1.03)
    save(fig, "saasbo_handoff", mode)


# ------------------------------------------------------------------ D. liquidus against content
def fig_liquidus(th, mode):
    rows = read_csv(RES / "calphad" / "liquidus_vs_content.csv")
    grids = read_csv(RES / "calphad" / "grids.csv")
    series = {}
    for r in rows:
        g = r["grid"]
        if g in ("liq-Zr", "liq-Ti", "liq-Cr", "liq-Mn", "liq-Fe") and r["liquidus_cost507_C"] not in ("", "None"):
            el = g.split("-")[1]
            w = float("".join(ch for ch in r["composition_wt"] if ch.isdigit() or ch == "."))
            series.setdefault(el, []).append((w, float(r["liquidus_cost507_C"])))
    for r in grids:
        if r.get("grid") == "liq-Sc" and r.get("liquidus_C"):
            series.setdefault("Sc", []).append((num(r.get("Sc")), num(r["liquidus_C"])))
    if not series:
        return
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    for j, el in enumerate([e for e in ("Zr", "Ti", "Sc", "Cr", "Mn", "Fe") if e in series]):
        pts = sorted(series[el])
        x, y = [p[0] for p in pts], [p[1] for p in pts]
        ax.plot(x, y, color=th["series"][j], label=el, marker="o", ms=5, mec=th["surface"], mew=1)
        ax.text(x[-1] + 0.08, y[-1], el, va="center", fontsize=9.5, color=th["ink"])
    ax.axhline(840, color=th["neutral"], lw=1)
    ax.text(6.9, 846, "melt setpoint of the runs so far (810-840 °C)", ha="right", fontsize=8, color=th["ink2"])
    ax.set_xlabel("addition to Al (wt%)")
    ax.set_ylabel("liquidus (°C)")
    ax.set_xlim(0, 7.6)
    ax.legend(loc="lower right", ncol=3, fontsize=8.5, title="binary Al-X")
    ax.set_title("How hot the melt must be to keep each addition dissolved")
    save(fig, "liquidus_vs_content", mode)


# ------------------------------------------------------------------ E. Si-Mg map
def fig_simg(th, mode):
    rows = [r for r in read_csv(RES / "calphad" / "grids.csv") if r.get("grid") == "SiMg" and r.get("kou_index_K") not in ("", None)]
    if not rows:
        return
    si = sorted({num(r.get("Si") or 0) for r in rows})
    mg = sorted({num(r.get("Mg") or 0) for r in rows})
    Z = np.full((len(mg), len(si)), np.nan)
    for r in rows:
        Z[mg.index(num(r.get("Mg") or 0)), si.index(num(r.get("Si") or 0))] = num(r["kou_index_K"])
    from matplotlib.colors import LinearSegmentedColormap, LogNorm

    cmap = LinearSegmentedColormap.from_list("seq", th["ramp"])
    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    zmin, zmax = max(np.nanmin(Z), 1.0), np.nanmax(Z)
    im = ax.imshow(Z, origin="lower", cmap=cmap, norm=LogNorm(vmin=zmin, vmax=zmax), aspect="auto")
    ax.set_xticks(range(len(si)), [f"{s:g}" for s in si])
    ax.set_yticks(range(len(mg)), [f"{m:g}" for m in mg])
    ax.grid(False)
    mid = math.sqrt(zmin * zmax)
    for i in range(len(mg)):
        for j in range(len(si)):
            if not np.isnan(Z[i, j]):
                dark_cell = (Z[i, j] > mid) if mode == "light" else (Z[i, j] < mid)
                ax.text(j, i, f"{Z[i, j]:.0f}", ha="center", va="center", fontsize=8.5, color="#ffffff" if dark_cell else "#0b0b0b")
    ax.set_xlabel("Si (wt%)")
    ax.set_ylabel("Mg (wt%)")
    ax.set_title("Kou cracking index (K) across Al-Si-Mg, with 0.15 Fe")
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.outline.set_visible(False)
    cb.set_label("higher = longer terminal freezing", color=th["ink2"])
    save(fig, "simg_map", mode)


def main():
    for mode, th in THEMES.items():
        style(th)
        for f in (fig_scheil, fig_cracking, fig_saasbo, fig_liquidus, fig_simg):
            try:
                f(th, mode)
            except Exception as e:  # noqa: BLE001
                print(f.__name__, mode, "failed:", type(e).__name__, e)
    print("figures:", sorted(p.name for p in FIG.glob("*.png")))


if __name__ == "__main__":
    main()
