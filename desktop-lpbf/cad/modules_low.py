"""Swappable heated build modules, hopper reservoirs and automation parts for the low-profile model (issue #260, PR #266).

lpbf_low.build() calls these with `h` = the lpbf_low module (geometry helpers and colours) and its `add()`. Every
number comes from module_params.py, which analysis/thermal_module.py also reads.

Build module (one of S25, M50, L75 in the machine at a time):
  fixed in the floor port ('module' group): spigot + flange + honed 316L cylinder, radial FKM O-ring, bottom flange
      with the rod gland, a front handle, two captive M6 thumb screws.
  moving with the piston ('piston' group, tagged 'in_module' so it leaves with the module):
      build plate (bayonet spigot, gripper groove) on a heater block (24 V cartridges, 3 type K thermocouples,
      240 C thermal cutoff), three Macor standoffs and two polished 316 shields, the piston head with the bore seal,
      the hollow 316 rod (inert inside) and its rod end: a potted end cap with a side cable exit and a 430 striker.
  Z stage ('zstage' group, follows the piston, offset by its own value): lift arm with a NdFeB pot magnet that
      holds the striker (a floating coupling: the bore centres the piston, the magnet only pulls it down).
"""
from __future__ import annotations

import math

import cadquery as cq

import module_params as MP

V = cq.Vector
BAYONET_R = 6.0          # plate spigot radius; three lugs reach BAYONET_R + 2.5


def polar(r, deg):
    a = math.radians(deg)
    return r * math.cos(a), r * math.sin(a)


def block_layout(key):
    """(heaters, thermocouples, standoffs, standoff dia, thermal cutoff) positions as (r, deg) in the heater block.
    Heater counts follow the thermal FEA: >= 1.5x the worst steady loss at 200 C (47 / 90 / 135 W) in 50 W cartridges."""
    m = MP.MODULES[key]
    rb = m["block_d"] / 2
    if key == "S25":
        return dict(heaters=[(5.5, 0.0), (5.5, 180.0)], heater_top=-MP.PLATE_T - 5.0,
                    tcs=[("control", 0.0, 0.0), ("edge", 10.0, 150.0), ("limit", 7.0, 270.0)],
                    standoffs=[(9.4, 90.0), (9.4, 225.0), (9.4, 315.0)], sd=5.0, tco=(9.0, 45.0))
    if key == "M50":
        return dict(heaters=[(m["bore"] / 4, a) for a in (0.0, 120.0, 240.0)], heater_top=-MP.PLATE_T - 1.0,
                    tcs=[("control", 0.0, 0.0), ("edge", 0.84 * rb, 90.0), ("limit", 7.0, 300.0)],
                    standoffs=[(0.8 * rb, a) for a in (60.0, 180.0, 300.0)], sd=8.0, tco=(8.0, 180.0))
    return dict(heaters=[(m["bore"] / 4, a) for a in (0.0, 72.0, 144.0, 216.0, 288.0)], heater_top=-MP.PLATE_T - 1.0,
                tcs=[("control", 0.0, 0.0), ("edge", 0.8 * rb, 108.0), ("limit", 10.0, 252.0)],
                standoffs=[(0.8 * rb, a) for a in (36.0, 180.0, 324.0)], sd=8.0, tco=(10.0, 36.0))


def zlevels():
    """z of each interface with the plate top at z_p = 0."""
    zb1 = -MP.PLATE_T
    zb0 = zb1 - MP.BLOCK_T
    zk0 = zb0 - MP.BREAK_T
    zh0 = zk0 - MP.HEAD_T
    zc = zh0 - MP.ROD_L                     # coupling face (striker bottom = magnet face)
    return dict(zb1=zb1, zb0=zb0, zk0=zk0, zh0=zh0, zc=zc, z_stop=MP.Z_P_MIN - MP.STACK)


def add_build_module(h, add, key, step=4):
    m = MP.MODULES[key]
    C = h.C
    R, W = m["bore"] / 2, m["wall"]
    Rp, Rb = m["plate_d"] / 2, m["block_d"] / 2
    L = block_layout(key)
    z = zlevels()
    zf = -MP.FLOOR_T
    pr = MP.PORT_D / 2
    z_stop = z["z_stop"]
    mg = dict(group="module", module="process")
    pg = dict(group="piston", tags=("in_module",))
    lab = f"{key}"

    # ---------- fixed module body ----------
    spig = h.tube(pr - MP.SPIGOT_FIT, R, (0, 0, zf), "z", MP.FLOOR_T)
    spig = spig.cut(h.tube(pr, pr - 2.9, (0, 0, zf + 4.0), "z", 3.6))                 # O-ring groove
    fl = h.fuse([h.cyl(MP.FLANGE_D / 2, (0, 0, zf - MP.FLANGE_T), "z", MP.FLANGE_T),
                 h.rbox(-MP.TAB_X, MP.TAB_X, -12, 12, zf - MP.FLANGE_T, zf, 6)])
    fl = fl.cut(h.cyl(R, (0, 0, zf - MP.FLANGE_T - 1), "z", MP.FLANGE_T + 2))
    for s in (-1, 1):
        fl = fl.cut(h.cyl(3.4, (s * MP.SCREW_X, 0, zf - MP.FLANGE_T - 1), "z", MP.FLANGE_T + 2))
    tb = h.tube(R + W, R, (0, 0, z_stop), "z", (zf - MP.FLANGE_T) - z_stop)
    add(f"Build module {lab}: spigot, flange and honed 316L cylinder (Ø{m['bore']:.1f} bore, {W:.0f} mm wall)",
        h.fuse([spig, fl, tb]), C["ss"], step, (0, -320, -60), mat="ss316l", bom="B1", section=True, **mg)
    add(f"Spigot O-ring (FKM {MP.SPIGOT_ORING}, radial seal in the floor port)",
        h.tube(pr, pr - 2.6, (0, 0, zf + 4.3), "z", 3.0), C["black"], step, (0, -320, -60), mat="fkm", bom="B2",
        section=True, **mg)
    bfr = R + W + 6.0
    bf = h.cyl(bfr, (0, 0, z_stop - MP.BOT_FLANGE_T), "z", MP.BOT_FLANGE_T).cut(
        h.cyl(MP.ROD_OD / 2 + 0.05, (0, 0, z_stop - MP.BOT_FLANGE_T - 1), "z", MP.BOT_FLANGE_T + 2))
    add(f"Module {lab} bottom flange (316L, double FKM O-ring rod gland)", bf, C["ss"], step, (0, -320, -60),
        mat="ss316l", bom="B1", section=True, **mg)
    zh = z_stop - MP.BOT_FLANGE_T / 2
    hd = h.fuse([h.box(-22, -16, -bfr - 26, -bfr + 3, zh - 3, zh + 3), h.box(16, 22, -bfr - 26, -bfr + 3, zh - 3, zh + 3),
                 h.box(-22, 22, -bfr - 32, -bfr - 26, zh - 3, zh + 3)])
    add(f"Module {lab} handle (front, for a hand or a gripper)", hd, C["anod"], step, (0, -320, -60), mat="al6061",
        bom="B1", **mg)
    sc = []
    for s in (-1, 1):
        sc += [h.cyl(5.0, (s * MP.SCREW_X, 0, zf - MP.FLANGE_T - 6), "z", 6), h.cyl(3.0, (s * MP.SCREW_X, 0, zf - MP.FLANGE_T), "z", MP.FLANGE_T + 10)]
    add("Captive M6 thumb screws (2, into helical inserts in the floor)", h.comp(sc), C["steel"], step, (0, -320, -60),
        mat="ss316l", bom="B2", **mg)

    # ---------- plate and heater stack (moves with the piston, leaves with the module) ----------
    zb1, zb0, zk0, zh0, zc = z["zb1"], z["zb0"], z["zk0"], z["zh0"], z["zc"]
    plate = h.cyl(Rp, (0, 0, zb1), "z", MP.PLATE_T).cut(h.tube(Rp + 1, Rp - 1.5, (0, 0, -7.0), "z", 3.0))
    lug = h.box(BAYONET_R - 0.5, BAYONET_R + 2.5, -3.0, 3.0, zb1 - 4.0, zb1 - 2.2)
    lugs = [lug.rotate(V(0, 0, 0), V(0, 0, 1), a) for a in (0.0, 120.0, 240.0)]
    add(f"Build plate {lab} (Ø{m['plate_d']:.1f} x {MP.PLATE_T:.0f}, 6061-T6; bayonet spigot, gripper groove)",
        h.fuse([plate, h.cyl(BAYONET_R, (0, 0, zb1 - 4.0), "z", 4.0)] + lugs), C["alu_dark"], step, (0, 0, 300),
        mat="al6061", bom="B1", section=True, **pg)
    blk = h.cyl(Rb, (0, 0, zb0), "z", MP.BLOCK_T)
    blk = blk.cut(h.cyl(BAYONET_R + 0.2, (0, 0, zb1 - 4.3), "z", 4.4)).cut(h.cyl(BAYONET_R + 2.9, (0, 0, zb1 - 4.3), "z", 2.3))
    for a in (60.0, 180.0, 300.0):                      # entry slots for the lugs (locked 60 deg away from them)
        blk = blk.cut(h.box(BAYONET_R - 0.5, BAYONET_R + 2.9, -3.3, 3.3, zb1 - 4.3, zb1 + 0.1).rotate(V(0, 0, 0), V(0, 0, 1), a))
    heaters, tcs, tcobj = [], [], []
    ht = L["heater_top"]
    for r, a in L["heaters"]:
        x, y = polar(r, a)
        blk = blk.cut(h.cyl(3.05, (x, y, zb0 - 1), "z", ht - zb0 + 1))
        heaters.append(h.cyl(3.0, (x, y, ht - m["heater_l"]), "z", m["heater_l"]))
    for nm, r, a in L["tcs"]:
        x, y = polar(r, a)
        top = zb1 - 5.0 if r < BAYONET_R + 3.5 else zb1 - 1.5
        blk = blk.cut(h.cyl(0.6, (x, y, zb0 - 1), "z", top - zb0 + 1))
        tcs.append(h.cyl(0.508, (x, y, zk0 - 1.0), "z", top - zk0 + 1.0))
    xt, yt = polar(*L["tco"])
    blk = blk.cut(h.cyl(2.1, (xt, yt, zb0 - 1), "z", 11.0))
    tcobj.append(h.cyl(2.0, (xt, yt, zb0), "z", 10.0))
    add(f"Heater block {lab} (6061-T6, bayonet socket)", blk, C["alu"], step, (0, 0, 250), mat="al6061", bom="H1",
        section=True, **pg)
    add(f"Cartridge heaters {lab} ({m['heaters']} x {m['heater_w']:.0f} W, 24 V, Ø6 x {m['heater_l']:.0f})", h.comp(heaters), C["hot"], step,
        (0, 0, 220), mat="steel", bom="H1", section=True, **pg)
    add(f"Type K thermocouples {lab} (control, edge, limit; 0.04 in. ungrounded, 316 sheath)", h.comp(tcs), C["yellow"], step,
        (0, 0, 220), mat="steel", bom="H1", section=True, **pg)
    add(f"Thermal cutoff {lab} (240 C, in series with the heaters)", h.comp(tcobj), C["red"], step, (0, 0, 220),
        mat="misc", mass_kg=0.002, bom="H2", section=True, **pg)
    so = []
    for r, a in L["standoffs"]:
        x, y = polar(r, a)
        so.append(h.cyl(L["sd"] / 2, (x, y, zk0), "z", MP.BREAK_T))
    add(f"Macor standoffs {lab} (3 x Ø{L['sd']:.0f} x {MP.BREAK_T:.0f}, thermal break)", h.comp(so), C["white"], step, (0, 0, 200),
        mat="macor", bom="H1", section=True, **pg)
    sh = []
    for zz in (zk0 + MP.BREAK_T / 3, zk0 + 2 * MP.BREAK_T / 3):
        d = h.cyl(Rb - 1.0, (0, 0, zz - 0.15), "z", 0.3)
        for r, a in L["standoffs"]:
            x, y = polar(r, a)
            d = d.cut(h.cyl(L["sd"] / 2 + 0.4, (x, y, zz - 1), "z", 2))
        for r, a in L["heaters"]:
            x, y = polar(r, a)
            d = d.cut(h.cyl(3.4, (x, y, zz - 1), "z", 2))
        for nm, r, a in L["tcs"]:
            x, y = polar(r, a)
            d = d.cut(h.cyl(1.2, (x, y, zz - 1), "z", 2))
        sh.append(d)
    add(f"Radiation shields {lab} (2 x 0.3 mm polished 316)", h.comp(sh), C["ss"], step, (0, 0, 190), mat="ss316l",
        bom="H1", section=True, **pg)
    head = h.cyl(Rb, (0, 0, zh0), "z", MP.HEAD_T)
    zs0, zs1 = zh0 + 6.0, zh0 + 12.0                    # bore-seal groove
    head = head.cut(h.tube(Rb + 1, Rb - 3.0, (0, 0, zs0), "z", zs1 - zs0))
    head = head.cut(h.cyl(5.0, (0, 0, zh0 + 7.0), "z", MP.HEAD_T))                      # wire hole into the rod
    head = head.cut(h.cyl(MP.ROD_OD / 2 + 0.02, (0, 0, zh0 - 1), "z", 9.0))            # rod socket
    for r, a in L["heaters"]:                                                             # lead pockets under the heaters
        x, y = polar(r, a)
        head = head.cut(h.cyl(4.0, (x, y, zk0 - 8.0), "z", 8.1))
    for nm, r, a in L["tcs"] + [("tco",) + tuple(L["tco"])]:
        x, y = polar(r, a)
        head = head.cut(h.cyl(1.6, (x, y, zk0 - 3.0), "z", 3.1))
    add(f"Piston head {lab} (6061-T6, cool side of the break; Tier B: 316L with a water channel)", head, C["alu"], step,
        (0, 0, 170), mat="al6061", bom="B1", section=True, **pg)
    add(f"Bore seal {lab} (aramid felt + carbon-filled PTFE scraper)", h.tube(R, Rb - 2.8, (0, 0, zs0 + 0.2), "z", zs1 - zs0 - 0.4),
        C["white"], step, (0, 0, 170), mat="felt", bom="B1", mcm="SEAL_PISTON", section=True, **pg)
    zr0 = zc + MP.ROD_END_T
    add(f"Hollow piston rod {lab} (5/8 in. x 0.065 in. 316, inert inside; leads run down it)",
        h.tube(MP.ROD_OD / 2, MP.ROD_ID / 2, (0, 0, zr0), "z", zh0 + 8.0 - zr0), C["ss"], step, (0, 0, 140), mat="ss316l",
        bom="B1", section=True, **pg)
    cap = h.cyl(11.0, (0, 0, zc + 5.0), "z", MP.ROD_END_T - 5.0).cut(h.cyl(MP.ROD_ID / 2, (0, 0, zc + 8.0), "z", MP.ROD_END_T))
    cap = h.fuse([cap, h.cyl(4.0, (-26.0, 0, zc + 9.5), "x", 16.0)]).cut(h.cyl(2.8, (-27.0, 0, zc + 9.5), "x", 30.0))
    add(f"Rod end {lab}: potted cable exit (Torr Seal) with a side outlet", cap, C["ss"], step, (0, 0, 120), mat="ss316l",
        bom="H2", section=True, **pg)
    add(f"Striker disc {lab} (416 stainless, on the pot magnet)", h.cyl(12.7, (0, 0, zc), "z", 5.0), C["steel"], step,
        (0, 0, 110), mat="steel", bom="B2", section=True, **pg)


def add_zstage(h, add, step=3):
    """Folded Z stage hung from the chamber floor, sized for the heated stack. Group 'zstage' follows the piston."""
    C = h.C
    zf = -MP.FLOOR_T
    z = zlevels()
    zc = z["zc"]                                         # coupling face at z_p = 0
    a0 = zc - MP.ARM_T
    ax0, ax1, ay0, ay1 = -23.0, 23.0, 66.0, 94.0
    car_lo, car_hi = min(MP.Z_P_MIN, MP.ZSTAGE_RELEASE) + a0, MP.Z_P_MAX + a0 + 40.0
    az0, az1 = car_lo - 3.0, car_hi + 3.0
    zg = dict(group="zstage")
    add("Z mounting flange (bolted under the floor)", h.box(-40, 100, 60, 100, zf - 10, zf), C["alu"], step, (0, 120, 0), mat="al6061", bom="M3")
    add("Z actuator body (KR-class U-rail, 2 mm lead, 100 mm stroke class)", h.box(ax0, ax1, ay0, ay1, az0, az1), C["steel"], step,
        (0, 160, 0), mat="steel", mass_kg=1.4, bom="M3", mcm="ACT_Z")
    bh = h.box(ax0, 100, ay0 - 4, ay1, az1, zf - 10).cut(h.cyl(19.2, (64.0, 80.0, az1 - 1), "z", 3.0)).cut(h.cyl(5.0, (64.0, 80.0, az1), "z", 25))
    add("Z bracket + fold-back belt housing (2:1)", bh, C["anod"], step, (0, 160, 0), mat="al6061", bom="M3")
    add("Z servo (ClearPath-SD, NEMA 23, folded)", h.place(h.servo_nema23(100.0, 18.0), (64.0, 80.0, az1), (1, 0, 0), (0, 0, 1)),
        C["motor"], step, (0, 200, 0), mat="misc", mass_kg=1.6, bom="M2")
    add("Z carriage", h.box(-21, 21, 56, ay0, a0, a0 + 40.0), C["steel"], step, (0, 160, 0), mat="steel", bom="M3", **zg)
    arm = h.rbox(-30, 30, -22, 56, a0, zc, 6).cut(h.cyl(12.7, (0, 0, zc - 7.0), "z", 7.1))
    add("Z lift arm (6061, 12 mm, pot-magnet coupling)", arm, C["alu"], step, (0, -150, 0), mat="al6061", bom="M3", **zg)
    add("Pot magnet (NdFeB in a steel cup, Ø25 x 7, 44 lbf, holds the rod's striker)", h.cyl(12.5, (0, 0, zc - 7.0), "z", 7.0), C["steel"], step,
        (0, -150, 0), mat="steel", bom="B2", **zg)


def reservoir_shape(h, key, xd, z0):
    """Reservoir body: wedge (plane-flow) hopper over an 8 mm outlet slot, interior ix x iy x iz, 1.2 mm 304 walls."""
    r = MP.RESERVOIRS[key]
    t = 1.2
    ix, iy, iz, wh = r["ix"], r["iy"], r["iz"], r["wedge_h"]
    zi = z0 + MP.GATE_T                                   # interior bottom (slot) level
    sw = MP.SLOT_W / 2
    outer = (cq.Workplane("XZ").polyline([(xd - sw - t, zi - 0.01), (xd + sw + t, zi - 0.01), (xd + ix / 2 + t, zi + wh), (xd + ix / 2 + t, zi + iz),
                                          (xd - ix / 2 - t, zi + iz), (xd - ix / 2 - t, zi + wh)]).close()
             .extrude(iy / 2 + t, both=True).val())
    inner = (cq.Workplane("XZ").polyline([(xd - sw, zi - 1), (xd + sw, zi - 1), (xd + sw, zi), (xd + ix / 2, zi + wh), (xd + ix / 2, zi + iz + 1),
                                          (xd - ix / 2, zi + iz + 1), (xd - ix / 2, zi + wh), (xd - sw, zi)]).close()
             .extrude(iy / 2, both=True).val())
    return outer.cut(inner), zi


def add_reservoir(h, add, key, xd, z_dock, step=7):
    """Reservoir docked on the metering base (slides out to the front on the dovetail, 'cartridge' group)."""
    C = h.C
    r = MP.RESERVOIRS[key]
    body, zi = reservoir_shape(h, key, xd, z_dock)
    cg = dict(group="cartridge")
    L2 = r["iy"] / 2 + 1.2
    base = h.box(xd - 15, xd + 15, -L2, L2, z_dock, z_dock + MP.GATE_T).cut(h.box(xd - MP.SLOT_W / 2, xd + MP.SLOT_W / 2, -r["slot"] / 2, r["slot"] / 2, z_dock - 1, z_dock + MP.GATE_T + 1))
    base = base.cut(h.box(xd - 13, xd + 13, -L2 - 1, L2 + 1, z_dock + 1.0, z_dock + 2.4))       # gate slot
    add(f"Reservoir {key} ({r['vol_cm3']:.0f} cm3, 304 SS wedge hopper, {r['slot']:.0f} mm outlet for the {r['for_module']} module)",
        h.fuse([body, base]), C["ss"], step, (0, 0, 380), mat="ss304", bom="R1", mcm="HOPPER", **cg)
    gate = h.box(xd - 12.8, xd + 12.8, -L2 + 0.5, L2 - 0.5, z_dock + 1.1, z_dock + 2.3).cut(
        h.box(xd - MP.SLOT_W / 2, xd + MP.SLOT_W / 2, -r["slot"] / 2, r["slot"] / 2, z_dock, z_dock + 3))
    add(f"Reservoir {key} shutter (shown open, as docked; springs shut when the reservoir slides out)", gate, C["steel"], step,
        (0, 0, 360), mat="ss304", bom="R1", **cg)
    fill = r["vol_cm3"] * 0.8
    pw = h.box(xd - r["ix"] / 2 + 0.5, xd + r["ix"] / 2 - 0.5, -r["iy"] / 2 + 0.5, r["iy"] / 2 - 0.5, zi + r["wedge_h"], zi + r["wedge_h"] + max(4.0, (fill * 1000 / (r["ix"] * r["iy"])) - r["wedge_h"] * 0.6))
    add(f"Reservoir {key} powder", pw, C["powder"], step, (0, 0, 380), mat="powder", bom="R1", **cg)
    top = zi + r["iz"] + 3.0
    hz1 = 258.0
    hd = h.fuse([h.box(xd - 4, xd + 4, -30, 30, hz1 - 10, hz1), h.box(xd - 4, xd + 4, -6, 6, top - 0.5, hz1 - 9.9)])
    add(f"Reservoir {key} lid with robot handle (grip plane z = 258 for every size)", h.fuse([hd, h.box(xd - r["ix"] / 2 - 1.2, xd + r["ix"] / 2 + 1.2, -L2, L2, top - 3.0, top)]),
        C["anod"], step, (0, 0, 420), mat="al6061", bom="R1", **cg)
