"""Geometry engine for the hand-operation checks (issue #260, PR #266): scene, part paths, tool and hand access.

Used by run_ops.py; operations.py says what to check. Nothing here is specific to one operation.

  Scene(cad, module, reservoir)   builds the model with lpbf_low.build() from the given cad folder, splits every fastener
                                  compound into one object per screw (joints.REGISTRY gives each screw's point and axis),
                                  tessellates every object once (cached under /tmp/ops-work/cache) and keeps an FCL BVH
                                  per object.
  path_check(...)                 moves a set of objects along a polyline (straight-line assembly-by-disassembly, or the
                                  documented path) through a machine state with a given set of objects present. FCL finds
                                  touching pairs fast; a pair only blocks if manifold3d finds more than VOL_TOL mm3 of
                                  shared volume and OpenCascade's exact boolean confirms it on the B-rep (chord error on a
                                  sliding fit is not a block). Also returns the smallest FCL gap along the path.
  tool_check(...)                 puts a real hand tool (tools.py) on a screw's axis, engaged in its socket, with a hand
                                  envelope on the handle, and turns it about the axis in 15 deg steps. A turning tool passes
                                  when it has a free arc of at least 60 deg (a hex key can be re-indexed every 60 deg); the
                                  torque screwdriver passes when it fits at all. The ball-end key may also tilt 15 or
                                  25 deg off the axis.
  reach_check(...)                a flat hand at a point plus a forearm running straight back from it, for operations
                                  done by hand (clamps, latches, sensors).

Units mm. Every clearance is the FCL distance between tessellated solids (0.1 mm chord), so it is good to ~0.1 mm.
"""
from __future__ import annotations

import hashlib
import math
import pathlib
import pickle
import sys
import time

import fcl
import manifold3d as mf
import numpy as np
import trimesh

VOL_TOL = 0.5        # mm3 of shared volume that counts as a block (as analysis/interference.py)
CHORD = 0.1          # tessellation chord, mm
CACHE = pathlib.Path("/tmp/ops-work/cache")


# ------------------------------------------------------------------------------------------------ small helpers
def loc_matrix(loc):
    if loc is None:
        return np.eye(4)
    t = loc.wrapped.Transformation()
    m = np.eye(4)
    for i in range(3):
        for j in range(4):
            m[i, j] = t.Value(i + 1, j + 1)
    return m


def T(v):
    m = np.eye(4)
    m[:3, 3] = v
    return m


def rot(axis, deg):
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    t = math.radians(deg)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    m = np.eye(4)
    m[:3, :3] = np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K
    return m


def frame(origin, z):
    """4x4 frame with its origin at `origin` and local +z along `z` (local x any perpendicular)."""
    z = np.asarray(z, float)
    z = z / np.linalg.norm(z)
    h = np.array([0.0, 0.0, 1.0]) if abs(z[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    x = np.cross(h, z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    m = np.eye(4)
    m[:3, 0], m[:3, 1], m[:3, 2], m[:3, 3] = x, y, z, origin
    return m


def bvh(V, F):
    b = fcl.BVHModel()
    b.beginModel(len(V), len(F))
    b.addSubModel(np.asarray(V, float), np.asarray(F, np.int64))
    b.endModel()
    return b


def fobj(geom, M4):
    return fcl.CollisionObject(geom, fcl.Transform(M4[:3, :3], M4[:3, 3]))


def aabb(V, M4):
    w = V @ M4[:3, :3].T + M4[:3, 3]
    return w.min(0), w.max(0)


def overlap(a, b, pad=0.0):
    return bool(np.all(a[0] - pad <= b[1]) and np.all(b[0] - pad <= a[1]))


def tess(shape, tol=CHORD):
    vs, ts = shape.tessellate(tol, 0.3)
    if not ts:
        return None, None
    return np.array([(p.x, p.y, p.z) for p in vs], float), np.array(ts, np.int64)


def to_manifold(V, F):
    tm = trimesh.Trimesh(V, F, process=True)
    tm.merge_vertices(digits_vertex=4)
    tm.remove_unreferenced_vertices()
    if tm.volume < 0:
        tm.invert()
    m = mf.Manifold(mf.Mesh(vert_properties=np.asarray(tm.vertices, np.float32), tri_verts=np.asarray(tm.faces, np.uint32)))
    if m.status() != mf.Error.NoError or m.is_empty():
        m = mf.Manifold.hull_points(np.asarray(tm.vertices, np.float32))
    return m


# ------------------------------------------------------------------------------------------------ the scene
class Scene:
    """Every part of lpbf_low.build(), with fastener compounds split into one object per screw."""

    def __init__(self, cad, module="M50", reservoir=None, verbose=True):
        cad = str(pathlib.Path(cad).resolve())
        if cad not in sys.path:
            sys.path.insert(0, cad)
        import fasteners as FS  # noqa: E402
        import joints as J  # noqa: E402
        import lpbf_low as M  # noqa: E402
        import module_params as MP  # noqa: E402
        self.M, self.J, self.FS, self.MP = M, J, FS, MP
        t0 = time.time()
        self.parts = M.build(module=module, reservoir=reservoir)
        self.reg = {k: dict(v) for k, v in J.REGISTRY.items()}
        self.module = module
        objs = []
        for i, p in enumerate(self.parts):
            if "calibration" in p.tags:      # calibration fixtures (the power head on the plate) exist only in interference.py's
                continue                     # calibration state; no hand operation here runs with them in place
            if "fastener" in p.tags:
                key, pn = p.tags[1], p.mcm
                r = self.reg[key]
                items = r["items"] if r["pn"] == pn else next(it for q, it in r["extra"] if q == pn)
                base = p.name.split(" (")[0]
                for k, (P, n) in enumerate(items):
                    objs.append(dict(name=f"{base} #{k + 1}", part=i, item=k, key=key, pn=pn, P=tuple(P), n=tuple(n),
                                     shape=FS.place(pn, P, n), kind=FS.CATALOG[pn]["kind"]))
            else:
                objs.append(dict(name=p.name, part=i, item=None, key=None, pn=p.mcm, shape=p.shape, kind="part"))
        self.objs = objs
        # cache tessellations by the cad sources' hash + module + reservoir
        h = hashlib.sha256()
        for f in sorted(pathlib.Path(cad).glob("*.py")):
            h.update(f.read_bytes())
        h.update(f"{module}-{reservoir}-{CHORD}-nocal".encode())
        CACHE.mkdir(parents=True, exist_ok=True)
        cf = CACHE / f"mesh-{h.hexdigest()[:16]}.pkl"
        if cf.exists():
            meshes = pickle.loads(cf.read_bytes())
        else:
            meshes = [tess(o["shape"]) for o in objs]
            cf.write_bytes(pickle.dumps(meshes))
        for o, (V, F) in zip(objs, meshes):
            o["V"], o["F"] = V, F
            o["bvh"] = bvh(V, F) if V is not None else None
            o["man"] = None
        self.n = len(objs)
        if verbose:
            print(f"scene: {len(self.parts)} parts -> {self.n} objects in {time.time() - t0:.1f} s", flush=True)

    # --- selection
    def find(self, *keys, exclude=(), fasteners=True):
        out = []
        for i, o in enumerate(self.objs):
            nm = self.parts[o["part"]].name if o["item"] is not None else o["name"]
            if any(k in nm for k in keys) and not any(x in nm for x in exclude):
                if fasteners or o["item"] is None:
                    out.append(i)
        return out

    def joint(self, key, pn=None):
        """object indices of the screws of joint `key` (its primary part number unless pn is given)."""
        pn = pn or self.reg[key]["pn"]
        return [i for i, o in enumerate(self.objs) if o["key"] == key and o["pn"] == pn]

    def group(self, g):
        return [i for i, o in enumerate(self.objs) if self.M.moves_with(self.parts[o["part"]], g)]

    def label(self, i):
        return self.objs[i]["name"]

    def short(self, i):
        return self.objs[i]["name"].split(" (")[0].split(":")[0][:60]

    # --- posing
    def pose(self, i, state):
        return loc_matrix(self.M.part_location(self.parts[self.objs[i]["part"]], state))

    def manifold(self, i):
        o = self.objs[i]
        if o["man"] is None and o["V"] is not None:
            o["man"] = to_manifold(o["V"], o["F"])
        return o["man"]

    def exact_volume(self, i, Mi, j, Mj):
        """OpenCascade exact shared volume of objects i and j at the given 4x4 poses."""
        import cadquery as cq
        from OCP.gp import gp_Trsf

        def loc(m):
            t = gp_Trsf()
            t.SetValues(*[float(m[r, c]) for r in range(3) for c in range(4)])
            return cq.Location(t)
        try:
            a = self.objs[i]["shape"].moved(loc(Mi))
            b = self.objs[j]["shape"].moved(loc(Mj))
            c = a.intersect(b)
            return float(c.Volume()) if c is not None else 0.0
        except Exception:  # noqa: BLE001
            return float("nan")

    def overlap_volume(self, i, Mi, j, Mj):
        a, b = self.manifold(i), self.manifold(j)
        if a is None or b is None:
            return 0.0
        return (a.transform(Mi[:3, :].astype(np.float32)) ^ b.transform(Mj[:3, :].astype(np.float32))).volume()


# ------------------------------------------------------------------------------------------------ world: present objects at a state
class World:
    def __init__(self, sc: Scene, state: dict, present):
        self.sc, self.state = sc, dict(state)
        self.present = sorted(set(present))
        self.M = {i: sc.pose(i, state) for i in self.present}
        self.bb = {i: aabb(sc.objs[i]["V"], self.M[i]) for i in self.present if sc.objs[i]["V"] is not None}
        self.fo = {i: fobj(sc.objs[i]["bvh"], self.M[i]) for i in self.bb}

    def near(self, box, pad=0.0, skip=()):
        return [i for i, b in self.bb.items() if i not in skip and overlap(box, b, pad)]

    def collide_geom(self, geom, M4, box, skip=()):
        """indices of present objects whose meshes touch geom at M4."""
        o = fobj(geom, M4)
        hits = []
        for j in self.near(box, 0.05, skip):
            req, res = fcl.CollisionRequest(), fcl.CollisionResult()
            if fcl.collide(o, self.fo[j], req, res):
                hits.append(j)
        return hits

    def distance_geom(self, geom, M4, box, skip=(), pad=60.0):
        o = fobj(geom, M4)
        best, arg = float("inf"), None
        for j in self.near(box, pad, skip):
            req, res = fcl.DistanceRequest(), fcl.DistanceResult()
            d = fcl.distance(o, self.fo[j], req, res)
            if d < best:
                best, arg = d, j
        return best, arg


# ------------------------------------------------------------------------------------------------ part paths
def polyline_samples(path, ds):
    pts = [np.asarray(p, float) for p in path]
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        L = np.linalg.norm(b - a)
        n = max(1, int(math.ceil(L / ds)))
        for k in range(1, n + 1):
            out.append(a + (b - a) * k / n)
    return out


def path_check(sc: Scene, state, present, moving, path, ds=2.0, start_skip=0.3, exact=True, max_exact=6):
    """Move objects `moving` (posed at `state`) by the offsets along `path` (list of xyz offsets, first usually 0).
    Returns dict(ok, blocked_by, at, at_s, exact_mm3, min_gap, gap_with, n)."""
    w = World(sc, state, [i for i in present if i not in moving])
    mov = [i for i in moving if sc.objs[i]["V"] is not None]
    Mm = {i: sc.pose(i, state) for i in mov}
    samples = polyline_samples(path, ds)
    s_acc, prev = 0.0, samples[0]
    min_gap, gap_with, cleared = float("inf"), None, {}
    n_exact = 0
    for k, off in enumerate(samples):
        s_acc += float(np.linalg.norm(off - prev))
        prev = off
        if k == 0 and start_skip:
            # the part sits on its seat at s = 0: test a hair along the first leg instead
            d0 = samples[1] - samples[0] if len(samples) > 1 else np.zeros(3)
            off = samples[0] + (d0 / (np.linalg.norm(d0) + 1e-12)) * start_skip
        Toff = T(off)
        for i in mov:
            Mi = Toff @ Mm[i]
            box = aabb(sc.objs[i]["V"], Mi)
            for j in w.collide_geom(sc.objs[i]["bvh"], Mi, box):
                vol = sc.overlap_volume(i, Mi, j, w.M[j])
                if vol <= VOL_TOL:
                    continue
                key = (i, j)
                if key in cleared and vol <= 3.0 * cleared[key] + VOL_TOL:
                    continue
                ve = sc.exact_volume(i, Mi, j, w.M[j]) if (exact and n_exact < max_exact) else vol
                n_exact += 1
                if ve == ve and ve <= VOL_TOL:
                    cleared[key] = vol
                    continue
                return dict(ok=False, blocked_by=sc.label(j), blocker=j, mover=sc.label(i), at=[round(float(x), 1) for x in off],
                            at_s=round(s_acc, 1), mesh_mm3=round(float(vol), 1), exact_mm3=None if ve != ve else round(float(ve), 1),
                            min_gap=None if min_gap == float("inf") else round(min_gap, 2),
                            gap_with=None if gap_with is None else sc.label(gap_with), n=k)
        if k % 3 == 0 or k == len(samples) - 1:
            for i in mov:
                Mi = Toff @ Mm[i]
                box = aabb(sc.objs[i]["V"], Mi)
                d, j = w.distance_geom(sc.objs[i]["bvh"], Mi, box, pad=10.0)
                if j is not None and 0 < d < min_gap:
                    min_gap, gap_with = d, j
    return dict(ok=True, blocked_by=None, min_gap=None if min_gap == float("inf") else round(min_gap, 2),
                gap_with=None if gap_with is None else sc.label(gap_with), n=len(samples), length=round(s_acc, 1))


def straight_paths(dirs, L, pre=None):
    """candidate removal paths: straight lines of length L along each of `dirs`, optionally after a first leg `pre`."""
    out = []
    for d in dirs:
        d = np.asarray(d, float)
        p0 = np.zeros(3)
        legs = [p0]
        if pre is not None:
            legs.append(np.asarray(pre, float))
        legs.append(legs[-1] + d / np.linalg.norm(d) * L)
        out.append(legs)
    return out


AXES = {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0), "+z": (0, 0, 1), "-z": (0, 0, -1)}


# ------------------------------------------------------------------------------------------------ tools on screws
def screw_frame(sc: Scene, i, state):
    """frame at the head's top on screw object i: local +z points out of the socket (away from the tip)."""
    o = sc.objs[i]
    c = sc.FS.CATALOG[o["pn"]]
    P, n = np.asarray(o["P"], float), np.asarray(o["n"], float)
    k = {"shcs": c.get("k", 0.0), "captive": c.get("k", 0.0)}.get(c["kind"], 0.0)
    top = P - n * k
    Mw = sc.pose(i, state)
    top_w = Mw[:3, :3] @ top + Mw[:3, 3]
    out_w = Mw[:3, :3] @ (-n)
    return frame(top_w, out_w), c


def arc_free(free):
    """largest run of consecutive True in a circular list -> (count, start index)."""
    n = len(free)
    if all(free):
        return n, 0
    best, start, run, rs = 0, 0, 0, 0
    for k in range(2 * n):
        if free[k % n]:
            if run == 0:
                rs = k % n
            run += 1
            if run > best:
                best, start = min(run, n), rs
        else:
            run = 0
    return best, start


def tool_check(sc: Scene, w: World, i, tool, step_deg=15.0, tilts=(0.0,), min_arc=60.0):
    """Tool `tool` (tools.Tool) on screw object i in world w (the screw itself is skipped).
    Returns dict(ok, arc_deg, tilt, blocked_by: {name: count}, clearance, clear_with, hand_blocked)."""
    F0, c = screw_frame(sc, i, w.state)
    skip = {i}
    blocked = {}
    best = None
    nth = 1 if tool.axisym else int(round(360.0 / step_deg))
    for tilt in tilts:
        azis = [0.0] if tilt == 0 else [0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0]
        for az in azis:
            Ft = F0 @ rot((0, 0, 1), az) @ rot((1, 0, 0), tilt) if tilt else F0
            free = []
            for k in range(nth):
                Mk = Ft @ rot((0, 0, 1), k * step_deg)
                ok = True
                for part_name, (geom, V) in tool.meshes.items():
                    box = aabb(V, Mk)
                    hits = w.collide_geom(geom, Mk, box, skip)
                    if hits:
                        ok = False
                        for j in hits:
                            nm = f"{part_name}: {sc.short(j)}"
                            blocked[nm] = blocked.get(nm, 0) + 1
                free.append(ok)
            if tool.axisym:
                arc = 360.0 if free[0] else 0.0
                k0 = 0
            else:
                cnt, k0 = arc_free(free)
                arc = cnt * step_deg
            cand = (arc, -tilt, az, k0, Ft, free)
            if best is None or cand[:2] > best[:2]:
                best = cand
            if arc >= 360.0 and tilt == 0:
                break
        if best and best[0] >= min_arc:
            break
    arc, mt, az, k0, Ft, free = best
    ok = arc >= (min_arc if not tool.axisym else 360.0)
    # clearance at the middle of the best free arc
    clearance, cw = None, None
    if arc > 0:
        kmid = (k0 + int(arc / step_deg) // 2) % max(1, len(free))
        Mk = Ft @ rot((0, 0, 1), kmid * step_deg)
        dmin = float("inf")
        for part_name, (geom, V) in tool.meshes.items():
            d, j = w.distance_geom(geom, Mk, aabb(V, Mk), skip, pad=40.0)
            if j is not None and d < dmin:
                dmin, cw = d, f"{part_name}: {sc.short(j)}"
        clearance = None if dmin == float("inf") else round(dmin, 2)
    top = sorted(blocked.items(), key=lambda kv: -kv[1])[:3]
    return dict(ok=bool(ok), arc_deg=round(arc, 0), tilt_deg=-mt, clearance=clearance, clear_with=cw, blocked_by=[n for n, _ in top])


def withdraw_check(sc: Scene, w: World, i, extra=2.0):
    """the screw itself has to come out along its axis: a cylinder 0.4 mm under the head's diameter (thread diameter for
    a set screw) from the head top outward for the screw's length + 2 mm must be free."""
    F0, c = screw_frame(sc, i, w.state)
    # a hair under the head (or thread) diameter, so the screw's own counterbore or tapped hole does not count
    d = float(c.get("dk", c.get("d", 3.0))) - 0.4
    L = float(c.get("L", 10.0)) + extra
    m = trimesh.creation.cylinder(radius=d / 2, height=L, sections=24)
    m.apply_translation((0, 0, L / 2 + 0.3))
    g = bvh(m.vertices, m.faces)
    hits = w.collide_geom(g, F0, aabb(m.vertices, F0), {i})
    return dict(ok=not hits, blocked_by=[sc.short(j) for j in hits][:3])


# ------------------------------------------------------------------------------------------------ hand reach
def reach_check(sc: Scene, w: World, point, approach, skip=(), hand=(100.0, 55.0, 90.0), forearm=(90.0, 65.0), reach=450.0, tag=""):
    """A flat hand (MIL-STD-1472H Fig. 57: bare hand flat 55 x 100) from `point` back toward the person, and a forearm (width x height,
    an assumption: no published forearm opening was confirmed)
    running straight back along `approach` (unit vector from the point toward the person) for `reach` mm."""
    a = np.asarray(approach, float)
    a /= np.linalg.norm(a)
    hw, ht, hl = hand
    fw, fh = forearm
    F = frame(np.asarray(point, float), a)
    hm = trimesh.creation.box(extents=(hw, ht, hl))
    hm.apply_translation((0, 0, hl / 2))
    fm = trimesh.creation.box(extents=(fw, fh, reach - hl))
    fm.apply_translation((0, 0, hl + (reach - hl) / 2))
    # keep the hand's broad side horizontal when the approach is horizontal
    best = None
    for roll in (0.0, 90.0):
        Mr = F @ rot((0, 0, 1), roll)
        hits = {}
        for nm, m in (("hand", hm), ("forearm", fm)):
            g = bvh(m.vertices, m.faces)
            for j in w.collide_geom(g, Mr, aabb(m.vertices, Mr), set(skip)):
                hits[f"{nm}: {sc.short(j)}"] = j
        if best is None or len(hits) < len(best[1]):
            best = (roll, hits)
        if not hits:
            break
    roll, hits = best
    return dict(ok=not hits, roll=roll, blocked_by=list(hits)[:4])
