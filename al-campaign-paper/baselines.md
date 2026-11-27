# Sc-free commercial baselines: EOS Al5X1 and Höganäs Al-HS1, printed and tested in-house

*Draft of 2026-11-27 for [#277](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/277#issuecomment-7228308921).
Nothing was ordered, and no vendor was contacted. Prices and lead times are not published by either vendor;
the planning numbers below are assumptions to replace with quotes.*

## Why these two, and which one first

Vendor datasheets already list scandium-free LPBF aluminum stronger than AlSi10Mg ([`risks.md`](risks.md), R1).
Sterling asked (2026-11-27) to make EOS Al5X1 (Al-Mg-Zr-Mn) and Höganäs Al-HS1 (Al-Mn-Cr-Zr), or at least one of
them, baselines on the Pareto front the campaign tries to expand, measured in-house the same way as the
candidates, AlSi10Mg and Scalmalloy.

| | EOS Aluminium Al5X1 | Höganäs forAM Al-HS1 GA |
|---|---|---|
| Composition (wt %) | Mg 2.5-4.2, Zr 0.6-1.8, Mn 0.1-1.0 (Fe, Si, Ti each ≤ 1.0) [1] | Mn 4.8, Cr 0.8, Zr 0.8, typical; no ranges given [2] |
| Datasheet yield / UTS / elongation, as built | V 240 / 310 / 23; H 260 / 310 / 23 [1] | Z 220 / 280 / 25; XY 220 / 285 / 25 [2] |
| After the vendor's direct age | 400 °C 6 h, gas quench: V 380 / 415 / 14.5; H 385 / 415 / 14.5 [1] | 375 °C 4 h in air: Z 355 / 420 / 16; XY 370 / 440 / 12 (6 h: 350-365 / 430-445 / 11-13) [2] |
| Datasheet basis | EOS M 290, 40 µm, ASTM E8; EOS "Core" product (TRL 3-5) [1] | Machined bars from printed cylinders; machine not stated [2] |
| B_NIR, import-weighted (wt %) | 3.06-4.20 at the range midpoints; 1.98-5.65 across the whole range | 5.43-5.63 |
| Compared with Scalmalloy (4.74-5.98), same import reliances for both | **Below at every allowed reliance** (difference −2.01 to −1.45), and below at every corner of its composition range | **Not clearly below** (difference −0.48 to +0.82: below only if Mg's reliance is near 100 %) |
| B_mass (wt % of listed elements) / B_cost (USD per kg of alloy) | 5.10 / 0.52 | 6.40 / 0.45 (Scalmalloy: 6.21 / 39.9) |
| On the Sc-free front (best datasheet yield vs B_NIR)? | **Yes**, between Al-Fe-Mg-Zr (376 MPa, 1.02 wt %) and EOS Al2139 T4 (460 MPa, 3.89 wt %) | **No**: Al5X1 is stronger at lower burden, and Al-Fe-Mg-Zr at much lower burden |

Burdens are from [`scripts/mineral_burden.py`](scripts/mineral_burden.py) on the rows added to
[`data/alloys.csv`](data/alloys.csv). "Same import reliances for both" is the paired comparison described under
[the metric to freeze](#the-burden-metric-to-freeze-before-the-screen-ranks-anything).

**Recommendation: buy Al5X1 first; add Al-HS1 if the budget allows.**

- **Al5X1 defines the front.** It is the strongest Sc-free commercial alloy on the datasheets in the region the
  campaign targets: it beats AlSi10Mg's as-built datasheet yield by about 80-150 MPa, and its burden is below Scalmalloy's under every
  allowed import reliance. A candidate that doesn't beat in-house Al5X1 at equal or lower burden hasn't expanded the
  front.
- **Al-HS1 is behind the front, but still useful.**
  - It is the commercial member of the Al-Mn-Cr-Zr family that seeds S1 and O3 come from.
  - Its datasheet claims about 200 MPa at 250 °C [3], which matters if the paper later claims hot strength (FLAIME O4).
  - Its burden is about Scalmalloy's, so measuring it shows what 4.8 wt % Mn costs.
  - If only one powder can be bought, it should be Al5X1.
- **There is a gap at the low-burden end.** Below Al5X1's burden (about 3 wt %), the only Sc-free points are a
  datasheet (Aheadd CP1, Al-Fe-Zr, 300 MPa aged, B_NIR 0.14) and a paper (Al-1.87Fe-1.02Mg-1.03Zr, 376 MPa aged,
  B_NIR 1.02).
  - B_NIR steers the screen toward Fe- and Zr-lean compositions. An in-house front of only Al5X1, Al-HS1 and
    Scalmalloy would let a low-burden replication of those alloys "expand the front".
  - So the claim also has to be checked against those reported values (pre-registration §4).
  - A third purchase, Aheadd CP1 (EOS store article 9030-0034, also "Contact sales" [4]), would anchor that end
    in-house. Decide this with the screen.

## Sourcing (public pages, read through the lab's network on 2026-11-27)

Neither vendor publishes a price, a lead time or a minimum order. Both route every request to sales.

| | EOS Aluminium Al5X1 | Höganäs forAM Al-HS1 GA 20-63 µm |
|---|---|---|
| Where it's sold | EOS online store, article **9030-0017**: price shown as €0.00 with "Contact sales" [4]. All 41 metal powders in that store show a price of zero and "Contact sales"; EOS AlSi10Mg is listed in 10 kg units | Höganäs AM powder page: "Contact your sales representative for more information and requests" [5]. Höganäs Japan's listings give "Price range" and "Delivery Time" as "Please contact us for details" [3] |
| Pack size | Not stated for Al5X1 (EOS lists its other powders in 10 kg units) | **10 kg** in a 10 L PE drum under argon; other sizes "available under certain conditions" [2] |
| Price | Not public | Not public |
| Lead time | Not public | Not public ("short delivery time" in Höganäs Japan's general text) |
| Other channels | None found. EOS also sells Al2139 AM and Aheadd CP1 the same way | KBM Advanced Materials (Fairfield, Ohio) signed in 2021 to distribute Höganäs AM powders in the U.S. and Canada [6]. Its website didn't load on 2026-11-27 (the certificate is for another domain), so it isn't confirmed as a current channel |
| Who to ask for a quote | **EOS of North America sales**, through the store page's "Contact sales" button [4], or EOS of North America's main line on the data sheet (+1 877 388 7916) [1] | **Höganäs AM sales** through the contact form at [hoganas.com/am](https://www.hoganas.com/am) (technical area "Additive manufacturing", type "Sales", country "United States") [5]. North American Höganäs in Pennsylvania is the regional sales arm (an older public listing; confirm) |
| Things to ask | Will EOS sell to a lab without an EOS machine (Utah prints on an Aconity MIDI; EOS's parameter set is for the EOS M 290 at 40 µm)? Is a 5 kg or smaller R&D lot possible? Stock location and ship date. Lot certificate contents (chemistry with O, PSD). SDS section 14 (transport class). A starting energy density for non-EOS machines | Smallest lot (is a 5 kg or R&D lot possible?). Stock location (Sweden or U.S.) and ship date. Lot certificate (chemistry with O, PSD). SDS section 14. Which machine and parameters the datasheet used |

**Planning numbers (assumptions, not quotes):**

- **Price.** Budget roughly **$1k-4k per 10 kg drum**, plus hazmat freight.
  - The low end is about what 10 kg of AlSi10Mg costs at public list prices: $70-80/kg for 10-50 kg lots, with
    a 3-week lead time, in one vendor's 2025 buyer's guide [7].
  - The high end is an assumption of about five times that. Neither vendor gives a ratio, and neither does trade
    press, which calls Scalmalloy powder "much more expensive than AlSi10Mg powder" [8].
  - Both vendors market these alloys as cheaper than alloys of similar strength [3, 9], so they should fall inside
    that range. Replace this with the quotes.
- **Lead time.** Plan on **2-4 weeks if a drum is in U.S. stock and 4-8 weeks if it ships from Europe**. For
  comparison, the same AlSi10Mg buyer's guide quotes 3 weeks for 10-50 kg [7]. Fine
  aluminum alloy powder is shipped as dangerous goods (the class is in each SDS, section 14), and the winter break
  falls inside that window. A made-to-order lot would miss the paper.
- **Quantity: one 10 kg drum of each covers the in-house plan** (below). That holds only if every bar is printed
  flat, as in April. One vertical 100 mm build on the full 170 mm MIDI cylinder needs about 9.5-12 kg, since Utah
  fills the supply to three times the build height ([#138](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138#issuecomment-6353370602)).
  The 55 mm reduction kit would need about 1-1.25 kg for the same height.
- **Who:** Gage requests both quotes in the week of Nov 30 (the draft below), and Sterling approves the PO **by
  Fri Dec 11**. A PO after Dec 11 probably means delivery after the break.

<details><summary>Quote request (draft for Gage; not sent)</summary>

> Subject: Quote request: [Al5X1, article 9030-0017 | forAM Al-HS1 GA 20-63 µm], 10 kg, university research
>
> We are a university research lab (Brigham Young University, Provo, Utah) comparing LPBF aluminum alloys. We
> would like a quote for one 10 kg container of [product], shipped to Provo, Utah, with the price, your earliest
> ship date and where the powder ships from, the freight and dangerous-goods charges, and payment terms for a
> university purchase order. Please also tell us:
> 1. whether a smaller research quantity (for example 5 kg) is available;
> 2. what the lot certificate reports (chemistry including oxygen, particle size distribution);
> 3. the transport classification (SDS section 14);
> 4. [EOS only] whether you sell this powder to a lab printing on a non-EOS machine (an Aconity MIDI), and a
>    recommended starting window for layer thickness and energy density on such a machine;
>    [Höganäs only] which machine and parameters the datasheet values were measured with.
>
> The parts are for research only; we may publish properties measured on our own machine, citing your datasheet
> for comparison.

</details>

## What the in-house measurement involves

"The same machine with the same parameters" needs one change. Each alloy has its own melt window, so one parameter
set would favour whichever alloy it was tuned for: AlSi10Mg from April, or EOS's Al5X1 set, which only runs on an
EOS M 290. The fair version, proposed for the pre-registration:

- **The same for every alloy:** machine (Utah's Aconity MIDI), layer thickness, plate temperature, scan strategy,
  gas flow, powder handling (sieve, dry, humidity log), specimen geometry and surface (flat sub-size ASTM E8 bars,
  6 × 6 mm section, built horizontal, as printed), test (extensometer, ASTM E8 strain rates) and statistics.
- **The same rule, not the same numbers, for laser power and speed:** every alloy, candidate or baseline, gets the
  same power-speed grid of density cubes, and its bars are printed at the grid point with the highest density.
- **Heat treatment as each vendor specifies:** Al5X1 400 °C 6 h with gas quench (inert atmosphere preferred) [1];
  Al-HS1 375 °C 4 h in air [2]; Scalmalloy 325 °C 4 h; AlSi10Mg as built and stress-relieved. Candidates get the one
  heat treatment chosen before printing.

**Per baseline powder:**

| Build | What | Powder | Tests |
|---|---|---|---|
| W (window) | 16 cubes, 10 mm, on a 4 × 4 power-speed grid centred on the alloy's published energy density, at the campaign's layer thickness and plate temperature | 1.0-1.2 kg | 16 Archimedes densities, 2-4 sections for cracks and pores |
| T (tensile) | 8 flat bars (3 as built, 3 after the vendor age, 2 spare), 4 cubes for hardness, 3 corrosion coupons, at the densest grid point | 0.6-1.2 kg | ≥ 6 valid tensile, 8 hardness (4 cubes × 2 conditions), 3 corrosion (if R11 is fixed), outside chemistry on the powder lot and one part |

So each baseline adds **2 builds, about 8 tensile tests, 20 densities, 8 hardness and 2 outside chemistry
samples**, plus one furnace run. One 10 kg drum leaves about 7.5-8.5 kg for a repeat in the finalists' session and
for spares.

**For the full one-to-one comparison:**

| Alloy | Powder | Builds | Tensile bars | Note |
|---|---|---|---|---|
| Al5X1 | buy, 10 kg | 2 | 8 | the front-defining baseline |
| Al-HS1 | buy, 10 kg (optional) | 2 | 8 | |
| AlSi10Mg | buy, 10 kg; the lab's stock was about 0.8 kg before April's build used part of it ([#138](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138#issuecomment-6353370602)) | 1-2 | 8 (3 as built, 3 stress-relieved, 2 spare) | re-test with an extensometer (R9); keeps the April bars as provisional |
| Scalmalloy | buy (from APWORKS or a licensed producer) or atomize D2 | 2 | 8 | the burden reference |
| **Total** | | **7-8 builds** | **32 bars** | about 16 h of frame time at 30 min a test |

## Fitting it into the #256 schedule

[The schedule](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md)
planned five Utah sessions (P1 Dec 2-3, P2 Dec 16-17, P3 Jan 12-13, P4 Jan 20-21, P5 Feb 2-3) and 36 Al atomizer
runs. None of the sessions is booked, and the atomizer has made no Al powder (R3, R4).

**Atomizer runs: the baselines take none, and they free two or three.**

| Run | Was | With the baselines |
|---|---|---|
| S1 (Al-Mn-Cr-Zr-Mg, Chalmers alloy F) | a published anchor for the Mn-rich family | **Drop.** Al-HS1 anchors that family in-house, and S1's B_NIR is above Scalmalloy's under every allowed reliance (+0.97 to +2.21), so it can't meet the claim. Frees a run and some of the Zr |
| D2 (Scalmalloy-type, in-house) | the burden reference, made in-house | **Drop if commercial Scalmalloy is bought.** It saves the Sc master alloy, and the campaign is Sc-free, so it needs no Sc route control |
| O1 (Al-3.6Mg-1.2Zr) | a published anchor | **Repurpose as the Al5X1 twin** (Al-3.35Mg-0.55Mn-1.2Zr from dosed charges). Its burden equals Al5X1's (paired difference −0.19 to +0.04). Printed next to commercial Al5X1, it measures what the in-house powder route does to a front alloy, as D1 does for AlSi10Mg (H3). Needs Zr (R6) |

The freed slots go to optimizer rounds, which is where new compositions come from.

**Utah builds are the cost.** The baselines add 7-8 builds to a plan that had about one composition per build. They
fit because the atomizer delay empties the early sessions:

| Session (#256 date) | Was | Proposed |
|---|---|---|
| P1 (Dec 2-3) | commercial AlSi10Mg: tracks, cubes, bars | Unchanged. Book it for mid-December if early December is gone. Re-test with an extensometer |
| P2 (Dec 16-17) | in-house 6063, D1, seed tracks | In-house powder only if the atomizer is back. Otherwise **Al5X1 W**, if the drum has arrived |
| P3 (Jan 12-13) | seed cubes, D2, R1 tracks | **Al5X1 T** (or W), **Al-HS1 W**, plus seed cubes |
| P4 (Jan 20-21) | R2/R3 tracks and cubes | **Al-HS1 T**, **Scalmalloy W/T**, plus R2/R3 |
| P5 (Feb 2-3) | finalists' bars, AlSi10Mg if needed | Finalists. Add Al5X1 and AlSi10Mg builds in the same session if Utah can fit them; otherwise the P3-P4 baseline bars are the comparators |

If Utah can do only one build per session day, ask for a third January day, or drop Al-HS1.

**When the baseline results could exist:**

| PO placed | Powder arrives | Al5X1 window | Al5X1 tensile, aged | Usable at |
|---|---|---|---|---|
| Fri Dec 4, from U.S. stock | about Dec 14-18 | P2 (Dec 16-17), if Utah takes it | early-January build; tested about Jan 22-29 | **G4 (Jan 29)**: the version A/B decision can use it |
| Fri Dec 11, from Europe | about Jan 8-15 | P3 (Jan 12-13) | P4 build; tested about Feb 8-12 | **Freeze (Feb 12)**, just |
| After the break, or made to order | February or later | February | March | Version B in April, or later |

Tensile here assumes an extensometer is in place (R9) and about 11 days from a Utah build to parts in hand, as in
April.

## AlSi10Mg at 228 MPa: what it means for using it as a baseline

The April Utah bars, as built, horizontal, as-printed surface, gave 228 ± 13 MPa yield, 376 ± 10 MPa UTS and
4.5 ± 0.5 % elongation (n = 4 valid; [PR #288](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/288)).
Against the as-built datasheets (PR #285):

- **Yield is 0.76-0.85 of the horizontal machined rows** (EOS 270, Nikon 300 MPa), and 0.86 of Nikon's
  as-printed-surface vertical bars (265 MPa). It is below EOS's lowest row (vertical, 233 MPa).
- **Elongation is about half** the horizontal machined rows (EOS 10.2 %, Nikon 8 %), but above Nikon's as-printed
  bars (3 %).
- **Part of the gap is measurement.** Three of the four valid tests had elastic slopes of 29-49 GPa against about
  70 GPa, so their yields are uncertain by up to about 30 MPa. The one test with a 70 GPa slope gave 235.5 MPa.
  The build parameters and plate temperature weren't recorded (SI S5). A heated plate coarsens AlSi10Mg's silicon
  network and lowers its as-built yield, so the plate temperature alone could explain part of the gap. The powder
  was lab stock with no humidity record.

**What follows:**

1. **AlSi10Mg can't be the bar for "better".** Beating 228 MPa is not beating AlSi10Mg as industry knows it: a
   candidate at 270 MPa would "beat AlSi10Mg" while matching EOS's datasheet. Measured against our own machine it is
   still the right floor, but the bar is now the Sc-free front, with in-house Al5X1 on it.
2. **The deficit could be AlSi10Mg's alone, or the whole process's.** AlSi10Mg's as-built strength comes from a
   fine cellular silicon network that depends on cooling rate, plate temperature and parameters. Al5X1 and Al-HS1
   get most of their strength from the direct age, which may depend less on how they were printed. Measuring them
   in-house tells the two cases apart. If aged Al5X1 lands near its datasheet while AlSi10Mg stays low, the gap is
   AlSi10Mg's. If both are low, it is the process, and the paper's claims stay relative to the in-house baselines.
3. **Re-measure AlSi10Mg** with the baselines: same session, extensometer, as built and stress-relieved. Ask Utah
   for the April build's parameters and plate temperature (R4).
4. **Keep the April bars as a provisional point** in the SI and in Fig. 1, labelled as such. They're still worth
   having: an in-house AlSi10Mg point 16-24 % below the sheets is exactly what a reader comparing our numbers with
   datasheets needs to see.
5. **"On par with the datasheets" needs a rule fixed in advance.** Proposed: the in-house mean yield, in the
   vendor's condition and the matching orientation, is at least 90 % of the datasheet's typical value. That allows
   for as-printed sub-size bars against machined ones. Elongation is reported against the as-printed datasheet
   rows where they exist. On April's numbers, AlSi10Mg is not on par: 228/270 = 0.85, and 228/300 = 0.76.

## The burden metric to freeze before the screen ranks anything

This expands R2 in [`risks.md`](risks.md) with the baselines in place.

| Metric | Does Al5X1 beat Scalmalloy? | Does Al-HS1? | Does it separate Sc-free alloys? | Where Al5X1 and Al-HS1 sit on the Sc-free front |
|---|---|---|---|---|
| **B_NIR**, import-weighted mass, compared under the same reliances | yes (robustly) | no (ambiguous) | yes, from 0.1 (Al-Fe-Zr) to 7 wt % (Al-Mn-Cr-Zr-Mg) | Al5X1 on the front; Al-HS1 behind it |
| B_mass, mass of listed elements | yes at the midpoints (5.10 vs 6.21); no at the top of its range (7.00) | no (6.40) | yes | same as B_NIR |
| B_cost, cost of the critical additions | yes (99 % below) | yes (99 % below) | no: every silver-free Sc-free alloy is 0.25-0.94 USD/kg (silver-bearing Al2139: 5.2) against Scalmalloy's 39.9, and those differences are tiny next to the powder's own price | neither: a tailored AlSiMg (417 MPa as built, on one machine, 0.26 USD/kg) dominates both |

**Recommendation: freeze B_NIR**, with these rules:

1. **Compare alloys under the same import reliances.** Mg, Si and Zr have only bounds, but the bound is the same
   unknown for every alloy. "Below Scalmalloy" means below under every allowed reliance, which the paired difference
   checks (`paired_difference` in [`mineral_burden.py`](scripts/mineral_burden.py)). The draft's rule, the whole
   interval below Scalmalloy's lowest value, compared an alloy at one reliance with Scalmalloy at another. It was
   stricter than it needed to be, but it doesn't change any verdict above.
2. **Use measured compositions**: the outside lab's for every printed alloy, the baselines included. Al5X1's
   composition range alone spans B_NIR 2-5.7 wt %, so the lot decides where it sits.
3. **Plot the midpoint, test at the bounds.** The front is drawn at the midpoint reliances, and the claim has to
   hold at the bounds too.
4. **Report B_mass and B_cost in the SI** as sensitivity. B_cost backs the plain statement that every Sc-free alloy
   is far cheaper in critical additions.
5. **Why B_NIR:**
   - It is the only one of the three that both counts how much critical material an alloy uses (the kickoff's
     "the more that there is", 09:48) and tells Sc-free alloys apart, which a front needs.
   - It is FLAIME's mineral-burden node with USGS import-reliance weights (proposal, lines 760-761), so the paper and the
     program use the same number.
   - It is reproducible from one public source.
   - Graedel or ESSENZ weights can be added later as sensitivity.

## Sources

1. EOS GmbH, Material Data Sheet, EOS Aluminium Al5X1 (status 10/2023), and its process data for the EOS M 290,
   40 µm. https://www.eos.info/05-datasheet-images/Assets_MDS_Metal/EOS_Aluminium_Al5X1/Material_DataSheet_EOS_Aluminium_Al5X1_EN.pdf
2. Höganäs AB, forAM Al-HS1 20-63 GA data sheet, 3312HOG-3 (2026). https://www.hoganas.com/globalassets/downloads/libary/additive-manufacturing_foram-al-hs1-20-63-ga_3312hog.pdf
3. Höganäs Japan K.K. product listings on IPROS: forAM Al-HS1/HS2, and Al-HS1 GA. https://pr.mono.ipros.com/en/hoganas/product/detail/2001560745/ ;
   https://pr.mono.ipros.com/en/hoganas/product/detail/2001065908/
4. EOS online store, EOS Aluminium Al5X1 (article 9030-0017), and the store's product list (read 2026-11-27).
   https://store.eos.info/products/eos-aluminium-al5x1
5. Höganäs, Aluminium-based metal powder for 3D printing (product list and sales contact).
   https://www.hoganas.com/en/powder-technologies/additive-manufacturing-metal-powders/3d-printing-metal-powders/aluminium-alloy-am-powders/
6. Metal AM, "Höganäs finalises agreement to supply KBM's AM and MIM powder sales platform" (2021), and "KBM adds
   IMR's aluminium powders to its online marketplace" (May 29, 2024). https://www.metal-am.com/?p=82565 ;
   https://www.metal-am.com/kbm-adds-imrs-aluminium-powders-to-its-online-marketplace/
7. Met3DP, "Metal powder for 3D printing AlSi10Mg: complete buyer's guide for 2025" (vendor page, read 2026-11-27):
   USD 70-80/kg and 3 weeks for 10-50 kg; USD 50-80/kg wholesale. https://blog.met3dp.com/blog/metal-powder-for-3d-printing-alsi10mg-complete-buyers-guide-for-2025/
8. Metal AM, "Scalmalloy is too expensive and design optimisation only makes sense in aerospace. True or false?"
   ("Scalmalloy powder is still much more expensive than AlSi10Mg powder"; powder is typically under 15 % of part
   cost). https://www.metal-am.com/articles/scalmalloy-is-too-expensive-and-design-optimisation-only-makes-sense-in-aerospace/
9. EOS press release, "EOS Expands Portfolio with Aluminum Al5X1 Alloy" (2023): "a more competitive cost than other
   aluminum alloys with similar strength and elongation properties". https://www.eos.info/press-media/press-center/press-releases/2023/eos-aluminum-alloy-al5x1
