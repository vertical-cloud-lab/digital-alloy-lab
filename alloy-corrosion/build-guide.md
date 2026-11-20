# Building the corrosion setup for the CubXL

Written 2026-10-26 for Ben's request on [#180](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/180)
for a build guide. The build steps were spread over four documents written between 17 and 19
October, and the later ones changed parts of the earlier ones. This file puts them in the order
you would build, with the latest decision in each place:

- [`bom/README.md`](bom/README.md) (19 Oct): what to print and buy, and the fixes found while
  making it. Where the documents disagree, this one wins.
- [`copper/cad/README.md`](copper/cad/README.md) (18 Oct): the cell's CAD, how to print and
  assemble it, and the bench tests.
- [`copper/protocol.md`](copper/protocol.md) §2 (18 Oct): the copper deck.
- [`cubxl-setup.md`](cubxl-setup.md) (17 Oct): the first deck, head and wiring plan.

**Nothing here has been printed, bought or tested.** Every position is a proposal in the CubOS
deck frame of Ben's 2026-10-02 calibration (mm; origin front-left-bottom, +y away from the
operator, +z up), to be re-jogged.

**With four stir modules on the deck** (2026-11-06), follow [`stirrers/BUILD.md`](stirrers/BUILD.md),
and order from [`stirrers/BOM.md`](stirrers/BOM.md). That deck moves tip rack 2 next to rack 1, puts
the stirred stocks in a column at x ≈ 76, and keeps only DI water and acid in the 9-position holder.
It changes §4's table, and adds a staging move to every protocol.

**Deck keys** (2026-11-09): every printed deck part now has press-fit key pockets underneath, and
keys that drop into the PandaDeck's slots, as on the stir modules. Making room for them made the tray
2 mm taller (coupon face at z 22) and moved the tube rack's rows 8 mm back. See
[`bom/deck-keys.md`](bom/deck-keys.md), and §4 below.

**Which deck.** On 22 October Sterling put copper corrosion first for the CubXL
([byu-vcl#298](https://github.com/vertical-cloud-lab/byu-vcl/issues/298#issuecomment-6352253304)),
so §4 lays out the copper deck. The aluminium deck uses the same printed parts. It differs only
in the stocks, the cups in use, station S4 and the tip waste.

## What changed since the first plan

| The 17–18 Oct documents say | Build this | Why |
| --- | --- | --- |
| `copper/cad/well_lid.step` | [`bom/cad/well_lid_v2_006.step`](bom/cad/well_lid_v2_006.step) (P03) | The old lid's O-ring sits on a 0.2 mm printed ledge, which sees about 200 MPa at the nominal load, four times PETG's yield. The v2 lid's 0.6 mm ceiling sees about 24 MPa |
| Two wells per lid, 9 mm apart | One well per lid | The 16 mm boss that centres the cap leaves no room. A second well on a piece needs a second tray load until someone draws an offset lid |
| A radial O-ring seals the cap (first copper draft) | The clearance cap, P01, with no O-ring | Pulling the O-ring cap off takes 2.3–85 N, and the electromagnet gives about 23 N on a 1 mm disc. The O-ring cap (P18) is a fallback only |
| P75 pogo pins on the cap | Same Sky CPG-37 pins (B06) on the cap; P75s only in the tray | The cap needs at most 0.4 N per pin; P75s are about 1 N |
| Reference tip 1.5 mm above the metal | 3.0 mm, up in the bore | 22 % more oxygen at the spot and a more even current, for about 2 mV more iR at a 1 mA/cm² reversal |
| Brass eyelets | 6 mm pins cut from 1/16 in brass rod (B12) | No 1.6 mm eyelet or rivet long enough for a 6 mm lid turned up |
| Area from the O-ring's ID, 0.0661 cm² | Each spot's wetted area, measured from its attack ring | The squeezed ring wets 0.101–0.126 cm² |
| Tray 19.5 mm tall, coupon face at deck z 20; then "give it 2 mm feet" | Tray 21.5 mm tall, coupon face at z 22, flat underside (2026-11-09) | The P75 pins are 16 mm long, so their tails ended 1 mm below the old tray. Feet would have lifted its key pockets off the keys |
| Tape the parts down; pins or pill mounts later | Deck keys in every deck part, plus thin tape under the tray and the cup block | The keys put a part back in the same place. They don't hold it down, and the electrode cap's magnets pull on those two ([`bom/deck-keys.md`](bom/deck-keys.md)) |
| Tube rack at y 20–54, tubes at y 28 and 46 | y 28–62, tubes at y 36 and 54 | The slot row at y 45 ran under the back row's tube tips |
| A 16.6 mm reference with a contact on top, soldered to the wire-wrap at the cap's axis | A 15.5 mm barrel with a bare silver-wire lead, joined to the −x pin's wire-wrap at the mouth of that pin's hole (2026-11-10) | The vendor makes one this short only with a silver-wire connector, without the strain relief and pin, which add 20 mm. The shorter barrel leaves about 1.8 mm of straight wire before the bend into the groove, not 0.7 mm |

## 1. Print

**On the A1 mini in PLA:** [`bom/a1-mini/`](bom/a1-mini/README.md) has every part below on four
sliced plates, plus an optional fifth, with the magnet pauses set. Its README says what changes
with PLA (2026-11-06).

**On the H2D in PLA, all at once:** [`bom/h2d/`](bom/h2d/README.md) has every part the lab doesn't
already have (no vial caps, tip rack, vial holder or stirrer prints) on one sliced plate: 28 pieces,
11.4 h, with both magnet pauses set. Check the fits after it prints (2026-11-06). Since 2026-11-09 the
plate has the keyed parts and ten deck keys: 38 pieces, 12.3 h, 362 g.

For every part ([`copper/cad/README.md`](copper/cad/README.md#printing-and-assembly)): PETG for
anything that touches liquid, 0.12–0.16 mm layers, 100 % infill for the lids and the cap (four
walls around every wetted bore elsewhere), slow outer walls. One 1 kg spool covers all of it: the
parts come to about 0.48 kg.

1. **Calibrate the printer's hole and boss diameters** on a test coupon. The cap's 0.12 mm
   clearance over the boss depends on them.
2. **Print the fit strips (P12) before the racks**, on the printer and filament the racks will
   use. Pick the hole that holds a real tip, or a real tube, by its collar without play. Set
   `TIP["hole_d"]` or `TUBE["hole_d"]` in [`bom/cad/cad_build_parts.py`](bom/cad/cad_build_parts.py),
   rerun it, then print the racks. For tip rack 2, print a second rack 1 instead of P11. It fits like
   rack 1 and is already keyed. Print it from [`bom/cad/tip_rack_1_20ul.step`](bom/cad/tip_rack_1_20ul.step),
   Ben's version from his Onshape document "20uL tip rack", with a 60 × 35 mm window in each side wall
   ([`bom/tip-rack-1.md`](bom/tip-rack-1.md)).
3. **Print the rest.** STEP and STL links for each part are in
   [`bom/README.md` §1](bom/README.md#1-what-to-print).

| ID | Part | Qty | On the bed | Pause for magnets |
| --- | --- | --- | --- | --- |
| P01 | Electrode cap | 2 | skirt down | — |
| P02 | Electrode carrier | 3 | flange down | — |
| P03 | Well lid v2, AS568-006 | 5 | bottom face down; no seam on the boss, which guides the cap | at z 5.6: two 4 × 2 mm magnets, same pole up |
| P06 | Coupon tray | 1 | the pocket floors must come out flat: they set the coupon face at deck z 22 | — |
| P07 | Shims, 1 and 3 mm | 4 + 4 | | — |
| P08 | Cup block: rinse 2, rinse 1, park | 1 | four walls around the bores | at z 44.6: six magnets, same pole up as the lids |
| P09 | Tip waste cup | 1 | | — |
| P10, P11 | Tube rack; tip rack 2 | 1 each | after step 2 | — |
| P13 | Magnetic vial caps (PANDA-BEAR's file) | 8 | PLA, with the PDMS fill and steel disc of the [capper module's BOM](https://github.com/vertical-cloud-lab/byu-vcl/blob/f1b4666/modules/electromagnetic-capper/BOM.md) | — |
| P14 | 9-position 20 mL holder (PANDA-BEAR's file) | 1 | only if the deck has no full holder yet | — |
| P04, P05 | Well lids v2, AS568-008 and -010 | 1 each | as P03 | as P03 |
| P15–P17 | Bench cell body, clamp and cover | 1 each | body floor down; leak-test it with DI water overnight | — |
| P19 | Deck keys, 0.05 mm press (plus one 0.10 and one 0.15 to test the fit) | 7 (9 with P11) | pill down, nub up, solid | — |

P04 and P05 are the copper calibration's larger wells, run on the CubXL. P15–P17 are the 1 cm²
bench cell they are compared with
([`copper/protocol.md` §5](copper/protocol.md#5-calibrate-first)).

## 2. Post-process and assemble

### The electrode cap (P01 and P02)

From [`copper/cad/README.md`](copper/cad/README.md#printing-and-assembly), with the BOM's
substitutions:

1. **Open the reference bore** to 2.05 mm by hand, with a #46 drill (2.06 mm, B47) in a pin vise.
2. **Open the two 1.0 mm pin holes from below for the CPG-37 pins** (B06): a Ø2.1 counterbore
   1.57 mm deep for the flange and barrel, then Ø1.6 × 1.1 mm for the tail. Leave the 1.0 mm hole
   above it for the wire. *Corrected 2026-11-09:* this step used to say "open the bottom 2.2 mm to 1.3 mm".
   The [datasheet](https://www.sameskydevices.com/product/resource/cpg-37-th-tr.pdf) pin has a
   Ø2.00 flange and a Ø1.50 tail and stands 2.20 mm free. Mounted the old way it would bottom out
   and hold the cap 1 mm off the lid ([`build-animation/parts-check.md`](build-animation/parts-check.md)).
   Solder the wire-wrap to the tail before pressing the pin in.
3. **Press two steel slugs** into the pockets in the skirt's underside, with a drop of
   cyanoacrylate: 3 mm drill rod (B10) cut to 2 mm, or any 3 mm steel pin. The lid's magnets
   pull on them to hold the cap down.
4. **Wind the counter:** five turns of 0.25 mm Pt wire (B21) on a 5.0 mm mandrel. Tie the coil to
   the carrier's three legs and take its lead up through the carrier's 0.6 mm hole. Press the
   carrier into the cap.
5. **Fit the reference:** push the leak-free 2 mm Ag/AgCl (B19) in from the top, tip first, until
   it stands 3.0 mm below the skirt, which puts its tip 3.0 mm above the metal. Its bare silver
   wire stands up out of the bore. Bend it 90° where it reaches the groove's floor, about 2 mm
   above the barrel, and lay it along the −x groove to the −x pin's hole. Seal the barrel's top
   and the bend with a dab of neutral-cure RTV silicone (H05), no higher than the recess floor.
6. **Fit the two spring pins** (B06) at x ±11 mm, each set 0.2 mm recessed so it sits at
   mid-stroke when the cap is seated. Each pin's 30 AWG wire-wrap (B15) comes up its hole to the
   recess floor.
   - **−x, the reference:** join the wire-wrap to the silver wire at the hole's 1.6 mm mouth,
     about 13 mm along the silver wire from the barrel, and tuck the joint into the mouth. Solder
     it only if the vendor says the electrode takes the heat at that distance; otherwise use
     silver-filled conductive epoxy. The reference input draws almost no current, so the joint's
     resistance doesn't matter.
   - **+x, the counter:** run the wire-wrap along the +x groove to the coil's lead and solder them.
   - **Keep both bare leads down in their grooves,** under the disc's adhesive. If both touched
     the steel disc, it would short the reference to the counter.

   The reference's pin lands on the lid's −x pad and the coil's pin on the +x pad.
   *Changed 2026-11-10:* these two steps used to solder the wire-wrap to a contact on the
   reference's top. The vendor makes a reference this short only with a bare silver-wire lead
   and no pin ([BOM B19](bom/README.md#electrodes)).
7. **Glue the steel disc on last** (1 in × 1 mm, self-adhesive, B09). It is what the
   electromagnet lifts.
8. **Mark an index on the cap.** The lid's magnets hold it at 0° or at 180°, and 180° swaps the
   reference and counter pads, so set it by hand at the park cup. The OCP check at cap-on
   ([`copper/protocol.md` §4](copper/protocol.md#4-sequence), step 3) catches a cap set down
   backwards.

The finished cap weighs about 13.5 g. Carried by the capper, it hangs 35.8 mm below the
carriage.

### The well lids (P03–P05)

1. **Check the counterbore's ceiling**, where the O-ring seals. If the bridged layer came out
   rough, face it flat with a 7 mm flat-bottom drill or end mill (B48) in a drill press.
2. **Pins for the pads:** cut 6 mm lengths of the 1/16 in brass rod (B12) and press them through
   the lid's two 1.6 mm holes at (±10, 15).
3. **Pads:** lay copper-foil tape (3M 1181, B11) at r 10–12 mm, within ±30° of +x (the counter
   pad) and of −x (the reference pad), each with a tail along y to its brass pin. Solder each tail
   to the top of its pin.

### The tray (P06)

1. **Melt in the M3 heat-set inserts** (B13), two per station, at y ±14.
2. **Fit the P75-B1 spring pins** (B07): one working-electrode pin up through each pocket floor,
   and two per station under the lid's brass pins. That is 12 in all. They are 16 mm long
   ([`build-animation/parts-check.md`](build-animation/parts-check.md)), so the tray was made 2 mm
   taller on 2026-11-09. A WE pin's tail now ends 1 mm above the deck, inside its bus channel.
3. **Press the two deck keys (P19) into the pockets under the front edge,** triangle to triangle
   ([`bom/deck-keys.md`](bom/deck-keys.md#fitting-them)). The tray's pockets are turned 180° from the
   other parts', so its keys go in the other way round.
4. **Wire the pins** in the 4 × 3 mm channels underneath with 26 AWG silicone wire (B16): the
   four working-electrode pins on one wire, the four reference pads on another, the four counter
   pads on a third. The cap is only ever on one station, so three wires serve all four. They leave
   at the tray's back edge, at x 222.5, where the JST-XH 4-pin plug goes (B18).
5. **Run the shielded cable** (Belden 9534, 3 ft, B17) from the plug to the potentiostat: WE, RE,
   CE and a spare. Connect the shield at the potentiostat's ground only.

### Loading a station

Put the piece face up in its pocket, with shims (P07) under a thin piece so its face sits at deck
z 22. Seat an AS568-006 O-ring (B01) in the lid's counterbore, put the lid on, and fit two
M3 × 8 screws (B14), finger-tight with a hex key (about 30 mN·m). On the copper deck S4 holds a
PTFE disc instead, a 6 mm slice of 3/4 in rod (B46), for the night's blanks.

## 3. Bench tests, before the cap goes on the deck

The six from [`copper/cad/README.md`](copper/cad/README.md#still-needs-a-bench-test). Each
replaces an estimate:

1. The force to lift the cap off a lid against its pins and the lid's magnets (estimated
   2.4 N), and the electromagnet's pull on the real disc at shimmed gaps of 0–0.4 mm (estimated
   22.8 N at contact on a 1 mm disc). Use a force gauge.
2. The cap's water loss: weigh a filled, capped well over 2 h (estimated 1.6 µL/h).
3. The pins' spring force at 0.93 mm of stroke, and their contact resistance on the foil pads.
4. The wetted area under the squeezed O-ring on a polished coupon, by dye or by an attack ring
   (estimated 0.101–0.126 cm²).
5. A leak check of the face seal on each alloy's finish.
6. Whether the capper's IR beam sees the electrode cap, and the decap height that touches the
   disc.

## 4. On the deck

**First, on Ben's current deck,** remove the two vials at x 137: the capper rides over that column
while the pipette works at the tray. Tip rack 1 stays where it is.

**Every keyed part lands about 1.9 mm in front of the coordinates below** (2026-11-10). Rack 1's key
pockets put the slot rows at y 43.13 + 45m, not 45m. The table keeps the planned numbers. The
corrected ones are in [`bom/tip-rack-1.md`](bom/tip-rack-1.md#where-the-rest-of-the-deck-sits).

| Item | Where (x, y) | Copper | Aluminium |
| --- | --- | --- | --- |
| Coupon tray (P06) | x 170–275, y 220–260; S1–S4 at x 185 / 210 / 235 / 260, y 240 | S1–S3 pieces; S4 the PTFE blank | four pieces |
| 9-position 20 mL holder | x 318; vials at y 35 + 33k | y 35 spare (FeSO₄, non-sulfide nights only); 68 1 M trace-metal HNO₃; 101 ASW; 134 ASW + 10 mg/L S; 167 ASW + 0.1 mg/L S; 200 DI water; **233 and 266 empty** | 101 0.6 M, 134 0.06 M and 167 0.006 M NaCl; 200 DI water |
| Cup block (P08) | cups at (30, 245), (60, 245), (90, 245) | rinse 2 (ASW), rinse 1 (DI), park | rinse (60) and park (90) |
| Tube rack (P10) | x 170–266, y 28–62; tubes at x 176 + 12k, y 36 and 54 | one tube per well, plus the stock blanks | one tube per spot |
| Tip rack 1 | Ben's, unmoved: A1 (291.3, 89) | | |
| Tip rack 2 (a second rack 1, [`tip_rack_1_20ul.step`](bom/cad/tip_rack_1_20ul.step); or P11) | A1 (266.332, 89), A2 (257.832, 89): keyed one slot column left of rack 1, as on the stirrer deck | | |
| Tip waste (P09) | | (385, 150) | (335, 60): its key needs a slot, so not (335, 40) |
| Potentiostat | x 0–80, y 290–330, outside the working volume | | |

The copper vials at y 233 and 266 stay empty because they sit under the bare pipette while the
capper sets the cap on S4.

1. **Key the parts in.** Press the deck keys (P19) into each part's pockets and drop the part's keys
   into their slots ([`bom/deck-keys.md`](bom/deck-keys.md)). **Also tape the tray and the cup block
   down** with thin double-sided tape (0.15 mm or less, clear of the pockets). The keys only locate a
   part, and lifting the electrode cap pulls up 1.0–1.7 N on those two, more than tips them.
2. **Teach every position, and pin the slot mapping:** jog the pipette over two PandaDeck slot
   centres, and set `GRID_X0` and `GRID_Y0` in [`bom/cad/deck_keys.py`](bom/cad/deck_keys.py) if
   they differ from X = 12.5 + 25n, Y = 45m. Then rerun
   [`copper/deck_cu.py`](copper/deck_cu.py) (or [`plot_deck_layout.py`](plot_deck_layout.py) for
   aluminium) with the real numbers. In their own geometry their tool-shadow checks pass 118 and
   99 tool-down events with no collision (rerun 2026-11-09 with the taller tray and the moved tube
   rack).
3. **Jog the decap height** to the top of the cap's disc, within about ±0.15 mm. That is tighter
   than vial caps need, because the lid's magnets hold the electrode cap down.
4. **Open every tube's lid fully,** so it hangs over the rack's edge: front row forward, back row
   back. A lid standing at 90° reaches z 50, above the 43 mm the capper rides at over the rack
   during tip pickup.

Heights to expect: coupon face z 22, lid top 28, boss top 32. With the cap seated its flange is at
z 40 and the top of its disc, the magnet contact, at 44. (All 2 mm higher than before 2026-11-09.)

## 5. Software and the first electrical checks

1. **Write the CubOS deck file** from the draft in
   [`cubxl-setup.md` §6](cubxl-setup.md#6-electronics-and-software), with the copper stocks above.
   Each station and cup is a `vial` with a magnetic cap, so `decap` and `cap` work unchanged.
2. **Run CubOS `validate_setup`** on a protocol that moves the cap park → S1 → rinse → park and
   fills S1 from two stocks. It is the real version of this folder's static checks.
3. **Measure a dummy cell** (10 kΩ and 1 µF, B26) at the end of the bus with the steppers
   energised, as they will be during a measurement, before trusting a nanoamp.
4. **Rules that go into every protocol,** since the deck checks assume them: cap moves only with
   no tip on the pipette; the cap on at most one station; while S_k is measured, the pipette works
   only at S_(k−1), the vials, the tubes or the racks; the cell switched off before every cap
   move.
5. **No unattended nights** until the potentiostat has a firmware or host timeout that opens the
   cell.

## 6. The potentiostat

- **Now: Dr. Porter's EZstat-Pro,** borrowed and beside the CubXL. Its ±1 µA range reads in 37 pA
  steps, fine enough for the well. It runs only from its Windows PC, because its NI-DAQmx driver
  has no build for the Pi's ARM processor, and the PC is reached through the CubXL Pi by Remote
  Desktop. Checks C1–C6 in
  [§7 of byu-vcl PR #291's runbook](https://github.com/vertical-cloud-lab/byu-vcl/blob/9280485/potentiostat/ezstat-pro/README.md#7-corrosion-checks-for-the-alloy-work)
  take it from a 10 kΩ resistor to the first CubXL well against the bench cell. Whether it may
  be used in salt water is still a question for Dr. Porter.
- **To run from the Pi under CubOS,** one of the BOM's three options: the EmStat Pico module (B23,
  in box B24), which the aluminium plan picked; the Pico development kit (B25), which the copper
  plan prefers because the galvanic (ZRA) test needs its second channel; or a MYSTAT build (B27),
  the cheapest, with no EIS. Not the Rodeostat HC: its lowest range steps in 4.9 nA and does not
  autorange.
- **CubOS needs three additions whichever is chosen:** a linear-sweep technique, scan rates below
  1 mV/s, and reversal at a current threshold. All three can be written against its simulation
  driver now ([README §5](README.md#5-which-potentiostat-what-corrosion-needs-input-for-231)).
- **Reference electrodes:** Dr. Porter's lab has none to lend. The leak-free 2 mm reference (B19)
  is being quoted as a 15.5 mm barrel with a bare silver-wire lead (BOM B19); B20 is the master
  it is checked against.

## Still open

- Nothing has been printed. The fits, the bench cell's seal and the cap's seating on a cup all
  need a first print.
- One well per lid: no offset lid has been drawn.
- The copper well simulation has not been rerun for the v2 lid's neck.
- Prices still to get: a quote for the leak-free reference (B19) and the C95800 bar (B45), and
  the drill rod (B10), PTFE rod (B46) and 7 mm drill (B48).
- The four working-electrode pins share one wire, so only the well being measured may be wet.
  Filling wells ahead of time needs a 4-channel relay board, which is in the first plan's
  [`bom.csv`](bom.csv) as optional but not in [`bom/bom.csv`](bom/bom.csv).
