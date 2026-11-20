# What the machine costs with used parts, and with cheaper same-spec parts (2026-11-20)

For [issue #260](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/260) and PR 266. Sterling asked what the
machine costs if we buy used parts, and if we swap McMaster and similar catalogue parts for cheaper, not
lower-quality, equivalents from other sources. All prices were read live on 2026-11-20 between 13:59 and 14:55 UTC.
eBay was read through the lab Pi (BYU network). Nothing was bought and no seller was contacted.

The baseline is [`bom.csv`](bom.csv) as it stands: **$39,440–112,978**. The low end takes the cheapest listed option on
every line and the high end the premium one. [`cost/cost_scenarios.py`](cost/cost_scenarios.py) recomputes every figure
below from `bom.csv`, [`cost/used-options.csv`](cost/used-options.csv) (39 listings) and
[`cost/cheaper-equivalents.csv`](cost/cheaper-equivalents.csv) (128 rows).

## Short answer

- **Used parts take the high end from $113k to $72k.** Almost all of that is the laser, scan head and scan card. A
  returnable 400 W single-mode IPG laser is $2,100 plus freight in Texas, against IPG's ~$23k quote with 10–12 weeks'
  lead time, if it passes the checks in §1. (The $1,300 unit PR 270 led with has a cut fibre.) The low end moves only
  $2.8k, because the BOM's low end already assumes cheap new parts: a PRC laser, a marking galvo and the open-source
  OPAL controller.
- **At the design's spec, the difference is about $34–40k.** The CW optics chain (laser, collimator, scan head, lens,
  scan card) is $44.0k new and $5.5k–11.2k used. With the cheapest options everywhere else, the machine is **$79.2k
  all new, $39.1k–44.8k with used majors, and $34.2k–39.9k with cheaper catalogue parts as well.**
- **Cheaper same-spec catalogue parts save $5.3k at the low end and $7.7k at the high end.** The biggest single item
  is an acrylic Cleatech glovebox in place of McMaster's steel one ($2.2k). Most of the rest is many small swaps: Kurt
  J. Lesker KF hoses, AutomationDirect safety and panel parts, Omega thermocouples, OnlineMetals sheet and Misumi
  T-slot hardware. McMaster is already the cheapest found for 6061 plate, the 30 mm T-slot rail, the M12 ball screws
  and the Class D extinguisher.
- **Both together: $31.7k–65.0k.**
- **Lead time: only the used laser shortens the critical path.** It ships the same day from El Paso, and with freight
  it comes to about $2.5k, under BYU's $3,500 purchase-order line. None of the cheaper sources takes longer than IPG's
  10–12 weeks except possibly one power supply (§4).
- **Engraver testbed first: it adds $7,500 whichever way the CW chain is bought.** It only gains time if the CW
  laser is bought new. A returnable used CW laser arrives sooner, costs a third as much, and is the real source.

| Scenario | Low (USD) | High (USD) | vs baseline low | vs baseline high |
|---|---:|---:|---:|---:|
| Baseline, all new (bom.csv) | 39,440 | 112,978 | +0 | +0 |
| Used majors | 36,655 | 71,884 | -2,785 | -41,094 |
| Cheaper same-spec equivalents | 34,168 | 105,324 | -5,272 | -7,654 |
| Both (used majors + cheaper equivalents) | 31,711 | 65,002 | -7,729 | -47,976 |
| Engraver testbed first, phase 0 (baseline prices, CW chain deferred) | 42,675 | 73,466 | +3,235 | -39,512 |
| Engraver testbed first, then the CW chain (baseline prices) | 46,940 | 120,478 | +7,500 | +7,500 |
| Engraver testbed first, phase 0 (both prices, CW chain deferred) | 36,132 | 58,256 | -3,308 | -54,722 |
| Engraver testbed first, then the CW chain (both prices) | 39,211 | 72,502 | -229 | -40,476 |

How the script combines them: each row of the two CSVs names the BOM component it replaces and what that component
adds to the line's low and high totals. For each component and each end, the scenario takes the cheaper of the BOM's
option and the alternative. So a scenario's low end still holds the BOM's under-spec low options. The like-for-like
comparison is the at-spec table:

| Build (CW chain at spec, cheapest listed option on every other line) | CW chain (USD) | Machine total (USD) |
|---|---:|---:|
| All new (IPG quote, SCANLAB quotes) | 44,012 | 79,188 |
| All new chain + cheaper equivalents elsewhere | 44,012 | 73,916 |
| Used CW chain + other used majors | 5,520–11,246 | 39,097–44,822 |
| Used CW chain + used majors + cheaper equivalents | 5,520–11,246 | 34,152–39,878 |

Run `python desktop-lpbf/cost/cost_scenarios.py --lines --at-spec` for every BOM line that changes, per scenario.

## 1. Used scenario

**How it was checked.** On 2026-11-20 between 14:01 and 14:22 UTC, through the lab Pi's SOCKS tunnel, in headed
Chrome on a virtual display. As PR 270 found, eBay only loads when the URL is typed into the address bar (`xdotool`),
so every search and item page was typed. About 50 pages loaded before eBay started serving its error page again.
Item pages loaded this time, so condition text, returns and shipping come from the listing itself. Every listing is a
row of [`cost/used-options.csv`](cost/used-options.csv), with URL, fetch time, condition, returns, the checks to make
and a verdict. Seller names are left out. These are asking prices, and most take offers. eBay's sold prices are still
behind a sign-in (checked 14:14 UTC).

**Still listed at yesterday's prices:** the three US YLR-400-SM-EOS lasers, the Korean YLR-500-AC, the YLR-200-AC-Y11,
the intelliSCAN III 20, the RTC5 card, the f = 254 mm LINOS lens, the IPG collimator, the Teledyne 3190 and the
Agilent IDP-3.

**What the item pages added:**
- **The $1,299.99 YLR-400-SM-EOS has a cut fibre.** Its description reads "Removed from working production line. All
  warranty seals are in place. Laser cable was cut." A single-mode output fibre has to be re-spliced or replaced by
  IPG, and that repair isn't quoted. So this is not a $1.3k working laser.
- **The $2,099.99 unit from the same dealer (M6860) is described as "Unit in mint condition. All warranty seals are in
  place".** It has 30-day returns with the seller paying return shipping. It ships by freight from El Paso, in a
  100 lb crate of 26 × 30 × 16 in. **This is the used laser to try first.**
- **The Korean YLR-500-AC is only "Power on tested, not functional tested", and the seller takes no returns.**
- **The RTC5 card "was tested using an IPG Photonics YLR-Series Laser System"** (P/N 117540.04). It has 30-day returns,
  with the buyer paying return shipping.
- **New since PR 270:** three IPG YLR-400-WC units (2017, 2019, 2017) at $4,500 each, with free returns. Their titles
  don't give the mode, and they are water-cooled.

**The picks the totals use:**

| Line | New (BOM) | Used, low pick | Used, high pick | Verdict |
|---|---|---|---|---|
| L1 laser | $3,300–23,000 | IPG YLR-400-SM-EOS (M6860), $2,099.99 + ~$400 freight (estimate); US, 30-day returns | IPG YLR-500-AC, $4,999.90 + $1,953 shipping; Korea, no returns | low: sensible with checks; high: risky |
| L3 collimator | $0–512 | $0 if the laser keeps its output optics | IPG P30-001277, $495 | check beam diameter and connector |
| L5 scan head | $419–12,000 | SCANLAB hurrySCAN 25 (1,500 W at 1064 nm), $1,200 + ~$200 shipping and DC supply (estimates); dealer's 30-day warranty | SCANLAB intelliSCAN III 20 (1080 nm), new open box, $1,527.71 + ~$150 supply (estimate); 30-day returns | sensible with checks |
| L6 lens | $486–2,500 | LINOS F-Theta-Ronar f = 254 mm, $99.99, free returns | the same lens, $599.99, free returns | marking lens, no CW rating |
| C1 scan card | $60–6,000 | (OPAL, $60, stays) | SCANLAB RTC5 PCIe, $1,520.34, 30-day returns | sensible with checks |
| G2 pumps | $2,079–5,491 | Edwards RV3 two-stage, $460.69, free returns (for 4396K21) | Agilent IDP-3 dry scroll, $1,284.58 (for the ~$4,000 scroll) | sensible |
| G6 trace O₂ | $1,271–2,091 | Alpha Omega Series 3000, $677.65 + ~$350 new cell (estimate) | Teledyne 3190, 4–20 mA, $779 + ~$350 cell; free returns | check the lowest range |
| G7 gauges | $3,281–3,781 | Agilent PVG-500 Pirani, open box, $289 + ~$30 reducer; Dwyer 628 0–15 psia transmitter, new surplus, $31 (for 3861N11) | InstruTech CVM211 Pirani, used, $356.55 + reducer | sensible |
| G9 dew point | $1,000–2,500 | Atlas Copco −100 to +20 °C dp transmitter, open box, $165.99 | Michell Easidew EA2-TX-100-DH, refurbished, $1,100 | check calibration date |
| T1 power sensor | $1,691–4,000 | (Thorlabs S322C stays; it stops at 200 W) | Ophir L1500W head, $499 (China) + Nova II meter, $1,279.99 (US) | recalibrate |
| M2 servo | $530–972 | one ClearPath-SD NEMA 23, open box, $197.18 | the same | sensible |

**Sensible vs risky.**
- **Sensible, mostly because they are returnable:** the M6860 laser, after the checks below; the SCANLAB heads that
  come with returns or a warranty; the RTC5; the LINOS lens; the Edwards RV3; the Pirani gauges; the Dwyer 628; the
  Teledyne 3190 with a new cell; and the ClearPath. The returnable $4,500 YLR-400-WC units are the fallback laser if
  IPG confirms from the serial that they are single-mode; they bring back the chiller (L2).
- **Risky:**
  - the cut-fibre YLR-400;
  - the Korean YLR-500-AC (no returns);
  - the Chinese YLR-500-WC units (no stated returns; a PRC seller raises README §7 Q1);
  - the $1,850 YLR-500-WC, whose mode isn't stated (500 W multimode units are common and won't give the spot);
  - the 2003-era RTC4 cards ($100–606);
  - used blowers, which aren't shown to be gas-tight.
- **Not worth buying used:**
  - safety relays, door interlocks, e-stops, laser eyewear, laser windows and extinguishers: buy these new and
    traceable. "Brand new" Omron G9SE-201 relays from China at $90.59 are the counterfeit risk;
  - HEPA elements, which are consumables;
  - gloveboxes, whose used inert boxes were $3,000–7,875;
  - KF hardware, which costs less new (§2).
- **Not in the BOM:** a UPS. A refurbished APC SMX1500 is $449.99, if one is added for the supervisor and controls.

**The risks of a used laser, and the checks.**
- **Back-reflection protection.** None of the listings states it. Al is reflective, and back-reflection damaged
  optics on NIST's AMMT (README §3.2). Give IPG the serial number and ask.
- **Hours.** None stated. Ask the seller, and read the status and alarm registers over RS-232 or Ethernet inside the
  return window (whether a model reports its hours wasn't checked).
- **Interlock and interface documents.** The -EOS units are OEM variants built for EOS machines. Ask IPG whether one
  runs stand-alone on the standard interface, with a hardware interlock and the guide laser, and get the user guide
  for that model.
- **Import.** A laser bought from Korea or China comes through US customs as a laser product under FDA's
  radiation-safety rules. Ask BYU's customs broker or purchasing what paperwork it needs (not checked: the shared
  web-search budget ran out). Buying within the US is not an export, so export rules only matter if the laser later
  leaves the country. ITAR isn't expected for a commercial industrial fibre laser, but I didn't check.
- **No vendor support or warranty.** Ask IPG what an evaluation or repair of a second-hand unit costs before
  relying on one.
- **Safety work is the same as for a new laser:** BYU Laser Safety Officer registration and the interlock chain in
  README §3.7.

**Test it inside the 30 days** (from PR 270's `sourcing/README.md`). Inspect the fibre end and the guide laser. Fire
into a dump at 10–100 % with a power meter, and plot power against set point. Read the status registers. If a
profiler is available, check M².

## 2. Cheaper same-spec equivalents

Every McMaster row the BOM totals count was looked up, in three parallel agent sessions. So were the DigiKey and
Thorlabs catalogue parts in the safety and controls lines, and the three estimate lines (Pirani, dew point, trace O₂).
Prices come from vendor pages, read with WebFetch or in headless Chrome through the tunnel. Each row of
[`cost/cheaper-equivalents.csv`](cost/cheaper-equivalents.csv) gives the part it replaces and its price, then the
alternative's vendor, part number, URL, price, fetch time, a same-spec call (`yes`, `close` or `no`), an equivalence
note and a lead-time note. The script counts a row only if a loaded page showed its price and the spec is `yes` or
`close`. Of 128 rows, 79 count. Not counted: 13 priced only from search snippets (mostly Zoro, which blocks
automated reads), 30 with no price found, and 6 others (wrong spec, used, or not in the BOM total).

The biggest swaps (savings at the BOM end where the part sits):

| Line | Replaces (now) | Alternative (vendor: part) | Now (USD) | Alt (USD) | Saving | Same spec? |
|---|---|---|---:|---:|---:|---|
| P1 | 4083N14 | Lab Supply Network: Cleatech 2100-2 with airlock | 4,305.48 | 2,135.00 | 2,170 | close: acrylic, not painted steel; 8 in. ports; larger; no humidity meter |
| S2 | Omron D4JL-4NFA-C5-NPT (DigiKey, out of stock) | AutomationDirect: IDEM KLM-202002 + actuator 140107 | 803.42 | 299.50 | 504 | close: solenoid power-to-unlock, 2,000 N, 4 NC + 1 NO, 44 in stock; different footprint |
| G2, G7 | 3497N23 × 5 | Kurt J. Lesker: MHB-QF-B24 | 1,922.25 | 1,097.50 | 825 | yes: braided, KF-25, 24 in., 1 in. ID, in stock |
| A2 | 5572N116 | TA Industrial: Dynabrade 61470 | 3,189.78 | 2,787.53 | 402 | close: very likely the unit McMaster resells; confirm NFPA 484 |
| H1 | 3871K606 × 9 | RSP Supply: Omega TJ36-CASS-040U-6-CC | 1,338.03 | 937.35 | 401 | close: 304 sheath, not 316; 40 in. cable |
| G7 | Pirani (estimate) | MKS: 275400-1-GD-T | 800.00 | 447.00 | 353 | close: non-linear 0.375–5.66 V output |
| S7 | 18995T81 | Global Test Supply: Honeywell BW Clip BWC2-X | 459.00 | 117.53 | 341 | close: same 2-year clip-on type; approvals not on the page |
| G7 | 8077K237 × 2 | U.S. Solid: USS2-00052 | 346.18 | 31.88 | 314 | close: brass, NC, zero-differential, but Cv 0.23 not 0.58; import brand |
| G2 | 4396K21 | Amazon: Robinair 15300 | 587.53 | 281.55 | 306 | close: HVAC two-stage, 3 cfm, 35 micron vs 15 (still far below 1 mbar) |
| S9 | 88895K51 × 9 | OnlineMetals: 7128 | 653.22 | 384.21 | 269 | yes: 5052-H32, 0.063 in., 24 × 24 in.; mill test report on request |
| G9 | dew point (estimate) | Selectum: Vaisala DMT143 | 2,500.00 | 2,281.70 | 218 | yes; confirm the 4–20 mA build; made to order |
| G7 | 3861N11 | ZOT Supply: Dwyer 628-00-GH-P1-E1-S1 | 358.05 | 157.06 | 201 | close: 0–15 psia, 4–20 mA; 0 in stock, 8 weeks |
| S9 | 5537T536 × 44 | Misumi: HBLFSN6 + HNTAJ6-6 nuts | 261.36 | 127.16 | 134 | close: die-cast; the 88 screws aren't priced |
| G7 | 4123K45 | MROSupply: Dixon BV2CV-100VV-A | 300.80 | 178.08 | 123 | yes: cast 316, KF-25, helium-tested to 1e-8 Torr |
| S1, S3, S4, C6 | Omron, IDEC and McMaster panel parts (10 rows) | AutomationDirect (IDEM, Fuji, Patlite, its own and Saginaw) | 1,062.02 | 552.75 | 509 | mostly close (§5 item 8) |
| M1, M3 | 6709K12 × 2 | DigiKey marketplace: HIWIN HGH-15-CA-Z0-C | 289.42 | 150.00 | 139 | close: genuine HIWIN; ships in about 20 days |

The other counted swaps save $887 more. They include the Cleatech box without airlock at P1's low end ($138), Misumi
drop-in nuts, the Lesker inline filter, the Harris regulator, the same Omron fibre parts from MRO Supply, a
StepperOnline stepper, Omega heaters and connectors, a Mean Well NDR supply, MKS KF clamps and rings, Solberg HEPA
elements, and 316 screws from Bolt Depot and Fair Wind.

**McMaster is already the cheapest found for:**
- 6061-T651 1/2 in. plate: Speedy Metals $183.23, Metals Depot $191.06, against $148.74;
- the 30 mm T-slot rail: 80/20 $25.07 and Misumi $28.18 per 4 ft, against $23.86;
- the M12 ball screws: Misumi $777–800, against $319–433 with nut;
- the 30 lb NaCl Class D extinguisher: Uline $1,145, against $920.22;
- the Solberg intake-filter housing (Solberg's own list price is $110), the DIN rail and the Thorlabs window.

**Not priced:** about $1.8k of McMaster parts. These are the B1 316 stock, the bellows couplings (Ruland's site blocks
automated reads), the 4566N401 nut, the latches, hinges and feet, the Macor rod, the O-rings and cords, and some
fasteners.

**Equivalence and traceability.** McMaster gives no certificates by default either. The name-brand alternatives
(Lesker, MKS, Dwyer, Omega, Vaisala, HIWIN, IDEM, Patlite, Harris, Solberg, Dixon) trace to their makers. OnlineMetals
offers a mill test report. Two alternatives are import brands, U.S. Solid and StepperOnline, and the Robinair price
was read off Amazon's search page without opening the product page. Unbranded KF-25 hoses ($26.99 for 500 mm) and ball
valves ($40–99) on eBay are in the CSV for scale but not counted.

## 3. Engraver testbed first

Monport's answers in the thread: the GT 200 W split MOPA is about $7,500 with the academic discount. It is pulsed only
(no CW or QCW), it runs Monport's closed "BSL" controller, and its galvo has a 15 mm aperture. So it can't stand in for
lines L1, L5 or C1 at the design's spec. It has no Python SDK (C1's requirement), and nothing says its galvo or lens
take 400–500 W CW.

What it would buy is a running bench while the CW chain is on order:
- commissioning of the chamber, gas loop, O₂ and dew-point sensing, interlocks, recoater, heated plate and layer camera;
- the open question in README §1b.1: whether pulsed 200 W light melts our Al powders at all.

The script prints the phase-0 spend (CW chain deferred, engraver added) and the total once the CW chain is bought as
well. **Either way the engraver adds $7,500.** It saves time only against a new IPG laser. A returnable used 400 W
single-mode laser can be on the bench in one to two weeks for about a third of the engraver's price, and it is the
real CW source. So buy the engraver only if the pulsed-melting question matters for its own sake, or if the used laser
fails its checks and the new IPG order goes in.

## 4. Lead time

| Item | Bought new | Used or cheaper source |
|---|---|---|
| L1 laser | IPG: 10–12 weeks after the order, plus BYU's PO process (over $3,500) | US dealer ships the same day; freight about a week (estimate); about $2.5k, under the $3,500 PO line. Korea: 4 days' shipping plus customs |
| L5 head, C1 card | SCANLAB lead times not quoted | eBay, in the US: the RTC5 listing gives Nov 23–25 delivery to Provo |
| S2 door interlock | Omron D4JL: none in stock at DigiKey, which takes no backorders | IDEM KLM-202002 at AutomationDirect: 44 in stock |
| A1 fibre amplifier | E3NX-FA41: 33-week factory lead time (5 in stock) | none |
| G2 inline filter | McMaster (stock not recorded) | Lesker LDA-KJLC-S-2KF25: 6–7 weeks, for an $82 saving |
| P1 glovebox | McMaster (stock not recorded) | Cleatech 2100-2: ships within 25 days |
| M1, M3 rails and carriages | McMaster (stock not recorded) | HIWIN through a DigiKey marketplace seller: about 20 days |
| S4 stack light | McMaster (stock not recorded) | Patlite at AutomationDirect: backordered to 2026-12-04 |
| G7 differential transmitter | McMaster (stock not recorded) | ProSense DPTA backordered to 2027-01-29; DwyerOmega 616KX: 121 in stock |
| C4 24 V supply | DigiKey | Mean Well NDR-480-24: stock not shown, 17-week factory lead time |

**The laser stays the critical path unless it is bought used.** Of the cheaper sources, only the NDR-480-24 might take
longer than IPG's 10–12 weeks, and DigiKey's SDR-480-24 stays as its fallback.

## 5. BOM changes I'd suggest (not made: `bom.csv` is unchanged)

1. **L1:** add the used route to `alternative`: used IPG YLR-400-SM-EOS on eBay, $2,099.99 plus freight, 30-day
   returns (`cost/used-options.csv`). Consider a `unit_low_usd` of 2,500 in place of the $3,300 unconfirmed Raycus,
   since it is the cheapest option found that meets the spec.
2. **L5:** the $419 low end is a marking head that L5's own note limits to a low-power bench. The cheapest head at spec
   is a used SCANLAB hurrySCAN 25 or intelliSCAN III 20, at about $1,400–1,700 with its supply. Make that the low end,
   or say in the note that the low end is under spec.
3. **C1:** add "used RTC5 PCIe, $1,520, tested on an IPG YLR" as an alternative. It needs a PC with a PCIe slot, which
   puts C2 at its $600 industrial-PC end.
4. **G2:** use a lab two-stage pump (a used Edwards RV3 at $461, or a Robinair 15300 at $281.55 new) in place of
   4396K21 at the low end. The ~$4,000 dry-scroll high end is $1,285 used (Agilent IDP-3).
5. **G7:** replace the $300–800 Pirani estimate with live prices: an MKS 275 at $447 new, or $289–357 open-box or used.
   Swap the five 3497N23 hoses for Kurt J. Lesker MHB-QF-B24 (saves $825), and 3861N11 for a Dwyer 628 0–15 psia
   transmitter ($157–186 new).
6. **G6 and G9:** the BOM's SST OXY-FLEX alternative may be a percent-level sensor, not a ppm one (check its range),
   in which case G6's $1,271 low end is too low. New ppm analyzers were $2,700 (Analytical Industries
   GPR-1500 at Instrumart). G9's $1,000 low estimate is below every live new price found (Vaisala DMT143 $2,281.70;
   Michell EA2-TX $2,556). Either raise both lows or name a used unit: $1,028–1,129 for O₂, including an estimated new
   cell, and $166–1,100 for dew point.
7. **H1:** 3871K606 ($148.67 × 9) → Omega TJ36-CASS-040U-6-CC ($104.15). Its sheath is 304, not 316, which is fine in
   argon at ≤ 500 °C. It saves $401.
8. **Safety and panel parts (S1–S4, C6):** AutomationDirect equivalents save about $1,010. The biggest is the IDEM
   KLM-202002 guard-lock switch ($287 + $12.50 actuator, 44 in stock) in place of the out-of-stock Omron D4JL
   ($803.42). It changes the door bracket, so the CAD needs a matching edit. S7: a Honeywell BW Clip ($117.53) is
   the same type as 18995T81, the 2-year clip-on detector. A fixed wall monitor would be the better room alarm.
9. **P1 and A2:** the Cleatech acrylic glovebox ($1,556–2,135) and Dynabrade's own 61470 wall vacuum ($2,787.53, very
   likely the unit McMaster resells) are the biggest single savings. Before switching, confirm the glovebox's gas
   ports and add a hygrometer, and confirm the vacuum's NFPA 484 listing.

## 6. Not done

- **No seller, vendor or IPG was contacted.** No used-laser listing states hours, cooling or back-reflection
  protection.
- **The shared web-search budget ran out at about 14:16 UTC.** After that, prices came only from vendors' own pages,
  so some rows have no price.
- **Freight, the head's DC supply, the O₂ cell and the reducer are estimates,** labelled as such in
  `used-options.csv`. Import duty, brokerage, tax and shipping on the new parts are not included.
- **Chillers weren't searched used.** eBay rate-limited the session first. L2 is needed only if the laser bought is
  water-cooled.
- **[`seal-parts.csv`](seal-parts.csv) appeared during this run** (another agent). Its priced rows come to about
  $2.9k of O-rings, latches, clamps and feedthroughs, some of them alternatives. They are not in `bom.csv` yet, so
  they are in none of the totals. One check: an FKM 75 AS568-238 is $2.142 each at The O-Ring Store (minimum 5),
  against McMaster's $2.25 each in a 5-pack. So the O-rings aren't cheaper elsewhere once The O-Ring Store's $10
  minimum and $9.95 shipping are added. The six hermetic feedthroughs ($2,057 together) are the seal-parts rows
  worth re-quoting.
- **Prices change.** Listings come and go, so re-read them before buying.

## Files

| File | What it is |
|---|---|
| [`cost/used-options.csv`](cost/used-options.csv) | 39 used and new-surplus listings: BOM line, component replaced, condition, price, shipping, estimated extras, returns and warranty, URL, fetch time, checks, verdict and whether the totals use it (`pick`) |
| [`cost/cheaper-equivalents.csv`](cost/cheaper-equivalents.csv) | 128 rows: the McMaster, DigiKey or Thorlabs part and its price, the alternative's vendor, part number, URL, price and fetch time, a same-spec call, equivalence and lead-time notes, and whether the totals count it |
| [`cost/cost_scenarios.py`](cost/cost_scenarios.py) | reads `bom.csv` and both CSVs, then prints the scenario totals, the at-spec table, and, with `--lines`, every BOM line that changes |
