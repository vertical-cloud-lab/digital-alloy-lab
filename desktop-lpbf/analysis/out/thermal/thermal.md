# Heated build modules: steady and transient thermal FEA (CalculiX, axisymmetric)

`analysis/thermal_module.py` builds an r–z model of each module from [`cad/module_params.py`](../../../cad/module_params.py) (stack 50 mm: plate 10, heater block 14, break 8, head 18; rod 77 mm with its end hardware), meshes it with 8-node axisymmetric quads (CAX8) and solves it with ccx 2.21. For each steady case it finds, by a secant on heater power, the power that holds the **plate top centre at 200 °C**. Inputs: 0.10 mm (plate) and 0.30 mm (block) radial argon gaps to the bore; plate–block contact 2000 W/m²K; 8 mm argon break with smeared Macor posts and radiation through 2 shields; felt/PTFE bore seal on the head rim; 0.03 mm spigot fit plus an FKM O-ring; flange on the floor at 1500 W/m²K; floor edge (r = 120 mm) at the chamber temperature. Plate top: forced argon h 17 W/m²K (× (50/D)^0.5) plus radiation. Under the floor: 5 W/m²K plus ε 0.3 to 25 °C. Coupling face: 10 W/m²K. Inside the cylinder below the head: adiabatic.

## Tier A, 200 °C plate, chamber 25 °C, powder on the plate (ε 0.5)

Temperatures in °C. Limits: felt/PTFE seal 204, FKM 200 (150 preferred), NdFeB magnet 80, block TCO 240. Loss split = share of heater power leaving the plate and block through the top / the radial gaps into the bore wall / the break into the head. Hot clearance = plate-to-bore radial clearance at temperature (µm, from the mean plate and bore-ring temperatures; 100 µm cold).

| Module, position | Heater (W) | Plate edge (centre − edge) | Block max | Bore seal | Spigot O-ring | Rod-gland O-rings | Coupling face (magnet) | Floor / all into chamber (W) | Split top / gaps / break (%) | Hot clearance (µm) |
|---|---|---|---|---|---|---|---|---|---|---|
| S25, build start (z_p 0) | **47** | 199 (1.2) | 240 | 58 | 35 | 43 | 39 | 39 / 44 | 6 / 89 / 5 | 51 |
| S25, build end (z_p −40) | **31** | 198 (1.6) | 228 | 114 | 30 | 109 | 65 | 21 / 22 | 19 / 76 / 5 | 68 |
| M50, build start (z_p 0) | **90** | 198 (2.3) | 217 | 71 | 44 | 49 | 44 | 75 / 86 | 9 / 84 / 6 | 5 |
| M50, build end (z_p −40) | **59** | 198 (2.4) | 212 | 123 | 35 | 118 | 68 | 42 / 43 | 22 / 72 / 6 | 37 |
| L75, build start (z_p 0) | **135** | 197 (3.4) | 211 | 66 | 54 | 46 | 42 | 112 / 130 | 12 / 83 / 5 | -36 |
| L75, build end (z_p −40) | **86** | 197 (3.2) | 208 | 122 | 40 | 117 | 68 | 62 / 64 | 24 / 71 / 5 | 6 |

Heaters and transients (heat-up from 25 °C at full power with the plate at z_p 0; cool-down with the heaters off from the build-end steady state, to the 50 °C door interlock):

| Module | Worst steady (W) | Installed now | ≥ 1.5 × worst, in whole heaters | Heat-up to 200 °C, installed | Heat-up, suggested | Block when the plate reaches 200 °C (suggested) | Least plate clearance in that heat-up (µm) | Cool-down to 50 °C |
|---|---|---|---|---|---|---|---|---|
| S25 | 47 | 2 × 50 W = 40 W | **2 × 50 W = 80 W** | never (levels at 179 °C) | 2 min | 260 °C | 49 | 15 min |
| M50 | 90 | 3 × 50 W = 80 W | **4 × 50 W = 160 W** | never (levels at 182 °C) | 4 min | 226 °C | 1 | 26 min |
| L75 | 135 | 5 × 50 W = 160 W | **6 × 50 W = 240 W** | 12 min | 5 min | 218 °C | -35 | 36 min |

## Sensitivities (heater power in W for 200 °C at the plate top centre)

| Case | S25 start | S25 end | M50 start | M50 end | L75 start | L75 end |
|---|---|---|---|---|---|---|
| baseline: chamber 25 °C, powder ε 0.5 | 47 | 31 | 90 | 59 | 135 | 86 |
| chamber and floor edge at 60 °C | 39 | 26 | 75 | 50 | 112 | 74 |
| bare plate, ε 0.1 (start only) | 46 | – | 88 | – | 130 | – |
| 60 °C chamber, bare plate | 38 | – | 73 | – | 108 | – |
| plate and block gaps full of powder (k 0.2), M50 | – | – | 293 | 90 | – | – |
| plate radial gap 0.05 mm instead of 0.10 (M50) | – | – | 125 | – | – | – |
| plate radial gap 0.20 mm instead of 0.10 (M50) | – | – | 68 | – | – | – |

## Tier B reserve: M50 at 500 °C, 316L head with its underside held at 30 °C, 5 mm flange band at 30 °C

| Position | Heater (W) | To water: head / flange (W) | Into floor (W) | Plate edge | Bore seal | Spigot O-ring | Rod-gland O-rings | Coupling face | Hot clearance (µm, 200 cold) |
|---|---|---|---|---|---|---|---|---|---|
| start | **243** | 21 / 77 | 101 | 495 | 55 | 54 | 41 | 37 | -65 |
| end | **179** | 48 / 48 | 54 | 494 | 162 | 39 | 122 | 49 | 10 |

## Against the lumped estimate in `requirements_budgets.py` (200 °C)

| Module | Lumped: rad + conv + posts + cylinder = loss (W) | FEA start / end (W) | FEA: top / gaps / break, start (W) | Lumped cool-down | FEA cool-down |
|---|---|---|---|---|---|
| S25 | 1 + 2 + 3 + 19 = 24 | 47 / 31 | 3 / 41 / 2 | 30 min | 15 min |
| M50 | 2 + 6 + 3 + 38 = 49 | 90 / 59 | 8 / 76 / 6 | 37 min | 26 min |
| L75 | 5 + 11 + 3 + 57 = 76 | 135 / 86 | 16 / 111 / 7 | 42 min | 36 min |

## What this means for the design

1. **The installed heaters are short at build start.** With the plate in the spigot (z_p 0) the set point takes 47 / 90 / 135 W (S25 / M50 / L75), against 31 / 59 / 86 W at the build end. 89–82 % of it crosses the 0.10 mm plate gap and 0.30 mm block gap into the bore. At the start that bore is the spigot, which the 0.03 mm fit and the flange tie to the floor, so most of the power ends up in the floor (M50: 75 of 90 W; the floor at the port only reaches 28 °C). With today's heaters, S25 levels at 179 °C and M50 levels at 182 °C after 3 h. Fit ≥ 1.5 × the worst case: S25 80 W, M50 160 W, L75 240 W (table above), or cut the gap loss (2, 3).
2. **The plate gap closes when hot.** The 6061 plate grows ~107 µm (M50) to ~161 µm (L75) on radius at 200 °C, while the 316L bore round it stays at 50–58 °C at build start. The 100 µm cold gap therefore runs at 5 µm (M50) and -36 µm (L75, interference) at steady state, and closes further in a fast heat-up because the bore lags (1 / -35 µm, M50 / L75 at the suggested power). A tighter gap also leaks more heat: 0.05 mm takes 125 W, 0.20 mm 68 W (M50). Set the cold radial clearance per size, ≥ ~0.12 mm for M50 and ≥ ~0.17 mm for L75 (keeps 30 µm hot; S25's 0.10 mm is fine), ramp-limit the heat-up, and close the gap against powder with a hot-side wiper at the plate rim.
3. **Powder in the gaps is the largest risk.** Filled with powder (k 0.2 against argon's ~0.025), the gaps make M50 need 293 W at the start (block 243 °C, past the 240 °C cutoff) and 90 W at the end, where the coupling face reaches 86 °C (magnet limit 80) and the rod gland 157 °C. At z_p 0 the plate gap opens onto the powder plane, so the wiper in point 2 is required, not optional.
4. **S25's heater block runs at its cutoff.** Its Ø24.8 contact face carries ~30 W at 2000 W/m²K, so the block runs ~40 °C above the plate: 240 °C at steady build start, against TCO_A = 240 °C, and 260 °C when the plate reaches 200 °C at 80 W. Put graphite foil in the contact (aim for ≥ 5000 W/m²K) and ramp-limit the power. Also, S25's central cartridge and its single central Macor standoff occupy the same spot; use a Macor sleeve round the cartridge, or three small standoffs.
5. **Seals and the magnet pass in Tier A with clean (argon) gaps.** Worst over the 200 °C cases: bore seal 127 °C (limit 204), spigot O-ring 83 °C (54 with a 25 °C chamber; prefer ≤ 150), rod-gland O-rings 122 °C (≤ 200), coupling face 70 °C (≤ 80). Build end is the hot case for the seal, gland and magnet, because the head then sits 2 mm above the bottom flange. The magnet has ~10 °C of margin, and loses it if powder fills the gaps (point 3). A 3–5 mm G10 or PEEK washer under the striker, or an SH-grade (150 °C) magnet, restores it. The 10 W/m²K coupling face is conservative: the 6061 Z arm under it is a better sink.
6. **The 0.03 mm spigot fit can bind.** The 316L spigot runs warmer than the 6061 port (it expands 16.5 against 23.6 µm/m·K), and the hot fit falls to -27 µm (with powder-filled gaps). Loosen it to ~0.10 mm radial, let the O-ring seal, and locate the module on the flange.
7. **Tier B (M50, 500 °C).** 243 W at the start (98 W to water, 101 W to the floor) and 179 W at the end. Seals and O-rings ≤ 162 °C (bore seal at the build end: the tube beside the head runs hot), magnet ≤ 49 °C. But the block reaches 540 °C, too near 6061's ~580 °C solidus, so Tier B needs a steel or ceramic heater block. The 0.20 mm cold plate gap runs at -65 µm, so Tier B needs ≥ ~0.3 mm.
8. **Against the lumped estimate.** `requirements_budgets.py` puts the Ø50 loss at 49 W, 38 W of it down a 60 mm cylinder wall assumed to be at plate temperature, and it has no plate-to-bore gap. The FEA agrees at the build end (59 W; the wall beside the plate runs at ~124 °C). At the build start, though, the plate sits in a 22.6 mm-thick 316L spigot held near floor temperature, and the gap carries ~76 W across ~150 K. The FEA cool-downs are shorter than the lumped 30–42 min for the same reason: the loss is larger.
9. **Chamber load.** 86 W (M50) to 130 W (L75) go into the chamber at build start, mostly through the floor. A 60 °C chamber cuts the heater power by ~17 % but warms the spigot O-ring by ~30 °C.

## Mesh and checks

- Element size 1.0 mm in the module, growing to 4 mm at the floor edge; gaps and contact layers are one element across (13091 nodes, 4163 CAX8 for M50 at build start). M50 build-start power: 2 mm mesh 90.6 W, 1 mm 90.3 W, 0.5 mm 90.1 W (+0.6 % and +0.2 % against the finest). Transients use the 2 mm mesh and ccx's automatic steps (≤ 8 °C, ≤ 60–120 s).
- Energy balance: heater power against the sum of all sinks closes to 0.03 % in every case; the exit split (gradients in the gap elements) to 12.5 %.
- Units and ccx conventions checked on 1D cases (annulus conduction, film, radiation): annulus +0.00 %, film +0.00 %, rad -0.15 %. ccx reports CAX reaction heat for a 2° sector (×180).
