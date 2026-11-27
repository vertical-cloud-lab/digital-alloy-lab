#!/usr/bin/env python3
"""The BW light for the side camera, as drawn (issue #260, monitoring/optics.md §4.1 "The BW light as drawn").

A Thorlabs M850D3 (850 nm LED, 1 x 1 mm die, on a Ø22 metal-core board) on a custom finned heat sink, imaged onto the plate
by an ACL25416U-B aspheric condenser in an SM1 lens tube, behind the back-wall window (BW). Pulsed by a DC2200 in TTL mode
from the Pico 2's strobe output (sync-and-data.md §1.3). This script:

1. traces rays (Monte Carlo) from the die, with Thorlabs' measured angular pattern, through the asphere's published Zemax
   prescription, the clamp frame, the window (Fresnel at each face), the slot and the liner, to the bed: the irradiance on
   the bed in the side camera's field, the beam across its axis at the plate centre, and where every ray ends up;
2. turns that into photo-electrons per pixel per exposure at the Chronos 2.1-HD (LW port, Kowa 50 mm, FBH850-10 +
   FESH1000; QE, pixel and full well from parts.py), and compares the lit bed and lit particles with the melt pool's,
   the plume's and hot spatter's own light in the same band, and with what a SOLIS-850C at BW would have given;
3. checks the LED's current, duty and junction temperature at the planned frame rates;
4. checks eye safety against the IEC 62471 / Directive 2006/25/EC IR-A limits: the beam itself, the light that can reach
   the guard's viewing panel, the window's reflection, and a bare plate's specular reflection through the open door.

Geometry from cad/monitoring_spec.py and analysis/monitoring/fab/frame_features.py, read at run time. Vendor numbers are in
VENDOR below with their sources (read through the lab tunnel on 2026-11-27, 08:21-08:39 UTC); everything marked "estimate"
is not from a datasheet.

    python bw_light.py            (~20 s, < 1 GB)
Writes analysis/out/monitoring/optics/bw_light.json, bw_light.md and bw_light.png.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "analysis" / "out" / "monitoring" / "optics"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "cad"))
sys.path.insert(0, str(ROOT / "analysis" / "monitoring" / "fab"))
import monitoring_spec as MS  # noqa: E402
import parts as PT  # noqa: E402
import radiometry as RM  # noqa: E402
import raytrace as RT  # noqa: E402

H, C = 6.62607015e-34, 2.99792458e8
TL = "https://www.thorlabs.com/item/"

# ------------------------------------------------------------------------------------------------ vendor data (read 2026-11-27)
VENDOR = dict(
    M850D3=dict(url=TL + "M850D3", read="2026-11-27T08:22Z", usd=143.64,
                spec="MTN005519-S01 Rev D (spec sheet, sha256 in bw_light.json)",
                P_min_W=1.4, P_typ_W=1.6, I_test_A=1.5, I_max_cw_A=1.5, VF_typ_V=3.35, VF_max_V=3.85, die_mm=(1.0, 1.0),
                rise_fall_ns=(11, 14), fwhm_nm=30, centroid_nm=850, peak_nm=860, view_full_deg=150, risk_group="RG0 (exempt)",
                Ee_200mm_uW_mm2=19.4, board="Ø22.0 x 1.6 mm MCPCB, 2.8 mm over the LED, 2 x Ø2.0 holes on Ø19.0 (M2)",
                op_temp_C=(0, 40), lifetime_h=10000),
    # the same LED mounted on a Ø57 heat sink: its sheet gives the pulsed maximum that the M850D3's sheet leaves out
    M850LP1=dict(url=TL + "M850LP1", read="2026-11-27T08:22Z", usd=434.72, spec="MTN005518-S01 Rev C",
                 I_max_pulsed_A=2.0, note="'Maximum Current (Pulsed) 2000 mA; limited to the maximum CW current when using the "
                 "DC2200, DC4100 or DC4104' (via the EEPROM); same power, die, rise time and viewing angle as the M850D3; Ø57 heat sink"),
    SOLIS_850C=dict(url=TL + "SOLIS-850C", read="2026-11-27T08:22Z", usd=1377.86, spec="MTN006952-S01 Rev B",
                    P_min_W=2.7, P_typ_W=3.6, emitter_d_mm=6.5, fwhm_nm=39, peak_nm=850, Ee_200mm_mW_mm2=0.6, I_max_A=1.0,
                    clear_aperture_mm=48.3, optics="LB1723-B + ACL25416U-B", risk_group="RG3 (high risk)"),
    ACL25416U_B=dict(url=TL + "ACL25416U-B", read="2026-11-27T08:23Z", usd=34.33, glass="B270", d_mm=25.4, ct_mm=14.0,
                     efl_mm=16.0, bfl_mm=7.3, ca_mm=22.9, na=0.79, coat="BBAR Ravg < 0.5 % 650-1050 nm",
                     # Zemax file ctn002266-s03.zmx and drawing acl25416u-b-e0w.pdf: S1 even asphere, S2 sphere
                     R1=8.818197, k1=-0.9991715, A=(8.6821674e-05, 6.3760123e-08, 2.4073084e-09, -1.7189021e-11), R2=-69.99948),
    DC2200=dict(url=TL + "DC2200", read="2026-11-27T08:23Z", usd=2593.01, manual="MTN005097-D02 (2023), §3.3.7 TTL Modulation Mode",
                ttl_fmax_kHz={"LED1 0-4 A (500 mA, 1 W load)": 23, "LED1 4-10 A": 18, "LED2 0-2 A (250 mA, 2 W load)": 27},
                fmax_def="fmax: rise + fall time (10-90 %) = 10 % of the TTL period, resistive load",
                led2="up to 2 A at up to 35 V (1.5 A at 50 V); M8 4-pin (CAB-LEDD1)"),
    TCDT1=dict(url=TL + "TCDT1", read="2026-11-27T08:39Z", usd=41.73, thick_mm=0.23, z_cm2K_W=1.7, k_W_mK=1.40),
)
# M850D3 spectrum and angular pattern, digitised from the spec sheet's plots (page 2, rendered at 300 dpi; +/-0.02)
LED_SPEC = [(750, 0.0), (770, 0.005), (780, 0.012), (790, 0.03), (800, 0.055), (810, 0.10), (820, 0.17), (830, 0.27), (840, 0.42),
            (845, 0.51), (850, 0.62), (855, 0.75), (860, 0.90), (865, 1.0), (868, 0.98), (870, 0.90), (875, 0.68), (880, 0.40),
            (885, 0.20), (890, 0.09), (895, 0.04), (900, 0.02), (910, 0.008), (925, 0.003), (950, 0.0)]
LED_ANG = [(0, 1.0), (10, 0.99), (20, 0.975), (30, 0.958), (40, 0.935), (50, 0.905), (55, 0.885), (60, 0.84), (65, 0.79), (70, 0.72),
           (71, 0.65), (73, 0.62), (74, 0.60), (75, 0.52), (77, 0.42), (80, 0.30), (83, 0.21), (85, 0.17), (88, 0.10), (90, 0.06)]
LED_IV = [(0.02, 2.6), (0.08, 2.7), (0.20, 2.8), (0.33, 2.9), (0.50, 3.0), (0.72, 3.1), (0.98, 3.2), (1.27, 3.3), (1.50, 3.35)]

# estimates (no datasheet number): flagged in the output
EST = dict(
    LI_exponent=0.85,          # light ~ I^0.85 above 1.5 A (droop); Thorlabs publishes no L-I curve for the M850D3
    dPdT_per_K=-0.003,         # output -0.3 %/K (typical 850 nm AlGaAs); not published
    dlam_dT_nm_K=0.25,         # peak shift +0.25 nm/K (typical); not published
    Rth_jb_K_W=8.0,            # junction to the board's back face, 1 x 1 mm IR die on an MCPCB; not published
    Tj_max_C=125.0,            # typical for this class; not published
    T_air_C=40.0,              # guard air at the cameras: 38-43 C (mechanics.md Checks §7)
    rho_bed=0.5,               # powder bed reflectance, Lambertian (as viewports.py and optics.md §4)
    tau_cam=0.8,               # LW window + slide + Kowa lens (as viewports.py)
    glint_px_fraction=0.5,     # share of a specular glint's image in its brightest 25 um pixel at f/4
    n_B270=(1.5230, 58.5),     # nd, vd (Schott B 270); Cauchy fit used for 850-870 nm
)
SLIDE_FRESNEL_COATED = 0.995   # asphere AR: Ravg < 0.5 % per face (Thorlabs)

# the custom heat sink (6061, black anodised): Ø36 collar with the SM1 thread, then a finned body; see _bw_light()
HEAT_SINK = dict(d=36.0, L=40.0, collar=10.0, fins=5, fin_t=2.0, fin_gap=4.0, root_d=24.0, bore_d=26.3, bore_depth=8.0)


def interp(table, x):
    a = np.asarray(table, float)
    return np.interp(x, a[:, 0], a[:, 1], left=0.0, right=0.0)


def n_b270(lam_nm):
    nd, vd = EST["n_B270"]
    B = (nd - 1) / vd / (1 / 0.4861 ** 2 - 1 / 0.6563 ** 2)
    return nd - B / 0.5876 ** 2 + B / (lam_nm / 1000.0) ** 2


# ------------------------------------------------------------------------------------------------ filters and camera
def fbh(lam, cwl=850.0, fwhm=10.0, tpk=0.92):
    """Thorlabs FBH hard-coated bandpass: T > 90 % at the CWL, FWHM 10 or 40 nm, OD > 5 out of band (family spec);
    modelled as a super-Gaussian (order 6) with that FWHM."""
    return tpk * np.exp(-np.log(2) * (np.abs(lam - cwl) / (fwhm / 2)) ** 6)


def fesh1000(lam):
    return 10 ** (-interp(PT.FESH1000_OD, lam))


CAM = PT.CAMS["Chronos 2.1-HD mono"]
LENS = PT.LENSES["Kowa LM50JC10M 50 mm"]
LAM = np.arange(700.0, 1001.0, 1.0)


def led_spectrum(shift_nm=0.0):
    s = interp(LED_SPEC, LAM - shift_nm)
    return s / np.trapezoid(s, LAM)


def gauss_spectrum(peak, fwhm):
    s = np.exp(-4 * np.log(2) * ((LAM - peak) / fwhm) ** 2)
    return s / np.trapezoid(s, LAM)


def camera_geometry():
    lw = np.array(MS.VIEWPORTS["LW"]["centre"], float)
    wd = float(np.linalg.norm(lw)) + MS.SIDE_CAMERA["standoff_mm"]          # viewports.py: lens front to plate centre
    f = LENS["f_mm"]
    m = f / (wd - f)
    px = CAM["px_um"] / m
    elev = MS.elevation_deg(tuple(lw))
    view = -lw / np.linalg.norm(lw)                                          # camera to plate
    vh = np.array([view[0], view[1], 0.0]) / math.hypot(view[0], view[1])
    across = np.array([-vh[1], vh[0], 0.0])
    roi = PT.ROI["Chronos 2.1-HD mono"]
    return dict(wd_mm=wd, m=m, um_per_px=px, elev_deg=elev, view=view, vh=vh, across=across, roi=roi,
                roi_across_mm=roi[0] * px / 1000, roi_along_bed_mm=roi[1] * px / 1000 / math.sin(math.radians(elev)))


def e_per_px(L_spec, t_us, N=4.0, filt="FBH850-10", tau=None, cg=None):
    """Photo-electrons in one pixel from a resolved source of spectral radiance L_spec (W m^-2 sr^-1 nm^-1 on LAM):
    E_image = pi L tau T_filters / (4 N^2 (1 + m)^2) (as viewports.illumination), times pixel area, exposure and QE."""
    cg = cg or camera_geometry()
    tau = EST["tau_cam"] if tau is None else tau
    T = filt_T(filt)
    qe = interp(CAM["qe"], LAM)
    Ei = math.pi * L_spec * tau * T / (4 * N * N * (1 + cg["m"]) ** 2)
    nph = Ei * (CAM["px_um"] * 1e-6) ** 2 * t_us * 1e-6 * LAM * 1e-9 / (H * C)
    return float(np.trapezoid(nph * qe, LAM))


FILTERS = {"FBH850-10": (850.0, 10.0), "FBH860-10": (860.0, 10.0), "FBH870-10": (870.0, 10.0), "FBH850-25": (850.0, 25.0),
           "FBH850-40": (850.0, 40.0)}     # Thorlabs, all $193.82 (read 2026-11-27T08:32-08:49Z); CWL and FWHM from the item titles


def filt_T(filt):
    if filt is None:
        return fesh1000(LAM)
    cwl, fw = FILTERS[filt]
    return fesh1000(LAM) * fbh(LAM, cwl=cwl, fwhm=fw)


def in_band(s, filt="FBH850-10"):
    return float(np.trapezoid(s * filt_T(filt), LAM))


# ------------------------------------------------------------------------------------------------ geometry of the light
def frame(axis):
    a = np.asarray(axis, float) / np.linalg.norm(axis)
    up = np.array([0.0, 0.0, 1.0]) - a[2] * a
    up /= np.linalg.norm(up)
    return a, up, np.cross(up, a)


def layout():
    """Positions along the outward BW sight line (t = 0 at the port centre on the wall's outer face, + outward), mm."""
    import frame_features as FF
    s = MS.VIEWPORTS["BW"]
    c = np.array(s["centre"], float)
    d = np.array(MS.axis_to_target(s["centre"]))
    a, up, side = frame(-d)
    y_out = FF.OUTER["y"]
    clamp_t = 4.76                      # clamp frame, 3/16 in. plate (monitoring_parts._bw)
    r_tube = 15.24                      # SM1 lens tube OD 1.20 in.
    tube_ahead = 8.9                    # the asphere's vertex stands this far ahead of the tube's front (sag at the rim 11.4 mm,
    #                                     less a 2.5 mm SM1RR in front of the rim)
    rim_y = math.sqrt(1 - a[1] ** 2)
    t_front = (clamp_t + 3.0 + r_tube * rim_y) / a[1]                          # tube rim 3 mm off the clamp frame
    t_s1 = t_front - tube_ahead
    _, info, _ = FF.bw_features(None, 0.0)
    return dict(c=c, d=d, a=a, up=up, side=side, y_out=y_out, clamp_t=clamp_t, r_tube=r_tube, t_tube_front=t_front, t_S1=t_s1,
                slot=info["slot"], seat=info["seat"], liner_x0=info["liner"]["x_range"][1], plate_dist=float(np.linalg.norm(c)),
                inner_y=FF.INNER["y"], liner=FF.LINER)


def sag(r, P):
    c, k = 1 / P["R1"], P["k1"]
    A4, A6, A8, A10 = P["A"]
    r2 = r * r
    return c * r2 / (1 + np.sqrt(1 - (1 + k) * c * c * r2)) + A4 * r2 ** 2 + A6 * r2 ** 3 + A8 * r2 ** 4 + A10 * r2 ** 5


def dsag(r, P):
    c, k = 1 / P["R1"], P["k1"]
    A4, A6, A8, A10 = P["A"]
    return c * r / np.sqrt(1 - (1 + k) * c * c * r * r) + 4 * A4 * r ** 3 + 6 * A6 * r ** 5 + 8 * A8 * r ** 7 + 10 * A10 * r ** 9


def refract(d, n, n1, n2):
    """Vector Snell; n is turned to face the incoming ray. Returns new directions and a mask of rays not totally reflected."""
    n = np.where((np.sum(d * n, axis=1) > 0)[:, None], -n, n)
    eta = n1 / n2
    cosi = -np.sum(d * n, axis=1)
    k = 1 - eta ** 2 * (1 - cosi ** 2)
    ok = k >= 0
    t = eta * d + (eta * cosi - np.sqrt(np.maximum(k, 0)))[:, None] * n
    return t / np.linalg.norm(t, axis=1)[:, None], ok, cosi


def fresnel_T(cosi, n1, n2):
    sini = np.sqrt(np.maximum(0, 1 - cosi ** 2))
    sint = n1 / n2 * sini
    cost = np.sqrt(np.maximum(0, 1 - sint ** 2))
    rs = ((n1 * cosi - n2 * cost) / (n1 * cosi + n2 * cost)) ** 2
    rp = ((n1 * cost - n2 * cosi) / (n1 * cost + n2 * cosi)) ** 2
    return 1 - 0.5 * (rs + rp)


def sample_led(N, rng):
    th = np.linspace(0, 90, 901)
    pdf = interp(LED_ANG, th) * np.sin(np.radians(th))
    cdf = np.cumsum(pdf)
    cdf /= cdf[-1]
    theta = np.radians(np.interp(rng.random(N), cdf, th))
    phi = rng.random(N) * 2 * np.pi
    x0 = (rng.random(N) - 0.5) * VENDOR["M850D3"]["die_mm"][0]
    y0 = (rng.random(N) - 0.5) * VENDOR["M850D3"]["die_mm"][1]
    d = np.stack([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), -np.cos(theta)], axis=1)
    return np.stack([x0, y0], axis=1), d, theta


def paraxial_gap(Lg):
    """Die-to-S2 gap (mm) that images the die onto the plate centre, from the thick-lens principal planes at 860 nm."""
    P = VENDOR["ACL25416U_B"]
    n = n_b270(860.0)
    R1, R2, d = P["R1"], P["R2"], P["ct_mm"]
    phi = (n - 1) * (1 / R1 - 1 / R2 + (n - 1) * d / (n * R1 * R2))
    f = 1 / phi
    h1 = -f * (n - 1) * d / (n * R2)        # S1 vertex to its principal plane (+ into the lens)
    h2 = -f * (n - 1) * d / (n * R1)        # S2 vertex to its principal plane (- into the lens)
    s_img = Lg["t_S1"] + Lg["plate_dist"] - h1 + 1.0    # +1 mm: the 3 mm window lengthens the path (t (1 - 1/n) / cos)
    s_obj = 1 / (1 / f - 1 / s_img)
    return dict(f=f, h1=h1, h2=h2, s_img=s_img, s_obj=s_obj, gap=s_obj + h2, m=s_img / s_obj)


def trace(Lg, gap, N=600_000, seed=1, P_led=1.0, keep=False):
    """Trace N rays carrying P_led W in all; returns where the power goes and the landing points on the bed."""
    rng = np.random.default_rng(seed)
    A = VENDOR["ACL25416U_B"]
    n_g = n_b270(860.0)
    r_ca = A["ca_mm"] / 2
    xy, d, theta = sample_led(N, rng)
    w = np.full(N, P_led / N)
    budget = {"emitted": w.sum()}
    z_led = A["ct_mm"] + gap
    p = np.column_stack([xy, np.full(N, z_led)])
    # S2: sphere, vertex at z = ct, centre at ct + R2 (Zemax coordinates, light travelling -z)
    Cz = A["ct_mm"] + A["R2"]
    oc = p - np.array([0, 0, Cz])
    b = np.sum(oc * d, axis=1)
    cc = np.sum(oc * oc, axis=1) - A["R2"] ** 2
    disc = b * b - cc
    t = -b - np.sqrt(np.maximum(disc, 0))
    p2 = p + t[:, None] * d
    r2 = np.hypot(p2[:, 0], p2[:, 1])
    live = (disc > 0) & (t > 0) & (r2 <= r_ca)
    budget["outside the asphere's clear aperture (on the tube and retaining ring)"] = w[~live].sum()
    n2 = (p2 - np.array([0, 0, Cz])) / abs(A["R2"])
    d2, ok, _ = refract(d, n2, 1.0, n_g)
    live &= ok
    w = w * SLIDE_FRESNEL_COATED
    # S1: even asphere z = sag(r), Newton along the ray
    tt = (sag(np.minimum(r2, 12.0), A) - p2[:, 2]) / d2[:, 2]
    for _ in range(30):
        q = p2 + tt[:, None] * d2
        rq = np.hypot(q[:, 0], q[:, 1])
        f = q[:, 2] - sag(np.minimum(rq, 12.69), A)
        drdt = (q[:, 0] * d2[:, 0] + q[:, 1] * d2[:, 1]) / np.maximum(rq, 1e-9)
        fp = d2[:, 2] - dsag(np.minimum(rq, 12.69), A) * drdt
        tt = tt - f / fp
    p1 = p2 + tt[:, None] * d2
    r1 = np.hypot(p1[:, 0], p1[:, 1])
    live &= (r1 <= r_ca) & np.isfinite(r1)
    g = dsag(np.minimum(r1, 12.69), A)
    n1 = np.column_stack([-g * p1[:, 0] / np.maximum(r1, 1e-9), -g * p1[:, 1] / np.maximum(r1, 1e-9), np.ones(N)])
    n1 /= np.linalg.norm(n1, axis=1)[:, None]
    d1, ok, _ = refract(d2, n1, n_g, 1.0)
    live &= ok
    w = w * SLIDE_FRESNEL_COATED
    lost_lens = (P_led / N) * live.sum() * (1 - SLIDE_FRESNEL_COATED ** 2)
    # to the model's frame: Zemax +z = outward along the sight line, origin at S1's vertex
    a, e1, e2 = Lg["a"], Lg["up"], Lg["side"]
    P0 = Lg["c"] + Lg["t_S1"] * a
    pm = P0 + p1[:, 2:3] * a + p1[:, 0:1] * e1 + p1[:, 1:2] * e2
    dm = d1[:, 2:3] * a + d1[:, 0:1] * e1 + d1[:, 1:2] * e2
    dm /= np.linalg.norm(dm, axis=1)[:, None]
    res = dict(budget={}, lost_lens_coat=lost_lens)

    def at_y(pp, dd, y):
        s = (y - pp[:, 1]) / dd[:, 1]
        return pp + s[:, None] * dd

    sl = Lg["slot"]
    e_1, e_2 = np.array(sl["end_centres_xz"][0]), np.array(sl["end_centres_xz"][1])

    def in_stadium(q, r):
        xz = q[:, [0, 2]]
        u = e_2 - e_1
        s = np.clip(((xz - e_1) @ u) / (u @ u), 0, 1)
        near = e_1 + s[:, None] * u
        return np.linalg.norm(xz - near, axis=1) <= r

    y_out = Lg["y_out"]
    y_clamp = y_out + Lg["clamp_t"]
    st = Lg["seat"]
    y_win_out = y_out - 0.75
    y_win_in = y_win_out - 3.0
    y_floor = y_out - st["depth"]
    q_c = at_y(pm, dm, y_clamp)
    q_c2 = at_y(pm, dm, y_out)
    m_clamp = in_stadium(q_c, sl["radius"] + 1.0) & in_stadium(q_c2, sl["radius"] + 1.0)
    q_g = at_y(pm, dm, y_win_out)
    m_ring = in_stadium(q_g, sl["radius"] + 0.5)
    hit_frame = live & ~(m_clamp & m_ring)
    res["budget"]["on the clamp frame and flat ring (outside the opening)"] = float(w[hit_frame].sum())
    live &= m_clamp & m_ring
    # window: fused silica, uncoated, flat on the wall (normal +y)
    n_fs = float(RT.n_glass("F_SILICA", 0.86))
    nrm = np.tile(np.array([0.0, 1.0, 0.0]), (N, 1))
    dw, ok, cos_a = refract(dm, nrm, 1.0, n_fs)
    T1 = fresnel_T(cos_a, 1.0, n_fs)
    refl_out = w * (1 - T1)                                            # reflected off the outer face, back out of the window
    pw1 = q_g
    q_w2 = at_y(pw1, dw, y_win_in)
    d_in, ok2, cos_b = refract(dw, nrm, n_fs, 1.0)
    T2 = fresnel_T(cos_b, n_fs, 1.0)
    refl_in = w * T1 * (1 - T2) * T1                                   # the inner face's reflection also leaves outward (once)
    res["window_reflected_W"] = float((refl_out + refl_in)[live].sum())
    w_after = w * T1 * T2
    res["budget"]["reflected by the window's two faces (back out, outside the chamber)"] = res["window_reflected_W"]
    res["budget"]["absorbed / multiply reflected in the window"] = float((w - w_after - refl_out - refl_in)[live].sum())
    w = w_after
    # gasket under the window and the slot (obround, normal to the wall) from y_floor to the inner face
    q_s1 = at_y(q_w2, d_in, y_floor)
    q_s2 = at_y(q_w2, d_in, Lg["inner_y"])
    m_slot = in_stadium(at_y(q_w2, d_in, y_win_in), sl["radius"] + 0.5) & in_stadium(q_s1, sl["radius"]) & in_stadium(q_s2, sl["radius"])
    res["budget"]["on the slot's walls and the gasket"] = float(w[live & ~m_slot].sum())
    live &= m_slot
    # lower back liner (0.5 mm, z 16-32), its left piece now starting at x liner_x0
    y_lin = Lg["inner_y"] - Lg["liner"]["gap"] - Lg["liner"]["t"]
    q_l = at_y(q_w2, d_in, y_lin)
    z0, z1 = Lg["liner"]["back_lo_z"]
    m_liner = ~((q_l[:, 0] > Lg["liner_x0"]) & (q_l[:, 2] >= z0) & (q_l[:, 2] <= z1))
    res["budget"]["on the lower back liner"] = float(w[live & ~m_liner].sum())
    live &= m_liner
    # inside the chamber: to the bed (z = 0) or a wall
    s_bed = -q_w2[:, 2] / d_in[:, 2]
    land = q_w2 + s_bed[:, None] * d_in
    inside = (np.abs(land[:, 0]) <= 140) & (np.abs(land[:, 1]) <= 95) & (d_in[:, 2] < 0)
    res["budget"]["on the chamber's walls (above the bed)"] = float(w[live & ~inside].sum())
    on_bed = live & inside
    res["budget"]["on the bed, inside the chamber"] = float(w[on_bed].sum())
    res["budget"]["outside the asphere's clear aperture (on the tube and retaining ring)"] = float(budget["outside the asphere's clear aperture (on the tube and retaining ring)"])
    res["budget"]["lens surfaces (AR coat, 0.5 % each)"] = float(lost_lens)
    res["budget"]["emitted"] = float(P_led)
    res["land"] = land[on_bed]
    res["w"] = w[on_bed]
    res["dir_in"] = d_in[on_bed]
    # the beam across its axis at the plate centre: crossing of the plane through the origin normal to the nominal axis d
    dd = Lg["d"]
    s_pl = -(q_w2 @ dd) / (d_in @ dd)
    cross = q_w2 + s_pl[:, None] * d_in
    res["cross"] = cross[live]
    res["w_cross"] = w[live]
    # the window's reflection, for the stray-light check: reflect at the outer face and follow it outward
    if keep:
        dr = dm - 2 * (dm @ np.array([0, 1.0, 0]))[:, None] * np.array([0, 1.0, 0])
        res["refl_p"] = q_g[live]
        res["refl_d"] = dr[live]
        res["refl_w"] = (refl_out + refl_in)[live]
    return res


def bed_stats(res, cg, plate_r):
    land, w = res["land"], res["w"]
    rel = land[:, :2]
    a_coord = rel @ cg["across"][:2]
    b_coord = rel @ cg["vh"][:2]
    in_roi = (np.abs(a_coord) <= cg["roi_across_mm"] / 2) & (np.abs(b_coord) <= cg["roi_along_bed_mm"] / 2)
    area_roi = cg["roi_across_mm"] * cg["roi_along_bed_mm"] / 100.0                       # cm^2
    E_roi = float(w[in_roi].sum()) / area_roi                                                # W/cm^2 (mean)
    # map, 1 mm bins
    edges = np.arange(-60.0, 60.01, 1.0)
    Hm, _, _ = np.histogram2d(land[:, 0], land[:, 1], bins=[edges, edges], weights=w)
    Hm = Hm / 0.01                                                                            # W/cm^2
    # ROI min/max over 1 mm cells whose centre is inside the ROI
    xc = 0.5 * (edges[1:] + edges[:-1])
    X, Y = np.meshgrid(xc, xc, indexing="ij")
    A_ = X * cg["across"][0] + Y * cg["across"][1]
    B_ = X * cg["vh"][0] + Y * cg["vh"][1]
    cell_in = (np.abs(A_) <= cg["roi_across_mm"] / 2 - 0.5) & (np.abs(B_) <= cg["roi_along_bed_mm"] / 2 - 0.5)
    vals = Hm[cell_in]
    on_plate = np.hypot(land[:, 0], land[:, 1]) <= plate_r
    return dict(E_roi_mean=E_roi, E_roi_min=float(vals.min()), E_roi_max=float(vals.max()), E_peak=float(Hm.max()),
                P_in_roi=float(w[in_roi].sum()), P_on_plate=float(w[on_plate].sum()), roi_cm2=area_roi), Hm, edges


def cross_stats(res, Lg):
    """Irradiance across the beam (normal to its axis) at the plate centre; vertical offset > 0 is above the bed."""
    cr, w = res["cross"], res["w_cross"]
    a, up, side = frame(Lg["d"])
    u = cr @ up
    v = cr @ side
    edges = np.arange(-10.0, 10.01, 0.25)
    Hc, _, _ = np.histogram2d(u, v, bins=[edges, edges], weights=w)
    Hc = Hc / (0.025 ** 2)                                                                    # W/cm^2
    cen = 0.5 * (edges[1:] + edges[:-1])
    prof_up = Hc[:, np.abs(cen) < 1.0].mean(axis=1)
    prof_side = Hc[np.abs(cen) < 1.0, :].mean(axis=0)

    def fw(prof):
        m = prof.max()
        k = np.where(prof >= m / 2)[0]
        return float(cen[k[-1]] - cen[k[0]] + 0.25) if len(k) else 0.0
    r7 = np.hypot(u, v) <= 3.5
    return dict(E_peak=float(Hc.max()), E_axis=float(Hc[np.ix_(np.abs(cen) < 0.6, np.abs(cen) < 0.6)].mean()),
                E_7mm_pupil=float(w[r7].sum() / (math.pi * 0.35 ** 2)), fwhm_up_mm=fw(prof_up), fwhm_side_mm=fw(prof_side),
                E_at_height={f"{h:g} mm": float(np.interp(h * math.cos(math.radians(MS.elevation_deg(tuple(Lg['c'])))), cen, prof_up))
                             for h in (0.0, 1.0, 2.0, 4.0, 6.0)}), Hc, edges


# ------------------------------------------------------------------------------------------------ the LED's drive and heat
def vf(I):
    a = np.asarray(LED_IV, float)
    if I <= a[-1, 0]:
        return float(np.interp(I, a[:, 0], a[:, 1]))
    slope = (a[-1, 1] - a[-3, 1]) / (a[-1, 0] - a[-3, 0])
    return float(a[-1, 1] + slope * (I - a[-1, 0]))


def p_opt(I, which="typ"):
    P = VENDOR["M850D3"]["P_typ_W" if which == "typ" else "P_min_W"]
    return P * (I / 1.5) ** (EST["LI_exponent"] if I > 1.5 else 1.0)


def heat_sink_Rth():
    """Natural convection (Churchill-Chu, horizontal cylinder) plus radiation (black anodised, eps 0.85) from the finned
    Ø36 x 40 heat sink in 40 C air at a 30 K rise; fins counted at 60 % (narrow gaps, natural convection)."""
    hs = HEAT_SINK
    D = hs["d"] / 1000
    Tm = 273.15 + EST["T_air_C"] + 15
    nu, alpha, k_air, Pr = 1.75e-5, 2.5e-5, 0.0275, 0.71
    Ra = 9.81 / Tm * 30 * D ** 3 / (nu * alpha)
    Nu = (0.60 + 0.387 * Ra ** (1 / 6) / (1 + (0.559 / Pr) ** (9 / 16)) ** (8 / 27)) ** 2
    h_c = Nu * k_air / D
    h_r = 4 * 0.85 * 5.670e-8 * Tm ** 3
    A_env = math.pi * D * hs["L"] / 1000 + math.pi * D ** 2 / 4
    A_fins = hs["fins"] * 2 * math.pi / 4 * ((hs["d"] / 1000) ** 2 - (hs["root_d"] / 1000) ** 2)
    R = 1 / (h_c * (A_env + 0.6 * A_fins) + h_r * A_env)
    vol = math.pi / 4 * (hs["d"] ** 2 * hs["collar"] + hs["root_d"] ** 2 * (hs["L"] - hs["collar"])
                         + hs["fins"] * hs["fin_t"] * (hs["d"] ** 2 - hs["root_d"] ** 2)) - math.pi / 4 * hs["bore_d"] ** 2 * hs["bore_depth"]
    m = vol * 1e-9 * 2700
    return dict(R_K_W=R, h_conv=h_c, h_rad=h_r, Ra=Ra, mass_g=m * 1000, C_J_K=m * 896, tau_s=R * m * 896)


def drive_table(hs):
    R_tape = VENDOR["TCDT1"]["z_cm2K_W"] / (math.pi * 1.1 ** 2)
    rows = []
    t_r = 0.5 * 0.1 / 27e3 * 1e6          # DC2200 LED2 (0-2 A): rise + fall = 10 % of the period at 27 kHz
    for fps in (24046, 10000, 1000):
        for t_exp in (10.0, 20.0):
            for I in (1.5, 2.0):
                period = 1e6 / fps
                pulse = t_exp + t_r                                      # TTL high: the rise before the exposure, then the exposure
                duty = min(1.0, (pulse + t_r) / period)                  # the fall after it counts too
                Pel = vf(I) * I
                Pheat = Pel - p_opt(I)
                q = Pheat * duty
                Tj_burst = EST["T_air_C"] + q * (EST["Rth_jb_K_W"] + R_tape)          # heat sink still at air temperature (tau >> 15 s)
                Tj_ss = EST["T_air_C"] + q * (EST["Rth_jb_K_W"] + R_tape + hs["R_K_W"])
                rows.append(dict(fps=fps, exposure_us=t_exp, I_pulse_A=I, ttl_high_us=round(pulse, 2), duty=round(duty, 3),
                                 I_avg_A=round(I * duty, 3), VF_V=round(vf(I), 2), P_el_peak_W=round(Pel, 2), P_heat_avg_W=round(q, 2),
                                 Tj_burst_C=round(Tj_burst, 1), Tj_steady_C=round(Tj_ss, 1),
                                 within_ratings=bool(I <= VENDOR["M850LP1"]["I_max_pulsed_A"] and I * duty <= 1.5 and fps <= 27e3),
                                 driver_ok=bool(fps <= 27e3)))
    # continuous (alignment, or the layer camera's raking light)
    for I in (0.75, 1.0, 1.5):
        q = vf(I) * I - p_opt(I)
        rows.append(dict(fps="CW", exposure_us="-", I_pulse_A=I, ttl_high_us="-", duty=1.0, I_avg_A=I, VF_V=round(vf(I), 2),
                         P_el_peak_W=round(vf(I) * I, 2), P_heat_avg_W=round(q, 2),
                         Tj_burst_C=round(EST["T_air_C"] + q * (EST["Rth_jb_K_W"] + R_tape), 1),
                         Tj_steady_C=round(EST["T_air_C"] + q * (EST["Rth_jb_K_W"] + R_tape + hs["R_K_W"]), 1),
                         within_ratings=True, driver_ok=True))
    return rows, R_tape, t_r


# ------------------------------------------------------------------------------------------------ eye safety
def R_weight(lam):
    lam = np.asarray(lam, float)
    return np.where(lam <= 700, 1.0, np.where(lam <= 1050, 10 ** ((700 - lam) / 500), 0.2))


def limits(alpha):
    ca_ir = min(max(alpha, 0.011), 0.1)
    ca_r = min(max(alpha, 0.0017), 0.1)
    return dict(L_IR_weak_stimulus_t_gt_10s=6000 / ca_ir, L_R_10s=50000 / (ca_r * 10 ** 0.25),
                E_IR_1000s=18000 * 1000 ** -0.75, E_IR_100s=18000 * 100 ** -0.75, E_IR_10s=18000 * 10 ** -0.75)


def risk_group(L_Rw, E_IR, alpha):
    lim = limits(alpha)
    rg_E = "exempt" if E_IR <= lim["E_IR_1000s"] else "RG1" if E_IR <= lim["E_IR_100s"] else "RG2" if E_IR <= lim["E_IR_10s"] else "RG3"
    rg_L = "exempt to RG2" if L_Rw <= lim["L_IR_weak_stimulus_t_gt_10s"] else "RG3"
    return dict(by_E_IR=rg_E, by_L_IR=rg_L, limits=lim)


def luminance(L_total, s):
    """Luminance (cd/m2) of a source of total radiance L_total with normalised spectrum s, CIE V(lambda) to 830 nm (extended
    table), halving every 10 nm past it."""
    V = [(700, 4.1e-3), (710, 2.1e-3), (720, 1.05e-3), (730, 5.2e-4), (740, 2.49e-4), (750, 1.2e-4), (760, 6.0e-5), (770, 3.0e-5),
         (780, 1.49e-5), (790, 7.4e-6), (800, 3.7e-6), (810, 1.8e-6), (820, 9.1e-7), (830, 4.5e-7)]
    v = np.where(LAM <= 830, interp(V, LAM), 4.5e-7 * 0.5 ** ((LAM - 830) / 10))
    return 683 * L_total * float(np.trapezoid(s * v, LAM))


# ------------------------------------------------------------------------------------------------ main
def main():
    Lg = layout()
    cg = camera_geometry()
    px = paraxial_gap(Lg)
    # best focus for the ROI: scan the die-to-S2 gap around the paraxial value
    scan = []
    for dg in np.arange(-1.0, 1.01, 0.25):
        r = trace(Lg, px["gap"] + dg, N=120_000, seed=2)
        st, _, _ = bed_stats(r, cg, MS.PLATE_R["M50"])
        scan.append((float(px["gap"] + dg), st["E_roi_mean"], st["P_in_roi"]))
    gap = max(scan, key=lambda s: s[1])[0]
    res = trace(Lg, gap, N=800_000, seed=1, keep=True)            # per watt of LED output
    st, Hm, edges = bed_stats(res, cg, MS.PLATE_R["M50"])
    cs, Hc, cedges = cross_stats(res, Lg)
    elev_bw = MS.elevation_deg(tuple(Lg["c"]))

    R = dict(sources=dict(geometry="cad/monitoring_spec.py, analysis/monitoring/fab/frame_features.py (run time)",
                          vendor=VENDOR, estimates=EST, camera="parts.py CAMS['Chronos 2.1-HD mono'], LENSES['Kowa LM50JC10M 50 mm']"),
             layout=dict(t_S1_mm=Lg["t_S1"], t_tube_front_mm=Lg["t_tube_front"], die_to_S2_mm=gap, paraxial=px,
                         t_die_mm=Lg["t_S1"] + VENDOR["ACL25416U_B"]["ct_mm"] + gap, focus_scan=scan, bw_elevation_deg=elev_bw,
                         sight_vs_wall_normal_deg=math.degrees(math.acos(abs(Lg["d"][1])))),
             camera=dict(wd_mm=cg["wd_mm"], m=cg["m"], um_per_px=cg["um_per_px"], elevation_deg=cg["elev_deg"], roi=cg["roi"],
                         roi_on_bed_mm=(cg["roi_across_mm"], cg["roi_along_bed_mm"])),
             budget_per_W=res["budget"], bed_per_W=st, beam_per_W=cs)

    # ---- the spectrum, the filter and the band
    s_led = led_spectrum()
    R["band"] = {f"{f}, LED at {sh:+.0f} nm": in_band(led_spectrum(sh), f) for f in FILTERS for sh in (0.0, 5.0, 10.0)}
    s_solis = gauss_spectrum(850.0, VENDOR["SOLIS_850C"]["fwhm_nm"])
    R["band"]["FBH850-10, SOLIS-850C"] = in_band(s_solis, "FBH850-10")
    R["band"]["FBH850-40, SOLIS-850C"] = in_band(s_solis, "FBH850-40")

    # ---- electrons per pixel (10 and 20 us, f/4) from each source
    def bed_e(E_W_cm2, t, filt="FBH850-10", s=s_led, N=4.0):
        L = EST["rho_bed"] / math.pi * E_W_cm2 * 1e4 * s          # W m^-2 sr^-1 nm^-1
        return e_per_px(L, t, N=N, filt=filt, cg=cg)
    cases = {}
    for I in (1.5, 2.0):
        for which in ("typ", "min"):
            P = p_opt(I, which)
            for t in (10.0, 20.0):
                for filt in ("FBH850-10", "FBH860-10", "FBH850-40"):
                    cases[f"bed, {I:g} A ({which} {P:.2f} W), {t:g} us, {filt}"] = dict(
                        E_bed_W_cm2=st["E_roi_mean"] * P, e=bed_e(st["E_roi_mean"] * P, t, filt), e_min_cell=bed_e(st["E_roi_min"] * P, t, filt),
                        e_max_cell=bed_e(st["E_roi_max"] * P, t, filt))
    R["lit_bed"] = cases
    # particles in the beam: a specular sphere (glint) and its share in one pixel
    Omega_p = math.pi * (LENS["f_mm"] / 8.0) ** 2 / cg["wd_mm"] ** 2     # f/4 pupil seen from the plate
    qe = interp(CAM["qe"], LAM)
    k_e = {fl: float(np.trapezoid(s_led * filt_T(fl) * qe * LAM * 1e-9 / (H * C), LAM)) for fl in ("FBH850-10", "FBH850-40")}
    parts_ = {}
    for I in (1.5, 2.0):
        In = cs["E_at_height"]["1 mm"] * p_opt(I) * 1e4                    # W/m^2 across the beam, 1 mm above the bed
        for D_um in (20, 45, 63, 100):
            for Rp in (0.5, 0.85):
                J = Rp * In * (D_um * 1e-6 / 2) ** 2 / 4                        # W/sr, specular sphere (isotropic)
                for t in (10.0, 20.0):
                    for fl, ke in k_e.items():
                        sfx = "" if fl == "FBH850-10" else ", FBH850-40"
                        parts_[f"{D_um} um sphere, R {Rp}, {I:g} A, {t:g} us{sfx}"] = J * Omega_p * EST["tau_cam"] * t * 1e-6 * ke * EST["glint_px_fraction"]
    R["lit_particles_peak_px_e"] = parts_
    R["particle_beam_W_m2_at_1mm"] = {f"{I:g} A": cs["E_at_height"]["1 mm"] * p_opt(I) * 1e4 for I in (1.5, 2.0)}
    # self-emission in the same band
    th_cam = math.radians(90 - cg["elev_deg"])

    def eps_dir(T_K, theta):
        lam_um = LAM / 1000
        w_ = 2 * math.pi * C / (lam_um * 1e-6)
        T_ = max(T_K, 933.0)
        rho_e = (24.2 + 0.0145 * (T_ - 933.0)) * 1e-8
        dens = 2377.0 - 0.311 * (T_ - 933.0)
        n_e = 3 * dens / 0.0269815 * RM.NA_
        wp2 = n_e * RM.EV ** 2 / (RM.EPS0 * RM.ME)
        gam = RM.EPS0 * wp2 * rho_e
        eps = 1 - wp2 / (w_ * w_ + 1j * gam * w_)
        ci = math.cos(theta)
        si2 = math.sin(theta) ** 2
        ct = np.sqrt(eps - si2)
        rs = np.abs((ci - ct) / (ci + ct)) ** 2
        rp = np.abs((eps * ci - ct) / (eps * ci + ct)) ** 2
        e_th = 1 - 0.5 * (rs + rp)
        scale = 0.12 / float(RM.eps_liquid_drude(1.0, 933.0))          # optics.md §3: scaled to 0.12 at 1 um (normal)
        return e_th * scale, float(np.interp(850, LAM, (1 - np.abs((1 - np.sqrt(eps)) / (1 + np.sqrt(eps))) ** 2) * scale))
    self_ = {}
    for T_K in (1500.0, 2000.0, 2500.0, 2763.0):
        e_th, e_n = eps_dir(T_K, th_cam)
        L = e_th * RM.planck(LAM / 1000, T_K)
        for t in (10.0, 20.0):
            self_[f"melt pool {T_K:.0f} K (eps {float(np.interp(850, LAM, e_th)):.3f} at {math.degrees(th_cam):.0f} deg; {e_n:.3f} normal), {t:g} us"] = e_per_px(L, t, cg=cg)
            self_[f"melt pool {T_K:.0f} K, {t:g} us, FBH850-40"] = e_per_px(L, t, cg=cg, filt="FBH850-40")
    for tau_p, T_K in ((2e-3, 2000.0), (1e-2, 2700.0)):
        L = tau_p * RM.planck(LAM / 1000, T_K)
        for t in (10.0, 20.0):
            self_[f"plume, optical depth {tau_p:g} at {T_K:.0f} K, {t:g} us"] = e_per_px(L, t, cg=cg)
            self_[f"plume, optical depth {tau_p:g} at {T_K:.0f} K, {t:g} us, FBH850-40"] = e_per_px(L, t, cg=cg, filt="FBH850-40")
    for T_K in (1500.0, 2000.0, 2200.0):
        L = 0.15 * RM.planck(LAM / 1000, T_K)
        for t in (10.0, 20.0):
            self_[f"hot spatter {T_K:.0f} K (grey 0.15), {t:g} us"] = e_per_px(L, t, cg=cg)
            self_[f"hot spatter {T_K:.0f} K (grey 0.15), {t:g} us, FBH850-40"] = e_per_px(L, t, cg=cg, filt="FBH850-40")
    R["self_emission_e_per_px"] = self_
    # SOLIS-850C at BW, if it fit: Thorlabs' maximum irradiance at 200 mm, through the window (as this trace: T 0.90), raking 10 deg
    T_win = res["budget"]["on the bed, inside the chamber"] / max(1e-12, res["budget"]["on the bed, inside the chamber"]
                                                                 + res["budget"]["reflected by the window's two faces (back out, outside the chamber)"]
                                                                 + res["budget"]["absorbed / multiply reflected in the window"])
    E_solis_beam = VENDOR["SOLIS_850C"]["Ee_200mm_mW_mm2"] * 0.1                     # W/cm^2 across the beam (upper bound at 200 mm)
    E_solis_bed = E_solis_beam * math.sin(math.radians(elev_bw)) * T_win
    R["solis"] = {f"{t:g} us, {f}": bed_e(E_solis_bed, t, f, s_solis) for t in (10.0, 20.0) for f in ("FBH850-10", "FBH850-40")}
    R["solis"]["E_bed_W_cm2_upper_bound"] = E_solis_bed
    R["solis"]["E_beam_W_cm2_at_200mm"] = E_solis_beam
    # what viewports.py asked for: half full well at 10 us
    R["half_full_well_e"] = 0.5 * CAM["fwc_e"]
    R["read_noise_e"] = CAM["read_e"]

    # ---- drive and heat
    hs = heat_sink_Rth()
    rows, R_tape, t_r = drive_table(hs)
    R["heat_sink"] = hs
    R["R_tape_K_W"] = R_tape
    R["dc2200_edge_us"] = t_r
    R["drive"] = rows
    # the warm LED: Thorlabs measured the spectrum with the board's back at 25 C at 1.5 A, i.e. the junction at ~25 + 3.4 W x (R_jb + tape)
    Tj_test = 25.0 + (vf(1.5) * 1.5 - p_opt(1.5)) * (EST["Rth_jb_K_W"] + R_tape)
    hot = {}
    for r in rows:
        if r["fps"] == 24046 and r["I_pulse_A"] == 2.0:
            for state in ("Tj_burst_C", "Tj_steady_C"):
                dT = r[state] - Tj_test
                sh = EST["dlam_dT_nm_K"] * dT
                hot[f"24 kfps, {r['exposure_us']:g} us, 2 A, {state[3:-2]}"] = dict(
                    Tj_C=r[state], shift_nm=round(sh, 1), output_factor=round(1 + EST["dPdT_per_K"] * dT, 3),
                    in_band={fl: round(in_band(led_spectrum(sh), fl), 3) for fl in ("FBH850-10", "FBH860-10", "FBH870-10", "FBH850-40")})
    R["warm_led"] = dict(Tj_at_Thorlabs_test_C=Tj_test, cases=hot)

    # ---- eye safety
    P_beam_typ = p_opt(1.5)
    ca = VENDOR["ACL25416U_B"]["ca_mm"]
    s_img = px["s_img"]
    Omega_img = math.pi * (ca / 2) ** 2 / s_img ** 2
    E_img_peak = cs["E_peak"] * P_beam_typ * 1e4                                    # W/m^2, 1.5 A CW
    L_ap = E_img_peak / Omega_img / T_win                                            # radiance of the filled aperture, before the window
    Rw = float(np.trapezoid(s_led * R_weight(LAM), LAM))
    alpha_img = ca / s_img
    eye = dict(R_weight_mean=Rw, luminance_cd_m2=luminance(L_ap, s_led), alpha_at_image_rad=alpha_img)
    # bare LED, for the check against Thorlabs' RG0: on-axis intensity from the measured pattern and 1.6 W; FOV-averaged at 200 mm
    th = np.radians(np.arange(0, 90.01, 0.5))
    I0 = VENDOR["M850D3"]["P_typ_W"] / float(np.trapezoid(interp(LED_ANG, np.degrees(th)) * 2 * np.pi * np.sin(th), th))
    L_bare = I0 / 1e-6
    a_bare = 1.0 / 200.0
    L_bare_fov = L_bare * (a_bare / 0.011) ** 2
    E_bare = I0 / 0.2 ** 2
    eye["bare_LED"] = dict(I0_W_sr=I0, I0_from_Thorlabs_Ee_W_sr=VENDOR["M850D3"]["Ee_200mm_uW_mm2"] * 0.04,
                           L_W_m2_sr=L_bare, L_R_weighted_FOV_0p011=L_bare_fov * Rw, E_IR_200mm=E_bare,
                           group=risk_group(L_bare_fov * Rw, E_bare, 0.011), thorlabs="RG0")
    for I, duty, label in ((1.5, 1.0, "CW 1.5 A"), (2.0, 0.6, "2.0 A pulses at 60 % duty (24 kfps, 20 us), time-averaged"),
                           (2.0, 0.36, "2.0 A pulses at 36 % duty (24 kfps, 10 us), time-averaged")):
        k = p_opt(I) / P_beam_typ * duty
        eye[label] = dict(L_R_weighted_aperture=L_ap * Rw * k, E_IR_image_peak=E_img_peak * k,
                          E_IR_image_7mm=cs["E_7mm_pupil"] * p_opt(I) * duty * 1e4,
                          group=risk_group(L_ap * Rw * k, E_img_peak * k, alpha_img))
    # the guard's viewing panel: what can reach it is scattered light only; the brightest diffuse surface is the lit bed
    L_bed = EST["rho_bed"] / math.pi * st["E_peak"] * p_opt(2.0) * 1e4
    eye["lit_bed_radiance_R_weighted"] = L_bed * Rw
    # the window's reflection: where it goes (outside the chamber, inside the guard)
    rp, rd, rw = res["refl_p"], res["refl_d"], res["refl_w"]
    post = dict(x=(-120.0, -100.0), y=(131.0, 151.0), z=(-160.0, 50.0))
    s_post = (post["y"][0] - rp[:, 1]) / rd[:, 1]
    qp = rp + s_post[:, None] * rd
    hit_post = (qp[:, 0] >= post["x"][0]) & (qp[:, 0] <= post["x"][1]) & (qp[:, 2] <= post["z"][1])
    s_pan = (215.0 - rp[:, 1]) / rd[:, 1]
    qpan = rp + s_pan[:, None] * rd
    Wr = float(rw.sum())
    spot = qpan[~hit_post]
    sp_area = max(1e-6, (np.percentile(spot[:, 0], 90) - np.percentile(spot[:, 0], 10)) * (np.percentile(spot[:, 2], 90) - np.percentile(spot[:, 2], 10)) / 100) if len(spot) > 100 else 1.0
    eye["window_reflection"] = dict(W_per_W=Wr, share_on_recoater_post=float(rw[hit_post].sum() / Wr),
                                    share_to_guard_back_panel=float(rw[~hit_post].sum() / Wr),
                                    panel_spot_centre=np.round(qpan[~hit_post].mean(axis=0), 1).tolist() if (~hit_post).any() else None,
                                    panel_E_W_m2_at_2A=float(rw[~hit_post].sum() * p_opt(2.0) / sp_area * 1e4) if (~hit_post).any() else 0.0)
    # bare plate, specular, chamber door open: reflect at z = 0 the rays that land on the plate (M50), follow them
    land, w, din = res["land"], res["w"], res["dir_in"]
    onp = np.hypot(land[:, 0], land[:, 1]) <= MS.PLATE_R["M50"]
    dref = din[onp] * np.array([1, 1, -1.0])
    p0 = land[onp]
    s_front = (-95.0 - p0[:, 1]) / dref[:, 1]
    s_right = (140.0 - p0[:, 0]) / dref[:, 0]
    s_lid = (120.0 - p0[:, 2]) / dref[:, 2]
    s_hit = np.minimum(np.where(s_front > 0, s_front, 1e9), np.minimum(np.where(s_right > 0, s_right, 1e9), np.where(s_lid > 0, s_lid, 1e9)))
    qd = p0 + s_hit[:, None] * dref
    thru_door = (np.abs(qd[:, 1] + 95.0) < 1e-6) & (np.abs(qd[:, 0]) <= 110) & (qd[:, 2] >= 8) & (qd[:, 2] <= 100)
    W_door = float(w[onp][thru_door].sum())
    if thru_door.any():
        qq = qd[thru_door]
        path = float(np.mean(s_img + np.linalg.norm(p0[thru_door] - 0, axis=1) + s_hit[thru_door]))
        ar = max(1e-6, (np.percentile(qq[:, 0], 95) - np.percentile(qq[:, 0], 5)) * (np.percentile(qq[:, 2], 95) - np.percentile(qq[:, 2], 5)) / 100)
        # on to the guard's front (lpbf_low: guard y -265; fixed panels x -420..-320 and 180..310; the sliding door between, with
        # the viewing window at x -300..160 and y -271.5..-269.5)
        dq = dref[thru_door]
        s_g = (-270.5 - qq[:, 1]) / dq[:, 1]
        qg = qq + s_g[:, None] * dq
        wg = w[onp][thru_door]
        in_view = (qg[:, 0] >= -300) & (qg[:, 0] <= 160)
        on_fixed = (qg[:, 0] >= 180) & (qg[:, 0] <= 310)
        guard = dict(share_to_viewing_window=float(wg[in_view].sum() / wg.sum()), share_to_fixed_front_panel=float(wg[on_fixed].sum() / wg.sum()),
                     share_elsewhere=float(wg[~in_view & ~on_fixed].sum() / wg.sum()), mean_hit=np.round(qg.mean(axis=0), 1).tolist(),
                     x_range=[float(np.percentile(qg[:, 0], 1)), float(np.percentile(qg[:, 0], 99))])
        for R_plate in (0.85,):
            E_door = W_door * P_beam_typ * R_plate / ar * 1e4
            L_door = L_ap * T_win * R_plate * Rw
            eye["bare_plate_specular_through_open_door"] = dict(
                plate_R=R_plate, share_of_beam=W_door / max(1e-12, float(w.sum())), door_hit_mean=np.round(qq.mean(axis=0), 1).tolist(),
                E_IR_at_door_W_m2_CW=E_door, L_R_weighted=L_door, alpha_rad=ca / path, path_mm=path,
                group=risk_group(L_door, E_door, ca / path), at_guard_front=guard,
                I_max_CW_A_below_L_IR=float(1.5 * min(1.0, limits(ca / path)["L_IR_weak_stimulus_t_gt_10s"] / L_door)))
    else:
        eye["bare_plate_specular_through_open_door"] = dict(share_of_beam=0.0)
    R["eye"] = eye
    R["focus_scan_note"] = "die-to-S2 gaps scanned around the paraxial conjugate; the one with the highest mean bed irradiance in the ROI is used"
    (OUT / "bw_light.json").write_text(json.dumps(R, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)) + "\n")
    figure(R, Hm, edges, cg, Hc, cedges)
    write_md(R)
    return R


def figure(R, Hm, edges, cg, Hc, cedges):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    ramp = ["#ffffff", "#cce3fd", "#9dc8f7", "#6aabf1", "#338ced", "#2370cd", "#1757ac", "#0e3d7e"]
    cmap = LinearSegmentedColormap.from_list("blue", ramp)
    ink, ink2, grid = "#191919", "#666666", "#d9d9d9"
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw=dict(width_ratios=[1, 1.3]))
    P = p_opt(2.0)
    im = a1.imshow((Hm * P).T, origin="lower", extent=[edges[0], edges[-1], edges[0], edges[-1]], cmap=cmap, vmin=0)
    cb = fig.colorbar(im, ax=a1, shrink=0.85)
    cb.set_label("bed irradiance at 2.0 A (W/cm²)", color=ink2)
    hw, hl = cg["roi_across_mm"] / 2, cg["roi_along_bed_mm"] / 2
    corners = np.array([[sx * hw * cg["across"][0] + sy * hl * cg["vh"][0], sx * hw * cg["across"][1] + sy * hl * cg["vh"][1]]
                        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1))])
    a1.plot(corners[:, 0], corners[:, 1], color=ink, lw=1.5)
    a1.annotate("side camera's field\n(640 × 96 px at 24 kfps)", xy=corners[1], xytext=(14, -48), textcoords="data", color=ink, fontsize=9,
                arrowprops=dict(arrowstyle="-", color=ink2, lw=0.8))
    t = np.linspace(0, 2 * np.pi, 200)
    rp = MS.PLATE_R["M50"]
    a1.plot(rp * np.cos(t), rp * np.sin(t), color=ink2, lw=1, ls="--")
    a1.text(-rp * 0.2, rp * 1.08, "M50 plate", color=ink2, fontsize=9)
    a1.annotate("light from BW", xy=(-30, 27), xytext=(-55, 48), color=ink2, fontsize=9, arrowprops=dict(arrowstyle="->", color=ink2))
    a1.annotate("to the LW camera", xy=(-57, -22), xytext=(-37, -22), color=ink2, fontsize=9, va="center",
                arrowprops=dict(arrowstyle="<-", color=ink2))
    a1.set_xlim(-60, 60)
    a1.set_ylim(-60, 60)
    a1.set_xlabel("x (mm)", color=ink2)
    a1.set_ylabel("y (mm)", color=ink2)
    a1.set_title("Where the M850D3's light lands (ray trace)", color=ink, fontsize=11, loc="left")
    # electrons per pixel, log scale, two exposures
    P2 = p_opt(2.0)
    rows = [("bed lit at 2.0 A, FBH850-10", "bed", "bed, 2 A (typ %.2f W), {t} us, FBH850-10" % P2),
            ("bed lit at 2.0 A, FBH850-40", "bed", "bed, 2 A (typ %.2f W), {t} us, FBH850-40" % P2),
            ("bed lit by a SOLIS-850C at BW, FBH850-10", "solis", "{t} us, FBH850-10"),
            ("45 µm powder glint (R 0.5), 2.0 A", "part", "45 um sphere, R 0.5, 2 A, {t} us"),
            ("hot spatter 2,000 K (own light)", "self", "hot spatter 2000 K (grey 0.15), {t} us"),
            ("hot spatter 1,500 K (own light)", "self", "hot spatter 1500 K (grey 0.15), {t} us"),
            ("plume, τ 0.002 at 2,000 K (own light)", "self", "plume, optical depth 0.002 at 2000 K, {t} us"),
            ("melt pool 2,000 K (own light)", "pool", "melt pool 2000 K"),
            ("melt pool 2,500 K (own light)", "pool", "melt pool 2500 K")]
    labels, v10, v20 = [], [], []
    for lab, kind, key in rows:
        vals = []
        for tt in ("10", "20"):
            if kind == "bed":
                vals.append(R["lit_bed"][key.format(t=tt)]["e"])
            elif kind == "solis":
                vals.append(R["solis"][key.format(t=tt)])
            elif kind == "part":
                vals.append(R["lit_particles_peak_px_e"][key.format(t=tt)])
            elif kind == "self":
                vals.append(R["self_emission_e_per_px"][key.format(t=tt)])
            else:
                k = next(k for k in R["self_emission_e_per_px"] if k.startswith(key) and k.endswith(f", {tt} us"))
                vals.append(R["self_emission_e_per_px"][k])
        labels.append(lab)
        v10.append(vals[0])
        v20.append(vals[1])
    y = np.arange(len(labels))[::-1]
    a2.axvline(R["read_noise_e"], color=ink2, lw=1, ls=":")
    a2.axvline(15000, color=ink2, lw=1, ls=":")
    a2.text(R["read_noise_e"] * 1.1, y[0] + 0.55, "read noise", color=ink2, fontsize=8)
    a2.text(15000 * 1.1, y[0] + 0.55, "full well", color=ink2, fontsize=8)
    for yy, a_, b_ in zip(y, v10, v20):
        a2.plot([a_, b_], [yy, yy], color=grid, lw=2, zorder=1)
    a2.scatter(v10, y, s=64, color="#257de0", label="10 µs", zorder=3, edgecolor="white", linewidth=2)
    a2.scatter(v20, y, s=64, color="#f47230", label="20 µs", zorder=3, edgecolor="white", linewidth=2)
    for yy, b_ in zip(y, v20):
        a2.text(b_ * 1.35, yy, f"{b_:,.0f}" if b_ >= 10 else f"{b_:.2g}", va="center", fontsize=8, color=ink)
    a2.set_xscale("log")
    a2.set_xlim(0.05, 3e6)
    a2.set_yticks(y)
    a2.set_yticklabels(labels, fontsize=9, color=ink)
    a2.set_xlabel("photo-electrons per pixel per exposure (Chronos 2.1-HD at LW, f/4)", color=ink2)
    a2.set_ylim(y[-1] - 0.7, y[0] + 1.0)
    a2.grid(axis="x", color=grid, lw=0.6)
    a2.set_axisbelow(True)
    for sp in ("top", "right"):
        a2.spines[sp].set_visible(False)
        a1.spines[sp].set_visible(False)
    a2.legend(loc="upper right", frameon=False, fontsize=9)
    a2.set_title("Light against the process's own glow (per pixel)", color=ink, fontsize=11, loc="left")
    fig.tight_layout()
    fig.savefig(OUT / "bw_light.png", dpi=130)
    plt.close(fig)


def write_md(R):
    f = lambda x, n=0: f"{x:,.{n}f}"   # noqa: E731
    L = ["# The BW light: M850D3 + ACL25416U-B imaged onto the plate (generated by analysis/monitoring/optics/bw_light.py)", ""]
    lo = R["layout"]
    L += [f"- Asphere vertex {lo['t_S1_mm']:.1f} mm out along the sight line from the port centre; tube front {lo['t_tube_front_mm']:.1f} mm; "
          f"die {lo['die_to_S2_mm']:.2f} mm behind S2 (paraxial {lo['paraxial']['gap']:.2f}), {lo['t_die_mm']:.1f} mm out; image {lo['paraxial']['s_img']:.0f} mm "
          f"from the lens, magnification {lo['paraxial']['m']:.1f}.",
          f"- Camera: working distance {R['camera']['wd_mm']:.0f} mm, {R['camera']['um_per_px']:.1f} um/px, ROI {R['camera']['roi'][0]} x {R['camera']['roi'][1]} px = "
          f"{R['camera']['roi_on_bed_mm'][0]:.1f} x {R['camera']['roi_on_bed_mm'][1]:.1f} mm on the bed.", ""]
    L += ["## Where 1 W of LED light goes", "", "| | W per W emitted |", "|---|---:|"]
    for k, v in R["budget_per_W"].items():
        L.append(f"| {k} | {v:.3f} |")
    b = R["bed_per_W"]
    c = R["beam_per_W"]
    L += ["", f"Per W emitted: bed irradiance in the camera's field {b['E_roi_mean']:.3f} W/cm² mean ({b['E_roi_min']:.3f}-{b['E_roi_max']:.3f} over 1 mm "
          f"cells), {b['P_in_roi']:.3f} W in the field ({b['roi_cm2']:.2f} cm²), {b['P_on_plate']:.3f} W on the M50 plate. Across the beam at the plate "
          f"centre: {c['E_peak']:.2f} W/cm² peak, FWHM {c['fwhm_side_mm']:.1f} mm wide x {c['fwhm_up_mm']:.1f} mm high.", ""]
    L += ["## In band", "", "| filter, source | share of the light through FBH + FESH1000 |", "|---|---:|"]
    for k, v in R["band"].items():
        L.append(f"| {k} | {v:.3f} |")
    L += ["", "## Electrons per pixel (half full well = %s, read noise %s)" % (f(R["half_full_well_e"]), f(R["read_noise_e"])), "",
          "| case | E bed (W/cm²) | e⁻/px mean | min-max cell |", "|---|---:|---:|---:|"]
    for k, v in R["lit_bed"].items():
        L.append(f"| {k} | {v['E_bed_W_cm2']:.3f} | {f(v['e'])} | {f(v['e_min_cell'])}-{f(v['e_max_cell'])} |")
    L += ["", "| particle in the beam (peak pixel) | e⁻ |", "|---|---:|"]
    for k, v in R["lit_particles_peak_px_e"].items():
        L.append(f"| {k} | {f(v)} |")
    L += ["", "| own light | e⁻/px |", "|---|---:|"]
    for k, v in R["self_emission_e_per_px"].items():
        L.append(f"| {k} | {v:,.3g} |")
    L += ["", "| SOLIS-850C at BW (if it fit) | e⁻/px |", "|---|---:|"]
    for k, v in R["solis"].items():
        L.append(f"| {k} | {v:,.3g} |")
    L += ["", "## The warm LED (spectrum shift and output against Thorlabs' test)", "",
          f"Junction at Thorlabs' test (board 25 C, 1.5 A): ~{R['warm_led']['Tj_at_Thorlabs_test_C']:.0f} C (estimate).", "",
          "| case | Tj (C) | shift (nm) | output | FBH850-10 | FBH860-10 | FBH870-10 | FBH850-40 |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for k, v in R["warm_led"]["cases"].items():
        ib = v["in_band"]
        L.append(f"| {k} | {v['Tj_C']} | {v['shift_nm']} | {v['output_factor']} | {ib['FBH850-10']} | {ib['FBH860-10']} | {ib['FBH870-10']} | {ib['FBH850-40']} |")
    L += ["", "## Drive and heat", "", f"Heat sink: R {R['heat_sink']['R_K_W']:.1f} K/W to 40 C air, {R['heat_sink']['mass_g']:.0f} g, "
          f"time constant {R['heat_sink']['tau_s']:.0f} s; tape {R['R_tape_K_W']:.2f} K/W; junction to board {EST['Rth_jb_K_W']} K/W (estimate). "
          f"DC2200 edge {R['dc2200_edge_us']:.2f} us (LED2, 27 kHz).", "",
          "| fps | exposure (us) | I pulse (A) | TTL high (us) | duty | I avg (A) | VF (V) | heat avg (W) | Tj, burst (C) | Tj, steady (C) | within ratings |",
          "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for r in R["drive"]:
        L.append(f"| {r['fps']} | {r['exposure_us']} | {r['I_pulse_A']} | {r['ttl_high_us']} | {r['duty']} | {r['I_avg_A']} | {r['VF_V']} | "
                 f"{r['P_heat_avg_W']} | {r['Tj_burst_C']} | {r['Tj_steady_C']} | {'yes' if r['within_ratings'] else 'no'} |")
    e = R["eye"]
    L += ["", "## Eye safety (IEC 62471 / 2006/25/EC exposure limits)", "",
          f"R(λ)-weighted share of the LED's light {e['R_weight_mean']:.3f}; luminance of the lit aperture ~{e['luminance_cd_m2']:.0f} cd/m² "
          f"(CIE V(λ) tail, rough); apparent source at the image {e['alpha_at_image_rad']:.3f} rad.", "",
          "| case | L_R weighted (W/m²/sr) | E_IR (W/m²) | by E_IR | by L_IR |", "|---|---:|---:|---|---|"]
    bl = e["bare_LED"]
    L.append(f"| bare LED at 200 mm (Thorlabs: RG0) | {bl['L_R_weighted_FOV_0p011']:,.0f} (0.011 rad FOV) | {bl['E_IR_200mm']:.1f} | {bl['group']['by_E_IR']} | {bl['group']['by_L_IR']} |")
    for k in [k for k in e if k.startswith("CW") or k.startswith("2.0 A")]:
        v = e[k]
        L.append(f"| in the beam at its image: {k} | {v['L_R_weighted_aperture']:,.0f} | {v['E_IR_image_peak']:,.0f} (7 mm: {v['E_IR_image_7mm']:,.0f}) | "
                 f"{v['group']['by_E_IR']} | {v['group']['by_L_IR']} |")
    d = e.get("bare_plate_specular_through_open_door", {})
    if d.get("share_of_beam", 0) > 0:
        L.append(f"| bare plate's specular reflection through the open chamber door (CW 1.5 A, R {d['plate_R']}) | {d['L_R_weighted']:,.0f} | "
                 f"{d['E_IR_at_door_W_m2_CW']:,.0f} | {d['group']['by_E_IR']} | {d['group']['by_L_IR']} |")
    if d.get("share_of_beam", 0) > 0:
        g_ = d["at_guard_front"]
        L += ["", f"Open chamber door, bare plate: {d['share_of_beam']:.0%} of the light on the bed leaves through the door (mean exit {d['door_hit_mean']}); "
              f"at the guard's front {g_['share_to_viewing_window']:.0%} reaches the viewing window, {g_['share_to_fixed_front_panel']:.0%} the fixed panel "
              f"(x {g_['x_range'][0]:.0f} to {g_['x_range'][1]:.0f}), {g_['share_elsewhere']:.0%} elsewhere. Below the L_IR limit at <= {d['I_max_CW_A_below_L_IR']:.2f} A CW."]
    wr = e["window_reflection"]
    L += ["", f"Window reflection: {wr['W_per_W']:.3f} W per W, {wr['share_on_recoater_post']:.0%} onto the recoater sensor post, "
          f"{wr['share_to_guard_back_panel']:.0%} to the guard's back panel (opaque) near {wr['panel_spot_centre']}, ~{wr['panel_E_W_m2_at_2A']:.0f} W/m² there at 2 A.",
          f"Brightest diffuse surface (the lit bed), R-weighted: {e['lit_bed_radiance_R_weighted']:.0f} W/m²/sr."]
    lim = limits(e["alpha_at_image_rad"])
    L += ["", "Limits used: " + ", ".join(f"{k} {v:,.0f}" for k, v in lim.items())]
    (OUT / "bw_light.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    R = main()
    b = R["bed_per_W"]
    print(json.dumps(dict(layout={k: v for k, v in R["layout"].items() if k != "focus_scan"}, budget=R["budget_per_W"], bed=b,
                          beam=R["beam_per_W"]), indent=1, default=str)[:4000])
