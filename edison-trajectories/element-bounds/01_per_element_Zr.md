# Phase 1 — Per-element bound: Zr

*Edison task: `6f403085-5c64-4837-b305-93ee368b3afb`*

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


TASK — Element-specific bound: Zr
Zr is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Zr LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Zr) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Zr) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Zr).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Zr (zirconium) upper bounds for BOFN / GA inner-solver (wt%)

| Bound type | Proposed Zr upper bound (wt%) | Literature anchor(s) with key numeric composition | 1-sentence rationale | Main limiting failure modes |
|---|---:|---|---|---|
| Conservative | 1.0 | Scalmalloy contains 0.1 at.% Zr (~0.3–0.35 wt% Zr); in LPBF Al7050, 0.4 wt% Zr was insufficient to fully suppress cracking, while 1 wt% Zr produced crack-free parts; Yu et al. likewise tested 0.3 and 1 wt% Zr in 7075 and found 1 wt% viable but with porosity tradeoff (glerum2020synthesisofprecipitationstrengthened pages 1-2, mertens2021laserpowderbed pages 1-3, mertens2021laserpowderbed pages 5-7, mertens2021laserpowderbed pages 3-5, yu2022processingandcharacterization pages 2-3) | 1.0 wt% is a conservative ceiling because it is already demonstrated as an effective LPBF grain-refining/crack-mitigation level in Al-rich high-strength systems while remaining close to the upper end of established AM practice rather than exploratory high-Zr alloy design (mertens2021laserpowderbed pages 1-3, mertens2021laserpowderbed pages 5-7, mertens2021laserpowderbed pages 3-5). | If pushed higher than this in general Al-rich LPBF spaces, risk rises for additive-induced porosity/fluidity penalties, onset of primary Al3Zr formation beyond effective supersaturation, and unnecessary mineral-burden/cost penalty; below this, cracking may remain insufficiently suppressed in crack-sensitive chemistries (mehta2023advancingnovelalmncrzr pages 3-5, yu2022processingandcharacterization pages 2-3). |
| Non-conservative | 1.5 | Mehta reports LPBF Zr solubility ~0.5–0.7 wt%, intentionally tested 1.0–1.2 wt% Zr alloys, and notes local trapping up to ~1.5 wt%; Kimura successfully printed Al–4Cr–1.5Zr; Griffiths processed Al–3.6Mg–1.2Zr and Al–2.9Mg–2.1Zr by SLM (mehta2023advancingnovelalmncrzr pages 5-7, kimura2021microstructuraldevelopmentand pages 7-9, mehta2023advancingnovelalmncrzr pages 1-3, mehta2023advancingnovelalmncrzr pages 3-5, griffiths2020coarseningandcreep pages 1-2) | 1.5 wt% is an aggressive but still defensible ceiling because LPBF studies show successful processing at 1.2–1.5 wt% Zr and Mehta explicitly identifies ~1.5 wt% as a plausible locally trapped level under rapid solidification, whereas going beyond this moves further into primary-intermetallic-dominated and less generalizable territory (mehta2023advancingnovelalmncrzr pages 5-7, kimura2021microstructuraldevelopmentand pages 7-9, mehta2023advancingnovelalmncrzr pages 3-5). | Primary Al3Zr formation/coarsening and associated embrittlement risk become more likely above the ~0.5–0.7 wt% supersaturation window; chemistry-dependent cracking can reappear when Zr is combined with eutectic-forming additions such as Mg, and model trustworthiness/generality degrade as the search enters more extreme nonequilibrium/high-intermetallic regimes (mehta2023advancingnovelalmncrzr pages 5-7, mehta2023advancingnovelalmncrzr pages 3-5, griffiths2020coarseningandcreep pages 1-2). |


*Table: This table summarizes conservative and non-conservative Zr upper bounds for Al-rich LPBF BOFN search spaces, anchored to published LPBF/SLM compositions and observed printability behavior. It is useful for choosing a practical search ceiling while flagging the mechanisms that likely limit higher Zr contents.*

### 1) CONSERVATIVE upper bound: **Zr ≤ 1.0 wt%**
A 1 wt% Zr ceiling is supported by LPBF studies in crack-sensitive high-strength Al alloys showing 0.4 wt% Zr was insufficient to fully prevent cracking, while increasing to ~1 wt% Zr yielded completely crack-free LPBF parts via Al3Zr-enabled grain refinement (mertens2021laserpowderbed pages 3-5). AA7075 LPBF work similarly shows 1 wt% Zr (vs 0.3 wt%) reduced crack density and enabled crack-free builds (at suitable energy density), providing additional precedent for ~1 wt% as an effective “upper-end of standard practice” Zr level (yu2022processingandcharacterization pages 1-2).

### 2) NON-CONSERVATIVE upper bound: **Zr ≤ 1.5 wt%**
A 1.5 wt% Zr ceiling is aggressive but defensible because (i) a heat-resistant alloy Al–4Cr–1.5Zr has been fabricated by L-PBF, and (ii) alloy-design work for PBF-LB indicates an effective Zr solubility window of ~0.5–0.7 wt% but deliberately exceeds it (1.0–1.2 wt%) to drive primary L12-Al3Zr formation, with local solute trapping reaching ~1.5 wt% Zr under rapid solidification (kimura2021microstructuraldevelopmentand pages 7-9, mehta2023advancingnovelalmncrzr pages 5-7, mehta2023advancingnovelalmncrzr pages 3-5). This upper bound also remains below the bulk Zr levels explored in some Al–Mg–Zr SLM alloys (up to 2.1 wt% Zr), which are feasible but push further into primary-intermetallic-dominated regimes (griffiths2020coarseningandcreep pages 1-2).

### 3) Key failure modes that set each bound

**What sets the 1.0 wt% conservative bound**
- **Porosity / density penalty from additive routes:** In Zr-modified AA7075, Zr additions reduced cracking but increased spherical porosity because unmelted particles degraded melt fluidity and disrupted Marangoni flow; higher energy density was needed to mitigate pores (yu2022processingandcharacterization pages 1-2).
- **Diminishing returns vs cracking for some chemistries:** 0.4 wt% Zr reduced grain size but still allowed cracks; the empirically effective level was ~1 wt% in an Al7050-derived system (mertens2021laserpowderbed pages 3-5).
- **Programmatic/mineral-burden objective:** Even if metallurgically tolerable, increasing Zr beyond ~1 wt% imposes additional mineral-burden penalty without guaranteed performance gains across broad chemistries (not directly evidenced in the retrieved papers; included here as a mission/objective consideration).

**What sets the 1.5 wt% non-conservative bound**
- **Crossing the PBF-LB Zr “solubility/supersaturation” window → primary Al3Zr prevalence:** PBF-LB alloy-design work reports Zr solubility ~0.5–0.7 wt% and shows that higher Zr increases primary L12-Al3Zr volume fraction/area fraction (e.g., 1.42 vol% vs 0.78 vol% in Zr-high vs Zr-low), changing solidification pathways and increasing intermetallic fraction (mehta2023advancingnovelalmncrzr pages 3-5).
- **Chemistry-dependent solidification cracking interactions (not monotonic):** Mg-containing variants reach a lower-temperature Mg-rich eutectic and show increased cracking susceptibility from segregation/secondary phases; one Mg-containing/Zr-low alloy cracked while an Mg-containing/Zr-high alloy did not, implying the boundary is interaction-dependent and risk increases as Zr is pushed high in multi-solute spaces (mehta2023advancingnovelalmncrzr pages 3-5).
- **Embrittlement risk after aging / coarsening behavior:** In Al–4Cr–1.5Zr, peak-aged fracture surfaces showed more brittle characteristics than as-fabricated condition, consistent with precipitation/coarse-phase effects that become more relevant as Zr (and thus Al3Zr) increases (kimura2021microstructuraldevelopmentand pages 7-9).

### 4) Element-specific caveats / interactions to flag for joint-constraints analysis
- **Zr–Mg coupling:** Mg widens the freezing range and promotes low-temperature eutectics/segregation that can increase hot-cracking susceptibility; Zr can counteract via nucleant formation and grain refinement, but the net effect is composition- and process-dependent (mehta2023advancingnovelalmncrzr pages 3-5, mehta2021highperformancealuminium pages 21-24).
- **Zr “dual role” (solute vs primary nucleant) creates a design tension:** Primary Al3Zr formation can refine grains and reduce cracking, but it also consumes Zr that might otherwise remain in supersaturated α-Al for subsequent nano-precipitation strengthening; achieving both effects can require pushing Zr above peritectic/solubility thresholds (croteau2018microstructureandmechanical pages 6-8).
- **Additive route matters (pre-alloyed vs blended elemental):** Elemental/powder-blend Zr additions can introduce unmelted particles and porosity sensitivity (process window tighter), whereas pre-alloyed powders may behave differently (yu2022processingandcharacterization pages 1-2).
- **Model/assessment caveat for CALPHAD + Scheil:** Several studies emphasize nonequilibrium/metastable behavior (solute trapping; metastable L12-Al3Zr) and effective solubility extensions under PBF-LB, which may not be fully captured by equilibrium-focused assessments; treat high-Zr regimes (≥~0.7–1.5 wt%) as higher epistemic-uncertainty zones in TCAl10-based screening (mehta2021highperformancealuminium pages 21-24, mehta2023advancingnovelalmncrzr pages 3-5).

References

1. (glerum2020synthesisofprecipitationstrengthened pages 1-2): Jennifer A. Glerum, Christoph Kenel, Tao Sun, and David C. Dunand. Synthesis of precipitation-strengthened al-sc, al-zr and al-sc-zr alloys via selective laser melting of elemental powder blends. Additive Manufacturing, 36:101461, Dec 2020. URL: https://doi.org/10.1016/j.addma.2020.101461, doi:10.1016/j.addma.2020.101461. This article has 105 citations and is from a highest quality peer-reviewed journal.

2. (mertens2021laserpowderbed pages 1-3): Raya Mertens, Lise Baert, Kim Vanmeensel, and Brecht Van Hooreweder. Laser powder bed fusion of high strength aluminum. Material Design & Processing Communications, Mar 2021. URL: https://doi.org/10.1002/mdp2.161, doi:10.1002/mdp2.161. This article has 23 citations and is from a peer-reviewed journal.

3. (mertens2021laserpowderbed pages 5-7): Raya Mertens, Lise Baert, Kim Vanmeensel, and Brecht Van Hooreweder. Laser powder bed fusion of high strength aluminum. Material Design & Processing Communications, Mar 2021. URL: https://doi.org/10.1002/mdp2.161, doi:10.1002/mdp2.161. This article has 23 citations and is from a peer-reviewed journal.

4. (mertens2021laserpowderbed pages 3-5): Raya Mertens, Lise Baert, Kim Vanmeensel, and Brecht Van Hooreweder. Laser powder bed fusion of high strength aluminum. Material Design & Processing Communications, Mar 2021. URL: https://doi.org/10.1002/mdp2.161, doi:10.1002/mdp2.161. This article has 23 citations and is from a peer-reviewed journal.

5. (yu2022processingandcharacterization pages 2-3): Wenhui Yu, Zhen Xiao, Xuhui Zhang, Yetao Sun, Peng Xue, Shuai Tan, Yongling Wu, and Hongyu Zheng. Processing and characterization of crack-free 7075 aluminum alloys with elemental zr modification by laser powder bed fusion. Materials Science in Additive Manufacturing, 1:4, Mar 2022. URL: https://doi.org/10.18063/msam.v1i1.4, doi:10.18063/msam.v1i1.4. This article has 73 citations and is from a peer-reviewed journal.

6. (mehta2023advancingnovelalmncrzr pages 3-5): Bharat Mehta, Karin Frisk, and Lars Nyborg. Advancing novel al-mn-cr-zr based family of alloys tailored for powder bed fusion-laser beam process. Journal of Alloys and Compounds, 967:171685, Dec 2023. URL: https://doi.org/10.1016/j.jallcom.2023.171685, doi:10.1016/j.jallcom.2023.171685. This article has 14 citations and is from a peer-reviewed journal.

7. (mehta2023advancingnovelalmncrzr pages 5-7): Bharat Mehta, Karin Frisk, and Lars Nyborg. Advancing novel al-mn-cr-zr based family of alloys tailored for powder bed fusion-laser beam process. Journal of Alloys and Compounds, 967:171685, Dec 2023. URL: https://doi.org/10.1016/j.jallcom.2023.171685, doi:10.1016/j.jallcom.2023.171685. This article has 14 citations and is from a peer-reviewed journal.

8. (kimura2021microstructuraldevelopmentand pages 7-9): Takahiro Kimura, Takayuki Nakamoto, Tomoatsu Ozaki, Takao Miki, Isao Murakami, Yoshiki Hashizume, and Akiei Tanaka. Microstructural development and aging behavior of al–cr–zr heat-resistant alloy fabricated using laser powder bed fusion. Journal of Materials Research and Technology, 15:4193-4207, Nov 2021. URL: https://doi.org/10.1016/j.jmrt.2021.10.027, doi:10.1016/j.jmrt.2021.10.027. This article has 39 citations and is from a peer-reviewed journal.

9. (mehta2023advancingnovelalmncrzr pages 1-3): Bharat Mehta, Karin Frisk, and Lars Nyborg. Advancing novel al-mn-cr-zr based family of alloys tailored for powder bed fusion-laser beam process. Journal of Alloys and Compounds, 967:171685, Dec 2023. URL: https://doi.org/10.1016/j.jallcom.2023.171685, doi:10.1016/j.jallcom.2023.171685. This article has 14 citations and is from a peer-reviewed journal.

10. (griffiths2020coarseningandcreep pages 1-2): S. Griffiths, J.R. Croteau, M.D. Rossell, R. Erni, A. De Luca, N.Q. Vo, D.C. Dunand, and C. Leinenbach. Coarsening- and creep resistance of precipitation-strengthened al–mg–zr alloys processed by selective laser melting. Acta Materialia, 188:192-202, Apr 2020. URL: https://doi.org/10.1016/j.actamat.2020.02.008, doi:10.1016/j.actamat.2020.02.008. This article has 155 citations and is from a highest quality peer-reviewed journal.

11. (yu2022processingandcharacterization pages 1-2): Wenhui Yu, Zhen Xiao, Xuhui Zhang, Yetao Sun, Peng Xue, Shuai Tan, Yongling Wu, and Hongyu Zheng. Processing and characterization of crack-free 7075 aluminum alloys with elemental zr modification by laser powder bed fusion. Materials Science in Additive Manufacturing, 1:4, Mar 2022. URL: https://doi.org/10.18063/msam.v1i1.4, doi:10.18063/msam.v1i1.4. This article has 73 citations and is from a peer-reviewed journal.

12. (mehta2021highperformancealuminium pages 21-24): B Mehta. High performance aluminium alloys for laser powder bed fusion: alloy design and development. Unknown journal, 2021.

13. (croteau2018microstructureandmechanical pages 6-8): Joseph R. Croteau, Seth Griffiths, Marta D. Rossell, Christian Leinenbach, Christoph Kenel, Vincent Jansen, David N. Seidman, David C. Dunand, and Nhon Q. Vo. Microstructure and mechanical properties of al-mg-zr alloys processed by selective laser melting. Acta Materialia, 153:35-44, Jul 2018. URL: https://doi.org/10.1016/j.actamat.2018.04.053, doi:10.1016/j.actamat.2018.04.053. This article has 542 citations and is from a highest quality peer-reviewed journal.

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


TASK — Element-specific bound: Zr
Zr is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Zr LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Zr) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Zr) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Zr).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
