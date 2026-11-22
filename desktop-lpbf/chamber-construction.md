# Chamber construction: a through-frame and a bolted floor plate (issue #260, PR #266)

Decision record for the process chamber's body, in answer to the BYU machinist's review of the build animation. He was
most worried about "that big first part where we have to carve a whole bunch of material out", with tooling too long to
find in the shop and "a few hundred hours of toolpathing, and machining". He also judged that he could do the features on
one of the shop's 4-axis machines. Sterling asked us to consider this and look into the 4-axis point. Nothing here has been
built or quoted by a shop.

## Decision

**Make the chamber body as a through-frame cut from 5-1/2 in. 6061-T651 plate, with a 20 mm floor plate bolted under it
on a second FKM face O-ring.**

- The frame's core comes out as one 274 x 184 mm slug, about 17 kg of reusable 6061, cut by waterjet or bandsaw rather than
  milled to chips.
- The walls are finished from the top and from the bottom, 62 mm each way, with a standard 3/4 in. end mill at 63 mm
  stick-out (3.3:1). No long, necked or special tool is needed anywhere on the frame or the floor plate.
- The frame takes three setups on a mill with a 4th axis: bottom up, top up, then the four walls in one clamping on the
  rotary. With 3-axis only it takes six. The floor plate takes two.
- It keeps every function. The interior stays 280 x 190 x 120 mm, and the lid gland, the 20 M5 lid inserts, the door
  opening, the inlet, outlet and overflow slots, the Ø96 port with its dowels and screws, the recoater bores, the KF-25 port,
  the SAE-4 ports, the through-beam holes, the legs and every under-floor mount are all in the model.
- Edison's literature review reached the same choice for a university shop
  ([`edison/r3-chamber-construction/answer.md`](edison/r3-chamber-construction/answer.md)).

| | Before: one block, 120 mm pocket | Now: frame + floor plate |
|---|---|---|
| Stock | 13 x 9.5 x 6 in. block, 12.1 L, 32.8 kg | frame 15 x 9.5 x 5.5 in. (incl. 1 in. clamp tabs, sawn off), floor 1 in. plate |
| Chips | 9.4 L (78 % of the block) | 2.5 L (frame) + 0.9 L (floor); the 7.0 L core comes out as one slug |
| Longest tool | 3/4 in. x 6 in. OAL at 112 mm (5.9:1); a 3/8 in. at 125 mm (13:1) for the R5 corners | 3/4 in. x 4 in. OAL at 63 mm (3.3:1) |
| Tool deflection per 100 N, worst feature | 656 µm (3/8 in., R5 corners and coves) | 5.2 µm (3/4 in., walls) |
| Residual stock, 3-axis with standard tools (voxel simulation) | 29.1 cm³ (3.4 with 6 in. tools) | 1.05 cm³ frame, 0.09 cm³ floor: voxel slivers in the R10 corners and Ø3-4 holes, all of which are cut |
| Inside vertical corners | R5 | R10 |
| Setups | 6 | frame 3 with a 4th axis (6 without), floor 2, plus the waterjet |
| Seals | lid O-ring | lid O-ring + floor O-ring (3.53 mm cord, 947 mm) + 4 bonded washers on the rail holes |
| Mass | 7.4 kg | 4.3 + 3.0 = 7.3 kg |
| Hours: CAM + setups + run + deburr (estimate, [hours](#hours)) | 37 h | 25 h |

## The problem as drawn

The numbers are in [`analysis/out/machining/chamber_frame.json`](analysis/out/machining/chamber_frame.json)
([`chamber_frame.py`](analysis/machining/chamber_frame.py)); the voxel stock-removal runs are in
[`machining.md`](machining.md).

- **Stock.** The block was 13 x 9.5 x 6 in. (12.1 L, 32.8 kg) for a 2.73 L part, so 9.4 L (78 %) became chips. McMaster
  doesn't sell such a block: its thickest rolled 6061-T651 plate is 4 in. (fetched 22:34 UTC).
- **Reach.** Every pocket feature sat 120 mm below the top face:

  | Feature | Reach | Tool | L/D | Deflection per 100 N (tool alone) |
  |---|---|---|---|---|
  | pocket walls | 123 mm | 3/4 in. x 6 in. OAL at 112 mm | 5.9 | 29.5 µm |
  | R5 vertical corners | 125 mm | 3/8 in. at 125 mm | 13.1 | 656 µm |
  | R5 floor coves | 125 mm | 3/8 in. ball at 125 mm | 13.1 | 656 µm |
  | pocket floor | 123 mm | 1 in. x 6 in. OAL at 108 mm | 4.3 | 8.4 µm |
  | recoater-rail insert holes in the back wall's inside face | 216 mm, through the door opening | Ø4.2 drill and M4 STI tap | 51 | (drill) |

  - Deflection is δ = F·L³/(3·E·I) for a carbide rod (E = 600 GPa) of 0.8 D. Mitsubishi Materials models an end mill as a
    rod of 0.7-0.8 D ([course page](https://www.mmc-carbide.com/permanent/courses/70/cutting-edge-classification.html),
    22:33 UTC); 0.7 D bends 1.7 times more.
  - 100 N is about the radial load of a full-height finishing pass in 6061: 0.25 mm radial, 0.05 mm per tooth, ~60 mm of
    flute engaged.
  - Haas says to "reduce cut depth and feed by 50% for long-flute or long-reach tools"
    ([HM42 chart](https://haascnc.com/content/dam/haascnc/ecommerce-assets/linedrawings/milling/end_mills/speeds-and-feeds/Speeds%20and%20Feeds_HM42-3FL.pdf),
    22:41 UTC). Helical suggests necked tools beyond 2-3 x D, and a 50 % feed cut when finishing deeper than 3 x D
    ([guidebook](https://mae.ufl.edu/designlab/Advanced%20Manufacturing/Helical_Machining_Guidebook.pdf) pp. 7-11).
  - So the 3/8 in. corner tool at 13:1 can only take very light cuts, and the long tools roughly quarter the removal rate in
    the lower half of the pocket.
- **Tools that had to be bought:** 6 in. OAL end mills. McMaster's are AlTiN steel grades: 3/4 in. 8745A19 at $307.93 and
  1 in. 8745A657 at $580.54. Lakeshore's longest uncoated 3/4 and 1 in. tools are 5 in. OAL and leave the lowest ~30 mm of
  the walls uncut. Long ball mills or a slim extension holder were needed for the corners and coves.
- **Hours** (the method is in [hours](#hours)): about 13 h of CAM, 6 setups (7.5 h), and 3.5-5 h of cutting at vendor feeds
  (15.5 h on the conservative removal rates machining.md used).
- **What drives the "few hundred hours" is not this part's cutting time.** It is programming and setting up 48 machined
  parts. The block's real costs were the long tools, the 13:1 corners, and the risk of scrapping a $700 block late in its
  program.

## Options compared

| Option | What it takes | Seal and leak | Verdict |
|---|---|---|---|
| 1. Monolithic pocket (as drawn) | 12.1 L block, 9.4 L of chips, 6 in. tools, a 13:1 corner tool, 6 setups | no body joint | rejected: tooling and risk ([problem as drawn](#the-problem-as-drawn)) |
| **2. Through-frame + bolted floor plate** | 5-1/2 in. plate; core out as a slug; 3.3:1 tools; 3 setups with a 4th axis | one more face O-ring (947 mm), metal to metal; +0.44 ppm/h O₂ by permeation ([seal cost](#what-the-floor-joint-costs)) | **chosen** |
| 3. Heavy-wall rectangular tube + end plates | McMaster stops at 8 x 8 in. with a 1/2 in. wall (6546K91, $420.00/ft); nothing near 12.3 x 8.7 in. with a 5/8 in. wall. Edison estimates a custom die at $5-15k. | two end O-rings | rejected: not stocked |
| 4. Welded box (TIG 6061, 5083 or 316L) | plates + a qualified vacuum welder, then post-weld machining of every sealing face; raw distortion 0.5-2 mm on a box this size (Edison's estimate); the 6061 HAZ drops to ~110 MPa | continuous welds, helium leak test | rejected for a first build: the same machining plus weld risk |
| 5. Bolted box of plates, O-rings in every joint | simple plates | three-way O-ring junctions at 8 corners; many glands | rejected |
| 6. Commercial chamber | nearest catalogue chambers are 12 in. cubes at $3,610-8,860 (LACO, Ideal Vacuum, Kurt J. Lesker); welded aluminium starts at 16 in. ($9,811, 8 weeks) | certified | rejected: too big for the 600 mm VLM height and the 312 x 222 footprint, and the door, slots and ports would still have to be cut into it |

Prices and listings for options 3 and 6 were fetched 2026-11-20 between 22:31 and 22:45 UTC: McMaster rectangular tube
(6546K91 and family), and the [LACO store](https://store.lacotech.com/vacuum/?page=1),
[Ideal Vacuum](https://www.idealvac.com/16-in-Cubic-Vacuum-Chamber-6061-T6-Aluminum/pp/P1011945) and
[Kurt J. Lesker](https://www.lesker.com/newweb/chambers/std_box_vacuum_chamber.cfm) pages.

## The design, as it now is in the model

The code is section 5 of [`cad/lpbf_low.py`](cad/lpbf_low.py) (constants in `FRAME`) and the `floor` and `rail` joints in
[`cad/joints.py`](cad/joints.py). Each part is built as its blank minus an ordered list of cuts, one per machining
operation (`CHAMBER_OPS`, ids `FR-01`…`FR-13` and `FP-01`…`FP-07`). The setup plan and the build animation name those
cuts.

### Frame ("Process chamber body …", 1.58 L, 4.3 kg)

- **Walls and height.** Walls 16 mm and 123.9 mm tall: the interior's 120 mm plus a 3.9 mm skirt below the floor-joint
  plane (z = 0). The outer corners are R8 and the inside vertical corners R10. A 3/4 in. end mill (R9.5) finishes them
  from each side.
- **Rebate, 8 mm wide x 3.9 mm tall,** round the bottom of the opening. The floor plate's 4 mm pad sits in it, 0.25 mm
  clear per side.
- **Why the skirt.** With the joint flush at z = 0, three seals on the outer faces would cross it, and each would leak
  along the joint line into its own sealed area:
  - the inlet plenum's O-ring reached z −6.8;
  - the through-beam heads' 2-010 grooves reached z −0.4;
  - the door O-ring's land came within 0.85 mm.

  The skirt keeps all of them on the frame. The joint itself (z = 0) is inside, under the walls.
- **Unchanged from the block:** the lid gland and the 20 M5 lid inserts in the top face, the Ø18 recoater bores, the KF-25
  bore and its 4 M5 inserts, the bearing-cap inserts, and the SAE-4 argon and O₂ ports.
- **Through-beam** (M6 x 0.75 at z +5): its 2-010 O-ring now sits in a Ø10.8 x 1.32 counterbore, on the thread's crest, as
  in an SAE / ISO 6149 port. The old face groove's inner wall was 0.1 mm thick round the thread, which `dfm.py` flagged
  and which also broke the FEA mesh.
- **Door opening:** same size (220 x 92), now with R6.5 corners for a 1/2 in. tool.
- **Inlet slot:** same size (120 x 8 at z 4…12), now with round ends.
- **Recoater-rail holes.** Four M4 holes are tapped *through* the back wall from outside. The rail screws go in from inside,
  and an M4 x 10 plug screw on a bonded seal washer closes each hole's outer end; the two screw tips are 1.2 mm apart.
  - Before, the inserts were in the wall's inside face. Any drill or tap had to come in through the door opening, 206 mm
    from the front face (the coordinator's options a-d).
  - This choice needs only a standard Ø3.3 drill and M4 tap, cut in the same back-face index as the inlet slot, at the cost
    of 4 small face seals.
  - The alternatives considered were: an extension drill and tap through the door (the long-reach problem again); a
    right-angle head (no BYU page lists one); hand-drilling through a jig with the frame open; or a rail bar bolted from
    outside, which would move the rail 20 mm and change the recoater.
- **Rail 260 mm** (was 270), so that its ends stop at the R10 back corners. Its holes are at x −110/−50/10/70, and the
  carriage block stays on the rail over the full stroke.
- **Inlet plenum.** Its cavity floor rose from z −3 to +1.5 so that its 2-044 groove stays at z ≥ −2.3, on the frame. Its
  4 screws below the old floor line moved to the sides (7 screws, was 9).
- **Lift-out liners** stop 9.5 mm short of each inside corner (was 8) to clear the R10 corners. They still fit: 0 in the
  interference check.

### Floor plate ("Chamber floor plate …", 1.12 L, 3.0 kg)

- 312 x 222 x 20 mm (z −20…0) from 1 in. 6061-T651. McMaster's 89155K165 (12 x 24 in., $267.02) gives one blank.
- **A 4 mm pad** (295.5 x 205.5, R17.75) carries the floor O-ring's face gland, and the edge band round it is 4 mm lower.
- **Through features,** now 3-axis plate features: the Ø96 H7 port; the outlet slot (124 x 8) and overflow slot
  (20 x 104), both now with round ends or R4 corners (the overflow funnel's pocket got the same R4).
- **Blind holes from below** for the module's thumb-screw inserts, dowel and diamond pin, the outlet-plenum, funnel,
  Z-flange and leg inserts.
- 18 U-notches at the edge for the floor screws.

### Floor joint

- **O-ring:** FKM 75A, 3.53 mm cord with a vulcanized splice, the same section as the lid's.
  - Groove 2.65 deep x 4.6 wide (Parker face gland for 0.139 in.: 2.57-2.72 x 4.50-4.75).
  - Its inner wall is 1.5 mm outside the walls' inner faces (R11.5 corners), on a 947 mm path.
  - Squeeze 24.9 % (21.2-28.4 % at ±0.05 mm and cord tolerance); fill 80 % (88 % worst cold).
  - One closed loop: no three-way junctions.
- **Screws:** 18 x M4 x 16 316 socket head (McMaster 92290A154, from `cad/fasteners.py`).
  - They go up through U-notches in the plate's edge band into tapped holes on the skirt's centre line, 12 mm outside the
    inner faces and outboard of the O-ring.
  - Plain tapped 6061 rather than inserts: an insert would leave 1 mm webs in the 8 mm skirt, and the floor comes off only
    for major maintenance.
  - The heads sit 8 mm up in the notches. That keeps them clear of the outlet plenum and the Z flange under the floor, and
    they can still be reached with the plenum on.
- **Spacing is set by what's under the floor and in the walls.** The tapped holes end at z +5.5, 2.5 mm under the door sill.
  They stay out of the inlet slot (|x| < 64 at the back), the plenum and Z-flange inserts, the through-beam, the legs and
  the door-hinge blocks: 6 screws front, 4 back, 4 each side.
- **Dowels:** 2 x Ø6 x 20 m6 316 (McMaster 93600A686), at the front-left and back-right corners. They are pressed into the
  plate and a slip fit in the frame.
- **Clamping.** The screws pull the pad's top face onto the frame metal to metal. The O-ring's squeeze is then the groove
  depth, and the skirt's bottom stays 0.1 mm clear of the band.
- **Crevice (powder trap).** The old R5 floor cove is gone. The floor meets the wall at a 90° corner whose joint line is a
  clamped hairline, 1.5 mm deep to the O-ring.
  - With a 0.025 mm flatness on both faces, the worst-case crevice volume is 1.5 x 0.025 x 940 = 35 mm³; the
    preload-clamped gap is far smaller.
  - It is narrower than the powder's D10 (~20 µm for 20-63 µm AlSi10Mg), and a vacuum nozzle reaches the corner.
  - Specify: deburr the frame's inside bottom edge to ≤ 0.1 mm with no chamfer, so the line stays a hairline; and face both
    sealing faces flat to 0.025 mm, Ra ≤ 0.8 µm.

**Shigley bolted-joint check** (Budynas & Nisbett, *Shigley's Mechanical Engineering Design* 10th ed., ch. 8; FEA case
1f, [`analysis/out/fea/fea.md`](analysis/out/fea/fea.md)):

- **Preload.** Proof strength is taken as 210 MPa: McMaster rates its 316 screws at 70 ksi tensile, and A4-50's yield is
  used as a conservative proof. That gives 1,383 N per screw at 1.1 N·m (K = 0.2), 24.9 kN in all.
- **Stiffness.** Grip 8.1 mm, k_b = 168 kN/mm, k_m = 304 kN/mm (30° frustum), so C = 0.356.
- **Threads and bearing.** 7.9 mm of engagement in 6061: the thread would strip at 7.9 kN, against 4.2 kN to break the
  screw. Head bearing is 61 MPa.
- **O-ring force:** 4.0 kN nominal (Lindley / Gent as `seals.py`), 5.1 kN at maximum squeeze, 9.1 kN on Parker's 80A bar.

| Case | Load on the joint | Load factor n_L | Separation factor n₀ |
|---|---|---|---|
| nominal O-ring, +20 mbar | 4.06 kN | 5.7 | 9.5 |
| O-ring at maximum squeeze, +50 mbar (relief valve at +34) | 5.37 kN | 4.3 | 7.2 |
| Parker 80A bar, +50 mbar | 9.40 kN | 2.5 | 4.1 |
| Parker 80A bar, +0.5 bar regulator fault | 11.95 kN | 2.0 | 3.2 |
| full vacuum | −1.79 kN: the atmosphere presses the plate on | – | – |

So the joint never opens in service, even with the stiffest O-ring and a regulator fault.

### What the floor joint costs

- **O₂ by permeation.** The floor O-ring runs at ~60 °C, near the heated module. With `seals.py`'s own Parker permeation
  model it lets in 1.41e-6 scc/s of O₂, against 9.5e-7 for the lid. That is +0.44 ppm O₂/h on the 1.76 ppm/h of every seal
  together ([`analysis/out/seals/seals.json`](analysis/out/seals/seals.json)), so holding 10 ppm takes about 44 sccm of Ar
  make-up flow instead of 35.
- **The 4 bonded washers** add about 0.02 ppm/h.
- **Mass:** 18 more screws and two dowels, about 50 g.
- **One more step in assembly.** The floor goes on the legs first, then the O-ring, the frame, the dowels and the screws.

## Structure (CalculiX)

[`analysis/fea/fea.py`](analysis/fea/fea.py) cases 1, 1b and 1f; results in [`analysis/out/fea/fea.md`](analysis/out/fea/fea.md).
Both chamber cases use 6061-T6 (yield 276 MPa), quadratic tetrahedra and the four leg pads under the floor plate fixed.
Loads: suction on every wetted face; the lid (case 1) and the door carried on their lands; and the module, outlet plenum and
funnel, which close the port and the two slots from below, pushing up on the floor plate round their openings.

| Case | Mesh | Peak σ_vM | 99.5 % | Largest displacement | Seal faces | Safety factors |
|---|---|---|---|---|---|---|
| 1: frame + floor plate, open top (the lid's 5907 N on the top land), full vacuum | 139,613 nodes | 54.4 MPa at the door opening's top corner (inside edge, R6.5) | 22.3 MPa | 208 µm at the top of the front wall | door land Δy 194 µm; lid land Δz 84 µm | yield 5.1; Goodman (vacuum cycles) 2.7; welded-HAZ allowable 2.0 |
| 1b: frame + floor plate + lid, full vacuum | 284,108 nodes | 28.0 MPa at the inlet slot's round end (back wall, x 60, z 8) | 9.6 MPa | 63 µm at the floor plate's centre | door land Δy 4.3 µm; window seat 49 µm | yield 9.9; Goodman 5.3; HAZ 3.9 |
| 1b′: the same at +20 mbar (argon working pressure) | same mesh | 0.55 MPa | 0.19 MPa | 1.2 µm | door land Δy 0.08 µm | yield 500 |
| block + lid, before (old case 1b) | 166,211 nodes | 9.1 MPa | 4.1 MPa | 24 µm | door Δy 4.1 µm; window seat 24 µm | yield 30; Goodman 16 |
| block, before (old case 1) | 131,797 nodes | 42.9 MPa | 21.3 MPa | 223 µm | door Δy 209 µm; lid Δz 79 µm | yield 6.4; Goodman 3.4 |

- **Case 1 is the worst case.** With the top open, the front wall's beam over the door bows in and peaks at the opening's
  top corners. With the lid on (case 1b) the lid ties the top of the walls and the peak halves.
- **Case 1b's peak is higher than the block's 9.1 MPa**, though still a yield SF of 9.9. Two things
  differ:
  - Case 1b now also carries the module, plenum and funnel pushing up under the floor (1.2 kN). That bows the floor plate
    63 µm and loads the round end of the inlet slot just above the floor joint.
  - The window seat sags 49 µm, against 24 µm before. That is negligible beside the
    beam's ±3.7 mm Rayleigh range.
- **At +20 mbar everything is tiny** (the linear model just reverses the loads and scales them by 0.002/0.1013): the
  joint sees at most +0.17 MPa of tension against 8.3 MPa of preload.
- **The floor joint stays closed.** Across the joint in case 1, σz averages -0.86 MPa
  (compression), with at most +0.34 MPa of tension locally. The 18 screws' preload puts
  8.3 MPa on the lands, and at vacuum the atmosphere presses the plate on.
- **Modelling.**
  - The joint is bonded over its full width. The 0.1 mm skirt gap, the 0.25 mm pad clearance and the groove are filled,
    because gmsh can't mesh the thin slots. So the joint is stiffer than its 3 mm of real lands; case 1f checks the joint
    itself.
  - The fastener holes are left out of the meshed bodies. With every M4 and M5 hole the mesh is 3.6 times the old case's,
    and OCC flags slivers where the floor screws' holes meet the joint. The holes don't change the global stress.
- **The floor joint (case 1f, Shigley)** is in the table above: separation factor 3.2 to 9.5 across the cases, load factor
  2.0 to 5.7.

## Machining it

The full plan is in [`analysis/out/machining/setup_plan.json`](analysis/out/machining/setup_plan.json)
([`setup_plan.py`](analysis/machining/setup_plan.py)), and [`machining.md`](machining.md) has the summary. In short:

- **Frame:**
  1. Saw the blank. Waterjet the core out from a Ø12 start hole: 35.6 in. of cut at 0.5-2.9 ipm, scaled from WARDJet's
     4 in. aluminium data, so 12-71 min. Or trepan it on the mill from both sides.
  2. **F-S1, bottom up**, toe clamps on the end tabs: face the bottom; the lower halves of the outside and the opening; the
     rebate; the 18 M4 holes and 2 dowel holes.
  3. **F-S2, top up**, on a "dummy floor" fixture plate that pins and screws the frame down through its own floor-screw
     holes: face the top; the upper halves; the lid gland; the lid inserts.
  4. **F-S3, the four walls in one clamping** on an HRT210-class rotary, A along the frame's z: the door opening, the
     slots, bores, ports and inserts. The dummy-floor plate goes on the platter. The frame swings 188 mm about A, more than
     the HRT210's 152.4 mm centre height, so the rotary needs a 2-1/2 in. riser.
- **Floor plate:** P-S1 top up (face, pad step, gland, port, slots, dowel and clearance holes), then P-S2 bottom up on two
  pins and a centre stud through the port (face, outer profile, notches, blind holes).
- **Time on the mill** at vendor feeds (Helical, Haas; 60 % efficiency): frame 112 min, floor plate 51 min, plus 12-71 min
  on the waterjet.
- **FreeCAD 1.0.2's CAM workbench,** run headless, programmed the same features and posted G-code: 60 min of cutting for the
  frame and 58 min for the floor plate ([`freecad_cam.json`](analysis/out/machining/freecad_cam.json)). Its O-ring grooves
  used a slow 1/8 in. tool and account for 38 and 35 min of that. FreeCAD didn't time taps, reamers or tool changes.
  CAMotics 1.2.0 then cut that G-code setup by setup, in Docker on Ubuntu 18.04 because its 2019 package needs V8 3.14
  and OpenSSL 1.1, which the runner's Ubuntu 26.04 lacks. It found seven problems in the facing, floor-drilling, stock
  and comment settings. With them fixed there are no gouges and no rapids through stock, and the cutting time is 58 min
  for the frame and 60 min for the floor plate ([`machining.md`](machining.md#g-code-simulated-in-camotics-2026-11-22)).

## Hours

The per-part model is [`hours.py`](analysis/machining/hours.py), output
[`hours.json`](analysis/out/machining/hours.json) and [`hours.csv`](analysis/out/machining/hours.csv).

- **CAM hours are an estimate.** A search found no published rule of thumb.
- **Setups** are at 0.75 h for vise parts and 1.25 h for large ones. Modern Machine Shop's survey median is 68-90 min, last
  good part to first good part ([MMS](https://mmsonline.com/articles/best-practices-of-top-us-shops), 22:43 UTC).

| Chamber body | CAM | Setups | Run | Deburr + inspect | Total |
|---|---|---|---|---|---|
| Before: block, 6 setups | 12.8 h | 7.5 h | 15.5 h (conservative) / 3.5-5 h (vendor feeds) | 1 h | 37 h (25-26 h at vendor feeds) |
| Now: frame (3 setups with a 4th axis) + floor plate (2) + waterjet | 8.2 h | 7.5 h | 7.1 h / 3.5 h | 2 h | 25 h (21 h) |

The machine as a whole is in [`machining.md`](machining.md#hours-for-the-whole-machine).

## Checks run on the new model

- **Interference** ([`analysis/interference.py`](analysis/interference.py), exact booleans, 5 states and 8 motion sweeps):
  0 interferences for M50, S25 and L75 on the final model (23:40-23:55 UTC). The outputs are
  [`analysis/out/interference.md`](analysis/out/interference.md) and `analysis/out/variants/interference-{S25-S,L75-L}.md`.
  - An earlier run caught one pair that wasn't the chamber's: another change's robot lift lug on the door touched the
    guard's viewing window. That lug has since been removed.
  - The 8 designed contacts the floor plate needs (spigot O-ring, module, thumb screws, dowels, module sensor, blade, floor
    O-ring) were added to `JOINTS` for the run. They have to go into `interference.py` itself; see the patch list below.
- **Machining:** `cam_sim.py`, `per_setup.py`, `dfm.py`, `setup_plan.py` and FreeCAD CAM ([`machining.md`](machining.md)).
- **FEA:** cases 1, 1b and 1f ([structure](#structure-calculix)).

## Second opinion: Edison r4 (2026-11-22)

Edison reviewed this design on 2026-11-22. The query was written in round 3 and sat unsent until the account had
credit again: [`edison/r4-frame-floor-review/`](edison/r4-frame-floor-review/) has the query, answer, references and full
trajectory. Each point below is checked against the model.

- **The lid's bolt land is thin. New, and not drawn.**
  - **What Edison says:** a 3.53 mm cord gland next to an M5 helical insert needs about 17.1 mm side by side, using its
    3 mm ligament allowance, against the 16 mm wall.
  - **What the model has:** `cad/joints.py` puts the 20 lid inserts at 11.8 mm outside the inner face. The
    gland's outer edge is at 7.6 mm. The Ø6.04 insert hole then leaves **1.18 mm of web to the gland and 1.18 mm to the
    outer face**, over the groove's 2.65 mm depth. [`machining.md`](machining.md) already lists "thicker webs at the
    lid inserts" as a change to draw.
  - **Options, by web left on each side:**

    | Option | Web each side | Trade-off |
    |---|---|---|
    | M4 inserts (91732A656) | 1.75 mm | – |
    | Plain tapped M5 | 1.7 mm | the lid comes off for service, so 6061 threads wear |
    | A 4 mm external lip round the frame's top band, with M5 inserts | 3.2 mm | the outside grows to 320 × 230 mm there, which fits the 241 × 381 mm blank, but the door's seal land on the front face has to be checked against it |
- **Floor crevice: already done.** Edison recommends a spigot or step so the floor locates inside the frame and seals on
  a horizontal face. The floor plate's 4 mm pad already sits in the frame's 8 × 3.9 mm rebate, with the O-ring on the
  pad's face. The worst-case crevice is about 35 mm³ (above).
- **Residual stress: new, add to the plan.**
  - Confirm the blank is certified T651 (stress-relieved by stretching), not plain T6.
  - Rough the core and the opening first, leaving 0.5–1 mm on the top, bottom and door sealing faces.
  - Unclamp, let it relax, re-indicate, then finish. With symmetric passes from both ends, Edison estimates the sealing
    faces stay within 0.1 mm. That figure is an estimate, not a measurement.
  - In the setup plan this adds a re-clamp between roughing and finishing in F-S1 and F-S2.
- **Taking the core out: agrees with the plan.** For a university shop Edison favours drilled corner holes plus a
  bandsaw, or waterjet at a job shop. It rates wire EDM as too slow and costly for roughing.
- **Blind tapped holes and virtual leaks.**
  - **Edison's advice:** at 1 mbar and with argon above ambient they are minor; use vented screws where a blind hole
    opens inside the seal, and clean and dry every hole.
  - **The model:** the lid and floor screw holes sit outboard of their glands, and the rail holes are tapped through
    and plugged from outside.
  - **Not checked:** the other joints, hole by hole.
- **Where Edison is wrong or out of date:**
  - **Gas flow:** its "3.8–7.6 L/min" for 2 m/s over the bed is a unit slip. 2 m/s through 190 mm × 10–20 mm is
    3.8–7.6 L/s, or 228–456 L/min. [`gas-flow.md`](gas-flow.md) sizes 140–200 L/min through the perforated 120 × 8 mm
    slot.
  - **FKM at 200 °C:** the spigot O-ring runs at ≤ 121 °C in the thermal FEA ([`modules.md`](modules.md)), not at the
    plate's 200 °C.
  - **Anodising:** Edison suggests it against galvanic attack. The materials selection already rejects it inside the
    chamber, because it outgasses 41–68× more water ([`low-profile.md`](low-profile.md) §3). Keep the 316 screws and
    18-8 inserts dry and use anti-seize.

## Scripts that should learn about the floor plate

The frame keeps the name prefix "Process chamber body", so scripts that look it up still find it. The floor plate is
"Chamber floor plate …", and the floor O-ring is "Floor O-ring …".

| Script | What it needs |
|---|---|
| `analysis/interference.py` | add to `JOINTS`: (`Spigot O-ring`, `Chamber floor plate`), (`Build module`, `Chamber floor plate`), (`Captive M6 thumb screws`, `Chamber floor plate`), (`Locating dowel`, `Chamber floor plate`), (`Module-present sensor`, `Chamber floor plate`), (`HSS recoater blade`, `Chamber floor plate`), (`Floor O-ring`, `Chamber floor plate`), (`Floor O-ring`, `Process chamber body`). These are exactly the entries the committed outputs were run with. |
| `analysis/ops/operations.py` | assembly A2: the floor plate onto the legs (the leg screws now go into the floor plate), then the floor O-ring, the frame (dowels), and the 18 floor screws (`floor`, `floor_dowels`); the rail screws' new plugs (`rail_plugs`) |
| `analysis/seals/seals.py` | picks up `GLANDS["floor"]` by itself; its text "the body machined from solid (no welds to leak)" should say a bolted floor; re-run it |
| `cad/render.py` | add `"Chamber floor plate"` and `"Floor O-ring"` to `SECTION_KEYS` |
| `cad/render_build.py` | chapter 2: machine the frame and the floor plate from `CHAMBER_OPS` and `setup_plan.json` instead of the block |
| `cad/vendor_parts.py` | its check table still says the rail is 270 mm (now 260) |
| `analysis/shop/shop_checks.py` | uses the old block's volume (330.2 x 241.3 x 127 minus the pocket) |
| `analysis/mass_budget.py` | nothing (it sums every part) |
| notes | `gas-flow.md`'s geometry table: the inlet plenum's cavity is now z 1.5…25, and the slot has round ends. `build-sequence.md`, `operations.md` and `followup-checks.md` describe the body as one block. |

## Sources

Fetched 2026-11-20, times UTC.

- **Machines.** Haas [VF-4](https://www.haascnc.com/machines/vertical-mills/vf-series/models/medium/vf-4.html) (22:27) and
  [HRT210](https://www.haascnc.com/machines/rotaries-indexers/rotary-tables/models/hrt210.html) (22:31), through the lab Pi.
- **BYU shops.** Physics' VF-2SS "provides new capabilities like a 4th axis"
  ([news](https://physics.byu.edu/department/news/2020-08-new-mill-becomes-part-of-the-p-a-family), 22:31). No BYU page
  names a rotary model, a trunnion, a 5-axis machine or a right-angle head (pages checked 22:31-22:46).
- **Feeds and speeds.**
  - Helical's [aluminium parameters](https://cdn.shopify.com/s/files/1/0612/0733/files/Helical_Aluminum_Parameters.pdf)
    (22:32) and [Machining Guidebook](https://mae.ufl.edu/designlab/Advanced%20Manufacturing/Helical_Machining_Guidebook.pdf)
    (22:32).
  - Haas end mill, insert, drill and tap charts (22:41).
  - [WARDJet](https://www.wardjet.com/nozzle-and-orifice/) waterjet speeds (22:39).
- **Stock and chambers.**
  - McMaster plate and tube (22:31-22:37).
  - OnlineMetals' [tolerance table](https://www.onlinemetals.com/en/aluminum-tolerances) (22:37). It gives ±0.130 in. for
    3.937-6.299 in. plate, which is why the frame comes from 5-1/2 in. plate.
  - Metals Depot's [6061 plate page](https://www.metalsdepot.com/aluminum-products/6061-aluminum-sheet-plate) (22:43).
  - The chamber vendors listed under [Options compared](#options-compared).
- **Edison.** `LITERATURE_HIGH` on chamber construction, [`edison/r3-chamber-construction/`](edison/r3-chamber-construction/).
