"""Electrical power checks for the desktop LPBF tray: per-leg currents, inrush against the breakers, the UPS's runtime
through a power cut, heat in the 3U DIN drawer, voltage drop over the real cable runs, heating of the hermetic pins,
and protective-conductor current.

Inputs: the load list below (each with its source or marked as an estimate), the dock of byu-vcl PR 318 (208Y/120 V,
L1 + L2 + N + PE, 30 A breaker, 24 A continuous), cable runs measured on cad/lpbf_low.py coordinates (rack x -990..-430,
DIN drawer z 170-301, process module around x 0, gas module x 400-990, dock at x 1156, y 370), and the heater and
module figures of modules.md / analysis/out/thermal. It refines analysis/tray/tray_budget.py (which is per phase)
by device and branch; where the two overlap, the totals agree within the estimates.

Run: /tmp/venv/bin/python desktop-lpbf/analysis/electrical/power_budget.py -> desktop-lpbf/analysis/out/electrical/power.{md,json}
"""
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out" / "electrical"
OUT.mkdir(parents=True, exist_ok=True)

V_LN, V_LL = 120.0, 208.0
DOCK_CONT_A = 24.0

# ------------------------------------------------------------------ loads on the AC side
# name: (branch, connection, rated W, power factor, build-typical W, inrush peak A (estimate), inrush s, source)
AC = {
    "laser": ("Q1 2P 15 A", "L1-L2", 1700.0, 1700 / 1900, 1056.0, 40.0, 0.01,
              "IPG spec sheet: 1,700 W / 1,900 VA max at 500 W out; typical-build draw from tray_budget.py (350 W at 60 % duty). Inrush not published: 40 A for 10 ms assumed (PFC front end)"),
    "UPS input": ("Q2 2P 15 A (multiwire)", "L1-N", None, 0.95, None, 50.0, 0.01,
                  "Eaton 5PX1500RTG2, 1,500 VA / 1,440 W out (model); input = backed load / 0.9 + recharge 100 W (estimate). Inrush 50 A, one half-cycle (estimate)"),
    "heater supply": ("Q2 2P 15 A (multiwire)", "L2-N", 250 / 0.89, 0.95, 97 / 0.89, 30.0, 0.005,
                      "Mean Well LRS-350-24 at the L75's 250 W, 89 % efficient (datasheet); its cold-start inrush is listed as 60 A at 230 VAC, so ~30 A at 120 VAC"),
    "pump": ("Q3 1P 15 A", "L2-N", 7 * 115 * 0.75, 0.75, 0.0, 42.0, 0.3,
             "McMaster 4396K21, 1/2 hp, 7 A at 115 V; locked-rotor ~6 x FLA (typical for a PSC/cap-start motor, estimate)"),
    "blower": ("Q4 1P 6 A", "L2-N", 230.0, 0.8, 50.0, 12.0, 0.2,
               "upper bound McMaster 9960K51 (1/8 hp, 115 V); a sealed 24 V brushless blower would be 20-50 W (tray_budget.py)"),
}

# ------------------------------------------------------------------ loads behind the UPS (W, rated / typical while building / held through a power cut)
BACKED = {
    "scan PC with RTC6": (200, 80, 0, "estimate (tray_budget.py); shut down 120 s into a power cut"),
    "galvo +/-15 V supply": (90, 30, 0, "estimate (tray_budget.py); off with the PC"),
    "48 V servo bus (2 ClearPath-SD)": (300, 30, 0, "estimate; disabled 60 s into a power cut"),
    "stepper drive + NEMA 17": (40, 10, 0, "estimate: 1.7 A class motor on 24 V"),
    "PLC + I/O modules": (12, 8, 8, "estimate: Productivity1000 CPU and five modules"),
    "safety controller + guard lock + lamps": (25, 15, 12, "estimate: SC26 ~4 W, lock solenoid ~6 W, two 22 mm lamps"),
    "O2 analyser": (20, 15, 15, "Ntron Microx class: zirconia cell heater (estimate)"),
    "dew-point + pressure transmitters + flow switch": (6, 4, 4, "estimate"),
    "argon NC solenoids (2, held)": (16, 8, 0, "estimate: closed (de-energised) after the cut"),
    "pneumatic valve manifold": (4, 1, 0, "estimate"),
    "Pi 5 + cameras + NFC + load cell": (20, 12, 8, "estimate (tray_budget.py ctrl line)"),
    "Ethernet switch": (6, 4, 4, "estimate"),
    "fans (module + drawer)": (8, 6, 3, "estimate"),
    "fibre amplifier + 4 proximity sensors": (4, 3, 3, "estimate"),
    "24 V / 48 V supply losses": (40, 15, 6, "estimate: ~88-92 % efficient DIN supplies"),
}

# ------------------------------------------------------------------ the UPS battery (Eaton 5PX1500RTG2 class)
UPS = dict(n=4, v=12.0, ah=9.0, k_peukert=1.15, inverter_eff=0.88, rated_w=1440.0,
           source="battery 4 x 12 V 9 Ah assumed for the 5PX 1500 G2 class (not read from Eaton's datasheet: its page timed out); Peukert k 1.15 for VRLA; inverter 88 % (byu-vcl PR 318's Vertiv figure)")

# ------------------------------------------------------------------ the 3U DIN drawer (cad/lpbf_low.py: 446.6 x 530 x 131 mm box)
DRAWER = dict(w=0.4466, d=0.530, h=0.131)
DRAWER_HEAT = {   # W dissipated inside the drawer, building (typical) / worst
    "24 V control supply losses (SDR-240-24 class at ~40 %)": (8, 14),
    "48 V servo supply losses": (4, 20),
    "heater supply losses (LRS-350-24 at 97 / 250 W)": (12, 31),
    "heater SSR (D1D20: ~1.3 V at 10.4 A worst, estimate)": (5, 14),
    "contactors K1, K3A, K3B, K4, K5 coils": (6, 9),
    "PLC + modules": (8, 12),
    "safety controller": (4, 5),
    "ClearCore": (4, 6),
    "stepper drive": (4, 10),
    "Pi 5 + DC-DC": (8, 12),
    "Ethernet switch": (3, 4),
    "CN708 + 2nd temperature relay": (3, 4),
    "terminal blocks, fuses, wiring (I^2 R)": (3, 6),
}
T_LIMITS = {"Banner SC26 (operating)": 55.0, "Productivity1000 PLC": 60.0, "Mean Well SDR (full load without derating)": 50.0,
            "Raspberry Pi 5 (throttles near)": 80.0}
AMBIENT = {"room 22 C": 22.0, "Shuttle, typical build, Shuttle 1 idle (heat.md)": 30.0,
           "Shuttle, worst (PR 318 busy case + this tray at 500 W)": 43.0}

# ------------------------------------------------------------------ cable runs (one way, m) measured on the model + 20 % and loops
RUNS = {   # name: (length m, current A, volts, conductor mm^2 [AWG], note)
    "dock -> PB1 (gas module) feeder": (0.8, 24.0, 208.0, 5.26, "10 AWG; at the full 24 A continuous"),
    "PB1 -> rack, laser 208 V": (2.4, 9.1, 208.0, 2.08, "14 AWG along the back duct"),
    "PB1 -> rack, UPS 120 V": (2.4, 7.4, 120.0, 2.08, "14 AWG"),
    "PB1 -> pump 120 V": (0.6, 7.0, 120.0, 2.08, "14 AWG"),
    "heater 24 V: drawer -> rod end (L75, 10.4 A)": (1.7, 10.4, 24.0, 1.31, "16 AWG pair incl. a 0.3 m service loop for the 50 mm stroke"),
    "heater 24 V with 18 AWG": (1.7, 10.4, 24.0, 0.823, "18 AWG for comparison"),
    "48 V servo bus: drawer -> Z servo (peak 5 A)": (1.6, 5.0, 48.0, 0.823, "18 AWG (Teknic DC power cable class)"),
    "24 V: drawer -> guard lock (0.5 A hold, 1 A pull-in)": (1.6, 1.0, 24.0, 0.326, "22 AWG"),
    "24 V: drawer -> gas module valves + O2 (2 A)": (2.3, 2.0, 24.0, 0.519, "20 AWG"),
    "+/-15 V: rack -> galvo (3 A peak per rail, estimate)": (1.3, 3.0, 15.0, 0.823, "18 AWG; better: the supply beside the head"),
}
RHO_CU = 0.0172e-6 * 1.2       # ohm m at ~60 C conductor

# ------------------------------------------------------------------ hermetic heater pins
PIN = dict(d_mm=1.02, l_mm=25.0, rho_ohm_m=0.43e-6,
           source="Accu-Glass Sub-C pins are Au-plated Ni-Fe, 0.040 in. (1.02 mm); Ni-Fe (alloy 52 class) resistivity ~0.43 uOhm m (estimate from the alloy); 25 mm conducting length assumed")


def leg_currents(phase):
    """phase: dict load -> W (real). Returns L1, L2, N currents (A, magnitudes added: conservative)."""
    L1 = L2 = N = 0.0
    for name, w in phase.items():
        br, conn, rated, pf, typ, *_ = AC[name]
        if conn == "L1-L2":
            i = w / (V_LL * pf)
            L1 += i
            L2 += i
        elif conn == "L1-N":
            i = w / (V_LN * pf)
            L1 += i
            N += i
        else:
            i = w / (V_LN * pf)
            L2 += i
            N -= i
    return L1, L2, abs(N)


def main():
    R = {}
    backed_rated = sum(v[0] for v in BACKED.values())
    backed_typ = sum(v[1] for v in BACKED.values())
    backed_hold = sum(v[2] for v in BACKED.values())
    ups_in_rated = backed_rated / UPS["inverter_eff"] + 100.0
    ups_in_typ = backed_typ / UPS["inverter_eff"] + 30.0
    phases = {
        "purge (pump on, heaters preheating)": {"pump": AC["pump"][2], "UPS input": ups_in_typ, "heater supply": AC["heater supply"][2], "blower": 50.0, "laser": 150.0},
        "building, typical": {"laser": AC["laser"][4], "UPS input": ups_in_typ, "heater supply": AC["heater supply"][4], "blower": 50.0},
        "building, worst (500 W CW, blower at its AC upper bound, UPS recharging)": {"laser": 1700.0, "UPS input": ups_in_rated, "heater supply": AC["heater supply"][2], "blower": 230.0},
        "everything at rated at once (pump interlocked off while lasing, so not a real state)": {"laser": 1700.0, "UPS input": ups_in_rated, "heater supply": AC["heater supply"][2], "blower": 230.0, "pump": AC["pump"][2]},
    }
    R["legs"] = {}
    for ph, loads in phases.items():
        L1, L2, N = leg_currents(loads)
        R["legs"][ph] = dict(L1=L1, L2=L2, N=N, total_W=sum(loads.values()), ok=max(L1, L2) <= DOCK_CONT_A)
    # inrush against breakers: UL 489 curves, magnetic trip band (multiples of In): B 3-5, C 5-10, D 10-20
    curves = {"B": (3, 5), "C": (5, 10), "D": (10, 20)}
    branch = {"laser": ("D", 15), "UPS input": ("D", 15), "heater supply": ("D", 15), "pump": ("C", 15), "blower": ("C", 6)}
    R["inrush"] = {}
    for name, (curve, In) in branch.items():
        pk, dur = AC[name][5], AC[name][6]
        lo, hi = curves[curve]
        for alt in ("B", "C", "D"):
            pass
        R["inrush"][name] = dict(breaker=f"{AC[name][0].split()[0]} {curve}{In}", peak_A=pk, duration_s=dur,
                                 magnetic_trip_min_A=lo * In, margin=lo * In / pk,
                                 with_C_curve_margin=5 * In / pk, with_B_curve_margin=3 * In / pk)
    tot_pk = AC["laser"][5] + AC["UPS input"][5] + AC["heater supply"][5]
    R["inrush"]["closing the main disconnect (laser + UPS + heater supply at once)"] = dict(peak_A=tot_pk, upstream="dock 30 A breaker, magnetic trip >= 150 A (C) / 300 A (D)", margin_vs_C=150 / tot_pk)
    # UPS runtime (Peukert)
    E_nom = UPS["n"] * UPS["v"] * UPS["ah"]
    Vb = UPS["n"] * UPS["v"]

    def runtime_min(p_w):
        i = p_w / (UPS["inverter_eff"] * Vb)
        H = 20.0
        C = UPS["ah"]
        t_h = H * (C / (i * H)) ** UPS["k_peukert"]
        return t_h * 60

    seq = []   # power-cut sequence: (from s, to s, load W)
    p_typ = backed_typ
    p_after_servo = p_typ - BACKED["48 V servo bus (2 ClearPath-SD)"][1]
    p_hold = backed_hold
    # energy-based with a load-dependent capacity (fraction of capacity used per second at each load)
    used = 0.0
    t = 0.0
    for t0, t1, p in ((0, 60, p_typ), (60, 120, p_after_servo), (120, 1e9, p_hold)):
        rt = runtime_min(p) * 60
        span = t1 - t0
        if used + span / rt >= 1.0:
            t = t0 + (1.0 - used) * rt
            used = 1.0
            break
        used += span / rt
        t = t1
    R["ups"] = dict(battery_Wh_nominal=E_nom, backed_rated_W=backed_rated, backed_typical_W=backed_typ, held_W=backed_hold,
                    runtime_at_rated_min=runtime_min(backed_rated), runtime_at_typical_min=runtime_min(backed_typ),
                    runtime_hold_only_min=runtime_min(backed_hold), power_cut_total_min=t / 60,
                    cooldown_to_50C_min=dict(S25=15, M50=28, L75=41), ups_rated_W=UPS["rated_w"], source=UPS["source"])
    # drawer heat
    typ = sum(v[0] for v in DRAWER_HEAT.values())
    worst = sum(v[1] for v in DRAWER_HEAT.values())
    w, d, h = DRAWER["w"], DRAWER["d"], DRAWER["h"]
    # free surfaces: front panel and the two sides (top and bottom face the PC and the rack's top: not counted), plus the back
    A_free = w * h + 2 * d * h + w * h
    k_enc = 5.5          # W/m2K, painted sheet steel in still air (IEC TR 60890 class value; PR 318 uses the same)
    dT_nat_typ, dT_nat_worst = typ / (k_enc * A_free), worst / (k_enc * A_free)
    cfm = lambda P, dT: P / (1.2 * 1005 * dT) * 2118.88
    R["drawer"] = dict(heat_typ_W=typ, heat_worst_W=worst, free_area_m2=A_free, rise_natural_typ_K=dT_nat_typ, rise_natural_worst_K=dT_nat_worst,
                       fan_cfm_for_10K_worst=cfm(worst, 10.0), fan_cfm_for_5K_worst=cfm(worst, 5.0),
                       inside_with_fan_10K={k: v + 10 for k, v in AMBIENT.items()}, inside_natural_worst={k: v + dT_nat_worst for k, v in AMBIENT.items()},
                       limits=T_LIMITS, items=DRAWER_HEAT)
    # voltage drop
    R["vdrop"] = {}
    for name, (L, I, V, A_mm2, note) in RUNS.items():
        Rloop = 2 * L * RHO_CU / (A_mm2 * 1e-6)
        dv = I * Rloop
        R["vdrop"][name] = dict(length_m=L, current_A=I, volts=V, mm2=A_mm2, drop_V=dv, drop_pct=100 * dv / V,
                                heater_power_loss_pct=(100 * (1 - (1 - dv / V) ** 2) if "heater" in name else None), note=note)
    # hermetic pins
    A_pin = math.pi / 4 * (PIN["d_mm"] * 1e-3) ** 2
    Rpin = PIN["rho_ohm_m"] * PIN["l_mm"] * 1e-3 / A_pin
    R["pins"] = {f"{n} pin(s) per pole at 10.4 A": dict(ohm_per_pin=Rpin, A_per_pin=10.4 / n, W_per_pin=(10.4 / n) ** 2 * Rpin,
                                                         W_total_both_poles=2 * n * (10.4 / n) ** 2 * Rpin, mV_per_pole=1e3 * (10.4 / n) * Rpin)
                 for n in (1, 2, 3)}
    R["pins"]["source"] = PIN["source"]
    # protective-conductor current (estimates; datasheet values to be read)
    leak = {"laser (EMI filter, estimate)": 3.5, "UPS (estimate)": 1.0, "heater supply LRS-350 (datasheet class < 0.75 mA at 240 V)": 0.75,
            "24 V / 48 V / +/-15 V DIN supplies behind the UPS (3 x 0.5, estimate)": 1.5, "pump motor (estimate)": 0.5, "PC (estimate)": 0.5}
    R["pe_current"] = dict(items=leak, total_mA=sum(leak.values()),
                           note="IEC 60204-1 8.2.8: above 10 mA in the protective conductor, use >= 10 mm2 Cu or a second PE conductor; above 3.5 mA, a plug-connected machine needs a warning and reinforced PE. A 5 mA GFCI upstream would trip.")
    (OUT / "power.json").write_text(json.dumps(R, indent=1, default=float))
    md(R)
    print(json.dumps({k: R[k] for k in ("legs", "ups")}, indent=1, default=float)[:3000])


def md(R):
    L = ["# Power, inrush, UPS, drawer heat, voltage drop and pin heating", "",
         "Generated by [`analysis/electrical/power_budget.py`](../../electrical/power_budget.py); loads, sources and estimates are listed in the script. "
         "It refines [`tray_budget.md`](../tray/tray_budget.md) by device and branch.", "",
         "## 1. Dock legs (208Y/120 V, 30 A breaker, 24 A continuous)", "",
         "| State | Input (W) | L1 (A) | L2 (A) | N (A) | Within 24 A? |", "|---|---|---|---|---|---|"]
    for ph, v in R["legs"].items():
        L.append(f"| {ph} | {v['total_W']:.0f} | {v['L1']:.1f} | {v['L2']:.1f} | {v['N']:.1f} | {'yes' if v['ok'] else '**no**'} |")
    L += ["", "Branch currents are added as magnitudes (power factors differ), so the leg figures lean high. Laser across L1-L2; UPS on L1-N; heater supply, pump and blower on L2-N.", "",
          "## 2. Inrush against the branch breakers (UL 489 DIN; magnetic trip band B 3-5, C 5-10, D 10-20 × In)", "",
          "| Load | Breaker | Inrush peak (A, estimate) | Duration (s) | Lowest magnetic trip (A) | Margin | Margin with a C curve | with a B curve |", "|---|---|---|---|---|---|---|---|"]
    for k, v in R["inrush"].items():
        if "breaker" in v:
            L.append(f"| {k} | {v['breaker']} | {v['peak_A']:.0f} | {v['duration_s']} | {v['magnetic_trip_min_A']:.0f} | {v['margin']:.1f}× | {v['with_C_curve_margin']:.1f}× | {v['with_B_curve_margin']:.1f}× |")
        else:
            L.append(f"| {k} | {v['upstream']} | {v['peak_A']:.0f} | – | 150 | {v['margin_vs_C']:.1f}× | – | – |")
    u = R["ups"]
    L += ["", "## 3. UPS (Eaton 5PX1500RTG2 class, 1,440 W) through a power cut", "",
          f"Backed load: {u['backed_rated_W']:.0f} W rated, {u['backed_typical_W']:.0f} W while building, {u['held_W']:.0f} W held after the PC and servos shut down (safety controller, guard lock, PLC, O2 analyser, Pi, switch). Battery {u['battery_Wh_nominal']:.0f} Wh nominal ({u['source']}).", "",
          "| Case | Runtime (min) |", "|---|---|",
          f"| at the rated backed load | {u['runtime_at_rated_min']:.0f} |",
          f"| at the building load | {u['runtime_at_typical_min']:.0f} |",
          f"| power-cut sequence: building load 60 s, servos off, PC off at 120 s, then the held load | **{u['power_cut_total_min']:.0f}** |",
          f"| cool-down of the plate to 50 °C (thermal.md): S25 / M50 / L75 | {u['cooldown_to_50C_min']['S25']} / {u['cooldown_to_50C_min']['M50']} / {u['cooldown_to_50C_min']['L75']} |", "",
          "## 4. Heat in the 3U DIN drawer", "",
          f"{R['drawer']['heat_typ_W']:.0f} W while building, {R['drawer']['heat_worst_W']:.0f} W worst. Free surface (front, back, two sides; top and bottom face the PC and the rack top) {R['drawer']['free_area_m2']:.3f} m² at 5.5 W/m²K: "
          f"**{R['drawer']['rise_natural_typ_K']:.0f} K / {R['drawer']['rise_natural_worst_K']:.0f} K above the air around it with no fan**. A fan moving {R['drawer']['fan_cfm_for_10K_worst']:.0f} CFM holds the worst case to a 10 K rise ({R['drawer']['fan_cfm_for_5K_worst']:.0f} CFM for 5 K).", "",
          "| Ambient | Inside, no fan, worst (°C) | Inside, fan at 10 K rise (°C) |", "|---|---|---|"]
    for k in R["drawer"]["inside_with_fan_10K"]:
        L.append(f"| {k} | {R['drawer']['inside_natural_worst'][k]:.0f} | {R['drawer']['inside_with_fan_10K'][k]:.0f} |")
    L += ["", "Limits: " + "; ".join(f"{k} {v:.0f} °C" for k, v in R["drawer"]["limits"].items()) + ".", "",
          "| Item | Building (W) | Worst (W) |", "|---|---|---|"]
    for k, (a, b) in R["drawer"]["items"].items():
        L.append(f"| {k} | {a} | {b} |")
    L += ["", "## 5. Voltage drop over the cable runs (copper at ~60 °C, both conductors)", "",
          "| Run | Length one way (m) | Current (A) | Conductor (mm²) | Drop (V) | Drop (%) | Heater power lost (%) | Note |", "|---|---|---|---|---|---|---|---|"]
    for k, v in R["vdrop"].items():
        hp = f"{v['heater_power_loss_pct']:.1f}" if v["heater_power_loss_pct"] is not None else "–"
        L.append(f"| {k} | {v['length_m']} | {v['current_A']} | {v['mm2']} | {v['drop_V']:.2f} | {v['drop_pct']:.1f} | {hp} | {v['note']} |")
    L += ["", "## 6. Heater current through hermetic Ni-Fe pins (no convection in vacuum)", "",
          "| Pins per pole | A per pin | W per pin | W in the feedthrough (both poles) | mV per pole |", "|---|---|---|---|---|"]
    for k, v in R["pins"].items():
        if k == "source":
            continue
        L.append(f"| {k} | {v['A_per_pin']:.1f} | {v['W_per_pin']:.2f} | {v['W_total_both_poles']:.2f} | {v['mV_per_pole']:.0f} |")
    L += ["", R["pins"]["source"], "", "## 7. Protective-conductor (earth leakage) current", "",
          "| Source | mA (estimate) |", "|---|---|"]
    for k, v in R["pe_current"]["items"].items():
        L.append(f"| {k} | {v} |")
    L += [f"| **total** | **{R['pe_current']['total_mA']:.1f}** |", "", R["pe_current"]["note"]]
    (OUT / "power.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
