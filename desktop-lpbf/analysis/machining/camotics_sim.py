"""Simulate the FreeCAD G-code for the chamber frame and floor plate in CAMotics, and compare the result with the CAD.

What it checks (issue #260, PR #266)
    freecad_cam.py posts one LinuxCNC program per setup (frame A/B/C, floor A/B). This script cuts each program in
    CAMotics 1.2.0's command-line simulator (camsim) with freecad_cam.TOOLS' tool sizes, chains the setups (the material
    left by A is the stock for B, and so on, in the part frame), and compares the result with the model:
      * gouges: material the part keeps that a setup removed;
      * leftover: material still there that the part does not have (unprogrammed features, missed cuts); both on a
        voxel grid (--res, 0.5 mm), counted only deeper than --min-depth (1 mm) from the model's surface (voxel noise);
      * loose pieces: material no longer joined to the part (slugs), per setup and at the end;
      * drill points: CAMotics has no drill shape (drills are flat cylinders here), so the 118 deg point's shortfall
        at full diameter is worked out from the programmed depths;
      * rapids (G0) through stock: every G0 move is swept against the in-process stock (the chained CAMotics result of
        the earlier setups, minus what this setup has cut so far, tracked as a z-map);
      * cycle time: CAMotics' own move timing (distance / F; rapids at the 10 m/min hard-coded in its src/gcode/Move.cpp)
        against FreeCAD's estimate and the recount in freecad_cam.json.
    Results: desktop-lpbf/analysis/out/machining/camotics/camotics_sim.json and PNGs; STLs stay in $CAMOTICS_WORK.

Why Docker (the install error, 2026-11-22)
    CAMotics' last release is 1.2.0 (2019). Its camotics_1.2.0_amd64.deb declares "libv8-3.14.5 | libv8-dev", which
    Ubuntu 26.04 satisfies through libnode-dev, so apt would install it; but the binaries are linked against
    libv8.so.3.14.5 (V8 3.14) and OpenSSL 1.1 (libssl.so.1.1, libcrypto.so.1.1), which 26.04 does not have:
        camsim: error while loading shared libraries: libv8.so.3.14.5: cannot open shared object file
    The fix is a container on Ubuntu 18.04, the newest LTS with V8 3.14 (gone after 19.10) and OpenSSL 1.1, plus
    libqt5websockets5, which the .deb needs but does not declare (without it: "libQt5WebSockets.so.5: cannot open
    shared object file"). camsim needs no display. Build once (the Dockerfile checks the .deb's sha256):
        docker build -t camotics:1.2.0 -f desktop-lpbf/analysis/machining/camotics.Dockerfile desktop-lpbf/analysis/machining

CAMotics 1.2.0's limits, and what this script does about them
    * G83 (peck drilling) is not implemented: camsim logs "Not implemented: G83" and skips the hole. Every canned cycle
      is expanded here into G0/G1 moves the way LinuxCNC runs it (pecks back to R, rapid down to 0.254 mm above the last
      depth), so the holes are cut and timed.
    * The tool starts at (0, 0, 0), inside the blank. A "G92 Z1000" after the preamble puts the start 1000 mm above work
      zero; the workpiece is given 1000 mm lower and the result is shifted back.
    * No A axis: camsim logs an A move as an XYZ move to the same point and goes on cutting as if A were 0 (tested on
      2026-11-25 with --a-axis-test: a hole programmed after G0 A90 went in from the top face, not a side face). So
      frame setup C, the four walls on the rotary, is simulated per A index: each index's block is posted as its own
      program in the machine frame at that index, cut on the blank turned into that frame, and turned back into the
      part frame (rot_of). The joined Haas program (gcode/frame_C_haas.nc) is those four blocks with the A moves between.
    * Memory: a full frame blank at 0.5 mm runs out of a 3 GB container, so each blank is cut in z slabs (each slab is
      its own CAMotics run; slabs the tool never reaches are not run, they are uncut blank). $CAMOTICS_MEM (default 3g)
      caps the container and $CAMOTICS_SLAB (default 32 mm) sets the slab: 2g with 16 mm slabs ran on 2026-11-23 and
      gave the same result. Under /tmp/capmem or /tmp/heavy (a systemd scope that drops the docker group), wrap the
      command in sg docker -c '...'.

Run (after freecad_cam.py has written /tmp/chamber-cam/gcode/*.ngc; frame.stl and floor.stl are inventory.py's STLs
of the same model, copied next to frame.brep and floor.brep):
    /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/machining/camotics_sim.py [--res 0.5] [--skip-sim]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import pathlib
import re
import subprocess
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import freecad_cam as FC  # noqa: E402  (plain-Python parts only: TOOLS, SETUPS, blanks)

IN_DIR = pathlib.Path(os.environ.get("CHAMBER_CAM_IN", "/tmp/chamber-cam"))
WORK = pathlib.Path(os.environ.get("CAMOTICS_WORK", "/tmp/cam-sim"))
OUT = HERE.parent / "out" / "machining" / "camotics"
IMAGE = os.environ.get("CAMOTICS_IMAGE", "camotics:1.2.0")   # the camotics.Dockerfile build
SHIFT = 1000.0             # G92 offset: the simulated start point is this far above work zero
CAMOTICS_RAPID = 10000.0   # mm/min, CAMotics 1.2.0 src/gcode/Move.cpp ("feed = 10000; // TODO FIXME")
PECK_BACKOFF = 0.254       # mm, LinuxCNC's G83 clearance above the last peck
SLAB = float(os.environ.get("CAMOTICS_SLAB", "32"))  # mm, z thickness of one CAMotics run (16 fits a 2 GB container)
DOCKER_MEM = os.environ.get("CAMOTICS_MEM", "3g")      # container memory cap (the shared runner asks for 2g)
DOCKER_CPUS = os.environ.get("CAMOTICS_CPUS", "1.5")   # container CPU cap (the shared runner, 2026-11-25)

L, W = 317.5, 228.6        # blank in x, y (both parts), centred on the part origin
BLANK_Z = {"frame": FC.FRAME_BLANK[2:], "floor": FC.FLOOR_BLANK[2:]}
CORE = (274.0, 184.0, 7.0)  # frame: the waterjet slug (L, W, corner R) out before milling (dfm.py, cam_sim.py)
GRID_LO = {"frame": (-159.0, -114.5, -5.5), "floor": (-159.0, -114.5, -23.0)}
GRID_HI = {"frame": (159.0, 114.5, 122.0), "floor": (159.0, 114.5, 3.0)}


# --- setup frames ---------------------------------------------------------------------------------
def rot_of(su):
    """the setup's model -> setup rotation, a signed permutation matrix (freecad_cam.rot_matrix): setups A and B turn
    the part about x (0 or 180 deg); setup C's A indexes (frame_C0 ... frame_C270) are in the machine frame at that
    index, A along X. CAMotics 1.2.0 cuts in X, Y, Z only (its tool path ignores A), so each index is simulated as its
    own 3-axis program on the blank turned into that index's frame, and the result is turned back into the part frame."""
    return np.array(FC.rot_matrix(su), dtype=float)


def perm_sign(rot):
    """setup axis i = sign[i] * part axis perm[i]"""
    perm = [int(np.argmax(np.abs(rot[i]))) for i in range(3)]
    return perm, [int(np.sign(rot[i][perm[i]])) for i in range(3)]


def setup_view(arr, rot):
    """a part-frame voxel array seen in the setup frame (a numpy view: writing to it writes the part array)"""
    perm, sign = perm_sign(rot)
    v = np.transpose(arr, perm)
    return v[tuple(slice(None, None, -1) if sg < 0 else slice(None) for sg in sign)]


def setup_coords(grid, rot):
    """voxel centre coordinates along the setup axes of setup_view (ascending)"""
    perm, sign = perm_sign(rot)
    return [grid.c[perm[i]] if sign[i] > 0 else -grid.c[perm[i]][::-1] for i in range(3)]


def rot_label(rot):
    return [[int(v) for v in r] for r in np.asarray(rot)]


def to_setup(p, rot):
    """part frame -> setup frame"""
    return np.asarray(p, float) @ np.asarray(rot, float).T


def to_part(p, rot):
    return np.asarray(p, float) @ np.asarray(rot, float)


def blank_box_setup(part, rot):
    z0, z1 = BLANK_Z[part]
    c = np.array([[sx * L / 2, sy * W / 2, z] for sx in (-1, 1) for sy in (-1, 1) for z in (z0, z1)])
    s = to_setup(c, rot)
    return s.min(0), s.max(0)


# --- G-code: parse, expand canned cycles, linearise -------------------------------------------------
WORD = re.compile(r"([A-Z])([-+]?\d*\.?\d+)")


def clean_comment(raw):
    """one comment per line, with any nested parentheses turned into brackets (G-code comments don't nest)"""
    a, b = raw.find("("), raw.rfind(")")
    if a < 0 or b <= a:
        return raw
    inner = raw[a + 1:b].replace("(", "[").replace(")", "]")
    return raw[:a] + "(" + inner + ")" + raw[b + 1:]


def expand(text):
    """Returns (camotics_text, moves). Canned cycles (G81/G83) become G0/G1 lines; G92 Z<SHIFT> goes after G21.
    moves: dicts with op, tool, rapid, p0, p1 (work coords), feed, arc=(cx, cy, cw) or None, line (in the CAMotics
    text), src_line (in the posted .ngc; a canned cycle's moves all carry its line)."""
    out, moves, nested = [], [], []
    pos = [0.0, 0.0, None]  # z unknown until the first Z word (the tool starts at the tool-change height)
    feed, tool, op, motion, cycle, rmode = None, None, None, None, None, 98
    cyc = {}

    def emit_move(rapid, tgt, arc=None):
        nonlocal pos
        p0 = list(pos)
        if p0[2] is None:  # first move: comes down from the tool-change height
            p0[2] = max(tgt[2], 300.0)
        if tgt != p0:
            moves.append(dict(op=op, tool=tool, rapid=rapid, p0=tuple(p0), p1=tuple(tgt), feed=feed, arc=arc,
                              line=len(out), src_line=src_no))
        pos = list(tgt)

    src_no = 0
    for src_no, raw in enumerate(text.splitlines(), 1):  # src_no: the line in the posted .ngc
        m = re.search(r"\(begin operation: (.*)\)", raw)
        if m:
            op = m.group(1)
        line = re.sub(r"\(.*?\)", "", raw).strip().upper()
        words = WORD.findall(line)
        g = [float(v) for k, v in words if k == "G"]
        p = {k: float(v) for k, v in words if k not in "GM"}
        mcodes = [int(float(v)) for k, v in words if k == "M"]
        if 6 in mcodes and "T" in p:
            tool = int(p["T"])
        if "F" in p:
            feed = p["F"]
        new_cycle = None
        for c in g:
            if c in (0, 1, 2, 3):
                motion, cycle = int(c), None
            elif c in (81, 83):
                new_cycle = int(c)
            elif c == 80:
                cycle = None
            elif c in (98, 99):
                rmode = int(c)
        if new_cycle is not None:
            cycle = new_cycle
            cyc = dict(init_z=pos[2])
        has_xyz = any(k in p for k in "XYZ")
        if cycle is not None and (has_xyz or "R" in p):
            for k in ("R", "Q", "Z"):
                if k in p:
                    cyc[k] = p[k]
            x, y = p.get("X", pos[0]), p.get("Y", pos[1])
            r, zb, q = cyc["R"], cyc["Z"], cyc.get("Q") if cycle == 83 else None
            init_z = cyc["init_z"] if cyc.get("init_z") is not None else r
            zclear = max(init_z, r) if rmode == 98 else r
            lines = []
            if pos[2] < r:
                lines.append((True, [pos[0], pos[1], r]))
            lines.append((True, [x, y, pos[2] if pos[2] >= r else r]))
            lines.append((True, [x, y, r]))
            if q:
                depth = r
                while depth > zb + 1e-9:
                    nxt = max(depth - q, zb)
                    lines.append((False, [x, y, nxt]))
                    depth = nxt
                    if depth > zb + 1e-9:
                        lines.append((True, [x, y, r]))
                        lines.append((True, [x, y, depth + PECK_BACKOFF]))
            else:
                lines.append((False, [x, y, zb]))
            lines.append((True, [x, y, zclear]))
            out.append("(camotics_sim: G%d expanded) " % cycle)
            for rapid, tgt in lines:
                out.append("G%d X%.4f Y%.4f Z%.4f%s" % (0 if rapid else 1, tgt[0], tgt[1], tgt[2],
                                                         "" if rapid else " F%.3f" % feed))
                emit_move(rapid, tgt)
            continue
        out.append(clean_comment(raw))
        if raw.count("(") > 1 or raw.count(")") > 1:
            nested.append(raw.strip())
        if line == "G21":
            out.append("G92 Z%.1f (camotics_sim: the start point %.0f mm above work zero)" % (SHIFT, SHIFT))
        if motion is None or not has_xyz:
            continue
        tgt = [p.get("X", pos[0]), p.get("Y", pos[1]), p.get("Z", pos[2] if pos[2] is not None else 300.0)]
        arc = None
        if motion in (2, 3):
            arc = (pos[0] + p.get("I", 0.0), pos[1] + p.get("J", 0.0), motion == 2)
        emit_move(motion == 0, tgt, arc)
    expand.nested_comments = nested
    return "\n".join(out) + "\n", moves


def segments(mv, chord=0.25):
    """(N+1, 3) points along a move; arcs split so the chord error is under `chord` mm"""
    p0, p1 = np.array(mv["p0"]), np.array(mv["p1"])
    if mv["arc"] is None:
        return np.stack([p0, p1])
    cx, cy, cw = mv["arc"]
    r = math.hypot(p0[0] - cx, p0[1] - cy)
    a0 = math.atan2(p0[1] - cy, p0[0] - cx)
    a1 = math.atan2(p1[1] - cy, p1[0] - cx)
    sweep = (a0 - a1) if cw else (a1 - a0)
    sweep %= 2 * math.pi
    if sweep < 1e-9:
        sweep = 2 * math.pi
    n = max(2, int(math.ceil(sweep / (2 * math.acos(max(-1.0, 1 - chord / max(r, 1e-6))) + 1e-12))))
    t = np.linspace(0, 1, n + 1)
    a = a0 - t * sweep if cw else a0 + t * sweep
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a), p0[2] + t * (p1[2] - p0[2])], -1)


def move_length(mv):
    s = segments(mv)
    return float(np.linalg.norm(np.diff(s, axis=0), axis=1).sum())


def camotics_times(moves):
    """CAMotics 1.2.0's own timing (Move.cpp): every move takes length / F; rapids at 10 m/min. Also at the VF-4's 25.4
    m/min for comparison. The first move from the tool-change height is left out (CAMotics starts it at the G92 point)."""
    per_op = {}
    for i, mv in enumerate(moves):
        d = move_length(mv) if i else 0.0
        o = per_op.setdefault(mv["op"], dict(feed_mm=0.0, rapid_mm=0.0, feed_s=0.0))
        if mv["rapid"]:
            o["rapid_mm"] += d
        else:
            o["feed_mm"] += d
            o["feed_s"] += d / mv["feed"] * 60
    for o in per_op.values():
        o["camotics_rapid_s"] = o["rapid_mm"] / CAMOTICS_RAPID * 60
        o["vf4_rapid_s"] = o["rapid_mm"] / FC.RAPID_MM_MIN * 60
    return per_op


# --- CAMotics runs -------------------------------------------------------------------------------
def run_camsim(su, cam_text, moves, res, threads=2):
    name, part, rot = su["name"], su["part"], rot_of(su)
    d = WORK / name
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.ngc").write_text(cam_text)
    lo, hi = blank_box_setup(part, rot)
    zmin_tool = min(min(m["p0"][2], m["p1"][2]) for m in moves)
    # slab boundaries on the comparison grid's cell boundaries (so no voxel centre sits on a slab face)
    glo = to_setup(np.array(GRID_LO[part]), rot)
    ghi = to_setup(np.array(GRID_HI[part]), rot)
    g0 = min(glo[2], ghi[2])
    cuts = [lo[2]]
    while True:
        nxt = g0 + math.ceil((cuts[-1] + SLAB - g0) / res) * res
        if nxt >= hi[2] - 1.0:
            break
        cuts.append(nxt)
    cuts.append(hi[2])
    tools = {str(t): dict(units="metric", shape="cylindrical", length=s["length"], diameter=s["d"],
                          description=s["name"]) for t, s in FC.TOOLS.items()}
    slabs = []
    for k in range(len(cuts) - 1):
        z0, z1 = cuts[k], cuts[k + 1]
        rec = dict(z0=round(z0, 3), z1=round(z1, 3), stl=None)
        slabs.append(rec)
        if z1 <= zmin_tool:  # the tool never gets down here: uncut blank
            rec["skipped"] = "below the lowest tool tip (z %.2f)" % zmin_tool
            continue
        tag = f"{name}_s{k}"
        proj = {"units": "metric", "resolution-mode": "manual", "resolution": res, "tools": tools,
                "workpiece": {"automatic": False, "margin": 0,
                              "bounds": {"min": [lo[0], lo[1], z0 - SHIFT], "max": [hi[0], hi[1], z1 - SHIFT]}},
                "files": [f"{name}.ngc"]}
        (d / f"{tag}.camotics").write_text(json.dumps(proj, indent=1))
        t0 = time.time()
        cmd = ["docker", "run", "--rm", f"--memory={DOCKER_MEM}", f"--memory-swap={DOCKER_MEM}", f"--cpus={DOCKER_CPUS}",
               "-v", f"{d}:/work", IMAGE, "sh", "-c",
               f"camsim -v --binary --threads {threads} {tag}.camotics {tag}.stl; echo exit=$?; "
               "cat /sys/fs/cgroup/memory.peak 2>/dev/null || true"]
        p = subprocess.run(cmd, capture_output=True, text=True)
        log = [ln for ln in (p.stdout + p.stderr).splitlines() if not ln.startswith(("/work", "Progress"))]
        (d / f"{tag}.log").write_text("\n".join(log))
        rec.update(seconds=round(time.time() - t0, 1), log_tail=log[-4:])
        stl = d / f"{tag}.stl"
        if stl.exists() and stl.stat().st_size > 84:
            rec["stl"] = str(stl)
        warn = sorted({ln.split("Not implemented:")[-1].strip() for ln in log if "Not implemented" in ln})
        rec["not_implemented"] = warn
        rec["errors"] = [re.sub(r"\x1b\[[0-9;]*m", "", ln) for ln in log if "ERROR" in ln][:10]
        if rec["errors"]:
            print("  CAMotics reported errors:", rec["errors"][:3], flush=True)
        print(f"  {tag}: z {z0:.2f}..{z1:.2f}, {rec['seconds']} s, {'ok' if rec['stl'] else 'FAILED'}", flush=True)
    return dict(slabs=slabs, res=res)


# --- voxels --------------------------------------------------------------------------------------
class Grid:
    def __init__(self, part, res):
        self.lo = np.array(GRID_LO[part])
        self.hi = np.array(GRID_HI[part])
        self.h = res
        self.n = np.round((self.hi - self.lo) / res).astype(int)
        self.c = [self.lo[a] + (np.arange(self.n[a]) + 0.5) * res for a in range(3)]

    def zeros(self):
        return np.zeros(tuple(self.n), bool)

    def box(self, x0, x1, y0, y1, z0, z1):
        m = self.zeros()
        ix = (self.c[0] > x0) & (self.c[0] < x1)
        iy = (self.c[1] > y0) & (self.c[1] < y1)
        iz = (self.c[2] > z0) & (self.c[2] < z1)
        m[np.ix_(ix, iy, iz)] = True
        return m


def read_stl(path):
    """triangles (n, 3, 3) float64 from a binary or ASCII STL"""
    with open(path, "rb") as f:
        head = f.read(84)
        n = int.from_bytes(head[80:84], "little")
        size = os.path.getsize(path)
        if size == 84 + 50 * n:
            dt = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
            return np.fromfile(f, dtype=dt, count=n)["v"].astype(np.float64)
    txt = open(path).read()
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", txt), float)
    return v.reshape(-1, 3, 3)


def voxelize(tris, grid, zrange=None):
    """Scan-line voxelisation along z with a winding count: voxel centre inside <=> crossings below it sum > 0.
    zrange limits the voxels written (others False). Tolerates small mesh defects (one bad column at most)."""
    eps = 1.234567e-6  # keeps column centres off mesh vertices and edges laid on the grid
    cx, cy, cz = grid.c[0] + eps, grid.c[1] + 2 * eps, grid.c[2]
    h = grid.h
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    area2 = (b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0])
    keep = np.abs(area2) > 1e-12
    a, b, c, area2 = a[keep], b[keep], c[keep], area2[keep]
    sign = np.where(area2 > 0, -1, 1).astype(np.int16)  # +z normal (ccw in xy) = leaving the solid going up
    xmin = np.minimum(np.minimum(a[:, 0], b[:, 0]), c[:, 0])
    xmax = np.maximum(np.maximum(a[:, 0], b[:, 0]), c[:, 0])
    ymin = np.minimum(np.minimum(a[:, 1], b[:, 1]), c[:, 1])
    ymax = np.maximum(np.maximum(a[:, 1], b[:, 1]), c[:, 1])
    i0 = np.clip(np.ceil((xmin - grid.lo[0] - eps) / h - 0.5).astype(np.int64), 0, grid.n[0])
    i1 = np.clip(np.floor((xmax - grid.lo[0] - eps) / h - 0.5).astype(np.int64), -1, grid.n[0] - 1)
    j0 = np.clip(np.ceil((ymin - grid.lo[1] - 2 * eps) / h - 0.5).astype(np.int64), 0, grid.n[1])
    j1 = np.clip(np.floor((ymax - grid.lo[1] - 2 * eps) / h - 0.5).astype(np.int64), -1, grid.n[1] - 1)
    ni, nj = np.maximum(i1 - i0 + 1, 0), np.maximum(j1 - j0 + 1, 0)
    cnt = ni * nj
    nz1 = grid.n[2] + 1
    acc = np.zeros(grid.n[0] * grid.n[1] * nz1, np.int16)
    # process in chunks of candidates to bound memory
    order = np.arange(len(cnt))
    start = 0
    while start < len(order):
        csum = np.cumsum(cnt[start:])
        stop = start + int(np.searchsorted(csum, 4_000_000, side="right")) + 1
        stop = min(stop, len(order))
        sl = slice(start, stop)
        cc = cnt[sl]
        tri = np.repeat(np.arange(start, stop), cc)
        if len(tri):
            offs = np.arange(len(tri)) - np.repeat(np.cumsum(cc) - cc, cc)
            ii = i0[tri] + offs // np.maximum(nj[tri], 1)
            jj = j0[tri] + offs % np.maximum(nj[tri], 1)
            px, py = cx[ii], cy[jj]
            A, B, C = a[tri], b[tri], c[tri]
            ar = area2[tri]
            w0 = ((B[:, 0] - px) * (C[:, 1] - py) - (B[:, 1] - py) * (C[:, 0] - px)) / ar
            w1 = ((C[:, 0] - px) * (A[:, 1] - py) - (C[:, 1] - py) * (A[:, 0] - px)) / ar
            w2 = 1 - w0 - w1
            ins = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
            z = w0 * A[:, 2] + w1 * B[:, 2] + w2 * C[:, 2]
            k = np.clip(np.ceil((z - grid.lo[2]) / h - 0.5).astype(np.int64), 0, grid.n[2])
            idx = (ii * grid.n[1] + jj) * nz1 + k
            np.add.at(acc, idx[ins], sign[tri][ins])
        start = stop
    acc = acc.reshape(grid.n[0], grid.n[1], nz1)
    occ = np.cumsum(acc, axis=2, dtype=np.int16)[:, :, :grid.n[2]] > 0
    if zrange is not None:
        occ &= ((cz > zrange[0]) & (cz < zrange[1]))[None, None, :]
    return occ


def setup_occupancy(su, sim, grid):
    """the material CAMotics leaves in one setup, on the part grid (blank where no slab was run)"""
    part, rot = su["part"], rot_of(su)
    z0, z1 = BLANK_Z[part]
    occ = grid.box(-L / 2, L / 2, -W / 2, W / 2, z0, z1)
    for s in sim["slabs"]:
        if s.get("skipped"):
            continue
        if not s["stl"]:
            raise RuntimeError("missing CAMotics output for %s slab %s" % (su["name"], s))
        tris = read_stl(s["stl"])
        tris[..., 2] += SHIFT
        tris = to_part(tris, rot)
        perm, sign = perm_sign(rot)
        ax = perm[2]  # the part axis along the setup's z; the slab is a range along it
        rng = sorted([sign[2] * s["z0"], sign[2] * s["z1"]])
        lims = [[-1e9, 1e9] for _ in range(3)]
        lims[ax] = rng
        region = grid.box(*lims[0], *lims[1], *lims[2])
        if ax == 2:  # the slab is a z range in the part frame too
            occ_s = voxelize(tris, grid, rng)
        else:
            occ_s = voxelize(tris, grid) & region
        occ = np.where(region, occ_s, occ)
        del tris, occ_s, region
    return occ


def core_mask(grid):
    Lc, Wc, R = CORE
    X, Y = np.meshgrid(grid.c[0], grid.c[1], indexing="ij")
    dx = np.maximum(np.abs(X) - (Lc / 2 - R), 0)
    dy = np.maximum(np.abs(Y) - (Wc / 2 - R), 0)
    inside = (np.abs(X) < Lc / 2) & (np.abs(Y) < Wc / 2) & (dx ** 2 + dy ** 2 < R ** 2)
    return np.repeat(inside[:, :, None], grid.n[2], axis=2)


# --- rapid moves through stock (z-map of this setup's cuts over the chained stock) ---------------------
def rapid_check(su, moves, stock_part, grid, tol=0.5, rshrink=0.5):
    """For each G0, the tool (radius - rshrink, a flat-ended cylinder going up forever) swept along the move against
    the stock it meets: the chained stock from earlier setups, minus everything this setup has cut so far (z-map h:
    the lowest tool tip so far in each column). Material counts if it lies more than `tol` above the tool tip and
    more than `tol` below h. Returns the offending moves. Also returns the cut z-map for the plot."""
    rot = rot_of(su)
    # stock in the setup frame: a transpose and flips of the part grid (every setup frame is a signed permutation)
    S, cs = setup_view(stock_part, rot), setup_coords(grid, rot)
    h = grid.h
    nz = S.shape[2]
    C = np.zeros(S.shape[:2] + (nz + 1,), np.int16)
    np.cumsum(S, axis=2, dtype=np.int16, out=C[:, :, 1:])
    zmap = np.full(S.shape[:2], np.inf)
    x0, y0, z0 = cs[0][0] - h / 2, cs[1][0] - h / 2, cs[2][0] - h / 2
    hits = []
    for mi, mv in enumerate(moves):
        r = FC.TOOLS[mv["tool"]]["d"] / 2
        pts = segments(mv)
        for p0, p1 in zip(pts[:-1], pts[1:]):
            rr = r - rshrink if mv["rapid"] else r
            lo = np.minimum(p0[:2], p1[:2]) - rr
            hi = np.maximum(p0[:2], p1[:2]) + rr
            i0, i1 = max(int((lo[0] - x0) / h), 0), min(int((hi[0] - x0) / h) + 1, S.shape[0])
            j0, j1 = max(int((lo[1] - y0) / h), 0), min(int((hi[1] - y0) / h) + 1, S.shape[1])
            if i0 >= i1 or j0 >= j1:
                continue
            X, Y = np.meshgrid(cs[0][i0:i1], cs[1][j0:j1], indexing="ij")
            d = p1 - p0
            a = d[0] ** 2 + d[1] ** 2
            fx, fy = p0[0] - X, p0[1] - Y
            c0 = fx ** 2 + fy ** 2 - rr ** 2
            if a < 1e-12:
                cov = c0 <= 0
                zt = np.full(X.shape, min(p0[2], p1[2]))
            else:
                bq = 2 * (d[0] * fx + d[1] * fy)
                disc = bq ** 2 - 4 * a * c0
                cov = disc >= 0
                sq = np.sqrt(np.where(cov, disc, 0))
                ta = np.clip((-bq - sq) / (2 * a), 0, 1)
                tb = np.clip((-bq + sq) / (2 * a), 0, 1)
                cov &= ((-bq + sq) / (2 * a) >= 0) & ((-bq - sq) / (2 * a) <= 1)
                zt = np.minimum(p0[2] + ta * d[2], p0[2] + tb * d[2])
            if not cov.any():
                continue
            sub = zmap[i0:i1, j0:j1]
            if mv["rapid"]:
                k_lo = np.clip(np.ceil((zt + tol - z0) / h - 0.5), 0, nz).astype(int)
                ztop = np.where(np.isinf(sub), 1e9, sub - tol)
                k_hi = np.clip(np.ceil((ztop - z0) / h - 0.5), 0, nz).astype(int)
                k_hi = np.maximum(k_hi, k_lo)
                Csub = C[i0:i1, j0:j1]
                n = (np.take_along_axis(Csub, k_hi[..., None], 2)[..., 0]
                     - np.take_along_axis(Csub, k_lo[..., None], 2)[..., 0])
                n = np.where(cov, n, 0)
                if n.max() > 0:
                    w = np.unravel_index(np.argmax(n), n.shape)
                    hits.append(dict(move=mi, op=mv["op"], tool=mv["tool"], gcode_line=mv["line"],
                                     p0=[round(v, 3) for v in p0], p1=[round(v, 3) for v in p1],
                                     material_mm3=float(n.sum()) * h ** 3, max_column_mm=float(n.max()) * h,
                                     at_setup_xy=[float(X[w]), float(Y[w])]))
            else:
                np.minimum(sub, np.where(cov, zt, np.inf), out=sub)
    # merge per move
    merged = {}
    for hit in hits:
        m = merged.setdefault(hit["move"], dict(hit, material_mm3=0.0, max_column_mm=0.0))
        m["material_mm3"] += hit["material_mm3"]
        m["max_column_mm"] = max(m["max_column_mm"], hit["max_column_mm"])
    out = []
    for m in merged.values():
        mv = moves[m["move"]]
        m.update(p0=[round(v, 3) for v in mv["p0"]], p1=[round(v, 3) for v in mv["p1"]],
                 material_mm3=round(m["material_mm3"], 2), max_column_mm=round(m["max_column_mm"], 2))
        out.append(m)
    return out, zmap, cs


# --- comparison ----------------------------------------------------------------------------------
def depth_into(mask, grid, chunk=100, overlap=40):
    """distance (mm) from each voxel of `mask` to the nearest voxel outside it (0 outside), EDT in x chunks with a
    20 mm overlap (exact up to 20 mm, which is plenty here) so it fits in memory"""
    from scipy import ndimage
    nx = mask.shape[0]
    out = np.zeros(mask.shape, np.float32)
    for s in range(0, nx, chunk):
        e = min(nx, s + chunk)
        a0, a1 = max(0, s - overlap), min(nx, e + overlap)
        d = ndimage.distance_transform_edt(mask[a0:a1], sampling=grid.h)
        out[s:e] = d[s - a0:e - a0]
        del d
    return out


def deep_regions(mask, depth, grid, min_depth, limit=25):
    """voxels of `mask` more than min_depth (mm) from the target surface, as connected regions"""
    from scipy import ndimage
    deep = mask & (depth >= min_depth)
    lab, n = ndimage.label(deep)
    out = []
    for k, sl in enumerate(ndimage.find_objects(lab), 1):
        reg = lab[sl] == k
        dd = np.where(reg, depth[sl], 0)
        w = np.unravel_index(np.argmax(dd), dd.shape)
        idx = [sl[a].start + w[a] for a in range(3)]
        bb = [[float(grid.c[a][sl[a].start] - grid.h / 2), float(grid.c[a][sl[a].stop - 1] + grid.h / 2)]
              for a in range(3)]
        out.append(dict(volume_mm3=round(float(reg.sum()) * grid.h ** 3, 1), max_depth_mm=round(float(dd.max()), 2),
                        deepest_at=[round(float(grid.c[a][idx[a]]), 2) for a in range(3)],
                        bbox=[[round(v, 2) for v in b] for b in bb]))
    out.sort(key=lambda c: -c["volume_mm3"])
    vol = float(deep.sum()) * grid.h ** 3
    return out[:limit], len(out), vol, deep


def render(name, target, final, gouge, left, grid, path, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ext = [grid.lo[0], grid.hi[0], grid.lo[1], grid.hi[1]]
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.4))
    proj = [("top view: material height (CAMotics, chained)", None)]
    top = np.where(final.any(2), grid.c[2][np.clip(final.shape[2] - 1 - np.argmax(final[:, :, ::-1], 2), 0, None)],
                   np.nan)
    im = axs[0].imshow(top.T, origin="lower", extent=ext, cmap="viridis")
    axs[0].set_title("simulated part, top of material (z, mm)", fontsize=9)
    fig.colorbar(im, ax=axs[0], fraction=0.035)
    g2 = gouge.sum(2) * grid.h
    l2 = left.sum(2) * grid.h
    for ax, arr, lab, cm in ((axs[1], g2, "gouge: kept material cut away (mm, summed through z)", "Reds"),
                             (axs[2], l2, "leftover: material still there (mm, summed through z)", "Blues")):
        ax.imshow(target.any(2).T, origin="lower", extent=ext, cmap="Greys", alpha=0.25)
        im = ax.imshow(np.where(arr > 0, arr, np.nan).T, origin="lower", extent=ext, cmap=cm,
                       vmin=0, vmax=max(1.0, float(np.nanmax(arr)) if arr.any() else 1.0))
        ax.set_title(lab, fontsize=9)
        fig.colorbar(im, ax=ax, fraction=0.035)
    for ax in axs:
        ax.set_xlabel("x (mm)")
        ax.set_ylabel("y (mm)")
        ax.set_aspect("equal")
    fig.suptitle(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=80)
    plt.close(fig)


def a_axis_test():
    """Does camsim simulate an A move? A 6 mm hole 10 mm deep at X10 from the top of a 50 mm cube, then G0 A90, then the
    same hole at X30. With A simulated, the second hole would enter a side face; if A is ignored it goes in from the top."""
    d = WORK / "a_axis_test"
    d.mkdir(parents=True, exist_ok=True)
    (d / "atest.ngc").write_text("G21 G90 G17\nG92 Z%.1f\nM6 T1\nG0 Z30\nG0 X10 Y0\nG1 Z15 F500\nG0 Z30\nG0 A90\nG0 X30 Y0\n"
                                 "G1 Z15 F500\nG0 Z30\nM2\n" % SHIFT)
    (d / "atest.camotics").write_text(json.dumps({
        "units": "metric", "resolution-mode": "manual", "resolution": 0.5,
        "tools": {"1": {"units": "metric", "shape": "cylindrical", "length": 30, "diameter": 6, "description": "6 mm"}},
        "workpiece": {"automatic": False, "margin": 0, "bounds": {"min": [0, -25, -25 - SHIFT], "max": [50, 25, 25 - SHIFT]}},
        "files": ["atest.ngc"]}))
    p = subprocess.run(["docker", "run", "--rm", "--memory=1g", f"--cpus={DOCKER_CPUS}", "-v", f"{d}:/work", IMAGE, "sh", "-c",
                        "cd /work && camsim -v --binary atest.camotics atest.stl"], capture_output=True, text=True)
    log = [ln for ln in (p.stdout + p.stderr).splitlines() if "atest.ngc:8:" in ln or "Not implemented" in ln]
    tris = read_stl(str(d / "atest.stl"))
    tris[..., 2] += SHIFT

    import types
    G = types.SimpleNamespace(lo=np.array([0.0, -25.0, -25.0]), hi=np.array([50.0, 25.0, 25.0]), h=0.5)  # a 50 mm cube
    G.n = np.round((G.hi - G.lo) / G.h).astype(int)
    G.c = [G.lo[k] + (np.arange(G.n[k]) + 0.5) * G.h for k in range(3)]
    occ = voxelize(tris, G)

    def solid(x, y, z):
        return bool(occ[tuple(int((v - G.lo[a]) / G.h) for a, v in enumerate((x, y, z)))])
    res = dict(program=(d / "atest.ngc").read_text().splitlines(), camsim_log_for_the_A_move=log,
               hole1_top_x10_cut=not solid(10, 0, 20), hole2_top_x30_cut=not solid(30, 0, 20),
               side_faces_cut=not (solid(30, -22, 0) and solid(30, 22, 0)),
               removed_cm3=round(float((~occ).sum()) * G.h ** 3 / 1000, 3), two_holes_cm3=round(2 * math.pi * 9 * 10 / 1000, 3))
    res["a_simulated"] = bool(res["side_faces_cut"] and not res["hole2_top_x30_cut"])
    res["verdict"] = ("CAMotics 1.2.0 simulates the A axis" if res["a_simulated"] else
                      "CAMotics 1.2.0 ignores the A axis: the hole after G0 A90 was cut from the top, as at A0")
    (OUT / "a_axis_test.json").write_text(json.dumps(res, indent=1))
    print(res["verdict"], flush=True)
    return res


WALLS = [("front wall (y -111..-95), cut at A0", 1, (-111.0, -95.0)), ("back wall (y 95..111), cut at A180", 1, (95.0, 111.0)),
         ("left wall (x -156..-140), cut at A90", 0, (-156.0, -140.0)), ("right wall (x 140..156), cut at A270", 0, (140.0, 156.0))]


def render_walls(tgt, final, grid, path, title):
    """setup C's work: the material through each wall (mm, summed along the wall's normal over its 16 mm), the model
    beside the chained CAMotics result, seen from outside the wall"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(4, 2, figsize=(13, 11.5))
    for row, (name, ax, (a0, a1)) in enumerate(WALLS):
        sel = (grid.c[ax] > a0) & (grid.c[ax] < a1)
        u = 1 - ax  # the wall's horizontal axis: x on the front and back, y on the sides
        for col, (arr, lab) in enumerate(((tgt, "model"), (final, "CAMotics, setups chained"))):
            m = np.compress(sel, arr, axis=ax).sum(axis=ax).astype(float) * grid.h   # over (u, z)
            ext = [grid.lo[u], grid.hi[u], grid.lo[2], grid.hi[2]]
            im = axs[row, col].imshow(m.T, origin="lower", extent=ext, cmap="viridis", vmin=0, vmax=a1 - a0, aspect="equal")
            axs[row, col].set_title(f"{name}: {lab}", fontsize=9)
            axs[row, col].set_xlabel("xy"[u] + " (mm)")
            axs[row, col].set_ylabel("z (mm)")
            if col == 1:
                fig.colorbar(im, ax=axs[row, col], fraction=0.02, label="material through the wall (mm)")
    fig.suptitle(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=70)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a-axis-test", action="store_true", help="only check whether camsim simulates an A move")
    ap.add_argument("--render-walls", action="store_true", help="only redraw camotics_frame_walls.png from $CAMOTICS_WORK")
    ap.add_argument("--res", type=float, default=0.5)
    ap.add_argument("--skip-sim", action="store_true", help="reuse the CAMotics STLs in $CAMOTICS_WORK")
    ap.add_argument("--parts", default="frame,floor")
    ap.add_argument("--min-depth", type=float, default=1.0, help="mm: deviations shallower than this are voxel noise")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    if a.a_axis_test:
        a_axis_test()
        return
    if a.render_walls:
        z = np.load(WORK / "frame_voxels.npz")
        shape = tuple(z["shape"])
        unpack = lambda k: np.unpackbits(z[k])[:int(np.prod(shape))].reshape(shape).astype(bool)  # noqa: E731
        render_walls(unpack("tgt"), unpack("final"), Grid("frame", a.res), OUT / "camotics_frame_walls.png",
                     f"frame setup C: the four walls on the rotary, model and CAMotics ({a.res} mm voxels)")
        return
    fc = json.load(open(HERE.parent / "out" / "machining" / "freecad_cam.json"))
    res_json = WORK / "camotics_runs.json"
    runs = json.load(open(res_json)) if (a.skip_sim and res_json.exists()) else {}
    report = dict(camotics=dict(version="CAMotics 1.2.0 (camsim), Docker image on ubuntu:18.04",
                                resolution_mm=a.res, tool_shapes="cylindrical (flat end) for end mills, face mill "
                                "and drills; drills cut a flat-bottomed hole to the programmed Z"),
                  setups={}, parts={})
    for part in a.parts.split(","):
        grid = Grid(part, a.res)
        sus = [su for su in FC.SETUPS if su["part"] == part]
        tgt = voxelize(read_stl(str(IN_DIR / f"{part}.stl")), grid)
        z0, z1 = BLANK_Z[part]
        stock = grid.box(-L / 2, L / 2, -W / 2, W / 2, z0, z1)
        if part == "frame":
            stock &= ~core_mask(grid)
        initial = stock.copy()
        for su in sus:
            name = su["name"]
            text = open(IN_DIR / "gcode" / f"{name}.ngc").read()
            cam_text, moves = expand(text)
            nested = list(expand.nested_comments)
            t0 = time.time()
            if name not in runs:
                print(name, "CAMotics", flush=True)
                runs[name] = run_camsim(su, cam_text, moves, a.res)
                json.dump(runs, open(res_json, "w"), indent=1)
            sim = runs[name]
            occ = setup_occupancy(su, sim, grid)
            print(f"{name}: voxelised in {time.time() - t0:.0f} s", flush=True)
            hits, zmap, cs = rapid_check(su, moves, stock, grid)
            before = float(stock.sum()) * a.res ** 3
            new_stock = stock & occ
            removed = before - float(new_stock.sum()) * a.res ** 3
            # pieces cut free in this setup (they drop out, or are held only by the fixture)
            from scipy import ndimage
            lab, nlab = ndimage.label(new_stock)
            sizes = np.bincount(lab.ravel())[1:] * a.res ** 3 / 1000
            del lab
            free = sorted((round(float(v), 2) for v in sizes if v > 0.001), reverse=True)[1:]
            gouge_here = stock & ~occ & tgt  # what this setup cut that the part keeps
            times = camotics_times(moves)
            fsu = next(s for s in fc["parts"][part]["setups"] if s["setup"] == name)
            ops = []
            for m in fsu["ops"]:
                t = times.get(m["label"], {})
                ops.append(dict(label=m["label"], tool=m.get("tool"),
                                camotics_min=round((t.get("feed_s", 0) + t.get("camotics_rapid_s", 0)) / 60, 2),
                                camotics_vf4_rapids_min=round((t.get("feed_s", 0) + t.get("vf4_rapid_s", 0)) / 60, 2),
                                freecad_cycle_time=m.get("freecad_cycle_time"),
                                recount_min=round(m.get("cut_time_min", 0) + m.get("rapid_time_min", 0), 2)))
            drills = []
            for m in fsu["ops"]:
                if m.get("kind") != "drill" or "error" in m:
                    continue
                d = FC.TOOLS[m["tool"]]["d"]
                tips = [min(mv["p0"][2], mv["p1"][2]) for mv in moves if mv["op"] == m["label"] and not mv["rapid"]]
                if not tips:
                    continue
                tip = min(tips)
                point = 0.5 * d / math.tan(math.radians(59.0))  # 118 deg point
                drills.append(dict(label=m["label"], drill_mm=d, model_floor_z=m["final_depth"],
                                   tip_z=round(tip, 3), full_diameter_to_z=round(tip + point, 3),
                                   full_diameter_short_by_mm=round(max(0.0, tip + point - m["final_depth"]), 2)))
            tot = lambda k: sum(v.get(k, 0) for v in times.values())  # noqa: E731
            report["setups"][name] = dict(
                part=part, rotation_model_to_setup=rot_label(rot_of(su)), a_deg=su.get("a_deg"), moves=len(moves),
                camotics_runs=sim["slabs"], removed_cm3=round(removed / 1000, 2),
                gouge_cm3_raw=round(float(gouge_here.sum()) * a.res ** 3 / 1000, 3),
                rapids_through_stock=sorted(hits, key=lambda h: -h["material_mm3"])[:40],
                n_rapids_through_stock=len(hits),
                time=dict(camotics_min=round((tot("feed_s") + tot("camotics_rapid_s")) / 60, 2),
                          camotics_feed_min=round(tot("feed_s") / 60, 2),
                          camotics_rapid_min=round(tot("camotics_rapid_s") / 60, 2),
                          with_vf4_rapids_min=round((tot("feed_s") + tot("vf4_rapid_s")) / 60, 2),
                          freecad_job_cycle_time=fsu.get("freecad_job_cycle_time"),
                          freecad_sum_of_ops_min=fsu["totals"]["freecad_sum_of_op_cycle_times_min"],
                          recount_min=fsu["totals"]["total_min"]),
                ops=ops, drills=drills, pieces_free_after_setup_cm3=free[:10],
                comments_with_nested_parentheses=len(nested))
            print(f"{name}: removed {removed / 1000:.1f} cm3, {len(hits)} rapids through stock, CAMotics time "
                  f"{report['setups'][name]['time']['camotics_min']} min", flush=True)
            stock = new_stock
            del occ, gouge_here
        final = stock
        # material no longer joined to the part (trepan slugs, profile-cut slot cores, rings): it drops out
        from scipy import ndimage
        lab, nlab = ndimage.label(final)
        sizes = np.bincount(lab.ravel())
        sizes[0] = 0
        main_k = int(np.argmax(sizes))
        loose = []
        for k, sl in enumerate(ndimage.find_objects(lab), 1):
            if k == main_k or sl is None:
                continue
            vol = float(sizes[k]) * a.res ** 3
            if vol < 1.0:
                continue
            bb = [[round(float(grid.c[ax][sl[ax].start] - grid.h / 2), 2),
                   round(float(grid.c[ax][sl[ax].stop - 1] + grid.h / 2), 2)] for ax in range(3)]
            loose.append(dict(volume_cm3=round(vol / 1000, 2), bbox=bb))
        loose.sort(key=lambda p: -p["volume_cm3"])
        final = lab == main_k
        del lab
        vol_t = float(tgt.sum()) * a.res ** 3
        vol_f = float(final.sum()) * a.res ** 3
        gouge = tgt & ~final
        din = depth_into(tgt, grid)       # depth inside the target
        gcomp, gn, gvol, gdeep = deep_regions(gouge, din, grid, a.min_depth)
        max_gouge = float(din[gouge].max()) if gouge.any() else 0.0
        del din
        left = final & ~tgt
        dout = depth_into(~tgt, grid)     # distance outside the target
        lcomp, ln, lvol, ldeep = deep_regions(left, dout, grid, a.min_depth)
        max_left = float(dout[left].max()) if left.any() else 0.0
        del dout
        report["parts"][part] = dict(
            target_cm3=round(vol_t / 1000, 2), simulated_cm3=round(vol_f / 1000, 2),
            stock_cm3=round(float(initial.sum()) * a.res ** 3 / 1000, 2),
            gouge_all_cm3=round(float(gouge.sum()) * a.res ** 3 / 1000, 3),
            leftover_all_cm3=round(float(left.sum()) * a.res ** 3 / 1000, 3),
            gouge_deeper_than_min_cm3=round(gvol / 1000, 3), leftover_deeper_than_min_cm3=round(lvol / 1000, 3),
            min_depth_mm=a.min_depth, n_gouge_regions=gn, n_leftover_regions=ln,
            max_gouge_depth_mm=round(max_gouge, 2), max_leftover_mm=round(max_left, 2),
            loose_pieces=loose[:20], n_loose_pieces=len(loose),
            gouges=gcomp, leftovers=lcomp)
        render(part, tgt, final, gdeep, ldeep, grid, OUT / f"camotics_{part}.png",
               f"{part}: CAMotics 1.2.0 cut of FreeCAD's G-code, setups chained ({a.res} mm voxels); "
               f"deviations deeper than {a.min_depth} mm")
        if part == "frame":
            render_walls(tgt, final, grid, OUT / "camotics_frame_walls.png",
                         f"frame setup C: the four walls on the rotary, model and CAMotics ({a.res} mm voxels)")
        np.savez_compressed(WORK / f"{part}_voxels.npz", tgt=np.packbits(tgt), final=np.packbits(final),
                            shape=np.array(tgt.shape))
        print(part, json.dumps({k: v for k, v in report["parts"][part].items() if k not in ("gouges", "leftovers")}),
              flush=True)
        del tgt, final, gouge, left, stock, initial, gdeep, ldeep
    out_json = OUT / "camotics_sim.json"
    if out_json.exists() and a.parts != "frame,floor":  # keep the other part's results from an earlier run
        old = json.load(open(out_json))
        for k in ("setups", "parts"):
            for n, v in old.get(k, {}).items():
                report[k].setdefault(n, v)
    json.dump(report, open(out_json, "w"), indent=1)
    print("wrote", out_json)
    summary = dict(ran=True, script="desktop-lpbf/analysis/machining/camotics_sim.py",
                   results="desktop-lpbf/analysis/out/machining/camotics/camotics_sim.json",
                   how="CAMotics 1.2.0 camsim in Docker on ubuntu:18.04 (camotics.Dockerfile), %.2f mm; setups "
                       "chained in the part frame" % a.res,
                   install_error="camotics_1.2.0_amd64.deb links libv8.so.3.14.5 and libssl.so.1.1/libcrypto.so.1.1, "
                                 "which Ubuntu 26.04 lacks; the .deb also needs libqt5websockets5 undeclared",
                   parts={p: {k: v for k, v in r.items() if k in ("gouge_deeper_than_min_cm3", "leftover_deeper_than_min_cm3",
                                                                   "max_gouge_depth_mm", "max_leftover_mm", "n_loose_pieces")}
                          for p, r in report["parts"].items()},
                   setups={n: dict(rapids_through_stock=s["n_rapids_through_stock"], camotics_min=s["time"]["camotics_min"])
                           for n, s in report["setups"].items()})
    fcj = HERE.parent / "out" / "machining" / "freecad_cam.json"
    d = json.load(open(fcj))
    d["camotics"] = summary
    json.dump(d, open(fcj, "w"), indent=1)


if __name__ == "__main__":
    main()
