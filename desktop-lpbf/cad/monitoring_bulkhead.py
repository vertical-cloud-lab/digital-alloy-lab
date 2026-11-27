"""The guard's monitoring bulkhead plate, MN-28 (issue #260, PR 281; monitoring/mechanics.md §1, monitoring-io.csv MN-28).

monitoring_parts._bulkhead() calls draw() here. The numbers live in this file, so the notes and checks read the geometry the model
draws. Importing it needs no cadquery.

Where: the guard's back panel, upper left (plate x -400..-220, z 220..346, on the panel's outside). The left panel is out: it stands
6.5 mm from the rack's vented side panel (x -428), with no room for a connector, its plug or a bend. The back panel's left part is
the nearest to the rack that has room: the cables leave toward +y and turn toward the rack's open back (y 300). The plate sits
above the inlet's filter frame (z <= 208) and below the guard's top rail (inside, z >= 346.1); its cut-out stays clear of the
back-left frame post (inside, x <= -400) and of the inlet trap (z <= 204). Inside, the connectors stand above the optics bridge
(z 211-236 for y <= 180) and behind the collimator (y 75-115, z 251-291), which their cables pass over at z 318.

What is drawn (all tagged "monitoring"; vendor parts are envelopes built from the dimensions named in each part's name):
  * the plate, 6061 0.080 in., laser-cut, screwed over a cut-out in the 1.6 mm back panel with 8 x M4 into rivet nuts, bare
    faces together: the bond to the guard;
  * one row at z 318: three isolated BNC feedthroughs (Neutrik NBB75DFIB, D-size), an RJ45 feedthrough (Neutrik NE8FDX-P6-B,
    shielded Cat6A, D-size) and an M12 8-pole A-coded feed-through (Murrelektronik 7000-48111-0000000);
  * below them a split cable entry for pre-terminated leads (icotek KEL 10|6, six KT grommets), and inside, over its cut-out,
    a black-anodised labyrinth shroud: the leads turn toward +x inside it and leave through a channel whose side wall stops
    every straight path from the guard to the grommets (light_check());
  * the mating plugs and cables on both sides, as envelopes: outside, a 40 mm bend toward the rack; inside, straight forward.
"""
from __future__ import annotations

import math

# ------------------------------------------------------------------------------------------------- the guard's back panel
Y_IN = 215.0                      # back panel, inner face (lpbf_low.py §12: gy1)
PANEL_T = 1.5
Y_OUT = Y_IN + PANEL_T            # 216.5, its outer face: the plate's inner face
FRAME = dict(post_x=-400.0, rail_z=346.11, bridge_top=236.11, bridge_back_y=180.0)   # what bounds the cut-out (checked in draw())

# ------------------------------------------------------------------------------------------------- the plate and the panel's cut-out
PLATE = dict(t=2.03, x=(-400.0, -220.0), z=(220.0, 346.0), r=6.0,
             what="6061-T6 sheet 0.080 in. (2.03 mm), laser-cut; bare, or clear chromate conversion coat, so its face bonds to the panel")
CUT = dict(x=(-386.0, -234.0), z=(234.0, 332.0))                    # 152 x 98 mm out of the back panel, under the plate
SCREWS = [(-393.0, 227.0), (-310.0, 227.0), (-227.0, 227.0), (-393.0, 339.0), (-310.0, 339.0), (-227.0, 339.0),
          (-393.0, 283.0), (-227.0, 283.0)]                          # 8 x M4, 7 mm outside the cut-out: Ø4.5 in the plate, Ø6.0 rivet nuts
SCREW_D, RIVNUT_D, RIVNUT_BULGE = 4.5, 6.0, 9.0                      # a set M4 rivet nut bulges to ~Ø9 behind the panel (envelope)

# ------------------------------------------------------------------------------------------------- the connectors (one row at z 318)
# Neutrik D-size: 26 x 31 mm flange, Ø24 cut-out and two Ø3.2 screw holes 19 mm apart across and 24 mm up, on a diagonal (Neutrik's
# D-series panel cut-out, as on its NL4MDXX drawing). Thickness of the flange and the body behind the plate are envelopes.
DS = dict(flange=(26.0, 31.0), flange_t=3.0, hole_d=24.0, screw_d=3.2, screw_dx=9.5, screw_dz=12.0, body_d=23.5, body_L1=12.0,
          jack_d=15.0, rj_box=(17.0, 15.0), body_L=32.0)
ROW_Z = 318.0
BNC_X = (-370.0, -340.0, -310.0)                                     # MN-13, MN-14, MN-17
RJ45_X = -280.0                                                      # MN-10
# Murrelektronik 7000-48111-0000000 (AutomationDirect's drawing): 34.3 mm long, SW18 collar, female end Ø14.7; Ø16.1 hole and a 4.5 mm
# wall at most (AutomationDirect's catalogue). Mounted collar and female end outside, the M16 nut and the male end inside. The nut
# (Ø24) and the collar's 3 mm are envelopes.
M12 = dict(x=-250.0, hole_d=16.1, collar_d=20.8, collar_t=3.0, front_d=14.7, front_L=9.0, thread_d=16.0, L=34.3, nut_d=24.0, nut_t=3.0)

# ------------------------------------------------------------------------------------------------- the split cable entry and its shroud
# icotek KEL 10|6 (part 42216), from icotek's KEL datasheet: frame 98 x 58 x 17 mm, cut-out 65 x 36 mm, 4 x Ø5.8 holes, six KT
# grommets (cables up to 17 mm), IP54, flat gasket included. Screw spacing 83 x 32 mm read off icotek's KEL 10 drawing (a catalogue
# extract): an envelope.
KEL = dict(x=-336.0, z=270.5, L=98.0, W=58.0, H=17.0, cut=(65.0, 36.0), screws=(83.0, 32.0), screw_d=5.8, pitch=(21.7, 18.0))
LEADS = [(-21.7, -9.0, 5.0, "MN-11 Chronos power"), (0.0, -9.0, 5.0, "MN-15 LDS12B, photodiode 1"),
         (21.7, -9.0, 5.0, "MN-15 LDS12B, photodiode 2")]          # grommet offsets from the KEL's centre, lead OD; the top row is spare
# the shroud (1.5 mm sheet): a box over the cut-out, D deep; its front wall stops s past the cut-out's +x edge; a channel h wide runs
# on to the side wall, which reaches w beyond the front wall. A straight path from the open channel to the cut-out needs
# w <= h D / s; w is larger (light_check()).
SHROUD = dict(t=1.5, margin=5.0, margin_x=1.5, D=34.0, s=30.0, h=24.0, w=30.0, flange=8.0, flange_x=12.0,
              what="1.5 mm 5052, bent and riveted, black anodised; flanged all round on the plate's inside, its -x flange under the KEL's two "
                   "left M5 screws, the rest riveted")

# ------------------------------------------------------------------------------------------------- plugs and cables (envelopes)
PLUG = dict(bnc=(14.5, 45.0, 5.0), rj45=((12.0, 14.0), 38.0, 7.5), m12=(20.0, 45.0, 7.0))   # (Ø or w x h, length, cable OD)
BEND_OUT = 40.0                  # mm, the outside cables' first bend (Cat6 S/FTP 7.5 mm: 4-5 x OD)
BEND_LEAD = 25.0                 # the leads' bend outside (5 mm DC leads: 5 x OD)
INSIDE_TO_Y = 110.0              # the inside cables run straight forward to here (over the collimator) in the model

REPORT: dict = {}


def light_check():
    """the shroud's straight-path test in the x-y plane. The cut-out spans x <= b1 on the plate (y = Y_OUT); the front wall's end is at
    (X_f, Y_OUT - D) with X_f = b1 + s; the side wall at X_b = X_f + h runs from the plate to y = Y_OUT - D - w. A ray from the open channel
    to the cut-out must pass between the front wall's end and the side wall; traced back it meets the plane y = Y_OUT - D - w at
    x = X_f + w s / D for the shallowest one (through the wall's end to the cut-out's edge). If that is beyond X_b (w s / D > h) it
    crossed the side wall: no straight path. Top and bottom walls close the channel, so any ray with a z component is caught too."""
    S = SHROUD
    reach = S["w"] * S["s"] / S["D"]
    return dict(shallowest_ray_x_past_front_wall_end_mm=round(reach, 2), channel_width_mm=S["h"], margin_mm=round(reach - S["h"], 2),
                w_min_mm=round(S["h"] * S["D"] / S["s"], 2), w_mm=S["w"], ok=reach > S["h"],
                extreme_ray_lands_past_cutout_edge_mm=round(S["s"] - S["D"] * S["h"] / S["w"], 2))


def shroud_box():
    """the shroud's outer extent: x0, x1, y0 (mouth plane), z0, z1, and its key planes"""
    S, K = SHROUD, KEL
    b0, b1 = K["x"] - K["cut"][0] / 2, K["x"] + K["cut"][0] / 2
    a0, a1 = K["z"] - K["cut"][1] / 2, K["z"] + K["cut"][1] / 2
    t, m, mx = S["t"], S["margin"], S["margin_x"]
    X_f = b1 + S["s"]
    X_b = X_f + S["h"]
    return dict(b0=b0, b1=b1, a0=a0, a1=a1, x_in0=b0 - mx, x0=b0 - mx - t, X_f=X_f, X_b=X_b, x1=X_b + t,
                z_in0=a0 - m, z_in1=a1 + m, z0=a0 - m - t, z1=a1 + m + t, y_front=Y_OUT - S["D"], y_mouth=Y_OUT - S["D"] - S["w"])


# ================================================================================================================ drawing
def draw(parts, add, h, module="M50"):
    import cadquery as cq

    V = cq.Vector
    C, box, cyl, comp, fuse = h.C, h.box, h.cyl, h.comp, h.fuse
    TAG = ("monitoring",)
    REPORT.clear()
    P, t = PLATE, PLATE["t"]
    y_pl1 = Y_OUT + t                                                   # the plate's outer face

    pn = [p for p in parts if p.name.startswith("Laser guard panels")][0]
    bb = pn.shape.BoundingBox()
    assert abs(bb.ymax - Y_OUT) < 0.6, bb.ymax
    # what the cut-out and the plate must stay clear of
    assert min(x for x, _ in SCREWS) - RIVNUT_BULGE / 2 > FRAME["post_x"] + 1.5, "rivet nuts too near the back-left post"
    assert max(z for _, z in SCREWS) + RIVNUT_BULGE / 2 < FRAME["rail_z"] - 1.5, "rivet nuts too near the top rail"
    assert all(min(abs(x - CUT["x"][0]), abs(x - CUT["x"][1]), abs(z - CUT["z"][0]), abs(z - CUT["z"][1])) >= 7.0 - 1e-6
               for x, z in SCREWS), "rivet nuts too near the cut-out's edge"
    assert P["z"][0] > 208.0 + 10.0, "plate too near the inlet filter's frame (z 208)"

    # ------------------------------------------------------------------ the panel's cut-out and the rivet nuts' holes
    s = pn.shape
    s = s.cut(box(CUT["x"][0], CUT["x"][1], Y_IN - 1.0, Y_OUT + 1.0, CUT["z"][0], CUT["z"][1]))
    for (x, z) in SCREWS:
        s = s.cut(cyl(RIVNUT_D / 2, (x, Y_IN - 1.0, z), "y", PANEL_T + 2.0))
    pn.shape = s.clean() if hasattr(s, "clean") else s

    # ------------------------------------------------------------------ the plate
    plate = h.rbox(P["x"][0], P["x"][1], Y_OUT, y_pl1, P["z"][0], P["z"][1], P["r"], edges="|Y")
    holes = []
    for x in BNC_X + (RJ45_X,):
        holes += [cyl(DS["hole_d"] / 2, (x, Y_OUT - 1.0, ROW_Z), "y", t + 2.0),
                  cyl(DS["screw_d"] / 2, (x - DS["screw_dx"], Y_OUT - 1.0, ROW_Z + DS["screw_dz"]), "y", t + 2.0),
                  cyl(DS["screw_d"] / 2, (x + DS["screw_dx"], Y_OUT - 1.0, ROW_Z - DS["screw_dz"]), "y", t + 2.0)]
    holes.append(cyl(M12["hole_d"] / 2, (M12["x"], Y_OUT - 1.0, ROW_Z), "y", t + 2.0))
    K = KEL
    holes.append(box(K["x"] - K["cut"][0] / 2, K["x"] + K["cut"][0] / 2, Y_OUT - 1.0, y_pl1 + 1.0, K["z"] - K["cut"][1] / 2, K["z"] + K["cut"][1] / 2))
    for sx in (-1, 1):
        for sz in (-1, 1):
            holes.append(cyl(K["screw_d"] / 2, (K["x"] + sx * K["screws"][0] / 2, Y_OUT - 1.0, K["z"] + sz * K["screws"][1] / 2), "y", t + 2.0))
    for (x, z) in SCREWS:
        holes.append(cyl(SCREW_D / 2, (x, Y_OUT - 1.0, z), "y", t + 2.0))
    for hh in holes:
        plate = plate.cut(hh)
    add(f"Guard bulkhead plate (MN-28: 6061 0.080 in. = 2.03 mm, {P['x'][1] - P['x'][0]:.0f} x {P['z'][1] - P['z'][0]:.0f} mm, laser-cut: four "
        "D-size cut-outs, an M12 hole and the KEL's cut-out; on the guard's back panel over a 152 x 98 mm cut-out, 8 x M4 into rivet nuts, "
        "bare faces together for the bond)", plate, C["alu"], 12, (0, 260, 0), mat="al6061", mass_kg=round(plate.Volume() * 2.70e-6, 3),
        bom="M0-B1", tags=TAG)

    # ------------------------------------------------------------------ D-size feedthroughs: 3 x isolated BNC, 1 x RJ45
    fw, fh = DS["flange"]

    def dsize(x, rj45=False):
        fl = box(x - fw / 2, x + fw / 2, y_pl1, y_pl1 + DS["flange_t"], ROW_Z - fh / 2, ROW_Z + fh / 2)
        body = cyl(DS["body_d"] / 2, (x, y_pl1, ROW_Z), "-y", t + DS["body_L1"])
        y_b = Y_OUT - DS["body_L1"]
        L2 = DS["body_L"] - DS["body_L1"]
        if rj45:
            bw, bh = DS["rj_box"]
            rear = box(x - bw / 2, x + bw / 2, y_b - L2, y_b, ROW_Z - bh / 2, ROW_Z + bh / 2)
        else:
            rear = cyl(DS["jack_d"] / 2, (x, y_b, ROW_Z), "-y", L2)
        return fuse([fl, body, rear])

    add("Guard bulkhead isolated BNC feedthroughs (3 x Neutrik NBB75DFIB, black D-shape, isolated from the plate: MN-13, MN-14, MN-17; "
        "D-size flange 26 x 31 and Ø24 cut-out per Neutrik's D-series, 3 mm flange and a Ø23.5 then Ø15 body 32 mm behind the plate: envelope)",
        comp([dsize(x) for x in BNC_X]), C["black"], 12, (0, 280, 0), mat="misc", mass_kg=0.03 * len(BNC_X), bom="M0-B2", tags=TAG)
    add("Guard bulkhead RJ45 feedthrough (Neutrik NE8FDX-P6-B etherCON Cat6A, shielded, black D-shape: MN-10; D-size flange and cut-out per "
        "Neutrik's D-series, body 32 mm behind the plate: envelope)", dsize(RJ45_X, rj45=True), C["black"], 12, (0, 280, 0), mat="misc",
        mass_kg=0.03, bom="M0-B3", tags=TAG)

    # ------------------------------------------------------------------ M12 8-pole feed-through
    M_ = M12
    y_front = y_pl1 + M_["collar_t"] + M_["front_L"]                    # the female end, outside
    y_in_end = y_front - M_["L"]
    m12 = fuse([cyl(M_["collar_d"] / 2, (M_["x"], y_pl1, ROW_Z), "y", M_["collar_t"]),
                cyl(M_["front_d"] / 2, (M_["x"], y_pl1 + M_["collar_t"], ROW_Z), "y", M_["front_L"]),
                cyl(M_["thread_d"] / 2, (M_["x"], y_pl1 + 0.01, ROW_Z), "-y", y_pl1 + 0.01 - y_in_end),
                cyl(M_["nut_d"] / 2, (M_["x"], Y_OUT, ROW_Z), "-y", M_["nut_t"])])
    add("Guard bulkhead M12 8-pole A-coded feed-through (Murrelektronik 7000-48111-0000000, shielded, male/female: MN-02 to MN-05; 34.3 mm "
        "long, SW18 collar, Ø14.7 female end outside, Ø16.1 hole, from AutomationDirect's drawing; the M16 nut Ø24 x 3: envelope)", m12, C["ss"], 12,
        (0, 280, 0), mat="misc", mass_kg=0.03, bom="M0-B4", tags=TAG)

    # ------------------------------------------------------------------ KEL 10|6 frame with its grommets (outside)
    kx0, kx1 = K["x"] - K["L"] / 2, K["x"] + K["L"] / 2
    kz0, kz1 = K["z"] - K["W"] / 2, K["z"] + K["W"] / 2
    frame = box(kx0, kx1, y_pl1, y_pl1 + K["H"], kz0, kz1)
    lead_holes = [cyl(od / 2 + 0.25, (K["x"] + dx, y_pl1 - 1.0, K["z"] + dz), "y", K["H"] + 2.0) for (dx, dz, od, _) in LEADS]
    for lh in lead_holes:
        frame = frame.cut(lh)
    add("Guard bulkhead split cable entry (icotek KEL 10|6, 42216: frame 98 x 58 x 17, cut-out 65 x 36 and 4 x Ø5.8 from icotek's datasheet, "
        "drawn solid; six KT grommets, one per pre-terminated lead (MN-11, MN-15 x 2) and three spare, IP54)", frame, C["black"], 12, (0, 300, 0),
        mat="misc", mass_kg=0.06, bom="M0-B5", tags=TAG)

    # ------------------------------------------------------------------ the labyrinth shroud (inside)
    S, B = SHROUD, shroud_box()
    st, fl_, flx = S["t"], S["flange"], S["flange_x"]
    yF, yM = B["y_front"], B["y_mouth"]
    walls = [
        box(B["x0"], B["X_f"], yF - st, yF, B["z0"], B["z1"]),                         # front wall, D off the plate, to X_f
        box(B["x0"], B["x_in0"], yF - st, Y_OUT, B["z0"], B["z1"]),                    # -x end wall
        box(B["X_b"], B["x1"], yM, Y_OUT, B["z0"], B["z1"]),                           # the channel's side wall, out to the mouth
        box(B["x0"], B["x1"], yF - st, Y_OUT, B["z_in1"], B["z1"]),                    # top over the box ...
        box(B["X_f"], B["x1"], yM, yF, B["z_in1"], B["z1"]),                           # ... and over the channel
        box(B["x0"], B["x1"], yF - st, Y_OUT, B["z0"], B["z_in0"]),                    # bottom over the box ...
        box(B["X_f"], B["x1"], yM, yF, B["z0"], B["z_in0"]),                           # ... and under the channel
        # flanges on the plate's inside (y Y_OUT - t .. Y_OUT): -x outward under the KEL's left screws, +x outward, top and bottom
        box(B["x0"] - flx, B["x0"], Y_OUT - st, Y_OUT, B["z0"], B["z1"]),
        box(B["x1"], B["x1"] + fl_, Y_OUT - st, Y_OUT, B["z0"], B["z1"]),
        box(B["x0"] - flx, B["x1"] + fl_, Y_OUT - st, Y_OUT, B["z1"], B["z1"] + fl_),
        box(B["x0"] - flx, B["x1"] + fl_, Y_OUT - st, Y_OUT, B["z0"] - fl_, B["z0"]),
    ]
    shroud = fuse(walls)
    for sx in (-1, 1):
        for sz in (-1, 1):
            shroud = shroud.cut(cyl(K["screw_d"] / 2, (K["x"] + sx * K["screws"][0] / 2, Y_OUT - 3.0, K["z"] + sz * K["screws"][1] / 2), "y", 4.0))
    lc = light_check()
    assert lc["ok"], lc
    add(f"Guard bulkhead cable-entry light shroud (a labyrinth over the KEL's inside: 1.5 mm aluminium, black anodised, {S['D']:.0f} mm deep; the "
        f"leads turn toward +x and leave through a {S['h']:.0f} mm channel whose side wall reaches {S['w']:.0f} mm past the front wall, so no "
        "straight path reaches the grommets)", shroud, C["black"], 12, (0, 120, 0), mat="al6061", mass_kg=round(shroud.Volume() * 2.68e-6, 3),
        bom="M0-B6", tags=TAG)

    # ------------------------------------------------------------------ mating plugs and cables, outside (envelopes)
    def arc_pts(p0, d0, d1, R, n=7):
        """points of a quarter bend of radius R starting at p0 heading d0 and ending heading d1 (unit axis vectors)"""
        c = [p0[k] + R * d1[k] for k in range(3)]
        return [tuple(c[k] - R * d1[k] * math.cos(a) + R * d0[k] * math.sin(a) for k in range(3))
                for a in [i * (math.pi / 2) / (n - 1) for i in range(n)]]

    def cable(p_start, y_bend, R, od, stub=20.0):
        pts = [p_start, (p_start[0], y_bend, p_start[2])]
        arc = arc_pts((p_start[0], y_bend, p_start[2]), (0, 1, 0), (-1, 0, 0), R)
        pts += arc[1:] + [(arc[-1][0] - stub, arc[-1][1], arc[-1][2])]
        return h.polyline_pipe(pts, od / 2, n=4)

    out = []
    y_bend0 = 272.0
    conns = [("bnc", x) for x in BNC_X] + [("rj45", RJ45_X), ("m12", M12["x"])]
    for i, (kind, x) in enumerate(conns):
        if kind == "bnc":
            d, L, od = PLUG["bnc"]
            y0 = y_pl1 + DS["flange_t"]
            out.append(cyl(d / 2, (x, y0, ROW_Z), "y", L))
        elif kind == "rj45":
            (w_, h_), L, od = PLUG["rj45"]
            y0 = y_pl1 + DS["flange_t"]
            out.append(box(x - w_ / 2, x + w_ / 2, y0, y0 + L, ROW_Z - h_ / 2, ROW_Z + h_ / 2))
        else:
            d, L, od = PLUG["m12"]
            y0 = y_front
            out.append(cyl(d / 2, (x, y0, ROW_Z), "y", L))
        out.append(cable((x, y0 + L - 1.0, ROW_Z), y_bend0 + 10.0 * i, BEND_OUT, od))
    y_k = y_pl1 + K["H"]
    for j, (dx, dz, od, _) in enumerate(LEADS):
        out.append(cable((K["x"] + dx, y_pl1 + 1.0, K["z"] + dz), y_k + 10.0 + 12.0 * j, BEND_LEAD, od, stub=15.0))
    add("Guard bulkhead mating plugs and cables outside the guard (straight BNC, RJ45 and M12 plugs, then a 40 mm bend toward the rack; the "
        "KEL's three leads with a 25 mm bend: envelopes, cables of M1-03, MN-10 and MN-02)", comp(out), C["hose"], 12, (0, 340, 0), mat="misc",
        mass_kg=0.15, tags=TAG)

    # ------------------------------------------------------------------ mating plugs and cables, inside (envelopes)
    ins = []
    y_rear = Y_OUT - DS["body_L"]
    for kind, x in conns:
        if kind == "bnc":
            d, L, od = PLUG["bnc"]
            y0 = y_rear
            ins.append(cyl(d / 2, (x, y0, ROW_Z), "-y", L))
        elif kind == "rj45":
            (w_, h_), L, od = PLUG["rj45"]
            y0 = y_rear
            ins.append(box(x - w_ / 2, x + w_ / 2, y0 - L, y0, ROW_Z - h_ / 2, ROW_Z + h_ / 2))
        else:
            d, L, od = PLUG["m12"]
            y0 = y_in_end
            ins.append(cyl(d / 2, (x, y0, ROW_Z), "-y", L))
        ins.append(cyl(od / 2, (x, y0 - L + 1.0, ROW_Z), "-y", y0 - L + 1.0 - INSIDE_TO_Y))
    add("Guard bulkhead mating plugs and cables inside the guard (straight BNC, RJ45 and M12 plugs; the cables run straight forward at z 318 "
        "over the collimator: envelopes)", comp(ins), C["hose"], 12, (0, 60, 0), mat="misc", mass_kg=0.08, tags=TAG)

    REPORT.update(plate=dict(x=P["x"], z=P["z"], y=(Y_OUT, round(y_pl1, 2)), t=t), panel_cutout=CUT, screws=SCREWS,
                  row_z=ROW_Z, bnc_x=BNC_X, rj45_x=RJ45_X, m12_x=M12["x"], kel=dict(x=K["x"], z=K["z"]),
                  shroud={k: round(v, 2) for k, v in B.items()}, light_check=lc,
                  inside_rear_y=round(min(y_rear, y_in_end), 2))
    return REPORT
