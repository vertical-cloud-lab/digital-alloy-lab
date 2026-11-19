"""Concept: an electrode cap that takes a stock 2 mm reference, with the steel disc on a side platform.

Ben's idea (PR 264, 2026-11-19): move the capper's steel disc off the cap's axis onto a platform
beside it, so a standard-length reference can stand out of the cap's top instead of fitting under
the disc. This script draws that cap around the stock Innovative Instruments LF-2 (2.0 mm PEEK
barrel, 63 mm overall with its strain relief and 1 mm gold pin), places it under the PAW-V2
electromagnet mount from its STEP file, measures the clearances, and renders the concept figure.
It is a concept for a decision, not a part to print: nothing here replaces electrode_cap.step.

Frames as in cad_cu_cell.py: C is the cap frame, origin at the centre of the skirt underside,
z up; seated on a lid, C = W + (0, 0, 6), and the metal is at C z -6. The platform's disc top
is kept at C z 16, the current cap's magnet contact, so every carried height stays as it is.

    pip install cadquery pyvista          # CadQuery 2.5, PyVista 0.49
    # the capper mount, pinned as in ../keyframes/README.md
    curl -sfL -o /tmp/byu-vcl-capper-cad/PAW-V2-ElectromagnetMount.step \\
      https://raw.githubusercontent.com/vertical-cloud-lab/byu-vcl/c129db521599fa86569174ff9fcf4aa205a9cf55/modules/electromagnetic-capper/cad/PAW-V2-ElectromagnetMount.step
    xvfb-run -a python ref_stock_concept.py --capper-cad /tmp/byu-vcl-capper-cad

Writes ref_stock_concept.json and ref-stock-concept.png.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cadquery as cq
import numpy as np

HERE = Path(__file__).resolve().parent

# ---- the stock reference (vendor page: 2.0 mm OD, PEEK, 63 mm overall, 1 mm gold pin).
# Barrel, strain relief and pin split as in the vendor's photo of the LF-2-Bent90
# (ref_bent90.json): relief 15.5 x 5.7 mm, pin 7 x 1.0 mm; the barrel takes the rest of 63 mm.
LF2 = {"od": 2.0, "overall": 63.0, "relief_len": 15.5, "relief_d": 5.7, "pin_len": 7.0, "pin_d": 1.0}
LF2["barrel"] = LF2["overall"] - LF2["relief_len"] - LF2["pin_len"]  # 40.5
TIP_C = -3.0            # tip 3.0 mm above the metal, as now
DISC_TOP_C = 16.0       # magnet contact, as now
OFFSET = 24.0           # cap axis to magnet axis, mm (the platform sits at +y)
BODY_TOP_C = 14.0       # cap body cut down 2 mm below the magnet face where it passes under the mount
COLLAR = (6.0, 18.0)    # a collar round the barrel on the cap's top: diameter, top C z
PLAT_D, PLAT_BOT = 28.0, 8.4   # the platform: a vial-cap top under the magnet
SOCKET = (2.6, 9.0)     # a 1 mm pin socket on a jumper lead: OD, length

# the PAW-V2 mount in its STEP frame: magnet axis (fitted), the tube's open end at z -43 (magnet end)
MOUNT_AXIS = (63.17, 6.53)
MOUNT_END_Z = -43.0
MAGNET_RECESS = 0.5     # the magnet's cavity is 20.5 mm for a 20 mm magnet


def cyl(d, z0, z1, x=0.0, y=0.0):
    return cq.Solid.makeCylinder(d / 2, z1 - z0, cq.Vector(x, y, z0))


def concept_cap():
    cap = cq.importers.importStep(str(HERE / "electrode_cap.step")).val()
    # cut the body down to BODY_TOP_C: no disc on the axis any more
    cap = cap.cut(cq.Solid.makeBox(60, 60, 10, cq.Vector(-30, -30, BODY_TOP_C)))
    # the collar and the reference bore through it
    cap = cap.fuse(cyl(COLLAR[0], BODY_TOP_C - 0.5, COLLAR[1]))
    # the platform under the magnet, with the vial cap's disc recess, and a web to the body
    plat = cyl(PLAT_D, PLAT_BOT, 15.37, 0, OFFSET)
    plat = plat.cut(cyl(25.4, 14.87, 16.0, 0, OFFSET))
    # the web stays at the body's height: it passes under the mount's open end
    web = cq.Solid.makeBox(12, OFFSET, BODY_TOP_C - PLAT_BOT, cq.Vector(-6, 0, PLAT_BOT))
    cap = cap.fuse(plat).fuse(web)
    # the reference bore, last, through the body, the web and the collar
    cap = cap.cut(cyl(2.05, 4.0, COLLAR[1] + 1))
    return cap.clean()


def lf2():
    b = LF2
    z0 = TIP_C
    barrel = cyl(b["od"], z0, z0 + b["barrel"])
    relief = cq.Solid.makeCone(b["relief_d"] / 2 * 0.6, b["relief_d"] / 2, b["relief_len"] * 0.25,
                               cq.Vector(0, 0, z0 + b["barrel"]))
    relief = relief.fuse(cyl(b["relief_d"], z0 + b["barrel"] + b["relief_len"] * 0.25, z0 + b["barrel"] + b["relief_len"]))
    pin = cyl(b["pin_d"], z0 + b["barrel"] + b["relief_len"], z0 + b["overall"])
    return barrel, relief, pin


def mount_in_C(capper_cad: Path):
    m = cq.importers.importStep(str(capper_cad / "PAW-V2-ElectromagnetMount.step")).val()
    # magnet end down (its STEP orientation); put the magnet face on the disc top
    face_C = DISC_TOP_C
    end_C = face_C - MAGNET_RECESS
    return m.translate(cq.Vector(-MOUNT_AXIS[0], OFFSET - MOUNT_AXIS[1], end_C - MOUNT_END_Z))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capper-cad", type=Path, required=True)
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()

    cap = concept_cap()
    disc = cyl(25.3, 15.0, DISC_TOP_C, 0, OFFSET)
    barrel, relief, pin = lf2()
    mount = mount_in_C(a.capper_cad)
    magnet = cyl(25.0, DISC_TOP_C + 0.0, DISC_TOP_C + 20.0, 0, OFFSET)
    sock = cyl(SOCKET[0], TIP_C + LF2["overall"] - 6.0, TIP_C + LF2["overall"] - 6.0 + SOCKET[1])
    carrier = cq.importers.importStep(str(HERE / "electrode_carrier.step")).val()
    coil = cq.importers.importStep(str(HERE / "pt_coil.step")).val()
    pins = cq.importers.importStep(str(HERE / "cap_pogo_pins.step")).val()
    lid = cq.importers.importStep(str(HERE / "well_lid.step")).val().translate(cq.Vector(0, 0, -6))
    mb = mount.BoundingBox()

    # clearances (mm); the mount is drawn as its STEP, the magnet as a 25 x 20 mm cylinder
    out = {
        "what": "concept only: a cap for the stock LF-2 with the steel disc on a platform beside the axis",
        "frame": "C: cap frame, origin at the centre of the skirt underside, z up; seated, C = W + (0, 0, 6); metal at C z -6",
        "stock_reference_drawn": {**LF2, "tip_C_z": TIP_C, "top_C_z": TIP_C + LF2["overall"],
                                  "source": "2in.com reference page: 2 mm OD, PEEK, 63 mm overall or custom, 1 mm gold pin; relief and pin from the LF-2-Bent90 photo"},
        "offset_cap_axis_to_magnet_axis_mm": OFFSET,
        "magnet_face_C_z": DISC_TOP_C,
        "mount_C_z": [round(mb.zmin, 2), round(mb.zmax, 2)],
        "reference_above_magnet_face_mm": round(TIP_C + LF2["overall"] - DISC_TOP_C, 2),
        "reference_above_mount_top_mm": round(TIP_C + LF2["overall"] - mb.zmax, 2),
        "with_socket_above_mount_top_mm": round(TIP_C + LF2["overall"] - 6.0 + SOCKET[1] - mb.zmax, 2),
        "clearance_mm": {
            "barrel_to_mount": round(barrel.distance(mount), 2),
            "relief_to_mount": round(relief.distance(mount), 2),
            "pin_socket_to_mount": round(sock.distance(mount), 2),
            "cap_body_to_mount": round(cap.cut(cyl(PLAT_D + 0.2, 0, 30, 0, OFFSET)).distance(mount), 2),
        },
        "interference_mm3": {
            "cap_vs_mount": round(cap.intersect(mount).Volume(), 3),
            "reference_vs_cap": round(barrel.intersect(cap).Volume(), 3),
            "reference_vs_carrier": round(barrel.intersect(carrier).Volume(), 3),
            "reference_vs_coil": round(barrel.intersect(coil).Volume(), 3),
            "cap_vs_lid_seated": round(cap.intersect(lid).Volume(), 3),
        },
        "platform_underside_above_lid_top_mm": PLAT_BOT,
        "platform_underside_above_boss_top_mm": round(PLAT_BOT - 4.0, 2),
        "cap_footprint_mm": {"along_offset": round(OFFSET + 14 + 14, 1), "across": 28.0, "was": "28 round"},
        "mass_g": {"cap_body_petg": round(cap.Volume() * 1.27e-3, 2), "steel_disc": round(disc.Volume() * 7.85e-3, 2),
                   "was_cap_body_petg": 8.5},
    }
    # the lift: hold-down and pins act at the cap axis, the magnet pulls at the platform
    lift_N = 2.44  # cad_check.json, electromagnet_must_lift_N: 2.31 N of hold-down (upper estimate) plus the cap's weight
    out["lift_moment_on_magnet_Nmm"] = round(lift_N * OFFSET, 1)
    out["lift_note"] = ("the 2.44 N the magnet lifts now acts 24 mm off the magnet's axis: a 59 N mm peel moment on the "
                        "disc. The P25/20 holds the disc over its 25 mm face; at a 0.09 mm gap at the far edge the pull is a "
                        "third of contact, so measure the pick-off on the bench before anything else")
    (HERE / "ref_stock_concept.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))

    if a.no_render:
        return
    render(cap, disc, (barrel, relief, pin), sock, mount, magnet, carrier, coil, pins, lid)


def mesh(shape, tol=0.05):
    import pyvista as pv
    v, t = shape.tessellate(tol, 0.2)
    V = np.array([[p.x, p.y, p.z] for p in v])
    T = np.hstack([np.full((len(t), 1), 3), np.array(t)]).ravel()
    return pv.PolyData(V, T)


INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"


def slice_x0(shape):
    """Faces of the solid cut by the plane x = 0 (through the cap and magnet axes), as paths in (y, z)."""
    from matplotlib.path import Path as MPath
    slab = cq.Solid.makeBox(0.002, 300, 300, cq.Vector(-0.001, -150, -150))
    cut = shape.intersect(slab)
    paths = []
    for f in cut.Faces():
        n = f.normalAt()
        if abs(n.x) < 0.99 or f.Center().x < 0:
            continue
        verts, codes = [], []
        for w in [f.outerWire()] + f.innerWires():
            pts = []
            for e in w.Edges():
                k = 24 if e.geomType() != "LINE" else 2
                seg = [e.positionAt(t / (k - 1)) for t in range(k)]
                if pts and (seg[0] - pts[-1]).Length > 1e-6 and (seg[-1] - pts[-1]).Length < (seg[0] - pts[-1]).Length:
                    seg = seg[::-1]
                pts.extend(seg)
            yz = [(q.y, q.z) for q in pts]
            verts += yz + [yz[0]]
            codes += [MPath.MOVETO] + [MPath.LINETO] * (len(yz) - 1) + [MPath.CLOSEPOLY]
        paths.append(MPath(verts, codes))
    return paths


def render(cap, disc, ref, sock, mount, magnet, carrier, coil, pins, lid):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import PathPatch
    import pyvista as pv
    pv.OFF_SCREEN = True
    barrel, relief, pin = ref
    coupon = cq.importers.importStep(str(HERE / "coupon_20x20x6.step")).val().translate(cq.Vector(0, 0, -6))
    oring = cq.importers.importStep(str(HERE / "face_oring_006.step")).val().translate(cq.Vector(0, 0, -6))

    # ---- left: the carried cap in 3D, lifted 14 mm off its lid
    top = TIP_C + LF2["overall"] - 6.0 + SOCKET[1]
    pts = np.array([[0, 0, top], [-2, -1, top + 4], [-7, -2, top - 4], [-10, -2, 40], [-11, -1.5, 24],
                    [-11, 0, BODY_TOP_C + 0.5]])
    lift = 14.0
    wire = pv.Spline(pts + [0, 0, lift], 80).tube(radius=0.45)
    p = pv.Plotter(window_size=(1100, 1250))
    p.set_background("white")
    T = lambda sh: sh.translate(cq.Vector(0, 0, lift))
    for sh, col, op in [(T(cap), "#e8e4d8", 1), (T(disc), "#8c9399", 1), (T(barrel), "#6b5a4a", 1), (T(relief), "#2b2b2b", 1),
                        (T(pin), "#d4a72c", 1), (T(sock), "#b03a2e", 1), (T(carrier), "#c9c2b0", 1), (T(coil), "#b9bec4", 1),
                        (T(pins), "#c8a24a", 1), (T(mount), "#8fb3d9", 0.45), (T(magnet), "#5d6670", 0.85),
                        (lid, "#d9cfb8", 1), (coupon, "#c07a4a", 1), (oring, "#5a3a2a", 1)]:
        p.add_mesh(mesh(sh), color=col, opacity=op, smooth_shading=False, specular=0.25)
    p.add_mesh(wire, color="#b03a2e")
    p.camera.position = (165, -190, 120)
    p.camera.focal_point = (0, 8, 32)
    p.camera.up = (0, 0, 1)
    p.camera.zoom(1.15)
    img = p.screenshot(return_img=True)
    p.close()

    # ---- right: the seated cap with the magnet on its disc, cut at x = 0 through both axes
    fig = plt.figure(figsize=(15, 8.6))
    a0 = fig.add_axes([0.0, 0.02, 0.42, 0.9])
    a0.imshow(img)
    a0.axis("off")
    a0.set_title("Carried: the magnet holds the platform's disc;\nthe stock LF-2 stands beside the mount",
                 fontsize=11, color=INK, loc="left")
    a1 = fig.add_axes([0.45, 0.07, 0.53, 0.83])
    up6 = lambda sh: sh.translate(cq.Vector(0, 0, 6))  # C -> W
    parts = [(coupon.translate(cq.Vector(0, 0, 6)), "#b89a8a"), (lid.translate(cq.Vector(0, 0, 6)), "#e9a47c"),
             (oring.translate(cq.Vector(0, 0, 6)), "#1d1d1d"), (up6(cap), "#efe9e2"), (up6(carrier), "#9c9b97"),
             (up6(coil), "#9ea3a8"), (up6(disc), "#8d9196"), (up6(barrel), "#6b5a4a"), (up6(relief), "#2b2b2b"),
             (up6(pin), "#d4a72c"), (up6(sock), "#b03a2e"), (up6(mount), "#8fb3d9"), (up6(magnet), "#5d6670")]
    for sh, col in parts:
        for path in slice_x0(sh):
            a1.add_patch(PathPatch(path, facecolor=col, edgecolor=INK, lw=0.4))
    a1.set_xlim(-24, 56)
    a1.set_ylim(-8, 78)
    a1.set_aspect("equal")
    a1.set_xlabel("y, mm (cap axis at 0, magnet axis at %.0f)" % OFFSET, fontsize=9, color=INK2)
    a1.set_ylabel("height above the metal, mm", fontsize=9, color=INK2)
    a1.tick_params(labelsize=8, colors=INK2)
    for sp in a1.spines.values():
        sp.set_color(MUTED)
    a1.set_title("Seated, with the magnet on the disc: cut through both axes", fontsize=11, color=INK, loc="left")

    def dim(x0, y0, x1, y1, text, tx, ty, ha="left"):
        a1.annotate("", xy=(x0, y0), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.7, shrinkA=0, shrinkB=0))
        a1.text(tx, ty, text, fontsize=8.5, color=INK, ha=ha, va="center")

    W = 6.0
    face = DISC_TOP_C + W
    mtop = 58.5 + W
    rtop = TIP_C + LF2["overall"] + W
    for yy in (0.0, OFFSET):
        a1.axvline(yy, color=MUTED, lw=0.6, ls="-.", zorder=0)
    dim(0, 73, OFFSET, 73, "%.0f mm, cap axis to magnet axis" % OFFSET, OFFSET + 1.0, 73)
    a1.axhline(face, color=MUTED, lw=0.5, ls=":")
    a1.text(55, face - 1.6, "magnet face", fontsize=8, color=INK2, ha="right")
    a1.axhline(mtop, color=MUTED, lw=0.5, ls=":")
    a1.text(55, mtop + 1.2, "top of the PAW-V2 mount", fontsize=8, color=INK2, ha="right")
    dim(-4, face, -4, rtop, "%.0f mm of reference\nabove the\nmagnet face" % (rtop - face), -5, (face + rtop) / 2, ha="right")
    a1.text(-23, 76, "its pin ends %.1f mm above\nthe mount's top, %.1f mm\nwith a socket on it" %
            (rtop - mtop, rtop - 6.0 + SOCKET[1] - mtop), fontsize=8.5, color=INK, ha="left", va="top")
    dim(2.85, 52, 24 - 14.5, 52, "6.6 mm", 4.0, 54.5)
    a1.text(-23, 9.5, "tip 3.0 mm\nabove the metal", fontsize=8.5, color=INK)
    a1.annotate("", xy=(0, 3), xytext=(-12, 9), arrowprops=dict(arrowstyle="->", color=INK2, lw=0.6))
    a1.text(30, 9.0, "platform: a vial cap's top\nwith the steel disc", fontsize=8.5, color=INK)
    a1.text(-23, 30, "cap body 1.5 mm\nunder the mount", fontsize=8.5, color=INK, ha="left")
    fig.text(0.01, 0.005, "Concept only (ref_stock_concept.py). LF-2 as the vendor lists it: 2.0 mm PEEK, 63 mm with its "
             "strain relief and 1 mm gold pin. PAW-V2 mount from its STEP, magnet end down. Lid and coupon as in cad/.",
             fontsize=8, color=MUTED)
    fig.savefig(HERE / "ref-stock-concept.png", dpi=110)


if __name__ == "__main__":
    main()
