# Real parts in the low-profile model (issue #260)

Sterling asked for real parts wherever possible. The fasteners were already real McMaster-Carr parts. Most other bought
parts in `cad/lpbf_low.py` were still boxes and cylinders. This note covers the next step.

- [`cad/vendor_parts.py`](cad/vendor_parts.py) draws **18 bought parts to their published dimensions**. Each one is a
  drop-in builder in the same local frame as the envelope it replaces.
- **11 of them were checked against the vendor's own CAD** (volume and bounding box).
- **Every builder was swapped into a copy of the model** and intersected with its neighbours using exact OpenCascade
  booleans.
- `lpbf_low.py` itself was **not edited**, because another agent is working on it. The integration list below gives the
  exact change for each part.

Files:
- [`vendor-parts.csv`](vendor-parts.csv): one row per builder, with part number, the dimensions used, source URL,
  price, fetch time and the volume check.
- [`cad/vendor-cad-manifest.csv`](cad/vendor-cad-manifest.csv): the 20 vendor files fetched, with URL, size and
  sha256. None of them is committed; they stay in `/tmp/parts-work`.
- [`analysis/out/real-parts/`](analysis/out/real-parts/):
  - `inventory.md` / `.csv`: all 63 bought-part entries in `build()`, ranked, with status;
  - `verify.json`: the CAD comparison;
  - `swapcheck.json`: the boolean check.

Re-run any of them with `python desktop-lpbf/cad/vendor_parts.py inventory|verify|swapcheck`. Run under `/tmp/capmem 3`.
`verify` needs the vendor files back in `/tmp/parts-work`. On a busy runner, `swapcheck` took 17 min of wall clock
(7 min of CPU).

## Refined to the vendors' evidence (2026-11-23)

See [`oem-parts.md`](oem-parts.md). In short:

- **Six builders were refined to the vendor CAD.**
  - The aligned volume IoU, from exact mesh booleans after the best axis rotation and ICP, went up for each:
    - ClearPath 0.59 → 0.66;
    - 6627T91 0.95 → 0.98;
    - 6709K12 0.78 → 0.83;
    - KF-25 / KF-40 clamps 0.28 / 0.52 → 0.71 / 0.80;
    - 4123K45 valve 0.58 → 0.88.
  - The KF stubs (0.97) and the ball nut (0.84) were left as they were.
- **The IPG laser and Eaton UPS fronts are now drawn** from the vendors' own render and photo: controls, display, grilles and
  handles.
- **The finishes were measured** from vendor photos (`cad/oem/finishes.json`), with silhouette overlays.
- **No builder grows outside its old box,** and no placement moved.
- **The 2026-11-23 vendor files were re-fetched into `/tmp/agentE/vcad`.** Every sha256 matches. `cad/oem/cad-manifest.csv`
  lists them. For `verify`, link that directory as `/tmp/parts-work/vcad` and `/tmp/parts-work/teknic`.

## Integrated into `lpbf_low.py` (2026-11-20)

After the seal work was committed, the real parts below went into the model. `lpbf_low.py` now does
`import vendor_parts as VP`.

**Interference check:** `analysis/interference.py` finds 0 interferences in every static state and every motion sweep,
for all three variants: M50/M, S25/S and L75/L (`analysis/out/interference.md`, `analysis/out/variants/`). The machine
is still 581.2 mm above the tray.

**Now real:**
- recoater and Z servos (Teknic CPM-SDSK-2311S);
- dosing stepper (6627T91);
- recoater rail, carriage and ball nut (6709K33, 6709K12, 4566N401);
- the three KF-25 ports (5786N23);
- the KF-40 overflow port, clamp and jar (5786N25 profile on 1.5 in. tube, 4518K73);
- f-theta lens (FTH160-1064), plus a new adapter ring;
- galvo (basiCube 20);
- IPG collimator;
- vacuum isolation valve (4123K45 with a 4518K72 clamp);
- laser (YLR-500-U3, 4U);
- UPS (5PX1500RTG2).

**Changes the real parts forced:**
- **Rack:** 11U, 515 mm tall (was 10U, 470 mm), because the laser is 4U. That is under the 564 mm budget.
- **Laser guard and process base plate, left side:** moved out from x = −370 to −420. The collimator with its strain
  relief is 206 mm long and now ends 4 mm inside the panel. The fibre crosses the panel at the existing guarded bulkhead.
- **Laser guard and process base plate, right side:** moved out from x = 290 to 310, for the 124 mm ball valve.
  - The valve's lever points back over the chamber, at z 157–162.
  - Its KF-25 clamp is turned with its ears up and hinge down, to clear the chamber's side draw latch.
  - The pump hose now starts at the valve's outlet flange, x = 298.2.
- **Galvo and beam line:**
  - The basiCube 20 sits on a new 10 mm riser plate.
  - The beam line moved to the real input: z = z_bridge1 + 40 = 272.7 (was 277.7) and y = −25.25 (was 0).
  - The beam tube is now Ø20 (was Ø28), so it clears the reservoir handles (z 258) by 4.7 mm.
  - The shutter and the collimator's V-mount moved with the beam.
- **f-theta adapter ring:** new part, 6061, Ø110 × 16 mm, M85×1 internal thread, under the bridge from z 191.7 to 207.7.
- **Recoater motor bracket:** top lowered by 1 mm, to `rz_ - 29.6`.
- **Z servo:** connector block faces the front.
- **Dosing stepper:** face moved 12 mm further out and the coupling made 12 mm longer, for the 6627T91's 24 mm shaft.
- **KF stubs:** `kf_weld_stub` now trims the weld tube to the requested stub length, keeping the flange and taper. That
  keeps the overflow fitting out of the funnel block and the vacuum stub inside its adapter plate.
- **KF-40 overflow clamp:** turned so its hinge faces +y and its wing faces +x. Facing −x it hit the module on its swap
  path.
- **Sliding guard door:** now slides 515 mm (was 470) on a rail extended to x = 720, so it uncovers the right door latch
  (operations.md).
- **Masses:**
  - servos 0.6 kg each (were 1.6);
  - galvo 3.75 kg (was 2.5);
  - lens 0.8 kg (was 0.6);
  - UPS 23 kg (was 25).

  `analysis/out/mass.*` has been re-run.

**Integrated in round 6 (2026-11-25, [`oem-parts.md`](oem-parts.md) round 6):**
- **Pump:** the Edwards nXDS6i (BOM G2 since 2026-11-22, in place of the 4396K21 this list named), drawn to Edwards'
  dimension drawing (silhouette IoU 0.923 over five views; Edwards publishes no CAD), with the vacuum hose on its NW25 inlet.
- **HEPA housing 5169K72:** on two KF-25 adapters and elbows (aligned volume IoU 0.949 against McMaster's CAD). The adapters,
  elbows and stand are not in BOM G5, and their dimensions are assumed.
- **Pressure transmitter 3861N11:** on an SAE-4 male × 1/4 NPT female adapter in the lid port (IoU 0.948). Its lead ends
  1.25 mm under the solid optics bridge, so it can't leave upward: it needs a 90° adapter, a side-exit transmitter or a bore
  in the bridge (not chosen).
- **Everything else** listed under "What is still not real" below.

The tables below are the swap test made before the integration. The positions in its "Change" column are the
pre-integration ones; the list above is what the model now uses.

## How the parts were sourced

- **McMaster-Carr:** product pages and "3-D STEP" downloads fetched through the lab Pi tunnel in headless Chrome, one
  part at a time.
- **Not fetched:**
  - 6709K33 rail: the page wants a rail length before it offers CAD;
  - 4277T52 relief valve: needs a set pressure chosen first;
  - 3497N23 hose: CAD not fetched;
  - 4396K21 pump: McMaster offers no CAD for it.
- **Thorlabs:** FTH160-1064 drawing PDF, from Thorlabs' public media link.
- **Teknic:** ClearPath 231x 3D model zip (public download) and dimensional drawing D1171/M.
- **Datasheets:** SCANLAB basiCube brochure (2025-06), Eaton 5PX1500RTG2 datasheet, Ntron Microx datasheet, Vaisala
  DMT143 datasheet, KNF N 630.1.2 datasheet.
- **IPG:** the laser and collimator dimensions come from IPG's drawings as transcribed in
  [`quotes/ipg-ylr-500-u3-sm-ac.md`](quotes/ipg-ylr-500-u3-sm-ac.md).

## Check against the vendor CAD

Volumes are in mm³; Δ is ours against the vendor's. "Extents" means the sorted bounding-box sizes.

| Part | Our builder | Vendor volume | Δ volume | Extents match |
|---|---|---|---|---|
| McMaster 5786N23 KF-25 weld fitting | `kf_weld_stub(25)` | 4,061 | −0.1 % | exact |
| McMaster 5786N25 KF-40 weld fitting | `kf_weld_stub(40)` | 8,414 | −0.8 % | exact |
| McMaster 4566N401 flange ball nut | `mcm_4566N401()` | 18,643 | +0.7 % | exact (flats 30 across) |
| McMaster 4518K72 KF-25 wing clamp | `kf_wing_clamp(25)` | 19,418 | −0.6 % | within 0.02 mm |
| McMaster 4518K73 KF-40 wing clamp | `kf_wing_clamp(40)` | 30,817 | −2.5 % | within 0.01 mm |
| McMaster 4123K45 KF-25 ball valve | `mcm_4123K45()` | 216,275 | −2.4 % | within 0.63 mm |
| McMaster 6627T91 NEMA 17 stepper | `mcm_6627T91()` | 81,513 | +5.4 % | within 0.1 mm |
| McMaster 6709K12 carriage | `mcm_6709K12()` | 30,696 | +10.5 % (internal ball returns not drawn) | exact |
| McMaster 5169K72 filter housing | `mcm_5169K72()` | 500,842 | +30.6 % | within 5.8 mm (McMaster's bracket rises 4.9 mm over the top) |
| McMaster 3861N11 transmitter | `mcm_3861N11()` | 19,505 without the coiled lead | +23 % | hex and thread only; the 36 in. lead is not drawn |
| McMaster 5537T983 leveling mount (already in the model) | the model's foot | 8,174 | −6.2 % | exact |
| Teknic CPM-231x ClearPath | `clearpath_sd_231x()` | 201,861 | +69 % (Teknic's housing has deep cooling grooves and a cavity; set the mass to 0.6 kg) | within 0.59 mm, connector block included |

Parts with no vendor CAD were drawn to the published overall size. Their extents match by construction:
- the 4396K21 pump: 368.3 × 142.9 × 304.8;
- the FTH160-1064 lens;
- the basiCube 20;
- the IPG laser and collimator;
- the Eaton UPS;
- the 6709K33 rail.

## Integration list (replace in `lpbf_low.py` / `modules_low.py`, with `import vendor_parts as VP`)

The swap check put each part where its envelope was and intersected it with every part its box touches. That run
included the fasteners. "Envelope" is the old shape's overlap with the same neighbour.

| Part (Part name in `build()`) | Change | Swap check | What the real part forces |
|---|---|---|---|
| Recoater servo (ClearPath-SD, NEMA 23) | `rmot = place(VP.clearpath_sd_231x(20.57), (-cx - 60, ry_, rz_), (0, 1, 0), (1, 0, 0))` | hits the motor bracket, 4,033 mm³ (envelope 0) | The motor is 59.1 mm square, not 57.15, so its underside is at `rz_ - 29.55`. Lower the bracket top from `rz_ - 28.6` to `rz_ - 29.6`. The body is 84.8 long (was 100), plus a 22.75 mm connector block on top. |
| Z servo (ClearPath-SD, NEMA 23, folded), in `modules_low.add_zstage` | `h.place(VP.clearpath_sd_231x(18.0, connector="-y"), (64.0, 80.0, az1), (1, 0, 0), (0, 0, 1))` | clear, including along the 41-step module swap path | With the connector toward +y it hits the process base plate (12,624 mm³), because it passes the window's y = 114 edge. Keep it on −y. |
| Dosing stepper (NEMA 17) | `place(VP.mcm_6627T91(), (xd, 74, rzc), (1, 0, 0), (0, -1, 0))` | the shaft enters the metering base (261 mm³) and the roller seal housing (195 mm³) | The shaft is the roller drive, so these overlaps are designed. The seal housing still needs its bore drawn. The body is 48 long, not 40. |
| Recoater carriage (15 mm rail) | `place(VP.mcm_6709K12(), (xc, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0))` | clear | 62.1 long with the grease nipple (was 57). |
| Recoater guide rail (15 mm, 270 mm) | `rr = place(VP.mcm_6709K33(270.0), (-135, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0))` | clear | The raceway grooves are assumed, since McMaster gives no section. |
| Recoater ball nut (flange on the +x face) | `place(VP.mcm_4566N401(), (xc + 10.5, ry_, rz_), (-1, 0, 0), (0, 0, 1))` | clear | The flange has flats 30 mm across, facing ±y. |
| f-theta lens | `lens = VP.thorlabs_fth160_1064().translate(V(0, 0, P["z_lens0"]))` | clear | The lens sits inside the old envelope. The flange shoulder is at z 191.7 (FFL), and the M85×1 thread runs from z 191.7 to 204.5. That is **3.2 mm below the bridge underside** (z 207.7), so the lens cannot screw into the bridge. It needs a 16 mm M85×1 adapter ring under the bridge, or a 16 mm boss. |
| 2-axis galvo scan head | `galvo = VP.scanlab_basicube20().translate(V(0, 0, zb1_))` | clear | 155 × 130 × 122 (was 115 × 115 × 110); the top clears the guard roof by 13 mm. The beam input is 30 mm above the mounting face (was 45) and 25.25 mm to the side of the lens axis. So set `P["beam_z"] = P["z_bridge1"] + 30` and move the beam line to y = −25.25: beam tube, shutter, collimator, V-mount and fibre start. The ±y side comes from reading the brochure's views as first-angle; check it on SCANLAB's drawing. |
| Collimator | `coll = VP.ipg_collimator_d5().translate(V(-210, -25.25, P["beam_z"]))`; keep the V-mount block | **hits the guard's left panel, 253 mm³** | 128 mm body + 78 mm strain relief = 206 mm (envelope 130). The relief ends at x = −416, 46 mm outside the panel at x = −370. Either give it a light-tight fibre feed-through in the panel, or fold the beam with a 45° mirror so the collimator lies along y. |
| Vacuum isolation valve (KF-25 angle, pneumatic) | `vv = comp([place(VP.kf_wing_clamp(25), (cx + 18, 0, 70), (0, 1, 0), (1, 0, 0)), VP.mcm_4123K45("+x").translate(V(cx + 18, 0, 70))])` | **hits the guard's right panel, 382 mm³** | The BOM's valve (G7: 4123K45, manual) is a straight 124 mm ball valve with a 138 mm lever. It is not the angle valve that was drawn. Its outlet flange lands at x = 298, past the guard wall at x = 290. Options: buy a KF-25 right-angle valve (BOM G7's "powered KF angle valve" alternative), or carry the line through the guard wall. The clamp's 574 mm³ overlap with the old vacuum port is an artefact of the old 5.5 mm-thick generic flange; it clears once the port is `kf_weld_stub`. |
| Pressure transducer | `VP.mcm_3861N11().translate(V(100, 50, lz1))` | 1,554 mm³ into the lid (the thread; this run was against the older Ø8 lid hole) | The BOM's 3861N11 has a 1/4 NPT male thread. Since this check, the model's lid port changed to a 7/16-20 SAE-4 O-ring boss. Pick a transmitter with an SAE-4 port, or add an SAE-4 × 1/4 NPT female adapter (about 25 mm taller; not drawn). |
| Inlet plenum port, Outlet plenum port, Vacuum port (KF-25) | `kf_stub(25, n)` → `VP.kf_weld_stub(25, n)`, same `place()` arguments | clear (the vacuum port was checked at its older 22 mm stub) | McMaster 5786N23 profile on a 1 in. × 0.065 in. tube. The 5786N23 is 12.7 long, so on the vacuum port's new 10 mm stub (now welded into the adapter plate) it reaches 2.7 mm further into the plate. |
| Overflow port (KF-40) | `kf_stub(40, 16)` → `VP.kf_weld_stub(40, 16)` | 18 mm³ into the funnel block | 5786N25 takes 1.5 in. tube (Ø38.1, not 41.3), and the fitting is 19.05 long. Bore the funnel block Ø38.2 (it is Ø38.0). |
| Overflow clamp (KF-40) | `kf_clamp(40)` → `VP.kf_wing_clamp(40)` | 930 mm³ each into the old port and jar flanges | Artefact of the generic flanges. Also redraw the jar as `VP.kf_weld_stub(40, 90)` plus its blank. The jar's inside drops from ~103 to ~81 cm³ on the 1.5 in. tube. |
| Sealed cyclone + HEPA housing | `filt = VP.mcm_5169K72().translate(V(470, -40, g0 + 20))` (keep the 20 mm stand) | 55 mm³ into the old "Filter outlet (KF-25)" stub | The BOM's housing is Ø95 × 92, not Ø116 × 254, and no cyclone is chosen. Its ports are 1/2 NPSC: the inlet is the side boss and the outlet is the bottom. Both KF-25 filter ports need NPT adapters and move. |
| Dry scroll pump | `pump = VP.mcm_4396K21().translate(V(770, 165, g0))` | 861 mm³ into the old "Pump inlet (KF-25)" | The BOM's pump (G2) is the 4396K21 rotary vane, 368 × 143 × 305 mm: 15 mm taller than the envelope with its inlet, and narrower. Its intake is a flare tee at about (681, 195, g0 + 245), so the KF-25 inlet moves there via a flare-to-NPT adapter and a 4518K49 (as BOM G2 says). |
| Fiber laser source, 500 W single-mode (3U) | `VP.ipg_ylr500_u3().translate(V(-710, ry0 + 30, zr))` with `nu = 4` | **9.8 L overlap with the scan PC above it** | The YLR-500-U3 is **4U (176.5 mm), not 3U**. The 10U rack is full (2 + 3 + 2 + 3 U), so it needs 11U: rack 470 → 515 mm, which keeps the rack top 515 mm above the tray (< 600). The alternative is a 2U DIN drawer. The handles stand 51 mm proud, 21 mm in front of the rack frame. |
| UPS (Eaton 5PX 1500 class, 2U) | `VP.eaton_5px1500rtg2().translate(V(-710, ry0 + 30, zr))` | clear | The real unit is 447 mm deep (envelope 530) and 23 kg (model 25). |

Masses to update in `Part.mass_kg`, taken from the sources:

| Part | Model | Real | Source |
|---|---|---|---|
| ClearPath 231x | 1.6 kg | 0.6 kg | Teknic |
| basiCube 20 | 2.5 kg | 3.75 kg (without objective) | SCANLAB |
| FTH160-1064 | 0.6 kg | 0.8 kg | Thorlabs drawing |
| Eaton UPS | 25 kg | 23 kg | Eaton |

The laser's 40 kg already matches. The 4396K21's mass was not captured.

## What is still not real, and why

The full list, ranked, is in `analysis/out/real-parts/inventory.md`. Of 63 bought-part entries in `build()`:
- 17 are now real in the model;
- 3 more have builders that are not used yet (pump, HEPA housing, transmitter);
- the two leveling-mount entries were already real;
- 41 are still generic.

**Vendor CAD fetched, but not redrawn for lack of time:**
- **Door hardware:** draw latches 1807A61 and hinges 1151A87.
  - The real 1807A61 is 135.5 × 44 × 30.5 mm with its strike, against 24 × 12 × 18 mm drawn per latch.
  - The latch base and strike mount in one plane. The keeper sits on the chamber face 15 mm behind the door's front face,
    so it needs a 15 mm spacer.
  - The drawn hinge is a custom knuckle hinge labelled 1151A87. The real 1151A87 is a 3 × 3 in. two-leaf lift-off hinge.
  - Both are a door redesign, not a one-line swap.
- **Argon solenoids 8077K237:** 41.9 × 94 × 80.9 mm each.
- **Regulator 78595A5:** 91 MB STEP.
- **Pot magnet 5679K95:** McMaster's model is 16 mm tall against the listed 7 mm; not resolved.
- **Ball screw 4566N101:** left as a Ø12 rod.

**No product chosen in the BOM, so there is nothing real to draw:**
- the safety shutter and beam dump (L4);
- the scan PC, DIN drawer and rack;
- the tray dock;
- the overflow jar (KF-40 half nipple, no part number);
- the KF-16 blank;
- the LED bar;
- the "KR-class" Z actuator and its carriage (BOM M3 lists 6638K11 + 6709K33 + 6709K12, which the model doesn't use).

**Blower (G4):** a gas-tight blower of this size was not found.
- The one maker-stated gas-tight pump found near 60 L/min is the KNF N 630.1.2 SP.9 E: 569 × 296 × 315 mm, 45 kg,
  three-phase. It is far too big.
- The 200 × 180 × 230 mm envelope stands for a part that may not exist. G4 needs a decision.

**O₂ and dew point (G6, G9):** small enough to fit the 150 × 160 × 210 mm panel-box envelope, but not drawn:
- Ntron Microx: DIN-rail module 69 × 85 × 57 mm, or panel unit 96 × 96 × 90 mm;
- Vaisala DMT143: Ø28 × 91.6 mm, G1/2.

**Published dimensions exist, but not drawn for lack of time:**
- the M12 sensors (PAM-AP-1H, M12 × 45 mm);
- the Pi HQ camera;
- the load cell;
- the operator controls;
- the D4JL guard lock.

**Guard frame:** the model uses a simplified 20 mm T-slot, while BOM S9 lists 30 mm 5537T97 (written for the older
cabinet). The two should be reconciled.

**Hoses:** drawn as tubes along routed paths. 3497N23 comes only as a 24 in. hose, and the routed lengths were not
matched to it.

## What was assumed and not checked

- **ClearPath connector block:** its length (38.49 mm) is read from an unlabelled drawing dimension.
- **IPG collimator:**
  - the length of the Ø28 output step (8 mm) is assumed;
  - the strain relief's diameters (Ø18 to Ø10) are assumed;
  - the laser's handle positions are assumed.
- **basiCube 20:**
  - mounting holes and the objective ring are not dimensioned in the brochure;
  - the ±y side of the input beam is an assumption.
- **6709K33 rail:** the raceway grooves are not published.
- **4396K21 pump:** the layout is taken from the catalogue photo.
- **Vendor CAD as reference:** used as published. The 5169K72 and 3861N11 files include brackets and cables, so their
  volume comparison is loose.
- **Moving parts:** none of the new parts move except the carriage and nut, and they move with the recoater. The swap
  check ran only in the parked state. Only the Z-servo fix was also checked along the module swap path.
