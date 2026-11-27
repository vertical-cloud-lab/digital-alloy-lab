# Monitoring cooling: the cameras, photodiodes and Pis in the laser guard's air (2026-11-27)

Issue #260, PR 281. [`mechanics.md`](mechanics.md) Checks §7 flagged that the monitoring cameras sit in the Shuttle's air, 38–43 °C in
the busy case, at or above a 40 °C rating. This note reads the ratings, models the temperatures, and designs and draws the cooling.
Nothing here is built or measured. Vendor parts are envelopes from listed dimensions; where a size was not read off a drawing, the
part's name says "envelope".

| File | What it is |
|---|---|
| [`cad/monitoring_cooling.py`](../cad/monitoring_cooling.py) | the cooling parts' geometry and `draw()`, which `monitoring_parts._cooling()` calls. The analysis reads the same numbers |
| [`analysis/monitoring/cooling/cooling.py`](../analysis/monitoring/cooling/cooling.py) | the guard's heat balance, the fans against the system's resistance, each device's temperature, the traps' OD → [`cooling.json`](../analysis/out/monitoring/cooling/cooling.json), [`cooling.md`](../analysis/out/monitoring/cooling/cooling.md) |
| [`analysis/monitoring/cooling/trap_mc.py`](../analysis/monitoring/cooling/trap_mc.py) | 1070 nm transmission of the chevron light trap: a 2-D Monte Carlo ray trace with weighted rays |
| [`ratings.csv`](../analysis/out/monitoring/cooling/ratings.csv) | the vendors' operating ranges and dissipations, with URLs and read times |
| [`price_lookups_round3_cooling.csv`](../analysis/out/monitoring/fab/price_lookups_round3_cooling.csv) | the cooling parts' prices and data (fan curves, filter media, foils, reflectance sources), keys CL… |
| [`analysis/interference.py`](../analysis/interference.py) | nine designed contacts added for the cooling parts |

## 0. Short answer

1. **The cameras don't sit in the Shuttle's air. They sit in the guard's air, which is much warmer.** The guard is a closed box of bare
   1.6 mm aluminium (1.62 m² of panels; UA ≈ 3.9 W/K to the Shuttle by natural convection and the little a bare sheet radiates). Inside
   it, 100–190 W is released besides the chamber's own heat: the galvo (30–69 W), two servos, PB2, the Chronos (20–40 W), the
   photodiodes and the beam path's absorbers. **As drawn, the guard's air runs 26–44 K above the Shuttle's: 58 °C in the typical case,
   64 °C in the busy one, 86 °C in the worst one.** That is a lower bound: once the air passes the chamber's 60 °C wall the model
   counts nothing from the chamber, whose input in a typical build is ~300 W. Every camera, both photodiodes, the LED, the lenses,
   PB2's Pi and the galvo are over their ratings in every case (§3).
2. **Ratings, read on the vendors' pages today (§1):** Chronos 2.1-HD −20 to +40 °C, with its own variable-speed fan; Alvium 1800 U-030
   VSWIR −20 to +55 °C *housing*; Pi Global Shutter and HQ cameras 0–50 °C; Pi 5 0–70 °C, its SoC throttling from 80 °C; PDA36A2
   10–40 °C; the 850 nm LEDs 0–40 °C; PreAmp One −40 to +65 °C; Kowa LM50JC10M −10 to +50 °C. InnoMaker publishes no temperature or
   power for its IMX296 board. **The tightest rating in the guard is not a camera's: the basiCube 20 galvo is rated 25 ± 10 °C.**
3. **Drawn (§4):** a light-trapped inlet low in the back panel's left half, with a filter pad outside; a light-trapped exhaust in its
   right half, with two 120 mm 24 V fans (Delta AFB1224SH) on a plenum outside. They move **118 m³/h at 64 Pa** (§6). Part of the
   inlet air is ducted by a 60 mm fan over the side camera and down into a hood round its body. G-10 breaks go under the side camera
   bracket's root, which bolts to the chamber's floor plate, and into the LP camera's filter holder, which screws onto the boss on the
   60 °C lid. PB2 gets a 40 mm fan and the Pi its Active Cooler. The LP camera's Pi, which had no place in the model, is drawn in a
   fanless heat-sink case on the bridge. **The guard's air then sits 5–10 K above the air it is fed:** 5–6 K on the Shuttle's air,
   7–10 K on cooler air from the dock, which also takes in the warm Shuttle's heat through the panels.
4. **Fed from the Shuttle, that is enough in the typical case and not in the busy one.** At 30.2 °C the guard is at 35.6 °C: everything
   is in rating, with the galvo at its limit (35.6 against 35). At 38.0 °C the guard is at 42.7 °C: the photodiodes, the LED, the
   galvo and the coaxial camera's board are over, and the Chronos, in its hood, is at 38.5 against 40. **So the cameras need the
   laser's answer (heat.md §2): air from outside the Shuttle, or chilled water.** Room air through a ventilated dock keeps everything
   in rating in the typical and busy cases (guard 28.7–29.3 °C). A chilled-water fan coil in the closed guard (not drawn) does nearly
   as well (33.6–34.5 °C), with the galvo close to its limit. Whichever is chosen for the laser should be sized for the guard too.
5. **The worst case (500 W continuous) still has one over, even with room air:** the coaxial camera's board, at 51.8 against 50 °C. The
   galvo heats the optics bridge 20 K above the guard's air, and the cage stands on posts on the bridge.
6. **The light traps meet the Class 1 requirement (OD 5.4) with black anodise; OD 7, the margin, needs hard black anodise or a foil
   lining.** Each trap is a stack of 1 mm blades bent to six legs,
   32 mm deep at a 10 mm pitch, with no straight line through it. For black hard anodise (11–20 % at 1 µm, NASA TP-3595) the trace
   gives OD 7.0–8.1 for the worst collimated beam and 7.9–9.2 for diffuse light, against **OD 5.4 needed** (safety.md §4.2, a direct
   500 W beam). Dyed black anodise (~29 % above 700 nm, Anoplate's chart) gives 6.1. Any finish under ~0.38 meets 5.4. Lining the
   blades with Thorlabs BKF12 foil (5.5 %) gives ~10. Thorlabs' black flocked paper, which is 66 % at 1 µm, would give only 3.5.
7. **Heat budget (heat.md §2):** fans that blow the guard's air into the Shuttle only move heat about inside it, plus their own 17 W.
   Ducting the supply and exhaust through a ventilated dock takes 250–360 W out of the Shuttle (−0.8 to −1.1 K) for 118 m³/h of room
   air. The fan coil puts 200–290 W on the chiller.
8. **Cost:** $700–1,280 for the drawn cooling (BOM M0-C1 to M0-C8 and M7-C1 to M7-C4). Of that, $480–1,060 is the sheet metal and
   traps, which are estimates (§8).
9. **The model:** 330 parts, 55 of them monitoring (was 318 and 43), ~4.2 kg more on the tray (the two traps are 2.4 kg of it). The
   height is unchanged at 579.6 mm and so is the x envelope. Interference: see §4.1.

## 1. Ratings

Read 2026-11-27 08:25–08:35 UTC through the lab tunnel; the URLs and the exact wording are in [`ratings.csv`](../analysis/out/monitoring/cooling/ratings.csv).

| Device | Where | Operating range (°C) | Ambient or case | Dissipation | Source |
|---|---|---|---|---|---|
| Kron Chronos 2.1-HD | side camera at LW | −20 to +40 | not stated (reads as ambient) | 40 W input rating (19 V, 40 W adapter); typical not published. Active cooling, variable-speed fan; the manual gives a sensor at 40–55 °C in a room | [krontech.ca](https://www.krontech.ca/product/chronos-2-1-hd-high-speed-camera/) and the 2.1-HD datasheet |
| Allied Vision Alvium 1800 U-030 VSWIR | route B, coaxial camera arm | −20 to +55 | **housing** | 2.0 W (USB), 2.2 W (5 V) | [alliedvision.com](https://www.alliedvision.com/en/products/area-scan-cameras/alvium/alvium-u/view/1243) |
| InnoMaker CAM-IMX296RAW | LP camera, coaxial camera | **not published** | – | not published (3.3 / 1.8 / 1.2 V rails) | [inno-maker.com](https://www.inno-maker.com/product/cam-mipi296raw-trigger/), user manual V2.02 |
| Raspberry Pi Global Shutter Camera (same IMX296) | the IMX296 boards' stand-in rating | 0 to 50, dry | ambient | not published | [product brief](https://datasheets.raspberrypi.com/gs-camera/gs-camera-product-brief.pdf) |
| Raspberry Pi HQ Camera | layer camera (existing) | 0 to 50, dry | ambient | – | [product brief](https://datasheets.raspberrypi.com/hq-camera/hq-camera-product-brief.pdf) |
| Raspberry Pi 5 | PB2; the LP camera's Pi | 0 to 70 | ambient; the SoC throttles from 80 °C, both CPU and GPU at 85 °C | ~4 W bare board active; PB2 8–12 W with its boards ([`power.md`](../analysis/out/electrical/power.md) §4) | [product brief](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-product-brief.pdf), Raspberry Pi documentation |
| Raspberry Pi Active Cooler | PB2's Pi | not published | – | fan steps at 50, 60, 67.5, 75 °C | [product brief](https://datasheets.raspberrypi.com/cooling/raspberry-pi-active-cooler-product-brief.pdf) |
| Raspberry Pi Pico 2 | trigger generator in PB2 | −20 to +85 (70 ambient) | – | mW | [datasheet](https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf) |
| Thorlabs PDA36A2 | coaxial photodiodes A and B | 10 to 40 | not stated | "actual usage < 5 W" each | [thorlabs.com](https://www.thorlabs.com/item/PDA36A2), manual rev D |
| Thorlabs M850LP1 (the M850L3 is discontinued) | BW light | 0 to 40, non-condensing | ambient; its casing runs up to 25 K above it | 5.1 W at 1.5 A | [thorlabs.com](https://www.thorlabs.com/item/M850LP1) |
| Thorlabs SOLIS-850C | optics.md's light through LP | 0 to 40 | housing ≤ 60 °C | 13.8 W | [thorlabs.com](https://www.thorlabs.com/item/SOLIS-850C) |
| MISTRAS PreAmp One, 28 V | AE preamp | −40 to +65 | not stated | < 1.0 W quiescent, < 2.1 W max | [mistrasgroup.com](https://www.mistrasgroup.com/products/acoustic-emission/preamplifiers/preamp-one-acoustic-emission-ae-pre-amplifier/) |
| Vallen AEP5 | AE preamp, alternative | −20 to +85 | not stated | 1.8 W | [vallen.de](https://www.vallen.de/sensors/preamplifiers/) |
| Omron E3NX-FA | in PB2 | −25 to +55 (one or two side by side) | ambient | ≤ 1 W | [omron.com](https://automation.omron.com/en/us/products/family/E3NX-FA) |
| Mean Well DDR-30G-5 | in PB2 | −40 to +85; full load to 60 °C | ambient | 85 % efficient | [meanwell.com](https://www.meanwell.com/Upload/PDF/DDR-30/DDR-30-SPEC.PDF) |
| Kowa LM50JC10M | side and LP lenses | −10 to +50 | – | – | [kowa-lenses.com](https://www.kowa-lenses.com/en/lm50jc10m-10mp-industrial-lens-c-mount) |
| SCANLAB basiCube 20 (context) | galvo on the bridge | **25 ± 10** | – | 24 V × ≤ 2.6 A; "air cooling: no" | [scanlab.de](https://www.scanlab.de/en/products/scan-systems/basicube/basicube-20) |

- **Ambient or case.** Only Allied Vision says *housing*. The others' ranges read as ambient, which here means the air round the part.
  For boards bolted to something warmer than that air (the LP camera on its boss, the coaxial camera and the Alvium on the bridge), §3
  checks the board's own temperature against the range.
- **The InnoMaker board has no rating,** so the Pi Global Shutter Camera's 0–50 °C, the same sensor on a similar board, stands in for it.
  Ask InnoMaker, or measure the board's temperature on the bench at 45 °C.
- **PB1 holds no Pi.** It is the power box beside the rack, outside the guard, and electrical.md already gives it a 27 CFM filter fan.
  The Pis are PB2's, on the bridge, and the LP camera's second Pi, which this round places beside it (§4).

## 2. The guard's air

`cooling.py` balances the guard as one well-mixed volume of air:

- **In:** the devices (galvo 30 / 69 W typical / worst, Z and recoater servos 20 W, dosing stepper 5–10 W, PB2 8–12 W, the LP camera's
  Pi 5–8 W, the Chronos 20–40 W, the two IMX296 boards 1.5–2 W, two PDA36A2 4–10 W, the LED 1–5 W, the AE preamp 1–2 W, the layer
  camera 1 W, and 5–12 W in the beam path). Most of these are the tray budget's or electrical's estimates; the camera numbers are the vendors' ratings, or half of them
  where only a rating is published. Then there is **the chamber's outside**, taken at **60 °C**, thermal.json's hot-chamber bound. It
  gives up its heat by natural or mixed convection over 0.27 m², radiates from bare 6061 (ε 0.1), and conducts down the four legs
  into the base plate. That comes to 40–130 W with the guard ventilated.
- **Out:** the panels, by natural convection on both faces and the little bare 5052 radiates (ε 0.07). The polycarbonate viewing
  window radiates more (ε 0.9). Heat also leaves down through the base plate. In total UA ≈ 3.9 W/K. With the cooling, add the exhaust
  flow, or the fan coil's 15 W/K to 20 °C water (an estimate for a 120 mm radiator and fan).

| Case | Shuttle air (°C) | As drawn (closed) | Vented, Shuttle air | Vented, room air from the dock (22 °C) | Closed, chilled-water fan coil (not drawn) |
|---|---:|---:|---:|---:|---:|
| typical build, rest of Shuttle 1 idling | 30.2 | **57.8** | 35.6 | 28.7 | 33.6 |
| typical build, PR 318's busy Shuttle | 38.0 | **63.8** | 42.7 | 29.3 | 34.5 |
| 500 W continuous, busy Shuttle | 42.6 | **86.1** | 48.8 | 31.7 | 39.2 |

(Guard air, °C. The Shuttle temperatures are `tray_budget.json`'s.) Where the heat goes in the typical case:

| | As drawn | Vented, Shuttle air | Vented, dock air | Fan coil |
|---|---:|---:|---:|---:|
| devices and fans (W) | 102 | 118 | 118 | 108 |
| chamber's outside at 60 °C (W) | 7 | 100 | 130 | 105 |
| out through the panels (W) | 109 | 16 | −4 (in) | 9 |
| out with the exhaust air, or into the coil (W) | – | 202 | 251 | 203 |

- **The closed guard is the problem, more than the Shuttle's temperature.** With ~100 W inside and 3.9 W/K out, it runs 26 K over its
  surroundings before the chamber adds anything. It stays well over them if the guess is wrong (typical case, `cooling.json`
  `sensitivity_typical_guard_air_c`): with painted panels (ε 0.9) it is at 50.5 °C, and with seams leaking 5 or 15 m³/h of air it is
  at 53.4 or 47.8 °C. An anodised chamber outside (ε 0.8) adds 0.8 K to the vented case.
- **The 60 °C chamber wall is a bound, not a result.** In a typical build the heaters put ~97 W into the module and the beam 210 W into
  the chamber. A 60 °C outside passes 40–130 W of that to the guard and its legs. The rest has to leave by the gas loop, or the
  chamber runs hotter than thermal.json assumes. Nobody has closed the chamber's own balance (§10).

## 3. Device temperatures, before and after

Each device's steady temperature comes from four terms:

- its own dissipation, into the air round it (natural convection, forced in the flow; ε 0.85 to the guard's inner surfaces);
- radiation from the 60 °C wall or lid where it faces one (the Chronos's front; the LP camera and lens over the lid);
- conduction through its mount: 1.3 W/K from the chamber's floor plate for the Chronos bracket, 0.1 W/K with the G-10 pad; 0.4 W/K
  from the LP boss for the LP camera, 0.017 W/K with the G-10 ring; 1 W/K from the bridge for the cage's devices;
- the optics bridge's own temperature: 70 % of the galvo's heat goes down its riser into a 25 mm plate. Its 0.12 m² could only shed
  30 W at ~40 K above the air, so most of it has to go that way.

The Chronos has its own fan, so it is taken as 25 W/m²K over its body and checked on the air it breathes. Bold marks a value over its
rating; the full set is in [`cooling.json`](../analysis/out/monitoring/cooling/cooling.json).

**Typical (Shuttle 30.2 °C):**

| Device | Rating (°C) | Checked on | As drawn | Vented, Shuttle air | Vented, dock air | Fan coil |
|---|---:|---|---:|---:|---:|---:|
| Chronos 2.1-HD | 40 | air in its hood | **57.8** | 30.7 | 22.5 | 33.6 |
| LP camera (IMX296) | 50 | board | **60.9** | 41.5 | 35.4 | 43.2 |
| Coaxial camera (IMX296) | 50 | board | **66.8** | 44.5 | 37.7 | 42.8 |
| Alvium U-030 VSWIR (route B) | 55 | housing | **68.3** | 45.9 | 39.2 | 44.3 |
| PDA36A2, each | 40 | air | **57.8** | 35.6 | 28.7 | 33.6 |
| BW 850 nm LED | 40 | air | **57.8** | 35.6 | 28.7 | 33.6 |
| AE preamp | 65 | case | 58.9 | 36.7 | 29.8 | 34.8 |
| Kowa lenses | 50 | air | **57.8** | 35.6 | 28.7 | 33.6 |
| PB2's air (Pi 5) | 70 | air | **82.3** | 39.9 | 33.0 | 37.8 |
| PB2's Pi 5 SoC | 80 | SoC | **99.8** | 57.4 | 50.5 | 55.3 |
| LP camera's Pi 5 SoC | 80 | SoC | 75.3 | 53.1 | 46.2 | 51.1 |
| basiCube 20 galvo (context) | 35 | air | **57.8** | **35.6** | 28.7 | 33.6 |
| optics bridge | – | – | 66.7 | 44.7 | 37.9 | 42.7 |

**Busy (Shuttle 38.0 °C):**

| Device | Rating (°C) | As drawn | Vented, Shuttle air | Vented, dock air | Fan coil |
|---|---:|---:|---:|---:|---:|
| Chronos 2.1-HD | 40 | **63.8** | 38.5 | 22.5 | 34.5 |
| LP camera (IMX296) | 50 | **62.3** | 47.8 | 35.9 | 44.0 |
| Coaxial camera (IMX296) | 50 | **72.7** | **51.5** | 38.3 | 43.8 |
| Alvium U-030 VSWIR | 55 | **74.2** | 52.9 | 39.7 | 45.3 |
| PDA36A2, each | 40 | **63.8** | **42.7** | 29.3 | 34.5 |
| BW 850 nm LED | 40 | **63.8** | **42.7** | 29.3 | 34.5 |
| AE preamp | 65 | 64.9 | 43.7 | 30.4 | 35.7 |
| Kowa lenses | 50 | **63.8** | 42.7 | 29.3 | 34.5 |
| PB2's air / SoC | 70 / 80 | **87.5 / 105.0** | 46.9 / 64.4 | 33.6 / 51.1 | 38.8 / 56.3 |
| LP camera's Pi SoC | 80 | **81.3** | 60.2 | 46.8 | 52.0 |
| basiCube 20 galvo (context) | 35 | **63.8** | **42.7** | 29.3 | 34.5 |

**Worst (500 W continuous, Shuttle 42.6 °C):** as drawn, everything is over, the AE preamp included (88 °C). Vented with the Shuttle's
air, the guard is at 48.8 °C, and the Chronos's hood air at 43.1 °C. All the cameras, the photodiodes, the LED, the galvo and both Pis'
SoCs (90, 84) are over. With dock air, only the coaxial camera's board (51.8 against 50, on a 53.0 °C bridge) is over. With the fan
coil, the coaxial camera (59.9), the Alvium (61.3), the galvo (39.2) and PB2's SoC (80.6) are over.

- **What each part of the cooling does.**
  - Ventilation does most of it, by taking the guard from 26–44 K over the Shuttle to 5–10 K over its supply.
  - The hood puts the Chronos in supply air instead of guard air, 4–6 K cooler. That keeps it in rating in the busy case on Shuttle
    air (38.5 against 42.7).
  - The G-10 pad cuts the bracket's link to the 60 °C floor plate from 1.3 to 0.1 W/K, which takes 6.5 K off the Chronos's body
    (44 °C with it, typical vented case).
  - The G-10 ring cuts the LP camera's link to its 60 °C boss from 0.4 to 0.017 W/K. In the typical vented case that board would be
    54 °C without the ring, over its 50, and is 41.5 °C with it.
  - **PB2 sealed is the worst spot in the guard.** Its 8–12 W in a 160 × 90 × 60 mm polycarbonate box (UA 0.25 W/K) holds its air
    ~25 K over the guard's: 63 °C and an 81 °C SoC in the vented guard in the typical case, 69 °C and 87 °C in the busy one. The
    40 mm fan (~5 m³/h through a filtered vent) brings the box to ~3 K over the guard.
- **The SoC figures use Geekworm's own test of its P573 passive case** (+35 K over a 26.9 °C room after 20 minutes of four-core stress;
  not steady, [geekworm.com](https://geekworm.com/blogs/news/p573-copper-thermal-paste-raspberry-pi-5-cooling-test)), taken for both
  Pis at full load and half that at the cameras-and-supervisor load. The Active Cooler is taken as the same. These are estimates.
- **The coaxial cage** inherits the bridge's temperature through its posts. G-10 pads under the posts would put the cage's devices back
  near the air's temperature. The cost is ~1.8 µm/K at the plate of drift between cube 1 on the bridge and cubes 2 and 3 on G-10
  (mechanics.md Checks §4). They are not drawn; supply air from the dock does the same job.

## 4. What is drawn

![The cooling parts: inlet trap and filter, the hood duct and hood round the side camera, the exhaust trap and fans](../analysis/out/monitoring/cooling/cooling_parts.png)

| Part | Where | Size | BOM |
|---|---|---|---|
| Back panel openings | inlet x −394…−218, z −118…202; exhaust x 40…284, z 108…338 | 176 × 320 and 244 × 230 mm, cut in the 1.6 mm back panel | (S9) |
| Inlet light trap | inside the back panel, y 181.5…213.5 | 32 chevron blades, 1 mm, six legs, 10 mm pitch, 32 mm deep, in a 2 mm frame riveted to the panel | M0-C3 |
| Inlet filter | outside the back panel | 30 ppi polyurethane foam pad in a 1.5 mm frame (10 mm envelope). A dock duct can bolt on in its place | M0-C5, M0-C6 |
| Hood duct | plenum behind the inlet trap's right-hand part (x −283…−218), up to z 127…203, forward beside the bridge's back-left post, then over the side camera | 65 × 76 mm, then 178 × 76 mm; 1 mm sheet, riveted | M7-C1 |
| Hood fan | in the duct, blowing forward | Delta AFB0624H-A, 60 × 60 × 25 mm, 24 V | M7-C2 |
| Side camera hood | round the Chronos: sides, back and floor, with the duct's floor as its top; open at the lens end | x −396…−214, y −106…27, z −15…127; floor cut round the bracket plate | M7-C1 |
| Exhaust light trap | inside the back panel, y 181.5…213.5 | 23 blades, the same section | M0-C3 |
| Exhaust plenum and fans | outside the back panel, at the exhaust's top | 1.5 mm box y 216.5…226.5; two Delta AFB1224SH 120 × 120 × 25 mm with finger guards, out to y 254.5 | M0-C1, M0-C2, M0-C6 |
| G-10 pad | between the side camera bracket's root and the chamber's floor plate (x −162…−156) | 6 mm × 80 × 16 mm, notched round the through-beam's fibre head; the bracket's root is 6 mm shorter, so the camera stays put | M7-C3 |
| G-10 ring | the first 5 mm of the LP camera's filter holder, on the boss's retaining ring | Ø32 × Ø25.4 × 5 mm, SM1-threaded both ends; the holder is 5 mm shorter | M7-C3 |
| PB2 vent fan | on PB2's +x end wall, over a Ø38 hole | Noctua NF-A4x10 24V, 40 × 40 × 10 mm; a filtered vent at PB2's other end (not drawn) | M0-C7 |
| LP camera's Pi | on the bridge behind the fold mirror, left of the LP camera, x −190…−96, y 117…179 | Pi 5 in a fanless aluminium case, envelope 94 × 62 × 33 mm, on 0.5 mm pads | M7-C4 |

- **Why the back panel.** The left panel is 8.5 mm from the rack's vented side panel, and its air is the rack's exhaust. The front has the
  door, its rail and the robot's AprilTags. The top would add height. The back faces the dock, where any duct would come from, and has
  room inside above the bridge and beside its posts. The air comes in low on the −x side, passes the Chronos and the cage there, crosses
  over the bridge and PB2, and leaves on the +x side.
- **The traps are clear of the beam's straight-line paths.** The collimator's beam runs along x at y ≈ 95, z 271, from x −387 to the
  fold mirror at −155. The inlet stops at x −218 and z 202, and the exhaust starts at x 40, behind PB2.

### 4.1 Interference

[`interference.py`](../analysis/interference.py) with `LPBF_MONITORING=1`, 330 parts, on M50, S25 and L75. The cooling parts touch the
panel, the floor plate and the LP ring face to face, so they add no volume to any pair; nine designed contacts declare them anyway.

| Module | Run (UTC) | Static states | Motion sweeps | Peak memory |
|---|---|---|---|---|
| M50 | 09:27–09:31 | 0 interferences in all six | 0 in all eight | 3.57 GB |
| S25 | 09:31–09:34 | 0 interferences in all six | 0 in all eight | 3.65 GB |
| L75 | 09:34–09:38 | 0 interferences in all six | 0 in all eight | 3.54 GB |

The reports are [`interference-monitoring-M50-M.md`](../analysis/out/monitoring/mech/interference-monitoring-M50-M.md) and its S25
and L75 siblings. Tightest static gaps between the cooling parts and the rest (exact OpenCascade distances, closed state):

| Cooling part | Nearest other part | Gap (mm) |
|---|---|---:|
| exhaust trap | optics bridge's back edge (y 180) | 1.5 |
| LP camera's Pi case | the bridge under it (on 0.5 mm pads); the fold mirror's cage cube; the LP camera | 0.5; 1.3; 4.5 |
| exhaust plenum, outside | guard frame | 1.9 |
| hood duct | the bridge's back-left post; the bridge's underside; the BW LED | 2.0; 8.1; 9.5 |
| inlet trap | guard frame; the bridge's back-left post | 4.0; 6.5 |
| hood fan | the bridge's back-left post | 4.5 |
| PB2 vent fan | PB2's screws; PB2 (drawn beside its tabs) | 4.3; 6.3 |
| side camera hood | the Chronos; the door drive's bracket | 6.3; 14.0 |
| G-10 pad | the chamber body above the floor plate | 0.1 |

The frames, plenums, pad and ring are drawn touching what they fasten to.

## 5. The light traps: OD at 1070 nm

[`trap_mc.py`](../analysis/monitoring/cooling/trap_mc.py) traces the trap's section: a periodic stack of zigzag blades, light entering
from the guard's side, each surface reflecting a fraction ρ (30 % of that specularly for anodise, which keeps some of the rolled sheet's
shine; all diffuse for the foils), with weighted rays. The section is 2-D because the blades are long (176–244 mm against a 10 mm
pitch): a ray's component along the blades doesn't change its number of bounces, and a long blade's diffuse scatter seen in section
follows cos θ / 2. The frames' end walls only add bounces. 120,000 rays for diffuse light; for a collimated beam, 30,000 at each angle
from −85° to +85° in 5° steps, keeping the worst.

| Blade surface at 1064–1070 nm | ρ | Source | OD, diffuse | OD, worst collimated beam |
|---|---:|---|---:|---:|
| Thorlabs BKF12 black aluminium foil | 0.055 | Thorlabs' BKF12 graph, 8° AOI (price_lookups CL61) | 11.0 | 9.8 |
| black hard ("Duranodic") anodise, low reading | 0.12 | [NASA TP-3595](https://ntrs.nasa.gov/citations/19960029068) (1995) Fig. 3, Beckman DK2 sphere | 9.2 | 8.1 |
| black hard anodise, high reading | 0.20 | the same, LPSR sphere | 7.9 | 7.0 |
| dyed black anodise | 0.29 | Anoplate's chart, "~29 % above 700 nm" (CL93's note) | 6.8 | 6.1 |
| (sweep) | 0.40 | – | 5.8 | 5.3 |
| (sweep) | 0.50 | – | 5.1 | 4.6 |
| Thorlabs black flocked paper | 0.66 | Thorlabs' blackout-materials graph | 4.0 | 3.5 |

- **Required: OD ≥ 5.4**, safety.md §4.2's figure for a guard window or filter behind which Class 1 holds against a direct 500 W
  beam. OD 7 passes 50 µW, 38× under the 1.9 mW Class 1 limit. The light that normally reaches the traps is far weaker: each port lets
  ≤ ~1 W of diffuse 1070 nm into the guard (optics.md §5), which needs only OD 2.7.
- **Every path through the trap has at least five bounces.** The seed-to-seed spread is ±0.4 in OD at the BKF12 level.
- **Black anodise is enough if it is black at 1 µm.** Dyes that look black can be bright in the near infrared: Thorlabs' flocked paper
  is 66 % and its hardboard ~80 %. Order integral-colour (hard) black, measure a blade's 1064 nm reflectance before fitting, or line the
  blades with BKF12. Thorlabs says BKF12 is "not intended for use in laser safety applications", so the guard's leakage test with a
  power meter before first light (safety.md §14) stays the deciding check.
- **A stationary direct beam is a different fault.** A black blade absorbs ~90 % of a beam where the bare panel absorbs ~8 %, so a
  500 W beam held on a blade would melt it where the panel might survive. The traps are off every straight path of the beam (§4), and
  safety.md's burn test of the panels should include a trap.
- **Pressure drop:** the legs turn the air through 124° five times and 62° twice. Idelchik's sharp-bend loss
  (0.95 sin²(δ/2) + 2.05 sin⁴(δ/2)), ×1.5 for the low Reynolds number (~650), plus laminar friction and the porosity 0.37's
  contraction gives K ≈ 18 on the passage velocity: 25 Pa a trap at 118 m³/h. This is an estimate: measure the guard's flow when built.

## 6. Fans and flow

| Item | Value | Basis |
|---|---|---|
| Exhaust fans | 2 × Delta AFB1224SH: 192 m³/h free air, 107 Pa, 46.5 dB(A), 6.7 W each | Delta datasheet; curve read off its graph (CL5) |
| System at the operating point | **118 m³/h, 64 Pa**: filter 12, inlet trap 25, exhaust trap 25, plenum and guards 2 Pa | `operating_point()` |
| Quieter pair (AFB1224M, 35.5 dB(A)) | 78 m³/h at 31 Pa: the guard then runs ~9 K over its supply, too warm with Shuttle air | the same |
| Hood fan | Delta AFB0624H-A (60 mm, 2.2 W, 34 dB(A)): ~20 m³/h, 0.54 m/s along the camera | CL90 curve; duct K ≈ 6 (estimate) |
| PB2 fan | Noctua NF-A4x10 24V: 8.9 m³/h free air, 19 Pa, 19.6 dB(A); ~5 m³/h through PB2 | CL91; flow estimated |
| Filter | 30 ppi polyurethane foam, ~20 Pa at 1 m/s taken | no maker publishes a pressure drop for these: estimate |

Seam leakage is ignored. The exhaust fans hold the guard ~37 Pa under the Shuttle (the inlet filter's and trap's drop), so the seams
draw air in rather than letting it out. The fans take ~17 W from the 24 V CTRL rail (2 × 6.7 + 2.2 + 1.1 W).

## 7. What it does to heat.md's budget

| Configuration | Into the Shuttle | Out of the Shuttle | Shuttle change | Needs |
|---|---:|---:|---:|---|
| Vented into the Shuttle (as drawn) | +17 W (fans) | – | +0.05 K | nothing |
| Supply and exhaust through a ventilated dock | +17 W | 251 / 273 / 361 W (typical / busy / worst) | −0.8 / −0.8 / −1.1 K | 118 m³/h of room air at the dock: the same Kardex question as the laser's exhaust (heat.md §2 option 2) |
| Closed guard, chilled-water fan coil | +6 W | 203 / 218 / 288 W to the water | −0.6 / −0.7 / −0.9 K | chilled water at the dock (heat.md §2 option 1): add ~0.3 kW to the chiller's size |

(Shuttle change from tray_budget.json's still-air Shuttle, 5.5 W/m²K over 55.9 m².) **Recommendation: decide the guard with the
laser.** If the laser goes to chilled water, fit the fan coil (option M0-C9) and blank the drawn vents, or keep them for when the chiller
is off. If the dock is ventilated, duct the inlet from it and the exhaust into it. Until either is decided,
don't run the Chronos, the photodiodes or the galvo with the Shuttle's air above ~30 °C.

## 8. Parts and cost

From [`monitoring-bom.csv`](../monitoring-bom.csv) (rebuilt by `build_bom.py`), prices read today through the lab tunnel:

| ID | Part | Qty | USD |
|---|---|---:|---:|
| M0-C1 | Delta AFB1224SH 120 mm 24 V fans (Amazon marketplace; distributors blocked the tunnel) | 2 | 89.46 |
| M0-C2 | Qualtek 08130 finger guards | 2 | 2.06 |
| M0-C3 | the two light traps, black anodised: 55 bent blades and frames (estimate) | 1 | 300–650 |
| M0-C4 | Thorlabs BKF12 black foil, 305 mm × 15.2 m, to line the blades | 1 | 38.91 |
| M0-C5 | McMaster 30 ppi polyurethane foam pad, 1/4 in., 16 × 20 in | 1 | 9.85 |
| M0-C6 | exhaust plenum and the filter's frame (estimate) | 1 | 60–130 |
| M0-C7 | Noctua NF-A4x10 24V PWM for PB2 | 1 | 15.95 |
| M0-C8 | Raspberry Pi 5 Active Cooler (Adafruit) | 1 | 13.50 |
| M7-C1 | hood, duct and plenum, 1 mm aluminium (estimate) | 1 | 120–280 |
| M7-C2 | Delta AFB0624H-A 60 mm 24 V fan | 1 | 16.86 |
| M7-C3 | McMaster 85345K741 G-10 sheet, 1/4 in., 6 × 6 in | 1 | 20.31 |
| M7-C4 | Geekworm P573 fanless case for the LP camera's Pi | 1 | 13.00 |
| | **drawn cooling** | | **~700–1,280** |
| M0-C9 | option: chilled-water fan coil (Koolance HX-120YC radiator $52.94 read; fan, couplings, hose estimated) | 1 | 150–400 |
| M0-C10 | option, not recommended: TE Technology AC-094 Peltier cooler, 94 W at ΔT 0 (half the load; ~240 W more into the Shuttle) | 1 | 635 |

## 9. What this changes in files it doesn't own (not made here)

- **[`mechanics.md`](mechanics.md) Checks §7:** the flag should read: *"The guard's air is not the Shuttle's. Closed, it runs 26–44 K
  over it (cooling.md §2), and every camera, the photodiodes, PB2's Pi and the galvo are over their ratings. With the drawn vents it
  sits 5–10 K over its supply. That is in rating on 30 °C Shuttle air, but not on the busy case's 38–43 °C. The supply has to be
  room air from a ventilated dock, or a chilled-water fan coil, decided with the laser."* Its Chronos row becomes −20 to +40 °C (Kron),
  and the IMX296 row 0–50 °C (the Pi GS camera; InnoMaker publishes none). The bracket row gains the G-10 pad.
- **[`monitoring.md`](../monitoring.md):** add the cooling to §4 step 0 (M0-C1 to C8) and step 7 (M7-C1 to C4), and to §9's model list.
  §7 or the risks gain one line: the guard needs ventilation and a supply from outside the Shuttle, the same decision as the laser.
- **[`heat.md`](../heat.md) §2:** the galvo (25 ± 10 °C) and the guard's 100–190 W belong in the laser decision. The guard needs 118 m³/h of
  room air through a ventilated dock, or ~0.3 kW more chiller.
- **[`electrical.md`](../electrical.md):** PB2 (Hammond 1554JGY, IP66, sealed) overheats as specified, with its air at 63–69 °C and the
  SoC at 81–87 °C even in a ventilated guard. It needs the 40 mm fan, a filtered vent and the Active Cooler, which takes it to IP2x
  inside the guard. The 24 V CTRL rail gains ~17 W of fans. The LP camera's Pi now has a place: on the bridge, x −190…−96, y 117…179.
- **[`safety.md`](../safety.md):** two new light-trapped openings in the guard's back panel. Show them to the LSO, and include a trap in
  the panel burn test and the leakage check before first light.
- **README:** list this note with the other monitoring notes. **bom.csv:** no change; the cooling is in monitoring-bom.csv (steps 0 and 7).
- **`analysis/interference.py`:** it now needs ~3.6 GB. M50 peaked at 3.57 GB, and S25 at 3.46 GB in its first state with or without
  the cooling parts, so the round's 3 GB cap kills it right after meshing. It was run here with a 4 GB cap.

## 10. Not done / limits

- **One well-mixed volume of air.** The guard's upper half, where PB2, the cage and the galvo are, will run warmer than the mean, and
  the corners the flow misses warmer still. No CFD of the guard's air was run. A coarse OpenFOAM case would test the flow path and
  the hood.
- **The chamber's heat is a bound, not a balance.** Its outside is held at 60 °C. A typical build's ~300 W into the chamber is more than
  that releases; where the rest goes (gas loop, legs, a hotter wall) needs the chamber's own model.
- **Most dissipations are estimates:** the galvo's 30 W, the servos, the Chronos's 20 W (Kron publishes only 40 W input), the PDA36A2's
  2 W, the IMX296 boards' 0.75 W, PB2's 8–12 W (power.md). The 70 % of the galvo's heat into the bridge, the bridge's 9–20 K rise and
  the cage's 1 W/K posts are assumptions; measure the bridge's temperature on the built frame.
- **Pressure drops are estimated:** the trap's K from Idelchik's sharp-bend formula with a low-Re allowance, the filter's 20 Pa at
  1 m/s, the duct's K ≈ 6. The fan curves are read off Delta's graphs (±5 %). The fans' prices are Amazon marketplace listings whose
  authenticity wasn't checked: Digi-Key, Mouser and Newark blocked the tunnel.
- **The traps' OD is a 2-D trace with Lambertian-plus-specular surfaces.** Black anodise's reflectance at 1 µm comes from one NASA
  sample (hard anodise) and one anodiser's chart (dyed); no maker of black anodise publishes it. Measure a blade. The traps' end walls,
  frames and rivets are not traced, and neither is a stationary beam's burn-through.
- **The Chronos's fan** is taken as 25 W/m²K over its body; Kron publishes no flow. If it draws more than the duct's ~20 m³/h, it
  also pulls guard air in at the hood's open end. Its sensor runs 40–55 °C in a room (Kron's manual), so check its on-screen
  temperature in the built guard.
- **Not drawn:** the fan coil, PB2's filtered vent and Active Cooler (inside PB2, a closed envelope in the model), the G-10 shoulder
  washers, cables, the trap blades' rivets, and G-10 pads under the cage's posts (§3).
- **Not checked:** noise in the Shuttle (2 × 46.5 dB(A)); the filter's loading and when to change it; condensation on a fan coil (20 °C
  water against the Shuttle's dew point); the robot's reach against the hood, whose −y side stands 9 mm further toward the door than
  the Chronos did (the traps are on the back panel, away from the door and the AprilTags).
- **No LSO review** of the openings, and no shop review of the bent blades (55 blades, ~275 bends).

## Sources

- Vendor ratings: [`ratings.csv`](../analysis/out/monitoring/cooling/ratings.csv) (read 2026-11-27 08:25–08:47 UTC; URLs per row).
- Prices, fan curves, filter media and foils: [`price_lookups_round3_cooling.csv`](../analysis/out/monitoring/fab/price_lookups_round3_cooling.csv)
  (read 08:37–09:04 UTC).
- Reflectance at 1 µm: NASA TP-3595 (1995), *Evaluation of Thermal Control Coatings and Polymeric Materials Exposed to Ground
  Simulated Atomic Oxygen and Vacuum Ultraviolet Radiation*, Fig. 3 ([NTRS 19960029068](https://ntrs.nasa.gov/citations/19960029068));
  Thorlabs' BKF12 and blackout-materials reflectance graphs ([thorlabs.com](https://www.thorlabs.com/blackout-and-laser-safety-materials?tabName=Overview));
  Anoplate's black anodise chart (CL93's note).
- Idelchik, I.E., *Handbook of Hydraulic Resistance*, sharp bends in channels: ζ = 0.95 sin²(δ/2) + 2.05 sin⁴(δ/2).
- Incropera, F.P. et al., *Fundamentals of Heat and Mass Transfer*: natural convection on vertical and horizontal plates, laminar
  forced convection over a plate, radiation between grey surfaces.
- Geekworm's P573 test ([geekworm.com](https://geekworm.com/blogs/news/p573-copper-thermal-paste-raspberry-pi-5-cooling-test), read 08:41 UTC).
- This repo: `analysis/out/tray/tray_budget.json` (Shuttle air, loads), [`heat.md`](../heat.md) §2, `analysis/out/thermal/thermal.json`
  (the 60 °C chamber bound), [`power.md`](../analysis/out/electrical/power.md) §4 (PB2), [`safety.md`](../safety.md) §4.2 (OD 5.4),
  [`optics.md`](optics.md) §5 (1070 nm at the ports), [`mechanics.md`](mechanics.md) Checks §3, §4 and §7.
