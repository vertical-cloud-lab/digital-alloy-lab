<!--
Edison Scientific PRECEDENT task (batch 5)
- Task ID: 5e00978c-82dc-449f-9c58-9057ee6cb816
- Submitted: 2026-10-17T06:20:03Z
- Fetched: 2026-10-17T06:51:54Z (status: success)
- Raw trajectory JSON: ../raw/b5-01-precedent-final-novelty.json.gz
- Synthesis: ../README.md
-->

Question:

Check this claim for counterexamples published up to October 2026: "No
published study has (a) designed a new copper alloy composition for
blown-powder laser directed energy deposition with a search that evaluates
CALPHAD along a modeled DED thermal history, (b) made each candidate as
pre-alloyed powder in-house, and (c) tested the as-deposited alloy against
wrought 70-30 copper-nickel (C71500) in seawater, including deposits on
cast nickel-aluminum bronze and wrought copper-nickel." Consider each part
separately and in combination, include Jia et al. 2026 (Addit. Manuf. 127,
105291), Uhlmann et al. 2024, Cabrioli et al. 2025, Bhattacharya et al.
2011, Li et al. 2021, and any 2025-2026 work, and propose the narrowest
accurate wording. Exclude publications by Sterling G. Baird.

---

Question: Check this claim for counterexamples published up to October 2026: "No
published study has (a) designed a new copper alloy composition for
blown-powder laser directed energy deposition with a search that evaluates
CALPHAD along a modeled DED thermal history, (b) made each candidate as
pre-alloyed powder in-house, and (c) tested the as-deposited alloy against
wrought 70-30 copper-nickel (C71500) in seawater, including deposits on
cast nickel-aluminum bronze and wrought copper-nickel." Consider each part
separately and in combination, include Jia et al. 2026 (Addit. Manuf. 127,
105291), Uhlmann et al. 2024, Cabrioli et al. 2025, Bhattacharya et al.
2011, Li et al. 2021, and any 2025-2026 work, and propose the narrowest
accurate wording. Exclude publications by Sterling G. Baird.


No. ## Assessment through 17 October 2026

**The absolute claim is not established.** The accessible literature contains substantial precedents for parts of the proposed workflow, but I found no *verified* paper satisfying **(a), (b), and (c) together**. Crucially, the primary texts of several studies specified in the question—including Jia et al. (2026), *Additive Manufacturing* **127**, 105291—were not retrievable in this search. Failure to retrieve them is not evidence that they lack the claimed methods. This assessment excludes publications by Sterling G. Baird.

**(a) Composition design and thermodynamic modelling.** The broad assertion that copper-containing laser DED compositions have not been guided by CALPHAD is false. Balkan and colleagues reported thermodynamic calculations alongside DED of a CuSn10–Inconel 718 gradient; Yang and colleagues used a CALPHAD-based hybrid Scheil–equilibrium criterion to select a crack-resistant SS316L–Ni–Monel 400 DED gradient. Neither accessible account establishes the *more specific* requirement of searching new copper-alloy compositions by evaluating CALPHAD **along a modelled DED thermal history**. A 2026 review also describes a laser-DED Cu–Al composition series assessed for corrosion, but does not establish that specific search method. (balkan2021directedenergydeposition pages 1-2, yang2024circumventingcrackingin pages 1-5, canacoo2026laseradditivemanufacturing pages 12-14)

**(b) Candidate-specific feedstock.** The distinction is *pre-alloying each candidate as a separate, in-house powder*, not merely mixing feedstocks to obtain different deposited compositions. The Cu–Al laser-DED series described in the 2026 review used **blended CuNiSiCr and Al–Mg–Si powders**; the cited DED gradient studies likewise do not establish the stipulated candidate-by-candidate powder production. This is an absence of verification in these sources, **not proof that no other study did it**. (canacoo2026laseradditivemanufacturing pages 12-14, canacoo2026laseradditivemanufacturing media b19e8f74, yang2024circumventingcrackingin pages 1-5, balkan2021directedenergydeposition pages 1-2)

**(c) Marine benchmark and substrates.** Earlier additive-manufacturing studies did examine Cu–Ni corrosion: a 2024 review describes laser-powder-bed-fused Cu–Ni exposure to 3% NaCl and reports that a wire-arc Cu–Ni electrochemical study **had no reference sample**. The 2026 Cu–Al laser-DED series reported corrosion performance comparable to **cast nickel-aluminium bronze (NAB)** for its 12 wt% Al alloy. *Comparing with cast NAB is not depositing on cast NAB.* None of those accessible reports establishes the entire stipulated experiment: **as-deposited** alloy tested in seawater against **wrought C71500**, with deposits made on **both cast NAB and wrought Cu–Ni**. An October 2026 paper also reports improved corrosion behaviour from Ti microalloying of *wire-arc* NAB, not that laser-DED benchmark. (nemani2024advancementsinadditive pages 26-28, nemani2024advancementsinadditive pages 41-43, canacoo2026laseradditivemanufacturing pages 12-14, canacoo2026laseradditivemanufacturing media b19e8f74, zhang2026effectoflowlevel pages 1-2)

The following matrix distinguishes verified partial precedents from papers that could not be assessed directly. (yang2024circumventingcrackingin pages 1-5, balkan2021directedenergydeposition pages 1-2, canacoo2026laseradditivemanufacturing pages 12-14, zhang2026effectoflowlevel pages 1-2)

| Source | (a) New Cu-alloy composition searched using CALPHAD along modeled DED thermal history | (b) Every candidate made in-house as pre-alloyed powder | (c) As-deposited seawater comparison with wrought C71500, including deposits on cast NAB and wrought Cu–Ni | Evidence grade / relevance to conjunction |
|---|---|---|---|---|
| Balkan et al. (2021), CuSn10–IN718 DED FGM | **Partial only.** Used thermodynamic/CALPHAD and non-equilibrium solidification calculations to assess phases in a DED gradient; it developed a gradient/process rather than searching new marine Cu-alloy compositions along a modeled DED thermal history. (balkan2021thermochemicalmodellingand pages 1-9, balkan2021thermochemicalmodellingand pages 9-13, balkan2021directedenergydeposition pages 1-2) | **No evidence.** Commercial CuSn10 and IN718 feedstocks/mixtures, not separately pre-alloyed in-house powder for every searched candidate. | **No.** No required seawater/C71500/substrate comparison. | **Strong partial precedent for DED + CALPHAD; not a counterexample to the conjunction.** |
| Yang et al. (2024), SS316L–Ni–Monel 400 FGM | **Partial only.** CALPHAD-based hybrid Scheil–equilibrium calculations guided a DED compositional path and cracking criterion, but this was dissimilar-alloy gradient design—not a search for a new copper-alloy composition evaluated along a modeled DED thermal history. (yang2024circumventingcrackingin pages 1-5) | **No evidence.** Multiple feedstocks were blended during DED, not candidate-specific in-house pre-alloyed powders. | **No.** No required marine benchmark or substrate matrix. | **Strong counterexample to any broad claim that DED copper-containing composition design had never used CALPHAD; not to narrow (a), (b), or (c).** |
| Nemani et al. (2024), review of Cu-alloy AM | **No full match.** It documents Cu–Ni AM and corrosion work, but not the specified CALPHAD/thermal-history composition-search workflow. The review says L-PBF Cu–Ni corrosion literature was very limited. (nemani2024advancementsinadditive pages 21-26, nemani2024advancementsinadditive pages 26-28) | **No match shown.** Reviewed studies used various powders; the cited evidence does not establish candidate-by-candidate in-house pre-alloying. | **Partial precedents only.** L-PBF Cu–Ni was exposed to 3% NaCl, while reviewed WAAM Cu–Ni PDP/EIS work had **no reference sample**. Neither establishes the complete C71500-plus-two-substrate comparison. (nemani2024advancementsinadditive pages 41-43, nemani2024advancementsinadditive pages 26-28) | **Useful landscape evidence; supports narrowing rather than an absolute claim about individual elements.** |
| Yao et al., summarized by Canacoo et al. (Sept. 2026), Cu–Al LDED series | **Partial composition series, not evidenced as CALPHAD thermal-history search.** Cu–Al alloys containing 6–12 wt% Al were deposited by LDED. (canacoo2026laseradditivemanufacturing pages 12-14, canacoo2026laseradditivemanufacturing media b19e8f74) | **No.** Used **blended CuNi₂SiCr and Al–Mg–Si powders**, not one in-house pre-alloyed powder per candidate. (canacoo2026laseradditivemanufacturing pages 12-14, canacoo2026laseradditivemanufacturing media b19e8f74) | **Partial but distinct.** Electrochemical/immersion performance improved with Al, and the 12 wt% Al alloy was reported comparable to **cast NAB**. That is not evidence of seawater testing against wrought C71500 or deposits on both cast NAB and wrought Cu–Ni. (canacoo2026laseradditivemanufacturing pages 12-14, canacoo2026laseradditivemanufacturing media b19e8f74) | **Important 2026 partial precedent; not a full counterexample. Do not conflate “comparable to cast NAB” with deposition on cast NAB.** |
| Zhang et al. (Oct. 2026), Ti-microalloyed WAAM NAB | **No.** Experimental Ti microalloying of NAB by wire-arc AM, not blown-powder laser DED or a CALPHAD/DED-thermal-history search. (zhang2026effectoflowlevel pages 1-2) | **No.** Wire-fed WAAM; the evidence does not show candidate-specific in-house pre-alloyed powder. | **No required comparison.** Corrosion improved at 0.1 wt% Ti, but no evidenced C71500 benchmark or both specified deposition substrates. (zhang2026effectoflowlevel pages 1-2) | **2026 composition/corrosion precedent outside the claimed process and comparison design.** |
| Jia et al. (2026), *Additive Manufacturing* 127, 105291 | **Unverified from available primary text.** | **Unverified.** | **Unverified.** | **Must be checked directly before making a categorical novelty claim; no conclusion should be inferred from failed retrieval.** |
| Uhlmann et al. (2024) | **Unverified from available primary text.** | **Unverified.** | **Unverified.** | **Not usable as affirmative or negative evidence without bibliographic disambiguation and primary-text inspection.** |
| Cabrioli et al. (2025) | **Unverified from available primary text.** | **Unverified.** | **Unverified.** | **Not usable as affirmative or negative evidence without primary-text inspection.** |
| Bhattacharya et al. (2011), Cu–30Ni direct metal deposition | **No evidenced match to (a).** The bibliographic record establishes DMD Cu–30Ni microstructure/mechanical/corrosion evaluation, but the primary text was unavailable here. | **Unverified.** | **Potentially relevant older corrosion precedent, but the exact electrolyte, comparator, and substrate details remain unverified here.** | **Do not claim it satisfies or fails narrow (c) until the paper is directly checked.** |
| Li et al. (2021) | **Unverified from available primary text.** | **Unverified.** | **Unverified.** | **Not usable as a counterexample assessment without identifying and inspecting the intended publication.** |
| **Combined assessment from evidenced sources** | **Partial precedents exist for DED + CALPHAD and for LDED copper-alloy composition/corrosion studies.** | **No evidenced source demonstrates every candidate being produced as in-house pre-alloyed powder.** | **No evidenced source demonstrates the complete as-deposited seawater comparison against wrought C71500 on both cast NAB and wrought Cu–Ni substrates.** | **No full counterexample is demonstrated by the inspected evidence, but the named unverified papers prevent a defensible universal “no published study” conclusion.** |


*Table: This matrix separates partial precedents from the claim’s full conjunction and flags named studies whose primary texts were unavailable. It also prevents conflating seawater testing, comparison with cast NAB, and deposition onto NAB.*

**Named-study limitation.** Bhattacharya et al. (2011), *Journal of Alloys and Compounds* **509**, 6364–6373, is an especially important earlier **Cu–30Ni direct-metal-deposition corrosion** precedent; its title and bibliographic record alone do not resolve its electrolyte, comparator, powder provenance or deposition substrates. I could not inspect that primary paper, or reliably inspect or disambiguate the intended Uhlmann et al. (2024), Cabrioli et al. (2025), and Li et al. (2021) papers. Most importantly, **Jia et al. (2026) cannot be scored yes or no on any of (a)–(c) from the retrieved evidence**. Thus a definitive claim covering all publications through October 2026 would overstate what was checked. (nemani2024advancementsinadditive pages 21-26, nemani2024advancementsinadditive pages 26-28)

**Narrowest supportable wording:** “In the non-Baird publications whose methods we could verify through **17 October 2026**, we identified precedents for thermodynamically guided copper-containing DED, for additive-manufactured Cu–Ni corrosion testing, and for laser-DED copper-alloy composition series with corrosion comparisons. **We did not verify a single study combining** a new copper-alloy composition search evaluating CALPHAD along a modelled blown-powder laser-DED thermal history, separately in-house-pre-alloyed powder for every candidate, and as-deposited seawater testing against wrought C71500 for deposits on both cast nickel-aluminium bronze and wrought copper–nickel. **This is a qualified finding, not a demonstrated ‘no published study’ result; Jia et al. (2026) and the other inaccessible named papers require direct checking.**” (yang2024circumventingcrackingin pages 1-5, balkan2021directedenergydeposition pages 1-2, nemani2024advancementsinadditive pages 26-28, canacoo2026laseradditivemanufacturing pages 12-14)

References

1. (balkan2021directedenergydeposition pages 1-2): Muhammed Enes Balkan, Eda Aydoğan, Murat Işık, Bora Derin, and Bahattin Koç. Directed energy deposition process development for functionally gradient copper-inconel 718 materials. Journal of Additive Manufacturing Technologies, Dec 2021. URL: https://doi.org/10.18416/jamtech.2111581, doi:10.18416/jamtech.2111581. This article has 12 citations.

2. (yang2024circumventingcrackingin pages 1-5): Zhening Yang, Alexander Richter, Hui Sun, Zi-Kui Liu, and Allison M. Beese. Circumventing cracking in grading 316l stainless steel to monel400 through compositional modifications in directed energy deposition. Dec 2024. URL: https://doi.org/10.1016/j.mtla.2024.102283, doi:10.1016/j.mtla.2024.102283. This article has 10 citations and is from a peer-reviewed journal.

3. (canacoo2026laseradditivemanufacturing pages 12-14): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

4. (canacoo2026laseradditivemanufacturing media b19e8f74): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

5. (nemani2024advancementsinadditive pages 26-28): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

6. (nemani2024advancementsinadditive pages 41-43): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

7. (zhang2026effectoflowlevel pages 1-2): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

8. (balkan2021thermochemicalmodellingand pages 1-9): ME Balkan. Thermochemical modelling and directed energy deposition of copper-nickel functionally gradient materials. Unknown journal, 2021.

9. (balkan2021thermochemicalmodellingand pages 9-13): ME Balkan. Thermochemical modelling and directed energy deposition of copper-nickel functionally gradient materials. Unknown journal, 2021.

10. (nemani2024advancementsinadditive pages 21-26): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.
