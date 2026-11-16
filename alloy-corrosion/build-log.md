# Building and troubleshooting the corrosion setup: the log

Started 2026-11-16 for Ben's request on
[#180](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/180#issuecomment-6929931012):
a PR of its own for building the copper corrosion setup on the CubXL and fixing what goes wrong.
The plan is in [`build-guide.md`](build-guide.md) and the parts are in
[`bom/README.md`](bom/README.md). This file records what actually happens: what arrived, what
printed, what fit, every bench measurement, and each problem with its fix.

**How to add to it.** Add a dated entry under [Log](#log), newest first: what was done, what was
measured (with units), and anything that didn't match the plan. Give a problem its own entry:
what happened, why, the fix, and which file changed. Put photos in `build-photos/` next to this
file, and keep people's faces and any screen showing a login out of them, since this repo is
public. Or comment on the PR with `@claude`, the result and a photo, and ask for it to be logged.

## Where things stand on 2026-11-16

**Nothing has been printed, assembled or tested yet.** Parts are on order.

### Orders

Ben's order list (`Items to Order.txt`, posted on
[#180](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/180#issuecomment-6753391753))
has 21 lines. Ben, please correct this table if the ME orders differ from the list.

| Order | What | Status |
| --- | --- | --- |
| ME order 13669 (2026-11-09) | "Most of the parts": the list's B01–B04 (O-rings, 100 of each), B06, B07, B10, B11, B12, B14, B15, B16, B17, B20, B21, B22, B26, B40 and B46 | ordered; arrivals not logged |
| ME order 13688 (2026-11-11) | The magnets alone: B08, 4 × 2 mm N52, 250 | approved by Sterling on 2026-11-11; arrival not logged |

**O-rings:** B01–B04 stay with The O-Ring Store's 100-packs. Filters4You's quote for its 10-packs
came to $157 on 2026-11-13, not the $23.96 its pages list.

### Not ordered yet

| BOM | Item | What's needed |
| --- | --- | --- |
| B19 | Leak-free Ag/AgCl reference | The vendor's quote. Ben expects it under $300. Pick the straight 15.5 mm barrel with a bare silver wire (what the BOM and build guide describe), or the custom bent LF-2-Bent90, which needs [`electrode_cap_bent90.stl`](copper/cad/electrode_cap_bent90.stl) instead of the electrode cap on the H2D plate ([`copper/cad/README.md`](copper/cad/README.md)) |
| B45 | C95800 bar | A quote, with the mill cert |
| B43, B44 | C71500 and C70600 bars | Ben's question: does the lab already have Cu–Ni stock? |
| B38, B39, B41 | Substitute ocean water, sodium sulfide, trace-metal nitric acid | Ben's question: can Chem Stores supply smaller amounts? B39 and B40 aren't needed until the sulfide nights; the first experiment is in plain seawater |
| B36 | 0.5 mL Safe-Lock tubes | Ben's question: from Chem Stores? Try a tube in the tube fit strip if it's another brand |
| B29 | 0.1 µm diamond lapping film ($265) | Ben's question: does the Prototyping lab have some? |
| B47 | #46 drill (2.06 mm) | **Not on the list.** It opens the cap's reference bore to 2.05 mm. Find one in the shop, or order it ($1.99) |
| B09 | Steel discs, 1 in × 1 mm, adhesive | **Not on the list.** The build video counts them as on hand, but the capper's discs are cut to the 16 mm vial caps. The electrode cap's recess takes a full 1 in disc: check, or order B09 ($27.79) |
| B13, B18 | M3 heat-set inserts, JST-XH pairs | On hand from ME order 13518 (the stirrer order) |
| B34 | Filament | Check stock: the H2D plate takes 362 g of PLA |

### Printing

| What | File | Status |
| --- | --- | --- |
| Every part the lab doesn't have, 38 pieces, 12.3 h, 362 g PLA, pauses at 4.2 h (14 magnets) and 10.4 h (6 magnets) | [`bom/h2d/h2d-corrosion-all.gcode.3mf`](bom/h2d/h2d-corrosion-all.gcode.3mf) | not printed |
| Tip rack 2, if the deck's second rack isn't a copy of rack 1 | [`bom/cad/tip_rack_1_20ul.step`](bom/cad/tip_rack_1_20ul.step) | not needed yet |

The H2D plate was sliced for the right nozzle on 2026-11-09. Since then `CLAUDE.md` says a
single-filament print goes on the left nozzle by default, and every nozzle a print uses must be
0.2 or 0.4 mm. A `@claude-print` run reads the installed nozzles first. Slicing for the left
nozzle was checked on 2026-11-09 (12.3 h, both pauses in place): set the filament to the left
nozzle in the project, or `PRINT_WITH = 1` in [`make_h2d_plate.py`](bom/h2d/make_h2d_plate.py).

## Measurements to make

Fill in the **Measured** column and log the entry. Each one replaces an estimate in the design.

### Before the 12 h print

| Check | Expect | Measured |
| --- | --- | --- |
| A magnet (B08) in a Ø4.1 × 2.1 mm pocket | 4.00 × 2.00 ± 0.10 mm, slides in | |
| Deck key (P19) fit in a part's pocket, in PLA on the H2D | 0.05 mm press (one dimple); try 0.10 and 0.15 mm if loose | |

### After the print ([`build-guide.md` §1](build-guide.md#1-print))

| Check | Expect | Measured |
| --- | --- | --- |
| Electrode cap over the lid's 16 mm boss | slides by hand with slight play (0.12 mm clearance) | |
| Carrier into the cap | presses in and stays | |
| Tube fit strip | the 8.2 mm hole holds a real 0.5 mL tube by its rim | |
| O-ring in the lid's counterbore | loose (OD 6.46 mm in Ø7.30): set it on the coupon first | |
| Brass rod (B12) in the lid's pin holes | 1.588 mm in 1.6 mm holes | |
| -006 O-ring cross-section, three rings | 1.70–1.85 mm | |

### Bench tests ([`build-guide.md` §3](build-guide.md#3-bench-tests-before-the-cap-goes-on-the-deck))

| # | Test | Estimate | Measured |
| --- | --- | --- | --- |
| 1 | Force to lift the cap off a lid; electromagnet pull on the real disc at 0–0.4 mm | 2.4 N; 22.8 N at contact | |
| 2 | Water lost from a filled, capped well over 2 h | 1.6 µL/h | |
| 3 | Spring force of the cap's pins at 0.93 mm stroke; contact resistance on the foil pads | 30 gf each | |
| 4 | Wetted area under the squeezed O-ring on a polished coupon | 0.101–0.126 cm² | |
| 5 | Face-seal leak check on each alloy's finish | no leak | |
| 6 | Whether the capper's IR beam sees the electrode cap; the decap height that touches the disc | to be found | |

### On the deck ([`build-guide.md` §4–5](build-guide.md#4-on-the-deck))

| Check | Expect | Measured |
| --- | --- | --- |
| Slot grid from two jogged slot centres | X = 12.45 + 25n, Y = 43.13 + 45m ([`bom/tip-rack-1.md`](bom/tip-rack-1.md)) | |
| Decap height on the electrode cap's disc | within ±0.15 mm of the top of the disc (z 44 planned) | |
| Upward pull on the tray and cup block when the cap lifts | 1.0–1.7 N; tape them down | |
| Dummy cell (10 kΩ, 1 µF) at the end of the bus, steppers energised | noise low enough to trust nanoamps | |
| EZstat-Pro checks C1–C6 | [byu-vcl PR #291 runbook §7](https://github.com/vertical-cloud-lab/byu-vcl/blob/9280485/potentiostat/ezstat-pro/README.md#7-corrosion-checks-for-the-alloy-work) | |

## Problems found before building

Found by drawing every part at its vendor's size, or by later checks. Each is already fixed in
the files named; check it on the real part.

| # | Problem | Fix | Where |
| --- | --- | --- | --- |
| 1 | The O-ring in the first well lid seals on a 0.2 mm printed ledge: about 200 MPa, four times PETG's yield | Print the v2 lid (0.6 mm ceiling, about 24 MPa) | [`bom/README.md`](bom/README.md#read-this-before-printing) |
| 2 | The cap's CPG-37 pins (B06) would bottom out in a 1.3 mm hole and hold the cap 1 mm off the lid | From below: Ø2.1 counterbore 1.57 mm deep, then Ø1.6 × 1.1 mm for the tail | [`build-guide.md` §2](build-guide.md#the-electrode-cap-p01-and-p02); B06's CSV note fixed on this PR |
| 3 | The P75-B1 pins (B07) are 16 mm long, not 11 mm | Tray 2 mm taller, coupon face at z 22; the bench cell stands on 15 mm feet | [`bom/deck-keys.md`](bom/deck-keys.md) |
| 4 | A slice of 1 in bar doesn't fit the 20.6 mm pocket | Mill four flats 20 mm across, or turn it to Ø20 | [`build-animation/parts-check.md`](build-animation/parts-check.md) |
| 5 | The sulfide kit needs 25 mL; a deck stock is 20 mL | Test the bottle each vial is filled from | same |
| 6 | Nothing sets the bench cell's graphite rod depth | Hang it on a collar | same |
| 7 | Keys locate a part but don't hold it; the cap's magnets pull the tray and cup block up 1.0–1.7 N | Thin double-sided tape under those two | [`bom/deck-keys.md`](bom/deck-keys.md) |
| 8 | The slot grid is 1.87 mm in front of the first estimate | Keyed parts land 1.87 mm forward of their planned y; teach every position | [`bom/tip-rack-1.md`](bom/tip-rack-1.md) |
| 9 | The cap seats at 0° or 180°, and 180° swaps the reference and counter pads | Mark an index; the OCP check at cap-on catches a backwards cap | [`build-guide.md` §2](build-guide.md#the-electrode-cap-p01-and-p02) |
| 10 | A tube lid standing at 90° reaches z 50, above the capper's path | Open every tube lid fully, over the rack's edge | [`build-guide.md` §4](build-guide.md#4-on-the-deck) |
| 11 | The Pt wire is hard temper | Anneal it before winding the coil | [`build-animation/parts-check.md`](build-animation/parts-check.md) |
| 12 | Dissolved copper may plate onto the counter during the anodic hold, so ICP-MS would read low | Compare on the bench; nobody has measured it | [Edison c2-01](copper-ded-edison/batch2/c2-01-graphite-counter-in-well.md) |

Still open in the design: one well per lid (no offset lid drawn), and the copper well simulation
not rerun for the v2 lid's neck.

## Log

### 2026-11-16: the build PR opened

Opened from #180's branch, with the status above. Two changes to the BOM came with it:
- B01–B04: the Filters4You substitute is marked not used, after the $157 quote (Ben, 2026-11-13).
- B06: the CSV's note and the README's table row still said to open the cap's pin holes to
  1.3 mm, which the 2026-11-09 datasheet check had corrected. Both now give the counterbore.
