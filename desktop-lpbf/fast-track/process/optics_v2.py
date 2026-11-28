"""Round 3 (2026-11-28): the optics chain re-checked on CAD v2, the current cad/ft_model.py (#260).

Round 2's optics.py ran on round 1's (v1) geometry, with its own copy of the heights (optics.CADP). Its changes went
into CAD v2: the lens axis 30 mm toward -Y, the window stack at (0, -11) in the box and (0, -21) in the cube, the
Ø44 cover-slide opening, and the cover slide hung 130 mm above the bed in the cube too. This script reads the v2
geometry from ft_model itself (P, levels() and the parts of build(state)) and re-runs, for FT-1 (box) and FT-1V (cube):

  1. clearance: the scanned beam (chief rays from the exit pupil on the lens axis, plus 2w of the beam itself) for the
     Ø30 build area and the Ø40 plate, k = 0.58-0.86, as a solid; its OpenCascade distance to every part near it
     (the MON camera and light parts included); the window's clear aperture and the lens's exit aperture analytically;
  2. scan angles per galvo against the head's and the lens's limits;
  3. back-reflection: the specular return from a flat plate, its displacement at the scan mirrors, the fraction that
     passes the mirrors' 25 mm aperture, the head's entrance aperture and the input turret (CAD v2's estimates), the
     power that could reach the fibre core; and where the return lands in the v2 scene (ray cast on its parts);
  4. footprint and irradiance on the cover slide and the window at v2's heights;
  5. thermal lens at v2's heights and stack centres: static r-z solve, and the steady and transient 2D solves while
     the first build's layer 1 scans (optics.py's solvers, unchanged);
  6. the lens's ghost foci against v2's mirror positions (P['head_in_z'], P['head_disp']).

Everything is compared with round 2's out/optics.json (v1). Nothing here has been checked on hardware.

Run: /tmp/tools/capmem 2 python desktop-lpbf/fast-track/process/optics_v2.py      (writes out/optics_v2.json; 11 min)
     /tmp/tools/capmem 2 python desktop-lpbf/fast-track/process/optics_v2.py --sight   (adds the camera and light
     sight lines from cad/ft_checks.py to the same file)
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import time

import numpy as np
from scipy.stats import ncx2

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "cad"))
import optics as O  # noqa: E402
import ft_model as M  # noqa: E402  (CadQuery: run under capmem)
import ft_vendor as VEN  # noqa: E402
import cadquery as cq  # noqa: E402

P = M.P
F = O.F
D_BEAM = P["beam_d"]                     # 5 mm collimated beam (1/e2)
STATES = {"box": "FT-1", "cube": "FT-1V"}
FIELDS = {"build area Ø30": 15.0, "plate Ø40": 20.0}
# The exit pupil's height sets k (chief-ray angle u = k theta). Round 2 took the LINOS recommended mirror distances
# (k 0.60-0.86). CAD v2 hangs the head so that its input axis (the Y mirror) is head_in_z = 43.5 mm above the lens's
# flange A, and the X mirror head_disp = 30.4 mm beyond it (estimates in ft_vendor.HS): see v2_pupil().
CLIP = 2.0                               # beam radius counted to 2w (0.03 % of the power outside)
EXCLUDE = ("Window, ", "Cover slide,", "Substrate", "Well block", "LINOS", "Powder", "Bench top")
APERTURE_PARTS = ("Cover-slide holder", "Cover-slide drop tube", "Inner clamp ring", "Box door", "Cube top plate",
                  "Window ring", "Window retaining flange", "Window-stack screws", "Beam tube centre section",
                  "Beam-tube lens collar")


def v2_pupil():
    """Mirror and pupil heights in CAD v2 against round 2's reading of the LINOS datasheet."""
    L = O.LINOS
    first_above_A = L["above_flange"] - (L["m2"] - L["m2_mech"])          # 16.0: first surface above flange A
    m2_v2 = P["head_in_z"] - first_above_A                                 # Y mirror before the first surface
    m1_v2 = m2_v2 + P["head_disp"]                                         # X mirror
    z_first = O.Z_FIRST                                                    # 360.8 above the focus (air)
    z_ep = z_first + (m2_v2 + m1_v2) / 2
    k_lo = 1 - (z_ep - L["WD"]) / F                                        # front principal plane at the lens bottom
    k_hi = 1 - (z_ep - z_first) / F                                        # ... at the first surface
    return dict(m2_before_first_surface_mm=m2_v2, m1_before_first_surface_mm=m1_v2, EP_above_focus_mm=z_ep,
                k_range=(k_lo, k_hi), v1=dict(m2=L["m2"], m1_head=L["m2"] + 29.88, m1_linos=L["m2"] + L["m1"],
                                               EP_above_focus_mm=O.Z_EP, k_range=O.K_RANGE),
                cad_pivot_above_bed_mm=P["pivot"], cad_k=F / (P["pivot"] - O.plates_focus_shift()))


def v2_stack(key):
    """Heights above the bed of the slide, window and lens in CAD v2, read from the built parts."""
    st = STATES[key]
    L = M.levels(st)
    dz = L["dz"]
    parts = M.build(st)
    bb = {p.name: p.shape.BoundingBox() for p in parts}
    w = next(b for n, b in bb.items() if n.startswith("Window, "))
    s = next(b for n, b in bb.items() if n.startswith("Cover slide,"))
    wc = ((w.xmin + w.xmax) / 2, (w.ymin + w.ymax) / 2)
    sc = ((s.xmin + s.xmax) / 2, (s.ymin + s.ymax) / 2)
    stk = dict(state=key, model=st, dz=dz, slide=(s.zmin - dz, s.zmax - dz), window=(w.zmin - dz, w.zmax - dz),
               lens_bot=L["lens_bot"] - dz, lens_flange=L["lens_top"] - dz, window_c=wc, slide_c=sc,
               roof_in=L["roof_in"] - dz, roof_out=L["roof_out"] - dz, apertures=[])
    return stk, parts


# ------------------------------------------------------------------------------------------------ 1. clearance
def env_at(stk, z, k, R, axis):
    """Centre (x, y) and radius of the scanned beam's envelope at real height z above the bed."""
    ha = O.air_height(stk, z)
    s = 1 - k * ha / F
    return (axis[0] * (1 - s), axis[1] * (1 - s)), R * s + CLIP * O.w_at(D_BEAM, ha), ha


def env_solid(stk, k, R, axis, z_top=None):
    z1 = (stk["lens_bot"] - 0.3) if z_top is None else z_top
    zs = set(np.round(np.linspace(0.3, 12.0, 7), 3)) | set(np.round(np.linspace(14.0, z1, 40), 3))
    zs |= {stk["slide"][0], stk["slide"][1], stk["window"][0], stk["window"][1]}
    wires = []
    for z in sorted(z for z in zs if 0.29 < z <= z1):
        (cx, cy), r, _ = env_at(stk, z, k, R, axis)
        wires.append(cq.Wire.makeCircle(r, cq.Vector(cx, cy, z + stk["dz"]), cq.Vector(0, 0, 1)))
    return cq.Solid.makeLoft(wires, True)


def clearances(stk, parts, env, pad=40.0):
    eb = env.BoundingBox()
    rows = []
    for p in parts:
        if p.name.startswith(EXCLUDE):
            continue
        b = p.shape.BoundingBox()
        if (b.xmin > eb.xmax + pad or b.xmax < eb.xmin - pad or b.ymin > eb.ymax + pad or b.ymax < eb.ymin - pad
                or b.zmin > eb.zmax + pad or b.zmax < eb.zmin - pad):
            continue
        try:
            d = float(env.distance(p.shape))
        except Exception:  # noqa: BLE001
            d = float("nan")
        hit = 0.0
        if d < 1e-6:
            try:
                hit = float(env.intersect(p.shape).Volume())
            except Exception:  # noqa: BLE001
                hit = float("nan")
        rows.append(dict(part=p.name, pid=p.pid, clearance_mm=round(d, 2), hit_mm3=round(hit, 2),
                         z_above_bed_mm=[round(b.zmin - stk["dz"], 1), round(b.zmax - stk["dz"], 1)]))
    rows.sort(key=lambda r: (r["clearance_mm"] if r["clearance_mm"] == r["clearance_mm"] else 1e9))
    return rows


def analytic_apertures(stk, k, R, axis):
    """Window clear aperture (Ø45.72, Edmund 38-990) at both faces; the lens's exit (the CAD's Ø70 bore, est.)."""
    out = {}
    wc = stk["window_c"]
    for face, z in (("window CA, lower face", stk["window"][0]), ("window CA, upper face", stk["window"][1])):
        (cx, cy), r, _ = env_at(stk, z, k, R, axis)
        out[face] = round(45.72 / 2 - (math.hypot(cx - wc[0], cy - wc[1]) + r), 2)
    (cx, cy), r, _ = env_at(stk, stk["lens_bot"], k, R, axis)
    out["lens exit (Ø70, CAD est.)"] = round(VEN.LINOS["nose_d"] / 2 - (math.hypot(cx - axis[0], cy - axis[1]) + r), 2)
    sc = stk["slide_c"]
    for face, z in (("cover slide (holder Ø44), lower face", stk["slide"][0]),):
        (cx, cy), r, _ = env_at(stk, z, k, R, axis)
        out[face] = round(P["cs_id"] / 2 - (math.hypot(cx - sc[0], cy - sc[1]) + r), 2)
    return out


# ------------------------------------------------------------------------------------------------ 2. scan angles
def scan_angles(axis, R):
    th = np.linspace(0, 2 * math.pi, 721)
    rr = np.linspace(0, R, 41)
    T, RR = np.meshgrid(th, rr)
    x, y = RR * np.cos(T) - axis[0], RR * np.sin(T) - axis[1]
    r = np.hypot(x, y)
    return dict(theta_x_max_rad=float(np.abs(x).max() / F), theta_y_max_rad=float(np.abs(y).max() / F),
                theta_y_min_rad=float(np.abs(y).min() / F), theta_r_max_rad=float(r.max() / F),
                r_min_mm=float(r.min()), r_max_mm=float(r.max()),
                mech_max_deg=float(math.degrees(r.max() / F / 2)),
                galvo1_limit_rad=O.HEAD["angle_galvo1"], galvo2_limit_rad=O.HEAD["angle_galvo2"],
                lens_limit_rad=math.radians(O.LINOS["scan_angle_deg"]),
                margin_vs_tighter_galvo_rad=float(O.HEAD["angle_galvo1"] - max(np.abs(x).max(), np.abs(y).max()) / F))


# ------------------------------------------------------------------------------------------------ 3. back-reflection
def frac_in_disc(delta, a, w):
    """Fraction of a Gaussian beam (1/e2 radius w) centred delta off a circular aperture's centre that passes it."""
    sig = w / 2.0
    return float(ncx2.cdf((a / sig) ** 2, 2, (delta / sig) ** 2))


def return_chain(r_rel, k, P_in=O.P_LASER):
    """Specular return from a flat plate at r_rel from the lens axis: displacement at the pupil, and the power left
    after the mirrors (25 mm aperture), the head's entrance aperture and the input turret (CAD v2 estimates), and
    the power into the fibre core (mode overlap exp(-(2 delta / D)^2))."""
    w = D_BEAM / 2
    delta = 2 * k * r_rel
    P0 = O.R_AL * O.T_ROUND * P_in
    f_mirror = frac_in_disc(delta, O.HEAD["aperture"] / 2, w)
    f_entr = frac_in_disc(delta, 9.0, w)          # ft_vendor.scanlab_hurryscan25: entrance aperture Ø18 (est.)
    f_turret = frac_in_disc(delta, 8.0, w)         # ft_vendor.hurryscan_input_stack: turret bore Ø16 (est.)
    eta = math.exp(-(2 * delta / D_BEAM) ** 2)
    return dict(r_rel_mm=r_rel, k=k, delta_mm=delta, returned_W=P0,
                miss_mirror_edge_mm=delta - O.HEAD["aperture"] / 2 - CLIP * w,
                miss_entrance_edge_mm=delta - 9.0 - CLIP * w, miss_turret_edge_mm=delta - 8.0 - CLIP * w,
                W_on_mirrors=P0 * f_mirror, W_past_entrance=P0 * min(f_mirror, f_entr),
                W_past_turret=P0 * min(f_mirror, f_entr, f_turret), W_core=P0 * eta,
                angle_at_fibre_x_divergence=2 * delta / D_BEAM)


def specular_landing(stk, parts, k, axis, R=20.0, n_r=10, n_t=72):
    """Ray-cast the specular return's chief ray from plate points (flat plate at focus) through the v2 scene: which
    part it meets first, or whether it re-enters the lens inside its exit aperture. Shares of the plate's area
    (n_r rings of n_t points, each weighted by its radius)."""
    import trimesh
    meshes, names = [], []
    for p in parts:
        if p.name.startswith(("Window, ", "Cover slide,", "Substrate", "Well block", "Bench top", "Powder")):
            continue
        b = p.shape.BoundingBox()
        if b.zmax - stk["dz"] < 1.0 or b.zmin - stk["dz"] > stk["lens_bot"] + 80:
            continue
        if min(abs(b.xmin), abs(b.xmax), abs(b.xmin + b.xmax) / 2) > 400:
            continue
        vs, fs = p.shape.tessellate(0.5, 0.3)
        if not fs:
            continue
        m = trimesh.Trimesh(vertices=[(v.x, v.y, v.z) for v in vs], faces=[tuple(f) for f in fs], process=False)
        meshes.append(m)
        names.append(p.name)
    scene = trimesh.util.concatenate(meshes)
    owner = np.concatenate([np.full(len(m.faces), i) for i, m in enumerate(meshes)])
    pts, wts = [(0.0, 0.0)], [R / n_r / 8.0]
    for i in range(1, n_r + 1):
        rr = R * (i - 0.5) / n_r
        for j in range(n_t):
            a_ = 2 * math.pi * (j + 0.5 * (i % 2)) / n_t
            pts.append((rr * math.cos(a_), rr * math.sin(a_)))
            wts.append(rr)
    pts, wts = np.array(pts), np.array(wts)
    zp = F / k + O.plates_focus_shift()           # exit pupil, real height (est.)
    o = np.c_[pts, np.full(len(pts), stk["dz"] + 0.05)]
    d_in = o - np.array([axis[0], axis[1], stk["dz"] + zp])     # incoming chief ray direction (down, outward)
    d_out = d_in * np.array([1, 1, -1])
    d_out /= np.linalg.norm(d_out, axis=1)[:, None]
    locs, idx, tri = scene.ray.intersects_location(o, d_out, multiple_hits=False)
    res = {}
    first = {}
    for loc, i, t in zip(locs, idx, tri):
        first[int(i)] = (names[owner[t]], loc)
    for i in range(len(pts)):
        nm, loc = first.get(i, ("nothing (escapes)", None))
        if nm.startswith("LINOS") and loc is not None:
            nm = ("LINOS lens, inside its Ø70 exit (back toward the head)"
                  if math.hypot(loc[0] - axis[0], loc[1] - axis[1]) <= VEN.LINOS["nose_d"] / 2 else "LINOS lens barrel")
        res[nm] = res.get(nm, 0.0) + wts[i]
    return {k_: round(100.0 * v / wts.sum(), 1) for k_, v in sorted(res.items(), key=lambda kv: -kv[1])}


# ------------------------------------------------------------------------------------------------ 6. ghosts
def lens_ghosts(m2, m1):
    out = []
    for g in O.LINOS["ghosts_from_first_surface"]:
        for mname, x in (("M2 (Y)", m2), ("M1 (X)", m1)):
            dmm = max(D_BEAM * abs(g - x) / g, 2 * O.LAM * g / (math.pi * 2.5) * 2)
            out.append(dict(ghost_mm=g, mirror=mname, mirror_mm=round(x, 2), gap_mm=round(g - x, 2),
                            spot_d_mm=round(dmm, 3), W_cm2_per_W=round(1.0 / (math.pi * (dmm / 20) ** 2), 1)))
    return out


# ------------------------------------------------------------------------------------------------ main
def main():
    t0 = time.time()
    OUT.mkdir(exist_ok=True)
    v1 = json.loads((OUT / "optics.json").read_text())
    axis = tuple(P["axis_off"])
    pup = v2_pupil()
    k_lo = min(pup["k_range"][0], O.K_RANGE[0])
    k_hi = max(pup["k_range"][1], O.K_RANGE[1])
    KS = (round(k_lo, 2), round(pup["cad_k"], 2), round(k_hi, 2))
    res = dict(model="cad/ft_model.py (CAD v2)", axis=axis, window_c=P["win_c"], cover_slide_c=P["cs_c"],
               cover_slide_z=P["cs_z"], cs_id=P["cs_id"], lens_wd=P["lens_wd"], pupil=pup, k_values=KS, stacks={},
               clearance={}, analytic={}, specular_landing={})
    stacks, allparts = {}, {}
    for key in STATES:
        stk, parts = v2_stack(key)
        stacks[key], allparts[key] = stk, parts
        res["stacks"][key] = {k_: v for k_, v in stk.items() if k_ != "apertures"}
        print(f"{key}: slide {stk['slide']}, window {stk['window']}, lens bottom {stk['lens_bot']:.2f} "
              f"({time.time() - t0:.0f} s)", flush=True)
    # 1. clearance (cached in /tmp so that a failure later on doesn't cost the 9 minutes again)
    cache = pathlib.Path("/tmp/r3-process/optics_v2_clearance.json")
    if "--resume" in sys.argv and cache.exists():
        c_ = json.loads(cache.read_text())
        res["clearance"], res["analytic"] = c_["clearance"], c_["analytic"]
    else:
        for key, stk in stacks.items():
            for fname, R in FIELDS.items():
                for k in KS:
                    env = env_solid(stk, k, R, axis)
                    rows = clearances(stk, allparts[key], env)
                    tag = f"{STATES[key]}, {fname}, k {k}"
                    res["clearance"][tag] = rows
                    res["analytic"][tag] = analytic_apertures(stk, k, R, axis)
                    near = ", ".join(f"{r['part'][:38]} {r['clearance_mm']}" for r in rows[:4])
                    print(f"{tag}: {near} | {res['analytic'][tag]} ({time.time() - t0:.0f} s)", flush=True)
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(dict(clearance=res["clearance"], analytic=res["analytic"])))
    # 2. scan angles
    res["scan_angles"] = {fname: scan_angles(axis, R) for fname, R in FIELDS.items()}
    # 3. back-reflection
    res["return_chain"] = {fname: [return_chain(abs(axis[1]) - R, k) for k in KS] for fname, R in FIELDS.items()}
    for key, stk in stacks.items():
        for k in (KS[0], KS[2]):
            res["specular_landing"][f"{STATES[key]}, k {k}"] = specular_landing(stk, allparts[key], k, axis)
            print(STATES[key], k, res["specular_landing"][f"{STATES[key]}, k {k}"], flush=True)
    # 4. irradiance
    res["irradiance"] = {key: O.surface_irradiance(stk, D_BEAM) for key, stk in stacks.items()}
    # 5. thermal lens: optics.py's solvers on the v2 stacks
    O.STACKS = {k_: dict(v, apertures=[]) for k_, v in stacks.items()}
    res["thermal_static"] = O.thermal_lens(D_BEAM)
    npz = OUT / "build_first_coupons_15mm.npz"
    res["thermal_transient"] = []
    for key, stk in stacks.items():
        for el, a_ref, cases in (("slide", 0.01, (20e-6 * 0.1 + 1e-3, 0.01, 0.02)),
                                 ("window", 20e-6 * 0.953 + 1e-3, (20e-6 * 0.953 + 1e-3,))):
            cen = stk["slide_c"] if el == "slide" else stk["window_c"]
            O.STACK_Y = {key: cen[1]}
            r = O.transient_lens(stk, el, a_ref, npz)
            for a_tot in cases:
                f = a_tot / a_ref
                res["thermal_transient"].append(dict(
                    state=key, element=el, a_tot=a_tot, centre=cen, period_s=r["period_s"],
                    steady_dz_mm=[x * f for x in r["steady_dz_mm"]], mean_dz_mm=r["transient_dz_mm"]["mean"] * f,
                    max_dz_mm=r["transient_dz_mm"]["max"] * f, max_x_zR=r["x_zR_max"] * f, T_max_K=r["T_max_K"] * f))
            print(f"transient {key} {el} ({time.time() - t0:.0f} s)", flush=True)
    # 6. ghosts
    res["lens_ghosts_v2"] = lens_ghosts(pup["m2_before_first_surface_mm"], pup["m1_before_first_surface_mm"])
    res["lens_ghosts_v1"] = lens_ghosts(O.LINOS["m2"], O.LINOS["m2"] + 29.88)
    # v1 numbers for the comparison
    res["v1"] = dict(stacks={k_: dict(slide=v["slide"], window=v["window"], lens_bot=v["lens_bot"])
                             for k_, v in v1["stacks"].items()},
                     irradiance=v1["irradiance"], thermal_static=v1["thermal_static"],
                     thermal_transient=v1["thermal_transient"])
    res["run_s"] = round(time.time() - t0, 1)
    (OUT / "optics_v2.json").write_text(json.dumps(res, indent=1, default=float))
    print(f"done in {time.time() - t0:.0f} s")
    return res


def landing():
    """Re-run only the specular-return ray cast and write it into optics_v2.json."""
    path = OUT / "optics_v2.json"
    res = json.loads(path.read_text())
    axis = tuple(P["axis_off"])
    KS = res["k_values"]
    res["specular_landing"] = {}
    for key in STATES:
        stk, parts = v2_stack(key)
        for k in (KS[0], KS[2]):
            res["specular_landing"][f"{STATES[key]}, k {k}"] = specular_landing(stk, parts, k, axis)
            print(STATES[key], k, res["specular_landing"][f"{STATES[key]}, k {k}"], flush=True)
    path.write_text(json.dumps(res, indent=1, default=float))


def sight():
    """The layer camera's and the raking lights' view of the plate in v2 (cad/ft_checks.sight_lines: rays from 157
    points of the Ø38 plate to the camera pupil and to each light, hopper at either park), added to optics_v2.json."""
    import ft_checks as CH
    path = OUT / "optics_v2.json"
    res = json.loads(path.read_text())
    res["sight_lines"] = {st: CH.sight_lines(st) for st in ("FT-1", "FT-1V")}
    res["camera"] = {st: CH.camera_numbers(st) for st in ("FT-1", "FT-1V")}
    path.write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps(res["sight_lines"], indent=1))


if __name__ == "__main__":
    if "--landing" in sys.argv:
        landing()
    elif "--sight" in sys.argv:
        sight()
    else:
        main()
