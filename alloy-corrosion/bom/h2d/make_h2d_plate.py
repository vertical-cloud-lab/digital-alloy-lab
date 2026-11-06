#!/usr/bin/env python3
"""One Bambu Lab H2D plate, in PLA, holding every printed part of the CubXL corrosion setup that the lab
doesn't already have.

Ben asked on #180 (2026-11-06) for all the parts at once on the H2D, leaving out what the lab already
has: the vial caps (P13), a tip rack (P11), the stir modules and a vial rack (P14). This script lays
the rest out on one H2D plate and checks the layout:
- every part is inside the area both nozzles reach, with a margin, and clear of the H2D's
  nozzle-wrap detection zone;
- the parts are a gap apart;
- the magnet pockets close exactly at each pause height.
It draws plate.png and writes plate.json. Given an unpacked Bambu Studio, it also writes the plate as
a Bambu Studio project (.3mf) and as sliced G-code (.gcode.3mf), with 100 % infill on the parts the
BOM asks it for, scarf seams on the lids and caps, and two pauses for the magnets. It then reads the
G-code back to check the pauses, the pockets and where the extrusions land.

The parts, their print orientations and infill, and the mesh and G-code helpers come from
../a1-mini/make_plates.py, so the two plate sets print the same parts the same way.

    python make_h2d_plate.py
    python make_h2d_plate.py --bambu /tmp/bambu/squashfs-root

--bambu  an unpacked Bambu Studio Linux AppImage (`--appimage-extract`); tested with 02.09.01.70.

Needs trimesh (with scipy and networkx), shapely, matplotlib and numpy.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np
from shapely.geometry import MultiPoint, box

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "a1-mini"))
import make_plates as a1  # noqa: E402  (PARTS, part_mesh, pause_layer, pocket and G-code helpers)

PARTS = a1.PARTS

# The H2D, from Bambu Studio's "Bambu Lab H2D 0.4 nozzle" profile (checked against it when --bambu is given).
BED_X, BED_Y, BED_Z = 350.0, 320.0, 325.0  # printable_area, printable_height
REACH = {"left": (0.0, 325.0), "right": (25.0, 350.0)}  # extruder_printable_area, x range of each nozzle
BOTH_X = (25.0, 325.0)  # where both nozzles reach: the layout stays in here, so either nozzle can print it
WRAP_ZONE = (145.0, 310.0, 256.0, 326.0)  # wrapping_exclude_area (x0, y0, x1, y1): kept clear
MARGIN = 5.0  # keep parts this far inside BOTH_X, the bed's front and back, and the wrap zone
GAP = 5.0  # minimum gap between parts

MACHINE = "Bambu Lab H2D 0.4 nozzle"
PROCESS = "0.20mm Standard @BBL H2D"
FILAMENT = "Bambu PLA Basic @BBL H2D"
MACHINE_MODEL = "Bambu Lab H2D"  # its model_id goes into slice_info (the command-line slicer leaves it blank)
# The command-line slicer doesn't know how many nozzles each H2D extruder holds, and stops with "No valid
# nozzle found" unless told: one standard nozzle on each side.
NOZZLES = ["--extruder-nozzle-count", "1,1", "--extruder-nozzle-volume-type", "Standard,Standard"]
NOZZLE_SIDE = {1: "left", 2: "right"}  # filament_map values: the extruder that prints filament 1
PRINT_WITH = 2  # the right nozzle, the H2D's main one (master_extruder_id); the left is checked too

LID_KEYS = ("lid_006", "lid_008", "lid_010")

# What isn't on the plate, and why (BOM IDs from ../README.md §1).
NOT_PRINTED = [
    ("P11", "Tip rack 2 x 15", "the lab has a tip rack"),
    ("P12 (tip)", "Fit strip for the tip rack's holes", "it only sizes P11's holes"),
    ("P13", "Magnetic vial caps (8)", "the lab has vial caps"),
    ("P14", "9-position vial holder", "the lab has a vial rack"),
    ("P18", "Fallback electrode cap with an O-ring", "the BOM's quantity is 0"),
    ("stirrers", "Stir-module prints (../../stirrers/BOM.md §3)", "the lab has the stir modules"),
]

# (part, x, y, z-rotation in degrees), with x, y the centre of the part's footprint on the bed.
# Front row: the seven lids, which get magnets at the first pause. Behind them the cup block, which
# gets magnets at the second pause, so it is in front of the tall bench cell body.
ITEMS = [
    # row 1, y 20-55: lids; the 008 and 010 calibration lids at the right end
    ("lid_006", 73, 37.5, 0), ("lid_006", 107, 37.5, 0), ("lid_006", 141, 37.5, 0),
    ("lid_006", 175, 37.5, 0), ("lid_006", 209, 37.5, 0), ("lid_008", 243, 37.5, 0), ("lid_010", 277, 37.5, 0),
    # row 2, y 65-109: cup block, tube rack, tip waste cup
    ("cup_block", 95, 79, 0), ("tube_rack", 199, 82, 0), ("tip_waste", 279, 87, 0),
    # row 3, y 119-159: coupon tray, the two electrode caps, the three carriers
    ("tray", 101.5, 139, 0), ("cap", 178, 139, 0), ("cap", 216, 139, 0),
    ("carrier", 244, 139, 0), ("carrier", 258, 139, 0), ("carrier", 272, 139, 0),
    # row 4, y 169-239: bench cell body, cover and clamp plate
    ("cell_body", 82, 204, 0), ("cell_cover", 160, 204, 0), ("cell_clamp", 228, 204, 0),
    # row 5, y 249-296: shims (1 mm in front, 3 mm behind) and the tube rack's fit strip
    ("shim_1", 71.2, 259.2, 0), ("shim_1", 97.6, 259.2, 0), ("shim_1", 124, 259.2, 0), ("shim_1", 150.4, 259.2, 0),
    ("shim_3", 71.2, 285.6, 0), ("shim_3", 97.6, 285.6, 0), ("shim_3", 124, 285.6, 0), ("shim_3", 150.4, 285.6, 0),
    ("strip_tube", 213, 272.4, 0),
]

# Pauses: (height of the pocket tops, parts whose pockets close there, what to insert).
PAUSES = [
    (5.6, LID_KEYS, "fourteen 4 x 2 mm magnets, two per lid, same pole up"),
    (44.6, ("cup_block",), "six 4 x 2 mm magnets in the cup block, same pole up as the lids"),
]

PLATE_NAME = "Corrosion setup, all parts"  # plate name in Bambu Studio (no colons: it drops those)


def placed():
    out, count = [], {}
    for key, x, y, rot in ITEMS:
        m = a1.part_mesh(key, None)
        if rot:
            m.apply_transform(a1.trimesh.transformations.rotation_matrix(math.radians(rot), [0, 0, 1]))
        m.apply_translation([x, y, 0])
        count[key] = count.get(key, 0) + 1
        out.append({"key": key, "name": f"{PARTS[key][0]}_{key}_{count[key]}", "x": x, "y": y, "rot": rot, "mesh": m})
    return out


def check(items):
    """Inside the reach of both nozzles, clear of the wrap zone, a gap apart; pockets close at each pause."""
    area = box(BOTH_X[0] + MARGIN, MARGIN, BOTH_X[1] - MARGIN, BED_Y - MARGIN)
    wrap = box(*WRAP_ZONE)
    hulls = []
    for it in items:
        m = it["mesh"]
        hull = MultiPoint(m.vertices[:, :2]).convex_hull
        it["footprint_mm"] = [round(float(v), 2) for v in (m.extents[0], m.extents[1])]
        it["height_mm"] = round(float(m.extents[2]), 2)
        assert area.contains(hull), f"{it['name']} is closer than {MARGIN} mm to the edge of where both nozzles reach"
        assert hull.distance(wrap) >= MARGIN, f"{it['name']} is closer than {MARGIN} mm to the wrap detection zone"
        assert m.bounds[1][2] <= BED_Z, f"{it['name']} is taller than the H2D's {BED_Z} mm"
        hulls.append((it["name"], hull))
    gaps = []
    for i in range(len(hulls)):
        for j in range(i + 1, len(hulls)):
            d = hulls[i][1].distance(hulls[j][1])
            gaps.append((d, hulls[i][0], hulls[j][0]))
            assert d >= GAP - 1e-6, f"{hulls[i][0]} and {hulls[j][0]} are {d:.1f} mm apart"
    union = MultiPoint(np.vstack([it["mesh"].vertices[:, :2] for it in items])).bounds
    res = {"min_gap_mm": round(min(gaps)[0], 1), "closest_pair": list(min(gaps)[1:]),
           "layout_extent_mm": [round(v, 1) for v in union],
           "footprint_area_cm2": round(sum(h.area for _, h in hulls) / 100, 1),
           "pauses": [], "pockets": []}
    for h, keys, what in PAUSES:
        z = a1.pause_layer(h)
        n = 0
        for it in items:
            if it["key"] not in keys:
                continue
            below, above = a1.holes_at(it["mesh"], h - 0.1), a1.holes_at(it["mesh"], h + 0.1)
            assert below > above, f"{it['name']}: no pocket closes at z {h}"
            # Pocket centres: solid just above the pocket tops, empty just below.
            new = a1.section_xy(it["mesh"], h + 0.1).difference(a1.section_xy(it["mesh"], h - 0.1))
            for g in getattr(new, "geoms", [new]):
                if g.area > 1.0:
                    res["pockets"].append((h, it["name"], g.centroid.x, g.centroid.y))
                    n += 1
        res["pauses"].append({"pocket_top_z": h, "pause_before_layer_z": z, "parts": list(keys),
                              "pockets": n, "insert": what})
    return res


def part_rows(items):
    rows = {}
    for it in items:
        bom, what, _, _, infill, note = PARTS[it["key"]]
        r = rows.setdefault(it["key"], {"bom": bom, "part": what, "qty": 0, "infill": infill or "15% (profile)",
                                         "on_the_bed": note, "volume_cm3": 0.0})
        r["qty"] += 1
        r["volume_cm3"] += it["mesh"].volume / 1000
    for r in rows.values():
        r["volume_cm3"] = round(r["volume_cm3"], 2)
    return list(rows.values())


# ---------------------------------------------------------------- drawing

def draw(items, res, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MplPolygon, Rectangle
    from trimesh.path.polygons import projected

    magnet_keys = {k for _, keys, _ in PAUSES for k in keys}
    fig, ax = plt.subplots(figsize=(12.5, 9.6))
    ax.add_patch(Rectangle((0, 0), BED_X, BED_Y, facecolor="#f4f4f2", edgecolor="#555", lw=1.2))
    for x0, x1 in ((0, BOTH_X[0]), (BOTH_X[1], BED_X)):
        ax.add_patch(Rectangle((x0, 0), x1 - x0, BED_Y, facecolor="#e2e2de", edgecolor="none", hatch="///",
                               alpha=0.8))
    ax.add_patch(Rectangle((BOTH_X[0] + MARGIN, MARGIN), BOTH_X[1] - BOTH_X[0] - 2 * MARGIN, BED_Y - 2 * MARGIN,
                           fill=False, edgecolor="#bbb", lw=0.8, ls="--"))
    wx0, wy0, wx1, wy1 = WRAP_ZONE
    ax.add_patch(Rectangle((wx0, wy0), wx1 - wx0, min(wy1, BED_Y) - wy0, facecolor="#e9c7c7", edgecolor="#a55", lw=0.8))
    ax.text((wx0 + wx1) / 2, (wy0 + BED_Y) / 2, "wrap detection zone", ha="center", va="center", fontsize=7, color="#733")
    ax.text(BOTH_X[0] / 2, BED_Y / 2, "left nozzle only", rotation=90, ha="center", va="center", fontsize=8, color="#555")
    ax.text((BOTH_X[1] + BED_X) / 2, BED_Y / 2, "right nozzle only", rotation=90, ha="center", va="center", fontsize=8,
            color="#555")
    for it in items:
        solid = PARTS[it["key"]][4] == "100%"
        outline = projected(it["mesh"], normal=[0, 0, 1], ignore_sign=True, rpad=1e-4, apad=1e-4)
        for g in getattr(outline, "geoms", [outline]):
            mag = it["key"] in magnet_keys
            ax.add_patch(MplPolygon(np.asarray(g.exterior.coords), closed=True,
                                    facecolor="#d9824b" if solid else "#7fa7c9",
                                    edgecolor="#7a1010" if mag else "#333", lw=1.8 if mag else 0.6))
            for hole in g.interiors:
                ax.add_patch(MplPolygon(np.asarray(hole.coords), closed=True, facecolor="#f4f4f2",
                                        edgecolor="#333", lw=0.4))
        label = PARTS[it["key"]][0]
        if it["key"] in ("lid_008", "lid_010"):
            label += "\n" + it["key"][-3:]
        if it["key"] != "carrier":
            ax.text(it["x"], it["y"], label, ha="center", va="center", fontsize=7.5, color="black",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))
    car = [it for it in items if it["key"] == "carrier"]
    ax.annotate("P02 x3", xy=(car[-1]["x"] + 4, car[-1]["y"]), xytext=(car[-1]["x"] + 14, car[-1]["y"] - 14),
                fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=0.6, color="#333"))
    s = res.get("slice")
    sub = f"{len(items)} pieces in PLA"
    if s:
        sub += f", {s['time_h']:.1f} h, {s['filament_g']:.0f} g"
    sub += "; magnet pauses before z " + " and ".join(f"{p['pause_before_layer_z']:g}" for p in res["pauses"])
    ax.set_title("CubXL corrosion setup: every part still to print, on one Bambu Lab H2D plate\n" + sub,
                 fontsize=11, loc="left")
    ax.set_xlim(-4, BED_X + 4)
    ax.set_ylim(-4, BED_Y + 4)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(0, BED_X + 1, 50))
    ax.set_yticks(np.arange(0, BED_Y + 1, 40))
    ax.tick_params(labelsize=7)
    ax.set_xlabel("x (mm); front of the printer at y = 0", fontsize=8)
    handles = [Rectangle((0, 0), 1, 1, facecolor="#d9824b", edgecolor="#333"),
               Rectangle((0, 0), 1, 1, facecolor="#7fa7c9", edgecolor="#333"),
               Rectangle((0, 0), 1, 1, facecolor="white", edgecolor="#7a1010", lw=1.8)]
    ax.legend(handles, ["100 % infill", "profile infill (15 %)", "magnets go in at a pause"],
              loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8, frameon=False)
    ax.text(1.02, 0.80, "H2D bed 350 x 320 mm, seen from above.\n"
            "Hatched: reached by one nozzle only.\nDashed: 5 mm inside where both reach.\n"
            "Labels are BOM IDs.\n\n"
            "Bambu PLA Basic profile, 0.20 mm layers,\n0.4 mm nozzle, textured PEI plate.\n"
            "Times and grams are Bambu Studio's\nestimates.",
            transform=ax.transAxes, va="top", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=110, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


# ---------------------------------------------------------------- Bambu Studio

def profiles(bambu: Path):
    bbl = bambu / "resources" / "profiles" / "BBL"
    index = json.loads((bbl.parent / "BBL.json").read_text())
    files = {it["name"]: bbl / it["sub_path"]
             for k in ("machine_model_list", "machine_list", "process_list", "filament_list") for it in index.get(k, [])}

    def flat(name):
        d = json.loads(files[name].read_text())
        out = flat(d["inherits"]) if d.get("inherits") else {}
        for inc in d.get("include", []) or []:
            out.update({k: v for k, v in flat(inc).items()
                        if k not in ("name", "instantiation", "type", "from", "setting_id", "inherits")})
        out.update({k: v for k, v in d.items() if k != "include"})
        return out
    return flat


def flatten_presets(bambu: Path, work: Path):
    """System presets with `inherits` resolved, marked as user presets of themselves (what the CLI accepts).
    Also checks that the bed numbers this script lays out against are the profile's."""
    flat = profiles(bambu)
    m = flat(MACHINE)
    area = [tuple(float(v) for v in p.split("x")) for p in m["printable_area"]]
    assert (max(a for a, _ in area), max(b for _, b in area)) == (BED_X, BED_Y), m["printable_area"]
    assert float(m["printable_height"]) == BED_Z
    ext = [[tuple(float(v) for v in p.split("x")) for p in s.split(",")] for s in m["extruder_printable_area"]]
    assert [(min(x for x, _ in e), max(x for x, _ in e)) for e in ext] == [REACH["left"], REACH["right"]], ext
    w = [tuple(float(v) for v in p.split("x")) for p in m["wrapping_exclude_area"]]
    assert (min(x for x, _ in w), min(y for _, y in w), max(x for x, _ in w), max(y for _, y in w)) == WRAP_ZONE, w
    model_id = flat(MACHINE_MODEL)["model_id"]

    paths = {}
    for typ, name, sid in (("machine", MACHINE, "printer_settings_id"), ("process", PROCESS, "print_settings_id"),
                           ("filament", FILAMENT, "filament_settings_id")):
        d = flat(name)
        d.update({"type": typ, "name": name, "inherits": name, "from": "User", "instantiation": "true"})
        d.pop("include", None)
        d[sid] = [name] if typ == "filament" else name
        if typ == "process":
            d["curr_bed_type"] = "Textured PEI Plate"  # the H2D's default plate; set explicitly for the CLI
        if typ == "filament":
            d["filament_colour"] = ["#FFFFFF"]  # display colour only; see the README on pigments
        paths[typ] = work / f"{typ}.json"
        paths[typ].write_text(json.dumps(d, indent=1))
    return paths, model_id


def bambu_plate(items, res, bambu: Path, presets, model_id: str, work: Path):
    app = bambu / "AppRun"
    stl_dir = work / "stl"
    stl_dir.mkdir()
    names = []
    for it in items:
        f = stl_dir / f"{it['name']}.stl"
        it["mesh"].export(f)
        names.append(f.name)
    settings = ["--load-settings", f"{presets['machine']};{presets['process']}", "--load-filaments", str(presets["filament"]),
                *NOZZLES]

    def side(n):
        return ["--filament-map-mode", "Manual", "--filament-map", str(n)]

    raw = work / "raw"
    raw.mkdir()
    a1.run([app, "--arrange", "0", "--orient", "0", *settings, *side(PRINT_WITH), "--outputdir", raw,
            "--export-3mf", "p.3mf", *names], stl_dir)

    # Per-object infill and scarf seams, the plate's name, and the magnet pauses.
    with zipfile.ZipFile(raw / "p.3mf") as z:
        ms = z.read("Metadata/model_settings.config").decode()
    for it in items:
        infill = PARTS[it["key"]][4]
        extra = []
        if infill:
            extra.append(f'<metadata key="sparse_infill_density" value="{infill}"/>')
        if it["key"] in LID_KEYS + ("cap",):
            extra.append('<metadata key="seam_slope_type" value="all"/>')  # scarf seam: no bump on the boss or bore
        if extra:
            pat = f'(<object id="\\d+">\\s*<metadata key="name" value="{re.escape(it["name"])}\\.stl"/>)'
            ms, n = re.subn(pat, lambda mm: mm.group(1) + "\n    " + "\n    ".join(extra), ms)
            assert n == 1, f"object {it['name']} not found in model_settings.config"
    ms, n = re.subn(r'<metadata key="plater_name" value="[^"]*"/>',
                    f'<metadata key="plater_name" value="{PLATE_NAME}"/>', ms)
    assert n == 1, "plate name not found in model_settings.config"
    layers = "".join(f'<layer top_z="{p["pause_before_layer_z"]}" type="1" extruder="1" color="" extra="" gcode="M400 U1"/>\n'
                     for p in res["pauses"])
    edits = {"Metadata/model_settings.config": ms.encode(),
             "Metadata/custom_gcode_per_layer.xml": (
                 '<?xml version="1.0" encoding="utf-8"?>\n<custom_gcodes_per_layer>\n<plate>\n<plate_info id="1"/>\n'
                 f'{layers}<mode value="SingleExtruder"/>\n</plate>\n</custom_gcodes_per_layer>\n').encode()}
    project = HERE / "h2d-corrosion-all.3mf"
    a1.rezip(raw / "p.3mf", project, edits)

    out = {}
    for n in (PRINT_WITH, 3 - PRINT_WITH):  # the file to print, then the other nozzle as a check only
        sliced_dir = work / f"sliced-{NOZZLE_SIDE[n]}"
        sliced_dir.mkdir()
        a1.run([app, "--slice", "0", *settings, *side(n), "--outputdir", sliced_dir, "--export-3mf", "s.gcode.3mf",
                str(project)], work)
        with zipfile.ZipFile(sliced_dir / "s.gcode.3mf") as z:
            info = z.read("Metadata/slice_info.config").decode()
            gcode = z.read("Metadata/plate_1.gcode").decode()
            proj = json.loads(z.read("Metadata/project_settings.config"))
        info, k = re.subn(r'(key="printer_model_id" value=")[^"]*(")', rf"\g<1>{model_id}\g<2>", info)
        assert k == 1, "printer_model_id not found in slice_info.config"
        s = summarise(info, gcode, proj, res["pockets"])
        assert s["nozzle"] == NOZZLE_SIDE[n], (s["nozzle"], n)
        if n == PRINT_WITH:
            a1.rezip(sliced_dir / "s.gcode.3mf", HERE / "h2d-corrosion-all.gcode.3mf",
                     {"Metadata/slice_info.config": info.encode()})
            out = s
        else:
            out["other_nozzle_check"] = {kk: s[kk] for kk in ("nozzle", "time_h", "filament_g", "pause_count",
                                                              "extrusion_xy_extent_mm")}
            out["other_nozzle_check"]["pockets_ok"] = len(s["magnet_pockets"]) == len(res["pockets"])
    return out


def summarise(info: str, gcode: str, proj: dict, pockets):
    meta = dict(re.findall(r'<metadata key="([^"]+)" value="([^"]*)"/>', info))
    out = {"slicer_version": re.search(r'X-BBL-Client-Version" value="([^"]+)"', info).group(1),
           "time_s": int(float(meta["prediction"])), "time_h": round(float(meta["prediction"]) / 3600, 2),
           "filament_g": float(meta["weight"]), "pause_count": int(meta.get("pause_count", 0)),
           "filament_m": float(re.search(r'used_m="([\d.]+)"', info).group(1)),
           "bed_type": proj.get("curr_bed_type"),
           "bed_temp_C": int(re.search(r"^; textured_plate_temp = (\d+)", gcode, re.M).group(1)),
           "nozzle_temp_C": int(re.search(r"^; nozzle_temperature = (\d+)", gcode, re.M).group(1)),
           "filament_map_mode": proj.get("filament_map_mode")}
    # Which nozzle prints: slice_info's filament_maps is the extruder used for each filament (1 left, 2 right).
    out["nozzle"] = NOZZLE_SIDE.get(int(meta["filament_maps"].split()[0]), "?")
    assert [str(v) for v in proj.get("filament_map", [])][:1] == meta["filament_maps"].split()[:1], "filament map"
    # When each pause comes: the last progress report (M73 P<percent> R<minutes left>) before it.
    out["pauses"] = []
    for m in re.finditer(r"^M400 U1", gcode, re.M):
        before = gcode[:m.start()]
        z = re.findall(r"^; Z_HEIGHT: ([\d.]+)", before, re.M)[-1]
        pct, left = re.findall(r"^M73 P(\d+) R(\d+)", before, re.M)[-1]
        out["pauses"].append({"before_layer_z": float(z), "progress_pct": int(pct),
                              "elapsed_h": round(out["time_s"] / 3600 - int(left) / 60, 2),
                              "remaining_h": round(int(left) / 60, 2)})
    # Where the extrusions landed: inside the bed, and inside the printing nozzle's reach.
    xs, ys = [], []
    for _, _, x0, y0, x1, y1 in a1.extrusions(gcode):
        xs += [x0, x1]
        ys += [y0, y1]
    ext = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    out["extrusion_xy_extent_mm"] = ext
    lo, hi = REACH[out["nozzle"]]
    assert lo <= ext[0] and ext[2] <= hi and 0 <= ext[1] and ext[3] <= BED_Y, ext
    out["magnet_pockets"] = a1.pocket_check(gcode, pockets)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bambu", type=Path, help="unpacked Bambu Studio AppImage (squashfs-root)")
    args = ap.parse_args()

    items = placed()
    res = check(items)
    work = Path(tempfile.mkdtemp(prefix="h2dplate-"))
    if args.bambu:
        presets, model_id = flatten_presets(args.bambu, work)
        res["slice"] = bambu_plate(items, res, args.bambu, presets, model_id, work)
        assert res["slice"]["pause_count"] == len(PAUSES), "pause count"
        assert [p["before_layer_z"] for p in res["slice"]["pauses"]] == [p["pause_before_layer_z"] for p in res["pauses"]]
    s = res.get("slice")
    print(f"{len(items)} pieces, min gap {res['min_gap_mm']} mm ({' / '.join(res['closest_pair'])}), "
          f"extent {res['layout_extent_mm']}" + (f", {s['time_h']} h, {s['filament_g']} g, pauses {s['pauses']}" if s else ""))

    draw(items, res, HERE / "plate.png")
    summary = {
        "made_by": "make_h2d_plate.py",
        "printer": MACHINE, "process": PROCESS, "filament": FILAMENT,
        "bed_mm": [BED_X, BED_Y, BED_Z], "nozzle_reach_x_mm": REACH, "layout_kept_in_x_mm": BOTH_X,
        "wrap_detection_zone_mm": WRAP_ZONE, "margin_mm": MARGIN, "min_gap_allowed_mm": GAP,
        "plate_name": PLATE_NAME,
        "not_printed": [{"bom": b, "part": p, "why": w} for b, p, w in NOT_PRINTED],
        "pieces": len(items),
        **{k: v for k, v in res.items() if k != "pockets"},
        "parts": part_rows(items),
        "placements": [{"name": it["name"], "centre_xy": [it["x"], it["y"]], "rot_z": it["rot"],
                        "footprint_mm": it["footprint_mm"], "height_mm": it["height_mm"]} for it in items],
    }
    (HERE / "plate.json").write_text(json.dumps(summary, indent=1) + "\n")
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
