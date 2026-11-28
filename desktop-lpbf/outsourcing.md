# Outsourcing: what to make at BYU, what to send out, what to buy (2026-11-22)

For [issue #260](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/260) and PR 266. Sterling asked us to look
into outsourcing options and prices for the custom parts, with uploads and automated quotes where they exist, to decide
what is made in house and what is outsourced.

How it was checked:

- Every custom part was exported from the model (`cad/lpbf_low.py` at commit 9f45d80, M50 module) as STEP in mm, plus DXF
  for the flat profile parts: 68 machined and sheet parts and 14 robot-tooling parts, 82 files in all
  ([`export_parts.py`](analysis/outsourcing/export_parts.py), [`parts.csv`](analysis/out/outsourcing/parts.csv)).
- The instant-quote sites were driven in headed Chrome on a virtual display, through the lab Pi's SOCKS tunnel (BYU
  network), on 2026-11-22 between 05:31 and 06:22 UTC.
- No account was made. No name, e-mail or address was typed, no terms were accepted and nothing was ordered or put in a
  cart. 51 distinct part files were uploaded ([`uploaded-files.csv`](analysis/out/outsourcing/uploaded-files.csv)
  gives the sha256 and size of each).
- Every attempt, priced or not, is a row of [`outsourcing-quotes.csv`](outsourcing-quotes.csv) (59 rows), with a
  screenshot in [`analysis/out/outsourcing/`](analysis/out/outsourcing/).
- Prices for work no site quotes instantly (honing, welding, finishing, the frame blank, standard chambers, shop rates)
  came from public pages (89 rows in [`research.csv`](analysis/out/outsourcing/research.csv)) and from Edison's sourced
  review ([`edison/r5-outsourcing/answer.md`](edison/r5-outsourcing/answer.md), cited below as "Edison r5").
- [`should_cost.py`](analysis/outsourcing/should_cost.py) compares, part by part, the in-house cost (shop hours from
  [`hours.csv`](analysis/out/machining/hours.csv) at a stated rate, plus stock and the tools in
  [`tooling-bom.csv`](tooling-bom.csv)) with the outsourced price. It then makes the call. Results:
  [`should_cost.csv`](analysis/out/outsourcing/should_cost.csv) and `.json`.

## Short answer

- **Who gave a price without an account:**
  - **SendCutSend**, for sheet and plate cutting and, new since Edison r5 was written, CNC machining of 6061 parts.
    - Its check states a largest billet of 8 × 8 × 12 in. It still priced the 12.3 × 8.7 in. lid and floor plate, but
      it rejected the frame, the base plates and the optics bridge.
    - It priced 36 parts in 39 rows: sheet and plate $3.55–689.66 a part, CNC $47.55–1,075.62.
    - Delivery dates were Nov 27 to Dec 7, 5 to 15 days out.
  - **OSH Cut**, for stainless sheet: $22.85 for a 316 liner.
  - **JLCCNC**, for one CNC part: the 316L overflow block at $123.46 in 304 (316L isn't in its instant list), with a
    6-day build plus 2-4 days UPS at $25.99.
  - **JLC3DP**, for one printed fixture: $26.20 in resin.
- **Who wanted an account first:** Xometry asks for a business e-mail, and so does RapidDirect (with its terms).
  Protolabs wants a full sign-up (name, company, e-mail, phone, postal code). Fictiv opens on a log-in page.
  - Protolabs Network (Hubs) asks for an export-control declaration before upload, and Craftcloud asks you to accept its
    terms. I made neither on the lab's behalf.
  - Big Blue Saw now redirects to Xometry, whose bot check failed. PCBWay's CNC page is a reviewed request form.
- **Cost (in-house at $65/h, including the $3,695 of tools to buy).** $65/h is the academic labour rate of BYU's
  Prototype Manufacturing Lab. It was seen only in search results for pml.byu.edu; the page itself wasn't read.

  | Route | Shop hours here | Cost | In-house queue at 20 h/week |
  |---|---:|---:|---:|
  | Everything made here | 329 h | $32,534 ($42,395 at $95/h; $11,169 if the labour is free) | 16.4 weeks |
  | Everything outsourced (39 parts on live quotes, the rest estimates) | 0 | $31,358 | none (deliveries take 1-8 weeks, in parallel) |
  | **Recommended split** | **152 h** | **$25,667** | **7.6 weeks** |

  At $65/h, outsourcing everything costs about the same as making everything. The split is cheaper than both, and it
  halves the queue on the mill and lathe. If the parts are made by students in the ME Prototyping Lab, where the
  labour is free, making everything costs $11k. Outsourcing then buys time, not money.
- **The split:**
  - **Make (27 parts):**
    - the frame (from a bought, cut-to-size 5-1/2 in. blank with the core waterjetted), the floor plate, the lid, the door
      and the cover-slide drawer: they carry every seal face, and their rework has to stay on campus;
    - the build plate, heater block, piston head, gland plate and rod end, which will change during thermal testing,
      and the hollow piston rod (bought tube, cut, welded into the rod end and polished);
    - the optics bridge and its welded posts, which are too big for any instant service;
    - the 14 robot tooling items.
  - **Outsource (32 parts):** the brackets, arms, legs, flanges, handles and small housings to SendCutSend CNC, the sheet
    and guard panels to SendCutSend, and the 316L overflow block to JLCCNC (confirm 316L). At qty 1 each of these costs
    $4-435 outside, against about 3.5 h ($230+) of CAM, setups and inspection here.
  - **Buy instead (15 parts):** the stock viewport, the Thorlabs SM-series parts, the NEMA 23 bracket, catalogue
    pulls, ceramic washers and the striker disc, as [`machining.md`](machining.md) lever 1 already says.
  - **Hybrids (8 parts):**
    - the two base plates: buy the profile cut ($666-690 at SendCutSend), then drill and tap here;
    - the five 316L sheet weldments (plenums, chute, gas knife, hopper): buy them cut and bent, TIG them here, then
      machine the flange faces;
    - the M50 module body: turn and weld here, then send it out for boring and honing.
- **Honing has no instant quote and no published price.**
  - Engine shops charge $45-150 a bore (search snippets). For one 316L bore to H7 and Ra 0.4 µm, the estimate is
    $150-400 (research.csv), or $250-750 minimum per job (Edison r5).
  - Prototype honing shops found: Engis (Illinois); Lee's Grinding (Ohio, bores 1-63.5 mm, so not L75); Condor
    Engineering (Colorado). No Utah shop advertises small-bore precision honing.
  - The honed-tube alternative is CRC Distribution's 316 honed tube, 2.000 × 2.250 in. (SSHT-2000X2250): Ra 0.1-0.4 µm,
    call for price, ID tolerance not stated. It still needs honing after the flange is welded on, unless the weld
    leaves the bore alone. Section 3 has the details.
- **Read the instant prices as lower bounds for the hard parts.** SendCutSend's CNC prices come before its
  manufacturability review. Its automatic check passed the lid, whose drawer slot is still drawn enclosed and can't be
  cut, and the heater block, whose bayonet undercut is lathe work. None of the prices includes material certificates,
  passivation, inspection reports or vacuum cleaning; Edison r5 §1.3 lists these as the usual gaps.

## 1. The decision, part by part

"Here" is the in-house hours and cost at $65/h, with stock. "Outside" is the live quote × qty, or a labelled estimate.
"Plan" is the cost on the recommended route: a catalogue part plus 1 h to fit it for "buy instead", and quote plus the
in-house share for the hybrids.
The reason names the deciding factor: capability, tolerance and finish, lead time, cost or risk. The full row for every
part, including the basis of every number, is in [`should_cost.csv`](analysis/out/outsourcing/should_cost.csv).

| Part | Qty | Here: h / $ | Outside: $ | Basis of the outside price | Call | Plan: $ | Why |
|---|---:|---:|---:|---|---|---:|---|
| Module M50 bottom flange: gland plate | 1 | 5.7 / 412 | 794 | estimate (job shop $110/h) | make | 412 | capability + cost |
| Build plate M50 | 1 | 7.0 / 459 | 228 | SendCutSend CNC | make | 459 | tolerance and finish + risk |
| Heater block M50 | 1 | 5.5 / 362 | 207 | SendCutSend CNC | make | 362 | tolerance and finish + risk |
| Piston head M50 | 1 | 8.6 / 564 | 271 | SendCutSend CNC | make | 564 | risk |
| Hollow piston rod M50 | 1 | 3.5 / 231 | 466 | estimate (job shop $110/h) | make | 231 | capability |
| Rod end M50: end cap with a side boss for the h… | 1 | 5.3 / 352 | 707 | estimate (job shop $110/h) | make | 352 | capability |
| Chamber floor plate | 1 | 8.2 / 701 | 1,076 | SendCutSend CNC | make | 701 | tolerance and finish + cost |
| Chamber lid | 1 | 6.8 / 568 | 638 | SendCutSend CNC | make | 568 | tolerance and finish |
| Cover-slide drawer | 1 | 6.0 / 443 | 444 | SendCutSend CNC | make | 443 | tolerance and finish |
| Chamber door | 1 | 5.2 / 408 | 454 | SendCutSend CNC | make | 408 | tolerance and finish |
| Optics bridge posts | 4 | 11.6 / 1,084 | 1,861 | estimate (job shop $110/h) | make | 1,084 | capability |
| Process chamber body | 1 | 16.1 / 3,057 | 7,000 | estimate (Edison r5 range) | make (buy the cut blank) | 3,057 | capability + tolerance and finish |
| Optics bridge | 1 | 8.1 / 1,192 | 1,735 | estimate (job shop $110/h) | make (buy plate at 1 in.) | 1,192 | capability |
| Build module M50: spigot, flange, honed 316L cy… | 1 | 7.2 / 1,369 | 1,200 | estimate (Edison r5 range) | outsource (specialist) | 1,369 | capability |
| Base plate, process module | 1 | 8.8 / 1,194 | 745 | estimate (scaled SendCutSend quote) | outsource the profile, drill in house | 1,031 | capability + cost |
| Base plate, gas module | 1 | 7.5 / 1,064 | 666 | SendCutSend | outsource the profile, drill in house | 910 | capability + cost |
| Cross-flow inlet plenum + nozzle | 1 | 3.5 / 238 | 60 | estimate (from the sheet quotes) | outsource the cut-and-bent pieces, weld in house | 190 | capability |
| Cross-flow outlet plenum under the floor | 1 | 3.5 / 237 | 60 | estimate (from the sheet quotes) | outsource the cut-and-bent pieces, weld in house | 190 | capability |
| Gas knife | 1 | 3.5 / 228 | 60 | estimate (from the sheet quotes) | outsource the cut-and-bent pieces, weld in house | 190 | capability |
| Dose chute | 1 | 3.5 / 231 | 60 | estimate (from the sheet quotes) | outsource the cut-and-bent pieces, weld in house | 190 | capability |
| Reservoir M | 1 | 3.5 / 232 | 60 | estimate (from the sheet quotes) | outsource the cut-and-bent pieces, weld in house | 190 | capability |
| Rack side panels | 2 | 3.0 / 233 | 193 | estimate (from the sheet quotes) | outsource | 193 | capability + cost + lead time |
| Chamber legs | 4 | 6.4 / 480 | 397 | SendCutSend CNC | outsource | 397 | cost + lead time |
| Z mounting flange | 1 | 3.7 / 250 | 116 | SendCutSend CNC | outsource | 116 | cost + lead time |
| Z bracket + fold-back belt housing | 1 | 3.6 / 269 | 146 | SendCutSend CNC | outsource | 146 | cost + lead time |
| Z lift arm | 1 | 3.5 / 236 | 27 | SendCutSend | outsource | 27 | cost + lead time |
| Module M50 handle | 1 | 3.5 / 230 | 188 | SendCutSend CNC | outsource | 188 | cost + lead time |
| Radiation shields M50 | 2 | 3.0 / 195 | 50 | estimate (from the sheet quotes) | outsource | 50 | capability + cost + lead time |
| Overflow funnel block | 1 | 5.0 / 382 | 123 | JLCCNC | outsource | 123 | cost |
| Lift-out wall liners | 1 | 1.5 / 99 | 23 | OSH Cut | outsource | 23 | capability + cost + lead time |
| Lift-out wall liners | 1 | 1.5 / 99 | 25 | estimate (from the sheet quotes) | outsource | 25 | capability + cost + lead time |
| Lift-out wall liners | 1 | 1.5 / 99 | 25 | estimate (from the sheet quotes) | outsource | 25 | capability + cost + lead time |
| Recoater carriage block | 1 | 3.6 / 250 | 376 | SendCutSend CNC | outsource | 376 | cost + lead time |
| Recoater arm | 1 | 3.5 / 229 | 48 | SendCutSend CNC | outsource | 48 | cost + lead time |
| Blade holder | 1 | 3.6 / 244 | 103 | SendCutSend CNC | outsource | 103 | cost + lead time |
| Recoater feedthrough spacer ring | 1 | 4.2 / 277 | 14 | SendCutSend | outsource | 14 | cost + lead time |
| Recoater floating bearing housing | 1 | 5.4 / 358 | 156 | SendCutSend CNC | outsource | 156 | cost + lead time |
| Metering base | 1 | 5.8 / 403 | 435 | SendCutSend CNC | outsource | 435 | cost + lead time |
| Reservoir M shutter | 1 | 1.5 / 98 | 25 | estimate (from the sheet quotes) | outsource | 25 | capability + cost + lead time |
| Reservoir M lid with robot handle | 1 | 3.5 / 232 | 215 | SendCutSend CNC | outsource | 215 | cost + lead time |
| Camera viewport adapter + boss | 1 | 7.0 / 470 | 379 | SendCutSend CNC | outsource | 379 | capability |
| Galvo riser plate | 1 | 3.6 / 259 | 65 | SendCutSend | outsource | 65 | cost + lead time |
| Laser guard panels | 1 | 1.5 / 116 | 77 | SendCutSend | outsource | 77 | capability + cost + lead time |
| Laser guard panels | 1 | 1.5 / 115 | 72 | estimate (from the sheet quotes) | outsource | 72 | capability + cost + lead time |
| Laser guard panels | 2 | 3.0 / 220 | 93 | SendCutSend | outsource | 93 | capability + cost + lead time |
| Laser guard panels | 1 | 1.5 / 101 | 32 | estimate (from the sheet quotes) | outsource | 32 | capability + cost + lead time |
| Laser guard panels | 1 | 1.5 / 100 | 29 | estimate (from the sheet quotes) | outsource | 29 | capability + cost + lead time |
| Sliding guard door | 1 | 1.5 / 105 | 139 | SendCutSend | outsource | 139 | capability + cost + lead time |
| Operator panel box | 1 | 1.5 / 113 | 182 | SendCutSend | outsource | 182 | capability + cost + lead time |
| Door drive bracket | 1 | 3.5 / 229 | 169 | estimate (fit to SendCutSend CNC) | outsource | 169 | cost + lead time |
| Door drive shaft and disc | 1 | 3.5 / 228 | 169 | estimate (fit to SendCutSend CNC) | outsource | 169 | cost + lead time |
| Blade-cartridge grip fin | 1 | 3.5 / 228 | 169 | estimate (fit to SendCutSend CNC) | outsource | 169 | cost + lead time |
| AprilTag plates | 2 | 4.3 / 285 | 7 | SendCutSend | outsource | 7 | cost + lead time |
| Macor standoff rings M50 | 6 | 5.8 / 454 | 846 | estimate (job shop $110/h) | buy instead | 72 | cost + risk |
| Macor standoff rings M50 | 3 | 5.0 / 402 | 739 | estimate (job shop $110/h) | buy instead | 72 | cost + risk |
| Striker disc M50 | 1 | 4.6 / 301 | 609 | estimate (job shop $110/h) | buy instead | 75 | cost |
| Recoater motor standoff | 1 | 4.7 / 325 | 385 | SendCutSend CNC | buy instead | 0 | cost |
| Recoater motor bracket | 1 | 3.7 / 339 | 207 | SendCutSend CNC | buy instead | 95 | cost |
| Window flange | 1 | 5.8 / 400 | 395 | SendCutSend CNC | buy instead | 515 | cost + risk |
| Window retaining ring | 1 | 4.7 / 316 | 292 | SendCutSend CNC | buy instead | 0 | cost |
| Field-stop aperture | 1 | 4.5 / 295 | 156 | SendCutSend CNC | buy instead | 105 | cost |
| Camera window retaining ring | 1 | 4.5 / 295 | 257 | estimate (fit to SendCutSend CNC) | buy instead | 0 | cost |
| Door handle | 1 | 3.5 / 230 | 76 | SendCutSend CNC | buy instead | 74 | cost |
| Door handle | 2 | 3.8 / 253 | 203 | estimate (fit to SendCutSend CNC) | buy instead | 0 | cost |
| f-theta adapter ring | 1 | 4.7 / 329 | 388 | SendCutSend CNC | buy instead | 125 | cost |
| Enclosed beam tube | 1 | 3.5 / 233 | 264 | SendCutSend CNC | buy instead | 100 | cost |
| Guard-door handle for the robot | 1 | 3.6 / 238 | 130 | SendCutSend CNC | buy instead | 74 | cost |
| Guard-door handle for the robot | 2 | 4.0 / 266 | 213 | estimate (fit to SendCutSend CNC) | buy instead | 0 | cost |
| Robot assembly tooling, 14 items (assembly-tooling.csv C1-C9) | 14 | 19.0 / 2,305 | 3,139 | estimates; JLC3DP quote for the mandrel | make | 2,305 | cost + lead time |

How the outside price was estimated where no site gave one:

- **Fit to SendCutSend CNC:** the 26 quantity-1 CNC quotes against our hours. Unit price = −$141 + $88.5 per in-house
  hour; R² = 0.41, so ±50 % on any one part. Used for six small 6061 parts that weren't uploaded.
- **Job shop:** hours × $110/h (the midpoint of $75-150/h for 3-axis work: Fabcon 2026, Edison r5 table 4) × 1.2,
  plus stock. Used for 316L lathe parts, the optics bridge and the tooling.
- **Edison r5 planning ranges** (not quotes):
  - a turnkey frame, $4,000-10,000+, taken as $7,000;
  - a specialist-finished module cylinder, $600-1,800, taken as $1,200.
- **Sheet:** unquoted 5052 panels were scaled from SendCutSend's two 5052 0.063 in. prices ($22 + $142/m²). Small
  stainless parts were taken at OSH Cut's $22.85 liner price. The welded 316L parts were taken at $60 each, cut and
  bent only.

## 2. The quotes

All prices are for one machine, before shipping and tax unless the row says otherwise.

- **SendCutSend:** "arrives as soon as" is the delivered date it showed for its standard US shipping.
- **CNC rows:** the price before SendCutSend's review. Its CNC offers only 6061-T6.
- **Sheet rows:** the profile only. Grooves, counterbores and pockets are machined afterwards.
- **Thicknesses:** rounded to stock. 10 mm became 3/8 in., 12 mm became 1/2 in. and 4 mm became 3/16 in., which the model
  would need to follow.

| Service | Part (file) | As quoted | Qty | $ each | Lead time | UTC | Screenshot |
|---|---|---|---:|---:|---|---|---|
| SendCutSend | galvo riser plate 6061 10 mm | 6061-T6 .375 in. (model 10 mm) | 1 | 65.00 | arrives Sat Nov 28 | 05:31 | [scs_07.jpg](analysis/out/outsourcing/scs_07.jpg) |
| SendCutSend | galvo riser plate 6061 10 mm | 6061-T6 .500 in. (thickness check; model 10 mm) | 1 | 87.71 | arrives Sat Nov 28 | 05:32 | none (overwritten) |
| SendCutSend | galvo riser plate 6061 10 mm | 5052-H32 .187 in. (thickness check) | 1 | 30.04 | arrives Sat Nov 28 | 05:33 | none (overwritten) |
| SendCutSend | z lift arm 6061 12 mm pot magnet coupling | 6061-T6 .500 in. (model 12 mm) | 1 | 27.12 | arrives Sat Nov 28 | 05:34 | [scs_zlift.jpg](analysis/out/outsourcing/scs_zlift.jpg) |
| SendCutSend | sliding guard door aluminium | 5052-H32 .187 in. (model 4 mm) | 1 | 138.78 | arrives Sat Nov 28 | 05:35 | [scs_guarddoor.jpg](analysis/out/outsourcing/scs_guarddoor.jpg) |
| SendCutSend | laser guard panels 1 5 mm aluminium 3 | 5052-H32 .063 in. (model 1.5 mm) | 2 | 46.29 | arrives Sat Nov 28 | 05:35 | [scs_guardpanel3.jpg](analysis/out/outsourcing/scs_guardpanel3.jpg) |
| SendCutSend | base plate gas module mic 6 15 mm | 6061-T6 .625 in. (model 15 mm MIC-6; SendCutSend MIC-6 stops at .500 in.) | 1 | 689.66 | arrives Tue Dec 1 | 05:39 | [scs_baseplate_6061.jpg](analysis/out/outsourcing/scs_baseplate_6061.jpg) |
| SendCutSend | base plate gas module mic 6 15 mm | MIC-6 .500 in. (thinner than the model 15 mm) | 1 | 666.42 | arrives Tue Dec 1 | 05:40 | [scs_baseplate_mic6.jpg](analysis/out/outsourcing/scs_baseplate_mic6.jpg) |
| SendCutSend | apriltag plates 2 x tag36h11 56 mm on the g… | 6061-T6 .080 in. (model 2 mm) | 2 | 3.55 | arrives Fri Nov 27 | 05:41 | [scs_apriltag.jpg](analysis/out/outsourcing/scs_apriltag.jpg) |
| SendCutSend | recoater feedthrough spacer ring 6061 9 mm … | 6061-T6 .375 in. (model 9 mm; the face O-ring grooves are machined after) | 1 | 14.01 | arrives Fri Nov 27 | 05:42 | [scs_spacer.jpg](analysis/out/outsourcing/scs_spacer.jpg) |
| SendCutSend | laser guard panels 1 5 mm aluminium 1 | 5052-H32 .063 in. (model 1.5 mm) | 1 | 76.81 | arrives Sat Nov 28 | 05:43 | [scs_guardpanel1.jpg](analysis/out/outsourcing/scs_guardpanel1.jpg) |
| SendCutSend | operator panel box on the rack s front post | 6061-T6, CNC (SendCutSend routed this bent-box STEP to CNC) | 1 | 181.63 | arrives Tue Dec 1 | 05:44 | [scs_panelbox_cnc.jpg](analysis/out/outsourcing/scs_panelbox_cnc.jpg) |
| SendCutSend CNC | chamber lid 6061 t6 16 mm cover slide drawe… | 6061-T6, CNC (price before review) | 1 | 637.94 | arrives Wed Dec 2 | 05:46 | [scs_cnc_lid.jpg](analysis/out/outsourcing/scs_cnc_lid.jpg) |
| SendCutSend CNC | chamber floor plate 6061 t6 20 mm bolted un… | 6061-T6, CNC (price before review) | 1 | 1,075.62 | arrives Mon Dec 7 | 05:46 | [scs_cnc_floor.jpg](analysis/out/outsourcing/scs_cnc_floor.jpg) |
| SendCutSend CNC | chamber door 6061 t6 15 mm drops down half … | 6061-T6, CNC (price before review) | 1 | 454.14 | arrives Wed Dec 2 | 05:47 | [scs_cnc_door.jpg](analysis/out/outsourcing/scs_cnc_door.jpg) |
| SendCutSend CNC | window flange 6061 two fkm o ring grooves | 6061-T6, CNC (price before review) | 1 | 395.05 | arrives Mon Nov 30 | 05:47 | [scs_cnc_windowflange.jpg](analysis/out/outsourcing/scs_cnc_windowflange.jpg) |
| SendCutSend CNC | z mounting flange bolted under the floor | 6061-T6, CNC (price before review) | 1 | 115.83 | arrives Sat Nov 28 | 05:47 | [scs_cnc_zflange.jpg](analysis/out/outsourcing/scs_cnc_zflange.jpg) |
| SendCutSend CNC | blade holder 6061 18 x 31 quick swap | 6061-T6, CNC (price before review) | 1 | 102.55 | arrives Mon Nov 30 | 05:47 | [scs_cnc_bladeholder.jpg](analysis/out/outsourcing/scs_cnc_bladeholder.jpg) |
| SendCutSend CNC | recoater carriage block 6061 | 6061-T6, CNC (price before review) | 1 | 376.23 | arrives Mon Nov 30 | 05:48 | [scs_cnc_carriage.jpg](analysis/out/outsourcing/scs_cnc_carriage.jpg) |
| SendCutSend CNC | heater block m50 6061 t6 bayonet socket | 6061-T6, CNC (price before review) | 1 | 207.36 | arrives Sat Nov 28 | 05:49 | [scs_cnc_heaterblock.jpg](analysis/out/outsourcing/scs_cnc_heaterblock.jpg) |
| SendCutSend CNC | metering base 6061 fluted roller over a 100… | 6061-T6, CNC (price before review) | 1 | 434.80 | arrives Sat Nov 28 | 05:51 | [scs_cnc_meteringbase.jpg](analysis/out/outsourcing/scs_cnc_meteringbase.jpg) |
| SendCutSend CNC | recoater floating bearing housing blind cap… | 6061-T6, CNC (price before review) | 1 | 155.70 | arrives Mon Nov 30 | 05:55 | [scs_cnc_bearinghousing.jpg](analysis/out/outsourcing/scs_cnc_bearinghousing.jpg) |
| SendCutSend CNC | piston head m50 6061 t6 cool side of the br… | 6061-T6, CNC (price before review) | 1 | 270.76 | arrives Mon Nov 30 | 05:55 | [scs_cnc_pistonhead.jpg](analysis/out/outsourcing/scs_cnc_pistonhead.jpg) |
| SendCutSend CNC | cover slide drawer 6061 robot pull tab half… | 6061-T6, CNC (price before review) | 1 | 444.45 | arrives Wed Dec 2 | 05:56 | [scs_cnc_drawer.jpg](analysis/out/outsourcing/scs_cnc_drawer.jpg) |
| SendCutSend CNC | build plate m50 50 5 x 10 6061 t6 bayonet s… | 6061-T6, CNC (price before review) | 1 | 227.94 | arrives Mon Nov 30 | 05:56 | [scs_cnc_buildplate.jpg](analysis/out/outsourcing/scs_cnc_buildplate.jpg) |
| SendCutSend CNC | camera viewport adapter boss 6061 1 in wind… | 6061-T6, CNC (price before review) | 1 | 379.48 | arrives Mon Nov 30 | 05:56 | [scs_cnc_cameraadapter.jpg](analysis/out/outsourcing/scs_cnc_cameraadapter.jpg) |
| SendCutSend CNC | recoater motor bracket | 6061-T6, CNC (price before review) | 1 | 206.98 | arrives Sat Nov 28 | 05:57 | [scs_cnc_motorbracket.jpg](analysis/out/outsourcing/scs_cnc_motorbracket.jpg) |
| SendCutSend CNC | f theta adapter ring 6061 m85x1 internal th… | 6061-T6, CNC (price before review) | 1 | 388.47 | arrives Sat Nov 28 | 06:03 | [scs_cnc_fthetaring.jpg](analysis/out/outsourcing/scs_cnc_fthetaring.jpg) |
| SendCutSend CNC | window retaining ring spigot bottoms metal … | 6061-T6, CNC (price before review) | 1 | 291.67 | arrives Sat Nov 28 | 06:03 | [scs_cnc_windowring.jpg](analysis/out/outsourcing/scs_cnc_windowring.jpg) |
| SendCutSend CNC | recoater motor standoff | 6061-T6, CNC (price before review) | 1 | 385.34 | arrives Sat Nov 28 | 06:03 | [scs_cnc_motorstandoff.jpg](analysis/out/outsourcing/scs_cnc_motorstandoff.jpg) |
| SendCutSend CNC | field stop aperture 36 passive beam limit | 6061-T6, CNC (price before review) | 1 | 156.14 | arrives Sat Nov 28 | 06:03 | [scs_cnc_fieldstop.jpg](analysis/out/outsourcing/scs_cnc_fieldstop.jpg) |
| SendCutSend CNC | door handle 1 | 6061-T6, CNC (price before review) | 1 | 76.21 | arrives Sat Nov 28 | 06:04 | [scs_cnc_doorhandle.jpg](analysis/out/outsourcing/scs_cnc_doorhandle.jpg) |
| SendCutSend CNC | guard door handle for the robot 12 x 130 ba… | 6061-T6, CNC (price before review) | 1 | 130.42 | arrives Sat Nov 28 | 06:04 | [scs_cnc_guardhandle.jpg](analysis/out/outsourcing/scs_cnc_guardhandle.jpg) |
| SendCutSend CNC | reservoir m lid with robot handle grip plan… | 6061-T6, CNC (price before review) | 1 | 214.78 | arrives Mon Nov 30 | 06:04 | [scs_cnc_reservoirlid.jpg](analysis/out/outsourcing/scs_cnc_reservoirlid.jpg) |
| SendCutSend CNC | module m50 handle 6061 screwed under the gl… | 6061-T6, CNC (price before review) | 1 | 188.40 | arrives Mon Nov 30 | 06:04 | [scs_cnc_modulehandle.jpg](analysis/out/outsourcing/scs_cnc_modulehandle.jpg) |
| SendCutSend CNC | recoater arm 6061 40 x 14 web | 6061-T6, CNC (price before review) | 1 | 47.55 | arrives Mon Nov 30 | 06:04 | [scs_cnc_recoaterarm.jpg](analysis/out/outsourcing/scs_cnc_recoaterarm.jpg) |
| SendCutSend CNC | enclosed beam tube | 6061-T6, CNC (price before review) | 1 | 264.44 | arrives Sat Nov 28 | 06:05 | [scs_cnc_beamtube.jpg](analysis/out/outsourcing/scs_cnc_beamtube.jpg) |
| SendCutSend CNC | z bracket fold back belt housing 2 1 | 6061-T6, CNC (price before review) | 1 | 146.29 | arrives Sat Nov 28 | 06:05 | [scs_cnc_zbracket.jpg](analysis/out/outsourcing/scs_cnc_zbracket.jpg) |
| SendCutSend CNC | chamber legs 6061 30 x 30 | 6061-T6, CNC (price before review) | 4 | 99.27 | arrives Mon Nov 30 | 06:06 | [scs_cnc_legs_q4.jpg](analysis/out/outsourcing/scs_cnc_legs_q4.jpg) |
| OSH Cut | lift out wall liners 0 5 mm 316l back sides… | 316 stainless #2B, 0.036 in. (20 ga; thinnest 316 offered; model 0.5 mm), deburred | 1 | 22.85 | not shown before sign-in | 06:08 | [osh_liner.jpg](analysis/out/outsourcing/osh_liner.jpg) |
| JLCCNC | overflow funnel block 316l bolted fkm face … | default spec: 6061 aluminium, bead blast + natural anodize, ISO 2768-m (the part is 316L; for scale only) | 1 | 32.98 | standard 6 days build + UPS Express Saver DDP 2-4 business days ($25.99) | 06:14 | [jlccnc_02.jpg](analysis/out/outsourcing/jlccnc_02.jpg) |
| JLCCNC | overflow funnel block 316l bolted fkm face … | SUS304 (the only stainless grade in the instant quote; the design is 316L), no finish, +/-0.05 mm, threads yes | 1 | 123.46 | build time for this spec not shown (the dialog's Save did not apply the spec); shipping as above | 06:16 | [jlccnc_overflow_304.jpg](analysis/out/outsourcing/jlccnc_overflow_304.jpg) |
| JLC3DP | tooling spigot mandrel | default: 9600 resin (SLA), white, general sanding | 1 | 26.20 | standard build 3 days + Global Standard Direct Line 8-10 business days ($17.10) or UPS Express Saver DDP 2-4 business days ($22.97) | 06:21 | [jlc3dp_mandrel.jpg](analysis/out/outsourcing/jlc3dp_mandrel.jpg) |

What the screenshots show and what to check:

- **Quantity breaks are steep for CNC.**
  - CNC: at 2 pieces each costs 58 % of a single one, and at 10 pieces 23 %.
  - Sheet: the median is 72 % at 2 and 59 % at 10.
  - So the same CNC part for two machines costs about 15 % more in total than for one.
- **The CNC quotes don't scale with what is hard here.** The frame's floor plate is the dearest at $1,075.62 (Dec 7).
  The heater block, whose undercut no 3-axis tool reaches, is $207.36.
- **Four quotes are for a different thickness** from the model: the galvo riser, the Z lift arm, the guard door and the
  gas-module base plate. Change the model to stock sizes, or face the parts down here.
- **Two prices are thickness checks, not plans:** the galvo riser at 1/2 in. and in 3/16 in. 5052. The run that opened
  them was meant for another part. Their screenshots were overwritten, so the CSV marks them.

## 3. What couldn't be instant-quoted, and the alternatives

| Item | What was found | Source (UTC fetch time in research.csv) | Use in the plan |
|---|---|---|---|
| Honing the Ø25.4 / 50.8 / 76.2 H7 bores | No price list from any honing shop. Engine shops $45-75 (bore + hone, motorcycle) and about $100-150 a bore; Edison r5 gives $100-225/h commercial, $250-750 minimum per job | [xrsonly.com/services](https://www.xrsonly.com/services), [thepricer.org](https://www.thepricer.org/motorcycle-engine-rebuild-cost/) (search snippets); Edison r5 table 4 | $400 per bore in the should-cost; ask Engis, Lee's Grinding or Condor for a real quote |
| Honed tube instead of honing | CRC Distribution SSHT-2000X2250, 316 honed tube 2.000 × 2.250 in., call for price, Ra 4-16 µin (0.1-0.4 µm), ID tolerance not published. Typical honed tube is H8/H9; H7 at 50.8 mm (+0.030) needs "+0.001/−0 in." on the order, and that is still too loose for the 25.4 mm bore (+0.021). Carbon-steel honed tube is $3.40/in. (CRC HT-2375X2000), but it isn't stainless. No stock 316 honed tube at 1.000 or 3.000 in. ID was found | [crconline.com SSHT-2000X2250](https://crconline.com/itemdetail/SSHT-2000X2250), [HT-2375X2000](https://www.crconline.com/itemdetail/HT-2375X2000) | Worth a quote for M50, but welding the flange on can still pull the bore in (machining.md), so plan a hone after welding anyway or move the weld away from the bore |
| Roller burnishing here | ID roller burnishing tools for 1.375-2.25 in. bores, $148-476 retail; 2-16 µin claimed after fine boring | [elliott-tool.com](https://www.elliott-tool.com/metal-finishing/burnishing-tools/id-od-carbide-burnishing/) (search snippets) | Fixes finish, not size or roundness; only if the boring holds H7 |
| TIG welding of the 316L module and sheet | No Utah shop publishes a rate; IBISWorld $95/h national; consumer guides $75-125/h; Edison r5 $90-175/h commercial | research.csv items 2 | Keep on campus (140 CTB weld lab, PF shop); 3 h at $65/h in the module's cost |
| Passivation, electropolishing (316L) | No price lists (Able, Harrison, Delstar). Able electropolishes one sample part free; Pioneer (Salt Lake City) lists passivation; Edison r5: $150-400 minimum lot | [d2pmagazine.com](https://d2pmagazine.com/?p=22202); research.csv item 3 | $150 lot in the module's cost; batch every 316L part into one lot |
| Anodizing (6061) | Vegas Metal Finishing: $100-150 per rack of 1-4 parts, Type II clear or black or Type III; Pioneer (Salt Lake City) has a 156 in. tank that takes the frame (no price) | [Vegas Metal Finishing order form](https://form.jotform.com/240280944652053) | Not in the plan: the chamber stays bare inside (build-sequence.md). If outside parts are anodized, one batch is $100-150 |
| Macor | Macor rod 0.5 × 12 in. $147.99, 0.25 in. $71.35 (Zoro); McMaster 8489K89's price didn't load; no Macor machining price list | [zoro.com](https://www.zoro.com/professional-plastics-macor-12-l-025-w-rmacor250/i/G500930934/) (search text) | Buy stock ceramic washers instead (machining.md lever 1) |
| The frame blank | Speedy Metals 5-1/2 in. 6061-T651: 12 × 12 in. $1,447.06, 12 × 18 in. $1,860.51, freight extra; OnlineMetals through Zoro $2,810.99 + $160 delivery. Metals Depot's pages stop at 1-3/4 in. | [speedymetals.com](https://speedymetals.com/p-2430-5-12-6061-t651-aluminum-plate.aspx) | $1,860.51 + ~$150 waterjet in the frame's cost; the 15 × 9.5 in. blank fits the 12 × 18 piece turned |
| A standard chamber instead of the frame | Ideal Vacuum 6061 cubes: 9 × 9 × 9 in. kit $2,584.79; 6 × 12 × 12 in. short cube $2,124-6,348; 16 in. welded cube $4,710-7,129 (search text). Terra Universal benchtop chambers $2,726-7,324. Lesker, MDC and Nor-Cal publish no box-chamber prices. Edison r5: a bespoke rectangular box from these vendors is $5,000-15,000+ | [idealvac.com](https://www.idealvac.com/en-us/vacuum-products/pl/141-1340), [terrauniversal.com](https://www.terrauniversal.com/product_pdf/Terra_5235-31.pdf); Edison r5 §3 | None has the 280 × 190 opening, the door, the recoater bores and the ports, so it would be machined anyway. Keep the frame |
| BYU's own rates | Prototype Manufacturing Lab labour $65/h academic, $85/h non-academic, $95/h off campus (pml.byu.edu/labor, search text only); the ME Prototyping Lab is free to students | research.csv item 7 | $65/h is the base rate; $95/h and $0/h are the sensitivities |
| Other shops' rates | Other universities: $59-100/h internal, $88-135/h external (Clemson, ASU, Iowa, Boise State: $100/h + $30 per machine-hour). Commercial 3-axis $75-150/h, 5-axis $100-250/h (Fabcon); wire EDM $65-180/h; waterjet $100-180/h (The Fabricator) | research.csv items 7 and 8 | $110/h job-shop rate for unquoted parts |

**Utah shops.** Hydraulic-cylinder honing only as part of a repair (Wheeler Machinery, Salt Lake City). Precision
grinding with honing not confirmed (Superior Grinding, South Salt Lake). Passivation and anodizing (Pioneer, Salt Lake
City). Vacuum chambers, certified welders and helium leak testing (LACO Technologies, Salt Lake City; from
machining.md). None publishes prices.

## 4. Lead time and the schedule

- **Outsourced parts arrive in 1-2 weeks.**
  - SendCutSend's delivered dates were 5-6 days out for sheet and plate and 6-15 days for CNC.
  - JLCCNC is 3, 6 or 11 days to build ($51.86 / $32.98 / $29.88 for the overflow block in 6061), plus 2-4 days by UPS
    ($25.99, duties paid).
  - JLC3DP is 3 days plus 2-10 days of shipping.
  - None of these is on the critical path if they are ordered in the first week.
- **The in-house queue drops from 329 h to 152 h.** At 20 shop hours a week (an assumption: one person half-time on
  the VF-4 and the lathe), that is 7.6 weeks instead of 16.4. The remaining queue is mostly the seal parts and the
  module, which are the parts worth the time.
- **The module's honing loop is the new long pole.** It runs: turn, weld, bore, ship out, hone, ship back. No honing
  shop published a lead time; plan 3-6 weeks, an estimate. Start the M50 body first.
- **The laser still sets the overall date** if it is bought new from IPG (10-12 weeks; cost-scenarios.md).

## 5. Not done, and caveats

- **No shop was contacted**, so honing, welding and finishing have no quote. Ask for these first: honing (Engis, Lee's
  Grinding, Condor), a 316 honed tube price (CRC), and BYU's PF Manufacturing Shop rate and queue.
- **SendCutSend's CNC prices are pre-review.** Its automatic check passed parts with undercuts and an enclosed slot
  (the lid, the heater block, the build plate). The real price or a rejection comes after its review.
- **The dovetail, internal-groove and compound-angle parts** were priced as plain 3-axis parts. No tolerance or
  finish could be set on SendCutSend. JLCCNC's ±0.05 mm option added 24 %, and its threads option another 25 %.
- **No certificates, inspection, passivation or vacuum cleaning** are in any instant price (Edison r5 §1.3). Put Ra,
  flatness, thread depth and insert type on a drawing before ordering a sealing part from anyone.
- **The hours model** (hours.py) carries its own caveats: CAM hours are an estimate, with no published rule. Its fixed
  ~3.5 h per part for CAM, setups and inspection is what makes the small parts cheaper outside.
- **Edison r5 is out of date on SendCutSend:** it calls it sheet-only, but SendCutSend now quotes CNC billet work. Its
  per-platform ranges are planning numbers, not quotes. Where this run has a live price, the live price is used.
- **Catalogue prices for the buy-instead parts are estimates** ($8.64-450, not fetched this run), except McMaster's
  pull.
- **The robot tooling's in-house costs** are assembly-tooling.csv's own estimates.

## 6. How to re-run

```bash
git worktree add --detach /tmp/snap-out HEAD                          # a frozen copy of cad/
/tmp/capmem 2 /tmp/venv/bin/python desktop-lpbf/analysis/outsourcing/export_parts.py \
    --cad /tmp/snap-out/desktop-lpbf/cad --out /tmp/outsourcing/parts  # 82 STEP + 17 DXF, parts.csv, manifest.csv (~1 min)
/tmp/venv/bin/python desktop-lpbf/analysis/outsourcing/should_cost.py  # reads parts.csv, hours.csv, dfm.json, the quotes
```

- **Re-quoting.**
  - SendCutSend (app.sendcutsend.com) takes 10 files per drop and asks "sign up or continue as guest" after the
    first batch. Continue as guest needs no details.
  - A DXF without units may load as inches. Switch it to mm on the card before configuring.
  - STEP files get a "Production Method" step: pick CNC Machining for billet parts.
  - JLCCNC (jlccnc.com/cnc-machining-quote) priced the first upload as a guest; later uploads did not register.
- **The exported part files are not committed** (6.9 MB): rebuild them with the export script.
  [`manifest.csv`](analysis/out/outsourcing/manifest.csv) lists all 99 files with sha256. Re-exported STEP files carry
  a new timestamp in their header, so their hashes will differ from the ones uploaded.
- **Rates and assumptions** are constants at the top of `should_cost.py`: `RATE`, `JOBSHOP_RATE`,
  `SHOP_HOURS_PER_WEEK`, the stock prices per kg, `HONE_USD` and `PASSIVATE_USD`.
