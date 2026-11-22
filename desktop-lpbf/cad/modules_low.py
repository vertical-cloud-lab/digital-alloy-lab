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
# hermetic glass-to-metal receptacle on the rod end (seals.md item 7). Envelope placeholders, replaced by the vendor's drawing below.
# Envelope: LEMO 1B hermetic receptacle (HGG.1B.310.CLLPV: M12 x 1 panel thread, Ø16 nut) on a Ø19 boss face with an O-ring. That
# part's published rating (2 A per contact, 1e-7 mbar L/s) misses the spec; see seal-parts.csv for the KF-16 parts that meet it.
HERMETIC = dict(label="hermetic receptacle, LEMO 1B envelope (HGG.1B.310)", pn="", mass_kg=0.02, thread_d=12.0, body_in=12.0, flange_d=19.0,
                flange_t=2.5, shell_d=12.0, shell_l=10.0, boss_r=9.5, boss_x=16.0, axis_above_striker=10.0,
                oring="2-014", oring_groove_id=12.6, oring_groove_od=17.2)


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
                    standoffs=[(9.0, 90.0), (9.0, 225.0), (9.0, 315.0)], sd=5.0, tco=(9.0, 45.0))   # r 9.0 (was 9.4): screws clear the seal groove
    if key == "M50":
        return dict(heaters=[(m["bore"] / 4, a) for a in (0.0, 120.0, 240.0)], heater_top=-MP.PLATE_T - 1.0,
                    tcs=[("control", 0.0, 0.0), ("edge", 0.84 * rb, 90.0), ("limit", 7.0, 300.0)],
                    # r = 18 (was 0.8 rb = 20.1) so the stack screws' Ø7 counterbores clear the bore-seal groove
                    standoffs=[(18.0, a) for a in (60.0, 180.0, 300.0)], sd=8.0, tco=(8.0, 180.0))
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
    rod_od, rod_id = MP.ROD_S25 if key == "S25" else (MP.ROD_OD, MP.ROD_ID)
    mg = dict(group="module", module="process")
    pg = dict(group="piston", tags=("in_module",))
    lab = f"{key}"

    # ---------- fixed module body ----------
    spig = h.tube(pr - MP.SPIGOT_FIT, R, (0, 0, zf), "z", MP.FLOOR_T)
    sg = MP.SPIGOT_GROOVE
    spig = spig.cut(h.tube(pr + 1.0, sg["root_d"] / 2, (0, 0, zf + sg["z0"]), "z", sg["width"]))     # O-ring groove (root Ø90.5 x 4.8)
    fl = h.fuse([h.cyl(MP.FLANGE_D / 2, (0, 0, zf - MP.FLANGE_T), "z", MP.FLANGE_T),
                 h.rbox(-MP.TAB_X, MP.TAB_X, -12, 12, zf - MP.FLANGE_T, zf, 6)] +
                [h.cyl(5.5, (0, s * MP.DOWEL_Y, zf - MP.FLANGE_T), "z", MP.FLANGE_T) for s in (-1, 1)] +
                [h.box(-6.0, 6.0, 0, s * MP.DOWEL_Y, zf - MP.FLANGE_T, zf) if s > 0 else h.box(-6.0, 6.0, s * MP.DOWEL_Y, 0, zf - MP.FLANGE_T, zf) for s in (-1, 1)])
    fl = fl.cut(h.cyl(R, (0, 0, zf - MP.FLANGE_T - 1), "z", MP.FLANGE_T + 2))
    for s in (-1, 1):
        fl = fl.cut(h.cyl(3.4, (s * MP.SCREW_X, 0, zf - MP.FLANGE_T - 1), "z", MP.FLANGE_T + 2))
        fl = fl.cut(h.cyl(3.0, (0, s * MP.DOWEL_Y, zf - MP.FLANGE_T - 1), "z", MP.FLANGE_T + 2))      # dowel holes
    tb = h.tube(R + W, R, (0, 0, z_stop), "z", (zf - MP.FLANGE_T) - z_stop)
    rc = R + W + MP.COLLAR_W                                   # collar / gland plate radius
    collar = h.tube(rc, R + W - 0.01, (0, 0, z_stop), "z", MP.COLLAR_T)
    add(f"Build module {lab}: spigot, flange, honed 316L cylinder (Ø{m['bore']:.1f} bore, {W:.0f} mm wall) and bottom collar, one TIG-welded body",
        h.fuse([spig, fl, tb, collar]), C["ss"], step, (0, -320, -60), mat="ss316l", bom="B1", section=True, **mg)
    # drawn as squeezed: from the groove root to the port wall, 4.2 of the groove's 4.8 mm
    add(f"Spigot O-ring (FKM 75A {MP.SPIGOT_ORING}, radial seal in the floor port; groove root Ø{sg['root_d']:.1f} x {sg['width']:.1f})",
        h.tube(pr, sg["root_d"] / 2, (0, 0, zf + sg["z0"] + 0.3), "z", sg["width"] - 0.6), C["black"], step, (0, -320, -60), mat="fkm", bom="B2",
        section=True, **mg)
    h.GLANDS["spigot"] = dict(kind="radial", ring=MP.SPIGOT_ORING, cs=3.53, depth=(MP.PORT_D - sg["root_d"]) / 2, width=sg["width"],
                              groove_d=sg["root_d"], groove_mat="ss", T=60.0, closure="module spigot in the floor port")
    # gland plate: bolted to the collar and the tube end (6 x M4, joints.py), sealed by a face O-ring, so the rod gland can be
    # serviced and powder that gets past the bore seal can be cleaned out of the cylinder's bottom
    rg = MP.ROD_GLAND[key]
    gs, gg = MP.GLAND_PLATE_SEAL[key], MP.GLAND_PLATE_GROOVE
    bf = h.cyl(rc, (0, 0, z_stop - MP.BOT_FLANGE_T), "z", MP.BOT_FLANGE_T).cut(
        h.cyl(rg["throat_d"] / 2, (0, 0, z_stop - MP.BOT_FLANGE_T - 1), "z", MP.BOT_FLANGE_T + 2))
    gi = gs["groove_id"] / 2
    bf = bf.cut(h.tube(gi + gg["width"], gi, (0, 0, z_stop - gg["depth"]), "z", gg["depth"] + 0.1))   # face O-ring groove, 2.6 wide
    # two Parker dynamic rod glands (groove Ø20.0 for the 5/8 in. rod, 3.6 wide), 2.3 mm lands, the lower one the primary seal
    land = (MP.BOT_FLANGE_T - 2 * rg["width"]) / 3
    zr_g = [z_stop - MP.BOT_FLANGE_T + land, z_stop - MP.BOT_FLANGE_T + 2 * land + rg["width"]]
    for zg in zr_g:
        bf = bf.cut(h.tube(rg["groove_d"] / 2, rg["throat_d"] / 2 - 0.01, (0, 0, zg), "z", rg["width"]))
    add(f"Module {lab} bottom flange: gland plate (316L, bolted to the welded collar; two FKM {rg['ring']} rod glands)", bf, C["ss"], step,
        (0, -320, -60), mat="ss316l", bom="B1", section=True, **mg)
    add(f"Module {lab} gland-plate O-ring (FKM 75A {gs['ring']}, face seal on the tube end and collar)",
        h.tube(gi + gg["width"] - 0.2, gi, (0, 0, z_stop - gg["depth"]), "z", gg["depth"]), C["black"], step, (0, -320, -60), mat="fkm", bom="B2", section=True, **mg)
    rcs = MP.AS568[rg["ring"]][1]
    add(f"Rod O-rings {lab} in the bottom flange (2 x FKM 75A {rg['ring']}, dynamic rod glands)",
        h.comp([h.tube(rg["groove_d"] / 2, rod_od / 2, (0, 0, zg + (rg["width"] - rcs) / 2), "z", rcs) for zg in zr_g]), C["black"], step, (0, -320, -60),
        mat="fkm", bom="B2", section=True, **mg)
    h.GLANDS[f"gland_plate_{key}"] = dict(kind="face", ring=gs["ring"], cs=1.78, depth=gg["depth"], width=gg["width"], groove_id=gs["groove_id"],
                                          groove_mat="ss", T=60.0, closure=f"gland plate on the welded collar ({key})")
    h.GLANDS[f"rod_{key}"] = dict(kind="rod", ring=rg["ring"], cs=rcs, depth=(rg["groove_d"] - rod_od) / 2, width=rg["width"], groove_d=rg["groove_d"],
                                  rod_d=rod_od, groove_mat="ss", T=110.0, n=2, closure=f"hollow rod through the gland plate ({key})")
    zt = z_stop - MP.BOT_FLANGE_T                                                         # gland plate's bottom face
    # handle (robot-ops.md, 2026-11-22): the two side arms under the gland plate as before, then a riser in front of the collar, an
    # arm forward under the outlet plenum (4 mm below it) and an I-section grip block in front of the door's hinge knuckles. The block
    # is in the same place for S25, M50 and L75 (MP.MODULE_GRIP), so the gripper takes it from the front without reaching under the
    # chamber; the 2F-85's pads close on the 40 mm web between the two flanges, which carry the 106 N pull and 158 N push by form
    # closure. The old handle sat under the gland plate (y -72 to -28), where the gripper's camera met the door
    G = MP.MODULE_GRIP
    yb0, yb1 = G["y0"], G["y1"]
    zw0, zw1 = G["z_web"]
    ft = G["flange_t"]
    za0, za1 = G["z_arm"]
    # the riser is 6 mm further back than the old handle's cross bar (front face at -rc - 26): on L75 it then passes the guard's bottom
    # front rail at 7.9 mm on the module's path (the robot audit found the cross bar's 1.9 mm too tight)
    hd = h.fuse([h.box(-24, -14, -rc - 20.5, -rc + 12, zt - 4, zt), h.box(14, 24, -rc - 20.5, -rc + 12, zt - 4, zt),
                 h.box(-24, 24, -rc - 26, -rc - 20, zt - 4, za1),                                  # riser in front of the collar
                 h.box(-G["arm_w"] / 2, G["arm_w"] / 2, yb1 - 0.01, -rc - 25.0, za0, za1),         # arm forward under the plenum
                 h.box(-G["web_w"] / 2, G["web_w"] / 2, yb0, yb1, zw0, zw1),                        # grip block: web
                 h.box(-G["flange_w"] / 2, G["flange_w"] / 2, yb0, yb1, zw1, zw1 + ft),            # top flange
                 h.box(-G["flange_w"] / 2, G["flange_w"] / 2, yb0, yb1, zw0 - ft, zw0)])           # bottom flange
    add(f"Module {lab} handle (6061, screwed under the gland plate; riser, arm and I-section robot grip block at y {yb0:.0f} to {yb1:.0f}, "
        f"in front of the door's hinge knuckles)", hd, C["anod"], step, (0, -320, -60), mat="al6061", bom="B1", **mg)

    # ---------- plate and heater stack (moves with the piston, leaves with the module) ----------
    zb1, zb0, zk0, zh0, zc = z["zb1"], z["zb0"], z["zk0"], z["zh0"], z["zc"]
    plate = h.cyl(Rp, (0, 0, zb1), "z", MP.PLATE_T).cut(h.tube(Rp + 1, Rp - 1.5, (0, 0, -7.0), "z", 3.0))
    plate = plate.cut(h.tube(Rp + 1, Rp - 1.2, (0, 0, -3.0), "z", 1.6))                      # wiper groove under the top edge
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
    # 1 mm lower than first drawn: its top was level with the bayonet lugs' underside, and the robot's plate twist hit it
    # (robot-ops.md). The pocket now stops 0.6 mm below the lug channel; the 10 mm body stands 1 mm proud of the block's
    # underside, 1.5 mm above the upper radiation shield.
    blk = blk.cut(h.cyl(2.1, (xt, yt, zb0 - 1), "z", 10.1))
    tcobj.append(h.cyl(2.0, (xt, yt, zb0 - 1.0), "z", 10.0))
    add(f"Plate rim wiper {lab} (carbon-filled PTFE split ring; keeps powder out of the hot gap)",
        h.tube(R, Rp - 1.1, (0, 0, -2.9), "z", 1.4), C["white"], step, (0, 0, 300), mat="ptfe", bom="B2", section=True, **pg)
    add(f"Heater block {lab} (6061-T6, bayonet socket)", blk, C["alu"], step, (0, 0, 250), mat="al6061", bom="H1",
        section=True, **pg)
    add(f"Cartridge heaters {lab} ({m['heaters']} x {m['heater_w']:.0f} W, 24 V, Ø6 x {m['heater_l']:.0f})", h.comp(heaters), C["hot"], step,
        (0, 0, 220), mat="steel", bom="H1", section=True, **pg)
    add(f"Type K thermocouples {lab} (control, edge, limit; 0.04 in. ungrounded, 316 sheath)", h.comp(tcs), C["yellow"], step,
        (0, 0, 220), mat="steel", bom="H1", section=True, **pg)
    add(f"Thermal cutoff {lab} (240 C, in series with the heaters)", h.comp(tcobj), C["red"], step, (0, 0, 220),
        mat="misc", mass_kg=0.002, bom="H2", section=True, **pg)
    # thermal break: each standoff is three Macor rings with the two polished 316 shields clamped between them, all on one
    # stack screw (joints.py: M3, M2.5 on S25) that runs up from a slotted counterbore in the piston head into a helical
    # insert in the heater block. Earlier drafts threaded M3 screws into the Macor itself, which is too weak for threads.
    bore_d = 2.9 if key == "S25" else 3.4                 # screw clearance through the rings and shields
    zsh = (zk0 + MP.BREAK_T / 3, zk0 + 2 * MP.BREAK_T / 3)  # shield mid-planes
    so = []
    for r, a in L["standoffs"]:
        x, y = polar(r, a)
        for z0, z1 in ((zk0, zsh[0] - 0.15), (zsh[0] + 0.15, zsh[1] - 0.15), (zsh[1] + 0.15, zk0 + MP.BREAK_T)):
            so.append(h.cyl(L["sd"] / 2, (x, y, z0), "z", z1 - z0).cut(h.cyl(bore_d / 2, (x, y, z0 - 1), "z", z1 - z0 + 2)))
    add(f"Macor standoff rings {lab} (3 standoffs x 3 rings, Ø{L['sd']:.0f}, cut from 8489K75 rod; thermal break)", h.comp(so), C["white"], step, (0, 0, 200),
        mat="macor", bom="H1", section=True, **pg)
    sh = []
    for zz in zsh:
        d = h.cyl(Rb - 1.0, (0, 0, zz - 0.15), "z", 0.3)
        for r, a in L["standoffs"]:
            x, y = polar(r, a)
            d = d.cut(h.cyl(bore_d / 2, (x, y, zz - 1), "z", 2))
        for r, a in L["heaters"]:
            x, y = polar(r, a)
            d = d.cut(h.cyl(3.4, (x, y, zz - 1), "z", 2))
        for nm, r, a in L["tcs"]:
            x, y = polar(r, a)
            d = d.cut(h.cyl(1.2, (x, y, zz - 1), "z", 2))
        sh.append(d)
    add(f"Radiation shields {lab} (2 x 0.3 mm polished 316, clamped between the Macor rings)", h.comp(sh), C["ss"], step, (0, 0, 190), mat="ss316l",
        bom="H1", section=True, **pg)
    head = h.cyl(Rb, (0, 0, zh0), "z", MP.HEAD_T)
    zs0, zs1 = zh0 + 6.0, zh0 + 12.0                    # bore-seal groove
    sd_ = MP.SEAL_DEPTH.get(key, 3.0)
    head = head.cut(h.tube(Rb + 1, Rb - sd_, (0, 0, zs0), "z", zs1 - zs0))
    head = head.cut(h.cyl(5.0, (0, 0, zh0 + 7.0), "z", MP.HEAD_T))                      # wire hole into the rod
    head = head.cut(h.cyl(rod_od / 2 + 0.02, (0, 0, zh0 - 1), "z", 9.0))               # rod socket (2 set screws, joints.py)
    for r, a in L["heaters"]:                                                             # lead pockets under the heaters
        x, y = polar(r, a)
        head = head.cut(h.cyl(4.0, (x, y, zk0 - 8.0), "z", 8.1))
    for nm, r, a in L["tcs"] + [("tco",) + tuple(L["tco"])]:
        x, y = polar(r, a)
        head = head.cut(h.cyl(1.6, (x, y, zk0 - 3.0), "z", 3.1))
    add(f"Piston head {lab} (6061-T6, cool side of the break; Tier B: 316L with a water channel)", head, C["alu"], step,
        (0, 0, 170), mat="al6061", bom="B1", section=True, **pg)
    add(f"Bore seal {lab} (aramid felt + carbon-filled PTFE scraper)", h.tube(R, Rb - sd_ + 0.2, (0, 0, zs0 + 0.2), "z", zs1 - zs0 - 0.4),
        C["white"], step, (0, 0, 170), mat="felt", bom="B1", mcm="SEAL_PISTON", section=True, **pg)
    zr0 = zc + MP.ROD_END_T
    rod_lab = "3/8 in. x 0.035 in." if key == "S25" else "5/8 in. x 0.065 in."
    add(f"Hollow piston rod {lab} ({rod_lab} seamless 316, polished Ra <= 0.2 um where it runs in the rod glands; inert inside; leads run down it)",
        h.tube(rod_od / 2, rod_id / 2, (0, 0, zr0), "z", zh0 + 8.0 - zr0), C["ss"], step, (0, 0, 140), mat="ss316l",
        bom="B1", section=True, **pg)
    # rod end cap: the rod is TIG-welded into it; a hermetic glass-to-metal receptacle screws into its side boss on an FKM face
    # O-ring, so the gas boundary at the rod end is metal, glass and one static O-ring (was potted stranded leads)
    HC = HERMETIC
    zx = zc + 5.0 + HC["axis_above_striker"]
    cap = h.cyl(11.0, (0, 0, zc + 5.0), "z", MP.ROD_END_T - 5.0).cut(h.cyl(rod_id / 2, (0, 0, zc + 8.0), "z", MP.ROD_END_T))
    cap = h.fuse([cap, h.cyl(HC["boss_r"], (-HC["boss_x"], 0, zx), "x", HC["boss_x"] - 6.0)])
    cap = cap.cut(h.cyl(HC["thread_d"] / 2, (-HC["boss_x"] - 1, 0, zx), "x", HC["boss_x"] - 2.0))            # panel thread / bore
    cap = cap.cut(h.tube(HC["oring_groove_od"] / 2, HC["oring_groove_id"] / 2, (-HC["boss_x"] - 0.01, 0, zx), "x", 1.35))   # face O-ring groove
    add(f"Rod end {lab}: end cap with a side boss for the hermetic connector (316L, rod welded in)", cap, C["ss"], step, (0, 0, 120), mat="ss316l",
        bom="H2", section=True, **pg)
    conn = h.fuse([h.cyl(HC["thread_d"] / 2 - 0.02, (-HC["boss_x"], 0, zx), "x", HC["body_in"]),
                   h.cyl(HC["flange_d"] / 2, (-HC["boss_x"] - HC["flange_t"], 0, zx), "x", HC["flange_t"]),
                   h.cyl(HC["shell_d"] / 2, (-HC["boss_x"] - HC["flange_t"] - HC["shell_l"], 0, zx), "x", HC["shell_l"])])
    add(f"Hermetic connector {lab} on the rod end ({HC['label']})", conn, C["ss"], step, (-60, 0, 120), mat="ss316l", mass_kg=HC["mass_kg"],
        bom="H2", mcm=HC["pn"], section=True, **pg)
    add(f"Hermetic-connector O-ring {lab} (FKM 75A {HC['oring']}, face seal under the flange)",
        h.tube(HC["oring_groove_od"] / 2 - 0.2, HC["oring_groove_id"] / 2, (-HC["boss_x"], 0, zx), "x", 1.32), C["black"], step, (-60, 0, 120),
        mat="fkm", bom="H2", section=True, **pg)
    h.GLANDS[f"hermetic_{key}"] = dict(kind="face", ring=HC["oring"], cs=1.78, depth=1.32, width=(HC["oring_groove_od"] - HC["oring_groove_id"]) / 2,
                                       groove_id=HC["oring_groove_id"], groove_mat="ss", T=40.0, closure=f"hermetic connector on the rod end ({key})")
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
    # 108 (was 100) deep in y so two of its four counterbored M5 screws (joints.py) sit behind the bracket, reachable from below
    add("Z mounting flange (bolted under the floor)", h.box(-40, 100, 60, 108, zf - 10, zf), C["alu"], step, (0, 120, 0), mat="al6061", bom="M3")
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
    """Reservoir docked on the metering base (slides out to the front on the dovetail, 'cartridge' group).

    Sealing (seals.md item 1): every reservoir has the same 30 x 112.4 mm base plate, so one dock takes S, M and L. The
    plate's underside seals on an FKM face O-ring in the dock face round the 12 x 100 mm dose opening; the dovetail rails'
    lips carry a 2 deg ramp over the last 15 mm of travel that pulls the plate 0.5 mm down onto that O-ring as the robot (or
    a hand) pushes it home, and a ball-nose spring plunger holds it there (the model draws the docked pose). The top is a
    welded 304 frame with an O-ring-sealed lid on two M3 screws, and the shutter runs in a slot closed at both ends, so a
    docked reservoir is a sealed part of the gas envelope and is purged with it."""
    C = h.C
    r = MP.RESERVOIRS[key]
    body, zi = reservoir_shape(h, key, xd, z_dock)
    cg = dict(group="cartridge")
    L2 = MP.RES_BASE_HALF_Y
    base = h.box(xd - 15, xd + 15, -L2, L2, z_dock, z_dock + MP.GATE_T).cut(h.box(xd - MP.SLOT_W / 2, xd + MP.SLOT_W / 2, -r["slot"] / 2, r["slot"] / 2, z_dock - 1, z_dock + MP.GATE_T + 1))
    base = base.cut(h.box(xd - 13, xd + 13, -L2 + 3.0, L2 - 3.0, z_dock + 1.0, z_dock + 2.4))       # shutter slot, closed at both ends
    # front pull tab (2026-11-22, operations.md U1.1): the enclosed beam tube runs 15 mm over the lid's handle fin, so a hand can't pinch
    # the fin from the front; it pinches this tab instead, between the rails, 8 mm in front of their ends (the robot keeps the fin)
    tab = h.box(xd - 8.0, xd + 8.0, -L2 - 14.0, -L2 + 0.5, z_dock + 0.5, z_dock + 3.5).cut(h.cyl(4.0, (xd, -L2 - 7.5, z_dock), "z", 5.0))
    base = h.fuse([base, tab])
    # top frame (304, 6 mm, welded on the hopper walls): overhangs the inside by 5 mm (sides) and 12 mm (ends) to carry the lid seal
    zt = zi + r["iz"]
    ox, oy = r["ix"] / 2 + 1.2, r["iy"] / 2 + 1.2
    fx, fy = r["ix"] / 2 - 5.0, r["iy"] / 2 - 12.0
    frame = h.box(xd - ox, xd + ox, -oy, oy, zt, zt + 6.0).cut(h.rbox(xd - fx, xd + fx, -fy, fy, zt - 1, zt + 7.0, 2.0))
    add(f"Reservoir {key} ({r['vol_cm3']:.0f} cm3, 304 SS wedge hopper, {r['slot']:.0f} mm outlet for the {r['for_module']} module; same 30 x 112 mm dock plate for every size)",
        h.fuse([body, base, frame]), C["ss"], step, (0, 0, 380), mat="ss304", bom="R1", mcm="HOPPER", **cg)
    gate = h.box(xd - 12.8, xd + 12.8, -L2 + 3.5, L2 - 3.5, z_dock + 1.1, z_dock + 2.3).cut(
        h.box(xd - MP.SLOT_W / 2, xd + MP.SLOT_W / 2, -r["slot"] / 2, r["slot"] / 2, z_dock, z_dock + 3))
    add(f"Reservoir {key} shutter (shown open, as docked; in a slot closed at both ends, springs shut when the reservoir slides out)", gate, C["steel"], step,
        (0, 0, 360), mat="ss304", bom="R1", **cg)
    fill = r["vol_cm3"] * 0.8
    pw = h.box(xd - r["ix"] / 2 + 0.5, xd + r["ix"] / 2 - 0.5, -r["iy"] / 2 + 0.5, r["iy"] / 2 - 0.5, zi + r["wedge_h"], zi + r["wedge_h"] + max(4.0, (fill * 1000 / (r["ix"] * r["iy"])) - r["wedge_h"] * 0.6))
    add(f"Reservoir {key} powder", pw, C["powder"], step, (0, 0, 380), mat="powder", bom="R1", **cg)
    # lid: 4 mm 6061 on the frame, FKM 1.78 mm face O-ring in its underside (Parker 1.32 x 2.3), two M3 screws (joints.py) into blind
    # tapped holes in the frame outside the seal
    top = zt + 6.0 + 4.0
    hz1 = 258.0
    (gi_x, gi_y) = h.fit_loop((fx + 1.5, fy + 1.5), 3.5, 2.5, 1.0)[0]
    w = MP.FACE_1P78["width"]
    groove = h.rbox(xd - gi_x - w, xd + gi_x + w, -gi_y - w, gi_y + w, zt + 6.0 - 0.01, zt + 6.0 + 1.32, 3.5 + w).cut(
        h.rbox(xd - gi_x, xd + gi_x, -gi_y, gi_y, zt + 5.0, zt + 8.0, 3.5))
    hd = h.box(xd - 4, xd + 4, -30, 30, hz1 - 10, hz1)
    if top - 0.5 < hz1 - 10.0:
        hd = h.fuse([hd, h.box(xd - 4, xd + 4, -6, 6, top - 0.5, hz1 - 9.9)])
    lid = h.fuse([hd, h.box(xd - ox, xd + ox, -oy, oy, zt + 6.0, top)]).cut(groove)
    add(f"Reservoir {key} lid with robot handle (grip plane z = 258 for every size; FKM O-ring face seal on the top frame)", lid,
        C["anod"], step, (0, 0, 420), mat="al6061", bom="R1", **cg)
    ring = h.rbox(xd - gi_x - w + 0.2, xd + gi_x + w - 0.2, -gi_y - w + 0.2, gi_y + w - 0.2, zt + 6.0, zt + 6.0 + 1.32, 3.5 + w - 0.2).cut(
        h.rbox(xd - gi_x, xd + gi_x, -gi_y, gi_y, zt + 5.0, zt + 8.0, 3.5))
    per = 2 * (2 * gi_x + 2 * gi_y) - (8 - 2 * math.pi) * 3.5
    pk = MP.pick_ring(per)
    add(f"Reservoir {key} lid O-ring (FKM 75A {pk[0]})", ring, C["black"], step, (0, 0, 420), mat="fkm", bom="R1", **cg)
    h.GLANDS[f"reservoir_lid_{key}"] = dict(kind="face", ring=pk[0], cs=1.78, depth=1.32, width=w, inner_perimeter=per, groove_mat="al", T=45.0,
                                            closure=f"reservoir {key} lid on its top frame")
    return dict(lid_screws=[(xd, s * (r["iy"] / 2 - 2.5), top) for s in (-1, 1)], frame_top=zt + 6.0)
