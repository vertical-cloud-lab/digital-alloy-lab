"""The fast-track shop's small common tool library, thread data and shop-time allowances (#260).

Plain Python (no CadQuery, no FreeCAD), so parts.py (venv), cam.py (FreeCAD's own Python) and sim.py all import it.

Feeds for 6061-T6 follow PR 266's freecad_cam.py (conservative vendor ranges):
  end mills: mm/min = rpm x flutes x chip load (in./tooth) x 25.4; plunge and ramp at half that
  drills:    mm/min = rpm x mm/rev
The machine is taken as PR 266's: a Haas VF-4 class 3-axis mill (8100 rpm, 25.4 m/min rapids) and a manual or
CNC lathe for the turned pieces.
"""
from __future__ import annotations

IN = 25.4
RAPID_MM_MIN = 25400.0          # VF-4 rapid (as freecad_cam.py's recount)

# T number -> tool. "shape": endmill | drill | chamfer (90 deg spot/countersink) | facemill
TOOLS = {
    1: dict(name="2.5 in. (63.5 mm) indexable face mill, 4 inserts", shape="endmill", d=63.5, flutes=4, rpm=3000,
            ipt=0.004, length=60.0, edge=8.0),
    2: dict(name="1/2 in. (12.7 mm) 3-flute carbide end mill", shape="endmill", d=12.7, flutes=3, rpm=7600,
            ipt=0.003, length=45.0, edge=32.0),
    3: dict(name="1/4 in. (6.35 mm) 3-flute carbide end mill, 1 in. flutes (long reach)", shape="endmill", d=6.35,
            flutes=3, rpm=8100, ipt=0.0015, length=38.0, edge=25.4),
    4: dict(name="1/8 in. (3.175 mm) 2-flute carbide end mill", shape="endmill", d=3.175, flutes=2, rpm=8100,
            ipt=0.0008, length=16.0, edge=9.5),
    5: dict(name="2.0 mm 2-flute carbide end mill (O-ring grooves: Parker's vacuum widths are 2.13-2.26 and "
                 "3.05-3.18 mm)", shape="endmill", d=2.0, flutes=2, rpm=8100, ipt=0.0005, length=10.0, edge=6.0),
    6: dict(name="3/4 in. (19.05 mm) 3-flute carbide end mill", shape="endmill", d=19.05, flutes=3, rpm=5100,
            ipt=0.005, length=66.0, edge=38.1),
    7: dict(name="1/2 in. 90 deg carbide spot drill (spotting, countersinks, chamfers)", shape="chamfer", d=12.7,
            rpm=4000, mm_rev=0.08, length=40.0, angle=90.0),
}
# drills by diameter (carbide jobber unless noted); T numbers 20+
DRILL_D = [1.6, 2.0, 2.05, 2.2, 2.4, 2.5, 3.3, 3.4, 4.2, 4.5, 5.0, 5.5, 6.4, 6.6, 9.6, 10.0, 6.1]   # 6.1: v2 heaters
for _i, _d in enumerate(DRILL_D):
    TOOLS[20 + _i] = dict(name="%.2f mm carbide drill" % _d, shape="drill", d=_d,
                          rpm=min(8100, int(round(60000 / _d / 10.0)) * 10),     # ~60-70 m/min surface speed in 6061
                          mm_rev=round(min(0.15, 0.025 * _d), 3), length=max(30.0, 12 * _d), angle=118.0)


def drill_tool(d):
    """T number of the drill of diameter d (mm)"""
    for t, v in TOOLS.items():
        if v["shape"] == "drill" and abs(v["d"] - d) < 1e-6:
            return t
    raise KeyError("no %.3f mm drill in the library" % d)


def feed_mm_min(t, ipt=None):
    v = TOOLS[t]
    if v["shape"] in ("drill", "chamfer"):
        return v["rpm"] * v["mm_rev"]
    return v["rpm"] * v["flutes"] * (ipt or v["ipt"]) * IN


# --- threads and holes (ISO metric coarse; clearance ISO 273 medium; ISO 4762 / ISO 10642 heads) ------------------
TAP_DRILL = {"M2": 1.6, "M2.5": 2.05, "M3": 2.5, "M4": 3.3, "M5": 4.2, "M6": 5.0}
CLEAR = {"M2": 2.4, "M2.5": 2.9, "M3": 3.4, "M4": 4.5, "M5": 5.5, "M6": 6.6}
CBORE = {"M3": (6.5, 3.4), "M4": (8.0, 4.5), "M5": (9.5, 5.5), "M6": (11.0, 6.6)}   # diameter, depth for SHCS heads
CSK = {"M2": 4.4, "M3": 6.9, "M4": 9.2, "M5": 11.4}                                  # 90 deg countersink diameter
PITCH = {"M2": 0.4, "M2.5": 0.45, "M3": 0.5, "M4": 0.7, "M5": 0.8, "M6": 1.0}

# --- time allowances, from PR 266's hours.py (desktop-lpbf/analysis/machining/hours.py) and robot-shop.md -----------
# CAM = 0.5 h + 0.6 h per setup + 0.015 h per hole (+1 h for a lathe-and-mill part); setups 0.75 h each in a vise,
# 1.25 h for parts over 300 mm; deburr + inspect 0.25 h a part, 1 h for a part with a sealing face. robot-shop.md's
# smaller allowances (0.7 h of CAM a part, 20 min a setup) give the low bound. Tapping, reaming, boring-head and
# lathe times are this folder's estimates (stated where they are used).
ALLOW = dict(cam_base=0.5, cam_per_setup=0.6, cam_per_hole=0.015, cam_lathe=1.0, setup_vise=0.75, setup_large=1.25,
             deburr=0.25, deburr_seal=1.0, low_cam_per_part=0.7, low_setup=20 / 60.0,
             tap_s_per_hole=12.0,       # rigid tap in and out incl. positioning (estimate)
             hand_tap_s_per_hole=90.0,  # tapping by hand in a fixture (estimate)
             ream_s_per_hole=20.0, bore_head_min=10.0, tool_change_s=4.2)
RATE_USD_H = 65.0                     # BYU PML academic rate, as manufacturing-route.md
