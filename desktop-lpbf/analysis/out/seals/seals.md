# Seals, leaks and purge: results (from `analysis/seals/seals.py`)

Model: `cad/lpbf_low.build('M50', 'M')`. All forces in N, leaks in std cc/s (sccs) unless noted. Sources are listed at the end.

## Seal inventory

| Seal / penetration | Held by | Status | Note |
|---|---|---|---|
| Lid O-ring, FKM 75A 3.53 mm cord in a face gland 2.65 x 4.6 in the body's top face | 20 x M5 316 into helical inserts (metal-to-metal) | **OK** | cord spliced into a ring: specify a vulcanized (hot) splice or a molded ring, never a glued joint, for vacuum |
| Door O-ring, 3.53 mm cord, groove on the door face 2.8 deep x 4.0 wide as drawn | 2 draw latches (McMaster 1807A61) at the top corners + 2 fixed hinges at the bottom; atmosphere under vacuum | **FIX** | gland is not the 2.65 x 4.6 the notes specify; latches were sized for +50 mbar only, not for squeezing the cord (see clamp table) |
| Window O-ring under the Ø50.8 x 8 fused-silica window; retaining ring 2 mm above the window top | nothing at +20 mbar: the window is 'unclamped' and floats up to 2 mm | **FIX** | +20 mbar lifts the window (3.2 N against its 0.35 N weight); needs an O-ring sandwich clamped to a metal stop |
| Window flange to lid: 6 x M4, no seal drawn | 6 x M4 | **MISSING** | needs a face O-ring (or make the flange part of the lid) |
| Cover-slide drawer front plate, ~1.78 mm cord on the lid's front face | nothing (a detent) | **FIX** | at +20 mbar the drawer is pushed out; the cord needs ~0.3-0.5 kN to squeeze: a cam or toggle clamp |
| Metering base to lid over the 12 x 100 mm dose slot: 4 x M4, no seal drawn | 4 x M4 | **MISSING** | needs a face O-ring round the slot |
| Reservoir on the dock face (dovetail, spring shutter); reservoir lid is a loose plate | nothing | **FIX** | an open path from room air through the powder column and the roller clearance into the chamber (flow table below) |
| Metering-roller shaft: PTFE V-ring (McMaster 9572K33) | - | **CHECK** | a V-ring is an excluder, not a vacuum seal; use a magnetic-fluid feedthrough or a magnetic coupling through a can |
| Recoater screw through the left wall (Ø18 hole): fixed bearing + PTFE V-ring | - | **CHECK** | same as the roller shaft |
| Recoater screw through the right wall (Ø18 hole): floating bearing housing, open bore | - | **MISSING** | the housing's Ø8 bore is open to the room: make it a blind cap with a face O-ring |
| KF-25 vacuum port, KF-25 inlet/outlet plenum ports, KF-40 overflow, KF-16 blank | KF clamps | **OK** | Al centering ring + FKM; the stubs are 304 and the body 6061: the stub-to-body joint needs its own O-ring |
| Inlet plenum (back wall) and outlet plenum (under the floor), 316L on 6061 | M4/M5 (not drawn) | **MISSING** | joints.py lists them as 'each with an FKM O-ring', not drawn; dissimilar metals, so bolted + O-ring, never welded |
| Argon in (back wall), O2 sample (side wall), pressure transducer and relief valve (lid): 1/4 NPT parts | pipe threads | **CHECK** | NPT into 6061 leaks at vacuum and galls; use SAE/ISO straight-thread O-ring-boss ports or KF/VCR adapters |
| Through-beam fibre heads in Ø3.2 holes through both side walls (z = +5) | - | **MISSING** | needs O-ring-sealed threaded heads or a window; they also sit in the condensate and spatter zone |
| Camera viewport adapter with a Ø1 in. window over a Ø22 hole in the lid | screws (not drawn) | **MISSING** | two seals needed: adapter to lid, window to adapter |
| Module spigot in the Ø96 floor port: FKM 2-238 radial (male gland) | radial; 2 captive M6 | **CHECK** | groove as drawn (root Ø90.2, 3.6 mm wide) is overfilled at worst tolerance (101 %) and light on squeeze (13-21 %); root Ø90.5 x 4.8 wide gives 17-25 % and <= 81 % |
| Gland plate on the welded collar: 1.78 mm cord face seal | 6 x M4 | **CHECK** | groove 2.4 wide: fill > 90 % at worst tolerance; widen to 2.6 |
| Hollow rod through the gland plate: 'double FKM 2-114 rod gland' (grooves not drawn) | - | **MISSING** | draw two 2-114 grooves (Ø20.0 groove, Ø15.93 throat) and specify a seamless, polished rod; friction counts against the Z coupling |
| Rod end: heater and thermocouple leads potted in Torr Seal | - | **FIX** | stranded leads wick gas along the strands through any potting; use a hermetic (glass-to-metal) feedthrough or solid pins |
| Blower, cyclone + HEPA housing, valves, hoses (KF-25 bellows) | KF clamps | **CHECK** | the HEPA housing in the BOM (McMaster 5169K72) is 1/2 NPSC threaded and its gas-tightness is not stated; the blower must be specified gas-tight |
| O2 analyser sample loop | fittings | **CHECK** | extractive analysers often have polymer tubing inside; return the sample to the loop, 316L lines, leak-check the analyser |

## Gland checks (Parker ORD 5700, AS568 tolerance, ±0.05 mm machining)

| Gland | CS | depth × width | stretch | squeeze nom (min–max) % | fill nom / worst cold / worst warm % | Parker face rule |
|---|---|---|---|---|---|---|
| lid | 3.53 | 2.65 × 4.60 | 0.0 % | 25 (21–28) | 80 / 88 / 89 at 70 °C | depth 2.57–2.72, width 4.01–4.17 (gas) / 4.5–4.75 (liquid) |
| door_as_drawn | 3.53 | 2.80 × 4.00 | 0.0 % | 21 (17–24) | 87 / 95 / 97 at 60 °C | depth 2.57–2.72, width 4.01–4.17 (gas) / 4.5–4.75 (liquid) |
| door_spec | 3.53 | 2.65 × 4.60 | 0.0 % | 25 (21–28) | 80 / 88 / 89 at 60 °C | depth 2.57–2.72, width 4.01–4.17 (gas) / 4.5–4.75 (liquid) |
| door_1p78_halfdovetail | 1.78 | 1.32 × 2.30 | 0.0 % | 26 (20–32) | 82 / 95 / 96 at 60 °C | depth 1.27–1.37, width 2.13–2.26 (gas) / 2.57–2.72 (liquid) |
| window_1p78 | 1.78 | 1.32 × 2.30 | 0.0 % | 26 (20–32) | 82 / 95 / 97 at 80 °C | depth 1.27–1.37, width 2.13–2.26 (gas) / 2.57–2.72 (liquid) |
| drawer_1p78 | 1.78 | 1.32 × 2.30 | 0.0 % | 26 (20–32) | 82 / 95 / 96 at 60 °C | depth 1.27–1.37, width 2.13–2.26 (gas) / 2.57–2.72 (liquid) |
| spigot_as_drawn | 3.53 | 2.90 × 3.60 | 1.9 % | 17 (13–21) | 92 / 101 / 102 at 60 °C | radial |
| spigot_groove_90p5_w4p8 | 3.53 | 2.75 × 4.80 | 2.3 % | 21 (17–25) | 73 / 79 / 81 at 60 °C | radial |
| gland_plate_as_drawn | 1.78 | 1.30 × 2.40 | 0.0 % | 27 (21–33) | 80 / 92 / 94 at 60 °C | depth 1.27–1.37, width 2.13–2.26 (gas) / 2.57–2.72 (liquid) |
| gland_plate_2p6 | 1.78 | 1.30 × 2.60 | 0.0 % | 27 (21–33) | 74 / 85 / 86 at 60 °C | depth 1.27–1.37, width 2.13–2.26 (gas) / 2.57–2.72 (liquid) |
| rod_2_114 | 2.62 | 2.06 × 3.60 | 0.0 % | 21 (17–26) | 73 / 80 / 83 at 110 °C | rod |

## Closure forces (FKM 75A: E = 7.05 MPa from Gent; Lindley load per length)

| Closure | Seal | Squeeze force | Parker Fig. 2-x range at 25 % | Available |
|---|---|---|---|---|
| Lid | 3.53 mm, 978 mm long, 25 % | 4103 N (4.19 N/mm) | 2.19e+03–9.42e+03 N | 20 × M5: ≥ 48 kN; vacuum 5907 N |
| Door, as drawn (3.53 mm) | 3.53 mm, 669 mm long, 25 % | 2805 N (4.19 N/mm) | 1.50e+03–6.44e+03 N | vacuum 2445 N; 2 latches rated 3558 N each |
| Door, 3.53 mm at 15 % | 3.53 mm, 669 mm long, 15 % | 1219 N (1.82 N/mm) | – | +20 mbar pushes out 48 N |
| Door, 1.78 mm at 25 % | 1.78 mm, 669 mm long, 25 % | 1414 N (2.11 N/mm) | 890–2.46e+03 N | vacuum 2445 N |
| Door, 1.78 mm at 15 % | 1.78 mm, 669 mm long, 15 % | 614 N (0.92 N/mm) | – | latch preload needed at +20 mbar |
| Drawer | 1.78 mm, 163 mm long, 25 % | 345 N (2.11 N/mm) | 217–601 N | +20 mbar pushes out 2.4 N; nothing clamps it |
| Window (sandwich) | 1.78 mm, 139 mm long, 25 % | 294 N (2.11 N/mm) | 185–511 N | +20 mbar lifts 3.3 N vs weight 0.35 N |

## Permeation (Parker §3.12.1) into the argon loop

Arrhenius temperature scaling with E_a = 37 kJ/mol (Parker's He pair; the N₂ pair gives 58).

| Seal | T (°C) | O₂ (sccs) | H₂O (sccs) |
|---|---|---|---|
| lid | 50 | 9.61e-07 | 1.57e-06 |
| door | 45 | 5.31e-07 | 8.69e-07 |
| window (sandwich, inner ring) | 60 | 2.09e-07 | 3.43e-07 |
| window flange to lid | 60 | 3.78e-07 | 6.20e-07 |
| camera adapter + its window | 45 | 1.51e-07 | 2.47e-07 |
| metering base to lid | 45 | 2.15e-07 | 3.52e-07 |
| reservoir dock face (proposed) | 45 | 2.29e-07 | 3.75e-07 |
| reservoir lid (proposed) | 45 | 2.53e-07 | 4.14e-07 |
| drawer | 50 | 1.57e-07 | 2.57e-07 |
| plenums (2) | 45 | 5.44e-07 | 8.91e-07 |
| KF-25 (7) + KF-40 (2) + KF-16 (1) centering rings | 35 | 4.49e-07 | 7.36e-07 |
| spigot 2-238 | 56 | 4.46e-07 | 7.30e-07 |
| gland plate | 45 | 1.39e-07 | 2.28e-07 |
| rod gland 2 x 2-114 (in tandem: the outer one carries the gradient) | 117 | 6.54e-07 | 1.07e-06 |
| **Total** | | **5.32e-06** | **8.71e-06** |

Gas envelope 11.3 L (chamber 6.4, hoses 1.5, filter housing 2.3, plenums and blower 1.1).
Permeation alone adds **1.67 ppm O₂/h** and 2.73 ppm H₂O/h with no make-up flow.
Outgassing of 4605 cm² of bare Al and 18 cm² of exposed FKM after ~1 h: 3.68e-05 + 2.37e-05 mbar·L/s, **19 ppm H₂O/h**, falling roughly as 1/t.
150 g of powder holding 50–300 ppm water by mass carries 8–45 mg: **829–4971 ppmv** in the loop if a 200 °C plate drives it off.

Make-up argon to hold the targets at steady state: 35.4 sccm for 10 ppm O₂ against permeation; 33 sccm for a −40 °C dew point against wall and seal outgassing.

Other leak sources (air at 1 atm, mbar·L/s; vendor-typical ranges):

| Source | Range | Fix |
|---|---|---|
| 2 rotary shafts through elastomer V-rings / lip seals (recoater screw, metering roller) | 1.00e-05–1.00e-03 | magnetic-fluid feedthrough (helium leak < 1e-10 mbar L/s class) or a magnetic coupling through a can (zero leak) |
| rod gland, 2 x 2-114 reciprocating | 1.00e-06–1.00e-04 | edge-welded bellows over the rod |
| potted stranded leads at the rod end | 1.00e-05–0.01 | glass-to-metal hermetic connector or KF feedthrough |
| threaded NPT ports (5-8 joints) | 1.00e-06–1.00e-03 | O-ring boss / VCR / KF |
| gas-tight side-channel blower, shaft seal | 1.00e-04–1.00e-03 | hermetic (canned / magnetic-drive) blower |

## Vacuum purge

Pump 4396K21: 1.42 L/s displacement; through two KF-25 bellows S_eff = 1.42 L/s at 800 mbar, 1.40 at 10 mbar, 1.28 at 1 mbar. **Pump-down to 1 mbar: 0.9 min**; time constant at atmosphere 8.0 s.

| Cycle (pump to 1 mbar, back-fill Ar 5.0) | O₂, ideal (ppm) |
|---|---|
| 1 | 207.81 |
| 2 | 1.20 |
| 3 | 1.00 |
| 4 | 1.00 |

### Powder beds while pumping (Kozeny–Carman k = 4.01e-12 m², Klinkenberg slip; U_mf = 2.8 mm/s)

| Bed | depth (mm) | Δp / bed weight at 1 atm | at 10 mbar | τ = V/S needed for ≤ 0.3 (s) |
|---|---|---|---|---|
| reservoir L (56 mm of powder) | 56 | 0.59 | 0.19 | 16 |
| build cylinder, end of build (40 mm) | 40 | 0.42 | 0.14 | 11 |
| overflow jar (90 mm) | 90 | 0.95 | 0.31 | 25 |
| reservoir M (40 mm) | 40 | 0.42 | 0.14 | 11 |

Reservoir as drawn (open to the room through the powder column): at +20 mbar, **299 sccm of argon leaves through the powder** at 8.9 mm/s superficial velocity, against a minimum fluidization velocity of 2.8 mm/s. Pumping down, room air comes in at ~9431 sccm.

## Rate-of-rise acceptance test

Leak budget 1.00e-04 mbar·L/s in 11.3 L is a rise of 5.33e-04 mbar/min; outgassing after ~1 h adds 3.23e-04 mbar/min. isolate at <= 1 mbar after >= 1 h pumping; read a Pirani or capacitance gauge for 10 min.

## Sources

1. Parker O-Ring Handbook ORD 5700: Design Chart 4-3 (face glands), Design Table 4-2 (static radial glands), §3.11 vacuum sealing and Table 3-20 (finish), §3.12.1 leak-rate approximation and Fig. 3-11 (Q), Table 3-24 (permeability), Figs. 2-4..2-6 (compression load). https://nfc.arizona.edu/sites/default/files/2022-02/parker_o-ring_handbook.pdf
2. Lindley, P. B. (1967). Compression characteristics of laterally-unrestrained rubber O-rings. J. Inst. Rubber Ind. 1, 209-213 (F/L = d E (1.25 e^1.5 + 50 e^6)); as used in e.g. https://doi.org/10.1016/j.triboint.2019.106062
3. Gent, A. N. (1958). On the relation between indentation hardness and Young's modulus. Trans. IRI 34, 46-57 (E [MPa] = 0.0981 (56 + 7.62336 S) / (0.137505 (254 - 2.54 S)))
4. Marco Rubber, O-ring permeation (FKM: H2O 40e-8 std cc cm/cm2 s bar): https://www.marcorubber.com/o-ring-permeation.htm
5. O'Hanlon, J. F. A User's Guide to Vacuum Technology, 3rd ed. (Wiley, 2003), Table 4.5 and App. C.5: outgassing of unbaked Al ~6e-9 and Viton A ~1e-6 Torr L/s/cm2 after 1 h; and Ch. 2-3 (viscous conductance, C = 135 d^4 p/L for air)
6. Kozeny-Carman permeability k = d^2 e^3 / (180 (1-e)^2); Klinkenberg (1941) slip k_a = k (1 + b/p), b = 4 c lambda p / r with c ~ 1 (API Drilling and Production Practice, 200-213)
7. Ergun minimum fluidization: U_mf = (rho_p - rho_g) g d^2 e^3 / (150 mu (1 - e)) for small particles (Kunii & Levenspiel, Fluidization Engineering, 2nd ed., Ch. 3)
8. McMaster-Carr 4396K21 (3 cfm, 1e-2 Torr) and the parts in ../../mcmaster-parts.csv, read through the lab Pi 2026-11-17
9. Airgas/Linde argon 5.0 (UHP) typical limits: O2 <= 1-2 ppm, H2O <= 1-3 ppm
