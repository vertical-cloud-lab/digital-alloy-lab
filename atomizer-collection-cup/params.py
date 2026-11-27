"""Every size and property the collection-cup CAD and analyses use, in one place (mm, s, kg, C unless noted).

The CAD (`cad/`), the thermal and structural models (`analysis/`) and the CAM (`cam/`) all import this
file, so a measured number changes everywhere at once. Each interface number says where it came from.
`MEASURE_FIRST` lists the ones a person should check with calipers before metal is cut.
"""

from dataclasses import dataclass, field

# ----------------------------------------------------------------------------------------- interface
# The cone's outlet joint. Believed ISO-KF (a hinged clamp, a centring ring and an O-ring: Nov 13
# cleaning video boWsO0rxHvU, Nov 17 teardown LpvrzaWELpE). Size not yet confirmed: KF-50 is the
# working assumption, KF-40 the alternative. See dims/ for the photo measurements.


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
    ring_thk: float       # axial; sets the gap between the two sealing faces
    oring_cs: float       # O-ring cross-section
    clamp_od: float       # outside of the clamp ring (without wing nut)
    clamp_w: float        # axial width of the clamp

    @property
    def bore(self):
        return self.tube_od - 2 * self.tube_wall


KF50 = KF("KF-50", flange_od=75.0, tube_od=50.8, tube_wall=1.65, lip=7.0, hub_od=57.0, taper_deg=15.0,
          ring_id=48.0, ring_od=55.0, ring_thk=4.0, oring_cs=5.0, clamp_od=96.0, clamp_w=24.0)
KF40 = KF("KF-40", flange_od=55.0, tube_od=38.1, tube_wall=1.65, lip=7.0, hub_od=44.0, taper_deg=15.0,
          ring_id=36.0, ring_od=42.0, ring_thk=4.0, oring_cs=5.0, clamp_od=76.0, clamp_w=24.0)
JOINT = KF50

# Room under the cone. Nominal from the rough earlier model (viz3d: clamp at z = 288-300 mm, container
# down to z = 60 mm), to be replaced by the photo measurements and then by a tape measure.
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
STOCK = dict(
    neck_len=25.0, reducer_len=40.0, reducer_d2=100.0,
    valve_body_od=130.0, valve_body_h=45.0, valve_bore=60.0,
    top_plate_od=150.0, top_plate_t=15.0,
    glass_od=100.0, glass_wall=5.0, glass_len=110.0,
    bottom_plate_od=150.0, bottom_plate_t=15.0,
    tie_rod_d=12.0, tie_rod_bc=125.0, n_tie=4,
    guard_od=112.0, guard_t=1.0,
    seal_groove_w=8.0, seal_groove_d=4.0,
)

# ---------------------------------------------------------------------------- the lab-built cups
# Option A: catalogue parts only (no machining, no welding). KF full nipple, KF blank at the bottom,
# a drop-in liner and a loose catch puck.
A = dict(
    nipple_len=200.0,          # face to face; standard lengths come from bom/
    blank_t=12.0,              # KF blank, sealing face to back
    liner_od=44.45, liner_wall=1.24, liner_gap_top=6.0,   # 1-3/4 in x 0.049 in 304 tube
    puck_d=44.0, puck_h=38.0, puck_chamfer=2.0,           # 304 bar, sits on the blank
)

# Option B: one 316L vessel, TIG welded: KF-50 weld stub (2 in tube) + 2 x 3 in concentric reducer + 3 in
# tube + flat 8 mm bottom disc. Only one seal, at the water-cooled cone. A 304 liner and a 304 catch puck
# drop in. The 3 in body gives the capacity a 2 in nipple can't (see option_capacity_cm3()).
B = dict(
    stub_len=25.0,             # KF weld stub's own tube below the flange face (vendor drawing in bom/)
    reducer_len=64.0,          # 2 x 3 in sanitary butt-weld concentric reducer (vendor)
    body_od=76.2, body_wall=1.65,  # 3 in x 0.065 in 316L tube
    body_len=250.0,            # KF face to the outside of the bottom; set from the measured room
    bottom_t=8.0,              # welded 316L disc (a flat floor and some heat sink)
    liner_od=69.85, liner_wall=1.24,   # 2-3/4 in x 0.049 in 304 tube, stands on the puck
    puck_d=70.0, puck_h=25.0, puck_chamfer=2.0,
)

# Option C: glass rebuild. Stock plates, tie rods and valve body; fused-quartz tube; FKM seals; a
# 304 liner sleeve hung in the top bore that covers the valve seat and the glass rim.
C = dict(
    quartz_od=100.0, quartz_wall=5.0, quartz_len=110.0,
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
