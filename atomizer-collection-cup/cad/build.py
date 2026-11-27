"""Build every assembly, export STEP, and check it: interference, mass, room under the cone, removal.

    python cad/build.py            # writes cad/out/*.step, cad/out/checks.json and cad/out/checks.md

Interference: exact OpenCascade booleans between every pair of parts in an assembly, plus each part
against the machine's cone section. Anything above 1 mm3 is reported. The O-rings are drawn squashed
to their compressed height, so they touch the flanges without overlapping.
Removal: the cup has to drop straight down far enough for the centring ring to clear (ring
thickness + 3 mm), then slide out sideways, so the room under it must be at least that.
"""

import itertools
import json
import math
import sys
from pathlib import Path

import cadquery as cq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import params as P  # noqa: E402
import parts as PT  # noqa: E402

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

DENSITY = {"316L": 8000, "304": 8000, "A2": 8000, "weld": 8000, "borosilicate": 2230, "fused_quartz": 2200,
           "EPDM": 1150, "FKM": 1850, "plastic": 1200, "TC": 8000}

ASSEMBLIES = {
    "stock": lambda: PT.joint_hardware() + PT.stock_cup(),
    "option_a": lambda: PT.joint_hardware() + PT.option_a(),
    "option_b": lambda: PT.joint_hardware() + PT.option_b(),
    "option_c": lambda: PT.joint_hardware() + PT.option_c(),
}

# pairs that are meant to touch along a face or a line (contact, not interference)
TOUCH_OK = ("weld bead", "thermocouple", "band clamp")


def overlap(a, b):
    bb = a.BoundingBox()
    cc = b.BoundingBox()
    if (bb.xmax < cc.xmin or cc.xmax < bb.xmin or bb.ymax < cc.ymin or cc.ymax < bb.ymin
            or bb.zmax < cc.zmin or cc.zmax < bb.zmin):
        return 0.0
    try:
        return a.intersect(b).Volume()
    except Exception:  # noqa: BLE001
        return float("nan")


def check(name, parts, cone):
    rows = []
    for (n1, s1, _, _), (n2, s2, _, _) in itertools.combinations(parts, 2):
        if any(t in n1 or t in n2 for t in TOUCH_OK):
            continue
        v = overlap(s1, s2)
        if not v <= 1.0:
            rows.append({"a": n1, "b": n2, "mm3": round(v, 1)})
    for n1, s1, _, _ in parts:
        for n2, s2, _, _ in cone:
            v = overlap(s1, s2)
            if not v <= 1.0:
                rows.append({"a": n1, "b": "machine: " + n2, "mm3": round(v, 1)})
    return rows


def main():
    cone = PT.cone_section()
    report = {"joint": P.JOINT.name, "z_joint_face_mm": P.Z_JOINT_FACE, "assemblies": {}}
    for name, fn in ASSEMBLIES.items():
        parts = fn()
        mass = sum(s.Volume() * 1e-9 * DENSITY.get(mat, 8000) for _, s, _, mat in parts)
        zmin = min(s.BoundingBox().zmin for _, s, _, _ in parts)
        rmax = max(max(abs(s.BoundingBox().xmax), abs(s.BoundingBox().xmin), abs(s.BoundingBox().ymax),
                       abs(s.BoundingBox().ymin)) for _, s, _, _ in parts)
        room = zmin + P.Z_JOINT_FACE           # gap between the cup's lowest point and the mat
        need = P.JOINT.ring_thk + 3.0
        inter = check(name, parts, cone)
        asm = cq.Assembly(name=name)
        for i, (n, s, col, mat) in enumerate(parts):
            asm.add(s, name=f"{i:02d}_{n}".replace(" ", "_").replace(":", "")[:60], color=cq.Color(*col))
        asm.save(str(OUT / f"{name}.step"))
        report["assemblies"][name] = {
            "parts": len(parts), "mass_kg": round(mass, 2), "lowest_point_z_mm": round(zmin, 1),
            "length_below_joint_mm": round(-zmin, 1), "max_radius_mm": round(rmax, 1),
            "gap_to_mat_mm": round(room, 1), "drop_needed_to_remove_mm": need,
            "fits": room >= max(P.FLOOR_CLEARANCE_MIN, need), "interferences": inter,
        }
        print(name, report["assemblies"][name]["mass_kg"], "kg", len(inter), "interferences", flush=True)
    full = cq.Assembly(name="machine_cone")
    for i, (n, s, col, mat) in enumerate(cone):
        full.add(s, name=f"{i:02d}_{n}".replace(" ", "_")[:60], color=cq.Color(*col))
    full.save(str(OUT / "machine_cone_section.step"))
    report["capacity_cm3"] = {k: round(v) for k, v in P.option_capacity_cm3().items()}
    (OUT / "checks.json").write_text(json.dumps(report, indent=2) + "\n")
    lines = [f"# CAD checks ({P.JOINT.name} joint, joint face {P.Z_JOINT_FACE:.0f} mm above the mat)\n",
             "| Assembly | Parts | Mass (kg) | Length below joint (mm) | Gap to mat (mm) | Fits | Interferences |",
             "|---|---:|---:|---:|---:|---|---|"]
    for n, r in report["assemblies"].items():
        it = "none" if not r["interferences"] else "; ".join(f"{x['a']} / {x['b']} {x['mm3']} mm3"
                                                           for x in r["interferences"])
        lines.append(f"| {n} | {r['parts']} | {r['mass_kg']} | {r['length_below_joint_mm']} | "
                     f"{r['gap_to_mat_mm']} | {'yes' if r['fits'] else '**no**'} | {it} |")
    lines.append("\nUsable volume (cm3): " + ", ".join(f"{k} {v}" for k, v in report["capacity_cm3"].items()))
    (OUT / "checks.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
