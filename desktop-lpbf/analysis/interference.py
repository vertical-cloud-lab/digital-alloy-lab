"""Exact B-rep interference and clearance checks on the low-profile model (cad/lpbf_low.py).

For each machine state (doors, recoater, piston, cartridge) every pair of parts whose bounding boxes overlap is
intersected with OpenCascade's boolean Common; any shared volume above VOL_TOL is an interference. Moving parts
are also swept through their whole range in N steps against every fixed part. Minimum clearances between each
moving group and its neighbours are measured with BRepExtrema at every state.

Run:  python desktop-lpbf/analysis/interference.py        (about 2-4 min on 4 cores)
Writes analysis/out/interference.json and analysis/out/interference.md.
"""
from __future__ import annotations

import json
import multiprocessing as mp
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "cad"))
import lpbf_low as M  # noqa: E402
from OCP.BRepExtrema import BRepExtrema_DistShapeShape  # noqa: E402

OUT = HERE / "out"
VOL_TOL = 0.5          # mm3: below this a shared volume is a touching face / tessellation artefact
GAP_WARN = 2.0         # mm: report moving-part clearances below this
N_SWEEP = 12

PARTS = None
SHAPES = None
BBS = None


def _init(state):
    global PARTS, SHAPES, BBS
    if PARTS is None:
        PARTS = M.build()
    SHAPES = M.posed(PARTS, state)
    BBS = [s.BoundingBox() for s in SHAPES]


def bb_overlap(a, b, tol=0.01):
    return (a.xmin - tol <= b.xmax and b.xmin - tol <= a.xmax and a.ymin - tol <= b.ymax and b.ymin - tol <= a.ymax
            and a.zmin - tol <= b.zmax and b.zmin - tol <= a.zmax)


def common_volume(i, j):
    try:
        c = SHAPES[i].intersect(SHAPES[j])
        return c.Volume() if c is not None else 0.0
    except Exception as e:  # noqa: BLE001
        return float("nan")


def min_dist(i, j):
    d = BRepExtrema_DistShapeShape(SHAPES[i].wrapped, SHAPES[j].wrapped)
    return d.Value() if d.IsDone() else float("nan")


def _pairs_job(args):
    state, pairs = args
    _init(state)
    out = []
    for i, j in pairs:
        v = common_volume(i, j)
        if v != v or v > VOL_TOL:
            out.append((i, j, v))
    return out


def _gap_job(args):
    state, pairs = args
    _init(state)
    return [(i, j, min_dist(i, j)) for i, j in pairs]


def check_state(pool, state, only=None):
    """All bbox-overlapping pairs (or pairs touching `only` indices) in `state`."""
    _init(state)
    n = len(SHAPES)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if "context" in PARTS[i].tags or "context" in PARTS[j].tags:
                continue
            if only is not None and i not in only and j not in only:
                continue
            if only is not None and i in only and j in only:
                continue
            if bb_overlap(BBS[i], BBS[j]):
                pairs.append((i, j))
    chunks = [pairs[k::4] for k in range(4)]
    res = []
    for r in pool.map(_pairs_job, [(state, c) for c in chunks]):
        res += r
    return pairs, res


def near_pairs(state, group, pad=12.0):
    _init(state)
    mov = [i for i, p in enumerate(PARTS) if p.group == group]
    out = []
    for i in mov:
        b = BBS[i]
        for j, p in enumerate(PARTS):
            if j in mov or "context" in p.tags:
                continue
            bj = BBS[j]
            if (b.xmin - pad <= bj.xmax and bj.xmin - pad <= b.xmax and b.ymin - pad <= bj.ymax and bj.ymin - pad <= b.ymax
                    and b.zmin - pad <= bj.zmax and bj.zmin - pad <= b.zmax):
                out.append((i, j))
    return out


def main():
    global PARTS
    t0 = time.time()
    PARTS = M.build()
    names = [p.name for p in PARTS]
    OUT.mkdir(exist_ok=True)
    ctx = mp.get_context("fork")
    report = dict(vol_tol_mm3=VOL_TOL, n_parts=len(PARTS), states=[], sweeps=[], clearances=[])
    with ctx.Pool(4) as pool:
        # 1. static states: everything against everything
        states = {"closed, parked, piston up": {},
                  "recoater at end, piston at bottom": {"recoater": M.MOTION["recoater"]["hi"], "piston": M.MOTION["piston"]["lo"]},
                  "doors open, cartridge out": {"door": M.MOTION["door"]["hi"], "gdoor": M.MOTION["gdoor"]["hi"], "cartridge": M.MOTION["cartridge"]["lo"]}}
        for label, st in states.items():
            pairs, hits = check_state(pool, st)
            report["states"].append(dict(state=label, pose=st, pairs_checked=len(pairs),
                                         interferences=[dict(a=names[i], b=names[j], volume_mm3=round(v, 2)) for i, j, v in hits]))
            print(f"[{time.time() - t0:5.0f} s] {label}: {len(pairs)} pairs, {len(hits)} interferences", flush=True)
        # 2. sweeps: each moving group through its range against everything else
        for g, m in M.MOTION.items():
            mov = {i for i, p in enumerate(PARTS) if p.group == g}
            worst = {}
            for k in range(N_SWEEP + 1):
                v = m["lo"] + (m["hi"] - m["lo"]) * k / N_SWEEP
                st = {g: v}
                if g == "cartridge":
                    st["gdoor"] = M.MOTION["gdoor"]["hi"]
                pairs, hits = check_state(pool, st, only=mov)
                for i, j, vol in hits:
                    key = (names[i], names[j])
                    if key not in worst or vol > worst[key][1]:
                        worst[key] = (v, vol)
            report["sweeps"].append(dict(group=g, note=m["note"], range=[m["lo"], m["hi"]], steps=N_SWEEP + 1,
                                         interferences=[dict(a=a, b=b, at=round(v, 2), volume_mm3=round(vol, 2)) for (a, b), (v, vol) in worst.items()]))
            print(f"[{time.time() - t0:5.0f} s] sweep {g}: {len(worst)} interfering pairs", flush=True)
        # 3. clearances: moving group vs neighbours at both ends of its range
        for g, m in M.MOTION.items():
            for v in (m["lo"], m["hi"]):
                st = {g: v}
                pairs = near_pairs(st, g)
                chunks = [pairs[k::4] for k in range(4)]
                res = []
                for r in pool.map(_gap_job, [(st, c) for c in chunks]):
                    res += r
                best = {}
                for i, j, d in res:
                    key = names[j]
                    if key not in best or d < best[key][1]:
                        best[key] = (names[i], d)
                for other, (mine, d) in sorted(best.items(), key=lambda kv: kv[1][1]):
                    report["clearances"].append(dict(group=g, at=v, moving=mine, other=other, gap_mm=round(d, 3)))
            print(f"[{time.time() - t0:5.0f} s] clearances {g}", flush=True)
    report["runtime_s"] = round(time.time() - t0, 1)
    (OUT / "interference.json").write_text(json.dumps(report, indent=1))
    write_md(report)
    print(f"done in {report['runtime_s']} s")


def write_md(r):
    L = [f"# Interference and clearance check ({r['n_parts']} parts)", "",
         f"Exact OpenCascade booleans; a shared volume above {r['vol_tol_mm3']} mm3 counts as an interference.", ""]
    L += ["## Static states", "", "| State | Pairs checked | Interferences |", "|---|---|---|"]
    for s in r["states"]:
        L.append(f"| {s['state']} | {s['pairs_checked']} | {len(s['interferences'])} |")
    for s in r["states"]:
        for it in s["interferences"]:
            L.append(f"- {s['state']}: **{it['a']}** x **{it['b']}**: {it['volume_mm3']} mm3")
    L += ["", "## Motion sweeps", "", "| Group | Range | Steps | Interfering pairs |", "|---|---|---|---|"]
    for s in r["sweeps"]:
        L.append(f"| {s['group']} ({s['note']}) | {s['range'][0]:g} to {s['range'][1]:g} | {s['steps']} | {len(s['interferences'])} |")
    for s in r["sweeps"]:
        for it in s["interferences"]:
            L.append(f"- {s['group']} at {it['at']}: **{it['a']}** x **{it['b']}**: {it['volume_mm3']} mm3")
    L += ["", f"## Tightest clearances of moving parts (< {GAP_WARN} mm)", "", "| Group | At | Moving part | Other part | Gap (mm) |", "|---|---|---|---|---|"]
    for c in r["clearances"]:
        if c["gap_mm"] < GAP_WARN:
            L.append(f"| {c['group']} | {c['at']:g} | {c['moving']} | {c['other']} | {c['gap_mm']:.3f} |")
    (OUT / "interference.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
