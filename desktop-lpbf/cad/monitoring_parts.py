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
  * the AE path (monitoring.md §5.4, monitoring/mechanics.md §4): on M50 and L75 a Ø3 mm 316 waveguide that slides free from
    the plate's spigot (Ø4 head domed R50, in a counterbore in the socket floor) down through the heater block, both radiation
    shields, the piston head's wire hole and the hollow rod, to its foot on a miniature sensor (MISTRAS PICO) in a 316L
    cartridge on the rod end's bore floor, with the spring under the sensor that sets the force on the plate, and a Microdot
    weld-in (SST FA40102) in the rod end's cap for the sensor's lead; on S25 the sensor in a strap clamp on the rod end's back
    face, as before; the preamp on the process base plate;
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
    add(f"LW window clamp ring (6061, 1/4 in. plate, Ø{cr['od']:.0f} x Ø{cr['id']:.0f}, 4 x M4 on Ø{cr['bolt_circle_d']:g}, a flat clear of the "
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


# the adapter's 4 x M4, where analysis/monitoring/fab/lp_cam.py programs them (its LP_BOLT): on Ø48 at +-60 and +-120 deg from the
# direction away from the lid's centre, each in an R5.5 lug on the flange. Until 2026-11-27 they were drawn 3.5 mm in from the
# Ø40.8 flange's edge, which put them in the adapter's own face O-ring groove (r 16.9) and their heads under the boss
LP_BOLT = dict(r=24.0, deg=(-120.0, -60.0, 60.0, 120.0), lug_r=5.5)


def lp_adapter_holes(c, r_a=None):
    """4 x M4 on the LP adapter and its blanking cap (LP_BOLT); r_a, the flange's radius, is no longer used"""
    away = math.atan2(c[1], c[0])
    return [(c[0] + LP_BOLT["r"] * math.cos(away + math.radians(t)), c[1] + LP_BOLT["r"] * math.sin(away + math.radians(t)))
            for t in LP_BOLT["deg"]]


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
    flange = fuse([cyl(r_a, (c[0], c[1], lz1), "z", 8.0)] +
                  [cyl(LP_BOLT["lug_r"], (x, y, lz1), "z", 8.0) for x, y in lp_adapter_holes(c)])   # lugs for the M4 screws
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
    add(f"LP adapter boss (6061; Ø{2 * r_a:.0f} flange with four screw lugs on the lid's face O-ring; Ø{2 * r_b:.0f} bore and window square to the line of "
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
# The sprung cold end (mechanics.md §4; analysis/monitoring/mech/ae_preload.py checks these numbers). z values are from the rod end's
# coupling face zc (modules_low.zlevels()). The waveguide slides free in its holes; its Ø4 head, domed R50 on top, presses on the plate's
# spigot and hangs in a counterbore in the socket floor when nothing holds it up. Its foot sits on a miniature sensor, face up, in a
# 316L cartridge that stands on the rod end's bore floor (two legs either side of the cross-drilling, which the type K leads still
# use). A spring under the sensor sets the force; the cartridge's cap stops the sensor with the plate off, so the head then stands
# delta0 above the seated spigot and the plate pushes it down that far. The sensor's lead runs up the rod to an in-line plug near the
# piston head, and a pigtail runs back down to a weld-in Microdot feedthrough in the cap's back, right of the cartridge, above the
# cross-drilling and the channel (nothing on the back face at the type K row: a gas-side body there would block the cross-drilling).
AE_CART = dict(
    wg_r=3.2, wg_deg=120.0, wg_d=3.0, hole_d=3.4,              # waveguide: axis (r, deg), shaft, its holes (as before)
    head_d=4.0, head_t=1.0, dome_R=50.0,                        # head on top, domed R50 (R25 would dent 6061 at 200 C; ae_preload.py §3)
    cb_d=4.4, cb_depth=1.3,                                     # counterbore in the heater block's socket floor
    delta0=0.6,                                                 # pre-travel: head above the seated spigot with the plate off
    cart_r=2.8, cart_deg=126.0, cart_od=6.3, cart_id=5.6,       # cartridge axis (r, deg), tube (turned 316L)
    floor_z=9.0, leg_top=12.9, seat_z=13.9, slot_y=(-0.3, 4.3), # stands on the bore floor; slot over the cross-drilling; spring seat
    cap_t=1.0, cap_hole=3.3, cable_slot_w=2.8,                  # stop cap with the waveguide's guide hole; slot for the sensor's lead
    # Lee Spring LC 029BB 09S316 (316, squared and ground): OD 4.78, ID 3.30, wire 0.74, free 19.05, solid 8.93, 3.94 N/mm
    spring_od=4.78, spring_wire=0.74, spring_L0=19.05, spring_L_stop=15.88, spring_L_solid=8.93, spring_n=12, spring_k=3.94,
    spring_su_MPa=1690.0,                                       # 316 spring wire (ASTM A313), ~0.74 mm: ~1690 MPa minimum tensile (assumed)
    sensor_d=5.0, sensor_h=4.0, boot_d=2.4, boot_L=4.1,         # MISTRAS PICO: Ø5 x 4, side cable (9.1 mm across with its boot)
    # SST FA40102 Microdot weld-in (laser or e-beam, SST's NS40102): Ø6.35 flange in a Ø6.43 x 0.51 counterbore, Ø5.18 through-bore;
    # gas side a Ø4.83 x 6.0 body and a Ø1.07 x 3.8 pin; air side 3.3 mm of 10-32 thread. In the cap's back, on a spot face
    ft_x=4.5, ft_z=15.0, ft_face_y=7.3, ft_flange_d=6.35, ft_cb_d=6.43, ft_cb=0.51, ft_bore_d=5.18, ft_body_d=4.83, ft_body_L=6.0,
    ft_pin_d=1.07, ft_pin_L=3.8, ft_thread_L=3.3, spot=7.4,
    plug_d=6.5, plug_L=14.0, cable_d=3.0, cable_L=16.0,         # mating 10-32 plug, then its cable to -x (envelope)
)
AE_CART["dome_h"] = AE_CART["dome_R"] - math.sqrt(AE_CART["dome_R"] ** 2 - (AE_CART["head_d"] / 2) ** 2)
AE_PARTS = {     # bought parts of the cold end, read on the makers' pages through the lab's tunnel (2026-11-27)
    "sensor": dict(vendor="MISTRAS", pn="PICO",
                   desc="miniature AE sensor Ø5 x 4 mm, stainless case and face, 200-750 kHz (resonance 250 kHz), 54 dB ref V/(m/s), "
                        "integral coax from the side to a BNC; quote only",
                   url="https://www.mistrasgroup.com/media/x13nu1vw/model_pico.pdf", read_utc="2026-11-27T08:27Z",
                   t_min_C=-65.0, t_max_C=177.0),
    "sensor_alt": dict(vendor="QingCheng (Qawrums)", pn="WM500/1",
                       desc="Ø4.7 x 4.0 mm, 100-1000 kHz (resonance 500 kHz), > 58 dB, -20 to 120 C, integral side cable; maker's sheet "
                            "only; quote only", url="https://aendt.com/sds/WM500-1.pdf", read_utc="2026-11-27T08:33Z",
                       t_min_C=-20.0, t_max_C=120.0),
    "spring": dict(vendor="Lee Spring", pn="LC 029BB 09S316",
                   desc="316 compression spring, squared and ground: OD 4.78, ID 3.30, wire 0.74, free 19.05, solid 8.93 mm, 3.94 N/mm, "
                        "39.4 N at solid; $8.87 each (1-19)", url="https://www.leespring.com/node/329221", read_utc="2026-11-27T08:48Z"),
    "feedthrough": dict(vendor="Solid Sealing Technology", pn="FA40102",
                        desc="Microdot (10-32) coaxial feedthrough, grounded shield, weld-in (laser or e-beam), Inconel pin, -269 to "
                             "450 C, He leak < 1e-10 atm cc/s; $34.50",
                        url="https://www.solidsealing.com/products/2052/Microdot-Feedthrough-1KV-2-Amp-0-042-inch-Inconel-Conductor-Weld-In-Without-Plug/",
                        read_utc="2026-11-27T08:29Z"),
    "couplant": dict(vendor="Chemours (McMaster 10195K41)", pn="Krytox LVP",
                     desc="PFPE vacuum grease, -15 to 300 C, 1e-13 Torr at 20 C, 1e-5 Torr at 200 C; $178.91 per 2 oz",
                     url="https://www.mcmaster.com/products/krytox-grease/?s=krytox-grease", read_utc="2026-11-27T08:34Z"),
}


def _helix(od, wire, length, n, p0):
    """a round-wire helical spring, `length` tall from p0 (the wire's ends are not ground in the model)"""
    rm, hh = (od - wire) / 2, length - wire
    path = cq.Wire.makeHelix(hh / n, hh, rm)
    prof = cq.Wire.makeCircle(wire / 2, V(rm, 0, 0), V(0, 1, 0))
    return cq.Solid.sweep(prof, [], path, isFrenet=True).translate(V(p0[0], p0[1], p0[2] + wire / 2))


def _ae(parts, add, h, module):
    C, box, cyl, tube, fuse = h.C, h.box, h.cyl, h.tube, h.fuse
    import modules_low as ML
    z = ML.zlevels()
    zc = z["zc"]
    pg = dict(group="piston", tags=("in_module",) + TAG)
    RF = ML.ROD_FT
    A = AE_CART
    if module in AE_XY:
        r, deg = AE_XY[module]
        ca, sa = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        x, y = r * ca, r * sa
        cc, sc = math.cos(math.radians(A["cart_deg"])), math.sin(math.radians(A["cart_deg"]))
        xc, yc = A["cart_r"] * cc, A["cart_r"] * sc
        z_tip = z["zb1"] - 4.0                                            # the plate spigot's underside (plate seated)
        z_sock = z["zb1"] - 4.3                                           # the socket's floor
        seat = zc + A["seat_z"]
        L_on = A["spring_L_stop"] - A["delta0"]                           # spring length with the plate on (no thermal growth)
        z_face = seat + L_on + A["sensor_h"]                              # the sensor's face = the waveguide's foot, plate on
        z_cap = seat + A["spring_L_stop"] + A["sensor_h"]                 # the stop cap's underside
        z_head0 = z_tip - A["dome_h"] - A["head_t"]
        # waveguide: shaft, head and dome (the dome's apex touches the spigot)
        dome = cq.Solid.makeSphere(A["dome_R"], V(x, y, z_tip - A["dome_R"]), angleDegrees1=-90, angleDegrees2=90).intersect(
            cyl(A["head_d"] / 2, (x, y, z_tip - A["dome_h"]), "z", A["dome_h"] + 0.01))
        wg = fuse([cyl(A["wg_d"] / 2, (x, y, z_face), "z", z_head0 - z_face + 0.01),
                   cyl(A["head_d"] / 2, (x, y, z_head0), "z", A["head_t"] + 0.001), dome])
        add(f"AE waveguide {module} (Ø3 mm 316, slides free; Ø4 head domed R{A['dome_R']:.0f} on the plate's spigot; foot on the sensor)",
            wg, C["ss"], 4, (0, 0, 260), mat="ss316l", bom="M4-06", section=True, **pg)
        hole = cyl(A["hole_d"] / 2, (x, y, z["zk0"] - 30.0), "z", z_sock - (z["zk0"] - 30.0) + 0.01)
        cb = cyl(A["cb_d"] / 2, (x, y, z_sock - A["cb_depth"]), "z", A["cb_depth"] + 0.02)
        _cut(parts, f"Heater block {module}", [hole, cb])
        _cut(parts, f"Radiation shields {module}", [hole])
        # cartridge: tube on the bore floor, legs either side of the cross-drilling, floor (spring seat), stop cap with the guide hole
        top = z_cap + A["cap_t"]
        cart = tube(A["cart_od"] / 2, A["cart_id"] / 2, (xc, yc, zc + A["floor_z"]), "z", top - (zc + A["floor_z"]))
        cart = fuse([cart, cyl(A["cart_id"] / 2 + 0.01, (xc, yc, zc + A["leg_top"]), "z", A["seat_z"] - A["leg_top"]),
                     cyl(A["cart_id"] / 2 + 0.01, (xc, yc, z_cap), "z", A["cap_t"])])
        cart = cart.cut(box(xc - 5, xc + 5, A["slot_y"][0], A["slot_y"][1], zc + A["floor_z"] - 0.1, zc + A["leg_top"]))
        cart = cart.cut(cyl(A["cap_hole"] / 2, (x, y, z_cap - 0.1), "z", A["cap_t"] + 0.2))
        cart = cart.cut(cq.Solid.makeCone(A["cap_hole"] / 2, A["cap_hole"] / 2 + 0.85, 0.85, V(x, y, top - 0.85), V(0, 0, 1)))
        # slot for the sensor's lead on the side facing the rod's axis, from the seat to under the cap
        u = (-cc, -sc)
        sl = box(-A["cable_slot_w"] / 2, A["cable_slot_w"] / 2, 0.0, A["cart_od"], seat + 0.5, z_cap - 0.6)
        sl = sl.rotate(V(0, 0, 0), V(0, 0, 1), math.degrees(math.atan2(u[1], u[0])) - 90.0).translate(V(xc, yc, 0))
        cart = cart.cut(sl)
        add(f"AE cartridge {module} (316L, Ø{A['cart_od']:.1f} tube on the rod end's bore floor: spring seat, stop cap, guide hole)",
            cart, C["ss"], 4, (0, 0, 140), mat="ss316l", bom="M4-10", section=True, **pg)
        spr = _helix(A["spring_od"], A["spring_wire"], L_on, A["spring_n"], (xc, yc, seat))
        add(f"AE spring {module} (Lee LC 029BB 09S316: 316, Ø{A['spring_od']:.2f} x {A['spring_L0']:.2f} free, {A['spring_k']:.2f} N/mm; "
            f"{L_on:.2f} long with the plate on)", spr, C["steel"], 4, (0, 0, 140), mat="steel", bom="M4-07", section=True, **pg)
        zs0 = seat + L_on
        boot = _cyl_ax(A["boot_d"] / 2, (xc + 2.0 * u[0], yc + 2.0 * u[1], zs0 + A["sensor_h"] / 2), (u[0], u[1], 0.0),
                       A["boot_L"] + 0.5)
        sens = fuse([cyl(A["sensor_d"] / 2, (xc, yc, zs0), "z", A["sensor_h"]), boot])
        add(f"AE sensor in the cartridge {module} (MISTRAS PICO, Ø{A['sensor_d']:.0f} x {A['sensor_h']:.0f}, face up; its side cable's boot "
            f"through the slot)", sens, C["blue"], 4, (0, 0, 140), mat="misc", mass_kg=0.001, bom="M4-01", section=True, **pg)
        # weld-in Microdot feedthrough in the cap's back (+y), right of the cartridge, above the cross-drilling and the channel
        fx, fz, fy = A["ft_x"], zc + A["ft_z"], A["ft_face_y"]
        sp = A["spot"] / 2
        _cut(parts, f"Rod end {module}: 316L", [box(fx - sp, fx + sp, fy, fy + 6.0, fz - sp, fz + sp),               # spot face
                                               cyl(A["ft_cb_d"] / 2, (fx, fy - A["ft_cb"], fz), "y", A["ft_cb"] + 0.01),  # weld counterbore
                                               cyl(A["ft_bore_d"] / 2, (fx, 0.0, fz), "y", fy + 0.01)])          # through-bore
        yf = fy - A["ft_cb"]
        ft = fuse([cyl(A["ft_flange_d"] / 2, (fx, yf, fz), "y", A["ft_cb"]),
                   cyl(A["ft_body_d"] / 2, (fx, yf - A["ft_body_L"], fz), "y", A["ft_body_L"] + 0.01),
                   cyl(A["ft_pin_d"] / 2, (fx, yf - A["ft_body_L"] - A["ft_pin_L"], fz), "y", A["ft_pin_L"] + 0.01),
                   cyl(A["ft_body_d"] / 2, (fx, fy, fz), "y", A["ft_thread_L"])])
        y2 = fy + A["ft_thread_L"]
        plug = fuse([cyl(A["plug_d"] / 2, (fx, y2, fz), "y", A["plug_L"]),
                     cyl(A["cable_d"] / 2, (fx - A["cable_L"], y2 + A["plug_L"] - A["plug_d"] / 2, fz), "x", A["cable_L"])])
        add(f"AE coaxial feedthrough {module} (SST FA40102 Microdot weld-in in the rod end's cap) with its mating 10-32 plug and cable "
            f"(envelope)", fuse([ft, plug]), C["ss"], 4, (0, 60, 120), mat="ss316l", mass_kg=0.02, bom="M4-11", section=True, **pg)
        REPORT["AE"] = dict(waveguide_xy=(round(x, 2), round(y, 2)), cartridge_xy=(round(xc, 2), round(yc, 2)), z_tip=z_tip,
                            z_foot=round(z_face, 2), z_cap=round(z_cap, 2), shaft_length=round(z_head0 - z_face, 1),
                            spring_on_mm=round(L_on, 2), feedthrough=(fx, fy, round(fz, 2)))
    else:
        # S25 (rod ID 7.7: no room for the waveguide and the cartridge): the sensor on the rod end's back face, outside the gas, as before
        yb = RF["back_y"]
        zs = zc + RF["face_z0"] + 11.0                                # Ø19 sensor, 1.5 mm above the block's bottom face (Z arm below)
        xs = -26.0
        sens = fuse([cyl(9.5, (xs, yb, zs), "y", 16.0), cyl(3.0, (xs + 9.0, yb + 8.0, zs), "x", 8.0)])
        add("AE sensor (wideband, MISTRAS WSa / Vallen VS900-M class; envelope Ø19 x 16 with a side connector) on the rod end's back face",
            sens, C["blue"], 4, (0, 160, 0), mat="misc", mass_kg=0.03, bom="M4-09", section=True, **pg)
        strap = fuse([box(xs - 14.5, xs + 14.5, yb + 16.0, yb + 19.0, zs - 4.0, zs + 4.0),
                      box(xs - 14.5, xs - 11.5, yb, yb + 16.0, zs - 4.0, zs + 4.0), box(xs + 11.5, xs + 14.5, yb, yb + 16.0, zs - 4.0, zs + 4.0)])
        add("AE sensor strap clamp (6061, 2 x M3 into the rod end's back face, wave spring over the sensor)", strap, C["alu_dark"], 4,
            (0, 170, 0), mat="al6061", bom="M4-09", section=True, **pg)
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
    """Cooling for the cameras and Pis in the guard's air (mechanics.md Checks §7; monitoring/cooling.md): light-trapped inlet and
    exhaust in the guard's back panel with two 120 mm exhaust fans, a duct and hood with its own fan for the side camera, G-10
    breaks under the side camera bracket's root and in the LP camera's filter holder, a fan on PB2, and the LP camera's Pi in a
    heat-sink case. The geometry is in monitoring_cooling.py, which the thermal analysis reads too."""
    import monitoring_cooling as MCOOL
    REPORT["cooling"] = MCOOL.draw(parts, add, h, module)


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
