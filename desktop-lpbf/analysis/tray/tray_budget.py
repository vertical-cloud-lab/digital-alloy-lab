"""Power and heat budget of the desktop LPBF tray inside the VLM, phase by phase.

Why: the machine is meant to run while its tray is stored in a Kardex Shuttle (byu-vcl PR 318: trays are powered
when stored, through a dock at the back right). Everything the tray draws ends up as heat inside the Shuttle's
enclosure unless chilled water or an exhaust duct carries it out. The quoted laser (IPG YLR-500-U3-SM-AC) is
forced-air cooled and is rated for 10-35 C ambient, and it is a 10-12 week order, so air- vs water-cooling has to be
settled before the PO.

Method (the same as byu-vcl PR 318's services.heat_budget, so the numbers add to its Shuttle budgets):
- each load's rated and typical draw, with its source; which branch it is on (UPS-backed or straight from the dock);
- per build phase, the electrical input of the tray;
- heat into the enclosure = tray input minus what chilled water carries out (for a water-cooled laser);
- the Shuttle's rise with no ventilation = W / (5.5 W/m2K x 55.9 m2), and the airflow that holds a 5 K or 10 K
  rise, W / (rho cp dT) with air at 1.2 kg/m3 and 1005 J/kg K;
- the dock's legs: 208Y/120 V, L1 + L2 + N + PE, 30 A breaker (PR 318), loaded to at most 80 % (24 A) continuous.

Run:  python desktop-lpbf/analysis/tray/tray_budget.py   ->  desktop-lpbf/analysis/out/tray/tray_budget.{md,json}
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "out" / "tray"

# ------------------------------------------------------------------------------------------------ sources
SRC = {
    "ipg": "IPG spec sheet G22-29856 rev. 00 for YLR-500-U3-SM-AC (quotes/ipg-ylr-500-u3-sm-ac.md): 1,500 W typ / "
           "1,700 W max, 1,600 VA typ / 1,900 VA max at 500 W out; 200-240 VAC 1-phase; forced air; 10-35 C ambient",
    "pump": "Edwards nXDS6i A73501983 (bom.csv G2), nXDS instruction manual A73501880 issue I (idealvac.com mirror, sha256 d04f0234..., read 2026-11-23 22:28Z): 100-127 V or 200-240 V +/-10 %, 1-phase 50/60 Hz, auto-sensing inverter drive; continuous rating 10 A rms at 100-127 V, 6 A rms at 200-240 V (Table 8); supply protection 10 A (Table 9); time-lag fuses or breakers, 'current transients can exceed the rated values' (issue B 3.6.1); RCD >= 30 mA 'to avoid trip during start up'; 260 W at ultimate, 170 W standby (Edwards catalogue page, search snippet). Taken at 208 V across L1-L2 at its 6 A rating while purging (power factor 0.6 assumed, so 749 W: a high "
            "side for the heat; the catalogue's 260 W at ultimate is the low side)",
    "blower_hi": "McMaster 9960K51 regenerative blower (mcmaster-parts.csv): 1/8 hp, 115 V; taken as the upper bound",
    "blower_lo": "sealed 24 V brushless blower: ~2.4 L/s (144 L/min, 2.5 m/s through 120 x 8 mm) against ~2 kPa is "
                 "~5 W of gas power; at 10-25 % blower efficiency, 20-50 W (estimate)",
    "heat": "modules.md / analysis/out/thermal: 2 / 3 / 5 x 50 W cartridges (S25 / M50 / L75), worst steady 44 / 72 / "
            "97 W at 200 C; Mean Well LRS-350-24 about 89 % efficient (datasheet)",
    "pc": "2U scan/laser controller PC with an RTC6 card: 80 W typical, 200 W rated (estimate)",
    "galvo": "SCANLAB basiCube 20 on one 24 V rail, <= 2.6 A (SCANLAB basiCube series data, electrical.md section 0 point 4; "
             "it is not +/-15 V), through a Mean Well HDR-100-24 (~90 % efficient): 69 W rated, ~30 W typical (estimate)",
    "servo": "three Teknic ClearPath-SD axes (recoater, Z, metering roller): ~10 W each holding/average, 100 W each "
             "peak (estimate)",
    "gas_inst": "O2 analyzer (zirconia cell heater ~10-20 W), dew-point transmitter (~2 W), pressure transmitters, "
                "two 24 V solenoids (~8 W each when held) (estimates)",
    "ctrl": "Pi 5 + cameras ~15 W, safety relay + guard lock + panel lamps ~15 W, network switch ~10 W, 24 V supply "
            "losses ~15 W (estimates)",
    "ups": "Eaton 5PX1500RTG2 (bom.csv D2, the model's 2U unit, electrical.md 1.2): line-interactive, 1,500 VA / 1,500 W; "
           "ENERGY STAR UPS dataset (data.energystar.gov resource ifxy-2uty, read 2026-11-23 22:48Z): efficiency 98.6 % at "
           "50 % and 75 % load, 98.4 % at 100 %, weighted 98.6 %; battery runtime 14 min at 50 % and 7 min at 100 % load. "
           "No 25 % or no-load figure is listed: 98.6 % at 25 % and a 10 W no-load draw are assumed. The Vertiv "
           "GXT5LI-1500 that byu-vcl PR 318 standardises on (online, 1,350 W, 88.8 % at 25 %, 29.1 W no-load) is D2's alternative",
    "dock": "byu-vcl PR 318 services.py: dock 208Y/120 V, L1, L2, N, PE, 30 A breaker; CombiTac O3 mm contacts 39 A",
    "shuttle": "byu-vcl PR 318 services.heat_budget: Shuttle enclosure 2.83 x 3.12 x 3.95 m, 55.9 m2 of walls and "
               "roof, 5.5 W/m2K for painted sheet steel in still air; Shuttle 1 idle 1,317 W (4.3 K), Shuttle 1 with a "
               "printer and the furnace working 3,720 W (12.1 K)",
    "chiller": "byu-vcl PR 318: the shared chiller is a Thermo Scientific ThermoFlex 900, 900 W at +20 C",
}

# laser model: P_el = P_ready + P_opt / eta, fitted to IPG's 1,700 W max at 500 W out with an assumed 150 W ready draw
LASER_READY_W = 150.0            # emission off, fans and electronics on (estimate: IPG doesn't publish it)
LASER_MAX_W, LASER_MAX_VA, LASER_OUT_W = 1700.0, 1900.0, 500.0
ETA = LASER_OUT_W / (LASER_MAX_W - LASER_READY_W)
PF = LASER_MAX_W / LASER_MAX_VA


def laser_w(p_opt):
    return LASER_READY_W + p_opt / ETA


# typical Al build: 350 W while the beam is on (AlSi10Mg needs 300-400 W at ~75 um), beam on 60 % of each layer's time
AL_POWER, DUTY = 350.0, 0.6

# loads: key -> (rated W, typical W while building, volts, backed?, source key)
LOADS = {
    "laser": (LASER_MAX_W, laser_w(AL_POWER * DUTY), 208, False, "ipg"),
    "pump": (6.0 * 208 * 0.6, 0.0, 208, False, "pump"),   # nXDS6i at 208 V, 6 A rating, pf 0.6 assumed; runs only while purging
    "blower": (230.0, 50.0, 120, False, "blower_hi"),
    "heaters": (250 / 0.89, 97 / 0.89, 120, False, "heat"),
    "pc": (200.0, 80.0, 120, True, "pc"),
    "galvo": (24 * 2.6 / 0.9, 30.0, 120, True, "galvo"),
    "servos": (300.0, 30.0, 120, True, "servo"),
    "gas_instruments": (60.0, 35.0, 120, True, "gas_inst"),
    "controls": (55.0, 55.0, 120, True, "ctrl"),
}

# phases: which loads run, and at what fraction of their typical draw ('rated' takes the rated draw)
PHASES = {
    "standby (docked, nothing running)": {"laser": 0.0, "pc": 1.0, "gas_instruments": 1.0, "controls": 1.0},
    "purge (pump on, 3 cycles, ~10-15 min)": {"pump": "rated", "laser": "ready", "pc": 1.0, "gas_instruments": 1.0,
                                             "controls": 1.0, "blower": 1.0},
    "preheat (heaters at full power, ~15-40 min)": {"heaters": "rated", "laser": "ready", "blower": 1.0, "pc": 1.0,
                                                   "gas_instruments": 1.0, "controls": 1.0},
    "building, typical (Al at 350 W, beam on 60 %)": {"laser": 1.0, "heaters": 1.0, "blower": 1.0, "pc": 1.0,
                                                     "galvo": 1.0, "servos": 1.0, "gas_instruments": 1.0,
                                                     "controls": 1.0},
    "building, worst (500 W, beam on continuously)": {"laser": "rated", "heaters": "rated", "blower": "rated",
                                                     "pc": "rated", "galvo": "rated", "servos": 1.0,
                                                     "gas_instruments": 1.0, "controls": 1.0},
}

UPS_MODEL = "Eaton 5PX1500RTG2"
UPS_IDLE, UPS_W = 10.0, 1500.0                 # no-load draw assumed (ENERGY STAR lists none for this line-interactive unit)
UPS_EFF = [(0.25, 0.986), (0.50, 0.986), (0.75, 0.986), (1.0, 0.984)]   # ENERGY STAR; the 25 % point assumed equal to 50 %


def ups_loss(w):
    pts = [(0.0, UPS_IDLE)] + [(f * UPS_W, f * UPS_W * (1 / e - 1)) for f, e in UPS_EFF]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if w <= x1:
            return y0 + (y1 - y0) * (w - x0) / (x1 - x0)
    return pts[-1][1]


AREA, K_ENCL, RHO_CP = 55.9, 5.5, 1.2 * 1005.0
SHUTTLE1_IDLE, SHUTTLE1_BUSY = 1317.0, 3720.0
ROOM_C = 22.0
# water-cooled variant: share of the laser's own loss that goes to the water (estimate for a water-cooled YLR)
WATER_SHARE = 0.85


def phase_rows(name, spec):
    rows = {}
    for k, f in spec.items():
        rated, typ, v, backed, _ = LOADS[k]
        if k == "laser" and f == "ready":
            w = LASER_READY_W
        elif k == "laser" and f == 0.0:
            w = 0.0
        elif f == "rated":
            w = rated
        else:
            w = typ * f
        rows[k] = dict(w=round(w, 1), volts=v, backed=backed)
    backed_w = sum(r["w"] for r in rows.values() if r["backed"])
    rows["ups loss"] = dict(w=round(ups_loss(backed_w), 1), volts=120, backed=False)
    total = sum(r["w"] for r in rows.values())
    laser = rows.get("laser", {}).get("w", 0.0)
    p_opt = 0.0
    if laser > LASER_READY_W:
        p_opt = (laser - LASER_READY_W) * ETA
    laser_loss = max(laser - p_opt, 0.0)
    heat_air = total                                  # air-cooled: everything ends up in the enclosure
    heat_water_variant = total - WATER_SHARE * laser_loss   # the beam's own power still ends up in the chamber
    # dock currents: laser across L1-L2 at 208 V (VA), 120 V loads split between the legs, largest first
    amps_208 = (laser / PF) / 208.0 if laser else 0.0
    amps_208 += sum(r["w"] / 0.6 / 208.0 for k, r in rows.items() if r["volts"] == 208 and k != "laser")   # the pump (pf 0.6)
    loads120 = sorted(((r["w"] / 0.95) / 120.0 for k, r in rows.items()
                       if r["volts"] == 120 and not r["backed"] and k != "ups loss"), reverse=True)
    ups_in_a = (backed_w + rows["ups loss"]["w"]) / 0.95 / 120.0
    legs = [amps_208, amps_208]
    for a in [ups_in_a] + loads120:
        i = 0 if legs[0] <= legs[1] else 1
        legs[i] += a
    def rise(w):
        return w / (K_ENCL * AREA)
    return dict(
        loads=rows, total_w=round(total), backed_w=round(backed_w), optical_w=round(p_opt),
        heat_to_enclosure_air_cooled_w=round(heat_air),
        heat_to_enclosure_water_cooled_w=round(heat_water_variant),
        shuttle_rise_k_alone=round(rise(heat_air), 1),
        shuttle_rise_k_with_idle_shuttle=round(rise(heat_air + SHUTTLE1_IDLE), 1),
        shuttle_rise_k_with_busy_shuttle=round(rise(heat_air + SHUTTLE1_BUSY), 1),
        shuttle_rise_k_with_busy_shuttle_water_cooled=round(rise(heat_water_variant + SHUTTLE1_BUSY), 1),
        airflow_m3h_for_5k=round(heat_air / (RHO_CP * 5) * 3600),
        airflow_m3h_for_10k=round(heat_air / (RHO_CP * 10) * 3600),
        dock_leg_amps=[round(a, 1) for a in legs],
        dock_ok=max(legs) <= 24.0,
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = {name: phase_rows(name, spec) for name, spec in PHASES.items()}
    ups_backed_rated = sum(LOADS[k][0] for k in LOADS if LOADS[k][3])
    data = dict(
        sources=SRC, laser_model=dict(ready_w=LASER_READY_W, wall_plug_eff=round(ETA, 3), pf=round(PF, 3),
                                      al_power_w=AL_POWER, duty=DUTY),
        ups=dict(model=UPS_MODEL, rated_w=UPS_W, backed_rated_w=ups_backed_rated,
                 fits=ups_backed_rated <= UPS_W),
        phases=res,
        shuttle=dict(area_m2=AREA, k_w_m2k=K_ENCL, room_c=ROOM_C, idle_w=SHUTTLE1_IDLE, busy_w=SHUTTLE1_BUSY),
    )
    (OUT / "tray_budget.json").write_text(json.dumps(data, indent=1))

    L = ["# Power and heat of the LPBF tray in the VLM, by phase", "",
         "Generated by `analysis/tray/tray_budget.py`. Method and sources in the script's docstring and the table at "
         "the end. Estimates are marked as such there.", "",
         f"Laser model: {LASER_READY_W:.0f} W ready + optical / {ETA:.2f} (fitted to IPG's {LASER_MAX_W:.0f} W at "
         f"{LASER_OUT_W:.0f} W out); a typical Al build at {AL_POWER:.0f} W with the beam on {DUTY:.0%} of the time.",
         "", "| Phase | Tray input (W) | Of it UPS-backed (W) | Heat into the Shuttle, air-cooled laser (W) | "
         "Same, water-cooled laser (W) | Shuttle rise, this tray alone (K) | + Shuttle 1 idle (K) | + Shuttle 1 busy (K) "
         "| + busy, water-cooled (K) | Air for a 5 K rise (m³/h) | Dock legs L1 / L2 (A, limit 24) |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, r in res.items():
        L.append(f"| {name} | {r['total_w']} | {r['backed_w']} | {r['heat_to_enclosure_air_cooled_w']} | "
                 f"{r['heat_to_enclosure_water_cooled_w']} | {r['shuttle_rise_k_alone']} | "
                 f"{r['shuttle_rise_k_with_idle_shuttle']} | {r['shuttle_rise_k_with_busy_shuttle']} | "
                 f"{r['shuttle_rise_k_with_busy_shuttle_water_cooled']} | {r['airflow_m3h_for_5k']} | "
                 f"{r['dock_leg_amps'][0]} / {r['dock_leg_amps'][1]}{'' if r['dock_ok'] else ' **over**'} |")
    w = res["building, worst (500 W, beam on continuously)"]
    t = res["building, typical (Al at 350 W, beam on 60 %)"]
    L += ["", "## What it means", "",
          f"- **The laser's ambient limit is the binding one.** IPG rates the unit for 10-35 °C. With no "
          f"ventilation, a typical build alone holds the Shuttle's air {t['shuttle_rise_k_alone']} K above the room "
          f"({ROOM_C + t['shuttle_rise_k_alone']:.0f} °C in a {ROOM_C:.0f} °C room), "
          f"{ROOM_C + t['shuttle_rise_k_with_idle_shuttle']:.0f} °C with the rest of Shuttle 1 idling, and "
          f"{ROOM_C + t['shuttle_rise_k_with_busy_shuttle']:.0f} °C if it shares the Shuttle with PR 318's busy case "
          f"(a printer and the furnace working). The worst case (500 W, beam on continuously) reaches "
          f"{ROOM_C + w['shuttle_rise_k_with_busy_shuttle']:.0f} °C. These are enclosure averages; the laser's own "
          "intake can be hotter if it breathes its exhaust.",
          f"- **This tray would be the largest heat source in its Shuttle while it builds:** "
          f"{t['heat_to_enclosure_air_cooled_w']}-{w['heat_to_enclosure_air_cooled_w']} W against 1,317 W for all six "
          "trays of Shuttle 1 idling.",
          "- **The air-cooled laser recirculates its own exhaust in a 695 mm slot.** Its fans are on the front panel; "
          "with the tray stored, the front faces the lift shaft and the back faces the dock wall. Nothing here models "
          "that air path; it needs the Shuttle's interior air speed from Kardex, or a test.",
          "- **Options, best first:** (1) order the water-cooled YLR-500 and take its heat out through the dock's "
          "chilled-water couplings; the shared ThermoFlex 900 (900 W) is then too small for a 500 W fibre laser's "
          "~1.2 kW loss and needs upsizing or a second chiller; (2) keep the air-cooled unit and duct its exhaust out "
          "of the Shuttle through a ventilated dock (Kardex has to say whether a column can be ventilated: PR 318's "
          "open question); (3) only build at the access opening, which ties up the opening for hours.",
          f"- **Electrically it fits one dock.** The worst coincident case puts {max(w['dock_leg_amps'])} A on a leg "
          "against 24 A continuous on the 30 A breaker; the pump only runs while purging, before the laser fires. The "
          "laser goes across L1-L2 at 208 V, inside IPG's 200-240 V, and so does the nXDS6i pump (200-240 V +/-10 %, 6 A).",
          f"- **UPS:** the backed branch (PC, scan head, servos' logic and drives, O₂ and dew-point, controls) is "
          f"{ups_backed_rated:.0f} W rated, inside the {UPS_MODEL}'s {UPS_W:,.0f} W (ENERGY STAR: 7 min at full load, 14 min at "
          "half). The laser, pump, blower and heaters stay on "
          "the unbacked branch, as PR 318's rule puts heaters and pumps. On a power cut the build stops, the O₂ "
          "logging and the guard lock stay alive, and the chamber holds its argon (valves fail closed).",
          "", "## Sources and estimates", ""]
    for k, v in SRC.items():
        L.append(f"- **{k}:** {v}")
    (OUT / "tray_budget.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:14]))


if __name__ == "__main__":
    main()
