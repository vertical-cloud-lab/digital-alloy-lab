<!--
Edison Scientific LITERATURE task (batch 3)
- Task ID: b93c9cc9-31ad-44d3-9dbf-898b17ecd928
- Submitted: 2026-10-17T05:46:06Z
- Fetched: 2026-10-17T06:16:55Z (status: success)
- Raw trajectory JSON: ../raw/b3-04-ultrasonic-atomized-cu-for-ded.json.gz
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

QUESTION: Report everything available on ultrasonic atomization of copper
alloys and on powders made from copper alloy scrap or machining chips for
DED. Start with Mueller et al. 2024, IOP Conf. Ser. Mater. Sci. Eng. 1296,
012036 (doi:10.1088/1757-899x/1296/1/012036): which atomizer and frequency,
melting method, feedstock (aluminium bronze chips), particle size, shape,
oxygen, yield, and how the powder performed in laser DED. Then: other
ultrasonic or small-batch atomization of Cu, bronzes, Cu-Ni or NAB;
AMAZEMET rePOWDER reports for any alloy melting above 1100 C with the
induction module (crucible plus pour onto the sonotrode) rather than arc or
plasma; and work on recycling naval copper alloy scrap or chips into AM
powder (point-of-need or shipyard sustainment). Give particle-size numbers
with frequency and melt temperature where reported.

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

QUESTION: Report everything available on ultrasonic atomization of copper
alloys and on powders made from copper alloy scrap or machining chips for
DED. Start with Mueller et al. 2024, IOP Conf. Ser. Mater. Sci. Eng. 1296,
012036 (doi:10.1088/1757-899x/1296/1/012036): which atomizer and frequency,
melting method, feedstock (aluminium bronze chips), particle size, shape,
oxygen, yield, and how the powder performed in laser DED. Then: other
ultrasonic or small-batch atomization of Cu, bronzes, Cu-Ni or NAB;
AMAZEMET rePOWDER reports for any alloy melting above 1100 C with the
induction module (crucible plus pour onto the sonotrode) rather than arc or
plasma; and work on recycling naval copper alloy scrap or chips into AM
powder (point-of-need or shipyard sustainment). Give particle-size numbers
with frequency and melt temperature where reported.

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


# Ultrasonic atomization and recycled copper-alloy feedstock for marine DED

**Scope and evidence limit.** The strongest direct precedent is already **ultrasonic atomization of nickel–aluminum-bronze (NAB) propeller-grinding chips followed by blown-powder laser DED**. It is therefore not defensible to claim novelty for that sequence alone. The distinguishing, still-unverified combination is *designed pre-alloyed compositions*, reproducible in-house powder production, sound deposits on both cast NAB and wrought Cu–Ni, and **as-deposited seawater performance benchmarked against wrought C71500**. “Ultrasonic vibration-assisted WAAM” means vibrating a build during deposition; it is **not** ultrasonic powder atomization. (uhlmann2024acomparativeevaluation pages 2-4, nemani2024advancementsinadditive pages 60-62, nemani2024advancementsinadditive pages 102-105)

## 1. Starting point: propeller-chip ultrasonic powder

**Müller, V.; Fasselt, J. M.; Kruse, T.; Klötzer, C.; Kleba-Ehrhardt, R.; Choma, T.; Biegler, M.; Rethmeier, M.** “Using ultrasonic atomization to recycle aluminium bronze chips for additive laser directed energy deposition.” *IOP Conference Series: Materials Science and Engineering* **1296**, 012036, indexed December **2023**; DOI **10.1088/1757-899X/1296/1/012036**. **Process:** recycled NAB chips → ultrasonically atomized powder → blown-powder laser DED. **[CITE] [NAVY: ship-propeller application, not verified US Navy funding] [NOVELTY-RISK: already demonstrates the scrap–ultrasonic-powder–laser-DED chain]**. The paper’s full text could not be obtained; its bibliographic record is indexed as 2023, although the question calls it 2024. The following **same-feedstock, same-investigator quantitative characterization comes from the accessible companion study**, not independently verified measurements from the IOP article. That companion explicitly says its authors previously used ultrasonic powder from the same grinding chips to make DED specimens. Consequently, neither a numerical IOP deposition density nor a claim of crack-free or corrosion-qualified IOP deposits can responsibly be supplied. (uhlmann2024acomparativeevaluation pages 2-4, uhlmann2024acomparativeevaluation pages 13-15)

**Uhlmann, E.; Polte, J.; Fasselt, J. M.; Müller, V.; Klötzer-Freese, C.; Kleba-Ehrhardt, R.; Biegler, M.; Rethmeier, M.** “A Comparative Evaluation of Powder Characteristics of Recycled Material from Bronze Grinding Chips for Additive Manufacturing.” *Materials* **17** (2024), 3396; DOI **10.3390/ma17143396**. **Process:** *powder preparation and testing*, with laser DED as the intended application; the article does not itself establish qualified deposited-part properties. **[CITE] [NUMBERS] [NAVY: maritime propellers; funded by EU MarTERA/Horizon 2020, not established US Navy/DoD funding] [NOVELTY-RISK] [GAP: actual DED-feed reliability, mechanical performance and seawater tests].** The feedstock was grinding chips from cast ship propellers, nominal **Cu balance, Al 8.5–10.5, Fe 4.0–5.5, Ni 4.0–6.0, Mn ≤3 wt%** (CuAl10Ni5Fe5/CC333G). The actual atomized powder’s reported EDX values were **Cu 75.16, Al 9.83, Fe 6.76, Ni 5.91, Mn 2.33 wt%**; EDX is not a high-precision certification of bulk composition. Equipment was an **AMAZEMET/BluePower AUS 500**, **induction furnace**, argon 5.0, **1,300 °C melt**, pressure-fed pour at **1.5 bar** onto a **40-kHz woven-carbon-fiber sonotrode**, followed by a **200-µm sieve**. This is an **AUS 500 result, not proof of the AMAZEMET rePOWDER induction module’s operating envelope**. (uhlmann2024acomparativeevaluation pages 7-10, uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 2-4, uhlmann2024acomparativeevaluation pages 13-15)

At **40 kHz/1,300 °C**, the area-equivalent image-analysis diameters were **D10/D50/D90 = 48/98/174 µm**, versus **64/95/135 µm** for commercial gas-atomized *different-composition* CuAl9.5Fe powder. Mean aspect ratio was **0.935** versus **0.843**; **82%** versus **43.5%** of particles had aspect ratio >0.9. Oxygen by hot-gas extraction was **0.013 wt%** in ultrasonic powder, versus **0.073 wt%** in sieved starting chips and **0.019 wt%** in the commercial powder. **Carney**, *not Hall*, funnel flow times were **8.62 versus 10.55 s/150 g**; Hausner ratios **1.05 versus 1.12**; repose angles **13.74° versus 20.08°**. Investigators saw few particle gas cavities but did **not** give a quantitative internal-powder-porosity fraction or a complete atomization/DED mass yield. Remaining ceramic grinding abrasives and ∼**20-µm carbon fibers from the sonotrode** are potential defect sources despite the excellent flow result. Corrosion electrolyte, duration, current, potential, impedance, attack depth, hardness, tensile properties and deposit density: **not measured in this powder-comparison paper**. (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 7-10, uhlmann2024acomparativeevaluation pages 6-7, uhlmann2024acomparativeevaluation pages 12-13, uhlmann2024acomparativeevaluation media c7a17bfe, uhlmann2024acomparativeevaluation media dda88e91)

**Müller, V.; Marko, A.; Kruse, T.; Biegler, M.; Rethmeier, M.** “Analysis and recycling of bronze grinding waste to produce maritime components using directed energy deposition.” Fraunhofer publication (2021); DOI **10.24406/publica-fhg-413178**. **Process:** *direct blown-powder laser DED of screened, irregular grinding waste—not atomized powder*. **[CITE] [NUMBERS] [NAVY: maritime application only] [GAP: screening does not solve feed defects].** The same nominal **CuAl10Fe5Ni5** propeller material, **Cu balance, Al 8.5–10.5, Fe 4.0–5.5, Ni 4.0–6.0, Mn <3 wt%**, was screened at **125 µm**; roughly **80% of original chips were retained/excluded**, which is a *screening loss*, **not** an ultrasonic-atomization yield. More than half the screened chips had maximum Feret length **>166 µm**, whereas 90% of reference commercial powder was **<150 µm**. Powder transport required an enlarged **11-mm** groove, was stable only up to about **7 g/min**, and DED ran at **6 g/min**, **600 W**, **370 mm/min**, **1.5-mm spot** on **316L steel**. Irregular feed, smoke/contamination, ceramic inclusions, porosity and chip-shaped lack-of-fusion defects resulted; **no defensible numeric deposit porosity, oxygen or seawater-corrosion outcome** was located. This failed direct-chip approach should not be represented as failure of the later remelted, spherical ultrasonic powder. (muller2021analysisandrecycling pages 4-6, muller2021analysisandrecycling pages 6-9, muller2021analysisandrecycling pages 1-4)

## 2. Other ultrasonic and small-batch reports: keep equipment and melting routes separate

**Cabrioli, M.; Colmenero, M. S.; Gholamzadeh, S.; Vanazzi, M.; Amirabdollahian, S.; Perini, M.; Łacisz, W.; Kalicki, B.** “Upcycling of Copper Scrap into High-Quality Powder for Additive Manufacturing: Processing, Characterization, and Sustainability Assessment.” *Journal of Manufacturing and Materials Processing* **9** (2025), 320; DOI **10.3390/jmmp9090320**. **Process:** insulated offshore-cable scrap → copper separation → **AMAZEMET rePOWDER ultrasonic atomization** → **laser blown-powder DED**. **[CITE] [NAVY: offshore/maritime context, not demonstrated Navy funding] [NOVELTY-RISK: recycled Cu to laser DED, but not a designed marine Cu alloy] [GAP].** The indexed article abstract identifies **approximately 99.5 wt% Cu**, successful DED printing and an assessed **>70% lower life-cycle global-warming potential** than the conventional mining route. Its indexed search excerpt identifies a **graphite crucible/induction furnace**, but the retrieved purported full text was **an unrelated report**, so **temperature, ultrasound frequency, D10/D50/D90, powder oxygen, Hall time, densities, powder yield, DED porosity, hardness, strength, saltwater protocol and corrosion measurements cannot be verified here**. It is effectively *near-pure copper*, not Cu–10–30Ni or NAB. Treat the indexed abstract as preliminary evidence, not as support for invented tabulated results. (ciftcli2025alloydevelopmentfrom pages 1-3, uhlmann2024acomparativeevaluation pages 2-4)

**Ciftci, J.; Choma, T.; Morończyk, B.; Kalicki, B.; Puchalski, F.; Żrodowski, Ł.** “Alloy Development From Sustainable Materials—Close-Loop of Materials Using Ultrasonic Atomization.” *Journal of the Japan Society of Powder and Powder Metallurgy* **72** (2025), S729–S735; DOI **10.2497/jjspm.15E-SIS13-03**. **Process:** AMAZEMET **rePOWDER**; a pictured **induction-melted, crucible-poured copper-alloy atomization stream**, alongside separate **induction-atomized Mg alloy**, **plasma-atomized C103 Nb alloy** and **arc-remelted/plasma-atomized Ti machining chips**. **[CITE] [GAP: Cu-alloy process image, not characterized Cu-alloy powder].** The induction apparatus uses an argon-pressure-actuated crucible pour onto a vibrating blade; **60 kHz** is specified for the **Mg** experiment, **not expressly for the pictured copper alloy**. There is **no reported Cu alloy composition, melt temperature, particle-size distribution, oxygen, recovered fraction or Cu-alloy DED outcome**. The article’s **40-kHz**, volume-based **36/49/118-µm D10/D50/D90**, **>85% below 100 µm** and **<600-ppm oxygen** refer to **arc/plasma-processed recycled Ti-alloy chips**, *not* induction-atomized Cu. Likewise, C103 is **plasma** melted. Neither may be presented as evidence of >1,100 °C **rePOWDER-induction** capability. (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6)

**Ukabhai, K. D.; Mkhonto, D.; Phasha, M.** “Investigation of Al-Cu using different preparation methods on the Amazemet RePowder machine.” *MATEC Web of Conferences* **417** (2025), 03001; DOI **10.1051/matecconf/202541703001**. **Process:** **rePOWDER induction-crucible/pour ultrasonic atomization**, with a separate **arc-melted comparison rod**; no AM build. **[CITE] [NUMBERS] [GAP: not Cu-rich and not above 1,100 °C].** Feed was **Al–10Cu wt%** mixed from pure Al and Cu pellets, not Cu–10Al. A **100-g** charge was induction melted at **1,100 °C**, argon-flushed, and poured onto a **40-kHz** plate; reported powder **d10/d50/d90 = 36/65/78 µm**. The text also says “90% below 70 µm,” which conflicts with its own **d90 = 78 µm** table; use the tabulated triplet with that caveat. Powder was predominantly spherical. No Hall flow, oxygen, recovered mass fraction, deposited density, mechanical, seawater or corrosion measurements were reported. This is a concrete **induction-module** example, but **not a melt above 1,100 °C** or proof of successful Cu-rich-alloy powder production. The authors describe an approximate **1,300 °C induction-module limit**, which should be tested for *each actual alloy/crucible/pour configuration* rather than treated as verified NAB/Cu–Ni capability. (ukabhai2025investigationofalcu pages 7-10, ukabhai2025investigationofalcu pages 1-3, ukabhai2025investigationofalcu pages 3-7)

**Finding on the requested high-temperature rePOWDER subset. [GAP]** Among the inspected original reports, **none provides a verified Cu, bronze, NAB or Cu–Ni powder dataset with an expressly stated *>1,100 °C* melt made by the *rePOWDER induction module* rather than arc or plasma**. The **1,300 °C NAB/40-kHz result belongs to the distinct AUS 500 apparatus**. The rePOWDER copper-stream photograph establishes that induction pouring of *some* copper alloy was attempted, but supplies neither composition nor temperature. Reporting the AUS 500 result as an already-proven in-house rePOWDER result would conceal a genuine equipment-specific feasibility risk. (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6, uhlmann2024acomparativeevaluation pages 4-6, ukabhai2025investigationofalcu pages 1-3)

**Afshari, E.; Ghambari, M.; Abdolmalek, H.** “Production of CuSn10 Bronze Powder from Machining Chips Using Jet Milling.” *International Journal of Advanced Manufacturing Technology* **92** (2017), 663–672; **DOI not verified in the available record**. **Process:** Cu–**10 wt% Sn** machining chips → **jet-milled**, *not ultrasonically atomized* powder; **no verified blown-powder DED demonstration**. **[CITE: qualified scrap-processing antecedent] [GAP].** The accessible later study describes jet-milled powder as irregular but less oxidized/hardened than ball-milled powder; quantitative PSD, oxygen and deposit/seawater data from the original could not be checked. Do not turn this powder-production paper into evidence for shipyard DED qualification. (uhlmann2024acomparativeevaluation pages 1-2, uhlmann2024acomparativeevaluation pages 13-15)

## 3. Closest deposit and seawater benchmarks—not scrap-ultrasonic-powder results

**Zhao, L.; Li, K.; Yao, J.; Yuan, Y.; Du, B.** “The Laser Deposited Nickel-Aluminum Bronze Coatings on SUS630 Stainless Steel and Its Corrosion Resistance in 3.5 wt.% NaCl Solution.” *Metals* **12** (2022), 781; DOI **10.3390/met12050781**. **Process:** blown-powder **laser deposition/cladding** of pre-existing **53–120-µm** NAB powder onto **SUS630 stainless steel**, directly (N-1) or over Ni–Al (N-2) or Ni–Cr (N-3) powder interlayers; *not* cast-NAB repair, ultrasonic powder or single-feed interlayer-free repair. Feed was **Cu 81.1, Al 10.8, Ni 4.1, Fe 4.0 wt%**. **[CITE] [NUMBERS] [NOVELTY-RISK: deposited NAB corrosion is established; interlayers violate the proposed single-stream comparison] [GAP: different substrates and chemistry].** At **25 ± 5 °C** in **3.5 wt% NaCl**, specimens equilibrated **20 min** before polarization; longer immersion observations ran to **21 days**. Polarization **i_corr** was **7.82 ± 0.50 / 4.65 ± 0.50 / 4.09 ± 0.40 µA cm⁻²**, **E_corr −248/−255/−252 mV** (reference scale should be checked before inter-study comparison), and calculated **R_p 2,810/5,275/4,865 Ω cm²**, for N-1/N-2/N-3. Maximum corrosion depths after the immersion series were **3.4 ± 0.1/2.0 ± 0.1/1.8 ± 0.1 µm**; Fe-rich dendrites dominated selective attack in N-1. At **21 days**, fitted EIS **R_ct** was **1,444/51,470/85,100 Ω cm²**. The independent tensile comparator called *as-deposited NAB* was **669 ± 10.4 MPa UTS, 17.46 ± 1.2% elongation**; composite N-1/N-2/N-3 values were **767.80 ± 7.3/891.54 ± 8.5/731.05 ± 6.7 MPa UTS** and **12.89 ± 1.0/6.87 ± 0.5/9.44 ± 0.6% elongation**, respectively. Coatings are described as dense, without a numeric porosity fraction; **hardness is not established here**. Do not compare a fresh 20-min polarization number directly with a year-long immersion mass-loss rate. (zhao2022thelaserdeposited pages 2-4, zhao2022thelaserdeposited pages 4-7, zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 13-14, zhao2022thelaserdeposited pages 10-13)

**Huo, R.; Wang, Z.; Wang, M.; Wang, R.; Zhang, S.; Zhang, C.; Wu, C.; Chen, H.; Chen, J.** “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing.” *Materials* **18** (2025), 2205; DOI **10.3390/ma18102205**. **Process:** **wire-arc DED/WAAM (cold-metal-transfer)**, **not powder laser DED**; ERCuNiAl wire **Cu balance, Al 8.73, Fe 5.90, Ni 4.52, Mn 1.39 wt%**, deposited on a copper-alloy plate, measured **as deposited**. **[CITE] [NUMBERS] [GAP: phase/thermal-history benchmark only].** In **aerated 3.5 wt% NaCl, 25 ± 5 °C**, with **3,600-s initial OCP stabilization** and short-duration electrochemistry, increasing heat input **243.8 → 644.7 J/mm** increased grain size **38.26 → 74.62 µm**, decreased reported measured surface hardness **192.4 ± 6.9 → 166.9 ± 0.3 HV**, increased **i_corr 2.56 ± 0.04 → 7.52 ± 0.07 µA cm⁻²**, and lowered fitted EIS **R_ct 2,485 → 707 Ω cm²**. The four polarization-potential entries are **−269.61 ± 40, −466.62 ± 10, −517.77 ± 20, −700.94 ± 15 mV** for progressively higher heat inputs. **Caution:** the abstract instead quotes hardness **198.3 → 171.7 HV**, while the results/conclusion give the measured **192.4 → 166.9 HV**; moreover, the EIS table labels *two successive rows S2* although four samples are discussed. Specify which source within the article a number comes from. No 30-day immersion, measured long-term rate or powder yield is provided. (huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 1-2, huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 13-15, huo2025modulatingheatinput pages 7-10, huo2025modulatingheatinput pages 15-16)

**Nemani, A. V.; Ghaffari, M.; Bokati, K. S.; Valizade, N.; Afshari, E.; Nasiri, A.** “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review.” *Journal of Manufacturing and Materials Processing* **8** (2024), 54; DOI **10.3390/jmmp8020054**. **Process:** *review*, carefully distinguishing laser DED, WAAM and LPBF. **[CITE] [NOVELTY-RISK] [GAP].** Its reference list identifies two especially pertinent, original, **non-ultrasonic** powder-DED NAB-repair precedents: **Yao, C.-L.; Kang, H.-S.; Lee, K.-Y.; Zhai, J.-G.; Shim, D.-S.** “A study on mechanical properties of CuNi2SiCr layered on nickel–aluminum bronze via directed energy deposition.” *Journal of Materials Research and Technology* **18** (2022), 5337–5361; DOI **10.1016/j.jmrt.2022.04.159**; and **Yao, C.-L.; Shim, D.-S.** “Corrosive properties of CuNi2SiCr fabricated through directed energy deposition on a nickel-aluminum bronze substrate.” *Journal of Alloys and Compounds* **918** (2022), 165776; DOI **10.1016/j.jallcom.2022.165776**. **Process:** laser powder DED of **CuNi2SiCr** onto **cast NAB**. CuNi2SiCr signifies an approximately **2-wt%-Ni precipitation-hardening Cu alloy**, **not** Cu–10–30Ni; its exact lot chemistry and corrosion test conditions/numbers are **unverified because both primary texts were unobtainable**. The review reports a **porous, low-hardness/low-strength deposit** relative to the NAB substrate in the mechanical study and says this particular repair combination was **not recommended**; it establishes an important failure mode, *not* a validated C71500-performance benchmark. The separate corrosion study must not be assumed to reach that same conclusion without its results. (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 113-114)

The same review lists **Li, B.; Zheng, H.; Han, C.; Zhou, K.**, “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition.” *Additive Manufacturing* **39** (2021), 101825; DOI **not independently verified here**. **Process:** laser metal deposition of **Cu balance–9Al–5Fe–5Ni wt%**, *not recycled ultrasonic powder*. Reported **yield strength 593–713 MPa**, **UTS 769–949 MPa**, **elongation 10–12%** across process conditions. No directly checked seawater protocol or i_corr is available for this item. **[CITE] [NUMBERS] [NOVELTY-RISK: NAB laser deposition and attractive as-built strength are not new] [GAP: qualified corrosion and recycled powder].** (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 113-114)

**Al-Fozan, S. A.; Malik, A. U.** “Effect of seawater level on corrosion behavior of different alloys.” *Desalination* **228** (2008), 61–67; DOI **10.1016/j.desal.2007.08.007**. **Process:** conventional **wrought** Cu–Ni exposure coupons, *not AM*. **[CITE] [NUMBERS] [GAP: a long-duration seawater reference, not a 30-day pass/fail specification].** The tested 70/30 alloy was **Cu 68.81, Ni 30.00, Fe 0.53, Mn 0.51 wt%** plus traces. Exposures were in **natural Arabian Gulf seawater** (chloride **24,090 ppm**, dissolved oxygen **7 ppm**, pH **8.1**) at approximately **25 ± 5 °C**, **12 L/h** circulation, with above-water, waterline and fully submerged placements. Fully submerged 70/30 corrosion rates at **192 and 365 days** were **0.067 and 0.049 mil/year (mpy)**, respectively—approximately **1.70 and 1.24 µm/year** using 1 mpy = 25.4 µm/year. Waterline rates were **0.082 and 0.098 mpy**. These are **long-exposure weight-loss rates**, not Tafel i_corr, and the alloy is a 70/30 *composition* comparator rather than a verified heat-specific certified C71500 coupon. No matched 30-day C71500 i_corr, E_corr, EIS or selective-attack threshold can be inferred. (alfozan2008effectofseawater pages 1-3, alfozan2008effectofseawater pages 3-5)

**Powell, C.** “Corrosion and Biofouling Resistance Evaluation of 90-10 Copper-Nickel” (2004); **DOI not verified**. **Process:** literature/field-exposure review of **wrought** Cu–Ni, primarily **Cu balance–9–11Ni–1–2Fe–0.5–1Mn wt% (C70600)**; **not** C71500 or AM. **[CITE] [NAVY: naval seawater-piping application, not identified DoD-funded research] [GAP].** Protective films can take **2–3 months** to mature in temperate seawater; published long-term review data approach approximately **1.3 µm/year** only after years of exposure. This is why **30-day static NaCl, 30-day flowing natural/artificial seawater and long-service wrought 70/30 rates are not interchangeable**, and why film development and hydrodynamics must be controlled in proposal comparisons. (powell2004corrosionandbiofouling pages 1-4, powell2004corrosionandbiofouling pages 4-6)

## What was **not** established

No verified source in this search demonstrates **rePOWDER induction-crucible/pour atomization above 1,100 °C of an explicitly specified Cu–Ni/NAB alloy with full powder PSD–Hall flow–apparent density–oxygen–yield data**, nor a **single-stream, pre-alloyed ultrasonic-powder laser-DED alloy series that is dense and crack-free both on itself and on cast NAB *and* wrought Cu–Ni and exceeds matched, as-deposited C71500 seawater performance without post-build heat treatment**. Equally, I found **no substantiated US Navy/DoD-funded publication specifically closing a shipyard NAB/Cu–Ni chips → qualified ultrasonic powder → corrosion-qualified DED repair loop**; German/EU propeller recycling is a *marine application*, not proof of Navy sponsorship. Report these as limits of the **retrieved evidence**, rather than universal claims that no such project exists. The inaccessible IOP, Yao and Cabrioli primary/full-text records prevent some requested deposit and powder measurements from being supplied. (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6, uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 13-15, nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 102-105)

## Top 5 things the PI should know

1. **Novelty must begin *after* the demonstrated propeller-chip → ultrasonic NAB powder → laser-DED chain.** Its powder already reached **48/98/174 µm**, **0.013 wt% O**, and **8.62 s/150 g Carney flow** at **1,300 °C/40 kHz**—but on an **AUS 500**, not proven rePOWDER induction hardware. (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 6-7, uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 2-4)
2. **Do not substitute arc/plasma success or Al–10Cu for a hot Cu-rich induction melt.** The only checked rePOWDER induction *numerical powder* result is **Al–10Cu at 1,100 °C/40 kHz**; qualify melt throughput, sonotrode wear, composition drift and per-lot yield on the actual Cu–Ni/NAB apparatus. (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6, ukabhai2025investigationofalcu pages 1-3, ukabhai2025investigationofalcu pages 3-7)
3. **Repair metallurgy is already a known hazard, not an empty application space.** Published CuNi2SiCr-on-cast-NAB **laser-powder DED** exists, and a reported porous/soft deposit was unsuitable mechanically; steel/NAB laser deposits also exhibit Fe-rich selective attack. Quantify the *bond region as well as the exposed deposit*. (nemani2024advancementsinadditive pages 79-83, zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 10-13)
4. **Establish an actual matched C71500 control before claiming a corrosion target.** Natural-seawater wrought 70/30 weight-loss rates after **192/365 days** were **0.067/0.049 mpy**, but they cannot be imposed as unmeasured 30-day electrochemical thresholds. Run same-exposure wrought controls and report local attack, flow and surface preparation. (alfozan2008effectofseawater pages 1-3, alfozan2008effectofseawater pages 3-5, powell2004corrosionandbiofouling pages 1-4)
5. **Make the proposal’s differentiator a verified composition → powder → deposit/interface → *as-deposited* seawater comparison**, explicitly testing whether heat-history-informed phase predictions add value over equilibrium CALPHAD and no physics. Powder oxygen, contamination and actual DED feed stability deserve separate model nodes: excellent benchtop powder flow alone did not establish long-term corrosion-qualified repair. (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 13-15, zhao2022thelaserdeposited pages 10-13, huo2025modulatingheatinput pages 15-16)

References

1. (uhlmann2024acomparativeevaluation pages 2-4): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

2. (nemani2024advancementsinadditive pages 60-62): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

3. (nemani2024advancementsinadditive pages 102-105): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

4. (uhlmann2024acomparativeevaluation pages 13-15): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

5. (uhlmann2024acomparativeevaluation pages 7-10): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

6. (uhlmann2024acomparativeevaluation pages 4-6): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

7. (uhlmann2024acomparativeevaluation pages 10-12): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

8. (uhlmann2024acomparativeevaluation pages 6-7): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

9. (uhlmann2024acomparativeevaluation pages 12-13): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

10. (uhlmann2024acomparativeevaluation media c7a17bfe): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

11. (uhlmann2024acomparativeevaluation media dda88e91): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

12. (muller2021analysisandrecycling pages 4-6): Vinzenz Müller, Angelina Marko, Tobias Kruse, Max Biegler, and Michael Rethmeier. Analysis and recycling of bronze grinding waste to produce maritime components using directed energy deposition. Text, 2021. URL: https://doi.org/10.24406/publica-fhg-413178, doi:10.24406/publica-fhg-413178. This article has 5 citations and is from a peer-reviewed journal.

13. (muller2021analysisandrecycling pages 6-9): Vinzenz Müller, Angelina Marko, Tobias Kruse, Max Biegler, and Michael Rethmeier. Analysis and recycling of bronze grinding waste to produce maritime components using directed energy deposition. Text, 2021. URL: https://doi.org/10.24406/publica-fhg-413178, doi:10.24406/publica-fhg-413178. This article has 5 citations and is from a peer-reviewed journal.

14. (muller2021analysisandrecycling pages 1-4): Vinzenz Müller, Angelina Marko, Tobias Kruse, Max Biegler, and Michael Rethmeier. Analysis and recycling of bronze grinding waste to produce maritime components using directed energy deposition. Text, 2021. URL: https://doi.org/10.24406/publica-fhg-413178, doi:10.24406/publica-fhg-413178. This article has 5 citations and is from a peer-reviewed journal.

15. (ciftcli2025alloydevelopmentfrom pages 1-3): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72(Supplement):S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 7 citations.

16. (ciftcli2025alloydevelopmentfrom pages 3-6): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72(Supplement):S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 7 citations.

17. (ukabhai2025investigationofalcu pages 7-10): Kiyaasha Dyal Ukabhai, Donald Mkhonto, and Maje Phasha. Investigation of al-cu using different preparation methods on the amazemet repowder machine. MATEC Web of Conferences, 417:03001, Jan 2025. URL: https://doi.org/10.1051/matecconf/202541703001, doi:10.1051/matecconf/202541703001. This article has 0 citations.

18. (ukabhai2025investigationofalcu pages 1-3): Kiyaasha Dyal Ukabhai, Donald Mkhonto, and Maje Phasha. Investigation of al-cu using different preparation methods on the amazemet repowder machine. MATEC Web of Conferences, 417:03001, Jan 2025. URL: https://doi.org/10.1051/matecconf/202541703001, doi:10.1051/matecconf/202541703001. This article has 0 citations.

19. (ukabhai2025investigationofalcu pages 3-7): Kiyaasha Dyal Ukabhai, Donald Mkhonto, and Maje Phasha. Investigation of al-cu using different preparation methods on the amazemet repowder machine. MATEC Web of Conferences, 417:03001, Jan 2025. URL: https://doi.org/10.1051/matecconf/202541703001, doi:10.1051/matecconf/202541703001. This article has 0 citations.

20. (uhlmann2024acomparativeevaluation pages 1-2): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

21. (zhao2022thelaserdeposited pages 2-4): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

22. (zhao2022thelaserdeposited pages 4-7): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

23. (zhao2022thelaserdeposited pages 7-10): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

24. (zhao2022thelaserdeposited pages 13-14): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

25. (zhao2022thelaserdeposited pages 10-13): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

26. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

27. (huo2025modulatingheatinput pages 1-2): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

28. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

29. (huo2025modulatingheatinput pages 13-15): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

30. (huo2025modulatingheatinput pages 7-10): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

31. (huo2025modulatingheatinput pages 15-16): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

32. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

33. (nemani2024advancementsinadditive pages 113-114): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

34. (alfozan2008effectofseawater pages 1-3): Saleh A. Al-Fozan and Anees U. Malik. Effect of seawater level on corrosion behavior of different alloys. Desalination, 228:61-67, Aug 2008. URL: https://doi.org/10.1016/j.desal.2007.08.007, doi:10.1016/j.desal.2007.08.007. This article has 190 citations and is from a domain leading peer-reviewed journal.

35. (alfozan2008effectofseawater pages 3-5): Saleh A. Al-Fozan and Anees U. Malik. Effect of seawater level on corrosion behavior of different alloys. Desalination, 228:61-67, Aug 2008. URL: https://doi.org/10.1016/j.desal.2007.08.007, doi:10.1016/j.desal.2007.08.007. This article has 190 citations and is from a domain leading peer-reviewed journal.

36. (powell2004corrosionandbiofouling pages 1-4): C Powell. Corrosion and biofouling resistance evaluation of 90-10 copper-nickel. Unknown journal, 2004.

37. (powell2004corrosionandbiofouling pages 4-6): C Powell. Corrosion and biofouling resistance evaluation of 90-10 copper-nickel. Unknown journal, 2004.
