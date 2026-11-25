"""The robotic build of the M50 desktop LPBF, step by step, in the order the two-arm cell does it (issue #260, PR #266).

Taken from render_build.py chapters 3-5, joints.py's joint table and analysis/ops/operations.py's A1/A2 lists, then
re-ordered so that every screw is driven from above or from the side and nothing heavy is lifted by one arm:
  * the heater stack is built upside down on a nest (everything drops in from above);
  * the gland plate (face ring, then its two rod rings by the ring loader) waits on its own nest; the rod, its rod end
    welded on by the shop, goes top end first through the plate's rings and then, with the plate riding on it, into the
    head's socket (round 4, 2026-11-22: the welded rod end no longer has to slide on after the rod rings);
  * the module body goes upright onto its nest for the spigot O-ring (the mandrel reaches into the bore), gripped across
    its tube (round 6), then upside down on its spigot face; the whole stack, rod and gland plate drop into the bore from the
    tube's open bottom end, which faces up; then the gland-plate screws (round 6: on the arc behind the rod end's
    feedthrough block, joints.py), the handle (round 6: lowered in front of the rod end's sleeves and slid back) and the
    striker. The rod end is a 316L block with seven weld-in feedthroughs, welded to the rod by the shop, so nothing is
    fitted to it here (round 6: the hermetic connector and the thermal cutoff are gone from the model, electrical.md
    section 13). It is turned upright for the plate, then turned over again for the chamber;
  * the chamber is worked upside down on Fixture C (outlet plenum, overflow funnel, module, Z stage and legs all go on
    from above), then both arms turn it over by two legs onto the base plate, which waits on Fixture B, an open stand
    the arms reach under (posts' and legs' base screws from below);
  * everything else goes on the upright chamber from above or the side.

Step fields (run_assembly.py reads them):
  do       place | screws | seal | flip | dual | note
  keys     name fragments of the model objects (checks.Scene.find), as operations.py
  grp      the sub-assembly the part joins (the part sweep only sees objects already in the same sub-assembly)
  phase    where that sub-assembly is and which way up (cell2.Cell.T_phase)
  path     removal path in the machine frame: offsets from the seated pose, first (0, 0, 0); insertion runs it backwards.
           "explode" = [(0, 0, 0), the part's explode offset] as render_build.py animates it
  tool     gripper | gripper+caps | vacuum | screwdriver | roller | roller_n | hand tools held in the gripper
  actor    A (front arm) or B (back arm); holder: the other arm holds the part at its seat while the actor works
  person   why a person (or a dedicated machine) does the step instead
"""
from __future__ import annotations

UP, DN = (0.0, 0.0, 1.0), (0.0, 0.0, -1.0)
# Round 6: the rod end is a 316L block (x +-40.5, y -22 to +6, zc + 1 to zc + 17 with zc = -141 at z_p = 0) with seven weld-in
# sleeves standing 12-21 mm out of its front face (modules_low.ROD_FT). Run 3 held the rod by its Ø22 end cap with the fingers
# along y, where the front finger now sits inside the block; so arm A takes the block by its two end faces, fingers along x
# (81 mm across, in the 2F-85's 85 mm stroke: 2 mm a side as it opens round it), at its mid-height and mid-depth. The pads
# (22 mm along y) stay behind the sleeves, and the fingertips stop 7 mm short of the gland plate's underside at the seat.
ROD_END_GRASP = dict(point=(0.0, -8.0, -132.0), z=UP, x=(1.0, 0.0, 0.0), width=81.0)


def P(id, label, keys, grp, phase, path, tool="gripper", actor="A", **kw):
    return dict(do="place", id=id, label=label, keys=list(keys), grp=grp, phase=phase, path=path, tool=tool, actor=actor, **kw)


def S(id, label, joint, grp, phase, actor="A", **kw):
    return dict(do="screws", id=id, label=label, joint=joint, grp=grp, phase=phase, actor=actor, tool="screwdriver", **kw)


def N(id, label, who, why, **kw):
    return dict(do="note", id=id, label=label, who=who, why=why, **kw)


def steps(module="M50"):
    m = module
    out = []
    a = out.append
    # =========================================================== chapter 3: the build module
    # ---- heater stack, upside down on the stack nest (block's top face down); "up" in the world is machine -z
    a(P("M01", "Heater block onto the stack nest, bayonet face down", ["Heater block"], "stack", "stack_inv", [(0, 0, 0), (0, 0, -60)]))
    a(N("M02", "Three M3 helical inserts in the block's underside", "machine shop",
        "Installed right after tapping with a powered insert tool and the tang broken off, as for every insert in the chamber "
        "body (render_build chapter 2); a cobot would need a dedicated inserter and tang-break station for 3 inserts."))
    a(P("M03", "Three cartridge heaters into their bores", ["Cartridge heaters"], "stack", "stack_inv", [(0, 0, 0), (0, 0, -90)],
        note="leads routed by a person (flexible cable)"))
    # round 6: no thermal cutoff any more (electrical.md section 13.4); the three type K are the control, edge and limit sensors
    a(P("M04", "Three type K thermocouples (control, edge, limit) into their bores", ["Type K thermocouples"], "stack", "stack_inv",
        [(0, 0, 0), (0, 0, -100)], note="leads routed by a person"))
    a(P("M05", "Macor rings and radiation shields over three guide pins", ["Macor standoff", "Radiation shields"], "stack", "stack_inv",
        [(0, 0, 0), (0, 0, -70)], tool="nozzle", per_solid=True, drop_ok=True, drop_mm=36.0, order="zdesc",
        note="3 temporary M3 guide pins in the inserts keep the 9 rings and 2 foils in line"))
    a(P("M06", "Piston head onto the break", ["Piston head"], "stack", "stack_inv", [(0, 0, 0), (0, 0, -80)]))
    a(P("M07", "Disc springs into the head's slotted counterbores (small-part vacuum nozzle)", ["Disc springs under"], "stack", "stack_inv",
        [(0, 0, 0), (0, 0, -40)], tool="nozzle", per_solid=False, drop_ok=True, drop_mm=6.0))
    a(S("M08", "Three M3 x 25 stack screws down through the head (torque-controlled: disc-spring preload)", f"stack_{m}", "stack", "stack_inv",
        torque_Nm=0.6))
    a(N("M09", "Bore seal (aramid felt + carbon-filled PTFE scraper) stretched into the head's groove", "person",
        "A felt strip and a split PTFE scraper are wrapped, not pushed; no published robot method for felt."))
    # ---- gland plate and rod (round 4, 2026-11-22: operations.md A1, assembly.md patch 1). The rod end stays welded, made by
    # the shop on the bare rod away from every O-ring. So the gland plate, its rod rings already loaded, goes onto the rod's
    # top end, the rod goes into the head with the plate riding on it, and the whole stack enters the bore from the tube's
    # open bottom end. The gland plate's own nest stands at the body_inv station before the body goes there (M18).
    a(dict(do="seal", id="M10", label="Gland-plate face O-ring (2-034) into the gland plate's groove, groove up, PFPE film",
           keys=["gland-plate O-ring"], grp="gland", phase="body_inv", method="ring", ring="gland_plate_M50", tool="gripper+caps",
           actor="B", path=[(0, 0, 0), (0, 0, 60)], note="the plate is then turned over onto its nest with the ring held by the grease film"))
    a(P("M11", "Gland plate, its face O-ring held by the film, turned over onto its own nest (face down, rod bore vertical)",
        ["bottom flange: gland plate", "gland-plate O-ring"], "gland", "body_inv", [(0, 0, 0), (0, 0, -80)], moved=True))
    a(dict(do="seal", id="M12", label="Two 2-114 rod O-rings folded through the Ø15.93 throat into their grooves (ring loader), plate on its nest",
           keys=["Rod O-rings"], grp="gland", phase="body_inv", method="loader", ring="rod_M50", tool="ring_loader", actor="A",
           path=[(0, 0, 0), (0, 0, -120)]))
    a(P("M13", "Rod (its rod end welded on by the shop: a 316L block with seven weld-in feedthroughs) lowered top end first through "
        "the gland plate's two rod O-rings, on its PEEK bullet",
        ["Hollow piston rod", "Rod end"], "gland", "body_inv", [(0, 0, 0), (0, 0, -150)], bullet="top",
        grasp=ROD_END_GRASP,
        note="arm A holds the rod by the feedthrough block's two ends (81 mm across); the nest holds the plate"))
    a(P("M14", "Rod, with the gland plate riding on it, into the piston head's socket (stack upside down: from above)",
        ["Hollow piston rod", "Rod end", "bottom flange: gland plate", "gland-plate O-ring", "Rod O-rings"], "stack", "stack_inv",
        [(0, 0, 0), (0, 0, -150)], merge="gland", moved=True,
        grasp=ROD_END_GRASP))
    a(S("M15", "Two M4 cup-point set screws into the rod (radial)", f"rod_{m}", "stack", "stack_inv", torque_Nm=1.1))
    # ---- module body: upright first for the spigot O-ring (the mandrel reaches 13 mm into the bore, where the heater block
    # sits once the stack is in: run 3's first pass), then upside down on its spigot face; the stack goes in from the tube's
    # open (bottom) end, which then faces up
    # round 6: gripped across the tube between the flange and the collar (Ø56.8 on M50), from the front, as the turn-overs
    # (M18, M26, M28) grip it. Run 3's automatic grasp took the flange's top slice, 119 mm across the dowel lugs, wider than the
    # 2F-85's 85 mm stroke. The nest's posts (20/90/160 deg) leave the front free for the fingers.
    a(P("M16", "Welded module body onto its upright nest (flange on the nest's three posts), gripped across the tube",
        ["Build module"], "body", "body_up", [(0, 0, 0), (0, 0, 120)],
        grasp=dict(point=(0.0, 0.0, -60.0), z=(0.0, 1.0, 0.0), x=(-1.0, 0.0, 0.0), width=56.8)))
    a(dict(do="seal", id="M17", label="Spigot O-ring (2-238) over the mandrel into the spigot groove (before the stack: the mandrel reaches into the bore)",
           keys=["Spigot O-ring"], grp="body", phase="body_up", method="mandrel", ring="spigot", tool="gripper", actor="A", holder="B",
           path=[(0, 0, 0), (0, 0, 40)]))
    a(dict(do="flip", id="M18", label="Module body turned upside down (wrist roll) onto its spigot nest, the tube's open end up",
           grp="body", frm="body_up", to="body_inv", actor="A"))
    a(P("M19", "Heater stack, rod and gland plate lowered into the bore from the tube's open end (body upside down); the gland plate "
        "lands on the welded collar",
        ["Heater block", "Cartridge heaters", "Type K thermocouples", "Macor standoff", "Radiation shields", "Piston head",
         "Bore seal", "Hollow piston rod", "Heater-stack screws", "Heater-block helical inserts", "Disc springs under", "Rod set screws",
         "Rod end", "bottom flange: gland plate", "gland-plate O-ring", "Rod O-rings"],
        "body", "body_inv", [(0, 0, 0), (0, 0, -260)], merge="stack", moved=True,
        grasp=ROD_END_GRASP,
        note="the bore seal and the block enter the honed bore square, over the bore's bottom lead-in"))
    a(S("M20", "Six M4 x 20 gland-plate screws on the arc behind the rod end's block (round 6, joints.py)", f"gland_{m}", "body", "body_inv",
        torque_Nm=2.2))
    # the round-4 handle runs from under the gland plate up the front of the tube and forward to the robot grip block; slid in
    # along y (runs 1-2) its start pose was out of arm A's reach, so run 3 lowered it from above. On the round-5 rod end that
    # drops its two side arms through the type K sleeves (run 4's first pass: blocked after 18 mm). Round 6: lowered 15 mm in
    # front of its seat, where the side arms' back ends (y -43.4) clear the sleeves (y >= -34) and the power sleeve (x +-6.3),
    # then slid the last 15 mm back along the gland plate's face, 17 mm above the sleeves. Held from above by the riser in front of
    # the collar, the fingers on its two ends (48 mm across x), so both fingers stay at y <= -52, in front of the sleeves (y >= -43):
    # run 4's second pass held the grip block's web from the front (arm A's upper arm met its own wrist 2), and run 5 held the
    # riser across its 6 mm with one finger behind it (that finger met the power sleeve).
    a(P("M21", "Handle lowered in front of the rod end's sleeves, then slid 15 mm back onto the gland plate (module upside down; held by "
        "its riser's two ends from above)", ["handle (6061"], "body", "body_inv", [(0, 0, 0), (0, -15, 0), (0, -15, -40)],
        grasp=dict(point=(0.0, -63.4, -88.0), z=UP, x=(1.0, 0.0, 0.0), width=48.0)))
    a(S("M22", "Two M4 handle screws", f"handle_{m}", "body", "body_inv", torque_Nm=2.2))
    a(P("M23", "Striker disc onto the rod end", ["Striker disc"], "body", "body_inv", [(0, 0, 0), (0, 0, -60)]))
    a(S("M24", "Three M3 x 10 flat-head striker screws", f"striker_{m}", "body", "body_inv", torque_Nm=1.1))
    # round 6: the hermetic connector (a LEMO 1B on a 2-014 in a side boss) is gone. The rod end is a 316L block with seven Solid
    # Sealing weld-ins TIG-welded at its front face, made by the shop with the rod (electrical.md section 13.3): it arrives with
    # the rod in M13 and is checked in M13, M14, M19 and M20-M24. Its plugs go on at the machine (chapter 4, C10's cables).
    a(N("M25", "Rod end's seven weld-in feedthroughs (3 x FA11631 + 3 x FA11632 type K, 1 x FA10443 4-pin power) welded into the 316L "
        "block's front face, and the rod into its top", "machine shop",
        "TIG welds at the block's face and at the rod, on the bare rod before chapter 3, away from every O-ring; the inner joints "
        "to the feedthrough pins are made before the sleeves are welded. Ask Solid Sealing to confirm the blind-bore weld and the "
        "weld access (electrical.md 13.3). The SMPW-K and power plugs go onto the sleeves at the machine, not here."))
    a(dict(do="flip", id="M26", label="Module turned upright (wrist roll, 180 deg about the tool axis) onto the upright nest",
           grp="body", frm="body_inv", to="body_up", actor="A"))
    a(P("M27", "Rim wiper onto the plate; plate into the bore onto the bayonet, turned 60 deg (piston at +8 mm overtravel)",
        ["Build plate", "Plate rim wiper"], "body", "body_up", [(0, 0, 0), (0, 0, 60)], rot=60.0, state={"piston": 8.0},
        grasp=dict(point=(0.0, 0.0, 5.5), z=DN, x=(1.0, 0.0, 0.0), width=50.5)))
    a(dict(do="flip", id="M28", label="Module turned upside down again (wrist roll) onto its spigot nest, ready for the chamber (C10)",
           grp="body", frm="body_up", to="body_inv", actor="A"))
    # round 6 (the merged layout, hot-swap.md 3.2a): the module side of the two SCHUNK NSE-HT zero-point clamps. Each 6061 arm hangs
    # from an ear of the flange (50 and 135 deg) and carries a SPC mini 20 class clamping pin under a zero-point module
    # (modules_low.zp_arms). On the upside-down module each arm goes on from above, after the last turn-over (the arms reach r ~110
    # and would meet the upright nest's posts), with its pin already screwed in on the bench: the pin's Ø20 head stands on the side of
    # the plate that faces the clamp, so it can't go in from above (run 5's first pass). Arm A holds each by its plate, 20 mm short
    # of the pin, across the plate's 24 mm: the automatic grasp took the plate near the hanger, where a fingertip met the rod end.
    a(P("M29", "Right zero-point arm with its clamping pin (SPC mini 20 class, screwed in on the bench) onto the flange's ear at 50 deg; "
        "its screws into the ear are not drawn", [f"Zero-point arms {m} #1", f"Zero-point clamping pins {m} #1"], "body", "body_inv",
        [(0, 0, 0), (0, 0, -60)], grasp=dict(point=(80.2, 42.5, -113.0), z=UP, x=(0.124, 0.992, 0.0), width=24.0)))
    a(P("M30", "Left zero-point arm with its clamping pin onto the flange's ear at 135 deg", [f"Zero-point arms {m} #2",
        f"Zero-point clamping pins {m} #2"], "body", "body_inv", [(0, 0, 0), (0, 0, -60)],
        grasp=dict(point=(-89.2, -10.6, -113.0), z=UP, x=(0.768, -0.640, 0.0), width=24.0)))
    # =========================================================== chapter 4a: the chamber, upside down on Fixture C
    # chamber-construction.md (landed 2026-11-20 22:58 UTC): a through-frame and a bolted 20 mm floor plate with a second 3.53 mm cord.
    # Floor plate face up on Fixture P (a pedestal on the floor, so the arms reach under its edges), its cord rolled in, the frame
    # lowered onto it (two dowels locate it), the 18 floor screws driven up from under the plate's edge, then both arms turn the
    # chamber over onto Fixture C for the under-floor work.
    fp_ins = ["Chamber floor plate", "Helical inserts for the module screws", "Z-flange helical inserts", "Leg helical inserts",
              "Outlet-plenum helical", "Overflow-funnel helical", "Floor-plate dowels", "Zero-point post helical"]
    fr_ins = ["Process chamber body", "Lid screw helical inserts", "Recoater rail helical inserts", "Inlet-plenum helical",
              "Vacuum-port adapter helical", "Bearing-cap helical"]
    a(P("C00a", "Floor plate (inserts and the two frame dowels already in) onto Fixture P, gland face up, by the vacuum gripper", fp_ins,
        "chamber", "chamber_up_P", [(0, 0, 0), (0, 0, 150)], tool="vacuum", grasp=dict(point=(-105.0, 5.0, 0.0), z=DN, x=(1.0, 0.0, 0.0))))
    a(dict(do="seal", id="C00b", label="Floor O-ring cord (3.53 mm, vulcanized splice) rolled into the floor plate's pad gland",
           keys=["Floor O-ring"], grp="chamber", phase="chamber_up_P", method="roller", ring="floor", tool="roller", actor="A", holder="B"))
    a(dict(do="dual", id="C00c", label="Frame lowered onto the floor plate's dowels, one arm on each side wall", keys=fr_ins, grp="chamber",
           phase="chamber_up_P", path=[(0, 0, 0), (0, 0, 150)], docks="P", grip_gap=16.0,
           grasps={"A": dict(point=(-148.0, 0.0, 108.0), z=DN, x=(1.0, 0.0, 0.0)), "B": dict(point=(148.0, 0.0, 108.0), z=DN, x=(1.0, 0.0, 0.0))}))
    a(S("C00d", "Eighteen M4 x 16 floor-plate screws up through the U-notches into the frame's skirt, from under the plate's edge",
        "floor", "chamber", "chamber_up_P", torque_Nm=1.1))
    a(dict(do="dual", id="C01", label="Chamber (frame + floor plate, 7.4 kg) carried upright by both arms from Fixture P into the trunnion's jaws",
           keys=["@chamberset"], grp="chamber", phase="chamber_up_T", frm="chamber_up_P", whole=True, path=[(0, 0, 0), (0, 0, 120)],
           docks="PT", grip_gap=16.0, lift=150.0,
           grasps={"A": dict(point=(-148.0, 60.0, 108.0), z=DN, x=(1.0, 0.0, 0.0)), "B": dict(point=(148.0, 60.0, 108.0), z=DN, x=(1.0, 0.0, 0.0))}))
    a(dict(do="rotate", id="C01b", label="The trunnion turns the chamber upside down (180 deg about x), both arms parked", grp="chamber",
           frm="chamber_up_T", to="chamber_inv"))
    a(P("C02", "Locating dowel and diamond pin into the floor", ["Locating dowel"], "chamber", "chamber_inv", [(0, 0, 0), (0, 0, -60)],
        force="dowel"))
    a(dict(do="seal", id="C03", label="Outlet-plenum O-ring (2-044) into the plenum's flange groove, plenum on a nest, PFPE film",
           keys=["Outlet plenum O-ring"], grp="plenum_out", phase="chamber_inv", method="ring", ring="outlet_plenum", tool="gripper+caps",
           actor="B", path=[(0, 0, 0), (0, 0, 60)]))
    a(P("C04", "Outlet plenum with its O-ring and KF-25 port onto the floor", ["outlet plenum", "Outlet plenum O-ring", "Outlet plenum port"],
        "chamber", "chamber_inv", [(0, 0, 0), (0, 0, -180)], merge="plenum_out"))
    a(S("C05", "Six M4 x 12 outlet-plenum screws", "plenum_out", "chamber", "chamber_inv", torque_Nm=2.2))
    a(dict(do="seal", id="C06", label="Overflow-funnel O-ring (2-042) into the funnel block's groove, PFPE film", keys=["Overflow funnel O-ring"],
           grp="funnel", phase="chamber_inv", method="ring", ring="overflow_funnel", tool="gripper+caps", actor="B", path=[(0, 0, 0), (0, 0, 60)]))
    a(P("C07", "Overflow funnel block (KF-40 port welded on) onto the floor", ["Overflow funnel block", "Overflow funnel O-ring", "Overflow port"],
        "chamber", "chamber_inv", [(0, 0, 0), (0, 0, -200)], merge="funnel"))
    a(S("C08", "Four M4 x 12 overflow-funnel screws", "funnel", "chamber", "chamber_inv", torque_Nm=2.2))
    a(P("C09", "Module-present sensor", ["Module-present sensor"], "chamber", "chamber_inv", "explode", note="its bracket screws are not drawn"))
    # round 6: the Z flange and its screws now go on before the module and the zero-point clamps (run 2's fix for C12, whose fingers
    # met the module's gland plate; run 5 found them on its back-arc screws, and C13's driver on a zero-point arm). The module's
    # swap path passes 12 mm under the flange (machine z), so it doesn't block C10.
    a(P("C12", "Z mounting flange alone onto the floor (the actuator goes on after the module, its screws now)", ["Z mounting flange"],
        "chamber", "chamber_inv", [(0, 0, 0), (0, 0, -150)]))
    a(S("C13", "Four counterbored M5 x 12 Z-flange screws", "zmount", "chamber", "chamber_inv", torque_Nm=4.2))
    # round 6 (the merged layout, hot-swap.md 3.2a): the two SCHUNK NSE-HT mini 88-20 zero-point modules hang from the floor at
    # (100, 40) and (-102, -26), each under a 10 mm 6061 plate on two 16 x 16 posts with an M6 stud into a floor insert. With the
    # chamber upside down the posts stand up off the floor and the plates and modules go on from above, pin face up. The plates'
    # and modules' own screws are not drawn.
    a(P("C09b", "Four zero-point posts turned into the floor's M6 inserts by their studs", ["Zero-point posts"], "chamber", "chamber_inv",
        [(0, 0, 0), (0, 0, -80)], per_solid=True, note="threaded: turned by wrist rotation with regrasps, which a straight sweep can't show"))
    a(P("C09c", "Two zero-point module plates (10 mm 6061) onto the posts; their screws into the posts' ends are not drawn",
        ["Zero-point module plates"], "chamber", "chamber_inv", [(0, 0, 0), (0, 0, -80)], per_solid=True, tool="vacuum"))
    a(P("C09d", "Two SCHUNK NSE-HT mini 88-20 zero-point modules (Ø88, 1.0 kg) onto the plates, pin face up: the vacuum gripper on the "
        "pin face (Ø88 is past the 2F-85's stroke)", ["Zero-point clamping modules"], "chamber", "chamber_inv", [(0, 0, 0), (0, 0, -80)],
        per_solid=True, tool="vacuum"))
    a(N("C09e", "M5 push-in elbows into the modules' release ports, and a temporary Ø4 release-air line from the cell's supply", "person",
        "Small threaded fittings with a tube to follow. The modules have to be open (6 bar) for the clamping pins to enter in C10."))
    # round 6: runs 1-3 held the module at (0, 0, -62) with the fingertips pointing along its axis, 40 mm apart: inside the bore,
    # past the gland plate and the rod end. The check never tested the fingers against the part they hold, so that passed. Arm B
    # now takes the handle's grip block (40 mm web) from behind the upside-down chamber (its front faces the back there), as the
    # tending robot takes it from the front of the machine (robot-ops.md). Its two arms' clamping pins enter the open zero-point
    # modules on the way in. Since round 6 it comes in along the machine's own swap path (lpbf_low.MODULE_PATH, reversed): run 5's
    # straight 150 mm drop along the axis took the flange's tab through the left zero-point plate, which is cut back only to clear
    # that path. So: in 158 mm behind the port (the module's front leads), 40 mm "below" it (machine z), then up into the port.
    a(P("C10", "Build module (upside down) into the Ø96 floor port along its swap path, held by its handle's grip block; dowel and "
        "diamond pin through its flange lugs, clamping pins into the open zero-point modules", ["@module"], "chamber", "chamber_inv",
        [(0, 0, 0), (0, 0, -40), (0, -158, -40), (0, -158, -150)], merge="body", moved=True,
        force="spigot", actor="B", grasp=dict(point=(0.0, -141.0, -47.0), z=(0.0, 1.0, 0.0), x=(1.0, 0.0, 0.0), width=40.0)))
    # round 6: the captive M6 and their retainers are gone (joints.py section 2); the clamps hold the module (hot-swap.md 3.2a)
    a(N("C11", "Release air off: the zero-point modules' springs lock both clamping pins (2 x 0.5 kN); no screws", "machine",
        "The cell vents the temporary line. 1 kN holds 4.6x the worst separating load (hot-swap.md 3.2a). The spigot ring is already "
        "home: arm B pushed the module in at C10 (132 N running). The captive M6 are gone; the floor keeps their inserts for a hand fallback."))
    a(P("C13b", "Z actuator, belt fold, servo, carriage, arm and magnet (pre-assembled) onto the flange",
        ["Z actuator", "Z bracket", "Z servo", "Z carriage", "Z lift arm", "Pot magnet"], "chamber", "chamber_inv",
        [(0, 0, 0), (0, 0, -150)], grasp=dict(point=(0.0, 80.0, -170.0), z=UP, x=(1.0, 0.0, 0.0)), note="its screws to the flange are not drawn"))
    a(P("C14", "Four legs onto the floor, one at a time", ["@legs"], "chamber", "chamber_inv", [(0, 0, 0), (0, 0, -120)], per_solid=True))
    a(S("C15", "One M6 x 25 down each leg's Ø11 bore (160 mm bit extension)", "legs", "chamber", "chamber_inv", torque_Nm=7.4, long_bit=165.0))
    # =========================================================== chapter 4b: base plate and posts on Fixture B
    a(dict(do="dual", id="F01", label="Process base plate onto Fixture B (both arms, one at each end)", keys=["Base plate, process"],
           grp="machine", phase="upright", path=[(0, 0, 0), (0, 0, 150)],
           grasps={"A": dict(point=(-370.0, -265.0, -167.5), z=(0.0, 1.0, 0.0), x=(0.0, 0.0, 1.0)),
                   "B": dict(point=(260.0, 215.0, -167.5), z=(0.0, -1.0, 0.0), x=(0.0, 0.0, 1.0))}))
    a(N("F02", "Levelling mounts", "person", "They thread in when the finished process module goes onto the tray (chapter 5); "
        "until then Fixture B carries the plate on its ends."))
    # round 6 (the merged layout): the zero-point release valve stands on the base plate behind the left-hand module, under the floor
    # once the chamber is on, so it goes on first
    a(P("F02b", "Zero-point release valve (3/2 NC, 24 V, on its sub-base) onto the base plate; its screws are not drawn",
        ["Zero-point release valve"], "machine", "upright", [(0, 0, 0), (0, 0, 120)]))
    # =========================================================== the turn-over
    a(dict(do="rotate", id="F05", label="The trunnion turns the chamber assembly (module, Z stage, legs) back upright", grp="chamber",
           frm="chamber_inv", to="chamber_up_T", sign=-1.0))
    a(dict(do="dual", id="F05b", label="Chamber assembly (with the module, zero-point clamps, Z stage and legs) carried upright by both "
           "arms, each holding a leg, from the trunnion onto the base plate", keys=["@chamberset"], grp="machine", phase="upright", frm="chamber_up_T", whole=True, merge="chamber",
           path=[(0, 0, 0), (0, 0, 120)], docks="TB", grip_gap=30.0, lift=320.0,
           # round 6: each leg held 40 mm lower (machine z -135), below the zero-point modules (z -109 to -89): at -95 arm B's inner
           # finger on the back-right leg (x 126-156, y 81-111 since round 6; B's grasp now on its centre) ran into the right module
           grasps={"A": dict(point=(-135.0, -90.0, -135.0), z=(0.0, 1.0, 0.0), x=(1.0, 0.0, 0.0)),
                   "B": dict(point=(141.0, 96.0, -135.0), z=(0.0, -1.0, 0.0), x=(1.0, 0.0, 0.0))}))
    a(S("F06", "Eight M6 x 25 base-plate-to-leg screws, from under the plate", "legs_base", "machine", "upright", torque_Nm=7.4))
    a(N("F06b", "Release-air line: Ø4 tube from the valve through a union Y to both zero-point modules' push-in elbows (in place of the "
        "temporary line); the valve's supply comes from the rack's air prep in chapter 5", "person",
        "Tube routing (deformable), as the hoses in chapter 5. The modules stay locked while the line is swapped: their springs hold."))
    # round 6 (the merged layout): the jar sits at the overflow slot's front end, (94, -46), its KF-40 joint at z -82, and has a grip
    # fin: an I-section level with the module's grip block and 100 mm to its right (automation.py section 8). It comes in from the
    # front along its lane and up 8 mm onto the centring ring (operations.md U4.7 reversed); arm A holds the fin's 40 mm web from the
    # front, as the tending robot does.
    a(P("F07", "Overflow jar in from the front along its lane and up 8 mm onto its KF-40 port, held by its grip fin", ["Overflow jar"],
        "machine", "upright", [(0, 0, 0), (0, 0, -8), (0, -260, -8)], actor="A",
        grasp=dict(point=(100.0, -141.0, -45.0), z=(0.0, 1.0, 0.0), x=(1.0, 0.0, 0.0), width=40.0)))
    a(N("F08", "KF-40 toggle clamp (MKS 100318805) round the jar's flange, lever to the front", "person",
        "Its hinged ring has to be held open round both flanges before one push on the lever locks it; nothing on the 2F-85 holds "
        "the ring open. An air-released KF clamp would let the robot do it (hot-swap.md)."))
    a(P("F09", "Overflow-jar sensor and its bracket, onto the front-right leg's back face", ["Overflow-jar present", "Overflow-jar sensor bracket"],
        "machine", "upright", "explode", actor="A"))
    a(S("F09b", "Two M4 x 10 jar-sensor bracket screws into the front-right leg", "jar_sensor", "machine", "upright", torque_Nm=2.2))
    a(P("F11", "LED bar (small-part vacuum nozzle on its top face)", ["Layer-light"], "machine", "upright", "explode", tool="nozzle"))
    a(P("F10", "Lift-out wall liners into the open chamber", ["Lift-out wall liner"], "machine", "upright", "explode", tool="vacuum"))
    a(N("F12", "Through-beam fibre heads with their 2-010 O-rings, threaded into the side walls from outside", "person",
        "Threading an M6 head with a fibre attached means winding the fibre with it; the ring itself is a pick-and-place."))
    a(dict(do="seal", id="F13", label="Inlet-plenum O-ring (2-044) into the plenum's flange groove, PFPE film", keys=["Inlet plenum O-ring"],
           grp="plenum_in", phase="upright", method="ring", ring="inlet_plenum", tool="gripper+caps", actor="B", path=[(0, 0, 0), (0, -60, 0)]))
    a(P("F14", "Inlet plenum with its O-ring and KF-25 port onto the back wall, held there by arm A", ["inlet plenum", "Inlet plenum O-ring",
                                                                                                    "Inlet plenum port"],
        "machine", "upright", "explode", actor="A", merge="plenum_in", hold_for="plenum_in"))
    a(S("F15", "Nine M4 x 16 inlet-plenum screws into the back wall", "plenum_in", "machine", "upright", actor="B", torque_Nm=2.2))
    a(P("F16", "Vacuum-port adapter (KF-25 stub welded in) with its 2-024 O-ring onto the right wall", ["Vacuum port"], "machine", "upright",
        "explode", hold_for="vac_port"))
    a(S("F17", "Four M5 x 20 vacuum-port screws", "vac_port", "machine", "upright", torque_Nm=4.2))
    a(P("F18", "Recoater rail with its carriage, carriage block, ball nut and arm (bought and pre-assembled on the rail) onto the back wall",
        ["Recoater guide rail", "Recoater carriage (", "Recoater carriage block", "Recoater ball nut", "Recoater arm"], "machine", "upright",
        [(0, 0, 0), (0, 0, 220)], hold_for="rail", grasp=dict(point=(-106.0, 72.0, 92.0), z=DN, x=(1.0, 0.0, 0.0), width=44.0)))
    a(S("F19", "Five M4 x 16 rail screws, driven from inside the chamber toward the back wall", "rail", "machine", "upright", actor="A",
        torque_Nm=2.2))
    a(P("F21", "Ball screw in through the right wall's bore and turned through the ball nut (30 turns at 10 mm lead) into the left bore",
        ["Recoater ball screw"], "machine", "upright", [(0, 0, 0), (420, 0, 0)]))
    a(P("F22", "Feedthrough spacer, its two 2-024 O-rings, the Ferrotec unit and the coupling on the left wall",
        ["Recoater feedthrough", "Recoater fixed bearing", "Recoater shaft coupling"], "machine", "upright", "explode",
        note="the feedthrough's own 6 x M4 are not drawn"))
    a(P("F23", "Blind bearing cap and its 2-019 O-ring on the right wall", ["Recoater floating bearing", "Recoater bearing-cap O-ring"],
        "machine", "upright", "explode", hold_for="bearing_cap"))
    a(S("F24", "Four M4 x 20 bearing-cap screws", "bearing_cap", "machine", "upright", torque_Nm=2.2))
    a(P("F25", "Motor standoff, bracket and recoater servo", ["Recoater motor standoff", "Recoater motor bracket", "Recoater servo"], "machine",
        "upright", "explode", per_part=True, note="their screws are not drawn"))
    a(P("F26", "Blade holder and blade, in through the door opening and up under the recoater arm", ["Blade holder", "HSS recoater blade"],
        "machine", "upright", [(0, 0, 0), (0, -260, 0)], grasp=dict(point=(-106.0, -45.0, 18.0), z=(0.0, 1.0, 0.0), x=(1.0, 0.0, 0.0), width=18.0)))
    a(S("F27", "Two M3 x 8 blade screws", "blade", "machine", "upright", torque_Nm=1.1))
    a(P("F28", "Gas knife and dose chute", ["Gas knife", "Dose chute"], "machine", "upright", "explode", per_part=True,
        note="how they hang from the walls is not drawn"))
    a(dict(do="seal", id="F29", label="Lid O-ring cord (3.53 mm) rolled into the body's top gland: arm A rolls, arm B feeds the cord",
           keys=["Lid O-ring"], grp="machine", phase="upright", method="roller", ring="lid", tool="roller", actor="A", holder="B"))
    a(P("F30", "Lid (inserts in) onto the cord, by the vacuum gripper", ["Chamber lid (", "Window-flange helical", "Metering-base helical",
                                                                         "Drawer latch receptacles"],
        "machine", "upright", [(0, 0, 0), (0, 0, 340)], tool="vacuum", grasp=dict(point=(105.0, 40.0, 136.0), z=DN, x=(1.0, 0.0, 0.0))))
    a(S("F31", "Twenty M5 x 25 lid screws, star pattern", "lid", "machine", "upright", torque_Nm=4.2))
    a(dict(do="seal", id="F32", label="Window-flange O-ring (2-036) into the flange's lower groove, PFPE film", keys=["Window-flange O-ring"],
           grp="wflange", phase="upright", method="ring", ring="window_flange", tool="gripper+caps", actor="B", path=[(0, 0, 0), (0, 0, -60)]))
    a(P("F33", "Field stop", ["Field-stop"], "machine", "upright", "explode"))
    a(P("F33b", "Window flange with its O-ring (Ø100: the vacuum gripper)", ["Window flange", "Window-flange O-ring"], "machine", "upright",
        "explode", merge="wflange", moved=True, tool="vacuum", grasp=dict(point=(0.0, 0.0, 158.0), z=DN, x=(1.0, 0.0, 0.0))))
    a(S("F34", "Six counterbored M4 x 16 window-flange screws (torque-controlled)", "window", "machine", "upright", torque_Nm=2.2))
    a(dict(do="seal", id="F35", label="Window O-ring (2-031) into the flange's seat groove", keys=["Window O-ring"], grp="machine",
           phase="upright", method="ring", ring="window_lower", tool="gripper+caps", actor="B", path=[(0, 0, 0), (0, 0, 60)]))
    a(P("F36", "Ø2 in. fused-silica window onto its O-ring", ["fused-silica window"], "machine", "upright", "explode",
        grasp=dict(point=(0.0, 0.0, 152.0), z=DN, x=(1.0, 0.0, 0.0))))
    a(P("F37", "FKM flat ring", ["Window clamp ring"], "machine", "upright", "explode"))
    a(P("F37b", "Window retaining ring (Ø100: the vacuum gripper)", ["Window retaining ring"], "machine", "upright", "explode", tool="vacuum",
        grasp=dict(point=(0.0, 0.0, 163.0), z=DN, x=(1.0, 0.0, 0.0))))
    a(S("F38", "Six M3 x 10 retaining-ring screws (torque-controlled: clamp the silica evenly)", "window_ring", "machine", "upright",
        torque_Nm=0.8))
    a(P("F39", "Cover-slide drawer (2-033 in its half-dovetail, put in on the bench) into the lid's front edge",
        ["Cover-slide drawer", "Cover slide (", "Drawer O-ring", "Drawer latches"], "machine", "upright", [(0, 0, 0), (0, -200, 0)],
        force="drawer", grasp=dict(point=(0.0, -126.0, 127.0), z=(0.0, 1.0, 0.0), x=(1.0, 0.0, 0.0))))
    a(N("F40", "Quarter-turn drawer latches", "robot (custom bit)", "Two quarter-turn studs, turned with a slotted bit on the "
        "screwdriver; the latch hardware is an envelope in the model (seals.md: no catalogue latch fits)."))
    a(P("F41", "Drawer-closed sensor", ["Drawer-closed sensor"], "machine", "upright", "explode"))
    a(dict(do="seal", id="F42", label="Metering-base O-ring (2-040) on its lid side (groove faces down when fitted: PFPE film)",
           keys=["Metering-base O-ring"], grp="mbase", phase="upright", method="ring", ring="metering_base",
           tool="gripper+caps", actor="B", path=[(0, 0, 0), (0, 0, -60)]))
    a(dict(do="seal", id="F42b", label="Metering-base dock-face O-ring (2-040), groove up", keys=["Metering-base dock-face"], grp="mbase",
           phase="upright", method="ring", ring="metering_base", tool="gripper+caps", actor="B", path=[(0, 0, 0), (0, 0, 60)]))
    a(P("F43", "Metering base alone (feedthrough, coupling and stepper not yet on) onto the lid", ["Metering base", "Metering-base O-ring",
                                                                                               "Metering-base dock-face"],
        "machine", "upright", "explode", merge="mbase", moved=True, grasp=dict(point=(-90.0, 0.0, 172.0), z=DN, x=(1.0, 0.0, 0.0))))
    a(S("F44", "Four M4 x 16 metering-base screws (before the roller feedthrough covers two of them)", "dose", "machine", "upright",
        torque_Nm=2.2))
    a(P("F45", "Roller feedthrough (threaded M8 x 1 over its 2-012), coupling, stepper, dock rails, load cell, NFC, side port, docked sensor",
        ["Roller shaft:", "Roller feedthrough", "Roller drive coupling", "Dosing stepper", "Dovetail rails", "Load cell", "NFC reader",
         "Side reservoir port", "Reservoir-docked sensor"], "machine", "upright", "explode", per_part=True,
        note="their screws are not drawn; the feedthrough is turned in (8 turns) by wrist rotation with regrasps"))
    a(P("F46", "Reservoir M slid onto the dovetail dock (about 94 N to seat on the dock O-ring)", [f"Reservoir {'M'}"], "machine", "upright",
        [(0, 0, 0), (0, -160, 0)], force="reservoir", grasp=dict(point=(-90.0, 0.0, 255.0), z=DN, x=(1.0, 0.0, 0.0))))
    a(dict(do="seal", id="F47", label="Camera adapter O-ring (2-022), PFPE film", keys=["Camera adapter O-ring"], grp="camad", phase="upright",
           method="ring", ring="camera_adapter", tool="gripper+caps", actor="B", path=[(0, 0, 0), (0, 0, -60)]))
    a(P("F48", "Camera viewport adapter with its 2-030", ["Camera viewport", "Camera adapter O-ring"], "machine", "upright", "explode",
        merge="camad", moved=True, note="its screws are not drawn"))
    a(P("F48b", "Camera window gasket (1 mm FKM flat ring), window, flat ring, retaining ring, in that order, then the camera",
        ["Camera window gasket", "Camera window (", "Camera window flat ring", "Camera window retaining ring", "Layer camera"], "machine",
        "upright", "explode", per_part=True, note="the retaining ring's and camera's screws are not drawn"))
    a(N("F49", "Pressure transducer and relief valve (SAE-4 O-ring-boss ports)", "person",
        "Threaded ports need a wrench on a hex and a set torque; a 2F-85 can only spin a plain body."))
    a(P("F50", "Hinge knuckles on the chamber and the two draw-latch strikes on its side faces", ["Door hinge knuckles on the chamber", "Draw-latch strikes"],
        "machine", "upright", "explode", per_part=True, note="hinge and latch screws are not drawn"))
    a(P("F51", "Door (cord rolled into its half-dovetail on the bench) brought in, knuckles in line", ["Chamber door", "Door O-ring",
                                                                                                   "Door hinge leaves", "Draw-latch brackets", "Draw latches",
                                                                                                   "Door handle"],
        "machine", "upright", [(0, 0, 0), (0, -200, 0)], grasp=dict(point=(0.0, -150.0, 95.0), z=(0.0, 1.0, 0.0), x=(1.0, 0.0, 0.0))))
    a(P("F52", "Hinge pins slid in along x", ["Hinge pins"], "machine", "upright", [(0, 0, 0), (-160, 0, 0)],
        grasp=dict(point=(100.0, -132.0, -12.0), z=(-1.0, 0.0, 0.0), x=(0.0, 0.0, 1.0))))
    a(P("F03", "Optics posts (moved here: they blocked the side-wall parts and the right latch) onto the base plate, one at a time, held by arm B while arm A drives their base screws from below",
        ["@posts"], "machine", "upright", [(0, 0, 0), (0, 0, 200)], actor="B", per_solid=True, hold_for="bridge_base"))
    a(S("F04", "Two M6 x 25 up into each post's bottom cap, from under the plate", "bridge_base", "machine", "upright", torque_Nm=7.4))
    a(N("F53", "f-theta lens threaded into its adapter ring over its 3 mm shim stack, under the bridge (on the bench, bridge upside down)", "person",
        "The Ø90 lens is wider than the 2F-85's 85 mm stroke and threads M85 x 1; a strap wrench by hand (operations.md: lens and ring "
        "fitted to the bridge on the bench)."))
    a(dict(do="dual", id="F54", label="Optics bridge (13.3 kg, lens and ring under it) onto the four posts, one arm at each end",
           keys=["Optics bridge (", "f-theta lens", "f-theta focus shims", "f-theta adapter ring"], grp="machine", phase="upright", path=[(0, 0, 0), (0, 0, 260)],
           grip_gap=25.5,
           grasps={"A": dict(point=(-330.0, -190.0, 220.2), z=(0.0, 1.0, 0.0), x=(0.0, 0.0, 1.0)),
                   "B": dict(point=(215.0, 180.0, 220.2), z=(0.0, -1.0, 0.0), x=(0.0, 0.0, 1.0))}))
    a(S("F55", "Eight M6 x 35 bridge screws down into the posts", "bridge", "machine", "upright", torque_Nm=7.4))
    a(P("F56", "Galvo riser plate (155 x 130: the vacuum gripper)", ["Galvo riser plate"], "machine", "upright", "explode", tool="vacuum",
        grasp=dict(point=(20.35, -6.8, 241.11), z=DN, x=(1.0, 0.0, 0.0))))
    a(P("F56b", "basiCube 20 scan head on the riser (3.75 kg: the vacuum gripper on its top)", ["2-axis galvo"], "machine", "upright", "explode",
        tool="vacuum", grasp=dict(point=(20.35, -6.8, 363.11), z=DN, x=(1.0, 0.0, 0.0)), note="its screws are not drawn"))
    a(P("F57", "Beam tubes, dichroic and fold-mirror cubes, shutter, photodiode chain and collimator",
        ["Enclosed beam tube", "Coaxial-monitoring dichroic", "Fold mirror", "Safety shutter", "Coaxial photodiode chain", "Collimator"], "machine", "upright", "explode",
        per_part=True))
    a(N("F58", "Process fiber routed to the collimator", "person", "Armoured fiber, >= 100 mm bend radius: cable routing stays manual."))
    a(N("F59", "Class 1 laser guard: T-slot frame, panels, door rail, sliding door, guard lock, operator panel", "person",
        "T-slot nuts and 1.5 mm panels up to 730 mm wide; its hardware is not drawn (joints.NOT_DRAWN)."))
    # =========================================================== chapter 5: tray
    a(N("T01", "Process module (84 kg) off Fixture B onto the VLM tray; levelling mounts threaded in", "person + hoist",
        "84 kg is 3.4 times two UR12e payloads; a hoist or lift table."))
    a(N("T02", "19 in. rack and its units (UPS 23 kg, laser 40 kg, PC 8 kg, DIN drawer 9 kg)", "person + lift",
        "the UPS and the laser exceed a UR12e's 12.5 kg; cage nuts and screws are not drawn"))
    a(N("T03", "Gas module: base plate, scroll pump (26 kg), blower, filter housing, O2 box, argon manifold", "person + lift",
        "the pump exceeds 12.5 kg; the units' screws are not drawn"))
    a(N("T04", "KF-25 bellows, vacuum valve, argon and O2 lines, and the zero-point valve's air supply", "person",
        "hose and tube routing (deformable, KF wing-nut clamps)"))
    a(N("T05", "Tray dock and umbilicals", "person", "cable and hose routing"))
    a(N("T06", "Leak check: rate of rise from <= 1 mbar, O2 drift at +20 mbar argon", "machine", "the seal verification in assembly.md"))
    return out
