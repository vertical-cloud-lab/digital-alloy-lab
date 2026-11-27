"""The in-situ monitoring hardware drawn into the low-profile model as real parts (issue #260, PR 281; monitoring/mechanics.md).

monitoring_spec.py says where each port, window and instrument goes; this file draws them and cuts the holes they need:
  * LW, left-wall viewport: the bore, window seat, clamp-ring holes and purge port exactly as the fabrication worker programmed
    them in setup C (analysis/monitoring/fab/frame_features.py, imported here, so the model and the CAM share one geometry); the
    Ø40 x 4 window flat on the wall between two FKM flat gaskets, the clamp ring, the cover slide and its clip on the left liner
    (with the liner's hole), the argon purge (SAE-4 bored-through fitting, 1/8 in. 316 tube through the wall, flattened tip over
    the slide, needle valve outside), and the Chronos 2.1-HD with lens and filters on a tilt block and a T-slot post;
  * BW, back-wall light window: the obround slot, rectangular seat and clamp holes (frame_features again), the window, its
    gaskets and clamp frame, the lower back liner's left piece shortened, and the 850 nm LED light outside on the sight line (an
    M850D3 imaged onto the plate by an ACL25416U-B in an SM1L05, on a finned heat sink, clamp and L bracket: _bw_light());
  * LP, steep lid port: a bore normal to the lid sized to pass the clear aperture across the lid, an adapter boss whose window
    sits square to the line of sight (optics.md §0 item 10), the cover slide in the boss under the window, the face O-ring, the
    IMX296 camera with its 50 mm lens and filters, and the cut-out in the optics bridge the camera passes through;
  * the coaxial branch as a 30 mm cage (monitoring_spec.COAX, optics.md §2): the existing photodiode chain behind cube 1 is
    replaced by cube 2 (DMSP950, camera arm to -y), cube 3 (DMLP805: photodiode A to -y, photodiode B to -x), lens tubes,
    cage rods and plates, the IMX296 coaxial camera and two PDA36A2s, a beam trap on cube 1's far port, and posts to the bridge;
  * the AE path (monitoring.md §5.4): a Ø2 mm 316 waveguide from the plate's spigot down through the heater block, both
    radiation shields and the piston head's wire hole and down the hollow rod, its cold end screwed into the rod end's bore
    floor; the AE sensor in a strap clamp on the rod end's back face (outside the gas boundary, <= ~75 C); the preamp on the
    process base plate;
  * the PicoScope 4444 and the sync breakout box on a bracket on the rack's outer side (sync-and-data.md §2.1 puts them in the
    4U drawer if its layout has room; the drawer is an envelope in the model, so they are drawn beside it).

Hook: lpbf_low.build(monitoring=True), or LPBF_MONITORING=1 in the environment for scripts that call build() unchanged
(interference.py, render_low.py, ...). By default (monitoring=None and no environment variable) nothing changes.

Every part is tagged "monitoring". Vendor parts are envelopes from their published dimensions; where a dimension was not read
off a drawing, the part's name or the comment says "envelope".
"""
from __future__ import annotations

import math
import pathlib
import sys

import cadquery as cq
import numpy as np

import module_params as MP
import monitoring_spec as MS

V = cq.Vector
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "analysis" / "monitoring" / "fab"))
import frame_features as FF  # noqa: E402

TAG = ("monitoring",)
REPORT: dict = {}          # what apply() decided (bores, cut-outs, positions); render and the note read it


def _unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def _frame(axis):
    """an orthonormal frame (a, up, side) with a along `axis` and `up` as close to +z as it can be"""
    a = _unit(axis)
    up = np.array([0.0, 0.0, 1.0]) - a[2] * a
    if np.linalg.norm(up) < 1e-6:
        up = np.array([0.0, 1.0, 0.0]) - a[1] * a
    up = _unit(up)
    side = np.cross(up, a)
    return a, up, side


def _local(shape, origin, a, up):
    """move a shape drawn in local coordinates (local z along a, local x along up) to `origin`"""
    return shape.moved(cq.Location(cq.Plane(origin=V(*map(float, origin)), xDir=V(*map(float, up)), normal=V(*map(float, a)))))


def _cyl_ax(r, p0, a, length):
    return cq.Solid.makeCylinder(r, length, V(*map(float, p0)), V(*map(float, a)))


def _tube_ax(ro, ri, p0, a, length):
    return _cyl_ax(ro, p0, a, length).cut(_cyl_ax(ri, np.asarray(p0) - 0.01 * np.asarray(a), a, length + 0.02))


def _find(parts, prefix):
    out = [p for p in parts if p.name.startswith(prefix)]
    if not out:
        raise KeyError(prefix)
    return out


def _cut(parts, prefix, tools, must=True):
    hit = [p for p in parts if p.name.startswith(prefix)]
    if must and not hit:
        raise KeyError(prefix)
    for p in hit:
        s = p.shape
        for t in tools:
            s = s.cut(t)
        p.shape = s.clean() if hasattr(s, "clean") else s
    return hit


# ======================================================================================================== LW: left-wall port
def _lw(parts, add, h):
    C, box, cyl, tube, comp, fuse = h.C, h.box, h.cyl, h.tube, h.comp, h.fuse
    cuts, info, g = FF.lw_features(None)
    _cut(parts, "Process chamber body", [s for _, s in cuts])
    s = MS.VIEWPORTS["LW"]
    win = s["window"]
    yc, zc = info["bore"]["centre_yz"]
    R = info["bore"]["d"] / 2
    x_out = -FF.OUTER["x"]
    seat_depth = info["seat"]["depth"]
    rw = win["d"] / 2
    gk = FF.GASKET
    x_floor = x_out + seat_depth                                     # seat floor (the window's inner side sits on a gasket there)
    # window stack, outside in: flat ring 0.75 | window | gasket 0.75 on the seat floor
    add("LW viewport gasket and flat ring (2 x FKM 75A sheet, 1.0 mm squeezed to 0.75; ID = the Ø%.0f bore)" % (2 * R),
        comp([tube(rw - 0.05, R + 0.5, (x_floor, yc, zc), "-x", gk), tube(rw - 0.05, R + 0.5, (x_out + gk, yc, zc), "-x", gk)]),
        C["black"], 5, (-200, 0, 0), mat="fkm", bom="M0-06", tags=TAG)
    add(f"LW viewport window (Edmund 36-983, Ø{win['d']:.0f} x {win['t']:.0f} mm UV fused silica, NIR I AR; flat on the wall's outer face)",
        cyl(rw, (x_floor - gk, yc, zc), "-x", win["t"]), C["glass"], 5, (-220, 0, 0), mat="fused_silica", bom="M0-01", opacity=0.45, tags=TAG)
    cr = info["clamp_ring"]
    ring = tube(cr["od"] / 2, cr["id"] / 2, (x_out, yc, zc), "-x", 6.35)
    for (y, z) in cr["holes_yz"]:
        ring = ring.cut(cyl(2.25, (x_out + 1, y, z), "-x", 9.0))
    if cr.get("flat"):                       # flat toward the plate-height through-beam's fibre head (frame_features.FIBRE_HEAD)
        fl = cr["flat"]
        uy, uz = fl["dir_yz"]
        ang = math.degrees(math.atan2(uz, uy))
        cutter = box(x_out - 10, x_out + 1, fl["dist_mm"], fl["dist_mm"] + 40, -40, 40).rotate(V(0, 0, 0), V(1, 0, 0), ang)
        ring = ring.cut(cutter.translate(V(0, yc, zc)))
    add(f"LW window clamp ring (6061, 1/4 in. plate, Ø{cr['od']:.0f} x Ø{cr['id']:.0f}, 4 x M4 on Ø{cr['bolt_circle_d']:.0f}, a flat clear of the "
        f"through-beam's fibre head; bottoms on the wall face)",
        ring, C["anod"], 5, (-240, 0, 0), mat="al6061", bom="M0-13", tags=TAG)
    # cover slide on the liner's inner face, centred on the sight line, and its sheet clip
    c, d = np.array(s["centre"], float), np.array(MS.axis_to_target(s["centre"]))
    x_lin_in = -FF.INNER["x"] + FF.LINER["gap"] + FF.LINER["t"]   # -139.4
    t_sl = (x_lin_in + 0.75 - c[0]) / d[0]
    ps = c + t_sl * d
    sl = MS.VIEWPORTS["LW"]["slide"]
    sl_t = 1.5                                                       # the bought slide (BOM M0-02: Precitec Ø30 x 1.5)
    add(f"LW cover slide (Ø{sl['d']:.0f} x {sl_t} mm fused silica, laser-head protective glass; consumable)",
        cyl(sl["d"] / 2, (x_lin_in, ps[1], ps[2]), "x", sl_t), C["glass"], 5, (160, 0, 0), mat="fused_silica", bom="M0-02", opacity=0.5, tags=TAG)
    lh = info["liner_hole"]
    xc_clip = x_lin_in + sl_t
    clip = box(xc_clip, xc_clip + 0.5, ps[1] - 18, ps[1] + 18, ps[2] - 18, ps[2] + 18).cut(cyl(lh["d"] / 2, (xc_clip - 1, ps[1], ps[2]), "x", 3))
    clip = fuse([clip, box(x_lin_in, xc_clip + 0.5, ps[1] - 18, ps[1] - 16.5, ps[2] - 18, ps[2] + 18),
                 box(x_lin_in, xc_clip + 0.5, ps[1] + 16.5, ps[1] + 18, ps[2] - 18, ps[2] + 18)])
    add("LW cover-slide clip (0.5 mm 316, folded sheet on the left liner; Ø%.0f opening)" % lh["d"], clip, C["ss"], 5, (160, 0, 0),
        mat="ss316l", bom="M0-15", tags=TAG)
    # the liner's holes: the sight line's and the purge tube's
    py, pz = info["purge_port"]["yz"]
    _cut(parts, "Lift-out wall liner, left", [cyl(lh["d"] / 2, (-FF.INNER["x"] - 1, lh["centre_yz"][0], lh["centre_yz"][1]), "x", 3),
                                              cyl(2.5, (-FF.INNER["x"] - 1, py, pz), "x", 3)])
    # purge: SAE-4 x 1/8 in. bored-through fitting in the wall's port, 1/8 in. 316 tube through the Ø4 passage, bent down inside,
    # its flattened tip 3 mm above the clip, blowing down across the slide; a needle valve on the tube outside
    fit = fuse([h.cq.Workplane("YZ").polygon(6, 16.5).extrude(-9.0).val().translate(V(x_out - 1.0, py, pz)),
                cyl(5.5, (x_out, py, pz), "-x", 1.0), cyl(4.0, (x_out - 10.0, py, pz), "-x", 10.0)])
    add("LW purge fitting (SAE-4 7/16-20 O-ring boss x 1/8 in. tube, 316, bored through; envelope)", fit, C["ss"], 5, (-200, 0, 0),
        mat="ss316l", mass_kg=0.03, bom="M0-12", tags=TAG)
    x_in_tube = x_lin_in + 2.4
    tube_in = h.polyline_pipe([(x_out - 16.0, py, pz + 34.0), (x_out - 16.0, py, pz + 6.0), (x_out - 12.0, py, pz), (x_lin_in + 0.5, py, pz),
                               (x_in_tube, py, pz - 4.0), (x_in_tube, py, ps[2] + 21.0)], 1.5875, 6)
    tip = box(x_in_tube - 0.6, x_in_tube + 0.6, py - 3.0, py + 3.0, ps[2] + 18.5, ps[2] + 21.0)
    add("LW purge tube (1/8 in. 316, through the wall's Ø4 passage; bent down inside, tip flattened to a 6 x 1 slot over the slide)",
        comp([tube_in, tip]), C["ss"], 5, (-200, 0, 0), mat="ss316l", mass_kg=0.02, bom="M0-12", tags=TAG)
    nv = fuse([box(x_out - 25.0, x_out - 7.0, py - 9.0, py + 9.0, pz + 34.0, pz + 69.0), cyl(5.0, (x_out - 25.0, py, pz + 51.5), "-x", 18.0)])
    add("LW purge needle valve (1/8 in. tube, 316, metering; envelope); argon from the purge manifold (route not drawn)", nv, C["ss"], 5,
        (-260, 0, 0), mat="misc", mass_kg=0.12, bom="M0-08", tags=TAG)
    REPORT["LW"] = dict(bore_d=info["bore"]["d"], seat=info["seat"], clamp_ring=cr, purge=info["purge_port"], liner_hole=lh,
                        slide_centre=ps.round(2).tolist(), window_tilt_deg=info["sight_vs_wall_normal_deg"])
    _chronos(parts, add, h, c, d, x_out - 6.35)


def _chronos(parts, add, h, c, d, x_face):
    """Chronos 2.1-HD + Kowa LM50JC10M + filters on the LW sight line; tilt block on a T-slot post from the process base plate"""
    C, box, fuse, comp = h.C, h.box, h.fuse, h.comp
    a, up, side = _frame(-d)                                         # outward along the sight line
    t0 = (x_face - c[0]) / a[0]
    sc = MS.SIDE_CAMERA
    L, W, H = sc["body_mm"]
    so = sc["standoff_mm"]
    t_f = 1.0 + 17.0 * math.sqrt(max(0.0, 1.0 - a[0] ** 2))         # the holder's rim, tilted to the ring's face, stays 1 mm off it
    p_f = c + (t0 + t_f) * a
    filt = _cyl_ax(17.0, p_f, a, so - t_f)
    lens_l, lens_r = 50.0, 16.0
    p_l = c + (t0 + so) * a
    lens = _cyl_ax(lens_r, p_l, a, lens_l)
    p_b = c + (t0 + so + lens_l) * a
    body = _local(box(-H / 2, H / 2, -W / 2, W / 2, 0.0, L), p_b, a, up)
    add("Side camera filters: FBH850-10 + FESH1000 in an SM1 holder on the lens (envelope)", filt, C["black"], 12, (-200, 0, 0),
        mat="misc", mass_kg=0.05, bom="M7-03", tags=TAG)
    add("Side camera lens (Kowa LM50JC10M, 50 mm C-mount, focuses at 176 mm; envelope Ø32 x 50)", lens, C["black"], 12, (-220, 0, 0),
        mat="misc", mass_kg=0.2, bom="M7-02", tags=TAG)
    add(f"Side high-speed camera (Kron Chronos 2.1-HD, {L:.0f} x {W:.0f} x {H:.1f} mm) on the LW sight line", body, C["motor"], 12,
        (-260, 0, 0), mat="misc", mass_kg=sc["mass_kg"], bom="M7-01", tags=TAG)
    # bracket (analysis/out/monitoring/mech/checks.md §3): a 5/8 in. (15.9 mm) x 80 mm 6061 plate reaching 139 mm from the left wall
    # to the camera's centre of mass (f1 169 Hz), under the camera's middle; its root is an angle flange bolted to the floor
    # plate's left edge (z -20..4: under the LW clamp ring, which reaches down to z 5.2). The plate runs at z -15.9..0, below the
    # frame's skirt, at y -78..2 (the door drive's bracket takes y <= -80), notched round the through-beam's fibre head. A fixed wedge (the sight
    # line's 12.9 deg, and its 7.3 deg azimuth by turning the camera on it) carries the camera on its 1/4-20 thread.
    tm = t0 + so + lens_l + L / 2
    pm = c + tm * a
    x_w = -FF.OUTER["x"]
    y0b, y1b = -78.0, 2.0                                            # clear of the door drive's bracket on the same face (y <= -80)
    reach = 139.0
    plate = box(x_w - reach - 45.0, x_w, y0b, y1b, -15.9, 0.0)
    root = box(x_w - 15.9, x_w, y0b, y1b, -20.0, 4.0)
    wedge = _local(box(-H / 2 - 80.0, -H / 2, -30.0, 30.0, -40.0, 40.0), pm, a, up).intersect(box(-1e4, 1e4, y0b, y1b, 0.0, 1e4))
    fy, fz = FF.FIBRE_HEAD["yz"]                                     # notch round the through-beam's fibre head
    notch = box(x_w - 25.0, x_w + 0.1, fy - FF.FIBRE_HEAD["flange_r"] - 2.0, fy + FF.FIBRE_HEAD["flange_r"] + 2.0, fz - 8.5, fz + 8.5)
    add("Side camera bracket (6061, 5/8 in. x 80 mm plate, 139 mm reach, on an angle root bolted to the floor plate's left edge)",
        fuse([plate, root]).cut(notch), C["alu_dark"], 12, (-200, 0, 0), mat="al6061", bom="M7-08", tags=TAG)
    add("Side camera wedge (6061, fixed 13 deg; the camera's 1/4-20 thread screws into it)", wedge, C["anod"], 12, (-220, 0, 0),
        mat="al6061", bom="M7-08", tags=TAG)
    REPORT["chronos"] = dict(lens_front=p_l.round(1).tolist(), body_back=(p_b + L * a).round(1).tolist(), camera_mid=pm.round(1).tolist(),
                             bracket=dict(plate="15.9 x 80 x %.0f" % (reach + 45.0), y=(y0b, y1b), z=(-15.9, 0.0), root_z=(-20.0, 4.0),
                                          com_reach_mm=round(float(x_w - pm[0]), 1)))


# ======================================================================================================== BW: back-wall window
def _bw(parts, add, h):
    C, box, cyl, comp, fuse = h.C, h.box, h.cyl, h.comp, h.fuse
    cuts, info, g = FF.bw_features(None, 0.0)
    _cut(parts, "Process chamber body", [s for _, s in cuts])
    y_out = FF.OUTER["y"]
    st = info["seat"]
    sl = info["slot"]
    e1, e2 = np.array(sl["end_centres_xz"][0]), np.array(sl["end_centres_xz"][1])
    u = _unit(e2 - e1)
    n = np.array([-u[1], u[0]])
    mid = 0.5 * (e1 + e2)
    sc = mid + FF.SEAT_SHIFT * u
    gk = FF.GASKET
    y_floor = y_out - st["depth"]
    Lw, Ww = st["L"] - 0.3, st["W"] - 0.3

    def rrect(L_, W_, r_, y0, t):
        return cq.Solid.extrudeLinear(FF.rrect_face_y(sc, u, L_, W_, r_, y0), V(0, t, 0))
    open_ = cq.Solid.extrudeLinear(FF.stadium_face_y(e1, e2, sl["radius"] + 0.5, y_floor - 1.0), V(0, 3.0 + st["depth"], 0))
    gas = comp([rrect(Lw, Ww, 3.8, y_floor, gk).cut(open_), rrect(Lw, Ww, 3.8, y_out - gk, gk).cut(open_)])
    add("BW window gasket and flat ring (2 x FKM 75A sheet, 1.0 mm squeezed to 0.75)", gas, C["black"], 5, (0, 200, 0), mat="fkm",
        bom="M0-06", tags=TAG)
    add(f"BW light window ({Lw:.1f} x {Ww:.1f} x 3 mm UV fused silica, corners chamfered; flat on the back wall)",
        rrect(Lw, Ww, 2.0, y_floor + gk, 3.0), C["glass"], 5, (0, 220, 0), mat="fused_silica", bom="M0-03", opacity=0.45, tags=TAG)
    fr = rrect(st["L"] + 18.0, st["W"] + 22.0, 6.0, y_out, 4.76).cut(cq.Solid.extrudeLinear(
        FF.stadium_face_y(e1, e2, sl["radius"] + 1.0, y_out - 1.0), V(0, 7.0, 0)))
    for (x, z) in info["clamp_frame"]["holes_xz"]:
        fr = fr.cut(cyl(2.25, (x, y_out - 1, z), "y", 8.0))
    # keep the frame on the wall's flat face (|x| <= 148) and above the frame's bottom edge (z -3.9)
    fr = fr.intersect(box(-FF.FLAT_X + 0.5, 0.0, y_out - 1, y_out + 10, -3.4, 200.0))
    for q in parts:                          # 1 mm clear of the inlet plenum's flange and of the recoater sensor clamp above
        if q.name.startswith("Cross-flow inlet plenum") or q.name.startswith("Recoater sensor clamps"):
            for sol in q.shape.Solids():
                b = sol.BoundingBox()
                if b.xmax > -160 and b.xmin < -60:
                    fr = fr.cut(box(b.xmin - 1, b.xmax + 1, y_out - 2, y_out + 12, b.zmin - 1, b.zmax + 1))
    add("BW window clamp frame (6061, 3/16 in. plate, 3 x M4; trimmed to the wall's flat face and bottom edge)", fr, C["anod"], 5,
        (0, 240, 0), mat="al6061", bom="M0-14", tags=TAG)
    # lower back liner, left piece: starts past the slot's opening (frame_features' liner range)
    x_new = info["liner"]["x_range"][1]
    for p in _find(parts, "Lift-out wall liner, back lower left"):
        p.shape = p.shape.intersect(box(x_new, 0.0, -1e3, 1e3, -1e3, 1e3))
        p.name = p.name.replace("(0.5 mm 316L", f"(starts at x {x_new:.1f}, clear of the BW opening; 0.5 mm 316L")
    s = MS.VIEWPORTS["BW"]
    REPORT["BW"] = dict(centre=list(s["centre"]), slot=sl, seat=st, liner_x0=x_new)


# ======================================================================================================== BW light
# The side camera's light (monitoring/optics.md §4.1; analysis/monitoring/optics/bw_light.py traces it and does the light budget,
# heat and eye safety): a Thorlabs M850D3 (850 nm LED, 1 x 1 mm die on a Ø22 metal-core board) on a custom finned 6061 heat sink,
# imaged onto the plate by an ACL25416U-B aspheric condenser in an SM1L05 lens tube, on the BW sight line; a split clamp on the heat
# sink's collar hangs from an L bracket screwed to the back wall above the BW clamp frame. Positions are along the outward sight line,
# t = 0 at the port centre on the wall's outer face. Dimensions read off Thorlabs' drawings on 2026-11-27: M850D3 spec sheet
# MTN005519-S01 (board Ø22.0 x 1.6, 2.8 over the LED, 2 x Ø2.0 holes on Ø19); ACL25416U-B drawing and Zemax file (Ø25.4, CT 14.0,
# S1 R 8.818 k -0.99917 + A4..A10, S2 R -70); SM1L05 drawing (Ø30.5 x 16.5, 12.7 internal thread, 3.0 external); SM1RR (2.0 thick,
# CA 22.9). The LED package, the tube's bore past its internal thread, the heat sink and the bracket are envelopes (named so).
BWL = dict(
    clear=3.0,                                                     # the tube's front rim off the BW clamp frame (4.76 mm plate)
    tube=dict(od=30.48, l=16.5, thread_in=12.7, thread_ext=3.0, od_ext=26.29, id_in=25.4, id_ext=23.5),   # SM1L05 (id_ext estimate)
    ring=dict(t=2.0, ca=22.9),                                     # SM1RR, flush with the tube's face; it bears on S1 at its clear aperture
    lens=dict(d=25.4, ct=14.0, R1=8.818197, k1=-0.9991715, A=(8.6821674e-05, 6.3760123e-08, 2.4073084e-09, -1.7189021e-11), R2=-69.99948),
    gap=8.2,                    # die to S2 (mm): the best focus for the side camera's field in bw_light.py (paraxial 8.9); set on the bench
    led=dict(board_d=22.0, board_t=1.6, pkg=3.5, h=2.8, emit=2.6),  # emit: the die's face above the board's back (estimate)
    hs=dict(d=36.0, L=40.0, collar=10.0, root_d=24.0, fins=5, fin_t=2.0, fin_pitch=6.0, bore_d=26.29, bore_past_tube=0.38, pedestal_d=22.5),
    clamp=dict(t0=1.0, w=8.0, half=23.0, up=25.0, top_z=60.5),     # split block on the heat sink's collar, its top flat under the arm
    bracket=dict(t=6.35, x=(-147.5, -123.0), z=(60.5, 78.0), holes_x=(-141.0, -129.5), hole_z=69.25,
                 arm=[(-147.5, 111.0), (-123.0, 111.0), (-123.0, 118.0), (-141.0, 162.0), (-150.0, 164.0), (-178.0, 130.0),
                      (-170.0, 118.0), (-156.0, 111.0)]),
)


def _asphere(Ld):
    """ACL25416U-B as a solid of revolution about local z: S1's vertex at z = 0, S2 toward +z (the LED side)."""
    c, k, A = 1 / Ld["R1"], Ld["k1"], Ld["A"]
    r_e = Ld["d"] / 2

    def s1(r):
        r2 = r * r
        return c * r2 / (1 + math.sqrt(1 - (1 + k) * c * c * r2)) + sum(ai * r2 ** (i + 2) for i, ai in enumerate(A))

    cz = Ld["ct"] + Ld["R2"]
    rs = np.linspace(0.0, r_e, 31)
    pts = [(float(r), float(s1(r))) for r in rs] + [(float(r), float(cz + math.sqrt(Ld["R2"] ** 2 - r * r))) for r in rs[::-1]]
    solid = cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0)).val()
    return solid, (lambda r: s1(r)), (lambda r: cz + math.sqrt(Ld["R2"] ** 2 - r * r))


def _bw_light(parts, add, h):
    """The light behind the BW window: M850D3 + ACL25416U-B in an SM1L05 on a finned heat sink, clamp and bracket (see BWL)."""
    C, box, fuse = h.C, h.box, h.fuse
    L = BWL
    y_out = FF.OUTER["y"]
    s = MS.VIEWPORTS["BW"]
    c, d = np.array(s["centre"], float), np.array(MS.axis_to_target(s["centre"]))
    a, up, side = _frame(-d)                                         # a: outward along the sight line
    T, Rg, Ld, Le, Hs = L["tube"], L["ring"], L["lens"], L["led"], L["hs"]
    P = lambda t: c + t * a                                         # noqa: E731
    lens, s1, s2 = _asphere(Ld)
    r_ca = Rg["ca"] / 2
    t_tube = (4.76 + L["clear"] + T["od"] / 2 * math.sqrt(1.0 - a[1] ** 2)) / a[1]   # tube front: its rim L["clear"] off the clamp frame
    t_s1 = t_tube + Rg["t"] - s1(r_ca)                              # the front ring bears on S1 at the ring's clear aperture
    t_die = t_s1 + Ld["ct"] + L["gap"]
    t_board = t_die + Le["emit"]                                    # the board's back face
    t_hs = t_tube + T["l"] - T["thread_ext"]                        # heat sink front face: the tube's shoulder bears on it
    t_floor = max(t_tube + T["l"] + Hs["bore_past_tube"], t_board)  # bore floor: the board on it, or on a pedestal rising from it
    assert t_floor - t_board < 3.0 and t_floor - t_hs < 8.0, (t_floor, t_board, t_hs)
    # lens tube with its two retaining rings
    tub = fuse([_cyl_ax(T["od"] / 2, P(t_tube), a, T["l"] - T["thread_ext"]), _cyl_ax(T["od_ext"] / 2, P(t_hs), a, T["thread_ext"])])
    tub = tub.cut(_cyl_ax(T["id_in"] / 2, P(t_tube - 0.01), a, T["thread_in"] + 0.01))
    tub = tub.cut(_cyl_ax(T["id_ext"] / 2, P(t_tube + T["thread_in"] - 0.01), a, T["l"] - T["thread_in"] + 0.02))
    t_r1 = t_tube
    t_r2 = t_s1 + s2(r_ca)                                          # the back ring bears on S2 at the same radius
    rings = [_tube_ax(T["id_in"] / 2, Rg["ca"] / 2, P(t), a, Rg["t"]) for t in (t_r1, t_r2)]
    add("BW LED lens tube (Thorlabs SM1L05, Ø30.5 x 16.5, with two SM1RR rings holding the asphere; bore past the thread an envelope)",
        fuse([tub] + rings), C["black"], 5, (0, 260, 0), mat="al6061", mass_kg=0.012, bom="M7-05b", tags=TAG)
    add("BW LED asphere (Thorlabs ACL25416U-B, Ø25.4 f 16 mm, B270, AR 650-1050 nm; from its Zemax prescription)",
        _local(lens, P(t_s1), a, up), C["glass"], 5, (0, 270, 0), mat="misc", mass_kg=0.0104, bom="M7-05a", opacity=0.45, tags=TAG)
    # the LED: Ø22 x 1.6 board, its package (envelope 3.5 x 3.5 x 1.2) facing the lens
    board = _cyl_ax(Le["board_d"] / 2, P(t_board - Le["board_t"]), a, Le["board_t"])
    pk = Le["pkg"] / 2
    pkg = _local(box(-pk, pk, -pk, pk, 0.0, Le["h"] - Le["board_t"]), P(t_board - Le["h"]), a, up)
    add("BW LED (Thorlabs M850D3, 850 nm, 1.4 W min at 1.5 A CW, 2 A pulsed; 1 x 1 mm die on a Ø22 x 1.6 MCPCB; package an envelope)",
        fuse([board, pkg]), C["pcb"], 5, (0, 280, 0), mat="misc", mass_kg=0.002, bom="M7-05", tags=TAG)
    # heat sink (custom, 6061, black anodised): Ø36 collar with the SM1 internal thread, then five Ø36 x 2 fins on a Ø24 root
    body = [_cyl_ax(Hs["d"] / 2, P(t_hs), a, Hs["collar"]), _cyl_ax(Hs["root_d"] / 2, P(t_hs + Hs["collar"]), a, Hs["L"] - Hs["collar"])]
    body += [_cyl_ax(Hs["d"] / 2, P(t_hs + Hs["collar"] + 2.0 + k * Hs["fin_pitch"]), a, Hs["fin_t"]) for k in range(Hs["fins"])]
    hs = fuse(body).cut(_cyl_ax(Hs["bore_d"] / 2, P(t_hs - 0.01), a, t_floor - t_hs + 0.01))
    if t_floor - t_board > 0.05:
        hs = hs.fuse(_cyl_ax(Hs["pedestal_d"] / 2, P(t_board), a, t_floor - t_board + 0.01))
    hs = hs.cut(_cyl_ax(1.0, P(t_board) + 12.2 * side, a, t_hs + Hs["L"] - t_board + 1.0))   # Ø2 hole past the board's edge for its leads
    add("BW LED heat sink (custom 6061, black anodised, Ø36 x 40, SM1 internal thread, five fins; envelope of a lathe part)", hs,
        C["anod"], 5, (0, 300, 0), mat="al6061", mass_kg=0.07, bom="M7-05c", tags=TAG)
    # split clamp on the collar, its top flat under the bracket's arm (2 x M4 up into the arm; clamp screw across the split)
    Cl, Bk = L["clamp"], L["bracket"]
    blk = _local(box(-Cl["half"], Cl["up"], -Cl["half"], Cl["half"], t_hs + Cl["t0"], t_hs + Cl["t0"] + Cl["w"]), c, a, up)
    blk = blk.intersect(box(-1e4, 1e4, -1e4, 1e4, -1e4, Cl["top_z"])).cut(_cyl_ax(Hs["d"] / 2, P(t_hs - 1.0), a, Hs["collar"] + 2.0))
    blk = blk.cut(_local(box(-Cl["half"] - 1, -Hs["d"] / 2 + 1.0, -0.5, 0.5, t_hs, t_hs + Hs["collar"]), c, a, up))   # the split, below
    add("BW LED clamp (custom 6061 split block on the heat sink's collar, 8 mm wide; envelope)", blk, C["alu_dark"], 5, (0, 300, 0),
        mat="al6061", mass_kg=0.03, bom="M7-05d", tags=TAG)
    # L bracket: a 1/4 in. 6061 flange on the back wall's outer face above the clamp frame (2 x M4 into new tapped holes), and an arm
    z0, z1 = Bk["z"]
    flange = box(Bk["x"][0], Bk["x"][1], y_out, y_out + Bk["t"], z0, z1)
    arm = cq.Solid.extrudeLinear(cq.Face.makeFromWires(cq.Wire.makePolygon([V(x, y, z0) for x, y in Bk["arm"]], close=True)), V(0, 0, Bk["t"]))
    holes = [h.cyl(2.25, (x, y_out - 1.0, Bk["hole_z"]), "y", Bk["t"] + 2.0) for x in Bk["holes_x"]]
    add("BW LED bracket (custom 6061 1/4 in. L: flange on the back wall above the BW clamp frame, 2 x M4; arm over the light; envelope)",
        fuse([flange, arm]).cut(h.comp(holes)), C["alu_dark"], 5, (0, 320, 0), mat="al6061", mass_kg=0.06, bom="M7-05d", tags=TAG)
    _cut(parts, "Process chamber body", [h.cyl(1.65, (x, y_out + 0.01, Bk["hole_z"]), "-y", 8.0) for x in Bk["holes_x"]])   # M4 tap drill, 8 deep
    REPORT["BW_light"] = dict(t_asphere_vertex=round(t_s1, 2), t_tube_front=round(t_tube, 2), t_die=round(t_die, 2), t_board_back=round(t_board, 2),
                              t_heat_sink=(round(t_hs, 2), round(t_hs + Hs["L"], 2)), die=P(t_die).round(1).tolist(),
                              heat_sink_back=P(t_hs + Hs["L"]).round(1).tolist(), asphere_vertex=P(t_s1).round(1).tolist())
    REPORT.setdefault("BW", {})["led_front"] = P(t_s1).round(1).tolist()


# ======================================================================================================== LP: steep lid port
def lp_geometry(centre=None):
    """the LP port for a candidate centre: the bore normal to the lid that would pass the clear aperture (fabrication.md's plan),
    and the bore on the line of sight drawn here (as the layer camera's, optics.md §8.5), with the room each leaves for the
    adapter's face seal next to the window flange (Ø100 on the lid's centre)"""
    s = MS.VIEWPORTS["LP"]
    c = np.array(centre or s["centre"], float)
    d = np.array(MS.axis_to_target(tuple(c)))
    rc = s["clear_d"] / 2
    z0, z1 = 120.0, 136.0                                                # lid underside and top
    pts = FF.clear_points(c, d, rc, 2, z0 - 0.5, z1 + 0.5)
    cen = 0.5 * (FF.axis_at(c, d, 2, z0) + FF.axis_at(c, d, 2, z1))
    r_need = float(np.max(np.hypot(pts[:, 0] - cen[0], pts[:, 1] - cen[1])))
    R_normal = FF.ceil_to(r_need + 0.5, 0.5)
    elev = MS.elevation_deg(tuple(c))
    r_b = rc + 2.0                                                       # Ø24 on the line of sight
    r_ell = r_b / math.sin(math.radians(elev))                           # the bore's ellipse on the lid's top face, long half-axis
    F = MP.FACE_1P78
    def seal_room(cx, cy, r_open):
        r_g = r_open + 2.0
        while MP.pick_ring(2 * math.pi * r_g) is None and r_g < r_open + 5.0:
            r_g += 0.1
        r_a = r_g + F["width"] + 2.5
        return dict(r_groove=r_g, r_adapter=r_a, gap_to_window_flange=float(np.hypot(cx, cy)) - r_a - 50.0)
    return dict(c=c, d=d, rc=rc, elevation=elev, r_bore=r_b, r_ellipse=r_ell, normal_bore_d=2 * R_normal, normal_bore_needed_d=2 * r_need,
                normal_bore_centre=cen, normal=seal_room(cen[0], cen[1], R_normal), on_axis=seal_room(c[0], c[1], r_ell))


def lp_adapter_holes(c, r_a):
    """4 x M4 on the LP adapter (and its blanking cap), 3.5 mm in from its edge, none on the side facing the window flange"""
    to_c = _unit([-c[0], -c[1], 0.0])
    out = []
    for k in range(4):
        ang = math.atan2(-to_c[1], -to_c[0]) + math.radians(-105 + 70 * k)
        out.append((c[0] + (r_a - 3.5) * math.cos(ang), c[1] + (r_a - 3.5) * math.sin(ang)))
    return out


def _lp(parts, add, h):
    C, box, cyl, tube, comp, fuse = h.C, h.box, h.cyl, h.tube, h.comp, h.fuse
    F = MP.FACE_1P78
    g = lp_geometry()
    c, d = g["c"], g["d"]
    a, up, side = _frame(-d)                                             # outward
    lz0, lz1 = 120.0, 136.0
    # bore on the line of sight through the lid (Ø24); the face O-ring groove is cut in the lid round the bore's ellipse, so the
    # adapter's face (and the flat blanking cap that stands in for it until the camera is bought) seal on it (fabrication.md §3)
    r_b = g["r_bore"]
    sr = g["on_axis"]
    r_g, r_a = sr["r_groove"], sr["r_adapter"]
    r_go = r_g + F["width"]
    flange = cyl(r_a, (c[0], c[1], lz1), "z", 8.0)
    s_top = float(getattr(MS, "LP_GEOM", {}).get("s_top", 34.0))
    r_bo = 17.0
    boss = _cyl_ax(r_bo, c - 12.0 * a, a, s_top + 12.0 - 3.0).intersect(box(-1e3, 1e3, -1e3, 1e3, lz1, 1e3))
    body = fuse([flange, boss])
    bore = _cyl_ax(r_b, c + 30.0 * d, -d, 30.0 + s_top)                  # from under the lid up through the boss
    body = body.cut(bore)
    p_w = c + (s_top - 3.0 - 0.75) * a                                    # window seat: 3 mm window on a 0.75 mm gasket
    body = body.cut(_cyl_ax(12.8, p_w - 0.75 * a, a, 5.0))
    p_s = c + 12.0 * a                                                    # slide pocket in the boss, under the window
    body = body.cut(_cyl_ax(12.75, p_s, a, 1.6))
    holes = lp_adapter_holes(c, r_a)
    for x, y in holes:
        body = body.cut(cyl(2.25, (x, y, lz1 - 1), "z", 10.0))
    add(f"LP adapter boss (6061; Ø{2 * r_a:.0f} flange on the lid's face O-ring; Ø{2 * r_b:.0f} bore and window square to the line of "
        f"sight; cover slide inside)", body, C["anod"], 7, (0, 0, 300), mat="al6061", bom="M7-16", tags=TAG)
    pk = MP.pick_ring(2 * math.pi * r_g)
    add(f"LP adapter O-ring (FKM 75A {pk[0]}, in the lid's face groove)", tube(r_go - 0.3, r_g, (c[0], c[1], lz1 - F["depth"]), "z", F["depth"]),
        C["black"], 7, (0, 0, 300), mat="fkm", bom="M0-07", tags=TAG)
    h.GLANDS["lp_adapter"] = dict(kind="face", ring=pk[0], cs=F["cs"], depth=F["depth"], width=F["width"], groove_id=2 * r_g,
                                  groove_mat="al", T=60.0, closure="LP adapter boss (or blanking cap) on the lid")
    add("LP window (Ø25.4 x 3 mm UV fused silica, square to the line of sight)", _cyl_ax(12.7, p_w, a, 3.0), C["glass"], 7, (0, 0, 330),
        mat="fused_silica", bom="M7-17", opacity=0.5, tags=TAG)
    add("LP window gasket and flat ring (FKM 75A sheet, 1.0 mm squeezed to 0.75)",
        comp([_tube_ax(12.6, 10.5, p_w - 0.75 * a, a, 0.75), _tube_ax(12.6, 10.5, p_w + 3.0 * a, a, 0.75)]), C["black"], 7, (0, 0, 330),
        mat="fkm", bom="M0-06", tags=TAG)
    p_r = c + s_top * a
    add("LP window retaining ring (SM1-class threaded ring, bottoms on the boss)", _tube_ax(16.0, 10.5, p_r, a, 3.0), C["anod"], 7,
        (0, 0, 335), mat="al6061", bom="M7-17", tags=TAG)
    add("LP cover slide (Ø25 x 1 mm fused silica, in the boss under the window; consumable)", _cyl_ax(12.5, p_s + 0.3 * a, a, 1.0),
        C["glass"], 7, (0, 0, 320), mat="fused_silica", bom="M7-18", opacity=0.5, tags=TAG)
    # the lid's bore on the line of sight and the adapter's tapped holes
    _cut(parts, "Chamber lid (6061-T6", [_cyl_ax(r_b, c + 30.0 * d, -d, 40.0), tube(r_go, r_g, (c[0], c[1], lz1 - F["depth"]), "z", F["depth"] + 0.01)]
         + [cyl(1.65, (x, y, lz1 - 8.0), "z", 8.1) for x, y in holes])
    # camera: filters + Kowa 50 mm + IMX296 board in a 40 x 40 x 30 housing
    so = float(MS.LID_CAMERA.get("standoff_mm", 15.0))
    p_f = c + (s_top + 3.0) * a
    filt = _cyl_ax(16.0, p_f, a, so - 3.0)
    p_l = c + (s_top + so) * a
    lens = _cyl_ax(16.0, p_l, a, 45.0)
    bw_, bh_, bl_ = MS.LID_CAMERA["body_mm"]
    p_b = p_l + 45.0 * a
    # the housing turned about its axis so a face, not a corner, faces +x: PB2 stands on the bridge just past the cut-out
    wx = np.array([1.0, 0.0, 0.0]) - a[0] * a
    th = math.atan2(float(wx @ side), float(wx @ up))
    up2 = math.cos(th) * up + math.sin(th) * side
    cam = _local(box(-bh_ / 2, bh_ / 2, -bw_ / 2, bw_ / 2, 0.0, bl_), p_b, a, up2)
    add("LP camera filters (FBH850-10 + FESH1000 in an SM1 holder; envelope)", filt, C["black"], 7, (0, 0, 340), mat="misc", mass_kg=0.04,
        bom="M7-14", tags=TAG)
    add("LP camera lens (Kowa LM50JC10M, 50 mm C-mount; envelope Ø32 x 45)", lens, C["black"], 7, (0, 0, 350), mat="misc", mass_kg=0.2,
        bom="M7-13", tags=TAG)
    add(f"LP camera (monochrome IMX296 board in a {bw_:.0f} x {bh_:.0f} x {bl_:.0f} housing)", cam, C["motor"], 7, (0, 0, 360), mat="misc",
        mass_kg=0.08, bom="M7-12", tags=TAG)
    # optics-bridge cut-out: the camera's swept outline through the bridge slab, 4 mm all round, cut vertically
    zb0, zb1 = h.P["z_bridge0"], h.P["z_bridge1"]
    cam_all = fuse([lens, cam])
    bb = cam_all.BoundingBox()
    cut = None
    if bb.zmax > zb0:
        sl = cam_all.intersect(box(-1e3, 1e3, -1e3, 1e3, zb0 - 2.0, zb1 + 2.0))
        hull = _xy_hull_prism(sl, zb0 - 1.0, zb1 + 1.0, grow=4.0)
        _cut(parts, "Optics bridge (6061", [hull])
        cb = hull.BoundingBox()
        cut = dict(x=(round(cb.xmin, 1), round(cb.xmax, 1)), y=(round(cb.ymin, 1), round(cb.ymax, 1)), area_mm2=round(hull.Volume() / (zb1 - zb0 + 2.0), 0))
    REPORT["LP"] = dict(centre=c.tolist(), elevation_deg=round(g["elevation"], 2), bore=f"Ø{2 * r_b:.0f} on the line of sight",
                        bore_ellipse_on_top_mm=round(2 * g["r_ellipse"], 1), adapter_d=round(2 * r_a, 1), o_ring=pk[0],
                        adapter_gap_to_window_flange_mm=round(sr["gap_to_window_flange"], 2),
                        normal_bore_alternative=dict(d=g["normal_bore_d"], needed_d=round(g["normal_bore_needed_d"], 2),
                                                     adapter_gap_to_window_flange_mm=round(g["normal"]["gap_to_window_flange"], 2)),
                        s_top=s_top, lens_front=p_l.round(1).tolist(), camera_top=(p_b + bl_ * a).round(1).tolist(), bridge_cutout=cut)


def _xy_hull_prism(shape, z0, z1, grow=0.0):
    """vertical prism over the convex hull of a shape's xy footprint, grown by `grow`"""
    vs, _ = shape.tessellate(0.5, 0.5)
    pts = np.array([(p.x, p.y) for p in vs])
    if grow:
        ang = np.linspace(0, 2 * math.pi, 24, endpoint=False)
        pts = (pts[:, None, :] + grow * np.stack([np.cos(ang), np.sin(ang)], 1)[None]).reshape(-1, 2)
    from scipy.spatial import ConvexHull
    hv = pts[ConvexHull(pts).vertices]
    w = cq.Workplane("XY").polyline([tuple(map(float, p)) for p in hv]).close().extrude(z1 - z0).val().translate(V(0, 0, z0))
    return w


# ======================================================================================================== coaxial cage
def _cage(parts, add, h):
    C, box, cyl, tube, comp, fuse = h.C, h.box, h.cyl, h.tube, h.comp, h.fuse
    VP = h.VP
    co = MS.COAX
    yb, zb = co["beam_y"], co["beam_z"]
    hc = 41.9 / 2
    zbr = h.P["z_bridge1"]
    x1, x2, x3 = co["cube1"]["x"], co["cube2"]["x"], co["cube3"]["x"]
    parts[:] = [p for p in parts if not p.name.startswith("Coaxial photodiode chain")]
    r_t = 15.25                                                          # SM1 lens tube OD 30.5

    def post(x, y, ztop):
        return box(x - 10, x + 10, y - 10, y + 10, zbr, ztop)

    def rods(p0, axis, length):
        e = np.array([0, 0, 1.0]) if axis in ("x", "-x", "y", "-y") else np.array([1.0, 0, 0])
        dv = np.array(h._AX[axis].toTuple())
        f = np.cross(dv, e)
        out = []
        for s1 in (-15.0, 15.0):
            for s2 in (-15.0, 15.0):
                q = np.array(p0) + s1 * e + s2 * f
                out.append(cyl(3.0, tuple(q), axis, length))
        return out
    cubes = [VP.thorlabs_cage_cube().translate(V(x, yb, zb)) for x in (x2, x3)]
    add("Coaxial cube 2 (Thorlabs C4W + B4C/M + FFM1; DMSP950: 955-990 nm to the camera arm, < 930 nm on) on a post",
        fuse([cubes[0], post(x2, yb, zb - hc)]), C["anod"], 9, (0, 0, 340), mat="misc", mass_kg=0.2, bom="M6-05", tags=TAG)
    add("Coaxial cube 3 (Thorlabs C4W + B4C/M + FFM1; DMLP805: < 790 nm to photodiode A, > 825 nm to photodiode B) on a post",
        fuse([cubes[1], post(x3, yb, zb - hc)]), C["anod"], 9, (0, 0, 340), mat="misc", mass_kg=0.2, bom="M5-08", tags=TAG)
    tubes = [tube(r_t, 12.7, (x1 - hc, yb, zb), "-x", (x1 - hc) - (x2 + hc)), tube(r_t, 12.7, (x2 - hc, yb, zb), "-x", (x2 - hc) - (x3 + hc))]
    rr = rods((x1 - hc, yb, zb), "-x", (x1 - hc) - (x2 + hc)) + rods((x2 - hc, yb, zb), "-x", (x2 - hc) - (x3 + hc))
    add("Coaxial lens tubes between the cubes (SM1; the shared FESH1000 after cube 1)", comp(tubes), C["black"], 9, (0, 0, 340), mat="misc",
        mass_kg=0.05, bom="M5-01", tags=TAG)
    # camera arm along -y from cube 2: FESH1000 + AC254-075-B in SM1 tubes, the board on a cage plate at the lens's focus
    y_c0 = yb - hc
    L_cam = 10.0 + 75.0 + 10.0
    y_pl = y_c0 - L_cam
    arm_c = [tube(r_t, 12.7, (x2, y_c0, zb), "-y", L_cam), box(x2 - hc, x2 + hc, y_pl - 8.0, y_pl, zb - hc, zb + hc)]
    rr += rods((x2, y_c0, zb), "-y", L_cam)
    board = box(x2 - 19.0, x2 + 19.0, y_pl - 8.0 - 22.0, y_pl - 8.0, zb - 19.0, zb + 19.0)
    add("Coaxial camera arm (SM1 tubes: FESH1000, AC254-075-B tube lens; CP33/M-class cage plate)", comp(arm_c), C["black"], 9, (0, -150, 300),
        mat="misc", mass_kg=0.12, bom="M6-03", tags=TAG)
    add("Coaxial camera (monochrome IMX296 board on an adapter plate; envelope 38 x 38 x 22)", fuse([board, post(x2, y_pl - 19.0, zb - 19.0)]),
        C["pcb"], 9, (0, -170, 300), mat="misc", mass_kg=0.05, bom="M6-02", tags=TAG)
    # photodiode B along -x from cube 3; photodiode A along -y from cube 3 (the existing T2 PDA36A2)
    L_pd = 10.0 + 60.0
    xb0 = x3 - hc
    pdb_t = [tube(r_t, 12.7, (xb0, yb, zb), "-x", L_pd)]
    rr += rods((xb0, yb, zb), "-x", L_pd)
    pdb = VP.thorlabs_pda36a2().translate(V(xb0 - L_pd, yb, zb))
    add("Photodiode B arm (FBH900-40, AC254-050-B, P500K pinhole in SM1 tubes)", comp(pdb_t), C["black"], 9, (-150, 0, 300), mat="misc",
        mass_kg=0.08, bom="M5-04", tags=TAG)
    add("Photodiode B (Thorlabs PDA36A2) on the cage, a post under the arm", fuse([pdb, post(xb0 - L_pd + 15.0, yb, zb - r_t)]), C["black"], 9,
        (-170, 0, 300), mat="misc", mass_kg=0.3, bom="M5-05", tags=TAG)
    ya0 = yb - hc
    pda_t = [tube(r_t, 12.7, (x3, ya0, zb), "-y", L_pd)]
    rr += rods((x3, ya0, zb), "-y", L_pd)
    pda = h.place(VP.thorlabs_pda36a2(), (x3, ya0 - L_pd, zb), (0, -1, 0), (0, 0, 1))
    add("Photodiode A arm (FBH700-40, AC254-050-B, P500K pinhole in SM1 tubes)", comp(pda_t), C["black"], 9, (0, -150, 300), mat="misc",
        mass_kg=0.08, bom="M5-03", tags=TAG)
    add("Photodiode A (Thorlabs PDA36A2, the existing T2 unit) on the cage, a post under the arm", fuse([pda, post(x3, ya0 - L_pd + 15.0, zb - r_t)]),
        C["black"], 9, (0, -170, 300), mat="misc", mass_kg=0.3, bom="T2", tags=TAG)
    add("Cage rods (Thorlabs ER-series Ø6, 30 mm cage)", comp(rr), C["ss"], 9, (0, 0, 340), mat="ss304", mass_kg=0.1, bom="M5-09", tags=TAG)
    # beam trap on cube 1's far port (-y face): the DMSP1000's forward leak
    bt = fuse([box(x1 - hc, x1 + hc, yb - hc - 30.0, yb - hc, zb - hc, zb + hc), post(x1, yb - hc - 15.0, zb - hc)])
    add("Beam trap on cube 1's far port (Thorlabs BTC30 class, >= 5 W; envelope 41.9 x 30 x 41.9) on a post", bt, C["black"], 9,
        (0, -150, 300), mat="misc", mass_kg=0.15, bom="M0-17", tags=TAG)
    REPORT["cage"] = dict(cubes_x=[x1, x2, x3], camera_plate_y=round(y_pl, 1), pd_b_face_x=round(xb0 - L_pd, 1), pd_a_face_y=round(ya0 - L_pd, 1))


# ======================================================================================================== AE path
AE_XY = {"M50": (3.2, 120.0), "L75": (3.2, 120.0)}        # waveguide (r, deg): through the piston head's Ø10 wire hole, clear of the TCs and heaters
AE_WG_D = 3.0                                              # Ø3 mm 316 (analysis/out/monitoring/mech/checks.md §6)


def _ae(parts, add, h, module):
    C, box, cyl, tube, comp, fuse = h.C, h.box, h.cyl, h.tube, h.comp, h.fuse
    import modules_low as ML
    z = ML.zlevels()
    zc = z["zc"]
    pg = dict(group="piston", tags=("in_module",) + TAG)
    RF = ML.ROD_FT
    wg = None
    if module in AE_XY:
        r, deg = AE_XY[module]
        x, y = r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg))
        z_top = z["zb1"] - 4.0                                            # the plate spigot's underside
        z_bot = zc + 9.0 - 3.0                                            # 3 mm into an M2 thread in the rod end's bore floor (striker below)
        wg = cyl(AE_WG_D / 2, (x, y, z_bot), "z", z_top - z_bot)
        add(f"AE waveguide {module} (Ø3 mm 316 rod; tip domed R >= 25 on the plate's spigot; down the hollow rod; cold end screwed "
            f"into the rod end)", wg, C["ss"], 4, (0, 0, 260), mat="ss316l", bom="M4-06", section=True, **pg)
        hole = cyl(AE_WG_D / 2 + 0.2, (x, y, z["zk0"] - 30.0), "z", (z["zb1"] - 4.3) - (z["zk0"] - 30.0) + 0.01)
        _cut(parts, f"Heater block {module}", [hole])
        _cut(parts, f"Radiation shields {module}", [hole])
        _cut(parts, f"Rod end {module}: 316L", [cyl(AE_WG_D / 2, (x, y, z_bot - 0.01), "z", 6.0)])
        REPORT["AE"] = dict(waveguide_xy=(round(x, 2), round(y, 2)), z_top=z_top, z_bottom=z_bot, length=round(z_top - z_bot, 1))
    # sensor on the rod end's back face (+y), at x -26: outside the gas boundary; spring strap screwed to the same face
    yb = RF["back_y"]
    zs = zc + RF["face_z0"] + 11.0                                    # Ø19 sensor, 1.5 mm above the block's bottom face (Z arm below)
    xs = -26.0
    sens = fuse([cyl(9.5, (xs, yb, zs), "y", 16.0), cyl(3.0, (xs + 9.0, yb + 8.0, zs), "x", 8.0)])
    add("AE sensor (wideband, MISTRAS WSa / Vallen VS900-M class; envelope Ø19 x 16 with a side connector) on the rod end's back face",
        sens, C["blue"], 4, (0, 160, 0), mat="misc", mass_kg=0.03, bom="M4-01", section=True, **pg)
    strap = fuse([box(xs - 14.5, xs + 14.5, yb + 16.0, yb + 19.0, zs - 4.0, zs + 4.0),
                  box(xs - 14.5, xs - 11.5, yb, yb + 16.0, zs - 4.0, zs + 4.0), box(xs + 11.5, xs + 14.5, yb, yb + 16.0, zs - 4.0, zs + 4.0)])
    add("AE sensor strap clamp (6061, 2 x M3 into the rod end's back face, wave spring over the sensor)", strap, C["alu_dark"], 4, (0, 170, 0),
        mat="al6061", bom="M4-09", section=True, **pg)
    # preamp on the process base plate, behind-left of the Z stage (<= 1 m of cable; the sensor's lead unplugs at a module swap)
    zbp = h.P["z_base1"]
    pre = box(-265.0, -155.0, -240.0, -180.0, zbp, zbp + 30.0)      # front-left: 5 mm off the guard's bottom rail, clear of the bridge posts and legs
    add("AE preamplifier (MISTRAS 2/4/6 class, 40 dB; envelope 110 x 60 x 30) on the process base plate", pre, C["blue"], 4, (0, 0, -150),
        mat="misc", mass_kg=0.25, bom="M4-02", tags=TAG)


# ======================================================================================================== digitizer, sync box
def _daq(parts, add, h):
    """PicoScope 4444 and the sync breakout box on the floor of the 4U drawer (sync-and-data.md §2.1); the drawer is an envelope here"""
    C, box = h.C, h.box
    dr = _find(parts, "DIN-rail drawer")[0].shape.BoundingBox()
    x0, y1, z0 = dr.xmin + 12.0, dr.ymax - 12.0, dr.zmin + 3.0
    add("Digitizer PicoScope 4444 (190 x 170 x 40 mm) on the 4U drawer's floor", box(x0, x0 + 190.0, y1 - 170.0, y1, z0, z0 + 40.0), C["blue"], 2,
        (0, -400, 0), mat="misc", mass_kg=1.0, module="rack", bom="M1-01", tags=TAG)
    add("Sync breakout box (bought enclosure, BNC bulkheads, isolator boards) in the 4U drawer", box(x0 + 200.0, x0 + 320.0, y1 - 80.0, y1, z0, z0 + 40.0),
        C["anod"], 2, (0, -400, 0), mat="misc", mass_kg=0.4, module="rack", bom="M1-07", tags=TAG)


# ======================================================================================================== camera cooling
def _cooling(parts, add, h, module="M50"):
    """Cooling for the cameras and Pis in the guard's air (mechanics.md Checks §7). Nothing drawn yet."""
    return


def apply(parts, add, h, module="M50"):
    """Add the monitoring parts to lpbf_low.build()'s list `parts` (in place) and cut the holes they need."""
    REPORT.clear()
    _lw(parts, add, h)
    _bw(parts, add, h)
    _bw_light(parts, add, h)
    _lp(parts, add, h)
    _cage(parts, add, h)
    _ae(parts, add, h, module)
    _daq(parts, add, h)
    _cooling(parts, add, h, module)
    return parts


if __name__ == "__main__":
    import json
    import time

    import lpbf_low as M
    t0 = time.time()
    ps = M.build(monitoring=True)
    mon = [p for p in ps if "monitoring" in p.tags]
    print(f"{len(ps)} parts ({len(mon)} monitoring) in {time.time() - t0:.1f} s")
    bb = M.envelope(ps)
    print(f"height above tray {bb.zmax - M.Z_TRAY:.1f} mm; x {bb.xmin:.0f}..{bb.xmax:.0f}")
    print(json.dumps(sys.modules["monitoring_parts"].REPORT, indent=1, default=str))
