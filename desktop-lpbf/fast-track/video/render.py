"""Render one chapter of the fast-track video: 3-D frames (1440 x 1080 JPEG) and one line of metadata per frame.

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/tools/capmem 3 /tmp/venv/bin/python desktop-lpbf/fast-track/video/render.py N
    ... render.py N --plan        # plan and check the chapter, print its paths and the end-state check; no frames
    ... render.py N --stills 6    # only six frames spread over the chapter (for a contact sheet)

Writes /tmp/ft-video/frames/chN/: NNNNN.jpg (only frames that differ from the one before), meta.jsonl (every frame: time,
shot, camera, which image to show, the overlay data), plan.json (every insertion, removal and move with its checked path),
and for the audit audit.pkl (every drawn frame's actors: what is visible, where, at which scale) and meshes.pkl.
"""
from __future__ import annotations

import hashlib
import json
import os
import pickle
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import engine as E  # noqa: E402
import scene as S  # noqa: E402
import story as ST  # noqa: E402

OUT = S.SCRATCH / "frames"
MAT = dict(smooth_shading=True, specular=0.3, specular_power=18, ambient=0.22, diffuse=0.85)
HALF = 2


def hex2rgb(h):
    return tuple(int(h[k:k + 2], 16) / 255 for k in (1, 3, 5))


def polydata(V, F):
    import pyvista as pv
    pd = pv.PolyData(np.asarray(V, float), np.c_[np.full(len(F), 3), F].ravel().astype(np.int64))
    return pd.compute_normals(split_vertices=True, feature_angle=35, auto_orient_normals=False)


def lines_pd(segs):
    import pyvista as pv
    segs = np.asarray(segs, float).reshape(-1, 2, 3)
    n = len(segs)
    pts = segs.reshape(-1, 3)
    cells = np.c_[np.full(n, 2), np.arange(0, 2 * n, 2), np.arange(1, 2 * n, 2)].ravel()
    return pv.PolyData(pts, lines=cells)


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return o


def plan_report(s):
    tl = s.tl
    rows = []
    for nt in tl.notes:
        rows.append(jsonable(nt))
    return rows


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", type=int, nargs="+")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--stills", type=int, default=0)
    ap.add_argument("--every", type=int, default=1)
    a = ap.parse_args()
    chs = a.chapter
    for c in chs:
        a.chapter = c
        one(a)
    import resource
    print(f"peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB", flush=True)


def one(a):
    t_start = time.time()
    s = ST.build(a.chapter)
    tl = s.tl
    T = tl.t
    nfr = int(round(T * E.FPS))
    d = OUT / f"ch{a.chapter}"
    d.mkdir(parents=True, exist_ok=True)
    probs = ST.verify_end(s) if a.chapter not in (0,) else []
    unpl = s.unplaced() if a.chapter in (1, 2, 3, 4, 6) else []
    rep = dict(chapter=a.chapter, title=tl.title, seconds=round(T, 2), frames=nfr, plan=plan_report(s),
               end_state_problems=probs, never_placed=unpl,
               shots=[(round(x[0], 2), round(x[1], 2), x[3]) for x in tl.shots],
               planning_s=round(time.time() - t_start, 1))
    (d / "plan.json").write_text(json.dumps(rep, indent=1))
    print(f"chapter {a.chapter} '{tl.title}': {T:.1f} s, {nfr} frames, planned in {time.time() - t_start:.1f} s", flush=True)
    for nt in tl.notes:
        if "collision" in nt:
            print("  COLLISION", nt["names"][:2], nt["collision"], flush=True)
    for nt in tl.notes:
        if "how" in nt:
            print(f"  {nt['t']:6.1f}s {nt['what']:14s} {nt['how']:28s} {nt['seconds']:5.1f}s  {nt['names'][0][:60]}"
                  + (f" (+{len(nt['names']) - 1})" if len(nt['names']) > 1 else ""), flush=True)
    for p in probs:
        print("  END STATE:", p, flush=True)
    for p in unpl:
        print("  NEVER PLACED:", p, flush=True)
    shots = [x for x in tl.shots if x[1] is not None and x[1] > x[0]]
    print("  shots:", ", ".join(f"{x[3]} {x[1] - x[0]:.1f}s" for x in shots), flush=True)
    if a.plan:
        return
    render(s, d, nfr, stills=a.stills, every=a.every)
    print(f"chapter {a.chapter}: done in {time.time() - t_start:.0f} s", flush=True)


def render(s, d, nfr, stills=0, every=1):
    import pyvista as pv
    from PIL import Image
    pv.OFF_SCREEN = True
    tl = s.tl
    for f in d.glob("*.jpg"):
        f.unlink()
    pl = pv.Plotter(off_screen=True, window_size=(E.W3, E.H3), lighting="three lights")
    pl.set_background("#f7f9fb", top="#dce5ee")
    pl.enable_anti_aliasing("fxaa")
    pl.enable_depth_peeling(number_of_peels=3)
    acts, edges = {}, {}
    for n, a in tl.actors.items():
        pd = polydata(a.V, a.F)
        acts[n] = pl.add_mesh(pd, color=hex2rgb(a.color), opacity=a.opacity, **MAT)
        acts[n].SetVisibility(False)
        if a.edges and a.opacity > 0.3 and a.kind == "part":
            fe = pd.extract_feature_edges(feature_angle=40, boundary_edges=False, non_manifold_edges=False,
                                          manifold_edges=False)
            if fe.n_points:
                edges[n] = pl.add_mesh(fe, color=(0.12, 0.13, 0.15), line_width=1.0, opacity=0.45)
                edges[n].SetVisibility(False)
    fxa, fxkey = {}, {}
    # audit recording
    arec = open(d / "audit.pkl", "wb")
    meshes = {n: dict(V=a.V, F=a.F, label=a.label, opacity=a.opacity, kind=a.kind, solid=a.solid)
              for n, a in tl.actors.items()}
    pickle.dump(meshes, open(d / "meshes.pkl", "wb"), protocol=4)
    meta = open(d / "meta.jsonl", "w")
    last_sig, last_img, last_csig = None, -1, None
    prev_pose = {}
    prev_fx = {}
    which = range(0, nfr, every)
    if stills:
        which = sorted(set(int(x) for x in np.linspace(0, nfr - 1, stills)))
    t0 = time.time()
    nr = 0
    for n in which:
        t = n / E.FPS
        st = tl.state(t)
        cam, shot = tl.cam_at(t)
        sig = []
        # actors
        for name, a in tl.actors.items():
            x = st[name]
            vis = bool(x["vis"])
            off = x["off"] + x["stage"]
            sc = x.get("scale")
            mo = x.get("morph")
            key = (vis, tuple(np.round(off, 4)), None if sc is None else tuple(np.round(sc, 5)), round(x["op"], 3), x["color"],
                   None if mo is None else mo[0])
            sig.append(key)
            act = acts[name]
            if prev_pose.get(name) != key:
                act.SetVisibility(vis)
                act.SetPosition(*map(float, off))
                if sc is not None:
                    act.SetOrigin(0.0, 0.0, float(sc[3]))
                    act.SetScale(float(sc[0]), float(sc[1]), float(sc[2]))
                else:
                    act.SetScale(1.0, 1.0, 1.0)
                act.GetProperty().SetOpacity(float(x["op"]))
                act.GetProperty().SetColor(*hex2rgb(x["color"]))
                if mo is not None and (prev_pose.get(name) is None or prev_pose[name][5] != mo[0]):
                    pd = polydata(mo[1], a.F)
                    act.GetMapper().SetInputData(pd)
                    if name in edges:
                        fe = pd.extract_feature_edges(feature_angle=40, boundary_edges=False, non_manifold_edges=False,
                                                      manifold_edges=False)
                        edges[name].GetMapper().SetInputData(fe)
                if name in edges:
                    e = edges[name]
                    e.SetVisibility(vis and x["op"] > 0.3)
                    e.SetPosition(*map(float, off))
                    if sc is not None:
                        e.SetOrigin(0.0, 0.0, float(sc[3]))
                        e.SetScale(float(sc[0]), float(sc[1]), float(sc[2]))
                    else:
                        e.SetScale(1.0, 1.0, 1.0)
                prev_pose[name] = key
        # effects
        fx = st["_fx"]
        for fname in list(fxa):
            if fname not in fx and fxa[fname].GetVisibility():
                fxa[fname].SetVisibility(False)
                fxkey[fname] = None
        for fname, f in fx.items():
            if f["kind"] == "lines":
                k = ("L", len(f["data"]), tuple(np.round(f["data"][-1].ravel(), 3)), f["color"])
            else:
                k = ("M", f.get("key"), f["color"], f["opacity"])
            sig.append((fname, k))
            if fxkey.get(fname) == k:
                continue
            fxkey[fname] = k
            if f["kind"] == "lines":
                pd = lines_pd(f["data"])
            else:
                pd = polydata(*f["data"])
            if fname not in fxa:
                if f["kind"] == "lines":
                    fxa[fname] = pl.add_mesh(pd, color=hex2rgb(f["color"]), line_width=f.get("width", 2.0), lighting=False)
                else:
                    fxa[fname] = pl.add_mesh(pd, color=hex2rgb(f["color"]), opacity=f["opacity"], **MAT)
            else:
                fxa[fname].GetMapper().SetInputData(pd)
                fxa[fname].GetProperty().SetColor(*hex2rgb(f["color"]))
                if f["kind"] != "lines":
                    fxa[fname].GetProperty().SetOpacity(f["opacity"])
            fxa[fname].SetVisibility(True)
        # camera
        csig = (tuple(np.round(cam.pos, 3)), tuple(np.round(cam.focal, 3)), round(cam.angle, 4))
        sig.append(csig)
        sig = hashlib.blake2b(repr(sig).encode(), digest_size=10).hexdigest()
        # motion is drawn at FPS / HALF new images a second (each shown HALF times); a cut is drawn at once
        rendered = sig != last_sig and (n % HALF == 0 or csig != last_csig or last_img < 0)
        if rendered:
            pl.camera.position = cam.pos
            pl.camera.focal_point = cam.focal
            pl.camera.up = cam.up
            pl.camera.view_angle = cam.angle
            pl.camera.clipping_range = (20.0, 12000.0)
            pl.render()                                  # screenshot() alone only renders the first time
            img = pl.screenshot(return_img=True)
            Image.fromarray(img).save(d / f"{n:05d}.jpg", quality=92)
            last_sig, last_img, last_csig = sig, n, csig
            nr += 1
        # audit record (only for drawn images): every actor whose drawn state changed, and the solid effects
        if not rendered:
            ov = tl.overlay_at(t)
            meta.write(json.dumps(jsonable(dict(n=n, t=round(t, 4), shot=shot, img=last_img, rendered=False,
                                                cam=[list(cam.pos), list(cam.focal), cam.angle], ov=ov))) + "\n")
            continue
        rec = dict(n=n, changed={}, fx={})
        for name, a in tl.actors.items():
            x = st[name]
            k = (bool(x["vis"]), tuple(np.round(x["off"] + x["stage"], 4)),
                 None if x.get("scale") is None else tuple(np.round(x["scale"], 5)),
                 None if x.get("morph") is None else x["morph"][0])
            if prev_fx.get(name) != k:
                rec["changed"][name] = dict(vis=k[0], off=k[1], scale=k[2], morph=k[3],
                                            V=None if x.get("morph") is None else np.asarray(x["morph"][1], np.float32))
                prev_fx[name] = k
        for fname, f in fx.items():
            if f.get("solid"):
                rec["fx"][fname] = (f.get("key"), f["data"] if prev_fx.get("fx:" + fname) != f.get("key") else None,
                                    f["opacity"])
                prev_fx["fx:" + fname] = f.get("key")
        pickle.dump(rec, arec, protocol=4)
        ov = tl.overlay_at(t)
        meta.write(json.dumps(jsonable(dict(n=n, t=round(t, 4), shot=shot, img=last_img, rendered=rendered,
                                            cam=[list(cam.pos), list(cam.focal), cam.angle], ov=ov))) + "\n")
        if n % 150 == 0:
            el = time.time() - t0
            print(f"  frame {n}/{nfr}  rendered {nr}  {el:.0f} s", flush=True)
    meta.close()
    arec.close()
    pl.close()
    print(f"  {nr} frames rendered of {len(which)}", flush=True)


if __name__ == "__main__":
    main()
