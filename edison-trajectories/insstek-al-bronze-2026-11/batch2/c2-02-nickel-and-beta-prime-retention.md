<!--
Edison Scientific LITERATURE task (batch 2)
- Task ID: 6334bbd3-596a-423c-84d0-58baf16486b0
- Submitted: 2026-11-10T16:31:14Z
- Fetched: 2026-11-10T17:02:12Z (status: success)
- Raw trajectory JSON: ../raw/c2-02-nickel-and-beta-prime-retention.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications)
submitted an ONR FY2027 Young Investigator Program proposal in October 2026 to
design new pre-alloyed copper alloy powders for single-stream blown-powder
laser directed energy deposition (DED). Goals: deposits that are dense and
crack-free, built on themselves and deposited on cast nickel-aluminum bronze
(NAB, UNS C95800) and wrought Cu-Ni (repair), that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). The searched space is Cu at least 65 wt% with Ni 0-30,
Al 0-9.5 (upper bound set by retained beta-prime martensite as deposited),
Fe 0-4.5, Mn 0-4, Ti 0-0.5, plus Cr, Si, Nb in Cu-Ni only, with NAB family
rules (above 7 Al: Fe <= Ni <= 5.5). Powder is made in-house by ultrasonic
atomization (AMAZEMET rePOWDER, 40 kHz, induction melting up to 1300 C); the
first copper alloy run uses UNS C63000 bar (Cu-10Al-5Ni-3Fe). Blown-powder DED
is bought at the University of Utah (InssTek MX-Lab: InssTek DMT process,
ytterbium fiber laser of 500 W maximum, 0.4 mm beam, six powder feeders,
45-150 um powder) and at the Colorado School of Mines (FormAlloy X2).
InssTek's material database (summarized for the PI by InssTek) lists
"Al-Bronze / UNS C95300" as a qualified DED material: Cu balance, Al 9-11 wt%,
Fe 0.8-1.5 wt% (no nickel); typical powder size average about 83.8 um;
melting range 1040-1045 C; applications listed as ship propellers and marine
components; tensile strength of InssTek DMT-produced material 628 MPa (XY) and
598 MPa (Z). The database summary gives no yield strength, elongation,
hardness, heat treatment, laser power, machine model or corrosion data.

QUESTION: In laser DED, laser cladding, LPBF, laser surface melting and
welding of aluminum bronzes, how much retained beta / martensitic
beta-prime forms as deposited, and how does it depend on Al, Ni, Fe and Mn
and on cooling rate and layer reheating? Specifically compare nickel-free
Cu-(9-11)Al-(1-4)Fe (C95300, C95400, CuAl10Fe) with NAB containing 4-5.5 wt%
Ni (C63000 Cu-10Al-5Ni-3Fe, C95800, C63200) processed the same way. Report
measured beta-prime fractions (XRD, EBSD, image analysis), martensite start
temperatures and their composition dependence, the eutectoid temperature and
composition shifts caused by Ni and Fe, critical cooling rates for retaining
beta, and how multi-layer reheating in DED tempers beta-prime into alpha +
kappa (or alpha + gamma-2 without Ni). Include laser-DED NAB results from
Southeast University (G. Sun, Z. Wang and co-workers), Muller et al. 2023
(IOP Conf. Ser. 1296, 012036; needle-like beta-prime at 1300 W), Doyle 2022
(wire-laser C95800), Murray et al. 2020 (LPBF NAB), Hyatt et al. 1998 (laser
clad NAB), and any nickel-free laser work. Is a Cu-10Al-5Ni-3Fe (C63000)
powder deposited by blown-powder DED at 300-500 W likely to be as
beta-prime-rich as nickel-free C95300?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition /
InssTek DMT, wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought,
weld overlay), the alloy composition in wt%, the condition (as deposited,
heat treated: temperature and time), the test conditions (e.g. 3.5 wt% NaCl
vs natural or substitute seawater per ASTM D1141, duration, flow), and the key
numbers (porosity/density, phase fractions, corrosion current density or rate,
Ecorr, selective-attack depth, hardness, UTS/yield/elongation with direction,
laser power/spot/speed/feed, powder size/flow/oxygen). Tag each item: [CITE]
worth citing; [NUMBERS] gives a quantitative benchmark; [NAVY] Navy/DoD-funded
or Navy application; [INSSTEK] made on an InssTek machine or by InssTek;
[GAP] shows something not yet done. If the literature does not answer part of
the question, say so plainly instead of padding with loosely related work.
End with a ranked "Top 5 things the PI should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications)
submitted an ONR FY2027 Young Investigator Program proposal in October 2026 to
design new pre-alloyed copper alloy powders for single-stream blown-powder
laser directed energy deposition (DED). Goals: deposits that are dense and
crack-free, built on themselves and deposited on cast nickel-aluminum bronze
(NAB, UNS C95800) and wrought Cu-Ni (repair), that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). The searched space is Cu at least 65 wt% with Ni 0-30,
Al 0-9.5 (upper bound set by retained beta-prime martensite as deposited),
Fe 0-4.5, Mn 0-4, Ti 0-0.5, plus Cr, Si, Nb in Cu-Ni only, with NAB family
rules (above 7 Al: Fe <= Ni <= 5.5). Powder is made in-house by ultrasonic
atomization (AMAZEMET rePOWDER, 40 kHz, induction melting up to 1300 C); the
first copper alloy run uses UNS C63000 bar (Cu-10Al-5Ni-3Fe). Blown-powder DED
is bought at the University of Utah (InssTek MX-Lab: InssTek DMT process,
ytterbium fiber laser of 500 W maximum, 0.4 mm beam, six powder feeders,
45-150 um powder) and at the Colorado School of Mines (FormAlloy X2).
InssTek's material database (summarized for the PI by InssTek) lists
"Al-Bronze / UNS C95300" as a qualified DED material: Cu balance, Al 9-11 wt%,
Fe 0.8-1.5 wt% (no nickel); typical powder size average about 83.8 um;
melting range 1040-1045 C; applications listed as ship propellers and marine
components; tensile strength of InssTek DMT-produced material 628 MPa (XY) and
598 MPa (Z). The database summary gives no yield strength, elongation,
hardness, heat treatment, laser power, machine model or corrosion data.

QUESTION: In laser DED, laser cladding, LPBF, laser surface melting and
welding of aluminum bronzes, how much retained beta / martensitic
beta-prime forms as deposited, and how does it depend on Al, Ni, Fe and Mn
and on cooling rate and layer reheating? Specifically compare nickel-free
Cu-(9-11)Al-(1-4)Fe (C95300, C95400, CuAl10Fe) with NAB containing 4-5.5 wt%
Ni (C63000 Cu-10Al-5Ni-3Fe, C95800, C63200) processed the same way. Report
measured beta-prime fractions (XRD, EBSD, image analysis), martensite start
temperatures and their composition dependence, the eutectoid temperature and
composition shifts caused by Ni and Fe, critical cooling rates for retaining
beta, and how multi-layer reheating in DED tempers beta-prime into alpha +
kappa (or alpha + gamma-2 without Ni). Include laser-DED NAB results from
Southeast University (G. Sun, Z. Wang and co-workers), Muller et al. 2023
(IOP Conf. Ser. 1296, 012036; needle-like beta-prime at 1300 W), Doyle 2022
(wire-laser C95800), Murray et al. 2020 (LPBF NAB), Hyatt et al. 1998 (laser
clad NAB), and any nickel-free laser work. Is a Cu-10Al-5Ni-3Fe (C63000)
powder deposited by blown-powder DED at 300-500 W likely to be as
beta-prime-rich as nickel-free C95300?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition /
InssTek DMT, wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought,
weld overlay), the alloy composition in wt%, the condition (as deposited,
heat treated: temperature and time), the test conditions (e.g. 3.5 wt% NaCl
vs natural or substitute seawater per ASTM D1141, duration, flow), and the key
numbers (porosity/density, phase fractions, corrosion current density or rate,
Ecorr, selective-attack depth, hardness, UTS/yield/elongation with direction,
laser power/spot/speed/feed, powder size/flow/oxygen). Tag each item: [CITE]
worth citing; [NUMBERS] gives a quantitative benchmark; [NAVY] Navy/DoD-funded
or Navy application; [INSSTEK] made on an InssTek machine or by InssTek;
[GAP] shows something not yet done. If the literature does not answer part of
the question, say so plainly instead of padding with loosely related work.
End with a ranked "Top 5 things the PI should know" list.


# Retained β′ in laser-processed aluminum bronzes

**Bottom line.** Laser processing can leave substantial martensitic material in **both** nickel-free Cu–Al–Fe and 4–5 wt% Ni aluminum bronze (NAB). The available studies do **not** establish that C63000 deposited at 300–500 W will be less β′-rich than nickel-free C95300 deposited with the same machine and thermal history. Nor do they give a defensible percentage difference: the relevant laser studies generally identify phases qualitatively, not by calibrated whole-deposit phase-fraction measurements. Moreover, a dark etched constituent, an XRD peak, and a TEM-identified martensite are not interchangeable evidence. (muller2023usingultrasonicatomization pages 8-12, li2021nanotwinscontainingmicrostructureand pages 9-14, kuprienko2025analysisofnickel pages 45-50, kuprienko2025analysisofnickela pages 45-50)

All compositions below are **wt%**; Cu is the balance unless otherwise stated. “As deposited” means no separate post-build heat treatment, **not** that underlying layers escaped reheating. Tags denote [CITE] useful primary evidence, [NUMBERS] quantitative benchmark, [NAVY] documented naval connection, [INSSTEK] demonstrated InssTek processing, and [GAP] an important unanswered comparison. **No cited experimental item was verified as made on an InssTek machine**; the supplied C95300 database entry is vendor information, not an independently characterized publication. No publications by the PI are used. (doyle2022additivemanufacturingof pages 47-53, muller2023usingultrasonicatomization pages 8-12, li2021nanotwinscontainingmicrostructureand pages 1-4)

## Transformation rules and what has actually been measured

At approximately 9–11% Al, the question is first **how much high-temperature β remains available to transform**: α formation and Al-consuming Fe-/Ni-rich precipitates change that amount before the material reaches its martensite-start temperature, *M*ₛ. Rapid passage through transformation windows favors retained β-derived martensite; greater heat input, slower effective cooling, or reheating of earlier layers can instead increase α and promote decomposition or precipitation. In nickel-free binary Cu–Al, slowly cooled β decomposes to **α + γ₂ (Cu₉Al₄)** at approximately **565 °C**. This binary temperature must not be applied unmodified to NAB: Ni and Fe sequester Al in κ precipitates and raise the Al content at which detrimental γ₂ develops; the commonly described NAB **α + NiAl-rich κIII** eutectoid formation spans approximately **800–660 °C**, depending on composition. These are different reactions/thermal histories, not a measured universal “Ni raises the eutectoid by 200 °C” coefficient. Mn affects transformation kinetics as well as composition. (konecna2012copperandcopper pages 25-27, fayanas2025nickelaluminiumbronze pages 1-2, kuprienko2025analysisofnickel pages 30-36)

**Measured or estimated phase fractions—not percentages inferred from photographs:**

* **Fayanas *et al.* (2025)**, “Nickel Aluminium Bronze Alloys With Enhanced Erosion-Corrosion Resistance And Mechanical Strength,” *J. Jpn. Soc. Powder Powder Metall.* **72**, S819–S826, DOI **10.2497/jjspm.15F-T13-08**. **Cast and powder-metallurgy/HIP**, not laser DED: cast 9.7Al–4.4Ni–4.3Fe–0.9Mn; sinter+HIP 10.0Al–5.0Ni–4.0Fe–1.0Mn. **EBSD β′:** **1% cast versus 4% sinter+HIP** before the separate **700 °C/2 h, slow-cool** anneal, which converted β′ toward α + κIII. These are useful *method* and thermal-history references, **not** measured DED fractions. Their reported initial relative densities are **99.2%** sinter+HIP and **99.9%** near-net-shape HIP. [CITE] [NUMBERS] [GAP] (fayanas2025nickelaluminiumbronze pages 2-5, fayanas2025nickelaluminiumbronze pages 1-2)
* **Jafari, Davoodi and Hosseinpour (2021)**, “Effect of Fluid Flow on the Corrosion Performance of as-Cast and Heat-Treated Nickel Aluminum Bronze Alloy (UNS C95800) in Saline Solution,” *Corrosion and Materials Degradation* **2**, 61–77, DOI **10.3390/cmd2010004**. **Cast** 8.79Al–4.50Ni–3.70Fe–1.00Mn, compared with **675 °C/6 h, air cooled**. Their **etched-image analysis**, rather than EBSD or diffraction refinement, assigned **β 20% → 7%** and **κ 33% → 66%** after annealing; the authors warn that finely structured κ may be overestimated. The figure labels the constituent **β**, so its percentages must not be presented as independently verified β′ crystallographic fractions. [CITE] [NUMBERS] [GAP] (jafari2021effectoffluid pages 2-4, jafari2021effectoffluid media a8b52b0c)
* **Kuprienko (2025)**, *Analysis of Nickel Aluminum Bronze Weld Metal Microstructure and Mechanical Response as a Function of Cooling Rate*, PhD dissertation, Ohio State University; **no verified DOI**. In **multilayer wire-arc DED** on wrought **C63200**, approximately 9Al–4Fe–4.5Ni–1Mn wire, image analysis assigned **α 70–84%, mean 77%**, in the initial deposit. **Do not subtract this number from 100 and call the remainder martensite**: electron microscopy identifies α plus κII/κIII in the dark intergranular material, not necessarily retained β′. The work acknowledges **Office of Naval Research Manufacturing Science Program** funding. [CITE] [NUMBERS] [NAVY] (kuprienko2025analysisofnickel pages 1-7, kuprienko2025analysisofnickel pages 67-72, kuprienko2025analysisofnickel pages 147-152, kuprienko2025analysisofnickel pages 152-158)

**Transformation temperatures and cooling rates.** Guerra *et al.* (2023), “Microstructure and Mechanical Properties of Cu-11Al-5Ni-4Fe wt% Manufactured by LPBF,” *Metals* **13**, 459, DOI **10.3390/met13030459**, measured DSC on **powder and as-built LPBF** Cu–11Al–5Ni–4Fe at **10 °C/min**: powder *M*ₛ **358.5 °C**; as-built specimens at **99, 125 and 198 J/mm³** respectively **366.4, 366.2 and 366.5 °C**, with *M*𝒻 **355.7, 354.0 and 341.8 °C**. DSC identifies a transformation on **subsequent controlled thermal cycling**; these values are not an in-situ measurement of the initial laser-cooling *M*ₛ, nor an experimentally determined Ni/Fe derivative. A separate approximately **170 °C** martensitic reaction attributed to NAB laser-clad simulations by Hyatt and coworkers is reported in Kuprienko’s critical review, but its dilatometric interpretation is **uncertain**; it is not a transferable *M*ₛ for C63000. [CITE] [NUMBERS] [GAP] (guerra2023microstructureandmechanical pages 8-10, kuprienko2025analysisofnickel pages 50-55)

**Sugiyama and Kobayashi (1961)**, “Effects of Nickel, Iron and Manganese Addition on β→α+γ₂ Transformation of Copper–Aluminium Alloys” [Japanese-language original; title translated], **journal and DOI not verified**. Their 900 °C/1 h homogenized, then **550–400 °C isothermally transformed** Cu–Al–Ni, Cu–Al–Fe and Cu–Al–Mn alloys produced TTT-derived estimates of the **critical cooling rate to *start* α+γ₂ formation**, not a measured critical rate for producing a specified whole-build β′ fraction. Near **12% Al**, Mn shifted the transformation nose from approximately **513 °C** without addition to **507 °C at 1.2% Mn**, **480 °C at 3% Mn**, and **450 °C at 5% Mn**. Corresponding table estimates for suppressing the *start* of that eutectoid are approximately **0.4, 0.15, 0.015 and 0.0007 °C/s**, respectively. The binary eutectoid is listed near **570 °C**; Mn-containing eutectoid temperatures fall to approximately **554, 523 and 483 °C**. Ni or Fe *individually* showed much smaller inhibition than Mn under these specific conditions. Their Al levels, ternary chemistries and reaction differ from 9–10% Al, Ni+Fe-containing NAB; these very low estimated rates are **not** a measured C63000 laser-DED quench threshold. [CITE] [NUMBERS] [GAP] (小林啓佑1961cual合金のβ→ pages 1-2, 小林啓佑1961cual合金のβ→ pages 3-4, 小林啓佑1961cual合金のβ→ pages 4-5)

Kuprienko’s **single-sensor thermal analysis** on NAB extracted from wire-arc DED measured **1000→800 °C cooling rates 139–424 °C/s**, versus **0.1 °C/s** furnace cooling. κII started at **947–974 °C** in Gleeble tests versus **1004 °C** after furnace cooling; κIII onset was **677–711 °C** versus **717 °C**. Fine κ persisted at hundreds of °C/s; these are **observed cooling rates, not a measured critical rate for zero κ or full martensite**. The thesis cautions that optical dark regions in comparable arc-deposited NAB were actually **α lamellae + κII + κIII** on TEM/diffraction. A separate laser-metal-deposition paper describes an **FCC-type β*** product, explicitly noting that its diffraction does not match all conventional β′ variants. Consequently, XRD indexing and EBSD phase libraries need validation by TEM before comparing fractions. [CITE] [NUMBERS] [NAVY] [GAP] (kuprienko2025analysisofnickel pages 131-137, kuprienko2025analysisofnickel pages 137-142, kuprienko2025analysisofnickel pages 45-50, li2021nanotwinscontainingmicrostructureand pages 9-14)

## Process-specific evidence: nickel-bearing and nickel-free

1. **Li, Zheng, Han and Zhou (2021)**, “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition,” *Additive Manufacturing* **39**, 101825, DOI **10.1016/j.addma.2020.101825**. **Blown-powder laser metal deposition**, nominal 9Al–5Fe–5Ni; measured powder **9.70 ± 0.89Al, 5.48 ± 0.86Fe, 4.47 ± 0.60Ni**. Gas-atomized **45–106 µm** powder, D₅₀ **76.29 µm**; **2-mm spot**, effective **1000–1500 W**, **0.5–1.5 m/min**, **1.5–2-mm hatch**. **As deposited**, relative density generally **>99%**, maximum **99.55%**; **750 W** produced lack-of-fusion pores and **2 m/min** could produce gas pores. TEM identified **β*** plates approximately **250 nm** wide, Widmanstätten α, Fe₃Al/NiAl and nanotwins; **no whole-build β*/β′ percentage or corrosion test**. Horizontal deposit-derived tensile samples: yield **593–713 MPa**, UTS **769–949 MPa**, elongation typically **10–12%**, with individual pore-affected specimens worse. The paper estimates the **DED cooling-rate regime 10³–10⁴ K/s**, rather than measuring a C63000-specific critical rate. Its funding is identified as a Singapore marine/offshore program, **not US Navy funding**. [CITE] [NUMBERS] [GAP] (li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 4-9, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 19-24)

2. **Müller, Fasselt, Kruse, Klötzer, Kleba-Ehrhardt, Choma, Biegler and Rethmeier (2023)**, “Using ultrasonic atomization to recycle aluminium bronze chips for additive laser directed energy deposition,” *IOP Conference Series: Materials Science and Engineering* **1296**, 012036, DOI **10.1088/1757-899X/1296/1/012036**. **Blown-powder laser DED**, *not* nickel-free bronze: ultrasonic-atomized **CuAl10Ni5Fe5** from propeller swarf versus a separately characterized **nickel-free CuAl9.5Fe reference powder**. The experimental **35-layer deposit used the Ni-bearing recycled powder** at **1300 W, 1-mm spot, 750 mm/min, 11 g/min**, on stainless steel; it is therefore **not** a matched deposited Ni/no-Ni comparison. The **40-kHz, 1300 °C rePOWDER** run gave **77% powder yield**, particle D₁₀/D₅₀/D₉₀ **45/96/179 µm**, **0.0125% oxygen** and Hausner ratio **1.05**; the nickel-free commercial powder gave **63/91/133 µm**, **0.0196% oxygen** and **1.12**. **As-deposited Ni-bearing** block: **>99.8% dense**, needle-like structure *interpreted* as predominantly β′, **266 HV**, XY yield **646 MPa**, UTS **911 MPa**, elongation approximately **9%**; **no XRD/EBSD β′ fraction or corrosion test**. This result directly disproves the categorical claim that ≈5% Ni prevents a martensitic-looking multilayer laser DED deposit. Unlike the proposed small 45–150-µm feeder window, this atomized batch included a substantial >150-µm tail. [CITE] [NUMBERS] [GAP] (muller2023usingultrasonicatomization pages 3-6, muller2023usingultrasonicatomization pages 8-12)

3. **Doyle (2022)**, *Additive Manufacturing of FeCrCoCuNi High Entropy Alloy via Laser Powder Bed Fusion and Nickel Aluminum Bronze via Laser Directed Energy Deposition*, MS thesis, Oregon State University, **no verified DOI**. **Wire-laser DED, MELTIO M450—not blown-powder DED or InssTek**; C95800 wire **8.64Al–4.21Ni–3.19Fe–1.32Mn**, 0.89-mm diameter; **six 976-nm diode lasers**, 0.9-mm spot. **As deposited** four selected builds: **800 W/300 mm min⁻¹ → 99.84%**, **1000 W/600 → 99.58%**, **1200 W/600 → 99.89%**, **1200 W/900 → 99.61%** density. Micrographs show α and darker material called martensitic β; κ and β assignments from XRD/SEM are **not quantitative**. As deposited: yield **410.5 ± 6.3 MPa**, UTS **757.8 ± 5.4 MPa**, elongation **29.0 ± 1.0%**, **218.8 ± 4.4 HV**. After **675 °C/6 h, furnace cool**: **372.2 ± 6.7 MPa**, **714.5 ± 8.3 MPa**, **31.2 ± 0.25%**, **204.1 ± 3.1 HV**. **No seawater test**; the thesis acknowledges a Navy grant. **Important discrepancy:** it interprets some post-anneal images/XRD as *more*, not less, β-like material; do not claim this study quantitatively demonstrates β′ decomposition. [CITE] [NUMBERS] [NAVY] [GAP] (doyle2022additivemanufacturingof pages 47-53, doyle2022additivemanufacturingof pages 53-58)

4. **Huang, Fu, Wang, Xiao, Sun, Wang and Nie (2026)**, “Densification Behavior and Microstructure of Nickel Aluminum Bronze Alloy Fabricated by Laser Powder Bed Fusion,” *Materials* **19**, 208, DOI **10.3390/ma19010208**. **LPBF, not DED**: measured powder **9.9Al–4.3Ni–4.5Fe–1.4Mn**, D₅₀ **38.9 µm**—**its Al exceeds the stated 9.5% design limit**. At **300 W, 1000 mm/s, 0.11-mm hatch and 30-µm layers**, achieved **>99.9%** density within optimized conditions. **As built**, XRD/optical microscopy describe a **β′-dominated columnar structure** with boundary α and minor κ; no reported β′ percentage. **675 °C/6 h, furnace cool** removes the identified β′ XRD peaks and promotes α + κ. Horizontal tensile: as-built yield/UTS/elongation **509.76/1069.38 MPa/9.03%**; annealed **574.86/780.11 MPa/25.58%**; as-built hardness **341 HV**. **No corrosion result**. A coauthor is affiliated with the Naval University of Engineering; affiliation alone does **not** establish Navy/DoD funding. Note the paper inconsistently calls one as-built optical micrograph “30 W/100 mm/s” although its methods and other figure captions state **300 W/1000 mm/s**. [CITE] [NUMBERS] [GAP] (huang2026densificationbehaviorand pages 2-4, huang2026densificationbehaviorand pages 4-6, huang2026densificationbehaviorand pages 6-10, huang2026densificationbehaviorand pages 10-12)

5. **Guerra, Ramos-Grez, La Fé-Perdomo, Castillo and Walczak (2023)**, *Metals* **13**, 459, DOI **10.3390/met13030459**, cited above. **LPBF Cu–11Al–5Ni–4Fe**, as built, approximately **97.5%** relative density over approximately **90–210 J/mm³**. XRD and microscopy identify acicular β′ plus α/κ, **without Rietveld or EBSD β′ fraction**. Hardness approximately **140–180 HB**, depending on orientation; maximum **compressive**, **not tensile**, strength approximately **1300 MPa** at approximately **20% compressive strain**. This composition also exceeds the proposal’s Al cap. **No seawater corrosion test**. [CITE] [NUMBERS] [GAP] (guerra2023microstructureandmechanical pages 4-6, guerra2023microstructureandmechanical pages 6-8, guerra2023microstructureandmechanical pages 8-10, guerra2023microstructureandmechanical pages 10-12)

6. **Guo, Cheng, Li, Teng, Hu, Han and Chen (2026)**, “Enhancing Corrosion and Wear Resistance of Aluminum Bronze Alloy by Nanosecond Pulsed Laser Surface Melting,” *Materials* **19**, 3995, DOI **10.3390/ma19183995**. **Nickel-lean laser surface melting, not DED:** measured **11.44Al–2.37Fe–0.49Ni–0.48Mn**, thus **not strictly nickel-free C95300/C95400** and outside the 9.5% Al cap. **As laser remelted**, **120/140/160 W**, 80-µm spot, **3000 mm/s**, five repeats: roughly **5.6–8.9-µm** remelted layer; β′ XRD peak intensities and lath-like appearance change **qualitatively**, and the authors expressly state **no quantitative phase fractions**. In **stagnant 3.5% NaCl**, 30-min OCP stabilization, 0.5 mV/s polarization versus **saturated calomel**, untreated versus 140 W: *i*₍corr₎ **13.1445 → 5.34145 µA/cm²**, *E*₍corr₎ **−0.29479 → −0.26515 V**, hardness **137.042 → 186.957 HV**. Increased apparent β′ here coincided with **better short-term electrochemical performance**, showing why β′ abundance alone is not a universal seawater-corrosion ranking; no C71500 comparator or long-flow exposure was tested. [CITE] [NUMBERS] [GAP] (guo2026enhancingcorrosionand pages 2-4, guo2026enhancingcorrosionand pages 4-6, guo2026enhancingcorrosionand pages 9-12, guo2026enhancingcorrosionand pages 6-9)

7. **Samodurova, Shaburova, Samoilova, Radionova, Zakirov, Pashkeev, Myasoedov, Erdakov and Trofimov (2020)**, “A Study of Characteristics of Aluminum Bronze Coatings Applied to Steel Using Additive Technologies,” *Materials* **13**, 461, DOI **10.3390/ma13020461**. **Nickel-free blown-powder laser cladding**, powder **8.5–10Al–2–4Fe**, approximately **0.5Mn–0.25Si–0.6Sn**, **40–100 µm**; steel substrate; **600–2200 W**, **2-mm spot, 12 mm/s, 15 g/min**. The as-clad material was **strongly steel-diluted**: measured coating Fe approximately **12.87–44.95%**, and Cu approximately **79.46–49.62%**, across the power series, so it is **not a controlled Cu-(9–11)Al-(1–4)Fe deposit**. Upper-coating hardness at 600 W **121 HV**, with higher local Fe-dendrite values; some conditions had substrate-penetrating cracks up to **300 µm**. **No β′ fraction or seawater corrosion**. This is a caution against attributing substrate-dilution effects to nominal powder chemistry. [CITE] [NUMBERS] [GAP] (samodurova2020astudyof pages 1-3, samodurova2020astudyof pages 3-8, samodurova2020astudyof pages 8-10)

8. **Timmons, Nasiri and Bishop (2025)**, “Laser Powder Bed Fusion Processing of UNS C64200 Aluminum–Silicon–Bronze,” *Journal of Manufacturing and Materials Processing* **9**, 147, DOI **10.3390/jmmp9050147**. **Nickel-free/trace-Ni LPBF comparator**, **6.29Al–1.52Si–0.09Fe–0.05Ni**, *not* C95300: at **320 W, 770 mm/s, 0.088-mm hatch** printed tensile blanks **99.5 ± 0.3%** dense. XRD and EBSD identify mixed **α + β′ as built**, with **no reported β′ area percentage**; **620 °C/2 h then water quench** gave essentially α alone. As-built yield/UTS/elongation **595 ± 28/797 ± 9 MPa/4.9 ± 1.0%** versus heat-treated **329 ± 2/567 ± 1 MPa/24.6 ± 0.3%**. It establishes that even **~6.3% Al without appreciable Ni** can produce detectable LPBF β′, not that its phase balance predicts 10% Al laser DED. No seawater results. [CITE] [NUMBERS] [GAP] (timmons2025laserpowderbed pages 2-4, timmons2025laserpowderbed pages 19-23, timmons2025laserpowderbed pages 15-19)

9. **Chang, Fang, Zhou, Zhang, Xi, Ghafoor and Huang (published online 2024; issue 2025)**, “Heterogeneous interfaces of aluminum bronze/Inconel 718 dissimilar alloys under different wire arc directed energy deposition sequences,” *International Journal of Extreme Manufacturing* **7**, 015003, DOI **10.1088/2631-7990/ad870f**. **Nickel-free ERCuAl-A2/CuAl9 wire-arc DED**, then joined to Inconel 718; **not laser, not a prealloyed C95300 powder**. Isolated as-deposited CuAl9 tensile values yield/UTS/elongation **207.2 ± 1.1/501.5 ± 4.2 MPa/60.7 ± 1.8%**; the CuAl9–Inconel horizontal bimetal is **302.7 ± 6.2/573.1 ± 5.9 MPa/22.2 ± 0.3%**. The paper does not supply a comparable, independently measured β′ fraction or C71500-standard seawater test. [CITE] [NUMBERS] [GAP] (chang2024heterogeneousinterfacesof pages 7-9)

10. **Zhao, Du, Yao, Chen, Ding and Li (2022)**, “Microstructure and Mechanical Properties of Nickel-Aluminum Bronze Coating on 17-4PH Stainless Steel by Laser Cladding,” *Chinese Journal of Mechanical Engineering* **35**, article 140, DOI **10.1186/s10033-022-00807-z**. **Powder laser cladding**, **10.80Al–4.73Ni–4.10Fe**, **1500–2400 W**, **3.4-mm spot**, **1.2 m/min**, one/four layers on **17-4PH steel**. As clad, XRD mainly reports α/κ/Fe; acicular regions appear but **no quantified β′**, and Fe/Cr-rich dendrites arise from the **steel substrate**, disappearing above the first layer. Cladding hardness **204–266 HV₀.₂**; **2400-W, four-layer** specimen UTS **767.80 MPa**, failing in bronze rather than at the bond. **No corrosion measurement**; not a valid NAB-on-NAB comparison. [CITE] [NUMBERS] [GAP] (zhao2022microstructureandmechanical pages 2-4, zhao2022microstructureandmechanical pages 4-6, zhao2022microstructureandmechanical pages 6-9)

**Specified papers without verifiable primary numerical extraction.** **Hyatt, Magee and Betancourt (1998)**, “The effect of heat input on the microstructure and properties of nickel aluminum bronze laser clad with a consumable of composition Cu–9.0Al–4.6Ni–3.9Fe–1.2Mn,” *Metallurgical and Materials Transactions A* **29**, 1677–1690, DOI **10.1007/s11661-998-0090-5**: **laser clad on cast NAB**; the accessible dissertation’s explicit attribution says the **42.5-J/mm** condition appeared nearly entirely martensitic, with boundary α, and intragranular Widmanstätten α grew with heat input, including around **150 J/mm**. Those are **secondary-reported optical observations, not measured β′ percentages**; primary full text was unavailable for checking its remaining process/corrosion numbers. [CITE] [GAP] (kuprienko2025analysisofnickel pages 50-55)

**Murray, Thomas, Wu, Neil and Hutchinson (2020)**, “Selective laser melting of nickel aluminium bronze,” *Additive Manufacturing* **33**, 101122, DOI **10.1016/j.addma.2020.101122**: **LPBF**, approximately **9.8Al–5.2Ni–4.6Fe–0.3Mn**, laser power approximately **85–95 W** as cited by later authors. The later Li paper reports **as-built elongation 0.4%**, then **700 °C/1 h** yield **490 MPa**, elongation **12.5%**; another source summarizes maximum density around **99.1%**. These are **secondary-reported**, not independently checked original-table values; neither a C95300 matched control nor a verified phase-percentage table was available. [CITE] [NUMBERS: secondary] [GAP] (li2021nanotwinscontainingmicrostructureand pages 1-4, timmons2025laserpowderbed pages 1-2)

**Southeast University: Jia and Sun/Wang coworkers.** The searches identified **Jia, Wang, Chen, Zhao, Sun and Han (2025)**, “Tailoring microstructural evolution in laser deposited nickel-aluminum bronze alloy by controlling water cooling condition,” *Journal of Materials Processing Technology* **335**, 118659, DOI **10.1016/j.jmatprotec.2024.118659**; **Jia, Li, Chen, Wang, Sun and Han (2025)**, “Effect of further precipitate refinement on mechanical properties and corrosion behavior of additively manufactured nickel aluminum bronze,” DOI **10.1016/j.corsci.2025.113114**; and **Jia, Yang, Li, Wang, Tan, Sun and Han (2026)**, “Subtractive composition design of nickel-aluminum bronze for laser additive manufacturing: achieving superior as-deposited mechanical and corrosion performance,” DOI **10.1016/j.addma.2026.105291**. **Their primary texts were unobtainable**: exact alloy, β′ fraction, cooling schedule, corrosion electrolyte and numerical corrosion improvements **cannot responsibly be supplied**. They are unusually relevant leads, not verified proof that a particular low-power C63000 formulation meets the proposal target. [CITE] [GAP]

## Corrosion endpoints and multilayer reheating

The strongest directly checked **composition trend** is **Tan *et al.* (2024)**, “Effect of Al/Ni Ratio on the Microstructure and Properties of Nickel–Aluminum Bronze Alloys,” *Materials* **17**, 1330, DOI **10.3390/ma17061330**. **Cast**, without post-cast treatment, at approximately constant **4Fe–2Mn**, the measured **Al/Ni pairs** were **6.94/6.82**, **7.90/6.13**, **8.94/5.18**, **9.94/3.99**. Optical microscopy/XRD found β′ becoming more apparent with increasing **Al/Ni**; **no quantitative β′ percentage** is reported. Hardness **104.02→202.46 HV**, UTS **356.33→750.67 MPa**, elongation **50.50→11.00%** across the series. In **25 °C stagnant 3.5% NaCl**, renewed every seven days, *i*₍corr₎ after **30 d** was **0.35, 0.36, 0.69 and 0.78 µA/cm²**, respectively; corresponding *E*₍corr₎ versus **Ag/AgCl** **−281.48, −295.55, −249.35 and −257.75 mV**. This experiment changes **Al and Ni together**, so it cannot isolate a 5% Ni effect at fixed 10% Al or prove behavior under laser DED. [CITE] [NUMBERS] [GAP] (tan2024effectofalni pages 2-4, tan2024effectofalni pages 4-6, tan2024effectofalni pages 10-12)

For **Jafari *et al.*’s cast C95800** above, the electrochemical test used **3.5% NaCl**, **25 or 40 °C**, stagnant or **0–9000-rpm rotating disk**, short **1000-s OCP** conditioning and 1 mV/s polarization. At **25 °C**, stagnant as-cast versus annealed: *i*₍corr₎ **1.74 versus 0.918 µA/cm²** and *E*₍corr₎ **−262 versus −255 mV versus Ag/AgCl**. At **9000 rpm**, *i*₍corr₎ **5.57 versus 5.22 µA/cm²**: flow substantially narrows the apparent benefit. This is **cast, not as-deposited DED**, and rpm cannot be relabeled as a seawater pipe velocity. [CITE] [NUMBERS] [GAP] (jafari2021effectoffluid pages 2-4, jafari2021effectoffluid pages 7-8, jafari2021effectoffluid pages 4-7)

For **Fayanas *et al.*’s cast and sinter+HIP NAB**, **480 h in stagnant 3.5% NaCl** gave measured cast before/after **700 °C/2 h** *i*₍corr₎ **6.45/2.12 µA/cm²**; sinter+HIP before/after **3.02/10.4 µA/cm²**, so heat treatment’s corrosion benefit **is not universal** across microstructures. Their separate **48-h, 3.8-m/s, 3%-sand, 3.5%-NaCl** erosion–corrosion exposure gave as-processed cast and sinter+HIP mass loss **8.7 and 7.6 mg/cm²**. Neither electrolyte is ASTM D1141 seawater, and neither set includes C71500. No justified numerical selective-attack depth was extracted from these papers. [CITE] [NUMBERS] [GAP] (fayanas2025nickelaluminiumbronze pages 1-2, fayanas2025nickelaluminiumbronze pages 5-7)

**Reheating is spatially selective.** A newly solidified top track can retain β-derived martensite while underlying tracks encounter remelting, elevated-temperature α/κ formation, or **subcritical tempering**. In NAB, sufficiently prolonged **675–700 °C for 2–6 h** demonstrates β′ decomposition toward α + κ and precipitation/coarsening; for nickel-free bronzes the competing equilibrium route includes **α + γ₂**, with local composition and dwell determining whether that detrimental constituent actually forms. A DED layer’s brief thermal spike is **not equivalent** to a six-hour anneal. Kuprienko documents reheated **layer bands** and identifies **fine α plus κ** in apparently dark regions; Li finds persistent β* even after multilayer powder DED; Müller finds needle-rich material throughout a 35-layer build. Thus an as-deposited component may have **different top, interior, interface and repair-dilution phase balances**. [CITE] [GAP] (huang2026densificationbehaviorand pages 6-10, fayanas2025nickelaluminiumbronze pages 2-5, kuprienko2025analysisofnickel pages 147-152, li2021nanotwinscontainingmicrostructureand pages 14-19, muller2023usingultrasonicatomization pages 8-12, konecna2012copperandcopper pages 25-27)

**Direct answer for 300–500 W C63000.** It is **plausible**, not established, that **10Al–5Ni–3Fe** would develop a mixed α/κ/β-derived microstructure rather than the same fraction as a nickel-free **9–11Al–1–4Fe** powder under identical conditions: Ni changes κ formation and the Al-dependent β inventory. But **≈5% Ni does not eliminate martensite**, and **higher Al within the nickel-free C95300 range can itself increase β-derived material**. Neither nominal power nor a quoted spot diameter fixes cooling rate: speed, absorbed power, powder rate, dilution into cast NAB versus Cu–Ni, substrate temperature and repeated-layer dwell are decisive. The **300–500-W, 0.4-mm-spot** InssTek apparatus cannot be equated by watts alone to Müller’s **1300-W/1-mm** or Li’s **1000–1500-W/2-mm** setup; insufficient absorbed energy can cause lack of fusion before phase tuning succeeds. Test prealloyed powders **side-by-side at matched density, actual deposit composition and thermal history**. The vendor’s nickel-free C95300 **628 MPa XY/598 MPa Z UTS** is a useful but **unverified-for-this-question** machine-specific strength comparator: its phase fractions, corrosion resistance, elongation, heat treatment and processing parameters are not supplied. There is **no evidence here** that either deposit, as deposited, meets the specified **wrought C71500** seawater benchmark. [CITE] [NUMBERS] [INSSTEK: vendor benchmark only] [GAP] (muller2023usingultrasonicatomization pages 3-6, muller2023usingultrasonicatomization pages 8-12, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 4-9, tan2024effectofalni pages 2-4)

### Top 5 things the PI should know

1. **Do not claim Ni suppresses laser-DED β′ to a known percentage.** Ni-bearing DED can be needle/martensite-rich; a same-process, fixed-Al nickel-free-versus-NAB **XRD/EBSD/TEM-validated phase-fraction** comparison is missing. (muller2023usingultrasonicatomization pages 8-12, li2021nanotwinscontainingmicrostructureand pages 9-14, jafari2021effectoffluid media a8b52b0c)
2. **The 9.5% Al ceiling is a hypothesis to test, not a verified sharp phase boundary.** Cast Al/Ni changes and LPBF outcomes show substantial dependence on both chemistry and processing; several informative NAB laser papers actually use **9.7–11% Al**, outside the proposed limit. (tan2024effectofalni pages 2-4, li2021nanotwinscontainingmicrostructureand pages 4-9, huang2026densificationbehaviorand pages 2-4, guerra2023microstructureandmechanical pages 8-10)
3. **Use the same seawater protocol for all candidates and wrought C71500.** Report as-deposited composition and porosity alongside static and controlled-flow **natural or ASTM D1141 substitute seawater** exposure, duration, polarization/reference electrode, mass loss and **cross-sectional maximum selective-attack depth**; 3.5% NaCl polarization alone cannot certify the target. (jafari2021effectoffluid pages 7-8, fayanas2025nickelaluminiumbronze pages 5-7, guo2026enhancingcorrosionand pages 9-12)
4. **Profile the actual multilayer thermal history and sample position.** Top-layer β′, reheated interior α/κ, and diluted NAB or Cu–Ni repair interface may give different mechanical and corrosion responses; verify suspect dark regions with diffraction/TEM, not etch contrast alone. (kuprienko2025analysisofnickel pages 147-152, kuprienko2025analysisofnickel pages 45-50, li2021nanotwinscontainingmicrostructureand pages 9-14)
5. **Treat powder production and power as coupled feasibility constraints.** Müller establishes rePOWDER feasibility but reports a **D₉₀ of 179 µm** and occasional sonotrode-derived carbon fibers; qualify the **45–150-µm cut**, oxygen/contamination and powder-flow response before assuming its **1300-W** density and phase outcome transfer to **300–500-W InssTek DMT**. (muller2023usingultrasonicatomization pages 3-6, muller2023usingultrasonicatomization pages 6-8, muller2023usingultrasonicatomization pages 8-12)

References

1. (muller2023usingultrasonicatomization pages 8-12): Vinzenz M. ̈uller, Janek Maria Fasselt, Tobias Kruse, Christian Kl ̈otzer, Rafael Kleba-Ehrhardt, Tomasz Choma, M. Biegler, and M. Rethmeier. Using ultrasonic atomization to recycle aluminium bronze chips for additive laser directed energy deposition. IOP Conference Series: Materials Science and Engineering, Dec 2023. URL: https://doi.org/10.1088/1757-899x/1296/1/012036, doi:10.1088/1757-899x/1296/1/012036. This article has 7 citations.

2. (li2021nanotwinscontainingmicrostructureand pages 9-14): Boyuan Li, Han Zheng, Chang-Jun Han, and K. Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive Manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 74 citations and is from a highest quality peer-reviewed journal.

3. (kuprienko2025analysisofnickel pages 45-50): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

4. (kuprienko2025analysisofnickela pages 45-50): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

5. (doyle2022additivemanufacturingof pages 47-53): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

6. (li2021nanotwinscontainingmicrostructureand pages 1-4): Boyuan Li, Han Zheng, Chang-Jun Han, and K. Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive Manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 74 citations and is from a highest quality peer-reviewed journal.

7. (konecna2012copperandcopper pages 25-27): Copper and Copper Alloys: Casting, Classification and Characteristic Microstructures This article has 61 citations.

8. (fayanas2025nickelaluminiumbronze pages 1-2): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

9. (kuprienko2025analysisofnickel pages 30-36): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

10. (fayanas2025nickelaluminiumbronze pages 2-5): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

11. (jafari2021effectoffluid pages 2-4): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

12. (jafari2021effectoffluid media a8b52b0c): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

13. (kuprienko2025analysisofnickel pages 1-7): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

14. (kuprienko2025analysisofnickel pages 67-72): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

15. (kuprienko2025analysisofnickel pages 147-152): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

16. (kuprienko2025analysisofnickel pages 152-158): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

17. (guerra2023microstructureandmechanical pages 8-10): Carolina Guerra, Jorge A. Ramos-Grez, Iván La Fé-Perdomo, Alejandro Castillo, and Magdalena Walczak. Microstructure and mechanical properties of cu-11al-5ni-4fe wt% manufactured by lpbf. Metals, 13:459, Feb 2023. URL: https://doi.org/10.3390/met13030459, doi:10.3390/met13030459. This article has 11 citations.

18. (kuprienko2025analysisofnickel pages 50-55): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

19. (小林啓佑1961cual合金のβ→ pages 1-2): 椙山正孝， 小林啓佑. Cu-al 合金の β→ α+ γ2 変態におよぼすニッケル, 鉄およびマンガン添加の影響. Unknown journal, 1961.

20. (小林啓佑1961cual合金のβ→ pages 3-4): 椙山正孝， 小林啓佑. Cu-al 合金の β→ α+ γ2 変態におよぼすニッケル, 鉄およびマンガン添加の影響. Unknown journal, 1961.

21. (小林啓佑1961cual合金のβ→ pages 4-5): 椙山正孝， 小林啓佑. Cu-al 合金の β→ α+ γ2 変態におよぼすニッケル, 鉄およびマンガン添加の影響. Unknown journal, 1961.

22. (kuprienko2025analysisofnickel pages 131-137): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

23. (kuprienko2025analysisofnickel pages 137-142): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

24. (li2021nanotwinscontainingmicrostructureand pages 4-9): Boyuan Li, Han Zheng, Chang-Jun Han, and K. Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive Manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 74 citations and is from a highest quality peer-reviewed journal.

25. (li2021nanotwinscontainingmicrostructureand pages 19-24): Boyuan Li, Han Zheng, Chang-Jun Han, and K. Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive Manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 74 citations and is from a highest quality peer-reviewed journal.

26. (muller2023usingultrasonicatomization pages 3-6): Vinzenz M. ̈uller, Janek Maria Fasselt, Tobias Kruse, Christian Kl ̈otzer, Rafael Kleba-Ehrhardt, Tomasz Choma, M. Biegler, and M. Rethmeier. Using ultrasonic atomization to recycle aluminium bronze chips for additive laser directed energy deposition. IOP Conference Series: Materials Science and Engineering, Dec 2023. URL: https://doi.org/10.1088/1757-899x/1296/1/012036, doi:10.1088/1757-899x/1296/1/012036. This article has 7 citations.

27. (doyle2022additivemanufacturingof pages 53-58): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

28. (huang2026densificationbehaviorand pages 2-4): Yi-Zhe Huang, Guanjun Fu, An Wang, Zhong-Xu Xiao, Jin-Feng Sun, Jun Wang, and Xiao-Jia Nie. Densification behavior and microstructure of nickel aluminum bronze alloy fabricated by laser powder bed fusion. Materials, 19:208, Jan 2026. URL: https://doi.org/10.3390/ma19010208, doi:10.3390/ma19010208. This article has 1 citations.

29. (huang2026densificationbehaviorand pages 4-6): Yi-Zhe Huang, Guanjun Fu, An Wang, Zhong-Xu Xiao, Jin-Feng Sun, Jun Wang, and Xiao-Jia Nie. Densification behavior and microstructure of nickel aluminum bronze alloy fabricated by laser powder bed fusion. Materials, 19:208, Jan 2026. URL: https://doi.org/10.3390/ma19010208, doi:10.3390/ma19010208. This article has 1 citations.

30. (huang2026densificationbehaviorand pages 6-10): Yi-Zhe Huang, Guanjun Fu, An Wang, Zhong-Xu Xiao, Jin-Feng Sun, Jun Wang, and Xiao-Jia Nie. Densification behavior and microstructure of nickel aluminum bronze alloy fabricated by laser powder bed fusion. Materials, 19:208, Jan 2026. URL: https://doi.org/10.3390/ma19010208, doi:10.3390/ma19010208. This article has 1 citations.

31. (huang2026densificationbehaviorand pages 10-12): Yi-Zhe Huang, Guanjun Fu, An Wang, Zhong-Xu Xiao, Jin-Feng Sun, Jun Wang, and Xiao-Jia Nie. Densification behavior and microstructure of nickel aluminum bronze alloy fabricated by laser powder bed fusion. Materials, 19:208, Jan 2026. URL: https://doi.org/10.3390/ma19010208, doi:10.3390/ma19010208. This article has 1 citations.

32. (guerra2023microstructureandmechanical pages 4-6): Carolina Guerra, Jorge A. Ramos-Grez, Iván La Fé-Perdomo, Alejandro Castillo, and Magdalena Walczak. Microstructure and mechanical properties of cu-11al-5ni-4fe wt% manufactured by lpbf. Metals, 13:459, Feb 2023. URL: https://doi.org/10.3390/met13030459, doi:10.3390/met13030459. This article has 11 citations.

33. (guerra2023microstructureandmechanical pages 6-8): Carolina Guerra, Jorge A. Ramos-Grez, Iván La Fé-Perdomo, Alejandro Castillo, and Magdalena Walczak. Microstructure and mechanical properties of cu-11al-5ni-4fe wt% manufactured by lpbf. Metals, 13:459, Feb 2023. URL: https://doi.org/10.3390/met13030459, doi:10.3390/met13030459. This article has 11 citations.

34. (guerra2023microstructureandmechanical pages 10-12): Carolina Guerra, Jorge A. Ramos-Grez, Iván La Fé-Perdomo, Alejandro Castillo, and Magdalena Walczak. Microstructure and mechanical properties of cu-11al-5ni-4fe wt% manufactured by lpbf. Metals, 13:459, Feb 2023. URL: https://doi.org/10.3390/met13030459, doi:10.3390/met13030459. This article has 11 citations.

35. (guo2026enhancingcorrosionand pages 2-4): Ling-Yu Guo, Hao-Jun Cheng, Fu-Shao Li, Qing Teng, Kai-Xiong Hu, Ming-Xing Han, and Yun Chen. Enhancing corrosion and wear resistance of aluminum bronze alloy by nanosecond pulsed laser surface melting. Sep 2026. URL: https://doi.org/10.3390/ma19183995, doi:10.3390/ma19183995. This article has 0 citations.

36. (guo2026enhancingcorrosionand pages 4-6): Ling-Yu Guo, Hao-Jun Cheng, Fu-Shao Li, Qing Teng, Kai-Xiong Hu, Ming-Xing Han, and Yun Chen. Enhancing corrosion and wear resistance of aluminum bronze alloy by nanosecond pulsed laser surface melting. Sep 2026. URL: https://doi.org/10.3390/ma19183995, doi:10.3390/ma19183995. This article has 0 citations.

37. (guo2026enhancingcorrosionand pages 9-12): Ling-Yu Guo, Hao-Jun Cheng, Fu-Shao Li, Qing Teng, Kai-Xiong Hu, Ming-Xing Han, and Yun Chen. Enhancing corrosion and wear resistance of aluminum bronze alloy by nanosecond pulsed laser surface melting. Sep 2026. URL: https://doi.org/10.3390/ma19183995, doi:10.3390/ma19183995. This article has 0 citations.

38. (guo2026enhancingcorrosionand pages 6-9): Ling-Yu Guo, Hao-Jun Cheng, Fu-Shao Li, Qing Teng, Kai-Xiong Hu, Ming-Xing Han, and Yun Chen. Enhancing corrosion and wear resistance of aluminum bronze alloy by nanosecond pulsed laser surface melting. Sep 2026. URL: https://doi.org/10.3390/ma19183995, doi:10.3390/ma19183995. This article has 0 citations.

39. (samodurova2020astudyof pages 1-3): Marina Samodurova, Nataliya Shaburova, Olga Samoilova, Liudmila Radionova, Ramil’ Zakirov, Kirill Pashkeev, Vyacheslav Myasoedov, Ivan Erdakov, and Evgeny Trofimov. A study of characteristics of aluminum bronze coatings applied to steel using additive technologies. Materials, 13:461, Jan 2020. URL: https://doi.org/10.3390/ma13020461, doi:10.3390/ma13020461. This article has 21 citations.

40. (samodurova2020astudyof pages 3-8): Marina Samodurova, Nataliya Shaburova, Olga Samoilova, Liudmila Radionova, Ramil’ Zakirov, Kirill Pashkeev, Vyacheslav Myasoedov, Ivan Erdakov, and Evgeny Trofimov. A study of characteristics of aluminum bronze coatings applied to steel using additive technologies. Materials, 13:461, Jan 2020. URL: https://doi.org/10.3390/ma13020461, doi:10.3390/ma13020461. This article has 21 citations.

41. (samodurova2020astudyof pages 8-10): Marina Samodurova, Nataliya Shaburova, Olga Samoilova, Liudmila Radionova, Ramil’ Zakirov, Kirill Pashkeev, Vyacheslav Myasoedov, Ivan Erdakov, and Evgeny Trofimov. A study of characteristics of aluminum bronze coatings applied to steel using additive technologies. Materials, 13:461, Jan 2020. URL: https://doi.org/10.3390/ma13020461, doi:10.3390/ma13020461. This article has 21 citations.

42. (timmons2025laserpowderbed pages 2-4): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 3 citations.

43. (timmons2025laserpowderbed pages 19-23): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 3 citations.

44. (timmons2025laserpowderbed pages 15-19): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 3 citations.

45. (chang2024heterogeneousinterfacesof pages 7-9): Tianxing Chang, Xuewei Fang, You Zhou, Hongkai Zhang, Naiyuan Xi, Shahid Ghafoor, and Ke Huang. Heterogeneous interfaces of aluminum bronze/inconel 718 dissimilar alloys under different wire arc directed energy deposition sequences. International Journal of Extreme Manufacturing, 7:015003, Nov 2024. URL: https://doi.org/10.1088/2631-7990/ad870f, doi:10.1088/2631-7990/ad870f. This article has 35 citations.

46. (zhao2022microstructureandmechanical pages 2-4): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

47. (zhao2022microstructureandmechanical pages 4-6): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

48. (zhao2022microstructureandmechanical pages 6-9): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

49. (timmons2025laserpowderbed pages 1-2): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 3 citations.

50. (tan2024effectofalni pages 2-4): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 15 citations.

51. (tan2024effectofalni pages 4-6): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 15 citations.

52. (tan2024effectofalni pages 10-12): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 15 citations.

53. (jafari2021effectoffluid pages 7-8): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

54. (jafari2021effectoffluid pages 4-7): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

55. (fayanas2025nickelaluminiumbronze pages 5-7): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

56. (li2021nanotwinscontainingmicrostructureand pages 14-19): Boyuan Li, Han Zheng, Chang-Jun Han, and K. Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive Manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 74 citations and is from a highest quality peer-reviewed journal.

57. (muller2023usingultrasonicatomization pages 6-8): Vinzenz M. ̈uller, Janek Maria Fasselt, Tobias Kruse, Christian Kl ̈otzer, Rafael Kleba-Ehrhardt, Tomasz Choma, M. Biegler, and M. Rethmeier. Using ultrasonic atomization to recycle aluminium bronze chips for additive laser directed energy deposition. IOP Conference Series: Materials Science and Engineering, Dec 2023. URL: https://doi.org/10.1088/1757-899x/1296/1/012036, doi:10.1088/1757-899x/1296/1/012036. This article has 7 citations.
