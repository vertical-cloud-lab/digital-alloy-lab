"""DXFs of three flat monitoring parts, from frame_features.json, for instant quotes (issue #260, PR 281):
  * the LW window clamp ring (6061, 1/4 in.): OD, ID and four M4 clearance holes on its bolt circle;
  * the BW window clamp frame (6061, 3/16 in.): a rounded rectangle over the seat, an opening 1 mm outside the slot, and the
    three clamp holes. Its outline is a stand-in for pricing: it runs close to the frame's bottom edge and needs fitting;
  * the LP blanking cap (6061, 1/4 in.): the LP adapter's outline and four holes, over the lid's face O-ring until the camera
    comes (Ø64 with four holes on Ø56 when LP was at (-60, -80); the SendCutSend quote below is for that disc).
SendCutSend priced all three on 2026-11-25 with no account (analysis/out/monitoring/fab/quotes/sendcutsend_quotes.csv).

Run: /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/fab/flat_parts_dxf.py   (writes analysis/out/monitoring/fab/dxf/)
"""
import json
import math
import pathlib

import cadquery as cq

W = pathlib.Path(__file__).resolve().parents[3]
ff = json.loads((W / "analysis/out/monitoring/fab/frame_features.json").read_text())
out = W / "analysis/out/monitoring/fab/dxf"
out.mkdir(parents=True, exist_ok=True)

# LW clamp ring: OD, ID, 4 holes on the bolt circle (M4 clearance 4.5)
cr = ff["LW"]["clamp_ring"]
ring = (cq.Workplane("XY").circle(cr["od"] / 2).circle(cr["id"] / 2).extrude(6.35)
        .faces(">Z").workplane().polarArray(cr["bolt_circle_d"] / 2, cr.get("hole0_deg", 45.0), 360, 4).hole(4.5))
if cr.get("flat"):   # the flat toward the through-beam's fibre head (frame_features.FIBRE_HEAD): local x = the wall's y, local y = z
    fl = cr["flat"]
    ang = math.degrees(math.atan2(fl["dir_yz"][1], fl["dir_yz"][0]))
    ring = ring.cut(cq.Workplane("XY").center(fl["dist_mm"] + 20.0, 0).rect(40.0, 80.0).extrude(20).translate((0, 0, -5))
                    .rotate((0, 0, 0), (0, 0, 1), ang))
cq.exporters.export(cq.Workplane("XY").add(ring.val()).section(3.0), str(out / "lw_clamp_ring.dxf"))

# BW clamp frame: rounded rectangle over the seat (+18 x +22 mm), opening = slot + 1 mm, 3 clearance holes (x-z of the wall)
bw = ff["BW"]
seat = bw["seat"]
slot = bw["slot"]
e1, e2 = slot["end_centres_xz"]
ang = math.radians(slot["long_axis_deg_from_x"])
u = (math.cos(ang), math.sin(ang))
mid = ((e1[0] + e2[0]) / 2 + 1.0 * u[0], (e1[1] + e2[1]) / 2 + 1.0 * u[1])   # the seat's centre (frame_features SEAT_SHIFT 1 mm)
L, H = seat["L"] + 18.0, seat["W"] + 22.0
frame = cq.Workplane("XY").rect(L, H).extrude(4.76).edges("|Z").fillet(6.0)
half = math.dist(e1, e2) / 2
r_open = slot["radius"] + 1.0
frame = frame.cut(cq.Workplane("XY").slot2D(2 * half + 2 * r_open, 2 * r_open, 0).extrude(10).translate((-1.0, 0, -1)))
for x, z in bw["clamp_frame"]["holes_xz"]:
    dx, dz = x - mid[0], z - mid[1]
    lx = dx * u[0] + dz * u[1]
    lz = -dx * u[1] + dz * u[0]
    frame = frame.cut(cq.Workplane("XY").center(lx, lz).circle(2.25).extrude(10).translate((0, 0, -1)))
cq.exporters.export(frame.section(2.0), str(out / "bw_clamp_frame.dxf"))

# LP blanking cap: until the steep camera is bought, a disc in the adapter boss's place: the adapter's outline and its four
# holes, over the lid's face O-ring round the Ø24 bore on the line of sight (cad/monitoring_parts.py; LP at monitoring_spec's
# centre, moved to (-40, 60) on 2026-11-25; it was a Ø64 disc with 4 holes on Ø56 over a Ø37 bore at (-60, -80))
import sys  # noqa: E402
sys.path.insert(0, str(W / "cad"))
import monitoring_parts as MPT  # noqa: E402
g = MPT.lp_geometry()
r_a = g["on_axis"]["r_adapter"]
c = g["c"]
cap = cq.Workplane("XY").circle(r_a).extrude(6.35)
for x, y in MPT.lp_adapter_holes(c, r_a):
    cap = cap.cut(cq.Workplane("XY").center(x - c[0], y - c[1]).circle(2.25).extrude(10).translate((0, 0, -1)))
cq.exporters.export(cq.Workplane("XY").add(cap.val()).section(3.0), str(out / "lp_blank_cap.dxf"))
for f in sorted(out.glob("*.dxf")):
    print(f, f.stat().st_size)
