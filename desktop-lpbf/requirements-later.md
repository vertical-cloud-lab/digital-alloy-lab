# Requirements to carry forward: heated plate, plate and hopper swaps, automation, multi-laser

sgbaird raised these on [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) on 2026-11-17 as "a note for later":

- a heated build plate;
- swappable build-plate sizes;
- swappable hopper sizes;
- automation-friendliness, such as cleaning the chamber and removing the build plate;
- much later, multi-laser printing with independently drivable lasers, as in Adam Clare's work.

None of these are in the CAD model yet. Another run on this PR is re-laying the machine out to be lower and wider, so this note sets out what the base design has to reserve for each item. That way, adding one later doesn't mean a new chamber, lid or frame. The numbers come from [`requirements_budgets.py`](requirements_budgets.py). The literature comes from three Edison tasks run for this note (§6).

| Requirement | When | What the base design reserves now |
|---|---|---|
| Heated build plate | build 200 °C into phase 1–2; reserve 500 °C | a heater stack in the piston (plate, heater block, ceramic standoffs, cooled piston head); heater and thermocouple feedthroughs; a sliding seal on the cool side of the thermal break; the door stays locked until the plate is below 50 °C |
| Swappable build-plate sizes | phase 1 | build *modules* (cylinder, piston, heater and plate as one unit) on one floor flange and one Z coupling. The floor opening, recoat stroke, blade, gas nozzle and camera view are sized for the largest module |
| Swappable hopper sizes | phase 1 | a fixed metering base on the lid with a standard flange; 25/100/250/500 cm³ reservoirs, each with its own shut-off; dose weighing on the metering base, not under the reservoir; large reservoirs sit beside the chamber, not on top |
| Automation-friendliness | phase 3 | plates (or modules) located on datums and held by a clamp a robot can release; a radiused chamber with a lift-out liner, sloped floor and vacuum port; a cover-slide cassette; a sensor that confirms every step |
| Multi-laser, independently driven | much later | a lid optics port big enough for 2–3 heads; spare head stations on the optics plate; spare scanner, laser and safety channels; chiller and power headroom; the beam layout chosen against the gas flow |

## 1. Heated build plate

The concept has plate heaters on the I/O list (§3.6 of the [README](README.md)) but no heater design. Its open question 3 asked whether 200 °C preheat is wanted. The answer is now yes.

**What the literature says** ([Edison](edison/plate-hopper-automation/answer.md), §1):

- **AlSi10Mg is not crack-limited, and preheat mostly ages it.**
  - At 150 °C, Si and β″ precipitate during the build, and the later T5 response becomes marginal (Zhu 2023).
  - At 160–170 °C, a long build ages unevenly with height: peak hardness sits ~40 mm above the plate (~10 h of remaining build), and the material nearest the plate is over-aged (Chambrin 2022; Casati 2018).
  - A cold plate keeps more Si in solution for direct ageing afterwards.
- **6xxx needs ~400–500 °C.** In EN AW 6182, columnar grains turn equiaxed from ~400 °C, and at 500 °C parts were crack-free at > 99 % density (Riener 2022). AA6061 was crack-free at 500 °C (Stopyra 2020).
- **7xxx and 2xxx are not fixed by plate heat alone.**
  - AA7075 still cracked at 100–200 °C, and at 400 °C the cracks changed form but remained. About 1 wt.% Zn and 0.3 wt.% Mg evaporated at every preheat (Velikajne 2026).
  - 200 °C did not stop cracking in AA2024 (Stopyra 2020).
  - These alloys need chemistry changes, such as grain refiners, or local beam heating (§5).
- **Heaters.**
  - Cartridge heaters are the standard. A custom tungsten module used six 100 W, 24 V cartridges, two K-type thermocouples, a ceramic insert and a 30 min soak to hold 700 °C at ±5 °C (Field 2020, thesis).
  - Induction held 800 °C for 450 min at ±10 °C, with water-cooled exchangers keeping the piston below 100 °C and the motors below ~70 °C (Caprio 2018, 2020).
  - A 3 kW AlN heater with poor insulation (44 % efficient) reached only 374 °C on the plate (Ramulifho 2022). Isolation matters more than heater power.
- **Atmosphere.** At 600 °C, tungsten powder oxidised visibly even under flowing argon (Field 2020). A hot bed raises the bar for O₂, and the O₂ sensor belongs in a cooled bypass, not above the hot plate.

**Design: a heater stack that rides on the piston.** From the top down:

1. the build plate. It is swappable: 6061 or an AlSi10Mg plate for Al alloys;
2. a heater block with 3–6 cartridge heaters in a symmetric pattern, and two thermocouples (centre and edge) read by the MAX31856s already in the BOM (C5). A third thermocouple on the cold side goes to an independent over-temperature trip;
3. three ceramic standoffs (Macor, k ≈ 1.5 W/m·K, or zirconia) as the thermal break;
4. the piston head, which carries the bore seal. It is air- or water-cooled in the 500 °C version;
5. the piston rod. A hollow rod, or a service loop through a floor feedthrough, carries heater power and the thermocouple out.

**Sizing (`requirements_budgets.py`, Ø50 plate, argon at 2 m/s):**

| Set point | Steady loss | Heater for a 15 min ramp | Passive cool-down to 50 °C |
|---|---|---|---|
| 200 °C | ~25 W | ~50 W | ~45 min |
| 500 °C | ~75 W | ~140 W | ~55 min |

- **The biggest loss is the build cylinder, not the plate's top surface.** The cylinder wall next to the plate runs close to plate temperature. That heat goes down the model's 1.7 mm-wall tube into the chamber floor: ~13 W at 200 °C and ~34 W at 500 °C, about half the total, as an upper bound. So the seal between the cylinder and the floor has to sit away from the hot zone, and at 500 °C the floor flange needs cooling. Viton is rated to about 200 °C.
- **Clearance.** The model's Ø53 Al plate grows 0.21 mm in diameter at 200 °C and 0.58 mm at 500 °C. Its 0.4 mm radial clearance in the Ø53.8 bore leaves room for that expansion, but it is too loose to contain powder (§2). Plates are swappable anyway, so each plate's cold clearance can be set for its set point.
- **Seals.** Don't put the sliding seal at the plate. PTFE's ~260 °C rating is a material limit, not a rating for a dynamic seal in powder, and the high-temperature builds in the literature keep seals and drives below ~70–100 °C (Edison rank 12). Put a graphite or labyrinth wiper next to the hot plate, and the real seal (PTFE, or aramid felt, never wool) on the cooled piston head below the standoffs. Do this at 200 °C too, so the 500 °C version changes parts, not layout.
- **Two tiers.**
  - Tier A, to build: 200 °C, ~100 W of cartridge heaters, a hot-side wiper, and a PTFE or aramid seal on the cool side.
  - Tier B, reserved: 500 °C (the level that made 6xxx crack-free), ~150–300 W for Ø50–Ø75, a water-cooled piston head, a cooled floor flange, and Z motion and heating interlocked on coolant flow.

  Both tiers use the same plate interface and the same feedthroughs.
- **Interlocks.**
  - An independent over-temperature cutout: a thermal fuse, or a second thermocouple wired to the safety relay. It does not depend on the supervisor.
  - The heater runs only under inert gas.
  - The guard lock (Omron D4JL) already holds the door while lasing or off atmospheric pressure. Add "plate above 50 °C" to that list, so air never meets hot Al powder.
- **Preheat is a screening variable.** It changes the thermal history the alloy sees, so it is a recipe parameter and goes into the dataset with the rest of the process window. Because AlSi10Mg keeps ageing at temperature for as long as the build runs, also record how long each coupon sat on the hot plate, and compare alloys at matched build height and duration.

## 2. Swappable build-plate sizes

The concept has a Ø50 mm plate with a Ø25 mm insert. The model now has a Ø53 plate in one Ø53.8 mm bore.

**What the literature says** ([Edison](edison/plate-hopper-automation/answer.md), §2 and ranks 2, 4, 5, 13, 20):

- **Small modular machines already exist.**
  - Schanz et al. (2022) built a 240 × 200 × 300 mm lab LPBF with a **Ø40 mm plate and up to four powders**. A 16-cube parameter study needed only ~0.8 cm³ of powder, a reservoir swap took < 3 min, and a recoat ~5 s.
  - Sisma's MYSINT100 plate carries twelve Ø12 mm removable inserts, located by precision pockets and Ø1.5 mm pins and screwed from below (Zanini 2024).
- **Containment clearances.** Edison recommends ~0.05–0.15 mm radial running clearance cold, and no more than 0.10–0.20 mm once hot. The model's 0.4 mm is too loose for 15–63 µm powder unless the seal closes it. Swap the plate, sleeve and upper seal together as one module, which is what a build module is.
- **Registration.** Use a three-point kinematic or zero-point coupling with one axial clamp, and never magnets alone above ~200 °C. Edison suggests ≤ 10 µm Z repeatability, ≤ 25 µm XY, ≤ 0.02° tilt and ≤ 20 µm flatness. It labels these as targets to validate, not literature values.
- **Results transfer only partly.** A small plate changes thermal mass, lateral heat loss, layer time and part spacing, and AlSi10Mg's in-situ ageing follows those. Treat small-plate results as screening evidence. Confirm winners with matched coupons on a production machine, matching layer time, scan strategy, gas-flow direction and thermal history.

**Two ways to swap sizes:**

| | Reduced-build-volume insert in one bore | Swappable build module |
|---|---|---|
| What changes | a sleeve and a smaller piston inside the main bore | the whole cylinder, piston, heater stack and plate |
| Precedent | Renishaw RBV, the Ø25 insert in the README | exchangeable build cylinders on EOS and TRUMPF machines |
| Heated plate | each insert needs its own heater and thermal break, inside the bigger piston | each module carries its own heater stack |
| Powder in the annulus | yes, and it is hard to clean | no |
| Plate removal | in the chamber | the module can leave the machine still closed (§4) |
| Cost | lower | a second floor flange and a Z quick-coupling |

**Recommendation: build modules.** One floor flange and one Z coupling take Ø25, Ø50 and Ø75 modules. The same choice makes the heated plate and plate removal easier.

What each size needs (`requirements_budgets.py`, 30 µm layers, 1.8 dose factor, AlSi10Mg):

| Module | Powder per 15 mm build | Powder for the full 40 mm stroke | Blade and cross-flow nozzle width | Cross-flow at 2 m/s (8 mm slot) |
|---|---|---|---|---|
| Ø25 | 18 g | 47 g | 65 mm | 62 L/min |
| Ø50 | 71 g | 189 g | 90 mm | 86 L/min |
| Ø75 | 160 g | 426 g | 115 mm | 110 L/min |
| Ø100 | 284 g | 758 g | 140 mm | 134 L/min |

**To reserve now:**

- **Size the floor opening and flange for the largest module.** Ø75 is the sensible ceiling for alloy screening. Ø100 already needs ~0.3 kg of powder for 15 mm, which is the batch size we built small to avoid.
- **Size the recoat stroke, blade, dose line and camera view for the largest module.** The cross-flow nozzle can be a per-size insert, or one nozzle sized for the largest. The blower has to deliver the larger flow either way.
- **The scan field is not a constraint.** The FTH254-1064's 156.7 mm field covers Ø100.
- **Plate datums.** Each plate locates on its piston head by dowels and a face, or kinematically, so a swap doesn't need re-levelling. After each swap, a touch-off or the layer camera confirms the plate height.

## 3. Swappable hopper sizes

The concept has one ~100 cm³ dose-from-above cartridge with a load cell under it.

**What the literature says** ([Edison](edison/plate-hopper-automation/answer.md), §3 and ranks 9, 11, 15, 18):

- **In most machines, the recoater gap sets the dose, not a mass measurement** (Revanur 2024, thesis). Weighing doses (below) is a step beyond common practice, and it closes the powder mass balance.
- **Small multi-reservoir feeders exist:**
  - Schanz's four rotating reservoirs;
  - an ORNL feeder with 16 small hoppers for refractory compositions (Hyer 2025);
  - double hoppers with a mixing chamber for blends.
- **Dose check.** For Ø50 at 50 µm, the geometric layer is 0.098 cm³ and Edison suggests commanding 0.2–0.4 cm³. That matches this concept's 1.8 dose factor and 50 % packing (0.35 cm³).
- **Cartridge practice.**
  - Each cartridge has a keyed identity (RFID or barcode) carrying tare, lot and alloy, and a normally closed bottom valve.
  - Less than 1 % of the powder should stay behind when the cartridge is removed.
  - Calibrate dose mass against actuator motion for every powder.
  - Weigh the overflow too, which closes the mass balance.
  - Quarantine recovered powder of a new alloy rather than reusing it.

**Split the hopper into a fixed metering base and a swappable reservoir.**

- **The metering base** sits in the lid. It holds the metering roller or slot and a shut-off.
- **The reservoir** docks to the base on a standard flange. KF-40 or KF-50 is cheap, sealed and needs one clamp. Each reservoir has its own valve, so it can be removed full, under argon.

**Reservoir sizes:**

| Reservoir | Covers |
|---|---|
| 25 cm³ | a 15 mm build on Ø25 (12 cm³); the full 40 mm Ø25 stroke takes 32 cm³ |
| 100 cm³ | a 15 mm build on Ø50 (48 cm³) or Ø75 (108 cm³, just) |
| 250 cm³ | the full Ø50 stroke (129 cm³), or a ~35 mm build on Ø75 (the full stroke takes 289 cm³) |
| 500 cm³ | Ø100 |

- **Weigh doses on the metering base, not under the reservoir.** A load cell sized for a full 500 cm³ cartridge (~5 kg) is good to about ±1 g. One dose is 0.04 g on Ø25 and 0.14 g on Ø50, so that cell resolves a dose only when averaged over ~80 and ~20 layers. A small dosing tray on its own 100–200 g cell can weigh each dose. Weigh the reservoir only for inventory.
- **Large reservoirs grow sideways, not up.** As a vertical Ø60 mm tube, a 500 cm³ reservoir stands ~180 mm tall, which works against the lower, wider layout this PR is moving to. Put big reservoirs beside the chamber and feed the metering base through a short screw or vibratory channel.

## 4. Automation-friendliness: plate removal and chamber cleaning

The concept has a Python supervisor with a REST API, docking hopper cartridges, and a CubOS-driven gantry *outside* the machine for cartridges and plates.

**What the literature says** ([Edison](edison/plate-hopper-automation/answer.md), §4 and ranks 14–17, 19):

- **Plate exchange.**
  - Airlocks or rapid-transfer ports, and zero-point clamps that keep one reference frame from the machine through the robot to post-processing (Khorasani 2020 review).
  - A sheet-metal clamping interface carried builds from LPBF to a robot to milling (Ferchow 2022).
  - Edison's targets: plates or modules < 5 kg, external grasp features, a positive lock, two independent presence sensors, a temperature permissive, load-cell confirmation of pickup, and a sealed canister for transport.
- **Cleaning.**
  - Tool-less liners, and a cover-slide carousel of 3–10 indexed positions with a transmission check before each build.
  - Internal corner radius ≥ 5 mm, no blind powder traps, and line of sight to the bed, overflow, ducts and window shield.
  - Al/Mg condensate is reactive waste: grounded tools or closed HEPA extraction, never compressed air.
  - Before a different alloy goes in, verify the chamber is clean with a camera, gravimetry and swabs.
- **Self-driving labs.**
  - Zhao et al. (2026) propose an AI auto-lab that couples multi-hopper printing, robotic heat treatment, X-ray CT and mechanical testing.
  - Collins and Ales (2026) describe agent-driven cells with safety interlocks, MCP interfaces and human-set stopping conditions, with hardness as a fast screening surrogate.
  - Both put a deterministic state machine under the AI scheduler, with read-only telemetry exposed widely and hazardous commands restricted.

**Removing the plate, in three ways:**

1. **Through the door, after vacuum depowdering.** This is the simplest. The plate is held by a clamp a robot can release, such as a pull stud with a spring-closed, air-released clamp, or a bayonet, instead of screws. Plates have gripper features.
2. **The whole build module drops out through the floor** into a sealed transfer can and goes to the glovebox for depowdering. This follows the exchangeable-cylinder machines. The powder stays inert and contained, which matters for Al under NFPA 484.
3. **The chamber door docks to the glovebox,** so the plate never leaves argon. This is the most contained route, but it is harder for a robot.

The build-module choice in §2 keeps route 2 open, and route 1 needs nothing extra.

**Cleaning the chamber:**

- radiused internal corners, with no exposed threads or blind holes where powder lands;
- a floor sloped to the overflow, and a lift-out liner tray that takes most of the soot with it;
- a KF-25 port for a HEPA vacuum wand, and argon sweep jets that push condensate to the filter;
- a cover-slide cassette that can be changed without lifting the lid;
- at the end of a build, the recoater sweeps leftover powder into the overflow.

**Sensors that confirm every step:**

- plate present and seated: camera, plus an inductive or contact sensor;
- plate temperature;
- O₂ and pressure;
- dose and reservoir weight;
- door-lock state.

The supervisor refuses the next step until the last one is confirmed, which is what lets a robot or gantry drive it.

## 5. Multi-laser printing, much later

**Whose work this is.** Edison's `LITERATURE_HIGH` search ([`edison/multi-laser/answer.md`](edison/multi-laser/answer.md)) found that the independently addressable multi-laser powder bed work comes mainly from the **University of Sheffield** (Kamran Mumtaz, Kristian Groom and their students), not from Adam Clare. It could not tie a multi-laser hardware paper to Clare; the Clare papers it did find are on spatter, in-situ monitoring and a powder-composition patent.

Its separate `LITERATURE` search on Clare's own papers ([`edison/clare-multi-laser-papers/answer.md`](edison/clare-multi-laser-papers/answer.md)) found two that match "independently drivable lasers":

- **[Sanchez, Hyde, Ashcroft, Ravi and Clare 2021](https://doi.org/10.1016/j.addma.2021.101948)**, *Additive Manufacturing* 41, 101948. On a Renishaw RenAM 500Q (four 500 W lasers, run at 212.5 W), 10 mm stripes of the *same* IN718 part were assigned to different lasers. Vertical multi-laser specimens crept to within 1 % of wrought 718 and beat single-laser ones, and build time more than halved.
- **[Bogo, Clare and Liao-McPherson 2026](https://doi.org/10.1109/CCTA62090.2026.11684174)**, IEEE CCTA 2026, a simulation from UBC. A leading melt beam and a trailing reheat beam (25–100 W each, 0–250 µm behind, 0.25–1 m/s) were tuned by iterative learning control to hit a target cooling rate. It reached −2.34 × 10⁶ K/s against a −2.50 × 10⁶ K/s target, where one beam gives −2.96 × 10⁶ K/s, and it converged in ~20–40 trials. There is no hardware yet.

The second paper is the closest to "independently drivable" in the closed-loop sense this lab cares about: two beams whose powers and spacing are set per vector to steer the cooling rate, tuned by a learning loop. **Doing that in hardware sets a hard requirement.** A beam 0–250 µm behind another at 0.25–1 m/s trails it by ~0.1–1 ms. So two separate scan heads must be registered to well under the 50 µm beam radius and share a clock that is good to well under 0.1 ms. Combining both beams ahead of one scan head gets that registration for free. But the offset is then fixed relative to the mirror axes, so the second beam trails only along one scan direction unless the offset can be rotated. Clare's other hits (Hirsch 2018 rework with SRAS inspection lasers, Guan 2015/2016 OCT, fractal scan paths) use one melting beam.

**What exists.** There are two families:

1. **Many low-power, individually switched diodes in one head on a gantry.** This is Sheffield's diode area melting (DAM).
   - The 808 nm head has 100 fibre-coupled channels at 5 W each, imaged to ~65 µm spots; experiments used 10 at a time. Each channel can melt, preheat, post-heat or remelt in the same pass ([Alsaddah et al. 2022](https://doi.org/10.1016/j.matdes.2022.110518)).
   - Blue DAM uses 6 × 3.5 W or 9 × 4 W diodes at 450 nm, with ~70 µm spots and 60 mm focal-length optics ([Erman et al. 2025](https://doi.org/10.1007/s00170-025-15090-0); [Caglar et al., SFF 2023](https://doi.org/10.26153/tsw/51029)).
   - It is slow: 40–500 mm/min against 0.1–3 m/s for galvo LPBF. Cooling is 191–8400 K/s against 10⁴–10⁷ K/s, and in Ti-6Al-4V it fell from 778 K/s with one beam to 191 K/s with six ([Liang et al. 2026](https://doi.org/10.1007/s40964-026-01951-x)). That gives coarser, different microstructures. For screening this is a deliberate thermal-history knob, not a stand-in for production LPBF. The README's "Sheffield diode point melting" row (§2.1) is the same group.
2. **A few high-power beams, each independently positioned.**
   - **Two or more galvo-scanned fibre lasers,** as in commercial multi-laser machines. Where fields overlap, colliding melt pools throw large spatter. In one study, AlSi10Mg overlap specimens had 17.4 % lower elongation than single-laser ones ([Yin et al. 2021](https://doi.org/10.1016/j.addma.2021.102178)). Stitching needed 500 µm of model overlap; 50 µm left lack of fusion (Rindler 2022, thesis). Multi-laser AlSi10Mg loses fatigue life unless gas flow and scan order are tuned ([Nagalingam et al. 2025](https://doi.org/10.3390/met15070807)).
   - **A melting beam plus a defocused heating beam.** Sheffield's DAMX pairs a 44 W, 450 nm melting spot (~100 × 150 µm) with a 140 W, 915 nm top-hat of 6–13 mm that can lead, surround or trail it. It heats locally to ~400 °C, reached 99.99 % density in Ti-6Al-4V and changed the α′ lath size (Aydin 2025, thesis).

**Wavelength matters for Al.** AlSi12 powder absorbs ~48 % at 450 nm, ~26 % at 808 nm and ~19 % near 1060 nm (Alsaddah 2023, thesis). That favours blue diodes for extra beams, but single blue diodes are only ~3.5–4.5 W each, with worse beam quality than a single-mode fibre laser.

**Edison's ranking for this machine:**

1. Keep the 1070 nm galvo beam for melting and add a **defocused heating laser** (100–200 W at 808 or 915 nm). This is the most useful first upgrade, and it suits crack-prone Al alloys. It is also a local alternative to the heated plate (§1): ~400 °C where the beam is, instead of everywhere.
2. A **blue diode array on a gantry** (DAM-style) for thermal-history experiments.
3. **Two galvo-scanned fibre lasers.** This is the most industrial option, but one scanner already covers a Ø50 plate.
4. A hybrid of 1 and 2.
5. A fixed array over a moving bed. Moving a powder bed and its gas nozzles conflicts with everything else in the design.

**What to reserve now.** This merges Edison's provisions with the geometry from `requirements_budgets.py`. Edison's window sizes, chiller kW and channel counts come without citations, and it wrongly gives the f = 254 mm lens a ~Ø50 mm field (it is 156.7 mm), so treat those as starting points.

- **Lid optics port.**
  - Make it one ~Ø110 mm O-ring face. It takes a single Ø2 in. window plate now, and later a Ø100 mm window, or a plate with a primary window plus a Ø40–60 mm auxiliary port.
  - Coat for 1070 nm and 915 nm. A 450 nm source gets its own blue-rated window.
  - Fused silica under a full atmosphere (safety factor 4) needs ≥ 2.2 mm for Ø48 mm clear and ≥ 4.6 mm for Ø100 mm.
- **Head positions (f = 254 mm, WD 301 mm, window 175 mm above the powder).**
  - A head reaches the whole Ø50 plate only within ±53 mm of the plate centre. There the worst incidence angle is ≤ ~18° and the spot stretches by ≤ ~5 %.
  - FTH254-1064 housings are Ø120 mm, so two sit ≥ 120 mm apart. They then share only a 37 mm band, 73 % of the plate width. Edison's "both scanners cover the whole plate" needs smaller lens housings, heads tilted toward the centre, a longer focal length, or pre-focusing heads with no f-theta.
  - One head needs ~Ø24 mm of clear window at the lid. Two heads at ±45 mm need one ~Ø82 mm window, or two ~Ø30 mm windows on 52 mm centres.
- **Optics plate.** Leave room and dowelled datums for a second scan head, plus a stiff rail with tip/tilt and XYZ adjustment for an auxiliary heating or diode head. Keep it clear of the main scan cone and the recoater.
- **Controller.** Leave room for a second XY2-100 channel and 8 or more isolated TTL or analogue laser channels. All of them run on one hardware clock, with a blanking line that turns every source off at once.
- **Safety.** Each source gets its own shutter, enable and emission indicator, all in the one hardwired chain from the README (§3.7). The guard and eyewear must also be rated for 450 nm if a blue source is added.
- **Cooling and power.** Edison suggests ~1.5–2 kW of spare chiller capacity, and loops that can be added.
- **Gas.** Fix the cross-flow direction before the head layout. Scan from upwind to downwind, never melt in another beam's downwind plume, and run a diode row across the flow.

## 6. Edison tasks run for this note

| Folder | Job | Question | Task |
|---|---|---|---|
| [`edison/clare-multi-laser-papers/`](edison/clare-multi-laser-papers/) | `LITERATURE` | Adam Clare's papers on multi-laser, multi-beam and laser-array processing | `a00790ad…` |
| [`edison/multi-laser/`](edison/multi-laser/) | `LITERATURE_HIGH` | his work, other multi-beam platforms, stitching and plume interaction, and what a one-laser machine should reserve | `040071dd…` |
| [`edison/plate-hopper-automation/`](edison/plate-hopper-automation/) | `LITERATURE_HIGH` | heated plates, plate-size swaps and reduced-volume inserts, hopper swaps, plate removal, depowdering and chamber cleaning | `d8157a51…` |

Each folder has the query, the answer, the references and the full trajectory. [`edison/run_edison.py`](edison/run_edison.py) submits, waits for and fetches them.
