"""OpenCAMLib drop-cutter and waterline runs for the machining review (issue #260, PR #266).

Runs in Python 3.11 (opencamlib 2023.1.11 has no wheel for the repo's Python 3.14), in a throw-away container:

  docker run --rm --memory=3g --cpus=1 --network none -v /tmp/mach-work:/work python:3.11-slim sh -c \
    "pip install -q --no-index /work/dl/*.whl && python /work/cam_ocl.py /work/cam/jobs.json"

(/work/dl holds the opencamlib-2023.1.11 and numpy-2.2.6 cp311 wheels; cam_sim.py writes jobs.json and copies this
file to /work.) For every job (one part STL, one setup direction, one tool) it rotates the part so the tool axis is
+Z, builds an ocl.STLSurf and runs ocl.BatchDropCutter over a regular XY grid twice: once with the cutter
(ocl.CylCutter, or ocl.BullCutter for a corner radius) and once with a cylinder the size of the tool holder. The tool
tip can go no lower than max(z_cutter, z_holder - stick-out), which is how a 3-axis CAM system checks holder
collisions. A job may also ask for waterline contours (ocl.Waterline) at a few Z levels, which are written as
toolpath polylines. Output: one .npz per job (grid, z_cl, z_holder, waterlines).
"""
import json
import math
import sys
import time

import numpy as np
import opencamlib as ocl

ROT = {   # part frame -> tool frame (tool axis = +Z of the tool frame, pointing from the tip to the spindle)
    "+z": np.eye(3),
    "-z": np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], float),
    "+x": np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], float),
    "-x": np.array([[0, -1, 0], [0, 0, 1], [-1, 0, 0]], float),
    "+y": np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float),
    "-y": np.array([[0, 0, -1], [1, 0, 0], [0, -1, 0]], float),
}


def read_stl(path):
    import struct
    data = open(path, "rb").read()
    if data[:5] == b"solid" and b"facet" in data[:400]:
        v = []
        for line in data.decode().splitlines():
            line = line.strip()
            if line.startswith("vertex"):
                v.append([float(t) for t in line.split()[1:4]])
        return np.array(v, float).reshape(-1, 3, 3)
    n = struct.unpack("<I", data[80:84])[0]
    arr = np.frombuffer(data[84:84 + n * 50], dtype=np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")]))
    return arr["v"].astype(float).reshape(-1, 3, 3)


def surf_from(tris):
    s = ocl.STLSurf()
    for t in tris:
        s.addTriangle(ocl.Triangle(ocl.Point(*t[0]), ocl.Point(*t[1]), ocl.Point(*t[2])))
    return s


def drop(surf, cutter, xs, ys, zmin):
    bdc = ocl.BatchDropCutter()
    bdc.setSTL(surf)
    bdc.setCutter(cutter)
    bdc.setThreads(1)
    for y in ys:
        for x in xs:
            bdc.appendPoint(ocl.CLPoint(float(x), float(y), zmin))
    bdc.run()
    cl = bdc.getCLPoints()
    z = np.array([p.z for p in cl], float)
    return z.reshape(len(ys), len(xs))


def main(jobfile):
    jobs = json.load(open(jobfile))
    cache = {}
    for job in jobs:
        t0 = time.time()
        R = ROT[job["dir"]]
        key = (job["stl"], job["dir"])
        if key not in cache:
            cache.clear()
            tris = read_stl(job["stl"]) @ R.T
            cache[key] = (tris, surf_from(tris))
        tris, surf = cache[key]
        lo, hi = tris.reshape(-1, 3).min(0), tris.reshape(-1, 3).max(0)
        st = job["step"]
        m = job["tool_d"] / 2 + 2 * st
        xs = np.arange(lo[0] - m, hi[0] + m + st, st)
        ys = np.arange(lo[1] - m, hi[1] + m + st, st)
        zmin = lo[2] - 1.0          # the floor the part sits on: the tool may go just past the part's far face
        if job.get("corner_r", 0) > 0:
            cut = ocl.BullCutter(job["tool_d"], job["corner_r"], 200.0)
        else:
            cut = ocl.CylCutter(job["tool_d"], 200.0)
        z_cl = drop(surf, cut, xs, ys, zmin)
        out = dict(xs=xs, ys=ys, z_cl=z_cl, zmin=zmin, R=R, lo=lo, hi=hi)
        if job.get("holder_d"):
            hs = max(st, 1.0)       # the holder only needs a coarse grid; resampled below
            xh = np.arange(xs[0], xs[-1] + hs, hs)
            yh = np.arange(ys[0], ys[-1] + hs, hs)
            zh = drop(surf, ocl.CylCutter(job["holder_d"], 500.0), xh, yh, zmin)
            ix = np.clip(np.round((xs - xh[0]) / hs).astype(int), 0, len(xh) - 1)
            iy = np.clip(np.round((ys - yh[0]) / hs).astype(int), 0, len(yh) - 1)
            out["z_holder"] = zh[np.ix_(iy, ix)]
        wl = []
        for zl in job.get("waterlines", []):
            w = ocl.Waterline()
            w.setSTL(surf)
            w.setCutter(ocl.CylCutter(job["tool_d"], 200.0))
            w.setZ(float(zl))
            w.setSampling(max(st, 0.5))
            w.run()
            for loop in w.getLoops():
                wl.append(np.array([[p.x, p.y, p.z] for p in loop], float))
        if wl:
            out["wl_n"] = np.array([len(a) for a in wl])
            out["wl"] = np.concatenate(wl)
        np.savez_compressed(job["out"], **out)
        print(f"{job['out'].split('/')[-1]}: {len(xs)}x{len(ys)} grid, {len(tris)} tris, {time.time() - t0:.1f} s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
