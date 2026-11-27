"""Bought parts of the fast-track machines drawn to the makers' dimensions (#260, PR 294 round 2).

Each builder draws a bought part from the numbers measured on the maker's STEP file (or read off its drawing) in our
own code; no vendor geometry is copied or committed. The STEP files are fetched into /tmp/ft-vcad/ and listed, with
their URL and sha256, in vendor-cad-manifest.csv.

    python desktop-lpbf/fast-track/cad/ft_vendor.py measure FILE [--faces AXIS SIDE]   # bbox, volume, faces, holes
    python desktop-lpbf/fast-track/cad/ft_vendor.py verify [key ...]                    # ours vs the vendor STEP

verify() compares each builder with the vendor's STEP by volume and by the sorted bounding-box extents, as
desktop-lpbf/cad/vendor_parts.py does. Our shapes are outer envelopes with the mounting features (holes, faces,
connector positions) at the measured places; their volume is larger where the vendor's part is hollow.

Every builder states its local frame. Units mm.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import cadquery as cq

HERE = pathlib.Path(__file__).resolve().parent
V = cq.Vector
IN = 25.4
VCAD = pathlib.Path("/tmp/ft-vcad")
OUT = HERE / "out"


# --------------------------------------------------------------------------------------------------
# helpers (local, so this file does not depend on ft_model)
# --------------------------------------------------------------------------------------------------
def _box(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def _cyl(r, p0, d, h):
    return cq.Solid.makeCylinder(r, h, V(*p0), V(*d))


def _rbox(x0, x1, y0, y1, z0, z1, r):
    w = cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
    if r > 0:
        w = w.edges("|Z").fillet(r)
    return w.val().translate(V(x0, y0, z0))


def _fuse(shapes):
    out = shapes[0]
    for s in shapes[1:]:
        out = out.fuse(s)
    return out.clean()


def _holes(shape, pts, r, z0, depth, d=(0, 0, 1)):
    for (x, y) in pts:
        shape = shape.cut(_cyl(r, (x, y, z0), d, depth))
    return shape


# --------------------------------------------------------------------------------------------------
# Sources: what each builder is drawn from
# --------------------------------------------------------------------------------------------------
SOURCES = {
    "zaber_x_vsr20a": dict(
        vendor="Zaber", pn="X-VSR20A-E01", file="X-VSR20A-E01.step",
        url="https://www.zaber.com/fs/series/X-VSR-E/7/X-VSR20A-E01/docs/X-VSR20A-E01.step",
        dims="measured on the STEP (2026-11-27): 88.0 x 101.0 x 73.0 mm retracted. Lift section 64 x 64 mm; base face "
             "64 x 64 with M6 clearance holes (6.6) on a 50 mm square (and 1/4 in. on 2 in.); drive housing 60 x 43.5 x "
             "21 mm on one side, 1 mm clear of the base plane, two bosses to 69 mm; M8 connector 15 mm out on the other "
             "side. Platform 64 x 64 x 7, R6.5 corners, top at 73.0: M6 tapped (5.0) on a 12.5/25 mm grid (12), M3 "
             "(2.5) at (+-10, +-10) and (+-16, +-16), M4 (3.3) at the centre. Datasheet (lead, 2026-11-27): 20 mm "
             "travel, 100 N centred load, 100 N continuous thrust, 3 N m moment, 48 mm/s, 0.609 kg"),
    "zaber_x_lsm100": dict(
        vendor="Zaber", pn="X-LSM100B-E03 (body from the X-LSM100A-E03 STEP)", file="X-LSM100A-E03.step",
        url="https://www.zaber.com/products/linear-stages/X-LSM-E/documents (X-LSM100A-E03.step)",
        dims="measured on the X-LSM100A-E03 STEP (2026-11-27; Zaber offers no STEP of the B, which the lead read as "
             "the same body with a faster lead screw): 239.2 long x 21.0 tall x 84.8 wide incl. the controller and its "
             "connectors. Channel 45 wide, 152 long; end cap 8.2; motor 20 x 20 and controller box 42.6 x 64 x 20.3 "
             "at one end, the box 40 mm to one side of the channel, two M8 connectors on its side and one on its end. "
             "Carriage 44 x 48.3, top 21.0 above the base: M3 grid (2.5) at 10 mm pitch, 4 x 4 at +-5/+-15, plus "
             "(+-10, 20); M4 at its centre. Base: M3 slots (3.6) at +-10 mm across, every 20 mm along. Datasheet "
             "(lead): 101.6 mm travel, 104 mm/s, 25 N continuous thrust, 250 N centred load, 4 N m pitch, 0.39 kg"),
    "zaber_x_lsq": dict(
        vendor="Zaber", pn="X-LSQ075B-E01 / X-LSQ150B-E01 (rejected)", file="X-LSQ075B-E01.step",
        url="https://www.zaber.com/products/linear-stages/X-LSQ-E/documents",
        dims="measured on the STEPs (2026-11-27): X-LSQ075B 285.85 x 65.0 x 43.1; X-LSQ150B 360.9 x 65.0 x 43.1. "
             "Envelope only: kept to show why it was dropped"),
    "scanlab_hurryscan25": dict(
        vendor="SCANLAB", pn="hurrySCAN 25 (drawn as the hurrySCAN 20/30 housing)", file="SCANLAB-hurrySCAN-EN.pdf",
        url="https://www.scanlab.de/sites/default/files/2026-11/SCANLAB-hurrySCAN-EN.pdf",
        dims="drawing p. 3: housing 206.9 x 140 x 180, entrance-face mounting (customer flange, M6 screws, Ø6 h6 "
             "pins), objective under the housing near the entrance end, beam displacement 25.25 (20) / 35.53 (30); "
             "measured off the bottom view: objective 57.3 from the entrance face, 55.1 / 84.9 from the sides. "
             "Estimates: the 25 uses this housing; displacement 30.4; input 43.5 above the bottom face. 5.8 kg"),
    "linos_ftheta_254": dict(
        vendor="Excelitas (LINOS)", pn="F-Theta-Ronar 4401-288-000-20", file="4401-288-000-20_2021.12-V4.pdf",
        url="https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/1068/4401-288-000-20_2021.12-V4.pdf",
        dims="datasheet: EFL 254.4, WD 296.2, FFL 344.8, body Ø118, knurled ring Ø119.8, length 69.2 incl. a 20.5 "
             "nose with the M85 x 1 thread, 1340 g, scan angle +-17.7 deg, field 157 x 157, design beam 20 mm"),
    "saginaw_16el1208sslp": dict(
        vendor="Saginaw Control & Engineering", pn="SCE-16EL1208SSLP", file="saginaw_16el1208sslp_drawing.pdf",
        url="https://asset.solutionsdirectonline.com/doc/Saginaw_Control_Engineering/saginaw_16el1208sslp_drawing.pdf",
        dims="drawing: body 16.00 x 12.00 x 8.00 in, 0.075 in 304, door 15.50 x 11.63 in, usable depth 8.30 in, "
             "quarter-turn latch, concealed hinges, poured gasket, panel studs 11.25 x 7.25 in, mounting holes Ø0.44 at "
             "14.50 x 10.50 in. Estimates: rim lip 22 mm, gasket 8 x 4, studs #10 x 12.7, hinge and latch bodies"),
    "thorlabs_mts50_z8": dict(
        vendor="Thorlabs", pn="MTS50/M-Z8", file="MTS50_M-Z8-Step.step",
        url="https://www.thorlabs.com/item/MTS50_M-Z8 (Step: 19760-E0W.step)",
        dims="measured on the STEP (2026-11-27): 163.45 long x 43.0 wide x 22.0 tall. Base 43 x 160.8 x 10.5; motor "
             "cover 43 x 78 x 12.5 at the rear (top at 22.0); carriage 43 x 43, top 22.0, at the rear end of its 50 mm "
             "travel in the file (centre 60.3 mm from the front end)"),
}


# --------------------------------------------------------------------------------------------------
# Zaber X-VSR20A-E01, vertical lift stage
# --------------------------------------------------------------------------------------------------
VSR = dict(sq=64.0, r=6.5, h=73.0, plat_t=7.0, base_h=20.0, travel=20.0,
           housing=(-19.0, 41.0, -59.5, -16.0, 1.0, 22.0),       # x0, x1, y0, y1, z0, z1 (local)
           conn=(41.0, 56.0, -50.5, -35.5, 5.7, 20.7), boss=((4.8, 14.8, -69.0, -59.5, 7.3, 18.3),
                                                             (19.0, 30.1, -66.0, -59.5, 6.7, 18.9)),
           m6_grid=[(x, y) for x in (-25.0, -12.5, 12.5, 25.0) for y in (-25.0, -12.5, 12.5, 25.0)
                    if abs(x) == 25.0 or abs(y) == 25.0],
           m3=[(sx * a, sy * a) for a in (10.0, 16.0) for sx in (-1, 1) for sy in (-1, 1)],
           base_holes=[(sx * 25.0, sy * 25.0) for sx in (-1, 1) for sy in (-1, 1)])


def zaber_x_vsr20a(lift=0.0, parts=False):
    """X-VSR20A-E01. Local frame: base face on z = 0, platform centre on the z axis, platform top at 73 + lift.
    The drive housing sits toward -y, the M8 connector toward +x (the STEP's y up -> z, its z -> -y).
    parts=True returns (fixed, moving) shapes."""
    s, r, h = VSR["sq"], VSR["r"], VSR["h"]
    base = _rbox(-s / 2, s / 2, -s / 2, s / 2, 0.0, VSR["base_h"], r)
    base = _holes(base, VSR["base_holes"], 3.3, -1.0, VSR["base_h"] + 2)
    core = _rbox(-s / 2 + 4, s / 2 - 4, -s / 2 + 4, s / 2 - 4, VSR["base_h"], h - VSR["plat_t"] - 1.0, r - 4 if r > 4 else 1.0)
    hx0, hx1, hy0, hy1, hz0, hz1 = VSR["housing"]
    housing = _box(hx0, hx1, hy0, hy1, hz0, hz1)
    conn = _box(*VSR["conn"])
    bosses = [_box(*b) for b in VSR["boss"]]
    fixed = _fuse([base, core, housing, conn] + bosses)
    # moving: the skirt (20 .. 66) and the platform (66 .. 73), both rise by `lift`
    skirt = _rbox(-s / 2, s / 2, -s / 2, s / 2, VSR["base_h"], h - VSR["plat_t"], r).cut(
        _box(-s / 2 + 3, s / 2 - 3, -s / 2 + 3, s / 2 - 3, VSR["base_h"] - 1, h))
    plat = _rbox(-s / 2, s / 2, -s / 2, s / 2, h - VSR["plat_t"], h, r)
    plat = _holes(plat, VSR["m6_grid"], 2.5, h - 10.0, 11.0)
    plat = _holes(plat, VSR["m3"], 1.25, h - 6.0, 7.0)
    plat = plat.cut(_cyl(1.65, (0, 0, h - 8.0), (0, 0, 1), 9.0))
    moving = _fuse([skirt, plat]).translate(V(0, 0, lift))
    if parts:
        return fixed, moving
    return _fuse([fixed, moving])


# --------------------------------------------------------------------------------------------------
# Zaber X-LSM100B-E03, low-profile linear stage (body measured on the X-LSM100A-E03 STEP)
# --------------------------------------------------------------------------------------------------
# local x = STEP z - 78.8 (carriage centre at mid-travel at x = 0), local y = STEP x, local z = STEP y + 10.67
LSM = dict(travel=101.6, h=21.0, w=45.0, ch=(-74.8, 77.2), cap=(77.2, 85.4), endplate=(-78.8, -74.8),
           motor=(-135.3, -78.8), box=(-138.8, -74.8, 10.16, 52.81), conn_end=(-153.8, -138.8, 28.9, 43.9, 5.07, 20.07),
           conn_side=((-108.65, 57.11, 62.31), (-123.35, 57.11, 62.31)),
           car=(-22.5, 25.8, 22.0, 17.27), car_block=(-17.5, 21.3, 17.5, 3.77),
           car_m3=[(x, y) for x in (-15.0, -5.0, 5.0, 15.0) for y in (-15.0, -5.0, 5.0, 15.0)] + [(20.0, -10.0), (20.0, 10.0)],
           base_slots=[(x, y) for x in [9.5 + 20 * k - 78.8 for k in range(8)] for y in (-10.0, 10.0)])


def zaber_x_lsm100(pos=0.0, parts=False):
    """X-LSM100B-E03. Local frame: base on z = 0, travel along +x, the carriage centre (its M4 hole) at x = pos,
    pos in [-50.8, +50.8] (0 = mid-travel). Motor and controller at -x; the controller box and its two M8
    connectors on the +y side. parts=True returns (fixed, carriage)."""
    w, h = LSM["w"], LSM["h"]
    x0, x1 = LSM["ch"]
    ch = _box(x0, x1, -w / 2, w / 2, 0.0, 16.77)
    ch = ch.cut(_box(x0 + 2, x1 - 2, -17.9, 17.9, 3.0, 17.0))                   # the open channel under the carriage
    for (x, y) in LSM["base_slots"]:
        ch = ch.cut(_box(x - 1.8, x + 1.8 + 2.75, y - 1.8, y + 1.8, -1.0, 4.0))
    cap = _box(LSM["cap"][0], LSM["cap"][1], -22.25, 22.25, 0.5, 20.5)
    ep = _box(LSM["endplate"][0], LSM["endplate"][1], -22.2, 42.8, 0.5, 20.75)
    mot = _box(LSM["motor"][0], LSM["motor"][1], -10.0, 10.0, 0.67, 20.67)
    bx0, bx1, by0, by1 = LSM["box"]
    cbox = _box(bx0, bx1, by0, by1, 0.5, 20.75)
    ce = _box(*LSM["conn_end"])
    cs = [_cyl(3.95, (x, y0, 12.2), (0, 1, 0), y1 - y0) for (x, y0, y1) in LSM["conn_side"]]
    fixed = _fuse([ch, cap, ep, mot, cbox, ce] + cs)
    cx0, cx1, cw, cz0 = LSM["car"]
    car = _box(cx0, cx1, -cw, cw, cz0, h)
    bx0_, bx1_, bw_, bz0_ = LSM["car_block"]
    car = car.fuse(_box(bx0_, bx1_, -bw_, bw_, bz0_, cz0))
    car = _holes(car, LSM["car_m3"], 1.25, cz0 - 0.1, 4.0)
    car = car.cut(_cyl(1.65, (0, 0, cz0 - 1.0), (0, 0, 1), 5.0))
    car = car.translate(V(pos, 0, 0))
    if parts:
        return fixed, car
    return _fuse([fixed, car])


def x_lsm100_extent():
    """Overall extents of the X-LSM100 in its local frame (x0, x1, y0, y1, z0, z1)."""
    return (LSM["conn_end"][0], LSM["cap"][1], -LSM["w"] / 2, LSM["conn_side"][0][2], 0.0, LSM["h"])


# --------------------------------------------------------------------------------------------------
# Zaber X-LSQ075B / X-LSQ150B: the rejected recoater stages (envelope at the measured size)
# --------------------------------------------------------------------------------------------------
LSQ = {"X-LSQ075B-E01": (285.85, 65.0, 43.1), "X-LSQ150B-E01": (360.9, 65.0, 43.1)}


def zaber_x_lsq(pn="X-LSQ075B-E01"):
    """Envelope, local frame: base on z = 0, centred on the x axis (length along x)."""
    L, W, H = LSQ[pn]
    return _box(-L / 2, L / 2, -W / 2, W / 2, 0.0, H)


# --------------------------------------------------------------------------------------------------
# Thorlabs MTS50/M-Z8, 50 mm stage with a Z8 DC servo (the PCard route's piston stage, mounted vertically)
# --------------------------------------------------------------------------------------------------
MTS = dict(L=163.45, base_L=160.8, w=43.0, base_h=10.5, h=22.0, motor=(-160.8, -82.8, 9.5), car=43.0, car_home=-60.3,
           travel=50.0, front=2.65)


def thorlabs_mts50_z8(pos=0.0, parts=False):
    """MTS50/M-Z8. Local frame: base on z = 0, travel along +x, front end at x = 0 (the STEP's z), the motor end
    toward -x; carriage centre at x = -60.3 + pos, pos in [0, 50] (0 = the file's position, the rear limit).
    parts=True returns (fixed, carriage). The base has a channel under the carriage and the motor cover is a shell,
    as in the STEP (its solids: base 44.0 cm3, motor cover 11.4 cm3, carriage 12.1 cm3)."""
    w = MTS["w"]
    base = _box(-MTS["base_L"], 0.0, -w / 2, w / 2, 0.0, MTS["base_h"])
    base = base.cut(_box(-82.0, -2.0, -15.0, 15.0, 4.5, MTS["base_h"] + 1))  # lead-screw channel (est. shape)
    m0, m1, mz = MTS["motor"]
    motor = _box(m0, m1, -w / 2, w / 2, mz, MTS["h"]).cut(_box(m0 + 2, m1 - 2, -w / 2 + 2, w / 2 - 2, mz - 1, MTS["h"] - 2))
    tip = _box(-6.0, MTS["front"], -6.0, 6.0, 2.0, 9.0)                       # front stop / bearing housing
    fixed = _fuse([base, motor, tip])
    c = MTS["car"]
    car = _box(-c / 2, c / 2, -w / 2, w / 2, 17.0, MTS["h"])                  # top plate
    car = car.fuse(_box(-c / 2, c / 2, -w / 2, -w / 2 + 4, 10.6, 17.0)).fuse(_box(-c / 2, c / 2, w / 2 - 4, w / 2, 10.6, 17.0))
    for x in (-12.5, 12.5):
        for y in (-12.5, 12.5):
            car = car.cut(_cyl(1.25, (x, y, MTS["h"] - 4.0), (0, 0, 1), 5.0))  # tapped holes on 25 mm (size assumed M3)
    car = car.translate(V(MTS["car_home"] + pos, 0, 0))
    if parts:
        return fixed, car
    return _fuse([fixed, car])


# --------------------------------------------------------------------------------------------------
# SCANLAB hurrySCAN 25 (housing of the hurrySCAN 20/30, which the 25 most likely shares: an assumption)
# --------------------------------------------------------------------------------------------------
# Brochure drawing (SCANLAB-hurrySCAN-EN.pdf p. 3, read 2026-11-27): housing 206.9 (along the input beam) x 140 x 180;
# beam displacement 25.25 mm (20) and 35.53 mm (30). Measured off the drawing's bottom view (scale checked on the
# 206.9/140 ratio, 1.475 vs 1.478): objective axis 57.3 mm from the entrance face, 55.1 and 84.9 mm from the side walls,
# objective bore ~Ø85 (the lens's M85 x 1). Interpolated for the 25 (estimate): displacement 30.4 mm. Input axis height
# above the bottom face (estimate): 43.5 mm = the LINOS nose (20.5) + its recommended Y-mirror distance m2 (23.0).
HS = dict(L=206.9, W=140.0, H=180.0, obj_x=57.3, side_neg=84.9, side_pos=55.1, disp=30.4, in_z=43.5, bore=85.0,
          mass_kg=5.8)


def scanlab_hurryscan25():
    """Local frame: objective axis on the z axis, the housing's bottom face on z = 0 (the lens's flange A seats here),
    the input beam travelling +x into the entrance face at x = -57.3, at y = -30.4 (est.) and z = 43.5 (est.).
    Connectors, as in the seller's photos of this unit (by eye): POWER IN (DB-9), DIGITAL_IN (DB-25) and three push-in
    fittings (water in/out, air) on the -y side face, near the entrance end."""
    L, W, H = HS["L"], HS["W"], HS["H"]
    x0 = -HS["obj_x"]
    y0 = -HS["side_neg"]
    body = _rbox(x0, x0 + L, y0, HS["side_pos"], 0.0, H, 3.0)
    body = body.cut(_cyl(HS["bore"] / 2, (0, 0, -1), (0, 0, 1), 25.0))                 # objective bore (nose goes in)
    body = body.cut(_cyl(9.0, (x0 - 1, -HS["disp"], HS["in_z"]), (1, 0, 0), 15.0))      # entrance aperture
    dsub9 = _box(x0 + 12, x0 + 33, y0 - 8, y0, 150.0, 162.0)
    dsub25 = _box(x0 + 42, x0 + 95, y0 - 8, y0, 150.0, 162.0)
    fit = [_cyl(5.0, (x0 + 120 + 16 * k, y0, 156.0), (0, -1, 0), 16.0) for k in range(3)]  # W in, W out, A
    return _fuse([body, dsub9, dsub25] + fit)


# the unit's input stack, by eye from the seller's photos (2026-11-27): a focusing-lens turret (~Ø50 x 40) on the
# entrance face and a goniometer-adjusted 45 deg input-mirror block (~70 x 70 x 80) on its end, so the beam comes in at
# 90 deg to the entrance axis
HS_IN = dict(turret=(50.0, 40.0), block=(70.0, 70.0, 80.0))


def hurryscan_input_stack(beam_from="-y"):
    """Local frame as scanlab_hurryscan25(). Returns (turret, block); the block's 45 deg mirror sits on the entrance
    axis at x = -57.3 - 40 - 35; beam_from: the side the collimator comes in from ('-y')."""
    d, l = HS_IN["turret"]
    x0 = -HS["obj_x"]
    yc, zc = -HS["disp"], HS["in_z"]
    turret = _cyl(d / 2, (x0 - l, yc, zc), (1, 0, 0), l).cut(_cyl(8.0, (x0 - l - 1, yc, zc), (1, 0, 0), l + 2))
    bx, by, bz = HS_IN["block"]
    xb1 = x0 - l
    blk = _box(xb1 - bx, xb1, yc - by / 2, yc + by / 2, zc - bz / 2, zc + bz / 2)
    blk = blk.cut(_cyl(9.0, (xb1 - bx / 2, yc - by / 2 - 1, zc), (0, 1, 0), by / 2 + 1))   # input port from -y
    blk = blk.cut(_cyl(9.0, (xb1 - bx - 1, yc, zc), (1, 0, 0), bx / 2 + 1))               # back port (coax)
    return turret, blk


# --------------------------------------------------------------------------------------------------
# LINOS F-Theta-Ronar 4401-288-000-20 (f = 254 mm, 1064 nm): datasheet O-LM_DS-4401-288-000-20_2021.12-V4
# --------------------------------------------------------------------------------------------------
LINOS = dict(efl=254.4, bfl=299.1, wd=296.2, ffl=344.8, d=118.0, ring_d=119.8, ring_l=14.0, L=69.2, nose=20.5,
             thread_d=85.0, nose_d=70.0, mass_kg=1.34, m1=25.6, m2=23.0, scan_deg=17.7, field=157.0)


def linos_ftheta_254():
    """Local frame: the mounting flange A (seats on the scan head's bottom face) on z = 0, the lens hanging below it:
    body Ø118 down to the knurled protective-glass ring Ø119.8 x 14 whose bottom is at z = -(FFL - WD) = -48.6; the
    M85 x 1 nose (20.5 long, Ø70 aperture) above z = 0 goes into the head."""
    b = LINOS["ffl"] - LINOS["wd"]                                                     # 48.6 below the flange
    body = _cyl(LINOS["d"] / 2, (0, 0, -b + LINOS["ring_l"]), (0, 0, 1), b - LINOS["ring_l"])
    ring = _cyl(LINOS["ring_d"] / 2, (0, 0, -b), (0, 0, 1), LINOS["ring_l"])
    nose = _cyl(LINOS["thread_d"] / 2, (0, 0, 0), (0, 0, 1), LINOS["nose"] - 4.5).fuse(
        _cyl(LINOS["nose_d"] / 2 + 5, (0, 0, LINOS["nose"] - 4.5), (0, 0, 1), 4.5))
    lens = _fuse([body, ring, nose])
    return lens.cut(_cyl(LINOS["nose_d"] / 2, (0, 0, -b + 3), (0, 0, 1), b + LINOS["nose"]))  # clear aperture


# --------------------------------------------------------------------------------------------------
# Saginaw SCE-16EL1208SSLP, 304 stainless Type 4X wall-mount box, drawn lid-up (its back is our floor)
# --------------------------------------------------------------------------------------------------
# Drawing saginaw_16el1208sslp_drawing.pdf (read 2026-11-27): body 16.00 x 12.00 x 8.00 in, 0.075 in 304; door 15.50 x
# 11.63 in; usable depth 8.30 in; concealed hinges on one long side, one quarter-turn latch on the other; poured-in-place
# gasket; 4 panel studs on the back at 11.25 x 7.25 in; 4 mounting holes Ø0.44 in at 14.50 x 10.50 in, 0.75 in from the
# edges. Estimates (not on the drawing): the rim's inward lip (22 mm, so the door's gasket lands on it), the gasket
# section, the hinge and latch bodies, the studs' length (12.7 mm) and thread (#10).
SAG = dict(out=(16.00 * IN, 12.00 * IN, 8.00 * IN), t=0.075 * IN, door=(15.50 * IN, 11.63 * IN), usable=8.30 * IN,
           lip=22.0, gasket=(8.0, 4.0), studs=(11.25 * IN, 7.25 * IN), stud=(4.8, 12.7), holes=(14.50 * IN, 10.50 * IN),
           hole_d=0.44 * IN, latch_d=25.0, hinge_x=(-120.0, 120.0))


def saginaw_16el1208sslp():
    """Local frame: the inside floor (the back panel's inner face) on z = 0, centred on the z axis; the 16 in side along x,
    the 12 in side along y; hinges on the +y edge, the latch at the middle of the -y edge; the door's inner face at
    z = 8.30 in (210.8). Returns a dict of named shapes."""
    (ox, oy, oz), t = SAG["out"], SAG["t"]
    ix, iy = ox - 2 * t, oy - 2 * t
    rim = oz - t                                                          # 201.3: top of the body's rim
    body = _box(-ox / 2, ox / 2, -oy / 2, oy / 2, -t, rim).cut(_box(-ix / 2, ix / 2, -iy / 2, iy / 2, 0.0, rim + 1))
    lip = SAG["lip"]
    body = body.fuse(_box(-ix / 2, ix / 2, -iy / 2, iy / 2, rim - t, rim).cut(
        _box(-ix / 2 + lip, ix / 2 - lip, -iy / 2 + lip, iy / 2 - lip, rim - t - 1, rim + 1)))
    hx_, hy_ = SAG["holes"][0] / 2, SAG["holes"][1] / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body.cut(_cyl(SAG["hole_d"] / 2, (sx * hx_, sy * hy_, -t - 1), (0, 0, 1), t + 2))
    gw, gh = SAG["gasket"]
    dx, dy = SAG["door"]
    z_g = rim                                                             # poured gasket sits on the lip
    gasket = _box(-dx / 2 + 4, dx / 2 - 4, -dy / 2 + 4, dy / 2 - 4, z_g, z_g + gh).cut(
        _box(-dx / 2 + 4 + gw, dx / 2 - 4 - gw, -dy / 2 + 4 + gw, dy / 2 - 4 - gw, z_g - 1, z_g + gh + 1))
    z_in = SAG["usable"]                                                  # door's inner face (dished panel)
    door = _box(-dx / 2, dx / 2, -dy / 2, dy / 2, z_in, z_in + t)
    door = door.fuse(_box(-dx / 2, dx / 2, -dy / 2, dy / 2, z_g + gh, z_in).cut(
        _box(-dx / 2 + t, dx / 2 - t, -dy / 2 + t, dy / 2 - t, z_g + gh - 1, z_in + 1)))
    ys = -iy / 2 + lip + 8.0                                              # latch shaft, inside the gasket line
    latch = _cyl(SAG["latch_d"] / 2, (0, ys, z_in + t), (0, 0, 1), 10.0).fuse(
        _box(-4, 4, ys - 12, ys + 12, z_in + t + 10, z_in + t + 14))
    latch = latch.fuse(_cyl(4.0, (0, ys, rim - t - 8), (0, 0, 1), z_in - (rim - t - 8)))
    latch = latch.fuse(_box(-8, 8, -iy / 2 + 6, ys + 4, rim - t - 8, rim - t - 1))           # cam behind the lip
    # concealed hinges: inside the opening at the back edge, an arm under the lip to the back wall
    yh = iy / 2 - lip
    hinges = [_box(x - 20, x + 20, yh - 16, yh - 1, rim - 26, z_in).fuse(_box(x - 20, x + 20, yh - 16, iy / 2, rim - 26, rim - t - 1))
              for x in SAG["hinge_x"]]
    sx_, sy_ = SAG["studs"][0] / 2, SAG["studs"][1] / 2
    studs = [_cyl(SAG["stud"][0] / 2, (a * sx_, b * sy_, 0.0), (0, 0, 1), SAG["stud"][1]).fuse(
        _cyl(5.0, (a * sx_, b * sy_, 0.0), (0, 0, 1), 3.0)) for a in (-1, 1) for b in (-1, 1)]
    return dict(body=body, gasket=gasket, door=door, latch=latch, hinges=_fuse(hinges), studs=_fuse(studs),
                rim=rim, lid_in=z_in, lid_out=z_in + t, inside=(ix, iy), opening=(ix - 2 * lip, iy - 2 * lip))


# --------------------------------------------------------------------------------------------------
# measure / verify
# --------------------------------------------------------------------------------------------------
def _load_step(path):
    vals = cq.importers.importStep(str(path)).vals()
    return vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)


def _ext(s):
    b = s.BoundingBox()
    return sorted([round(b.xlen, 2), round(b.ylen, 2), round(b.zlen, 2)])


def measure(path, faces=None):
    """Print what the builders were drawn from: bbox, volume, solids, and (with faces=(axis, side)) the circles on the
    planar faces at that extreme (mounting faces and their holes)."""
    from collections import defaultdict

    from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
    from OCP.GeomAbs import GeomAbs_Circle, GeomAbs_Plane
    s = _load_step(path)
    bb = s.BoundingBox()
    print(json.dumps(dict(file=str(path), bbox=[round(v, 2) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)],
                          ext=[round(bb.xlen, 2), round(bb.ylen, 2), round(bb.zlen, 2)], volume=round(s.Volume(), 1),
                          n_solids=len(s.Solids()))))
    for so in sorted(s.Solids(), key=lambda q: -q.Volume())[:12]:
        b = so.BoundingBox()
        print("  solid", round(so.Volume(), 1), [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)])
    if not faces:
        return
    axis, side = faces
    k = "xyz".index(axis)
    ext = (bb.xmax, bb.ymax, bb.zmax)[k] if side == "max" else (bb.xmin, bb.ymin, bb.zmin)[k]
    for f in s.Faces():
        ad = BRepAdaptor_Surface(f.wrapped)
        if ad.GetType() != GeomAbs_Plane:
            continue
        n = ad.Plane().Axis().Direction()
        if (abs(n.X()), abs(n.Y()), abs(n.Z()))[k] < 0.999:
            continue
        c = f.Center()
        if abs((c.x, c.y, c.z)[k] - ext) > 0.6:
            continue
        fb = f.BoundingBox()
        print(f"  face {axis}={(c.x, c.y, c.z)[k]:.2f} area {f.Area():.0f} x[{fb.xmin:.2f},{fb.xmax:.2f}] "
              f"y[{fb.ymin:.2f},{fb.ymax:.2f}] z[{fb.zmin:.2f},{fb.zmax:.2f}]")
        circ = defaultdict(set)
        for e in f.Edges():
            ca = BRepAdaptor_Curve(e.wrapped)
            if ca.GetType() == GeomAbs_Circle:
                ci = ca.Circle()
                p = ci.Location()
                circ[round(ci.Radius(), 3)].add((round(p.X(), 2), round(p.Y(), 2), round(p.Z(), 2)))
        for r in sorted(circ):
            print(f"    d={2 * r:.2f} n={len(circ[r])}: {sorted(circ[r])}")


BUILDERS = {
    # key: (builder at the vendor file's pose, vendor STEP file, or the drawing's extents where there is no STEP)
    "zaber_x_vsr20a": (lambda: zaber_x_vsr20a(0.0), "X-VSR20A-E01.step"),
    "zaber_x_lsm100": (lambda: zaber_x_lsm100(-50.8), "X-LSM100A-E03.step"),
    "zaber_x_lsq075b": (lambda: zaber_x_lsq("X-LSQ075B-E01"), "X-LSQ075B-E01.step"),
    "zaber_x_lsq150b": (lambda: zaber_x_lsq("X-LSQ150B-E01"), "X-LSQ150B-E01.step"),
    "thorlabs_mts50_z8": (lambda: thorlabs_mts50_z8(0.0), "MTS50_M-Z8-Step.step"),
    # drawings only: the housing / body without connectors, fittings and nose, against the drawing's numbers
    "scanlab_hurryscan25": (lambda: _rbox(-HS["obj_x"], HS["L"] - HS["obj_x"], -HS["side_neg"], HS["side_pos"], 0, HS["H"], 3.0),
                            ("drawing", sorted([HS["L"], HS["W"], HS["H"]]))),
    "linos_ftheta_254": (linos_ftheta_254, ("drawing", sorted([LINOS["ring_d"], LINOS["ring_d"], LINOS["L"]]))),
    "saginaw_16el1208sslp": (lambda: saginaw_16el1208sslp()["body"], ("drawing", sorted([s for s in SAG["out"]]))),
}


def verify(keys=None):
    """Volume and sorted bbox extents of our shapes against the vendor STEP in /tmp/ft-vcad (where it exists), or the
    drawing's overall dimensions. Writes out/vendor-verify.json and returns the rows."""
    OUT.mkdir(exist_ok=True)
    f = OUT / "vendor-verify.json"
    res = [r for r in (json.loads(f.read_text()) if f.exists() else []) if keys and r["key"] not in keys]
    for k, (fn, fname) in BUILDERS.items():
        if keys and k not in keys:
            continue
        s = fn()
        r = dict(key=k, file=fname if isinstance(fname, str) else "drawing", ours_mm3=round(s.Volume(), 1), ours_ext=_ext(s),
                 vendor_mm3=None, vendor_ext=None)
        if not isinstance(fname, str):
            r["vendor_ext"] = [round(v, 2) for v in fname[1]]
            r["dext_max_mm"] = round(max(abs(a - b) for a, b in zip(r["ours_ext"], r["vendor_ext"])), 2)
            r["vendor_note"] = "no STEP: overall extents from the maker's drawing"
            res.append(r)
            print(json.dumps(r), flush=True)
            continue
        p = VCAD / fname
        if p.exists():
            try:
                v = _load_step(p)
                r["vendor_mm3"], r["vendor_ext"] = round(v.Volume(), 1), _ext(v)
                r["dvol_pct"] = round(100.0 * (r["ours_mm3"] - r["vendor_mm3"]) / r["vendor_mm3"], 1)
                r["dext_max_mm"] = round(max(abs(a - b) for a, b in zip(r["ours_ext"], r["vendor_ext"])), 2)
            except Exception as e:  # noqa: BLE001  report and carry on
                r["vendor_note"] = f"{type(e).__name__}: {e}"
        else:
            r["vendor_note"] = "vendor file not in /tmp/ft-vcad"
        res.append(r)
        print(json.dumps(r), flush=True)
    res.sort(key=lambda q: q["key"])
    f.write_text(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if cmd == "measure":
        fa = None
        if "--faces" in sys.argv:
            i = sys.argv.index("--faces")
            fa = (sys.argv[i + 1], sys.argv[i + 2])
        measure(sys.argv[2], fa)
    elif cmd == "verify":
        verify(sys.argv[2:] or None)
    else:
        print(__doc__)
