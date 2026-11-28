"""Check the CAD's catalogue parts against the vendors' own STEP models.

    VENDOR_STEP_DIR=/tmp/bomwork python cad/vendor_check.py      # writes cad/out/vendor_check.{json,md,png}

The STEP files (McMaster-Carr, downloaded through bom/fetch_*.py) are not committed: they are the vendor's, and
McMaster's models are approximate. For each part: both solids are put on the z axis (the vendor's axis found
from its principal moments), the vendor's is flipped and slid along z to the position of largest overlap, and
the script reports both volumes, the overlap, and the volume each has that the other doesn't, as a percentage
of the vendor's volume. A section plot overlays the two outlines.
"""

import json
import math
import os
import sys
from pathlib import Path

import cadquery as cq
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
import params as P  # noqa: E402
import parts as PT  # noqa: E402

OUT = HERE / "out"
STEP_DIR = Path(os.environ.get("VENDOR_STEP_DIR", "/tmp/bomwork"))


def mine():
    kf = P.JOINT
    g = kf.ring_thk / 2

    def nipple(L):
        up = PT.kf_flange(kf, 0.0, down=True, tube_len=L / 2)
        lo = PT.kf_flange(kf, -L, down=False, tube_len=L / 2)
        return up.fuse(lo)
    ring, oring = PT.kf_centring_ring(kf, 0.0)
    b = P.B
    rt, R_o = kf.tube_od / 2, b["body_od"] / 2
    L = b["reducer_len"]
    red = PT.revolve([(rt - 1.65, 0), (rt, 0), (rt, -8), (R_o, -L + 8), (R_o, -L), (R_o - 1.65, -L), (R_o - 1.65, -L + 8),
                      (rt - 1.65, -8)])
    return {
        "4518K38": ("KF-50 x 2 in butt-weld stub, 19.05 (B1)", PT.kf_flange(kf, 0.0, down=True, tube_len=19.05)),
        "4518K43": ("KF-50 x 2 in butt-weld stub, 39.69 (alternative)", PT.kf_flange(kf, 0.0, down=True, tube_len=39.69)),
        "4518K61": ("KF-50 blank / cap (A2, B9)", PT.kf_blank(kf, 0.0)),
        "4518K877": ("KF-50 full nipple, 139.7", nipple(139.7)),
        "4518K65": ("KF-50 centring ring + FKM O-ring", ring.fuse(oring)),
        "5237K471": ("3 x 2 in concentric butt-weld reducer (B2)", red),
        "4518K74": ("KF-50 hinged wing-nut clamp", PT.kf_clamp(kf, 0.0)),
    }


def find_step(pn):
    for p in STEP_DIR.rglob("*"):
        if p.suffix.lower() in (".step", ".stp") and pn in p.name:
            return p
    return None


def principal_axis(shape):
    """Unit vector of the symmetry axis: the principal axis whose moment differs from the other two."""
    props = cq.occ_impl.shapes.GProp_GProps()
    from OCP.BRepGProp import BRepGProp
    BRepGProp.VolumeProperties_s(shape.wrapped, props)
    m = props.MatrixOfInertia()
    I = np.array([[m.Value(i, j) for j in (1, 2, 3)] for i in (1, 2, 3)])
    w, v = np.linalg.eigh(I)
    d = [abs(w[0] - w[1]) + abs(w[0] - w[2]), abs(w[1] - w[0]) + abs(w[1] - w[2]), abs(w[2] - w[0]) + abs(w[2] - w[1])]
    k = int(np.argmax(d))
    c = props.CentreOfMass()
    return v[:, k], np.array([c.X(), c.Y(), c.Z()])


def to_z(shape):
    ax, c = principal_axis(shape)
    s = shape.translate(cq.Vector(*(-c)))
    z = np.array([0, 0, 1.0])
    rot = np.cross(ax, z)
    if np.linalg.norm(rot) > 1e-9:
        ang = math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(ax, z))))))
        s = s.rotate(cq.Vector(0, 0, 0), cq.Vector(*rot), ang)
    return s


def best_overlap(vendor, ours):
    """Flip and slide the vendor solid along z for the largest overlap with ours."""
    bb_o = ours.BoundingBox()
    best = (-1.0, None)
    for flip in (False, True):
        v = vendor.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 180) if flip else vendor
        bb_v = v.BoundingBox()
        # coarse: align the tops, the bottoms and the centres, then a grid around each
        starts = [bb_o.zmax - bb_v.zmax, bb_o.zmin - bb_v.zmin, (bb_o.zmax + bb_o.zmin - bb_v.zmax - bb_v.zmin) / 2]
        for z0 in starts:
            for dz in np.arange(-3.0, 3.01, 0.5):
                vv = v.translate(cq.Vector(0, 0, z0 + dz))
                inter = ours.intersect(vv).Volume()
                if inter > best[0]:
                    best = (inter, (flip, z0 + dz))
    flip, z = best[1]
    for dz in np.arange(-0.5, 0.51, 0.1):
        v = vendor.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 180) if flip else vendor
        vv = v.translate(cq.Vector(0, 0, z + dz))
        inter = ours.intersect(vv).Volume()
        if inter > best[0]:
            best = (inter, (flip, z + dz))
    flip, z = best[1]
    v = vendor.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 180) if flip else vendor
    return v.translate(cq.Vector(0, 0, z)), best[0]


def section_xy(shape):
    """Outline points of a shape's half-section in the x-z plane (x >= 0)."""
    sec = shape.intersect(cq.Workplane("XZ").rect(400, 800).extrude(0.02, both=True).val())
    pts = []
    for e in sec.Edges():
        for t in np.linspace(0, 1, 12):
            p = e.positionAt(t)
            if p.x >= -1e-6:
                pts.append((p.x, p.z))
    return np.array(pts)


def main():
    if not STEP_DIR.exists():
        sys.exit(f"no vendor STEP folder at {STEP_DIR}; run bom/fetch_*.py or set VENDOR_STEP_DIR")
    rows = {}
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    items = mine()
    fig, axes = plt.subplots(1, len(items), figsize=(3.0 * len(items), 4.4))
    for ax, (pn, (label, ours)) in zip(axes, items.items()):
        path = find_step(pn)
        if path is None:
            rows[pn] = dict(part=label, status="vendor STEP not found")
            continue
        vendor = cq.importers.importStep(str(path)).val()
        if hasattr(vendor, "Solids") and len(vendor.Solids()) > 1:
            vendor = vendor.Solids()[0].fuse(*vendor.Solids()[1:])
        vendor = to_z(vendor)
        ours_z = to_z(ours)
        vv, inter = best_overlap(vendor, ours_z)
        Vv, Vo = vv.Volume(), ours_z.Volume()
        rows[pn] = dict(part=label, vendor_volume_mm3=round(Vv, 1), our_volume_mm3=round(Vo, 1),
                        volume_diff_pct=round(100 * (Vo - Vv) / Vv, 1), overlap_mm3=round(inter, 1),
                        vendor_only_pct=round(100 * (Vv - inter) / Vv, 1), ours_only_pct=round(100 * (Vo - inter) / Vv, 1),
                        vendor_bbox_mm=[round(x, 2) for x in (vv.BoundingBox().xlen, vv.BoundingBox().ylen, vv.BoundingBox().zlen)],
                        our_bbox_mm=[round(x, 2) for x in (ours_z.BoundingBox().xlen, ours_z.BoundingBox().ylen,
                                                           ours_z.BoundingBox().zlen)])
        try:
            a, b = section_xy(vv), section_xy(ours_z)
            ax.plot(a[:, 0], a[:, 1], ".", ms=1.2, color="tab:blue", label="vendor STEP")
            ax.plot(b[:, 0], b[:, 1], ".", ms=1.2, color="tab:orange", label="our CAD")
        except Exception:  # noqa: BLE001
            pass
        ax.set_aspect("equal")
        ax.set_title(f"{pn}\n{rows[pn]['volume_diff_pct']:+.1f} % vol, {rows[pn]['vendor_only_pct']:.1f} / "
                     f"{rows[pn]['ours_only_pct']:.1f} % unshared", fontsize=7)
        ax.tick_params(labelsize=6)
        print(pn, rows[pn], flush=True)
    axes[0].legend(fontsize=6, markerscale=6)
    fig.suptitle("Our CAD vs the vendor's STEP (half sections; McMaster's models are approximate)", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "vendor_check.png", dpi=130)
    plt.close(fig)
    (OUT / "vendor_check.json").write_text(json.dumps(rows, indent=1) + "\n")
    md = ["# Our CAD against the vendors' STEP models\n",
          "Volumes in mm3. 'Unshared' is the volume one model has and the other doesn't, after flipping and sliding the "
          "vendor model along the axis to the best overlap, as a % of the vendor's volume. The STEP files are McMaster's "
          "(approximate models) and are not in the repo.\n",
          "| Part no. | Part | vendor vol. | our vol. | difference | vendor-only | ours-only |", "|---|---|---:|---:|---:|---:|---:|"]
    for pn, r in rows.items():
        if "vendor_volume_mm3" in r:
            md.append(f"| {pn} | {r['part']} | {r['vendor_volume_mm3']:.0f} | {r['our_volume_mm3']:.0f} | "
                      f"{r['volume_diff_pct']:+.1f} % | {r['vendor_only_pct']:.1f} % | {r['ours_only_pct']:.1f} % |")
        else:
            md.append(f"| {pn} | {r['part']} | {r['status']} | | | | |")
    (OUT / "vendor_check.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
