# Lead times, running cost and time estimates for the robot-built video (2026-11-25)

For [issue #260](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/260) and PR 266, round 7. Sterling asked
on 2026-11-25 for three things in the video. He wanted the running cost by category, with the expensive items called out
one by one, and a running total of used against new. He wanted the anticipated lead times, especially the long ones, and
how short they get if we buy used. And he wanted time estimates for machining and assembly.

The numbers are in [`hud.json`](hud.json) (for the video's panels), [`costs-leadtimes.csv`](costs-leadtimes.csv) and
[`times.csv`](times.csv). [`build_hud.py`](../analysis/robotbuild_data/build_hud.py) rebuilds all three from files in
the repo.

How the numbers were read:
- **New parts:** lead times were read on 2026-11-25 between 05:30 and 05:50 UTC. They are the 128 rows of
  [`leadtime-lookups.csv`](../analysis/robotbuild_data/leadtime-lookups.csv), each with its URL and fetch time.
- **Used parts:** the used picks of [`cost/used-options.csv`](../cost/used-options.csv) (read on 2026-11-20) were
  re-read between 06:05 and 06:16 UTC: price, eBay's delivery window to Provo (84602) and returns
  ([`ebay-recheck.csv`](../analysis/robotbuild_data/ebay-recheck.csv)).
- **Pages that block datacenter IPs or render only with JavaScript** were read through the lab Pi (BYU network): eBay,
  Thorlabs, Marshall Scientific, CDW and BYU's purchasing pages.
- **Nothing was bought.** No account was used, no form was filled and no vendor or seller was contacted.

## Short answer

- **Bought new, the laser sets the schedule: 12–15 weeks until it arrives.** That is IPG's 10–12 weeks after the order
  ([quote of 2026-11-18](../quotes/ipg-ylr-500-u3-sm-ac.md)), plus BYU's purchase order and freight. BYU's Capstone
  office says "Allow ten days to two weeks PLUS shipping time for a large order to be placed through University
  Purchasing" (purchases over $3,500 need a PO; [capstone.byu.edu](https://capstone.byu.edu/purchase-orders), read
  2026-11-25). With the parts split between BYU's shop and outside vendors as
  [`outsourcing.md`](../outsourcing.md) recommends, fabrication takes 9–10.5 weeks. So the machine is assembled at
  about **13–16 weeks**.
- **As chosen in `bom.csv`, two cheap switches would set the schedule first.**
  - The IDEC HS6B-12B05 guard-position switch in S2 ($123) is "not kept in stock" at Digi-Key, with a 27-week
    manufacturer lead time.
  - The Omron K8DT-TH1CD in H2 ($240) is out of stock until 03-Mar-2027, with a 19-week lead time.

  Bought as chosen, the parts take **29–30 weeks**. Swap both for stocked parts before ordering:
  [`modules.md`](../modules.md) already names the 67F bimetal thermostat ($8.33) in place of the K8DT. The weeks below
  assume these two swaps.
- **Bought used, the purchases take 1–4 weeks, and fabrication sets the schedule.**
  - The used IPG (still listed on 2026-11-25) ships by freight from El Paso: about a week.
  - eBay gives delivery windows to Provo of 3–7 days for its scan head and lens, 3–6 days for the scan card, and 5–10
    days for the pump and the O₂ and dew-point sensors.
  - Nothing left on the used route waits more than about 4 weeks. The longest is the THK Z actuator, at 2 days to 3
    weeks.

  The machine is then assembled at about **10–11.5 weeks**, so **buying used saves about 2.5–4.5 weeks**. If every part
  is machined at BYU instead (16.4 weeks of queue at 20 shop hours a week, `outsourcing.md`), fabrication sets both
  routes at 19–20 weeks. Then used saves no time, only money.
- **Money, at the design's spec: $115.6k all new against $70.3k–75.6k with the used majors.** That saves $40.0k–45.3k,
  almost all of it on the laser, scan head and scan card: the CW optics chain is $44.4k new and $6.0k–11.2k used. Over
  the BOM's full ranges, new is $76.3k–161.2k and used $68.2k–117.5k.
- **Running total in the order of the table tour** (at spec, new / used):

  | # | Category | This category, new / used | Running, new / used |
  |---:|---|---:|---:|
  | 1 | Stock to machine | $4.4k / $4.4k | $4.4k / $4.4k |
  | 2 | Sheet | $1.0k / $1.0k | $5.5k / $5.5k |
  | 3 | Motion | $5.0k / $4.9k | $10.4k / $10.4k |
  | 4 | Vacuum and gas | $13.5k / $8.4k | $24.0k / $18.8k |
  | 5 | Laser and optics | $42.7k / $8.9k–14.1k | $66.7k / $27.7k–32.9k |
  | 6 | Electronics, heaters and sensors | $27.9k / $22.6k | $94.5k / $50.3k–55.5k |
  | 7 | Seals and fasteners | $0.7k / $0.7k | $95.2k / $50.9k–56.2k |
  | 8 | Frames | $0.7k / $0.7k | $95.9k / $51.6k–56.9k |
  | 9 | Bought, not on the table (glovebox, dust vacuum, extinguisher, power meter, ...) | $10.5k / $9.5k | $106.4k / $61.1k–66.3k |
  | 10 | Services (machining; module welding, boring, honing) | $9.2k / $9.2k | $115.6k / $70.3k–75.6k |

- **Machining: 287.3 h with a 4th axis (302.3 h on a 3-axis) for 57 parts.** That is CAM 132.1 h, setups 98.6 h (113.6
  h on a 3-axis), cutting 33.2 h, and deburring and inspection 23.2 h
  ([`hours.json`](../analysis/out/machining/hours.json); its CAM hours are an estimate, with no published rule). The
  chamber frame and floor plate alone are 25.4 h.
- **Assembly: 139 checked steps.**
  - **Arms:** about 3.3 h, plus 0.8 h of MiR trips to the long table.
  - **People:** about 13 person-hours, half of it the laser guard and the integration on the tray.
  - **Steps the arms can't do:** 27 steps fail or partly fail for the arms (26 on reach or collisions, 1 on force:
    the dowel press), and 19 are steps for a person or the shop.

  All of these times are estimates: `results.json`'s "seconds" is the checker's compute time, not how long a step takes
  (§5).

## 1. What sets the schedule

| Route | All bought parts at BYU | Set by | Next longest | Assembled, outsourcing split | Assembled, all made at BYU |
|---|---|---|---|---|---|
| New, as chosen in `bom.csv` | 28.7–29.7 wk | S2: IDEC HS6B-12B05, 27 wk + PO | H2 K8DT 15.7–21.7 wk; laser 11.9–15.0 wk | 29.7–30.7 wk | 29.7–30.7 wk |
| New, with S2 and H2 swapped for stocked parts | 11.9–15.0 wk | L1: the IPG laser (and its collimator) | G6 O₂ analyzer 6.3–8.7 wk; L6 lens 4.7–6.7 wk; D2 UPS 3.1–4.6 wk | 12.9–16.0 wk | 19.1–20.3 wk |
| Used majors, with the same swaps | 0.6–4.0 wk | M3: THK KR26 Z actuator, 2 d to 3 wk | the McMaster and Digi-Key POs, 1.7–3.4 wk | **10.3–11.5 wk** (fabrication sets it) | 19.1–20.3 wk (fabrication) |

How the weeks are built ([`leadtimes.py`](../analysis/robotbuild_data/leadtimes.py)):
- **Days to BYU** = the vendor's stated ship time, plus transit, plus BYU's PO step when that vendor's order is $3,500
  or more. Transit is 2–5 days by ground and 3–7 days by LTL freight (estimates); eBay's own delivery window is used
  where the listing gives one. The PO step is 10–14 days.
- **Who needs a PO.** New: IPG, SCANLAB, Marshall Scientific, MROSupply, Thorlabs, Digi-Key, McMaster and the
  services. Used: only McMaster, Digi-Key, MROSupply and the services stay over $3,500. The eBay buys go on a PCard:
  BYU Financial Services says "Use a PCard (Procurement Card) for non-catalog goods and services under $3,500"
  ([finserve.byu.edu](https://finserve.byu.edu/paying-for-goods-and-services), read 2026-11-25). The used laser with
  freight is about $2.5k. Whether a PCard may buy on eBay was not checked.
- **Fabrication** starts when the McMaster stock arrives (12–20 days, including its PO). Then comes `outsourcing.md`'s
  in-house queue: 7.6 weeks for the 152 h of its recommended split, or 16.4 weeks for all 329 h, at 20 shop hours a week
  (its assumption: one person half-time). Outsourced parts arrive in 1–2 weeks in parallel: SendCutSend states 2–4
  production days for sheet and 2–5 for CNC, and its quotes of 2026-11-22 gave delivery 5–15 days out. The build
  module's honing loop (turn, weld, bore, ship out, hone, ship back) is 3–6 weeks (estimate), so start it first.
- **Assembly and the leak check** add about a week (estimate).
- **Lines with no published lead time** are left out of the maximum (see "Still open"). They are the risks that could
  move the date.

## 2. The long-lead items, and how short they get used

| Line | Item | New, as the vendor states it (read 2026-11-25) | New, days to BYU | Used or faster route (re-read 2026-11-25) | Days |
|---|---|---|---|---|---|
| L1 | IPG YLR-500-U3-SM-AC laser, ~$23k | "10–12 weeks ARO"; "unlikely to deliver much faster" (IPG quote, 2026-11-18) | 83–105 (PO + freight) | eBay, US surplus dealer: YLR-400-SM-EOS (M6860), $2,099.99 or Best Offer, + ~$400 freight (estimate); "Unit in mint condition"; "30 days returns. Seller pays for return shipping"; freight from El Paso, delivery "Varies" | 3–8 (estimate) |
| S2 | IDEC HS6B-12B05 guard-position switch, $123.45 | Digi-Key: "not kept in stock"; 27-week manufacturer lead time | 201–208 | a stocked guard-position switch (not chosen yet); Digi-Key's HS5L guard lock has 3 in stock, then 16 weeks | 12–22 (PO) |
| H2 | Omron K8DT-TH1CD door-channel relay, $240.25 | Digi-Key: 0 in stock, "1 expected in stock on 03-Mar-2027", 19-week lead | 110–152 | the 67F bimetal thermostat ($8.33, `modules.md`) or SOLO SL4848-RR-D ($143); stock not checked | 12–22 (PO) |
| G6 | Ntron Microx O₂ analyzer, $2,091 | Instrumart: "Usually ships in 6-8 weeks" | 44–61 | eBay, US: Alpha Omega Series 3000, $650 + ~$350 cell (estimate), "Estimated between Mon Nov 30 and Thu Dec 3"; or Teledyne 3190, $779, 60-day returns, Nov 30–Dec 5 | 5–8 |
| L6 | Thorlabs FTH160-1064 lens + windows, $1,255.84 | "Available: In Stock Overseas"; "Transfers between locations typically take 3-4 weeks" | 33–47 (PO) | eBay, US: LINOS f = 254 mm, now $539.99 (the $99.99 one ended on Nov 23), Nov 28–Dec 2, 30-day returns. A marking lens, not the drawn f = 160 mm | 3–7 |
| D2 | Eaton 5PX1500RTG2 UPS, $1,137.99 | CDW: "Item Backordered"; Digi-Key: 0 in stock, one expected 15-Dec-2026 | 22–32 | eBay, US refurbisher: APC SMX1500RM2U, $449.99, Nov 28–Dec 2, no returns | 3–7 |
| G9 | Vaisala DMT143 dew point, $2,281.70 | Selectum: "2 Weeks Factory Lead Time"; made to order, non-returnable | 16–19 | eBay, US: Atlas Copco open box, $150 + $15.99, Nov 30–Dec 3 | 5–8 |
| L5, C1 | SCANLAB basiCube 20 ($12,000) and RTC6 ($6,065): both placeholders | quote only; no lead time published, and no reseller lists a new one | unknown | used, US: hurrySCAN 25, $1,200 (dealer, 30-day warranty; it also lists a hurrySCAN 25 with a Sill f = 163 mm lens at $1,500). Or an open-box intelliSCAN III 20 on eBay, $1,500, Nov 28–Dec 2. RTC5 PCIe on eBay, $1,499.99, "delivery in 2–4 days", 30-day returns | 3–8 / 3–6 |
| L5 alt | Thorlabs QS20XY-Y1 galvo, $5,893.56 | "Available: Today" | 12–20 (PO) | the in-stock new alternative if SCANLAB is slow | |
| A1 | Omron E3NX-FA41 fibre amplifier, $353.03 | Digi-Key: 5 in stock, then "Manufacturer Standard Lead Time 33 Weeks" | 12–20 (PO) | order now while the stock lasts | |
| S1 | Banner XS26-2 safety controller, $1,093.01 | Digi-Key: 1 in stock, then 4 weeks | 12–20 (PO) | buy new (safety part) | |
| B3 | SCHUNK NSE-HT mini 88-20, 2 × $2,680 | MROSupply: "typically shipped within 1 day" (search snippet; its site was down for maintenance on 2026-11-25); the SPC-HT pins have no distributor listing | unknown | not searched used | |
| G2 | Edwards nXDS6i, $5,977.85 | Marshall Scientific: "Typically ships within Same Business Day", brand new | 12–20 (PO) | eBay, US: Agilent IDP-3, $1,149.99 + $134.59, Nov 30–Dec 5, "Seller does not accept returns" | 5–10 |
| T1 | Gentec-EO UP55M-500W head + U-LINK, $2,785 | prices listed; "CONTACT SALES" for anything else | unknown | eBay: Ophir L1500W head from China ($454 + $45, Dec 3–15, no returns) + Nova II meter (US, $1,279.99) | 8–20 |
| M3 | THK KR26 Z actuator, $883 | Oriental Motor: "Contact your local sales office"; THK Quick Ship: "2 days to 2 weeks depending on current stock levels"; MISUMI: "23 Day(s) or more" | 4–28 | not searched used | |

Already in stock and shipping within days (new):
- AutomationDirect: all seven Productivity1000 parts, 11–355 of each; in-stock orders before 6 p.m. ET ship the same
  day.
- Teknic: ClearPath and ClearCore "ship within 3 business days" for up to 5 pieces.
- Digi-Key: the HARTING dock (233 and 158 in stock), the Banner expansion modules (38 and 7) and the CN708 (6 in stock,
  then 12 weeks).
- Thorlabs: the DMSP1000, NF1064-44, LW1P1/M and LG1 show "Available: Today".
- Edmund: the 38-990 window (5 in stock) and 57-983 target (20+) on its UK and Canadian sites.
- Dynabrade 61470 (the cheaper dust vacuum): "Est. Lead Time: 6 days" at TA Industrial.
- McMaster: "98% of items ship from stock, and most orders arrive same or next day". Its product pages render only by
  script, so no single part's stock was read.

**The 2026-11-25 reads only move the critical path through the two switches.** Every other new part known to be slow
(the O₂ analyzer at 6–8 weeks, the lens at 3–4 weeks, the UPS backorder) still arrives before the laser. None of them
waits longer than fabrication on the used route.

## 3. Cost by category

"At spec" follows `cost_scenarios.py`'s at-spec rule. The CW optics chain (L1, L3, L5, L6, C1) is at its BOM high end,
and every other line at its cheapest listed option. "Used" takes the used picks still listed on 2026-11-25 and new
parts elsewhere. Each BOM line goes in the category where render_build's `kit_cat()` puts its parts on the table. Three
lines are split by component (B1, S9, A2), and two pseudo-categories hold what the table doesn't show.

| Category | Lines | New at spec | Used | BOM range, new | BOM range, used | Cheaper same-spec, new |
|---|---|---:|---:|---:|---:|---:|
| Stock to machine | G1 F4 F5 B1 (stock) | 4,424 | 4,424 | 4,424–5,131 | 4,424–5,131 | 4,424–5,131 |
| Sheet | S9 (sheet) R1 A2 (liners) | 1,038 | 1,038 | 1,038–1,858 | 1,038–1,858 | 769–1,589 |
| Motion | M1–M5 A3 | 4,969 | 4,901 | 4,969–7,860 | 4,901–7,764 | 4,827–7,718 |
| Vacuum and gas | G2–G7 G9 B4 | 13,543 | 8,440 | 13,543–18,731 | 8,440–11,498 | 11,790–16,977 |
| Laser and optics | L1–L7 S5 T2 A2 (slides) | 42,703 | 8,853–14,079 | 9,388–48,018 | 8,116–19,394 | 9,388–47,995 |
| Electronics, heaters, sensors | C1–C6 M6 S1–S4 H1–H3 B3 A1 D1 D2 E1–E4 | 27,855 | 22,622 | 21,915–37,141 | 21,227–30,404 | 21,117–36,343 |
| Seals and fasteners | G8 B2 FX | 661 | 661 | 661–928 | 661–928 | 576–843 |
| Frames | S9 (frame) F3 | 689 | 689 | 689–1,339 | 689–1,339 | 689–1,339 |
| Bought, not on the table | P1 S6 S7 S8 T1 T3 E5 A2 (vacuum) | 10,497 | 9,491 | 10,497–15,372 | 9,491–14,366 | 9,957–12,799 |
| Services | X1, B1 (welding, boring, honing) | 9,215 | 9,215 | 9,215–24,777 | 9,215–24,777 | 9,215–24,777 |
| **Total** | 64 lines | **115,594** | **70,334–75,560** | **76,339–161,155** | **68,202–117,459** | **72,751–155,512** |

Both scenarios together (used majors and cheaper equivalents): $64,816–112,017.

Where the used money goes:
- the laser: $23,000 → $2,500 (the returnable M6860 with ~$400 freight; the Korean YLR-500-AC is $6,953 with no
  returns);
- the scan head: $12,000 → $1,400–1,678;
- the scan card: $6,065 → $1,520 (an RTC5, so the PC needs a PCIe slot);
- the vacuum pump: $5,978 → $1,285;
- the dew-point sensor: $2,282 → $166–1,100;
- the O₂ analyzer: $2,091 → $1,028–1,129 with a new cell;
- the lens: $1,256 → $540 (an f = 254 mm marking lens);
- the power meter: $2,785 → $1,779;
- the UPS: $1,138 → $450.

Safety parts (relays, interlocks, the shutter, eyewear, extinguisher, O₂ monitors) stay new, as
[`cost-scenarios.md`](../cost-scenarios.md) recommends.

## 4. The expensive items, one by one

Every item over about $1,000 new, plus the servos, the supervisor or scan PC and the argon regulator, is in
`hud.json` (`items`) and `costs-leadtimes.csv`, 37 in all. Each item has:
- its new price, how firm that price is (quote, catalogue or estimate), and its source;
- its used listing (title, seller type, condition, returns, location, URL and fetch time; sellers aren't named), with
  the 2026-11-25 re-read;
- its lead times, the same-spec cheaper options for its line, and a note on risk.

The ones that matter most:

| Item | New | Used | The used listing | Risk |
|---|---:|---:|---|---|
| Fiber laser, 500 W SM (IPG YLR-500-U3-SM-AC) | 23,000 | 2,500 | YLR-400-SM-EOS (M6860), US surplus dealer, "Unit in mint condition", 30-day returns, seller pays return shipping | test it inside the 30 days. The $1,299.99 unit from the same dealer (still listed, 2 available) has a cut fibre ("Laser cable was cut"). No listing states hours, cooling or back-reflection protection |
| Scan head (SCANLAB basiCube 20) | 12,000 (placeholder) | 1,400 | hurrySCAN 25, 1500 W at 1064 nm, dealer with a 30-day warranty (still on its site on 2026-11-25) | check XY2-100 against SL2-100. The dealer's $1,500 hurrySCAN 25 comes with a Sill f = 163 mm lens, close to the drawn f = 160 mm |
| Scan card (SCANLAB RTC6) | 6,065 (placeholder) | 1,520 | RTC5 PCIe, US surplus seller, 30-day returns, buyer pays return shipping | needs a PCIe PC and SCANLAB's driver for a second-hand card |
| Zero-point clamps (2 × SCHUNK NSE-HT mini) | 5,770–6,380 | buy new | none searched | its pins have no published price or lead |
| Vacuum pump (Edwards nXDS6i) | 5,978 | 1,285 | Agilent IDP-3, US eBay seller, "Seller does not accept returns" | tip seals; not returnable |
| Glovebox (McMaster 4083N14) | 4,305 | buy new | used inert boxes were $3,000–7,875 | Cleatech 2100-2, $2,135, is the cheaper new box |
| Metal-dust vacuum (McMaster 5572N116) | 3,190 | buy new | none | Dynabrade 61470, $2,787.53 in 6 days |
| Power meter (Gentec-EO UP55M + U-LINK) | 2,785 | 1,779 | Ophir L1500W head (China, no returns) + Nova II meter (US) | recalibrate |
| Safety controller (Banner XS26-2 + modules) | 2,376 | buy new | none | 1 in stock at Digi-Key |
| Dew point (Vaisala DMT143) | 2,282 | 166 | Atlas Copco transmitter, open box, US, 30-day returns | made to order and non-returnable new; check the used unit's calibration |
| O₂ analyzer (Ntron Microx) | 2,091 | 1,028 | Alpha Omega Series 3000, US surplus seller, + ~$350 cell (estimate) | 6–8 weeks new |
| Shutter and beam dump | 508–2,000 | buy new | none | no catalogue shutter rated for 500 W CW was found |
| Recirculation blower (gas-tight) | 300–1,500 | buy new | used blowers aren't shown to be gas-tight | no gas-tight blower of this size found: the largest open purchase |
| MIC-6 plate (McMaster 86825K49) | 1,349 | buy new | | |
| f-theta lens (Thorlabs FTH160-1064 + windows) | 1,256 | 540 | LINOS f = 254 mm, US, 30-day returns | not the drawn focal length, and no CW rating |
| UPS (Eaton 5PX1500RTG2) | 1,138 | 450 | APC SMX1500RM2U, US UPS refurbisher, no returns | backordered new; ask the refurbisher for the battery date |

## 5. Time estimates

- **Machining**, per part, is in `times.csv` (section `machining`): CAM, setups (3-axis and 4th axis), cutting, and
  deburring and inspection. Totals are 287.3 h with an HRT210 4th axis and 302.3 h on a 3-axis, for 57 parts and
  69 / 137 setups. The chamber frame and floor plate are 25.4 h, of which 2.2 h is the posted G-code's cutting time
  (CAMotics).
- **The robot shop** ([`robot-shop.md`](../robot-shop.md), section `robot shop`): 137 person-hours by hand against 60–78
  in the cell. The cell runs 20 h a day once the CAM is done, and needs 34 h of machine time. These come from the
  older 48-part `dfm.json` (27.7 h of cutting). `hours.json` (57 parts) has since raised CAM to 132 h and cutting to
  33 h, so the robot-shop figures are low. Setting up the cell is not included: likely months for the first machine.
- **Assembly, per step** (section `assembly`): `analysis/out/assembly/results.json`'s `seconds` field is the time the
  FCL and IK checker took to compute each step. It is not how long the arm takes. `times.csv` therefore gives estimates,
  all labelled:
  - **Each placement:** 30 s, plus the insertion path from `sequence.json` at 10 mm/s.
  - **Screws:** 20 s plus 15 s a screw.
  - **Other arm moves:** 90 s for an O-ring or cord, 30 s for a flip, 60 s for a two-arm carry, 15 s for a tool change.
  - **MiR trips:** one per 4 parts, 140 s a round trip (from `timeline.py`'s legs, dockings and registrations).
  - **Person steps:** the minutes in `PERSON_MIN`. Each screw the arm couldn't drive is 1 min, and each failed
    placement 5 min.

  | Chapter | Steps | Arm time | MiR trips | Person time | Failed or partial | Person or shop steps |
  |---|---:|---:|---:|---:|---:|---:|
  | 40, the build module | 30 | 26 min | 12 min | 2.2 h (2 h is the shop TIG-welding seven feedthroughs) | 0 | 3 |
  | 41, chamber and process module | 103 | 1.9 h | 37 min | 6.5 h (3 h is the Class 1 laser guard) | 27 | 11 |
  | 50, integration on the tray | 6 | 1 h (leak check) | 0 | 4.3 h (hoist, rack units, gas module, hoses, dock) | 0 | 5 |

  The assembly renderer's own motion times (`proc_s`) replace these once its trajectories exist.

## 6. Inconsistencies found (reported, not changed)

1. **`cost-scenarios.md`'s totals are stale.** It gives $39,440–112,978 for the baseline, but `bom.csv` is now
   $76,339–161,155. The BOM grew in the 2026-11-22 to 25 rounds: electrical, X1 machining, the zero-point clamps, the
   tray dock and UPS. Running [`cost/cost_scenarios.py`](../cost/cost_scenarios.py) on today's BOM gives the current
   figures.
2. **Eight `cost/used-options.csv` base values predate the BOM.** `cost_scenarios.py` then subtracts components that
   are no longer in the line. Its used scenario comes to $73,554–120,061; re-based on today's lines, and with the
   2026-11-25 re-reads, it is $68,202–117,459 (`hud.json` → `consistency.used_rebase`). The changes:
   - **G2:** the 4396K21 rotary vane is gone, and both ends are now dry scrolls.
   - **T1:** the Gentec head is now at both ends, so the used Ophir set replaces $2,785, not $4,000.
   - **G9:** the Vaisala DMT143 replaces the old $1,000–2,500 estimate.
   - **G7:** the $455 Vacuum Research Pirani replaces the old $300–800 estimate.
   - **L3:** the high end is now the $790 expander.
   - **L6:** the low end is now the Thorlabs lens.
   - **M2:** two servos at $265–293 each.
   - **D2:** the refurbished UPS is added; D2 wasn't in the BOM when the used search ran.
   - **L6's $99.99 lens listing** ended on Nov 23; the other LINOS dropped to $539.99.
3. **25 counted rows of `cost/cheaper-equivalents.csv` replace parts no longer in their line**, worth $1,685. Examples are
   the Omron D4JL (S2 is IDEC now), the G9SE-201 (S1 is Banner), the 6709K12/K33 (M3 is THK), the SDR-480-24 and the
   old C6 enclosure parts. Without them the cheaper scenario is $72,751–155,512, against $71,067–153,500 as the script
   stands. The 88895K51 row is for 9 sheets; S9 now takes 7.
4. **Read the at-spec rule with care.** It takes the high end of L3 and L6. L6's low end is now the drawn lens (Thorlabs,
   $1,255.84 with windows), and its $2,500 high end is the Sill-lens alternative. L3's $790 high end is the fallback
   expander, while the IPG collimator's price is still to come. So the at-spec new total overstates the drawn chain by
   up to about $2.0k.
5. **`bom.csv`'s high end isn't one buildable machine.** It carries a $3,000 chiller (L2) next to the air-cooled IPG, the
   Vertiv UPS and the $5,000 CombiTac dock.
6. **`results.json`'s `seconds` is compute time** (see §5).
7. **`render_build.kit_cat()` has no keyword for the SCHUNK zero-point modules.** They fall to its default and lie in
   the electronics zone, so the HUD counts B3 there. Adding "Zero-point" to its motion keywords would move them, and
   B3 would then move to motion here too.
8. **Some earlier statements no longer hold.**
   - Cleatech's "ships within 25 days" (`cost-scenarios.md` §4) is no longer on its page.
   - DwyerOmega's CNI32-AL-DC, listed at 56 weeks, is now "unable to accept backorders" at Digi-Key.
   - `cost/used-options.csv`'s URL for the hurrySCAN 25 is cut short and returns 404. The dealer's search still lists
     the head.
   - The IDP-3 listing takes no returns; on 2026-11-20 its returns were "not stated".
9. **The scan PC may not be costed.** The model draws a 2U "Scan + laser controller PC" and tags it C1, but C1 holds
   only the RTC6 and its breakout ($6,065). The nearest cost is C2's $600 high end ("small industrial PC"); C2's low end
   is the Raspberry Pi 5 the model draws in PB2. A used RTC5 also needs a PC with a PCIe slot.

## 7. Still open

- **No published lead time, so a quote is needed:**
  - SCANLAB basiCube 20 and RTC6. Their $12,000 and $6,000 are BOM placeholders, not quotes.
  - The ≥ 500 W shutter: none in a catalogue; IPG's beam shutter is quote only.
  - Gentec-EO's head ("CONTACT SALES").
  - Solid Sealing's weld-ins ("Get in touch to place an order").
  - The Ferrotec SFL-006-NN and SSL-005-NN.
  - SCHUNK's SPC-HT mini 20 pins.
  - A gas-tight blower.
  - The Macurco OX-6: Kele blocks automated reads.
  - Thorlabs' PDA36A2: its page shows "Lead Time" with no date.

  Any of these could move the used route's date if it runs past ~10 weeks.
- **BYU purchasing.**
  - The 10–14 days is the Capstone office's guidance; the lab's own PO time may differ.
  - If McMaster is a Workday punchout supplier at BYU, its orders skip the PO step. Not checked.
  - Whether a PCard can buy on eBay was not checked.
- **Used listings sell.** These were read on 2026-11-25. The Nova II meter, the Pirani gauges, the Dwyer transmitter
  and the Edwards RV3 weren't re-read. Prices are asking prices, and most take offers.
- **Not read for stock:** McMaster's own pages (they render only by script), Midwest Steel's cutting time (the site
  blocks automated reads), and the Raycus and nLIGHT lasers (quote only).
- **Honing has no published turnaround:** Engis says only "Fast Turnaround Time". The 3–6 weeks is `outsourcing.md`'s
  estimate.
- **Estimates:** transit (2–5 days ground, 3–7 days freight), the used laser's freight (~$400, about a week), the
  assembly step times, and fabrication at 20 shop hours a week.

## Files and re-run

| File | What it is |
|---|---|
| [`hud.json`](hud.json) | Everything, for the compositor (also at `/tmp/robotbuild/data/hud.json`). Start with `tour` (the display strings for each category and its items, in tour order) and `headline`; `categories`, `items`, `lead_times` (every line and the schedule), `times` (machining, robot shop, assembly) and `consistency` (re-basing notes) have the detail |
| [`costs-leadtimes.csv`](costs-leadtimes.csv) | One row per category, item and BOM line: new, used, cheaper and at-spec prices, the running totals, the used listing, lead times new and used with their sources, and risk |
| [`times.csv`](times.csv) | Machining per part and in total, the robot-shop timeline, assembly per step and chapter (estimates), MiR trips, and the schedule per route |
| [`../analysis/robotbuild_data/build_hud.py`](../analysis/robotbuild_data/build_hud.py) | Builds the three files from `bom.csv`, the cost CSVs, the model's part tags, the machining, shop and assembly outputs, `leadtimes.py` and `ebay-recheck.csv` |
| [`../analysis/robotbuild_data/leadtimes.py`](../analysis/robotbuild_data/leadtimes.py) | Lead time per BOM line (new, used, faster), BYU's PO step, transit, fabrication, and the schedule routes |
| [`../analysis/robotbuild_data/leadtime-lookups.csv`](../analysis/robotbuild_data/leadtime-lookups.csv) | 128 vendor reads from 2026-11-25, each with the stated text, stock, URL, fetch time, basis (page or search snippet) and how it was read |
| [`../analysis/robotbuild_data/ebay-recheck.csv`](../analysis/robotbuild_data/ebay-recheck.csv) | The used picks re-read on 2026-11-25: still listed or ended, price, shipping, eBay's delivery window to 84602, returns |
| [`../analysis/robotbuild_data/fetch_pages.py`](../analysis/robotbuild_data/fetch_pages.py), [`ebay_recheck.py`](../analysis/robotbuild_data/ebay_recheck.py) | The readers: headless Chromium through the lab Pi's SOCKS tunnel, and typed-URL headed Chrome for eBay |

Re-run from the repo root (standard library only): `python desktop-lpbf/analysis/robotbuild_data/build_hud.py`.
