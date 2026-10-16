# Phase 1 — Per-element bound: Zn

*Edison task: `b42d3e02-4b02-4ac0-871a-dba383d4e49f`*

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


TASK — Element-specific bound: Zn
Zn is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Zn LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Zn) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Zn) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Zn).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Element: Zn — proposed BOFN upper bounds (wt%)

The bounds below are intended for an **Al-rich LPBF** search space, where feasibility is primarily limited by (i) **Zn volatility/evaporation** and (ii) **7xxx-type hot cracking** driven by wide solidification interval and grain-boundary liquid-film rupture.

| Bound type | Proposed Zn upper bound (wt%) | Evidence basis (specific alloys/studies and Zn wt% in powder and/or built) | Main mechanism limiting |
|---|---:|---|---|
| Conservative | 6.5 | Mertens et al. LPBF study used Al7050 baseline with 5.7–6.7 wt% Zn; this is essentially the conventional 7050/7075 Zn regime and already sits near the practical LPBF limit before severe cracking/evaporation countermeasures become necessary. Stopyra et al. showed AA7075 can reach high density but still suffers persistent hot cracking. (mertens2021laserpowderbed pages 1-3, mertens2021laserpowderbed media 1852a3dc, stopyra2020laserpowderbed pages 1-6) | Hot cracking from wide solidification interval and intergranular liquid-film rupture; Zn evaporation/loss becomes nontrivial even in conventional 7xxx chemistry. |
| Non-conservative | 14.5 | Babu et al. explicitly designed LPBF Al-10Zn-2Mg, Al-14Zn-3Mg, and Al-18Zn-4Mg high-solute alloys; separate corrosion study measured 14.7 wt% Zn in Al-14Zn-3Mg powder and 10.9 wt% Zn after LPBF, demonstrating that ~14–15 wt% Zn feedstock is printable but already incurs major Zn loss. Mertens et al. also used ~12.3 wt% Zn feedstock to compensate Zn evaporation. (babu2020laserpowderbed pages 1-2, babu2021onthecorrosion pages 1-2, mertens2021laserpowderbed pages 1-3, mertens2021laserpowderbed media 1852a3dc) | Strong Zn volatility/evaporation causing composition drift, smoke/spatter/porosity and local cracking; at still higher Zn (toward 18 wt%) risk of severe hot cracking, segregation, and loss of robust process window rises sharply. |


*Table: This table summarizes conservative and non-conservative Zn upper bounds for Al-rich LPBF alloy search, tied to published LPBF Al-Zn studies and the mechanisms that practically limit Zn content. It is useful for setting BOFN inner-solver bounds that distinguish near-qualified chemistry from more aggressive exploratory high-solute space.*

### 1) CONSERVATIVE upper bound (Zn)
**Zn ≤ 6.5 wt%**.  
This matches the conventional Zn range of **Al7050 (5.7–6.7 wt% Zn)** used as a baseline in an LPBF study, representing a defensible “commercial 7xxx chemistry” regime before extreme Zn-loss compensation becomes necessary. (mertens2021laserpowderbed media 1852a3dc, mertens2021laserpowderbed pages 1-3)

### 2) NON-CONSERVATIVE upper bound (Zn)
**Zn ≤ 14.5 wt%**.  
LPBF has been demonstrated on **high-solute Al–Zn–Mg** alloys at/near this level: an Al-14Zn-3Mg study measured **14.7 wt% Zn in the powder** and **10.9 wt% Zn after LPBF**, evidencing that ~14–15 wt% Zn feedstock can be processed but incurs substantial Zn loss and heightened defect risk. (babu2021onthecorrosion pages 1-2)

### 3) Key failure modes setting each bound

**Conservative bound (~6.5 wt% Zn):**
- **Hot (solidification) cracking in 7xxx alloys** driven by wide solidification interval and intergranular liquid-film rupture along columnar grain boundaries; observed even when high density is achieved in AA7075 LPBF. (stopyra2020laserpowderbed pages 1-6)
- **Zn evaporation / composition drift** (Zn has low boiling point; preferential evaporation) causing spatter/porosity and reducing strengthening response; motivates staying near conventional Zn levels unless explicitly compensating. (mauduit2017studyofthe pages 19-20, mertens2021laserpowderbed pages 1-3)

**Non-conservative bound (~14.5 wt% Zn):**
- **Strong Zn volatility** → large Zn loss between powder and build (quantified in Al-14Zn-3Mg), with associated composition gradients that can couple to cracking/porosity. (babu2021onthecorrosion pages 1-2)
- **Evaporation-driven porosity and process instabilities** (smoke/spatter, keyhole destabilization) that shrink the viable LPBF process window as Zn increases. (meng2024researchprogresson pages 6-8)
- **Enhanced microsegregation + wide freezing range effects** (general 7xxx behavior): promotes grain-boundary liquid films and cracking; the higher the solute loading, the more aggressive the mitigation required (grain refinement, eutectic engineering). (stopyra2020laserpowderbed pages 1-6, kvvssn2025recentprogressin pages 27-28)

### 4) Element-specific caveats / interactions for joint-constraints analysis
- **Zn–Mg coupling (Zn:Mg ratio):** Zn and Mg both evaporate; studies explicitly add excess Zn to maintain ratios needed for precipitation strengthening after LPBF, implying Zn bounds should be analyzed jointly with Mg and with expected evaporation losses. (mertens2021laserpowderbed pages 1-3, babu2021developmentofhigh pages 74-74)
- **Si interaction (crack mitigation but also sensitivity):** Si additions (~2–4 wt% in literature) can reduce cracking by narrowing the solidification range and improving fluidity/backfilling cracks, but Si (even as impurity in 7075) can also influence grain-boundary liquid film stability; treat Si as a coupled variable rather than independent. (wang2020selectivelasermelting pages 35-37, stopyra2020laserpowderbed pages 1-6, aversa2022laserpowderbed pages 1-3)
- **Zr as a key enabler at higher Zn:** Grain refinement via Zr/Al3Zr heterogeneous nucleation is repeatedly used to mitigate cracking in Zn-bearing LPBF alloys; high-Zn regions of the search space should likely require minimum Zr (or equivalent inoculant strategy) as a soft/hard constraint. (wang2020selectivelasermelting pages 35-37, aversa2022laserpowderbed pages 1-3, mertens2021laserpowderbed pages 1-3)
- **Expect Zn loss to be process-dependent:** Evaporation loss depends on energy density/melt mode and can be several wt% in reports; incorporate a “powder→build composition transfer function” (or uncertainty) when scoring CALPHAD/Scheil outputs. (wang2020selectivelasermelting pages 35-37, babu2021onthecorrosion pages 1-2)


References

1. (mertens2021laserpowderbed pages 1-3): Raya Mertens, Lise Baert, Kim Vanmeensel, and Brecht Van Hooreweder. Laser powder bed fusion of high strength aluminum. Material Design & Processing Communications, Mar 2021. URL: https://doi.org/10.1002/mdp2.161, doi:10.1002/mdp2.161. This article has 23 citations and is from a peer-reviewed journal.

2. (mertens2021laserpowderbed media 1852a3dc): Raya Mertens, Lise Baert, Kim Vanmeensel, and Brecht Van Hooreweder. Laser powder bed fusion of high strength aluminum. Material Design & Processing Communications, Mar 2021. URL: https://doi.org/10.1002/mdp2.161, doi:10.1002/mdp2.161. This article has 23 citations and is from a peer-reviewed journal.

3. (stopyra2020laserpowderbed pages 1-6): Wojciech Stopyra, Konrad Gruber, Irina Smolina, Tomasz Kurzynowski, and Bogumiła Kuźnicka. Laser powder bed fusion of aa7075 alloy: influence of process parameters on porosity and hot cracking. Additive manufacturing, 35:101270, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101270, doi:10.1016/j.addma.2020.101270. This article has 309 citations and is from a highest quality peer-reviewed journal.

4. (babu2020laserpowderbed pages 1-2): A.P. Babu, S.K. Kairy, A. Huang, and N. Birbilis. Laser powder bed fusion of high solute al-zn-mg alloys: processing, characterisation and properties. Materials & Design, 196:109183, Nov 2020. URL: https://doi.org/10.1016/j.matdes.2020.109183, doi:10.1016/j.matdes.2020.109183. This article has 40 citations and is from a highest quality peer-reviewed journal.

5. (babu2021onthecorrosion pages 1-2): A.P. Babu, S. Choudhary, J.C. Griffith, A. Huang, and N. Birbilis. On the corrosion of a high solute al-zn-mg alloy produced by laser powder bed fusion. Corrosion Science, 189:109626, Aug 2021. URL: https://doi.org/10.1016/j.corsci.2021.109626, doi:10.1016/j.corsci.2021.109626. This article has 69 citations and is from a highest quality peer-reviewed journal.

6. (mauduit2017studyofthe pages 19-20): A Mauduit, S Pillot, and H Gransac. Study of the suitability of aluminum alloys for additive manufacturing by laser powder bed fusion. Unknown journal, 2017.

7. (meng2024researchprogresson pages 6-8): Fuxiang Meng and Yulei Du. Research progress on laser powder bed fusion additive manufacturing of zinc alloys. Materials, 17:4309, Aug 2024. URL: https://doi.org/10.3390/ma17174309, doi:10.3390/ma17174309. This article has 11 citations.

8. (kvvssn2025recentprogressin pages 27-28): Varma Kvvssn, Muhammad Muteeb Butt, Hossein Laieghi, Zia Uddin, Elmas Salamci, Duck Bong Kim, and Hüseyin Kizil. Recent progress in additive manufacturing of 7xxx aluminum alloys. The International Journal of Advanced Manufacturing Technology, 137:4353-4399, Mar 2025. URL: https://doi.org/10.1007/s00170-025-15415-z, doi:10.1007/s00170-025-15415-z. This article has 26 citations.

9. (babu2021developmentofhigh pages 74-74): ABIRAMI PRIYADARSHINI BABU. Development of high solute aluminium alloys in net shape through additive manufacturing. ArXiv, Sep 2021. URL: https://doi.org/10.26180/16552485.v1, doi:10.26180/16552485.v1. This article has 0 citations.

10. (wang2020selectivelasermelting pages 35-37): Zhi Wang, Raghunandan Ummethala, Neera Singh, Shengyang Tang, Challapalli Suryanarayana, Jürgen Eckert, and Konda Gokuldoss Prashanth. Selective laser melting of aluminum and its alloys. Materials, 13:4564, Oct 2020. URL: https://doi.org/10.3390/ma13204564, doi:10.3390/ma13204564. This article has 136 citations.

11. (aversa2022laserpowderbed pages 1-3): Alberta Aversa, Giulio Marchese, Diego Manfredi, Massimo Lorusso, Flaviana Calignano, Sara Biamino, Mariangela Lombardi, Paolo Fino, and Matteo Pavese. Laser powder bed fusion of a high strength al-si-zn-mg-cu alloy. ArXiv, 8:300, Apr 2018. URL: https://doi.org/10.3390/met8050300, doi:10.3390/met8050300. This article has 67 citations.

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


TASK — Element-specific bound: Zn
Zn is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Zn LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Zn) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Zn) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Zn).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
