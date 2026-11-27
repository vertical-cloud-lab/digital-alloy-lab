"""Collision audit of what the robot-build video's frames actually draw (round 8, issue #260, PR #266).

Sterling's byu-vcl lesson 1 (notes/2026-11-26-byu-vcl-video-lessons.md): "an audit of every drawn frame, for everything that
moves, with a depth threshold (1.5 mm) and a short list of allowed contacts. An earlier audit that checked only the arms
reported zero and was wrong." So this reads what the renderer drew (audit_rec.py's recordings, ROBOTBUILD_AUDIT=1), not
what a planner said it would draw: people, bases, loads, failed attempts and scripted moves are all in it.

    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/scene_audit.py names 50-integration      # the chapter's actors
    /tmp/capmem 3G /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/scene_audit.py run 50-integration [--every 1]
    xvfb-run -a ... scene_audit.py run 50-integration --stills 3    # and close-up stills of the worst pairs

Method
------
* Replay. frames.pkl holds, per recorded frame, only the actors whose mesh, matrix, opacity or visibility changed;
  meshes.pkl one record per mesh version. Replaying every record up to frame n gives the drawn state at n. A chapter
  rendered in slices (<chapter>.part<k>/audit, or <chapter>/audit.part<k> after merge_parts.py) is replayed slice by slice;
  each slice's first record holds its whole scene.
* Movers. A first pass over frames.pkl marks every actor whose matrix or mesh changes at any point in the chapter (people are
  re-skinned every frame, so all their parts move). Each mover is checked in every checked frame (also while it rests)
  against every other visible actor with opacity >= OPAQUE, moving or static. Pairs of two static actors are not checked.
* Broad phase: world-space bounding boxes (numpy). Narrow phase: python-fcl BVH meshes (OBBRSS) of the recorded triangles,
  built once per mesh version (identical re-skins share one model), no decimation unless a mesh has more than
  MAX_TRIS triangles (then vtkQuadricClustering, and the pair is re-checked on the full mesh before it is reported). Of a
  pair, the mesh with fewer triangles is the one shrunk by TOUCH_MM (round 9), so a big mesh (chapter 30's stock, ~0.6 M
  triangles re-meshed every 3 frames) gets one BVH per version, not two.
* Depth: the translational penetration depth, the same measure as the planner's audit (analysis/robot/cell.py depth(),
  byu-vcl PR 318's collide.depth()): the shortest translation of one mesh, over 26 directions (the faces, edges and corners
  of a cube), on the ladder 1.5, 3, 6, 12, 25, 50, 100 mm, that frees it; a pair freed at 1.5 mm is within the limit. A
  deeper pair is refined by bisection along the directions that free it (to about 1/16 of the rung). It is the minimum
  translation that separates the two drawn shapes (sampled in 26 directions, so at most ~8 % over the true minimum), which is
  what a viewer sees as one thing inside another; unlike a vertex's distance inside the other mesh, it needs no closed meshes.
* Cache: a pair is re-checked only when one of its meshes or their relative pose changed; so rigid sub-meshes of one body
  (a UR link's pieces, the MiR's boxes, a module's parts) cost one check each. A violating pair whose relative pose and
  meshes never change over the chapter is reported apart as "rigid" (it is how the model is drawn, not something the motion
  does).
* Allowed contacts: ALLOWED below, each a pair of name patterns, a depth it may reach (None: any) and its reason. Everything
  else deeper than 1.5 mm is a violation.

Memory (round 9): chapter 30's round-8 audit ran out of its 3 GB cap 200 frames in. The cause was the decimation of
its stock (vtkQuadricDecimation on ~0.6 M triangles: over 4 GB and minutes per version, measured on a synthetic
recording), not the people. Decimation is now vtkQuadricClustering (linear, bounded) and only over MAX_TRIS = 2.5 M; a
full BVH of 0.6 M triangles is ~350 MB and 1.8 s. The audit streams: mesh versions and their BVHs are dropped as soon as
no actor draws them (as before); every AUDIT_CHUNK recorded frames, and whenever the process passes AUDIT_SOFT_MB, every
BVH still cached is dropped too (they are rebuilt on demand) and the heap is trimmed (malloc_trim); the worst frame of each
violating pair (for --stills) is kept on disk, not in memory. `peak_rss_mb` in the output says what it took.

Output: analysis/out/videoqa/scene_audit_<chapter>.json (frames checked, pairs, worst depth and frame numbers per pair) and,
with --stills, scene_audit_<chapter>_<k>.png (the frame as drawn beside a close-up of the pair from the recorded meshes).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pickle
import re
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = REPO / "desktop-lpbf" / "analysis" / "out" / "videoqa"
ROOT = Path(os.environ.get("ROBOTBUILD", "/tmp/robotbuild"))
FRAMES = ROOT / "frames"
KEEP = Path(os.environ.get("AUDIT_KEEP", "/tmp/w3audit"))      # hard-linked copies of slices' audit folders (watch)

DEPTH_MM = 1.5
TOUCH_MM = 0.3                       # one mesh of a pair is shrunk this much first (byu-vcl collide._eroded, cell.py
                                     # Body.eroded): a fit drawn at zero clearance (a pin in its bore, a screw in its hole,
                                     # a part on its seat) reads as touching, not as its whole length deep
OPAQUE = 0.3                         # actors fainter than this are not obstacles (glass at 0.38 is)
LADDER = (1.5, 3.0, 6.0, 12.0, 25.0, 50.0, 100.0)
DEEP = 999.0
MAX_TRIS = int(os.environ.get("AUDIT_MAX_TRIS", "2500000"))
CHUNK = int(os.environ.get("AUDIT_CHUNK", "200"))          # recorded frames between drops of every cached BVH
SOFT_MB = int(os.environ.get("AUDIT_SOFT_MB", "1800"))     # resident size past which every cached BVH is dropped at once
REFINE = int(os.environ.get("AUDIT_REFINE", "6"))   # a violating pair's depth is re-measured at most every REFINE frames
_DIRS = np.array([d for d in product((-1, 0, 1), repeat=3) if any(d)], float)
_DIRS /= np.linalg.norm(_DIRS, axis=1)[:, None]

ARM_LINKS = ("base", "shoulder", "upper_arm", "forearm", "wrist1", "wrist2", "wrist3")
ADJ = {("base", "shoulder"), ("shoulder", "upper_arm"), ("upper_arm", "forearm"), ("forearm", "wrist1"),
       ("wrist1", "wrist2"), ("wrist2", "wrist3")}
PERSON_PARTS = r"(skin|forearm|coat|coat skirt|coat collar|shirt|glove|shoes|trousers|hair|brow|iris|sclera|glasses \w+)"
RE_PERSON = re.compile(rf"^(?P<who>[^/]+)/{PERSON_PARTS}$")
RE_LINK = re.compile(r"^(?P<arm>.+?)/(?P<link>base|shoulder|upper_arm|forearm|wrist1|wrist2|wrist3)/\d+$")
# what rides on the flange: the tool changer, the 2F-85's parts, the wrist camera, fingertip caps, a quick-change plate and
# the shop arms' alternative grippers
# a person's eyes, brows, hair and glasses ride on the head, inside or just over its skin: the skin is checked for them
# (and their own meshes are left out as movers, which saves rebuilding five more BVH models per person and frame)
RE_RIDERS = re.compile(r"^[^/]+/(iris|sclera|brow|hair|glasses \w+)$")
RE_FLANGE = re.compile(r"^(?P<arm>.+?)/(changer|gr/.*|cam/.*|cap/.*|qc|3fg/.*|vgp/.*)$")


# ================================================================================================ allowed contacts
def _same_person(a, b):
    ma, mb = RE_PERSON.match(a), RE_PERSON.match(b)
    return bool(ma and mb and ma["who"] == mb["who"])


def _arm_of(n):
    m = RE_LINK.match(n) or RE_FLANGE.match(n)
    return m["arm"] if m else None


def _adjacent_links(a, b):
    ma, mb = RE_LINK.match(a), RE_LINK.match(b)
    if not (ma and mb and ma["arm"] == mb["arm"]):
        return False
    la, lb = ma["link"], mb["link"]
    return la == lb or (la, lb) in ADJ or (lb, la) in ADJ


def _flange_stack(a, b):
    """wrist3 and everything bolted to the flange, of one arm."""
    for x, y in ((a, b), (b, a)):
        fx = RE_FLANGE.match(x)
        if not fx:
            continue
        ly = RE_LINK.match(y)
        if ly and ly["arm"] == fx["arm"] and ly["link"] == "wrist3":
            return True
        fy = RE_FLANGE.match(y)
        if fy and fy["arm"] == fx["arm"]:
            return True
    return False


def _base_on_mir(a, b):
    """An arm's base link (and its shoulder housing, which turns on it) on its own MiR's mounting plate."""
    for x, y in ((a, b), (b, a)):
        m = RE_LINK.match(x)
        if m and m["link"] in ("base",):
            arm = m["arm"]
            tags = {arm, arm[3:] if arm.startswith("arm") else arm}
            if any(y.startswith(f"mir{t}/") for t in tags):
                return True
    return False


def _pat(pa, pb):
    ra, rb = re.compile(pa), re.compile(pb)
    return lambda a, b: bool((ra.search(a) and rb.search(b)) or (ra.search(b) and rb.search(a)))


# (name, test, depth it may reach or None for any, reason). Chapter-specific entries are keyed by chapter prefix.
RE_NOT_SOLID = re.compile(r"(^|/)[^/]*(water|coolant|\barc\b|glow|spray)[^/]*$", re.I)


def _not_solid(a, b):
    return bool(RE_NOT_SOLID.search(a) or RE_NOT_SOLID.search(b))


ALLOWED_ALL = [
    ("not a solid", _not_solid, None,
     "water in a wash or rinse tank, coolant, a welding arc's glow: drawn volumes that things may enter"),
    ("person's own layers", _same_person, None,
     "one person's skin, clothes, shoes and glasses are layers of one skinned body (people.py offsets the clothes from it)"),
    ("adjacent UR links", _adjacent_links, None,
     "neighbouring UR12e links meet at their joint (the pieces of one link, and the planner's ADJACENT pairs in cell.py)"),
    ("flange stack", _flange_stack, None,
     "the tool changer, the 2F-85 and its fingers, caps and the wrist camera are bolted to the flange and to each other"),
    ("arm base on its MiR", _base_on_mir, None,
     "the arm's base is bolted to its own MiR's mounting plate (only the base link; any other link in its MiR is a violation)"),
]
ALLOWED_CHAPTER = {
    "50-integration": [
        ("lift table's own parts", _pat(r"^lift/", r"^lift/"), None,
         "the scissor arms are pinned to the lift table's base and platform, and the handle is bolted to the base"),
        ("hands on the load", _pat(r"^op/(glove|forearm|skin)$", r"^(m/|lift/handle$)"), 25.0,
         "the person's gloved fingertips on the module, rack, unit or gas part being pushed, or the hands on the lift "
         "table's handle bar (people.py's fingers curl a little into what they touch), up to 25 mm"),
        ("load on the lift table", _pat(r"^lift/body$", r"^m/"), 3.0,
         "a load standing on the lift table's platform (its feet 3 mm above the tray's floor), up to 3 mm"),
    ],
}


FASTENER_KINDS = ("shcs", "fhcs", "set", "insert", "dowel", "plunger")
RE_DRIVER = re.compile(r"^[^/]+/tool/(nutrunner|screwdriver|driver|bit|socket)", re.I)


def fastener_rules(kinds):
    """The assembly chapters (actors "o<i>", kinds from the run's asm_scene.pkl): a screw, insert or dowel drawn in its
    hole, and a driver's bit or socket on the screw it turns."""
    def is_f(n):
        return kinds.get(n) in FASTENER_KINDS

    def screw_in_part(a, b):
        return (is_f(a) and kinds.get(b) == "part") or (is_f(b) and kinds.get(a) == "part")

    def driver_on_screw(a, b):
        return (is_f(a) and RE_DRIVER.match(b) is not None) or (is_f(b) and RE_DRIVER.match(a) is not None)

    def screw_in_insert(a, b):
        sc = ("shcs", "fhcs", "set")
        return (kinds.get(a) in sc and kinds.get(b) == "insert") or (kinds.get(b) in sc and kinds.get(a) == "insert")
    return [
        ("screw in its hole", screw_in_part, 40.0,
         "a socket-head, flat-head or set screw, insert, dowel or plunger drawn in its hole: its thread or shank is drawn "
         "inside the part it fastens (the CAD's holes are not threaded), up to 40 mm"),
        ("screw in its insert", screw_in_insert, 40.0,
         "a screw threaded into its threaded insert (round 9: chapter 41's 19 insert x screw pairs, up to 10.5 mm in round 8; "
         "the inserts are drawn as solid sleeves), up to 40 mm"),
        ("driver on its screw", driver_on_screw, 30.0,
         "the nutrunner's or screwdriver's bit or socket on the screw it turns, up to 30 mm (the socket's depth)"),
    ]


def allowed_rules(chapter, kinds=None):
    rules = list(ALLOWED_ALL)
    for pre, extra in ALLOWED_CHAPTER.items():
        if chapter.startswith(pre):
            rules += extra
    if kinds:
        rules += fastener_rules(kinds)
    return rules


# ================================================================================================ reading the recordings
def stream(path):
    """Every pickled record of a stream, up to its end or a truncated last record (a render killed mid-write)."""
    if not Path(path).exists():
        return
    with open(path, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                return
            except Exception as e:                                  # noqa: BLE001
                print(f"  {path}: stream ends in a damaged record ({e!r})", flush=True)
                return


def audit_dirs(chapter):
    """The recording folders of a chapter, in frame order: <chapter>/audit, the merged slices' <chapter>/audit.part<k>,
    unmerged slices <chapter>.part<k>/audit, and copies kept by `watch` (KEEP/<folder>/audit) of slices since merged."""
    found = {}
    d = FRAMES / chapter / "audit"
    if (d / "frames.pkl").exists():
        found[chapter] = d
    for d in sorted((FRAMES / chapter).glob("audit.part*")):
        found[f"{chapter}.part{d.name.rsplit('part', 1)[1]}"] = d
    for d in sorted(FRAMES.glob(f"{chapter}.part*")):
        if (d / "audit" / "frames.pkl").exists():
            found[d.name] = d / "audit"
    for d in sorted(KEEP.glob(f"{chapter}.part*")) + ([KEEP / chapter] if (KEEP / chapter).exists() else []):
        if d.name not in found and (d / "audit" / "frames.pkl").exists():
            found[d.name] = d / "audit"

    def order(k):
        return int(k.rsplit("part", 1)[1]) if ".part" in k else -1
    return [(k, found[k]) for k in sorted(found, key=order)]


def frame_png(chapter, n):
    """The frame as drawn, wherever it is now (merged or still in its slice)."""
    for d in [FRAMES / chapter, *sorted(FRAMES.glob(f"{chapter}.part*")), *sorted(KEEP.glob(f"{chapter}*"))]:
        p = d / f"{n:05d}.png"
        if p.exists():
            return p
    return None


class Meshes:
    """meshes.pkl read lazily: a frame only refers to mesh versions written before it, so reading forward until a key turns
    up keeps at most one frame's worth of versions in memory. `want(name)`: keep only those actors' versions."""

    def __init__(self, path, want=None):
        self.it = stream(path)
        self.ahead = {}
        self.lastF = {}
        self.want = want

    def get(self, key):
        while key not in self.ahead:
            try:
                r = next(self.it)
            except StopIteration:
                raise KeyError(key)
            nm = r["name"]
            if self.want is not None and not self.want(nm):
                continue
            F = r["F"] if r["F"] is not None else self.lastF.get(nm)
            if F is None:
                F = np.zeros((0, 3), np.int32)
            self.lastF[nm] = F
            self.ahead[r["key"]] = (nm, np.asarray(r["V"], np.float32), np.asarray(F, np.int32))
        return self.ahead.pop(key)


class Replay:
    """The drawn state, frame by frame: for each recorded frame (tag, n, actors {name: Actor}, dirty names). Mesh versions
    are shared by content (identical re-skins are one Geom) and dropped when no actor draws them any more."""

    def __init__(self, dirs, want=None):
        self.dirs, self.want = dirs, want
        self.geoms, self.refs = {}, {}
        self.truncated = False

    def drop_models(self, actors):
        """Drop every cached BVH (geoms and the actors' FCL objects); they are rebuilt on demand."""
        for g in self.geoms.values():
            g._model = g.full = g._ero = None
        for a in actors.values():
            a.obj = a.eobj = None

    def _ref(self, g, d):
        c = self.refs.get(g.gid, 0) + d
        if c <= 0:
            self.refs.pop(g.gid, None)
            self.geoms.pop(g.gid, None)
        else:
            self.refs[g.gid] = c

    def frames(self):
        for tag, d in self.dirs:
            self.truncated = False
            mesh = Meshes(d / "meshes.pkl", self.want)
            actors = {}
            for r in stream(d / "frames.pkl"):
                n = int(r["n"])
                for name in r.get("removed", ()):
                    a = actors.pop(name, None)
                    if a is not None and a.geom is not None:
                        self._ref(a.geom, -1)
                dirty = set()
                for name, (key, M, op, vis) in r["changed"].items():
                    if self.want is not None and not self.want(name):
                        continue
                    a = actors.get(name)
                    if a is None:
                        a = actors[name] = Actor(name)
                    if key != a.key:
                        try:
                            _, V, F = mesh.get(key)
                        except KeyError:              # a recording still being written: its meshes end here
                            print(f"  {tag}: mesh {key} not in meshes.pkl (still being written?); stopping at frame {n}",
                                  flush=True)
                            self.truncated = True
                            break
                        g = gid_of(V, F)
                        if a.geom is None or g != a.geom.gid:
                            geo = self.geoms.get(g)
                            if geo is None:
                                geo = self.geoms[g] = Geom(V, F, g)
                            self._ref(geo, +1)
                            if a.geom is not None:
                                self._ref(a.geom, -1)
                            a.geom = geo
                            a.obj = None
                            a.eobj = None
                        a.key = key
                    a.M = np.asarray(M, np.float32)
                    a.op, a.vis = float(op), bool(vis)
                    a.lo, a.hi = world_box(a.geom.corners, a.M)
                    dirty.add(name)
                if self.truncated:
                    break
                yield tag, n, actors, dirty
            for a in actors.values():
                if a.geom is not None:
                    self._ref(a.geom, -1)


def histories(dirs):
    """Pass 1 (frames.pkl only): per actor, its changes [(n, key, M, opacity, visible)], and the recorded frame numbers."""
    hist, ns = {}, []
    for tag, d in dirs:
        for r in stream(d / "frames.pkl"):
            n = int(r["n"])
            ns.append(n)
            for name, (key, M, op, vis) in r["changed"].items():
                hist.setdefault(name, []).append((n, (tag, key), np.asarray(M, np.float32), float(op), bool(vis)))
            for name in r.get("removed", ()):
                hist.setdefault(name, []).append((n, None, None, 0.0, False))
    return hist, ns


def _keys_change(h):
    """Does an actor's mesh change? Each slice of a chapter numbers its mesh versions afresh, so only a second version
    within one recording counts."""
    per = {}
    for x in h:
        if x[1] is not None:
            per.setdefault(x[1][0], set()).add(x[1][1])
    return any(len(v) > 1 for v in per.values())


def movers_of(hist):
    """Actors whose matrix or mesh changes after they first appear."""
    out = set()
    for name, h in hist.items():
        Ms = [x[2] for x in h if x[2] is not None]
        if _keys_change(h) or any(not np.allclose(Ms[0], M, atol=1e-3) for M in Ms[1:]):
            out.add(name)
    return out


# ================================================================================================ geometry
def _fcl():
    import fcl
    return fcl


class Geom:
    """One mesh version: local bounding box corners and (lazily) its FCL model."""
    __slots__ = ("V", "F", "corners", "gid", "_model", "ntri", "full", "_reps", "_ero")

    def __init__(self, V, F, gid):
        self.V, self.F, self.gid = V, F, gid
        lo, hi = V.min(0), V.max(0)
        self.corners = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])], float)
        self._model = None
        self.full = None
        self.ntri = len(F)
        self._reps = None
        self._ero = None

    def ero(self):
        """FCL model of the mesh shrunk TOUCH_MM along its vertex normals."""
        if self._ero is None:
            self._ero = _bvh(_fcl(), eroded(self.V, self.F), self.F)
        return self._ero

    def rep_pts(self):
        if self._reps is None:
            self._reps = reps(self.V, self.F)
        return self._reps

    def model(self, full=False):
        fcl = _fcl()
        if full:
            if self.full is None:
                self.full = _bvh(fcl, self.V, self.F)
            return self.full
        if self._model is None:
            V, F = self.V, self.F
            if len(F) > MAX_TRIS:
                V, F = _decimate(V, F, MAX_TRIS)
            self._model = _bvh(fcl, V, F)
            if len(F) == len(self.F):
                self.full = self._model
        return self._model


def eroded(V, F, mm=TOUCH_MM):
    """V moved mm inwards along the vertex normals, each connected piece by the sign of its own volume (welded by position,
    so a box drawn with its own vertices per face shrinks as one piece)."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    V = np.asarray(V, float)
    if not len(F):
        return V
    key = np.round(V * 1000.0).astype(np.int64)
    _, first, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    inv = inv.ravel()
    W = V[first]
    Fw = inv[np.asarray(F, np.int64)]
    a, b, c = W[Fw[:, 0]], W[Fw[:, 1]], W[Fw[:, 2]]
    fn = np.cross(b - a, c - a)
    e = np.r_[Fw[:, [0, 1]], Fw[:, [1, 2]]]
    g = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(len(W), len(W)))
    nc, lab = connected_components(g, directed=False)
    vol = np.bincount(lab[Fw[:, 0]], weights=np.einsum("ij,ij->i", a, np.cross(b, c)), minlength=nc)
    sgn = np.where(vol >= 0.0, 1.0, -1.0)
    vn = np.zeros_like(W)
    for k in range(3):
        np.add.at(vn, Fw[:, k], fn)
    vn /= np.maximum(np.linalg.norm(vn, axis=1), 1e-12)[:, None]
    Wm = W - mm * sgn[lab][:, None] * vn
    return Wm[inv]


def _bvh(fcl, V, F):
    g = fcl.BVHModel()
    g.beginModel(len(V), len(F))
    g.addSubModel(np.ascontiguousarray(V, np.float64), np.ascontiguousarray(F, np.int32))
    g.endModel()
    return g


def _decimate(V, F, n):
    """About n triangles by vertex clustering (vtkQuadricClustering: one pass, memory linear in the mesh). Round 8 used
    vtkQuadricDecimation here, which took over 4 GB and minutes on chapter 30's 0.6 M-triangle stock."""
    import pyvista as pv
    import vtk
    m = pv.PolyData(np.asarray(V, float), np.c_[np.full(len(F), 3), F].ravel())
    lo, hi = np.asarray(V).min(0), np.asarray(V).max(0)
    ext = np.maximum(hi - lo, 1e-6)
    cell = (float(np.prod(ext)) / max(n / 2.0, 1.0)) ** (1.0 / 3.0)       # ~2 triangles a cell on a surface
    div = [int(min(max(e / cell, 2), 1024)) for e in ext]
    q = vtk.vtkQuadricClustering()
    q.SetInputData(m)
    q.SetNumberOfDivisions(*div)
    q.Update()
    out = pv.wrap(q.GetOutput()).triangulate()
    return np.asarray(out.points, np.float32), np.asarray(out.faces).reshape(-1, 4)[:, 1:].astype(np.int32)


def _trim():
    """Give freed heap pages back to the system (glibc keeps them after numpy and FCL free large blocks)."""
    try:
        import ctypes
        ctypes.CDLL("libc.so.6").malloc_trim(0)
    except Exception:                                              # noqa: BLE001
        pass


def _rss_now():
    try:
        return int(open("/proc/self/statm").read().split()[1]) * os.sysconf("SC_PAGE_SIZE") // 2 ** 20
    except Exception:                                              # noqa: BLE001
        return 0


def _wind_impl():
    os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba_cache")
    import numba

    @numba.njit(cache=True)
    def wind(P, V, F):
        """Generalised winding number of each point of P about the triangle mesh (V, F): ~1 inside a closed mesh, ~0
        outside; robust to small holes and to several closed pieces merged into one mesh."""
        out = np.zeros(P.shape[0])
        for k in range(P.shape[0]):
            s = 0.0
            for t in range(F.shape[0]):
                ax = V[F[t, 0], 0] - P[k, 0]
                ay = V[F[t, 0], 1] - P[k, 1]
                az = V[F[t, 0], 2] - P[k, 2]
                bx = V[F[t, 1], 0] - P[k, 0]
                by = V[F[t, 1], 1] - P[k, 1]
                bz = V[F[t, 1], 2] - P[k, 2]
                cx = V[F[t, 2], 0] - P[k, 0]
                cy = V[F[t, 2], 1] - P[k, 1]
                cz = V[F[t, 2], 2] - P[k, 2]
                la = math.sqrt(ax * ax + ay * ay + az * az)
                lb = math.sqrt(bx * bx + by * by + bz * bz)
                lc = math.sqrt(cx * cx + cy * cy + cz * cz)
                det = ax * (by * cz - bz * cy) - ay * (bx * cz - bz * cx) + az * (bx * cy - by * cx)
                div = la * lb * lc + (ax * bx + ay * by + az * bz) * lc + (bx * cx + by * cy + bz * cz) * la + \
                    (cx * ax + cy * ay + cz * az) * lb
                s += 2.0 * math.atan2(det, div)
            out[k] = s / (4.0 * math.pi)
        return out
    return wind


_WIND = []


def winding(P, V, F):
    if not _WIND:
        _WIND.append(_wind_impl())
    return _WIND[0](np.ascontiguousarray(P, np.float64), np.ascontiguousarray(V, np.float64),
                    np.ascontiguousarray(F, np.int64))


def reps(V, F, k=8):
    """Up to k vertices, one in each of the k largest connected pieces of a mesh: if two meshes' surfaces don't cross,
    each piece of one is wholly inside or wholly outside the other, so one vertex a piece decides it."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    if not len(F):
        return V[:1].astype(float)
    e = np.r_[F[:, [0, 1]], F[:, [1, 2]]]
    g = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(len(V), len(V)))
    nc, lab = connected_components(g, directed=False)
    used = np.zeros(len(V), bool)
    used[F.ravel()] = True
    cnt = np.bincount(lab[used], minlength=nc)
    out = []
    for c in np.argsort(-cnt)[:k]:
        if cnt[c] == 0:
            break
        out.append(V[np.nonzero((lab == c) & used)[0][0]])
    return np.asarray(out, float)


def contained(x, Mx, y, My):
    """Is a piece of mesh x wholly inside mesh y, or a piece of y inside x (their surfaces apart)? Geoms x, y at Mx, My."""
    for a, Ma, b, Mb in ((x, Mx, y, My), (y, My, x, Mx)):
        P = a.rep_pts() @ Ma[:3, :3].T.astype(float) + Ma[:3, 3].astype(float)      # world
        lo, hi = world_box(b.corners, Mb)
        P = P[np.all((P >= lo) & (P <= hi), axis=1)]
        if not len(P):
            continue
        Mi = np.linalg.inv(Mb.astype(float))
        Pl = P @ Mi[:3, :3].T + Mi[:3, 3]
        if np.any(winding(Pl, b.V, b.F) > 0.5):
            return True
    return False


def gid_of(V, F):
    h = hashlib.blake2b(digest_size=12)
    h.update(np.ascontiguousarray(V).tobytes())
    h.update(np.ascontiguousarray(F).tobytes())
    return h.hexdigest()


def collide(fcl, oa, ob):
    return fcl.collide(oa, ob, fcl.CollisionRequest(), fcl.CollisionResult()) > 0


def tdepth(fcl, oa, Ma, ob, ca, cb, need=DEPTH_MM, ga=None, gb=None, Mb=None, swallow=True, refine=True):
    """Translational penetration depth of oa (placed at Ma) into ob: 0 if apart, <= `need` if a translation of `need` frees
    it, else the refined smallest freeing translation over 26 directions (DEEP if 100 mm does not). With the Geoms (ga,
    gb, Mb) given, a translation that only swallows one mesh inside the other doesn't count as freeing it, and a mesh
    wholly inside the other counts as in contact (FCL's BVH test only sees surfaces crossing); `swallow` False skips that
    test at the start (the bounding boxes show neither can be inside the other)."""
    def hit(M, inside=True):
        oa.setTransform(fcl.Transform(M[:3, :3], M[:3, 3]))
        if collide(fcl, oa, ob):
            return True
        return inside and ga is not None and contained(ga, M, gb, Mb)
    R, p = Ma[:3, :3].astype(float), Ma[:3, 3].astype(float)
    M0 = np.eye(4)
    M0[:3, :3], M0[:3, 3] = R, p
    try:
        if not hit(M0, swallow):
            return 0.0
        c = ca - cb
        nrm = float(np.linalg.norm(c))
        order = np.argsort(-(_DIRS @ (c / nrm))) if nrm > 1e-9 else np.arange(len(_DIRS))
        prev = 0.0
        for t in LADDER:
            if t > need and not refine:
                return -1.0                   # deeper than `need`, not measured further
            free = []
            for i in order:
                M = M0.copy()
                M[:3, 3] = p + t * _DIRS[i]
                if not hit(M):
                    free.append(i)
                    if t <= need or len(free) >= 4:
                        break
            if free:
                if t <= need:
                    return t
                best = t
                for i in free:
                    lo, hi = prev, t
                    for _ in range(4):
                        mid = 0.5 * (lo + hi)
                        M = M0.copy()
                        M[:3, 3] = p + mid * _DIRS[i]
                        if hit(M):
                            lo = mid
                        else:
                            hi = mid
                    best = min(best, hi)
                return float(best)
            prev = t
        return DEEP
    finally:
        oa.setTransform(fcl.Transform(R, p))


def prep(fcl, x, y):
    """Place the pair's FCL objects: the first one shrunk TOUCH_MM, the second as drawn."""
    if x.eobj is None:
        x.eobj = fcl.CollisionObject(x.geom.ero(), fcl.Transform())
    x.eobj.setTransform(fcl.Transform(x.M[:3, :3].astype(float), x.M[:3, 3].astype(float)))
    if y.obj is None:
        y.obj = fcl.CollisionObject(y.geom.model(), fcl.Transform())
    y.obj.setTransform(fcl.Transform(y.M[:3, :3].astype(float), y.M[:3, 3].astype(float)))


def world_box(corners, M):
    w = corners @ M[:3, :3].T + M[:3, 3]
    return w.min(0), w.max(0)


# ================================================================================================ the audit
class Actor:
    __slots__ = ("name", "key", "M", "op", "vis", "geom", "lo", "hi", "obj", "eobj")

    def __init__(self, name):
        self.name = name
        self.key = None
        self.M = np.eye(4, dtype=np.float32)
        self.op, self.vis = 1.0, False
        self.geom = None
        self.lo = self.hi = None
        self.obj = None
        self.eobj = None


def _ranges(ns, gap):
    out = []
    for n in sorted(ns):
        if out and n - out[-1][1] <= gap:
            out[-1][1] = n
        else:
            out.append([n, n])
    return out


def run(chapter, every=1, stills=0, quiet=False, max_frames=None, only=None):
    fcl = _fcl()
    t0 = time.time()
    dirs = audit_dirs(chapter)
    if not dirs:
        raise SystemExit(f"{chapter}: no recordings (run the renderer with ROBOTBUILD_AUDIT=1)")
    hist, ns_all = histories(dirs)
    movers = movers_of(hist)
    labels = asm_labels() if any(re.match(r"^o\d+$", nm) for nm in hist) else {}
    rules = allowed_rules(chapter, {k: v.split(":")[0] for k, v in labels.items()})
    print(f"{chapter}: {len(ns_all)} recorded frames in {len(dirs)} recording(s), {len(hist)} actors, {len(movers)} move "
          f"({time.time() - t0:.0f} s)", flush=True)
    rule_of = {}                       # (a, b) -> rule index or -1

    def rule_for(a, b):
        k = (a, b) if a < b else (b, a)
        r = rule_of.get(k)
        if r is None:
            r = -1
            for i, (_, test, _, _) in enumerate(rules):
                if test(a, b):
                    r = i
                    break
            rule_of[k] = r
        return r
    viol = {}                           # (a, b) -> dict(worst, frame, frames=set(), snap: a file under snapdir)
    import tempfile
    snapdir = Path(tempfile.mkdtemp(prefix="audit_snaps_"))
    peak = [0]
    allowed_hits = {}                   # rule index -> dict(pairs=set(), frames=0, worst)
    cache = {}                          # (a, b) -> (signature, depth)
    checked = 0
    n_pairs_tested = n_fcl = 0
    recorded = 0
    rp = Replay(dirs)
    pend = set()                        # actors changed since the last checked frame
    active = {}                         # violating pairs of the last checked frame -> depth
    last_tag = None
    for tag, n, actors, dirty in rp.frames():
        recorded += 1
        pend |= dirty
        if tag != last_tag:
            last_tag, active = tag, {}
            pend |= set(actors)
        if max_frames and checked >= max_frames:
            continue
        if every > 1 and n % every:
            continue
        checked += 1
        rss = _rss_now()
        peak[0] = max(peak[0], rss)
        if (CHUNK and checked % CHUNK == 0) or rss > SOFT_MB:
            rp.drop_models(actors)      # stream: nothing cached outlives a chunk, nor the soft limit
            import gc
            gc.collect()
            _trim()
            if rss > SOFT_MB and not quiet:
                print(f"  {tag}: frame {n}: {rss} MB resident, over {SOFT_MB} MB: every cached BVH dropped "
                      f"({_rss_now()} MB now)", flush=True)
        if not pend:                    # nothing moved, appeared or faded: the last frame's verdicts stand
            for k in active:
                viol[k]["frames"].add(n)
            continue
        pend = set()
        active = {}
        live = [a for a in actors.values() if a.vis and a.op >= OPAQUE and a.geom is not None and a.geom.ntri]
        if not live:
            continue
        lo = np.array([a.lo for a in live])
        hi = np.array([a.hi for a in live])
        mv = [i for i, a in enumerate(live) if a.name in movers and not RE_RIDERS.match(a.name)
              and (only is None or re.search(only, a.name))]
        seen = set()
        for i in mv:
            ov = np.all((lo[i] <= hi) & (lo <= hi[i]), axis=1)
            ov[i] = False
            for j in np.nonzero(ov)[0]:
                a, b = live[i], live[j]
                k = (a.name, b.name) if a.name < b.name else (b.name, a.name)
                if k in seen:
                    continue
                seen.add(k)
                ri = rule_for(a.name, b.name)
                lim = DEPTH_MM
                if ri >= 0:
                    if rules[ri][2] is None:
                        ah = allowed_hits.setdefault(ri, dict(pairs=set(), frames=0))
                        if len(ah["pairs"]) < 2000:
                            ah["pairs"].add(k)
                        ah["frames"] += 1
                        continue
                    lim = rules[ri][2]
                # the mesh with fewer triangles is the one shrunk (its BVH is built twice at most), names break ties
                x, y = (a, b) if (a.geom.ntri, a.name) < (b.geom.ntri, b.name) else (b, a)
                rel = np.linalg.inv(x.M.astype(float)) @ y.M.astype(float)
                sig = (x.name, x.geom.gid, y.geom.gid, np.round(rel[:3, :3], 5).tobytes(), np.round(rel[:3, 3], 2).tobytes())
                c = cache.get(k)
                if c is not None and c[0] == sig:
                    dep = c[1]
                elif c is not None and c[1] > lim and n - c[2] < REFINE:
                    # a pair already deeper than its limit: only check it still is (the 1.5 mm rung); its depth is
                    # measured again at most every REFINE frames, and carried in between
                    n_pairs_tested += 1
                    prep(fcl, x, y)
                    n_fcl += 1
                    cx, cy = 0.5 * (x.lo + x.hi), 0.5 * (y.lo + y.hi)
                    q = tdepth(fcl, x.eobj, x.M, y.obj, cx, cy, need=lim, ga=x.geom, gb=y.geom, Mb=y.M, refine=False)
                    dep = c[1] if q < 0 else q
                    cache[k] = (sig, dep, c[2] if q < 0 else n)
                else:
                    n_pairs_tested += 1
                    prep(fcl, x, y)
                    n_fcl += 1
                    cx, cy = 0.5 * (x.lo + x.hi), 0.5 * (y.lo + y.hi)
                    swallow = bool(np.all(x.lo >= y.lo) and np.all(x.hi <= y.hi)) or \
                        bool(np.all(y.lo >= x.lo) and np.all(y.hi <= x.hi))
                    dep = tdepth(fcl, x.eobj, x.M, y.obj, cx, cy, need=lim, ga=x.geom, gb=y.geom, Mb=y.M,
                                 swallow=swallow)
                    if dep > lim and (x.geom.model() is not x.geom.model(full=True) or
                                      y.geom.model() is not y.geom.model(full=True)):
                        ox = fcl.CollisionObject(x.geom.ero(), fcl.Transform(x.M[:3, :3].astype(float),
                                                                                        x.M[:3, 3].astype(float)))
                        oy = fcl.CollisionObject(y.geom.model(full=True), fcl.Transform(y.M[:3, :3].astype(float),
                                                                                        y.M[:3, 3].astype(float)))
                        dep = tdepth(fcl, ox, x.M, oy, cx, cy, need=lim, ga=x.geom, gb=y.geom, Mb=y.M)
                    cache[k] = (sig, dep, n)
                if ri >= 0:
                    ah = allowed_hits.setdefault(ri, dict(pairs=set(), frames=0, worst=0.0))
                    if dep > 0:
                        ah["pairs"].add(k)
                        ah["frames"] += 1
                        ah["worst"] = max(ah.get("worst", 0.0), min(dep, lim))
                if dep > lim:
                    v = viol.get(k)
                    if v is None:
                        v = viol[k] = dict(worst=0.0, frame=n, frames=set(), rule=ri, lim=lim)
                    v["frames"].add(n)
                    active[k] = dep
                    if dep > v["worst"]:
                        v["worst"], v["frame"] = dep, n
                        if stills:              # the worst frame's two meshes, on disk (a stock version is ~15 MB)
                            sp = snapdir / f"{len(viol) if 'snap' not in v else v['snap'].stem}.pkl"
                            sp.write_bytes(pickle.dumps(((x.geom.V, x.geom.F), x.M.copy(), (y.geom.V, y.geom.F),
                                                         y.M.copy()), protocol=4))
                            v["snap"] = sp
        if not quiet and checked % 50 == 0:
            print(f"  {tag}: frame {n}, {checked} checked, {len(viol)} violating pairs, {n_fcl} narrow checks, "
                  f"{len(rp.geoms)} meshes, {time.time() - t0:.0f} s, {_rss_now()} MB now, peak {_rss_mb()} MB", flush=True)
    # rigid pairs: relative pose and meshes constant over every recorded change of either actor
    rigid = {}
    for k in list(viol):
        if _rigid(hist, *k):
            rigid[k] = viol.pop(k)
    gap = max(1, every) + 1
    lab = labels
    rows = []
    for (a, b), v in sorted(viol.items(), key=lambda kv: -kv[1]["worst"]):
        rows.append(dict(a=a, b=b, **({"a_is": lab[a]} if a in lab else {}), **({"b_is": lab[b]} if b in lab else {}),
                         worst_mm=_r(v["worst"]), worst_frame=v["frame"], frames=len(v["frames"]),
                         frame_ranges=_ranges(v["frames"], gap)[:40], limit_mm=v["lim"],
                         rule=rules[v["rule"]][0] if v["rule"] >= 0 else None))
    out = dict(
        chapter=chapter, threshold_mm=DEPTH_MM, opaque_min=OPAQUE,
        recordings=[str(d) for _, d in dirs], frames_recorded=recorded, frames_checked=checked,
        subsample=f"every {every} frame(s) of the recording" if every > 1 else "every recorded frame",
        recorded_every=_recorded_every(ns_all),
        actors=len(hist), movers=len(movers), mover_names=sorted(movers)[:400],
        method="translational penetration depth (26 directions, ladder 1.5-100 mm, bisection-refined), python-fcl BVH meshes "
               "of the recorded triangles, containment by winding numbers; a pair is re-checked when a mesh or the relative "
               f"pose changes; a pair deeper than its limit is re-checked every frame at the limit, its depth re-measured "
               f"at most every {REFINE} frames",
        narrow_checks=n_fcl, pairs_tested=n_pairs_tested,
        violations=len(rows), worst_mm=rows[0]["worst_mm"] if rows else 0.0,
        worst=rows[0] if rows else None, pairs=rows[:300],
        rigid_pairs=[dict(a=a, b=b, worst_mm=_r(v["worst"]), frames=len(v["frames"])) for (a, b), v in
                     sorted(rigid.items(), key=lambda kv: -kv[1]["worst"])][:100],
        allowed=[dict(rule=rules[i][0], depth_allowed_mm=rules[i][2], reason=rules[i][3],
                      pairs_in_contact=len(h["pairs"]), pair_frames=h["frames"],
                      examples=sorted(h["pairs"])[:12], worst_mm=_r(h.get("worst", 0.0)) if rules[i][2] else None)
                 for i, h in sorted(allowed_hits.items())],
        seconds=round(time.time() - t0, 1),
        peak_rss_mb=int(_rss_mb()), memory=f"streamed: BVHs dropped every {CHUNK} recorded frames and past {SOFT_MB} MB",
    )
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"scene_audit_{chapter}.json"
    path.write_text(json.dumps(out, indent=1, default=_js) + "\n")
    if stills:
        out["stills"] = make_stills(chapter, viol, stills)
        path.write_text(json.dumps(out, indent=1, default=_js) + "\n")
    import shutil
    shutil.rmtree(snapdir, ignore_errors=True)
    print(f"{chapter}: {checked} frames checked, {len(rows)} violating pairs (worst {out['worst_mm']} mm), "
          f"{len(rigid)} rigid, {n_fcl} narrow checks, {out['seconds']} s -> {path}", flush=True)
    for r in rows[:25]:
        print(f"   {r['worst_mm']!s:>7} mm  {r['a']}  x  {r['b']}  frames {r['frames']} (worst {r['worst_frame']}) "
              f"{r['frame_ranges'][:4]}", flush=True)
    return out


def asm_labels():
    """The assembly chapters' objects are actors "o<i>": their names and kinds from the run's asm_scene.pkl (ASM_TRAJ, or the
    newest under ROBOTBUILD/traj), for the report only."""
    import glob
    path = os.environ.get("ASM_TRAJ")
    cands = [Path(path) / "asm_scene.pkl"] if path else [Path(x) for x in glob.glob(str(ROOT / "traj" / "*" / "asm_scene.pkl"))]
    cands = [c for c in cands if c.exists()]
    if not cands:
        return {}
    c = max(cands, key=lambda q: q.stat().st_mtime)
    try:
        objs = pickle.loads(c.read_bytes())["objs"]
    except Exception:                                               # noqa: BLE001
        return {}
    return {f"o{i}": f"{o.get('kind', '')}: {str(o.get('name', ''))[:70]}" for i, o in objs.items()}


def _rss_mb():
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024


def _js(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, set):
        return sorted(o)
    if isinstance(o, tuple):
        return list(o)
    return str(o)


def _r(x):
    return None if x is None else (round(float(x), 1) if x < DEEP else ">100")


def _recorded_every(ns):
    if len(ns) < 2:
        return 1
    d = np.diff(sorted(set(ns)))
    return int(np.median(d)) if len(d) else 1


def _rigid(hist, a, b):
    ha, hb = hist.get(a, []), hist.get(b, [])
    if _keys_change(ha) or _keys_change(hb):
        return False
    ns = sorted({x[0] for x in ha} | {x[0] for x in hb})
    rel0 = None
    ia = ib = 0
    Ma = Mb = None
    for n in ns:
        while ia < len(ha) and ha[ia][0] <= n:
            if ha[ia][2] is not None:
                Ma = ha[ia][2]
            ia += 1
        while ib < len(hb) and hb[ib][0] <= n:
            if hb[ib][2] is not None:
                Mb = hb[ib][2]
            ib += 1
        if Ma is None or Mb is None:
            continue
        rel = np.linalg.inv(Ma.astype(float)) @ Mb.astype(float)
        if rel0 is None:
            rel0 = rel
        elif not (np.allclose(rel[:3, :3], rel0[:3, :3], atol=1e-4) and np.allclose(rel[:3, 3], rel0[:3, 3], atol=0.05)):
            return False
    return True


# ================================================================================================ stills
def make_stills(chapter, viol, k):
    """The worst k pairs: the frame as drawn (if its PNG is still there) beside a close-up of the two recorded meshes (the
    moving one red, the other blue, both half see-through), aimed at the overlap of their bounding boxes. The close-up is
    rendered in a child process (VTK can abort on a software display); without it the still is the frame alone."""
    import subprocess
    import tempfile
    from PIL import Image, ImageDraw
    paths = []
    worst = sorted(viol.items(), key=lambda kv: -kv[1]["worst"])[:k]
    tmp = Path(tempfile.mkdtemp(prefix="audit_stills_"))
    for idx, ((a, b), v) in enumerate(worst):
        snap = v.get("snap")
        if snap is None or not Path(snap).exists():
            continue
        ga, Ma, gb, Mb = pickle.loads(Path(snap).read_bytes())
        right = None
        try:
            pk, png_r = tmp / f"{idx}.pkl", tmp / f"{idx}.png"
            pk.write_bytes(pickle.dumps(dict(A=(ga[0], ga[1], Ma), B=(gb[0], gb[1], Mb))))
            r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "still", str(pk), str(png_r)],
                               capture_output=True, text=True, timeout=180)
            if r.returncode == 0 and png_r.exists():
                right = Image.open(png_r).convert("RGB")
        except Exception as e:                                       # noqa: BLE001
            print(f"  close-up {idx + 1} failed: {e!r}", flush=True)
        png = frame_png(chapter, v["frame"])
        left = Image.open(png).convert("RGB").resize((960, 540)) if png is not None else None
        if left is None and right is None:
            continue
        canvas = Image.new("RGB", (960 + (640 if right is not None else 0) if left is not None else 640, 600), "white")
        x0 = 0
        if left is not None:
            canvas.paste(left, (0, 60))
            x0 = 960
        if right is not None:
            canvas.paste(right.resize((640, 540)), (x0, 60))
        d = ImageDraw.Draw(canvas)
        dep = f"{v['worst']:.1f} mm" if v["worst"] < DEEP else "over 100 mm"
        d.text((10, 6), f"{chapter}, frame {v['frame']}: {dep} deep (limit {v['lim']} mm)", fill="black")
        d.text((10, 24), f"{a}", fill="#d1495b")
        d.text((10, 40), f"{b}", fill="#2a7fff")
        p = OUT / f"scene_audit_{chapter}_{idx + 1}.png"
        canvas.save(p, optimize=True)
        paths.append(str(p.relative_to(REPO)) if p.is_relative_to(REPO) else str(p))
    return paths


def render_still(pk, out):
    import pyvista as pv
    d = pickle.loads(Path(pk).read_bytes())
    pl = pv.Plotter(off_screen=True, window_size=(640, 540), lighting="three lights")
    pl.set_background("#f4f6f8")
    meshes = []
    for (V, F, M), col in ((d["A"], "#d1495b"), (d["B"], "#2a7fff")):
        P = np.asarray(V, float) @ np.asarray(M, float)[:3, :3].T + np.asarray(M, float)[:3, 3]
        m = pv.PolyData(P, np.c_[np.full(len(F), 3), np.asarray(F, np.int64)].ravel())
        meshes.append(m)
        pl.add_mesh(m, color=col, opacity=0.55)
    lo = np.maximum(meshes[0].bounds[::2], meshes[1].bounds[::2])
    hi = np.minimum(meshes[0].bounds[1::2], meshes[1].bounds[1::2])
    c = 0.5 * (lo + hi)
    size = min(float(max(np.max(np.abs(hi - lo)), 60.0)), 1500.0)
    pos = c + np.array([1.6, -2.2, 1.4]) * size
    pl.camera_position = [tuple(pos), tuple(c), (0, 0, 1)]
    img = pl.screenshot(return_img=True)
    pl.close()
    from PIL import Image
    Image.fromarray(np.asarray(img)[:, :, :3]).save(out)


# ================================================================================================ names, watch
def names(chapter):
    dirs = audit_dirs(chapter)
    hist, ns = histories(dirs)
    mv = movers_of(hist)
    groups = {}
    for n in sorted(hist):
        pre = n.split("/")[0] if "/" in n else n
        groups.setdefault(pre, []).append(n)
    print(f"{chapter}: {len(ns)} recorded frames, {len(hist)} actors, {len(mv)} move")
    for pre, lst in sorted(groups.items()):
        m = [x for x in lst if x in mv]
        print(f"  {pre}: {len(lst)} actors, {len(m)} moving; e.g. {lst[:4]}" + (f"; moving e.g. {m[:4]}" if m else ""))


def keep(folder):
    """Hard-link a finished slice's audit folder (and its frames) under KEEP, so merge_parts.py can't take them away."""
    import shutil
    import subprocess
    dst = KEEP / folder.name
    if dst.exists():
        return dst
    KEEP.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["cp", "-al", str(folder), str(dst)], capture_output=True, text=True)
    if r.returncode:
        print(f"keep {folder}: {r.stderr.strip()}", flush=True)
        shutil.rmtree(dst, ignore_errors=True)
        return None
    return dst


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    if len(sys.argv) > 1 and sys.argv[1] == "still":
        render_still(sys.argv[2], sys.argv[3])
        sys.exit(0)
    ap.add_argument("cmd", choices=["run", "names", "keep"])
    ap.add_argument("chapter")
    ap.add_argument("--every", type=int, default=1, help="check every k-th recorded frame (all are replayed)")
    ap.add_argument("--stills", type=int, default=0)
    ap.add_argument("--max_frames", type=int, default=0)
    ap.add_argument("--only", default=None, help="only movers whose name matches this regex (debugging)")
    a = ap.parse_args()
    if a.cmd == "names":
        names(a.chapter)
    elif a.cmd == "keep":
        print(keep(FRAMES / a.chapter))
    else:
        run(a.chapter, every=a.every, stills=a.stills, max_frames=a.max_frames or None, only=a.only)
