# Heat: the laser's heat in the build module, and the machine's heat in the VLM

Written 2026-11-20 for [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), as part of
the request for "heat transfer theory and simulations ... to help catch issues and enhance performance before we buy and
build". Two heat paths had not been checked before. Both change what to buy. Nothing here has been built or measured.

| File | What it is |
|---|---|
| [`analysis/thermal_laser.py`](analysis/thermal_laser.py) | CalculiX, axisymmetric: the module thermal model of [`thermal_module.py`](analysis/thermal_module.py) with the beam's time-averaged absorbed power added in the plate; 36 runs plus 18 with the module cooled → [`laser_heat.md`](analysis/out/thermal/laser_heat.md) |
| [`analysis/tray/tray_budget.py`](analysis/tray/tray_budget.py) | the tray's electrical input and heat, phase by phase, against the VLM dock and the Shuttle's enclosure, using byu-vcl PR 318's method and numbers → [`tray_budget.md`](analysis/out/tray/tray_budget.md) |
| [`edison/followup-laser-heat/`](edison/followup-laser-heat/) | Edison `LITERATURE_HIGH` second opinion on both questions (§3) |

## 1. The laser heats the build module more than its heaters do

The heater sizing in [`modules.md`](modules.md) and [`analysis/out/thermal/thermal.md`](analysis/out/thermal/thermal.md)
was done with the laser off. At 200 °C a module loses only 30–97 W, mostly through the plate's radial gap into the bore
wall and the chamber floor. During a build, the beam's absorbed power reaches the plate through the part, and averaged
over a layer cycle it is the same size:

| Module | Loss at 200 °C, laser off (start / end of stroke) | Absorbed laser power, sparse layout (25 % of the plate scanned per layer) | Dense layout (70 %) | Dense, keyhole absorptance |
|---|---|---|---|---|
| S25 | 44 / 30 W | 16 W | 35 W | 46 W |
| M50 | 72 / 52 W | 45 W | 81 W | 108 W |
| L75 | 97 / 71 W | 73 W | 111 W | 148 W |

(AlSi10Mg at 350 W, 1300 mm/s, 0.13 mm hatch, absorptance 0.45 or 0.6 in keyhole mode, 0.2 s of jumps per layer, an
8 s recoat cycle.)

**When the laser brings more than the module loses, the heater switches off and the plate drifts up.** Nothing in the
module can take heat away. With the module as drawn:
- a dense M50 build reaches **290 °C** at the end of the stroke, with the Z-coupling magnet face at **85 °C** (NdFeB is
  rated to 80 °C) and the rod-gland O-rings at **155 °C** (150 °C preferred for FKM);
- a dense L75 build reaches **286 °C**, magnet 82 °C, rod gland 149 °C;
- even a dense S25 build passes 200 °C at the end of the stroke (231 °C);
- the heater block's 240 °C cutoff trips first (from 37 / 64 / 88 W absorbed at the end of the stroke), but it only
  opens a heater circuit that is already off, so **it protects nothing here**. If it is a one-shot fuse, it then has to
  be replaced before the next build;
- the hot plate-to-bore clearance stays at 45 µm or more at the dense loads. It closes (the plate seizes) only from
  ~104 W absorbed on S25 and ~127 W on M50 (not within 150 W on L75), which a keyhole-mode dense M50 build (108 W)
  approaches.

The densest layout that keeps the plate at 200 °C at the end of the stroke is **57 % of the plate area per layer on
S25, 31 % on M50 and 24 % on L75** (38 / 20 / 15 % in keyhole mode). Bigger plates are worse, because the laser heat
grows with the scanned area while the losses grow with the perimeter.

**What it changes for Al screening:** the preheat temperature is a screening variable, and the plate would no longer
be at the temperature in the recipe. AlSi10Mg and Al-Mg-Sc-Zr age in place above ~200 °C, and Mg and Zn evaporate faster
as the bed heats ([`preheat-and-plates.md`](preheat-and-plates.md) §3).

### The fix: take heat out of the module under the floor

Same model, with the module's outside below the floor (tube, flange, gland plate, rod) cooled harder
([`laser_heat.md`](analysis/out/thermal/laser_heat.md), last table):

| Cooling under the floor | Heater needed at laser off, end of stroke (S25 / M50 / L75; installed 100 / 150 / 250 W) | Dense build, end of stroke: plate | Rod gland | Magnet face | Hot plate clearance |
|---|---|---|---|---|---|
| natural convection (as drawn) | 30 / 52 / 71 W | 231 / 290 / 286 °C | 117 / 155 / 149 °C | 68 / 85 / 82 °C | ≥ 48 µm |
| a small fan blowing on the module (h ≈ 40 W/m²K) | 37 / 65 / 88 W | 200 / 244 / 242 °C | 56 / 74 / 72 °C | 28–29 °C | ≥ 56 µm |
| water-cooled jacket on the tube (30 °C, h ≈ 300 W/m²K) | 48 / 80 / 107 W | 200 / 206 / 207 °C | 39–45 °C | 30 °C | ≥ 57 µm |

- **A fan under the chamber floor is the cheap first step.** It fixes the magnet and the rod gland in every case, and
  the installed heaters still have 2.0–2.8× margin with it running (1.9–2.3× with the water jacket). The plate still drifts to ~240 °C in dense M50 and
  L75 builds at the end of the stroke.
- **A water-cooled sleeve holds the plate within ~7 K of 200 °C** at the end of the stroke, with the heaters still
  inside their rating. The module drops out through the floor at a swap, so the sleeve has to be fixed under the floor
  port and the module slides into it. Through a 0.5 mm air gap a fixed sleeve only reaches h ≈ 50 W/m²K, the fan case;
  reaching the water-jacket case needs a contact sleeve (a split clamp or a spring band) or water to the module itself.
- **At the start of the stroke cooling below the floor barely helps** (dense M50 and L75: 216–223 °C in every case),
  because the plate sits in the spigot and its heat goes into the floor. That is +16–23 K for the first few millimetres.
- **Whatever cools the module, the controls need three changes:**
  1. log the plate thermocouple per layer as a screening variable, not the set point;
  2. add a plate over-temperature trip that drops **laser enable**, not just the heaters (for example the CN708 limit
     relay into the safety relay's laser-enable chain at ~230 °C);
  3. let the scan software insert a dwell when the plate passes the set point by more than a few kelvin.
- **Swap the NdFeB pot magnet for SmCo** (or the switched coupling of [`hot-swap.md`](hot-swap.md)) whatever else is
  done. It already had only 11 °C of margin with the laser off.

## 2. The machine's heat in the VLM

byu-vcl PR 318 runs trays while they are stored in the Kardex Shuttle, powered through the dock. Everything this tray
draws ends up as heat inside the Shuttle unless chilled water or a duct carries it out.

| Phase | Tray input | Unventilated Shuttle rise: this tray alone / with Shuttle 1 idling / with PR 318's busy case |
|---|---|---|
| standby | 0.2 kW | 0.7 / 5.0 / 12.8 K |
| purge (pump on) | 1.0 kW | 3.3 / 7.6 / 15.4 K |
| building, typical (350 W, beam on 60 %) | 1.2 kW | 4.0 / 8.3 / 16.1 K |
| building, worst (500 W continuous) | 2.7 kW | 8.7 / 13.0 / 20.8 K |

- **The quoted IPG YLR-500-U3-SM-AC is forced-air cooled and rated for 10–35 °C ambient.** In a 22 °C room the
  Shuttle's air would average about 30 °C during a typical build with the rest of Shuttle 1 idling, and 38–43 °C with
  PR 318's busy case. Those are averages: the laser's front-panel fans could also breathe the hot air it has just
  exhausted, in a 695 mm slot with the lift shaft in front of it.
- **While it builds, this tray would be the biggest heat source in its Shuttle:** 1.2–2.7 kW against 1.3 kW for all six
  trays of Shuttle 1 idling.
- **Decide before ordering the laser** (10–12 weeks): either
  1. a water-cooled YLR-500 on the dock's chilled water (the shared ThermoFlex 900 is a 900 W unit, too small for a
     500 W fibre laser's ~1.2 kW loss: size the chiller for it); or
  2. the air-cooled unit with its exhaust ducted out of the Shuttle through a ventilated dock (PR 318 already lists
     "can a column be ventilated?" as a question for Kardex); or
  3. build only at the access opening, which ties the opening up for hours per build.
- **Electrically it fits one dock.** The worst coincident case puts 13.6 A on a leg against 24 A continuous on the dock's
  30 A breaker. The laser takes 208 V across L1–L2 (IPG: 200–240 V). The pump runs only while purging.
- **UPS:** the backed branch (PC, scan head, servo drives, O₂ and dew-point, safety and controls) is about 0.7 kW
  rated, inside PR 318's Vertiv GXT5LI-1500 (1.35 kW, online). The laser, pump, blower and heaters stay unbacked, as
  PR 318 does for heaters and pumps.

## 3. What Edison's second opinion adds

Edison `LITERATURE_HIGH`, task `410abc9e…` (submitted 14:33 UTC, fetched 15:05 UTC), ~45k characters, is in
[`edison/followup-laser-heat/answer.md`](edison/followup-laser-heat/answer.md) with its references and the full
trajectory. It agrees with both findings and adds numbers:

- **Interlayer time is the strongest lever.** On a 100 °C platform, 316L cuboids reached ~545 °C at an 18 s interlayer
  time, ~230 °C at 65 s and ~170 °C at 116 s ([Chaudry et al. 2022](https://doi.org/10.1007/s40964-022-00282-x)). So the
  scan software's dwell (fix 3 above) is a real control, not a fallback; a ~28–30 s recoat dwell was enough to stop
  cross-layer accumulation on an EOS machine ([Bugatti and Colosimo 2024](https://doi.org/10.1016/j.jmapro.2024.06.050)).
- **Drift costs properties in the alloys we screen.** AlSi10Mg on a 200 °C platform is already over-aged after ~10 h
  of building (100.5 ± 3 HV) and falls below 80 HV at 250 °C ([Bosio et al. 2021](https://doi.org/10.1007/s11837-020-04523-8));
  200 °C AlSi10Mg is weaker than 35 °C material, with a coarser Si network
  ([Macías et al. 2020](https://doi.org/10.1016/j.actamat.2020.10.001)); A357 regions that ran above ~230 °C lost up to
  30 % of their properties ([Heugue et al. 2026](https://doi.org/10.3390/met16080854)). Edison's conclusion is that
  holding the plate within about ±10 °C of the set point is a metallurgical requirement, not a nicety.
- **Zn and Mg loss in 7075 doesn't depend on the plate temperature** (~1 wt% Zn and ~0.3 wt% Mg from 25 to 400 °C,
  [Velikajne et al. 2026](https://doi.org/10.3390/ma19050970)): it is set in the melt pool.
- **Magnet:** NdFeB's practical limit is 80–180 °C depending on grade; conventional SmCo is rated to ~300 °C, at about
  30–40 % less holding force for the same size ([Liu 2019](https://doi.org/10.1088/1674-1056/28/1/017501)). Swap to SmCo.
- **FKM:** 200 °C continuous, ~230 °C short excursions. The rod gland stays well inside that once the module is cooled.
- **Air-cooled laser:** the quoted unit's 1.7 kW in, 0.5 kW out implies ~29 % wall-plug efficiency and ~1.2 kW of heat;
  Edison found no published derating data for air-cooled LPBF-class lasers in enclosures, and calls forced exhaust
  "effectively mandatory" or water cooling the alternative ([Ballato et al. 2024](https://doi.org/10.1088/1361-6463/ad1ddc)).
- **What it couldn't find:** published details of how commercial machines take heat out of the build cylinder. The
  literature only says the platform is the main heat sink.

## 4. Caveats

- The laser loads are time averages from scan rate, layout density and recoat time. The absorptance (0.45, 0.6 in
  keyhole) and the 8 s recoat cycle are assumptions; a slower recoat or a dwell lowers the average.
- The heat is put in the plate, as if the part conducted all of it down. Early in a build that is close; with a tall,
  thin part some of it leaves through the cake top instead, so the end-of-stroke figures lean high.
- The cooled cases change only the module's outside below the floor; the chamber floor edge stays at 25 °C as before.
- The tray budget's laser model (150 W ready, 32 % wall-plug at full power) is fitted to IPG's one published draw.
  The galvo, PC, servo and instrument draws are estimates and are marked so in the script.
- The Shuttle rise uses PR 318's still-air figure (5.5 W/m²K over 55.9 m²). Kardex has not published the interior
  temperature its drives allow or how much heat a tray may give off.
