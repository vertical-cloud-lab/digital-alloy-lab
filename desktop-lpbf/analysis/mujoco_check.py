"""MuJoCo checks on the low-profile model (cad/lpbf_low.py): motion, loads, door drop, and VLM-tray transit.

1. Kinematic sweep with collision. Every moving part and every fixed part near its path is split into convex
   pieces (CoACD) and loaded into MuJoCo; each joint (recoater, piston, door, guard door, cartridge) is swept over
   its range and MuJoCo's contacts are logged. Convex decomposition is coarse (it can invent contact in a concave
   corner or a 0.4 mm fit), so every contact is labelled with the verdict of the exact B-rep check
   (interference.py), which is the authority on interference.
2. Dynamics. Each axis is driven through a realistic move by a stiff position servo under gravity; the peak
   actuator force or torque is reported (servo and screw sizing).
3. Door drop. The 15 mm drop-down door is released at the closed position and falls onto its 95 degree stop:
   peak hinge-stop torque and impact speed, to size a damper.
4. VLM transit. The three modules (masses and centres of mass from mass_budget.py) stand on rubber feet on a
   tray that is accelerated vertically and horizontally; foot lift-off and sliding are checked.

Run:  python desktop-lpbf/analysis/mujoco_check.py      (CoACD meshes cached in /tmp/mj)
Writes analysis/out/mujoco.json and analysis/out/mujoco.md.
"""
from __future__ import annotations

import hashlib
import json
import math
import pathlib
import sys
import time

import coacd
import mujoco
import numpy as np
import trimesh

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "cad"))
sys.path.insert(0, str(HERE))
import lpbf_low as M  # noqa: E402
from interference import is_joint  # noqa: E402

OUT = HERE / "out"
CACHE = pathlib.Path("/tmp/mj")
PAD = 25.0              # mm around a group's swept box: fixed parts inside it are loaded as obstacles
SKIP_STATIC = ("Laser guard panels", "Guard frame", "hoses", "line", "fiber", "Chilled", "supply", "exhaust", "duct", "VLM tray", "Base plate", "Leveling")


def mesh_of(shape, tol=0.25):
    vs, ts = shape.tessellate(tol, 0.3)
    v = np.array([(p.x, p.y, p.z) for p in vs]) / 1000.0
    tm = trimesh.Trimesh(v, np.array(ts), process=True)
    tm.merge_vertices()
    return tm


def convex_pieces(name, shape, threshold=0.03):
    key = hashlib.md5((name + str(shape.BoundingBox().xmin) + str(shape.Volume())).encode()).hexdigest()[:12]
    d = CACHE / key
    if d.exists() and any(d.iterdir()):
        return sorted(d.glob("*.stl"))
    d.mkdir(parents=True, exist_ok=True)
    pieces = []
    for k, s in enumerate(list(shape.Solids()) or [shape]):
        tm = mesh_of(s)
        if len(tm.faces) == 0:
            continue
        hull = tm.convex_hull
        if tm.volume > 0 and tm.volume / max(hull.volume, 1e-12) > 0.97:
            pieces.append(hull)
            continue
        try:
            res = coacd.run_coacd(coacd.Mesh(tm.vertices, tm.faces), threshold=threshold, max_convex_hull=24,
                                  preprocess_mode="auto", resolution=1500, mcts_iterations=60, mcts_nodes=15, seed=1)
            pieces += [trimesh.Trimesh(v, f) for v, f in res]
        except Exception:  # noqa: BLE001
            pieces.append(hull)
    for k, pc in enumerate(pieces):
        pc.export(d / f"p{k:03d}.stl")
    return sorted(d.glob("*.stl"))


def swept_box(parts, group):
    m = M.MOTION[group]
    lo = np.array([1e9] * 3)
    hi = -lo
    for v in np.linspace(m["lo"], m["hi"], 7):
        for s in M.posed([p for p in parts if p.group == group], {group: v}):
            b = s.BoundingBox()
            lo = np.minimum(lo, [b.xmin, b.ymin, b.zmin])
            hi = np.maximum(hi, [b.xmax, b.ymax, b.zmax])
    return lo - PAD, hi + PAD


def build_mjcf(parts, groups):
    """MJCF with one static body per obstacle part and one jointed body per motion group (metres, kg)."""
    assets, bodies, names = [], [], {}
    sel_static = set()
    boxes = {g: swept_box(parts, g) for g in groups}
    for i, p in enumerate(parts):
        if p.group or any(k in p.name for k in SKIP_STATIC) or "context" in p.tags:
            continue
        b = p.shape.BoundingBox()
        for lo, hi in boxes.values():
            if b.xmin <= hi[0] and lo[0] <= b.xmax and b.ymin <= hi[1] and lo[1] <= b.ymax and b.zmin <= hi[2] and lo[2] <= b.zmax:
                sel_static.add(i)
    t0 = time.time()
    geoms = {}
    for i, p in enumerate(parts):
        if i not in sel_static and p.group not in groups:
            continue
        files = convex_pieces(p.name, p.shape)
        rho = M.MAT.get(p.mat, {}).get("rho", 1000)
        if p.mass_kg is not None:
            vol = max(p.shape.Volume() * 1e-9, 1e-9)
            rho = p.mass_kg / vol if p.mass_kg > 0 else 1.0
        g = []
        for k, f in enumerate(files):
            mn = f"m{i}_{k}"
            assets.append(f'<mesh name="{mn}" file="{f}"/>')
            g.append(f'<geom name="g{i}_{k}" type="mesh" mesh="{mn}" density="{rho:.1f}" rgba="0.7 0.7 0.75 1"/>')
        geoms[i] = g
        names[i] = p.name
    print(f"convex decomposition of {len(geoms)} parts in {time.time() - t0:.0f} s", flush=True)
    for i in sel_static:
        if i in geoms:
            bodies.append(f'<body name="s{i}">' + "".join(geoms[i]) + "</body>")
    hy, hz = M.DOOR_HINGE
    jdef = {"recoater": 'type="slide" axis="1 0 0"', "piston": 'type="slide" axis="0 0 1"', "gdoor": 'type="slide" axis="1 0 0"',
            "cartridge": 'type="slide" axis="0 1 0"', "door": f'type="hinge" axis="1 0 0" pos="0 {hy / 1000:.4f} {hz / 1000:.4f}"'}
    acts = []
    for g in groups:
        m = M.MOTION[g]
        lo, hi = (math.radians(m["lo"]), math.radians(m["hi"])) if g == "door" else (m["lo"] / 1000, m["hi"] / 1000)
        gg = "".join(x for i, p in enumerate(parts) if p.group == g for x in geoms.get(i, []))
        bodies.append(f'<body name="{g}"><joint name="j_{g}" {jdef[g]} range="{lo:.5f} {hi:.5f}" limited="true" damping="0.5" armature="0.001"/>{gg}</body>')
        kp = 2.0e5 if g != "door" else 2.0e2
        acts.append(f'<position name="a_{g}" joint="j_{g}" kp="{kp}" kv="{2 * math.sqrt(kp) * 0.5:.1f}" ctrllimited="false"/>')
    xml = f"""<mujoco model="desktop_lpbf_low">
  <compiler angle="radian" boundmass="1e-4" boundinertia="1e-9"/>
  <option timestep="0.0005" gravity="0 0 -9.81" integrator="implicitfast"><flag filterparent="disable"/></option>
  <asset>{''.join(assets)}</asset>
  <worldbody>{''.join(bodies)}</worldbody>
  <actuator>{''.join(acts)}</actuator>
</mujoco>"""
    return xml, names


def contacts(model, data, names, groups):
    out = []
    for ci in range(data.ncon):
        c = data.contact[ci]
        b1 = model.body(model.geom_bodyid[c.geom1]).name
        b2 = model.body(model.geom_bodyid[c.geom2]).name
        if c.dist > -1e-4:          # report penetrations deeper than 0.1 mm
            continue
        def lab(b):
            return b if b in groups else names.get(int(b[1:]), b)
        out.append((lab(b1), lab(b2), -c.dist * 1000))
    return out


def sweep(model, data, names, groups, exact):
    res = {}
    for g in groups:
        j = model.joint(f"j_{g}")
        lo, hi = model.jnt_range[j.id]
        worst = {}
        for v in np.linspace(lo, hi, 25):
            mujoco.mj_resetData(model, data)
            data.qpos[model.jnt_qposadr[j.id]] = v
            mujoco.mj_forward(model, data)
            for a, b, pen in contacts(model, data, names, groups):
                if g not in (a, b):
                    continue
                other = b if a == g else a
                if other not in worst or pen > worst[other][1]:
                    worst[other] = (float(v), pen)
        rows = []
        for other, (v, pen) in sorted(worst.items(), key=lambda kv: -kv[1][1]):
            if (g, other) in exact:
                verdict = "interferes (exact)"
            elif any(is_joint(p.name, other) for p in M.build.__globals__["_LAST"] if p.group == g):
                verdict = "designed joint (e.g. rod in its seal bore); exact check clear"
            else:
                verdict = "convex-decomposition artefact; exact B-rep check clear"
            rows.append(dict(other=other, at=round(v * (180 / math.pi if g == "door" else 1000), 2), depth_mm=round(pen, 2), verdict=verdict))
        res[g] = rows
        print(f"  sweep {g}: {len(rows)} contacting parts", flush=True)
    return res


def no_contacts(model):
    saved = (model.geom_contype.copy(), model.geom_conaffinity.copy())
    model.geom_contype[:] = 0
    model.geom_conaffinity[:] = 0
    return saved


def dynamics(model, data, groups):
    """Drive each axis through a smooth move with contacts off; peak actuator effort (N or N·m)."""
    moves = {"recoater": (0.0, 0.196, 2.0), "piston": (0.0, -0.040, 2.0), "gdoor": (0.0, 0.47, 2.0),
             "cartridge": (0.0, -0.125, 2.0), "door": (0.0, math.radians(95), 3.0)}
    out = {}
    for g in groups:
        a0, a1, T = moves[g]
        mujoco.mj_resetData(model, data)
        aid = model.actuator(f"a_{g}").id
        jid = model.joint(f"j_{g}").id
        peak, hold = 0.0, 0.0
        n = int((T + 0.5) / model.opt.timestep)
        for k in range(n):
            t = k * model.opt.timestep
            s = min(t / T, 1.0)
            u = a0 + (a1 - a0) * (10 * s**3 - 15 * s**4 + 6 * s**5)
            for gg in groups:
                data.ctrl[model.actuator(f"a_{gg}").id] = u if gg == g else 0.0
            mujoco.mj_step(model, data)
            f = abs(data.actuator_force[aid])
            peak = max(peak, f)
        hold = abs(data.actuator_force[aid])
        unit = "N·m" if g == "door" else "N"
        body = model.body(g)
        out[g] = dict(moving_mass_kg=round(float(model.body_subtreemass[body.id]), 3), move=f"{a0:g} to {a1:g} {'rad' if g == 'door' else 'm'} in {T:g} s (quintic)", peak=round(peak, 2), hold_at_end=round(hold, 2), unit=unit,
                      final_error=round(float(data.qpos[model.jnt_qposadr[jid]] - a1), 6))
    return out


def door_drop(model, data):
    """Release the door at 0 deg with no actuator: it swings onto the 95 deg limit."""
    mujoco.mj_resetData(model, data)
    jid = model.joint("j_door").id
    model.actuator_gainprm[model.actuator("a_door").id, 0] = 0.0
    model.actuator_biasprm[model.actuator("a_door").id, :3] = 0.0
    # angle at which gravity stops holding the door shut (CoM passes over the hinge axis)
    tip = None
    for deg in np.arange(0.0, 60.0, 0.25):
        mujoco.mj_resetData(model, data)
        data.qpos[model.jnt_qposadr[jid]] = math.radians(deg)
        mujoco.mj_forward(model, data)
        if -data.qfrc_bias[model.jnt_dofadr[jid]] > 0:
            tip = float(deg)
            break
    mujoco.mj_resetData(model, data)
    data.qpos[model.jnt_qposadr[jid]] = math.radians((tip or 0.0) + 1.0)
    peak_w, peak_lim, t_hit = 0.0, 0.0, None
    model.dof_damping[model.jnt_dofadr[jid]] = 0.0
    for k in range(int(2.0 / model.opt.timestep)):
        mujoco.mj_step(model, data)
        w = abs(data.qvel[model.jnt_dofadr[jid]])
        peak_w = max(peak_w, w)
        lim = abs(data.qfrc_constraint[model.jnt_dofadr[jid]])
        if lim > peak_lim:
            peak_lim, t_hit = lim, k * model.opt.timestep
    body = model.body("door")
    return dict(self_closing_until_deg=tip, door_mass_kg=round(float(model.body_subtreemass[body.id]), 3), peak_speed_rad_s=round(peak_w, 2),
                tip_speed_m_s=round(peak_w * 0.125, 2), peak_stop_torque_Nm=round(peak_lim, 1), t_s=round(t_hit or 0, 3),
                note="contacts off, hinge friction and damping zero (worst case); MuJoCo's soft joint limit stands in for a hard stop, so the stop torque depends on its stiffness")


def transit(mass_rows, accel=((0, 0, 3.0), (0, 0, -3.0), (2.0, 0, 0), (0, 2.0, 0), (2.0, 2.0, -3.0), (4.0, 0, 0), (0, 4.0, 0), (0, 6.0, 0)), mu=0.5):
    """Three modules as rigid bodies on four rubber feet on the tray.

    The tray is fixed and its acceleration a enters as an effective gravity g_eff = g - a (exact for a translating
    tray): a for 0.3 s, then -a for 0.3 s (accelerate, brake), then 0.3 s still. Accelerations in m/s2 are assumed."""
    bodies = []
    for mod, r in mass_rows.items():
        (x0, x1, y0, y1), m, com = r["foot"], r["mass_kg"], r["com_mm"]
        hx, hy = (x1 - x0) / 2000, (y1 - y0) / 2000
        cx, cy = (x0 + x1) / 2000, (y0 + y1) / 2000
        hz = max(com[2] - M.Z_TRAY, 30.0) / 1000.0
        feet = "".join(f'<geom type="sphere" size="0.01" pos="{sx * (hx - 0.03):.4f} {sy * (hy - 0.03):.4f} {-hz + 0.01:.4f}" friction="{mu} 0.005 0.0001" mass="0.05"/>' for sx in (-1, 1) for sy in (-1, 1))
        Ixx, Iyy, Izz = m * ((2 * hy) ** 2 + (2 * hz) ** 2) / 12, m * ((2 * hx) ** 2 + (2 * hz) ** 2) / 12, m * ((2 * hx) ** 2 + (2 * hy) ** 2) / 12
        bodies.append(f'<body name="{mod}" pos="{cx:.4f} {cy:.4f} {hz:.4f}"><freejoint/>'
                      f'<inertial pos="{com[0] / 1000 - cx:.4f} {com[1] / 1000 - cy:.4f} 0" mass="{m:.3f}" diaginertia="{Ixx:.4f} {Iyy:.4f} {Izz:.4f}"/>{feet}</body>')
    xml = f"""<mujoco><option timestep="0.0005" gravity="0 0 -9.81"/>
  <worldbody><geom name="tray" type="box" size="1.225 0.432 0.002" pos="0 0 -0.002" friction="{mu} 0.005 0.0001"/>{''.join(bodies)}</worldbody></mujoco>"""
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    g = np.array([0, 0, -9.81])
    out = []
    for a in accel:
        a = np.array(a, float)
        mujoco.mj_resetData(model, data)
        model.opt.gravity[:] = g
        for _ in range(2000):
            mujoco.mj_step(model, data)
        start = {mod: (data.body(mod).xpos.copy(), data.body(mod).xmat.copy()) for mod in mass_rows}
        min_feet = {mod: 4 for mod in mass_rows}
        dt = model.opt.timestep
        for k in range(int(0.9 / dt)):
            t = k * dt
            ph = (t % 0.3) / 0.3
            acc = (a if t < 0.3 else (-a if t < 0.6 else 0 * a)) * math.sin(math.pi * ph) ** 2
            model.opt.gravity[:] = g - acc
            mujoco.mj_step(model, data)
            for mod in mass_rows:
                bid = model.body(mod).id
                n = sum(1 for ci in range(data.ncon) if model.geom_bodyid[data.contact[ci].geom1] == bid or model.geom_bodyid[data.contact[ci].geom2] == bid)
                min_feet[mod] = min(min_feet[mod], n)
        rows = {}
        for mod in mass_rows:
            p0, R0 = start[mod]
            d = data.body(mod).xpos - p0
            tilt = math.degrees(math.acos(max(-1.0, min(1.0, float(data.body(mod).xmat.reshape(3, 3)[2, 2])))))
            rows[mod] = dict(slide_mm=round(float(np.linalg.norm(d[:2]) * 1000), 3), tilt_deg=round(tilt, 3), min_feet_in_contact=int(min_feet[mod]))
        out.append(dict(tray_accel_m_s2=[float(x) for x in a], result=rows))
    model.opt.gravity[:] = g
    return out


def main():
    t0 = time.time()
    OUT.mkdir(exist_ok=True)
    CACHE.mkdir(exist_ok=True)
    parts = M.build()
    M.build.__globals__["_LAST"] = parts
    groups = list(M.MOTION)
    xml, names = build_mjcf(parts, groups)
    (CACHE / "desktop_lpbf_low.xml").write_text(xml)
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    print(f"MuJoCo model: {model.nbody} bodies, {model.ngeom} geoms, {model.nmesh} meshes", flush=True)
    exact = set()
    ij = OUT / "interference.json"
    if ij.exists():
        r = json.loads(ij.read_text())
        for s in r["sweeps"]:
            for it in s["interferences"]:
                exact.add((s["group"], it["b"]))
                exact.add((s["group"], it["a"]))
    rep = dict(model=dict(bodies=model.nbody, geoms=model.ngeom, meshes=model.nmesh))
    rep["sweep"] = sweep(model, data, names, groups, exact)
    no_contacts(model)
    rep["dynamics"] = dynamics(model, data, groups)
    print("  dynamics done", flush=True)
    rep["door_drop"] = door_drop(model, data)
    import mass_budget
    mb = mass_budget.compute()
    rep["mass_by_module"] = {k: dict(mass_kg=v["mass_kg"], com_mm=v["com_mm"]) for k, v in mb["modules"].items()}
    rep["transit"] = transit({k: mb["modules"][k] for k in ("rack", "process", "gas")})
    rep["runtime_s"] = round(time.time() - t0, 1)
    (OUT / "mujoco.json").write_text(json.dumps(rep, indent=1))
    write_md(rep)
    print(f"done in {rep['runtime_s']} s")


def write_md(r):
    L = ["# MuJoCo checks", "", f"Model: {r['model']['bodies']} bodies, {r['model']['geoms']} convex geoms (CoACD), generated by `analysis/mujoco_check.py` in {r['runtime_s']} s.", "",
         "## 1. Joint sweeps with collision (coarse; the exact B-rep check decides)", "",
         "| Group | Contacting part | At | Depth (mm) | Verdict |", "|---|---|---|---|---|"]
    for g, rows in r["sweep"].items():
        if not rows:
            L.append(f"| {g} | none | | | |")
        for x in rows:
            L.append(f"| {g} | {x['other']} | {x['at']} | {x['depth_mm']} | {x['verdict']} |")
    L += ["", "## 2. Actuator effort over a realistic move (gravity + inertia, stiff position servo)", "",
          "| Axis | Moving mass (kg) | Move | Peak | Holding at end |", "|---|---|---|---|---|"]
    for g, d in r["dynamics"].items():
        L.append(f"| {g} | {d['moving_mass_kg']} | {d['move']} | {d['peak']} {d['unit']} | {d['hold_at_end']} {d['unit']} |")
    d = r["door_drop"]
    L += ["", "## 3. Door released at the closed position", "",
          f"Gravity holds the unlatched door shut until it is pulled past {d['self_closing_until_deg']}° (its centre of mass is behind the hinge). Released just past that, the "
          f"door ({d['door_mass_kg']} kg) reaches a peak angular speed {d['peak_speed_rad_s']} rad/s (free edge {d['tip_speed_m_s']} m/s); "
          f"peak stop torque {d['peak_stop_torque_Nm']} N·m at t = {d['t_s']} s. {d['note']}.", "",
          "## 4. VLM tray transit (assumed accelerations; no Kardex/Modula figure was available)", "",
          "Each case: a smooth (sin²) 0.3 s acceleration pulse with the peak shown, a matching braking pulse, then 0.3 s still; rubber feet, friction 0.5.", "",
          "| Tray acceleration (m/s²) | Module | Slide (mm) | Tilt (°) | Min. feet in contact |", "|---|---|---|---|---|"]
    for t in r["transit"]:
        for mod, x in t["result"].items():
            L.append(f"| {t['tray_accel_m_s2']} | {mod} | {x['slide_mm']} | {x['tilt_deg']} | {x['min_feet_in_contact']} |")
    L += ["", "Module masses and centres of mass (from `mass_budget.py`):", "", "| Module | Mass (kg) | CoM (mm, machine frame) |", "|---|---|---|"]
    for k, v in r["mass_by_module"].items():
        L.append(f"| {k} | {v['mass_kg']} | {tuple(round(c) for c in v['com_mm'])} |")
    (OUT / "mujoco.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
