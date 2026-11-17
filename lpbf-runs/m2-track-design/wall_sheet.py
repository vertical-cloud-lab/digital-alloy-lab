"""Wall-by-wall sheet for Carl's stepped parts on the M2 (issue #100, PR #243, 2026-11-17).

    python wall_sheet.py          # -> out/wall_sheet.csv (72 walls; plates 1-2 alone are the 48-wall version),
                                  #    out/wall_regime_grid.csv and out/m2-wall-design.png; about 2 min on 4 cores
    python wall_sheet.py figure   # redraw the figure from the two CSVs, no Eagar-Tsai

The part (Carl's drawing in PR #243, 2026-11-17): a base about 1.75 x 0.5 in with 8 thin walls standing on it,
each wall running across the 0.5 in width. Scaled from the drawing, a wall is about 1.3 mm (0.05 in) thick, on a
6.2 mm pitch, and 0.3 in tall. Every wall gets its own parameters. 3 parts a plate and 2-3 plates give 24 walls a
plate, 48 or 72 in all.

Each wall is a small bulk build (many tracks, many layers), not a single track. So:

- Only the hatch power P and speed v change from wall to wall. Trace spacing (0.09 mm), spot (130 um), layer,
  contours, delays and scan strategy stay as in the 316L set, so energy per volume follows P/v alone.
- The window is a band in (P, P/v): P from 150 to 370 W, and P/v from 0.09 to 0.55 J/mm, a third to twice the
  316L hatch's 0.274 J/mm. Speed is capped at 3000 mm/s. The upper cap keeps hot, swollen walls (a recoater
  risk) out of the first plates. The lower cap still has standard contours around a porous core.
- Each plate holds 21 settings from one scrambled Sobol sequence in (P, log P/v): points 0-20 on plate 1,
  21-41 on plate 2 and 42-62 on plate 3, so plates 1-2 are a 42-point design and plates 1-3 a 63-point one. Each
  plate also has 3 controls at the 316L hatch (370 W, 1350 mm/s), one per part. A plate's 21 settings are dealt
  to its 3 parts in snake order of P/v, so every part spans the window. Each part's 7 settings and its control
  then go to random wall positions (seed 100 + plate).
- For each setting the sheet gives VED at 30 and 50 um layers, Gan et al.'s keyhole number Ke (line_sheet.py),
  the steady-state Eagar-Tsai width W and depth D (130 um spot, absorptivity 0.4, as in eagar_tsai_316l.py), and
  Tang et al.'s overlap rule for lack of fusion, (h/W)^2 + (t/D)^2 <= 1, with h the trace spacing and t the layer
  (Addit. Manuf. 14, 39 (2017), https://doi.org/10.1016/j.addma.2016.12.001). Above 1, the half-elliptical pools
  leave unmelted gaps between tracks and layers. Eagar-Tsai is conduction only, cold substrate, no powder, so
  these regimes are a starting guess for the AM Module to replace, not a prediction.
"""
from __future__ import annotations

import csv
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from scipy.stats import qmc

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE))

from eagar_tsai_316l import steady_state_pkg  # noqa: E402
from line_sheet import keyhole_number           # noqa: E402

SEED = 100                       # issue #100
SPOT_UM = 130.0                  # the 316L hatch's spot
TRACE_MM = 0.09                  # the 316L hatch's trace spacing (Carl's photos)
LAYERS_UM = (30.0, 50.0)         # the 316L set's layer is not in the photos yet: both are shown
P_RANGE = (150.0, 370.0)         # W; 370 W is the 316L hatch, the most this laser is known to run
EL_RANGE = (0.09, 0.55)          # J/mm, P/v; the 316L hatch is 0.274
V_MAX = 3000.0                   # mm/s
CONTROL = dict(set="C", P=370.0, v=1350.0)     # the 316L hatch ("Adv. surface area")
PLATES, PARTS, WALLS = 3, 3, 8
PER_PLATE = PARTS * WALLS - PARTS              # 21 Sobol settings + 3 controls


def to_pv(u: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Unit square -> (P in W, v in mm/s): P linear in P_RANGE, P/v log-uniform between max(EL_lo, P/V_MAX) and
    EL_hi, so no point needs more than V_MAX. Rounded to 1 W and 5 mm/s."""
    P = np.round(P_RANGE[0] + u[:, 0] * (P_RANGE[1] - P_RANGE[0]))
    lo = np.log(np.maximum(EL_RANGE[0], P / V_MAX))
    el = np.exp(lo + u[:, 1] * (math.log(EL_RANGE[1]) - lo))
    return P, np.round(P / el / 5.0) * 5.0


def sobol(n: int, seed: int = SEED) -> np.ndarray:
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")      # n = 63 is not a power of 2; fine for a prefix of the sequence
        return qmc.Sobol(d=2, scramble=True, seed=seed).random(n)


def walls() -> list[dict]:
    """The 72 walls in plate, part, wall order, with their settings (no model columns yet)."""
    u = sobol(PLATES * PER_PLATE)
    P, v = to_pv(u)
    rows = []
    for plate in range(PLATES):
        idx = list(range(plate * PER_PLATE, (plate + 1) * PER_PLATE))
        idx.sort(key=lambda i: P[i] / v[i])
        parts: list[list[dict]] = [[] for _ in range(PARTS)]
        for r, i in enumerate(idx):                      # snake order: 0 1 2 2 1 0 0 1 2 ...
            k = r % PARTS if (r // PARTS) % 2 == 0 else PARTS - 1 - r % PARTS
            parts[k].append(dict(set=f"W{i:03d}", sobol_index=i, P=float(P[i]), v=float(v[i])))
        rng = np.random.default_rng(SEED + plate)
        for k, sets in enumerate(parts):
            sets = sets + [dict(CONTROL, sobol_index="")]
            for pos, j in enumerate(rng.permutation(len(sets))):
                rows.append(dict(plate=plate + 1, part=k + 1, wall=pos + 1, **sets[j]))
    return rows


def _et(args):
    P, v = args
    r = steady_state_pkg(P, v * 1e-3, spot_um=SPOT_UM)
    return r["W"], r["D"]


def lof_index(W_um: float, D_um: float, t_um: float) -> float:
    """Tang et al. (2017): (h/W)^2 + (t/D)^2; above 1 means lack of fusion."""
    return (TRACE_MM * 1e3 / W_um) ** 2 + (t_um / D_um) ** 2


def regime(lof: float, ke: float) -> str:
    if lof > 1.0:
        return "lack of fusion"
    return "keyhole mode" if ke >= 6.0 else "dense"


def with_model(rows: list[dict]) -> list[dict]:
    keys = sorted({(r["P"], r["v"]) for r in rows})
    with ProcessPoolExecutor() as ex:
        et = dict(zip(keys, ex.map(_et, keys)))
    out = []
    for order, r in enumerate(rows):
        W, D = et[(r["P"], r["v"])]
        ke = keyhole_number(r["P"], r["v"], SPOT_UM)
        el = r["P"] / r["v"]
        lof = {t: lof_index(W, D, t) for t in LAYERS_UM}
        out.append(dict(plate=r["plate"], part=r["part"], wall=r["wall"],
                        order_in_plate=(r["part"] - 1) * WALLS + r["wall"], set=r["set"],
                        sobol_index=r["sobol_index"], power_W=int(r["P"]), speed_mm_s=int(r["v"]),
                        spot_um=int(SPOT_UM), trace_spacing_mm=TRACE_MM, P_over_v_J_mm=round(el, 4),
                        VED_30um_J_mm3=round(el / (TRACE_MM * 0.030), 1),
                        VED_50um_J_mm3=round(el / (TRACE_MM * 0.050), 1), Ke=round(ke, 2),
                        ET_width_um=round(W, 1), ET_depth_um=round(D, 1),
                        LoF_index_30um=round(lof[30.0], 2), LoF_index_50um=round(lof[50.0], 2),
                        regime_30um=regime(lof[30.0], ke), regime_50um=regime(lof[50.0], ke)))
    return out


def regime_grid() -> list[dict]:
    """Eagar-Tsai on a coarse (P, v) grid for the figure's lack-of-fusion boundaries."""
    Ps = np.linspace(130.0, 390.0, 9)
    vs = np.geomspace(220.0, 3400.0, 11)
    keys = [(float(p), float(round(v))) for p in Ps for v in vs]
    with ProcessPoolExecutor() as ex:
        res = list(ex.map(_et, keys))
    return [dict(P_W=p, v_mm_s=v, ET_width_um=round(W, 1), ET_depth_um=round(D, 1),
                 LoF_index_30um=round(lof_index(W, D, 30.0), 3), LoF_index_50um=round(lof_index(W, D, 50.0), 3))
            for (p, v), (W, D) in zip(keys, res)]


# --- figure ---------------------------------------------------------------------------------------------------------
INK, INK2, MUTED, SURFACE = "#0b0b0b", "#52514e", "#8a8984", "#fcfcfb"
PLATE_STYLE = {1: ("#2a78d6", "o"), 2: ("#eb6834", "s"), 3: ("#1baf7a", "^")}   # categorical slots 1-3 + shape
ZONE = {"lof": "#ece9e2", "keyhole": "#dfe9f6"}


def figure(sheet: list[dict], grid: list[dict], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch, Rectangle
    from scipy.interpolate import griddata

    plt.rcParams.update({"font.size": 9.5, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                         "ytick.color": INK2, "axes.titlesize": 10.5})
    fig = plt.figure(figsize=(13.2, 6.2), constrained_layout=True)
    fig.set_facecolor(SURFACE)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0])
    ax = fig.add_subplot(gs[0, 0])
    ax.set_facecolor(SURFACE)

    # zones: Ke >= 6 (keyhole mode) and Eagar-Tsai + Tang lack of fusion at 30 um; dashed boundary at 50 um
    v = np.geomspace(220, 3400, 240)
    P = np.linspace(130, 390, 240)
    VV, PP = np.meshgrid(v, P)
    Ke = np.vectorize(lambda p_, v_: keyhole_number(p_, v_, SPOT_UM))(PP, VV)
    pts = np.array([[math.log(float(g["v_mm_s"])), float(g["P_W"])] for g in grid])
    lof30 = griddata(pts, [float(g["LoF_index_30um"]) for g in grid], (np.log(VV), PP), method="cubic")
    lof50 = griddata(pts, [float(g["LoF_index_50um"]) for g in grid], (np.log(VV), PP), method="cubic")
    ax.contourf(VV, PP, lof30, levels=[1.0, 1e3], colors=[ZONE["lof"]])
    ax.contourf(VV, PP, Ke, levels=[6.0, 1e3], colors=[ZONE["keyhole"]])
    ax.contour(VV, PP, lof30, levels=[1.0], colors=[INK2], linewidths=1.2)
    ax.contour(VV, PP, lof50, levels=[1.0], colors=[INK2], linewidths=1.2, linestyles="--")
    ax.contour(VV, PP, Ke, levels=[6.0], colors=["#2a78d6"], linewidths=1.0, alpha=0.6)
    # window: P/v band, P range, v cap (the 316L hatch's P/v dotted)
    for el in (EL_RANGE[0], 0.274, EL_RANGE[1]):
        vv = np.geomspace(max(P_RANGE[0] / el, 220), min(P_RANGE[1] / el, V_MAX), 50)
        ax.plot(vv, el * vv, color=MUTED, lw=0.9, ls=":" if el == 0.274 else "-")
    ax.annotate(f"P/v {EL_RANGE[1]} J/mm", (P_RANGE[0] / EL_RANGE[1], P_RANGE[0]), xytext=(-4, -12),
                textcoords="offset points", fontsize=7.8, color=INK2, ha="right", va="top")
    ax.annotate(f"P/v {EL_RANGE[0]} J/mm", (P_RANGE[0] / EL_RANGE[0], P_RANGE[0]), xytext=(4, -12),
                textcoords="offset points", fontsize=7.8, color=INK2, ha="left", va="top")
    ax.text(V_MAX * 1.02, 330, f"{V_MAX:.0f}\nmm/s\ncap", fontsize=7.8, color=INK2, ha="left", va="center")
    for p_ in P_RANGE:
        ax.plot([max(p_ / EL_RANGE[1], 220), min(p_ / EL_RANGE[0], V_MAX)], [p_, p_], color=MUTED, lw=0.9)
    ax.plot([V_MAX, V_MAX], [EL_RANGE[0] * V_MAX, P_RANGE[1]], color=MUTED, lw=0.9)

    for plate in range(1, PLATES + 1):
        c, m = PLATE_STYLE[plate]
        rs = [r for r in sheet if int(r["plate"]) == plate and r["set"] != "C"]
        ax.scatter([float(r["speed_mm_s"]) for r in rs], [float(r["power_W"]) for r in rs], s=46 if m != "^" else 54,
                   marker=m, c=c, edgecolors=SURFACE, linewidths=1.4, zorder=4)
    ax.scatter([CONTROL["v"]], [CONTROL["P"]], s=230, marker="*", c=INK, edgecolors=SURFACE, linewidths=1.2, zorder=5)
    ax.text(3330, 388, "lack of fusion\n(Eagar–Tsai + overlap rule)", fontsize=8.2, color=INK2, ha="right", va="top")
    ax.text(228, 388, "keyhole mode (Ke ≥ 6)", fontsize=8.2, color="#1c5cab", ha="left", va="top")
    ax.set_xscale("log")
    ax.set_xticks([250, 500, 1000, 2000, 3000])
    ax.set_xticklabels(["250", "500", "1000", "2000", "3000"])
    ax.minorticks_off()
    ax.set_xlim(220, 3400)
    ax.set_ylim(130, 390)
    ax.set_xlabel("Hatch speed (mm/s, log scale)")
    ax.set_ylabel("Hatch power (W)")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    n_each = {p: sum(1 for r in sheet if int(r["plate"]) == p and r["set"] != "C") for p in range(1, PLATES + 1)}
    ax.set_title(f"(a) {sum(n_each.values())} Sobol settings in (P, log P/v) and 9 controls\n"
                 "zones: Eagar–Tsai at 130 µm, a first guess for the AM Module", loc="left", color=INK)
    handles = [Line2D([], [], ls="none", marker=PLATE_STYLE[p][1], ms=7.5, mfc=PLATE_STYLE[p][0], mec=SURFACE,
                      label=f"plate {p} ({n_each[p]} settings)") for p in range(1, PLATES + 1)]
    handles += [Line2D([], [], ls="none", marker="*", ms=13, mfc=INK, mec=SURFACE, label="control: 316L hatch, 370 W,\n1350 mm/s (its P/v dotted)"),
                Patch(facecolor=ZONE["lof"], edgecolor="none", label="lack of fusion at 30 µm layers"),
                Line2D([], [], color=INK2, ls="--", lw=1.2, label="its edge at 50 µm layers"),
                Patch(facecolor=ZONE["keyhole"], edgecolor="none", label="keyhole mode, Ke ≥ 6")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=3, frameon=False, fontsize=8.2)

    # (b) plate 1 as three parts of eight walls, in the sheet's order
    bx = fig.add_subplot(gs[0, 1])
    bx.set_facecolor(SURFACE)
    bx.set_xlim(-0.6, WALLS + 0.2)
    bx.set_ylim(-0.4, PARTS * 1.55 + 0.1)
    bx.axis("off")
    for k in range(PARTS):
        y0 = (PARTS - 1 - k) * 1.55
        bx.add_patch(Rectangle((0.0, y0), WALLS, 0.36, fc="#e4e3de", ec=MUTED, lw=0.8))
        bx.text(-0.12, y0 + 0.18, f"part {k + 1}", ha="right", va="center", fontsize=9, color=INK)
        for r in [r for r in sheet if int(r["plate"]) == 1 and int(r["part"]) == k + 1]:
            x = int(r["wall"]) - 0.5
            ctrl = r["set"] == "C"
            bx.add_patch(Rectangle((x - 0.09, y0 + 0.36), 0.18, 0.62, fc=INK if ctrl else "#b9b8b1", ec="none"))
            lab = "control\n370 W\n1350" if ctrl else f"{r['set']}\n{int(float(r['power_W']))} W\n{int(float(r['speed_mm_s']))}"
            bx.text(x, y0 + 1.02, lab, ha="center", va="bottom", fontsize=7.6, color=INK, linespacing=1.05)
            bx.text(x, y0 + 0.18, str(int(r["wall"])), ha="center", va="center", fontsize=7.5, color=INK2)
    bx.text(0.0, -0.18, "Wall numbers 1–8 count from the marked end of each base; speeds in mm/s. Every wall: "
            "130 µm spot,\n0.09 mm trace spacing, the 316L set's contours and layer. Plates 2 and 3: "
            "out/wall_sheet.csv.", fontsize=7.8, color=INK2, va="top")
    bx.set_title("(b) Plate 1: three parts, eight walls each (side view, not to scale)", loc="left", color=INK)
    fig.suptitle("Carl's stepped parts on the M2: one hatch power and speed per wall, everything else at the "
                 "316L set", x=0.01, ha="left", fontsize=12, color=INK)
    fig.savefig(path, dpi=150, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def write(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    if sys.argv[1:] == ["figure"]:
        figure(list(csv.DictReader(open(OUT / "wall_sheet.csv"))), list(csv.DictReader(open(OUT / "wall_regime_grid.csv"))),
               OUT / "m2-wall-design.png")
        sys.exit()
    sheet = with_model(walls())
    write(OUT / "wall_sheet.csv", sheet)
    grid = regime_grid()
    write(OUT / "wall_regime_grid.csv", grid)
    figure([{k: str(x) for k, x in r.items()} for r in sheet], [{k: str(x) for k, x in g.items()} for g in grid],
           OUT / "m2-wall-design.png")

    for plate in range(1, PLATES + 1):
        rs = [r for r in sheet if r["plate"] == plate]
        sob = [r for r in rs if r["set"] != "C"]
        print(f"plate {plate}: P {min(r['power_W'] for r in sob)}-{max(r['power_W'] for r in sob)} W, "
              f"v {min(r['speed_mm_s'] for r in sob)}-{max(r['speed_mm_s'] for r in sob)} mm/s, "
              f"P/v {min(r['P_over_v_J_mm'] for r in sob)}-{max(r['P_over_v_J_mm'] for r in sob)}, "
              f"Ke {min(r['Ke'] for r in sob)}-{max(r['Ke'] for r in sob)}; at 30 um",
              {g: sum(r["regime_30um"] == g for r in sob) for g in ("lack of fusion", "dense", "keyhole mode")},
              "at 50 um", {g: sum(r["regime_50um"] == g for r in sob) for g in ("lack of fusion", "dense", "keyhole mode")})
        for k in range(1, PARTS + 1):
            ps = [r for r in sob if r["part"] == k]
            print(f"   part {k}: P/v {min(r['P_over_v_J_mm'] for r in ps)}-{max(r['P_over_v_J_mm'] for r in ps)}")
    c = next(r for r in sheet if r["set"] == "C")
    print("control:", {k: c[k] for k in ("Ke", "ET_width_um", "ET_depth_um", "LoF_index_30um", "LoF_index_50um",
                                         "regime_30um", "regime_50um", "VED_30um_J_mm3", "VED_50um_J_mm3")})
