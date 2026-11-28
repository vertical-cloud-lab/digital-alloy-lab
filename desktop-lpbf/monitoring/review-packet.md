# The review packet: what the LSO and the shop are asked to check (2026-11-27)

Issue #260, PR 281. Nothing in the monitoring plan has been bought, measured, or reviewed by BYU's Laser Safety Officer
(LSO) or a machinist. This note doesn't do those reviews. It puts what each reviewer needs in one place: a STEP file and a
view of every part monitoring adds that has to be made, and of every existing part it changes, plus the questions for
each reviewer, with links to where each answer was worked out.

| File | What it is |
|---|---|
| [`analysis/monitoring/review/review_packet.py`](../analysis/monitoring/review/review_packet.py) | builds the model without and with the monitoring parts (`LPBF_MONITORING`), picks the made and the changed parts, writes the STEP files, views and tables |
| [`analysis/out/monitoring/review/parts.md`](../analysis/out/monitoring/review/parts.md) | the two parts tables, with links to each STEP file and view |
| [`analysis/out/monitoring/review/step/`](../analysis/out/monitoring/review/step/) | one STEP file per part, in millimetres and machine coordinates. A changed part also has `<part>-removed.step`, the material monitoring takes off it |
| [`analysis/out/monitoring/review/png/`](../analysis/out/monitoring/review/png/) | views: grey is the part, red is what monitoring removes; `<part>-N.png` is a close-up of the Nth place it changes |
| [`analysis/out/monitoring/review/review_packet.json`](../analysis/out/monitoring/review/review_packet.json) | the same, with sizes, volumes and masses |

## 1. For the Laser Safety Officer

safety.md §1 already plans to register the laser with the LSO's office, and to ask whether the enclosed machine counts as
Class 1 in operation. The guard is the laser boundary: 1.5 mm panels, and a viewing panel of OD 7.8 at 1070 nm (OD ≥ 5.4 is
enough at 500 W). Monitoring adds windows into the chamber, light sources, openings in the guard and an alignment task. Each
item below says what the design does, what the LSO is asked, and where the numbers are worked out.

| # | Item | What the design does | Asked of the LSO | Worked out in |
|---|---|---|---|---|
| L1 | Three new viewports into the chamber: LW (left wall), BW (back wall), LP (lid) | Each passes diffuse and glinting 1070 nm light into the guarded volume. At 500 W that is up to 0.47 W (LW), 0.18 W (BW) and 0.99 W (LP) through the window, and a glint bound of 1.3 W into a camera's pupil at LP. The guard contains it: nothing changes at the guard | Agree that the machine stays Class 1 in operation with the ports open to the guarded volume. Choose between a blank fitted with tools and an interlock for a port whose camera is off | [`optics.md`](optics.md) §5, `viewports.py` |
| L2 | A filter in front of every camera | OD ≥ 8 at 1070 nm on each one. The side and LP cameras have FBH850-10 + FESH1000 (> 11) and the coaxial branch ~14. The existing layer camera has only OD 5.1, so it gets a FESH1000 too | Make "filters on before a camera is powered with the laser on" part of the SOP | [`optics.md`](optics.md) §5 |
| L3 | The coaxial branch above the optics bridge | The DMSP1000 passes 0.3–0.6 W of the forward beam to cube 1's far port, so a beam trap rated ≥ 5 W goes there now, with a FESH1000 (OD 6) behind cube 1. The cage is closed with SM1 tubes | Approve the beam trap, and the cage and tubes as part of the beam enclosure above the bridge | [`optics.md`](optics.md) §0 items 1–2 and §2; [`mechanics.md`](mechanics.md) §1 |
| L4 | Aligning the coaxial branch | The red guide beam passes straight through the DMSP1000, so the branch is aligned and calibrated with the process beam at low power | Write it into the alignment SOP: power limit, eyewear for 1070 nm, beam blocks, who may do it, guard open or closed | [`monitoring.md`](../monitoring.md) §9; the machine's [`optics.md`](../optics.md) §4.4 |
| L5 | The 850 nm light for the side camera, at BW | A Thorlabs M850D3 LED, imaged onto the plate by an asphere outside the BW window and pulsed from the Pico 2. No direct path leaves the guard: its light ends on the bed, the lens tube, the clamp frame and the guard's opaque back panel. As a lamp system it is RG3 in its own beam, inside the closed chamber; the lit bed is exempt by ~700×. With the chamber door open over a bare, polished plate, its reflection out of the door is above the retinal limit for staring past 10 s at 1.5 A CW (under it below 0.85 A). So the light is enabled only with the chamber door shut, or held to ≤ 0.75 A CW for alignment with the door open | Agree that an LED source needs no laser controls, and approve the door-shut enable (the door switch in the driver's enable, or the Pico 2 holding the strobe low) or the 0.75 A alignment limit. Drop the 808 nm, 10 W laser option (BOM M7-10, Class 4) unless the LSO approves it with an interlock | [`optics.md`](optics.md) §4.1 (eye safety, IEC 62471), `bw_light.py` |
| L6 | New openings in the guard | Two light-trapped vents in the guard's back panel keep the cameras in rating: an inlet (176 × 320 mm, low on the left) and an exhaust (244 × 230 mm, on the right, with two 120 mm fans outside). Each trap is a stack of 1 mm aluminium blades bent to six legs, 32 mm deep, with no straight line through it, and off every straight path of the beam. Traced OD at 1070 nm for the worst collimated beam: 7.0–8.1 with black hard anodise, 6.1 with dyed black anodise, ~10 lined with black foil, against the OD 5.4 needed for a direct 500 W beam. Also one bulkhead plate for the monitoring cables (MN-28), on the back panel's upper left over a 152 × 98 mm cut-out, which it laps by 14 mm: three isolated BNC, an RJ45 and an M12 feedthrough, whose closed bodies leave no opening, and a split cable entry whose grommets seal each lead. Over the entry's inside, a black-anodised labyrinth shroud leaves no straight path from the guard to the grommets: the shallowest ray through its channel lands 2.8 mm outside the entry's cut-out. Dust caps close unplugged connectors. The panels in front of the cameras are fastened with tools or interlocked | Approve the traps' attenuation and which finish. Include a trap in the panel burn test (a black blade absorbs ~90 % of a held beam) and in the leakage check with a power meter before first light. Approve the bulkhead, and include it, with its connectors capped and with every lead in place, in the leakage check. Say whether panels in front of the cameras need interlocks | [`cooling.md`](cooling.md) §4–5, `trap_mc.py`; [`mechanics.md`](mechanics.md) §1 and `monitoring_bulkhead.py` (the bulkhead); [`sync-and-data.md`](sync-and-data.md) §4.2 |
| L7 | Monitoring and the safety chain | Monitoring adds no safety input or output and can only ask for a stop. A hold at the next layer goes through the Pi supervisor, a stop through the scan PC, and a hazard through a request bit to the PLC. If a monitor fails, the build is not stopped | Confirm that nothing here needs to be part of the safety chain | [`sync-and-data.md`](sync-and-data.md) §4 |
| L8 | A broken viewport window | The windows are fused silica with a safety factor of 17–34 at 1 atm, and slides in front of them catch spatter. A cracked window is a gas problem (the O₂ permissive catches it), not a laser one: the beam stays inside the guard | Note it | [`mechanics.md`](mechanics.md) Checks §1; [`sync-and-data.md`](sync-and-data.md) §4.2 |
| L9 | Eyepieces and unfiltered cameras | Never fitted to a viewport | Put it in the SOP | [`monitoring.md`](../monitoring.md) §6 |
| L10 | The guard's floor | The guard stands on the process base plate, whose Z-stage window, the slot for the module's rod end and the folded Z servo's window open into the 37 mm gap between the plate and the tray, which is open to the Shuttle all round: ~0.041 m² of free area, without a trap. The cooling CFD found it (most of the guard's air comes in that way). The ports put up to ~1 W of diffuse 1070 nm each into the guard, as the layer camera's window already does. Nobody has traced whether that light can leave through the floor | Decide whether the floor needs a light-tight cover as part of the guard: a sheet-metal plate under the base plate round the Z stage, with a brush strip or labyrinth where the arm and the rod end pass. The cooling needs that cover anyway. Include the floor in the leakage check before first light | [`cooling.md`](cooling.md) §4.2, `guard_cfd.py`; [`optics.md`](optics.md) §5 |

## 2. For the machine shop

The shop's earlier review ([`machining.md`](../machining.md)) covered the machine's own parts. Monitoring adds a few small
parts and cuts features into parts that are made anyway: the frame, the lid, the optics bridge, two liners and the build
module. [`parts.md`](../analysis/out/monitoring/review/parts.md) lists every one with its STEP file and views.

**What the packet holds** (M50; [`parts.md`](../analysis/out/monitoring/review/parts.md) has every size, mass, STEP file and view):

| Kind | Parts | How they're meant to be made |
|---|---|---|
| Laser-cut flat plate | LW window clamp ring, BW window clamp frame, LP blanking cap; the guard's bulkhead plate (0.080 in. 6061, 180 × 126 mm, round 3) | SendCutSend, quoted on 2026-11-27 at $7.43–10.26 each in 6061 ([`fabrication.md`](fabrication.md) §4); the bulkhead plate at $32.85 in 0.080 in. 6061 (SendCutSend's instant quote of 11:23 UTC, from [`bulkhead_plate.dxf`](../analysis/out/monitoring/fab/dxf/bulkhead_plate.dxf); BOM M0-B1) |
| Machined, compound angle | LP adapter boss | bought: SendCutSend CNC priced the layer camera's similar boss at $379 |
| Machined | side camera bracket and its 13° wedge; the BW LED's L bracket and split clamp | outsourced in the BOM (M7-08, M7-05d), or in house |
| Turned | the BW LED's finned heat sink (Ø36 × 40, SM1 internal thread); the AE waveguide's Ø4 head domed R50 on a 1/8 in. 316 rod; the AE cartridge (316L, Ø6.3 × 0.35 wall, 25.8 long, pressed-in cap); the G-10 ring (Ø32 × Ø25.4 × 5, SM1-threaded both ends) | in house |
| Sheet metal | the LW cover-slide clip (0.5 mm 316); the two light traps (55 blades, ~275 bends, in 2 mm frames); the side camera's hood and duct (1 mm, riveted); the exhaust plenum (1.5 mm); the bulkhead's light shroud (1.5 mm, bent and riveted, black anodised) | in house, or a sheet-metal shop for the traps |
| Bought and worked on | the LW purge fitting (bored through) and tube (bent, tip flattened) | in house |
| Cut from sheet | the G-10 pad under the side camera bracket's root (6 × 80 × 16 mm) | in house |

Existing parts that monitoring cuts into, all made anyway:
- **the chamber frame:** the LW port at A90 and the BW slot at A180, with their seats and screw holes, and two M4 holes for the BW
  light's bracket;
- **the lid:** the LP bore on its line of sight, the 2-025 groove and four M4;
- **the optics bridge:** the LP camera's 54.7 × 60.1 mm cut-out;
- **the heater block and both radiation shields:** the AE waveguide's hole, and the block's counterbore for its head;
- **the rod end:** the weld-in's spot face, counterbore and hole;
- **the left liner:** the sight and purge holes;
- **the lower back liner:** shortened;
- **the guard's back panel:** the two vent openings, and the bulkhead's 152 × 98 mm cut-out with eight Ø6 holes for M4 rivet nuts 7 mm outside it.

**Programs.** These programs were posted with FreeCAD 1.0.2 and simulated in CAMotics 1.2.0. A holder, spindle and fixture
check was also run on them. None has been run on a machine.

| Program | Part and setup | What it cuts | Cutting time |
|---|---|---|---:|
| [`frame_C90_with_LW.ngc`](../analysis/out/monitoring/fab/gcode/frame_C90_with_LW.ngc) | frame, setup C at A90 (the existing C90 program with the LW port added) | Ø31 bore, Ø40.2 × 5.5 seat, 4 × M4 on Ø49.5, the SAE-4 purge port | +2.44 min |
| [`mon_C180_BW.ngc`](../analysis/out/monitoring/fab/gcode/mon_C180_BW.ngc) | frame, setup C at A180 | the BW seat and obround slot, the clamp frame's 3 × M4, the BW light bracket's 2 × M4 | 5.11 min |
| [`mon_lid_LP_top.ngc`](../analysis/out/monitoring/fab/gcode/mon_lid_LP_top.ngc) | lid flat, in its top setup | the 2-025 face groove and the adapter's 4 × M4 | 5.84 min |
| [`mon_lid_LP_sine.ngc`](../analysis/out/monitoring/fab/gcode/mon_lid_LP_sine.ngc) | lid on a 27.93° sine plate | the Ø24 bore, one helix | 1.05 min |

CAMotics on the frame's seven programs chained finds 0 rapids through stock and no gouge deeper than 1 mm, and on the lid no gouge
and no leftover deeper than 0.5 mm ([`camotics_walls_monitoring.png`](../analysis/out/monitoring/fab/camotics_walls_monitoring.png),
[`camotics_lid_LP.png`](../analysis/out/monitoring/fab/camotics_lid_LP.png)). The holder check finds 0 collisions in every setup
([`cam_monitoring.json`](../analysis/out/monitoring/fab/cam_monitoring.json)). The lid needs two new tools: a 2.0 mm end mill for
the groove, and a 1/2 in. end mill with 1-1/2 in. of flutes for the bore. **Not programmed:**
- the optics bridge's cut-out (~6 min in the bridge's own top setup);
- the AE features in the heater block, shields and rod end;
- the liners;
- the guard panel's openings;
- every small part above.

**Questions for the shop:**

| # | Part | Question | Where it's worked out |
|---|---|---|---|
| S1 | Frame, left and back walls | Do the LW port at A90 and the BW slot at A180 suit the rotary setup as programmed? The tightest clearance is the 1/4 in. end mill's shank, 2.76 mm from the stock in the BW slot | [`fabrication.md`](fabrication.md) §2 |
| S2 | Lid, LP bore | A Ø24 bore 27.9° off the lid's normal, with the lid on a sine plate, cut as one helix. Is a sine plate or an angle plate better on our mills, or should the lid go out? | [`fabrication.md`](fabrication.md) §3 |
| S3 | Window seats (LW Ø40.2 × 5.5, BW 58 × 27 × 4.5, LP on the boss) | The seat depth sets the squeeze on a 1.0 mm FKM flat gasket: 0.75 mm left gives 15–35 % across the window's ±0.2 mm thickness. Which depth tolerance and floor finish can we hold? | [`mechanics.md`](mechanics.md) Checks §2 |
| S4 | Optics bridge | A ~55 × 60 mm cut-out through the 25 mm bridge for the LP camera. Will it move the bridge's flatness under the scan head? Should it be cut before the final facing? | [`mechanics.md`](mechanics.md) §3 |
| S5 | Heater block and shields | A Ø3.4 hole through the block and both shields for the AE waveguide, and a Ø4.4 × 1.3 counterbore for its head in the socket floor. The hole leaves 0.9 mm of aluminium to the control thermocouple's hole, and the counterbore 0.4 mm over that hole's top 0.6 mm. Can they be cut straight that close, or does the thermocouple's hole need moving? | [`mechanics.md`](mechanics.md) §4.7 |
| S6 | Rod end | The AE sensor's lead leaves through a Solid Sealing FA40102 Microdot weld-in in the rod end's cap. That needs a 7.4 × 7.4 mm spot face milled on the cap's curve (≤ 3.7 mm deep), a Ø6.43 × 0.51 weld counterbore and a Ø5.18 hole into the bore. The weld-in is laser or e-beam welded outside (not TIG), before the rod is TIG-welded on 4 mm away. Can the spot face be milled on the curve? Will the rod's weld disturb the weld-in? | [`mechanics.md`](mechanics.md) §4.5 and §4.7 |
| S7 | Small flat parts | The LW clamp ring, the BW clamp frame and the LP blanking cap are laser-cut outside (SendCutSend quotes). Their thinnest metal is the LW ring's 2.0 mm outside each Ø4.5 hole (2.97 mm from its flat to the nearest hole), and 3.35 mm round the BW frame's third screw | [`fabrication.md`](fabrication.md) §0 and §4 |
| S8 | The side camera's bracket and wedge | A 5/8 in. × 80 mm 6061 plate reaching 184 mm, on an angle root, with a 13° wedge. Is the root stiff enough as drawn? The checks assumed a solid cantilever | [`mechanics.md`](mechanics.md) Checks §3 |
| S9 | Liners and clips | A Ø27 sight hole and a Ø5 purge hole in the left liner, the lower back liner shortened, and a 0.5 mm 316 slide clip | [`mechanics.md`](mechanics.md) §1 |
| S10 | Light traps and the guard's back panel | 55 blades of 1 mm aluminium, each bent to six legs at a 10 mm pitch (~275 bends), black hard anodised, riveted in 2 mm frames; two openings (176 × 320 and 244 × 230 mm) in the 1.5 mm back panel. Can we bend the blades consistently, or should the traps go out? | [`cooling.md`](cooling.md) §4–5 and §8 |
| S11 | BW light: heat sink, clamp, bracket | A Ø36 × 40 6061 heat sink with five fins and an SM1 internal thread, black anodised; a split clamp on its collar; a 1/4 in. L bracket on two new M4 holes in the back wall above the BW clamp frame | [`optics.md`](optics.md) §4.1 |
| S12 | AE cartridge and waveguide | The cartridge is a 316L tube, Ø6.3 with a 0.35 mm wall and 25.8 mm long, with two legs and a pressed-in cap carrying a Ø3.3 guide hole. The waveguide is a Ø4 head domed R50 on a 1/8 in. 316 rod, lapped to length (turned, or a button laser-welded on). Can we turn the thin wall and hold the waveguide's length? The stop force is shimmed at assembly | [`mechanics.md`](mechanics.md) §4.1–4.2 and §4.7 |
| S13 | Hood, duct, plenum and G-10 parts | The side camera's hood and duct in 1 mm aluminium, riveted; the exhaust plenum in 1.5 mm; a 6 mm G-10 pad under the side camera bracket's root, whose root is 6 mm shorter for it; a G-10 ring turned and SM1-threaded both ends | [`cooling.md`](cooling.md) §4 |
| S14 | The guard's bulkhead plate and shroud | A 180 × 126 mm plate of 0.080 in. 6061, laser-cut with four D-size cut-outs (Ø24 and two Ø3.2), an Ø16.1 hole and a 65 × 36 mm cut-out, its face left bare to bond; a 152 × 98 mm cut-out and eight M4 rivet nuts in the 1.6 mm back panel, 4 mm of sheet between each nut's hole and the cut-out; a small shroud bent and riveted from 1.5 mm sheet and black anodised. Are the rivet nuts' edge distances enough, and should the plate go out with the clamp rings? | [`mechanics.md`](mechanics.md) §1 |

## 3. Sign-off

Filled in by the reviewers, not by this note.

| Reviewer | Items | Date | Outcome | Changes asked for |
|---|---|---|---|---|
| BYU Laser Safety Officer | L1–L10 | | | |
| Machine shop | S1–S14 and the parts in [`parts.md`](../analysis/out/monitoring/review/parts.md) | | | |

## Not done / limits

- **The packet shows the M50 module.** The module's own parts change with S25 and L75 (the AE path). Run
  `review_packet.py --module L75` for those.
- **Bought parts are envelopes in the model**, so they aren't in the packet. Their part numbers are in
  [`monitoring-bom.csv`](../monitoring-bom.csv).
- **The views aren't drawings.** They show where each part changes, not tolerances. The shop works from the STEP files and
  the questions above, and asks for a drawing where it needs one.
- **No one has reviewed anything yet.** This is what to send.
