<!--
Edison Scientific LITERATURE_HIGH (job-futurehouse-paperqa3-high)
Task ID: 5060ace2-75c9-4e0d-ab83-1a87573d6dc4
Submitted: 2026-11-12T16:41:08Z; fetched: 2026-11-12T17:13:27Z; status: success; has_successful_answer: True
Retrieved with edison-client 0.18.0 (EDISON_PLATFORM_API_KEY) from GitHub Actions for issue #254. The full trajectory is in the .trajectory.json file beside this one.
-->

**Question (LITERATURE_HIGH):** Why is cryogenic mechanical testing important for aerospace structural alloys, and what does it reveal that room-temperature testing does not? Cover, with citations and DOIs: (1) Applications that need cryogenic qualification: liquid hydrogen (20 K), liquid oxygen (90 K) and liquid methane (111 K) propellant tanks and feedlines on launch vehicles (Space Shuttle external tank, SLS, Falcon 9, Ariane, H-II/H3), liquid-hydrogen aircraft, cryogenic wind tunnels, cryocooled space instruments, and superconducting-magnet structures. (2) How yield and tensile strength, elongation, fracture toughness (K_Ic, J_Ic), fatigue and fatigue-crack growth, and impact energy change between 295 K, 77 K, 20 K and 4 K for FCC (aluminum, austenitic stainless, nickel), BCC (ferritic steels) and HCP (titanium) alloys; ductile-to-brittle transitions; serrated or discontinuous plastic flow and adiabatic heating at 4 K; thermal contraction and thermal cycling; welds and heat-affected zones. (3) Failures, anomalies or design changes traced to missing or inadequate cryogenic property data, and the gaps in design-allowable databases (MMPDS) at cryogenic temperatures. (4) Test standards and practice (ASTM E1450, ISO 6892-3, ASTM E23 low-temperature Charpy, ASTM E1820/E399 and ASTM E647 at cryogenic temperature, JIS Z 2277), whether 77 K liquid-nitrogen tests are a valid proxy for 20 K or 4 K service, and how cost and helium scarcity shape what gets tested. (5) Hydrogen compatibility at cryogenic temperature for liquid-hydrogen service. Context: the BYU Vertical Cloud Lab designs aluminum alloys for laser powder bed fusion (LPBF) with AI and CALPHAD, including critical-mineral-lean compositions (less Sc, Li, Ce), makes its own powder by ultrasonic atomization, and tests in a ladder of single tracks, density cubes and tensile bars. It is deciding whether and how to add cryogenic mechanical testing. Prefer primary sources, NASA/NIST technical reports and standards; give DOIs or report numbers; give numbers with temperatures and units; and say which claims are strongly vs. weakly supported.

---

Question: Why is cryogenic mechanical testing important for aerospace structural alloys, and what does it reveal that room-temperature testing does not? Cover, with citations and DOIs: (1) Applications that need cryogenic qualification: liquid hydrogen (20 K), liquid oxygen (90 K) and liquid methane (111 K) propellant tanks and feedlines on launch vehicles (Space Shuttle external tank, SLS, Falcon 9, Ariane, H-II/H3), liquid-hydrogen aircraft, cryogenic wind tunnels, cryocooled space instruments, and superconducting-magnet structures. (2) How yield and tensile strength, elongation, fracture toughness (K_Ic, J_Ic), fatigue and fatigue-crack growth, and impact energy change between 295 K, 77 K, 20 K and 4 K for FCC (aluminum, austenitic stainless, nickel), BCC (ferritic steels) and HCP (titanium) alloys; ductile-to-brittle transitions; serrated or discontinuous plastic flow and adiabatic heating at 4 K; thermal contraction and thermal cycling; welds and heat-affected zones. (3) Failures, anomalies or design changes traced to missing or inadequate cryogenic property data, and the gaps in design-allowable databases (MMPDS) at cryogenic temperatures. (4) Test standards and practice (ASTM E1450, ISO 6892-3, ASTM E23 low-temperature Charpy, ASTM E1820/E399 and ASTM E647 at cryogenic temperature, JIS Z 2277), whether 77 K liquid-nitrogen tests are a valid proxy for 20 K or 4 K service, and how cost and helium scarcity shape what gets tested. (5) Hydrogen compatibility at cryogenic temperature for liquid-hydrogen service. Context: the BYU Vertical Cloud Lab designs aluminum alloys for laser powder bed fusion (LPBF) with AI and CALPHAD, including critical-mineral-lean compositions (less Sc, Li, Ce), makes its own powder by ultrasonic atomization, and tests in a ladder of single tracks, density cubes and tensile bars. It is deciding whether and how to add cryogenic mechanical testing. Prefer primary sources, NASA/NIST technical reports and standards; give DOIs or report numbers; give numbers with temperatures and units; and say which claims are strongly vs. weakly supported.

# Why Cryogenic Mechanical Testing Is Important for Aerospace Structural Alloys

## 1. Applications Requiring Cryogenic Qualification

Cryogenic mechanical testing is essential because numerous aerospace and energy systems expose structural alloys to temperatures far below ambient. The principal applications include:

**Launch-vehicle propellant tanks and feedlines.** The Space Shuttle External Tank stored both liquid hydrogen (LH2, ~20 K) and liquid oxygen (LOX, ~90 K) and was constructed primarily from Al 2219 (earlier configurations) and Al-Li 2195 (Super Lightweight Tank) (mital2006reviewofcurrent pages 10-13, tzoumakis2024multiphysicsdigitalmodel pages 6-7). NASA's Space Launch System (SLS) core stage likewise uses Al 2219 for its LH2 and LOX tanks (tzoumakis2024multiphysicsdigitalmodel pages 6-7). Aluminum alloys 2219, 2195, 2029, 2A14, and 5A06 have been used or developed for LH2 propellant tanks in U.S. and Chinese launch vehicles (qiu2021researchprogressof pages 6-8). Liquid methane (~111 K) is an emerging propellant for vehicles such as SpaceX's Starship and others, requiring similar cryogenic qualification of tank materials (weakly supported—specific vehicle-level data were not found in the retrieved literature).

**Liquid-hydrogen aircraft.** NASA and Boeing have investigated LH2 cryotanks for aircraft, including the hydrogen-fueled B-57 bomber program and more recent commuter-aircraft concepts using Al 2219 tanks (mital2006reviewofcurrent pages 10-13, tzoumakis2024multiphysicsdigitalmodel pages 6-7). Material selection for LH2 aircraft cryotanks must account for cryogenic strength, fatigue under thermal cycling, and hydrogen compatibility (shabbirkhanUnknownyeard4.2identification pages 12-14).

**Superconducting-magnet structures.** Structural casings and conduits for superconducting magnets in fusion reactors (ITER, CFETR) and particle accelerators operate at 4.2 K in liquid helium. Austenitic stainless steels such as 316LN, JN1, JJ1, JK2LB, and Nitronic 50 are the primary structural materials, requiring simultaneous high yield strength (≥1000–1200 MPa) and high fracture toughness (K(J)Ic ≥ 200 MPa·m^0.5) at 4 K (dai2025developmentofcryogenic pages 8-10, shindo2003cryogenicfractureand pages 1-2, mcrae2017fatigueandfracture pages 1-3).

**Cryocooled space instruments and cryogenic wind tunnels.** These applications require structural materials characterized at temperatures from ~4 K to ~77 K (weakly supported—general cryogenic-instrument references found but specific vehicle-level citations not retrieved).

**Titanium in cryogenic service.** Ti-5Al-2.5Sn ELI has been used for liquid-helium and liquid-hydrogen containers and conduits, including in the Apollo program (qiu2021researchprogressof pages 8-9).

## 2. How Mechanical Properties Change with Temperature by Crystal Structure

The following table summarizes representative property data from the literature:

| Crystal structure | Alloy / condition / orientation | Temperature (K) | Yield strength (MPa) | UTS (MPa) | Elongation (%) | Fracture toughness, K_Ic (MPa√m) | Source |
|---|---|---:|---:|---:|---:|---:|---|
| FCC | Al 2195-T8 plate, longitudinal | 297 | 524 | 552 | 9.0 | — | (hafley2011evaluationofaluminum pages 24-28) |
| FCC | Al 2195-T8 plate, longitudinal | 77 | 641 | 696 | 10.9 | — | (hafley2011evaluationofaluminum pages 24-28) |
| FCC | 304L stainless steel | 300 | 258 | 725 | 75.9 | — | (kim2023tensileandfracture pages 7-10) |
| FCC | 304L stainless steel | 77 | 856 | 2,172 | 35.7 | — | (kim2023tensileandfracture pages 7-10) |
| FCC | 304L stainless steel | 20 | 1,059 | 2,433 | 32.6 | — | (kim2023tensileandfracture pages 7-10) |
| FCC | 316L stainless steel, annealed | 295 | 296 | 589 | — | — | (walsh1996the4k pages 1-4) |
| FCC | 316L stainless steel, annealed | 4 | 485 | 860 | 37 | 260 | (walsh1996the4k pages 1-4) |
| FCC | Modified 316LN stainless steel, ~20% cold-worked | 295 | 438 | 754 | — | — | (walsh1996the4k pages 1-4) |
| FCC | Modified 316LN stainless steel, ~20% cold-worked | 4 | 1,284 | 1,648 | 28 | 159 | (walsh1996the4k pages 1-4) |
| HCP | Ti-5Al-2.5Sn ELI, air-cooled, LT orientation | 77 | — | — | — | 111 | (vanstone1977investigationofthe pages 75-78, vanstone1974theeffectof pages 42-45) |
| HCP | Ti-5Al-2.5Sn ELI, air-cooled, LT orientation | 20 | — | — | — | 90–91 | (vanstone1977investigationofthe pages 75-78, vanstone1974theeffectof pages 42-45) |
| FCC | LPBF AlSi10Mg, reference room-temperature condition | 295 | — | 250 ± 11 | — | — | (adams2023materialandscan pages 43-47) |
| FCC | LPBF AlSi10Mg, XY build orientation | 20 | — | 483 | — | — | (adams2023materialandscan pages 43-47) |
| FCC | LPBF AlSi10Mg, Z build orientation | 20 | — | 512 | — | — | (adams2023materialandscan pages 43-47) |


*Table: Representative tensile and fracture properties illustrate that cooling usually raises strength but can alter ductility and toughness in alloy-, processing-, and orientation-dependent ways. Dashes identify properties not reported in the cited datasets.*

### 2.1 FCC Alloys (Aluminum, Austenitic Stainless Steel, Nickel)

**Strength increases substantially.** For 304L stainless steel, the 0.2% yield strength rises from 258 MPa at 300 K to 856 MPa at 77 K and 1059 MPa at 20 K—a four-fold increase (kim2023tensileandfracture pages 7-10). Ultimate tensile strength increases from 725 MPa to 2172 MPa (77 K) and 2433 MPa (20 K) (kim2023tensileandfracture pages 7-10). For Al 2195-T8, longitudinal yield strength increases from 524 MPa (297 K) to 641 MPa (77 K), with UTS rising from 552 to 696 MPa (hafley2011evaluationofaluminum pages 24-28, hafley2011evaluationofaluminuma pages 21-24). Annealed 316L shows yield strength increasing from 296 MPa (295 K) to 485 MPa (4 K), with UTS from 589 to 860 MPa (walsh1996the4k pages 1-4).

**Elongation decreases but ductility is retained.** For 304L, elongation falls from 75.9% (300 K) to 35.7% (77 K) and 32.6% (20 K)—substantial reduction but not brittle failure (kim2023tensileandfracture pages 7-10). FCC aluminum alloys do not exhibit an obvious ductile-to-brittle transition owing to their crystal structure (qiu2021researchprogressof pages 6-8). In some cases, aluminum alloy elongation actually increases at cryogenic temperature: Al 5083 and Al 6061 showed improved elongation at 20 K (kim2022metallicmaterialevaluation pages 5-9).

**Fracture toughness behavior is complex.** For annealed 316L, K_Ic reaches 260 MPa·m^0.5 at 4 K (walsh1996the4k pages 1-4), but cold-worked 316L drops to 117 MPa·m^0.5 (walsh1996the4k pages 1-4). The strength–toughness tradeoff is critical: increasing yield strength through cold work or heat treatment can sharply reduce cryogenic fracture toughness (walsh1996the4k pages 1-4). For 316LN, a 700 °C/100 h heat treatment reduced 4 K toughness by ~40% with only ~10% strength decrease (walsh1996the4k pages 1-4). Fracture toughness of 316 stainless steel increases from RT to 77 K but decreases slightly from 77 K to 20 K, while remaining above the room-temperature value (qiu2021researchprogressof pages 5-6). For 304L, J_Ic was 321.4 kJ/m² at 77 K versus 254.2 kJ/m² at 20 K (kim2023tensileandfracture pages 13-16).

**INCOLOY 908** (nickel-base) achieves yield strength of 1200 MPa and K_Ic of 200 MPa·m^0.5 at 4.2 K for fusion-magnet applications (dai2025developmentofcryogenic pages 8-10).

### 2.2 BCC Alloys (Ferritic Steels)

Ferritic steels with BCC crystal structure undergo a pronounced ductile-to-brittle transition (DBT) at low temperatures. Impact toughness and fracture toughness drop catastrophically below the DBT temperature, which can range from roughly −40 °C to well above room temperature depending on composition. This is why BCC ferritic and martensitic steels are generally excluded from cryogenic propellant-tank service; martensitic stainless steels are specifically excluded from LH2 applications because of intrinsically low fracture toughness (shabbirkhanUnknownyeard4.2identification pages 21-25). This represents a critical finding that room-temperature testing would entirely miss: a ferritic steel with adequate RT toughness may be completely brittle at 77 K or 20 K (strongly supported by well-established metallurgical principles, though specific numerical data for ferritic steels at cryogenic temperatures were not the focus of the retrieved papers).

### 2.3 HCP Alloys (Titanium)

For Ti-5Al-2.5Sn ELI (air-cooled), plane-strain fracture toughness K_Ic is 111 ksi√in (~101 ksi√in by compact tension) at 77 K and decreases to ~82–83 ksi√in at 20 K in the LT orientation (vanstone1977investigationofthe pages 75-78, vanstone1974theeffectof pages 42-45). Furnace-cooled ELI material shows lower toughness: 75 ksi√in at 77 K and 62–64 ksi√in at 20 K (vanstone1977investigationofthe pages 75-78, vanstone1974theeffectof pages 42-45). Air cooling improves ELI toughness by approximately 30% relative to furnace cooling, attributed to suppression of ordering in the alpha phase (stone1978influenceofcomposition pages 15-18). Fracture remains predominantly ductile (dimpled rupture via microvoid coalescence) even at 20 K, with deformation twinning playing an increasingly important role in cryogenic plasticity (vanstone1977investigationofthe pages 16-23, stone1978influenceofcomposition pages 31-34, vanstone1977investigationofthe pages 54-61). Extra-low interstitial (ELI) grade is essential: normal-interstitial Ti-5Al-2.5Sn has roughly half the cryogenic toughness of ELI material (stone1978influenceofcomposition pages 1-6).

### 2.4 Serrated/Discontinuous Plastic Flow and Adiabatic Heating at 4 K

A phenomenon unique to cryogenic temperatures—absent at room temperature—is serrated or discontinuous plastic flow. At 77 K and below, 304L stainless steel exhibits intermittent stress drops and stepwise displacement increases during tensile loading; at 300 K the flow is smooth (kim2023tensileandfracture pages 7-10). At 20 K, both small and large stress-drop events occur, with the behavior becoming more complex than at 77 K (kim2023tensileandfracture pages 7-10).

The physical mechanism involves catastrophic failure of Lomer–Cottrell dislocation locks: accumulated edge dislocations pile up against internal barriers, and when the local shear stress reaches the cohesive strength, the barrier collapses, producing an avalanche of dislocation motion and a sudden load drop (skoczen2010constitutivemodelof pages 3-4, skoczen2010constitutivemodelof pages 4-7). Because lattice specific heat approaches zero near absolute zero, even small amounts of plastic work cause large local temperature rises of ~40–50 K per serration event (skoczen2010constitutivemodelof pages 9-10). This adiabatic heating can temporarily suppress further serrations and alter the apparent stress–strain curve. Internal load-cell measurements at 4.2 K show that the mechanical stress drop precedes the temperature rise, establishing that dislocation-barrier failure is the primary trigger rather than thermal instability (skoczen2010constitutivemodelof pages 14-19). The constitutive model by Skoczeń et al. (doi: 10.1016/j.ijplas.2010.02.003) couples elastic response, plastic flow with Lomer–Cottrell lock density as an internal variable, and low-temperature phonon-based heat transport to reproduce serrated stress–strain curves (skoczen2010constitutivemodelof pages 9-10, skoczen2010constitutivemodelof pages 19-20, skoczen2010constitutivemodelof pages 1-3).

ASTM E1450 limits strain rates during cryogenic tensile testing specifically to control deformation-induced heating; excessively rapid displacement at 4 K or 20 K can raise specimen temperature and produce results resembling 77 K behavior (kim2023tensileandfracture pages 4-6).

### 2.5 Welds and Heat-Affected Zones

Weld integrity at cryogenic temperatures is a critical concern. During the Super Lightweight Tank development, Al-Li 2195 introduced significant weld-related challenges, including "significant production impacts" from rework and difficulties with complex-curvature welds; the program eventually returned complex-curvature components to Al 2219 (welzyn2011externaltankthestructure pages 6-9, welzyn2011externaltankthestructure pages 9-12). For austenitic stainless steels at 4 K, delta-ferrite, non-metallic inclusions, chromium-carbide precipitation, and coarse columnar grains reduce weld fracture toughness; submerged-arc welds are generally inferior to GTA and GMA welds at cryogenic temperatures (deimel1998strengthandtoughness pages 1-2). TIG and laser-beam weldments of cryogenic steels for fusion magnets achieved tensile strengths of 1555 and 1522 MPa (>97% of base metal) with K(J)Ic values of 210 and 241 MPa·m^0.5 at 4 K (dai2025developmentofcryogenic pages 8-10).

## 3. Failures, Anomalies, and Design-Allowable Gaps

**Space Shuttle External Tank Al-2090 cracking.** During the STS-133 launch campaign, cracking was discovered in five Al-2090 hat-shaped stringers at the intertank/LOX-tank interface. The initial crack was approximately nine inches long on each side. The root cause was that Al-2090's short-transverse capability was lower than expected while actual stresses—combining assembly-induced strains with cryogenically induced deflections during LOX tank filling—were higher than expected (smith2020lessonlearnedfrom pages 4-9, smith2020lessonlearnedfrom pages 1-4). Material specialists had warned against using Al-2090 in highly stressed regions, but the warning was lost. All five stringers were repaired and remaining Al-2090 stringers were reinforced with radius blocks (smith2020lessonlearnedfrom pages 4-9). This incident illustrates how inadequate characterization of anisotropic cryogenic properties can lead to structural failure.

**MMPDS/design-allowable gaps.** Advanced and newly developed materials, including AM alloys, are insufficiently characterized at cryogenic temperatures. Manufacturing variability produces substantial scatter in measured properties, forcing large margins between average measured strengths and allowable values (mital2006reviewofcurrent pages 10-13). The MMPDS handbook provides limited cryogenic data for many alloys; for LH2 tank materials, additional experimentation at actual service temperatures is required (shabbirkhanUnknownyeard4.2identification pages 21-25). For LPBF aluminum alloys specifically, AlSi10Mg had "no previously recorded mechanical data at 20 K" prior to recent studies (adams2023materialandscan pages 33-37), highlighting the near-complete absence of cryogenic design allowables for additively manufactured alloys.

## 4. Test Standards and Practice

**ASTM E1450** governs tensile testing of structural alloys in liquid helium; specimens are fully immersed, tested in displacement control at strain rates ≤10^−3 s^−1, with provisions for serrated yielding and adiabatic heating (perez2022mechanicaltestingof pages 15-18, castro2025mechanicalandmetallurgical pages 48-58). **ASTM E1820** covers elastic–plastic fracture toughness (J_Ic) measurement, including at cryogenic temperatures using the unloading-compliance method (kim2023tensileandfracture pages 4-6, kim2023tensileandfracture pages 13-16, castro2025mechanicalandmetallurgical pages 48-58). **ISO 6892-3:2015** applies to tensile testing from +10 °C to −196 °C using refrigeration, compressed gas, or liquid-nitrogen immersion with a 10-minute soak (perez2022mechanicaltestingof pages 12-15). **JIS Z 2277:2000** specifically covers tensile testing in liquid helium at ~4 K, with requirements for cryostat design, grips, alignment, and cryogenic extensometry (perez2022mechanicaltestingof pages 12-15). **ISO 6892-4:2015** governs tensile testing in liquid helium at 4 K (perez2022mechanicaltestingof pages 12-15). JIS Z 2284 covers elastic–plastic fracture-toughness J_Ic testing in liquid helium (kim2023tensileandfracture pages 17-18).

**Whether 77 K tests proxy for 20 K or 4 K service.** The evidence strongly indicates that 77 K liquid-nitrogen tests are not a reliable proxy for 20 K or 4 K behavior. For 304L, yield strength increases an additional 24% from 77 K to 20 K, UTS increases 12%, and J_Ic decreases by ~21% (kim2023tensileandfracture pages 7-10, kim2023tensileandfracture pages 13-16). Fracture morphology transitions from dimples at 300 K to mixed dimples and cleavage facets at 77 K and 20 K, with deeper secondary cracks at 20 K (kim2023tensileandfracture pages 13-16). Discontinuous yielding severity differs between 77 K and 20 K (kim2023tensileandfracture pages 7-10). Therefore, testing at the actual service temperature is necessary for qualification.

**Cost and helium scarcity.** Liquid helium costs approximately £20–25 per litre versus £0.50 per litre for liquid nitrogen—a 40–50× cost differential (perez2022mechanicaltestingof pages 10-12). A mechanical-testing cryostat may consume 25–30 litres of liquid helium during a single 30-minute cooldown (perez2022mechanicaltestingof pages 18-21). Helium recovery and reliquefaction systems add substantial infrastructure cost (perez2022mechanicaltestingof pages 21-23). This cost disparity means that many laboratories default to 77 K nitrogen testing, reserving true 20 K or 4 K testing for cases where direct characterization is essential. Temperatures below 77 K require liquid helium in addition to nitrogen pre-cooling (perez2022mechanicaltestingof pages 18-21, perez2022mechanicaltestingof pages 21-23), making helium availability a practical gate on whether sub-77 K tests are performed at all.

## 5. Hydrogen Compatibility at Cryogenic Temperature

At room temperature, electrochemical hydrogen charging of 304L stainless steel reduces the reduction in area from 78.3% to 66.4%, with distinct brittle fracture zones visible in fractography (kim2022metallicmaterialevaluation pages 13-16). At 20 K, however, additional hydrogen embrittlement was not clearly distinguishable from the ductility reduction caused by cryogenic temperature itself: fractures showed localized necking associated with discontinuous yielding rather than hydrogen-specific brittle features (kim2022metallicmaterialevaluation pages 13-16). Previous studies found hydrogen embrittlement effects to be negligible at liquid-hydrogen temperatures because extremely low temperatures reduce hydrogen-atom mobility, limiting diffusion into the lattice (kim2023tensileandfracture pages 1-2). For 304LN and 316LN tested at 20 K, liquid hydrogen reduced elongation by only 2–4% compared with gaseous helium, though relative reductions in area were 61% for 304LN and 77% for 316LN (kim2022metallicmaterialevaluation pages 2-4).

Austenitic stainless steels derive their hydrogen resistance from stable FCC structure; metastable grades such as 304 are less resistant than stable grades such as 310 and 316 because strain-induced martensite provides hydrogen trapping and crack initiation sites (qiu2021researchprogressof pages 3-5). Aluminum alloys are generally considered to have low sensitivity to hydrogen embrittlement in LH2 service (qiu2021researchprogressof pages 6-8). Nonetheless, evaluation under MSC.1/Circular.1622 for marine LH2 systems requires fracture-toughness (J_Ic or CTOD) testing specifically at 20 K in hydrogen-relevant environments, including assessment of welds and heat-affected zones (kim2023acomprehensivereview pages 26-27).

## Implications for BYU Vertical Cloud Lab LPBF Aluminum Alloys

The evidence strongly supports adding cryogenic mechanical testing to the BYU Vertical Cloud Lab's testing ladder. Key considerations include:

1. **LPBF aluminum alloys show substantial cryogenic strengthening.** SLM AlSi10Mg demonstrates ~93–105% UTS increase from RT to 20 K (from ~250 MPa to ~483–512 MPa) (adams2023materialandscan pages 43-47). LPBF Al10SiMg reaches 395 MPa UTS with 25% uniform elongation at 15 K (naeem2025enhancedstrengthand pages 1-2). LPBF AA2219 shows increased strength at 77 K with condition-dependent elongation changes (tumulu2025laserpowderbed pages 108-112). These gains cannot be predicted from room-temperature data alone.

2. **No cryogenic design allowables exist for LPBF alloys.** AlSi10Mg had no recorded 20 K mechanical data prior to recent studies (adams2023materialandscan pages 33-37). Novel compositions (critical-mineral-lean alloys with reduced Sc, Li, Ce) will have even less basis for cryogenic performance prediction.

3. **77 K testing with liquid nitrogen is a practical and informative first step,** given that it is ~40–50× cheaper than helium-based 4 K or 20 K testing (perez2022mechanicaltestingof pages 10-12). However, if LH2 tank service (20 K) is targeted, qualification at 20 K in liquid helium is ultimately necessary because properties differ significantly from 77 K values (kim2023tensileandfracture pages 4-6, kim2023tensileandfracture pages 13-16).

4. **Fracture toughness and fatigue testing** should accompany tensile testing, as the strength–toughness tradeoff at cryogenic temperatures is alloy- and microstructure-specific and cannot be extrapolated from tensile data alone (morris1991thestrengthand pages 10-12, walsh1996the4k pages 1-4).

5. **Weld and joint characterization** is critical if friction-stir or other joining methods are contemplated, as cryogenic weld performance can differ substantially from base metal (deimel1998strengthandtoughness pages 1-2, welzyn2011externaltankthestructure pages 6-9).

**Confidence assessment.** Claims about FCC alloy strengthening at cryogenic temperatures, serrated flow phenomena, test standards, and helium cost are strongly supported by multiple primary sources. Claims about specific Falcon 9, Ariane, and H-II/H3 cryogenic material qualification are weakly supported (mentioned only in general context). The Space Shuttle Al-2090 cracking incident and MMPDS gap claims are moderately supported by the retrieved NASA technical documents. Hydrogen compatibility claims at cryogenic temperature are moderately supported, with the consensus that hydrogen mobility is reduced at 20 K but that service-temperature testing remains necessary for qualification.

References

1. (mital2006reviewofcurrent pages 10-13): SK Mital, JZ Gyekenyesi, SM Arnold, and RM Sullivan. Review of current state of the art and key design issues with potential solutions for liquid hydrogen cryogenic storage tank structures for aircraft applications. Unknown journal, 2006.

2. (tzoumakis2024multiphysicsdigitalmodel pages 6-7): George Tzoumakis, Konstantinos Fotopoulos, and George Lampeas. Multi-physics digital model of an aluminum 2219 liquid hydrogen aircraft tank. Aerospace, 11:161, Feb 2024. URL: https://doi.org/10.3390/aerospace11020161, doi:10.3390/aerospace11020161. This article has 13 citations.

3. (qiu2021researchprogressof pages 6-8): Yinan Qiu, Huan Yang, Lige Tong, and Li Wang. Research progress of cryogenic materials for storage and transportation of liquid hydrogen. Metals, 11:1101, Jul 2021. URL: https://doi.org/10.3390/met11071101, doi:10.3390/met11071101. This article has 267 citations.

4. (shabbirkhanUnknownyeard4.2identification pages 12-14): S Shabbir-Khan, J Cooper, J De Courcy, and T Rendall. D4. 2 identification of materials for lh2 tank manufacture. Unknown journal, Unknown year.

5. (dai2025developmentofcryogenic pages 8-10): Jingjing Dai and Chuanjun Huang. Development of cryogenic structural steels for magnetic confinement fusion. Cryo, 1:13, Oct 2025. URL: https://doi.org/10.3390/cryo1040013, doi:10.3390/cryo1040013. This article has 2 citations.

6. (shindo2003cryogenicfractureand pages 1-2): Yasuhide Shindo and Katsumi Horiguchi. Cryogenic fracture and adiabatic heating of austenitic stainless steels for superconducting fusion magnets. Science and Technology of Advanced Materials, 4:319-326, Jan 2003. URL: https://doi.org/10.1016/s1468-6996(03)00063-9, doi:10.1016/s1468-6996(03)00063-9. This article has 25 citations and is from a peer-reviewed journal.

7. (mcrae2017fatigueandfracture pages 1-3): D M McRae, S Balachandran, and R P Walsh. Fatigue and fracture of three austenitic stainless steels at cryogenic temperatures. IOP Conference Series: Materials Science and Engineering, 279:012001, Dec 2017. URL: https://doi.org/10.1088/1757-899x/279/1/012001, doi:10.1088/1757-899x/279/1/012001. This article has 24 citations.

8. (qiu2021researchprogressof pages 8-9): Yinan Qiu, Huan Yang, Lige Tong, and Li Wang. Research progress of cryogenic materials for storage and transportation of liquid hydrogen. Metals, 11:1101, Jul 2021. URL: https://doi.org/10.3390/met11071101, doi:10.3390/met11071101. This article has 267 citations.

9. (hafley2011evaluationofaluminum pages 24-28): RA Hafley, MS Domack, SJ Hales, and RN Shenoy. Evaluation of aluminum alloy 2050-t84 microstructure and mechanical properties at ambient and cryogenic temperatures. Unknown journal, 2011.

10. (kim2023tensileandfracture pages 7-10): Myung-Sung Kim, Taehyun Lee, Jong-Won Park, and Yongjin Kim. Tensile and fracture characteristics of 304l stainless steel at cryogenic temperatures for liquid hydrogen service. Metals, 13:1774, Oct 2023. URL: https://doi.org/10.3390/met13101774, doi:10.3390/met13101774. This article has 34 citations.

11. (walsh1996the4k pages 1-4): RP Walsh and LT Summers. The 4 k tensile and fracture toughness properties of a modified 316ln conduit alloy. Unknown journal, 1996.

12. (vanstone1977investigationofthe pages 75-78): RH Vanstone, JR Low Jr, and JL Shannon Jr. Investigation of the fracture mechanism in ti-5al-2.5 sn at cryogenic temperatures. Unknown journal, 1977.

13. (vanstone1974theeffectof pages 42-45): RH Vanstone, JR Low Jr, and JL Shannon Jr. The effect of microstructure on the fracture toughness of titanium alloys. Unknown journal, 1974.

14. (adams2023materialandscan pages 43-47): Reece Michael Adams. Material and scan spacing variation for improved mechanical performance of additively manufactured materials at cryogenic temperatures. Text, Jan 2023. URL: https://doi.org/10.7273/000004509, doi:10.7273/000004509. This article has 2 citations and is from a peer-reviewed journal.

15. (hafley2011evaluationofaluminuma pages 21-24): RA Hafley, MS Domack, SJ Hales, and RN Shenoy. Evaluation of aluminum alloy 2050-t84 microstructure and mechanical properties at ambient and cryogenic temperatures. Unknown journal, 2011.

16. (kim2022metallicmaterialevaluation pages 5-9): Myung-Sung Kim, Taehyun Lee, Yeonhong Son, Junesung Park, Minsung Kim, Hyeonjun Eun, Jong-Won Park, and Yongjin Kim. Metallic material evaluation of liquid hydrogen storage tank for marine application using a tensile cryostat for 20 k and electrochemical cell. Processes, 10:2401, Nov 2022. URL: https://doi.org/10.3390/pr10112401, doi:10.3390/pr10112401. This article has 41 citations.

17. (qiu2021researchprogressof pages 5-6): Yinan Qiu, Huan Yang, Lige Tong, and Li Wang. Research progress of cryogenic materials for storage and transportation of liquid hydrogen. Metals, 11:1101, Jul 2021. URL: https://doi.org/10.3390/met11071101, doi:10.3390/met11071101. This article has 267 citations.

18. (kim2023tensileandfracture pages 13-16): Myung-Sung Kim, Taehyun Lee, Jong-Won Park, and Yongjin Kim. Tensile and fracture characteristics of 304l stainless steel at cryogenic temperatures for liquid hydrogen service. Metals, 13:1774, Oct 2023. URL: https://doi.org/10.3390/met13101774, doi:10.3390/met13101774. This article has 34 citations.

19. (shabbirkhanUnknownyeard4.2identification pages 21-25): S Shabbir-Khan, J Cooper, J De Courcy, and T Rendall. D4. 2 identification of materials for lh2 tank manufacture. Unknown journal, Unknown year.

20. (stone1978influenceofcomposition pages 15-18): RH Van Stone and WS Pierce. Influence of composition, annealing treat-ment, and texture on the fracture tough. Unknown journal, 1978.

21. (vanstone1977investigationofthe pages 16-23): RH Vanstone, JR Low Jr, and JL Shannon Jr. Investigation of the fracture mechanism in ti-5al-2.5 sn at cryogenic temperatures. Unknown journal, 1977.

22. (stone1978influenceofcomposition pages 31-34): RH Van Stone and WS Pierce. Influence of composition, annealing treat-ment, and texture on the fracture tough. Unknown journal, 1978.

23. (vanstone1977investigationofthe pages 54-61): RH Vanstone, JR Low Jr, and JL Shannon Jr. Investigation of the fracture mechanism in ti-5al-2.5 sn at cryogenic temperatures. Unknown journal, 1977.

24. (stone1978influenceofcomposition pages 1-6): RH Van Stone and WS Pierce. Influence of composition, annealing treat-ment, and texture on the fracture tough. Unknown journal, 1978.

25. (skoczen2010constitutivemodelof pages 3-4): B. Skoczeń, J. Bielski, S. Sgobba, and D. Marcinek. Constitutive model of discontinuous plastic flow at cryogenic temperatures. International Journal of Plasticity, 26:1659-1679, Dec 2010. URL: https://doi.org/10.1016/j.ijplas.2010.02.003, doi:10.1016/j.ijplas.2010.02.003. This article has 81 citations and is from a highest quality peer-reviewed journal.

26. (skoczen2010constitutivemodelof pages 4-7): B. Skoczeń, J. Bielski, S. Sgobba, and D. Marcinek. Constitutive model of discontinuous plastic flow at cryogenic temperatures. International Journal of Plasticity, 26:1659-1679, Dec 2010. URL: https://doi.org/10.1016/j.ijplas.2010.02.003, doi:10.1016/j.ijplas.2010.02.003. This article has 81 citations and is from a highest quality peer-reviewed journal.

27. (skoczen2010constitutivemodelof pages 9-10): B. Skoczeń, J. Bielski, S. Sgobba, and D. Marcinek. Constitutive model of discontinuous plastic flow at cryogenic temperatures. International Journal of Plasticity, 26:1659-1679, Dec 2010. URL: https://doi.org/10.1016/j.ijplas.2010.02.003, doi:10.1016/j.ijplas.2010.02.003. This article has 81 citations and is from a highest quality peer-reviewed journal.

28. (skoczen2010constitutivemodelof pages 14-19): B. Skoczeń, J. Bielski, S. Sgobba, and D. Marcinek. Constitutive model of discontinuous plastic flow at cryogenic temperatures. International Journal of Plasticity, 26:1659-1679, Dec 2010. URL: https://doi.org/10.1016/j.ijplas.2010.02.003, doi:10.1016/j.ijplas.2010.02.003. This article has 81 citations and is from a highest quality peer-reviewed journal.

29. (skoczen2010constitutivemodelof pages 19-20): B. Skoczeń, J. Bielski, S. Sgobba, and D. Marcinek. Constitutive model of discontinuous plastic flow at cryogenic temperatures. International Journal of Plasticity, 26:1659-1679, Dec 2010. URL: https://doi.org/10.1016/j.ijplas.2010.02.003, doi:10.1016/j.ijplas.2010.02.003. This article has 81 citations and is from a highest quality peer-reviewed journal.

30. (skoczen2010constitutivemodelof pages 1-3): B. Skoczeń, J. Bielski, S. Sgobba, and D. Marcinek. Constitutive model of discontinuous plastic flow at cryogenic temperatures. International Journal of Plasticity, 26:1659-1679, Dec 2010. URL: https://doi.org/10.1016/j.ijplas.2010.02.003, doi:10.1016/j.ijplas.2010.02.003. This article has 81 citations and is from a highest quality peer-reviewed journal.

31. (kim2023tensileandfracture pages 4-6): Myung-Sung Kim, Taehyun Lee, Jong-Won Park, and Yongjin Kim. Tensile and fracture characteristics of 304l stainless steel at cryogenic temperatures for liquid hydrogen service. Metals, 13:1774, Oct 2023. URL: https://doi.org/10.3390/met13101774, doi:10.3390/met13101774. This article has 34 citations.

32. (welzyn2011externaltankthestructure pages 6-9): K Welzyn, JC Pilet, and D Diecidue-Conners. External tank-the structure backbone. Unknown journal, 2011.

33. (welzyn2011externaltankthestructure pages 9-12): K Welzyn, JC Pilet, and D Diecidue-Conners. External tank-the structure backbone. Unknown journal, 2011.

34. (deimel1998strengthandtoughness pages 1-2): P. Deimel, H. Fischer, and M. Hoffmann. Strength and toughness properties of two nitrogen alloyed stainless steels and their submerged arc weldments at cryogenic temperatures. Journal of Materials Science, 33:1105-1116, Feb 1998. URL: https://doi.org/10.1023/a:1004301004055, doi:10.1023/a:1004301004055. This article has 14 citations and is from a peer-reviewed journal.

35. (smith2020lessonlearnedfrom pages 4-9): James Smith, Kenneth Hamm Jr, Kauser Imtiaz, and Ivatury S. Raju. Lesson learned from recent space flight assessments. ArXiv, Jan 2020. URL: https://doi.org/10.2514/6.2020-0246, doi:10.2514/6.2020-0246. This article has 2 citations.

36. (smith2020lessonlearnedfrom pages 1-4): James Smith, Kenneth Hamm Jr, Kauser Imtiaz, and Ivatury S. Raju. Lesson learned from recent space flight assessments. ArXiv, Jan 2020. URL: https://doi.org/10.2514/6.2020-0246, doi:10.2514/6.2020-0246. This article has 2 citations.

37. (adams2023materialandscan pages 33-37): Reece Michael Adams. Material and scan spacing variation for improved mechanical performance of additively manufactured materials at cryogenic temperatures. Text, Jan 2023. URL: https://doi.org/10.7273/000004509, doi:10.7273/000004509. This article has 2 citations and is from a peer-reviewed journal.

38. (perez2022mechanicaltestingof pages 15-18): N Salmeron Perez, R M Shaw, and M R L Gower. Mechanical testing of fibre-reinforced polymer matrix composites at cryogenic temperatures. requirements for mechanical test capability at -269°c (4 k). Unknown journal, Jun 2022. URL: https://doi.org/10.47120/npl.mat102, doi:10.47120/npl.mat102.

39. (castro2025mechanicalandmetallurgical pages 48-58): E Rodríguez Castro. Mechanical and metallurgical assessment of austenitic stainless steel as structural materials for superconducting high field magnets at cryogenic temperature. Unknown journal, 2025.

40. (perez2022mechanicaltestingof pages 12-15): N Salmeron Perez, R M Shaw, and M R L Gower. Mechanical testing of fibre-reinforced polymer matrix composites at cryogenic temperatures. requirements for mechanical test capability at -269°c (4 k). Unknown journal, Jun 2022. URL: https://doi.org/10.47120/npl.mat102, doi:10.47120/npl.mat102.

41. (kim2023tensileandfracture pages 17-18): Myung-Sung Kim, Taehyun Lee, Jong-Won Park, and Yongjin Kim. Tensile and fracture characteristics of 304l stainless steel at cryogenic temperatures for liquid hydrogen service. Metals, 13:1774, Oct 2023. URL: https://doi.org/10.3390/met13101774, doi:10.3390/met13101774. This article has 34 citations.

42. (perez2022mechanicaltestingof pages 10-12): N Salmeron Perez, R M Shaw, and M R L Gower. Mechanical testing of fibre-reinforced polymer matrix composites at cryogenic temperatures. requirements for mechanical test capability at -269°c (4 k). Unknown journal, Jun 2022. URL: https://doi.org/10.47120/npl.mat102, doi:10.47120/npl.mat102.

43. (perez2022mechanicaltestingof pages 18-21): N Salmeron Perez, R M Shaw, and M R L Gower. Mechanical testing of fibre-reinforced polymer matrix composites at cryogenic temperatures. requirements for mechanical test capability at -269°c (4 k). Unknown journal, Jun 2022. URL: https://doi.org/10.47120/npl.mat102, doi:10.47120/npl.mat102.

44. (perez2022mechanicaltestingof pages 21-23): N Salmeron Perez, R M Shaw, and M R L Gower. Mechanical testing of fibre-reinforced polymer matrix composites at cryogenic temperatures. requirements for mechanical test capability at -269°c (4 k). Unknown journal, Jun 2022. URL: https://doi.org/10.47120/npl.mat102, doi:10.47120/npl.mat102.

45. (kim2022metallicmaterialevaluation pages 13-16): Myung-Sung Kim, Taehyun Lee, Yeonhong Son, Junesung Park, Minsung Kim, Hyeonjun Eun, Jong-Won Park, and Yongjin Kim. Metallic material evaluation of liquid hydrogen storage tank for marine application using a tensile cryostat for 20 k and electrochemical cell. Processes, 10:2401, Nov 2022. URL: https://doi.org/10.3390/pr10112401, doi:10.3390/pr10112401. This article has 41 citations.

46. (kim2023tensileandfracture pages 1-2): Myung-Sung Kim, Taehyun Lee, Jong-Won Park, and Yongjin Kim. Tensile and fracture characteristics of 304l stainless steel at cryogenic temperatures for liquid hydrogen service. Metals, 13:1774, Oct 2023. URL: https://doi.org/10.3390/met13101774, doi:10.3390/met13101774. This article has 34 citations.

47. (kim2022metallicmaterialevaluation pages 2-4): Myung-Sung Kim, Taehyun Lee, Yeonhong Son, Junesung Park, Minsung Kim, Hyeonjun Eun, Jong-Won Park, and Yongjin Kim. Metallic material evaluation of liquid hydrogen storage tank for marine application using a tensile cryostat for 20 k and electrochemical cell. Processes, 10:2401, Nov 2022. URL: https://doi.org/10.3390/pr10112401, doi:10.3390/pr10112401. This article has 41 citations.

48. (qiu2021researchprogressof pages 3-5): Yinan Qiu, Huan Yang, Lige Tong, and Li Wang. Research progress of cryogenic materials for storage and transportation of liquid hydrogen. Metals, 11:1101, Jul 2021. URL: https://doi.org/10.3390/met11071101, doi:10.3390/met11071101. This article has 267 citations.

49. (kim2023acomprehensivereview pages 26-27): Myung-Sung Kim and Kang Woo Chun. A comprehensive review on material compatibility and safety standards for liquid hydrogen cargo and fuel containment systems in marine applications. Journal of Marine Science and Engineering, 11:1927, Oct 2023. URL: https://doi.org/10.3390/jmse11101927, doi:10.3390/jmse11101927. This article has 48 citations.

50. (naeem2025enhancedstrengthand pages 1-2): Muhammad Naeem, Asif Ur Rehman, Liliana Romero Resendiz, Elmas Salamci, Huseyin Aydin, Peyman Ansari, Stefanus Harjo, Wu Gong, Yusuf Usta, Olcay Ersel Canyurt, Xun-Li Wang, and Metin U. Salamci. Enhanced strength and ductility in an additively manufactured al10simg alloy at cryogenic temperatures. Communications Materials, Apr 2025. URL: https://doi.org/10.1038/s43246-025-00793-4, doi:10.1038/s43246-025-00793-4. This article has 5 citations and is from a peer-reviewed journal.

51. (tumulu2025laserpowderbed pages 108-112): SK Tumulu. Laser powder bed fusion additive manufacturing (lpbf-am) of aluminum-copper alloys. Unknown journal, 2025.

52. (morris1991thestrengthand pages 10-12): JW Morris. The strength and toughness of stainless steels at cryogenic temperature. Unknown journal, 1991.
