"""Records what every rendered frame draws, so that scene_audit.py can check the drawn frames themselves for collisions
(round 8, issue #260, PR #266).

Sterling's byu-vcl lesson 1 (notes/2026-11-26-byu-vcl-video-lessons.md): an audit that checked only the planned arm paths
reported zero and was wrong; the frames also draw people, bases, loads, failed attempts and scripted moves. So the audit
reads what the renderer actually drew, not what a planner said it would draw.

Switched on by the environment, so no renderer has to change:

    ROBOTBUILD_AUDIT=1            record every frame of every chapter rendered in this process
    ROBOTBUILD_AUDIT_EVERY=k      record every k-th frame only (default 1)

pvscene.PVScene.render() calls record() after apply(), with common.CURRENT (the open common.Chapter) for the frame number.
Per chapter it writes <frames>/<chapter>/audit/ (a slice of a chapter writes into its own part folder, like its frames):

    meshes.pkl   a stream of pickled records, one per mesh version: dict(key, name, V (n x 3 float32, the actor's own
                 coordinates, mm), F (m x 3 int32) or None when the faces equal those of the previous version of the
                 same actor (re-skinned people), F_key)
    frames.pkl   a stream of pickled records, one per recorded frame: dict(n, changed={actor: (mesh_key, M 4x4 float32,
                 opacity, visible)}, removed=[actors]) -- only what changed since this chapter's previous record, so the
                 state at frame n is the replay of every record up to n.

An actor's mesh version changes when its mapper's input object or that object's VTK modification time changes (people
are re-skinned in place every frame). Nothing here changes what is drawn.
"""
from __future__ import annotations

import os
import pickle

import numpy as np

EVERY = max(1, int(os.environ.get("ROBOTBUILD_AUDIT_EVERY", "1") or 1))


def enabled():
    return os.environ.get("ROBOTBUILD_AUDIT", "") not in ("", "0")


class _ChapterRec:
    def __init__(self, folder):
        self.dir = folder / "audit"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.fm = open(self.dir / "meshes.pkl", "wb")
        self.ff = open(self.dir / "frames.pkl", "wb")
        self.ver = {}        # actor -> (input id, mtime) of its last stored mesh
        self.key = {}        # actor -> mesh key of its last stored mesh
        self.fkey = {}       # actor -> (n_faces, faces hash) last stored
        self.sent = {}       # actor -> (mesh key, matrix bytes, opacity, visible) last written
        self.last_n = -1
        self.count = 0

    def close(self):
        for f in (self.fm, self.ff):
            try:
                f.close()
            except Exception:
                pass


_RECS = {}


def _faces(poly):
    from vtk.util.numpy_support import vtk_to_numpy
    cells = poly.GetPolys()
    if cells is None or cells.GetNumberOfCells() == 0:
        return np.zeros((0, 3), np.int32)
    try:
        off = vtk_to_numpy(cells.GetOffsetsArray())
        con = vtk_to_numpy(cells.GetConnectivityArray())
        sizes = np.diff(off)
        if len(sizes) and np.all(sizes == 3):
            return con.reshape(-1, 3).astype(np.int32)
        tris = []
        for i in range(len(sizes)):          # fan-triangulate the rare quads and polygons
            ids = con[off[i]:off[i + 1]]
            for k in range(1, len(ids) - 1):
                tris.append((ids[0], ids[k], ids[k + 1]))
        return np.asarray(tris, np.int32).reshape(-1, 3)
    except Exception:
        arr = vtk_to_numpy(cells.GetData())
        out, i = [], 0
        while i < len(arr):
            k = int(arr[i])
            ids = arr[i + 1:i + 1 + k]
            for j in range(1, k - 1):
                out.append((ids[0], ids[j], ids[j + 1]))
            i += k + 1
        return np.asarray(out, np.int32).reshape(-1, 3)


def record(scene, chapter):
    """Called by PVScene.render() after apply(). `chapter` is common.CURRENT (or None: nothing is recorded)."""
    if chapter is None or not enabled():
        return
    n = int(getattr(chapter, "n", 0))
    if n % EVERY:
        return
    folder = chapter.dir
    rec = _RECS.get(str(folder))
    if rec is None:
        rec = _RECS[str(folder)] = _ChapterRec(folder)
    if n == rec.last_n:                      # a second render of the same frame (an inset): the first one counts
        return
    rec.last_n = n
    from vtk.util.numpy_support import vtk_to_numpy
    changed = {}
    cache = {}
    for name, actor in scene.actors.items():
        g = scene.group_of.get(name, "static")
        if g not in cache:
            cache[g] = np.asarray(scene.world(g), np.float32)
        M = cache[g]
        a = float(scene.alpha.get(name, 1.0))
        vis = a > 0.02
        opac = float(min(1.0, scene.base_alpha.get(name, 1.0) * a))
        mapper = actor.GetMapper()
        poly = mapper.GetInput() if mapper is not None else None
        if poly is None or poly.GetNumberOfPoints() == 0:
            continue
        ver = (id(poly), int(poly.GetMTime()))
        if rec.ver.get(name) != ver and vis:
            V = vtk_to_numpy(poly.GetPoints().GetData()).astype(np.float32)
            F = _faces(poly)
            fk = (len(F), hash(F[: min(len(F), 2000)].tobytes()))
            same_f = rec.fkey.get(name) == fk
            key = f"{name}#{rec.count}"
            rec.count += 1
            pickle.dump(dict(key=key, name=name, V=V, F=None if same_f else F, F_key=fk), rec.fm, protocol=4)
            rec.ver[name], rec.key[name], rec.fkey[name] = ver, key, fk
        key = rec.key.get(name)
        if key is None:                      # never visible yet: nothing to check
            continue
        sig = (key, M.tobytes(), round(opac, 3), vis)
        if rec.sent.get(name) != sig:
            changed[name] = (key, M, opac, vis)
            rec.sent[name] = sig
    removed = [nm for nm in list(rec.sent) if nm not in scene.actors]
    for nm in removed:
        rec.sent.pop(nm, None)
        rec.ver.pop(nm, None)
        rec.key.pop(nm, None)
    pickle.dump(dict(n=n, changed=changed, removed=removed), rec.ff, protocol=4)
    if n % 50 == 0:
        rec.fm.flush()
        rec.ff.flush()


def close(chapter):
    rec = _RECS.pop(str(getattr(chapter, "dir", "")), None)
    if rec is not None:
        rec.close()
