# Feedstock forms for alloy melts: cost per kg and trade-offs

Written for [issue #250](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/250) (alternatives to
machining cups and plugs). It compares the cost per kg of wire, powder, shot or pellets, and round bar for the
elements in the FLAIME aluminium campaign and the copper campaign (#117). It then compares two ways of dosing a
composition: UW-Madison's AlloyBot, which uses pellets plus wire, and ours, which fills machined 6063 cups with
powder.

**How the prices were gathered.** All prices were read on 2026-11-10. McMaster-Carr and Thermo Fisher (Alfa Aesar)
were read in a headed Chrome tunnelled through a lab Pi, because both sites need JavaScript. Those rows, with URLs,
are in [`prices.csv`](prices.csv). [`usd_per_kg.py`](usd_per_kg.py) recomputes USD/kg from pack size or from wire and
rod geometry. Other vendors were read with plain web fetches and are linked inline.

**Caveats.**
- These are small-lot list prices, before any university discount and without shipping or hazmat fees.
- Thermo Fisher's online promotion (about 15% off until 28 Dec 2026) is excluded; list prices are used.
- Quotes from partner companies are left out (see `CLAUDE.md`).

## Short answer

- **Grade matters far more than form.** For a given element, the big price step is between commodity metal and
  research-chemical catalogues (Lesker, Goodfellow, Alfa, Sigma). The step between wire, shot, powder and bar within
  one grade is much smaller.
  - **Al:**
    - Commodity forms: 6061/6063 bar and ER1100/ER4043 welding wire are $18–35/kg.
    - Research grades: 99.99% Lesker evaporation pellets are $1,200–1,400/kg, and 99+% 1 mm research wire is
      $355–760/kg.
    - LME aluminium was $3.15/kg on 9 Nov.
  - **Cu:**
    - Commodity forms: C110 bar, bare electrical wire, chops and casting grain are $31–43/kg.
    - Research grades: Lesker pellets are $760–1,100/kg and Alfa 99.9% wire is $148–181/kg.
    - LME copper was $14.03/kg.
- **Wire versus pellets in AlloyBot's own numbers.** SI Table S1 has wire at 3× (Ni) to 590× (Mg) the cost of
  pellets per unit volume, because it is short research reels. AlloyBot therefore doses pellets first and uses wire
  only for the last fraction of a percent.
- **Welding wire is the exception.** It is commodity wire in alloy compositions that sit almost on top of our
  targets:
  - ER1100, ER4043, ER4047 and ER5356 for Al, at $18–43/kg.
  - ERCuNiAl, whose composition ranges overlap C95800's, at $103–134/kg.
  - ERCuNi 70/30 at about $68/kg.
- **The balance metal sets the cost of a charge.** It is 70–95 wt% of our charges, and buying it as bar (our cups)
  is already the cheapest route. Pricing our charges at AlloyBot's pellet prices would make feedstock about 25–35×
  more expensive (see [cost per charge](#cost-per-charge)).
- **The additions are cheap whichever form we use**: a few dollars per charge. What matters for them is whether they
  dissolve below the induction module's ~1300 °C limit, and how much oxide they bring in. Master alloys solve both,
  and Belmont Metals sells most of the Al- and Cu-based ones we need online, in 1–20 lb units, at $18–86/kg.

## AlloyBot in brief

Selvaraj, Boonpetch, Dutta, Pek and Kube, *AlloyBot: On-Demand Synthesis of Bulk Alloys by Automatic Arc-Melting*,
Research Square preprint, 21 May 2026, [doi:10.21203/rs.3.rs-9761885/v1](https://doi.org/10.21203/rs.3.rs-9761885/v1)
(CC BY 4.0).

**Feedstock and dosing.**
- Each of 12 elements has a pellet dispenser and a wire dispenser.
  - Pellets are 3.175 mm evaporation pellets from Kurt J. Lesker. They are singulated by a rotating disk and
    approach the target mass without exceeding it.
  - Wire is 0.5–1.0 mm, from Lesker, Goodfellow and ESPI. It is cut to length to make up the remainder.
- A balance closes the loop, and a robot stacks each element's cup into a copper crucible.

**Melting.**
- A four-electrode arc melter with a load lock handles buttons of 1–5 cm³ (up to 25 cm³), with optional suction
  casting.
- Throughput is one alloy per hour, or more than 150 per week.

**Dosing resolution.**
- One pellet adds about 2.5 at.% to a 1 cm³ alloy, 0.5 at.% to 5 cm³, and 0.1 at.% to 25 cm³.
- A 2 mm piece of 1 mm wire adds about 0.03 at.% to 5 cm³.

**Cost.**
- Feedstock dominates: the median is about $103 per 5 cm³, with a 5th–95th percentile of $40–376.
- Letting the target volume float so that a costly length of wire becomes a whole pellet saves 12–39%. For
  Ti-6Al-4V, going from 5.00 to 5.07 cm³ cuts the cost from $85 to $58.

**What they avoid.**
- Table 1 sets the rule "avoid powders due to concerns of availability, cost, impurity pickup, containment, health,
  and safety".
- Si, Mn, Cr, Ce, La and Y have no wire listed ("No availability found").
- Master alloys "are often only available as granules of irregular size and shape" and are left for a future
  dispenser.

AlloyBot's SI Table S1, converted from USD per 5 cm³ to USD/kg:

| Element | Pellets, USD/kg | Wire, USD/kg | Wire ÷ pellets |
|---|---|---|---|
| Al | 1,407 | confidential quote | — |
| Cu | 1,094 | confidential quote | — |
| Mg | 1,841 | 1,086,766 | 590× |
| Si | 1,116 | none found | — |
| Zn | 812 | 78,515 | 97× |
| Mn | 472 | none found | — |
| Fe | 1,422 | 107,417 | 76× |
| Ni | 1,774 | 5,635 | 3× |
| Sn | 2,058 | 104,899 | 51× |
| Cr | 362 | none found | — |
| Ti | 2,530 | 29,694 | 12× |
| Zr | 2,055 | 74,387 | 36× |
| Ce | 10,487 | none found | — |

The SI's wire prices are Goodfellow short-reel prices, which is why they are so high. Advent and Alfa sell 1 mm
research wire on 50–500 m spools for roughly 1–2× the pellet price, for example Al 99.5% at $355/kg and Cu 99.9% at
$148–290/kg.

## USD/kg by form, for our elements

Each cell gives the cheapest public small-lot price found, plus a research-grade price where it differs a lot.
"Bought" marks what the lab has actually ordered.

| Element | Round bar | Wire | Shot / pellets / pieces | Powder | Master alloy (Belmont unless noted) |
|---|---|---|---|---|---|
| **Al** | 6061: 20–22 (McMaster, 1–2" × 6 ft) and 16.5 (Speedy, 2" × 6 ft). **6063, 3/4": 32–46 (bought, #152)** | ER1100: 17.6. ER4043: 22.5–29. ER5356: 22. ER4047: 30–39. **1100 Ø3.2 mm: 55 (bought, byu-vcl#8)**. 99+% 1 mm: 355–760 | 99.8% ingot: 13 (list price, #146). 99.7% granules: 43 (AEE). 99.9% shot: 61–127 (Alfa). 99.99% pellets: 1,199 (Lesker) | 99.9% 1–5 µm: 76 (AEE). Gas-atomized AlSi10Mg: 51–194 (**194 bought**) | — (Al is the carrier) |
| **Cu** | C110: 33–43 (McMaster, 1–2" × 6 ft). C101: 42 (Zoro). **630 bronze rod: 90 (bought, #219)**. C955: 46–48. C954: 32–43 | Bare 14 AWG: 30.8. ERCu: 56–80. Alfa 99.9% 1–1.5 mm: 148–181 | Chops or casting grain: 33. Alfa 99.9% shot: 97. Lesker 99.99% pellets: 758 | Thermo 99%: 75. AEE 99.9%: 134. Alfa: 232–285 | — (Cu is the carrier) |
| **Ni** | Alfa 99.5% Ø12.7 mm: 376 | ERNi-1: 84 (contains Ti). Alfa 0.5 mm: 3,297 | Luciteria shot: 85. Alfa shot: 235. Lesker: 1,416 | AEE 99.98%: 108 | Al-20Ni: 37. Al-50Ni: 41. Cu-50Ni shot: 70 |
| **Fe** | Alfa Ø7.6 mm: 2,477 | Advent 1 mm: 1,405. ER70S-6: 11 (contains Mn and Si) | Alfa pieces: 63. Lesker: 1,202 | AEE electrolytic: 111 | Al-10Fe: 19. Cu-30Fe shot: ~58 |
| **Mn** | — | not sold | Alfa pieces: 53–62. Lesker: 310 | Thermo 99.3% −325 mesh: 166. −40 mesh: 219 | Al-20Mn: 34. Al-60Mn: 58. Cu-30Mn: 47–86 |
| **Cr** | — | not sold | Lesker: 318. Alfa: 378–414 | AEE −100 mesh: 104. Alfa −325 mesh: 420 | Al-20Cr: 38. Cu-10Cr: 44. Cu-5Cr: 68 |
| **Si** | — | not sold | Alfa 98.4% lump: 53–63. Lesker: 368 | AEE −325 mesh: 64. **McMaster ~45 µm: 118 (bought)** | Al-12Si: 34. Cu-Si: 62–67 |
| **Mg** | — | AZ61A rod: 276 (alloy). Goodfellow reels only | Sigma chips: 279. Lesker: 1,552 | 86–93 (purity not stated). 99.9%: 2,580 | Al-50Mg: 56. Cu-20Mg: 67 |
| **Zn** | Alfa: 196 | 500 lb drum: 11.5. Alfa 1 mm: 2,946 | Ingot: 8. Alfa shot: 95 | AEE: 56 | — |
| **Sn** | Alfa: 310 | Advent 1 mm: 1,795 | Cut wire pieces: 86. Alfa shot: 208 | Alfa −325 mesh: 202 | not offered |
| **Ti** | Alfa 99.5%: 575 | ERTi-2: 282. Alfa 2 mm: 2,294 | Alfa sponge: 206. Lesker: 2,156 | AEE <20 µm: 277 | Al-10Ti: 21. Al-5Ti-1B: 20–58. Cu-30Ti: 43 |
| **Zr** | — | Advent Zr702: 13,333 | Lesker Zr702: 1,634 | AEE −20+60 mesh: 252 (export-restricted) | Al-10Zr: 60. Cu-50Zr: 70. Cu-33Zr: 76 |
| **Ce** | — | none | Alfa ingot under oil: 644–2,492 | ~680,000 (1 g) | Al-Ce: quote only |
| **Sc** | — | none | Lesker pieces: 58,500 | ~685,000 (1 g) | Al-2Sc: quote. USGS gives about $30/kg in bulk |

**Exchange references, USD/kg.**
- LME cash, 9 Nov 2026 ([Westmetall](https://www.westmetall.com/en/markdaten.php)): Al 3.15, Cu 14.03, Ni 16.19,
  Zn 3.75, Sn 46.35.
- China, 10 Nov 2026 ([Trading Economics](https://tradingeconomics.com/commodities)): Mg 2.42, Si 1.27.
- USGS MCS 2026: Zr sponge about 22.

**Sources for the table.**
- [Belmont Metals Al master alloys](https://www.belmontmetals.com/product-category/aluminum-master-alloys) and
  [Cu master alloys](https://www.belmontmetals.com/product-category/copper-master-alloys).
- [Atlantic Equipment Engineers / Micron Metals](https://micronmetals.com/) (AEE).
- [Kurt J. Lesker evaporation materials](https://www.lesker.com/newweb/deposition_materials/depositionmaterials_evaporationmaterials_1.cfm?pgid=al1)
  (budgetary prices).
- [Advent](https://advent-rm.com/en-GB/Products/Pure-Metals/Aluminium/Form/Wire/Line/AL5028) wire.
- Welding wire at [WeldingMart](https://weldingmart.com/) and [Canada Welding Supply](https://canadaweldingsupply.com/).
- [Rotometals](https://www.rotometals.com/) for Cu chops, Zn and Sn.
- [Speedy Metals](https://www.speedymetals.com/).
- [Nassau National Cable](https://nassaunationalcable.com/products/1000-14-awg-solid-bare-copper-conductor-soft-drawn-wire)
  for bare Cu wire.
- The lab's own orders: [byu-vcl#8](https://github.com/vertical-cloud-lab/byu-vcl/issues/8#issuecomment-3757060281),
  [#152](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/152#issuecomment-6353385667),
  [#219](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/219#issuecomment-6509252104) and the quotes
  in [#146](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146#issuecomment-6353382512).

**Thermo Fisher hides many reactive powders.** It shows no online price for Al, Mg, Ni, Fe, Ti, Zn or Zr powder
("Contact Us"); Zr powder ships wet. AEE ships Ti and Zr as hazmat classes 4.2 and 4.1. For 1-lb lots, freight and
hazmat fees can exceed the cost of the powder.

## What we have bought

From the issue threads; partner companies excluded.

**Bought:**
- 1100 Al wire, Ø3.2 mm, 1 lb, $25.18 (byu-vcl#8).
- Si powder, ~45 µm, 1 lb, $53.58 (McMaster).
- AlSi10Mg powder, 15–45 µm, 1 kg, $193.95 (MSE Supplies).
- 50 g of 99.99% Si, 100–200 mesh (Thermo).
- 3/4" 6063-T52 rod for the cups (McMaster 1640T16; $60.14 list per 8 ft, about $32/kg).
- 3 ft of 3/4" C63000 bronze rod for the copper runs ($174.50, about $90/kg).

**Ordered, not yet arrived:** the elemental-powder order from August (presumably the ESPI one; quotes in #146) ships Nov 12.
The matching Thermo order expired unplaced.

**Never bought:** no master alloy has been bought or quoted.

**Quoted in #146, USD/kg:**
- ESPI: Mn 350, Cr 650, Zn 450, Sn 400, Ti 650, Sc 235,000, Er 32,000.
- Thermo, for 50–250 g packs: Si 1,060, Fe 488, Ni 689, Cu 578, Cr 8,500.

Lab-pack powder in 50–250 g lots typically costs 4–17× the 1–2 lb AEE price for the same element, and up to 80× for Cr.

## Cost per charge

The script is [`melt_cost.py`](melt_cost.py). Charge sizes follow the records: Al runs are planned at 250–350 g,
from 3–5 dosed cups topped up with 6063 rod, and the Cu runs were 858–1,080 g. Costs are feedstock only, with no
machining labour, shipping or hazmat fees.

| Charge | Pellets at AlloyBot SI prices | Cups from bar + powders (today) | Sawn bar + master alloys (no cups) | Off-the-shelf near-target feedstock |
|---|---|---|---|---|
| Al-3Mn-1Cr-1Zr, 300 g | $412 | $11.7 | $10.9 | — |
| C95800 NAB, 1,000 g | $1,158 | $45.8 † | $42.3 | ERCuNiAl wire: $103–134. C955 rod (Cu-11Al-4Fe-4Ni): $46–48 |
| C71500 Cu-30Ni, 1,000 g | $1,298 | $56.2 † | $55.6 | ERCuNi wire: about $68. 3/4" C71500 bar: about $88 |

† The cup's capacity limits these. A 6063 cup and plug weighs 38.7 g and holds about 8.8 g of powder, which is at
most 18.6 wt% even with Al powder. C95800 needs 18.7 wt% of additions and C71500 needs 30 wt%. In a copper cup of
the same size the wall weighs about 3.3× as much. Neither alloy can be made in a single standard cup.

### Inputs to `melt_cost.py`

| Route | Balance metal, USD/kg | Additions, USD/kg |
|---|---|---|
| Pellets | Lesker pellets, SI Table S1: Al 1,407, Cu 1,094 | SI Table S1: Mn 472, Cr 362, Zr 2,055, Ni 1,774, Fe 1,422 |
| Cups from bar + powders | 6063 rod as bought, 32; C110 rod, 34 | Mn 166 (Thermo), Cr 104, Zr 252, Ni 108, Fe 111, Al powder 76 (all AEE) |
| Sawn bar + master alloys | 6063, 32; C110, 34 | Al-60Mn 58, Al-20Cr 38, Al-10Zr 60, Cu-50Ni 70, Cu-30Fe 58, Cu-30Mn 86 (Belmont). Al in NAB added as 6063 pieces, 32 |

**Machining is the real cost of cups.** On the records:
- Each 58.4 g blank loses about 20 g to chips.
- One cup-and-plug set was estimated at about 40 min; it has never been timed.
- The press fit runs near the wall's yield point, and the Oct 19 plugs came out undersize
  ([#179](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/179#issuecomment-6537833653),
  [#156](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/156#issuecomment-6353390000)).

At 3–5 cups per Al charge, that is 2–3.5 hours of machining for about $11 of metal.

## AlloyBot's pellets and wire vs. our cups and powders

| | AlloyBot (pellets + wire, arc melting) | Ours (6063 cups + powders, induction crucible) |
|---|---|---|
| Scale | 1–25 cm³, i.e. 3–67 g of Al or 9–224 g of Cu | 250–350 g of Al and about 1 kg of Cu per run |
| Balance metal | Lesker pellets at $760–1,560/kg | Bar at $20–46/kg, about 20–45× cheaper |
| Dosing resolution | Fine wire is needed because the buttons are small | One 3 mm pellet is at most about 0.06 wt% of a 300 g charge, so shot alone is fine and wire adds little |
| Preparation labour | None: everything comes in dispense-ready forms | About 40 min of machining per cup-and-plug set, with ~35% of each blank lost to chips |
| Automation | Fully automatic: pellet singulator, wire cutter, balance, robot | The powder doser is automated and accurate (6.5676 g against a 6.5674 g target), but cups are machined and plugs pressed by hand |
| Purity and oxygen | High: low-surface-area pellets and wire. O from the feedstock certificates is 220–940 ppmw (SI Table S2); measured values are higher but typical of arc melting | Fine powder carries oxide. The AlSi10Mg core failed to melt in, with Mg oxide skins suspected; the 4047 core melted |
| Elements with no wire | Si, Mn, Cr, Ce, La, Y are pellets only; master alloys are deferred | Powders exist for all of them; Ce, Sc and Er are costly and pyrophoric |
| Dissolution of high-melting additions | Arc temperatures melt everything (Zr, Ti, Cr, W) | Below the ~1300 °C induction limit, Zr, Cr, Ti, Fe, Mn and Si dissolve rather than melt. AMAZEMET's engineer advised master alloys, because loose powder sinters but won't melt in until part of the charge is molten |
| Volatile elements | Mg, Zn and Al evaporate under the arc, so they built a vapour-containment lid | Induction is gentler, but Mg burns off above about 700 °C |
| Composition range | Any composition the dispensers can reach | The cup sets the ceiling (≤18.6 wt% additions) and the floor (the 6063 always brings its 0.2–0.6 Si, 0.45–0.9 Mg and ≤0.35 Fe) |
| Safety | No powder handling | Flammable fine powders such as Al, Mg, Ti and Zr need dust control and hazmat shipping |
| Output | A bulk button or suction-cast rod | Powder: the product itself, and a feedstock for later charges |

**Making our own powder is a real advantage.**
- What the atomizer makes can be fed back in:
  - Off-size fractions and crucible leftovers can be remelted.
  - In-house 4047 powder was put back in a cup and re-atomized on Oct 2
    ([#157](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/157#issuecomment-6353391236)).
  - A master alloy can be atomized once and its powder used as a dosing feedstock for a whole campaign.
- AlloyBot has no way to reuse output, because its output is a button.
- Two cautions:
  - Every pass adds oxide, and oxygen pickup per pass hasn't been measured.
  - The 914 g of oversize and leftover Cu from #219 hasn't been reused yet.

## Alternatives to machining cups and plugs

Most promising first.

1. **Sawn bar plus master-alloy pieces, with no cup.**
   - The balance is sawn 6063 (or C101/C110), and the additions are Belmont master alloys: Al-10Zr, Al-20Cr,
     Al-20/60Mn, Al-10Fe, Al-20/50Ni, Al-10Ti, Al-50Mg and Al-12Si; Cu-50Ni, Cu-30Fe, Cu-30Mn, Cu-10Cr, Cu-Si and
     Cu-Zr.
   - These melt or dissolve below 1300 °C and need no containment, which is what AMAZEMET's engineer recommended.
   - Feedstock cost is the same as cups (see above), and the machining step disappears.
   - **Gaps:** Al-Cu, Cu-Al, Al-Ce and Al-Sc are quote-only (Milward, Chinese suppliers), and dilute masters take up
     a large share of a small charge. Sc, Ce and Er stay elemental, or come from an arc-melted master made in house.
2. **Welding wire as a near-target base.**
   - Al: ER1100, ER4043, ER4047, ER5356 and ER2319 cover Al-Si, Al-Mg and Al-Cu bases at $18–70/kg.
   - Cu: ERCuNiAl overlaps C95800's composition ranges, and ERCuNi is 70/30 Cu-Ni.
   - The wire can be coiled into the crucible, or cut and weighed like AlloyBot's.
   - AMAZEMET's plasma module also feeds 1.2–2.4 mm wire continuously.
   - The first BYU proof of concept already used cut 1100 wire.
3. **Commodity shot or chops for the balance, poured into the crucible.**
   - Options: Cu chops or casting grain at about $33/kg, Zn ingot at $8/kg, 99.8% Al ingot at about $13/kg, or Al
     granules at $43/kg.
   - This works with additions that are solid pieces. Loose powders are still the problem.
4. **Near-composition bar plus a small trim.**
   - C955 rod ($46–48/kg) is one example; then add Mn and adjust Al.
   - This minimises how much has to dissolve.
5. **Easier containers, if powder must stay.**
   - 6063 tube cut to length: about break-even at today's cup size
     ([byu-vcl#277](https://github.com/vertical-cloud-lab/byu-vcl/pull/277#issuecomment-6534631992)).
   - Al or Cu foil packets, as used in arc melting.
   - Thin-wall cups, holding up to about 37 wt% powder.
   - Sand-cast cups are dirtier, and pressed or CIP compacts were judged unreliable
     ([#179](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/179#issuecomment-6647463028)).
6. **Pellets plus wire as AlloyBot does it.** This is worth copying only for the dispensing hardware, for minor
   additions at scale. At our charge sizes the evaporation-grade pellet price makes it the most expensive route by
   far.

## Open items

- **Google Scholar.** The xref (`citation_for_view=f_fp_OTzKREC:aqlVkmm33-oC`) could not be opened: Scholar showed a
  CAPTCHA through the Pi and returned 403 from elsewhere. In OpenAlex, AlloyBot is that author's newest primary
  paper, so the link is most likely the same preprint.
- **Prices not found publicly:** 1100/1050 bar, C10200, C95800 bar, and the Al-Cu, Cu-Al, Al-Ce and Al-Sc master
  alloys. Ask Belmont or Milward for a quote.
- **Belmont pack weights:** some pages conflict on piece weight (Cu-30Mn) or leave it out (Cu-30Fe, Al-50Si), so
  those USD/kg figures are approximate.
