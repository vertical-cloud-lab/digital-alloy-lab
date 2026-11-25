#!/usr/bin/env python3
"""CalculiX cross-check of the cover-slide thermal lens (issue #260).

A 2-degree sector of the Ø46 (rim contact) x 2 mm fused-silica slide (Edmund 36-299, read from the model since 2026-11-25;
it was 3 mm), meshed here as C3D6 wedges at the axis and C3D8
bricks elsewhere, graded toward the centre. The absorbed power (Gaussian, w = beam radius on the slide) goes into the
bottom element row (the fouled face). Rim nodes are held at the mount temperature; top and bottom faces lose heat by
*FILM at h = 10 W/m2K (radiation + natural convection in argon, linearised), as in thermal_lens.py. The nodal
temperatures give the optical path difference chi * integral T dz, and a beam-weighted parabola gives the lens power.
Compares with the finite-volume solve and the analytic central curvature in thermal_lens.py.

Writes analysis/out/optics/thermal_lens_ccx.md / .json; the CalculiX deck and results stay in /tmp/optics-ccx.
Run: python desktop-lpbf/analysis/optics/thermal_lens_ccx.py   (needs `ccx` on the PATH)
"""
from __future__ import annotations

import json
import math
import shutil
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "optics"
import sys  # noqa: E402
sys.path.insert(0, str(HERE.parents[1] / "cad"))
import lpbf_low as MODEL  # noqa: E402  (slide thickness and height from the model's P block, as thermal_lens.py)
WORK = Path("/tmp/optics-ccx")
WORK.mkdir(parents=True, exist_ok=True)

K = 1.38e-3                 # W/(mm K), fused silica (Corning 7980)
CHI = 9.871e-6              # 1/K, dn/dT + (n-1)(1+nu)alpha (thermal_lens.py)
H = 10e-6                   # W/(mm2 K)
R, T_TH = 23.0, MODEL.P["slide_t"]   # mm: rim contact radius (the drawer's Ø46 seat), slide thickness (2.0 since 2026-11-25)
P_LASER = 500.0
CASES = [("3.2 mm beam, fogged 0.5 %", 3.2, 5e-3), ("5 mm beam, fogged 0.5 %", 5.0, 5e-3), ("3.2 mm beam, light film 0.05 %", 3.2, 5e-4),
         ("2.5 mm beam (drawn), light film 0.05 %", 2.5, 5e-4)]
H_SLIDE = MODEL.P["z_slide0"]   # mm above focus: the slide's bottom face (127.0 since 2026-11-25; was 126)


def build_and_run(w, P_abs, tag):
    nr, nz = 70, 12
    # graded radial nodes: fine to ~3w, then geometric to the rim
    r_fine = np.linspace(0, 3 * w, 46)
    r_out = np.geomspace(3 * w, R, nr - 45 + 1)[1:]
    rn = np.concatenate([r_fine, r_out])
    zn = np.linspace(0, T_TH, nz + 1)
    half = math.radians(1.0)
    nodes = {}
    nid = 0
    # node ids: axis nodes (one per z), then (i, j, side) for i >= 1
    ax_id = {}
    for j, z in enumerate(zn):
        nid += 1
        nodes[nid] = (0.0, 0.0, z)
        ax_id[j] = nid
    ring = {}
    for i in range(1, len(rn)):
        for j, z in enumerate(zn):
            for s, a in ((0, -half), (1, half)):
                nid += 1
                nodes[nid] = (rn[i] * math.cos(a), rn[i] * math.sin(a), z)
                ring[(i, j, s)] = nid
    elems, eid = [], 0
    bf = []
    films = []
    for i in range(len(rn) - 1):
        r1, r2 = rn[i], rn[i + 1]
        # mean surface flux over the ring, W/mm2
        e1, e2 = math.exp(-2 * r1 ** 2 / w ** 2), math.exp(-2 * r2 ** 2 / w ** 2)
        qs = P_abs * (e1 - e2) / (math.pi * (r2 ** 2 - r1 ** 2))
        for j in range(nz):
            eid += 1
            if i == 0:
                n = [ax_id[j], ring[(1, j, 0)], ring[(1, j, 1)], ax_id[j + 1], ring[(1, j + 1, 0)], ring[(1, j + 1, 1)]]
                elems.append(("C3D6", eid, n))
            else:
                n = [ring[(i, j, 0)], ring[(i + 1, j, 0)], ring[(i + 1, j, 1)], ring[(i, j, 1)],
                     ring[(i, j + 1, 0)], ring[(i + 1, j + 1, 0)], ring[(i + 1, j + 1, 1)], ring[(i, j + 1, 1)]]
                elems.append(("C3D8", eid, n))
            if j == 0:
                bf.append((eid, qs / (zn[1] - zn[0])))
                films.append((eid, "F1"))
            if j == nz - 1:
                films.append((eid, "F2"))
    rim = [ring[(len(rn) - 1, j, s)] for j in range(nz + 1) for s in (0, 1)]
    L = ["*HEADING", f"cover slide thermal lens, {tag}", "*NODE, NSET=NALL"]
    L += [f"{k}, {x:.6f}, {y:.6f}, {z:.6f}" for k, (x, y, z) in nodes.items()]
    for typ in ("C3D6", "C3D8"):
        L.append(f"*ELEMENT, TYPE={typ}, ELSET=E{typ}")
        L += [f"{e}, " + ", ".join(map(str, n)) for t, e, n in elems if t == typ]
    L += ["*ELSET, ELSET=EALL", "EC3D6, EC3D8", "*NSET, NSET=RIM"] + [", ".join(map(str, rim[k:k + 12])) for k in range(0, len(rim), 12)]
    L += ["*MATERIAL, NAME=FS", "*CONDUCTIVITY", f"{K}", "*SOLID SECTION, ELSET=EALL, MATERIAL=FS",
          "*INITIAL CONDITIONS, TYPE=TEMPERATURE", "NALL, 0.0",
          "*STEP", "*HEAT TRANSFER, STEADY STATE", "*BOUNDARY", "RIM, 11, 11, 0.0", "*DFLUX"]
    L += [f"{e}, BF, {q:.6e}" for e, q in bf]
    L += ["*FILM"] + [f"{e}, {f}, 0.0, {H:.3e}" for e, f in films]
    L += ["*NODE PRINT, NSET=NALL", "NT", "*END STEP"]
    deck = WORK / f"slide_{tag}.inp"
    deck.write_text("\n".join(L) + "\n")
    subprocess.run(["ccx", "-i", deck.with_suffix("").name], cwd=WORK, check=True, capture_output=True, timeout=600)
    # parse temperatures
    T = {}
    reading = False
    for line in (WORK / f"slide_{tag}.dat").read_text().splitlines():
        if "temperatures" in line.lower():
            reading = True
            continue
        if reading:
            parts = line.split()
            if len(parts) == 2:
                try:
                    T[int(parts[0])] = float(parts[1])
                except ValueError:
                    pass
    # OPD along the theta = -1 deg face (side 0) and the axis
    rr, opd = [0.0], [CHI * np.trapezoid([T[ax_id[j]] for j in range(nz + 1)], zn)]
    for i in range(1, len(rn)):
        rr.append(rn[i])
        opd.append(CHI * np.trapezoid([T[ring[(i, j, 0)]] for j in range(nz + 1)], zn))
    rr, opd = np.array(rr), np.array(opd)
    # weighted parabola fit (r in mm, OPD in mm): D = -2 b (1/mm)
    wt = np.exp(-2 * rr ** 2 / w ** 2) * np.maximum(rr, 1e-6)
    # integrate on the non-uniform grid: weights times local spacing
    dr = np.gradient(rr)
    X = np.vstack([np.ones_like(rr), rr ** 2]).T
    sw = np.sqrt(wt * dr)
    a, b = np.linalg.lstsq(X * sw[:, None], opd * sw, rcond=None)[0]
    D = -2 * b * 1e3          # 1/m
    T_centre = float(np.mean([T[ax_id[j]] for j in range(nz + 1)]))
    return dict(nodes=len(nodes), elements=len(elems), T_centre_K=T_centre, D_eff_per_m=D)


def main():
    if not shutil.which("ccx"):
        raise SystemExit("ccx not found")
    fv = json.loads((OUT / "thermal_lens.json").read_text())
    rows = []
    for name, Dc, a in CASES:
        w = Dc / 2 * H_SLIDE / 160.0
        P_abs = a * P_LASER
        res = build_and_run(w, P_abs, name.split(",")[0].replace(" ", "").replace(".", "p") + f"_{a:g}")
        fvc = [c for c in fv["cases"] if c["D_coll_mm"] == Dc and c["element"].startswith("cover slide") and abs(c["a_tot"] - a) < 1e-9][0]
        D0 = CHI * P_abs / (math.pi * K * 1e3 * (w * 1e-3) ** 2)
        h = H_SLIDE * 1e-3
        dz = lambda D: h ** 2 * D / (1 + h * D) * 1e3
        rows.append(dict(case=name, w_mm=w, P_abs_W=P_abs, ccx=res, fv_D_eff=fvc["D_eff_per_m"], fv_T_centre=fvc["T_centre_K"],
                         analytic_D0=D0, dz_ccx_mm=dz(res["D_eff_per_m"]), dz_fv_mm=dz(fvc["D_eff_per_m"])))
    (OUT / "thermal_lens_ccx.json").write_text(json.dumps(rows, indent=1))
    L = ["# CalculiX cross-check of the cover-slide thermal lens (`analysis/optics/thermal_lens_ccx.py`)", "",
         "2° sector of the slide (C3D6 at the axis, C3D8 elsewhere), absorbed power in the bottom element row, rim at the mount "
         "temperature, *FILM h = 10 W/m²K on both faces. Same inputs as the finite-volume solve in thermal_lens.py.", "",
         "| Case | Beam w on slide (mm) | P_abs (W) | Mesh (nodes / elements) | ΔT centre, CalculiX / FV (K) | D_eff, CalculiX / FV (1/m) | Central curvature D0 (1/m) | Focus shift, CalculiX / FV (mm) |",
         "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['case']} | {r['w_mm']:.2f} | {r['P_abs_W']:.2f} | {r['ccx']['nodes']} / {r['ccx']['elements']} | "
                 f"{r['ccx']['T_centre_K']:.1f} / {r['fv_T_centre']:.1f} | {r['ccx']['D_eff_per_m']:.3f} / {r['fv_D_eff']:.3f} | "
                 f"{r['analytic_D0']:.3f} | {r['dz_ccx_mm']:.1f} / {r['dz_fv_mm']:.1f} |")
    (OUT / "thermal_lens_ccx.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
