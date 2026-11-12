<!--
Edison Scientific LITERATURE task (batch 5)
- Task ID: 1a8c4326-4281-450f-bdf7-31ac5fcb5a78
- Submitted: 2026-10-17T06:20:10Z
- Fetched: 2026-10-17T06:52:02Z (status: success)
- Raw trajectory JSON: ../raw/b5-10-cuni-segregation-film-am.json.gz
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

QUESTION: How does dendritic segregation of Ni, Fe and Mn in as-solidified
or as-deposited Cu-Ni (welds, castings, WAAM, LPBF, laser deposits) change
corrosion product film formation and localized attack in seawater, and how
large is the segregation (EDS/EPMA core-to-interdendrite contrast) as a
function of cooling rate? Include Song et al. 2024 (WAAM 70-30), Liu et al.
2024 and Nadimi et al. 2025 (LPBF 70-30), Cu-Ni weld metal studies, and the
role of Fe in solution vs precipitated. Can a Scheil or back-diffusion
calculation predict the measured contrast, and does it predict corrosion?

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

QUESTION: How does dendritic segregation of Ni, Fe and Mn in as-solidified
or as-deposited Cu-Ni (welds, castings, WAAM, LPBF, laser deposits) change
corrosion product film formation and localized attack in seawater, and how
large is the segregation (EDS/EPMA core-to-interdendrite contrast) as a
function of cooling rate? Include Song et al. 2024 (WAAM 70-30), Liu et al.
2024 and Nadimi et al. 2025 (LPBF 70-30), Cu-Ni weld metal studies, and the
role of Fe in solution vs precipitated. Can a Scheil or back-diffusion
calculation predict the measured contrast, and does it predict corrosion?

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


# Dendritic segregation and seawater corrosion of as-deposited Cu–Ni

**Bottom line.** The strongest measured pattern is **Ni and Fe enrichment in dendrite cores, but Mn enrichment in the last-solidified interdendritic material**. In WAAM 70/30 Cu–Ni, the Ni-poor interdendritic network is preferentially attacked after chloride polarization, even though some WAAM specimens outperform wrought 70/30 on specimen-scale electrochemical metrics. Weld microprobe data quantify a much larger local contrast than a nominal alloy composition reveals. The literature reviewed does **not** establish segregation contrast as a measured function of cooling rate, nor validate a Scheil/back-diffusion calculation as a predictor of seawater corrosion. (song2024microstructuresandcorrosion pages 13-14, devletian2006fluxcoredarc pages 7-10, song2024microstructuresandcorrosion pages 14-17)

The following comparison keeps measured compositions separate from estimates and makes the missing cooling-rate measurements explicit.

| Source / process | Nominal or bulk composition (wt%) | Measured core / interdendritic composition (wt%) | Quantified contrast | Cooling rate | Corrosion linkage |
|---|---|---|---|---|---|
| Savage, Nippes & Miller, Cu–Ni weld metal; data reproduced by Devletian et al. | Bulk: Ni 29.6, Fe 0.52, Mn 0.87, Cu 68.9 | Dendrite core / crack-tip boundary: Ni 38.0 / 16.4; Fe 0.59 / 0.22; Mn 0.90 / 1.71; Cu 60.5 / 81.6 | Core-to-boundary ratio: Ni 2.32, Fe 2.68; Mn partitions oppositely, ratio 0.53. Boundary is 21.6 percentage points Ni-poorer and 21.1 points Cu-richer. | Not reported numerically | Establishes strong Ni and Fe depletion and Mn enrichment in terminal interdendritic liquid associated with solidification cracking, but no seawater-corrosion test was paired with the EPMA profiles. (devletian2006fluxcoredarc pages 7-10) |
| Mukherjee & Ghosh 2011, laser-assisted direct metal deposition (DMD) | Cu–Ni 70/30 specification: Ni 29–33, Fe 0.4–0.7, Mn ≤1, Cu balance | Dendrite / interdendritic: Cu ≈63 / ≈71; Ni was not independently quantified in the extracted EDS result. | Interdendritic region is ≈8 percentage points Cu-richer. Values of ≈37/29 wt% Ni are only binary-balance estimates and are **not measured Ni values**. | Not reported numerically; described only as high solidification rate/undercooling | DMD corrosion rate was 9.1 µm/y after 30 days in static ASTM D1141 synthetic seawater; the study did not spatially map attack onto the EDS profile. (mukherjee2011frictionstirprocessing pages 1-2, mukherjee2011frictionstirprocessing pages 5-6) |
| Song et al. 2024, wire-arc DED/WAAM | Wire: Cu 67.5, Ni 30, Fe 0.55, Mn 0.7, Ti 0.25, Si 0.1 | Ni-rich dendrite cores and Ni-depleted interdendritic regions; line scans showed a maximum stated “20% concentration difference,” but tabulated endpoint compositions were not supplied. | Treat “20%” as ambiguous—neither 20 percentage points nor 20% relative contrast is established explicitly in the text. | Not measured or reported numerically | Polarization produced preferential interdendritic attack attributed to Ni depletion. Sample 6 nevertheless exceeded wrought material in bulk electrochemical metrics, so segregation did not determine specimen-level ranking by itself. (song2024microstructuresandcorrosion pages 13-14, song2024microstructuresandcorrosion pages 2-5, song2024microstructuresandcorrosion pages 14-17) |
| Gao et al. 2025, LPBF CuNi30–xCr | Base powder: Cu–30.450Ni–0.590Fe–0.470Mn–0.130Si–0.009C; Cr added at 0–3 | No matched Ni/Fe/Mn dendrite-core/interdendritic EDS values reported; Cr changed from mainly dissolved at low addition to 4–30 µm Cr-rich regions at higher addition. | No quantitative Ni, Fe, or Mn segregation contrast suitable for comparison. | Generic LPBF range stated as 10³–10⁶ K/s and local rate as >10³ K/s; not measured for the analyzed specimens. | In short-term 3.5 wt% NaCl tests, adding 3% Cr shifted Ecorr from −0.238 to −0.210 V vs SCE and reduced icorr from 1.38×10⁻⁶ to 7.72×10⁻⁷ A/cm²; this does not validate a cooling-rate–segregation relationship. (shiyang2025effectofcr pages 1-4, shiyang2025effectofcr pages 4-7, shiyang2025effectofcr pages 7-9) |


*Table: Quantitative core-to-interdendritic contrasts are available for weld metal and laser DMD, but no study supplies a calibrated cooling-rate series with matching Ni–Fe–Mn measurements and seawater corrosion. The table separates measured values from inferred or ambiguously reported contrasts.*

## Directly relevant studies and benchmarks

**1. Song, J., Jimenez, X. A., To, A. C., and Fu, Y., “Microstructures and Corrosion Properties of Wire Arc Additive Manufactured Copper–Nickel Alloys,” *Materials* 17 (2024), 876. DOI: 10.3390/ma17040876.** **Process:** wire-arc DED/WAAM, not laser or powder DED. **Composition, wt%:** TECHALLOY 413 wire Cu 67.5, Ni 30, Fe 0.55, Mn 0.70, Ti 0.25, Si 0.10; wrought C71500 comparison plate Cu 68.046, Ni 30.46, Fe 0.56, Mn 0.73. **Test:** naturally aerated, room-temperature **3.5 wt% NaCl**, 3 h open-circuit exposure followed by EIS and cyclic polarization; this was not a natural-seawater or 30-day immersion test. No porosity or macro/microscopic cracks were observed by optical microscopy, but numerical density was not reported. (song2024microstructuresandcorrosion pages 1-2, song2024microstructuresandcorrosion pages 2-5)

EDS shows Ni-rich cores and Ni-depleted interdendritic regions; the authors describe a local Ni concentration difference **as high as “20%,” without tabulating matched core/interdendritic wt% or defining whether this means percentage points or relative percent**. After polarization, interdendritic areas attack preferentially. The best overall WAAM condition was 8 m/min wire feed, 1000 mm/min travel, 3.85 mm track spacing. Its fitted film resistance was **1.40 × 10⁵ Ω (XY)** and **1.66 × 10⁵ Ω (YZ)** versus **1.08 × 10⁵** and **1.18 × 10⁵ Ω** for wrought plate; these are reported **Ω, not Ω·cm²**. Its passive current was lower and breakdown potential higher than wrought, but numerical *i*₍corr₎, corrosion rate, and localized-attack depth were not established. The authors assumed Cu₂O to estimate film thicknesses of tens to hundreds of nanometers; they did **not** directly establish comparative film chemistry. Wire and plate also differ in Ti and Si, confounding any attribution of their bulk ranking solely to segregation. **[CITE] [NUMBERS] [NAVY]** ONR grant N00014-21-1-2800. **[NOVELTY-RISK]** As-built Cu–Ni segregation and corrosion optimization already exist for WAAM. **[GAP]** No measured cooling-rate/segregation calibration, long immersion, or Fe/Mn core-to-boundary analysis. (song2024microstructuresandcorrosion pages 13-14, song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion pages 14-17)

**2. Savage, W. F., Nippes, E. F., and Miller, T. W., “Microsegregation in 70CuNi 70/30 Weld Metal,” *Welding Journal* (June 1976), 165s–173s. DOI: not identified.** The original microprobe table is reproduced in **Devletian, J. H., and Sullivan, M. J., *Flux Cored Arc Welding of CuNi 90/10 Piping with CuNi 70/30 Filler Metal*, Portland State University/NASSCO final report (2006), DOI: not identified**. **Process:** Cu–Ni fusion weld metal; the related investigation included GTAW/Varestraint welds, not DED. **Measured wt%, bulk → core → dendrite-boundary crack tip:** Ni **29.6 → 38.0 → 16.4**; Fe **0.52 → 0.59 → 0.22**; Mn **0.87 → 0.90 → 1.71**; Cu **68.9 → 60.5 → 81.6**. Thus the core–boundary differences are **21.6 percentage points Ni**, **0.37 Fe**, and **−0.81 Mn**. Back-filled liquation cracks contained **12.7–15.6 Ni, 0.10–0.14 Fe, and 1.94 Mn wt%**. These crack-tip/liquation samples probe extreme last-liquid chemistry, **not** a representative uncracked-dendrite average. No cooling rate or seawater-corrosion test accompanies these profiles. **[CITE] [NUMBERS] [NAVY]** Navy weldability relevance. **[GAP]** The most useful Ni–Fe–Mn partition benchmark is not itself a corrosion-prediction dataset. (devletian2006fluxcoredarc pages 7-10, devletian2006fluxcoredarc pages 43-48)

The companion **Devletian–Sullivan 2006** FCAW study used 70/30-type filler on **90/10 Cu–Ni naval pipe**: analyzed experimental deposits contained approximately **32.1–32.6 Ni, 0.80–0.81 Fe, and 0.50–1.00 Mn wt%**. Welds were fully dendritic, with Ni-rich cores, but porosity and spatter were unacceptable; no weld/HAZ cracking was observed. Weld-metal hardness was **99–107 KHN**; transverse joint tensile strengths were approximately **41,200–45,000 psi**, with weld-metal failures affected by inclusions/pores. There was **no seawater test** and no quantitative Fe/Mn profile for these experimental FCAW deposits. These results warn that crack freedom alone does not establish density or corrosion suitability. **[NUMBERS] [NAVY] [GAP]** (devletian2006fluxcoredarc pages 1-4, devletian2006fluxcoredarc pages 30-37, devletian2006fluxcoredarc pages 37-43)

**3. Mukherjee, S., and Ghosh, A. K., “Friction stir processing of direct metal deposited copper–nickel 70/30,” *Materials Science and Engineering A* 528 (2011), 3289–3294. DOI: 10.1016/j.msea.2011.01.063.** **Process:** laser-assisted **direct metal deposition** onto rolled/wrought 70/30 Cu–Ni, then optional friction-stir processing (FSP); the publication does **not verify that its DMD feed was one pre-alloyed powder stream**. It provides a *typical-alloy range*, not a lot assay: **29–33 Ni, 0.4–0.7 Fe, ≤1 Mn wt%, Cu balance**. **Test:** ASTM G31 **30-day static immersion**, ASTM D1141 synthetic seawater at **20 °C, pH 8.2**, sealed vessel; flow was not imposed. As-deposited DMD had approximately **63 wt% Cu in dendrites versus 71 wt% interdendritic**, an **8-percentage-point** contrast; converting these to 37/29 Ni assumes binary balance and is **not measured Ni**. Dendrite-arm spacing was approximately **5.7 µm**. Porosity was **3.3%** next to the substrate and **1.3%** in the upper DMD layer; FSP reduced it to **0.35%** but produced overlap-region fine cracks. (mukherjee2011frictionstirprocessing pages 2-5, mukherjee2011frictionstirprocessing pages 1-2, mukherjee2011frictionstirprocessing pages 5-6)

DMD versus FSP, respectively: immersion corrosion **9.1 versus 12.7 µm/year**, yield strength **187.1 versus 325 MPa**, UTS **339.4 versus 350.2 MPa**, elongation **13.8% versus 1.2%**; the FSP region reached approximately **145 HV**. Thirty-day FSP specimens showed preferential attack along overlap regions, without a reported attack depth. Crucially, **less porosity and apparent homogenization did not improve the measured corrosion rate**; the authors suggest, but do not demonstrate, Fe precipitation as one possible reason. **[CITE] [NUMBERS] [NAVY]** ONR grant N00014-07-C0282 and Naval Undersea Warfare Center input. **[NOVELTY-RISK]** Laser-deposited Cu–Ni on Cu–Ni repair substrate and 30-day substitute-seawater testing already exist. **[GAP]** Powder provenance, controlled compositions, substrate-interface corrosion, and Fe phase-state proof remain unresolved. (mukherjee2011frictionstirprocessing pages 5-6, mukherjee2011frictionstirprocessing pages 2-5, mukherjee2011frictionstirprocessing pages 6-6)

**4. Liu, Z. et al., “Investigation on mechanical properties and corrosion behavior of laser powder bed fusion 70/30 copper-nickel alloy,” *Corrosion Science* 232 (2024), 112040. DOI: 10.1016/j.corsci.2024.112040.** **Process:** LPBF 70/30 Cu–Ni. The DOI and article identification are corroborated in a subsequent CuNi30–Cr article, **but Liu’s full text was unobtainable in this search**. Accordingly, its powder chemistry/size/flow/oxygen, density, tensile data, core–interdendrite EDS, cooling rate, solution/exposure conditions, film analyses, and corrosion numbers **cannot be responsibly supplied here**. **[CITE] [NOVELTY-RISK]** Prior as-printed LPBF 70/30 mechanical-and-corrosion study. **[GAP]** Whether it quantitatively resolves the proposed segregation–film relationship remains unverified, not disproven. (shiyang2025effectofcr pages 9-10)

**5. Nadimi, M., Song, J., Cheng, L., and Fu, Y., “Corrosion evaluation and microstructural characteristics of 70/30 copper-nickel alloy fabricated by laser powder bed fusion,” *Journal of Alloys and Metallurgical Systems* (2025). DOI: 10.1016/j.jalmes.2025.100155.** **Process:** LPBF 70/30 Cu–Ni. Its bibliographic record was found, but **the article text was unobtainable**; test electrolyte, duration, porosity, segregation, film composition, electrochemistry, and strength therefore remain **unverified**. It must be evaluated before claiming LPBF 70/30 corrosion or microstructure to be novel. **[CITE] [NOVELTY-RISK] [GAP]** Do not infer its results from Song’s different WAAM process. (song2024microstructuresandcorrosion pages 14-17)

**6. Gao, S., He, X., Zhang, M., Chen, H., Zhou, S., Wang, Y., and Ding, J., “Effect of Cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting,” *Powder Metallurgy Technology* 43 (2025), 444–452. DOI: 10.19591/j.cnki.cn11-1974/tf.2025030025.** **Process:** LPBF/SLM, **not DED**; gas-atomized CuNi30 base powder (**Cu–30.450Ni–0.590Fe–0.470Mn–0.130Si–0.009C wt%**, **15–53 µm**) was mechanically mixed/alloyed with **0, 1, 2, or 3 wt% elemental Cr powder**—**not a newly atomized, single-stream pre-alloyed powder**. **Test:** static **3.5 wt% NaCl at 25 °C**, ≥30 min OCP, then polarization at **0.5 mV/s**; no reported 30-day flowing-seawater validation. Optimized baseline density was **98.44%** at **400 W, 900 mm/s, 70 µm hatch**. Across 0→3% Cr, **HV0.2 increased 126→157**, *E*₍corr₎ shifted **−0.238→−0.210 V versus SCE**, and *i*₍corr₎ fell **1.38 × 10⁻⁶→7.72 × 10⁻⁷ A/cm²**. Higher Cr also produced Cr-rich regions/precipitates; a claimed protective Cr-rich film is inferred from electrochemistry and morphology rather than demonstrated as a 30-day marine service film. The authors cite a **generic** LPBF cooling range of 10³–10⁶ K/s, **not paired specimen-specific cooling and Ni/Fe/Mn EDS measurements**. **[CITE] [NUMBERS] [NOVELTY-RISK]** CuNi30–Cr corrosion optimization has already been explored. **[GAP]** Pre-alloyed powder, blown-powder DED, repair, and long-term corrosion are not established by this work. (shiyang2025effectofcr pages 1-4, shiyang2025effectofcr pages 4-7, shiyang2025effectofcr pages 9-10, shiyang2025effectofcr pages 7-9)

**7. Lewis, R. O., and LaQue, F., *Evaluation of Copper-Nickel Alloys for OTEC Applications*, technical report (1981). DOI: 10.2172/6255887.** **Process:** conventional **wrought/service tubing**, with compiled cast/modified-alloy comparisons; **not AM**. Commercial **C71500 ≈Cu–30Ni–0.4–0.7Fe** and **C70600 ≈Cu–10Ni–1.0–1.8Fe wt%** provide appropriate wrought baselines. In reported natural-seawater exposures, C71500 general-corrosion ranges were **0.3–0.5 mil/year in quiet water** and **0.5–0.7 mil/year at 2 ft/s**; long-term rates for both Cu–Ni grades fell below **2.5 µm/year after 14–16 years** in quiet/low-velocity water. These are **service/exposure-dependent benchmarks, not acceptance limits transferable to a 3 h NaCl scan**. The review also reports that 70/30 Cu–Ni with approximately **2.8% Cr (C71900)** resists high-velocity impingement but showed **two- to threefold greater localized-attack susceptibility** than C71500 in some quiet/low-flow comparisons. **[CITE] [NUMBERS] [NAVY]** Marine tubing relevance. **[GAP]** Classical corrosion evidence does not supply AM segregation maps. (lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 43-48)

**8. Sparrow, A., Smith, W., and Ansell, T. Y., “LPBF Parameter Optimization of Mechanical, Non-Thermal Generated C71500 Powder,” *Metals* 16 (2026), 10; published December 2025. DOI: 10.3390/met16010010.** **Process:** LPBF of mechanically generated **pre-existing C71500 bar-stock powder**, not blown-powder DED or ultrasonically atomized powder. **Powder:** **D10/D50/D90 = 24/44/77 µm**; apparent density **3.12 g/cm³**, tap density **4.26 g/cm³**; flow was reported as GranuDrum cohesive indices **15/15/18 at 2/10/20 rpm, not Hall flow**. Powder EDS indicated approximately **5 wt% oxygen**, which the authors explicitly considered inadequate to quantify oxygen pickup; **do not use this as a trustworthy bulk-oxygen specification**. Optimized prints exceeded **99.8% relative density**, reached **165–175 HV0.2**, and averaged **384.7 MPa UTS, 317.2 MPa yield, 31.1% elongation** across reported tensile specimens. **No seawater corrosion or segregation-versus-cooling-rate results. [NUMBERS] [NAVY]** Naval Postgraduate School study. **[NOVELTY-RISK]** Pre-alloyed C71500 powder/ML-guided LPBF processing already exist, but neither composition-network optimization nor DED corrosion qualification is shown. (sparrow2025lpbfparameteroptimization pages 1-3, sparrow2025lpbfparameteroptimization pages 8-11, sparrow2025lpbfparameteroptimization pages 11-12)

## Film mechanism, cooling rate, and predictive limits

The protective marine product is principally **Cu₂O**, with Ni and Fe modifying its composition/defect transport; bulky copper hydroxychlorides can form an additional, less-protective outer product. In **six-month flowing-seawater** data compiled by Lewis and LaQue, an approximately **Cu–11.6Ni–1.05Fe** alloy containing only **0.08 wt% precipitated Fe** formed a film reported as **27 wt% Ni and 15 wt% Fe**, whereas an approximately **Cu–11.3Ni–1.99Fe** alloy with **1.84 wt% precipitated Fe** formed a film with **20 wt% Ni and 4.3 wt% Fe**. This supports the importance of **available Fe in solid solution** for Ni/Fe enrichment, but the alloy Fe contents also differ, so it is not a controlled proof that precipitation alone caused the change. The review finds the best impingement behavior with solutionized Fe, **not** that all precipitated Fe is harmful: a 90/10 alloy with >90% Fe precipitated could still perform favorably. Its qualitative Fe optimum is around **0.5 wt% for 70/30** and **1.5 wt% for 90/10**; in reported 70/30 tests, **>2 wt% Fe increased crevice attack** and **>4 wt% promoted pitting/film blistering**. Mn’s measured enrichment in weld interdendrites is clear; its *independent* effect on seawater-film chemistry and local attack was **not isolated** by these datasets. (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 14-17, devletian2006fluxcoredarc pages 7-10, lewis1981evaluationofcoppernickel pages 43-48)

**Can Scheil predict the contrast?** In principle, a composition-specific CALPHAD/Scheil calculation can predict the **direction and limiting range of solidification partitioning**; the measured weld profiles provide a stringent sign check (**Ni and Fe core-enriched; Mn last-liquid-enriched**). Scheil’s no-solid-diffusion assumption, however, does not uniquely produce an EDS spot contrast: that requires specifying the sampled solid fraction, interaction volume, spatial position, dilution, and subsequent remelting/thermal cycling. Finite-solid-diffusion/back-diffusion calculations require diffusion mobility, dendrite length scale, and a defensible local temperature–time history; rapid-interface solute trapping may matter for LPBF. **None of the accessible Cu–Ni studies here validates equilibrium versus Scheil versus back-diffusion predictions against a matched, measured cooling-rate series of Ni–Fe–Mn EPMA profiles. Nor does any validate a direct Scheil-to-*i*₍corr₎ or attack-depth prediction.** Corrosion additionally depends on Fe phase state, evolving film, defects, exposed orientation, electrolyte and flow; Song’s locally attacked yet globally competitive WAAM specimens and Mukherjee’s homogenized yet faster-corroding FSP material illustrate why a segregation number alone cannot rank service performance. (song2024microstructuresandcorrosion pages 13-14, mukherjee2011frictionstirprocessing pages 5-6, devletian2006fluxcoredarc pages 7-10, lewis1981evaluationofcoppernickel pages 17-19, song2024microstructuresandcorrosion pages 14-17)

**Scope of the remaining gap.** The accessible evidence supplies **no defensible cast-to-weld-to-WAAM-to-LPBF cooling-rate-versus-core/interdendrite regression**, no verified Liu/Nadimi numerical results, and no demonstration that an **as-deposited single-stream pre-alloyed blown-powder laser DED** composition simultaneously meets wrought C71500 in a matched long-duration seawater test **and** forms sound repairs on both cast NAB and wrought Cu–Ni. Those are research objectives, not literature-established outcomes. (song2024microstructuresandcorrosion pages 13-14, mukherjee2011frictionstirprocessing pages 1-2, shiyang2025effectofcr pages 1-4, devletian2006fluxcoredarc pages 7-10)

## Top 5 things the PI should know

1. **Do not frame Ni-rich-core/Ni-poor-interdendrite segregation as new:** weld EPMA measures **38.0 versus 16.4 wt% Ni**, and ONR-funded WAAM already demonstrates preferential interdendritic attack. Frame the missing advance as **measured, controllable partitioning linked to film and long-duration performance**. (song2024microstructuresandcorrosion pages 13-14, devletian2006fluxcoredarc pages 7-10)
2. **Separate local susceptibility from bulk ranking:** Song’s WAAM can beat wrought in short NaCl electrochemistry while attacking preferentially between dendrites; test attack depth and film chemistry as well as *i*₍corr₎ and EIS. (song2024microstructuresandcorrosion pages 13-14, song2024microstructuresandcorrosion pages 10-13)
3. **Measure Fe’s state, not just nominal Fe:** dissolved Fe benefits protective-film enrichment; precipitation changes that benefit, while excessive Fe can increase localized attack. Mn’s independent corrosion role remains unmeasured in the cited segregation profiles. (lewis1981evaluationofcoppernickel pages 17-19, devletian2006fluxcoredarc pages 7-10, lewis1981evaluationofcoppernickel pages 43-48)
4. **Treat physics as a testable intermediate model, not a corrosion oracle:** compare measured core/interdendrite Ni–Fe–Mn and precipitates with equilibrium, Scheil, and thermal-history/back-diffusion calculations **before** testing whether those predictions improve corrosion forecasts. (devletian2006fluxcoredarc pages 7-10, lewis1981evaluationofcoppernickel pages 17-19)
5. **State the novelty boundary precisely:** laser DMD repair on Cu–Ni, 30-day ASTM D1141 immersion, LPBF CuNi30–Cr alloying, and Navy LPBF C71500 powders have precedents. The defensible distinction is **new pre-alloyed powder compositions delivered as one blown-powder laser-DED stream, dual-substrate repair, as-deposited long-duration seawater qualification, and a validated cost-aware linked-model search**; Liu 2024 and Nadimi 2025 still need primary-text verification before stronger comparative claims. (mukherjee2011frictionstirprocessing pages 1-2, shiyang2025effectofcr pages 1-4, sparrow2025lpbfparameteroptimization pages 1-3, song2024microstructuresandcorrosion pages 14-17)

References

1. (song2024microstructuresandcorrosion pages 13-14): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

2. (devletian2006fluxcoredarc pages 7-10): JH Devletian, MJ Sullivan, and CW Engineer. Flux cored arc welding of cuni 90/10 piping with cuni 70/30 filler metal. Unknown journal, 2006.

3. (song2024microstructuresandcorrosion pages 14-17): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

4. (mukherjee2011frictionstirprocessing pages 1-2): S. Mukherjee and Amit K. Ghosh. Friction stir processing of direct metal deposited copper–nickel 70/30. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 528:3289-3294, Apr 2011. URL: https://doi.org/10.1016/j.msea.2011.01.063, doi:10.1016/j.msea.2011.01.063. This article has 38 citations.

5. (mukherjee2011frictionstirprocessing pages 5-6): S. Mukherjee and Amit K. Ghosh. Friction stir processing of direct metal deposited copper–nickel 70/30. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 528:3289-3294, Apr 2011. URL: https://doi.org/10.1016/j.msea.2011.01.063, doi:10.1016/j.msea.2011.01.063. This article has 38 citations.

6. (song2024microstructuresandcorrosion pages 2-5): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

7. (shiyang2025effectofcr pages 1-4): GAO Shiyang, HE Xing, Z Mina, and C Haida. Effect of cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting. Unknown journal, 2025. URL: https://doi.org/10.19591/j.cnki.cn11-1974/tf.2025030025, doi:10.19591/j.cnki.cn11-1974/tf.2025030025.

8. (shiyang2025effectofcr pages 4-7): GAO Shiyang, HE Xing, Z Mina, and C Haida. Effect of cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting. Unknown journal, 2025. URL: https://doi.org/10.19591/j.cnki.cn11-1974/tf.2025030025, doi:10.19591/j.cnki.cn11-1974/tf.2025030025.

9. (shiyang2025effectofcr pages 7-9): GAO Shiyang, HE Xing, Z Mina, and C Haida. Effect of cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting. Unknown journal, 2025. URL: https://doi.org/10.19591/j.cnki.cn11-1974/tf.2025030025, doi:10.19591/j.cnki.cn11-1974/tf.2025030025.

10. (song2024microstructuresandcorrosion pages 1-2): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

11. (song2024microstructuresandcorrosion pages 10-13): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

12. (devletian2006fluxcoredarc pages 43-48): JH Devletian, MJ Sullivan, and CW Engineer. Flux cored arc welding of cuni 90/10 piping with cuni 70/30 filler metal. Unknown journal, 2006.

13. (devletian2006fluxcoredarc pages 1-4): JH Devletian, MJ Sullivan, and CW Engineer. Flux cored arc welding of cuni 90/10 piping with cuni 70/30 filler metal. Unknown journal, 2006.

14. (devletian2006fluxcoredarc pages 30-37): JH Devletian, MJ Sullivan, and CW Engineer. Flux cored arc welding of cuni 90/10 piping with cuni 70/30 filler metal. Unknown journal, 2006.

15. (devletian2006fluxcoredarc pages 37-43): JH Devletian, MJ Sullivan, and CW Engineer. Flux cored arc welding of cuni 90/10 piping with cuni 70/30 filler metal. Unknown journal, 2006.

16. (mukherjee2011frictionstirprocessing pages 2-5): S. Mukherjee and Amit K. Ghosh. Friction stir processing of direct metal deposited copper–nickel 70/30. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 528:3289-3294, Apr 2011. URL: https://doi.org/10.1016/j.msea.2011.01.063, doi:10.1016/j.msea.2011.01.063. This article has 38 citations.

17. (mukherjee2011frictionstirprocessing pages 6-6): S. Mukherjee and Amit K. Ghosh. Friction stir processing of direct metal deposited copper–nickel 70/30. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 528:3289-3294, Apr 2011. URL: https://doi.org/10.1016/j.msea.2011.01.063, doi:10.1016/j.msea.2011.01.063. This article has 38 citations.

18. (shiyang2025effectofcr pages 9-10): GAO Shiyang, HE Xing, Z Mina, and C Haida. Effect of cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting. Unknown journal, 2025. URL: https://doi.org/10.19591/j.cnki.cn11-1974/tf.2025030025, doi:10.19591/j.cnki.cn11-1974/tf.2025030025.

19. (lewis1981evaluationofcoppernickel pages 14-17): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

20. (lewis1981evaluationofcoppernickel pages 17-19): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

21. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

22. (sparrow2025lpbfparameteroptimization pages 1-3): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

23. (sparrow2025lpbfparameteroptimization pages 8-11): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

24. (sparrow2025lpbfparameteroptimization pages 11-12): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.
