"""Catalogue of every hand operation on the low-profile desktop LPBF (issue #260, PR #266): assembly, use,
maintenance and swap-outs, step by step. run_ops.py checks each step on the model (checks.py, tools.py).

Step kinds (each a dict; `do` says which check runs):
  place   a part (or several, moving together) goes in. Checked as assembly-by-disassembly: the reverse of its path must
          be free with only the parts placed before it present. `path`: "explode" (the straight line render_build.py
          animates, from the part's explode offset) or a list of offsets; if that is blocked, the six axis directions
          are tried and reported.
  screws  every screw of a joint (joints.REGISTRY key) is driven: the screw's own withdrawal line and each tool in
          tools.candidates() are checked at that moment. torque=True: the joint needs a set torque (window, disc-spring
          stack, module flange at half torque), so only the torque screwdriver counts as a full pass.
  remove  a part leaves along `paths` (tried in order; the first free one is the answer), and stays out for the rest of
          the operation.
  reach   a flat hand at `point` with the forearm running back along `approach` (one or more directions tried).
  note    no geometric check (off-machine work, waiting, software); minutes only.
Every operation has: kind, interval (where the notes or a vendor give one), where it is done (bench, or the machine on
its VLM tray at the access opening), state (motion-group values), whether it opens the chamber to air, and minutes per
step (rough, for a trained person; not measured).
"""
from __future__ import annotations

import math

import module_params as MP

LZ0, LZ1 = 120.0, 136.0
XD, XP = MP.X_DOSE, MP.X_PARK
CY = 111.0
OPEN = {"gdoor": 470.0}                          # guard door slid open
OPEN_DOOR = {"gdoor": 470.0, "door": 95.0}       # and the chamber door dropped
FRONT = (0, -1, 0)
UP = (0, 0, 1)
OUT_FRONT = [(0, 0, 0), (0, -520, 0)]
_c = (75.0, -45.0, 136.0)                        # layer camera: its axis points from the plate centre through the viewport
CAM_UP = tuple(v / math.sqrt(sum(x * x for x in _c)) for v in _c)


def place(label, keys, path="explode", minutes=2, exclude=(), note="", rot=None, move_placed=False, per_part=False):
    """rot: turn the parts this many degrees about z (through the origin) before the path (the plate's bayonet);
    move_placed: the parts were placed in earlier steps and now move as one unit (the heater stack into the bore)."""
    return dict(do="place", label=label, keys=list(keys), exclude=list(exclude), path=path, minutes=minutes, note=note, rot=rot,
                move_placed=move_placed, per_part=per_part)


def screws(label, joint, minutes, torque=False, pn=None, note=""):
    return dict(do="screws", label=label, joint=joint, torque=torque, pn=pn, minutes=minutes, note=note)


def remove(label, keys, paths, minutes=2, exclude=(), rot=None, note="", state=None):
    return dict(do="remove", label=label, keys=list(keys), exclude=list(exclude), paths=paths, minutes=minutes, rot=rot, note=note, state=state)


PINCH_HAND = (46.0, 25.0, 60.0)     # fingers pinching a tab, a key or a clamp's wing nut (width x thickness x length)


def reach(label, point, approach=(FRONT,), skip=(), minutes=1, note="", hand=None, state=None):
    """hand centre at `point` (put ~30 mm above a grip point for a horizontal reach, so the fingers reach down to it)."""
    return dict(do="reach", label=label, point=point, approach=list(approach), skip=list(skip), minutes=minutes, note=note, hand=hand, state=state)


def note(label, minutes, why=""):
    return dict(do="note", label=label, minutes=minutes, note=why)


def lift_then(dz, d, L=520.0, pre=None):
    """offsets: optional first leg, up dz, then L along d."""
    legs = [(0.0, 0.0, 0.0)]
    if pre:
        legs.append(tuple(pre))
    x, y, z = legs[-1]
    legs.append((x, y, z + dz))
    legs.append((x + d[0] * L, y + d[1] * L, z + dz + d[2] * L))
    return legs


def axis_paths(L=520.0, first=None):
    out = []
    for d in ((0, -1, 0), (0, 0, 1), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, -1)):
        legs = [(0.0, 0.0, 0.0)]
        if first:
            legs.append(tuple(first))
        x, y, z = legs[-1]
        legs.append((x + d[0] * L, y + d[1] * L, z + d[2] * L))
        out.append(legs)
    return out


STACK = ["Heater block", "Cartridge heaters", "Type K thermocouples", "Thermal cutoff", "Macor standoff", "Radiation shields",
         "Piston head", "Bore seal", "Hollow piston rod", "Build plate", "Plate rim wiper", "Heater-stack screws",
         "Heater-block helical inserts", "Disc springs under", "Rod set screws"]
MODULE_BODY = ["Build module", "Spigot O-ring", "bottom flange: gland plate", "gland-plate O-ring", "handle (6061", "Gland-plate screws",
               "Handle screws", "Captive M6", "Captive-screw retainers"]
LID_SET = ["Chamber lid", "Window flange", "fused-silica window", "Window O-ring", "Window retaining ring", "Field-stop", "Cover-slide drawer",
           "Cover slide (", "Drawer O-ring", "Drawer latches", "Drawer latch wing head", "Drawer latch receptacles", "Drawer-closed sensor", "Gas knife", "Dose chute",
           "Metering base", "Metering-base O-ring", "Metering-base dock-face", "NFC reader", "Dovetail rails", "Roller shaft:", "Roller feedthrough",
           "Roller drive coupling", "Dosing stepper", "Window clamp ring", "Window-flange O-ring", "Camera adapter O-ring", "Camera window", "Side reservoir port", "Reservoir-docked sensor", "Load cell", "Camera viewport",
           "Pressure transducer", "Overpressure relief", "Window-flange screws", "Window-flange helical", "Window retaining-ring screws",
           "Metering-base screws", "Metering-base helical"]


def catalogue(module="M50"):
    m = MP.MODULES[module]
    res = m["reservoir"]
    ops = []

    # ============================== A. assembly ==============================
    ops.append(dict(id="A1", kind="assembly", name=f"Assemble the heated {module} build module (render_build chapter 3)", where="bench",
                    interval="once per module", state={}, present="sequence", bench=True, air=False, steps=[
        place("Heater block on the bench", ["Heater block"], path=None, minutes=1),
        note("Three M3 helical inserts into the block's underside (insert tool, on the bench)", 5),
        place("Cartridge heaters up into their bores from below", ["Cartridge heaters"], path=[(0, 0, 0), (0, 0, -90)], minutes=3),
        place("Thermocouples and the thermal cutoff from below", ["Type K thermocouples", "Thermal cutoff"], path=[(0, 0, 0), (0, 0, -100)], minutes=4),
        place("Macor rings and radiation shields under the block", ["Macor standoff", "Radiation shields"], path=[(0, 0, 0), (0, 0, -70)], minutes=4),
        place("Piston head under the break", ["Piston head"], path=[(0, 0, 0), (0, 0, -80)], minutes=2),
        place("Disc springs into the head's slotted counterbores", ["Disc springs under"], path=[(0, 0, 0), (0, 0, -40)], minutes=2),
        place("Stack screws up through the head (placed)", ["Heater-stack screws"], path=[(0, 0, 0), (0, 0, -40)], minutes=1),
        screws("Stack screws driven from below (disc-spring preload: torque-controlled)", f"stack_{module}", 4, torque=True),
        place("Bore seal into its groove", ["Bore seal"], path=None, minutes=3),
        # 2026-11-22: the rod end stays welded (an all-metal gas boundary with one static O-ring at the connector). The gland plate goes
        # onto the rod from the rod's top end, before the rod goes into the head, and the stack enters the bore from below with the
        # gland plate riding on the rod, so the weld is made by the shop on the bare rod, away from every O-ring (assembly.md M25)
        place("Gland plate with its two rod O-rings (ring loader) and its face O-ring, under the head", ["bottom flange: gland plate", "gland-plate O-ring", "Rod O-rings"],
              path=[(0, 0, 0), (0, 0, -80)], minutes=4),
        place("Rod with its end cap (welded by the shop on the bare rod), top end up through the gland plate's rings into the head's socket",
              ["Hollow piston rod", "Rod end"], path=[(0, 0, 0), (0, 0, -150)], minutes=3, note="the rod's top end on the PEEK bullet through the rings"),
        screws("Rod set screws (radial)", f"rod_{module}", 2),
        place("Hermetic connector with its O-ring into the rod end's side boss", ["Hermetic connector", "Hermetic-connector O-ring"],
              path=[(0, 0, 0), (-60, 0, 0)], minutes=3),
        place("Striker disc", ["Striker disc"], path=[(0, 0, 0), (0, 0, -60)], minutes=1),
        screws("Three M3 flat-head striker screws from below", f"striker_{module}", 3),
        place("Rim wiper onto the plate, plate onto the bayonet (turned 60 deg)", ["Build plate", "Plate rim wiper"],
              path=[(0, 0, 0), (0, 0, 60)], minutes=2, rot=60.0),
        place("Welded module body on the bench (the stack waits below it)", ["Build module", "Spigot O-ring"], path=None, minutes=1),
        place("Stack, rod and gland plate up into the bore from below (lead-in on the bore's bottom edge); gland plate onto the collar",
              STACK + ["Rod end", "Hermetic connector", "Hermetic-connector O-ring", "Striker disc", "Striker screws", "bottom flange: gland plate",
                       "gland-plate O-ring", "Rod O-rings"], path=[(0, 0, 0), (0, 0, -260)], minutes=4,
              note="the bore seal and plate must enter the honed bore square", move_placed=True),
        screws("Six M4 gland-plate screws from below", f"gland_{module}", 4, torque=True),
        place("Handle under the gland plate", ["handle (6061"], path=[(0, 0, 0), (0, -80, 0)], minutes=1),
        screws("Two M4 handle screws", f"handle_{module}", 2),
    ]))

    ops.append(dict(id="A2", kind="assembly", name="Assemble the process module and put it on the tray (render_build chapters 4-5)",
                    where="bench, then the VLM tray", interval="once", state={}, present="sequence", bench=False, air=False, steps=[
        place("Base plate on its four levelling mounts (M8 stems threaded up)", ["Base plate, process", "Leveling mounts, process", "VLM tray"],
              path=None, minutes=10),
        place("Chamber legs onto the base plate", ["Chamber legs"], minutes=3),
        screws("Base-plate-to-leg screws, 2 x M6 per leg, up from under the plate (37 mm above the bench)", "legs_base", 8),
        # the chamber is a through-frame on a bolted floor plate (chamber-construction.md): floor plate, its cord, frame, floor screws
        place("Floor plate with its helical inserts and two pressed dowels onto the legs",
              ["Chamber floor plate", "Helical inserts for the module screws", "Z-flange helical inserts", "Leg helical inserts",
               "Outlet-plenum helical inserts", "Overflow-funnel helical inserts", "Floor-plate dowels"], minutes=5),
        screws("Leg-to-floor screws, one M6 up each leg's Ø11 bore through the base plate into the floor plate", "legs", 8),
        place("Floor O-ring: 3.53 mm FKM cord, a vulcanized loop, pressed into the pad's face gland", ["Floor O-ring"], minutes=4),
        place("Through-frame lowered over the floor plate's pad onto the two dowels, with its lid-screw inserts",
              ["Process chamber body", "Lid screw helical inserts"], minutes=4),
        screws("Eighteen M4 floor screws up through the plate's U-notches into the frame's skirt (~1.1 N m)", "floor", 10, torque=True),
        place("Locating dowel and diamond pin pressed into the floor from below", ["Locating dowel"], path=[(0, 0, 0), (0, 0, -60)], minutes=5),
        place("Outlet plenum and its O-ring under the floor", ["outlet plenum", "Outlet plenum O-ring", "Outlet plenum port"], minutes=5),
        screws("Six M4 outlet-plenum screws up into the floor", "plenum_out", 4),
        place("Overflow funnel block, its O-ring, KF-40 port", ["Overflow funnel", "Overflow port"], minutes=4),
        screws("Four M4 overflow-funnel screws up into the floor", "funnel", 3),
        place("Overflow jar up to its port (clamp put on by hand)", ["Overflow jar"], path=[(0, 0, 0), (0, 0, -8), (520, 0, -8)], minutes=2),
        place("KF-40 clamp", ["Overflow clamp"], path=None, minutes=1),
        place("Overflow-jar and module-present sensors", ["Overflow-jar present", "Module-present sensor"], minutes=4),
        place("Wall liners (six pieces) and their pull tabs into the open chamber", ["Lift-out wall liner", "Liner pull tab"], minutes=3, per_part=True),
        place("LED bar", ["Layer-light"], minutes=3),
        place("Through-beam fibre heads and their O-rings, threaded into the side walls from outside", ["Plate-height through-beam", "Fibre-head O-rings"],
              path=None, minutes=3),
        place("Inlet plenum and its O-ring on the back wall", ["inlet plenum", "Inlet plenum O-ring", "Inlet plenum port"], minutes=3),
        screws("Seven M4 inlet-plenum screws into the back wall", "plenum_in", 5),
        place("Vacuum-port adapter plate and its O-ring on the right wall", ["Vacuum port"], minutes=2),
        screws("Four M5 vacuum-port adapter screws", "vac_port", 3),
        place("Recoater rail onto the back wall", ["Recoater guide rail"], minutes=2),
        screws("Four M4 rail screws into the back wall's holes, tapped through from outside", "rail", 4),
        screws("Four M4 plug screws on bonded seal washers in those holes, on the back wall's outer face", "rail_plugs", 3),
        place("Carriage on the rail (slid on from the rail's end)", ["Recoater carriage (", "Recoater carriage block"], minutes=3),
        place("Ball screw (animation: dropped in from above)", ["Recoater ball screw"], path="explode", minutes=4,
              note="it passes through Ø18 bores in both side walls"),
        place("Ball nut threaded onto the screw, arm on the block", ["Recoater ball nut", "Recoater arm"], path=None, minutes=3,
              note="a threading (helical) motion; not a straight-line check"),
        place("Feedthrough (spacer, O-rings, Ferrotec unit, coupling), bearing cap, motor standoff, bracket, servo",
              ["Recoater feedthrough", "Recoater fixed bearing", "Recoater shaft coupling", "Recoater floating bearing", "Recoater bearing-cap O-ring",
               "Recoater motor standoff", "Recoater motor bracket", "Recoater servo"], minutes=15, per_part=True),
        screws("Four M4 bearing-cap screws on the right wall", "bearing_cap", 3),
        place("Blade holder and blade", ["Blade holder", "HSS recoater blade"], minutes=2),
        screws("Two M3 blade screws", "blade", 2),
        place("Z stage hung under the floor", ["Z mounting flange", "Z actuator", "Z bracket", "Z servo", "Z carriage", "Z lift arm", "Pot magnet"],
              minutes=6),
        screws("Four counterbored M5 Z-flange screws from below", "zmount", 5),
        dict(do="module", label=f"Build module {module} in along its swap path (Z arm released)", minutes=3),
        screws("Two captive M6 screws pull the module flange up to the floor", "module_flange", 2, torque=True, pn="95966A705"),
        place("Gas knife and dose chute (hung under the lid line)", ["Gas knife", "Dose chute"], minutes=4),
        place("Lid O-ring cord into the body's gland", ["Lid O-ring"], path=None, minutes=4),
        place("Lid with its inserts", ["Chamber lid", "Window-flange helical", "Metering-base helical"], minutes=2),
        screws("Twenty M5 lid screws, star pattern", "lid", 15),
        place("Field stop, window flange and its O-ring", ["Field-stop", "Window flange", "Window-flange O-ring"], minutes=2),
        screws("Six counterbored M4 window-flange screws", "window", 4, torque=True),
        place("Window O-rings, fused-silica window, clamp ring, retaining ring", ["Window O-ring", "fused-silica window", "Window clamp ring",
                                                                                  "Window retaining ring"], minutes=4),
        screws("Six M3 retaining-ring screws (clamp the fused silica evenly)", "window_ring", 4, torque=True),
        place("Cover-slide drawer into the lid's front edge", ["Cover-slide drawer", "Cover slide (", "Drawer O-ring", "Drawer latches",
                                                                "Drawer latch wing head", "Drawer latch receptacles"],
              path=[(0, 0, 0), (0, -200, 0)], minutes=1),
        place("Drawer-closed sensor", ["Drawer-closed sensor"], minutes=2),
        place("Metering base, dock rails, load cell, NFC, stepper, seal housing, side port, docked sensor",
              ["Metering base", "Metering-base O-ring", "Metering-base dock-face", "NFC reader", "Dovetail rails", "Roller shaft:", "Roller feedthrough",
               "Roller drive coupling", "Dosing stepper", "Side reservoir port", "Reservoir-docked sensor", "Load cell"],
              minutes=10),
        screws("Four M4 metering-base screws", "dose", 4),
        place(f"Reservoir {res} onto the dovetail", [f"Reservoir {res}"], path=[(0, 0, 0), (0, -160, 0)], minutes=1),
        place("Camera viewport, window and camera, pressure transducer, relief valve", ["Camera viewport", "Camera adapter O-ring", "Camera window",
                                                                                        "Layer camera", "Pressure transducer", "Overpressure relief"],
              minutes=8),
        place("Hinge knuckles on the chamber front, draw-latch strikes on its side faces", ["Door hinge knuckles on the chamber", "Draw-latch strikes"], minutes=10),
        place("Door (with its O-ring, leaves, latch brackets and latches, handle), knuckles lined up", ["Chamber door", "Door O-ring", "Door hinge leaves",
                                                                                                       "Draw-latch brackets", "Draw latches",
                                                                                   "Door handle"], path=[(0, 0, 0), (0, -200, 0)], minutes=8,
              note="hinge and latch screws are not drawn"),
        place("Hinge pins slid in along x", ["Hinge pins"], path=[(0, 0, 0), (-160, 0, 0)], minutes=2),
        place("Optics bridge posts on the base plate", ["Optics bridge posts"], minutes=4),
        screws("Optics-post base screws, 2 x M6 up into each post from under the base plate", "bridge_base", 8),
        place("Optics bridge onto the posts", ["Optics bridge ("], minutes=3),
        screws("Optics-bridge screws, 2 x M6 x 35 down into each post", "bridge", 6),
        place("f-theta adapter ring under the bridge, galvo riser and galvo on the bridge", ["f-theta adapter ring", "Galvo riser plate", "2-axis galvo"], minutes=6),
        place("f-theta lens threaded up into its adapter ring from under the bridge", ["f-theta lens"], path=[(0, 0, 0), (0, 0, -60)], minutes=3),
        place("Beam tube, shutter, collimator, fiber", ["Enclosed beam tube", "Safety shutter", "Collimator", "Process fiber"], minutes=15),
        place("Laser guard: frame, panels, door rail, sliding door, lock", ["Guard frame", "Laser guard panels", "Guard door rail", "Sliding guard door", "OD 7+",
                                                                           "Guard-locking"], minutes=60),
        place("Rack frame, units, panels, operator panel", ["19 in. rack", "UPS (", "Fiber laser source", "Scan + laser", "DIN-rail", "Rack side panels",
                                                            "Operator panel", "E-stop", "Key switch", "Emission indicator", "Reset button"], path=None, minutes=60),
        place("Gas module base and units", ["Base plate, gas", "Leveling mounts, gas", "Dry scroll pump", "Pump inlet", "Sealed cyclone", "Filter inlet",
                                            "Filter outlet", "Sealed side-channel", "Blower inlet", "Blower outlet", "Trace O2", "Argon solenoid", "Argon pressure"],
              path=None, minutes=60),
        place("Vacuum valve, hoses, argon and O2 lines", ["Vacuum isolation valve", "Gas-loop + vacuum hoses", "Argon line", "O2 sample line"], path=None, minutes=45),
        place("Tray dock and umbilicals", ["Tray dock", "Umbilical duct", "Chilled-water", "Argon supply from the dock", "Pump exhaust"], path=None, minutes=30),
        note("Leak check: rate of rise from <= 1 mbar and O2 drift over 1 h at +20 mbar argon (pain-points P27)", 90),
    ]))

    # ============================== U. use ==============================
    ops.append(dict(id="U1", kind="use", name=f"Fill reservoir {res} and put it on the dock", where="glovebox or hood, then the tray at the access opening",
                    interval="each alloy / each build", state=OPEN, present="all", air=True, steps=[
        reach("Hand on the reservoir's pull tab (the lid handle carried forward to y -100, z 248..258, in front of the beam tube)", (XD, -85.0, 272.0),
              (FRONT,), skip=[f"Reservoir {res}"], hand=PINCH_HAND),
        remove(f"Reservoir {res} slides out on its dovetail and out through the guard door", [f"Reservoir {res}"],
               [[(0, 0, 0), (0, -125, 0), (0, -520, 0)]], minutes=1),
        note("Fill it in the glovebox (or under argon in a hood): ~80 g per 15 mm build; weigh, close, NFC tag", 15),
        note("Slide it back on (the reverse path, checked above); the dock cam opens its shutter", 1),
    ]))
    ops.append(dict(id="U2", kind="use", name="Start a build: plate in, door shut, purge, preheat", where="tray at the access opening",
                    interval="each build", state=OPEN_DOOR, present="all", air=True, steps=[
        reach("Plate in through the chamber door onto the bayonet (piston at +8 mm)", (0.0, 0.0, 45.0), (FRONT,), skip=["Build plate", "Plate rim wiper"],
              minutes=2),
        # since 2026-11-23 the latches ride on brackets on the door's ears and point forward: their levers are at y -207 when the door is
        # shut, in front of the front-right optics post (y -185..-125). Checked with the door shut (the latch moves with the door).
        reach("Close the door and the right draw latch (on the door's right bracket, lever at its front end)", (161.9, -222.0, 54.0),
              ((0, -1, 0), (-0.5, -0.85, 0), (0, -0.7, 0.7)), skip=["Draw latches", "Draw-latch strikes", "Draw-latch actuators"], minutes=1,
              hand=PINCH_HAND, state={"door": 0.0}),
        reach("Left draw latch", (-161.9, -222.0, 54.0), ((0, -1, 0), (0.5, -0.85, 0), (0, -0.7, 0.7)),
              skip=["Draw latches", "Draw-latch strikes", "Draw-latch actuators"], minutes=0, hand=PINCH_HAND, state={"door": 0.0}),
        note("Close the guard door (guard lock engages)", 0.5),
        note("Purge: 2-3 vacuum-argon cycles to <= 100 ppm O2 (budgets.py: 2 cycles from 1 mbar, 3 from 10 mbar), then flow", 15),
        note("Preheat the plate to 200 C (~15 min ramp on Ø50, README)", 15),
    ]))
    ops.append(dict(id="U3", kind="use", name="Build loop (dose, spread, expose, lower) - automated", where="tray in its bay or at the opening",
                    interval="each layer", state={}, present="all", air=False, steps=[
        note("Per layer: roller doses, blade spreads, camera checks, laser exposes, piston drops 30 um (robot/automation agent covers this)", 0),
        note("A 15 mm build is 500 layers; ~1.5 h for small cubes on a comparable machine (pain-points)", 90),
    ]))
    ops.append(dict(id="U4", kind="use", name="Finish a build: cool down, raise the plate, take it out, empty the overflow, return powder",
                    where="tray at the access opening", interval="each build", state=dict(OPEN_DOOR, piston=MP.Z_P_MAX), present="all", air=True, steps=[
        note("Cool the plate to < 50 C (door interlock, module_params.T_DOOR_OPEN): ~50 min for Ø50 (preheat-and-plates.md)", 50),
        note("Vent to air through the filter; passivation per the cleaning SOP (pain-points P35)", 10),
        reach("Hand through the chamber door to the plate (plate top at z = +8 mm; hand centre 37 mm above it)", (0.0, 0.0, 45.0), (FRONT,),
              skip=["Build plate", "Plate rim wiper"], minutes=1),
        remove("Plate: turned 60 deg off its bayonet, lifted 20 mm (spigot and lugs over the 8 mm door sill), out through the door",
               ["Build plate", "Plate rim wiper"], [[(0, 0, 0), (0, 0, 20), (0, -520, 20)]], rot=60.0, minutes=2),
        reach("Fingers on the overflow jar's KF-40 clamp under the floor", (100.0, -45.0, -70.0), ((0, -1, 0), (0.6, -0.8, 0), (1, 0, 0)),
              skip=["Overflow clamp", "Overflow jar"], minutes=1, hand=PINCH_HAND),
        remove("KF-40 clamp opened and taken off by hand", ["Overflow clamp"], [], minutes=1),
        remove("Overflow jar: clamp off, drop 5 mm off the centring ring, out", ["Overflow jar"],
               axis_paths(520.0, first=(0, 0, -5)), minutes=3),
        note("Sieve (63 um) and return powder in the glovebox; log mass", 20),
    ]))

    # ============================== M. maintenance ==============================
    ops.append(dict(id="M1", kind="maintenance", name="Cover slide: inspect, clean or replace", where="tray at the access opening",
                    interval="inspect each build; replace on fouling (transmission or camera limit, pain-points P12)", state=OPEN, present="all", air=True, steps=[
        reach("Fingers on the drawer's pull tab (lid front edge)", (0.0, -CY - 40.0, 135.0), (FRONT,), skip=["Cover-slide drawer"], hand=PINCH_HAND),
        remove("Quarter-turn latches released; drawer out of the lid and out through the guard door", ["Cover-slide drawer", "Cover slide (", "Drawer O-ring",
                                                                                                         "Drawer latches", "Drawer latch wing head"],
               [[(0, 0, 0), (0, -120, 0), (0, -520, 0)]], minutes=1),
        note("Lift the slide out of its pocket, clean (IPA, lens tissue) or replace; check the drawer O-ring", 5),
        note("Drawer back in (reverse path); purge before the next build", 1),
    ]))
    ops.append(dict(id="M2", kind="maintenance", name="Recoater blade: swap", where="tray at the access opening", interval="each alloy (hot-swap.md)",
                    state=OPEN_DOOR, present="all", air=True, steps=[
        reach("Hand with a key through the door to the blade screws (recoater parked)", (-50.0, -30.0, 50.0), (FRONT, (0.5, -0.85, 0)),
              skip=["Blade screws"], hand=PINCH_HAND),
        screws("Two M3 blade screws, heads toward +x, 14 mm above the floor", "blade", 3),
        remove("Blade off the holder (+x 5 mm), up 10 mm over the sill, out through the door", ["HSS recoater blade"],
               [[(0, 0, 0), (5, 0, 0), (5, 0, 10), (5, -520, 10)]], minutes=1),
        note("New blade against the holder's datum; set the 50 um gap with a feeler gauge", 10),
    ]))
    ops.append(dict(id="M3", kind="maintenance", name="Liners out, chamber cleaned (alloy change)", where="tray at the access opening",
                    interval="each alloy change (~1 h on an Aconity MINI, pain-points)", state=dict(OPEN_DOOR, recoater=0.0), present="all", air=True, steps=[
        note("Passivate condensate (slow air bleed, liner thermocouple watched) before vacuuming (pain-points P35)", 30),
        # six pieces since 2026-11-23 (lpbf_low section 5). The recoater sits at one end of its stroke while the pieces on the other side come out.
        remove("Right side liner with its pull tab: 4 mm in off the wall, 21 mm forward (the ball screw leaves its slot), in to x 105, down 6 mm, "
               "out through the door", ["Lift-out wall liner, right", "Liner pull tab, right"],
               [[(0, 0, 0), (-4, 0, 0), (-4, -21, 0), (-35, -21, 0), (-35, -21, -6), (-35, -541, -6)]], minutes=2, state={"recoater": 0.0}),
        remove("Back liner, upper right: 3 mm off the wall, forward over the ball screw, left 25 mm, out through the door",
               ["Lift-out wall liner, back upper right"], [[(0, 0, 0), (0, -3, 0), (0, -40, 0), (-25, -40, 0), (-25, -560, 0)]], minutes=1,
               state={"recoater": 0.0}),
        remove("Back liner, lower right: forward under the ball screw, left 25 mm, out through the door", ["Lift-out wall liner, back lower right"],
               [[(0, 0, 0), (0, -3, 0), (0, -40, 0), (-25, -40, 0), (-25, -560, 0)]], minutes=1, state={"recoater": 0.0}),
        note("Recoater to the right end of its stroke (x +100), so the carriage block is clear of the left pieces", 1),
        remove("Left side liner with its pull tab (mirror of the right)", ["Lift-out wall liner, left", "Liner pull tab, left"],
               [[(0, 0, 0), (4, 0, 0), (4, -21, 0), (35, -21, 0), (35, -21, -6), (35, -541, -6)]], minutes=2, state={"recoater": 206.0}),
        remove("Back liner, upper left: forward over the ball screw to y 54 (behind the dose chute), right 50 mm, out through the door",
               ["Lift-out wall liner, back upper left"], [[(0, 0, 0), (0, -3, 0), (0, -40, 0), (50, -40, 0), (50, -560, 0)]], minutes=1,
               state={"recoater": 206.0}),
        remove("Back liner, lower left: forward under the ball screw, right 26 mm, out under the dose chute and through the door",
               ["Lift-out wall liner, back lower left"], [[(0, 0, 0), (0, -3, 0), (0, -40, 0), (26, -40, 0), (26, -560, 0)]], minutes=1,
               state={"recoater": 206.0}),
        note("HEPA-vacuum the chamber, swab the coves, wipe the window side of the cover slide", 30),
    ]))
    ops.append(dict(id="M4", kind="maintenance", name="Lid off (lid O-ring, chute, gas knife, inside of the window)", where="tray at the access opening",
                    interval="lid O-ring: on damage or when the leak-up rate rises; not routine", state=OPEN, present="all", air=True, steps=[
        remove(f"Reservoir {res} out first", [f"Reservoir {res}"], [[(0, 0, 0), (0, -125, 0), (0, -520, 0)]], minutes=1),
        remove("Layer camera off its boss along its own (tilted) axis, out through the bridge's Ø80 hole, then to the front", ["Layer camera"],
               [[(0, 0, 0), tuple(100.0 * c for c in CAM_UP), tuple(100.0 * c + d for c, d in zip(CAM_UP, (0, -520, 0)))],
                [(0, 0, 0), tuple(140.0 * c for c in CAM_UP), tuple(140.0 * c + d for c, d in zip(CAM_UP, (0, -520, 0)))]]),
        screws("Twenty M5 lid screws, with the optics bridge 67 mm above the heads", "lid", 15),
        remove("Lid with everything on it: up as far as the lens allows, then out the front", LID_SET,
               [lift_then(5, FRONT), lift_then(15, FRONT), lift_then(19, FRONT)], minutes=5),
        note("Clean the gland, new FKM cord, refit; leak check 1 h", 90),
    ]))
    ops.append(dict(id="M5", kind="maintenance", name="Window: clean the inside face, replace the window O-ring", where="tray at the access opening",
                    interval="on fouling or when the leak-up rate rises", state=OPEN, present="all", air=True, steps=[
        screws("Six M3 retaining-ring screws, under the f-theta lens", "window_ring", 6, torque=True),
        remove("Retaining ring up and out", ["Window retaining ring"], [lift_then(6, FRONT), lift_then(15, FRONT)]),
        remove("Window up and out", ["fused-silica window"], [lift_then(12, FRONT), lift_then(18, FRONT)]),
        note("New FKM O-ring; window back with the ring torqued evenly; leak check", 60),
    ]))
    ops.append(dict(id="M6", kind="maintenance", name="Optics out (galvo + lens) for window or lid work", where="tray at the access opening",
                    interval="only when M4/M5 need it", state=OPEN, present="all", air=False, steps=[
        remove("f-theta lens unthreaded and lowered out of the bridge", ["f-theta lens"], [[(0, 0, 0), (0, 0, -60), (0, -520, -60)], [(0, 0, 0), (0, 0, -19)]]),
        remove("Galvo with the lens on it, lifted off the bridge", ["2-axis galvo", "f-theta lens"], [lift_then(80, FRONT), lift_then(60, FRONT)]),
        note("Refit, then re-calibrate the scan field (grid burn, galvo correction table)", 120),
    ]))
    ops.append(dict(id="M7", kind="maintenance", name="Build module on the bench: rod seals, gland O-ring, bore seal, heaters, thermocouples",
                    where="bench (module out, see S2)", interval="rod and bore seals on wear or powder past the seal; heaters and TCs on failure (P42, P43)",
                    state={}, present="module", bench=True, air=False, steps=[
        screws("Six M4 gland-plate screws from below", f"gland_{module}", 4),
        remove("Gland plate, heater stack, rod and its welded end down out of the bore together (the gland plate rides on the rod)",
               ["bottom flange: gland plate", "gland-plate O-ring", "Rod O-rings", "handle (6061", "Handle screws"] + STACK +
               ["Rod end", "Hermetic connector", "Hermetic-connector O-ring", "Striker disc", "Striker screws"], [[(0, 0, 0), (0, 0, -260)]], minutes=4),
        note("On the bench: the two rod set screws out of the head, the rod (with its welded end, connector and striker) pulled down out of the "
             "head's socket and through the gland plate; the two 2-114s then come out of their grooves. The rod's top end is a plain Ø15.875 tube "
             "end in the gland's Ø15.93 throat", 15),
        note("Heaters and thermocouples slide down out of the block once the head is off (3 stack screws); their leads run down the rod to the hermetic "
             "connector in the rod end", 60),
    ]))
    ops.append(dict(id="M8", kind="maintenance", name="Recoater shaft feedthrough (Ferrotec magnetic-fluid unit) and servo", where="tray at the access opening",
                    interval="on leak-up rise or feedthrough wear", state=OPEN, present="all", air=True, steps=[
        reach("Hand to the recoater servo, left of the chamber", (-289.0, 15.0, 51.0), (FRONT, (0, 0, 1)), skip=["Recoater servo", "Recoater motor"]),
        remove("Servo off its standoff", ["Recoater servo"], axis_paths(520.0, first=(-25, 0, 0)), minutes=5),
        remove("Motor standoff and bracket", ["Recoater motor standoff", "Recoater motor bracket"], axis_paths(520.0, first=(-10, 0, 0)), minutes=5),
        remove("Feedthrough unit and coupling off the left wall", ["Recoater fixed bearing", "Recoater shaft coupling"], axis_paths(520.0, first=(-30, 0, 0)),
               minutes=10),
        note("New packing; refit; leak check", 60),
    ]))
    ops.append(dict(id="M9", kind="maintenance", name="Dosing roller feedthrough (Ferrotec magnetic-fluid unit) and stepper", where="tray at the access opening",
                    interval="on leak-up rise", state=OPEN, present="all", air=True, steps=[
        remove("Dosing stepper off the metering base", ["Dosing stepper"], axis_paths(520.0, first=(0, 15, 0)), minutes=5),
        remove("Roller drive coupling and feedthrough", ["Roller drive coupling", "Roller shaft:"], axis_paths(520.0, first=(0, 12, 0)), minutes=5),
    ]))
    ops.append(dict(id="M10", kind="maintenance", name="Plate-height through-beam heads and sensors", where="tray at the access opening",
                    interval="on failure or misalignment", state=OPEN, present="all", air=False, steps=[
        reach("Fingers on the right through-beam head (outside the right wall, z = 5)", (180.0, 0.0, 5.0), (FRONT, UP, (1, 0, 0), (0, -0.7, 0.7), (0.5, -0.85, 0)),
              skip=["Plate-height through-beam"], hand=PINCH_HAND),
        reach("Left through-beam head", (-180.0, 0.0, 5.0), (FRONT, UP, (-1, 0, 0), (0, -0.7, 0.7), (-0.5, -0.85, 0)), skip=["Plate-height through-beam"],
              hand=PINCH_HAND),
        reach("Module-present sensor under the floor", (-55.0, -25.0, -40.0), (FRONT, (0, 0, -1)), skip=["Module-present sensor"], hand=PINCH_HAND),
        reach("Overflow-jar sensor", (150.0, -20.0, -118.0), (FRONT, (1, 0, 0)), skip=["Overflow-jar present"], hand=PINCH_HAND),
    ]))
    ops.append(dict(id="M11", kind="maintenance", name="Lubricate the recoater rail carriage and ball nut (vacuum grease)", where="tray at the access opening",
                    interval="rule of thumb: every 6 months or ~100 km of travel (~500 builds at 0.2 m per stroke); vendor manual not checked",
                    state=dict(OPEN_DOOR, recoater=100.0), present="all", air=True, steps=[
        reach("Grease gun nozzle to the carriage's end face (recoater moved to the centre)", (-35.0, 70.0, 62.0), (FRONT, (-0.5, -0.85, 0)),
              skip=["Recoater carriage"], hand=PINCH_HAND),
        reach("Ball nut", (16.0, 50.0, 55.0), (FRONT, (0.5, -0.85, 0)), skip=["Recoater ball nut", "Recoater ball screw"], hand=PINCH_HAND),
    ]))
    ops.append(dict(id="M12", kind="maintenance", name="HEPA element and cyclone (gas module)", where="tray at the access opening, two people",
                    interval="on pressure drop across the HEPA (pain-points P11: life depends on load, not hours)", state={}, present="all", air=True, steps=[
        note("Valve the housing off under argon; passivate by a slow air bleed with a thermocouple on the housing (P10)", 30),
        reach("Hands to the housing's top clamp", (470.0, -110.0, 90.0), (FRONT, UP), skip=["Sealed cyclone", "Filter inlet"], hand=PINCH_HAND),
        remove("Inlet hose end off the housing top", ["Filter inlet"], [[(0, 0, 0), (0, 0, 60)]]),
        dict(do="clear", label="Element out straight up: a Ø110 x 230 mm column above the housing must be free",
             box=(470.0 - 55.0, 470.0 + 55.0, -95.0, 15.0, 96.0, 96.0 + 230.0), skip=["Sealed cyclone", "Filter inlet", "Gas-loop + vacuum hoses"], minutes=10),
        note("Spent element under dry sand; Class D extinguisher at hand (P34, P10)", 10),
    ]))

    # ============================== S. swap-outs ==============================
    ops.append(dict(id="S1", kind="swap", name="Build plate swap", where="tray at the access opening", interval="each build",
                    state=dict(OPEN_DOOR, piston=MP.Z_P_MAX), present="all", air=True, steps=[
        remove("Old plate out (as U4)", ["Build plate", "Plate rim wiper"], [[(0, 0, 0), (0, 0, 20), (0, -520, 20)]], rot=60.0, minutes=2),
        note("New plate in (reverse path); graphite foil; turned 60 deg to lock", 2),
    ]))
    ops.append(dict(id="S2", kind="swap", name=f"Build module swap ({module})", where="tray at the access opening", interval="between campaigns",
                    state=dict(OPEN, zstage=MP.ZSTAGE_RELEASE), present="all", air=True, steps=[
        note("Cool, vent; Z arm released (drops 45 mm away from the striker)", 2),
        screws("Two captive M6 screws, from under the chamber", "module_flange", 3, pn="95966A705"),
        reach("Hand on the module handle's grip block, in front of the door", (0.0, -141.0, -47.0), (FRONT,), skip=["handle (6061"]),
        dict(do="module", label="Module out along its swap path (drop 40, forward 170, up 18, over the guard sill)", minutes=3),
        note("New module in (reverse path); captive screws at half torque (hot-swap.md); Z arm up; purge", 20),
    ]))
    ops.append(dict(id="S3", kind="swap", name=f"Reservoir swap ({res})", where="tray at the access opening", interval="each alloy",
                    state=OPEN, present="all", air=True, steps=[
        remove(f"Reservoir {res} out", [f"Reservoir {res}"], [[(0, 0, 0), (0, -125, 0), (0, -520, 0)]], minutes=1),
        note("Other reservoir on (reverse path); NFC read; the load cell tares", 1),
    ]))
    return ops
