# The corrosion setup, built from scratch: an animation

Made 2026-11-09 for Sterling's request on [#180](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/180):
take Ben's order list (`Items to Order.txt`, 18 lines) as the BOM, add what the lab already has,
and animate the build from the parts up: lay the parts out one at a time, then put them together,
including the printed parts, the O-rings, the pogo pins and the sulfide kit. Every bought part is
drawn at the size its vendor publishes, so a part that won't fit shows up here before it arrives.
**Nothing in it has been built or tested.**

**[`build-from-scratch.mp4`](build-from-scratch.mp4)** (1280 × 720, 30 fps, 3 min 59 s).
[`build-cap.gif`](build-cap.gif) is the electrode cap chapter alone, and
[`build-sheet.png`](build-sheet.png) has one frame from each chapter.

| Chapter | Starts | What it shows |
| --- | --- | --- |
| — | 0:00 | Title card |
| 1 what was ordered: stock, electrodes, wire, the sulfide kit | 0:06 | Ten lines of Ben's order list, one at a time: drill rod, PTFE and brass rod, graphite rods, the Ossila reference, Belden cable, both wires, the foil tape, the CHEMets kit |
| 1 what was ordered: small parts | 0:23 | The four O-ring sizes, CPG-37 and P75-B1 pins, magnets, M3 screws, Pt wire, the dummy cell's resistor and capacitor, the leak-free reference (being quoted); inserts, JST pair and steel discs from the lab |
| 2 not on the order yet | 0:44 | Seawater, sodium sulfide, trace-metal nitric acid, 0.5 mL tubes, lapping film, the Cu–Ni and NAB bars |
| 3 printing everything on the H2D | 0:56 | The plate rising layer by layer, with the print clock; 14 magnets at pause 1, 6 at pause 2 |
| 4 cutting the stock | 1:13 | Steel slugs, brass pins, the PTFE blank; a slice of 1 in bar that doesn't fit the pocket, then flatted |
| 5 a well lid | 1:28 | The O-ring's fit in the counterbore, brass pins, copper-foil pads, the sealed-in magnets |
| 6 the electrode cap | 1:44 | #46 drill, steel slugs, CPG-37 pins, the Pt coil wound on its carrier, the reference, the wire-wrap leads, the steel disc |
| 7 the coupon tray, coupons and lids | 2:10 | Heat-set inserts; twelve P75-B1 pins from below; the bus wires, JST plug and Belden cable; coupons and shims; O-rings, lids and screws; the pins at work |
| 8 the bench cell (calibration against a 1 cm² window) | 2:38 | Clamp plate and WE pin, coupon, AS568-013, body and four screws, seawater, cover, graphite counter on a collar, Ossila reference |
| 9 checking a sulfide stock: CHEMets K-9510 | 2:54 | 25 mL in the cup, 3 drops of activator, the ampoule snapped, mixed, 5 min, read on the comparator |
| 10 on the CubXL | 3:14 | Each module placed on the stirrer deck; the capper carries the cap from the park cup to S1; the current path lit |
| 11 what the model caught | 3:45 | The findings, listed below |

Colours on each part's card: **blue**, on Ben's order; **amber**, not ordered yet or being quoted;
**green**, printed on the H2D; **grey**, already in the lab.

## What drawing the parts at their real size caught

The sizes, with a link and a quote for each, are in [`parts-check.md`](parts-check.md).

1. **The cap's CPG-37 pins need a different hole.** The BOM says to open the cap's pin holes to
   1.3 mm and recess the flange 0.2 mm. The [datasheet](https://www.sameskydevices.com/product/resource/cpg-37-th-tr.pdf)
   pin has a Ø2.00 flange and a Ø1.50 × 1.10 tail, and stands only 2.20 mm free with 0.9 mm of
   stroke. Mounted as the BOM says, it would bottom out and hold the cap about 1 mm off the lid.
   For mid-stroke (1.50 mm, 30 gf) on the 0.07 mm foil pads, cut a **Ø2.1 counterbore 1.57 mm deep**,
   then **Ø1.6 × 1.1 mm** for the tail, and keep the 1.0 mm hole above it for the wire. Solder
   the wire-wrap to the tail before pressing the pin in. The datasheet also lists a black plastic
   housing, (Ø2.30) × 4.10; check on arrival whether it comes off.
2. **The P75-B1 pins are 16 mm long, not the CAD's 11 mm.** In the tray, each WE pin's tail ends
   1.0 mm below the tray's underside, so the tray would stand on four pin tails: print it with
   2 mm feet. In the bench cell the pin hangs 13 mm below the 8 mm clamp plate: stand the cell on
   15 mm feet.
3. **A slice of a 1 in bar doesn't fit the 20.6 mm pockets.** C71500, C70600 and C95800 are
   bought as 1 in round. Mill four flats 20 mm across, or turn the slice to Ø20, before polishing.
4. **The sulfide test takes a 25 mL sample, and a deck stock is one 20 mL vial.** Test the bottle
   each vial is filled from, at the start and end of each sulfide night. The kit doesn't see copper
   or silver sulfides; thiosulfate, sulfite and oxidants interfere.
5. **Graphite: yes in the bench cell, no in the cap.** Edison's answer is summarised below. In
   the bench cell, nothing in the cover sets the 10 mm rod's depth, so it would slide down beside
   the window. Hang it on a collar.
6. **Smaller fits to try on the first print.**
   - The AS568-006 is loose in its counterbore (OD 6.46 in Ø7.30) and falls out when the lid is
     turned over. Set it on the coupon, centred, and lower the lid over it. The ordered rings are
     brown, not black.
   - The magnets are 4.00 × 2.00 ±0.10 mm for Ø4.1 × 2.1 pockets. Try one before the 11 h plate.
   - The brass rod is 1.588 mm for 1.6 mm holes.
   - The Pt wire is hard temper (and 99.95 %, not the list's 99.90 %). Anneal it before winding.
   - The steel disc is a full 1.00 in for a Ø25.4 recess.

## The graphite question

[Edison c2-01](../copper-ded-edison/batch2/c2-01-graphite-counter-in-well.md) says to keep the Pt
coil in the cap. McMaster's graphite rods ([9121K](https://www.mcmaster.com/products/graphite-rods/),
1/16 to 1/8 in) state no purity. Graphite carries Fe, Ni and Cu, which are on the ICP-MS list. It is
porous, so it carries copper from well to well. It sheds when it is the anode in chloride. The Pt-free
option to try is a 3 mm glassy-carbon rod, which would need a redesigned cap. The hobby rod is fine
in the 250 mL bench cell after an acid leach and a blank. The full summary is in
[`../copper-ded-edison/README.md`](../copper-ded-edison/README.md#batch-2-graphite-or-platinum-for-the-counter).

## What is drawn exactly, and what isn't

- **From this PR's CAD, as is:**
  - the well lid v2, electrode cap, carrier, coupon tray, cup block, tube rack, tip waste cup,
    shims and the three bench-cell parts (STL files in [`../copper/cad/`](../copper/cad/) and
    [`../bom/cad/`](../bom/cad/));
  - the H2D plate's layout ([`../bom/h2d/`](../bom/h2d/README.md));
  - the deck positions of the stirrer layout ([`../stirrers/deck_stir.py`](../stirrers/deck_stir.py)).
- **From vendor data:** every bought part in `parts_lib.py`. The exceptions follow.
- **Sizes nobody publishes, drawn as typical:**
  - the CHEMets ampoule, cup and comparators;
  - the P75-B1 barrel length (its overall length is published);
  - the wire-wrap insulation and its spool;
  - the 3M tape's core;
  - the Ossila cap and pin diameters;
  - the EZstat-Pro's box.
- **Schematic:**
  - the CubXL frame, gantry and head, reused from [`../copper/render_cubxl_cu.py`](../copper/render_cubxl_cu.py);
  - the stir modules, at their published 49 × 44 mm envelope;
  - the tip racks, drawn as blocks.
- **Drawn the way the CAD has it, not the fix:**
  - the cap's pin holes;
  - the tray without feet;
  - square 20 × 20 coupons in the tray chapter (chapter 4 shows the flatted slice);
  - the pad pins ending inside the tray.
- **Not shown:**
  - polishing;
  - the leak test;
  - filling and running a spot, which is in [`../copper/cubxl-cu-spot.mp4`](../copper/cubxl-cu-spot.mp4).
- **The cap's index mark:** the capper sets the cap down at 0°. 180° also seats and swaps RE and CE.

## Files

| File | What it is |
| --- | --- |
| [`render_build.py`](render_build.py) | The animation: one class per chapter, keyframed poses, cards and labels |
| [`parts_lib.py`](parts_lib.py) | Meshes of the bought parts; `DIMS` holds every size and where it came from |
| [`parts-check.md`](parts-check.md) | Each bought part against what it has to fit, with links |
| `build-from-scratch.mp4`, `build-cap.gif`, `build-sheet.png` | The outputs |

## To run

As run on the GitHub Actions runner (Ubuntu 24.04, Python 3.12, PyVista 0.49, VTK 9.6, gmsh 4.15), from
this folder. The capper's three STEP files stayed in byu-vcl; fetch them pinned, as in
[`../copper/keyframes/README.md`](../copper/keyframes/README.md#commands).

```bash
pip install pyvista gmsh matplotlib imageio imageio-ffmpeg numpy pillow trimesh shapely
mkdir -p /tmp/byu-vcl-capper-cad
for f in 9VialHolder20mL_TightFit PAW-V2-ElectromagnetMount VialCap16mm; do
  curl -sfL -o /tmp/byu-vcl-capper-cad/$f.step \
    https://raw.githubusercontent.com/vertical-cloud-lab/byu-vcl/c129db521599fa86569174ff9fcf4aa205a9cf55/modules/electromagnetic-capper/cad/$f.step
done
# four parallel parts, about 9 min on 4 cores, then join them and make the GIF, the sheet and chapters.json
for i in 0 1 2 3; do
  xvfb-run -a -s "-screen 0 1400x900x24" python render_build.py --capper-cad /tmp/byu-vcl-capper-cad --part $i/4 &
done; wait
python render_build.py --assemble 13
# one still per chapter, or chosen moments of one chapter
xvfb-run -a python render_build.py --capper-cad /tmp/byu-vcl-capper-cad --stills
xvfb-run -a python render_build.py --capper-cad /tmp/byu-vcl-capper-cad --only Cap --at 5,12,20
```
