# Phase 1 — Per-element bound: Li

*Edison task: `33d44d1f-07b8-466d-b8ff-232de5a85e7c`*

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


TASK — Element-specific bound: Li
Li is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Li LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Li) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Li) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Li).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Element-specific compositional bounds for Li (wt%) in Al-rich LPBF BOFN search space

| Bound type | Proposed Li upper bound (wt%) | Primary literature basis | Key limiting failure modes |
|---|---:|---|---|
| Conservative | 1.5 | 2195 LPBF used 1.08 wt% Li powder and achieved crack-free, 99.92% dense builds under Ar with O2/H2O <100 ppm, so ~1.5 wt% stays close to demonstrated high-density LPBF practice for Al-rich Al-Li alloys (qi2019analuminumlithiumallloy pages 1-2). Shao et al. also show 1 wt% Li gives the best density/property balance among 1/2/3 wt% SLM alloys (99.51% density) (shao2024microstructureandmechanical pages 1-2). | Hot cracking sensitivity of Al-Li alloys (large solidification range, high thermal expansion, eutectic grain-boundary films); Li evaporation/handling sensitivity; need for tight atmosphere control. |
| Non-conservative | 3.0 | Shao et al. successfully printed 1, 2, and 3 wt% Li Al-Cu-Li-Mg-Ag-Sc-Zr alloys; at 3 wt% Li, as-printed Li reached 3.24 wt% but density fell to ~92% with ~15% Li loss and δ’ formation, making 3.0 wt% an aggressive but still experimentally demonstrated ceiling (shao2024microstructureandmechanical pages 12-14, shao2024microstructureandmechanical pages 3-4, shao2024microstructureandmechanical pages 1-2). Binary USP-LPBF has reached 4 wt% Li, but only at ~95–96% density with vapor-hole/porosity issues and near the cited ~4.0–4.2 wt% α-Al solubility limit, so 4 wt% is better treated as an outer literature edge than a BO search bound (yurekliaUnknownyear3dprintingof pages 1-4, yurekliaUnknownyear3dprintingof pages 4-6, shao2024microstructureandmechanical pages 12-14). | Volatile-pore formation and strong densification loss above ~2–3 wt% Li; ~15% Li evaporation; δ’/Al3Li emergence by 3 wt%; narrowing process window. Pushing toward 4 wt% approaches α-Al solubility/theoretical limit and gives only moderate density with vapor-hole defects. |


*Table: This table summarizes conservative and non-conservative Li upper bounds for Al-rich LPBF alloy search spaces, grounded in demonstrated LPBF/SLM literature and the observed failure modes that become limiting as Li increases.*

### 1) CONSERVATIVE upper bound: **Li ≤ 1.5 wt%**
A qualified aerospace Al–Cu–Li alloy powder (AA2195 chemistry) used for LPBF contained **Li = 1.08 wt%** and was printed **crack-free at 99.92% relative density** under protective Ar with **O2 and H2O < 100 ppm** after parameter optimization, supporting ~1–1.5 wt% Li as an established, defensible LPBF-safe regime. (qi2019analuminumlithiumallloy pages 1-2)

### 2) NON-CONSERVATIVE upper bound: **Li ≤ 3.0 wt%**
SLM of Al–Cu–Li–Mg–Ag–Sc–Zr prealloyed powders with **nominal Li = 1, 2, 3 wt%** was demonstrated; the 3 wt% alloy printed crack-free but showed a large density drop (to **~92%**) and **δ′ (Al3Li)** formation, indicating 3.0 wt% is an aggressive but experimentally demonstrated ceiling before severe volatility/porosity and phase risks dominate. (shao2024microstructureandmechanical pages 1-2, shao2024microstructureandmechanical pages 12-14)

*Literature edge (outer limit, not recommended as BO bound):* binary USP-LPBF reported printing **Al–4 wt% Li** near the cited ~4 wt% solubility limit, but only achieved ~95–96% density with vapor-hole/porosity defects, indicating rapidly diminishing printability margin near 4 wt% Li. (yurekliaUnknownyear3dprintingof pages 1-4, yurekliaUnknownyear3dprintingof pages 4-6)

### 3) Key failure modes that set each bound

**Conservative bound (~1.5 wt% Li) limiting modes**
- **Hot cracking susceptibility**: Al–Li alloys are prone to hot cracking in laser processing due to large solidification range, high thermal expansion, and low-melting eutectic formation; conservative Li helps avoid pushing these sensitivities. (qi2019analuminumlithiumallloy pages 1-2)
- **Powder/processing environmental sensitivity**: successful AA2195 LPBF used stringent atmosphere control (**O2/H2O <100 ppm**), implying risk of oxidation/contamination issues if Li (high chemical activity) is increased without tight controls. (qi2019analuminumlithiumallloy pages 1-2)

**Non-conservative bound (~3.0 wt% Li) limiting modes**
- **Volatilization-driven porosity and densification loss**: at higher Li (and with Mg present), higher energy input/residence time increases Li/Mg volatilization and produces spherical/circular “volatile pores”; at 3 wt% Li densification dropped to ~92%. (shao2024microstructureandmechanical pages 12-14, shao2024microstructureandmechanical pages 1-2)
- **Li loss / composition drift**: ~**15% Li loss** during SLM was reported, complicating composition control and CALPHAD fidelity. (shao2024microstructureandmechanical pages 1-2)
- **Phase/embrittlement risk**: δ′ (Al3Li) appeared at 3 wt% Li in the SLM Al–Cu–Li–Mg–Ag–Sc–Zr system, coincident with sharp ductility loss. (shao2024microstructureandmechanical pages 12-14)
- **Narrower process window**: higher Li required higher optimized energy density and exhibited more defect sensitivity. (shao2024microstructureandmechanical pages 12-14)

### 4) Element-specific caveats / interactions for joint-constraints analysis
- **Li–Cu coupling controls precipitate field**: as Li increases, the dominant Cu–Li phases shift (≈1 wt%: θ/T1/TB; ≈2 wt%: T1+T2; ≈3 wt%: T2+δ′), so Li bounds should be co-analyzed with Cu to avoid undesirable precipitate regimes and ductility collapse. (shao2024microstructureandmechanical pages 12-14)
- **Li–Mg co-volatility**: Li and Mg are both low-melting/volatile under SLM; if Mg is allowed in the palette, enforce a joint constraint or penalize combinations that require high energy density (risking volatilization pores). (shao2024microstructureandmechanical pages 12-14)
- **Sc/Zr as compensating additions**: Sc+Zr additions form Al3(Sc,Zr) dispersoids that refine grains and mitigate cracking; if exploring Li toward the non-conservative limit, consider requiring minimum Sc+Zr (or treating them as preferred companions) to preserve printability. (shao2024microstructureandmechanical pages 1-2, shao2024microstructureandmechanical pages 2-3)
- **Atmosphere constraint**: successful LPBF of Li-bearing AA2195 explicitly used Ar with **O2/H2O <100 ppm**; treat oxygen/moisture control as a process-side constraint interacting with Li. (qi2019analuminumlithiumallloy pages 1-2)
- **Near-solubility regime caution**: a cited equilibrium α-Al Li solubility of ~4.2 wt% suggests that pushing Li above ~3 wt% heads toward a regime where δ/δ′ risks and porosity dominate unless very high solidification rates are assured (e.g., specialized USP-LPBF). (shao2024microstructureandmechanical pages 12-14, yurekliaUnknownyear3dprintingof pages 1-4)

References

1. (qi2019analuminumlithiumallloy pages 1-2): Yang Qi, Hu Zhang, Haihong Zhu, Xiaojia Nie, and Xiaoyan Zeng. An aluminum-lithium allloy produced by laser powder bed fusion. Unknown, Jan 2019. URL: https://doi.org/10.26153/tsw/17298, doi:10.26153/tsw/17298. This article has 1 citations.

2. (shao2024microstructureandmechanical pages 1-2): Shuobing Shao, Zhuoheng Liang, Peng Yin, Xinyuan Li, and Yongzhong Zhang. Microstructure and mechanical properties of al–li alloys with different li contents prepared by selective laser melting. Materials, 17:657, Jan 2024. URL: https://doi.org/10.3390/ma17030657, doi:10.3390/ma17030657. This article has 11 citations.

3. (shao2024microstructureandmechanical pages 12-14): Shuobing Shao, Zhuoheng Liang, Peng Yin, Xinyuan Li, and Yongzhong Zhang. Microstructure and mechanical properties of al–li alloys with different li contents prepared by selective laser melting. Materials, 17:657, Jan 2024. URL: https://doi.org/10.3390/ma17030657, doi:10.3390/ma17030657. This article has 11 citations.

4. (shao2024microstructureandmechanical pages 3-4): Shuobing Shao, Zhuoheng Liang, Peng Yin, Xinyuan Li, and Yongzhong Zhang. Microstructure and mechanical properties of al–li alloys with different li contents prepared by selective laser melting. Materials, 17:657, Jan 2024. URL: https://doi.org/10.3390/ma17030657, doi:10.3390/ma17030657. This article has 11 citations.

5. (yurekliaUnknownyear3dprintingof pages 1-4): B Yüreklia, D Liub, T Ullspergera, H Kohla, and L Schadea. 3d printing of al-li with increased li content using laser assisted powder bed fusion. Unknown journal, Unknown year.

6. (yurekliaUnknownyear3dprintingof pages 4-6): B Yüreklia, D Liub, T Ullspergera, H Kohla, and L Schadea. 3d printing of al-li with increased li content using laser assisted powder bed fusion. Unknown journal, Unknown year.

7. (shao2024microstructureandmechanical pages 2-3): Shuobing Shao, Zhuoheng Liang, Peng Yin, Xinyuan Li, and Yongzhong Zhang. Microstructure and mechanical properties of al–li alloys with different li contents prepared by selective laser melting. Materials, 17:657, Jan 2024. URL: https://doi.org/10.3390/ma17030657, doi:10.3390/ma17030657. This article has 11 citations.

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


TASK — Element-specific bound: Li
Li is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Li LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Li) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Li) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Li).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
