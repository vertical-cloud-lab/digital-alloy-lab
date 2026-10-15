# Edison Scientific LITERATURE_HIGH Output — Critical Minerals + Al Alloy Framing Defensibility

**Task ID:** `039eae23-5eb4-46fc-871a-e270e513c823`
**Mode:** LITERATURE_HIGH | **Date:** 2026-04-10 | **Size:** ~35K chars
**Part of:** Topic 3B Deep-Dive Series (10 queries, ~331K chars total)

> *Raw Edison Scientific output below. The query prompt appears first, followed by the model's structured response.*

---

Question: 
RESEARCH QUESTION: Is it scientifically and programmatically defensible to frame aluminum alloy discovery as "critical mineral demand reduction" for a DOE AMMTO proposal?

Context: DOE Genesis Mission Topic 3B (Critical Minerals, AMMTO) calls for "automated discovery platforms to accelerate material discovery, manufacturing, and qualification through closed-loop systems... REDUCING DEMAND for critical minerals." A proposal (FLAIME) wants to use Al alloys as the Phase I demonstration material for an autonomous alloy discovery platform.

Investigate thoroughly:
1. Which critical minerals (per DOE/USGS definitions) are contained in alloys that aluminum could substitute for? Quantify.
2. What is the DOE/USGS official critical minerals list and how does it intersect with structural alloys?
3. Are there published examples of Al alloy development explicitly motivated by critical mineral reduction (e.g., Al-Ce replacing rare-earth magnets, Al replacing Co/Ni superalloys in lower-temp applications)?
4. What are the strongest and weakest arguments for this framing?
5. Would an AMMTO program manager accept this framing, or would they see it as a stretch?
6. Provide quantitative estimates: How many kg/year of critical minerals could be displaced by novel Al alloys in specific applications?

Cite all sources with page numbers.


## Executive conclusion
It is scientifically defensible to frame aluminum-alloy discovery as **critical mineral demand reduction** for a DOE AMMTO “Critical Minerals” topic **only if the proposal explicitly targets substitution of alloys/components that contain DOE/USGS-critical minerals (especially Mg, Ni, Co, and in some cases platinum-group metals), and if claims about rare-earth (Nd/Dy/Tb) impacts are framed as supply-chain risk mitigation rather than direct demand reduction.** The framing becomes a stretch if Phase I centers solely on “Al is abundant” without quantifying displaced critical minerals, or if it implies Al–Ce alloys directly replace NdFeB magnets or high-pressure turbine superalloys. (bauer20232023criticalmaterials pages 16-18, staff2024usgsmineralreview pages 6-8, grilli2017solutionsforcritical pages 3-6, helbig2020supplyriskconsiderations pages 1-3)

A key limitation of this analysis is that **the Genesis Mission Topic 3B solicitation text itself was not retrievable in this run**, so I cannot quote the exact FOA language; the answer below therefore anchors “critical mineral” definitions and demand-reduction mechanisms to **USGS’s official critical-minerals list** and **DOE’s 2023 Critical Materials Assessment/Strategy**. (staff2024usgsmineralreview pages 6-8, bauer20232023criticalmaterials pages 16-18)


## 1) Which USGS/DOE critical minerals are contained in structural alloys that aluminum could substitute for (and how to quantify)
### 1.1 Official USGS critical minerals that commonly appear in structural/engineering alloys
USGS’s 2022 Final List of Critical Minerals (Federal Register 87 FR 10381) includes multiple elements that are standard constituents of structural alloys or high-performance engineering alloys—e.g., **Ni, Co, Cr, Mn, Mg, Ti, Nb, Ta, W, and many rare earth elements**. (staff2024usgsmineralreview pages 6-8)

In the USGS table excerpt, Ni and Co are explicitly listed with “batteries and metallurgy,” Mg is listed for “metallurgy,” Ti for “metallurgy and pigments,” and many refractory/strengthening elements (Nb, Ta, W) are listed for “metallurgy.” (staff2024usgsmineralreview pages 6-8)

### 1.2 Quantification approach (defensible for AMMTO)
A defensible quantification for “critical mineral demand reduction” is:

\[\text{Displaced critical mineral (kg/yr)} = (\text{baseline component mass (kg/yr)})\times(\text{critical-element wt%})\times(\text{substitution penetration})\]

Baseline **critical-element wt%** can be sourced from nominal compositions of incumbent alloys (examples below). Baseline **component mass/market tonnage** must be tied to an addressable application segment (automotive castings, Mg-alloy parts, certain Ni-superalloy components, etc.). Representative superalloy market mass data exist in the retrieved evidence (global superalloy demand in 2008), but many application-specific volumes (e.g., exhaust manifolds, compressor cases) were not in the retrieved corpus and therefore must be handled as explicit assumptions if used. (kollova2022superalloys—characterizationusageanda pages 1-2, grilli2021criticalrawmaterials pages 8-9)

### 1.3 Incumbent alloy examples containing critical minerals (compositions)
Nickel-based superalloys are explicitly multi-element systems containing numerous critical commodities. A review of Ni-superalloys provides nominal compositions for representative alloys. For example, a table of compositions includes **Rene 80** with **Cr 14 wt%, Co 9.5 wt%, Mo 4 wt%, Al 3 wt%, Ti 5 wt%, W 4 wt%** and **CMSX-4** with **Cr 6.5 wt%, Co 9 wt%, Mo 0.6 wt%, Al 5.6 wt%, Ti 1 wt%, Ta 6.5 wt%, Re 3 wt%, W 6 wt%** (plus Ni balance). (grilli2021criticalrawmaterials pages 8-9)

Another study emphasizes that Ni superalloys can include **Al, Ti, Cr, Fe, Co, Nb, Mo, Ru, Ta, W, Re** (and Ni) and provides typical Re contents (e.g., ~3 wt% in 2nd generation and ~6 wt% in 3rd generation single-crystal alloys), and notes industry interest in **low-Re/no-Re** variants due to supply risk and cost. (helbig2020supplyriskconsiderations pages 3-5)


## 2) What are the official DOE/USGS critical minerals lists, and how do they intersect with structural alloys?
### 2.1 USGS critical minerals (official list)
USGS published the **“2022 Final List of Critical Minerals”** in the Federal Register (**87 FR 10381**) on Feb. 24, 2022, pursuant to Section 7002 of the Energy Act of 2020; it revised the 2018 list (**83 FR 23295**) and expanded the list to **50 mineral commodities**. The excerpted USGS table (“Table 3: The 2022 U.S. critical minerals list”) shows many of the elements relevant to alloying and metallurgy, including Ni, Co, Mg, Ti, Cr, Nb, Ta, W, REEs, and PGMs. (staff2024usgsmineralreview pages 6-8, staff2024usgsmineralreview media 73ac4725)

The same source also explicitly notes changes from 2018 to 2022: **added nickel and zinc; listed out individual platinum-group metals and rare earth elements; removed helium, potash, rhenium, strontium, and uranium.** (staff2024usgsmineralreview pages 6-8)

### 2.2 DOE critical/near-critical materials (official DOE energy-sector list)
DOE’s 2023 Critical Materials Assessment/Strategy identifies short-term (2020–2025) **critical** materials as **dysprosium, neodymium, gallium, graphite, cobalt, terbium, and iridium**, and **near-critical** materials as **lithium, uranium, electrical steel, nickel, magnesium, SiC, fluorine, praseodymium, and platinum**. (bauer20232023criticalmaterials pages 16-18)

For the medium term (2025–2035), DOE indicates **nickel, platinum, magnesium, SiC, and praseodymium** shift to “critical,” and **aluminum, copper, and silicon** become “near critical.” (bauer20232023criticalmaterials pages 16-18)

### 2.3 Intersection with structural alloys
DOE’s list explicitly includes **nickel, cobalt, magnesium** (and later aluminum itself as near-critical), which creates a strong programmatic bridge to structural alloys and lightweighting alloys. (bauer20232023criticalmaterials pages 16-18, bauer20232023criticalmaterials pages 34-36)

USGS’s list includes a broader set of metallurgy-relevant commodities (Nb, Ta, W, many REEs) that appear in high-performance alloys. (staff2024usgsmineralreview pages 6-8)


## 3) Published examples of aluminum alloy development explicitly motivated by critical mineral reduction or supply-chain stability
### 3.1 Al–Ce / Al–La alloys motivated by REE supply-chain resilience (explicitly stated)
Peer-reviewed literature directly frames Al–Ce/La alloy development as a supply-chain strategy:

- **Sims et al. (2016)** propose Ce-rich aluminum casting alloys as a high-volume outlet for Ce (a byproduct of RE mining), arguing this can “stabilize the global rare earth market” and thereby “decrease the long-term criticality” of other REEs and impact technologies involving “Nd and Dy” (in the excerpted pages). (sims2016ceriumbasedintermetallicstrengthenedaluminum pages 1-3)

- **Sims et al. (2022)** explicitly state that promoting demand for Ce and La can improve “supply chain stability for all rare earth elements,” and further argue that shifting value toward La/Ce could “potentially lower[] the price and/or supply volatility of Nd and other critical REEs.” They provide quantitative context for imbalance (La/Ce are >70% of ore mass but <10% of value; magnet REEs represent much of the value) and argue large La/Ce usage in Al alloys could rebalance production economics and stabilize supply chains. (sims2022howceriumand pages 1-3, sims2022howceriumand pages 3-5)

- **Nguyen et al. (2019)** model the impacts of introducing Al–Ce alloys into the U.S. automotive market, emphasizing that increased demand for co-product cerium can improve mine economics for other, more critical REEs; they also highlight recycling and segregation challenges (important for AMMTO manufacturability/qualification framing). (nguyen2019anticipatingimpactsof pages 1-2)

- **Amon & McCall (2025)** explicitly position Al–Ce (and Al–La) alloys as a cerium valorization strategy with potential to “substitute critical materials” and to replace “expensive aluminum-scandium.” (amon2025opportunitiesforcerium pages 1-4)

These are strong precedents for a supply-chain-focused framing, but they are **not** direct evidence that Al alloys reduce Nd/Dy/Tb demand by substitution (i.e., they do not replace magnets); they argue **market balancing / mining economics** pathways. (sims2022howceriumand pages 1-3, sims2022howceriumand pages 3-5)

### 3.2 Al as substitution for critical-mineral-containing superalloys: what the literature supports
The strongest direct “demand reduction” substitution logic is **not** “Al replaces turbine blades,” but rather:
- **targeted substitution of Ni/Co-containing alloys in moderate-temperature applications**, and/or
- **materials and manufacturing efficiency** that reduces required mass of critical alloys.

Literature on Ni-superalloys emphasizes that there is currently “no suitable substitute for superalloys” for the most extreme high-temperature uses; replacement is described as difficult. (helbig2020supplyriskconsiderations pages 1-3, grilli2017solutionsforcritical pages 3-6)

Thus, a proposal that claims broad replacement of Ni-based superalloys by Al alloys would conflict with these statements unless tightly scoped to temperatures/service conditions where high-temperature Al alloys are plausible. (grilli2017solutionsforcritical pages 3-6, darolia2019developmentofstrong pages 1-3)


## 4) Strongest vs weakest arguments for framing Al-alloy discovery as “critical mineral demand reduction”
### Strongest arguments
1. **Direct displacement of DOE/USGS-listed critical minerals Mg, Ni, Co** in specific component classes.
   - DOE explicitly flags **nickel and magnesium** as near-critical short term and critical medium term, and **cobalt** as critical short term. (bauer20232023criticalmaterials pages 16-18)
   - USGS lists Ni, Co, Mg as critical minerals used in metallurgy. (staff2024usgsmineralreview pages 6-8)

2. **Quantifiable critical-element content in incumbent alloys** (e.g., Co~9 wt%, Ta~6.5 wt%, W~6 wt%, Re~3 wt% in CMSX-4) provides straightforward “kg displaced” calculations when paired with any credible adoption volume. (grilli2021criticalrawmaterials pages 8-9)

3. **Manufacturing/qualification emphasis aligns with DOE Critical Materials Strategy pillars**, including “Develop Alternatives” and “Materials and Manufacturing Efficiency,” even when the alternative is a new alloy system. (bauer20232023criticalmaterials pages 1-9)

4. **Supply-chain-resilience precedent exists for Al–Ce/La alloys**: multiple studies explicitly connect Al–Ce/La alloys to stabilizing the REE supply chain and reducing volatility of critical REEs (Nd/Dy) through coproduct-demand mechanisms. (sims2016ceriumbasedintermetallicstrengthenedaluminum pages 1-3, sims2022howceriumand pages 1-3)

### Weakest arguments (likely to be challenged)
1. **Claiming Al–Ce alloys reduce demand for Nd/Dy/Tb by substituting magnets.** The evidence supports REE market balancing and potentially reduced volatility, not direct substitution of magnet REEs. (sims2022howceriumand pages 1-3, sims2022howceriumand pages 3-5)

2. **Claiming Al alloys replace the hottest Ni-superalloy turbine sections.** Literature notes no suitable substitute for superalloys and that replacement is hard; Ni-superalloys’ multi-element design is complex and often critical-element-dependent. (helbig2020supplyriskconsiderations pages 1-3, grilli2017solutionsforcritical pages 3-6, darolia2019developmentofstrong pages 1-3)

3. **Overstating the criticality of aluminum itself** to justify the demo. DOE does classify aluminum as “near critical” in the medium term in the excerpted evidence, but this does not by itself demonstrate “demand reduction for critical minerals,” because aluminum is the *chosen material* rather than the displaced mineral. (bauer20232023criticalmaterials pages 16-18)


## 5) Would an AMMTO program manager accept this framing?
Based on the evidence available here, the most programmatically defensible positioning is:

- **Primary framing**: “autonomous alloy discovery to reduce demand for critical minerals **Ni/Co/Mg** through substitution and manufacturing efficiency in targeted moderate-temperature and lightweighting applications.” (bauer20232023criticalmaterials pages 16-18, staff2024usgsmineralreview pages 6-8)

- **Secondary framing (carefully worded)**: “Al–Ce/La alloys as a supply-chain stabilization pathway for critical magnet REEs by increasing coproduct value and improving domestic REE mining economics,” explicitly avoiding the claim of direct Nd/Dy demand displacement. (sims2022howceriumand pages 1-3, sims2022howceriumand pages 3-5)

A program manager would likely view the framing as a stretch if the proposal cannot:
1) name which critical minerals are reduced (by official list),
2) identify which incumbent alloys/components contain them, and
3) provide at least order-of-magnitude displacement estimates.

The provided evidence supports (1) and (2) strongly and supports (3) at an order-of-magnitude level with transparent assumptions; therefore, the framing can be acceptable if written narrowly and quantified. (staff2024usgsmineralreview pages 6-8, bauer20232023criticalmaterials pages 16-18, grilli2021criticalrawmaterials pages 8-9, kollova2022superalloys—characterizationusageanda pages 1-2)


## 6) Quantitative estimates: kg/year of critical minerals displaced by novel Al alloys (illustrative scenarios)
Two evidence-anchored quantitative baselines are available here:

- Global superalloy demand reported as **54,431,084.4 kg in 2008**. (kollova2022superalloys—characterizationusageanda pages 1-2)
- Representative superalloy compositions showing **critical elements at multi-wt% levels** (e.g., CMSX-4 with Co 9%, Ta 6.5%, W 6%, Re 3%). (grilli2021criticalrawmaterials pages 8-9)

A third baseline from DOE supports automotive lightweighting scale:
- DOE reports aluminum use of **459 lb/vehicle (2020)** and expected **+12% by 2026**. (bauer20232023criticalmaterials pages 34-36)

The table below provides transparent, order-of-magnitude displacement calculations based on these baselines.

| Scenario | Baseline material and application | Baseline annual mass of material | Baseline critical mineral mass fraction(s) | Assumed substitution fraction | Computed critical-mineral displacement (kg/year) | Feasibility / temperature-limit notes |
|---|---|---|---|---|---|---|
| 1 | Global Ni-base superalloys in gas turbines / aerospace hot-section hardware; novel high-temperature Al alloys substitute only a low-temperature subset | 54,431,084.4 kg/yr global superalloy demand in 2008 (kollova2022superalloys—characterizationusageanda pages 1-2) | Representative Ni-superalloy chemistry (CMSX-4): Co 9 wt%, Ta 6.5 wt%, W 6 wt%, Re 3 wt%, Cr 6.5 wt%, balance Ni; Ni is >50 wt% in all types (grilli2021criticalrawmaterials pages 8-9, helbig2020supplyriskconsiderations pages 3-5) | 5% of total superalloy mass | Ni displaced ≈ 54,431,084.4 × 0.05 × 0.60 = 1,632,933 kg/yr; Co ≈ 54,431,084.4 × 0.05 × 0.09 = 244,940 kg/yr; Ta ≈ 54,431,084.4 × 0.05 × 0.065 = 176,901 kg/yr; W ≈ 54,431,084.4 × 0.05 × 0.06 = 163,293 kg/yr; Re ≈ 54,431,084.4 × 0.05 × 0.03 = 81,647 kg/yr (grilli2021criticalrawmaterials pages 8-9, helbig2020supplyriskconsiderations pages 3-5) | Aggressive upper-bound framing for moderate-temperature components only; not credible for the hottest creep-limited turbine sections because literature states no suitable substitute for superalloys in those uses and replacement is hard (helbig2020supplyriskconsiderations pages 1-3, grilli2017solutionsforcritical pages 3-6, darolia2019developmentofstrong pages 1-3) |
| 2 | Lower-temperature / lower-Re single-crystal or advanced Ni-superalloy components; Al alloy replaces only the Re-bearing subset | Same 54,431,084.4 kg/yr superalloy baseline, but assume only 10% of market is the relevant advanced Re-bearing subset (assumption, not cited) built from later-generation alloys (kollova2022superalloys—characterizationusageanda pages 1-2) | Re content in advanced single-crystal alloys ~3 wt% (2nd gen) to ~6 wt% (3rd gen); low-Re alloy example 1.2 wt% Re also reported (helbig2020supplyriskconsiderations pages 3-5, darolia2019developmentofstrong pages 1-3) | 10% of the assumed Re-bearing subset, i.e. effective 1% of total superalloy market | Conservative case using 3 wt% Re: 54,431,084.4 × 0.10 × 0.10 × 0.03 = 16,329 kg Re/yr displaced; upper case using 6 wt% Re: 54,431,084.4 × 0.10 × 0.10 × 0.06 = 32,659 kg Re/yr displaced (helbig2020supplyriskconsiderations pages 3-5, darolia2019developmentofstrong pages 1-3) | More defensible than Scenario 1 because it targets selected expensive Re-bearing alloys, but still limited to moderate-service components; hottest applications remain poor candidates for Al substitution (helbig2020supplyriskconsiderations pages 1-3, darolia2019developmentofstrong pages 1-3) |
| 3 | Automotive lightweighting: novel Al alloys displace critical-mineral-intensive alternatives in part of future vehicle mass growth | DOE states Al usage reached 459 lb/vehicle in 2020 and is expected to grow another 12% by 2026; growth increment = 459 × 0.12 = 55.08 lb = 24.98 kg Al/vehicle (bauer20232023criticalmaterials pages 34-36). Assume 1,000,000 vehicles/yr affected (assumption, not cited) | If displaced alternative is Mg alloy, use 100 wt% Mg for a first-order upper bound; Mg is DOE near-critical short term and critical medium term, USGS critical mineral (bauer20232023criticalmaterials pages 16-18, staff2024usgsmineralreview pages 8-10) | Assume 25% of the added Al mass directly substitutes Mg-intensive lightweight components | Mg displaced ≈ 24.98 kg/vehicle × 1,000,000 vehicles/yr × 0.25 = 6,245,000 kg Mg/yr displaced (bauer20232023criticalmaterials pages 34-36, bauer20232023criticalmaterials pages 16-18, staff2024usgsmineralreview pages 8-10) | Programmatically attractive because DOE explicitly ties Al to vehicle lightweighting and Mg is DOE-critical/near-critical; technically plausible for many cast and structural parts, but this is assumption-sensitive and not all added Al actually replaces Mg rather than steel or cast iron (bauer20232023criticalmaterials pages 34-36, bauer20232023criticalmaterials pages 16-18) |


*Table: This table gives three order-of-magnitude scenarios for critical-mineral displacement enabled by novel aluminum alloys, using available evidence for superalloy demand, representative superalloy compositions, and DOE vehicle lightweighting data. It is useful for framing defensible upper-bound and moderate cases in a proposal.*

Interpretation guidance for proposal writing:
- Scenario 3 (Mg displacement in lightweighting) is the **cleanest “demand reduction” story** because Mg is explicitly DOE-critical/near-critical and substitution is plausible for many structural parts. (bauer20232023criticalmaterials pages 16-18, bauer20232023criticalmaterials pages 34-36)
- Scenarios 1–2 are useful as **upper bound / conservative bound** stories for Ni/Co/Ta/W/Re, but must be explicitly scoped to moderate-temperature components because superalloy substitution is otherwise contradicted by the literature. (helbig2020supplyriskconsiderations pages 1-3, grilli2017solutionsforcritical pages 3-6)


## 7) Practical guidance: how to frame aluminum-alloy discovery without overreach
Recommended defensible framing language (consistent with the above evidence):

1. “We will demonstrate a closed-loop autonomous alloy discovery platform on aluminum alloys that are engineered to **substitute for Mg- and Ni/Co-bearing alloys** in defined transportation/industrial component classes, thereby **reducing demand** for DOE/USGS-listed critical minerals (Mg, Ni, Co).” (bauer20232023criticalmaterials pages 16-18, staff2024usgsmineralreview pages 6-8)

2. “Where Al–Ce/La compositions are explored, the critical-minerals impact is framed as **REE supply-chain stabilization** (through coproduct-demand rebalancing) rather than direct displacement of magnet REEs.” (sims2022howceriumand pages 1-3, sims2022howceriumand pages 3-5)

3. “We will avoid claims of replacing high-pressure turbine blade superalloys; instead we target **moderate-temperature castings and lightweight structures** where high-temperature Al alloys can be performance-competitive.” (helbig2020supplyriskconsiderations pages 1-3, darolia2019developmentofstrong pages 1-3)


## Summary mapping of critical minerals to substitution pathways
The following table summarizes which USGS critical minerals are plausibly addressable via Al-alloy substitution (directly or indirectly) and whether DOE classifies them as critical/near-critical in the retrieved evidence.

| Critical mineral (USGS 2022) | Structural / engineering alloy context | Representative way novel Al alloys could substitute or reduce use | DOE 2023 status noted in extracted evidence | Citations |
|---|---|---|---|---|
| Nickel | Ni-base superalloys; stainless and high-Ni battery-linked alloys; USGS lists Ni for batteries and metallurgy | Strongest substitution case is moderate-temperature cast/wrought parts where high-temp Al alloys can replace some Ni-bearing components; weak for hottest turbine sections | Near-critical short term; critical medium term | (staff2024usgsmineralreview pages 6-8, bauer20232023criticalmaterials pages 16-18) |
| Cobalt | Co-base superalloys; binder/addition in high-performance alloys; USGS lists Co for batteries and metallurgy | Possible reduction in selected moderate-temperature engine/industrial components if Al alloys displace some Co/Ni alloy mass; not credible for hottest creep-limited parts | Critical short term | (staff2024usgsmineralreview pages 6-8, bauer20232023criticalmaterials pages 16-18) |
| Magnesium | Mg alloys in vehicle lightweighting; USGS lists Mg for metallurgy | Direct substitution pathway: Al alloys can replace Mg alloys in many cast/lightweight structures while reducing Mg demand | Near-critical short term; critical medium term | (staff2024usgsmineralreview pages 6-8, bauer20232023criticalmaterials pages 16-18, bauer20232023criticalmaterials pages 34-36) |
| Titanium | Ti alloys, aluminides, powders; USGS lists Ti for metallurgy and pigments | Al alloys can replace Ti in lower-temperature lightweight structures, castings, housings, brackets, and some transportation parts where specific strength demands permit | Not identified in extracted DOE critical / near-critical lists | (staff2024usgsmineralreview pages 8-10, bauer20232023criticalmaterials pages 16-18) |
| Chromium | Stainless steels, corrosion-resistant steels, superalloys; USGS lists Cr for metallurgy | Limited direct critical-mineral reduction case: Al can replace some Cr-bearing steels/cast irons in lightweight/corrosion-sensitive components, but DOE relevance is indirect because Cr not highlighted in extracted DOE list | Not identified in extracted DOE critical / near-critical lists | (staff2024usgsmineralreview pages 6-8, bauer20232023criticalmaterials pages 16-18) |
| Manganese | Steels and some battery chemistries; USGS lists Mn for batteries and metallurgy | Al alloys may reduce use of Mn-bearing steels in lightweight body/chassis/casting applications, but this is a secondary framing rather than a headline case | Not identified in extracted DOE critical / near-critical lists | (staff2024usgsmineralreview pages 6-8, bauer20232023criticalmaterials pages 16-18) |
| Niobium | HSLA steels, superalloys, specialty alloys; USGS lists Nb for metallurgy | Plausible only where Al replaces Nb-microalloyed steels or selected high-performance castings; likely niche and hard to quantify cleanly | Not identified in extracted DOE critical / near-critical lists | (staff2024usgsmineralreview pages 6-8, bauer20232023criticalmaterials pages 16-18) |
| Tungsten | Tool steels, hardmetals, superalloys; USGS lists W for metallurgy | Very limited Al substitution case except replacing some heavy W-containing high-temp/ wear parts in less severe service; weak proposal anchor | Not identified in extracted DOE critical / near-critical lists | (staff2024usgsmineralreview pages 8-10, bauer20232023criticalmaterials pages 16-18) |
| Tantalum | Superalloys, refractory/corrosion uses; USGS lists Ta for capacitors and metallurgy | Only niche reduction via replacing Ta-bearing high-temp alloys in moderate-service components; weak broad demand-reduction claim | Not identified in extracted DOE critical / near-critical lists | (staff2024usgsmineralreview pages 6-8, bauer20232023criticalmaterials pages 16-18) |
| Rare earths: Nd, Pr, Dy, Tb | Permanent magnets; some specialty alloys; USGS lists individual REEs and applications including permanent magnets | Indirect but publishable case: Al-Ce/La alloys do not replace NdFeB magnets directly, but can improve REE supply-chain balance and potentially reduce volatility / reliance on critical magnet REEs by creating demand for abundant La/Ce coproducts | Nd and Dy critical/near-critical in DOE evidence: Nd critical short term; Pr near-critical short term and critical medium term; Dy critical short term; Tb critical short term | (staff2024usgsmineralreview pages 6-8, staff2024usgsmineralreview pages 8-10, bauer20232023criticalmaterials pages 16-18, sims2022howceriumand pages 1-3, sims2022howceriumand pages 3-5) |
| Rare earths: Ce, La | Alloying additions in emerging Al-Ce / Al-La alloys; USGS lists Ce and La individually | Positive programmatic case is supply-chain rebalancing rather than demand reduction: Al-Ce/La alloys create high-volume use for abundant coproduct REEs and may stabilize mining economics for critical magnet REEs | Ce and La not listed as critical / near-critical in extracted DOE evidence | (staff2024usgsmineralreview pages 6-8, staff2024usgsmineralreview pages 8-10, bauer20232023criticalmaterials pages 16-18, sims2022howceriumand pages 1-3, sims2022howceriumand pages 3-5, nguyen2019anticipatingimpactsof pages 1-2) |
| Platinum-group metals: Pt, Ir | High-temperature/corrosion uses, catalysts, coatings; USGS lists Pt and Ir individually | Little direct structural-alloy substitution by Al except niche component redesigns; not a strong Al-alloy demonstration case | Pt near-critical short term and critical medium term; Ir critical short term | (staff2024usgsmineralreview pages 6-8, staff2024usgsmineralreview pages 8-10, bauer20232023criticalmaterials pages 16-18) |
| Scandium | Al-Sc alloys for high strength/weldability; USGS lists Sc for ceramics, fuel cells, metallurgy | Novel Al alloys can reduce need for Sc-containing Al alloys by achieving similar performance with Ce/La/Mg/other lower-risk chemistries | Not identified in extracted DOE critical / near-critical lists | (staff2024usgsmineralreview pages 6-8, amon2025opportunitiesforcerium pages 1-4) |


*Table: This table maps selected USGS 2022 critical minerals used in structural or engineering alloys to realistic substitution or demand-reduction pathways via aluminum alloys. It also flags whether extracted DOE 2023 evidence classifies each mineral as critical or near-critical, helping judge which proposal framings are strongest.*


## Notes on evidence and missing items
- The USGS table excerpt (Mining Engineering annual review) provides the Federal Register citation and an enumerated list (Table 3) but, in the retrieved excerpt, the table continues across pages and the full 50-item enumeration may not be fully visible; however, the citation to the official Federal Register notice is explicit. (staff2024usgsmineralreview pages 6-8, staff2024usgsmineralreview pages 8-10)
- The DOE 2023 critical/near-critical lists are present in the excerpted evidence but without the report’s internal page numbers for Figures ES.1/ES.2; the extracted excerpt text provides the lists. (bauer20232023criticalmaterials pages 16-18)
- Application-specific deployment volumes (e.g., annual tonnage of a given alloy in a given component class) were not present in the retrieved evidence set beyond the superalloy market-demand figure; any proposal should therefore cite authoritative industry or USGS/DOE market-flow data for the chosen application segment to firm up kg/yr displacement estimates.


References

1. (bauer20232023criticalmaterials pages 16-18): Diana Bauer, Helena Khazdozian, Jeremy Mehta, Ruby Nguyen, Michael Severson, Bjorn Vaagensmith, Lionel Toba, Bo Zhang, Tasmin Hossain, Adam Sibal, Braeton Smith, Matthew Riddle, Diane Graziano, Tony Mathew, Patrick Cuscaden, Qiang Dai, Chukwunwike Iloeje, Lesley Edgemon, Caitlyn Sarna, and Julian Quaresima. 2023 critical materials strategy. ArXiv, Jul 2023. URL: https://doi.org/10.2172/1998242, doi:10.2172/1998242. This article has 18 citations.

2. (staff2024usgsmineralreview pages 6-8): U Staff. Usgs mineral review. Unknown journal, 2024.

3. (grilli2017solutionsforcritical pages 3-6): Maria Grilli, Tiziano Bellezze, Ernst Gamsjäger, Antonio Rinaldi, Pavel Novak, Sebastian Balos, Radu Piticescu, and Maria Ruello. Solutions for critical raw materials under extreme conditions: a review. Materials, 10:285, Mar 2017. URL: https://doi.org/10.3390/ma10030285, doi:10.3390/ma10030285. This article has 90 citations.

4. (helbig2020supplyriskconsiderations pages 1-3): Christoph Helbig, Alex M. Bradshaw, Andrea Thorenz, and Axel Tuma. Supply risk considerations for the elements in nickel-based superalloys. Resources, 9:106, Aug 2020. URL: https://doi.org/10.3390/resources9090106, doi:10.3390/resources9090106. This article has 25 citations.

5. (kollova2022superalloys—characterizationusageanda pages 1-2): A Kollová and K Pauerová. Superalloys—characterization, usage and recycling. Unknown journal, 2022.

6. (grilli2021criticalrawmaterials pages 8-9): Maria Luisa Grilli, Daniele Valerini, Anca Elena Slobozeanu, Bogdan O. Postolnyi, Sebastian Balos, Antonella Rizzo, and Radu Robert Piticescu. Critical raw materials saving by protective coatings under extreme conditions: a review of last trends in alloys and coatings for aerospace engine applications. Materials, 14:1656, Mar 2021. URL: https://doi.org/10.3390/ma14071656, doi:10.3390/ma14071656. This article has 112 citations.

7. (helbig2020supplyriskconsiderations pages 3-5): Christoph Helbig, Alex M. Bradshaw, Andrea Thorenz, and Axel Tuma. Supply risk considerations for the elements in nickel-based superalloys. Resources, 9:106, Aug 2020. URL: https://doi.org/10.3390/resources9090106, doi:10.3390/resources9090106. This article has 25 citations.

8. (staff2024usgsmineralreview media 73ac4725): U Staff. Usgs mineral review. Unknown journal, 2024.

9. (bauer20232023criticalmaterials pages 34-36): Diana Bauer, Helena Khazdozian, Jeremy Mehta, Ruby Nguyen, Michael Severson, Bjorn Vaagensmith, Lionel Toba, Bo Zhang, Tasmin Hossain, Adam Sibal, Braeton Smith, Matthew Riddle, Diane Graziano, Tony Mathew, Patrick Cuscaden, Qiang Dai, Chukwunwike Iloeje, Lesley Edgemon, Caitlyn Sarna, and Julian Quaresima. 2023 critical materials strategy. ArXiv, Jul 2023. URL: https://doi.org/10.2172/1998242, doi:10.2172/1998242. This article has 18 citations.

10. (sims2016ceriumbasedintermetallicstrengthenedaluminum pages 1-3): Zachary C. Sims, David Weiss, Scott K. McCall, Michael A. McGuire, Ryan T. Ott, Tom Geer, O. Rios, and P. Turchi. Cerium-based, intermetallic-strengthened aluminum casting alloy: high-volume co-product development. JOM, 68:1940-1947, May 2016. URL: https://doi.org/10.1007/s11837-016-1943-9, doi:10.1007/s11837-016-1943-9. This article has 202 citations and is from a peer-reviewed journal.

11. (sims2022howceriumand pages 1-3): Zachary C. Sims, Michael S. Kesler, Hunter B. Henderson, Emilio Castillo, Tomer Fishman, David Weiss, Prentice Singleton, Roderick Eggert, Scott K. McCall, and Orlando Rios. How cerium and lanthanum as coproducts promote stable rare earth production and new alloys. Journal of Sustainable Metallurgy, 8:1225-1234, Jul 2022. URL: https://doi.org/10.1007/s40831-022-00562-4, doi:10.1007/s40831-022-00562-4. This article has 75 citations and is from a peer-reviewed journal.

12. (sims2022howceriumand pages 3-5): Zachary C. Sims, Michael S. Kesler, Hunter B. Henderson, Emilio Castillo, Tomer Fishman, David Weiss, Prentice Singleton, Roderick Eggert, Scott K. McCall, and Orlando Rios. How cerium and lanthanum as coproducts promote stable rare earth production and new alloys. Journal of Sustainable Metallurgy, 8:1225-1234, Jul 2022. URL: https://doi.org/10.1007/s40831-022-00562-4, doi:10.1007/s40831-022-00562-4. This article has 75 citations and is from a peer-reviewed journal.

13. (nguyen2019anticipatingimpactsof pages 1-2): Ruby T. Nguyen, D. Devin Imholte, Orlando R. Rios, David Weiss, Zachary Sims, Eric Stromme, and Scott K. McCall. Anticipating impacts of introducing aluminum-cerium alloys into the united states automotive market. Resources, Conservation and Recycling, 144:340-349, May 2019. URL: https://doi.org/10.1016/j.resconrec.2019.02.009, doi:10.1016/j.resconrec.2019.02.009. This article has 56 citations.

14. (amon2025opportunitiesforcerium pages 1-4): Alfred Amon and Scott K. McCall. Opportunities for cerium valorization in the rare earth supply chain. The Minerals, Metals &amp; Materials Series, pages 245-252, Jan 2025. URL: https://doi.org/10.1007/978-3-031-80892-0\_23, doi:10.1007/978-3-031-80892-0\_23. This article has 0 citations.

15. (darolia2019developmentofstrong pages 1-3): R. Darolia. Development of strong, oxidation and corrosion resistant nickel-based superalloys: critical review of challenges, progress and prospects. International Materials Reviews, 64:355-380, Oct 2019. URL: https://doi.org/10.1080/09506608.2018.1516713, doi:10.1080/09506608.2018.1516713. This article has 352 citations and is from a domain leading peer-reviewed journal.

16. (bauer20232023criticalmaterials pages 1-9): Diana Bauer, Helena Khazdozian, Jeremy Mehta, Ruby Nguyen, Michael Severson, Bjorn Vaagensmith, Lionel Toba, Bo Zhang, Tasmin Hossain, Adam Sibal, Braeton Smith, Matthew Riddle, Diane Graziano, Tony Mathew, Patrick Cuscaden, Qiang Dai, Chukwunwike Iloeje, Lesley Edgemon, Caitlyn Sarna, and Julian Quaresima. 2023 critical materials strategy. ArXiv, Jul 2023. URL: https://doi.org/10.2172/1998242, doi:10.2172/1998242. This article has 18 citations.

17. (staff2024usgsmineralreview pages 8-10): U Staff. Usgs mineral review. Unknown journal, 2024.