### Navy copper alloys: rod and AWS A5.7 filler wire

This follows the first copper answer for vertical-cloud-lab/byu-vcl#286 (`../2026-10-17-copper-sourcing/`). It was run from [digital-alloy-lab#123](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/123), and the list also feeds the ONR YIP copper-nickel draft (#117). Prices and stock were read on 2026-10-17. Nothing was ordered and no quotes were requested.

All 141 listings are in `navy_copper_alloys.csv`. Each row gives the vendor, part number and link, diameter and tolerance, length or package, price, stock or lead time, cert, a quote-only flag, the specs the listing names, and how the page was read (browser, fetch or search snippet). Two columns are computed: `usd_per_unit` and `unit`, giving $/ft for bar and $/lb for wire.

**Headlines**
- **McMaster does sell 90/10 Cu-Ni rod. The first answer said it didn't, and that was wrong.** [4644N14](https://www.mcmaster.com/4644N14/) is 3/4" ±.003", ASTM B151, at **$130.26/ft**. That's $30/ft under Online Metals' $160.03, and it's the only Cu-Ni bar found with a stated tolerance. The listing sits in its own category ("Marine-Grade 90/10 Copper Nickel Rods"), which McMaster's copper-nickel search doesn't return. McMaster has no 70/30.
- **For 70/30 (C71500), Online Metals' $68.26/ft (first answer) is still the only posted price.** Hillman Brass & Copper lists 3/4" and 5/8" bar of both 70/30 and 90/10 as in stock, but quote-only.
- **Nothing on the Navy-specific cast and wrought list has a posted price** from 1/2" to 1": C95800, C63200, C95700, C96400, C96200, C61400 and C92200 are all quote-only or not found. The smallest C90300 found is 1", which ships at 1.031–1.041".
- **Filler:** McMaster has ERCuNiAl and ERCuAl-A2 at every size asked for, in packages from 1 lb. It also has ERCuSi-A at every size except 0.045" MIG, though Washington Alloy's ERCuSi-A at Cyberweld is cheaper. ERCuNi comes only in 10 lb TIG tubes, about $29–31/lb for Lincoln Techalloy 413 with a lot cert, or 30 lb MIG spools. **ERCuMnNiAl has no public price anywhere.** ERCuSn-A is sold only by Airgas, in 11 lb or larger packages.
- **Zinc:** C92200 and C90300 won't boil (about 15–25 mbar of Zn against the 200 mbar Ar fill). But C92200's 1–2 % Pb would end up as free lead in the powder, so **use C90300** if a tin bronze is wanted.

### Rod and bar, best option per alloy

"First answer" means the option was already priced in the first drop, and nothing better was found this time.

| Alloy | Best stocked option, 3/4" unless noted | Price | Dia. tol. | Notes |
|---|---|---|---|---|
| **C70600** 90-10 Cu-Ni | McMaster [4644N14](https://www.mcmaster.com/4644N14/) | $130.26 / 1 ft (about $168/kg) | ±.003" | **New.** O60 temper, lot cert downloadable after shipping. 1/2" is 4644N13 at $92.17/ft |
| **C71500** 70-30 Cu-Ni | Online Metals mp-00059837 (first answer) | $68.26 / 1 ft (about $88/kg) | not stated | Quote-only: [Hillman](https://hillmanbrass.com/product/100390732) CUNI715RD0750 (3/4") and RD0625 (5/8"), both "in stock"; [Wieland Diversified](https://www.wieland-diversified.com/copper-nickel/copper-nickel-c71500/) 0.75" to MIL-C-15726 and ASTM B151; Farmers Copper, Aviva, Busby. Goodfellow has only 12.7 mm, at $920 per 500 mm |
| **C96400** cast 70-30 | none priced | — | — | [Concast](https://www.concast.com/c96400.php) makes B505 solids from 1/2" to 9", quote-only, oversize allowance not stated |
| **C96200** cast 90-10 | none | — | — | No bar or rod from anyone; sold as castings only |
| **C95800** cast NAB | none priced | — | — | Quote-only: [Aviva](https://www.avivametals.com/collections/bronze-alloys/nickel-aluminum-bronze/c95800-alpha-nickel-aluminum-bronze), [Concast](https://www.concast.com/c95800.php) (1/2"–9", but not on its standard-stock list), [Anchor](https://www.anchorbronze.com/c95800). Atlas has it only as rectangle |
| **C63200** Navy NAB | none priced | — | — | Best lead: [Wieland Diversified](https://www.wieland-diversified.com/aluminum-bronze/aluminum-bronze-c63200/) lists 0.75" under "Stocked Alloys", to QQ-C-465, B150 and MIL-B-24059, quote-only. Aviva starts at 1". Farmers Copper, Anchor and Busby quote |
| **C63000** NAB | Atlas 3/4" × 12" (first answer) | $56.00, ships in 2–4 weeks (about $85/kg) | not stated | The only new option is Online Metals' eBay store, 0.75" × 72" for $414.52 ($69.09/ft plus $25.21 shipping) |
| **C95700** Mn-Ni-Al bronze | none | — | — | No bar stock and no quoting source found |
| **C61400** Al bronze | none priced | — | — | Farmers Copper and Anchor quote. McMaster doesn't sell 614; its nearest is 642 (C64200), [89195K41](https://www.mcmaster.com/89195K41/), 3/4" ±.004", $74.17/ft |
| **C95400** Al bronze | Atlas 3/4" × 12" (first answer) | $28.34 | oversize | Nothing cheaper found. Bunting's 3/4" × 13" bar (B954S000006-13) is $36.35 |
| **C65500** Si bronze | Online Metals (first answer) | $76.10 / 1 ft | not stated | Online Metals also lists 0.75" × 36" on Walmart for $122.09 ($40.70/ft), but out of stock and seen only in a search snippet |
| **C92200** "M" bronze | none priced | — | — | Concast (1/2"–9") and Aviva, both quote-only |
| **C90300** "G" bronze | 1" only: [Bunting B903S000008](https://catalog.buntingbearings.com/item/-font-color-black-continuous-cast-solid-bars-font-/-font-color-black-c90300-sae-620-font-bronze-bars/b903s000008) | price not shown | **ships 1.031–1.041"** | Marked as a stock item. Online Metals' 1" (mp-00034516) comes with an MTR, but its price couldn't be read. Nobody lists 3/4" or 5/8" |

**List-only alloys (zinc or beryllium):**
- C48500 leaded naval brass: McMaster [9105K25](https://www.mcmaster.com/9105K25/), 3/4" ±.002", $40.68/ft.
- C86300 manganese bronze, smallest round 1":
  - Atlas 1" × 12": $51.40.
  - McMaster [89225K52](https://www.mcmaster.com/89225K52/): $81.78/ft, ships 1.0525–1.0725".
- C17200 beryllium copper: McMaster [8940N3](https://www.mcmaster.com/8940N3/), 3/4" ±.003", $168.99/ft.
- Quote-only or not found: C48200, C86500 (Concast quote). C44300 and C68700 are tube alloys, with no US rod stock.

### Filler wire, best option per class

Prices are per package. Where a listing says "per lb", the minimum package is shown in brackets.

| Class (UNS) | TIG 1/16" | TIG 3/32" | TIG 1/8" | MIG 0.035" | MIG 0.045" |
|---|---|---|---|---|---|
| **ERCuNi** (C71581) | Lincoln Techalloy 413 at WeldingMart: $308.15 / 10 lb | Techalloy 413: $297.15 / 10 lb. By the lb at Gas and Supply: FM67 $35.60, Midalloy $37.48 (both 0 in stock) | Techalloy 413: $293.15 / 10 lb | Airgas only: Special Metals Monel 67 about $53/lb, Arcos 813 $1,759.80, both 30 lb spools | Airgas only: Monel 67 about $49/lb, 30 lb spool |
| **ERCuNiAl** (C63280) | McMaster [4683N11](https://www.mcmaster.com/4683N11/): $58.26 / 1 lb; 4683N14: $233.02 / 5 lb | 4683N12: $57.21 / 1 lb; 4683N15: $228.85 / 5 lb | 4683N13: $58.26 / 1 lb; 4683N16: $233.02 / 5 lb | McMaster [7678A753](https://www.mcmaster.com/7678A753/): $66.78 / 1 lb; 7678A755: $513.72 / 10 lb | 7678A754: $60.63 / 1 lb; 7678A756: $466.36 / 10 lb |
| **ERCuMnNiAl** (C63380) | Ampco-Trode 40, 10 lb, quote-only | same | same | not offered | Ampco-Trode 40, 30 lb, quote-only. Airgas lists Böhler UTP A34N only at .062" |
| **ERCuAl-A2** (C61800) | McMaster [7972A471](https://www.mcmaster.com/7972A471/): $35.89 / 1 lb; 7972A475: $134.59 / 5 lb | 7972A481: $35.44 / 1 lb; 7972A485: $132.90 / 5 lb | 7972A491: $34.00 / 1 lb; 7972A495: $127.50 / 5 lb | McMaster [7678A103](https://www.mcmaster.com/7678A103/): $35.33 / 1 lb; 7678A104: $95.65 / 3 lb; 7678A422: $289.85 / 11 lb | McMaster 7678A421: $69.04 / 1 lb. Blue Demon on eBay: $689.07 / 33 lb ($20.88/lb) |
| **ERCuSi-A** (C65600) | Washington Alloy at Cyberweld: $19.75 / 1 lb, $167.75 / 10 lb | $19.55 / 1 lb, $167.75 / 10 lb | $19.55 / 1 lb, $167.75 / 10 lb | Washington Alloy: $39.15 / 2 lb, $186.65 / 10 lb | Washington Alloy: $49.20 / 2 lb, $232.00 / 10 lb (McMaster has no 0.045") |
| **ERCuSn-A** (C51800) | Airgas, Böhler UTP A 32: about $59/lb, 11 lb tube | about $41/lb, 22 lb tube | about $81/lb, 22 lb box | none found | Airgas, UTP A 32: about $57/lb, 33 lb spool |

- **ERCuNi is not sold by McMaster.** Neither is ERCuMnNiAl or ERCuSn-A.
- **MIL-E-21562 RN67/EN67** is cited only on Airgas's Arcos 813 1/8" listing (AH2S813DP7). The 3/32" part carries a "MIL" suffix (AH2S813CP7MIL, $664.60 / 10 lb), but the cert it comes with isn't described.
- **Certs:**
  - Lincoln publishes a Q2 lot certificate online for Techalloy 413.
  - McMaster's filler listings make no cert statement, but its raw-material listings (rod, bar, bare wire) offer a lot-traceable cert from Order History.
  - No other filler listing says a certificate of conformance or test report ships with it. Ask for one with the PO.
- **UNS on the listings:** none of the ERCuNiAl or ERCuMnNiAl listings print a UNS. The only listing found with any UNS is CWI Gen 413 (ERCuNi, C71581), at a Canadian store. So C63280 and C63380 are still unconfirmed; check them on the certs.
- **Bare wire in the base alloys:**
  - C71500 and C70600: none with a price. California Fine Wire quotes "70-30" and "Alloy 90" (a 90-10 resistance alloy) fine wire, and Little Falls Alloys quotes only C71000 (80-20).
  - NAB: no wire anywhere.
  - C65500: wire is quote-only (Aviva, 1/16" up).
  - Phosphor bronze C51000, not ERCuSn-A's C51800, is at McMaster: [9668K53](https://www.mcmaster.com/9668K53/), 0.040", $17.62 per 1/4 lb, and 9668K73, 0.081", $30.91 per 1/4 lb.
  - C61400: none found. C92200 and C90300 are casting alloys, so there's no wire.

### Before melting any of the new alloys

- **Temperature.** By the same 50–80 °C superheat rule as the first answer:

  | Alloy | Liquidus | Pour |
  |---|---|---|
  | C96400 | 1238 °C | 1290–1320 °C, the same as C71500 |
  | C96200 | about 1150 °C | 1200–1230 °C |
  | C61400 | about 1050 °C | 1100–1130 °C |
  | C90300 | 1000 °C | 1050–1080 °C |
  | C95700 | about 990 °C | 1040–1070 °C |
  | C92200 | 988 °C | 1040–1070 °C |

  Liquidus values for C96400, C90300 and C92200 are from the Concast datasheets; the rest are from MakeItFrom.
- **Zinc in C92200 and C90300 is fine; the lead in C92200 isn't.**
  - Both alloys allow 3–5 % Zn. Pure Zn's vapour pressure at their pour temperatures is 3–4 bar.
  - Dissolved in copper, though, zinc's activity coefficient is only about 0.1. A [1968 Cu-Zn vapour-pressure study](https://www.doi.org/10.2473/SHIGENTOSOZAI1953.84.968_1663) gives 0.11 at 1200 °C, scaled here as a regular solution.
  - That puts Zn's partial pressure at **15–25 mbar, about a tenth of the 200 mbar Ar fill**. The same estimate gives 200–275 mbar for naval brass, which is why that one boils.
  - So expect some zinc fume on the viewport and filters, and check the powder's Zn by ICP, but these alloys won't boil.
  - The real problem with C92200 is its 1–2 % Pb. Lead doesn't dissolve in solid copper, so the powder would carry free lead particles, a respirable lead hazard. C90300 caps Pb at 0.30 %.
- **C96400 is a casting alloy.** It carries 0.5–1.5 % Nb and allows up to 0.15 % C, so carbon picked up from the graphite matters less against its spec than against C71500's.
- **Cast bar ships oversize.** These are the stated ranges:
  - C90300, Bunting 1": 1.031–1.041".
  - C86300, McMaster 1": 1.0525–1.0725".
  - C95400, McMaster's 3/4": up to about 0.895".
  - C96400 and C95800 at Concast: not stated, so ask for the actual OD with the quote.
- **Tariff.** Anchor Bronze's pages say a 50 % Section 232 tariff has applied to the copper content of copper products since 2025-08-01. That's worth a line in the #117 budget.

<details><summary>How this was read, and what to treat with care</summary>

- **How it was read.** Six research agents ran in parallel, using web search, page fetches and headless Chrome on the GitHub runner. One covered McMaster; the rest covered other vendors for Cu-Ni rod, NAB/MAB rod, Al/Si/Sn bronze rod plus the list-only alloys, Cu-Ni and NAB fillers, and Al/Si/Sn fillers.
- **McMaster part numbers were read from category tables, not product pages.** Each row sat under its product-family heading. This time every product page showed a login form, so unlike the first answer, the part numbers weren't checked one by one against their page titles. The 90/10 rods are in the category at `/products/marine-grade-90-10-copper-nickel-rods~~/`. McMaster doesn't show stock without a login.
- **Online Metals** was behind a Cloudflare check that blocked headless Chrome, headed Chrome under Xvfb, WebFetch and a text proxy. Its rows come from search snippets, marked `read_via = search snippet`.
- **Airgas** hides prices until a delivery ZIP is entered, so its rows are snippet prices. Airgas's own mirror sites disagree by up to about 60 % (for example UTP46189 at $57.18/lb against $91.00/lb). One row sourced only from Airgas's staging site was dropped.
- **Snippet prices can be stale.** Gas and Supply's live prices were about $8/lb above its snippets.
- **Mislabelled listings:**
  - WeldingMart's Lincoln ED036805 is titled "Aluminum MIG Wire", but its URL says SuperGlaze SiBR (ERCuSi-A).
  - Hillman's C715 pages carry a "C70600" heading.
  - WeldingMart and Airgas print Techalloy 413's class as "ERCrNi". All three need confirming when ordering.
- **Not reached:** Lincoln direct, Hobart, Forney, Home Depot, Lowe's and Amazon (for Al/Si/Sn filler), Admiralty Metals, Kloeckner, and Industrial Metal Supply's search. eBay item pages and Walmart blocked the runner.

</details>
