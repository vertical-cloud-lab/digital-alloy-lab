# Real fasteners in the model, and how they were checked against McMaster-Carr's CAD

Written 2026-11-19 for [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), in answer to
"no illustrative parts. Get real parts (e.g., from mcmaster CAD, and you could recreate your own version and double check
that the volume matches exactly against the mcmaster CAD if you're avoiding committing the file here)". The other half of that
request, how the hot-swappable parts should be held, is in [`hot-swap.md`](hot-swap.md).

Nothing here has been built. Prices are McMaster-Carr list prices read on McMaster's own pages through the lab Pi on 2026-11-19.

| File | What it is |
|---|---|
| [`cad/fasteners.py`](cad/fasteners.py) | every McMaster screw, insert, pin, retainer and disc spring the model uses, recreated in CadQuery from McMaster's listed dimensions and from measurements of McMaster's own model |
| [`cad/verify_fasteners.py`](cad/verify_fasteners.py) | loads McMaster's STEP files from `/tmp/mcm_cad` and compares volume and bounding box with our copies → [`cad/out/fastener-check.md`](cad/out/fastener-check.md) |
| [`cad/fastener-cad-manifest.csv`](cad/fastener-cad-manifest.csv) | every McMaster file used for the check: name, size, sha256, URL and time. The files are McMaster's and are not committed |
| [`cad/joints.py`](cad/joints.py) | the joint table: where each fastener goes, and the holes it needs cut into the parts it joins |
| [`cad/fastener_bom.py`](cad/fastener_bom.py) → [`fasteners.csv`](fasteners.csv) | the fasteners for one machine with all three build modules, by part number, with packs and cost |

## How the copies were checked

McMaster offers two STEP models of each part: a full one, whose screws have true helical threads, and a "simplified" one with a plain shank at the thread's major diameter. Both were downloaded through the lab Pi for every part below ([`cad/fastener-cad-manifest.csv`](cad/fastener-cad-manifest.csv)). Each part was then rebuilt twice, from McMaster's listed dimensions plus measurements of its model:
- **light:** the shape the machine model uses, compared with the simplified model;
- **detailed:** the thread added as revolved rings with McMaster's axial profile. Rings and a helix with the same profile hold the same volume per unit length (π times the mean of r² over a pitch), so the detailed copy is compared with the full model by volume.

| Part | As listed | Used | McMaster simplified, mm³ | Ours, light | Δ | McMaster full, mm³ | Ours, detailed | Δ |
|---|---|---|---|---|---|---|---|---|
| [95966A705](https://www.mcmaster.com/95966A705/) | Socket Head Captive Panel Screw, M6 x 1 mm Thread, 20 mm Long (6 mm thread, 4.2 mm reduced shank) | 6 | 711.32 | 711.32 | +0.0002 % | 677.94 | 685.46 | +1.11 % |
| [9713K54](https://www.mcmaster.com/9713K54/) | Belleville Disc Spring, 302 Stainless Steel, for 1/8" Shaft, 0.125" ID, 0.25" OD, 0.013" Thick | 6 | – | 7.95 | – | 8.04 | 7.95 | -1.11 % |
| [93600A686](https://www.mcmaster.com/93600A686/) | 316 Stainless Steel Dowel Pin, 6 mm Diameter, 20 mm Long (ISO 2338 m6) | 2 | – | 558.47 | – | 558.47 | 558.47 | +0.0000 % |
| [93395A204](https://www.mcmaster.com/93395A204/) | 316 Stainless Steel Hex Drive Flat Head Screw, 90 Degree Countersink, M3 x 0.5 mm Thread, 10 mm Long | 9 | 82.76 | 82.76 | +0.0015 % | 71.88 | 71.33 | -0.77 % |
| [91732A767](https://www.mcmaster.com/91732A767/) | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M2.5 x 0.45 mm Thread Size, 3.8 mm Installed Length | 3 | – | 9.75 | – | 17.05 | 16.40 | -3.80 % |
| [91732A647](https://www.mcmaster.com/91732A647/) | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M3 x 0.5 mm Thread Size, 4.5 mm Installed Length | 6 | – | 15.25 | – | 27.30 | 26.27 | -3.78 % |
| [91732A649](https://www.mcmaster.com/91732A649/) | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M4 x 0.7 mm Thread Size, 4 mm Installed Length | 6 | – | 25.44 | – | 35.65 | 34.52 | -3.17 % |
| [91732A656](https://www.mcmaster.com/91732A656/) | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M4 x 0.7 mm Thread Size, 6 mm Installed Length | 9 | – | 38.16 | – | 56.16 | 54.00 | -3.85 % |
| [91732A261](https://www.mcmaster.com/91732A261/) | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M5 x 0.8 mm Thread Size, 7.5 mm Installed Length | 24 | – | 67.56 | – | 98.16 | 95.15 | -3.07 % |
| [91732A262](https://www.mcmaster.com/91732A262/) | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M6 x 1 mm Thread Size, 9 mm Installed Length | 4 | – | 122.11 | – | 151.27 | 146.08 | -3.43 % |
| [91732A782](https://www.mcmaster.com/91732A782/) | 18-8 Stainless Steel Helical Threaded Insert, Pronged, M6 x 1 mm Thread Size, 12 mm Installed Length | 6 | – | 162.82 | – | 206.54 | 200.86 | -2.75 % |
| [91065A610](https://www.mcmaster.com/91065A610/) | Retainer for M6 x 1 mm Thread Size Captive Panel Screws, 18-8 Stainless Steel | 6 | – | 9.29 | – | 9.27 | 9.29 | +0.24 % |
| [92029A142](https://www.mcmaster.com/92029A142/) | 316 Stainless Steel Cup-Point Set Screw, M4 x 0.7 mm Thread, 6 mm Long | 2 | 62.51 | 62.51 | +0.0013 % | 49.47 | 49.28 | -0.38 % |
| [92029A152](https://www.mcmaster.com/92029A152/) | 316 Stainless Steel Cup-Point Set Screw, M4 x 0.7 mm Thread, 16 mm Long | 4 | 188.17 | 188.18 | +0.0014 % | 149.48 | 148.60 | -0.59 % |
| [92290A854](https://www.mcmaster.com/92290A854/) | 316 Stainless Steel Socket Head Screw, M2.5 x 0.45 mm Thread, 30 mm Long, Partially Threaded | 3 | 181.34 | 181.86 | +0.29 % | 148.87 | 164.27 | +10.35 % |
| [92290A113](https://www.mcmaster.com/92290A113/) | 316 Stainless Steel Socket Head Screw, M3 x 0.5 mm Thread, 8 mm Long, Fully Threaded | 2 | 117.26 | 117.26 | +0.0003 % | 106.30 | 106.26 | -0.03 % |
| [92290A115](https://www.mcmaster.com/92290A115/) | 316 Stainless Steel Socket Head Screw, M3 x 0.5 mm Thread, 10 mm Long, Fully Threaded | 6 | 131.40 | 131.40 | +0.0010 % | 117.66 | 117.59 | -0.06 % |
| [92290A124](https://www.mcmaster.com/92290A124/) | 316 Stainless Steel Socket Head Screw, M3 x 0.5 mm Thread, 25 mm Long, Partially Threaded | 6 | 236.39 | 237.43 | +0.44 % | 211.84 | 212.37 | +0.25 % |
| [92290A144](https://www.mcmaster.com/92290A144/) | 316 Stainless Steel Socket Head Screw, M4 x 0.7 mm Thread, 10 mm Long, Fully Threaded | 6 | 259.15 | 259.15 | +0.0009 % | 234.04 | 234.06 | +0.0052 % |
| [92290A154](https://www.mcmaster.com/92290A154/) | 316 Stainless Steel Socket Head Screw, M4 x 0.7 mm Thread, 16 mm Long, Fully Threaded | 33 | 334.55 | 334.55 | +0.0006 % | 293.27 | 293.41 | +0.05 % |
| [92290A228](https://www.mcmaster.com/92290A228/) | 316 Stainless Steel Socket Head Screw, M5 x 0.8 mm Thread, 12 mm Long, Fully Threaded | 4 | 474.91 | 474.91 | +0.0001 % | 431.73 | 430.81 | -0.21 % |
| [92290A252](https://www.mcmaster.com/92290A252/) | 316 Stainless Steel Socket Head Screw, M5 x 0.8 mm Thread, 25 mm Long, Fully Threaded | 20 | 730.17 | 730.17 | +0.0001 % | 641.05 | 637.75 | -0.51 % |
| [92290A330](https://www.mcmaster.com/92290A330/) | 316 Stainless Steel Socket Head Screw, M6 x 1 mm Thread, 25 mm Long, Fully Threaded | 20 | 1,095.05 | 1,095.05 | +0.0000 % | 959.67 | 956.41 | -0.34 % |
| [92290A334](https://www.mcmaster.com/92290A334/) | 316 Stainless Steel Socket Head Screw, M6 x 1 mm Thread, 35 mm Long, Partially Threaded | 8 | 1,369.63 | 1,377.79 | +0.60 % | 1,239.54 | 1,244.78 | +0.42 % |

"Used" is the count for one machine with all three build modules ([`fasteners.csv`](fasteners.csv)). The full table, including parts checked but not used and the bounding-box comparison, is [`cad/out/fastener-check.md`](cad/out/fastener-check.md).


## What changed in the model

**The joint table.** [`cad/joints.py`](cad/joints.py) runs at the end of `lpbf_low.build()`. For each joint it places the real parts
and cuts their holes into the parts they join:
- clearance holes at ISO 273 medium sizes, and counterbores for ISO 4762 heads;
- tapped holes drawn at the thread's nominal diameter, a cosmetic thread, so a screw touches its hole without overlapping it;
- helical-insert holes drawn at the insert's installed OD. Aluminium threads that are taken apart more than a few times get
  18-8 helical inserts.

Every screw is 316 stainless (McMaster's 92290A family and its set and flat-head screws), so there is one material inside and
outside the chamber, and no Cu or Zn. The inserts are 18-8, the only stainless McMaster lists for metric helical inserts.

| Joint | Hardware (McMaster) | Count, M50 build | Holes |
|---|---|---|---|
| lid to chamber body | 20 × 92290A252 (316 Socket Head Screw); 20 × 91732A261 (18-8 Helical Threaded Insert) | 40 | Ø5.5 through the lid; M5 STI-tapped 7.5 mm in the body |
| build module flange to the chamber floor | 2 × 95966A705 (Socket Head Captive Panel Screw); 2 × 91065A610 (Retainer for M6 x 1 mm Thread Size Captive Panel Screws); 2 × 91732A782 (18-8 Helical Threaded Insert) | 6 | Ø6.8 in the flange tabs with a Ø8.6 retainer recess; M6 STI 12 mm in the floor |
| build module location | 2 × 93600A686 (316 Dowel Pin) | 2 | Ø6 press fits 10 mm in the floor; Ø6 slip fits in the flange lugs |
| heater block, Macor rings and shields, piston head | 3 × 92290A124 (316 Socket Head Screw); 3 × 91732A647 (18-8 Helical Threaded Insert); 3 × 9713K54 (Belleville Disc Spring) | 9 | Ø7 counterbores and Ø3.4 holes in the head, both slotted ± 0.3 mm radially; Ø3.4 through the rings and shields; M3 STI in the block |
| gland plate to the welded collar | 6 × 92290A154 (316 Socket Head Screw) | 6 | Ø4.5 in the plate; M4 tapped through the 8 mm collar |
| handle to gland plate | 2 × 92290A144 (316 Socket Head Screw) | 2 | Ø4.5 in the handle; M4 tapped 8 mm in the plate |
| hollow rod in the piston head | 2 × 92029A152 (316 Cup-Point Set Screw) | 2 | M4 tapped radially from the head's OD to the rod socket |
| 416 striker to the rod end | 3 × 93395A204 (316 Hex Drive Flat Head Screw) | 3 | 90° countersinks in the striker; M3 tapped 6 mm in the rod end |
| recoater rail to the back wall | 5 × 92290A154 (316 Socket Head Screw); 5 × 91732A656 (18-8 Helical Threaded Insert) | 10 | 6709K33's own Ø4.5 / Ø7.5 counterbores; M4 STI 6 mm in the wall |
| HSS blade to its holder | 2 × 92290A113 (316 Socket Head Screw) | 2 | Ø3.4 in the blade; M3 tapped in the holder |
| window flange to the lid | 6 × 92290A154 (316 Socket Head Screw); 6 × 91732A649 (18-8 Helical Threaded Insert) | 12 | Ø8 counterbores and Ø4.5 in the flange; M4 STI 4 mm in the lid |
| window retaining ring to the flange | 6 × 92290A115 (316 Socket Head Screw) | 6 | Ø3.4 in the ring; M3 tapped 6.5 mm in the flange |
| metering base to the lid | 4 × 92290A154 (316 Socket Head Screw); 4 × 91732A656 (18-8 Helical Threaded Insert) | 8 | Ø4.5 in the base's tabs; M4 STI 6 mm in the lid |
| Z mounting flange to the floor | 4 × 92290A228 (316 Socket Head Screw); 4 × 91732A261 (18-8 Helical Threaded Insert) | 8 | Ø10 counterbores in the flange; M5 STI 7.5 mm in the floor |
| chamber legs to the floor | 4 × 92290A330 (316 Socket Head Screw); 4 × 91732A262 (18-8 Helical Threaded Insert) | 8 | Ø11 bore up each leg; Ø11 access hole in the base plate; M6 STI 9 mm in the floor |
| base plate to the legs | 8 × 92290A330 (316 Socket Head Screw) | 8 | Ø6.6 in the base plate; M6 tapped 12 mm in the leg |
| optics bridge to its posts | 8 × 92290A334 (316 Socket Head Screw) | 8 | Ø6.6 in the bridge; M6 tapped in the post's welded top cap |
| optics posts to the base plate | 8 × 92290A330 (316 Socket Head Screw) | 8 | Ø6.6 in the base plate; M6 tapped in the post's welded bottom cap |

S25 and L75 carry the same joints with their own sizes: S25's stack is 3 × M2.5 × 30 (92290A854) into M2.5 inserts (91732A767), with no disc spring, and its rod set screws are M4 × 6 (92029A142).

- **Lid to chamber body:** Opened only for maintenance, and it must squeeze the lid O-ring evenly and hold it at vacuum, so screws are right here. Inserts because the lid comes off many times over the machine's life and 6061 threads wear; 1.2 mm of metal each side between the gland and the outer wall.
- **Build module flange to the chamber floor:** Swapped by a person between campaigns. The dowel and diamond pin locate the module; the screws only hold it up (the loads are < 0.2 kN against ~6 kN of preload). See hot-swap.md for the robot-swap alternatives.
- **Heater block, Macor rings and shields, piston head:** Replaces M3 screws threaded into Macor (too weak). The screw runs from the cool piston head through three Macor rings, with the two shields clamped between them, into a helical insert in the hot block. Radial slots in the head let the block grow; a disc spring keeps the preload through heat cycles. Heat through the three screws: hot-swap.md.
- **Gland plate to the welded collar:** Replaces a welded bottom flange. A 316L collar welded round the tube end takes 6 x M4; the plate seals on the tube end and collar with a 1.78 mm FKM face O-ring. Take the piston out of the top, then the plate comes off to replace the rod O-rings or clean out powder that passed the bore seal.

**The two choices `build-sequence.md` left open:**
1. **The module's bottom flange is no longer welded to the tube.** A 316L collar ring is TIG-welded round the tube's bottom end
   as part of the module body. The gland plate bolts to the collar with 6 × M4 × 16 and seals on the tube end and collar with a
   1.78 mm FKM face O-ring. With the piston stack lifted out of the top, the plate comes off, so the rod's O-rings can be changed
   and powder that got past the bore seal can be cleaned out of the cylinder. The tube's 3 mm wall is no longer asked to hold a
   thread. The gland plate grows to Ø80.8 / Ø55.4 / Ø106.2 (M50 / S25 / L75).
2. **No screw threads into Macor.** Each of the three standoffs is now three Macor rings with the two polished radiation shields
   clamped between them. One screw per standoff runs from a counterbore in the piston head's underside, up through the head,
   the rings and the shields, into an 18-8 helical insert in the heater block. M50 and L75 use M3 × 25 and S25 uses M2.5 × 30.
   - **The counterbores and holes in the head are radial slots (± 0.3 mm).** The block runs ~100 °C hotter than the head, so at
     the M50 screw circle it grows ~42 µm more. The slots let it slide instead of bending the screw.
   - **A disc spring under each M3 head holds the preload** while the stack heats and cools (M50, L75). There was no room for
     one in S25's Ø5 counterbore.
   - **M50's standoffs moved in from r = 20.1 to r = 18 mm** so the counterbores clear the bore-seal groove.
   - **S25's rod is now 1/2 × 0.035 in. 316 tube** (was 5/8 in.). Its Ø24.8 head has no room for the counterbores beside a
     5/8 in. rod socket.
   - **The heat that the screws carry across the break** is worked out in [`hot-swap.md`](hot-swap.md) §4.

**Smaller changes:**
- **Recoater rail:** McMaster 6709K33's own hole pattern (M4, 60 mm pitch, the first hole 20 mm from the end), counterbored
  as for a 15 mm rail. It replaces a drawn 25 mm pitch.
- **Leveling mounts:** drawn to McMaster 5537T983's listed size: Ø25 base, 20.64 mm body, M8 × 31.75 mm stem threaded up
  through the 15 mm base plate. The drawn foot was 20 mm tall in all, so the base plates now sit 17.4 mm higher. **The
  machine is 581.6 mm tall on the tray, up from 564.2 mm**: still 113 mm under Modula's 695 mm bay S.
- **Optics posts:** 10 mm 6061 end caps TIG-welded into the square tubes, to take the M6 screws.
- **Metering base:** two screw tabs at its ends.
- **Z mounting flange:** 8 mm deeper in y, so two of its four counterbored screws can be reached from below behind the bracket.
- **Module handle:** now screwed under the gland plate with 2 × M4 × 10.
- **Window flange:** screwed to the lid with M4 × 4 inserts, because the cover-slide drawer's slot is only 5 mm under the lid's
  top face.
- **Diamond pin:** the same Ø6 × 20 dowel (93600A686) with two flats ground to leave 2 mm lands across x, the usual shop-made
  relieved pin.

## The animation

[`cad/render_build.py`](cad/render_build.py) now drives the joint table's own screws, at their own positions, in McMaster's
shape:
- **Chapter 1** shows each fastener part number as its own pile.
- **Chapter 2** adds two machining ops to the chamber body: the STI-tapped insert holes from the top, then from below and the
  back. It welds the bottom collar onto the module body.
- **Chapters 3–5** drive every screw in this table, including the new gland-plate, handle, rod and striker screws.

Four sets of screws in the earlier animation were only illustrative: the levelling-mount screws, the door hinge screws, the rack
unit screws and the gas module's feet. They are gone. The levelling mounts now thread in by their own stems. The hinge, latch,
rack and gas-unit screws wait for those parts' hole patterns, below.

## Not drawn yet

- **Door hinges (2 x McMaster 1151A87) to door and chamber:** the hinge's own countersunk holes; screws chosen when the hinge CAD replaces the drawn knuckles
- **Draw latches (2 x 1807A61) and keepers:** 4 screws each, per the latch's hole pattern; not drawn
- **Recoater carriage block to carriage (6709K12), ball nut (4566N401) to block, bearing housings, motor bracket:** M4 per the vendor hole patterns; not drawn
- **Inlet and outlet plenums, overflow funnel block to the chamber (316L to 6061, each with an FKM O-ring):** M4 / M5 316 screws into helical inserts; not drawn
- **Z actuator, carriage, arm and servo; recoater and dosing motors:** per the vendor drawings; not drawn
- **Rack units:** standard M6 cage nuts and screws in the rack's EIA-310 holes; not drawn
- **Gas module units (pump, blower, filter housing, O2 box, manifold) to their base plate:** per the vendor drawings; not drawn
- **Laser guard frame and panels:** T-slot hardware as in BOM line S9; not drawn
- **Galvo to the optics bridge, lens to galvo, camera and gauges:** per the vendor drawings / thread; not drawn

The bought parts other than fasteners (rails, carriages, ball screws, hinges, latches, servos, KF fittings, the pot magnet and
so on) are still drawn from their listed dimensions, as before. Each could be recreated and volume-checked the same way.

## Re-run

```bash
python desktop-lpbf/cad/verify_fasteners.py          # needs McMaster's STEP files in /tmp/mcm_cad (fetch through the Pi tunnel)
python desktop-lpbf/cad/fastener_bom.py              # fasteners.csv
python desktop-lpbf/analysis/interference.py M50     # and S25 S, L75 L
```
