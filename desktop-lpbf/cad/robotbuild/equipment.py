"""The robot shop's equipment as meshes, from published drawings and spec sheets (round 7, issue #260, PR #266).

Sterling, 2026-11-25: two mobile manipulators shown carrying out every machining and assembly step, "which also implies
getting accurate models of the corresponding machining, processing, and assembly equipment". These replace
analysis/shop/shop_cell.py's boxes. Every builder returns {name: Part} in its station's local frame (shop_cell's
convention: mm, z up, origin on the floor at the middle of the face the robot works from, +y into the station, x to the
right as you face it), with the moving pieces as their own parts so a renderer moves them with a 4x4 (Part.M). The same
parts give the planner FCL arrays (`fcl_items`): everything with collide=True, triangulated, in the shop frame.

Sources (fetched 2026-11-20 22:18-22:45 UTC unless noted; every one is also a row of robot-shop-equipment.csv):
  Haas VF-4      haascnc.com VF-4 page and machine layout drawing (vf-4_4ss_mld_01_2022.pdf): travels 1270/508/635 mm,
                 table 1321 x 495 mm with 5 T-slots 16 mm on 80 mm, table top 940 mm, spindle centre line 838 mm and the
                 table's front 341 mm behind the front face, nose to table 107-742 mm, enclosure 3128 x 2314 mm with its
                 roof at 2004 mm, 20-pocket carousel; the front aperture 1588 mm (62.5 in) from the 2023 VF-3/SS drawing
                 (same enclosure). Estimated here: the sill (880) and header (1900), the doors' windows, the column's top
                 above the roof (to 2740 mm), the carousel's size, the pendant's arm.
  Pendant        the Haas NGC pendant as byu-vcl PR 318 fitted it on the ST-10 (machining_fit.py): 477 x 635 x 95 mm.
  HRT210         haascnc.com HRT210 page and its 2016 dimension drawing: platter 210 mm, centre height 152.40 mm, body
                 470 x 178 x 315 mm; on the 63.5 mm (2-1/2 in.) riser of setup F-S3 (chamber-construction.md).
  HPTS6          Haas 6 in. pneumatic tailstock: 152 mm centre height (proportions estimated).
  Kurt XL6A      Penn Tool's listing: 6 in. jaws, opening 0-14.5 in.; the body's length and height are estimated
                 (a 6 in. Kurt is about 175 mm wide; jaws 1.75 in. high).
  Haas ST-10     vendored from byu-vcl PR 318 (vertical-lab/machining_cell.py, branch claude/issue-303-20261103-1736,
                 9740ba8): ST10 and st10_parts(), its outside from Haas's ST-10/15 machine layout drawing (12/20/2024)
                 checked against footage by machining_fit.py. Kept as fitted: enclosure 2160 x 1021 x 1795 mm, door
                 opening 794-1382 mm along the front from a 680 mm sill to 1636 mm, spindle axis 307 mm behind the front
                 face at 991 mm. The inside (6.5 in. chuck from the ST-10 page, the turret, the slant bed) is ours.
  Hyd-Mech S-20A surplusrecord.com listing: 13 x 18 in. capacity, table 31 in. (787 mm), about 93 x 86 x 52 in.; a scissor
                 (pivot) saw, so the head swings about a hinge behind the vise. Wheel size and head shape estimated.
  JumboFlex 50   Schmalz JumboFlex (generation 1) page: up to 50 kg, one-hand control, loads to 2 x 1 m. Tube diameter,
                 stroke and the suction foot are estimates.
  Gorbel jib     WSJ360-500-8-14 (tsoverheadcrane.com): 500 lb, 8 ft under the boom, 14 ft span, 360 deg.
  Vestil table   SCTAB-1000-2040-AC (zoro.com): 20 x 40 in. platform, 1000 lb; set to 760 mm here.
  Crest tank     Powersonic 7 gal (globalindustrial.com): tank 19.5 x 11.75 x 8 in.; its outside is estimated.
  ATI deburr     Speedeburr / AC-180 class compliant spindle (ati-ia.com): about 0.6 kg; on a fixed stand here.
  Granite        Precise grade A 36 x 24 x 4 in. (penntoolco.com) on McMaster's 2196A831 stand, 36 in. work height.
  Gauges         Mitutoyo 570-412 height gauge (0-300 mm) and 511-712-20 dial bore gauge (35-60 mm): sizes estimated.
  Pallet         GMA 48 x 40 in. stringer pallet, ~5.6 in. high (the US standard); pallet jack 27 x 48 in. forks, 2.9 in.
                 lowered (the common manual jack, e.g. Vestil PM4-2748): published class sizes, the body estimated.
  Grippers       Robotiq 2F-85 (ur_arm's meshes), OnRobot 3FG15 (external grip 4-152 mm, 1.15 kg; its body drawn as a
                 156 mm puck, estimated), OnRobot VGP20 (264 x 184 x 92 mm, datasheet), ATI QC-11 tool changer (0.245 kg).
  TIG            a 48 x 36 in. welding table at 36 in., an inverter TIG on a cart, an argon cylinder: class sizes, estimated.

Nothing here is a layout of a real BYU room; the shop is hypothetical (robot-shop.md).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
import pyvista as pv

INCH = 25.4

# ------------------------------------------------------------------------------------------------ colours (Haas look)
C = dict(
    haas="#dfe3e6", haas_dark="#3f464d", haas_red="#c8102e", glass="#9fc3d9", steel="#a7afb7", dark="#2b2f33",
    table="#5b646d", slot="#3e454c", vise="#2f5f8a", jaw="#9aa3ab", rotary="#2d3136", platter="#8e979f",
    head="#d8dce0", holder="#3a3f45", tool="#d9b44a", screen="#101418", saw="#2e6d46", saw_blade="#c9ced3",
    yellow="#e5b400", orange="#e07b28", wood="#b8925a", wood_dark="#8f6b3d", box="#c8a46e", granite="#3c3f44",
    blue="#2b6cb0", alu="#cfd4d9", rubber="#202326", tank="#bfc6cc", water="#7fb5d8", green="#2a9d8f",
    mir="#4a4f55", gauge="#d0d4d8", argon="#6b8e23", tig="#1f4e8c", red="#b22222", stand="#6b7480",
)


@dataclass
class Part:
    mesh: pv.PolyData
    color: str = "#b9c0c7"
    opacity: float = 1.0
    collide: bool = True
    M: np.ndarray = field(default_factory=lambda: np.eye(4))   # extra pose in the station frame (moving pieces)
    group: str = ""


# ------------------------------------------------------------------------------------------------ mesh helpers
def box(x0, x1, y0, y1, z0, z1):
    return pv.Box(bounds=(min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1))).triangulate()


def cyl(p0, p1, r, res=32):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    L = float(np.linalg.norm(d))
    return pv.Cylinder(center=(p0 + p1) / 2, direction=d / L, radius=r, height=L, resolution=res).triangulate()


def tube(p0, p1, ro, ri, res=40):
    """A closed annulus (pipe) from p0 to p1."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    L = float(np.linalg.norm(d))
    disc = pv.Disc(center=(0, 0, 0), inner=ri, outer=ro, normal=(0, 0, 1), r_res=1, c_res=res)
    m = disc.extrude((0, 0, L), capping=True).triangulate()
    return m.transform(_frame_to(p0, d / L), inplace=False)


def _frame_to(p0, z):
    z = np.asarray(z, float) / np.linalg.norm(z)
    x = np.cross([0, 0, 1.0], z) if abs(z[2]) < 0.95 else np.cross([0, 1.0, 0], z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    M = np.eye(4)
    M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = x, y, z, p0
    return M


def merge(ms):
    ms = [m for m in ms if m is not None and m.n_points]
    out = ms[0].copy()
    for m in ms[1:]:
        out = out.merge(m)
    return out.triangulate()


def open_box(x0, x1, y0, y1, z0, z1, t):
    """A tank: floor and four walls, open at the top."""
    return merge([box(x0, x1, y0, y1, z0, z0 + t), box(x0, x1, y0, y0 + t, z0, z1), box(x0, x1, y1 - t, y1, z0, z1),
                  box(x0, x0 + t, y0, y1, z0, z1), box(x1 - t, x1, y0, y1, z0, z1)])


def frame_ring(x0, x1, y0, y1, z0, z1, ix0, ix1, iy0, iy1):
    return merge([box(x0, x1, y0, iy0, z0, z1), box(x0, x1, iy1, y1, z0, z1), box(x0, ix0, iy0, iy1, z0, z1),
                  box(ix1, x1, iy0, iy1, z0, z1)])


def T(p=(0, 0, 0), R=None):
    M = np.eye(4)
    if R is not None:
        M[:3, :3] = R
    M[:3, 3] = p
    return M


def Rz(deg):
    a = math.radians(deg)
    return np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1.0]])


def Rx(deg):
    a = math.radians(deg)
    return np.array([[1.0, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])


def Ry(deg):
    a = math.radians(deg)
    return np.array([[math.cos(a), 0, math.sin(a)], [0, 1.0, 0], [-math.sin(a), 0, math.cos(a)]])


def about(M_rot, c):
    """A 3x3 rotation about the point c, as a 4x4."""
    c = np.asarray(c, float)
    return T(c - M_rot @ c, M_rot)


def placed(parts, M, prefix=""):
    """parts moved by M (their own M premultiplied), names prefixed."""
    return {prefix + n: Part(p.mesh, p.color, p.opacity, p.collide, M @ p.M, p.group) for n, p in parts.items()}


def world_mesh(p: Part):
    return p.mesh.transform(p.M, inplace=False) if not np.allclose(p.M, np.eye(4)) else p.mesh


def fcl_items(parts, M=np.eye(4), prefix=""):
    """[(name, (v, f), colour)] in the frame M maps to, for shop_cell.ShopScene / cell.Body (collide=True only)."""
    out = []
    for n, p in parts.items():
        if not p.collide:
            continue
        m = p.mesh.triangulate()
        v = np.asarray(m.points, float)
        f = m.faces.reshape(-1, 4)[:, 1:].astype(np.int32)
        A = M @ p.M
        v = v @ A[:3, :3].T + A[:3, 3]
        out.append((prefix + n, (v, f), p.color))
    return out


# ================================================================================================ Haas VF-4
VF4 = dict(
    W=3128.0, D=2314.0, roof=2004.0, col_top=2740.0,       # enclosure (MLD); the column's top above the roof is est.
    travel=(1270.0, 508.0, 635.0),
    table_L=1321.0, table_W=495.0, table_t=90.0, table_z=940.0, slots=5, slot_w=16.0, slot_pitch=80.0, slot_d=14.0,
    spindle_y=838.0, table_front_y=341.0, nose_to_table=(107.0, 742.0),
    door_w=1588.0, sill_z=880.0, header_z=1900.0, front_t=60.0,   # aperture (2023 drawing); sill and header est.
    door_t=28.0, win=(560.0, 600.0),                               # each door's window (est.)
    pendant=(477.0, 635.0, 95.0),                                  # NGC pendant as PR 318 fitted it on the ST-10
    carousel_r=360.0, pockets=20,
)


def vf4_table(z_top, xc, yc, P=VF4):
    """The table with its five T-slots along X (render_vmc.table, in the machine)."""
    L, W, t = P["table_L"], P["table_W"], P["table_t"]
    body = box(xc - L / 2, xc + L / 2, yc - W / 2, yc + W / 2, z_top - t, z_top - P["slot_d"])
    n, p, sw = P["slots"], P["slot_pitch"], P["slot_w"]
    ys = [yc + (k - (n - 1) / 2) * p for k in range(n)]
    edges = [yc - W / 2] + sum([[y - sw / 2, y + sw / 2] for y in ys], []) + [yc + W / 2]
    strips = [box(xc - L / 2, xc + L / 2, a, b, z_top - P["slot_d"], z_top) for a, b in zip(edges[0::2], edges[1::2])]
    slots = [box(xc - L / 2, xc + L / 2, y - sw / 2, y + sw / 2, z_top - P["slot_d"], z_top - P["slot_d"] + 1) for y in ys]
    return merge([body] + strips), merge(slots)


def kurt_xl6a(opening=150.0):
    """Kurt XL6A 6 in. air vise in its own frame: base centred on the origin, jaws closing along +y towards the fixed
    jaw at the back (+y), on the table at z = 0. Returns parts and the clamping geometry."""
    jw, jh = 6 * INCH, 1.75 * INCH                         # jaw width and height (published class sizes)
    L, Wb, Hb = 640.0, 175.0, 98.0                         # body length (opens to 14.5 in.), width, height to the ways (est.)
    o = float(np.clip(opening, 0.0, 14.5 * INCH))
    y_fixed = L / 2 - 120.0                                # the fixed jaw's clamping face
    parts = {
        "vise body": Part(merge([box(-Wb / 2, Wb / 2, -L / 2, L / 2, 0, Hb - 25), box(-Wb / 2 - 25, Wb / 2 + 25, -60, 60, 0, 22)]),
                          C["vise"]),
        "vise fixed jaw": Part(merge([box(-Wb / 2, Wb / 2, y_fixed, y_fixed + 70, Hb - 25, Hb + jh),
                                      box(-jw / 2, jw / 2, y_fixed, y_fixed + 8, Hb, Hb + jh)]), C["vise"]),
        "vise moving jaw": Part(merge([box(-Wb / 2, Wb / 2, y_fixed - o - 90, y_fixed - o, Hb - 25, Hb + jh),
                                       box(-jw / 2, jw / 2, y_fixed - o - 8, y_fixed - o, Hb, Hb + jh)]), C["vise"]),
        "vise jaw plates": Part(merge([box(-jw / 2, jw / 2, y_fixed - 1, y_fixed + 1, Hb + 2, Hb + jh),
                                       box(-jw / 2, jw / 2, y_fixed - o - 1, y_fixed - o + 1, Hb + 2, Hb + jh)]), C["jaw"]),
        "vise air cylinder": Part(cyl((0, -L / 2 - 150, 55), (0, -L / 2, 55), 55.0), C["dark"]),
        "vise air line": Part(cyl((60, -L / 2 - 120, 40), (60, -L / 2 - 120, 0), 5.0), C["blue"], collide=False),
    }
    return parts, dict(y_fixed=y_fixed, floor_z=Hb, top_z=Hb + jh, jaw_w=jw, opening=o, L=L)


def hrt210(a_deg=0.0, riser=63.5, with_tail=False, tail_x=420.0):
    """Haas HRT210 on a riser, A axis along +x. Frame: origin on the table under the platter face's centre; the housing
    behind it (-x), the platter facing +x. Sized as freecad_cam.FIXTURES['frame_C0'] has it (holder_check.py swept the
    tools against those boxes): housing 177.8 mm along A (the drawing's 7.0 in.), 248 mm across plus the motor box on -y
    (470 mm in all, the drawing's 18.5 in.), axis 152.4 mm above its base; platter 210 x 15.9 mm. Returns parts (the
    platter in 'HRT210 platter', group 'A') and the axis point."""
    zc = riser + 152.4
    hx0, hx1 = -193.7, -15.9                       # housing along A, platter face at x = 0
    parts = {
        "HRT210 riser": Part(box(hx0, hx1, -342.9, 124.0, 0, riser), "#3e454c"),
        "HRT210 housing": Part(merge([box(hx0, hx1, -124.0, 124.0, riser, zc + 124.0),
                                     box(hx0 - 20, hx1 + 5, -150.0, 150.0, riser, riser + 18)]), C["rotary"]),
        "HRT210 motor box": Part(box(hx0, hx1, -342.9, -124.0, riser, zc + 124.0), C["rotary"]),
        "HRT210 badge": Part(box(hx0 + 30, hx1 - 30, -125.0, -124.0, zc + 40, zc + 90), C["haas_red"], collide=False),
    }
    plat = merge([cyl((hx1, 0, zc), (0, 0, zc), 105.0, res=64)] +
                 [box(-1, 1, -6, 6, 30, 100).transform(T((0.5, 0, zc), Rx(60 * k)), inplace=False) for k in range(6)])
    parts["HRT210 platter"] = Part(plat, C["platter"], M=about(Rx(a_deg), (0, 0, zc)), group="A")
    if with_tail:
        parts["HPTS6 tailstock"] = Part(merge([box(tail_x + 20, tail_x + 170, -70, 70, riser, zc + 45),
                                                box(tail_x, tail_x + 200, -95, 95, riser, riser + 18),
                                                cyl((tail_x - 30, 0, zc), (tail_x + 20, 0, zc), 22.0)]), C["rotary"])
        parts["tailstock riser"] = Part(box(tail_x - 10, tail_x + 210, -105, 105, 0, riser), "#3e454c")
    return parts, dict(axis=(0.0, 0.0, zc), riser=riser)


TABLE_LAYOUT = dict(hrt_face=-200.0, fixture=100.0, vise=300.0)   # table-local x of the platter face, the 3-axis
                                                                  # fixtures' centre and the vise's centre (our layout)


def vf4(door=1.0, table_x=0.0, table_y=0.0, spindle_z=None, vise_open=150.0, hrt_a=0.0, with_vise=False, with_hrt=True,
        tool=("end mill 3/4 in.", 19.05, 60.0), P=VF4):
    """The Haas VF-4 in its station frame (origin on the floor at the middle of the front face, +y into the machine).
    door: 0 shut .. 1 fully open (both doors part to the sides). table_x / table_y: the table's offset (mm) from its load
    position (centred on the spindle in X, nearest the door in Y). spindle_z: nose height above the table top (default
    the top of travel). The vise sits on the table's right half and the HRT210 (on its riser) on the left half, as
    shop_cell has them. Returns (parts, meta)."""
    W, D, H = P["W"], P["D"], P["roof"]
    ft, dw, s0, s1 = P["front_t"], P["door_w"], P["sill_z"], P["header_z"]
    out = {}
    # ---- the enclosure: front frame round the aperture, side and back walls, the roof with the column's hood
    out["front panel below the door"] = Part(box(-W / 2, W / 2, 0, ft, 0, s0), C["haas"])
    out["front panel above the door"] = Part(box(-W / 2, W / 2, 0, ft, s1, H), C["haas"])
    out["front panel left of the door"] = Part(box(-W / 2, -dw / 2, 0, ft, s0, s1), C["haas"])
    out["front panel right of the door"] = Part(box(dw / 2, W / 2, 0, ft, s0, s1), C["haas"])
    out["front sill trim"] = Part(box(-dw / 2 - 30, dw / 2 + 30, -20, ft, s0 - 40, s0), C["haas_dark"])
    out["Haas red stripe"] = Part(box(-W / 2, W / 2, -2, 0, H - 120, H - 90), C["haas_red"], collide=False)
    out["left wall"] = Part(box(-W / 2, -W / 2 + 20, ft, D, 0, H), C["haas"], opacity=1.0)
    out["right wall"] = Part(box(W / 2 - 20, W / 2, ft, D, 0, H), C["haas"])
    out["back wall"] = Part(box(-W / 2, W / 2, D - 20, D, 0, H), C["haas"])
    # the roof; its panel over the table (y 60-600) lifts off for crane loading (our assumption, to check on the machine)
    out["roof"] = Part(merge([box(-W / 2, -560, ft, D, H - 20, H), box(560, W / 2, ft, D, H - 20, H),
                              box(-560, 560, 600, 1050, H - 20, H)]), C["haas"])
    out["roof panel over the table"] = Part(box(-560, 560, ft, 600, H - 20, H), C["haas"], group="roof panel")
    out["column hood"] = Part(merge([box(-560, 560, 1050, D - 60, H - 20, P["col_top"]),
                                     box(-330, 330, 600, 1050, H - 20, P["col_top"] - 40)]), C["haas"])
    # ---- the two sliding doors, each with its window; open = parted to the sides behind the front frame
    dwi = dw / 2 + 40.0
    for side, sgn in (("left", -1), ("right", 1)):
        x_shut0, x_shut1 = (0.0, dwi) if sgn > 0 else (-dwi, 0.0)
        shift = sgn * door * dwi
        x0, x1 = x_shut0 + shift, x_shut1 + shift
        wx, wz = P["win"]
        cx = (x0 + x1) / 2
        door_m = merge([box(x0, x1, -P["door_t"] - 6, -6, s0 - 30, (s0 + s1) / 2 - wz / 2),
                        box(x0, x1, -P["door_t"] - 6, -6, (s0 + s1) / 2 + wz / 2, s1 + 30),
                        box(x0, cx - wx / 2, -P["door_t"] - 6, -6, (s0 + s1) / 2 - wz / 2, (s0 + s1) / 2 + wz / 2),
                        box(cx + wx / 2, x1, -P["door_t"] - 6, -6, (s0 + s1) / 2 - wz / 2, (s0 + s1) / 2 + wz / 2)])
        out[f"{side} door"] = Part(door_m, C["haas"])
        out[f"{side} door window"] = Part(box(cx - wx / 2, cx + wx / 2, -P["door_t"] + 2, -14, (s0 + s1) / 2 - wz / 2,
                                              (s0 + s1) / 2 + wz / 2), C["glass"], opacity=0.28)
        hx = x1 - 60 if sgn < 0 else x0 + 40
        out[f"{side} door handle"] = Part(box(hx, hx + 20, -P["door_t"] - 60, -P["door_t"] - 6, 1200, 1500), C["dark"])
    # robot-ready option: the Haas auto door's drive on the header (est. size)
    out["auto door drive (option)"] = Part(box(-dw / 2 - 260, -dw / 2 + 120, -110, -6, s1 + 40, s1 + 190), C["haas_dark"])
    # ---- the pendant, swung back against the right side (as PR 318 swings the ST-10's), the work light, the label
    pw, ph, pd = P["pendant"]
    out["pendant"] = Part(merge([box(W / 2 + 10, W / 2 + 10 + pd, 120, 120 + pw, 1080, 1080 + ph),
                                 box(W / 2, W / 2 + 40, 300, 360, 1500, 1560)]), C["haas"])
    out["pendant screen"] = Part(box(W / 2 + 10 + pd, W / 2 + 12 + pd, 170, 170 + 380, 1330, 1330 + 280), C["screen"],
                                 collide=False)
    out["pendant red button"] = Part(cyl((W / 2 + 10 + pd, 120 + pw - 60, 1150), (W / 2 + 30 + pd, 120 + pw - 60, 1150), 18),
                                     C["haas_red"], collide=False)
    # ---- inside: base and chip trough with the auger, saddle, way covers, table, column, head, spindle, carousel
    tf, tL, tW, tz, tt = P["table_front_y"], P["table_L"], P["table_W"], P["table_z"], P["table_t"]
    out["base and chip trough"] = Part(merge([box(-W / 2 + 20, W / 2 - 20, ft, tf - 20, 0, s0 - 120),
                                              box(-W / 2 + 20, W / 2 - 20, ft, ft + 30, s0 - 120, s0 - 40)]), C["haas_dark"])
    out["chip auger"] = Part(cyl((-W / 2 + 60, ft + 120, s0 - 160), (W / 2 - 60, ft + 120, s0 - 160), 55.0), C["steel"],
                             collide=False)
    xc = table_x
    yc = tf + tW / 2 + table_y
    out["saddle"] = Part(box(xc * 0 - 700, 700, yc - 330, yc + 330, 420, tz - tt), C["haas_dark"])
    out["base casting"] = Part(box(-W / 2 + 120, W / 2 - 120, tf - 20, D - 80, 0, 420), C["haas_dark"])
    out["Y way cover (bellows)"] = Part(box(-650, 650, yc + 330, 1180, tz - tt - 60, tz - tt - 20), "#596169")
    body, slots = vf4_table(tz, xc, yc, P)
    out["table"] = Part(body, C["table"], group="table")
    out["table T-slots"] = Part(slots, C["slot"], collide=False, group="table")
    ysp = P["spindle_y"]
    nose = tz + (P["nose_to_table"][1] if spindle_z is None else spindle_z)
    out["column"] = Part(box(-560, 560, 1180, D - 80, 420, P["col_top"] - 60), C["haas_dark"])
    out["head"] = Part(merge([box(-250, 250, ysp - 170, 1180, nose + 150, nose + 820),
                              box(-200, 200, ysp + 120, 1180, nose + 820, nose + 1050)]), C["haas"], group="head")
    out["head stripe"] = Part(box(-252, 252, ysp - 172, ysp - 168, nose + 700, nose + 740), C["haas_red"], collide=False,
                              group="head")
    out["spindle nose"] = Part(cyl((0, ysp, nose), (0, ysp, nose + 150), 85.0, res=48), C["steel"], group="head")
    name, td, stick = tool
    out["tool holder (CT40)"] = Part(merge([cyl((0, ysp, nose - 70), (0, ysp, nose), 31.75, res=40),
                                            cyl((0, ysp, nose - 100), (0, ysp, nose - 70), 25.0, res=40)]), C["holder"],
                                     group="head")
    out["tool"] = Part(cyl((0, ysp, nose - 100 - stick), (0, ysp, nose - 100), td / 2, res=28), C["tool"], group="head")
    out["air gun nozzle (AAG option)"] = Part(cyl((110, ysp - 60, nose + 160), (60, ysp - 30, nose + 20), 6.0), C["dark"],
                                              collide=False, group="head")
    # 20-pocket carousel ("umbrella") on the column's left, holders hanging from its rim
    cr = P["carousel_r"]
    cz = tz + P["nose_to_table"][1] + 120.0          # pockets level with the nose at Z home (tool change height)
    cxx, cyy = -cr - 330, ysp + 40
    rim = [cyl((cxx, cyy, cz - 40), (cxx, cyy, cz + 60), cr, res=60), cyl((cxx, cyy, cz + 60), (cxx, cyy, cz + 260), 140.0)]
    holders = []
    for k in range(P["pockets"]):
        a = 2 * math.pi * k / P["pockets"]
        px, py = cxx + (cr - 45) * math.cos(a), cyy + (cr - 45) * math.sin(a)
        holders.append(cyl((px, py, cz - 140), (px, py, cz - 40), 26.0, res=16))
    out["tool carousel (20 pockets)"] = Part(merge(rim), C["haas"])
    out["tool holders in the carousel"] = Part(merge(holders), C["holder"], collide=False)
    out["carousel arm"] = Part(box(cxx, -200, cyy - 60, cyy + 60, cz + 150, cz + 260), C["haas_dark"])
    out["coolant tank"] = Part(box(-W / 2 + 60, -W / 2 + 900, D - 700, D - 90, 0, 350), "#2f6f9f", collide=False)
    out["work light"] = Part(box(-200, 200, 200, 260, H - 70, H - 30), "#f6f4d2", collide=False)
    # ---- workholding on the table: Kurt XL6A on the right half, HRT210 + riser + tailstock on the left half
    meta = dict(table_centre=(xc, yc, tz), table_top=tz, spindle=(0.0, ysp, nose), door=(dw, s0, s1), nose_z=nose)
    L_ = TABLE_LAYOUT
    meta.update(fixture_centre=(xc + L_["fixture"], yc, tz))
    if with_vise:                     # jaws along X, the fixed jaw on the -x side, the air cylinder overhanging at +x
        vparts, vm = kurt_xl6a(vise_open)
        Mv = T((xc + L_["vise"], yc, tz), Rz(90.0))
        out.update({n: Part(p.mesh, p.color, p.opacity, p.collide, Mv @ p.M, "table") for n, p in vparts.items()})
        meta.update(vise_centre=(xc + L_["vise"], yc, tz), vise_x_fixed=xc + L_["vise"] - vm["y_fixed"],
                    vise_floor_z=tz + vm["floor_z"], vise_top_z=tz + vm["top_z"], vise_M=Mv)
    if with_hrt:
        hparts, hm = hrt210(hrt_a)
        Mh = T((xc + L_["hrt_face"], yc, tz))
        out.update({n: Part(p.mesh, p.color, p.opacity, p.collide, Mh @ p.M, "table") for n, p in hparts.items()})
        meta.update(hrt_axis=tuple((Mh @ np.r_[hm["axis"], 1.0])[:3]), hrt_M=Mh)
    # WIPS (option): the tool setter on the table's left end
    out["WIPS tool setter (option)"] = Part(cyl((xc - tL / 2 + 60, yc - 160, tz), (xc - tL / 2 + 60, yc - 160, tz + 95), 32.0),
                                            C["dark"], group="table")
    return out, meta


# ================================================================================================ Haas ST-10 (PR 318)
# Vendored from byu-vcl PR 318, vertical-lab/machining_cell.py (9740ba8), with its attribution: the outside from Haas's
# ST-10/15 machine layout drawing (12/20/2024), checked against footage by machining_fit.py; the fitted dimensions kept.
ST10 = dict(
    W=2160.0, D=1021.0, H=1795.0, t=20.0,
    base_h=676.0, base_x0=40.0, base_x1=2087.0, base_y0=35.0, base_y1=985.0, feet=76.0,
    door_x0=794.0, door_x1=1382.0, door_z0=680.0, door_z1=1636.0,
    panel_x0=767.0, panel_w=642.0,
    win_x0=235.0, win_w=238.0, win_z0=1143.0, win_z1=1486.0,
    surround_x0=740.0, surround_x1=1430.0,
    pend_x0=1492.0, pend_x1=1969.0, pend_z0=1032.0, pend_z1=1667.0, pend_d=205.0,
    scr_x0=1620.0, scr_x1=1937.0, scr_z0=1376.0, scr_z1=1604.0,
    lcov_w=130.0, lcov_y0=20.0, lcov_y1=470.0, lcov_z0=800.0, lcov_z1=1290.0,
    cab_x0=950.0, cab_x1=1900.0, cab_d=270.0, cab_h=1842.0,
    conv_x1=3138.0, conv_y0=130.0, conv_y1=510.0, conv_low=300.0, conv_top=1576.0, conv_dis=1064.0, conv_head=343.0,
    spin_y=307.0, spin_z=991.0, nose_x=860.0,
)
ST10_GREY, ST10_WHITE, ST10_DOOR = "#545a5e", "#e6e8ea", "#404347"


def _slab(p0, p1, half_w, y0, y1):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    L = float(np.hypot(*d))
    a = math.degrees(math.atan2(d[1], d[0]))
    b = box(0, L, y0, y1, -half_w, half_w)
    return b.rotate_y(-a, inplace=False).translate((p0[0], 0, p0[1]), inplace=False)


def st10(door=1.0, jaw_open=0.0, chuck_d=165.0, p=None, jaw_deg=90.0):
    """The Haas ST-10 in its station frame: PR 318's machine frame (x along the spindle from the headstock end, y from the
    front face in, z up) shifted so that x = 0 is the chuck's face. door: 0 shut .. 1 open (it slides left over the
    white panel). The 6.5 in. chuck (ST-10 page) is on the spindle nose; the turret parks at the right."""
    p = dict(ST10, **(p or {}))
    W, D, H, t, bh = p["W"], p["D"], p["H"], p["t"], p["base_h"]
    dx0, dx1, dz0, dz1 = p["door_x0"], p["door_x1"], p["door_z0"], p["door_z1"]
    chuck_L = 95.0
    x_face = p["nose_x"] + chuck_L                     # the chuck face in PR 318's frame
    S = T((-x_face, 0.0, 0.0))                          # PR 318 frame -> station frame
    out = {}
    enc = [box(0, W, D - t, D, bh, H), box(0, t, 0, D, bh, H), box(W - t, W, 0, D, bh, H), box(0, W, 0, D, H - t, H)]
    out["skin back, sides and roof"] = Part(merge(enc), ST10_WHITE)
    out["front panel left of the door"] = Part(box(0, dx0, 0, t, bh, H - t), ST10_WHITE)
    out["front panel right of the door"] = Part(box(dx1, W, 0, t, bh, H - t), ST10_WHITE)
    out["front panel above the door"] = Part(box(dx0, dx1, 0, t, dz1, H - t), ST10_WHITE)
    out["front panel below the door"] = Part(box(dx0, dx1, 0, t, bh, dz0), ST10_WHITE)
    sx0, sx1 = p["surround_x0"], p["surround_x1"]
    out["door surround"] = Part(merge([box(sx0, dx0, -4, 0, bh, H - 60), box(dx1, sx1, -4, 0, bh, H - 60),
                                       box(dx0, dx1, -4, 0, dz1, H - 60), box(sx0, sx1, -4, 0, bh, dz0)]), ST10_GREY)
    out["base"] = Part(merge([box(p["base_x0"], p["base_x1"], p["base_y0"], p["base_y1"], p["feet"], bh),
                              box(-5, W + 5, -12, p["base_y1"], bh - 28, bh)]), ST10_GREY)
    out["motor cover"] = Part(box(-p["lcov_w"], 0, p["lcov_y0"], p["lcov_y1"], p["lcov_z0"], p["lcov_z1"]), ST10_WHITE)
    out["electrical cabinet"] = Part(box(p["cab_x0"], p["cab_x1"], D, D + p["cab_d"], p["feet"], p["cab_h"]), ST10_WHITE)
    pd = 110.0                                          # PR 318's cell swings the pendant back: 110 mm proud, not 205
    out["pendant"] = Part(merge([box(p["pend_x0"], p["pend_x1"], -pd, -pd + 95, p["pend_z0"], p["pend_z1"]),
                                 box(p["pend_x1"] - 90, p["pend_x1"] - 20, -pd + 95, 0, p["pend_z1"] - 160, p["pend_z1"] - 60)]),
                          ST10_WHITE)
    out["pendant screen"] = Part(box(p["scr_x0"], p["scr_x1"], -pd - 2, -pd, p["scr_z0"], p["scr_z1"]), C["screen"], collide=False)
    xh0 = p["conv_x1"] - p["conv_head"]
    cy0, cy1, lo = p["conv_y0"], p["conv_y1"], p["conv_low"]
    out["chip conveyor"] = Part(merge([box(p["base_x1"] - 200, p["base_x1"] + 280, cy0, cy1, lo, lo + 210),
                                       _slab((p["base_x1"] + 120, lo + 105), (xh0 + 60, p["conv_top"] - 120), 115.0, cy0, cy1),
                                       box(xh0, p["conv_x1"], cy0, cy1, p["conv_top"] - 330, p["conv_top"]),
                                       box(xh0 + 60, p["conv_x1"] - 60, cy0 + 20, cy1 - 20, p["conv_dis"], p["conv_top"] - 330)]),
                                ST10_GREY)
    # the door: shut over the opening; open = slid left by its width less the overlap
    x0d = p["panel_x0"] - door * (p["panel_w"] - 20.0)
    pw = p["panel_w"]
    out["door"] = Part(merge([box(x0d, x0d + pw, -30, -6, dz0 - 20, p["win_z0"]), box(x0d, x0d + pw, -30, -6, p["win_z1"], dz1 + 30),
                              box(x0d, x0d + p["win_x0"], -30, -6, p["win_z0"], p["win_z1"]),
                              box(x0d + p["win_x0"] + p["win_w"], x0d + pw, -30, -6, p["win_z0"], p["win_z1"]),
                              box(x0d + pw - 75, x0d + pw - 55, -70, -30, 1150, 1450)]), ST10_DOOR)
    out["door window"] = Part(box(x0d + p["win_x0"], x0d + p["win_x0"] + p["win_w"], -22, -14, p["win_z0"], p["win_z1"]),
                              C["glass"], opacity=0.3, collide=False)
    out["auto door drive (VOP option)"] = Part(box(dx0 - 150, dx0 + 200, -90, -4, dz1 + 40, dz1 + 130), ST10_GREY)
    # inside (ours): chip pan, slant bed, headstock, spindle nose, chuck and jaws, turret
    ys, zs = p["spin_y"], p["spin_z"]
    out["chip pan"] = Part(box(t, W - t, t, D - t, bh, bh + 12), "#5c6064")
    out["slant bed"] = Part(box(x_face + 30, W - 60, ys + 180, D - t, bh, zs + 120), "#4a4f54")
    out["headstock"] = Part(box(t + 20, p["nose_x"] - 20, ys - 250, D - t, bh, zs + 330), "#7d838a")
    out["spindle nose"] = Part(cyl((p["nose_x"] - 25, ys, zs), (p["nose_x"], ys, zs), 95.0, res=48), C["steel"])
    out["chuck (6.5 in.)"] = Part(cyl((p["nose_x"], ys, zs), (x_face - 20, ys, zs), chuck_d / 2, res=48), "#80878e",
                                  group="spindle")
    jr = 27.0 + jaw_open
    for k in range(3):
        a = math.radians(jaw_deg + 120 * k)          # jaw_deg: the spindle oriented (M19) before a load
        u = np.array([0.0, math.cos(a), math.sin(a)])
        jv = box(x_face - 20, x_face + 25, -14, 14, jr, jr + 40)
        R = np.column_stack([[1.0, 0, 0], np.cross(u, [1.0, 0, 0]), u])
        out[f"chuck jaw {k + 1}"] = Part(jv.transform(T((0, ys, zs), R), inplace=False), C["steel"], group="spindle")
    tx, ty, tz_ = x_face + 470.0, ys + 300.0, zs + 160.0
    out["turret (12-station)"] = Part(merge([cyl((tx - 70, ty, tz_), (tx + 70, ty, tz_), 175.0, res=12),
                                             cyl((tx + 70, ty, tz_), (tx + 160, ty, tz_), 110.0)]), "#b0b6bc")
    out["turret tools"] = Part(merge([box(tx - 20, tx + 20, ty - 230, ty - 170, tz_ - 30, tz_ + 30),
                                      cyl((tx - 140, ty - 120, tz_ - 120), (tx, ty - 120, tz_ - 120), 12.0)]), C["tool"])
    out["cross slide"] = Part(box(tx - 140, tx + 260, ty + 60, D - t - 10, tz_ - 260, tz_ + 240), "#4a4f54")
    parts = placed(out, S)
    meta = dict(chuck_face=(0.0, ys, zs), door=(dx0 - x_face, dx1 - x_face, dz0, dz1), spin_y=ys, spin_z=zs,
                x_face_pr318=x_face, W=W, D=D)
    return parts, meta


# ================================================================================================ Hyd-Mech S-20A
def s20a(head=1.0, vise_open=60.0, bar=None):
    """Hyd-Mech S-20A automatic scissor bandsaw: the bar runs along x (fed from -x), the blade cuts across it at x = 0;
    the robot works from the front (y = 0). head: 1 raised .. 0 through the cut. bar: (L, W, H) of the bar in the vise."""
    tz = 787.0                                                # table height (published, 31 in.)
    out = {}
    out["saw base cabinet"] = Part(merge([box(-900, 700, 120, 1050, 80, tz - 60), box(-960, 760, 80, 1090, 0, 80)]), C["saw"])
    out["saw bed"] = Part(box(-420, 420, 150, 760, tz - 60, tz), C["steel"])
    out["saw fixed jaw"] = Part(box(-330, 330, 640, 700, tz, tz + 340), C["saw"])
    out["saw moving jaw"] = Part(box(-330, 330, 640 - vise_open - 60 - (bar[1] if bar else 0), 640 - vise_open - (bar[1] if bar else 0),
                                     tz, tz + 340), C["saw"])
    out["shuttle vise"] = Part(box(-880, -480, 200, 720, tz, tz + 260), "#3a7a55")
    out["infeed roller table"] = Part(merge([box(-3000, -920, 280, 640, tz - 75, tz - 60)] +
                                            [box(x - 25, x + 25, 300, 620, 0, tz - 75) for x in (-2900, -1900, -1000)]),
                                      C["steel"])
    out["infeed rollers"] = Part(merge([cyl((x, 300, tz - 30), (x, 620, tz - 30), 30.0, res=16)
                                        for x in np.arange(-2950, -950, 300)]), "#c0c6cc")
    out["outfeed table"] = Part(box(450, 1400, 280, 640, tz - 40, tz - 10), C["steel"])
    # the head: a C-frame pivoting about a hinge behind the vise (y 1000, z tz + 120); raised 35 deg at head = 1
    hinge = np.array([0.0, 1000.0, tz + 120.0])
    ang = 35.0 * head
    hm = merge([box(-980, 980, 520, 980, tz + 60, tz + 420),           # the beam
                cyl((-760, 520, tz + 240), (-760, 980, tz + 240), 260.0, res=40),   # wheel covers
                cyl((760, 520, tz + 240), (760, 980, tz + 240), 260.0, res=40),
                box(-30, 30, 980, 1030, tz + 80, tz + 400)])
    blade = merge([box(-560, 560, 690, 700, tz - 20, tz + 10), box(-560, -520, 690, 700, tz - 20, tz + 260),
                   box(520, 560, 690, 700, tz - 20, tz + 260)])
    Mh = about(Rx(ang), hinge)
    out["saw head"] = Part(hm, C["saw"], M=Mh, group="head")
    out["saw blade (1 in.)"] = Part(blade, C["saw_blade"], M=Mh, group="head")
    out["blade guards"] = Part(merge([box(-560, -470, 640, 760, tz + 10, tz + 300), box(470, 560, 640, 760, tz + 10, tz + 300)]),
                               "#e5b400", M=Mh, group="head")
    out["hydraulic cylinder"] = Part(cyl((0, 1080, tz - 200), (0, 1000, tz + 200), 45.0), C["dark"], collide=False)
    out["saw control box"] = Part(box(800, 1150, 120, 300, tz + 100, tz + 700), C["saw"])
    out["coolant tray"] = Part(box(-500, 500, 140, 780, tz - 140, tz - 60), "#2a2e33", collide=False)
    return out, dict(bed_z=tz, hinge=hinge, jaw_y=640.0)


# ================================================================================================ jib + vacuum lifter
JIB = dict(under_boom=8 * 12 * INCH, span=14 * 12 * INCH, mast_r=110.0, boom_h=200.0)


MACHINE_JIB = dict(under_boom=1700.0, span=2400.0, mast_r=90.0, boom_h=150.0)   # a jib on its own mast beside the VF-4's
# door, its boom low enough (1700-1850 mm) to swing in under the 1900 mm header, so the tube lifter sets a block on the
# table from in front (our assumption: the free-standing jib of robot-shop-equipment.csv built to a 1700 mm height; a
# tube lifter can't come down through the VF-4's roof, and a person can't guide a load lifted over a 2 m enclosure)


def jib_lifter(yaw=0.0, r=1800.0, hook_z=1200.0, load=None, grip=True, J=None):
    """A free-standing jib (Gorbel WSJ360 class; JIB: 8 ft under the boom, 14 ft span; MACHINE_JIB: the low one beside the
    VF-4) with a Schmalz JumboFlex 50 vacuum tube lifter on its trolley. Frame: the mast's foot at the origin. yaw (deg)
    turns the boom about the mast (0 = along +x); r: trolley radius (mm); hook_z: the suction foot's face (mm above the
    floor). Returns parts and the foot's pose."""
    J = J or JIB
    ub, span = J["under_boom"], J["span"]
    out = {}
    low = ub < 2000.0
    mast_top = ub + J["boom_h"] + (450.0 if low else 120.0)
    out["jib base plate"] = Part(box(-450, 450, -450, 450, 0, 40), C["yellow"])
    out["jib mast"] = Part(cyl((0, 0, 40), (0, 0, mast_top), J["mast_r"], res=32), C["yellow"])
    Mb = T((0, 0, 0), Rz(yaw))
    # a knee brace under a tall boom; a tie rod from the mast's top over a low one (nothing hangs into the work zone)
    brace = (_slab((80, mast_top - 30), (0.6 * span, ub + J["boom_h"] + 5), 14.0, -15, 15) if low else
             _slab((150, ub - 20), (1100, ub - 650), 30.0, -40, 40))
    boom = merge([box(0, span, -60, 60, ub, ub + J["boom_h"]), box(-120, 120, -120, 120, ub - 40, ub + J["boom_h"] + 40),
                  brace])
    out["jib boom (enclosed track)"] = Part(boom, C["yellow"], M=Mb, group="boom")
    out["vacuum blower"] = Part(box(250, 650, -250, 250, 40, 520), "#2f5f8a")
    out["vacuum hose up the mast"] = Part(cyl((300, 0, 520), (300, 0, ub - 100), 40.0), C["rubber"], collide=False)
    # trolley, the lifting tube (it shortens as it lifts), the handle and the suction foot
    tr = np.array([r, 0.0, ub])
    tube_top = ub - 60.0
    tube_bot = hook_z + 260.0
    lift = merge([box(r - 90, r + 90, -80, 80, ub - 60, ub), cyl((r, 0, tube_bot), (r, 0, tube_top), 80.0, res=32)])
    handle = merge([box(r - 160, r + 160, -60, 60, hook_z + 120, hook_z + 260), cyl((r - 120, 0, hook_z + 200), (r - 420, 0, hook_z + 330), 18.0),
                    box(r - 460, r - 400, -40, 40, hook_z + 300, hook_z + 380)])
    foot = merge([box(r - 200, r + 200, -130, 130, hook_z + 30, hook_z + 120), box(r - 190, r + 190, -120, 120, hook_z, hook_z + 30)])
    out["JumboFlex lifting tube"] = Part(lift, "#3b4148", M=Mb, group="boom")
    out["JumboFlex handle"] = Part(handle, "#2f5f8a", M=Mb, group="boom")
    out["suction foot (block)"] = Part(foot, C["dark"], M=Mb, group="boom")
    foot_pose = Mb @ T((r, 0.0, hook_z))
    return out, dict(foot=foot_pose, handle=Mb @ T((r - 430, 0.0, hook_z + 340)), trolley=Mb @ T(tr))


# ================================================================================================ pallet, jack, lift table
def pallet(L=48 * INCH, W=40 * INCH, H=144.0):
    """GMA 48 x 40 in. stringer pallet: 7 top boards, 3 stringers, 5 bottom boards. Frame: centre of its footprint."""
    out = []
    bt, bw = 16.0, 140.0
    for k in range(7):
        x = -L / 2 + bw / 2 + k * (L - bw) / 6
        out.append(box(x - bw / 2, x + bw / 2, -W / 2, W / 2, H - bt, H))
    for y in (-W / 2 + 19, 0.0, W / 2 - 19):
        out.append(box(-L / 2, L / 2, y - 19, y + 19, bt, H - bt))
    for k in range(5):
        x = -L / 2 + bw / 2 + k * (L - bw) / 4
        out.append(box(x - bw / 2, x + bw / 2, -W / 2, W / 2, 0, bt))
    return {"pallet": Part(merge(out), C["wood"])}


def pallet_jack(raise_mm=0.0, handle_deg=10.0):
    """A manual pallet jack, 27 x 48 in. forks, 2.9 in. lowered: forks along +x from the pump at x = 0."""
    fl, fw, ow = 48 * INCH, 7 * INCH, 27 * INCH
    z0 = 2.9 * INCH + raise_mm
    out = {}
    forks = [box(0, fl, y - fw / 2, y + fw / 2, z0 - 50, z0) for y in (-(ow - fw) / 2, (ow - fw) / 2)]
    forks += [cyl((fl - 60, y, 40), (fl - 60, y + 40, 40), 40.0, res=16) for y in (-(ow - fw) / 2 - 20, (ow - fw) / 2 - 20)]
    out["pallet jack forks"] = Part(merge(forks), C["red"])
    out["pallet jack pump"] = Part(merge([box(-200, 40, -260, 260, 60, z0 + 120), cyl((-120, -40, 0 + 90), (-120, 40, 90), 90.0, res=20)]),
                                   C["red"])
    a = math.radians(handle_deg)
    hx, hz = -120 - 1150 * math.sin(a), 230 + 1150 * math.cos(a)
    out["pallet jack handle"] = Part(merge([cyl((-120, 0, 230), (hx, 0, hz), 16.0), box(hx - 20, hx + 20, -150, 150, hz - 20, hz + 20)]),
                                     C["red"])
    return out, dict(handle=(hx, 0.0, hz))


def lift_table(top_z=760.0):
    """Vestil SCTAB-1000-2040-AC: 20 x 40 in. platform (here 1016 along x), electric scissor; frame: centre on the floor."""
    L, W = 40 * INCH, 20 * INCH
    out = {"lift table base": Part(box(-L / 2 + 20, L / 2 - 20, -W / 2 + 20, W / 2 - 20, 0, 70), C["stand"]),
           "lift table platform": Part(box(-L / 2, L / 2, -W / 2, W / 2, top_z - 45, top_z), C["stand"])}
    h = top_z - 115.0
    leg = math.hypot(L - 160, h)
    ang = math.degrees(math.atan2(h, L - 160))
    legs = []
    for y in (-W / 2 + 60, W / 2 - 60):
        for sgn in (1, -1):
            b = box(-leg / 2, leg / 2, -20, 20, -20, 20).transform(T((0, y, 70 + h / 2), Ry(-sgn * ang)), inplace=False)
            legs.append(b)
    out["lift table scissors"] = Part(merge(legs), "#4f565d")
    out["lift table motor"] = Part(box(-200, 100, -150, 150, 70, 250), C["dark"], collide=False)
    return out


# ================================================================================================ TIG welding
def tig_station():
    """TIG welding: a 48 x 36 in. steel table at 36 in., an inverter TIG on a cart, an argon cylinder, a fume arm; the
    person stands at -y (the front). Frame: the table's front edge centre on the floor."""
    tz = 36 * INCH
    L, W = 48 * INCH, 36 * INCH
    out = {"welding table top": Part(merge([box(-L / 2, L / 2, 0, W, tz - 16, tz)] +
                                           [box(-L / 2 + 40 + 100 * k, -L / 2 + 52 + 100 * k, 2, W - 2, tz - 0.5, tz + 0.2)
                                            for k in range(0)]), "#4a4f55"),
           "welding table legs": Part(merge([box(x - 30, x + 30, y - 30, y + 30, 0, tz - 16)
                                             for x in (-L / 2 + 60, L / 2 - 60) for y in (60, W - 60)] +
                                            [box(-L / 2 + 60, L / 2 - 60, 40, W - 40, 150, 180)]), "#3a3f45"),
           "TIG power source on its cart": Part(merge([box(L / 2 + 150, L / 2 + 520, 100, 700, 0, 650),
                                                       box(L / 2 + 180, L / 2 + 490, 150, 650, 650, 1100)]), C["tig"]),
           "argon cylinder": Part(merge([cyl((L / 2 + 330, 800, 30), (L / 2 + 330, 800, 1450), 115.0), cyl((L / 2 + 330, 800, 1450), (L / 2 + 330, 800, 1560), 40.0)]),
                                  C["argon"]),
           "fume extractor arm": Part(merge([cyl((-L / 2 - 200, W + 150, 0), (-L / 2 - 200, W + 150, 2100), 50.0),
                                             cyl((-L / 2 - 200, W + 150, 2100), (-200, W / 2, 1500), 60.0),
                                             cyl((-200, W / 2, 1500), (-100, W / 2 - 50, 1250), 110.0)]), C["yellow"], collide=False),
           "welding curtain": Part(box(-L / 2 - 400, L / 2 + 800, W + 300, W + 310, 0, 1900), "#c0392b", opacity=0.55, collide=False)}
    return out, dict(top_z=tz)


# ================================================================================================ wash, deburr, measuring
def bench(w=1830.0, d=760.0, h=860.0, top=C["wood"]):
    out = {"bench top": Part(box(-w / 2, w / 2, 0, d, h - 40, h), top),
           "bench frame": Part(merge([box(sx * (w / 2 - 50) - 25, sx * (w / 2 - 50) + 25, y - 25, y + 25, 0, h - 40)
                                      for sx in (-1, 1) for y in (40, d - 40)] + [box(-w / 2 + 30, w / 2 - 30, 60, d - 60, 120, 150)]),
                                C["stand"])}
    return out


def wash_deburr(lid_open=True, basket_up=0.0):
    """Deburr and wash bench: the Crest Powersonic 7 gal tank (19.5 x 11.75 x 8 in. inside) at the left with its basket,
    a rinse tank, the ATI compliant deburr spindle on a fixed stand and a brush wheel at the right, a drying air knife.
    Frame: the bench's front edge centre on the floor (robot at -y)."""
    h = 860.0
    out = bench(2400.0, 760.0, h)
    ti, tw, td = 19.5 * INCH, 11.75 * INCH, 8 * INCH
    x0, y0 = -1100.0, 180.0
    out["ultrasonic tank (Crest 7 gal)"] = Part(merge([open_box(x0, x0 + ti + 90, y0, y0 + tw + 90, h, h + td + 120, 45.0),
                                                       box(x0, x0 + ti + 90, y0 - 60, y0, h, h + 140)]), C["tank"])
    out["tank water"] = Part(box(x0 + 45, x0 + 45 + ti, y0 + 45, y0 + 45 + tw, h + 60, h + td + 40), C["water"], opacity=0.55,
                             collide=False)
    bz = h + 80 + basket_up
    out["parts basket"] = Part(open_box(x0 + 60, x0 + 30 + ti, y0 + 60, y0 + 30 + tw, bz, bz + 150, 4.0), "#9aa3ab")
    out["basket handle"] = Part(merge([box(x0 + 45 + ti / 2 - 10, x0 + 45 + ti / 2 + 10, y0 + 60, y0 + 30 + tw, bz + 190, bz + 210),
                                       box(x0 + 45 + ti / 2 - 10, x0 + 45 + ti / 2 + 10, y0 + 60, y0 + 70, bz + 150, bz + 200),
                                       box(x0 + 45 + ti / 2 - 10, x0 + 45 + ti / 2 + 10, y0 + 20 + tw, y0 + 30 + tw, bz + 150, bz + 200)]),
                                "#9aa3ab")
    if lid_open:
        out["tank lid (open)"] = Part(box(x0, x0 + ti + 90, y0 + tw + 90, y0 + tw + 110, h + td + 120, h + td + 120 + tw), C["tank"])
    xr = x0 + ti + 90 + 60                            # the rinse tank: the basket goes from the ultrasonic tank into it
    out["rinse tank"] = Part(open_box(xr, xr + 540, y0, y0 + 340, h, h + 260, 20.0), "#9aa7b3")
    out["rinse water"] = Part(box(xr + 20, xr + 520, y0 + 20, y0 + 320, h + 40, h + 200), C["water"], opacity=0.5, collide=False)
    # deburr: ATI compliant spindle pointing up on a stand, a brush wheel on a motor, a hood behind
    xd = 450.0
    out["deburr spindle stand"] = Part(merge([box(xd - 90, xd + 90, 250, 430, h, h + 160)]), C["stand"])
    out["ATI compliant deburr spindle"] = Part(merge([cyl((xd, 340, h + 160), (xd, 340, h + 330), 38.0), cyl((xd, 340, h + 330), (xd, 340, h + 365), 6.0)]),
                                               "#c0c6cc")
    out["brush wheel motor"] = Part(merge([box(xd + 230, xd + 470, 250, 430, h, h + 180)]), "#7b5ea7")
    out["brush wheel"] = Part(cyl((xd + 200, 340, h + 300), (xd + 240, 340, h + 300), 75.0), "#a58bd0")
    out["brush shaft"] = Part(cyl((xd + 240, 340, h + 300), (xd + 330, 340, h + 300), 12.0), C["steel"], collide=False)
    out["dust hood"] = Part(box(xd - 150, xd + 520, 560, 600, h, h + 520),
                            "#6d7a86")
    out["drying air knife"] = Part(box(950, 1150, 200, 620, h, h + 300), "#6d7a86")
    return out, dict(top_z=h, tank=(x0 + 45 + ti / 2, y0 + 45 + tw / 2, h + td + 120), basket_handle_z=bz + 200, rinse=(xr + 270, y0 + 170, h + 20),
                     deburr_tip=(xd, 340, h + 365), brush=(xd + 200, 340, h + 300))


def granite_station():
    """Measuring: a 36 x 24 x 4 in. grade A granite plate on its stand (36 in. work height), a Mitutoyo height gauge, a
    dial bore gauge on a stand with its setting ring. Frame: the plate's front edge centre on the floor."""
    L, W, Tk = 36 * INCH, 24 * INCH, 4 * INCH
    top = 36 * INCH
    out = {"granite stand": Part(merge([box(-L / 2 + 40, L / 2 - 40, 40, W - 40, 0, 60)] +
                                       [box(x - 30, x + 30, y - 30, y + 30, 0, top - Tk) for x in (-L / 2 + 80, L / 2 - 80)
                                        for y in (80, W - 80)] + [box(-L / 2 + 50, L / 2 - 50, 50, W - 50, top - Tk - 50, top - Tk)]),
                                 C["stand"]),
           "granite surface plate": Part(box(-L / 2, L / 2, 0, W, top - Tk, top), C["granite"])}
    hx, hy = 250.0, 380.0
    out["height gauge base"] = Part(box(hx - 60, hx + 60, hy - 100, hy + 100, top, top + 45), C["gauge"])
    out["height gauge column"] = Part(box(hx - 20, hx + 20, hy + 40, hy + 80, top + 45, top + 560), C["gauge"])
    out["height gauge slider and display"] = Part(box(hx - 45, hx + 45, hy - 10, hy + 90, top + 180, top + 290), "#2c3e50")
    out["height gauge scriber"] = Part(box(hx - 8, hx + 8, hy - 140, hy - 10, top + 200, top + 212), C["gauge"])
    bx, by = -300.0, 420.0
    out["bore gauge stand"] = Part(merge([box(bx - 60, bx + 60, by - 60, by + 60, top, top + 25), cyl((bx, by, top + 25), (bx, by, top + 300), 12.0)]),
                                   C["stand"])
    out["bore gauge (dial, 35-60 mm)"] = Part(merge([cyl((bx + 60, by, top + 120), (bx + 60, by, top + 380), 8.0),
                                                     cyl((bx + 60, by - 15, top + 400), (bx + 60, by + 15, top + 400), 30.0)]), C["gauge"])
    out["setting ring (50.80 mm)"] = Part(tube((bx + 150, by + 40, top), (bx + 150, by + 40, top + 25), 45.0, 25.4), C["steel"])
    return out, dict(top_z=top)


# ================================================================================================ robot tool stand
def tool_stand(present=("2F-85", "3FG15", "VGP20", "blow-off gun", "nut runner")):
    """The robots' tool stand: a post and a shelf of nests at 900 mm, one tool on an ATI QC-11 tool plate in each.
    Frame: the stand's front face centre on the floor (robot at -y). `present`: the tools parked in it now."""
    sz = 900.0
    out = {"tool stand frame": Part(merge([box(-700, 700, 60, 360, 0, 40), box(-40, 40, 160, 260, 40, sz - 30),
                                           box(-700, 700, 60, 360, sz - 30, sz)]), C["stand"])}
    nests = dict(zip(("2F-85", "3FG15", "VGP20", "blow-off gun", "nut runner"), (-560.0, -280.0, 0.0, 280.0, 560.0)))
    for name, x in nests.items():
        out[f"nest {name}"] = Part(merge([box(x - 70, x - 45, 60, 300, sz, sz + 60), box(x + 45, x + 70, 60, 300, sz, sz + 60)]),
                                   "#d9b23a")
        if name not in present:
            continue
        plate = cyl((x, 180, sz + 60), (x, 180, sz + 82), 32.0)
        if name == "2F-85":
            body = merge([box(x - 37, x + 37, 140, 220, sz + 82, sz + 82 + 95), box(x - 42, x - 30, 160, 200, sz + 82 + 95, sz + 82 + 150),
                          box(x + 30, x + 42, 160, 200, sz + 82 + 95, sz + 82 + 150)])
            col = C["dark"]
        elif name == "3FG15":
            body = merge([cyl((x, 180, sz + 82), (x, 180, sz + 82 + 75), 78.0, res=40)] +
                         [box(-8, 8, 50, 70, 0, 90).transform(T((x, 180, sz + 82 + 75), Rz(120 * k)), inplace=False) for k in range(3)])
            col = "#3c4650"
        elif name == "VGP20":
            body = merge([box(x - 92, x + 92, 180 - 132 + 60, 180 + 132 - 60, sz + 82, sz + 82 + 92)] +
                         [cyl((x + dx, 180 + dy, sz + 82 + 92), (x + dx, 180 + dy, sz + 82 + 112), 18.0, res=20)
                          for dx in (-50, 50) for dy in (-45, 45)])
            col = "#33373b"
        elif name == "blow-off gun":
            body = merge([box(x - 25, x + 25, 150, 210, sz + 82, sz + 82 + 110), cyl((x, 180, sz + 82 + 110), (x, 180, sz + 82 + 230), 5.0)])
            col = "#c0392b"
        else:
            body = merge([cyl((x, 180, sz + 82), (x, 180, sz + 82 + 220), 30.0), cyl((x, 180, sz + 82 + 220), (x, 180, sz + 82 + 280), 5.0)])
            col = "#e0a526"
        out[f"tool plate {name}"] = Part(plate, "#9aa3ab")
        out[f"tool {name}"] = Part(body, col)
    return out, dict(nests=nests, top_z=sz)


def gripper_3fg15(open_d=120.0):
    """OnRobot 3FG15 in the tool0 frame (z along the tool axis): a 156 mm puck (est.) and three fingers on a circle of
    diameter open_d (external grip 4-152 mm, published)."""
    body = cyl((0, 0, 0), (0, 0, 75), 78.0, res=40)
    fingers = []
    for k in range(3):
        a = math.radians(90 + 120 * k)
        r = open_d / 2 + 10
        fingers.append(box(-9, 9, -10, 10, 75, 165).transform(T((r * math.cos(a), r * math.sin(a), 0), Rz(math.degrees(a))), inplace=False))
    return {"3FG15 body": Part(body, "#3c4650"), "3FG15 fingers": Part(merge(fingers), "#9aa3ab")}, dict(tcp=150.0)


# ================================================================================================ stock and rack
def cantilever_rack(bars=True):
    """McMaster 4849T1 single-sided cantilever rack: 82 W x 96 H x 40 D in., 4 levels, 24 in. arms (the arms point at
    the aisle, -y). Frame: the arms' tips' line centre on the floor."""
    Wr, Hr, Dr = 82 * INCH, 96 * INCH, 40 * INCH
    arm = 24 * INCH
    out = {"rack base": Part(merge([box(x - 50, x + 50, 0, Dr, 0, 100) for x in (-Wr / 2 + 50, Wr / 2 - 50)]), C["orange"]),
           "rack columns": Part(merge([box(x - 50, x + 50, Dr - 200, Dr - 50, 100, Hr) for x in (-Wr / 2 + 50, Wr / 2 - 50)] +
                                      [box(-Wr / 2 + 50, Wr / 2 - 50, Dr - 160, Dr - 90, z, z + 40) for z in (900, 1800)]),
                            C["orange"])}
    levels = (450.0, 950.0, 1450.0, 1950.0)
    arms = []
    for z in levels:
        for x in (-Wr / 2 + 50, Wr / 2 - 50):
            arms.append(box(x - 40, x + 40, Dr - 200 - arm, Dr - 200, z - 60, z))
    out["rack arms"] = Part(merge(arms), C["orange"])
    if bars:
        b = []
        for i, (r_, z) in enumerate(((54.0, 950.0), (54.0, 1450.0), (108.0, 1450.0), (86.0, 1950.0))):
            b.append(cyl((-Wr / 2 + 20, Dr - 300 - i * 25 - r_, z + r_ / 2), (Wr / 2 - 20, Dr - 300 - i * 25 - r_, z + r_ / 2), r_ / 2))
        out["bar stock (6061, 316)"] = Part(merge(b), C["alu"])
    return out, dict(levels=levels, tip_y=Dr - 200 - arm)


def box_mesh_with_tape(L, W, H, open_flaps=0.0):
    """A shipping box: body, the tape seam along x on top, and the two long top flaps (open_flaps 0 shut .. 1 open,
    folded out to the sides about their hinges on the long edges)."""
    body = open_box(-L / 2, L / 2, -W / 2, W / 2, 0, H - 2, 4.0)     # corrugated board, 4 mm
    tape = box(-L / 2 - 1, L / 2 + 1, -24, 24, H - 2, H + 0.5)
    a = 120.0 * open_flaps
    flaps = []
    for sgn in (-1, 1):
        f = box(-L / 2, L / 2, -W / 2 if sgn > 0 else 0.0, 0.0 if sgn > 0 else W / 2, -1.5, 1.5)
        # hinge on the long edge at y = sgn * W / 2: the flap lies from the hinge towards the middle when shut
        Mf = T((0, sgn * W / 2, H)) @ T((0, 0, 0), Rx(sgn * a)) @ T((0, -sgn * W / 2, 0))
        flaps.append(f.transform(Mf, inplace=False))
    return {"box": Part(body, C["box"]), "tape": Part(tape, "#d8c9a3", collide=False), "flaps": Part(merge(flaps), "#c09a64")}
