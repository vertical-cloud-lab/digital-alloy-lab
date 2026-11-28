"""Milling CAM for option B's weld-alignment fixture, checked by cutting it in CAMotics and comparing with the CAD.

    python cam/mill_cam.py            # writes cam/gcode/fixture_op1.nc, fixture_op2.nc, cam/out/mill_sim.json + PNGs
                                      # (needs Docker and the camotics:1.2.0 image, see CAMOTICS below)

The part: a 6061-T6 V-block, 120 x 114.3 x 60 mm, that holds each of option B's two welded parts coaxial while it
is tacked and welded (each part's 3 in ferrule overhangs one end of the block). A 90 deg V carries the 3 in body tube (76.2 OD), the reducer's 3 in end and, on a folded 0.025 in (0.64 mm) shim, the KF-50 flange
rim (74.93 OD): in a 90 deg V the axis sits r*sqrt(2) above the apex, so a cylinder 0.635 mm smaller in radius
needs a 0.635 mm shim on each flank to share the axis. The 2 in stub and the reducer's cone clear the V. There is
no slot under the seams: the V supports everything continuously and the welds are made on top as the part rolls.
A 6 mm relief along the apex keeps the tube off the sharp corner. Four M6 tapped holes take two strap clamps.

Stock: 6061-T6 flat bar 2-1/2 x 4-1/2 in (63.5 x 114.3), sawn to 120 (ends and sides as sawn/as rolled).
Setup 1: bottom up, face 0.5 mm. Setup 2: top up, face 3.0 mm to 60.0; rough the V in 2 mm z-levels with a 12 mm
end mill, leaving 0.3 mm on the flanks; finish both flanks with a 12.7 mm 90 deg chamfer mill in passes down the
flank; cut the apex relief with a 6 mm end mill; spot, drill and tap 4 x M6.
Programs: LinuxCNC/Haas-style metric G-code, no canned cycles (CAMotics 1.2.0 does not run G83/G84), the drill
pecks and the tap written out as G1 moves.

Check: each setup is cut in CAMotics 1.2.0 (camsim, Docker image built from desktop-lpbf's camotics.Dockerfile on
PR #266) on the stock, and the result is compared with the CAD in sections (x = 60, 120.65, 150, 225 and z = -5):
gouge = area the CAD keeps but the cut removed, leftover = area the CAD removes but the cut kept, each with its
largest depth. Rapid moves are checked against the in-process stock as well.
"""

import json
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import params as P  # noqa: E402

OUT = HERE / "out"
GC = HERE / "gcode"
WORK = Path("/tmp/fixture-camotics")
for d in (OUT, GC, WORK):
    d.mkdir(parents=True, exist_ok=True)
IMAGE = "camotics:1.2.0"
SHIFT = 1000.0

# ----------------------------------------------------------------------------------------------- part
# 120 mm long so that each welded part's 3 in ferrule (flange OD 90.9, wider than the V) overhangs an end:
# the upper part sits KF flange on the shim at x = 0 with its ferrule past x = 120; the pot sits ferrule past x = 0
# with its tube and end cap (both 76.2 OD) in the V.
L = 120.0
W, H = 114.3, 60.0
STOCK_H = 63.5
V_HALF = 36.0                  # half-width of the V at the top face; apex depth = V_HALF (90 deg)
APEX_W, APEX_Z = 6.0, -38.0    # relief slot along the apex
SEAM_X = P.B["stub_len"] + P.B["reducer_len"]     # reducer-to-body seam, from the flange's sealing face (x = 0)
SLOT = False      # no cross slot: the V carries the reducer's 3 in end and the tube continuously (W2 is welded on
                  # top as the part rolls; the back-purge looks after the root)
SLOT_W, SLOT_HALF_Y, SLOT_Z = 20.0, 40.0, -40.0
HOLES = [(x, y) for x in (30.0, L - 20.0) for y in (46.0, -46.0)]
TAP_DRILL, DRILL_Z, TAP_Z = 5.0, -16.0, -12.0
R_TUBE = P.B["body_od"] / 2
R_FLANGE = P.JOINT.flange_od / 2
SHIM = R_TUBE - R_FLANGE          # normal shim thickness on each flank


def axis_height():
    return -V_HALF + R_TUBE * math.sqrt(2)


def fixture_solid():
    import cadquery as cq
    blk = cq.Workplane("XY").box(L, W, H, centered=(False, True, False)).translate((0, 0, -H))
    v = (cq.Workplane("YZ").polyline([(-V_HALF - 5, 5), (V_HALF + 5, 5), (0, -V_HALF)]).close()
         .extrude(L + 20).translate((-10, 0, 0)))
    blk = blk.cut(v)
    blk = blk.cut(cq.Workplane("XY").box(L + 20, APEX_W, 10, centered=(False, True, False))
                  .translate((-10, 0, APEX_Z)))
    if SLOT:
        slot = (cq.Workplane("XY").box(SLOT_W, 2 * SLOT_HALF_Y, 50, centered=(True, True, False))
                .edges("|Z").fillet(TOOLS[2]["d"] / 2 - 0.01))          # the 12 mm end mill leaves r = 6 corners
        blk = blk.cut(slot.translate((SEAM_X, 0, SLOT_Z)))
    for x, y in HOLES:
        blk = blk.cut(cq.Workplane("XY").circle(TAP_DRILL / 2).extrude(-DRILL_Z + 1).translate((x, y, DRILL_Z)))
    return blk.val()


# ----------------------------------------------------------------------------------------------- tools
TOOLS = {
    1: dict(name="50 mm face mill, 3 inserts (APKT 1604)", shape="cylindrical", d=50.0, length=40, S=3800, F=1100),
    2: dict(name="12 mm 3-flute carbide end mill for Al, 36 mm flute", shape="cylindrical", d=12.0, length=45,
            S=8000, F=1400),
    3: dict(name="12.7 mm (1/2 in) 90 deg carbide chamfer mill, 4 flutes", shape="conical", d=12.7, length=6.35,
            angle=90, S=6000, F=600),
    4: dict(name="6 mm 2-flute carbide end mill, 19 mm flute", shape="cylindrical", d=6.0, length=25, S=10000, F=600),
    5: dict(name="10 mm 90 deg spot drill", shape="conical", d=10.0, length=5.0, angle=90, S=3000, F=200),
    6: dict(name="5.0 mm carbide jobber drill (M6 tap drill)", shape="cylindrical", d=5.0, length=40, S=4000, F=300),
    7: dict(name="M6 x 1.0 spiral-point tap (simulated at its 5.0 minor dia)", shape="cylindrical", d=5.0, length=30,
            S=500, F=500),
}


class Prog:
    def __init__(self, name, setup, comment):
        self.name, self.setup = name, setup
        self.lines = ["%", f"O{1000 + setup} ({comment})", "G21 G17 G40 G49 G80 G90 G94", "G54"]
        self.moves = []
        self.pos = np.array([0.0, 0.0, 50.0])
        self.tool = None
        self.safe = 10.0

    def use(self, t):
        tl = TOOLS[t]
        self.tool = t
        # G-code comments do not nest: a "(" inside a comment ends it early and the rest is read as words, which
        # is how the first CAMotics check found the chamfer passes being cut by the previous tool (T2)
        name = tl["name"].replace("(", "[").replace(")", "]")
        self.lines += ["G0 Z50.", f"T{t} M06 ({name})", f"S{tl['S']} M03", f"G43 H{t:02d} Z50. M08"]
        self.pos = np.array([self.pos[0], self.pos[1], 50.0])

    def g0(self, x=None, y=None, z=None):
        p = self.pos.copy()
        for i, v in enumerate((x, y, z)):
            if v is not None:
                p[i] = v
        self.lines.append("G0 " + " ".join(f"{a}{v:.3f}" for a, v, o in zip("XYZ", p, self.pos) if abs(v - o) > 1e-9))
        self.moves.append(dict(p0=self.pos.tolist(), p1=p.tolist(), rapid=True, tool=self.tool))
        self.pos = p

    def g1(self, x=None, y=None, z=None, f=None):
        p = self.pos.copy()
        for i, v in enumerate((x, y, z)):
            if v is not None:
                p[i] = v
        if np.allclose(p, self.pos):
            return
        f = f or TOOLS[self.tool]["F"]
        self.lines.append("G1 " + " ".join(f"{a}{v:.3f}" for a, v, o in zip("XYZ", p, self.pos) if abs(v - o) > 1e-9)
                          + f" F{f:.0f}")
        self.moves.append(dict(p0=self.pos.tolist(), p1=p.tolist(), rapid=False, tool=self.tool, feed=f))
        self.pos = p

    def end(self):
        self.lines += ["G0 Z50. M09", "M05", "G28 G91 Z0.", "G90", "M30", "%"]

    def text(self, sim=False):
        out = []
        for ln in self.lines:
            if sim:
                if ln in ("%",) or ln.startswith("O") or ln.startswith("G28") or ln == "G91":
                    continue
                ln = ln.replace(" M08", "").replace(" M09", "")
                if ln.startswith("G43"):
                    ln = ln.split(" ", 2)[2]
            out.append(ln)
        if sim:
            out.insert(2, f"G92 Z{SHIFT:.0f}")      # the simulator starts the tool at 0,0,0: call that Z1000
        return "\n".join(out) + "\n"


def face(pr, z_levels, y_rows, x0=-30.0, x1=L + 30.0):
    for z in z_levels:
        for k, y in enumerate(y_rows):
            xa, xb = (x0, x1) if k % 2 == 0 else (x1, x0)
            pr.g0(xa, y)
            pr.g0(z=z + 2)
            pr.g1(z=z, f=600)
            pr.g1(x=xb)
            pr.g0(z=z + 2 if k < len(y_rows) - 1 else 10)


def op1():
    pr = Prog("fixture_op1", 1, "B weld fixture, setup 1: bottom up, face 0.5")
    pr.use(1)
    # stock top (the bar's bottom side) at z = 0 before facing; face to z = -0.5
    pr.g0(-30, -35)
    face(pr, [-0.5], [-35.0, 0.0, 35.0])
    pr.end()
    return pr


def op2():
    pr = Prog("fixture_op2", 2, "B weld fixture, setup 2: top up, face to 60.0, V, relief, slot, M6 holes")
    # work zero: top of the finished part (z = 0), x = 0 at the flange end, y = 0 on the V's centreline.
    # The faced stock (63.0 tall) stands 3.0 above work zero.
    pr.use(1)
    pr.g0(-30, -35)
    face(pr, [1.0, 0.0], [-35.0, 0.0, 35.0])
    # --- rough the V: z-levels, 12 mm EM, 0.3 mm left normal to the flank (0.42 in y)
    pr.use(2)
    r = TOOLS[2]["d"] / 2
    allow = 0.3 * math.sqrt(2)
    z = -2.0
    first = True
    while True:
        w = V_HALF + z - allow - r          # largest |y| of the tool centre at this level
        if w < 0:
            break
        ys = list(np.arange(-w, w + 1e-9, r)) if w > 0 else [0.0]
        if ys[-1] < w - 1e-6:
            ys.append(w)
        for k, y in enumerate(ys):
            xa, xb = (-r - 2, L + r + 2) if k % 2 == 0 else (L + r + 2, -r - 2)
            if first or k == 0:
                pr.g0(z=10)
                pr.g0(xa, y)
                pr.g0(z=z + 2.5)
                pr.g1(z=z, f=600)
                first = False
            else:
                pr.g1(xa, y)          # step over beyond the part end, in air
            pr.g1(x=xb)
        pr.g0(z=10)
        first = True
        z -= 2.0
    # --- finish the flanks with the 90 deg chamfer mill: the tip runs on the flank line extended
    pr.use(3)
    rc = TOOLS[3]["d"] / 2
    for side in (1, -1):
        y_top = V_HALF - rc                    # tip y where the cone's top edge meets the top face
        tips = list(np.arange(y_top, 0.0, -3.5)) + [0.0]
        for k, yt in enumerate(tips):
            zt = yt - V_HALF
            xa, xb = (-rc - 2, L + rc + 2) if k % 2 == 0 else (L + rc + 2, -rc - 2)
            pr.g0(z=10)
            pr.g0(xa, side * yt)
            pr.g0(z=zt + 2)
            pr.g1(z=zt, f=400)
            pr.g1(x=xb)
        pr.g0(z=10)
    # --- apex relief: 6 mm EM down the centreline to z = -38 in 1 mm steps
    pr.use(4)
    r4 = TOOLS[4]["d"] / 2
    zs = list(np.arange(-34.0, APEX_Z - 1e-9, -1.0))
    if zs[-1] > APEX_Z + 1e-9:
        zs.append(APEX_Z)
    for k, z in enumerate(zs):
        xa, xb = (-r4 - 2, L + r4 + 2) if k % 2 == 0 else (L + r4 + 2, -r4 - 2)
        pr.g0(z=10) if k == 0 else None
        pr.g0(xa, 0.0) if k == 0 else None
        pr.g0(z=-31.0) if k == 0 else None
        pr.g1(x=xa, y=0.0, z=z, f=300)
        pr.g1(x=xb)
    pr.g0(z=10)
    # --- seam slot (only if SLOT): 12 mm EM, two x positions, zig-zag in y, 2 mm levels to z = -40
    if SLOT:
        _slot(pr)
    _holes(pr)
    pr.end()
    return pr


def _slot(pr):
    r = TOOLS[2]["d"] / 2
    pr.use(2)
    xs = [SEAM_X - SLOT_W / 2 + r, SEAM_X + SLOT_W / 2 - r]
    ymax = SLOT_HALF_Y - r
    z = -2.0
    while z >= SLOT_Z - 1e-9:
        for k, x in enumerate(xs):
            pr.g0(z=10) if k == 0 else None
            ya, yb = (-ymax, ymax) if k % 2 == 0 else (ymax, -ymax)
            if k == 0:
                pr.g0(x, ya)
                pr.g0(z=z + 2.5)
                pr.g1(z=z, f=400)
            else:
                pr.g1(x, ya)
            pr.g1(y=yb)
        pr.g1(x=xs[0])                 # along the -y wall: the y passes alone leave a scallop between the two x's
        z = round(z - 2.0, 3) if z - 2.0 >= SLOT_Z - 1e-9 or abs(z - SLOT_Z) < 1e-9 else SLOT_Z
        if abs(z - SLOT_Z) < 1e-9 and pr.pos[2] <= SLOT_Z + 1e-9:
            break
    pr.g0(z=10)


def _holes(pr):
    # --- holes: spot, peck drill, tap (written out; CAMotics does not run canned cycles)
    pr.use(5)
    for x, y in HOLES:
        pr.g0(x, y)
        pr.g0(z=2)
        pr.g1(z=-3.0, f=200)
        pr.g0(z=2)
    pr.g0(z=10)
    pr.use(6)
    for x, y in HOLES:
        pr.g0(x, y)
        pr.g0(z=2)
        z = 0.0
        while z > DRILL_Z + 1e-9:
            z = max(z - 4.0, DRILL_Z)
            pr.g1(z=z, f=300)
            pr.g0(z=2)
            if z > DRILL_Z:
                pr.g0(z=z + 0.5)
        pr.g0(z=5)
    pr.use(7)
    for x, y in HOLES:
        pr.g0(x, y)
        pr.g0(z=5)
        pr.g1(z=TAP_Z, f=500)
        pr.g1(z=5, f=500)          # on the machine: G84 rigid tap, or reverse the spindle out (M04)


# ---------------------------------------------------------------------------------------------- CAMotics
def camsim(pr, stock_lo, stock_hi, res=0.5):
    d = WORK / pr.name
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{pr.name}.ngc").write_text(pr.text(sim=True))
    tools = {}
    for t, s in TOOLS.items():
        rec = dict(units="metric", shape=s["shape"], length=s["length"], diameter=s["d"], description=s["name"])
        if s["shape"] == "conical":
            rec["angle"] = s["angle"]
        tools[str(t)] = rec
    proj = {"units": "metric", "resolution-mode": "manual", "resolution": res, "tools": tools,
            "workpiece": {"automatic": False, "margin": 0,
                          "bounds": {"min": [stock_lo[0], stock_lo[1], stock_lo[2] - SHIFT],
                                     "max": [stock_hi[0], stock_hi[1], stock_hi[2] - SHIFT]}},
            "files": [f"{pr.name}.ngc"]}
    (d / f"{pr.name}.camotics").write_text(json.dumps(proj, indent=1))
    t0 = time.time()
    p = subprocess.run(["docker", "run", "--rm", "--memory=6g", "-v", f"{d}:/work", IMAGE, "sh", "-c",
                        f"camsim -v --binary --threads 2 {pr.name}.camotics {pr.name}.stl; echo exit=$?"],
                       capture_output=True, text=True)
    log = [ln for ln in (p.stdout + p.stderr).splitlines() if not ln.startswith(("Progress", "/work"))]
    (d / f"{pr.name}.log").write_text("\n".join(log))
    import trimesh
    m = trimesh.load(d / f"{pr.name}.stl")
    m.apply_translation([0, 0, SHIFT])
    return m, dict(seconds=round(time.time() - t0, 1), log_tail=log[-3:],
                   not_implemented=sorted({ln.split("Not implemented:")[-1].strip() for ln in log if "Not implemented" in ln}))


def sections_compare(sim, cad_mesh):
    """Gouge and leftover in sections of the simulated part against the CAD."""
    from shapely.geometry import MultiPolygon, Polygon
    from shapely.ops import unary_union

    def polys(mesh, origin, normal, to2d):
        s = mesh.section(plane_origin=origin, plane_normal=normal)
        if s is None:
            return Polygon()
        out = []
        for ent in s.discrete:
            pts = [to2d(p) for p in ent]
            if len(pts) >= 3:
                pg = Polygon(pts).buffer(0)
                if pg.area > 0.05:
                    out.append(pg)
        # even-odd: holes are inner loops
        res = Polygon()
        for pg in sorted(out, key=lambda q: -q.area):
            res = res.symmetric_difference(pg)
        return res

    out = {}
    planes = [("x=60", [60, 0, 0], [1, 0, 0], lambda p: (p[1], p[2])),
              ("x=%.0f" % (L - 10), [L - 10, 0, 0], [1, 0, 0], lambda p: (p[1], p[2])),
              ("x=%.0f (holes)" % HOLES[0][0], [HOLES[0][0], 0, 0], [1, 0, 0], lambda p: (p[1], p[2])),
              ("x=%.0f (holes)" % HOLES[2][0], [HOLES[2][0], 0, 0], [1, 0, 0], lambda p: (p[1], p[2])),
              ("z=-5", [0, 0, -5], [0, 0, 1], lambda p: (p[0], p[1]))]
    figs = []
    for name, o, n, f in planes:
        a, b = polys(sim, o, n, f), polys(cad_mesh, o, n, f)
        gouge = b.difference(a)
        left = a.difference(b)

        def depth(region, ref):
            if region.is_empty:
                return 0.0
            mx = 0.0
            geoms = getattr(region, "geoms", [region])
            for g in geoms:
                for x, y in g.exterior.coords:
                    from shapely.geometry import Point
                    mx = max(mx, Point(x, y).distance(ref.boundary))
            return mx
        out[name] = dict(sim_area=round(a.area, 1), cad_area=round(b.area, 1), gouge_mm2=round(gouge.area, 2),
                         leftover_mm2=round(left.area, 2), gouge_depth=round(depth(gouge, b), 3),
                         leftover_depth=round(depth(left, b), 3))
        figs.append((name, a, b))
    return out, figs


def rapids_through_stock(moves, cad_mesh, stock_top):
    """Rapid moves that pass below the finished surface where material is still present (coarse check: any
    G0 below the stock top that enters the CAD solid's interior)."""
    import trimesh
    bad = 0
    for mv in moves:
        if not mv["rapid"]:
            continue
        p0, p1 = np.array(mv["p0"]), np.array(mv["p1"])
        if max(p0[2], p1[2]) > stock_top + 0.5 and min(p0[2], p1[2]) > stock_top + 0.5:
            continue
        pts = p0 + np.linspace(0, 1, 40)[:, None] * (p1 - p0)
        inside = cad_mesh.contains(pts)
        if inside.any():
            bad += 1
    return bad


def main():
    import cadquery as cq
    import trimesh
    solid = fixture_solid()
    cq.exporters.export(cq.Workplane().add(solid), str(OUT / "fixture_b.step"))
    cq.exporters.export(cq.Workplane().add(solid), str(WORK / "fixture_b.stl"), tolerance=0.05, angularTolerance=0.1)
    cad_mesh = trimesh.load(WORK / "fixture_b.stl")
    p1, p2 = op1(), op2()
    for pr in (p1, p2):
        (GC / f"{pr.name}.nc").write_text(pr.text())
    res = {"part": "B weld-alignment fixture (6061-T6)", "stock": "2-1/2 x 4-1/2 in 6061-T6 flat bar, sawn to 120",
           "axis_height_above_top_mm": round(axis_height(), 3), "shim_mm": round(SHIM, 3),
           "cad_volume_cm3": round(solid.Volume() / 1e3, 1), "mass_kg": round(solid.Volume() * 2.70e-6, 2)}
    # setup 2 on the bottom-faced stock (63.0 tall, its top 3.0 above work zero)
    sim2, info2 = camsim(p2, [0, -W / 2, -H], [L, W / 2, 3.0])
    sim2.export(OUT / "fixture_op2_sim.stl") if False else None
    cmp2, figs = sections_compare(sim2, cad_mesh)
    res["setup2"] = dict(camotics=info2, sections=cmp2, sim_volume_cm3=round(abs(sim2.volume) / 1e3, 1),
                         rapids_into_part=rapids_through_stock(p2.moves, cad_mesh, 3.0))
    # cycle time (feed moves at their F; rapids at 10 m/min, plus 8 s per tool change)
    def ctime(pr):
        t = 0.0
        for mv in pr.moves:
            dist = float(np.linalg.norm(np.array(mv["p1"]) - np.array(mv["p0"])))
            t += dist / (mv["feed"] if not mv["rapid"] else 10000.0) * 60
        return t + 8 * sum(1 for ln in pr.lines if "M06" in ln)
    res["cycle_time_min"] = {p1.name: round(ctime(p1) / 60, 1), p2.name: round(ctime(p2) / 60, 1)}
    res["tools"] = {str(k): v["name"] for k, v in TOOLS.items()}
    (OUT / "mill_sim.json").write_text(json.dumps(res, indent=1) + "\n")
    plot(figs, res, sim2)
    print(json.dumps({k: v for k, v in res.items() if k != "tools"}, indent=1))


def plot(figs, res, sim):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(figs), figsize=(4.2 * len(figs), 4.2))
    for ax, (name, a, b) in zip(axes, figs):
        for geom, col, lab in ((b, "#1f77b4", "CAD"), (a, "#ff7f0e", "CAMotics cut")):
            for g in getattr(geom, "geoms", [geom]):
                if g.is_empty:
                    continue
                x, y = g.exterior.xy
                ax.plot(x, y, color=col, lw=1.2 if lab == "CAD" else 0.8, ls="-" if lab == "CAD" else "--", label=lab)
                for hole in g.interiors:
                    x, y = hole.xy
                    ax.plot(x, y, color=col, lw=0.8, ls="-" if lab == "CAD" else "--")
        s = res["setup2"]["sections"][name]
        ax.set_title(f"{name}\ngouge {s['gouge_mm2']} mm2 (max {s['gouge_depth']} mm), "
                     f"left {s['leftover_mm2']} mm2 (max {s['leftover_depth']} mm)", fontsize=7)
        ax.set_aspect("equal")
        ax.tick_params(labelsize=6)
        h, lab = ax.get_legend_handles_labels()
        uniq = dict(zip(lab, h))
        ax.legend(uniq.values(), uniq.keys(), fontsize=6, loc="lower right")
    fig.suptitle("B weld fixture: CAMotics 1.2.0 cut of setup 2 vs CAD, in sections", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "mill_fixture_sections.png", dpi=130)
    plt.close(fig)
    try:
        import pyvista as pv
        pv.global_theme.allow_empty_mesh = True
        pl = pv.Plotter(off_screen=True, window_size=(1400, 800))
        pl.set_background("white")
        m = pv.wrap(sim)
        pl.add_mesh(m, color=(0.78, 0.80, 0.84), smooth_shading=False, specular=0.3)
        pl.camera_position = [(-180, -260, 220), (120, 0, -30), (0, 0, 1)]
        pl.add_text("B weld fixture as cut in CAMotics (setup 2)", font_size=12, color="black")
        pl.screenshot(str(OUT / "mill_fixture_camotics.png"))
        pl.close()
    except Exception as ex:  # noqa: BLE001
        print("render skipped:", ex)


if __name__ == "__main__":
    main()
