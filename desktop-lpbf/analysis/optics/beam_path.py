#!/usr/bin/env python3
"""Desktop LPBF optics, beam path end to end (issue #260).

Gaussian beam with M^2 (embedded-Gaussian ABCD with lambda' = M^2 lambda) from the IPG single-mode fibre through the
collimator, the galvo, the f = 160 mm f-theta, the chamber window and the cover slide to the plate. Writes
analysis/out/optics/beam_path.json and beam_path.md (and beam_path.png).

Sections
  A  inputs (each with its source)
  B  fibre -> collimator -> spot, for every collimator option
  C  where the focus lands in the model, and the depth-of-focus budget
  D  apertures: galvo, lens, and the lid stack (field stop, window bores, drawer, lid bore) against the three plates
  E  field geometry: scan angles, angle of incidence, spot elongation, shift from the plates
  F  irradiance and linear power density on every surface, against the published ratings
  G  back-reflection: ghosts from the plane surfaces, return into the fibre, the melt-pool cat's eye
  H  laser safety optics: NOHD per beam state, guard burn-through bounds, eyewear OD (cross-check of safety.md)

Units: mm, W, rad unless stated. Machine frame of cad/lpbf_low.py: z = 0 is the powder plane.
Nothing here uses a lens prescription: the f-theta is a paraxial lens of f = 160 mm whose air focus the model puts at
z = 0 (flange focal length 191.7 mm from the flange shoulder at z = 191.7). Where the answer depends on the lens's
chief-ray angle (not published), it is given as a range.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.special import erfc

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "optics"
OUT.mkdir(parents=True, exist_ok=True)
import sys  # noqa: E402
sys.path.insert(0, str(HERE.parents[1] / "cad"))
import lpbf_low as MODEL  # noqa: E402  (the lens, bridge and galvo heights come from the model's P block)
MP_ = MODEL.P

# ---------------------------------------------------------------------------------------------------------------
# A. Inputs
# ---------------------------------------------------------------------------------------------------------------
SRC = {
    "ipg": "IPG spec G22-29856 rev. 00 for YLR-500-U3-SM-AC, as transcribed in desktop-lpbf/quotes/ipg-ylr-500-u3-sm-ac.md "
           "(1070 nm; M2 1.05 typ / 1.1 max; bare QBH divergence 130/140/150 mrad full angle, 86 %; standard collimators 5 mm or 7.5 mm)",
    "fth": "Thorlabs FTH160-1064 (vendor-lookups.csv, fetched 2026-11-13T23:45Z, https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=6430): "
           "EFL 160 mm, scan field 110.6 x 110.6 mm, max entrance beam 12 mm, WD 182.5 mm, FFL 191.7 mm, AR 1020-1080 nm, "
           "damage threshold given only for pulses (5 J/cm2, 10 ns); drawing stn012046: input aperture 39 mm, Ø75 protective window",
    "bc": "SCANLAB basiCube 20: 20 mm aperture; 1000 W at 1064 nm (README 3.2, https://www.scanlab.de/en/print-product/1061)",
    "model": f"cad/lpbf_low.py (P block and sections 7 and 9): lens output end z {MP_['z_lens0']:.2f} (raised {MP_['focus_shift']} mm), "
             f"nose z {MP_['z_lens0'] + 50.2:.2f}; galvo bottom z {MP_['z_bridge1'] + MP_['galvo_riser']:.2f}, beam input and 2nd mirror z {MP_['z_galvo_m2']:.2f}; "
             f"window Ø50.8 x {MP_['win_t']} fused silica z {MP_['z_win0']:.2f}-{MP_['z_win0'] + MP_['win_t']:.2f} (Edmund 38-990, CA Ø45.72), "
             "flange bore Ø42 below it, retaining ring Ø44 above; field stop Ø36 z 131-136; "
             f"cover slide Ø{MP_['slide_d']:.0f} x {MP_['slide_t']} z {MP_['z_slide0']:.1f}-{MP_['z_slide0'] + MP_['slide_t']:.1f} (Edmund 36-299, 1064 V-coat, CA Ø42.5); "
             f"drawer opening Ø46 z 125.3-{MP_['z_slide0']:.1f}; lid bore Ø56 z 120-125; plates in Ø25.4 / 50.8 / 76.2 bores (2026-11-25: was 8 mm window, 3 mm slide)",
    "edmund": "Edmund Optics 36-299 (Ø50.00 ±0.1 x 2.00 +0.15/-0.00 mm, CA Ø42.50, 1064 nm V-coat, $121 / $103 at 6-25) and 38-990 "
              "(Ø50.80 +0/-0.10 x 9.53 ±0.20 mm, CA Ø45.72, 1064 nm V-coat, $295), product pages fetched 2026-11-25T00:50Z through the lab tunnel",
    "malitson": "Malitson 1965, fused silica Sellmeier (JOSA 55, 1205; refractiveindex.info)",
    "safety": "desktop-lpbf/safety.md section 4 and safety_calcs.py (MPE 5 mW/cm2 for t >= 10 s at 1070 nm, 7 mm pupil, NOHD form)",
}

LAM = 1.070e-3                    # mm
M2_TYP, M2_MAX = 1.05, 1.10
THETA_FULL = (0.130, 0.140, 0.150)  # rad, bare fibre, full angle 86 % (= 1/e2 for a Gaussian)
P_LASER = 500.0
F_FT = 160.0
WD, FFL = 182.5, 191.7
Z_LENS_OUT = MP_["z_lens0"]          # 185.91: raised by the plates' focus shift (was 182.5)
Z_GALVO_IN = MP_["z_galvo_m2"]       # 271.11: the 2nd mirror, the scan pupil (was 272.7)
Z_GALVO_IN_OLD = 272.7               # before 2026-11-23: 10 mm riser, lens not raised
Z_LENS_OUT_OLD = 182.5
Z_HP = Z_LENS_OUT - WD + F_FT        # the lens's rear principal plane (air focus at Z_LENS_OUT - WD)
GALVO_AP = 20.0
LENS_IN_AP = 39.0
LENS_MAX_BEAM = 12.0
PLATES = {"S25": 25.4 / 2, "M50": 50.8 / 2, "L75": 76.2 / 2}
FIELD_HALF = 110.6 / 2


def n_fs(lam_um: float) -> float:
    """Fused silica index, Malitson 1965."""
    l2 = lam_um ** 2
    return math.sqrt(1 + 0.6961663 * l2 / (l2 - 0.0684043 ** 2) + 0.4079426 * l2 / (l2 - 0.1162414 ** 2)
                     + 0.8974794 * l2 / (l2 - 9.896161 ** 2))


N_FS = n_fs(1.070)
# (name, z bottom, z top), fused silica: read from the model (Edmund 36-299 slide and 38-990 window since 2026-11-25)
Z_S0, Z_S1 = MP_["z_slide0"], MP_["z_slide0"] + MP_["slide_t"]
Z_W0, Z_W1 = MP_["z_win0"], MP_["z_win0"] + MP_["win_t"]
PLATES_GLASS = [("cover slide", Z_S0, Z_S1), ("window", Z_W0, Z_W1)]
T_GLASS = sum(b - a for _, a, b in PLATES_GLASS)

# apertures in the lid stack: (name, z_lo, z_hi, diameter)
LID_APS = [("lid bore", 120.0, 125.0, 56.0), ("drawer opening", 125.3, Z_S0, 46.0), ("cover slide clear aperture", Z_S0, Z_S1, 42.5),
           ("field stop", 131.0, 136.0, 36.0), ("window flange bore (below window)", 136.0, Z_W0, 42.0),
           ("window clear aperture", Z_W0, Z_W1, 45.72), ("window retaining ring (above window)", Z_W1 + 0.75, 163.0, 44.0)]
I_FS = [a[0] for a in LID_APS].index("field stop")

# collimator options: name -> beam diameter D (1/e2), or focal length
COLL = {
    "IPG affixed 2.5 mm (drawn from 2026-11-23; YLR series datasheet rev 2/26)": dict(D=2.5),
    "IPG 2.5 mm + Sill S6EXK0012-328 1.2x expander (catalogue, no power rating)": dict(D=3.0),
    "D = 3.2 mm (the ~75 um target; f_c ~ 23 mm: no catalogue part found)": dict(D=3.2),
    "Wavelength COL-1070-D25-F30 (QBH, f = 30 mm; also low-profile.md's label)": dict(fc=30.0),
    "IPG standard, 5 mm beam (drawn until 2026-11-22)": dict(D=5.0),
    "IPG standard, 7.5 mm beam": dict(D=7.5),
}


# ---------------------------------------------------------------------------------------------------------------
# Gaussian helpers (embedded Gaussian, lambda' = M2 * lambda)
# ---------------------------------------------------------------------------------------------------------------
def spot_d(D, f, m2):
    return 4 * m2 * LAM * f / (math.pi * D)


def zr(d_spot, m2):
    w0 = d_spot / 2
    return math.pi * w0 ** 2 / (m2 * LAM)


def w_at(w0, z_r, dz):
    return w0 * math.sqrt(1 + (dz / z_r) ** 2)


def coupling_defocus(sep, z_r):
    """Power overlap of two identical Gaussian modes whose waists are `sep` apart along the axis."""
    return 1.0 / (1.0 + (sep / (2 * z_r)) ** 2)


def coupling_tilt(alpha, w0, m2=1.0):
    """Overlap of two identical Gaussians crossing at angle alpha at the waist (lam' = m2 lam)."""
    return math.exp(-(math.pi * w0 * alpha / (m2 * LAM)) ** 2)


def coupling_offset(dx, w0):
    return math.exp(-(dx / w0) ** 2)


R = {"sources": SRC, "inputs": dict(lambda_nm=1070, M2=[M2_TYP, M2_MAX], theta_full_mrad=[t * 1e3 for t in THETA_FULL],
                                     n_fused_silica_1070=round(N_FS, 5), P_W=P_LASER, f_mm=F_FT)}

# ---------------------------------------------------------------------------------------------------------------
# B. Fibre -> collimator -> spot
# ---------------------------------------------------------------------------------------------------------------
# real-beam waist at the fibre from the far-field divergence: W0 = M2 lam / (pi theta_half)
mfd = {f"{t*1e3:.0f} mrad": 2 * M2_TYP * LAM / (math.pi * t / 2) * 1e3 for t in THETA_FULL}
R["fibre"] = dict(mfd_um_from_divergence=mfd, note="second-moment beam diameter at the fibre end, from IPG's divergence spec with M2 1.05")
rows = []
for name, c in COLL.items():
    for th in THETA_FULL:
        D = c.get("D") or c["fc"] * th
        fc = c.get("fc") or D / th
        for m2 in (M2_TYP, M2_MAX):
            d = spot_d(D, F_FT, m2)
            z = zr(d, m2)
            rows.append(dict(collimator=name, theta_full_mrad=th * 1e3, fc_mm=fc, D_mm=D, M2=m2, spot_um=d * 1e3, zR_mm=z,
                             dof5_mm=z * math.sqrt(1.05 ** 2 - 1), dof10_mm=z * math.sqrt(1.10 ** 2 - 1),
                             spot_f254_um=spot_d(D, 254.0, m2) * 1e3,
                             galvo_clip=math.exp(-2 * (GALVO_AP / 2) ** 2 / (D / 2) ** 2),
                             lens_beam_ok=D <= LENS_MAX_BEAM))
R["collimators"] = rows

# collimator focal length for a wanted spot: d = MFD_real * f / f_c  ->  f_c = 4 M2 lam f / (pi d theta)... use D
need = {}
for d_um in (60, 70, 75, 80, 90, 100):
    D = 4 * M2_MAX * LAM * F_FT / (math.pi * d_um * 1e-3)
    need[d_um] = dict(D_mm=D, fc_mm_at_140=D / 0.140, fc_range=[D / 0.150, D / 0.130])
R["collimator_for_spot"] = need

# ---------------------------------------------------------------------------------------------------------------
# C. Focus position in the model, and the depth-of-focus budget
# ---------------------------------------------------------------------------------------------------------------
shift = sum((b - a) * (1 - 1 / N_FS) for _, a, b in PLATES_GLASS)
d_tol_slide = 0.15 * (1 - 1 / N_FS)        # Edmund 36-299 thickness tolerance +0.15/-0.00 mm (25-250 was +/-0.38)
d_tol_win = 0.20 * (1 - 1 / N_FS)          # Edmund 38-990 thickness tolerance +/-0.20 mm
budget = [
    (f"window {MP_['win_t']} mm + slide {MP_['slide_t']} mm of fused silica in the converging beam (static; take out by raising the lens)", shift, "static"),
    ("cover slide thickness tolerance +0.15/-0.00 mm (Edmund 36-299): focus up to this much lower", d_tol_slide, "per slide"),
    ("window thickness tolerance +/-0.20 mm (Edmund 38-990)", d_tol_win, "once (the burn test takes it out)"),
    ("plate stack growth at 200 C (powder-spreading.md), if the blade is zeroed cold", 0.112, "zero the blade hot"),
    ("bridge posts +50 K (mech.md F)", 0.070, "slow drift"),
]
# the model raises the lens by P["focus_shift"]; check it against this script's own number
Z_FOCUS_DRAWN = (Z_LENS_OUT - WD) - shift          # where the focus lands as drawn (0 = on the powder)
assert abs(MP_["focus_shift"] - shift) < 0.01, f"model raises the lens {MP_['focus_shift']} mm, the plates shift the focus {shift:.3f} mm"
shift_bom = (9.53 + 2.0) * (1 - 1 / N_FS)           # with the optics BOM's glass: Edmund 38-990 window, 36-299 slide (drawn since 2026-11-25)
shift_old = (8.0 + 3.0) * (1 - 1 / N_FS)            # the 8 mm window and 3 mm slide drawn until 2026-11-23
R["focus_shift_mm"] = dict(plates=shift, model_lens_raise=MP_["focus_shift"], focus_as_drawn_z=Z_FOCUS_DRAWN,
                           plates_bom_glass=shift_bom, focus_with_bom_glass_z=(Z_LENS_OUT - WD) - shift_bom,
                           plates_old_8_3=shift_old, shim_nominal_mm=MP_["lens_shim"],
                           lens_travel_mm=dict(up_with_no_shims=MP_["lens_shim"], down_with_6mm_of_shims=6.0 - MP_["lens_shim"]),
                           budget=[dict(item=a, mm=b, kind=c) for a, b, c in budget])
for r in rows:
    r["spot_at_model_focus_um"] = 2 * w_at(r["spot_um"] / 2, r["zR_mm"], Z_FOCUS_DRAWN)
    r["spot_before_raise_um"] = 2 * w_at(r["spot_um"] / 2, r["zR_mm"], shift)

# off-axis: the plates' focus shift along z grows with the chief-ray angle u
def plate_focus_shift_z(u):
    """z-shift of the focus for a plate stack of T_GLASS at chief-ray angle u (paraxial about the chief ray)."""
    s = math.sin(u)
    along = T_GLASS * (1 - math.cos(u) / math.sqrt(N_FS ** 2 - s ** 2))
    return along * math.cos(u)


def plate_lateral_shift(u):
    s = math.sin(u)
    return T_GLASS * s * (1 - math.cos(u) / math.sqrt(N_FS ** 2 - s ** 2))


def plate_astig(u):
    """Sagittal-tangential focal separation from a tilted plate (thin-plate formula, Smith, Modern Optical Engineering)."""
    s2 = math.sin(u) ** 2
    return T_GLASS * (N_FS ** 2 - 1) * s2 / (N_FS ** 2 - s2) ** 1.5


# ---------------------------------------------------------------------------------------------------------------
# D/E. Field geometry and apertures, for a range of chief-ray ratios k = u'/theta (u' = chief-ray angle at the plate)
# ---------------------------------------------------------------------------------------------------------------
KS = (0.3, 0.5, 0.75)
# thin-lens estimate of k: lens at its rear principal plane (160 mm above the focus), stop at the galvo's mirrors (z 272.7)
_d_s = Z_GALVO_IN - Z_HP
_d_xp = _d_s * F_FT / (F_FT - _d_s)          # virtual exit pupil above the lens
K_THIN = F_FT / (F_FT + _d_xp)
Z_NOSE = Z_LENS_OUT + 50.2
Z_H_MID = Z_LENS_OUT + 50.2 / 2
K_RANGE = {f"as drawn (2nd mirror {Z_GALVO_IN - Z_NOSE:.0f} mm above the nose)": (1 - (Z_GALVO_IN - Z_HP) / F_FT, 1 - (Z_GALVO_IN - Z_H_MID) / F_FT),
           "before 2026-11-23 (2nd mirror 40 mm above the nose)": (1 - (Z_GALVO_IN_OLD - F_FT) / F_FT, 1 - (Z_GALVO_IN_OLD - (Z_LENS_OUT_OLD + 25.1)) / F_FT),
           "Thorlabs A1 = 7.5 mm (2nd mirror 7.5 mm above the nose)": (1 - (Z_NOSE + 7.5 - Z_HP) / F_FT, 1 - (Z_NOSE + 7.5 - Z_H_MID) / F_FT)}
K_DRAWN = list(K_RANGE.values())[0]


def chief_r(r_img, k, z):
    """Radius of the chief ray at height z above the plate (straight line, plates ignored: their shift is < 0.6 mm)."""
    th = r_img / F_FT
    return r_img - z * math.tan(k * th)


def beam_w(D, m2, z, z_focus=0.0):
    d = spot_d(D, F_FT, m2)
    return w_at(d / 2, zr(d, m2), z - z_focus)


def clip_fraction(r_c, w, ap_r):
    """Fraction of a Gaussian (1/e2 radius w) centred r_c from the axis lost outside a circle of radius ap_r (edge approx)."""
    s = ap_r - r_c
    return 0.5 * erfc(math.sqrt(2) * s / w)


def max_radius(D, m2, k, ap, loss=1e-3):
    """Largest plate radius whose beam passes aperture `ap` with less than `loss` clipped."""
    name, z0, z1, dia = ap
    lo, hi = 0.0, 60.0
    for _ in range(60):
        mid = (lo + hi) / 2
        worst = max(clip_fraction(abs(chief_r(mid, k, z)), beam_w(D, m2, z) / math.cos(k * mid / F_FT), dia / 2)
                    for z in np.linspace(z0, z1, 6))
        lo, hi = (mid, hi) if worst < loss else (lo, mid)
    return lo


field = []
for k in KS:
    for pl, r in PLATES.items():
        th = r / F_FT
        u = k * th
        field.append(dict(k=k, plate=pl, r_mm=r, scan_optical_deg=math.degrees(th), mirror_mech_deg=math.degrees(th / 2),
                          aoi_deg=math.degrees(u), elongation_pct=100 * (1 / math.cos(u) - 1),
                          plate_lateral_shift_mm=plate_lateral_shift(u), plate_focus_shift_extra_mm=plate_focus_shift_z(u) - shift,
                          plate_astig_mm=plate_astig(u), chief_r_at_slide=chief_r(r, k, (Z_S0 + Z_S1) / 2), chief_r_at_window=chief_r(r, k, (Z_W0 + Z_W1) / 2),
                          chief_r_at_lens_out=chief_r(r, k, Z_LENS_OUT)))
R["field"] = field
R["k_range_thin_lens"] = {k: list(v) for k, v in K_RANGE.items()}
# clear diameter each lid opening needs to pass the L75 edge (r 38.1) with < 0.1 % clipped
need_d = []
for D in (5.0, 3.2):
    for k in (0.3, 0.45, 0.6):
        rec = dict(D_mm=D, k=k)
        for name, z0, z1, dia in LID_APS:
            worst = 0.0
            for z in np.linspace(z0, z1, 6):
                rc = abs(chief_r(38.1, k, z))
                w = beam_w(D, M2_MAX, z) / math.cos(k * 38.1 / F_FT)
                worst = max(worst, rc + 1.55 * w)      # 0.5 erfc(1.55 sqrt2) = 0.1 %
            rec[name] = 2 * worst
        need_d.append(rec)
R["needed_clear_diameter_L75"] = need_d
R["k_thin_lens_estimate"] = dict(k=K_THIN, stop_above_lens_mm=_d_s, exit_pupil_above_lens_mm=_d_xp,
                                 note="thin lens at H' (z 160) with H = H'; the real front principal plane is unknown, so k could be ~0.3-0.8")

aps = []
for cname, D in (("IPG 2.5 mm (drawn)", 2.5), ("IPG 5 mm", 5.0), ("D 3.2 mm", 3.2)):
    for k in KS:
        rec = dict(collimator=cname, k=k)
        for ap in LID_APS:
            rec[ap[0]] = max_radius(D, M2_MAX, k, ap)
        # reach of the field stop: where half the beam still passes (beam centre on the stop edge, at its lowest face)
        rec["field stop: beam centre on the edge (50 % passes)"] = max_radius(D, M2_MAX, k, LID_APS[I_FS], loss=0.5)
        aps.append(rec)
R["apertures"] = aps
# L75 reach as drawn: the drawn k range (thin-lens bounds and their middle), every lid opening, < 0.1 % clipped
reach = []
for cname, D in (("IPG 2.5 mm (drawn)", 2.5), ("D 3.2 mm", 3.2), ("IPG 5 mm", 5.0)):
    for k in (K_DRAWN[0], sum(K_DRAWN) / 2, K_DRAWN[1]):
        per = {ap[0]: max_radius(D, M2_MAX, k, ap) for ap in LID_APS}
        lim = min(per, key=per.get)
        reach.append(dict(collimator=cname, k=k, reach_mm=per[lim], limited_by=lim, per_aperture=per, L75_passes=per[lim] >= 38.1,
                          M50_passes=per[lim] >= 25.4))
R["reach_as_drawn"] = reach
# galvo and lens input apertures: beam walk at the lens nose for a pupil d_p above it
walk = []
for d_p in (30.0, 45.0, 60.0):
    for pl, r in PLATES.items():
        th = r / F_FT
        walk.append(dict(pupil_above_nose_mm=d_p, plate=pl, walk_mm=d_p * math.tan(th), edge_mm_5mm=d_p * math.tan(th) + 2.5 * 1.5,
                         lens_in_radius=LENS_IN_AP / 2))
R["lens_input_walk"] = walk

# ---------------------------------------------------------------------------------------------------------------
# F. Irradiance on every surface at 500 W (lens raised so the focus is on the plate)
# ---------------------------------------------------------------------------------------------------------------
def surf_table(D, m2):
    d = spot_d(D, F_FT, m2)
    z_r = zr(d, m2)
    w0 = d / 2
    out = []
    W = D / 2
    def add(name, w, extra=""):
        out.append(dict(surface=name, beam_d_mm=2 * w, peak_W_cm2=2 * P_LASER / (math.pi * (w / 10) ** 2),
                        linear_W_cm=P_LASER / (2 * w / 10), note=extra))
    add("collimator output lens", W)
    add("shutter mirror / dump (closed)", W, "the dump takes all 500 W")
    add("galvo mirrors (45 deg: the footprint is 1.41x longer, so the surface irradiance is 0.71x this)", W)
    add("f-theta input", W)
    # image space: reduced distance from the focus; glass portions count t/n
    def w_img(z):
        red = z
        for _, a, b in PLATES_GLASS:
            if z > b:
                red -= (b - a) * (1 - 1 / N_FS)
            elif z > a:
                red -= (z - a) * (1 - 1 / N_FS)
        return w_at(w0, z_r, red)
    add(f"f-theta output (protective window, z {Z_LENS_OUT:.1f})", w_img(Z_LENS_OUT))
    add(f"chamber window, top (z {Z_W1:.1f})", w_img(Z_W1))
    add(f"chamber window, bottom (z {Z_W0:.1f})", w_img(Z_W0))
    add(f"cover slide, top (z {Z_S1:.1f})", w_img(Z_S1))
    add(f"cover slide, bottom (z {Z_S0:.1f})", w_img(Z_S0), "the face that fouls")
    add("plate, at focus", w0, "melts")
    return out


R["irradiance"] = {"IPG 5 mm, M2 1.1": surf_table(5.0, M2_MAX), "D 3.2 mm, M2 1.1": surf_table(3.2, M2_MAX)}

# ---------------------------------------------------------------------------------------------------------------
# G. Back-reflection
# ---------------------------------------------------------------------------------------------------------------
R_UNC = ((N_FS - 1) / (N_FS + 1)) ** 2
R_AR = 0.0025          # per surface, a typical V/BBAR coating at the design wavelength (Edmund/Thorlabs quote <0.25-0.5 %)
ghost = []
for D in (5.0, 3.2):
    d = spot_d(D, F_FT, M2_MAX)
    z_r = zr(d, M2_MAX)
    fc = D / 0.140
    for name, h in (("slide bottom", Z_S0), ("slide top", Z_S1), ("window bottom", Z_W0), ("window top", Z_W1),
                    ("f-theta protective window (lower face)", Z_LENS_OUT)):
        # air-equivalent height above the focus
        red = h - sum((b - a) * (1 - 1 / N_FS) for _, a, b in PLATES_GLASS if h >= b)
        eta = coupling_defocus(2 * red, z_r)
        # thin-lens (at H', 160 mm above focus) image of the ghost for the return trip
        obj = 2 * red - F_FT
        v = 1 / (1 / F_FT + 1 / obj) if obj > 0 else float("nan")
        # where the return focuses relative to the fibre end: longitudinal magnification (fc/f)^2
        dz_fib = 2 * red * (fc / F_FT) ** 2
        w_fib = (D / 2) * dz_fib / fc
        ghost.append(dict(D_mm=D, surface=name, height_air_mm=red, core_coupling=eta,
                          returned_W_uncoated=P_LASER * R_UNC * eta, returned_W_AR=P_LASER * R_AR * eta,
                          total_back_W_uncoated=P_LASER * R_UNC, total_back_W_AR=P_LASER * R_AR,
                          ghost_focus_z_thin_lens=F_FT + v if v == v else None,
                          return_focus_from_fibre_mm=dz_fib, return_radius_at_fibre_mm=w_fib))
R["ghosts"] = dict(R_uncoated=R_UNC, R_AR=R_AR, rows=ghost)

# melt-pool cat's eye: a flat specular spot at focus returns into the core when the chief-ray angle u' is below ~the
# beam's own cone half-angle; coupling falls as exp(-(2 u'/theta_b)^2) for a reflected cone tilted by 2u'
cats = []
for D in (5.0, 3.2):
    th_b = D / (2 * F_FT)                       # image-space 1/e2 half-angle
    d = spot_d(D, F_FT, M2_MAX)
    w0 = d / 2
    for k in KS:
        for r in (0.0, 1.0, 2.0, 3.0, 5.0, 8.0, 12.7, 25.4):
            u = k * r / F_FT
            eta = coupling_tilt(2 * u, w0, M2_MAX)
            cats.append(dict(D_mm=D, k=k, r_mm=r, chief_angle_mrad=u * 1e3, beam_half_angle_mrad=th_b * 1e3, core_coupling=eta,
                             returned_W_at_R0p9=0.9 * P_LASER * 0.98 * eta))
R["cats_eye"] = cats

# ---------------------------------------------------------------------------------------------------------------
# H. Laser safety optics (same method and MPE as safety_calcs.py)
# ---------------------------------------------------------------------------------------------------------------
MPE = 5.0e-3   # W/cm2, t >= 10 s, 1070 nm
def nohd(P, phi, a_cm=0.0):
    return (math.sqrt(4 * P / (math.pi * MPE)) - a_cm) / phi / 100.0   # m
saf = []
for D in (5.0, 3.2):
    phi_col = 4 * M2_MAX * LAM / (math.pi * D)                 # full-angle divergence of the collimated beam
    phi_foc = D / F_FT                                          # full angle out of the focus
    saf.append(dict(D_mm=D, collimated_phi_mrad=phi_col * 1e3, NOHD_collimated_km=nohd(P_LASER, phi_col, D / 10) / 1e3,
                    focus_phi_mrad=phi_foc * 1e3, NOHD_focus_m=nohd(P_LASER, phi_foc), NOHD_specular_Al_m=nohd(0.9 * P_LASER, phi_foc)))
R["safety"] = dict(rows=saf, NOHD_bare_fibre_m=nohd(P_LASER, 0.140), NOHD_bare_fibre_m_130=nohd(P_LASER, 0.130),
                   OD_direct=math.log10(P_LASER / (math.pi * 0.35 ** 2) / MPE))
# guard: 1-D lower bound on burn-through of 1.6 mm 5052 (no conduction; all of it heated to melting and fused) at
# distances beyond focus, cold (0.08) and hot (0.4) absorptance, the same model and inputs as safety_calcs.py
rho, c, Tm, L, t = 2680, 900, 607, 389e3, 1.6e-3
E_area = rho * t * (c * (Tm - 25) + L) / 1e4      # J/cm2
burn = []
for D in (5.0, 3.2):
    for dz in (50.0, 150.0, 300.0, 600.0):
        dd = spot_d(D, F_FT, M2_MAX)
        w = w_at(dd / 2, zr(dd, M2_MAX), dz)
        I_avg = 0.865 * P_LASER / (math.pi * (w / 10) ** 2)     # W/cm2 inside the 1/e2 radius
        burn.append(dict(D_mm=D, from_focus_mm=dz, beam_d_mm=2 * w, I_W_cm2=I_avg,
                         t_cold_s=E_area / (0.08 * I_avg), t_hot_s=E_area / (0.4 * I_avg)))
R["guard_burn"] = dict(E_J_cm2=E_area, rows=burn)

# ---------------------------------------------------------------------------------------------------------------
# I. Collimator choice (2026-11-25, optics.md §9.1): what each option does to the process, in numbers
# ---------------------------------------------------------------------------------------------------------------
# The baseline with a known Al process window: EOS M 290 (100 um focus, EOS system datasheet) with AlSi10Mg at 370 W,
# 1300 mm/s, 0.19 mm hatch, 30 um layers (Liu & Gibbons, SFF 2023, on an EOSINT M 280). Keyhole number (Gan et al. 2021,
# Nat. Commun. 12, 2379, doi:10.1038/s41467-021-22704-0): Ke = eta P / ((T_l - T_0) pi rho C_p sqrt(alpha V r0^3));
# conduction < 1.4, transition 1.4-6, keyhole > 6, fitted on Ti-6Al-4V, Al6061 and SS316. Only ratios to the baseline are
# used here, so the absorptivity and the Al properties cancel: Ke ~ P / sqrt(V r0^3).
BASE = dict(name="EOS M 290 / M 280, AlSi10Mg 30 um", d_um=100.0, P=370.0, V=1.3, h=0.19, t=0.030)
V_GALVO = 1.1                 # m/s: basiCube 20 marking speed at f = 160 mm (README §3.1, SCANLAB)
HATCH_PER_SPOT = BASE["h"] / (BASE["d_um"] * 1e-3)      # 1.9: the baseline's hatch / spot, assumed to carry over
COUPON_MM2 = 3 * 10.0 * 10.0  # three 10 x 10 mm screening coupons per layer (README §3.3: "the galvo scans three coupons")
RECOAT_S, JUMP_S = 8.0, 0.2   # recoat cycle and jumps per layer (heat.md)
BUILD_MM = 15.0               # screening build height (README §3.3)
PLATE_GROWTH = 0.112          # mm, plate stack at 200 C (powder-spreading.md)
FILM_ZR = 0.73                # light-film (0.05 %) slide thermal shift in Rayleigh ranges: the same for every beam (thermal_lens.md)
I_BASE = 2 * BASE["P"] / (math.pi * (BASE["d_um"] * 1e-4 / 2) ** 2)     # W/cm2 peak


def ke_ratio(P, V, d_um):
    return (P / BASE["P"]) * math.sqrt(BASE["V"] / V) * (BASE["d_um"] / d_um) ** 1.5


def p_same_ke(V, d_um):
    """Power that gives the baseline's Ke at speed V and spot d."""
    return BASE["P"] * math.sqrt(V / BASE["V"]) * (d_um / BASE["d_um"]) ** 1.5


CHOICE = [
    ("IPG 5 mm affixed (in the quote; drawn until 2026-11-22)", dict(D=5.0)),
    ("Wavelength COL-1070-D25-F30 (QBH, f 30 mm)", dict(fc=30.0)),
    ("custom collimator, f ~ 23 mm (D 3.2 mm)", dict(D=3.2)),
    ("IPG 5 mm + 1.5x Galilean expander used backwards (D 3.33 mm)", dict(D=5.0 / 1.5, extra="2 more lenses in the 500 W beam")),
    ("IPG 2.5 mm + Sill 1.2x expander (D 3.0 mm)", dict(D=3.0, extra="2 more lenses in the 500 W beam")),
    ("IPG 2.5 mm affixed (drawn since 2026-11-23)", dict(D=2.5)),
    ("IPG 5 mm, run out of focus so the powder sees 75 um", dict(D=5.0, defocus_to_um=75.0)),
]
k_mid = sum(K_DRAWN) / 2
choice = []
for name, c in CHOICE:
    D = c.get("D") or c["fc"] * 0.140
    d0 = spot_d(D, F_FT, M2_MAX) * 1e3                  # um at focus
    z_r = zr(d0 * 1e-3, M2_MAX)                          # mm
    dz = z_r * math.sqrt((c["defocus_to_um"] / d0) ** 2 - 1) if "defocus_to_um" in c else 0.0
    dd = lambda off: d0 * math.sqrt(1 + ((dz + off) / z_r) ** 2)     # spot (um) with the powder `off` mm further from the focus
    d = dd(0.0)
    band10 = z_r * math.sqrt(1.10 ** 2 - 1) if dz == 0 else None
    # the light-film thermal lens moves the focus 0.73 z_R toward the lens: focus below the powder -> spot shrinks; above -> grows
    film = (dd(-FILM_ZR * z_r), dd(+FILM_ZR * z_r)) if dz else (dd(FILM_ZR * z_r), dd(FILM_ZR * z_r))
    hatch = HATCH_PER_SPOT * d * 1e-3
    p_eq = p_same_ke(V_GALVO, d)
    scan_s = COUPON_MM2 / (V_GALVO * 1e3 * hatch) + JUMP_S
    layers = BUILD_MM / BASE["t"]
    w0 = d0 * 1e-3 / 2
    # cat's eye: radius at the plate beyond which < 10 W returns into the fibre core (flat specular reflector, R 0.9)
    u10 = math.sqrt(math.log(0.9 * P_LASER * 0.98 / 10.0)) * M2_MAX * LAM / (math.pi * w0) / 2
    reach_fs = max_radius(D, M2_MAX, k_mid, LID_APS[I_FS])
    choice.append(dict(option=name, D_mm=D, spot_focus_um=d0, defocus_mm=dz, spot_powder_um=d, zR_mm=z_r, band10_mm=band10,
                       growth_pct=100 * (dd(PLATE_GROWTH) / d - 1), err1mm_um=(min(dd(1.0), dd(-1.0)), max(dd(1.0), dd(-1.0))),
                       err1mm_pct=100 * (max(dd(1.0), dd(-1.0)) / d - 1),
                       film_um=film, film_mm=FILM_ZR * z_r,
                       I350_MW_cm2=2 * 350 / (math.pi * (d * 1e-4 / 2) ** 2) / 1e6, I500_MW_cm2=2 * 500 / (math.pi * (d * 1e-4 / 2) ** 2) / 1e6,
                       I350_x_base=2 * 350 / (math.pi * (d * 1e-4 / 2) ** 2) / I_BASE,
                       ke350=ke_ratio(350, V_GALVO, d), ke500=ke_ratio(500, V_GALVO, d), p_same_ke_W=p_eq,
                       hatch_mm=hatch, rate_mm3_s=V_GALVO * 1e3 * hatch * BASE["t"], scan_s_layer=scan_s,
                       build_min=layers * (scan_s + RECOAT_S) / 60, scan_share=scan_s / (scan_s + RECOAT_S),
                       PD_kW_cm=P_LASER / (D / 10) / 1e3, galvo_fill=D / GALVO_AP, lens_fill=D / LENS_MAX_BEAM,
                       cats_eye_r10_mm=u10 / k_mid * F_FT, stop_reach_mm=reach_fs, extra=c.get("extra", "")))
R["collimator_choice"] = dict(baseline=BASE, v_galvo_m_s=V_GALVO, hatch_per_spot=HATCH_PER_SPOT, coupons_mm2=COUPON_MM2,
                              recoat_s=RECOAT_S, build_mm=BUILD_MM, k_mid=k_mid, I_base_W_cm2=I_BASE, rows=choice)

(OUT / "beam_path.json").write_text(json.dumps(R, indent=1, default=float))

# ---------------------------------------------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------------------------------------------
L = ["# Beam path, end to end (`analysis/optics/beam_path.py`)", "",
     f"500 W, 1070 nm, M² {M2_TYP} typ / {M2_MAX} max; f = {F_FT:.0f} mm; fused silica n = {N_FS:.4f} at 1070 nm. "
     "Paraxial: no lens prescription is used.", "",
     "## B. Collimator → spot (bare-fibre divergence 140 mrad; range 130–150 mrad in brackets)", "",
     "| Collimator | f_c (mm) | D (mm) | Spot, M² 1.05 / 1.1 (µm) | Rayleigh range ±z_R (mm) | ±5 % / ±10 % spot growth (mm) | Spot at f = 254 (µm) | Galvo Ø20 clip |",
     "|---|---|---|---|---|---|---|---|"]
for name in COLL:
    rr = [r for r in rows if r["collimator"] == name]
    mid_t = [r for r in rr if abs(r["theta_full_mrad"] - 140) < 1]
    a, b = mid_t[0], mid_t[1]
    lo = min(r["spot_um"] for r in rr); hi = max(r["spot_um"] for r in rr)
    L.append(f"| {name} | {a['fc_mm']:.1f} | {a['D_mm']:.2f} | {a['spot_um']:.0f} / {b['spot_um']:.0f} [{lo:.0f}–{hi:.0f}] | "
             f"{b['zR_mm']:.2f} | {b['dof5_mm']:.2f} / {b['dof10_mm']:.2f} | {b['spot_f254_um']:.0f} | {b['galvo_clip']:.1e} |")
L += ["", "Collimated beam needed for a given spot at f = 160 mm (M² 1.1): " + "; ".join(
    f"{k} µm → D {v['D_mm']:.2f} mm, f_c {v['fc_mm_at_140']:.1f} mm ({v['fc_range'][0]:.1f}–{v['fc_range'][1]:.1f})" for k, v in need.items()), "",
    f"Fibre: the divergence spec implies a {mfd['140 mrad']:.1f} µm beam diameter at the fibre end ({mfd['150 mrad']:.1f}–{mfd['130 mrad']:.1f} µm).", "",
    "## C. Where the focus lands", "",
    f"The {MP_['win_t']} mm window (Edmund 38-990) and {MP_['slide_t']} mm slide (Edmund 36-299), drawn as the BOM parts since 2026-11-25, "
    f"push the focus down by **{shift:.2f} mm** (the 8 mm window and 3 mm slide drawn before gave {shift_old:.2f} mm). The model raises the lens by "
    f"{MP_['focus_shift']} mm (lens output end z {Z_LENS_OUT:.2f}), so the focus lands at z = {Z_FOCUS_DRAWN:+.3f} mm. The extra "
    f"{MP_['focus_shift'] - round(shift_old, 2):.2f} mm comes out of the shim stack ({MP_['lens_shim']:.2f} mm nominal, was 3.00), so the bridge "
    f"does not move; 0–6 mm of shims moves the lens {MP_['lens_shim']:.2f} mm up (no shims) to {6 - MP_['lens_shim']:.2f} mm down. "
    "Spot on the powder plane as drawn, and if the lens had not been raised (M² 1.1, 140 mrad):", ""]
for name in COLL:
    b = [r for r in rows if r["collimator"] == name and abs(r["theta_full_mrad"] - 140) < 1][1]
    L.append(f"- {name}: {b['spot_um']:.0f} µm at focus, **{b['spot_at_model_focus_um']:.0f} µm on the powder** "
             f"(before: {b['spot_before_raise_um']:.0f} µm, {shift / b['zR_mm']:.1f} z_R out)")
L += ["", "| Focus budget item | mm | kind |", "|---|---|---|"] + [f"| {a} | {b:.3f} | {c} |" for a, b, c in budget]
L += ["", "## D/E. Field geometry (k = chief-ray angle at the plate / optical scan angle; not published for the FTH160-1064)", "",
      "| k | Plate | r (mm) | Scan, optical (°) | Mirror (°) | AOI (°) | Elongation (%) | Plate lateral shift (mm) | Extra focus shift (mm) | Astigmatism (mm) | Chief ray r at slide / window / lens out (mm) |",
      "|---|---|---|---|---|---|---|---|---|---|---|"]
for f_ in field:
    L.append(f"| {f_['k']} | {f_['plate']} | {f_['r_mm']:.1f} | {f_['scan_optical_deg']:.1f} | {f_['mirror_mech_deg']:.1f} | {f_['aoi_deg']:.1f} | "
             f"{f_['elongation_pct']:.2f} | {f_['plate_lateral_shift_mm']:.3f} | {f_['plate_focus_shift_extra_mm']:.3f} | {f_['plate_astig_mm']:.3f} | "
             f"{f_['chief_r_at_slide']:.1f} / {f_['chief_r_at_window']:.1f} / {f_['chief_r_at_lens_out']:.1f} |")
L += ["", f"Thin-lens estimate of k (lens at H', z {Z_HP:.1f}; stop at the 2nd mirror, z {Z_GALVO_IN:.1f}): exit pupil {_d_xp:.0f} mm above the lens, k = {K_THIN:.2f}. "
      "The lens's real principal planes are not published, so the tables span k = 0.3-0.75.", ""]
L += ["", "k from a thin lens with its front principal plane between the lens body's middle and H' (z 160): " + "; ".join(
    f"{k}: {a:.2f}-{b:.2f}" for k, (a, b) in K_RANGE.items()), "",
    "Clear diameter each lid opening needs to pass the L75 edge (r 38.1 mm) with < 0.1 % clipped (mm):", "",
    "| Beam | k | " + " | ".join(f"{a[0]} (drawn Ø{a[3]:.0f})" for a in LID_APS) + " |", "|---|---|" + "---|" * len(LID_APS)]
for r_ in need_d:
    L.append(f"| {r_['D_mm']} mm | {r_['k']} | " + " | ".join(f"{r_[a[0]]:.1f}" for a in LID_APS) + " |")
L += ["", "Largest plate radius each lid aperture passes with < 0.1 % clipped (mm; plates are 12.7 / 25.4 / 38.1):", "",
      "| Collimator | k | " + " | ".join(a[0] + f" Ø{a[3]:.0f}" for a in LID_APS) + " | field stop, 50 % reach |",
      "|---|---|" + "---|" * (len(LID_APS) + 1)]
for a in aps:
    L.append(f"| {a['collimator']} | {a['k']} | " + " | ".join(f"{a[x[0]]:.1f}" for x in LID_APS) +
             f" | {a['field stop: beam centre on the edge (50 % passes)']:.1f} |")
L += ["", "L75 reach as drawn (k over the drawn thin-lens range; the opening that limits it; < 0.1 % clipped):", "",
      "| Collimator | k | Reach (mm) | Limited by | L75 (38.1) | M50 (25.4) |", "|---|---|---|---|---|---|"]
L += [f"| {r_['collimator']} | {r_['k']:.2f} | {r_['reach_mm']:.1f} | {r_['limited_by']} | {'yes' if r_['L75_passes'] else 'no'} | {'yes' if r_['M50_passes'] else 'no'} |" for r_ in reach]
L += ["", "## F. Irradiance at 500 W (lens refocused onto the plate)", ""]
for key, tab in R["irradiance"].items():
    L += [f"**{key}**", "", "| Surface | Beam Ø (mm) | Peak (W/cm²) | P/D (W/cm) | Note |", "|---|---|---|---|---|"]
    L += [f"| {s['surface']} | {s['beam_d_mm']:.3f} | {s['peak_W_cm2']:.3g} | {s['linear_W_cm']:.3g} | {s['note']} |" for s in tab]
    L.append("")
L += ["## G. Back-reflection", "",
      f"Uncoated fused silica reflects {100*R_UNC:.2f} % per face; a good AR coat ~{100*R_AR:.2f} %.", "",
      "| D (mm) | Surface | Height (air-equiv., mm) | Core coupling | Into the core, uncoated / AR (W) | Back toward the head, uncoated / AR (W) | Ghost focus z (thin lens) | Return focus from fibre end (mm) / radius there (mm) |",
      "|---|---|---|---|---|---|---|---|"]
for g in ghost:
    gz = f"{g['ghost_focus_z_thin_lens']:.0f}" if g["ghost_focus_z_thin_lens"] else "–"
    L.append(f"| {g['D_mm']} | {g['surface']} | {g['height_air_mm']:.1f} | {g['core_coupling']:.1e} | {g['returned_W_uncoated']:.3f} / {g['returned_W_AR']:.4f} | "
             f"{g['total_back_W_uncoated']:.1f} / {g['total_back_W_AR']:.2f} | {gz} | {g['return_focus_from_fibre_mm']:.1f} / {g['return_radius_at_fibre_mm']:.2f} |")
L += ["", "Flat specular melt pool or bare plate at focus (cat's eye), R 0.9, optics T 0.98 (W back into the core):", "",
      "| D (mm) | k | r = 0 | 1 | 2 | 3 | 5 | 8 | 12.7 | 25.4 mm |", "|---|---|---|---|---|---|---|---|---|---|"]
for D in (5.0, 3.2):
    for k in KS:
        cc = [c for c in cats if c["D_mm"] == D and c["k"] == k]
        L.append(f"| {D} | {k} | " + " | ".join(f"{c['returned_W_at_R0p9']:.3g}" for c in cc) + " |")
L += ["", "## H. Safety optics (MPE 5 mW/cm², as safety_calcs.py)", "",
      "| D (mm) | Collimated φ (mrad) | NOHD collimated (km) | Through f-theta φ (mrad) | NOHD from focus (m) | NOHD specular Al (m) |", "|---|---|---|---|---|---|"]
L += [f"| {s['D_mm']} | {s['collimated_phi_mrad']:.3f} | {s['NOHD_collimated_km']:.1f} | {s['focus_phi_mrad']:.1f} | {s['NOHD_focus_m']:.0f} | {s['NOHD_specular_Al_m']:.0f} |" for s in saf]
L += ["", f"Bare fibre: NOHD {R['safety']['NOHD_bare_fibre_m']:.1f} m (140 mrad), {R['safety']['NOHD_bare_fibre_m_130']:.1f} m (130 mrad). "
      f"Eyewear for the direct beam: OD ≥ {R['safety']['OD_direct']:.1f}.", "",
      f"Guard, 1.6 mm 5052, 1-D lower bound on burn-through ({E_area:.0f} J/cm², no conduction):", "",
      "| D (mm) | From focus (mm) | Beam Ø (mm) | I (W/cm²) | t at absorptance 0.08 / 0.4 (s) |", "|---|---|---|---|---|"]
L += [f"| {b['D_mm']} | {b['from_focus_mm']:.0f} | {b['beam_d_mm']:.2f} | {b['I_W_cm2']:.3g} | {b['t_cold_s']:.2f} / {b['t_hot_s']:.2f} |" for b in burn]
CC = R["collimator_choice"]
L += ["", "## I. Collimator choice: what each option does to the process (optics.md §9.1)", "",
      f"Baseline with a known Al window: {BASE['name']}, {BASE['d_um']:.0f} µm, {BASE['P']:.0f} W, {BASE['V'] * 1e3:.0f} mm/s, hatch {BASE['h']} mm "
      f"(peak {I_BASE / 1e6:.1f} MW/cm²). Ke ratio = keyhole number (Gan et al. 2021) over the baseline's, at {V_GALVO} m/s (the basiCube 20's marking speed); "
      f"it scales as P/√(V r³). Hatch = {HATCH_PER_SPOT:.1f} × spot (the baseline's ratio, assumed). Screening build: three 10 × 10 mm coupons, "
      f"{BUILD_MM:.0f} mm at {BASE['t'] * 1e3:.0f} µm, {RECOAT_S:.0f} s recoat, run at the power that matches the baseline's Ke. M² 1.1, 140 mrad.", "",
      "| Option | D (mm) | Spot on powder (µm) | z_R (mm) | ±10 % band (mm) | 0.112 mm plate growth | Spot after a ±1 mm focus error | Light-film thermal shift | Peak at 350 W (MW/cm², × baseline) | Ke × baseline at 350 / 500 W | Power for the baseline's Ke at 1.1 m/s (W) | Hatch (mm) | Rate (mm³/s) | 15 mm screening build (min) | P/D on the optics at 500 W (kW/cm) | Cat's eye < 10 W beyond r (mm) | Field-stop reach, k {:.2f} (mm) |".format(k_mid),
      "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for c in CC["rows"]:
    band = f"±{c['band10_mm']:.2f}" if c["band10_mm"] else "– (on the slope)"
    film = (f"{c['film_mm']:.1f} mm → {c['film_um'][0]:.0f} µm" if not c["defocus_mm"]
            else f"{c['film_mm']:.1f} mm → {c['film_um'][0]:.0f} or {c['film_um'][1]:.0f} µm")
    L.append(f"| {c['option']} | {c['D_mm']:.2f} | {c['spot_powder_um']:.0f}" + (f" ({c['spot_focus_um']:.0f} at focus, {c['defocus_mm']:.2f} mm out)" if c["defocus_mm"] else "") +
             f" | {c['zR_mm']:.2f} | {band} | {c['growth_pct']:+.1f} % | {c['err1mm_um'][0]:.0f}–{c['err1mm_um'][1]:.0f} µm | {film} | "
             f"{c['I350_MW_cm2']:.1f} ({c['I350_x_base']:.2f}×) | {c['ke350']:.2f} / {c['ke500']:.2f} | {c['p_same_ke_W']:.0f} | {c['hatch_mm']:.3f} | {c['rate_mm3_s']:.1f} | "
             f"{c['build_min']:.0f} (scan {100 * c['scan_share']:.0f} %) | {c['PD_kW_cm']:.2f} | {c['cats_eye_r10_mm']:.1f} | {c['stop_reach_mm']:.1f} |")
L += ["", "Notes: the light-film shift (0.05 % absorbed in the slide) is 0.73 z_R for every beam size (thermal_lens.md); with the defocused option "
      "it shrinks or grows the spot depending on which side of the powder the focus sits. The expander rows add two lenses to the 500 W beam "
      "(each a further ~0.2 z_R of thermal shift when clean, Faas et al. 2018). Galvo fill D/20 mm and f-theta fill D/12 mm are ≤ 0.42 for every option."]
(OUT / "beam_path.md").write_text("\n".join(L) + "\n")

# ---------------------------------------------------------------------------------------------------------------
# Figure: caustics near focus for the collimator options, against the layer, the stack growth and the plate shift
# ---------------------------------------------------------------------------------------------------------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.5, 4.4), dpi=150)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    zz = np.linspace(-6, 6, 400)
    cols = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]      # categorical slots 1-4, fixed order (dataviz palette)
    short = ["IPG 2.5 mm (drawn)", "2.5 mm + 1.2x expander", "D 3.2 mm (75 µm target)", "QBH f_c 30 mm"]
    for (name, c), col, lab in zip(COLL.items(), cols, short):
        D = c.get("D") or c["fc"] * 0.140
        d = spot_d(D, F_FT, M2_MAX)
        z_r = zr(d, M2_MAX)
        yy = 2 * np.array([w_at(d / 2, z_r, z) for z in zz]) * 1e3
        ax.plot(zz, yy, color=col, lw=2, label=f"{lab}: {d*1e3:.0f} µm, ±{z_r:.1f} mm")
        ax.annotate(lab, (zz[0], yy[0]), xytext=(4, 0), textcoords="offset points", fontsize=7, color="#52514e",
                    va="center") if yy[0] < 235 else None
    ax.axvline(shift, color="#52514e", ls="--", lw=1)
    ax.text(shift + 0.12, 28, f"powder plane before the lens\nwas raised {shift:.1f} mm", fontsize=7, color="#52514e")
    ax.axvspan(0, 0.112, color="#52514e", alpha=0.18, lw=0)
    ax.text(0.2, 6, "plate growth at 200 °C (0.11 mm)", fontsize=7, color="#52514e")
    ax.set_xlabel("height above the focus (mm)")
    ax.set_ylabel("1/e² spot diameter (µm)")
    ax.set_ylim(0, 240)
    ax.set_xlim(-6, 6)
    ax.grid(alpha=0.25, lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=7, frameon=False, loc="upper center")
    ax.set_title("Spot vs focus, f = 160 mm, M² 1.1, IPG fibre at 140 mrad", fontsize=9, color="#0b0b0b")
    fig.tight_layout()
    fig.savefig(OUT / "beam_path.png")
except Exception as e:  # figure is optional
    print("figure skipped:", e)

print((OUT / "beam_path.md").read_text())
