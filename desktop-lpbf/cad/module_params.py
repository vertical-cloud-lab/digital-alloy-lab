"""Shared parameters for the swappable heated build modules, the hopper reservoirs and the automation parts
of the low-profile desktop LPBF (issue #260, PR #266). Pure Python (no CadQuery), so the CAD model
(lpbf_low.py), the thermal FEA (analysis/thermal_module.py) and the sizing scripts all read the same numbers.

Units mm, degrees C, W. Origin and axes as in lpbf_low.py: z = 0 is the powder plane (chamber floor top),
+X is the recoat direction, +Y points to the back.

Stack in every module, top down, with the plate top at z_p (z_p = 0 at the start of a build):
  build plate      z_p - PLATE_T .. z_p             6061-T6 (or 5083-H321 held at 200 C); bayonet spigot underneath
  contact face     preloaded flat face, plate on the heater block
  heater block     .. - BLOCK_T                     6061-T6, 24 V cartridge heaters in radial holes, 2 type K thermocouples
  thermal break    .. - BREAK_T                     3 Macor standoffs + 2 polished 316 radiation shields, argon gap
  piston head      .. - HEAD_T                      6061-T6 (Tier A) or 316L with a water channel (Tier B); carries the bore seal
  hollow rod       .. - ROD_L                       316 tube, inert inside; heater and thermocouple leads run down it
"""

# ---- vertical stack (shared by every module size) ----
PLATE_T = 10.0
BLOCK_T = 14.0
BREAK_T = 8.0           # Macor standoff height = argon gap between block and head
HEAD_T = 18.0
STACK = PLATE_T + BLOCK_T + BREAK_T + HEAD_T          # 50 mm, plate top to piston-head bottom
BUILD_STROKE = 40.0     # z_p from 0 down to -40 during a build
STOP_BELOW = 2.0        # bottom stop 2 mm below the deepest build position
OVERTRAVEL = 8.0        # z_p = +8: plate rim stands 8 mm proud of the floor so a gripper can take it
Z_P_MIN = -(BUILD_STROKE + STOP_BELOW)                # -42
Z_P_MAX = OVERTRAVEL                                  # +8
BOT_FLANGE_T = 14.0     # module gland plate, bolted under a collar welded to the tube end. 14 mm (was 10) so it holds two
                        # Parker dynamic rod glands (3.6 mm wide each) with 2.3 mm lands (seals.md, item 6)
COLLAR_T = 8.0          # 316L collar ring TIG-welded round the tube's bottom end; the gland plate's 6 x M4 screws thread into it
COLLAR_W = 12.0         # collar radial width beyond the tube OD (bolt circle at tube OD + 6.5 mm)
ROD_OD, ROD_ID = 15.875, 12.7                         # 5/8 in. x 0.065 in. wall 316 tube (M50, L75)
ROD_S25 = (9.525, 7.747)                              # 3/8 in. x 0.035 in. wall 316 tube for S25: its Ø24.8 piston head has no room
                                                      # for the stack screws' counterbores beside a 5/8 in. rod socket
SEAL_DEPTH = {"S25": 1.6}                             # radial depth of the bore-seal groove (3.0 elsewhere): S25's stack screws pass inside it
ROD_END_T = 24.0        # rod-end hardware: 430 SS striker (5) + end cap (19) carrying a hermetic glass-to-metal connector on its
                        # side (was 14 with a potted cable exit: stranded leads wick gas along the strands, seals.md item 7)
ROD_L = (OVERTRAVEL - (-(BUILD_STROKE + STOP_BELOW))) + BOT_FLANGE_T + ROD_END_T + 3.0   # 77: piston-head bottom to the coupling face
ARM_T = 12.0            # Z lift arm under the coupling face (pot magnet set flush in its top)
ZSTAGE_RELEASE = -45.0  # arm drops 45 mm below the rod end (magnet breaks away) before a module swap
MODULE_DROP = 40.0      # module drops 40 mm: spigot out of the floor port and under the outlet plenum

# ---- floor port (one port takes every module) ----
FLOOR_T = 20.0
PORT_D = 96.0           # through-hole in the chamber floor; every module's spigot fills it, flush with the floor
SPIGOT_FIT = 0.10       # radial clearance spigot / port. The FEA found 0.03 mm (H7/g6) closing to -23 um hot with powder in
                        # the plate gap; the O-ring seals, and two dowels in the floor locate the module on its flange
DOWEL_Y = 54.0          # Ø6 dowel (y = +54) and diamond pin (y = -54) in the floor's underside, through two lugs on the flange
PLATE_BLOCK_HC = 5000.0 # W/m2K, plate on the heater block through graphite foil (bare Al-Al face ~2000; the FEA found S25's block
                        # at its 240 C cutoff with 2000)
FLANGE_D = 100.0        # module flange disc under the floor
FLANGE_T = 10.0
TAB_X = 64.0            # two tabs to x = +/-64 carry the captive M6 thumb screws at x = +/-58
SCREW_X = 58.0
SPIGOT_ORING = "2-238"  # FKM 75A, radial static seal in a groove on the spigot OD
SPIGOT_GROOVE = dict(root_d=90.5, width=4.8, z0=3.6)   # root Ø90.5 x 4.8 wide (was 90.2 x 3.6: 101 % fill at worst tolerance),
                        # from zf + 3.6: 17-25 % squeeze, <= 81 % fill (analysis/seals/seals.py)

# ---- module sizes ----
# bore: honed (H7, Ra <= 0.4 um) after the spigot-flange is welded to the 316L tube.
# plate clearance is radial, cold, and set per heating tier (the plate is Al, the bore stainless):
#   Tier A (<= 200 C) 0.10 mm; Tier B (500 C, reserved) 0.20 mm. Heater block clearance 0.30 mm.
# heaters: 24 V DC cartridges (Tier A) in radial holes at mid-block, count x watts sized by analysis/thermal_module.py
MODULES = {
    "S25": dict(bore=25.4, wall=3.0, heaters=2, heater_w=50.0, heater_d=6.0, heater_l=22.0,
                reservoir="S", blade_len=45.0, label="Ø25 module"),
    "M50": dict(bore=50.8, wall=3.0, heaters=3, heater_w=50.0, heater_d=6.0, heater_l=22.0,
                reservoir="M", blade_len=70.0, label="Ø50 module"),
    "L75": dict(bore=76.2, wall=3.0, heaters=5, heater_w=50.0, heater_d=6.0, heater_l=22.0,
                reservoir="L", blade_len=95.0, label="Ø75 module"),
}
CLEAR = {"A": dict(plate=0.10, block=0.30, t_max=200.0), "B": dict(plate=0.20, block=0.35, t_max=500.0)}
# Tier A cold radial plate clearance per size. The thermal FEA (analysis/out/thermal) found that with 0.10 mm the hot
# Al plate closes the gap in the cooler stainless spigot at the start of a build: +5 um on M50 and -36 um (seized) on
# L75. Plate growth minus bore growth at 200 C is ~0.05 / 0.10 / 0.14 mm radial, so these leave ~0.05 mm hot.
PLATE_CLEAR_A = {"S25": 0.10, "M50": 0.15, "L75": 0.20}
for k, m in MODULES.items():
    m["plate_clear"] = PLATE_CLEAR_A[k]
    m["plate_d"] = m["bore"] - 2 * m["plate_clear"]
    m["block_d"] = m["bore"] - 2 * CLEAR["A"]["block"]
    m["tube_od"] = m["bore"] + 2 * m["wall"]
    m["spigot_wall"] = (PORT_D - m["bore"]) / 2
    m["standoff_r"] = {"S25": 9.0, "M50": 18.0}.get(k, 0.8 * m["block_d"] / 2)    # as modules_low.block_layout
    m["standoff_d"] = 8.0 if k != "S25" else 5.0
    m["n_standoffs"] = 3
MACOR = dict(d=8.0, k=1.46, t_max=800.0)    # Macor standoffs Ø8 x BREAK_T
RAD_SHIELDS = 2                              # 0.1 mm polished 316 shields in the argon gap

# ---- largest module sets the recoat and gas geometry ----
DOSE_HALF = 50.0        # dose line / blade half-length (y): plate radius 38.1 + ~12 mm
X_DOSE, X_PARK, X_END = -90.0, -106.0, 100.0
OVF_X0, OVF_X1 = 90.0, 110.0
INLET_HALF = 60.0       # cross-flow inlet slot half-width (x), 120 x 8 mm
OUTLET_HALF = 62.0      # outlet floor slot half-length (x)
OUTLET_Y = (-94.0, -86.0)

# ---- hopper: fixed metering base + docking reservoirs (all slide out to the front under the optics bridge) ----
# interior x, y, z of the reservoir body; outlet slot length = plate diameter + ~20 mm; gate opens on docking.
RESERVOIRS = {
    "S": dict(ix=26.0, iy=46.0, iz=36.0, slot=45.0, for_module="S25"),
    "M": dict(ix=26.0, iy=72.0, iz=56.0, slot=70.0, for_module="M50"),
    "L": dict(ix=48.0, iy=110.0, iz=56.0, slot=95.0, for_module="L75"),
}
WEDGE_HALF_ANGLE = 35.0  # deg from vertical, 304 2B walls: plane-flow (wedge) hopper toward mass flow for fine Al powder
SLOT_W = 8.0             # outlet slot width (x) over the metering roller
GATE_T = 4.0             # spring-closed slide gate under each reservoir, opened by a cam on the dock
for k, r in RESERVOIRS.items():
    import math as _m
    h = (r["ix"] - SLOT_W) / 2 / _m.tan(_m.radians(WEDGE_HALF_ANGLE))
    r["wedge_h"] = h
    r["vol_cm3"] = r["iy"] * ((r["ix"] + SLOT_W) / 2 * h + r["ix"] * (r["iz"] - h)) / 1000.0
SIDE_PORT = "KF-16, back face of the metering base, blanked: reserved for a >= 500 cm3 side reservoir with an auger"

# ---- heated-plate control and interlocks ----
T_SET_A = 200.0
T_DOOR_OPEN = 50.0      # guard and chamber door stay locked until the plate is below this
T_LIMIT_A = 240.0       # independent limit controller trips (latching) above this
TCO_A = 240.0           # thermal cutoff in series with the heaters, in the heater block
HEATER_V = 24.0


# ---- seals: AS568 FKM 75A O-rings (Parker ORD 5700 glands; see seals.md and analysis/seals/seals.py) ----
# AS568 dash number -> (ID, cross-section) in mm, from the AS568 inch sizes.
_AS568_IN = {"2-006": (0.114, 0.070), "2-007": (0.145, 0.070), "2-008": (0.176, 0.070), "2-009": (0.208, 0.070), "2-010": (0.239, 0.070),
             "2-011": (0.301, 0.070), "2-012": (0.364, 0.070), "2-013": (0.426, 0.070), "2-014": (0.489, 0.070), "2-015": (0.551, 0.070),
             "2-016": (0.614, 0.070), "2-017": (0.676, 0.070), "2-018": (0.739, 0.070), "2-019": (0.801, 0.070), "2-020": (0.864, 0.070),
             "2-021": (0.926, 0.070), "2-022": (0.989, 0.070), "2-023": (1.051, 0.070), "2-024": (1.114, 0.070), "2-025": (1.176, 0.070),
             "2-026": (1.239, 0.070), "2-027": (1.301, 0.070), "2-028": (1.364, 0.070), "2-029": (1.489, 0.070), "2-030": (1.614, 0.070),
             "2-031": (1.739, 0.070), "2-032": (1.864, 0.070), "2-033": (1.989, 0.070), "2-034": (2.114, 0.070), "2-035": (2.239, 0.070),
             "2-036": (2.364, 0.070), "2-037": (2.489, 0.070), "2-038": (2.614, 0.070), "2-039": (2.739, 0.070), "2-040": (2.864, 0.070),
             "2-041": (2.989, 0.070), "2-042": (3.239, 0.070), "2-043": (3.489, 0.070), "2-044": (3.739, 0.070), "2-045": (3.989, 0.070),
             "2-046": (4.239, 0.070), "2-047": (4.489, 0.070), "2-048": (4.739, 0.070), "2-049": (4.989, 0.070), "2-050": (5.239, 0.070),
             "2-110": (0.362, 0.103), "2-114": (0.612, 0.103), "2-238": (3.484, 0.139), "3-904": (0.351, 0.072)}
AS568 = {k: (round(a * 25.4, 2), round(b * 25.4, 2)) for k, (a, b) in _AS568_IN.items()}
FACE_1P78 = dict(cs=1.78, depth=1.32, width=2.3)        # Parker face gland for 1.78 mm cord, gas/vacuum column (also the half-dovetail)
DOVETAIL_DEG = 24.0                                      # half-dovetail: outer wall undercut 24 deg (Parker 66 deg wall)


def pick_ring(inner_perimeter_mm, cs=1.78, target=0.02, max_stretch=0.05):
    """AS568 ring for a face groove whose inner wall has this perimeter: the ring is stretched onto the inner wall (external
    pressure at vacuum pushes it inward), aiming at ~2 % and never above 5 % stretch. Returns (dash, ID, stretch)."""
    best = None
    for k, (d, c) in AS568.items():
        if abs(c - cs) > 0.05 or not k.startswith("2-0"):
            continue
        st = inner_perimeter_mm / (math.pi * d) - 1.0
        if 0.0 <= st <= max_stretch and (best is None or abs(st - target) < abs(best[2] - target)):
            best = (k, d, st)
    return best


import math  # noqa: E402  (pick_ring uses it; module_params stays pure Python)

# gland plate face seal on the welded collar: groove 2.6 wide (was 2.4: 94 % fill), 1.3 deep; inner diameter set so a standard
# AS568 ring sits on the inner wall with 1.5-3.3 % stretch
GLAND_PLATE_SEAL = {"S25": dict(ring="2-024", groove_id=28.72), "M50": dict(ring="2-034", groove_id=54.5), "L75": dict(ring="2-041", groove_id=78.4)}
GLAND_PLATE_GROOVE = dict(width=2.6, depth=1.3)
# rod gland: two Parker dynamic (reciprocating) rod glands in the gland plate; seamless polished 316 rod
ROD_GLAND = {"M50": dict(ring="2-114", groove_d=20.0, throat_d=15.93, width=3.6), "L75": dict(ring="2-114", groove_d=20.0, throat_d=15.93, width=3.6),
             "S25": dict(ring="2-110", groove_d=13.64, throat_d=9.58, width=3.6)}
RES_BASE_HALF_Y = 56.2   # one docking-plate footprint for every reservoir (the L reservoir's): 30 x 112.4 mm
DOCK_OPENING = (12.0, 100.0)   # dose opening in the dock face (x, y): takes every reservoir's slot (45 / 70 / 95 x 8)
