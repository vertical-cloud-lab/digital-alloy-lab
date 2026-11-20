# Heated build modules: steady and transient thermal FEA (CalculiX, axisymmetric)

`analysis/thermal_module.py` builds an r–z model of each module from [`cad/module_params.py`](../../../cad/module_params.py) (stack 50 mm: plate 10, heater block 14, break 8, head 18; rod 77 mm with its end hardware), meshes it with 8-node axisymmetric quads (CAX8) and solves it with ccx 2.21. For each steady case it finds, by a secant on heater power, the power that holds the **plate top centre at 200 °C**. Inputs: radial argon plate and 0.30 mm block gaps to the bore (cold radial plate clearance per size: S25 0.10 mm, M50 0.15 mm, L75 0.20 mm); plate–block contact 5000 W/m²K; 8 mm argon break with smeared Macor posts and radiation through 2 shields; felt/PTFE bore seal on the head rim; 0.10 mm spigot fit plus an FKM O-ring; flange on the floor at 1500 W/m²K; floor edge (r = 120 mm) at the chamber temperature. Plate top: forced argon h 17 W/m²K (× (50/D)^0.5) plus radiation. Under the floor: 5 W/m²K plus ε 0.3 to 25 °C. Coupling face: 10 W/m²K. Inside the cylinder below the head: adiabatic.

## Tier A, 200 °C plate, chamber 25 °C, powder on the plate (ε 0.5)

Temperatures in °C. Limits: felt/PTFE seal 204, FKM 200 (150 preferred), NdFeB magnet 80, block TCO 240. Loss split = share of heater power leaving the plate and block through the top / the radial gaps into the bore wall / the break into the head. Hot clearance = plate-to-bore radial clearance at temperature (µm, from the mean plate and bore-ring temperatures).

| Module, position | Heater (W) | Plate edge (centre − edge) | Block max | Bore seal | Spigot O-ring | Rod-gland O-rings | Coupling face (magnet) | Floor / all into chamber (W) | Split top / gaps / break (%) | Hot clearance (µm) |
|---|---|---|---|---|---|---|---|---|---|---|
| S25, build start (z_p 0) | **44** | 199 (1.2) | 221 | 60 | 39 | 45 | 41 | 35 / 42 | 6 / 89 / 5 | 51 |
| S25, build end (z_p −40) | **30** | 198 (1.6) | 215 | 111 | 33 | 107 | 64 | 20 / 21 | 20 / 75 / 5 | 67 |
| M50, build start (z_p 0) | **72** | 198 (1.6) | 206 | 70 | 48 | 49 | 44 | 57 / 68 | 12 / 81 / 7 | 56 |
| M50, build end (z_p −40) | **52** | 198 (2.0) | 205 | 116 | 38 | 112 | 65 | 35 / 37 | 24 / 69 / 7 | 82 |
| L75, build start (z_p 0) | **97** | 198 (1.9) | 204 | 66 | 56 | 46 | 42 | 74 / 92 | 17 / 76 / 7 | 64 |
| L75, build end (z_p −40) | **71** | 198 (2.3) | 203 | 113 | 42 | 108 | 64 | 50 / 52 | 28 / 66 / 6 | 96 |

Heaters and transients (heat-up from 25 °C at full power with the plate at z_p 0; cool-down with the heaters off from the build-end steady state, to the 50 °C door interlock):

| Module | Worst steady (W) | Installed now | ≥ 1.5 × worst, in whole heaters | Heat-up to 200 °C, installed | Heat-up, suggested | Block when the plate reaches 200 °C (installed) | Least plate clearance in that heat-up (µm) | Cool-down to 50 °C |
|---|---|---|---|---|---|---|---|---|
| S25 | 44 | 2 × 50 W = 100 W | **2 × 50 W = 100 W** | 1 min | – | 242 °C | 48 | 15 min |
| M50 | 72 | 3 × 50 W = 150 W | **3 × 50 W = 150 W** | 3 min | – | 211 °C | 51 | 28 min |
| L75 | 97 | 5 × 50 W = 250 W | **3 × 50 W = 150 W** | 4 min | 9 min | 209 °C | 60 | 40 min |

## Sensitivities (heater power in W for 200 °C at the plate top centre)

| Case | S25 start | S25 end | M50 start | M50 end | L75 start | L75 end |
|---|---|---|---|---|---|---|
| baseline: chamber 25 °C, powder ε 0.5 | 44 | 30 | 72 | 52 | 97 | 71 |
| chamber and floor edge at 60 °C | 37 | 26 | 60 | 44 | 81 | 61 |
| bare plate, ε 0.1 (start only) | 44 | – | 70 | – | 93 | – |
| 60 °C chamber, bare plate | 36 | – | 58 | – | 77 | – |
| plate and block gaps full of powder (k 0.2), M50 | – | – | 226 | 84 | – | – |
| plate radial gap 0.10 mm instead of 0.15 (M50) | – | – | 85 | – | – | – |
| plate radial gap 0.20 mm instead of 0.15 (M50) | – | – | 65 | – | – | – |

## Tier B reserve: M50 at 500 °C, 316L head with its underside held at 30 °C, 5 mm flange band at 30 °C

| Position | Heater (W) | To water: head / flange (W) | Into floor (W) | Plate edge | Bore seal | Spigot O-ring | Rod-gland O-rings | Coupling face | Hot clearance (µm, 200 cold) |
|---|---|---|---|---|---|---|---|---|---|
| start | **235** | 20 / 93 | 76 | 495 | 58 | 64 | 43 | 38 | -61 |
| end | **175** | 47 / 57 | 42 | 494 | 159 | 43 | 120 | 49 | 9 |

## Against the lumped estimate in `requirements_budgets.py` (200 °C)

| Module | Lumped: rad + conv + posts + cylinder = loss (W) | FEA start / end (W) | FEA: top / gaps / break, start (W) | Lumped cool-down | FEA cool-down |
|---|---|---|---|---|---|
| S25 | 1 + 2 + 3 + 19 = 24 | 44 / 30 | 3 / 39 / 2 | 30 min | 15 min |
| M50 | 2 + 6 + 3 + 38 = 49 | 72 / 52 | 8 / 58 / 5 | 37 min | 28 min |
| L75 | 5 + 11 + 3 + 57 = 76 | 97 / 71 | 16 / 74 / 7 | 42 min | 40 min |

## What this means for the design

1. **Build start is the worst case.** With the plate in the spigot (z_p 0) the set point takes 44 / 72 / 97 W (S25 / M50 / L75), against 30 / 52 / 71 W at the build end. 76–88 % of it crosses the radial plate and block gaps into the bore. At the start that bore is the spigot, which its 0.10 mm fit and the flange tie to the floor, so most of the power ends up in the floor (M50: 57 of 72 W; the floor at the port only reaches 27 °C). The heaters now in `module_params.py` give S25 2.3×, M50 2.1×, L75 2.6× the worst steady power, so all meet the 1.5× margin.
2. **The plate gap closes when hot.** The 6061 plate grows ~107 µm (M50) to ~161 µm (L75) on radius at 200 °C, while the 316L bore round it stays at 52–59 °C at build start. With the cold clearances now in `module_params.py` (S25 100, M50 150, L75 200 µm), the hot gap at steady build start is 51 / 56 / 64 µm (S25 / M50 / L75), and the least in a full-power heat-up, when the bore lags, is 48 / 51 / 64 µm. The gap also sets the leak: M50 at 0.10 / 0.15 / 0.20 mm takes 85 / 72 / 65 W. That leaves ≥ 20 µm everywhere, so these clearances work. Close the gap against powder with a hot-side wiper at the plate rim.
3. **Powder in the gaps is the largest risk.** Filled with powder (k 0.2 against argon's ~0.025), the gaps make M50 need 226 W at the start (block 216 °C, 24 °C under the 240 °C cutoff) and 84 W at the end, where the coupling face reaches 84 °C (magnet limit 80) and the rod gland 151 °C. At z_p 0 the plate gap opens onto the powder plane, so the wiper in point 2 is required, not optional.
4. **S25's heater block runs 19 °C under its cutoff.** Most of its heat crosses the small Ø24.8 contact face (5000 W/m²K) to reach the plate rim, so the block runs 21 °C above the set point: 221 °C at steady build start, against TCO_A = 240 °C, and 242 °C when the plate reaches 200 °C at full power (100 W installed). The contact is modelled with graphite foil (5000 W/m²K); with a bare Al face (~2000 W/m²K) the block ran at its cutoff. Ramp-limit the heat-up: cap the block at ~225 °C with its own thermocouple reading, so the cutoff never sees the overshoot.
5. **Seals and the magnet pass in Tier A with clean (argon) gaps.** Worst over the 200 °C cases: bore seal 121 °C (limit 204), spigot O-ring 84 °C (56 with a 25 °C chamber; prefer ≤ 150), rod-gland O-rings 117 °C (≤ 200), coupling face 68 °C (≤ 80). Build end is the hot case for the seal, gland and magnet, because the head then sits 2 mm above the bottom flange. The magnet has 12 °C of margin, and loses it if powder fills the gaps (point 3). A 3–5 mm G10 or PEEK washer under the striker, or an SH-grade (150 °C) magnet, restores it. The 10 W/m²K coupling face is conservative: the 6061 Z arm under it is a better sink.
6. **Spigot fit (0.10 mm radial cold).** The 316L spigot runs warmer than the 6061 port (it expands 16.5 against 23.6 µm/m·K), and the hot fit falls to 37 µm (with powder-filled gaps). A 0.03 mm (H7/g6) fit closed to −23 µm in the first run, so the fit is now loose, the O-ring seals and two dowels locate the module on its flange.
7. **Tier B (M50, 500 °C).** 235 W at the start (114 W to water, 76 W to the floor) and 175 W at the end. Seals and O-rings ≤ 159 °C (bore seal at the build end: the tube beside the head runs hot), magnet ≤ 49 °C. But the block reaches 520 °C, too near 6061's ~580 °C solidus, so Tier B needs a steel or ceramic heater block. The 0.20 mm cold plate gap runs at -61 µm, so Tier B needs ≥ ~0.3 mm.
8. **Against the lumped estimate.** `requirements_budgets.py` puts the Ø50 loss at 49 W, 38 W of it down a 60 mm cylinder wall assumed to be at plate temperature, and it has no plate-to-bore gap. The FEA agrees at the build end (52 W; the wall beside the plate runs at ~114 °C). At the build start, though, the plate sits in a 22.6 mm-thick 316L spigot held near floor temperature, and the gap carries ~58 W across ~148 K. The FEA cool-downs are shorter than the lumped 30–42 min for the same reason: the loss is larger.
9. **Chamber load.** 68 W (M50) to 92 W (L75) go into the chamber at build start, mostly through the floor. A 60 °C chamber cuts the M50 heater power by 17 % but warms the spigot O-ring by 29 °C.

## Mesh and checks

- Element size 1.0 mm in the module, growing to 4 mm at the floor edge; gaps and contact layers are one element across (13293 nodes, 4229 CAX8 for M50 at build start). M50 build-start power: 2 mm mesh 72.4 W, 1 mm 72.1 W, 0.5 mm 72.0 W (+0.6 % and +0.2 % against the finest). Transients use the 2 mm mesh and ccx's automatic steps (≤ 8 °C, ≤ 60–120 s).
- Energy balance: heater power against the sum of all sinks closes to 0.03 % in every case. The exit split comes from gradients in the gap elements and closes to 0.8 % at build start; at build end the cake gradient at the plate's top corner is under-resolved, so the top share there is the remainder.
- Units and ccx conventions checked on 1D cases (annulus conduction, film, radiation): annulus +0.00 %, film +0.00 %, rad -0.15 %. ccx reports CAX reaction heat for a 2° sector (×180).
