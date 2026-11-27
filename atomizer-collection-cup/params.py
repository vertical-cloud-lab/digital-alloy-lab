"""Every size and property the collection-cup CAD and analyses use, in one place (mm, s, kg, C unless noted).

The CAD (`cad/`), the thermal and structural models (`analysis/`) and the CAM (`cam/`) all import this
file, so a measured number changes everywhere at once. Each interface number says where it came from.
`MEASURE_FIRST` lists the ones a person should check with calipers before metal is cut.
"""

from dataclasses import dataclass, field

# ----------------------------------------------------------------------------------------- interface
# The cone's outlet joint: ISO-KF, size KF-50 (dims/README.md: a metal centring ring inside a brown O-ring on a
# flat face, a hinged wing-nut clamp; O-ring OD / flange OD = 0.827 in photo 04, which rules out KF-40).
# Flange, ring, O-ring and clamp sizes are the vendors' (bom/vendor_dims.json: Lesker QF50 drawings, MDC PG092,
# McMaster 4518K38/K61/K65/K74 STEP files measured with CadQuery).


@dataclass(frozen=True)
class KF:
    """ISO-KF (ISO 2861 / DIN 28403) flange, nominal. Verify against the vendor drawing (bom/)."""
    name: str
    flange_od: float      # mm
    tube_od: float        # weld tube OD (inch tube)
    tube_wall: float
    lip: float            # axial thickness of the flange disc at its OD
    hub_od: float         # where the 15 deg back taper meets the hub
    taper_deg: float      # back taper the clamp bears on
    ring_id: float        # centring ring bore (metal)
    ring_od: float        # centring ring OD at the O-ring groove root
    ring_thk: float       # face-to-face gap when clamped = the O-ring's squeezed height (see recess_depth)
    oring_cs: float       # O-ring cross-section
    clamp_od: float       # outside of the clamp ring (without wing nut)
    clamp_w: float        # axial width of the clamp
    recess_d: float = 0.0       # centring-ring recess in each sealing face (diameter)
    recess_depth: float = 0.0   # its depth; ring body thickness = ring_thk + 2 * recess_depth
    ring_body_od: float = 0.0   # the ring's body (in the recesses); ring_od is its rib, = the O-ring's ID

    @property
    def bore(self):
        return self.tube_od - 2 * self.tube_wall


# KF-50: flange OD 74.93, 5.08 thick at the hub, 2.9 at the rim, 15 deg back taper (all vendors); face recess
# 52.32 dia (McMaster STEP). Ring bore 49.4-50.0, body OD 51.9, 7.98 thick; O-ring AS568-330, 53.34 x 5.33
# (Lesker QF50-200-SRV). McMaster's STEP gives a 2.6 mm recess, which with the 7.98 ring would leave a 2.8 mm
# face gap: the O-ring squeezed by half, and too thin for the over-pressure ring (A&N 4000076 / Lesker
# QF50-200-OPR, 3.81 mm wide), which sits between the faces. A gap of at least 3.81 mm means a recess of at most
# (7.98 - 3.81) / 2 = 2.09 mm, so 2.0 mm (4.0 mm gap, 25 % squeeze) is used; McMaster's models are approximate.
# Clamp: Lesker
# QF50-200-SSC body OD 82 x 20 wide, McMaster 4518K74 94 x 26.4; 90 x 22 is drawn.
KF50 = KF("KF-50", flange_od=74.93, tube_od=50.8, tube_wall=1.65, lip=5.08, hub_od=58.6, taper_deg=15.0,
          ring_id=49.7, ring_od=53.34, ring_thk=4.0, oring_cs=5.33, clamp_od=90.0, clamp_w=22.0,
          recess_d=52.32, recess_depth=2.0, ring_body_od=51.9)
KF40 = KF("KF-40", flange_od=55.0, tube_od=38.1, tube_wall=1.65, lip=7.0, hub_od=44.0, taper_deg=15.0,
          ring_id=36.0, ring_od=42.0, ring_thk=4.0, oring_cs=5.0, clamp_od=76.0, clamp_w=24.0)
JOINT = KF50

# Room under the cone: NOT measured (dims/README.md: no photo or frame shows it at a known scale). 300 +/- 50 mm
# is the rough October model's value (viz3d: clamp at z = 288-300 mm). Measure with the cone latched.
Z_JOINT_FACE = 300.0          # cone's outlet sealing face above the mat (mm)
FLOOR_CLEARANCE_MIN = 25.0    # keep the cup's bottom at least this far above the mat
CONE_OUTLET_SPIGOT_OD = 50.8  # the cone's own outlet tube, above its KF flange
CONE_OUTLET_LEN = 40.0        # visible length of that spigot below the cone body
CONE_HALF_ANGLE = 30.0        # deg from the axis; the cone section under the chamber (photos)
CONE_TOP_D = 210.0            # the cone's mouth (frame with the two green toggle latches)
CONE_H = 120.0

# --------------------------------------------------------------------------------- the stock cup
# As seen in the training videos and the Nov 13/17 photos; used for the "before" model and the
# comparison runs. Rough until dims/ has the measured values.
# Photo and video measurements in dims/README.md (each with its +/- and source); the rest are estimates.
# Layout, top to bottom: KF-50 flange and neck, conical reducer to ~65 mm, a DN65 sanitary butterfly valve
# (bolted halves holding the EPDM seat; 4-bolt flange ~111 OD), the top plate, the glass in its guard, the bottom
# plate, 4 x M12 tie rods between the plates.
STOCK = dict(
    neck_len=12.0, reducer_len=30.0, reducer_d2=65.0,           # KF face to the valve flange ~53 (dims)
    valve_body_od=111.0, valve_body_h=50.0, valve_bore=60.0,     # 111 +/- 15, bore ~60 inferred (dims)
    top_plate_od=170.0, top_plate_t=10.0,                        # OD as the bottom plate (by eye); t estimated
    glass_od=100.0, glass_wall=5.0, glass_len=110.0,             # 96 +/- 6, 5.7 +/- 1, ~110 (dims); run record 100
    bottom_plate_od=170.0, bottom_plate_t=10.0,                  # 170.5 +/- 9 (dims); rim ~6 +/- 1.5, t estimated
    tie_rod_d=12.0, tie_rod_bc=145.0, n_tie=4,                   # M12 (dims), bolt circle 145 +/- 10
    guard_od=116.0, guard_t=1.0,                                 # 116 +/- 15 (dims)
    seal_groove_w=8.0, seal_groove_d=3.0,                        # band 107 / 92 (dims); depth not seen
)

# ---------------------------------------------------------------------------- the lab-built cups
# Option A: catalogue parts only (no machining, no welding). KF full nipple, KF blank at the bottom,
# a drop-in liner and a loose catch puck.
A = dict(
    nipple_len=160.0,          # face to face: Duniway KF50-NP 160 mm (stock lengths 140/160/163/320; bom/)
    blank_t=5.08,              # KF blank, sealing face to back (Lesker QF50-200-SB, McMaster 4518K61)
    liner_od=44.45, liner_wall=1.24, liner_gap_top=6.0,   # 1-3/4 in x 0.049 in 304 tube (McMaster 11116N835)
    puck_d=44.0, puck_h=30.0, puck_chamfer=2.0,           # 304 bar (2 in), sits on the blank inside the ring
)

# Option B: one 316L vessel, TIG welded: KF-50 weld stub (2 in tube) + 2 x 3 in concentric reducer + 3 in
# tube + flat 8 mm bottom disc. Only one seal, at the water-cooled cone. A 304 liner and a 304 catch puck
# drop in. The 3 in body gives the capacity a 2 in nipple can't (see option_capacity_cm3()).
B = dict(
    stub_len=19.05,            # KF-50 x 2 in butt-weld stub, face to tube end (McMaster 4518K38, Lesker QF50-200-SST)
    reducer_len=101.6,         # 3 x 2 in butt-weld concentric reducer, 316L, 0.065 wall (McMaster 5237K471)
    body_od=76.2, body_wall=1.65,  # 3 in x 0.065 in 316 tube (OnlineMetals 4256)
    body_len=250.0,            # KF face to the outside of the bottom; check against the measured room
    bottom_t=8.0,              # welded 316L disc (a flat floor and some heat sink)
    liner_od=69.85, liner_wall=1.65,   # 2-3/4 in x 0.065 in 304 tube (McMaster 11116N864; 0.049 not stocked)
    puck_d=70.0, puck_h=25.0, puck_chamfer=2.0,
)

# Option C: glass rebuild. Stock plates, tie rods and valve body; fused-quartz tube; FKM seals; a
# 304 liner sleeve hung in the top bore that covers the valve seat and the glass rim.
C = dict(
    quartz_od=100.0, quartz_wall=4.0, quartz_len=110.0,       # MTI HQT100: 100 x 92 mm (5 mm wall is custom)
    sleeve_od=56.0, sleeve_wall=1.0, sleeve_len=75.0, sleeve_lip_od=64.0,
)

# ------------------------------------------------------------------------------- loads and limits
P_VAC_ABS = 0.010       # bar absolute at the bottom of a pump-down (HMI -850 mbar at ~860 mbar room)
P_RUN_G = 0.150         # bar gauge during a pour
P_RELIEF_G = 0.80       # bar gauge, the chamber's mechanical relief valve (training video 1, 6:42)
P_DESIGN_INT = 1.5 * P_RELIEF_G
P_DESIGN_EXT = 1.0      # full vacuum, bar

# Hot shot: 630 bronze (C63000) at the plate; values as in atomizer-runs/2026-11-13/estimates.py
SHOT = dict(T_arrive=1050.0, T_sol=1040.0, T_liq=1054.0, cp_s=480.0, cp_l=530.0, L=230e3,
            rho=7600.0, k=40.0)
SHOT_MASSES_G = (25, 50, 100, 200, 400, 816)

# Seal limits (C): continuous / short excursion. Sources in analysis/README.md.
SEAL_LIMITS = {"EPDM": (150, 175), "FKM": (200, 250), "VMQ silicone": (200, 230), "FFKM": (275, 320),
               "PTFE": (260, 300)}

MATERIALS = {  # k W/m/K, rho kg/m3, cp J/kg/K, E GPa, nu, alpha 1/K, emissivity (outside, oxidised)
    "316L": dict(k=16.3, rho=8000, cp=500, E=193, nu=0.30, alpha=16.0e-6, eps=0.35),
    "304": dict(k=16.2, rho=8000, cp=500, E=193, nu=0.29, alpha=17.3e-6, eps=0.35),
    "Cu": dict(k=390, rho=8940, cp=385, E=117, nu=0.34, alpha=17.0e-6, eps=0.3),
    "borosilicate": dict(k=1.2, rho=2230, cp=830, E=64, nu=0.20, alpha=3.3e-6, eps=0.9),
    "fused_quartz": dict(k=1.4, rho=2200, cp=740, E=72, nu=0.17, alpha=0.55e-6, eps=0.9),
    "FKM": dict(k=0.2, rho=1850, cp=1400, E=0.006, nu=0.49, alpha=160e-6, eps=0.9),
    "EPDM": dict(k=0.25, rho=1150, cp=1800, E=0.005, nu=0.49, alpha=160e-6, eps=0.9),
}

MEASURE_FIRST = [
    "cone outlet joint: KF or tri-clamp, and its size (read the clamp, or caliper the flange OD)",
    "height of the cone's outlet sealing face above the mat, with the cone latched",
    "bore of the cone's outlet spigot",
    "stock cup: overall height, and the glass OD, wall and length (the broken glass is in hand)",
    "stock plates: groove ID/OD/depth for the glass seals, plate thickness, tie-rod size and bolt circle",
    "whether the cup's weight hangs on the clamp or rests on a support",
    "the splash plate's width, radius and thickness, and the bore it hooks into",
    "which seals are in the spares kit (training video 9, 36:58: 'You have spare glass ... and the seal under the glass')",
]


def option_capacity_cm3():
    """Usable volume of each lab-built option (to 15 mm below the top face), cm3."""
    import math
    j = JOINT
    a_bore = math.pi / 4 * j.bore ** 2
    a_liner = math.pi / 4 * (A["liner_od"] - 2 * A["liner_wall"]) ** 2
    out = {}
    h_a = A["nipple_len"] - A["puck_h"] - 15.0
    out["A (liner + puck)"] = a_liner * h_a / 1e3
    out["A (no liner, no puck)"] = a_bore * (A["nipple_len"] - 15.0) / 1e3
    a_body = math.pi / 4 * (B["body_od"] - 2 * B["body_wall"]) ** 2
    a_bliner = math.pi / 4 * (B["liner_od"] - 2 * B["liner_wall"]) ** 2
    h_straight = B["body_len"] - B["stub_len"] - B["reducer_len"] - B["bottom_t"]
    out["B (no liner, no puck)"] = (a_body * h_straight + a_bore * (B["stub_len"] + B["reducer_len"] - 15.0)) / 1e3
    out["B (liner + puck)"] = (a_bliner * (h_straight - B["puck_h"]) + a_bore * (B["stub_len"] + B["reducer_len"] - 15.0)) / 1e3
    return out


if __name__ == "__main__":
    for k, v in option_capacity_cm3().items():
        print(f"{k:>24s}: {v:6.0f} cm3")
