<!--
Edison Scientific PRECEDENT task (batch 1)
- Task ID: 9a135f0a-50a2-44c7-b213-1b9dc3a8d2cb
- Submitted: 2026-10-17T05:10:48Z
- Fetched: 2026-10-17T05:42:10Z (status: success)
- Raw trajectory JSON: ../raw/b1-09-precedent-ml-cu-am.json.gz
- Synthesis: ../README.md
-->

Question:

Has anyone used Bayesian optimization, active learning, machine learning, or
any closed-loop or cost-aware multi-fidelity search to design the COMPOSITION
of a copper alloy (Cu-Ni, aluminum bronze / nickel-aluminum bronze, Cu-Sn,
Cu-Mn-Al, CuCrZr or similar) for additive manufacturing or welding, or to
co-optimize powder atomization settings together with alloy composition for
AM? Include process-parameter optimization of copper alloys in DED or LPBF by
BO/ML as a closer analogue, and seawater corrosion as a target property.
Exclude publications by Sterling G. Baird. Give citations with DOIs and say
plainly whether the combination "cost-aware BO over a linked composition ->
powder -> DED -> corrosion pipeline for copper alloys" has precedent.

---

Question: Has anyone used Bayesian optimization, active learning, machine learning, or
any closed-loop or cost-aware multi-fidelity search to design the COMPOSITION
of a copper alloy (Cu-Ni, aluminum bronze / nickel-aluminum bronze, Cu-Sn,
Cu-Mn-Al, CuCrZr or similar) for additive manufacturing or welding, or to
co-optimize powder atomization settings together with alloy composition for
AM? Include process-parameter optimization of copper alloys in DED or LPBF by
BO/ML as a closer analogue, and seawater corrosion as a target property.
Exclude publications by Sterling G. Baird. Give citations with DOIs and say
plainly whether the combination "cost-aware BO over a linked composition ->
powder -> DED -> corrosion pipeline for copper alloys" has precedent.


No. # Copper-alloy design for additive manufacturing: precedent assessment

**Plain answer: I found no published precedent for cost-aware Bayesian optimization (BO) over a linked copper-alloy *composition → powder atomization → directed-energy deposition (DED) → seawater corrosion* pipeline.** There are credible precedents for individual stages and some adjacent two-stage problems, but none identified here jointly selects copper-alloy chemistry, atomization conditions, DED conditions, and marine-corrosion outcomes in a cost-aware, multi-fidelity experimental loop. This is a finding about the literature located, not proof that no such work exists. Publications by Sterling G. Baird are excluded.

## Closest precedents, by what they actually optimize

| Study and DOI | Demonstrated scope | Why it is not the proposed pipeline |
|---|---|---|
| Wang *et al.* (2019), **10.1038/s41524-019-0227-7** | ML inverse design of high-strength, conductive **copper-alloy compositions**; two newly made compositions were checked against property predictions. | Composition design, but not copper AM, atomization, DED, or seawater corrosion. (zhang2022rapiddesignof pages 10-10, khandelwal2024intelligentdesignof pages 1-3) |
| Zhang *et al.* (2021), *Acta Materialia* **215**, 117118, “Machine learning assisted composition effective design for precipitation strengthened copper alloys”; and Zhang *et al.* (2022), **10.1007/s12613-022-2479-3** | The former is identified in the latter’s references and discussion as **Bayesian/ML-guided Cu–Ni–Co–Si composition design**. The separate 2022 paper used BO and 32 experiments to choose **90% secondary cold rolling and aging at 450 °C for 1.25 h** for a low-Co Cu–Ni–Co–Si–X alloy. | These concern conventional precipitation-strengthened copper alloys and deformation/aging, **not** AM. In particular, the 2022 BO decision variables are processing conditions, not the alloy composition. I could not independently verify the 2021 article’s DOI from accessible full text, so do not infer it from its article number. (zhang2022rapiddesignof pages 10-10, zhang2022rapiddesignof pages 1-3, khandelwal2024intelligentdesignof pages 1-3) |
| Khandelwal and Manna (2024), **10.32604/cmc.2024.042752** | CatBoost plus a genetic algorithm and Pareto screening **propose Cu–Cr–Zr–Ni–Si-family chemistries** to balance strength and conductivity; validation is against independent published measurements. | ML composition search, **not experimental closed-loop BO**, and not AM, powder manufacture, or chloride-corrosion optimization. (khandelwal2024intelligentdesignof pages 23-25, khandelwal2024intelligentdesignof pages 1-3) |
| Rankouhi *et al.* (2021), **10.1016/j.addma.2021.101836** | **ML-assisted selection of selective-laser-melting parameters for compositionally graded 316L–Cu parts.** | The composition gradient is a steel/copper multimaterial build, not BO design of a Cu–Ni or bronze alloy’s elemental recipe; no linked atomization or corrosion search is established. (laurikainen2025laserpowderbed pages 22-23, laurikainen2025laserpowderbed pages 18-22) |
| Tamura *et al.* (2021), **10.1016/j.matdes.2020.109290** | Experimental BO for **gas atomization of a fixed Ni–Co superalloy**, choosing melt temperature and gas pressure. Three optimization cycles yielded **77.85% powder below 53 µm** and approximately **72% lower powder-manufacturing cost** than a commercial comparator. | This is a particularly close **powder-stage and economic analogue**, but the material is not a copper alloy; chemistry was not a BO variable, and the study did not optimize DED or corrosion. Lower manufacturing cost is an *outcome*, not evidence of cost-aware multi-fidelity acquisition over the proposed pipeline. (tamura2021machinelearningdrivenoptimization pages 26-31, tamura2021machinelearningdrivenoptimization pages 1-5, tamura2021machinelearningdrivenoptimization pages 5-9, tamura2021machinelearningdrivenoptimization pages 9-14) |
| Pandiyan *et al.* (2026), **10.1007/s40964-026-01854-x** | ML classification of **local 316L–CuCrZr fractions** during LPBF from acoustic and optical process signals. | An *in-situ composition sensor*, not inverse alloy-composition design or experimental BO. (pandiyan2026learningcompositionsensitivesignatures pages 1-2) |

**Copper DED/LPBF parameter-optimization qualification.** Copper process-search precedents should not automatically be described as BO: a Cu–15Sn LPBF study varied laser power, speed, and hatch spacing using **response-surface methodology and ANOVA**, with **fixed, prealloyed gas-atomized bronze powder**; Fang *et al.* reported CuCrZr LPBF parameter optimization, DOI **10.3390/met11091410**. These support copper printability/process tuning, but the verified Cu–15Sn method is conventional statistical design, not sequential BO. A 2024 copper-AM review, DOI **10.3390/jmmp8020054**, also surveys Cu–Ni, bronzes, CuCrZr, and NAB across AM routes. I could verify Rankouhi’s multimaterial LPBF study as an ML **parameter-selection** analogue, but not a copper-alloy DED experiment that closes a BO loop over alloy composition and deposition settings. (fang2021preparationofcucrzr pages 1-4, laurikainen2025laserpowderbed pages 18-22, laurikainen2025laserpowderbed pages 22-23, nemani2024advancementsinadditive pages 26-28, nemani2024advancementsinadditive pages 60-62)

## Marine corrosion is a real downstream objective, but not a linked BO objective

Huo *et al.* (2025), **10.3390/ma18102205**, compared **fixed-composition nickel–aluminum bronze** deposited by cold-metal-transfer wire-arc AM at different heat inputs. In **laboratory 3.5 wt% NaCl**, raising heat input from **243.8 to 644.7 J/mm** increased corrosion current density from **2.56 ± 0.04 to 7.52 ± 0.07 µA/cm²**. This connects an AM/welding setting to a marine-*proxy* corrosion measurement without ML composition search. Zhang *et al.* (2026), **10.1007/s44500-026-00016-x**, varied Ti microalloying of wire-arc-AM NAB and measured corrosion in **3.5 wt% NaCl**; 0.1 wt% Ti reduced corrosion current density by **15.6%** relative to the unmodified deposit. That is unusually close **composition–AM–corrosion experimental evidence**, but its tested Ti levels were not selected by a demonstrated BO/active-learning loop, and there is no powder stage. (huo2025modulatingheatinput pages 1-2, zhang2026effectoflowlevel pages 4-8, zhang2026effectoflowlevel pages 1-2, huo2025modulatingheatinput pages 4-5)

For powder-bed bronze, Zeng *et al.* (2020), **10.1016/j.addma.2020.101411**, evaluated LPBF Cu–10Sn before and after annealing: a review reports improved immersion/electrochemical corrosion behavior after annealing in **3.5 wt% NaCl**, not optimization of alloy chemistry. For an actual seawater-related Cu–Ni question, Qian *et al.* (2025), **10.1007/s42114-024-01174-0**, tested galvanically coupled **B10/B30 copper–nickel pipes in static seawater**; their decision was pipe-material arrangement, not AM alloy design. Importantly, **3–3.5% NaCl is an artificial chloride proxy, not necessarily natural seawater**, and should be labeled accordingly. (qian2025corrosivestudyof pages 1-2, nemani2024advancementsinadditive pages 50-53, nemani2024advancementsinadditive pages 53-56, nemani2024advancementsinadditive pages 110-112)

**Verdict:** Copper compositional ML/BO, BO-controlled *non-copper* powder atomization, ML-guided copper-containing LPBF parameters, and chloride testing of AM copper alloys all have separate precedents. The **cost-aware, multi-fidelity, closed-loop integration of copper-alloy composition with powder atomization, DED fabrication, and seawater-corrosion feedback was not identified**. Claim novelty for that *specific integration*, not for BO alloy design, copper AM, or corrosion testing individually. (zhang2022rapiddesignof pages 1-3, tamura2021machinelearningdrivenoptimization pages 26-31, laurikainen2025laserpowderbed pages 22-23, nemani2024advancementsinadditive pages 26-28, zhang2026effectoflowlevel pages 1-2, huo2025modulatingheatinput pages 4-5)

References

1. (zhang2022rapiddesignof pages 10-10): Hongtao Zhang, Huadong Fu, Yuheng Shen, and Jian-Xin Xie. Rapid design of secondary deformation-aging parameters for ultra-low co content cu-ni-co-si-x alloy via bayesian optimization machine learning. International Journal of Minerals, Metallurgy and Materials, 29:1197-1205, May 2022. URL: https://doi.org/10.1007/s12613-022-2479-3, doi:10.1007/s12613-022-2479-3. This article has 48 citations.

2. (khandelwal2024intelligentdesignof pages 1-3): Parth Khandelwal and Indranil Manna. Intelligent design of high strength and high conductivity copper alloys using machine learning assisted by genetic algorithm. Computers, Materials &amp; Continua, 79:1727-1755, Jan 2024. URL: https://doi.org/10.32604/cmc.2024.042752, doi:10.32604/cmc.2024.042752. This article has 16 citations and is from a peer-reviewed journal.

3. (zhang2022rapiddesignof pages 1-3): Hongtao Zhang, Huadong Fu, Yuheng Shen, and Jian-Xin Xie. Rapid design of secondary deformation-aging parameters for ultra-low co content cu-ni-co-si-x alloy via bayesian optimization machine learning. International Journal of Minerals, Metallurgy and Materials, 29:1197-1205, May 2022. URL: https://doi.org/10.1007/s12613-022-2479-3, doi:10.1007/s12613-022-2479-3. This article has 48 citations.

4. (khandelwal2024intelligentdesignof pages 23-25): Parth Khandelwal and Indranil Manna. Intelligent design of high strength and high conductivity copper alloys using machine learning assisted by genetic algorithm. Computers, Materials &amp; Continua, 79:1727-1755, Jan 2024. URL: https://doi.org/10.32604/cmc.2024.042752, doi:10.32604/cmc.2024.042752. This article has 16 citations and is from a peer-reviewed journal.

5. (laurikainen2025laserpowderbed pages 22-23): K Laurikainen. Laser powder bed fusion of copper alloy-based multi-materials: manufacturing and process optimization: a literature review. Unknown journal, 2025.

6. (laurikainen2025laserpowderbed pages 18-22): K Laurikainen. Laser powder bed fusion of copper alloy-based multi-materials: manufacturing and process optimization: a literature review. Unknown journal, 2025.

7. (tamura2021machinelearningdrivenoptimization pages 26-31): Ryo Tamura, Toshio Osada, Kazumi Minagawa, Takuma Kohata, Masashi Hirosawa, Koji Tsuda, and Kyoko Kawagishi. Machine learning-driven optimization in powder manufacturing of ni-co based superalloy. Materials &amp; Design, 198:109290, Jan 2021. URL: https://doi.org/10.1016/j.matdes.2020.109290, doi:10.1016/j.matdes.2020.109290. This article has 101 citations and is from a highest quality peer-reviewed journal.

8. (tamura2021machinelearningdrivenoptimization pages 1-5): Ryo Tamura, Toshio Osada, Kazumi Minagawa, Takuma Kohata, Masashi Hirosawa, Koji Tsuda, and Kyoko Kawagishi. Machine learning-driven optimization in powder manufacturing of ni-co based superalloy. Materials &amp; Design, 198:109290, Jan 2021. URL: https://doi.org/10.1016/j.matdes.2020.109290, doi:10.1016/j.matdes.2020.109290. This article has 101 citations and is from a highest quality peer-reviewed journal.

9. (tamura2021machinelearningdrivenoptimization pages 5-9): Ryo Tamura, Toshio Osada, Kazumi Minagawa, Takuma Kohata, Masashi Hirosawa, Koji Tsuda, and Kyoko Kawagishi. Machine learning-driven optimization in powder manufacturing of ni-co based superalloy. Materials &amp; Design, 198:109290, Jan 2021. URL: https://doi.org/10.1016/j.matdes.2020.109290, doi:10.1016/j.matdes.2020.109290. This article has 101 citations and is from a highest quality peer-reviewed journal.

10. (tamura2021machinelearningdrivenoptimization pages 9-14): Ryo Tamura, Toshio Osada, Kazumi Minagawa, Takuma Kohata, Masashi Hirosawa, Koji Tsuda, and Kyoko Kawagishi. Machine learning-driven optimization in powder manufacturing of ni-co based superalloy. Materials &amp; Design, 198:109290, Jan 2021. URL: https://doi.org/10.1016/j.matdes.2020.109290, doi:10.1016/j.matdes.2020.109290. This article has 101 citations and is from a highest quality peer-reviewed journal.

11. (pandiyan2026learningcompositionsensitivesignatures pages 1-2): Vigneashwara Pandiyan, Antonios Baganis, Antti Salminen, and Christian Leinenbach. Learning composition-sensitive signatures in multi-material pbf-lb: a lightweight, modality-aware, explainable graph-attention sensor fusion framework for in-situ monitoring of graded 316l–cucrzr alloys. Progress in Additive Manufacturing, 11:9409-9437, Jul 2026. URL: https://doi.org/10.1007/s40964-026-01854-x, doi:10.1007/s40964-026-01854-x. This article has 0 citations and is from a peer-reviewed journal.

12. (fang2021preparationofcucrzr pages 1-4): Xiangyao Fang, Weisheng Xia, Qingsong Wei, Yiping Wu, Weiwen Lv, and Wentao Guo. Preparation of cu-cr-zr alloy by laser powder bed fusion: parameter optimization, microstructure, mechanical and thermal properties for microelectronic applications. Metals, 11:1410, Sep 2021. URL: https://doi.org/10.3390/met11091410, doi:10.3390/met11091410. This article has 39 citations.

13. (nemani2024advancementsinadditive pages 26-28): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

14. (nemani2024advancementsinadditive pages 60-62): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

15. (huo2025modulatingheatinput pages 1-2): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

16. (zhang2026effectoflowlevel pages 4-8): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

17. (zhang2026effectoflowlevel pages 1-2): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

18. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

19. (qian2025corrosivestudyof pages 1-2): Feng Qian, Xvhui Liu, Rui Cui, Kai Wang, Chao Wang, Xiong Bao, Dongsheng Dong, Mengni Zhou, Zunhua Zhang, Xiaofeng Guo, and Jie Wang. Corrosive study of b10/b30 copper-nickel alloys coupled pipeline in static seawater. Advanced Composites and Hybrid Materials, Jan 2025. URL: https://doi.org/10.1007/s42114-024-01174-0, doi:10.1007/s42114-024-01174-0. This article has 12 citations and is from a peer-reviewed journal.

20. (nemani2024advancementsinadditive pages 50-53): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

21. (nemani2024advancementsinadditive pages 53-56): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

22. (nemani2024advancementsinadditive pages 110-112): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.
