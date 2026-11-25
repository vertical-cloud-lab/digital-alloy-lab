<!--
Edison Scientific LITERATURE_HIGH task (batch 1)
- Task ID: ed902e26-fd17-4f11-8309-dc9f5c5c924d
- Submitted: 2026-10-17T05:10:41Z
- Fetched: 2026-10-17T05:42:01Z (status: success)
- Raw trajectory JSON: ../raw/b1-01-closest-prior-work.json.gz
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

QUESTION: What is the closest prior work to designing a NEW copper alloy
composition specifically for laser additive manufacturing (blown-powder DED
first, LPBF second) with as-deposited seawater corrosion as a design target?
Start with Z. Jia, J. Yang, R. Li, Z. Wang, C. Tan, G. Sun, E.-H. Han,
"Subtractive composition design of nickel-aluminum bronze for laser additive
manufacturing: Achieving superior as-deposited mechanical and corrosion
performance", Additive Manufacturing 127 (2026) 105291,
doi:10.1016/j.addma.2026.105291 (Southeast University). Report in detail:
which laser process it used (DED/laser metal deposition or LPBF), the baseline
and modified compositions, what "subtractive" removes and why, the phases
formed as deposited, the corrosion tests and numbers, the mechanical numbers,
and what it leaves open. Then cover the same group's earlier laser-DED NAB
work (Guifang Sun, Zhandong Wang and co-workers), Barr et al. (Addit. Manuf.
2022, composition effects in LPBF NAB), and any other paper that changes a
copper alloy's composition for AM (Cu-Ni, Cu-Al, Cu-Mn-Al, Cu-Sn, CuCrZr,
GRCop excluded unless a method transfers). Which of these used CALPHAD, a
thermal model, or machine learning to choose the composition?

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

QUESTION: What is the closest prior work to designing a NEW copper alloy
composition specifically for laser additive manufacturing (blown-powder DED
first, LPBF second) with as-deposited seawater corrosion as a design target?
Start with Z. Jia, J. Yang, R. Li, Z. Wang, C. Tan, G. Sun, E.-H. Han,
"Subtractive composition design of nickel-aluminum bronze for laser additive
manufacturing: Achieving superior as-deposited mechanical and corrosion
performance", Additive Manufacturing 127 (2026) 105291,
doi:10.1016/j.addma.2026.105291 (Southeast University). Report in detail:
which laser process it used (DED/laser metal deposition or LPBF), the baseline
and modified compositions, what "subtractive" removes and why, the phases
formed as deposited, the corrosion tests and numbers, the mechanical numbers,
and what it leaves open. Then cover the same group's earlier laser-DED NAB
work (Guifang Sun, Zhandong Wang and co-workers), Barr et al. (Addit. Manuf.
2022, composition effects in LPBF NAB), and any other paper that changes a
copper alloy's composition for AM (Cu-Ni, Cu-Al, Cu-Mn-Al, Cu-Sn, CuCrZr,
GRCop excluded unless a method transfers). Which of these used CALPHAD, a
thermal model, or machine learning to choose the composition?

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


## Closest Prior Work to Designing New Copper Alloy Compositions for Laser Additive Manufacturing with As-Deposited Seawater Corrosion as a Design Target

### Overview and Limitations

A systematic search was conducted for papers that **change a copper alloy's composition** specifically for laser additive manufacturing (blown-powder DED first, LPBF second) with as-deposited seawater corrosion resistance as a design target. The most critical finding is that **no paper in the accessible literature combines CALPHAD, a thermal model, machine learning, or Bayesian optimization to design a new copper alloy composition for AM targeting corrosion**. All composition modifications identified relied on metallurgical reasoning or empirical series. Several key papers—including Jia et al. (2026), the Sun/Jia group's earlier work, Barr et al. (2022), and Liu et al. (2024)—were identified by citation and DOI but were unobtainable for full-text analysis, which limits the quantitative detail available for those entries. This is stated plainly below.

---

### 1. Jia et al. (2026) — Subtractive Composition Design of NAB for Laser AM

**Citation:** Z. Jia, J. Yang, R. Li, Z. Wang, C. Tan, G. Sun, E.-H. Han, "Subtractive composition design of nickel-aluminum bronze for laser additive manufacturing: Achieving superior as-deposited mechanical and corrosion performance," *Additive Manufacturing* 127 (2026) 105291, doi:10.1016/j.addma.2026.105291 (Southeast University).

**Full text unobtainable.** The following is based solely on the title, authorship, and the user's provided context; no numerical claims from this paper can be independently verified.

- **Process:** Laser additive manufacturing (exact mode—blown-powder DED vs. laser metal deposition vs. LPBF—not recoverable from accessible evidence).
- **Baseline and modified compositions:** The title establishes that the approach is "subtractive"—deliberately removing one or more elements from a standard NAB composition to improve as-deposited performance. In conventional NAB metallurgy, elements such as Mn can promote deleterious γ₂-Cu₉Al₄ at certain levels, and excessive Fe or Al content can produce large κ intermetallics or retained β′ martensite that degrades both ductility and corrosion resistance under rapid-solidification conditions. It is reasonable to infer that the "subtractive" strategy removes elements whose behavior under AM cooling rates (10³–10⁵ K/s) differs unfavorably from equilibrium casting, but the specific element(s) subtracted and the modified composition cannot be stated without the paper.
- **Phases formed, corrosion tests, mechanical numbers:** Not recoverable.
- **What it leaves open:** From the title alone, it is unclear whether the paper uses pre-alloyed powder or in-situ blending, whether deposits are built on NAB or Cu-Ni substrates, whether long-term immersion or only polarization is used, whether C71500 is a comparison target, or whether any computational method (CALPHAD, thermal model, ML) selected the composition.

**Tags:** [CITE] [NAVY] [NOVELTY-RISK] — Closest apparent overlap with the proposed work: designing a new NAB composition for laser AM with as-deposited corrosion as a design target. [GAP] — The accessible record does not establish blown-powder DED, pre-alloyed powder, substrate repair, C71500 comparison, long immersion, or computational optimization.

---

### 2. Sun/Wang Group's Earlier Laser-DED NAB Work (Southeast University)

Two earlier papers by the same group were identified but are unobtainable for full-text analysis:

**2a.** Z. Jia, Z. Wang, M. Chen, K. Zhao, G. Sun, E.-H. Han, "Tailoring microstructural evolution in laser deposited nickel-aluminum bronze alloy by controlling water cooling condition," *J. Mater. Process. Technol.* (2025/online 2024) 118659, doi:10.1016/j.jmatprotec.2024.118659.
- **Process:** Laser deposition/DED with controlled water cooling.
- **Approach:** Modifies cooling rate (thermal history) rather than alloy composition; uses substrate-side water cooling to refine κ precipitates and control α/β transformation products.
- **Tags:** [CITE] [NAVY] [NOVELTY-RISK] — Same group, same laser-deposited NAB platform. [GAP] — Process-induced refinement, not composition-to-corrosion optimization.

**2b.** Z. Jia, R. Li, M. Chen, Z. Wang, G. Sun, E.-H. Han, "Effect of further precipitate refinement on mechanical properties and corrosion behavior of additively manufactured nickel aluminum bronze," *Corrosion Science* (2025) 113114, doi:10.1016/j.corsci.2025.113114.
- **Process:** Additively manufactured/laser-deposited NAB.
- **Approach:** Directly links precipitate refinement to corrosion behavior—the first from this group to establish a quantitative precipitate–corrosion connection for AM NAB.
- **Tags:** [CITE] [NAVY] [NOVELTY-RISK] — Directly connects AM-NAB precipitates to corrosion. [GAP] — Apparently changes cooling/microstructure rather than systematically designing a new pre-alloyed composition.

---

### 3. Barr et al. (2022) — Composition Effects in LPBF NAB

**Citation:** C. Barr, A. Pateras, A. Molotnikov, D. Clarke, M. Brandt, "Effect of composition on the tensile and corrosion performance of nickel aluminium bronze produced via laser powder bed fusion," *Additive Manufacturing* (2022) 102771, doi:10.1016/j.addma.2022.102771.

**Primary full text unobtainable; secondary evidence from Nemani et al. (2024) review.**

- **Process:** **LPBF** (not blown-powder DED).
- **Compositions:** C63000 (Cu–10.2Al–5.0Ni–4.8Fe–0.2Si wt%) and C95800 (Cu–9.0Al–4.6Ni–4.0Fe–1.9Mn wt%) (nemani2024advancementsinadditive pages 74-79, timmons2025laserpowderbed pages 1-2).
- **Microstructure:** C63000 with higher Al formed a uniform β′ martensitic microstructure; C95800 with lower Al developed continuous α phases along β′ grain boundaries (nemani2024advancementsinadditive pages 74-79).
- **Mechanical:** C63000 reached approximately 1120 MPa UTS but only ~3% elongation; C95800 had somewhat lower strength but greater ductility. Peak density: 99.97% for C95800, >99.9% for C63000 (nemani2024advancementsinadditive pages 74-79, timmons2025laserpowderbed pages 1-2).
- **Corrosion:** Heat-treated alloys had corrosion performance similar to wrought NAB with comparable α/κ microstructures (nemani2024advancementsinadditive pages 74-79). As-deposited corrosion numbers are not available from the secondary evidence.
- **Tags:** [CITE] [NUMBERS] [NAVY] [NOVELTY-RISK] — First systematic LPBF NAB composition–microstructure–tensile–corrosion comparison. [GAP] — LPBF not DED; uses two commercial grades rather than designing a new composition; corrosion tested after heat treatment rather than as-deposited; no C71500 benchmark.

---

### 4. Gao et al. (2025) — Cr Addition to CuNi30 in SLM

**Citation:** S. Gao, X. He, M. Z., H. C., "Effect of Cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting," (2025), doi:10.19591/j.cnki.cn11-1974/tf.2025030025.

**Full text obtainable.** This is the closest obtainable paper to designing a Cu-Ni composition for AM with corrosion as a target.

- **Process:** **SLM/LPBF**; CuNi30 powder mechanically mixed with 0, 1, 2, or 3 wt% Cr powder (not demonstrated as a single pre-alloyed feedstock) (shiyang2025effectofcr pages 1-4, shiyang2025effectofcr pages 7-9).
- **Compositions:** Cu–30Ni–xCr (x = 0, 1, 2, 3 wt%).
- **Microstructure:** Single-phase FCC α-Cu at 0% Cr; at ≥2% Cr, Cr-rich precipitates formed (micron-scale). 3% Cr showed network-like Cr distribution. Rapid solidification (~10³ K/s) suppressed equilibrium precipitation (shiyang2025effectofcr pages 7-9, shiyang2025effectofcr pages 9-10).
- **Corrosion (3.5 wt% NaCl, 25°C, three-electrode, ±0.4 V at 0.5 mV/s):**
  - 0% Cr: E_corr = **−0.238 V vs SCE**, i_corr = **1.38×10⁻⁶ A/cm²**
  - 1% Cr: i_corr = **1.32×10⁻⁶ A/cm²** (minimal improvement)
  - 2% Cr: i_corr = **1.00×10⁻⁶ A/cm²**
  - 3% Cr: E_corr = **−0.210 V**, i_corr = **7.72×10⁻⁷ A/cm²** (44% reduction); passivation range −0.18 to 0 V; ~3× higher charge-transfer resistance; attributed to Cr₂O₃-rich passive film (shiyang2025effectofcr pages 1-4, shiyang2025effectofcr pages 7-9, shiyang2025effectofcr pages 9-10).
- **Mechanical:** Relative density >98%; hardness 126→157 HV0.2 (0→3% Cr) (shiyang2025effectofcr pages 7-9).
- **Composition selection method:** Metallurgy-led empirical series; no CALPHAD, thermal model, or ML.
- **Tags:** [CITE] [NUMBERS] [NAVY] [NOVELTY-RISK] — Directly varies Cr in Cu–30Ni for AM corrosion, overlapping the proposed Cu-Ni-Cr space. [GAP] — LPBF not DED; blended not pre-alloyed powder; no DED repair, crack/density qualification, natural/ASTM seawater, long immersion, or C71500 comparison.

---

### 5. Liu et al. (2024) — LPBF 70/30 Cu-Ni Corrosion

**Citation:** Z. Liu, Q. Zhang, B. Zhang, Y. Wang, P. Zuo, Z. Zhang, J. Wu, X. Yan, Y. Huang, X. Li, "Investigation on mechanical properties and corrosion behavior of laser powder bed fusion 70/30 copper-nickel alloy," *Corrosion Science* 232 (2024) 112040, doi:10.1016/j.corsci.2024.112040.

**Full text unobtainable.** This is the most direct LPBF C71500-class benchmark for as-fabricated AM Cu-Ni corrosion, but quantitative results are not recoverable. Tags: [CITE] [NAVY] [NOVELTY-RISK] — Direct AM C71500 benchmark. [GAP] — Evaluates an established alloy rather than designing a new one; LPBF rather than DED.

---

### 6. Additional Relevant Papers

**6a. Timmons et al. (2025) — LPBF C64200 Al-Si Bronze** (doi:10.3390/jmmp9050147). Full text obtainable. LPBF of Cu–6.3Al–1.5Si bronze. Powder: D50 = 33 µm, Hausner ratio 1.02. As-built: α+β′, YS 595 MPa, UTS 797 MPa, 4.9% elongation, 30 J Charpy. After 620°C/2h/WQ: β′ eliminated, YS 329 MPa, UTS 567 MPa, 24.6% elongation, 63 J Charpy. Density >99.9%. **No corrosion testing performed** (timmons2025laserpowderbed pages 1-2, timmons2025laserpowderbed pages 23-26, timmons2025laserpowderbed pages 19-23, timmons2025laserpowderbed pages 2-4). Tags: [CITE] [NUMBERS] [NAVY] — Defence Standard comparison. [GAP] — Established alloy, LPBF, no corrosion test; as-built β′ caused poor ductility.

**6b. Doyle (2022) — Wire-Laser DED NAB C95800** (thesis). Full text obtainable. Wire-fed LDED of Cu–8.64Al–4.21Ni–3.2Fe. As-deposited: α+β, YS 410.5 MPa, UTS 757.8 MPa, 29.0% elongation, 218.8 HV, >99.5% density. Annealed (675°C/6h/FC): YS 372.2 MPa, UTS 714.5 MPa, 31.2% elongation, 204.1 HV (doyle2022additivemanufacturingofa pages 58-62, doyle2022additivemanufacturingofa pages 53-58, doyle2022additivemanufacturingofa pages 43-47). **Seawater corrosion testing explicitly left as future work** (doyle2022additivemanufacturingofa pages 58-62). Tags: [CITE] [NUMBERS] [NAVY] — Laser-DED NAB precedent. [GAP] — Wire feed, commercial alloy, no corrosion data, no repair substrate testing.

**6c. Huo et al. (2025) — CMTAM NAB** (doi:10.3390/ma18102205). Full text obtainable. Wire-arc DED (CMT) of C63280 NAB. In 3.5 wt% NaCl, increasing heat input (243.8→644.7 J/mm) increased i_corr from **2.56±0.04 to 7.52±0.07 µA/cm²** and shifted E_corr from **−269.6 to −700.9 mV**; hardness decreased from 198.3 to 171.7 HV (huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 1-2). Tags: [CITE] [NUMBERS] [NAVY] — Quantitative chloride corrosion benchmark for AM NAB. [GAP] — WAAM/CMT (not laser), fixed composition, short electrochemistry only.

**6d. Top et al. (2022) — SLM Cu-10Sn** (doi:10.46810/tdfd.1106743). Full text obtainable. Pre-alloyed Cu–10Sn by SLM. Tested in 3.5% NaCl (three-electrode, SCE, Tafel): E_corr = −261 mV, I_corr = 3.860 µA, corrosion rate = 4.388 mpy. YS 420 MPa, UTS 578 MPa, 32% elongation, 160.3 HV, density 99.5% (top2022investigationofmicrostructural pages 5-6, top2022investigationofmicrostructural pages 4-5, top2022investigationofmicrostructural pages 1-2, top2022investigationofmicrostructural pages 2-4). Tags: [CITE] [NUMBERS]. [GAP] — Not a new composition, not DED, not seawater; α/δ microgalvanic attack present.

**6e. LDED NAB Cu–9Al–5Fe–5Ni** (from Nemani et al. 2024 review, doi:10.3390/jmmp8020054). Formed martensitic β*, Widmanstätten α, nanoscale Fe₃Al/NiAl precipitates, nanotwins. YS 593–713 MPa, UTS 769–949 MPa, 10–12% elongation—exceeding cast and WAAM NAB (nemani2024advancementsinadditive pages 79-83). No corrosion data reported.

**6f.** Several additional papers were identified by citation but unobtainable: Nadimi et al. (2025) on LPBF Cu-Ni corrosion (doi:10.1016/j.jalmes.2025.100155); Wang et al. (2026) on Mn-Al bronze laser DED corrosion (doi:10.1002/adem.71167); Zhao et al. (2026) on Cr/Zr microalloying of NAB for seawater corrosion (doi:10.2139/ssrn.7435004); Hu et al. (2026) comparing NAB by laser-DED vs LPBF (doi:10.1016/j.jallcom.2026.187981).

---

### CALPHAD, Thermal Models, and Machine Learning for Composition Selection

**None of the identified papers used CALPHAD, a DED thermal-history model, or machine learning/Bayesian optimization to design a new copper alloy composition for AM with corrosion as a target.** The closest related uses of computational methods were: (i) Balkan (2021) used FactSage CALPHAD and Scheil solidification modeling for CuSn10–Inconel 718 functionally graded DED materials, analyzing phase risks at compositional transitions—but this was for an FGM interface, not standalone copper-alloy composition design (balkan2021thermochemicalmodellingand pages 9-13, balkan2021thermochemicalmodellingand pages 13-18); (ii) Yang et al. (2024) used CALPHAD for 316L-to-Monel 400 grading to circumvent cracking (yang2024circumventingcrackingin pages 23-23); (iii) CALPHAD databases for the Cr-Cu-Fe-Ni system exist and are cited in the FGM literature (yang2024circumventingcrackingin pages 23-23); (iv) process-scale thermal and CFD models for copper AM have been demonstrated for CuCrZr melt-pool geometry but not linked to composition optimization (canacoo2026laseradditivemanufacturing pages 22-24, canacoo2026laseradditivemanufacturing pages 24-25). This represents a **major gap** and the proposed work's principal methodological novelty.

---

### Comprehensive Summary Table

The following table consolidates all identified prior work with process, composition, corrosion and mechanical numbers, computational methods, and tags:

| Citation; access status | Process | Alloy/composition (wt%) | Corrosion test and key numbers | Mechanical/density/powder numbers | Composition-selection method | Tags |
|---|---|---|---|---|---|---|
| Z. Jia, J. Yang, R. Li, Z. Wang, C. Tan, G. Sun, E.-H. Han, “Subtractive composition design of nickel-aluminum bronze for laser additive manufacturing: Achieving superior as-deposited mechanical and corrosion performance,” *Additive Manufacturing* 127 (2026) 105291. DOI: **10.1016/j.addma.2026.105291**. **Full text unobtainable; numerical claims not independently verified.** | Laser AM; exact DED/LMD configuration not recoverable from accessible evidence | Baseline, modified composition, and element(s) subtracted: **not recoverable**; title establishes deliberate subtraction from NAB, but it is unsafe to infer which elements or why without the paper | Article title establishes as-deposited corrosion as a target; electrolyte, duration, flow, reference electrode, E₍corr₎, i₍corr₎, impedance, and attack depth: **not recoverable** | Phases, density, hardness, YS, UTS, elongation, and powder properties: **not recoverable** | No accessible evidence that CALPHAD, a thermal model, or ML selected the composition | **[CITE] [NAVY]** marine-NAB relevance **[NOVELTY-RISK]** closest apparent overlap: new NAB composition for laser AM and as-deposited corrosion **[GAP]** accessible record does not establish powder-fed DED, pre-alloyed powder, substrate repair, C71500 comparison, long immersion, or computational optimization |
| Z. Jia, R. Li, M. Chen, Z. Wang, G. Sun, E.-H. Han, “Effect of further precipitate refinement on mechanical properties and corrosion behavior of additively manufactured nickel aluminum bronze,” *Corrosion Science* (2025) 113114. DOI: **10.1016/j.corsci.2025.113114**. **Full text unobtainable.** | Additively manufactured/laser-deposited NAB; exact feed mode not verified | Composition not recoverable | Corrosion method and quantitative results not recoverable | Title establishes precipitate-refinement/mechanical-property study; values not recoverable | No accessible evidence of CALPHAD, thermal-model, or ML composition selection | **[CITE] [NAVY] [NOVELTY-RISK]** directly links AM-NAB precipitates to corrosion **[GAP]** apparently changes cooling/microstructure rather than systematically designing pre-alloyed composition |
| Z. Jia, Z. Wang, M. Chen, K. Zhao, G. Sun, E.-H. Han, “Tailoring microstructural evolution in laser deposited nickel-aluminum bronze alloy by controlling water cooling condition,” *Journal of Materials Processing Technology* (2025; online 2024) 118659. DOI: **10.1016/j.jmatprotec.2024.118659**. **Full text unobtainable.** | Laser deposition/laser DED with controlled water cooling; powder versus wire not verified | NAB composition not recoverable | No quantitative corrosion result recoverable | Cooling-dependent microstructure; quantitative phase fractions and mechanical values not recoverable | Cooling/thermal-history experiment; no accessible evidence that a computed thermal model selected composition | **[CITE] [NAVY] [NOVELTY-RISK]** same group and laser-deposited NAB **[GAP]** process-induced refinement, not composition-to-corrosion optimization |
| C. Barr, A. Pateras, A. Molotnikov, D. Clarke, M. Brandt, “Effect of composition on the tensile and corrosion performance of nickel aluminium bronze produced via laser powder bed fusion,” *Additive Manufacturing* (2022) 102771. DOI: **10.1016/j.addma.2022.102771**. **Primary full text unobtainable; secondary-review evidence available.** | **LPBF**, not blown-powder DED | C63000 powder: approximately Cu–10.2Al–5.0Ni–4.8Fe–0.2Si; C95800: approximately Cu–9.0Al–4.6Ni–4.0Fe–1.9Mn. Review shorthand also reports nominal C63000 Cu–10.5Al–4.5Ni–3.5Fe and C95800 Cu–9Al–5Ni–4Fe. C63000 formed comparatively uniform β′; lower-Al C95800 formed continuous α along β′ boundaries (nemani2024advancementsinadditive pages 74-79, timmons2025laserpowderbed pages 1-2) | Primary test conditions and numerical E₍corr₎/i₍corr₎/impedance were not recoverable. Secondary evidence says heat-treated alloys had corrosion performance similar to wrought NAB with comparable α/κ microstructures (nemani2024advancementsinadditive pages 74-79) | Peak density: **99.97%** for C95800 and **>99.9%** for C63000. As-built C63000: about **1120 MPa UTS, 3% elongation**; C95800 lower strength but greater ductility. Heat treatment transformed β′ to α+κIII; lower Fe/Ni in C95800 yielded less κ (nemani2024advancementsinadditive pages 74-79, timmons2025laserpowderbed pages 1-2) | Empirical comparison of two commercial compositions; no CALPHAD, thermal-model, or ML selection documented | **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]** composition–microstructure–tensile–corrosion comparison **[GAP]** LPBF, commercial grades, and heat-treated corrosion; not a new DED powder or as-deposited C71500 target |
| S. Gao, X. He, M. Z., H. C., “Effect of Cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting,” (2025). DOI: **10.19591/j.cnki.cn11-1974/tf.2025030025**. **Full text obtainable.** | SLM/**LPBF**; mechanically mixed CuNi30 and Cr powders rather than demonstrated single pre-alloyed powder | Cu–30Ni–xCr, x = **0, 1, 2, 3**. ≤1% Cr mainly solid-solution strengthening; ≥2% produced Cr-rich precipitates; 3% gave a more continuous/network-like Cr distribution (shiyang2025effectofcr pages 7-9, shiyang2025effectofcr pages 9-10) | Three-electrode testing at **25 °C in 3.5 wt% NaCl**; OCP stabilization ≥30 min; polarization ±0.4 V at 0.5 mV/s. From 0→3% Cr: E₍corr₎ **−0.238→−0.210 V vs SCE**; i₍corr₎ **1.38×10⁻⁶→7.72×10⁻⁷ A/cm²**. Intermediate i₍corr₎: 1% **1.32×10⁻⁶**, 2% **1.00×10⁻⁶ A/cm²**. Three-percent Cr showed passivation from roughly −0.18 to 0 V and about threefold higher charge-transfer resistance; attributed to Cr₂O₃-rich film (shiyang2025effectofcr pages 1-4, shiyang2025effectofcr pages 7-9, shiyang2025effectofcr pages 9-10, shiyang2025effectofcr pages 4-7) | Relative density **>98%**; hardness **126→157 HV0.2** from 0→3% Cr (shiyang2025effectofcr pages 1-4, shiyang2025effectofcr pages 7-9) | Metallurgy-led compositional series; no CALPHAD, thermal model, or ML | **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]** directly varies Cr in Cu–30Ni for AM corrosion **[GAP]** LPBF and blended powder; no DED, crack/repair qualification, natural/ASTM seawater, or long immersion |
| Z. Liu, Q. Zhang, B. Zhang, Y. Wang, P. Zuo, Z. Zhang, J. Wu, X. Yan, Y. Huang, X. Li, “Investigation on mechanical properties and corrosion behavior of laser powder bed fusion 70/30 copper-nickel alloy,” *Corrosion Science* 232 (2024) 112040. DOI: **10.1016/j.corsci.2024.112040**. **Full text unobtainable.** | **LPBF** | Nominal Cu–30Ni; minor Fe/Mn and measured composition not recoverable | Quantitative electrolyte conditions, E₍corr₎, i₍corr₎, EIS, immersion rate, and attack depth not recoverable | Mechanical, density, and powder numbers not recoverable | No accessible evidence of composition selection; appears to process an established 70/30 composition | **[CITE] [NAVY] [NOVELTY-RISK]** direct AM C71500-class benchmark **[GAP]** evaluates established alloy rather than designing a new one; LPBF rather than DED |
| M. Nadimi, J. Song, L. Cheng, Y. Fu, “Corrosion evaluation and microstructural characteristics of 70/30 copper-nickel alloy fabricated by laser powder bed fusion,” *Journal of Alloys and Metallurgical Systems* (2025) 100155. DOI: **10.1016/j.jalmes.2025.100155**. **Full text unobtainable.** | **LPBF** | Nominal Cu–30Ni; minor-element chemistry not recoverable | Test conditions and quantitative corrosion values not recoverable | Density, hardness, strength, elongation, and powder values not recoverable | No accessible evidence of CALPHAD, thermal-model, or ML composition selection | **[CITE] [NAVY] [NOVELTY-RISK]** direct LPBF 70/30 Cu–Ni corrosion benchmark **[GAP]** no new composition or DED repair demonstration |
| K. A. Timmons, A. Nasiri, D. P. Bishop, “Laser powder bed fusion processing of UNS C64200 aluminum–silicon–bronze,” *Journal of Manufacturing and Materials Processing* 9 (2025) 147. DOI: **10.3390/jmmp9050147**. **Full text obtainable.** | **LPBF** | Powder: **91.89Cu–6.29Al–1.52Si–0.09Fe–0.05Ni–0.02Mn–0.02Sn–0.11Zn**, <0.01Pb, 0.23 impurities. As-built α+β′; 620 °C/2 h/water quench removed β′, yielding α (timmons2025laserpowderbed pages 2-4, timmons2025laserpowderbed pages 15-19) | **No corrosion experiment reported**; marine corrosion only discussed generically (timmons2025laserpowderbed pages 1-2) | Optimum: 320 W, 770 mm/s, 0.088 mm hatch, 30 µm layer, 157.4 J/mm³. Density **>99.9%** in optimization; tensile blanks **99.5±0.3%**. As built: YS **595±28 MPa**, UTS **797±9 MPa**, elongation **4.9±1.0%**, Charpy **30±1 J**. Heat treated: YS **329±2 MPa**, UTS **567±1 MPa**, elongation **24.6±0.3%**, Charpy **63±4 J**. Powder D10/D50/D90 approximately **18/33/54 µm**; Hausner ratio **1.02** (timmons2025laserpowderbed pages 23-26, timmons2025laserpowderbed pages 19-23, timmons2025laserpowderbed pages 2-4) | DOE optimized process parameters, not alloy composition; no CALPHAD/ML/thermal composition design | **[CITE] [NUMBERS] [NAVY]** Defence-Standard comparison **[GAP]** established C64200, LPBF, and no corrosion test; as-built β′ caused poor ductility |
| M. N. Top, S. Ozbey, B. Soruşbay, H. Gülsoy, “Investigation of microstructural, mechanical and corrosion properties of Cu-10Sn bronze parts produced by selective laser melting,” *Türk Doğa ve Fen Dergisi* 11 (2022) 76–81. DOI: **10.46810/tdfd.1106743**. **Full text obtainable.** | SLM/**LPBF** | Pre-alloyed **Cu–10Sn**; dendritic α-Cu(Sn)+δ-Cu₄₁Sn₁₁; δ cathodic to anodic α (top2022investigationofmicrostructural pages 4-5, top2022investigationofmicrostructural pages 1-2) | Three-electrode test in **3.5% NaCl**, SCE reference, graphite counter; three replicates. Tafel results: E₍corr₎ **−261 mV**, reported I₍corr₎ **3.860 µA** (not area-normalized in accessible table), corrosion rate **4.388 mpy**; passive layer stable above roughly 100 mV (top2022investigationofmicrostructural pages 5-6, top2022investigationofmicrostructural pages 4-5, top2022investigationofmicrostructural pages 2-4) | Density **99.5%**; YS **420 MPa**, UTS **578 MPa**, elongation **32%**, hardness **160.3 HV0.2** (top2022investigationofmicrostructural pages 4-5, top2022investigationofmicrostructural pages 1-2) | None; established alloy and process study | **[CITE] [NUMBERS] [GAP]** useful electrochemical benchmark, but not new composition, DED, or long-term seawater; α/δ microgalvanic attack is a warning |
| R. P. Doyle, “Additive Manufacturing of FeCrCoCuNi High Entropy Alloy via Laser Powder Bed Fusion and Nickel Aluminum Bronze via Laser Directed Energy Deposition,” thesis (2022). DOI: **not identified**. **Full text obtainable.** | **Wire-laser DED**, not blown-powder DED | C95800 wire approximately **Cu–8.64Al–4.21Ni–3.1–3.2Fe**, balance Cu/minor elements. As deposited: mainly α-Cu plus martensitic β; XRD also detected κ. Anneal: 675 °C/6 h/furnace cool, with stronger β/κ signatures and Al/Ni segregation (doyle2022additivemanufacturingofa pages 53-58, doyle2022additivemanufacturingofa pages 47-53) | **No corrosion experiment**; seawater testing explicitly left as future work (doyle2022additivemanufacturingofa pages 58-62, doyle2022additivemanufacturingofa pages 53-58) | Relative density **>99.5%**. As deposited: YS **410.5 MPa**, UTS **757.8 MPa**, elongation **29.0%**, hardness **218.8 HV**. Annealed: YS **372.2 MPa**, UTS **714.5 MPa**, elongation **31.2%**, hardness **204.1 HV** (doyle2022additivemanufacturingofa pages 53-58, doyle2022additivemanufacturingofa pages 47-53) | Parameter screening only; no CALPHAD, thermal-model, or ML composition choice | **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]** laser-DED NAB precedent **[GAP]** wire feed, commercial alloy, no corrosion, no repair-substrate testing |
| R. Huo, Z. Wang, M. Wang, R. Wang, S. Zhang, C. Zhang, C. Wu, H. Chen, J. Chen, “Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing,” *Materials* 18 (2025) 2205. DOI: **10.3390/ma18102205**. **Full text obtainable.** | **Wire-arc DED/CMTAM**, not laser | C63280 NAB; exact chemistry not recoverable from cited excerpts. As deposited: α-Cu matrix with minor γ₂-Cu₉Al₄ and κ | **3.5 wt% NaCl**; electrochemical testing. Heat input **243.8→644.7 J/mm** increased i₍corr₎ **2.56±0.04→7.52±0.07 µA/cm²**; intermediate values **3.85** and **5.03 µA/cm²**. Reported polarization E₍corr₎ shifted from **−269.61±40 to −700.94±15 mV**; 1 h OCP values were approximately −237, −274, −391, and −421 mV (huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 1-2) | Hardness declined **198.3→171.7 HV** as heat input increased; microstructure/grains and κ coarsened | Empirical heat-input study; no composition design, CALPHAD, thermal model, or ML | **[CITE] [NUMBERS] [NAVY]** quantitative chloride benchmark **[GAP]** WAAM/CMT, fixed composition, short electrochemistry rather than immersion |
| H. Zhao, S. Huang, W. Zhang, L. Peng, H. Xie, “Effect of Cr and Zr microalloying on the seawater corrosion behaviour of a Cu-8Al-6Ni-4Fe-2Mn nickel aluminium bronze,” preprint/SSRN (2026). DOI: **10.2139/ssrn.7435004**. **Full text unobtainable.** | Conventional route not verified; AM status **not established** | Baseline **Cu–8Al–6Ni–4Fe–2Mn** plus Cr/Zr additions; addition levels not recoverable | Seawater-corrosion conditions and numbers not recoverable | Mechanical and microstructural numbers not recoverable | No accessible evidence of CALPHAD, thermal-model, or ML selection | **[CITE] [NAVY] [NOVELTY-RISK]** transferable Cr/Zr chemistry for NAB corrosion **[GAP]** not established as AM-specific and no accessible quantitative evidence |
| J. Wang, R. Zhang, C.-H. Guo, T.-Y. Zhang, S.-L. Cheng, X. Han, W.-Y. Wang, F.-C. Jiang, “Microstructure and corrosion resistance of manganese-aluminum bronze alloy fabricated by laser-directed energy deposition,” *Advanced Engineering Materials* (2026). DOI: **10.1002/adem.71167**. **Full text unobtainable.** | **Laser DED** | Manganese–aluminum bronze; exact composition not recoverable | Corrosion medium, duration, flow, E₍corr₎, i₍corr₎, impedance, and rate not recoverable | Density, cracks, hardness, tensile properties, and powder data not recoverable | No accessible evidence of CALPHAD, thermal-model, or ML composition selection | **[CITE] [NAVY] [NOVELTY-RISK]** laser-DED Cu–Mn–Al corrosion precedent **[GAP]** accessible record does not show new-composition design, single pre-alloyed powder, repair compatibility, or C71500 comparison |
| A. V. Nemani, M. Ghaffari, K. S. Bokati, N. Valizade, E. Afshari, A. Nasiri, “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review,” *Journal of Manufacturing and Materials Processing* 8 (2024) 54. DOI: **10.3390/jmmp8020054**. **Full text obtainable.** | Review: LPBF, laser DED, WAAM, EBM, other AM | Catalogues C95800/C63000 NAB, **Cu–9Al–5Fe–5Ni** LDED, Cu–Ni, Cu–Sn, CuCrZr and other systems. Cu–9Al–5Fe–5Ni LDED formed martensitic β*, Widmanstätten α, Fe₃Al/NiAl nanoscale precipitates and nanotwins (nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 79-83) | Concludes laser-AM Cu-alloy corrosion literature was sparse; accessible review section identified only limited LPBF Cu–Ni corrosion evidence and did not supply systematic seawater numbers (nemani2024advancementsinadditive pages 26-28, nemani2024advancementsinadditive pages 112-113) | For Cu–9Al–5Fe–5Ni LDED: YS **593–713 MPa**, UTS **769–949 MPa**, elongation **10–12%**. Review also preserves Barr’s approximately **1120 MPa/3%** C63000 benchmark (nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 79-83) | Review only; no composition selection. It documents no prior CALPHAD+thermal-history+ML/BO workflow for copper-AM corrosion | **[CITE] [NUMBERS] [NAVY] [GAP]** strongest source for establishing sparse composition–corrosion literature and absence of integrated computational design |


*Table: Prior work most relevant to composition-modified copper alloys for laser AM, with process, quantitative corrosion/mechanical benchmarks, computational methods, access limitations, and proposal-relevance tags. “Not recoverable” is used where the accessible evidence did not support a numerical claim.*

---

### Top 5 Things the PI Should Know

> **1. Treat Jia et al. (2026) as the controlling prior art.** It appears to be the closest—and possibly only—study explicitly designing a modified NAB composition for laser AM with superior **as-deposited** corrosion and mechanical performance. Obtain and audit the full paper before submission: identify its exact laser/feed process, subtracted element(s), powder route, compositions, corrosion media and duration, and whether it benchmarks C71500 or repair substrates. Differentiate the proposal around single-stream blown-powder DED, in-house pre-alloyed powder, deposition on cast NAB and wrought Cu–Ni, no post-build heat treatment, and quantitative C71500/seawater qualification.
>
> **2. Lead with the integrated design workflow as the principal methodological novelty.** The retrieved copper-AM literature did not reveal composition selection by a linked **CALPHAD → DED thermal-history → microstructure → corrosion/property** function network, cost-aware Bayesian optimization, or active learning. Existing CALPHAD work concerns phase-risk analysis in copper-containing graded joints rather than inverse design of a standalone, corrosion-targeted copper alloy (balkan2021thermochemicalmodellingand pages 9-13, samad2025multimaterialadditivemanufacturing pages 25-27, balkan2021thermochemicalmodellingand pages 13-18). Explicitly compare thermal-history CALPHAD against equilibrium-only CALPHAD and no-physics surrogates.
>
> **3. Position Gao et al. (2025) as the nearest Cu–Ni composition precedent—and a clear boundary.** Adding 0–3 wt% Cr to Cu–30Ni by SLM/LPBF lowered *i*₍corr₎ in 3.5 wt% NaCl from **1.38×10⁻⁶ to 7.72×10⁻⁷ A cm⁻²**, shifted *E*₍corr₎ from **−0.238 to −0.210 V vs SCE**, increased hardness from **126 to 157 HV0.2**, and produced >98% density (shiyang2025effectofcr pages 1-4, shiyang2025effectofcr pages 7-9, shiyang2025effectofcr pages 9-10, shiyang2025effectofcr pages 4-7). It materially overlaps the proposed Cu–Ni–Cr space, but used LPBF and mechanically mixed powders—not single-stream DED of a pre-alloyed powder—and did not establish repair compatibility, crack freedom, natural/ASTM seawater durability, or superiority to wrought C71500.
>
> **4. Make corrosion-test rigor a differentiator, not merely another response variable.** Much laser-AM copper literature stops at density, phases, hardness, and tensile behavior; some nominally marine studies report only short electrochemical tests in 3.5 wt% NaCl. Examples include Cu–10Sn Tafel testing and CMT-AM NAB polarization, while laser-DED NAB work has explicitly left seawater corrosion for future work (huo2025modulatingheatinput pages 10-13, doyle2022additivemanufacturingofa pages 58-62, doyle2022additivemanufacturingofa pages 53-58, top2022investigationofmicrostructural pages 5-6, top2022investigationofmicrostructural pages 4-5, top2022investigationofmicrostructural pages 2-4). Use a defensible hierarchy: rapid polarization/EIS for screening, then ASTM D1141 or natural seawater immersion with controlled aeration/flow, mass loss, cross-sectional selective-attack depth, corrosion products, and wrought C71500 controls.
>
> **5. Claim the narrow, supportable white space—not “first AM copper-alloy design.”** Barr et al. already compared NAB compositions in LPBF, and laser-DED/WAAM studies already establish NAB process–microstructure–property relationships (nemani2024advancementsinadditive pages 74-79, timmons2025laserpowderbed pages 1-2, nemani2024advancementsinadditive pages 79-83, doyle2022additivemanufacturingofa pages 47-53). The defensible gap is the combined demonstration of **new low-Ni Cu–Ni and NAB compositions, made as characterized pre-alloyed powder, deposited by single-stream blown-powder laser DED, dense and crack-free both self-supported and on naval repair substrates, and seawater-resistant as deposited at least to wrought C71500**, with composition selected by cost-aware physics-informed Bayesian optimization.


*Blockquote: Ranked, actionable guidance for differentiating the proposed ONR YIP work from the closest copper-alloy AM precedents while making appropriately bounded novelty claims.*

---

### Summary of Gaps Relative to the Proposed Work

The literature search reveals that the proposed work occupies a narrowly defined but defensible white space at the intersection of several gaps:

1. **Blown-powder laser DED of pre-alloyed copper alloy powders** with composition designed for marine corrosion is essentially unoccupied. All laser-DED NAB work identified used wire feed (Doyle 2022) or standard compositions (doyle2022additivemanufacturingofa pages 53-58, doyle2022additivemanufacturingofa pages 43-47). All LPBF NAB work used commercial powders (C95800, C63000, C63020, C64200) (nemani2024advancementsinadditive pages 74-79, timmons2025laserpowderbed pages 1-2).

2. **As-deposited seawater corrosion** testing of laser AM copper alloys is extremely sparse. Most studies either omit corrosion entirely (Doyle 2022, Timmons 2025) or use short-term polarization in 3.5% NaCl (Gao 2025, Huo 2025, Top 2022) rather than long-term immersion in natural or ASTM D1141 substitute seawater (huo2025modulatingheatinput pages 10-13, shiyang2025effectofcr pages 1-4, doyle2022additivemanufacturingofa pages 58-62, top2022investigationofmicrostructural pages 5-6).

3. **Computational alloy design (CALPHAD + thermal model + Bayesian optimization)** has not been applied to copper alloys for AM with corrosion as a target (balkan2021thermochemicalmodellingand pages 9-13, samad2025multimaterialadditivemanufacturing pages 25-27, balkan2021thermochemicalmodellingand pages 13-18, canacoo2026laseradditivemanufacturing pages 22-24).

4. **Deposition on repair substrates** (cast NAB, wrought Cu-Ni) and **benchmarking against wrought C71500** in seawater are not documented for any laser-AM copper alloy.

5. **In-house ultrasonic atomization of custom copper alloy powders** for DED is not represented in the literature; all studies use commercial pre-alloyed or mechanically blended powders.

References

1. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

2. (timmons2025laserpowderbed pages 1-2): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

3. (shiyang2025effectofcr pages 1-4): GAO Shiyang, HE Xing, Z Mina, and C Haida. Effect of cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting. Unknown journal, 2025. URL: https://doi.org/10.19591/j.cnki.cn11-1974/tf.2025030025, doi:10.19591/j.cnki.cn11-1974/tf.2025030025.

4. (shiyang2025effectofcr pages 7-9): GAO Shiyang, HE Xing, Z Mina, and C Haida. Effect of cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting. Unknown journal, 2025. URL: https://doi.org/10.19591/j.cnki.cn11-1974/tf.2025030025, doi:10.19591/j.cnki.cn11-1974/tf.2025030025.

5. (shiyang2025effectofcr pages 9-10): GAO Shiyang, HE Xing, Z Mina, and C Haida. Effect of cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting. Unknown journal, 2025. URL: https://doi.org/10.19591/j.cnki.cn11-1974/tf.2025030025, doi:10.19591/j.cnki.cn11-1974/tf.2025030025.

6. (timmons2025laserpowderbed pages 23-26): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

7. (timmons2025laserpowderbed pages 19-23): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

8. (timmons2025laserpowderbed pages 2-4): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

9. (doyle2022additivemanufacturingofa pages 58-62): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

10. (doyle2022additivemanufacturingofa pages 53-58): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

11. (doyle2022additivemanufacturingofa pages 43-47): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

12. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

13. (huo2025modulatingheatinput pages 1-2): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

14. (top2022investigationofmicrostructural pages 5-6): Mustafa Naci TOP, Semih OZBEY, Batuhan SORUŞBAY, and Hamit GÜLSOY. Investigation of microstructural, mechanical and corrosion properties of cu-10sn bronze parts produced by selective laser melting. Türk Doğa ve Fen Dergisi, 11:76-81, Jun 2022. URL: https://doi.org/10.46810/tdfd.1106743, doi:10.46810/tdfd.1106743. This article has 7 citations.

15. (top2022investigationofmicrostructural pages 4-5): Mustafa Naci TOP, Semih OZBEY, Batuhan SORUŞBAY, and Hamit GÜLSOY. Investigation of microstructural, mechanical and corrosion properties of cu-10sn bronze parts produced by selective laser melting. Türk Doğa ve Fen Dergisi, 11:76-81, Jun 2022. URL: https://doi.org/10.46810/tdfd.1106743, doi:10.46810/tdfd.1106743. This article has 7 citations.

16. (top2022investigationofmicrostructural pages 1-2): Mustafa Naci TOP, Semih OZBEY, Batuhan SORUŞBAY, and Hamit GÜLSOY. Investigation of microstructural, mechanical and corrosion properties of cu-10sn bronze parts produced by selective laser melting. Türk Doğa ve Fen Dergisi, 11:76-81, Jun 2022. URL: https://doi.org/10.46810/tdfd.1106743, doi:10.46810/tdfd.1106743. This article has 7 citations.

17. (top2022investigationofmicrostructural pages 2-4): Mustafa Naci TOP, Semih OZBEY, Batuhan SORUŞBAY, and Hamit GÜLSOY. Investigation of microstructural, mechanical and corrosion properties of cu-10sn bronze parts produced by selective laser melting. Türk Doğa ve Fen Dergisi, 11:76-81, Jun 2022. URL: https://doi.org/10.46810/tdfd.1106743, doi:10.46810/tdfd.1106743. This article has 7 citations.

18. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

19. (balkan2021thermochemicalmodellingand pages 9-13): ME Balkan. Thermochemical modelling and directed energy deposition of copper-nickel functionally gradient materials. Unknown journal, 2021.

20. (balkan2021thermochemicalmodellingand pages 13-18): ME Balkan. Thermochemical modelling and directed energy deposition of copper-nickel functionally gradient materials. Unknown journal, 2021.

21. (yang2024circumventingcrackingin pages 23-23): Zhening Yang, Alexander Richter, Hui Sun, Zi-Kui Liu, and Allison M. Beese. Circumventing cracking in grading 316l stainless steel to monel400 through compositional modifications. Jan 2024. URL: https://doi.org/10.48550/arxiv.2407.16050, doi:10.48550/arxiv.2407.16050. This article has 1 citations.

22. (canacoo2026laseradditivemanufacturing pages 22-24): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

23. (canacoo2026laseradditivemanufacturing pages 24-25): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

24. (shiyang2025effectofcr pages 4-7): GAO Shiyang, HE Xing, Z Mina, and C Haida. Effect of cr on microstructure and corrosion resistance of copper-nickel alloys fabricated by selective laser melting. Unknown journal, 2025. URL: https://doi.org/10.19591/j.cnki.cn11-1974/tf.2025030025, doi:10.19591/j.cnki.cn11-1974/tf.2025030025.

25. (timmons2025laserpowderbed pages 15-19): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

26. (doyle2022additivemanufacturingofa pages 47-53): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

27. (nemani2024advancementsinadditive pages 62-68): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

28. (nemani2024advancementsinadditive pages 26-28): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

29. (nemani2024advancementsinadditive pages 112-113): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

30. (samad2025multimaterialadditivemanufacturing pages 25-27): Saneej N. Samad, Jacklyn Griffis, Guha Manogharan, and Nadia Kouraytem. Multi-material additive manufacturing of metals: a review of structures and mechanical characteristics. Engineering Science in Additive Manufacturing, 1:025180010, Jun 2025. URL: https://doi.org/10.36922/esam025180010, doi:10.36922/esam025180010. This article has 25 citations.
