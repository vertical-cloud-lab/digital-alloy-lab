"""Meshes for the fast-track progression video (#260, PR 294): ft_model's parts tessellated once per state, and the room.

Everything drawn is a triangle mesh in mm, in ft_model's frame (origin at the centre of the substrate's top at the start of a
build, +X the recoat direction, +Y to the back, +Z up). The same triangles are drawn by render.py and checked by plan.py
and audit.py, so what the audit checks is what the video shows.

    /tmp/venv/bin/python desktop-lpbf/fast-track/video/scene.py      # builds the mesh cache (/tmp/ft-video/cache)
"""
from __future__ import annotations

import hashlib
import math
import os
import pathlib
import pickle
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
FT = HERE.parent
REPO = FT.parents[1]
SCRATCH = pathlib.Path(os.environ.get("FT_VIDEO", "/tmp/ft-video"))
CACHE = SCRATCH / "cache"
# The video shows the round-1 model: ft_model.py, ft_progression.py, ft_checks.py, fast_track.py, parts.csv and
# lpbf_model.py are read
# from git revision MODEL_REV (d117ba8: ft_model.py as of 91c1931, X-LSQ075B recoater, lens on the plate axis), written
# once under SCRATCH/pin-<rev>/ in the repo's layout, so the CAD v2 model and round 2's schedule and prices on the branch
# change nothing drawn. FT_MODEL_REV="" uses the working tree instead.
MODEL_REV = os.environ.get("FT_MODEL_REV", "d117ba8")
PIN_FILES = ("desktop-lpbf/fast-track/cad/ft_model.py", "desktop-lpbf/fast-track/cad/ft_progression.py",
             "desktop-lpbf/fast-track/cad/ft_checks.py", "desktop-lpbf/fast-track/fast_track.py",
             "desktop-lpbf/fast-track/parts.csv", "desktop-lpbf/cad/lpbf_model.py")


def _pin(rev):
    import subprocess
    root = SCRATCH / f"pin-{rev}"
    for rel in PIN_FILES:
        p = root / rel
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            out = subprocess.run(["git", "-C", str(REPO), "show", f"{rev}:{rel}"], check=True, capture_output=True).stdout
            p.write_bytes(out)
    return root


MROOT = _pin(MODEL_REV) if MODEL_REV else REPO
FTM = MROOT / "desktop-lpbf" / "fast-track"          # where ft_model, ft_progression, fast_track and parts.csv come from
for d in (FT / "cad", FT, FT.parent / "cad", FTM / "cad", FTM, FTM.parent / "cad"):
    sys.path.insert(0, str(d))                        # the pinned files first; the working tree for anything else
TOL, ANG = 0.25, 0.3                      # tessellation: chord tolerance (mm), angular tolerance (rad)


def model():
    import ft_model as M
    return M


def model_sig():
    """A hash of the model's source, so the cache follows the CAD worker's changes."""
    h = hashlib.blake2b(digest_size=6)
    for p in (FTM / "cad" / "ft_model.py", FTM.parent / "cad" / "lpbf_model.py"):
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()


def tess(shape):
    vs, ts = shape.tessellate(TOL, ANG)
    if not ts:
        return None
    V = np.array([(v.x, v.y, v.z) for v in vs], np.float32)
    F = np.array(ts, np.int32).reshape(-1, 3)
    return V, F


def state_meshes(state):
    """{name: dict(V, F, color, opacity, pid, sub, group)} for ft_model.build(state) (plate at the start of a build, hopper
    at the right end of its travel). Names are unique within a state (a repeat gets ' #2')."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{state}-{model_sig()}.pkl"
    if path.exists():
        return pickle.loads(path.read_bytes())
    M = model()
    out = {}
    for p in M.build(state):
        m = tess(p.shape)
        if m is None:
            continue
        name = p.name
        k = 2
        while name in out:
            name = f"{p.name} #{k}"
            k += 1
        out[name] = dict(V=m[0], F=m[1], color=p.color, opacity=float(p.opacity), pid=p.pid, sub=p.sub, group=p.group)
    path.write_bytes(pickle.dumps(out, protocol=4))
    return out


# ------------------------------------------------------------------------------------------------ the room (our context)
def _box(x0, x1, y0, y1, z0, z1):
    V = np.array([[x, y, z] for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)], np.float32)
    F = np.array([[0, 2, 1], [1, 2, 3], [4, 5, 6], [5, 7, 6], [0, 1, 4], [1, 5, 4], [2, 6, 3], [3, 6, 7],
                  [0, 4, 2], [2, 4, 6], [1, 3, 5], [3, 7, 5]], np.int32)
    return V, F


def bench_z():
    return float(model().P["bench_z"])


BENCH_H = 900.0                            # bench top above the floor (a lab bench, estimate)


def floor_z():
    return bench_z() - BENCH_H


def room():
    """{name: dict(V, F, color, opacity)}: floor, back wall, the bench's legs and shelf. The bench top is ft_model's."""
    zb = bench_z()
    zf = floor_z()
    out = {}
    out["Room: floor"] = dict(mesh=_box(-2600, 2200, -2400, 2400, zf - 20, zf), color="#d9dcdf", opacity=1.0)
    out["Room: back wall"] = dict(mesh=_box(-2600, 2200, 2400, 2420, zf, zf + 2700), color="#eef0f2", opacity=1.0)
    legs = []
    for x in (-830, 570):
        for y in (-330, 400):
            legs.append(_box(x - 25, x + 25, y - 25, y + 25, zf, zb - 40))
    out["Room: bench legs"] = dict(mesh=_merge(legs), color="#6d7378", opacity=1.0)
    out["Room: bench shelf"] = dict(mesh=_box(-860, 600, -330, 400, zf + 140, zf + 160), color="#b7a27a", opacity=1.0)
    return {k: dict(V=v["mesh"][0], F=v["mesh"][1], color=v["color"], opacity=v["opacity"], pid="", sub="room", group="")
            for k, v in out.items()}


def _merge(ms):
    Vs, Fs, n = [], [], 0
    for V, F in ms:
        Vs.append(V)
        Fs.append(F + n)
        n += len(V)
    return np.vstack(Vs), np.vstack(Fs)


def person_meshes(at, facing=(0.0, -1.0, 0.0)):
    """PR 266's MakeHuman figure (render_scale.person), standing still for scale: [(name, V, F, colour)]."""
    import render_scale as RS
    out = []
    for k, (m, col) in enumerate(RS.person(at=at, facing=facing)):
        tri = m.triangulate()
        F = np.asarray(tri.faces).reshape(-1, 4)[:, 1:].astype(np.int32)
        out.append((f"Person for scale/{k}", np.asarray(tri.points, np.float32), F, col))
    return out


def parks():
    """The hopper's two beam-clear parks (ft_checks.travel_needed)."""
    import ft_checks
    t = ft_checks.travel_needed()
    return float(t["left_park"]), float(t["right_park"])


if __name__ == "__main__":
    import time
    for s in model().STATES:
        t0 = time.time()
        m = state_meshes(s)
        print(f"{s}: {len(m)} parts, {sum(len(v['F']) for v in m.values())} triangles, {time.time() - t0:.1f} s")
    print("parks", parks())
