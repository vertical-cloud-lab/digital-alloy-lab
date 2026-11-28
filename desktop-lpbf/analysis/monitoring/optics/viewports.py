#!/usr/bin/env python3
"""Off-axis cameras at the left-wall (LW) and steep lid (LP) viewports, their light, and laser safety at every viewport
(issue #260, monitoring/optics.md §4-5).

Geometry from cad/monitoring_spec.py (read at run time). For each camera and lens: magnification, um per pixel across and
along the view, field, f-number against depth of field and diffraction, exposure against motion blur for spatter at 1-20 m/s,
the window's effect (tilted plate: astigmatism, focus shift, boresight shift, ghosts), and the illumination power for a 10 us
exposure. Then the 1070 nm light reaching each viewport at 500 W (diffuse from the powder and the pool; specular glints from
a curved pool) and the filter OD each camera needs.

    python viewports.py
Writes analysis/out/monitoring/optics/viewports.json and viewports.md.
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
import monitoring_spec as MS  # noqa: E402
import parts as PT  # noqa: E402
import raytrace as RT  # noqa: E402

H, C = 6.62607015e-34, 2.99792458e8
FACE_NORMAL = {"-x": (-1.0, 0.0, 0.0), "+x": (1.0, 0.0, 0.0), "+y": (0.0, 1.0, 0.0), "-y": (0.0, -1.0, 0.0), "+z": (0.0, 0.0, 1.0)}


def port_geometry(key):
    v = MS.VIEWPORTS[key]
    p = np.array(v["centre"])
    ax = np.array(MS.axis_to_target(v["centre"]))          # into the chamber
    n = np.array(FACE_NORMAL[v["face"]])
    face_tilt = math.degrees(math.acos(abs(float(ax @ n))))  # a window seated on the wall's face, its normal vs the line of sight
    # a window on a boss whose end face is square to the line of sight (worker C's port design: <KEY>_GEOM with s_top, the end
    # face's distance along the axis) has no tilt
    geom = getattr(MS, f"{key}_GEOM", None)
    on_axis = bool(geom and "s_top" in geom) or v.get("seat") == "axis"
    return dict(centre=p.tolist(), dist_mm=float(np.linalg.norm(p)), elevation_deg=MS.elevation_deg(v["centre"]),
                window_tilt_deg=0.0 if on_axis else face_tilt, face_tilt_deg=face_tilt,
                seat="square to the line of sight (boss)" if on_axis else "on the wall's face",
                window=v.get("window") or getattr(MS, "WINDOW", None), slide=v.get("slide") or getattr(MS, "SLIDE", None))


def tilted_plate(t, tilt_deg, lam_um=0.81, na=0.03):
    """Plane-parallel plate in a converging beam (Smith, Modern Optical Engineering): focus shift along the axis, sagittal-
    tangential astigmatism, lateral (boresight) shift, blur ~ astigmatism x NA, and the double-bounce ghost's offset."""
    n = float(RT.n_glass("F_SILICA", lam_um))
    s = math.sin(math.radians(tilt_deg))
    c = math.cos(math.radians(tilt_deg))
    shift = t * (1 - c / math.sqrt(n * n - s * s)) / c if tilt_deg else t * (1 - 1 / n)
    astig = t * (n * n - 1) * s * s / (n * n - s * s) ** 1.5
    lateral = t * s * (1 - c / math.sqrt(n * n - s * s))
    th_g = math.asin(s / n)
    ghost_offset = 2 * t * math.tan(th_g) * c
    return dict(focus_shift_mm=shift, astigmatism_mm=astig, blur_um=astig * na * 1e3, boresight_shift_mm=lateral,
                ghost_offset_mm=ghost_offset, reflection_deviation_deg=2 * tilt_deg)


def camera_case(port, cam, lens, f_number, wd, lam_nm=850.0):
    d = PT.CAMS[cam]
    L = PT.LENSES[lens]
    f = L["f_mm"]
    m = f / (wd - f)
    px = d["px_um"] / m                                     # um on the object, across the view
    elev = port["elevation_deg"]
    along = px / math.sin(math.radians(elev))
    pupil = f / f_number
    na = pupil / 2 / wd
    lam = lam_nm * 1e-3
    airy_obj = 0.61 * lam / na                              # um, Rayleigh radius on the object
    blur_c = 2 * px * 1e-3                                  # 2-pixel blur circle on the object (mm)
    dof = 2 * blur_c * wd / pupil + lam * 1e-3 / na ** 2    # geometric (2-px blur) + diffraction, total
    roi = PT.ROI[cam]
    field_across = roi[0] * px * 1e-3
    field_along = roi[1] * along * 1e-3
    return dict(port=port["key"], camera=cam, lens=lens, f_number=f_number, wd_mm=wd, magnification=m,
                um_per_px_across=px, um_per_px_along_plate=along, rayleigh_um=airy_obj, diffraction_vs_2px=airy_obj / (2 * px),
                dof_mm=dof, focus_band_on_plate_mm=dof / math.cos(math.radians(elev)),
                lens_mod_ok=L["mod_mm"] <= wd, lens_mod_mm=L["mod_mm"], image_circle_mm=L["image_circle_mm"],
                sensor_diag_mm=d["diag_mm"], covers_full_sensor=L["image_circle_mm"] >= d["diag_mm"],
                roi_px=roi, roi_field_mm=(field_across, field_along), field_cm2_roi=field_across * field_along / 100)


def blur_table(px_um, exposures_us=(1, 2, 5, 10, 20, 41), speeds=(1, 5, 10, 20)):
    return {f"{v} m/s": {f"{t} us": v * t / px_um for t in exposures_us} for v in speeds}


def illumination(cam, f_number, m, lam_nm, t_us, target_e, rho=0.5, tau=0.8, in_band=1.0):
    """Irradiance on the plate (W/cm2) for target_e electrons in a pixel: Lambertian powder of reflectance rho, image
    irradiance E_i = rho E tau / (4 N^2 (1 + m)^2)."""
    d = PT.CAMS[cam]
    qe = float(np.interp(lam_nm, *zip(*d["qe"])))
    e_ph = H * C / (lam_nm * 1e-9)
    Ei = target_e * e_ph / (qe * (d["px_um"] * 1e-6) ** 2 * t_us * 1e-6)
    Es = Ei * 4 * f_number ** 2 * (1 + m) ** 2 / (rho * tau * in_band)
    return Es / 1e4


def laser_at_port(port, P=500.0, rho_d=0.7, lens_pupil_mm=12.5):
    """1070 nm at the viewport: a Lambertian return (reflectance rho_d, a bound: Al powder absorbs ~0.2-0.6 at 1 um) from the
    spot, and a specular-glint bound from a curved pool (reflectance 0.9 spread over a cone of +/-40 deg, i.e. surface slopes to
    20 deg). Irradiance at the window and power into a camera pupil of lens_pupil_mm."""
    d = port["dist_mm"] * 1e-3
    th_e = math.radians(90 - port["elevation_deg"])        # emission angle from the plate normal
    E_d = rho_d * P * math.cos(th_e) / (math.pi * d * d)    # W/m2
    a_pupil = math.pi * (lens_pupil_mm * 1e-3 / 2) ** 2
    a_win = math.pi * (port["clear_d"] * 1e-3 / 2) ** 2
    omega_cone = 2 * math.pi * (1 - math.cos(math.radians(40)))
    in_cone = math.degrees(th_e) <= 40
    E_s = (0.9 * P / omega_cone / (d * d)) if in_cone else 0.0
    return dict(port=port["key"], emission_angle_deg=math.degrees(th_e), diffuse_W_cm2=E_d / 1e4, diffuse_W_into_window=E_d * a_win,
                diffuse_W_into_pupil=E_d * a_pupil, glint_bound_W_cm2=E_s / 1e4, glint_bound_W_into_pupil=E_s * a_pupil,
                in_glint_cone=in_cone)


def main():
    R = dict(sources=dict(geometry="cad/monitoring_spec.py (read at run time)", parts="analysis/monitoring/optics/parts.py"), ports={},
             cameras=[], blur={}, illumination=[], laser=[])
    for key in MS.VIEWPORTS:
        g = port_geometry(key)
        g["key"] = key
        g["clear_d"] = MS.VIEWPORTS[key]["clear_d"]
        t_total = g["window"]["t"] + (g["slide"]["t"] if g["slide"] else 0.0)
        g["plates"] = tilted_plate(t_total, g["window_tilt_deg"], na=0.035)
        g["plates_if_window_normal_to_view"] = tilted_plate(t_total, 0.0, na=0.035)
        R["ports"][key] = g
    # lens front to plate centre: port centre to plate + the boss's end face along the axis (if the spec draws one) + standoff
    def boss(key):
        g = getattr(MS, f"{key}_GEOM", None)
        return float(g["s_top"]) if g and "s_top" in g else 0.0
    wd_lw = R["ports"]["LW"]["dist_mm"] + boss("LW") + MS.SIDE_CAMERA["standoff_mm"]
    wd_lp = R["ports"]["LP"]["dist_mm"] + boss("LP") + MS.LID_CAMERA.get("standoff_mm", 28.0)   # fits.json: 28 mm off the lid
    R["working_distance_mm"] = dict(LW=wd_lw, LP=wd_lp)
    for cam, lens, N, port, wd in PT.CAMERA_CASES(wd_lw, wd_lp):
        R["cameras"].append(camera_case(R["ports"][port], cam, lens, N, wd))
    for c in R["cameras"]:
        R["blur"][f"{c['camera']} + {c['lens']} at {c['port']}"] = blur_table(c["um_per_px_across"])
    for c in R["cameras"]:
        for lam, in_band, src in ((850.0, 1.0, "diode laser or LED behind a filter as wide as its spectrum"),
                                  (850.0, 0.3, "LED (~30-40 nm wide) behind a 10 nm filter")):
            for t in (10.0, 100.0):
                Es = illumination(c["camera"], c["f_number"], c["magnification"], lam, t, 0.5 * PT.CAMS[c["camera"]]["fwc_e"], in_band=in_band)
                R["illumination"].append(dict(case=f"{c['camera']} + {c['lens']} f/{c['f_number']} at {c['port']}", source=src, exposure_us=t,
                                              W_cm2_on_plate=Es, field_cm2=round(c["field_cm2_roi"], 2), roi=c["roi_px"]))
    # where the light comes from: power to put E (normal-incidence W/cm2) on the camera's field from a port at elevation e,
    # with a delivery efficiency eta (condenser + window + filter): P = E A / sin(e) / eta
    base = next(c for c in R["cameras"] if c["camera"].startswith("Chronos") and c["lens"].startswith("Kowa") and c["f_number"] == 4.0)
    for t_us in (10.0, 20.0, 2.0):
        for src, in_band, eta in (("pulsed 850 nm LED + FBH850-40 (in band ~0.8)", 0.8, 0.3), ("808 nm diode laser, fibre + collimator", 1.0, 0.6)):
            E = illumination(base["camera"], 4.0, base["magnification"], 850.0, t_us, 0.5 * PT.CAMS[base["camera"]]["fwc_e"], in_band=in_band)
            for key, how in (("LW", "through the camera's own port with a 50:50 cube (x 0.25 round trip)"), ("BW", "back-wall window, raking"),
                             ("LP", "steep lid port")):
                e = R["ports"][key]["elevation_deg"]
                extra = 4.0 if key == "LW" else 1.0
                R.setdefault("light_power", []).append(dict(exposure_us=t_us, source=src, port=key, how=how, elevation_deg=e,
                                                            W_needed=E * base["field_cm2_roi"] / math.sin(math.radians(e)) / eta * extra))
    for key in ("LW", "LP", "BW"):
        R["laser"].append(laser_at_port(R["ports"][key]))
    # every LP position the spec lists as a candidate: geometry, the IMX296 + 50 mm view, and the 1070 nm it receives
    R["lp_candidates"] = []
    v = MS.VIEWPORTS["LP"]
    for cen in v.get("candidates", [v["centre"]]):
        p = np.array(cen, float)
        ax = np.array(MS.axis_to_target(tuple(cen)))
        geom = getattr(MS, "LP_GEOM", None)
        on_axis = bool(geom and "s_top" in geom) or v.get("seat") == "axis"
        face_tilt = math.degrees(math.acos(abs(float(ax @ np.array(FACE_NORMAL[v["face"]])))))
        g = dict(key=f"LP at {tuple(round(c) for c in cen)}", centre=list(cen), dist_mm=float(np.linalg.norm(p)),
                 elevation_deg=MS.elevation_deg(tuple(cen)), clear_d=v["clear_d"], window=v.get("window"), slide=v.get("slide"))
        wd = g["dist_mm"] + boss("LP") + MS.LID_CAMERA.get("standoff_mm", 28.0)
        c = camera_case(dict(g, key="LP"), "IMX296 mono", "Kowa LM50JC10M 50 mm", 5.6, wd)
        lz = laser_at_port(g)
        t_total = (g["window"]["t"] if g["window"] else 0.0) + (g["slide"]["t"] if g["slide"] else 0.0)
        R["lp_candidates"].append(dict(centre=list(cen), is_spec_centre=list(cen) == list(v["centre"]), elevation_deg=g["elevation_deg"],
                                       dist_mm=g["dist_mm"], wd_mm=wd, um_per_px=(c["um_per_px_across"], c["um_per_px_along_plate"]),
                                       window_tilt_if_on_face_deg=face_tilt, astig_if_on_face_mm=tilted_plate(t_total, face_tilt, na=0.035)["astigmatism_mm"],
                                       seat_on_axis=on_axis, diffuse_W_cm2=lz["diffuse_W_cm2"], diffuse_W_into_pupil=lz["diffuse_W_into_pupil"],
                                       glint_bound_W_into_pupil=lz["glint_bound_W_into_pupil"]))
    R["layer_camera_port"] = laser_at_port(dict(key="layer camera (75, -45, 136)", dist_mm=float(np.linalg.norm([75, -45, 136])),
                                                elevation_deg=math.degrees(math.atan2(136, math.hypot(75, 45))), clear_d=20.0))
    (OUT / "viewports.json").write_text(json.dumps(R, indent=1, default=float) + "\n")
    write_md(R)
    return R


def write_md(R):
    L = ["# Viewport cameras, light and laser safety (generated by analysis/monitoring/optics/viewports.py)", ""]
    L += ["| port | centre (mm) | to plate centre (mm) | elevation | window seat | window tilt to the view (on the face) | window + slide | focus shift / astigmatism / blur at NA 0.035 | ghost offset |",
          "|---|---|---:|---:|---|---:|---|---|---:|"]
    for k, g in R["ports"].items():
        p = g["plates"]
        L.append(f"| {k} | {tuple(round(c) for c in g['centre'])} | {g['dist_mm']:.0f} | {g['elevation_deg']:.1f} deg | {g['seat']} | {g['window_tilt_deg']:.1f} deg ({g['face_tilt_deg']:.1f}) | "
                 f"{g['window']['d']} x {g['window']['t']} mm{(' + ' + str(g['slide']['t']) + ' mm') if g['slide'] else ''} | "
                 f"{p['focus_shift_mm']:.2f} / {p['astigmatism_mm']:.3f} mm / {p['blur_um']:.1f} um | {p['ghost_offset_mm']:.2f} mm |")
    lp = R["ports"]["LP"]
    L += ["", f"LP as in cad/monitoring_spec.py now: centre {tuple(round(c) for c in lp['centre'])}, {lp['elevation_deg']:.1f} deg; "
          f"working distances LW {R['working_distance_mm']['LW']:.0f} mm, LP {R['working_distance_mm']['LP']:.0f} mm. Every LP candidate the spec lists:", "",
          "| LP centre | elevation | to plate centre (mm) | WD (mm) | IMX296 + 50 mm: um/px across / along | window tilt if seated on the lid (astigmatism) | 1070 nm diffuse at the window (W/cm2) | into a 12.5 mm pupil (W) | glint bound into the pupil (W) |",
          "|---|---:|---:|---:|---|---|---:|---:|---:|"]
    for q in R.get("lp_candidates", []):
        L.append(f"| {tuple(round(c) for c in q['centre'])}{' (spec)' if q['is_spec_centre'] else ''} | {q['elevation_deg']:.1f} deg | {q['dist_mm']:.0f} | {q['wd_mm']:.0f} | "
                 f"{q['um_per_px'][0]:.1f} / {q['um_per_px'][1]:.1f} | {q['window_tilt_if_on_face_deg']:.0f} deg ({q['astig_if_on_face_mm']:.2f} mm){'; seated square on a boss' if q['seat_on_axis'] else ''} | "
                 f"{q['diffuse_W_cm2']:.2f} | {q['diffuse_W_into_pupil']:.2f} | {q['glint_bound_W_into_pupil']:.2f} |")
    L += ["", "| camera + lens | port | f/# | WD (mm) | m | um/px across / along the plate | Rayleigh (um) | DOF (mm) | lens focuses at this WD | lens covers the sensor |",
          "|---|---|---:|---:|---:|---|---:|---:|---|---|"]
    for c in R["cameras"]:
        L.append(f"| {c['camera']} + {c['lens']} | {c['port']} | {c['f_number']} | {c['wd_mm']:.0f} | {c['magnification']:.3f} | "
                 f"{c['um_per_px_across']:.1f} / {c['um_per_px_along_plate']:.0f} | {c['rayleigh_um']:.0f} | {c['dof_mm']:.2f} | "
                 f"{'yes' if c['lens_mod_ok'] else 'no (MOD %d mm): extension tube' % c['lens_mod_mm']} | {'yes' if c['covers_full_sensor'] else 'centre crop only'} |")
    L += ["", "## Motion blur (pixels) for spatter, across the view", ""]
    for k, b in R["blur"].items():
        cols = list(next(iter(b.values())).keys())
        L += [f"**{k}**", "", "| speed | " + " | ".join(cols) + " |", "|---|" + "---:|" * len(cols)]
        L += [f"| {v} | " + " | ".join(f"{x:.1f}" for x in row.values()) + " |" for v, row in b.items()]
        L.append("")
    L += ["## Light needed on the plate for half the full well (powder reflectance 0.5, optics 0.8)", "",
          "| case | source | exposure (us) | W/cm2 on the plate | field (cm2) | W in the field |", "|---|---|---:|---:|---:|---:|"]
    for r in R["illumination"]:
        fc = r["field_cm2"]
        L.append(f"| {r['case']} | {r['source']} | {r['exposure_us']:.0f} | {r['W_cm2_on_plate']:.3g} | {fc if fc else '-'} | {(r['W_cm2_on_plate'] * fc) if fc else float('nan'):.3g} |")
    L += ["", "## Source power for the Chronos + 50 mm f/4 at LW, 640 x 96 field, half full well", "",
          "| exposure (us) | source | from | elevation | W of light needed |", "|---:|---|---|---:|---:|"]
    for r in R.get("light_power", []):
        L.append(f"| {r['exposure_us']:.0f} | {r['source']} | {r['port']}: {r['how']} | {r['elevation_deg']:.1f} deg | {r['W_needed']:.2g} |")
    L += ["", "## 1070 nm at each viewport, 500 W", "",
          "| port | emission angle from the normal | diffuse at the window (W/cm2) | diffuse into the window (W) | diffuse into a 12.5 mm pupil (W) | glint bound into the pupil (W) |",
          "|---|---:|---:|---:|---:|---:|"]
    for r in R["laser"] + [R["layer_camera_port"]]:
        L.append(f"| {r['port']} | {r['emission_angle_deg']:.0f} deg | {r['diffuse_W_cm2']:.3g} | {r['diffuse_W_into_window']:.3g} | {r['diffuse_W_into_pupil']:.3g} | "
                 f"{r['glint_bound_W_into_pupil']:.3g}{'' if r['in_glint_cone'] else ' (outside the +/-40 deg cone)'} |")
    (OUT / "viewports.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
