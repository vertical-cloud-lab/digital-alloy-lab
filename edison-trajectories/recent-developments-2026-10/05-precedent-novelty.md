<!--
Edison Scientific PRECEDENT task
- Task ID: 4e6cabdf-216c-4c24-8310-161e896aa58a
- Submitted: 2026-10-06T19:03:23Z
- Fetched: 2026-10-06T19:34:48Z (status: success)
- Raw trajectory JSON: raw/05-precedent-novelty.json
- Companion to: README.md (synthesis), ../../afosr-yip-white-paper/
-->

Question:

Has anyone applied cost-aware Bayesian optimization of function networks
(BOFN) with partial evaluations - i.e., an optimizer that models a multi-stage
pipeline as a directed acyclic graph of surrogate models and chooses which
intermediate node (e.g., a cheap thermodynamic simulation or proxy experiment
vs. an expensive final property measurement) to evaluate next based on
information gained per unit cost - to an additive manufacturing pipeline for
metal alloys (composition -> powder atomization -> laser powder bed fusion ->
microstructure -> mechanical property)? Consider both journal papers and
preprints, with emphasis on anything from 2025-2026, and include close
analogues (multi-stage / cascade BO, multi-fidelity BO with intermediate
process outputs, process-structure-property chained Gaussian processes) in
metals AM, alloy design, or other materials-manufacturing pipelines. Exclude
publications by Sterling G. Baird. State clearly whether the claim "applied
for the first time to a complex additive manufacturing pipeline for alloys"
is still defensible, and suggest a safer wording if not.

---

Question: Has anyone applied cost-aware Bayesian optimization of function networks
(BOFN) with partial evaluations - i.e., an optimizer that models a multi-stage
pipeline as a directed acyclic graph of surrogate models and chooses which
intermediate node (e.g., a cheap thermodynamic simulation or proxy experiment
vs. an expensive final property measurement) to evaluate next based on
information gained per unit cost - to an additive manufacturing pipeline for
metal alloys (composition -> powder atomization -> laser powder bed fusion ->
microstructure -> mechanical property)? Consider both journal papers and
preprints, with emphasis on anything from 2025-2026, and include close
analogues (multi-stage / cascade BO, multi-fidelity BO with intermediate
process outputs, process-structure-property chained Gaussian processes) in
metals AM, alloy design, or other materials-manufacturing pipelines. Exclude
publications by Sterling G. Baird. State clearly whether the claim "applied
for the first time to a complex additive manufacturing pipeline for alloys"
is still defensible, and suggest a safer wording if not.


No. ## Assessment (literature searched through 6 October 2026)

**I did not find a non–Sterling G. Baird journal paper or preprint demonstrating the exact combination specified:** a cost-aware Bayesian optimizer that represents the *composition → powder atomization → laser powder-bed fusion (LPBF) → microstructure → mechanical-property* route as a directed network of stage surrogates and adaptively decides whether to obtain another intermediate result or pay for a downstream measurement. This is a finding about the literature located, **not proof that no such publication exists**. Crucially, both the optimization method and nearly the entire physical alloy pipeline have substantial prior art; they should not be claimed as independently new. (buathong2023bayesianoptimizationof pages 3-4, taherimousavi2024additivelymanufacturablehighstrength pages 9-12, taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 9-12)

### Closest precedents and what they actually demonstrate

| Work | Demonstrated contribution | Boundary relative to the proposed claim |
|---|---|---|
| **Astudillo and Frazier, *Bayesian Optimization of Function Networks* (2021).** | Models a directed network with separate Gaussian processes (GPs) and uses expected improvement informed by intermediate outputs. | The original general-network algorithm evaluates the **whole network** at each iteration; observing internal outputs is not itself a partial-evaluation policy. (astudillo2021bayesianoptimizationof pages 1-2, torresi2026multistagebayesianoptimisation pages 2-3) |
| **Buathong *et al.*, *Bayesian Optimization of Function Networks with Partial Evaluations* (2023 preprint; ICML 2024).** | **Direct methodological precedent.** Its p-KGFN policy chooses a node and feasible input using expected improvement in the best posterior-mean solution **divided by that node’s evaluation cost**. In its principal setting, a downstream query uses *previously produced parent outputs*, so upstream dependencies are respected. | Its manufacturing example, **Manu-GP**, is a synthetic network sampled from GP priors, not an alloy-atomization/LPBF campaign; other demonstrations include molecular FreeSolv and pharmaceutical-product examples. Do not claim to invent cost-aware BOFN with partial evaluations. (buathong2023bayesianoptimizationof pages 3-4, buathong2023bayesianoptimizationof pages 7-8, buathong2023bayesianoptimizationof pages 8-9, buathong2506fastbayesianoptimization pages 9-11) |
| **Buathong and Frazier, *Fast Bayesian Optimization of Function Networks with Partial Evaluations* (2025 preprint).** | Accelerates node-level, cost-aware p-KGFN selection, reporting up to **16.03-fold** lower acquisition runtime. | Its **Manu** case remains a simulated manufacturing network. Unlike the earlier paper’s main feasible-input setting, this fast variant assumes a node can be queried at a feasible input **without first obtaining its parent outputs**; the authors identify physically constrained dependencies as future work. (buathong2506fastbayesianoptimization pages 8-9, buathong2506fastbayesianoptimization pages 9-11) |
| **Torresi and Friederich, *Multi-stage Bayesian optimisation for dynamic decision-making in self-driving labs* (*Digital Discovery*, 2026).** | A particularly close **cascade-GP and partial-workflow** analogue: an inventory preserves intermediate samples; nested expected improvement chooses between starting samples and advancing existing ones. The framework permits stage-cost weighting. It is tested on synthetic cascades and retrospective molecular-property datasets, including simulated-versus-experimental hydration free energy. | **Not metal AM.** Moreover, although heterogeneous costs are tested, the authors report using **uniform stage costs in their principal experiments** because explicit cost weighting performed worse; their heterogeneous-cost benefit can arise from resumable sampling without putting cost into the acquisition. It should not be described unqualifiedly as an empirical demonstration of information-per-unit-cost selection in alloys. (torresi2026multistagebayesianoptimisation pages 5-6, torresi2026multistagebayesianoptimisation pages 6-7, torresi2026multistagebayesianoptimisation pages 7-10, torresi2026multistagebayesianoptimisation pages 10-12) |
| **Taheri-Mousavi *et al.*, 2024 preprint and *Advanced Materials* article (2026), DOI 10.1002/adma.202509507.** | **Closest physical-pipeline precedent.** CALPHAD/ICME-informed **composition BO** led to a custom Al alloy; the authors screened compositions and printability, **ultrasonically atomized powder**, optimized LPBF settings, examined microstructure, and performed hardness and tensile testing. The journal abstract reports **395 MPa** tensile strength after aging. | Its BO selects alloy compositions against simulated design metrics; subsequent screening, powder production, printing and testing are **not reported as competing costed nodes selected by a BOFN partial-evaluation acquisition**. Thus the *integrated composition-to-property AM route* has precedent, even if the proposed **adaptive stage-selection rule applied across it** has not been located. (taherimousavi2024additivelymanufacturablehighstrength pages 7-9, taherimousavi2024additivelymanufacturablehighstrength pages 9-12, taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 9-12, taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 1-4) |
| **Alvi *et al.*, *npj Computational Materials* (2026).** | Cost-aware, batch deep-GP BO chooses among **unequally costly property/information-source queries** for refractory high-entropy-alloy design; not every alloy receives every measurement. | The reported alloy case is **in silico** and concerns heterogeneous property tasks, **not sequential atomization → LPBF → microstructure → testing nodes**. (alvi2026deepgaussianprocessbased pages 14-16, alvi2026deepgaussianprocessbased pages 2-4, alvi2026deepgaussianprocessbased pages 1-2) |
| **Hur and Lee, *Compressing the Validation Bottleneck* (2026 preprint).** | Proposes a cost-aware metal-AM measurement agent that could use hardness instead of tensile testing, or X-ray/composition/CALPHAD instead of more expensive characterization, requesting the latter when prediction uncertainty is high. | Calls the DED-based metal-AM laboratory one the authors **“are building”** and describes evaluation in the future tense; it does **not establish a completed, experimentally demonstrated BOFN/LPBF pipeline**. It nevertheless makes broad claims about *first cost-aware intermediate-versus-final measurement decisions in metal AM* especially risky. (hur2607compressingthevalidation pages 1-2, hur2607compressingthevalidation pages 2-4) |
| **de Sousa *et al.*, *International Journal of Advanced Manufacturing Technology* (2026); Comlek *et al.*, *Journal of Mechanical Design* (2025).** | De Sousa combines single-bead, single-layer and multilayer experiments with GP/multiobjective optimization for **AlSi10Mg laser directed-energy deposition**. Comlek fuses previously published **LPBF, electron-beam-melting and welding** data with a source-aware GP to predict Ti–6Al–4V yield strength. | Respectively, a staged **process-parameter** study rather than acquisition among costed pipeline nodes, and **predictive multi-source GP fusion** rather than sequential experimental BO. Neither is the specified LPBF alloy-production BOFN. (sousa2026gaussianprocessregression pages 1-2, sousa2026gaussianprocessregression pages 15-17, comlek2025heterogeneousmultisourcedata pages 13-17) |

Additional single-stage precedents are Tamura *et al.*’s 2021 BO of **Ni–Co superalloy gas-atomization parameters** and Kavas *et al.*’s 2025 preprint on BO-tuned **LPBF feedback control**. They optimize different parts of the proposed route, not a shared cost-aware, composition-to-mechanical-property function network. (tamura2021machinelearningdrivenoptimization pages 1-5, kavas2025insitucontrollerautotuning pages 1-3)

### Is “applied for the first time to a complex additive manufacturing pipeline for alloys” defensible?

**Not as written.** It leaves the distinguishing algorithmic feature unstated and can be read as claiming priority for applying BO to an integrated alloy-AM pipeline—despite the Taheri-Mousavi composition-to-powder-to-LPBF-to-property study—or for partial-evaluation, cost-aware network BO, which Buathong *et al.* had already developed. If the intended contribution is a *new application of an existing acquisition principle* to an experimentally realized, physically constrained **alloy LPBF process network**, a carefully delimited, qualified priority claim remains **plausible on the literature found**, but cannot be guaranteed by a search. It is important to specify whether intermediate queries are genuinely feasible given parent outputs and whether stage costs actually affect the next-evaluation decisions; merely recording intermediate observations, running inexpensive simulations before expensive tests, or using chained GPs is insufficient. (buathong2023bayesianoptimizationof pages 3-4, taherimousavi2024additivelymanufacturablehighstrength pages 9-12, torresi2026multistagebayesianoptimisation pages 6-7, buathong2506fastbayesianoptimization pages 8-9)

**Safer wording:** “To our knowledge, this is the first *demonstrated application of cost-aware Bayesian optimization of a partially evaluable function network* to an integrated **metal-alloy composition–powder-production–LPBF–microstructure–mechanical-property workflow**, in which the optimizer adaptively selects feasible intermediate or downstream evaluations under stage-dependent costs.” **Use “demonstrated” and list every stage only if the reported study actually executes or validates those stages and shows adaptive choices between them**; otherwise say “we propose a framework for…” and name only the stages implemented. (buathong2023bayesianoptimizationof pages 3-4, taherimousavi2024additivelymanufacturablehighstrength pages 9-12, hur2607compressingthevalidation pages 2-4)

References

1. (buathong2023bayesianoptimizationof pages 3-4): Poompol Buathong, Jiayue Wan, Raul Astudillo, Samuel Daulton, Maximilian Balandat, and Peter I. Frazier. Bayesian optimization of function networks with partial evaluations. ArXiv, Nov 2023. URL: https://doi.org/10.48550/arxiv.2311.02146, doi:10.48550/arxiv.2311.02146. This article has 15 citations.

2. (taherimousavi2024additivelymanufacturablehighstrength pages 9-12): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 11 citations.

3. (taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 9-12): S. Mohadeseh Taheri‐Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mirko Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high‐strength aluminum alloys with coarsening‐resistant microstructures achieved via rapid solidification. Advanced Materials, Oct 2026. URL: https://doi.org/10.1002/adma.202509507, doi:10.1002/adma.202509507. This article has 17 citations and is from a highest quality peer-reviewed journal.

4. (astudillo2021bayesianoptimizationof pages 1-2): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 84 citations.

5. (torresi2026multistagebayesianoptimisation pages 2-3): Luca Torresi and Pascal Friederich. Multi-stage bayesian optimisation for dynamic decision-making in self-driving labs. Digital Discovery, 5:1900-1912, Jan 2026. URL: https://doi.org/10.1039/d5dd00572h, doi:10.1039/d5dd00572h. This article has 7 citations and is from a peer-reviewed journal.

6. (buathong2023bayesianoptimizationof pages 7-8): Poompol Buathong, Jiayue Wan, Raul Astudillo, Samuel Daulton, Maximilian Balandat, and Peter I. Frazier. Bayesian optimization of function networks with partial evaluations. ArXiv, Nov 2023. URL: https://doi.org/10.48550/arxiv.2311.02146, doi:10.48550/arxiv.2311.02146. This article has 15 citations.

7. (buathong2023bayesianoptimizationof pages 8-9): Poompol Buathong, Jiayue Wan, Raul Astudillo, Samuel Daulton, Maximilian Balandat, and Peter I. Frazier. Bayesian optimization of function networks with partial evaluations. ArXiv, Nov 2023. URL: https://doi.org/10.48550/arxiv.2311.02146, doi:10.48550/arxiv.2311.02146. This article has 15 citations.

8. (buathong2506fastbayesianoptimization pages 9-11): Poompol Buathong and Peter I. Frazier. Fast bayesian optimization of function networks with partial evaluations. ArXiv, Jun 2506. URL: https://doi.org/10.48550/arxiv.2506.11456, doi:10.48550/arxiv.2506.11456. This article has 0 citations.

9. (buathong2506fastbayesianoptimization pages 8-9): Poompol Buathong and Peter I. Frazier. Fast bayesian optimization of function networks with partial evaluations. ArXiv, Jun 2506. URL: https://doi.org/10.48550/arxiv.2506.11456, doi:10.48550/arxiv.2506.11456. This article has 0 citations.

10. (torresi2026multistagebayesianoptimisation pages 5-6): Luca Torresi and Pascal Friederich. Multi-stage bayesian optimisation for dynamic decision-making in self-driving labs. Digital Discovery, 5:1900-1912, Jan 2026. URL: https://doi.org/10.1039/d5dd00572h, doi:10.1039/d5dd00572h. This article has 7 citations and is from a peer-reviewed journal.

11. (torresi2026multistagebayesianoptimisation pages 6-7): Luca Torresi and Pascal Friederich. Multi-stage bayesian optimisation for dynamic decision-making in self-driving labs. Digital Discovery, 5:1900-1912, Jan 2026. URL: https://doi.org/10.1039/d5dd00572h, doi:10.1039/d5dd00572h. This article has 7 citations and is from a peer-reviewed journal.

12. (torresi2026multistagebayesianoptimisation pages 7-10): Luca Torresi and Pascal Friederich. Multi-stage bayesian optimisation for dynamic decision-making in self-driving labs. Digital Discovery, 5:1900-1912, Jan 2026. URL: https://doi.org/10.1039/d5dd00572h, doi:10.1039/d5dd00572h. This article has 7 citations and is from a peer-reviewed journal.

13. (torresi2026multistagebayesianoptimisation pages 10-12): Luca Torresi and Pascal Friederich. Multi-stage bayesian optimisation for dynamic decision-making in self-driving labs. Digital Discovery, 5:1900-1912, Jan 2026. URL: https://doi.org/10.1039/d5dd00572h, doi:10.1039/d5dd00572h. This article has 7 citations and is from a peer-reviewed journal.

14. (taherimousavi2024additivelymanufacturablehighstrength pages 7-9): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 11 citations.

15. (taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 1-4): S. Mohadeseh Taheri‐Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mirko Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high‐strength aluminum alloys with coarsening‐resistant microstructures achieved via rapid solidification. Advanced Materials, Oct 2026. URL: https://doi.org/10.1002/adma.202509507, doi:10.1002/adma.202509507. This article has 17 citations and is from a highest quality peer-reviewed journal.

16. (alvi2026deepgaussianprocessbased pages 14-16): Sk Md Ahnaf Akif Alvi, Brent Vela, V. Attari, Jan Janssen, Danny Perez, Douglas L. Allaire, and Raymundo Arróyave. Deep gaussian process-based cost-aware batch bayesian optimization for complex materials design campaigns. npj Computational Materials, Feb 2026. URL: https://doi.org/10.1038/s41524-026-01981-7, doi:10.1038/s41524-026-01981-7. This article has 7 citations and is from a peer-reviewed journal.

17. (alvi2026deepgaussianprocessbased pages 2-4): Sk Md Ahnaf Akif Alvi, Brent Vela, V. Attari, Jan Janssen, Danny Perez, Douglas L. Allaire, and Raymundo Arróyave. Deep gaussian process-based cost-aware batch bayesian optimization for complex materials design campaigns. npj Computational Materials, Feb 2026. URL: https://doi.org/10.1038/s41524-026-01981-7, doi:10.1038/s41524-026-01981-7. This article has 7 citations and is from a peer-reviewed journal.

18. (alvi2026deepgaussianprocessbased pages 1-2): Sk Md Ahnaf Akif Alvi, Brent Vela, V. Attari, Jan Janssen, Danny Perez, Douglas L. Allaire, and Raymundo Arróyave. Deep gaussian process-based cost-aware batch bayesian optimization for complex materials design campaigns. npj Computational Materials, Feb 2026. URL: https://doi.org/10.1038/s41524-026-01981-7, doi:10.1038/s41524-026-01981-7. This article has 7 citations and is from a peer-reviewed journal.

19. (hur2607compressingthevalidation pages 1-2): Kyunghoon Hur and Chi-Hun Lee. Compressing the validation bottleneck: an agentic self-driving lab for scientific discovery. ArXiv, Jul 2607. URL: https://doi.org/10.48550/arxiv.2607.04508, doi:10.48550/arxiv.2607.04508. This article has 0 citations.

20. (hur2607compressingthevalidation pages 2-4): Kyunghoon Hur and Chi-Hun Lee. Compressing the validation bottleneck: an agentic self-driving lab for scientific discovery. ArXiv, Jul 2607. URL: https://doi.org/10.48550/arxiv.2607.04508, doi:10.48550/arxiv.2607.04508. This article has 0 citations.

21. (sousa2026gaussianprocessregression pages 1-2): Jurandir Marcos Sá de Sousa, Henrique Santos Ferreira, Anselmo Thiesen, Marcos Vinicius Bento, William Mendes de Farias, Priscila Maria Barra Ferreira, Mustafa Awd, Evgeniya Kabliman, Alexandre Pinhel Soares, and Juliane Ribeiro da Cruz. Gaussian process regression for optimizing l-ded processing parameters in alsi10mg additive manufacturing. The International Journal of Advanced Manufacturing Technology, 146:247-287, Jul 2026. URL: https://doi.org/10.1007/s00170-026-18817-9, doi:10.1007/s00170-026-18817-9. This article has 0 citations.

22. (sousa2026gaussianprocessregression pages 15-17): Jurandir Marcos Sá de Sousa, Henrique Santos Ferreira, Anselmo Thiesen, Marcos Vinicius Bento, William Mendes de Farias, Priscila Maria Barra Ferreira, Mustafa Awd, Evgeniya Kabliman, Alexandre Pinhel Soares, and Juliane Ribeiro da Cruz. Gaussian process regression for optimizing l-ded processing parameters in alsi10mg additive manufacturing. The International Journal of Advanced Manufacturing Technology, 146:247-287, Jul 2026. URL: https://doi.org/10.1007/s00170-026-18817-9, doi:10.1007/s00170-026-18817-9. This article has 0 citations.

23. (comlek2025heterogeneousmultisourcedata pages 13-17): Yigitcan Comlek, Sandipp Krishnan Ravi, Piyush Pandita, Sayan Ghosh, Liping Wang, and Wei Chen. Heterogeneous multi-source data fusion through input mapping and latent variable gaussian process. Journal of Mechanical Design, pages 1-17, Feb 2025. URL: https://doi.org/10.1115/1.4068016, doi:10.1115/1.4068016. This article has 13 citations and is from a domain leading peer-reviewed journal.

24. (tamura2021machinelearningdrivenoptimization pages 1-5): Ryo Tamura, Toshio Osada, Kazumi Minagawa, Takuma Kohata, Masashi Hirosawa, Koji Tsuda, and Kyoko Kawagishi. Machine learning-driven optimization in powder manufacturing of ni-co based superalloy. Materials &amp; Design, 198:109290, Jan 2021. URL: https://doi.org/10.1016/j.matdes.2020.109290, doi:10.1016/j.matdes.2020.109290. This article has 101 citations and is from a highest quality peer-reviewed journal.

25. (kavas2025insitucontrollerautotuning pages 1-3): Baris Kavas, Efe C. Balta, Michael Tucker, Raamadaas Krishnadas, Alisa Rupenyan, John Lygeros, and Markus Bambach. In-situ controller autotuning by bayesian optimization for closed-loop feedback control of laser powder bed fusion process. ArXiv, Jun 2025. URL: https://doi.org/10.48550/arxiv.2406.19096, doi:10.48550/arxiv.2406.19096. This article has 36 citations.
