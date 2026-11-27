"""Cooling for the monitoring cameras and the Pis in the laser guard (issue #260, PR 281; monitoring/cooling.md).

monitoring_parts._cooling() calls draw() here. The numbers live in this file so that the thermal and light-trap analysis
(analysis/monitoring/cooling/cooling.py) reads the same geometry the model draws. Importing it needs no cadquery.

What is drawn (all tagged "monitoring"; every part's name says "envelope" where its size is not read off a vendor drawing):
  * an INLET in the guard's back panel, low on the left (x -394..-218, z -118..202): a filter pad in a frame outside, a
    chevron light trap (six-leg blades, black anodised) inside, and behind the trap's right-hand part a plenum and a duct
    with a 60 mm fan that carry part of the inlet air over the side camera and down into a hood round its body;
  * the HOOD round the Chronos 2.1-HD: top, sides and back of 1 mm aluminium, open at the lens end, so the duct's air runs
    along the camera body and leaves past the lens toward the LW port;
  * an EXHAUST in the back panel, high on the right (x 40..284, z 230..344): the same chevron trap inside, and two 120 mm
    24 V fans on a short plenum outside, blowing out of the guard toward the tray's back edge (or into a dock duct);
  * G-10 thermal breaks: a 6 mm pad between the side camera bracket's root and the chamber floor plate (the bracket's root
    is trimmed by the pad's thickness so the camera stays where it was), and a 5 mm G-10 ring in place of the first 5 mm of
    the LP camera's filter holder (the holder screws onto the boss, which sits on the 60 C lid);
  * a 40 mm 24 V fan on PB2's +x end wall (PB2 gets a Ø38 hole under it and a filtered vent at the other end; the Pi 5
    inside gets the official Active Cooler);
  * the second Pi 5 (the LP camera's; the PB2 Pi's two camera ports are taken) in a fanless aluminium heat-sink case on the
    optics bridge beside the LP camera (envelope).
"""
from __future__ import annotations

import math

# ------------------------------------------------------------------------------------------------- the guard (lpbf_low.py §12)
# mirrored from lpbf_low.build() (gx0, gx1, gy0, gy1, gz0 = z_base1, gz1 = z_bridge1 + galvo riser + GALVO_H + 3); draw()
# checks them against the drawn panels
GUARD = dict(x0=-420.0, x1=310.0, y0=-265.0, y1=215.0, z0=-160.0, z1=366.11, panel_t=1.5, frame=20.0,
             panel="5052 sheet 0.063 in. (1.6 mm), bare (bom.csv S9)", door_window=(-300.0, 160.0, -120.0, 326.11))

# ------------------------------------------------------------------------------------------------- chevron light trap
# blades: 1 mm aluminium sheet bent to six legs (three V's) across the trap's 32 mm depth, 10 mm pitch, 10 mm amplitude: no
# straight line through it (amplitude >= pitch). Black anodised (Type II, black dye). trap_mc.py traces it.
LOUVRE = dict(D=32.0, A=10.0, n=6, p=10.0, t=1.0, finish="black anodised 5052 or 6061 (MIL-A-8625 Type II, class 2 black)")

# the back panel's inner face is y = 215; the traps' blades sit at y 181.5..213.5 and their frame's flange touches the panel
Y_TRAP = (215.0 - 1.5 - LOUVRE["D"], 215.0 - 1.5)
INLET = dict(x=(-394.0, -218.0), z=(-118.0, 202.0), what="inlet: filter outside, trap inside; back panel, low left")
EXHAUST = dict(x=(40.0, 284.0), z=(228.0, 338.0), what="exhaust: trap inside, two 120 mm fans outside; back panel, high right")
FILTER = dict(t=10.0, frame_t=1.5, media="polyester or polyurethane filter pad, 10 mm (G3/G4 class)")

# plenum behind the inlet trap's right-hand part, duct over the side camera, hood round its body
PLENUM = dict(x=(-283.0, -218.0), y=(150.0, Y_TRAP[0]), z=(-118.0, 202.0))
DUCT1 = dict(x=(-283.0, -218.0), y=(27.0, 150.0), z=(127.0, 203.0))          # forward from the plenum's top, beside the bridge post
DUCT2 = dict(x=(-396.0, -218.0), y=(-106.0, 27.0), z=(127.0, 203.0))         # over the camera; its floor is the hood's top
HOOD = dict(x=(-396.0, -214.0), y=(-106.0, 27.0), z=(-15.0, 127.0), t=1.0, floor_opening_x=(-392.0, -336.0))
SHEET_T = 1.0

FAN_HOOD = dict(size=60.0, depth=25.0, centre=(-250.5, 112.0, 165.0), axis="-y", part="60 mm 24 V axial fan (envelope 60 x 60 x 25)")
FAN_EXH = dict(size=120.0, depth=25.0, n=2, x0=42.0, z0=223.0, y0=215.0 + 1.5 + 10.0, guard=3.0,
               part="120 mm 24 V axial fan (envelope 120 x 120 x 25)")
EXH_PLENUM = dict(y=(216.5, 226.5))
FAN_PB2 = dict(size=40.0, depth=10.0, part="40 mm 24 V axial fan (envelope 40 x 40 x 10)")

# G-10 thermal breaks
G10_ROOT = dict(t=6.0, k=0.29, what="G-10/FR-4, 6 mm, between the side camera bracket's root and the chamber floor plate; "
                                    "the M5 screws pass in G-10 shoulder washers")
G10_RING = dict(t=5.0, od=32.0, id=25.4, k=0.29, what="G-10 ring, Ø32 x Ø25.4 x 5, first 5 mm of the LP camera's filter holder")

# the LP camera's Pi (second Pi 5) in a fanless heat-sink case on the bridge beside the LP camera
PI2_CASE = dict(x=(-190.0, -96.0), y=(117.0, 179.0), z_gap=0.5, h=33.0,      # behind the fold mirror (y <= 116), left of the LP camera
                part="Raspberry Pi 5 in a fanless aluminium heat-sink case (envelope 94 x 62 x 33)")

REPORT: dict = {}


def chevron_points(y_in, z_base):
    """one blade's centre line in (y, z): legs from the guard side (y_in) to the panel side"""
    L = LOUVRE
    return [(y_in + j * L["D"] / L["n"], z_base + (L["A"] if j % 2 else 0.0)) for j in range(L["n"] + 1)]


def opening_area_m2(which):
    s = INLET if which == "inlet" else EXHAUST
    return (s["x"][1] - s["x"][0]) * (s["z"][1] - s["z"][0]) * 1e-6


# ================================================================================================================ drawing
def draw(parts, add, h, module="M50"):
    import cadquery as cq
    import numpy as np

    V = cq.Vector
    C, box, cyl, comp, fuse = h.C, h.box, h.cyl, h.comp, h.fuse
    TAG = ("monitoring",)
    G = GUARD
    REPORT.clear()

    def find(prefix):
        return [p for p in parts if p.name.startswith(prefix)]

    # check the guard against the drawn panels
    pn = find("Laser guard panels")[0]
    bb = pn.shape.BoundingBox()
    assert abs(bb.xmin - (G["x0"] - G["panel_t"])) < 0.6 and abs(bb.ymax - (G["y1"] + G["panel_t"])) < 0.6, (bb.xmin, bb.ymax)
    assert abs(bb.zmax - (G["z1"] + G["panel_t"])) < 0.6, bb.zmax

    yb = G["y1"]                                    # back panel, inner face
    L = LOUVRE
    y_in, y_out = Y_TRAP

    def louvre(x0, x1, z0, z1, name, bom, dx_view):
        blades = []
        phi = math.atan2(L["A"], L["D"] / L["n"])
        dz = L["t"] / math.cos(phi)                  # vertical offset that gives the legs t normal to them
        nb = int(round((z1 - z0) / L["p"]))              # the frame's top plate sits on the top blade's peaks (A = p): no gap
        z1 = z0 + nb * L["p"]
        for k in range(nb):
            zb = z0 + k * L["p"]
            pts = chevron_points(y_in, zb)
            poly = pts + [(y, z - dz) for (y, z) in reversed(pts)]
            w = cq.Workplane("YZ", origin=(x0, 0, 0)).polyline(poly).close().extrude(x1 - x0)
            blades.append(w.val())
        fr = 2.0
        frame = [box(x0 - fr, x0, y_in, y_out + 1.5, z0 - fr, z1 + fr), box(x1, x1 + fr, y_in, y_out + 1.5, z0 - fr, z1 + fr),
                 box(x0, x1, y_in, y_out + 1.5, z0 - fr, z0), box(x0, x1, y_in, y_out + 1.5, z1, z1 + fr)]
        add(f"{name} light trap: {nb} chevron blades (1 mm aluminium, six legs, 10 mm pitch, 32 mm deep), black anodised, in a 2 mm frame "
            f"on the back panel's inside", comp(blades + frame), C["black"], 12, (0, 180, 0), mat="al6061", mass_kg=0.0027 * nb * (x1 - x0) / 10.0,
            bom=bom, tags=TAG)
        return nb

    # ------------------------------------------------------------------ panel openings
    xi0, xi1 = INLET["x"]
    zi0, zi1 = INLET["z"]
    xe0, xe1 = EXHAUST["x"]
    ze0, ze1 = EXHAUST["z"]
    op_in = box(xi0 + 2.0, xi1 - 2.0, yb - 1.0, yb + G["panel_t"] + 1.0, zi0 + 2.0, zi1 - 2.0)
    op_ex = box(xe0 + 2.0, xe1 - 2.0, yb - 1.0, yb + G["panel_t"] + 1.0, ze0 + 2.0, ze1 - 2.0)
    s = pn.shape
    for t_ in (op_in, op_ex):
        s = s.cut(t_)
    pn.shape = s.clean() if hasattr(s, "clean") else s
    nb_in = louvre(xi0, xi1, zi0, zi1, "Guard inlet", "MC-02", (0, 180, 0))
    nb_ex = louvre(xe0, xe1, ze0, ze1, "Guard exhaust", "MC-02", (0, 180, 0))

    # ------------------------------------------------------------------ inlet filter (outside the back panel)
    yo = yb + G["panel_t"]
    ft = FILTER["t"]
    fr_ = box(xi0 - 6.0, xi1 + 6.0, yo, yo + ft + 1.5, zi0 - 6.0, zi1 + 6.0).cut(box(xi0, xi1, yo - 1.0, yo + ft + 3.0, zi0, zi1))
    pad = box(xi0, xi1, yo, yo + ft, zi0, zi1)
    add(f"Guard inlet filter: {FILTER['media']} ({xi1 - xi0:.0f} x {zi1 - zi0:.0f} mm) in a 1.5 mm aluminium frame on the back panel's outside; "
        "a duct from the dock can replace it", comp([pad, fr_]), C["panel"], 12, (0, 240, 0), mat="misc", mass_kg=0.15, bom="MC-03", tags=TAG)

    # ------------------------------------------------------------------ plenum, ducts, hood (1 mm sheet)
    t = SHEET_T

    def shell(x, y, z, open_faces=()):
        """a closed 1 mm box shell over the box (x, y, z) with the named faces left open"""
        outer = box(x[0], x[1], y[0], y[1], z[0], z[1])
        inner = box(x[0] + t, x[1] - t, y[0] + t, y[1] - t, z[0] + t, z[1] - t)
        sh = outer.cut(inner)
        big = 5.0
        cuts = {"-x": box(x[0] - big, x[0] + t + 0.01, y[0] + t, y[1] - t, z[0] + t, z[1] - t),
                "+x": box(x[1] - t - 0.01, x[1] + big, y[0] + t, y[1] - t, z[0] + t, z[1] - t),
                "-y": box(x[0] + t, x[1] - t, y[0] - big, y[0] + t + 0.01, z[0] + t, z[1] - t),
                "+y": box(x[0] + t, x[1] - t, y[1] - t - 0.01, y[1] + big, z[0] + t, z[1] - t),
                "-z": box(x[0] + t, x[1] - t, y[0] + t, y[1] - t, z[0] - big, z[0] + t + 0.01),
                "+z": box(x[0] + t, x[1] - t, y[0] + t, y[1] - t, z[1] - t - 0.01, z[1] + big)}
        for f in open_faces:
            sh = sh.cut(cuts[f])
        return sh

    P, D1, D2, H = PLENUM, DUCT1, DUCT2, HOOD
    plen = shell(P["x"], P["y"], P["z"], ("+y",))
    # the plenum's front wall gets the duct's mouth at its top
    plen = plen.cut(box(D1["x"][0] + t, D1["x"][1] - t, P["y"][0] - 1.0, P["y"][0] + t + 0.01, D1["z"][0] + t, min(D1["z"][1], P["z"][1]) - t))
    d1 = shell(D1["x"], D1["y"], D1["z"], ("+y", "-y"))
    d2 = shell(D2["x"], D2["y"], D2["z"], ())
    d2 = d2.cut(box(D1["x"][0] + t, D1["x"][1] - t, D2["y"][1] - t - 0.01, D2["y"][1] + 1.0, D2["z"][0] + t, D2["z"][1] - t))   # duct 1 enters
    fo = H["floor_opening_x"]
    d2 = d2.cut(box(fo[0], fo[1], D2["y"][0] + t, D2["y"][1] - t, D2["z"][0] - 1.0, D2["z"][0] + t + 0.01))                    # down into the hood
    add("Hood duct: plenum behind the inlet trap's right-hand part and a duct over the side camera (1 mm aluminium, riveted; "
        f"{D1['x'][1] - D1['x'][0]:.0f} x {D1['z'][1] - D1['z'][0]:.0f} mm, then {D2['x'][1] - D2['x'][0]:.0f} x {D2['z'][1] - D2['z'][0]:.0f} mm)",
        comp([plen, d1, d2]), C["panel"], 12, (0, 120, 160), mat="al6061", mass_kg=0.45, bom="MC-04", tags=TAG)
    # hood: sides, back and top over the camera body; open at the lens end (+x) and the bottom (the bracket closes part of it)
    hx, hy, hz = H["x"], H["y"], H["z"]
    brb = find("Side camera bracket")[0].shape.BoundingBox()
    floor = box(hx[0], hx[1], hy[0], hy[1], hz[0], hz[0] + t).cut(box(brb.xmin - 1.0, brb.xmax + 1.0, brb.ymin - 1.0, brb.ymax + 1.0,
                                                                       hz[0] - 1.0, hz[0] + t + 1.0))
    hood = [box(hx[0], hx[1], hy[0], hy[0] + t, hz[0] + t, hz[1] - t),      # -y side
            box(hx[0], hx[1], hy[1] - t, hy[1], hz[0] + t, hz[1] - t),      # +y side
            box(hx[0], hx[0] + t, hy[0] + t, hy[1] - t, hz[0] + t, hz[1] - t),   # back
            floor]                                                          # floor, cut round the bracket plate
    add("Side camera hood (1 mm aluminium: sides, back and floor round the Chronos body, the duct's floor is its top; open at the lens end)",
        comp(hood), C["panel"], 12, (-150, 0, 120), mat="al6061", mass_kg=0.25, bom="MC-04", tags=TAG)
    fc = np.array(FAN_HOOD["centre"])
    fs, fd = FAN_HOOD["size"], FAN_HOOD["depth"]
    fan_h = box(fc[0] - fs / 2, fc[0] + fs / 2, fc[1] - fd / 2, fc[1] + fd / 2, fc[2] - fs / 2, fc[2] + fs / 2)
    fan_h = fan_h.cut(cyl(fs / 2 - 2.0, (fc[0], fc[1] - fd, fc[2]), "y", 2 * fd)).fuse(cyl(15.0, (fc[0], fc[1] - fd / 2, fc[2]), "y", fd))
    add(f"Hood fan in the duct ({FAN_HOOD['part']}), blowing toward the camera", fan_h, C["black"], 12, (0, 120, 220), mat="misc", mass_kg=0.05,
        bom="MC-05", tags=TAG)

    # ------------------------------------------------------------------ exhaust plenum and fans outside the back panel
    yp0, yp1 = EXH_PLENUM["y"]
    nf, fsz, fdp = FAN_EXH["n"], FAN_EXH["size"], FAN_EXH["depth"]
    fx0, fz0 = FAN_EXH["x0"], FAN_EXH["z0"]
    ex_w = (xe0 - 2.0, fx0 + nf * fsz + 2.0)
    ex_z = (min(ze0, fz0) - 2.0, max(ze1, fz0 + fsz) + 2.0)
    pl = box(ex_w[0], ex_w[1], yp0, yp1, ex_z[0], ex_z[1]).cut(box(ex_w[0] + 1.5, ex_w[1] - 1.5, yp0 - 1.0, yp1 + 1.0, ex_z[0] + 1.5, ex_z[1] - 1.5))
    add("Guard exhaust plenum outside the back panel (1.5 mm aluminium, gasketed to the panel)", pl, C["panel"], 12, (0, 240, 0), mat="al6061",
        mass_kg=0.2, bom="MC-04", tags=TAG)
    fans = []
    for i in range(nf):
        x0 = fx0 + i * fsz
        f = box(x0, x0 + fsz, yp1, yp1 + fdp, fz0, fz0 + fsz)
        f = f.cut(cyl(fsz / 2 - 3.0, (x0 + fsz / 2, yp1 - 1.0, fz0 + fsz / 2), "y", fdp + 2.0)).fuse(cyl(20.0, (x0 + fsz / 2, yp1, fz0 + fsz / 2), "y", fdp))
        g = box(x0, x0 + fsz, yp1 + fdp, yp1 + fdp + FAN_EXH["guard"], fz0, fz0 + fsz).cut(
            cyl(fsz / 2 - 3.0, (x0 + fsz / 2, yp1 + fdp - 1.0, fz0 + fsz / 2), "y", FAN_EXH["guard"] + 2.0))
        fans += [f, g]
    add(f"Guard exhaust fans ({nf} x {FAN_EXH['part']}) with finger guards, blowing out of the back of the guard", comp(fans), C["black"], 12,
        (0, 260, 0), mat="misc", mass_kg=0.17 * nf, bom="MC-01", tags=TAG)

    # ------------------------------------------------------------------ G-10 under the side camera bracket's root
    br = find("Side camera bracket")[0]
    bbb = br.shape.BoundingBox()
    x_face = bbb.xmax                                                    # the root's face on the floor plate (x -156)
    tg = G10_ROOT["t"]
    br.shape = br.shape.cut(box(x_face - tg, x_face + 1.0, bbb.ymin - 1.0, bbb.ymax + 1.0, bbb.zmin - 1.0, bbb.zmax + 1.0))
    br.name = br.name.replace("on an angle root bolted", f"on an angle root, {tg:.0f} mm shorter for a G-10 break, bolted")
    root_z = (-20.0, -4.0)                                               # the floor plate's edge the root bolts to (mechanics.md §1)
    import frame_features as FF
    fy, fz = FF.FIBRE_HEAD["yz"]
    pad = box(x_face - tg, x_face, bbb.ymin, bbb.ymax, root_z[0], root_z[1]).cut(
        box(x_face - 25.0, x_face + 0.1, fy - FF.FIBRE_HEAD["flange_r"] - 2.0, fy + FF.FIBRE_HEAD["flange_r"] + 2.0, fz - 8.5, fz + 8.5))
    add(f"G-10 thermal break under the side camera bracket's root ({tg:.0f} mm G-10/FR-4, {bbb.ymax - bbb.ymin:.0f} x {root_z[1] - root_z[0]:.0f} mm; "
        "screws in G-10 shoulder washers)", pad, C["yellow"], 12, (-200, 0, 0),
        mat="misc", mass_kg=0.015, bom="MC-06", tags=TAG)

    # ------------------------------------------------------------------ G-10 ring in the LP camera's filter holder
    import monitoring_spec as MS
    lp = MS.VIEWPORTS["LP"]
    c = np.array(lp["centre"], float)
    d = np.array(MS.axis_to_target(lp["centre"]))
    a = -d
    s_top = float(getattr(MS, "LP_GEOM", {}).get("s_top", 34.0))
    p0 = c + (s_top + 3.0) * a
    tr = G10_RING["t"]
    flt = find("LP camera filters")[0]
    cutter = cq.Solid.makeCylinder(20.0, tr + 0.05, V(*map(float, p0 - 0.02 * a)), V(*map(float, a)))
    flt.shape = flt.shape.cut(cutter)
    flt.name = flt.name.replace("in an SM1 holder", f"in an SM1 holder on a {tr:.0f} mm G-10 ring")
    ring = cq.Solid.makeCylinder(G10_RING["od"] / 2, tr, V(*map(float, p0)), V(*map(float, a))).cut(
        cq.Solid.makeCylinder(G10_RING["id"] / 2 + 0.5, tr + 1.0, V(*map(float, p0 - 0.5 * a)), V(*map(float, a))))
    add(f"G-10 thermal break ring under the LP camera's filter holder (Ø{G10_RING['od']:.0f} x Ø{G10_RING['id']:.1f} x {tr:.0f} mm, "
        "SM1-threaded both ends)", ring, C["yellow"], 7, (0, 0, 345), mat="misc", mass_kg=0.004, bom="MC-06", tags=TAG)

    # ------------------------------------------------------------------ PB2: a 40 mm fan on its +x end wall
    pb2 = find("PB2 process-module box")[0]
    pbb = pb2.shape.BoundingBox()
    fs4, fd4 = FAN_PB2["size"], FAN_PB2["depth"]
    yc4, zc4 = 0.5 * (pbb.ymin + pbb.ymax), 0.5 * (pbb.zmin + pbb.zmax)
    f4 = box(pbb.xmax, pbb.xmax + fd4, yc4 - fs4 / 2, yc4 + fs4 / 2, zc4 - fs4 / 2, zc4 + fs4 / 2)
    add(f"PB2 vent fan ({FAN_PB2['part']}) on PB2's +x end wall over a Ø38 hole; a filtered vent at the other end", f4, C["black"], 12,
        (120, 0, 120), mat="misc", mass_kg=0.02, bom="MC-07", tags=TAG)

    # ------------------------------------------------------------------ the LP camera's Pi in a heat-sink case on the bridge
    zb1 = h.P["z_bridge1"]
    pc = PI2_CASE
    case = box(pc["x"][0], pc["x"][1], pc["y"][0], pc["y"][1], zb1 + pc["z_gap"], zb1 + pc["z_gap"] + pc["h"])
    add(f"LP camera's Pi: {pc['part']} on the optics bridge, on four 0.5 mm pads; CSI ribbon to the LP camera", case, C["alu_dark"], 12,
        (0, 0, 300), mat="misc", mass_kg=0.25, bom="MC-08", tags=TAG)

    REPORT.update(inlet=dict(opening=INLET, blades=nb_in, face_m2=round(opening_area_m2("inlet"), 4)),
                  exhaust=dict(opening=EXHAUST, blades=nb_ex, face_m2=round(opening_area_m2("exhaust"), 4)),
                  hood=HOOD, duct1=DUCT1, duct2=DUCT2, plenum=PLENUM, pb2=dict(bbox=[round(v, 1) for v in (pbb.xmin, pbb.ymin, pbb.zmin, pbb.xmax, pbb.ymax, pbb.zmax)]),
                  bracket_root_face_x=round(x_face, 2), lp_ring_at=(p0.round(1).tolist()))
    return REPORT
