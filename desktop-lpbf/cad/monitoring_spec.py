"""Shared geometry for the in-situ monitoring hardware (issue #260, PR 281; builds on monitoring.md).

One place for where each port, window and instrument goes, so the model (cad/monitoring_parts.py), the machining
(analysis/monitoring/fab), the gas-flow and spatter models (analysis/monitoring/plume), the optics (analysis/monitoring/optics)
and the mechanics (analysis/monitoring/mech) all use the same numbers. Read it at run time; don't copy numbers out of it.

Coordinates are the model's (mm): plate centre at the origin, powder surface z = 0, +x toward the blade's park/end side, +y toward
the back wall (inlet plenum), +z up. Chamber inside x +/-140, y +/-95, z 0..120; walls 16 mm (outer faces x +/-156, y +/-111);
lid z 120..136; optics bridge z 211.1..236.1; the coaxial beam line at y -25.25, z 271.1.

Starting values come from monitoring.md §3 (453 candidate windows checked against the model, 2026-11-25) and optics.md §9.2.
Where a value is marked "to check", cad/monitoring_parts.py may move it after checking it on the model; it then edits this file
and says why in the comment.
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------------------------------------------------------- the target
PLATE_R = {"S25": 25.2 / 2, "M50": 50.5 / 2, "L75": 75.8 / 2}     # plate radii (module_params.MODULES)
TARGET = (0.0, 0.0, 0.0)                                           # every viewport bore is drilled on its line to the plate centre


def axis_to_target(p, target=TARGET):
    """Unit vector from a port centre p toward the target (the viewing direction, into the chamber)."""
    d = [t - q for t, q in zip(target, p)]
    n = math.sqrt(sum(c * c for c in d))
    return tuple(c / n for c in d)


def elevation_deg(p, target=TARGET):
    dx, dy, dz = (q - t for q, t in zip(p, target))
    return math.degrees(math.atan2(dz, math.hypot(dx, dy)))


# ---------------------------------------------------------------------------------------------------------------- viewports
# Each viewport: a bore through the wall (or lid) on its line of sight to the plate centre, a fused-silica window on an FKM
# O-ring seat on the OUTSIDE face (atmosphere pushes it onto its seal at vacuum; a clamp ring holds it at +20 mbar), a sacrificial
# cover slide on the inside where spatter and condensate land, and a hole in the liner the bore passes through.
#   centre      : where the bore's axis meets the outer face (mm)
#   clear_d     : clear aperture the optics need through the whole bore (mm)
#   window      : outside window, diameter x thickness (mm) and material
#   slide       : inside cover slide, diameter x thickness (mm)
#   purge       : argon purge across the slide (from the argon line through a needle valve), or None
#   blank       : ships with a blanking plate in place of the window until the instrument is bought
VIEWPORTS = {
    "LW": dict(
        what="left-wall side viewport: high-speed camera for spatter, plume, denudation and the powder heap (monitoring.md §3, step 7)",
        face="-x", centre=(-156.0, -20.0, 36.0),          # monitoring.md's best left-wall view was (-156, -20, 40); z 36 keeps a Ø40
        clear_d=25.0,                                     # centre clear (clear to z 35) - to check on the model
        window=dict(d=38.1, t=5.0, mat="UV fused silica, AR 650-1050 nm"), slide=dict(d=30.0, t=1.0), purge=True, blank=True,
    ),
    "BW": dict(
        what="back-wall light window: raking light for the layer camera, 8-13 deg (optics.md §9.2 option D)",
        face="+y", centre=(-125.0, 111.0, 25.0),          # optics.md used x -105; the recoater sensor posts stand outside at x -110
        clear_d=20.0,                                     # (monitoring.md §3), so start at -125 - to check on the model
        window=dict(d=25.4, t=3.0, mat="N-BK7 or UV fused silica, AR visible"), slide=None, purge=False, blank=False,
    ),
    "LP": dict(
        what="steep lid port: compact camera at ~54-62 deg for a second, steep view (monitoring.md §3); needs a cut-out in the bridge",
        face="+z", centre=(-60.0, -80.0, 136.0),          # 53.6 deg; its camera line crosses the bridge near (-93, -124) - inside the
        clear_d=20.0,                                     # reservoir slot (x -118..-62), so it may block the reservoir's way out.
        window=dict(d=25.4, t=3.0, mat="UV fused silica"), slide=dict(d=25.0, t=1.0), purge=False, blank=True,
        candidates=[(-60.0, -80.0, 136.0), (-40.0, 60.0, 136.0), (-20.0, 80.0, 136.0), (80.0, 80.0, 136.0)],   # monitoring.md §3 lid rows
    ),
}

# ---------------------------------------------------------------------------------------------------------------- instruments
SIDE_CAMERA = dict(
    port="LW", body="Kron Chronos 2.1-HD", body_mm=(155.0, 96.0, 67.3), mass_kg=1.0,     # mass to check (Kron datasheet)
    lens_options=["50 mm f/2.8-4 C-mount", "75 mm f/4 C-mount"], standoff_mm=15.0,       # lens front 15 mm off the window adapter
    room_note="monitoring.md §3: behind a 60 mm lens a Ø120 body has 180 mm before the guard panel (140 mm behind a 100 mm lens)",
)
LID_CAMERA = dict(port="LP", body="monochrome IMX296 global-shutter board in a housing", lens="50 mm C-mount", body_mm=(40.0, 40.0, 30.0))

# Coaxial branch (monitoring.md §0 item 3): the existing DMSP1000 cube stays where it is; the SM1 photodiode tube behind it becomes
# a 30 mm cage with two more cubes. Free room above the bridge (monitoring.md fits.json): x -230..-170, y -200..-62 (front branch),
# x -400..-254, y -60..10 (along -x), x -420..-200, y -170..-70, z 244..335 (front-left arm for a folded Chronos).
COAX = dict(
    beam_y=-25.25, beam_z=271.11,
    cube1=dict(x=-155.0, what="existing DMSP1000 (reflects 1070 nm into the galvo, passes 520-985 nm)"),
    cube2=dict(x=-215.0, out="-y", what="splitter to the coaxial camera branch (toward the front)"),
    cube3=dict(x=-285.0, out="-x and one side", what="splitter between the two pyrometer photodiodes (two-colour pair)"),
    camera_branch=dict(dir="-y", y_end=-200.0, what="tube lens + monochrome camera, ~8 um/px at the plate (f_tube = 160 x px/8)"),
    cage="Thorlabs 30 mm cage (ER rods, C4W/CM1 cubes, CP33 plates, SM1 lens tubes)",
)

AE = dict(
    options=["drawbar as the waveguide: sensor at its cold end, if the drawbar is drawn and runs down the rod",
             "Ø3 mm 316 waveguide, spring-loaded tip on the plate's underside, down the hollow rod to a room-temperature sensor",
             "sensor on the rod end (<= ~75 C)"],
    sensor_room_temp="broadband AE sensor (e.g. MISTRAS WSa / Vallen VS900-M class) + 2/4/6 preamp, at <= 60 C",
)

DAQ = dict(
    digitizer="PicoScope 4444 (4 differential channels, 14-bit, 20 MHz) or a 2 MS/s DAQ for AE",
    where="the 4U DIN drawer in the rack, or the Pi box on the bridge (electrical.md §13)",
    signals=["coaxial photodiode 1", "coaxial photodiode 2", "AE (preamp out)", "laser gate", "RTC6 layer-start / sync"],
)


def summary():
    out = {}
    for k, v in VIEWPORTS.items():
        out[k] = dict(centre=v["centre"], axis=tuple(round(c, 4) for c in axis_to_target(v["centre"])),
                      elevation_deg=round(elevation_deg(v["centre"]), 1),
                      to_plate_centre_mm=round(math.dist(v["centre"], TARGET), 1), clear_d=v["clear_d"])
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(summary(), indent=1))
