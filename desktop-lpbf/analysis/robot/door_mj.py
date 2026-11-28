"""The chamber door's own motion in MuJoCo, for the robot cell (robot-ops.md): what the damper does once the robot lets go.

The door (every part of lpbf_low's "door" motion group: plate, cord, hinge leaves, strikes, handle, the damper's drive disc) is one
hinged body; its mass, centre of mass and inertia about the hinge come from the CAD (trimesh mass properties of each part at its
material's density, or its catalogue mass). Three runs:
  1. opening, no damper: released at 20 deg (the robot pulled it past its balance angle) and free to fall to its 95 deg stop;
  2. opening with the McMaster 6597K124 one-way rotary damper (2.0 +/- 0.4 N m; taken as a linear damper rated at 20 rpm, so
     c = 2.0 / 2.09 = 0.96 N m s/rad: an assumption, McMaster gives no speed for the rating);
  3. closing: released at 8 deg after the robot has lifted it, falling shut under its own weight onto the cord (the one-way
     damper does not act in this direction).
Writes analysis/out/robot/door_mj.json.

Run: python desktop-lpbf/analysis/robot/door_mj.py
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "cad"))
OUT = HERE.parent / "out" / "robot"


def door_inertia():
    import lpbf_low as M
    import trimesh
    parts = [p for p in M.build(module="M50") if p.group == "door"]
    hy, hz = M.DOOR_HINGE
    m_tot, mom, I = 0.0, np.zeros(3), 0.0
    rows = []
    for p in parts:
        vs, fs = p.shape.tessellate(0.2, 0.3)
        v = np.array([(q.x, q.y, q.z) for q in vs]) / 1000.0
        tm = trimesh.Trimesh(v, np.array(fs).reshape(-1, 3), process=True)
        rho = M.MAT.get(p.mat, {}).get("rho", 1000.0)
        vol = abs(tm.volume) if tm.is_volume else float(p.shape.Volume()) * 1e-9
        m = p.mass_kg if p.mass_kg is not None else vol * rho
        c = tm.center_mass if tm.is_volume else np.array(p.shape.Center().toTuple()) / 1000.0
        # inertia about the hinge axis (x through (hy, hz)): the part's own about its centroid (scaled to its mass) + parallel axis
        if tm.is_volume and vol > 0:
            Ic = tm.moment_inertia * (m / (abs(tm.volume) * 1.0)) / 1.0
            Ixx = float(Ic[0, 0])
        else:
            Ixx = 0.0
        r2 = (c[1] - hy / 1000.0) ** 2 + (c[2] - hz / 1000.0) ** 2
        I += Ixx + m * r2
        m_tot += m
        mom += m * c
        rows.append(dict(part=p.name[:70], kg=round(m, 3)))
    cg = mom / m_tot
    return dict(mass_kg=m_tot, cog_m=cg.tolist(), hinge_m=[hy / 1000.0, hz / 1000.0], I_hinge=I, parts=rows)


def simulate(d, start_deg, stop_deg, damping, close=False, t_end=6.0):
    import mujoco
    hy, hz = d["hinge_m"]
    cg = np.array(d["cog_m"])
    # body frame at the hinge axis; the door's centre of mass relative to it, at 0 deg (door shut)
    rc = cg - np.array([cg[0], hy, hz])
    I_c = max(d["I_hinge"] - d["mass_kg"] * (rc[1] ** 2 + rc[2] ** 2), 1e-6)
    hi = 95.0
    xml = f"""
<mujoco>
  <option timestep="0.0005" gravity="0 0 -9.81"/>
  <worldbody>
    <body name="door" pos="0 {hy} {hz}">
      <joint name="hinge" type="hinge" axis="1 0 0" range="0 {hi}" limited="true" damping="{damping}" solreflimit="0.004 1"/>
      <inertial pos="0 {rc[1]} {rc[2]}" mass="{d['mass_kg']}" diaginertia="{I_c} {I_c} {I_c}"/>
    </body>
  </worldbody>
</mujoco>"""
    m = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(m)
    # a positive angle about +x tips the top towards -y ((0,0,1) -> (0,-sin,cos)), as lpbf_low's door: positive = open
    data.qpos[0] = math.radians(start_deg)
    t, peak_w, hit_t, hit_w, ang = 0.0, 0.0, None, None, []
    stop = math.radians(stop_deg)
    while data.time < t_end:
        mujoco.mj_step(m, data)
        w = abs(float(data.qvel[0]))
        peak_w = max(peak_w, w)
        a = float(data.qpos[0])
        if hit_t is None and ((not close and a >= stop - 1e-3) or (close and a <= 1e-3)):
            hit_t, hit_w = float(data.time), w
        if len(ang) < 400 and int(data.time / 0.02) > len(ang):
            ang.append(round(math.degrees(a), 2))
    r_handle = math.hypot(-0.152 - hy, 0.095 - hz)
    return dict(start_deg=start_deg, damping_Nms_per_rad=damping, time_to_stop_s=(round(hit_t, 2) if hit_t else None),
                angular_speed_at_stop_rad_s=(round(hit_w, 3) if hit_w is not None else None),
                handle_speed_at_stop_m_s=(round(hit_w * r_handle, 3) if hit_w is not None else None),
                peak_angular_speed_rad_s=round(peak_w, 3), angle_every_20ms_deg=ang[:200])


def main():
    d = door_inertia()
    hy, hz = d["hinge_m"]
    cg = np.array(d["cog_m"])
    bal = math.degrees(math.atan2(cg[1] - hy, cg[2] - hz))
    res = dict(door=dict(mass_kg=round(d["mass_kg"], 3), cog_mm=[round(x * 1000, 1) for x in cg], I_hinge_kg_m2=round(d["I_hinge"], 5),
                         balance_deg=round(bal, 1), max_gravity_torque_Nm=round(d["mass_kg"] * 9.81 * math.hypot(cg[1] - hy, cg[2] - hz), 3),
                         parts=d["parts"]),
               damper=dict(product="McMaster 6597K124 one-way rotary damper", rated_Nm=2.0, assumed_rated_speed_rpm=20.0,
                           c_Nms_per_rad=round(2.0 / (20 * 2 * math.pi / 60), 3)))
    c = res["damper"]["c_Nms_per_rad"]
    res["open_free"] = simulate(d, 20.0, 95.0, 0.0)
    res["open_damped"] = simulate(d, 20.0, 95.0, c)
    res["close_from_8deg"] = simulate(d, 8.0, 95.0, 0.0, close=True)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "door_mj.json").write_text(json.dumps(res, indent=1))
    for k in ("open_free", "open_damped", "close_from_8deg"):
        r = res[k]
        print(k, {kk: r[kk] for kk in r if kk != "angle_every_20ms_deg"})
    print("door", {k: v for k, v in res["door"].items() if k != "parts"})


if __name__ == "__main__":
    main()
