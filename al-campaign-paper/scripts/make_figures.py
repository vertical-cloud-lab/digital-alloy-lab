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
import sys
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
DATA = PAPER / "data"
FIG = PAPER / "manuscript" / "figures"
GEN = PAPER / "manuscript" / "generated"
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
    txt = (f"PLACEHOLDER{(' · ' + panel) if panel else ''}\n\n"
           f"Needs: {row['data_needed']}\n\n"
           f"Data file: {row['data_files']}\n"
           f"Gate: {row['gate']} · data due {final:%b %d, %Y} · owner: {row['owner']}")
    ax.text(0.5, 0.5, txt, ha="center", va="center", fontsize=6.3, color=INK2, wrap=True,
            transform=ax.transAxes)


def save(fig, name: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight", dpi=200)
    plt.close(fig)


def style(ax) -> None:
    ax.grid(True, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# ------------------------------------------------------------------------- Fig. 1
def fig1(p, bench, tensile, alloys, burdens) -> str:
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw={"wspace": 0.32})
    status = []

    al = bench[bench["series"].str.startswith("AlSi10Mg")]
    sc = bench[bench["series"].str.startswith("Scalmalloy")]
    ih = inhouse_alsi(tensile)
    ys_m, ys_sd, ys_hw, n = mean_ci(ih["ys_mpa"]) if not ih.empty else (np.nan,) * 3 + (0,)
    el_m, el_sd, _, _ = mean_ci(ih["el_pct"]) if not ih.empty else (np.nan,) * 3 + (0,)
    camp = campaign_tensile(tensile)

    # (a) yield strength vs elongation
    style(a)
    if n:
        # Proposed rule (outline.md): higher yield than the in-house comparator by more than the
        # CIs, at no lower elongation. Shade where a candidate would have to land.
        a.add_patch(Rectangle((el_m, ys_m + ys_hw), 40, 400, facecolor=REGION, edgecolor="none", zorder=0))
        a.text(el_m + 0.5, 553, "stronger than in-house AlSi10Mg, as ductile", ha="left",
               va="top", fontsize=6.3, color=INK2)
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
                  linewidths=0.8, zorder=5, label="campaign alloys")
        status.append("(a) campaign tensile drawn")
    else:
        a.scatter([], [], s=34, color=C_NEW, label="campaign alloys (tensile due Feb 12)")
        status.append("(a) campaign points pending")
    # direct labels (relief for the low-contrast hues; the legend is kept as well)
    a.text(21.0, 318, "Scalmalloy\nas built", color=INK, fontsize=6.3, ha="center", va="center")
    a.text(16.6, 476, "Scalmalloy\naged", color=INK, fontsize=6.3, ha="left", va="center")
    a.text(12.0, 140, "AlSi10Mg\nstress-relieved", color=INK, fontsize=6.3, ha="center", va="center")
    a.text(1.2, 315, "AlSi10Mg\nas built", color=INK, fontsize=6.3, ha="left", va="center")
    a.set_xlim(0, 26)
    a.set_ylim(100, 560)
    a.set_xlabel("Elongation (%)")
    a.set_ylabel("Yield strength (MPa)")
    a.set_title("(a) Strength and ductility", loc="left")
    a.legend(loc="upper left", bbox_to_anchor=(0.0, -0.17), ncol=2, handletextpad=0.3, columnspacing=1.0)

    # (b) yield strength vs critical-mineral burden
    style(b)
    have_b = not burdens.empty and burdens["B_nir"].notna().any()
    if have_b and n:
        b_al = burdens.loc["AlSi10Mg", "B_nir"] if "AlSi10Mg" in burdens.index else np.nan
        b_sc = burdens.loc["Scalmalloy", "B_nir"] if "Scalmalloy" in burdens.index else np.nan
        xmax = np.nanmax([b_al, b_sc]) * 1.35
        if not math.isnan(b_sc):
            b.add_patch(Rectangle((0, ys_m + ys_hw), b_sc, 400, facecolor=REGION, edgecolor="none", zorder=0))
            b.text(b_sc * 0.03, 545, "region of interest: stronger than in-house AlSi10Mg,\nless burden than Scalmalloy",
                   fontsize=6.3, color=INK2, va="top")
        for name, x, rows, col in (("AlSi10Mg", b_al, al, C_ALSI), ("Scalmalloy", b_sc, sc, C_SCAL)):
            if math.isnan(x):
                continue
            ys = rows["yield_MPa"]
            b.vlines(x, ys.min(), ys.max(), color=col, linewidth=2.0, zorder=3)
            b.scatter([x] * len(ys), ys, s=22, facecolors="white", edgecolors=col, linewidths=1.0, zorder=4)
            b.text(x + xmax * 0.02, ys.max(), f"{name}\n(datasheets)", fontsize=6.3, va="top", color=INK)
        b.errorbar(b_al, ys_m, yerr=ys_sd, fmt="o", ms=5.5, color=C_ALSI, mec="white", mew=0.8,
                   elinewidth=0.9, capsize=2, zorder=5)
        cand = burdens.drop(index=[i for i in ("AlSi10Mg", "Scalmalloy") if i in burdens.index])
        if not camp.empty and not cand.empty:
            g = camp.groupby("alloy_id")["ys_mpa"].mean()
            ids = [i for i in g.index if i in cand.index]
            b.scatter(cand.loc[ids, "B_nir"], g[ids], s=34, color=C_NEW, edgecolors="white", zorder=6)
            status.append("(b) campaign points drawn")
        else:
            status.append("(b) campaign points pending")
        b.set_xlim(0, xmax)
        b.set_ylim(100, 560)
        b.set_xlabel("Critical-mineral burden B (wt %, import-weighted; see SI)")
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
    ax.set_ylabel("Yield strength (MPa), mean ± 95 % CI")
    if camp.empty:
        ax.text(0.98, 0.95, "finalists: tensile\ndue Feb 12", transform=ax.transAxes, ha="right", va="top",
                fontsize=6.3, color=INK2)
    ax.set_title("(c) Yield strength", loc="left")
    status.append("(c) in-house AlSi10Mg drawn" + ("" if camp.empty else " with campaign alloys"))
    save(fig, "fig5-mechanical")
    return "; ".join(status)


# ------------------------------------------------------------------------ tables
def tex_escape(s: str) -> str:
    return (str(s).replace("\\", "\\textbackslash{}").replace("&", "\\&").replace("%", "\\%")
            .replace("_", "\\_").replace("#", "\\#").replace("µ", "\\textmu{}").replace("°", "\\textdegree{}"))


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
               .replace("3D Systems Certified Scalmalloy (A) datasheet 2022-02-23", "3D Systems [3dsystems]"))
        key = src[src.find("[") + 1: src.find("]")] if "[" in src else ""
        src = src.split(" [")[0] + (rf"~\cite{{ds_{key}}}" if key else "")
        cond = r["condition"].split(" (")[0]
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


def table_compositions(alloys, burdens) -> None:
    els = ["si", "mg", "mn", "cr", "zr", "sc", "fe", "ni", "ti", "cu", "ce", "er", "zn"]
    num = lambda v: pd.to_numeric(pd.Series([v]), errors="coerce").fillna(0).iloc[0]
    present = [e for e in els if e in alloys.columns and pd.to_numeric(alloys[e], errors="coerce").fillna(0).gt(0).any()]
    ncol = 1 + len(present) + 3
    lines = [rf"\begin{{tabular}}{{@{{}}l{'r' * len(present)}rrr@{{}}}}", r"\toprule"]
    head = ["Alloy"] + [e.capitalize() for e in present] + [r"$B_\mathrm{NIR}$", r"$B_\mathrm{cost}$", "Sc"]
    lines.append(" & ".join(head) + r" \\")
    unit = [""] + ([rf"\multicolumn{{{len(present)}}}{{c}}{{wt\%, nominal}}"] if present else []) + \
           [r"wt\%", r"USD\,kg$^{-1}$", r"wt\%"]
    lines.append(" & ".join(unit) + r" \\")
    lines.append(r"\midrule")
    for _, r in alloys.iterrows():
        vals = [fmt(r.get(e), 2) if num(r.get(e)) > 0 else "--" for e in present]
        bb = burdens.loc[r["alloy_id"]] if (not burdens.empty and r["alloy_id"] in burdens.index) else None
        tail = [fmt(bb["B_nir"], 2), fmt(bb["B_cost"], 2), fmt(bb["Sc"], 2)] if bb is not None else ["--"] * 3
        name = tex_escape(r["name"]) if pd.notna(r.get("name")) else tex_escape(r["alloy_id"])
        if str(r.get("role", "")) not in ("benchmark", ""):
            name += rf" ({tex_escape(r['role'])})"
        lines.append(" & ".join([name] + vals + tail) + r" \\")
    lines.append(r"\midrule")
    lines.append(rf"\multicolumn{{{ncol}}}{{@{{}}l}}{{\placeholder{{Campaign alloys with measured compositions: due Feb 19, 2027}}}} \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (GEN / "tab-compositions.tex").write_text("\n".join(lines) + "\n")


def numbers(tensile, runs, alloys, burdens) -> None:
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
    for aid, macro in (("AlSi10Mg", "BAlSi"), ("Scalmalloy", "BScal")):
        v = burdens.loc[aid, "B_nir"] if (not burdens.empty and aid in burdens.index) else float("nan")
        c = burdens.loc[aid, "B_cost"] if (not burdens.empty and aid in burdens.index) else float("nan")
        lines.append(num(macro + "nir", v, 2, "B"))
        lines.append(num(macro + "cost", c, 2, "B"))
    (GEN / "numbers.tex").write_text("\n".join(lines) + "\n")


def status_md(p: pd.DataFrame, status: dict[str, str]) -> None:
    rows = ["# Figure and table status", "",
            f"*Generated by `scripts/make_figures.py` on {TODAY:%Y-%m-%d}. The plan and the dates are in "
            "[`figure-plan.csv`](figure-plan.csv); edit them there.*", "",
            "| Item | Title | Drawn now | Final data due | Days left | Gate | Owner |",
            "|---|---|---|---|---|---|---|"]
    for pid, r in p.iterrows():
        final = dt.date.fromisoformat(r["final_due"])
        rows.append(f"| {pid} | {r['title']} | {status.get(pid, r['status_2026_11_27'])} | {final:%b %d, %Y} | "
                    f"{(final - TODAY).days} | {r['gate']} | {r['owner']} |")
    (PAPER / "figure-status.md").write_text("\n".join(rows) + "\n")


def main() -> None:
    GEN.mkdir(parents=True, exist_ok=True)
    p = plan()
    bench = pd.read_csv(BENCH) if BENCH.exists() else pd.DataFrame(
        columns=["series", "alloy", "condition", "orientation", "yield_MPa", "uts_MPa", "elongation_pct", "source"])
    tensile, runs, alloys = read("tensile.csv"), read("runs.csv"), read("alloys.csv")
    burdens = mb.table(alloys, mb.load_criticality()) if not alloys.empty else pd.DataFrame()
    status = {
        "Fig1": fig1(p, bench, tensile, alloys, burdens),
        "Fig2": generic("Fig2", p, read("calphad_screen.csv"), "fig2-calphad-screen", draw_calphad),
        "Fig3": generic("Fig3", p, read("powder.csv"), "fig3-powders", draw_powder),
        "Fig4": generic("Fig4", p, read("density.csv"), "fig4-printability", draw_density),
        "Fig5": fig5(p, tensile, read("hardness.csv")),
        "Fig6": generic("Fig6", p, read("corrosion.csv"), "fig6-corrosion", draw_corrosion),
    }
    table_benchmarks(bench, tensile)
    if not alloys.empty:
        table_compositions(alloys, burdens)
    numbers(tensile, runs, alloys, burdens)
    status_md(p, status)
    for k, v in status.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
