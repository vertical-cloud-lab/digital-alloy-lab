"""Export every custom part of the low-profile desktop LPBF (issue #260, PR #266) for outsourcing quotes.

For each part render_build.kind() calls 'stock' (machined) or 'sheet' (cut, bent, welded), and for the printed robot
assembly fixtures in analysis/out/assembly/tooling/, this writes:
  <out>/<slug>.step          one solid per distinct piece, in mm, moved so its bounding box starts at the origin
  <out>/<slug>.dxf           for flat profile parts only (a plate whose through-profile times its thickness is the
                             part's volume within 10 %): the through-profile (outline and through holes), 1:1 in mm
  <out>/parts.csv / .json    part, material, stock, qty per machine, envelope, volume, process class, critical features
  <out>/manifest.csv         every file written, with sha256 and size

The flat-profile test slices the plate at 15, 50 and 85 % of its thickness and keeps what all three slices share, so
blind pockets, counterbores and grooves drop out of the DXF; the STEP has them.

Run (use a frozen copy of cad/ while someone else edits the model):
  git worktree add --detach /tmp/snap-out HEAD
  /tmp/capmem 2 /tmp/venv/bin/python desktop-lpbf/analysis/outsourcing/export_parts.py \
      --cad /tmp/snap-out/desktop-lpbf/cad --out /tmp/outsourcing/parts
Takes about 2 min. The part files are not committed (they are rebuilt from the model); manifest.csv and parts.csv are
copied to desktop-lpbf/analysis/out/outsourcing/ by hand.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
import shutil
import sys
import time

# Process class per part, by slug prefix (first match wins). From machining.md, hours.csv's 'special' column,
# setup_plan.json (setup counts, 4th-axis swing) and build-sequence.md. 'flat' parts also get a DXF.
PROCESS = [
    ("process_chamber_body", "4-axis mill (3 setups on an HRT210 + riser); core out by waterjet or bandsaw"),
    ("chamber_floor_plate", "3-axis mill, 2 setups"),
    ("chamber_lid", "3-axis mill, 2 setups + drawer slot (keyseat cutter or sinker EDM)"),
    ("chamber_door", "3-axis mill, 2 setups + dovetail groove"),
    ("build_module_m", "lathe + TIG weld (316L, back-purged) + lathe (post-weld bore) + hone + 3-axis mill"),
    ("module_m50_bottom_flange", "lathe (internal grooves) + 3-axis mill"),
    ("hollow_piston_rod", "buy tube; cut, weld into rod end, polish"),
    ("rod_end", "lathe + 3-axis mill"),
    ("striker", "lathe + 3-axis mill (416 stainless)"),
    ("macor", "Macor: lathe (cut rod to length)"),
    ("build_plate", "lathe (bayonet lugs, groove) + 3-axis mill"),
    ("heater_block", "lathe (internal groove) + 3-axis mill"),
    ("piston_head", "lathe + 4-axis mill"),
    ("window_flange", "lathe + 3-axis mill"),
    ("window_retaining", "lathe"),
    ("field_stop", "lathe"),
    ("f_theta_adapter", "lathe (M85x1 internal thread)"),
    ("camera_window_retaining", "lathe"),
    ("camera_viewport", "4-axis mill + sine plate (compound-angle boss)"),
    ("cover_slide_drawer", "4-axis mill + dovetail groove"),
    ("recoater_floating_bearing", "lathe + 3-axis mill"),
    ("recoater_motor_standoff", "lathe"),
    ("optics_bridge_posts", "TIG weld (6061 tube + end caps) + 3-axis mill"),
    ("overflow_funnel", "3-axis mill (316L)"),
]
SHEET = [  # sheet parts (kind 'sheet'): material from the model; all are cut, bent and most are welded
    ("inlet_plenum", "sheet: laser cut + bend + TIG weld (316L)"),
    ("outlet_plenum", "sheet: laser cut + bend + TIG weld (316L)"),
    ("dose_chute", "sheet: laser cut + bend + weld (316L)"),
    ("gas_knife", "sheet: laser cut + bend + weld (316L)"),
    ("reservoir", "sheet: laser cut + bend + weld"),
    ("liners", "sheet: laser cut + bend"),
    ("radiation_shields", "sheet: laser cut (+ bend)"),
    ("laser_guard_panels", "sheet: laser cut + bend (5052)"),
    ("sliding_guard_door", "sheet: laser cut + bend"),
    ("rack_side_panels", "sheet: laser cut + bend"),
    ("umbilical_duct", "sheet: laser cut + bend"),
    ("operator_panel_box", "sheet: laser cut + bend + PEM inserts"),
]
# Critical features the quote must carry (machining.md 'Tolerances and finishes', seals.md, modules.md).
CRITICAL = {
    "process_chamber_body": "lid O-ring face gland 4.6 x 2.65 (+/-0.05) in the top face, flat 0.05 mm over 312 x 222; "
                            "floor O-ring rebate; SAE-4 O-ring-boss ports; Ø18 and Ø25.4 bores; STI inserts",
    "chamber_floor_plate": "floor face O-ring gland (+/-0.05); Ø96.00 H7 module port; 2 x Ø6 H7 dowel holes; STI inserts",
    "chamber_lid": "Ø56 window bore and O-ring seat; enclosed 72 x 6 drawer slot (redesign pending); STI inserts; "
                   "SAE-4 sensor ports",
    "chamber_door": "half-dovetail O-ring groove 1.32 x 2.3 (dovetail cutter); seal face Ra <= 0.8 um",
    "build_module_m": "Ø50.80 H7 (+0.030/0) bore, Ra <= 0.4 um, honed after welding; spigot Ø95.80 +/-0.02 with a "
                      "2-238 radial groove, concentric to the bore within ~0.05; 3 circumferential TIG seams, back-purged",
    "module_m50_bottom_flange": "two 2-114 rod-gland grooves Ø20.0 in a Ø15.93 throat (internal grooving tool)",
    "build_plate": "bayonet lugs, 0.4 mm rise over 40 deg (+/-0.02 suggested); 0.15 mm cold gap to the bore",
    "heater_block": "bayonet socket with an internal groove; 3 x Ø6.1 cartridge bores; Ø1.2 thermocouple holes 10:1",
    "piston_head": "radial seal grooves; 0.4 mm webs to fix",
    "window_flange": "two FKM O-ring grooves (+/-0.05), seal faces Ra <= 0.8 um",
    "cover_slide_drawer": "half-dovetail O-ring groove (dovetail cutter)",
    "metering_base": "two FKM face O-ring grooves",
    "camera_viewport": "boss and bore on a compound angle; FKM face O-ring groove",
    "overflow_funnel": "FKM face O-ring groove (316L)",
    "recoater_feedthrough_spacer": "FKM face O-ring grooves both sides",
    "recoater_floating_bearing": "FKM face O-ring groove; bearing bore",
    "hollow_piston_rod": "polished Ra <= 0.2 um where it runs in the gland",
    "f_theta_adapter": "M85x1 internal thread",
    "rod_end": "Ø5.6 x 29 deep hole (peck); rod welded in",
}
MAT = {"al6061": "6061-T6", "mic6": "MIC-6 cast tooling plate", "macor": "Macor", "ss316l": "316L", "steel": "416 stainless",
       "ss304": "304", "al5052": "5052-H32"}


def first(table, slug, default=""):
    for k, v in table:
        if slug.startswith(k) or k in slug:
            return v
    return default


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def through_profile(cq, solid):
    """(face, thickness, area ratio) for a plate-like solid, rotated so its thin axis is z; else None."""
    bb = solid.BoundingBox()
    dims = [bb.xlen, bb.ylen, bb.zlen]
    ax = dims.index(min(dims))
    t = dims[ax]
    if t > 26.0 or max(dims) < 3.0 * t:
        return None
    s = solid
    if ax == 0:
        s = s.rotate((0, 0, 0), (0, 1, 0), 90)
    elif ax == 1:
        s = s.rotate((0, 0, 0), (1, 0, 0), 90)
    b = s.BoundingBox()
    s = s.translate(cq.Vector(-b.xmin, -b.ymin, -b.zmin))
    b = s.BoundingBox()
    common = None
    for f in (0.15, 0.5, 0.85):
        z = b.zmin + f * b.zlen
        plane = cq.Face.makePlane(b.xlen * 1.2 + 10, b.ylen * 1.2 + 10, basePnt=(b.xlen / 2, b.ylen / 2, z), dir=(0, 0, 1))
        sec = s.intersect(plane).translate(cq.Vector(0, 0, -z))
        common = sec if common is None else common.intersect(sec)
    area = sum(f.Area() for f in common.Faces())
    ratio = area * b.zlen / s.Volume() if s.Volume() > 0 else 0
    if not (0.9 <= ratio <= 1.1) or not common.Faces():
        return None
    return common, b.zlen, ratio


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cad", required=True)
    ap.add_argument("--out", default="/tmp/outsourcing/parts")
    ap.add_argument("--module", default="M50")
    a = ap.parse_args()
    cad = pathlib.Path(a.cad).resolve()
    sys.path.insert(0, str(cad))
    sys.path.insert(0, str(cad.parent / "analysis" / "machining"))
    import cadquery as cq
    from cadquery.occ_impl.exporters.dxf import DxfDocument
    import inventory as INV   # kind() and slug(), the same classification as the machining review
    import lpbf_low as M
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    dfm_path = cad.parent / "analysis" / "out" / "machining" / "dfm.json"
    dfm = {r["slug"]: r for r in json.loads(dfm_path.read_text())["parts"]} if dfm_path.exists() else {}
    t0 = time.time()
    parts = M.build(include_tray=False, module=a.module, fasteners=True)
    print(f"built {len(parts)} parts in {time.time() - t0:.0f} s", flush=True)
    rows, seen = [], set()
    for p in parts:
        k = INV.kind(p)
        if k not in ("stock", "sheet"):
            continue
        s = INV.slug(p.name)
        while s in seen:
            s += "_b"
        seen.add(s)
        groups = {}
        for sol in p.shape.Solids():
            bb = sol.BoundingBox()
            key = (round(sol.Volume() / 50.0), tuple(sorted(round(d) for d in (bb.xlen, bb.ylen, bb.zlen))))
            groups.setdefault(key, []).append(sol)
        for gi, (key, sols) in enumerate(sorted(groups.items(), key=lambda kv: -kv[0][0])):
            sol = sols[0]
            bb = sol.BoundingBox()
            sol = sol.translate(cq.Vector(-bb.xmin, -bb.ymin, -bb.zmin))
            name = s if len(groups) == 1 else f"{s}_{gi + 1}"
            step = out / f"{name}.step"
            cq.exporters.export(cq.Workplane().add(sol), str(step))
            files = [step]
            prof = None
            try:
                prof = through_profile(cq, sol)
            except Exception as e:  # noqa: BLE001 - a failed slice only means no DXF
                print("  profile failed:", name, e)
            if prof:
                face, t, ratio = prof
                doc = DxfDocument()
                doc.add_shape(face)
                dxf = out / f"{name}.dxf"
                doc.document.saveas(str(dxf))
                files.append(dxf)
            env = sorted((bb.xlen, bb.ylen, bb.zlen), reverse=True)
            d = dfm.get(s, {})
            if k == "sheet":
                proc = first(SHEET, s, "sheet: laser cut + bend")
            else:
                proc = first(PROCESS, s, "")
                if not proc:
                    proc = "waterjet or saw + 3-axis mill (drill, tap)" if prof else "3-axis mill, 2 setups"
            crit = next((v for kk, v in CRITICAL.items() if s.startswith(kk)), "")
            hc = d.get("hole_counts", {})
            holes = "; ".join(f"{n} x {kk}" for kk, n in sorted(hc.items()) if not kk.startswith("sti-tip"))
            rows.append(dict(
                part=p.name, slug=s, file=name, kind=k, material=MAT.get(p.mat, p.mat), stock=d.get("stock", ""),
                qty_per_machine=len(sols), pieces_in_model=len(p.shape.Solids()),
                envelope_mm=" x ".join(f"{x:.1f}" for x in env), volume_cm3=round(sol.Volume() / 1000.0, 2),
                mass_kg=round(sol.Volume() * 1e-9 * M.MAT.get(p.mat, {"rho": 2700})["rho"], 3),
                flat_profile=bool(prof), thickness_mm=round(prof[1], 2) if prof else "", process=proc,
                holes=holes, critical=crit, files=" ".join(f.name for f in files)))
            print(f"{k:5s} {name:62s} {p.mat:7s} x{len(sols)} {rows[-1]['envelope_mm']:24s} {'DXF' if prof else ''}", flush=True)
    # printed robot assembly fixtures (already STEP, written by analysis/assembly)
    tool_dir = cad.parent / "analysis" / "out" / "assembly" / "tooling"
    for f in sorted(tool_dir.glob("*.step")):
        shp = cq.importers.importStep(str(f)).val()
        bb = shp.BoundingBox()
        dst = out / f"tooling_{f.name}"
        shutil.copyfile(f, dst)
        rows.append(dict(part=f"Robot assembly fixture {f.stem} (analysis/out/assembly/tooling)", slug=f"tooling_{f.stem}",
                         file=dst.stem, kind="printed", material="PETG / PLA (printed)", stock="filament",
                         qty_per_machine=1, pieces_in_model=len(shp.Solids()),
                         envelope_mm=" x ".join(f"{x:.1f}" for x in sorted((bb.xlen, bb.ylen, bb.zlen), reverse=True)),
                         volume_cm3=round(shp.Volume() / 1000.0, 2), mass_kg=round(shp.Volume() * 1.27e-6, 3),
                         flat_profile=False, thickness_mm="", process="print (FDM)", holes="", critical="", files=dst.name))
    (out / "parts.json").write_text(json.dumps(dict(module=a.module, cad=str(cad), built_utc=time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
                                                    parts=rows), indent=1))
    with open(out / "parts.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(out / "manifest.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "sha256", "bytes"])
        for f in sorted(out.glob("*")):
            if f.suffix in (".step", ".dxf"):
                w.writerow([f.name, sha256(f), f.stat().st_size])
    print(f"{len(rows)} rows, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
