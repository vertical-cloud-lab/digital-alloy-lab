"""Figures for the DEM spreading runs (issue #260): summary chart, top views (height maps), side views and a GIF.

Re-run after dem_spread.py has produced /tmp/powder/<case>/ and analysis/out/powder/<case>.json:
    /tmp/venv/bin/python desktop-lpbf/analysis/powder/dem_figures.py
Writes PNG/GIF files to desktop-lpbf/analysis/out/powder/.
"""
import glob
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import EllipseCollection
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dem_spread as D  # noqa: E402

OUT = D.OUT
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]          # validated default categorical order
BLUES = LinearSegmentedColormap.from_list("blue_ramp", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
EMPTY = "#d9d8d4"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF})


def load(case):
    return json.load(open(os.path.join(OUT, f"{case}.json")))


def summary():
    rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(OUT, "g*.json")))]
    base = [r for r in rows if abs(r["E_sim_MPa"] - D.E_SIM / 1e6) < 1e-9]
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
    keys = [("low", 50), ("low", 150), ("high", 50), ("high", 150)]
    metrics = [("packing_fraction", "packing fraction in the gap"), ("coverage", "plate area covered"),
               ("empty_patch_fraction_D50", "area in holes ≥ D50")]
    for ax, (m, lab) in zip(axs, metrics):
        for (coh, v), c in zip(keys, SERIES):
            pts = sorted([(r["gap_um"], r[m]) for r in base if r["cohesion"] == coh and r["v_mms"] == v])
            if not pts:
                continue
            x, y = zip(*pts)
            ax.plot(x, y, "-o", color=c, lw=2, ms=6, mec=SURF, mew=1.5,
                    label=f"Γ {D.GAMMA[coh]*1e3:g} mJ/m², {v} mm/s")
        stiff = [r for r in rows if r["E_sim_MPa"] > D.E_SIM / 1e6 * 1.5]
        for r in stiff:
            ax.plot(r["gap_um"], r[m], "o", mfc=SURF, mec=SERIES[1], mew=1.5, ms=7,
                    label=f"same, E ×{r['E_sim_MPa'] / (D.E_SIM / 1e6):.0f}" if ax is axs[0] else None)
        ax.set_xlabel("blade gap above the substrate mid-plane (µm)")
        ax.set_title(lab, color=INK, loc="left")
        ax.grid(True, color=GRID, lw=0.6)
        ax.set_xlim(40, 165)
        ax.set_ylim(bottom=0)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        sec = ax.secondary_xaxis("top", functions=(lambda g: g / 57.0, lambda r: r * 57.0))
        sec.set_xlabel("gap / D90 (D90 = 57 µm)", color=INK2)
    axs[0].legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "dem_summary.png"), dpi=130)
    plt.close(fig)


def topviews(cases):
    fig, axs = plt.subplots(len(cases), 1, figsize=(7.5, 2.0 * len(cases) + 0.8))
    fig.subplots_adjust(hspace=0.55, bottom=0.12, top=0.97)
    vmax = 160
    for ax, c in zip(axs, cases):
        cdir = os.path.join(D.WORK, c)
        hm = np.load(os.path.join(cdir, "heightmap.npy")) * 1e6
        cov = np.load(os.path.join(cdir, "covered.npy"))
        r = load(c)
        x0, x1 = r["zone_mm"]
        img = np.ma.masked_where(~cov, hm)
        ax.imshow(np.where(cov, np.nan, 1.0), extent=[x0, x1, 0, D.W * 1e3], origin="lower",
                  cmap=LinearSegmentedColormap.from_list("e", [EMPTY, EMPTY]), aspect="equal", vmin=0, vmax=1)
        im = ax.imshow(img, extent=[x0, x1, 0, D.W * 1e3], origin="lower", cmap=BLUES, vmin=0, vmax=vmax,
                       aspect="equal")
        ax.set_title(f"gap {r['gap_um']:.0f} µm, {r['v_mms']:.0f} mm/s, Γ {r['gamma_mJm2']:g} mJ/m² | "
                     f"cover {r['coverage']*100:.0f} %, holes ≥ D50 {r['empty_patch_fraction_D50']*100:.1f} %, "
                     f"packing {r['packing_fraction']:.2f}", loc="left", fontsize=8, color=INK)
        ax.set_yticks([0, 0.4])
        ax.set_ylabel("y (mm)")
    axs[-1].set_xlabel("x along the spread (mm); grey = bare substrate")
    cax = fig.add_axes([0.25, 0.035, 0.5, 0.012])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_label("powder top height (µm)")
    fig.savefig(os.path.join(OUT, "dem_topview.png"), dpi=130, bbox_inches="tight")
    plt.close(fig)


def blade_outline(gap, xc):
    zc = gap + D.R_NOSE
    a = np.linspace(np.pi, 2 * np.pi, 60)
    xs = np.r_[xc - D.R_NOSE, xc + D.R_NOSE * np.cos(a), xc + D.R_NOSE, xc + D.R_NOSE, xc - D.R_NOSE]
    zs = np.r_[zc + 1.2e-3, zc + D.R_NOSE * np.sin(a), zc, zc + 1.2e-3, zc + 1.2e-3]
    return xs * 1e3, zs * 1e3


def side(ax, d, gap, xc, title, slab=40e-6, zmax=0.75):
    sel = np.abs(d["y"] - D.W / 2) < slab
    typ = d["type"].astype(int)
    for mask, col in ((sel & (typ == D.T_BUMP), "#a9a8a2"), (sel & (typ <= D.NBIN), SERIES[0])):
        w = 2 * d["radius"][mask] * 1e3
        ec = EllipseCollection(w, w, np.zeros_like(w), units="xy", offsets=np.c_[d["x"][mask] * 1e3, d["z"][mask] * 1e3],
                               transOffset=ax.transData, facecolors=col, edgecolors="none")
        ax.add_collection(ec)
    bx, bz = blade_outline(gap, xc)
    ax.fill(bx, bz, color="#c3c2b7", ec=INK2, lw=0.8)
    ax.axhline(gap * 1e3, color=INK2, lw=0.6, ls="--")
    ax.set_xlim(0, D.LX * 1e3)
    ax.set_ylim(-0.03, zmax)
    ax.set_aspect("equal")
    ax.set_title(title, loc="left", fontsize=8.5, color=INK)
    ax.set_ylabel("z (mm)")


def sideviews(cases):
    fig, axs = plt.subplots(len(cases), 1, figsize=(11, 1.9 * len(cases)))
    for ax, c in zip(axs, cases):
        _, d = D.read_dump(os.path.join(D.WORK, c, "final.txt"))
        r = load(c)
        side(ax, d, r["gap_um"] * 1e-6, D.XC0 + D.TRAVEL,
             f"{c}: end of the stroke, 80 µm thick slice at mid-width; dashed line = blade gap")
    axs[-1].set_xlabel("x (mm)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "dem_sideview.png"), dpi=130)
    plt.close(fig)


def gif(case, nmax=40):
    from PIL import Image
    cdir = os.path.join(D.WORK, case)
    meta = json.load(open(os.path.join(cdir, "meta.json")))
    files = sorted(glob.glob(os.path.join(cdir, "dump", "d_*.txt")), key=lambda f: int(f.split("_")[-1][:-4]))
    files = files[:: max(1, len(files) // nmax)]
    frames = []
    for f in files:
        step, d = D.read_dump(f)
        t = (step - meta["n_settle"]) * meta["dt"]
        xc = D.XC0 + meta["v_ms"] * min(max(t, 0), D.TRAVEL / meta["v_ms"])
        fig, ax = plt.subplots(figsize=(9, 1.6))
        side(ax, d, meta["gap_m"], xc, f"{case}: t = {t*1e3:5.1f} ms", zmax=0.7)
        ax.set_xlabel("x (mm)")
        fig.tight_layout()
        fig.canvas.draw()
        frames.append(Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3]).quantize(colors=64))
        plt.close(fig)
    frames[0].save(os.path.join(OUT, f"dem_{case}.gif"), save_all=True, append_images=frames[1:], duration=120, loop=0,
                   optimize=True)


if __name__ == "__main__":
    summary()
    topviews(["g60_v50_low", "g100_v50_low", "g150_v150_low", "g100_v50_high", "g150_v150_high"])
    sideviews(["g60_v50_low", "g100_v50_low", "g100_v50_high"])
    gif("g100_v50_low")
    print("figures written to", OUT)
