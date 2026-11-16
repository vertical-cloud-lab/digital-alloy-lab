"""Line-by-line sheet for the M2 pilot: what to enter in CL WRX Control for each line (issue #100, PR #243).

    python line_sheet.py          # -> out/pilot_line_sheet.csv (72 lines), out/pilot_line_sheet_48.csv (48 lines),
                                  #    out/spot_regimes.csv (both spots, every setting) and out/m2-spot-choice.png;
                                  #    about 2 min on 4 cores
    python line_sheet.py figure   # redraw the figure from out/spot_regimes.csv

Carl's photos of the M2's 316L parameter set (PR #243, 2026-11-10) show that CL WRX Control 2.4 sets a spot size
for each exposure type (50, 70 and 130 um appear), and that the set's hatch, "Adv. surface area", runs 370 W,
1350 mm/s, 130 um spot and 0.09 mm trace spacing. So the pilot has to pick a spot. This script:

1. computes Gan et al.'s keyhole number for every setting at a 50 um and a 130 um spot,
       Ke = eta P / ((T_l - T_0) pi rho c_p sqrt(alpha v r0^3)),   r0 = spot radius,
   (Nat. Commun. 12, 2379 (2021), https://doi.org/10.1038/s41467-021-22704-0, Eq. 1). Their X-ray data put
   conduction below Ke 1.4, transition from 1.4 to 6, keyhole above 6, a stable keyhole below about 16 and a
   chaotic one (pores, spatter) above about 30. eta = 0.4 and the 316L values are those of eagar_tsai_316l.py;
   eta rises in a deep keyhole, so Ke here is low there, which doesn't move the regime boundaries much;
2. runs the steady-state Eagar-Tsai model (the package and inputs eagar_tsai_316l.py uses) at both spots;
3. writes the sheet at the chosen spot, 130 um: one row per line, in exposure order, with the panel, the position
   counted from the gas-outlet side, the mount piece, the set, power, speed, spot, P/v, Ke and the regime.

Positions come from ../m2-viz/layout.py (seed 100), so the sheet, the pilot-design figure and the animation agree.
The 48-line fallback keeps all four panels at 12 lines each: one 8-point Sobol net (points 0-7 on A, 8-15 on B,
16-23 on C, 24-31 on D, each a balanced set over the whole window) plus two of points 32-39, and 2 controls.
"""
from __future__ import annotations

import csv
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "m2-viz"))

import design                                  # noqa: E402  (the Sobol sets)
from eagar_tsai_316l import MATERIALS, ABSORPTIVITY, T0, steady_state_pkg  # noqa: E402
import layout                                  # noqa: E402  (positions on the panels, seed 100)

SPOT_UM = 130.0                 # the pilot's spot: the 316L set's hatch spot
OTHER_SPOT_UM = 50.0            # the M2's smallest (its fixed focus), for comparison
CONTROL = dict(id="C", P=370.0, v=1350.0)      # the 316L set's hatch ("Adv. surface area"), from Carl's photos
# The other 316L settings in the photos, for the figure (P W, v mm/s, spot um)
M2_316L = {
    "hatch (control)": (370.0, 1350.0, 130.0),
    "upskin hatch": (200.0, 980.0, 130.0),
    "downskin hatch": (280.0, 1300.0, 130.0),
    "lattice support": (270.0, 1200.0, 50.0),
}
KE_BANDS = ((0.0, 1.4, "conduction"), (1.4, 6.0, "transition"), (6.0, 16.0, "keyhole, stable"),
            (16.0, 30.0, "keyhole, fluctuating"), (30.0, math.inf, "keyhole, unstable (pores)"))


def keyhole_number(P: float, v_mm_s: float, spot_um: float, eta: float = ABSORPTIVITY, mat: str = "nominal") -> float:
    m = MATERIALS[mat]
    rhoc = m["rho"] * m["cp"]
    alpha = m["k"] / rhoc
    r0 = spot_um * 1e-6 / 2.0
    return eta * P / ((m["T_liq"] - T0) * math.pi * rhoc * math.sqrt(alpha * v_mm_s * 1e-3 * r0 ** 3))


def regime(ke: float) -> str:
    return next(name for lo, hi, name in KE_BANDS if lo <= ke < hi)


def _et(args):
    P, v, spot = args
    r = steady_state_pkg(P, v * 1e-3, spot_um=spot)
    return dict(W_um=r["W"], D_um=r["D"], L_um=r["L"])


def model_table(sets: list[dict]) -> list[dict]:
    jobs = [(s["P"], s["v"], spot) for s in sets for spot in (OTHER_SPOT_UM, SPOT_UM)]
    with ProcessPoolExecutor() as ex:
        res = list(ex.map(_et, jobs))
    rows = []
    for (P, v, spot), r in zip(jobs, res):
        sid = next(s["id"] for s in sets if s["P"] == P and s["v"] == v)
        ke = keyhole_number(P, v, spot)
        rows.append(dict(set=sid, P_W=P, v_mm_s=v, spot_um=spot, E_J_mm=round(P / v, 4), Ke=round(ke, 2),
                         regime=regime(ke), ET_W_um=round(r["W_um"], 1), ET_D_um=round(r["D_um"], 1),
                         ET_L_um=round(r["L_um"], 1)))
    return rows


def sheet72(model: dict) -> list[dict]:
    rows = []
    for t in layout.track_map():
        sid = "C" if t["set"] == layout.CONTROL else t["set"]
        m = model[(sid, SPOT_UM)]
        rows.append(dict(line=t["order"] + 1, panel=t["insert"], position_from_outlet=t["k"] + 1, mount_piece=t["group"],
                         set=sid, power_W=int(m["P_W"]), speed_mm_s=int(m["v_mm_s"]), spot_um=int(SPOT_UM),
                         P_over_v_J_mm=m["E_J_mm"], Ke=m["Ke"], regime_by_Ke=m["regime"],
                         ET_width_um=m["ET_W_um"], ET_depth_um=m["ET_D_um"]))
    return rows


def sheet48(model: dict, seed: int = layout.SEED) -> list[dict]:
    """4 panels x 12 lines: one 8-point Sobol net per panel + 2 of points 32-39 + 2 controls, random positions."""
    P, v = design.to_pv(design.sobol_points(64)[:40])
    rng = np.random.default_rng(seed)
    rows, line = [], 1
    for k, panel in enumerate(layout.INSERTS):
        idx = list(range(8 * k, 8 * k + 8)) + [32 + 2 * k, 33 + 2 * k]
        sets = [dict(id=f"S{i:03d}", P=float(P[i]), v=float(v[i])) for i in idx] + [dict(CONTROL)] * 2
        for pos, j in enumerate(rng.permutation(len(sets))):
            s = sets[j]
            ke = keyhole_number(s["P"], s["v"], SPOT_UM)
            m = model.get((s["id"], SPOT_UM))
            rows.append(dict(line=line, panel=panel, position_from_outlet=pos + 1, mount_piece=1 + (pos >= 6),
                             set=s["id"], power_W=int(s["P"]), speed_mm_s=int(s["v"]), spot_um=int(SPOT_UM),
                             P_over_v_J_mm=round(s["P"] / s["v"], 4), Ke=round(ke, 2), regime_by_Ke=regime(ke),
                             ET_width_um=m["ET_W_um"] if m else "", ET_depth_um=m["ET_D_um"] if m else ""))
            line += 1
    return rows


# --- figure: where the 64 settings fall at each spot -----------------------------------------------------------------
BAND_COLOURS = ("#cde2fb", "#9ec5f4", "#6da7ec", "#2a78d6", "#184f95")   # one blue ramp, light -> dark (ordinal)
INK, INK2, SURFACE, ACCENT = "#0b0b0b", "#52514e", "#fcfcfb", "#eb6834"


def figure(table: list[dict], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    plt.rcParams.update({"font.size": 9.5, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                         "ytick.color": INK2, "axes.titlesize": 10})
    v = np.geomspace(200, 2400, 300)
    P = np.linspace(80, 400, 300)
    VV, PP = np.meshgrid(v, P)
    levels = [0.0, 1.4, 6.0, 16.0, 30.0, 1e4]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.4), sharey=True, constrained_layout=True)
    fig.set_facecolor(SURFACE)
    for ax, spot in zip(axes, (OTHER_SPOT_UM, SPOT_UM)):
        ax.set_facecolor(SURFACE)
        Ke = np.vectorize(lambda p_, v_: keyhole_number(p_, v_, spot))(PP, VV)
        ax.contourf(VV, PP, Ke, levels=levels, colors=BAND_COLOURS)
        cs = ax.contour(VV, PP, Ke, levels=levels[1:-1], colors=[SURFACE], linewidths=1.0)
        ax.clabel(cs, fmt={1.4: "Ke 1.4", 6.0: "Ke 6", 16.0: "Ke 16", 30.0: "Ke 30"}, fontsize=8, colors=INK,
                  inline_spacing=2)
        rs = [r for r in table if float(r["spot_um"]) == spot and r["set"] != "C"]
        deep = [r for r in rs if float(r["ET_D_um"]) >= 30]
        shallow = [r for r in rs if float(r["ET_D_um"]) < 30]
        ax.scatter([float(r["v_mm_s"]) for r in deep], [float(r["P_W"]) for r in deep], s=34, c=INK,
                   edgecolors=SURFACE, linewidths=1.2, zorder=3)
        ax.scatter([float(r["v_mm_s"]) for r in shallow], [float(r["P_W"]) for r in shallow], s=34, c=SURFACE,
                   edgecolors=INK, linewidths=1.6, zorder=3)
        ax.scatter([CONTROL["v"]], [CONTROL["P"]], s=190, marker="*", c=ACCENT, edgecolors=SURFACE, linewidths=1.2,
                   zorder=4)
        ke_c = keyhole_number(CONTROL["P"], CONTROL["v"], spot)
        ax.annotate(f"control = the 316L hatch, Ke {ke_c:.1f}", (CONTROL["v"], CONTROL["P"]),
                    xytext=(-14, 12), textcoords="offset points", ha="right", va="bottom", fontsize=8.5, color=INK,
                    bbox=dict(boxstyle="round,pad=0.25", fc=SURFACE, ec="none", alpha=0.9),
                    arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
        n = {name: sum(r["regime"] == name for r in rs) for _, _, name in KE_BANDS}
        kh = sum(float(r["Ke"]) >= 6 for r in rs)
        hi = sum(float(r["Ke"]) >= 16 for r in rs)
        if spot == SPOT_UM:
            title = (f"{spot:.0f} µm spot (the 316L hatch's): Ke {min(float(r['Ke']) for r in rs):.1f}–"
                     f"{max(float(r['Ke']) for r in rs):.1f}\n{n['conduction'] + n['transition']} conduction or "
                     f"transition, {kh} stable keyhole, none above Ke 16")
        else:
            title = (f"{spot:.0f} µm spot (the M2's focus): Ke {min(float(r['Ke']) for r in rs):.1f}–"
                     f"{max(float(r['Ke']) for r in rs):.1f}\n{kh} of 64 in keyhole mode, {hi} of them above Ke 16")
        ax.set_title(title, loc="left", color=INK)
        ax.set_xscale("log")
        ax.set_xticks([250, 500, 1000, 2000])
        ax.set_xticklabels(["250", "500", "1000", "2000"])
        ax.minorticks_off()
        ax.set_xlim(200, 2400)
        ax.set_ylim(80, 400)
        ax.set_xlabel("Scan speed (mm/s, log scale)")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0].set_ylabel("Laser power (W)")
    handles = [Patch(facecolor=c, edgecolor="none", label=name) for c, (_, _, name) in zip(BAND_COLOURS, KE_BANDS)]
    handles += [Line2D([], [], ls="none", marker="o", ms=6.5, mfc=INK, mec=SURFACE, label="Sobol setting"),
                Line2D([], [], ls="none", marker="o", ms=6.5, mfc=SURFACE, mec=INK, mew=1.4,
                       label="Eagar–Tsai depth < 30 µm\n(may not bond through the layer)"),
                Line2D([], [], ls="none", marker="*", ms=13, mfc=ACCENT, mec=SURFACE, label="control (316L hatch)")]
    fig.legend(handles=handles, loc="outside right center", frameon=False, title="Regime by keyhole number",
               title_fontsize=9.5, alignment="left")
    fig.suptitle("The pilot's 64 Sobol settings (100–375 W, 250–2000 mm/s) at the M2's two spot sizes",
                 x=0.01, ha="left", fontsize=11.5, color=INK)
    fig.text(0.01, -0.035, "Ke = ηP / ((T_l − T_0) π ρ c_p √(α v r0³)), r0 = spot radius (Gan et al., Nat. Commun. 12, 2379, "
             "2021): conduction below 1.4, keyhole above 6, a stable keyhole below about 16, pores and spatter above "
             "about 30.\n316L: η 0.4, T_l 1723 K, ρ 7300 kg/m³, c_p 710 J/kg/K, k 26 W/m/K (as in eagar_tsai_316l.py). "
             "Steady-state Eagar–Tsai depths, widths and lengths for every point: out/spot_regimes.csv.",
             fontsize=8, color=INK2, ha="left", va="top")
    fig.savefig(path, dpi=150, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def write(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    if sys.argv[1:] == ["figure"]:                      # redraw from the saved table, no Eagar-Tsai
        figure(list(csv.DictReader(open(OUT / "spot_regimes.csv"))), OUT / "m2-spot-choice.png")
        sys.exit()
    sets = [dict(id=s["id"], P=s["P"], v=s["v"]) for s in design.pilot_sets()]
    P40, v40 = design.to_pv(design.sobol_points(64)[:40])
    assert all(sets[i]["P"] == P40[i] and sets[i]["v"] == v40[i] for i in range(32)), "Sobol prefix mismatch"
    extra = [dict(id=f"S{i:03d}", P=float(P40[i]), v=float(v40[i])) for i in range(32, 40)]
    assert all(e["id"] == sets[32 + j]["id"] and e["P"] == sets[32 + j]["P"] for j, e in enumerate(extra))
    sets.append(dict(CONTROL))
    table = model_table(sets)
    write(OUT / "spot_regimes.csv", table)
    model = {(r["set"], r["spot_um"]): r for r in table}
    s72, s48 = sheet72(model), sheet48(model)
    write(OUT / "pilot_line_sheet.csv", s72)
    write(OUT / "pilot_line_sheet_48.csv", s48)
    figure(table, OUT / "m2-spot-choice.png")

    for spot in (OTHER_SPOT_UM, SPOT_UM):
        rs = [r for r in table if r["spot_um"] == spot and r["set"] != "C"]
        counts = {name: sum(r["regime"] == name for r in rs) for _, _, name in KE_BANDS}
        print(f"spot {spot:.0f} um, 64 Sobol settings: Ke {min(r['Ke'] for r in rs)}-{max(r['Ke'] for r in rs)};",
              counts, f"E-T depth {min(r['ET_D_um'] for r in rs)}-{max(r['ET_D_um'] for r in rs)} um,",
              f"width {min(r['ET_W_um'] for r in rs)}-{max(r['ET_W_um'] for r in rs)} um")
    for name, (P, v, spot) in M2_316L.items():
        print(f"M2 316L {name}: {P:.0f} W, {v:.0f} mm/s, {spot:.0f} um -> Ke {keyhole_number(P, v, spot):.1f}"
              f" ({regime(keyhole_number(P, v, spot))}); at {OTHER_SPOT_UM if spot == SPOT_UM else SPOT_UM:.0f} um"
              f" Ke {keyhole_number(P, v, OTHER_SPOT_UM if spot == SPOT_UM else SPOT_UM):.1f}")
    for nm, sh in (("72", s72), ("48", s48)):
        print(nm, "lines:", {name: sum(r["regime_by_Ke"] == name for r in sh) for _, _, name in KE_BANDS},
              "distinct sets", len({r["set"] for r in sh}))
