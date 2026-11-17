# Building and troubleshooting the corrosion setup: the log

Started 2026-11-16 for Ben's request on
[#180](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/180#issuecomment-6929931012):
a PR of its own, [#264](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264), for building the
copper corrosion setup on the CubXL and fixing what goes wrong.
The plan is in [`build-guide.md`](build-guide.md) and the parts are in
[`bom/README.md`](bom/README.md). This file records what actually happens: what arrived, what
printed, what fit, every bench measurement, and each problem with its fix.

**How to add to it.** Add a dated entry under [Log](#log), newest first: what was done, what was
measured (with units), and anything that didn't match the plan. Give a problem its own entry:
what happened, why, the fix, and which file changed. Put photos in `build-photos/` next to this
file, and keep people's faces and any screen showing a login out of them, since this repo is
public. Or comment on the PR with `@claude`, the result and a photo, and ask for it to be logged.

## Where things stand on 2026-11-17

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
| B41 | Trace-metal nitric acid, 500 mL | **From BYU Chem Stores**, $119.66 (Ben, 2026-11-16), against $193 shipped as hazmat |
| B39 | Sodium sulfide nonahydrate | **Sigma's 100 g, $78.10.** Chem Stores' 500 g is $102.82, and 100 g is plenty. Not needed until the sulfide nights: the first experiment is in plain seawater |
| B36 | 0.5 mL Safe-Lock tubes | **Fisher's 500, Eppendorf Quality, colorless (05-402-18), $147.84** (Ben, 2026-11-16). The PCR clean ($193) and Forensic DNA Grade ($188) bags certify DNA, not metals (log, below). Chem Stores' 100 ($43.86) last about 11 nights at 9 a night, and the R1–R3 calibration alone takes about 12. If a tube isn't Eppendorf's, try it in the tube fit strip |
| B38 | Substitute ocean water | Not quoted by Chem Stores yet; $135 for 4 L from Government Scientific Source |
| B30 | 1 µm diamond suspension ($35), PACE | Copper's 1 µm step, on the lab's Mark V cloths. **Still needed** (log, 2026-11-17): the lab's 1 µm alumina leaves Al, and its 0.1 µm diamond is too fine to follow the SiC papers. The lab's 0.1 µm diamond is copper's last step now, so the colloidal silica (B32, $29) and the 0.1 µm film (B29, $265) are no longer needed |
| B34 | Filament | Check stock: the H2D plate takes 362 g of PLA |

**On hand, so not ordered** (Ben, [2026-11-16](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6930927185)
and 2026-11-17: [the cloths](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6962338430)
and [the liquids](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6963040371)):

| BOM | Item | Where from |
| --- | --- | --- |
| B09 | Steel discs, 1 in | The capper's. The electrode cap's Ø25.4 × 0.5 mm recess is the one in PANDA-BEAR's `VialCap16mm.step`, so they fit. Measure the thickness (below) |
| B13, B18 | M3 heat-set inserts, JST-XH pairs | ME order 13518 (the stirrer order): the same ruthex M3 × 5.7 insert, for the same Ø4.0 mm holes |
| B47, B48 | #46 drill (2.06 mm), end mill for facing | BYU's Prototyping lab |
| B31, B33 | Polishing pads for the 1 µm diamond and the final polish | The lab's Mark V MCR12 micro rayon cloths, 12 in PSA, 10 a pack. Copper takes 6, one per alloy and abrasive (below) |
| H12, in place of B32 | 0.1 µm diamond suspension | The polishing lab. Copper's last step, on a second cloth. The lab's 1 µm alumina is the SOP's, for aluminium only |

### Printing

| What | File | Status |
| --- | --- | --- |
| Every part the lab doesn't have, 38 pieces, 12.3 h, 362 g PLA, left nozzle, pauses at 4.2 h (14 magnets) and 10.4 h (6 magnets) | [`bom/h2d/h2d-corrosion-all.gcode.3mf`](bom/h2d/h2d-corrosion-all.gcode.3mf) | not printed |
| Tip rack 2, if the deck's second rack isn't a copy of rack 1 | [`bom/cad/tip_rack_1_20ul.step`](bom/cad/tip_rack_1_20ul.step) | not needed yet |

The H2D plate was re-sliced for the left nozzle on 2026-11-17 (log, below). A single-filament
print goes on the left nozzle by default, and every nozzle a print uses must be 0.2 or 0.4 mm.
A `@claude-print` run reads the installed nozzles first. The file is sliced for a 0.4 mm
standard nozzle.

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
| A steel disc (B09, the capper's) in the cap's Ø25.4 × 0.5 recess; its thickness | drops in, as on a vial cap; 1.0 mm assumed (a 0.5 mm disc still lifts the cap, with a margin of 2.3) | |
| Facing the counterbore ceiling with the end mill (B48), only if it's rough | 0.05 mm off at most | |

### Polishing the first piece of each alloy ([`copper/protocol.md` §1](copper/protocol.md#1-specimen))

| Check | Expect | Measured |
| --- | --- | --- |
| The lab's 0.1 µm diamond | a suspension, not the SOP's 0.1 µm film; enough for a few mL a piece | |
| Unused Mark V MCR12 cloths in the pack | 6 for copper: C71500, C95800 and C70600, one for the 1 µm and one for the 0.1 µm diamond | |
| 1 µm diamond (B30) on a cloth, after the SiC papers | SiC scratches gone in about 2 min (PACE's copper procedure) | |
| Ultrasonic clean, then the 0.1 µm diamond on a second cloth, in 1 min runs | 1 µm scratches gone in a few minutes (SOP Step 7); on NAB, no pulled-out κ | |

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
| Two tube blanks on the first night: B36 tubes straight from the bag, not acid-leached, each with 300 µL of DI water and step 12's 20 µL of 1 M acid, open in the rack all night | Cu, Ni, Fe and Mn below the ICP-MS limit (Eppendorf's values give under 0.05 ng of Cu a tube). If so, skip the pre-leach in [`copper/protocol.md` §6](copper/protocol.md#6-icp-ms-the-sample-and-its-blanks) | |

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

### 2026-11-17: the polishing liquids on hand (1 µm alumina, 0.1 µm diamond)

From [Ben's question](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6963040371)
([the reply](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6963046774)):
the lab has 1 µm alumina and 0.1 µm diamond. Are B30 and B32 still needed? **B30 is, B32 isn't.**
- **B30, the 1 µm diamond ($35): still to buy.** Neither liquid can do its step.
  - The alumina is the SOP's Step 5 abrasive, for aluminium. On copper its residue is Al, which
    EDS and the NAB tubes measure, and no blank catches grains pressed into the face. NIST's
    microprobe lab avoids alumina for the same reason
    ([Geller and Engle 2002](https://doi.org/10.6028/jres.107.051)).
  - The 0.1 µm diamond is too fine to follow the SiC papers. The SOP already warns that even
    1 µm to 0.1 µm may be too big a step.
- **B32, the colloidal silica ($29): optional now.** Copper's polish ends on the lab's 0.1 µm
  diamond instead, on a second Mark V cloth.
  - That is the size NIST asks for on copper ("requiring 0.1 µm to finish"), and the SOP's own
    last step for aluminium, so one finish serves EDS on both.
  - c1-05's baseline ended on colloidal silica, but c1-05 found no study that compared finishes on
    these alloys. Silica also takes off the last smeared layer chemically. Diamond leaves it
    thinner but doesn't remove it. That is for the finish arms to test (protocol §5), with B32 if
    a silica arm is wanted.
- **If the 0.1 µm diamond is the SOP's film,** not a liquid, it still works. Give each copper alloy
  an unused film, and run it as SOP Step 7 does. Aluminium's films stay with aluminium.
- **Totals** (from the scripts: Python ran this time). Still to get: $1,103.10 plus the C95800
  quote, down from $1,132.10. The stirrer order list is $1,796.71, down from $1,825.71. In the
  BOM, "copper adds" is $838 (was $867) and "copper, optional" $813 (was $784).
- **The scripts confirm the hand edits.** Before this change, `bom_totals.py` reproduced
  `totals.json` exactly, and `order_list.py` reproduced `order-list.csv` apart from the line
  endings of two rows.
- **Files:** `copper/protocol.md` §1 and §5, `copper/test-matrix.csv` (F1), `bom/bom.csv` (B29–B33,
  H07, and a new H12), `bom/README.md`, `bom/totals.json`, `stirrers/order_list.py`,
  `order-list.csv`, `order-totals.json` and `stirrers/BOM.md`.

### 2026-11-17: the H2D print file, re-sliced for the left nozzle

From [Ben's request](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6962590447)
to bring the H2D print file over to this PR.
- **The files were already on this branch.** This PR is stacked on #180, so it has every file #180
  has. GitHub's *Files changed* tab lists only what this PR changes. Re-slicing puts the plate's
  files in this PR's diff.
- **What changed:** the print now goes on the left nozzle, the default for a single-filament print.
  The project's plate is set to the left nozzle as well. Under Bambu Studio's "Auto For Flush"
  setting, it went back to the right nozzle whenever the project was sliced again.
- **What didn't:**
  - the parts, the layout and the settings;
  - 12.3 h and 362.49 g (119.6 m);
  - the pauses: before z 5.8, 4.2 h in, and before z 44.8, 10.4 h in with 1.9 h left.
- **Checks:** Python was blocked, so an awk script made them. On the 9 November file it gives the same
  numbers as `make_h2d_plate.py`. On the new file:
  - every extrusion is inside x 49.2–313.7 and y 20.2–295.6 mm, within the left nozzle's reach
    (x 0–325);
  - the 20 magnet pockets are 2.26 mm from the nearest plastic before their pause, and 0.17–0.19 mm
    after it;
  - the 7 key pockets are open at mid-depth and roofed above, as before.
- **Still no preview picture in the sliced file.** The slicer renders it with OpenGL, and that
  failed both under a virtual X display and under a headless Wayland compositor.
- **Files:** in `bom/h2d/`, `h2d-corrosion-all.gcode.3mf`, `h2d-corrosion-all.3mf`, `plate.json`,
  `make_h2d_plate.py` (`PRINT_WITH = 1`, and the plate's own setting) and the README.

### 2026-11-17: the polishing cloths on hand (Mark V MCR12)

From [Ben's question](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6962338430)
([the reply](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6962345645)):
the lab has Mark V MCR12 cloths (micro rayon, white, 12 in PSA, 10 a pack). Are they enough for
the copper tests? **Yes, as the cloths. Copper still needs two liquids for them.**
- **What they are.** Mark V calls them a ["final polish white color low nap cloth used with
  Diamond or Alumina for soft materials"](https://markvlab.com/polishing-cloths/product/1143-micro-rayon-white-cloth-12-psa-10-pkg).
  They do the job of both PACE pads in the BOM: ATLANTIS (B31), a low-nap pad for 1 µm diamond,
  and NAPPAD (B33), a high-nap final pad.
- **What goes on them: 1 µm diamond (B30, $35), then colloidal silica (B32, $29).** That is the
  protocol's baseline (§1, from Edison's c1-05). So the 0.1 µm film (B29, $265) is now optional.
- **No alumina on copper.** That rules out both the SOP's 1 µm alumina and the 0.05 µm alumina
  that ends [PACE's copper procedure](https://metallographic.com/guides/copper-and-copper-alloys-preparation).
  - Its residue is Al, which EDS and the NAB tubes measure, and the cathodic series is read from
    where Al release stops.
  - Grains pressed into the face reach no blank: S4's fixture blank is PTFE.
  - Diamond leaves carbon and silica leaves Si, and copper's measurements include neither.
  - Cu–Ni gets the same polish, because the finish and the alloy never change together.
- **Six cloths:** one per alloy and abrasive, as the SOP does with its pads. Count the unused ones.
  Cloths already used on aluminium stay with aluminium. Another 10 are $94 from Mark V.
- **Ask the polishing lab first** whether it has 1 µm diamond or colloidal silica. The SOP's EBSD
  polish uses colloidal silica on the vibratory polisher.
- **Totals.** Still to get: $1,132.10 plus the C95800 quote, down from $1,333.10. The stirrer order
  list is $1,825.71, down from $2,026.71. In the BOM, "copper adds" is $867 (was $1,068) and
  "copper, optional" $784 (was $788).
- **Files:** `copper/protocol.md` §1, `bom/bom.csv`, `bom/README.md`, `bom/totals.json`,
  `stirrers/BOM.md`, `stirrers/order_list.py`, `order-list.csv` and `order-totals.json`. Python
  still couldn't run, so the outputs were edited by hand and the sums checked with awk.

### 2026-11-16: which grade of tube (B36)

From [Ben's question](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6931531023)
([the reply](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6931538613)):
Fisher's 500-packs of the 0.5 mL Safe-Lock tube are $147.84 in Eppendorf Quality, $188 in Forensic
DNA Grade and $193 in PCR clean. **Buy Eppendorf Quality, colorless (05-402-18).**
- **The dearer grades don't help ICP-MS.** In
  [Eppendorf's purity-grade guide](https://usascientific.com/cms/files/Epp_Purity.pdf), PCR clean and
  Forensic DNA Grade lots are certified free of human DNA, DNase, RNase and PCR inhibitors. No grade
  is tested for metals.
- **Eppendorf's metal numbers.** Its
  [certificate 0012602500-04](https://cdn.shopify.com/s/files/1/2245/7875/files/Eppendorf_Consumables_Certificate-Quality-Conformity-Eppendorf-Tubes-Trace-metal.pdf)
  (2020, a distributor's copy) gives typical values, not lot by lot. Safe-Lock tubes were filled with
  concentrated nitric acid for 1 h. For the 0.5 mL tube: Cu below 0.1 µg/L; Ni, Mn, Cr and Pb below
  0.05 µg/L; Zn below 1 µg/L; Al 3 µg/L. A full tube would then hold under 0.05 ng of Cu.
  - The ICP-MS needs about 0.42 ng of Cu in one of our tubes to see it: 0.13 µg/L in 3.2 mL after the
    10× dilution.
  - A fresh spot puts 290–580 ng of Cu in its tube ([`copper/protocol.md` §6](copper/protocol.md#6-icp-ms-the-sample-and-its-blanks)).
  - Al is the one metal it found, up to 1.5 ng a tube. That matters only for Al on NAB, and the
    fixture blank measures it.
- **Colorless, not colored.** Blue and green plastics are usually tinted with copper phthalocyanine.
- **The price.** $147.84, not the $108.90 the BOM had from a 2026-10-19 search snippet (Fisher's
  site blocks the runner). Still the 500: $0.30 a tube, against $0.44 for Chem Stores' 100.
- **The pre-leach** in protocol §6 may not be needed. Run the two tube blanks (Measurements, on the
  deck) and decide from them. The protocol now says so.
- **Totals.** Still to get: $1,333.10 plus the C95800 quote, up from $1,294.16. The stirrer order
  list is $2,026.71, up from $1,987.77. In the BOM, the aluminium shakedown is $371 and option 1
  running $1,606. "Copper adds" stays $1,068, since B36 counts under both alloys.
- **Files:** `bom/bom.csv`, `bom/README.md`, `bom/totals.json`, `stirrers/BOM.md`,
  `stirrers/order_list.py`, `order-list.csv` and `order-totals.json`, and `copper/protocol.md` §6.
  Python still couldn't run, so the outputs were edited by hand and the sums checked with awk.

### 2026-11-16: what the lab has, and Chem Stores' prices

From [Ben's comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/264#issuecomment-6930927185).
**No print file changes.**
- **On hand:**
  - **B09:** the capper's steel discs. PANDA-BEAR's `VialCap16mm.step` has a Ø25.4 × 0.5 mm recess on top,
    and the electrode cap's recess copies it, so a disc that fits a vial cap fits the electrode
    cap. *Correction:* the entry below said the capper's discs were cut smaller, for the vial caps.
    They aren't. The cap's pull numbers assume a 1.0 mm disc, so measure one. At 0.5 mm the
    electromagnet still pulls about 5.7 N, 2.3 times the 2.44 N the cap needs out to a 0.18 mm gap
    (`cad_check.py`'s model).
  - **B13 and B18:** the inserts and JST pairs from ME order 13518.
  - **B47 and B48:** the #46 drill and an end mill, at BYU's Prototyping lab. Use a 7 mm or 1/4 in
    end mill, and take 0.05 mm at most off the counterbore's ceiling. Each 0.1 mm cuts the
    O-ring's squeeze from 21 % to about 16 %.
- **Chem Stores' prices:**
  - **B41:** the nitric acid comes from Chem Stores, at $119.66 against $193.
  - **B39:** Sigma's 100 g ($78.10) rather than Chem Stores' 500 g ($102.82), unless shipping
    closes the gap.
  - **B36:** the 500 ($108.90) rather than Chem Stores' 100 ($43.86). A night takes about 9 tubes,
    so the R1–R3 calibration alone uses about 108.
- **Totals:** the stirrer order list comes to $1,987.77, down from $2,072.79. The BOM's "copper
  adds" is now $1,068 and the aluminium shakedown $332.
- **Files:** `bom/bom.csv`, `bom/README.md`, `bom/bom_totals.py` → `totals.json`,
  `stirrers/BOM.md`, `stirrers/order_list.py` → `order-list.csv` and `order-totals.json`, and
  `build-guide.md`. Python couldn't run in that session, so the two JSON files and the order list
  were edited by hand and the sums checked with awk. Rerun both scripts to confirm.

### 2026-11-16: the build PR opened

Opened from #180's branch, with the status above. Two changes to the BOM came with it:
- B01–B04: the Filters4You substitute is marked not used, after the $157 quote (Ben, 2026-11-13).
- B06: the CSV's note and the README's table row still said to open the cap's pin holes to
  1.3 mm, which the 2026-11-09 datasheet check had corrected. Both now give the counterbore.
