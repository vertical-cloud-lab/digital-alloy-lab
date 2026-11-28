"""SOP 01 (DSC/DTA melting and freezing of atomized powder, #262): an animated walk through every step of
``../sops/01-dsc-solidification.md`` on a modelled bench: the micro riffle splitter, the microbalance, the STA with its
argon and vacuum, the operator, and the data each step produces (synthetic examples from ``../analysis/``).

    python sop01_dsc.py sop01_c1          # one chapter -> out/mp4/sop01_c1.mp4 (PREVIEW=1: a contact sheet in /tmp)
    python sop01_dsc.py join              # out/mp4/sop01.mp4 + out/sop01.json, the step sheet and the preview GIF

Chapters: c1 samples (riffle split, weighing, the record, the chip); c2 equipment and set-up (the STA, crucibles,
loading, pump-down and purge); c3 calibration (standards, tau, the Al check); c4 the program (the run, inside the
furnace, rates, baseline, time); c5 after the run and the analysis; c6 acceptance, the ESPEI export, open questions.
"""
from __future__ import annotations

import math
import sys

import numpy as np
import pyvista as pv

import stage as S
from stage import R, T

import audit
import models_dsc as M
import sop01_lib as L
import sop01_panels as P

BH = S.BENCH_H
TITLE = "SOP 01 · DSC melting and freezing of atomized powder"
CHAPTERS = ["sop01_c1", "sop01_c2", "sop01_c3", "sop01_c4", "sop01_c5", "sop01_c6"]
CR = M.CRUCIBLE
PR = (0.69, 0.075, 0.30)           # a data panel, top right (under the step label)
PL = (0.01, 0.075, 0.30)           # ... top left (under the title)
TW_GRIP = (105.0, 0.0, 0.0)        # where the hand holds the tweezers (the tips are at the origin)
TW_PARK = T((L.TRAY_STA[0] + 60.0, L.TRAY_STA[1] - 30.0, BH + 0.6)) @ R((0, 0, 1), 200)   # tweezers set down by the tray
SP_GRIP = (118.0, 0.0, 1.0)        # ... and the spatula
ALLOW = [("person*glove*", "tweezers*"), ("person*glove*", "spatula*"), ("person*glove*", "jar*"),
         ("person*glove*", "pan_carry*"), ("person*glove*", "riffle_splitter:pan_r*"), ("person*glove*", "bottle*"),
         ("person*glove*", "dsc_sta:furnace*"), ("person*glove*", "dsc_sta:body/dsc_grey*"),
         ("person*glove*", "tray*"), ("tweezers*", "cru*"), ("tweezers*", "chip*"), ("spatula*", "cru*"),
         ("spatula*", "pan_carry*"), ("cru*", "microbalance:body*"), ("cru*", "dsc_sta:body*"), ("cru*", "tray*"),
         ("chip*", "cru*"), ("cru*", "cru*"), ("jar*", "riffle_splitter:body*"), ("pan_carry*", "pan_carry*"),
         ("ethanol*", "*"), ("spoon_heap*", "spatula*"), ("spoon_heap*", "pan_carry*"), ("tray*", "bench/top"),
         ("chip*", "wipe*")]


def cam(target, dist, az, el):
    return S.look(target, dist, az, el)


def body_alpha(op, a):
    """Fade the operator's body (not the gloves) for a close-up of the hands and the tool."""
    for n in op.p.names():
        if "glove" not in n:
            op.sc.alpha[n] = a


def fade_body(op, a0, a1):
    def up(u):
        body_alpha(op, a0 + (a1 - a0) * u)
    return up


def tw_at(P, yaw=-110.0, pitch=26.0, up=0.0, h=None):
    """The tweezers' world pose with their tips on the near rim of a crucible standing at P (base centre), the legs
    running off towards yaw (deg from +x; -90 = towards the operator), tilted up by pitch; `up` lifts it clear. h: the
    grip's height over the base (default the crucible's rim; 0.2 for a lid)."""
    P = np.asarray(P, float)
    yr = math.radians(yaw)
    hz = CR["h"] - 0.6 if h is None else h
    rim = P + np.array([math.cos(yr) * (CR["od"] / 2 - 0.2), math.sin(yr) * (CR["od"] / 2 - 0.2), hz + up])
    return T(rim) @ R((0, 0, 1), yaw) @ R((0, 1, 0), -pitch)


def back_out(Mw, yaw, dist, dz=0.0):
    """A pose moved `dist` mm back along the tool's legs (horizontally, towards yaw) and dz up."""
    yr = math.radians(yaw)
    return T((math.cos(yr) * dist, math.sin(yr) * dist, dz)) @ Mw


def up_(Mw, dz):
    return T((0, 0, dz)) @ Mw


def carry(sc, op, group, poses, side="r", grip=TW_GRIP, lean=None, look=None, extra=None):
    """update(u): `group` along the world poses, the operator's hand on its grip point (the hand follows the tool)."""
    mv = S.path_mover(sc, group, poses)
    st = {}

    def up(u):
        if not st:
            st["lean0"] = op.lean
        mv(u)
        w = sc.world(group)
        g = (w @ np.r_[grip, 1.0])[:3]
        kw = {"hands": {side: tuple(g)}}
        if lean is not None:
            op.lean = st["lean0"] + (lean - st["lean0"]) * u
            kw["lean"] = op.lean
        if look is not None:
            kw["look"] = look
        op.hands[side] = tuple(g)
        op.p.set(**kw)
        if extra is not None:
            extra(u)
    return up


def release(op, side="r", lean=0.0, look=None):
    """update(u): the hand back to rest from where it is, standing up straight."""
    st = {}

    def up(u):
        if not st:
            st["h0"] = np.asarray(op.p.hand_point(side), float)
            st["lean0"] = op.lean
        rest = np.asarray(op.p.rest_hand(side), float)
        h = st["h0"] + (rest - st["h0"]) * u
        op.lean = st["lean0"] + (lean - st["lean0"]) * u
        op.p.set(hands={side: tuple(h) if u < 0.999 else None}, lean=op.lean, look=look)
        op.hands[side] = None if u >= 0.999 else tuple(h)
    return up


def new(name, sub):
    return S.SOPScene(name, f"{TITLE}: {sub}")


def tool_to(sc, op, tool, a, b, via_dz=110.0, lean=14.0, look=None, grip=TW_GRIP, extra=None):
    """The tool from pose a to pose b, lifted to via_dz over the bench in between (clear of the pans and jars)."""
    za, zb = a[2, 3], b[2, 3]
    hi = max(BH + via_dz, za + 20.0, zb + 20.0)
    pa = T((0, 0, hi - za)) @ a
    pb = T((0, 0, hi - zb)) @ b
    return carry(sc, op, tool, [a, pa, pb, b], grip=grip, lean=lean, look=look, extra=extra)


def gauge(sc, rows):
    sc.gauges = list(rows)


# ================================================================================================ chapter 1: samples
def c1():
    sc = new("sop01_c1", "samples")
    lab = L.Lab(sc)
    op = lab.op
    rif, bal, sta = lab.rig["riffle"], lab.rig["bal"], lab.rig["sta"]
    au = audit.Audit(sc, allow=ALLOW)
    op.set(x=-1150.0, y=L.OP_Y - 60.0, hd=0.0)
    sc.card(TITLE, ["Checks: liquidus, solidus, incipient melting, freezing range, fs(T), latent heat",
                    "against Thermo-Calc and pycalphad (equilibrium and Scheil)",
                    "Draft SOP: nothing here has been run on our instrument yet"],
            seconds=4.0, label="SOP 01",
            note="Data panels are synthetic examples made with ../analysis/dsc_solidification.py and espei_export.py.")
    sc.cam = cam((-150, 0, BH + 220), 4300, -8, 17)
    sc.step("Overview", "The DSC bench, left to right | splitter, microbalance, STA, PC; argon and pump", 4.5, None,
            hold=1.0,
            labels=[("micro riffle splitter", rif.world((0, 0, 150)), (0.07, 0.30)),
                    ("microbalance, 1 ug", bal.world(M.BAL_POINTS["top"]), (0.22, 0.22)),
                    ("STA (TG-DSC) to 1600 C", sta.world(M.STA_POINTS["furnace_top"]), (0.50, 0.14)),
                    ("Ar >= 99.999 %", lab.rig["gas"].world((0, 0, 1300)), (0.86, 0.20)),
                    ("vacuum pump", lab.rig["pump"].world((0, 0, 220)), (0.88, 0.62))])
    # ---- the riffle split
    jx, jy = L.JAR
    hop = rif.world(M.RIFFLE_POINTS["hopper_rim"])
    grip = np.array([L.JAR_D / 2 + 12.0, 0.0, 62.0])               # the right hand on the jar's right side

    def jar_pose(u):
        a = T((jx, jy, BH))
        lift = T((jx, jy, BH + 120))
        over = T((hop[0] + 62, hop[1] - 4, hop[2] + 48))
        if u < 0.3:
            return S.blend(a, lift, S.ease(u / 0.3))
        if u < 0.65:
            return S.blend(lift, over, S.ease((u - 0.3) / 0.35))
        k = S.ease((u - 0.65) / 0.35)
        return over @ R((0, 1, 0), -112 * k, (0, 0, L.JAR_H * 0.85))

    near = cam((L.RIF[0] + 50, L.RIF[1] - 30, BH + 120), 1000, -58, 28)
    walk = op.walk(L.RIF[0] + 110.0, L.OP_Y, 0.0)
    sc.step("Samples", "A riffle-split sub-sample, not a scoop off the top", 3.2, walk, hold=0.2, cam_to=near,
            labels=[("Humboldt H-3971C micro riffle splitter", rif.world((-57, 0, 150)), (0.18, 0.18)),
                    ("16 chutes, 3.2 mm", rif.world((-20, -32, 84)), (0.14, 0.55)),
                    ("20-63 um sieve cut, 125 mL jar", (jx, jy, BH + 70), (0.78, 0.66))])
    sc.step("Samples", "A riffle-split sub-sample, not a scoop off the top", 1.6,
            op.reach("r", [op.p.rest_hand("r"), (jar_pose(0) @ np.r_[grip, 1])[:3]], lean=10.0,
                     look=(jx, jy, BH + 60)), hold=0.1)
    sc.step("Samples", "A riffle-split sub-sample, not a scoop off the top", 4.0,
            carry(sc, op, "jar", [jar_pose(k / 12) for k in range(13)], grip=grip, lean=14.0, look=tuple(hop),
                  extra=lambda u: rif.set(feed=min(1.0, max(0.0, (u - 0.82) / 0.15)))),
            hold=0.3)
    sc.step("Samples", "Half runs to each pan through alternate chutes", 3.5,
            rif.move({"feed": (1.0, 0.0), "stream": (0.0, 1.0), "split_l": (0.0, 1.0), "split_r": (0.0, 1.0)}),
            hold=0.6, cam_to=cam((L.RIF[0], L.RIF[1], BH + 70), 640, -55, 24),
            labels=[("receiving pans", rif.world((-38, -42, 30)), (0.20, 0.70))])
    sc.step("Samples", "Repeat on one half, down to about 1 g", 3.5,
            S.together(rif.move({"stream": (1.0, 0.0)}),
                       carry(sc, op, "jar", [jar_pose(1 - k / 12) for k in range(13)], grip=grip, lean=10.0)),
            hold=0.5, cam_to=near)
    # the right pan out, swapped for its carried copy, and to the balance
    pan_grip = np.array([M.RIFFLE["pan_x1"] + 8.0, 0.0, 74.0])      # on the pan's high back
    pan0 = rif.world((0, 0, 0))
    out = np.asarray(rif.inst.joints["pan_r"].vec, float)
    p_out = T(np.add(pan0, out))
    sc.step("Samples", "Take one half to the balance", 2.5,
            S.together(rif.move({"pan_r": (0.0, 1.0)}),
                       op.reach("r", lambda u: (T(out * u) @ T(pan0) @ np.r_[pan_grip, 1.0])[:3], lean=12.0)),
            hold=0.2)
    rif.set(pan_r=1.0)
    sc.show(rif.names["pan_r"] + rif.names["split_r"], 0.0)
    sc.show(lab.pan_names, 1.0)
    sc.gmat["pan_carry"] = p_out
    dest = T((L.PAN_SPOT[0] - (M.RIFFLE["pan_x0"] + M.RIFFLE["pan_x1"]) / 2, L.PAN_SPOT[1], BH))
    up1 = T((0, 0, 110)) @ p_out
    mid = T((0, 0, 140)) @ T(((p_out[0, 3] + dest[0, 3]) / 2, (p_out[1, 3] + dest[1, 3]) / 2, BH))
    over = T((0, 0, 60)) @ dest
    walk = op.walk(L.PAN_SPOT[0] + 90.0, L.OP_Y, 0.0)
    sc.step("Samples", "Take one half to the balance", 4.0,
            S.together(walk, carry(sc, op, "pan_carry", [p_out, up1, mid, over, dest], grip=pan_grip, lean=8.0)),
            hold=0.2, cam_to=cam((L.BAL[0] - 120, L.BAL[1] - 140, BH + 90), 1150, 50, 30))
    bal_close = cam(np.add(bal.world(M.BAL_POINTS["pan"]), (-40, -40, 25)), 440, 50, 28)
    sc.step("Weigh", "Tare an empty alumina crucible on the microbalance", 2.0,
            S.together(release(op, lean=0.0), bal.move({"door": (0.0, 1.0)})), hold=0.3,
            labels=[("Sartorius Cubis II micro balance, 1 ug", bal.world((60, 40, 110)), (0.70, 0.18)),
                    ("round glass draft shield, motorized", bal.world(M.BAL_POINTS["door_grip"]), (0.75, 0.82))])
    # tweezers: crucible A from the tray onto the pan (a close-up of the hand and the tool)
    tw = "tweezers"
    pA = lab.pocket[0]
    pan_pt = bal.world(M.BAL_POINTS["pan"])
    tw0 = lab.tw_rest()
    pick = tw_at(pA)
    place = tw_at(pan_pt)
    door_out = back_out(place, -110, 75, 6)                       # in front of the open shield, at the pan's height
    sc.step("Weigh", "Tare an empty alumina crucible on the microbalance", 3.0,
            S.together(fade_body(op, 1.0, 0.15),
                       tool_to(sc, op, tw, tw0, pick, via_dz=60, lean=14.0, look=tuple(pA))),
            hold=0.2, cam_to=bal_close)
    L.attach(sc, "cruA", tw)
    sc.step("Weigh", "Tare an empty alumina crucible on the microbalance", 3.0,
            carry(sc, op, tw, [pick, up_(pick, 40), up_(door_out, 30), door_out, up_(place, 3), place],
                  lean=18.0, look=tuple(pan_pt)),
            hold=0.1)
    L.attach(sc, "cruA", bal.group("body"))
    sc.step("Weigh", "Close the shield and tare: 0.000 mg", 2.6,
            S.together(carry(sc, op, tw, [place, up_(place, 3), door_out, up_(door_out, 30)], lean=14.0),
                       S.staged((0.5, 1.0, bal.move({"door": (1.0, 0.0)})))),
            hold=0.8, labels=[("tare: 0.000 mg", bal.world(M.BAL_POINTS["display"]), (0.82, 0.30))])
    # the micro-spatula: powder from the split half into the crucible
    sp = "spatula"
    sp0 = sc.world(sp)
    pan_pw = (sc.world("pan_carry") @ np.r_[(M.RIFFLE["pan_x0"] + M.RIFFLE["pan_x1"]) / 2, 0.0, 4.0, 1.0])[:3]
    dip = T(pan_pw) @ R((0, 0, 1), -95) @ R((0, 1, 0), -60)
    tip_c = np.add(pan_pt, (0, 0, CR["h"] + 3.0))
    over_c = T(tip_c) @ R((0, 0, 1), -110) @ R((0, 1, 0), -22)
    tipped = T(tip_c) @ R((0, 0, 1), -110) @ R((1, 0, 0), 70) @ R((0, 1, 0), -22)
    sp_out = back_out(over_c, -110, 80, 0)
    sc.step("Weigh", "Spoon in 10-25 mg with a micro-spatula", 3.2,
            S.together(S.staged((0.0, 0.4, bal.move({"door": (0.0, 1.0)}))),
                       S.staged((0.0, 0.45, carry(sc, op, tw, [up_(door_out, 30), up_(tw0, 60), tw0], lean=10.0)),
                                (0.45, 1.0, tool_to(sc, op, sp, sp0, dip, via_dz=130, grip=SP_GRIP, lean=12.0,
                                                    look=tuple(pan_pw))))),
            hold=0.1, cam_to=cam(np.add(pan_pt, (-110, -60, 30)), 600, 46, 32))
    heap = "spoon_heap"
    sc.add(f"{heap}/powder", pv.Sphere(radius=1.6, center=(3.0, 0, 0.9), theta_resolution=20, phi_resolution=12),
           S.MATERIALS["al_powder"][:3], heap, specular=0.02)
    sc.parent[heap] = sp
    sc.gmat[heap] = np.eye(4)
    sc.step("Weigh", "Spoon in 10-25 mg with a micro-spatula", 3.4,
            carry(sc, op, sp, [dip, up_(dip, 120), up_(sp_out, 30), sp_out, over_c, tipped], grip=SP_GRIP,
                  lean=16.0, look=tuple(pan_pt),
                  extra=lambda u: (lab.fill("cruA", bed=min(1.0, max(0.0, (u - 0.85) / 0.15))),
                                   sc.alpha.__setitem__(f"{heap}/powder",
                                                        1.0 - min(1.0, max(0.0, (u - 0.85) / 0.15))))),
            hold=0.1)
    sc.step("Weigh", "Close the shield and read: 15.200 mg", 2.6,
            S.together(carry(sc, op, sp, [tipped, over_c, sp_out, up_(sp_out, 60), up_(sp0, 60), sp0],
                             grip=SP_GRIP, lean=8.0),
                       S.staged((0.4, 0.9, bal.move({"door": (1.0, 0.0)})))),
            hold=1.0, labels=[("15.200 mg (10-25 mg)", bal.world(M.BAL_POINTS["display"]), (0.82, 0.30))])
    # its lid, and the second replicate
    lidA = "cruA_lid"
    plid = lab.pocket[4]
    lid_pick = tw_at(plid, pitch=20, h=0.2)
    lid_place = tw_at(np.add(pan_pt, (0, 0, CR["h"])), pitch=20, h=0.2)
    lid_out = back_out(lid_place, -110, 75, 6)
    sc.step("Weigh", "Lid on. Two replicates per alloy | A 15.20 mg, B 15.08 mg", 3.0,
            S.together(S.staged((0.0, 0.4, bal.move({"door": (0.0, 1.0)}))),
                       tool_to(sc, op, tw, tw0, lid_pick, via_dz=60, lean=14.0)),
            hold=0.1, cam_to=bal_close)
    L.attach(sc, lidA, tw)
    sc.step("Weigh", "Lid on. Two replicates per alloy | A 15.20 mg, B 15.08 mg", 2.8,
            carry(sc, op, tw, [lid_pick, up_(lid_pick, 40), up_(lid_out, 30), lid_out, up_(lid_place, 2), lid_place],
                  lean=16.0),
            hold=0.1)
    L.attach(sc, lidA, "cruA")
    lab.fill("cruB", bed=1.0)
    sc.step("Weigh", "Lid on. Two replicates per alloy | A 15.20 mg, B 15.08 mg", 2.6,
            S.together(carry(sc, op, tw, [lid_place, lid_out, up_(lid_out, 50), up_(tw0, 50), tw0], lean=8.0),
                       S.staged((0.4, 0.9, bal.move({"door": (1.0, 0.0)}))), fade_body(op, 0.15, 1.0)),
            hold=1.0, labels=[("B: 15.08 mg, in the tray", tuple(lab.pocket[1] + (0, 0, 4)), (0.30, 0.74))])
    # the run record
    sc.panel("record", P.panel_record(), rect=(0.68, 0.075, 0.30), alpha=0.0)
    sc.step("Record", "Record run ID, sieve cut, humidity, days since atomization", 1.0,
            S.together(sc.fade_panel("record", 0.0, 1.0), release(op)), hold=4.0,
            cam_to=cam((L.BAL[0] - 140, L.BAL[1] - 110, BH + 60), 1250, -42, 30))
    sc.step("Record", "Record run ID, sieve cut, humidity, days since atomization", 0.6,
            sc.fade_panel("record", 1.0, 0.0), hold=0.0)
    # the printed or cast chip
    chip_c = np.array([L.CHIPS[0] + 25, L.CHIPS[1], BH + 0.3])
    cube_c = np.array([L.CHIPS[0], L.CHIPS[1], BH + 0.3])
    chip_cam = cam((chip_c[0] - 12, chip_c[1] + 5, BH + 8), 300, -52, 38)
    sc.step("Chip", "Printed or cast: a chip of similar mass | from a cube or the crucible remnant", 3.0,
            op.walk(L.CHIPS[0] + 120.0, L.OP_Y, 0.0), hold=1.2, cam_to=chip_cam,
            labels=[("10 mm printed cube", tuple(cube_c + (0, 0, 10)), (0.25, 0.25)),
                    ("chip, about 15 mg, ground flat on one side", tuple(chip_c + (0, 0, 1.1)), (0.70, 0.30))])

    def tw_chip(Pc, up=0.0, pitch=30.0):
        return T(np.add(Pc, (0, -1.4, 0.55 + up))) @ R((0, 0, 1), -90) @ R((0, 1, 0), -pitch)
    held = tw_chip(chip_c, 14.0)
    cur = sc.world(tw)
    sc.step("Chip", "Clean it in ethanol and dry it", 2.6,
            S.together(fade_body(op, 1.0, 0.15),
                       tool_to(sc, op, tw, cur, tw_chip(chip_c), via_dz=70, lean=14.0, look=tuple(chip_c))),
            hold=0.1)
    L.attach(sc, "chip", tw)
    bot = sc.world("bottle")
    squirt_at = T((chip_c[0] - 70, chip_c[1] + 70, BH + 60)) @ R((0, 0, 1), 145) @ R((1, 0, 0), -30)
    stream = "ethanol"
    nozzle = (squirt_at @ np.r_[0.0, -48.0, 160.0, 1.0])[:3]
    target = (held @ np.r_[0.0, 0.0, 1.0, 1.0])[:3]
    sc.add(f"{stream}/jet", pv.Line(tuple(nozzle), tuple(target), resolution=1).tube(radius=0.45, n_sides=12),
           S.MATERIALS["water_clear"][:3], stream, opacity=0.5, specular=0.6)
    sc.alpha[f"{stream}/jet"] = 0.0
    sc.step("Chip", "Clean it in ethanol and dry it", 3.4,
            S.together(carry(sc, op, tw, [tw_chip(chip_c), held], lean=12.0),
                       carry(sc, op, "bottle", [bot, T((0, 0, 70)) @ bot, squirt_at], side="l",
                             grip=(-36.0, 0.0, 70.0), lean=12.0,
                             extra=lambda u: sc.alpha.__setitem__(f"{stream}/jet", 1.0 if u > 0.85 else 0.0))),
            hold=1.0, cam_to=cam((chip_c[0] - 20, chip_c[1] + 10, BH + 30), 380, -55, 30))
    sc.alpha[f"{stream}/jet"] = 0.0
    pC = lab.pocket[3]
    drop = tw_chip(np.add(pC, (0, 0, CR["floor"] + 0.1)), pitch=62.0)
    sc.step("Chip", "Dried, into a crucible, flat side down", 3.2,
            S.together(carry(sc, op, "bottle", [squirt_at, T((0, 0, 70)) @ bot, bot], side="l",
                             grip=(-36.0, 0.0, 70.0), lean=10.0),
                       carry(sc, op, tw, [held, up_(held, 40), up_(drop, 40), up_(drop, 6), drop], lean=14.0,
                             look=tuple(pC))),
            hold=0.2, cam_to=cam((pC[0], pC[1], BH + 8), 260, 40, 40))
    L.attach(sc, "chip", "cruC")
    sc.step("Chip", "Dried, into a crucible, flat side down", 2.2,
            S.together(tool_to(sc, op, tw, drop, tw0, via_dz=70, lean=6.0), release(op, side="l"),
                       fade_body(op, 0.15, 1.0)),
            hold=1.0)
    sc.save()
    au.save()


# ================================================================================================ chapter 2: set-up
def sta_frame(sta):
    s = sta.world(M.STA_POINTS["sample"])
    r = sta.world(M.STA_POINTS["ref"])
    return s, r


def c2():
    sc = new("sop01_c2", "equipment and set-up")
    lab = L.Lab(sc)
    op = lab.op
    sta, bal = lab.rig["sta"], lab.rig["bal"]
    au = audit.Audit(sc, allow=ALLOW)
    lab.fill("cruA", bed=1.0)
    lab.fill("cruB", bed=1.0)
    # crucible A and its lid sit in the tray (the lid on it), as at the end of chapter 1
    sc.gmat["cruA_lid"] = T(np.add(lab.pocket[0], (0, 0, CR["h"])))
    L.attach(sc, "cruA_lid", "cruA")
    sc.gmat["cruR_lid"] = T(np.add(lab.pocket[2], (0, 0, CR["h"])))
    L.attach(sc, "cruR_lid", "cruR")
    op.set(x=L.TRAY[0] + 10.0, y=L.OP_Y, hd=0.0)
    sc.cam = cam((700, 0, 900), 3600, 28, 16)
    gas, pump = lab.rig["gas"], lab.rig["pump"]
    sc.step("Set-up", "A heat-flux DSC/STA to 750 C (Al), 1150 C (Cu) | here a NETZSCH STA 449 F5: RT-1600 C, vacuum-tight",
            5.0, None, hold=1.0,
            labels=[("NETZSCH STA 449 F5 Jupiter, 600 x 700 x 650 mm", sta.world((-30, -300, 650)), (0.24, 0.16)),
                    ("3 mass-flow controllers inside", sta.world((-300, 90, 200)), (0.12, 0.62)),
                    ("Ar >= 99.999 %, two-stage regulator", gas.world((0, -30, 1480)), (0.80, 0.18)),
                    ("Edwards RV5 pump, to 1e-2 mbar", pump.world((0, 0, 200)), (0.82, 0.74))])
    # alumina, never platinum
    pt_names = [n for n in sc.actors if n.startswith("ptcru/")]
    trayc = np.array((L.TRAY[0], L.TRAY[1], BH))
    sc.step("Crucibles", "Alumina crucibles with lids, for Al and Cu alloys | 85 uL, 6.8 mm, 99.7 % Al2O3", 3.0,
            None, hold=1.5, cam_to=cam(trayc + (15, -5, 6), 230, -30, 38),
            labels=[("Al2O3 crucible, 85 uL", tuple(lab.pocket[1] + (0, 0, 4)), (0.30, 0.22)),
                    ("its lid", tuple(lab.pocket[5] + (0, 0, 0.4)), (0.62, 0.20))])
    sc.step("Crucibles", "Never platinum with aluminium | molten Al attacks Pt: it ruins the pan, maybe the sensor", 1.0,
            lambda u: sc.show(pt_names, u), hold=4.0,
            labels=[("NOT for Al: Pt/Rh crucible", (L.TRAY[0] + 60.0, L.TRAY[1] - 10.0, BH + 4.0), (0.78, 0.40))])
    sc.show(pt_names, 0.0)
    # carry the tray to the STA
    tray_dest = T((L.TRAY_STA[0], L.TRAY_STA[1], BH))
    for nm in ("cruA", "cruB", "cruR", "cruC", "cruB_lid", "cruC_lid"):
        L.attach(sc, nm, "tray")
    tray0 = sc.world("tray")
    tgrip = (0.0, -26.0, 10.0)
    sc.step("Load", "Take the crucibles to the STA", 5.0,
            S.together(op.walk(L.STA_OP_X, L.OP_Y_STA, 0.0),
                       carry(sc, op, "tray", [tray0, up_(tray0, 140), up_(tray_dest, 140), tray_dest], grip=tgrip,
                             lean=12.0)),
            hold=0.2, cam_to=cam((0, -150, BH + 200), 1900, -35, 22))
    # open the furnace: press safety + up together, the hoist lifts it, then it swings aside
    btn = sta.world(M.STA_POINTS["btn_open"])
    sc.step("Load", "Open the furnace: safety and up together", 2.6,
            S.together(release(op, lean=0.0),
                       S.staged((0.4, 1.0, op.reach("r", [op.p.rest_hand("r"), btn + (0, -22, 0)], lean=6.0)))),
            hold=0.2, cam_to=cam(np.add(sta.world(M.STA_POINTS["sensor"]), (60, -60, -80)), 1500, 52, 22))
    sc.step("Load", "Open the furnace: the hoist lifts it", 3.0,
            S.together(sta.move({"hoist": (0.0, 1.0)}), release(op)), hold=0.2)
    fgrip = sta.world((M.STA_P["xs"] + M.STA_P["f_d"] / 2 + 6, M.STA_P["ys"], M._g["zf"] + 60), piece="furnace")
    sc.step("Load", "Swing the furnace to the side", 3.0,
            S.together(sta.move({"furnace": (0.0, 1.0)}),
                       op.reach("r", lambda u: sta.world((M.STA_P["xs"] - M.STA_P["f_d"] / 2 - 10, M.STA_P["ys"] - 20,
                                                          M._g["zf"] + 60), piece="furnace"), lean=8.0)),
            hold=0.3,
            labels=[("TG-DSC sensor: sample front, reference back", sta.world(M.STA_POINTS["sensor"]), (0.20, 0.30))])
    # tweezers: the empty reference crucible (with lid) on the back position, then the sample crucible on the front
    s_pos, r_pos = sta_frame(sta)
    tw = "tweezers"
    tw_cur = sc.world(tw)
    sens_cam = cam(np.add(sta.world(M.STA_POINTS["sensor"]), (0, -6, 4)), 230, 42, 24)
    pR = lab.tray_world(2)
    pickR = tw_at(pR, pitch=30)
    placeR = tw_at(r_pos, yaw=-100, pitch=30)
    sc.step("Load", "Empty reference crucible, with lid, on the back position", 3.2,
            S.together(release(op), fade_body(op, 1.0, 0.15),
                       tool_to(sc, op, tw, tw_cur, pickR, via_dz=60, lean=10.0, look=tuple(pR))),
            hold=0.1, cam_to=cam(np.add(pR, (0, 0, 10)), 330, -40, 40))
    L.attach(sc, "cruR", tw)
    sc.step("Load", "Empty reference crucible, with lid, on the back position", 3.6,
            carry(sc, op, tw, [pickR, up_(pickR, 120), up_(placeR, 60), up_(placeR, 3), placeR], lean=10.0,
                  look=tuple(r_pos)),
            hold=0.1, cam_to=sens_cam)
    L.attach(sc, "cruR", sta.group("body"))
    pA = lab.tray_world(0)
    pickA = tw_at(pA, pitch=30)
    placeA = tw_at(s_pos, yaw=-100, pitch=30)
    sc.step("Load", "Sample crucible on the front position, close to you", 3.2,
            tool_to(sc, op, tw, placeR, pickA, via_dz=150, lean=10.0, look=tuple(pA)), hold=0.1,
            cam_to=cam(np.add(pA, (0, 0, 10)), 330, -40, 40))
    L.attach(sc, "cruA", tw)
    sc.step("Load", "Sample crucible on the front position, close to you", 3.6,
            carry(sc, op, tw, [pickA, up_(pickA, 120), up_(placeA, 60), up_(placeA, 3), placeA], lean=10.0,
                  look=tuple(s_pos)),
            hold=0.6, cam_to=sens_cam,
            labels=[("sample, 15.20 mg, lid on", tuple(np.add(s_pos, (0, 0, CR["h"]))), (0.25, 0.70)),
                    ("reference: empty crucible and lid", tuple(np.add(r_pos, (0, 0, CR["h"]))), (0.72, 0.22))])
    L.attach(sc, "cruA", sta.group("body"))
    sc.step("Load", "Swing the furnace back and lower it", 3.0,
            S.together(tool_to(sc, op, tw, placeA, TW_PARK, via_dz=150, lean=6.0),
                       S.staged((0.3, 1.0, sta.move({"furnace": (1.0, 0.0)}))), fade_body(op, 0.15, 1.0)),
            hold=0.1, cam_to=cam(np.add(sta.world(M.STA_POINTS["sensor"]), (60, -60, -80)), 1500, 52, 22))
    sc.step("Load", "Swing the furnace back and lower it", 2.6,
            S.together(sta.move({"hoist": (1.0, 0.0)}), release(op)), hold=0.4)
    # pump down and backfill, three times; then the purge
    p_cam = cam((900, -150, 650), 2700, 30, 16)

    def cycles(u):
        k = min(2, int(u * 3))
        f = u * 3 - k
        if f < 0.55:
            p = 1013.0 * (0.01 / 1013.0) ** (f / 0.55)
            ph = "pumping down"
        else:
            p = 0.01 + (1013.0 - 0.01) * min(1.0, (f - 0.55) / 0.4)
            ph = "backfill with Ar"
        gauge(sc, [("cycle", f"{k + 1} of 3"), ("pressure", f"{p:,.2f} mbar" if p < 10 else f"{p:,.0f} mbar"),
                   ("", ph)])
        pump.set(led=1.0 if f < 0.55 else 0.0)
    sc.step("Purge", "Pump down to 1e-2 mbar, backfill with argon | three times, to clear the air", 7.0, cycles,
            hold=0.6, cam_to=p_cam)

    def purge(u):
        gauge(sc, [("purge 1", "Ar 50 mL/min"), ("protective", "Ar 20 mL/min"), ("pressure", "1,013 mbar")])
        sta.set(leds=1.0)
    sc.step("Purge", "Purge with argon at about 50 mL/min | >= 99.999 %, through the mass-flow controllers", 1.0,
            purge, hold=4.0, cam_to=cam(np.add(sta.world(M.STA_POINTS["panel"]), (0, 0, 60)), 900, 25, 18),
            labels=[("purge 1, purge 2, protective", sta.world((-120, -350, 150)), (0.75, 0.70))])
    sc.save()
    au.save()


# ================================================================================================ chapter 3: calibration
def c3():
    sc = new("sop01_c3", "calibration")
    lab = L.Lab(sc)
    op = lab.op
    sta = lab.rig["sta"]
    au = audit.Audit(sc, allow=ALLOW)
    op.set(x=L.STDS[0] + 40.0, y=L.OP_Y_STA, hd=0.0)
    std = np.array((L.STDS[0], L.STDS[1], BH))
    labels = []
    for i, (el, tm, _) in enumerate(M.STANDARDS):
        labels.append((f"{el} {tm}", tuple(std + (-38 + 19 * i, 0, 6.6)), (0.12 + 0.19 * i, 0.22 if i % 2 else 0.78)))
    sc.cam = cam(std + (0, 0, 20), 900, -30, 35)
    sc.step("Calibrate", "Calibrate temperature and enthalpy with pure metals | that bracket the range", 3.5, None,
            hold=0.5, cam_to=cam(std + (0, 0, 4), 300, -20, 50), labels=labels)
    sc.step("Calibrate", "In, Zn, Al for the Al alloys; Ag, Au for Cu | same crucibles, gas and rate as the samples",
            0.5, None, hold=4.0, labels=labels)
    sc.panel("tau", P.panel_tau(), rect=PL, alpha=0.0)
    sens = sta.world(M.STA_POINTS["sensor"])
    sta_cam = cam(np.add(sens, (120, -100, -150)), 1500, 38, 20)
    sc.step("Calibrate", "Fit the time constant tau to the trailing edge | of the Zn or Al standard's peak", 1.2,
            S.together(sc.fade_panel("tau", 0.0, 1.0), sta.move({"glow": (0.0, 0.35)}),
                       lambda u: gauge(sc, [("standard", "Zn, 419.5 C"), ("furnace", f"{30 + 400 * u:.0f} C")])),
            hold=4.5, cam_to=sta_cam)
    sc.step("Calibrate", "Check tau weekly | and after any change of crucible type", 0.5, None, hold=3.5)
    sc.panel("al", P.panel_al(), rect=PL, alpha=0.0)
    sc.step("Calibrate", "Al standard: onset 660.3 +- 0.5 K | heat of fusion about 397 J/g, within 3 %", 1.2,
            S.together(sc.fade_panel("tau", 1.0, 0.0), sc.fade_panel("al", 0.0, 1.0),
                       sta.move({"glow": (0.35, 0.6)}),
                       lambda u: gauge(sc, [("standard", "Al, 660.3 C"), ("furnace", f"{430 + 250 * u:.0f} C")])),
            hold=5.0)
    sc.step("Calibrate", "Al standard: onset 660.3 +- 0.5 K | heat of fusion about 397 J/g, within 3 %", 0.8,
            S.together(sc.fade_panel("al", 1.0, 0.0), sta.move({"glow": (0.6, 0.0)}),
                       lambda u: gauge(sc, [])), hold=0.3)
    sc.save()
    au.save()


# ================================================================================================ chapter 4: the program
def c4():
    sc = new("sop01_c4", "the program")
    lab = L.Lab(sc)
    op = lab.op
    sta = lab.rig["sta"]
    au = audit.Audit(sc, allow=ALLOW)
    s_pos, r_pos = sta_frame(sta)
    # the loaded sensor: sample A (powder, lid) at the front, the reference (lid) behind
    lab.fill("cruA", bed=1.0)
    for nm, pos in (("cruA", s_pos), ("cruR", r_pos)):
        sc.gmat[nm] = T(pos)
        sc.gmat[f"{nm}_lid"] = T(np.add(pos, (0, 0, CR["h"])))
        L.attach(sc, f"{nm}_lid", nm)
        L.attach(sc, nm, sta.group("body"))
    op.set(x=L.PC[0] - 150.0, y=L.OP_Y, hd=-15.0)
    prog = P.program()
    total = prog["total_min"]
    sc.panel("prog", P.panel_program(), rect=PR, alpha=0.0)
    sens = sta.world(M.STA_POINTS["sensor"])
    sta_cam = cam(np.add(sens, (100, -100, -150)), 1600, -30, 18)
    inside = cam(np.add(s_pos, (0, 0, 2.5)), 95, -28, 22)
    lid_names = sc.members("cruA_lid")
    names = {k: f"cruA/{k}" for k in ("bed", "cake", "melt", "bead")}

    def glow_for(Tc):
        return max(0.0, min(1.0, (Tc - 350.0) / 370.0))

    def run(t0, t1, extra=None, see=None):
        """update(u): the program from t0 to t1 (min): the panel's cursor, the furnace glow, the gauge."""
        def up(u):
            tm = t0 + (t1 - t0) * u
            Tc = P.program_T(tm)
            sc.panels["prog"]["u"] = tm / total
            sta.set(glow=0.75 * glow_for(Tc))
            gauge(sc, [("time", f"{int(tm // 60)} h {int(tm % 60):02d} min"), ("furnace", f"{Tc:.0f} C"),
                       ("segment", P.segment_at(tm))])
            if extra is not None:
                extra(u, Tc)
        return up
    sc.cam = sta_cam
    sc.step("Program 1", "Hold at 30 C, then 20 K/min to 450 C", 1.0, sc.fade_panel("prog", 0.0, 1.0), hold=0.2)
    sc.step("Program 1", "Hold at 30 C, then 20 K/min to 450 C", 4.0, run(0.0, 26.0), hold=0.4)
    # inside the furnace, see-through only now: the powder sinters, melts into a bead, freezes, melts again
    def see(a):
        sta.set(**{"~furnace": a, "~hoist": 0.0})
        for n in lid_names:
            sc.alpha[n] = 1.0 - 0.8 * a

    def heat1(u, Tc):
        sinter = min(1.0, max(0.0, (Tc - 560.0) / 50.0))
        melt = min(1.0, max(0.0, (Tc - 600.0) / 40.0))
        lab.fill("cruA", bed=1.0 - sinter, cake=sinter * (1.0 - melt), melt=melt)
    sc.step("Program 2", "Heat 1 at 10 K/min to 720 C, hold 2 min | the powder sinters, then melts into a bead", 1.5,
            lambda u: see(u), hold=0.0, cam_to=inside,
            labels=[("sample crucible: powder", tuple(np.add(s_pos, (0, -2, 3.0))), (0.22, 0.70))])
    sc.step("Program 2", "Heat 1 at 10 K/min to 720 C, hold 2 min | the powder sinters, then melts into a bead", 7.0,
            run(26.0, 55.0, heat1), hold=0.5)

    def cool(u, Tc):
        sol = min(1.0, max(0.0, (631.0 - Tc) / 50.0))                 # freezing starts under the liquidus
        lab.fill("cruA", bed=0.0, cake=0.0, melt=1.0 - sol, bead=sol)
    sc.step("Program 3", "Cool at 10 K/min to 450 C | for undercooling and nucleation, not the liquidus", 5.0,
            run(55.0, 82.0, cool), hold=0.5)

    def heat2(u, Tc):
        melt = min(1.0, max(0.0, (Tc - 577.0) / 60.0))
        lab.fill("cruA", melt=melt, bead=1.0 - melt)
    sc.step("Program 4", "Heat 2 at 10 K/min to 720 C | the solidified bead: closer to Scheil", 5.0,
            run(82.0, 109.0, heat2), hold=0.4)

    def to_rt(u, Tc):
        sol = min(1.0, max(0.0, (631.0 - Tc) / 50.0))
        lab.fill("cruA", melt=1.0 - sol, bead=sol)
    sc.step("Program 4", "Then cool to room temperature: a run of about 2.3 h", 3.5,
            S.together(run(109.0, total, to_rt), lambda u: see(1.0 - u)), hold=0.4, cam_to=sta_cam)
    sc.panel("beta", P.panel_beta(), rect=PR, alpha=0.0)
    sc.step("Program 5", "Repeat on fresh powder at 5 and 20 K/min | extrapolate onset and end to beta -> 0", 1.0,
            S.together(sc.fade_panel("prog", 1.0, 0.0), sc.fade_panel("beta", 0.0, 1.0), lambda u: gauge(sc, [])),
            hold=5.0)
    sc.panel("base", P.panel_baseline(), rect=PR, alpha=0.0)
    sc.step("Program 6", "An empty-crucible baseline each day, subtracted | same program, same crucibles", 1.0,
            S.together(sc.fade_panel("beta", 1.0, 0.0), sc.fade_panel("base", 0.0, 1.0)), hold=5.0)
    sc.step("Time", "About 2-2.5 h a run: three rates fill a day | with an autosampler they run overnight", 1.5,
            S.together(sc.fade_panel("base", 1.0, 0.0), sta.move({"asc": (0.0, 1.0)})), hold=4.0,
            cam_to=cam(np.add(sens, (120, -60, -100)), 1500, 35, 24),
            labels=[("automatic sample changer, 20 positions (option)", sta.world((150.0, -160.0, 300.0)),
                     (0.78, 0.30))])
    sc.step("Time", "About 20 min hands-on per sample", 1.0, sta.move({"asc": (1.0, 0.0)}), hold=3.0)
    sc.save()
    au.save()


# ================================================================================================ chapter 5: after the run
def c5():
    sc = new("sop01_c5", "after the run and the analysis")
    lab = L.Lab(sc)
    op = lab.op
    sta, bal = lab.rig["sta"], lab.rig["bal"]
    au = audit.Audit(sc, allow=ALLOW)
    s_pos, r_pos = sta_frame(sta)
    for nm, pos in (("cruA", s_pos), ("cruR", r_pos)):
        sc.gmat[nm] = T(pos)
        sc.gmat[f"{nm}_lid"] = T(np.add(pos, (0, 0, CR["h"])))
        L.attach(sc, f"{nm}_lid", nm)
        L.attach(sc, nm, sta.group("body"))
    lab.fill("cruA", bead=1.0)
    # the tray waits beside the STA, as in chapter 2
    for nm in ("cruB", "cruC", "cruB_lid", "cruC_lid"):
        L.attach(sc, nm, "tray")
    sc.gmat["tray"] = T((L.TRAY_STA[0], L.TRAY_STA[1], BH))
    sens = sta.world(M.STA_POINTS["sensor"])
    op.set(x=L.STA_OP_X, y=L.OP_Y_STA, hd=0.0)
    tw = "tweezers"
    sc.gmat[tw] = TW_PARK
    sc.cam = cam(np.add(sens, (60, -60, -80)), 1500, 52, 22)
    btn = sta.world(M.STA_POINTS["btn_open"])
    sc.step("After the run", "Cool, open the furnace, take the crucible out", 2.0,
            op.reach("r", [op.p.rest_hand("r"), btn + (0, -22, 0)], lean=6.0), hold=0.1)
    sc.step("After the run", "Cool, open the furnace, take the crucible out", 3.0,
            S.together(sta.move({"hoist": (0.0, 1.0)}), release(op)), hold=0.1)
    sc.step("After the run", "Cool, open the furnace, take the crucible out", 2.6, sta.move({"furnace": (0.0, 1.0)}),
            hold=0.1)
    pickA = tw_at(s_pos, yaw=-100, pitch=30)
    tw0 = sc.world(tw)
    sc.step("After the run", "Cool, open the furnace, take the crucible out", 3.0,
            S.together(fade_body(op, 1.0, 0.15), tool_to(sc, op, tw, tw0, pickA, via_dz=150, lean=10.0)),
            hold=0.1, cam_to=cam(np.add(sens, (0, -6, 4)), 230, 42, 24))
    L.attach(sc, "cruA", tw)
    pocket0 = lab.tray_world(0)
    dropA = tw_at(pocket0, pitch=30)
    sc.step("After the run", "Cool, open the furnace, take the crucible out", 3.2,
            carry(sc, op, tw, [pickA, up_(pickA, 60), up_(dropA, 120), up_(dropA, 4), dropA], lean=8.0),
            hold=0.2, cam_to=cam(np.add(pocket0, (0, 0, 8)), 360, -40, 40))
    L.attach(sc, "cruA", "tray")
    # the mass check at the balance (a cut: the crucible already on the pan)
    pan_pt = bal.world(M.BAL_POINTS["pan"])
    sc.gmat["cruA"] = T(pan_pt)
    L.attach(sc, "cruA", bal.group("body"))
    sc.gmat[tw] = T((L.TOOLS[0], L.TOOLS[1], BH + 0.6)) @ R((0, 0, 1), 200)
    body_alpha(op, 1.0)
    op.set(x=L.BAL[0] - 150.0, y=L.OP_Y, hd=0.0, hands={"r": None}, lean=0.0)
    sc.panel("mass", P.panel_mass(), rect=(0.69, 0.075, 0.30), alpha=0.0)
    sc.step("Mass", "Weigh it again: mass loss under 0.5 % | more means oxidation or evaporation (Mg, Zn)", 1.0,
            sc.fade_panel("mass", 0.0, 1.0), hold=5.0,
            cam_to=cam(np.add(pan_pt, (-40, -40, 25)), 480, 50, 28),
            labels=[("15.170 mg after the run", bal.world(M.BAL_POINTS["display"]), (0.82, 0.62))])
    # the bead (lid off, a close look)
    sc.gmat["cruA_lid"] = T(np.add(pan_pt, (14.0, -6.0, 0.0)))
    L.attach(sc, "cruA_lid", bal.group("body"))
    sc.step("Bead", "The solidified bead: keep it for XRD and SEM", 1.0, sc.fade_panel("mass", 1.0, 0.0), hold=3.5,
            cam_to=cam(np.add(pan_pt, (0, 0, 2)), 70, 30, 55),
            labels=[("bead, about 3.5 mm", tuple(np.add(pan_pt, (0, 0, 2.6))), (0.70, 0.30))])
    # the analysis, at the PC
    pc = np.array((L.PC[0], L.PC[1] + 110.0, BH + 300.0))
    pc_cam = cam(pc, 1700, -20, 8)
    sc.panel("hf", P.panel_heatflow(), rect=(0.015, 0.075, 0.40), alpha=0.0)
    sc.step("Analysis", "dsc_solidification.py on Heat 2 | lag-corrected, sigmoidal baseline", 1.2,
            S.together(sc.fade_panel("hf", 0.0, 1.0), sc.drive_panel("hf", 0.0, 0.0)), hold=0.2, cam_to=pc_cam)
    sc.step("Analysis", "Solidus: the extrapolated onset | liquidus: end of the peak (99.9 %) after the lag correction",
            4.0, sc.drive_panel("hf", 0.0, 1.0), hold=4.0)
    sc.panel("fs", P.panel_fs(), rect=(0.015, 0.075, 0.40), alpha=0.0)
    sc.step("Analysis", "Also 1 %/99 % T, latent heat (J/g), Kou and CSC | measured minus model dT at fs = 0.1-0.9", 1.0,
            S.together(sc.fade_panel("hf", 1.0, 0.0), sc.fade_panel("fs", 0.0, 1.0)), hold=5.5)
    sc.step("Analysis", "Model: Scheil for the MEASURED composition | Thermo-Calc or pycalphad, composition from SOP 05",
            0.5, None, hold=4.5)
    sc.panel("h12", P.panel_h1h2(), rect=(0.015, 0.075, 0.40), alpha=0.0)
    sc.step("Analysis", "Heat 1 vs Heat 2: a lower onset on Heat 1 | is incipient melting of segregated powder", 1.0,
            S.together(sc.fade_panel("fs", 1.0, 0.0), sc.fade_panel("h12", 0.0, 1.0)), hold=5.0)
    sc.step("Analysis", "Heat 1 vs Heat 2: a lower onset on Heat 1 | is incipient melting of segregated powder", 0.6,
            sc.fade_panel("h12", 1.0, 0.0), hold=0.0)
    sc.save()
    au.save()


# ================================================================================================ chapter 6: acceptance
def c6():
    sc = new("sop01_c6", "acceptance, export, open questions")
    lab = L.Lab(sc)
    op = lab.op
    sta, bal = lab.rig["sta"], lab.rig["bal"]
    au = audit.Audit(sc, allow=ALLOW)
    pan_pt = bal.world(M.BAL_POINTS["pan"])
    sc.gmat["cruA"] = T(pan_pt)
    L.attach(sc, "cruA", bal.group("body"))
    lab.fill("cruA", bead=1.0)
    lab.fill("cruB", bed=1.0)
    op.set(x=L.PC[0] - 200.0, y=L.OP_Y, hd=-10.0)
    sens = sta.world(M.STA_POINTS["sensor"])
    sc.cam = cam(np.add(sens, (300, -100, -250)), 2300, 20, 16)
    sc.panel("acc", P.panel_accept(), rect=(0.66, 0.075, 0.33), alpha=0.0)
    sc.step("Acceptance", "Al standard within +-0.5 K and 3 %; replicates within 2 K | mass loss under 0.5 %", 1.0,
            sc.fade_panel("acc", 0.0, 1.0), hold=6.0)
    sc.panel("zpf", P.panel_espei(), rect=(0.60, 0.075, 0.39), alpha=0.0)
    sc.step("Export", "Liquidus and solidus become ESPEI ZPF entries | espei_export.py, plus ORCHID-style rows", 1.0,
            S.together(sc.fade_panel("acc", 1.0, 0.0), sc.fade_panel("zpf", 0.0, 1.0)), hold=6.0)
    sc.step("Open questions", "Which BYU DSC reaches 750 C (1150 C for Cu)? | and does it have an autosampler?", 1.2,
            S.together(sc.fade_panel("zpf", 1.0, 0.0), sta.move({"asc": (0.0, 0.0)})), hold=4.0,
            cam_to=cam(np.add(sens, (0, -100, -200)), 1800, -15, 18))
    pB = lab.pocket[1]
    pC = lab.pocket[3]
    sc.step("Open questions", "Does the oxide shell on the powder distort Heat 1? | compare with a chip of the same alloy",
            2.0, None, hold=3.5, cam_to=cam(np.add((pB + pC) / 2, (0, 0, 3)), 150, -25, 48),
            labels=[("powder", tuple(np.add(pB, (0, 0, 3))), (0.30, 0.30)),
                    ("chip", tuple(np.add(pC, (0, 0, 2))), (0.70, 0.30))])
    sc.step("Open questions", "Name the primary phase before a ZPF entry | XRD or SEM of the DSC bead", 2.0, None,
            hold=4.0, cam_to=cam(np.add(pan_pt, (0, 0, 2)), 75, 30, 55),
            labels=[("DSC bead", tuple(np.add(pan_pt, (0, 0, 2.6))), (0.70, 0.30))])
    sc.save()
    au.save()


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "sop01_c1"
    if which == "join":
        dst = S.join("sop01", CHAPTERS)
        print(dst, S.contact_sheet("sop01"), S.preview_gif("sop01"))
        return
    {"sop01_c1": c1, "sop01_c2": c2, "sop01_c3": c3, "sop01_c4": c4, "sop01_c5": c5, "sop01_c6": c6}[which]()


if __name__ == "__main__":
    main()
