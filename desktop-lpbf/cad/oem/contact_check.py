"""Static contact check of the parts changed on 2026-11-23 (oem-parts.md): exact OCC intersections of each changed part with every
part whose bounding box it touches, in the closed, parked state of build(module). Run it on this tree and on an older tree to see
whether a refinement created a contact (the full answer, with the motion sweeps and the designed-contact list, is
analysis/interference.py; this is the quick check when its shared heavy slots are busy).

    python contact_check.py <cad dir> <module> <out.json> [r5|r6]      # r6 (default): the parts changed on 2026-11-25
"""
import json
import pathlib
import sys

CHANGED_R5 = ["Fiber laser source", "UPS (Eaton", "Recoater servo (ClearPath", "Z servo (ClearPath", "Dosing stepper (NEMA 17)",
              "Recoater carriage", "Overflow clamp (KF-40)", "Vacuum isolation valve", "Chamber door (", "DIN-rail drawer"]
# round 6 (2026-11-25): the nXDS6i, the 5169K72 filter train, the transmitter on its SAE-4 adapter, the KF stubs and the hose and
# exhaust runs that moved with them, and the rack units whose fronts changed
CHANGED_R6 = ["Dry scroll pump", "Pump inlet (KF-25)", "Sealed cyclone + HEPA housing", "Filter inlet (KF-25)", "Filter outlet (KF-25)",
              "Pressure transducer", "Gas-loop + vacuum hoses", "Pump exhaust to the dock", "Fiber laser source", "UPS (Eaton"]
CHANGED = CHANGED_R6


def touch(a, b, tol=0.01):
    return (a.xmin <= b.xmax + tol and b.xmin <= a.xmax + tol and a.ymin <= b.ymax + tol and b.ymin <= a.ymax + tol
            and a.zmin <= b.zmax + tol and b.zmin <= a.zmax + tol)


def main(cad, module, out, which="r6"):
    changed = CHANGED_R5 if which == "r5" else CHANGED_R6
    sys.path.insert(0, cad)
    import lpbf_low as M
    parts = M.build(module=module)
    res = []
    for pre in changed:
        for p in [q for q in parts if q.name.startswith(pre)]:
            pb = p.shape.BoundingBox()
            for q in parts:
                if q is p or "context" in q.tags or not touch(pb, q.shape.BoundingBox()):
                    continue
                try:
                    v = p.shape.intersect(q.shape).Volume()
                except Exception as e:      # report and carry on
                    v = f"{type(e).__name__}"
                if not isinstance(v, float) or v > 1e-3:
                    res.append(dict(part=p.name[:70], other=q.name[:70], mm3=v if isinstance(v, str) else round(v, 3)))
                    print(res[-1], flush=True)
    pathlib.Path(out).write_text(json.dumps(dict(cad=cad, module=module, contacts=res), indent=1))
    print(len(res), "contacts")


if __name__ == "__main__":
    main(*sys.argv[1:5])
