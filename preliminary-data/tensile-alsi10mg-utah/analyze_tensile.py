"""Tensile properties of the as-built LPBF AlSi10Mg coupons printed at the University of Utah.

Reads the unmodified MTS TestSuite exports in raw/, the measured cross-sections in
specimen-dimensions.csv and the vendor values in datasheet-values.csv. Writes
results.csv, stress-strain.png and datasheet-comparison.png next to this file.

    python analyze_tensile.py

Method (details and caveats in README.md):
- stress = force / measured cross-section (engineering stress, MPa)
- strain = the MTS channel "Axial AI1_AOX" (%), as in the student's script (raw/)
- elastic slope fitted between 10 % and 35 % of UTS on the loading branch; the strain
  origin is moved to where that line crosses zero stress (toe compensation), which also
  removes the compressive preload the grips put on the coupon
- yield = 0.2 % offset (Rp0.2) from that slope; UTS = max force / area
- fracture = last sample with force >= 90 % of max; total extension at fracture At is the
  strain there, and elongation after fracture A = At - stress_at_fracture / slope
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
FIT_WINDOW = (0.10, 0.35)  # fraction of UTS used for the elastic fit
OFFSET_PCT = 0.2  # offset for Rp0.2, in % strain
FRACTURE_FRACTION = 0.90  # last sample with F >= 0.9 Fmax is the fracture point
SMOOTH = 11  # samples (about 0.1 s at 100 Hz), centred rolling mean for the yield crossing

# Colours: reference categorical slots 1-3 (validated adjacent and all-pairs) plus text inks.
BLUE, ORANGE, AQUA = "#257de0", "#f47230", "#00b894"
INK, INK2, GRID = "#191919", "#666666", "#e6e6e6"


def read_mts(path):
    """MTS TestSuite CSV: 6 header lines, column names, units, then data."""
    df = pd.read_csv(path, skiprows=[0, 1, 2, 3, 4, 5, 7], encoding="utf-8-sig")
    df.columns = ["time_s", "displacement_mm", "force_N", "strain_pct"]
    return df


def analyse(df, area_mm2):
    stress = df["force_N"].to_numpy() / area_mm2
    strain = df["strain_pct"].to_numpy()
    idx = np.arange(len(stress))
    imax = int(np.argmax(stress))
    uts = float(stress[imax])

    lo, hi = FIT_WINDOW
    fit = (stress >= lo * uts) & (stress <= hi * uts) & (idx < imax)
    slope, intercept = np.polyfit(strain[fit], stress[fit], 1)  # MPa per % strain
    e0 = -intercept / slope
    eps = strain - e0  # toe-compensated strain, %

    s_s = pd.Series(stress).rolling(SMOOTH, center=True, min_periods=1).mean().to_numpy()
    e_s = pd.Series(eps).rolling(SMOOTH, center=True, min_periods=1).mean().to_numpy()
    gap = s_s - slope * (e_s - OFFSET_PCT)  # > 0 while the curve is above the offset line
    start = int(idx[fit].max())
    below = np.nonzero(gap[start : imax + 1] <= 0)[0]
    if below.size == 0:
        raise ValueError("curve never crosses the 0.2 % offset line before UTS")
    j = start + int(below[0])
    w = gap[j - 1] / (gap[j - 1] - gap[j])
    ys = float(s_s[j - 1] + w * (s_s[j] - s_s[j - 1]))
    eps_ys = float(e_s[j - 1] + w * (e_s[j] - e_s[j - 1]))

    i_f = int(np.nonzero(stress >= FRACTURE_FRACTION * uts)[0].max())
    at = float(eps[i_f])
    a = at - float(stress[i_f]) / slope

    load = stress > 0.2 * uts
    rate = np.polyfit(df["time_s"].to_numpy()[load & (idx < imax)],
                      df["displacement_mm"].to_numpy()[load & (idx < imax)], 1)[0]
    return {
        "preload_MPa": float(stress[0]),
        "crosshead_mm_per_s": float(rate),
        "fit_slope_GPa": float(slope) * 100 / 1000,
        "yield_Rp02_MPa": ys,
        "uts_MPa": uts,
        "strain_at_uts_pct": float(eps[imax]),
        "total_ext_at_fracture_At_pct": at,
        "elongation_after_fracture_A_pct": a,
        "_eps": eps,
        "_stress": stress,
        "_i_f": i_f,
        "_eps_ys": eps_ys,
        "_imax": imax,
    }


def stress_strain_figure(res, dims, out):
    fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=150)
    order = [1, 2, 3, 4, 5]  # draw the highlighted test last
    label_y = {}
    for t in order:
        r = res[t]
        eps, s, i_f = r["_eps"], r["_stress"], r["_i_f"]
        first = int(np.nonzero(s >= 0)[0][0])  # drop the compressive clamping preload
        x, y = eps[first : i_f + 1], s[first : i_f + 1]
        if t == 5:
            ax.plot(x, y, color=BLUE, lw=2.0, zorder=5)
        elif t == 4:
            ax.plot(x, y, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=3)
        else:
            ax.plot(x, y, color="#9c9c9c", lw=1.2, zorder=3)
        ax.plot(r["_eps_ys"], r["yield_Rp02_MPa"], "o", ms=5, color=BLUE if t == 5 else INK2,
                mec="white", mew=1.0, zorder=6)
        ax.plot(eps[r["_imax"]], r["uts_MPa"], "D", ms=5, color=BLUE if t == 5 else INK2,
                mec="white", mew=1.0, zorder=6)
        label_y[t] = (x[-1], y[-1])
    # direct labels in a column right of the curves, ordered by fracture stress, with leaders
    x_lab, y_top, step = 6.05, 398, 14
    for k, t in enumerate(sorted(label_y, key=lambda k: -label_y[k][1])):
        xe, ye = label_y[t]
        yl = y_top - k * step
        ax.plot([xe + 0.04, x_lab - 0.06], [ye, yl], color="#c8c8c8", lw=0.7, zorder=2)
        txt = f"Test {t}" + (" (grip break)" if t == 4 else "")
        ax.text(x_lab, yl, txt, fontsize=8, va="center", color=INK if t == 5 else INK2,
                fontweight="bold" if t == 5 else "normal")
    ax.set_xlim(0, 7.6)
    ax.set_ylim(0, 430)
    ax.set_xlabel("Engineering strain (%)", color=INK)
    ax.set_ylabel("Engineering stress (MPa)", color=INK)
    ax.set_title("As-built LPBF AlSi10Mg, University of Utah Aconity MIDI, room temperature",
                 fontsize=9.5, color=INK, loc="left")
    ax.grid(color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("#9c9c9c")
    ax.tick_params(colors=INK2)
    from matplotlib.lines import Line2D
    handles = [
        Line2D([], [], color=BLUE, lw=2, label="Test 5: 0.001 in/s, lower clamp force"),
        Line2D([], [], color="#9c9c9c", lw=1.2, label="Tests 1-3: 0.005 in/s"),
        Line2D([], [], color=INK2, lw=1.2, ls=(0, (4, 3)), label="Test 4: 0.001 in/s, broke in grip"),
        Line2D([], [], color=INK2, marker="o", ls="", ms=5, label="0.2 % offset yield"),
        Line2D([], [], color=INK2, marker="D", ls="", ms=5, label="UTS"),
    ]
    ax.legend(handles=handles, loc="lower right", fontsize=7.5, frameon=False)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def comparison_figure(res, ds, out):
    rows = [("This work: Utah, near-net-shape, horizontal (n = 4)", None, BLUE)]
    for _, d in ds.iterrows():
        src = "EOS M 290" if d["source"] == "EOS" else "Nikon SLM 280"
        surf = "machined" if d["specimen_surface"].startswith("machined") else "near-net-shape"
        rows.append((f"{src}: {surf}, {d['orientation']}", d, ORANGE if d["source"] == "EOS" else AQUA))
    metrics = [("yield_Rp02_MPa", "yield_MPa", "yield_min_MPa", "0.2 % yield (MPa)", (180, 330)),
               ("uts_MPa", "uts_MPa", "uts_min_MPa", "UTS (MPa)", (330, 490)),
               ("elongation_after_fracture_A_pct", "elongation_pct", "elongation_min_pct",
                "Elongation after fracture (%)", (0, 12))]
    valid = [1, 2, 3, 5]
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.4), dpi=150, sharey=True)
    ypos = np.arange(len(rows))[::-1]
    for ax, (key, dkey, dmin, title, lim) in zip(axs, metrics):
        for y, (name, d, col) in zip(ypos, rows):
            if d is None:
                vals = [res[t][key] for t in valid]
                ax.plot(vals, [y] * len(vals), "o", ms=6, mfc="white", mec=col, mew=1.4, zorder=4)
                ax.plot(res[5][key], y, "o", ms=6.5, color=col, mec="white", mew=1.0, zorder=5)
                ax.plot([np.mean(vals)] * 2, [y - 0.28, y + 0.28], color=col, lw=2, zorder=3)
            else:
                if pd.notna(d[dmin]):
                    ax.plot([d[dmin], d[dkey]], [y, y], color=col, lw=2, solid_capstyle="round", zorder=3)
                    ax.plot(d[dmin], y, "|", ms=9, color=col, mew=2, zorder=4)
                ax.plot(d[dkey], y, "s", ms=6.5, color=col, mec="white", mew=1.0, zorder=5)
        ax.set_xlim(*lim)
        ax.set_title(title, fontsize=9, color=INK, loc="left")
        ax.grid(axis="x", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color("#9c9c9c")
        ax.tick_params(colors=INK2, labelsize=8, left=False)
    axs[0].set_yticks(ypos)
    axs[0].set_yticklabels([r[0] for r in rows], fontsize=8, color=INK)
    fig.text(0.01, 0.015,
             "This work: open circles = tests 1, 2, 3, 5; filled = test 5; bar = mean (test 4, a grip break, excluded). "
             "Datasheets: square = mean; Nikon line runs to its 95/95 minimum. All as-built (no heat treatment).",
             fontsize=7, color=INK2)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(out)
    plt.close(fig)


def main():
    dims = pd.read_csv(HERE / "specimen-dimensions.csv")
    ds = pd.read_csv(HERE / "datasheet-values.csv")
    res, table = {}, []
    for _, d in dims.iterrows():
        r = analyse(read_mts(HERE / d["csv"]), d["area_mm2"])
        res[int(d["test"])] = r
        table.append({"test": int(d["test"]), "csv": d["csv"], "area_mm2": d["area_mm2"],
                      "fracture_location": d["fracture_location"],
                      **{k: round(v, 3) if "pct" in k or "GPa" in k or "mm_per_s" in k else round(v, 1)
                         for k, v in r.items() if not k.startswith("_")}})
    out = pd.DataFrame(table)
    out.to_csv(HERE / "results.csv", index=False)
    valid = out[out["test"] != 4]
    cols = ["yield_Rp02_MPa", "uts_MPa", "elongation_after_fracture_A_pct", "total_ext_at_fracture_At_pct",
            "fit_slope_GPa"]
    print(out.drop(columns=["csv"]).to_string(index=False))
    print("\nmean (sd), tests 1, 2, 3, 5:")
    for c in cols:
        print(f"  {c}: {valid[c].mean():.1f} ({valid[c].std(ddof=1):.1f})")
    stress_strain_figure(res, dims, HERE / "stress-strain.png")
    comparison_figure(res, ds, HERE / "datasheet-comparison.png")


if __name__ == "__main__":
    main()
