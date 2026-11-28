"""CAM for the fast-track pieces in FreeCAD 1.0's CAM workbench, headless (#260, PR 294 round 2).

Follows PR 266's desktop-lpbf/analysis/machining/freecad_cam.py: one FreeCAD Job per setup, a box stock, tool
controllers from a small common library (tools.py), FreeCAD's own MillFace, Adaptive, PocketShape, Profile, Helix and
Drilling operations, the `linuxcnc` post, FreeCAD's CycleTime and a recount of the posted G-code (freecad_cam.py's
gcode_times: feeds as programmed, rapids at 25.4 m/min, G81/G83 expanded).

Input: /tmp/ft-fab/pieces.json and /tmp/ft-fab/pieces/<pid>.brep from parts.py. Each setup turns the piece so the
setup's "up" direction is +Z (rotation rows as freecad_cam.py), then programs, in order: face the top (MillFace),
the outside (Adaptive outside the top face's outline, down to the setup's depth), and every recorded feature whose
entry direction faces the spindle: pockets and grooves (Pocket on the floor face found by a probe point; PocketShape posts no path on these faces in 1.0.2), large
pockets (Adaptive), through openings (Profile round the inside of the opening in the entry face), bores (Helix),
holes (Drilling with G83 pecks, one op per drill and depth), counterbores (Pocket on the floor annulus) and
countersinks (Drilling with the 90 deg spot drill). A slot through a tube wall, which has no flat entry face, is a
Custom op with hand-written G-code.

Run:  /tmp/tools/capmem 3 /tmp/setup/squashfs-root/usr/bin/freecadcmd -c \
        "import runpy; runpy.run_path('desktop-lpbf/fast-track/fab/cam.py', run_name='__main__')"
Writes desktop-lpbf/fast-track/fab/gcode/<setup>.ngc and fab/out/cam.json. $FT_CAM_ONLY=MK-03,MK-07 limits the pieces.

Not programmed (timed in hours.py as estimates): tapping, reaming, the boring-head finish of the 40 H7 bore, the lathe
work, deburring. Tool changes are counted, not timed, by the recount.
"""
import json
import math
import os
import re
import sys

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.path.join(os.getcwd(), "desktop-lpbf", "fast-track", "fab")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "analysis", "machining")))
import tools as T  # noqa: E402
import freecad_cam as FC  # noqa: E402  (plain functions: gcode_times, clean_label)

SCR = "/tmp/ft-fab"
GDIR = os.path.join(HERE, "gcode")
OUT_JSON = os.path.join(HERE, "out", "cam.json")
ROT = {"+Z": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "-Z": ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
       "+X": ((0, 1, 0), (0, 0, 1), (1, 0, 0)), "-X": ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
       "+Y": ((1, 0, 0), (0, 0, -1), (0, 1, 0)), "-Y": ((-1, 0, 0), (0, 0, -1), (0, -1, 0))}
UP_OF = {"-z": "+Z", "+z": "-Z", "-x": "+X", "+x": "-X", "-y": "+Y", "+y": "-Y"}
AXIS_I = {"x": 0, "y": 1, "z": 2}
STEP = {1: 3.0, 2: 6.0, 3: 3.0, 4: 1.0, 5: 0.5, 6: 10.0}       # step-downs (pockets, profiles), mm
ADAPT_STEP = {2: 12.0, 3: 6.0, 4: 2.0, 6: 19.0}                  # Adaptive step-downs (small radial stepover)


def rot(up, p):
    r = ROT[up]
    return tuple(sum(r[i][k] * p[k] for k in range(3)) for i in range(3))


def setup_box(up, b):
    """part-frame box -> setup-frame (x0, y0, z0, L, W, H)"""
    x0, x1, y0, y1, z0, z1 = b
    pts = [rot(up, (x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    return lo[0], lo[1], lo[2], hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]


def custom_slot_gcode(cx, cy, z_top, w, h, depth, tool_d, feed, plunge):
    """zig-zag pocket for a w x h (x by y) rectangular window through a wall of `depth`, tool centre inside by D/2"""
    lines = []
    xa, xb = cx - w / 2 + tool_d / 2, cx + w / 2 - tool_d / 2
    ya, yb = cy - h / 2 + tool_d / 2, cy + h / 2 - tool_d / 2
    z = z_top
    if xb < xa:                                   # slot narrower than two radii: one pass down the middle
        xa = xb = cx
    lines.append("G0 X%.3f Y%.3f" % (xa, ya))
    lines.append("G0 Z%.3f" % (z_top + 2.0))
    lines.append("G1 Z%.3f F%.1f" % (z_top + 0.2, plunge))
    step = 0.3
    while z > z_top - depth + 1e-6:
        z = max(z - step, z_top - depth)
        # ramp down along y (review-r3: no straight plunge), then back to the corner
        lines.append("G1 X%.3f Y%.3f Z%.3f F%.1f" % (xa, yb, z, plunge))
        lines.append("G1 X%.3f Y%.3f F%.1f" % (xa, ya, feed))
        n = max(1, int(math.ceil((xb - xa) / (0.6 * tool_d))))
        for i in range(n + 1):
            x = xa + (xb - xa) * i / n
            lines.append("G1 X%.3f Y%.3f F%.1f" % (x, ya if i % 2 == 0 else yb, feed))
            lines.append("G1 X%.3f Y%.3f F%.1f" % (x, yb if i % 2 == 0 else ya, feed))
        lines.append("G1 X%.3f Y%.3f F%.1f" % (xa, ya, feed))
    lines.append("G0 Z%.3f" % (z_top + 5.0))
    return lines


def g0_links_to_g1(text, safe, feed=5000.0):
    """review-r3: FreeCAD's Adaptive links sideways with G0 below the operation's safe height, and a Haas G00 is a
    dogleg, not a straight line. Inside each Adaptive operation, a G0 with no Z move made below its safe height becomes
    a G1 at `feed`, and the next cutting move gets its own feed back. Returns (text, number of links changed)."""
    out, cur_op, z, last_f, restore, n = [], None, None, None, False, 0
    for ln in text.splitlines():
        m = re.match(r"\(begin operation: (.*)\)", ln)
        if m:
            cur_op = m.group(1)
        elif ln.startswith("(finish operation"):
            cur_op = None
        words = dict(re.findall(r"([XYZF])([-+]?\d*\.?\d+)", ln))
        code = ln.split()[0] if ln.split() else ""
        if code == "G0" and "Z" not in words and ("X" in words or "Y" in words) and cur_op in safe and z is not None \
                and z < safe[cur_op] - 1e-6:
            ln = ln.rstrip().replace("G0", "G1", 1) + " F%.3f" % feed
            restore = True
            n += 1
        elif code in ("G1", "G2", "G3"):
            if "F" in words:
                last_f = float(words["F"])
                restore = False
            elif restore and last_f is not None:
                ln = ln.rstrip() + " F%.3f" % last_f
                restore = False
        if "Z" in words and code in ("G0", "G1", "G2", "G3"):
            z = float(words["Z"])
        out.append(ln)
    return "\n".join(out) + "\n", n


def per_second(lines):
    """FreeCAD's Path keeps feeds in mm/s and the post writes mm/min (x 60): hand-written Custom G-code in mm/min is
    converted on the way in"""
    return [re.sub(r"F([-+]?\d*\.?\d+)", lambda m: "F%.4f" % (float(m.group(1)) / 60.0), ln) for ln in lines]


def run():
    import FreeCAD
    import Part
    import Path
    import Path.Main.Job as PathJob
    import Path.Main.Stock as PathStock
    import Path.Op.Adaptive
    import Path.Op.Custom
    import Path.Op.Drilling
    import Path.Op.Helix
    import Path.Op.MillFace
    import Path.Op.Pocket
    import Path.Op.Profile
    import Path.Tool.Bit as PathToolBit
    import Path.Tool.Controller as PathToolController
    from Path.Post.scripts import linuxcnc_post

    os.makedirs(GDIR, exist_ok=True)
    spec = json.load(open(os.path.join(SCR, "pieces.json")))
    only = [p for p in os.environ.get("FT_CAM_ONLY", "").split(",") if p]
    doc = FreeCAD.newDocument("ft_cam")
    results = []

    for pc in spec["pieces"]:
        if not pc["setups"] or (only and pc["pid"] not in only):
            continue
        src = Part.Shape()
        src.read(os.path.join(SCR, "pieces", pc["pid"] + ".brep"))
        start_b = None
        if os.path.exists(os.path.join(SCR, "pieces", pc["pid"] + "_start.brep")):
            start_b = Part.Shape()
            start_b.read(os.path.join(SCR, "pieces", pc["pid"] + "_start.brep"))
        bb0 = (start_b or src).BoundBox
        stock_part = (bb0.XMin, bb0.XMax, bb0.YMin, bb0.YMax, bb0.ZMin, bb0.ZMax)
        for su in pc["setups"]:
            up = su["up"]
            R = ROT[up]
            shp = src.copy()
            shp.transformShape(FreeCAD.Matrix(R[0][0], R[0][1], R[0][2], 0, R[1][0], R[1][1], R[1][2], 0,
                                              R[2][0], R[2][1], R[2][2], 0, 0, 0, 0, 1))
            model = doc.addObject("Part::Feature", su["name"].replace("-", "_") + "_model")
            model.Shape = shp
            doc.recompute()
            job = PathJob.Create("Job_" + su["name"].replace("-", "_"), [model])
            job.PostProcessor = "linuxcnc"
            job.PostProcessorArgs = "--no-show-editor --precision 3"
            for tc in list(job.Tools.Group):
                job.Tools.removeObject(tc)
            sx0, sy0, sz0, sL, sW, sH = setup_box(up, stock_part)
            old = job.Stock
            job.Stock = PathStock.CreateBox(job, FreeCAD.Vector(sL, sW, sH),
                                            FreeCAD.Placement(FreeCAD.Vector(sx0, sy0, sz0), FreeCAD.Rotation()))
            doc.removeObject(old.Name)
            base = job.Model.Group[0]
            doc.recompute()
            S = base.Shape
            sbb = S.BoundBox
            stock_top = sz0 + sH
            tcs = {}

            def tc_for(t):
                if t in tcs:
                    return tcs[t]
                v = T.TOOLS[t]
                shape_file = {"endmill": "endmill.fcstd", "drill": "drill.fcstd", "chamfer": "chamfer.fcstd"}[v["shape"]]
                bit = PathToolBit.Factory.Create("T%d" % t, shape_file)
                bit.Diameter = v["d"]
                if hasattr(bit, "Length"):
                    bit.Length = v["length"]
                if v["shape"] == "endmill" and hasattr(bit, "CuttingEdgeHeight"):
                    bit.CuttingEdgeHeight = v["edge"]
                if v["shape"] == "chamfer" and hasattr(bit, "CuttingEdgeAngle"):
                    bit.CuttingEdgeAngle = v["angle"]
                tc = PathToolController.Create("TC%d_%s" % (t, job.Name), bit, t)
                f = T.feed_mm_min(t)
                tc.HorizFeed = "%f mm/min" % f
                tc.VertFeed = "%f mm/min" % (f if v["shape"] in ("drill", "chamfer") else 0.5 * f)
                tc.HorizRapid = "%f mm/min" % T.RAPID_MM_MIN
                tc.VertRapid = "%f mm/min" % T.RAPID_MM_MIN
                tc.SpindleSpeed = v["rpm"]
                tc.SpindleDir = "Forward"
                job.Proxy.addToolController(tc)
                tcs[t] = tc
                return tc

            def up_faces():
                out = []
                for i, f in enumerate(S.Faces):
                    if type(f.Surface).__name__ != "Plane":
                        continue
                    n = f.normalAt(0, 0)
                    if n.z > 0.999:
                        out.append(("Face%d" % (i + 1), f))
                return out

            def top_face():
                c = [(n, f) for n, f in up_faces() if abs(f.BoundBox.ZMax - sbb.ZMax) < 0.01]
                return max(c, key=lambda nf: nf[1].Area)

            def outline_face():
                """the flat face (up or down) whose outer wire encloses the most: the piece's silhouette when the top
                face is notched (a slot open to the side) or smaller than a lower flange"""
                best = None
                for i, f in enumerate(S.Faces):
                    if type(f.Surface).__name__ != "Plane" or abs(abs(f.normalAt(0, 0).z) - 1) > 1e-3:
                        continue
                    try:
                        a_ = Part.Face(f.OuterWire).Area
                    except Exception:
                        continue
                    if best is None or a_ > best[2] + 1e-6:
                        best = ("Face%d" % (i + 1), f, a_)
                return best[0], best[1]

            def face_at(p, tol=0.02):
                v = Part.Vertex(FreeCAD.Vector(*p))
                best = None
                for n, f in up_faces():
                    if abs(f.BoundBox.ZMax - p[2]) > 0.05:
                        continue
                    d = f.distToShape(v)[0]
                    if d < tol and (best is None or d < best[2]):
                        best = (n, f, d)
                if best is None:
                    raise ValueError("no up-facing face at %s; up faces at z %s" % (
                        p, sorted({round(f.BoundBox.ZMax, 2) for n, f in up_faces()})))
                return best[0], best[1]

            def cyl_faces(x, y, r, tol=0.02):
                out = []
                for i, f in enumerate(S.Faces):
                    s_ = f.Surface
                    if type(s_).__name__ != "Cylinder" or abs(abs(s_.Axis.z) - 1) > 1e-6:
                        continue
                    if abs(s_.Radius - r) > 1e-3 or math.hypot(s_.Center.x - x, s_.Center.y - y) > tol:
                        continue
                    out.append(("Face%d" % (i + 1), f))
                return out

            ops = []

            def set_depths(op, start=None, final=None, step=None):
                for prop, val in (("StartDepth", start), ("FinalDepth", final), ("StepDown", step)):
                    if val is not None and hasattr(op, prop):
                        op.setExpression(prop, None)
                        setattr(op, prop, val)

            def finish(op, label, t, meta):
                op.Label = FC.clean_label(label)
                op.ToolController = tc_for(t)
                if op.Name.startswith("Adaptive"):
                    meta["safe_z"] = "adaptive"
                if hasattr(op, "CoolantMode"):
                    op.CoolantMode = "Flood"
                ops.append((op, dict(label=op.Label, tool=t, tool_name=T.TOOLS[t]["name"],
                                     feed_mm_min=round(T.feed_mm_min(t), 1), **meta)))

            errors = []

            def attempt(label, fn):
                try:
                    fn()
                except Exception as e:  # keep going, record it
                    import traceback
                    tb = traceback.extract_tb(e.__traceback__)[-1]
                    errors.append(dict(label=label, error="%s: %s (%s:%d)" % (type(e).__name__, e,
                                                                              os.path.basename(tb.filename), tb.lineno)))

            top_z = sbb.ZMax
            # 1. face
            if su.get("face"):
                def _face():
                    t = su["face"][0]
                    if stock_top - top_z < 0.02:
                        return
                    tc_for(t)
                    n, f = top_face()
                    op = Path.Op.MillFace.Create("Face", parentJob=job)
                    op.Base = [(base, [n])]
                    op.BoundaryShape = "Boundbox"
                    op.StepOver = 70
                    op.ClearEdges = True
                    op.ZigZagAngle = 0.0
                    set_depths(op, stock_top, top_z, max(0.5, min(2.0, stock_top - top_z)))
                    finish(op, "Face top %.2f to z %.2f" % (stock_top, top_z), t, dict(kind="face"))
                attempt("face", _face)
            # 2. outside
            if su.get("outline"):
                def _outline():
                    t, z_to = su["outline"]
                    tc_for(t)
                    n, f = outline_face()
                    op = Path.Op.Adaptive.Create("Adaptive", parentJob=job)
                    op.Base = [(base, [n])]
                    op.Side = "Outside"
                    op.OperationType = "Clearing"
                    op.UseOutline = True
                    op.StepOver = 12
                    op.Tolerance = 0.1
                    set_depths(op, top_z, z_to, ADAPT_STEP.get(t, 6.0))
                    finish(op, "Outside, adaptive, z %.2f to %.2f" % (top_z, z_to), t, dict(kind="outline"))
                attempt("outline", _outline)
            # 3. features entering from above in this setup
            feats = [f for f in pc["features"] if UP_OF[f["axis"]] == up]
            order = {"boss": -0.5, "adaptive": 0, "pocket": 1, "face_region": 1, "custom_gcode": 1, "groove": 2, "opening": 3, "custom_slot": 3, "bore": 4, "drill": 5,
                     "cbore": 6, "csk": 7}
            feats.sort(key=lambda f: (order[f["kind"]] + (4.5 if f.get("late") else 0), f.get("tool", 0), -f.get("d", 0)))
            for f in feats:
                k = f["kind"]
                lab = f.get("name") or ("hole %s" % f.get("hid"))

                def _do(f=f, k=k, lab=lab):
                    t = f["tool"]
                    if k in ("pocket", "groove", "adaptive", "face_region"):
                        p = rot(up, f["probe"])
                        n, face = face_at(p)
                        tc_for(t)
                        if k == "face_region":
                            # an open pocket (FreeCAD 1.0.2's Pocket and Adaptive post nothing for these): MillFace
                            # over the floor face's own region
                            op = Path.Op.MillFace.Create("Face", parentJob=job)
                            op.Base = [(base, [n])]
                            op.BoundaryShape = "Face Region"
                            op.StepOver = 40
                            op.ClearEdges = False
                            set_depths(op, top_z, face.BoundBox.ZMax, STEP.get(t, 1.0))
                        elif k == "adaptive":
                            op = Path.Op.Adaptive.Create("Adaptive", parentJob=job)
                            op.Base = [(base, [n])]
                            op.Side = "Inside"
                            op.OperationType = "Clearing"
                            op.StepOver = 15
                            op.Tolerance = 0.1
                            set_depths(op, top_z, face.BoundBox.ZMax, ADAPT_STEP.get(t, 6.0))
                        else:
                            z0 = top_z
                            if f.get("z_top") is not None:
                                q = list(f["probe"])
                                q[AXIS_I[f["axis"][1]]] = f["z_top"]
                                z0 = rot(up, q)[2]
                            if k == "groove":
                                # a groove: profile both wires of its floor with the tool inside the floor (two
                                # passes cover up to 2 tool diameters); a 3D Pocket also clears the disc inside it
                                op = Path.Op.Profile.Create("Profile", parentJob=job)
                                op.Base = [(base, [n])]
                                op.processPerimeter = True
                                op.processHoles = True
                                op.processCircles = True
                                op.Side = "Inside"
                            else:
                                op = Path.Op.Pocket.Create("Pocket", parentJob=job)
                                op.Base = [(base, [n])]
                                op.OffsetPattern = "Offset"
                                op.StepOver = 45
                            set_depths(op, z0, face.BoundBox.ZMax, STEP.get(t, 1.0))
                        finish(op, lab, t, dict(kind=k))
                    elif k == "opening":
                        p = rot(up, f["probe"])
                        n, face = face_at(p)
                        ex = list(f["probe"])
                        ax = f["axis"][1]
                        ex[AXIS_I[ax]] = f["z_exit"]
                        z_exit = rot(up, ex)[2]
                        tc_for(t)
                        op = Path.Op.Profile.Create("Profile", parentJob=job)
                        op.Base = [(base, [n])]
                        op.processHoles = True
                        op.processPerimeter = False
                        op.processCircles = False
                        op.Side = "Outside"
                        set_depths(op, face.BoundBox.ZMax, z_exit - 0.3, STEP.get(t, 1.0))
                        finish(op, lab + ", profile to z %.2f" % (z_exit - 0.3), t, dict(kind=k))
                    elif k == "boss":
                        # material round a boss: Adaptive outside the boss's top face, down to the face round it
                        p = rot(up, f["probe"])
                        n, face = face_at(p)
                        ex = list(f["probe"])
                        ex[AXIS_I[f["axis"][1]]] = f["z_base"]
                        z_base = rot(up, ex)[2]
                        tc_for(t)
                        op = Path.Op.Adaptive.Create("Adaptive", parentJob=job)
                        op.Base = [(base, [n])]
                        op.Side = "Outside"
                        op.OperationType = "Clearing"
                        op.UseOutline = True
                        op.StepOver = 12
                        op.Tolerance = 0.1
                        set_depths(op, top_z, z_base, ADAPT_STEP.get(t, 6.0))
                        finish(op, lab + ", adaptive outside to z %.2f" % z_base, t, dict(kind=k))
                    elif k == "custom_gcode":
                        tc_for(t)
                        op = Path.Op.Custom.Create("Custom", parentJob=job)
                        op.Gcode = per_second(f["gcode"])
                        finish(op, lab, t, dict(kind=k))
                    elif k == "custom_slot":
                        c = rot(up, f["center"])
                        tl = T.TOOLS[t]
                        g = custom_slot_gcode(c[0], c[1], c[2], f["size"][0], f["size"][1], f["depth"], tl["d"],
                                              T.feed_mm_min(t), 0.5 * T.feed_mm_min(t))
                        tc_for(t)
                        op = Path.Op.Custom.Create("Custom", parentJob=job)
                        op.Gcode = per_second(g)
                        finish(op, lab + ", custom zig-zag", t, dict(kind=k))
                    elif k == "bore":
                        x, y, _ = rot(up, (f["xy"][0], f["xy"][1], 0.0))
                        names = [nm for nm, _ in cyl_faces(x, y, f["r"])]
                        if not names:
                            raise ValueError("bore face not found")
                        zs = sorted(rot(up, (f["xy"][0], f["xy"][1], z))[2] for z in (f["z_top"], f["z_bot"]))
                        z_hi, z_lo = zs[1], zs[0]
                        through = z_lo <= sbb.ZMin + 0.01
                        tc_for(t)
                        op = doc.addObject("Path::FeaturePython", "Helix")
                        op.Proxy = Path.Op.Helix.ObjectHelix(op, "Helix", job)
                        op.Base = [(base, names[:1])]
                        d = T.TOOLS[t]["d"]
                        outer = f["r"] - d / 2
                        op.StartRadius = 0.0
                        op.StepOver = 40
                        op.Direction = "CCW"
                        op.StartSide = "Inside"
                        set_depths(op, z_hi + 1.0, z_lo - (0.5 if through else 0.0), 1.0)   # review-r3: start 1 above
                        finish(op, "%s, helix z %.2f to %.2f" % (lab, z_hi, z_lo - (0.5 if through else 0)), t,
                               dict(kind=k))
                    elif k in ("drill", "csk"):
                        d = f["d"] if k == "drill" else None
                        groups = {}
                        for p0 in f["pts"]:
                            ps = rot(up, p0)
                            hd = f["d"] if k == "drill" else None
                            if k == "csk":
                                # the hole under the countersink: its drill diameter is in the matching drill feature
                                hd = next(g["d"] for g in pc["features"] if g["kind"] == "drill" and g["hid"] == f["hid"])
                            names = [nm for nm, fc in cyl_faces(ps[0], ps[1], hd / 2)]
                            if not names:
                                raise ValueError("hole %s at %s not found (d %.2f)" % (f["hid"], ps, hd))
                            if k == "drill":
                                if f["through"]:
                                    zb = min(fc.BoundBox.ZMin for nm, fc in cyl_faces(ps[0], ps[1], hd / 2))
                                    final = zb - 0.3 * d - 0.5
                                else:
                                    final = ps[2] - f["depth"] - 0.3 * d
                            else:
                                final = ps[2] - f["d"] / 2
                            key = (round(ps[2], 3), round(final, 3))
                            groups.setdefault(key, []).append(names[0])
                        for (zs_, zf_), names in sorted(groups.items()):
                            tc_for(t)
                            op = doc.addObject("Path::FeaturePython", "Drill")
                            op.Proxy = Path.Op.Drilling.ObjectDrilling(op, "Drill", job)
                            op.Base = [(base, names)]
                            op.RetractMode = "G98"
                            if k == "drill":
                                op.PeckEnabled = True
                                op.setExpression("PeckDepth", None)     # review-r3: else every G83 pecks 0.75 D
                                op.PeckDepth = max(0.5, T.TOOLS[t]["d"] * (1.0 if f["depth"] < 4 * d or f["through"]
                                                                            else 0.5))
                            set_depths(op, zs_, zf_)
                            op.setExpression("RetractHeight", None)
                            op.RetractHeight = zs_ + 2.0
                            finish(op, "%s %d x %.2f %s, z %.2f to %.2f" % (
                                "Drill" if k == "drill" else "Countersink", len(names),
                                f["d"], f.get("size", ""), zs_, zf_), t, dict(kind=k, holes=len(names)))
                    elif k == "cbore":
                        for p0 in f["pts"]:
                            ps = rot(up, p0)
                            names = [nm for nm, _ in cyl_faces(ps[0], ps[1], f["d"] / 2)]
                            if not names:
                                raise ValueError("c'bore at %s not found" % (ps,))
                            tc_for(t)
                            op = doc.addObject("Path::FeaturePython", "Helix")
                            op.Proxy = Path.Op.Helix.ObjectHelix(op, "Helix", job)
                            op.Base = [(base, names[:1])]
                            op.StartRadius = 0.0
                            op.StepOver = 40
                            op.Direction = "CCW"
                            op.StartSide = "Inside"
                            set_depths(op, ps[2] + 1.0, ps[2] - f["depth"], 0.5)
                            finish(op, "C'bore %.1f x %.1f at %.1f %.1f, helix" % (f["d"], f["depth"], ps[0], ps[1]), t,
                                   dict(kind=k))
                attempt(lab, _do)

            doc.recompute()
            posted, cur, metas = [], None, []
            for op, meta in ops:
                if meta.get("safe_z") == "adaptive":
                    try:
                        meta["safe_z"] = float(op.SafeHeight.Value)
                    except Exception:
                        meta["safe_z"] = stock_top + 1.0
                meta["freecad_cycle_time"] = getattr(op, "CycleTime", None)
                meta["commands"] = len(op.Path.Commands)
                if meta["commands"] == 0:
                    meta["error"] = "operation produced no path"
                    metas.append(meta)
                    continue
                if op.ToolController.ToolNumber != cur:
                    posted.append(op.ToolController)
                    cur = op.ToolController.ToolNumber
                posted.append(op)
                metas.append(meta)
            job.recompute()
            gpath = os.path.join(GDIR, su["name"] + ".ngc")
            text = linuxcnc_post.export(posted, gpath, "--no-show-editor --precision 3") if posted else ""
            if posted and not text:
                text = open(gpath).read()
            safe = {m["label"]: m["safe_z"] for m in metas if m.get("safe_z") is not None}
            text, n_links = g0_links_to_g1(text, safe)
            if posted:
                with open(gpath, "w") as fh:
                    fh.write(text)
            times, ntc = FC.gcode_times(text) if text else ({}, 0)
            tot = dict(feed_mm=0.0, rapid_mm=0.0, feed_s=0.0, rapid_s=0.0)
            for m in metas:
                g = times.get(m["label"])
                if g:
                    m["cut_min"] = round(g["feed_s"] / 60, 2)
                    m["rapid_min"] = round(g["rapid_s"] / 60, 2)
                    for kk in tot:
                        tot[kk] += g[kk]
            fc_s = 0
            for m in metas:
                ct = m.get("freecad_cycle_time")
                if ct and re.fullmatch(r"\d+:\d\d:\d\d", ct):
                    h_, mi_, s_ = (int(x) for x in ct.split(":"))
                    fc_s += 3600 * h_ + 60 * mi_ + s_
            res = dict(pid=pc["pid"], setup=su["name"], up=up, label=su.get("label"), repeat=su.get("repeat", 1),
                       g0_links_to_g1=n_links,
                       rotation=[list(r) for r in R],
                       stock_box_setup=[round(v, 3) for v in (sx0, sy0, sz0, sL, sW, sH)],
                       gcode=os.path.relpath(gpath, HERE) if posted else None, ops=metas, errors=errors,
                       tool_changes=ntc, cut_min=round(tot["feed_s"] / 60, 2), rapid_min=round(tot["rapid_s"] / 60, 2),
                       total_min=round((tot["feed_s"] + tot["rapid_s"]) / 60, 2),
                       freecad_cycle_min=round(fc_s / 60, 2), freecad_job_cycle=getattr(job, "CycleTime", None))
            results.append(res)
            print("%-10s %-3s ops %2d errors %d  recount %.1f min  FreeCAD %.1f min" % (
                su["name"], up, len(metas), len(errors), res["total_min"], res["freecad_cycle_min"]), flush=True)
            for e in errors:
                print("     ERROR", e["label"], e["error"][:160], flush=True)
            for m in metas:
                if m.get("error"):
                    print("     EMPTY", m["label"], flush=True)
    return FreeCAD.Version(), results


def main():
    try:
        import FreeCAD  # noqa: F401
    except ImportError:
        sys.exit("run under freecadcmd (see the docstring)")
    version, results = run()
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    old = {}
    if os.environ.get("FT_CAM_ONLY") and os.path.exists(OUT_JSON):
        redo = set(os.environ["FT_CAM_ONLY"].split(","))
        old = {r["setup"]: r for r in json.load(open(OUT_JSON)).get("setups", []) if r["pid"] not in redo}
    for r in results:
        old[r["setup"]] = r
    out = dict(tool="FreeCAD %s (%s) CAM workbench, freecadcmd headless; linuxcnc post" % (".".join(version[:3]),
                                                                                          version[3]),
               tools={("T%d" % t): dict(v, feed_mm_min=round(T.feed_mm_min(t), 1)) for t, v in T.TOOLS.items()},
               setups=sorted(old.values(), key=lambda r: r["setup"]))
    json.dump(out, open(OUT_JSON, "w"), indent=1)
    print("wrote", OUT_JSON)


if __name__ == "__main__":
    main()
