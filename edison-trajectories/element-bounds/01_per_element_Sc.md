# Phase 1 — Per-element bound: Sc

*Edison task: `2fc74fd6-087f-476c-9f0c-708b561e29f3`*

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


TASK — Element-specific bound: Sc
Sc is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Sc LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Sc) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Sc) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Sc).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Element-specific compositional bound — Sc (wt%) for Al-rich LPBF BOFN search space

| Bound type | Proposed Sc upper bound (wt%) | Literature anchor composition(s) and process | Rationale/limit-setting observations | Key citations (IDs) |
|---|---:|---|---|---|
| Conservative | 0.8 | Scalmalloy® nominal 0.60–0.80 wt% Sc for SLM/LPBF; example powder batch 4.60Mg-0.66Sc-0.42Zr-0.49Mn wt%. Also consistent with LPBF Al-4.46Mn-1.09Mg-0.8Sc-0.64Zr wt% and lower-Sc SLM Al-3.02Mg-0.2Sc-0.1Zr. | 0.8 wt% is the top end of an established commercial/qualified LPBF alloy family and has direct LPBF precedent in an Al-rich Mn-Mg-Sc-Zr alloy. This makes it a defensible search-space cap before entering more exploratory high-Sc territory. | (janus2025microstructureandmechanical pages 1-3, yan2023microstructuresandhigh pages 2-4, li2019selectivelasermelting pages 1-2) |
| Non-conservative | 1.0 | Anchored by LPBF Al-4.46Mn-1.09Mg-0.8Sc-0.64Zr wt% and by SLM elemental-blend Al-0.75Sc-0.75Zr at.% (Al-rich), where ~60% of Sc and Zr precipitated as primary L12 phases; eutectic/peritectic precipitation is discussed. | 1.0 wt% Sc is an aggressive but still Al-rich exploratory cap: it extends modestly beyond the highest explicit LPBF wt% example (0.8 wt%) while remaining below compositions where primary Al3(Sc,Zr) formation substantially consumes solute and raises microstructural uncertainty. The bound is also checked by Sc cost/criticality, which strongly penalizes pushing Sc higher. | (yan2023microstructuresandhigh pages 2-4, glerum2020synthesisofprecipitationstrengthened pages 7-8, czerwinski2020criticalassessment36 pages 3-5) |


*Table: This table summarizes a literature-anchored conservative and non-conservative upper bound for scandium in Al-rich LPBF alloys. It is useful for defining BOFN/GA search limits while balancing commercial precedent, printability, phase-formation risk, and Sc criticality.*

### 1) CONSERVATIVE upper bound (Sc)
**Upper bound: Sc ≤ 0.8 wt%**.
Scalmalloy® (developed for SLM/LPBF) has a published nominal Sc range of **0.60–0.80 wt%**, with an example powder batch at **0.66 wt% Sc** (and Mg 4.60 wt%, Zr 0.42 wt%, Mn 0.49 wt%), making **0.8 wt%** a directly defensible “commercial/qualified” upper cap. (janus2025microstructureandmechanical pages 1-3)

### 2) NON-CONSERVATIVE upper bound (Sc)
**Upper bound: Sc ≤ 1.0 wt%**.
An explicit LPBF Al-rich multicomponent alloy has been demonstrated at **0.8 wt% Sc** (Al-4.46Mn-1.09Mg-0.8Sc-0.64Zr, wt%, ICP-AES), so **1.0 wt%** extends modestly beyond the highest clearly documented LPBF value while remaining in an Al-rich regime; further increases are increasingly likely to be “wasted” into primary L1\_2 Al3(Sc,Zr) formed during rapid solidification (≈**60%** of Sc and Zr consumed as primary L1\_2 precipitates in an Al-Sc-Zr SLM elemental-blend study). (yan2023microstructuresandhigh pages 2-4, glerum2020synthesisofprecipitationstrengthened pages 7-8)

### 3) Key failure modes that set each bound

**Conservative bound (0.8 wt% Sc): key limiters**
- **Cost / mineral-burden / supply-chain criticality:** Sc is described as scarce with high, volatile pricing and supply limitations, which makes higher-Sc regions disproportionately unattractive under a mineral-burden objective. (czerwinski2020criticalassessment36 pages 3-5)
- **Primary intermetallic formation / microstructure heterogeneity:** Sc (with Zr) forms primary Al3(Sc,Zr) that nucleates before α-Al and drives heterogeneous microstructures; while beneficial for grain refinement, it can also consume solute and complicate structure/property control if pushed higher. (lu2023microstructuralevaluationand pages 9-10)

**Non-conservative bound (1.0 wt% Sc): key additional limiters**
- **Solute “waste” into primary L1\_2 phases and non-equilibrium eutectic/peritectic precipitation:** In SLM Al-Sc-Zr, a large fraction of Sc can precipitate as **primary L1\_2** during rapid solidification (reported ~60%), with additional mention that phases may precipitate as **eutectic/peritectic** under fast cooling; this reduces Sc supersaturation available for desired secondary precipitation and raises uncertainty/risk as Sc increases. (glerum2020synthesisofprecipitationstrengthened pages 7-8)
- **Process-parameter sensitivity / defects (cracks vs keyholing/evaporation):** In SLM Al–3.02Mg–0.2Sc–0.1Zr, cracks could be inhibited by increasing VED, but excessive VED caused transition to **keyhole mode due to metal evaporation**, reflecting a narrow process window that can tighten further as composition and melting behavior change. (li2019selectivelasermelting pages 1-2)
- **Evaporation-driven porosity:** LPBF Al-Mg-Sc-Zr studies report evaporation of low-melting elements (Mg) causing **gas pores** and constraints on parameters to avoid violent vaporization/sputtering; higher rare-earth/transition additions can exacerbate sensitivity to thermal history and melt pool dynamics. (lu2023microstructuralevaluationand pages 9-10)

### 4) Element-specific caveats / interactions for follow-up joint-constraints analysis

- **Strong Sc–Zr coupling:** Zr co-addition promotes thermally stable core–shell Al3(Sc,Zr) nano-precipitates and is widely used to reduce Sc usage (cost) while maintaining strengthening; joint constraints should consider keeping **Zr/Sc** above a minimum to avoid over-reliance on Sc. (lu2023microstructuralevaluationand pages 1-2, glerum2020synthesisofprecipitationstrengthened pages 7-8)
- **Cracking vs grain-refinement trade:** Sc/Zr inoculates can markedly alleviate hot/solidification cracking by grain refinement and heterogeneous grain structures, so Sc should not be treated purely as a “risk” element—there is a processability benefit that interacts with Mn/Mg/Si and scan strategy. (yan2023microstructuresandhigh pages 1-2)
- **Mg interaction (evaporation + pore formation):** In Al-Mg-based LPBF alloys, Mg evaporation is explicitly linked to gas porosity; if BOFN explores higher Mg simultaneously with higher Sc, incorporate a coupled constraint (e.g., maximum Mg or energy-density envelope) to avoid confounding “composition vs process” effects. (lu2023microstructuralevaluationand pages 9-10)
- **Economics-driven constraint:** Because Sc’s cost/availability is a dominant practical limiter, treat Sc as having an explicit mineral-burden penalty and consider a hard cap (conservative) plus a soft cap (non-conservative) depending on optimization phase. (czerwinski2020criticalassessment36 pages 3-5)


References

1. (janus2025microstructureandmechanical pages 1-3): K. Janus, A. Jarzębska, A. Wójcik, A. Garbacz-Klempka, J. Piekło, S. Terlicka, M. Piękoś, J. J. Sobczak, O. Krasa, and Ł. Krawczyk. Microstructure and mechanical properties of scalmalloy® produced by selective laser melting in term of long-term applications. Archives of Civil and Mechanical Engineering, May 2025. URL: https://doi.org/10.1007/s43452-025-01242-2, doi:10.1007/s43452-025-01242-2. This article has 2 citations.

2. (yan2023microstructuresandhigh pages 2-4): Yuqing Yan, Chengqi Lu, Zhenyu Chen, Yuhao Zhuo, Chuanyang Wang, and Qingbo Jia. Microstructures and high temperature tensile behaviours of laser powder bed fusion fabricated al-mn-sc alloy. Metals, 13:788, Apr 2023. URL: https://doi.org/10.3390/met13040788, doi:10.3390/met13040788. This article has 9 citations.

3. (li2019selectivelasermelting pages 1-2): Rui-di Li, Hui Chen, Chao Chen, Hongbin Zhu, Minbo Wang, Tiechui Yuan, and B. Song. Selective laser melting of gas atomized al–3.02mg–0.2sc–0.1zr alloy powder: microstructure and mechanical properties. Advanced Engineering Materials, Dec 2019. URL: https://doi.org/10.1002/adem.201800650, doi:10.1002/adem.201800650. This article has 33 citations and is from a peer-reviewed journal.

4. (glerum2020synthesisofprecipitationstrengthened pages 7-8): Jennifer A. Glerum, Christoph Kenel, Tao Sun, and David C. Dunand. Synthesis of precipitation-strengthened al-sc, al-zr and al-sc-zr alloys via selective laser melting of elemental powder blends. Additive Manufacturing, 36:101461, Dec 2020. URL: https://doi.org/10.1016/j.addma.2020.101461, doi:10.1016/j.addma.2020.101461. This article has 105 citations and is from a highest quality peer-reviewed journal.

5. (czerwinski2020criticalassessment36 pages 3-5): Frank Czerwinski. Critical assessment 36: assessing differences between the use of cerium and scandium in aluminium alloying. Materials Science and Technology, 36:255-263, Feb 2020. URL: https://doi.org/10.1080/02670836.2019.1702775, doi:10.1080/02670836.2019.1702775. This article has 51 citations and is from a peer-reviewed journal.

6. (lu2023microstructuralevaluationand pages 9-10): Yuxian Lu, Hao Zhang, Peng Xue, Lihui Wu, Fengchao Liu, Luanluan Jia, Dingrui Ni, Bolv Xiao, and Zongyi Ma. Microstructural evaluation and tensile properties of al-mg-sc-zr alloys prepared by lpbf. Crystals, 13:913, Jun 2023. URL: https://doi.org/10.3390/cryst13060913, doi:10.3390/cryst13060913. This article has 23 citations.

7. (lu2023microstructuralevaluationand pages 1-2): Yuxian Lu, Hao Zhang, Peng Xue, Lihui Wu, Fengchao Liu, Luanluan Jia, Dingrui Ni, Bolv Xiao, and Zongyi Ma. Microstructural evaluation and tensile properties of al-mg-sc-zr alloys prepared by lpbf. Crystals, 13:913, Jun 2023. URL: https://doi.org/10.3390/cryst13060913, doi:10.3390/cryst13060913. This article has 23 citations.

8. (yan2023microstructuresandhigh pages 1-2): Yuqing Yan, Chengqi Lu, Zhenyu Chen, Yuhao Zhuo, Chuanyang Wang, and Qingbo Jia. Microstructures and high temperature tensile behaviours of laser powder bed fusion fabricated al-mn-sc alloy. Metals, 13:788, Apr 2023. URL: https://doi.org/10.3390/met13040788, doi:10.3390/met13040788. This article has 9 citations.

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


TASK — Element-specific bound: Sc
Sc is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Sc LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Sc) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Sc) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Sc).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
