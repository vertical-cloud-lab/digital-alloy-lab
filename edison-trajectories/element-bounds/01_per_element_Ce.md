# Phase 1 — Per-element bound: Ce

*Edison task: `73d9e126-4f4e-4db7-8411-e9ad7134e9ac`*

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


TASK — Element-specific bound: Ce
Ce is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Ce LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Ce) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Ce) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Ce).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


### Ce compositional bounds for BOFN / GA inner-solver (wt% Ce)

| Bound category | Bound (wt% Ce) | Primary literature anchor(s) | 1-line justification | Key failure modes that motivate the bound |
|---|---:|---|---|---|
| Conservative Ce upper bound | 10 wt% | Zhou et al. 2020 LPBF Al-10Ce (measured powder/build ~11.8/10.7 wt% Ce); Liu et al. 2024 review of eutectic Al-Ce (~10–12 wt% Ce) (zhou2020laserpowderbed pages 4-7, liu2024reviewoflaser pages 2-4) | 10 wt% is a defensible conservative ceiling because near-eutectic binary Al-Ce at this level has direct LPBF evidence for >99% density and no solidification cracking, while staying at the well-established Al-rich eutectic composition window. | Above the eutectic, risk rises for primary/interconnected Al11Ce3 formation and embrittling Ce-rich networks; even at ~10 wt% porosity appears under overly high energy density/slow scan (keyholing), and Ce’s very low solubility means added Ce rapidly converts to intermetallic fraction rather than benign solid solution (zhou2020laserpowderbed pages 11-12, liu2024reviewoflaser pages 2-4). |
| Non-conservative Ce upper bound | 15 wt% | Yakubov 2022 dissertation compiling successful LPBF Al-15Ce-9Mg and Al-11Ce-7Mg; Hesselmann et al. 2022 near-eutectic Al-Ce with primary Al11Ce3 / Al13CeMg6 context; Liu et al. 2024 on Mg-related LPBF defects (yakubov2022laserpowderbed pages 29-34, hesselmann2022effectofprecipitationforming pages 1-3, liu2024reviewoflaser pages 6-8) | 15 wt% is an aggressive but defensible ceiling because LPBF reports exist for Al-15Ce-9Mg, showing that Ce can be pushed materially above the ~10–12 wt% eutectic in Al-rich ternaries, albeit with much narrower process/composition robustness. | Bound is set by transition toward primary Al11Ce3/intermetallic-dominated solidification, coarse/spiky Ce-rich phases and network embrittlement, plus severe practical defects when Ce is introduced poorly (oxidation to AlCeO3, balling, porosity) and, in Mg-bearing systems, Mg vaporization/keyholing and spherical pores; beyond this level the search space likely becomes increasingly intermetallic-rich and less generically LPBF-robust (yakubov2022laserpowderbed pages 95-99, yakubov2022laserpowderbed pages 113-117, hesselmann2022effectofprecipitationforming pages 1-3, liu2024reviewoflaser pages 6-8). |


*Table: This table summarizes conservative and non-conservative Ce upper bounds for an LPBF Al-alloy search space, anchored to reported LPBF Al-Ce compositions and the main processing/microstructural failure modes that limit further Ce addition.*

#### 1) CONSERVATIVE upper bound: **Ce ≤ 10 wt%**
Near‑eutectic **Al–10Ce** has direct LPBF evidence for high density (>99%) and no solidification cracking across a usable processing window, with measured Ce remaining ~10–11 wt% in powder/build. (zhou2020laserpowderbed pages 4-7)

#### 2) NON‑CONSERVATIVE upper bound: **Ce ≤ 15 wt%**
LPBF literature compiled in Yakubov’s dissertation reports successful fabrication of **Al‑15Ce‑9Mg** (15 wt% Ce), demonstrating that Ce can be pushed materially above the ~10–12 wt% eutectic range in Al‑rich ternaries, albeit with reduced robustness and stronger reliance on powder/process control. (yakubov2022laserpowderbed pages 95-99)

#### 3) Key failure modes that set each bound

**What sets the conservative bound (~10 wt%):**
- **Keyholing/porosity sensitivity at high energy density** even for Al‑10Ce (large pores at slower scan speeds / higher energy density). (zhou2020laserpowderbed pages 11-12, zhou2020laserpowderbed pages 4-7)
- **Intermetallic fraction/network risk grows rapidly with Ce** because Ce solubility in Al is extremely low and Ce partitions to **Al11Ce3**; pushing above eutectic increases risk of primary/interconnected intermetallic morphologies (embrittlement, reduced toughness, and harder-to-print solidification paths). (liu2024reviewoflaser pages 2-4)

**What sets the non‑conservative bound (~15 wt%):**
- **Primary intermetallic / coarse “spikey” Ce-rich phase formation** (e.g., Al11Ce3 and other Ce-bearing intermetallics), which can concentrate at boundaries and increase brittleness and defect sensitivity as Ce rises. (yakubov2022laserpowderbed pages 113-117, yakubov2022laserpowderbed pages 29-34)
- **Powder-handling / atomization practicality (oxidation):** elemental Ce is highly oxidation-prone; Ce-containing oxide films (identified as **AlCeO3**) reduce wettability and promote **balling and high porosity**, lowering relative density in in‑situ blended powders. This becomes a dominant practical constraint at higher Ce if not using pre-alloyed powders. (yakubov2022laserpowderbed pages 95-99)
- **If Mg is co-alloyed (common in high-Ce AM alloys):** Mg vaporization during LPBF drives **keyholing and spherical porosity**, tightening the feasible process window even if Ce itself reduces cracking susceptibility. (liu2024reviewoflaser pages 6-8)

#### 4) Ce-specific caveats / interactions to flag for joint-constraints analysis
- **Ce × powder route:** bounds assume **pre-alloyed/gas-atomized** Ce-containing powder; **elemental Ce blending** can fail due to oxidation/AlCeO3 film formation and balling/porosity, so your acquisition solver should encode a “feedstock route” constraint or penalize powder-blend strategies for Ce. (yakubov2022laserpowderbed pages 95-99)
- **Ce × Mg:** Mg can dominate printability via vaporization/keyholing; for designs with Mg in the several-wt% regime, consider either (i) tighter Ce cap than 15 wt% or (ii) explicit process-parameter constraints (high scan speed / reduced energy density) to maintain density. (liu2024reviewoflaser pages 6-8)
- **Ce × Si:** Ce has strong affinity with Al and Si (Ce-containing phases can form even with minor Si), which can shift eutectic/intermetallic morphologies; treat Ce–Si regions as higher risk for unexpected phase formation/segregation and validate Scheil/phase selection carefully. (yakubov2022laserpowderbed pages 29-34)
- **Ce × Cu:** Ce can form Ce–Cu intermetallics (e.g., Al8CeCu4 cited as a Ce-containing intermetallic), so high Cu with high Ce may accelerate brittle phase accumulation and narrow the printable/ductile region. (yakubov2022laserpowderbed pages 29-34)
- **Mineral-burden objective:** Ce is a rare-earth element; high Ce fractions can incur a mineral-burden penalty compared with more abundant alloying elements, so search-space exploration above the conservative bound should be justified by performance gains. (liu2024reviewoflaser pages 28-29)


References

1. (zhou2020laserpowderbed pages 4-7): Le Zhou, Thinh Huynh, Sharon Park, Holden Hyer, Abhishek Mehta, Shutao Song, Yuanli Bai, Brandon McWilliams, Kyu Cho, and Yongho Sohn. Laser powder bed fusion of al–10 wt% ce alloys: microstructure and tensile property. Journal of Materials Science, 55:14611-14625, Jul 2020. URL: https://doi.org/10.1007/s10853-020-05037-z, doi:10.1007/s10853-020-05037-z. This article has 116 citations and is from a peer-reviewed journal.

2. (liu2024reviewoflaser pages 2-4): Yuanfan Liu, Yang Li, Mingliang Wang, and Zhe Chen. Review of laser powder bed fusion’s microstructure and mechanical characteristics for al-ce alloys. Materials, 17:5085, Oct 2024. URL: https://doi.org/10.3390/ma17205085, doi:10.3390/ma17205085. This article has 6 citations.

3. (zhou2020laserpowderbed pages 11-12): Le Zhou, Thinh Huynh, Sharon Park, Holden Hyer, Abhishek Mehta, Shutao Song, Yuanli Bai, Brandon McWilliams, Kyu Cho, and Yongho Sohn. Laser powder bed fusion of al–10 wt% ce alloys: microstructure and tensile property. Journal of Materials Science, 55:14611-14625, Jul 2020. URL: https://doi.org/10.1007/s10853-020-05037-z, doi:10.1007/s10853-020-05037-z. This article has 116 citations and is from a peer-reviewed journal.

4. (yakubov2022laserpowderbed pages 29-34): Vladislav Yakubov. Laser powder bed fusion fabrication of cerium-containing aluminium alloys: solidification behaviour, microstructure evolution and mechanical properties. Dissertation, Jan 2022. URL: https://doi.org/10.26190/unsworks/24548, doi:10.26190/unsworks/24548. This article has 0 citations.

5. (hesselmann2022effectofprecipitationforming pages 1-3): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Additive Manufacturing, 57:102959, Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 24 citations and is from a highest quality peer-reviewed journal.

6. (liu2024reviewoflaser pages 6-8): Yuanfan Liu, Yang Li, Mingliang Wang, and Zhe Chen. Review of laser powder bed fusion’s microstructure and mechanical characteristics for al-ce alloys. Materials, 17:5085, Oct 2024. URL: https://doi.org/10.3390/ma17205085, doi:10.3390/ma17205085. This article has 6 citations.

7. (yakubov2022laserpowderbed pages 95-99): Vladislav Yakubov. Laser powder bed fusion fabrication of cerium-containing aluminium alloys: solidification behaviour, microstructure evolution and mechanical properties. Dissertation, Jan 2022. URL: https://doi.org/10.26190/unsworks/24548, doi:10.26190/unsworks/24548. This article has 0 citations.

8. (yakubov2022laserpowderbed pages 113-117): Vladislav Yakubov. Laser powder bed fusion fabrication of cerium-containing aluminium alloys: solidification behaviour, microstructure evolution and mechanical properties. Dissertation, Jan 2022. URL: https://doi.org/10.26190/unsworks/24548, doi:10.26190/unsworks/24548. This article has 0 citations.

9. (liu2024reviewoflaser pages 28-29): Yuanfan Liu, Yang Li, Mingliang Wang, and Zhe Chen. Review of laser powder bed fusion’s microstructure and mechanical characteristics for al-ce alloys. Materials, 17:5085, Oct 2024. URL: https://doi.org/10.3390/ma17205085, doi:10.3390/ma17205085. This article has 6 citations.

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


TASK — Element-specific bound: Ce
Ce is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Ce LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Ce) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Ce) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Ce).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
