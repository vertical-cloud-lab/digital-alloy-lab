#!/usr/bin/env python3
"""Redraw the campaign paper's figures, tables and in-text numbers from the campaign data.

    pip install matplotlib pandas numpy
    python al-campaign-paper/scripts/make_figures.py

Reads   al-campaign-paper/data/*.csv, al-campaign-paper/figure-plan.csv and
        literature/al-lpbf-benchmark-alloys/property-window.csv (vendor datasheets, PR #285).
Writes  al-campaign-paper/manuscript/figures/<id>.pdf and .png,
        al-campaign-paper/manuscript/generated/*.tex (tables and \\newcommand numbers),
        al-campaign-paper/figure-status.md.

The campaign fills the paper as it runs: add rows to the CSVs in data/ and re-run. A figure or
table with no data yet is drawn as a labelled placeholder that says what it needs and when that
data is due (from figure-plan.csv). Nothing here invents a value.
"""
from __future__ import annotations

import datetime as dt
import math
import os
import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mineral_burden as mb  # noqa: E402

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
# Overridable so the tests can run on synthetic data without touching the real outputs.
DATA = Path(os.environ.get("CAMPAIGN_DATA", PAPER / "data"))
FIG = Path(os.environ.get("CAMPAIGN_FIG", PAPER / "manuscript" / "figures"))
GEN = Path(os.environ.get("CAMPAIGN_GEN", PAPER / "manuscript" / "generated"))
STATUS = Path(os.environ.get("CAMPAIGN_STATUS", PAPER / "figure-status.md"))
BENCH = ROOT / "literature" / "al-lpbf-benchmark-alloys" / "property-window.csv"
TODAY = dt.date.today()

# Colour follows the alloy, never the data source. Three hues (validated all-pairs for a
# scatter with the dataviz validator); the source is shown by fill: hollow = datasheet,
# filled = measured by the lab.
C_ALSI = "#257de0"   # AlSi10Mg family
C_SCAL = "#f47230"   # Scalmalloy family
C_NEW = "#00b894"    # campaign alloys
INK = "#191919"
INK2 = "#666666"
GRID = "#e6e6e6"
REGION = "#f2f2f2"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 7.5,
    "axes.labelsize": 8,
    "axes.titlesize": 8.5,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK,
    "axes.linewidth": 0.6,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "xtick.labelcolor": INK,
    "ytick.labelcolor": INK,
    "text.color": INK,
    "legend.frameon": False,
    "legend.fontsize": 7,
    "pdf.fonttype": 42,
    "savefig.dpi": 300,
})


# ----------------------------------------------------------------------------- data
def read(name: str) -> pd.DataFrame:
    p = DATA / name
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p, comment=None)
    return df.dropna(how="all")


def plan() -> pd.DataFrame:
    return pd.read_csv(PAPER / "figure-plan.csv").set_index("id")


def inhouse_alsi(tensile: pd.DataFrame) -> pd.DataFrame:
    if tensile.empty:
        return tensile
    t = tensile[(tensile["alloy_id"] == "AlSi10Mg-commercial") & (tensile["valid"].str.lower() == "yes")]
    return t


def campaign_tensile(tensile: pd.DataFrame) -> pd.DataFrame:
    if tensile.empty:
        return tensile
    return tensile[~tensile["alloy_id"].str.startswith("AlSi10Mg") & (tensile["valid"].str.lower() == "yes")]


def mean_ci(x: pd.Series) -> tuple[float, float, float, int]:
    """Mean, SD, half-width of the 95 % t confidence interval, n."""
    x = pd.to_numeric(x, errors="coerce").dropna()
    n = len(x)
    if n == 0:
        return float("nan"), float("nan"), float("nan"), 0
    m, s = float(x.mean()), float(x.std(ddof=1)) if n > 1 else float("nan")
    t95 = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447, 8: 2.365, 9: 2.306, 10: 2.262}
    hw = t95.get(n, 1.96) * s / math.sqrt(n) if n > 1 else float("nan")
    return m, s, hw, n


# ----------------------------------------------------------------------- helpers
def placeholder(ax, pid: str, p: pd.DataFrame, panel: str = "") -> None:
    """Grey panel saying what data this panel needs and when it is due."""
    row = p.loc[pid]
    ax.set_facecolor("#fafafa")
    for s in ax.spines.values():
        s.set_edgecolor("#bdbdbd")
        s.set_linestyle((0, (3, 2)))
    ax.set_xticks([])
    ax.set_yticks([])
    final = dt.date.fromisoformat(row["final_due"])
    fig = ax.figure
    width_in = ax.get_position().width * fig.get_size_inches()[0]
    ncol = max(18, int(width_in * 72 / (6.3 * 0.58)))
    parts = [f"PLACEHOLDER{(' · ' + panel) if panel else ''}", "",
             f"Needs: {row['data_needed']}", "",
             f"Data file: {row['data_files']}",
             f"Gate: {row['gate']} · data due {final:%b %d, %Y} · owner: {row['owner']}"]
    txt = "\n".join(textwrap.fill(t, ncol) if t else "" for t in parts)
    ax.text(0.5, 0.5, txt, ha="center", va="center", fontsize=6.3, color=INK2, transform=ax.transAxes)


def save(fig, name: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    # No timestamps in the files, so re-running with unchanged data leaves git clean.
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight", dpi=200, metadata={"Software": None})
    plt.close(fig)


def style(ax) -> None:
    ax.grid(True, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# ------------------------------------------------------------------------- Fig. 1
GREY = "#8c8c8c"


def fig1(p, bench, tensile, alloys, burdens, lit, lit_b) -> str:
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.3), gridspec_kw={"wspace": 0.30})
    status = []

    al = bench[bench["series"].str.startswith("AlSi10Mg")]
    sc = bench[bench["series"].str.startswith("Scalmalloy")]
    ih = inhouse_alsi(tensile)
    ys_m, ys_sd, ys_hw, n = mean_ci(ih["ys_mpa"]) if not ih.empty else (np.nan,) * 3 + (0,)
    el_m, el_sd, _, _ = mean_ci(ih["el_pct"]) if not ih.empty else (np.nan,) * 3 + (0,)
    camp = campaign_tensile(tensile)
    com = lit[lit["kind"].str.startswith("commercial")] if not lit.empty else lit
    pap = lit[lit["kind"].str.startswith("peer")] if not lit.empty else lit

    # (a) yield strength vs elongation
    style(a)
    if n:
        # Proposed rule (outline.md): higher yield than the in-house comparator by more than the
        # CIs, at no lower elongation. Shade where a candidate would have to land.
        a.add_patch(Rectangle((el_m, ys_m + ys_hw), 40, 400, facecolor=REGION, edgecolor="none", zorder=0))
        a.text(29.6, 598, "stronger than in-house AlSi10Mg,\nas ductile", ha="right",
               va="top", fontsize=6.3, color=INK2)
    if not lit.empty:
        # Rows that are the two ends of a published range are not a pair: draw the range as a box.
        rng = lit["basis"].astype(str).str.startswith("range end")
        for (aid, cond), g in lit[rng].groupby(["alloy_id", "condition"]):
            a.add_patch(Rectangle((g["el_pct"].min(), g["ys_mpa"].min()), g["el_pct"].max() - g["el_pct"].min(),
                                  g["ys_mpa"].max() - g["ys_mpa"].min(), facecolor="none", edgecolor=GREY,
                                  linewidth=0.8, linestyle=(0, (2, 1.5)), zorder=2))
        com = com[~com["basis"].astype(str).str.startswith("range end")]
        a.plot([], [], color=GREY, linewidth=0.8, linestyle=(0, (2, 1.5)), label="Sc-free, datasheet range")
        a.scatter(com["el_pct"], com["ys_mpa"], s=22, marker="D", facecolors="white", edgecolors=GREY,
                  linewidths=0.9, zorder=2, label="Sc-free, datasheets")
        a.scatter(pap["el_pct"], pap["ys_mpa"], s=26, marker="^", facecolors="white", edgecolors=GREY,
                  linewidths=0.9, zorder=2, label="Sc-free, papers")
    a.scatter(al["elongation_pct"], al["yield_MPa"], s=26, facecolors="white", edgecolors=C_ALSI,
              linewidths=1.0, zorder=3, label="AlSi10Mg, datasheets")
    a.scatter(sc["elongation_pct"], sc["yield_MPa"], s=26, facecolors="white", edgecolors=C_SCAL,
              linewidths=1.0, zorder=3, label="Scalmalloy, datasheets")
    if n:
        a.errorbar(el_m, ys_m, xerr=el_sd, yerr=ys_sd, fmt="o", ms=5.5, color=C_ALSI, mec="white",
                   mew=0.8, elinewidth=0.9, capsize=2, zorder=4,
                   label=f"AlSi10Mg, Utah, as built (n = {n})")
    if not camp.empty:
        g = camp.groupby("alloy_id")
        a.scatter(g["el_pct"].mean(), g["ys_mpa"].mean(), s=34, color=C_NEW, edgecolors="white",
                  linewidths=0.8, zorder=5, label="this work")
        status.append("(a) campaign tensile drawn")
    else:
        a.scatter([], [], s=34, color=C_NEW, label="this work (tensile due Feb 12)")
        status.append("(a) campaign points pending")
    a.text(21.0, 322, "Scalmalloy\nas built", color=INK, fontsize=6.3, ha="center", va="center")
    a.text(16.6, 480, "Scalmalloy\naged", color=INK, fontsize=6.3, ha="left", va="center")
    a.text(12.0, 140, "AlSi10Mg\nstress-relieved", color=INK, fontsize=6.3, ha="center", va="center")
    a.text(1.0, 332, "AlSi10Mg\nas built", color=INK, fontsize=6.3, ha="left", va="center")
    a.set_xlim(0, 30)
    a.set_ylim(100, 600)
    a.set_xlabel("Elongation (%)")
    a.set_ylabel("Yield strength (MPa)")
    a.set_title("(a) Strength and ductility", loc="left")
    a.legend(loc="upper left", bbox_to_anchor=(0.0, -0.17), ncol=2, handletextpad=0.3, columnspacing=0.8)

    # (b) yield strength vs critical-mineral burden B_NIR (interval: USGS gives some reliances as bounds)
    style(b)
    have_b = (not burdens.empty and "B_nir" in burdens and burdens["B_nir"].notna().any()) and n
    if have_b:
        def bvals(aid):
            r = burdens.loc[aid]
            return r["B_nir"], r["B_nir_low"], r["B_nir_high"]
        bsc, bsc_lo, bsc_hi = bvals("Scalmalloy")
        bal, bal_lo, bal_hi = bvals("AlSi10Mg")
        b.add_patch(Rectangle((0, ys_m + ys_hw), bsc_lo, 400, facecolor=REGION, edgecolor="none", zorder=0))
        b.text(0.15, 598, "stronger than in-house AlSi10Mg,\nbelow Scalmalloy's lowest burden",
               fontsize=6.3, color=INK2, va="top")
        if not lit.empty and not lit_b.empty:
            for kind, mk in (("commercial", "D"), ("peer", "^")):
                rows = lit[lit["kind"].str.startswith(kind)]
                rows = rows[rows["alloy_id"].isin(lit_b.index[lit_b["B_nir"].notna()])]
                if rows.empty:
                    continue
                x = lit_b.loc[rows["alloy_id"], "B_nir"].values
                b.scatter(x, rows["ys_mpa"], s=22 if mk == "D" else 26, marker=mk, facecolors="white",
                          edgecolors=GREY, linewidths=0.9, zorder=2)
            # label the low-burden Sc-free alloys that already beat in-house AlSi10Mg
            for aid, lab, dy in (("aheadd-cp1", "Al-Fe-Zr", -16), ("al-fe-mg-zr", "Al-Fe-Mg-Zr", 10),
                                 ("eos-al5x1", "Al-Mg-Zr-Mn", 12), ("croteau-al-mg-zr", "Al-Mg-Zr", -16),
                                 ("chalmers-alloy-f", "Al-Mn-Cr-Zr-Mg", -14)):
                if aid in lit_b.index and not math.isnan(lit_b.loc[aid, "B_nir"]):
                    y = lit.loc[lit["alloy_id"] == aid, "ys_mpa"].max()
                    b.text(lit_b.loc[aid, "B_nir"] + 0.12, y + dy, lab, fontsize=6.0, color=INK2, va="center")
        for name, (x, lo, hi), rows, col in (("AlSi10Mg", (bal, bal_lo, bal_hi), al, C_ALSI),
                                             ("Scalmalloy", (bsc, bsc_lo, bsc_hi), sc, C_SCAL)):
            ys = rows["yield_MPa"]
            b.vlines(x, ys.min(), ys.max(), color=col, linewidth=1.6, zorder=3)
            b.hlines(ys.max(), lo, hi, color=col, linewidth=1.0, zorder=3)
            b.scatter([x] * len(ys), ys, s=22, facecolors="white", edgecolors=col, linewidths=1.0, zorder=4)
            b.text(hi + 0.15, ys.max() + (45 if name == "Scalmalloy" else 0), f"{name}\n(datasheets)",
                   fontsize=6.3, va="center", color=INK)
        b.errorbar(bal, ys_m, yerr=ys_sd, fmt="o", ms=5.5, color=C_ALSI, mec="white", mew=0.8,
                   elinewidth=0.9, capsize=2, zorder=5)
        # planned seeds: burden known from the target composition, strength not yet measured
        seeds = alloys[alloys["role"].astype(str).str.contains("seed")] if not alloys.empty else alloys
        pts = sorted((burdens.loc[r["alloy_id"], "B_nir"], r["alloy_id"]) for _, r in seeds.iterrows()
                     if r["alloy_id"] in burdens.index and not math.isnan(burdens.loc[r["alloy_id"], "B_nir"]))
        prev, level = -9.0, 0
        for x, aid in pts:
            level = level + 1 if x - prev < 0.45 else 0
            prev = x
            b.plot([x, x], [100, 118], color=C_NEW, linewidth=1.4, zorder=5)
            b.text(x, 122 + 13 * level, aid, fontsize=5.8, ha="center", va="bottom", color=INK)
        b.text(8.3, 190, "ticks at the bottom:\nplanned seed compositions,\nburden only", fontsize=6.0,
               color=INK2, ha="left", va="center")
        cand = burdens.drop(index=[i for i in burdens.index if i in ("AlSi10Mg", "Scalmalloy")])
        if not camp.empty and not cand.empty:
            g = camp.groupby("alloy_id")["ys_mpa"].mean()
            ids = [i for i in g.index if i in cand.index]
            b.scatter(cand.loc[ids, "B_nir"], g[ids], s=34, color=C_NEW, edgecolors="white", zorder=6)
            status.append("(b) campaign points drawn")
        else:
            status.append("(b) campaign points pending; seeds shown as burden ticks")
        b.set_xlim(0, 11.5)
        b.set_ylim(100, 600)
        b.set_xlabel("Critical-mineral burden $B_\\mathrm{NIR}$ (wt %, import-weighted)")
        b.set_ylabel("Yield strength (MPa)")
        b.set_title("(b) Strength and critical-mineral burden", loc="left")
    else:
        placeholder(b, "Fig1", p, "(b) needs the burden inputs in data/element-criticality.csv and data/alloys.csv")
        b.set_title("(b) Strength and critical-mineral burden", loc="left")
        status.append("(b) burden inputs missing")
    save(fig, "fig1-benchmark-map")
    return "; ".join(status)


# --------------------------------------------------------------- Figs. 2, 3, 4, 6
def generic(pid: str, p: pd.DataFrame, data: pd.DataFrame, name: str, draw) -> str:
    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    if data.empty:
        placeholder(ax, pid, p)
        ax.set_title(f"{pid}. {p.loc[pid, 'title']}", loc="left")
        out = "placeholder (no rows yet)"
    else:
        style(ax)
        draw(ax, data)
        ax.set_title(f"{pid}. {p.loc[pid, 'title']}", loc="left")
        out = f"drawn from {len(data)} rows"
    save(fig, name)
    return out


def draw_calphad(ax, d):
    sc = ax.scatter(d["freezing_range_c"], d["strengthening_phase_frac"], c=d["burden_B"], cmap="Blues",
                    s=12, edgecolors="none")
    picked = d[d["picked_as"].notna() & (d["picked_as"].astype(str) != "")]
    ax.scatter(picked["freezing_range_c"], picked["strengthening_phase_frac"], s=40, facecolors="none",
               edgecolors=C_NEW, linewidths=1.2, label="picked")
    plt.colorbar(sc, ax=ax, label="burden B")
    ax.set_xlabel("Freezing range (°C)")
    ax.set_ylabel("Strengthening-phase fraction")
    ax.legend(loc="upper right")


def draw_powder(ax, d):
    g = d.groupby("alloy_id")[["d10_um", "d50_um", "d90_um"]].mean()
    x = np.arange(len(g))
    ax.vlines(x, g["d10_um"], g["d90_um"], color=C_NEW, linewidth=2)
    ax.scatter(x, g["d50_um"], color=C_NEW, s=20, zorder=3)
    ax.set_xticks(x, g.index, rotation=30, ha="right")
    ax.set_ylabel("Particle size, D10-D50-D90 (µm)")


def draw_density(ax, d):
    g = d.groupby("alloy_id")["rel_density_pct"].max().sort_values()
    ax.scatter(range(len(g)), g.values, color=C_NEW, s=20)
    ax.axhline(99.0, color=INK2, linewidth=0.8, linestyle=(0, (3, 2)))
    ax.set_xticks(range(len(g)), g.index, rotation=30, ha="right")
    ax.set_ylabel("Best relative density (%)")


def draw_corrosion(ax, d):
    g = d[d["valid"].astype(str).str.lower() == "yes"].groupby("alloy_id")["icorr_ua_cm2"].agg(["mean", "std"])
    ax.errorbar(range(len(g)), g["mean"], yerr=g["std"], fmt="o", color=C_NEW, capsize=2)
    ax.set_xticks(range(len(g)), g.index, rotation=30, ha="right")
    ax.set_yscale("log")
    ax.set_ylabel("Corrosion current density (µA cm$^{-2}$)")


# ------------------------------------------------------------------------- Fig. 5
def fig5(p, tensile, hardness) -> str:
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.6), gridspec_kw={"wspace": 0.45})
    status = []
    if hardness.empty:
        placeholder(axs[0], "Fig5", p, "(a) hardness")
        status.append("(a) placeholder")
    else:
        style(axs[0])
        g = hardness.groupby(["alloy_id", "condition"])["hv_mean"].mean().unstack()
        g.plot(kind="bar", ax=axs[0], legend=True, width=0.7)
        axs[0].set_ylabel("Hardness (HV)")
        status.append("(a) drawn")
    axs[0].set_title("(a) Hardness", loc="left")

    camp = campaign_tensile(tensile)
    placeholder(axs[1], "Fig5", p, "(b) stress-strain, same build") if camp.empty else style(axs[1])
    axs[1].set_title("(b) Stress-strain", loc="left")
    status.append("(b) placeholder" if camp.empty else "(b) needs raw curves (see SI S6)")

    ax = axs[2]
    style(ax)
    ih = inhouse_alsi(tensile)
    groups = [("AlSi10Mg\nUtah (Apr 2026)", ih, C_ALSI)]
    for aid, d in camp.groupby("alloy_id") if not camp.empty else []:
        groups.append((aid, d, C_NEW))
    for i, (lab, d, col) in enumerate(groups):
        m, s, hw, n = mean_ci(d["ys_mpa"])
        ax.bar(i, m, width=0.6, color=col, edgecolor="white", linewidth=0.8)
        if not math.isnan(hw):
            ax.errorbar(i, m, yerr=hw, color=INK, capsize=2, linewidth=0.8)
        ax.text(i, 8, f"n = {n}", ha="center", fontsize=6.3, color="white")
    ax.set_xticks(range(len(groups)), [g[0] for g in groups], fontsize=6.5)
    ax.set_ylabel("Yield strength (MPa)")
    ax.set_ylim(0, 340)
    if camp.empty:
        ax.text(0.5, 0.97, "finalists' tensile due Feb 12", transform=ax.transAxes, ha="center", va="top",
                fontsize=6.3, color=INK2)
    ax.set_title("(c) Yield strength", loc="left")
    status.append("(c) in-house AlSi10Mg drawn" + ("" if camp.empty else " with campaign alloys"))
    save(fig, "fig5-mechanical")
    return "; ".join(status)


# ------------------------------------------------------------------------ tables
def tex_escape(s: str) -> str:
    return (str(s).replace("\\", "\\textbackslash{}").replace("&", "\\&").replace("%", "\\%")
            .replace("_", "\\_").replace("#", "\\#").replace("µ", "\\textmu{}").replace("°", "\\textdegree{}")
            .replace("$", "\\$").replace(">=", "$\\geq$").replace("<", "$<$").replace(">", "$>$"))


def fmt(v, nd=0):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "--"
    return "--" if math.isnan(v) else f"{v:.{nd}f}"


def table_benchmarks(bench, tensile) -> None:
    ih = inhouse_alsi(tensile)
    lines = [r"\begin{tabular}{@{}llllrrr@{}}", r"\toprule",
             r"Alloy & Source & Condition & Orient. & YS (MPa) & UTS (MPa) & EL (\%) \\", r"\midrule"]
    for _, r in bench[bench["series"] != "target"].iterrows():
        src = r["source"].split(" (")[0]
        src = (src.replace("EOS process data sheet EOS M 290 30 um", "EOS M 290 [eos]")
               .replace("Nikon SLM Solutions MDS AlSi10Mg SLM 500 30 um", "Nikon SLM 500 [nikon]")
               .replace("Colibrium Additive M2 Series 5 Al-Mg-Sc 400 W 50 um", "Colibrium M2 [colibrium]")
               .replace("3D Systems Certified Scalmalloy (A) datasheet 2022-02-23", "3D Systems [3dsystems]")
               .replace("3D Systems Certified Scalmalloy", "3D Systems [3dsystems]"))
        key = src[src.find("[") + 1: src.find("]")] if "[" in src else ""
        src = src.split(" [")[0] + (rf"~\cite{{ds_{key}}}" if key else "")
        cond = r["condition"].split(" (")[0]
        if "unmachined" in str(r["series"]):
            cond += ", as-printed surface"
        lines.append(f"{tex_escape(r['alloy'].split(' (')[0])} & {src} & {tex_escape(cond)} & "
                     f"{tex_escape(r['orientation'])} & {fmt(r['yield_MPa'])} & {fmt(r['uts_MPa'])} & "
                     f"{fmt(r['elongation_pct'], 1)} \\\\")
    if not ih.empty:
        ys = mean_ci(ih["ys_mpa"])
        uts = mean_ci(ih["uts_mpa"])
        el = mean_ci(ih["el_pct"])
        lines.append(r"\midrule")
        lines.append(rf"AlSi10Mg & This lab, Utah MIDI, $n={ys[3]}$ & as built, as-printed surface & horizontal & "
                     rf"${ys[0]:.0f}\pm{ys[1]:.0f}$ & ${uts[0]:.0f}\pm{uts[1]:.0f}$ & ${el[0]:.1f}\pm{el[1]:.1f}$ \\")
    lines.append(r"\midrule")
    lines.append(r"\multicolumn{7}{@{}l}{\placeholder{Campaign alloys and in-house AlSi10Mg-type (D1): data due Feb 12, 2027}} \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (GEN / "tab-benchmarks.tex").write_text("\n".join(lines) + "\n")


def interval(bb) -> str:
    lo, hi = bb.get("B_nir_low", float("nan")), bb.get("B_nir_high", float("nan"))
    if any(math.isnan(float(v)) for v in (lo, hi)):
        return "--"
    return f"{lo:.1f}" if abs(hi - lo) < 0.05 else f"{lo:.1f}--{hi:.1f}"


def table_elements() -> None:
    """SI table S3: per-element inputs of the burden metric, straight from data/element-criticality.csv."""
    path = DATA / "element-criticality.csv"
    if not path.exists():
        return
    d = pd.read_csv(path)
    lines = [r"\begin{tabular}{@{}lllrl@{}}", r"\toprule",
             r"Element & On 2025 list & U.S.\ net import reliance, 2025 (\%) & Price (USD\,kg$^{-1}$) & Price basis \\",
             r"\midrule"]
    for _, r in d.iterrows():
        price = fmt(r["price_usd_per_kg"], 2) if pd.notna(r["price_usd_per_kg"]) else "--"
        lines.append(" & ".join([str(r["element"]).capitalize(), tex_escape(r["on_2025_list"]),
                                 tex_escape(r["nir_reported"]), price, tex_escape(r["price_basis"])]) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (GEN / "tab-elements.tex").write_text("\n".join(lines) + "\n")


def table_literature(lit, lit_b) -> None:
    """SI table: scandium-free comparators with their burden (one row per alloy, best strength)."""
    if lit.empty:
        return
    lines = [r"\begin{tabular}{@{}llrrrrl@{}}", r"\toprule",
             r"Alloy & Condition (highest yield listed) & YS (MPa) & EL (\%) & $B_\mathrm{NIR}$ (wt\%) & "
             r"$B_\mathrm{cost}$ (USD\,kg$^{-1}$) & Source \\", r"\midrule"]
    for aid, d in lit.groupby("alloy_id", sort=False):
        r = d.loc[d["ys_mpa"].idxmax()]
        bb = lit_b.loc[aid] if aid in lit_b.index else None
        lines.append(" & ".join([tex_escape(r["name"]), tex_escape(r["condition"]), fmt(r["ys_mpa"]),
                                 fmt(r["el_pct"], 1), interval(bb) if bb is not None else "--",
                                 fmt(bb["B_cost"], 2) if bb is not None else "--",
                                 rf"\cite{{{r['cite_key']}}}"]) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (GEN / "tab-literature.tex").write_text("\n".join(lines) + "\n")


def table_compositions(alloys, burdens) -> None:
    els = ["si", "mg", "mn", "cr", "zr", "sc", "fe", "ni", "ti", "cu", "ce", "er", "zn"]
    num = lambda v: pd.to_numeric(pd.Series([v]), errors="coerce").fillna(0).iloc[0]
    present = [e for e in els if e in alloys.columns and pd.to_numeric(alloys[e], errors="coerce").fillna(0).gt(0).any()]
    ncol = 1 + len(present) + 2
    lines = [rf"\begin{{tabular}}{{@{{}}l{'r' * len(present)}rr@{{}}}}", r"\toprule"]
    head = ["Alloy"] + [e.capitalize() for e in present] + [r"$B_\mathrm{NIR}$", r"$B_\mathrm{cost}$"]
    lines.append(" & ".join(head) + r" \\")
    unit = [""] + ([rf"\multicolumn{{{len(present)}}}{{c}}{{wt\%, nominal}}"] if present else []) + \
           [r"wt\%", r"USD\,kg$^{-1}$"]
    lines.append(" & ".join(unit) + r" \\")
    lines.append(r"\midrule")
    for _, r in alloys.iterrows():
        vals = [fmt(r.get(e), 2) if num(r.get(e)) > 0 else "--" for e in present]
        bb = burdens.loc[r["alloy_id"]] if (not burdens.empty and r["alloy_id"] in burdens.index) else None
        tail = ([interval(bb), fmt(bb["B_cost"], 2)] if bb is not None else ["--"] * 2)
        name = tex_escape(r["name"]) if pd.notna(r.get("name")) else tex_escape(r["alloy_id"])
        if str(r.get("role", "")) not in ("benchmark", ""):
            name += rf" ({tex_escape(r['role'])})"
        lines.append(" & ".join([name] + vals + tail) + r" \\")
    lines.append(r"\midrule")
    lines.append(rf"\multicolumn{{{ncol}}}{{@{{}}l}}{{\placeholder{{Campaign alloys with measured compositions: due Feb 19, 2027}}}} \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (GEN / "tab-compositions.tex").write_text("\n".join(lines) + "\n")


def numbers(tensile, runs, alloys, burdens, lit=None, lit_b=None) -> None:
    ih = inhouse_alsi(tensile)
    ys = mean_ci(ih["ys_mpa"]) if not ih.empty else (np.nan,) * 3 + (0,)
    uts = mean_ci(ih["uts_mpa"]) if not ih.empty else (np.nan,) * 3 + (0,)
    el = mean_ci(ih["el_pct"]) if not ih.empty else (np.nan,) * 3 + (0,)
    al_runs = runs[runs["alloy_id"].notna()] if not runs.empty else runs
    cand = alloys[alloys["role"].isin(["seed", "pick", "finalist"])] if not alloys.empty else alloys

    def num(name, v, nd=0, ph="[--]"):
        try:
            ok = not math.isnan(float(v))
        except (TypeError, ValueError):
            ok = False
        return rf"\newcommand{{\{name}}}{{{(f'{float(v):.{nd}f}' if ok else rf'\placeholder{{{ph}}}')}}}"

    lines = ["% Generated by scripts/make_figures.py. Do not edit by hand.",
             num("InhouseYS", ys[0]), num("InhouseYSsd", ys[1]), num("InhouseYShw", ys[2]),
             num("InhouseUTS", uts[0]), num("InhouseUTSsd", uts[1]),
             num("InhouseEL", el[0], 1), num("InhouseELsd", el[1], 1), num("InhouseN", ys[3]),
             num("NAlRuns", len(al_runs) if len(al_runs) else float("nan"), 0, "N runs"),
             num("NCompositions", len(cand) if len(cand) else float("nan"), 0, "N compositions")]
    def g(aid, col):
        return burdens.loc[aid, col] if (not burdens.empty and aid in burdens.index) else float("nan")
    for aid, macro in (("AlSi10Mg", "BAlSi"), ("Scalmalloy", "BScal"), ("S1", "BSone"), ("S2", "BStwo"),
                       ("S3", "BSthree"), ("S4", "BSfour"), ("O1", "BOone")):
        lines.append(num(macro + "nir", g(aid, "B_nir"), 1, "B"))
        lines.append(num(macro + "nirlo", g(aid, "B_nir_low"), 1, "B"))
        lines.append(num(macro + "nirhi", g(aid, "B_nir_high"), 1, "B"))
        lines.append(num(macro + "nirallo", g(aid, "B_nir_al_low"), 1, "B"))
        lines.append(num(macro + "niralhi", g(aid, "B_nir_al_high"), 1, "B"))
        c = g(aid, "B_cost")
        lines.append(num(macro + "cost", c, 0 if (not math.isnan(c) and c >= 10) else 2, "B"))
    # Comparisons typed in the text, generated here so they follow the data.
    lines += [num("InhouseYSpctEOS", 100 * ys[0] / 270), num("InhouseUTSpctEOS", 100 * uts[0] / 461)]
    sc_w = g("Scalmalloy", "Sc")
    sc_cost = g("Scalmalloy", "B_cost")
    master = sc_w / 2.0 * 30.0  # kg of Al-2Sc master alloy per kg of alloy is w_Sc/2; USGS: 30 USD/kg
    sc_cost_master = sc_cost - sc_w / 100.0 * 5200.0 + master
    lines += [num("ScalSc", sc_w, 2), num("ScalMasterCost", master), num("ScalCostMaster", sc_cost_master)]
    if lit is not None and not lit.empty and lit_b is not None and not lit_b.empty:
        ag = set(lit.loc[lit["family"].astype(str).str.contains("Ag"), "alloy_id"])
        nonag = lit_b.loc[[a for a in lit_b.index if a not in ag], "B_cost"].dropna()
        agc = lit_b.loc[[a for a in lit_b.index if a in ag], "B_cost_priced"].dropna()
        # Floors, because the text says "at least".
        lines += [num("CostRedMinNonAg", math.floor(100 * (1 - nonag.max() / sc_cost))),
                  num("CostRedMinMaster", math.floor(100 * (1 - nonag.max() / sc_cost_master))),
                  num("CostRedAgLo", math.floor(100 * (1 - agc.max() / sc_cost))),
                  num("CostRedAgHi", math.floor(100 * (1 - agc.min() / sc_cost)))]
    # Sc-free comparators already in the region of interest: stronger than in-house AlSi10Mg by more than
    # its 95 % CI half-width, and below Scalmalloy's lowest B_NIR (midpoint, and robustly at the high end).
    if lit is not None and not lit.empty and lit_b is not None and not lit_b.empty and ys[3]:
        sc_lo = g("Scalmalloy", "B_nir_low")
        best = lit.groupby("alloy_id")["ys_mpa"].max()
        thr = ys[0] + ys[2]
        mid = [a for a in best.index if best[a] > thr and lit_b.loc[a, "B_nir"] < sc_lo]
        rob = [a for a in best.index if best[a] > thr and lit_b.loc[a, "B_nir_high"] < sc_lo]
        onmap = [a for a in best.index if not math.isnan(lit_b.loc[a, "B_nir"])]
        ds_bar = 300.0  # strongest machined as-built AlSi10Mg datasheet row (Nikon, horizontal)
        mid_ds = [a for a in onmap if best[a] > ds_bar and lit_b.loc[a, "B_nir"] < sc_lo]
        rob_ds = [a for a in onmap if best[a] > ds_bar and lit_b.loc[a, "B_nir_high"] < sc_lo]
        lines += [num("NLit", len(onmap)), num("NLitRegionMid", len(mid)), num("NLitRegionRobust", len(rob)),
                  num("NLitRegionMidDS", len(mid_ds)), num("NLitRegionRobustDS", len(rob_ds)), num("YSbar", thr)]
    (GEN / "numbers.tex").write_text("\n".join(lines) + "\n")


def status_md(p: pd.DataFrame, status: dict[str, str]) -> None:
    rows = ["# Figure and table status", "",
            f"*Generated by `scripts/make_figures.py` on {TODAY:%Y-%m-%d}. The plan and the dates are in "
            "[`figure-plan.csv`](figure-plan.csv); edit them there.*", "",
            "| Item | Title | Drawn now | Draft due | Final data due | Days left | Gate | Owner |",
            "|---|---|---|---|---|---|---|---|"]
    for pid, r in p.iterrows():
        final = dt.date.fromisoformat(r["final_due"])
        draft = dt.date.fromisoformat(r["draft_due"])
        rows.append(f"| {pid} | {r['title']} | {status.get(pid, r['status_2026_11_27'])} | {draft:%b %d} | {final:%b %d, %Y} | "
                    f"{(final - TODAY).days} | {r['gate']} | {r['owner']} |")
    STATUS.write_text("\n".join(rows) + "\n")


def main() -> None:
    GEN.mkdir(parents=True, exist_ok=True)
    p = plan()
    bench = pd.read_csv(BENCH) if BENCH.exists() else pd.DataFrame(
        columns=["series", "alloy", "condition", "orientation", "yield_MPa", "uts_MPa", "elongation_pct", "source"])
    tensile, runs, alloys = read("tensile.csv"), read("runs.csv"), read("alloys.csv")
    crit = mb.load_criticality()
    burdens = mb.table(alloys, crit) if not alloys.empty else pd.DataFrame()
    lit = read("literature-alloys.csv")
    lit_b = mb.table(lit.drop_duplicates("alloy_id"), crit) if not lit.empty else pd.DataFrame()
    status = {
        "Fig1": fig1(p, bench, tensile, alloys, burdens, lit, lit_b),
        "Fig2": generic("Fig2", p, read("calphad_screen.csv"), "fig2-calphad-screen", draw_calphad),
        "Fig3": generic("Fig3", p, read("powder.csv"), "fig3-powders", draw_powder),
        "Fig4": generic("Fig4", p, read("density.csv"), "fig4-printability", draw_density),
        "Fig5": fig5(p, tensile, read("hardness.csv")),
        "Fig6": generic("Fig6", p, read("corrosion.csv"), "fig6-corrosion", draw_corrosion),
    }
    table_benchmarks(bench, tensile)
    if not alloys.empty:
        table_compositions(alloys, burdens)
    table_literature(lit, lit_b)
    table_elements()
    numbers(tensile, runs, alloys, burdens, lit, lit_b)
    status_md(p, status)
    for k, v in status.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
