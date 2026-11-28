"""Electrical parts that electrical.md section 0 listed as missing from the model (issue #260, PR #266, round 5). Called from
one hook line at the end of lpbf_low.build(), after joints.py and automation.py:

    electrical_parts.add_features(add, sys.modules[__name__], module)

Drawn here (every part tagged "electrical"; mounts and envelopes, no cable routes):
  1. PB1, the power box: a 16 x 12 x 6 in steel NEMA 12 enclosure on a two-rail stand on the tray, left of the rack (the
     place cad/electrical.py checked), with the padlockable disconnect handle on its front side wall and the filter fan on
     its door (-x). It holds Q0, Q1-Q4, KM0-KM2, K1, K2, the SSR, the DC supplies and the PE bar (electrical.md 1.1);
  2. PB2, the process-module Pi box, on the optics bridge behind the galvo: 0.19-0.22 m in a straight line from the layer
     camera, the NFC antenna and the load cell, so the CSI ribbon and the I2C cables stay under 0.5 m (electrical.md 0 point 8);
  3. the Z stage's home (top) and lower-limit sensors: two M8 inductive sensors in a bracket on the actuator body, reading a
     steel flag on the carriage; the lower one sits 14 mm below the flag's swap-release position, so the 45 mm release
     drop does not trip it (electrical-io.csv M-06);
  4. the recoater's home and far over-travel sensors: two M12 magnetic-field sensors outside the chamber's back wall, each on
     a 20 mm T-slot post bolted to the process base plate, reading a magnet on the carriage block through the 16 mm 6061
     wall and the 0.5 mm 316L liner (no chamber port and no hole in the frame; electrical-io.csv M-04, M-05);
  5. the guard-position switch, separate from the guard lock (ISO 14119), on the door rail between the lock and the handle's
     open position;
  6. two more E-stops: on the guard's right side panel near its front corner, and on the front of the gas module's O2 box
     (electrical-io.csv S-02, S-03);
  7. the dock's two leading PE contacts on the dock's mating face (protective-conductor current ~8 mA, electrical.md 8).

The Pirani gauge on its KF-25 tee at the vacuum port is drawn in lpbf_low.py section 10, next to the vacuum line it sits on.

Not drawn: the LED bar's feedthrough. The only chamber opening it could share is the vacuum port, on the chamber side of the
isolation valve, and a tee or cross there pushes the valve 76-100 mm through the guard's right panel; electrical.md
2026-11-23 says why and what to do instead.

Mounting holes: where a part bolts to a machined part (the process base plate, the optics bridge), the screw is a real
McMaster part from fasteners.py and its hole is cut in that part with joints.py's helpers, as joints.py does.
"""
from __future__ import annotations

import cadquery as cq

import joints as J

V = cq.Vector
TAG = ("electrical",)
IN = 25.4

# real parts (electrical-bom.csv has the prices, URLs and read times)
PB1 = dict(w=6 * IN, d=12 * IN, h=16 * IN, x1=-1008.0, y0=-300.0, stand=15.0,   # 16 x 12 x 6 in (electrical-bom.csv E1-10)
           pn="16 x 12 x 6 in steel NEMA 12 wall-mount enclosure, McMaster 7812K class (envelope from the nominal size)")
PB2 = dict(L=160.0, W=90.0, H=60.5, pn="Hammond 1554JGY polycarbonate box, IP66, 160 x 90 x 60.5 mm")
M8_SENSOR = dict(d=8.0, L=30.0, conn_d=10.0, conn_L=10.0, pn="AutomationDirect KSE-AP-3F inductive M8, PNP NO, 3 mm flush, 40 mm long")
MAG_SENSOR = dict(d=12.0, L=50.0, conn_d=14.0, conn_L=12.0, pn="Turck BIM-M12E-AP4X-H1141 magnetic-field sensor M12, PNP NO, 62 mm long")


def _closure_parts(add):
    """lpbf_low.build()'s parts list (the list add() appends to), so holes can be cut in machined parts."""
    for c in add.__closure__ or ():
        if isinstance(c.cell_contents, list):
            return c.cell_contents
    return []


def add_features(add, M, module):
    P, C = M.P, M.C
    box, cyl, fuse, comp, tube = M.box, M.cyl, M.fuse, M.comp, M.tube
    parts = _closure_parts(add)
    zt = M.Z_TRAY
    cx, cy = P["cx"], P["cy"]

    # ---------------------------------------------------------------- 1. PB1 power box, left of the rack
    x1, x0 = PB1["x1"], PB1["x1"] - PB1["w"]
    y0, y1 = PB1["y0"], PB1["y0"] + PB1["d"]
    z0, z1 = zt + PB1["stand"], zt + PB1["stand"] + PB1["h"]
    add(f"Power box PB1: main disconnect Q0, branch breakers Q1-Q4, KM0-KM2, K1/K2, SSR and the DC supplies ({PB1['pn']})",
        box(x0, x1, y0, y1, z0, z1), C["white"], 13, (-200, 0, 0), mat="steel", mass_kg=16.0, module="tray", bom="E1", tags=TAG)
    rails = [box(x0 + 10.0, x1 - 10.0, y, y + 30.0, zt, z0) for y in (y0 + 20.0, y1 - 50.0)]
    add("PB1 stand (2 x 30 x 15 mm 6061 rails, bolted to the tray)", comp(rails), C["alu_dark"], 13, (-200, 0, 0), mat="al6061", module="tray",
        bom="E1", tags=TAG)
    # Socomec 147E1111 handle on the front (-y) side wall, on its 150 mm shaft 14070515 to the 22013003 switch inside
    hnd = fuse([box(-1110.0, -1060.0, y0 - 12.0, y0, zt + 250.0, zt + 330.0), cyl(14.0, (-1085.0, y0 - 12.0, zt + 290.0), "-y", 30.0),
                box(-1089.0, -1081.0, y0 - 50.0, y0 - 42.0, zt + 240.0, zt + 340.0)])
    add("PB1 disconnect handle Q0 (Socomec 147E1111, red/yellow, padlockable in OFF; 22013003 UL 98 switch inside)", hnd, C["red"], 13,
        (-200, -100, 0), mat="misc", mass_kg=0.3, module="tray", bom="E1", tags=TAG)
    # Fandis FF12D24UN filter fan (cut-out 125 x 125 mm class) low on the door, exhaust grille high
    fan = comp([box(x0 - 12.0, x0, y0 + 90.0, y0 + 240.0, z0 + 40.0, z0 + 190.0), box(x0 - 12.0, x0, y0 + 90.0, y0 + 240.0, z1 - 170.0, z1 - 20.0)])
    add("PB1 filter fan Fandis FF12D24UN (27 CFM, 24 V DC) and exhaust grille on the door", fan, C["black"], 13, (-260, 0, 0), mat="misc",
        mass_kg=0.6, module="tray", bom="E1", tags=TAG)

    # ---------------------------------------------------------------- 2. PB2 Pi box on the optics bridge, behind the galvo
    zb = P["z_bridge1"]
    bx0, by0 = -40.0, 75.0
    bx1, by1 = bx0 + PB2["L"], by0 + PB2["W"]
    body = box(bx0, bx1, by0, by1, zb, zb + PB2["H"])
    tabs = [box(x, x + 14.0, by0 + 20.0, by1 - 20.0, zb, zb + 4.0) for x in (bx0 - 14.0, bx1)]
    add(f"PB2 process-module box: Raspberry Pi 5, PN532 NFC, NAU7802 load-cell ADC, DDR-30G-5, E3NX amplifier, M12 junction ({PB2['pn']})",
        fuse([body] + tabs), C["white"], 9, (0, 120, 200), mat="pc", mass_kg=0.9, module="process", bom="C6", tags=TAG)
    m4 = J.find("shcs", 4, 10, style="a")
    pts = [((x, y, zb + 4.0), (0, 0, -1)) for x in (bx0 - 7.0, bx1 + 7.0) for y in (by0 + 30.0, by1 - 30.0)]
    tools = [J.hole(p, n, -0.01, 4.2, J.CLEAR[4]) for p, n in pts]
    J.cut_parts([p for p in parts if p.name.startswith("PB2 process-module box")], "PB2 process-module box", tools)
    J.cut_parts(parts, "Optics bridge (6061", [J.hole(p, n, 4.0, 4.0 + 12.0, 4.0) for p, n in pts], must=False)   # M4 tapped, 12 deep
    J.add_fasteners(M, add, "electrical_pb2", "PB2 to the optics bridge, M4 x 10", m4, pts, 9, "C6", tags=TAG)

    # ---------------------------------------------------------------- 3. Z home and lower-limit sensors
    # carriage x -21..21, y 56..66, z -153..-113 at z_p = 0 (zstage group); actuator body x -23..23, y 66..94 (fixed)
    zf = -133.0                                                     # flag centre at z_p = 0
    flag = box(-31.0, -21.0, 59.0, 65.5, zf - 6.0, zf + 6.0)
    add("Z sensor flag (2 mm steel tab on the carriage's -x side)", flag, C["steel"], 3, (0, 0, -150), group="zstage", mat="steel",
        mass_kg=0.01, module="process", bom="E3", tags=TAG)
    # home at the top (z_p = +8: flag at zf + 8), lower limit 14 mm below the flag's swap-release position (zf - 45), so the
    # release does not trip it and a runaway past it does
    zs = {"home (top, z_p = +8)": zf + 8.0, "lower limit (14 mm below the swap release)": zf - 45.0 - 14.0}
    br = [box(-27.0, -23.0, 66.0, 94.0, min(zs.values()) - 8.0, max(zs.values()) + 8.0)]
    sens = []
    for nm, z in zs.items():
        blk = fuse([box(-44.0, -32.0, 57.0, 69.0, z - 6.0, z + 6.0), box(-32.0, -23.0, 66.5, 69.0, z - 6.0, z + 6.0)])
        br.append(blk.cut(cyl(M8_SENSOR["d"] / 2 + 0.02, (-45.0, 63.0, z), "x", 14.0)))
        sens.append(fuse([cyl(M8_SENSOR["d"] / 2, (-32.0 - M8_SENSOR["L"], 63.0, z), "x", M8_SENSOR["L"]),
                          cyl(M8_SENSOR["conn_d"] / 2, (-32.0 - M8_SENSOR["L"] - M8_SENSOR["conn_L"], 63.0, z), "x", M8_SENSOR["conn_L"])]))
    add("Z sensor bracket (6061, clamped to the actuator body's -x side)", fuse(br), C["alu_dark"], 3, (0, 0, -150), mat="al6061",
        module="process", bom="E3", tags=TAG)
    add(f"Z home and lower-limit sensors (2 x {M8_SENSOR['pn']}; 1 mm to the flag)", comp(sens), C["blue"], 3, (0, 0, -150), mat="misc",
        mass_kg=0.04, module="process", bom="E3", tags=TAG)

    # ---------------------------------------------------------------- 4. recoater home and far over-travel sensors
    # carriage block x -128..-84 (centre -106) at park, back face y 92; travel to centre +100. Magnet on the back face, sensors
    # outside the back wall (y 111) at the two ends of travel, at the block's mid-height
    zr = 62.0
    mag = cyl(6.0, (P["x_park"], 90.5, zr), "y", 3.0)
    add("Recoater position magnet (NdFeB Ø12 x 3, bonded into a pocket in the carriage block's back face)", mag, C["steel"], 6, (0, 0, 220),
        group="recoater", mat="steel", mass_kg=0.003, module="process", bom="E3", tags=TAG)
    xs = {"home (park)": P["x_park"] - 4.0, "far over-travel": P["x_end"] + 10.0}
    posts, clamps, msens = [], [], []
    for nm, x in xs.items():
        post = box(x - 10.0, x + 10.0, 131.0, 151.0, P["z_base1"], zr - 12.0).cut(cyl(2.5, (x, 141.0, P["z_base1"] - 0.01), "z", 12.0))
        posts.append(post)
        cl = box(x - 10.0, x + 10.0, cy + 1.0, 151.0, zr - 12.0, zr + 12.0).cut(cyl(MAG_SENSOR["d"] / 2 + 0.02, (x, cy, zr), "y", 41.0))
        clamps.append(cl)
        msens.append(fuse([cyl(MAG_SENSOR["d"] / 2, (x, cy + 0.5, zr), "y", MAG_SENSOR["L"]),
                           cyl(MAG_SENSOR["conn_d"] / 2, (x, cy + 0.5 + MAG_SENSOR["L"], zr), "y", MAG_SENSOR["conn_L"])]))
    add("Recoater sensor posts (2 x 20 mm T-slot, McMaster 47065T101 class, on the process base plate)", comp(posts), C["tslot"], 6, (0, 200, 0),
        mat="al6061", module="process", bom="E3", mcm="TSLOT", tags=TAG)
    add("Recoater sensor clamps (6061, split clamp on each post)", comp(clamps), C["alu_dark"], 6, (0, 200, 0), mat="al6061", module="process",
        bom="E3", tags=TAG)
    add(f"Recoater home and over-travel sensors (2 x {MAG_SENSOR['pn']}; see the magnet through the back wall)", comp(msens), C["blue"], 6,
        (0, 200, 0), mat="misc", mass_kg=0.06, module="process", bom="E3", tags=TAG)
    m5 = J.find("shcs", 5, 25, style="a")
    pts5 = [((x, 141.0, P["z_base0"]), (0, 0, 1)) for x in xs.values()]
    J.cut_parts(parts, "Base plate, process module", [J.hole(p, n, -0.01, P["z_base1"] - P["z_base0"] + 0.01, J.CLEAR[5]) for p, n in pts5], must=False)
    J.add_fasteners(M, add, "electrical_recoater_posts", "Recoater sensor posts to the base plate, M5 x 25 into the post's tapped core", m5, pts5, 6,
                    "E3", tags=TAG)

    # ---------------------------------------------------------------- 5. guard-position switch (separate from the lock)
    gy0, pt = -265.0, 1.5
    gz1 = P["z_bridge1"] + P["galvo_h"] + 25.0
    # between the guard-door handle's top (z 170, which reaches x 197-209 with the door open) and the guard lock (gz1 - 120)
    zg0, zg1 = 176.0, min(240.0, gz1 - 126.0)
    add("Guard-position switch IDEC HS6B-12B05 (2NC + 1NO, tongue actuator on the door; separate from the guard lock, ISO 14119)",
        box(181.0, 200.0, gy0 - pt - 30.0, gy0 - pt - 13.0, zg0, zg1), C["yellow"], 12, (0, -280, 0), mat="misc",
        mass_kg=0.15, bom="S2", tags=TAG)

    # ---------------------------------------------------------------- 6. two more E-stops
    def estop(x0_, x1_, y0_, y1_, z0_, z1_, face):
        enc = box(x0_, x1_, y0_, y1_, z0_, z1_)
        c = ((x0_ + x1_) / 2, (y0_ + y1_) / 2, (z0_ + z1_) / 2)
        if face == "x":
            p0 = (x1_, c[1], c[2])
        else:
            p0 = (c[0], y0_, c[2])
        head = fuse([cyl(20.0, p0, face, 8.0), cyl(15.0, tuple(V(*p0) + V(*M._AX[face]) * 8.0), face, 18.0)])
        return enc, head

    gx1 = 310.0
    enc1, head1 = estop(gx1 + pt, gx1 + pt + 70.0, -250.0, -180.0, 100.0, 170.0, "x")
    enc2, head2 = estop(870.0, 940.0, -310.0, -240.0, -60.0, 10.0, "-y")
    for (enc, head, where, mod) in ((enc1, head1, "guard right side, near the front", "process"), (enc2, head2, "front of the gas module's O2 box", "gas")):
        add(f"E-stop enclosure, {where} (1-hole yellow, 70 x 70 x 70 mm class)", enc, C["yellow"], 12, (0, -200, 0), mat="misc", mass_kg=0.2,
            module=mod, bom="S3", tags=TAG)
        add(f"E-stops IDEC XW1E-BV402M-R, {where} (40 mm mushroom, 2 NC)", head, C["red"], 12, (0, -220, 0), mat="misc", mass_kg=0.05,
            module=mod, bom="S3", tags=TAG)

    # ---------------------------------------------------------------- 8. two leading PE contacts on the dock's mating face
    dx0, dy0 = M.TRAY["inner"][0] / 2 - 110, M.TRAY["inner"][1] / 2 - 90
    pe = [fuse([cyl(4.0, (dx0 + 108.0, y, zt + 115.0), "x", 4.0), cyl(2.5, (dx0 + 112.0, y, zt + 115.0), "x", 3.0)]) for y in (dy0 + 20.0, dy0 + 60.0)]
    add("Dock PE contacts (2 x leading protective-earth contacts on the dock's face, 10 AWG each to PB1's PE bar)", comp(pe), C["yellow"], 13,
        (200, 0, 0), mat="misc", mass_kg=0.02, module="tray", bom="D1", tags=TAG)
