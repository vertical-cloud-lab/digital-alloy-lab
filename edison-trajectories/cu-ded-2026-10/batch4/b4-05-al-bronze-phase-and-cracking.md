<!--
Edison Scientific LITERATURE task (batch 4)
- Task ID: 35ff7da1-9b33-48f5-be8b-02ddcbbebba7
- Submitted: 2026-10-17T06:11:12Z
- Fetched: 2026-10-17T06:41:53Z (status: success)
- Raw trajectory JSON: ../raw/b4-05-al-bronze-phase-and-cracking.json.gz
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

QUESTION: How do Al content and phase constitution (single-phase alpha vs
duplex alpha+beta; Fe and Ni additions) control hot cracking and porosity
when aluminum bronzes and NAB are welded, clad, or deposited, and how does
that interact with seawater corrosion (selective phase corrosion of beta /
beta-prime, kappa-III)? Report filler metal studies (ERCuAl-A1, A2, A3,
ERCuNiAl, ERCuMnNiAl), the Al and Fe thresholds where cracking or selective
attack appears, and DED or laser cladding examples. What composition
window would avoid both cracking and selective phase corrosion as deposited?

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

QUESTION: How do Al content and phase constitution (single-phase alpha vs
duplex alpha+beta; Fe and Ni additions) control hot cracking and porosity
when aluminum bronzes and NAB are welded, clad, or deposited, and how does
that interact with seawater corrosion (selective phase corrosion of beta /
beta-prime, kappa-III)? Report filler metal studies (ERCuAl-A1, A2, A3,
ERCuNiAl, ERCuMnNiAl), the Al and Fe thresholds where cracking or selective
attack appears, and DED or laser cladding examples. What composition
window would avoid both cracking and selective phase corrosion as deposited?

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


# Aluminum-bronze weldability and seawater performance: implications for pre-alloyed powder DED

**Bottom line.** The literature supports a *phase-constitution design rule*, not a validated aluminum or iron percentage at which an aluminum-bronze DED deposit suddenly becomes crack-free and immune to selective corrosion. A predominantly Cu-rich **α deposit**, with neither continuous retained β/β′ nor a connected α–κIII eutectoid, is the defensible starting target. That target must also hold at the **repair interface and heat-affected zone (HAZ)**: a sound deposit can sit above selectively corroding substrate. These are hypotheses to test against as-deposited, phase-resolved immersion results, not established guarantees of performance equal to wrought C71500. (dharmendra2019microstructuralevolutionand pages 1-2, dobson2024corrosionmechanismsand pages 1-6, dobson2024corrosionmechanismsand pages 130-135, dharmendra2019microstructuralevolutionand pages 5-7)

## Mechanism and composition boundaries

In **binary Cu–Al**, the α/duplex boundary is approximately **9 wt% Al under equilibrium**; β can appear above approximately **8–8.5 wt% Al under ordinary nonequilibrium cooling**. An older binary-alloy treatment places the limiting α solubility at **9.4 wt% Al** and the α+β interval at roughly **9.4–11.8 wt% Al**. These are cooling- and alloy-dependent *phase boundaries*, **not measured hot-cracking thresholds**. Nickel and iron additions around 4–5 wt% each alter β decomposition, consume Al in κ aluminides, and can suppress brittle γ₂ relative to binary bronze; they do **not** ensure an α-only *as-deposited* laser microstructure. Nor is **11 wt% Al** a universal γ₂ onset for every cooling history. (dharmendra2019microstructuralevolutionand pages 1-2, davis1974surfacingsteelwith pages 12-17, davis1974surfacingsteelwith pages 24-30)

During rapid solidification, a duplex α+β alloy may retain or transform β to martensitic **β′**; slower cooling or subsequent layer reheating can instead produce α plus κ precipitates. The distinction matters: **κII is predominantly Fe₃Al; lamellar κIII is NiAl; fine κIV is Fe-rich.** TEM diffraction established these assignments in a Cu–9Al–4Fe–4Ni–1Mn WAAM deposit that contained κII, κIII and 5–10 nm κIV but *no observed β′*. Fast laser processing can take a different path and retain β′. Fe **above approximately 5 wt%** is associated with coarse κI formation **under slow cooling**; this is neither a demonstrated weld-cracking limit nor proof that an Fe-rich powder below 5 wt% cannot form harmful local phases. (kuprienko2025analysisofnickel pages 18-23, kuprienko2025analysisofnickela pages 36-41, dharmendra2019microstructuralevolutionand pages 5-7, dharmendra2019microstructuralevolutionand pages 9-13)

**Cracks, voids and corrosion are separate outcomes.** α-rich bronze generally favors ductility and avoids a continuous Al-rich β/β′ path. Duplex structures can gain strength or wear resistance but introduce brittle constituents and galvanic interfaces. Hot cracking additionally depends on the solidification path, restraint, impurities, dilution and thermal cycle; porosity depends on entrained gas, oxides, feed quality and lack of fusion. In particular, a reported crack in **steel** caused by liquid Cu penetration is *not* evidence of an intrinsic cracking limit for an aluminum-bronze deposit on NAB. No controlled comparison located here establishes a numerical Al- or Fe-based threshold for both crack-free welding and absence of selective attack. (wang2020theformationmechanisms pages 1-6, dharmendra2019microstructuralevolutionand pages 2-3, wang2020theformationmechanisms pages 6-12, zhao2022microstructureandmechanical pages 4-6)

The electrochemical preference is also **environment-dependent**. In ordinary seawater, α within the α–κIII eutectoid has been reported to dissolve adjacent to κIII; under **locally acidic conditions, approximately pH <4**, the preference can reverse and **κIII itself dissolves** along its continuous lamellae. β′ retained in a weld or HAZ provides another selective-attack route. Thus “α+κ instead of β′” alone is not a sufficient corrosion criterion: *connectivity, local pH, biofouling and residual stress* matter. (berlangalabari2025theeffectof pages 2-4, dobson2024corrosionmechanismsand pages 154-157, dobson2024corrosionmechanismsand pages 122-126)

## Quantitative primary evidence

The following comparison keeps process, exposure and test endpoint together; a short NaCl polarization experiment should not be treated as equivalent to flowing or biofouled seawater immersion.

| Study / DOI | Process and feed chemistry (wt%) | Medium / time | Verified outcomes and limitation |
|---|---|---|---|
| Zhao et al., *Metals* 12 (2022) 781. DOI: [10.3390/met12050781](https://doi.org/10.3390/met12050781) | Blown-powder laser deposition on SUS630; pre-alloyed NAB powder Cu–10.8Al–4.1Ni–4.0Fe, 53–120 µm. N-1: direct NAB/steel; N-2: Ni–5Al interlayer; N-3: Ni–20Cr interlayer. Deposited upper-layer compositions: N-1 Cu–9.8Al–3.8Ni–11.2Fe; N-2 Cu–10.4Al–12.4Ni–4Fe; N-3 Cu–10.9Al–10.8Ni–4.1Fe–1.9Cr. Laser: 2400 W, 1000 mm/min, 3.2 mm spot, 50% overlap. (zhao2022thelaserdeposited pages 2-4, zhao2022thelaserdeposited pages 4-7) | Aerated 3.5 wt% NaCl, 25 ± 5 °C; 20 min stabilization; Ag/AgCl reference; polarization at 0.5 mV/s. ASTM G31 immersion for 7, 14, and 21 d; EIS through 21 d. (zhao2022thelaserdeposited pages 2-4) | At 21 d, maximum attack depths were 3.4 ± 0.1 µm (N-1), 2.0 ± 0.1 µm (N-2), and 1.8 ± 0.1 µm (N-3). Corrosion-current densities were 7.82 ± 0.50, 4.65 ± 0.50, and 4.09 ± 0.40 µA/cm²; corrosion potentials were −248, −255, and −252 mV; polarization resistances were 2810, 5275, and 4865 Ω·cm². Direct deposition produced anodically attacked Fe-rich dendrites; Ni-based interlayers limited steel dilution. Limitation: steel substrate/interlayers and elevated deposited Ni make this unlike single-stream repair on NAB or Cu–Ni. (zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 10-13) |
| Huo et al., *Materials* 18 (2025) 2205. DOI: [10.3390/ma18102205](https://doi.org/10.3390/ma18102205) | Wire-arc DED/CMT on Cu; ERCuNiAl wire Cu–8.73Al–5.90Fe–4.52Ni–1.39Mn. Heat inputs S1–S4: 243.8, 378.8, 502.8, and 644.7 J/mm; interpass temperature ≤50 °C. (huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 2-4) | Aerated 3.5 wt% NaCl, 25 ± 5 °C; 3600 s OCP; saturated calomel reference; EIS from 10⁻² to 10⁵ Hz; polarization at 0.5 mV/s after 1800 s OCP; triplicates. (huo2025modulatingheatinput pages 4-5) | Increasing heat input coarsened grains from 38.26 to 74.62 µm and reduced hardness from 192.4 ± 6.9 to 166.9 ± 0.3 HV. Corrosion-current densities increased monotonically: 2.56 ± 0.04, 3.85 ± 0.11, 5.03 ± 0.08, and 7.52 ± 0.07 µA/cm²; reported corrosion potentials were −269.61 ± 40, −466.62 ± 10, −517.77 ± 20, and −700.94 ± 15 mV. Limitation: short electrochemical tests, no long immersion or selective-attack depth, and γ₂ identification rests partly on SEM/EDS. (huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 7-10) |
| Dharmendra et al., *Additive Manufacturing* 30 (2019) 100872. DOI: [10.1016/j.addma.2019.100872](https://doi.org/10.1016/j.addma.2019.100872) | GMAW-based WAAM using AWS A5.7 ERCuNiAl, nominal Cu–9Al–4Fe–4Ni–1Mn; 114 A, 12.5 V, 480 mm/min, wire feed 6.5 m/min, estimated heat input 170 J/mm; 60 layers. (dharmendra2019microstructuralevolutionand pages 3-5, dharmendra2019microstructuralevolutionand pages 2-3) | No corrosion exposure. ASTM E8 room-temperature tensile tests; 3–5 specimens. | As-built WAAM: YS 388 ± 12 MPa, UTS 685 ± 10 MPa, elongation 26 ± 1%; cast comparator: 300 ± 15 MPa, 670 ± 8 MPa, and 16 ± 2%. No β′ was detected; the microstructure contained α, globular Fe₃Al κII, lamellar NiAl κIII, and 5–10 nm Fe-rich κIV. No serious weld-metal solidification or HAZ-liquation cracking was reported. Limitation: no quantified density/porosity and no corrosion testing. (dharmendra2019microstructuralevolutionand pages 5-7, dharmendra2019microstructuralevolutionand pages 13-14) |
| Berlanga-Labari et al., *Lubricants* 13 (2025) 290. DOI: [10.3390/lubricants13070290](https://doi.org/10.3390/lubricants13070290) | Cast NAB nominally CuAl10Fe5Ni5 and cast MAB C95700 nominally CuAl10Mn12Fe5; distinguishing measured contents were NAB 4.6Ni–1.2Mn and MAB 2.1Ni–12.8Mn. NAB contained 52.9% α, 32.3% β, and 14.3% κ; MAB contained 57.7% α, 30.4% β, and 11.8% κ. (berlangalabari2025theeffectof pages 2-4, berlangalabari2025theeffectof pages 4-7) | 1 M NaCl at room temperature; alumina-ball pin-on-disk at 10 or 40 N; 3600 s sliding; Pt counter and Ag/AgCl reference; polarization scan 0.1 mV/s. (berlangalabari2025theeffectof pages 2-4) | Static corrosion rate was approximately 0.02 mm/y and sliding rate approximately 0.1 mm/y. OCP was approximately −250 mV for NAB and −500 mV for MAB. Wear coefficients at 10 N were 5.5 × 10⁻⁶ (NAB) and 2.2 × 10⁻⁶ mm³/N·m (MAB); at 40 N they were 1.6 × 10⁻⁵ and 6.1 × 10⁻⁶ mm³/N·m. NAB showed pitting near small κ phases; MAB showed selective attack of large Fe/Mn-rich κ phases. Limitation: severe 1 M NaCl tribocorrosion, not quiescent seawater immersion or an AM deposit. (berlangalabari2025theeffectof pages 7-11, berlangalabari2025theeffectof pages 4-7) |
| Dobson, University of Bristol PhD dissertation (2024), *Corrosion Mechanisms and Fatigue Behaviour of Marine Biofouled Plasma Welded Nickel Aluminium Bronze*. DOI: not verified | Bead-on-plate plasma welding of cast NAB Cu–9.14Al–4.38Fe–4.84Ni–0.09Mn using 1.2 mm Cu6328/SIFMIG 44 wire; 250 °C preheat; no post-weld heat treatment. Weld and HAZ contained α + retained β′; HAZ width 0.96 ± 0.09 mm. (dobson2024corrosionmechanismsand pages 92-95, dobson2024corrosionmechanismsand pages 126-130, dobson2024corrosionmechanismsand pages 130-135) | Natural seawater at Millbay Marina, Plymouth, 1 m depth, 12 or 18 months; salinity 28.1–35.3 psu, 9.7–19.2 °C, pH 7.5–8.3. Comparator: ASTM D1141 simulated seawater, 12 or 18 months, 34.4–36.2 psu, 27.2–32.5 °C, pH 8.1–8.4. (dobson2024corrosionmechanismsand pages 92-95, dobson2024corrosionmechanismsand pages 95-100, dobson2024corrosionmechanismsand pages 130-135) | Simulated-seawater corrosion rate was 0.06 mm/y; natural seawater averaged about 10× higher, with 1.27 mm/y over the first 2 months and 0.11 mm/y over 12 months. Natural seawater caused β′ selective attack in the HAZ and κIII attack in stressed or biofouled crevices; maximum biofouling-pit depth was 986 µm and maximum κIII penetration was 1331 µm. A 12-month-corroded fatigue specimen tested at 182 MPa, R = 0.1, and 20 Hz failed at 2.5 × 10⁵ cycles; corrosion features extended approximately 1.3 mm below the surface. Limitation: dissertation, natural environment not controlled for flow, and no wrought C71500 comparator. (dobson2024corrosionmechanismsanda pages 235-240, dobson2024corrosionmechanismsand pages 154-157, dobson2024corrosionmechanismsand pages 100-107, dobson2024corrosionmechanismsand pages 122-126) |


*Table: Comparison of the strongest quantitative evidence on deposited or welded aluminum bronzes and NAB, including process chemistry, exposure conditions, corrosion, defects, and mechanical benchmarks. Limitations identify where each study does not directly represent single-stream blown-powder DED repair.*

Two details sharpen the interpretation of those benchmarks. First, **Zhao and coauthors’ 2022 laser studies are directly relevant prior art for *pre-alloyed, blown-powder NAB***, not examples of elemental-powder blending: the mechanical study used **Cu–10.80Al–4.10Fe–4.73Ni**, **45–100 µm** spherical powder with reported **0.025 wt% O** on 17-4PH steel. Its coatings measured **204–266 HV₀.₂**; dye penetrant found no major surface cracks or pores, but the lowest-energy specimen had an approximately **40 µm** interfacial hole/lack-of-fusion defect. It did not report a numerical bulk density, Hall flow, apparent powder density, corrosion test or C71500 comparison. **Full citation:** L. Zhao, B. Du, J. Yao, H. Chen, R. Ding and K. Li, “Microstructure and Mechanical Properties of Nickel-Aluminum Bronze Coating on 17-4PH Stainless Steel by Laser Cladding,” *Chinese Journal of Mechanical Engineering* **35**, 140 (2022), DOI **10.1186/s10033-022-00807-z**. **Process:** blown-powder laser cladding/laser direct deposition. **Tags:** [CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]—pre-alloyed NAB powder laser deposition already exists; [GAP]—no long-term seawater test. (zhao2022microstructureandmechanical pages 1-2, zhao2022microstructureandmechanical pages 2-4, zhao2022microstructureandmechanical pages 4-6)

Second, the *Metals* laser-deposition corrosion comparison used **the same nominal Cu–10.8Al–4.1Ni–4.0Fe powder** for the NAB layer, but its improved N-2/N-3 results arose partly from **separate Ni–Al or Ni–Cr interlayers and resultant compositional dilution**. In N-1, the upper deposited region averaged **11.2 wt% Fe** through steel dilution, and attacked Fe-rich dendrites contained approximately **56.1 wt% Fe locally**. Neither value establishes an intrinsic **11 wt% bulk-Fe cracking threshold** for a single powder deposited on NAB. After **21 days in 3.5 wt% NaCl**, maximum sectioned attack depths were **3.4 ± 0.1, 2.0 ± 0.1 and 1.8 ± 0.1 µm** for N-1/N-2/N-3, respectively; corresponding short-test *i*₍corr₎ values were **7.82, 4.65 and 4.09 µA cm⁻²**. **Full citation:** L. Zhao, K. Li, J. Yao, Y. Yuan and B. Du, “The Laser Deposited Nickel-Aluminum Bronze Coatings on SUS630 Stainless Steel and Its Corrosion Resistance in 3.5 wt.% NaCl Solution,” *Metals* **12**, 781 (2022), DOI **10.3390/met12050781**. **Process:** pre-alloyed blown-powder laser deposition on SUS630, with or without separately deposited interlayers. **Tags:** [CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]—powder NAB and corrosion already studied; [GAP]—not single-feed alloy design on NAB or Cu–Ni, and not natural seawater. (zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 1-2, zhao2022thelaserdeposited pages 2-4, zhao2022thelaserdeposited pages 4-7)

## Filler-metal evidence and its limits

- **ERCuNiAl:** C. Dharmendra, A. Hadadzadeh, B. S. Amirkhiz, G. D. Janaki Ram and M. Mohammadi, “Microstructural evolution and mechanical behavior of nickel aluminum bronze Cu-9Al-4Fe-4Ni-1Mn fabricated through wire-arc additive manufacturing,” *Additive Manufacturing* **30**, 100872 (2019), DOI **10.1016/j.addma.2019.100872**. **Process:** GMAW-based wire-arc DED, ERCuNiAl, nominal Cu–9Al–4Fe–4Ni–1Mn; approximately **170 J mm⁻¹**. Its as-built bar gave **388 ± 12 MPa yield**, **685 ± 10 MPa ultimate strength** and **26 ± 1% elongation** versus **300 ± 15 MPa**, **670 ± 8 MPa** and **16 ± 2%** for its cast comparison. The authors report no serious weld-metal solidification or HAZ-liquation cracking; **no seawater conditions, corrosion current, density or quantified porosity were reported**. This establishes *feasibility at one chemistry and thermal history*, not an Al/Fe cracking boundary. **Tags:** [CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]—as-built NAB wire DED and phase control are prior art; [GAP]—no corrosion qualification. (dharmendra2019microstructuralevolutionand pages 3-5, dharmendra2019microstructuralevolutionand pages 13-14, dharmendra2019microstructuralevolutionand pages 2-3)
- **ERCuNiAl, higher-Fe wire:** R. Huo *et al.*, “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing,” *Materials* **18**, 2205 (2025), DOI **10.3390/ma18102205**. **Process:** CMT wire-arc DED on Cu; wire **Cu–8.73Al–5.90Fe–4.52Ni–1.39Mn**. **Test:** aerated **3.5 wt% NaCl**, **25 ± 5 °C**, **3600 s** initial OCP, saturated calomel reference. From **243.8 to 644.7 J mm⁻¹**, grain size rose **38.26→74.62 µm**, measured surface hardness fell **192.4→166.9 HV**, and *i*₍corr₎ rose **2.56 ± 0.04→7.52 ± 0.07 µA cm⁻²**. These are *heat-input effects at one nominal wire composition*, not evidence that **5.9% Fe** causes or prevents cracking; no long immersion or attack depth was reported. **Tags:** [CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]—direct as-deposited processing–corrosion relationship; [GAP]—no powder or natural-seawater qualification. (huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 7-10)
- **ERCuAl-A2:** J. Wang, C. C. de Castro and X. Lu, “The Formation Mechanisms and Improvement Measures for Penetrating Cracks in QAl9-4/Q345B Welded Joint,” *Journal of Materials Engineering and Performance* **29**, 2346–2354 (2020), DOI **10.1007/s11665-020-04749-2**. **Process:** GTAW with ERCuAl-A2 versus SMAW with **a different T307 consumable**, joining bronze **Cu–9.7Al–3.40Fe–0.037Ni** to steel. SMAW with **150 °C** preheat produced transverse cracks and voids; GTAW/A2 with **200 °C** preheat produced a radiographically sound joint. Strength/elongation changed from **337.4 MPa/2.1%** to **436.5 MPa/18.2%**. Critically, the cracked joint involved Cu penetration at the **steel** interface, and its bronze had **0.126 wt% Pb**, well above the **>0.03 wt% Pb** level discussed as favoring low-melting constituents. Simultaneous changes in consumable, process and preheat prevent attributing the improvement to an A2 composition threshold. **Seawater:** not tested. **Tags:** [CITE] [NUMBERS] [GAP]—no controlled bronze-on-bronze filler ranking. (wang2020theformationmechanisms pages 1-6, wang2020theformationmechanisms pages 6-12)
- **ERCuAl-A2, historical surfacing:** P. B. Davis, *Surfacing Steel with Aluminum Bronze by the Submerged Arc Welding Process* (1974 thesis; **no DOI verified**). **Process:** submerged-arc surfacing of 1020 steel with ECuAl-A2, not laser DED. Flux moisture and excessive slag cover promoted porosity; changing voltage, penetration and dilution changed soundness, while weaving produced cracking. The thesis warns that **>10% iron dilution** impairs mechanical/corrosion properties and reports a low-dilution procedure; these are **steel-overlayer dilution observations, not an intrinsic 10 wt% Fe limit for NAB powder**. **Seawater test:** none documented in the cited sections. **Tags:** [CITE] [NAVY] [GAP]—not directly transferable to single-powder NAB repair. (davis1974surfacingsteelwith pages 12-17, davis1974surfacingsteelwith pages 52-57, davis1974surfacingsteelwith pages 162-172)

**ERCuAl-A1, ERCuAl-A3 and ERCuMnNiAl:** A defensible *head-to-head experimental ranking* against A2 and ERCuNiAl—with actual deposited wt% Al/Fe, restrained cracking, pore fraction and phase-resolved seawater attack—was **not established by the accessible studies**. Consequently, assigning A1/A2/A3 or ERCuMnNiAl a numerical “safe” Al/Fe cutoff would be unsupported. Their nominal filler designations should not be substituted for measured post-dilution deposit compositions. (dharmendra2019microstructuralevolutionand pages 2-3, wang2020theformationmechanisms pages 6-12, nemani2024advancementsinadditive pages 60-62)

## Corrosion evidence that changes the screening criterion

**T. H. E. Dobson, *Corrosion Mechanisms and Fatigue Behaviour of Marine Biofouled Plasma Welded Nickel Aluminium Bronze*, University of Bristol PhD dissertation (2024); dissertation DOI not verified.** **Process:** plasma *wire* weld on cast **Cu–9.14Al–4.38Fe–4.84Ni–0.09Mn**, Cu6328/SIFMIG 44 filler, **250 °C** preheat, **no post-weld heat treatment**. Weld/HAZ retained α+β′; measured HAZ width was **0.96 ± 0.09 mm**. **Tests:** natural Millbay Marina seawater at **1 m depth**, **12 and 18 months** (seasonally **9.7–19.2 °C; 28.1–35.3 psu; pH 7.5–8.3**), versus ASTM **D1141** simulated seawater for the same intervals (**27.2–32.5 °C; 34.4–36.2 psu**). This was a sheltered marina exposure, *not a stated controlled-flow test*. The simulated-seawater rate was **0.06 mm year⁻¹**; natural seawater gave **1.27 mm year⁻¹** during an initial two-month exposure, **0.11 mm year⁻¹** over 12 months, and approximately **tenfold higher average loss** over the longer comparison. β′ in the weld/HAZ selectively corroded; stressed or biofouled areas outside the HAZ showed κIII attack to a maximum **1331 µm**, versus maximum biofouling-associated pit depth **986 µm**. The thesis reports funding by **EPSRC and Babcock**, not ONR. Its marine/defence relevance does *not* make the experiment Navy-funded. **Tags:** [CITE] [NUMBERS] [NAVY]—defence component/application; [NOVELTY-RISK]—as-welded phase-specific seawater failure is known; [GAP]—no optimized single-stream powder DED or C71500 comparator. (dobson2024corrosionmechanismsand pages 1-6, dobson2024corrosionmechanismsand pages 154-157, dobson2024corrosionmechanismsand pages 92-95, dobson2024corrosionmechanismsand pages 95-100, dobson2024corrosionmechanismsand pages 100-107, dobson2024corrosionmechanismsand pages 122-126, dobson2024corrosionmechanismsand pages 130-135)

**C. Berlanga-Labari, A. Claver, M. V. Biezma-Moraleda and J. Fernández-Palacio, “The Effect of Kappa Phases on Tribocorrosion Behaviour of Nickel Aluminum Bronze (NAB) and Manganese Aluminum Bronze (MAB),” *Lubricants* **13**, 290 (2025), DOI 10.3390/lubricants13070290.** **Process:** *cast*, not AM; nominal **CuAl10Fe5Ni5 NAB** versus **CuAl10Mn12Fe5 MAB**, with reported NAB **4.6Ni/1.2Mn** and MAB **2.1Ni/12.8Mn** wt%. **Test:** **1 M NaCl**, room temperature, alumina-ball sliding at **10 or 40 N for 3600 s**, Ag/AgCl reference; this solution is *not ASTM D1141 or natural seawater*. Static corrosion was approximately **0.02 mm year⁻¹**, rising to about **0.1 mm year⁻¹** with sliding; OCPs were approximately **−250 mV NAB** and **−500 mV MAB**. NAB pitted near smaller κ constituents; **lower-Ni MAB showed selective attack of larger Fe/Mn-rich κ constituents**. Thus replacing Ni with Mn is not, by itself, a corrosion-safe design rule. Figure 6 displays the static/sliding comparison. **Tags:** [CITE] [NUMBERS] [NAVY]—naval propulsion context; [GAP]—no deposited specimens or natural-seawater immersion. (berlangalabari2025theeffectof pages 7-11, berlangalabari2025theeffectof pages 2-4, berlangalabari2025theeffectof media f994da44, berlangalabari2025theeffectof pages 4-7)

**Additional laser/LPBF boundary checks.** The Zhao *Chinese Journal of Mechanical Engineering* powder-cladding study above establishes that a dense-looking laser coating is technically possible yet may contain a local lack-of-fusion hole, while Zhao *Metals* establishes that Fe-enriched *substrate dilution* can dominate its short-term corrosion. C. Guerra, J. A. Ramos-Grez, I. La Fé-Perdomo, A. Castillo and M. Walczak, “Microstructure and Mechanical Properties of Cu-11Al-5Ni-4Fe wt% Manufactured by LPBF,” *Metals* **13**, 459 (2023), DOI **10.3390/met13030459**, reports **nitrogen-atomized powder <40 µm** (median **<17 µm**), approximately **97.5% relative density** and as-built martensitic microstructure; it provides **no seawater corrosion comparison**. **Process:** LPBF, **not blown-powder DED**. [CITE] [NUMBERS] [GAP]. An AM literature review also reports earlier Cu–9Al–5Fe–5Ni laser-metal deposition with β′/Widmanstätten α and mechanical properties, but the original study’s bibliographic DOI and methods were not independently verified here; it should **not** be claimed as a newly demonstrated corrosion-qualified powder repair. (zhao2022microstructureandmechanical pages 1-2, zhao2022microstructureandmechanical pages 4-6, nemani2024advancementsinadditive pages 79-83, guerra2023microstructureandmechanical pages 2-4)

## Proposed *experimental* composition window—not a certified safe window

For a **lower-Ni, α-first aluminum-bronze branch**, investigate roughly **Cu–7–8.5Al–1–3Fe–0–2Ni–0–1Mn (wt%, balance Cu)**, with measured powder and diluted-deposit chemistry rather than target melt chemistry used in acceptance decisions. The upper Al edge deliberately probes the nonequilibrium onset of β in nearly binary bronze; the Fe choice stays below the **slow-cooled κI association around 5% Fe**. Those numbers define a **screening domain inferred from phase evidence**, *not* experimentally proven limits on cracking, porosity or marine corrosion. An α-rich deposit may also sacrifice the strength/wear resistance of conventional NAB; its HAZ on a **Cu–9Al–4Fe–4Ni** cast substrate can still become β′-rich. Retain a conventional **Cu–8.5–9.5Al–3.5–4.5Fe–4–5Ni–approximately 1Mn** NAB branch as the repair/strength control, but **reject any as-deposited condition exhibiting connected β/β′, continuous κIII-linked attack, unacceptable HAZ attack or γ₂**, rather than assuming its traditional chemistry is seawater-safe without heat treatment. A low-Ni, high-Mn duplex MAB is a *comparison*, not the presumed answer. None of the cited bronze studies proves equivalence to wrought **70–30 Cu–Ni C71500** under matched seawater flow and duration. (dharmendra2019microstructuralevolutionand pages 1-2, kuprienko2025analysisofnickela pages 36-41, dobson2024corrosionmechanismsand pages 1-6, dobson2024corrosionmechanismsand pages 154-157, dharmendra2019microstructuralevolutionand pages 2-3, berlangalabari2025theeffectof pages 4-7)

For the proposal, test **single pre-alloyed powder lots** on themselves, cast NAB and wrought Cu–Ni; measure deposit *and interface* composition, powder size/flow/apparent density/O, volumetric pores and cracks, and phase *identity and connectivity*. Use short electrochemistry as a screening node, then **matched C71500 controls and 30-day immersion** in explicitly specified natural or ASTM D1141 seawater, including polished-section maximum selective-attack depth. Add controlled flow or a stated static control: polarization current alone cannot validate the service claim. Compare CALPHAD run **along the modeled thermal/reheat history** against equilibrium-only predictions, especially for β′ and κIII in each reheated layer and substrate HAZ. The missing quantitative crack threshold and joint density–phase–natural-seawater map are the opportunity; previous pre-alloyed powder laser cladding means *making a NAB coating alone is not novel*. (dobson2024corrosionmechanismsand pages 1-6, dobson2024corrosionmechanismsand pages 154-157, dobson2024corrosionmechanismsand pages 92-95, dharmendra2019microstructuralevolutionand pages 5-7, zhao2022microstructureandmechanical pages 2-4, zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 2-4)

## Top 5 things the PI should know

1. **Treat the as-deposited HAZ as a primary corrosion outcome.** Plasma-welded NAB retained selectively attacked β′ even without post-weld treatment; under biofouled acidic crevices, connected κIII attack reached **1.331 mm**. (dobson2024corrosionmechanismsand pages 154-157, dobson2024corrosionmechanismsand pages 130-135)
2. **Do not advertise a proven Al/Fe “no-crack, no-dealloying” threshold.** Approximately **8–9.4% Al** describes context-dependent phase changes; **~5% Fe** concerns coarse κI under slow cooling, not a validated DED crack cutoff. (dharmendra2019microstructuralevolutionand pages 1-2, kuprienko2025analysisofnickela pages 36-41, davis1974surfacingsteelwith pages 12-17)
3. **Pre-alloyed NAB blown-powder laser deposition and NaCl corrosion are already prior art.** Differentiate through *new composition–powder–deposit–interface* optimization, matched natural-seawater/C71500 testing and no post-build heat treatment—not by claiming first NAB powder cladding. (zhao2022microstructureandmechanical pages 1-2, zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 2-4)
4. **Short NaCl results can mis-rank service performance.** In the welded-NAB study, ASTM D1141 tank exposure gave **0.06 mm year⁻¹**, while natural seawater caused substantially greater and more localized damage; low-Ni MAB also showed κ-selective attack under sliding. (dobson2024corrosionmechanismsand pages 154-157, dobson2024corrosionmechanismsand pages 100-107, berlangalabari2025theeffectof pages 4-7)
5. **Differentiate real process defects from composition limits.** One low-energy powder-clad specimen had an approximately **40 µm** hole; steel dilution produced anodic Fe-rich dendrites; the A2 comparison changed process, filler and preheat together. None measures a transferable intrinsic filler-metal porosity or hot-cracking threshold. (wang2020theformationmechanisms pages 6-12, zhao2022microstructureandmechanical pages 4-6, zhao2022thelaserdeposited pages 4-7)

References

1. (dharmendra2019microstructuralevolutionand pages 1-2): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

2. (dobson2024corrosionmechanismsand pages 1-6): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

3. (dobson2024corrosionmechanismsand pages 130-135): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

4. (dharmendra2019microstructuralevolutionand pages 5-7): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

5. (davis1974surfacingsteelwith pages 12-17): PB Davis. Surfacing steel with aluminum bronze by the submerged arc welding process. Unknown journal, 1974.

6. (davis1974surfacingsteelwith pages 24-30): PB Davis. Surfacing steel with aluminum bronze by the submerged arc welding process. Unknown journal, 1974.

7. (kuprienko2025analysisofnickel pages 18-23): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

8. (kuprienko2025analysisofnickela pages 36-41): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

9. (dharmendra2019microstructuralevolutionand pages 9-13): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

10. (wang2020theformationmechanisms pages 1-6): Jian Wang, Camila Caroline de Castro, and Xiaofeng Lu. The formation mechanisms and improvement measures for penetrating cracks in qal9-4/q345b welded joint. Journal of Materials Engineering and Performance, 29:2346-2354, Mar 2020. URL: https://doi.org/10.1007/s11665-020-04749-2, doi:10.1007/s11665-020-04749-2. This article has 3 citations and is from a peer-reviewed journal.

11. (dharmendra2019microstructuralevolutionand pages 2-3): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

12. (wang2020theformationmechanisms pages 6-12): Jian Wang, Camila Caroline de Castro, and Xiaofeng Lu. The formation mechanisms and improvement measures for penetrating cracks in qal9-4/q345b welded joint. Journal of Materials Engineering and Performance, 29:2346-2354, Mar 2020. URL: https://doi.org/10.1007/s11665-020-04749-2, doi:10.1007/s11665-020-04749-2. This article has 3 citations and is from a peer-reviewed journal.

13. (zhao2022microstructureandmechanical pages 4-6): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

14. (berlangalabari2025theeffectof pages 2-4): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

15. (dobson2024corrosionmechanismsand pages 154-157): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

16. (dobson2024corrosionmechanismsand pages 122-126): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

17. (zhao2022thelaserdeposited pages 2-4): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

18. (zhao2022thelaserdeposited pages 4-7): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

19. (zhao2022thelaserdeposited pages 7-10): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

20. (zhao2022thelaserdeposited pages 10-13): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

21. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

22. (huo2025modulatingheatinput pages 2-4): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

23. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

24. (huo2025modulatingheatinput pages 7-10): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

25. (dharmendra2019microstructuralevolutionand pages 3-5): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

26. (dharmendra2019microstructuralevolutionand pages 13-14): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

27. (berlangalabari2025theeffectof pages 4-7): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

28. (berlangalabari2025theeffectof pages 7-11): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

29. (dobson2024corrosionmechanismsand pages 92-95): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

30. (dobson2024corrosionmechanismsand pages 126-130): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

31. (dobson2024corrosionmechanismsand pages 95-100): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

32. (dobson2024corrosionmechanismsanda pages 235-240): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

33. (dobson2024corrosionmechanismsand pages 100-107): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

34. (zhao2022microstructureandmechanical pages 1-2): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

35. (zhao2022microstructureandmechanical pages 2-4): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

36. (zhao2022thelaserdeposited pages 1-2): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

37. (davis1974surfacingsteelwith pages 52-57): PB Davis. Surfacing steel with aluminum bronze by the submerged arc welding process. Unknown journal, 1974.

38. (davis1974surfacingsteelwith pages 162-172): PB Davis. Surfacing steel with aluminum bronze by the submerged arc welding process. Unknown journal, 1974.

39. (nemani2024advancementsinadditive pages 60-62): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

40. (berlangalabari2025theeffectof media f994da44): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

41. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

42. (guerra2023microstructureandmechanical pages 2-4): Carolina Guerra, Jorge A. Ramos-Grez, Iván La Fé-Perdomo, Alejandro Castillo, and Magdalena Walczak. Microstructure and mechanical properties of cu-11al-5ni-4fe wt% manufactured by lpbf. Metals, 13:459, Feb 2023. URL: https://doi.org/10.3390/met13030459, doi:10.3390/met13030459. This article has 11 citations.
