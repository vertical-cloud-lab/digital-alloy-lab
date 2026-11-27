# Phase 1 — Per-element bound: Mg

*Edison task: `f2312e42-605c-468d-8028-f21c3b3b5d15`*

## Answer

Question: PROJECT CONTEXT — FLAIME (Fast Learning AI for Mineral Efficiency), DOE Genesis
Mission Phase I, Topic 3-B (AMMTO). The team is performing Bayesian Optimization
over Function Networks (BOFN/pKGFN) over a single joint search space:
(Al + 15 non-Al alloying elements) x atomization process x LPBF process.

The 15 non-Al element palette is:
  Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn.

Composition is parameterized as weight fractions that sum to 1.0; Al is the
matrix element. Down-selection is driven by CALPHAD (TCAl10 + AM Module),
Scheil solidification range, hot-cracking susceptibility, printability, and a
mineral-burden objective (USGS criticality / import reliance).

Anchor systems include Al-Mn-Cr-Zr and Al-Zr; the broader palette is intended
to enable AI-discovered sub-systems (ternary through ~9-component). All alloys
are Al-rich (Al typically >= 85 wt% for good LPBF processability and to remain
within the trustworthy region of TCAl10's binary/ternary Muggianu extrapolation).

We need element-by-element compositional BOUNDS (in weight percent, wt%) for
the BOFN / GA acquisition inner-solver search space.


TASK — Element-specific bound: Mg
Mg is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Mg LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Mg) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Mg) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Mg).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


This response proposes Mg (wt%) bounds for the BOFN/GA inner-solver LPBF Al-alloy search space, grounded in Mg levels used in commercial/qualified LPBF powders and in published higher‑Mg LPBF/SLM alloy studies.

| Bound type | Suggested Mg upper bound (wt%) | Primary literature basis (named alloy/composition) | Evidence snippets summary (1 line) | Key failure modes/constraints |
|---|---:|---|---|---|
| Conservative | 4.5 | Scalmalloy / Al-4.5Mg-0.75Sc-0.35Zr-0.45Mn; corroborated by LPBF Al-Mg alloy practice around AA5083-family Mg contents (babu2021developmentofhigh pages 74-74, zhou2019microstructureandmechanical pages 1-2) | Commercial AM benchmark Scalmalloy sits at 4.5 wt% Mg, while AA5083-family LPBF powders are ~3.2–3.3 wt% Mg and unmodified 5xxx already show cracking sensitivity near this range (babu2021developmentofhigh pages 74-74, zhou2019microstructureandmechanical pages 1-2, hyer2021effectsofalloy pages 4-6) | Solidification/hot cracking peaks near ~4.5 wt% Mg in Al-Mg modeling; AA5083 shows cracking without modification; Mg burn-off/unstable melt dynamics, spatter, pores, and MgO fume formation remain concerns (hyer2021effectsofalloy pages 4-6, bartl2022influenceofsurface pages 1-2, mauduit2017studyofthe pages 19-20) |
| Non-conservative | 8.0 | High-Mg SLM alloy design Al-8.0Mg-1.3Si-0.5Mn-0.5Sc-0.3Zr; related Al-6Mg and Al-6Mg-1.3Si studies (li2020developingahighstrength pages 1-2, li2020developingahighstrength pages 2-5) | 6 wt% Mg without Si develops microcracks, 6 wt% Mg + 1.3 wt% Si suppresses cracking, and an 8 wt% Mg designed alloy was printed dense/crack-free but showed Mg loss to ~6.82 wt% after printing (li2020developingahighstrength pages 2-5, li2020developingahighstrength pages 1-2) | Requires joint constraints with Si and grain refiners; otherwise high Mg raises crack density, shrinkage, evaporation/composition drift, and print instability; practical retained Mg may fall below nominal due to burn-off (li2020developingahighstrength pages 2-5, leijon2023highthroughputprintabilityscreening pages 1-2, bartl2022influenceofsurface pages 1-2) |


*Table: This table summarizes conservative and non-conservative Mg upper bounds for Al-rich LPBF alloy search spaces, grounded in commercial AM alloys and higher-Mg experimental SLM studies. It also highlights the Mg-specific failure modes and alloy interactions that should inform subsequent joint-constraint modeling.*

## 1) CONSERVATIVE Mg upper bound: **4.5 wt% Mg**
A conservative upper bound of 4.5 wt% is supported by the commercial AM benchmark Scalmalloy (often reported as Al-4.5Mg-0.75Sc-0.35Zr-0.45Mn), demonstrating industrially used LPBF Al-rich Al–Mg–(Sc,Zr) chemistry at ~4.5 wt% Mg (babu2021developmentofhigh pages 74-74). This is also consistent with literature identifying maximum solidification-cracking susceptibility in Al–Mg near ~4.5 wt% Mg and the observation that 5xxx-series compositions around this Mg level (e.g., AA5083-family) are challenging and crack-prone in LPBF unless modified (hyer2021effectsofalloy pages 4-6, zhou2019microstructureandmechanical pages 1-2).

## 2) NON-CONSERVATIVE Mg upper bound: **8.0 wt% Mg**
A defensible but more aggressive upper bound is 8.0 wt% Mg, based on experimental SLM/LPBF alloy design studies that explicitly target and print an Al-8.0Mg-1.3Si-0.5Mn-0.5Sc-0.3Zr composition, achieving crack-free/dense builds when coupled with Si (eutectic/Mg2Si) and grain-refining/strengthening additions (Sc, Zr, Mn) (li2020developingahighstrength pages 1-2). In the same work, a 6 wt% Mg alloy without sufficient Si showed micro-cracking, while 6 wt% Mg + 1.3 wt% Si suppressed cracking; the “8 wt% Mg” design also exhibited measurable Mg loss during processing (printed Mg ~6.82 wt%), implying that evaporation/composition drift increases with such high nominal Mg and must be anticipated in constraints (li2020developingahighstrength pages 2-5).

## 3) Key failure modes that set each bound
### Conservative bound (~4.5 wt% Mg)
- **Solidification/hot cracking near Al–Mg peak susceptibility**: Modeling indicates a maximum cracking susceptibility around ~4.5 wt% Mg, aligning with typical 5xxx Mg levels and motivating not exceeding this in a “safe” search space absent strong crack-mitigation measures (hyer2021effectsofalloy pages 4-6).
- **LPBF cracking/defect sensitivity in 5xxx-like chemistries**: AA5083-family powders at ~3.2–3.3 wt% Mg showed poor buildability in LPBF (pores/solidification cracking/compositional deviation due to evaporation) unless modified (e.g., Zr-containing variant) (zhou2019microstructureandmechanical pages 1-2).
- **Mg evaporation / burn-off and melt instability**: Mg evaporation during laser melting can generate MgO-rich fumes and is linked to unstable melt dynamics, increased spatter, and defects such as voids and process pores; thus even at moderate Mg, process robustness can degrade (bartl2022influenceofsurface pages 1-2, mauduit2017studyofthe pages 19-20).

### Non-conservative bound (~8 wt% Mg)
- **Hot cracking and micro-cracking above ~6 wt% Mg without eutectic/feeding control**: In SLM Al–Mg–Sc–Zr, increasing Mg increases crack density; 6 wt% Mg exhibited micro-cracks and reduced strength unless Si was added (li2020developingahighstrength pages 1-2, li2020developingahighstrength pages 2-5).
- **Evaporation-driven composition deviation (especially at high Mg)**: High-Mg designs show Mg loss between nominal and as-printed composition, consistent with the general observation that Mg evaporates readily in LPBF and that evaporative loss increases with Mg content (li2020developingahighstrength pages 2-5, leijon2023highthroughputprintabilityscreening pages 1-2, mauduit2017studyofthe pages 19-20).
- **Spatter/porosity and powder/process contamination risks**: Mg evaporation is associated with turbulent molten pools, spatter, and porosity; MgO fumes/dust can also burden filtration and chamber cleanliness (mauduit2017studyofthe pages 19-20, bartl2022influenceofsurface pages 1-2).

## 4) Element-specific caveats and Mg interactions for joint-constraints analysis
- **Mg–Si coupling is critical**: Si additions can suppress cracking in high-Mg Al by forming an intergranular/eutectic constituent (Mg2Si/Al eutectic) that improves feeding and reduces crack formation; empirically, adding 1.3 wt% Si to Al-6Mg-0.2Sc-0.1Zr inhibited hot cracking (li2020developingahighstrength pages 1-2, li2020developingahighstrength pages 2-5). Therefore, allowing Mg > ~4.5 wt% should likely be paired with a minimum Si constraint (or an equivalent eutectic-former strategy).
- **Grain-refiner/precipitation additions interact with Mg-enabled printability**: Sc and Zr (forming Al3(Sc,Zr)) and/or other refiners (Ti, Zr, Sc) are cited as printability-restoring strategies when shrinkage and cracking risk rise; these additions may be necessary if exploring high-Mg regions (li2020developingahighstrength pages 1-2, leijon2023highthroughputprintabilityscreening pages 1-2).
- **Mg evaporation scales with Mg content and affects “as-built composition” constraints**: Screening work reports Mg evaporative loss increases linearly with Mg level, and high-Mg alloy printing can show measurable Mg loss versus nominal (leijon2023highthroughputprintabilityscreening pages 1-2, li2020developingahighstrength pages 2-5). For BOFN, consider constraining both (a) nominal Mg and (b) predicted retained Mg after evaporation (process-dependent), or penalize compositions requiring large evaporation compensation.
- **Interaction with 5xxx-like cracking peak**: Even “moderate” Mg near 4–5 wt% aligns with a cracking-susceptibility maximum in Al–Mg; if Mg is placed near that region, additional mitigation (Si/eutectic engineering, diffusion/freezing-time manipulation, grain refinement) may be required (hyer2021effectsofalloy pages 4-6, leijon2023highthroughputprintabilityscreening pages 1-2).



References

1. (babu2021developmentofhigh pages 74-74): ABIRAMI PRIYADARSHINI BABU. Development of high solute aluminium alloys in net shape through additive manufacturing. ArXiv, Sep 2021. URL: https://doi.org/10.26180/16552485.v1, doi:10.26180/16552485.v1. This article has 0 citations.

2. (zhou2019microstructureandmechanical pages 1-2): Le Zhou, Holden Hyer, Sharon Park, Hao Pan, Yuanli Bai, Katherine P. Rice, and Yongho Sohn. Microstructure and mechanical properties of zr-modified aluminum alloy 5083 manufactured by laser powder bed fusion. Additive Manufacturing, 28:485-496, Aug 2019. URL: https://doi.org/10.1016/j.addma.2019.05.027, doi:10.1016/j.addma.2019.05.027. This article has 244 citations and is from a highest quality peer-reviewed journal.

3. (hyer2021effectsofalloy pages 4-6): Holden Hyer, Le Zhou, Abhishek Mehta, and Yongho Sohn. Effects of alloy composition and solid-state diffusion kinetics on powder bed fusion cracking susceptibility. Journal of Phase Equilibria and Diffusion, 42:5-13, Nov 2021. URL: https://doi.org/10.1007/s11669-020-00844-y, doi:10.1007/s11669-020-00844-y. This article has 38 citations and is from a peer-reviewed journal.

4. (bartl2022influenceofsurface pages 1-2): Marko Bärtl, Xiao Xiao, Jürgen Brillo, and Frank Palm. Influence of surface tension and evaporation on melt dynamics of aluminum alloys for laser powder bed fusion. Journal of Materials Engineering and Performance, 31:6221-6233, Jan 2022. URL: https://doi.org/10.1007/s11665-022-06592-z, doi:10.1007/s11665-022-06592-z. This article has 28 citations and is from a peer-reviewed journal.

5. (mauduit2017studyofthe pages 19-20): A Mauduit, S Pillot, and H Gransac. Study of the suitability of aluminum alloys for additive manufacturing by laser powder bed fusion. Unknown journal, 2017.

6. (li2020developingahighstrength pages 1-2): Ruidi Li, Minbo Wang, Zhiming Li, Peng Cao, Tiechui Yuan, and Hongbin Zhu. Developing a high-strength al-mg-si-sc-zr alloy for selective laser melting: crack-inhibiting and multiple strengthening mechanisms. Acta Materialia, 193:83-98, Jul 2020. URL: https://doi.org/10.1016/j.actamat.2020.03.060, doi:10.1016/j.actamat.2020.03.060. This article has 619 citations and is from a highest quality peer-reviewed journal.

7. (li2020developingahighstrength pages 2-5): Ruidi Li, Minbo Wang, Zhiming Li, Peng Cao, Tiechui Yuan, and Hongbin Zhu. Developing a high-strength al-mg-si-sc-zr alloy for selective laser melting: crack-inhibiting and multiple strengthening mechanisms. Acta Materialia, 193:83-98, Jul 2020. URL: https://doi.org/10.1016/j.actamat.2020.03.060, doi:10.1016/j.actamat.2020.03.060. This article has 619 citations and is from a highest quality peer-reviewed journal.

8. (leijon2023highthroughputprintabilityscreening pages 1-2): Freddy Leijon and Johan Moverare. High-throughput printability screening of almgsi alloys for powder bed fusion. Metals, 13:1114, Jun 2023. URL: https://doi.org/10.3390/met13061114, doi:10.3390/met13061114. This article has 0 citations.

---

## Prompt

```
PROJECT CONTEXT — FLAIME (Fast Learning AI for Mineral Efficiency), DOE Genesis
Mission Phase I, Topic 3-B (AMMTO). The team is performing Bayesian Optimization
over Function Networks (BOFN/pKGFN) over a single joint search space:
(Al + 15 non-Al alloying elements) x atomization process x LPBF process.

The 15 non-Al element palette is:
  Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn.

Composition is parameterized as weight fractions that sum to 1.0; Al is the
matrix element. Down-selection is driven by CALPHAD (TCAl10 + AM Module),
Scheil solidification range, hot-cracking susceptibility, printability, and a
mineral-burden objective (USGS criticality / import reliance).

Anchor systems include Al-Mn-Cr-Zr and Al-Zr; the broader palette is intended
to enable AI-discovered sub-systems (ternary through ~9-component). All alloys
are Al-rich (Al typically >= 85 wt% for good LPBF processability and to remain
within the trustworthy region of TCAl10's binary/ternary Muggianu extrapolation).

We need element-by-element compositional BOUNDS (in weight percent, wt%) for
the BOFN / GA acquisition inner-solver search space.


TASK — Element-specific bound: Mg
Mg is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Mg LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Mg) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Mg) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Mg).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
