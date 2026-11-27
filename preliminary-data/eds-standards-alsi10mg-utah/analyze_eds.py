"""Tabulate and plot the standards-based EDS of the polished Utah AlSi10Mg coupon.

Inputs (all in this folder):
  raw/unknowns/*.msa, raw/standards/*.msa   spectra as posted in vertical-cloud-lab/caliber
  dtsa2-results.csv                         DTSA-II results, transcribed from the reports
  dtsa2-rerun/broadened.csv                 the DTSA-II re-run (dtsa2-rerun/run.sh) with the
                                            0.96 us runs fitted against broadened standards

Outputs:
  results.csv                one row per run: acquisition settings read from the .msa headers,
                             DTSA-II's numbers, the composition renormalized without O, and
                             what (if anything) is wrong with the run
  composition-by-run.png     Mg and Si for every run, against the AlSi10Mg specification

It also prints the amp-time check described in README.md.

Run:  python analyze_eds.py   (needs numpy and matplotlib)
"""
import csv
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
E = np.arange(4096) * 0.005  # keV; every file is 4096 channels x 5 eV, zero offset

# Dead time of each standard, read off the EDAX display while it was collected
# (caliber#12, comments 6803490926 for MgO and Si, 6865364302 for Al). Percent.
STD_DEAD_TIME = {  # kV: (MgO, Si, Al)
    5: (32, 25, 29),
    10: (60, 63, 67),
    15: (79, 90, 91.5),
    20: (81, 95, 96),
    25: (86, 98.7, 98.9),
}
SPEC = {"Mg": (0.20, 0.45), "Si": (9.0, 11.0)}  # wt %, EN AC-43000 / ASTM F3318
STANDARDLESS_FEEDSTOCK = {"Mg": 1.4, "Si": 7.9}  # ../sem-eds-feedstock/, normalized to metals


def read_msa(path):
    """Return (header dict, counts array) for an EMSA/MAS file."""
    hdr, counts = {}, []
    in_data = False
    for line in Path(path).read_text(encoding="latin-1").splitlines():
        if line.startswith("#SPECTRUM"):
            in_data = True
            continue
        if line.startswith("#ENDOFDATA"):
            break
        if in_data:
            counts += [float(t) for t in re.split(r"[,\s]+", line.strip()) if t]
        elif line.startswith("#"):
            key, _, val = line.lstrip("#").partition(":")
            hdr[key.split()[0].upper()] = val.strip()
    y = np.array(counts)
    if y.size == 2 * 4096:  # XY pairs
        y = y[1::2]
    return hdr, y


def num(hdr, key):
    try:
        return float(hdr[key])
    except (KeyError, ValueError):
        return None


def fwhm_ev(y, lo=1.40, hi=1.60):
    """FWHM of the strongest peak in [lo, hi) keV (Al Ka), interpolated at half height."""
    m = (E >= lo) & (E < hi)
    x, yy = E[m], y[m].astype(float)
    half = yy.max() / 2
    above = np.where(yy >= half)[0]
    i0, i1 = above[0], above[-1]
    left = np.interp(half, [yy[i0 - 1], yy[i0]], [x[i0 - 1], x[i0]])
    right = np.interp(half, [yy[i1 + 1], yy[i1]], [x[i1 + 1], x[i1]])
    return 1000 * (right - left)


def spectrum_info(path):
    hdr, y = read_msa(path)
    lt = num(hdr, "LIVETIME")
    return {
        "date": hdr.get("DATE", ""),
        "time": hdr.get("TIME", ""),
        "beam_kV": num(hdr, "BEAMKV"),
        "probe_current_nA": num(hdr, "PROBECUR"),
        "live_time_s": lt,
        "total_counts": int(y.sum()),
        "counts_per_live_s": round(y.sum() / lt) if lt else None,
        "amp_time_us": num(hdr, "AMPTIME"),
        "al_ka_fwhm_eV": round(fwhm_ev(y), 1),
    }


# --- amp-time check: does broader peaks in the unknown alone change the fitted Mg? -------------
ROIS = {"O": (0.424, 0.626), "Mg": (1.128, 1.380), "Al": (1.354, 1.658), "Si": (1.600, 1.945)}


def tophat(y, width_ev=75.0):
    """Zero-sum top-hat filter, as in the filter fit DTSA-II uses."""
    w = int(round(width_ev / 5.0))
    s = max(1, w // 2)
    kernel = np.r_[-np.ones(s) / (2 * s), np.ones(w) / w, -np.ones(s) / (2 * s)]
    return np.convolve(y, kernel, mode="same")


def filter_fit_ratios(unknown, refs):
    """Weighted least squares of the filtered unknown on the filtered standards, each standard
    used only inside its ROI. Returns fitted Mg/Al and Si/Al intensity ratios (arbitrary scale,
    for comparing spectra with each other only)."""
    cols, mask = [], np.zeros_like(E, dtype=bool)
    for el, y in refs.items():
        r = (E >= ROIS[el][0]) & (E <= ROIS[el][1])
        cols.append(tophat(y) * r)
        mask |= r
    a = np.array(cols).T
    w = 1 / np.sqrt(np.maximum(unknown, 1))
    coef, *_ = np.linalg.lstsq(a[mask] * w[mask, None], tophat(unknown)[mask] * w[mask], rcond=None)
    k = dict(zip(refs, coef))
    return k["Mg"] / k["Al"], k["Si"] / k["Al"]


def broaden(y, target_ev, current_ev):
    sigma_ch = np.sqrt(target_ev**2 - current_ev**2) / 2.3548 / 5.0
    x = np.arange(-30, 31)
    g = np.exp(-0.5 * (x / sigma_ch) ** 2)
    return np.convolve(y, g / g.sum(), mode="same")


def amp_time_check():
    std = {el: read_msa(HERE / f"raw/standards/{f}_5kV.msa")[1].astype(float)
           for el, f in (("O", "MgO"), ("Mg", "MgO"), ("Al", "Al"), ("Si", "Si"))}
    s1 = read_msa(HERE / "raw/unknowns/sobol_exp_1_1.msa")[1].astype(float)
    rows = [("sobol_exp_1_1, as measured (7.68 us)", s1),
            ("sobol_exp_1_1, broadened to 90 eV", broaden(s1, 90.0, fwhm_ev(s1)))]
    for t in ("trial8_1", "trial10_1", "trial12_1", "trial13_1"):
        rows.append((f"{t} (0.96 us)", read_msa(HERE / f"raw/unknowns/{t}.msa")[1].astype(float)))
    base = filter_fit_ratios(s1, std)[0]
    print("\nAmp-time check, 5 kV, top-hat filter fit against the 5 kV standards (7.68 us):")
    print(f"  {'spectrum':40s} {'Al Ka FWHM':>10s} {'Mg/Al (vs 11-06 run)':>21s}")
    for name, y in rows:
        mg_al, _ = filter_fit_ratios(y, std)
        print(f"  {name:40s} {fwhm_ev(y):8.1f} eV {mg_al / base:21.2f}")


# --- main ------------------------------------------------------------------------------------
def classify(row):
    problems = []
    if row["amp_time_us"] != 7.68:
        problems.append(f"amp time {row['amp_time_us']:g} us; the standards used 7.68 us")
    kv = int(row["beam_kV"])
    if max(STD_DEAD_TIME[kv]) > 35:
        lo, hi = min(STD_DEAD_TIME[kv]), max(STD_DEAD_TIME[kv])
        problems.append(f"{kv} kV standards collected at {lo:g}-{hi:g} % dead time")
    if row["mg_standard_entered_as"] != "MgO":
        problems.append("MgO standard entered as pure Mg")
    if not 0.95 <= float(row["analytical_sum"]) <= 1.05:
        problems.append(f"analytical total {float(row['analytical_sum']):.3f}")
    return problems


def main():
    with open(HERE / "dtsa2-results.csv", newline="") as f:
        dtsa = list(csv.DictReader(f))
    out = []
    for d in dtsa:
        info = spectrum_info(HERE / "raw/unknowns" / f"{d['run']}.msa")
        assert info["beam_kV"] == float(d["beam_kV"]), d["run"]
        row = {"run": d["run"], **info, "mg_standard_entered_as": d["mg_standard_entered_as"],
               "std_dead_time_pct_MgO_Si_Al": "/".join(f"{v:g}" for v in STD_DEAD_TIME[int(d["beam_kV"])]),
               "analytical_sum": d["analytical_sum"]}
        for el in ("O", "Mg", "Al", "Si"):
            row[f"{el}_wt_norm"] = d[f"{el}_wt"]
            row[f"{el}_sd"] = d[f"{el}_sd"]
        metals = sum(float(d[f"{el}_wt"]) for el in ("Mg", "Al", "Si"))
        for el in ("Mg", "Al", "Si"):
            row[f"{el}_wt_metals"] = round(100 * float(d[f"{el}_wt"]) / metals, 2)
        problems = classify(row)
        row["usable"] = "yes" if not problems else "no"
        row["problems"] = "; ".join(problems)
        out.append(row)
    with open(HERE / "results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for r in out:
        print(f"{r['run']:14s} {r['beam_kV']:4.0f} kV {r['amp_time_us']:5.2f} us  FWHM {r['al_ka_fwhm_eV']:5.1f}  "
              f"Sum {float(r['analytical_sum']):.3f}  Mg {r['Mg_wt_metals']:5.2f}  Si {r['Si_wt_metals']:5.2f}  "
              f"{r['usable']:3s} {r['problems']}")
    plot(out)
    amp_time_check()


def refit_metals():
    """Mg and Si renormalized without O, from the DTSA-II re-run with broadened standards,
    for the 0.96 us runs at 5 kV."""
    out = {}
    with open(HERE / "dtsa2-rerun/broadened.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["amp_time_us"] == "0.96" and r["beam_kV"] == "5":
                metals = sum(float(r[f"{el}_wt_norm"]) for el in ("Mg", "Al", "Si"))
                out[r["run"]] = {el: 100 * float(r[f"{el}_wt_norm"]) / metals for el in ("Mg", "Si")}
    return out


def plot(rows):
    ink, ink2, grid = "#191919", "#666666", "#e6e6e6"
    refit = refit_metals()
    groups = [  # (label, colour, marker, x offset, test)
        ("Matched settings, analytical total 1.03 (11-06)", "#257de0", "o", -0.6,
         lambda r: r["usable"] == "yes"),
        ("Unknown at 0.96 µs amp time, standards at 7.68 µs (11-18)", "#f47230", "s", 0.6,
         lambda r: r["amp_time_us"] != 7.68),
        ("10-25 kV standards at 60-99 % dead time (11-06, 11-11, 11-20)", "#00b894", "^", -0.6,
         lambda r: r["usable"] == "no" and r["amp_time_us"] == 7.68),
    ]
    fig, axes = plt.subplots(2, 1, figsize=(8.6, 7.4), sharex=True)
    for ax, el in zip(axes, ("Mg", "Si")):
        lo, hi = SPEC[el]
        ax.axhspan(lo, hi, color="#d9d9d9", alpha=0.6, lw=0, zorder=0)
        ax.text(26.9, (lo + hi) / 2, "AlSi10Mg\nspec", va="center", ha="left", fontsize=8.5, color=ink2)
        ref = STANDARDLESS_FEEDSTOCK[el]
        ax.axhline(ref, color=ink2, lw=1.2, ls=(0, (4, 3)), zorder=1)
        ax.text(26.9, ref, "standardless,\nfeedstock\npowder", va="center", ha="left", fontsize=8.5, color=ink2)
        xpos = {}
        for label, colour, marker, dx, test in groups:
            sel = [r for r in rows if test(r)]
            xs, ys = [], []
            for kv in sorted({r["beam_kV"] for r in sel}):
                at = [r for r in sel if r["beam_kV"] == kv]
                jit = np.linspace(-0.4, 0.4, len(at)) if len(at) > 1 else [0.0]
                for j, r in zip(jit, at):
                    xs.append(kv + dx + j)
                    ys.append(r[f"{el}_wt_metals"])
                    xpos[r["run"]] = (kv + dx + j, r[f"{el}_wt_metals"])
            ax.plot(xs, ys, ls="none", marker=marker, ms=8.5, mfc=colour, mec="white", mew=1.0,
                    label=label if el == "Mg" else None, zorder=3)
        # The same 11-18 runs at 5 kV, re-fitted in DTSA-II against standards broadened to
        # their resolution (dtsa2-rerun/). The 5 kV standards are the sound ones.
        xs, ys = [], []
        for run, (x, y0) in xpos.items():
            if run in refit:
                y1 = refit[run][el]
                ax.plot([x, x], [y0, y1], color="#f47230", lw=1.0, alpha=0.7, zorder=2)
                xs.append(x)
                ys.append(y1)
        ax.plot(xs, ys, ls="none", marker="s", ms=8.5, mfc="white", mec="#f47230", mew=1.6, zorder=3,
                label="Same 11-18 runs at 5 kV, re-fitted against standards broadened to match"
                if el == "Mg" else None)
        ax.set_ylabel(f"{el} (wt %, Al + Si + Mg = 100)", color=ink)
        ax.grid(axis="y", color=grid, lw=0.8)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color("#b3b3b3")
        ax.tick_params(colors=ink2)
    axes[0].set_ylim(-0.05, 1.6)
    axes[1].set_ylim(6.5, 15.5)
    s1 = next(r for r in rows if r["run"] == "sobol_exp_1_1")
    axes[0].annotate(f"{s1['Mg_wt_metals']:.2f}", (5 - 0.6, s1["Mg_wt_metals"]), xytext=(0, 9),
                     textcoords="offset points", fontsize=9, color=ink, ha="center", va="bottom")
    axes[1].annotate(f"{s1['Si_wt_metals']:.1f}", (5 - 0.6, s1["Si_wt_metals"]), xytext=(0, 9),
                     textcoords="offset points", fontsize=9, color=ink, ha="center", va="bottom")
    for r in rows:
        if r["mg_standard_entered_as"] != "MgO":
            axes[0].annotate("MgO entered\nas pure Mg", (r["beam_kV"] + 0.6, r["Mg_wt_metals"]),
                             xytext=(-10, 0), textcoords="offset points", fontsize=8, color=ink2,
                             va="center", ha="right")
    axes[1].set_xticks([5, 10, 15, 20, 25])
    axes[1].set_xlim(2.5, 26.6)
    axes[1].set_xlabel("Beam energy (kV)", color=ink)
    axes[0].legend(loc="lower left", bbox_to_anchor=(-0.01, 1.0), frameon=False, fontsize=9, labelcolor=ink)
    fig.suptitle("Standards-based EDS (NIST DTSA-II) of a polished, as-built Utah AlSi10Mg coupon: 17 runs",
                 x=0.02, ha="left", fontsize=11.5, color=ink, y=0.995)
    fig.tight_layout(rect=(0, 0, 0.9, 0.97))
    fig.savefig(HERE / "composition-by-run.png", dpi=160)


if __name__ == "__main__":
    main()
