"""Round 3 (2026-11-28): build times on CAD v2 with the thermal FEA's dwell (#260).

Round 2's build times (scan_program.py, out/build_times.csv) had no dwell and the v1 recoater stroke. Here:

- scan: each layer's list time and energy from the first build's file (out/build_first_coupons_15mm.npz) by
  scan_program.layer_time (the RTC4 lists of rtc4_list.py run within 5 ms of it);
- recoat: the Zaber X-LSM100B-E03 between the hopper parks of CAD v2 (cad/ft_checks.travel_needed(): the beam
  envelope plus 3 mm; and the park drawn in ft_model, P['hx_default'], as a longer case), at Zaber's published
  104 mm/s. Zaber publishes no acceleration for it (product page and X-LSM-E manual, read 2026-11-28): the device's
  `accel` setting holds it, to be read with `get accel`. 1000 mm/s2 (round 2's estimate) and 250 mm/s2 are used;
- spreading speed 40 mm/s (estimate) and Heriot-Watt's 10 mm/s; plate step on the X-VSR20A; 0.5 s host overhead;
- dwell: the thermal FEA (analysis/out/fea/thermal.md, case 3, CAD v2): holding the substrate top within +10 K of
  200 C allows 14.0 W absorbed on average with the block at the set point, and 26.7 W with the block 20 K below
  (plate set point lowered so its heater stays off). Each layer then takes max(scan + recoat, A E / P_allowed). The
  control worker's lumped study at the FE's 0.67 W/K (control/out/dwell-study-fe.csv, +5 K band) is listed beside it.

Run: /tmp/tools/capmem 1 python desktop-lpbf/fast-track/process/build_time_v2.py   (writes out/build_times_v2.csv,
     out/build_time_v2.json; imports the CAD model for the parks)
"""
from __future__ import annotations

import csv
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "cad"))
import scan_program as SPG  # noqa: E402

V_MAX = 104.0                      # mm/s, X-LSM100B-E03 (zaber.com, read 2026-11-27 and 2026-11-28)
ACCELS = (1000.0, 250.0)           # mm/s2: not published; round 2's estimate, and a slow default
SPREADS = (40.0, 10.0)             # mm/s
P_ALLOW = {"block at set point": 14.0, "block 20 K below": 26.7}   # W absorbed, +10 K band (thermal FEA, case 3)
ABSORPTIVITY = (0.3, 0.45, 0.6)
HEIGHTS = (5.0, 10.0, 15.0)


def parks():
    import ft_checks as CH  # noqa: E402  (CadQuery)
    import ft_model as M  # noqa: E402
    tr = CH.travel_needed()
    return dict(left=tr["left_park"], right=tr["right_park"], drawn_right=M.P["hx_default"],
                stage_travel=M.P["rc_travel"], stage=M.P["rc_stage"])


def main():
    pk = parks()
    strokes = {"v2 parks (ft_checks)": pk["right"] - pk["left"], "to the drawn park (hx 37.5)": pk["drawn_right"] - pk["left"]}
    segs, kinds, pidx, ptr, meta = SPG.load_build(OUT / "build_first_coupons_15mm.npz")
    parts = [SPG.Part(**p) for p in meta["parts"]]
    psets = {k: SPG.ParamSet(**v) for k, v in meta["psets"].items()}
    tm = SPG.Timing(**meta["timing"])
    layer_mm = next(iter(psets.values())).layer
    lt = [SPG.layer_time(segs[ptr[k]:ptr[k + 1]], kinds[ptr[k]:ptr[k + 1]], pidx[ptr[k]:ptr[k + 1]], parts, psets, tm)
          for k in range(len(ptr) - 1)]
    t_list = np.array([r["t_list"] for r in lt])
    E = np.array([r["energy_J"] for r in lt])
    rows, recoats = [], {}
    for sname, stroke in strokes.items():
        for acc in ACCELS:
            for vs in SPREADS:
                stage = SPG.Stage("Zaber X-LSM100B-E03", V_MAX, acc)
                rc = SPG.recoat_time(SPG.Recoat(stroke=stroke, v_spread=vs), stage, layer_mm)
                recoats[f"{sname}, {acc:g} mm/s2, spread {vs:g} mm/s"] = rc
                base = t_list + rc["t_recoat"]
                for h in HEIGHTS:
                    n = int(round(h / layer_mm))
                    row = dict(stroke_case=sname, stroke_mm=round(stroke, 1), accel_mm_s2=acc, v_spread_mm_s=vs,
                               recoat_s=round(rc["t_recoat"], 3), build_mm=h, layers=n,
                               no_dwell_h=round(base[:n].sum() / 3600, 3))
                    for case, Pa in P_ALLOW.items():
                        for A in ABSORPTIVITY:
                            per = np.maximum(base[:n], A * E[:n] / Pa)
                            row[f"{case}, A {A}: h"] = round(per.sum() / 3600, 3)
                            row[f"{case}, A {A}: s a layer"] = round(per.mean(), 2)
                    rows.append(row)
    with (OUT / "build_times_v2.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    fe = list(csv.DictReader((HERE.parent / "control" / "out" / "dwell-study-fe.csv").open()))
    lumped = [dict(band_K=r["band_K"], block_offset_K=r["block_offset_K"], A=r["absorptivity"], period_s=r["period_s"],
                   build_10mm_h=r["build_10mm_h"], build_15mm_h=r["build_15mm_h"],
                   build_5mm_h=round(float(r["period_s"]) * 167 / 3600, 2))
              for r in fe if r["g_source"].startswith("thermal FEA: substrate") and float(r["band_K"]) == 5.0]
    info = dict(parks=pk, strokes=strokes, recoat=recoats, layer_mm=layer_mm, layers=len(lt),
                scan_s_mean=float(t_list.mean()), scan_s_range=[float(t_list.min()), float(t_list.max())],
                energy_J_mean=float(E.mean()), P_allowed_W=P_ALLOW, lumped_fe_5K=lumped,
                v1=dict(stroke_mm=66.4, recoat_s=3.07, no_dwell_10mm_h=0.60))
    (OUT / "build_time_v2.json").write_text(json.dumps(info, indent=1))
    main_rows = [r for r in rows if r["stroke_case"].startswith("v2 parks") and r["accel_mm_s2"] == 1000.0
                 and r["v_spread_mm_s"] == 40.0]
    print("parks", pk, "strokes", strokes)
    for k, rc in recoats.items():
        print(f"{k}: recoat {rc['t_recoat']:.2f} s (return {rc['t_return']:.2f}, spread {rc['t_spread']:.2f})")
    for r in main_rows:
        print(r)
    return info


if __name__ == "__main__":
    main()
