"""Meshes of the bought parts, at the sizes their vendors publish, for render_build.py.

Every number used to draw a part is in DIMS, with where it came from. parts-check.md lists what
each vendor page or datasheet says and what it changes. Units: mm. Each part is drawn in its own
frame: axis along +z, bottom (or the end that goes in first) at z 0, unless the docstring says
otherwise.
"""

from __future__ import annotations

import math

import numpy as np
import pyvista as pv

IN = 25.4

# ----------------------------------------------------------------------------------------- sizes
# "src" says where each number comes from. See parts-check.md for the quotes and links.
DIMS = {
    # The O-Ring Store, FDA brown Viton 75 (AS568 sizes; ID x cross-section)
    "oring_006": dict(id=2.90, cs=1.78, src="AS568-006, The O-Ring Store FDABV75006"),
    "oring_008": dict(id=4.47, cs=1.78, src="AS568-008, The O-Ring Store FDABV75008"),
    "oring_010": dict(id=6.07, cs=1.78, src="AS568-010, The O-Ring Store FDABV75010"),
    "oring_013": dict(id=10.82, cs=1.78, src="AS568-013, The O-Ring Store FDABV75013"),
    # Same Sky CPG-37-TH-TR (the cap's two low-force pins). Filled from the datasheet.
    # z from the flange's underside (the board face): tail below, barrel and plunger above.
    "cpg37": dict(free_h=2.20, work_h=1.50, min_h=1.30, stroke=0.9, tail_d=1.50, tail_l=1.10, flange_d=2.00, flange_t=0.20,
                  barrel_d=1.25, barrel_top=1.10, plunger_d=0.80, hole_d=1.60, force_gf=30,
                  src="Same Sky CPG-37-TH-TR datasheet drawing"),
    # Adafruit 2430, P75-B1 needle-head pogo pin (the tray's 12 pins and the bench cell's one)
    # Adafruit: body 1.0, tip 0.7, 16 mm free, 13 mm compressed. Barrel length not published: drawn 12.6.
    "p75": dict(length=16.0, barrel_d=1.0, barrel_l=12.6, plunger_d=0.7, needle_l=1.2, stroke=3.0,
                src="Adafruit 2430 page (barrel length assumed)"),
    # totalElement 4 x 2 mm N52
    "magnet": dict(d=4.0, h=2.0, tol=0.10, src="totalElement D4X2MMN52: 4.00 x 2.00 +/-0.10, Ni-Cu-Ni"),
    # McMaster 91292A112 M3 x 0.5 x 8 mm, 18-8 socket head
    "m3x8": dict(head_d=5.5, head_h=3.0, hex=2.5, length=8.0, d=3.0, pitch=0.5, src="ISO 4762 / McMaster 91292A112"),
    # ruthex RX-M3x5.7 heat-set insert (on hand from ME order 13518)
    "insert_m3": dict(od=4.6, length=5.7, id=3.0, src="ruthex RX-M3x5.7"),
    # rods and wire
    "brass_rod": dict(d=1 / 16 * IN, length=12 * IN, count=3, src="K&S 8162, 1/16 x 12 in, 3 pack"),
    "drill_rod": dict(d=3.0, length=36 * IN, src="McMaster 88625K62, O1, 3 mm +/-0.013 x 3 ft, annealed"),
    "ptfe_rod": dict(d=0.75 * IN, length=12 * IN, src="McMaster 8546K15, 3/4 in +0.000/+0.005 in, sold by the foot"),
    "graphite_rod": dict(d=10.0, length=100.0, count=2, src="ChemicalStore GR4BAR10X100"),
    "pt_wire": dict(d=0.25, length=200.0, src="Advent PT543404: 99.95 %, hard temper"),
    # references
    # Ossila drawing: glass 6 x 80, assembled 72 below the cap + 25 cap + 15 pin. Cap and pin diameters not given.
    "ossila_ref": dict(d=6.0, length=72.0, glass_l=80.0, cap_d=10.0, cap_l=25.0, pin_d=2.0, pin_l=15.0, frit_l=3.0,
                       wire_d=0.25, wire_l=58.5, src="Ossila C2015B1 drawing"),
    "lf2": dict(d=2.0, length=16.6, pin_d=1.0, pin_l=1.3, stock_length=63.0, src="Innovative Instruments LF-2"),
    # wiring
    "foil_1181": dict(width=0.25 * IN, thick=0.066, foil=0.036, length=16.5e3, core_id=76.2, core_wall=3.0,
                      src="3M 1181 datasheet (core size not published: drawn on a 3 in core)"),
    "wirewrap": dict(od=0.5, length=200e3, spool_d=54.0, spool_w=30.0, hub_d=30.0, color="#2d6cdf",
                     src="Adafruit 1446 (only '30 AWG, 200 m' is published: OD and spool drawn as typical)"),
    "silicone26": dict(od=1.5, length=25 * 304.8, color="#202020", src="Adafruit 2517: OD 1.5 +/-0.1"),
    "belden9534": dict(od=4.674, length=3 * 304.8, jacket="#8f9296", src="Belden 9534 datasheet: OD 4.674, Al foil + drain"),
    # dummy cell
    "res_mfp25": dict(body_d=2.4, body_l=6.3, lead_d=0.65, lead_l=28.0, src="Yageo MFP datasheet"),
    "cap_ecqe": dict(w=12.0, h=14.0, t=6.7, pitch=10.0, lead_d=0.6, lead_l=20.0, src="Panasonic ECQ-E datasheet (max sizes)"),
    # on hand
    "steel_disc": dict(d=25.4, t=1.0, src="totalElement SP13M"),
    "jst_xh4": dict(w=12.4, d=5.75, h=7.0, pitch=2.5, src="JST XH, 4 way"),
    "voa_vial": dict(d=27.5, h=57.0, src="Fisher 12-100-112 20 mL VOA"),
    "tube_05": dict(d=7.8, length=30.0, rim_d=10.0, src="Eppendorf 0.5 mL Safe-Lock: 7.8 below the rim, 30 long"),
    # CHEMets K-9510: 30 ampoules (one kind for both ranges), activator (~9 mL, 3 drops), 25 mL cup, C-9501 round
    # comparator (0-1 ppm) and C-9510 flat comparator (1-10 ppm). No sizes are published: drawn as typical.
    "chemets": dict(ampoule_d=8.0, ampoule_l=68.0, tip_l=12.0, cup_d=40.0, cup_h=48.0, cup_ml=25.0, drops=3, wait_min=5,
                    box=(160.0, 110.0, 60.0), src="CHEMetrics K-9510 instructions (sizes not published)"),
    "ezstat": dict(box=(150.0, 120.0, 55.0), src="NuVant EZstat-Pro (size not published; drawn schematic)"),
}


# ----------------------------------------------------------------------------------------- helpers
def fin(m: pv.PolyData, angle=35.0) -> pv.PolyData:
    m = m.triangulate().clean()
    if not m.n_points:
        return m
    closed = m.n_open_edges == 0
    return m.compute_normals(auto_orient_normals=closed, split_vertices=True, feature_angle=angle)


def revolve(profile_rz, res=48, angle=360.0) -> pv.PolyData:
    """Revolve a closed (r, z) polyline about z."""
    pts = np.array([[max(r, 0.0), 0.0, z] for r, z in profile_rz], float)
    poly = pv.PolyData(pts, faces=np.hstack([[len(pts)], np.arange(len(pts))]))
    m = poly.extrude_rotate(resolution=res, angle=angle, capping=angle < 360, rotation_axis=(0, 0, 1))
    return fin(m, 40)


def cyl(r, z0, z1, x=0.0, y=0.0, res=48) -> pv.PolyData:
    return fin(pv.Cylinder(center=(x, y, (z0 + z1) / 2), direction=(0, 0, 1), radius=r, height=z1 - z0,
                           resolution=res, capping=True), 40)


def rod_x(d, x0, x1, y=0.0, z=None, res=40) -> pv.PolyData:
    z = d / 2 if z is None else z
    return fin(pv.Cylinder(center=((x0 + x1) / 2, y, z), direction=(1, 0, 0), radius=d / 2, height=x1 - x0,
                           resolution=res, capping=True), 40)


def box(x0, y0, z0, x1, y1, z1) -> pv.PolyData:
    """An axis-aligned box with outward-wound faces and flat normals."""
    v = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0], [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], float)
    quads = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    faces = np.hstack([[4, *q] for q in quads])
    m = pv.PolyData(v, faces).triangulate()
    return m.compute_normals(auto_orient_normals=False, consistent_normals=False, split_vertices=True, feature_angle=30)


def torus(R, r, z=0.0, ures=72, vres=24) -> pv.PolyData:
    t = pv.ParametricTorus(ringradius=R, crosssectionradius=r, u_res=ures, v_res=vres, w_res=4)
    return fin(t.translate((0, 0, z), inplace=False), 80)


def tube_path(points, r, n_sides=14) -> pv.PolyData:
    line = pv.lines_from_points(np.asarray(points, float))
    return fin(line.tube(radius=r, n_sides=n_sides, capping=True), 80)


def helix(R, pitch, turns, z0=0.0, n=None, phase=0.0):
    n = n or max(16, int(turns * 64))
    a = np.linspace(0, 2 * math.pi * turns, n) + phase
    return np.c_[R * np.cos(a), R * np.sin(a), z0 + pitch * a / (2 * math.pi)]


def spiral(r0, r1, turns, z=0.0, n=None):
    n = n or max(32, int(turns * 72))
    a = np.linspace(0, 2 * math.pi * turns, n)
    r = np.linspace(r0, r1, n)
    return np.c_[r * np.cos(a), r * np.sin(a), np.full(n, z)]


# ----------------------------------------------------------------------------------------- parts
def oring(size: str) -> pv.PolyData:
    """Free (unsqueezed) AS568 ring lying flat, bottom at z 0."""
    d = DIMS[f"oring_{size}"]
    return torus((d["id"] + d["cs"]) / 2, d["cs"] / 2, z=d["cs"] / 2)


def oring_od(size: str) -> float:
    d = DIMS[f"oring_{size}"]
    return d["id"] + 2 * d["cs"]


def cpg37() -> dict:
    """Same Sky CPG-37-TH-TR, free (2.20 mm high). z 0 at the flange's underside (the board face): the tail goes
    down into a 1.60 mm hole, the barrel and plunger stand up. Returns {"barrel" (with tail and flange), "plunger"}."""
    d = DIMS["cpg37"]
    b = [(0, -d["tail_l"]), (d["tail_d"] / 2 - 0.08, -d["tail_l"]), (d["tail_d"] / 2, -d["tail_l"] + 0.08), (d["tail_d"] / 2, 0),
         (d["flange_d"] / 2, 0), (d["flange_d"] / 2, d["flange_t"]), (d["barrel_d"] / 2, d["flange_t"]),
         (d["barrel_d"] / 2, d["barrel_top"]), (0, d["barrel_top"])]
    top = d["free_h"]
    p = [(0, d["barrel_top"] - 0.3), (d["plunger_d"] / 2, d["barrel_top"] - 0.3), (d["plunger_d"] / 2, top - d["plunger_d"] / 2 * 0.8),
         (d["plunger_d"] / 2 * 0.75, top - 0.1), (0, top)]
    return {"barrel": revolve(b, 32), "plunger": revolve(p, 32)}


def p75() -> dict:
    """Adafruit P75-B1, free. z 0 at the barrel's bottom; needle up."""
    d = DIMS["p75"]
    bl = d["barrel_l"]
    b = [(0, 0), (d["barrel_d"] / 2 * 0.85, 0), (d["barrel_d"] / 2, 0.3), (d["barrel_d"] / 2, bl), (0, bl)]
    tip0 = d["length"] - d["needle_l"]
    p = [(0, bl - 1.0), (d["plunger_d"] / 2, bl - 1.0), (d["plunger_d"] / 2, tip0), (0.04, d["length"]), (0, d["length"])]
    return {"barrel": revolve(b, 32), "plunger": revolve(p, 32)}


def magnet() -> pv.PolyData:
    d = DIMS["magnet"]
    return cyl(d["d"] / 2, 0, d["h"], res=40)


def shcs_m3x8() -> dict:
    """Socket head cap screw, head up: underside of the head at z 0, shank down to z -8."""
    d = DIMS["m3x8"]
    head = revolve([(0, 0), (d["head_d"] / 2 - 0.2, 0), (d["head_d"] / 2, 0.2), (d["head_d"] / 2, d["head_h"] - 0.3),
                    (d["head_d"] / 2 - 0.3, d["head_h"]), (0, d["head_h"])], 48)
    teeth, z = [], 0.0
    rmaj, rmin = d["d"] / 2, d["d"] / 2 - 0.31
    prof = [(0, 0.0)]
    n = int(d["length"] / d["pitch"])
    for k in range(n):
        z0 = -k * d["pitch"]
        prof += [(rmaj, z0 - 0.1), (rmin, z0 - d["pitch"] / 2), (rmaj, z0 - d["pitch"] + 0.05)]
    prof += [(rmin, -d["length"]), (0, -d["length"])]
    shank = revolve(prof, 32)
    hexr = d["hex"] / math.sqrt(3)
    hx = pv.Polygon(center=(0, 0, d["head_h"] + 0.02), radius=hexr, n_sides=6)
    return {"head": head, "shank": shank, "socket": fin(hx)}


def heat_set_insert() -> pv.PolyData:
    d = DIMS["insert_m3"]
    r_o, r_i, L = d["od"] / 2, d["id"] / 2, d["length"]
    prof = [(r_i, 0)]
    k = 0
    z = 0.0
    while z < L - 0.6:
        prof += [(r_o - 0.25, z + 0.05), (r_o, z + 0.35), (r_o - 0.25, z + 0.65)]
        z += 0.7
        k += 1
    prof += [(r_o - 0.3, L), (r_i, L)]
    return revolve(prof, 36)


def rod(key: str, x0=0.0, y=0.0) -> pv.PolyData:
    d = DIMS[key]
    return rod_x(d["d"], x0, x0 + d["length"], y)


def pt_wire_coil(turns=3.0) -> pv.PolyData:
    """0.2 m of 0.25 mm wire as supplied: a loose coil lying flat."""
    d = DIMS["pt_wire"]
    R = d["length"] / (2 * math.pi * turns)
    pts = helix(R, 0.35, turns, z0=d["d"] / 2, n=600)
    return tube_path(pts, d["d"] / 2, 10)


def ossila_ref() -> dict:
    """Glass body down (frit at z 0), cap and pin up. The glass shows 72 mm below the 25 mm cap."""
    d = DIMS["ossila_ref"]
    L, r = d["length"], d["d"] / 2
    glass = revolve([(r - 0.6, d["frit_l"]), (r, d["frit_l"]), (r, L), (r - 0.6, L)], 48)
    frit = cyl(r - 0.35, 0, d["frit_l"] + 0.3, res=32)
    fill = cyl(r - 0.65, d["frit_l"] + 0.3, L * 0.8, res=32)
    wire = cyl(d["wire_d"] / 2 + 0.05, L + d["cap_l"] - d["wire_l"] - 4, L + 4, res=12)
    agcl = cyl(0.3, L + d["cap_l"] - d["wire_l"] - 4, L + d["cap_l"] - d["wire_l"] + 14, res=12)
    cap = cyl(d["cap_d"] / 2, L, L + d["cap_l"], res=40)
    pin = cyl(d["pin_d"] / 2, L + d["cap_l"], L + d["cap_l"] + d["pin_l"], res=20)
    return {"glass": glass, "frit": frit, "fill": fill, "wire": wire, "agcl": agcl, "cap": cap, "pin": pin}


def lf2_ref(length=None) -> dict:
    """Leak-free reference, tip at z 0, contact up."""
    d = DIMS["lf2"]
    L = length or d["length"]
    body = revolve([(0, 0.25), (0.6, 0), (d["d"] / 2, 0.4), (d["d"] / 2, L - d["pin_l"]), (0, L - d["pin_l"])], 32)
    tip = cyl(0.55, -0.02, 0.3, res=20)
    pin = cyl(d["pin_d"] / 2, L - d["pin_l"], L, res=16)
    return {"body": body, "tip": tip, "pin": pin}


def foil_roll() -> dict:
    """3M 1181 1/4 in roll on its core, lying flat."""
    d = DIMS["foil_1181"]
    r_core = d["core_id"] / 2
    r_c2 = r_core + d["core_wall"]
    r_out = math.sqrt(r_c2 ** 2 + d["length"] * d["thick"] / math.pi)
    w = d["width"]
    core = revolve([(r_core, 0), (r_c2, 0), (r_c2, w), (r_core, w)], 72)
    foil = revolve([(r_c2, 0), (r_out, 0), (r_out, w), (r_c2, w)], 72)
    return {"core": core, "foil": foil, "r_out": r_out}


def wire_spool() -> dict:
    d = DIMS["wirewrap"]
    R, w, h = d["spool_d"] / 2, d["spool_w"], d["hub_d"] / 2
    fl = 1.5
    spool = revolve([(4, 0), (R, 0), (R, fl), (h, fl), (h, w - fl), (R, w - fl), (R, w), (4, w)], 64)
    wire = revolve([(h, fl), (R - 3, fl), (R - 3, w - fl), (h, w - fl)], 64)
    return {"spool": spool, "wire": wire}


def wire_coil(key: str, R=None, turns=None, z0=0.0) -> pv.PolyData:
    d = DIMS[key]
    if R is None:
        R = 45.0
    turns = d["length"] / (2 * math.pi * R) if turns is None else turns
    turns_shown = min(turns, 7.0)
    pts = helix(R, d["od"] * 1.05, turns_shown, z0=z0 + d["od"] / 2, n=int(turns_shown * 90))
    return tube_path(pts, d["od"] / 2, 14)


def belden_coil(R=None) -> dict:
    d = DIMS["belden9534"]
    turns = 3.0
    R = R or d["length"] / (2 * math.pi * turns)
    pts = helix(R, d["od"] * 1.05, turns - 0.08, z0=d["od"] / 2, n=320)
    jacket = tube_path(pts, d["od"] / 2, 20)
    end = pts[-1]
    tang = pts[-1] - pts[-2]
    tang /= np.linalg.norm(tang)
    cols = ["#d23a2f", "#1f1f1f", "#2e6fdb", "#f2f2f2"]
    cond = []
    side = np.cross(tang, [0, 0, 1.0])
    for k, c in enumerate(cols):
        off = (k - 1.5) * 0.9 * side
        p0 = end + off
        cond.append((tube_path([p0, p0 + tang * 9 + off * 0.8], 0.42, 10), c))
    drain = tube_path([end, end + tang * 8 + np.array([0, 0, 1.2])], 0.25, 8)
    return {"jacket": jacket, "conductors": cond, "drain": drain, "R": R}


def resistor() -> dict:
    """Axial, lying along x, centre at the origin, leads bent down."""
    d = DIMS["res_mfp25"]
    L, r = d["body_l"], d["body_d"] / 2
    body = fin(pv.Cylinder(center=(0, 0, r), direction=(1, 0, 0), radius=r, height=L, resolution=32), 40)
    bands = []
    for k, (x, c) in enumerate(zip([-2.0, -1.2, -0.4, 0.4, 1.6, 2.4], ["#7a4a1c", "#111111", "#111111", "#d23a2f", "#7a4a1c", "#7d3fa8"])):
        bands.append((fin(pv.Cylinder(center=(x, 0, r), direction=(1, 0, 0), radius=r * 1.04, height=0.32, resolution=32)), c))
    leads = [tube_path([(s * L / 2, 0, r), (s * (L / 2 + 3), 0, r), (s * (L / 2 + 3.5), 0, r - 0.6),
                        (s * (L / 2 + 3.5), 0, -d["lead_l"] / 2)], d["lead_d"] / 2, 10) for s in (-1, 1)]
    return {"body": body, "bands": bands, "leads": leads}


def film_cap() -> dict:
    """Radial box capacitor, standing on its leads; body bottom at z 0."""
    d = DIMS["cap_ecqe"]
    w, t, h = d["w"], d["t"], d["h"]
    body = fin(pv.Box(bounds=(-w / 2, w / 2, -t / 2, t / 2, 0, h)), 30)
    leads = [tube_path([(s * d["pitch"] / 2, 0, 0.5), (s * d["pitch"] / 2, 0, -d["lead_l"])], d["lead_d"] / 2, 10)
             for s in (-1, 1)]
    return {"body": body, "leads": leads}


def jst_xh4() -> dict:
    d = DIMS["jst_xh4"]
    w, dd, h = d["w"], d["d"], d["h"]
    housing = box(-w / 2, -dd / 2, 0, w / 2, dd / 2, h)
    pins = [box(-1.5 * d["pitch"] + k * d["pitch"] - 0.32, -0.32, h - 0.5, -1.5 * d["pitch"] + k * d["pitch"] + 0.32, 0.32, h + 3.4)
            for k in range(4)]
    plug = box(-w / 2 + 0.3, -dd / 2 + 0.3, h + 3.6, w / 2 - 0.3, dd / 2 - 0.3, h + 3.6 + 6.0)
    return {"housing": housing, "pins": pins, "plug": plug}


def steel_disc() -> pv.PolyData:
    d = DIMS["steel_disc"]
    return cyl(d["d"] / 2, 0, d["t"], res=64)


def voa_vial(with_liquid=None) -> dict:
    d = DIMS["voa_vial"]
    r, h = d["d"] / 2, d["h"]
    glass = revolve([(0, 0), (r - 1, 0), (r, 1.2), (r, h - 8), (r - 2.2, h - 6), (r - 2.2, h), (r - 3.4, h), (r - 3.4, h - 6.4),
                     (r - 1.2, h - 8.4), (r - 1.2, 1.6), (0, 1.6)], 48)
    out = {"glass": glass}
    if with_liquid:
        out["liquid"] = cyl(r - 1.4, 1.7, 1.7 + with_liquid, res=48)
    return out


def tube_05ml() -> dict:
    """0.5 mL tube, tip at z 0, rim up, lid open to the side."""
    d = DIMS["tube_05"]
    r = d["d"] / 2
    body = revolve([(0, 0), (1.2, 0), (r - 0.5, 12), (r, 26), (r, d["length"] - 2), (d["rim_d"] / 2, d["length"] - 2),
                    (d["rim_d"] / 2, d["length"]), (r - 0.6, d["length"]), (r - 0.6, 26), (r - 1.1, 12), (1.6, 0.8), (0, 0.8)], 32)
    lid = cyl(d["rim_d"] / 2, 0, 2.2, res=32).translate((d["rim_d"] + 0.5, 0, d["length"] - 2.2), inplace=False)
    return {"body": body, "lid": lid}


def ezstat_box() -> dict:
    bx, by, bz = DIMS["ezstat"]["box"]
    body = box(-bx / 2, -by / 2, 0, bx / 2, by / 2, bz)
    face = box(-bx / 2 + 8, -by / 2 - 0.3, 8, bx / 2 - 8, -by / 2, bz - 8)
    return {"body": body, "face": face}


def bottle(d, h, neck_d=None, cap_h=None) -> dict:
    neck_d = neck_d or d * 0.45
    cap_h = cap_h or h * 0.12
    r, rn = d / 2, neck_d / 2
    body = revolve([(0, 0), (r - 2, 0), (r, 2), (r, h * 0.78), (rn + 1, h * 0.9), (rn, h * 0.9), (rn, h), (0, h)], 48)
    cap = cyl(rn + 1.2, h - 1, h - 1 + cap_h, res=40)
    return {"body": body, "cap": cap}


def stir_module() -> dict:
    """Compact stir module (byu-vcl#269), schematic at its published envelope: 49 x 44 base, body top 42,
    vial rim at 67.6 with the 4.6 mm spacer. The vial sits in the holder's bore."""
    base = box(-24.5, -22, 0, 24.5, 22, 12)
    fan = cyl(19.0, 12, 30, res=48)
    holder = revolve([(14.6, 30), (17.5, 30), (17.5, 42), (14.6, 42)], 48)
    return {"base": base, "fan": fan, "holder": holder}


def flatted_disc(R=0.5 * IN, half=10.0, h=6.0, n_arc=10) -> pv.PolyData:
    """A slice of round bar with four flats milled 2 x half across, face at z 0, back at z -h. The outline is
    the four corner arcs of the bar; straight flats join them."""
    a0 = math.acos(half / R)  # the arc spans a0 .. 90 deg - a0 around each diagonal
    pts = []
    for q in range(4):
        for a in np.linspace(a0, math.pi / 2 - a0, n_arc):
            ang = a + q * math.pi / 2
            pts.append((R * math.cos(ang), R * math.sin(ang), -h))
    pts = np.array(pts)
    n = len(pts)
    poly = pv.PolyData(pts, faces=np.hstack([[n], np.arange(n)]))
    return fin(poly.extrude((0, 0, h), capping=True), 40)


def collar(d_in=10.0, d_out=18.0, h=5.0) -> pv.PolyData:
    return revolve([(d_in / 2, 0), (d_out / 2, 0), (d_out / 2, h), (d_in / 2, h)], 48)
