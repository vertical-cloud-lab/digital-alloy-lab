<!--
Edison Scientific LITERATURE task (batch 5)
- Task ID: 3dc07109-89a5-41f4-a7f8-cef0e9d895c6
- Submitted: 2026-10-17T06:20:08Z
- Fetched: 2026-10-17T06:51:59Z (status: success)
- Raw trajectory JSON: ../raw/b5-08-point-of-need-recycling.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What work exists on turning naval or maritime copper alloy scrap
(NAB propeller grinding chips, Cu-Ni pipe offcuts, cable copper) into AM
feedstock at or near the point of need, and what does it show about powder
quality, cost, energy, and logistics? Cover the EU MarTERA project
(Uhlmann et al. 2024; Mueller et al. 2021, 2023), Cabrioli et al. 2025
(rePOWDER atomization of offshore-cable copper for laser DED, life-cycle
assessment), Navy or DoD expeditionary or shipyard powder-making efforts
(e.g. recycling chips on ships, ultrasonic atomizers on vessels), and any
analysis of how small-lot atomization changes qualification. Quote numbers
(yields, oxygen, energy, CO2) where reported.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What work exists on turning naval or maritime copper alloy scrap
(NAB propeller grinding chips, Cu-Ni pipe offcuts, cable copper) into AM
feedstock at or near the point of need, and what does it show about powder
quality, cost, energy, and logistics? Cover the EU MarTERA project
(Uhlmann et al. 2024; Mueller et al. 2021, 2023), Cabrioli et al. 2025
(rePOWDER atomization of offshore-cable copper for laser DED, life-cycle
assessment), Navy or DoD expeditionary or shipyard powder-making efforts
(e.g. recycling chips on ships, ultrasonic atomizers on vessels), and any
analysis of how small-lot atomization changes qualification. Quote numbers
(yields, oxygen, energy, CO2) where reported.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.


# Maritime copper scrap as additive-manufacturing feedstock

**Bottom line.** Published work demonstrates that ship-propeller nickel–aluminium bronze (NAB) grinding chips can be converted into unusually spherical, low-oxygen powder, and that recovered offshore-cable copper can be atomized and laser-deposited. It does **not** establish a qualified, shipboard scrap-to-powder-to-repair route, nor as-deposited seawater performance comparable with wrought C71500. The distinction matters: powder characterization, a successful deposition, and a life-cycle model answer different questions. (uhlmann2024acomparativeevaluation pages 1-2, uhlmann2024acomparativeevaluation pages 13-15, saai2025comparativelifecycle pages 1-2, strieby2024operationalizingmetaladditive pages 1-9)

**1. Uhlmann, E.; Polte, J.; Fasselt, J. M.; Müller, V.; Klötzer-Freese, C.; Kleba-Ehrhardt, R.; Biegler, M.; Rethmeier, M.** “A Comparative Evaluation of Powder Characteristics of Recycled Material from Bronze Grinding Chips for Additive Manufacturing.” *Materials* **17** (2024), 3396. **DOI:** 10.3390/ma17143396. **Process:** propeller-grinding chips → ball milling, impact-whirl milling, or argon-shielded ultrasonic remelting/atomization; powders intended for **blown-powder laser DED**, not an alloy-design or deposited-part qualification study. **Alloy:** cast NAB CC333G, nominal CuAl10Ni5Fe5; its specified ranges are Cu 76–83, Al 8.5–10.5, Fe 4.0–5.5, Ni 4.0–6.0 and Mn ≤3.0 wt%. The measured atomized sample was Cu 75.16, Al 9.83, Fe 6.76, Ni 5.91 and Mn 2.33 wt% by EDX; the authors caution against treating EDX as precise bulk chemical certification. Its gas-atomized *comparison* powder was a different, essentially Ni-free Cu–Al–Fe alloy. The ultrasonic run used an AUS 500, a 1,300 °C melt, 40-kHz sonotrode, argon and a 200-µm spatter-removal sieve. (uhlmann2024acomparativeevaluation pages 2-4, uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 7-10)

**Powder benchmarks:** ultrasonic powder particle-size *percentiles* X₁₀/X₅₀/X₉₀ were **48/98/174 µm**; mean aspect ratio **0.935**, with **82%** of particles above aspect ratio 0.9, versus **43.5%** for the different-composition commercial reference. Oxygen was **0.013 wt%** in ultrasonic powder, **0.073 wt%** in starting chips, **0.019 wt%** in the commercial reference, **0.186–0.190 wt%** after ball milling, and **0.119–0.141 wt%** after impact-whirl milling. Carney—not Hall—flow times were **8.62 s/150 g** (ultrasonic), **10.55** (reference), **17.35/17.03** (ball milling) and **26.17/14.13** (impact-whirl milling at 3,000/8,000 rpm); the ultrasonic powder’s Hausner ratio was **1.05**. These particle-size percentiles and the **82% shape statistic are not mass yields** of usable DED powder. Ceramic grinding-abrasive contamination persisted, and the ultrasonic powder contained some sonotrode-derived carbon fibres. **Not reported here:** measured atomization yield, electricity, powder cost, CO₂, deposited density/porosity, strength, hardness or corrosion. The authors expressly call for actual powder-feeder, deposit-property and environmental/economic testing. **Test conditions:** powder tests only; no NaCl/seawater exposure or immersion duration. **[CITE] [NUMBERS] [NOVELTY-RISK]** Direct precedent for recycled pre-alloyed NAB and in-house ultrasonic powder; **[GAP]** no validated repair or seawater-qualified deposit. (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 6-7, uhlmann2024acomparativeevaluation pages 13-15, uhlmann2024acomparativeevaluation media 1840b690, uhlmann2024acomparativeevaluation pages 7-10)

**2. Müller, V.; Fasselt, J. M.; Kruse, T.; Klötzer, C.; Kleba-Ehrhardt, R.; Choma, T.; Biegler, M.; Rethmeier, M.** “Using Ultrasonic Atomization to Recycle Aluminium Bronze Chips for Additive Laser Directed Energy Deposition.” *IOP Conference Series: Materials Science and Engineering* **1296** (2023), 012036. **DOI:** 10.1088/1757-899X/1296/1/012036. **Process:** recycled aluminium-bronze chips → ultrasonic powder for laser DED. This is the closest named process predecessor, but its full paper was not obtainable in this search. Uhlmann *et al.* identify it as prior work; their 2024 measurements must **not** be relabelled as Müller’s 2023 yield, deposit or corrosion results. **Composition, powder yield/oxygen, deposited properties, test medium/duration, cost and emissions:** not independently verified here. **[CITE] [NOVELTY-RISK]** Chip-to-ultrasonic-powder-to-laser-DED is not itself a new concept; **[GAP]** verified corrosion and lot-to-lot qualification results are unavailable from the retrieved record. (uhlmann2024acomparativeevaluation pages 15-15, uhlmann2024acomparativeevaluation pages 13-15)

**3. Müller, V.; Marko, A.; Kruse, T.; Biegler, M.; Rethmeier, M.** “Analysis and Recycling of Bronze Grinding Waste to Produce Maritime Components Using Directed Energy Deposition.” In *LiM—Lasers in Manufacturing* (2021), Wissenschaftliche Gesellschaft Lasertechnik und Photonik, Hannover. **DOI:** none verified. **Process:** bronze grinding waste and laser DED for maritime components, as identified by Uhlmann *et al.*; the underlying proceedings were not retrieved. **Composition, deposition geometry, powder yield/oxygen, mechanical and corrosion test conditions/results, cost and CO₂:** not verifiable from the available citation. Do not infer a seawater-qualified propeller repair from the title. **[CITE] [NOVELTY-RISK] [GAP]** Relevant early maritime recycling precedent, not a quantitative benchmark on present evidence. The 2024 follow-up acknowledges EU Horizon 2020/MarTERA funding, grant **728053**. (uhlmann2024acomparativeevaluation pages 15-15, uhlmann2024acomparativeevaluation pages 13-15)

**4. Cabrioli, M.; Colmenero, M. S.; Gholamzadeh, S.; Vanazzi, M.; Amirabdollahian, S.; Perini, M.; Łacisz, W.; Kalicki, B.** “Upcycling of Copper Scrap into High-Quality Powder for Additive Manufacturing: Processing, Characterization, and Sustainability Assessment.” *Journal of Manufacturing and Materials Processing* **9** (2025), 320. **DOI:** 10.3390/jmmp9090320. **Process:** remove plastic/rubber from retired offshore electrical cable → ultrasonic atomization of recovered copper → **laser DED** demonstration and comparative life-cycle assessment. **Composition:** approximately **99.5 wt% Cu purity**, **not** a Cu–Ni or NAB repair alloy. The publisher-indexed abstract reports good powder flow, apparent/tapped density and particle-size distribution, successful laser deposition, and **more than 70% lower global-warming potential than the compared conventional mining route**. Critically, the full-text retrieval returned an unrelated report; consequently **exact powder-size distribution, flow, oxygen, size-fraction yield, kWh/kg, kg CO₂-eq/kg, LCA boundary/functional unit, deposit porosity and all cost figures cannot be checked here**. The >70% figure is an **abstract-level comparison, not a measured atomizer-energy saving**, and should not be transferred to alloyed powder or shipboard operation. **Corrosion medium/duration and electrochemical, selective-attack, hardness and tensile results:** not established by the accessible record. **[CITE] [NUMBERS—abstract only] [NOVELTY-RISK]** Establishes offshore-cable-copper upcycling with laser DED and an LCA claim; **[GAP]** does not establish alloyed marine-repair corrosion performance or point-of-need economics. (cabrioli2025upcyclingofcopper pages 9-12)

**5. Saai, A.; Hepo-oja, L.; Müller, V.; Puukko, P.; Klötzer-Freese, C.; Wagner, F.; Azrague, K.** “Comparative Life Cycle Assessments of Greenhouse Gas Emissions Associated with Directed Energy Deposition Repairing and Sand-Casting Replacement of a Ship Propeller.” *Progress in Additive Manufacturing* **10** (2025), 11781–11799. **DOI:** 10.1007/s40964-025-01316-w. **Processes:** **gas-atomized-powder laser DED** of propeller hub, **wire-arc DED** of blade, versus **sand-cast** replacement; **not** on-vessel atomization or proof that recycled scrap powder was deposited. **Alloy:** modeled NAB ranges Cu **79–83.2**, Al **8.5–9.5**, Ni **4–5**, Fe **3.5–4.5**, Mn **0.8–1.5 wt%**. In the industrial inventory, one hub repair consumed **30 kg powder** and deposited **23 kg**—approximately **23% overspray**—while one blade repair consumed **19.5 kg wire**. The LCA uses **85% atomization yield as an assumption for sensitivity analysis**, **not a measured yield of Müller’s or Uhlmann’s atomizer**. It adopts a literature value of **2,000 kWh per tonne of atomized copper/copper-alloy powder** (**2 kWh/kg**) rather than directly metering a local small-lot machine. Modeled **10% greater powder yield** reduced raw-powder GHG by **3%**; **10% less overspray** reduced raw-powder GHG by **13%** and whole laser-repair GHG by **7%**. Across its specified 20-year propeller scenario, cumulative DED-repair contributions were **no more than 62%** of replacement GHG. Supplying powder from Norway rather than China lowered modeled GHG for a German hub repair by **28%**, showing why electricity mix cannot be replaced with an unsupported ‘local is greener’ assertion. It is an LCA, not measured seawater corrosion or a cost comparison; the repair inventory also includes preprocessing/postprocessing, so its GHG ratio is not an atomizer-only saving. **[CITE] [NUMBERS] [NOVELTY-RISK]** Maritime DED repair and sustainability are prior art; **[GAP]** measured chip-to-powder inventory and corrosion-qualified recycled-alloy repair remain open. (saai2025comparativelifecycle pages 1-2, saai2025comparativelifecycle pages 6-8, saai2025comparativelifecycle pages 11-14, saai2025comparativelifecycle pages 8-9, saai2025comparativelifecycle media ed562b9a)

**6. Raute, J.; Beret, A.; Biegler, M.; Rethmeier, M.** “Life Cycle Assessment in Additive Manufacturing of Copper Alloys—Comparison between Laser and Electron Beam.” *Welding in the World* **68** (2024), 3169–3176. **DOI:** 10.1007/s40194-024-01856-9. **Processes:** **blown-powder laser DED versus wire-electron-beam DED** on laboratory cylinders—not powder-making, wire-laser DED, WAAM, or equivalent feedstock compositions. **Powder alloy:** Cu balance, Al **9.63**, Fe **1.25**, other elements <0.5 wt%; **wire alloy:** Cu balance, Al **9**, Ni **4.5**, Fe **3.5**, Mn **1.3 wt%**. Measured complete-machine process electricity, per gram *deposited*, was **11,046 kJ/g** for laser/powder versus **3,713 kJ/g** for electron-beam/wire; **2.24 g starting powder per gram deposited**, versus approximately **1 g wire/g deposited**. Their modeled laser/powder GWP was about **threefold** the electron-beam/wire value, **but powder atomization and wire drawing were explicitly excluded from the inventory**. These very large deposited-mass-normalized process-energy numbers must not be confused with Saai’s **2 kWh/kg powder-production assumption**. **Seawater conditions, density, hardness and corrosion:** not reported as comparative endpoints. **[CITE] [NUMBERS] [GAP]** Captures how low deposition capture and system overhead can defeat feedstock savings; not an apples-to-apples test of pre-alloyed NAB powder against NAB wire. (raute2024lifecycleassessment pages 2-4, raute2024lifecycleassessment pages 4-5, raute2024lifecycleassessment pages 5-7)

**7. Strieby, S. F.** *Operationalizing Metal Additive Manufacturing for Expeditionary Employment by the United States Marine Corps.* Naval Postgraduate School Acquisition Research Program sponsored report **NPS-LM-23-263**, **March 2023**; **DOI:** none identified. **Process:** USMC expeditionary **wire-arc DED plus CNC machining** and comparative logistics/cost-effectiveness modeling; **not** an ultrasonic-atomized powder study. The report describes a deployed hybrid wire-arc capability, in use since **2018**, and explains the appeal of solid wire over hazardous or contamination-sensitive powder. Its analysis **excludes feedstock costs**, uncertain material waste and several deployment/supply burdens; it does not establish a dollar-per-kg local-powder advantage. **Copper alloy composition, powder quality, seawater tests and shipboard atomizer output:** none reported. An at-sea printer or mobile wire-arc unit is **not evidence that ships recycle machining chips into AM powder**. **[NAVY] [CITE] [GAP]** Strong point-of-need *logistics rationale*, but not validation of shipboard scrap-to-powder or marine copper repair. (strieby2024operationalizingmetaladditive pages 1-9, strieby2024operationalizingmetaladditive pages 48-53, strieby2024operationalizingmetaladditive pages 99-103)

## Qualification and unanswered metrics

**Small lots change the unit of qualification from ‘one commercially established powder’ to a traceable chain of scrap source, decontamination, melt chemistry, atomization run, sieved fraction, powder delivery and deposited repair.** This is an engineering implication, **not a published numerical qualification-cost estimate**. Uhlmann documents why source abrasives, atomizer contact material, oxygen, size and flow cannot be assumed constant; its standards-based measurements use image-analysis sizing, **Carney** flow, apparent/tap density and oxygen assays. Saai’s yield and overspray sensitivities show why records must distinguish recovered feedstock mass, AM-size-fraction yield and deposition capture. None of these sources quantifies the cost per qualified small batch or proves transferable qualification from NAB to Cu–Ni. A separate certified-production **LPBF Ti-6Al-4V**, not copper DED, study illustrates the limitation of relying on powder alone: across **175 powder-reuse cycles**, powder oxygen rose **8.2% relative** and manufactured-part oxygen **25.1% relative**, despite properties remaining within that application’s specifications. It is an analogy for surveillance, not a naval-copper acceptance criterion. (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 13-15, saai2025comparativelifecycle pages 11-14, uhlmann2024acomparativeevaluation media 1840b690, gibbons2026alongitudinalstudy pages 1-2)

**No verified source here reports an ultrasonic powder atomizer operating aboard a US Navy vessel, recycling shipboard chips, or a shipyard-produced Cu–Ni/NAB powder lot qualified for naval service.** Nor do the verified recycling studies provide the requested as-deposited 3.5 wt% NaCl versus ASTM D1141/natural-seawater comparison, exposure duration or flow, corrosion-current density, *E*₍corr₎, impedance, selective-attack depth, or a head-to-head wrought **70–30 Cu–Ni/C71500** benchmark. Accordingly those fields are **not reported/not verified**, not zero; successful powder flow and deposition should never be represented as evidence of seawater resistance. Likewise, no substantiated per-kg local small-lot powder **price**, measured **rePOWDER kWh/kg**, or measured **kg CO₂-eq/kg alloy powder** was obtained. (uhlmann2024acomparativeevaluation pages 13-15, saai2025comparativelifecycle pages 11-14, strieby2024operationalizingmetaladditive pages 1-9)

## Top 5 things the PI should know

1. **Position novelty in composition-to-qualified-performance, not in atomizing scrap.** MarTERA already covers NAB chips, ultrasonic spherical powder and laser-DED intent; the unfilled claim is deliberately designed, single-feed Cu–Ni/NAB alloy deposits, including dissimilar repair interfaces, validated *as deposited* against wrought C71500 in defined seawater tests. (uhlmann2024acomparativeevaluation pages 15-15, uhlmann2024acomparativeevaluation pages 13-15, uhlmann2024acomparativeevaluation pages 7-10)
2. **Make contamination and lot identity first-class model inputs.** The measured NAB oxygen spread—**0.013 wt% atomized versus 0.119–0.190 wt% mechanically milled**—and ceramic/carbon contaminants show why scrap origin and atomization conditions may matter as much as nominal alloy chemistry. (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation media 1840b690, uhlmann2024acomparativeevaluation pages 7-10)
3. **Report three different yields, never one ambiguous ‘powder yield.’** Usable-size-fraction mass yield is missing for the key Uhlmann study; Saai’s **85%** is modeled atomization yield, while its **23%** is deposition overspray. Measure both plus starting-scrap-to-accepted-powder recovery by lot. (uhlmann2024acomparativeevaluation pages 6-7, saai2025comparativelifecycle pages 11-14, saai2025comparativelifecycle media ed562b9a)
4. **Keep the sustainability claim conditional and metered.** Cabrioli’s **>70%** mining-comparator GWP result concerns essentially pure recycled copper; Saai’s **2 kWh/kg** is assumed atomization energy; Raute excludes actual powder manufacture from its process LCA. A convincing naval comparison needs actual small-run electricity, inert gas, scrap pretreatment, reject fractions, overspray and logistics, with an explicit electricity mix and functional unit. (saai2025comparativelifecycle pages 11-14, saai2025comparativelifecycle pages 8-9, raute2024lifecycleassessment pages 4-5, raute2024lifecycleassessment pages 5-7)
5. **Do not claim the Navy has demonstrated shipboard copper-powder recycling.** Verified expeditionary precedent here is principally **wire-arc hybrid manufacturing**, while measured shipboard atomizer performance, batch qualification cost and seawater-qualified recycled-powder repairs remain unsubstantiated. Treat point-of-need powder-making as a proposed capability whose safety, logistics and acceptance evidence still must be generated. (strieby2024operationalizingmetaladditive pages 43-48, strieby2024operationalizingmetaladditive pages 1-9, strieby2024operationalizingmetaladditive pages 48-53, strieby2024operationalizingmetaladditive pages 99-103)

References

1. (uhlmann2024acomparativeevaluation pages 1-2): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

2. (uhlmann2024acomparativeevaluation pages 13-15): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

3. (saai2025comparativelifecycle pages 1-2): Afaf Saai, Lotta Hepo-oja, Vinzenz Müller, Pasi Puukko, Christian Klötzer-Freese, Florian Wagner, and Kamal Azrague. Comparative life cycle assessments of greenhouse gas emissions associated with directed energy deposition repairing and sand-casting replacement of a ship propeller. Progress in Additive Manufacturing, 10:11781-11799, Aug 2025. URL: https://doi.org/10.1007/s40964-025-01316-w, doi:10.1007/s40964-025-01316-w. This article has 6 citations and is from a peer-reviewed journal.

4. (strieby2024operationalizingmetaladditive pages 1-9): S Strieby. Operationalizing metal additive manufacturing for expeditionary employment by the united states marine corps. Unknown journal, 2024.

5. (uhlmann2024acomparativeevaluation pages 2-4): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

6. (uhlmann2024acomparativeevaluation pages 4-6): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

7. (uhlmann2024acomparativeevaluation pages 7-10): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

8. (uhlmann2024acomparativeevaluation pages 10-12): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

9. (uhlmann2024acomparativeevaluation pages 6-7): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

10. (uhlmann2024acomparativeevaluation media 1840b690): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

11. (uhlmann2024acomparativeevaluation pages 15-15): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

12. (cabrioli2025upcyclingofcopper pages 9-12): Mattia Cabrioli, María Silva Colmenero, Sepideh Gholamzadeh, Matteo Vanazzi, Sasan Amirabdollahian, Matteo Perini, Wojciech Łacisz, and Bartosz Kalicki. Upcycling of copper scrap into high-quality powder for additive manufacturing: processing, characterization, and sustainability assessment. Journal of Manufacturing and Materials Processing, 9:320, Sep 2025. URL: https://doi.org/10.3390/jmmp9090320, doi:10.3390/jmmp9090320. This article has 7 citations.

13. (saai2025comparativelifecycle pages 6-8): Afaf Saai, Lotta Hepo-oja, Vinzenz Müller, Pasi Puukko, Christian Klötzer-Freese, Florian Wagner, and Kamal Azrague. Comparative life cycle assessments of greenhouse gas emissions associated with directed energy deposition repairing and sand-casting replacement of a ship propeller. Progress in Additive Manufacturing, 10:11781-11799, Aug 2025. URL: https://doi.org/10.1007/s40964-025-01316-w, doi:10.1007/s40964-025-01316-w. This article has 6 citations and is from a peer-reviewed journal.

14. (saai2025comparativelifecycle pages 11-14): Afaf Saai, Lotta Hepo-oja, Vinzenz Müller, Pasi Puukko, Christian Klötzer-Freese, Florian Wagner, and Kamal Azrague. Comparative life cycle assessments of greenhouse gas emissions associated with directed energy deposition repairing and sand-casting replacement of a ship propeller. Progress in Additive Manufacturing, 10:11781-11799, Aug 2025. URL: https://doi.org/10.1007/s40964-025-01316-w, doi:10.1007/s40964-025-01316-w. This article has 6 citations and is from a peer-reviewed journal.

15. (saai2025comparativelifecycle pages 8-9): Afaf Saai, Lotta Hepo-oja, Vinzenz Müller, Pasi Puukko, Christian Klötzer-Freese, Florian Wagner, and Kamal Azrague. Comparative life cycle assessments of greenhouse gas emissions associated with directed energy deposition repairing and sand-casting replacement of a ship propeller. Progress in Additive Manufacturing, 10:11781-11799, Aug 2025. URL: https://doi.org/10.1007/s40964-025-01316-w, doi:10.1007/s40964-025-01316-w. This article has 6 citations and is from a peer-reviewed journal.

16. (saai2025comparativelifecycle media ed562b9a): Afaf Saai, Lotta Hepo-oja, Vinzenz Müller, Pasi Puukko, Christian Klötzer-Freese, Florian Wagner, and Kamal Azrague. Comparative life cycle assessments of greenhouse gas emissions associated with directed energy deposition repairing and sand-casting replacement of a ship propeller. Progress in Additive Manufacturing, 10:11781-11799, Aug 2025. URL: https://doi.org/10.1007/s40964-025-01316-w, doi:10.1007/s40964-025-01316-w. This article has 6 citations and is from a peer-reviewed journal.

17. (raute2024lifecycleassessment pages 2-4): Julius Raute, Alexander Beret, Max Biegler, and Michael Rethmeier. Life cycle assessment in additive manufacturing of copper alloys—comparison between laser and electron beam. Welding in the World, 68:3169-3176, Oct 2024. URL: https://doi.org/10.1007/s40194-024-01856-9, doi:10.1007/s40194-024-01856-9. This article has 9 citations and is from a domain leading peer-reviewed journal.

18. (raute2024lifecycleassessment pages 4-5): Julius Raute, Alexander Beret, Max Biegler, and Michael Rethmeier. Life cycle assessment in additive manufacturing of copper alloys—comparison between laser and electron beam. Welding in the World, 68:3169-3176, Oct 2024. URL: https://doi.org/10.1007/s40194-024-01856-9, doi:10.1007/s40194-024-01856-9. This article has 9 citations and is from a domain leading peer-reviewed journal.

19. (raute2024lifecycleassessment pages 5-7): Julius Raute, Alexander Beret, Max Biegler, and Michael Rethmeier. Life cycle assessment in additive manufacturing of copper alloys—comparison between laser and electron beam. Welding in the World, 68:3169-3176, Oct 2024. URL: https://doi.org/10.1007/s40194-024-01856-9, doi:10.1007/s40194-024-01856-9. This article has 9 citations and is from a domain leading peer-reviewed journal.

20. (strieby2024operationalizingmetaladditive pages 48-53): S Strieby. Operationalizing metal additive manufacturing for expeditionary employment by the united states marine corps. Unknown journal, 2024.

21. (strieby2024operationalizingmetaladditive pages 99-103): S Strieby. Operationalizing metal additive manufacturing for expeditionary employment by the united states marine corps. Unknown journal, 2024.

22. (gibbons2026alongitudinalstudy pages 1-2): Duncan W. Gibbons and Andre F. van der Merwe. A longitudinal study of ti-6al-4v eli powder reuse for laser powder bed fusion in a certified medical device manufacturing facility. The International Journal of Advanced Manufacturing Technology, Sep 2026. URL: https://doi.org/10.1007/s00170-026-19064-8, doi:10.1007/s00170-026-19064-8. This article has 0 citations.

23. (strieby2024operationalizingmetaladditive pages 43-48): S Strieby. Operationalizing metal additive manufacturing for expeditionary employment by the united states marine corps. Unknown journal, 2024.
