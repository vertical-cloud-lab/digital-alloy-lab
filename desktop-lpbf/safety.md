# Safety review of the desktop LPBF cell: laser, argon, aluminium powder, hot plate, robot

Written 2026-11-20 for [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), after the PI asked for "safety features and general laser safety, gas safety, etc. Especially what's published at BYU but also general resources, handbooks, tutorials". It verifies and extends [Edison's safety review](edison/r3-safety/answer.md). Nothing here has been seen by BYU's Laser Safety Officer (LSO), Fire Marshal or Environmental Health and Safety. It is a design-review input, not an approval.

| File | What it is |
|---|---|
| [`safety_calcs.py`](safety_calcs.py) | every number below, with each input tagged as published, from this repo, or assumed. Run it with `/tmp/venv/bin/python desktop-lpbf/safety_calcs.py` |
| [`safety-parts.csv`](safety-parts.csv) | 33 real parts for the gaps, with price, basis and fetch time |
| [`notes/2026-11-20-safety-sources.md`](notes/2026-11-20-safety-sources.md) | each source: URL, fetch time, how it was read, and what it says |

## 1. The short answer

**The design has the right skeleton and four holes that matter.** It already has a hardwired interlock chain, a guard lock, a shutter and dump, a key switch, emission lights, E-stops, a latching plate-temperature limit with a 240 C cutoff, a 50 C door gate, an O2 permissive and a Class D extinguisher. What it lacks:

1. **A fixed oxygen monitor.** BOM line S7 (McMaster 18995T81, $459) is a *portable* detector with a two-year non-replaceable battery. Nothing watches the Kardex shaft.
2. **A limit on how much argon a fault can release.** The machine holds only 18 L of argon, which is harmless. The *supply* is the hazard: a size-80 cylinder (2.4 m³) takes an unventilated 30 m³ room to 19.3 % O2, and a size-300 cylinder (9.5 m³) takes it to 15.3 %. Inside the Shuttle's ~24 m³ of free air the same cylinders give 19.0 % and 14.2 %.
3. **A safety controller with enough inputs.** The Omron G9SE-201 ($275) cannot take guard, two or three E-stops, key, shutter feedback, two O2 channels, plate-below-50 C, module-present, VLM and robot signals. A programmable safety controller (Banner SC26-2 class, about $1,770) can.
4. **A written passivation and bag-out method for the filter and cyclone.** The README says "passivated in a controlled way" but gives no procedure, no air-admission limit and no bag-out kit. The filter cake is the most likely fire in this machine.

Smaller gaps: no sonic orifice or rated relief on the argon line, no exhaust duct for the pump and relief outlets, no bonding points, no laser warning signs, no respirator or flame-resistant clothing, no module-present laser inhibit, no aspirating smoke detection in the Shuttle.

**BYU publishes less than hoped.** Its Risk Management and Safety site lists 35 safety programs, including Laser Safety, Machine Guarding, Lockout Tagout, Hot Work, Respiratory Protection and Electrical Safety. **Every program page is behind BYU's CAS login**, so none could be read. The open pages give the contacts by role, the fire-extinguisher and fire-code scope, the hot-work permit checklist, and a 2013/2020 chemical hygiene plan with compressed-gas rules. BYU has **no listed program for compressed gas, combustible dust, oxygen deficiency or robots**. Someone with a BYU account should read the gated pages (§3).

## 2. The top risks, ranked

| # | Risk | Why it ranks here | What bounds it | Section |
|---|---|---|---|---|
| 1 | **Argon asphyxiation in the Shuttle or the room** | Death in 5-8 minutes below 6 % O2, and no warning; argon pools low; a supply fault, not the machine, supplies the gas. Fully credible on a long dock line | fixed O2 monitors (room, shaft, bay) that close the argon valve; a sonic orifice; ducted exhaust; the smallest cylinder, kept outside | §5 |
| 2 | **Filter and condensate fire** | Condensate has MIE < 1 mJ and ignites on air admission; aluminium plus water gives hydrogen; a fire inside a VLM is hard to reach | inerted, valved-off filter, slow air admission with a thermocouple, two people, sand, Class D, no vacuuming of fresh condensate | §7 |
| 3 | **Class 4 beam outside the machine** | 500 W at 1070 nm is invisible; the NHZ off the f-theta runs to 114 m; bare fibre 25 m; diffuse 0.6-1.3 m; a stalled galvo is a stationary beam | opaque guard, shutter, module-present inhibit, alignment at reduced power, eyewear OD, SOP | §4 |
| 4 | **Robot reaches in while something is live** | Hot plate (200 C), open guard, powder, laser, argon and a mobile base share one handoff | one permissive that includes laser off, plate < 50 C, argon closed, O2 good, VLM stopped, MiR parked | §9 |
| 5 | **Aluminium dust cloud or layer** | AlSi10Mg is an explosible St 1 dust (Kst 151 bar m/s, Pmax 6.1 bar, one test); finer fractions are worse | enclosed transfers, bonding, combustible-dust vacuum, DHA | §7 |
| 6 | **Vacuum and overpressure** | Chamber, window and door are sized with margin (window SF 48 at 1 atm). 650 J if it implodes | a rated relief, window retention, particle trap on the pump | §6 |
| 7 | **Electrical** | 7.9 A at 240 V for the laser; 14.6 A at 24 V for the heaters | LOTO, fused heater legs, bonded chassis | §8 |

## 3. What BYU publishes

Read on 2026-11-20 (details and times in the [source log](notes/2026-11-20-safety-sources.md) §1).

| Topic | What BYU publishes, in the open | What is behind login or missing |
|---|---|---|
| **Laser safety: LSO, registration, SOPs, training, eyewear** | The Safety and Health Programs index lists a **Laser Safety** program, owned by the "Program Manager: Lab, Laser, and Radiation Safety". A BYU research group's page gives only general laser etiquette. | The program page itself, the registration form, any SOP template and the eyewear rule: all gated. **Not read.** Stanford's manual shows what a program usually requires: register every Class 3b and 4 laser with the LSO (again after major modification), a written SOP that includes alignment, job-specific training, eyewear chosen for direct and diffuse beams, key control, interlocks and a remote interlock connector. |
| **Compressed gas cylinders** | The chemical hygiene plan (Jan 2013, reviewed Dec 2020): "Always use the smallest size cylinder required"; carts "capped and secured by an approved cylinder support strap or chain"; every uncapped cylinder secured on its own; "never bleed a cylinder completely empty"; a leaking cylinder may need evacuation and "only appropriately trained hazmat responders" stop it. | No separate compressed-gas program is listed. |
| **Asphyxiants and O2 monitoring** | "Do not store cryogens or dry ice in non-ventilated rooms." Confined Spaces is a listed (gated) program. | No oxygen-deficiency or argon rule, and no O2-monitor requirement, found. OSHA's 19.5 % applies regardless. |
| **Reactive or combustible metal dust** | The chemical hygiene plan covers pyrophorics ("store and use ... in an inert atmosphere") and water-reactive materials generally. BYU science buildings carry large yellow extinguishers "for combustible metals (magnesium, potassium, etc)". | No combustible-dust or NFPA 484/652 program. **BYU's own metal-AM lab (a Concept Laser M2 that runs aluminium) already exists on campus: ask it for its SOPs and dust hazard analysis.** |
| **Chemical hygiene** | The plan itself: written protocols and training for research-specific hazards, near-miss reporting, respirators only inside a respiratory protection program. The Fulton College keeps a Laboratory and Shop Safety Plan, a hazard checklist, a risk matrix and an SOP template. | The college plan is on a private share link: not read. |
| **Machine guarding and robotics** | Machine Guarding sits under the "Program Manager: Electrical, Fall, and Equipment Safety". | Page gated. No robot or cobot standard found. |
| **Electrical and lockout/tagout** | Electrical Safety and Lockout Training are listed programs, same manager. | Both pages gated. |
| **Hot work** | The permit form: no alternative to hot work; flammables within **35 ft** removed or shielded; correct extinguisher; fire watch for **1 hour** after plus a monitor for **3 more hours**. Hot work is "prohibited ... unless authorized in writing" by the RMSD managing director or the university fire marshal. | It does not mention lasers. Treat laser-melting aluminium powder as a question for the Fire Marshal, not as a hot-work permit. |
| **Building and fire code** | The Fire Marshal Office does "fire and life safety code interpretation, inspection and enforcement on new and existing buildings", plan reviews and extinguishers: "an extinguisher within 75 feet". Under the IFC and NFPA 1, powder-bed AM equipment must be listed to UL 2011 or field-evaluated (UL). | No published list of hazardous-materials control-area limits for aluminium powder. |

**Who to talk to first, by role:**
1. **The Program Manager for Lab, Laser and Radiation Safety (the LSO's office):** register a Class 4 laser before first light; get the SOP template; ask whether they will classify the enclosed machine as Class 1 in operation; agree the eyewear and alignment rules.
2. **The Fire Marshal Office:** the dust hazard analysis and its edition of NFPA 484/652/660, whether a UL 2011 field evaluation is needed, the Class D plan, powder storage limits, and what to do about a fire inside a Kardex Shuttle.
3. **Health and Exposure Controls:** the respirator program, fit testing, and O2 monitoring for argon.
4. **Electrical, Fall and Equipment Safety:** lockout/tagout, machine guarding and the robot cell.
5. **The BYU metal-AM lab and the Fulton College health and safety officer.**
6. **Kardex:** written approval for a Class 4 laser, argon, 2.7 kW of heat and powder inside the Shuttle (§10).

## 4. Laser

### 4.1 What applies

| Document | What it does for us | Free to read? |
|---|---|---|
| **ANSI Z136.1** (safe use of lasers) | The user standard: classification, MPE, NHZ, eyewear OD, SOPs, training, LSO. The basis of every university manual. | No. The NIU and Stanford manuals reproduce the working parts |
| **ANSI Z136.9** (manufacturing environments) | Same, for industrial laser work; useful where a research machine is run like a production cell | No |
| **IEC 60825-1** | Product classification and accessible-emission limits | No |
| **IEC 60825-4:2022** | Laser guards: passive guard testing, interlocks, labels | No (preview only) |
| **ISO 11553-1** | Safety of laser processing machines | No |
| **21 CFR 1040.10 and .11** | Federal laser product standard. Class IV needs a protective housing, interlocks, a **key**, an **emission indicator**, a **beam attenuator**, a **remote interlock connector** and a **manual reset after an interlock stop or a power loss over 5 s** | Yes. The page applies to products "manufactured or assembled after August 1, 1976" and has **no sentence exempting a machine built by its user**. The README's claim that such a laser is exempt comes from university manuals (Northwestern: "home-made lasers used by their designers are not subject to the requirements of the FLPPS, but must be classified per ... ANSI Z136.1"). Treat it as the working position and ask BYU's LSO. It ends if the machine is ever given or sold. |

For a lab-built machine used in-house the practical test is the one the BOM already follows: **build to the FDA Class IV list, classify under Z136.1, register with the LSO, and make the enclosure meet Class 1 (IEC 60825-4) in operation**, then treat service with the guard open as Class 4.

### 4.2 The numbers (`safety_calcs.py` §1)

Inputs: 500 W CW, 1070 nm, M² 1.1, 5 mm collimated beam, f = 160 mm (the low-profile layout; the README's block diagram still says 254 mm).

| Quantity | Value | Source of the method |
|---|---|---|
| MPE, eye, t ≥ 10 s | **5 mW/cm²** (5 CC mW/cm², CC = 1) | NIU manual, from Z136.1 |
| MPE, skin, t ≥ 10 s | **1.0 W/cm²** (0.2 CA, CA = 5) | same. A 500 W beam on 1 cm² is 500 times this |
| Class 1 accessible emission | **~1.9 mW** (MPE through a 7 mm pupil) | derived |
| Focused spot (M² 1.1, 5 mm beam, f = 160) | 48 µm diameter, Rayleigh range 1.5 mm, 5.5 × 10⁷ W/cm² | estimate |
| **NHZ**, collimated 5 mm beam | **11.9 km**: everything in line of sight | Z136.1 NOHD form |
| NHZ, direct beam through the f-theta (31 mrad full angle) | **114 m** from the focus | same |
| NHZ, specular off bare Al plate (R 0.9, assumed) | 108 m | same |
| NHZ, **bare fibre end** (140 mrad, IPG spec) | **25 m** | same |
| NHZ, diffuse off powder (ρ 0.5 / 0.1) | **1.3 m / 0.56 m** | Lambertian |
| **Eyewear OD**, direct 500 W | **≥ 5.4** (OD 6 minimum, 7 for margin) | OD = log₁₀(H₀/MPE) |
| Eyewear OD, alignment at 50 W / 5 W | ≥ 4.4 / ≥ 3.4 | same |
| Guard window or filter OD for Class 1 behind it | **≥ 5.4** at 500 W; OD 7 passes 50 µW, 38 times under the limit | same |

What the numbers mean:
- **Alignment, not operation, is the exposure.** A direct 500 W beam puts 13,000 kW/m² on eyewear; eyewear is tested for seconds at its rated power density. So **never let eyewear be the only control**: align at the lowest stable power (an assumed 50 W, check IPG's minimum) or with the 0.1-1 mW red guide laser, with a beam block or the dump in the beam.
- **A bare QBH output is a 25 m hazard.** Unplugging the fibre with the laser enabled is the worst service error; the interlock must also stop emission when the fibre is disconnected or the head is removed.
- **A stalled galvo is a stationary beam.** Z136.1 gives no credit for scanning. The guard and chamber must survive a stationary spot.
- **Aluminium back-reflection** is a risk to the laser and the optics, not only to people. The IPG spec sheet does not state a back-reflection rating: IPG still owes that in writing (BOM L1).

### 4.3 Does the guard survive a stationary beam? (`safety_calcs.py` §2)

Edison's historical IEC 60825-4 test times are 30,000 s (T1), 100 s (T2) and 10 s (T3), that is 15 MJ, 50 kJ and 5 kJ at 500 W. A screening model gives these bounds (not survival times):

| Sheet, spot | Lower bound on burn-through (1-D, no conduction) | Thin-sheet steady state |
|---|---|---|
| Any sheet at or near focus | 0.02 ms to 0.05 s | breached |
| **Al 5052 1.6 mm** (BOM guard), 150 mm from focus | **0.17 s** | melts only if absorptance rises from the cold 0.08 toward 0.4 |
| Al 5052 1.6 mm, 500 mm from focus (w 7.8 mm) | 1.9 s | does not melt in steady state |
| Al 5052 3.0 mm, any position | 0.3-3.5 s | does not melt in steady state |
| Steel 304 or mild steel, 1.5-2 mm, defocused | 0.3-5 s | melts (low conductivity) |
| Polycarbonate viewing panel (rated 102 kW/m² for 100 s, T2) | – | **5-5,100 times its rating** if the beam or a 10 % specular reflection reaches it |

- A **1.6 mm aluminium guard is plausible as a second barrier but not proven**; the answer depends on absorptance, which changes as the surface oxidises or soots. Only a test on the finished panel, at worst-case focus, decides.
- The **chamber is the primary barrier**: 12.7-16 mm 6061 walls and lid are ten times the thickness of the guard sheet.
- **The polycarbonate panel must never see the beam.** The design already says so (no chamber viewport, beam inside an opaque chamber); keep a labyrinth or baffle between any beam path and the panel, and prefer an absorbing glass filter.
- **Interlock response is cheap.** A 20 ms path (relay plus shutter) lets 10 J reach a stationary spot against a 5 kJ T3 budget. A 100 ms path lets 50 J. The shutter and the laser's inhibit should both fire from the safety controller.

### 4.4 Interlocks and the laser's safe state

| Function | Design |
|---|---|
| Guard position | Two-channel, monitored, coded actuator on the sliding door, separate from the lock (ISO 14119 defeat resistance) |
| Guard lock | Locked while the laser is enabled, the chamber is off atmospheric pressure, or the plate is above 50 C (already in the design). Use a **power-to-lock** design: a spring-lock switch unlocks on power loss |
| Laser enable | Safety controller output to the laser's interlock input **and** a normally-closed monitored shutter **and** a software inhibit; a laser-source interlock connector alone is not a two-channel function |
| Emission indicator | Beacon outside the room and on the guard, driven by the controller (CFR (f)(5)) |
| Key switch | Master key; remove it to inhibit (CFR (f)(4)) |
| Reset | Manual, outside the hazard zone, after any interlock stop or a power loss over 5 s (CFR (f)(10)) |
| Module-present | Laser enable requires the build module in its port, the plate present and the cover slide in place (new; §11 P1) |
| Fibre-present | Fibre connected and the head in place (new) |
| E-stop | Drops laser enable, shutter, scanner and recoater motion and the heater contactor. It does **not** vent or close the chamber: the argon valve closes on an O2 alarm instead, and the guard stays locked until the plate is below 50 C and the chamber is at ambient. The SOP covers this (§12) |

## 5. Argon, gas and oxygen

### 5.1 Inventory and releases (`safety_calcs.py` §3)

- **Machine:** chamber 6.4 L (280 × 190 × 120 mm), loop 10 L (the low-profile layout's number), voids ~2 L (assumed): **18.4 L of argon**. A start-up (three backfill cycles plus the loop) sends about **38 L** through the pump exhaust.
- **Releases from a supply fault** (room 30 m³ is Edison's hypothetical; Shuttle free air 24 m³ is 70 % of the 2.83 × 3.12 × 3.95 m enclosure from byu-vcl PR 318, an assumption because Kardex publishes no interior volume):

| Release | into 30 m³ room | into Shuttle (24 m³) |
|---|---|---|
| Machine inventory (18 L) | 20.9 % O2 | 20.9 % |
| Size-80 cylinder (85 ft³, 2.4 m³) | 19.3 % | 19.0 % |
| Size-125 (3.6 m³) | 18.6 % | 18.1 % |
| Size-200 (7.1 m³) | 16.5 % | 15.7 % |
| **Size-300 (336 ft³, 9.5 m³)** | **15.3 %** | **14.2 %** |
| 180 L liquid cylinder (143 m³) | 0.2 % | 0.1 % |
| Argon needed to reach 19.5 % O2 | 2.15 m³ | 1.75 m³ |

- **One tray bay** (1.47 m³, half free) is the first-minutes case: 0.05 m³ of argon takes still air in it to 19.5 %, and **the machine's own 18 L would drop it to 20.4 %**. Argon is 1.38 times denser than air: 2.4 m³ spread on the Shuttle floor is 0.5 m deep.
- **The leak rate sets how long you have.** Sonic flow through a 1 mm hole at 7 bar is 47 L/min (19.5 % in the room in 46 minutes); 4 mm at 7 bar is 750 L/min (3 minutes); 4 mm at 150 bar from a cylinder is 14,000 L/min (seconds). **Put a critical-flow orifice (0.5-1 mm, 12-47 L/min) in the supply line**, downstream of the shutoff and upstream of everything inside the Shuttle, so a failed regulator cannot dump a cylinder.
- **Ventilation holds the limit against a leak:** it needs 13.4 times the leak flow. The ducted exhaust that [`heat.md`](heat.md) already proposes for the laser (1.2 kW, 5 K rise: ~720 m³/h) would hold 19.5 % against a 890 L/min leak, **if it runs whenever argon can flow and exhausts outside the Shuttle.**

### 5.2 Monitors, set points and placement

OSHA defines an oxygen-deficient atmosphere as one "below 19.5 % by volume" (29 CFR 1910.134). LBNL's effects table: < 17 % fatigue; < 16 % dizziness; < 15 % impaired judgement; < 12 % unconsciousness possible; < 6 % death in 5-8 minutes. NIST's metal-AM lab warned at 19 % and evacuated at 17 %; Edison proposes earlier points and this review keeps them.

| Level | Action |
|---|---|
| **20.0 %** | Local horn and strobe; controller logs it; ventilation to high |
| **19.5 %** | Latching evacuation alarm; **argon valve closes** (the NC solenoid, from the controller); laser and heaters inhibit; exhaust to maximum; no entry |
| **Sensor fault or lost signal** | Treated as 19.5 % |
| **Reset** | Only after the cause is found and O2 ≥ 20.5 % for 5 minutes at every sensor |

Placement, because argon pools and mixes slowly: **two sensors in the room** (about 0.3 m and 1.5 m above the floor, one near the cylinder); **two in the Shuttle** (one low at the shaft floor, one at the tray bay); a **personal monitor** for whoever is at the machine. LBNL notes floor O2 can be below 15 % while breathing height reads above 20 %. Fixed part: Macurco OX-6 (0-25 %, 4-20 mA, two relays; $663 from an extract, list $1,275). The BOM's 18995T81 ($459) is the personal monitor. Dispersion should be checked once, with a puff test, not assumed.

### 5.3 Cylinders and lines

BYU's chemical hygiene plan: smallest cylinder, strap or chain, never empty. So: **a size-80 or smaller cylinder, chained outside the Shuttle and outside the room if the building allows**, a two-stage regulator with a 0-5 psi delivery stage, the sonic orifice, an NC shutoff at the cylinder and one at the dock, a check valve, and leak-tight stainless line to the machine. A P100 respirator gives no oxygen (OSHA APF table; Spelce 2016): **nobody enters an oxygen-deficient bay**.

### 5.4 Overpressure relief (`safety_calcs.py` §3b)

- The door sees 48 N at +20 mbar and 483 N at +200 mbar over its 241 cm²; the two draw latches are rated 3.56 kN each. The lid has a 16 mm 6061 plate, 20 M5 screws (≥ 48 kN) and 5.4 kN of atmosphere at vacuum. **The structure takes a full bar of overpressure; the seals and window retention are the limit.**
- The BOM's relief is McMaster 4277T52: 0.5 psi (34.5 mbar), set accuracy ± 20 %, opens at 28-41 mbar, fully open at about 30-46 mbar, **Cv "Not Rated"**, nylon, made for air. It is the right set point and an unrated device.
- With a sonic orifice limiting the supply to 12-47 L/min, a relief of **Kv ≥ 0.14-0.56 (Cv ≥ 0.16-0.65)** holds +50 mbar; the unrated 4277T52 may or may not. Without the orifice, a 300 L/min failure needs Kv ≥ 3.6 and 3,000 L/min needs Kv ≥ 36. Use **a rated spring relief (KF-40, Accuglass PRV-K40, $460)** as the second stage and, if wanted, a KF-40 burst disc (9-11 psi, $1,381) as the last resort. Pipe every outlet out of the room and the Shuttle.

## 6. Vacuum, window and implosion (`safety_calcs.py` §4)

- **Window:** Ø50.8 × 8 mm fused silica on a Ø48 seat. Peak stress 1.08 MPa (Roark; the repo's CalculiX run gives 1.15), safety factor **48** against 52.4 MPa. 2.8 mm would give SF 6. The force on it at full vacuum is 183 N.
- **Lid and door:** 5.4 kN (5.9 kN counting the gland) and 2.4 kN at full vacuum, matching [`seals.md`](seals.md). The door's draw latches carry nothing at vacuum; at +20 mbar each needs 725 N of preload for 25 % squeeze.
- **Implosion:** the stored energy is about p·V = 650 J for 6.4 L, an upper bound, not a window-fragment energy. The window is a thick glass disc with a metal retaining ring (seals.md fix): confirm the ring holds fragments, and keep the vacuum gauge on the safety display. Do not open the door until the chamber has equalised.
- **Pump exhaust:** pump-down lifts powder (seals.md). Fit a particle trap on the pump inlet and vent the exhaust through a duct, not into the bay.

## 7. Aluminium powder, condensate and fire (`safety_calcs.py` §5)

### 7.1 What is known

- **AlSi10Mg:** one test reports **Pmax 0.61 MPa (6.1 bar), Kst 151 bar·m/s (St 1), MIE 80 mJ** (Sun 2023, read via Edison; the table is an image). Another study: alloys MIE 13-23 mJ, 5-7 bar, 250-360 bar/s; pure Al 4 mJ. Atomised Al: Kst 64-274 bar·m/s, Pmax 3.3-11.8 bar (finer is worse; > 38 µm usually Kst < 100).
- **Filter-collected Al** (D50 ~5 µm): MIE < 3 mJ; filter Kst 2-3 times the bulk (Edison, Scotton 2026). **LPBF condensate:** "very low minimum ignition energy (< 1 mJ)", unoxidised, and "if a chemical reaction ... occurs ... it can be expected to develop slowly. First, the condensate on the filter surface is oxidized ... Then, the fabric of the filter may ignite" (EOS notice).
- **The numbers depend on the sample.** The dust hazard analysis (DHA) must test this lab's virgin, used, spatter, cyclone and filter samples; none of the published values transfers to Al-Mg-Sc or a grain-refined 6xxx/7xxx.
- **Inventory:** the S / M / L reservoirs hold 53 / 136 / 326 g (assumed 1.4 g/cm³). Dispersed in a 30 m³ room that is under 11 g/m³, below the tens of g/m³ at which Al dust clouds propagate (from memory: the AlSi10Mg MEC is in Sun's table, unread). The risk is **layers, the filter and open handling, not a room cloud.** 0.33 kg spread 0.8 mm deep covers 0.3 m².

### 7.2 Filter and cyclone: the controlled-oxidation window

- Aluminium oxidation releases **31 MJ/kg**: 10 g of condensate is 311 kJ. Air admitted at 0.1 / 0.3 / 1 / 3 L/min, fully consumed, is **16 / 49 / 163 / 488 W**. A 0.1 m² steel housing sheds about 50 W at 50 K rise. So **admit air at no more than ~0.3 L/min into the sealed housing, or better step the oxygen in argon (0.1 %, 1 %, 5 %, 21 %) with a thermocouple in the cake, pausing at each step until the temperature falls.** These steps are an estimate for the DHA to confirm; no published aluminium-specific procedure was found.
- **Water:** Al plus water gives 1.25 L of hydrogen per gram of Al. A wet separator needs venting and a hydrogen assessment; filters wetted with water before removal (a patent) need the same.
- **Other practice from the literature:** transfer dry condensate into an airtight bin with sand and silicone oil (Sintavia); cool the filter first; two people; PPE; sand tub and extinguisher at hand (EOS).
- **Do not vacuum fresh condensate.** Passivate it first, then vacuum with a combustible-dust vacuum.

### 7.3 Vacuum, grounding, PPE and storage

| Item | Requirement |
|---|---|
| **Vacuum** | Rated for the dust: Class II Div 1 Groups E, F, G (Group E is aluminium and magnesium). McMaster 5572N116 ($3,190) in the BOM qualifies and needs 35 scfm of dry air; alternatives are the Dynabrade 61496 water-immersion unit ($6,648) and PrestiVac EV2-15 EX ($8,283) |
| **Grounding and bonding** | Chamber, lid, door, filter housing, cyclone, reservoir dock, drawer, pump and exchange pail bonded to a bus bar and to building ground. Check continuity each shift (target ≤ 10 Ω to ground; conductive hoses and containers < 1 MΩ: values from NFPA 77 as usually quoted, to be confirmed) |
| **PPE** | Full-facepiece P100 for chamber opening, powder and filter work (HEPA 99.97 % at 0.3 µm; APF 50), fit-tested and medically cleared **inside BYU's respiratory program**; FR coveralls; thermal gloves for 200 C parts; conductive footwear; no synthetic outer layers |
| **Storage** | Closed, grounded, dry containers; Al and Mg powders away from water, acids and oxidisers; Mg-bearing powders apart from the rest; limits from BYU's Fire Marshal. Argon, never nitrogen, for Mg (the lab's rule) |
| **Fire** | Class D (BOM S8, McMaster 6435T23, sodium chloride 30 lb, $920) outside the Shuttle; dry sand; no water, CO₂ or ordinary compressed-air blow-off on a metal fire. BYU's science buildings carry yellow Class D units; ask the Fire Marshal what the lab is expected to hold |
| **Codes** | NFPA 484 (AM chapter: DHA, emergency shutdown, part harvesting, powder storage, training, emergency response), NFPA 652/654, consolidated in **NFPA 660 (2025)** per Edison: ask which edition BYU's Fire Marshal enforces. IFC and NFPA 1 require UL 2011 listing or a field evaluation; NEC Article 670 and Articles 500-503 apply to the install |

### 7.4 Lessons from incidents (as Edison found them)

NIST's metal-AM lab had no filter fire but flagged filter changes as the main hazard. AL Solutions (2010, zirconium dust) and aluminium-finishing deflagrations that propagated through ducts show what housekeeping and unisolated collectors do. OSHA's willful citation after the 2013 Powderpart aluminium fire was for having no Class D extinguisher. Water on Al filter dust killed two people at an LPBF maker (pain-points P34).

## 8. Hot plate and electrical (`safety_calcs.py` §6-7)

- **Plate:** 200 C. Stored heat above 25 C: **19 / 43 / 95 kJ** (S25 / M50 / L75, assumed masses). Cool-down to 50 C from the FEA: 15 / 28 / 40 minutes. A bare metal contact burns in about 10 s at 55-60 C and in about 1 s at 65-70 C (recalled from ISO 13732-1 and ASTM C1055, to be checked), so **the 50 C release is a conservative gate**.
- **Layers already in the design:** control and edge thermocouples, an independent limit thermocouple into a latching CN708, a 240 C thermal cutoff in series with the heaters, and the door lock. **Add:** the CN708 output as a safety-controller input, a HOT lamp on the guard, a heat-rated landing pad for the plate in the drawer path, and a rule that the robot never carries a plate above 50 C unless the SOP says so.
- **240 V:** the laser draws up to 1.9 kVA (7.9 A at 240 V); the tray in the worst case 2.7 kW (11.2 A); the dock legs are limited to 24 A. **24 V:** L75's heaters are 250 W (10.4 A), the 350 W supply 14.6 A. 24 V DC is a low-voltage circuit, but a shorted cartridge lead is a fire: **fuse every heater leg** (about twice its 2.1 A) and size wire for the supply's short-circuit current.
- **Lockout/tagout:** the energies to isolate are 240 V, the laser's capacitors (vendor discharge time), the scanner and servo drives, the pump, argon (at the cylinder and at +20 mbar), vacuum, pneumatic clamps, the lift tray, and the hot plate (thermal). BYU's LOTO program is gated: get it. Fit a lockable disconnect at the dock and the machine.

## 9. The robot, the mobile base and the lift (`safety_calcs.py` §8)

- **Arm:** UR12e, 12.5 kg payload, 1,300 mm reach, up to 4 m/s TCP (UR). **Base:** MiR250, up to 2 m/s, payload up to 250 kg (MiR). The standards: ISO 10218-1/-2:2025 (robot, cell), ISO/TS 15066 (collaborative contact), ANSI/A3 R15.08-1/-2 (mobile robot maker and integrator), ISO 12100 (risk assessment), ISO 13849-1 (performance level), ISO 13855 (safety distance), ISO 14119 (interlock devices). They are paywalled; the values quoted here are from vendor pages and search extracts.
- **A collaborative arm is not a collaborative application.** The arm's force limiting says nothing about a hot plate, a sharp edge, a closing guard door, a powder jar or a moving base. An effective moving mass of ~13 kg (assumed) at 0.25 m/s carries 0.41 J and a spring-mass peak of ~350 N against a 150 N/mm contact (assumed stiffness); ISO/TS 15066 gives 29 body-region limits to compare against, which are not reproduced here. **Clamping against the machine or the Shuttle is not fixed by a force limit.**
- **Mobile-base stopping distance** (reaction 0.3 s, deceleration 0.5 m/s², both assumed; ask MiR): 0.18 m at 0.3 m/s, 0.9 m at 0.8 m/s, 1.8 m at 1.2 m/s, **4.6 m at 2 m/s.** Set a low speed zone near the Shuttle opening and in the aisle by the machine. ISO 13855: S = K·T + C (K 1,600 mm/s walking; for T = 0.3 s and C = 850 mm that is 1,330 mm).
- **The hand-off permissive.** Before the arm may open the guard or reach into the machine, **all** must be true and must be read through safety-rated inputs, not a network message: laser emission off and shutter closed; key in remote-safe; plate below 50 C; chamber at ambient and the argon valve closed; room, shaft and bay O2 ≥ 20.5 %; the Kardex tray stopped and locked; the MiR docked with brakes on; no person in the cell's scanned zone. **Loss of any one** (power, comms, O2 sensor, docking, localisation) goes to a defined safe state with no automatic restart.
- **Restrict the arm.** Use the UR's safety-rated planes and joint limits to keep the TCP out of the optics bridge, the f-theta and the scanner. The laser must not be enabled while the arm is inside the guard.
- **Kardex:** it has not published any approval for a Class 4 laser, argon, powder or heat in the Shuttle; Kardex and Fike recommend aspirating detection and inert-gas suppression for VLM fires (pain-points P51), and IG-100 is nitrogen, which is the wrong agent for Mg-bearing powder (the lab's argon rule). Write to Kardex for: tray and point loads, vibration, ventilation or exhaust, fire protection, moving utilities, and whether the lift can be commanded to a safe parking state on an O2 alarm.

## 10. Gap analysis against the current design

"BOM" lines are from [`bom.csv`](bom.csv). Parts for each gap are in [`safety-parts.csv`](safety-parts.csv).

| Feature | In the design now | Missing or wrong | Part to add |
|---|---|---|---|
| Room O2 monitor | S7 McMaster 18995T81 $459: **portable, 2-year battery** | A fixed monitor with relays | SP1 Macurco OX-6 |
| Shuttle and bay O2 monitors | – | Two, independent, low and at the tray bay | SP2 (×2) |
| Argon shutoff on O2 alarm | 2 NC solenoids (G7) | Not wired to O2 relay; one more at the supply | SP4 |
| Supply flow limit | – | Sonic orifice | SP5 |
| Chamber relief | G7 McMaster 4277T52, Cv not rated | A rated second stage, vented out | SP6, SP7, SP8 |
| Cylinder | 78595A5 regulator-flowmeter | Smallest cylinder, restrained, outside | SP9 |
| Pump exhaust | "vent outside the room" (README) | A duct, a flow switch and an interlock | SP10 |
| Warning signs and beacon | S4 key, indicator, reset, stack light | Class 4 sign and labels | SP11, SP12, SP13 |
| Guard lock | S2 Omron D4JL ($803, out of stock at fetch) | Confirm power-to-lock; spare option | SP14, SP15 |
| Safety relay | S1 Omron G9SE-201 $275 | Too few inputs | SP16 Banner SC26-2 class |
| E-stops | S3 IDEC XA1E ×2 | Three or more places, all into the controller | SP30 |
| Beam dump and shutter | L4 | Add a monitored shutter and a dump for every direction | SP17 |
| Viewing window | S5 Thorlabs LW1P1/M | OD ≥ 5.4 at 1070 nm and a damage rating, never in the beam | SP18 |
| Eyewear | S6 Thorlabs LG1 ×2 | Confirm OD and CW damage rating at 1070 nm | SP19 |
| Class D | S8 6435T23 $920 | Where it hangs; sand; ask the Fire Marshal | SP20, SP21 |
| Fire detection in the Shuttle | – | Aspirating detection (ask Kardex) | SP22 |
| Dust vacuum | A2 McMaster 5572N116 | Fine; add rules for using it | SP23, SP24 |
| Grounding | "ground and bond everything" (README) | Bonding points, a bus bar, a tester | SP25, SP26 |
| Filter bag-out | "passivated ... sand or oil" (README) | Kit and procedure | SP27 |
| Respirator and FR | – | Full-face P100, FR coveralls, gloves | SP28, SP29 |
| Plate limit | H2 CN708 latching, 240 C cutoff | CN708 output into the controller | SP31 |
| LOTO | – | Lockable disconnect | SP32 |
| Presence sensing on the aisle | – | Only if the MiR and Kardex do not cover it | SP33 |
| IPG back-reflection protection and interlock input | "not on the spec sheet" (quote) | Get it from IPG in writing | – |
| **Doc errors found** | README block diagram says f = 254 mm; S7 labelled a room monitor; FDA exemption stated as fact | Fix in the README | – |

## 11. Design changes to model (patch requests)

| ID | Where | Change | Why |
|---|---|---|---|
| P1 | Process module, Z-stage port and optics bridge | **Module-present, plate-present and cover-slide-present sensors** into the laser-enable chain (the A1 module sensor already exists; route it to the safety controller). Add a removable beam-stop cap for the Ø96 port when a module is out | The beam falls through the empty port during a module swap |
| P2 | Guard sliding door and panel overlaps | 20 mm minimum overlap or a labyrinth on every guard seam; a coded actuator **separate from** the lock; a power-to-lock locking switch | IEC 60825-4 leakage at seams; ISO 14119 |
| P3 | Guard front, viewing panel | Baffle so no beam path or specular reflection sees the panel; swap PC for an absorbing glass filter | PC is rated 102 kW/m² and can see 5-5,100× that |
| P4 | Guard front face and top | E-stop on the front, a **HOT** lamp tied to the CN708, a beacon on the top, Class 4 labels | Visible state |
| P5 | Gas and vacuum module, argon manifold | Add in order: NC shutoff, critical-flow orifice, 0-5 psi regulator, pressure switch, check valve; KF-40 port for a rated relief; second KF-40 for an optional burst disc | §5.4 |
| P6 | Gas and vacuum module, right side | A **vent header** collecting the pump exhaust, relief outlets and sample-gas exhaust into one DN25 stub on the dock duct, with a flow switch | Argon and dust must leave the Shuttle |
| P7 | Gas and vacuum module | **O2 sensor bosses** (low, at the module's right-hand side) for the machine's local sensor, and a conduit to the dock for the Shuttle monitors | §5.2 |
| P8 | Filter housing and cyclone pot | Isolation valves each side (exists); add a **bleed port with a needle valve**, a **thermocouple well** in the cake, a grounding lug, a bag-out flange and a drain; mount so the lid lifts into a bag in front, not into the machine | §7.2 |
| P9 | Every module base | A **bonding bus bar** on each base and a strap to the tray frame; lugs on chamber, lid, door, filter, cyclone, reservoir dock, drawer, pump | §7.3 |
| P10 | Drawer and exchange landing | A heat-rated, non-combustible landing pad for the hot plate; a plate-above-50 C stop in the drawer path | §8 |
| P11 | Chamber lid | A rated relief port and a pressure transducer on the safety display | §5.4 |
| P12 | Cell layout | UR12e safety planes excluding the optics bridge; the guard handle in the arm's reach with a monitored position; E-stop and reset out of the arm's reach | §9 |
| P13 | Dock and gas line | An NC shutoff at the dock, outside the Shuttle; the cylinder outside the Shuttle; a pressure-decay test point | §5.3 |
| P14 | Process module | A smoke or heat detector inside the guard on the exhaust path | Fire detection is the first thing a VLM lacks |

## 12. SOP outline

Each line is a section of a written SOP for BYU's LSO and Fire Marshal; the permissives are from §4.4, §5.2 and §9.

1. **Start-up.** Check fixed O2 monitors are on and above 20.5 %; the Class 4 sign is lit; the guard locks; the shutter closes on an interlock test; the key is in; the laser's fibre is connected; the cover slide is clean; module, plate and slide present; E-stop test; log it.
2. **Pump and purge.** Close the door; the argon valve opens only with exhaust flow proven; pump to ≤ 1 mbar; backfill; repeat two or three cycles; O2 < 100 ppm at the bed; pump exhaust vented outside.
3. **Run.** Laser enable requires O2 < setpoint, pressure in window, guard locked, plate present, key in; the relief and pressure transducer are on the display; heaters only under argon with O2 below set point.
4. **Opening the guard or chamber.** Laser off, shutter closed, key out; plate below 50 C (or heat-rated procedure); chamber vented to ambient; argon valve closed; O2 ≥ 20.5 % in room, shaft and bay; **respirator on**; two people for filter-side tasks.
5. **Powder handling.** Sieve, load and unload in the glovebox or an enclosed bonded transfer; bonded containers; non-sparking tools; no dry sweeping or compressed-air blow-off; combustible-dust vacuum only; spills: layer thickness recorded; closed, labelled, grounded storage.
6. **Filter and cyclone change.** Cool; isolate under argon; controlled oxygen steps with a thermocouple (§7.2); two people; FR clothing; P100 full-face; sand pail and Class D at hand; bag-out into a grounded container under sand; label; waste via BYU's unwanted-lab-material process; never vacuum fresh condensate.
7. **Alignment with the laser on.** LSO-approved, written, in a posted controlled area; lowest stable power or the red guide laser; beam block or dump in the path; eyewear OD ≥ 5 for the power used (7 on hand) and checked for damage; second person; no jewellery; key held by the person aligning; guard interlock bypass only by a key-controlled, labelled, time-limited override approved by the LSO; restart-after-break rule: re-check the setup and eyewear.
8. **Robot tending.** Hand-off permissive (§9) satisfied; the arm enters only when the permissive holds; the MiR parks in the marked zone at low speed; arm limited to its safety planes; powder and hot plates carried only as the SOP says; recovery by a trained person; no restart without a deliberate reset outside the zone.
9. **Emergencies.**
   - **Fire:** E-stop; leave; 911; do not use water, CO₂ or air on metal fire; a small Class D fire may be fought by a trained person with the Class D extinguisher or dry sand; report any extinguisher use to Risk Management. Tell the fire department there is aluminium powder, argon and a Class 4 laser. Stop the lift.
   - **Argon alarm:** leave; close the supply from outside; call for help; **no entry without SCBA and a second person**; keep others out; ventilate; do not reset until O2 ≥ 20.5 % at every sensor.
   - **Laser exposure:** stop emission, close the shutter, key out; get the eyes seen **the same hour** by an eye doctor; report to the LSO and Risk Management through the incident system.
   - **Hot plate burn, powder exposure, injury:** first aid; report.

## 13. What I checked from Edison's review, and what I added

- **Confirmed:** the 19.5 % definition (OSHA 1910.134 read); the 30 m³ room figure (2.15 m³ of argon for 19.5 %, reproduced); OD 7 passing 50 µW at 500 W; the T1/T2/T3 test times give 15 MJ, 50 kJ and 5 kJ; the published AlSi10Mg Kst, Pmax and MIE; the < 1 mJ condensate MIE and the slow-onset oxidation (EOS notice read).
- **Changed:** Edison found no BYU documents. BYU's index, fire, hot-work, policy and chemical-hygiene pages are open and say what §3 says; the program pages are gated. The README's FDA-exemption claim is **not in the CFR text**.
- **Added:** MPE (5 mW/cm² eye, 1 W/cm² skin) from a manual that reproduces Z136.1; the Class 1 limit of 1.9 mW; NHZ for the actual optics (114 m, 25 m bare fibre, 0.6-1.3 m diffuse); eyewear OD from power rather than from the label; a screening guard model with the polycarbonate panel's shortfall; a supply-fault argon table for the actual cylinder sizes and the Shuttle volume; the leak-rate and ventilation arithmetic that argues for a sonic orifice and a ducted exhaust; the oxidation-heat argument for a 0.3 L/min air-admission limit; the S7 monitor being portable; the G9SE's channel shortfall; 33 priced parts; 14 patch requests.

## 14. Open items

- **BYU:** read the gated program pages (Laser, Machine Guarding, Lockout, Electrical, Hot Work, Respiratory) with a BYU account; register the laser; ask the Fire Marshal for the DHA edition and the aluminium-powder limits.
- **Kardex:** interior air volume, ventilation and fire protection; written approval.
- **IPG:** back-reflection protection, interlock input, minimum stable output, collimated and bare-fibre behaviour on interlock.
- **Standards:** the ANSI Z136.1 edition BYU uses; the IEC 60825-4 Annex D test results for the real guard panel (a burn test); NFPA 484/660 edition; ISO/TS 15066 values for the chosen contacts; CGA P-1 and SB-2.
- **Tests before first light:** laser enclosure leakage with a power meter; guard burn-through at worst-case focus; interlock fault tests; O2 monitor response with a puff of argon in the bay; relief flow; a passivation dry run with a surrogate; bonding resistance; hand-off permissive with the robot.
