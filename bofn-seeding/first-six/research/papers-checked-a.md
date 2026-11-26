# Primary-paper check: candidate LPBF Al alloys (papers_a)

Compiled 2026-11-26. All values are copied from the source named for each paper. "Not accessed" means I did not see that part of the paper. VED values marked "(my calc.)" are P/(v·h·t), computed by me and not quoted from the paper. Kelvin is converted to °C (K − 273) only where marked.

Access summary:
- FULL TEXT: papers 2, 3 and 4 (Chalmers repository PDFs), the Mehta PhD thesis (Chalmers), paper 1 (Springer HTML page via the tunnelled browser; text only, tables 1–2 rendered as "Full size table" links, so I did not see those two tables), paper 5 (Innsbruck repository PDF, version of record).
- ABSTRACT ONLY: papers 6, 7, 8, 10, 11 and 12 (ScienceDirect not used; HAL and digital.csic.es copies sit behind an anti-bot check, which I did not try to pass).
- Paper 9: blocked. tandfonline.com and research.rug.nl both showed a Cloudflare "Just a moment..." check, both via curl and in the tunnelled browser. I added nothing to what you already had.
- Warning: the Zenodo record 7902936 that OpenAlex lists as an OA copy of Mair et al. actually contains a DIFFERENT paper: Guo et al., Al-Mg-Mn-Er-Zr, Mater. Des. 222 (2022) 111064. Do not cite it as Mair.

---

## 1. Mehta et al. (Chalmers), "Al–Mn–Cr–Zr-based alloys tailored for powder bed fusion-laser beam process: alloy design, printability, resulting microstructure and alloy properties", J. Mater. Res. 37 (2022). DOI 10.1557/s43578-022-00533-1
- Read: link.springer.com article page (open access) via the tunnelled browser. FULL TEXT of the body. Table 1 (compositions) and Table 2 (DOE ranges) did NOT render (they were links). Compositions are taken from paper 2 and the thesis, which give ICP for the same alloys A–C.
- Alloys: two ternaries and one quaternary. A = Al-Mn-Zr, B = Al-Mn-Cr (Zr-free), C = Al-Mn-Cr-Zr. ICP values are under paper 2.
- Powder: "nitrogen gas atomisation", "nominal particle size range of 20–53 µm", from Höganäs AB. PSD is in Table S1 (not accessed).
- LPBF: "EOS M100 machine with a 40 µm spot size, 200 W (170W nominal) power Yb-fibre laser". Power fixed at 170 W, layer 0.03 mm, scan rotation 67°. Two-level full-factorial DOE on hatch and speed (alloys A and B), plus laser power as a third variable for alloy C. DOE ranges are in Table 2 (not accessed). Powder dried at 353 K (80 °C) for 4 h before every print. The thesis says the M100 has no plate pre-heating ("Not possible").
- Density and cracking: "Good relative density (~ 99.5%)". Alloy C at optimum ~99.6 % average. "no cracks were observed in any of the samples printed". That includes the Zr-FREE alloy B, so a Zr-free Al-Mn-Cr variant was printed crack-free.
- Hardness as-printed: "Alloys A, B and C show average hardness values of 91, 99 and 102 HV". Ageing at 678 K (405 °C): A and C harden for 2–6 h, then over-age. Maximum increase 18 HV (A) and 28 HV (C). Zr-free B rises for about 1 h, then over-ages quickly. At 523 K for 24 h, negligible change.
- Microstructure: columnar grains along the build direction, with no L12 Al3Zr grain refinement seen. Mn-rich nano-precipitates sit at melt-pool boundaries (<100 nm spherical, plus 200–400 nm with Al6Mn stoichiometry) and at grain/cell boundaries (8.42 and 8.58 wt% Mn by EDX). XRD shows minor Al12Mn/Al6Mn, "< 5 vol%".
- Tensile: none in this paper.
- Useful for our seed recipe: (1) Al-~5Mn-0.8Cr with or without 0.5–0.6 Zr prints crack-free at 170 W on a 40 µm spot, and Zr is not needed for crack resistance. (2) Most of the as-built strength comes from solid solution, and Zr plus Cr give the ageing response.

## 2. Mehta et al., "Effect of precipitation kinetics on microstructure and properties of novel Al-Mn-Cr-Zr based alloys developed for powder bed fusion – laser beam process", J. Alloys Compd. 920 (2022) 165870. DOI 10.1016/j.jallcom.2022.165870
- Read: research.chalmers.se/publication/531215 (accepted/published PDF). FULL TEXT.
- Composition (Table 1, ICP-AES, wt%), as-atomised / as-printed:
  - Alloy A: Al-4.7Mn-0.48Zr-0.15Fe-0.16Si / Al-4.8Mn-0.47Zr-0.16Fe-0.16Si
  - Alloy B: Al-5.0Mn-0.8Cr-0.14Fe-0.16Si / Al-4.9Mn-0.8Cr-0.18Fe-0.17Si
  - Alloy C: Al-5.0Mn-0.8Cr-0.59Zr-0.16Fe-0.16Si / Al-5.0Mn-0.8Cr-0.60Zr-0.16Fe-0.17Si
- Powder: gas atomised, Höganäs AB, 20–53 µm.
- LPBF: "EOS M100 machine with 40 µm spot size and 200 W (170 W nominal power)". Printed at "170 W power, 0.1 mm hatch distance, 1500 mm/s scan speed and 0.03 mm layer thickness with scan rotation of 67°". Powder dried at 353 K for 4 h. VED = 37.8 J/mm³ (my calc.). Specimens were 8×8×16 mm cuboids. Plate T is not stated (the M100 cannot pre-heat, per the thesis).
- Heat treatments: water quench after 523–678 K. Alloy C as-printed 102 HV. Peaks: "143 HV at 623 K for 24 h and 142 HV at 648 K for 14 h" (350 °C/24 h and 375 °C/14 h). At 648 K: 136 HV after 8–10 h, then a secondary peak of 142 HV at 14 h. 678 K never exceeds 130 HV. 648 K for 100 h gives 122 HV. Only temperatures >573 K harden alloy C. After 648 K, A and B gained 23 % and 15 % and C gained 34 %. At 678 K over-ageing starts after 6 h (A, C) and 2 h (B). HV0.3, averaged over XZ and XY.
- Microstructure: precipitation at melt-pool boundaries. A refined-grain region (<5 µm) and a columnar region (>50–100 µm) (Fig. 8). Mn-rich precipitates grow first at grain boundaries, then in the bulk. They shift from Al12Mn-like to Al6Mn-like composition. Zr-rich precipitates decorate the Mn-rich ones.
- Tensile: none.
- Useful for our seed recipe: alloy C, Al-5.0Mn-0.8Cr-0.6Zr (ICP), at 170 W / 1500 mm/s / 0.1 mm / 30 µm. Direct age at 623 K/24 h or 648 K/14 h (+~40 HV). Powder composition carries over to the part almost unchanged, with no Mn loss.

## 3. Mehta et al., "Advancing novel Al-Mn-Cr-Zr based family of alloys tailored for powder bed fusion-laser beam process", J. Alloys Compd. 967 (2023) 171685. DOI 10.1016/j.jallcom.2023.171685
- Read: research.chalmers.se/publication/537053. FULL TEXT.
- Composition (Table 1, ICP-OES, as-printed, wt%):
  - C (Zr-low, Mg-free): Al-5.0Mn-0.8Cr-0.6Zr-0.0Mg-0.17Fe-0.24Si
  - D (Zr-high, Mg-free): Al-4.7Mn-0.8Cr-1.2Zr-0.0Mg-0.13Fe-0.21Si
  - E (Zr-low, Mg): Al-4.7Mn-0.8Cr-0.7Zr-1.0Mg-0.16Fe-0.21Si
  - F (Zr-high, Mg): Al-4.8Mn-0.9Cr-1.1Zr-1.2Mg-0.19Fe-0.20Si
- Mg loss: "slight evaporation of Mg (0.1 wt % and 0.2 wt % respectively)" for E and F, powder to part. The thesis (p. 44) gives the reverse assignment: 1 wt% Mg in E lost 0.2 and 1.2 wt% Mg in F lost 0.1. The paper and the thesis disagree on which alloy lost which. Oxygen fell after printing in all alloys. Alloy C powder held ~1340 ppm O.
- Powder: gas atomised, Höganäs, 20–53 µm. O measured by LECO.
- LPBF: "EOS M290 machine with 100 µm spot size and 400 W (370 W nominal power)". DOE on C and D: power 200–370 W, speed 375–2000 mm/s. Optimum "370 W power, 0.13 mm hatch distance, 1300 mm/s laser speed and 0.03 mm layer thickness with a scan rotation of 67°". Density ">99.7 %" for all four alloys, and 99.7–99.8 % for C and D. VED = 73.0 J/mm³ (my calc.). Contour scanning was deactivated, which left sub-surface porosity in C and D. O2 set point <0.1 % (<1000 ppm). Plate T: not stated. The thesis says the M290 can pre-heat up to 200 °C but gives no value used. The thesis notes that M290 powder was NOT dried.
- Cracking: "Alloy E (Zr-low, Mg-containing) showed solidification cracking". Cracks start around melt-pool boundaries. "alloy F did not show any solidification cracking". Alloys D and F are grain-refined by primary L12 Al3Zr: average ECD "~26 µm in alloy C → ~1 µm in alloy F". The structure is bimodal, with refined grains at melt-pool boundaries. Zr solubility via PBF-LB is "around 0.5–0.7 wt %".
- Hardness: as-printed, F is 29.7 HV above C and E is 11.8 HV above C. Abstract: "previously known as-printed hardness of 102 HV to 132 HV in one of the variants". Direct ageing at 623 K (0–32 h) and 648 K (0–24 h), air cooled. Peak times at 648 K: C 14 h, D 4 h, E 8 h, F 8 h. Gains: C +40 HV, D +35 HV, E and F +40 HV. F peaks at "172 HV at 623 K 24 h and 648 K 8 h".
- Useful for our seed recipe: (1) 1 wt% Mg with 0.6–0.7 Zr CRACKS, while Mg with ≥1.1 Zr does not, because Zr above ~0.6 wt% refines the grains. (2) M290 window: 370 W / 1300 mm/s / 0.13 mm / 30 µm. (3) Mg-free variants need no grain refiner to stay crack-free.

## 4a. Mehta et al., "Mechanical properties and microstructural characterisation including high-temperature performance of Al-Mn-Cr-Zr based alloys tailored for PBF-LB", Mater. Des. 244 (2024) 113160. DOI 10.1016/j.matdes.2024.113160
- Read: research.chalmers.se/publication/542131. FULL TEXT. The individual tensile values are only in Fig. 2/Fig. 5, and the rounded table values come from the thesis (4b).
- Alloys (Table 1, wt%/at%): C Al-5.0Mn-0.8Cr-0.6Zr. D Al-4.7Mn-0.8Cr-1.2Zr. F Al-4.8Mn-0.9Cr-1.1Zr-1.2Mg (Fe 0.13–0.19, Si 0.20–0.24).
- Powder: nitrogen gas atomised, Höganäs, 20–53 µm.
- LPBF: EOS M290, 100 µm spot, "370 W power, 1300 mm/s laser scanning speed, 0.13 mm hatch distance and 0.03 mm layer thickness". Density ">99.8 %", Ar with O2 ≤0.1 %, 67° rotation. Plate T: not stated.
- Heat treatments: heated at 10 K/min, air cooled. HT1 = 623 K/24 h for all alloys. HT2 = 648 K/14 h (C), 648 K/4 h (D), 648 K/8 h (F).
- Tensile: printed as cylinders (thesis: 100 mm long, Ø14 mm), heat treated, then MACHINED. Seven samples per condition, Z and XY. Zwick Z100 with 25 mm extensometer. Text: as-printed ">15 %" elongation with YS "between 250–400 MPa". C is isotropic, while D and F differ by ~30 MPa between directions. After HT, C and D have "YS at about 350 MPa". F reaches "high YS reaching 500 MPa for all the conditions" with "lower ductility (3–7%)". F as-printed shows PLC serrations. High temperature (peak aged): C UTS falls from ~400 MPa at RT to ~180 MPa at 573 K. F UTS falls from 550 MPa at RT to ~125 MPa at 573 K. Abstract: "Yield strength up to 170 MPa at 573 K".
- Fracture: in Z tests, fracture follows melt-pool tracks rich in melt-pool-boundary precipitates. The precipitate-free or coarse zone is 10–15 µm at melt-pool boundaries vs 1–2 µm elsewhere.

## 4b. Mehta, B., PhD thesis "Development of high performance aluminium alloys tailored for powder bed fusion-laser beam", Chalmers University of Technology, 2023 (ISBN 978-91-7905-909-5). research.chalmers.se/publication/537076
- Read: FULL TEXT PDF.
- Table 3 (ICP-OES, as-printed, wt%): A Al-4.7Mn-0.48Zr. B Al-4.8Mn-0.8Cr. C Al-5Mn-0.8Cr-0.6Zr. D Al-4.7Mn-0.8Cr-1.2Zr-0Mg. E Al-4.7Mn-0.8Cr-0.7Zr-1Mg. F Al-4.8Mn-0.9Cr-1.1Zr-1.2Mg (Fe 0.13–0.19, Si 0.16–0.21). Powder is nitrogen gas atomised, 20–53 µm.
- Table 7: the EOS M100 has a 40 µm spot, 170 W nominal, and plate pre-heating "Not possible". The EOS M290 has an 85 µm laser diameter (papers 3 and 4 say 100 µm), 370 W nominal, and pre-heating "Up to 200 °C". Ar shielding keeps O2 <0.1 %. Density was 99.5–99.6 % on the M100 (up to 0.4 % residual porosity) and 99.7–99.8 % on the M290 (<0.2 %).
- Table 8 (RT tensile, averaged over XZ and XY, "rounded off"):

  | Alloy | Condition | YS (MPa) | UTS (MPa) | El (%) |
  |---|---|---|---|---|
  | C | as-printed | 250 | 310 | 25 |
  | C | 648 K 24 h | 350 | 440 | 8 |
  | D | as-printed | 300 | 330 | 25 |
  | D | 648 K 4 h | 360 | 430 | 3 |
  | F | as-printed | 390 | 450 | 17 |
  | F | 648 K 8 h | 500 | 560 | 5 |

  Note: Table 8 lists C's treatment as "648 K 24 h", while Mater. Des. Table 2 lists HT2 for C as 648 K/14 h. This is an inconsistency in the source.
- High-temperature tests: alloy F has YS 490 MPa at RT and ~100 MPa at 573 K. Alloy C has 340 MPa at RT and >150 MPa at 573 K.
- Thermal stability: alloy C, peak-aged at 623 K/24 h, shows no hardness loss after 523 K for 2544 h, and loses 17 HV (~12 %) after 623 K for 1054 h.
- Useful for our seed recipe: Mg-free Al-5Mn-0.8Cr-(0.6 to 1.2)Zr gives 250–300 MPa YS with 25 % elongation as-built and ~350 MPa YS when aged. The Mg + high-Zr variant F gives 500 MPa YS / 5 % aged. All tensile bars were machined from Ø14 mm cylinders.

## 5. Mair et al. (Innsbruck), "Microstructural features and mechanical properties of a novel Ti- and Zr-modified Al-Mn alloy processed by laser powder bed fusion", J. Alloys Compd. 897 (2022) 163156. DOI 10.1016/j.jallcom.2021.163156
- Read: diglib.uibk.ac.at (ULB Tirol), version of record PDF, open. FULL TEXT. 
- Composition (wt%): Table 1 powder ICP-AES: Al bal., 4.80 Mn, 0.82 Ti, 0.71 Zr, 0.14 Fe, 0.06 Si, 0.02 Cu. Table 2 as-built: 4.50 Mn, 0.77 Ti, 0.69 Zr, 0.13 Fe, 0.06 Si, 0.01 Cu. The paper calls this "no significant change". The paper gives no separate nominal composition beyond "Al-Mn-Ti-Zr".
- Powder: "atomized with inert gas (N2) by Ecka Granules GmbH". Sieved at 63 µm. D10/D50/D90 = 26.4/41.3/61.8 µm. Bulk 1.31 and tap 1.64 g/cm³, Hausner 1.25 ("Fair").
- LPBF: AconityLAB, 1064 nm Yb:YAG fibre laser (spot size not stated). Pure Al platforms, Ar with O2 <30 ppm. Stripes 10 mm, zigzag, 67° rotation. Optimum: "no preheating of the substrate plate, layer thickness tL = 30 µm; hatch distance d = 100 µm; laser power PL = 380 W; and scanning speed vs = 1900 mm/s". VED = 66.7 J/mm³ (my calc.). The tested window is not given in the text I read (only the optimum). Conduction-mode melting.
- Density and cracks: 99.9 ± 0.1 %, with no pores or solidification cracks.
- Tensile (Table 5, as-built only): specimens printed horizontally, near-contour, then milled to ISO 6892 E 3. HV10 108 ± 1, YS 284 ± 3 MPa, UTS 320 ± 1 MPa, A 16.9 ± 0.2 %. UTS is reached at 9 % strain. No heat-treated data.
- Microstructure: bimodal. Equiaxed grains along melt-pool borders (11.2 % of area, 0.84 ± 0.28 µm) and columnar grains (69.3 %, 2.75 ± 1.82 µm, <001> fibre, max intensity ~4.2). Primary L12 Al3(TixZr1−x) cubes sit in the equiaxed grains near the melt-pool bottom. A quasi-crystalline AlxMn(Fe,Si) phase forms on grain boundaries. Mn in solid solution is "1.9 ± 0.3 at% (≙ 3.7 ± 0.5 wt%)", worth "~104 MPa ≙ 37% share of yield strength".
- Why it prints: Mn boiling point is 2061 °C vs 1091 °C for Mg, and grain refinement comes from Al3(Ti,Zr).
- Useful for our seed recipe: Al-4.8Mn-0.8Ti-0.7Zr (powder ICP) at 380 W / 1900 mm/s / 100 µm / 30 µm with no preheat gives 99.9 % density and YS 284 MPa / 16.9 % as-built. Mn fell 4.80 → 4.50 wt% from powder to part.

## 6. Pauzon et al., "A novel laser powder bed fusion Al-Fe-Zr alloy for superior strength-conductivity trade-off", Scripta Mater. 219 (2022) 114878. DOI 10.1016/j.scriptamat.2022.114878; and Pauzon et al., "Direct ageing of LPBF Al-1Fe-1Zr for high conductivity and mechanical performance", Acta Mater. 258 (2023) 119199. DOI 10.1016/j.actamat.2023.119199
- Read: ABSTRACT ONLY. The HAL copies (hal-03863812, hal-04327074) returned an anti-bot page, and ScienceDirect was not used.
- Scripta abstract (HAL API): Al-Fe-Zr alloy with "superior yield strength (310 MPa) and thermal conductivity (180 W/m·K) after direct ageing (400°C/4h)". Ageing precipitates "plate-like Al13Fe4 and coherent Al3Zr-L12 nanoprecipitates".
- Acta abstract: seen only as a search-engine snippet (AMiner), not verified: "high conductivity (27 MS/m) and yield strength (330MPa) after a simple direct ageing step at 400°C/4h".
- Composition, powder, parameters, as-built tensile: not accessed.

## 7. Qi et al.: (a) "Laser powder bed fusion of a near-eutectic Al–Fe binary alloy: Processing and microstructure", Addit. Manuf. 35 (2020) 101308, DOI 10.1016/j.addma.2020.101308; (b) "Managing both high strength and thermal conductivity of a laser powder bed fused Al–2.5Fe binary alloy: Effect of annealing on microstructure", Mater. Sci. Eng. A 805 (2021) 140591, DOI 10.1016/j.msea.2020.140591
- Read: ABSTRACT ONLY (closed access, via Semantic Scholar).
- (a) Al–2.5 mass% Fe. Optimum "P = 204 W, v ≤ 800 mms-1" gives relative density >99%. Pv^-1/2 is used as the density criterion. Columnar grains have a mean width of ∼21 µm. Nano metastable Al6Fe. The hardness sentence in the retrieved abstract is garbled ("mean size ∼ 90 HV"), so I cannot quote the hardness value. Hatch, layer, machine and plate T: not accessed.
- (b) As-fabricated: "tensile strength of ∼320 MPa", thermal conductivity ∼150 W m-1 K-1. Annealing at 300 °C raises conductivity to ∼185 W m-1 K-1 "without a loss of tensile strength". Annealing at 500 °C "significantly decreased" strength. YS and elongation: not accessed.

## 8. Wang et al., "Design of Al–Fe–Mn alloy for both high-temperature strength and sufficient processability of laser powder bed fusion", Addit. Manuf. 68 (2023) 103524. DOI 10.1016/j.addma.2023.103524 (CC-BY hybrid OA)
- Read: ABSTRACT ONLY (OpenAlex). The only OA location is ScienceDirect, which I did not use. No Al-2.5Fe-2Cu paper was located in the time available.
- Al–2.5Fe–2Mn (mass%), near-eutectic L → α-Al + Al6M. Relative density "above 99%". Strength "remained above 240 MPa at an elevated temperature of 300 °C". Room-temperature UTS, parameters and plate T: NOT accessed. The earlier claim of "UTS about 369 MPa" could NOT be verified.

## 9. Li et al., "Precipitation evolution, aging strengthening and thermal stability in Al–Fe-Mg-Zr eutectic alloy via laser powder bed fusion", Virtual Phys. Prototyp. (2025). DOI 10.1080/17452759.2025.2516663
- Read: BLOCKED. tandfonline.com and research.rug.nl both showed a Cloudflare "Just a moment..." page, in curl and in the tunnelled browser (two tries). Table 1, plate temperature, spot size, scan strategy and Table 2 were not accessed. Nothing is added to your confirmed values. A search snippet of the RUG page mentions "YS of 124 MPa at 350 °C" (unverified).

## 10. (a) Xu et al., "Achieving high strength in laser powder-bed fusion processed AlFeCuZr alloy via dual-nanoprecipitations and grain boundary segregation", J. Mater. Sci. Technol. 137 (2023) 56–66, DOI 10.1016/j.jmst.2022.07.033. (b) Pérez-Prado et al., "An Al-5Fe-6Cr alloy with outstanding high temperature mechanical behavior by laser powder bed fusion", Addit. Manuf. 55 (2022) 102828, DOI 10.1016/j.addma.2022.102828
- (a) Not confirmed as paper 9's ref. 27, because paper 9 was blocked. ABSTRACT seen only via a search-engine snippet (AMiner), unverified: crack-free, near-dense "Al-1Fe-0.6Cu-1.3Zr", YS "500 MPa at room temperature and 163 MPa at 573 K". Coarse-grain zones average 0.95 µm and fine-grain zones 0.45 µm. (Al,Cu)Fe3 and Al3Zr nanoparticles. Ductility and parameters: not accessed. The snippet gives 500 MPa, not 497.
- (b) ABSTRACT ONLY (OpenAlex). The CSIC repository PDF sits behind an anti-bot page. Al-5Fe-6Cr (wt%), powder "produced by casting and gas atomization". Relative density 99.8 %, 192 HV at RT. YS "273 ± 5 MPa and 179 ± 3 MPa at 300ºC and 400ºC". Strength comes from nanoscale icosahedral i-phase and intermetallics. RT tensile and parameters: not accessed.

## 11. Zhou et al. (University of Central Florida), "Microstructure and mechanical properties of Zr-modified aluminum alloy 5083 manufactured by laser powder bed fusion", Addit. Manuf. 28 (2019) 485–496. DOI 10.1016/j.addma.2019.05.027
- Read: ABSTRACT ONLY (Semantic Scholar). The only OA copy is a ScienceDirect author manuscript.
- AA5083 + 0.7 wt.% Zr, gas-atomized powder. Laser powers 200 W and 350 W with various speeds. Plain AA5083 was unprintable (pores, cracks, or "compositional deviation due to evaporation"). 5083+Zr was near-full density, crack-free and "with proper composition". As-built YS 212 / UTS 317 MPa / El 22.3 %. After 400 °C/2 h: YS 319 / UTS 392 MPa / El 14.1 %. Primary Al3Zr at melt-pool boundaries, and ~3 nm Al3Zr after HT. Melt/atomization temperature, powder size, optimum parameters and plate T: NOT accessed.

## 12. Mehta, A. et al. (University of Central Florida), "Additive manufacturing and mechanical properties of the dense and crack free Zr-modified aluminum alloy 6061 fabricated by the laser-powder bed fusion", Addit. Manuf. 41 (2021) 101966. DOI 10.1016/j.addma.2021.101966
- Read: ABSTRACT ONLY (Semantic Scholar).
- AA6061 + 1 wt.% Zr, gas-atomized powders. Plain 6061 cracked "regardless of LPBF parameters". 6061+Zr was crack-free "for a certain LPBF processing window". As-built YS 210 / UTS 268 MPa / strain-at-failure 26.5 %. After T6: 300 / 327 MPa / 14 %. Crack-freedom comes from grain refinement. Atomization melt temperature, powder size, parameters and plate T: NOT accessed.

---

## Summary table

| Alloy | Measured composition (wt%) | Best parameters | Plate T | As-built YS/UTS/El | Aged YS/UTS/El (treatment) | Density | Full text? |
|---|---|---|---|---|---|---|---|
| Chalmers C (Al-Mn-Cr-Zr) | 5.0Mn-0.8Cr-0.6Zr (ICP printed) | M100: 170 W/1500 mm/s/0.10/30 µm, 40 µm spot. M290: 370 W/1300/0.13/30, 100 µm spot | M100 none possible; M290 not stated | 250/310/25 (thesis Tbl 8). 102 HV (M100) | 350/440/8 (648 K 24 h per thesis; 14 h per Mater. Des.). 142–143 HV at 648 K/14 h or 623 K/24 h | 99.5–99.6 % (M100), >99.7 % (M290) | Yes |
| Chalmers B (Zr-free) | 4.9Mn-0.8Cr | M100 DOE (range in Tbl 2, not seen) | none | 99 HV only | over-ages after ~1 h at 678 K | ~99.5 %, crack-free | Yes (Tbl 2 not seen) |
| Chalmers D | 4.7Mn-0.8Cr-1.2Zr | M290 370/1300/0.13/30 | not stated | 300/330/25 | 360/430/3 (648 K 4 h) | >99.7 % | Yes |
| Chalmers E | 4.7Mn-0.8Cr-0.7Zr-1.0Mg | same | not stated | not tested (cracks) | +40 HV, 8 h at 648 K | cracked | Yes |
| Chalmers F | 4.8Mn-0.9Cr-1.1Zr-1.2Mg | same | not stated | 390/450/17 | 500/560/5 (648 K 8 h). 172 HV | >99.8 % | Yes |
| Mair Al-Mn-Ti-Zr | powder 4.80Mn-0.82Ti-0.71Zr; part 4.50Mn-0.77Ti-0.69Zr | AconityLAB 380 W/1900/0.10/30, stripes 10 mm, 67° | no preheat | 284/320/16.9; 108 HV10 | none reported | 99.9 % | Yes |
| Al-1Fe-1Zr (Pauzon) | not accessed | not accessed | n.a. | not accessed | YS 310 (Scripta), 330 (Acta snippet), 400 °C/4 h | not accessed | Abstract |
| Al-2.5Fe (Qi) | nominal 2.5Fe | 204 W, ≤800 mm/s (other params n.a.) | n.a. | UTS ~320 | 300 °C anneal: UTS kept | >99 % | Abstract |
| Al-2.5Fe-2Mn (Wang) | nominal | n.a. | n.a. | RT n.a.; >240 MPa at 300 °C | n.a. | >99 % | Abstract |
| Al-Fe-Mg-Zr (Li) | your values | your values | not accessed | your values | your values | 99.8 % | Blocked |
| Al-1Fe-0.6Cu-1.3Zr (Xu) | n.a. | n.a. | n.a. | YS 500 (snippet) | n.a. | near-full | Snippet only |
| Al-5Fe-6Cr (Pérez-Prado) | nominal | n.a. | n.a. | 192 HV; YS 273 at 300 °C | n.a. | 99.8 % | Abstract |
| 5083+0.7Zr (Zhou) | nominal | 200/350 W tested | n.a. | 212/317/22.3 | 319/392/14.1 (400 °C/2 h) | near-full | Abstract |
| 6061+1Zr (A. Mehta) | nominal | n.a. | n.a. | 210/268/26.5 | 300/327/14 (T6) | near-full | Abstract |
