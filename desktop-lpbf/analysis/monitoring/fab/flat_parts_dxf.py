"""DXFs of three flat monitoring parts, for instant quotes (issue #260, PR 281), as the model draws them on 2026-11-27:
  * the LW window clamp ring (6061, 1/4 in.): Ø58, ID 31, four M4 clearance holes on Ø50 starting at 60 deg, and the flat
    toward the plate-height through-beam's fibre head (frame_features.json);
  * the BW window clamp frame (6061, 3/16 in.): the rounded rectangle over the seat, trimmed as cad/monitoring_parts._bw trims
    it (the wall's flat face, its bottom edge, 1 mm clear of the inlet plenum's flange: frame_features.bw_clamp_outline), an
    opening 1 mm outside the slot, and the three clamp holes with the third one moved (frame_features.bw_hole3);
  * the LP blanking cap (6061, 1/4 in.): over the lid's face O-ring until the steep camera is bought: the adapter's Ø40.8
    outline with four lugs for the M4 screws where lp_cam.py programs them (Ø48, outside the O-ring groove; the adapter as
    drawn has them inside it). It was a Ø64 disc when LP was at (-60, -80).
SendCutSend priced the 2026-11-25 versions with no account; scs_quote.py re-prices these (quotes/sendcutsend_quotes.csv).
Also writes dxf/flat_parts.json: each outline's size, area and the metal round each hole.

Run: /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/fab/flat_parts_dxf.py   (writes analysis/out/monitoring/fab/dxf/)
"""
import json
import math
import pathlib
import sys

import cadquery as cq
import numpy as np

W = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(W / "cad"))
sys.path.insert(0, str(HERE))
import frame_features as FF  # noqa: E402
import lp_cam  # noqa: E402

ff = json.loads((W / "analysis/out/monitoring/fab/frame_features.json").read_text())
out = W / "analysis/out/monitoring/fab/dxf"
out.mkdir(parents=True, exist_ok=True)
info = {}


def web(face, holes, r_hole):
    """metal between each hole and the outline (2D, mm)"""
    ow, z = face.outerWire(), face.Center().z
    return [round(cq.Vertex.makeVertex(x, y, z).distance(ow) - r_hole, 2) for x, y in holes]


# LW clamp ring: OD, ID, 4 holes on the bolt circle (M4 clearance 4.5); local x = the wall's y, local y = z
cr = ff["LW"]["clamp_ring"]
ring = (cq.Workplane("XY").circle(cr["od"] / 2).circle(cr["id"] / 2).extrude(6.35)
        .faces(">Z").workplane().polarArray(cr["bolt_circle_d"] / 2, cr.get("hole0_deg", 45.0), 360, 4).hole(4.5))
if cr.get("flat"):   # the flat toward the through-beam's fibre head (frame_features.FIBRE_HEAD)
    fl = cr["flat"]
    ang = math.degrees(math.atan2(fl["dir_yz"][1], fl["dir_yz"][0]))
    ring = ring.cut(cq.Workplane("XY").center(fl["dist_mm"] + 20.0, 0).rect(40.0, 80.0).extrude(20).translate((0, 0, -5))
                    .rotate((0, 0, 0), (0, 0, 1), ang))
sec = cq.Workplane("XY").add(ring.val()).section(3.0)
cq.exporters.export(sec, str(out / "lw_clamp_ring.dxf"))
f2 = sec.faces().val()
rh = [(cr["bolt_circle_d"] / 2 * math.cos(math.radians(cr.get("hole0_deg", 45.0) + 90 * k)),
       cr["bolt_circle_d"] / 2 * math.sin(math.radians(cr.get("hole0_deg", 45.0) + 90 * k))) for k in range(4)]
bb = f2.BoundingBox()
info["lw_clamp_ring"] = dict(material="6061-T6 1/4 in. (6.35 mm)", size_mm=[round(bb.xlen, 2), round(bb.ylen, 2)],
                             area_mm2=round(f2.Area(), 1), holes=4, hole_d=4.5, web_to_outline_mm=web(f2, rh, 2.25))

# BW clamp frame in the wall's x-z plane (local x = model x, local y = model z), as monitoring_parts._bw draws it
bw = ff["BW"]
seat, slot = bw["seat"], bw["slot"]
e1, e2 = np.array(slot["end_centres_xz"][0]), np.array(slot["end_centres_xz"][1])
u = (e2 - e1) / np.linalg.norm(e2 - e1)
sc = 0.5 * (e1 + e2) + FF.SEAT_SHIFT * u
outline = FF.bw_clamp_outline(sc, u, seat["L"], seat["W"])
pts = list(outline.exterior.coords)[:-1]
frame = cq.Workplane("XY").polyline([tuple(map(float, p)) for p in pts]).close().extrude(4.76)
half = float(np.linalg.norm(e2 - e1)) / 2
r_open = slot["radius"] + 1.0
mid = 0.5 * (e1 + e2)
frame = frame.cut(cq.Workplane("XY").center(*mid).slot2D(2 * half + 2 * r_open, 2 * r_open, math.degrees(math.atan2(u[1], u[0])))
                  .extrude(10).translate((0, 0, -1)))
for x, z in bw["clamp_frame"]["holes_xz"]:
    frame = frame.cut(cq.Workplane("XY").center(x, z).circle(2.25).extrude(10).translate((0, 0, -1)))
sec = frame.section(2.0)
cq.exporters.export(sec, str(out / "bw_clamp_frame.dxf"))
f2 = sec.faces().val()
bb = f2.BoundingBox()
info["bw_clamp_frame"] = dict(material="6061-T6 3/16 in. (4.76 mm)", size_mm=[round(bb.xlen, 2), round(bb.ylen, 2)],
                              area_mm2=round(f2.Area(), 1), holes=3, hole_d=4.5,
                              web_to_outline_mm=web(f2, bw["clamp_frame"]["holes_xz"], 2.25),
                              note="outline polygonised from frame_features.bw_clamp_outline (R6 corners as 32-segment arcs)")

# LP blanking cap: the adapter's Ø40.8 disc and four R5.5 lugs round the screw holes (lp_cam.LP_BOLT), in the lid's x-y
L = lp_cam.lp()
c, r_a = L["c"], L["r_a"]
lug = lp_cam.LP_BOLT["lug_r"]
cap = cq.Workplane("XY").circle(r_a).extrude(6.35)
for x, y in L["holes"]:
    cap = cap.union(cq.Workplane("XY").center(x - c[0], y - c[1]).circle(lug).extrude(6.35))
try:   # round the eight inside corners where the lugs meet the disc
    cap = cap.edges("|Z").edges(cq.selectors.BoxSelector((-40, -40, -1), (40, 40, 8))).fillet(1.5)
except Exception as e:  # noqa: BLE001
    print("cap fillet skipped:", type(e).__name__, str(e)[:100])
for x, y in L["holes"]:
    cap = cap.cut(cq.Workplane("XY").center(x - c[0], y - c[1]).circle(2.25).extrude(10).translate((0, 0, -1)))
sec = cq.Workplane("XY").add(cap.val()).section(3.0)
cq.exporters.export(sec, str(out / "lp_blank_cap.dxf"))
f2 = sec.faces().val()
bb = f2.BoundingBox()
lh = [(x - c[0], y - c[1]) for x, y in L["holes"]]
info["lp_blank_cap"] = dict(material="6061-T6 1/4 in. (6.35 mm)", size_mm=[round(bb.xlen, 2), round(bb.ylen, 2)],
                            area_mm2=round(f2.Area(), 1), holes=4, hole_d=4.5, bolt_circle_d=2 * lp_cam.LP_BOLT["r"],
                            web_to_outline_mm=web(f2, lh, 2.25), disc_d=round(2 * r_a, 2), lug_r=lug)
(out / "flat_parts.json").write_text(json.dumps(info, indent=1))
print(json.dumps(info, indent=1))
for f in sorted(out.glob("*.dxf")):
    print(f, f.stat().st_size)
