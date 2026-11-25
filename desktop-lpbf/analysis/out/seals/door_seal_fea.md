# Door as a seal carrier: CalculiX, held by its latches (round 6, 2026-11-25)

Door: 6061-T6, 15 mm, with the two latch brackets bonded to its ears, from `cad/lpbf_low.py`. C3D10 mesh, 76165 nodes (hmax 5, hmin 1.5 mm; case C: the door alone, 67776 nodes). Seal centre line 662 mm; 1.78 mm FKM 75A cord in a 1.32 mm deep half-dovetail, so the land is metal-to-metal at 25.8 % squeeze. Cord reaction from Lindley (E = 7.05 MPa from Gent): 1401 N at 25 %, 1490 N at 25.8 %, as a uniform pressure on the groove floor, plus (all but C) springs at Lindley's tangent stiffness, 8.68 N/mm per mm of squeeze per mm of seal, so the cord pushes less where the door bows away. +20 mbar on the 23341 mm² inside the seal (47 N).

Positions read from the model:
- latches (McMaster 1807A61, rated 3558 N): base on the bracket's outer face at x ±146, y -207 to -127, z 34.0-76.2, modelled as a rigid body; pull line x ±158, z 54 (the hook 12 mm off the base, assumed);
- brackets' feet on the ears' front faces: x ±128 to ±146, z 36-72; the pull line is 12 mm outboard of the feet's outer edge and 42 mm outboard of the gland's side runs;
- hinge leaves on the door's front face: x -100 to -80 and 80 to 100, z -6 to 30; pin axis (y, z) = (-132, -12); the pin holes were slotted ±0.6 mm in y until 2026-11-25 (A and D float on them, B and C hold the pins at the slots' ends) and are round since (E, F);
- the land: 2920 nodes of the door's back face with the frame or the floor plate behind them (outside the door opening).

The gland itself spans 19.6-31.6 % squeeze over its tolerances (nominal 25.8 %, seals.py), so the fifth column takes 6.2 % off the lowest squeeze; it should stay at or above 15 %.

| Case | Squeeze along the gland | Lowest at | Margin to 15 % | Lowest at worst tolerance | Cord line load | Contact pressure, mean / peak (Hertz) | Land gap, largest | Each latch | Latch SF on rating | Each hinge (y) |
|---|---|---|---|---|---|---|---|---|---|---|
| **A**: hinges float in their slots (z only), latch hooks held on their pull lines at the 25 % position, cord stiffness | 15.8–20.9 % | bottom (x 0, z 1) | 15 µm | **9.6 %** | 1.00–1.55 N/mm | 1.4–1.8 / 1.8–2.3 MPa | 180 µm at x -0, z -6 (nominal 15) | 383 N | 9.3 | 0 N |
| **B**: as A, with the hinge pins at the ends of their slots (y and z held) | 22.8–25.1 % | top (x 2, z 107) | 139 µm | 16.5 % | 1.79–2.13 N/mm | 1.9–2.1 / 2.5–2.7 MPa | 58 µm at x 2, z 114 (nominal 15) | 30 N | 118.1 | 651 N |
| **C**: round-5 boundary conditions: door alone, the brackets' feet's footprints held in y, hinges y and z, no cord stiffness | 23.1–25.0 % | top (x 0, z 107) | 143 µm | 16.8 % | 1.83–2.12 N/mm | 1.9–2.1 / 2.5–2.7 MPa | – | 208 N | 17.1 | 516 N |
| **D750**: design: each latch preloaded to 0.75 kN (21 % of its rating), hinges floating, the door's land in contact with the chamber's front face where pulled onto it, cord stiffness | 16.1–22.4 % | top (x 0, z 107) | 20 µm | **9.9 %** | 1.03–1.74 N/mm | 1.5–1.9 / 1.9–2.4 MPa | 175 µm at x -0, z 114; 34 of 2920 land nodes touch | 750 N | 4.7 | 0 N |
| **D1200**: design: each latch preloaded to 1.20 kN (34 % of its rating), hinges floating, the door's land in contact with the chamber's front face where pulled onto it, cord stiffness | 15.2–22.0 % | bottom (x 0, z 1) | 4 µm | **9.0 %** | 0.94–1.69 N/mm | 1.4–1.9 / 1.8–2.4 MPa | 192 µm at x -0, z -6; 34 of 2921 land nodes touch | 1200 N | 3.0 | 0 N |
| **E750**: as D at 0.75 kN, but the hinge pins hold the door's bottom edge where its land touches (no float: the hinge set at assembly and locked) | 23.6–25.8 % | top (x 0, z 107) | 153 µm | 17.3 % | 1.90–2.25 N/mm | 2.0–2.2 / 2.5–2.8 MPa | 44 µm at x -0, z 114; 385 of 2920 land nodes touch | 750 N | 4.7 | 1118 N |
| **E1200**: as D at 1.20 kN, but the hinge pins hold the door's bottom edge where its land touches (no float: the hinge set at assembly and locked) | 23.5–25.8 % | top (x 0, z 107) | 151 µm | 17.2 % | 1.89–2.25 N/mm | 2.0–2.2 / 2.5–2.8 MPa | 46 µm at x -0, z 114; 361 of 2920 land nodes touch | 1200 N | 3.0 | 1287 N |
| **F750**: as E at 0.75 kN, with a 12 x 20 mm rib along the door's top edge on its front face (x ±112) | 23.9–25.8 % | top (x 0, z 107) | 158 µm | 17.6 % | 1.95–2.25 N/mm | 2.0–2.2 / 2.6–2.8 MPa | 38 µm at x -0, z 114; 330 of 2922 land nodes touch | 750 N | 4.7 | 1064 N |

Squeeze (%) at points along the gland (the lower of the two sides):

| Case | top centre | bottom centre | top, x = +/-60 | bottom, x = +/-60 | corners, top | corners, bottom | sides, mid-height (latch line) |
|---|---|---|---|---|---|---|---|
| A | 15.8 | 15.8 | 17.1 | 17.0 | 20.1 | 20.1 | 20.9 |
| B | 22.8 | 24.8 | 23.0 | 25.0 | 23.4 | 25.1 | 24.7 |
| C | 23.1 | 24.7 | 23.4 | 24.9 | 24.2 | 25.0 | 24.9 |
| D750 | 16.1 | 16.1 | 17.6 | 17.6 | 21.5 | 21.5 | 22.4 |
| D1200 | 15.2 | 15.2 | 16.8 | 16.8 | 21.0 | 21.0 | 22.0 |
| E750 | 23.6 | 25.6 | 23.8 | 25.8 | 24.4 | 25.8 | 25.5 |
| E1200 | 23.5 | 25.6 | 23.7 | 25.8 | 24.2 | 25.8 | 25.5 |
| F750 | 23.9 | 25.6 | 24.0 | 25.8 | 24.3 | 25.8 | 25.5 |

| Case | von Mises, door | ears | brackets | bracket at the latch patch (model edge) | SF on yield (276 MPa) | Hinge pins' y travel |
|---|---|---|---|---|---|---|
| A | 26.9 MPa | 16.8 MPa | 10.0 MPa | 20.3 MPa | 10.2 (13.6 at the patch) | -124 to -98 µm (slot ±600) |
| B | 21.4 MPa | 6.1 MPa | 2.7 MPa | 2.1 MPa | 12.9 (132.2 at the patch) | 0 to 0 µm (slot ±600) |
| C | 17.5 MPa | 18.4 MPa | 18.4 MPa | 3.0 MPa | 15.0 (92.7 at the patch) | 0 to 0 µm (slot ±600) |
| D750 | 33.6 MPa | 31.8 MPa | 19.1 MPa | 38.0 MPa | 8.2 (7.3 at the patch) | -125 to -92 µm (slot ±600) |
| D1200 | 36.6 MPa | 51.1 MPa | 30.5 MPa | 62.2 MPa | 5.4 (4.4 at the patch) | -137 to -102 µm (slot ±600) |
| E750 | 23.6 MPa | 34.5 MPa | 19.4 MPa | 43.1 MPa | 8.0 (6.4 at the patch) | 0 to 0 µm (slot ±600) |
| E1200 | 26.6 MPa | 52.9 MPa | 30.2 MPa | 64.6 MPa | 5.2 (4.3 at the patch) | 0 to 0 µm (slot ±600) |
| F750 | 26.2 MPa | 34.3 MPa | 19.5 MPa | 42.6 MPa | 8.1 (6.5 at the patch) | 0 to 0 µm (slot ±600) |

Contact (cases D-F): the land is a set of penalty springs (1e+05 N/mm per node) switched on where the door presses on the chamber and off where it would pull; D750: 7 solves, 34 nodes touching, 642 N through the land; D1200: 7 solves, 34 nodes touching, 1608 N through the land; E750: 8 solves, 385 nodes touching, 2287 N through the land; E1200: 9 solves, 361 nodes touching, 3531 N through the land; F750: 8 solves, 330 nodes touching, 2173 N through the land.

Clearances, door shut (exact OpenCascade distances): Draw latches on the door to Optics bridge posts 2.25 mm; Draw-latch brackets on the door to Optics bridge posts 34.00 mm; Draw-latch actuators to Optics bridge posts 14.00 mm.

What it means:
- **The round-5 latches pry the door open (cases D).** Each pulls on a line 12 mm outboard of its ear's tip, and the ear's tip is the outermost place the door bears on the chamber (the chamber's front face ends at x ±156). So the door pivots on the ear tips: the preload goes through the tips, and the door's middle lifts off its land and its cord. More preload, more lift.
- **The fix drawn since 2026-11-25 (cases E): the hinge holds the door's bottom edge.** Round pin holes in place of the ±0.6 mm slots, and the chamber's knuckle blocks shimmed at assembly so the shut door's land just touches. Set each latch to about 0.75 kN, and no more: that is the cord's force at metal-to-metal plus +20 mbar, over two latches. The hinge pins need a close fit; the FEA takes the hinge as rigid.
- Case C repeats the round-4/5 boundary conditions on the new geometry: they hold the ears' front faces, so they can't show a pull outboard of the bearing.

Notes:
- Squeeze is read at the groove floor's nodes: the case's reference squeeze (25 % for A-C, metal-to-metal for D-F) plus the door's displacement toward the chamber over the cord's 1.78 mm. A-C hold the latch hooks (or the ears) where the squeeze would be 25 % with a rigid door; D-F apply the latch preload as a force and let the door find its place on the cord and the land.
- Contact pressure: Hertz line contact of a cord on a flat (E* = E / 0.75), from the local line load. Rough at 20-30 % squeeze; the line load is the firmer number.
- The latch is rigid from its base to its hook: the latch's own stretch, and how its preload changes with the +20 mbar increment, are not modelled.
- The brackets' feet are bonded to the ears: their screws (not drawn in the model) carry the prying from the pull line's offset (mech.md §C).
