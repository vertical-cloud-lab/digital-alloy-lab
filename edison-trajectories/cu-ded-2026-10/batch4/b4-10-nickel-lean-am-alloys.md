<!--
Edison Scientific LITERATURE task (batch 4)
- Task ID: 4a7669c6-b815-4939-b8fa-c113c2997a04
- Submitted: 2026-10-17T06:11:17Z
- Fetched: 2026-10-17T06:41:59Z (status: success)
- Raw trajectory JSON: ../raw/b4-10-nickel-lean-am-alloys.json.gz
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

QUESTION: What additive manufacturing (any process) and laser cladding
results exist for nickel-lean marine copper alloys: manganese-aluminum bronze
(C95700, CuMn11-13Al8Fe3Ni2-3), Cu-Ni-Al (5-15 Ni, 1-3 Al, e.g. Hiduron-type
or Cu-7Ni-3Al-1Fe-1Mn), and Cu-Al-Fe-Mn without Ni? Report process,
composition, as-deposited phases (beta, kappa, NiAl/Ni3Al precipitation
during reheating), porosity, and corrosion in NaCl or seawater, especially
Wang et al. 2026 (Adv. Eng. Mater., MAB by laser DED) and Ziqiang et al. 2025
(Sci. Rep., laser cladding of ZCuAl8Mn13Fe3Ni2 propeller alloy). Which
nickel-lean composition is the most promising starting point for a DED
powder, and why?

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

QUESTION: What additive manufacturing (any process) and laser cladding
results exist for nickel-lean marine copper alloys: manganese-aluminum bronze
(C95700, CuMn11-13Al8Fe3Ni2-3), Cu-Ni-Al (5-15 Ni, 1-3 Al, e.g. Hiduron-type
or Cu-7Ni-3Al-1Fe-1Mn), and Cu-Al-Fe-Mn without Ni? Report process,
composition, as-deposited phases (beta, kappa, NiAl/Ni3Al precipitation
during reheating), porosity, and corrosion in NaCl or seawater, especially
Wang et al. 2026 (Adv. Eng. Mater., MAB by laser DED) and Ziqiang et al. 2025
(Sci. Rep., laser cladding of ZCuAl8Mn13Fe3Ni2 propeller alloy). Which
nickel-lean composition is the most promising starting point for a DED
powder, and why?

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


## Nickel-lean marine copper alloys: evidence relevant to powder-fed laser DED

**Bottom line.** Powder-fed laser cladding of an approximately 2 wt% Ni manganese–aluminum bronze (MAB) has been demonstrated, but its as-clad corrosion current was **higher**, not lower, than that of the corresponding casting. A separate 2026 paper explicitly reports laser DED of MAB, creating a direct prior-art issue; its full text could not be obtained, so its composition, porosity, phases, and corrosion numbers cannot responsibly be stated here. Neither result establishes corrosion parity with wrought C71500 in seawater. (ziqiang2025lasercladdingremanufacturing pages 1-3, ziqiang2025lasercladdingremanufacturing pages 6-9)

The following table separates direct laser-cladding evidence from cast metallurgical precedents and *wire-electron-beam* analogues. The latter are AM, but neither blown-powder laser DED nor wire-laser DED or WAAM. [CITE] identifies useful proposal citations; [NUMBERS] identifies quantitative benchmarks; [NAVY] denotes an identified marine/propeller application, **not verified Navy funding**; [NOVELTY-RISK] denotes overlap; and [GAP] denotes a missing measurement or demonstration. (ziqiang2025lasercladdingremanufacturing pages 1-3, raute2023processsetupand pages 1-2, chumaevskii2025effectofthe pages 3-5)

| Directly checked paper | Process and composition, wt% | As-produced phases / quality | Test conditions and key values | Key limitation for proposed powder DED |
|---|---|---|---|---|
| **Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. “Laser cladding remanufacturing of propeller ZCuAl8Mn13Fe3Ni2 alloy.” *Scientific Reports* 15, 12381 (2025). [DOI: 10.1038/s41598-025-96674-4](https://doi.org/10.1038/s41598-025-96674-4)** (ziqiang2025lasercladdingremanufacturing pages 1-3, ziqiang2025lasercladdingremanufacturing pages 6-9) | Powder-fed laser cladding onto same-alloy cast substrate; gas-atomized spherical powder, 45–150 µm. Assay: Al 8.15, Mn 13.16, Fe 3.03, Ni 2.11, C 0.035, Pb <0.005, Cu bal. Laser 1600 W, scan 6 mm/s, powder-feed setting 2 r/min, gas 3.5 L/min. | As-clad α-Cu FCC + β-Cu3Al BCC + γ₂-Al4Cu9 + κ (reported AlFe, AlFe3, Ni2MnAl); finer 5–10 µm grains and more β/κ than cast; HAZ ≈100 µm. No quantitative porosity, crack metric, powder oxygen, Hall flow, or apparent density. | Artificial-seawater weight-loss testing is mentioned, but composition/duration and numerical loss are unavailable. Polarization: *E*cor = −0.271 V clad versus −0.266 V cast. Article is internally inconsistent: table/conclusion imply *i*cor = **3.729×10⁻³** versus 3.142×10⁻³ mA/cm², while abstract/body state **3.729×10⁻²** versus 3.142×10⁻² mA/cm². Clad hardness 278 HB versus cast 242 HB (+14.88%); clad current +18.68%, hence slightly poorer corrosion resistance. (ziqiang2025lasercladdingremanufacturing pages 3-6, ziqiang2025lasercladdingremanufacturing pages 1-3) | Closest verified single-powder laser-cladding precedent and direct novelty risk. It does **not** establish dense/crack-free bulk self-builds, NAB or Cu–Ni repair compatibility, 30-day seawater behavior, or parity with wrought C71500. Current-density exponent must be checked before proposal use. |
| **Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. “The Effect of Kappa Phases on Tribocorrosion Behaviour of Nickel Aluminum Bronze (NAB) and Manganese Aluminum Bronze (MAB).” *Lubricants* 13, 290 (2025). [DOI: 10.3390/lubricants13070290](https://doi.org/10.3390/lubricants13070290)** (berlangalabari2025theeffectof pages 2-4, berlangalabari2025theeffectof pages 4-7) | Cast C95700 MAB, identified as CuAl10Mn12Fe5; measured Mn 12.8 and Ni 2.1 (exact bulk Al/Fe values not supplied in checked passage). Compared with cast CuAl10Fe5Ni5 NAB. | α + β/β′ + κ. MAB fractions: α 57.7%, β 30.4%, κ 11.8%; κ mean area 753 µm². MAB κ is Mn/Fe-rich and rosette-like. Hardness: α 130±6 HV, β 250±8 HV, κ 3.3±0.2 GPa; bulk 150±6 HV. | 1 M NaCl, room temperature; Al₂O₃ ball, 10 or 40 N; OCP/COF for 3600 s; polarization during sliding at 0.1 mV/s; Ag/AgCl reference. Static corrosion ≈0.02 mm/y and loaded ≈0.1 mm/y; MAB OCP ≈−500 mV. Wear coefficients: 2.2×10⁻⁶ mm³/Nm at 10 N and 6.1×10⁻⁶ at 40 N. Selective attack occurred at κ and α/κ interfaces. (berlangalabari2025theeffectof pages 2-4, berlangalabari2025theeffectof pages 7-11) | Strong marine degradation benchmark, but **cast**, not AM; 1 M NaCl is not natural or ASTM D1141 seawater. No powder, porosity, immersion-depth, EIS, or C71500 comparison. It shows the β/κ selective-corrosion risk of C95700-like deposits. |
| **Ran Yang, Jiuba Wen, Yanjun Zhou, Kexing Song, Liye Niu, Huiwen Guo, and Yan Yu. “Effect of heat treatment on microstructure and mechanical properties of Cu–6.9Ni–2.97Al–0.99Fe–1.06Mn alloy.” *Materials Science and Technology* 36, 83–91 (2020). [DOI: 10.1080/02670836.2019.1684035](https://doi.org/10.1080/02670836.2019.1684035)** (yang2020effectofheat pages 3-6, yang2020effectofheat pages 1-3) | Conventionally cast Cu–6.9Ni–2.97Al–0.99Fe–1.06Mn; solution treated 950°C/2 h, water quenched, then aged at 500–600°C. | As-cast α-Cu plus coherent FCC γ-Ni3Al, 2–15 nm. Solution treatment dissolves precipitates to single α; ageing 550°C/6 h produces 6–13 nm coherent Ni3Al. No NiAl was identified. | No corrosion test. At 550°C/6 h: hardness 153 HB versus 58 HB solutionized; tensile strength 587 MPa versus 305 MPa; elongation remained >15%. Peak reported hardness was 167 HB at 550°C. (yang2020effectofheat pages 6-8, yang2020effectofheat pages 3-6) | Best direct basis for a Cu–7Ni–3Al–1Fe–1Mn starting chemistry and Ni3Al strengthening, but it is **not AM or as-deposited** and strengthening required deliberate furnace ageing. Whether DED interlayer reheating precipitates Ni3Al without post-build treatment—and whether it helps seawater corrosion—remains unproved. |
| **Julius Raute, Max Biegler, and Michael Rethmeier. “Process Setup and Boundaries of Wire Electron Beam Additive Manufacturing of High-Strength Aluminum Bronze.” *Metals* 13, 1416 (2023). [DOI: 10.3390/met13081416](https://doi.org/10.3390/met13081416)** (raute2023processsetupand pages 1-2, raute2023processsetupand pages 2-4) | Wire-electron-beam DED in vacuum; assayed wire: Cu bal., Al 9.0, Ni 4.5, Fe 3.5, Mn 1.3. Deposited on 1.4404 stainless steel. Stable energy window 18–32 J/mm³; deposition 0.6–2.5 kg/h. | Dendritic Cu–Al solid solution in quasieutectoid matrix with probable fine Fe/Ni-rich κ; reheating/slow vacuum cooling was inferred to suppress brittle β. Cylinders had no optically observed pores, inclusions, or cracks above the base plate, but no numerical porosity. Hardness generally ≈150–210 HV1 or >200 HV1 depending condition. | No corrosion testing. Horizontal tensile specimens averaged yield ≈369 MPa, UTS ≈693 MPa, elongation ≈18%; individual elongations 12.4–21%. (raute2023processsetupand pages 12-14, raute2023processsetupand pages 7-9) | Demonstrates processability and useful reheating-driven phase control, but it is **wire-electron-beam**, not powder-laser DED, and uses ≈4.5% Ni rather than the target Cu–Ni–Al family. No NaCl/seawater or C71500 benchmark. |
| **A. V. Chumaevskii, A. V. Nikolaeva, V. M. Semenchuk, K. S. Osipovich, D. A. Gurianov, and E. A. Kolubaev. “Effect of the order of component deposition on the structure of the transition zone of bimetallic structures produced using high-performance electron beam additive manufacturing.” *Letters on Materials* 15, 199–206 (2025). [DOI: 10.48612/letters/2025-3-199-206](https://doi.org/10.48612/letters/2025-3-199-206)** (chumaevskii2025effectofthe pages 1-2, chumaevskii2025effectofthe pages 3-5) | Wire-electron-beam DED of CuAl9Mn2 onto 13Mn6 steel. Bronze wire: Cu bal., Al 8–10, Mn 1.5–2.5; no intentional Fe or Ni listed. | Bronze: dendritic α-Cu columnar grains + residual martensitic β′. Bronze-on-steel gave a ≈5.5±0.8 µm transition layer with no observed pores, cracks, or delamination; reverse order increased mixing and caused boundary cracks/delamination. No numerical porosity. | No corrosion test. For bronze deposited over steel: bronze region UTS 468 MPa, yield 191 MPa, elongation 59%; transition zone 408 MPa, 198 MPa, and 38%. Bronze microhardness ≈1.15±0.08 GPa. (chumaevskii2025effectofthe pages 3-5, chumaevskii2025effectofthea pages 7-8, chumaevskii2025effectofthe pages 7-8) | Useful repair-interface/process-order evidence only. It is **wire-electron-beam**, not powder DED; substrate is steel, not NAB or Cu–Ni; CuAl9Mn2 is Ni-free but also lacks intentional Fe, so it is not the requested Cu–Al–Fe–Mn family. No marine-corrosion evidence. |
| **V. O. Semin, A. O. Panfilov, V. R. Utyaganova, A. V. Vorontsov, and A. P. Zykova. “Corrosion characteristics of BrAMts9-2/06Kh18N9T composites obtained by dual-wire electron-beam additive manufacturing.” *Obrabotka Metallov* 26(3), 163–178 (2024). [DOI: 10.17212/1994-6309-2024-26.3-163-178](https://doi.org/10.17212/1994-6309-2024-26.3-163-178)** (семин2024коррозионныехарактеристикикомпозитов pages 1-2, семин2024коррозионныехарактеристикикомпозитов pages 2-4) | Dual-wire electron-beam AM of CuAl9Mn2 bronze and Ni-bearing ER321/06Kh18N9T stainless steel at 10–75 vol% steel. Wire diameter 1.6 mm; 30 kV, 44–77 mA, 400 mm/min. The composite is not nickel-free. | Increasing steel suppresses bronze β′ and introduces α-Fe(Cr), κIV-Fe3Al and Ni-bearing phases/solid solution. This is an intentionally mixed bronze–steel composite, not a pre-alloyed marine-copper deposit. | 3.5 wt% NaCl; three-electrode cell with Ag/AgCl (1 M KCl), graphite counter; polarization −0.5 to 0 V at 1 mV/s; EIS 0.1–10⁵ Hz, 10 mV. Plain CuAl9Mn2: *E*cor −0.207 V, *i*cor 11.390 µA/cm², initial *R*ct 1,385 Ω·cm². With 25/50/75 vol% steel: *i*cor 4.945/1.043/0.512 µA/cm² and initial *R*ct 7,269/21,630/177,000 Ω·cm². (семин2024коррозионныехарактеристикикомпозитов pages 8-10) | Quantitative electrochemical benchmark but **dual-wire electron-beam composition blending**, directly outside the single-pre-alloyed-powder scope. Improvement derives largely from stainless fraction; there is no immersion duration, natural/ASTM seawater test, powder characterization, or C71500 comparator. |


*Table: Comparison of directly verified AM, cladding, and cast studies relevant to nickel-lean marine copper alloys. It distinguishes quantitative evidence from unresolved reporting errors and major process or corrosion gaps.*

### Direct laser precedent and an important reporting discrepancy

**[CITE] [NUMBERS] [NAVY—propeller application] [NOVELTY-RISK] [GAP]** Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen, “Laser cladding remanufacturing of propeller ZCuAl8Mn13Fe3Ni2 alloy,” *Scientific Reports* **15**, 12381 (2025), **doi:10.1038/s41598-025-96674-4**. This is pre-alloyed, gas-atomized powder laser-cladded onto a cast substrate of the same alloy—not a demonstration of a bulk, self-supported DED build or repair on NAB or wrought Cu–Ni. Its measured powder chemistry was Cu balance, **8.15 Al–13.16 Mn–3.03 Fe–2.11 Ni wt%**; particle size was **45–150 µm**. The as-clad coating contained α, β, γ₂, and κ, with more β/κ and less α than cast material, and measured **278 versus 242 HB**. Its reported *E*₍corr₎ was **−0.271 versus −0.266 V**; the clad current was **18.68% higher** than cast. Crucially, the paper is internally inconsistent about the **absolute current-density exponent**: its table/conclusion give **3.729 × 10⁻³ versus 3.142 × 10⁻³ mA cm⁻²**, whereas its abstract/body give **3.729 × 10⁻² versus 3.142 × 10⁻² mA cm⁻²**. Preserve that qualification rather than using either exponent as an unambiguous benchmark. Artificial-seawater weight-loss testing is mentioned, but a verified composition, exposure time, flow rate, and numerical immersion loss are unavailable in the examined passages; likewise no quantitative density/porosity, Hall flow, apparent powder density, or powder oxygen was established. (ziqiang2025lasercladdingremanufacturing pages 1-3, ziqiang2025lasercladdingremanufacturing pages 3-6, ziqiang2025lasercladdingremanufacturing pages 6-9)

**[CITE] [NOVELTY-RISK] [GAP]** Junfeng Wang, Renping Zhang, Chun-Huan Guo, Tong-Yu Zhang, Shi-Li Cheng, Xiaofan Han, Wen-Yuan Wang, and Feng-Chun Jiang, “Microstructure and corrosion resistance of manganese-aluminum bronze alloy fabricated by laser-directed energy deposition,” *Advanced Engineering Materials* (2026), **doi:10.1002/adem.71167**. The bibliographic record establishes **MAB laser DED plus corrosion** as prior work. The article itself was unobtainable in this search: its feedstock composition and whether it used one pre-alloyed blown-powder stream, its phases, density, corrosion electrolyte and duration, and measured values are **unverified**, not negative findings. It must be checked before claiming novelty for MAB DED or citing numerical performance. No Navy/DoD funding can be established from the available record.

### Phase-controlled alternatives and boundaries of the evidence

**[CITE] [NUMBERS] [GAP]** Ran Yang, Jiuba Wen, Yanjun Zhou, Kexing Song, Liye Niu, Huiwen Guo, and Yan Yu, “Effect of heat treatment on microstructure and mechanical properties of Cu–6.9Ni–2.97Al–0.99Fe–1.06Mn alloy,” *Materials Science and Technology* **36**, 83–91 (2020), **doi:10.1080/02670836.2019.1684035**. This is **cast**, not AM: as-cast α-Cu already contained **2–15 nm γ-Ni₃Al**; solutionizing at **950 °C for 2 h** dissolved it, and furnace ageing at **550 °C for 6 h** produced coherent **6–13 nm Ni₃Al**, increasing tensile strength from **305 to 587 MPa** and hardness from **58 to 153 HB** relative to the solutionized condition, while elongation remained **>15%**. The reported peak hardness of **167 HB** is a separate peak on the ageing curves, not the cited 6 h value. These data do **not** demonstrate NiAl, precipitation *during DED reheating*, or NaCl/seawater resistance of an as-deposited Cu–Ni–Al alloy. (yang2020effectofheat pages 3-6, yang2020effectofheat pages 6-8)

**[CITE] [NUMBERS] [GAP]** Julius Raute, Max Biegler, and Michael Rethmeier, “Process Setup and Boundaries of Wire Electron Beam Additive Manufacturing of High-Strength Aluminum Bronze,” *Metals* **13**, 1416 (2023), **doi:10.3390/met13081416**. Although designated CuAl8Ni6, the **actual reported wire assay** is Cu balance, **9.0 Al–4.5 Ni–3.5 Fe–1.3 Mn wt%**. Wire-electron-beam DED produced optically pore-/crack-free cylinders **above the base plate**, without a quantified density, and horizontal specimens averaged **369 MPa yield strength, 693 MPa UTS, and 18% elongation**. The authors infer that repeated heating and slow vacuum cooling favor α and fine κ over brittle β; that inference is **not** evidence of Ni₃Al or NiAl precipitation. **No chloride-corrosion test** was reported. This is a useful feasibility comparator but neither Cu–Ni–Al at 1–3% Al nor laser-powder DED. (raute2023processsetupand pages 2-4, raute2023processsetupand pages 7-9, raute2023processsetupand pages 12-14)

**[CITE] [NUMBERS] [NAVY—marine-alloy service context] [GAP]** Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio, “The Effect of Kappa Phases on Tribocorrosion Behaviour of Nickel Aluminum Bronze (NAB) and Manganese Aluminum Bronze (MAB),” *Lubricants* **13**, 290 (2025), **doi:10.3390/lubricants13070290**. Their **cast C95700** contained **12.8 wt% Mn and 2.1 wt% Ni**: it is nickel-*lean*, **not nickel-free**. The cast microstructure included **57.7% α, 30.4% β, and 11.8% κ** by the paper’s phase quantification, with κ-associated selective attack. In **1 M NaCl**, room-temperature sliding at **10/40 N for 3,600 s**, static corrosion was described as approximately **0.02 mm yr⁻¹**, rising to approximately **0.1 mm yr⁻¹** with wear; these approximate rates are **not** 30-day immersion measurements or C71500 comparisons. A cropped phase-comparison figure and phase-quantification table support the cast α/β/κ observation. (berlangalabari2025theeffectof pages 2-4, berlangalabari2025theeffectof pages 4-7, berlangalabari2025theeffectof pages 7-11, berlangalabari2025theeffectof media 5840abed)

**[CITE] [NUMBERS] [GAP]** A. V. Chumaevskii, A. V. Nikolaeva, V. M. Semenchuk, K. S. Osipovich, D. A. Gurianov, and E. A. Kolubaev, “Effect of the order of component deposition on the structure of the transition zone of bimetallic structures produced using high-performance electron beam additive manufacturing,” *Letters on Materials* **15**, 199–206 (2025), **doi:10.48612/letters/2025-3-199-206**. **Wire-electron-beam** deposition of nominal **Cu–8–10Al–1.5–2.5Mn wt%** bronze onto **13Mn6 steel** produced dendritic α plus residual β′ and an interface with no observed pores, cracks, or delamination; **reverse deposition order** caused interfacial defects. The bronze-region UTS/yield/elongation were **468/191 MPa/59%**. This is a useful warning about repair-interface directionality, but **CuAl9Mn2 has no intentionally specified Fe or Ni in its bronze feed**: Fe acquired from steel does not make it a single-feed Cu–Al–Fe–Mn powder alloy. No NaCl/seawater test or numerical porosity is reported. (chumaevskii2025effectofthe pages 3-5, chumaevskii2025effectofthea pages 7-8)

**[CITE] [NUMBERS] [GAP]** V. O. Semin, A. O. Panfilov, V. R. Utyaganova, A. V. Vorontsov, and A. P. Zykova, “Corrosion characteristics of BrAMts9-2/06Kh18N9T composites obtained by dual-wire electron-beam additive manufacturing,” *Obrabotka Metallov* **26**(3), 163–178 (2024), **doi:10.17212/1994-6309-2024-26.3-163-178**. In **3.5 wt% NaCl**, plain CuAl9Mn2 yielded **11.390 µA cm⁻²**, *E*₍corr₎ **−0.207 V**, and initial *R*₍ct₎ **1,385 Ω cm²**; intentionally blending **25/50/75 vol% stainless steel** reduced the reported currents to **4.945/1.043/0.512 µA cm⁻²**. These are short electrochemical measurements, **not** validated seawater-immersion rates. The composite incorporates **Ni-bearing stainless steel**, and the improvement must not be claimed for nickel-free Cu–Al–Fe–Mn—or for a single pre-alloyed powder stream. (семин2024коррозионныехарактеристикикомпозитов pages 2-4, семин2024коррозионныехарактеристикикомпозитов pages 8-10, семин2024коррозионныехарактеристикикомпозитов pages 4-6)

**Evidence gaps that affect the decision.** No examined paper establishes, for a **pre-alloyed Cu–Al–Fe–Mn powder with zero Ni**, all of blown-powder laser-DED processability, as-deposited β/κ phase fractions, quantified density/cracking, and marine corrosion. CuAl9Mn2 bronze-on-steel and bronze–stainless results do not fill that gap. Likewise, the examined Cu–Ni–Al work establishes *cast* Ni₃Al precipitation, not a verified as-deposited DED precipitation-and-corrosion mechanism. None of the checked reports supplies a matched **wrought C71500**, 30-day natural/ASTM D1141 seawater, controlled-flow, selective-attack-depth comparison, or the proposed per-lot Hall-flow/apparent-density/oxygen dataset. Do not compare their *i*₍corr₎ values as though **1 M NaCl, 3.5 wt% NaCl, and unspecified artificial seawater** were interchangeable. (berlangalabari2025theeffectof pages 2-4, yang2020effectofheat pages 6-8, chumaevskii2025effectofthe pages 3-5, семин2024коррозионныехарактеристикикомпозитов pages 2-4, ziqiang2025lasercladdingremanufacturing pages 1-3)

### Most promising first powder

**Start with Cu–≈7Ni–≈2–3Al–≈1Fe–≈1Mn (wt%; Cu balance), using the directly studied Cu–6.9Ni–2.97Al–0.99Fe–1.06Mn composition as the initial target.** This is a **research starting point, not a demonstrated C71500-equivalent alloy**. Relative to ~2% Ni MAB it consumes more nickel, but its cast evidence offers a largely α-Cu matrix with a measured Ni₃Al-strengthening route rather than deliberately accepting a large β/κ fraction associated with selective corrosion. Relative to 10–30% Ni Cu–Ni compositions it remains substantially nickel-leaner. The decisive proposed experiments are whether actual DED thermal cycles produce useful Ni₃Al **without post-build ageing**, whether the deposit remains dense and crack-free on *both* repair substrates, and whether as-deposited chloride/seawater performance meets the wrought-C71500 control. Treat **C95700-like Cu–Al–Mn–Fe–≈2Ni** as the closest laser-process and propeller-repair **benchmark**, not an untested novelty claim; retain **zero-Ni Cu–Al–Fe–Mn** as a higher-risk exploratory branch rather than calling CuAl9Mn2-with-steel its proof. (yang2020effectofheat pages 3-6, yang2020effectofheat pages 6-8, ziqiang2025lasercladdingremanufacturing pages 6-9, berlangalabari2025theeffectof pages 4-7, chumaevskii2025effectofthe pages 3-5)

## Top 5 things the PI should know

1. **MAB laser DED is already published in 2026;** verify Wang *et al.*’s full article and exact scope before making any novelty claim. **doi:10.1002/adem.71167.**
2. **Single-alloy MAB powder laser cladding already exists**, and its reported as-clad electrochemical behavior is *worse* than same-alloy cast—not proof of superior as-deposited marine service. **doi:10.1038/s41598-025-96674-4.** (ziqiang2025lasercladdingremanufacturing pages 1-3, ziqiang2025lasercladdingremanufacturing pages 6-9)
3. **The Pi *et al.* absolute corrosion current contains a tenfold reporting discrepancy.** Quote the relative **+18.68%** finding with the exponent caveat; do not build a quantitative proposal target on an unqualified value. (ziqiang2025lasercladdingremanufacturing pages 6-9, ziqiang2025lasercladdingremanufacturing pages 1-3)
4. **Cu–7Ni–3Al–1Fe–1Mn has directly observed cast Ni₃Al, not proven DED self-ageing or seawater parity.** DED interpass-thermal-history predictions and direct precipitate measurements are a testable distinction from the cast work. (yang2020effectofheat pages 6-8, yang2020effectofheat pages 3-6)
5. **The defensible unmet result is a linked, controlled demonstration:** characterized *single* pre-alloyed powder → quantified self-build and NAB/Cu–Ni repair interfaces → measured as-deposited phases/defects → matched C71500 seawater corrosion, including long exposure and localized attack. The presently checked electrochemical and electron-beam studies do not establish that result. (ziqiang2025lasercladdingremanufacturing pages 1-3, chumaevskii2025effectofthe pages 3-5, семин2024коррозионныехарактеристикикомпозитов pages 2-4)

References

1. (ziqiang2025lasercladdingremanufacturing pages 1-3): Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. Laser cladding remanufacturing of propeller zcual8mn13fe3ni2 alloy. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-96674-4, doi:10.1038/s41598-025-96674-4. This article has 7 citations and is from a peer-reviewed journal.

2. (ziqiang2025lasercladdingremanufacturing pages 6-9): Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. Laser cladding remanufacturing of propeller zcual8mn13fe3ni2 alloy. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-96674-4, doi:10.1038/s41598-025-96674-4. This article has 7 citations and is from a peer-reviewed journal.

3. (raute2023processsetupand pages 1-2): Julius Raute, Max Biegler, and Michael Rethmeier. Process setup and boundaries of wire electron beam additive manufacturing of high-strength aluminum bronze. Metals, 13:1416, Aug 2023. URL: https://doi.org/10.3390/met13081416, doi:10.3390/met13081416. This article has 10 citations.

4. (chumaevskii2025effectofthe pages 3-5): AV Chumaevskii and AV Nikolaeva. Effect of the order of component deposition on the structure of the transition zone of bimetallic structures produced using high-performance electron beam additive …. Unknown journal, 2025.

5. (ziqiang2025lasercladdingremanufacturing pages 3-6): Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. Laser cladding remanufacturing of propeller zcual8mn13fe3ni2 alloy. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-96674-4, doi:10.1038/s41598-025-96674-4. This article has 7 citations and is from a peer-reviewed journal.

6. (berlangalabari2025theeffectof pages 2-4): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

7. (berlangalabari2025theeffectof pages 4-7): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

8. (berlangalabari2025theeffectof pages 7-11): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

9. (yang2020effectofheat pages 3-6): Ran Yang, Jiuba Wen, Yanjun Zhou, Kexing Song, Liye Niu, Huiwen Guo, and Yan Yu. Effect of heat treatment on microstructure and mechanical properties of cu–6.9ni–2.97al–0.99fe–1.06mn alloy. Materials Science and Technology, 36:83-91, Jan 2020. URL: https://doi.org/10.1080/02670836.2019.1684035, doi:10.1080/02670836.2019.1684035. This article has 6 citations and is from a peer-reviewed journal.

10. (yang2020effectofheat pages 1-3): Ran Yang, Jiuba Wen, Yanjun Zhou, Kexing Song, Liye Niu, Huiwen Guo, and Yan Yu. Effect of heat treatment on microstructure and mechanical properties of cu–6.9ni–2.97al–0.99fe–1.06mn alloy. Materials Science and Technology, 36:83-91, Jan 2020. URL: https://doi.org/10.1080/02670836.2019.1684035, doi:10.1080/02670836.2019.1684035. This article has 6 citations and is from a peer-reviewed journal.

11. (yang2020effectofheat pages 6-8): Ran Yang, Jiuba Wen, Yanjun Zhou, Kexing Song, Liye Niu, Huiwen Guo, and Yan Yu. Effect of heat treatment on microstructure and mechanical properties of cu–6.9ni–2.97al–0.99fe–1.06mn alloy. Materials Science and Technology, 36:83-91, Jan 2020. URL: https://doi.org/10.1080/02670836.2019.1684035, doi:10.1080/02670836.2019.1684035. This article has 6 citations and is from a peer-reviewed journal.

12. (raute2023processsetupand pages 2-4): Julius Raute, Max Biegler, and Michael Rethmeier. Process setup and boundaries of wire electron beam additive manufacturing of high-strength aluminum bronze. Metals, 13:1416, Aug 2023. URL: https://doi.org/10.3390/met13081416, doi:10.3390/met13081416. This article has 10 citations.

13. (raute2023processsetupand pages 12-14): Julius Raute, Max Biegler, and Michael Rethmeier. Process setup and boundaries of wire electron beam additive manufacturing of high-strength aluminum bronze. Metals, 13:1416, Aug 2023. URL: https://doi.org/10.3390/met13081416, doi:10.3390/met13081416. This article has 10 citations.

14. (raute2023processsetupand pages 7-9): Julius Raute, Max Biegler, and Michael Rethmeier. Process setup and boundaries of wire electron beam additive manufacturing of high-strength aluminum bronze. Metals, 13:1416, Aug 2023. URL: https://doi.org/10.3390/met13081416, doi:10.3390/met13081416. This article has 10 citations.

15. (chumaevskii2025effectofthe pages 1-2): AV Chumaevskii and AV Nikolaeva. Effect of the order of component deposition on the structure of the transition zone of bimetallic structures produced using high-performance electron beam additive …. Unknown journal, 2025.

16. (chumaevskii2025effectofthea pages 7-8): AV Chumaevskii and AV Nikolaeva. Effect of the order of component deposition on the structure of the transition zone of bimetallic structures produced using high-performance electron beam additive …. Unknown journal, 2025.

17. (chumaevskii2025effectofthe pages 7-8): AV Chumaevskii and AV Nikolaeva. Effect of the order of component deposition on the structure of the transition zone of bimetallic structures produced using high-performance electron beam additive …. Unknown journal, 2025.

18. (семин2024коррозионныехарактеристикикомпозитов pages 1-2): В Семин, А Панфилов, and В Утяганова. Коррозионные характеристики композитов брамц9-2/06х18н9т, полученных двухпроволочным электронно-лучевым аддитивным производством. Unknown journal, 2024.

19. (семин2024коррозионныехарактеристикикомпозитов pages 2-4): В Семин, А Панфилов, and В Утяганова. Коррозионные характеристики композитов брамц9-2/06х18н9т, полученных двухпроволочным электронно-лучевым аддитивным производством. Unknown journal, 2024.

20. (семин2024коррозионныехарактеристикикомпозитов pages 8-10): В Семин, А Панфилов, and В Утяганова. Коррозионные характеристики композитов брамц9-2/06х18н9т, полученных двухпроволочным электронно-лучевым аддитивным производством. Unknown journal, 2024.

21. (berlangalabari2025theeffectof media 5840abed): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

22. (семин2024коррозионныехарактеристикикомпозитов pages 4-6): В Семин, А Панфилов, and В Утяганова. Коррозионные характеристики композитов брамц9-2/06х18н9т, полученных двухпроволочным электронно-лучевым аддитивным производством. Unknown journal, 2024.
