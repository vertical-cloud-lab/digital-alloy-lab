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

# Properties for eagar-tsai. AlSi10Mg: the Edison values Xavier's sweep uses (#235); MatCalc mc_al
# gives 868.6 K liquidus / 842.7 K solidus for the composition sent to Thermo-Calc
# (arroyave-orchid-tools/pycalphad-al-cu/data/am_module_alloys_mc_al.csv). The blend has no
# measured properties, so it gets the same thermal properties and two isotherms from mc_al: the
# Al-Si eutectic (850 K) and the liquidus (1019 K, primary Si). Which one the AM module puts at the
# pool edge matters for a 24 % Si alloy.
MATERIALS = {
    "alsi10mg": [dict(name="AlSi10Mg, liquidus 867 K", T_iso=867.0, k=110.0, rho=2650.0, cp=1040.0)],
    "byu-blend": [
        dict(name="blend, eutectic 850 K", T_iso=850.0, k=110.0, rho=2650.0, cp=1040.0),
        dict(name="blend, liquidus 1019 K", T_iso=1019.0, k=110.0, rho=2650.0, cp=1040.0),
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
    for m in masks.values():  # the legend's colour swatches are not regions
        m[max(lg[2] - 3, 0): lg[3] + 4, max(lg[0] - 3, 0): lg[1] + 4] = False
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
# eagar-tsai response profiles (temperature rise per watt of absorbed power)
# --------------------------------------------------------------------------------------------
PROFILE_STEP_M = 1e-6
PROFILE_DEPTH_M = 700e-6


def _profiles_one(args):
    v_mm_s, beam_d_m, k, rho, cp, hatch_m = args
    from eagar_tsai._core import _INTEGRAND  # compiled LowLevelCallable when built from source

    v = v_mm_s * 1e-3
    alpha = k / (rho * cp)
    sig = math.sqrt(2.0) * beam_d_m / 2.0  # eagar-tsai's internal sigma (BeamParameters.sigma)
    p = alpha / (v * sig)
    s1 = 1.0 / (math.pi * (k / alpha) * math.sqrt(math.pi * alpha * v * sig**3))  # K per absorbed W
    zs = math.sqrt(alpha * sig / v)

    def integral(x, y, z):
        return quad(_INTEGRAND, 0.0, np.inf, args=(x / sig, y / sig, z / zs, p))[0]

    xs_coarse = np.concatenate([np.linspace(-3 * sig, 2 * sig, 21), np.geomspace(2.2 * sig, 4e-3, 45)])

    def max_over_x(y, z):
        vals = np.array([integral(x, y, z) for x in xs_coarse])
        i = int(vals.argmax())
        lo, hi = xs_coarse[max(i - 1, 0)], xs_coarse[min(i + 1, xs_coarse.size - 1)]
        r = minimize_scalar(lambda x: -integral(x, y, z), bounds=(lo, hi), method="bounded",
                            options=dict(xatol=1e-9))
        return float(max(vals[i], -r.fun))

    coords = np.arange(0.0, PROFILE_DEPTH_M + PROFILE_STEP_M / 2, PROFILE_STEP_M)
    F_z = np.array([max_over_x(0.0, -z) for z in coords]) * s1  # centre line, vs depth
    F_y = np.array([max_over_x(y, 0.0) for y in coords]) * s1  # surface, vs half-width
    F_h = np.array([max_over_x(hatch_m / 2.0, -z) for z in coords]) * s1  # at y = h/2, vs depth
    xline = np.arange(-10 * sig, 4e-3, PROFILE_STEP_M)
    F_x = np.array([integral(x, 0.0, 0.0) for x in xline]) * s1  # surface centre line, vs x
    return dict(v_mm_s=v_mm_s, coords=coords, F_z=F_z, F_y=F_y, F_h=F_h, xline=xline, F_x=F_x)


def build_profiles(cfg, mat, speeds, workers=4):
    args = [(v, cfg["beam_radius_um"] * 1e-6, mat["k"], mat["rho"], mat["cp"], cfg["hatch_um"] * 1e-6)
            for v in speeds]
    with ProcessPoolExecutor(workers) as ex:
        return {r["v_mm_s"]: r for r in ex.map(_profiles_one, args)}


def _crossing(coord, F, level):
    """Largest coordinate at which the decreasing profile F still reaches level (linear interp)."""
    above = np.where(F >= level)[0]
    if above.size == 0:
        return 0.0
    i = above.max()
    if i == F.size - 1:
        return float("inf")
    f0, f1 = F[i], F[i + 1]
    return float(coord[i] + (coord[i + 1] - coord[i]) * (f0 - level) / (f0 - f1))


def geometry(prof, Q, dT_iso):
    """W, D, L, Dh (um) and peak temperature rise (K) for absorbed power Q (W)."""
    level = dT_iso / Q
    c = prof["coords"]
    D = _crossing(c, prof["F_z"], level) * 1e6
    W = 2.0 * _crossing(c, prof["F_y"], level) * 1e6
    Dh = _crossing(c, prof["F_h"], level) * 1e6
    melt = np.where(prof["F_x"] >= level)[0]
    L = float((prof["xline"][melt.max()] - prof["xline"][melt.min()]) * 1e6) if melt.size else 0.0
    return dict(W_um=W, D_um=D, L_um=L, Dh_um=Dh, dT_peak_K=Q * float(prof["F_y"][0]))


def q_crit(prof, dT_iso, fn, lo=0.5, hi=1500.0):
    """Smallest absorbed power Q (W) at which fn(geometry) turns True (bisection; fn monotone in Q)."""
    if not fn(geometry(prof, hi, dT_iso)):
        return float("nan")
    if fn(geometry(prof, lo, dT_iso)):
        return lo
    for _ in range(45):
        mid = 0.5 * (lo + hi)
        if fn(geometry(prof, mid, dT_iso)):
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


# --------------------------------------------------------------------------------------------
# Classification
# --------------------------------------------------------------------------------------------
def class_am_criteria(g, cfg):
    """The AM module's two lack-of-fusion tests applied to eagar-tsai's pool (Dh <= D, so lof implies lof_hatch)."""
    t = cfg["layer_um"]
    if g["D_um"] <= t:
        return "lof"
    if g["Dh_um"] <= t:
        return "lof_hatch"
    return "none"


def class_et_default(g, cfg, wdr=2.5):
    """eagar-tsai's own classifier (eagar_tsai._api._classify_defect, Sheikh et al. 2024)."""
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


AM_TO_ET = {"keyhole": "keyhole", "lof": "lack_of_fusion", "lof_hatch": "lack_of_fusion", "none": "defect_free"}


def inferred_absorptivity(mp, beam_radius_um):
    """A from the peak of the plotted heat-source intensity, q0 = 2 A P / (pi R^2), R the 1/e^2 radius.

    The plotted intensity runs from q0 to q0/e^2 (30574/4138 = 45286/6129 = 7.39), i.e. out to r = R,
    which is what a Gaussian 2AP/(pi R^2) exp(-2 r^2/R^2) drawn over the beam radius gives.
    """
    R_mm = beam_radius_um * 1e-3
    return mp["q_peak_W_mm2"] * math.pi * R_mm**2 / (2.0 * mp["P"])


# --------------------------------------------------------------------------------------------
# Main comparison
# --------------------------------------------------------------------------------------------
def compare(png_dir: pathlib.Path, out: pathlib.Path, workers: int) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    res = {}
    for key, cfg in MAPS.items():
        pts, bnd, meta = digitize(cfg, png_dir / cfg["png"])
        pts.to_csv(out / f"{key}-am-module-grid-points.csv", index=False)
        bnd.to_csv(out / f"{key}-am-module-boundaries.csv", index=False, float_format="%.2f")
        mp = MELT_POOLS[key]
        A_inf = inferred_absorptivity(mp, cfg["beam_radius_um"])
        T_pre = cfg["preheat_C"] + 273.15
        speeds = sorted(set(range(cfg["speeds"][0], cfg["speeds"][-1] + 1, 100)) | {int(mp["v_mm_s"])})
        R = dict(cfg=cfg, pts=pts, bnd=bnd, meta=meta, A_inf=A_inf, variants={})
        for mat in MATERIALS[key]:
            t0 = time.time()
            profs = build_profiles(cfg, mat, speeds, workers)
            dT_iso = mat["T_iso"] - T_pre  # pool edge, as a rise above the preheated plate
            t, h = cfg["layer_um"], cfg["hatch_um"]

            def at(A, P, v):
                g = geometry(profs[v], A * P, dT_iso)
                g["T_peak_K"] = g["dT_peak_K"] + T_pre
                return g

            # grid points over an absorptivity sweep
            recs = []
            A_list = [round(A_inf, 4)] + [round(a, 2) for a in np.arange(0.05, 0.951, 0.01)]
            for A in A_list:
                for r in pts.itertuples():
                    g = at(A, r.power_W, r.speed_mm_s)
                    recs.append(dict(A=A, power_W=r.power_W, speed_mm_s=r.speed_mm_s, am_class=r.am_class,
                                     marker=r.marker, W_um=g["W_um"], D_um=g["D_um"], L_um=g["L_um"],
                                     Dh_um=g["Dh_um"], T_peak_K=g["T_peak_K"],
                                     et_am_criteria=class_am_criteria(g, cfg),
                                     et_default=class_et_default(g, cfg),
                                     et_boiling=g["T_peak_K"] >= T_BOIL_AL_K))
            grid = pd.DataFrame(recs)
            # boundary absorptivity A_eff(v) = Q_crit(v) / P_AM(v)
            crit = {
                "lof": lambda g: g["D_um"] > t,
                "lof_hatch": lambda g: g["Dh_um"] > t,
                "keyhole_wd2.5": lambda g: g["D_um"] > 0 and g["W_um"] / g["D_um"] <= 2.5,
                "boiling": lambda g: g["dT_peak_K"] + T_pre >= T_BOIL_AL_K,
            }
            arows = []
            for v in speeds:
                b = bnd.iloc[(bnd.speed_mm_s - v).abs().argsort()[:3]].mean(numeric_only=True)
                row = dict(speed_mm_s=v, P_am_keyhole_W=b.P_keyhole_W, P_am_lof_hatch_W=b.P_lof_hatch_W,
                           P_am_lof_W=b.P_lof_W)
                for name, fn in crit.items():
                    row[f"Q_{name}_W"] = q_crit(profs[v], dT_iso, fn)
                row["A_eff_lof"] = row["Q_lof_W"] / b.P_lof_W
                row["A_eff_lof_hatch"] = row["Q_lof_hatch_W"] / b.P_lof_hatch_W
                row["A_eff_keyhole_wd2.5"] = row["Q_keyhole_wd2.5_W"] / b.P_keyhole_W
                row["A_eff_keyhole_boiling"] = row["Q_boiling_W"] / b.P_keyhole_W
                arows.append(row)
            aeff = pd.DataFrame(arows)
            # melt-pool point, and the absorptivity that would match each AM dimension
            g_mp = at(A_inf, mp["P"], int(mp["v_mm_s"]))
            match = {}
            for dim, am_val in (("D_um", mp.get("D_um")), ("L_um", mp.get("L_um")),
                                ("W_um", 2 * mp["y_extent_um"] if "y_extent_um" in mp else None),
                                ("T_peak_K", mp["T_peak_K"])):
                if am_val is None:
                    continue
                if dim == "T_peak_K":
                    fn = (lambda val: (lambda g: g["dT_peak_K"] + T_pre >= val))(am_val)
                else:
                    fn = (lambda d, val: (lambda g: g[d] >= val))(dim, am_val)
                Q = q_crit(profs[int(mp["v_mm_s"])], dT_iso, fn)
                match[dim] = dict(am=am_val, A_match=Q / mp["P"])
            R["variants"][mat["name"]] = dict(mat=mat, grid=grid, aeff=aeff, meltpool=g_mp, match=match,
                                              seconds=round(time.time() - t0, 1), slug=mat.get("slug"))
            print(f"{key} / {mat['name']}: {time.time() - t0:.0f} s", flush=True)
        res[key] = R
    return res


def agreement(grid_A: pd.DataFrame) -> dict:
    """Agreement counts at one absorptivity, over the grid points visible on the AM map."""
    vis = grid_A[grid_A.am_class != "hidden"]
    nk = vis[vis.am_class != "keyhole"]
    lofs = nk.et_am_criteria == nk.am_class
    am_kh = vis.am_class == "keyhole"
    return dict(
        visible=int(len(vis)),
        lof_classes_match=int(lofs.sum()), lof_classes_n=int(len(nk)),
        am_keyhole=int(am_kh.sum()),
        et_wd25_keyhole=int((vis.et_default == "keyhole").sum()),
        et_wd25_keyhole_and_am_keyhole=int(((vis.et_default == "keyhole") & am_kh).sum()),
        et_boiling=int(vis.et_boiling.sum()),
        et_boiling_and_am_keyhole=int((vis.et_boiling & am_kh).sum()),
        et_default_match=int((vis.et_default == vis.am_class.map(AM_TO_ET)).sum()),
        et_default_counts=vis.et_default.value_counts().to_dict(),
        am_counts=vis.am_class.value_counts().to_dict(),
    )


def write_outputs(res: dict, out: pathlib.Path) -> dict:
    summary = {}
    for key, R in res.items():
        S = dict(A_inferred=round(R["A_inf"], 4), legend_box_px=R["meta"]["legend_box_px"], variants={})
        for name, V in R["variants"].items():
            slug = "liquidus" if "liquidus" in name or key == "alsi10mg" else "eutectic"
            if key == "alsi10mg":
                slug = "liquidus-867K"
            elif "eutectic" in name:
                slug = "eutectic-850K"
            else:
                slug = "liquidus-1019K"
            V["slug"] = slug
            g = V["grid"]
            # CSVs: grid points at the inferred A and every 0.05; boundary absorptivities
            keep = g[(g.A == round(R["A_inf"], 4)) | (np.isclose((g.A * 100) % 5, 0) & (g.A >= 0.1))]
            keep.round({c: 2 for c in ("W_um", "D_um", "L_um", "Dh_um", "T_peak_K")}).to_csv(
                out / f"{key}-eagar-tsai-grid-{slug}.csv", index=False)
            V["aeff"].to_csv(out / f"{key}-eagar-tsai-boundary-absorptivity-{slug}.csv", index=False,
                             float_format="%.4f")
            # agreement vs A
            curve = []
            for A, gA in g.groupby("A"):
                a = agreement(gA)
                curve.append(dict(A=A, lof_classes_match=a["lof_classes_match"], lof_classes_n=a["lof_classes_n"],
                                  et_default_match=a["et_default_match"], visible=a["visible"],
                                  et_wd25_keyhole_and_am_keyhole=a["et_wd25_keyhole_and_am_keyhole"],
                                  et_wd25_keyhole=a["et_wd25_keyhole"], am_keyhole=a["am_keyhole"]))
            curve = pd.DataFrame(curve).sort_values("A")
            curve.to_csv(out / f"{key}-agreement-vs-absorptivity-{slug}.csv", index=False)
            best = curve.loc[curve.lof_classes_match.idxmax()]
            ae = V["aeff"]
            S["variants"][name] = dict(
                slug=slug,
                at_A_inferred=agreement(g[g.A == round(R["A_inf"], 4)]),
                best_A_lof_classes=float(best.A), best_lof_classes_match=int(best.lof_classes_match),
                A_eff={c: dict(median=round(float(ae[c].median()), 3), min=round(float(ae[c].min()), 3),
                               max=round(float(ae[c].max()), 3), n=int(ae[c].notna().sum()))
                       for c in ["A_eff_lof", "A_eff_lof_hatch", "A_eff_keyhole_wd2.5", "A_eff_keyhole_boiling"]},
                meltpool_at_A_inferred={k: round(v, 1) for k, v in V["meltpool"].items()},
                match={k: {kk: round(vv, 3) for kk, vv in d.items()} for k, d in V["match"].items()},
                seconds=V["seconds"],
            )
        summary[key] = S
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary


INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
SERIES = {"lof": "#2a78d6", "lof_hatch": "#eb6834", "keyhole_wd2.5": "#1baf7a", "keyhole_boiling": "#eda100"}
LABELS = {"lof": "LOF: D = t", "lof_hatch": "LOF hatch: Dh = t", "keyhole_wd2.5": "keyhole: W/D = 2.5",
          "keyhole_boiling": "peak T = Al boiling (2743 K)"}
SHORT = {"lof": "D = t", "lof_hatch": "Dh = t", "keyhole_wd2.5": "W/D = 2.5", "keyhole_boiling": "boiling"}
DASH = {"lof": "-", "lof_hatch": (0, (6, 2)), "keyhole_wd2.5": (0, (1.5, 1.5)), "keyhole_boiling": (0, (6, 2, 1.5, 2))}


def _spread(ys, gap):
    """Nudge label positions apart so no two are closer than gap (keeps order)."""
    order = sorted(range(len(ys)), key=lambda i: ys[i])
    out = list(ys)
    for a, b in zip(order, order[1:]):
        if out[b] - out[a] < gap:
            out[b] = out[a] + gap
    return out


def plot_maps(res: dict, out: pathlib.Path, png_dir: pathlib.Path, blend_variant: str):
    import matplotlib.patheffects as pe

    fig, axes = plt.subplots(1, 2, figsize=(13, 6.4), dpi=130)
    for ax, (key, R) in zip(axes, res.items()):
        cfg = R["cfg"]
        im = np.asarray(Image.open(png_dir / cfg["png"]).convert("RGB"))
        x_lo, x_hi, y_lo, y_hi = cfg["frame"]
        crop = im[y_lo: y_hi + 1, x_lo: x_hi + 1]
        v_lo, P_hi = _px_to_data(cfg, x_lo, y_lo)
        v_hi, P_lo = _px_to_data(cfg, x_hi, y_hi)
        ax.imshow(crop, extent=[v_lo, v_hi, P_lo, P_hi], aspect="auto", alpha=0.8, zorder=0)
        name = next(n for n in R["variants"] if key == "alsi10mg" or blend_variant in n)
        V = R["variants"][name]
        ae = V["aeff"]
        A = R["A_inf"]
        ends = []
        for c, qcol in (("lof", "Q_lof_W"), ("lof_hatch", "Q_lof_hatch_W"),
                        ("keyhole_wd2.5", "Q_keyhole_wd2.5_W"), ("keyhole_boiling", "Q_boiling_W")):
            P = ae[qcol] / A
            ok = (P >= P_lo) & (P <= P_hi)
            ax.plot(ae.speed_mm_s[ok], P[ok], color=SERIES[c], lw=2.0, ls=DASH[c], zorder=4, label=LABELS[c],
                    path_effects=[pe.Stroke(linewidth=4.2, foreground="white"), pe.Normal()])
            if ok.any():
                ends.append([c, float(ae.speed_mm_s[ok].iloc[-1]), float(P[ok].iloc[-1])])
        if ends:
            ys = _spread([e[2] for e in ends], gap=0.035 * (P_hi - P_lo))
            for (c, xe, _), yl in zip(ends, ys):
                ax.annotate(SHORT[c], (xe, yl), xytext=(-4, 0), textcoords="offset points", ha="right",
                            va="center", fontsize=7.5, color=INK, zorder=6,
                            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))
        ax.set_xlim(v_lo, v_hi)
        ax.set_ylim(P_lo, P_hi)
        ax.set_xlabel("Scan speed (mm/s)", color=INK)
        ax.set_ylabel("Laser power (W)", color=INK)
        ttl = cfg["label"] + f"\neagar-tsai at A = {A:.2f}, beam R = {cfg['beam_radius_um']:.0f} µm, " \
              f"t = {cfg['layer_um']:.0f} µm, h = {cfg['hatch_um']:.0f} µm, preheat {cfg['preheat_C']:.0f} °C"
        if key != "alsi10mg":
            ttl += f",\npool edge at the mc_al {blend_variant} ({V['mat']['T_iso']:.0f} K)"
        ax.set_title(ttl, fontsize=8.5, color=INK, loc="left")
        ax.tick_params(colors=INK2, labelsize=8)
        for sp in ax.spines.values():
            sp.set_color(INK2)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, frameon=False, fontsize=8.5,
               title="Lines: eagar-tsai boundaries.  Fills and markers: the Thermo-Calc AM module's own map.",
               title_fontsize=8.5)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(out / "am-module-maps-with-eagar-tsai-boundaries.png")
    plt.close(fig)


def plot_aeff(res: dict, out: pathlib.Path):
    panels = []
    for key, R in res.items():
        for name, V in R["variants"].items():
            panels.append((key, R, name, V))
    fig, axes = plt.subplots(1, len(panels), figsize=(5.0 * len(panels), 4.6), dpi=130, sharey=True)
    for ax, (key, R, name, V) in zip(axes, panels):
        ae = V["aeff"]
        ends = []
        for c, col in (("lof", "A_eff_lof"), ("lof_hatch", "A_eff_lof_hatch"),
                       ("keyhole_wd2.5", "A_eff_keyhole_wd2.5"), ("keyhole_boiling", "A_eff_keyhole_boiling")):
            y = ae[col]
            ok = y.notna()
            if ok.sum() == 0:
                continue
            ax.plot(ae.speed_mm_s[ok], y[ok], color=SERIES[c], lw=2, ls=DASH[c], marker="o", ms=3, label=LABELS[c])
            ends.append([c, float(ae.speed_mm_s[ok].iloc[-1]), float(y[ok].iloc[-1])])
        ys = _spread([e[2] for e in ends], gap=0.04)
        for (c, xe, _), yl in zip(ends, ys):
            ax.annotate(SHORT[c], (xe, yl), xytext=(5, 0), textcoords="offset points", fontsize=7, color=INK2,
                        va="center")
        ax.axhline(R["A_inf"], color=INK2, lw=1, ls=(0, (4, 3)), zorder=1,
                   label="A the AM module applied in its melt-pool render")
        ax.set_title(f"{R['cfg']['label'].split(' (')[0]}, pool edge {name.split(', ', 1)[1]}\n"
                     f"A in the AM module's melt-pool render = {R['A_inf']:.2f}",
                     fontsize=9, loc="left", color=INK)
        ax.set_xlabel("Scan speed (mm/s)", color=INK)
        ax.grid(color=GRID, lw=0.6)
        ax.tick_params(colors=INK2, labelsize=8)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0].set_ylabel("Absorptivity eagar-tsai needs to put\nthe boundary where the AM module has it", color=INK)
    axes[0].set_ylim(0, 0.8)
    for ax in axes:
        ax.set_xlim(right=ax.get_xlim()[1] + 0.12 * (ax.get_xlim()[1] - ax.get_xlim()[0]))
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=5, frameon=False, fontsize=8)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(out / "eagar-tsai-absorptivity-to-match-am-module.png")
    plt.close(fig)


def validate(args):
    """Check the profile shortcut against eagar_tsai.compute_single_point at a few points."""
    from eagar_tsai import BeamParameters, MaterialProperties, SimulationDomain, compute_single_point

    cfg = MAPS["alsi10mg"]
    mat = MATERIALS["alsi10mg"][0]
    pts = [(250.0, 900.0, 0.31), (150.0, 1500.0, 0.31), (350.0, 500.0, 0.31), (120.0, 2100.0, 0.5),
           (375.0, 400.0, 0.38)]
    profs = build_profiles(cfg, mat, sorted({int(p[1]) for p in pts}), workers=args.workers)
    rows = []
    for P, v, A in pts:
        g = geometry(profs[int(v)], A * P, mat["T_iso"] - T0_ET)  # no preheat: like for like
        r = compute_single_point(
            BeamParameters(beam_diameter=cfg["beam_radius_um"] * 1e-6, power=P, velocity=v * 1e-3, absorptivity=A),
            MaterialProperties(liquidus_temperature=mat["T_iso"], thermal_conductivity=mat["k"],
                               density=mat["rho"], specific_heat=mat["cp"]),
            SimulationDomain(spatial_resolution_um=1.0), full_field=False)
        rows.append(dict(P_W=P, v_mm_s=v, A=A,
                         W_profile=round(g["W_um"], 1), W_eagar_tsai=round(r.width * 1e6, 1),
                         D_profile=round(g["D_um"], 1), D_eagar_tsai=round(r.depth * 1e6, 1),
                         L_profile=round(g["L_um"], 1), L_eagar_tsai=round(r.length * 1e6, 1),
                         Tpeak_profile=round(g["dT_peak_K"] + T0_ET, 1), Tpeak_eagar_tsai=round(r.peak_temperature, 1)))
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
    ap.add_argument("--blend-variant", default="eutectic", choices=["eutectic", "liquidus"],
                    help="which pool-edge isotherm the blend panel of the map figure uses")
    args = ap.parse_args()
    png_dir, out = pathlib.Path(args.png_dir), pathlib.Path(args.out)
    if args.cmd == "digitize":
        for key, cfg in MAPS.items():
            pts, bnd, meta = digitize(cfg, png_dir / cfg["png"])
            print(key, meta)
            print(pts.pivot(index="power_W", columns="speed_mm_s", values="am_class").iloc[::-1].to_string())
            print(pts.pivot(index="power_W", columns="speed_mm_s", values="marker").iloc[::-1].to_string())
    elif args.cmd == "validate":
        validate(args)
    else:
        res = compare(png_dir, out, args.workers)
        summary = write_outputs(res, out)
        plot_maps(res, out, png_dir, args.blend_variant)
        plot_aeff(res, out)
        print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
