# Edison Scientific LITERATURE_HIGH Output — DOE Critical Minerals Strategy & Policy Context

**Task ID:** `2b917608-113e-47de-8290-5faf39fb1b6b`
**Mode:** LITERATURE_HIGH | **Date:** 2026-04-10 | **Size:** ~33K chars
**Part of:** Topic 3B Deep-Dive Series (10 queries, ~331K chars total)

> *Raw Edison Scientific output below. The query prompt appears first, followed by the model's structured response.*

---

Question: 
RESEARCH QUESTION: What is DOE's overarching critical minerals strategy, and how does an AI-driven alloy discovery platform fit within it?

Context: Need to understand the broader DOE critical minerals ecosystem to position FLAIME correctly.

Investigate:
1. DOE Critical Minerals Strategy (2021) and updates: what are the 5 pillars?
2. Executive Order 14017 (Feb 2021) on supply chains: implications for critical minerals R&D
3. DOE's Critical Materials Assessment (2023): which materials are most critical and why?
4. How does DOE distinguish between "demand reduction" (substitution, efficiency) vs. "supply diversification" (mining, recycling)?
5. Which DOE offices fund critical minerals work? (AMMTO, BES, EERE, ARPA-E, others)
6. ARPA-E programs: ULTIMATE, METALS, OPEN — any relevant to alloy substitution?
7. IRA (Inflation Reduction Act) funding for critical minerals: how much and for what?
8. DOE's perspective on "alloy design for critical mineral reduction" — is this an established funding theme?
9. How does the Genesis Mission's critical minerals topic differ from existing DOE critical minerals programs?
10. What metrics does DOE use to evaluate "demand reduction" proposals? (kg displaced, cost savings, supply risk reduction)

Cite all sources.


## DOE overarching critical minerals/materials strategy and where an AI-driven alloy-discovery platform fits

### 1) DOE’s overarching strategy (the “five pillars” framework)
DOE’s updated strategy framework for critical minerals/materials is articulated as five pillars in its *2023 Critical Materials Strategy* (CMS), which states DOE’s strategic framework “will continue to focus on five pillars” and lists them explicitly (bauer20232023criticalmaterials pages 1-9). The pillars (with DOE’s intent language) are:

1. **Diversify & Expand Supply** — “Diversify and expand critical mineral and material supply from varying sources while minimizing waste and increasing techno-economic coproduction of materials – to ensure material availability.” (bauer20232023criticalmaterials pages 1-9)
2. **Develop Alternatives** — “Innovate alternative materials and/or manufacturing components – reduce demand and partially offset the need for virgin materials.” (bauer20232023criticalmaterials pages 1-9)
3. **Materials and Manufacturing Efficiency** — “Use and process materials efficiently across the entire supply chain and life cycle – to reduce waste.” (bauer20232023criticalmaterials pages 1-9)
4. **Circular Economy** — “Remanufacture, refurbish, repair, reuse, recycle, and repurpose – to extend the lifetime of materials and partially offset the need for virgin materials.” (bauer20232023criticalmaterials pages 1-9)
5. **Enabling Activities** — Cross-cutting functions including “criticality assessments, stockpiling, international engagement, market development, and advanced theoretical, computational, and experimental tools – to accelerate progress.” (bauer20232023criticalmaterials pages 1-9)

**Key implication for positioning FLAIME (AI alloy discovery):** DOE’s strategy is explicitly not only supply-side; it has multiple demand-side pillars (alternatives/substitution, efficiency, and circularity). An AI-driven alloy discovery platform is naturally aligned to these demand-side pillars and to the “Enabling Activities” pillar (advanced computational tools) (bauer20232023criticalmaterials pages 1-9).

### 2) Executive Order 14017 (Feb 2021) and implications for critical minerals R&D
DOE’s supply-chain work in 2021–2022 is explicitly framed as a response to **Executive Order (EO) 14017, “America’s Supply Chains,”** which directed the Secretary of Energy to evaluate energy-sector supply chains and produce a report; DOE responded with an energy supply chain strategy report and a set of “deep dive” assessments within the EO’s one-year timeframe (mann2022gridenergystorage pages 1-8, finan2022nuclearenergy pages 1-7). In that response:

- DOE identifies **critical-mineral-dependent technologies** and crosscutting topics as priorities, explicitly including **neodymium magnets** and **platinum group metals and other catalysts** (mann2022gridenergystorage pages 1-8, finan2022nuclearenergy pages 1-7).
- DOE uses a structured analytic approach including prioritization, supply baselines, demand forecasting, U.S. economics of production, policy analysis, and scenario analysis/“war-gaming” (chan2022competitivenessandcommercialization pages 1-7).
- DOE’s broader EO-14017-linked supply-chain strategy discussions emphasize both **supply measures** (domestic mining/processing, demonstrations and financing) and **demand-side measures** (substitution and design-for-recycling), e.g., support for substitution technologies to reduce dependence on rare earths and PGMs and funding for processing/manufacturing/recycling plus rare-earth facility demonstration (igogo2022americasstrategyto pages 40-43).

**Implication:** EO 14017 drove DOE to treat critical minerals as a supply-chain vulnerability that can be mitigated by (i) expanding/reshoring supply chains and (ii) technology innovation that reduces reliance (substitution, efficiency, recycling)—creating a policy basis for R&D platforms that can rapidly generate substitute/low-criticality materials (igogo2022americasstrategyto pages 40-43, chan2022competitivenessandcommercialization pages 1-7).

### 3) DOE Critical Materials Assessment (2023): what materials are “most critical” and why
In DOE’s 2023 CMS, DOE describes its **Critical Materials Assessment** as an updated, energy-application-driven criticality analysis using two primary axes:

- **Importance to clean energy technologies** (importance-to-energy)
- **Supply risk**

DOE defines three categories: materials scoring **≥3 on both axes are “critical,”** materials scoring **≥3 on one axis and 2 on the other are “near critical,”** and others are “not critical,” applied for short-term (2020–2025) and medium-term (2025–2035) windows (bauer20232023criticalmaterials pages 133-136).

**Short-term (2020–2025) “critical” materials (DOE list):** cobalt, dysprosium, gallium, natural graphite, iridium, neodymium, terbium (bauer20232023criticalmaterials pages 133-136, bauer20232023criticalmaterials pages 16-18).

**Short-term “near critical” materials (DOE list):** electrical steel, fluorine, lithium, magnesium, nickel, platinum, praseodymium, silicon carbide (SiC), uranium (bauer20232023criticalmaterials pages 133-136, bauer20232023criticalmaterials pages 16-18).

DOE also documents that scores can shift over time due to market dynamics, substitutes, and technology deployment trends, and it describes a screening process for which materials enter detailed assessment (bauer20232023criticalmaterials pages 133-136, bauer20232023criticalmaterials pages 76-78).

**Implication for alloy design:** Several short-term critical/near-critical items (e.g., cobalt, nickel, magnesium, electrical steel, rare earths) are used heavily in devices where alloy and materials design can change bill-of-materials intensity (e.g., structural alloys, magnet alloys, high-temperature alloys), making “Develop Alternatives” and “Materials and Manufacturing Efficiency” directly relevant (bauer20232023criticalmaterials pages 1-9, lograsso2024criticalmaterialsinstitute pages 6-9).

### 4) DOE framing: “demand reduction” vs “supply diversification”
DOE operationalizes the distinction via its pillar structure:

- **Supply diversification/expansion** is principally under **“Diversify & Expand Supply”** (diversify and expand supply sources; coproduction; availability focus) (bauer20232023criticalmaterials pages 1-9).
- **Demand reduction** is distributed across:
  - **Develop Alternatives** (explicitly “reduce demand”) (bauer20232023criticalmaterials pages 1-9)
  - **Materials and Manufacturing Efficiency** (reduce waste via more efficient use/processing) (bauer20232023criticalmaterials pages 1-9)
  - **Circular Economy** (extend lifetime; reuse/recycle; offset virgin materials) (bauer20232023criticalmaterials pages 1-9)

DOE’s EO-14017-linked supply-chain strategy discussion likewise places **substitution, efficiency, and design-for-reuse/recycling** alongside supply actions like mining/processing demonstrations and financing (igogo2022americasstrategyto pages 40-43).

### 5) Which DOE offices/channels fund critical minerals work (as explicitly supported in the retrieved corpus)
Across the retrieved DOE-related sources, explicit offices and channels include:

- **AMMTO** and the **Critical Materials Research, Development, Demonstration, and Commercialization Application (RDD&CA) Program** (Energy Act of 2020) as a DOE implementation vehicle for critical materials priorities (bauer20232023criticalmaterials pages 1-9).
- **EERE** funding the **Critical Materials Institute (CMI)** for supply diversification, substitutes, and recycling/reuse (igogo2022americasstrategyto pages 38-40).
- **FECM** (Fossil Energy and Carbon Management) creating a **Mineral Sustainability** subprogram (recovery of rare earths/critical materials from coal waste and by-products) (igogo2022americasstrategyto pages 38-40).
- DOE **Loan Programs Office (LPO)** financing and authorities as part of the critical-minerals supply-chain toolkit (igogo2022americasstrategyto pages 40-43, igogo2022americasstrategyto pages 43-45).
- DOE **SBIR/STTR** programs (commercialization-oriented R&D finance mechanisms referenced in the supply-chain context) (igogo2022americasstrategyto pages 40-43, igogo2022americasstrategyto pages 43-45).
- **NETL / Office of Fossil Energy** programs related to rare earth recovery from coal and coal byproducts (policy analysis evidence) (he2018thetradesecuritynexus pages 7-8).

**Note on BES/Office of Science:** BES and related Office of Science programs are not explicitly identified in the evidence snippets retrieved here; therefore they are not asserted as “funders” in this report, even though they may do so in DOE’s broader ecosystem.

### 6) ARPA‑E programs relevant to alloy substitution and materials efficiency (ULTIMATE, METALS, OPEN)
Evidence in the retrieved corpus shows multiple ARPA‑E programmatic “homes” for alloy-oriented demand reduction and efficiency:

- **METALS (Modern Electro/Thermochemical Advances in Light Metal Systems):** described as targeting efficient production and recycling of Al/Mg/Ti to lower cost and energy use (rohlfing2017arpaeimpactsa pages 7-10). Example outcomes include aluminum scrap sorting/decoating/melt certification and large projected energy savings relative to conventional aluminum production routes (xu2018arpaeimpactsa pages 11-14).
- **OPEN:** includes an ORNL alloy project explicitly motivated by **reducing chromium use** because chromium is described as critical and not domestically available; the project aims to develop lower-Cr alternatives (alumina-forming Fe-base austenitic alloys) (xu2018arpaeimpactsa pages 1-6).
- **ULTIMATE:** an ARPA‑E-funded alloy program evidenced here via a project that uses ML-guided alloy discovery and experimental down-selection against explicit high-temperature alloy performance metrics (melt point, density, ductility, and strength at 1300°C), illustrating ARPA‑E’s support for accelerated computational alloy discovery methods (sharon2023computationallyguidedodsrefractory pages 4-6).

### 7) IRA (Inflation Reduction Act) funding mechanisms relevant to critical minerals
Within the retrieved corpus, the IRA’s critical-minerals relevance is expressed through both **production incentives** and **DOE finance/industrial policy tools**:

- **45X Advanced Manufacturing Production Credit** provides production incentives for battery supply-chain elements, including **“critical minerals — 10% of the production cost”** and **electrode active materials — 10% of production cost**, as well as $35/kWh for battery cells and $10/kWh for modules (allan2026u.s.cleanenergy pages 1-4).
- **Defense Production Act (DPA) funding**: IRA appropriates **up to $500M** for enhanced use of DPA to support critical mineral production (ewing2023strengtheningsupplychains pages 9-12).
- **DOE ATVM loans**: IRA removed the ATVM loan cap and appropriated **$3B** (available through 2028) (lodge2024reapplicationfora pages 57-59).
- A summary source lists IRA “credit-subsidy” allocations and related lines including **DOE LPO Title 17 ($3.6B)**, **LPO Advanced Technology Vehicles ($3.0B)**, and **Domestic Manufacturing Conversion Grants ($2.0B)** (zolnowski2024tenstepstoa pages 23-26).

### 8) DOE perspective on “alloy design for critical mineral reduction”: established theme?
Within the accessible corpus, “alloy design/substitution to reduce critical-material dependence” is an established theme in practice and program structure:

- DOE’s strategy explicitly includes **Develop Alternatives** (demand reduction via alternative materials/components) and **Materials and Manufacturing Efficiency** (waste/material-intensity reduction) (bauer20232023criticalmaterials pages 1-9).
- ARPA‑E OPEN contains an explicit alloy example framed as reducing a critical material input (lower-Cr alloy alternatives) (xu2018arpaeimpactsa pages 1-6).
- ARPA‑E ULTIMATE supports accelerated alloy discovery with advanced computational + experimental down-selection (sharon2023computationallyguidedodsrefractory pages 4-6).
- CMI explicitly prioritizes “developing substitutes” and maintains enabling computational/experimental capabilities plus TEA to evaluate feasibility and guide planning (lograsso2024criticalmaterialsinstitute pages 9-11).

Because FOA text and proposal evaluation criteria were not retrieved in this corpus, this conclusion is grounded in program/project documentation rather than solicitation language.

### 9) How an AI-driven alloy discovery platform fits within DOE’s strategy
An AI-driven alloy discovery platform (e.g., FLAIME) fits most directly as:

- A **demand reduction** tool under **Develop Alternatives** (substitution) and **Materials and Manufacturing Efficiency** (reduced material intensity, improved yield/scrap reduction), and as a **circularity enabler** if it designs for recyclability and recycled-feedstock tolerance (bauer20232023criticalmaterials pages 1-9, upasani2022mappingtheopportunity pages 34-37).
- An **Enabling Activities** capability, because DOE explicitly frames “advanced theoretical, computational, and experimental tools” as cross-cutting accelerators of progress (bauer20232023criticalmaterials pages 1-9), and ARPA‑E practice shows ML-guided alloy discovery paired with experimental validation and manufacturability constraints (sharon2023computationallyguidedodsrefractory pages 4-6).

A practical way to position such a platform to DOE is therefore:

1. **Start from DOE’s “most critical” materials** (short-term critical list) and select high-leverage substitution targets (e.g., reducing cobalt use in alloys/components or avoiding rare-earth-containing alloy systems in certain applications), while ensuring performance parity and manufacturability (bauer20232023criticalmaterials pages 133-136, sharon2023computationallyguidedodsrefractory pages 4-6).
2. **Quantify outcomes in DOE-recognized metric families**: mass-based virgin material offset (via virgin material use avoided/material flow rates), circularity measures, and LCA/TEA outcomes (GHG/energy/water; cost/ROI/break-even) (upasani2022mappingtheopportunity pages 42-44, upasani2022mappingtheopportunity pages 34-37, lograsso2024criticalmaterialsinstitute pages 9-11).
3. **Connect to the right DOE channels** depending on maturity: early-stage computational+experimental workflows via ARPA‑E (ULTIMATE/OPEN-like models), scaling via AMMTO/RDD&CA, and manufacturing/finance scaling via LPO and IRA-linked incentives (bauer20232023criticalmaterials pages 1-9, allan2026u.s.cleanenergy pages 1-4, zolnowski2024tenstepstoa pages 23-26).

The table below maps DOE pillars to how an AI alloy platform supports them and suggests evidence-based metrics.

| DOE pillar (exact wording) | Pillar intent (1 sentence) | Example DOE programs/offices mentioned in evidence | How AI alloy discovery fits (demand reduction vs supply diversification) | Suggested quantitative metrics |
|---|---|---|---|---|
| Diversify & Expand Supply | Diversify and expand critical mineral and material supply from varying sources while minimizing waste and increasing techno-economic coproduction to ensure availability. (bauer20232023criticalmaterials pages 1-9) | FECM Mineral Sustainability subprogram; rare earth elements demonstration program; DOE Critical Materials RDD&CA Program; Loan Programs Office; Critical Materials Institute/CMI. (igogo2022americasstrategyto pages 38-40, bauer20232023criticalmaterials pages 1-9, igogo2022americasstrategyto pages 40-43) | Mostly indirect fit: AI alloy discovery contributes only secondarily by reducing pressure on virgin supply; pillar is primarily supply diversification, mining/processing, recycling feedstock expansion, and coproduction. (igogo2022americasstrategyto pages 38-40, igogo2022americasstrategyto pages 40-43) | Reduced virgin material demand for target critical element (kg/year); reduced dependence on high-risk import share proxy; change in projected material demand relative to baseline technology; cost impact of avoided virgin input use. (bauer20232023criticalmaterials pages 1-9, upasani2022mappingtheopportunity pages 42-44, upasani2022mappingtheopportunity pages 58-60) |
| Develop Alternatives | Innovate alternative materials and/or manufacturing components to reduce demand and partially offset the need for virgin materials. (bauer20232023criticalmaterials pages 1-9) | EERE-funded CMI; ARPA-E OPEN alloy work on lower-Cr alternatives; ARPA-E REACT-related substitution context; DOE-funded substitute development activities. (igogo2022americasstrategyto pages 38-40, xu2018arpaeimpactsa pages 1-6, rohlfing2017arpaeimpactsa pages 7-10) | Primary fit: AI-driven alloy discovery is a demand-reduction/substitution tool that designs lower-criticality alloys or components delivering required performance with less or no scarce material. (xu2018arpaeimpactsa pages 1-6, igogo2022americasstrategyto pages 38-40, igogo2022americasstrategyto pages 40-43) | kg critical material displaced per unit and per year; % reduction in critical element content; performance parity vs incumbent alloy; supply-risk reduction proxy using DOE criticality category or import-concentration proxy; cost per kg displaced. (bauer20232023criticalmaterials pages 133-136, bauer20232023criticalmaterials pages 16-18, upasani2022mappingtheopportunity pages 42-44, upasani2022mappingtheopportunity pages 58-60) |
| Materials and Manufacturing Efficiency | Use and process materials efficiently across the entire supply chain and life cycle to reduce waste. (bauer20232023criticalmaterials pages 1-9) | ARPA-E METALS; DOE advanced manufacturing/AM-related efforts; Advanced Manufacturing Office/AMMTO authorship in DOE strategy. (bauer20232023criticalmaterials pages 1-9, xu2018arpaeimpactsa pages 1-6, xu2018arpaeimpactsa pages 11-14) | Strong fit: AI can optimize composition for manufacturability/yield and enable equivalent performance with lower material intensity, less scrap, and better process efficiency. This is demand reduction through efficiency rather than new supply. (xu2018arpaeimpactsa pages 1-6, xu2018arpaeimpactsa pages 11-14, bauer20232023criticalmaterials pages 1-9) | Manufacturing yield improvement (%); scrap reduction (kg/unit); material intensity reduction (kg critical element per component); energy savings in production (MJ or %); production cost savings ($/unit). (xu2018arpaeimpactsa pages 11-14, upasani2022mappingtheopportunity pages 34-37, upasani2022mappingtheopportunity pages 58-60) |
| Circular Economy | Remanufacture, refurbish, repair, reuse, recycle, and repurpose to extend the lifetime of materials and partially offset the need for virgin materials. (bauer20232023criticalmaterials pages 1-9) | BIL battery and critical mineral recycling programs; DOE circular-economy modeling tools (CELAVI, GREET, EverBatt, etc.); CMI recycling/reuse efforts. (igogo2022americasstrategyto pages 38-40, igogo2022americasstrategyto pages 54-57, upasani2022mappingtheopportunity pages 34-37, upasani2022mappingtheopportunity pages 58-60) | Partial fit: AI alloy discovery can design alloys for easier recyclability/reuse or compatibility with recycled feedstocks, reducing virgin demand through circularity rather than primary extraction. (igogo2022americasstrategyto pages 40-43, upasani2022mappingtheopportunity pages 34-37, upasani2022mappingtheopportunity pages 42-44) | Virgin material use avoided (kg); recovered/recirculated material fraction (%); solid waste generation (kg); in-flow/out-flow circularity (%); GHG, energy, and water impacts from LCA. (upasani2022mappingtheopportunity pages 34-37, upasani2022mappingtheopportunity pages 42-44, upasani2022mappingtheopportunity pages 58-60) |
| Enabling Activities | Use cross-cutting functions such as criticality assessments, stockpiling, international engagement, market development, and advanced theoretical, computational, and experimental tools to accelerate progress. (bauer20232023criticalmaterials pages 1-9) | DOE Critical Materials RDD&CA Program; FY2022 Critical Minerals and Materials crosscut; DOE hub-and-spoke market analysis; national labs; stakeholder RFIs and deep-dive assessments under EO 14017. (chan2022competitivenessandcommercialization pages 1-7, igogo2022americasstrategyto pages 38-40, igogo2022americasstrategyto pages 40-43, bauer20232023criticalmaterials pages 1-9) | Excellent fit: an AI-driven alloy discovery platform is best positioned as an enabling computational tool that accelerates substitution, efficiency, and design-for-circularity across multiple pillars. (bauer20232023criticalmaterials pages 1-9, sharon2023computationallyguidedodsrefractory pages 7-10, sharon2023computationallyguidedodsrefractory pages 4-6) | Time-to-discovery reduction; number of candidate alloys screened/validated; probability of meeting target specs; uncertainty-bounded supply-risk reduction scenarios; techno-economic and LCA outputs for each candidate. (bauer20232023criticalmaterials pages 1-9, sharon2023computationallyguidedodsrefractory pages 4-6, upasani2022mappingtheopportunity pages 34-37, upasani2022mappingtheopportunity pages 31-34) |


*Table: This table maps DOE’s five critical materials strategy pillars to where an AI-driven alloy discovery platform most naturally fits. It is useful for positioning such a platform as primarily an enabling and demand-reduction capability, while showing secondary relevance to efficiency and circular-economy goals.*

### 10) Genesis Mission comparison (limitation)
No primary “Genesis Mission” critical-minerals topic document was retrievable in the current corpus, so a direct, cited comparison to DOE’s existing critical-minerals programs cannot be made here without speculation (caers2023testimonybeforethe pages 1-4). The positioning guidance above therefore anchors to DOE’s established pillars, assessment framework, and program vehicles.

## Conclusion
DOE’s overarching critical minerals/materials strategy is a five-pillar framework balancing supply diversification with demand reduction (substitution, efficiency) and circularity, supported by enabling activities including advanced computational/experimental tools (bauer20232023criticalmaterials pages 1-9). DOE’s 2023 assessment prioritizes materials by supply risk and importance to clean energy, identifying a short-term critical list dominated by battery and magnet-related materials (bauer20232023criticalmaterials pages 133-136). An AI-driven alloy discovery platform fits squarely within DOE’s “Develop Alternatives” and “Enabling Activities” pillars, with strong additional relevance to manufacturing efficiency and circular economy goals, and can be framed with DOE-aligned quantification (virgin material use avoided; circularity; LCA/TEA metrics) and DOE-aligned funding pathways (ARPA‑E → AMMTO/RDD&CA → LPO/IRA-enabled scale-up) (upasani2022mappingtheopportunity pages 34-37, bauer20232023criticalmaterials pages 1-9, allan2026u.s.cleanenergy pages 1-4).

References

1. (bauer20232023criticalmaterials pages 1-9): Diana Bauer, Helena Khazdozian, Jeremy Mehta, Ruby Nguyen, Michael Severson, Bjorn Vaagensmith, Lionel Toba, Bo Zhang, Tasmin Hossain, Adam Sibal, Braeton Smith, Matthew Riddle, Diane Graziano, Tony Mathew, Patrick Cuscaden, Qiang Dai, Chukwunwike Iloeje, Lesley Edgemon, Caitlyn Sarna, and Julian Quaresima. 2023 critical materials strategy. ArXiv, Jul 2023. URL: https://doi.org/10.2172/1998242, doi:10.2172/1998242. This article has 18 citations.

2. (mann2022gridenergystorage pages 1-8): Margaret Mann, Vicky Putsche, and Benjamin Shrager. Grid energy storage - supply chain deep dive assessment. ArXiv, Feb 2022. URL: https://doi.org/10.2172/1871557, doi:10.2172/1871557. This article has 14 citations.

3. (finan2022nuclearenergy pages 1-7): Ashley Finan, Andrew Foss, Michael Goff, Christine King, and Christopher Lohse. Nuclear energy - supply chain deep dive assessment. ArXiv, Feb 2022. URL: https://doi.org/10.2172/1871579, doi:10.2172/1871579. This article has 18 citations.

4. (chan2022competitivenessandcommercialization pages 1-7): Vanessa Chan, Stephen Hendrickson, Lucia Tian, Allison Irion, Matthew Riddle, and Braeton Smith. Competitiveness and commercialization of energy technologies - supply chain deep dive assessment. ArXiv, Feb 2022. URL: https://doi.org/10.2172/1871592, doi:10.2172/1871592. This article has 1 citations.

5. (igogo2022americasstrategyto pages 40-43): Tsisilile A Igogo. America's strategy to secure the supply chain for a robust clean energy transition. ArXiv, Feb 2022. URL: https://doi.org/10.2172/1871491, doi:10.2172/1871491. This article has 27 citations.

6. (bauer20232023criticalmaterials pages 133-136): Diana Bauer, Helena Khazdozian, Jeremy Mehta, Ruby Nguyen, Michael Severson, Bjorn Vaagensmith, Lionel Toba, Bo Zhang, Tasmin Hossain, Adam Sibal, Braeton Smith, Matthew Riddle, Diane Graziano, Tony Mathew, Patrick Cuscaden, Qiang Dai, Chukwunwike Iloeje, Lesley Edgemon, Caitlyn Sarna, and Julian Quaresima. 2023 critical materials strategy. ArXiv, Jul 2023. URL: https://doi.org/10.2172/1998242, doi:10.2172/1998242. This article has 18 citations.

7. (bauer20232023criticalmaterials pages 16-18): Diana Bauer, Helena Khazdozian, Jeremy Mehta, Ruby Nguyen, Michael Severson, Bjorn Vaagensmith, Lionel Toba, Bo Zhang, Tasmin Hossain, Adam Sibal, Braeton Smith, Matthew Riddle, Diane Graziano, Tony Mathew, Patrick Cuscaden, Qiang Dai, Chukwunwike Iloeje, Lesley Edgemon, Caitlyn Sarna, and Julian Quaresima. 2023 critical materials strategy. ArXiv, Jul 2023. URL: https://doi.org/10.2172/1998242, doi:10.2172/1998242. This article has 18 citations.

8. (bauer20232023criticalmaterials pages 76-78): Diana Bauer, Helena Khazdozian, Jeremy Mehta, Ruby Nguyen, Michael Severson, Bjorn Vaagensmith, Lionel Toba, Bo Zhang, Tasmin Hossain, Adam Sibal, Braeton Smith, Matthew Riddle, Diane Graziano, Tony Mathew, Patrick Cuscaden, Qiang Dai, Chukwunwike Iloeje, Lesley Edgemon, Caitlyn Sarna, and Julian Quaresima. 2023 critical materials strategy. ArXiv, Jul 2023. URL: https://doi.org/10.2172/1998242, doi:10.2172/1998242. This article has 18 citations.

9. (lograsso2024criticalmaterialsinstitute pages 6-9): Thomas Lograsso, Bruce Moyer, and Melinda Thach. Critical materials institute (cmi) year 10 cumulative report. ArXiv, Apr 2024. URL: https://doi.org/10.2172/2338076, doi:10.2172/2338076. This article has 1 citations.

10. (igogo2022americasstrategyto pages 38-40): Tsisilile A Igogo. America's strategy to secure the supply chain for a robust clean energy transition. ArXiv, Feb 2022. URL: https://doi.org/10.2172/1871491, doi:10.2172/1871491. This article has 27 citations.

11. (igogo2022americasstrategyto pages 43-45): Tsisilile A Igogo. America's strategy to secure the supply chain for a robust clean energy transition. ArXiv, Feb 2022. URL: https://doi.org/10.2172/1871491, doi:10.2172/1871491. This article has 27 citations.

12. (he2018thetradesecuritynexus pages 7-8): Yujia He. The trade-security nexus and u.s. policy making in critical minerals. Resources Policy, 59:238-249, Dec 2018. URL: https://doi.org/10.1016/j.resourpol.2018.07.010, doi:10.1016/j.resourpol.2018.07.010. This article has 40 citations and is from a peer-reviewed journal.

13. (rohlfing2017arpaeimpactsa pages 7-10): Eric Rohlfing. Arpa-e impacts: a sampling of project outcomes, volume ii. ArXiv, Feb 2017. URL: https://doi.org/10.2172/1346817, doi:10.2172/1346817. This article has 0 citations.

14. (xu2018arpaeimpactsa pages 11-14): Yanzhi Ann Xu. Arpa-e impacts: a sampling of project outcomes, volume iii. ArXiv, Jun 2018. URL: https://doi.org/10.2172/1464210, doi:10.2172/1464210. This article has 1 citations.

15. (xu2018arpaeimpactsa pages 1-6): Yanzhi Ann Xu. Arpa-e impacts: a sampling of project outcomes, volume iii. ArXiv, Jun 2018. URL: https://doi.org/10.2172/1464210, doi:10.2172/1464210. This article has 1 citations.

16. (sharon2023computationallyguidedodsrefractory pages 4-6): John Sharon, Anthony Ventura, Ryan Deacon, Ken Smith, and Soumalya Sarkar. Computationally-guided ods refractory heas via additive manufacturing. ArXiv, Oct 2023. URL: https://doi.org/10.2172/2375527, doi:10.2172/2375527. This article has 0 citations.

17. (allan2026u.s.cleanenergy pages 1-4): Bentley B. Allan, Jonas Goldman, and Shreyas Shende. U.s. clean energy supply chains after the <i>inflation reduction act</i>. Environmental Research Letters, 21:034019, Feb 2026. URL: https://doi.org/10.1088/1748-9326/ae2698, doi:10.1088/1748-9326/ae2698. This article has 0 citations and is from a highest quality peer-reviewed journal.

18. (ewing2023strengtheningsupplychains pages 9-12): J Ewing, R Earnhardt, M Carlson, and J Reeves. Strengthening supply chains for us decarbonization. Unknown journal, 2023.

19. (lodge2024reapplicationfora pages 57-59): MM Lodge and DS General. Re: application for observer status. Unknown journal, 2024.

20. (zolnowski2024tenstepstoa pages 23-26): MD Zolnowski and LLC Greyfriars. Ten steps to achieve resilient cobalt supply chains. Unknown journal, 2024.

21. (lograsso2024criticalmaterialsinstitute pages 9-11): Thomas Lograsso, Bruce Moyer, and Melinda Thach. Critical materials institute (cmi) year 10 cumulative report. ArXiv, Apr 2024. URL: https://doi.org/10.2172/2338076, doi:10.2172/2338076. This article has 1 citations.

22. (upasani2022mappingtheopportunity pages 34-37): Shubhankar Upasani, Julien Walzberg, Dwarakanath Ravikumar, A. Carpenter, G. Heath, Ulises R. Gracida-Alvarez, Thathiana Benavides, Hui Xu, Troy R. Hawkins, Daniel Desantis, and J. Cresko. Mapping the opportunity space to model the circular economy using tools funded by the doe office of energy efficiency and renewable energy. ArXiv, Apr 2022. URL: https://doi.org/10.2172/1863766, doi:10.2172/1863766. This article has 6 citations.

23. (upasani2022mappingtheopportunity pages 42-44): Shubhankar Upasani, Julien Walzberg, Dwarakanath Ravikumar, A. Carpenter, G. Heath, Ulises R. Gracida-Alvarez, Thathiana Benavides, Hui Xu, Troy R. Hawkins, Daniel Desantis, and J. Cresko. Mapping the opportunity space to model the circular economy using tools funded by the doe office of energy efficiency and renewable energy. ArXiv, Apr 2022. URL: https://doi.org/10.2172/1863766, doi:10.2172/1863766. This article has 6 citations.

24. (upasani2022mappingtheopportunity pages 58-60): Shubhankar Upasani, Julien Walzberg, Dwarakanath Ravikumar, A. Carpenter, G. Heath, Ulises R. Gracida-Alvarez, Thathiana Benavides, Hui Xu, Troy R. Hawkins, Daniel Desantis, and J. Cresko. Mapping the opportunity space to model the circular economy using tools funded by the doe office of energy efficiency and renewable energy. ArXiv, Apr 2022. URL: https://doi.org/10.2172/1863766, doi:10.2172/1863766. This article has 6 citations.

25. (igogo2022americasstrategyto pages 54-57): Tsisilile A Igogo. America's strategy to secure the supply chain for a robust clean energy transition. ArXiv, Feb 2022. URL: https://doi.org/10.2172/1871491, doi:10.2172/1871491. This article has 27 citations.

26. (sharon2023computationallyguidedodsrefractory pages 7-10): John Sharon, Anthony Ventura, Ryan Deacon, Ken Smith, and Soumalya Sarkar. Computationally-guided ods refractory heas via additive manufacturing. ArXiv, Oct 2023. URL: https://doi.org/10.2172/2375527, doi:10.2172/2375527. This article has 0 citations.

27. (upasani2022mappingtheopportunity pages 31-34): Shubhankar Upasani, Julien Walzberg, Dwarakanath Ravikumar, A. Carpenter, G. Heath, Ulises R. Gracida-Alvarez, Thathiana Benavides, Hui Xu, Troy R. Hawkins, Daniel Desantis, and J. Cresko. Mapping the opportunity space to model the circular economy using tools funded by the doe office of energy efficiency and renewable energy. ArXiv, Apr 2022. URL: https://doi.org/10.2172/1863766, doi:10.2172/1863766. This article has 6 citations.

28. (caers2023testimonybeforethe pages 1-4): J Caers. Testimony before the us house of representatives committee on science, space, and technology. Unknown journal, 2023.