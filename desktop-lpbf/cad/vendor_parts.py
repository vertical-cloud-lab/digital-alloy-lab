"""Bought parts drawn to their published dimensions, as drop-in replacements for the envelopes in lpbf_low.py (issue #260).

Each builder returns a cq.Shape in the SAME local frame as the generic helper or envelope it replaces, so the swap in
lpbf_low.py is one line (SWAPS below lists the exact line for each, and the position changes the real part forces).
Dimensions come from the vendor's drawing, listing or datasheet named in SOURCES; where the vendor publishes CAD we
compare our shape with it by volume and sorted bounding-box extents, the way verify_fasteners.py does. Vendor CAD is
never committed: it is fetched into /tmp (vendor-cad-manifest.csv records URL, size and sha256).

    python desktop-lpbf/cad/vendor_parts.py inventory   # every Part of build(): which are envelopes, ranked -> analysis/out/real-parts/
    python desktop-lpbf/cad/vendor_parts.py verify      # our shapes vs vendor CAD in /tmp/parts-work/vcad (and /tmp/parts-work/teknic)
    python desktop-lpbf/cad/vendor_parts.py swapcheck   # swap each builder into a build() and run exact booleans against its neighbours

Run each under the memory cap, e.g. /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/cad/vendor_parts.py swapcheck (17 min wall,
7 min CPU on a busy 4-core runner; inventory takes seconds, verify about 5 min with the 64 MB Teknic STEP).
Units mm. Every builder states its local frame; "drop-in for" names the lpbf_low call it replaces.
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


# --------------------------------------------------------------------------------------------
# small helpers (kept local so this file does not depend on lpbf_low)
# --------------------------------------------------------------------------------------------
def _box(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def _cyl(r, p0, d, h):
    return cq.Solid.makeCylinder(r, h, V(*p0), V(*d))


def _fuse(shapes):
    out = shapes[0]
    for s in shapes[1:]:
        out = out.fuse(s)
    return out.clean()


def _revolve(pts):
    """Solid of revolution about local z from a closed (r, z) polyline (r >= 0)."""
    w = cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))
    return w.val()


def _rbox(x0, x1, y0, y1, z0, z1, r, edges="|Z"):
    w = cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
    if r > 0:
        w = w.edges(edges).fillet(r)
    return w.val().translate(V(x0, y0, z0))


# --------------------------------------------------------------------------------------------
# Sources: one entry per builder. dims = the numbers the builder uses; cad = vendor file used by verify()
# --------------------------------------------------------------------------------------------
SOURCES = {
    "clearpath_sd_231x": dict(vendor="Teknic", pn="CPM-SDSK-2311S-RLN (2310S same frame)", price="$293 (2311S), $265 (2310S), qty 1-9",
        url="https://teknic.com/files/downloads/23xx%20CPM%20Dimensional%20Drawing.pdf",
        dims="flange 59.10 sq; body 84.81 behind the mounting face; pilot 38.10 x 1.90; shaft 9.50 x 20.57 (3 mm key); 4 x 5.20 on 66.67 BC; connector block 53.85 wide, 22.75 above the flange, 38.49 long (assumed: the unlabelled .515 [38.49] dimension); 0.6 kg",
        cad="/tmp/parts-work/teknic/CPM-231x-Q.STEP", fetched="2026-11-20T14:11Z"),
    "mcm_6709K12": dict(vendor="McMaster-Carr", pn="6709K12", price="$144.71 each", url="https://www.mcmaster.com/6709K12/",
        dims="28 overall height from rail bottom; 34 wide; 38.8 steel block + end caps/seals = 56.6 long; grease nipple +5.5; carriage underside 4.7 above rail bottom; 4 x M4 on 26 x 26",
        cad="/tmp/parts-work/vcad/6709K12.STEP", fetched="2026-11-20T13:57Z"),
    "mcm_6709K33": dict(vendor="McMaster-Carr", pn="6709K33", price="$0.31 per mm (280 mm = $86.80)", url="https://www.mcmaster.com/6709K33/",
        dims="15 wide x 15 high; M4 holes 60 c-c, 20 from the end, 9.7 deep counterbore listed; raceway grooves 2 per side (assumed R1.6 at 3.5 and 11 mm, not published)",
        cad="", fetched="2026-11-20T14:05Z"),
    "mcm_4566N401": dict(vendor="McMaster-Carr", pn="4566N401", price="$244.44 each", url="https://www.mcmaster.com/4566N401/",
        dims="length 43; body 23; flange 40 x 10 with flats 30 across (McMaster CAD); bolt circle 32, 6 x 4.5 holes; bore = screw 12",
        cad="/tmp/parts-work/vcad/4566N401.STEP", fetched="2026-11-20T13:58Z"),
    "mcm_6627T91": dict(vendor="McMaster-Carr", pn="6627T91", price="$81.74 each", url="https://www.mcmaster.com/6627T91/",
        dims="NEMA 17, 42.3 sq (stator 41.9); body 48.0 behind the mounting face; pilot 22 x 2; shaft 5 D-profile x 24 beyond the pilot; rear cap with a 0.76 lead boss",
        cad="/tmp/parts-work/vcad/6627T91.STEP", fetched="2026-11-20T14:00Z"),
    "mcm_5786N23": dict(vendor="McMaster-Carr", pn="5786N23", price="$13.65 each", url="https://www.mcmaster.com/5786N23/",
        dims="ISO-KF 25 flange OD 39.88 (1.57 in.), face bore 26.16, rim 3.05 thick, 15 deg back taper; 1 in. x 0.065 in. tube end; 12.7 long",
        cad="/tmp/parts-work/vcad/5786N23.STEP", fetched="2026-11-20T14:00Z"),
    "mcm_5786N25": dict(vendor="McMaster-Carr", pn="5786N25", price="$17.31 each", url="https://www.mcmaster.com/5786N25/",
        dims="ISO-KF 40 flange OD 54.86 (2.16 in.), face bore 41.14, rim 3.05 thick, 15 deg back taper; 1.5 in. x 0.083 in. tube end; 19.05 long",
        cad="/tmp/parts-work/vcad/5786N25.STEP", fetched="2026-11-20T14:00Z"),
    "mcm_4518K72": dict(vendor="McMaster-Carr", pn="4518K72", price="$13.67 each", url="https://www.mcmaster.com/4518K72/",
        dims="KF-25 wing-nut clamp: ring OD 55.2, 17 thick at the ears; hinge to -x (32.5 from the axis), wing nut to +x (44.7) and +y (36.1) (McMaster CAD extents)",
        cad="/tmp/parts-work/vcad/4518K72.STEP", fetched="2026-11-20T14:01Z"),
    "mcm_4518K73": dict(vendor="McMaster-Carr", pn="4518K73", price="$15.31 each", url="https://www.mcmaster.com/4518K73/",
        dims="KF-40 wing-nut clamp: ring OD 71.0, 17 thick at the ears; hinge to -x (40.0), wing nut to +x (53.5) and +y (36.1) (McMaster CAD extents)",
        cad="/tmp/parts-work/vcad/4518K73.STEP", fetched="2026-11-20T14:01Z"),
    "mcm_4123K45": dict(vendor="McMaster-Carr", pn="4123K45", price="$300.80 each", url="https://www.mcmaster.com/4123K45/",
        dims="KF-25 x KF-25 full-port ball valve: end to end 124.2 (4.89 in.); body 60.45 square (2.38 in.); handle top 91.7 above the axis; lever 138.2 long from the stem (7.89 in. overall)",
        cad="/tmp/parts-work/vcad/4123K45.STEP", fetched="2026-11-20T14:00Z"),
    "mcm_3861N11": dict(vendor="McMaster-Carr", pn="3861N11", price="$358.05 each", url="https://www.mcmaster.com/3861N11/",
        dims="1/4 NPT male x 16.5 (0.65 in.); 1.96 in. (49.8) from the thread shoulder to the cable exit; 24 A/F hex (0.94 in.), 27 across corners; 36 in. cable (not drawn beyond a 20 mm stub)",
        cad="/tmp/parts-work/vcad/3861N11.STEP", fetched="2026-11-20T14:00Z"),
    "mcm_5169K72": dict(vendor="McMaster-Carr", pn="5169K72 (+ 9179K14 HEPA element)", price="$107.84 each (element $48.73)", url="https://www.mcmaster.com/5169K72/",
        dims="housing 3 3/4 in. (95.25) dia x 3 5/8 in. (92.1) high; side inlet boss to 57.4 from the axis; 1/2 NPSC female side inlet, bottom outlet; bracket tabs +/-60.6 (McMaster CAD)",
        cad="/tmp/parts-work/vcad/5169K72.STEP", fetched="2026-11-20T14:02Z"),
    "mcm_4396K21": dict(vendor="McMaster-Carr", pn="4396K21", price="$587.53 each", url="https://www.mcmaster.com/4396K21/",
        dims="overall 14 1/2 x 5 5/8 x 12 in. (368.3 x 142.9 x 304.8, to the handle top); layout (motor, pump block, handle, top intake) from the catalogue photo; no CAD offered",
        cad="", fetched="2026-11-20T14:02Z"),
    "thorlabs_fth160_1064": dict(vendor="Thorlabs", pn="FTH160-1064", price="$1,011.78 (vendor-lookups.csv)", url="https://media.thorlabs.com/globalassets/items/f/ft/fth/fth160-1064/stn012046-e0w.pdf",
        dims="50.2 long; output ring 90 dia x 9.2 (= FFL 191.7 - WD 182.5); M85x1 thread 12.8 long; 78 dia step to 29.1; cone to 53 dia at 44.1; nose 53 dia with a 39 aperture; 0.8 kg",
        cad="", fetched="2026-11-20T14:00Z"),
    "scanlab_basicube20": dict(vendor="SCANLAB", pn="basiCube 20", price="quote (BOM L5)", url="https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-basiCube-Series-EN.pdf",
        dims="155 deep x 130 wide x 122 high; input aperture 20 dia, axis 30 above the bottom face and 83.5 from the left edge of the input face; output axis 57.15 from the input face, 58.25 from the left edge (beam displacement 25.25); 3.75 kg without objective; objective ring and holes not dimensioned",
        cad="", fetched="2026-11-20T14:15Z"),
    "ipg_collimator_d5": dict(vendor="IPG Photonics", pn="standard collimator, 5 mm beam (YLR-500-U3-SM-AC option)", price="not quoted yet",
        url="quotes/ipg-ylr-500-u3-sm-ac.md (IPG drawing transcribed; PDF not committed)",
        dims="housing 30 dia, 28 dia at the output end, 128 +/- 3 long, plus 78 strain relief (relief diameters and the 28 dia step length assumed)",
        cad="", fetched="2026-11-18"),
    "ipg_ylr500_u3": dict(vendor="IPG Photonics", pn="YLR-500-U3-SM-AC", price="approx. $23k (quote 2026-11-18)", url="quotes/ipg-ylr-500-u3-sm-ac.md (IPG spec G22-29856 and drawings; PDF not committed)",
        dims="4U: 176.5 high; 482.3 over the rack ears, 465 body; 506 body deep, 557.2 over the handles; 40 kg (handle positions assumed)",
        cad="", fetched="2026-11-18"),
    "eaton_5px1500rtg2": dict(vendor="Eaton", pn="5PX1500RTG2", price="not found", url="https://assets.tripplite.com/product-pdfs/en/5px1500rtg2.pdf",
        dims="2U, 86.36 high x 436.88 wide x 447.04 deep; 23 kg; rack ears 482.6 (standard 19 in., not stated for this model)",
        cad="", fetched="2026-11-20T14:15Z"),
}


# --------------------------------------------------------------------------------------------
# Motion: servos, steppers, guides, screws
# --------------------------------------------------------------------------------------------
def clearpath_sd_231x(shaft_l=20.57, connector="+y"):
    """Teknic ClearPath-SD NEMA 23, 231x frame (CPM-SDSK-2310S/2311S), drawing D1171/M.
    Drop-in for lpbf_low.servo_nema23(): mounting face at local z = 0, body toward -z, shaft +z; the connector block
    is on local +y (connector="-y" puts it on the other side)."""
    sq, L = 59.10, 84.81
    body = cq.Workplane("XY").rect(sq, sq).extrude(-L).edges("|Z").chamfer(5.0).val()
    for sx in (-1, 1):                                   # 4 x Ø5.2 on a Ø66.67 bolt circle (47.14 square), 10 mm deep
        for sy in (-1, 1):
            body = body.cut(_cyl(2.6, (sx * 23.57, sy * 23.57, -10.0), (0, 0, 1), 10.01))
    s = 1.0 if connector == "+y" else -1.0
    blk = _box(-53.85 / 2, 53.85 / 2, 0, 22.75, -L, -L + 38.49)
    if s < 0:
        blk = blk.mirror("XZ")
    blk = blk.translate(V(0, s * sq / 2, 0))
    pilot = _cyl(19.05, (0, 0, 0), (0, 0, 1), 1.90)
    shaft = _cyl(4.75, (0, 0, 0), (0, 0, 1), shaft_l).cut(_box(-1.5, 1.5, 4.75 - 1.8, 5.0, shaft_l - 12.0, shaft_l + 0.1))
    return _fuse([body, blk, pilot, shaft])


def mcm_6627T91():
    """McMaster 6627T91 NEMA 17 stepper. Drop-in for lpbf_low.stepper_nema17(40): mounting face at z = 0, body toward
    -z, pilot (and here the 5 mm D shaft) toward +z."""
    body = cq.Workplane("XY").rect(42.3, 42.3).extrude(-48.0).edges("|Z").chamfer(3.5).val()
    boss = _box(-8.0, 8.0, 21.15, 21.96, -48.0, -38.4)          # lead exit on the rear cap
    pilot = _cyl(11.0, (0, 0, 0), (0, 0, 1), 2.0)
    shaft = _cyl(2.5, (0, 0, 0), (0, 0, 1), 26.0).cut(_box(2.0, 3.0, -3.0, 3.0, 11.0, 26.1))
    holes = [_cyl(1.5, (sx * 15.5, sy * 15.5, -4.5), (0, 0, 1), 4.51) for sx in (-1, 1) for sy in (-1, 1)]
    out = _fuse([body, boss, pilot, shaft])
    for h in holes:
        out = out.cut(h)
    return out


def mcm_6709K12():
    """McMaster 6709K12 ball carriage for the 15 mm rail. Drop-in for lpbf_low.guide_carriage(57, 34, 28, 3, 15, 15):
    rail along local x, carriage centred at x = 0, rail centred in y, rail bottom at z = 0, carriage top at z = 28."""
    zb, zt = 4.7, 28.0
    blk = _box(-19.4, 19.4, -17.0, 17.0, zb, zt)
    caps = _box(-25.8, 25.8, -16.0, 16.0, zb + 0.4, zt - 0.3)          # plastic end caps
    seals = _box(-28.3, 28.3, -16.0, 16.0, zb + 0.5, zt - 1.2)         # rubber end seals
    body = _fuse([blk, caps, seals])
    body = body.cut(_box(-30, 30, -7.8, 7.8, zb - 1, 15.4))            # rail channel (rail 15 x 15, 0.4 above its top)
    body = body.cut(_box(-30, 30, -17.5, -16.2, zb - 1, zb + 3.0)).cut(_box(-30, 30, 16.2, 17.5, zb - 1, zb + 3.0))
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body.cut(_cyl(1.65, (sx * 13.0, sy * 13.0, zt - 5.0), (0, 0, 1), 5.01))   # 4 x M4 x 5 deep, 26 x 26
    nip = _fuse([_cyl(3.5, (28.3, 0, 19.7), (1, 0, 0), 2.5), _cyl(2.6, (30.8, 0, 19.7), (1, 0, 0), 3.0)])   # above the rail top (McMaster CAD)
    return _fuse([body, nip])


def mcm_6709K33(L):
    """McMaster 6709K33 15 mm rail cut to L. Drop-in for lpbf_low.guide_rail(L, 15, 15): along local +x 0..L, centred
    in y, base on z = 0, M4 counterbored holes 60 mm c-c starting 20 mm from the end (listed). The four raceway
    grooves are not published: drawn as R1.6 grooves at z = 11 (upper) and 6.5 (lower) on each side (assumed)."""
    prof = cq.Workplane("YZ").polyline([(-7.5, 0), (7.5, 0), (7.5, 14.2), (6.7, 15.0), (-6.7, 15.0), (-7.5, 14.2)]).close().extrude(L).val()
    for sy in (-1, 1):
        for z in (11.0, 6.5):
            prof = prof.cut(_cyl(1.6, (-1, sy * 7.5, z), (1, 0, 0), L + 2))
    x = 20.0
    while x <= L - 5.0:
        prof = prof.cut(_cyl(2.25, (x, 0, -1), (0, 0, 1), 17)).cut(_cyl(3.75, (x, 0, 15.0 - 5.3), (0, 0, 1), 6.0))
        x += 60.0
    return prof


def mcm_4566N401():
    """McMaster 4566N401 fast-travel flange ball nut (M12, 10 mm lead). Drop-in for lpbf_low.ball_nut(12, 23, 43, 40, 10):
    nut on local x, centred at x = 0, flange at the -x end; bore = the 12 mm screw (contact). Flats 30 across on local y."""
    fl = _cyl(20.0, (-21.5, 0, 0), (1, 0, 0), 10.0).cut(_box(-22, -11, 15.0, 21, -21, 21)).cut(_box(-22, -11, -21, -15.0, -21, 21))
    for k in range(6):
        a = math.radians(60 * k)
        fl = fl.cut(_cyl(2.25, (-22, 16.0 * math.sin(a), 16.0 * math.cos(a)), (1, 0, 0), 12))
    body = _cyl(11.5, (-11.5, 0, 0), (1, 0, 0), 33.0)
    return _fuse([fl, body]).cut(_cyl(6.0, (-22, 0, 0), (1, 0, 0), 44))


# --------------------------------------------------------------------------------------------
# Vacuum hardware: ISO-KF weld stubs, clamps, valve, transmitter
# --------------------------------------------------------------------------------------------
KF_REAL = {   # flange OD, face bore, rim thickness, tube OD, tube ID, fitting length (McMaster CAD sections)
    25: dict(fo=39.88, fb=26.16, rim=3.05, to=25.40, ti=22.10, flen=12.70, pn="5786N23"),
    40: dict(fo=54.86, fb=41.14, rim=3.05, to=38.10, ti=33.88, flen=19.05, pn="5786N25"),
}


def kf_weld_stub(size, stub=None):
    """McMaster 5786N23 (KF-25) / 5786N25 (KF-40) aluminium weld fitting, extended with its own tube to `stub`.
    Drop-in for lpbf_low.kf_stub(size, stub): flange face at local z = 0, tube toward -z, hollow.
    Profile from McMaster's CAD: full-OD rim, then the ISO 2861 15 deg back taper (slope 3.73) down to the tube."""
    k = KF_REAL[size]
    L = k["flen"] if stub is None else max(stub, k["flen"])
    ro, rt, rb, ri = k["fo"] / 2, k["to"] / 2, k["fb"] / 2, k["ti"] / 2
    d1 = k["rim"] + (ro - rt) / 3.73
    outer = [(ri, 0.0), (ro, 0.0), (ro, -k["rim"]), (rt, -d1), (rt, -L), (ri, -L)]
    s = _revolve(outer)
    return s.cut(_cyl(rb, (0, 0, -k["rim"] + 0.2), (0, 0, 1), k["rim"]))   # face counterbore for the centring ring


def kf_wing_clamp(size):
    """McMaster 4518K72 (KF-25) / 4518K73 (KF-40) wing-nut clamp. Drop-in for lpbf_low.kf_clamp(size): centred on the
    joint plane (local z = 0), axis z, hinge toward -x, the bolt ears and wing nut toward +x (wing up +y)."""
    k = KF_REAL[size]
    if size == 25:
        ro, rl, h, xh, xe, yw = 27.6, 15.5, 5.4, -32.5, 44.65, 36.09
    else:
        ro, rl, h, xh, xe, yw = 35.5, 22.5, 6.5, -40.0, 53.47, 36.09
    rr, zr = k["fo"] / 2 + 0.4, k["rim"] + 0.1                 # clears both flange rims at the joint plane,
    zl = zr + (rr - rl) / 3.73                                 # then follows their 15 deg back tapers in to the lips
    ring = _revolve([(rr, -zr), (rl, -zl), (rl, -h), (ro, -h), (ro, h), (rl, h), (rl, zl), (rr, zr)])
    hinge = _cyl(4.0, (xh + 4.0, -6.0, -6.5), (0, 0, 1), 13.0)
    ears = _box(ro - 4.0, xe - 6.0, -7.0, 7.0, -8.5, 8.5).cut(_box(ro - 4.5, xe, -1.0, 1.0, -9, 9))
    bolt = _cyl(2.5, (xe - 12.0, -10.0, 0), (0, 1, 0), 32.0)
    wing = _fuse([_cyl(6.0, (xe - 12.0, 9.0, 0), (0, 1, 0), 9.0), _box(xe - 24.0, xe, 14.0, yw, -1.5, 1.5)])
    return _fuse([ring, hinge, ears, bolt, wing])


def mcm_4123K45(handle="+x"):
    """McMaster 4123K45 KF-25 x KF-25 manual full-port ball valve (the BOM's pump isolation valve, line G7).
    Local frame: inlet flange face at x = 0, flow along +x, outlet face at x = 124.2, stem up (+z) at x = 62.1; the
    lever (138.2 from the stem) points along `handle` ("+x": over the outlet, "-x": back over the inlet).
    Replaces the 'KF-25 angle, pneumatic' envelope: NOT a drop-in (straight-through, 124 mm long)."""
    k = KF_REAL[25]
    fl_in = _revolve([(11.05, 0), (k["fo"] / 2, 0), (k["fo"] / 2, 3.05), (12.7, 3.05 + (k["fo"] / 2 - 12.7) / 3.73), (12.7, 18.0), (11.05, 18.0)])
    fl_out = fl_in.mirror("XY").translate(V(0, 0, 124.2))
    tube = _fuse([fl_in, fl_out]).rotate(V(0, 0, 0), V(0, 1, 0), 90)     # axis z -> x
    body = _cyl(27.0, (62.1 - 20.05, 0, 0), (1, 0, 0), 40.1)                       # centre section of the 3-piece body
    caps = _cyl(21.0, (18.0, 0, 0), (1, 0, 0), 88.2)                                # end caps between body and flanges
    bolts = []
    for sy in (-1, 1):                                                              # 4 tie bolts with heads and nuts
        for sz in (-1, 1):
            bolts += [_cyl(3.0, (62.1 - 38.4, sy * 23.71, sz * 23.71), (1, 0, 0), 74.9),
                      _cyl(6.2, (62.1 - 38.4, sy * 23.71, sz * 23.71), (1, 0, 0), 5.0), _cyl(6.2, (62.1 + 31.5, sy * 23.71, sz * 23.71), (1, 0, 0), 5.0)]
    pad = _box(62.1 - 15.0, 62.1 + 15.0, -15.0, 15.0, 30.23, 53.64)
    stem = _cyl(6.5, (62.1, 0, 53.64), (0, 0, 1), 6.9)
    sgn = 1.0 if handle == "+x" else -1.0
    lever_x0, lever_x1 = sorted((62.1 - sgn * 25.0, 62.1 + sgn * 138.18))
    lever = _box(lever_x0, lever_x1, -13.3, 13.3, 86.75, 91.69)
    riser = _box(62.1 - 12.5, 62.1 + 12.5, -13.0, 13.0, 53.64, 90.9)
    return _fuse([tube, body, caps, pad, stem, lever, riser] + bolts).cut(_cyl(11.05, (-1, 0, 0), (1, 0, 0), 126.2))   # full port, open


def mcm_3861N11():
    """McMaster 3861N11 0-15 psia transmitter. Local frame: thread shoulder (hex seat) at z = 0 on the axis, the 1/4 NPT
    thread below (z -16.5..0, drawn at the 13.7 mm major diameter), body up to the cable exit at z = 49.8, then a 20 mm
    cable stub (the 36 in. coiled lead is not drawn). Drop-in for the 'Pressure transducer' envelope at (100, 50, lz1)."""
    thread = _cyl(13.7 / 2, (0, 0, -16.5), (0, 0, 1), 16.5)
    hexa = cq.Workplane("XY").polygon(6, 27.0).extrude(9.0).val()
    body = _cyl(11.9, (0, 0, 9.0), (0, 0, 1), 33.0)
    cap = cq.Solid.makeCone(11.9, 6.0, 7.8, V(0, 0, 42.0), V(0, 0, 1))
    cable = _cyl(3.0, (0, 0, 49.8), (0, 0, 1), 20.0)
    return _fuse([thread, hexa, body, cap, cable])


# --------------------------------------------------------------------------------------------
# Gas module
# --------------------------------------------------------------------------------------------
def mcm_5169K72():
    """McMaster 5169K72 vacuum-rated intake-filter housing (takes the 9179K14 HEPA element), axis vertical.
    Local frame: axis at x = y = 0, bottom (outlet, 1/2 NPSC female) at z = 0, top at z = 92.1; side inlet boss toward
    +x; the mounting bracket's two tabs along +/-y. Replaces the 'cyclone + HEPA housing' envelope (no cyclone is chosen)."""
    can = _revolve([(0, 0), (44.0, 0), (47.6, 4.0), (47.6, 88.1), (44.0, 92.1), (0, 92.1)])
    boss = _cyl(11.5, (40.0, 0, 46.0), (1, 0, 0), 17.4)
    tabs = [_box(-13.8, 13.8, sy * 38.3 if sy > 0 else -60.6, 60.6 if sy > 0 else -38.3, 30.0, 34.0) for sy in (-1, 1)]
    s = _fuse([can, boss] + tabs)
    return s.cut(_cyl(8.0, (45.0, 0, 46.0), (1, 0, 0), 14.0)).cut(_cyl(8.0, (0, 0, -1.0), (0, 0, 1), 12.0))   # 1/2 NPSC ports


def mcm_4396K21():
    """McMaster 4396K21 rotary-vane pump (1e-2 Torr, 3 cfm, 1/2 hp), from the listed overall size 368.3 x 142.9 x 304.8
    (14 1/2 x 5 5/8 x 12 in., to the top of the handle) and the catalogue photo's layout: motor on +x, pump block on -x,
    handle over the pump block, flare intake tee on top of the block. McMaster offers no CAD for it, so only the overall
    extents are checked. Local frame: centred in x and y, feet on z = 0, length along x."""
    L, W, H = 368.3, 142.9, 304.8
    feet = _box(-L / 2 + 20, L / 2 - 40, -W / 2 + 10, W / 2 - 10, 0, 18)
    zm = 18 + W / 2 - 6                                                   # motor sits 2 mm into the feet (no tangent faces)
    motor = _cyl(W / 2 - 4, (-L / 2 + 150, 0, zm), (1, 0, 0), L - 150 - 6)
    endcap = _cyl(W / 2 - 14, (L / 2 - 6.5, 0, zm), (1, 0, 0), 6.5)
    block = _rbox(-L / 2, -L / 2 + 150, -W / 2, W / 2, 18, 205, 10)
    sw = _box(40.0, 110.0, -30, 30, 18 + W - 8, 18 + W + 30)                # switch / capacitor box on the motor
    handle = _fuse([_cyl(9.5, (-L / 2 + 30, 0, 205), (0, 0, 1), H - 205 - 9.5), _cyl(9.5, (-L / 2 + 30, 0, H - 9.5), (1, 0, 0), 120),
                    _cyl(9.5, (-L / 2 + 150, 0, 205), (0, 0, 1), H - 205 - 9.5)])
    intake = _fuse([_cyl(8.0, (-L / 2 + 95, 30, 205), (0, 0, 1), 40), _cyl(6.0, (-L / 2 + 75, 30, 235), (1, 0, 0), 40)])
    return _fuse([feet, motor, endcap, block, sw, handle, intake])


# --------------------------------------------------------------------------------------------
# Optics and laser
# --------------------------------------------------------------------------------------------
def thorlabs_fth160_1064():
    """Thorlabs FTH160-1064 f-theta lens, from drawing stn012046 (rev A). Local frame: output end (toward the work) at
    z = 0, axis +z, input nose at z = 50.2. The flange shoulder (top of the Ø90 ring) is at z = 9.2 = FFL 191.7 - WD
    182.5; the M85x1 thread runs from there to z = 22.0. Drop-in for the lens envelope: translate to (0, 0, P['z_lens0'])."""
    prof = [(0, 0), (45.0, 0), (45.0, 9.2), (42.5, 9.2), (42.5, 22.0), (39.0, 22.0), (39.0, 29.1), (26.5, 44.1), (26.5, 50.2), (0, 50.2)]
    s = _revolve(prof)
    return s.cut(_cyl(19.5, (0, 0, 44.1), (0, 0, 1), 6.2)).cut(_cyl(37.5, (0, 0, -0.01), (0, 0, 1), 1.5))   # Ø39 input aperture, window recess


def scanlab_basicube20():
    """SCANLAB basiCube 20, from the basiCube brochure's drawing (2025-06). Local frame: the OUTPUT axis at x = y = 0,
    the bottom (beam-out) face at z = 0, the input face toward -x. Input aperture Ø20 at (-57.15, -25.25, 30): the beam
    enters 30 mm above the mounting face and 25.25 mm to the side of the output axis (side assumed from first-angle views)."""
    x0, x1 = -57.15, 155.0 - 57.15
    y0, y1 = -(130.0 - 58.25), 58.25
    s = _rbox(x0, x1, y0, y1, 0, 122.0, 6.0)
    s = s.cut(_cyl(10.0, (x0 - 1, -25.25, 30.0), (1, 0, 0), 12.0)).cut(_cyl(10.0, (0, 0, -1), (0, 0, 1), 12.0))
    return s


GALVO_IN = (-57.15, -25.25, 30.0)   # input beam point of scanlab_basicube20() in its local frame


def ipg_collimator_d5(relief=True):
    """IPG standard 5 mm-beam collimator on the delivery fibre (YLR-U3 option), from IPG's drawing as transcribed in
    quotes/ipg-ylr-500-u3-sm-ac.md: Ø30 housing, Ø28 at the output end, 128 long, plus 78 of strain relief.
    Local frame: output face at x = 0 on the beam axis, beam toward +x, housing toward -x. The Ø28 step length (8 mm)
    and the relief's diameters (Ø18 to Ø10) are not on the drawing transcription: assumed."""
    out = _cyl(14.0, (-8.0, 0, 0), (1, 0, 0), 8.0)
    body = _cyl(15.0, (-128.0, 0, 0), (1, 0, 0), 120.0)
    parts = [out, body]
    if relief:
        parts.append(cq.Solid.makeCone(5.0, 9.0, 78.0, V(-206.0, 0, 0), V(1, 0, 0)))
    return _fuse(parts)


def ipg_ylr500_u3():
    """IPG YLR-500-U3-SM-AC, 4U 19 in. chassis. Local frame: x centred, y = 0 at the rack-ear plane (rear face of the
    front panel), +y into the rack, z = 0 at the chassis bottom. Body 465 x 506 x 176.5, ears 482.3 wide x 3 thick, two
    handles to 557.2 - 506 = 51.2 in front of the body (handle position and section assumed: Ø12 bars 120 mm apart)."""
    H = 176.5
    body = _box(-232.5, 232.5, 0, 506.0, 0, H)
    ears = _box(-482.3 / 2, 482.3 / 2, -3.0, 0, 0, H)
    hd = []
    for sx in (-1, 1):
        xh = sx * (482.3 / 2 - 14.0)
        hd += [_box(xh - 6, xh + 6, -45.0, -2.0, H / 2 + sz * 60.0 - 6, H / 2 + sz * 60.0 + 6) for sz in (-1, 1)]
        hd.append(_box(xh - 6, xh + 6, -51.2, -39.2, H / 2 - 66.0, H / 2 + 66.0))
    return _fuse([body, ears] + hd)


def eaton_5px1500rtg2():
    """Eaton 5PX1500RTG2 2U UPS (datasheet: 86.36 x 436.88 x 447.04, 23 kg). Same frame as ipg_ylr500_u3(); the 482.6 mm
    ear width is the 19 in. standard (not stated for this model); ears 3 mm thick in front of the body."""
    H = 86.36
    return _fuse([_box(-436.88 / 2, 436.88 / 2, 0, 447.04, 0, H), _box(-482.6 / 2, 482.6 / 2, -3.0, 0, 0, H)])


# --------------------------------------------------------------------------------------------
# Swaps into lpbf_low.build(): the exact placement each one-line change uses (and what it forces)
# --------------------------------------------------------------------------------------------
def swaps(M):
    """[(replaces: exact Part names, new shape in model coordinates, line to change in lpbf_low, note on fit)]."""
    P = M.P
    cx, cy, ix, iy = P["cx"], P["cy"], P["ix"], P["iy"]
    ry_, rz_ = P["rc_screw_y"], P["rc_screw_z"]
    lz1, xd = P["lid_z1"], P["x_dose"]
    zf = -P["floor"]
    g0 = P["z_base1"]
    import module_params as MP
    import modules_low as ML
    z = ML.zlevels()
    a0 = z["zc"] - MP.ARM_T
    car_lo, car_hi = min(MP.Z_P_MIN, MP.ZSTAGE_RELEASE) + a0, MP.Z_P_MAX + a0 + 40.0
    az1 = car_hi + 3.0
    rzc = lz1 + 28.0
    xc = P["x_park"]
    out = []

    def add(names, shape, line, note):          # names: Part-name prefixes (the model's names grow suffixes)
        out.append(dict(replaces=names, shape=shape, line=line, note=note))

    add(["Recoater servo (ClearPath-SD, NEMA 23)"], M.place(clearpath_sd_231x(20.57), (-cx - 60, ry_, rz_), (0, 1, 0), (1, 0, 0)),
        "rmot = place(VP.clearpath_sd_231x(20.57), (-cx - 60, ry_, rz_), (0, 1, 0), (1, 0, 0))",
        "59.1 sq (not 57.15) and 84.8 long (not 100) + a 22.75 mm connector block on top: the motor bracket top must drop ~1 mm (rz_ - 28.6 -> rz_ - 29.6)")
    add(["Z servo (ClearPath-SD, NEMA 23, folded)"], M.place(clearpath_sd_231x(18.0, connector="-y"), (64.0, 80.0, az1), (1, 0, 0), (0, 0, 1)),
        "modules_low.add_zstage: h.place(VP.clearpath_sd_231x(18.0, connector='-y'), (64.0, 80.0, az1), (1, 0, 0), (0, 0, 1))",
        "connector block must face -y (front): on +y it hits the process base plate (12.6 cm3) beyond the window's y = 114 edge; 84.8 long instead of 100")
    add(["Dosing stepper (NEMA 17)"], M.place(mcm_6627T91(), (xd, 74, rzc), (1, 0, 0), (0, -1, 0)),
        "place(VP.mcm_6627T91(), (xd, 74, rzc), (1, 0, 0), (0, -1, 0))",
        "48 mm body (not 40) and the 5 mm x 24 shaft now drawn; the shaft runs into the roller seal housing (designed)")
    add(["Recoater carriage (15 mm rail)"], M.place(mcm_6709K12(), (xc, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0)),
        "place(VP.mcm_6709K12(), (xc, iy, P['rc_rail_z']), (1, 0, 0), (0, -1, 0))", "same 28 x 34 section; 62.1 long with the grease nipple (was 57)")
    add(["Recoater guide rail (15 mm, 270 mm)"], M.place(mcm_6709K33(270.0), (-135, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0)),
        "rr = place(VP.mcm_6709K33(270.0), (-135, iy, P['rc_rail_z']), (1, 0, 0), (0, -1, 0))", "same envelope; raceway grooves drawn (assumed)")
    add(["Recoater ball nut (flange on the +x face)"], M.place(mcm_4566N401(), (xc + 10.5, ry_, rz_), (-1, 0, 0), (0, 0, 1)),
        "place(VP.mcm_4566N401(), (xc + 10.5, ry_, rz_), (-1, 0, 0), (0, 0, 1))", "flange has flats 30 mm across (faces +/-y)")
    zl0 = P["z_lens0"]
    add(["f-theta lens, f = 160 mm (FTH160-1064 envelope)"], thorlabs_fth160_1064().translate(V(0, 0, zl0)),
        "lens = VP.thorlabs_fth160_1064().translate(V(0, 0, P['z_lens0']))",
        "fits inside the old envelope; its M85x1 thread (z 191.7-204.5) ends 3.2 mm below the bridge (z 207.7): needs a 16 mm M85x1 adapter ring under the bridge")
    zb1_ = P["z_bridge1"]
    add(["2-axis galvo scan head (basiCube class)"], scanlab_basicube20().translate(V(0, 0, zb1_)),
        "galvo = VP.scanlab_basicube20().translate(V(0, 0, zb1_))",
        "155 x 130 x 122 (was 115 x 115 x 110); beam input at z = z_bridge1 + 30 (was + 45) and y = -25.25 (was 0): beam tube, shutter and collimator move")
    bz = zb1_ + GALVO_IN[2]
    add(["Collimator (QBH, f = 30 mm, D ~ 3.2 mm) on V-mount"], ipg_collimator_d5().translate(V(-210.0, GALVO_IN[1], bz)),
        "coll = VP.ipg_collimator_d5().translate(V(-210, -25.25, P['beam_z'])) with P['beam_z'] = P['z_bridge1'] + 30 (keep the V-mount block)",
        "206 mm with its strain relief (envelope 130): the relief ends at x = -416, 46 mm outside the guard's left panel (x = -370)")
    add(["Vacuum isolation valve (KF-25 angle, pneumatic)"],
        _fuse([M.place(kf_wing_clamp(25), (cx + 18, 0, 70), (0, 1, 0), (1, 0, 0)), mcm_4123K45("+x").translate(V(cx + 18, 0, 70))]),
        "vv = comp([place(VP.kf_wing_clamp(25), (cx + 18, 0, 70), (0, 1, 0), (1, 0, 0)), VP.mcm_4123K45('+x').translate(V(cx + 18, 0, 70))])",
        "the BOM's valve is a straight 124 mm ball valve with a 138 mm lever, not an angle valve: its outlet flange lands at x = 298, outside the guard (x = 290)")
    add(["Pressure transducer"], mcm_3861N11().translate(V(100, 50, lz1)),
        "VP.mcm_3861N11().translate(V(100, 50, lz1)); the lid port must then be 1/4 NPT (Ø13.7 drawn), not the 7/16-20 SAE-4 boss",
        "3861N11 has a 1/4 NPT male thread: the lid's new SAE-4 O-ring-boss port needs a different transmitter (or an SAE-4 x 1/4 NPT female adapter, +~25 mm)")
    for nm, p0, xd_, nrm, stub in [("Inlet plenum port (KF-25)", (0, cy + 32 + 20, 11), (1, 0, 0), (0, 1, 0), 26),
                                   ("Outlet plenum port (KF-25)", (86, (MP.OUTLET_Y[0] + MP.OUTLET_Y[1]) / 2, zf - 45 - 26), (1, 0, 0), (0, 0, 1), 26),
                                   ("Vacuum port (KF-25", (cx + 18, 0, 70), (0, 1, 0), (1, 0, 0), 10)]:
        add([nm], M.place(kf_weld_stub(25, stub), p0, xd_, nrm), f"place(VP.kf_weld_stub(25, {stub}), {p0}, {xd_}, {nrm})", "McMaster 5786N23 profile + 1 in. x 0.065 in. tube")
    ox = (P["ovf_x0"] + P["ovf_x1"]) / 2
    add(["Overflow port (KF-40)"], M.place(kf_weld_stub(40, 16), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, -1)),
        "place(VP.kf_weld_stub(40, 16), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, -1))", "5786N25 takes 1.5 in. tube (38.1 OD), not 41.3")
    add(["Overflow clamp (KF-40)"], M.place(kf_wing_clamp(40), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, 1)),
        "place(VP.kf_wing_clamp(40), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, 1))", "wing nut reaches 53.5 mm from the axis (+x)")
    add(["Sealed cyclone + HEPA housing (316L, valves off for passivation)"], mcm_5169K72().translate(V(470, -40, g0 + 20)),
        "filt = VP.mcm_5169K72().translate(V(470, -40, g0 + 20)) (keep the 20 mm stand; inlet is now the side boss, outlet the bottom)",
        "Ø95 x 92 instead of Ø116 x 254; ports are 1/2 NPSC, so the two KF-25 filter ports move to NPT adapters")
    add(["Dry scroll pump (≤ 0.3 mbar, 6 m3/h class)"], mcm_4396K21().translate(V(770, 165, g0)),
        "pump = VP.mcm_4396K21().translate(V(770, 165, g0))", "368 x 143 x 305: 15 mm taller than the envelope with its inlet; intake is a flare tee on the pump block, so the KF-25 inlet moves")
    rx0, rx1, ry0 = -990.0, -430.0, -300.0
    zr_laser = M.Z_TRAY + 25.0 + 2 * 44.45
    add(["Fiber laser source, 500 W single-mode (3U)"], ipg_ylr500_u3().translate(V((rx0 + rx1) / 2, ry0 + 30, zr_laser + 1)),
        "laser unit: nu 3 -> 4 and the rack 470 -> 515 mm tall (or the DIN drawer 3U -> 2U); shape VP.ipg_ylr500_u3().translate(V(-710, ry0 + 30, zr))",
        "4U (176.5), not 3U: overlaps the scan PC above it by 43 mm in a 10U rack; handles 51 mm proud of the rack front")
    add(["UPS (Eaton 5PX 1500 class, 2U)"], eaton_5px1500rtg2().translate(V((rx0 + rx1) / 2, ry0 + 30, M.Z_TRAY + 25.0 + 1)),
        "VP.eaton_5px1500rtg2().translate(V(-710, ry0 + 30, zr))", "smaller than the 2U envelope (447 deep, not 530)")
    return out


# --------------------------------------------------------------------------------------------
# CLI: inventory, verify, swapcheck
# --------------------------------------------------------------------------------------------
OUT = HERE.parent / "analysis" / "out" / "real-parts"

# (substring of the Part name, status, real part / reason). status: env = envelope or generic shape of a bought part;
# done = replaced here; design = lab-made part (drawn as designed, not a vendor part)
GENERIC = [
    ("Leveling mounts", "checked", "McMaster 5537T983: drawn to McMaster's CAD dimensions (volume checked here)"),
    ("19 in. rack frame", "env", "no rack chosen; S9 lists 30 mm T-slot for the old cabinet"),
    ("UPS (Eaton", "done", "Eaton 5PX1500RTG2"),
    ("Fiber laser source", "done", "IPG YLR-500-U3-SM-AC (4U)"),
    ("Scan + laser controller PC", "env", "no PC chosen (BOM C1 is a SCANLAB RTC6 card, quote)"),
    ("DIN-rail drawer", "env", "contents chosen (C3, C4, S1) but no drawer/enclosure: BOM C6 is a McMaster 7812K14 wall box"),
    ("Rack side panels", "env", "sheet, no part number"),
    ("Overflow port (KF-40)", "done", "McMaster 5786N25"),
    ("Overflow jar", "env", "KF-40 half nipple: no part number in the BOM"),
    ("Overflow clamp", "done", "McMaster 4518K73"),
    ("Overflow-jar present sensor", "env", "AutomationDirect PAM-AP-1H (M12 x 45): not drawn yet"),
    ("Inlet plenum port", "done", "McMaster 5786N23"),
    ("Outlet plenum port", "done", "McMaster 5786N23"),
    ("Vacuum port (KF-25", "done", "McMaster 5786N23"),
    ("Layer-light LED bar", "env", "no part number"),
    ("Plate-height through-beam", "env", "Omron E32-T61-S: not drawn yet"),
    ("Module-present sensor", "env", "AutomationDirect PAM-AP-1H: not drawn yet"),
    ("Recoater guide rail", "done", "McMaster 6709K33 (no CAD offered for the cut length: drawn to the listing)"),
    ("Recoater carriage (15 mm rail)", "done", "McMaster 6709K12"),
    ("Recoater ball screw", "env", "McMaster 4566N101: kept as a Ø12 rod (CAD fetched; helical thread not redrawn)"),
    ("Recoater ball nut", "done", "McMaster 4566N401"),
    ("Recoater servo", "done", "Teknic CPM-SDSK-2311S-RLN"),
    ("Z servo", "done", "Teknic CPM-SDSK-2311S-RLN"),
    ("Z actuator body", "env", "'KR-class' actuator: not in the BOM (M3 lists 6638K11 + 6709K33 + 6709K12)"),
    ("Z carriage", "env", "part of the KR-class actuator envelope"),
    ("Pot magnet", "env", "McMaster 5679K95: CAD fetched; 7 mm cup drawn, 9 mm of extra parts in McMaster's model not resolved"),
    ("Dosing stepper", "done", "McMaster 6627T91"),
    ("Side reservoir port (KF-16", "env", "KF-16 blank: no part number"),
    ("Reservoir-docked sensor", "env", "AutomationDirect PAM-AP-1H: not drawn yet"),
    ("Drawer-closed sensor", "env", "AutomationDirect PAM-AP-1H: not drawn yet"),
    ("NFC reader antenna", "env", "Adafruit 364 board: not drawn"),
    ("Load cell", "env", "Laumas ALLUE3: not drawn yet"),
    ("Layer camera", "env", "Raspberry Pi HQ camera + C-mount lens: not drawn yet"),
    ("Pressure transducer", "done", "McMaster 3861N11"),
    ("Overpressure relief valve", "env", "McMaster 4277T52: page needs a set-pressure choice before CAD; not fetched"),
    ("Door hinge leaves", "env", "labelled 1151A87 but drawn as custom knuckles; 1151A87 is a 3 x 3 in. two-leaf hinge (CAD fetched)"),
    ("Door hinge knuckles on the chamber", "env", "as above"),
    ("Draw-latch keepers", "env", "1807A61 strike (CAD fetched): real latch is 135.5 mm long"),
    ("Draw latches on the door", "env", "1807A61 (CAD fetched): real latch is 135.5 x 44 x 30.5 mm, drawn here as 24 x 12 x 18"),
    ("f-theta lens", "done", "Thorlabs FTH160-1064"),
    ("2-axis galvo scan head", "done", "SCANLAB basiCube 20"),
    ("Safety shutter + beam dump", "env", "no product chosen (BOM L4: quote)"),
    ("Collimator (QBH", "done", "IPG 5 mm collimator"),
    ("Process fiber", "env", "IPG delivery cable (Ø8.5 per IPG's QBH drawing; drawn Ø10)"),
    ("Dry scroll pump", "done", "McMaster 4396K21 (BOM G2's choice; listing dimensions only)"),
    ("Pump inlet (KF-25)", "env", "needs a flare-to-NPT adapter + 4518K49 (BOM G2)"),
    ("Sealed cyclone + HEPA housing", "done", "McMaster 5169K72 (no cyclone chosen)"),
    ("Filter inlet (KF-25)", "env", "5169K72 ports are 1/2 NPSC: adapters not chosen"),
    ("Filter outlet (KF-25)", "env", "as above"),
    ("Sealed side-channel blower", "env", "no gas-tight blower of this size found (KNF N 630.1.2 SP.9 E is 569 x 296 x 315, 45 kg)"),
    ("Blower inlet", "env", "follows the blower"),
    ("Blower outlet", "env", "follows the blower"),
    ("Trace O2 analyzer + dew-point", "env", "Ntron Microx (panel 96 x 96 x 90) + Vaisala DMT143 (Ø28 x 91.6): not drawn yet"),
    ("Argon solenoid manifold", "env", "McMaster 8077K237 x 2 (CAD fetched) on a custom block: not drawn yet"),
    ("Argon pressure regulator", "env", "McMaster 78595A5 (CAD fetched, 91 MB): not drawn yet"),
    ("Vacuum isolation valve", "done", "McMaster 4123K45 (straight ball valve, not an angle valve)"),
    ("Gas-loop + vacuum hoses", "env", "McMaster 3497N23 is a 24 in. hose; routed lengths not matched"),
    ("Guard frame (20 mm T-slot)", "env", "simplified 20 mm profile; BOM S9 lists 30 mm 5537T97"),
    ("Guard-locking door switch", "env", "Omron D4JL-4NFA-C5-NPT: not drawn yet"),
    ("E-stop", "env", "IDEC XA1E-BV3U02-R: not drawn"),
    ("Key switch", "env", "McMaster 6749K3: not drawn"),
    ("Emission indicator", "env", "McMaster 7545K316 + 7545K7: not drawn"),
    ("Reset button", "env", "McMaster 6749K201: not drawn"),
    ("Tray dock", "env", "CombiTac-type: no part number"),
]


def _status(name):
    for sub, st, why in GENERIC:
        if name.startswith(sub) or sub in name:
            return st, why
    return "design", ""


def inventory():
    sys.path.insert(0, str(HERE))
    import lpbf_low as M
    parts = M.build(include_tray=True, fasteners=False)
    P = M.P
    ch = (-P["cx"], P["cx"], -P["cy"], P["cy"], -P["floor"], P["lid_z1"])
    rows = []
    for p in parts:
        st, why = _status(p.name)
        if st == "design":
            continue
        b = p.shape.BoundingBox()
        dx = max(ch[0] - b.xmax, b.xmin - ch[1], 0.0)
        dy = max(ch[2] - b.ymax, b.ymin - ch[3], 0.0)
        dz = max(ch[4] - b.zmax, b.zmin - ch[5], 0.0)
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        tier = "A" if (dist <= 100.0 or p.group) else ("B" if p.module == "process" else ("C" if p.module == "gas" else "D"))
        rows.append(dict(name=p.name, bom=p.bom, module=p.module, group=p.group, status=st, real=why,
                         ext=f"{b.xlen:.0f} x {b.ylen:.0f} x {b.zlen:.0f}", bbox_l=round(b.xlen * b.ylen * b.zlen / 1e6, 3),
                         dist_mm=round(dist, 0), tier=tier))
    rows.sort(key=lambda r: (r["tier"], -r["bbox_l"]))
    for k, r in enumerate(rows, 1):
        r["rank"] = k
    OUT.mkdir(parents=True, exist_ok=True)
    import csv
    with open(OUT / "inventory.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["rank", "tier", "name", "status", "real", "bom", "module", "group", "ext", "bbox_l", "dist_mm"])
        w.writeheader()
        w.writerows(rows)
    lines = ["# Bought parts drawn as envelopes or generic shapes in `lpbf_low.build()`", "",
             "Written by `cad/vendor_parts.py inventory`. Tier A: within 100 mm of the chamber or moving; B: rest of the process",
             "module (optics bridge, guard); C: gas module; D: rack and tray. Ranked by tier, then by bounding-box volume.",
             "Status: **done** = a real-part builder is in `vendor_parts.py`; env = still an envelope or generic shape; checked =",
             "already drawn to the vendor's CAD.", "",
             "| Rank | Tier | Part | Status | Real part / why not | BOM | Size (mm) | Box (L) | To chamber (mm) |", "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['rank']} | {r['tier']} | {r['name']} | {'**done**' if r['status'] == 'done' else r['status']} | {r['real']} | {r['bom']} | {r['ext']} | {r['bbox_l']} | {r['dist_mm']:.0f} |")
    (OUT / "inventory.md").write_text("\n".join(lines) + "\n")
    print(len(rows), "bought parts;", sum(r["status"] == "done" for r in rows), "replaced")


def _load_step(path):
    vals = cq.importers.importStep(str(path)).vals()
    return vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)


def _ext(s):
    b = s.BoundingBox()
    return sorted([round(b.xlen, 2), round(b.ylen, 2), round(b.zlen, 2)])


def verify(keys=None):
    """Volume and sorted bbox extents of our shapes against the vendor CAD in /tmp (where it exists)."""
    ours = {"mcm_6709K12": mcm_6709K12, "mcm_4566N401": mcm_4566N401, "mcm_6627T91": mcm_6627T91,
            "mcm_5786N23": lambda: kf_weld_stub(25), "mcm_5786N25": lambda: kf_weld_stub(40),
            "mcm_4518K72": lambda: kf_wing_clamp(25), "mcm_4518K73": lambda: kf_wing_clamp(40),
            "mcm_4123K45": lambda: mcm_4123K45("-x"), "mcm_3861N11": mcm_3861N11, "mcm_5169K72": mcm_5169K72,
            "clearpath_sd_231x": clearpath_sd_231x, "mcm_4396K21": mcm_4396K21, "thorlabs_fth160_1064": thorlabs_fth160_1064,
            "scanlab_basicube20": scanlab_basicube20, "ipg_collimator_d5": ipg_collimator_d5, "ipg_ylr500_u3": ipg_ylr500_u3,
            "eaton_5px1500rtg2": eaton_5px1500rtg2, "mcm_6709K33": lambda: mcm_6709K33(270.0)}
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / "verify.json"                       # merge into earlier results, keyed by builder
    res = [r for r in (json.loads(f.read_text()) if f.exists() else []) if not keys or r["key"] not in keys]
    for k, fn in ours.items():
        if keys and k not in keys:
            continue
        s = fn()
        r = dict(key=k, pn=SOURCES[k]["pn"], ours_mm3=round(s.Volume(), 1), ours_ext=_ext(s), vendor_mm3=None, vendor_ext=None)
        cad = SOURCES[k]["cad"]
        if cad and pathlib.Path(cad).exists():
            try:
                v = _load_step(cad)
                r["vendor_mm3"], r["vendor_ext"] = round(v.Volume(), 1), _ext(v)
                if k == "mcm_3861N11":      # drop the coiled 36 in. lead (the solid that reaches furthest)
                    sol = sorted(v.Solids(), key=lambda q: -max(q.BoundingBox().xlen, q.BoundingBox().ylen, q.BoundingBox().zlen))
                    rest = cq.Compound.makeCompound(sol[1:])
                    r["vendor_note"] = f"without the coiled lead: {rest.Volume():.0f} mm3, extents {_ext(rest)}"
                r["dvol_pct"] = round(100.0 * (r["ours_mm3"] - r["vendor_mm3"]) / r["vendor_mm3"], 1)
                r["dext_max_mm"] = round(max(abs(a - b) for a, b in zip(r["ours_ext"], r["vendor_ext"])), 2)
            except Exception as e:     # report and carry on
                r["vendor_note"] = f"{type(e).__name__}: {e}"
        res.append(r)
        print(json.dumps(r), flush=True)
        f.write_text(json.dumps(sorted(res, key=lambda q: q["key"]), indent=1))
    return res


def swapcheck(skip=()):
    """Swap each builder into build() and intersect it (exact OCC boolean) with every part whose box it touches."""
    sys.path.insert(0, str(HERE))
    import lpbf_low as M
    parts = M.build(include_tray=True, fasteners=True)
    res = []
    OUT.mkdir(parents=True, exist_ok=True)
    for sw in swaps(M):
        if any(s in sw["replaces"][0] for s in skip):
            continue
        new = sw["shape"]
        nb = new.BoundingBox()
        old = [p for p in parts if any(p.name.startswith(n) for n in sw["replaces"])]
        hits, old_hits = [], []
        for p in parts:
            if any(p.name.startswith(n) for n in sw["replaces"]) or "context" in p.tags:
                continue
            pb = p.shape.BoundingBox()
            if pb.xmin > nb.xmax or pb.xmax < nb.xmin or pb.ymin > nb.ymax or pb.ymax < nb.ymin or pb.zmin > nb.zmax or pb.zmax < nb.zmin:
                continue
            try:
                v = new.intersect(p.shape).Volume()
            except Exception as e:
                v = float("nan")
            if v > 0.5 or v != v:
                ov = sum(o.shape.intersect(p.shape).Volume() for o in old) if old else 0.0
                hits.append(dict(part=p.name, mm3=round(v, 1), envelope_mm3=round(ov, 1)))
        ob = old[0].shape.BoundingBox() if old else None
        r = dict(replaces=sw["replaces"][0], found=bool(old), line=sw["line"], note=sw["note"],
                 new_bbox=[round(x, 1) for x in (nb.xmin, nb.xmax, nb.ymin, nb.ymax, nb.zmin, nb.zmax)],
                 old_bbox=[round(x, 1) for x in (ob.xmin, ob.xmax, ob.ymin, ob.ymax, ob.zmin, ob.zmax)] if ob else None,
                 hits=hits)
        res.append(r)
        print(json.dumps(r), flush=True)
        (OUT / "swapcheck.json").write_text(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if cmd == "inventory":
        inventory()
    elif cmd == "verify":
        verify(sys.argv[2:] or None)
    elif cmd == "swapcheck":
        swapcheck()
