"""Optics chain of the fast-track LPBF with real numbers (#260).

IPG YLR-400-SM (1070 nm, M2 <= 1.1) -> collimator (5 mm, or 7.5 mm) -> SCANLAB hurrySCAN 25 -> LINOS F-Theta-Ronar
4401-288-000-20 (f = 254 mm) -> beam tube -> fused-silica window (Ø50.8 x 9.53) and cover slide (Ø50 x 1) -> the
Ø40 plate, in the box (FT-0 / FT-1) and in the cube (FT-1V).

  A  inputs, each with its source
  B  spot and Rayleigh range
  C  field geometry: scan angles, telecentricity, spot elongation, focus shift; the window's lateral shift
  D  footprint and irradiance on the window and cover slide; a layer's time-averaged irradiance map
  E  clear apertures needed against the CAD's openings, for the centred and the offset field
  F  thermal lens of the window and the cover slide (clean, dirty), static beam and scanned layer
  G  back-reflection: plane-surface ghosts, the specular plate or melt at focus (cat's eye), and the offset field

Units: mm, W, rad unless stated. Heights are above the powder plane (the bed), in the frame of cad/ft_model.py.
Run: python desktop-lpbf/fast-track/process/optics.py      (writes out/optics.json, out/optics.md, img/*.png)
     /tmp/tools/capmem 1 python desktop-lpbf/fast-track/process/optics.py --check-cad   (compares heights with ft_model)
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
IMG = HERE / "img"

# ---------------------------------------------------------------------------------------------------------------
# A. Inputs
# ---------------------------------------------------------------------------------------------------------------
LAM = 1.070e-3            # mm
M2_MAX, M2_TYP = 1.1, 1.05
P_LASER = 400.0
F = 254.4                 # mm, LINOS 4401-288-000-20 EFL (datasheet 2021.12-V4)
LINOS = dict(EFL=254.4, BFL=299.1, WD=296.2, FFL=344.8, beam_design=20.0, m1=25.6, m2=23.0, m2_mech=18.5,
             scan_angle_deg=17.7, field=157.0, spot_um_20mm=25.0, T=0.96, LIDT_J_cm2_9ns=10.0,
             body=(119.8, 69.2), above_flange=20.5, ghosts_from_first_surface=(14.2, 19.6, 52.6, 71.3, 72.4, 142.8, 457.8))
# heights above the focus (air, no plates): flange A at FFL; entrance face 20.5 above A; first surface m2 - m2_mech
# = 4.5 mm inside the entrance face; M2 23.0 and M1 48.6 mm before the first surface; entrance pupil midway
Z_FIRST = LINOS["FFL"] + LINOS["above_flange"] - (LINOS["m2"] - LINOS["m2_mech"])        # 360.8
Z_EP = Z_FIRST + LINOS["m2"] + LINOS["m1"] / 2                                            # 396.6
HEAD = dict(angle_galvo1=0.26, angle_galvo2=0.40, tracking_ms=0.50, aperture=25.0, housing=(206.9, 140.0, 180.0),
            power_W=1500.0)
N_FS = 1.4496             # fused silica at 1070 nm (Malitson 1965)
BEAMS = (5.0, 7.5)        # mm, IPG standard collimated beams (1/e2)
FIELD_R = 20.0            # Ø40 plate
USABLE_R = 15.0           # Ø30 build area
SRC = {
    "ipg": "IPG YLR-SM: 1070 nm, M2 1.05 typ / 1.1 max, standard collimators 5 mm and 7.5 mm (desktop-lpbf/quotes/"
           "ipg-ylr-500-u3-sm-ac.md, IPG spec G22-29856 as transcribed); bare QBH divergence 130-150 mrad full angle",
    "cad": "cad/ft_model.py P and levels(): window ring on the lid (box) or the top plate (cube); window 2 mm above the "
           "ring's underside; cover slide 5.5 mm under the holder top; openings: holder Ø40, clamp and window rings Ø44, "
           "lid and top-plate bores Ø53, beam tube Ø54",
    "window": "Edmund Optics 38-990: Ø50.80 x 9.53 mm fused silica, 1064 nm V-coat, clear aperture Ø45.72 (PR 266 "
              "analysis/optics/beam_path.py, read 2026-11-25)",
    "slide": "cover slide Ø50 x 1 mm (cad/ft_model.py); clear aperture assumed Ø45 (est.)",
    "linos": "LINOS F-Theta-Ronar 4401-288-000-20 datasheet O-LM_DS-4401-288-000-20_2021.12-V4 (Excelitas, via "
             "Digi-Key): EFL 254.4, BFL 299.1, WD 296.2, FFL 344.8, design beam 20 mm, mirrors m1 25.6 / m2 23.0 "
             "(m2 mech 18.5), +-17.7 deg, field 157 x 157, T > 96 %, LIDT 10 J/cm2 at 9 ns, back-reflex foci 14.2, "
             "19.6, 52.6, 71.3, 72.4, 142.8, 457.8 mm from the first surface; no telecentricity or CW rating given",
    "head": "SCANLAB hurrySCAN 25 (scanlab.de/en/print-product/609): 25 mm aperture, +-0.26 rad (galvo 1) and +-0.40 "
            "rad (galvo 2) optical, tracking error 0.50 ms, 1500 W at 1064 nm, housing 206.9 x 140 x 180 mm, 5.8 kg; "
            "this unit's SCANcheck sticker is dated 2003 (lead, from the listing photos)",
    "silica": "Corning 7980: k 1.38 W/mK, dn/dT 9.6e-6 /K, alpha 0.52e-6 /K, nu 0.16, rho 2201, c 740 (as in PR 266 "
              "analysis/optics/thermal_lens.py)",
}

# CAD heights (copied from ft_model.P and the formulas in levels() and build(); --check-cad compares them)
CADP = dict(deck_t=10.0, so_l=12.7, well_h=40.0, box_in_z=8 * 25.4, box_t=1.9, gasket=1.0, cube_frame=12 * 25.4,
            cube_plate_t=22.9, cube_boss=7.6, window_t=9.53, lens_wd=300.0, lens_l=66.0)


def stack(state: str) -> dict:
    """Heights above the bed of the window, cover slide and every opening the beam passes, for 'box' or 'cube'."""
    c = CADP
    bf = c["deck_t"] + c["so_l"] + c["well_h"]                    # 62.7
    if state == "box":
        dz = 0.0
        roof_in = -bf + c["box_in_z"]                             # 140.5
        lid_z0 = roof_in + c["gasket"]                            # 141.5
        z = lid_z0 + c["box_t"]                                   # 143.4: window ring on the lid
        cs_top = roof_in - 6.0
    else:
        dz = c["cube_plate_t"] - c["box_t"]                       # 21.0
        floor_top = -bf + dz
        c0 = floor_top - c["cube_boss"] + c["cube_frame"] / 2
        roof_in = c0 + c["cube_frame"] / 2 - c["cube_boss"]       # 247.9 (world)
        z = roof_in + c["cube_plate_t"]                           # 270.8 (world)
        cs_top = roof_in
    lens_bot = c["lens_wd"] + dz
    col_z0 = lens_bot - 14.0
    ap = []
    ap.append(("cover-slide holder (under the slide)", cs_top - 10, cs_top - 5.6, 20.0))
    ap.append(("cover-slide holder (over the slide)", cs_top - 4.4, cs_top, 20.0))
    if state == "box":
        ap.append(("inner clamp ring", lid_z0 - 6, lid_z0, 22.0))
        ap.append(("lid bore", lid_z0, z, 26.5))
    else:
        ap.append(("top-plate bore", roof_in, z, 26.5))
    ap.append(("window ring ledge", z, z + 2, 22.0))
    ap.append(("window clear aperture", z + 2, z + 2 + c["window_t"], 45.72 / 2))
    ap.append(("retaining flange", z + 11.7, z + 16, 22.0))
    ap.append(("beam tube", z + 16, col_z0, 27.0))
    out = dict(state=state, dz=dz, slide=(cs_top - 5.5 - dz, cs_top - 4.5 - dz),
               window=(z + 2 - dz, z + 2 + c["window_t"] - dz), lens_bot=lens_bot - dz,
               apertures=[(n, a - dz, b - dz, r) for (n, a, b, r) in ap])
    return out


STACKS = {s: stack(s) for s in ("box", "cube")}


def check_cad():
    sys.path.insert(0, str(HERE.parent / "cad"))
    import ft_model as M  # noqa: E402  (CadQuery import: ~0.6 GB, run under capmem)
    for st, name in (("box", "FT-1"), ("cube", "FT-1V")):
        L = M.levels(name)
        parts = {p.name: p.shape.BoundingBox() for p in M.build(name)}
        w = [b for n, b in parts.items() if n.startswith("Window,")][0]
        s = [b for n, b in parts.items() if n.startswith("Cover slide")][0]
        print(name, "window z", round(w.zmin - L["dz"], 2), round(w.zmax - L["dz"], 2), "here", STACKS[st]["window"],
              "| slide z", round(s.zmin - L["dz"], 2), round(s.zmax - L["dz"], 2), "here", STACKS[st]["slide"])


# ---------------------------------------------------------------------------------------------------------------
# B. Spot
# ---------------------------------------------------------------------------------------------------------------
def spot_d(D, m2=M2_MAX, f=F):
    return 4 * m2 * LAM * f / (math.pi * D)


def z_rayleigh(D, m2=M2_MAX, f=F):
    w0 = spot_d(D, m2, f) / 2
    return math.pi * w0 ** 2 / (m2 * LAM)


def w_at(D, h, m2=M2_MAX, f=F):
    """1/e2 radius of the focused beam h (air-equivalent) from the focus."""
    w0 = spot_d(D, m2, f) / 2
    return w0 * math.sqrt(1 + (h / z_rayleigh(D, m2, f)) ** 2)


def air_height(st, h):
    """Air-equivalent height above the focus of a plane at real height h (glass below it counts t(1 - 1/n) less)."""
    red = 0.0
    for (a, b) in (st["slide"], st["window"]):
        if h >= b:
            red += (b - a) * (1 - 1 / N_FS)
        elif h > a:
            red += (h - a) * (1 - 1 / N_FS)
    return h - red


# ---------------------------------------------------------------------------------------------------------------
# C. Field geometry
# ---------------------------------------------------------------------------------------------------------------
# Chief-ray angle on the bed u = k * theta, theta = r / f the optical scan angle. A thin lens with the stop (the scan
# mirrors) d in front of it gives k = 1 - d / f; the exit pupil then sits f / k above the focus. The LINOS lens's
# pupil distance sets k (README); the CAD's envelope pivots at the lens top, 366 mm, i.e. k = 0.69. Range used:
# LINOS: entrance pupil 396.6 mm above the focus; the front principal plane lies somewhere between the first surface
# (360.8) and the lens bottom (296.2), not given: k = 1 - (Z_EP - z_H) / f = 0.86 ... 0.60.
K_RANGE = (0.60, 0.86)
K_MID = 0.73                  # principal plane mid-lens (est.)


def field_row(r, k, D=5.0):
    th = r / F
    u = k * th
    zr = z_rayleigh(D)
    sag = r ** 2 / (2 * F)                               # focus surface of an uncorrected lens (bound, not the LINOS)
    t_w = CADP["window_t"]
    lat_w = t_w * math.sin(u) * (1 - math.cos(u) / math.sqrt(N_FS ** 2 - math.sin(u) ** 2))   # lateral shift, window
    lat_s = 1.0 * math.sin(u) * (1 - math.cos(u) / math.sqrt(N_FS ** 2 - math.sin(u) ** 2))
    return dict(r_mm=r, k=k, theta_opt_deg=math.degrees(th), theta_mech_deg=math.degrees(th) / 2,
                u_deg=math.degrees(u), elongation_pct=100 * (1 / math.cos(u) - 1),
                sag_uncorrected_mm=sag, sag_over_zR=sag / zr, growth_at_sag_pct=100 * (math.sqrt(1 + (sag / zr) ** 2) - 1),
                lateral_shift_window_um=1e3 * lat_w, lateral_shift_slide_um=1e3 * lat_s,
                xy_shift_per_100um_height_um=100 * math.tan(u))


def plates_focus_shift(u=0.0):
    """Longitudinal focus shift (mm, away from the lens) from the window and the slide for a ray at angle u."""
    t = CADP["window_t"] + 1.0
    return t * (1 - math.cos(u) / math.sqrt(N_FS ** 2 - math.sin(u) ** 2))


# ---------------------------------------------------------------------------------------------------------------
# D/E. Footprints and apertures
# ---------------------------------------------------------------------------------------------------------------
def chief_xy(x, y, h, k, axis=(0.0, 0.0)):
    """Chief-ray position at height h for the bed point (x, y), lens axis at `axis` (exit pupil f/k above focus)."""
    s = 1 - h * k / F
    return axis[0] + (x - axis[0]) * s, axis[1] + (y - axis[1]) * s


def envelope(st, k, D, axis=(0.0, 0.0), R=FIELD_R, clip=2.0, margin=2.0):
    """For each opening: the radius the beam needs (2 w: < 0.04 % of the power outside) plus `margin`, measured
    from the opening's best centre (the footprint's centre at that height) and from the lens axis."""
    rows = []
    ang = np.linspace(0, 2 * math.pi, 361)
    for (name, a, b, r_av) in st["apertures"]:
        need_c, need_ax, cen = 0.0, 0.0, (0.0, 0.0)
        for h in (a, b):
            ha = air_height(st, h)
            w = w_at(D, ha)
            xs, ys = chief_xy(R * np.cos(ang), R * np.sin(ang), ha, k, axis)
            cx, cy = (xs.max() + xs.min()) / 2, (ys.max() + ys.min()) / 2
            rc = float(np.max(np.hypot(xs - cx, ys - cy))) + clip * w
            rax = float(np.max(np.hypot(xs - axis[0], ys - axis[1]))) + clip * w
            if rc > need_c:
                need_c, cen = rc, (cx, cy)
            need_ax = max(need_ax, rax)
        rows.append(dict(opening=name, z0=a, z1=b, r_available=r_av, r_needed_centred_on_footprint=need_c + margin,
                         footprint_centre=cen, r_needed_about_lens_axis=need_ax + margin))
    return rows


def surface_irradiance(st, D, P=P_LASER):
    rows = []
    for nm, (a, b) in (("cover slide", st["slide"]), ("window", st["window"])):
        for face, h in (("lower face", a), ("upper face", b)):
            ha = air_height(st, h - 1e-9) if face == "lower face" else air_height(st, h)
            w = w_at(D, ha)
            rows.append(dict(element=nm, face=face, h_mm=h, h_air_mm=ha, beam_d_mm=2 * w,
                             peak_kW_cm2=2 * P / (math.pi * (w / 10) ** 2) / 1e3,
                             mean_kW_cm2=P / (math.pi * (w / 10) ** 2) / 1e3))
    return rows


def layer_irradiance_map(st, D, k, axis, npz, layer=0, h=None, pix=0.1, half=26.0):
    """Time-averaged irradiance (W/cm2) of one layer on the plane at height h (default: cover slide lower face),
    from the build file's vectors, over the layer period; also the dwell-weighted peak."""
    sys.path.insert(0, str(HERE))
    import scan_program as SPG  # noqa: E402
    segs, kinds, pidx, ptr, meta = SPG.load_build(npz)
    parts = [SPG.Part(**p) for p in meta["parts"]]
    psets = {kk: SPG.ParamSet(**v) for kk, v in meta["psets"].items()}
    tm = SPG.Timing(**meta["timing"])
    a, b = ptr[layer], ptr[layer + 1]
    lt = SPG.layer_time(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, tm)
    period = lt["t_list"] + SPG.recoat_time(SPG.Recoat(), SPG.X_LSM100B, next(iter(psets.values())).layer)["t_recoat"]
    h = st["slide"][0] if h is None else h
    ha = air_height(st, h)
    w = w_at(D, ha)
    xs, ys, wts = [], [], []
    for s, kd, ii in zip(segs[a:b], kinds[a:b], pidx[a:b]):
        ps = psets[parts[ii].pset]
        P, v = (ps.P_hatch, ps.v_hatch) if kd == 0 else (ps.P_contour, ps.v_contour)
        L = math.hypot(s[2] - s[0], s[3] - s[1])
        n = max(int(L / 0.02), 1)
        t = (np.arange(n) + 0.5) / n
        x = s[0] + (s[2] - s[0]) * t
        y = s[1] + (s[3] - s[1]) * t
        cx, cy = chief_xy(x, y, ha, k, axis)
        xs.append(cx); ys.append(cy); wts.append(np.full(n, P * (L / v) / n))
    xs, ys, wts = np.concatenate(xs), np.concatenate(ys), np.concatenate(wts)
    edges = np.arange(-half, half + pix / 2, pix)
    Hm, _, _ = np.histogram2d(xs, ys, bins=[edges, edges], weights=wts)       # J per pixel
    from scipy.ndimage import gaussian_filter
    Hm = gaussian_filter(Hm, sigma=(w / 2) / pix, mode="constant")              # the beam's footprint (sigma = w/2)
    Imap = Hm / period / (pix / 10) ** 2                                         # W/cm2, layer-averaged
    return dict(edges=edges, I=Imap, w=w, h=h, h_air=ha, period=period, E=float(wts.sum()),
                I_peak_inst=2 * P_LASER / (math.pi * (w / 10) ** 2))


# ---------------------------------------------------------------------------------------------------------------
# F. Thermal lens (axisymmetric finite volumes, after PR 266's analysis/optics/thermal_lens.py)
# ---------------------------------------------------------------------------------------------------------------
FS = dict(k=1.38, dndT=9.6e-6, alpha=0.52e-6, nu=0.16, n=N_FS, rho=2201.0, c=740.0)
FS["chi"] = FS["dndT"] + (FS["n"] - 1) * (1 + FS["nu"]) * FS["alpha"]


def solve_disc(R, t, w, P_abs, where="bottom", h_face=10.0, nr=200, nz=20):
    """Steady r-z conduction in a disc (SI). Rim held at the mount temperature; faces lose h_face (W/m2K).
    Source: Gaussian of 1/e2 radius w with P_abs, in the bottom cell layer ('bottom') or through the bulk.
    Returns r (m), OPD(r) (m), centre temperature rise (K)."""
    k = FS["k"]
    dr, dz = R / nr, t / nz
    rc = (np.arange(nr) + 0.5) * dr
    N = nr * nz
    I, J = np.meshgrid(np.arange(nr), np.arange(nz))
    I, J = I.ravel(), J.ravel()
    p = J * nr + I
    rows, cols, vals = [], [], []
    diag = np.zeros(N)
    # radial neighbours
    for di in (-1, 1):
        ii = I + di
        rf = rc[I] + di * dr / 2
        A = 2 * math.pi * rf * dz
        g = k * A / dr
        inside = (ii >= 0) & (ii < nr)
        rows += [p[inside]]; cols += [(J * nr + ii)[inside]]; vals += [-g[inside]]
        diag[inside] += g[inside]
        rim = ii == nr
        diag[rim] += (k * A / (dr / 2))[rim]
    for dj in (-1, 1):
        jj = J + dj
        A = 2 * math.pi * rc[I] * dr
        g = k * A / dz
        inside = (jj >= 0) & (jj < nz)
        rows += [p[inside]]; cols += [(jj * nr + I)[inside]]; vals += [-g[inside]]
        diag[inside] += g[inside]
        face = ~inside
        diag[face] += (1.0 / (1.0 / (h_face * A) + (dz / 2) / (k * A)))[face]
    rows.append(p); cols.append(p); vals.append(diag)
    A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N))
    q = P_abs * 2 / (math.pi * w ** 2) * np.exp(-2 * rc ** 2 / w ** 2)
    Af = 2 * math.pi * rc * dr
    b = np.zeros(N)
    if where == "bulk":
        b[:] = np.tile(q * Af / nz, nz)
    else:
        b[:nr] = q * Af
    T = spla.spsolve(A.tocsc(), b).reshape(nz, nr)
    opd = FS["chi"] * T.sum(axis=0) * dz
    return rc, opd, float(T[:, 0].mean())


def fit_defocus(r, opd, w):
    """Gaussian-weighted fit OPD ~ a + b r^2 over the beam; lens power D = -2 b (1/m)."""
    wt = np.exp(-2 * r ** 2 / w ** 2) * r
    X = np.vstack([np.ones_like(r), r ** 2]).T
    sw = np.sqrt(wt)
    a, bb = np.linalg.lstsq(sw[:, None] * X, sw * opd, rcond=None)[0]
    return -2 * bb


def focus_shift_mm(h_mm, D_per_m):
    h = h_mm * 1e-3
    return 1e3 * h ** 2 * D_per_m / (1 + h * D_per_m)


ABSORPTION = {
    "clean: 20 ppm/cm bulk + 0.1 % coatings": None,
    "dirty slide: 1 % at the lower face": 0.01,
    "dirty slide: 2 % at the lower face": 0.02,
}


def thermal_lens(D, P_abs_scale=1.0, w_override=None):
    rows = []
    for st in STACKS.values():
        for nm, (a, b), R in (("cover slide Ø50 x 1", st["slide"], 20.0e-3), ("window Ø50.8 x 9.53", st["window"], 22.0e-3)):
            t = (b - a) * 1e-3
            ha = air_height(st, a)
            w = (w_override or w_at(D, ha)) * 1e-3
            for an, frac in ABSORPTION.items():
                if frac is None:
                    a_tot = 20e-6 * (t * 100) + 1e-3
                    where = "bulk"
                elif nm.startswith("window"):
                    continue                                   # the slide takes the soot, not the window
                else:
                    a_tot, where = frac, "bottom"
                Pabs = a_tot * P_LASER * P_abs_scale
                r, opd, Tc = solve_disc(R, t, w, Pabs, where=where)
                Dp = fit_defocus(r, opd, w)
                dz = focus_shift_mm(ha, Dp)
                rows.append(dict(state=st["state"], element=nm, absorption=an, a_tot=a_tot, P_abs_W=Pabs, h_air_mm=ha,
                                 w_mm=w * 1e3, dT_centre_K=Tc, D_per_m=Dp, focus_shift_mm=dz,
                                 x_zR=dz / z_rayleigh(D)))
    return rows


def scanned_lens(st, element, a_tot, D=5.0, k=K_MID, axis=(0.0, 0.0), npz=None, h_face=10.0):
    """Layer-averaged thermal lens while the coupon build scans: the layer's time-averaged irradiance map on the
    element (layer_irradiance_map) times the absorption is the source of a steady 2D thin-plate conduction solve
    (in-plane conduction k t, both faces losing h_face, rim at the mount temperature). OPD = chi t T. The lens
    power seen by the beam at each coupon's image is a Gaussian-weighted paraboloid fit over the beam."""
    from scipy.ndimage import map_coordinates  # noqa: F401
    a, b = st["slide"] if element == "slide" else st["window"]
    t = (b - a) * 1e-3
    Rrim = (HOLDER_R if element == "slide" else 22.0)
    m = layer_irradiance_map(st, D, k, axis, npz, h=a)
    I = m["I"] * 1e4 * a_tot                                     # absorbed W/m2, layer-averaged
    edges = m["edges"]
    pix = (edges[1] - edges[0]) * 1e-3
    xc = (edges[:-1] + edges[1:]) / 2
    X, Y = np.meshgrid(xc, xc, indexing="ij")
    cen = (0.0, STACK_Y[st["state"]]) if axis != (0.0, 0.0) else (0.0, 0.0)   # the recommended stack centre
    inside = np.hypot(X - cen[0], Y - cen[1]) < Rrim
    n = inside.sum()
    idx = -np.ones(X.shape, int)
    idx[inside] = np.arange(n)
    kt = FS["k"] * t
    rows, cols, vals = [], [], []
    diag = np.full(n, 2 * h_face * pix * pix)
    ii, jj = np.nonzero(inside)
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        i2, j2 = ii + di, jj + dj
        ok = (i2 >= 0) & (i2 < X.shape[0]) & (j2 >= 0) & (j2 < X.shape[1])
        nb = np.full(n, -1)
        nb[ok] = idx[i2[ok], j2[ok]]
        diag += kt                                               # every face conducts (to a neighbour or the rim)
        m_in = nb >= 0
        rows.append(idx[ii, jj][m_in]); cols.append(nb[m_in]); vals.append(np.full(m_in.sum(), -kt))
    rows.append(np.arange(n)); cols.append(np.arange(n)); vals.append(diag)
    A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))
    T = np.zeros(X.shape)
    T[inside] = spla.spsolve(A.tocsc(), I[inside] * pix * pix)
    opd = FS["chi"] * t * T
    w = m["w"]
    out = []
    sys.path.insert(0, str(HERE))
    import scan_program as SPG  # noqa: E402
    _, _, _, _, meta = SPG.load_build(npz)
    for p in meta["parts"]:
        px, py = chief_xy(p["cx"], p["cy"], air_height(st, a), k, axis)
        r2 = (X - px) ** 2 + (Y - py) ** 2
        sel = r2 < (2 * w) ** 2
        wt = np.exp(-2 * r2[sel] / w ** 2)
        xx, yy = (X[sel] - px) * 1e-3, (Y[sel] - py) * 1e-3
        Am = np.vstack([np.ones_like(xx), xx, yy, xx ** 2 + yy ** 2]).T
        sw = np.sqrt(wt)
        coef = np.linalg.lstsq(sw[:, None] * Am, sw * opd[sel], rcond=None)[0]
        Dp = -2 * coef[3]
        dz = focus_shift_mm(air_height(st, a), Dp)
        out.append(dict(part=p["name"], D_per_m=Dp, focus_shift_mm=dz, x_zR=dz / z_rayleigh(D)))
    return dict(state=st["state"], element=element, a_tot=a_tot, P_abs_mean_W=float((I * pix * pix).sum()),
                T_max_K=float(T.max()), parts=out, T=T, edges=edges, I=m["I"], w=w, period=m["period"])


def transient_lens(st, element, a_tot, npz, D=5.0, k=None, axis=None, pix=0.15, dt=2.5e-3, periods=2,
                   sample=0.01, h_face=10.0):
    """Within-layer (transient) thermal lens of the slide or window while the first build's layer 1 is scanned.
    2D thin plate, explicit time steps: rho c t dT/dt = k t lap(T) - 2 h T + q, rim (r > the holder radius about the
    stack centre) at the mount temperature. Starts from the steady solution of the layer-averaged source, runs
    `periods` layer periods (scan, then recoat with the laser off) and records, every `sample` s while the laser is
    on, the lens power the beam sees (Gaussian-weighted paraboloid fit of OPD = chi t T over 2w). Returns the time
    series and its statistics against the steady value."""
    k = K_MID if k is None else k
    axis = AXIS if axis is None else axis
    sys.path.insert(0, str(HERE))
    import scan_program as SPG  # noqa: E402
    segs, kinds, pidx, ptr, meta = SPG.load_build(npz)
    parts = [SPG.Part(**p) for p in meta["parts"]]
    psets = {kk: SPG.ParamSet(**v) for kk, v in meta["psets"].items()}
    tm = SPG.Timing(**meta["timing"])
    a, b = ptr[0], ptr[1]
    T_, X_, Y_, P_ = SPG.layer_path(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, tm, dt=1e-4)
    t_list = SPG.layer_time(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, tm)["t_list"]
    period = t_list + SPG.recoat_time(SPG.Recoat(), SPG.X_LSM100B, next(iter(psets.values())).layer)["t_recoat"]
    z0, z1 = st["slide"] if element == "slide" else st["window"]
    th = (z1 - z0) * 1e-3
    ha = air_height(st, z0)
    w = w_at(D, ha)
    cx, cy = chief_xy(X_, Y_, ha, k, axis)
    E_ = P_ * 1e-4 * a_tot                                        # absorbed J per path sample
    cen = (0.0, STACK_Y[st["state"]])
    Rrim = HOLDER_R if element == "slide" else 22.0
    n = int(math.ceil(2 * (Rrim + 1.0) / pix))
    edges_x = cen[0] - (Rrim + 1.0) + np.arange(n + 1) * pix
    edges_y = cen[1] - (Rrim + 1.0) + np.arange(n + 1) * pix
    xc, yc = (edges_x[:-1] + edges_x[1:]) / 2, (edges_y[:-1] + edges_y[1:]) / 2
    Xg, Yg = np.meshgrid(xc, yc, indexing="ij")
    inside = np.hypot(Xg - cen[0], Yg - cen[1]) < Rrim
    from scipy.ndimage import gaussian_filter
    sig_pix = (w / 2) / pix
    pm = pix * 1e-3
    rc_t = FS["rho"] * FS["c"] * th * pm * pm                     # J/K per cell
    G = FS["k"] * th                                              # W/K between neighbours (square cells)
    Hl = 2 * h_face * pm * pm                                     # W/K to the gas, both faces

    def deposit(sel):
        H, _, _ = np.histogram2d(cx[sel], cy[sel], bins=[edges_x, edges_y], weights=E_[sel])
        return gaussian_filter(H, sig_pix, mode="constant")      # J per cell

    # steady state of the layer-averaged source
    q_avg = deposit(np.ones(len(T_), bool)) / period              # W per cell
    idx = -np.ones(Xg.shape, int)
    idx[inside] = np.arange(inside.sum())
    ii, jj = np.nonzero(inside)
    N = len(ii)
    rows, cols, vals = [np.arange(N)], [np.arange(N)], [np.full(N, Hl + 4 * G)]
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb = idx[np.clip(ii + di, 0, n - 1), np.clip(jj + dj, 0, n - 1)]
        okk = nb >= 0
        rows.append(np.arange(N)[okk]); cols.append(nb[okk]); vals.append(np.full(okk.sum(), -G))
    A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N))
    Tm = np.zeros(Xg.shape)
    Tm[inside] = spla.spsolve(A.tocsc(), q_avg[inside])

    def lens_at(Tf, px, py):
        r2 = (Xg - px) ** 2 + (Yg - py) ** 2
        sel = r2 < (2 * w) ** 2
        wt = np.exp(-2 * r2[sel] / w ** 2)
        xx, yy = (Xg[sel] - px) * 1e-3, (Yg[sel] - py) * 1e-3
        Am = np.vstack([np.ones_like(xx), xx, yy, xx ** 2 + yy ** 2]).T
        sw = np.sqrt(wt)
        coef = np.linalg.lstsq(sw[:, None] * Am, sw * FS["chi"] * th * Tf[sel], rcond=None)[0]
        return focus_shift_mm(ha, -2 * coef[3])

    steady = [lens_at(Tm, px, py) for px, py in zip(cx[::2000], cy[::2000])]
    Tf = Tm.copy()
    out_t, out_dz = [], []
    nsteps = int(math.ceil(period / dt))
    lap = np.zeros_like(Tf)
    for per in range(periods):
        next_sample = 0.0
        for s_ in range(nsteps):
            t0, t1 = s_ * dt, (s_ + 1) * dt
            sel = (T_ >= t0) & (T_ < t1)
            src = deposit(sel) if sel.any() else 0.0
            lap[1:-1, 1:-1] = Tf[2:, 1:-1] + Tf[:-2, 1:-1] + Tf[1:-1, 2:] + Tf[1:-1, :-2] - 4 * Tf[1:-1, 1:-1]
            Tf = Tf + (G * lap * dt - Hl * Tf * dt + src) / rc_t
            Tf[~inside] = 0.0
            if per == periods - 1 and sel.any() and t0 >= next_sample:
                j = np.nonzero(sel)[0][-1]
                out_t.append(t1)
                out_dz.append(lens_at(Tf, cx[j], cy[j]))
                next_sample = t0 + sample
    dz = np.array(out_dz)
    return dict(state=st["state"], element=element, a_tot=a_tot, w_mm=w, period_s=period, dt=dt, pix=pix,
                steady_dz_mm=[float(np.min(steady)), float(np.max(steady))],
                transient_dz_mm=dict(mean=float(dz.mean()), p95=float(np.percentile(dz, 95)), max=float(dz.max())),
                x_zR_max=float(dz.max() / z_rayleigh(D)), T_max_K=float(Tf.max()), t=out_t, dz=dz.tolist())


# ---------------------------------------------------------------------------------------------------------------
# G. Back-reflection
# ---------------------------------------------------------------------------------------------------------------
R_AR = 0.0025              # per face, V-coat at 1064-1070 nm (typ. < 0.25 %)
R_BARE = ((N_FS - 1) / (N_FS + 1)) ** 2
T_ROUND = 0.95             # f-theta + window + slide, there and back (est.)
R_AL = 0.90                # polished / machined Al at 1070 nm, specular (bound; bead-blasted plates are diffuse)


def ghost_coupling(h_air, D):
    """Power overlap with the fibre mode of the reflection from a plane at h_air above the focus: a waist 2 h_air
    out of place."""
    zr = z_rayleigh(D)
    return 1.0 / (1.0 + (2 * h_air / (2 * zr)) ** 2)


def cats_eye(r, k, D, R=R_AL, P=P_LASER):
    """Specular flat reflector at focus, at field radius r from the lens axis. Returns the beam's displacement at the
    scanner pupil (mm), the overlap with the fibre mode, and the watts into the core."""
    u = k * r / F
    delta = 2 * u * F
    eta = math.exp(-(delta / (D / 2)) ** 2)
    return delta, eta, R * T_ROUND * P * eta


def offset_for(delta_min, k, D=5.0, R=FIELD_R):
    """Lens-axis offset s that keeps every bed point of the field at a displacement >= delta_min."""
    r_min = delta_min / (2 * k)
    return r_min + R, r_min


def melt_curvature_coupling(Rc_mm, D):
    """Overlap with the incident mode of the beam returned by a curved reflector of radius Rc at the waist.
    Two coaxial Gaussians of equal size w0 at one plane, wavefront curvatures differing by 2/Rc:
    eta = 4 / ((w1/w2 + w2/w1)^2 + (pi w1 w2 / lam')^2 (2/Rc)^2) = 1 / (1 + (z_R / Rc)^2)."""
    return 1.0 / (1.0 + (z_rayleigh(D) / Rc_mm) ** 2)


# ---------------------------------------------------------------------------------------------------------------
def main():
    if "--check-cad" in sys.argv:
        check_cad()
        return
    OUT.mkdir(exist_ok=True)
    IMG.mkdir(exist_ok=True)
    res = dict(sources=SRC, stacks=STACKS)
    res["spot"] = [dict(D_mm=D, M2=m2, spot_um=1e3 * spot_d(D, m2), zR_mm=z_rayleigh(D, m2),
                        dof_5pct_mm=2 * z_rayleigh(D, m2) * math.sqrt(1.05 ** 2 - 1),
                        dz_10pct_mm=z_rayleigh(D, m2) * math.sqrt(1.1 ** 2 - 1))
                   for D in BEAMS for m2 in (M2_TYP, M2_MAX)]
    res["plates_focus_shift_mm"] = plates_focus_shift()
    res["field"] = [field_row(r, k) for r in (15.0, 20.0, 30.0, 40.0, 50.0) for k in K_RANGE + (K_MID,)]
    res["irradiance"] = {f"{s}, D {D} mm": surface_irradiance(STACKS[s], D) for s in STACKS for D in BEAMS}
    res["apertures"] = {}
    for s in STACKS:
        for k in K_RANGE:
            res["apertures"][f"{s}, centred, k {k}"] = envelope(STACKS[s], k, 5.0)
            res["apertures"][f"{s}, axis at y = -30, k {k}"] = envelope(STACKS[s], k, 5.0, axis=(0.0, -30.0))
    res["thermal_static"] = {f"D {D}": thermal_lens(D) for D in BEAMS}
    res["ghosts"] = []
    for s, st in STACKS.items():
        for nm, (a, b) in (("slide", st["slide"]), ("window", st["window"])):
            for face, h in (("lower", a), ("upper", b)):
                ha = air_height(st, h)
                eta = ghost_coupling(ha, 5.0)
                res["ghosts"].append(dict(state=s, surface=f"{nm} {face} face", h_air=ha, eta=eta,
                                          back_W_AR=P_LASER * R_AR, core_W_AR=P_LASER * R_AR * eta,
                                          core_W_bare=P_LASER * R_BARE * eta))
    res["cats_eye"] = [dict(r_mm=r, k=k, D=D, **dict(zip(("delta_mm", "eta", "core_W"), cats_eye(r, k, D))))
                       for D in BEAMS for k in K_RANGE + (K_MID,) for r in (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0)]
    res["offset"] = {f"k {k}": {f"delta {dm} mm": offset_for(dm, k) for dm in (7.0, 10.0, 15.0)} for k in K_RANGE + (K_MID,)}
    res["melt_curvature"] = [dict(Rc_mm=Rc, eta=melt_curvature_coupling(Rc, 5.0)) for Rc in (0.1, 0.3, 1.0, 3.0, 10.0, 100.0)]
    # the lens's own ghosts: where each back-reflex focus sits against the mirrors (M2 23.0, M1 48.6 mm before the
    # first surface); spot on the mirror for a 5 mm beam, geometric, and its irradiance per watt of ghost power
    gh = []
    for g in LINOS["ghosts_from_first_surface"]:
        for mname, x in (("M2", LINOS["m2"]), ("M1", LINOS["m2"] + LINOS["m1"])):
            dmm = max(5.0 * abs(g - x) / g, 2 * LAM * g / (math.pi * 2.5) * 2)
            gh.append(dict(ghost_mm=g, mirror=mname, mirror_mm=x, gap_mm=g - x, spot_d_mm=dmm,
                           W_cm2_per_W=1.0 / (math.pi * (dmm / 20) ** 2)))
    res["lens_ghosts"] = gh
    res["lens_ghost_power_W"] = P_LASER * R_AR
    # the offset field and the optional head tilt
    s_off = abs(AXIS[1])
    off = dict(s_mm=s_off, r_min=s_off - FIELD_R, r_max=s_off + FIELD_R, theta_max_rad=(s_off + FIELD_R) / F,
               head_limit_rad=HEAD["angle_galvo1"], lens_limit_rad=math.radians(LINOS["scan_angle_deg"]))
    for k in K_RANGE:
        off[f"u_deg_k{k}"] = [math.degrees(k * r / F) for r in (s_off - FIELD_R, s_off, s_off + FIELD_R)]
        off[f"delta_mm_k{k}"] = [2 * k * r for r in (s_off - FIELD_R, s_off, s_off + FIELD_R)]
    for tilt in (3.0, 5.0, 10.0):
        dz = FIELD_R * math.tan(math.radians(tilt))
        off[f"tilt_{tilt:g}"] = dict(edge_defocus_mm=dz, spot_growth_pct=100 * (math.sqrt(1 + (dz / z_rayleigh(5.0)) ** 2) - 1),
                                     u_min_deg=[math.degrees(k * (s_off - FIELD_R) / F) + tilt for k in K_RANGE])
    res["offset"] = off
    res["lens_mount"] = dict(flange_above_bed_mm=LINOS["FFL"] + plates_focus_shift(), lens_bottom_above_bed_mm=LINOS["WD"] + plates_focus_shift(),
                             entrance_face_mm=LINOS["FFL"] + LINOS["above_flange"] + plates_focus_shift(),
                             first_surface_mm=Z_FIRST + plates_focus_shift(), EP_mm=Z_EP + plates_focus_shift())
    npz = OUT / "build_first_coupons_15mm.npz"
    res["thermal_scanned"] = []
    keep = {}
    for s, st in STACKS.items():
        for el, a_tot in (("slide", 20e-6 * 0.1 + 1e-3), ("slide", 0.01), ("slide", 0.02),
                          ("window", 20e-6 * 0.953 + 1e-3)):
            r = scanned_lens(st, el, a_tot, axis=AXIS, npz=npz)
            keep[(s, el, a_tot)] = r
            res["thermal_scanned"].append({k: v for k, v in r.items() if k not in ("T", "edges", "I")})
    # within-layer (transient) lens: one run per element at a reference absorption; the model is linear in it
    res["thermal_transient"] = []
    for s, st in STACKS.items():
        for el, a_ref, cases in (("slide", 0.01, (20e-6 * 0.1 + 1e-3, 0.01, 0.02)), ("window", 20e-6 * 0.953 + 1e-3,
                                                                                    (20e-6 * 0.953 + 1e-3,))):
            r = transient_lens(st, el, a_ref, npz)
            for a_tot in cases:
                f = a_tot / a_ref
                res["thermal_transient"].append(dict(
                    state=s, element=el, a_tot=a_tot, period_s=r["period_s"],
                    steady_dz_mm=[x * f for x in r["steady_dz_mm"]],
                    mean_dz_mm=r["transient_dz_mm"]["mean"] * f, p95_dz_mm=r["transient_dz_mm"]["p95"] * f,
                    max_dz_mm=r["transient_dz_mm"]["max"] * f, max_x_zR=r["x_zR_max"] * f, T_max_K=r["T_max_K"] * f))
    (OUT / "optics.json").write_text(json.dumps(res, indent=1, default=float))
    figures(res, keep)
    return res


AXIS = (0.0, -30.0)       # recommended lens axis on the bed: 30 mm in front of the plate centre (README, G)
STACK_Y = {"box": -11.0, "cube": -21.0}   # recommended window-stack centre (y, mm) with the axis offset
HOLDER_R = 22.0           # recommended cover-slide holder opening: Ø44 (drawn Ø40)


def figures(res, keep):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    C1, C2, C3 = "#257de0", "#f47230", "#00b894"
    INK, INK2, GRID = "#191919", "#666666", "#e6e6e6"
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                         "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})
    # ---- scan field and back-reflection ----
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.8), gridspec_kw=dict(width_ratios=[1, 1.25]))
    a1.set_aspect("equal")
    a1.add_patch(Circle((0, 0), 19.9, fc="#f4f4f4", ec=INK2, lw=1.0))
    a1.add_patch(Circle((0, 0), 15.0, fc="none", ec=INK2, lw=0.8, ls="--"))
    for ang in (90, 210, 330):
        a1.add_patch(Circle((17.1 * math.cos(math.radians(ang)), 17.1 * math.sin(math.radians(ang))), 1.9, fc=INK2, ec="none"))
    for (ax_, lab, col) in (((0.0, 0.0), "lens axis, centred (as drawn)", C2), (AXIS, "lens axis, offset 30 mm (recommended)", C1)):
        a1.plot(*ax_, marker="+", ms=12, mew=2, color=col, ls="none", label=lab)
        r7 = offset_for(10.0, K_RANGE[0])[1]
        a1.add_patch(Circle(ax_, r7, fc="none", ec=col, lw=1.5))
    a1.text(0, -2.2, "specular return\nreaches the\ncollimator", ha="center", va="top", fontsize=7, color=INK)
    a1.text(0, 21.5, "Ø40 plate, Ø30 build area, M2 screw heads", ha="center", fontsize=8, color=INK)
    a1.text(offset_for(10.0, K_RANGE[0])[1] + 1.0, -30, f"r < {offset_for(10.0, K_RANGE[0])[1]:.1f} mm", ha="left",
            va="center", fontsize=7.5, color=INK)
    a1.set_xlim(-27, 27); a1.set_ylim(-42, 25)
    a1.set_xlabel("x on the bed (mm)  (+X recoat)"); a1.set_ylabel("y on the bed (mm)  (gas flows +Y)")
    a1.legend(loc="upper left", bbox_to_anchor=(0.0, -0.12), fontsize=7.5, frameon=False, ncol=1)
    a1.grid(color=GRID, lw=0.6)
    a1.set_title("Where the lens axis meets the bed", fontsize=10, color=INK, loc="left")
    r = np.linspace(0.0, 52.0, 400)
    for k, col, ls in ((K_RANGE[0], C1, "-"), (K_MID, C2, "-"), (K_RANGE[1], C3, "-")):
        W = [max(cats_eye(x, k, 5.0)[2], 1e-6) for x in r]
        a2.semilogy(r, W, color=col, lw=2, ls=ls, label=f"telecentricity k = {k} (u = k·r/f)")
    a2.axhline(1.0, color=INK2, lw=0.8, ls=":")
    a2.text(51, 1.25, "1 W", ha="right", fontsize=7.5, color=INK2)
    for (lo, hi, y, lab) in ((0, 20, 1e3, "plate, axis centred: r 0-20 mm"), (10, 50, 1e-4, "plate, axis offset 30 mm: r 10-50 mm")):
        a2.plot([lo, hi], [y, y], color=INK, lw=3, solid_capstyle="butt")
        a2.text(hi + 0.8, y, lab, ha="left" if hi < 40 else "right", va="center" if hi < 40 else "bottom", fontsize=7.5, color=INK)
    a2.set_ylim(1e-6, 1e4)
    a2.set_xlabel("distance r of the scanned point from the lens axis (mm)")
    a2.set_ylabel("W into the fibre core (flat Al at focus, R 0.9, 400 W)")
    a2.grid(color=GRID, lw=0.6, which="major")
    a2.legend(loc="lower left", fontsize=7.5, frameon=False)
    a2.set_title("Specular return into the fibre core (5 mm beam)", fontsize=10, color=INK, loc="left")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(IMG / "scan-field.png", dpi=150)
    plt.close(fig)
    # ---- irradiance on the cover slide during one layer (box, offset axis) ----
    rr = keep[("box", "slide", 0.01)]
    fig, (b1, b2) = plt.subplots(1, 2, figsize=(11.5, 4.9))
    e = rr["edges"]
    ext = (e[0], e[-1], e[0], e[-1])
    im = b1.imshow(rr["I"].T, origin="lower", extent=ext, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
        "b", ["#ffffff", "#cce3fd", "#84b9f3", "#338ced", "#1b64be", "#0e3d7e"]))
    cen = (0.0, STACK_Y["box"])
    b1.add_patch(Circle(cen, HOLDER_R, fc="none", ec=INK, lw=1.0, ls="--"))
    b1.text(cen[0], cen[1] + HOLDER_R + 0.8, "holder opening Ø44 at y = -11 (recommended)", ha="center", fontsize=7.5, color=INK)
    b1.plot(*AXIS, marker="+", ms=10, mew=2, color=C1)
    b1.text(AXIS[0] + 1.5, AXIS[1] - 1.5, "lens axis", fontsize=7.5, color=INK)
    b1.set_xlim(-26, 26); b1.set_ylim(-36, 14)
    cb = fig.colorbar(im, ax=b1, shrink=0.85)
    cb.set_label("W/cm², averaged over the layer period", color=INK)
    b1.set_xlabel("x (mm)"); b1.set_ylabel("y (mm)")
    b1.set_title(f"Cover slide in the box ({STACKS['box']['slide'][0]:.0f} mm up), layer 1, axis offset 30 mm.\n"
                 f"Instantaneous peak at 400 W: {2 * P_LASER / (math.pi * (rr['w'] / 10) ** 2) / 1e3:.1f} kW/cm²",
                 fontsize=9, color=INK, loc="left")
    T = rr["T"]
    im2 = b2.imshow(T.T, origin="lower", extent=ext, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
        "o", ["#ffffff", "#fde3d3", "#f8b58e", "#f47230", "#c4541c", "#7d3410"]))
    b2.add_patch(Circle(cen, HOLDER_R, fc="none", ec=INK, lw=1.0, ls="--"))
    b2.set_xlim(-26, 26); b2.set_ylim(-36, 14)
    cb2 = fig.colorbar(im2, ax=b2, shrink=0.85)
    cb2.set_label("temperature rise (K)", color=INK)
    b2.set_xlabel("x (mm)")
    wz = [p for p in rr["parts"]]
    worst = max(wz, key=lambda p: abs(p["focus_shift_mm"]))
    b2.set_title(f"Its temperature rise with 1 % soot (layer-averaged):\nfocus moves {worst['focus_shift_mm']:.2f} mm "
                 f"({worst['x_zR']:.2f} z_R) at part {worst['part']}", fontsize=9, color=INK, loc="left")
    fig.tight_layout()
    fig.savefig(IMG / "window-irradiance.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
