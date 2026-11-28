"""Laser heat in the heated build modules: does the beam push the plate past its set point? (issue #260, PR #266)

The module thermal FEA (thermal_module.py) sizes the heaters with the laser off. During a build, the beam's absorbed
power reaches the plate through the part, and averaged over a layer cycle it is of the same size as the module's whole
loss at 200 C (44-97 W). If it is larger, the heater controller switches off and the plate drifts above its set point,
with nothing to take the heat away. This script answers, for each module (S25, M50, L75) at build start (z_p = 0) and
build end (z_p = -40):
  - the time-averaged absorbed laser power for a sparse and a dense screening layout (from scan rate and recoat time);
  - with that power deposited in the plate (the part conducts it down: solid Al, k ~ 150 W/m K, against the powder's
    0.2), the plate temperature with the heater off, or the heater power still needed to hold 200 C;
  - what the bore seal, spigot O-ring, rod-gland O-rings, the Z-coupling magnet face, the block (TCO) and the hot
    plate-to-bore clearance see.

It reuses thermal_module.py's geometry, mesh, materials and boundary conditions unchanged; the only addition is a
body flux in the plate region (R_PLATE) for the laser.

Assumptions (all named below): AlSi10Mg at 350 W, 1300 mm/s, 0.13 mm hatch (169 mm2/s of scanned area);
absorptance 0.45 (conduction to transition mode; 0.6 in keyhole as the sensitivity); 0.2 s per layer of jumps and
skywriting; a recoat cycle of 8 s (206 mm stroke out and back at ~75 mm/s, plus dosing); sparse layout 25 % of the
plate area, dense 70 %.

Run:  OMP_NUM_THREADS=1 python desktop-lpbf/analysis/thermal_laser.py         (~11 min, one core)
      python desktop-lpbf/analysis/thermal_laser.py report                     (tables and plot from the .json)
      OMP_NUM_THREADS=1 python desktop-lpbf/analysis/thermal_laser.py jacket  (the cooling fix, ~6 min; needs the .json)
      -> desktop-lpbf/analysis/out/thermal/laser_heat.{md,json,png}
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
os.environ.setdefault("THERMAL_RUN", "/tmp/thermal-laser")
import thermal_module as TM  # noqa: E402

MP = TM.MP
OUT = HERE / "out" / "thermal"
TM.RUN.mkdir(parents=True, exist_ok=True)

P_LASER, V_SCAN, HATCH = 350.0, 1300.0, 0.13      # W, mm/s, mm
ABS, ABS_KEYHOLE = 0.45, 0.60
T_JUMP, T_RECOAT = 0.2, 8.0                       # s per layer
FILL = {"sparse (25 % of the plate)": 0.25, "dense (70 % of the plate)": 0.70}
Q_GRID = [0.0, 30.0, 60.0, 90.0, 120.0, 150.0]   # W absorbed, time-averaged


def absorbed_w(key, fill, absorptance=ABS):
    a_plate = math.pi * (MP.MODULES[key]["plate_d"] / 2) ** 2
    t_scan = fill * a_plate / (V_SCAN * HATCH) + T_JUMP
    f_on = t_scan / (t_scan + T_RECOAT)
    return absorptance * P_LASER * f_on, f_on, t_scan


def plate_volume_mm3(mesh):
    v = 0.0
    for e in mesh.region("plate"):
        i, j = mesh.I[e], mesh.J[e]
        r0, r1, z0, z1 = mesh.rl[i], mesh.rl[i + 1], mesh.zl[j], mesh.zl[j + 1]
        v += math.pi * (r1 ** 2 - r0 ** 2) * (z1 - z0)
    return v


def solve(mesh, case, P_heater, Q_laser, Vp, job, T0=None):
    par = TM.write_inp(job, mesh, case, P_heater, T0=T0)
    p = TM.RUN / f"{job}.inp"
    txt = p.read_text()
    if Q_laser > 0:
        add = f"*DFLUX\nR_PLATE, BF, {Q_laser * 1e3 / Vp:.8g}\n"
        txt = txt.replace("*FILM\n", add + "*FILM\n", 1)
        p.write_text(txt)
    TM.run_ccx(job)
    T = np.full(mesh.used.sum() + 1, np.nan)
    rfl = {}
    for kind, s, t, rows in TM.read_dat(job):
        if kind == "temperatures":
            a = np.array(rows)
            T[a[:, 0].astype(int)] = a[:, 1]
        elif kind.startswith("total heat generation"):
            rfl[s] = rows[0][0] * 180 * 1e-3
    return T, rfl, par


def case_at(key, z_p, Q, Vp_cache={}):
    pos = "start" if z_p == 0 else "end"
    case = dict(name=f"laser_{key}_{pos}_{Q:.0f}", key=key, z_p=z_p, pos=pos, T_set=MP.T_SET_A, T_ch=25.0,
                eps=TM.EPS_POWDER)
    g = TM.geometry(key, z_p, "A", "ARGON", None, None)
    mesh = TM.Mesh(g, TM.H0)
    Vp = plate_volume_mm3(mesh)
    nc, _ = TM.centre_node(mesh)
    job = case["name"]
    # heater off first: if the laser alone holds the plate at or above the set point, that's the answer
    T, rfl, par = solve(mesh, case, 0.0, Q, Vp, job)
    P = 0.0
    if T[nc] < MP.T_SET_A - 0.05:
        hist = [(0.0, T[nc])]
        P = max(5.0, 0.6 * (MP.T_SET_A - 25.0) * MP.MODULES[key]["bore"] / 50.8 - Q)
        T0 = T
        for _ in range(12):
            T, rfl, par = solve(mesh, case, P, Q, Vp, job, T0=T0)
            hist.append((P, T[nc]))
            if abs(T[nc] - MP.T_SET_A) < 0.05:
                break
            (p1, t1), (p2, t2) = hist[-2], hist[-1]
            P = max(0.0, p2 + (MP.T_SET_A - t2) * (p2 - p1) / (t2 - t1))
            T0 = T
    r = TM.post(mesh, case, P_w=max(P + Q, 1e-6), T=T, rfl=rfl, par=par)
    keep = ("T_plate_centre", "T_plate_edge", "T_block_max", "T_seal_max", "T_oring_max", "T_gland_max",
            "T_rod_end", "T_plate_mean", "T_bore_ring_mean", "clear_plate_hot_mm", "into_chamber_W")
    out = {k: (round(float(r[k]), 3) if k == "clear_plate_hot_mm" else round(float(r[k]), 1)) for k in keep}
    out.update(key=key, pos=pos, Q_laser_W=Q, P_heater_W=round(P, 1),
               heater_off=bool(P == 0.0), sinks_W={k: round(v, 1) for k, v in r["sinks_W"].items()},
               balance_W=round(sum(r["sinks_W"].values()) - (P + Q), 2))
    return out


def q_for_limit(rows, field, limit):
    """Absorbed laser power at which `field` reaches `limit` (linear interpolation over the heater-off rows)."""
    pts = [(r["Q_laser_W"], r[field]) for r in rows]
    for (q0, t0), (q1, t1) in zip(pts, pts[1:]):
        if (t0 - limit) * (t1 - limit) <= 0 and t1 != t0:
            return q0 + (limit - t0) * (q1 - q0) / (t1 - t0)
    return None


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    loads = {}
    for key in MP.MODULES:
        loads[key] = {}
        for name, f in FILL.items():
            q, f_on, t_scan = absorbed_w(key, f)
            qk, _, _ = absorbed_w(key, f, ABS_KEYHOLE)
            loads[key][name] = dict(Q_W=round(q, 1), Q_keyhole_W=round(qk, 1), beam_on=round(f_on, 3),
                                    t_scan_s=round(t_scan, 2))
    rows = []
    for key in MP.MODULES:
        for z_p in (0.0, -MP.BUILD_STROKE):
            for Q in Q_GRID:
                r = case_at(key, z_p, Q)
                rows.append(r)
                print(f"{key} {r['pos']:5s} Q={Q:5.0f} W  heater={r['P_heater_W']:6.1f} W  plate={r['T_plate_centre']:6.1f}"
                      f"  block={r['T_block_max']:6.1f}  gland={r['T_gland_max']:6.1f}  magnet={r['T_rod_end']:6.1f}"
                      f"  clear={r['clear_plate_hot_mm'] * 1000:6.1f} um  bal={r['balance_W']:+.2f}", flush=True)
    summary = summarize(rows)
    data = dict(assumptions=dict(P_laser_W=P_LASER, v_scan_mm_s=V_SCAN, hatch_mm=HATCH, absorptance=ABS,
                                 absorptance_keyhole=ABS_KEYHOLE, t_jump_s=T_JUMP, t_recoat_s=T_RECOAT, fills=FILL,
                                 T_chamber_C=25.0, limits=TM.LIMITS),
                laser_loads=loads, rows=rows, summary=summary, seconds=round(time.time() - t0))
    (OUT / "laser_heat.json").write_text(json.dumps(data, indent=1, default=float))
    report(data)
    plot(data)
    print(f"done in {time.time() - t0:.0f} s")


def summarize(rows):
    """Per module and position: the absorbed laser power at which the heater switches off (extrapolated from the
    heater-on runs: heater power falls about 1:1 with laser power, since both heat the plate) and at which each limit
    is reached (interpolated over the heater-off runs)."""
    lim = TM.LIMITS
    summary = {}
    for key in MP.MODULES:
        for pos in ("start", "end"):
            rr = [r for r in rows if r["key"] == key and r["pos"] == pos]
            on = [r for r in rr if not r["heater_off"]]
            if len(on) >= 2:
                (q1, p1), (q2, p2) = (on[-2]["Q_laser_W"], on[-2]["P_heater_W"]), (on[-1]["Q_laser_W"], on[-1]["P_heater_W"])
                q_off = q2 + p2 * (q2 - q1) / max(p1 - p2, 1e-6)
            else:
                q_off = on[-1]["Q_laser_W"] + on[-1]["P_heater_W"]
            base = on[-1:] + [r for r in rr if r["heater_off"]]
            summary[f"{key}_{pos}"] = dict(
                laser_off_heater_W=on[0]["P_heater_W"], heater_off_from_W=round(q_off, 0),
                Q_magnet_80C=q_for_limit(base, "T_rod_end", lim["magnet"]),
                Q_gland_150C=q_for_limit(base, "T_gland_max", lim["oring_pref"]),
                Q_gland_200C=q_for_limit(base, "T_gland_max", lim["gland"]),
                Q_tco=q_for_limit(base, "T_block_max", lim["tco"]),
                Q_clear_25um=q_for_limit(base, "clear_plate_hot_mm", 0.025),
                Q_clear_0=q_for_limit(base, "clear_plate_hot_mm", 0.0))
    return summary


def max_fill(key, q_limit, absorptance=ABS):
    """Largest scanned share of the plate area per layer whose time-averaged absorbed power stays under q_limit."""
    a_plate = math.pi * (MP.MODULES[key]["plate_d"] / 2) ** 2
    f_on = q_limit / (absorptance * P_LASER)
    if f_on >= 1:
        return 1.0
    t_scan = f_on * T_RECOAT / (1 - f_on)
    return max(0.0, (t_scan - T_JUMP) * V_SCAN * HATCH / a_plate)


def fmt(v, unit=" W", nd=0):
    return "–" if v is None else f"{v:.{nd}f}{unit}"


def report(data):
    lim = data["assumptions"]["limits"]
    L = ["# Laser heat in the heated build modules", "",
         "Generated by [`analysis/thermal_laser.py`](../../thermal_laser.py) (CalculiX, axisymmetric; the geometry, mesh, "
         "materials and boundary conditions of [`thermal_module.py`](../../thermal_module.py), plus a body flux in the "
         "plate for the beam's time-averaged absorbed power). Chamber 25 °C, powder ε 0.5. The heater holds the plate "
         "centre at 200 °C until the laser alone keeps it there; past that point the heater is off and the plate drifts up.",
         "", "## How much laser heat a build puts in", "",
         f"AlSi10Mg at {P_LASER:.0f} W, {V_SCAN:.0f} mm/s, {HATCH} mm hatch ({V_SCAN * HATCH:.0f} mm²/s scanned), "
         f"absorptance {ABS} ({ABS_KEYHOLE} in keyhole mode), {T_JUMP} s of jumps per layer, an {T_RECOAT:.0f} s recoat "
         "cycle. Time-averaged absorbed power (W), beam-on fraction in brackets:", "",
         "| Module | " + " | ".join(FILL) + " | Module loss at 200 °C, laser off (thermal.md, start / end) |",
         "|---|" + "---|" * len(FILL) + "---|"]
    loss = {"S25": "44 / 30", "M50": "72 / 52", "L75": "97 / 71"}
    for key, d in data["laser_loads"].items():
        L.append(f"| {key} | " + " | ".join(f"{v['Q_W']:.0f} ({v['beam_on']:.0%}); keyhole {v['Q_keyhole_W']:.0f}"
                                            for v in d.values()) + f" | {loss[key]} |")
    L += ["", "## What the module sees", "",
          "| Module, position | Laser (W) | Heater (W) | Plate centre (°C) | Block max (°C, TCO 240) | Bore seal (°C) | "
          "Spigot O-ring (°C) | Rod-gland O-rings (°C, FKM 200, 150 preferred) | Magnet face (°C, NdFeB 80) | "
          "Hot plate clearance (µm) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in data["rows"]:
        L.append(f"| {r['key']} {r['pos']} | {r['Q_laser_W']:.0f} | {r['P_heater_W']:.0f}{' (off)' if r['heater_off'] else ''} | "
                 f"{r['T_plate_centre']:.0f} | {r['T_block_max']:.0f} | {r['T_seal_max']:.0f} | {r['T_oring_max']:.0f} | "
                 f"{r['T_gland_max']:.0f} | {r['T_rod_end']:.0f} | {r['clear_plate_hot_mm'] * 1000:.0f} |")
    L += ["", "## Laser power at which each limit is reached (W absorbed, time-averaged)", "",
          "| Module, position | Heater switches off | Magnet face 80 °C | Rod gland 150 °C | Rod gland 200 °C | "
          "Block TCO 240 °C | Plate clearance 25 µm | Plate clearance 0 (seizes) |", "|---|---|---|---|---|---|---|---|"]
    for k, s in data["summary"].items():
        L.append(f"| {k.replace('_', ' ')} | {fmt(s['heater_off_from_W'])} | {fmt(s['Q_magnet_80C'])} | "
                 f"{fmt(s['Q_gland_150C'])} | {fmt(s['Q_gland_200C'])} | {fmt(s['Q_tco'])} | {fmt(s['Q_clear_25um'])} | "
                 f"{fmt(s['Q_clear_0'])} |")
    L += ["", "## Densest layout that keeps the plate at its set point", "",
          "Scanned share of the plate area per layer at which the time-averaged absorbed power equals the module's "
          "laser-off loss (the heater has just switched off), with the scan and recoat assumptions above:", "",
          "| Module | Build start, absorptance 0.45 | Build end, 0.45 | Build end, keyhole 0.6 |", "|---|---|---|---|"]
    for key in MP.MODULES:
        s0, s1 = data["summary"][f"{key}_start"], data["summary"][f"{key}_end"]
        L.append(f"| {key} | {max_fill(key, s0['heater_off_from_W']):.0%} | {max_fill(key, s1['heater_off_from_W']):.0%} | "
                 f"{max_fill(key, s1['heater_off_from_W'], ABS_KEYHOLE):.0%} |")
    L += jacket_section(data)
    L += ["", "A dash means the limit isn't reached inside the swept range (0-150 W). Heat balance closes to within "
          f"{max(abs(r['balance_W']) for r in data['rows']):.2f} W in every run.", ""]
    (OUT / "laser_heat.md").write_text("\n".join(L) + "\n")


def plot(data):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.2), sharey=False)
    colors = {"S25": "#4C78A8", "M50": "#F58518", "L75": "#54A24B"}
    for ax, (field, lab, limit) in zip(axs, (("T_plate_centre", "Plate centre (°C)", 200.0),
                                             ("T_gland_max", "Rod-gland O-rings (°C)", 150.0),
                                             ("T_rod_end", "Z-coupling magnet face (°C)", 80.0))):
        for key in MP.MODULES:
            for pos, ls in (("start", "-"), ("end", "--")):
                rr = [r for r in data["rows"] if r["key"] == key and r["pos"] == pos]
                ax.plot([r["Q_laser_W"] for r in rr], [r[field] for r in rr], ls, color=colors[key], marker="o", ms=3,
                        label=f"{key} {pos}")
            for name, d in data["laser_loads"][key].items():
                if "dense" in name:
                    ax.axvline(d["Q_W"], color=colors[key], lw=0.8, alpha=0.5)
        ax.axhline(limit, color="#888", lw=1, ls=":")
        ax.set_xlabel("time-averaged absorbed laser power (W)")
        ax.set_title(lab, fontsize=10)
        ax.grid(alpha=0.25)
    axs[0].legend(fontsize=7, ncol=2)
    fig.suptitle("Laser heat in the build modules: heater holds 200 °C until it switches off (thin lines: dense layout)",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "laser_heat.png", dpi=110)


JACKETS = {"natural convection (as drawn)": (5.0, 25.0), "fan on the module under the floor": (40.0, 25.0),
           "water jacket on the module (30 C water)": (300.0, 30.0)}


def jacket():
    """The fix: take heat out of the module's outside below the floor (tube, flange, gland plate, rod). For each
    module and position: the heater power that holds 200 C with the laser off (= the absorbed laser power at which the
    heater switches off), and what the module sees at the dense layout's laser power with the heater off."""
    t0 = time.time()
    h0, T0 = TM.H_UNDER, TM.T_ROOM
    d = json.loads((OUT / "laser_heat.json").read_text())
    res = []
    for name, (h, Tj) in JACKETS.items():
        TM.H_UNDER, TM.T_ROOM = h, Tj
        for key in MP.MODULES:
            q_dense = d["laser_loads"][key]["dense (70 % of the plate)"]["Q_W"]
            for z_p in (0.0, -MP.BUILD_STROKE):
                r0 = case_at(key, z_p, 0.0)
                r1 = case_at(key, z_p, q_dense)
                res.append(dict(jacket=name, h=h, T_coolant=Tj, key=key, pos=r0["pos"],
                                heater_at_laser_off_W=r0["P_heater_W"],
                                installed_W=MP.MODULES[key]["heaters"] * MP.MODULES[key]["heater_w"],
                                laser_off=r0, dense=r1, Q_dense_W=q_dense))
                print(f"{name[:22]:22s} {key} {r0['pos']:5s} heater@Q0={r0['P_heater_W']:6.1f} W | dense Q={q_dense:5.1f}:"
                      f" heater={r1['P_heater_W']:5.1f} plate={r1['T_plate_centre']:6.1f} gland={r1['T_gland_max']:6.1f}"
                      f" magnet={r1['T_rod_end']:6.1f} clear={r1['clear_plate_hot_mm'] * 1000:5.1f} um", flush=True)
    TM.H_UNDER, TM.T_ROOM = h0, T0
    d["jacket"] = dict(cases=res, seconds=round(time.time() - t0))
    (OUT / "laser_heat.json").write_text(json.dumps(d, indent=1, default=float))
    report(d)


def jacket_section(d):
    if "jacket" not in d:
        return []
    L = ["", "## The fix: take heat out of the module below the floor", "",
         "Same model, with the module's outside below the chamber floor (tube, flange, gland plate, rod) cooled harder: "
         "h = 5 W/m²K is the natural convection the model has now; 40 W/m²K is a small fan blowing on the module "
         "under the floor; 300 W/m²K at 30 °C stands for a water jacket on the tube. 'Laser off' is the heater power "
         "that holds 200 °C (it is also the absorbed laser power at which the heater switches off); 'dense' is the "
         "dense layout's laser power from the first table.", "",
         "| Cooling | Module, position | Heater at laser off (W) / installed (W) | Dense: laser (W) | Dense: heater (W) | "
         "Dense: plate (°C) | Dense: rod gland (°C) | Dense: magnet face (°C) | Dense: hot plate clearance (µm) | "
         "Laser off: hot plate clearance (µm) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for c in d["jacket"]["cases"]:
        r1, r0 = c["dense"], c["laser_off"]
        flag = " **over**" if c["heater_at_laser_off_W"] > c["installed_W"] else ""
        L.append(f"| {c['jacket']} | {c['key']} {c['pos']} | {c['heater_at_laser_off_W']:.0f} / {c['installed_W']:.0f}{flag} | "
                 f"{c['Q_dense_W']:.0f} | {r1['P_heater_W']:.0f}{' (off)' if r1['heater_off'] else ''} | "
                 f"{r1['T_plate_centre']:.0f} | {r1['T_gland_max']:.0f} | {r1['T_rod_end']:.0f} | "
                 f"{r1['clear_plate_hot_mm'] * 1000:.0f} | {r0['clear_plate_hot_mm'] * 1000:.0f} |")
    return L


if __name__ == "__main__":
    if "jacket" in sys.argv[1:]:
        jacket()
        sys.exit(0)
    if "report" in sys.argv[1:]:                 # rewrite the .md and .png from the .json, no FEA
        d = json.loads((OUT / "laser_heat.json").read_text())
        d["summary"] = summarize(d["rows"])
        (OUT / "laser_heat.json").write_text(json.dumps(d, indent=1, default=float))
        report(d)
        plot(d)
    else:
        main()
