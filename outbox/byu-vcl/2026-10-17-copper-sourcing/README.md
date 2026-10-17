### Copper alloys and high-purity Cu rod for the atomizer (#286)

Run from [digital-alloy-lab#123](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/123) while this repo is out of credits. Prices and stock were read on 2026-10-17. The Pi isn't reachable from that repo, so McMaster was read with headless Chrome on the GitHub runner. Its category tables loaded without a login, and so did the product pages after one early login prompt. Every McMaster part number below matches its page title.

**Size: 3/4" round, same as the 6063 bar** ([1640T16](https://www.mcmaster.com/1640T16/)). Cups (2.750" long, 1/2" drill 2.25" deep) and plugs are made the same way, with each plug turned from the same bar as its cup. A cup and plug take about 3.5" of bar, so 1 ft makes three. 5/8" is the fallback if 3/4" won't get past the sealing rod's adapter.

**Mass is what changes.** A 3/4" × 2.75" slug is 19.9 cm³. That is 54 g in 6063, about 150 g in the aluminum bronzes, and 170–178 g in copper, CuNi and silicon bronze. Two slugs come to 300–360 g, inside the 400–500 g charges in published rePowder work.

### Order

**McMaster, one PO** (it doesn't show stock status without a login):

| | Alloy | Part | Dia. tol. | Price |
|---|---|---|---|---|
| **High-purity Cu** | 101 (C10100, oxygen-free), 99.99 % Cu, ASTM B187 | [8965K72](https://www.mcmaster.com/8965K72/) 3/4" | ±.004" | $101.26 / 2 ft ($69.92 / 1 ft) |
| **Nickel-aluminum bronze** | 630 (C63000), ASTM B150 | [8203K41](https://www.mcmaster.com/8203K41/) 3/4" | ±.004" | $75.22 / 1 ft |
| **Aluminum bronze** | 954 (C95400), ASTM B505, cast | [8958K61](https://www.mcmaster.com/8958K61/) 5/8" nominal, arrives 0.68–0.77" | +.053 to +.145" | $38.46 / 13" |
| **Silicon bronze** | 655 (C65500), ASTM B98 | [89575K23](https://www.mcmaster.com/89575K23/) 3/4" | ±.004" | $88.64 / 1 ft |

That's $303.58. McMaster lets you download each lot's material certificate from Order History after it ships.

**Copper-nickel, which McMaster doesn't stock as rod** (it only has MIL-T-16420 CuNi pipe). Both are on Online Metals, sold by Southern Copper:

| | Alloy | Listing | Price | Ships |
|---|---|---|---|---|
| **70/30 CuNi** | C71500 | [0.75" OD, mp-00059837](https://www.onlinemetals.com/en/buy/copper/0-75-inch-od-copper-nickel-round-bar-715/pid/mp-00059837) | $68.26 / 1 ft, mill test report available | 1 business day, from Pelham, AL |
| **90/10 CuNi** | C70600 | [3/4", mp-00068382](https://www.onlinemetals.com/en/buy/3-4-inch-copper-nickel-round-bar-c706/pid/mp-00068382) | $160.03 / 1 ft (5/8" is $142.30) | 2 business days |

Neither listing gives a diameter tolerance, so mic them when they arrive. The runner was shown a Cloudflare check on the 90/10 page, so that price was read through a text proxy and not in a browser.

**C95800, the cast NAB used for propellers, isn't stocked at 3/4" anywhere I found.** [Concast](https://www.concast.com/c95800.php) and [Anchor Bronze](https://anchorbronze.com/c95800) quote it. The McMaster 630 above is the in-stock stand-in from the same family. McMaster's nearest cast NAB is 955, in 1" only ([3588N11](https://www.mcmaster.com/3588N11/), $100.09 / 1 ft).

### Higher purity than 101

C10100 is already a 99.99 % spec. A lab supplier only buys you a fifth or sixth nine:

| Purity | Source | Size | Price | Note |
|---|---|---|---|---|
| 99.99 % | McMaster 101, above | 3/4" ±.004" | $69.92 / 1 ft | Cheapest high-purity option that fits |
| 99.999 % | [Thermo Scientific Puratronic 012754.DT](https://www.thermofisher.com/order/catalog/product/012754.DT) | Ø19 mm | $928.65 / 250 mm | Tolerance not stated |
| 99.99 % | [Goodfellow](https://www.goodfellow.com/usa/copper-rod-1000052020) | Ø19 mm ±5 % | $1,230 / 300 mm | In stock, dispatched within 48 h. ±5 % keeps it ≤19.95 mm |
| 99.9995 % | [Advent Research Materials CU5095](https://www.advent-rm.com/en-gb/products/pure-metals/copper/form/rod/line/cu5095) (UK) | Ø20 mm | $412 / 50 mm, $649 / 100 mm, $1,154 / 250 mm | Tolerance not stated, so may need turning |
| 5N, 6N | [ESPI Metals](https://shop.espimetals.com/elements/elements-copper?form=245): Knc2447 (5N), Knc3886 (6N) | 0.750" | Quote, sold by the inch | Only 3/4" 5N/6N found |

### Why these alloys (Navy)

1. **70/30 CuNi (C71500)** is used for seawater piping and heat exchangers, and is preferred on submarines. In Feb 2026 NAVSEA posted draft AM specs for it, including **MIL-PRF-XX758, 70-30 CuNi powder feedstock for LPBF**. I read the notice on [an aggregator of SAM.gov posts](https://fundinglandscape.com/opportunity/cmlaf9dzy003gjm04dmr0k5ci), not on SAM.gov itself. In Sep 2025, Velo3D and Linde AMT agreed to supply US-made 70-30 CuNi powder for the Navy ([ASM](https://www.asminternational.org/linde-advanced-material-technologies-and-velo3d-advance-u-s-navy-shipbuilding-with-fully-domestic-additive-manufacturing-supply-chain/)). In 2026 an LPBF CuNi valve body passed production-level testing for the submarine fleet ([VoxelMatters](https://www.voxelmatters.com/vacco-delivers-additively-manufactured-valve-for-u-s-navy-submarine-fleet/)). **It's the most relevant powder target here.**
2. **Cast NAB (C95800)** is used for propellers, valve bodies and pump bodies (MIL-B-24480). A draft MIL-PRF-XX750 covers wire-arc NAB ([notice](https://fundinglandscape.com/opportunity/cmlaf9f10003tjm04hu154s4m)), and NSWC Carderock reviewed NAB AM in 2021 ([DTIC AD1147115](https://apps.dtic.mil/sti/trecms/pdf/AD1147115.pdf)). Wrought C63000/C63200 covers shafts and fasteners.
3. **90/10 CuNi (C70600)** is the most widely used seawater piping and condenser alloy (MIL-T-16420).
4. **Lower priority:** C95400 aluminum bronze (MIL-B-16033), C65500 silicon bronze (marine fasteners), C46400 naval brass and C86300 manganese bronze (marine hardware).

### Before melting any of it

- **Temperature.** With Indutherm's 50–80 °C superheat rule (#232):
  - Cu: about 1135–1165 °C
  - NAB: about 1105–1140 °C
  - 90/10 CuNi: about 1200–1230 °C
  - 70/30 CuNi: about 1290–1320 °C (its liquidus is 1240 °C)

  Ask AMAZEMET for the induction module's ceiling before running 70/30.
- **Skip naval brass and manganese bronze.** They are 25–40 % Zn, and Zn boils at 907 °C, below their pour temperatures. By my rough estimate, Zn's partial pressure over molten naval brass is at or above the 200 mbar Ar fill. It will boil off, coat the viewport and filters, and shift the composition. Manganese bronze is not far behind. If AMAZEMET says it's fine, McMaster's 464 is [8970K59](https://www.mcmaster.com/8970K59/) ($74.65 / 1 ft).
- **Don't atomize beryllium copper.** Its powder is a respirable Be hazard. McMaster stocks 3/4" C17200 ([8940N3](https://www.mcmaster.com/8940N3/)), but leave it out.
- **Cast bar is oversize.** ASTM B505 bar (954, 955, 863) comes .05–.15" over nominal:
  - McMaster's 3/4" 954 ([8958K62](https://www.mcmaster.com/8958K62/)) is 0.80–0.90" (20.4–22.7 mm) and would have to be turned to .750". That's why the 5/8" is in the order above.
  - ToughMet ([5445N12](https://www.mcmaster.com/5445N12/)) is 0 to +.040", so up to 20.07 mm.
- **Use 101, not 110.** 110 (C11000, [8966K11](https://www.mcmaster.com/8966K11/), $43.59 / 1 ft) carries 0.02–0.04 % oxygen, which the graphite turns into CO. McMaster sells 101 as the copper with no oxygen to outgas.
- **Carbon in CuNi.** Nickel dissolves carbon and copper barely does, so 70/30 is the alloy most likely to pick up carbon from the graphite. CuNi specs cap C at about 0.05 %. Ask AMAZEMET whether they melt it in graphite or use a liner.
- **Pour pressure.** Copper's surface tension is about 1.3 N/m, against about 0.9 N/m for Al. That raises 2γ/r at the Ø0.7 mm nozzle to about 75 mbar, from about 50 mbar for Al.

<details><summary>More sources, and how this was found</summary>

**Cheaper or alternate listings.**
- Online Metals:
  - [630, 3/4"](https://www.onlinemetals.com/en/buy/bronze/0-75-nickel-aluminum-bronze-round-bar-630/pid/13960): $70.73 / 1 ft
  - [655, 3/4"](https://www.onlinemetals.com/en/buy/bronze/0-75-silicon-bronze-round-bar-655-h04/pid/7823): $76.10 / 1 ft
  - [464, 3/4"](https://www.onlinemetals.com/buy/0-75-brass-round-bar-464-h02-extruded/pid/13445): $53.39 / 1 ft
  - [101 copper, 3/4"](https://www.onlinemetals.com/en/buy/copper/0-75-copper-round-bar-101-h04/pid/7146): about $87.89 / 1 ft. That figure is from a search snippet, because the site blocked the runner.
- Atlas Bronze:
  - [C95400, 3/4" × 12"](https://www.atlasbronze.com/C95400-Solid-Bar-3-4-ODx12-L-p/9540s-6-96.htm): $28.34, ships in 2–3 business days. It's continuous cast, so expect it oversize and plan to turn it.
  - [C63000, 3/4" × 12"](https://www.atlasbronze.com/C63000-Solid-Round-Bar-3-4-OD-x-12-L-p/6300s-6-96.htm): $56.00, but ships in 2–4 weeks.
- Speedy Metals: [954, 3/4"](https://www.speedymetals.com/p-1985-34-rd-ca-954-aluminum-bronze.aspx), $34.38 / 1 ft, about 1/16" oversize.
- Goodfellow: [OFHC, 99.95 %, Ø19 mm](https://www.goodfellow.com/usa/ofhc-copper-rod-1000069742), $590 / 300 mm. That's both pricier and less pure than McMaster 101.

**Quote only:**
- C71500 and C70600: [Farmers Copper](https://www.farmerscopper.com/copper-nickel-715-c715-c71500.html) (C71500 round from 1/2", ASTM B151 and MIL-C-15726) and [Busby Metals](https://busbymetals.com/products/copper-silicon-copper-nickel-copper-nickel-silicon/c71500/)
- C63200: [Busby Metals](https://busbymetals.com/products/nickel-aluminum-bronze/63200) and [Anchor Bronze](https://anchorbronze.com/c63200)
- C72900: Concast

**Blocked or not reached.** Aviva Metals, Midwest Steel & Aluminum and National Bronze blocked the fetches. Kurt J. Lesker, Surepure, Princeton Scientific and MSE Supplies weren't checked.

**Method.**
- McMaster: headless Chrome on the GitHub runner read the category pages (`/products/101-copper-rods/`, `/products/aluminum-bronze-rods/` and so on). Every 1/2"–1" row from the families checked is in [`mcmaster_copper_rods.csv`](mcmaster_copper_rods.csv), with prices by length.
- Other vendors: web search and page fetches. Atlas Bronze and the 70/30 Online Metals page were also checked in Chrome.
- Navy uses and specs: CDA, Concast datasheets, EverySpec, DTIC and trade press. Liquidus values are from Concast and MakeItFrom, because copper.org blocked the fetch.

</details>
