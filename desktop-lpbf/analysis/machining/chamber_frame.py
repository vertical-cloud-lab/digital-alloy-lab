"""The chamber body as drawn before (one block with a 120 mm deep pocket) against the through-frame + floor plate
(chamber-construction.md): stock, chips, the reach and length-to-diameter every feature needs, and how far each tool bends.

Deflection: an end mill as a cantilever, delta = F L^3 / (3 E I), with I = pi D_e^4 / 64 and D_e = 0.8 D (Mitsubishi Materials
models an end mill as a solid rod of 0.7-0.8 D; 0.7 D bends 1.7x more), E = 600 GPa (WC-Co), per 100 N of radial load, which is
about what a full-height finishing pass in 6061 puts on a 3/4 in. tool (0.25 mm radial, 0.05 mm/tooth, ~60 mm of flute
engaged, K_c ~ 700 N/mm2: ~240 N tangential, ~0.4 of that radial). The holder and spindle add to it; this is the tool alone.
Volumes come from cam_sim.json (voxel stock-removal runs) where it has them.

Run:  /tmp/venv/bin/python desktop-lpbf/analysis/machining/chamber_frame.py   (reads analysis/out/machining/cam_sim.json; < 1 s)
Writes desktop-lpbf/analysis/out/machining/chamber_frame.json.
"""
from __future__ import annotations

import json
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[3] / "desktop-lpbf" / "analysis" / "out" / "machining"
IN = 25.4
E_WC = 600e3      # MPa
F = 100.0         # N


def bend(d, L, k=0.8):
    I = math.pi * (k * d) ** 4 / 64
    return F * L ** 3 / (3 * E_WC * I)


def tool(name, d, L, why):
    return dict(tool=name, d_mm=round(d, 3), stick_out_mm=L, L_over_D=round(L / d, 1), deflection_um_per_100N=round(1000 * bend(d, L), 1),
                deflection_um_per_100N_at_0p7D=round(1000 * bend(d, L, 0.7), 1), N_for_25um=round(25e-3 / bend(d, L) * F), why=why)


def main():
    cam = json.loads((OUT / "cam_sim.json").read_text())["detailed"]
    fr = cam["process_chamber_body"]
    fp = cam["chamber_floor_plate"]
    old = dict(
        design="one 6061-T6 block, 13 x 9.5 x 6 in., 280 x 190 x 120 mm pocket, R5 vertical corners, R5 floor coves, 16 mm walls, 20 mm floor",
        stock_L=round(13 * 9.5 * 6 * IN ** 3 / 1e6, 2), part_L=2.73, chips_L=9.42, chips_pct=78,
        residual_cm3=dict(standard_tools=29.1, plus_6in_long_tools=3.4, with_5in_tools_found_for_sale=15.3, plus_32mm_extension_holder=0.9),
        source="machining.md (cam_sim.json and chamber_reach.json before the redesign, 2026-11-20)",
        features=[
            dict(feature="pocket walls, 120 mm deep", reach_mm=123, tool=tool("3/4 in. x 6 in. OAL", 0.75 * IN, 112, "walls to the floor")),
            dict(feature="R5 vertical corners, 120 mm tall", reach_mm=125, tool=tool("3/8 in. at 125 mm (extension or 6 in. long)", 0.375 * IN, 125, "R5 needs a tool under Ø10")),
            dict(feature="R5 floor coves", reach_mm=125, tool=tool("3/8 in. ball, 125 mm", 0.375 * IN, 125, "a cove needs a ball or corner-radius tool at full depth")),
            dict(feature="pocket floor (20 mm floor, flat over the blade path)", reach_mm=123, tool=tool("1 in. x 6 in. OAL", IN, 108, "floor and lower walls")),
            dict(feature="recoater-rail insert holes in the back wall's inside face", reach_mm=206 + 10, tool=tool("Ø4.2 drill + M4 STI tap through the door opening", 4.22, 216,
                                                                                                                  "16 mm front wall + 190 mm interior")),
        ])
    new = dict(
        design="through-frame from 5-1/2 in. plate (walls 16 mm, 123.9 mm tall, R10 corners, 8 x 3.9 rebate) + 20 mm floor plate",
        frame=dict(milled_stock_L=round(fr["std"]["stock_mm3"] / 1e6, 2), part_L=round(fr["std"]["part_mm3"] / 1e6, 2), chips_L=round(fr["std"]["removed_mm3"] / 1e6, 2),
                   core_slug_L=round(274 * 184 * 5.5 * IN / 1e6 - (4 - math.pi) * 49 * 5.5 * IN / 1e6, 2), residual_cm3=dict(standard_tools=round(fr["std"]["residual_mm3"] / 1000, 2),
                                                                                                                         plus_long_tools=round(fr["std+long"]["residual_mm3"] / 1000, 2)),
                   residual_note="what is left is voxel slivers at the R10 corners (the 3/4 in. tool's R9.5 fits) and Ø3-4 holes the voxels can't resolve; all are cut"),
        floor=dict(milled_stock_L=round(fp["std"]["stock_mm3"] / 1e6, 2), part_L=round(fp["std"]["part_mm3"] / 1e6, 2), chips_L=round(fp["std"]["removed_mm3"] / 1e6, 2),
                   residual_cm3=round(fp["std"]["residual_mm3"] / 1000, 2)),
        features=[
            dict(feature="opening walls, finished from the top and from the bottom, 62 mm each", reach_mm=62, tool=tool("3/4 in. x 4 in. OAL (standard)", 0.75 * IN, 63, "R10 corners")),
            dict(feature="outer profile, from both sides", reach_mm=62, tool=tool("3/4 in. x 4 in. OAL (standard)", 0.75 * IN, 63, "")),
            dict(feature="rebate 8 x 3.9 (bottom)", reach_mm=4, tool=tool("3/4 in. x 4 in. OAL", 0.75 * IN, 63, "same tool")),
            dict(feature="door opening through the 16 mm front wall, R6.5", reach_mm=16, tool=tool("1/2 in. x 3 in. OAL", 0.5 * IN, 38, "")),
            dict(feature="inlet slot 120 x 8 through 16 mm, round ends", reach_mm=16, tool=tool("1/4 in. 3-flute", 0.25 * IN, 25, "")),
            dict(feature="lid and floor O-ring glands 4.6 x 2.65", reach_mm=2.65, tool=tool("4 mm 2-flute", 4.0, 16, "")),
            dict(feature="rail holes: M4 tapped through the back wall from outside", reach_mm=16, tool=tool("Ø3.3 drill / M4 tap", 3.3, 30, "no inside-face holes left")),
            dict(feature="floor plate: pad step, port Ø96, slots, notches (20 mm plate)", reach_mm=20, tool=tool("3/4 in. x 4 in. OAL", 0.75 * IN, 63, "")),
        ])
    r = dict(old=old, new=new, chips_saved_L=round(old["chips_L"] - new["frame"]["chips_L"] - new["floor"]["chips_L"], 2),
             method=__doc__.split("\n\n")[1].replace("\n", " "))
    (OUT / "chamber_frame.json").write_text(json.dumps(r, indent=1))
    for k in ("old", "new"):
        for f in r[k]["features"]:
            t = f["tool"]
            print(f"{k:3s} {f['feature'][:60]:60s} {t['tool'][:34]:34s} L/D {t['L_over_D']:5.1f}  {t['deflection_um_per_100N']:7.1f} um/100 N")
    print(json.dumps({k: v for k, v in r["new"].items() if k in ("frame", "floor")}, indent=0), r["chips_saved_L"])


if __name__ == "__main__":
    main()
