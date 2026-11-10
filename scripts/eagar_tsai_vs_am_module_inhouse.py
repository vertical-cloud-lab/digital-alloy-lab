"""Compare ArroyaveLab/eagar-tsai with our in-house Thermo-Calc AM-module results (#235).

The in-house results are four PNGs that Thermo-Calc's account manager ran for us with the
settings we asked for (``edison-trajectories/results/scanparams/scanparams_summary.csv`` on the
``consolidation-2`` branch). They live in ``figures/thermo-calc-am-module-prelim-results/`` on
that branch. No CSV came with them, so this script reads the numbers off the images:

* ``digitize``: for both printability maps (stock AlSi10Mg and the BYU AA1100+Si+AlSi10Mg blend)
  it finds the class of every grid point (keyholing, lack of fusion D/t <= 1, lack of fusion at
  half the hatch Dh/t <= 1, or none) from the fill colour around its marker, and traces the three
  region boundaries column by column. Points and boundary stretches under the legend are marked
  hidden.
* ``compare``: runs eagar-tsai with the same beam, layer, hatch and preheat, then
  - applies the AM module's own criteria (D/t and Dh/t; Dh is the melt-pool depth at half the
    hatch distance from the track centre line) and eagar-tsai's defaults (Sheikh et al. 2024:
    W/D <= 2.5 keyhole, D <= t or (h/W)^2 + t/(t+D) >= 1 lack of fusion);
  - finds, at every speed, the absorptivity eagar-tsai needs to put each boundary where the AM
    module drew it;
  - compares the two melt-pool points the AM module rendered.

eagar-tsai's temperature rise is proportional to the absorbed power Q = A*P, and the model only
returns the surface (z = 0) and centre-line (y = 0) planes. So for each speed the script builds
max-over-x profiles of the temperature rise per watt with eagar-tsai's own compiled integrand
(``eagar_tsai._core._INTEGRAND``) and the package's scaling. It reads W, D, L, Dh and the peak
temperature off those profiles for any Q, and checks them against ``compute_single_point``.

eagar-tsai fixes the ambient temperature at 298 K. Its temperature field is linear in (T - T0),
so a build-plate preheat T_p is the same as lowering the melt isotherm by (T_p - 298 K). Peak
temperatures are reported with the preheat added back.

Usage::

    git show origin/consolidation-2:figures/thermo-calc-am-module-prelim-results/<png> > <png>
    python scripts/eagar_tsai_vs_am_module_inhouse.py all \\
        --png-dir arroyave-orchid-tools/eagar-tsai/am-module-inhouse \\
        --out arroyave-orchid-tools/eagar-tsai/am-module-inhouse
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import time
from concurrent.futures import ProcessPoolExecutor

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

# --------------------------------------------------------------------------------------------
# The two AM-module printability maps: inputs (from scanparams_summary.csv) and pixel calibration
# --------------------------------------------------------------------------------------------
# Pixel calibration: v = v0 + (x - x0) * dv ; P = P0 + (y0 - y) * dP. Calibrated on the grid
# markers (AlSi10Mg: 300..2100 mm/s every 200, 100..400 W every 50; blend: 400..2400 mm/s every
# 400, 75..315 W every 60), which sit within 1 px of these lines.
MAPS = {
    "alsi10mg": dict(
        png="AlSi10Mg-printability-map.png",
        label="AlSi10Mg (Al-10Si-0.325Mg)",
        speeds=list(range(300, 2101, 200)),
        powers=list(range(100, 401, 50)),
        x0=138.0, v0=300.0, dv=3.0,
        y0=28.0, P0=400.0, dP=300.0 / 598.0,
        frame=(138, 738, 28, 626),
        beam_radius_um=40.0,
        layer_um=30.0,
        hatch_um=130.0,
        preheat_C=150.0,
        keyhole_wk_dk=0.7,
    ),
    "byu-blend": dict(
        png="BYU-AA1100-Si-AlSi10Mg-blend-printability-map.png",
        label="BYU AA1100+Si+AlSi10Mg blend (Al-24.30Si-0.14Mg)",
        speeds=list(range(400, 2401, 400)),
        powers=list(range(75, 316, 60)),
        x0=136.0, v0=400.0, dv=2000.0 / 600.0,
        y0=627.0, P0=75.0, dP=60.0 / 127.5,
        frame=(136, 736, 29, 627),
        beam_radius_um=45.0,
        layer_um=30.0,
        hatch_um=100.0,
        preheat_C=30.0,
        keyhole_wk_dk=0.7,
    ),
}

# The two 3D melt pools the AM module rendered (read off the colour bars and the axis labels).
MELT_POOLS = {
    "alsi10mg": dict(P=250.0, v_mm_s=900.0, T_peak_K=3044.0, T_min_K=423.0, q_peak_W_mm2=30574.0,
                     q_min_W_mm2=4138.0, u_max_m_s=3.3),
    "byu-blend": dict(P=375.0, v_mm_s=400.0, T_peak_K=2846.0 + 273.15, T_min_K=30.0 + 273.15,
                      q_peak_W_mm2=45286.0, q_min_W_mm2=6129.0, u_max_m_s=3.2,
                      L_um=1470.0, y_extent_um=231.0, D_um=349.0),
}

# Fill colours of the Thermo-Calc printability map.
COLOURS = {
    "keyhole": (237, 121, 127),
    "lof_hatch": (187, 131, 198),
    "lof": (121, 153, 106),
    "none": (255, 255, 255),
}
MARKER_COLOURS = [(22, 41, 132), (141, 33, 76)]

# Properties for eagar-tsai. AlSi10Mg: the Edison values Xavier's sweep uses (#235). The blend
# has no measured values; it gets the same thermal properties and two isotherms (eutectic and
# liquidus) because which one the AM module puts at the pool edge matters for a 24 % Si alloy.
MATERIALS = {
    "alsi10mg": [dict(name="AlSi10Mg, T_liq 867 K", T_iso=867.0, k=110.0, rho=2650.0, cp=1040.0)],
    "byu-blend": [
        dict(name="blend, eutectic 850 K", T_iso=850.0, k=110.0, rho=2650.0, cp=1040.0),
        dict(name="blend, liquidus ~1028 K", T_iso=1028.0, k=110.0, rho=2650.0, cp=1040.0),
    ],
}
T_BOIL_AL_K = 2743.0
T0_ET = 298.0  # eagar-tsai's fixed ambient temperature (eagar_tsai._types._T0_K)


# --------------------------------------------------------------------------------------------
# Digitizing
# --------------------------------------------------------------------------------------------
def _load(png: pathlib.Path) -> np.ndarray:
    return np.asarray(Image.open(png).convert("RGB")).astype(int)


def _near(im: np.ndarray, colour, tol=45) -> np.ndarray:
    return np.abs(im - np.array(colour)).sum(axis=2) < tol


def _legend_box(im: np.ndarray, frame) -> tuple[int, int, int, int]:
    """Find the legend rectangle (dark border) inside the plot frame, upper right."""
    x_lo, x_hi, y_lo, y_hi = frame
    dark = im.sum(axis=2) < 200
    # rows of the legend's top/bottom border: long dark runs that are not the frame lines
    rows = [y for y in range(y_lo + 1, (y_lo + y_hi) // 2) if dark[y, x_lo + 5: x_hi - 5].sum() > 250]
    cols = [x for x in range(x_lo + 5, x_hi - 1) if dark[y_lo + 3: rows[-1] if rows else y_lo + 120, x].sum() > 80]
    top = min(rows) if rows else y_lo
    bottom = max(rows) if rows else y_lo + 110
    left = min(cols) if cols else (x_lo + x_hi) // 2
    right = max(cols) if cols else x_hi
    return left, right, top, bottom


def _px_to_data(cfg, x, y):
    return cfg["v0"] + (x - cfg["x0"]) * cfg["dv"], cfg["P0"] + (cfg["y0"] - y) * cfg["dP"]


def _data_to_px(cfg, v, P):
    return cfg["x0"] + (v - cfg["v0"]) / cfg["dv"], cfg["y0"] - (P - cfg["P0"]) / cfg["dP"]


def digitize(cfg: dict, png: pathlib.Path) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    im = _load(png)
    x_lo, x_hi, y_lo, y_hi = cfg["frame"]
    lg = _legend_box(im, cfg["frame"])
    masks = {k: _near(im, c) for k, c in COLOURS.items()}
    marker = np.zeros(im.shape[:2], bool)
    for c in MARKER_COLOURS:
        marker |= _near(im, c, 90)

    def hidden(x, y, pad=3):
        return lg[0] - pad <= x <= lg[1] + pad and lg[2] - pad <= y <= lg[3] + pad

    rows = []
    for P in cfg["powers"]:
        for v in cfg["speeds"]:
            xc, yc = _data_to_px(cfg, v, P)
            votes = {k: 0 for k in COLOURS}
            for dy in range(-9, 10):
                for dx in range(-9, 10):
                    r = math.hypot(dx, dy)
                    if not (5.0 <= r <= 9.0):
                        continue
                    x, y = int(round(xc + dx)), int(round(yc + dy))
                    if not (x_lo + 3 <= x <= x_hi - 3 and y_lo + 3 <= y <= y_hi - 3) or hidden(x, y):
                        continue
                    for k, m in masks.items():
                        if m[y, x]:
                            votes[k] += 1
            total = sum(votes.values())
            if total < 6:
                cls, frac = "hidden", float("nan")
            else:
                cls = max(votes, key=votes.get)
                frac = votes[cls] / total
            # marker style: filled (centre is marker-coloured), open (ring only), or none
            xi, yi = int(round(xc)), int(round(yc))
            style = "none"
            if min(xi - x_lo, x_hi - xi, yi - y_lo, y_hi - yi) <= 3:
                style = "edge"  # half under the frame line: can't tell filled from open
            elif not hidden(xi, yi, 0):
                win = marker[max(yi - 4, 0): yi + 5, max(xi - 4, 0): xi + 5]
                if marker[yi, xi] or marker[yi, max(xi - 1, 0)] or marker[yi, xi + 1 if xi + 1 < im.shape[1] else xi]:
                    style = "filled"
                elif win.sum() >= 6:
                    style = "open"
            rows.append(dict(power_W=P, speed_mm_s=v, am_class=cls, vote_fraction=round(frac, 3),
                             marker=style))
    pts = pd.DataFrame(rows)

    # boundaries, one sample per pixel column
    brows = []
    for x in range(x_lo + 2, x_hi - 1):
        v, _ = _px_to_data(cfg, x, 0)
        col_red = np.where(masks["keyhole"][y_lo + 2: y_hi - 1, x])[0] + y_lo + 2
        col_pur = np.where((masks["lof_hatch"] | masks["lof"])[y_lo + 2: y_hi - 1, x])[0] + y_lo + 2
        col_grn = np.where(masks["lof"][y_lo + 2: y_hi - 1, x])[0] + y_lo + 2
        P_kh = P_lh = P_lof = float("nan")
        if col_red.size:
            yb = col_red.max()
            # hidden if the red region runs into the legend in this column
            in_legend_cols = lg[0] - 3 <= x <= lg[1] + 3
            if not (in_legend_cols and yb <= lg[3] + 3):
                P_kh = _px_to_data(cfg, x, yb + 0.5)[1]
        if col_pur.size:
            P_lh = _px_to_data(cfg, x, col_pur.min() - 0.5)[1]
        if col_grn.size:
            P_lof = _px_to_data(cfg, x, col_grn.min() - 0.5)[1]
        brows.append(dict(speed_mm_s=round(v, 1), P_keyhole_W=P_kh, P_lof_hatch_W=P_lh, P_lof_W=P_lof))
    bnd = pd.DataFrame(brows)
    meta = dict(legend_box_px=list(map(int, lg)))
    return pts, bnd, meta


# --------------------------------------------------------------------------------------------
# eagar-tsai response profiles (per watt of absorbed power)
# --------------------------------------------------------------------------------------------
def _profiles_one(args):
    v_mm_s, beam_d_m, k, rho, cp, hatch_m = args
    from eagar_tsai._core import _INTEGRAND  # compiled LowLevelCallable when built from source

    v = v_mm_s * 1e-3
    alpha = k / (rho * cp)
    sig = math.sqrt(2.0) * beam_d_m / 2.0  # eagar-tsai's internal sigma
    p = alpha / (v * sig)
    s1 = 1.0 / (math.pi * (k / alpha) * math.sqrt(math.pi * alpha * v * sig**3))  # K per W absorbed
    zs = math.sqrt(alpha * sig / v)

    def I(x, y, z):
        return quad(_INTEGRAND, 0.0, np.inf, args=(x / sig, y / sig, z / zs, p))[0]

    xs_coarse = np.concatenate([np.linspace(-2 * sig, 2 * sig, 17), np.geomspace(2.2 * sig, 3e-3, 40)])

    def maxx(y, z):
        vals = np.array([I(x, y, z) for x in xs_coarse])
        i = int(vals.argmax())
        lo = xs_coarse[max(i - 1, 0)]
        hi = xs_coarse[min(i + 1, xs_coarse.size - 1)]
        if hi <= lo:
            return float(vals[i]), float(xs_coarse[i])
        r = minimize_scalar(lambda x: -I(x, y, z), bounds=(lo, hi), method="bounded",
                            options=dict(xatol=1e-8))
        best = max(vals[i], -r.fun)
        return float(best), float(r.x if -r.fun >= vals[i] else xs_coarse[i])

    step = 1e-6
    depths = np.arange(0.0, 400e-6 + step / 2, step)
    widths = np.arange(0.0, 400e-6 + step / 2, step)
    F_z = np.array([maxx(0.0, -z)[0] for z in depths]) * s1
    F_y = np.array([maxx(y, 0.0)[0] for y in widths]) * s1
    F_h = np.array([maxx(hatch_m / 2.0, -z)[0] for z in depths]) * s1
    xline = np.arange(-3 * sig, 3e-3, step)
    F_x = np.array([I(x, 0.0, 0.0) for x in xline]) * s1
    return dict(v_mm_s=v_mm_s, depths=depths, widths=widths, F_z=F_z, F_y=F_y, F_h=F_h,
                xline=xline, F_x=F_x)


def _crossing(coord, F, level):
    """Largest coordinate where the decreasing profile F still reaches level (linear interp)."""
    above = np.where(F >= level)[0]
    if above.size == 0:
        return 0.0
    i = above.max()
    if i == F.size - 1:
        return float("inf")
    f0, f1 = F[i], F[i + 1]
    return float(coord[i] + (coord[i + 1] - coord[i]) * (f0 - level) / (f0 - f1))


def geometry(prof, Q, dT_iso):
    """W, D, L, Dh in um and the peak temperature rise in K for absorbed power Q (W)."""
    level = dT_iso / Q
    D = _crossing(prof["depths"], prof["F_z"], level) * 1e6
    half_w = _crossing(prof["widths"], prof["F_y"], level) * 1e6
    Dh = _crossing(prof["depths"], prof["F_h"], level) * 1e6 if prof["F_h"][0] >= level else 0.0
    melt = np.where(prof["F_x"] >= level)[0]
    L = float((prof["xline"][melt.max()] - prof["xline"][melt.min()]) * 1e6) if melt.size else 0.0
    dT_peak = Q * float(prof["F_y"][0])
    return dict(W_um=2 * half_w, D_um=D, L_um=L, Dh_um=Dh, dT_peak_K=dT_peak)


def build_profiles(cfg, mat, speeds, workers=4):
    args = [(v, cfg["beam_radius_um"] * 1e-6, mat["k"], mat["rho"], mat["cp"], cfg["hatch_um"] * 1e-6)
            for v in speeds]
    with ProcessPoolExecutor(workers) as ex:
        res = list(ex.map(_profiles_one, args))
    return {r["v_mm_s"]: r for r in res}


def classify_am_criteria(g, cfg):
    t = cfg["layer_um"]
    lof = g["D_um"] <= t
    lofh = g["Dh_um"] <= t
    return "lof" if lof else ("lof_hatch" if lofh else "none")


def classify_et_default(g, cfg, wdr=2.5):
    t, h = cfg["layer_um"], cfg["hatch_um"]
    W, D, L = g["W_um"], g["D_um"], g["L_um"]
    if D <= 0 or W <= 0:
        return "lack_of_fusion"
    if W / D <= wdr:
        return "keyhole"
    if D <= t or (h / W) ** 2 + t / (t + D) >= 1.0:
        return "lack_of_fusion"
    if L / W >= 2.3 or math.pi * W / L < math.sqrt(2.0 / 3.0):
        return "balling"
    return "defect_free"


def q_crit(prof, dT_iso, fn, lo=1.0, hi=600.0):
    """Smallest absorbed power Q (W) at which fn(geometry) becomes True (bisection; fn monotone)."""
    if not fn(geometry(prof, hi, dT_iso)):
        return float("nan")
    if fn(geometry(prof, lo, dT_iso)):
        return lo
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if fn(geometry(prof, mid, dT_iso)):
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


# --------------------------------------------------------------------------------------------
# Main comparison
# --------------------------------------------------------------------------------------------
def inferred_absorptivity(mp, beam_radius_um):
    """A from the peak of the plotted heat-source intensity, q0 = 2 A P / (pi R^2) (1/e^2 radius R)."""
    R_mm = beam_radius_um * 1e-3
    return mp["q_peak_W_mm2"] * math.pi * R_mm**2 / (2.0 * mp["P"])


def run(args):
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    png_dir = pathlib.Path(args.png_dir)
    summary = {}
    t_start = time.time()
    for key, cfg in MAPS.items():
        pts, bnd, meta = digitize(cfg, png_dir / cfg["png"])
        pts.to_csv(out / f"{key}-am-module-grid-points.csv", index=False)
        bnd.to_csv(out / f"{key}-am-module-boundaries.csv", index=False, float_format="%.2f")
        mp = MELT_POOLS[key]
        A_inf = inferred_absorptivity(mp, cfg["beam_radius_um"])
        dT_pre = cfg["preheat_C"] + 273.15 - T0_ET
        fine_speeds = sorted(set(np.arange(cfg["speeds"][0], cfg["speeds"][-1] + 1, 100).tolist())
                             | set(cfg["speeds"]) | {mp["v_mm_s"]})
        S = dict(digitize=meta, A_inferred=A_inf, materials={})
        for mat in MATERIALS[key]:
            t0 = time.time()
            profs = build_profiles(cfg, mat, fine_speeds, workers=args.workers)
            dT_iso = mat["T_iso"] - (cfg["preheat_C"] + 273.15)  # rise above the preheated plate
            tag = mat["name"]
            # grid points, at the inferred absorptivity and over a sweep
            recs = []
            for A in [A_inf] + list(np.round(np.arange(0.10, 0.701, 0.05), 2)):
                for _, r in pts.iterrows():
                    g = geometry(profs[r.speed_mm_s], A * r.power_W, dT_iso)
                    recs.append(dict(material=tag, A=round(A, 4), power_W=r.power_W, speed_mm_s=r.speed_mm_s,
                                     am_class=r.am_class, marker=r.marker, **{k: round(v, 2) for k, v in g.items()},
                                     T_peak_K=round(g["dT_peak_K"] + cfg["preheat_C"] + 273.15, 1),
                                     et_am_criteria=classify_am_criteria(g, cfg),
                                     et_default=classify_et_default(g, cfg)))
            grid = pd.DataFrame(recs)
            slug = tag.split(",")[1].strip().split()[0] if key == "byu-blend" else "liq"
            grid.to_csv(out / f"{key}-eagar-tsai-grid-{slug}.csv", index=False)
            # boundary absorptivities: A_eff(v) = Q_crit(v) / P_AM(v)
            t, h = cfg["layer_um"], cfg["hatch_um"]
            crit = {
                "lof": lambda g: g["D_um"] > t,
                "lof_hatch": lambda g: g["Dh_um"] > t,
                "et_keyhole_wd2.5": lambda g: g["D_um"] > 0 and g["W_um"] / g["D_um"] <= 2.5,
                "boiling": lambda g: g["dT_peak_K"] + cfg["preheat_C"] + 273.15 >= T_BOIL_AL_K,
            }
            arows = []
            for v in fine_speeds:
                prof = profs[v]
                b = bnd.iloc[(bnd.speed_mm_s - v).abs().argsort()[:3]].mean()
                row = dict(material=tag, speed_mm_s=v, P_am_keyhole_W=b.P_keyhole_W,
                           P_am_lof_hatch_W=b.P_lof_hatch_W, P_am_lof_W=b.P_lof_W)
                for name, fn in crit.items():
                    row[f"Q_{name}_W"] = q_crit(prof, dT_iso, fn)
                row["A_eff_lof"] = row["Q_lof_W"] / b.P_lof_W
                row["A_eff_lof_hatch"] = row["Q_lof_hatch_W"] / b.P_lof_hatch_W
                row["A_eff_keyhole_wd2.5"] = row["Q_et_keyhole_wd2.5_W"] / b.P_keyhole_W
                row["A_eff_keyhole_boiling"] = row["Q_boiling_W"] / b.P_keyhole_W
                arows.append(row)
            aeff = pd.DataFrame(arows)
            aeff.to_csv(out / f"{key}-eagar-tsai-boundary-absorptivity-{slug}.csv", index=False,
                        float_format="%.4f")
            # melt-pool point
            g = geometry(profs[mp["v_mm_s"]], A_inf * mp["P"], dT_iso)
            S["materials"][tag] = dict(
                seconds=round(time.time() - t0, 1),
                meltpool_at_A_inferred={k: round(v, 1) for k, v in g.items()},
                T_peak_K_at_A_inferred=round(g["dT_peak_K"] + cfg["preheat_C"] + 273.15, 1),
                profiles={str(v): None for v in []},
            )
            S["materials"][tag]["profiles_store"] = None
            summary.setdefault(key, S)
            # keep the profiles for plotting
            S["materials"][tag]["_profs"] = profs
            S["materials"][tag]["_grid"] = grid
            S["materials"][tag]["_aeff"] = aeff
            S["materials"][tag]["_dT_iso"] = dT_iso
        S["_pts"], S["_bnd"] = pts, bnd
        summary[key] = S
    summary["_seconds"] = round(time.time() - t_start, 1)
    return summary


def validate(args):
    """Check the profile shortcut against eagar_tsai.compute_single_point at a few points."""
    from eagar_tsai import BeamParameters, MaterialProperties, SimulationDomain, compute_single_point

    cfg = MAPS["alsi10mg"]
    mat = MATERIALS["alsi10mg"][0]
    pts = [(250.0, 900.0, 0.31), (150.0, 1500.0, 0.31), (350.0, 500.0, 0.31), (120.0, 2100.0, 0.5)]
    profs = build_profiles(cfg, mat, sorted({p[1] for p in pts}), workers=args.workers)
    rows = []
    for P, v, A in pts:
        g = geometry(profs[v], A * P, mat["T_iso"] - T0_ET)  # no preheat here: compare like for like
        r = compute_single_point(
            BeamParameters(beam_diameter=cfg["beam_radius_um"] * 1e-6, power=P, velocity=v * 1e-3, absorptivity=A),
            MaterialProperties(liquidus_temperature=mat["T_iso"], thermal_conductivity=mat["k"],
                               density=mat["rho"], specific_heat=mat["cp"]),
            SimulationDomain(spatial_resolution_um=1.0), full_field=False)
        rows.append(dict(P=P, v=v, A=A,
                         W_profile=round(g["W_um"], 1), W_et=round(r.width * 1e6, 1),
                         D_profile=round(g["D_um"], 1), D_et=round(r.depth * 1e6, 1),
                         L_profile=round(g["L_um"], 1), L_et=round(r.length * 1e6, 1),
                         Tpk_profile=round(g["dT_peak_K"] + T0_ET, 1), Tpk_et=round(r.peak_temperature, 1)))
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "profile-shortcut-vs-compute_single_point.csv", index=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["digitize", "validate", "all"])
    ap.add_argument("--png-dir", default="arroyave-orchid-tools/eagar-tsai/am-module-inhouse")
    ap.add_argument("--out", default="arroyave-orchid-tools/eagar-tsai/am-module-inhouse")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    if args.cmd == "digitize":
        for key, cfg in MAPS.items():
            pts, bnd, meta = digitize(cfg, pathlib.Path(args.png_dir) / cfg["png"])
            print(key, meta)
            print(pts.pivot(index="power_W", columns="speed_mm_s", values="am_class").iloc[::-1].to_string())
            print(pts.pivot(index="power_W", columns="speed_mm_s", values="marker").iloc[::-1].to_string())
    elif args.cmd == "validate":
        validate(args)
    else:
        import plot_am_inhouse  # noqa: F401  (plots live in a sibling module)


if __name__ == "__main__":
    main()
