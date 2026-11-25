"""Mechanics checks for the in-situ monitoring hardware (issue #260, PR 281): windows, seals and clamps, the side camera's
bracket, the coaxial cage, the lid camera against the optics bridge, the acoustic-emission path, and temperatures at the ports.

Every geometric number is read at run time from cad/monitoring_spec.py, cad/lpbf_low.py, cad/module_params.py, the
ports as programmed (analysis/out/monitoring/fab/frame_features.json), monitoring-bom.csv, the module thermal FEA
(thermal.json) and fea.json; the
constants that are not in the repo are in mech_inputs.py with their sources. bridge_modal.py (CalculiX) writes
bridge_modal.json, which check 5 reads if it exists.

Run:  /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/mech/mech_monitoring.py
Writes analysis/out/monitoring/mech/checks.json, checks.md and checks.png.
"""
from __future__ import annotations

import csv
import json
import math
import pathlib
import re
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mech_inputs as MI  # noqa: E402

MS, MP, P = MI.MS, MI.MP, MI.P
ROOT = MI.ROOT
OUT = ROOT / "analysis" / "out" / "monitoring" / "mech"
sys.path.insert(0, str(ROOT / "analysis" / "monitoring" / "optics"))
import parts as OPT  # noqa: E402  (camera and lens data, analysis/monitoring/optics/parts.py)

G = 9.81
SIGMA = 5.670374e-8
VLM_AIR = (30.0, 43.0)      # C: air round the machine in the Shuttle, typical build and PR 318's busy case (heat.md §2)


def bom_rows():
    with open(ROOT / "monitoring-bom.csv", newline="") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def disc_dims(text):
    m = re.search(r"Ø([\d.]+) x ([\d.]+) mm", text)
    return (float(m.group(1)), float(m.group(2))) if m else None


# ============================================================================================ 1. windows and slides
def disc_window(name, d, t, a, glass="fused silica", p=MI.P_ATM):
    g = MI.GLASS[glass]
    s = MI.K_SS * p * a ** 2 / t ** 2
    D = g["E"] * t ** 3 / (12 * (1 - g["nu"] ** 2))
    w = p * a ** 4 * (5 + g["nu"]) / (64 * D * (1 + g["nu"]))          # Roark Table 11.2 case 10a, centre deflection
    t_req = a * math.sqrt(MI.K_SS * p * MI.SF_WINDOW / g["MR"]) if g["MR"] else None
    R = a ** 2 / (2 * w) if w > 0 else float("inf")                       # bent window ~ meniscus, both radii R
    n = 1.45
    f_m = n * R ** 2 / ((n - 1) ** 2 * t) / 1000.0
    out = dict(port=name, glass=glass, d_mm=d, t_mm=t, unsupported_r_mm=a, p_MPa=p, sigma_MPa=s, MR_MPa=g["MR"],
               SF=(g["MR"] / s) if g["MR"] else None, t_needed_SF4_mm=t_req, deflection_um=w * 1000, window_focal_m=f_m,
               MR_needed_for_SF4_MPa=MI.SF_WINDOW * s)
    out["pass"] = bool(out["SF"] and out["SF"] >= MI.SF_WINDOW)
    return out


def rect_window(name, L, W, t, span_a, span_b, glass="fused silica", p=MI.P_ATM):
    """Rectangular plate simply supported on all edges (Roark Table 11.4 case 1a), spans a x b (b the short one)."""
    g = MI.GLASS[glass]
    ab = span_a / span_b
    tab_r = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 3.0, 4.0, 5.0, 1e9]
    tab_beta = [0.2874, 0.3762, 0.4530, 0.5172, 0.5688, 0.6102, 0.7134, 0.7410, 0.7476, 0.7500]
    tab_alpha = [0.0444, 0.0616, 0.0770, 0.0906, 0.1017, 0.1110, 0.1335, 0.1400, 0.1417, 0.1421]
    beta = float(np.interp(ab, tab_r, tab_beta))
    alpha = float(np.interp(ab, tab_r, tab_alpha))
    s = beta * p * span_b ** 2 / t ** 2
    w = alpha * p * span_b ** 4 / (g["E"] * t ** 3)
    out = dict(port=name, glass=glass, size_mm=(L, W, t), spans_mm=(span_a, span_b), beta=beta, p_MPa=p, sigma_MPa=s,
               MR_MPa=g["MR"], SF=(g["MR"] / s) if g["MR"] else None,
               t_needed_SF4_mm=span_b * math.sqrt(beta * p * MI.SF_WINDOW / g["MR"]) if g["MR"] else None,
               deflection_um=w * 1000, MR_needed_for_SF4_MPa=MI.SF_WINDOW * s)
    out["pass"] = bool(out["SF"] and out["SF"] >= MI.SF_WINDOW)
    return out


def slide_thermal(name, d, t, port_centre, T_plate=200.0, T_ch=(25.0, 60.0), eps_plate=0.5, T_spatter=933.0):
    """Cover slide: radiation it absorbs from the hot plate (fused silica is opaque past ~4 um, so it takes the plate's
    thermal IR), the centre-to-rim rise that gives (rim held by its clip), the stress, and a molten-Al spatter quench."""
    g = MI.GLASS["fused silica"]
    dist = math.dist(port_centre, MS.TARGET)
    elev = math.radians(MS.elevation_deg(port_centre))
    out = []
    for key, r_p in MS.PLATE_R.items():
        A_p = math.pi * (r_p * 1e-3) ** 2
        F = A_p * math.sin(elev) / (math.pi * (dist * 1e-3) ** 2)         # view factor slide -> plate (small, facing the plate)
        for tc in T_ch:
            q = eps_plate * SIGMA * ((T_plate + 273.15) ** 4 - (tc + 273.15) ** 4) * F    # W/m2 on the slide
            a = d / 2 * 1e-3
            dT = q * a ** 2 / (4 * g["k"] * t * 1e-3)                    # disc heated on one face, rim at T_ch
            out.append(dict(plate=key, T_ch=tc, view_factor=F, q_W_m2=q, dT_centre_rim_K=dT,
                            sigma_MPa=g["E"] * g["alpha"] * dT / 2))
    R_shock = g["MR"] * (1 - g["nu"]) / (g["E"] * g["alpha"])            # K, first thermal-shock parameter
    worst = max(out, key=lambda r: r["dT_centre_rim_K"])
    dT_spatter = T_spatter - (min(T_ch) + 273.15)
    return dict(port=name, d_mm=d, t_mm=t, rows=out, worst=worst, R_thermal_shock_K=R_shock, spatter_quench_K=dT_spatter,
                pass_=worst["sigma_MPa"] < g["MR"] / MI.SF_WINDOW and dT_spatter < R_shock)


def check_windows():
    B = bom_rows()
    ff = MI.FRAME_FEATURES
    lw_a = ff["LW"]["bore"]["d"] / 2
    bw_slot = ff["BW"]["slot"]
    lp_a = MS.VIEWPORTS["LP"]["clear_d"] / 2 + 0.5           # the layer camera's flat gasket has ID 21 for a Ø20 aperture
    rows = []
    spec = MS.VIEWPORTS
    lw_cat = disc_dims(B["M0-01"]["element"])
    rows.append(disc_window("LW (spec Ø38.1 x 5)", spec["LW"]["window"]["d"], spec["LW"]["window"]["t"], lw_a))
    rows.append(disc_window(f"LW (catalogue 36-983, Ø{lw_cat[0]:g} x {lw_cat[1]:g})", lw_cat[0], lw_cat[1], lw_a))
    lp_cat = disc_dims(B["M7-17"]["element"])
    rows.append(disc_window(f"LP (25-245, Ø{lp_cat[0]:g} x {lp_cat[1]:g})", lp_cat[0], lp_cat[1], lp_a))
    m = re.search(r"([\d.]+) x ([\d.]+) x ([\d.]+) mm", B["M0-03"]["element"])
    bw = tuple(float(x) for x in m.groups())
    span_a = bw_slot["length"]
    span_b = bw_slot["width"]
    rows.append(rect_window("BW (57.7 x 26.7 x 3)", *bw, span_a, span_b))
    rows.append(rect_window("BW in N-BK7", *bw, span_a, span_b, glass="N-BK7"))
    plus = [disc_window(r["port"], r["d_mm"], r["t_mm"], r["unsupported_r_mm"], p=MI.P_OVER) for r in rows if "d_mm" in r]
    slides = []
    lw_sl = disc_dims(B["M0-02"]["element"])
    lp_sl = disc_dims(B["M7-18"]["element"])
    slides.append(slide_thermal("LW slide", lw_sl[0], lw_sl[1], spec["LW"]["centre"]))
    slides.append(slide_thermal("LP slide", lp_sl[0], lp_sl[1], spec["LP"]["centre"]))
    ok = all(r["pass"] for r in rows if r["glass"] == "fused silica") and all(s["pass_"] for s in slides)
    return dict(windows=rows, at_plus_20mbar=plus, slides=slides, pass_=ok,
                method="Roark: disc simply supported at the bore edge (sigma = 1.25 p a^2/t^2, as fea.py case 7), rectangle simply "
                       "supported on the BW slot (Table 11.4 case 1a, conservative for an obround); SF on the abraded modulus of "
                       "rupture; slides: plate radiation on one face, rim at chamber temperature; thermal-shock parameter "
                       "R = MR(1-nu)/(E alpha)")


# ============================================================================================ 2. seals and clamps
def squeeze_range(t0, t_inst, tol):
    lo_t, hi_t = t_inst - tol / 2, t_inst + tol / 2              # two gaskets share the window's thickness error
    return (t0 - hi_t) / t0, (t0 - t_inst) / t0, (t0 - lo_t) / t0


def check_seals():
    ff = MI.FRAME_FEATURES
    lw_bore = ff["LW"]["bore"]["d"]
    lw_win = disc_dims(bom_rows()["M0-01"]["element"])
    sl = ff["BW"]["slot"]
    A_slot = (sl["length"] - sl["width"]) * sl["width"] + math.pi * (sl["width"] / 2) ** 2
    bw_win = (57.7, 26.7)
    lp_a = MS.VIEWPORTS["LP"]["clear_d"] / 2 + 0.5
    ports = {
        "LW": dict(A_gasket=math.pi / 4 * (lw_win[0] ** 2 - lw_bore ** 2), A_window=math.pi / 4 * lw_win[0] ** 2,
                   screws=int(ff["LW"]["clamp_ring"]["screws"].split(" x ")[0])),
        "BW": dict(A_gasket=bw_win[0] * bw_win[1] - A_slot, A_window=bw_win[0] * bw_win[1],
                   screws=int(ff["BW"]["clamp_frame"]["screws"].split(" x ")[0])),
        "LP": dict(A_gasket=math.pi * (12.7 ** 2 - lp_a ** 2), A_window=math.pi * 12.7 ** 2, screws=4),
    }
    sheets = {"1/32 in. (BOM M0-06)": MI.SHEET_IN_BOM_MM, "1.0 mm (layer camera, lpbf_low.py)": MI.SHEET_LAYER_CAM_MM}
    flat = []
    for sname, t0 in sheets.items():
        lo, nom, hi = squeeze_range(t0, MI.GASKET_INSTALLED_MM, 2 * MI.WINDOW_T_TOL_MM / 2)
        ok = lo >= MI.FKM["squeeze_flat"][0] and hi <= MI.FKM["squeeze_flat"][1] + 0.05
        flat.append(dict(sheet=sname, t0_mm=t0, installed_mm=MI.GASKET_INSTALLED_MM, squeeze_min=lo, squeeze_nom=nom, squeeze_max=hi,
                         glass_bearing_max_MPa=MI.FKM["E_c_MPa"][1] * max(hi, 0.0), pass_=bool(ok)))
    sc = MI.SCREW_M4
    T_rec = 2.0                                              # N m, recommended torque (bottomed clamp: preload only needs to beat the gasket)
    F_screw = T_rec / (sc["K_nut"] * sc["d"] * 1e-3)         # N
    F_proof = sc["preload_frac"] * sc["Sp_A4_70"] * sc["At"]
    strip = 0.75 * math.pi * sc["d"] * 8.0 * 0.58 * MI.MAT["al6061"]["sy"]   # 8 mm of 6061 thread engagement (frame_features: tapped 8 deep)
    clamp = []
    for k, v in ports.items():
        s_max = MI.FKM["E_c_MPa"][1] * flat[1]["squeeze_max"]
        F_g = s_max * v["A_gasket"]
        F_p = MI.P_OVER * v["A_window"]
        F_atm = MI.P_ATM * v["A_window"]
        clamp.append(dict(port=k, A_gasket_mm2=v["A_gasket"], gasket_force_max_N=F_g, plus20mbar_N=F_p, vacuum_on_inner_gasket_N=F_atm,
                          inner_gasket_stress_at_vacuum_MPa=(MI.FKM["E_c_MPa"][0] * flat[1]["squeeze_min"]) + F_atm / v["A_gasket"],
                          screws=v["screws"], preload_each_N=F_screw, separation_margin=v["screws"] * F_screw / (F_g + F_p),
                          screw_stress_frac_of_proof=F_screw / F_proof, thread_strip_N=strip,
                          pass_=v["screws"] * F_screw / (F_g + F_p) >= 2.0 and F_screw <= F_proof))
    # O-ring alternative: a Parker face gland (module_params FACE_1P78) on the seat floor round the bore, inside the window's edge
    oring = []
    for k, (bore, win) in {"LW": (lw_bore, lw_win[0]), "LP": (2 * lp_a, 25.4)}.items():
        land = 1.0
        gid = bore + 2 * land
        pick = MP.pick_ring(math.pi * gid)
        if pick:
            dash, ID, st = pick
            od_groove = gid + 2 * MP.FACE_1P78["width"]
            fits = od_groove + 2 * land <= win
            cs = MP.FACE_1P78["cs"]
            sq = [(cs - 0.08 - (MP.FACE_1P78["depth"] + 0.03)) / (cs - 0.08), (cs - MP.FACE_1P78["depth"]) / cs,
                  (cs + 0.08 - (MP.FACE_1P78["depth"] - 0.03)) / (cs + 0.08)]
            oring.append(dict(port=k, ring=dash, ring_id_mm=ID, stretch=st, groove_id_mm=gid, groove_od_mm=od_groove,
                              window_d_mm=win, fits_under_window=fits, squeeze=sq))
        else:
            oring.append(dict(port=k, ring=None, fits_under_window=False, groove_id_mm=gid, window_d_mm=win))
    ok = flat[1]["pass_"] and all(c["pass_"] for c in clamp)
    return dict(flat_gasket=flat, clamps=clamp, oring_alternative=oring, torque_Nm=T_rec, pass_=ok,
                fkm_src=MI.FKM["src"], screw_src=sc["src"],
                method="clamp ring bottoms on the wall (frame_features): gasket squeeze set by the sheet, the 0.75 mm the seat allows, "
                       "and the window's thickness tolerance shared by the two gaskets; gasket force = E_c x squeeze x area; "
                       "screws: preload from torque (K 0.2) vs gasket force + 20 mbar with margin 2; Parker face gland as "
                       "module_params.FACE_1P78 for the O-ring option")


# ============================================================================================ 3. side camera bracket
def check_side_camera():
    c = MS.VIEWPORTS["LW"]["centre"]
    ax = np.array(MS.axis_to_target(c))                    # into the chamber
    cam = MI.ASSUMED["Chronos 2.1-HD"]
    lens = MI.ASSUMED["Kowa LM50JC10M"]
    body = cam["dims"]
    stand = MS.SIDE_CAMERA["standoff_mm"]
    s_cm = stand + lens["L"] + body[0] / 2                  # CoM from the window's outer face, along the line
    p_cm = np.array(c) - ax * s_cm
    L = abs(p_cm[0] - c[0])                                  # bracket reach from the wall face (x) to the CoM
    m = cam["kg"] + lens["kg"]
    Lb = (body[0] + lens["L"]) * 1e-3
    J = m * (Lb ** 2 + (body[2] * 1e-3) ** 2) / 12
    wd = math.dist(c, MS.TARGET) + stand
    lensd = OPT.LENSES["Kowa LM50JC10M 50 mm"]
    px_obj = OPT.CAMS["Chronos 2.1-HD mono"]["px_um"] * (wd - lensd["f_mm"]) / lensd["f_mm"]
    E = MI.AL6061["E"] * 1e6
    rho = MI.AL6061["rho"]
    b = 0.080
    f_exc = 60.0                                            # Hz: blower rotation at 60 Hz mains (2-pole), recoater 10 Hz (600 rpm)
    v_base = 1.0e-3                                         # m/s RMS frame vibration near a running blower (assumed; ISO 10816 class I 'satisfactory' 0.71-1.8)
    x_base = v_base * math.sqrt(2) / (2 * math.pi * f_exc)
    rows = []
    Lm = L * 1e-3
    for t_in in (0.25, 0.375, 0.5, 0.625, 0.75, 1.0):
        t = t_in * 25.4e-3
        I = b * t ** 3 / 12
        K = E * I / Lm ** 3 * np.array([[12, -6 * Lm], [-6 * Lm, 4 * Lm ** 2]])
        mb = rho * b * t * Lm
        Mc = mb * Lm / 420 * np.array([[156, -22 * Lm], [-22 * Lm, 4 * Lm ** 2]]) / Lm + np.diag([m, J])
        ev, vec = np.linalg.eig(np.linalg.solve(Mc, K))
        order = np.argsort(np.real(ev))
        w2 = np.real(ev[order])
        phi = np.real(vec[:, order[0]])
        f1, f2 = math.sqrt(w2[0]) / 2 / math.pi, math.sqrt(w2[1]) / 2 / math.pi
        gain = abs(1 + phi[1] / phi[0] * wd * 1e-3)              # image motion per unit of tip translation in mode 1
        F = np.array([(m + mb / 2) * G, 0.0])
        v, th = np.linalg.solve(K, F)
        r = f_exc / f1
        rel = x_base * r ** 2 / abs(1 - r ** 2)
        static_img = abs(v) + abs(th) * wd * 1e-3
        dyn = rel * 1e6 * gain
        rows.append(dict(t_in=t_in, t_mm=t * 1e3, f1_hz=f1, f2_hz=f2, sag_um=v * 1e6, tilt_urad=th * 1e6,
                         static_image_shift_um=static_img * 1e6, dyn_image_um_at_60Hz=dyn,
                         pass_=bool(f1 >= 2.5 * f_exc and dyn < 0.5 * px_obj)))
    pick = next((r for r in rows if r["pass_"]), None)
    return dict(reach_mm=L, camera_kg=m, J_kgm2=J, wd_mm=wd, px_across_um=px_obj, um_per_urad=wd * 1e-3,
                excitation=dict(f_hz=f_exc, base_um=x_base * 1e6, note="side-channel blower (bom.csv G4, model not chosen): a 2-pole motor "
                                "turns at 48-58 Hz on mains; recoater <= 600 rpm (10 Hz, electrical.md); base vibration 1 mm/s RMS assumed"),
                bracket_width_mm=b * 1e3, rows=rows, pick=pick, pass_=pick is not None,
                method="cantilever plate from the chamber's left wall to the camera's centre of mass, camera as a rigid body (mass and "
                       "pitch inertia) at the tip: 2-DOF eigenvalues with the plate's consistent mass; image shift = translation + "
                       "tilt x working distance (mode 1's shape for the vibration); criterion f1 >= 2.5 x 60 Hz and vibration "
                       "< 0.5 px; the static sag is aimed out when the camera is set up")


# ============================================================================================ 4. coaxial cage
def check_cage():
    co = MS.COAX
    A = MI.ASSUMED
    by, bz = co["beam_y"], co["beam_z"]
    x1, x2, x3 = co["cube1"]["x"], co["cube2"]["x"], co["cube3"]["x"]
    half = 41.3 / 2
    rod = A["ER rod per 100 mm"]["kg"] / 100
    yb = co["camera_branch"]["y_end"]
    Lbr = abs(yb - by) - half
    items = [
        ("cube 2 (DMSP950)", A["C4W cube + B4C base + FFM1"]["kg"], (x2, by, bz)),
        ("cube 3 (DMLP805)", A["C4W cube + B4C base + FFM1"]["kg"], (x3, by, bz)),
        ("rods cube 1-2 (4)", 4 * rod * (x1 - x2), ((x1 + x2) / 2, by, bz)),
        ("rods cube 2-3 (4)", 4 * rod * (x2 - x3), ((x2 + x3) / 2, by, bz)),
        ("camera branch rods (4)", 4 * rod * Lbr, (x2, by - half - Lbr / 2, bz)),
        ("camera branch plates (2 x CP33)", 2 * A["CP33 plate"]["kg"], (x2, by - half - Lbr / 2, bz)),
        ("tube lens AC254-075 in SM1L10", A["SM1L10 + optic"]["kg"], (x2, by - half - 0.5 * Lbr, bz)),
        ("IMX296 camera", A["IMX296 board + housing"]["kg"], (x2, yb, bz)),
        ("PD-A arm (lens, pinhole, filter tubes)", 2 * A["SM1L10 + optic"]["kg"], (x3 - half - 30, by, bz)),
        ("PD-A (PDA36A2, moved from cube 1)", A["PDA36A2"]["kg"], (x3 - half - 70, by, bz)),
        ("PD-B arm (lens, pinhole, filter tubes)", 2 * A["SM1L10 + optic"]["kg"], (x3, by - half - 30, bz)),
        ("PD-B (PDA36A2)", A["PDA36A2"]["kg"], (x3, by - half - 70, bz)),
        ("posts and clamps (5)", 5 * A["galvo-side stand-off post"]["kg"], ((x2 + x3) / 2, by - 30, (bz + P["z_bridge1"]) / 2)),
    ]
    mtot = sum(i[1] for i in items)
    cm = np.sum([np.array(i[2]) * i[1] for i in items], axis=0) / mtot
    arm_from_cube1 = abs(cm[0] - x1)
    moment = mtot * G * arm_from_cube1 * 1e-3
    # camera branch as a cantilever off cube 2 (4 x Ø6 303 rods on a 30 mm square), tip load = camera + half the rods
    d = 6.0
    E = MI.STEEL_303["E"]
    I_lo = 4 * math.pi * d ** 4 / 64
    I_hi = I_lo + 4 * (math.pi * d ** 2 / 4) * 15.0 ** 2
    W = (A["IMX296 board + housing"]["kg"] + A["SM1L10 + optic"]["kg"] + 2 * A["CP33 plate"]["kg"]) * G + 4 * rod * Lbr * G / 2
    sag = {k: W * Lbr ** 3 / (3 * E * I) * 1000 for k, I in (("rods alone", I_lo), ("rods acting together", I_hi))}
    mag = MI.TUBE_LENS_F_MM / MI.F_THETA_MM                   # tube lens (optics-parts.csv MO12) over the f-theta's focal length
    px_plate = OPT.CAMS["IMX296 mono"]["px_um"] / mag
    point = {k: v / mag for k, v in sag.items()}
    f_branch = {k: math.sqrt(3 * E * I / Lbr ** 3 * 1e3 / (W / G)) / 2 / math.pi for k, I in (("rods alone", I_lo), ("rods acting together", I_hi))}
    post_h = bz - P["z_bridge1"]
    drift_post = post_h * MI.AL6061["alpha"] * 1000 / mag    # um at the plate per K of post-to-post difference
    drift_axis = (MI.AL6061["alpha"] - MI.STEEL_303["alpha"]) * (x1 - x3) * 1000   # um per K, rods vs bridge along the beam
    f_theta = 160.0
    # the bridge's sway mode with the cage added (fea.json case 6b): f ~ 1/sqrt(m), m = bridge plate + optics + post tops
    v6 = next(v for v in MI.FEA["6"]["variants"] if v["variant"].startswith("as built"))
    plate_vol = (605 * 370 * 25 - math.pi * 63 ** 2 * 25 - 56 * 251 * 25 - math.pi * 40 ** 2 * 25) * 1e-9
    m_modal = plate_vol * MI.AL6061["rho"] + v6["optics_kg"]
    f_with = v6["modes"][0]["f_hz"] * math.sqrt(m_modal / (m_modal + mtot))
    return dict(items=[dict(item=i[0], kg=i[1], xyz=i[2]) for i in items], mass_kg=mtot, cm_xyz=cm.tolist(),
                arm_from_cube1_mm=arm_from_cube1, moment_about_cube1_Nm=moment, branch_len_mm=Lbr,
                branch_sag_um=sag, branch_pointing_um_at_plate=point, branch_f1_hz=f_branch, px_at_plate_um=px_plate, magnification=mag,
                post_height_mm=post_h, drift_um_per_K_post_difference=drift_post, axial_mismatch_um_per_K=drift_axis,
                boresight_um_per_urad_cube1_tilt=2 * f_theta * 1e-3, bridge_f1_hz=v6["modes"][0]["f_hz"], bridge_f1_with_cage_hz=f_with,
                masses_src="mech_inputs.ASSUMED: estimated from the parts' sizes, not weighed",
                pass_=bool(sag["rods acting together"] / mag < px_plate and f_with > 100.0),
                method="masses at their places on the spec's beam line; camera branch a cantilever of 4 ER rods (bounds: rods alone, "
                       "rods acting together through the plates); sensor shift / magnification = shift at the plate; bridge sway "
                       "mode scaled by 1/sqrt(mass)")


# ============================================================================================ 5. bridge cut-out (reads bridge_modal.json)
def check_bridge():
    jf = OUT / "bridge_modal.json"
    v6 = next(v for v in MI.FEA["6"]["variants"] if v["variant"].startswith("as built"))
    out = dict(fea_case6b_f_hz=[m["f_hz"] for m in v6["modes"]])
    cands = {}
    for tag, c in {"spec": MS.VIEWPORTS["LP"]["centre"]}.items():
        cands[tag] = MI.lp_camera_envelope(c)
    out["envelope"] = cands
    if not jf.exists():
        out.update(pass_=None, note="bridge_modal.json not found: run bridge_modal.py (CalculiX)")
        return out
    R = json.loads(jf.read_text())
    out["modal"] = R
    base = R["variants"].get("base")
    res = []
    for tag, cd in R["candidates"].items():
        row = dict(candidate=tag, centre=cd["centre"], in_bridge_level_cm3=cd["vol_in_bridge_level_cm3"],
                   in_reservoir_slot_cm3=cd["vol_in_reservoir_slot_cm3"], in_plate_cm3=cd["vol_in_plate_cm3"], cut_bbox_xy=cd["cut_bbox_xy"])
        v = R["variants"].get(tag)
        if v and base:
            row.update(f_hz=v["f_hz"], f_base_hz=base["f_hz"], df1_pct=100 * (v["f_hz"][0] / base["f_hz"][0] - 1),
                       df_pct=[100 * (a / b - 1) for a, b in zip(v["f_hz"], base["f_hz"])], removed_cm3=v["removed_cm3"])
        res.append(row)
    out["rows"] = res
    sj = OUT / "bridge_sweep.json"
    if sj.exists():
        out["sweep"] = json.loads(sj.read_text())["rows"]
    ok = all((r.get("f_hz") or [999])[0] >= 100.0 for r in res)
    out["pass_"] = ok
    return out


# ============================================================================================ 6. acoustic-emission path
def fin_profile(segments, T_tip, d_mm, k=MI.SS316["k"], n=1400, T_air=35.0, h_air=16.0, L_out=0.0):
    """Steady 1-D fin: k A T'' = h P (T - T_s(z)). segments: [(length_mm, T_surround_start, T_surround_end, h)]; then L_out mm
    in air. T(0) = T_tip (the plate's underside); the far end is adiabatic (the sensor's own exchange is small)."""
    segs = list(segments) + ([(L_out, T_air, T_air, h_air)] if L_out > 0 else [])
    Ltot = sum(s[0] for s in segs) * 1e-3
    z = np.linspace(0, Ltot, n)
    dz = z[1] - z[0]
    Ts = np.zeros(n)
    hh = np.zeros(n)
    z0 = 0.0
    for L, a, b, h in segs:
        z1 = z0 + L * 1e-3
        m = (z >= z0 - 1e-12) & (z <= z1 + 1e-12)
        Ts[m] = a + (b - a) * (z[m] - z0) / max(z1 - z0, 1e-12)
        hh[m] = h
        z0 = z1
    d = d_mm * 1e-3
    A = math.pi * d ** 2 / 4
    Pm = math.pi * d
    Amat = np.zeros((n, n))
    rhs = np.zeros(n)
    Amat[0, 0] = 1.0
    rhs[0] = T_tip
    for i in range(1, n - 1):
        Amat[i, i - 1] = Amat[i, i + 1] = k * A / dz ** 2
        Amat[i, i] = -2 * k * A / dz ** 2 - hh[i] * Pm
        rhs[i] = -hh[i] * Pm * Ts[i]
    Amat[-1, -1] = 1.0
    Amat[-1, -2] = -1.0
    T = np.linalg.solve(Amat, rhs)
    return z * 1e3, T, Ts


def h_annulus(r_in_mm, r_out_mm, T_C, eps=0.3, gas_k=MI.ARGON_K):
    r1, r2 = r_in_mm * 1e-3, r_out_mm * 1e-3
    hg = gas_k / (r1 * math.log(r2 / r1))
    Tk = T_C + 273.15
    hr = 4 * eps * SIGMA * Tk ** 3 / (1 + (r1 / r2) * (1 / eps - 1)) * 1.0
    return hg + hr


def check_ae():
    ae = MI.AE
    temps = MI.module_temps()
    d = ae["waveguide_d_mm"]
    rod_id = MP.ROD_ID
    cases = {k: v for k, v in temps.items() if k.startswith("M50") and k.split("_")[1] in ("start", "end")
             and ("_e0.5" in k or "powder" in k or "tierB" in k) and "scr" not in k and "_h2" not in k and "mesh" not in k
             and "clear" not in k}
    prof = {}
    need = []
    for name, t in cases.items():
        segs = [(MP.BLOCK_T, t["T_block"], t["T_block"], h_annulus(d / 2, d / 2 + 0.5, t["T_block"], gas_k=0.024)),
                (MP.BREAK_T, t["T_block"], t["T_head"], h_annulus(d / 2, 4.0, (t["T_block"] + t["T_head"]) / 2, gas_k=0.022)),
                (MP.HEAD_T, t["T_head"], t["T_head"], h_annulus(d / 2, d / 2 + 0.5, t["T_head"], gas_k=0.02)),
                (MP.ROD_L, t["T_rod_gland"], t["T_rod_end"], h_annulus(d / 2, rod_id / 2, (t["T_rod_gland"] + t["T_rod_end"]) / 2)),
                (MP.ROD_END_T, t["T_rod_end"], t["T_rod_end"], h_annulus(d / 2, d / 2 + 0.5, t["T_rod_end"], gas_k=0.02))]
        row = dict(case=name, T_plate=t["T_plate"], T_rod_end=t["T_rod_end"], T_ch=t["T_ch"])
        for L_out in (0.0, 25.0, 50.0, 100.0):
            z, T, Ts = fin_profile(segs, t["T_plate"], d, L_out=L_out, T_air=VLM_AIR[0])
            row[f"T_sensor_out{int(L_out)}"] = float(T[-1])
            if L_out in (0.0, 50.0):
                prof[f"{name}|{int(L_out)}"] = dict(z=z[::20].tolist(), T=T[::20].tolist(), Ts=Ts[::20].tolist())
        for key, t_air in (("L_out_for_60C_mm", VLM_AIR[0]), ("L_out_for_60C_busy_mm", VLM_AIR[1])):
            lo, hi = 0.0, 300.0
            for _ in range(30):
                mid = (lo + hi) / 2
                z, T, Ts = fin_profile(segs, t["T_plate"], d, L_out=mid, T_air=t_air)
                lo, hi = (lo, mid) if T[-1] <= ae["sensor_t_max_C"] else (mid, hi)
            row[key] = hi if hi < 299 else None
        row["inside_length_mm"] = sum(s[0] for s in segs)
        need.append(row)
    # Hertz contact, waveguide tip on the plate's underside (316 on 6061)
    s316, al = MI.SS316, MI.MAT["al6061"]
    Es = 1 / ((1 - s316["nu"] ** 2) / s316["E"] + (1 - al["nu"] ** 2) / al["E"])
    hertz = []
    for R in (1.5, 10.0, 25.0, 50.0):
        for F in ae["preload_N"]:
            a = (3 * F * R / (4 * Es)) ** (1 / 3)
            p0 = 3 * F / (2 * math.pi * a ** 2)
            hertz.append(dict(R_mm=R, F_N=F, contact_d_um=2 * a * 1000, p0_MPa=p0, yields_6061=p0 > 1.6 * al["sy"],
                              k_contact_N_per_m=2 * a * 1e-3 * Es * 1e6))
    # acoustics: bar velocity, wavelength, Rayleigh-Love dispersion, and a contact-spring transmission estimate
    c0 = math.sqrt(s316["E"] * 1e6 / s316["rho"])
    Zm = s316["rho"] * c0 * math.pi * (d * 1e-3) ** 2 / 4
    acoustics = []
    for f in (100e3, 300e3, 500e3):
        lam = c0 / f * 1e3
        row = dict(f_kHz=f / 1e3, wavelength_mm=lam, d_over_lambda=d / lam,
                   phase_velocity_drop_pct=100 * s316["nu"] ** 2 * math.pi ** 2 * (d / 2 / lam) ** 2,
                   phase_velocity_drop_drawbar8_pct=100 * s316["nu"] ** 2 * math.pi ** 2 * (4.0 / lam) ** 2)
        for R in (1.5, 50.0):
            kc = next(h["k_contact_N_per_m"] for h in hertz if h["R_mm"] == R and h["F_N"] == ae["preload_N"][1])
            x = 2 * math.pi * f * Zm / (2 * kc)
            row[f"dry_tip_R{R:g}_dB"] = -10 * math.log10(1 + x ** 2)
        k_grease = 1.5e9 / 10e-6 * math.pi * (d * 1e-3) ** 2 / 4           # 10 um of grease (bulk modulus ~1.5 GPa) on the flat tip
        x = 2 * math.pi * f * Zm / (2 * k_grease)
        row["greased_flat_tip_dB"] = -10 * math.log10(1 + x ** 2)
        acoustics.append(row)
    Z = ae["Z_MRayl"]

    def tl(z1, z2):
        return -10 * math.log10(4 * z1 * z2 / (z1 + z2) ** 2)
    att = [a * (sum(s for s in (MP.BLOCK_T, MP.BREAK_T, MP.HEAD_T, MP.ROD_L, MP.ROD_END_T)) + 50) * 1e-3 for a in ae["attenuation_316_dB_per_m"]]
    m50 = MP.MODULES["M50"]
    area_frac = MP.MODULES["M50"]["n_standoffs"] * math.pi * (MP.MACOR["d"] / 2) ** 2 / (math.pi * (m50["block_d"] / 2) ** 2)
    wg = dict(tip_greased=(abs(acoustics[-1]["greased_flat_tip_dB"]), 3.0), Al_to_316=(tl(Z["6061"], Z["316"]),) * 2,
              attenuation=tuple(att), end_cap_seal=(0.5, 2.0), sensor_shoe_greased=ae["interface_dB"]["greased"])
    rod = dict(graphite_foil_x2=tuple(2 * x for x in ae["interface_dB"]["graphite_foil"]),
               macor_impedance_x2=(2 * tl(Z["6061"], Z["Macor"]),) * 2,
               macor_dry_contacts_x2=tuple(2 * x for x in ae["interface_dB"]["dry_metal"]),
               standoff_area=(-10 * math.log10(area_frac),) * 2, head_rod_endcap=(2.0, 6.0),
               sensor_greased=ae["interface_dB"]["greased"])
    tot_wg = (sum(v[0] for v in wg.values()), sum(v[1] for v in wg.values()))
    tot_rod = (sum(v[0] for v in rod.values()), sum(v[1] for v in rod.values()))
    rod_end_max = max(v["T_rod_end"] for k, v in temps.items() if "powder" not in k)
    rod_end_powder = max(v["T_rod_end"] for k, v in temps.items() if "powder" in k)
    ok_temp = all(r["L_out_for_60C_mm"] is not None for r in need)
    ok = ok_temp and rod_end_max <= ae["rod_end_t_max_C"]
    return dict(waveguide_d_mm=d, bar_velocity_m_s=c0, mech_impedance_Ns_m=Zm, thermal=need, profiles=prof, hertz=hertz,
                acoustics=acoustics, budget_waveguide_dB=wg, budget_rod_end_dB=rod, total_waveguide_dB=tot_wg, total_rod_end_dB=tot_rod,
                standoff_area_fraction=area_frac, rod_end_max_C=rod_end_max, rod_end_powder_gaps_C=rod_end_powder,
                pass_=ok, src=[ae["attenuation_src"], ae["interface_src"], ae["Z_src"]],
                method="fin equation through the module's stack with the surroundings' temperatures from thermal.json (argon gaps by "
                       "conduction + radiation), then in air; Hertz sphere-on-flat; bar velocity and Rayleigh-Love dispersion; the tip "
                       "as a contact spring k = 2aE* against the rod's impedance rho c A; interface budgets from impedances and Edison")


# ============================================================================================ 7. temperatures at the ports
def slide_with_purge(windows, flows_lpm=(1.0, 3.0), T_gas=(25.0, 60.0), T_purge=(22.0, 30.0)):
    """The LW slide's temperature with the argon purge blowing across its chamber face. plume.md §4.3: a slide 10 K colder than
    the gas next to it collects 20-120x more condensate. Purge: laminar flat plate over the slide (Nu = 0.664 Re^0.5 Pr^(1/3)) at the
    Ø4 passage's exit velocity; the far face sees the outer window across the bore (argon conduction + glass-to-glass radiation)."""
    s = next(x for x in windows["slides"] if x["port"].startswith("LW"))
    D = s["d_mm"] * 1e-3
    d_pass = 4.0e-3                                          # frame_features LW purge: "Ø4 passage through"
    nu, k, pr, rho, cp = 1.40e-5, MI.ARGON_K, 0.67, 1.623, 520.0   # argon at 300 K, 1 atm
    gap = (abs(MS.VIEWPORTS["LW"]["centre"][0]) - 140.0) * 1e-3      # outer face to the inner face of the 16 mm wall
    q = s["worst"]["q_W_m2"]
    rows = []
    for Q in flows_lpm:
        u = Q / 60e3 / (math.pi * d_pass ** 2 / 4)
        Re = u * D / nu
        h_p = 0.664 * Re ** 0.5 * pr ** (1 / 3) * k / D
        for tg in T_gas:
            h_c = k / gap + 4 * 0.75 * SIGMA * (tg + 273.15) ** 3
            for tp in T_purge:
                Ts = (h_p * tp + h_c * tg + q) / (h_p + h_c)
                heater_W = rho * Q / 60e3 * cp * max(tg - tp, 0.0)
                rows.append(dict(purge_lpm=Q, u_m_s=u, h_purge=h_p, h_back=h_c, T_gas=tg, T_purge=tp, T_slide=Ts,
                                 colder_than_gas_K=tg - Ts, heater_to_match_W=heater_W))
    off = [dict(T_gas=tg, T_slide=tg + q / (4 * 0.75 * SIGMA * (tg + 273.15) ** 3 + k / gap + 5.0)) for tg in T_gas]
    return dict(rows=rows, purge_off=off, worst_colder_K=max(r["colder_than_gas_K"] for r in rows),
                heater_max_W=max(r["heater_to_match_W"] for r in rows))


def check_port_thermal(windows):
    vlm = dict(typical=VLM_AIR[0], busy=(38.0, VLM_AIR[1]), src="heat.md §2: Shuttle air ~30 C in a typical build with Shuttle 1 idling, "
                                                                "38-43 C in PR 318's busy case (22 C room)")
    walls = (25.0, 60.0)                                    # thermal.json T_ch: the chamber at 25 C and the hot case at 60 C
    cam_face = (MS.SIDE_CAMERA["body_mm"][1] * MS.SIDE_CAMERA["body_mm"][2]) * 1e-6
    q_wall = [0.9 * SIGMA * ((w + 273.15) ** 4 - (vlm["busy"][1] + 273.15) ** 4) * 0.3 * cam_face for w in walls]
    slide_worst = max(s["worst"]["dT_centre_rim_K"] for s in windows["slides"])
    rows = [dict(item="outer windows (LW, BW, LP)", T_C=f"{walls[0]:.0f}-{walls[1]:.0f}", basis="at the wall or lid temperature (thermal.json T_ch cases)",
                 limit="FKM gasket 200 C", ok=True),
            dict(item="inside cover slides", T_C=f"{walls[0]:.0f}-{walls[1] + slide_worst:.1f}",
                 basis=f"chamber gas/wall + {slide_worst:.2f} K from the plate's radiation (check 1)", limit="fused silica: none", ok=True),
            dict(item="Chronos body and lens (outside the LW port)", T_C=f"{vlm['typical']:.0f} (typical) / {vlm['busy'][0]:.0f}-{vlm['busy'][1]:.0f} (busy VLM)",
                 basis=f"air in the guard = Shuttle air; the 60 C wall adds {max(q_wall):.2f} W of radiation to its front face",
                 limit="Kron's operating range not found in the repo (machine-vision cameras: typically 0-40 or 0-45 C)", ok=None),
            dict(item="IMX296 lid camera and coaxial cage", T_C=f"{vlm['typical']:.0f}-{vlm['busy'][1]:.0f}",
                 basis="above the lid/bridge, in the guard's air", limit="InnoMaker board: check (Pi GS camera 0-50 C)", ok=None)]
    purge = slide_with_purge(windows)
    return dict(rows=rows, vlm=vlm, radiation_from_wall_W=q_wall, purge=purge, pass_=None,
                flag="the busy-VLM air (38-43 C) is at or above a 40 C camera limit; the cameras need the same answer as the laser "
                     "(heat.md §2: chilled water or a ducted exhaust)")


def fmt(x, nd=1):
    if x is None:
        return "-"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, (int, float)):
        if abs(x) >= 1e4:
            return f"{x:,.0f}"
        return f"{x:.{nd}f}"
    return str(x)


def write_md(R):
    L = []
    w = R["1"]
    L.append("### 1. Windows and cover slides\n")
    L.append("| Window | Glass | Size (mm) | Unsupported span (mm) | Stress at 1 atm (MPa) | SF (MR 52.4) | Thickness for SF 4 (mm) | Centre deflection (µm) |")
    L.append("|---|---|---|---|---:|---:|---:|---:|")
    for r in w["windows"]:
        size = f"Ø{r['d_mm']:g} × {r['t_mm']:g}" if "d_mm" in r else " × ".join(f"{x:g}" for x in r["size_mm"])
        span = f"r {r['unsupported_r_mm']:.1f}" if "d_mm" in r else f"{r['spans_mm'][0]:.1f} × {r['spans_mm'][1]:.1f}"
        sf = fmt(r["SF"]) if r["SF"] else f"needs MR ≥ {r['MR_needed_for_SF4_MPa']:.1f}"
        L.append(f"| {r['port']} | {r['glass']} | {size} | {span} | {r['sigma_MPa']:.2f} | {sf} | {fmt(r['t_needed_SF4_mm'], 2)} | {r['deflection_um']:.2f} |")
    L.append("")
    for s in w["slides"]:
        L.append(f"- **{s['port']}** (Ø{s['d_mm']:g} × {s['t_mm']:g}): the hot plate puts at most {s['worst']['q_W_m2']:.1f} W/m² on it "
                 f"({s['worst']['plate']}, view factor {s['worst']['view_factor']:.4f}), a {s['worst']['dT_centre_rim_K']:.3f} K rise and "
                 f"{s['worst']['sigma_MPa']:.4f} MPa. A molten-Al droplet is a {s['spatter_quench_K']:.0f} K quench against fused silica's "
                 f"thermal-shock parameter of {s['R_thermal_shock_K']:.0f} K.")
    fmin = min(r['window_focal_m'] for r in w['windows'] if 'window_focal_m' in r) / 1000
    L.append(f"- At +20 mbar every window carries 1/50 of these stresses. Bent at vacuum, each window is a weak meniscus lens with a "
             f"focal length of {fmin:,.0f} km or more: no optical effect.")
    L.append("")
    s = R["2"]
    L.append("### 2. Seals and clamps\n")
    L.append("The seats as programmed ([`fabrication.md`](fabrication.md), `frame_features.py`) bottom the clamp on the wall, with 0.75 mm "
             "left for each flat FKM gasket (under the window and over it). The squeeze then depends on the sheet and on the window's "
             "thickness tolerance, which the two gaskets share:\n")
    L.append("| FKM sheet | Squeeze: thinnest / nominal / thickest window | Within 15-35 %? | Most the glass bears (MPa) |")
    L.append("|---|---|---|---:|")
    for f in s["flat_gasket"]:
        L.append(f"| {f['sheet']}: {f['t0_mm']:.2f} mm | {100 * f['squeeze_min']:.0f} / {100 * f['squeeze_nom']:.0f} / {100 * f['squeeze_max']:.0f} % | "
                 f"{fmt(f['pass_'])} | {f['glass_bearing_max_MPa']:.1f} |")
    L.append("\nThe glass touches only FKM, on both faces at the same radii, so the clamp puts no bending into it. "
             f"Window thickness tolerance taken as ±{MI.WINDOW_T_TOL_MM:g} mm.\n")
    L.append("| Port | Gasket area (mm²) | Gasket force, max (N) | +20 mbar (N) | Screws | Preload each at "
             f"{s['torque_Nm']:.1f} N·m (N) | Margin against lift-off | Thread strip in 6061 (N) |")
    L.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for c in s["clamps"]:
        L.append(f"| {c['port']} | {c['A_gasket_mm2']:.0f} | {c['gasket_force_max_N']:.0f} | {c['plus20mbar_N']:.1f} | {c['screws']} × M4 | "
                 f"{c['preload_each_N']:.0f} | {c['separation_margin']:.1f} | {c['thread_strip_N']:,.0f} |")
    L.append("")
    for o in s["oring_alternative"]:
        if o.get("ring"):
            L.append(f"- **O-ring option, {o['port']}:** AS568 {o['ring']} (ID {o['ring_id_mm']:.2f}, {100 * o['stretch']:.1f} % stretch) in a "
                     f"Parker face gland (module_params FACE_1P78) from Ø{o['groove_id_mm']:.1f} to Ø{o['groove_od_mm']:.1f}, squeeze "
                     f"{100 * o['squeeze'][0]:.0f}-{100 * o['squeeze'][2]:.0f} %; "
                     + ("fits under the window." if o["fits_under_window"] else f"**does not fit** under the Ø{o['window_d_mm']:g} window."))
        else:
            L.append(f"- **O-ring option, {o['port']}:** no AS568 1.78 mm ring fits a groove from Ø{o['groove_id_mm']:.1f} under a "
                     f"Ø{o['window_d_mm']:g} window: keep the flat gasket (the layer camera's reason too).")
    L.append("")
    c = R["3"]
    L.append("### 3. Side camera bracket (Chronos at LW)\n")
    L.append(f"The camera and lens ({c['camera_kg']:.2f} kg, pitch inertia {c['J_kgm2'] * 1e4:.0f} kg·cm²) sit {c['reach_mm']:.0f} mm out "
             f"from the left wall, on the sight line. One pixel is {c['px_across_um']:.1f} µm across at the plate; a camera tilt of 1 µrad "
             f"moves the view {c['um_per_urad']:.3f} µm. Excitation: {c['excitation']['note']}.\n")
    L.append(f"| 6061 plate, {c['bracket_width_mm']:.0f} mm wide | f1 (Hz) | f2 (Hz) | Static sag (µm) | Tilt (µrad) | Static image shift (µm) | Image motion at 60 Hz (µm) | OK |")
    L.append("|---|---:|---:|---:|---:|---:|---:|---|")
    for r in c["rows"]:
        L.append(f"| {r['t_in']:g} in. ({r['t_mm']:.1f} mm) | {r['f1_hz']:.0f} | {r['f2_hz']:.0f} | {abs(r['sag_um']):.1f} | {abs(r['tilt_urad']):.0f} | "
                 f"{r['static_image_shift_um']:.1f} | {r['dyn_image_um_at_60Hz']:.3f} | {fmt(r['pass_'])} |")
    L.append("")
    g = R["4"]
    L.append("### 4. Coaxial cage on the bridge\n")
    L.append(f"- **Added mass:** {g['mass_kg']:.2f} kg (estimated from the parts' sizes), centre of mass at "
             f"({g['cm_xyz'][0]:.0f}, {g['cm_xyz'][1]:.0f}, {g['cm_xyz'][2]:.0f}), {g['arm_from_cube1_mm']:.0f} mm from cube 1: "
             f"{g['moment_about_cube1_Nm']:.2f} N·m if it hung from cube 1's post alone. Put a post under each cube and under each branch's end.")
    L.append(f"- **Camera branch** ({g['branch_len_mm']:.0f} mm of rods off cube 2, unsupported): tip sag "
             f"{g['branch_sag_um']['rods acting together']:.2f}-{g['branch_sag_um']['rods alone']:.1f} µm, "
             f"{g['branch_pointing_um_at_plate']['rods acting together']:.2f}-{g['branch_pointing_um_at_plate']['rods alone']:.1f} µm at the plate "
             f"against a {g['px_at_plate_um']:.1f} µm pixel there; its first mode {g['branch_f1_hz']['rods alone']:.0f}-"
             f"{g['branch_f1_hz']['rods acting together']:.0f} Hz. The sag is static and calibrates out, but the low end of that mode "
             "sits near the bridge's own 128 Hz: a post at the branch's end removes both.")
    L.append("- The added mass counts PD-A, which moves from cube 1's chain (already in fea.py case 6's 0.5 kg tap mass), so it is an "
             "upper bound.")
    L.append(f"- **Thermal drift:** {g['drift_um_per_K_post_difference']:.2f} µm at the plate per K of difference between two "
             f"{g['post_height_mm']:.0f} mm aluminium posts ({g['drift_um_per_K_post_difference'] / g['px_at_plate_um']:.2f} px/K); "
             f"{g['axial_mismatch_um_per_K']:.1f} µm/K of steel rod against aluminium bridge along the beam (it loads the cube clamps, "
             f"not the view); tilting cube 1 by 1 µrad moves the laser {g['boresight_um_per_urad_cube1_tilt']:.2f} µm against the coaxial view.")
    L.append(f"- **Bridge sway mode with the cage:** {g['bridge_f1_hz']:.1f} → {g['bridge_f1_with_cage_hz']:.1f} Hz (mass scaling), above the 100 Hz criterion.")
    L.append("")
    b = R["5"]
    L.append("### 5. The steep lid camera and the optics bridge\n")
    if b.get("rows"):
        L.append("| LP candidate | Camera envelope at the bridge's level (cm³) | of which in the reservoir slot (cm³) | in the plate (cm³) | f1-f6 with the cut (Hz) | Change in f1 |")
        L.append("|---|---:|---:|---:|---|---:|")
        for r in b["rows"]:
            fs = ", ".join(f"{x:.0f}" for x in r["f_hz"]) if r.get("f_hz") else "no cut needed"
            L.append(f"| {r['candidate']} {tuple(round(x) for x in r['centre'])} | {r['in_bridge_level_cm3']:.1f} | {r['in_reservoir_slot_cm3']:.1f} | "
                     f"{r['in_plate_cm3']:.1f} | {fs} | {fmt(r.get('df1_pct'), 1)} % |")
        base = b["modal"]["variants"].get("base")
        if base:
            L.append(f"\nUncut bridge on the same mesh ({b['modal']['mesh']}): {', '.join(f'{x:.0f}' for x in base['f_hz'])} Hz "
                     f"(fea.py case 6b at hmax 10: {', '.join(f'{x:.0f}' for x in b['fea_case6b_f_hz'])} Hz). Gravity sag at the lens: "
                     + ", ".join(f"{k} {v['gravity']['lens_bore_sag_um']:.1f} µm" for k, v in b["modal"]["variants"].items()) + ".")
            if b.get("sweep"):
                L.append("\nWith the lens front moved along the line (the boss's height isn't fixed yet), the camera envelope "
                         "at the bridge's level, in cm³ (in the reservoir slot / in the plate):\n")
                sos = sorted({r["standoff_mm"] for r in b["sweep"]})
                L.append("| LP candidate | " + " | ".join(f"lens front +{s:g} mm" for s in sos) + " |")
                L.append("|---|" + "---:|" * len(sos))
                for cand in dict.fromkeys(r["candidate"] for r in b["sweep"]):
                    rr = {r["standoff_mm"]: r for r in b["sweep"] if r["candidate"] == cand}
                    L.append(f"| {cand} | " + " | ".join(f"{rr[s]['in_slot_cm3']:.0f} / {rr[s]['in_plate_cm3']:.0f}" for s in sos) + " |")
                L.append("\nNo standoff keeps a 50 mm lens and a 30 mm camera below the bridge: at the spec's position it always "
                         "stands in the reservoir slot, at the back-half one it always needs the cut-out. A fold mirror or a shorter "
                         "lens would.")
            back = next((r for r in b["rows"] if r["candidate"] == "back"), None)
            if back and back.get("f_hz"):
                L.append("\n![Mode 1 of the bridge with the back-half LP cut-out](../analysis/out/monitoring/mech/bridge_fea/bridge_mode1_back.png)")
    else:
        L.append(b.get("note", ""))
    L.append("")
    a = R["6"]
    L.append("### 6. Acoustic emission: waveguide or rod end\n")
    L.append(f"Ø{a['waveguide_d_mm']:g} mm 316 waveguide from the plate's underside through the heater block, the thermal break, the piston head, "
             f"the hollow rod and its end cap ({a['thermal'][0]['inside_length_mm']:.0f} mm), then out into air:\n")
    L.append(f"| Module case (thermal.json) | Plate (°C) | Rod end (°C) | Sensor at the end cap (°C) | 25 mm out | 50 mm out | "
             f"Length out for ≤ 60 °C (mm), air {VLM_AIR[0]:.0f} / {VLM_AIR[1]:.0f} °C |")
    L.append("|---|---:|---:|---:|---:|---:|---:|")
    for r in a["thermal"]:
        L.append(f"| {r['case']} | {r['T_plate']:.0f} | {r['T_rod_end']:.1f} | {r['T_sensor_out0']:.1f} | {r['T_sensor_out25']:.1f} | "
                 f"{r['T_sensor_out50']:.1f} | {fmt(r['L_out_for_60C_mm'], 0)} / {fmt(r['L_out_for_60C_busy_mm'], 0)} |")
    L.append("")
    L.append("| Tip radius (mm) | Preload (N) | Contact Ø (µm) | Peak pressure (MPa) | Dents the 6061 plate? |")
    L.append("|---:|---:|---:|---:|---|")
    for h in a["hertz"]:
        L.append(f"| {h['R_mm']:g} | {h['F_N']:.0f} | {h['contact_d_um']:.0f} | {h['p0_MPa']:.0f} | {fmt(h['yields_6061'])} |")
    L.append("")
    L.append(f"Bar velocity {a['bar_velocity_m_s']:.0f} m/s.\n")
    L.append("| f (kHz) | Wavelength (mm) | d/λ | Phase-velocity drop, Ø3 (%) | same, Ø8 drawbar (%) | Dry tip R 1.5 (dB) | Dry tip R 50 (dB) | Greased flat tip (dB) |")
    L.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in a["acoustics"]:
        L.append(f"| {r['f_kHz']:.0f} | {r['wavelength_mm']:.1f} | {r['d_over_lambda']:.2f} | {r['phase_velocity_drop_pct']:.2f} | "
                 f"{r['phase_velocity_drop_drawbar8_pct']:.1f} | {r['dry_tip_R1.5_dB']:.0f} | {r['dry_tip_R50_dB']:.0f} | {r['greased_flat_tip_dB']:.2f} |")
    L.append("")
    L.append(f"- **Loss budget:** waveguide with greased ends {a['total_waveguide_dB'][0]:.0f}-{a['total_waveguide_dB'][1]:.0f} dB; "
             f"sensor on the rod end {a['total_rod_end_dB'][0]:.0f}-{a['total_rod_end_dB'][1]:.0f} dB (graphite foil twice, two Macor "
             f"contacts, the three Ø8 standoffs carrying {100 * a['standoff_area_fraction']:.1f} % of the block's area, head/rod/end cap).")
    L.append(f"- **Rod end:** at most {a['rod_end_max_C']:.1f} °C with clean gaps, {a['rod_end_powder_gaps_C']:.1f} °C with powder in "
             "them (thermal.json), against ~75 °C for a sensor there; keep its preamp off the rod.")
    L.append("- **Where the loss is:** in the contacts, not the impedance mismatches. Al/Macor is 0.04 dB as a bonded interface "
             "(Edison's answer gives 1–2 dB for a 0.13–0.20 reflection coefficient, which is 0.07–0.18 dB); Al/316 is 1 dB. A dry "
             "point contact at the tip costs 10–34 dB at 100–500 kHz; a greased flat tip under 1 dB. Rod attenuation hardly matters: "
             "even 5 dB/m, ten times the value assumed here, is 1 dB over the guide.")
    L.append("- **Drawbar as the guide** (the robot cell's, hot-swap.md): at Ø8 mm its phase velocity drops 4 % at 300 kHz and "
             "12 % at 500 kHz (Rayleigh-Love, rough past d/λ 0.3): fine to ~200 kHz, smeared above. It also adds the pull stud and "
             "ball-lock contacts to the path.")
    L.append("")
    t = R["7"]
    L.append("### 7. Temperatures at the ports\n")
    L.append("| Item | Temperature (°C) | Basis | Limit |")
    L.append("|---|---|---|---|")
    for r in t["rows"]:
        L.append(f"| {r['item']} | {r['T_C']} | {r['basis']} | {r['limit']} |")
    L.append(f"\n- **Flag:** {t['flag']}.")
    pg = t["purge"]
    L.append("\n**The LW slide with its argon purge.** The purge blows bottled argon across the slide's chamber face; the slide's other "
             "face looks at the outer window across the bore. plume.md (§4.3) found that a slide 10 K colder than the gas next to it "
             "collects 20–120× more condensate:\n")
    L.append("| Purge (L/min) | Exit speed (m/s) | h, purge side / window side (W/m²K) | Chamber gas (°C) | Purge gas (°C) | Slide (°C) | Colder than the gas (K) | Heater to warm the purge to the gas (W) |")
    L.append("|---:|---:|---|---:|---:|---:|---:|---:|")
    for r in pg["rows"]:
        L.append(f"| {r['purge_lpm']:g} | {r['u_m_s']:.1f} | {r['h_purge']:.0f} / {r['h_back']:.0f} | {r['T_gas']:.0f} | {r['T_purge']:.0f} | "
                 f"{r['T_slide']:.1f} | {r['colder_than_gas_K']:.1f} | {r['heater_to_match_W']:.2f} |")
    L.append(f"\n- With the purge off the slide sits {min(o['T_slide'] - o['T_gas'] for o in pg['purge_off']):.1f}-"
             f"{max(o['T_slide'] - o['T_gas'] for o in pg['purge_off']):.1f} K above the gas (the plate's radiation): it repels condensate.")
    L.append(f"- **A room-temperature purge makes the slide up to {pg['worst_colder_K']:.0f} K colder than a hot chamber's gas**, which can "
             f"undo what the purge gains (13–45×, plume.md). Warm the purge to the chamber gas: at most {pg['heater_max_W']:.1f} W, a "
             "heater-taped stainless tube before the needle valve with a thermocouple, or take the purge from the recirculation loop.")
    return "\n".join(L) + "\n"


SOURCES = [
    "Young, W.C., Budynas, R.G. (2002). Roark's Formulas for Stress and Strain, 7th ed.: Table 11.2 case 10a (disc, simply supported, "
    "uniform pressure), Table 11.4 case 1a (rectangle, simply supported).",
    "Corning HPFS 7980 fused silica: E 72.7 GPa, nu 0.16, CTE 0.52-0.57 ppm/K; 52.4 MPa abraded modulus of rupture (the value "
    "analysis/fea/fea.py case 7 uses). SCHOTT N-BK7 datasheet (E 82 GPa, CTE 7.1 ppm/K; no modulus of rupture published).",
    "Parker O-Ring Handbook ORD 5700: face-seal gland for 1.78 mm cord (cad/module_params.py FACE_1P78, pick_ring).",
    "ASME BPVC Section VIII-1, Appendix 2, Table 2-5.1: gasket factors m = 1.00, y = 200 psi for elastomer >= 75A.",
    "ISO 898-1 (M4 stress area 8.78 mm2), ISO 3506-1 (A4-70 proof stress 450 MPa); Shigley's Mechanical Engineering Design "
    "(preload 75 % of proof for reusable joints; T = K F d).",
    "Johnson, K.L. (1985). Contact Mechanics: Hertz sphere-on-flat; first yield at p0 = 1.6 Y.",
    "Graff, K.F. (1975). Wave Motion in Elastic Solids: bar velocity, Rayleigh-Love correction for a rod's longitudinal mode.",
    "Incropera, F.P. et al. Fundamentals of Heat and Mass Transfer: fin equation; conduction across an annular gas gap; "
    "radiation between concentric cylinders.",
    "Edison r8-ae-waveguide (desktop-lpbf/edison/r8-ae-waveguide/answer.md): waveguide sizes and preload (9-22 N), interface "
    "losses, ~13 dB for a 1.59 x 306 mm guide vs direct mounting (Zelenyak 2015), 145 mm guide 200 -> ~50 C (Kazys 2021), "
    "couplant < 5 dB (Xu 2024).",
    "This repo: analysis/out/thermal/thermal.json (module thermal FEA), analysis/out/fea/fea.json (case 6b bridge modes), "
    "heat.md §2 (Shuttle air), analysis/out/monitoring/fab/frame_features.json (port seats and clamps), monitoring-bom.csv "
    "(windows and slides), monitoring/optics-parts.csv and analysis/monitoring/optics/parts.py (camera, lens, tube lens).",
]

LIMITS = [
    "**Bought parts' masses and sizes are estimates** (mech_inputs.ASSUMED): the Thorlabs cage parts from their size, the Kowa "
    "lens as Ø36 x 51 mm and 0.15 kg, the Chronos at the spec's 1.0 kg. Weigh or look them up before the bracket is cut.",
    "**Window thickness tolerance (+/-0.2 mm) and the FKM's compression modulus (6-12 MPa) are assumptions.** They set the "
    "gasket squeeze and force; check the windows' certificates and squeeze a sample of the sheet.",
    "**The bracket model is a plate cantilever.** The bolted root, the camera's own tripod thread and any adapter all add "
    "compliance and lower f1: take the next plate size up, or add a gusset, if the root isn't a stiff bolted face.",
    "**Vibration levels are assumed** (1 mm/s RMS at 60 Hz); the blower isn't chosen. Measure on the built frame with the blower "
    "and recoater running before trusting high-zoom side video.",
    "**The bridge modal runs use hmax 12** (fea.py's case 6b uses 10; the uncut bridge agrees within 0.5 % for modes 1-4) and the "
    "assumed camera envelope + 3 mm. A different camera or boss height moves the cut.",
    "**The AE numbers are 1-D estimates.** The tip as a contact spring, impedance mismatches at normal incidence, attenuation "
    "extrapolated to 100-500 kHz, interface ranges from Edison. Only pencil-lead breaks on the real stack (monitoring.md §5.4) "
    "settle the choice.",
    "**The waveguide's route is not drawn.** It shares the hollow rod (ID 12.7) with the heater and thermocouple leads, and with "
    "the drawbar in the robot cell; it needs its own seal through the end cap (an O-ring round a Ø3 rod damps it little; not "
    "checked).",
    "**Temperatures at the ports are lumped.** No CFD of the guard's air; Kron's operating range for the Chronos wasn't found.",
    "**Not checked:** the slide clips, the purge port's flow forces, the LP boss's stresses (its loads are grams), the cage's post "
    "clamps.",
]


def summary_rows(R):
    w, s, c, g, b, a, t = (R[k] for k in "1234567")
    fs = [r for r in w["windows"] if r["glass"] == "fused silica"]
    bk7 = next(r for r in w["windows"] if r["glass"] == "N-BK7")
    flat_bom, flat_1mm = s["flat_gasket"]
    pick = c["pick"]
    back = next((r for r in b.get("rows", []) if r["candidate"] == "back"), None)
    spec = next((r for r in b.get("rows", []) if r["candidate"] == "spec"), None)
    worst = max(a["thermal"], key=lambda r: r["L_out_for_60C_busy_mm"] or 0)
    return [
        ("1. Windows and slides", "pass" if w["pass_"] else "FAIL",
         f"fused silica SF {min(r['SF'] for r in fs):.0f}-{max(r['SF'] for r in fs):.0f} at 1 atm (SF 4 wanted); a borosilicate BW window "
         f"would need an abraded strength of {bk7['MR_needed_for_SF4_MPa']:.1f} MPa, which nobody publishes: make it fused silica. Slides: "
         f"< 1 K from the plate, spatter well inside fused silica's thermal-shock limit."),
        ("2. Seals and clamps", "pass with 1.0 mm FKM" if flat_1mm["pass_"] else "FAIL",
         f"the 0.75 mm the seats leave squeezes 1.0 mm sheet {100 * flat_1mm['squeeze_min']:.0f}-{100 * flat_1mm['squeeze_max']:.0f} %, but the "
         f"BOM's 1/32 in. sheet only {100 * flat_bom['squeeze_min']:.0f} to {100 * flat_bom['squeeze_max']:.0f} %: **change M0-06 to 1.0 mm "
         f"sheet**. Clamp screws at {s['torque_Nm']:.0f} N·m: lift-off margin {min(x['separation_margin'] for x in s['clamps']):.1f} or more."),
        ("3. Side camera bracket", "pass" if c["pass_"] else "FAIL",
         (f"a {pick['t_in']:g} in. ({pick['t_mm']:.1f} mm) x {c['bracket_width_mm']:.0f} mm 6061 plate, {c['reach_mm']:.0f} mm reach: f1 "
          f"{pick['f1_hz']:.0f} Hz (≥ 150 wanted, 2.5x the blower's 60 Hz), vibration {pick['dyn_image_um_at_60Hz']:.1f} µm at the plate "
          f"against a {c['px_across_um']:.0f} µm pixel; 1/2 in. gives {c['rows'][2]['f1_hz']:.0f} Hz. A fixed 13° wedge, not a ball head.")
         if pick else "no plate up to 1 in. passes"),
        ("4. Coaxial cage", "pass" if g["pass_"] else "FAIL",
         f"{g['mass_kg']:.2f} kg added; post every cube and each branch end; drift {g['drift_um_per_K_post_difference']:.1f} µm/K at the "
         f"plate; bridge sway {g['bridge_f1_hz']:.0f} -> {g['bridge_f1_with_cage_hz']:.0f} Hz."),
        ("5. Lid camera vs the bridge", "pass (back-half LP)" if back and b.get("pass_") else ("open" if not back else "FAIL"),
         (f"at the spec's LP {tuple(round(x) for x in spec['centre'])} the camera fits the reservoir slot ({spec['in_reservoir_slot_cm3']:.0f} cm³ "
          f"of it) and **blocks the reservoirs' way out**; at the back-half LP {tuple(round(x) for x in back['centre'])} it needs a cut-out "
          f"of {back['cut_bbox_xy'][1] - back['cut_bbox_xy'][0]:.0f} x {back['cut_bbox_xy'][3] - back['cut_bbox_xy'][2]:.0f} mm, which moves f1 "
          f"{back['df1_pct']:+.1f} % (to {back['f_hz'][0]:.0f} Hz) and the higher modes {min(back['df_pct']):+.1f} % at most.")
         if back and spec and back.get("f_hz") else b.get("note", "")),
        ("6. AE path", "pass" if a["pass_"] else "FAIL",
         f"a Ø{a['waveguide_d_mm']:g} waveguide reaches the end cap at {worst['T_sensor_out0']:.0f} °C in the worst case (powder in the gaps) "
         f"and is under 60 °C {worst['L_out_for_60C_busy_mm']:.0f} mm out in 43 °C air; tip R >= 25 mm at 10-20 N (a Ø3 ball dents the plate); "
         f"loss {a['total_waveguide_dB'][0]:.0f}-{a['total_waveguide_dB'][1]:.0f} dB greased vs {a['total_rod_end_dB'][0]:.0f}-"
         f"{a['total_rod_end_dB'][1]:.0f} dB at the rod end; rod end {a['rod_end_max_C']:.0f} °C ({a['rod_end_powder_gaps_C']:.0f} with powder in the gaps)."),
        ("7. Temperatures at the ports", "flag",
         f"windows and slides at wall temperature (25-61 °C), fine for FKM and fused silica; but a room-temperature purge makes the LW "
         f"slide up to {t['purge']['worst_colder_K']:.0f} K colder than a hot chamber's gas, which draws condensate (plume.md): warm the purge "
         f"(≤ {t['purge']['heater_max_W']:.1f} W). The cameras sit in the Shuttle's air, 38-43 °C in the busy case, at or above a 40 °C rating."),
    ]


def write_checks_md(R, tables):
    L = ["<!-- generated by analysis/monitoring/mech/mech_monitoring.py, to paste under '## Checks' in monitoring/mechanics.md: "
         "its links are relative to desktop-lpbf/monitoring/ -->", ""]
    B = "../analysis/out/monitoring/mech"
    L.append(f"Run {R['run_utc']} UTC by [`mech_monitoring.py`](../analysis/monitoring/mech/mech_monitoring.py) and "
             f"[`bridge_modal.py`](../analysis/monitoring/mech/bridge_modal.py) (CalculiX); every number is in "
             f"[`checks.json`]({B}/checks.json) and [`bridge_modal.json`]({B}/bridge_modal.json).\n")
    L.append("| Check | Result | In one line |")
    L.append("|---|---|---|")
    for name, res, line in summary_rows(R):
        L.append(f"| {name} | {res} | {line} |")
    L.append("")
    L.append(f"![Waveguide temperatures through the module and window safety factors]({B}/checks.png)\n")
    L.append(tables)
    L.append("### Sources\n")
    L += [f"- {s}" for s in SOURCES]
    L.append("\n### Not done / limits\n")
    L += [f"- {s}" for s in LIMITS]
    return "\n".join(L) + "\n"


def make_figure(R, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), dpi=110)
    a = R["6"]
    cols = ["#2b6cd2", "#5fa8e8", "#d2602b", "#f0a35e", "#7f8890", "#151719", "#8e44ad", "#c39bd3"]
    k50 = [k for k in a["profiles"] if k.endswith("|50")]
    for i, k in enumerate(k50):
        v = a["profiles"][k]
        c = cols[i % len(cols)]
        ax[0].plot(v["z"], v["T"], color=c, lw=1.5, label=k.split("|")[0].replace("_", " "))
        ax[0].plot(v["z"], v["Ts"], color=c, lw=0.7, ls=":")
    zs = np.cumsum([0, MP.BLOCK_T, MP.BREAK_T, MP.HEAD_T, MP.ROD_L, MP.ROD_END_T])
    for z0, z1, lab in zip(zs[:-1], zs[1:], ["block", "break", "head", "hollow rod", "end cap"]):
        ax[0].axvline(z0, color="#bbbbbb", lw=0.6)
        ax[0].text((z0 + z1) / 2, 8, lab, fontsize=6.5, color="#555555", rotation=90, va="bottom", ha="center")
    ax[0].text(zs[-1] + 3, 8, "in air", fontsize=6.5, color="#555555", rotation=90, va="bottom")
    ax[0].axvline(zs[-1], color="#555555", lw=0.8)
    ax[0].axhline(MI.AE["sensor_t_max_C"], color="#c0392b", lw=0.8, ls="--")
    ax[0].text(zs[-1] + 2, MI.AE["sensor_t_max_C"] + 6, "sensor 60 °C", fontsize=7, color="#c0392b")
    ax[0].set_xlabel("distance from the plate's underside along the waveguide (mm)")
    ax[0].set_ylabel("temperature (°C)")
    ax[0].set_title(f"Ø{a['waveguide_d_mm']:g} mm 316 waveguide, 50 mm out into air (dotted: surroundings)", fontsize=9)
    ax[0].legend(fontsize=7, loc="upper right")
    ax[0].set_ylim(0, 520)
    w = [r for r in R["1"]["windows"]]
    names = [r["port"].replace(" (", "\n(") for r in w]
    sf = [r["SF"] if r["SF"] else r["MR_needed_for_SF4_MPa"] / MI.SF_WINDOW * 0 for r in w]
    ax[1].barh(range(len(w)), [s or 0 for s in sf], color=["#2b6cd2" if r["SF"] else "#bbbbbb" for r in w])
    for i, r in enumerate(w):
        txt = f"SF {r['SF']:.0f}" if r["SF"] else f"N-BK7: needs MR ≥ {r['MR_needed_for_SF4_MPa']:.0f} MPa"
        ax[1].text((r["SF"] or 0) + 0.5, i, txt, va="center", fontsize=7)
    ax[1].axvline(MI.SF_WINDOW, color="#c0392b", lw=0.9, ls="--")
    ax[1].set_yticks(range(len(w)))
    ax[1].set_yticklabels(names, fontsize=7)
    ax[1].set_xlabel("safety factor at 1 atm (fused silica, MR 52.4 MPa)")
    ax[1].set_title("Viewport windows at vacuum (dashed: SF 4)", fontsize=9)
    ax[1].invert_yaxis()
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    R = {}
    R["1"] = check_windows()
    R["2"] = check_seals()
    R["3"] = check_side_camera()
    R["4"] = check_cage()
    R["5"] = check_bridge()
    R["6"] = check_ae()
    R["7"] = check_port_thermal(R["1"])
    R["run_utc"] = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
    (OUT / "checks.json").write_text(json.dumps(R, indent=1, default=float))
    (OUT / "checks.md").write_text(write_checks_md(R, write_md(R)))
    make_figure(R, OUT / "checks.png")
    for k in "1234567":
        print(k, "pass" if R[k].get("pass_") else ("n/a" if R[k].get("pass_") is None else "FAIL"))
    return R


if __name__ == "__main__":
    main()
