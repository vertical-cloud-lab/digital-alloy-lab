#!/usr/bin/env python3
"""The f-theta outside 1064 nm (issue #260, monitoring/optics.md §1).

Thorlabs publishes no prescription for the FTH160-1064: its Zemax download is a ZAR archive whose lens file is a black box
("265-FTH160-1064-R1A - with-mirrors_BB.ZMX"). So this script designs REPRESENTATIVE 3-element 1064 nm f-theta lenses that
meet the published specs (EFL 160 mm, 12 mm beam, scan angle +/-28 deg, working distance 182.5 mm behind an N-BK7 protective
window, A2 = 12.3 mm from the 2nd galvo mirror to the first vertex, f-theta distortion < 0.1 %), each with real glasses,
optimised at 1064 nm. Three glass sets bracket the unknown real one:
  FS      all fused silica (high-power industrial style)
  SF11    all N-SF11 dense flint (typical marking lens: high index, few elements)
  SF11+BK7  N-SF11 negative meniscus, N-BK7 positives (partly colour-corrected)
It then traces each one, in the machine's geometry (2nd mirror 35 mm above the lens's nose, the 9.53 mm fused-silica chamber
window and the 2 mm cover slide as drawn in cad/lpbf_low.py), from 600 to 1700 nm: focal shift against 1070 nm, field
curvature, lateral colour on the plate across the M50 and L75 fields, and spot sizes in the camera bands. It compares them
with monitoring_optics.py's fused-silica singlet estimate, and checks the design against Thorlabs' published 1064 nm field
curvature (+0.2 mm on axis; tangential +0.02 / sagittal -0.14 mm at 20 deg).

    python desktop-lpbf/analysis/monitoring/optics/ftheta.py        (~1-2 min; run under /tmp/capmem 2)

Writes analysis/out/monitoring/optics/ftheta.json, ftheta.md, ftheta.png.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                      # desktop-lpbf/
OUT = ROOT / "analysis" / "out" / "monitoring" / "optics"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "cad"))
import raytrace as RT  # noqa: E402
import lpbf_low as MODEL  # noqa: E402   (lens, galvo, window and slide heights)

P_ = MODEL.P
EFL, EPD, WD, A2 = 160.0, 12.0, 182.5, 12.3          # Thorlabs FTH160-1064 spec table (f-theta-scan-lenses, fetched 2026-11-25T06:39Z)
A1 = 7.5
LAM_D = 1.064
FIELDS_DEG = (0.0, 7.0, 14.0, 21.0, 28.0)
W_FIELD = (1.0, 1.0, 1.0, 1.0, 0.5)
LENS_LEN = 50.2                                      # housing length (drawing); nose 41.0 mm above the flange
# machine geometry (cad/lpbf_low.py P block): lens output end, nose, 2nd galvo mirror, window, slide
Z_OUT = P_["z_lens0"]                                # 186.08: the protective window's outer face, taken as the WD reference
Z_NOSE = Z_OUT + LENS_LEN
Z_M2 = P_["z_galvo_m2"]                              # 271.11
A1_MACHINE = Z_M2 - Z_NOSE                           # ~34.8 mm (Thorlabs: 7.5)
Z_W0, Z_W1 = P_["z_win0"], P_["z_win0"] + P_["win_t"]
Z_S0, Z_S1 = P_["z_slide0"], P_["z_slide0"] + P_["slide_t"]

GLASS_SETS = {"FS": ("F_SILICA", "F_SILICA", "F_SILICA"),
              "SF11": ("N-SF11", "N-SF11", "N-SF11"),
              "SF11+BK7": ("N-SF11", "N-BK7", "N-BK7")}


def build(x, glasses, stop_to_v1=A2, with_plates=False):
    """Surfaces in a frame with the stop (2nd galvo mirror) at z = 0 and light going +z. x = [c1..c6, t1, g1, t2, g2, t3, g3].
    Returns (surfs, z_image) where z_image is the nominal image plane (air WD behind the window, or the plate)."""
    c = x[:6]
    t1, g1, t2, g2, t3, g3 = x[6:]
    z = stop_to_v1
    S = []
    for i, (ca, cb, t, g, gl) in enumerate(((c[0], c[1], t1, g1, glasses[0]), (c[2], c[3], t2, g2, glasses[1]),
                                            (c[4], c[5], t3, g3, glasses[2]))):
        S.append(RT.Surf(z, ca, gl, 45.0))
        S.append(RT.Surf(z + t, cb, "AIR", 45.0))
        z += t + g
    S.append(RT.Surf(z, 0.0, "N-BK7", 37.5))          # protective window FTHW75-1064: N-BK7, 2.0 mm
    S.append(RT.Surf(z + 2.0, 0.0, "AIR", 37.5))
    z_out = z + 2.0
    if not with_plates:
        return S, z_out + WD
    # machine: chamber window and cover slide below the lens output end (heights from the model)
    for zt, zb in ((Z_W1, Z_W0), (Z_S1, Z_S0)):
        S.append(RT.Surf(z_out + (Z_OUT - zt), 0.0, "F_SILICA", 25.4))
        S.append(RT.Surf(z_out + (Z_OUT - zb), 0.0, "AIR", 25.4))
    return S, z_out + Z_OUT                             # the plate (z = 0 in machine coordinates)


def efl_of(S, lam):
    h = 0.25
    P0 = np.array([[0.0, h, -1.0]])
    D0 = np.array([[0.0, 0.0, 1.0]])
    P, D, ok = RT.trace(P0, D0, S, lam)
    return -h / (D[0, 1] / D[0, 2])


GRID = RT.pupil_grid(5, 12)
N_RES = 1 + sum(3 + (th > 0) for th in FIELDS_DEG) + 7


def merit(x, glasses):
    S, zi = build(x, glasses)
    r = []
    try:
        f = efl_of(S, LAM_D)
    except Exception:  # noqa: BLE001
        return np.full(N_RES, 1e3)
    r.append((f - EFL) / 0.05)
    for th, w in zip(FIELDS_DEG, W_FIELD):
        P0, D0, _ = RT.beam_rays(math.radians(th), EPD, 0.0, GRID)
        P, D, ok = RT.trace(P0, D0, S, LAM_D)
        if not ok.all():
            r += [1e2] * (3 + (th > 0))
            continue
        rms, cen = RT.rms_at(P, D, zi)
        r.append(w * rms / 0.002)
        # field curvature: tangential and sagittal foci within ~0.2 mm of the image plane (Thorlabs' curve stays within +/-0.2 mm)
        zt, _ = RT.best_focus(P, D, axis=1)
        zs, _ = RT.best_focus(P, D, axis=0)
        r.append(w * (zt - zi) / 0.1)
        r.append(w * (zs - zi) / 0.1)
        if th > 0:
            r.append(w * (cen[1] - EFL * math.radians(th)) / (EFL * math.radians(th)) / 2e-4)
    # mechanical: edge thickness >= 1.5 mm, edge air gaps >= 0.3 mm, total length <= 44 mm (housing 50.2)
    c = x[:6]
    sd = [12.0, 14.0, 17.0, 19.0, 22.0, 24.0]
    sag = [ci * s * s / (1 + math.sqrt(max(1 - (ci * s) ** 2, 1e-9))) for ci, s in zip(c, sd)]
    t1, g1, t2, g2, t3, g3 = x[6:]
    edges = [t1 - sag[0] + sag[1], t2 - sag[2] + sag[3], t3 - sag[4] + sag[5]]
    for e in edges:
        r.append(max(0.0, 1.5 - e) * 50)
    for g, sa, sb in ((g1, sag[1], sag[2]), (g2, sag[3], sag[4]), (g3, sag[5], 0.0)):
        r.append(max(0.0, 0.3 - (g - sa + sb)) * 50)
    total = t1 + g1 + t2 + g2 + t3 + g3 + 2.0
    r.append(max(0.0, total - 44.0) * 10)
    return np.array(r)


X0 = np.array([-1 / 30, -1 / 60, -1 / 150, -1 / 45, 1 / 300, -1 / 120, 4.0, 4.0, 8.0, 1.0, 8.0, 2.0])
LO = np.array([-0.07] * 6 + [2.5, 0.5, 2.5, 0.5, 2.5, 0.5])
HI = np.array([0.07] * 6 + [14.0, 20.0, 14.0, 20.0, 14.0, 10.0])


def design(glasses, seeds=8, rng=None):
    rng = rng or np.random.default_rng(260)
    best = None
    for k in range(seeds):
        x0 = X0.copy() if k == 0 else np.clip(X0 * (1 + 0.25 * rng.standard_normal(12)), LO + 1e-6, HI - 1e-6)
        try:
            res = least_squares(merit, x0, args=(glasses,), bounds=(LO, HI), x_scale="jac", max_nfev=400)
        except Exception:  # noqa: BLE001
            continue
        if best is None or res.cost < best.cost:
            best = res
    return best.x, best.cost


def describe(x, glasses):
    S, zi = build(x, glasses)
    rows = []
    for i, s in enumerate(S):
        nxt = S[i + 1].z - s.z if i + 1 < len(S) else zi - s.z
        rows.append(dict(surface=i + 1, R_mm=(1 / s.c if s.c else float("inf")), thickness_mm=nxt, medium_after=s.after))
    perf = []
    for th in (0.0, 4.55, 9.1, 13.6, 20.0, 28.0):
        P0, D0, _ = RT.beam_rays(math.radians(th), EPD, 0.0, GRID)
        P, D, ok = RT.trace(P0, D0, S, LAM_D)
        rms, cen = RT.rms_at(P, D, zi)
        zt, _ = RT.best_focus(P, D, axis=1)
        zs, _ = RT.best_focus(P, D, axis=0)
        perf.append(dict(field_deg=th, rms_um=rms * 1e3, airy_um=1.22 * LAM_D * EFL / EPD,
                         distortion_pct=(100 * (cen[1] - EFL * math.radians(th)) / (EFL * math.radians(th)) if th else 0.0),
                         tangential_focus_mm=zt - zi, sagittal_focus_mm=zs - zi, all_rays_pass=bool(ok.all())))
    return dict(prescription=rows, efl_1064=efl_of(S, LAM_D), length_v1_to_window_mm=S[-1].z - S[0].z, perf_1064=perf)


# ---------------------------------------------------------------------------------------------------- chromatic evaluation
LAMS = (0.600, 0.650, 0.700, 0.750, 0.800, 0.850, 0.900, 0.950, 1.000, 1.070, 1.300, 1.550, 1.650)
PLATE_R = {"axis": 0.0, "S25 edge": 12.7, "M50 edge": 25.4, "L75 edge": 38.1}


def galvo_angle_for(S, r_target, lam=1.070, stop_z=0.0):
    """Optical scan angle (rad) that puts the 1070 nm chief ray on plate radius r_target (machine geometry)."""
    zi = S[-1].z + Z_S0                                  # plate below the slide's bottom face
    lo, hi = 0.0, 0.35
    for _ in range(50):
        mid = (lo + hi) / 2
        P0, D0, _ = RT.beam_rays(mid, 1e-3, stop_z, np.array([[0.0, 0.0]]))
        P, D, ok = RT.trace(P0, D0, S, lam)
        y = RT.to_plane(P, D, zi)[0, 1]
        lo, hi = (mid, hi) if y < r_target else (lo, mid)
    return (lo + hi) / 2


def chroma(x, glasses, stop_to_v1):
    """Trace in the machine geometry: stop = 2nd galvo mirror, chamber window and slide in place."""
    S, z_plate = build(x, glasses, stop_to_v1=stop_to_v1, with_plates=True)
    res = {}
    grid = RT.pupil_grid(6, 14)
    for name, r in PLATE_R.items():
        th = galvo_angle_for(S, r) if r > 0 else 0.0
        rec = dict(galvo_optical_deg=math.degrees(th), by_lambda={})
        ref = None
        for lam in LAMS:
            out = {}
            for epd in (6.0, 12.0, 18.0):
                P0, D0, _ = RT.beam_rays(th, epd, 0.0, grid)
                P, D, ok = RT.trace(P0, D0, S, lam)
                Pm, Dm = P[ok], D[ok]
                zb, rms_b = RT.best_focus(Pm, Dm)
                zt, _ = RT.best_focus(Pm, Dm, axis=1)
                zs, _ = RT.best_focus(Pm, Dm, axis=0)
                rms_p, cen_p = RT.rms_at(Pm, Dm, z_plate)
                # chief ray (beam centre) on the plate
                Pc, Dc, _ = RT.trace(*RT.beam_rays(th, 1e-3, 0.0, np.array([[0.0, 0.0]]))[:2], S, lam)
                yc = RT.to_plane(Pc, Dc, z_plate)[0, 1]
                out[f"epd{int(epd)}"] = dict(best_focus_mm=z_plate - zb, tangential_mm=z_plate - zt, sagittal_mm=z_plate - zs,
                                             rms_at_best_um=rms_b * 1e3, rms_on_plate_um=rms_p * 1e3, chief_y_on_plate_mm=yc,
                                             airy_radius_um=1.22 * lam * EFL / epd, vignetted=int((~ok).sum()))
            rec["by_lambda"][f"{lam * 1000:.0f}"] = out
        # relative to 1070 nm: focal shift (positive = focus above the plate, toward the lens) and lateral colour on the plate
        r1070 = rec["by_lambda"]["1070"]["epd12"]
        for lam_k, out in rec["by_lambda"].items():
            for k, o in out.items():
                o["focal_shift_vs_1070_mm"] = o["best_focus_mm"] - r1070["best_focus_mm"]
                o["lateral_colour_um"] = (o["chief_y_on_plate_mm"] - r1070["chief_y_on_plate_mm"]) * 1e3
        res[name] = rec
    return res


def singlet_estimate(lam_um, r_mm):
    """monitoring_optics.py's estimate: an all-fused-silica singlet of f = 160 mm (focus shift and lateral colour)."""
    nl, n0 = float(RT.n_glass("F_SILICA", lam_um)), float(RT.n_glass("F_SILICA", 1.070))
    df = EFL * (nl - n0) / (n0 - 1)
    return df, df * r_mm / EFL * 1e3


def band_spread(x, glasses, stop_to_v1, lam_c, half):
    """Focus spread over a filter band (lam_c +/- half), on axis, 12 mm pupil, and the blur it gives at that NA."""
    S, z_plate = build(x, glasses, stop_to_v1=stop_to_v1, with_plates=True)
    zs = []
    for lam in (lam_c - half, lam_c + half):
        P0, D0, _ = RT.beam_rays(0.0, 12.0, 0.0)
        P, D, ok = RT.trace(P0, D0, S, lam)
        zs.append(RT.best_focus(P[ok], D[ok])[0])
    dz = abs(zs[1] - zs[0])
    return dz, dz * (6.0 / EFL) * 1e3      # blur diameter ~ dz * 2 NA, i.e. +/- dz/2 at NA 0.0375 -> dz * NA


def chief_k(x, glasses, stop_to_v1, r_mm):
    """k = chief-ray angle at the plate / optical scan angle (optics.md §1.4), for the 1070 nm chief ray landing at r_mm."""
    S, z_plate = build(x, glasses, stop_to_v1=stop_to_v1, with_plates=True)
    th = galvo_angle_for(S, r_mm)
    P, D, ok = RT.trace(*RT.beam_rays(th, 1e-3, 0.0, np.array([[0.0, 0.0]]))[:2], S, 1.070)
    return math.atan2(D[0, 1], D[0, 2]) / th, th


def main(reuse=False):
    prev = json.loads((OUT / "ftheta.json").read_text()) if reuse and (OUT / "ftheta.json").exists() else None
    R = dict(sources=dict(
        thorlabs_spec="Thorlabs f-theta family page, https://www.thorlabs.com/f-theta-scan-lenses (fetched 2026-11-25T06:39Z): FTH160-1064 "
                      "EFL 160 mm, +/-28 deg, 110.6 mm field, 12 mm beam, WD 182.5 mm, FFL 191.7 mm, A1 7.5, A2 12.3, dM 20 mm, "
                      "3 elements + protective window (N-BK7 2.0 mm), AR 1020-1080 nm Ravg < 0.3 % and 450-700 nm < 1.0 % per surface",
        thorlabs_field_curvature="fth160-1064_fthetadistortion_780.gif (sha256 3174d33c925d7fb9...): field curvature +0.20 mm on axis, "
                                 "tangential ~+0.02 / sagittal ~-0.14 mm at 20 deg, +0.08 / +0.12 at 28 deg; distortion < 0.06 %",
        thorlabs_zemax="FTH160-1064 'Zemax (ZAR)' download (sha256 8ca3d220a2727e11..., 147,788 bytes): lens file "
                       "'265-FTH160-1064-R1A - with-mirrors_BB.ZMX', a black box; not unpacked here",
        glasses="Sellmeier: Malitson 1965 (fused silica); SCHOTT data sheets (N-BK7, N-SF11)",
        model="cad/lpbf_low.py P block: lens output end z %.2f, nose z %.2f, 2nd mirror z %.2f (A1 %.1f mm), window z %.2f-%.2f, slide z %.1f-%.1f"
              % (Z_OUT, Z_NOSE, Z_M2, A1_MACHINE, Z_W0, Z_W1, Z_S0, Z_S1)))
    R["designs"] = {}
    stop_machine = A2 + (A1_MACHINE - A1)               # the 2nd mirror to the first vertex in the machine
    for name, gl in GLASS_SETS.items():
        if prev and name in prev["designs"]:
            x, cost = np.array(prev["designs"][name]["x"]), prev["designs"][name]["merit_cost"]
        else:
            x, cost = design(gl)
        d = describe(x, gl)
        d["glasses"] = list(gl)
        d["x"] = list(map(float, x))
        d["merit_cost"] = float(cost)
        d["chroma_machine"] = chroma(x, gl, stop_machine)
        d["band_spread"] = {f"{lc * 1000:.0f}+/-{h * 1000:.0f} nm": dict(zip(("focus_spread_mm", "blur_um_NA0.0375"),
                                                                              band_spread(x, gl, stop_machine, lc, h)))
                            for lc, h in ((0.850, 0.020), (0.850, 0.005), (0.940, 0.005), (0.950, 0.005), (0.700, 0.020),
                                          (0.700, 0.005), (1.550, 0.006))}
        d["k_machine"] = {pl: chief_k(x, gl, stop_machine, r)[0] for pl, r in (("M50 edge", 25.4), ("L75 edge", 38.1))}
        d["k_thorlabs_A1"] = {pl: chief_k(x, gl, A2, r)[0] for pl, r in (("M50 edge", 25.4), ("L75 edge", 38.1))}
        R["designs"][name] = d
        print(name, "cost", round(cost, 3), "EFL", round(d["efl_1064"], 3), "len", round(d["length_v1_to_window_mm"], 1),
              "k", {k: round(v, 3) for k, v in d["k_machine"].items()}, flush=True)
    R["singlet"] = {f"{lam * 1000:.0f}": {k: dict(zip(("focal_shift_mm", "lateral_colour_um"), singlet_estimate(lam, r)))
                                          for k, r in PLATE_R.items() if r > 0} for lam in LAMS}
    R["stop_to_first_vertex_machine_mm"] = stop_machine
    (OUT / "ftheta.json").write_text(json.dumps(R, indent=1) + "\n")
    write_md(R)
    plot(R)
    return R


def write_md(R):
    D = R["designs"]
    L = ["# The f-theta outside 1064 nm (generated by analysis/monitoring/optics/ftheta.py)", "",
         "Three representative 3-element f = 160 mm f-theta lenses, each optimised at 1064 nm to the FTH160-1064's published specs, "
         "then traced in the machine's geometry (2nd galvo mirror %.1f mm before the first vertex; 9.53 mm window and 2 mm slide). "
         "Thorlabs' own prescription is a black box, so these bracket it; they are not the real lens." % R["stop_to_first_vertex_machine_mm"], "",
         "## At 1064 nm, in Thorlabs' geometry (A2 = 12.3 mm)", "",
         "| design | glasses | EFL (mm) | v1 to window (mm) | RMS spot 0 / 13.6 / 28 deg (um) | distortion max (%) | T / S focus at 13.6 deg (mm) | T / S at 28 deg (mm) |",
         "|---|---|---:|---:|---|---:|---|---|"]
    for n, d in D.items():
        p = {round(q["field_deg"], 2): q for q in d["perf_1064"]}
        L.append(f"| {n} | {' / '.join(d['glasses'])} | {d['efl_1064']:.2f} | {d['length_v1_to_window_mm']:.1f} | "
                 f"{p[0.0]['rms_um']:.1f} / {p[13.6]['rms_um']:.1f} / {p[28.0]['rms_um']:.1f} | "
                 f"{max(abs(q['distortion_pct']) for q in d['perf_1064']):.3f} | {p[13.6]['tangential_focus_mm']:+.2f} / {p[13.6]['sagittal_focus_mm']:+.2f} | "
                 f"{p[28.0]['tangential_focus_mm']:+.2f} / {p[28.0]['sagittal_focus_mm']:+.2f} |")
    L += ["", "Thorlabs (published curve): +0.20 mm on axis; T +0.02 / S -0.14 mm at 20 deg; T +0.08 / S +0.12 at 28 deg; distortion < 0.06 %. "
          "Airy radius at 1064 nm and a 12 mm beam: 17.3 um.", "",
          "## Focal shift against 1070 nm, on axis, in the machine (mm; + = toward the lens)", "",
          "| band | singlet estimate (monitoring_optics.py) | " + " | ".join(D) + " |", "|---|---:|" + "---:|" * len(D)]
    for lam in ("650", "700", "850", "950", "1300", "1550", "1650"):
        L.append(f"| {lam} nm | {R['singlet'][lam]['M50 edge']['focal_shift_mm']:+.2f} | " +
                 " | ".join(f"{d['chroma_machine']['axis']['by_lambda'][lam]['epd12']['focal_shift_vs_1070_mm']:+.2f}" for d in D.values()) + " |")
    L += ["", "## Lateral colour on the plate: where the band's view sits against the 1070 nm spot (um; - = toward the axis)", "",
          "| band | edge | singlet | " + " | ".join(D) + " |", "|---|---|---:|" + "---:|" * len(D)]
    for lam in ("700", "850", "950", "1550"):
        for e in ("M50 edge", "L75 edge"):
            L.append(f"| {lam} nm | {e} | {-R['singlet'][lam][e]['lateral_colour_um']:+.0f} | " +
                     " | ".join(f"{d['chroma_machine'][e]['by_lambda'][lam]['epd12']['lateral_colour_um']:+.0f}" for d in D.values()) + " |")
    L += ["", "## Image quality at each band's own best focus (RMS spot radius on the plate, um; 12 mm / 18 mm pupil)", "",
          "| band | field | " + " | ".join(D) + " | Airy radius, 12 mm |", "|---|---|" + "---|" * len(D) + "---:|"]
    for lam in ("700", "850", "950", "1070", "1550"):
        for e in ("axis", "M50 edge", "L75 edge"):
            L.append(f"| {lam} nm | {e} | " + " | ".join(
                f"{d['chroma_machine'][e]['by_lambda'][lam]['epd12']['rms_at_best_um']:.1f} / {d['chroma_machine'][e]['by_lambda'][lam]['epd18']['rms_at_best_um']:.1f}"
                for d in D.values()) + f" | {1.22 * int(lam) / 1000 * EFL / 12:.1f} |")
    L += ["", "## Tangential / sagittal focus at 1070 nm off axis, in the machine (mm from the plate)", "",
          "| field | " + " | ".join(D) + " |", "|---|" + "---|" * len(D)]
    for e in ("S25 edge", "M50 edge", "L75 edge"):
        L.append(f"| {e} | " + " | ".join(f"{d['chroma_machine'][e]['by_lambda']['1070']['epd12']['tangential_mm']:+.2f} / "
                                         f"{d['chroma_machine'][e]['by_lambda']['1070']['epd12']['sagittal_mm']:+.2f}" for d in D.values()) + " |")
    L += ["", "## Focus spread across a filter band (on axis, 12 mm pupil)", "", "| band | " + " | ".join(D) + " |", "|---|" + "---|" * len(D)]
    for b in next(iter(D.values()))["band_spread"]:
        L.append(f"| {b} | " + " | ".join(f"{d['band_spread'][b]['focus_spread_mm']:.2f} mm ({d['band_spread'][b]['blur_um_NA0.0375']:.0f} um blur)" for d in D.values()) + " |")
    L += ["", "## Chief-ray ratio k (angle at the plate / optical scan angle; optics.md §1.4 bounds it at 0.33-0.62 as drawn)", "",
          "| geometry | " + " | ".join(D) + " |", "|---|" + "---|" * len(D)]
    L.append("| machine (A1 %.1f mm), M50 / L75 edge | " % A1_MACHINE +
             " | ".join(f"{d['k_machine']['M50 edge']:.2f} / {d['k_machine']['L75 edge']:.2f}" for d in D.values()) + " |")
    L.append("| Thorlabs' A1 7.5 mm, M50 / L75 edge | " + " | ".join(f"{d['k_thorlabs_A1']['M50 edge']:.2f} / {d['k_thorlabs_A1']['L75 edge']:.2f}" for d in D.values()) + " |")
    L += ["", "## Prescriptions (light from the galvo toward the plate; R in mm, thickness to the next surface)", ""]
    for n, d in D.items():
        L.append(f"**{n}:** " + "; ".join(f"R {r['R_mm']:.1f}, t {r['thickness_mm']:.2f} {r['medium_after']}" for r in d["prescription"]))
        L.append("")
    (OUT / "ftheta.md").write_text("\n".join(L) + "\n")


def plot(R):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    D = R["designs"]
    lams = [int(k) for k in next(iter(D.values()))["chroma_machine"]["axis"]["by_lambda"]]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    cols = {"FS": "#1f77b4", "SF11": "#d62728", "SF11+BK7": "#2ca02c"}
    for n, d in D.items():
        ax[0].plot(lams, [d["chroma_machine"]["axis"]["by_lambda"][str(l)]["epd12"]["focal_shift_vs_1070_mm"] for l in lams], "o-", color=cols[n], label=n)
        ax[1].plot(lams, [d["chroma_machine"]["L75 edge"]["by_lambda"][str(l)]["epd12"]["lateral_colour_um"] for l in lams], "o-", color=cols[n], label=n + ", L75 edge")
        ax[1].plot(lams, [d["chroma_machine"]["M50 edge"]["by_lambda"][str(l)]["epd12"]["lateral_colour_um"] for l in lams], "s--", color=cols[n], alpha=0.6, label=n + ", M50 edge")
    ax[0].plot(lams, [R["singlet"][str(l)]["M50 edge"]["focal_shift_mm"] for l in lams], "k:", label="fused-silica singlet (old estimate)")
    ax[1].plot(lams, [-R["singlet"][str(l)]["L75 edge"]["lateral_colour_um"] for l in lams], "k:", label="singlet, L75 edge")
    for a in ax:
        a.axvspan(750, 875, color="0.88", zorder=0)
        a.axvline(1070, color="0.5", lw=0.8)
        a.set_xlabel("wavelength (nm)")
        a.grid(alpha=0.3)
    ax[0].set_ylabel("focus above the plate vs 1070 nm (mm)")
    ax[1].set_ylabel("view offset on the plate vs 1070 nm spot (um)")
    ax[0].set_title("Focal shift, on axis (machine geometry)")
    ax[1].set_title("Lateral colour (grey: reported galvo stop band)")
    ax[0].legend(fontsize=8)
    ax[1].legend(fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(OUT / "ftheta.png", dpi=130)


if __name__ == "__main__":
    main(reuse="--reuse" in sys.argv)
