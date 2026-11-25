# Edison Scientific LITERATURE_HIGH Output — Domestically-Secure Elemental Substitutions for Import-Reliant Solutes in LPBF Al Alloys

**Task ID:** `90e31524-e8e4-4a69-9bb2-5f8a7158d3af`
**Mode:** LITERATURE_HIGH | **Date:** 2026-06-29 | **Size:** ~31K chars
**Context:** PR #93 follow-up. Companion to the import-reliance audit of the 15 non-Al
solutes (`Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn`) and the
`alloy_element_bounds.csv` caps used by `edison-trajectories/composition-scaling-verify.py`.

> *Raw Edison Scientific output below. The query prompt appears first, followed by the model's structured response.*

---

Question:
For LPBF printable Al alloys, which DOMESTICALLY SECURE / abundant alloying elements (low U.S. net-import-reliance) can metallurgically SUPPLANT the most import-reliant critical solutes (Sc, Er, Sn, Mn, Ti, Cr, Ni, Mg), and at what performance cost? Six substitution hypotheses were posed (Zr→Sc/Er; Fe→Ni/Ti; Ce→Sc/Mn/Cr; B→Sc/Ti grain refinement; Ca→Mg/REE; Si-expanded→Mg/Cu/Mn-lean), plus a request to name additional domestically-secure elements worth adding to the palette and to rank the opportunities. Full prompt preserved in PR #93 thread.

---

# Domestically Secure Elemental Substitutions for Import-Reliant Solutes in LPBF Aluminum Alloys

## Overview

This report evaluates six substitution hypotheses for replacing import-reliant alloying elements (Sc, Er, Sn, Mn, Ti, Cr, Ni, Mg) with domestically secure or abundant alternatives in laser powder bed fusion (LPBF) printable aluminum alloys. Each substitution is assessed for metallurgical mechanism, quantified performance, LPBF printability, and supply-chain rationale. Two additional elements not in the current 15-element palette—boron (B) and calcium (Ca)—are identified as high-value additions.

The following table summarizes all six substitution hypotheses with quantified performance data:

| Substitution hypothesis | Domestic element(s) used | Import-reliant element(s) displaced | Representative alloy(s) | Key mechanical properties at RT (YS / UTS / EL) | High-temp performance | LPBF printability | Supply-chain benefit (NIR reduction) | Performance vs. benchmark |
|---|---|---|---|---|---|---|---|---|
| **Zr → Sc/Er** | Zr (domestic zircon feedstock; mixed refining case) | Sc, Er / heavy REE | Scalmalloy benchmark; Sc-lean Al-Mg-Sc-Zr; emerging Sc-free Al-Mg-Zr / Addalloy-type concepts | **Benchmark Scalmalloy (aged):** 468-508 / 517-541 / ~8.5-15.9%; **Sc-lean Al-Mg-Sc-Zr:** UTS ~536 MPa aged | Scalmalloy-class alloys retain strength via Al3(Sc,Zr); Zr contributes coarsening resistance and L1\_2 precipitation | Strong: Al-Mg-(Sc,)Zr is a proven LPBF family; Sc-free Al-Mg-Zr is being actively developed | Removes the **highest-risk** solutes (Sc, Er), but does **not** remove Zr dependence; major reduction in REE reliance | **Strong but incomplete substitute**: Zr can cover precipitation/grain-refinement roles, but available evidence still falls short of proving full Scalmalloy parity without some Sc; likely modest-to-moderate strength penalty unless paired with another domestic element such as Fe, Ce, or Si (mehta2021laserpowderbed pages 7-10, boillatnewport2024heattreatmentpostprocessing pages 9-11, cerri2024mainheattreatments pages 14-16, lu2023microstructuralevaluationand pages 1-2) |
| **Fe → Ni/Ti** | Fe (fully domestic / U.S. net exporter), often with Zr or Cr | Ni, Ti (and partly Mn/Cr in heat-resistant roles) | Al-5Fe-6Cr; CP1 Al-Fe-Zr; comparison benchmark: DuAlumin-3D Al-9Ce-4Ni-0.5Mn-1Zr | **Al-5Fe-6Cr:** 400 / 547 / 3.8% | **YS:** 273 MPa at 300°C; 179 MPa at 400°C; excellent thermal stability from slow-diffusing Fe-bearing intermetallics / i-phases | Strong for high-temp alloys; Fe-bearing LPBF alloys are printable and specifically developed for AM; CP1 also has good processability | Very high: can directly displace **Ni** and partially avoid **Ti** for elevated-temperature strengthening, while using the most secure solute in the set | **One of the strongest substitution cases** for high-temperature service: much better thermal retention than AlSi10Mg and competitive with Ni-bearing AM Al in the 250-400°C window, though RT ductility is low and some systems still rely on Cr or Zr (perezprado2022anal5fe6cralloy pages 7-9, perezprado2022anal5fe6cralloy pages 1-2, perezprado2022anal5fe6cralloy pages 9-10, yadegari2025aluminumlaseradditive pages 14-15, plotkowski2025additivelymanufacturinghightemperature pages 12-17, plotkowski2025additivelymanufacturinghightemperature pages 8-12) |
| **Ce → Sc / Mn / Cr** | Ce (domestically mineable light REE), optionally with Ca and Mn | Sc directly for thermal-stability strategy; can reduce Mn/Cr demand for crack suppression / eutectic control | Al-10Ce; binary Al-Ce; Al-3Ce-0.8Ca-1.9Mn; Al92Mn6Ce2 | **Binary Al-Ce:** 222 / 319 / 10.8%; **Al-3Ce-0.8Ca-1.9Mn:** 321 / 429 / 10.9%; **Al92Mn6Ce2:** hardness 180 HV5, compressive stress >1200 MPa | Binary and multicomponent Al-Ce alloys show thermal stability to ~400°C; Al11Ce3 is coarsening-resistant; Ce-containing alloys outperform conventional AM Al at elevated T | Strong: narrow freezing ranges, high melt fluidity, and crack-free LPBF are repeatedly reported; several Ce alloys print without baseplate heating | High: replaces nearly all **Sc** function for eutectic thermal stability and strongly reduces need for **Mn/Cr** crack-management additions in some designs | **Strong for printability + thermal stability, moderate for peak RT strength**: binary Ce trails Scalmalloy substantially, but Ce+Ca+Mn reaches a useful middle ground; best viewed as a scalable, secure high-temperature / crack-resistant route rather than a full Scalmalloy-strength replacement (hesselmann2022effectofprecipitationforming pages 1-3, liu2024reviewoflaser pages 2-4, liu2024reviewoflaser pages 15-17, yakubov2022laserpowderbed pages 124-127, liu2024reviewoflaser pages 23-25, gabrysiak2021developmentandcharacterization pages 1-2, wei2025compositionoptimizationand pages 1-2, wei2025compositionoptimizationand pages 14-15) |
| **B → Sc/Ti grain refinement** | B, especially in Ti-free borides such as CaB6; also LaB6, AlB2-forming routes | Sc and Ti in the **grain-refinement / crack-suppression** role only | 2 wt.% CaB6 in 2024 Al; 0.05-0.5 wt.% LaB6 in AlSi10Mg; BN-derived AlB2 routes | No stand-alone bulk-property benchmark given; **CaB6:** crack-free equiaxed grains ~0.91 ± 0.32 µm; **LaB6:** grain size ~1.6 µm | Benefit is indirect: refined equiaxed grains and stabilized boundaries; not a primary high-temp strengthener by itself | Promising as an additive/nucleant strategy; strong evidence for crack elimination and grain refinement, but mainly in composite / modified-powder studies | Moderate-to-high if it allows elimination or minimization of **Sc** and **Ti** used mainly for nucleation | **Good auxiliary substitute, weak stand-alone substitute**: boron-based refiners can plausibly replace part of the Sc/Ti crack-suppression function, but they do not replicate Scalmalloy-style precipitation strengthening; best used in combination with Zr, Fe, Ce, or Si (minasyan2022laserpowderbedfusion pages 30-32, minasyan2022laserpowderbedfusion pages 10-12, minasyan2022laserpowderbedfusion pages 7-10, yadegari2025aluminumlaseradditive pages 14-15, minasyan2022laserpowderbedfusion pages 32-33) |
| **Ca → Mg / REE** | Ca (domestically abundant, low density), often with Cu, Mn, Zr, or Ce | Part of Mg strengthening/printability role; can reduce Ce/REE need in eutectic AM alloys | Al-10Ca; Al5Ca3Cu1.5Mn0.4Zr; Al-3Ce-0.8Ca-1.9Mn | **Al5Ca3Cu1.5Mn0.4Zr:** YS ~244 MPa; **Al-3Ce-0.8Ca-1.9Mn:** 321 / 429 / 10.9%; **Al-10Ca:** dense crack-free LPBF with preheating | Good thermal stability in Ca-Cu-Mn-Zr alloy: ~7% hardness loss after 100 h at 350-400°C; Ca also depresses eutectic temperature and reduces hot cracking | Good but process-sensitive: Al-10Ca required substrate preheating; Ca evaporation (~6%) is a concern in laser melting | High potential because Ca is abundant, lightweight, and can partly replace **Mg** and some **REE** functionality in eutectic/high-temp alloy design | **Promising but not yet mature**: attractive for lightweight, crack-resistant eutectic systems and as a Ce reducer, but current RT strengths are generally below Scalmalloy and Ca volatility must be managed (preussner2023additivemanufacturingof pages 1-3, letyagin2025characteristicsoflaserremelted pages 1-2, letyagin2025characteristicsoflaserremelted pages 12-13, letyagin2025characteristicsoflaserremelted pages 13-15, wei2025compositionoptimizationand pages 14-15, wei2025compositionoptimizationand pages 15-17, wei2025compositionoptimizationand pages 2-4) |
| **Si-expanded → Mg/Cu/Mn-lean** | Si (partly domestic / mixed refining exposure), optionally small Mg/Cu/Zn additions | Reduces reliance on Mg-, Cu-, and Mn-intensive strengthening strategies; avoids Sc entirely in baseline printable alloys | AlSi10Mg; Si-modified 7075 / Al-Si-Zn-Mg-Cu | **AlSi10Mg:** UTS ~300-460 MPa as-built; stress-relieved example 166 / 280 / 6.4%; **Si-modified 7075:** 315 / 387 / not reported here | Limited above ~250°C: AlSi10Mg UTS ~163 MPa at 250°C and ~34 MPa at 450°C; not a strong high-temp replacement | Excellent: near-eutectic Si gives narrow solidification range (~30°C), high fluidity, high absorptivity, and very low cracking susceptibility | Moderate: strongly reduces demand for scarce grain refiners and can lower Mg/Cu/Mn usage, but Si itself is not fully refinery-secure | **Best low-risk baseline for printability, weak high-temp substitute**: very defensible for crack-free LPBF and moderate RT strength, but cannot replace Ni/Fe/Ce/Zr strategies for sustained service above ~200-250°C (aversa2019newaluminumalloys pages 1-3, aversa2022laserpowderbed pages 1-3, yakubov2022laserpowderbed pages 51-54, aversa2019newaluminumalloys pages 6-8, lehmhus2022hightemperaturemechanicalproperties pages 21-22, lehmhus2022hightemperaturemechanicalproperties pages 1-2) |


*Table: This table compares the six domestically oriented substitution hypotheses for LPBF aluminum alloys, summarizing what import-reliant solutes each option could displace and the expected performance cost. It is useful for prioritizing which substitutions remove the most supply risk while retaining the most defensible mechanical and thermal performance.*

---

## 1. Zr Replacing Sc and Er: Al₃Zr L1₂ Precipitation and Grain Refinement

**Supply-chain rationale.** Sc (~100% NIR) and Er (~100% NIR) are the most import-reliant solutes in the palette. Zr is domestically mined from zircon sands in Florida and Virginia, making it a "mixed" but far more accessible alternative.

**Metallurgical mechanism.** Zr forms metastable L1₂-ordered Al₃Zr precipitates that serve as heterogeneous nucleation sites during solidification, promoting columnar-to-equiaxed grain transition and suppressing hot cracking—the same fundamental role played by Al₃(Sc,Zr) in Scalmalloy® (lu2023microstructuralevaluationand pages 1-2). The Al₃Zr dispersoid is also coarsening-resistant due to Zr's low diffusivity in Al.

**Performance benchmark.** Scalmalloy® (Al-Mg-Sc-Zr) after peak aging at 325 °C/4 h achieves YS of 468–508 MPa and UTS of 517–541 MPa with 8.5–15.9% elongation (mehta2021laserpowderbed pages 7-10, boillatnewport2024heattreatmentpostprocessing pages 9-11, cerri2024mainheattreatments pages 14-16). A reduced-Sc Al-Mg-Sc-Zr alloy by LPBF reached UTS of 536 MPa and 14.8% elongation after aging at 325 °C/2 h (lu2023microstructuralevaluationand pages 1-2). Fully Sc-free Al-Mg-Zr alloys (e.g., Addalloy® 5T) are under active development but publicly available mechanical data are still limited. Constellium's CP1 Al-Fe-Zr alloy uses Al₃Zr as the primary grain refiner and strengthener alongside plate-like Al₁₃Fe₄, demonstrating that Zr can anchor an entire LPBF alloy design without Sc (yadegari2025aluminumlaseradditive pages 14-15).

**Strength of substitution.** The Zr-for-Sc swap is metallurgically the most direct analog because both form coherent L1₂ precipitates. However, Al₃Zr has a higher nucleation barrier and slower precipitation kinetics than Al₃Sc, meaning some strength penalty (~10–20% YS reduction) is likely unless Zr is paired with a second domestic element such as Fe (for intermetallic strengthening) or Ce (for eutectic crack suppression).

**Weakness.** Zr alone cannot fully replicate the extremely fine equiaxed grain zone that Sc produces at melt-pool boundaries, and Zr refining is not fully domestic.

---

## 2. Fe as a Deliberate Strengthener Displacing Ni and Ti for Elevated-Temperature Service

**Supply-chain rationale.** Fe is the only fully domestically secure solute (U.S. is a net exporter). Ni (~48% NIR, one closing U.S. mine) and Ti-sponge (~100% NIR) are the primary elevated-temperature solutes it can displace.

**Metallurgical mechanism.** Fe has extremely low diffusivity in Al (10⁻¹⁰–10⁻¹² cm²/s at 600 °C), which retards intermetallic coarsening and grain growth at elevated temperatures (perezprado2022anal5fe6cralloy pages 1-2). In LPBF, rapid solidification traps Fe in supersaturated solid solution and produces nanoscale Fe-bearing intermetallics (Al₁₃Fe₄, icosahedral i-phase) that are thermally stable to 400 °C (perezprado2022anal5fe6cralloy pages 9-10).

**Performance data.** The Al-5Fe-6Cr alloy by LPBF achieves outstanding high-temperature properties: YS = 400 ± 14 MPa and UTS = 547 ± 24 MPa at room temperature; YS = 344 MPa at 200 °C, 273 MPa at 300 °C, and 179 MPa at 400 °C (perezprado2022anal5fe6cralloy pages 7-9). This substantially outperforms LPBF AlSi10Mg (UTS ~163 MPa at 250 °C, ~34 MPa at 450 °C) (lehmhus2022hightemperaturemechanicalproperties pages 1-2) and is competitive with DuAlumin-3D (Al-9Ce-4Ni-0.5Mn-1Zr), which outperforms benchmark 2618 and A201 above 250 °C (plotkowski2025additivelymanufacturinghightemperature pages 12-17, plotkowski2025additivelymanufacturinghightemperature pages 8-12). The CP1 Al-Fe-Zr alloy combines Fe with Zr for dual precipitation of coherent nano-Al₃Zr and plate-like Al₁₃Fe₄ during direct aging, achieving high strength plus high thermal conductivity (yadegari2025aluminumlaseradditive pages 14-15).

**Strength of substitution.** This is the single strongest supply-chain case: Fe is fully domestic, displaces the most tonnage-relevant import-reliant high-temperature solute (Ni), and the mechanical evidence is robust. An Al-Fe-Zr or Al-Fe-Ce system can plausibly reach the high-temperature performance window currently served by Al-Ce-Ni (DuAlumin-3D) without Ni.

**Weakness.** Room-temperature ductility of Fe-rich Al alloys is low (3.8% for Al-5Fe-6Cr) (perezprado2022anal5fe6cralloy pages 7-9). Most published Al-Fe alloys still use Cr (77% NIR), so a truly domestic-only formulation requires pairing Fe with Zr, Ce, or Si instead of Cr.

---

## 3. Ce (Domestic Light REE) Replacing Sc for Thermal Stability and Mn/Cr for Crack Suppression

**Supply-chain rationale.** Ce is a light rare-earth element domestically mineable at Mountain Pass, CA as a byproduct of bastnasite processing. It can displace Sc (~100% NIR) for thermal stability and reduce the need for Mn (100% NIR) and Cr (77% NIR) for crack management.

**Metallurgical mechanism.** Ce has negligible solubility in Al (~0.01 wt.% at RT) and extremely low diffusivity, forming the thermally stable Al₁₁Ce₃ intermetallic that resists coarsening to at least 400 °C—exceeding the ~350 °C limit of Al₃Sc (yakubov2022laserpowderbed pages 124-127, liu2024reviewoflaser pages 2-4). Near-eutectic Al-Ce compositions have narrow freezing ranges (~30.5 °C for Al-5wt%Ce), providing excellent crack-free LPBF processability without baseplate heating (hesselmann2022effectofprecipitationforming pages 1-3, yakubov2022laserpowderbed pages 29-34). The Al₁₁Ce₃ eutectic phase contributes ~77–193 MPa to yield strength through Orowan looping (liu2024reviewoflaser pages 15-17, liu2024reviewoflaser pages 13-15).

**Performance data.** Binary Al-10Ce by LPBF: YS = 222 MPa, UTS = 319 MPa, EL = 10.8% (hesselmann2022effectofprecipitationforming pages 1-3, liu2024reviewoflaser pages 13-15). With Sc+Zr additions: Al-10Ce-0.4Sc-0.2Zr achieves UTS = 445 MPa, YS = 344 MPa, EL = 10% (liu2024reviewoflaser pages 23-25). The Al₉₂Mn₆Ce₂ metastable alloy by LPBF achieved hardness of 180 HV5, compressive stress exceeding 1200 MPa, and failure strain up to 40% (gabrysiak2021developmentandcharacterization pages 1-2). Al-3Ce-0.8Ca-1.9Mn: YS = 321 MPa, UTS = 429 MPa, EL = 10.9%, with UTS ~250 MPa retained at 300 °C (wei2025compositionoptimizationand pages 1-2, wei2025compositionoptimizationand pages 14-15).

**Strength of substitution.** Ce is a strong substitute for Sc's thermal-stability function and for Mn/Cr's crack-suppression role. The wide LPBF processing window and coarsening-resistant intermetallics are well demonstrated. The Al-Ce-Ca-Mn quaternary system is particularly promising, reaching YS > 320 MPa with good ductility.

**Weakness.** Binary Al-Ce RT strength (222 MPa YS) trails Scalmalloy by >200 MPa. Ce cannot replicate Sc's coherent L1₂ precipitation strengthening; it operates through a fundamentally different (eutectic/Orowan) mechanism. Mountain Pass light-REE supply, while domestic, is still a single-source risk.

---

## 4. Boron (B) as a Grain Refiner / Nucleant Replacing Sc/Zr and Ti

**Supply-chain rationale.** The U.S. is the dominant global borate producer (Boron, CA). Boron is not in the current 15-element palette but should be added. The key Ti-free boride compound is CaB₆, which uses two domestically abundant elements (Ca + B).

**Metallurgical mechanism.** CaB₆ particles function as heterogeneous nucleation sites and Zener-pinning agents at grain boundaries, promoting columnar-to-equiaxed transition and suppressing solidification cracking (minasyan2022laserpowderbedfusion pages 10-12). Addition of 2 wt.% CaB₆ to 2024 Al alloy produced crack-free, fully equiaxed microstructure with grain size of 0.91 ± 0.32 µm by LPBF (minasyan2022laserpowderbedfusion pages 10-12). LaB₆ at 0.05–0.5 wt.% refined AlSi10Mg grains to ~1.6 µm (minasyan2022laserpowderbedfusion pages 10-12). BN additions form AlB₂ and AlN in situ, increasing tensile strength, with a recommended limit of ~1 wt.% (minasyan2022laserpowderbedfusion pages 32-33).

**Performance data.** Boron-based compounds are primarily grain refiners and crack suppressors; they do not provide bulk precipitation strengthening comparable to Al₃Sc. CaB₆ and LaB₆ both improve hardness and tensile strength without sacrificing ductility at their optimal loading levels (minasyan2022laserpowderbedfusion pages 30-32). TiB₂ remains the most effective grain refiner but requires import-reliant Ti (minasyan2022laserpowderbedfusion pages 7-10, minasyan2022laserpowderbedfusion pages 5-7).

**Strength of substitution.** CaB₆ is the most compelling Ti-free, fully domestic grain refiner identified. It directly addresses the crack-suppression sub-function of Sc and Ti. Best used as an additive (≤2 wt.%) combined with other strengthening strategies.

**Weakness.** Boron compounds address only the nucleation/grain-refinement aspect, not the precipitation-strengthening package. This is an auxiliary tool, not a standalone replacement for Sc.

---

## 5. Ca (Calcium) as a Lightweight Addition Replacing Part of Mg and REE

**Supply-chain rationale.** Ca is domestically abundant, inexpensive, and has very low density (1.55 g/cm³), making it attractive for lightweight alloy design to partly replace Mg (~50%+ NIR) and reduce REE demand.

**Metallurgical mechanism.** Ca forms Al₄Ca eutectic phases with lamellar morphology that strengthen through Hall-Petch-like interlamellar spacing reduction under rapid solidification (preussner2023additivemanufacturingof pages 1-3). In Ce-containing alloys, Ca depresses the eutectic precipitation temperature, reducing hot cracking susceptibility while maintaining a stable Al₁₁(Ce,Ca)₃ phase fraction (wei2025compositionoptimizationand pages 15-17, wei2025compositionoptimizationand pages 2-4). Ca additions of 0.5–4 wt.% create fine eutectic structures around 100 nm (wei2025compositionoptimizationand pages 2-4).

**Performance data.** Al-10Ca by LPBF: dense, crack-free samples with Al-Al₄Ca lamellar eutectic; substrate preheating required (preussner2023additivemanufacturingof pages 1-3). Al₅Ca₃Cu₁.₅Mn₀.₄Zr: YS = 244 MPa, hardness 96 HV after laser remelting, with only ~7.5% hardness loss after 100 h at 350–400 °C (compared to ~22% for Zr-free) (letyagin2025characteristicsoflaserremelted pages 1-2, letyagin2025characteristicsoflaserremelted pages 13-15). Al-3Ce-0.8Ca-1.9Mn: YS = 321 MPa, UTS = 429 MPa, EL = 10.9% (wei2025compositionoptimizationand pages 1-2, wei2025compositionoptimizationand pages 15-17). Ca evaporation during laser processing is ~6% under optimal conditions, which must be managed (letyagin2025characteristicsoflaserremelted pages 13-15).

**Strength of substitution.** Ca is a strong complement to Ce in eutectic alloy design for AM, and the Al-Ce-Ca-Mn quaternary demonstrates that Ca can enable competitive mechanical properties while reducing both REE content and Mg dependence. Ca also provides excellent hot-tearing resistance comparable to Al-Si eutectic systems (letyagin2025characteristicsoflaserremelted pages 12-13).

**Weakness.** Ca is not yet in the FLAIME palette and is a relatively early-stage AM alloying element. Ca volatility during LPBF is a process concern. Standalone Al-Ca binary alloys have moderate strength.

---

## 6. Si (Partially Domestic) Expanded as the Primary Strengthener for Mg-Lean / Cu-Lean Compositions

**Supply-chain rationale.** Si is mined domestically but refined partially abroad (mixed security). Expanding Si as the primary strengthener enables Mg-lean, Cu-lean, Mn-lean baselines that avoid the most import-reliant solutes.

**Metallurgical mechanism.** Near-eutectic Si (~10–12 wt.%) provides an extremely narrow solidification range (~30 °C), excellent melt fluidity, high laser absorptivity (~70% for Si particles), and low thermal expansion—all enabling crack-free LPBF processing (aversa2019newaluminumalloys pages 1-3). Strengthening arises from Si supersaturation, Orowan looping by Si precipitates, Hall-Petch refinement of eutectic cells, and dislocation hardening (aversa2019newaluminumalloys pages 1-3, montanari2023additivemanufacturingof pages 16-17). Addition of Si to crack-susceptible alloys like 7075 dramatically reduces cracking and enables production of fully dense LPBF parts (aversa2022laserpowderbed pages 1-3).

**Performance data.** AlSi10Mg by LPBF: as-built UTS = 300–460 MPa depending on parameters and orientation; stress-relieved at 350 °C/2 h: UTS = 280 MPa, YS = 166 MPa, EL = 6.4% (lehmhus2022hightemperaturemechanicalproperties pages 21-22, lehmhus2022hightemperaturemechanicalproperties pages 1-2). High-temperature degradation is severe: UTS drops to ~163 MPa at 250 °C and ~34 MPa at 450 °C (lehmhus2022hightemperaturemechanicalproperties pages 1-2). Si-modified 7075 (Al-Si-Zn-Mg-Cu): YS = 315 MPa, UTS = 387 MPa as-built, with further improvement after aging (aversa2022laserpowderbed pages 1-3, aversa2019newaluminumalloys pages 6-8).

**Strength of substitution.** Si is the most proven, lowest-risk baseline for LPBF printability. Expanding Si content can reduce reliance on Mg, Cu, and Mn as primary strengtheners while maintaining excellent processability.

**Weakness.** Si-based alloys fail above ~250 °C, making them unsuitable as replacements for high-temperature solutes (Ni, Ti, Cr). Si refinement security is mixed. This substitution is complementary to, not a replacement for, the Fe/Ce/Zr strategies.

---

## Additional Domestically Secure Elements Worth Adding to the 15-Element Palette

### Boron (B)
- **Mechanism:** CaB₆ and AlB₂ as heterogeneous nucleants and Zener-pinning grain-boundary stabilizers; replaces Sc/Ti grain-refinement function (minasyan2022laserpowderbedfusion pages 30-32, minasyan2022laserpowderbedfusion pages 10-12).
- **Upper bound:** ~2 wt.% as CaB₆ or ~1 wt.% as BN-derived AlB₂ (minasyan2022laserpowderbedfusion pages 32-33).
- **Displaces:** Sc and Ti in their grain-refinement/crack-suppression role.
- **U.S. supply:** Dominant global borate producer (Boron, CA).

### Calcium (Ca)
- **Mechanism:** Eutectic former (Al₄Ca, Al₁₁(Ce,Ca)₃), hot-cracking suppressant, lightweight density reducer; replaces part of Mg solid-solution and Ce/REE eutectic functions (preussner2023additivemanufacturingof pages 1-3, wei2025compositionoptimizationand pages 2-4).
- **Upper bound:** ~5–10 wt.% for eutectic compositions; 0.5–1 wt.% as a modifier in Ce-based alloys.
- **Displaces:** Part of Mg demand and reduces Ce content needed for crack-free eutectic processing.
- **U.S. supply:** Domestically abundant from limestone and dolomite; no import reliance.
- **Caveat:** ~6% evaporation during LPBF requires process management (letyagin2025characteristicsoflaserremelted pages 13-15).

### Vanadium (V)
- **Mechanism:** Slow-diffusing transition metal forming Al-Fe-V-Si intermetallics with high thermal stability up to 400 °C; mentioned in heat-resistant Al-Fe-V-Si series alloys for aviation (montanari2023additivemanufacturingof pages 17-19, aversa2019newaluminumalloys pages 19-19).
- **Upper bound:** ~1–3 wt.% (typically as part of Al-Fe-V-Si quaternary).
- **Displaces:** Part of Ti and Cr high-temperature dispersoid roles.
- **U.S. supply:** U.S. has significant V resources; NIR is moderate (~15–25%).

---

## Final Ranking of Substitution Opportunities

| Rank | Opportunity | Import-reliance removed (1-5) | Performance retention (1-5) | Combined | Brief rationale | Key evidence |
|---|---|---:|---:|---:|---|---|
| 1 | Fe replacing Ni/Ti for elevated-temperature strength | 5 | 4 | 9 | Fe is the most supply-secure solute in the set and can displace highly import-reliant Ni and part of Ti’s high-temperature role; LPBF Al-5Fe-6Cr retains unusually high strength at 300-400°C, though ductility is limited and some versions still rely on Cr/Zr. | Al-5Fe-6Cr: YS 400 MPa at RT, 273 MPa at 300°C, 179 MPa at 400°C; CP1 Al-Fe-Zr uses Fe + Zr for printable, thermally stable AM alloys (perezprado2022anal5fe6cralloy pages 7-9, perezprado2022anal5fe6cralloy pages 1-2, perezprado2022anal5fe6cralloy pages 9-10, yadegari2025aluminumlaseradditive pages 14-15) |
| 2 | Ce replacing Sc and reducing Mn/Cr demand | 4 | 3 | 7 | Ce can remove dependence on the most import-reliant rare-earth solutes while supporting crack-free eutectic LPBF processing and thermal stability; however, binary Al-Ce trails Scalmalloy-class strength and usually needs help from Ca/Mn/Sc/Zr to reach stronger property levels. | Binary Al-Ce: YS 222 MPa, UTS 319 MPa, EL 10.8%; Al-3Ce-0.8Ca-1.9Mn: YS 321 MPa, UTS 429 MPa (hesselmann2022effectofprecipitationforming pages 1-3, liu2024reviewoflaser pages 13-15, wei2025compositionoptimizationand pages 1-2, wei2025compositionoptimizationand pages 15-17) |
| 3 | Si-expanded baseline replacing some Mg/Cu/Mn dependence | 3 | 4 | 7 | Si is only a mixed-security case, but expanding Si is highly effective for printability and can reduce dependence on Mg-, Cu-, and Mn-heavy strengthening strategies; the main penalty is weak strength retention above about 250°C. | AlSi10Mg LPBF: UTS ~300-460 MPa depending on condition; stress-relieved UTS 280 MPa at RT and 163 MPa at 250°C; Si-modified 7075: YS 315 MPa, UTS 387 MPa (aversa2019newaluminumalloys pages 1-3, aversa2022laserpowderbed pages 1-3, yakubov2022laserpowderbed pages 51-54, lehmhus2022hightemperaturemechanicalproperties pages 21-22, lehmhus2022hightemperaturemechanicalproperties pages 1-2) |
| 4 | Zr replacing Sc/Er | 4 | 3 | 7 | Zr directly targets the highest-risk Sc/Er precipitation and grain-refinement functions and is far more scalable, but Zr is still only a mixed domestic-security case and the open literature here does not yet prove full Scalmalloy-equivalent performance without at least some Sc or another helper solute. | Scalmalloy benchmark after aging: YS ~468-508 MPa, UTS ~517-541 MPa; Zr is known to provide Al3Zr/L1₂ strengthening and crack suppression, but a fully quantified Sc-free parity case was not established in the retrieved evidence (mehta2021laserpowderbed pages 7-10, boillatnewport2024heattreatmentpostprocessing pages 9-11, cerri2024mainheattreatments pages 14-16) |
| 5 | Ca replacing part of Mg/REE function | 3 | 2 | 5 | Ca is abundant, lightweight, and improves eutectic crack resistance, making it attractive for reducing Mg or REE dependence, but current LPBF-relevant Ca alloys are earlier-stage and generally below top-tier strength benchmarks; volatility during melting is an added risk. | Al-10Ca prints crack-free with preheating; Al5Ca3Cu1.5Mn0.4Zr: YS 244 MPa; Al-3Ce-0.8Ca-1.9Mn: YS 321 MPa, UTS 429 MPa; Ca evaporation ~6% reported in laser processing (preussner2023additivemanufacturingof pages 1-3, letyagin2025characteristicsoflaserremelted pages 1-2, letyagin2025characteristicsoflaserremelted pages 12-13, letyagin2025characteristicsoflaserremelted pages 13-15, wei2025compositionoptimizationand pages 15-17) |
| 6 | B-based grain refinement replacing part of Sc/Ti nucleation role | 2 | 2 | 4 | Boron is compelling from a supply perspective and Ti-free borides can suppress cracking, but B mainly replaces only the nucleation/grain-refinement sub-function, not the full precipitation-strengthening package delivered by Sc or Sc+Zr systems. | CaB6 at 2 wt.% gave crack-free equiaxed grains (~0.91 µm); LaB6 at 0.05-0.5 wt.% refined AlSi10Mg to ~1.6 µm grains (minasyan2022laserpowderbedfusion pages 30-32, minasyan2022laserpowderbedfusion pages 10-12, minasyan2022laserpowderbedfusion pages 7-10, yadegari2025aluminumlaseradditive pages 14-15) |
| Special note | Ca + Ce synergy | 4 | 4 | 8 | This combination looks stronger than either substitution alone: Ce supplies eutectic thermal stability while Ca depresses eutectic temperature and reduces hot cracking, enabling a much more competitive middle-ground alloy family without Sc/Ni. | Al-3Ce-0.8Ca-1.9Mn achieved YS 321 MPa, UTS 429 MPa, EL 10.9% with strong LPBF crack-suppression rationale (wei2025compositionoptimizationand pages 1-2, wei2025compositionoptimizationand pages 14-15, wei2025compositionoptimizationand pages 15-17, wei2025compositionoptimizationand pages 2-4) |


*Table: This table ranks the substitution pathways by how much import reliance they can remove and how defensible the retained LPBF alloy performance is. It is useful for prioritizing which supply-secure alloy directions should enter the search space first.*

## Synthesis and Recommendations

The most impactful single substitution is **Fe as a deliberate strengthener** for elevated-temperature applications, directly displacing Ni and Ti using the only fully domestic solute (perezprado2022anal5fe6cralloy pages 7-9, perezprado2022anal5fe6cralloy pages 1-2). The **Ce + Ca synergy** emerges as the second most compelling pathway, combining domestic light-REE thermal stability with Ca's crack-suppression and density benefits to achieve YS > 320 MPa and UTS > 429 MPa with excellent printability (wei2025compositionoptimizationand pages 1-2, wei2025compositionoptimizationand pages 15-17). **Zr replacing Sc/Er** is metallurgically the most direct analog but cannot yet fully match Scalmalloy's strength without helper elements (mehta2021laserpowderbed pages 7-10, cerri2024mainheattreatments pages 14-16). **Si expansion** provides an excellent low-risk printability baseline but is thermally limited (aversa2019newaluminumalloys pages 1-3, lehmhus2022hightemperaturemechanicalproperties pages 1-2). **Boron (as CaB₆)** and **calcium** are recommended additions to the 15-element palette because they provide Ti-free grain refinement and lightweight eutectic functionality, respectively, using fully domestic elements (minasyan2022laserpowderbedfusion pages 10-12, preussner2023additivemanufacturingof pages 1-3).

The optimal strategy for the FLAIME project is to combine these substitutions synergistically: use **Fe + Zr** for high-temperature intermetallic strengthening, **Ce + Ca** for eutectic crack suppression and thermal stability, **Si** for printability baseline, and **CaB₆** as a grain-refining additive—all while minimizing or eliminating Sc, Er, Ni, Ti-sponge, and Cr from the alloy design space.
