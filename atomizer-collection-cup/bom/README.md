# Collection cup: catalogue parts, prices and vendor dimensions (2026-11-27)

Public catalogue prices for the lab-built collection cup (options A, B and C in `../params.py`), fetched
2026-11-27 between 17:45 and 18:13 UTC. Prices are USD for one unit as listed, before shipping, tax and
cut-to-length fees. Nothing was ordered or quoted and no vendor account was used, so lines that only show
"price on request" or "request a quote" are listed as not priced.

| File | What it is |
|---|---|
| `vendor-lookups.csv` | 175 lookups, one row per vendor part: item, option, vendor, part number, material, key dimensions (mm), price, quantity break, stock or lead time, URL, fetch time, notes |
| `vendor_dims.json` | Vendor dimensions the CAD needs, keyed by part number, from the vendors' tables, drawings and free STEP files (measured with CadQuery). `_vs_params` compares them with `params.py` |
| `fetch_*.py` | Re-run the lookups (see the end of this file) |

## Totals

Cheapest sensible pick per line; the per-line tables below list the alternatives.

| Option | Total (USD) | What sets it |
|---|---:|---|
| A, catalogue only | **185.00** | Duniway 160 mm KF-50 nipple 67.00; blank, centring ring, clamp and two over-pressure rings (bottom joint and cone joint) 74.98; liner and puck stock 43.02 |
| B, welded 316L, KF-50 top end | **404.35** | Metal 219.83 (stub, reducer, tube, bar, liner, puck); thermocouples, clamps, 2-channel meter and buzzer 144.14; ER316L rod 27.13; over-pressure ring for the cone joint 13.25 |
| B, welded 316L, 2 in tri-clamp top end | **364.15** | As above with a 316L tri-clamp ferrule (10.76) and a spare FKM gasket (2.84) instead of the KF stub and the cone's over-pressure ring |
| C, glass rebuild | **523.27** | Quartz tube 189.98 and the 316L bar for the valve-delete spacer 207.00 |
| Every option | 12.84 | Snoop leak-check fluid, 8 oz |

Optional, not in the totals: an isolation valve (KF-50 ball valve, Lesker BVR0200MVQF, 359.00, PTFE seat,
bakeable 100 °C; or a 2 in tri-clamp butterfly valve, McMaster 4820K63, 316 with FKM seat, 388.68; or
Dernord DER0316, 58.99, seat material not stated and the valve rated only to 93 °C) and a gauge for a
rate-of-rise test (Duniway DTC-531-115 thermocouple gauge, 505.00, plus a KF16 to 1/8 NPT stub, 25.50).

## Per option

Bar lengths are the blank lengths in `cam/lathe_cam.py` (part, plus 10 mm in the chuck and 1 mm to face), rounded up. Speedy Metals cuts bar to length and prices it by the inch; "/in" is its 1 in base price and longer pieces cost a little less per inch, so those lines are upper estimates. No cut fees are shown.

### Option A: catalogue only

| Line | Pick (vendor, part no.) | Buy | Unit price | Ext. | Stock / lead | Alternative |
|---|---|---|---|---|---|---|
| KF-50 full nipple (160 mm) | Duniway Stockroom KF50-NP | 1 | 67.00 | 67.00 | not shown | Lesker QF50-200-N 140 mm 83.45; MDC 721003 163 mm 132.83; McMaster 4518K877 140 mm 118.37 |
| KF-50 blank (304) | Duniway Stockroom KF50-FB | 1 | 16.00 | 16.00 | not shown | A&N 4000163 22.00 (177 in stock); MDC 712003 23.10 |
| Bottom centring ring, stainless + FKM | MDC Precision 710003 (K200-CR) | 1 | 18.48 | 18.48 | Available, ships tomorrow | A&N 4000008 (316) 19.00; Lesker QF50-200-SRV 20.55; Lesker QF50-200-SCV captured outer ring 14.00 |
| Over-pressure ring, bottom joint | A&N Corporation (ANCORP) 4000076 (QF50-200-OPR) | 1 | 13.25 | 13.25 | 94 in stock | McMaster 4518K69 (ring + Al outer ring, 50 psi) 43.30 replaces this line and the ring above |
| Bottom clamp, Al wing nut | Duniway Stockroom KF50-CP | 1 | 14.00 | 14.00 | not shown | A&N 4040003 16.50; Lesker QF50-200-C 16.60; stainless: Lesker QF50-200-SSC 31.70 |
| Liner, 304 tube 1-3/4 in x 0.049 in | McMaster-Carr 11116N835 | 1 ft | 24.20 | 24.20 | not shown | - |
| Catch puck, 304 bar 2 in (49 mm blank) | Speedy Metals p-1866 (2 in Rd 304 CF annealed) | 2 in | 9.41/in | 18.82 | not shown | McMaster 89535K65 64.26 (6 in) |
| Over-pressure ring on the cone's existing KF-50 joint (recommended) | A&N Corporation (ANCORP) 4000076 (QF50-200-OPR) | 1 | 13.25 | 13.25 | 94 in stock | Lesker QF50-200-OPR 12.25 (not stocked); McMaster 4518K69 ring + Al outer ring 43.30 (50 psi) |
| **Total** | | | | **185.00** | | |

### Option B: welded 316L, KF-50 top end

| Line | Pick (vendor, part no.) | Buy | Unit price | Ext. | Stock / lead | Alternative |
|---|---|---|---|---|---|---|
| KF-50 weld stub, 316L, 19.05 mm | Kurt J. Lesker QF50-200-SSL | 1 | 40.55 | 40.55 | not stocked: 'KJLC will contact you' | 304L in stock: A&N 4000126 25.00, Lesker QF50-200-SST 29.35, McMaster 4518K38 36.28; 316 long (40.1 mm): A&N 4003138 58.00 |
| 2 x 3 in concentric reducer, butt weld, 316L (101.6 mm) | McMaster-Carr 5237K471 | 1 | 32.13 | 32.13 | Delivers Monday (2026-11-30) | BuyFittingsOnline BF631W-3X2-7 (polished) 45.47; McMaster 5237K47 (polished) 49.84 |
| Body: 316L tube 3 in x 0.065 in | OnlineMetals 4256 | 12 in | 48.43 | 48.43 | not shown | McMaster 4466K62 52.39 (1 ft) |
| Bottom disc: 316L bar 3-1/4 in (19 mm blank) | Speedy Metals p-2646 (3-1/4 in Rd 316 CF annealed) | 1 in | 31.61/in | 31.61 | not shown; UPS up to 90 in, longer by freight | McMaster 9260K4 (3-1/2 in disc) 75.12 for 1 in |
| Liner: 304 tube 2-3/4 in OD (0.065 in wall; 0.049 not stocked) | OnlineMetals (marketplace, sold by Stainless Headers Mfg.) mp-00038303 | 12 in | 38.95 | 38.95 | not shown; ships from Lake City MN | McMaster 11116N864 52.88 |
| Catch puck: 304 bar 3 in (36 mm blank) | Speedy Metals p-1872 (3 in Rd 304 CF annealed) | 1.5 in | 18.77/in | 28.16 | not shown | McMaster 89535K75 124.24 (6 in) |
| Type K washer thermocouple (junction 900 C) | Auber Instruments TC-K-WS | 2 | 15.85 | 31.70 | not shown | DwyerOmega WTK-HD-72-S 87.49 |
| Worm-drive clamp for the 2 in stub (pack of 10) | McMaster-Carr 5415K18 | 1 pk | 12.89 | 12.89 | not shown | screws zinc-plated, 121 C: see note |
| Worm-drive clamp for the 3 in body (pack of 10) | McMaster-Carr 5415K23 | 1 pk | 18.26 | 18.26 | not shown | as above |
| 2-channel type K meter, 2 alarm relays | Auber Instruments SYL-2813AC | 1 | 69.99 | 69.99 | not shown | - |
| Buzzer, 30-120 VAC panel mount | McMaster-Carr 56965T26 | 1 | 11.30 | 11.30 | not shown | DC version 56965T23 8.06 |
| ER316L TIG rod 1/16 in, 1 lb | McMaster-Carr 7972A501 | 1 lb | 27.13 | 27.13 | in stock; part page: Delivers Monday (2026-11-30) | 3/32 in 7972A479 29.31 |
| Over-pressure ring on the cone's existing KF-50 joint (recommended) | A&N Corporation (ANCORP) 4000076 (QF50-200-OPR) | 1 | 13.25 | 13.25 | 94 in stock | Lesker QF50-200-OPR 12.25 (not stocked); McMaster 4518K69 ring + Al outer ring 43.30 (50 psi) |
| **Total** | | | | **404.35** | | |

### Option B, tri-clamp top end

These two lines replace the KF stub and the cone's over-pressure ring above (B total 364.15).

| Line | Pick (vendor, part no.) | Buy | Unit price | Ext. | Stock / lead | Alternative |
|---|---|---|---|---|---|---|
| 2 in tri-clamp short weld ferrule, 316L (12.7 mm) | McMaster-Carr 50485K213 | 1 | 10.76 | 10.76 | Delivers Monday (2026-11-30) | BuyFittingsOnline BF614WMP-2 9.29 ($40 order minimum) |
| 2 in tri-clamp gasket, FKM (spare for the cone joint) | McMaster-Carr 5044K55 | 1 | 2.84 | 2.84 | in stock; part page: Delivers Monday (2026-11-30) | PTFE McMaster 43315K55 3.06 / Brewers TC20GASPTFE 1.25 |
| **Total** | | | | **13.60** | | |

### Option C: glass rebuild

| Line | Pick (vendor, part no.) | Buy | Unit price | Ext. | Stock / lead | Alternative |
|---|---|---|---|---|---|---|
| Fused quartz tube 100 x 92 (4 mm wall) x 300 mm, one end closed | MTI Corporation HQT100 (SKU TQH4D300) | 1 | 189.98 | 189.98 | 17 in stock | MTI TQ4D650 100 x 94 x 650 275.00; TGP 95x100 602.50 per 5 ft |
| Glass seals: FKM O-ring AS568-342 (91.44 x 5.33), size to the measured groove | Global O-Ring and Seal V75342 | 2 | 6.91 | 13.82 | not shown | -341 V75341 6.62; -344 V75344 7.32; FKM cord McMaster 96515K129 3.78/ft |
| 304 sheet 18 ga (1.22 mm) 12 x 12 in, splash shield / pan | McMaster-Carr 8983K38 | 1 | 22.85 | 22.85 | not shown | 16 ga 8983K42 27.12 |
| 304 bar 2-3/4 in for the entrance sleeve (86 mm blank) | Speedy Metals p-1871 (2-3/4 in Rd 304 CF annealed) | 3.5 in | 21.82/in | 76.37 | not shown | - |
| 316L bar 5-1/2 in for the valve-delete spacer (56 mm blank) | Speedy Metals p-2655 (5-1/2 in Rd 316 CF annealed) | 2.25 in | 92.00/in | 207.00 | not shown | McMaster 9260K7 (6 in x 2 in disc, 50.8 mm, short of 56) 378.60 |
| Over-pressure ring on the cone's existing KF-50 joint (recommended) | A&N Corporation (ANCORP) 4000076 (QF50-200-OPR) | 1 | 13.25 | 13.25 | 94 in stock | Lesker QF50-200-OPR 12.25 (not stocked); McMaster 4518K69 ring + Al outer ring 43.30 (50 psi) |
| **Total** | | | | **523.27** | | |

### Every option

| Line | Pick (vendor, part no.) | Buy | Unit price | Ext. | Stock / lead | Alternative |
|---|---|---|---|---|---|---|
| Leak-check fluid, Snoop 8 oz | Keep Supply (Swagelok distributor) MS-SNOOP-8OZ | 1 | 12.84 | 12.84 | In stock, ships today | McMaster 10875T22 9.02 |
| **Total** | | | | **12.84** | | |

### Notes on the picks

**A.** Nobody stocks a 150 to 250 mm KF-50 full nipple. Stock lengths are 139.7 to 140 mm (Lesker,
McMaster, A&N), 160 mm (Duniway) and 163.3 mm (MDC), then 317.5 to 320 mm, which is too long for the
~275 mm under the cone (`Z_JOINT_FACE - FLOOR_CLEARANCE_MIN`). Lesker's online nipple builder makes any
length and ships in about 10 days, but shows a price only after configuring, so it is not priced here. At
160 mm, option A holds 148 cm3 with the liner and puck (203 cm3 at the 200 mm in `params.py`). The KF-50
blanks are 5.08 mm thick, not 12 mm; the puck takes the heat, and Lesker's solid blank stub QF50-200-US
(25.4 mm, 36.90) is the thick option. All the stocked nipples are 304 or 304L; none is 316L.

**B.**
- The only 316L KF-50 weld stubs with a price are Lesker QF50-200-SSL (40.55, "KJLC will contact you", so
  not on the shelf) and A&N 4003138 (40.1 mm long, 58.00, stock not shown). 304L stubs are in stock:
  A&N 4000126 (25.00, 8 in stock), Lesker QF50-200-SST (29.35, bore matches 2 in x 0.065 in tube),
  McMaster 4518K38 (36.28). 304L welds to 316L with ER316L or ER309L, and nothing here needs 316L's
  corrosion resistance.
- Short stubs are 19.05 mm from the sealing face to the tube end (Lesker, MDC, McMaster, A&N); McMaster's
  STEP has 12.6 mm of straight tube after the flange taper. The top thermocouple's 12 mm band at
  `top - lip - 9` would straddle the stub-to-reducer weld. Put it on the reducer's 2 in end, or use a
  40 mm stub (Lesker QF50-200-LFT, 304L, 34.85; McMaster 4518K43, 51.49).
- The 2 x 3 in reducer is 101.6 mm long (4 in) at both McMaster and Wayland, not 64 mm. No vendor gives
  the straight ends, and McMaster's STEP is a plain cone. With `body_len` 250 the straight 3 in section
  drops from 153 to 121 mm and capacity from 770 to 694 cm3 bare (587 to 522 cm3 with liner and puck).
- 2-3/4 in x 0.049 in 304 tube isn't stocked; the pick is 0.065 in wall. The OD is still 69.85 mm in the
  72.9 mm bore; only the ID drops, from 67.4 to 66.5 mm. 2-1/2 in x 0.049 in is McMaster 11116N839, 28.75 per ft.
- Thermocouples: Auber TC-K-WS washer probes, junction rated 900 °C, fibreglass lead 316 °C continuous
  (482 °C peak), so keep the lead off the hot wall. McMaster's clamp-on (37045K532, 427 °C) and washer
  (5796N13, 482 °C) probes fall short of 500 °C, and no band-type probe rated to 500 °C has a public price.
  The McMaster 5415K worm-drive clamps have zinc-plated screws rated 250 °F (121 °C). Fine for the top,
  but use an all-stainless clamp at the bottom; none was priced.
- Auber SYL-2813AC: two type K inputs, one normally-open 3 A relay per channel, 85 to 260 VAC. It can
  switch the 30 to 120 VAC McMaster buzzer straight off mains.

**B with a tri-clamp cone joint.** The 316L short weld ferrule (14WMP) is 12.7 mm long, flange OD 63.91
mm, bore 47.50 mm, so it welds straight to the reducer's 2 in x 0.065 in end; the top thermocouple then
goes on the reducer. Sanitary clamps are pressure rated (McMaster 4322K153: 450 psi at 72 °F), so no
over-pressure ring is needed. Gaskets: FKM 5044K55 (−26 to 204 °C), PTFE 43315K55 (−73 to 260 °C),
silicone 4520K45 (−40 to 232 °C).

**C.**
- Nobody stocks a 100 x 5 mm fused-quartz tube. The nearest are MTI HQT100, 100 x 92 (4 mm wall) x 300 mm
  with one end closed (189.98, 17 in stock; cut off the closed end for two 110 mm pieces), MTI TQ4D650,
  100 x 94 x 650 (275.00, 3 left), and TGP 95x100, 2.5 mm wall (602.50 per 5 ft). Nobody publishes a
  price for cutting and grinding the ends (MTI doesn't cut; TGP and Wale charge extra).
- Thermal limits, fused quartz: TGP gives 1250 °C continuous, strain point 1120 °C. Heraeus HSQ 300
  gives 1150 °C continuous and 1300 °C short-term. No vendor gives a thermal-shock ΔT figure, only "exceptional".
- Thermal limits, borosilicate 3.3: Simax gives 500 °C short-term maximum and an ISO 718 thermal-shock ΔT of 136 K for a 5 mm wall.
  Simax and SCHOTT DURAN both say to stay under a 120 °C temperature difference.
- Borosilicate price: DURAN 100 x 5.0 is a standard size but has no public price. The comparison
  prices are McMaster 1176K29, 108 x 95.3 x 127 mm (82.73; at 108 mm OD it won't fit the 100 mm groove),
  and Wale BS-100C, 100 x 2.4 wall, a case of 3 x 5 ft (144.00).
- Glass seals: for the CAD's groove (8 mm wide, centred on the glass wall), an AS568-342 O-ring
  (91.44 x 5.33) sits under the wall. A -344 (97.79 ID) would sit on the groove's outer edge. Measure the real
  groove first (`MEASURE_FIRST`). Every elastomer found tops out at 204 to 232 °C, so the 304 sleeve and
  pan still have to keep shot off the seals.

## KF joints under overpressure

The chamber runs at +150 mbar gauge during a pour (1.16 bar absolute) and its relief valve opens at
+0.8 bar gauge (1.81 bar absolute). No vendor sells ISO-KF as a pressure joint. Most rate a standard
centring ring and clamp up to about atmosphere or 1.5 bar absolute; with an over-pressure ring or outer
ring the rating rises to 50 psi or more.

| Source | What it says |
|---|---|
| Kurt J. Lesker, [Flanges FAQ](https://www.lesker.com/newweb/flanges/FlangesFAQ.cfm) | "What is the maxmium internal pressure rating for vacuum flanges? Atmospheric. It is not recommended to expect vacuum flanges to hold pressure above atmospheric." |
| Lesker, [KF technical notes](https://www.lesker.com/newweb/flanges/flanges_technicalnotes_kf_1.cfm) | KF flanges are limited by the O-ring "to applications with temperatures between ~0° C and 120—180° C, and pressure from atmosphere to ~10-8 Torr or mbar." |
| Pfeiffer, [Vacuum Technology Know-how, 3.3.2.2 ISO-KF flange](https://www.pfeiffervacuum.com/global/en/knowledge/vacuum-technology/mechanical-components-in-vacuum/connections) | "suitable for pressures up to 1 · 10-8 hPa and can be used for overpressures up to 1,500 hPa." (Absolute or gauge isn't stated.) Metal seals need "special clamps for metal seals". |
| Edwards, [NW50 centring ring C10517395](https://global.my.edwardsvacuum.com/en/Catalog/Hardware-and-Fittings/Components-and-Fittings-ISO-KF/ISO-KF-Gaskets/ISO-KF-Centering-Ring-%2B-O-Ring-St-St-FKM/p/C10517395) | "Recommended Pressure Range Max 1.500 × 10⁵" Pa (1.5 bar absolute); components are "not intended to provide full structural support". |
| Leybold, [catalogue chapter Flanges and Fittings, 2025/02](https://www.leybold.com/content/dam/brands/leybold/downloads/catalogue-chapters-pdf/080_EN_Flange_Fittings.pdf), p. 10 | "Suitable up to pressures of 2.5 bar (36 psi) with inner centerring ring and clamping ring/quick clamping ring"; "5 bar (33 psi) with outside ring resp. ultra sealing ring and 3-part clamping ring" (units as printed). p. 6: "They have not been designed to support mechanical loads." |
| McMaster-Carr, [KF centring rings](https://www.mcmaster.com/products/kf-centering-rings/) | "To use fittings in pressure applications, buy a pressure-rated ring (sold separately)." Every standard KF-50 fitting, ring and clamp: "Not Rated". KF-50 ring with aluminium outer ring [4518K69](https://www.mcmaster.com/4518K69/): "50 psi @ 72° F". |
| A&N Corporation, [over-pressure rings](https://ancorp.com/product-category/iso-qf-lf-kf-nw-iso-k-flanges-fittings/hardware-seals/over-pressure-rings/) | They "prevent 'blow out' due to the presence of pressures greater than 1 standard atmosphere within a vacuum system"; the QF50 ring is rated 50 psig. |
| Lesker, [over-pressure rings](https://www.lesker.com/newweb/flanges/hardware_over_pressure_rings.cfm?pgid=0) | They "fit around the outside diameter of a QF Centerings Ring to help retain the oring if a system is exposed to a sudden burst of pressure." |
| MKS, [100316306](https://www.mks.com/p/100316306) | "Series 31 ISO-KF vacuum components are designed for use at subatmospheric pressure". |

What this means here:
- +150 mbar is inside every number above except Lesker's "atmospheric", MKS's "subatmospheric" and
  McMaster's "Not Rated", and
  the stock cup hung on this joint through every pour at that pressure.
- +0.8 bar (1.81 bar absolute) is above Pfeiffer's and Edwards' 1.5 bar for a standard ring. Only
  Leybold's 2.5 bar covers it.
- Internal pressure pushes the O-ring outward, and a standard centring ring has nothing outside it. At
  +0.8 bar the joint also carries about 260 N of separating force over the 64 mm O-ring circle (48 N at
  +150 mbar), and no vendor rates a standard KF-50 clamp for that.
- So every option's table includes an over-pressure ring (A&N QF50-200-OPR, 50 psig, 13.25) for the
  cone's existing joint, and option A has a second one for its bottom joint. A ring with an outer ring
  does the same job in one part: McMaster 4518K69, 50 psi, 43.30, outer ring 76.7 mm OD, so check that
  the clamp closes over it. So does Lesker QF50-200-SCV, a captured O-ring in an 8 mm outer ring, 14.00,
  but Lesker gives no pressure rating for it.
- With a tri-clamp cone joint, B needs no over-pressure ring.

## Seal temperature ratings found

| Seal | Rating (vendor's words or figures) | Source |
|---|---|---|
| FKM O-ring, KF-50 (AS568-330) | −26 to 210 °C | Lesker O-V330 part page |
| FKM in KF service | "the highest a FKM oring can be safely heated is 150C" (nitrile 100 °C) | Lesker Flanges FAQ |
| FKM | −15 to +150 °C (max. bakeout) | Leybold catalogue p. 9 |
| FKM centring ring | −10 to 150 °C ambient operation | Edwards C10517395 |
| FKM / silicone KF rings | 150 °C sustained, 200 °C intermittent | A&N O-ring page |
| FKM, SS ring / Al ring | 0 to 300 °F (149 °C) / 0 to 350 °F (177 °C) | McMaster 4518K65 / 5777N15 |
| FKM O-rings, cord, sheet | 0 to 400 °F (204 °C); cord 5 to 395 °F | McMaster |
| Silicone O-ring, KF-50 | −50 to 230 °C | Lesker O-S330 part page |
| Silicone KF ring | −50 to 390 °F (199 °C) | McMaster 4518K771 |
| Silicone cord / O-ring / sheet | −60 to 400 °F / −65 to 400 °F / −80 to 450 °F | McMaster |
| FFKM, Kalrez 4079 | 316 °C maximum continuous | [DuPont](https://www.dupont.com/products/kalrez-4079.html); Lesker's Kalrez KF-50 O-ring O-K330 is price on request |
| Aluminium KF gasket | −196 to +200 °C (ΔT max 2.5 °C/min) | Leybold catalogue p. 9; Edwards' NW50 aluminium metal seal C27159007 lists −10 to 150 °C and is quote only |
| KF parts overall | flanges bakeable to 150 °C; nipples and half nipples 200 °C | MDC part pages |
| Tri-clamp gaskets, 2 in | FKM −26 to 204 °C; PTFE −73 to 260 °C; silicone −40 to 232 °C (Brewers −50 to 230 °C); EPDM −34 to 149 °C | McMaster, Brewers Hardware |
| Butterfly valve seats, 2 in, 316 body | silicone −80 to 450 °F (232 °C); EPDM −20 to 300 °F (149 °C); FKM −20 to 400 °F (204 °C), all 145 psi; PTFE −40 to 450 °F (232 °C), 60 psi | McMaster 4820K23 / K117 / K63 / K136 |
| KF-50 ball valve seat | PTFE seat, FKM shaft seal, bakeable 100 °C | Lesker BVR0200MVQF |

`params.SEAL_LIMITS` has FKM at 200/250 °C and silicone at 200/230 °C. The KF vendors' own figures for FKM
are lower: 150 °C for bakeout and sustained use, 200 to 210 °C peak.

## Vendor dimensions that differ from `params.py`

All in mm. The full set, with sources, is in `vendor_dims.json` (`_vs_params` and one entry per part).

| `params.py` | Now | Vendors | Source |
|---|---:|---|---|
| `KF50.flange_od` | 75.0 | 74.93 (2.95 in) | every vendor; no change needed |
| `KF50.lip` (flange thickness at the hub) | 7.0 | 5.08 (0.200 in) | Lesker QF50-200-SB, MDC drawing, McMaster 4518K61 STEP, A&N |
| flange rim thickness at the OD | 4.6 (derived) | 2.9 | McMaster 4518K38 STEP |
| `KF50.hub_od` | 57.0 | ~58.6 (from rim 2.9, hub 5.08, 15°) | derived; the 15° taper itself matches |
| face recess for the centring ring | none | 52.3 dia x 2.6 deep | McMaster STEP; Lesker blank drawing |
| `KF50.ring_id` | 48.0 | 49.4 (Lesker) / 50.0 (McMaster, A&N) | |
| `KF50.ring_od` | 55.0 | ring body OD 51.9; the O-ring sits outside it on the centre rib | Lesker QF50-200-SRV drawing |
| `KF50.ring_thk` (axial) | 4.0 | ring body 7.98, seated in the 2.6 mm face recesses | McMaster 4518K65 STEP; Lesker SCV 8.0 |
| `KF50.oring_cs` | 5.0 | 5.33 (AS568-330: 53.34 ID, 64.0 OD) | Lesker, A&N; McMaster's model draws 6.2 |
| `KF50.clamp_od` | 96.0 | 82 (Lesker SS) / 87.4 (MDC Al) / 94.0 (McMaster and A&N Al) | over the wing nut: 112 to 122 |
| `KF50.clamp_w` | 24.0 | 20 (Lesker SS, chain) / 26.4 (McMaster Al) / 16 (A&N CNC SS) | |
| `A.nipple_len` | 200 | stock 140, 160, 163.3, 317.5 to 320 | no 200 or 250 mm in stock |
| `A.blank_t` | 12.0 | 5.08 | |
| `B.stub_len` | 25.0 | 19.05 (short) or 40.1 (long) | Lesker, MDC, McMaster, A&N |
| `B.reducer_len` | 64.0 | 101.6 | McMaster 5237K471 (STEP 101.600), Wayland 31W table |
| reducer straight ends (`tan_len` in `cad/parts.py`) | 8.0 | not stated | McMaster's STEP has none |
| `B.liner_wall` | 1.24 | 1.65 (0.065 in; 0.049 in isn't stocked at 2-3/4 in) | McMaster, OnlineMetals |
| `C.quartz_wall` | 5.0 | 4 (MTI), 3 (MTI), 2.5 (TGP, Wale); 5 is custom | |
| 2 in tri-clamp ferrule (B variant) | none | 12.7 long, flange OD 63.91, bore 47.50 | McMaster 50485K213 STEP |

These match `params.py`: the 15° taper, the 2 in x 0.065 in KF tube and nipple bore (47.5), the 3 in x
0.065 in body (76.2 x 1.65), the 1-3/4 in x 0.049 in A liner (44.45 x 1.24), and the 3-1/4, 3 and 2 in bar sizes.

## Not priced, or gaps

- No 200 or 250 mm KF-50 full nipple from any vendor checked. Lesker's nipple builder makes one but
  only prices after configuring.
- High-temperature KF-50 seals:
  - The only metal seal found is Edwards' NW50 aluminium seal C27159007, quote only. Pfeiffer says metal
    seals need special clamps. Lesker, MDC, McMaster, A&N and Duniway list none.
  - Lesker's Kalrez KF-50 O-ring O-K330 is price on request.
  - Ideal Vacuum's Kalrez 6375 KF-50 ring P106149 (425.44) and SS/FKM ring P101244 (17.54) come from search
    snippets only. idealvac.com and agilent.com returned 403 through the lab network, the runner and WebFetch.
- KF-50 to 2 in tri-clamp adapter: not found at McMaster, Duniway or A&N.
- Gauges and valves:
  - No KF-flanged dial gauge was found. MDC's Bourdon gauge on KF-50 (432013, −30 inHg to +30 psig) is
    quote only, as is MDC's KF-50 inline valve (320055).
  - Steel & O'Brien's 316L 2 in butterfly valve BFVPC-2 is quote only. No 2 in tri-clamp butterfly valve
    sold as 316L has a public price; McMaster's are "316".
- Tube, bar and fittings:
  - The reducer's straight-end length isn't published anywhere.
  - 2-3/4 in x 0.049 in 304 tube isn't stocked.
  - 2 in thick 316L plate wasn't looked up; the bar is cheaper for the spacer.
- Glass:
  - A 100 x 5 mm fused-quartz tube needs a custom quote, and cutting and grinding charges aren't published.
  - Borosilicate 100 x 5.0 has no public price.
- Thermocouples and clamps:
  - No band-type pipe-clamp thermocouple rated to 500 °C with a public price; washer probes under a
    clamp instead.
  - The all-stainless worm-drive clamps (stainless screws) didn't load on McMaster's page.
  - Omega, Inkbird and Red Lion 2-channel meters weren't priced.
- Pages that didn't help:
  - Glacier Stainless's domain doesn't resolve, and qsiquartz.com redirects to a site with no catalogue.
  - Duniway pages show no stock, wall thickness or ring material.
  - Speedy Metals and OnlineMetals show no cut fees.
- "KJLC will contact you" on a Lesker row means the part isn't on the shelf: QF50-200-SSL, QF50-200-OPR
  and QF50-200-NL.

## Re-running the lookups

```bash
pip install playwright beautifulsoup4 lxml "requests[socks]"   # uses the system Chrome if present
python bom/fetch_lesker_mdc.py          # Lesker tables (plain HTTP) and MDC part pages
python bom/fetch_kf_mcmaster.py         # McMaster KF-50 parts (price, stock, pressure rating) and Duniway
python bom/fetch_sanitary.py            # every sanitary, valve, gasket, filler and metal-stock row in the CSV
python bom/fetch_glass_tc.py            # quartz and borosilicate, seals, thermocouples, meter, buzzer, Snoop
```

`fetch_render.py` is the shared helper: headless Chrome through a SOCKS proxy on `127.0.0.1:1080`.
McMaster-Carr and Technical Glass Products block datacenter addresses, so these scripts need a tunnel
that exits from a normal network (`ssh -N -D 127.0.0.1:1080 <host>`); `fetch_render.py --direct` skips it.
The scripts print the current price lines to compare with `vendor-lookups.csv`; they don't rewrite it.
