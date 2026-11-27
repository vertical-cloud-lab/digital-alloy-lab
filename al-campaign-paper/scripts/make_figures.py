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
import matplotlib.cm
import matplotlib.colors

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
DOMINATED = "#d9d9d9"  # part of the region of interest the Sc-free front already covers
# Sc-free commercial baselines, bought and printed in-house (../baselines.md). They are drawn in neutral ink
# with a square marker and a direct label, not in a fourth hue: no fourth hue passes the all-pairs colour
# check against the three above (dataviz validator, light mode).
C_BASE = INK
BASELINES = {"Al5X1": "eos-al5x1", "Al-HS1": "hoganas-al-hs1"}  # alloys.csv id -> literature-alloys.csv id
# tensile.csv alloy_id prefixes of bought (commercial) powders; everything else is a campaign alloy.
COMMERCIAL_RE = r"^(AlSi10Mg|Scalmalloy|Al5X1|Al-HS1)"

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
    """Valid tests of the campaign's own alloys (not the bought benchmark and baseline powders)."""
    if tensile.empty:
        return tensile
    aid = tensile["alloy_id"].astype(str)
    return tensile[~aid.str.match(COMMERCIAL_RE) & (tensile["valid"].astype(str).str.lower() == "yes")]


def commercial_tensile(tensile: pd.DataFrame, base: str) -> pd.DataFrame:
    """Valid in-house tests of a bought powder, e.g. base "Al5X1" matches alloy_id "Al5X1-commercial"."""
    if tensile.empty:
        return tensile
    aid = tensile["alloy_id"].astype(str)
    return tensile[aid.str.startswith(base + "-commercial") & (tensile["valid"].astype(str).str.lower() == "yes")]


def cond_class(c) -> str:
    """Condition classes used to match an in-house test with a datasheet row."""
    c = str(c).lower()
    if "stress" in c:
        return "stress-relieved"
    if "age" in c or "heat" in c or "t6" in c or "t7" in c:
        return "aged"
    return "as built"


def datasheet_ys(base: str, cls: str, bench: pd.DataFrame, lit: pd.DataFrame) -> list[float]:
    """Datasheet yield strengths (horizontal bars) that an in-house horizontal bar of `base` in condition class
    `cls` is compared with: the benchmark sheets of PR #285 for AlSi10Mg and Scalmalloy, the vendor's own sheet
    for a baseline. Empty if the vendor gives none for that condition (e.g. AlSi10Mg aged: we don't T6)."""
    if base in ("AlSi10Mg", "Scalmalloy"):
        if bench.empty:
            return []
        rows = bench[bench["orientation"].astype(str) == "horizontal"]
        if cls == "as built":
            rows = rows[rows["series"] == f"{base} as-built"]
        elif cls == "stress-relieved" and base == "AlSi10Mg":
            rows = rows[rows["condition"].astype(str).str.contains("stress relief")]
        elif cls == "aged" and base == "Scalmalloy":
            rows = rows[rows["series"] == "Scalmalloy aged"]
        else:
            return []
        return rows["yield_MPa"].astype(float).tolist()
    lid = BASELINES.get(base)
    if lid is None or lit.empty:
        return []
    rows = lit[(lit["alloy_id"] == lid) & lit["orientation"].astype(str).isin(["H", "XY"])]
    aged = rows["condition"].astype(str).str.contains("aged")
    rows = rows[aged] if cls == "aged" else rows[~aged]
    return rows["ys_mpa"].astype(float).tolist()


def lit_best(lit: pd.DataFrame, lit_b: pd.DataFrame) -> pd.DataFrame:
    """One point per Sc-free comparator: its highest listed yield strength and its B_NIR midpoint."""
    if lit.empty or lit_b.empty:
        return pd.DataFrame(columns=["ys", "b"])
    best = lit.groupby("alloy_id")["ys_mpa"].max()
    return pd.DataFrame({"ys": best, "b": lit_b["B_nir"].reindex(best.index)}).dropna()


def front_points(pts: pd.DataFrame) -> pd.DataFrame:
    """The rows of pts (columns b, ys) that no other row beats on both lower burden and higher strength."""
    keep = mb.pareto_front([(i, float(r["b"]), float(r["ys"])) for i, r in pts.iterrows()])
    return pts.loc[keep].sort_values("b")


def staircase(ax, front: pd.DataFrame, x1: float, y0: float, shade: bool, **line) -> None:
    """Draw a lower-burden/higher-strength front as a staircase up to x1, and optionally shade the part of
    the box above y0 that it dominates (burden >= a front point's and strength <= it)."""
    f = front[front["b"] < x1].sort_values("b")
    if f.empty:
        return
    bs, ss = f["b"].tolist(), f["ys"].tolist()
    edges = bs[1:] + [x1]
    if shade:
        for b, s, e in zip(bs, ss, edges):
            if s > y0 and e > b:
                ax.add_patch(Rectangle((b, y0), e - b, s - y0, facecolor=DOMINATED, edgecolor="none", zorder=0.5))
    lx, ly = [bs[0], bs[0]], [y0, ss[0]]
    for i in range(1, len(bs)):
        lx += [bs[i], bs[i]]
        ly += [ss[i - 1], ss[i]]
    lx.append(x1)
    ly.append(ss[-1])
    ax.plot(lx, ly, **line)


def verdict_vs_scal(comp: dict, comps: dict, crit: pd.DataFrame) -> str:
    """Below / above / depends: B_NIR against Scalmalloy with both under the same import reliances."""
    if "Scalmalloy" not in comps:
        return "--"
    lo, hi = mb.paired_difference(comp, comps["Scalmalloy"], crit)
    if math.isnan(lo):
        return "--"
    return "below" if hi < 0 else ("above" if lo > 0 else "depends")


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
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.5), gridspec_kw={"wspace": 0.30})
    status = []

    al = bench[bench["series"].str.startswith("AlSi10Mg")]
    sc = bench[bench["series"].str.startswith("Scalmalloy")]
    ih = inhouse_alsi(tensile)
    ys_m, ys_sd, ys_hw, n = mean_ci(ih["ys_mpa"]) if not ih.empty else (np.nan,) * 3 + (0,)
    el_m, el_sd, _, _ = mean_ci(ih["el_pct"]) if not ih.empty else (np.nan,) * 3 + (0,)
    camp = campaign_tensile(tensile)
    base_ids = set(BASELINES.values())
    others = lit[~lit["alloy_id"].isin(base_ids)] if not lit.empty else lit
    base_rows = lit[lit["alloy_id"].isin(base_ids)] if not lit.empty else lit
    com = others[others["kind"].str.startswith("commercial")] if not others.empty else others
    pap = others[others["kind"].str.startswith("peer")] if not others.empty else others
    # in-house tests of the bought baseline powders (filled squares once they exist)
    ih_base = {k: commercial_tensile(tensile, k) for k in BASELINES}
    have_ih_base = any(not d.empty for d in ih_base.values())

    # (a) yield strength vs elongation
    style(a)
    if n:
        # Proposed rule (preregistration.md): higher yield than the in-house comparator by more than the
        # CIs, at no lower elongation. Shade where a candidate would have to land.
        a.add_patch(Rectangle((el_m, ys_m + ys_hw), 40, 400, facecolor=REGION, edgecolor="none", zorder=0))
        a.text(29.6, 598, "stronger than in-house AlSi10Mg,\nas ductile", ha="right",
               va="top", fontsize=6.3, color=INK2)
    if not others.empty:
        # Rows that are the two ends of a published range are not a pair: draw the range as a box.
        rng = others["basis"].astype(str).str.startswith("range end")
        for (aid, cond), g in others[rng].groupby(["alloy_id", "condition"]):
            a.add_patch(Rectangle((g["el_pct"].min(), g["ys_mpa"].min()), g["el_pct"].max() - g["el_pct"].min(),
                                  g["ys_mpa"].max() - g["ys_mpa"].min(), facecolor="none", edgecolor=GREY,
                                  linewidth=0.8, linestyle=(0, (2, 1.5)), zorder=2))
        com = com[~com["basis"].astype(str).str.startswith("range end")]
        a.plot([], [], color=GREY, linewidth=0.8, linestyle=(0, (2, 1.5)), label="Sc-free, datasheet range")
        a.scatter(com["el_pct"], com["ys_mpa"], s=22, marker="D", facecolors="white", edgecolors=GREY,
                  linewidths=0.9, zorder=2, label="Sc-free, datasheets")
        a.scatter(pap["el_pct"], pap["ys_mpa"], s=26, marker="^", facecolors="white", edgecolors=GREY,
                  linewidths=0.9, zorder=2, label="Sc-free, papers")
    if not base_rows.empty:
        a.scatter(base_rows["el_pct"], base_rows["ys_mpa"], s=30, marker="s", facecolors="white",
                  edgecolors=C_BASE, linewidths=1.0, zorder=4, label="Sc-free baselines, datasheets")
        for aid, lab, xy in (("eos-al5x1", "Al5X1 aged", (21.5, 428)), ("hoganas-al-hs1", "Al-HS1 aged", (21.5, 392))):
            g = base_rows[base_rows["alloy_id"] == aid]
            if not g.empty:
                top = g.loc[g["ys_mpa"].idxmax()]
                a.annotate(lab, xy=(top["el_pct"], top["ys_mpa"]), xytext=xy, fontsize=6.3, color=INK,
                           ha="left", va="center",
                           arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.5, shrinkA=1, shrinkB=4))
    a.scatter(al["elongation_pct"], al["yield_MPa"], s=26, facecolors="white", edgecolors=C_ALSI,
              linewidths=1.0, zorder=3, label="AlSi10Mg, datasheets")
    a.scatter(sc["elongation_pct"], sc["yield_MPa"], s=26, facecolors="white", edgecolors=C_SCAL,
              linewidths=1.0, zorder=3, label="Scalmalloy, datasheets")
    if n:
        a.errorbar(el_m, ys_m, xerr=el_sd, yerr=ys_sd, fmt="o", ms=5.5, color=C_ALSI, mec="white",
                   mew=0.8, elinewidth=0.9, capsize=2, zorder=5,
                   label=f"AlSi10Mg, Utah, as built (n = {n})")
    if have_ih_base:
        for k, d in ih_base.items():
            for cls, g in d.groupby(d["condition"].map(cond_class)):
                m, s_, _, nn = mean_ci(g["ys_mpa"])
                e, es, _, _ = mean_ci(g["el_pct"])
                a.errorbar(e, m, xerr=es, yerr=s_, fmt="s", ms=5.5, color=C_BASE, mec="white", mew=0.8,
                           elinewidth=0.9, capsize=2, zorder=5)
        a.errorbar([], [], fmt="s", ms=5.5, color=C_BASE, mec="white", label="Sc-free baselines, in-house")
        status.append("(a) in-house baselines drawn")
    else:
        a.scatter([], [], s=30, marker="s", color=C_BASE, label="Sc-free baselines, in-house (due Feb 12)")
    if not camp.empty:
        g = camp.groupby("alloy_id")
        a.scatter(g["el_pct"].mean(), g["ys_mpa"].mean(), s=34, color=C_NEW, edgecolors="white",
                  linewidths=0.8, zorder=6, label="this work")
        status.append("(a) campaign tensile drawn")
    else:
        a.scatter([], [], s=34, color=C_NEW, label="this work (tensile due Feb 12)")
        status.append("(a) campaign points pending")
    a.plot([], [], color=INK2, linewidth=1.0, linestyle=(0, (4, 2)), label="Sc-free front, reported values")
    a.text(21.0, 322, "Scalmalloy\nas built", color=INK, fontsize=6.3, ha="center", va="center")
    a.text(16.6, 480, "Scalmalloy\naged", color=INK, fontsize=6.3, ha="left", va="center")
    a.text(12.0, 140, "AlSi10Mg\nstress-relieved", color=INK, fontsize=6.3, ha="center", va="center")
    a.text(1.0, 332, "AlSi10Mg\nas built", color=INK, fontsize=6.3, ha="left", va="center")
    a.set_xlim(0, 30)
    a.set_ylim(100, 600)
    a.set_xlabel("Elongation (%)")
    a.set_ylabel("Yield strength (MPa)")
    a.set_title("(a) Strength and ductility", loc="left")
    a.legend(loc="upper left", bbox_to_anchor=(0.0, -0.17), ncol=3, handletextpad=0.3, columnspacing=0.8)

    # (b) yield strength vs critical-mineral burden B_NIR, plotted at the midpoint reliances
    style(b)
    have_b = (not burdens.empty and "B_nir" in burdens and burdens["B_nir"].notna().any()) and n
    if have_b:
        def bvals(aid):
            r = burdens.loc[aid]
            return r["B_nir"], r["B_nir_low"], r["B_nir_high"]
        bsc, bsc_lo, bsc_hi = bvals("Scalmalloy")
        bal, bal_lo, bal_hi = bvals("AlSi10Mg")
        ybar = ys_m + ys_hw
        # Region of interest at the midpoint reliances: stronger than in-house AlSi10Mg, less burden than
        # Scalmalloy. The claim itself is tested with both alloys under the same reliances (Methods).
        b.add_patch(Rectangle((0, ybar), bsc, 600 - ybar, facecolor=REGION, edgecolor="none", zorder=0))
        # The Sc-free front on reported values (datasheets and papers, best condition of each alloy).
        best = lit_best(lit, lit_b)
        front = front_points(best) if not best.empty else best
        if not front.empty:
            staircase(b, front, bsc, ybar, shade=True, color=INK2, linewidth=1.0, linestyle=(0, (4, 2)), zorder=1)
        b.text(0.12, 594, "light: a new alloy here\nexpands the Sc-free front", fontsize=6.0, color=INK2, va="top")
        if not others.empty and not lit_b.empty:
            for kind, mk in (("commercial", "D"), ("peer", "^")):
                rows = others[others["kind"].str.startswith(kind)]
                rows = rows[rows["alloy_id"].isin(lit_b.index[lit_b["B_nir"].notna()])]
                if rows.empty:
                    continue
                x = lit_b.loc[rows["alloy_id"], "B_nir"].values
                b.scatter(x, rows["ys_mpa"], s=22 if mk == "D" else 26, marker=mk, facecolors="white",
                          edgecolors=GREY, linewidths=0.9, zorder=2)
            for aid, lab, dx, dy, ha in (("aheadd-cp1", "Al-Fe-Zr", 0.12, -16, "left"),
                                         ("al-fe-mg-zr", "Al-Fe-Mg-Zr", 0.2, 20, "center"),
                                         ("eos-al2139", "Al2139 T4", -0.15, 10, "right"),
                                         ("chalmers-alloy-f", "Al-Mn-Cr-Zr-Mg", 0.45, 18, "left")):
                if aid in lit_b.index and not math.isnan(lit_b.loc[aid, "B_nir"]):
                    y = lit.loc[lit["alloy_id"] == aid, "ys_mpa"].max()
                    b.text(lit_b.loc[aid, "B_nir"] + dx, y + dy, lab, fontsize=6.0, color=INK2, va="center", ha=ha)
        # Baselines: datasheet values (hollow squares, interval bar at the top value), in-house when measured.
        for k, lid in BASELINES.items():
            if k not in burdens.index or base_rows.empty:
                continue
            x, lo, hi = bvals(k)
            g = base_rows[base_rows["alloy_id"] == lid]
            if g.empty or math.isnan(x):
                continue
            b.hlines(g["ys_mpa"].max(), lo, hi, color=C_BASE, linewidth=1.0, zorder=3)
            b.scatter([x] * len(g), g["ys_mpa"], s=30, marker="s", facecolors="white", edgecolors=C_BASE,
                      linewidths=1.0, zorder=4)
            if k == "Al5X1":
                b.text(lo - 0.1, g["ys_mpa"].max() - 42, f"{k}\n(datasheet)", fontsize=6.3, color=INK,
                       va="center", ha="right")
            else:
                b.text(x + 0.14, g["ys_mpa"].min() - 22, f"{k}\n(datasheet)", fontsize=6.3, color=INK, va="center")
            d = ih_base.get(k)
            if d is not None and not d.empty:
                for cls, gg in d.groupby(d["condition"].map(cond_class)):
                    m, s_, _, _ = mean_ci(gg["ys_mpa"])
                    b.errorbar(x, m, yerr=s_, fmt="s", ms=5.5, color=C_BASE, mec="white", mew=0.8,
                               elinewidth=0.9, capsize=2, zorder=6)
        if have_ih_base:
            pts = []
            for k, d in ih_base.items():
                if not d.empty and k in burdens.index:
                    pts.append((k, burdens.loc[k, "B_nir"], d.groupby(d["condition"].map(cond_class))["ys_mpa"].mean().max()))
            ihf = pd.DataFrame([(q[1], q[2]) for q in pts], columns=["b", "ys"], index=[q[0] for q in pts])
            staircase(b, front_points(ihf), bsc, ybar, shade=False, color=C_BASE, linewidth=1.2, zorder=5)
            status.append("(b) in-house baseline front drawn")
        for name, (x, lo, hi), rows, col in (("AlSi10Mg", (bal, bal_lo, bal_hi), al, C_ALSI),
                                             ("Scalmalloy", (bsc, bsc_lo, bsc_hi), sc, C_SCAL)):
            ys = rows["yield_MPa"]
            b.vlines(x, ys.min(), ys.max(), color=col, linewidth=1.6, zorder=3)
            b.hlines(ys.max(), lo, hi, color=col, linewidth=1.0, zorder=3)
            b.scatter([x] * len(ys), ys, s=22, facecolors="white", edgecolors=col, linewidths=1.0, zorder=4)
            if name == "Scalmalloy":
                b.text(hi + 0.12, 545, f"{name} (datasheets)", fontsize=6.3, va="center", color=INK)
            else:
                b.text(hi + 0.15, ys.max(), f"{name}\n(datasheets)", fontsize=6.3, va="center", color=INK)
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
        cand = burdens.drop(index=[i for i in burdens.index if i in ("AlSi10Mg", "Scalmalloy") or i in BASELINES])
        if not camp.empty and not cand.empty:
            g = camp.groupby("alloy_id")["ys_mpa"].mean()
            ids = [i for i in g.index if i in cand.index]
            b.scatter(cand.loc[ids, "B_nir"], g[ids], s=34, color=C_NEW, edgecolors="white", zorder=7)
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


def fig2(p, d, crit) -> str:
    """Printability screen: Kou's crack index against the freezing range of the aluminum matrix, coloured by
    import-weighted burden. Filled markers have a Zr-, Sc- or Ti-bearing primary phase (a possible grain refiner);
    known crackers are drawn as squares with the same fill rule, so a cracker with such a phase stays visible."""
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    if d.empty:
        placeholder(ax, "Fig2", p)
        ax.set_title(f"Fig2. {p.loc['Fig2', 'title']}", loc="left")
        save(fig, "fig2-calphad-screen")
        return "placeholder (no rows yet)"
    style(ax)
    b = mb.table(d.rename(columns={"composition_id": "alloy_id"}), crit)["B_nir"].values
    x = pd.to_numeric(d["csc_index"], errors="coerce").clip(lower=1).values
    y = pd.to_numeric(d["freezing_range_c"], errors="coerce").values
    prim = d["primary_phase"].astype(str).str.upper()
    refiner = (prim.str.contains("AL3") | prim.str.contains("ZR") | prim.str.contains("SC")).values
    crack = d["family"].astype(str).eq("known-cracker").values
    picked = d["picked_as"].fillna("").astype(str).replace("nan", "").values
    norm = matplotlib.colors.Normalize(vmin=0, vmax=np.nanmax(b) if np.isfinite(np.nanmax(b)) else 1)
    cmap = matplotlib.colormaps["Blues"]
    # Draw published alloys first, crackers next, the lab's planned compositions last (on top).
    order = sorted(range(len(d)), key=lambda i: (bool(picked[i]), crack[i]))
    for i in order:
        c = cmap(0.25 + 0.75 * norm(b[i])) if np.isfinite(b[i]) else GREY
        mk = "s" if crack[i] else "o"
        z = 4 if picked[i] else (3 if crack[i] else 2)
        size = 34 if picked[i] else 26
        if refiner[i]:
            ax.scatter(x[i], y[i], marker=mk, s=size, color=c, edgecolors=INK if crack[i] else INK2,
                       linewidths=1.1 if crack[i] else 0.5, zorder=z)
        else:
            ax.scatter(x[i], y[i], marker=mk, s=size, facecolors="white", edgecolors=INK if crack[i] else c,
                       linewidths=1.2, zorder=z)
        if picked[i]:
            off = {"O1": (-16, -11), "D2": (5, 4), "O2-noEr": (-52, -10), "S1": (4, -10), "S2": (-16, -10)}.get(
                picked[i], (5, 3))
            ax.annotate(picked[i].replace("-noEr", " (no Er)"), (x[i], y[i]), xytext=off,
                        textcoords="offset points", fontsize=6.3, color=INK, zorder=5)
    sm = matplotlib.cm.ScalarMappable(norm=norm, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
        "b", [cmap(0.25), cmap(1.0)]))
    cb = fig.colorbar(sm, ax=ax, pad=0.01)
    cb.set_label("$B_\\mathrm{NIR}$ midpoint (wt %)", fontsize=7)
    ax.set_xscale("log")
    ax.set_xlabel("Kou crack-susceptibility index near the end of solidification (K)")
    ax.set_ylabel("Freezing range of the Al matrix (K)")
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([], [], marker="o", ls="", color=GREY, mec=INK2, label="Zr-, Sc- or Ti-bearing primary phase"),
                       Line2D([], [], marker="o", ls="", mfc="white", mec=GREY, label="no such primary phase"),
                       Line2D([], [], marker="s", ls="", mfc="white", mec=INK, label="known to crack in LPBF (same fill rule)")],
              loc="upper left", fontsize=6.3)
    prelim = d["note"].astype(str).str.contains("preliminary").any() if "note" in d else False
    ax.set_title("(a) Printability screen" + (" with open databases (preliminary)" if prelim else ""), loc="left")
    save(fig, "fig2-calphad-screen")
    return f"drawn from {len(d)} rows" + (" (preliminary)" if prelim else "")


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
def fig5(p, tensile, hardness, bench, lit) -> str:
    fig, axs = plt.subplots(2, 2, figsize=(7.2, 5.4), gridspec_kw={"wspace": 0.32, "hspace": 0.62})
    axs = axs.ravel()
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
    placeholder(axs[1], "Fig5", p, "(b) stress-strain, same session") if camp.empty else style(axs[1])
    axs[1].set_title("(b) Stress-strain", loc="left")
    status.append("(b) placeholder" if camp.empty else "(b) needs raw curves (see SI S6)")

    # (c) yield strength of everything printed and tested in-house, mean and 95 % CI, one bar per
    # powder and condition. Baselines not yet measured show their vendor datasheet value as a hollow square.
    ax = axs[2]
    style(ax)
    groups = []  # (label, data, colour, datasheet values if not measured)
    ih = inhouse_alsi(tensile)
    for cls, d in (ih.groupby(ih["condition"].map(cond_class)) if not ih.empty else []):
        groups.append((f"AlSi10Mg\n{cls}", d, C_ALSI, None))
    for base in BASELINES:
        d = commercial_tensile(tensile, base)
        if d.empty:
            groups.append((f"{base}\naged", None, C_BASE, datasheet_ys(base, "aged", bench, lit)))
        else:
            for cls, dd in d.groupby(d["condition"].map(cond_class)):
                groups.append((f"{base}\n{cls}", dd, C_BASE, None))
    d = commercial_tensile(tensile, "Scalmalloy")
    for cls, dd in (d.groupby(d["condition"].map(cond_class)) if not d.empty else []):
        groups.append((f"Scalmalloy\n{cls}", dd, C_SCAL, None))
    for aid, dd in camp.groupby("alloy_id") if not camp.empty else []:
        groups.append((aid, dd, C_NEW, None))
    for i, (lab, d, col, ds) in enumerate(groups):
        if d is None:
            if ds:
                ax.scatter([i] * len(ds), ds, s=30, marker="s", facecolors="white", edgecolors=col, linewidths=1.0,
                           zorder=3)
                ax.text(i, min(ds) - 12, "datasheet;\nin-house due", ha="center", va="top", fontsize=5.8, color=INK2)
            continue
        m, s_, hw, n = mean_ci(d["ys_mpa"])
        ax.bar(i, m, width=0.6, color=col, edgecolor="white", linewidth=0.8)
        if not math.isnan(hw):
            ax.errorbar(i, m, yerr=hw, color=INK, capsize=2, linewidth=0.8)
        ax.text(i, 8, f"n = {n}", ha="center", fontsize=6.3, color="white")
    ax.set_xticks(range(len(groups)), [g[0] for g in groups], fontsize=6.3)
    ax.set_xlim(-0.6, len(groups) - 0.4)
    ax.set_ylabel("Yield strength (MPa)")
    ax.set_ylim(0, 450)
    if camp.empty:
        ax.text(0.98, 0.45, "finalists' tensile\ndue Feb 12", transform=ax.transAxes, ha="right", va="top",
                fontsize=6.3, color=INK2)
    ax.set_title("(c) Yield strength, printed and tested here", loc="left")
    status.append("(c) in-house AlSi10Mg drawn" + ("" if camp.empty else " with campaign alloys"))

    # (d) on par with the datasheets? In-house mean yield divided by the vendor's typical value for the same
    # condition (horizontal bars), with the 95 % CI. Proposed threshold for "on par": 0.90 (preregistration.md).
    ax = axs[3]
    style(ax)
    ax.axhline(1.0, color=INK2, linewidth=0.8)
    ax.axhline(0.9, color=INK2, linewidth=0.8, linestyle=(0, (3, 2)))
    ax.text(7.45, 0.905, "0.90: on par (proposed)", fontsize=6.0, color=INK2, va="bottom", ha="right")
    cats = [("AlSi10Mg", "as built", C_ALSI, ih), ("AlSi10Mg", "stress-relieved", C_ALSI, ih)]
    for base in BASELINES:
        d = commercial_tensile(tensile, base)
        cats += [(base, "as built", C_BASE, d), (base, "aged", C_BASE, d)]
    d = commercial_tensile(tensile, "Scalmalloy")
    cats += [("Scalmalloy", "as built", C_SCAL, d), ("Scalmalloy", "aged", C_SCAL, d)]
    drawn = 0
    for i, (base, cls, col, d) in enumerate(cats):
        ds = datasheet_ys(base, cls, bench, lit)
        dd = d[d["condition"].map(cond_class) == cls] if (d is not None and not d.empty) else pd.DataFrame()
        if dd.empty or not ds:
            ax.text(i, 0.62, "due" if ds else "no sheet", rotation=90, ha="center", va="bottom", fontsize=6.0,
                    color=INK2)
            continue
        m, _, hw, _ = mean_ci(dd["ys_mpa"])
        for j, v in enumerate(sorted(ds)):
            x = i + (j - (len(ds) - 1) / 2) * 0.18
            ax.errorbar(x, m / v, yerr=(hw / v if not math.isnan(hw) else None), fmt="o", ms=4.5, color=col,
                        mec="white", mew=0.6, elinewidth=0.8, capsize=1.5, zorder=3)
        drawn += 1
    short = {"as built": "AB", "stress-relieved": "SR", "aged": "aged"}
    ax.set_xticks(range(len(cats)), [short[c] for _, c, _, _ in cats], fontsize=6.0)
    # powder names once per pair, under the condition labels
    import matplotlib.transforms as mtransforms
    tr = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
    for i in range(0, len(cats), 2):
        ax.text(i + 0.5, -0.17, cats[i][0], transform=tr, ha="center", va="top", fontsize=6.3, color=INK)
    ax.set_xlim(-0.6, len(cats) - 0.4)
    ax.set_ylim(0.6, 1.2)
    ax.set_ylabel("In-house yield / datasheet yield")
    ax.set_title("(d) Against the vendors' datasheets", loc="left")
    status.append(f"(d) {drawn} of {len(cats)} powder-condition pairs drawn")
    save(fig, "fig5-mechanical")
    return "; ".join(status)


# ------------------------------------------------------------------ SI Fig. S1
def fig_s_burden(alloys, burdens, lit, lit_b) -> str:
    """Every alloy's import-weighted burden interval and the cost of its critical additions, side by side,
    so the reader can see that the two metrics rank the alloys differently."""
    rows = []
    for aid, r in burdens.iterrows():
        role = alloys.set_index("alloy_id").loc[aid, "role"] if aid in set(alloys["alloy_id"]) else ""
        name = alloys.set_index("alloy_id").loc[aid, "name"] if aid in set(alloys["alloy_id"]) else aid
        kind = ("benchmark" if role == "benchmark" else "baseline" if str(role).startswith("baseline")
                else "seed" if "seed" in str(role) else "campaign")
        rows.append((str(name), kind, r))
    if not lit_b.empty:
        names = lit.drop_duplicates("alloy_id").set_index("alloy_id")["name"]
        for aid, r in lit_b.iterrows():
            if aid in BASELINES.values():  # drawn once, as a baseline
                continue
            rows.append((str(names.get(aid, aid)), "comparator", r))
    rows = [x for x in rows if not math.isnan(float(x[2]["B_nir"]))]
    if not rows:
        return "no burden data"
    rows.sort(key=lambda x: x[2]["B_nir"])
    col = {"benchmark": None, "baseline": C_BASE, "seed": C_NEW, "comparator": GREY, "campaign": C_NEW}
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 0.22 * len(rows) + 1.0), sharey=True,
                               gridspec_kw={"wspace": 0.08, "width_ratios": [1.3, 1]})
    for i, (name, kind, r) in enumerate(rows):
        c = col[kind] or (C_ALSI if name.startswith("AlSi") else C_SCAL)
        a.hlines(i, r["B_nir_low"], r["B_nir_high"], color=c, linewidth=3.0)
        a.plot(r["B_nir"], i, "o", ms=3.5, color="white", mec=c, mew=1.0)
        cost = r["B_cost"] if not math.isnan(float(r["B_cost"])) else r.get("B_cost_priced", float("nan"))
        if not math.isnan(float(cost)):
            b.plot(cost, i, "o", ms=4.5, color=c, mec="white", mew=0.6)
    sc = burdens.loc["Scalmalloy"] if "Scalmalloy" in burdens.index else None
    if sc is not None:
        a.axvline(sc["B_nir_low"], color=C_SCAL, linewidth=0.8, linestyle=(0, (3, 2)))
        b.axvline(sc["B_cost"], color=C_SCAL, linewidth=0.8, linestyle=(0, (3, 2)))
    for ax in (a, b):
        style(ax)
    a.set_yticks(range(len(rows)), [x[0] for x in rows], fontsize=6.3)
    a.set_xlabel("$B_\\mathrm{NIR}$ (wt %, interval from USGS bounds)")
    b.set_xscale("log")
    b.set_xlabel("$B_\\mathrm{cost}$ (USD per kg of alloy, log scale)")
    a.set_title("(a) Import-weighted burden", loc="left")
    b.set_title("(b) Cost of critical additions", loc="left")
    a.text(0.99, 0.02, "dashed: Scalmalloy's lower bound (compare alloys at\nthe same reliances, not interval to interval)",
           transform=a.transAxes, ha="right", fontsize=6.0, color=INK2)
    b.text(0.97, 0.02, "dashed: Scalmalloy", transform=b.transAxes, ha="right", fontsize=6.0, color=INK2)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=C_ALSI, linewidth=3, label="AlSi10Mg"),
               Line2D([], [], color=C_SCAL, linewidth=3, label="Scalmalloy"),
               Line2D([], [], color=C_BASE, linewidth=3, label="Sc-free baseline"),
               Line2D([], [], color=C_NEW, linewidth=3, label="planned seed"),
               Line2D([], [], color=GREY, linewidth=3, label="Sc-free comparator")]
    a.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.0, 1.06), ncol=5, fontsize=6.3,
             handlelength=1.5, columnspacing=0.8)
    save(fig, "figS1-burden-sensitivity")
    return f"drawn for {len(rows)} alloys"


# ------------------------------------------------------------------------ tables
def tex_escape(s: str) -> str:
    return (str(s).replace("\\", "\\textbackslash{}").replace("&", "\\&").replace("%", "\\%")
            .replace("_", "\\_").replace("#", "\\#").replace("µ", "\\textmu{}").replace("°", "\\textdegree{}")
            .replace("$", "\\$").replace(">=", "$\\geq$").replace("<", "$<$").replace(">", "$>$")
            .replace("Hoganas", 'H\\"ogan\\"as'))


def fmt(v, nd=0):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "--"
    return "--" if math.isnan(v) else f"{v:.{nd}f}"


def table_benchmarks(bench, tensile, lit) -> None:
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
    # The Sc-free baselines' own datasheets (data/literature-alloys.csv).
    if not lit.empty:
        srcs = {"eos-al5x1": (r"EOS M 290, 40\,\textmu m~\cite{ds_al5x1}", "Al5X1"),
                "hoganas-al-hs1": (r"H\"ogan\"as~\cite{ds_hoganas}", "Al-HS1")}
        rows = lit[lit["alloy_id"].isin(list(srcs))]
        if not rows.empty:
            lines.append(r"\midrule")
        for _, r in rows.iterrows():
            src, name = srcs[r["alloy_id"]]
            cond = str(r["condition"]).replace(" (ASTM E8)", "")
            lines.append(f"{name} & {src} & {tex_escape(cond)} & {tex_escape(r['orientation'])} & "
                         f"{fmt(r['ys_mpa'])} & {fmt(r['uts_mpa'])} & {fmt(r['el_pct'], 1)} \\\\")
    measured = [("AlSi10Mg", ih)] + [(b, commercial_tensile(tensile, b)) for b in (*BASELINES, "Scalmalloy")]
    first = True
    for name, d in measured:
        if d.empty:
            continue
        for cls, g in d.groupby(d["condition"].map(cond_class)):
            ys, uts, el = mean_ci(g["ys_mpa"]), mean_ci(g["uts_mpa"]), mean_ci(g["el_pct"])
            if first:
                lines.append(r"\midrule")
                first = False
            site = "This lab, Utah MIDI" if name == "AlSi10Mg" and str(g["build_id"].iloc[0]).startswith("utah-midi-2026-04") \
                else "This lab"
            lines.append(rf"{name} & {site}, $n={ys[3]}$ & {cls}, as-printed surface & horizontal & "
                         rf"${ys[0]:.0f}\pm{ys[1]:.0f}$ & ${uts[0]:.0f}\pm{uts[1]:.0f}$ & ${el[0]:.1f}\pm{el[1]:.1f}$ \\")
    lines.append(r"\midrule")
    lines.append(r"\multicolumn{7}{@{}l}{\placeholder{In-house Al5X1, Al-HS1, Scalmalloy and AlSi10Mg re-test; campaign "
                 r"alloys and in-house AlSi10Mg-type (D1): data due Feb 12, 2027}} \\")
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


def table_literature(lit, lit_b, crit=None, scal=None) -> None:
    """SI table: scandium-free comparators with their burden (one row per alloy, best strength), and whether
    their B_NIR is below Scalmalloy's with both under the same import reliances."""
    if lit.empty:
        return
    lines = [r"\begin{tabular}{@{}llrrrrll@{}}", r"\toprule",
             r"Alloy & Condition (highest yield listed) & YS (MPa) & EL (\%) & $B_\mathrm{NIR}$ (wt\%) & "
             r"$B_\mathrm{cost}$ (USD\,kg$^{-1}$) & vs \Scal & Source \\", r"\midrule"]
    for aid, d in lit.groupby("alloy_id", sort=False):
        r = d.loc[d["ys_mpa"].idxmax()]
        bb = lit_b.loc[aid] if aid in lit_b.index else None
        v = verdict_vs_scal(mb.composition(r), {"Scalmalloy": scal}, crit) if (crit is not None and scal) else "--"
        lines.append(" & ".join([tex_escape(r["name"]), tex_escape(r["condition"]), fmt(r["ys_mpa"]),
                                 fmt(r["el_pct"], 1), interval(bb) if bb is not None else "--",
                                 fmt(bb["B_cost"], 2) if bb is not None else "--", v,
                                 rf"\cite{{{r['cite_key']}}}"]) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (GEN / "tab-literature.tex").write_text("\n".join(lines) + "\n")


def table_compositions(alloys, burdens, crit=None) -> None:
    els = ["si", "mg", "mn", "cr", "zr", "sc", "fe", "ni", "ti", "cu", "ce", "er", "zn"]
    num = lambda v: pd.to_numeric(pd.Series([v]), errors="coerce").fillna(0).iloc[0]
    present = [e for e in els if e in alloys.columns and pd.to_numeric(alloys[e], errors="coerce").fillna(0).gt(0).any()]
    comps = {r["alloy_id"]: mb.composition(r) for _, r in alloys.iterrows()}
    ncol = 1 + len(present) + 3
    lines = [rf"\begin{{tabular}}{{@{{}}l{'r' * len(present)}rlr@{{}}}}", r"\toprule"]
    head = ["Alloy"] + [e.capitalize() for e in present] + [r"$B_\mathrm{NIR}$", r"vs \Scal", r"$B_\mathrm{cost}$"]
    lines.append(" & ".join(head) + r" \\")
    unit = [""] + ([rf"\multicolumn{{{len(present)}}}{{c}}{{wt\%, nominal}}"] if present else []) + \
           [r"wt\%", "", r"USD\,kg$^{-1}$"]
    lines.append(" & ".join(unit) + r" \\")
    lines.append(r"\midrule")
    for _, r in alloys.iterrows():
        vals = [fmt(r.get(e), 2) if num(r.get(e)) > 0 else "--" for e in present]
        bb = burdens.loc[r["alloy_id"]] if (not burdens.empty and r["alloy_id"] in burdens.index) else None
        v = "--" if (r["alloy_id"] == "Scalmalloy" or crit is None) else verdict_vs_scal(comps[r["alloy_id"]], comps, crit)
        tail = ([interval(bb), v, fmt(bb["B_cost"], 2)] if bb is not None else ["--"] * 3)
        name = tex_escape(r["name"]) if pd.notna(r.get("name")) else tex_escape(r["alloy_id"])
        role = str(r.get("role", ""))
        if role.startswith("baseline"):
            name += " (baseline)"
        elif role not in ("benchmark", ""):
            name += rf" ({tex_escape(role)})"
        lines.append(" & ".join([name] + vals + tail) + r" \\")
    lines.append(r"\midrule")
    lines.append(rf"\multicolumn{{{ncol}}}{{@{{}}l}}{{\placeholder{{Campaign alloys and the baselines' lots with measured compositions: due Feb 19, 2027}}}} \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (GEN / "tab-compositions.tex").write_text("\n".join(lines) + "\n")


def signed(v: float, nd: int = 2) -> str:
    return f"${v:+.{nd}f}$".replace("+", "{+}") if not math.isnan(v) else "--"


def table_paired(alloys, burdens, crit) -> None:
    """SI table: every alloy in alloys.csv against Scalmalloy on B_NIR with both under the same import
    reliances, plus B_mass and B_cost."""
    comps = {r["alloy_id"]: mb.composition(r) for _, r in alloys.iterrows()}
    if "Scalmalloy" not in comps:
        return
    lines = [r"\begin{tabular}{@{}llllrr@{}}", r"\toprule",
             r"Alloy & $B_\mathrm{NIR}$ (wt\%) & $B_\mathrm{NIR} - B_\mathrm{NIR}^\mathrm{Scal}$, same reliances (wt\%) & "
             r"vs \Scal & $B_\mathrm{mass}$ (wt\%) & $B_\mathrm{cost}$ (USD\,kg$^{-1}$) \\", r"\midrule"]
    for _, r in alloys.iterrows():
        aid = r["alloy_id"]
        bb = burdens.loc[aid]
        if aid == "Scalmalloy":
            diff, v = "0", "--"
        else:
            lo, hi = mb.paired_difference(comps[aid], comps["Scalmalloy"], crit)
            diff = f"{signed(lo)} to {signed(hi)}"
            v = verdict_vs_scal(comps[aid], comps, crit)
        lines.append(" & ".join([tex_escape(r["name"]), interval(bb), diff, v, fmt(bb["B_mass"], 2),
                                 fmt(bb["B_cost"], 2)]) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (GEN / "tab-paired.tex").write_text("\n".join(lines) + "\n")


def numbers(tensile, runs, alloys, burdens, lit=None, lit_b=None, crit=None, bench=None) -> None:
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
    for aid, macro in (("AlSi10Mg", "BAlSi"), ("Scalmalloy", "BScal"), ("Al5X1", "BAlfive"), ("Al-HS1", "BAlhs"),
                       ("S1", "BSone"), ("S2", "BStwo"), ("S3", "BSthree"), ("S4", "BSfour"), ("O1", "BOone")):
        lines.append(num(macro + "mass", g(aid, "B_mass"), 1, "B"))
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
                  num("CostRedAgHi", math.floor(100 * (1 - agc.min() / sc_cost))),
                  num("CostRedAgMasterLo", math.floor(100 * (1 - agc.max() / sc_cost_master))),
                  num("CostRedAgMasterHi", math.floor(100 * (1 - agc.min() / sc_cost_master)))]
    # B_NIR against Scalmalloy with both alloys under the same import reliances (mineral_burden.paired_difference).
    comps = {r["alloy_id"]: mb.composition(r) for _, r in alloys.iterrows()} if not alloys.empty else {}
    if crit is not None and "Scalmalloy" in comps:
        for aid, macro in (("AlSi10Mg", "PAlSi"), ("Al5X1", "PAlfive"), ("Al-HS1", "PAlhs"), ("S1", "PSone"),
                           ("S2", "PStwo"), ("S3", "PSthree"), ("O1", "POone"), ("O3", "POthree")):
            lo, hi = mb.paired_difference(comps[aid], comps["Scalmalloy"], crit) if aid in comps else (np.nan, np.nan)
            lines.append(rf"\newcommand{{\{macro}lo}}{{{signed(lo)}}}")
            lines.append(rf"\newcommand{{\{macro}hi}}{{{signed(hi)}}}")
        lo, hi = mb.paired_difference(comps["Al-HS1"], comps["Al5X1"], crit) if {"Al-HS1", "Al5X1"} <= set(comps) else (np.nan, np.nan)
        lines += [rf"\newcommand{{\PHSvsfivelo}}{{{signed(lo)}}}", rf"\newcommand{{\PHSvsfivehi}}{{{signed(hi)}}}"]
        lo, hi = mb.paired_difference(comps["O1"], comps["Al5X1"], crit) if {"O1", "Al5X1"} <= set(comps) else (np.nan, np.nan)
        lines += [rf"\newcommand{{\POonevsfivelo}}{{{signed(lo)}}}", rf"\newcommand{{\POonevsfivehi}}{{{signed(hi)}}}"]
        seeds = [a for a in alloys.loc[alloys["role"].astype(str).str.contains("seed"), "alloy_id"]]
        groups = {"below": [], "depends": [], "above": []}
        for a_ in seeds:
            v = verdict_vs_scal(comps[a_], comps, crit)
            if v in groups:
                groups[v].append(a_)
        for k, macro in (("below", "SeedsBelow"), ("depends", "SeedsDepends"), ("above", "SeedsAbove")):
            lines.append(rf"\newcommand{{\{macro}}}{{{', '.join(groups[k]) if groups[k] else 'none'}}}")
            lines.append(num("N" + macro, len(groups[k])))
    # In-house AlSi10Mg against the horizontal as-built datasheet rows (on-par check, Fig. 5d).
    if bench is not None and not bench.empty and ys[3]:
        ds = datasheet_ys("AlSi10Mg", "as built", bench, lit if lit is not None else pd.DataFrame())
        if ds:
            lines += [num("InhouseRatioLo", ys[0] / max(ds), 2), num("InhouseRatioHi", ys[0] / min(ds), 2)]
    # Sc-free comparators already in the region of interest: stronger than in-house AlSi10Mg by more than
    # its 95 % CI half-width, and below Scalmalloy's lowest B_NIR (midpoint, and robustly at the high end).
    if lit is not None and not lit.empty and lit_b is not None and not lit_b.empty and ys[3]:
        sc_mid = g("Scalmalloy", "B_nir")
        best = lit.groupby("alloy_id")["ys_mpa"].max()
        lit_comp = {a: mb.composition(r) for a, r in lit.drop_duplicates("alloy_id").set_index("alloy_id").iterrows()}
        robust = {a: (crit is not None and "Scalmalloy" in comps and mb.robustly_below(lit_comp[a], comps["Scalmalloy"], crit))
                  for a in best.index}
        thr = ys[0] + ys[2]
        onmap = [a for a in best.index if not math.isnan(lit_b.loc[a, "B_nir"])]
        mid = [a for a in onmap if best[a] > thr and lit_b.loc[a, "B_nir"] < sc_mid]
        rob = [a for a in onmap if best[a] > thr and robust[a]]
        ds_bar = 300.0  # strongest machined as-built AlSi10Mg datasheet row (Nikon, horizontal)
        mid_ds = [a for a in onmap if best[a] > ds_bar and lit_b.loc[a, "B_nir"] < sc_mid]
        rob_ds = [a for a in onmap if best[a] > ds_bar and robust[a]]
        lines += [num("NLit", len(onmap)), num("NLitRegionMid", len(mid)), num("NLitRegionRobust", len(rob)),
                  num("NLitRegionMidDS", len(mid_ds)), num("NLitRegionRobustDS", len(rob_ds)), num("YSbar", thr)]
        # The Sc-free front on reported values, and the part of it inside the region of interest.
        front = front_points(lit_best(lit, lit_b))
        inreg = front[(front["b"] < sc_mid) & (front["ys"] > thr)]
        short = {"aheadd-cp1": "Al--Fe--Zr (Aheadd CP1)", "al-fe-mg-zr": "Al--Fe--Mg--Zr", "eos-al5x1": "Al5X1",
                 "eos-al2139": "Al2139 (T4)", "hoganas-al-hs1": "Al-HS1", "croteau-al-mg-zr": "Al--Mg--Zr",
                 "chalmers-alloy-f": "Al--Mn--Cr--Zr--Mg", "hrl-7a77": "7A77", "alsimg-tailored": "tailored Al--Si--Mg",
                 "al-mg-mn-er-zr": "Al--Mg--Mn--Er--Zr", "eckart-a20x": "A20X"}
        hv = mb.hypervolume([(i, r["b"], r["ys"]) for i, r in front.iterrows()], sc_mid, thr)
        lines += [num("HVreported", hv), num("NFront", len(front)), num("NFrontRegion", len(inreg)),
                  rf"\newcommand{{\FrontRegionList}}{{{', '.join(short.get(a, a) for a in inreg.index)}}}",
                  rf"\newcommand{{\FrontList}}{{{', '.join(short.get(a, a) for a in front.index)}}}"]
        on_front = {k: (lid in front.index) for k, lid in BASELINES.items()}
        lines += [rf"\newcommand{{\AlfiveOnFront}}{{{'on' if on_front['Al5X1'] else 'behind'}}}",
                  rf"\newcommand{{\AlhsOnFront}}{{{'on' if on_front['Al-HS1'] else 'behind'}}}"]
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
        "Fig2": fig2(p, read("calphad_screen.csv"), crit),
        "Fig3": generic("Fig3", p, read("powder.csv"), "fig3-powders", draw_powder),
        "Fig4": generic("Fig4", p, read("density.csv"), "fig4-printability", draw_density),
        "Fig5": fig5(p, tensile, read("hardness.csv"), bench, lit),
        "Fig6": generic("Fig6", p, read("corrosion.csv"), "fig6-corrosion", draw_corrosion),
    }
    table_benchmarks(bench, tensile, lit)
    if not alloys.empty:
        table_compositions(alloys, burdens, crit)
        table_paired(alloys, burdens, crit)
    scal = (mb.composition(alloys.set_index("alloy_id").loc["Scalmalloy"])
            if not alloys.empty and "Scalmalloy" in set(alloys["alloy_id"]) else None)
    table_literature(lit, lit_b, crit, scal)
    table_elements()
    status["S3"] = "Inputs sourced; Fig. S1 " + fig_s_burden(alloys, burdens, lit, lit_b)
    numbers(tensile, runs, alloys, burdens, lit, lit_b, crit, bench)
    status_md(p, status)
    for k, v in status.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
