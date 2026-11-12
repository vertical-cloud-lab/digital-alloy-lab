<!--
Edison Scientific LITERATURE_HIGH (job-futurehouse-paperqa3-high)
Task ID: c690cb5a-afe5-4b91-87eb-7a59884a1a71
Submitted: 2026-11-12T16:41:09Z; fetched: 2026-11-12T17:04:48Z; status: success; has_successful_answer: True
Retrieved with edison-client 0.18.0 (EDISON_PLATFORM_API_KEY) from GitHub Actions for issue #254. The full trajectory is in the .trajectory.json file beside this one.
-->

**Question (LITERATURE_HIGH):** What is known, with quantitative data, citations and DOIs, about the cryogenic mechanical behavior of aluminum alloys used or proposed for aerospace cryogenic structures? Cover: (1) Wrought alloys: 2219 and 2014 (Al-Cu); 2195, 2050, 2060, 2098, 2198 and other Al-Li alloys; 5083, 5456 and 5182 (Al-Mg); 6061; 7050 and 7075. Give yield strength, tensile strength, elongation and fracture toughness at 295 K, 77 K, 20 K and 4 K. Explain why most aluminum alloys become both stronger and more ductile at cryogenic temperature (work-hardening and dislocation storage, suppression of Portevin-Le Chatelier serrations, T1 and delta-prime precipitates and grain-boundary effects in Al-Li), and the exceptions (alloys or tempers whose toughness drops, delamination in Al-Li plate). (2) Welds: friction stir and fusion welds of 2219 and 2195 at cryogenic temperature (Shuttle super-lightweight tank, SLS core stage, Falcon 9). (3) Additively manufactured aluminum: LPBF AlSi10Mg, AlSi7Mg/A357, Scalmalloy (Al-Mg-Sc-Zr), A20X/A205, Al-Cu-Ce, Al-Fe-Zr, Al-Mn-Sc, and 2219/2319 by wire-arc additive manufacturing: any data at 77 K or below, and the effect of porosity, the eutectic silicon network, anisotropy and heat treatment on cryogenic ductility and toughness. (4) Keep cryogenic service testing separate from cryogenic processing (cryorolling, deep cryogenic treatment) and say briefly what the processing literature shows. (5) Gaps: which aluminum alloy classes, especially AM alloys and alloys lean in Sc, Li or rare earths, lack cryogenic property data. Context: the BYU Vertical Cloud Lab designs aluminum alloys for laser powder bed fusion (LPBF) with AI and CALPHAD, including critical-mineral-lean compositions (less Sc, Li, Ce), makes its own powder by ultrasonic atomization, and tests in a ladder of single tracks, density cubes and tensile bars. It is deciding whether and how to add cryogenic mechanical testing. Prefer primary sources, NASA/NIST technical reports and standards; give DOIs or report numbers; give numbers with temperatures and units; and say which claims are strongly vs. weakly supported.

---

Question: What is known, with quantitative data, citations and DOIs, about the cryogenic mechanical behavior of aluminum alloys used or proposed for aerospace cryogenic structures? Cover: (1) Wrought alloys: 2219 and 2014 (Al-Cu); 2195, 2050, 2060, 2098, 2198 and other Al-Li alloys; 5083, 5456 and 5182 (Al-Mg); 6061; 7050 and 7075. Give yield strength, tensile strength, elongation and fracture toughness at 295 K, 77 K, 20 K and 4 K. Explain why most aluminum alloys become both stronger and more ductile at cryogenic temperature (work-hardening and dislocation storage, suppression of Portevin-Le Chatelier serrations, T1 and delta-prime precipitates and grain-boundary effects in Al-Li), and the exceptions (alloys or tempers whose toughness drops, delamination in Al-Li plate). (2) Welds: friction stir and fusion welds of 2219 and 2195 at cryogenic temperature (Shuttle super-lightweight tank, SLS core stage, Falcon 9). (3) Additively manufactured aluminum: LPBF AlSi10Mg, AlSi7Mg/A357, Scalmalloy (Al-Mg-Sc-Zr), A20X/A205, Al-Cu-Ce, Al-Fe-Zr, Al-Mn-Sc, and 2219/2319 by wire-arc additive manufacturing: any data at 77 K or below, and the effect of porosity, the eutectic silicon network, anisotropy and heat treatment on cryogenic ductility and toughness. (4) Keep cryogenic service testing separate from cryogenic processing (cryorolling, deep cryogenic treatment) and say briefly what the processing literature shows. (5) Gaps: which aluminum alloy classes, especially AM alloys and alloys lean in Sc, Li or rare earths, lack cryogenic property data. Context: the BYU Vertical Cloud Lab designs aluminum alloys for laser powder bed fusion (LPBF) with AI and CALPHAD, including critical-mineral-lean compositions (less Sc, Li, Ce), makes its own powder by ultrasonic atomization, and tests in a ladder of single tracks, density cubes and tensile bars. It is deciding whether and how to add cryogenic mechanical testing. Prefer primary sources, NASA/NIST technical reports and standards; give DOIs or report numbers; give numbers with temperatures and units; and say which claims are strongly vs. weakly supported.

# Cryogenic Mechanical Behavior of Aluminum Alloys for Aerospace Cryogenic Structures

## 1. Wrought Alloys

### 1.1 Al-Cu Alloys (2219, 2014)

Aluminum alloy 2219-T87 has been the workhorse cryogenic tank alloy since the Space Shuttle External Tank program. Its strength–toughness combination improves dramatically as temperature decreases from 295 K toward 4 K; yield strength increases only modestly, but fracture toughness and tensile elongation increase substantially (morris1988mechanicalpropertiesof pages 8-11, morris1988mechanicalpropertiesof pages 6-8). The fracture mode in 2219-T87 does not change between room temperature and cryogenic conditions—it remains brittle transgranular shear—which is consistent with the toughness gain being driven by enhanced work hardening rather than a fracture-mode transition (rao1989cryogenictoughnessof pages 4-6). Quantitative 2219-T87 property data at specific temperatures (77 K, 20 K, 4 K) are compiled in the NASA MMPDS/MIL-HDBK-5 database and the Cryogenic Materials Data Handbook (DOI: 10.21236/ad0420406) (schwartzberg1964cryogenicmaterialsdata pages 43-51), but the data in the retrieved handbook sections are presented primarily as figures rather than tables. Published values from the literature indicate typical room-temperature properties of approximately YS ≈ 352 MPa, UTS ≈ 455 MPa, with significant increases at 77 K and 20 K. Alloy 2014 data at cryogenic temperatures also exist in the Cryogenic Materials Data Handbook but were not extracted in numerical form from the available sources.

### 1.2 Al-Li Alloys (2195, 2050, 2090, 2091, 8090, 8091)

**2195-T8** is the primary alloy for the Space Shuttle Super Lightweight Tank (SLWT) and the SLS core stage. At 298 K, 2195-T8 exhibits YS = 586 MPa and UTS = 614 MPa; at 20 K, these increase to YS = 724 MPa (+23.5%) and UTS = 859 MPa (+39.9%), with elongation rising from approximately 11% to approximately 14% (wang2023influenceofcryogenic pages 4-6, wang2023influenceofcryogenic pages 2-4). At 77 K in the L orientation (1.85-inch thick plate), YS = 641 MPa (93 ksi), UTS = 696 MPa (101 ksi), and elongation = 10.9%; in the LT orientation, YS = 634 MPa (92 ksi), UTS = 717 MPa (104 ksi), and elongation = 7.6% (hafley2011evaluationofaluminuma pages 24-28, hafley2011evaluationofaluminumb pages 24-28). The fracture toughness behavior of 2195 is temper- and orientation-dependent: published data show a minimal increase or possible decrease from 295 K to 77 K depending on orientation, followed by a significant increase at 20 K (hafley2011evaluationofaluminuma pages 24-28). Chen et al. (1998, DOI: 10.1361/105994998770347576) demonstrated that the fracture toughness ratio (FTR = cryogenic KIc / ambient KIc) correlates with the size of T1 (Al₂CuLi) precipitates at subgrain boundaries: large subgrain-boundary T1 degrades cryogenic toughness, while MSRC aging that promotes finer matrix T1 and suppresses subgrain-boundary T1 can improve FTR by more than 15% (chen1998theeffectsof pages 2-4, chen1998theeffectsof pages 4-6).

**2050-T84** was evaluated by NASA Langley as a potential cryogenic tank alloy. At 77 K (−320 °F), the longitudinal t/6 location exhibited YS = 562 MPa (81.5 ksi), UTS = 612 MPa (88.8 ksi), and total elongation = 16.9% (hafley2011evaluationofaluminuma pages 28-34, hafley2011evaluationofaluminum pages 28-34). Conditional fracture toughness (KQ,JIC, not validated KIc) at 77 K varied by orientation: L-T = 35.6 MPa√m (decreased from 42.2 at RT), T-L = 31.0 MPa√m (increased from 27.3), and L-S = 48.8 MPa√m (increased from 41.4) (hafley2011evaluationofaluminum pages 24-28, hafley2011evaluationofaluminuma pages 24-28). No 20 K data were generated; testing at −423 °F was recommended as future work (hafley2011evaluationofaluminuma pages 28-34).

**2090-T8E41** (Al-2.7Cu-2.2Li-0.1Zr), a first-generation Al-Li alloy, shows the most dramatic cryogenic improvement of any commercial aluminum alloy. Rao and Ritchie (1989, DOI: 10.1007/BF02653929) reported (L orientation): at 298 K, YS = 552 MPa, UTS = 589 MPa, elongation = 11%, KIc = 36 MPa√m (L-T); at 77 K, YS = 587 MPa, UTS = 642 MPa, elongation = 14%, KIc = 51 MPa√m (L-T)—a 42% toughness increase (rao1989cryogenictoughnessof pages 4-6). The strain-hardening exponent increased from 0.06 to 0.15. Morris and Glazer (1988) noted that the combined strength–toughness of 2090-T81 at 4–77 K was substantially superior to any other commercially available aluminum alloy (morris1988mechanicalpropertiesofb pages 1-6, morris1988mechanicalpropertiesofa pages 1-6).

**2091-T351** showed: at 298 K, YS = 369 MPa, UTS = 451 MPa, elongation = 10%, KIc = 33 MPa√m (L-T, KQ); at 77 K, YS = 442 MPa, UTS = 596 MPa, elongation = 16%, KIc = 41 MPa√m (rao1989cryogenictoughnessof pages 4-6). However, **2091-T8X** (peak-aged) exhibited decreased L-T toughness at 77 K: KIc dropped from 46 to 44 MPa√m, while S-L toughness decreased from 25 to 16 MPa√m, accompanied by a fracture-mode transition from ductile void coalescence to brittle transgranular shear with intergranular delamination (rao1989cryogenictoughnessof pages 1-2, rao1989cryogenictoughnessof pages 4-6).

**8091-T8X** showed an exceptional cryogenic toughness increase: L-T KIc rose from 20 MPa√m at 298 K to 38 MPa√m at 77 K, while elongation doubled from 6% to 12% (rao1989cryogenictoughnessof pages 4-6).

The following table summarizes available wrought alloy cryogenic data:

| Alloy/Temper | Temperature (K) | Yield Strength (MPa) | UTS (MPa) | Elongation (%) | Fracture Toughness, KIC (MPa√m) | Source |
|---|---:|---:|---:|---:|---:|---|
| 2195-T8, L | 298 | 586 | 614 | ≈11 | — | Wang et al., DOI: 10.3390/met13040740 (wang2023influenceofcryogenic pages 4-6) |
| 2195-T8, L | 77 | 641 | 696 | 10.9 | — | Hafley et al., NASA evaluation (hafley2011evaluationofaluminuma pages 24-28) |
| 2195-T8 | 20 | 724 | 859 | ≈14 | — | Wang et al., DOI: 10.3390/met13040740 (wang2023influenceofcryogenic pages 4-6) |
| 2050-T84 plate | 298 | — | — | — | **Conditional KQ,JIC:** 42.2 L–T; 27.3 T–L; 41.4 L–S | Hafley et al.; values did not satisfy ASTM E1820 validity (hafley2011evaluationofaluminum pages 24-28) |
| 2050-T84, L, t/6 | 77 | 562 | 612 | 16.9 | **Conditional KQ,JIC:** 35.6 L–T; 31.0 T–L; 48.8 L–S | Hafley et al.; tensile and conditional toughness results (hafley2011evaluationofaluminum pages 24-28, hafley2011evaluationofaluminuma pages 28-34) |
| 2090-T8E41, L | 298 | 552 | 589 | 11 | 36 L–T; 17 S–L | Rao et al., DOI: 10.1007/BF02653929 (rao1989cryogenictoughnessof pages 4-6) |
| 2090-T8E41, L | 77 | 587 | 642 | 14 | 51 L–T; 15 S–L | Rao et al., DOI: 10.1007/BF02653929 (rao1989cryogenictoughnessof pages 4-6) |
| 2091-T351, L | 298 | 369 | 451 | 10 | 33 L–T **(KQ)**; 19 S–L | Rao et al., DOI: 10.1007/BF02653929 (rao1989cryogenictoughnessof pages 4-6) |
| 2091-T351, L | 77 | 442 | 596 | 16 | 41 L–T **(KQ)**; 17 S–L | Rao et al., DOI: 10.1007/BF02653929 (rao1989cryogenictoughnessof pages 4-6) |
| 2091-T8X, L | 298 | 425 | 481 | 8 | 46 L–T **(KQ)**; 25 S–L | Rao et al., DOI: 10.1007/BF02653929 (rao1989cryogenictoughnessof pages 4-6) |
| 2091-T8X, L | 77 | 483 | 610 | 14 | 44 L–T **(KQ)**; 16 S–L | Rao et al., DOI: 10.1007/BF02653929 (rao1989cryogenictoughnessof pages 4-6) |
| 8091-T8X, L | 298 | 537 | 581 | 6 | 20 L–T; 9 S–L | Rao et al., DOI: 10.1007/BF02653929 (rao1989cryogenictoughnessof pages 4-6) |
| 8091-T8X, L | 77 | 574 | 697 | 12 | 38 L–T; 8 S–L | Rao et al., DOI: 10.1007/BF02653929 (rao1989cryogenictoughnessof pages 4-6) |
| 6061-T651 | 20 | — | ≈535 | Not resolved | — | Adams, DOI: 10.7273/000004509 (adams2023materialandscan pages 37-43) |


*Table: Reported tensile and fracture-toughness properties for selected wrought aluminum alloys at ambient and cryogenic temperatures. Orientation and ASTM-validity qualifications are retained because toughness values are not interchangeable across crack orientations or between KIC and conditional KQ,JIC results.*

### 1.3 Al-Mg Alloys (5083, 5456, 5182)

Alloy 5456 was used in the first stage of the Saturn I and Saturn IB launch vehicles and in cryogenic tanks and equipment (schwartzberg1964cryogenicmaterialsdata pages 22-26, schwartzberg1964cryogenicmaterialsdata pages 29-33). The Cryogenic Materials Data Handbook (DOI: 10.21236/ad0420406) contains extensive cryogenic property data for 5456 in various tempers (H321, H343, O), presented primarily as figures showing tensile strength, yield strength, elongation, and notch strength as functions of temperature from −423 °F (20 K) to room temperature (schwartzberg1964cryogenicmaterialsdata pages 43-51, schwartzberg1964cryogenicmaterialsdata pages 51-55). Alloy 5083-O is widely used for LNG tank construction. Both 5xxx alloys generally show increasing strength and maintained or improved ductility at cryogenic temperatures, consistent with FCC behavior. Alloy 5182 data at cryogenic service temperatures were not identified in the retrieved literature.

### 1.4 6061

Alloy 6061-T651 at 20 K exhibited a mean UTS of approximately 535 ± 28 MPa, compared with a room-temperature value of 497 ± 8 MPa (adams2023materialandscan pages 37-43). The Ekin (2011) appendix tables list a room-temperature 0.2% YS of 275 MPa for 6061-T87, with elastic-property data at cryogenic temperatures (ekin2011appendixdatatables pages 155-158). Lee and Huang (2016, DOI: 10.2320/matertrans.m2015170) investigated the mechanical properties and dislocation substructure of 6061-T6 at cryogenic impact temperatures, confirming enhanced work hardening at low temperatures.

### 1.5 7xxx Alloys (7050, 7075)

Alloy 7075-T6 represents an important exception to the general trend of cryogenic improvement. Direct measurements have shown that the fracture toughness of 7075 **decreases** between room temperature and 77 K (morris1988mechanicalpropertiesof pages 11-13). Morris and Glazer (1988) reported that Saji et al. observed increasing toughness (as estimated by work to fracture) and elongation in 7075 down to a peak at approximately 30 K, followed by decreasing values from 30 K to 4 K, with the peak associated with maximum laminar splitting (morris1988mechanicalpropertiesof pages 11-13). This is consistent with the behavior reported by Rao and Ritchie (1989) for 7075-T6 and 7475-T6, which undergo a fracture-mode transition from ductile tearing (void coalescence) to brittle transgranular shear at lower temperatures, reducing toughness (rao1989cryogenictoughnessof pages 4-6). Alloy 7050 cryogenic data were not found in the retrieved literature.

## 2. Mechanisms of Cryogenic Strengthening and Ductility Enhancement

### 2.1 Why Most Aluminum Alloys Become Stronger and More Ductile at Cryogenic Temperature

The general improvement in mechanical properties of FCC aluminum alloys at cryogenic temperatures is well established and is governed by several interacting mechanisms (strongly supported):

**Work hardening and dislocation storage.** At low temperatures, thermally activated processes such as cross-slip and dynamic recovery are suppressed, so dislocations accumulate more rapidly during plastic deformation. In 2195-T8, dislocation density increased from approximately 2 × 10¹⁴ m⁻² at 298 K to 5 × 10¹⁴ m⁻² at 20 K under similar deformation (wang2023influenceofcryogenic pages 9-12). EBSD and TEM analyses confirm denser dislocation tangles and finer cellular substructure at 77 K (zhang2021cryogenicdeformationbehavior pages 8-11). This increased dislocation density directly raises flow stress and the strain-hardening rate.

**Considère criterion and delayed necking.** Morris and Glazer (1988) showed using Considère plots for 2090-T81 that the increased strain-hardening rate at low temperature postpones the tensile instability point (dσ/dε = σ) to larger strains, extending uniform elongation (morris1988mechanicalpropertiesof pages 11-13, morris1988mechanicalpropertiesofb pages 8-11). All 2090-T81 specimens failed at or beyond the Considère criterion, even when no observable necking occurred.

**Suppression of Portevin–Le Chatelier (PLC) serrations.** PLC effects, caused by dynamic strain aging from solute–dislocation interactions, are suppressed at low temperatures and high strain rates because solute atoms (particularly Mg in 5xxx alloys) cannot diffuse fast enough to pin mobile dislocations. At cryogenic temperatures, PLC serrations disappear, producing smoother, more uniform plastic flow (naeem2025enhancedstrengthand pages 1-2). In LPBF A205, serrated flow present at room temperature was eliminated at −196 °C (tumulu2025laserpowderbeda pages 158-162).

**T1 and δ′ precipitate effects in Al-Li alloys.** In 2195 and other Al-Cu-Li alloys, the T1 (Al₂CuLi) precipitate is the primary strengthening phase. Its interaction with dislocations at low temperature contributes to enhanced work hardening. The location and size of T1 critically affect cryogenic fracture toughness: large T1 at subgrain boundaries degrades the cryogenic FTR, while fine matrix T1 enhances it (chen1998theeffectsof pages 2-4, chen1998theeffectsof pages 4-6).

**Delamination toughening in Al-Li alloys.** In alloys with unrecrystallized, pancake-shaped grain structures (2090, 2091, 8091), short-transverse delamination cracks perpendicular to the main crack plane become more numerous and deeper at lower temperatures. In crack-divider orientations (L-T), this reduces through-thickness constraint and places each ligament closer to plane-stress conditions, where Kc is higher. For 2090-T8E41, Rao and Ritchie modeled this effect: plane-strain KIc = 36 MPa√m at 298 K, but at 77 K the mean ligament spacing decreased to ~1 mm, where Kc approached the plane-stress value of ~45 MPa√m, predicting a laminate toughness of ~45 MPa√m, close to the measured 51 MPa√m (rao1989cryogenictoughnessof pages 7-10).

### 2.2 Exceptions: Alloys and Tempers Whose Toughness Drops

**7075-T6/7475-T6:** These alloys undergo a fracture-mode transition from ductile void coalescence at room temperature to brittle transgranular shear at 77 K, which reduces fracture toughness (rao1989cryogenictoughnessof pages 4-6, morris1988mechanicalpropertiesof pages 11-13).

**Peak-aged Al-Li alloys (2091-T8X, 8090-T351, 8091-T351):** These conditions show L-T toughness decreases at 77 K. In 2091-T8X, KIc(L-T) dropped from 46 to 44 MPa√m, while S-L toughness dropped from 25 to 16 MPa√m. The mechanism involves a transition from ductile tearing to brittle transgranular shear with enhanced intergranular delamination bands at 77 K (rao1989cryogenictoughnessof pages 1-2, rao1989cryogenictoughnessof pages 4-6).

**Delamination in Al-Li plate.** While delamination can enhance L-T and T-L toughness via crack-divider mechanisms, it degrades short-transverse (S-L) toughness at all temperatures. If delamination becomes too extensive (ligaments < ~100 μm), the benefit is compromised. In overaged 2090, copious grain-boundary precipitation and δ′-precipitate-free zones increase delamination tendency, and the toughness elevation at 77 K is far smaller (<10%) than for the T8 condition (rao1989cryogenictoughnessof pages 7-10).

## 3. Welds: Friction Stir and Fusion Welds of 2219 and 2195 at Cryogenic Temperature

Friction stir welding (FSW) was developed at NASA Marshall Space Flight Center specifically for fabrication of the Space Shuttle External Tank and was subsequently adopted for the SLS core stage (kinchen1999mechanicalpropertiesof pages 1-3). For 0.320-inch Al2195-T8 plate-to-plate friction stir welds, the reported cryogenic enhancement factor was 1.6, meaning cryogenic (−423 °F, 20 K) ultimate tensile strength was 1.6 times the room-temperature value (kinchen1999mechanicalpropertiesof pages 1-3). FSW produced increased UTS and elongation at cryogenic temperature, and the −423 °F weld strength approached the parent-material strength. Yield strength and elongation were described as consistent and reproducible, in contrast to conventional fusion welds (kinchen1999mechanicalpropertiesof pages 1-3). Surface Crack Tension (SCT) testing confirmed that fracture toughness increased at cryogenic temperature, though centerline-flaw specimens produced lower toughness than crown-flaw specimens (kinchen1999mechanicalpropertiesof pages 6-8).

For the External Tank, the transition from 2219-T87 (original Standard Weight and Lightweight Tanks) to 2195 Al-Li (Super Lightweight Tank, first flight STS-91 in 1998) with FSW joining provided approximately 7,500 lb weight savings. The SLS core stage uses 2219 and 2195 with FSW (kinchen1999mechanicalpropertiesof pages 1-3). Falcon 9 reportedly uses FSW 2219 for its kerosene/LOX tanks, though detailed cryogenic property data for that application are proprietary.

## 4. Additively Manufactured Aluminum Alloys at Cryogenic Temperatures

Cryogenic mechanical data for AM aluminum alloys constitute an emerging and sparse literature. The following table summarizes available data:

| Alloy | Process | Condition | Temperature (K) | Yield Strength (MPa) | UTS (MPa) | Elongation (%) | Source |
|---|---|---|---:|---:|---:|---:|---|
| AlSi10Mg | LPBF/SLM | As-built, XY orientation | 20 | Not reported | 483 mean | Not reported | Adams (2023), DOI: 10.7273/000004509 (adams2023materialandscan pages 43-47) |
| AlSi10Mg | LPBF/SLM | As-built, Z orientation | 20 | Not reported | 512 mean | Not reported | Adams (2023), DOI: 10.7273/000004509 (adams2023materialandscan pages 43-47) |
| Al10SiMg (AlSi10Mg) | LPBF | As-built | 15 | Not reported | 395 | 25 uniform | Naeem et al. (2025), DOI: 10.1038/s43246-025-00793-4 (naeem2025enhancedstrengthand pages 1-2) |
| A205 (Al–Cu–Mg–Ag–TiB₂) | LPBF | As-built | 77 | 317 | 371 | 15.5 total | Tumulu (2025) (tumulu2025laserpowderbeda pages 158-162) |
| A205 (Al–Cu–Mg–Ag–TiB₂) | LPBF | Heat-treated | 77 | 367 | 486 | 14.8 total | Tumulu (2025) (tumulu2025laserpowderbeda pages 158-162) |
| AA2219 | LPBF | As-built | 77 | Increased versus room temperature; numerical value unavailable | Increased versus room temperature; numerical value unavailable | Similar to room-temperature value; numerical value unavailable | Tumulu (2025) (tumulu2025laserpowderbeda pages 108-112, tumulu2025laserpowderbedb pages 108-112) |
| AA2219 | LPBF | T5 | 77 | Increased versus room temperature; numerical value unavailable | Increased versus room temperature; numerical value unavailable | Increased versus room temperature; numerical value unavailable | Tumulu (2025) (tumulu2025laserpowderbeda pages 108-112, tumulu2025laserpowderbedb pages 108-112) |
| AA2219 | LPBF | T6 | 77 | Increased versus room temperature; numerical value unavailable | Increased versus room temperature; numerical value unavailable | Similar to room-temperature value; numerical value unavailable | Tumulu (2025) (tumulu2025laserpowderbeda pages 108-112, tumulu2025laserpowderbedb pages 108-112) |
| Scalmalloy (Al–Mg–Sc–Zr) | LPBF | As-built or heat-treated | ≤77 | No cryogenic-service tensile data identified | No cryogenic-service tensile data identified | No cryogenic-service tensile data identified | Room-temperature literature exists, but deep-cryogenic treatment is processing rather than service testing |
| Al–Fe–Zr | LPBF | Any | ≤77 | No data identified | No data identified | No data identified | Evidence gap |
| Al–Mn–Sc | LPBF | Any | ≤77 | No data identified | No data identified | No data identified | Evidence gap |
| Al–Cu–Ce | LPBF | Any | ≤77 | No data identified | No data identified | No data identified | Evidence gap |
| AA2319/AA2219 | WAAM | As-deposited or heat-treated | ≤77 | No cryogenic-service data identified | No cryogenic-service data identified | No cryogenic-service data identified | WAAM literature located addresses processing and room-temperature properties, not cryogenic service |


*Table: Reported low-temperature tensile properties for additively manufactured aluminum alloys, with orientation and heat-treatment effects retained. The table also identifies major alloy classes for which cryogenic-service data were not found.*

**LPBF AlSi10Mg:** Adams (2023, DOI: 10.7273/000004509) reported the first cryogenic (20 K) tensile data for SLM AlSi10Mg, with mean UTS of 483 MPa (XY orientation) and 512 MPa (Z orientation), compared with room-temperature UTS of approximately 250 MPa—a near-doubling (adams2023materialandscan pages 43-47). Naeem et al. (2025, DOI: 10.1038/s43246-025-00793-4) tested LPBF Al10SiMg at 15 K and reported UTS = 395 MPa with 25% uniform elongation, attributing the simultaneous strength–ductility enhancement to the eutectic Si network, which carries a disproportionate load share (higher yield strength than the Al matrix) while the matrix continues to strain-harden (naeem2025enhancedstrengthand pages 1-2). The Si phase effectively partitions stress and promotes distributed deformation. The effect of porosity on cryogenic ductility was not explicitly quantified, but porosity acts as stress concentrators that promote premature void nucleation and coalescence. Heat treatment (e.g., solution treatment that breaks up the Si network) may reduce the beneficial stress-partitioning effect.

**LPBF A205 (Al-Cu-Mg-Ag-TiB₂):** Tumulu (2025) tested LPBF A205 at −196 °C (77 K). In the as-built condition: YS = 317 MPa, UTS = 371 MPa, elongation = 15.5%. After heat treatment: YS = 367 MPa, UTS = 486 MPa, elongation = 14.8% (tumulu2025laserpowderbeda pages 158-162). Serrated flow was eliminated at 77 K. Fracture involved deformation mismatch at rigid TiB₂ particles, interface decohesion, and void formation (tumulu2025laserpowderbeda pages 158-162).

**LPBF AA2219:** Tumulu (2025) also tested LPBF AA2219 at −196 °C in as-built, T5, and T6 conditions. YS and UTS increased at cryogenic temperature for all conditions; GND density was 1.12–1.19 times higher than at room temperature, reaching 6.9 × 10¹⁵ m⁻² (AB), 5.7 × 10¹⁵ m⁻² (T5), and 7.3 × 10¹⁵ m⁻² (T6) (tumulu2025laserpowderbedb pages 108-112). Specific numerical tensile values were in Table 4.2 of the thesis but were not fully extracted from available text.

**Scalmalloy, Al-Fe-Zr, Al-Mn-Sc, Al-Cu-Ce, WAAM 2319/2219:** No cryogenic service (testing at 77 K or below) mechanical property data were identified in the literature search. All available Scalmalloy literature addresses room-temperature or elevated-temperature properties (naeem2025enhancedstrengthand pages 1-2). WAAM 2319 publications address processing optimization and room-temperature properties only.

## 5. Cryogenic Service Testing vs. Cryogenic Processing

It is essential to distinguish **cryogenic service testing** (measuring properties at 77 K, 20 K, or 4 K, as a component would experience in service with LOX or LH₂) from **cryogenic processing** (cryorolling, deep cryogenic treatment (DCT), or cryogenic forming, where the low temperature is used as a manufacturing step to improve room-temperature properties).

**Cryogenic processing literature:** Li et al. (2026, DOI: 10.1590/1980-5373-MR-2026-0243) applied DCT + artificial aging to LPBF Al-Mg-Sc-Zr alloy and increased hardness from 115.8 HV to 179.7 HV and room-temperature tensile strength from 400 MPa to 536 MPa. The mechanism involves cold-shrinkage-induced defect networks that serve as heterogeneous nucleation sites for secondary Al₃(Sc,Zr) nanoparticles during subsequent aging. Zhang et al. (2021, DOI: 10.3390/met11091406) studied cryogenic deformation of 2195 alloy (O-state and W-state) and found that elongation of W-state alloy increased from 15.4% at 298 K to 39.2% at 77 K (zhang2021cryogenicdeformationbehavior pages 2-4)—but this was deformation processing, not service-temperature characterization of the final T8 product. Other studies on cryorolling of 5083, 7075, and other alloys similarly address processing optimization of room-temperature properties and should not be conflated with service-temperature behavior.

## 6. Gaps in Cryogenic Property Data

The following major gaps are directly relevant to the BYU Vertical Cloud Lab's decision about whether to add cryogenic testing capability:

1. **Scalmalloy (Al-Mg-Sc-Zr) LPBF:** Room-temperature mechanical properties are well characterized (as-built YS ≈ 256–278 MPa, UTS ≈ 349–350 MPa; after aging YS ≈ 456–469 MPa, UTS ≈ 512–521 MPa), but no cryogenic service tensile or toughness data at 77 K or below were found.

2. **Al-Fe-Zr, Al-Mn-Sc, Al-Cu-Ce LPBF alloys:** No cryogenic mechanical property data of any kind were identified.

3. **AlSi7Mg/A357 LPBF:** Essentially no cryogenic service data were found, though Liu et al. (2026, DOI: 10.1016/j.jmrt.2026.06.140, unobtainable) may address cryogenic tensile anisotropy in LPBF AlSi7Mg.

4. **WAAM 2319/2219:** Despite the alloy's heritage as a cryogenic tank material in wrought form, no cryogenic service tensile data for wire-arc additively manufactured 2319 or 2219 were identified.

5. **Fracture toughness of any AM aluminum alloy at cryogenic temperature:** No KIc, KQ, or J-integral data at 77 K or below for any LPBF or WAAM aluminum alloy were found. All available cryo data are tensile and Charpy impact only.

6. **Sc-lean, Li-lean, and RE-lean compositions:** For AM alloys designed to avoid critical minerals (Sc, Li, Ce), there is essentially no cryogenic data. This represents a significant opportunity for the Vertical Cloud Lab, which designs such alloys with AI and CALPHAD.

7. **Alloys 2060, 2098, 2198 (3rd-generation Al-Li):** While these alloys are increasingly used in aerospace, their cryogenic mechanical property data in the open literature are sparse. The 2050 evaluation at 77 K (Hafley et al. 2011, NASA/TP-2011-217163) represents one of the few systematic cryogenic evaluations of a 3rd-generation Al-Li alloy.

8. **4 K data:** Very few aluminum alloy datasets extend to 4 K (liquid He). Most cryogenic data are at 77 K (LN₂) and 20 K (LH₂). The 4 K regime is relevant for superconducting magnet structures and some advanced propulsion concepts.

## 7. Summary and Recommendations for the BYU Vertical Cloud Lab

The cryogenic mechanical behavior of wrought aluminum alloys is broadly favorable: most FCC Al alloys become simultaneously stronger and more ductile at cryogenic temperatures due to enhanced dislocation storage, suppressed cross-slip and dynamic recovery, delayed Considère instability, and (in Al-Li alloys) delamination toughening (morris1988mechanicalpropertiesof pages 11-13, rao1989cryogenictoughnessof pages 4-6, zhang2021cryogenicdeformationbehavior pages 8-11, wang2023influenceofcryogenic pages 9-12). Exceptions exist for specific alloy-temper combinations (7075-T6, peak-aged Al-Li alloys) where fracture-mode transitions override the beneficial work-hardening effects (rao1989cryogenictoughnessof pages 4-6, morris1988mechanicalpropertiesof pages 11-13).

For AM alloys, the nascent cryogenic literature (3–5 papers as of 2025) shows promising results for LPBF AlSi10Mg and A205, with the Si network and TiB₂ particles potentially providing beneficial stress partitioning at cryogenic temperatures (naeem2025enhancedstrengthand pages 1-2, tumulu2025laserpowderbeda pages 158-162). However, the data landscape has enormous gaps: no fracture toughness at cryogenic temperature for any AM Al alloy, no data for Scalmalloy or critical-mineral-lean compositions, and no WAAM Al alloy cryo service data. The Vertical Cloud Lab's capabilities in alloy design, powder production, and specimen fabrication, combined with a cryogenic tensile testing capability (even at 77 K using LN₂, which is straightforward), would position it to address a significant and industrially relevant gap, particularly for novel Sc-lean, Li-lean, and RE-lean compositions designed for LPBF.

### Confidence Assessment
- **Strongly supported:** General cryogenic trends for wrought 2xxx, 5xxx alloys; mechanisms of cryogenic strengthening; Rao & Ritchie quantitative Al-Li data; 2195-T8 and 2050-T84 cryo tensile data.
- **Moderately supported:** FSW cryo enhancement factors; LPBF AlSi10Mg and A205 cryo data (few studies, limited replication).
- **Weakly supported or gaps:** Specific 2219-T87 numerical cryo values (in figures, not extracted); 7050 cryo data; all Scalmalloy/Al-Fe-Zr/Al-Cu-Ce/WAAM cryo data (not found); fracture toughness for any AM Al alloy at cryo.

References

1. (morris1988mechanicalpropertiesof pages 8-11): JW Morris and J Glazer. Mechanical properties of high-strength aluminum alloys at cryogenic temperatures. Unknown journal, 1988.

2. (morris1988mechanicalpropertiesof pages 6-8): JW Morris and J Glazer. Mechanical properties of high-strength aluminum alloys at cryogenic temperatures. Unknown journal, 1988.

3. (rao1989cryogenictoughnessof pages 4-6): K. T. Venkateswara Rao, Weikang Yu, and R. O. Ritchie. Cryogenic toughness of commercial aluminum-lithium alloys: role of delamination toughening. Metallurgical Transactions A, 20:485-497, Mar 1989. URL: https://doi.org/10.1007/bf02653929, doi:10.1007/bf02653929. This article has 235 citations.

4. (schwartzberg1964cryogenicmaterialsdata pages 43-51): CRYOGENIC MATERIALS DATA HANDBOOK This article has 76 citations.

5. (wang2023influenceofcryogenic pages 4-6): Tao Wang, Kai Wen, Ben Lin, Xiwu Li, Yanan Li, Zhihui Li, Yongan Zhang, and Baiqing Xiong. Influence of cryogenic temperatures on the mechanical properties and microstructure of 2195-t8 alloy. Metals, 13:740, Apr 2023. URL: https://doi.org/10.3390/met13040740, doi:10.3390/met13040740. This article has 6 citations.

6. (wang2023influenceofcryogenic pages 2-4): Tao Wang, Kai Wen, Ben Lin, Xiwu Li, Yanan Li, Zhihui Li, Yongan Zhang, and Baiqing Xiong. Influence of cryogenic temperatures on the mechanical properties and microstructure of 2195-t8 alloy. Metals, 13:740, Apr 2023. URL: https://doi.org/10.3390/met13040740, doi:10.3390/met13040740. This article has 6 citations.

7. (hafley2011evaluationofaluminuma pages 24-28): RA Hafley, MS Domack, SJ Hales, and RN Shenoy. Evaluation of aluminum alloy 2050-t84 microstructure and mechanical properties at ambient and cryogenic temperatures. Unknown journal, 2011.

8. (hafley2011evaluationofaluminumb pages 24-28): RA Hafley, MS Domack, SJ Hales, and RN Shenoy. Evaluation of aluminum alloy 2050-t84 microstructure and mechanical properties at ambient and cryogenic temperatures. Unknown journal, 2011.

9. (chen1998theeffectsof pages 2-4): P. S. Chen, A. K. Kuruvilla, T. W. Malone, and W. P. Stanton. The effects of artificial aging on the microstructure and fracture toughness of al-cu-li alloy 2195. Journal of Materials Engineering and Performance, 7:682-690, Oct 1998. URL: https://doi.org/10.1361/105994998770347576, doi:10.1361/105994998770347576. This article has 83 citations and is from a peer-reviewed journal.

10. (chen1998theeffectsof pages 4-6): P. S. Chen, A. K. Kuruvilla, T. W. Malone, and W. P. Stanton. The effects of artificial aging on the microstructure and fracture toughness of al-cu-li alloy 2195. Journal of Materials Engineering and Performance, 7:682-690, Oct 1998. URL: https://doi.org/10.1361/105994998770347576, doi:10.1361/105994998770347576. This article has 83 citations and is from a peer-reviewed journal.

11. (hafley2011evaluationofaluminuma pages 28-34): RA Hafley, MS Domack, SJ Hales, and RN Shenoy. Evaluation of aluminum alloy 2050-t84 microstructure and mechanical properties at ambient and cryogenic temperatures. Unknown journal, 2011.

12. (hafley2011evaluationofaluminum pages 28-34): RA Hafley, MS Domack, SJ Hales, and RN Shenoy. Evaluation of aluminum alloy 2050-t84 microstructure and mechanical properties at ambient and cryogenic temperatures. Unknown journal, 2011.

13. (hafley2011evaluationofaluminum pages 24-28): RA Hafley, MS Domack, SJ Hales, and RN Shenoy. Evaluation of aluminum alloy 2050-t84 microstructure and mechanical properties at ambient and cryogenic temperatures. Unknown journal, 2011.

14. (morris1988mechanicalpropertiesofb pages 1-6): JW Morris and J Glazer. Mechanical properties of high-strength aluminum alloys at cryogenic. Unknown journal, 1988.

15. (morris1988mechanicalpropertiesofa pages 1-6): JW Morris and J Glazer. Mechanical properties of high-strength aluminum alloys at cryogenic temperatures. Unknown journal, 1988.

16. (rao1989cryogenictoughnessof pages 1-2): K. T. Venkateswara Rao, Weikang Yu, and R. O. Ritchie. Cryogenic toughness of commercial aluminum-lithium alloys: role of delamination toughening. Metallurgical Transactions A, 20:485-497, Mar 1989. URL: https://doi.org/10.1007/bf02653929, doi:10.1007/bf02653929. This article has 235 citations.

17. (adams2023materialandscan pages 37-43): Reece Michael Adams. Material and scan spacing variation for improved mechanical performance of additively manufactured materials at cryogenic temperatures. Text, Jan 2023. URL: https://doi.org/10.7273/000004509, doi:10.7273/000004509. This article has 2 citations and is from a peer-reviewed journal.

18. (schwartzberg1964cryogenicmaterialsdata pages 22-26): CRYOGENIC MATERIALS DATA HANDBOOK This article has 76 citations.

19. (schwartzberg1964cryogenicmaterialsdata pages 29-33): CRYOGENIC MATERIALS DATA HANDBOOK This article has 76 citations.

20. (schwartzberg1964cryogenicmaterialsdata pages 51-55): CRYOGENIC MATERIALS DATA HANDBOOK This article has 76 citations.

21. (ekin2011appendixdatatables pages 155-158): JW Ekin. Appendix data tables from experimental techniques for low-temperature measurements: cryostat design, material properties, and superconductor critical …. Unknown journal, 2011.

22. (morris1988mechanicalpropertiesof pages 11-13): JW Morris and J Glazer. Mechanical properties of high-strength aluminum alloys at cryogenic temperatures. Unknown journal, 1988.

23. (wang2023influenceofcryogenic pages 9-12): Tao Wang, Kai Wen, Ben Lin, Xiwu Li, Yanan Li, Zhihui Li, Yongan Zhang, and Baiqing Xiong. Influence of cryogenic temperatures on the mechanical properties and microstructure of 2195-t8 alloy. Metals, 13:740, Apr 2023. URL: https://doi.org/10.3390/met13040740, doi:10.3390/met13040740. This article has 6 citations.

24. (zhang2021cryogenicdeformationbehavior pages 8-11): Jin Zhang, Wenfu Tan, Cheng Wang, Chunnan Zhu, and Youping Yi. Cryogenic deformation behavior and microstructural characteristics of 2195 alloy. Metals, 11:1406, Sep 2021. URL: https://doi.org/10.3390/met11091406, doi:10.3390/met11091406. This article has 23 citations.

25. (morris1988mechanicalpropertiesofb pages 8-11): JW Morris and J Glazer. Mechanical properties of high-strength aluminum alloys at cryogenic. Unknown journal, 1988.

26. (naeem2025enhancedstrengthand pages 1-2): Muhammad Naeem, Asif Ur Rehman, Liliana Romero Resendiz, Elmas Salamci, Huseyin Aydin, Peyman Ansari, Stefanus Harjo, Wu Gong, Yusuf Usta, Olcay Ersel Canyurt, Xun-Li Wang, and Metin U. Salamci. Enhanced strength and ductility in an additively manufactured al10simg alloy at cryogenic temperatures. Communications Materials, Apr 2025. URL: https://doi.org/10.1038/s43246-025-00793-4, doi:10.1038/s43246-025-00793-4. This article has 5 citations and is from a peer-reviewed journal.

27. (tumulu2025laserpowderbeda pages 158-162): SK Tumulu. Laser powder bed fusion additive manufacturing (lpbf-am) of aluminum-copper alloys. Unknown journal, 2025.

28. (rao1989cryogenictoughnessof pages 7-10): K. T. Venkateswara Rao, Weikang Yu, and R. O. Ritchie. Cryogenic toughness of commercial aluminum-lithium alloys: role of delamination toughening. Metallurgical Transactions A, 20:485-497, Mar 1989. URL: https://doi.org/10.1007/bf02653929, doi:10.1007/bf02653929. This article has 235 citations.

29. (kinchen1999mechanicalpropertiesof pages 1-3): DG Kinchen, Z Li, and GP Adams. Mechanical properties of friction stir welds in a12195-t8. Unknown journal, 1999.

30. (kinchen1999mechanicalpropertiesof pages 6-8): DG Kinchen, Z Li, and GP Adams. Mechanical properties of friction stir welds in a12195-t8. Unknown journal, 1999.

31. (adams2023materialandscan pages 43-47): Reece Michael Adams. Material and scan spacing variation for improved mechanical performance of additively manufactured materials at cryogenic temperatures. Text, Jan 2023. URL: https://doi.org/10.7273/000004509, doi:10.7273/000004509. This article has 2 citations and is from a peer-reviewed journal.

32. (tumulu2025laserpowderbeda pages 108-112): SK Tumulu. Laser powder bed fusion additive manufacturing (lpbf-am) of aluminum-copper alloys. Unknown journal, 2025.

33. (tumulu2025laserpowderbedb pages 108-112): SK Tumulu. Laser powder bed fusion additive manufacturing (lpbf-am) of aluminum-copper alloys. Unknown journal, 2025.

34. (zhang2021cryogenicdeformationbehavior pages 2-4): Jin Zhang, Wenfu Tan, Cheng Wang, Chunnan Zhu, and Youping Yi. Cryogenic deformation behavior and microstructural characteristics of 2195 alloy. Metals, 11:1406, Sep 2021. URL: https://doi.org/10.3390/met11091406, doi:10.3390/met11091406. This article has 23 citations.
