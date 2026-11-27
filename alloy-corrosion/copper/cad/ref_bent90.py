"""Can a bent leak-free reference (the vendor's LF-2-Bent90) ride in the electrode cap?

On 2026-11-10 Innovative Instruments answered that a reference 16.6 mm long overall needs a bare
silver-wire lead, with no strain relief or pin, and sent a photo of their LF-2-Bent90: the 2 mm
LF-2 bent 90 degrees, with the usual strain relief and gold pin. Ben posted it on PR 180
(2026-11-11). This script draws two versions in the cap from cad_cu_cell.py and checks them:

- PHOTO: as photographed. Leg lengths read off the ruler in the photo (PHOTO_MEASURED below).
- CUSTOM: the photographed tip leg, the other leg cut to 6 mm, a bare silver wire out of its end.
  It needs one change to the cap: a 2.2 mm slot under the steel disc for the bent leg, in place of
  the 0.6 mm reference groove. The slot's floor sets the tip height, so the leg seats on it.

Writes electrode_cap_bent90.step/.stl (the cap with the slot), ag_agcl_ref_bent90.step/.stl (the
custom electrode, drawn seated), ref_bent90.json (dimensions, interference, clearances) and
ref-bent90.png. CadQuery 2.8, matplotlib.

    python ref_bent90.py        # about 30 s
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("cad_cu_cell", HERE / "cad_cu_cell.py")
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)
P = cc.P
cyl, boxs = cc.cyl, cc.boxs

# ------------------------------------------------------------------ the vendor's photo
# 1440 x 1920 px phone photo, electrode flat on paper under a ruler (cm marks upside down).
# Long cm ticks (centroids, px): 142.1, 317.5, 490.5, 662.0, 831.5, 1000.0, 1167.9, 1335.0, so the
# scale runs from 17.5 px/mm at the left to 16.7 at the right (the camera was not square on).
# Leg lengths are measured to the outside of the other leg, as a bent part is usually specified.
PHOTO_MEASURED = {
    "label_in_photo": "LF-2-Bent90",
    "scale_px_per_mm": {"x_135_to_318": 17.54, "x_318_to_490": 17.30},
    "tip_leg_mm": {"value": 17.2, "range": [16.9, 17.2],
                   "how": "outer face of the long leg (x 135.4 at the tip leg's centreline) to the tip (x 431-438), "
                          "integrated over the local ruler scale"},
    "barrel_od_mm": {"value": 1.95, "how": "the tip leg is 34 px tall at 17.4 px/mm; the vendor's 2.0 mm"},
    "bend": "tight: the inside corner is nearly sharp, the outside radius about 2 mm",
    "long_leg_mm": {"value": 34.0, "range": [32.6, 34.1],
                    "how": "top of the tip leg (y 578) to the strain relief (y 1174), 3.5 deg tilt; the ruler gives no "
                           "scale along y, so 17.5 px/mm is assumed, and the pin's width hints at up to 5 % more"},
    "strain_relief_mm": {"length": 15.5, "width": 5.7, "rows": [1174, 1445]},
    "pin_mm": {"length": 7.0, "diameter": 1.0, "rows": [1445, 1569]},
    "relief_plus_pin_mm": 22.5,
    "vendor_says_relief_plus_pin_mm": 20.0,
}

D = P["ref_d"]                 # 2.0 mm barrel
TIP_C = -P["ref_tip_w"]        # tip 3.0 mm below the skirt underside = 3.0 mm above the metal
FLOOR = P["cap_top"] - P["disc_t"] - P["glue_t"]   # recess floor, 14.87: the disc's tape sits on it
RC = 1.2                       # bend centreline radius: 0.2 mm inside, 2.2 mm outside, as tight as the photo's
WIRE_D = 0.5                   # silver wire diameter: not known yet (ask the vendor); 0.5 drawn
SLOT_W = 2.2                   # printed slot for the 2.0 mm leg

CUSTOM = {"tip_leg": 17.0, "tol": 0.5, "leg": 6.0}   # what to ask for (leg lengths to the outside of the other leg)
PHOTO = {"tip_leg": 17.0, "leg": 34.0, "relief": (15.5, 5.7), "pin": (7.0, 1.0)}


def bent_ref(tip_leg, leg, relief=None, pin=None):
    """C frame. Tip leg down the cap's axis, bend, then the other leg toward -x (the reference pin's side).
    tip_leg: tip to the top of the other leg; leg: outside of the tip leg (x +1) to the end of the leg."""
    z_h = TIP_C + tip_leg - D / 2          # the bent leg's centreline
    z_b = z_h - RC                         # the tip leg ends, the bend starts
    tip = cyl(D, TIP_C, z_b)
    bend = (cq.Workplane("XY", origin=(0, 0, z_b)).circle(D / 2)
            .revolve(90, (-RC, 0, 0), (-RC, -1, 0)).val())
    x_end = D / 2 - leg
    arm = cq.Solid.makeCylinder(D / 2, -RC - x_end, cq.Vector(-RC, 0, z_h), cq.Vector(-1, 0, 0))
    body = cc.union(tip, bend, arm)
    extras = {}
    x = x_end
    if relief:
        L, W = relief
        extras["relief"] = cq.Solid.makeCylinder(W / 2, L, cq.Vector(x, 0, z_h), cq.Vector(-1, 0, 0))
        x -= L
    if pin:
        L, W = pin
        extras["pin"] = cq.Solid.makeCylinder(W / 2, L, cq.Vector(x, 0, z_h), cq.Vector(-1, 0, 0))
        x -= L
    return body, extras, {"z_centreline": z_h, "z_top": z_h + D / 2, "z_bottom": z_h - D / 2,
                          "x_leg_end": x_end, "x_far_end": x}


def silver_wire(z_h, x_from):
    """The bare lead, straight from the leg's end to the mouth of the -x pin's 1.6 mm hole."""
    x_to = -P["pin_r"] + 0.8
    return cq.Solid.makeCylinder(WIRE_D / 2, x_from - x_to, cq.Vector(x_from, 0, z_h), cq.Vector(-1, 0, 0))


def cap_bent(z_h, x_end):
    """electrode_cap with a slot for the bent leg. The slot's floor is the leg's underside, so the
    leg seats on it and sets the tip height. The 0.6 mm wire groove deepens to the leg's centreline."""
    cap, floor, _ = cc.cap_body("clearance")
    z0 = z_h - D / 2
    slot = boxs(x_end - 1.0, -SLOT_W / 2, z0, D / 2 + 0.1, SLOT_W / 2, floor + 0.01)
    # under the bend: relief for a bend tighter or looser than drawn
    relief = boxs(-RC - 1.3, -SLOT_W / 2, z0 - 0.5, D / 2 + 0.1, SLOT_W / 2, z0 + 0.01)
    wire = boxs(-P["pin_r"], -0.6, z_h - 0.6, x_end - 0.9, 0.6, floor + 0.01)
    return cap.cut(slot).cut(relief).cut(wire).clean(), floor


def section_polys(shape, y=0.0, tol=0.03):
    """Triangles of the section of a solid by the plane y = const, as (x, z) polygons."""
    s = shape.translate(cq.Vector(0, -y, 0)).rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), -90)
    out = []
    try:
        faces = cq.Workplane("XY").add(s).section(0.0).faces().vals()
    except Exception:
        return out
    for f in faces:
        verts, tris = f.tessellate(tol)
        for t in tris:
            out.append([(verts[i].x, verts[i].y) for i in t])
    return out


def vol(a, b):
    try:
        return round(a.intersect(b).Volume(), 4)
    except Exception:
        return None


def main():
    p = P
    lid = cc.well_lid().translate(cq.Vector(0, 0, -p["lid_top"]))          # W -> C for a seated cap
    pads, eyelets, mags = cc.lid_extras()
    f_oring = cc.face_oring()[0].translate(cq.Vector(0, 0, -p["lid_top"]))
    cpn = cc.coupon().translate(cq.Vector(0, 0, -p["lid_top"]))
    cap0, floor, _ = cc.cap_body("clearance")
    carrier = cc.electrode_carrier()
    disc, ref_straight, coil, pins, steel = cc.electrodes()

    # ---- the custom bent reference and its cap
    ref_c, _, g_c = bent_ref(CUSTOM["tip_leg"], CUSTOM["leg"])
    wire_c = silver_wire(g_c["z_centreline"], g_c["x_leg_end"])
    cap_c, _ = cap_bent(g_c["z_centreline"], g_c["x_leg_end"])
    # ---- as photographed, in the unmodified cap (it can only leave through the cap's side)
    ref_p, ex_p, g_p = bent_ref(PHOTO["tip_leg"], PHOTO["leg"], PHOTO["relief"], PHOTO["pin"])

    cq.exporters.export(cq.Workplane().add(cap_c), str(HERE / "electrode_cap_bent90.step"))
    cq.exporters.export(cq.Workplane().add(cap_c), str(HERE / "electrode_cap_bent90.stl"), tolerance=0.02, angularTolerance=0.25)
    ref_w = cc.union(ref_c, wire_c)
    cq.exporters.export(cq.Workplane().add(ref_w), str(HERE / "ag_agcl_ref_bent90.step"))
    cq.exporters.export(cq.Workplane().add(ref_w), str(HERE / "ag_agcl_ref_bent90.stl"), tolerance=0.01, angularTolerance=0.2)

    # ---- checks
    coil_hole = cyl(0.6, p["ceiling_z"], floor, p["coil_r"], 0.0)
    pin_hole = cyl(1.6, p["pin_top_c"], floor, -p["pin_r"], 0.0)
    slot_only = boxs(g_c["x_leg_end"] - 1.0, -SLOT_W / 2, g_c["z_bottom"], D / 2 + 0.1, SLOT_W / 2, floor)
    custom = {
        "ask_for": {"tip_leg_mm": CUSTOM["tip_leg"], "tip_leg_tol_mm": CUSTOM["tol"], "other_leg_mm": CUSTOM["leg"],
                    "measured_to": "the outside of the other leg", "lead": "bare silver wire, at least 40 mm, straight out of the other leg's end",
                    "no": "strain relief or pin"},
        "seated_C_mm": {k: round(v, 3) for k, v in g_c.items()},
        "tip_above_metal_mm": round(TIP_C + p["lid_top"], 3),
        "tip_above_metal_if_tip_leg_is_mm": {f"{L:.1f}": round(g_c["z_bottom"] + D - L + p["lid_top"], 2)
                                             for L in (CUSTOM["tip_leg"] - CUSTOM["tol"], CUSTOM["tip_leg"] + CUSTOM["tol"])},
        "leg_top_below_recess_floor_mm": round(floor - g_c["z_top"], 3),
        "leg_top_below_disc_mm": round(floor + p["glue_t"] - g_c["z_top"], 3),
        "longest_tip_leg_that_fits_with_tip_at_3mm": round(floor - TIP_C, 3),
        "wire_from_leg_end_to_pin_hole_mouth_mm": round(g_c["x_leg_end"] - (-p["pin_r"] + 0.8), 2),
        "slot": {"width": SLOT_W, "floor_C_z": round(g_c["z_bottom"], 3), "x": [round(g_c["x_leg_end"] - 1.0, 2), round(D / 2 + 0.1, 2)],
                 "depth_below_recess_floor": round(floor - g_c["z_bottom"], 3)},
        "walls_mm": {"slot_to_coil_lead_hole": round(slot_only.distance(coil_hole), 3),
                     "slot_to_minus_x_pin_hole": round(slot_only.distance(pin_hole), 3),
                     "slot_to_carrier_socket_top": round(g_c["z_bottom"] - (p["ceiling_z"] + p["socket_h"]), 3)},
        "clearances_mm": {"reference_to_coil": round(ref_c.distance(coil), 3),
                          "reference_to_disc": round(ref_c.distance(disc), 3),
                          "wire_to_disc": round(wire_c.distance(disc), 3),
                          "reference_to_carrier": round(ref_c.distance(carrier), 3)},
        "interference_mm3": {"reference_vs_cap": vol(ref_c, cap_c), "reference_vs_carrier": vol(ref_c, carrier),
                             "reference_vs_disc": vol(ref_c, disc), "reference_vs_coil": vol(ref_c, coil),
                             "reference_vs_lid": vol(ref_c, lid), "wire_vs_cap": vol(wire_c, cap_c), "wire_vs_disc": vol(wire_c, disc),
                             "carrier_vs_cap": vol(carrier, cap_c), "coil_vs_cap": vol(coil, cap_c)},
        "cap_volume_removed_mm3": round(cap0.Volume() - cap_c.Volume(), 2),
        "disc_glue_area_lost_pct": round(100 * ((-(g_c["x_leg_end"] - 1.0) + D / 2 + 0.1) * SLOT_W) / (math.pi / 4 * p["recess_d"] ** 2), 1),
    }
    r_fl = p["flange_d"] / 2
    photo = {
        "drawn": PHOTO,
        "far_end_from_cap_axis_mm": round(-g_p["x_far_end"], 2),
        "beyond_flange_mm": round(-g_p["x_far_end"] - r_fl, 2),
        "leg_and_relief_band_C_z": [round(g_p["z_centreline"] - PHOTO["relief"][1] / 2, 2), round(g_p["z_centreline"] + PHOTO["relief"][1] / 2, 2)],
        "below_magnet_face_mm": {"leg": round(p["cap_top"] - g_p["z_top"], 2), "relief_top": round(p["cap_top"] - (g_p["z_centreline"] + PHOTO["relief"][1] / 2), 2)},
        "leg_vs_unmodified_cap_mm3": vol(ref_p, cap0),
        "why_not": [
            "the leg, strain relief and pin stick out of the cap's side: the gold pin ends this far from the axis",
            "the pin needs a socket and a lead: either a cable the head drags between wells, cups and the park cup, or a jumper back into the cap",
            "it runs 0.2-6 mm under the magnet face, the height of the capper's IR break beam, whose housings cad_check.json puts 3 mm outside the flange, so it could only point between them",
        ],
    }
    out = {"photo_measured": PHOTO_MEASURED, "custom": custom, "as_photographed": photo,
           "frame": "C: cap frame, origin at the centre of the skirt underside, z up; seated on a lid, C = W + (0, 0, 6); the metal is at C z -6"}
    (HERE / "ref_bent90.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({"custom": custom, "as_photographed": {k: v for k, v in photo.items() if k != "why_not"}}, indent=1))

    # ---- figure: sections through the pins (y = 0) and through the slot
    C = {"cap": "#c9c4b6", "lid": "#b9cfe0", "coupon": "#c58b5a", "ref": "#e8dcc0", "ref_edge": "#8a7a55", "relief": "#222222",
         "pin": "#c9a227", "disc": "#7d8187", "coil": "#9aa0a6", "carrier": "#d9d3c3", "wire": "#a8a9ad", "pads": "#b87333",
         "water": "#dceefa", "oring": "#5a3d2b"}

    def draw(ax, items, xlim, zlim, title):
        # liquid in the well (to the cap's ceiling), drawn first
        r_b = p["bore_d"] / 2
        ax.add_patch(plt.Rectangle((-r_b, -p["lid_top"] + p["throat_top"]), 2 * r_b, p["lid_top"] - p["throat_top"] + p["boss_h"] - 0.3,
                                   color=C["water"], zorder=0, lw=0))
        for shape, col, ec, z in items:
            polys = section_polys(shape)
            if polys:
                ax.add_collection(PolyCollection(polys, facecolors=col, edgecolors=col, linewidths=0.3, zorder=z))
        ax.set_xlim(*xlim)
        ax.set_ylim(*zlim)
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=10, loc="left")
        ax.set_xlabel("x in the cap (mm); the reference pin is at x −11", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.grid(alpha=0.25, lw=0.5)

    common = [(lid, C["lid"], None, 1), (cpn, C["coupon"], None, 1), (f_oring, C["oring"], None, 2),
              (pads.translate(cq.Vector(0, 0, -p["lid_top"])), C["pads"], None, 2), (carrier, C["carrier"], None, 3),
              (coil, C["coil"], None, 4), (disc, C["disc"], None, 3), (pins, C["pin"], None, 4)]
    fig = plt.figure(figsize=(13.0, 7.6))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.35, 1.0], height_ratios=[1.0, 1.0], wspace=0.12, hspace=0.32)
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])

    draw(ax1, [(cap0, C["cap"], None, 2)] + common + [(ref_p, C["ref"], None, 5), (ex_p["relief"], C["relief"], None, 5),
                                                     (ex_p["pin"], C["pin"], None, 5)],
         (-62, 34), (-13, 21), "A. As photographed (LF-2-Bent90, strain relief and pin): it can't stay inside the cap")
    ax1.axhline(p["cap_top"], color="#444", lw=0.8, ls="--")
    ax1.text(-61, p["cap_top"] + 0.6, "magnet face (capper)", fontsize=7, color="#444")
    ax1.annotate("", xy=(g_p["x_far_end"], -9.5), xytext=(-r_fl, -9.5), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax1.text((g_p["x_far_end"] - r_fl) / 2, -11.8, f"{-g_p['x_far_end'] - r_fl:.0f} mm past the cap's flange, then a cable or jumper from the pin",
             ha="center", fontsize=8)
    ax1.text(-23.5, g_p["z_top"] + 0.5, f"other leg about {PHOTO['leg']:.0f} mm", fontsize=8, ha="center")
    ax1.text(g_p["x_leg_end"] - PHOTO["relief"][0] / 2, g_p["z_centreline"] - 5.6,
             f"strain relief about {PHOTO['relief'][0]:.1f} x {PHOTO['relief'][1]:.1f}", fontsize=8, ha="center")
    ax1.text(g_p["x_far_end"] + 3.5, g_p["z_centreline"] + 1.6, "gold pin", fontsize=8, ha="center")
    ax1.text(15.5, 2.0, f"tip leg about {PHOTO['tip_leg']:.0f} mm,\nas in the photo", fontsize=8, ha="left")

    items_c = [(cap_c, C["cap"], None, 2)] + common + [(ref_c, C["ref"], None, 5), (wire_c, C["wire"], None, 6)]
    draw(ax2, items_c, (-37, 27), (-12.5, 19.0), "B. Custom: the same tip leg, the other leg cut to 6 mm, bare silver wire")
    ax2.annotate("", xy=(4.5, TIP_C), xytext=(4.5, g_c["z_top"]), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax2.annotate(f"tip leg {CUSTOM['tip_leg']:.1f} ± {CUSTOM['tol']:.1f},\ntip to the top of the leg", xy=(4.6, 6.0), xytext=(14.8, 6.0),
                 fontsize=7.5, va="center", arrowprops=dict(arrowstyle="-", lw=0.5, color="#555"))
    ax2.annotate("", xy=(D / 2, 17.3), xytext=(g_c["x_leg_end"], 17.3), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax2.plot([D / 2, D / 2], [g_c["z_top"], 17.6], color="#555", lw=0.4, ls=":")
    ax2.plot([g_c["x_leg_end"], g_c["x_leg_end"]], [g_c["z_top"], 17.6], color="#555", lw=0.4, ls=":")
    ax2.text((D / 2 + g_c["x_leg_end"]) / 2, 17.8, f"other leg {CUSTOM['leg']:.0f}", fontsize=7.5, ha="center")
    ax2.annotate("bare silver wire to\nthe −x (RE) pin's hole", xy=(-8.5, g_c["z_centreline"]), xytext=(-36.5, 8.0), fontsize=7.5,
                 arrowprops=dict(arrowstyle="-", lw=0.5, color="#555"))
    ax2.annotate(f"slot floor sets the height;\nleg top {floor - g_c['z_top']:.2f} under the recess", xy=(-3.0, g_c["z_bottom"]),
                 xytext=(-36.5, 1.5), fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=0.5, color="#555"))
    ax2.annotate("", xy=(-2.2, -p["lid_top"]), xytext=(-2.2, TIP_C), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax2.text(-2.5, -5.4, "3.0", fontsize=7.5, ha="right")
    ax2.text(-9.5, -11.0, "metal (coupon)", fontsize=7.5)
    ax2.text(14.8, -3.0, "lid, well and\nO-ring", fontsize=7.5)

    # C: top view of the cap's recess floor with the slot
    floor_cut = cap_c.intersect(boxs(-20, -20, floor - 3.6, 20, 20, floor - 0.0))
    top_polys = []
    try:
        for f in cq.Workplane("XY").add(cap_c).section(g_c["z_centreline"]).faces().vals():
            verts, tris = f.tessellate(0.03)
            top_polys += [[(verts[i].x, verts[i].y) for i in t] for t in tris]
    except Exception:
        pass
    ax3.add_collection(PolyCollection(top_polys, facecolors=C["cap"], edgecolors=C["cap"], linewidths=0.3, zorder=1))
    ref_top = []
    for f in cq.Workplane("XY").add(cc.union(ref_c, wire_c)).section(g_c["z_centreline"]).faces().vals():
        verts, tris = f.tessellate(0.02)
        ref_top += [[(verts[i].x, verts[i].y) for i in t] for t in tris]
    ax3.add_collection(PolyCollection(ref_top, facecolors=C["ref"], edgecolors=C["ref_edge"], linewidths=0.2, zorder=3))
    th = [2 * math.pi * k / 120 for k in range(121)]
    for r, ls in ((p["recess_d"] / 2, "--"), (p["flange_d"] / 2, "-")):
        ax3.plot([r * math.cos(t) for t in th], [r * math.sin(t) for t in th], color="#555", lw=0.7, ls=ls)
    for ang in p["pin_angles"]:
        x, y = cc.polar(p["pin_r"], ang)
        ax3.text(x, y - 2.6, "RE pin" if ang == 180 else "CE pin", ha="center", fontsize=7.5)
    ax3.set_xlim(-15, 15)
    ax3.set_ylim(-20, 15)
    ax3.set_aspect("equal")
    ax3.tick_params(labelsize=7)
    ax3.grid(alpha=0.25, lw=0.5)
    ax3.set_title(f"C. The cap cut at the leg's centreline (z {g_c['z_centreline']:.1f}), disc off", fontsize=10, loc="left")
    ax3.set_xlabel("x (mm)", fontsize=8)
    ax3.text(-14.5, -19.3, f"slot {SLOT_W} mm wide, its floor {floor - g_c['z_bottom']:.2f} mm below the recess floor;\n"
             f"{custom['walls_mm']['slot_to_coil_lead_hole']:.2f} mm of wall to the coil's lead hole", fontsize=7.5)
    del floor_cut

    fig.suptitle("A bent leak-free reference in the electrode cap (sections through the reference and the pins, cap seated)",
                 fontsize=11, y=0.995)
    fig.savefig(HERE / "ref-bent90.png", dpi=130, bbox_inches="tight")
    print("wrote ref-bent90.png")


if __name__ == "__main__":
    main()
