#!/usr/bin/env python3
"""Plates for the Bambu Lab A1 mini, in PLA, holding every printed part of the CubXL corrosion setup.

Ben asked on #180 (2026-11-06) for all the setup's printed parts on the A1 mini's 180 x 180 mm plate,
in PLA, in batches if they don't fit. They don't fit on one plate, so this script lays them out on
five: a short fit check first, three main plates, and an optional fifth for the vial holder. It checks
each layout (inside the bed with a margin, a gap between parts, magnet pockets open at the pause
layer), draws plates.png and writes plates.json. Given an unpacked Bambu Studio, it also writes
each plate as a Bambu Studio project (.3mf) and as sliced G-code (.gcode.3mf), with 100 % infill on
the parts the BOM asks it for and a pause for the magnets.

    python make_plates.py --capper-cad /tmp/capper-cad
    python make_plates.py --capper-cad /tmp/capper-cad --bambu /tmp/bambu/squashfs-root

--capper-cad  a folder holding VialCap16mm.step and 9VialHolder20mL_TightFit.step from
              vertical-cloud-lab/byu-vcl at f1b4666, modules/electromagnetic-capper/cad/
              (PANDA-BEAR's files, GPL-2.0-or-later: see LICENSE-GPL-2.0.txt and NOTICE.txt here).
--bambu       an unpacked Bambu Studio Linux AppImage (`--appimage-extract`); tested with 02.09.01.70.

Needs trimesh, cascadio (STEP), shapely, matplotlib and numpy.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import MultiPoint, box

HERE = Path(__file__).resolve().parent
AC = HERE.parents[1]  # alloy-corrosion/

BED = 180.0  # A1 mini, mm
MARGIN = 5.0  # keep parts this far inside the bed edge
GAP = 5.0  # minimum gap between parts
LAYER, FIRST_LAYER = 0.2, 0.2  # 0.20mm Standard @BBL A1M

MACHINE = "Bambu Lab A1 mini 0.4 nozzle"
PROCESS = "0.20mm Standard @BBL A1M"
FILAMENT = "Bambu PLA Basic @BBL A1M"
MODEL_ID = "N1"  # the A1 mini's model_id in Bambu Studio's BBL profiles

FLIP = trimesh.transformations.rotation_matrix(math.pi, [1, 0, 0])  # upside down

# key: BOM ID, what it is, source, print orientation, infill (None = the profile's 15 %), notes.
# Orientation: None = as drawn; FLIP = turned over. Sources are relative to alloy-corrosion/, or
# "capper:" for the PANDA-BEAR STEP files.
PARTS = {
    "lid_006": ("P03", "Well lid v2, AS568-006", "bom/cad/well_lid_v2_006.stl", None, "100%",
                "bottom face down; two magnets at the pause"),
    "lid_008": ("P04", "Well lid v2, AS568-008", "bom/cad/well_lid_v2_008.stl", None, "100%",
                "bottom face down; two magnets at the pause"),
    "lid_010": ("P05", "Well lid v2, AS568-010", "bom/cad/well_lid_v2_010.stl", None, "100%",
                "bottom face down; two magnets at the pause"),
    "cap": ("P01", "Electrode cap", "copper/cad/electrode_cap.stl", None, "100%", "skirt down"),
    "carrier": ("P02", "Electrode carrier", "copper/cad/electrode_carrier.stl", FLIP, "100%",
                "turned over: plug on the bed, legs up"),
    "tray": ("P06", "Coupon tray", "copper/cad/coupon_tray.stl", None, None, "pockets up"),
    "shim_1": ("P07", "Shim 1 mm", "copper/cad/shim_1mm.stl", None, None, ""),
    "shim_3": ("P07", "Shim 3 mm", "copper/cad/shim_3mm.stl", None, None, ""),
    "cup_block": ("P08", "Cup block", "bom/cad/cup_block_3.stl", None, "100%",
                  "base down; six magnets at the pause"),
    "tip_waste": ("P09", "Tip waste cup", "bom/cad/tip_waste_cup.stl", None, None, ""),
    "tube_rack": ("P10", "Tube rack 2 x 8", "bom/cad/tube_rack_2x8.stl", FLIP, None,
                  "upside down: the hole plate on the bed, like the fit strip"),
    "tip_rack": ("P11", "Tip rack 2 x 15", "bom/cad/tip_rack_2x15.stl", FLIP, None,
                 "upside down: the hole plate on the bed, like the fit strip"),
    "strip_tube": ("P12", "Fit strip, tube", "bom/cad/fit_strip_tube.stl", None, None, ""),
    "strip_tip": ("P12", "Fit strip, tip", "bom/cad/fit_strip_tip.stl", None, None, ""),
    "vial_cap": ("P13", "Magnetic vial cap", "capper:VialCap16mm.step", None, None,
                 "skirt down; PDMS fill and steel disc afterwards"),
    "holder_a": ("P14", "9-vial holder, positions 1-5", "capper:9VialHolder20mL_TightFit.step#a", None, None,
                 "cut from PANDA-BEAR's one-piece holder"),
    "holder_b": ("P14", "9-vial holder, positions 6-9", "capper:9VialHolder20mL_TightFit.step#b", None, None,
                 "cut from PANDA-BEAR's one-piece holder"),
    "cell_body": ("P15", "Bench cell body", "bom/cad/bench_cell_body.stl", None, "100%", "floor down"),
    "cell_clamp": ("P16", "Bench cell clamp plate", "bom/cad/bench_cell_clamp.stl", None, None,
                   "counterbored face down"),
    "cell_cover": ("P17", "Bench cell cover", "bom/cad/bench_cell_cover.stl", FLIP, None,
                   "turned over: flat top on the bed, lip up"),
    # Deck keys (2026-11-09, ../cad/deck_keys.py): the stir module's key, solid so the nub prints like the
    # four-wall keys of byu-vcl's 2026-10-22 fit test. Dimples on the pill's top: one per 0.05 mm of press.
    "deck_key": ("P19", "Deck key, 0.05 mm press", "bom/cad/deck_key.stl", None, "100%",
                 "pill on the bed, nub up; one dimple"),
    "deck_key_010": ("P19", "Deck key, 0.10 mm press (fit test)", "bom/cad/deck_key_fit_0.10.stl", None, "100%",
                     "pill on the bed, nub up; two dimples"),
    "deck_key_015": ("P19", "Deck key, 0.15 mm press (fit test)", "bom/cad/deck_key_fit_0.15.stl", None, "100%",
                     "pill on the bed, nub up; three dimples"),
}

# The holder is 297.4 mm long, more than the bed's 254.6 mm diagonal. Cut it through the web
# between positions 5 and 6 (y = -148.5 in its STEP frame, where pockets sit at y = -33 k).
HOLDER_CUT_Y = -148.5

# Each plate: slug, title, when to print it, pauses as (height of the pocket tops, what to insert),
# and parts as (part, x, y, z-rotation in degrees) with x, y the centre of the part's footprint.
PLATES = [
    {
        "slug": "plate1-fit-check",
        "title": "1  Fit check (print first)",
        "name": "1 Fit check",  # plate name in Bambu Studio (no colons: it drops those)
        "when": "First. Check the cap over the lid's boss, the carrier in the cap, and the strips' holes on real tips and tubes",
        "pauses": [(5.6, "two 4 x 2 mm magnets in the lid, same pole up")],
        "items": [("strip_tube", 90, 62, 0), ("strip_tip", 90, 42, 0),
                  ("lid_006", 62, 100, 0), ("cap", 96, 100, 0), ("carrier", 124, 100, 0)],
    },
    {
        "slug": "plate2-cell",
        "title": "2  Cell: lids, cap, carriers, shims, tray",
        "name": "2 Cell parts",  # plate name in Bambu Studio (no colons: it drops those)
        "when": "After plate 1 shows the cap slides over the boss",
        "pauses": [(5.6, "twelve 4 x 2 mm magnets, two per lid, same pole up")],
        "items": [("tray", 90, 30, 0),
                  ("lid_006", 25, 75.5, 0), ("lid_006", 55, 75.5, 0), ("lid_006", 85, 75.5, 0),
                  ("lid_006", 25, 116.5, 0), ("lid_008", 55, 116.5, 0), ("lid_010", 85, 116.5, 0),
                  ("cap", 120, 75.5, 0), ("carrier", 147, 75.5, 0), ("carrier", 162, 75.5, 0),
                  ("shim_1", 120, 116.5, 0), ("shim_1", 146.4, 116.5, 0),
                  ("shim_3", 24, 150.2, 0), ("shim_3", 50.4, 150.2, 0), ("shim_3", 76.8, 150.2, 0),
                  ("shim_3", 103.2, 150.2, 0), ("shim_1", 129.6, 150.2, 0), ("shim_1", 156, 150.2, 0)],
    },
    {
        "slug": "plate3-deck",
        "title": "3  Deck: cup block, racks, tip waste, vial caps",
        "name": "3 Deck parts and vial caps",  # plate name in Bambu Studio (no colons: it drops those)
        "when": "After the fit strips from plate 1 have picked the rack holes (rerun cad_build_parts.py if they changed)",
        "pauses": [(44.6, "six 4 x 2 mm magnets in the cup block, same pole up as the lids")],
        "items": [("tube_rack", 60, 25, 0), ("cup_block", 58, 62, 0), ("tip_waste", 34, 104, 0),
                  ("tip_rack", 124, 77, 0),
                  ("vial_cap", 154, 22, 0), ("vial_cap", 154, 56, 0), ("vial_cap", 154, 90, 0),
                  ("vial_cap", 154, 124, 0), ("vial_cap", 154, 158, 0),
                  ("vial_cap", 26, 146, 0), ("vial_cap", 60, 146, 0), ("vial_cap", 94, 96, 0)],
    },
    {
        "slug": "plate4-bench-cell",
        "title": "4  Bench cell (copper calibration)",
        "name": "4 Bench cell",  # plate name in Bambu Studio (no colons: it drops those)
        "when": "Any time; nothing on it depends on the fit check",
        "pauses": [],
        "items": [("cell_body", 45, 55, 0), ("cell_cover", 127, 55, 0), ("cell_clamp", 90, 130, 0)],
    },
    {
        "slug": "plate5-vial-holder-optional",
        "title": "5  Optional: 9-vial holder in two pieces",
        "name": "5 Vial holder (optional)",  # plate name in Bambu Studio (no colons: it drops those)
        "when": "Only if the deck has no full 9-position holder yet",
        "pauses": [],
        "items": [("holder_a", 69, 90, 0), ("holder_b", 113, 90, 0)],
    },
]

_cache: dict[str, trimesh.Trimesh] = {}


def load_source(src: str, capper: Path | None) -> trimesh.Trimesh:
    if src.startswith("capper:"):
        if capper is None:
            raise SystemExit("--capper-cad is needed for the PANDA-BEAR parts (P13, P14)")
        name, _, half = src[len("capper:"):].partition("#")
        scene = trimesh.load(capper / name)
        mesh = scene.to_geometry() if isinstance(scene, trimesh.Scene) else scene
        if getattr(scene, "units", None) in ("meters", "m") or mesh.extents.max() < 1.0:
            mesh.apply_scale(1000.0)
        mesh.merge_vertices()
        if half == "a":
            mesh = mesh.slice_plane([0, HOLDER_CUT_Y, 0], [0, 1, 0], cap=True)
        elif half == "b":
            mesh = mesh.slice_plane([0, HOLDER_CUT_Y, 0], [0, -1, 0], cap=True)
        return mesh
    return trimesh.load(AC / src, force="mesh")


def part_mesh(key: str, capper: Path | None) -> trimesh.Trimesh:
    """The part in its print orientation, footprint centred on the origin, sitting on z = 0."""
    if key not in _cache:
        _, _, src, orient, _, _ = PARTS[key]
        m = load_source(src, capper)
        if orient is not None:
            m.apply_transform(orient)
        lo, hi = m.bounds
        m.apply_translation([-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]])
        _cache[key] = m
    return _cache[key].copy()


def placed(plate, capper):
    out, count = [], {}
    for key, x, y, rot in plate["items"]:
        m = part_mesh(key, capper)
        if rot:
            m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(rot), [0, 0, 1]))
        m.apply_translation([x, y, 0])
        count[key] = count.get(key, 0) + 1
        out.append({"key": key, "name": f"{PARTS[key][0]}_{key}_{count[key]}", "x": x, "y": y, "rot": rot, "mesh": m})
    return out


def pause_layer(h: float) -> float:
    """print_z of the first layer above a pocket top at h: the pause goes in before it."""
    k = (h - FIRST_LAYER) / LAYER
    assert abs(k - round(k)) < 1e-6, f"pocket top {h} is not on a {LAYER} mm layer boundary"
    return round(h + LAYER, 3)


def holes_at(m: trimesh.Trimesh, z: float) -> int:
    s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if s is None:
        return 0
    p, _ = s.to_2D()
    return sum(len(q.interiors) for q in p.polygons_full)


def section_xy(m: trimesh.Trimesh, z: float):
    """The part's cross-section at height z, as a shapely shape in bed coordinates."""
    from shapely.ops import unary_union
    s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    t = np.eye(4)
    t[2, 3] = -z
    p, _ = s.to_2D(to_2D=t)
    return unary_union(p.polygons_full)


def check(plate, items):
    """Bounds, gaps, heights, and for each pause that the pockets are open below it and covered above."""
    bed = box(MARGIN, MARGIN, BED - MARGIN, BED - MARGIN)
    hulls = []
    for it in items:
        m = it["mesh"]
        hull = MultiPoint(m.vertices[:, :2]).convex_hull
        it["footprint_mm"] = [round(v, 2) for v in (m.extents[0], m.extents[1])]
        it["height_mm"] = round(float(m.extents[2]), 2)
        assert bed.contains(hull), f"{plate['slug']}: {it['name']} is closer than {MARGIN} mm to the bed edge"
        assert m.bounds[1][2] <= BED, f"{it['name']} is taller than the A1 mini's 180 mm"
        hulls.append((it["name"], hull))
    gaps = []
    for i in range(len(hulls)):
        for j in range(i + 1, len(hulls)):
            d = hulls[i][1].distance(hulls[j][1])
            gaps.append(d)
            assert d >= GAP - 1e-6, f"{plate['slug']}: {hulls[i][0]} and {hulls[j][0]} are {d:.1f} mm apart"
    plate["min_gap_mm"] = round(min(gaps), 1) if gaps else None
    plate["pause_layers"], plate["pockets"] = [], []
    for h, _ in plate["pauses"]:
        plate["pause_layers"].append(pause_layer(h))
        for it in items:
            if it["key"] not in ("lid_006", "lid_008", "lid_010", "cup_block"):
                continue
            below, above = holes_at(it["mesh"], h - 0.1), holes_at(it["mesh"], h + 0.1)
            assert below > above, f"{it['name']}: no pocket closes at z {h}"
            # Pocket centres: solid just above the pocket tops, empty just below.
            new = section_xy(it["mesh"], h + 0.1).difference(section_xy(it["mesh"], h - 0.1))
            for g in getattr(new, "geoms", [new]):
                if g.area > 1.0:
                    plate["pockets"].append((h, it["name"], g.centroid.x, g.centroid.y))


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

def draw(plates, results, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MplPolygon, Rectangle
    from trimesh.path.polygons import projected

    fig, axes = plt.subplots(2, 3, figsize=(15, 10.6))
    for ax, plate in zip(axes.flat, plates):
        items = results[plate["slug"]]["items"]
        ax.add_patch(Rectangle((0, 0), BED, BED, facecolor="#f4f4f2", edgecolor="#555", lw=1.2))
        ax.add_patch(Rectangle((MARGIN, MARGIN), BED - 2 * MARGIN, BED - 2 * MARGIN, fill=False,
                               edgecolor="#bbb", lw=0.8, ls="--"))
        for it in items:
            solid = PARTS[it["key"]][4] == "100%"
            outline = projected(it["mesh"], normal=[0, 0, 1], ignore_sign=True, rpad=1e-4, apad=1e-4)
            geoms = getattr(outline, "geoms", [outline])
            for g in geoms:
                ax.add_patch(MplPolygon(np.asarray(g.exterior.coords), closed=True,
                                        facecolor="#d9824b" if solid else "#7fa7c9", edgecolor="#333", lw=0.6))
                for hole in g.interiors:
                    ax.add_patch(MplPolygon(np.asarray(hole.coords), closed=True, facecolor="#f4f4f2",
                                            edgecolor="#333", lw=0.4))
            ax.text(it["x"], it["y"], PARTS[it["key"]][0], ha="center", va="center", fontsize=7.5,
                    color="black", bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))
        s = results[plate["slug"]].get("slice")
        sub = f"{len(items)} pieces"
        if s:
            sub += f", {s['time_h']:.1f} h, {s['filament_g']:.0f} g PLA"
        if plate["pauses"]:
            sub += f"; pause at z {', '.join(str(z) for z in plate['pause_layers'])}"
        ax.set_title(f"{plate['title']}\n{sub}", fontsize=10, loc="left")
        ax.set_xlim(-4, BED + 4)
        ax.set_ylim(-4, BED + 4)
        ax.set_aspect("equal")
        ax.set_xticks([0, 45, 90, 135, 180])
        ax.set_yticks([0, 45, 90, 135, 180])
        ax.tick_params(labelsize=7)
    ax = axes.flat[-1]
    ax.axis("off")
    ax.add_patch(Rectangle((0.02, 0.80), 0.08, 0.06, transform=ax.transAxes, facecolor="#d9824b", edgecolor="#333"))
    ax.text(0.13, 0.83, "100 % infill (touches the liquid)", transform=ax.transAxes, va="center", fontsize=9)
    ax.add_patch(Rectangle((0.02, 0.70), 0.08, 0.06, transform=ax.transAxes, facecolor="#7fa7c9", edgecolor="#333"))
    ax.text(0.13, 0.73, "profile infill (15 %)", transform=ax.transAxes, va="center", fontsize=9)
    ax.text(0.02, 0.62, "A1 mini bed, 180 x 180 mm, seen from above;\n"
            "dashed line: 5 mm margin. Labels are BOM IDs.\n\n"
            "PLA (Bambu PLA Basic profile), 0.20 mm layers,\n"
            "0.4 mm nozzle, textured PEI plate.\n"
            "Times and grams are Bambu Studio's estimates.",
            transform=ax.transAxes, va="top", fontsize=9)
    fig.suptitle("CubXL corrosion setup: every printed part on A1 mini plates", fontsize=13, x=0.02, ha="left")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------- Bambu Studio

def flatten_presets(bambu: Path, work: Path):
    """System presets with `inherits` resolved, marked as user presets of themselves (what the CLI accepts)."""
    bbl = bambu / "resources" / "profiles" / "BBL"
    index = json.loads((bbl.parent / "BBL.json").read_text())
    files = {it["name"]: bbl / it["sub_path"]
             for k in ("machine_model_list", "machine_list", "process_list", "filament_list") for it in index.get(k, [])}

    def flat(name, seen=()):
        d = json.loads(files[name].read_text())
        out = flat(d["inherits"], seen + (name,)) if d.get("inherits") else {}
        for inc in d.get("include", []) or []:
            out.update({k: v for k, v in flat(inc, seen + (name,)).items()
                        if k not in ("name", "instantiation", "type", "from", "setting_id", "inherits")})
        out.update({k: v for k, v in d.items() if k != "include"})
        return out

    paths = {}
    for typ, name, sid in (("machine", MACHINE, "printer_settings_id"), ("process", PROCESS, "print_settings_id"),
                           ("filament", FILAMENT, "filament_settings_id")):
        d = flat(name)
        d.update({"type": typ, "name": name, "inherits": name, "from": "User", "instantiation": "true"})
        d.pop("include", None)
        d[sid] = [name] if typ == "filament" else name
        if typ == "process":
            d["curr_bed_type"] = "Textured PEI Plate"  # the CLI otherwise slices for the cool plate (35 C)
        if typ == "filament":
            d["filament_colour"] = ["#FFFFFF"]  # display colour only; see the README on pigments
        paths[typ] = work / f"{typ}.json"
        paths[typ].write_text(json.dumps(d, indent=1))
    return paths


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(map(str, cmd))} failed ({r.returncode}):\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    return r


def rezip(src: Path, dst: Path, edits: dict[str, bytes]):
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = edits.pop(item.filename, None)
            zout.writestr(item, data if data is not None else zin.read(item.filename))
        for name, data in edits.items():
            zout.writestr(name, data)


def bambu_plate(plate, items, bambu: Path, presets, work: Path):
    app = bambu / "AppRun"
    stl_dir = work / plate["slug"]
    stl_dir.mkdir()
    names = []
    for it in items:
        f = stl_dir / f"{it['name']}.stl"
        it["mesh"].export(f)
        names.append(f.name)
    settings = ["--load-settings", f"{presets['machine']};{presets['process']}", "--load-filaments", str(presets["filament"])]
    raw = work / f"{plate['slug']}-raw"
    raw.mkdir()
    run([app, "--arrange", "0", "--orient", "0", *settings, "--outputdir", raw, "--export-3mf", "p.3mf", *names], stl_dir)

    # Per-object infill, the plate's name and the magnet pauses.
    with zipfile.ZipFile(raw / "p.3mf") as z:
        ms = z.read("Metadata/model_settings.config").decode()
    for it in items:
        infill = PARTS[it["key"]][4]
        extra = []
        if infill:
            extra.append(f'<metadata key="sparse_infill_density" value="{infill}"/>')
        if it["key"] in ("lid_006", "lid_008", "lid_010", "cap"):
            extra.append('<metadata key="seam_slope_type" value="all"/>')  # scarf seam: no bump on the boss or bore
        if extra:
            pat = f'(<object id="\\d+">\\s*<metadata key="name" value="{re.escape(it["name"])}\\.stl"/>)'
            ms, n = re.subn(pat, lambda m: m.group(1) + "\n    " + "\n    ".join(extra), ms)
            assert n == 1, f"object {it['name']} not found in model_settings.config"
    ms = ms.replace('<metadata key="plater_name" value=""/>',
                    f'<metadata key="plater_name" value="{plate["name"]}"/>')
    edits = {"Metadata/model_settings.config": ms.encode()}
    if plate["pauses"]:
        layers = "".join(f'<layer top_z="{z}" type="1" extruder="1" color="" extra="" gcode="M400 U1"/>\n'
                         for z in plate["pause_layers"])
        edits["Metadata/custom_gcode_per_layer.xml"] = (
            '<?xml version="1.0" encoding="utf-8"?>\n<custom_gcodes_per_layer>\n<plate>\n<plate_info id="1"/>\n'
            f'{layers}<mode value="SingleExtruder"/>\n</plate>\n</custom_gcodes_per_layer>\n').encode()
    project = HERE / f"{plate['slug']}.3mf"
    rezip(raw / "p.3mf", project, edits)

    sliced_dir = work / f"{plate['slug']}-sliced"
    sliced_dir.mkdir()
    run([app, "--slice", "0", *settings, "--outputdir", sliced_dir, "--export-3mf", "s.gcode.3mf", str(project)], work)
    with zipfile.ZipFile(sliced_dir / "s.gcode.3mf") as z:
        info = z.read("Metadata/slice_info.config").decode()
        gcode = z.read("Metadata/plate_1.gcode").decode()
    info = re.sub(r'(key="printer_model_id" value=")[^"]*(")', rf"\g<1>{MODEL_ID}\g<2>", info)
    rezip(sliced_dir / "s.gcode.3mf", HERE / f"{plate['slug']}.gcode.3mf",
          {"Metadata/slice_info.config": info.encode()})
    return summarise(info, gcode, items, plate["pockets"])


def extrusions(gcode: str):
    """(layer z, feature, x0, y0, x1, y1) for every extruding move of the model; arcs (G2/G3) are split into
    0.2 mm chords. Moves under '; FEATURE: Custom' (purge and prime lines) are left out."""
    z = feat = x = y = None
    for line in gcode.splitlines():
        if line.startswith("; Z_HEIGHT:"):
            z = round(float(line.split(":")[1]), 2)
            continue
        if line.startswith("; FEATURE:"):
            feat = line.split(":", 1)[1].strip()
            continue
        if not line.startswith(("G0 ", "G1 ", "G2 ", "G3 ")):
            continue
        w = {t[0]: float(t[1:]) for t in line.split(";")[0].split()[1:] if t[0] in "XYEIJ" and len(t) > 1}
        nx, ny = w.get("X", x), w.get("Y", y)
        if None not in (x, y, nx, ny) and z is not None and feat and feat != "Custom" and w.get("E", 0.0) > 0:
            if line.startswith(("G2", "G3")):
                cx, cy = x + w.get("I", 0.0), y + w.get("J", 0.0)
                r = math.hypot(x - cx, y - cy)
                a0, a1 = math.atan2(y - cy, x - cx), math.atan2(ny - cy, nx - cx)
                if line.startswith("G2"):  # clockwise
                    while a1 >= a0:
                        a1 -= 2 * math.pi
                else:
                    while a1 <= a0:
                        a1 += 2 * math.pi
                n = max(2, int(abs(a1 - a0) * r / 0.2) + 2)
                pts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(a0, a1, n)]
                for (px, py), (qx, qy) in zip(pts, pts[1:]):
                    yield z, feat, px, py, qx, qy
            else:
                yield z, feat, x, y, nx, ny
        x, y = nx, ny


def pocket_check(gcode: str, pockets):
    """Distance from each magnet pocket's centre to the nearest extrusion in the last layer before the
    pause (should clear the pocket) and in the first layer after it (should cover the pocket)."""
    layers = {}
    for z, _, x0, y0, x1, y1 in extrusions(gcode):
        layers.setdefault(z, []).append((x0, y0, x1, y1))

    def nearest(zl, px, py):
        seg = np.asarray(layers[round(zl, 2)])
        a, b = seg[:, :2], seg[:, 2:]
        ab = b - a
        t = np.clip(((px - a[:, 0]) * ab[:, 0] + (py - a[:, 1]) * ab[:, 1]) / np.maximum((ab ** 2).sum(1), 1e-12), 0, 1)
        return float(np.min(np.hypot(a[:, 0] + t * ab[:, 0] - px, a[:, 1] + t * ab[:, 1] - py)))

    out = []
    for h, name, px, py in pockets:
        before, after = nearest(h, px, py), nearest(h + LAYER, px, py)
        assert before > 1.5 and after < 0.5, f"{name}: pocket at ({px:.1f}, {py:.1f}) not open before / covered after the pause"
        out.append({"part": name, "pocket_xy": [round(px, 2), round(py, 2)], "nearest_extrusion_mm_at_z_" + f"{h}": round(before, 2),
                    "nearest_extrusion_mm_at_z_" + f"{round(h + LAYER, 2)}": round(after, 2)})
    return out


def summarise(info: str, gcode: str, items, pockets=()):
    meta = dict(re.findall(r'<metadata key="([^"]+)" value="([^"]*)"/>', info))
    out = {"slicer_version": re.search(r'X-BBL-Client-Version" value="([^"]+)"', info).group(1),
           "time_s": int(float(meta["prediction"])), "time_h": round(float(meta["prediction"]) / 3600, 2),
           "filament_g": float(meta["weight"]), "pause_count": int(meta.get("pause_count", 0)),
           "filament_m": float(re.search(r'used_m="([\d.]+)"', info).group(1)),
           "bed_temp_C": int(re.search(r"^; textured_plate_temp = (\d+)", gcode, re.M).group(1)),
           "nozzle_temp_C": int(re.search(r"^; nozzle_temperature = (\d+)", gcode, re.M).group(1))}
    # When each pause comes: the last progress report (M73 P<percent> R<minutes left>) before it.
    out["pauses"] = []
    for m in re.finditer(r"^M400 U1", gcode, re.M):
        before = gcode[:m.start()]
        z = re.findall(r"^; Z_HEIGHT: ([\d.]+)", before, re.M)[-1]
        pct, left = re.findall(r"^M73 P(\d+) R(\d+)", before, re.M)[-1]
        out["pauses"].append({"before_layer_z": float(z), "progress_pct": int(pct),
                              "elapsed_h": round(out["time_s"] / 3600 - int(left) / 60, 2), "remaining_h": round(int(left) / 60, 2)})
    # Where the extrusions landed, against the bed.
    xs, ys = [], []
    for _, _, x0, y0, x1, y1 in extrusions(gcode):
        xs += [x0, x1]
        ys += [y0, y1]
    out["extrusion_xy_extent_mm"] = [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]
    assert 0 <= out["extrusion_xy_extent_mm"][0] and out["extrusion_xy_extent_mm"][2] <= BED
    assert 0 <= out["extrusion_xy_extent_mm"][1] and out["extrusion_xy_extent_mm"][3] <= BED
    out["magnet_pockets"] = pocket_check(gcode, pockets)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--capper-cad", type=Path, help="folder with PANDA-BEAR's VialCap16mm.step and 9VialHolder20mL_TightFit.step")
    ap.add_argument("--bambu", type=Path, help="unpacked Bambu Studio AppImage (squashfs-root)")
    args = ap.parse_args()

    results = {}
    work = Path(tempfile.mkdtemp(prefix="a1plates-"))
    presets = flatten_presets(args.bambu, work) if args.bambu else None
    for plate in PLATES:
        items = placed(plate, args.capper_cad)
        check(plate, items)
        res = {"title": plate["title"], "bambu_plate_name": plate["name"], "when": plate["when"],
               "pauses": [{"pocket_top_z": h, "pause_before_layer_z": z, "insert": what}
                          for (h, what), z in zip(plate["pauses"], plate.get("pause_layers", []))],
               "min_gap_mm": plate["min_gap_mm"], "parts": part_rows(items),
               "placements": [{"name": it["name"], "centre_xy": [it["x"], it["y"]], "rot_z": it["rot"],
                               "footprint_mm": it["footprint_mm"], "height_mm": it["height_mm"]} for it in items],
               "items": items}
        if args.bambu:
            res["slice"] = bambu_plate(plate, items, args.bambu, presets, work)
            assert res["slice"]["pause_count"] == len(plate["pauses"]), f"{plate['slug']}: pause count"
        results[plate["slug"]] = res
        s = res.get("slice")
        print(f"{plate['slug']}: {len(items)} pieces, min gap {plate['min_gap_mm']} mm"
              + (f", {s['time_h']} h, {s['filament_g']} g, pauses {s['pauses']}" if s else ""))

    draw(PLATES, results, HERE / "plates.png")
    summary = {
        "made_by": "make_plates.py",
        "printer": MACHINE, "process": PROCESS, "filament": FILAMENT,
        "bed_mm": [BED, BED], "margin_mm": MARGIN, "min_gap_mm": GAP,
        "holder_cut": f"9VialHolder20mL_TightFit.step cut at y = {HOLDER_CUT_Y} (between positions 5 and 6)",
        "plates": {k: {kk: vv for kk, vv in v.items() if kk != "items"} for k, v in results.items()},
    }
    if args.bambu:
        summary["bambu_studio"] = next(r["slice"]["slicer_version"] for r in results.values())
        req = [p for p in PLATES if "optional" not in p["slug"]]
        summary["required_total"] = {
            "time_h": round(sum(results[p["slug"]]["slice"]["time_h"] for p in req), 1),
            "filament_g": round(sum(results[p["slug"]]["slice"]["filament_g"] for p in req), 1)}
    (HERE / "plates.json").write_text(json.dumps(summary, indent=1) + "\n")
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
