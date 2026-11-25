"""Batch driver for the 3D melt-pool solver (fv3d.py): named case sets, one JSON line per case, fields kept in /tmp.

Run (each case 1-5 min on one core):
    OMP_NUM_THREADS=1 /tmp/capmem 3 python run_cases.py ref          # the 8 reference points behind surface_fields.npz
    OMP_NUM_THREADS=1 /tmp/capmem 3 python run_cases.py sens         # Marangoni factor, absorptivity, layer, grid
    OMP_NUM_THREADS=1 /tmp/capmem 3 python run_cases.py map          # cross-check points against the analytical models
    python run_cases.py collect                                       # -> analysis/out/monitoring/melt/surface_fields.npz
Results: analysis/out/monitoring/melt/fv_cases.jsonl (summaries), /tmp/melt_runs/<tag>.npz (fields, not committed).
"""
from __future__ import annotations

import json
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fv3d  # noqa: E402

OUT = HERE.parents[1] / "out" / "monitoring" / "melt"
RUNS = pathlib.Path("/tmp/melt_runs")
H_REF = (6e-6, 5e-6, 4e-6)
A_REF = 0.35
XG = np.arange(-1200.0, 300.0 + 1e-9, 4.0)     # um, beam frame
YG = np.arange(-400.0, 400.0 + 1e-9, 4.0)


def ref_cases():
    out = []
    for alloy in ("AlSi10Mg", "6061"):
        for v in (1.1, 0.6):
            for T0 in (25.0, 200.0):
                out.append(fv3d.Case(alloy=alloy, P=320.0, v=v, A=A_REF, T0=T0 + 273.15, h=H_REF,
                                     tag=f"ref_{alloy}_320W_{v:.1f}ms_{T0:.0f}C"))
    return out


def sens_cases():
    base = dict(alloy="AlSi10Mg", P=320.0, v=1.1, A=A_REF, T0=298.15, h=(8e-6, 6e-6, 5e-6))
    out = [fv3d.Case(**base, tag="sens_base_coarse")]
    for fM in (1.0, 3.0):
        out.append(fv3d.Case(**(base | dict(f_M=fM)), tag=f"sens_fM{fM:.1f}"))
    out.append(fv3d.Case(**(base | dict(t_layer=0.0)), tag="sens_bare"))
    out.append(fv3d.Case(**(base | dict(evap=False)), tag="sens_noevap"))
    out.append(fv3d.Case(**(base | dict(h=(4e-6, 3.5e-6, 3e-6))), tag="sens_fine"))
    return out


def val_cases():
    """Patel & Vlasea's AlSi10Mg single tracks (108 um spot, 30 um layer; via Edison r8-melt-plume) at A = 0.35, and A 0.30 / 0.40
    at 300 W."""
    out = []
    for P, v in ((200.0, 0.917), (250.0, 0.917), (300.0, 0.917), (350.0, 0.917), (200.0, 0.688), (350.0, 0.688)):
        out.append(fv3d.Case(alloy="AlSi10Mg", P=P, v=v, d_spot=108e-6, A=A_REF, h=(8e-6, 6e-6, 5e-6),
                             tag=f"val_{P:.0f}W_{v:.3f}ms"))
    for A in (0.30, 0.40):
        out.append(fv3d.Case(alloy="AlSi10Mg", P=300.0, v=0.917, d_spot=108e-6, A=A, h=(8e-6, 6e-6, 5e-6),
                             tag=f"val_300W_0.917ms_A{A:.2f}"))
    return out


def map_cases():
    out = []
    # 7075 also with the surface Mg/Zn activity cut 10x (f_vol 0.1): with the bulk activity, HKL evaporates more Zn than the pool
    # holds and takes ~13 % of the absorbed power; measured losses (~18 % of the Zn) put it near 0.1
    for P, v in ((320.0, 1.1), (320.0, 0.6)):
        out.append(fv3d.Case(alloy="7075", P=P, v=v, A=A_REF, T0=298.15, h=(8e-6, 6e-6, 5e-6), f_vol=0.1,
                             tag=f"map_7075_{P:.0f}W_{v:.1f}ms_fvol0.1"))
    pts = {"7075": ((320.0, 1.1), (320.0, 0.6), (200.0, 1.1)), "Al": ((320.0, 1.1),),
           "AlSi10Mg": ((200.0, 1.1), (400.0, 1.1)), "6061": ((200.0, 1.1), (400.0, 1.1))}
    for alloy, pv in pts.items():
        for P, v in pv:
            out.append(fv3d.Case(alloy=alloy, P=P, v=v, A=A_REF, T0=298.15, h=(8e-6, 6e-6, 5e-6),
                                 tag=f"map_{alloy}_{P:.0f}W_{v:.1f}ms"))
    return out


def run_set(cases, skip_done=True):
    RUNS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    log = OUT / "fv_cases.jsonl"
    done = set()
    if skip_done and log.exists():
        done = {json.loads(l)["case"]["tag"] for l in log.read_text().splitlines() if l.strip()}
    for c in cases:
        if c.tag in done:
            print("skip", c.tag)
            continue
        t0 = time.time()
        s, summ = fv3d.run(c, verbose=False)
        Ts = s.surface_grid(XG * 1e-6, YG * 1e-6)
        # centre-plane (y ~ 0) slice and the cross-section at the widest point, for plots
        j0 = 0
        iw = int(np.argmax((s.T[:, :, 0] >= s.al.T_liq).sum(axis=1))) if (s.T[:, :, 0] >= s.al.T_liq).any() else 0
        np.savez_compressed(RUNS / f"{c.tag}.npz", Ts=Ts.astype(np.float32), xg=XG, yg=YG, xc=s.xc, yc=s.yc, zc=s.zc,
                            xf=s.xf, yf=s.yf, zf=s.zf,
                            T_xz=s.T[:, j0, :].astype(np.float32), T_yz=s.T[iw, :, :].astype(np.float32), x_yz=s.xc[iw],
                            sol=np.array([[p["y"], p["z"], p["G"], p["R"], p["Tdot_liq"], p["t_sol"]] for p in
                                          getattr(s, "sol_pts", [])]))
        with log.open("a") as f:
            f.write(json.dumps(summ, default=float) + "\n")
        L = summ["liquid"]
        print(f"{c.tag:40s} {s.N:7d} cells {time.time() - t0:6.0f} s conv={summ['converged']} it={summ['iterations']}  "
              f"L/W/D {L['L'] * 1e6:5.0f}/{L['W'] * 1e6:4.0f}/{L['D'] * 1e6:4.0f} um  Tpk {summ['T_peak']:6.0f} K  "
              f"bal {summ['energy']['balance_W']:+.3f} W", flush=True)


def collect():
    """surface_fields.npz: the reference surface temperature fields on one regular grid (see melt-pool.md, 'Data for the optics')."""
    log = OUT / "fv_cases.jsonl"
    rows = {json.loads(l)["case"]["tag"]: json.loads(l) for l in log.read_text().splitlines() if l.strip()}
    tags = [c.tag for c in ref_cases() if c.tag in rows]
    T, liq, mush, meta = [], [], [], []
    for t in tags:
        d = np.load(RUNS / f"{t}.npz")
        r = rows[t]
        Ts = d["Ts"]
        T.append(Ts)
        liq.append(Ts >= r["T_liq"])
        mush.append((Ts >= r["T_sol"]) & (Ts < r["T_liq"]))
        c = r["case"]
        meta.append(dict(tag=t, alloy=c["alloy"], P_W=c["P"], v_m_s=c["v"], spot_1e2_um=c["d_spot"] * 1e6, A=c["A"],
                         T0_K=c["T0"], f_M=c["f_M"], layer_um=c["t_layer"] * 1e6, T_sol_K=r["T_sol"], T_liq_K=r["T_liq"],
                         T_boil_alloy_1atm_K=r["T_boil_alloy"], T_peak_K=r["T_peak"],
                         pool_L_um=r["liquid"]["L"] * 1e6, pool_W_um=r["liquid"]["W"] * 1e6, pool_D_um=r["liquid"]["D"] * 1e6))
    import evap as EV
    import props as PR
    for m in meta:
        m["T_wall_K"] = EV.T_wall(PR.Alloy(m["alloy"]), m["spot_1e2_um"] * 0.5e-6)
    T = np.stack(T)
    Tb = np.array([m["T_boil_alloy_1atm_K"] for m in meta])[:, None, None]
    Tw = np.array([m["T_wall_K"] for m in meta])[:, None, None]
    np.savez_compressed(
        OUT / "surface_fields.npz",
        x_um=XG.astype(np.float32), y_um=YG.astype(np.float32), T_K=T.astype(np.float32),
        T_capped_K=np.minimum(T, Tw).astype(np.float32),
        liquid=np.stack(liq), mushy=np.stack(mush), above_boil=(T >= Tb),
        cases=np.array([m["tag"] for m in meta]), meta_json=np.array(json.dumps(meta)),
        README=np.array("Surface temperature T_K[case, ix, iy] (K) on the powder/melt surface, beam frame: the beam centre is at "
                        "(0, 0) and moves toward +x, so the melt pool trails toward -x. x_um, y_um: cell-centre coordinates in um "
                        "(4 um grid). From fv3d.py (3D quasi-steady conduction, see melt-pool.md): no free surface, so where "
                        "T_K exceeds the alloy's 1 atm boiling point (meta T_boil_alloy_1atm_K) the real surface is a vapour "
                        "depression; its wall sits near T_wall_K, where the recoil pressure 0.54 p_sat holds a hole of the beam's "
                        "radius open against 1 atm and surface tension. T_capped_K = min(T_K, T_wall_K) is that reading (use it "
                        "for emission). liquid: T >= liquidus; mushy: solidus "
                        "<= T < liquidus; above_boil: T >= boiling point (depression). meta_json: per-case inputs and pool "
                        "sizes. Emissivity is not applied here."))
    print("wrote", OUT / "surface_fields.npz", T.shape, [m["tag"] for m in meta])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "collect":
        collect()
    else:
        for name in cmd.split("+"):
            run_set({"ref": ref_cases, "sens": sens_cases, "map": map_cases, "val": val_cases}[name]())
