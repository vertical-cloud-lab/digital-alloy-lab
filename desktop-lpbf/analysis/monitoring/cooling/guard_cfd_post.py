"""Post-processing for guard_cfd.py (monitoring/cooling.md §4.2): reads the solved cases under /tmp and writes
analysis/out/monitoring/cooling/guard_cfd.json, guard_cfd.md, guard_cfd_T.png and guard_cfd_flow.png.

    /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/cooling/guard_cfd.py post /tmp/guard-cfd/typ12 /tmp/guard-cfd/busy12 ...

The first case named is the one the figures show. For each case: the air round each device (fluid cells 2-3 cells, ~12-36 mm, from
the device's cells: mean and 95th percentile), the hood's air, the mean air above and below the optics bridge, the local mean age of the
air (OpenFOAM's age function object: seconds since the air came in), the heat balance (wallHeatFlux per patch, the exhaust's
enthalpy) and the convergence (the last 500 iterations of the volume-mean and exhaust temperatures, the final residuals).
"""
from __future__ import annotations

import json
import pathlib
import re

import numpy as np
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[2]
OUT = D / "analysis" / "out" / "monitoring" / "cooling"
import guard_cfd as GC  # noqa: E402

RHO, CP = GC.RHO, GC.CP


def latest(case):
    ts = [p for p in case.iterdir() if p.is_dir() and re.fullmatch(r"\d+(\.\d+)?", p.name) and p.name != "0"]
    return max(ts, key=lambda p: float(p.name))


def read_field(path, n):
    s = path.read_text()
    m = re.search(r"internalField\s+nonuniform\s+List<(scalar|vector)>\s*(\d+)\s*\(", s)
    if not m:
        m2 = re.search(r"internalField\s+uniform\s+([^;]+);", s)
        v = m2.group(1).strip("() ").split()
        return np.tile(np.array(v, float), (n, 1)).squeeze()
    start = m.end()
    end = s.index("\n)\n", start)
    body = s[start:end].replace("(", " ").replace(")", " ")
    a = np.array(body.split(), float)
    return a.reshape(n, 3) if m.group(1) == "vector" else a


def last_rows(path):
    rows = [ln.split() for ln in path.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    return rows


def fo_file(case, fo, fname):
    """a function object's output file in its latest start-time folder (a continuation writes a new one)"""
    d = case / "postProcessing" / fo
    t = max((p for p in d.iterdir() if p.is_dir()), key=lambda p: float(p.name))
    return t / fname


N_AVG = 500                                                     # iterations averaged for the heat balance and the exhaust


def heat_balance(case, meta):
    rows = last_rows(fo_file(case, "wallHeatFlux", "wallHeatFlux.dat"))
    t_last = float(rows[-1][0])
    Q = {}
    for r in rows:
        if float(r[0]) > t_last - N_AVG:
            Q.setdefault(r[1], []).append(float(r[4]))
    Q = {k: float(np.mean(v)) for k, v in Q.items()}
    fl = last_rows(fo_file(case, "exhaustFlow", "surfaceFieldValue.dat"))
    et = last_rows(fo_file(case, "exhaustT", "surfaceFieldValue.dat"))
    sel = lambda rr: [float(r[1]) for r in rr if float(r[0]) > float(rr[-1][0]) - N_AVG]
    mdot = abs(float(np.mean(sel(fl))))
    T_ex = float(np.mean(sel(et))) - 273.15
    q_h = meta["q_hood_m3h"]
    T_mix = meta["supply_c"] + meta["hood_pickup_k"] * q_h / meta["q_exhaust_m3h"]
    Q_ex = mdot * CP * (T_ex - T_mix)
    panels = sum(v for k, v in Q.items() if k.startswith("panel") or k == "window")
    src = sum(v for k, v in Q.items() if k in meta["heat_W"])
    tot_in = src + Q.get("chamber", 0.0) + Q.get("floor", 0.0)
    hist_T = np.array([float(r[1]) for r in et]) - 273.15
    return dict(Q_by_patch_W={k: round(v, 2) for k, v in Q.items() if abs(v) > 0.005}, sources_W=round(src, 1),
                chamber_W=round(Q.get("chamber", 0.0), 1), floor_legs_W=round(Q.get("floor", 0.0), 1), panels_W=round(panels, 1),
                in_W=round(tot_in, 1), exhaust_W=round(Q_ex, 1), mdot_kg_s=round(mdot, 5), q_exhaust_m3h=round(mdot / RHO * 3600, 1),
                T_exhaust_c=round(T_ex, 2), T_supply_mix_c=round(T_mix, 2),
                imbalance_W=round(tot_in + panels - Q_ex, 1), imbalance_pct=round(100 * (tot_in + panels - Q_ex) / tot_in, 1),
                exhaust_T_range_last500_k=round(float(np.ptp(np.array(sel(et)))), 3),
                vol_T_drift_last500_k=vol_drift(case))


def vol_drift(case):
    v = last_rows(fo_file(case, "volT", "volFieldValue.dat"))
    t1 = float(v[-1][0])
    a = [float(r[1]) for r in v if float(r[0]) > t1 - N_AVG]
    return round(a[-1] - a[0], 3)


def residuals(case):
    txt = (case / "log.buoyantSimpleFoam").read_text().splitlines()
    res = {}
    for ln in txt[::-1]:
        m = re.search(r"Solving for (\w+), Initial residual = ([\d.eE+-]+)", ln)
        if m and m.group(1) not in res:
            res[m.group(1)] = float(m.group(2))
        if len(res) >= 7:
            break
    it = [ln for ln in txt if ln.startswith("Time = ")]
    conv = any("SIMPLE solution converged" in ln for ln in txt)
    return dict(final_initial_residuals={k: float(f"{v:.2e}") for k, v in res.items()}, iterations=len(it), converged_to_tolerance=conv)


def analyse(case):
    case = pathlib.Path(case)
    meta = json.load(open(case / "case_meta.json"))
    g = np.load(case / "grid.npz", allow_pickle=True)
    X, Y, Z, lab, ijk = g["X"], g["Y"], g["Z"], g["lab"], g["ijk"]
    names = list(g["names"])
    n = len(ijk)
    t = latest(case)
    avg = (t / "TMean").exists()
    T = read_field(t / ("TMean" if avg else "T"), n) - 273.15
    U = read_field(t / ("UMean" if avg else "U"), n)
    age = read_field(t / "age", n) if (t / "age").exists() else np.full(n, np.nan)
    sh = lab.shape
    F = lab == 0
    T3 = np.full(sh, np.nan)
    A3 = np.full(sh, np.nan)
    U3 = np.full(sh + (3,), np.nan)
    T3[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = T
    A3[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = age
    U3[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = U
    dx, dy, dz = np.diff(X), np.diff(Y), np.diff(Z)
    vol = dx[:, None, None] * dy[None, :, None] * dz[None, None, :] * 1e-9
    xc, yc, zc = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1]), 0.5 * (Z[1:] + Z[:-1])
    Ts = meta["supply_c"]
    V = float(vol[F].sum())
    q = meta["q_exhaust_m3h"] / 3600
    tau_n = V / q

    def stats(mask):
        w = vol[mask]
        return dict(mean_rise_k=round(float((T3[mask] * w).sum() / w.sum() - Ts), 2),
                    p95_rise_k=round(float(np.nanpercentile(T3[mask], 95) - Ts), 2),
                    mean_age_s=round(float((A3[mask] * w).sum() / w.sum()), 1), cells=int(mask.sum()))

    st = ndimage.generate_binary_structure(3, 1)
    dev = {}
    for key, label, rating, check in GC.REPORT:
        if key not in names:
            continue
        m = lab == names.index(key) + 1
        # the air round it: fluid cells 2-3 cells (~12-36 mm) from the device, outside its own first layer of cells
        shell = ndimage.binary_dilation(m, st, iterations=3) & F & ~ndimage.binary_dilation(m, st, iterations=1)
        dev[key] = dict(label=label, rating_c=rating, checked_on=check, **stats(shell))
    H = GC.MC.HOOD
    hood = F & ((xc > H["x"][0]) & (xc < H["x"][1]))[:, None, None] & ((yc > H["y"][0]) & (yc < H["y"][1]))[None, :, None] & \
        ((zc > H["z"][0]) & (zc < H["z"][1]))[None, None, :]
    back = hood & (xc < -330)[:, None, None]                    # the camera's back half, near where the duct's air drops in
    front = hood & (xc > -260)[:, None, None]                   # its lens end, where the hood's air leaves
    dev["chronos"].update(hood_all=stats(hood), hood_back_half=stats(back), hood_lens_end=stats(front))
    above = F & (zc > 236.1)[None, None, :]
    below = F & (zc < 211.1)[None, None, :]
    zones = dict(all=stats(F), above_bridge=stats(above), below_bridge=stats(below),
                 upper_half=stats(F & (zc > 0.5 * (Z[0] + Z[-1]))[None, None, :]),
                 lower_half=stats(F & (zc <= 0.5 * (Z[0] + Z[-1]))[None, None, :]))
    # dead zones: air older than 3 nominal time constants, as connected regions of more than 20 cm3
    old = F & (A3 > 3 * tau_n)
    reg, nreg = ndimage.label(old, st)
    dz_list = []
    for r in range(1, nreg + 1):
        mm = reg == r
        v = float(vol[mm].sum())
        if v < 20e-6:
            continue
        ii, jj, kk = np.nonzero(mm)
        dz_list.append(dict(volume_L=round(v * 1000, 2), x=[round(float(X[ii.min()])), round(float(X[ii.max() + 1]))],
                            y=[round(float(Y[jj.min()])), round(float(Y[jj.max() + 1]))],
                            z=[round(float(Z[kk.min()])), round(float(Z[kk.max() + 1]))],
                            mean_age_s=round(float(np.nanmean(A3[mm])), 1), mean_rise_k=round(float(np.nanmean(T3[mm]) - Ts), 2)))
    dz_list.sort(key=lambda d: -d["volume_L"])
    # the air entering the exhaust: the layer of cells in front of its face, weighted by the flow into it
    E = GC.MC.EXHAUST
    jx = int(np.searchsorted(Y, GC.MC.Y_TRAP[0]) - 1)
    lay = np.zeros(sh, bool)
    lay[:, jx, :] = ((xc > E["x"][0]) & (xc < E["x"][1]))[:, None] & ((zc > E["z"][0]) & (zc < E["z"][1]))[None, :]
    lay &= F
    w = np.clip(U3[..., 1], 0, None)[lay] * (dx[:, None, None] * dz[None, None, :] * np.ones(sh))[lay]
    ages = A3[lay]
    short = float(w[ages < 0.25 * tau_n].sum() / w.sum()) if w.sum() > 0 else float("nan")
    ex_above = float(w[(np.broadcast_to(zc[None, None, :], sh)[lay]) > 236.1].sum() / w.sum())
    flow = dict(fluid_volume_m3=round(V, 4), nominal_time_constant_s=round(tau_n, 2),
                air_change_effectiveness=round(tau_n / (2 * zones["all"]["mean_age_s"]), 3),
                exhaust_flow_younger_than_quarter_tau=round(short, 3), exhaust_flow_from_above_bridge=round(ex_above, 3),
                dead_zones_age_gt_3tau=dz_list[:8], dead_volume_fraction=round(float(vol[old].sum() / V), 3))
    return dict(case=str(case), averaged_fields=bool(avg), time=t.name, meta={k: meta[k] for k in ("h_mm", "load", "supply_c", "q_exhaust_m3h", "q_hood_m3h", "q_inlet_m3h",
                                                             "inlet_angle_deg", "heat_W", "legs_to_floor_W", "wellmixed_guard_c",
                                                             "variant", "n", "q_window_m3h", "network", "network_sealed")
                                    if k in meta},
                cells=int(F.sum()), devices=dev, zones=zones, flow=flow, heat=heat_balance(case, meta), convergence=residuals(case),
                _fields=dict(T3=T3, A3=A3, U3=U3, lab=lab, names=names, X=X, Y=Y, Z=Z, Ts=Ts, tau=tau_n))


def compare_wellmixed(r, cj):
    """CFD air round each device against cooling.py's well-mixed guard air, and the device temperatures shifted by the difference"""
    Ts = r["meta"]["supply_c"]
    case = "typical" if abs(Ts - cj["cases"]["typical"]["T_s"]) < 0.05 else "busy"
    wm = cj["results"][f"{case}/vent_shuttle"]
    Tg = wm["guard"]["T_g"]
    rows = {d["device"]: d for d in wm["devices"]}
    pis = wm["pis"]
    out = []
    for key, d in r["devices"].items():
        air = Ts + d["mean_rise_k"]
        air_p95 = Ts + d["p95_rise_k"]
        if key == "chronos":
            wm_air = rows["Chronos 2.1-HD (side camera)"]["air_c"]
            hood = d["hood_all"]
            air, air_p95 = Ts + hood["mean_rise_k"], Ts + hood["p95_rise_k"]
            checked, wm_checked = air, wm_air
            back = Ts + d["hood_back_half"]["mean_rise_k"]
        else:
            wm_air = Tg
            shift = air - Tg
            # boards bolted to something: cooling.py's device_T is linear, so only the air's share of the board's coupling moves
            # with the air round it; the coaxial camera's mount is the bridge (1 W/K), which moves with the air round the bridge
            bridge_shift = Ts + r["devices"]["bridge"]["mean_rise_k"] - Tg if "bridge" in r["devices"] else shift
            if key in ("camCoax", "camLP"):
                nm = "Coaxial camera (IMX296 board on the cage)" if key == "camCoax" else "LP camera (IMX296 board in a housing)"
                wm_checked = rows[nm]["case_c"]
                t = rows[nm]["terms"]
                G = t["G_air"] + t["G_rad"] + t["G_mount"]
                shift = (t["G_air"] * shift + (t["G_mount"] * bridge_shift if key == "camCoax" else 0.0)) / G
            elif key == "bridge":
                wm_checked = wm["bridge_c"]
            elif key == "aePre":
                wm_checked = rows["AE preamp (PreAmp One)"]["case_c"]
            elif key == "pb2":
                wm_checked = pis["pb2_box_air_c"]
            elif key == "piLP":
                wm_checked = pis["pi2_soc_c"]
            else:
                wm_checked = Tg
            checked = wm_checked + shift
            back = None
        rating = d["rating_c"]
        out.append(dict(key=key, device=d["label"], checked_on=d["checked_on"], rating_c=rating,
                        cfd_air_c=round(air, 1), cfd_air_rise_k=round(air - Ts, 1), cfd_air_p95_c=round(air_p95, 1),
                        wellmixed_air_c=round(wm_air, 1), wellmixed_rise_k=round(wm_air - Ts, 1),
                        wellmixed_checked_c=round(wm_checked, 1), cfd_checked_c=round(checked, 1),
                        margin_k=None if rating is None else round(rating - checked, 1),
                        ok=None if rating is None else bool(checked <= rating), hood_back_c=None if back is None else round(back, 1)))
    return dict(case=case, wellmixed_guard_c=Tg, wellmixed_rise_k=round(Tg - Ts, 1), rows=out)


def figures(r, tag="typ"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    f = r["_fields"]
    T3, A3, U3, lab, X, Y, Z, Ts, tau = f["T3"], f["A3"], f["U3"], f["lab"], f["X"], f["Y"], f["Z"], f["Ts"], f["tau"]
    names = f["names"]
    xc, yc, zc = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1]), 0.5 * (Z[1:] + Z[:-1])
    devs = {"chronos": "Chronos", "camCoax": "coax cam", "pdA": "PD-A", "pdB": "PD-B", "pb2": "PB2", "camLP": "LP cam",
            "piLP": "LP Pi", "galvo": "galvo", "chamber": "chamber", "bridge": "bridge"}
    cuts = [("z", 266.0, "above the bridge, z 266 mm"), ("z", 60.0, "below the bridge, z 60 mm"),
            ("y", -40.0, "through the hood and the cage, y -40 mm"), ("y", 160.0, "along the back panel, y 160 mm")]
    grey = ListedColormap(["#d9d9d9"])

    def plane(arr, ax_, v):
        if ax_ == "z":
            k = int(np.searchsorted(Z, v) - 1)
            return arr[:, :, k].T, (X[0], X[-1], Y[0], Y[-1]), ("x (mm)", "y (mm)"), k
        j = int(np.searchsorted(Y, v) - 1)
        return arr[:, j, :].T, (X[0], X[-1], Z[0], Z[-1]), ("x (mm)", "z (mm)"), j

    for what in ("T", "flow"):
        fig, axs = plt.subplots(2, 2, figsize=(14, 10.5), constrained_layout=True)
        for ax, (ax_, v, title) in zip(axs.ravel(), cuts):
            arr = (T3 - Ts) if what == "T" else A3 / tau
            P, ext, lbl, idx = plane(arr, ax_, v)
            S, _, _, _ = plane((lab > 0).astype(float), ax_, v)
            ax.pcolormesh(X, (Y if ax_ == "z" else Z), np.ma.masked_invalid(np.where(S > 0, 1.0, np.nan)), cmap=grey, vmin=0, vmax=1,
                          shading="flat")
            ax.set_aspect("equal")
            if what == "T":
                im = ax.pcolormesh(X, (Y if ax_ == "z" else Z), np.ma.masked_invalid(P), cmap="inferno",
                                   vmin=0, vmax=12, shading="flat")
            else:
                im = ax.pcolormesh(X, (Y if ax_ == "z" else Z), np.ma.masked_invalid(P), cmap="viridis_r", vmin=0, vmax=4,
                                   shading="flat")
                if ax_ == "z":
                    u, w_ = U3[:, :, idx, 0].T, U3[:, :, idx, 1].T
                    gx, gy = np.meshgrid(xc, yc)
                else:
                    u, w_ = U3[:, idx, :, 0].T, U3[:, idx, :, 2].T
                    gx, gy = np.meshgrid(xc, zc)
                s = 2
                ax.quiver(gx[::s, ::s], gy[::s, ::s], u[::s, ::s], w_[::s, ::s], color="white", scale=6, width=0.0022,
                          headwidth=3.5)
            # label devices cut by the plane
            for key, nm in devs.items():
                if key not in names:
                    continue
                Mk, _, _, _ = plane((lab == names.index(key) + 1).astype(float), ax_, v)
                if Mk.sum() < 2:
                    continue
                rr, cc = np.nonzero(Mk > 0)
                yy = (Y if ax_ == "z" else Z)
                ax.text(float(xc[cc].mean()), float(0.5 * (yy[rr] + yy[rr + 1]).mean()), nm, color="#1f77b4", fontsize=8,
                        ha="center", va="center", fontweight="bold")
            ax.set_title(title, fontsize=11)
            ax.set_xlabel(lbl[0])
            ax.set_ylabel(lbl[1])
        cb = fig.colorbar(im, ax=axs, shrink=0.6, location="right")
        if what == "T":
            cb.set_label("air temperature above the supply (K)")
            fig.suptitle(f"Guard air ({r['meta']['variant']}), {r['meta']['load']} load, {r['meta']['h_mm']:.0f} mm cells: rise over the "
                         f"{Ts:.1f} °C supply; grey = parts", fontsize=12)
            fn = OUT / "guard_cfd_T.png"
        else:
            cb.set_label("local mean age of the air / nominal time constant V/Q")
            fig.suptitle(f"Guard air, flow path ({r['meta']['variant']}): age of the air (yellow = fresh, dark = stale; 1 = V/Q = "
                         f"{tau:.1f} s) and the in-plane velocity (arrows); grey = parts", fontsize=12)
            fn = OUT / "guard_cfd_flow.png"
        fig.savefig(fn, dpi=95)
        plt.close(fig)


def write_md(res):
    L = ["# Guard air CFD (generated by guard_cfd.py post)\n"]
    names = list(res["cases"])
    L.append("## Summary: air round each device, K over the supply (mean of the cells 2-3 cells from it)\n")
    L.append("| Device | " + " | ".join(names) + " |")
    L.append("|---|" + "---:|" * len(names))
    keys = [k for k, *_ in GC.REPORT]
    for k in keys:
        cells = []
        for n in names:
            d = res["cases"][n]["devices"].get(k)
            if d is None:
                cells.append("-")
            elif k == "chronos":
                cells.append(f"{d['hood_all']['mean_rise_k']} (back {d['hood_back_half']['mean_rise_k']}, lens end {d['hood_lens_end']['mean_rise_k']})")
            else:
                cells.append(f"{d['mean_rise_k']}")
        lab = res["cases"][names[0]]["devices"][k]["label"] if k in res["cases"][names[0]]["devices"] else k
        L.append(f"| {lab} | " + " | ".join(cells) + " |")
    for zn, zl in (("above_bridge", "air above the bridge"), ("below_bridge", "air below the bridge"), ("all", "all the air")):
        L.append(f"| {zl} | " + " | ".join(str(res["cases"][n]["zones"][zn]["mean_rise_k"]) for n in names) + " |")
    L.append("| exhaust (flow-weighted) | " + " | ".join(f"{res['cases'][n]['heat']['T_exhaust_c'] - res['cases'][n]['meta']['supply_c']:.2f}" for n in names) + " |")
    L.append("| mean age above / below the bridge (s) | " + " | ".join(f"{res['cases'][n]['zones']['above_bridge']['mean_age_s']} / {res['cases'][n]['zones']['below_bridge']['mean_age_s']}" for n in names) + " |")
    L.append("")
    for name, r in res["cases"].items():
        m, h, c, fl = r["meta"], r["heat"], r["convergence"], r["flow"]
        L.append(f"## {name}: {m['variant']}, {m['load']} load, supply {m['supply_c']} °C, {m['h_mm']:.0f} mm cells ({r['cells']} cells)\n")
        win = f", {m['q_window_m3h']:.1f} through the base plate's open window" if m.get("q_window_m3h") else ""
        L.append(f"Flow {m['q_exhaust_m3h']} m³/h out ({m['q_inlet_m3h']:.1f} through the inlet, {m['q_hood_m3h']} through the hood{win}). "
                 f"Heat in: sources {h['sources_W']} W, chamber at 60 °C {h['chamber_W']} W, legs to the base plate {h['floor_legs_W']} W; "
                 f"panels {h['panels_W']} W; exhaust {h['exhaust_W']} W at {h['T_exhaust_c']} °C (imbalance {h['imbalance_pct']} %). "
                 f"Iterations {c['iterations']}, final residuals {c['final_initial_residuals']}.\n")
        cw = r["wellmixed"]
        L.append(f"Well-mixed (cooling.py): guard air {cw['wellmixed_guard_c']} °C, {cw['wellmixed_rise_k']} K over the supply. CFD "
                 f"exhaust {h['T_exhaust_c'] - m['supply_c']:.1f} K, volume mean {r['zones']['all']['mean_rise_k']} K, above the "
                 f"bridge {r['zones']['above_bridge']['mean_rise_k']} K, below it {r['zones']['below_bridge']['mean_rise_k']} K.\n")
        L.append("| Device | Checked on | Rating (°C) | CFD air round it (°C), mean / 95th percentile | rise (K) | well-mixed air (°C) | well-mixed checked (°C) | CFD checked (°C) | margin (K) |")
        L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
        for d in cw["rows"]:
            L.append(f"| {d['device']} | {d['checked_on']} | {d['rating_c'] if d['rating_c'] is not None else '-'} | {d['cfd_air_c']} / "
                     f"{d['cfd_air_p95_c']} | {d['cfd_air_rise_k']} | {d['wellmixed_air_c']} | {d['wellmixed_checked_c']} | {d['cfd_checked_c']} | "
                     f"{d['margin_k'] if d['margin_k'] is not None else '-'} |")
        L.append(f"\nAge of the air: V/Q {fl['nominal_time_constant_s']} s; air-change effectiveness {fl['air_change_effectiveness']} "
                 f"(0.5 = fully mixed); mean age above the bridge {r['zones']['above_bridge']['mean_age_s']} s, below "
                 f"{r['zones']['below_bridge']['mean_age_s']} s; {100 * fl['exhaust_flow_younger_than_quarter_tau']:.0f} % of the exhaust "
                 f"flow is younger than V/(4Q); {100 * fl['exhaust_flow_from_above_bridge']:.0f} % of it leaves above the bridge. "
                 f"Air older than 3 V/Q: {100 * fl['dead_volume_fraction']:.1f} % of the volume.\n")
        if fl["dead_zones_age_gt_3tau"]:
            L.append("| Dead zone (age > 3 V/Q) | x (mm) | y (mm) | z (mm) | volume (L) | mean age (s) | rise (K) |")
            L.append("|---|---|---|---|---:|---:|---:|")
            for i, z in enumerate(fl["dead_zones_age_gt_3tau"]):
                L.append(f"| {i + 1} | {z['x']} | {z['y']} | {z['z']} | {z['volume_L']} | {z['mean_age_s']} | {z['mean_rise_k']} |")
            L.append("")
    (OUT / "guard_cfd.md").write_text("\n".join(L) + "\n")


def main(cases):
    cj = GC.load_cooling()
    res = dict(cases={})
    first = None
    for c in cases:
        r = analyse(c)
        r["wellmixed"] = compare_wellmixed(r, cj)
        nm = pathlib.Path(c).name
        if first is None:
            first = r
        res["cases"][nm] = {k: v for k, v in r.items() if k != "_fields"}
        print(nm, json.dumps(res["cases"][nm]["heat"]), json.dumps(res["cases"][nm]["zones"]))
    figures(first)
    res["network"] = dict(sealed=GC.network(0.0), floor_open=next((v["meta"].get("network") for v in res["cases"].values() if v["meta"].get("network")), None),
                          note="guard_cfd.network(): the flows with cooling.py's resistances and fan curves, the hood path in parallel with the inlet")
    res["notes"] = ("Steady RANS (k-epsilon) of the guard's air on a Cartesian grid with the parts voxelised; see guard_cfd.py's docstring "
                    "for every assumption. 'Air round it' = fluid cells 2-3 cells (12-36 mm on the 12 mm grid) from the device's own cells.")
    json.dump(res, open(OUT / "guard_cfd.json", "w"), indent=1, default=float)
    write_md(res)
    print((OUT / "guard_cfd.md").read_text())
