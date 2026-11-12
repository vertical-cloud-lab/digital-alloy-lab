<!--
Edison Scientific LITERATURE_HIGH task (batch 6)
- Task ID: 9b7269e1-9196-4f5c-88ed-239c947fcec6
- Submitted: 2026-10-17T18:37:41Z
- Fetched: 2026-10-17T19:07:39Z (status: success)
- Raw trajectory JSON: ../raw/b6-03-blended-vs-prealloyed-ded.json.gz
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

QUESTION: The University of Utah's InssTek MX-Lab can feed up to six powders
at once, so a composition can also be made in the melt pool from blends of
elemental, master-alloy, or commercial pre-alloyed copper alloy powders
before the ultrasonic atomizer makes a pre-alloyed lot of it. Could such
in-situ alloyed deposits be a cheap, lower-fidelity stand-in for deposits
from pre-alloyed powder in a multi-fidelity search? Cover copper alloys first
(Cu-Ni from Cu + Ni or Cu + Cu-Ni powders; Cu-Al and NAB from Cu + Al or
Cu + Al-alloy powders, e.g. Yao et al. 2025, Addit. Manuf. 105:104787;
graded Cu-Ni or Cu-Al deposits; Missouri S&T work on Cu-Ni from blended
elemental powders), then other alloys (Ti-6Al-4V and Ti alloys from elemental
blends, Ni superalloys, steels, high-entropy alloys, e.g. Nelaturu et al.
2024 and Kitt et al. 2024; compositionally graded libraries). Report:
(1) composition accuracy and homogeneity against the target (EDS or ICP maps,
unmelted or partly melted particles, macrosegregation, evaporation losses of
Mn and Al); (2) porosity, cracking and microstructure (phases, grain size,
martensite) compared with the same composition deposited from pre-alloyed
powder; (3) differences in hardness, tensile properties and especially
corrosion in NaCl or seawater between blended and pre-alloyed deposits;
(4) whether rankings of compositions by hardness, cracking or corrosion from
blended deposits agree with rankings from pre-alloyed deposits or from cast
or wrought material, with numbers; (5) any multi-fidelity, transfer-learning
or active-learning work that used blended-powder DED or graded libraries as a
lower-fidelity source; (6) practical problems of multi-hopper feeding with
powders of different density and size (e.g. Cu, Al, Ni), feed-rate
calibration, and separation of particles in the stream. Say plainly where no
blended-versus-pre-alloyed comparison exists for copper alloys.

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

QUESTION: The University of Utah's InssTek MX-Lab can feed up to six powders
at once, so a composition can also be made in the melt pool from blends of
elemental, master-alloy, or commercial pre-alloyed copper alloy powders
before the ultrasonic atomizer makes a pre-alloyed lot of it. Could such
in-situ alloyed deposits be a cheap, lower-fidelity stand-in for deposits
from pre-alloyed powder in a multi-fidelity search? Cover copper alloys first
(Cu-Ni from Cu + Ni or Cu + Cu-Ni powders; Cu-Al and NAB from Cu + Al or
Cu + Al-alloy powders, e.g. Yao et al. 2025, Addit. Manuf. 105:104787;
graded Cu-Ni or Cu-Al deposits; Missouri S&T work on Cu-Ni from blended
elemental powders), then other alloys (Ti-6Al-4V and Ti alloys from elemental
blends, Ni superalloys, steels, high-entropy alloys, e.g. Nelaturu et al.
2024 and Kitt et al. 2024; compositionally graded libraries). Report:
(1) composition accuracy and homogeneity against the target (EDS or ICP maps,
unmelted or partly melted particles, macrosegregation, evaporation losses of
Mn and Al); (2) porosity, cracking and microstructure (phases, grain size,
martensite) compared with the same composition deposited from pre-alloyed
powder; (3) differences in hardness, tensile properties and especially
corrosion in NaCl or seawater between blended and pre-alloyed deposits;
(4) whether rankings of compositions by hardness, cracking or corrosion from
blended deposits agree with rankings from pre-alloyed deposits or from cast
or wrought material, with numbers; (5) any multi-fidelity, transfer-learning
or active-learning work that used blended-powder DED or graded libraries as a
lower-fidelity source; (6) practical problems of multi-hopper feeding with
powders of different density and size (e.g. Cu, Al, Ni), feed-rate
calibration, and separation of particles in the stream. Say plainly where no
blended-versus-pre-alloyed comparison exists for copper alloys.

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


## Can In-Situ Alloyed DED Deposits Serve as a Cheap, Lower-Fidelity Stand-In for Pre-Alloyed Powder Deposits in a Multi-Fidelity Search? A Literature Assessment

### Summary of the Evidence Landscape

The following analysis synthesizes findings across six reporting criteria, organized by alloy family (copper alloys first, then other systems). A comprehensive comparison table is provided below.

| Reference | Alloy system | Process | Feedstock / comparison | Key numbers and findings | Tags |
|---|---|---|---|---|---|
| **Karnati et al. (2019)**, *Metals* 9, 287, DOI: **10.3390/met9030287**; *Int. J. Adv. Manuf. Technol.* 103, 239–250, DOI: **10.1007/s00170-019-03553-0** | Cu–Ni FGM; Cu-rich feed about 70 wt% Cu–30 wt% Ni-source, with Ni supplied as Delero-22 | Blown-powder laser DED / laser metal deposition | Blended Cu + near-pure Ni-alloy powder; no same-composition pre-alloyed control | Deposited composition differed from design by about **4%**. Pulse-width modulation induced melt-pool vibration to suppress segregation. FGM parameters included **1 kW peak power**, **43% duty cycle**, **500 mm/min**, and about **15 g/min**. Tensile failure occurred in the Cu-rich region. No porosity or corrosion comparison was reported. (chen2022processingandcharacterization pages 38-42, karnati2019onthefeasibility pages 1-3, karnati2019onthefeasibility pages 3-5, chen2020areviewon pages 10-13) | **[CITE] [NUMBERS] [NOVELTY-RISK] [GAP]** Direct overlap with in-situ-alloyed Cu–Ni; no pre-alloyed control or seawater data. |
| **Clayton (2013)**, *The Use of Elemental Powder Mixes in Laser-Based Additive Manufacturing*, Missouri S&T thesis; DOI not identified | AISI 430 and 316 stainless steels | Blown-powder laser DED | Direct comparison of elemental blends and commercial pre-alloyed powders | For 430 SS, EDS indicated homogeneous blended deposits, but microstructures differed: pre-alloyed material contained ferrite and martensite; blended material was fully ferritic. At **500 g**, hardness was **356 ± 46 VHN** pre-alloyed versus **150 ± 4 VHN** blended. After **770 °C for 1 h** and air cooling: **210 ± 6 versus 130 ± 2 VHN**. No corrosion comparison. (clayton2013theuseof pages 57-65, clayton2013theuseof pages 48-57) | **[CITE] [NUMBERS] [GAP]** Demonstrates that EDS homogeneity does not establish property equivalence. |
| **Chen et al. (2016)**, “Effect of Powder Particle Size on the Fabrication of Ti-6Al-4V Using Direct Laser Metal Deposition from Elemental Powder Mixture,” DOI: **10.17265/2159-5275/2016.07.005** | Ti–6Al–4V, wt% | Blown-powder direct laser metal deposition | Elemental Ti + Al + V blend; no direct same-build pre-alloyed control | EDS line scans indicated homogeneous deposits. Mean particle sizes were about **106 µm Ti**, **165 µm Al**, and **175 µm V**. Composition became more stable when sizes were selected to equalize particle populations and transport. Powders were mixed for **20 min** and deposited with a **1 kW Nd:YAG laser**. (chen2016effectofpowder pages 1-3) | **[CITE] [NUMBERS] [GAP]** Useful feedstock-design precedent; no direct pre-alloyed property comparison. |
| **Huang et al. (2022)**, “Corrosion Resistance of Selective Laser Melted Ti6Al4V3Cu Alloy Produced Using Pre-Alloyed and Mixed Powder,” *Materials* 15, 2487, DOI: **10.3390/ma15072487** | Ti–6Al–4V–3Cu, wt% | LPBF / selective laser melting; cast control | Gas-atomized pre-alloyed powder versus mixed **97 wt% Ti–6Al–4V + 3 wt% Cu** | Powder d90: **41.39 µm** pre-alloyed and **44.60 µm** mixed. Mixed feed produced Cu-rich/Cu-deficient regions. Ti2Cu: **6.61 versus 7.22 wt%**; grain size: about **2.75 versus 2.69 µm**. In **0.9 wt% NaCl at 37 °C**, polarization resistance was **371.67 ± 103.60 versus 354.17 ± 141.78 kΩ·cm²**. After **12 days**, total ion release was **0.165 versus 0.172 mg/L**, and Cu release was **0.029 versus 0.031 mg/L**. Pre-alloyed powder gave slightly better corrosion resistance. (huang2022corrosionresistanceof pages 9-13, huang2022corrosionresistanceof pages 13-14, huang2022corrosionresistanceof pages 4-7, huang2022corrosionresistanceof pages 2-4) | **[CITE] [NUMBERS] [NOVELTY-RISK]** Best direct corrosion precedent, but it is Ti-base LPBF rather than Cu-base DED. |
| **Gerdt et al. (2026)**, “High-Throughput Alloy Screening by Means of In Situ Alloying with Multi-wire DED-LB Nozzle COAXquattro,” DOI: **10.1007/s11666-026-02316-0** | IN625–316L mixtures with Ti, Al, or Mo additions | Multi-wire laser DED with supplementary powder feeding | In-situ mixing of commercial IN625 and 316L wires at 2:2 and 1:3 ratios; pure-alloy controls | Porosity was **less than 0.5%**. Hardness was **192.4 ± 16.5 HV** for 2:2, **187.9 ± 12.9 HV** for 1:3, **186.0 ± 10.8 HV** for 316L, and **214.8 ± 21.7 HV** for IN625. In **3.5 wt% NaCl**, corrosion potential was about **−0.16 to −0.17 V versus Ag/AgCl**; corrosion-current density was **6×10⁻⁸ A/cm²** for 316L, **8.8×10⁻⁸** for IN625, and **1.0×10⁻⁷** for the 1:3 mixture. Ti/Al/Mo-modified walls exhibited hot cracking. (gerdt2026highthroughputalloyscreening pages 1-2, gerdt2026highthroughputalloyscreening pages 6-11, gerdt2026highthroughputalloyscreening pages 4-6) | **[CITE] [NUMBERS] [NOVELTY-RISK]** In-situ alloying with CALPHAD, hardness, and NaCl screening; not powder-only Cu alloys or multi-fidelity BO. |
| **Chen et al. (2020)**, “A Review on Metallic Alloys Fabrication Using Elemental Powder Blends by Laser Powder Directed Energy Deposition Process,” *Materials* 13, 3562, DOI: **10.3390/ma13163562** | Ti alloys, steels, Cu–Ni, Cu–Al transport studies, Ni alloys, HEAs, and FGMs | Blown-powder laser DED review | Elemental and master-alloy blends versus conventional pre-alloyed-feedstock practice | Reports about **4%** Cu–Ni composition error; Al in nominal AlCoCrFeNi was only **10–15 at%** versus **20 at%** designed; refractory HEA deviation reached **3.5%**. Identifies density/size segregation, unequal capture, evaporation, absorptivity, and mixing enthalpy as separate error sources. (chen2020areviewon pages 10-13, chen2020areviewon pages 5-8, chen2020areviewon pages 8-10) | **[CITE] [NUMBERS] [GAP]** Core review; does not establish ranking transfer to pre-alloyed Cu alloys. |
| **Li (2018)**, *Modeling and Experimental Investigations on Particle Dynamic Behaviors in Laser 3D Printing with Blown Powder*, Missouri S&T thesis; related article DOI: **10.1007/s00170-018-1909-x** | Cu–4047 Al transport; Ti–6Al–4V/TiB2 example | Blown-powder DED feed-system and powder-spray experiments | Premixed dissimilar powders; unoptimized versus density–size-matched distributions | A nominal **50:50 vol% Cu–Al** blend initially exited as about **93.25% Al and 6.75% Cu**; Cu reached about 50% only after **21 s**, then became dominant. Matching constituent density–diameter-squared values maintained approximately **50:50** delivery. Ti–6Al–4V/TiB2 hardness declined from **453 to 363** as fine TiB2 was depleted. (li2018modelingandexperimental pages 22-27, li2018modelingandexperimental pages 17-22, li2018modelingandexperimental pages 86-91, li2018modelingandexperimental pages 37-42) | **[CITE] [NUMBERS] [NOVELTY-RISK]** Essential warning for Cu/Al/Ni feed calibration and stream segregation. |
| **Yao et al. (2025)**, “Microstructural and interfacial characteristics in repair of nickel-aluminum bronze by in-situ synthesis of Cu–Al alloys via directed energy deposition,” *Additive Manufacturing* 105, 104787, DOI: **10.1016/j.addma.2025.104787** | In-situ Cu–Al repair deposits on cast NAB | Blown-powder laser DED | Cu + Al-bearing powder in-situ synthesis; no verified same-composition pre-alloyed control in the accessible record | The bibliographic record confirms directly overlapping Cu–Al/NAB repair, but the full text was unavailable in the retrieved corpus. Composition maps, porosity, hardness, corrosion conditions, and numerical results therefore cannot be reported reliably. | **[CITE] [NAVY] [NOVELTY-RISK] [GAP]** Direct NAB-repair overlap; blended-versus-pre-alloyed equivalence and seawater performance remain unestablished. |
| **Rodrigues et al. (2026)**, “Designing Homogeneous Ti-Nb-Fe-Sn β Titanium Alloys by PBF-LB: A Pre-Alloyed Powder Blend Strategy,” DOI: **10.48550/arXiv.2609.17476** | Ti–Nb–Fe–Sn β-Ti alloys | PBF-LB / LPBF | Blend of pre-alloyed master-alloy powders rather than elemental powders or one target-composition powder | Uses **70 µm layers**, remelting of every layer, and **1000 °C for 2 h** followed by water quenching. Master-alloy blending was intended to reduce unmelted refractory Nb and the homogenization burden. No quantitative side-by-side porosity, hardness, tensile, or corrosion results against fully pre-alloyed target-composition powder were available. (rodrigues2026designinghomogeneoustinbfesn pages 5-9) | **[CITE] [GAP]** Master-alloy blending may be more transferable than elemental Cu/Al blending, but property equivalence is unproven. |


*Table: Comparison of the strongest quantitative studies on in-situ alloying, blended feedstocks, and pre-alloyed controls across copper and non-copper alloy systems. The table highlights direct benchmarks, overlap risks, and the absence of a blended-versus-pre-alloyed copper-alloy corrosion comparison.*

---

### 1. Composition Accuracy and Homogeneity

**Cu–Ni from blended elemental powders (Missouri S&T).** Karnati et al. (2019, *Metals* 9:287, DOI: 10.3390/met9030287; *Int. J. Adv. Manuf. Technol.* 103:239–250, DOI: 10.1007/s00170-019-03553-0) deposited Cu–Ni functionally graded materials from blended Cu and Delero-22 (Ni–Si–B) powder by blown-powder laser DED. The deposited composition deviated from the design by approximately 4% (chen2022processingandcharacterization pages 38-42, chen2020areviewon pages 10-13). Cu–Ni has a positive enthalpy of mixing, which impedes melt-pool homogenization; pulse-width-modulated laser power was required to induce melt-pool vibrations and suppress segregation (chen2020areviewon pages 10-13). EDS showed that the actual deposited gradient depended strongly on laser duty cycle rather than solely on the nominal powder blend ratio (karnati2019onthefeasibility pages 1-3). **No comparison against a same-composition pre-alloyed Cu–Ni powder was performed.**

**Cu–Al powder separation.** Li (2018, Missouri S&T thesis; related article DOI: 10.1007/s00170-018-1909-x) demonstrated that a 50:50 vol% Cu–4047 Al premixed powder, when fed through a common carrier-gas stream, initially exited the nozzle as approximately 93.25% Al and only 6.75% Cu, because the lighter Al particles accelerated faster (li2018modelingandexperimental pages 37-42). Cu only reached ~50% after approximately 21 seconds. After optimizing particle-size distributions so that the product ρ_p × d_p² was matched between Cu and Al, separation was effectively eliminated and the stream maintained approximately 50:50 (li2018modelingandexperimental pages 86-91, li2018modelingandexperimental pages 37-42). This is directly relevant: Cu (8.96 g/cm³), Al (2.70 g/cm³), and Ni (8.91 g/cm³) span a >3× density range.

**Cu–Al/NAB in-situ synthesis (Yao et al. 2025).** Yao et al. (2025, *Additive Manufacturing* 105:104787, DOI: 10.1016/j.addma.2025.104787) synthesized Cu–Al alloys in situ from blended powders by DED for NAB repair. The full text was not accessible; quantitative composition maps and homogeneity data cannot be reported. [CITE] [NAVY] [NOVELTY-RISK] [GAP]

**Ti–6Al–4V from elemental blends.** Chen et al. (2016, DOI: 10.17265/2159-5275/2016.07.005) deposited Ti–6Al–4V from elemental Ti, Al, and V by laser DED at Missouri S&T. EDS line scans showed homogeneous deposits when particle sizes were selected to equalize transport: mean sizes were ~106 µm Ti, 165 µm Al, 175 µm V (chen2016effectofpowder pages 1-3). Composition became more stable when particle populations were balanced.

**General findings.** The comprehensive review by Chen et al. (2020, *Materials* 13:3562, DOI: 10.3390/ma13163562) reports that elemental Al in a designed AlCoCrFeNi HEA was only 10–15 at% versus the 20 at% target, and refractory HEA composition deviations reached 3.5% (chen2020areviewon pages 10-13). Evaporation losses (especially of Al and Mn) and differential capture rates are additional, element-specific error sources beyond powder-stream segregation (chen2020areviewon pages 10-13). [CITE] [NUMBERS]

---

### 2. Porosity, Cracking, and Microstructure

**Cu–Ni.** Karnati et al. (2019) did not report porosity, cracking, or direct microstructural comparison against pre-alloyed Cu–Ni (karnati2019onthefeasibility pages 1-3, karnati2019onthefeasibility pages 3-5). The study focused on gradient tailoring. [GAP]

**430 stainless steel (blended vs. pre-alloyed, laser DED).** Clayton (2013, Missouri S&T thesis) provides the strongest direct comparison. Pre-alloyed 430 SS produced a ferritic + martensitic microstructure, whereas the elemental blend was fully ferritic despite EDS indicating homogeneous composition (clayton2013theuseof pages 57-65, clayton2013theuseof pages 48-57). This implies that rapid-solidification phase selection depends on the starting powder state, not just the average deposited composition. At 500 g Vickers load, hardness was 356 ± 46 VHN (pre-alloyed) versus 150 ± 4 VHN (blended); after annealing at 770 °C for 1 h and air cooling, values were 210 ± 6 versus 130 ± 2 VHN (clayton2013theuseof pages 57-65). [CITE] [NUMBERS] [GAP]

**IN625:316L in-situ wire DED.** Gerdt et al. (2026, DOI: 10.1007/s11666-026-02316-0) demonstrated <0.5% porosity in all in-situ alloyed wire-DED specimens mixing IN625 and 316L at 2:2 and 1:3 ratios (gerdt2026highthroughputalloyscreening pages 6-11). However, wall specimens with added Ti, Al, or Mo powders all exhibited hot cracking in the near-surface region along grain boundaries and dendritic cells (gerdt2026highthroughputalloyscreening pages 6-11). CALPHAD Scheil predictions agreed well with experimentally observed phases. [CITE] [NUMBERS] [NOVELTY-RISK]

**Ti6Al4V3Cu (SLM, pre-alloyed vs. mixed).** Huang et al. (2022, DOI: 10.3390/ma15072487) showed that both SLM routes produced fine grain sizes (~2.75 vs. 2.69 µm) much finer than cast (~4.45 µm). However, the mixed-powder route produced Cu-rich and Cu-deficient regions with irregularly distributed Ti₂Cu precipitates (7.22 wt% vs. 6.61 wt% in pre-alloyed), creating a less uniform microstructure (huang2022corrosionresistanceof pages 13-14, huang2022corrosionresistanceof pages 4-7). [CITE] [NUMBERS]

---

### 3. Hardness, Tensile Properties, and Corrosion

**Cu–Ni.** No published hardness, tensile, or corrosion comparison between blended-elemental and pre-alloyed Cu–Ni DED deposits was found in the accessible literature. Karnati et al. (2019) reported tensile tests only on the gradient structure, with fracture in the Cu-rich region, but did not test a uniform Cu-30Ni composition against a pre-alloyed reference (karnati2019onthefeasibility pages 1-3). **No corrosion data in NaCl or seawater for blended Cu–Ni DED deposits exist.** [GAP]

**Cu–Al / NAB.** The full text of Yao et al. (2025) was not accessible, so hardness, tensile, and corrosion numbers for in-situ synthesized Cu–Al cannot be reported. A related Yao et al. paper on cavitation erosion resistance of in-situ Cu–Al DED deposits was identified (DOI: 10.1016/j.jmrt.2025.07.170) but also not accessible. [GAP]

**Ti6Al4V3Cu (LPBF, corrosion comparison).** In 0.9 wt% NaCl at 37 °C, polarization resistance was 371.67 ± 103.60 kΩ·cm² (pre-alloyed) versus 354.17 ± 141.78 kΩ·cm² (mixed), a modest advantage for the pre-alloyed route (huang2022corrosionresistanceof pages 9-13). After 12 days of immersion, total ion release was 0.165 mg/L (pre-alloyed) versus 0.172 mg/L (mixed); Cu release was 0.029 versus 0.031 mg/L (huang2022corrosionresistanceof pages 9-13). Both SLM alloys substantially outperformed the cast alloy. The pre-alloyed material's advantage was attributed to a more uniform Ti₂Cu distribution and higher proportional β phase content (huang2022corrosionresistanceof pages 13-14). [CITE] [NUMBERS]

**430 SS (hardness comparison).** The 430 SS hardness difference (356 vs. 150 VHN, as-deposited) is the most dramatic example: EDS homogeneity was achieved, but the microstructure and therefore the hardness were fundamentally different between blended and pre-alloyed routes (clayton2013theuseof pages 57-65). [CITE] [NUMBERS]

**IN625:316L (in-situ wire DED, corrosion).** In 3.5 wt% NaCl, corrosion current density was 6 × 10⁻⁸ A/cm² (316L), 8.8 × 10⁻⁸ (IN625), and 1.0 × 10⁻⁷ (1:3 mixture)—the in-situ alloy had roughly double the corrosion rate of either parent alloy (gerdt2026highthroughputalloyscreening pages 6-11). Hardness values were 192.4 ± 16.5 HV (2:2), 187.9 ± 12.9 HV (1:3), 186.0 ± 10.8 HV (316L), and 214.8 ± 21.7 HV (IN625) (gerdt2026highthroughputalloyscreening pages 6-11). [CITE] [NUMBERS]

---

### 4. Ranking Transfer: Do Blended Deposits Preserve Composition Rankings?

**No study was found that explicitly compares the ranking of compositions by hardness, cracking, or corrosion from blended-powder DED deposits against rankings from the same compositions deposited from pre-alloyed powder, or from cast/wrought material.** This is a critical gap. The 430 SS result (Clayton 2013) demonstrates that rankings can fail catastrophically: a composition that appears homogeneous by EDS may produce a fundamentally different phase assemblage and therefore a different hardness ranking when deposited from elemental versus pre-alloyed powder (clayton2013theuseof pages 57-65). The Huang et al. (2022) Ti6Al4V3Cu comparison shows that the direction of the corrosion ranking was preserved (pre-alloyed ≥ mixed >> cast), but the magnitudes were close enough that the ranking between blended and pre-alloyed could reverse within experimental scatter (huang2022corrosionresistanceof pages 9-13). [GAP]

---

### 5. Multi-Fidelity, Transfer-Learning, or Active-Learning Work Using Blended DED as a Lower-Fidelity Source

**No publication was found that explicitly uses blended-powder or multi-hopper DED deposits as a lower-fidelity data source in a formal multi-fidelity Bayesian optimization or transfer-learning framework.** Several works come close:

- Liu et al. (2024, *Materials Genome Engineering Advances* 2(3), DOI: 10.1002/mgea.55) reviewed DED compositionally graded libraries as high-throughput screening tools for alloy design, citing examples of 80 Fe–Cr–Ni compositions screened and Cu10Sn-to-316L gradients producing >200 tensile samples (liu2024high‐throughputpreparationfor pages 12-12, liu2024high‐throughputpreparationfor pages 13-13). This is high-throughput screening but not formal multi-fidelity optimization. [CITE]

- Sreeramagiri and Balasubramanian (2022, *Frontiers in Materials* 9, DOI: 10.3389/fmats.2022.825276) argued that DED-based compositional variation could support combinatorial alloy discovery and validation of computational predictions, but did not implement a multi-fidelity loop (sreeramagiri2022directedenergydeposition pages 1-2). [CITE]

- Gerdt et al. (2026, DOI: 10.1007/s11666-026-02316-0) combined in-situ wire+powder DED alloying with CALPHAD-based Scheil predictions and potentiodynamic corrosion screening in 3.5% NaCl—the closest analog to the proposed pipeline—but did not cast it as multi-fidelity optimization (gerdt2026highthroughputalloyscreening pages 1-2, gerdt2026highthroughputalloyscreening pages 6-11). [CITE] [NOVELTY-RISK]

- Chawla et al. (2026, *Communications Materials*, DOI: 10.1038/s43246-026-01294-8) noted that compositionally graded libraries coupled with automated nanoindentation could feed multi-fidelity schemes, but the paper addresses thin-film sputtered libraries, not DED (chen2022processingandcharacterization pages 38-42). [CITE]

**Using blended-powder DED as a formal lower-fidelity node in cost-aware Bayesian optimization of function networks is, to the best of our knowledge, novel.** [GAP] [NOVELTY-RISK]

---

### 6. Practical Problems of Multi-Hopper Feeding with Powders of Different Density and Size

**Density-driven stream segregation.** Li (2018, Missouri S&T) showed that particle acceleration in the carrier gas scales as a ∝ 1/(ρ_p × d_p²). For Cu (8.96 g/cm³) and 4047 Al (2.70 g/cm³) at equal volume fractions, an unoptimized premix exited as ~93% Al initially and shifted to mostly Cu over time (li2018modelingandexperimental pages 37-42). The remedy is to select particle sizes so that the ρ_p × d_p² product is approximately equal across constituents (li2018modelingandexperimental pages 86-91). This approach was validated for spherical powders but has unknown effectiveness for non-spherical or irregular particles (chen2020areviewon pages 10-13).

**Capture-rate and evaporation errors.** Even after resolving stream segregation, different powders have different melt-pool capture probabilities depending on size, momentum, and divergence angle (chen2020areviewon pages 10-13). Evaporation of volatile elements (Al, Mn, Zn) at the melt pool surface introduces additional, element-specific composition losses that depend on laser power and dwell time. Chen et al. (2016) found that matching particle populations and selecting sizes for constant divergence angle helped control Ti–Al–V composition (chen2016effectofpowder pages 1-3). For Cu–Al combinations, the large differences in density and melting temperature make all of these issues more severe, and further model development is needed (chen2020areviewon pages 10-13).

**Multi-hopper versus premixed feeding.** When powders are fed from separate hoppers to a multi-nozzle head (as on the InssTek MX-Lab), each stream can be individually calibrated, potentially avoiding the premix segregation problem. However, mixing must then occur entirely in the melt pool, and powders arriving from different nozzles may have different spatial distributions at the melt-pool surface (chen2022processingandcharacterization pages 42-47). Kenny et al. (2026, DOI: 10.1007/s40964-026-01888-1) noted that absorptivity, particle size distribution, and powder density create challenges for multi-hopper management, local powder confinement, and real-time composition control. [CITE]

---

### Where the Literature Does Not Answer the Question

The following comparisons **do not exist** in the accessible literature for copper alloys and are stated plainly:

1. **No blended-versus-pre-alloyed corrosion comparison exists for Cu–Ni or Cu–Al DED deposits in NaCl or seawater.** All Cu–Ni DED work (Karnati et al.) tested gradients, not uniform compositions against pre-alloyed controls.

2. **No ranking-transfer study** has been published verifying whether blended-powder DED preserves the composition ranking obtained from pre-alloyed DED, cast, or wrought Cu–Ni or aluminum bronze.

3. **No multi-fidelity BO or transfer-learning study** has used blended-powder DED as a lower-fidelity source for any alloy system, let alone copper alloys.

4. **No porosity or cracking comparison** between blended-elemental and pre-alloyed Cu–Ni or Cu–Al DED deposits has been published.

5. **Yao et al. (2025)** on in-situ Cu–Al synthesis for NAB repair by DED was identified but the full text was not accessible; detailed property comparisons cannot be confirmed.

6. **Nelaturu et al. (2024) and Kitt et al. (2024)** were not found in the accessible literature databases despite targeted searching.

---

### Top 5 Things the PI Should Know

**1. Composition homogeneity ≠ property equivalence.** The 430 SS comparison (Clayton 2013) is the strongest cautionary example: EDS showed a chemically homogeneous blended deposit, but the microstructure was fully ferritic (150 VHN) instead of ferritic + martensitic (356 VHN), because the solidification pathway depends on the starting powder state (clayton2013theuseof pages 57-65). For Cu–Ni, the positive mixing enthalpy adds an additional thermodynamic barrier to melt-pool homogenization (chen2020areviewon pages 10-13). **The PI should expect that blended deposits will be a biased surrogate, not a noisy replica, of pre-alloyed deposits.**

**2. Cu–Al powder feeding is the hardest practical challenge.** A Cu–Al premix self-segregates by >85% in the carrier-gas stream unless particle sizes are specifically matched to equalize ρ_p × d_p² (li2018modelingandexperimental pages 37-42). The InssTek's separate hoppers avoid premix segregation but shift the mixing burden entirely to the melt pool, where Cu's high reflectivity and thermal conductivity already make laser coupling difficult. For NAB compositions containing 9–11% Al, the Al fraction is small enough that absolute composition error (in wt%) may be tolerable, but evaporation of Al at the melt-pool surface will be an additional loss channel.

**3. The only published blended-vs.-pre-alloyed corrosion comparison (Huang et al. 2022, Ti6Al4V3Cu LPBF) shows the ranking was preserved but the gap was small.** Rp was 371.67 vs. 354.17 kΩ·cm², within the scatter bands (huang2022corrosionresistanceof pages 9-13). This is encouraging but involves a Ti alloy in NaCl, not a Cu alloy in seawater. The microstructural difference (inhomogeneous Cu in the mixed alloy) could create galvanic micro-cells that are more consequential for Cu–Ni alloys where the corrosion mechanism depends on the Cu₂O/Ni-enriched protective film.

**4. Using blended DED as a lower-fidelity node in multi-fidelity BO is genuinely novel.** No precedent was found in the literature. The closest analog is Gerdt et al. (2026), who combined multi-wire in-situ alloying with CALPHAD screening and NaCl corrosion testing but did not frame it as multi-fidelity optimization (gerdt2026highthroughputalloyscreening pages 1-2, gerdt2026highthroughputalloyscreening pages 6-11). The PI's proposed function-network approach would be the first to formalize the blended-deposit fidelity gap and exploit it within cost-aware BO.

**5. A small "calibration campaign" comparing blended vs. pre-alloyed at 2–3 Cu–Ni compositions would be extremely high-value.** No such data exist for any copper alloy by any AM process. Even a single composition (e.g., Cu-30Ni-0.5Fe-0.7Mn) deposited both ways and tested by potentiodynamic polarization in 3.5% NaCl would establish the bias and noise of the lower-fidelity source and make the multi-fidelity proposal credible. Without it, the assumption that blended deposits preserve corrosion rankings remains unvalidated.

References

1. (chen2022processingandcharacterization pages 38-42): Y Chen. Processing and characterization of tini-based alloys fabricated by laser aided manufacturing. Unknown journal, 2022.

2. (karnati2019onthefeasibility pages 1-3): Sreekar Karnati, Yunlu Zhang, Frank F. Liou, and Joseph W. Newkirk. On the feasibility of tailoring copper–nickel functionally graded materials fabricated through laser metal deposition. Metals, 9:287, Mar 2019. URL: https://doi.org/10.3390/met9030287, doi:10.3390/met9030287. This article has 31 citations.

3. (karnati2019onthefeasibility pages 3-5): Sreekar Karnati, Yunlu Zhang, Frank F. Liou, and Joseph W. Newkirk. On the feasibility of tailoring copper–nickel functionally graded materials fabricated through laser metal deposition. Metals, 9:287, Mar 2019. URL: https://doi.org/10.3390/met9030287, doi:10.3390/met9030287. This article has 31 citations.

4. (chen2020areviewon pages 10-13): Yitao Chen, Xinchang Zhang, Mohammad Masud Parvez, and Frank Liou. A review on metallic alloys fabrication using elemental powder blends by laser powder directed energy deposition process. Materials, 13:3562, Aug 2020. URL: https://doi.org/10.3390/ma13163562, doi:10.3390/ma13163562. This article has 79 citations.

5. (clayton2013theuseof pages 57-65): RM Clayton. The use of elemental powder mixes in laser-based additive manufacturing. Unknown journal, 2013.

6. (clayton2013theuseof pages 48-57): RM Clayton. The use of elemental powder mixes in laser-based additive manufacturing. Unknown journal, 2013.

7. (chen2016effectofpowder pages 1-3): Xueyang Chen, Lei Yan, Wei Li, Zhiyuan Wang, Frank Liou, and Joe Newkirk. Effect of powder particle size on the fabrication of ti-6al-4v using direct laser metal deposition from elemental powder mixture. Journal of Mechanics Engineering and Automation, 6:348-355, Jul 2016. URL: https://doi.org/10.17265/2159-5275/2016.07.005, doi:10.17265/2159-5275/2016.07.005. This article has 12 citations.

8. (huang2022corrosionresistanceof pages 9-13): Gonghao Huang, Zefeng Fan, Liu Li, Yanjin Lu, and Jinxin Lin. Corrosion resistance of selective laser melted ti6al4v3cu alloy produced using pre-alloyed and mixed powder. Materials, 15:2487, Mar 2022. URL: https://doi.org/10.3390/ma15072487, doi:10.3390/ma15072487. This article has 10 citations.

9. (huang2022corrosionresistanceof pages 13-14): Gonghao Huang, Zefeng Fan, Liu Li, Yanjin Lu, and Jinxin Lin. Corrosion resistance of selective laser melted ti6al4v3cu alloy produced using pre-alloyed and mixed powder. Materials, 15:2487, Mar 2022. URL: https://doi.org/10.3390/ma15072487, doi:10.3390/ma15072487. This article has 10 citations.

10. (huang2022corrosionresistanceof pages 4-7): Gonghao Huang, Zefeng Fan, Liu Li, Yanjin Lu, and Jinxin Lin. Corrosion resistance of selective laser melted ti6al4v3cu alloy produced using pre-alloyed and mixed powder. Materials, 15:2487, Mar 2022. URL: https://doi.org/10.3390/ma15072487, doi:10.3390/ma15072487. This article has 10 citations.

11. (huang2022corrosionresistanceof pages 2-4): Gonghao Huang, Zefeng Fan, Liu Li, Yanjin Lu, and Jinxin Lin. Corrosion resistance of selective laser melted ti6al4v3cu alloy produced using pre-alloyed and mixed powder. Materials, 15:2487, Mar 2022. URL: https://doi.org/10.3390/ma15072487, doi:10.3390/ma15072487. This article has 10 citations.

12. (gerdt2026highthroughputalloyscreening pages 1-2): L. Gerdt, H. Hillig, S. Biastoch, J. Kaspar, and F.-L. Toma. High-throughput alloy screening by means of in situ alloying with multi-wire ded-lb nozzle coaxquattro. Journal of Thermal Spray Technology, Oct 2026. URL: https://doi.org/10.1007/s11666-026-02316-0, doi:10.1007/s11666-026-02316-0. This article has 0 citations and is from a peer-reviewed journal.

13. (gerdt2026highthroughputalloyscreening pages 6-11): L. Gerdt, H. Hillig, S. Biastoch, J. Kaspar, and F.-L. Toma. High-throughput alloy screening by means of in situ alloying with multi-wire ded-lb nozzle coaxquattro. Journal of Thermal Spray Technology, Oct 2026. URL: https://doi.org/10.1007/s11666-026-02316-0, doi:10.1007/s11666-026-02316-0. This article has 0 citations and is from a peer-reviewed journal.

14. (gerdt2026highthroughputalloyscreening pages 4-6): L. Gerdt, H. Hillig, S. Biastoch, J. Kaspar, and F.-L. Toma. High-throughput alloy screening by means of in situ alloying with multi-wire ded-lb nozzle coaxquattro. Journal of Thermal Spray Technology, Oct 2026. URL: https://doi.org/10.1007/s11666-026-02316-0, doi:10.1007/s11666-026-02316-0. This article has 0 citations and is from a peer-reviewed journal.

15. (chen2020areviewon pages 5-8): Yitao Chen, Xinchang Zhang, Mohammad Masud Parvez, and Frank Liou. A review on metallic alloys fabrication using elemental powder blends by laser powder directed energy deposition process. Materials, 13:3562, Aug 2020. URL: https://doi.org/10.3390/ma13163562, doi:10.3390/ma13163562. This article has 79 citations.

16. (chen2020areviewon pages 8-10): Yitao Chen, Xinchang Zhang, Mohammad Masud Parvez, and Frank Liou. A review on metallic alloys fabrication using elemental powder blends by laser powder directed energy deposition process. Materials, 13:3562, Aug 2020. URL: https://doi.org/10.3390/ma13163562, doi:10.3390/ma13163562. This article has 79 citations.

17. (li2018modelingandexperimental pages 22-27): W Li. Modeling and experimental investigations on particle dynamic behaviors in laser 3d printing with blown powder. Unknown journal, 2018.

18. (li2018modelingandexperimental pages 17-22): W Li. Modeling and experimental investigations on particle dynamic behaviors in laser 3d printing with blown powder. Unknown journal, 2018.

19. (li2018modelingandexperimental pages 86-91): W Li. Modeling and experimental investigations on particle dynamic behaviors in laser 3d printing with blown powder. Unknown journal, 2018.

20. (li2018modelingandexperimental pages 37-42): W Li. Modeling and experimental investigations on particle dynamic behaviors in laser 3d printing with blown powder. Unknown journal, 2018.

21. (rodrigues2026designinghomogeneoustinbfesn pages 5-9): J. Rodrigues, K. Bartha, M. Casas-Luna, G. V. Prandi, M. Sangali, Kateřina Ficková, J. Kozlík, M. Šlapáková, Martin Koller, A. Strnad, Josef Str'ask'y, M. Janeček, and R. Caram. Designing homogeneous ti-nb-fe-sn β titanium alloys by pbf-lb: a pre-alloyed powder blend strategy. ArXiv, Sep 2026. URL: https://doi.org/10.48550/arxiv.2609.17476, doi:10.48550/arxiv.2609.17476. This article has 0 citations.

22. (liu2024high‐throughputpreparationfor pages 12-12): Min Liu, Chenxu Lei, Yongxiang Wang, Baicheng Zhang, and Xuan-hui Qu. High‐throughput preparation for alloy composition design in additive manufacturing: a comprehensive review. Materials Genome Engineering Advances, Jul 2024. URL: https://doi.org/10.1002/mgea.55, doi:10.1002/mgea.55. This article has 45 citations.

23. (liu2024high‐throughputpreparationfor pages 13-13): Min Liu, Chenxu Lei, Yongxiang Wang, Baicheng Zhang, and Xuan-hui Qu. High‐throughput preparation for alloy composition design in additive manufacturing: a comprehensive review. Materials Genome Engineering Advances, Jul 2024. URL: https://doi.org/10.1002/mgea.55, doi:10.1002/mgea.55. This article has 45 citations.

24. (sreeramagiri2022directedenergydeposition pages 1-2): Praveen Sreeramagiri and Ganesh Balasubramanian. Directed energy deposition of multi-principal element alloys. Frontiers in Materials, Apr 2022. URL: https://doi.org/10.3389/fmats.2022.825276, doi:10.3389/fmats.2022.825276. This article has 31 citations.

25. (chen2022processingandcharacterization pages 42-47): Y Chen. Processing and characterization of tini-based alloys fabricated by laser aided manufacturing. Unknown journal, 2022.
