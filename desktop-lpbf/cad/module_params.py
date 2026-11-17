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
BOT_FLANGE_T = 10.0     # module bottom flange (double FKM O-ring rod gland)
ROD_OD, ROD_ID = 15.875, 12.7                         # 5/8 in. x 0.065 in. wall 316 tube
ROD_END_T = 14.0        # rod-end hardware: 430 SS striker (5) + potted end cap with a side cable exit (9)
ROD_L = (OVERTRAVEL - (-(BUILD_STROKE + STOP_BELOW))) + BOT_FLANGE_T + ROD_END_T + 3.0   # 77: piston-head bottom to the coupling face
ARM_T = 12.0            # Z lift arm under the coupling face (pot magnet set flush in its top)
ZSTAGE_RELEASE = -45.0  # arm drops 45 mm below the rod end (magnet breaks away) before a module swap
MODULE_DROP = 40.0      # module drops 40 mm: spigot out of the floor port and under the outlet plenum

# ---- floor port (one port takes every module) ----
FLOOR_T = 20.0
PORT_D = 96.0           # through-hole in the chamber floor; every module's spigot fills it, flush with the floor
SPIGOT_FIT = 0.03       # radial clearance spigot / port (H7/g6 at 96 mm)
FLANGE_D = 100.0        # module flange disc under the floor
FLANGE_T = 10.0
TAB_X = 64.0            # two tabs to x = +/-64 carry the captive M6 thumb screws at x = +/-58
SCREW_X = 58.0
SPIGOT_ORING = "2-240"  # FKM, radial (piston-type) static seal on the spigot OD, in the floor port

# ---- module sizes ----
# bore: honed (H7, Ra <= 0.4 um) after the spigot-flange is welded to the 316L tube.
# plate clearance is radial, cold, and set per heating tier (the plate is Al, the bore stainless):
#   Tier A (<= 200 C) 0.10 mm; Tier B (500 C, reserved) 0.20 mm. Heater block clearance 0.30 mm.
# heaters: 24 V DC cartridges (Tier A) in radial holes at mid-block, count x watts sized by analysis/thermal_module.py
MODULES = {
    "S25": dict(bore=25.4, wall=3.0, heaters=1, heater_w=40.0, heater_d=6.0, heater_l=20.0,
                reservoir="S", blade_len=45.0, label="Ø25 module"),
    "M50": dict(bore=50.8, wall=3.0, heaters=2, heater_w=40.0, heater_d=6.0, heater_l=20.0,
                reservoir="M", blade_len=70.0, label="Ø50 module"),
    "L75": dict(bore=76.2, wall=3.0, heaters=4, heater_w=40.0, heater_d=6.0, heater_l=20.0,
                reservoir="L", blade_len=95.0, label="Ø75 module"),
}
CLEAR = {"A": dict(plate=0.10, block=0.30, t_max=200.0), "B": dict(plate=0.20, block=0.35, t_max=500.0)}
for k, m in MODULES.items():
    m["plate_d"] = m["bore"] - 2 * CLEAR["A"]["plate"]
    m["block_d"] = m["bore"] - 2 * CLEAR["A"]["block"]
    m["tube_od"] = m["bore"] + 2 * m["wall"]
    m["spigot_wall"] = (PORT_D - m["bore"]) / 2
    m["standoff_r"] = 0.55 * m["bore"] / 2 if k != "S25" else 0.0     # S25: one central standoff
    m["n_standoffs"] = 3 if k != "S25" else 1
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
