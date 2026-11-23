"""Run every hand operation in operations.py on the model and write the results (issue #260, PR #266).

Run (from the repo root; the cad folder is an argument so the checks can be re-run on the final model):
    OMP_NUM_THREADS=1 /tmp/capmem 4 xvfb-run -a -s "-screen 0 1280x960x24" \
        /tmp/venv/bin/python desktop-lpbf/analysis/ops/run_ops.py desktop-lpbf/cad [M50|S25|L75] [--no-png] [--only=U1,U2] [--tag=-x]
Writes desktop-lpbf/analysis/out/ops/results-<module>.json, results-<module>.md and fail-*.png.
The first run tessellates the model (~2 min); later runs on unchanged cad files reuse /tmp/ops-work/cache.
"""
from __future__ import annotations

import json
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import checks as CK  # noqa: E402

OUT = HERE.parent / "out" / "ops"


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    cad = args[0] if args else str(HERE.parent.parent / "cad")
    module = args[1] if len(args) > 1 else "M50"
    png = "--no-png" not in argv
    only = [a.split("=", 1)[1] for a in argv if a.startswith("--only=")]
    tag = next((a.split("=", 1)[1] for a in argv if a.startswith("--tag=")), "")     # results-<module><tag>.*: a partial run keeps the full one
    t0 = time.time()
    sc = CK.Scene(cad, module)
    import operations as OP  # noqa: E402  (needs module_params from the cad folder on sys.path)
    import tools as TL  # noqa: E402
    ops = OP.catalogue(module)
    if only:
        ops = [o for o in ops if o["id"] in only[0].split(",")]
    ALL = list(range(sc.n))
    MODULE_SET = sc.group("module")
    OUT.mkdir(parents=True, exist_ok=True)
    renders, rows = [], []

    def objs_for(keys, exclude=()):
        return sc.find(*keys, exclude=tuple(exclude)) if keys else []

    for op in ops:
        print(f"[{time.time() - t0:6.1f} s] {op['id']} {op['name']}", flush=True)
        op_state = dict(op.get("state", {}))
        state = dict(op_state)
        seq = op.get("present") == "sequence"
        if op.get("present") == "module":
            base = list(MODULE_SET)
        elif seq:
            base = []
        else:
            base = list(ALL)
        placed, removed = [], set()
        op_rows = []
        for k, st in enumerate(op["steps"]):
            sid = f"{op['id']}.{k + 1}"
            state = dict(op_state, **(st.get("state") or {}))     # a step may move a group first (door shut, recoater to one end)
            r = dict(id=sid, op=op["id"], step=st["label"], do=st["do"], minutes=st.get("minutes", 0), note=st.get("note", ""))

            def present_now(extra=()):
                if seq:
                    return sorted(set(placed) | set(extra))
                return sorted((set(base) - removed) | set(extra))

            try:
                if st["do"] == "note":
                    r.update(status="-", detail="")
                elif st["do"] == "place":
                    mov = objs_for(st["keys"], st.get("exclude", ()))
                    if op.get("bench"):
                        mov = [i for i in mov if i in MODULE_SET]
                    if not st.get("move_placed"):
                        mov = [i for i in mov if i not in placed]
                    if not mov:
                        r.update(status="?", detail="no part matched")
                    elif st["path"] is None:
                        r.update(status="-", detail="placed by hand or welded on; no path check")
                    else:
                        groups = {}
                        if st["path"] == "explode" and st.get("per_part"):
                            for i in mov:
                                groups.setdefault(tuple(sc.parts[sc.objs[i]["part"]].explode), []).append(i)
                        elif st["path"] == "explode":
                            # the step's parts move together, along the first (non-fastener) part's explode offset
                            lead = next((i for i in mov if sc.objs[i]["item"] is None), mov[0])
                            groups[tuple(sc.parts[sc.objs[lead]["part"]].explode)] = mov
                        else:
                            groups[None] = mov
                        pre = CK.rot((0, 0, 1), st["rot"]) if st.get("rot") else None
                        details, ok_all, tight = [], True, None
                        for ex, gi in groups.items():
                            path = [(0, 0, 0), ex] if ex is not None else st["path"]
                            if ex is not None and np.linalg.norm(ex) < 1e-6:
                                continue
                            res = path_check_rot(sc, state, present_now(), gi, path, pre)
                            if res["ok"]:
                                g = res["min_gap"]
                                tight = g if tight is None or (g is not None and g < tight) else tight
                                details.append(f"documented path clear (gap {g} mm to {res['gap_with'] and res['gap_with'][:40]})")
                                continue
                            ok_all = False
                            free = []
                            for nm, d in CK.AXES.items():
                                rr = path_check_rot(sc, state, present_now(), gi, [(0, 0, 0), tuple(np.array(d) * 520.0)], pre, ds=5.0, exact=False)
                                if rr["ok"]:
                                    free.append(nm)
                            two = "" if free else two_leg(sc, state, present_now(), gi, pre)
                            details.append(f"documented path {tuple(round(float(x)) for x in path[-1])} blocked by {res['blocked_by'][:50]} "
                                           f"after {res['at_s']} mm; free straight directions: {', '.join(free) or 'none'}"
                                           + (f"; {two}" if two else ""))
                            renders.append(dict(kind="path", sid=sid, mov=gi, at=res["at"], blocker=res["blocker"], state=state,
                                                present=present_now(), title=f"{sid} {st['label'][:70]}: blocked by {sc.short(res['blocker'])}"))
                        r.update(status="PASS" if ok_all else "FAIL", detail="; ".join(details), clearance=tight)
                    placed.extend(i for i in mov if i not in placed)
                elif st["do"] == "module":
                    mov = list(MODULE_SET)
                    if seq:
                        placed.extend(i for i in mov if i not in placed)
                    pres = [i for i in present_now() if i not in mov]
                    path = sc.M.MOTION["module"]["path"]
                    stt = dict(state)
                    stt["zstage"] = sc.MP.ZSTAGE_RELEASE
                    res = CK.path_check(sc, stt, pres + mov, mov, path, ds=4.0)
                    r.update(status="PASS" if res["ok"] else "FAIL", clearance=res.get("min_gap"),
                             detail=(f"swap path clear; tightest gap {res['min_gap']} mm to {res['gap_with']}" if res["ok"] else
                                     f"blocked by {res['blocked_by'][:60]} at s = {res['at_s']} mm"))
                    if not res["ok"]:
                        renders.append(dict(kind="path", sid=sid, mov=mov, at=res["at"], blocker=res["blocker"], state=stt, present=pres,
                                            title=f"{sid} module swap path blocked by {sc.short(res['blocker'])}"))
                elif st["do"] == "screws":
                    idx = sc.joint(st["joint"], st.get("pn"))
                    pres = present_now(idx)
                    w = CK.World(sc, state, pres)
                    per = []
                    for i in idx:
                        c = sc.FS.CATALOG[sc.objs[i]["pn"]]
                        s = float(c.get("s", 2.0))
                        wd = CK.withdraw_check(sc, w, i)
                        best, tq = None, None
                        for tool in TL.candidates(s):
                            tr = CK.tool_check(sc, w, i, tool, tilts=tool.tilts)
                            tr["tool"] = tool.name
                            if tool.torque:
                                tq = tr
                            if tr["ok"]:
                                best = tr
                                break
                        if tq is None:
                            tq = dict(ok=False)
                        per.append(dict(i=i, name=sc.label(i), withdraw=wd, best=best, torque=tq))
                    nfail = sum(1 for p in per if p["best"] is None or not p["withdraw"]["ok"])
                    nwarn = sum(1 for p in per if p["best"] is not None and st.get("torque") and not p["torque"].get("ok"))
                    status = "FAIL" if nfail else ("WARN" if nwarn else "PASS")
                    tools_used = sorted({p["best"]["tool"].split(" (")[0] for p in per if p["best"]})
                    cl = [p["best"]["clearance"] for p in per if p["best"] and p["best"]["clearance"] is not None]
                    blk = {}
                    for p in per:
                        if not p["withdraw"]["ok"]:
                            for b in p["withdraw"]["blocked_by"]:
                                blk[f"withdrawal: {b}"] = blk.get(f"withdrawal: {b}", 0) + 1
                    det = f"{len(idx)} screws; {len(idx) - nfail} reachable with: {', '.join(tools_used) or 'nothing'}"
                    if st.get("torque"):
                        det += f"; torque screwdriver fits {sum(1 for p in per if p['torque'].get('ok'))}/{len(idx)}"
                    tq_block = {}
                    for p in per:
                        if not p["torque"].get("ok"):
                            for b in p["torque"].get("blocked_by", []):
                                tq_block[b] = tq_block.get(b, 0) + 1
                    if tq_block:
                        det += "; torque driver blocked by " + ", ".join(sorted(tq_block, key=lambda b: -tq_block[b])[:2])
                    if blk:
                        det += "; " + ", ".join(sorted(blk)[:2])
                    fails = [p for p in per if p["best"] is None]
                    if fails:
                        # re-run the most forgiving key to say what blocks it
                        p = fails[0]
                        s = float(sc.FS.CATALOG[sc.objs[p['i']]['pn']].get("s", 2.0))
                        tr = CK.tool_check(sc, w, p["i"], TL.lkey_short(s))
                        det += f"; e.g. {p['name']}: short-arm key free arc {tr['arc_deg']:.0f} deg, blocked by {', '.join(tr['blocked_by'][:2])}"
                        renders.append(dict(kind="tool", sid=sid, screw=p["i"], tool="lkey_short", s=s, state=state, present=pres,
                                            title=f"{sid} {sc.short(p['i'])}: no tool fits ({', '.join(tr['blocked_by'][:1])})"))
                    elif nwarn:
                        p = next(p for p in per if not p["torque"].get("ok"))
                        s = float(sc.FS.CATALOG[sc.objs[p['i']]['pn']].get("s", 2.0))
                        renders.append(dict(kind="tool", sid=sid, screw=p["i"], tool="torque_sd", s=s, state=state, present=pres,
                                            title=f"{sid} {sc.short(p['i'])}: torque screwdriver blocked ({', '.join(p['torque'].get('blocked_by', [])[:1])})"))
                    r.update(status=status, detail=det, clearance=min(cl) if cl else None,
                             per_screw=[dict(screw=p["name"], withdraw_ok=p["withdraw"]["ok"], tool=p["best"]["tool"] if p["best"] else None,
                                             arc=p["best"]["arc_deg"] if p["best"] else None, clearance=p["best"]["clearance"] if p["best"] else None,
                                             clear_with=p["best"]["clear_with"] if p["best"] else None, torque_ok=p["torque"].get("ok"),
                                             torque_blocked_by=p["torque"].get("blocked_by")) for p in per])
                    if seq:
                        placed.extend(i for i in idx if i not in placed)
                    else:
                        removed.update(idx)          # unscrewed and set aside for the rest of the operation
                elif st["do"] == "remove":
                    mov = [i for i in objs_for(st["keys"], st.get("exclude", ())) if i not in removed]
                    if op.get("present") == "module":
                        mov = [i for i in mov if i in MODULE_SET]
                    pres = present_now()
                    pre = None
                    if st.get("rot"):
                        pre = CK.rot((0, 0, 1), st["rot"])
                    results, ok = [], False
                    if not st["paths"]:
                        r.update(status="-", detail="by hand; no path check")
                        removed.update(mov)
                        print(f"   {sid} {r['status']:4s} {st['label'][:70]}", flush=True)
                        op_rows.append(r)
                        continue
                    for path in st["paths"]:
                        res = path_check_rot(sc, state, pres, mov, path, pre)
                        results.append((path, res))
                        if res["ok"]:
                            ok = True
                            break
                    if ok:
                        path, res = results[-1]
                        r.update(status="PASS", clearance=res["min_gap"],
                                 detail=f"free along {fmt_path(path)}; tightest gap {res['min_gap']} mm to {(res['gap_with'] or '')[:50]}"
                                 + (f" (first try {fmt_path(results[0][0])} blocked by {results[0][1]['blocked_by'][:40]})" if len(results) > 1 else ""))
                    else:
                        path, res = results[0]
                        others = "; ".join(f"{fmt_path(p)}: {rr['blocked_by'][:40]} at {rr['at_s']} mm" for p, rr in results[1:4])
                        r.update(status="FAIL", detail=f"{fmt_path(path)} blocked by {res['blocked_by'][:60]} after {res['at_s']} mm"
                                 + (f"; also tried {others}" if others else ""))
                        renders.append(dict(kind="path", sid=sid, mov=mov, at=res["at"], blocker=res["blocker"], state=state, present=pres, pre=pre,
                                            title=f"{sid} {st['label'][:60]}: blocked by {sc.short(res['blocker'])}"))
                    removed.update(mov)
                elif st["do"] == "reach":
                    pres = present_now()
                    skip = set(objs_for(st["skip"]))
                    pt = st["point"]
                    if isinstance(pt, str):
                        ids = objs_for([pt])
                        w0 = CK.World(sc, state, ids)
                        bb = [w0.bb[i] for i in ids if i in w0.bb]
                        lo = np.min([b[0] for b in bb], 0)
                        hi = np.max([b[1] for b in bb], 0)
                        pt = tuple(((lo + hi) / 2).tolist())
                    w = CK.World(sc, state, pres)
                    outs = []
                    for a in st["approach"]:
                        rr = CK.reach_check(sc, w, pt, a, skip=skip, **({"hand": tuple(st["hand"])} if st.get("hand") else {}))
                        outs.append((a, rr))
                        if rr["ok"]:
                            break
                    ok = outs[-1][1]["ok"]
                    r.update(status="PASS" if ok else "FAIL",
                             detail=(f"hand + forearm clear from {fmt_dir(outs[-1][0])}" if ok else
                                     "blocked: " + "; ".join(f"from {fmt_dir(a)}: {', '.join(rr['blocked_by'][:2])}" for a, rr in outs)))
                elif st["do"] == "clear":
                    pres = present_now()
                    skip = set(objs_for(st["skip"]))
                    x0, x1, y0, y1, z0, z1 = st["box"]
                    import trimesh
                    m = trimesh.creation.box(extents=(x1 - x0, y1 - y0, z1 - z0))
                    m.apply_translation(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
                    w = CK.World(sc, state, pres)
                    g = CK.bvh(m.vertices, m.faces)
                    hits = w.collide_geom(g, np.eye(4), CK.aabb(np.asarray(m.vertices), np.eye(4)), skip)
                    r.update(status="PASS" if not hits else "FAIL", detail=("column clear" if not hits else
                                                                             "blocked by " + ", ".join(sc.short(j) for j in hits[:3])))
            except Exception as e:  # noqa: BLE001
                r.update(status="ERR", detail=f"{type(e).__name__}: {e}")
            print(f"   {sid} {r['status']:4s} {st['label'][:70]} | {r.get('detail', '')[:160]}", flush=True)
            op_rows.append(r)
        rows.append(dict(id=op["id"], kind=op["kind"], name=op["name"], where=op["where"], interval=op["interval"], air=op["air"],
                         minutes=round(sum(s.get("minutes", 0) for s in op["steps"]), 1), steps=op_rows))
        (OUT / f"results-{module}{tag}.json").write_text(json.dumps(dict(module=module, cad=str(cad), ops=rows), indent=1, default=str))
    write_md(rows, module, OUT / f"results-{module}{tag}.md", time.time() - t0)
    print(f"[{time.time() - t0:6.1f} s] checks done; {len(renders)} failing cases to draw", flush=True)
    if png and renders:
        draw(sc, renders, module)
    print(f"done in {time.time() - t0:.0f} s")


def two_leg(sc, state, pres, mov, pre, budget_s=90.0):
    """first free two-leg path: a short first leg (10 or 30 mm along an axis), then 520 mm along an axis."""
    t0 = time.time()
    for L1 in (10.0, 30.0):
        for n1, d1 in CK.AXES.items():
            p1 = tuple(np.array(d1) * L1)
            for n2, d2 in CK.AXES.items():
                if n2 == n1 or time.time() - t0 > budget_s:
                    continue
                path = [(0, 0, 0), p1, tuple(np.array(p1) + np.array(d2) * 520.0)]
                rr = path_check_rot(sc, state, pres, mov, path, pre, ds=5.0, exact=False)
                if rr["ok"]:
                    return f"free two-leg path: {L1:.0f} mm {n1}, then {n2}"
    return "no two-leg path (10/30 mm then an axis) found" if time.time() - t0 <= budget_s else "two-leg search stopped at its time budget"


def path_check_rot(sc, state, pres, mov, path, pre, **kw):
    if pre is None:
        return CK.path_check(sc, state, pres, mov, path, **kw)
    # apply a rotation about z (through the origin) to the moving objects before translating: wrap their poses
    orig = sc.pose

    def posed(i, st, _o=orig):
        m = _o(i, st)
        return pre @ m if i in mov else m
    sc.pose = posed
    try:
        return CK.path_check(sc, state, pres, mov, path, **kw)
    finally:
        sc.pose = orig


def fmt_path(p):
    return " -> ".join("(" + ", ".join(f"{float(v):.0f}" for v in q) + ")" for q in p[1:])


def fmt_dir(a):
    names = {(0, -1, 0): "the front", (0, 0, 1): "above", (1, 0, 0): "the right", (-1, 0, 0): "the left", (0, 0, -1): "below", (0, 1, 0): "the back"}
    return names.get(tuple(int(round(x)) if abs(x - round(x)) < 1e-9 else x for x in a), str(tuple(round(x, 2) for x in a)))


def write_md(rows, module, path, dt):
    L = [f"# Hand operations checked on the model ({module} module)", "",
         f"Generated by `run_ops.py` in {dt:.0f} s. PASS: the geometry allows it. WARN: possible, but not with the tool the joint needs "
         "(a torque screwdriver). FAIL: blocked (reason given). `-`: no geometric check (off-machine work, waiting, or a part placed by hand).", ""]
    tot = {"PASS": 0, "WARN": 0, "FAIL": 0, "ERR": 0}
    for op in rows:
        for s in op["steps"]:
            if s["status"] in tot:
                tot[s["status"]] += 1
    L += [f"Steps: {tot['PASS']} pass, {tot['WARN']} warn, {tot['FAIL']} fail, {tot['ERR']} errors.", ""]
    for op in rows:
        L += [f"## {op['id']} {op['name']}", "",
              f"{op['kind']}; {op['where']}; interval: {op['interval']}; opens the chamber to air: {'yes' if op['air'] else 'no'}; "
              f"~{op['minutes']:.0f} min of hands-on and waiting time", "",
              "| Step | What | Result | Tightest clearance (mm) | Detail |", "|---|---|---|---|---|"]
        for s in op["steps"]:
            cl = s.get("clearance")
            L.append(f"| {s['id']} | {s['step']} | {s['status']} | {'' if cl is None else cl} | {s.get('detail', '').replace('|', '/')} |")
        L.append("")
    path.write_text("\n".join(L) + "\n")


PRIORITY = ["U4.7", "M5.1", "M4.4", "M7.2", "M3.2", "M4.3", "M8.2", "M9.1", "U2.2", "S2.4", "A2.3"]


def draw(sc, renders, module, limit=12):
    import pyvista as pv
    pv.OFF_SCREEN = True
    seen = set()
    n = 0
    renders = sorted(renders, key=lambda j: PRIORITY.index(j["sid"]) if j["sid"] in PRIORITY else 99)
    for job in renders:
        key = (job["kind"], job.get("tool"), job["title"].split(":")[0][:12])
        if key in seen or n >= limit:
            continue
        seen.add(key)
        n += 1
        pl = pv.Plotter(off_screen=True, window_size=(1000, 760))
        pl.set_background("white")
        st = job["state"]
        if job["kind"] == "tool":
            i = job["screw"]
            F0, _ = CK.screw_frame(sc, i, st)
            Mk = F0
            centre = F0[:3, 3]
            meshes = tool_meshes(job["tool"], job["s"])
            for nm, m in meshes:
                m = m.copy()
                m.apply_transform(Mk)
                pl.add_mesh(pv.wrap(m), color="#e0201b" if nm == "tool" else "#ff9a9a", opacity=1.0 if nm == "tool" else 0.55)
            mov, hi = [i], None
        else:
            mov = job["mov"]
            Toff = CK.T(job["at"])
            pre = job.get("pre")
            pts = []
            for i in mov:
                o = sc.objs[i]
                if o["V"] is None:
                    continue
                Mi = Toff @ (pre if pre is not None else np.eye(4)) @ sc.pose(i, st)
                V = o["V"] @ Mi[:3, :3].T + Mi[:3, 3]
                pts.append(V)
                pl.add_mesh(pv.PolyData(V, np.hstack([np.full((len(o["F"]), 1), 3), o["F"]]).ravel()), color="#e0201b")
            centre = np.vstack(pts).mean(0) if pts else np.zeros(3)
            hi = job["blocker"]
        rad = 170.0
        w = CK.World(sc, st, [j for j in job["present"] if j not in mov])
        for j in w.near((centre - rad, centre + rad)):
            o = sc.objs[j]
            if o["V"] is None or j in mov:
                continue
            V = o["V"] @ w.M[j][:3, :3].T + w.M[j][:3, 3]
            col = "#f0a020" if j == hi else "#b8c0c8"
            op = 1.0 if j == hi else 0.35
            pl.add_mesh(pv.PolyData(V, np.hstack([np.full((len(o["F"]), 1), 3), o["F"]]).ravel()), color=col, opacity=op)
        pl.add_text(job["title"][:110], font_size=9, color="black")
        pl.camera.focal_point = tuple(centre)
        pl.camera.position = tuple(centre + np.array([260.0, -420.0, 260.0]))
        pl.camera.up = (0, 0, 1)
        fn = OUT / f"fail-{module}-{job['sid'].replace('.', '-')}.png"
        pl.screenshot(str(fn))
        pl.close()
        print("wrote", fn.name, flush=True)


def tool_meshes(kind, s):
    import tools as TL
    t = TL.lkey_short(s) if kind == "lkey_short" else TL.torque_sd(s)
    return list(t.tm.items())


if __name__ == "__main__":
    main(sys.argv[1:])
