# A lab-built collection cup for the rePowder atomizer (#269)

On Nov 13 2026 a C63000 bronze run made shot instead of powder. The shot piled up on the stock cup's splash
plate and butterfly valve, just under its seals: it burned the EPDM valve seat and cracked the borosilicate tube
(`atomizer-runs/2026-11-13/` on the analysis branches). AMAZEMET can't give a date for a replacement, so this
folder designs one the lab can make in days to weeks.

**Recommendation: option B, a 316L cup in two welded parts joined by a 3 in sanitary tri-clamp.**
- **The upper part** is a KF-50 stub, a catalogue 3×2 in reducer and a 3 in ferrule. It stays on the cone's KF-50
  outlet, the only seal at the chamber. Below that seal the bore only widens, and nothing inside can catch hot
  metal.
- **The pot** is a 3 in ferrule, a 3 in tube and a turned end cap with an 8 mm floor and an R6 inside corner. It
  holds a loose 304 catch puck and a liner with a 1.5 mm gap to the wall, and comes off after every run with its
  full 72.9 mm opening.
- **Monitoring:** two clamp-on thermocouples feed a 2-channel alarm.
- **Cost:** about $449 in priced catalogue parts, plus standard sanitary fittings, four lathe parts and a milled
  welding fixture.

**Before buying, measure the room under the cone**: the distance from the KF face to the mat with the cone
latched. No photo or video showed it at a known scale. B is drawn 250 mm long for an assumed 300 mm of room.

![four cups under the cone, cut in half](cad/img/lineup.png)

| | Stock (Nov 13) | **B: upper part + pot** | A: catalogue KF nipple | C: quartz rebuild |
|---|---|---|---|---|
| What it is | KF flange, reducer, DN65 butterfly valve (EPDM seat), borosilicate tube between plates | KF-50 stub + 3×2 in reducer + 3 in ferrule; tri-clamp; pot = ferrule + 3 in tube + end cap (R6 inside), puck and liner | KF-50 nipple 160 mm, blank on the bottom; puck and liner | stock plates, fused-quartz tube, a spacer in place of the valve, a sleeve over the top seal, a pan over the bottom seal |
| Seals near the hot metal | valve seat right under the inlet, glass seals top and bottom | the KF O-ring at the cooled cone (40 °C at 816 g of shot); the tri-clamp gasket, 30 mm above an 816 g pile | bottom O-ring next to the puck | glass seals at both ends |
| Shot it takes before its hottest seal reaches 150 / 200 °C | the seat burns at once; the glass cracks if shot reaches it (S cases) | about 495 / 640 g (the gasket); PTFE gasket (260 °C) to about 800 g; the KF O-ring stays under 40 °C | about 120 / 220 g | under 400 g: bottom glass seal 264 °C at 400 g |
| Usable volume above the puck | — | 522 cm³ | 159 cm³ | about 600 cm³ (estimate) |
| Catalogue cost (priced lines) | — | **$449** + sanitary fittings | $198 | about $520 |
| Build | — | 4 lathe parts, 4 TIG welds, 1 milled fixture, hydro and leak tests | order and assemble | turn a spacer and sleeve, cut the quartz; valve removal not checked |
| Edison's ranking | — | best long-term (welded metal) | fastest interim | not recommended |

## How B got here

The design changed three times during the analyses, and each change is recorded in the history:

1. **Floor:** a sharp welded floor corner reached 87 MPa (0.82 of yield) with 816 g of shot. The floor became a
   turned end cap with an R6 inside corner, which brought it to 61 MPa.
2. **Neck:** an independent review of the build documents found that **the 70 mm puck and liner could not pass the
   47.5 mm KF neck** of a cup welded shut below it. Dropping the liner put the hot pile against the pressure wall:
   700 MPa elastic at the contact, so it would yield in every bad run.
3. **Split:** the cup now splits at a 3 in tri-clamp. The pot opens at 72.9 mm, the liner and its gap come back,
   a fused lump can be got out, the KF joint stays made up between runs, and the pot is carried away capped.

## What the analyses show

| Check | Result | Where |
|---|---|---|
| Thermal FEA, CalculiX, 19 cases | B keeps the KF O-ring at 26 / 30 / 40 °C for 100 / 400 / 816 g of shot landing at 1050 °C. The tri-clamp gasket reaches 47 / 116 / 263 °C (pile conductivity 2–20 W/m K: 233–268 °C). **What B can't take is shot held near the KF seal:** 25 g fused in the bore under the joint takes the O-ring to 195 °C, and 100 g to 389 °C. That is why nothing goes inside its top and the shields must be in. A good run (816 g of powder at 400 °C) leaves B's bottom thermocouple at 87 °C, against 107–319 °C for shot. A's bottom O-ring passes 200 °C at about 220 g; C's bottom glass seal reaches 264 °C at 400 g | `analysis/thermal.py`, [`thermal_summary.md`](analysis/out/thermal_summary.md) |
| The Nov 13 failure, reconstructed | 120 g of shot against the stock cup's EPDM seat puts it at 1013 °C, but the glass stays at 50 °C. 300 g that falls into the glass puts it at 931 °C, the bottom EPDM seal at 412 °C, and at least 55 MPa of tension in the borosilicate (short-term strength ~40 MPa): it cracks, as it did | `S_seat_120`, `S_glass_300` |
| Model checks | energy is conserved (558 kJ to within 0.06 kJ at 0.5 s; what leaves only grows), and the pile in the mesh weighs 816.0 g (`analysis/energy_check.py`). Steady film, radiation and surface-flux cases match closed-form answers to 0.001 K (`analysis/verify_axifea.py`). Mesh convergence, checked on the previous iteration of B: a 0.55× finer mesh moved the O-ring peak 0.5 K and the hang-up peak 7 K, on the safe side | `analysis/` |
| Structural FEA, the pot | 9.5 MPa at +1.2 bar (1.5 × relief) and 9.0 MPa under full vacuum. Worst thermal stress with 816 g of shot: 61 MPa, at most 0.53 of yield, at the end cap's R6 corner | `analysis/structural.py`, [`structural_summary.md`](analysis/out/structural_summary.md) |
| Hand calculations | buckling under vacuum 180×+; UG-34 flat head needs 1.4 mm (8 used); the KF clamp gives ~1.8 kN finger-tight against 0.84 kN of separating force at +1.2 bar; the liner keeps ≥1.1 mm of gap when hot; the puck and liner clear the pot's opening by 2.9 / 3.05 mm | `analysis/handcalcs.py`, [`handcalcs.md`](analysis/out/handcalcs.md) |
| Glass (C) | with the pan and sleeve, the glass itself is fine (quartz 0.8–1.3 MPa, borosilicate 5.6 MPa); its bottom seal is what fails | `analysis/structural.py` |
| KF under pressure | standard rings are rated to ~1.5 bar abs (Pfeiffer, Edwards); the relief opens at ~1.8 bar abs, so an over-pressure ring (50 psig) is part of the design | `bom/README.md` |
| Collisions at the KF joint | the upper part goes on and off clear of the cone with the clamp off; a hinged clamp left hanging open hits its flange (38 positions) | `cad/build_gif.py`, `cad/out/build_collisions.json` |
| Lathe CAM | end cap (a blind pocket), puck, liner and tube cut in a 2D stock-removal simulation: no gouges, at most 0.1 mm left, no rapids through stock | `cam/lathe_cam.py`, `cam/out/lathe_*.png` |
| Mill CAM | the weld fixture cut in CAMotics 1.2.0 matches the CAD within the 0.5 mm grid, with a 31 min cycle. The first run found a real bug: nested comments skipped a tool change | `cam/mill_cam.py`, `cam/out/mill_fixture_sections.png` |
| CAD against vendor STEP models | McMaster's KF-50 stubs and 139.7 mm nipple are within 1 % by volume. The A&N stub and Duniway nipple in the BOM had no STEP model to check | `cad/vendor_check.py`, [`vendor_check.md`](cad/out/vendor_check.md) |
| Edison final design check | agrees with the ledge-free design and the alarms. Asked for: no sharp welded floor corner (done); a hydro proof instead of a 1.5× pneumatic one (in the procedure); rate-of-rise targets of about 0.04 / 0.004 mbar/min; low heat input with chills; a safety lanyard; logging the thermocouples, ideally with rate-of-rise logic and a latched trip; and the vendor's written rating for the KF joint with the over-pressure ring | `edison/literature_high_final_design_check.md` |

![build, install, a bad run and removal (shows the earlier welded-shut version; see note below)](cad/img/build_b.gif)

The animation was rendered before the split. It shows B welded shut in one piece, so its install and removal
chapters move the whole cup. With the split, the upper part goes on once that way, and only the pot comes off
each run (`procedure.md` §6, §8).

## Build it

- [`procedure.md`](procedure.md):
  - measure, order, machine, and weld both parts in the fixture with a back-purge;
  - hydro proof, bench soap test, and rate-of-rise on the machine;
  - thermocouple alarms (top 120 °C, bottom 150 °C) and a safety lanyard;
  - install, run limits, and pot removal.
- [`checklist.md`](checklist.md): one printable page for the person at the atomizer.
- [`BOM.md`](BOM.md): every line linked to its catalogue page (prices 2026-11-27); alternatives in
  [`bom/README.md`](bom/README.md).
- [`cad/drawings/collection_cup_drawings.pdf`](cad/drawings/collection_cup_drawings.pdf): B's two parts on
  the tri-clamp, the turned parts, the fixture, and A.
- `cam/gcode/`: lathe programs for the end cap, puck, liner and tube; mill programs for the fixture.
- `cad/out/option_b.step`, `option_a.step`, `machine_cone_section.step`, `cam/out/fixture_b.step`.

## Until B is built

A is all catalogue parts and arrives first, but it is small and its bottom joint sits next to the pile. With its
30 mm puck it takes about 120 g of copper-alloy shot before the bottom O-ring passes 150 °C. A 60 mm puck would
raise that to about 250 g (FEA: bottom O-ring 148 °C, top 92 °C); this variant isn't drawn. Use A for aluminium
runs and small copper charges only, always with the shields.

## Rules this design depends on

1. AMAZEMET's shields lie in the cone's mouth on every run: one for aluminium, more for copper alloys.
2. Nothing sits inside the upper part: no splash plate, no valve, no ledge. On Nov 13 the shot burned the seal
   because it was held right under it.
3. The O₂ hard stop and the plate stop rule from the Nov 13 analysis still apply. B survives a bad run; it
   doesn't prevent one.
4. Replace the KF O-ring after a top alarm, and the tri-clamp gasket after a bottom alarm.

## Still open

- **(measure)** The joint's height above the mat, and the cone flange's OD. Then set `Z_JOINT_FACE` and
  `B["body_len"]` in `params.py` and re-run `cad/build.py`.
- **The gasket margin for a full charge of shot.** PTFE (260 °C) meets the 263 °C worst case only just. The next
  step would be a turned one-piece KF-50 to 3 in tri-clamp adapter, about 33 mm long, in place of the stub, the
  101.6 mm reducer and a ferrule. It raises the joint about 100 mm above the pile and adds capacity. The
  geometry has been checked by hand but isn't drawn or CAM'd.
- The sanitary parts (ferrules, clamp, gaskets, caps) aren't priced yet. Their sizes are the ASME BPE / 3-A
  standard ones drawn here.
- The centring-ring recess depth. McMaster's approximate STEP says 2.6 mm, but that would leave too thin a face
  gap for the 3.81 mm over-pressure ring. 2.0 mm (at most 2.09 mm by the ring) is used.
- Option C assumes the stock valve can be unbolted from its reducer and top plate. Nobody has checked.
- The build animation predates the split (see above).

## Files

| Path | What |
|---|---|
| `params.py` | every size, load and property; the source of each interface number |
| `dims/` | interface sizes measured from the photos and training/teardown video frames |
| `bom/` | 175 catalogue lookups, vendor dimensions from drawings and STEP files, `make_bom.py` |
| `edison/` | design review, precedent search and a final design check (Edison Scientific), with full trajectories; AMAZEMET and national-lab staff names redacted |
| `cad/` | CadQuery model (`parts.py`), checks (`build.py`), renders, drawings, build GIF, vendor check |
| `cam/` | lathe and mill CAM with their simulations |
| `analysis/` | CalculiX thermal and structural FEA, hand calculations, energy audit, verification |
| `run_all.sh` | re-runs everything in order (about an hour on 4 cores) |
