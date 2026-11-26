# Primary-paper check: Al alloys for LPBF seed recipes (papers_b)

Checked 2026-11-26. About 40 minutes of work. Values are quoted from the papers. "Abstract only" means only the abstract was read, and everything else is "not accessed". "Read from figure" means the value is approximate. ScienceDirect, Wiley, HAL (Anubis bot check) and Monash Bridges (Cloudflare) all put up challenge pages; none was attempted. The Brunel repository timed out.

---

## 1. Knoop et al., "A Tailored AlSiMg Alloy for Laser Powder Bed Fusion", Metals 10(4) 514 (2020). DOI 10.3390/met10040514
**Read:** FULL TEXT (MDPI HTML via the tunnel browser; tables parsed from the page HTML).
- **Composition.** Nominal AlSi3.5Mg2.5 "with additions of common micro alloying elements". Powder by ICP-OES (Table 1, wt%): Si 3.3, Mg 2.3, O 0.07, H 97 ppm, "Other" 0.43, Al bal. Footnote: "Other: Including Mn, Zr, Fe, and other impurities". **The alloy is NOT stated to be Zr-free.** Mn, Zr and Fe are lumped into the 0.43 %, with no breakdown given. Table 1 is titled "powder and bulk material" but shows only a powder row, so no printed-part composition and no Mg-loss figure. Theoretical max Mg2Si is 3.96 wt%.
- **Powder.** Closed-coupled gas atomisation by Ecka Granules Germany GmbH (Velden). Size 20-63 µm, with some particles above 63 µm. D10/D50/D90 are not given as numbers (curve in Fig. 1).
- **LPBF.** Main machine SLM Solutions SLM 125 HL (400 W Yb fibre, minimum focus 68 µm). "Best results ... volume energy density of 61.7 J/mm³, a laser power of 370 W and a layer thickness of 50 µm". **Scan speed and hatch are not stated.** The tested window and scan strategy are not given beyond "scanning vectors in each layer were rotated". Parameters were later transferred to a Concept Laser M2, with no M2 parameters given. Atmosphere not stated.
- **Plate temperature.** Methods say builds at 50 °C and 120 °C, but Results report 100 °C and 50 °C, so the paper is internally inconsistent. Heat-treatment development used 50 °C, held by "pausing this process for 3 min after the exposure of each layer". The authors warn that a 200 °C plate over-ages the alloy during the build.
- **Density / cracking.** No relative-density number. Samples described as dense and crack-free, with "single, fine pores".
- **Tensile.** Vertical (Z) cylindrical bars, DIN 50125 type B, 5 mm diameter, machined. Note: the bars that accompanied the bending tests were not machined.
  - As-built, SLM125, 100 °C plate: YS 381 ± 3 MPa, UTS 483 ± 3, A 6.1 ± 1.2 %.
  - As-built, SLM125, 50 °C plate: YS 270 ± 1, UTS 442 ± 1, A 12.7 ± 0.8 %.
  - As-built, Concept Laser M2 (plate T not given): YS 417 ± 3, UTS 506 ± 4, A 10.1 ± 1.3 %.
  - Direct ageing (T5-type, no solution treatment) from the 50 °C builds, Table 2:
    - 140 °C 1 h: 311 ± 2 / 463 ± 4 / 8.4 ± 1.0
    - 140 °C 2.5 h: 323 ± 2 / 466 ± 13 / 10.2 ± 2.0
    - **170 °C 1 h (chosen): 348 ± 1 / 484 ± 1 / 10.5 ± 1.3**
    - 190 °C 30 min: 411 ± 1 / 485 ± 2 / 4.7 ± 0.9
    - 190 °C 1 h: 408 ± 2 / 475 ± 3 / 3.7 ± 1.3
  - Soft anneal (best ductility): YS 96 ± 6, UTS 179 ± 2, A 25.6 ± 0.9 %. Fig. 6b covers 250-380 °C.
  - **No T6 (solution + age) data in this paper.**
  - Bending angle (VDA 238-100, unmachined) / UTS:
    - As-built: 26.8° / 407 MPa
    - 170 °C 1 h: 21.0° / 453 MPa
    - 380 °C 1 h: 96.5° / 181 MPa
  - Reference alloys:
    - AlSi10Mg as-built: 16.7° / 429 MPa
    - Scalmalloy as-built: 79.1° / 366 MPa
    - Scalmalloy 325 °C 4 h: 27.3° / 496 MPa
- **Ageing.** No over-ageing at 170 °C up to 10 h.
- **Microstructure.** EBSD mean grain size 6.2 ± 5.7 µm (longitudinal) and 6.0 ± 4.6 µm (transverse). Columnar grains in the melt pool, fine equiaxed grains at the pool bottom, no clear texture. Cells under 1 µm with a Si-rich film at the cell boundaries.
- **Companion paper:** Solanki et al., "LPBF and heat treatment of a Mg2Si-rich aluminium alloy", Prog. Addit. Manuf. 11 (2026) 4611-4631, DOI 10.1007/s40964-026-01583-1. FULL TEXT read (Springer, OA).
  - Same alloy, now sold as CustAlloy® by Kymera Ecka.
  - DMG MORI LASERTEC 30 SLM, argon, **no build-plate heating**.
  - Window: P 370 W and t 50 µm fixed; v 800-1800 mm/s; h 0.05-0.125 mm.
  - Best: **v 1200 mm/s, h 0.1 mm**, VED 61.7 J/mm³, relative density 99.87 %. Worst: 97.70 % at 1800 mm/s.
  - This is the same VED as Knoop, so Knoop's unstated v and h are probably 1200 mm/s and 0.1 mm. That is an inference, not stated by Knoop.
  - Grain size 6.6 µm.
  - Hardness: 130 HBW as-built, peak 164 HBW at DA 190 °C 330 min. Solution treatment at 540 °C drops it to 35-61 HBW.
  - No tensile data. The Table 3 composition was not visible.
- **Useful for our seed recipe:**
  - ~Al-3.3Si-2.3Mg prints dense on a 370 W, 50 µm, ~62 J/mm³ recipe.
  - Keep the plate cold (≤50-100 °C) and direct-age at 170-190 °C for ~1 h.
  - Ask the supplier what is in the 0.43 % "Other (Mn, Zr, Fe)" before calling it a Zr-free benchmark.

## 2. Kimura et al., MSEA 754 (2019) 786-798. DOI 10.1016/j.msea.2019.02.015
**Read:** ABSTRACT ONLY (Semantic Scholar). ScienceDirect has a human-verification check; no OA copy found.
- Alloys: Al-4Si with Mg rising to ~2.5 mass% (Al-4Si up to Al-4Si-2.0Mg, plus Al-4Si-2.5Mg). The exact Mg steps are not in the abstract.
- Density: >99.5 % up to 2.0Mg. "Approximately 99.4 %" at 2.5Mg, because of gas pores from Mg evaporation.
- Tensile strength and 0.2 % proof stress "significantly increased with the Mg content". Elongation "decreased in a stepwise manner", blamed on gas pores and shrinkage cavities. **No numbers in the abstract.** Cracking is not mentioned in the abstract.
- Machine, parameters, plate T, numbers: not accessed.
- **Useful for our seed recipe:** Al-4Si-(0-2.5)Mg is a Mg ladder that has already been printed. Above ~2 % Mg, expect Mg-vapour porosity.

## 3. Magsimal-59-type / Al-Mg2Si pseudo-binary eutectic by LPBF
No LPBF paper on "AlMg5Si2Mn" or "Fehrmann AlMgty" turned up in Crossref or OpenAlex (searches returned nothing relevant). Two Al-Mg2Si papers were found:
- **(3a) Yang et al. (Brunel), "Microstructure and mechanical properties of pseudo binary eutectic Al-Mg2Si alloy processed by LPBF", J. Mater. Res. Technol. 24 (2023) 2187-2199. DOI 10.1016/j.jmrt.2023.03.147.** ABSTRACT ONLY. Gold OA, but the ScienceDirect copy is behind the challenge and the Brunel BURA copy timed out.
  - Alloy: Al-9.6Mg-4.9Si wt% (= Al-13.3Mg2Si), "low solidification range and hot-cracking susceptibility ... successfully processed".
  - Density: 99.3 % at VED 129.6 J/mm³.
  - As-built: **UTS 557 MPa, YS 439 MPa, El 2.9 %**.
  - Microstructure: fine α-Al, cellular eutectic Mg2Si, GP zones, α-Al12(Fe,Mn)3Si.
  - Measured composition, machine, plate T: not accessed.
- **(3b) Otani et al., Mater. Des. 252 (2025) 113787. DOI 10.1016/j.matdes.2025.113787.** ABSTRACT ONLY.
  - Crack-free, relative density >99.5 %.
  - Mg vaporisation: Mg fell from 11.3 to 7.6 % in the part. Printed composition Al-7.6Mg-5.4Si wt%.
  - Room temperature: UTS 529 MPa, ductility <2 %.
  - Primary Mg2Si appears at Mg-rich pool boundaries.
  - YS, machine, parameters: not accessed.
- **Useful for our seed recipe:** near-eutectic Al-Mg2Si (Al-~10Mg-~5Si) prints crack-free with no Zr or Sc and gives YS ~440 MPa as-built, but elongation is only 2-3 %. Budget for large Mg loss (11.3 → 7.6 % in 3b).

## 4. Dreano et al., "Computational design of a crack-free aluminum alloy for additive manufacturing", Addit. Manuf. 55 (2022) 102876. DOI 10.1016/j.addma.2022.102876
**Read:** NOT ACCESSED. Title, authors and DOI confirmed via Crossref. ScienceDirect and HAL (hal-03791539) both show bot or human checks, and no abstract was available from OpenAlex or Semantic Scholar. The composition in the brief (Al-6.7Mg-3Si-1.4Ni-1Zn-0.3Fe) is **unverified**.

## 5. A357 / AlSi7Mg0.6
- Aversa et al., Metals 7 (2017) 68, DOI 10.3390/met7020068. ABSTRACT ONLY (MDPI blocked direct download; I ran out of time for a tunnel fetch).
  - Builds on platforms "heated up to different temperatures". The platform acts as in-situ ageing, and the optimum platform temperature gave +17 % UTS.
  - Direct ageing was also studied.
  - Numbers not accessed.
- Rao et al., Mater. Des. (2016), DOI 10.1016/j.matdes.2016.07.009, and Rao et al., Addit. Manuf. (2017), DOI 10.1016/j.addma.2017.08.007: NOT ACCESSED (Elsevier, closed, no abstract retrieved).
- No paper matching "Yang, Rometsch et al. 2018" on A357 was identified. The closest is Rao et al., Int. J. Fatigue 2019, DOI 10.1016/j.ijfatigue.2019.105215 (not accessed).
- Martin et al. (paper 13) report AlSi10Mg on a Concept Laser M2: YS 209, UTS 315 MPa, El 7.3 %.

## 6. Croteau et al., Acta Mater. 153 (2018) 35-44. DOI 10.1016/j.actamat.2018.04.053
**Read:** FULL TEXT of the ACCEPTED MANUSCRIPT (Empa DORA, CC-BY-NC-ND), read as rendered page images. Not the typeset version.
- **Composition (powder, ICP-OES at ATI Wah Chang):** Al-3.60Mg-1.18Zr and Al-3.66Mg-1.57Zr wt% (= Al-4.0Mg-0.35Zr and Al-4.0Mg-0.47Zr at%). Printed part: "decrease in magnesium concentration from 3.6 to 2.7 wt.% in the bulk samples processed with the highest laser energy density".
- **Powder:** NanoAl LLC "Addalloy™", inert-gas atomised by Nanoval GmbH (Berlin). Sieved to 10-45 µm with d50 = 13.7 µm. The tensile blocks used 8-25 µm powder; the TEM sample used d50 = 37 µm powder with 40 µm layers.
- **LPBF:** Concept Laser M2, 200 W fibre laser, 1071 nm, M² = 1.02, spot 90 µm. Argon with <0.5 % O2.
  - Window: P = 200 W, t = 30 µm, h = 135 or 150 µm, v = 200-800 mm/s, so E = 56-247 J/mm³. Chessboard scan strategy.
  - Tensile blocks: E = 247 J/mm³ (200 W, 200 mm/s, 135 µm, 30 µm).
  - **Plate temperature not stated** in the manuscript.
- **Density / cracking:** >99.2 % relative density (Archimedes and image analysis) for E = 123-247 J/mm³, "reliably producing crack-free samples". The abstract gives 99.2-99.9 %.
- **Tensile:** 16 dogbones per alloy, machined, gauge 2.5 mm diameter × 8.0 mm long. Half Z, half XY.

  | Alloy | Condition | Orientation | YS (MPa) | UTS (MPa) | El (%) |
  |---|---|---|---|---|---|
  | Al-3.60Mg-1.18Zr | as-fabricated | Z | 221 ± 1 | 287 ± 1 | 25.6 ± 0.8 |
  | Al-3.60Mg-1.18Zr | as-fabricated | XY | 220 ± 3 | 292 ± 2 | 29.0 ± 1.6 |
  | Al-3.66Mg-1.57Zr | as-fabricated | Z | 282 ± 8 | 332 ± 2 | 24.0 ± 1.0 |
  | Al-3.66Mg-1.57Zr | as-fabricated | XY | 290 ± 6 | 329 ± 3 | 25.2 ± 1.8 |
  | Al-3.60Mg-1.18Zr | peak-aged | Z | 350 ± 7 | 382 ± 5 | 17.1 ± 2.0 |
  | Al-3.60Mg-1.18Zr | peak-aged | XY | 353 ± 5 | 386 ± 3 | 18.6 ± 0.9 |
  | Al-3.66Mg-1.57Zr | peak-aged | Z | 349 ± 15 | 383 ± 5 | 19.5 ± 4.4 |
  | Al-3.66Mg-1.57Zr | peak-aged | XY | 365 ± 11 | 389 ± 4 | 23.9 ± 4.4 |

  The table says only "post heat treatment / peak-aged". The hardness figure for the peak is 400 °C / 8 h.
- **Hardness:** as-fabricated 875 ± 27 MPa (1.18Zr) and 961 ± 33 MPa (1.57Zr). Both reach 1310 ± 42 MPa after 400 °C / 8 h.
  - Ageing at 400 °C: first peak at ~2 h, second at ~6-8 h. Hardness is ~90 % of peak after 60 h.
- **Microstructure:**
  - Bimodal grains: fine equiaxed 770 ± 340 nm at the melt-pool boundaries, each nucleated on a cuboidal primary L1₂ Al3Zr; columnar grains ~1 µm wide × ~5-10 µm long with [100] texture.
  - Nano-oxides are present.
  - Fine grains grow from 770 to 1280 nm after 144 h at 400 °C.
- **Useful for our seed recipe:**
  - Zr ≥ ~1.2 wt% (hyper-peritectic) is what makes Al-3.6Mg crack-free.
  - Expect ~25 % relative Mg loss at high energy density.
  - Peak-age at 400 °C / ~8 h: YS ~350-365 MPa with 17-24 % elongation, isotropic.

## 7. Jia et al., Acta Mater. 171 (2019) 108-118, DOI 10.1016/j.actamat.2019.04.014; Bayoumy et al., Mater. Des. 198 (2021) 109317, DOI 10.1016/j.matdes.2020.109317
- **Jia:** ABSTRACT ONLY. Mn and Sc are the main strengthening elements. After 300 °C / 5 h: **YS up to 560 MPa, ductility ~18 %**. Composition, parameters and platform T not in the abstract, so not accessed.
- **Bayoumy:** ABSTRACT ONLY. Gold OA, but the ScienceDirect, Monash and KIT copies were not retrieved: Monash returned a Cloudflare challenge, and KIT was not tried for lack of time.
  - Optimum window gives relative density >99.8 %, "all ... yield strength exceeding 430 MPa and ductility of over 17 %".
  - Bimodal grains, with Al3Sc and Mn(Fe)-rich quasicrystal particles.
  - Composition and parameters not accessed.

## 8. Spierings et al.: Mater. Des. 115 (2017) 52-63, DOI 10.1016/j.matdes.2016.11.040; CIRP Annals 65 (2016), DOI 10.1016/j.cirp.2016.04.057
NOT ACCESSED: closed, and no abstract was available from OpenAlex or S2. Knoop et al. cite Scalmalloy as Al-4.6Mg-0.66Sc-0.42Zr-0.49Mn, as do Croteau et al. (second-hand). Knoop's own Scalmalloy on an EOS M290 (45 µm, 48 J/mm³) gave UTS 366 MPa as-built and 496 MPa after 325 °C / 4 h.

## 9. Low-Sc Al-Mg-Sc-Zr; Li et al., "Developing a high-strength Al-Mg-Si-Sc-Zr alloy for SLM", Acta Mater. 193 (2020) 83-98, DOI 10.1016/j.actamat.2020.03.060
**Li 2020:** ABSTRACT ONLY.
- Al-xMg-0.2Sc-0.1Zr (x = 1.5, 3.0, 6.0) all hot-crack, and crack density rises with Mg.
- Adding 1.3 wt% Si to Al-6Mg-0.2Sc-0.1Zr "effectively inhibits hot cracking".
- Final alloy Al-8.0Mg-1.3Si-0.5Mn-0.5Sc-0.3Zr: as-printed UTS 497 MPa, El 11 %; aged UTS 550 MPa, El 8-17 %.
- No separate low-Sc variation paper was read (not accessed).
- **Useful for our seed recipe:** at low Sc and Zr (0.2 / 0.1), Al-Mg cracks, but adding Si (Mg2Si eutectic) cures it. This is the same mechanism as papers 1 and 3.

## 10. Er-bearing alloys (Er as Sc substitute)
Most of these papers come from one university group in Beijing; a second group published Yu et al. 2023. Affiliations were not checked, because only abstracts were read for most of them.
- **Guo et al., "Microstructure and mechanical properties of Al-Mg-Mn-Er-Zr alloys fabricated by LPBF", Mater. Des. 222 (2022) 111064. DOI 10.1016/j.matdes.2022.111064.** ABSTRACT ONLY.
  - Primary Al3Zr at the pool boundary refines grains and "suppresses the formation of solidification cracking".
  - Ageing gives Al3(Er,Zr) core-shell precipitates. Best: YS 440 ± 3, UTS 520 ± 2, El 15.5 ± 1.0 %.
  - Composition not accessed.
- **Wei et al., JMRT 35 (2025) 6147-6155, DOI 10.1016/j.jmrt.2025.02.257.** ABSTRACT ONLY.
  - Al-8.5Mg-0.78Mn-0.96Er-1.94Zr. Primary L1₂ Al3(Er,Zr) gives nearly fully equiaxed grains.
  - As-built: UTS 521, YS 446, El 14 %. Ageing raises YS and lowers elongation (no number in the abstract).
- **Yu et al., Met. Mater. Int. 29 (2023) 3235-3248, DOI 10.1007/s12540-023-01449-z.** FULL TEXT (Springer, via tunnel).
  - ICP-AES (wt%): powder Mn 6.01, Mg 2.74, Er 0.86, Zr 0.52; printed Mn 5.82, Mg 2.68, Er 0.79, Zr 0.54.
  - Powder: VIGA, D50 35.6 µm, D90 56.8 µm.
  - Machine EP M250. t 30 µm; P 250 or 350 W; v 800-1200 mm/s; h 100 µm; 67° rotation; **platform 100 °C**; argon.
  - Cracks in most samples ("weak grain refining effect of the Er"). Only 350 W / 800 mm/s gave ~99 % with "no obvious keyhole or crack".
  - Grains: columnar, ~5 µm wide.
  - As-built: YS 327 ± 5, UTS 502 ± 3, El 12.2 ± 1 %.
  - 350 °C / 6 h: 171 ± 1 HV, YS 339 ± 2, UTS 508 ± 1, El 8.1 ± 1 %.
- Yu et al., Trans. Nonferrous Met. Soc. China 34 (2024) 2431, DOI 10.1016/S1003-6326(24)66551-9. ABSTRACT ONLY. Adding Si to Al-Mn-Mg-Er-Zr eliminated cracks: 99.6 %, YS 371 ± 7, UTS 518 ± 6.
- Gao et al., JMRT 38 (2025) 118, Al-Mg-Er-Zr-Sc (abstract only): YS 521, UTS 531, El 12 % after heat treatment.
- **Er without Zr:** none of the papers I found prints an Er-bearing, Zr-free Al-Mg alloy crack-free. Every Er alloy found also contains Zr (0.5-1.94 %), with Sc or Si in some. Even with 0.5 % Zr, Yu 2023 cracked across most of the window.

## 11. Taheri-Mousavi et al., Adv. Mater. (2025), DOI 10.1002/adma.202509507 (arXiv 2406.17457)
**Read:** FULL TEXT of the arXiv version, including supplementary discussion. The published Adv. Mater. version (title "...Coarsening-Resistant Microstructures Achieved via...") was not compared.
- **Final composition is Al-Ni-Zr-Er only. Y and Yb are NOT in it;** they belong to the benchmark "alloy 1" of Gong et al., Al-2.14Ni-1.15Zr-1.35Er-0.25Y-0.73Yb.
  - Nominal: Al-2.73Ni-3.19Zr-2.33Er wt% (Ni 1.33 at%, Zr 1 at%).
  - Powder by XRF: Al-2.47Ni-3.25Zr-2.38Er.
  - Printed part by XRF: Al-2.55Ni-2.9Zr-2.37Er.
- **Powder:** ultrasonic atomisation (AUS500, Indutherm Bluepower; acknowledgements credit AMAZEMET). PSD is reported as "d10 = 44.5 %, d50 = 63.8 %, d90 = 91.5 %", units as printed.
- **LPBF:** SLM Solutions 250 HL, 70 µm beam. 350 W, h 120 µm, v 1100 mm/s, t 50 µm, 8 mm stripes, 67° rotation. **Preheat 200 °C.** Ar-4.6 with O2 <1000 ppm. Crack-free cubes.
- **Properties:**
  - 180 HV as-built. Peak hardness after 8-10 h at 400 °C, "~50 % higher hardness than the benchmark".
  - Tensile values are only in Fig. 3c (curves, not read numerically). The paper says "50 % higher yield strength" than alloy 1.
  - Equiaxed, untextured grains of 1-2 µm.
- **Useful for our seed recipe:** the Er route still relies on ~3 wt% Zr. It is not an Er-only design.

## 12. Tan, Zhang et al., Acta Mater. 196 (2020) 1-16. DOI 10.1016/j.actamat.2020.06.026 (SSRN preprint 10.2139/ssrn.3592041)
NOT ACCESSED. Elsevier is closed, there was no time for SSRN (also Cloudflare-fronted), and no abstract was retrieved.

## 13. Martin et al., "3D printing of high-strength aluminium alloys", Nature 549 (2017) 365-369. DOI 10.1038/nature23894
**Read:** FULL TEXT (nature.com via tunnel, plus the Table 1 page).
- **Feedstock:** Valimet 7075 powder: Zn 5.40, Mg 2.25, Cu 1.54, Cr 0.19, Fe 0.17, Si 0.13, Mn 0.02, Ti <0.01 wt%. Valimet 6061: Mg 0.83, Si 0.62, Fe 0.25, Cu 0.23, Cr 0.08, Mn 0.04, Zn 0.04, Ti 0.02. Both ~45 µm.
- **Zr addition:** coated with **1 vol% hydrogen-stabilised Zr (ZrH2) nucleants** by electrostatic assembly. Not expressed in wt%.
- **LPBF:** Concept Laser M2 (400 W) running Concept Laser's standard AlSi10Mg parameters, which the paper calls "proprietary ... cannot be accessed by the user". Island scanning with 2 mm islands. Layers 25-80 µm. Flowing argon. **"Room temperature with no applied heat to the build plate."** 6061 build plates.
- **Mg/Zn loss (ICP-OES, 7075+Zr):** ~32 % Mg loss and ~25 % Zn loss.
- **Heat treatment (T6):** 480 °C / 2 h, water quench, then 120 °C / 18 h.
- **Tensile (Table 1):**
  - AM 7075 + Zr T6: YS 325-373, UTS 383-417 MPa, E 63-66 GPa, El 3.8-5.4 %.
  - AM 7075 T6 (no Zr): UTS 25.5 MPa, El 0.4 % (cracked).
  - AM AlSi10Mg: YS 209, UTS 315, El 7.3 %.
  - No 6061 + Zr tensile values are given; only micrographs show it crack-free.
- **Useful for our seed recipe:** with Zr nucleants, 7075 prints crack-free on a cold plate, but loses ~1/3 of its Mg.

## 14. Uddin et al., Addit. Manuf. 22 (2018) 405-415. DOI 10.1016/j.addma.2018.05.047
**Read:** ABSTRACT ONLY (Semantic Scholar).
- **Powder-bed heating 500 °C** gives crack-free AA6061 and removes melt-pool banding.
- As-fabricated: HV 54; YS 60, UTS 130 MPa, El 15 %. Heat-treated parts are "comparable to ... T6" (no numbers in the abstract).
- Grains: columnar [100], ~25 µm × 400 µm.
- **Machine not given in the abstract.** The Aconity attribution is unconfirmed (not accessed).

---

## Summary table

| Alloy | Measured composition (wt%) | Best parameters | Plate T | As-built YS/UTS/El | Aged YS/UTS/El (treatment) | Density | Full text? |
|---|---|---|---|---|---|---|---|
| AlSi3.5Mg2.5 (Knoop 2020) | powder Si 3.3, Mg 2.3, other 0.43 (incl. Mn, Zr, Fe) | SLM125: 370 W, 50 µm, 61.7 J/mm³ (v/h not stated; 1200 mm/s / 0.1 mm in the 2026 companion) | 50 or 100 °C (Methods also say 120 °C) | 270/442/12.7 % (50 °C); 381/483/6.1 % (100 °C); 417/506/10.1 % (CL M2) | 348/484/10.5 % (170 °C 1 h); 411/485/4.7 % (190 °C 0.5 h); no T6 | not given (99.87 % in 2026 companion) | Yes |
| Al-4Si-xMg, x ≤ 2.5 (Kimura 2019) | not accessed | not accessed | n/a | rises with Mg (no numbers) | n/a | >99.5 % (≤2Mg); ~99.4 % (2.5Mg) | Abstract |
| Al-9.6Mg-4.9Si (Yang 2023) | not accessed | VED 129.6 J/mm³ | not accessed | 439/557/2.9 % | n/a | 99.3 % | Abstract |
| Al-7.6Mg-5.4Si (Otani 2025) | part 7.6Mg (from 11.3) | not accessed | not accessed | UTS 529, El <2 % | n/a | >99.5 % | Abstract |
| Al-Mg-Si-Ni-Zn (Dreano 2022) | unverified | not accessed | not accessed | not accessed | not accessed | not accessed | No |
| Al-3.60Mg-1.18Zr / Al-3.66Mg-1.57Zr (Croteau 2018) | ICP of powder as named; Mg 3.6 → 2.7 in part | CL M2: 200 W, 200 mm/s, 135 µm, 30 µm, 247 J/mm³, chessboard | not stated | 220-221/287-292/26-29 %; 282-290/329-332/24-25 % | 350-353/382-386/17-19 %; 349-365/383-389/20-24 % (peak, 400 °C ~8 h) | >99.2 % | Yes (AAM) |
| Al-Mn-Sc (Jia 2019) | not accessed | not accessed | not accessed | not accessed | YS ≤560, El ~18 % (300 °C 5 h) | not accessed | Abstract |
| Al-Mn-Mg-Sc-Zr (Bayoumy 2021) | not accessed | not accessed | not accessed | YS >430, El >17 % | not accessed | >99.8 % | Abstract |
| Al-8Mg-1.3Si-0.5Mn-0.5Sc-0.3Zr (Li 2020) | not accessed | not accessed | not accessed | UTS 497, El 11 % | UTS 550, El 8-17 % | not accessed | Abstract |
| Al-Mg-Mn-Er-Zr (Guo 2022) | not accessed | not accessed | not accessed | not accessed | 440/520/15.5 % | not accessed | Abstract |
| Al-8.5Mg-0.78Mn-0.96Er-1.94Zr (Wei 2025) | not accessed | not accessed | not accessed | 446/521/14 % | YS up, El down | not accessed | Abstract |
| Al-Mn-Mg-Er-Zr (Yu 2023) | part Mn 5.82, Mg 2.68, Er 0.79, Zr 0.54 | EP M250: 350 W, 800 mm/s, 100 µm, 30 µm | 100 °C | 327/502/12.2 % | 339/508/8.1 % (350 °C 6 h) | ~99 % (cracks elsewhere) | Yes |
| Al-Ni-Zr-Er (Taheri-Mousavi 2025) | part Ni 2.55, Zr 2.9, Er 2.37 (XRF) | SLM 250HL: 350 W, 1100 mm/s, 120 µm, 50 µm | 200 °C | 180 HV (tensile in figure only) | peak 400 °C 8-10 h | crack-free | Yes (arXiv) |
| 7075 + 1 vol% ZrH2 (Martin 2017) | powder as listed; −32 % Mg, −25 % Zn | CL M2 with proprietary AlSi10Mg set | room temperature, no heating | n/a | 325-373/383-417/3.8-5.4 % (T6) | "some residual porosity" | Yes |
| AA6061 (Uddin 2018) | not accessed | not accessed | 500 °C bed | 60/130/15 % | ≈ T6 (no numbers) | not accessed | Abstract |
| AlSi10Mg (Martin 2017, CL M2) | CL31 spec | proprietary | room temperature | 209/315/7.3 % | n/a | n/a | Yes |
| 2024 + Ti (Tan 2020), A357 (Rao), Scalmalloy (Spierings) | not accessed | not accessed | not accessed | not accessed | not accessed | not accessed | No |
