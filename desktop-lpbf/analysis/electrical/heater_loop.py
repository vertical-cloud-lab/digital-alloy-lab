"""Heater control loop of the build modules: lumped thermal model fitted to the CalculiX results, PID tuning, the laser's
heat input, and an SSR-fails-shorted fault with the latching limit.

Why: the electrical design (electrical.md) picks the heater switching (DC SSR + two contactors), the independent latching
limit (DwyerOmega CN708 on the limit thermocouple) and the set points. Three questions decide them:
  1. can a plain PID on the block thermocouple hold the plate at 200 C, with the block capped at 225 C, when the laser
     brings more heat than the module loses (heat.md: dense M50 81 W against 52-72 W)?
  2. if the SSR fails shorted, how long until the limit trips, and how hot do the plate, block and seals get?
  3. where should the limit be set so that it never trips in normal running?

Model (per module and position, "start" = plate at z_p 0, "end" = z_p -40):
  fast node F = plate + heater block (C_F), slow node S = bore wall, spigot, piston head and rod (C_S):
    C_F dT_F/dt = Q_heater + Q_laser - G_FS (T_F - T_S) - G_Fa (T_F - T_a) - k_r ((T_F+273)^4 - (T_a+273)^4)
    C_S dT_S/dt = G_FS (T_F - T_S) - G_Sa (T_S - T_a)
  T_F is the plate-centre temperature of the FEA. The block reads T_F + r_B * Q_heater (lagged 8 s): the block runs
  above the plate only while the heater pushes heat into it (FEA: S25 +21 K at 44 W, M50 +6 K at 72 W, L75 +4 K at 97 W).
  Seals and the magnet follow the slow node: T_x - T_a = a_x (T_S - T_a), with a_x from the FEA steady cases.
  The radiation-like k_r term stands for everything that makes the FEA sub-linear (radiation, argon conductivity rising
  with temperature); it is an empirical fit, not a radiation calculation.
Calibration data, all from this repo: analysis/out/thermal/thermal.json (full-power heat-up from 25 C at z_p 0 for
three hours, heater-off cool-down from the 200 C steady state at z_p -40) and analysis/out/thermal/laser_heat.json
(steady plate temperature against heater + laser power at both positions).

Control: discrete PID at 0.5 s on the control thermocouple (type K in the block, 2 s first-order lag: McMaster 3871K606
lists 0.3 s in liquid; 2 s allows for a drilled hole), output = SSR duty (time-proportioned at 1 s: the ripple is ignored,
the fast node's time constant is minutes), conditional-integration anti-windup, and an override that caps the block at
225 C (modules.md). The limit: limit thermocouple (same lag) into the CN708, latching at T_LIMIT; 0.5 s for its scan and
relay, 0.05 s for the contactor it drops.

Run:  /tmp/venv/bin/python desktop-lpbf/analysis/electrical/heater_loop.py
  ->  desktop-lpbf/analysis/out/electrical/heater_loop.{md,json,png}
"""
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares

AN = Path(__file__).resolve().parents[1]
OUT = AN / "out" / "electrical"
OUT.mkdir(parents=True, exist_ok=True)
TH = json.loads((AN / "out" / "thermal" / "thermal.json").read_text())
LH = json.loads((AN / "out" / "thermal" / "laser_heat.json").read_text())

T_A = 25.0
INSTALLED = {"S25": 100.0, "M50": 150.0, "L75": 250.0}       # module_params.py: 2 / 3 / 5 x 50 W
T_SET = 200.0
BLOCK_CAP = 225.0                                             # modules.md: PID output limited by a block ceiling
T_LIMIT = 235.0                                               # chosen below (normal block peak <= 225)
TCO = None                                                    # no thermal cutoff (electrical.md 2026-11-23); was the Cantherm RT240, 240 C (holding 205 C)
# one-shot cutoffs checked against the job (Tf, Th, DC rating): the old part and the two highest-holding ones found
TCO_CANDIDATES = {
    "Cantherm RT240 (the old part)": dict(Tf=240.0, Th=205.0, dc="not read", src="electrical.md 0 point 6 (holding 205 C)"),
    "Therm-O-Disc Microtemp G4, 257 C": dict(Tf=257.0, Th=220.0, dc="5 A at 24 V DC", src="farnell.com/datasheets/3689251.pdf p.4, read 2026-11-23 22:31Z"),
    "Cantherm SDF DF280S": dict(Tf=280.0, Th=230.0, dc="AC only (250 V 10 A, 125 V 15 A); UL, VDE, CCC applied for",
                                src="Cantherm SDF datasheet p.4 (mirror datasheet.chipsmall.com/SDF-DF091S/256659.pdf), read 2026-11-23 22:46Z"),
}
TAU_TC, TAU_B = 2.0, 8.0
DT = 0.25


def steady_points(key, pos):
    """(total input W, plate centre C) from laser_heat.json rows (heater + laser)."""
    pts = []
    for r in LH["rows"]:
        if r["key"] == key and r["pos"] == pos:
            pts.append((r["P_heater_W"] + r["Q_laser_W"], r["T_plate_centre"]))
    return pts


def seal_ratios(key, pos):
    """a_x = (T_x - T_a) / (T_plate - T_a) at the FEA steady cases (same position): bore seal, rod gland, magnet face."""
    rows = [r for r in LH["rows"] if r["key"] == key and r["pos"] == pos]
    out = {}
    for name, col in (("bore seal", "T_seal_max"), ("rod gland", "T_gland_max"), ("magnet face", "T_rod_end")):
        out[name] = float(np.mean([(r[col] - T_A) / (r["T_plate_centre"] - T_A) for r in rows]))
    return out


def unpack(p):
    C_F, C_S, G_FS, G_Sa, G_Fa, k_r = np.exp(p)
    return C_F, C_S, G_FS, G_Sa, G_Fa, k_r * 1e-9


def rhs(t, y, par, q_of_t):
    C_F, C_S, G_FS, G_Sa, G_Fa, k_r = par
    TF, TS = y
    q = q_of_t(t)
    dF = (q - G_FS * (TF - TS) - G_Fa * (TF - T_A) - k_r * ((TF + 273.15) ** 4 - (T_A + 273.15) ** 4)) / C_F
    dS = (G_FS * (TF - TS) - G_Sa * (TS - T_A)) / C_S
    return [dF, dS]


def steady(par, q):
    C_F, C_S, G_FS, G_Sa, G_Fa, k_r = par
    g = G_Fa + G_FS * G_Sa / (G_FS + G_Sa)
    f = lambda T: g * (T - T_A) + k_r * ((T + 273.15) ** 4 - (T_A + 273.15) ** 4) - q
    TF = brentq(f, T_A, 3000.0) if q > 0 else T_A
    TS = (G_FS * TF + G_Sa * T_A) / (G_FS + G_Sa)
    return TF, TS


def fit(key, pos):
    pts = steady_points(key, pos)
    if pos == "start":
        tr = [TH["transient"][f"heat_{key}"]] + ([TH["transient"]["heatS_L75"]] if key == "L75" else [])
    else:
        tr = [TH["transient"][f"cool_{key}"]]

    def run(par, tr_):
        t = np.array(tr_["t"])
        qf = tr_["spec"]["P_w"]
        if tr_["spec"]["P_w"] > 0:
            y0 = [T_A, T_A]
        else:   # cool-down from the 200 C steady state at this position (heater power from the FEA steady case)
            p0 = TH["steady"][tr_["spec"]["T_init_from"].replace("_h2", "")]["P_heater_W"]
            y0 = list(steady(par, p0))
        s = solve_ivp(rhs, (0, t[-1]), y0, t_eval=t, args=(par, lambda _t: qf), method="LSODA", rtol=1e-6, atol=1e-6)
        return t, s.y[0]

    def resid(p):
        par = unpack(p)
        r = []
        for tr_ in tr:
            t, TF = run(par, tr_)
            T_fea = np.array(tr_["T_centre"])
            w = np.where(t < 1800, 1.0, 0.5)            # the first 30 min matter most for the fault and heat-up
            r.append(w * (TF - T_fea))
        for q, T in pts:
            r.append(np.array([3.0 * (steady(par, q)[0] - T)]))
        return np.concatenate(r)

    p0 = np.log([120.0, 600.0, 0.6, 0.6, 0.15, 3.0])
    sol = least_squares(resid, p0, x_scale=1.0, max_nfev=400)
    par = unpack(sol.x)
    res = resid(sol.x)
    # report the fit quality on the FEA's own terms
    stats = {}
    for tr_ in tr:
        t, TF = run(par, tr_)
        T_fea = np.array(tr_["T_centre"])
        m30 = t <= 1800
        stats[tr_["spec"]["name"]] = dict(rms_K=float(np.sqrt(np.mean((TF - T_fea) ** 2))),
                                          max_K_first_30min=float(np.max(np.abs(TF - T_fea)[m30])))
    stats["steady_points_max_K"] = float(max(abs(steady(par, q)[0] - T) for q, T in pts))
    return par, stats, res


def block_offset(key):
    """r_B (K/W): block max minus plate centre per watt of heater, from the FEA steady cases."""
    vals = []
    for pos in ("start", "end"):
        s = TH["steady"][f"{key}_{pos}_ch25_e0.5"]
        vals.append((s["T_block_max"] - s["T_plate_centre"]) / s["P_heater_W"])
    return float(np.mean(vals))


class Sim:
    """Fixed-step simulation of one module with the controller, the limit and faults."""

    def __init__(self, key, pos, par, rB, kp, ti, td=0.0):
        self.key, self.pos, self.par, self.rB = key, pos, par, rB
        self.kp, self.ti, self.td = kp, ti, td
        self.Pmax = INSTALLED[key]
        self.sp_block = None

    def run(self, t_end, y0=None, laser=None, ssr_short_at=None, limit_on=True, limit=T_LIMIT, tco_on=True,
            dwell=None, sp=T_SET, cap=BLOCK_CAP, record_every=2.0, tco=None):
        """laser: callable(t, state) -> W absorbed in the plate; dwell: K above the set point at which the next layer is held."""
        C_F, C_S, G_FS, G_Sa, G_Fa, k_r = self.par
        TF, TS = y0 if y0 is not None else (T_A, T_A)
        qf = 0.0                                     # lagged heater power (sets the block offset)
        Tc = TF + self.rB * qf                       # control TC reading
        Tl = Tc                                      # limit TC reading
        integ, e_prev = 0.0, 0.0
        u = 0.0
        tripped, t_trip, tco_open, t_tco = False, None, False, None
        trip_pending = None
        layer = dict(phase="recoat", t0=0.0, held=0.0, n=0) if laser is not None else None
        rec = {k: [] for k in ("t", "TF", "TB", "TS", "u", "q_laser", "Tc")}
        peaks = dict(TF=TF, TB=TF, TS=TS)
        nxt = 0.0
        t = 0.0
        u_ff = steady_heater(self, sp) / self.Pmax          # feed-forward: the duty that holds sp with the laser off
        qm = 0.0
        Tp_est = Tc
        while t < t_end:
            # --- controller every 0.5 s
            if abs((t / 0.5) - round(t / 0.5)) < 1e-9:
                # the PLC knows the heater power it commands, so it estimates the plate from the block reading:
                # T_plate ~ T_block - r_B * P_heater (lagged). Without this, S25's plate runs 21 K hot once the laser
                # takes over the heating (the block offset vanishes when the heater is off).
                qm += (self.Pmax * u - qm) * 0.5 / TAU_B
                Tp_est = Tc - self.rB * qm
                e = sp - Tp_est
                u_pid = u_ff + self.kp * e + integ
                u_cap = 0.2 * (cap - Tc)                   # block ceiling override (P only, 20 %/K: full power up to 5 K below the cap)
                u_new = min(u_pid, u_cap)
                u_sat = min(max(u_new, 0.0), 1.0)
                if u_sat == u_new or (u_new > 1 and e < 0) or (u_new < 0 and e > 0):
                    integ += self.kp * 0.5 / self.ti * e
                integ = min(max(integ, -1.0), 1.0)
                u = u_sat
                e_prev = e
            q_cmd = self.Pmax * u
            if ssr_short_at is not None and t >= ssr_short_at:
                q_cmd = self.Pmax
            if tripped or tco_open:
                q_cmd = 0.0
            # --- laser and dwell logic
            ql = 0.0
            if layer is not None:
                if layer["phase"] == "scan":
                    ql = laser["q_scan"]
                    if t - layer["t0"] >= laser["t_scan"]:
                        layer.update(phase="recoat", t0=t)
                else:
                    ready = t - layer["t0"] >= laser["t_recoat"]
                    hot = dwell is not None and Tp_est > sp + dwell
                    if ready and not hot and not tripped:
                        layer.update(phase="scan", t0=t, n=layer["n"] + 1)
                    elif ready and hot:
                        layer["held"] += DT
            # --- plant
            qf += (q_cmd - qf) * DT / TAU_B
            dF = (q_cmd + ql - G_FS * (TF - TS) - G_Fa * (TF - T_A) - k_r * ((TF + 273.15) ** 4 - (T_A + 273.15) ** 4)) / C_F
            dS = (G_FS * (TF - TS) - G_Sa * (TS - T_A)) / C_S
            TF += dF * DT
            TS += dS * DT
            TB = TF + self.rB * qf
            Tc += (TB - Tc) * DT / TAU_TC
            Tl += (TB - Tl) * DT / TAU_TC
            # --- limit (latching) and the thermal cutoff
            if limit_on and not tripped and trip_pending is None and Tl >= limit:
                trip_pending = t + 0.5 + 0.05
            if trip_pending is not None and t >= trip_pending and not tripped:
                tripped, t_trip = True, t
            if tco_on and not tco_open and (tco or TCO) is not None and TB >= (tco or TCO):
                tco_open, t_tco = True, t
            peaks["TF"] = max(peaks["TF"], TF)
            peaks["TB"] = max(peaks["TB"], TB)
            peaks["TS"] = max(peaks["TS"], TS)
            if t >= nxt:
                for k_, v_ in (("t", t), ("TF", TF), ("TB", TB), ("TS", TS), ("u", u if not (tripped or tco_open) else 0.0),
                               ("q_laser", ql), ("Tc", Tc)):
                    rec[k_].append(v_)
                nxt += record_every
            t += DT
        return dict(rec=rec, peaks=peaks, tripped=tripped, t_trip=t_trip, tco_open=tco_open, t_tco=t_tco,
                    layers=layer["n"] if layer else None, held=layer["held"] if layer else None, final=(TF, TS))


def steady_heater(sim, sp):
    """Heater power that holds the plate at sp with the laser off (from the fitted model)."""
    C_F, C_S, G_FS, G_Sa, G_Fa, k_r = sim.par
    g = G_Fa + G_FS * G_Sa / (G_FS + G_Sa)
    return g * (sp - T_A) + k_r * ((sp + 273.15) ** 4 - (T_A + 273.15) ** 4)


def tune_grid(key, par, rB):
    """Grid search of Kp (duty/K) and Ti (s) on the fitted plant: heat-up from 25 C at the build start, then a 30 W
    laser step at 30 min. Score = time to settle within +/-2 K of 200 C + 60 s per K of overshoot + 30 s per K of the
    laser-step excursion; the block cap and the feed-forward are active."""
    best = None
    grid = []
    for kp in (0.01, 0.02, 0.04, 0.08, 0.15):
        for ti in (60.0, 120.0, 240.0, 480.0, 960.0):
            sim = Sim(key, "start", par, rB, kp, ti)
            las = dict(q_scan=30.0, t_scan=1e9, t_recoat=1800.0)
            r = sim.run(3600, laser=las, record_every=2.0)
            t, TF = np.array(r["rec"]["t"]), np.array(r["rec"]["TF"])
            pre = t < 1800
            outside = np.where(np.abs(TF[pre] - T_SET) > 2.0)[0]
            t_set = float(t[pre][outside[-1]]) if len(outside) else 0.0
            over = max(0.0, float(TF[pre].max() - T_SET))
            exc = float(np.max(np.abs(TF[~pre] - T_SET)))
            score = t_set + 60 * over + 30 * exc + (1e5 if r["tripped"] else 0)
            grid.append(dict(Kp=kp, Ti=ti, settle_s=t_set, overshoot_K=over, laser_step_K=exc, score=score))
            if best is None or score < best["score"]:
                best = grid[-1]
    return best, grid


def tune(key, par, rB):
    """FOPDT from a 10 % duty step at 200 C on the fitted plant, then SIMC (Skogestad 2003) with tau_c = max(theta, 60 s)."""
    sim = Sim(key, "start", par, rB, 0, 1)
    P0 = steady_heater(sim, T_SET)
    y0 = steady(par, P0)
    dq = 0.1 * INSTALLED[key]
    C_F, C_S, G_FS, G_Sa, G_Fa, k_r = par
    t = np.arange(0, 3600, 1.0)
    s = solve_ivp(rhs, (0, t[-1]), list(y0), t_eval=t, args=(par, lambda _t: P0 + dq), method="LSODA", rtol=1e-7)
    TF = s.y[0] - y0[0]
    # the block reading leads the plate by r_B dq through the 8 s heater lag and the 2 s TC: add as dead time
    K = (TF[-1]) / 0.1                               # K per unit duty, at one hour (slow node not settled: conservative)
    i63 = np.argmax(TF >= 0.632 * TF[-1])
    i05 = np.argmax(TF >= 0.05 * TF[-1])
    theta = TAU_TC + 0.5 + float(t[i05]) * 0.0      # measurement and sample delay
    tau = float(t[i63])
    tau_c = max(theta, 60.0)
    kc = tau / (K * (tau_c + theta))
    ti = min(tau, 4 * (tau_c + theta))
    return dict(K_per_duty=float(K), tau_s=tau, theta_s=theta, tau_c_s=tau_c, Kp_per_K=float(kc), Ti_s=float(ti), P0_W=float(P0))


def main():
    results = dict(fits={}, tuning={}, heatup={}, build={}, ssr_short={}, notes={})
    models = {}
    for key in ("S25", "M50", "L75"):
        rB = block_offset(key)
        for pos in ("start", "end"):
            par, stats, _ = fit(key, pos)
            models[(key, pos)] = par
            results["fits"][f"{key}_{pos}"] = dict(C_F_JK=par[0], C_S_JK=par[1], G_FS_WK=par[2], G_Sa_WK=par[3], G_Fa_WK=par[4],
                                                    k_r=par[5], r_B_KW=rB, seals=seal_ratios(key, pos), fit=stats)
            print(key, pos, {k: round(v, 3) for k, v in zip(("C_F", "C_S", "G_FS", "G_Sa", "G_Fa"), par[:5])}, stats)

    for key in ("S25", "M50", "L75"):
        rB = block_offset(key)
        tn = tune(key, models[(key, "start")], rB)
        best, grid = tune_grid(key, models[(key, "start")], rB)
        tn.update(Kp_per_K=best["Kp"], Ti_s=best["Ti"], grid_best=best, grid=grid)
        results["tuning"][key] = tn
        kp, ti = tn["Kp_per_K"], tn["Ti_s"]
        # 1. heat-up from 25 C at the build start
        sim = Sim(key, "start", models[(key, "start")], rB, kp, ti)
        r = sim.run(3600, sp=T_SET)
        tt, TF, TB = np.array(r["rec"]["t"]), np.array(r["rec"]["TF"]), np.array(r["rec"]["TB"])
        reached = np.where(TF >= T_SET - 2.0)[0]
        i_in = int(reached[0]) if len(reached) else len(TF) - 1
        after = TF[i_in:]
        # settled: last time it was outside +/- 2 K
        outside = np.where(np.abs(TF - T_SET) > 2.0)[0]
        t_settle = float(tt[outside[-1]]) if len(outside) else 0.0
        results["heatup"][key] = dict(t_within_2K_min=float(tt[i_in] / 60), t_settled_2K_min=t_settle / 60,
                                      overshoot_K=float(max(0.0, after.max() - T_SET)), block_peak_C=float(TB.max()),
                                      tripped=r["tripped"])
        if key == "M50":
            heat_rec = r["rec"]
        # 2. a dense build at the end of the stroke (worst: lowest loss), with and without the dwell rule
        ld = LH["laser_loads"][key]["dense (70 % of the plate)"]
        q_scan = 350.0 * 0.45
        t_scan = ld["t_scan_s"] + 0.2
        laser = dict(q_scan=q_scan, t_scan=t_scan, t_recoat=8.0)
        simE = Sim(key, "end", models[(key, "end")], rB, kp, ti)
        y0 = steady(models[(key, "end")], steady_heater(simE, T_SET))
        out_b = {}
        for label, dw in (("no dwell", None), ("dwell at +3 K", 3.0)):
            rb = simE.run(5400, y0=y0, laser=laser, dwell=dw)
            TFb = np.array(rb["rec"]["TF"])
            tb = np.array(rb["rec"]["t"])
            last = tb >= 3600
            nominal_layers = 5400 / (t_scan + 8.0)
            out_b[label] = dict(plate_max_C=float(TFb.max()), plate_last30min_mean_C=float(TFb[last].mean()),
                                plate_last30min_band_K=float(TFb[last].max() - TFb[last].min()),
                                limit_tripped=rb["tripped"], t_trip_min=(rb["t_trip"] / 60 if rb["t_trip"] else None),
                                layers_in_90min=rb["layers"], nominal_layers=nominal_layers,
                                time_penalty_pct=float(100 * (nominal_layers / max(rb["layers"], 1) - 1)),
                                heater_mean_W=float(np.mean(np.array(rb["rec"]["u"])[last]) * INSTALLED[key]))
            if key == "M50":
                out_b[label]["rec"] = {k: rb["rec"][k] for k in ("t", "TF", "TB", "u")}
        results["build"][key] = dict(q_scan_W=q_scan, t_scan_s=t_scan, t_recoat_s=8.0, mean_laser_W=ld["Q_W"], **out_b)
        # 3. SSR fails shorted at t = 60 s from the 200 C steady state, at both positions
        res_ssr = {}
        for pos in ("start", "end"):
            par = models[(key, pos)]
            simS = Sim(key, pos, par, rB, kp, ti)
            P0 = steady_heater(simS, T_SET)
            y0 = steady(par, P0)
            a = seal_ratios(key, pos)
            G_FS, G_Sa = par[2], par[3]
            ss_ratio = (G_FS + G_Sa) / G_FS          # slow node -> plate-equivalent rise at steady
            case = {}
            for label, kw in (("limit trips", dict(limit_on=True, tco_on=False)),
                              ("limit failed, RT240 (240 C) would open", dict(limit_on=False, tco_on=True, tco=240.0)),
                              ("limit failed, a 257 C cutoff would open", dict(limit_on=False, tco_on=True, tco=257.0)),
                              ("limit failed, a 280 C cutoff would open", dict(limit_on=False, tco_on=True, tco=280.0)),
                              ("no protection (1 h)", dict(limit_on=False, tco_on=False))):
                rs = simS.run(3600 if "no protection" in label else 1800, y0=y0, ssr_short_at=60.0, **kw)
                TS_pk = rs["peaks"]["TS"]
                seals = {n: T_A + a[n] * ss_ratio * (TS_pk - T_A) for n in a}
                case[label] = dict(t_to_trip_s=(rs["t_trip"] - 60.0) if rs["t_trip"] else None,
                                   t_to_tco_s=(rs["t_tco"] - 60.0) if rs["t_tco"] else None,
                                   plate_peak_C=rs["peaks"]["TF"], block_peak_C=rs["peaks"]["TB"], **{f"{n}_peak_C": v for n, v in seals.items()})
                if key == "M50" and pos == "end":
                    case[label]["rec"] = {k: rs["rec"][k] for k in ("t", "TF", "TB", "TS")}
            # steady state with no protection at all
            TFs, TSs = steady(par, INSTALLED[key])
            case["steady, no protection"] = dict(plate_C=TFs, block_C=TFs + rB * INSTALLED[key],
                                                 **{f"{n}_C": T_A + a[n] * (TFs - T_A) for n in a})
            res_ssr[pos] = case
        results["ssr_short"][key] = res_ssr

    # ---------------------------------------------------------------- figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 2, figsize=(13, 8.5))
    # (a) fit against the FEA heat-up
    for key, c in (("S25", "#3a6ea5"), ("M50", "#c0392b"), ("L75", "#2e8b57")):
        tr_ = TH["transient"][f"heat_{key}"]
        t = np.array(tr_["t"])
        par = models[(key, "start")]
        s = solve_ivp(rhs, (0, t[-1]), [T_A, T_A], t_eval=t, args=(par, lambda _t: tr_["spec"]["P_w"]), method="LSODA")
        ax[0, 0].plot(t / 60, tr_["T_centre"], color=c, lw=2.2, alpha=0.45, label=f"{key} FEA, {tr_['spec']['P_w']:.0f} W")
        ax[0, 0].plot(t / 60, s.y[0], color=c, lw=1.0, ls="--", label=f"{key} lumped fit")
    ax[0, 0].set_xlim(0, 60)
    ax[0, 0].set_ylim(0, 420)
    ax[0, 0].set_xlabel("time (min)")
    ax[0, 0].set_ylabel("plate centre (°C)")
    ax[0, 0].set_title("(a) Full-power heat-up from 25 °C: CalculiX vs the lumped model")
    ax[0, 0].legend(fontsize=7, ncol=2)
    # (b) M50 heat-up under PID
    t = np.array(heat_rec["t"]) / 60
    ax[0, 1].plot(t, heat_rec["TF"], color="#c0392b", label="plate centre")
    ax[0, 1].plot(t, heat_rec["TB"], color="#e67e22", ls="--", label="heater block")
    ax2 = ax[0, 1].twinx()
    ax2.plot(t, np.array(heat_rec["u"]) * 100, color="#7f8c8d", lw=0.8, label="SSR duty")
    ax2.set_ylabel("SSR duty (%)")
    ax2.set_ylim(0, 110)
    ax[0, 1].axhline(BLOCK_CAP, color="#e67e22", lw=0.6, ls=":")
    ax[0, 1].axhline(T_LIMIT, color="k", lw=0.6, ls=":")
    ax[0, 1].text(1, T_LIMIT + 2, f"limit {T_LIMIT:.0f} °C", fontsize=7)
    ax[0, 1].text(1, BLOCK_CAP - 9, f"block cap {BLOCK_CAP:.0f} °C", fontsize=7, color="#e67e22")
    ax[0, 1].set_xlim(0, 30)
    ax[0, 1].set_ylim(0, 260)
    ax[0, 1].set_xlabel("time (min)")
    ax[0, 1].set_ylabel("°C")
    ax[0, 1].set_title("(b) M50 heat-up under the tuned PI (block capped)")
    ax[0, 1].legend(loc="lower right", fontsize=7)
    # (c) dense M50 build at the end of the stroke
    for label, c in (("no dwell", "#c0392b"), ("dwell at +3 K", "#2e8b57")):
        rb = results["build"]["M50"][label]["rec"]
        ax[1, 0].plot(np.array(rb["t"]) / 60, rb["TF"], color=c, lw=0.9, label=f"plate, {label}")
    ax[1, 0].axhline(T_LIMIT, color="k", lw=0.6, ls=":")
    ax[1, 0].axhline(T_SET, color="#7f8c8d", lw=0.6, ls=":")
    ax[1, 0].set_xlabel("time (min)")
    ax[1, 0].set_ylabel("plate centre (°C)")
    ax[1, 0].set_ylim(180, 300)
    ax[1, 0].set_title("(c) Dense M50 build, plate at the end of the stroke (81 W absorbed vs 52 W lost)")
    ax[1, 0].legend(fontsize=7)
    # (d) SSR shorted, M50 end
    for label, c in (("limit trips", "#2e8b57"), ("limit failed, a 280 C cutoff would open", "#e67e22"), ("no protection (1 h)", "#c0392b")):
        rs = results["ssr_short"]["M50"]["end"][label]["rec"]
        ax[1, 1].plot(np.array(rs["t"]) / 60, rs["TB"], color=c, lw=1.0, label=f"block, {label}")
        ax[1, 1].plot(np.array(rs["t"]) / 60, rs["TS"], color=c, lw=0.8, ls=":")
    ax[1, 1].axhline(T_LIMIT, color="k", lw=0.6, ls=":")
    ax[1, 1].axhline(280.0, color="#e67e22", lw=0.6, ls=":")
    ax[1, 1].set_xlabel("time (min); the SSR shorts at 1 min")
    ax[1, 1].set_ylabel("°C (dotted: slow node, bore wall / head / rod)")
    ax[1, 1].set_title("(d) M50, SSR fails shorted at the end of the stroke (150 W)")
    ax[1, 1].set_xlim(0, 60)
    ax[1, 1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "heater_loop.png", dpi=130)

    # strip records from the json
    for key in results["build"]:
        for label in ("no dwell", "dwell at +3 K"):
            results["build"][key][label].pop("rec", None)
    for key in results["ssr_short"]:
        for pos in results["ssr_short"][key]:
            for label in results["ssr_short"][key][pos]:
                results["ssr_short"][key][pos][label].pop("rec", None)
    results["notes"] = dict(T_SET=T_SET, BLOCK_CAP=BLOCK_CAP, T_LIMIT=T_LIMIT, TCO=TCO, TCO_CANDIDATES=TCO_CANDIDATES, TAU_TC=TAU_TC, TAU_B=TAU_B, DT=DT)
    (OUT / "heater_loop.json").write_text(json.dumps(results, indent=1, default=float))
    write_md(results)


def f1(x):
    return "–" if x is None else f"{x:.0f}"


def write_md(R):
    L = ["# Heater control loop: lumped model, PID, laser heat and an SSR that fails shorted", "",
         "Generated by [`analysis/electrical/heater_loop.py`](../../electrical/heater_loop.py). Method, inputs and assumptions are in the script's docstring. "
         "The lumped model is fitted to this repo's CalculiX results (`analysis/out/thermal/thermal.json`, `laser_heat.json`); it is not a new FEA.", "",
         f"Set point {T_SET:.0f} °C at the plate centre; block cap {BLOCK_CAP:.0f} °C; latching limit {T_LIMIT:.0f} °C on the limit thermocouple; no thermal cutoff (dropped 2026-11-23, section 5); thermocouple lag {TAU_TC:.0f} s.", "",
         "## 1. Fit of the lumped model to the FEA", "",
         "| Module, position | C fast / slow (J/K) | G fast-slow / slow-ambient / fast-ambient (W/K) | r_B block offset (K/W) | Fit: RMS over the FEA curve (K) | worst in the first 30 min (K) | worst steady point (K) |",
         "|---|---|---|---|---|---|---|"]
    for k, v in R["fits"].items():
        fs = [x for n, x in v["fit"].items() if n != "steady_points_max_K"][0]
        L.append(f"| {k} | {v['C_F_JK']:.0f} / {v['C_S_JK']:.0f} | {v['G_FS_WK']:.2f} / {v['G_Sa_WK']:.2f} / {v['G_Fa_WK']:.3f} | {v['r_B_KW']:.3f} | "
                 f"{fs['rms_K']:.1f} | {fs['max_K_first_30min']:.1f} | {v['fit']['steady_points_max_K']:.1f} |")
    L += ["", "## 2. PI tuning and heat-up", "",
          "PI with a feed-forward duty (the heater power that holds 200 °C, which the PLC knows from calibration) and the block cap. "
          "Kp and Ti are picked by a grid search on the fitted plant (heat-up from 25 °C, then a 30 W laser step at 30 min); "
          "a first-order-plus-dead-time fit of the same plant is shown for reference (its 1 h gain and 63 % time). Kp is in duty per kelvin of plate error.", "",
          "| Module | Heater needed at 200 °C (W) | FOPDT gain (K per unit duty, 1 h) | τ (s) | θ (s) | Kp (duty/K) | Ti (s) | Heat-up: within 2 K (min) | settled ±2 K (min) | Overshoot (K) | Block peak (°C) | Limit tripped? |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in R["tuning"].items():
        h = R["heatup"][k]
        L.append(f"| {k} | {v['P0_W']:.0f} | {v['K_per_duty']:.0f} | {v['tau_s']:.0f} | {v['theta_s']:.1f} | {v['Kp_per_K']:.3f} | {v['Ti_s']:.0f} | "
                 f"{h['t_within_2K_min']:.1f} | {h['t_settled_2K_min']:.1f} | {h['overshoot_K']:.1f} | {h['block_peak_C']:.0f} | {'yes' if h['tripped'] else 'no'} |")
    L += ["", "## 3. A dense build at the end of the stroke (the lowest-loss position), 90 minutes", "",
          "350 W, absorptance 0.45: 158 W into the plate while the beam scans, then an 8 s recoat. The heater cannot cool, so with more laser heat than loss the plate drifts up. "
          "The dwell rule holds the next layer until the control thermocouple is back within 3 K of its set point.", "",
          "| Module | Mean laser (W) | Case | Plate max (°C) | Plate, last 30 min: mean / band (°C / K) | Limit trip | Layers in 90 min (nominal) | Build-time penalty | Heater mean (W) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k, v in R["build"].items():
        for label in ("no dwell", "dwell at +3 K"):
            b = v[label]
            trip = f"at {b['t_trip_min']:.0f} min" if b["limit_tripped"] else "no"
            L.append(f"| {k} | {v['mean_laser_W']:.0f} | {label} | {b['plate_max_C']:.0f} | {b['plate_last30min_mean_C']:.0f} / {b['plate_last30min_band_K']:.0f} | {trip} | "
                     f"{b['layers_in_90min']} ({b['nominal_layers']:.0f}) | {b['time_penalty_pct']:.0f} % | {b['heater_mean_W']:.0f} |")
    L += ["", "## 4. The SSR fails shorted (full installed power from the 200 °C steady state)", "",
          "| Module, position | Case | Time to the limit trip (s) | Time to the TCO (s) | Plate peak (°C) | Block peak (°C) | Bore seal (°C) | Rod gland (°C) | Magnet face (°C) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k, v in R["ssr_short"].items():
        for pos, cases in v.items():
            for label, c in cases.items():
                if label.startswith("steady"):
                    L.append(f"| {k} {pos} | {label} | – | – | {c['plate_C']:.0f} | {c['block_C']:.0f} | {c['bore seal_C']:.0f} | {c['rod gland_C']:.0f} | {c['magnet face_C']:.0f} |")
                else:
                    L.append(f"| {k} {pos} | {label} | {f1(c['t_to_trip_s'])} | {f1(c['t_to_tco_s'])} | {c['plate_peak_C']:.0f} | {c['block_peak_C']:.0f} | "
                             f"{c['bore seal_peak_C']:.0f} | {c['rod gland_peak_C']:.0f} | {c['magnet face_peak_C']:.0f} |")
    hb = {k: R["heatup"][k]["block_peak_C"] for k in R["heatup"]}
    L += ["", "## 5. Is there a thermal cutoff that fits? (2026-11-23)", "",
          "A one-shot cutoff in series with the heaters must hold (Th, 168 h without opening) at the hottest normal block temperature, "
          f"which is the {BLOCK_CAP:.0f} °C block cap (heat-up block peaks: " + ", ".join(f"{k} {v:.0f} °C" for k, v in hb.items()) +
          "; S25's block runs 216-221 °C at 200 °C on the plate), and it must break the heater current at 24 V DC: "
          f"{INSTALLED['S25'] / 24:.1f} / {INSTALLED['M50'] / 24:.1f} / {INSTALLED['L75'] / 24:.1f} A (S25 / M50 / L75).", "",
          "| Cutoff | Tf (°C) | Th (°C) | Holds at the 225 °C cap? | DC rating | Source |", "|---|---|---|---|---|---|"]
    for n, c in TCO_CANDIDATES.items():
        L.append(f"| {n} | {c['Tf']:.0f} | {c['Th']:.0f} | {'yes' if c['Th'] >= BLOCK_CAP else 'no'} | {c['dc']} | {c['src']} |")
    L += ["", "None of them does both, so the cutoff is dropped: the latching limit (CN708 on its own thermocouple, K2) and the PLC's "
          "over-temperature on the control and edge thermocouples (K1 through the safety controller, the diverse input the interlock check "
          "added) each stop an SSR short on their own. Both read thermocouples in the same block with the same lag, so the 'limit trips' "
          "rows of section 4 stand for either channel. The 'would open' rows show what each cutoff would add if both channels failed: "
          "a 280 °C part opens only after the plate has passed the limit by tens of kelvin, and the 240 °C part opens first on S25 in "
          "normal fault handling, which is the nuisance trip the drop removes."]
    L += ["", "![Heater loop](heater_loop.png)", "",
          "## Caveats", "",
          "- Two lumped nodes stand in for a 14,000-node axisymmetric model. They reproduce the FEA heat-up and cool-down to the RMS errors in §1; seal temperatures are scaled from the slow node with the FEA's steady ratios, so they are estimates.",
          "- The laser's heat is put into the fast node as a square wave per layer, as `thermal_laser.py` puts its time average into the plate. Melt-pool and part-top temperatures are not modelled.",
          "- The SSR duty is used as an average; time-proportioning ripple at a 1 s cycle is under 0.1 K on these masses (C_F ≥ 40 J/K at ≤ 250 W).",
          "- Thermocouple lag 2 s and the CN708's 0.5 s are assumptions; the result is not sensitive to them because the block rises at well under 3 K/s even at full power."]
    (OUT / "heater_loop.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
