# Build guide: the copper corrosion setup with four stir modules

Ben asked on [#180](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/180)
(2026-11-06) for a build guide to follow as soon as the parts in [`BOM.md`](BOM.md) arrive. It
covers the deck in [`README.md`](README.md): four compact stir modules in a column where tip rack 2
was planned, with both tip racks side by side. Where it doesn't say otherwise, follow
[`../build-guide.md`](../build-guide.md) for the corrosion cell and byu-vcl's
[`BUILD.md`](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/BUILD.md)
for each stirrer. This guide gives the order, and what is different with four stirrers.

**Nothing here has been built or run.** Every deck position is a proposal in the CubOS deck frame
of Ben's 2026-10-02 calibration (mm; origin front-left, +y away from you), to be taught.

| Stage | What | Needs |
| --- | --- | --- |
| [1](#1-print) | Print the corrosion plates and the stirrer parts | A1 mini |
| [2](#2-build-the-cell-and-bench-test-it) | Electrode cap, lids, tray; six bench tests | the cell parts |
| [3](#3-build-stirrers-b-c-and-d) | Three more stirrers, each tested on stirrer 1's pins | the stirrer parts |
| [4](#4-the-hub-at-the-uno) | Four sockets at the Uno | perfboard, JST-XH |
| [5](#5-the-four-stirrer-firmware) | Firmware that drives four, one at a time | **not written yet** |
| [6](#6-set-up-the-deck) | Everything on the deck, cables routed | |
| [7](#7-teach-and-check) | Teach positions, write the deck file, run the checks | the Pi |
| [8](#8-the-rules-every-protocol-follows) | The rules every protocol follows | |
| [9](#9-the-ezstat-pro) | Wire the tray to the EZstat-Pro | |
| [10](#10-first-runs) | Water first, then a real spot | |

## 1. Print

1. **Corrosion parts, in PLA:** plates 1–4 of [`../bom/a1-mini/`](../bom/a1-mini/README.md). Plate 1
   first: its cap-over-boss and fit-strip checks decide whether the others print as they are.
   Plate 3 has tip rack 2 (P11); if the file for Ben's tip rack 1 exists, print another of those
   instead, since it already fits.
2. **Stirrer parts, in PETG:** the set in [`BOM.md` §3](BOM.md#3-print), with byu-vcl `BUILD.md`'s
   settings (4 walls, 30 % infill, the carrier at 100 %, 0.15 mm elephant-foot compensation).
   Check them as its [stage 1](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/BUILD.md#1-print-the-parts)
   says: each key slides into a deck slot, each nub starts in its pocket, a vial clicks into each
   holder, and a fan drops into each base.

**Which base goes where.** Stirrer A is the one already built, on a 2026-10-28 base, with its cable
notch in the −Y wall. It goes at the front of the column with that wall facing you, so its cable
leaves toward the front edge. B, C and D get the 2026-11-04 base, with the notch in the −X wall,
facing left. D reuses the 2026-10-30 print's holder, carrier and keys on a new base. Its old base
has the −Y notch, which in the middle of a column would trap the cable between two stirrers.

## 2. Build the cell and bench-test it

Follow [`../build-guide.md`](../build-guide.md) §2 and §3 as they are: the electrode cap (P01, P02),
the v2 well lids (P03–P05), the tray (P06) and its 3-wire bus, then the six bench tests. Two changes:

- **Inserts and connectors come from the stirrer order:** the tray's M3 heat-set inserts (B13) are
  the stirrer BOM's item 11, and its JST-XH plug and socket (B18) are a pair from item 9.
- **The bench cell (P15–P17) gets built too:** [`../copper/protocol.md` §5](../copper/protocol.md#5-calibrate-first)
  calibrates the well against it before the first real spot.

## 3. Build stirrers B, C and D

Build each as byu-vcl `BUILD.md` builds the compact stirrer: keys pressed in, four inserts,
magnets in the carrier with opposite poles up, the junction board wired hole for hole from its
diagram, the bench check, then the assembly. Do the stages in its order; the
[measure-first list](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/BUILD.md#measure-first)
applies to each fan and each batch of washers.

What is different here:

1. **Label each stirrer A, B, C or D** on its base, and each cable's Uno end with the same letter.
   The letter sets its pins at the Uno (stage 4) and its place on the deck (stage 6).
2. **Cable length:** measure each route from its place in the column to the Uno, clear of the
   gantry, before cutting. The column's left edge is at deck x 51.5, so B, C and D leave from the
   left; A leaves from the front.
3. **Test each new stirrer on stirrer 1's pins, today, before any firmware change.** Unplug A at
   the Uno, plug the new stirrer into A's socket (D10/D2), and run byu-vcl `BUILD.md`
   [stage 8](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/BUILD.md#8-first-spins):
   no vial at 300 and 1200 rpm, then a vial of 10 mL of water with the bar on the Ø15 × 4.6 mm
   spacer, three starts from rest at 300 rpm. The Uno already runs the stirrer image (flashed
   2026-11-03), so this works now, and it proves each stirrer before stage 5. Plug A back in after.
4. **A spacer in every holder.** On 2026-11-05 the vial only started from rest once it sat 4.6 mm up.
   Seated, the bar's pull stalled the fan. Glue nothing: the spacer just sits on the cup's floor.

## 4. The hub at the Uno

From byu-vcl#269's [four stirrers on one Uno](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/README.md#four-stirrers-on-one-uno).
The Uno has one 5V pin, so the four cables meet at a small hub.

1. **Look first.** Check that nothing is soldered to D5, D6, D7, D8, D12 or A5 on the Uno or a shield.
   The firmware claims D5–D7 for NeoPixel dots and the line-break LED, which aren't wired. If they
   are, pick other pins and say so on byu-vcl#269.
2. **Build the hub** on one perfboard strip (item 10): four JST-XH sockets (item 9, the half with
   recessed contacts), a 5V rail and a GND rail joining every socket's pins 1 and 2, and one lead
   from each rail to the Uno's 5V and a GND pin.
3. **Signal leads,** each socket's pin 3 (gate) and pin 4 (Hall) to its own pins:

   | Stirrer | Deck place | Gate (pin 3) | Hall (pin 4) |
   | --- | --- | --- | --- |
   | A (stirrer 1, built) | front, y 45 | **D10** | **D2** |
   | B (stirrer 2) | y 90 | **D5** | **D8** |
   | C (stirrer 3) | y 135 | **D6** | **D12** |
   | D (stirrer 4) | back, y 180 | **D7** | **A5** |

   Use male pins on the leads (half a male–male jumper each) into the Uno's headers, or the proto
   shield's pads if it is fitted.
4. **Meter it unpowered:** 5V to GND is not a short, and each socket's pins 3 and 4 reach only their
   own Uno pins.
5. **Plug in only A until stage 5 is done.** Today's firmware drives D7 high at boot whenever the
   line-break beam is broken, and leaves it there, which would run stirrer D flat out. D13 stays
   free: the bootloader blinks it on every reset.

**Current:** one fan at a time stays under 0.1 A, and the four Hall sensors add up to 20 mA, well
inside the Uno's 500 mA USB fuse. Don't run two fans at once off the Uno.

## 5. The four-stirrer firmware

**Not written yet.** Until it is, the Uno drives stirrer A only, and B–D can be tested one at a time
on A's socket (stage 3). What it has to do, from byu-vcl#269's plan:

- Timer1 stays the 200 Hz clock (fast PWM, TOP 1249, clk/64). Its overflow and compare-B interrupts
  switch the running stirrer's gate pin in software and sample that stirrer's Hall pin 200 times a
  second, counting falling edges. The speed loop is unchanged.
- `30,<stirrer>,<rpm>[,<seconds>]` starts one stirrer and stops any other; `31` also says which one
  runs. Drop the two NeoPixel dots and the line-break LED; keep the ring on D3 and the sensor on D4.
- It fits: the one-stirrer image uses 20,340 of 32,256 bytes of flash.

**To get it:** ask `@claude` on byu-vcl#269 to write it, build it on the CubXL Pi, and run it in
`firmware/uno_sim` against the fan model before anything is flashed. Then flash it the way byu-vcl
`BUILD.md` [stage 7](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/BUILD.md#7-flash-the-uno)
does: `HOLD` file, read the board back, verify it is the image you expect, write, check `31` and
`14` answer, run `pipette_test`, remove `HOLD`. Then plug in B, C and D and spin each at 300 rpm for
30 s with water in its vial.

**The other way,** if the shared Uno shouldn't change: a Seeed XIAO RP2040 in each stirrer, each
on its own USB to the Pi (byu-vcl `firmware/main.py`, untested). That costs about $40 for four
XIAOs plus their USB cables, but lets stirring run during a CubOS run, which the Uno can't do
([stage 8](#8-the-rules-every-protocol-follows)).

## 6. Set up the deck

Start from Ben's deck: take off the two vials at x 137, as [`../build-guide.md` §4](../build-guide.md#4-on-the-deck)
says. Tip rack 1 stays where it is. Then, from the back of the deck to the front:

| Item | Where (deck x, y) | Notes |
| --- | --- | --- |
| Coupon tray (P06) | x 170–275, y 220–260; S1–S4 at x 185 / 210 / 235 / 260, y 240 | S1–S3 the pieces, S4 the PTFE blank |
| Cup block (P08) | cups at (30, 245), (60, 245), (90, 245) | rinse 2 (ASW), rinse 1 (DI), park |
| **Stirrers A–D** | vials at x ≈ 76; y 45, 90, 135, 180 (bases x 51.5–100.5, 44 mm deep) | keys in the slot pair either side of x 76. A at the front, cable forward; B–D with the −X wall to the left |
| **Tip rack 1** (Ben's) | unmoved: A1 (291.332, 89), A2 (282.832, 89) | |
| **Tip rack 2** (P11) | **A1 (266.332, 89), A2 (257.832, 89)**: one slot column (25 mm) left of rack 1, 5 mm gap | was planned at x 99.5–108 |
| 9-position holder | x 318: **DI water at y 35, 1 M HNO₃ at y 68**; the rest empty | from y 101 back, drawing from it would put the capper on tip rack 2 |
| Tube rack (P10) | x 170–266, y 20–54 | open each lid fully, hanging over the edge |
| Tip waste (P09) | (385, 150) | |

**What goes in the stirred vials** (20 mL VOA vials with magnetic caps, a 15 × 6 mm bar and the
spacer in each):

| Stirrer | Copper nights | Aluminium nights |
| --- | --- | --- |
| A, y 45 | ASW (D1141, no heavy metals) | 0.6 M NaCl |
| B, y 90 | ASW + 0.1 mg/L S | 0.06 M NaCl |
| C, y 135 | ASW + 10 mg/L S | 0.006 M NaCl |
| D, y 180 | spare: FeSO₄ conditioning on non-sulfide nights only (never on the deck with sulfide) | spare |

**Fill each stirred vial to about 15 mL.** A night's eight wells take at most 1.2 mL from one
stock. Draw at `height: -20` (20 mm below the rim), as the stir trial dispensed, not the −35 of
`pipette_test`: the bar lies on the vial's floor, and the spacer has raised the floor 4.6 mm. Teach
the draw height on a filled vial so the tip is well under the surface and well above the bar.

**Route the stirrer cables** flat along the deck's left and front edges, taped, never across a
path the head or its cables sweep, to the hub at the Uno. A's goes forward from y 23. B, C and D's
go left from x 51.5.

**Tape the flat-bottomed corrosion parts down** until the slot mapping is pinned, as
[`../build-guide.md` §4](../build-guide.md#4-on-the-deck) says. The stirrers' keys locate them.

## 7. Teach and check

1. **Teach:** jog the pipette, with a tip, over each stirred vial's centre and its rim, with the
   spacer in. The model has (76, y) and rim z 67.6 (63 seated + 4.6). Ben's first stirrer taught at
   x 126 and rim 66, so expect a couple of mm either way. Teach tip rack 2's A1 and A2, and two
   PandaDeck slot centres for the rest of the deck.
2. **Rerun the plan check with the taught numbers:** set `STIR_X`, `STIR_Y`, `STIR_RIM` and
   `TIP_RACK_2` in [`deck_stir.py`](deck_stir.py) and run it. It must still say 0 rigid-head problems,
   and every staged fill passing.
3. **Write the CubOS deck file.** Start from the draft in [`../cubxl-setup.md` §6](../cubxl-setup.md#6-electronics-and-software)
   with the copper stocks, and add:

   ```yaml
   labware:
     stir_A: {type: vial, name: stir_A, height: 83, diameter: 28, location: {x: 76, y: 45, z: 67.6}, capacity_ul: 20000}
     # stir_B, stir_C, stir_D at y 90, 135, 180: taught x, y and rim z
     tip_rack_2: {type: tip_rack, model_name: panda_2x15_tip_rack, rows: 15, columns: 2, calibration: {a1: {x: 266.332, y: 89.0}, a2: {x: 257.832, y: 89.0}}, pickup_z: 59}
     water: {type: vial, name: water, height: 83, diameter: 28, location: {x: 318, y: 35, z: 56}, capacity_ul: 20000}
     acid:  {type: vial, name: acid,  height: 83, diameter: 28, location: {x: 318, y: 68, z: 56}, capacity_ul: 20000}
   positions:   # pipette frame: stirred vial + (95, 11), at travel height
     stage_A: [171.0, 56.0, 87.0]
     stage_B: [171.0, 101.0, 87.0]
     stage_C: [171.0, 146.0, 87.0]
     stage_D: [171.0, 191.0, 87.0]
   ```

4. **Before the first run that visits a stirrer,** run on the Pi, as for every new deck: the
   checks-only pass of `cubxl_run.py` (`validate_setup`, the mock run, `passive_shadow`), then
   byu-vcl's [`tip_clearance.py`](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/cubos/tools/tip_clearance.py)
   and [`capped_vial_keepout.py`](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/cubos/tools/capped_vial_keepout.py)
   once per stirred vial (`--vial stir_A`, then B, C, D). The first three stay green however high a
   vial stands. `tip_clearance.py`'s height margin over a capped stirred vial proved too generous
   (Ben, 2026-11-05), so the keep-out check is the one that has to pass.

## 8. The rules every protocol follows

1. **Stage before going back to a stirred vial.** CubOS moves X first, then Y, so a move into the
   column ends with a Y leg along the column, over the other stirred vials. With a tip on, the tip
   won't clear their caps. So before every `aspirate` from a stirred vial, and before every `cap`
   of one, send the pipette to that vial's stage point:

   ```yaml
   - move: {instrument: pipette, position: stage_A, travel_z: 87}
   - aspirate: {position: stir_A, volume_ul: 18.75, height: -20.0}
   ```

   The one exception: an `aspirate` straight after that vial's own `decap`, which leaves the pipette
   in the vial's row already. In [`deck_stir.py`](deck_stir.py)'s walk of every fill (four stocks,
   three wells, the stock opened before or after the tip goes on, eight transfers), **21 of 24 fills
   take the tip straight over a capped stirred vial without staging; with it, all 24 pass.** The
   tip then stays at least 34 mm from every capped vial's axis (24 mm needed), and a carried cap
   34 mm (28 mm: no overlap in plan).
2. **Stir between runs, not during one.** Opening the Uno's port resets it, and CubOS holds that
   port for the whole run, so a script can't stir while a run is going, and CubOS has no stir step
   yet (a `set_stirrer` step modelled on `set_lights` would add one). For now, before a run, stir
   each stock in turn from the Pi with byu-vcl `BUILD.md`'s stage 8 script:
   `30,<stirrer>,300,60` once stage 5 is done (`30,300,60` for A today).
3. **Stir capped, and stop before the vial is opened.** Stirring an open sulfide stock speeds its
   loss to the air, and a turning bar under the tip is a crash risk. Nothing in a run stirs, so this
   holds by itself while rule 2 does.
4. **The corrosion rules still apply** ([`../build-guide.md` §5](../build-guide.md#5-software-and-the-first-electrical-checks)):
   cap moves with no tip on, the electrode cap on at most one station, the cell off before every
   cap move, no unattended nights yet.

**What stirring buys here, and what it doesn't.** A stock mixed before it goes on the deck doesn't
separate on its own, so stirring it again changes little. Stirring matters when something is
added to a vial on the deck: a spike, or making the 0.1 mg/L sulfide stock from the 10 mg/L one
(ten 20 µL transfers into 19.8 mL of ASW). The P20 can't mix 20 mL; byu-vcl#169's paint test showed
that. It also re-mixes a stock after a long wait, when opening it has let the top evaporate or
lose sulfide.

## 9. The EZstat-Pro

The tray's 3-wire bus ends in a JST-XH plug at its back edge (x 222.5). Run the shielded cable
(B17) from its mate to the EZstat, and connect its leads, which end in stackable banana plugs with
push-on clips (byu-vcl PR #291's [runbook](https://github.com/vertical-cloud-lab/byu-vcl/blob/9280485/potentiostat/ezstat-pro/README.md)):

| Bus wire | EZstat lead |
| --- | --- |
| WE (the four pogo pins under the pieces) | WORKING (black), with WORKING SENSE (black) stacked into its back |
| RE (the four reference pads) | REFERENCE (white), on its own now: no longer stacked with COUNTER as for the dummy loads |
| CE (the four counter pads) | COUNTER (red) |
| Cable shield | GROUND (green), at the EZstat end only |

Tin the cable's far ends or crimp small lugs on them for the clips. Connect with the cell off, in
the runbook's order (ground, reference, counter, working sense, working), and disconnect in
reverse. Then the runbook's [§7 checks C1–C6](https://github.com/vertical-cloud-lab/byu-vcl/blob/9280485/potentiostat/ezstat-pro/README.md#7-corrosion-checks-for-the-alloy-work)
take it from a 10 kΩ resistor to the first CubXL well against the bench cell. The dummy cell (B26)
goes at the tray's end of the bus with the steppers energised. **The EZstat has no EIS,** so the
copper sequence skips step 5 and runs OCP for 30 min. Whether it may be used in salt water is
still a question for Dr. Porter.

## 10. First runs

1. **Water only, no electrochemistry:** all four stirred vials with DI water, a dummy piece in S1.
   One protocol that, for each stirrer in turn, picks up a tip, decaps the vial, draws twice into
   S1 with a stage move before the second draw, stages, recaps, and drops the tip. Watch the tip
   past each capped neighbour, and the deck camera's frames after.
2. **Stir each vial** for 60 s at 300 rpm, then at 600, from the Pi, with the vial capped as the
   run left it. Check by eye that each bar turns with its magnets. In the 2026-11-05 trial the same
   spacer stack fell into bursts after a decap and recap: if that recurs, add one M3 washer under
   that vial, or try the 12 × 3 mm bar (BOM, optional).
3. **Then the cell:** the leak check on each alloy's finish, a dummy cell on the bus, and the
   calibration of [`../copper/protocol.md` §5](../copper/protocol.md#5-calibrate-first) before the
   first real spot.

## What to report back

On #180 for the deck and the corrosion cell, on byu-vcl#269 for the stirrers:

- the taught stirred-vial positions and rims, tip rack 2's A1 and A2, and the slot mapping;
- whether each stirrer started from rest three times in a row on its spacer, and after a decap and
  recap;
- whether any stirrer lifted when its cap came off;
- the cable lengths each stirrer needed;
- anything a tip or a carried cap came close to that the checks didn't predict.
