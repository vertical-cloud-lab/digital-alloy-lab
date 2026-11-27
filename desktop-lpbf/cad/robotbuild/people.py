"""People for the robot-built desktop LPBF video (issue #260, PR #266, round 7; the feet locked in round 9): a skinned
human, dressed for a machine shop.

Vendored from byu-vcl PR 318 (vertical-cloud-lab/byu-vcl, branch claude/issue-303-20261103-1736, commit 9740ba8,
``vertical-lab/people.py``, round 11 of #303), which is the lab's own code. Changed here, and nothing else:

* the clothes are for a machine shop, not a wet lab, in the colours of the PR branch's other MakeHuman figure
  (render_scale.PERSON_COLOURS, from cad/human/build_person.py: a long-sleeved T-shirt, jeans, trainers), so the people
  in the two videos look alike: the old coat's trunk and sleeves are the T-shirt (sleeves to 55 mm above the wrist, or
  rolled with ``SLEEVE``; no collar unless ``collar=True``), its skirt cut short to a T-shirt's hem at the hip, bare
  hands by default (no gloves near a spindle; ``gloves=`` gives a colour for leather work gloves when handling stock or
  a hoist), and the same wrap-around safety glasses (ANSI Z87.1 style);
* the MakeHuman files and the derived model are cached in ``$ROBOTBUILD/cache/makehuman`` (``/tmp/robotbuild/...``),
  never in the repo;
* the scene it draws into is ``pvscene.PVScene`` (an adapter over ``common.plotter()``), not PR 318's ``scene.Scene``.

PR 318's docstring, as it was (the clothes it describes are now the shop clothes above):

Sterling on round 10's figure (capsule limbs on a box of a coat, an egg of a head): "Yikes.. That's kind of a cringy
looking human, although I don't totally dislike the idea of showing an actual person with movement." This one is
MakeHuman's base mesh (hm08: one smooth body of 13,380 vertices with a face, ears and five fingers a hand) on MakeHuman's
default skeleton and its skin weights, posed every frame by linear-blend skinning in numpy:

* a walk cycle (hips, knees, ankles; the arms swing against the legs), the shoes grounded every frame (their lowest
  point GROUND over the floor, so the hips bob as the legs spread);
* a lean, 60 % at the hips and 40 % along the lower spine;
* both arms solved to hand targets (two-bone IK from the posed shoulder, elbows out and down), the forearm turned to
  the hand's work or to a given palm direction, the fingers together and curled (more when holding);
* the head turned to what the person looks at.

It is dressed by region, the regions cut along smooth lines with the skin weights carried onto the cuts: a lab coat
over the torso and arms to the wrists (pushed out 12 mm, smoothed, and hung: its front and back bridged over hollows
top to bottom and side to side, so it doesn't follow the waist, the seat or the spine), its skirt to mid-thigh
(MakeHuman's skirt helper, tied more to the pelvis than to each thigh), a collar with lapels, a scrub top with its own
V-neck, trousers that hang straight from the knee, shoes, blue nitrile gloves 55 mm up the forearm, skin on the face and
neck, short hair thinning to its line, brows, eyes, and wrap-around safety glasses. 1.75 m in shoes.

Sources, fetched at run time into ``.cache/makehuman/`` and never committed, pinned to one commit of
https://github.com/makehumancommunity/makehuman (CC0 1.0: section C of its LICENSE.md, "The license for the bundled
assets", which covers the base mesh and the rigs), each file's sha256 checked:

* ``makehuman/data/3dobjs/base.obj``: the base mesh. Its ``body``, ``helper-skirt`` and the two eye groups are used;
  the other helpers (tights, hair, teeth, tongue, eyelashes, genitals) and the ``joint-*`` marker groups are dropped.
* ``makehuman/data/rigs/default.mhskel``: the default skeleton (163 bones; each joint is the mean of a joint group's
  vertices). The face's bones are folded into ``head``, the toes into ``foot``, the breasts into the chest: 74 bones
  are posed.
* ``makehuman/data/rigs/default_weights.mhw``: its skin weights.

API as round 10's ``upkeep_clip.Person``: ``set(x, y, hd, lean, phase, amp, hands, look=None, grip=None, palm=None)``,
``hold``, ``let_go``, ``held``, ``rest_hand``, ``names``, ``show``; and ``hand_point`` (a palm's centre, world) and
``posed`` (each part's world points and faces, for collision checks).

Round 9 (2026-11-27; Sterling: "moonwalk"; round 8's audit: the phase-driven gait slid the planted foot 0.34-1.0 m per
metre walked): **the feet are locked.** ``set()`` keeps its arguments, but the legs no longer play a walk cycle from
``phase`` and ``amp`` (both are now accepted and ignored). Each Person has a ``Gait`` (below): a planted foot stays on its
footprint in the world, a foot that has to move steps there on a raised arc, and each leg is solved to its foot by
two-bone IK (hip, knee over the toes, ankle; the foot flat on its heading; the pelvis drops as far as both legs need).
Walking, turning on the spot, side-steps, backing up and shuffles come out of the body's path by themselves, and
standing still is both feet planted. New in the API:

* ``place(x, y, hd, **set_kw)``: both feet planted under the body, no steps (a cut). A move of more than 250 mm or 45 deg
  in one frame, or of more than 10 mm within one frame, is taken as a cut too.
* ``set(..., frame=k)``: the frame number, for tests; by default it is the open common.Chapter's (``common.CURRENT.n``),
  so a renderer need not pass it. pvscene.PVScene.render() runs ``Person._tick`` first, so a foot in the air lands and a
  last settling step is taken while the caller holds the body still without calling set().
* ``set(..., elbow={"l": world direction})``: where the elbow points (default: out and down); ``bend={"l": True}``
  turns the wrist (up to 45 deg) so the palm faces exactly ``palm``, the fingers flat along the face it rests on and the
  thumb back.
* ``walking`` (a foot in the air or the body moving), ``gait.steps``, ``gait.overreach_frames`` (frames a stance leg
  couldn't reach its footprint: the body outran the steps; should be 0), ``drop`` (the pelvis' drop this frame, mm).
* ``carry(lo, hi, M, ends=("-x", "+x"))``: two people carrying a box-shaped load by its ends: each one's stance, hands,
  palms, elbows and lean, so the hands hold the load's sides (or underside) and the dressed body stays >= 30 mm off it;
  ``carry_check(person, lo, hi, M)`` measures a drawn pose against the box. ``body_front(zlo, zhi, lean)``: how far in
  front of its origin the dressed body reaches at those heights.
* walk.py ``--selftest``: a straight walk, turns, side-steps and backing up, and a two-person carry, measured by walk.py's
  own stance-foot slip and gliding checks (round 9: 0.0 mm and 0 frames).

How each caller switches (grep of 2026-11-27):

* **Anything that moves a person** (shop_chapters.Crew.step / walk_to / step_back, ch_integration.Mover): set x, y, hd every
  frame along a path a person can walk (up to ~1.3 m/s and ~12 deg a frame turning on the spot; ease in and out); the
  feet follow. Stop advancing ``phase``/``amp`` (ignored now) and drop Crew.step's second ``set(hands=fix)`` (round 9's
  pelvis drop is decided before the arm IK, so the hands land on their targets; it is harmless if left). A person who
  must be somewhere else across a cut: ``place()``. Don't walk a person in a time-lapse: cut.
* **Two-person lifts** (shop_chapters.team_lift: stance_xy and end_hands): per frame, ``st = people.carry(lo, hi,
  M_world, ends=...)`` with the load's own box (lo, hi) and world pose; then for each person ``p.set(**{k: s[k] for k in
  ("x", "y", "hd", "lean", "hands", "palm", "elbow", "bend", "grip", "look")})``. The stance is rigid in the load's frame,
  so moving the load walks the people with it (one forwards, one backwards, or both sideways). Walk them to their
  stances first (set x, y, hd towards ``st[i]``), and ease the hands from ``rest_hand`` to ``st[i]["hands"]``.
  ``reach_mm`` > 0 means the load rides too low or too far to hold at arm's length: raise it (the side grip holds a block
  whose middle is about 1.0 m up). ``carry_check`` per frame gives the body's clearance and the hands' depth.
* **People who only stand** (ch_intro, ch_parts and hall.py's person; asm_render's operator; shop_chapters' person at the
  bench, the saw, the welder): nothing to change. A ``set()`` that moves them between shots is a placement (both feet
  planted at once); ``place()`` says so explicitly.

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/people.py
                                         # close-up stills of the poses -> /tmp/robotbuild/people_*.png
"""
from __future__ import annotations

import functools
import hashlib
import json
import math
import os
import pickle
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pyvista as pv

HERE = Path(__file__).resolve().parent
CACHE = Path(os.environ.get("ROBOTBUILD", "/tmp/robotbuild")) / "cache" / "makehuman"
MH_SHA = "a8bc2d54ff0ac92e78ff71431b1023eda42bf482"      # makehumancommunity/makehuman, master, 2024-06-26
MH_URL = f"https://raw.githubusercontent.com/makehumancommunity/makehuman/{MH_SHA}/makehuman/data/{{path}}"
FILES = {
    "base.obj": ("3dobjs/base.obj", "8e761e6624b8f54536409135d1636da63b32486a90d4897f84e121d144f6fb4c"),
    "default.mhskel": ("rigs/default.mhskel", "99f179bce0aa850b45d4191a1d0d234c5851f881c057439470ded3bddf729a24"),
    "default_weights.mhw": ("rigs/default_weights.mhw",
                            "0f3641d651ae3d00ad6b4ccee43142edb109d3bd909d27d9e4139ef1beed8625"),
}
MODEL_V = 108                        # bump when the derived model changes (the cached pickle's name); 107: shop clothes;
                                     # 108: shoes as each foot's convex hull (107's showed the toes)

HEIGHT = 1735.0                     # the body, sole to crown, mm; the shoes add ~10 mm and the hair ~5: 1.75 m
GROUND = 2.0                        # the lowest point of the shoes, mm over the floor (the floor's tape is 1.5 mm)
SOLE = 10.0                         # the shoes' sole under the foot
def _rgb(h):
    return tuple(int(h[k:k + 2], 16) / 255 for k in (1, 3, 5))


# Colours as render_scale.PERSON_COLOURS (cad/human/build_person.py's MakeHuman figure on the PR branch, 2026-11-25:
# a long-sleeved T-shirt, jeans and trainers), so the people in the two videos look alike.
SKIN = _rgb("#c49a7e")
COAT = _rgb("#4d6d91")               # the long-sleeved T-shirt (the lab coat's region)
SHIRT = COAT                         # the coat's V: the same T-shirt (a V-neck)
TROUSERS = _rgb("#39465a")           # jeans
SHOES = _rgb("#2f3237")              # trainers
GLOVE = (0.71, 0.56, 0.36)           # tan leather work gloves, when asked for (Person(gloves=True)); none by default
SLEEVE = None                        # None: sleeves to the wrist; a number (mm): rolled to that far below the elbow
TAIL = 80.0                          # the shirt's tail hangs out to this far under the hip joints, mm
HAIR = _rgb("#3b2c22")
BROW = _rgb("#33261d")
IRIS = _rgb("#3a2a20")
SCLERA = _rgb("#dcd8d2")
LENS = (0.80, 0.88, 0.93)
FRAME = (0.16, 0.18, 0.22)

# offsets along the posed normals, mm: the coat and its skirt stand off the body; the trousers are loose
OFFSET = dict(coat=8.0, skirt=10.0, collar=8.0, trousers=7.0, shoes=9.0, glove=1.2, hair=6.0, shirt=1.5, brow=0.8)

FACE_BONES = ("levator", "oris", "risorius", "oculi", "orbicularis", "temporalis", "tongue", "special", "jaw", "eye")


# ================================================================================================ the assets
def _fetch(key: str) -> Path:
    path, sha = FILES[key]
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / key
    if not out.exists():
        req = urllib.request.Request(MH_URL.format(path=path), headers={"User-Agent": "Mozilla/5.0"})
        tmp = out.with_suffix(out.suffix + ".part")
        tmp.write_bytes(urllib.request.urlopen(req, timeout=300).read())
        tmp.replace(out)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    if digest != sha:
        raise RuntimeError(f"{out}: sha256 {digest}, expected {sha} (MakeHuman {MH_SHA[:7]})")
    return out


def _merged(bone: str) -> str:
    """The posed bone a MakeHuman bone's weights go to: the face's bones to the head, toes to the foot, the breasts
    to the chest."""
    if bone.startswith(FACE_BONES):
        return "head"
    if bone.startswith("toe"):
        return "foot" + bone[-2:]
    if bone.startswith("breast"):
        return "spine02"
    return bone


def _to_ours(p: np.ndarray, k: float, y0: float) -> np.ndarray:
    """MakeHuman (x to the figure's left, y up, z forward, decimetres) to ours (x to its right, y forward, z up, mm,
    the soles at z = SOLE). A rotation, no mirror."""
    p = np.asarray(p, float)
    return np.stack([-p[..., 0] * k, p[..., 2] * k, (p[..., 1] - y0) * k + SOLE], axis=-1)


def _build_model() -> dict:
    obj, skel, wts = (_fetch(k) for k in FILES)
    verts, groups, cur = [], {}, None
    for line in obj.read_text().splitlines():
        if line.startswith("v "):
            verts.append([float(t) for t in line.split()[1:4]])
        elif line.startswith("g "):
            cur = line.split()[1]
        elif line.startswith("f "):
            groups.setdefault(cur, []).append([int(t.split("/")[0]) - 1 for t in line.split()[1:]])
    Vmh = np.array(verts)
    keep = ("body", "helper-skirt", "helper-l-eye", "helper-r-eye")
    quads = {g: np.array(groups[g], int) for g in keep}
    body_v = np.unique(quads["body"])
    y0, y1 = Vmh[body_v, 1].min(), Vmh[body_v, 1].max()
    k = HEIGHT / (y1 - y0)
    sk = json.loads(skel.read_text())
    J = {name: _to_ours(Vmh[idx].mean(0), k, y0) for name, idx in sk["joints"].items()}
    # the posed bones, parents before children
    bones = {}
    for b, d in sk["bones"].items():
        if _merged(b) != b:
            continue
        bones[b] = dict(parent=d["parent"], head=J[d["head"]], tail=J[d["tail"]])
    order, done = [], set()
    while len(order) < len(bones):
        for b, d in bones.items():
            if b not in done and (d["parent"] is None or d["parent"] in done):
                order.append(b)
                done.add(b)
    # the used vertices, re-indexed
    used = np.unique(np.concatenate([q.ravel() for q in quads.values()]))
    remap = -np.ones(len(Vmh), int)
    remap[used] = np.arange(len(used))
    V = _to_ours(Vmh[used], k, y0)
    tris = {}
    for g, q in quads.items():
        q = remap[q]
        tris[g] = np.r_[q[:, [0, 1, 2]], q[:, [0, 2, 3]]]
    # skin weights onto the posed bones, normalised per vertex
    bidx = {b: i for i, b in enumerate(order)}
    acc = {}
    for b, lst in json.loads(wts.read_text())["weights"].items():
        j = bidx[_merged(b)]
        for vi, w in lst:
            r = remap[vi]
            if r >= 0:
                acc[(r, j)] = acc.get((r, j), 0.0) + w
    rows = np.array([r for r, _ in acc], int)
    cols = np.array([c for _, c in acc], int)
    vals = np.array(list(acc.values()), float)
    tot = np.bincount(rows, weights=vals, minlength=len(V))
    vals = vals / tot[rows]
    dom = np.zeros(len(V), int)                      # each vertex's heaviest bone
    best = np.zeros(len(V))
    for r, c, w in zip(rows, cols, vals):
        if w > best[r]:
            best[r], dom[r] = w, c
    eyes = {s: V[np.unique(remap[quads[f"helper-{s}-eye"]])].mean(0) for s in ("l", "r")}
    return dict(V=V, tris=tris, order=order, parent=[bidx.get(bones[b]["parent"], -1) for b in order],
                head=np.array([bones[b]["head"] for b in order]), tail=np.array([bones[b]["tail"] for b in order]),
                rows=rows, cols=cols, vals=vals, dom=dom, eyes=eyes, scale=k, y0=y0)


@functools.lru_cache(maxsize=None)
def model() -> dict:
    # keyed on the code that builds the model (from _fetch to the Person class), not the whole file: round 9's walker and
    # posing code change without rebuilding the derived model (about a minute) in every worker's process
    src = Path(__file__).read_text()
    a, b = src.find("def _fetch("), src.find("\nclass Person")
    key = hashlib.sha256((src[a:b] + MH_SHA).encode()).hexdigest()[:12]
    path = CACHE / f"model_v{MODEL_V}_{key}.pkl"
    if path.exists():
        try:
            return pickle.loads(path.read_bytes())
        except Exception:                               # noqa: BLE001
            pass
    m = _build_model()
    m.update(_dress(m))
    CACHE.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".part")
    tmp.write_bytes(pickle.dumps(m))
    tmp.replace(path)
    return m


# ================================================================================================ the clothes
TROUSER_BONES = ("root", "pelvis", "upperleg", "lowerleg", "foot")
TRUNK_BONES = ("spine", "clavicle")


def _poly(P, F, W=None) -> pv.PolyData:
    m = pv.PolyData(np.asarray(P, float), np.c_[np.full(len(F), 3), np.asarray(F, int)].ravel())
    if W is not None:
        m.point_data["W"] = np.asarray(W, np.float32)
    return m


def _faces(m: pv.PolyData) -> np.ndarray:
    m = m.triangulate()
    f = np.asarray(m.faces).reshape(-1, 4)
    return f[:, 1:].astype(int)


def _split(m: pv.PolyData, field: np.ndarray) -> tuple[pv.PolyData, pv.PolyData]:
    """(where field > 0, the rest), cut along field = 0 (the weights are interpolated onto the cut)."""
    m = m.copy()
    m.point_data["_f"] = np.asarray(field, float)
    m.set_active_scalars("_f")
    pos = m.clip_scalar(scalars="_f", value=0.0, invert=False)
    neg = m.clip_scalar(scalars="_f", value=0.0, invert=True)
    out = []
    for x in (pos, neg):
        x = pv.PolyData(x.extract_surface(algorithm=None)) if not isinstance(x, pv.PolyData) else x
        x = x.triangulate().clean(tolerance=1e-6)
        for k in list(x.point_data.keys()):
            if k != "W":
                del x.point_data[k]
        out.append(x)
    return out[0], out[1]


def _drape(P: np.ndarray, mask: np.ndarray, axis, z_top: float, nbins: int = 60) -> np.ndarray:
    """A coat hangs: below z_top its radius about the body's vertical axis never comes back in (it can't tuck into
    the waist), at the front and back; at the sides, where the arms hang, it follows the body."""
    idx = np.where(mask & (P[:, 2] <= z_top))[0]
    if not len(idx):
        return P
    d = P[idx, :2] - axis
    r = np.hypot(d[:, 0], d[:, 1])
    phi = np.arctan2(d[:, 1], d[:, 0])
    b = ((phi + np.pi) / (2 * np.pi) * nbins).astype(int) % nbins
    newr = r.copy()
    for k in range(nbins):
        s = np.where((b == k) | (b == (k - 1) % nbins) | (b == (k + 1) % nbins))[0]
        own = b[s] == k
        if not own.any():
            continue
        o = s[np.argsort(-P[idx[s], 2])]
        run = np.maximum.accumulate(r[o])
        sel = b[o] == k
        newr[o[sel]] = run[sel]
    w = np.clip((np.abs(np.sin(phi)) - 0.40) / 0.35, 0.0, 1.0)
    newr = r + w * (newr - r)
    out = P.copy()
    out[idx, :2] = axis + d * (newr / np.maximum(r, 1e-9))[:, None]
    return out


def _offset(m: pv.PolyData, mm: float, smooth: int = 0) -> pv.PolyData:
    m = m.copy()
    if smooth:
        W = m.point_data["W"].copy()
        m = m.smooth_taubin(n_iter=smooth, pass_band=0.08, boundary_smoothing=False, feature_smoothing=False)
        m.point_data["W"] = W
    if mm:
        F = _faces(m)
        N = _normals(np.asarray(m.points, float), F, m.n_points)
        m.points = np.asarray(m.points, float) + mm * N
    return m


def _shoe_hulls(shoes: pv.PolyData) -> pv.PolyData:
    """Each shoe as the convex hull of its foot (2026-11-25): offsetting the foot itself, as 107 did, left the toes showing
    through like a sock. The hull's corners are the foot's own vertices, so they keep their skin weights."""
    from scipy.spatial import ConvexHull
    P = np.asarray(shoes.points, float)
    W = np.asarray(shoes.point_data["W"], np.float32)
    Ps, Fs, Ws, base = [], [], [], 0
    for sgn in (1.0, -1.0):
        idx = np.where(P[:, 0] * sgn > 0.0)[0]
        if len(idx) < 8:
            continue
        h = ConvexHull(P[idx])
        used = np.unique(h.simplices)
        remap = -np.ones(len(idx), int)
        remap[used] = np.arange(len(used))
        F = remap[h.simplices]
        Q = P[idx[used]]
        c = Q.mean(0)
        n = np.cross(Q[F[:, 1]] - Q[F[:, 0]], Q[F[:, 2]] - Q[F[:, 0]])
        flip = np.einsum("ij,ij->i", n, Q[F].mean(1) - c) < 0.0       # every face outward
        F[flip] = F[flip][:, ::-1]
        Ps.append(Q)
        Ws.append(W[idx[used]])
        Fs.append(F + base)
        base += len(used)
    return _poly(np.vstack(Ps), np.vstack(Fs), np.vstack(Ws))


def _bridge(P: np.ndarray, mask: np.ndarray, sign: float, dz: float = 14.0) -> np.ndarray:
    """Cloth stretched across a hollow: in each height slice, the masked points' profile y(x) (sign +1: the front,
    -1: the back) is raised to its convex hull, so a coat spans the chest and the back instead of following them."""
    out = P.copy()
    idx = np.where(mask)[0]
    if len(idx) < 3:
        return out
    z = P[idx, 2]
    for z0 in np.arange(z.min(), z.max() + dz, dz):
        win = idx[(z >= z0 - 1.5 * dz) & (z < z0 + 1.5 * dz)]
        mine = idx[(z >= z0 - dz / 2) & (z < z0 + dz / 2)]
        if len(win) < 3 or not len(mine):
            continue
        o = np.argsort(P[win, 0])
        pts = np.c_[P[win, 0][o], sign * P[win, 1][o]]
        hull = []
        for q in pts:
            while len(hull) >= 2 and ((hull[-1][0] - hull[-2][0]) * (q[1] - hull[-2][1]) -
                                      (hull[-1][1] - hull[-2][1]) * (q[0] - hull[-2][0])) >= 0:
                hull.pop()
            hull.append(q)
        hx, hy = np.array(hull).T
        if len(hx) < 2:
            continue
        yh = np.interp(P[mine, 0], hx, hy)
        out[mine, 1] = sign * np.maximum(sign * P[mine, 1], yh)
    return out


def _vbridge(P: np.ndarray, mask: np.ndarray, axis, nbins: int = 48) -> np.ndarray:
    """Cloth hangs over hollows top to bottom too: at the front and the back, each angular sector's profile r(z) about
    the body's vertical axis is raised to its convex hull, so the coat runs straight from the shoulder blades to the
    seat (and from the chest down) instead of following the small of the back."""
    idx = np.where(mask)[0]
    if len(idx) < 3:
        return P
    d = P[idx, :2] - axis
    r = np.hypot(d[:, 0], d[:, 1])
    phi = np.arctan2(d[:, 1], d[:, 0])
    b = ((phi + np.pi) / (2 * np.pi) * nbins).astype(int) % nbins
    z = P[idx, 2]
    newr = r.copy()
    for k in range(nbins):
        s = np.where((b == k) | (b == (k - 1) % nbins) | (b == (k + 1) % nbins))[0]
        mine = np.where(b == k)[0]
        if len(s) < 3 or not len(mine):
            continue
        o = s[np.argsort(z[s])]
        hull = []
        for q in zip(z[o], r[o]):
            while len(hull) >= 2 and ((hull[-1][0] - hull[-2][0]) * (q[1] - hull[-2][1]) -
                                      (hull[-1][1] - hull[-2][1]) * (q[0] - hull[-2][0])) >= 0:
                hull.pop()
            hull.append(q)
        hz, hr = np.array(hull).T
        if len(hz) < 2:
            continue
        newr[mine] = np.maximum(r[mine], np.interp(z[mine], hz, hr))
    w = np.clip((np.abs(np.sin(phi)) - 0.40) / 0.35, 0.0, 1.0)
    newr = r + w * (newr - r)
    out = P.copy()
    out[idx, :2] = axis + d * (newr / np.maximum(r, 1e-9))[:, None]
    return out


def _leg_drape(P: np.ndarray, mask: np.ndarray, knee: np.ndarray, ankle: np.ndarray, nbins: int = 40) -> np.ndarray:
    """A trouser leg hangs straight from the knee: about the shin's axis, its radius never comes back in going
    down."""
    e3 = _unit(knee - ankle)
    e1 = _unit(np.cross(e3, (0.0, 1.0, 0.0)))
    e2 = np.cross(e3, e1)
    idx = np.where(mask)[0]
    if not len(idx):
        return P
    d = P[idx] - ankle
    h = d @ e3
    q = np.c_[d @ e1, d @ e2]
    r = np.hypot(q[:, 0], q[:, 1])
    phi = np.arctan2(q[:, 1], q[:, 0])
    b = ((phi + np.pi) / (2 * np.pi) * nbins).astype(int) % nbins
    top = float((knee - ankle) @ e3)
    newr = r.copy()
    for k in range(nbins):
        s = np.where(((b == k) | (b == (k - 1) % nbins) | (b == (k + 1) % nbins)) & (h <= top))[0]
        if not len(s):
            continue
        o = s[np.argsort(-h[s])]
        run = np.maximum.accumulate(r[o])
        sel = b[o] == k
        newr[o[sel]] = run[sel]
    out = P.copy()
    scale = newr / np.maximum(r, 1e-9)
    out[idx] = ankle + np.outer(h, e3) + (q[:, :1] * scale[:, None]) * e1 + (q[:, 1:] * scale[:, None]) * e2
    return out


def _dress(m: dict) -> dict:
    """The parts drawn in one colour each, in the rest pose: {part: dict(P, F, rows, cols, vals)}; region edges are
    cut along smooth lines (the weights interpolated onto them), the garments smoothed, draped and pushed out."""
    V, order = m["V"], m["order"]
    nb = len(order)
    Wd = np.zeros((len(V), nb), np.float32)
    Wd[m["rows"], m["cols"]] = m["vals"]
    H = lambda b: m["head"][order.index(b)]          # noqa: E731
    bones = np.array(order)

    def dom(W):
        return bones[np.asarray(W).argmax(1)]

    tb = m["tris"]["body"]
    bv, inv = np.unique(tb, return_inverse=True)
    body = _poly(V[bv], inv.reshape(-1, 3), Wd[bv])
    P = V[bv]
    db = dom(Wd[bv])
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    n0 = H("neck01")
    # 1. the head and neck above the collar line (lower at the front, rising over the shoulders)
    zc = n0[2] - 34.0 + 0.50 * (n0[1] - y) + 1.7 * np.maximum(np.abs(x) - 50.0, 0.0)
    # the shirt (a scrub top) has its own V-neck: the skin shows in a narrow V under the neck, down to z_vs
    z_vs = n0[2] - 105.0
    f_vs = np.minimum(0.62 * (z - z_vs) - np.abs(x), y - (n0[1] + 15.0))
    headneck = np.isin(db, ["head", "neck01", "neck02", "neck03", "spine01", "spine02", "clavicle.L", "clavicle.R"])
    upper, lower = _split(body, np.where(headneck, np.maximum(z - zc, f_vs), -200.0))
    # hair: the scalp above a line from the forehead's hairline down to the nape, not over the ears
    eye = (m["eyes"]["l"] + m["eyes"]["r"]) / 2
    Pu = np.asarray(upper.points)
    zr, yr, ax_ = Pu[:, 2] - eye[2], Pu[:, 1] - eye[1], np.abs(Pu[:, 0])
    f_hair = zr - (48.0 - 0.55 * np.clip(-yr - 25.0, -40.0, 220.0) + 0.20 * np.maximum(yr, 0.0))
    f_ear = np.maximum.reduce([58.0 - ax_, zr - 40.0, -100.0 - yr, (-yr - 150.0)])
    hair, skin = _split(upper, np.minimum(f_hair, np.maximum(f_ear, (zr - 40.0) * 3.0)))
    # the hair: thicker over the crown, thinning to nothing at its line (not a cap's hard edge)
    hair = _offset(hair, 0.0, smooth=12)
    Ph = np.asarray(hair.points, float)
    zr_h, yr_h = Ph[:, 2] - eye[2], Ph[:, 1] - eye[1]
    fh = zr_h - (48.0 - 0.55 * np.clip(-yr_h - 25.0, -40.0, 220.0) + 0.20 * np.maximum(yr_h, 0.0))
    Nh = _normals(Ph, _faces(hair), len(Ph))
    hair.points = Ph + (1.5 + 9.0 * np.clip(fh / 45.0, 0.0, 1.0))[:, None] * Nh
    # the brows: two short arcs over the eyes
    Ps = np.asarray(skin.points)
    f_brow = np.full(len(Ps), -50.0)
    for sd in ("l", "r"):
        e = m["eyes"][sd]
        u = (Ps[:, 0] - e[0]) / 25.0
        v = (Ps[:, 2] - (e[2] + 17.0 - 6.0 * u * u)) / 3.6
        f_brow = np.maximum(f_brow, np.where(Ps[:, 1] > e[1] - 12.0, 1.0 - u * u - v * v, -50.0))
    brow, skin = _split(skin, f_brow)
    # 2. the shirt in the coat's V
    Pl = np.asarray(lower.points)
    zv0 = H("spine01")[2] - 60.0
    f_v = np.minimum(0.45 * (Pl[:, 2] - zv0) - np.abs(Pl[:, 0]), Pl[:, 1] - (n0[1] + 25.0))
    shirt, lower = _split(lower, f_v)
    # 3. the gloves, 55 mm up the forearm from the wrist
    Pl = np.asarray(lower.points)
    dl = dom(lower.point_data["W"])
    f_g = np.full(len(Pl), -500.0)
    for sd in ("L", "R"):
        w_, e_ = H(f"wrist.{sd}"), H(f"lowerarm01.{sd}")
        a_ = _unit(w_ - e_)
        arm = np.array([b.endswith(sd) and b.startswith(("upperarm", "lowerarm", "wrist", "metacarpal", "finger"))
                        for b in dl])
        f_g = np.where(arm, (Pl - w_) @ a_ + 55.0, f_g)
    glove, lower = _split(lower, f_g)
    # 3b. with SLEEVE set, the sleeves are rolled to SLEEVE mm below the elbow: the forearm from there to the hand is skin
    Pl = np.asarray(lower.points)
    dl = dom(lower.point_data["W"])
    f_f = np.full(len(Pl), -500.0)
    SL = 0.0 if SLEEVE is None else SLEEVE
    for sd in ("L", "R"):
        e_, w_ = H(f"lowerarm01.{sd}"), H(f"wrist.{sd}")
        a_ = _unit(w_ - e_)
        arm = np.array([b.endswith(sd) and b.startswith(("upperarm", "lowerarm", "wrist", "metacarpal", "finger"))
                        for b in dl])
        f_f = np.where(arm, (Pl - e_) @ a_ - SL, f_f)
    forearm = None
    if SLEEVE is not None:
        forearm, lower = _split(lower, f_f)
    # 4. the shoes, up to the ankle
    Pl = np.asarray(lower.points)
    dl = dom(lower.point_data["W"])
    leg = np.array([b.startswith(("upperleg", "lowerleg", "foot")) for b in dl])
    shoes, lower = _split(lower, np.where(leg, H("foot.L")[2] + 30.0 - Pl[:, 2], -500.0))
    # 5. the coat (trunk and arms) and the trousers (hips and legs): the cut is under the coat's skirt
    dl = dom(lower.point_data["W"])
    coat, trousers = _split(lower, np.where(np.array([b.startswith(TROUSER_BONES) for b in dl]), -1.0, 1.0))
    # the skirt: MakeHuman's skirt helper, cut level at mid-thigh
    ts = m["tris"]["helper-skirt"]
    sv, sinv = np.unique(ts, return_inverse=True)
    skirt = _poly(V[sv], sinv.reshape(-1, 3), Wd[sv])
    hip, knee = H("upperleg01.L")[2], H("lowerleg01.L")[2]
    cut = hip - TAIL                             # the work shirt's tail, out to the hip (the lab coat's was mid-thigh)
    skirt, _ = _split(skirt, np.asarray(skirt.points)[:, 2] - cut)
    # drape the coat's trunk and the skirt together, then smooth and push out
    # the skirt hangs more from the pelvis than it follows each thigh
    Ws = np.asarray(skirt.point_data["W"], float)
    Ws = 0.55 * Ws
    Ws[:, order.index("root")] += 0.45
    skirt.point_data["W"] = Ws.astype(np.float32)
    # the coat's torso ends 10 mm under the skirt's top edge, so the skirt is the outside surface below it (round 11's
    # first try had the torso's lower edge show through the skirt at the small of the back)
    Pk0 = np.asarray(skirt.points, float)
    ek = np.sort(np.r_[_faces(skirt)[:, [0, 1]], _faces(skirt)[:, [1, 2]], _faces(skirt)[:, [2, 0]]], axis=1)
    uk, ck = np.unique(ek, axis=0, return_counts=True)
    bk = np.unique(uk[ck == 1])
    top_edge = Pk0[bk][Pk0[bk][:, 2] > cut + 50.0]
    skirt_top = float(top_edge[:, 2].min()) if len(top_edge) else float(Pk0[:, 2].max())
    dcoat = dom(coat.point_data["W"])
    is_trunk = np.array([b.startswith(TRUNK_BONES) for b in dcoat])
    coat, _ = _split(coat, np.where(is_trunk, np.asarray(coat.points)[:, 2] - (skirt_top - 10.0), 1.0))
    coat = _offset(coat, 0.0, smooth=40)
    Pc, Pk = np.asarray(coat.points, float), np.asarray(skirt.points, float)
    trunk = np.array([b.startswith(TRUNK_BONES) for b in dom(coat.point_data["W"])])
    waist = np.abs(Pc[:, 2] - H("spine03")[2]) < 40.0
    axis = np.array([0.0, float(Pc[trunk & waist, 1].mean()) if (trunk & waist).any() else 0.0])
    chest = trunk & (Pc[:, 2] < H("neck01")[2] - 20.0) & (np.abs(Pc[:, 0]) < 175.0)
    Pc = _bridge(Pc, chest & (Pc[:, 1] > axis[1] + 15.0), 1.0)
    Pc = _bridge(Pc, chest & (Pc[:, 1] < axis[1] - 15.0), -1.0)
    both = np.r_[Pc, Pk]
    hang = np.r_[trunk, np.ones(len(Pk), bool)]
    both = _vbridge(both, hang & (both[:, 2] < H("neck01")[2] - 45.0), axis)
    zt = H("spine01")[2] - 10.0
    dr = _drape(both, hang, axis, zt)
    coat.points, skirt.points = dr[:len(Pc)], dr[len(Pc):]
    Pt = np.asarray(trousers.points, float)
    dt = dom(trousers.point_data["W"])
    for sd in ("L", "R"):
        Pt = _leg_drape(Pt, np.array([x_.startswith("lowerleg") and x_.endswith(sd) for x_ in dt]),
                        H(f"lowerleg01.{sd}") + (0, 0, 40.0), H(f"foot.{sd}"))
    trousers.points = Pt
    parts = dict(
        skin=skin, hair=hair, brow=_offset(brow, OFFSET["brow"]),
        shirt=_offset(shirt, OFFSET["shirt"]), glove=_offset(glove, OFFSET["glove"]),
        shoes=_offset(_shoe_hulls(_offset(shoes, 0.0, smooth=25)), OFFSET["shoes"]), trousers=_offset(trousers, OFFSET["trousers"], smooth=24),
        coat=_offset(coat, OFFSET["coat"], smooth=30), skirt=_offset(skirt, OFFSET["skirt"], smooth=20))
    # eyes: the iris where the eyeball faces forward
    for sd in ("l", "r"):
        te = m["tris"][f"helper-{sd}-eye"]
        ev, einv = np.unique(te, return_inverse=True)
        eyem = _poly(V[ev], einv.reshape(-1, 3), Wd[ev])
        c = V[ev].mean(0)
        dv = np.asarray(eyem.points) - c
        fwd = dv[:, 1] / np.maximum(np.linalg.norm(dv, axis=1), 1e-9)
        iris, sclera = _split(eyem, fwd - 0.80)
        for k_, part in (("iris", iris), ("sclera", sclera)):
            parts[k_] = part if k_ not in parts else parts[k_].merge(part)
    out = {}
    for k_, part in parts.items():
        F = _faces(part)
        W = np.asarray(part.point_data["W"], float)
        r_, c_ = np.nonzero(W > 1e-4)
        v_ = W[r_, c_]
        v_ = v_ / np.bincount(r_, weights=v_, minlength=len(W))[r_]
        out[k_] = dict(P=np.asarray(part.points, float), F=F, rows=r_, cols=c_, vals=v_)
    if forearm is not None:
        F_ = _faces(forearm)
        W_ = np.asarray(forearm.point_data["W"], float)
        r_, c_ = np.nonzero(W_ > 1e-4)
        v_ = W_[r_, c_]
        v_ = v_ / np.bincount(r_, weights=v_, minlength=len(W_))[r_]
        out["forearm"] = dict(P=np.asarray(forearm.points, float), F=F_, rows=r_, cols=c_, vals=v_)
    out["collar"] = _collar(out["coat"], H)
    return dict(parts=out, glasses=_glasses(m), skirt_cut=cut)


def _collar(coat: dict, H) -> dict | None:
    """The coat's collar along its neck opening: standing 30 mm at the back, lying out as lapels along the V."""
    P, F = coat["P"], coat["F"]
    e = np.sort(np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]], axis=1)
    u, c = np.unique(e, axis=0, return_counts=True)
    b = u[c == 1]
    n0 = H("neck01")
    keep = (P[b[:, 0], 2] > H("spine01")[2] - 20.0) & (np.abs(P[b[:, 0], 0]) < 140.0) & \
        (P[b[:, 1], 2] > H("spine01")[2] - 20.0)
    b = b[keep]
    if len(b) < 8:
        return None
    adj = {}
    for i, j in b:
        adj.setdefault(i, []).append(j)
        adj.setdefault(j, []).append(i)
    start = max(adj, key=lambda v: -P[v, 1])                # at the back
    loop, prev, cur = [start], None, start
    while True:
        nxt = [w for w in adj[cur] if w != prev and w not in loop[1:]]
        if not nxt:
            break
        prev, cur = cur, nxt[0]
        if cur == start:
            break
        loop.append(cur)
    if len(loop) < 8:
        return None
    loop = np.array(loop)
    P0 = P[loop]
    for _ in range(3):                                   # smooth the edge along the loop (a moving average)
        P0 = (np.roll(P0, 2, 0) + np.roll(P0, 1, 0) + P0 + np.roll(P0, -1, 0) + np.roll(P0, -2, 0)) / 5.0
    front = np.clip((P0[:, 1] - (n0[1] - 5.0)) / 45.0, 0.0, 1.0)
    out = P0[:, :2] - np.array([0.0, n0[1]])
    out = np.c_[out / np.maximum(np.linalg.norm(out, axis=1), 1e-9)[:, None], np.zeros(len(P0))]
    side = np.c_[np.sign(P0[:, 0]), np.zeros(len(P0)), np.zeros(len(P0))]
    up = np.array([0.0, 0.0, 1.0])
    stand = (1.0 - front)[:, None]
    lap = front[:, None]
    r1 = P0 + stand * (up * 16.0 + out * 4.0) + lap * (side * 12.0 + np.array([0, 4.0, 2.0]))
    r2 = P0 + stand * (up * 30.0 + out * 14.0) + lap * (side * 30.0 + np.array([0, 7.0, -6.0]))
    rings = [P0, r1, r2]
    n = len(loop)
    pts = np.concatenate(rings)
    faces = []
    for r in range(len(rings) - 1):
        for i in range(n):
            a, b2 = r * n + i, r * n + (i + 1) % n
            faces += [(a, b2, b2 + n), (a, b2 + n, a + n)]
    rows, cols, vals = coat["rows"], coat["cols"], coat["vals"]
    o = np.argsort(rows, kind="stable")
    rs, cs, vs = rows[o], cols[o], vals[o]
    s0, s1 = np.searchsorted(rs, loop), np.searchsorted(rs, loop, side="right")
    R_, C_, W_ = [], [], []
    for r in range(len(rings)):
        for i, (a0, a1) in enumerate(zip(s0, s1)):
            R_ += [r * n + i] * (a1 - a0)
            C_ += list(cs[a0:a1])
            W_ += list(vs[a0:a1])
    return dict(P=pts, F=np.array(faces), rows=np.array(R_), cols=np.array(C_), vals=np.array(W_))


def _glasses(m: dict) -> dict:
    """Wrap-around safety glasses on the rest head: {piece: (points, faces)}; they ride on the head bone."""
    el, er = m["eyes"]["l"], m["eyes"]["r"]
    c = (el + er) / 2
    half = abs(el[0] - er[0]) / 2
    cx, cy, cz = c[0], c[1] - 70.0, c[2]                 # the arc's axis, behind the eyes
    rad = (c[1] + 24.0) - cy                             # the lens 24 mm in front of the eyes' centres
    phis = np.radians(np.linspace(-66, 66, 41))
    zs = np.array([-21.0, -14.0, 0.0, 12.0, 17.0])
    pts, faces = [], []
    for z in zs:
        for ph in phis:
            sag = 1.0 - 0.10 * (z / 20.0) ** 2
            pts.append((cx + rad * math.sin(ph), cy + rad * math.cos(ph) * sag, cz + z - 3.0 * math.cos(2 * ph)))
    n = len(phis)
    for i in range(len(zs) - 1):
        for j in range(n - 1):
            a = i * n + j
            faces += [(a, a + 1, a + n + 1), (a, a + n + 1, a + n)]
    lens = (np.array(pts), np.array(faces))
    fr = []
    top = np.array(pts[(len(zs) - 1) * n:(len(zs)) * n])
    for j in range(n - 1):
        a, b = top[j], top[j + 1]
        d = b - a
        fr.append(pv.Cylinder(center=(a + b) / 2, direction=d, radius=3.0, height=float(np.linalg.norm(d)) + 1.5,
                              resolution=10).triangulate())
    for sgn in (-1, 1):
        p0 = np.array([cx + sgn * rad * math.sin(math.radians(66)), cy + rad * math.cos(math.radians(66)), cz + 8.0])
        p1 = np.array([cx + sgn * (half + 46.0), c[1] - 108.0, cz - 2.0])
        d = p1 - p0
        fr.append(pv.Cylinder(center=(p0 + p1) / 2, direction=d, radius=2.6, height=float(np.linalg.norm(d)),
                              resolution=10).triangulate())
    frame = fr[0].merge(fr[1:]).clean()
    ff = np.asarray(frame.faces).reshape(-1, 4)[:, 1:]
    return dict(lens=lens, frame=(np.asarray(frame.points, float), ff))


# ================================================================================================ maths
def _rot(axis, ang: float) -> np.ndarray:
    a = np.asarray(axis, float)
    a = a / max(np.linalg.norm(a), 1e-12)
    x, y, z = a
    c, s = math.cos(ang), math.sin(ang)
    C = 1 - c
    return np.array([[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
                     [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
                     [z * x * C - y * s, z * y * C + x * s, c + z * z * C]])


def _unit(v) -> np.ndarray:
    v = np.asarray(v, float)
    return v / max(np.linalg.norm(v), 1e-12)


def _M(Rm=None, t=None) -> np.ndarray:
    M = np.eye(4)
    if Rm is not None:
        M[:3, :3] = Rm
    if t is not None:
        M[:3, 3] = t
    return M


def _normals(P: np.ndarray, F: np.ndarray, n: int) -> np.ndarray:
    a, b, c = P[F[:, 0]], P[F[:, 1]], P[F[:, 2]]
    fn = np.cross(b - a, c - a)
    out = np.zeros((n, 3))
    for k in range(3):
        for j in range(3):
            out[:, j] += np.bincount(F[:, k], weights=fn[:, j], minlength=n)
    return out / np.maximum(np.linalg.norm(out, axis=1), 1e-12)[:, None]


# ================================================================================================ the person
class Person:
    """A person, 1.75 m, in shop clothes: one skinned body posed every frame (see the module's docstring). Its local
    frame: x to its right, y the way it faces, z up, the origin on the floor between its feet; ``set(x, y, hd)``
    puts that frame in the world (hd in degrees about z, 0 = facing +y)."""

    LEAN_HIPS = 0.6                     # of a lean, the share taken at the hips (the rest along the lower spine)
    STRIDE = 1016.0                     # mm per gait cycle

    def __init__(self, sc, name="person", coat=COAT, skin=SKIN, hair=HAIR, trousers=TROUSERS, gloves=None, collar=False):
        """coat: the T-shirt's colour; gloves: None (bare hands, the default near a spindle), True (tan leather) or
        an RGB colour."""
        self.sc, self.n = sc, name
        m = self.m = model()
        self.order = m["order"]
        self.bi = {b: i for i, b in enumerate(self.order)}
        self.group = f"{name}_body"
        glove = skin if not gloves else (GLOVE if gloves is True else gloves)
        colours = dict(skin=skin, forearm=skin, coat=coat, skirt=coat, collar=coat, shirt=coat, glove=glove, shoes=SHOES,
                       trousers=trousers, hair=hair, brow=BROW, iris=IRIS, sclera=SCLERA)
        spec = dict(coat=0.08, skirt=0.08, collar=0.08, glove=0.15 if gloves else 0.12, shoes=0.3, hair=0.05, skin=0.12,
                    forearm=0.12, iris=0.6,
                    sclera=0.4)
        self.parts = {}                                  # part -> (its data, PolyData)
        for part, d in m["parts"].items():
            if part == "collar" and not collar:              # a T-shirt has no collar (collar=True: a work shirt's)
                continue
            if d is None or not len(d["F"]):
                continue
            poly = _poly(d["P"], d["F"])
            poly.point_data["Normals"] = np.zeros((len(d["P"]), 3))
            poly.point_data.active_normals_name = "Normals"
            nm = f"{name}/{'coat ' if part in ('skirt', 'collar') else ''}{part}"
            sc.add(nm, poly, colours[part], self.group, specular=spec.get(part, 0.1), split_sharp_edges=False)
            sc.set_mesh(nm, poly)
            self.parts[part] = (d, poly)
        self.rigid = {}                                  # pieces that ride on the head: the glasses
        for piece, (P, F) in m["glasses"].items():
            poly = _poly(P, F)
            nm = f"{name}/glasses {piece}"
            if piece == "lens":
                sc.add(nm, poly, LENS, self.group, opacity=0.38, specular=0.9, split_sharp_edges=False)
            else:
                sc.add(nm, poly, FRAME, self.group, specular=0.5)
            sc.set_mesh(nm, poly)
            self.rigid[piece] = (P, poly)
        self.hand_groups = {s: f"{name}_hand_{s}" for s in ("l", "r")}
        self.groups = [self.group, *self.hand_groups.values()]
        self.held = {}                                   # side -> (group, offset from the hand's frame)
        self.st = dict(x=0.0, y=0.0, hd=0.0, lean=0.0, phase=0.0, amp=0.0, hands={"l": None, "r": None}, look=None,
                       grip={"l": 0.3, "r": 0.3}, palm={"l": None, "r": None}, elbow={"l": None, "r": None},
                       bend={"l": False, "r": False})
        self._rest_arm()
        self._rest_leg()
        self.gait = Gait()                               # round 9: the feet (stance foot locked, swing foot on an arc)
        self.drop = 0.0                                  # the pelvis' drop under its rest height this frame, mm
        self._posed_key = None
        hooks = getattr(sc, "before_render", None)       # pvscene.PVScene: the feet keep stepping while nobody calls set()
        if isinstance(hooks, list):
            hooks.append(self._tick)
        self.set()

    # ------------------------------------------------------------------------------------------- set-up
    def H(self, b) -> np.ndarray:
        return self.m["head"][self.bi[b]]

    def T(self, b) -> np.ndarray:
        return self.m["tail"][self.bi[b]]

    def _rest_leg(self):
        """The rest leg's geometry for the IK (round 9): hip (upperleg01's head), knee (lowerleg01's), ankle (foot's), the
        thigh's and shin's rest frames (the bone, then the body's x made square to it: the knee's hinge), and each shoe's
        points about its ankle (to keep the sole on the floor, flat or pitched)."""
        d = self.m["parts"]["shoes"]
        P = d["P"]
        self.leg = {}
        for i, side in enumerate(("L", "R")):
            hip, knee, ankle = self.H(f"upperleg01.{side}"), self.H(f"lowerleg01.{side}"), self.H(f"foot.{side}")
            frames = []
            for a, b in ((hip, knee), (knee, ankle)):
                e1 = _unit(b - a)
                e2 = _unit(np.array([1.0, 0.0, 0.0]) - e1[0] * e1)
                frames.append(np.c_[e1, e2, np.cross(e1, e2)])
            sole = P[(P[:, 0] < 0) if side == "L" else (P[:, 0] > 0)] - ankle
            self.leg[i] = dict(side=side, hip=hip, knee=knee, ankle=ankle, L1=float(np.linalg.norm(knee - hip)),
                               L2=float(np.linalg.norm(ankle - knee)), B1=frames[0], B2=frames[1], sole=sole)
        # the ankle over the floor with the foot flat and its sole's lowest point at GROUND
        self.ankle_z = GROUND - float(min(self.leg[i]["sole"][:, 2].min() for i in (0, 1)))

    def _rest_arm(self):
        """The rest arm's geometry for the IK (the upper arm, the elbow to the palm's centre, the flexion axis) and
        the fingers' rest directions."""
        self.arm = {}
        for s, side in (("l", "L"), ("r", "R")):
            Sh, El, Wr = self.H(f"upperarm01.{side}"), self.H(f"lowerarm01.{side}"), self.H(f"wrist.{side}")
            k1, k2 = self.H(f"finger2-1.{side}"), self.H(f"finger5-1.{side}")
            palm_n = -_unit(np.cross(k1 - Wr, k2 - Wr))
            base, tip = self.H(f"finger3-1.{side}"), self.T(f"finger3-3.{side}")
            dm = _unit(base - self.H(f"metacarpal2.{side}"))
            if (tip - (base + dm * np.linalg.norm(tip - base))) @ palm_n < 0:
                palm_n = -palm_n
            palm = Wr + 0.55 * ((k1 + k2) / 2 - Wr) + 12.0 * palm_n
            a0 = _unit(El - Sh)
            f0 = _unit(palm - El)
            k0 = _unit(np.cross(a0, f0))
            mid = _unit(self.T(f"finger3-1.{side}") - self.H(f"finger3-1.{side}"))
            close = {}
            for fi in (2, 4, 5):
                d = _unit(self.T(f"finger{fi}-1.{side}") - self.H(f"finger{fi}-1.{side}"))
                ang = math.acos(float(np.clip(d @ mid, -1, 1)))
                close[fi] = _rot(np.cross(d, mid), 0.8 * ang) if ang > 1e-3 else np.eye(3)
            self.arm[s] = dict(side=side, L1=float(np.linalg.norm(El - Sh)), L2=float(np.linalg.norm(palm - El)),
                               a0=a0, f0=f0, k0=k0, e0=math.acos(float(np.clip(a0 @ f0, -1, 1))), palm=palm,
                               palm_n=palm_n, close=close, fw=_unit(Wr - self.H(f"lowerarm02.{side}")))

    # ------------------------------------------------------------------------------------------- the API
    def names(self):
        return [n for n, g in self.sc.group_of.items() if g in self.groups]

    def show(self, a):
        for n in self.names():
            self.sc.alpha[n] = a

    def frame(self) -> np.ndarray:
        s = self.st
        c, si = math.cos(math.radians(s["hd"])), math.sin(math.radians(s["hd"]))
        return _M(np.array([[c, -si, 0], [si, c, 0], [0, 0, 1.0]]), (s["x"], s["y"], 0.0))

    def rest_hand(self, side) -> np.ndarray:
        """Where a hand hangs (world): at the side, a little forward, swinging against the legs when walking (round 9:
        the swing follows the feet, the left hand forward as the right foot is)."""
        sx = -1.0 if side == "l" else 1.0
        swing = self.gait.arm_swing(side, self.st)
        a = self.arm[side]
        sh = self.H(f"upperarm01.{a['side']}")
        local = np.r_[sx * (abs(sh[0]) + 40.0), 45.0 + swing,
                      sh[2] - a["L1"] - a["L2"] + 18.0 + 0.25 * abs(swing) - self.drop, 1.0]
        return (self.frame() @ local)[:3]

    def set(self, **kw):
        """Pose the person: x, y (mm), hd (deg) put its frame in the world; lean (deg), hands {"l", "r": world point or
        None}, palm, grip, look as before. Round 9: the legs are no longer a phase-driven cycle: the feet are planted on
        footprints and step when the body moves away from them (Gait), each leg solved to its foot. ``phase`` and
        ``amp`` are accepted and ignored. ``frame=k`` gives the frame number explicitly (default: the open
        common.Chapter's, or, with none open, one frame per call that moves the body)."""
        s = self.st
        clock = kw.pop("frame", None)
        for k, v in kw.items():
            if k in ("hands", "grip", "palm", "elbow", "bend"):
                s[k] = dict(s[k], **v)
            else:
                s[k] = v
        if clock is not None:
            self.gait.explicit = True
        self.gait.update(s["x"], s["y"], s["hd"], _clock() if clock is None else int(clock))
        self._pose()

    def place(self, x=None, y=None, hd=None, **kw):
        """Put the person somewhere new, both feet planted under the body (a cut: no steps drawn)."""
        s = self.st
        s.update({k: float(v) for k, v in (("x", x), ("y", y), ("hd", hd)) if v is not None})
        self.gait.reset(s["x"], s["y"], s["hd"], clock=kw.get("frame", _clock()))
        self.set(**kw)

    def _tick(self):
        """pvscene's before_render hook: bring the feet up to the frame being drawn (a swing foot lands, a last step
        settles) when nobody called set() for this frame."""
        if self.gait.update(self.st["x"], self.st["y"], self.st["hd"], _clock(), passive=True):
            self._pose()

    @property
    def walking(self) -> bool:
        """A foot is in the air or the body is moving."""
        return self.gait.busy()

    def hold(self, side, group):
        """Carry Scene group `group` in a hand from now on (as it is now, relative to the hand)."""
        sc = self.sc
        Mw = sc.world(group)
        Mh = sc.gmat[self.hand_groups[side]]
        self.held[side] = (group, np.linalg.inv(Mh) @ Mw)

    def let_go(self, side, parent=None):
        sc = self.sc
        grp, _ = self.held.pop(side)
        Mw = sc.world(grp)
        if parent is None:
            sc.parent.pop(grp, None)
            sc.gmat[grp] = Mw
        else:
            sc.parent[grp] = parent
            sc.gmat[grp] = np.linalg.inv(sc.world(parent)) @ Mw

    def hand_point(self, side) -> np.ndarray:
        """The palm's centre now (world)."""
        return (self.sc.gmat[self.hand_groups[side]] @ np.r_[self.arm[side]["palm"], 1.0])[:3]

    # ------------------------------------------------------------------------------------------- posing
    def _chain(self, Q: dict, root: np.ndarray) -> np.ndarray:
        """Skinning transforms (nb, 4, 4): each bone's rotation Q (in the rest frame, about its rest head)
        composed down the chain from the root's transform."""
        S = np.empty((len(self.order), 4, 4))
        heads = self.m["head"]
        for i, b in enumerate(self.order):
            p = self.m["parent"][i]
            base = root if p < 0 else S[p]
            q = Q.get(b)
            if q is None:
                S[i] = base
            else:
                h = heads[i]
                L = np.eye(4)
                L[:3, :3] = q
                L[:3, 3] = h - q @ h
                S[i] = base @ L
        return S

    def _legs(self, Q, Rr, Finv):
        """Round 9: each leg solved to its foot (two-bone IK, the knee towards the foot's toes), the foot flat on its
        heading (pitched a little in the air). The pelvis drops just enough for both legs to reach their feet (a knee
        never quite straight). Returns the root's transform; fills Q's thigh, shin and foot rotations."""
        hips = (self.H("upperleg01.L") + self.H("upperleg01.R")) / 2
        t0 = hips - Rr @ hips
        feet = self.gait.pose()                          # [(x, y, heading deg, lift mm, pitch deg)] world, left and right
        hd = self.st["hd"]
        tg = []
        need = self.gait.knee_flex()                     # a little more knee while walking
        for i, (fx, fy, psi, lift, pitch) in enumerate(feet):
            lg = self.leg[i]
            Rf = _rot((0, 0, 1), math.radians(psi - hd)) @ _rot((1, 0, 0), math.radians(pitch))
            lowest = float((lg["sole"] @ Rf.T)[:, 2].min())
            A = (Finv @ np.r_[fx, fy, GROUND - lowest + lift, 1.0])[:3]
            Hp = Rr @ lg["hip"] + t0
            dxy = float(np.hypot(*(A[:2] - Hp[:2])))
            Lm = 0.985 * (lg["L1"] + lg["L2"])
            reach = math.sqrt(max(Lm * Lm - dxy * dxy, 0.0))
            need = max(need, float(Hp[2] - A[2] - reach))
            tg.append((A, Rf))
        drop = min(max(need, 0.0), 180.0)
        self.drop = drop
        root = _M(Rr, t0 + np.array([0.0, 0.0, -drop]))
        over = 0.0
        for i, (A, Rf) in enumerate(tg):
            lg = self.leg[i]
            sd = lg["side"]
            Hp = root[:3, :3] @ lg["hip"] + root[:3, 3]
            d = A - Hp
            L1, L2 = lg["L1"], lg["L2"]
            Lr = float(np.linalg.norm(d))
            L = min(max(Lr, abs(L1 - L2) + 5.0), L1 + L2 - 0.5)
            over = max(over, Lr - L)
            du = _unit(d)
            pole = Rf[:, 1]                              # the knee goes over the toes
            v = pole - (pole @ du) * du
            v = _unit(v if np.linalg.norm(v) > 1e-6 else np.array([0.0, 1.0, 0.0]))
            a = (L1 * L1 - L2 * L2 + L * L) / (2 * L)
            b = math.sqrt(max(L1 * L1 - a * a, 0.0))
            K = Hp + a * du + b * v
            A2 = Hp + L * du
            e2 = _unit(np.cross(du, v))
            e1 = _unit(K - Hp)
            Rth = np.c_[e1, e2, np.cross(e1, e2)] @ lg["B1"].T
            e1 = _unit(A2 - K)
            Rsh = np.c_[e1, e2, np.cross(e1, e2)] @ lg["B2"].T
            Q[f"upperleg01.{sd}"] = Rr.T @ Rth
            Q[f"lowerleg01.{sd}"] = Rth.T @ Rsh
            Q[f"foot.{sd}"] = Rsh.T @ Rf
        self.gait.note_overreach(over)
        return root

    def _pose(self):
        s = self.st
        Q = {}
        lean = math.radians(s["lean"])
        F = self.frame()
        Finv = np.linalg.inv(F)
        # the pelvis: the lean's share at the hips, about the hip joints, and a little yaw with the feet; the legs to the
        # feet (round 9: the stance foot stays on its footprint; the pelvis drops so both legs reach)
        sway = self.gait.sway(s)
        Rr = _rot((1, 0, 0), -self.LEAN_HIPS * lean) @ _rot((0, 0, 1), sway)
        root = self._legs(Q, Rr, Finv)
        rest = (1.0 - self.LEAN_HIPS) * lean
        for b in ("spine05", "spine04", "spine03", "spine02"):
            Q[b] = _rot((1, 0, 0), -rest / 4)
        Q["spine01"] = _rot((0, 0, 1), -1.3 * sway)
        # the head: towards what it looks at, or ahead
        S = self._chain(Q, root)
        look = s["look"]
        yaw = pitch = 0.0
        if look is not None:
            loc = Finv @ np.r_[np.asarray(look, float), 1.0]
            hpos = (S[self.bi["head"]] @ np.r_[self.H("head") + (0, 60.0, 40.0), 1.0])[:3]
            d = loc[:3] - hpos
            yaw = float(np.clip(math.atan2(-d[0], max(d[1], 1e-6)), -1.2, 1.2))
            down = math.atan2(-d[2], math.hypot(d[0], d[1]))
            pitch = float(np.clip(down - lean, math.radians(-25), math.radians(45)))
        elif lean > 0:
            pitch = -0.35 * lean
        for b, k in (("neck01", 0.3), ("neck03", 0.25), ("head", 0.45)):
            Q[b] = _rot((0, 0, 1), k * yaw) @ _rot((1, 0, 0), -k * pitch)
        S = self._chain(Q, root)
        # the arms: two-bone IK from the posed shoulder to each palm target
        for side in ("l", "r"):
            tgt = s["hands"][side]
            Hw = self.rest_hand(side) if tgt is None else np.asarray(tgt, float)
            Hl = (Finv @ np.r_[Hw, 1.0])[:3]
            bend = bool(s["bend"][side]) and tgt is not None and s["palm"][side] is not None
            aim = Hl
            for _ in range(3 if bend else 1):            # with a bent wrist the palm moves: aim again, less its error
                self._arm(Q, root, S, side, aim, tgt, Finv, bend)
                if bend:
                    St = self._chain(Q, root)
                    got = (St[self.bi[f"wrist.{self.arm[side]['side']}"]] @ np.r_[self.arm[side]["palm"], 1.0])[:3]
                    aim = aim + (Hl - got)
        S = self._chain(Q, root)
        # round 9: no grounding shift here: each foot is already where its footprint (or its swing) puts it, the lowest
        # point of a planted sole at GROUND (round 8 shifted the whole body to ground the lowest shoe, which dragged the
        # planted foot along with the gait)
        self.S = S
        # the hands' frames (world), for what they hold
        for side in ("l", "r"):
            Mh = F @ S[self.bi[f"wrist.{self.arm[side]['side']}"]]
            self.sc.gmat[self.hand_groups[side]] = Mh
            if side in self.held:
                grp, off = self.held[side]
                self.sc.gmat[grp] = Mh @ off
                self.sc.parent.pop(grp, None)
        self._skin(S)
        self.sc.gmat[self.group] = F

    def _arm(self, Q, root, S, side, Hl, tgt, Finv, bend=False):
        """One arm: two-bone IK from the posed shoulder to the palm target Hl (local), the forearm turned to the palm's
        direction, the wrist bent (bend: round 9, up to 45 deg) to finish turning it, the fingers curled."""
        s = self.st
        if True:
            a = self.arm[side]
            sd = a["side"]
            Q.pop(f"wrist.{sd}", None)
            Sh = (S[self.bi[f"shoulder01.{sd}"]] @ np.r_[self.H(f"upperarm01.{sd}"), 1.0])[:3]
            d = Hl - Sh
            L = float(np.linalg.norm(d))
            L1, L2 = a["L1"], a["L2"]
            L = min(max(L, abs(L1 - L2) + 5.0), L1 + L2 - 2.0)
            du = _unit(d)
            sx = -1.0 if side == "l" else 1.0
            pole = np.array([sx * 0.75, -0.30, -1.0]) if s["elbow"][side] is None else Finv[:3, :3] @ _unit(s["elbow"][side])
            v = pole - (pole @ du) * du
            if np.linalg.norm(v) < 1e-6:
                v = np.array([sx, 0.0, 0.0]) - du[0] * sx * du
            v = _unit(v)
            p = (L1 * L1 - L2 * L2 + L * L) / (2 * L)
            q = math.sqrt(max(L1 * L1 - p * p, 0.0))
            E = Sh + p * du + q * v
            Ht = Sh + du * L
            au = _unit(E - Sh)
            fu = _unit(Ht - E)
            k = _unit(np.cross(v, du))
            eps = math.acos(float(np.clip(au @ fu, -1, 1)))
            Rw = np.c_[au, k, np.cross(au, k)] @ np.c_[a["a0"], a["k0"], np.cross(a["a0"], a["k0"])].T
            P = S[self.bi[f"shoulder01.{sd}"]][:3, :3]
            Q[f"upperarm01.{sd}"] = P.T @ Rw
            Q[f"lowerarm01.{sd}"] = _rot(a["k0"], eps - a["e0"])
            # the forearm's turn: palms down to a bar in front, towards the thighs when hanging; or the palm turned
            # to face a given direction (s["palm"]: "down" or a vector in the world)
            want = s["palm"][side]
            if want is None or tgt is None:
                reach = 0.0 if tgt is None else float(np.clip((Hl[2] - (Sh[2] - L1 - L2 + 120.0)) / 380.0, 0.0, 1.0))
                Q[f"lowerarm02.{sd}"] = _rot(a["fw"], -sx * math.radians(-15.0 + 70.0 * reach))
            else:
                tdir = np.array([0.0, 0.0, -1.0]) if isinstance(want, str) else Finv[:3, :3] @ _unit(want)
                Q[f"lowerarm02.{sd}"] = np.eye(3)
                St = self._chain(Q, root)
                n0 = St[self.bi[f"wrist.{sd}"]][:3, :3] @ a["palm_n"]
                fax = _unit(St[self.bi[f"lowerarm01.{sd}"]][:3, :3] @ a["fw"])
                u0, u1 = n0 - (n0 @ fax) * fax, tdir - (tdir @ fax) * fax
                th = math.atan2(float(fax @ np.cross(u0, u1)), float(u0 @ u1))
                Q[f"lowerarm02.{sd}"] = _rot(a["fw"], th)
                if bend:                                 # round 9: the wrist finishes the turn (the fingers along a face)
                    St = self._chain(Q, root)
                    Rp = St[self.bi[f"wrist.{sd}"]][:3, :3]
                    n1 = Rp @ a["palm_n"]
                    ax = np.cross(n1, tdir)
                    ang = math.atan2(float(np.linalg.norm(ax)), float(n1 @ tdir))
                    if np.linalg.norm(ax) > 1e-9 and ang > 1e-3:
                        Rm = _rot(ax, min(ang, math.radians(45.0)))
                        Q[f"wrist.{sd}"] = Rp.T @ Rm @ Rp
            # the fingers: together, curled a little, more when holding
            g = s["grip"][side] if side not in self.held else 0.8
            for fi in range(2, 6):
                for j, w in ((1, 0.8), (2, 1.0), (3, 0.75)):
                    b = f"finger{fi}-{j}.{sd}"
                    ax = _unit(np.cross(_unit(self.T(b) - self.H(b)), a["palm_n"]))
                    R_ = _rot(ax, math.radians(70.0) * g * w)
                    Q[b] = R_ @ a["close"][fi] if (j == 1 and fi in a["close"]) else R_
            for j in (1, 2, 3):
                b = f"finger1-{j}.{sd}"
                ax = _unit(np.cross(_unit(self.T(b) - self.H(b)), a["palm_n"]))
                if bend:                                 # a flat hand on a face: the thumb back out of the palm's way
                    Q[b] = _rot(ax, math.radians(-22.0))
                elif j > 1:
                    Q[b] = _rot(ax, math.radians(35.0) * g)
                else:
                    Q.pop(b, None)

    def _skin(self, S):
        for part, (d, poly) in self.parts.items():
            P0, rows, cols, vals = d["P"], d["rows"], d["cols"], d["vals"]
            Pk = np.einsum("kij,kj->ki", S[cols, :3, :3], P0[rows]) + S[cols, :3, 3]
            n = len(P0)
            P = np.empty((n, 3))
            for j in range(3):
                P[:, j] = np.bincount(rows, weights=vals * Pk[:, j], minlength=n)
            poly.points = P
            poly.point_data["Normals"] = _normals(P, d["F"], n)
            poly.point_data.active_normals_name = "Normals"
        Mh = S[self.bi["head"]]
        for piece, (P0, poly) in self.rigid.items():
            poly.points = P0 @ Mh[:3, :3].T + Mh[:3, 3]

    def posed(self) -> dict:
        """{actor name: (points (n, 3) in the world, faces (m, 3))} as posed now: for collision checks."""
        F = self.sc.gmat[self.group]
        out = {}
        for part, (d, poly) in self.parts.items():
            P = np.asarray(poly.points, float)
            out[part] = (P @ F[:3, :3].T + F[:3, 3], d["F"])
        return out


# ================================================================================================ the feet (round 9)
def _clock():
    """The frame being drawn: the open common.Chapter's frame count (audit_rec.py numbers its records the same way), or
    None when no chapter is open."""
    c = sys.modules.get("common")
    cur = getattr(c, "CURRENT", None) if c is not None else None
    n = getattr(cur, "n", None)
    return int(n) if n is not None else None


def _wrap(a):
    return (a + 180.0) % 360.0 - 180.0


def _smooth(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3.0 - 2.0 * u)


class Gait:
    """Round 9's foot lock (Sterling, 2026-11-26: "moonwalk"; round 8's audit: people.py's phase-driven gait slid the
    planted foot 0.34-1.0 m per metre walked). Each Person owns one (``person.gait``); nobody needs to drive it.

    The body's frame (x, y, hd: the pelvis' path on the floor) is whatever the caller sets, frame by frame. Each foot is
    either planted on a footprint (its ankle's point on the floor and its heading, world) or in the air on its way to the
    next one. A planted foot never moves: its sole's lowest point is at GROUND and the leg is solved to it (Person._legs:
    two-bone IK hip-knee-ankle, the knee over the toes, the foot flat on its heading; the pelvis drops as far as both legs
    need). When the body moves away from where a foot would stand (its home: HOME_X to the side of the body's line,
    HOME_Y behind its origin, toes out TOE_OUT), the foot further off steps: it lifts and travels a raised arc (smoothstep
    along the floor, a sine up and down, toes down then up) for n frames to the footprint where it would stand when the
    body has gone half a step past it (the body's speed and turn rate times the time to landing plus half a step), with the
    feet kept MIN_SEP apart across the body, no more than SPREAD_MAX apart, and turning at most TURN_MAX a step. Then the
    other foot. So walking, turning on the spot, side-steps, backing up and shuffles all come out as discrete steps, and
    standing still is both feet planted. The cadence follows the speed: 1.25 steps a second standing (settling steps) to
    2.0 at 1.3 m/s, the foot in the air for about 0.78 of a step.

    Time is the drawn frame: the open common.Chapter's frame number (or ``set(frame=k)``; with no chapter open, one frame
    per set() that moves the body). Calling set() again in the same frame re-solves that frame from the previous one, so
    a caller may set the body several times before it renders. pvscene.PVScene.render() calls Person._tick first, so the
    feet keep stepping (a swing lands, a settling step) while a caller holds the body still without calling set(). A
    move of more than JUMP_MM (walk.py's JUMP_MM, 3 m/s) or JUMP_DEG in one frame is a cut: the feet are put under the
    body, as is a move of more than PLACE_MM within one frame. ``Person.place(x, y, hd)`` does that explicitly.

    What it can't do: a body that moves faster than about 1.4 m/s outruns the steps (the stance leg can't reach its
    footprint and the foot would be dragged; ``overreach_frames`` counts such frames); a person should not walk in a
    time-lapse (cut instead)."""

    FPS = 12.0
    HOME_X, HOME_X_WALK, HOME_Y = 110.0, 95.0, -15.0   # mm: the ankles' home about the body's origin, standing and walking
    TOE_OUT = 5.0                       # deg each foot turns out
    JUMP_MM, JUMP_DEG = 250.0, 45.0     # one frame's move that is a cut, not walking
    PLACE_MM, PLACE_DEG = 10.0, 3.0     # a move within one frame (no time for a step) that is a placement
    R_TURN = 160.0                      # mm of a foot's "distance from home" per radian of heading error
    STEP_MAX = 1300.0                   # mm a foot travels in one step at most (a stride: twice the step length)
    SPREAD_MAX = 760.0                  # mm between the planted ankles at most (a long step)
    MIN_SEP = 160.0                     # mm between the ankles across the body at least (the shoes are 116 mm wide)
    TURN_MAX = 50.0                     # deg a foot turns in one step at most
    SETTLE_MM, STEP_MM = 70.0, 25.0     # a foot steps when this far from home: standing, and walking at speed

    def __init__(self):
        self.feet = None                # [left, right]: dict(p=ankle's floor point (2,), psi=heading deg, sw=None or the swing)
        self.body = None                # (x, y, hd) at the last frame advanced
        self.v = np.zeros(2)            # the body's velocity, mm a frame (smoothed)
        self.w = 0.0                    # its turn rate, deg a frame (smoothed)
        self.since = 99                 # frames since a foot landed
        self.last = 1                   # the foot that stepped last
        self.clock = None               # the frame the state is at
        self.virtual = False            # the clock is our own (no chapter open)
        self.base = None                # (clock, state) before this frame: a second set() in the frame starts from it
        self.seen = None                # ((x, y, hd), clock) of the last update
        self.steps = 0
        self.overreach_frames = 0
        self.overreach_mm = 0.0
        self.explicit = False           # set(frame=k) was used: the render hook leaves the clock to the caller

    # ---------------------------------------------------------------------------------------- state
    @staticmethod
    def _cp(feet):
        return None if feet is None else [dict(f, p=f["p"].copy(), sw=None if f["sw"] is None else dict(f["sw"]))
                                          for f in feet]

    def _state(self):
        return self._cp(self.feet), self.body, self.v.copy(), self.w, self.since, self.last, self.steps

    def _restore(self, st):
        feet, self.body, v, self.w, self.since, self.last, self.steps = st
        self.feet, self.v = self._cp(feet), v.copy()

    def home(self, x, y, hd, i, walk=0.0):
        """Foot i's (0 left, 1 right) footprint for a body at (x, y, hd): (ankle's floor point, heading)."""
        sx = -1.0 if i == 0 else 1.0
        hx = self.HOME_X + (self.HOME_X_WALK - self.HOME_X) * walk
        a = math.radians(hd)
        c, s = math.cos(a), math.sin(a)
        lx, ly = sx * hx, self.HOME_Y
        return np.array([x + c * lx - s * ly, y + s * lx + c * ly]), hd - sx * self.TOE_OUT

    def reset(self, x, y, hd, clock=None):
        """Both feet planted at home under a body at (x, y, hd) (a cut)."""
        self.feet = []
        for i in (0, 1):
            p, psi = self.home(x, y, hd, i)
            self.feet.append(dict(p=p, psi=psi, sw=None))
        self.body = (float(x), float(y), float(hd))
        self.v, self.w, self.since = np.zeros(2), 0.0, 99
        if clock is not None:
            self.clock = clock
        self.base = (self.clock, self._state())
        self.seen = None

    # ---------------------------------------------------------------------------------------- time
    def update(self, x, y, hd, clock=None, passive=False):
        """Bring the feet to frame `clock` (None: our own clock) with the body at (x, y, hd). True if anything changed."""
        body = (float(x), float(y), float(hd))
        if passive and (clock is None or self.virtual or self.explicit):
            return False                                 # the render hook follows a chapter's clock only
        virtual = clock is None
        if virtual:
            if self.virtual and self.seen is not None and self.seen[0] == body:
                return False
            clock = self.clock + 1 if (self.virtual and self.clock is not None) else 0
        if passive and self.seen is not None and self.seen == (body, clock):
            return False
        before = self.pose() if self.feet is not None else None
        if self.feet is None or virtual != self.virtual or self.clock is None or clock < self.clock:
            # a new sequence (the first pose, a chapter opened): adopt the clock; a move now is a placement
            self.virtual = virtual
            if self.feet is None or self._moved(body, self.body):
                self.reset(*body, clock=clock)
            else:
                self.body = body
                self.clock = clock
                self.base = (clock, self._state())
        else:
            if clock > self.clock:
                self.base = (self.clock, self._state())
                self.clock = clock
            else:
                self._restore(self.base[1])
            k = clock - self.base[0]
            b0 = self.body
            moved = math.hypot(body[0] - b0[0], body[1] - b0[1])
            turned = abs(_wrap(body[2] - b0[2]))
            if k <= 0:
                if self._moved(body, b0):
                    self.reset(*body, clock=clock)
                else:
                    self.body = body
            elif moved / k > self.JUMP_MM or turned / k > self.JUMP_DEG:
                self.reset(*body, clock=clock)
            else:
                for j in range(1, k + 1):
                    u = j / k
                    self._frame((b0[0] + (body[0] - b0[0]) * u, b0[1] + (body[1] - b0[1]) * u,
                                 b0[2] + _wrap(body[2] - b0[2]) * u))
        self.seen = (body, clock)
        return before is None or before != self.pose() or not passive

    def _moved(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1]) > self.PLACE_MM or abs(_wrap(a[2] - b[2])) > self.PLACE_DEG

    def _speed(self):
        return float(np.linalg.norm(self.v)) + self.R_TURN * math.radians(abs(self.w))

    def _timing(self, speed):
        """(frames from one landing to the next, frames a foot is in the air, frames both feet stay down after a landing,
        counting the landing's) at `speed` mm a frame: 1.4 steps a second for a settling step, 1.9 at 1 m/s, 2.3 at most."""
        vm = speed * self.FPS / 1000.0
        c = float(np.clip(1.4 + 0.5 * vm, 1.4, 2.3))       # steps a second
        P = max(4, int(round(self.FPS / c)))
        ds = 1 + int(speed < 25.0) + int(speed < 8.0)
        return P, int(np.clip(P - ds + 1, 4, 9)), ds

    def _frame(self, body):
        x, y, hd = body
        d = np.array([x - self.body[0], y - self.body[1]])
        v0 = self.v
        self.v = 0.5 * self.v + 0.5 * d
        self.a = 0.5 * getattr(self, "a", np.zeros(2)) + 0.5 * (self.v - v0)
        self.w = 0.5 * self.w + 0.5 * _wrap(hd - self.body[2])
        self.body = body
        self.since += 1
        for i, f in enumerate(self.feet):
            sw = f["sw"]
            if sw is None:
                continue
            sw["k"] += 1
            if 2 * sw["k"] <= sw["n"]:                   # the first half of a swing still aims at the moving target,
                n_now = self._timing(self._speed())[1]   # and a body speeding up shortens it
                if n_now < sw["n"]:
                    sw["n"] = max(sw["k"] + 2, n_now)
                sw["p1"], sw["psi1"] = self._target(i, sw["n"] - sw["k"])
            elif sw["k"] <= sw["n"] - 2:                 # later, it follows a body that slows down (a shorter last
                p1, psi1 = self._target(i, sw["n"] - sw["k"])   # step instead of one past the stop), 45 mm a frame at most
                dp = p1 - np.asarray(sw["p1"], float)
                dl = float(np.linalg.norm(dp))
                sw["p1"] = np.asarray(sw["p1"], float) + (dp * (45.0 / dl) if dl > 45.0 else dp)
                sw["psi1"] = psi1
            if sw["k"] >= sw["n"]:
                f["p"], f["psi"], f["sw"] = np.asarray(sw["p1"], float).copy(), float(sw["psi1"]), None
                self.since, self.last = 0, i
        if self.feet[0]["sw"] is None and self.feet[1]["sw"] is None:
            self._maybe_step()

    def _target(self, i, t):
        """Foot i's next footprint if it lands in t frames: as far ahead of the body as it will be behind it when it
        lifts again (a stance lasts a step and the double support after it)."""
        x, y, hd = self.body
        v = self.v
        sp = float(np.linalg.norm(v))
        vl = v + getattr(self, "a", np.zeros(2)) * t   # the body's velocity at the landing: speeding up or slowing down
        if sp < 1e-6 or float(vl @ v) <= 0.0:
            vl = np.zeros(2)
        else:
            vl = vl * min(1.0, (sp + 6.0 * t) / max(float(np.linalg.norm(vl)), 1e-9))
        P, _, ds = self._timing(float(np.linalg.norm(vl)) + self.R_TURN * math.radians(abs(self.w)))
        half = 0.5 * (P + ds)
        hdp = hd + self.w * (t + half)
        walk = float(np.clip(sp / 40.0, 0.0, 1.0))
        ahead = 0.5 * (v + vl) * t + vl * half
        p, psi = self.home(x + ahead[0], y + ahead[1], hdp, i, walk)
        o, f = self.feet[1 - i], self.feet[i]
        a = math.radians(hdp)
        right = np.array([math.cos(a), math.sin(a)])
        sx = -1.0 if i == 0 else 1.0
        lat = float((p - o["p"]) @ right)
        if sx * lat < self.MIN_SEP:                      # never across (or onto) the other foot
            p = p + right * sx * (self.MIN_SEP - sx * lat)
        dv = p - o["p"]
        dl = float(np.linalg.norm(dv))
        if dl > self.SPREAD_MAX:
            p = o["p"] + dv * (self.SPREAD_MAX / dl)
        tv = p - f["p"]
        tl = float(np.linalg.norm(tv))
        if tl > self.STEP_MAX:
            p = f["p"] + tv * (self.STEP_MAX / tl)
        return p, f["psi"] + float(np.clip(_wrap(psi - f["psi"]), -self.TURN_MAX, self.TURN_MAX))

    def _maybe_step(self):
        speed = self._speed()
        P, n, ds = self._timing(speed)
        if self.since < ds:
            return
        thr = float(np.clip(self.SETTLE_MM - 2.5 * speed, self.STEP_MM, self.SETTLE_MM))
        errs, tg = [], []
        for i in (0, 1):
            p1, psi1 = self._target(i, n)
            f = self.feet[i]
            errs.append(float(np.linalg.norm(p1 - f["p"])) + self.R_TURN * math.radians(abs(_wrap(psi1 - f["psi"]))))
            tg.append((p1, psi1))
        i = int(np.argmax(errs))
        if errs[i] < thr:
            return
        if i == self.last and errs[1 - i] >= thr:        # alternate feet while both want to go
            i = 1 - i
        f = self.feet[i]
        p1, psi1 = tg[i]
        travel = float(np.linalg.norm(p1 - f["p"]))
        f["sw"] = dict(p0=f["p"].copy(), psi0=f["psi"], p1=p1, psi1=psi1, k=1, n=n,
                       lift=float(np.clip(30.0 + 0.07 * travel, 30.0, 75.0)))
        self.steps += 1

    # ---------------------------------------------------------------------------------------- what is drawn
    def pose(self):
        """Each foot now: [(x, y, heading deg, lift mm, pitch deg)], left then right (world)."""
        out = []
        for f in self.feet:
            sw = f["sw"]
            if sw is None:
                out.append((float(f["p"][0]), float(f["p"][1]), float(f["psi"]), 0.0, 0.0))
                continue
            u = sw["k"] / sw["n"]
            s = _smooth(u)
            p = sw["p0"] + (np.asarray(sw["p1"]) - sw["p0"]) * s
            psi = sw["psi0"] + _wrap(sw["psi1"] - sw["psi0"]) * s
            out.append((float(p[0]), float(p[1]), float(psi), sw["lift"] * math.sin(math.pi * u),
                        -10.0 * math.sin(2.0 * math.pi * u)))
        return out

    def _split(self, st):
        """The right foot's lead over the left along the body's heading, mm."""
        a = math.radians(st["hd"])
        fwd = np.array([-math.sin(a), math.cos(a)])
        P = self.pose()
        return float((np.array(P[1][:2]) - np.array(P[0][:2])) @ fwd)

    def arm_swing(self, side, st):
        """How far forward a hanging hand swings (mm): against the feet, the left hand forward with the right foot."""
        if self.feet is None:
            return 0.0
        d = self._split(st)
        return float(np.clip((0.2 if side == "l" else -0.2) * d, -110.0, 110.0))

    def sway(self, st):
        """The pelvis' yaw (rad), the hip over the forward foot a little ahead."""
        if self.feet is None:
            return 0.0
        return 0.05 * float(np.clip(self._split(st) / 400.0, -1.0, 1.0))

    def knee_flex(self):
        """The pelvis' least drop (mm): the knees a little bent while walking."""
        return 15.0 * float(np.clip(np.linalg.norm(self.v) / 30.0, 0.0, 1.0))

    def busy(self):
        return self.feet is not None and (any(f["sw"] is not None for f in self.feet) or self._speed() > 0.5)

    def note_overreach(self, mm):
        if mm > 1.0:
            self.overreach_frames += 1
            self.overreach_mm = max(self.overreach_mm, float(mm))


# ================================================================================================ two people carrying (round 9)
ARM_BONES = ("upperarm", "lowerarm", "wrist", "metacarpal", "finger", "shoulder", "clavicle")
HIP_PIVOT = (12.8, 911.3)               # (y, z) of the hip joints at rest: a lean turns the body above them about x


@functools.lru_cache(maxsize=None)
def _body_points():
    """The dressed body at rest without its arms (local frame): the points a carried load must stay clear of."""
    m = model()
    order = m["order"]
    out = []
    for part, d in m["parts"].items():
        if d is None or part in ("glove", "forearm", "iris", "sclera", "brow"):
            continue
        n = len(d["P"])
        best, dom = np.zeros(n), np.zeros(n, int)
        for r, c, v in zip(d["rows"], d["cols"], d["vals"]):
            if v > best[r]:
                best[r], dom[r] = v, c
        arm = np.array([order[c].startswith(ARM_BONES) for c in dom])
        out.append(d["P"][~arm])
    return np.vstack(out)


def body_front(zlo, zhi, lean=0.0):
    """How far in front of its origin (local y, mm) the dressed body reaches between heights zlo and zhi, leaning `lean`
    degrees (the body above the hips turned about them), arms left out."""
    P = _body_points()
    y, z = P[:, 1], P[:, 2]
    a = math.radians(lean)
    yp, zp = HIP_PIVOT
    up = z > zp
    y2 = np.where(up, yp + (y - yp) * math.cos(a) + (z - zp) * math.sin(a), y)
    z2 = np.where(up, zp + (z - zp) * math.cos(a) - (y - yp) * math.sin(a), z)
    sel = (z2 >= zlo) & (z2 <= zhi)
    return float(y2[sel].max()) if sel.any() else 0.0


def carry(lo, hi, M, ends=("-x", "+x"), grip=None, clear=30.0, inset=None, gap=18.0, z_hands=None):
    """Two people carrying a box-shaped load, one at each of two opposite ends (round 9; round 8's audit found their gloves
    and coats over 100 mm inside the plate they carried). Returns [dict] per person, ready for ``Person.set(**d)`` (x, y,
    hd, lean, hands, palm, grip, look), plus ``reach_mm`` (how far the hardest hand is from the arm's reach, < 0 when
    within it) and ``front_mm`` (the body's front to the load's face).

    lo, hi: the load's box in its own frame (mm); M: its pose (4 x 4, world; the load level). ends: the two faces held,
    "-x", "+x", "-y" or "+y" of the load's frame; each person stands outside one, facing the load. grip: "side" (palms
    in on the two faces beside the end, `inset` mm in from it, at z_hands or the box's mid-height, `gap` mm off the faces
    so the wrists and forearms stay out) or "under" (palms up under the bottom face, `inset` in from the end; the
    forearms must come in level, so the load rides at elbow height); default "side" when the end is at most 420 mm wide.
    The person stands as close as keeps the dressed body (people.py's mesh at rest, arms left out, leaned as needed to
    reach) `clear` mm off the load's face. A stance is rigid in the load's frame, so moving the load moves the people
    with it, and their Gait walks them there (``carry_check`` measures what was drawn)."""
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    M = np.asarray(M, float)
    R, t = M[:3, :3], M[:3, 3]
    corners = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]) @ R.T + t
    zb, zt = float(corners[:, 2].min()), float(corners[:, 2].max())
    out = []
    for e in ends:
        ax = "xyz".index(e[1])
        sgn = -1.0 if e[0] == "-" else 1.0
        lat = 1 - ax if ax < 2 else 0                    # the other horizontal axis of the load
        nrm = R[:, ax] * sgn                             # the end face's outward normal (world)
        nh = np.array([nrm[0], nrm[1]]) / max(1e-9, float(np.hypot(nrm[0], nrm[1])))
        face_c = (lo + hi) / 2
        face_c[ax] = hi[ax] if sgn > 0 else lo[ax]
        fc = R @ face_c + t
        width = hi[lat] - lo[lat]
        length = hi[ax] - lo[ax]
        g = grip or ("side" if width <= 420.0 else "under")
        ins = inset if inset is not None else (min(90.0, 0.25 * length) if g == "side" else 30.0)
        hd = math.degrees(math.atan2(nh[0], -nh[1]))     # facing -nh: forward (-sin hd, cos hd) = -nh
        a = math.radians(hd)
        right = np.array([math.cos(a), math.sin(a)])
        latw = R[:, lat] * (1.0 if float(R[:2, lat] @ right) >= 0 else -1.0)   # the load's lateral axis, to the right
        zc = (zb + zt) / 2 if z_hands is None else float(z_hands)
        fwd3 = np.array([-nh[0], -nh[1], 0.0])
        right3 = np.array([right[0], right[1], 0.0])
        best = None
        for lean in np.arange(0.0, 26.0, 2.0):
            d = body_front(zb - 40.0, zt + 40.0, lean) + clear + 6.0      # 6 mm for the walk (pelvis sway, drop)
            hands, palm, elbow = {}, {}, {}
            for s, sx in (("l", -1.0), ("r", 1.0)):
                if g == "side":                          # the forearm along the side face, elbow down: the fingers
                    c = fc - nrm * ins + latw * sx * (width / 2 + gap)    # run along the face, not into it
                    c[2] = zc
                    hands[s], palm[s] = c, tuple(-latw * sx)
                    elbow[s] = tuple(right3 * sx * 0.25 - fwd3 * 0.25 + np.array([0.0, 0.0, -1.0]))
                else:
                    c = fc - nrm * ins + latw * sx * min(width / 2 - 40.0, 190.0)
                    c[2] = zb - gap * 0.3
                    hands[s], palm[s], elbow[s] = c, (0.0, 0.0, 1.0), None
            org = np.array([fc[0], fc[1]]) + nh * d
            # the reach: each shoulder (upperarm01's head, turned with the lean about the hips, the pelvis 25 mm down) to
            # its hand, against 470 mm of the 520 mm arm (the walk's bob takes up to 50 mm more)
            worst = -1e9
            for s, sx in (("l", -1.0), ("r", 1.0)):
                yp, zp = HIP_PIVOT
                sy = yp + (15.2 - yp) * math.cos(math.radians(lean)) + (1407.0 - zp) * math.sin(math.radians(lean))
                sz = zp + (1407.0 - zp) * math.cos(math.radians(lean)) - 25.0
                loc = np.array([(hands[s][:2] - org) @ right, (hands[s][:2] - org) @ -nh, hands[s][2]])
                worst = max(worst, float(np.linalg.norm(loc - np.array([sx * 174.7, sy, sz]))) - 470.0)
            cand = dict(x=float(org[0]), y=float(org[1]), hd=hd, lean=float(lean),
                        hands={s: tuple(float(v) for v in hands[s]) for s in hands}, palm=palm, elbow=elbow,
                        grip={"l": 0.0, "r": 0.0} if g == "side" else {"l": 0.05, "r": 0.05}, bend={"l": True, "r": True},
                        look=tuple(float(v) for v in (R @ ((lo + hi) / 2) + t)), reach_mm=round(worst, 1),
                        front_mm=round(d, 1), end=e, kind=g)
            if best is None or worst < best["reach_mm"] - 1.0:
                best = cand
            if worst <= 0.0:
                best = cand
                break
        out.append(best)
    return out


def carry_check(person, lo, hi, M):
    """What a drawn pose does with a carried box (lo, hi in its frame, pose M): the dressed body's (arms and hands left
    out) nearest distance to it, mm (negative: inside), and the hands' and sleeves' deepest point inside it."""
    M = np.asarray(M, float)
    R, t = M[:3, :3], M[:3, 3]
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    order = person.order
    body, arms = [], []
    for part, (P, F) in person.posed().items():
        d = person.parts[part][0]
        n = len(d["P"])
        best, dom = np.zeros(n), np.zeros(n, int)
        for r, c, v in zip(d["rows"], d["cols"], d["vals"]):
            if v > best[r]:
                best[r], dom[r] = v, c
        arm = np.array([order[c].startswith(ARM_BONES) for c in dom]) | (part in ("glove", "forearm"))
        q = (P - t) @ R
        out_d = np.linalg.norm(np.maximum(np.maximum(lo - q, q - hi), 0.0), axis=1)
        in_d = np.minimum(q - lo, hi - q).min(1)
        sd = np.where(in_d > 0, -in_d, out_d)
        body.append(sd[~arm])
        arms.append(sd[arm])
    b, a = np.concatenate(body), np.concatenate(arms)
    return dict(body_clear_mm=round(float(b.min()), 1), hands_in_mm=round(float(max(0.0, -a.min())), 1))


# ================================================================================================ a look at it
def _preview():
    """Close-up stills: standing, mid-stride, pushing a cart, leaning in to reach, from the front, the side, the back and
    the face, plus one with a soda can for scale -> /tmp/robotbuild/people_*.png."""
    import sys
    sys.path.insert(0, str(HERE))
    import common
    import pvscene
    from PIL import Image
    out = Path(os.environ.get("ROBOTBUILD", "/tmp/robotbuild"))
    out.mkdir(parents=True, exist_ok=True)
    poses = {
        "stand": dict(lean=0.0, amp=0.0, phase=0.0, hands={"l": None, "r": None}, look=None),
        "walk": dict(lean=0.0, amp=1.0, phase=0.6 * math.pi, hands={"l": None, "r": None}, look=None),
        "push": dict(lean=20.0, amp=0.8, phase=1.1, hands={"l": (-215.0, 236.0, 849.0), "r": (215.0, 236.0, 849.0)},
                     look=None),
        "reach": dict(lean=30.0, amp=0.0, phase=0.0, hands={"l": (-120.0, 560.0, 1090.0), "r": (40.0, 620.0, 1010.0)},
                      look=(40.0, 700.0, 1000.0)),
    }
    cams = {"front": [(1500, 2600, 1500), (0, 0, 950), (0, 0, 1)], "side": [(2900, 300, 1400), (0, 150, 950), (0, 0, 1)],
            "back": [(-1300, -2600, 1700), (0, 0, 950), (0, 0, 1)], "face": [(250, 900, 1620), (0, 0, 1560), (0, 0, 1)]}
    pl = pvscene.plotter((640, 720))
    sc = pvscene.PVScene(pl)
    sc.add("floor", pv.Plane(center=(0, 0, -1), i_size=4000, j_size=4000), common.FLOOR, specular=0.0)
    can = pv.Cylinder(center=(420.0, 300.0, 61.0), direction=(0, 0, 1), radius=33.0, height=122.0, resolution=40)
    sc.add("soda can", can, "#c8102e", specular=0.6)
    p = Person(sc, "p")
    imgs = []
    for nm, kw in poses.items():
        p.set(**kw)
        row = [sc.render(cam, 30.0 if cn != "face" else 26.0) for cn, cam in cams.items()]
        path = out / f"people_{nm}.png"
        Image.fromarray(np.concatenate(row, axis=1)).save(path)
        imgs.append(path)
    print("\n".join(str(i) for i in imgs))


if __name__ == "__main__":
    _preview()
