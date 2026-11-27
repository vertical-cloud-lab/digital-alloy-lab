# Phase 1 — Per-element bound: Fe

*Edison task: `4bc97047-8a4f-4cc4-8798-f81e8ce49990`*

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


TASK — Element-specific bound: Fe
Fe is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Fe LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Fe) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Fe) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Fe).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Element-specific Fe upper bounds for BOFN search space (Al-rich LPBF alloys)

### 1) CONSERVATIVE Fe upper bound (wt%)
**Fe ≤ 0.10 wt%**.
Commercial LPBF AlSi10Mg feedstock is commonly supplied with very low Fe; Böhm et al. report a commercial AlSi10Mg (EN AC-43000) powder used for LPBF with **Fe = 0.10 wt%** (supplier composition in Table 1). This level is consistent with keeping Fe largely as a trace impurity to avoid deleterious Fe-rich intermetallics and property scatter in Al-Si(-Mg) LPBF alloys. (bohm2020dilutionratioand pages 1-3, bohm2020dilutionratioand media 07f52da1)

### 2) NON-CONSERVATIVE Fe upper bound (wt%)
**Fe ≤ 5.0 wt%**.
Multiple LPBF/SLM studies demonstrate feasibility of Al-rich alloys with Fe at a few wt%: (i) Yamasaki et al. add Fe to a heat-resistant Al alloy up to **5.0 wt% Fe** (“Base + 5Fe”) and report improved high-temperature strength and good ductility in the rapidly solidified SLM condition, contrasting with coarse β-Al5FeSi issues under slow cooling. (ii) Pérez‑Prado et al. successfully fabricate dense LPBF parts from **Al–5Fe–6Cr (wt%)** powder with **99.8% relative density**, showing that ~5 wt% Fe can be processable when coupled with suitable co-alloying (here Cr) and LPBF processing. (yamasaki2019effectoffe pages 1-3, perezprado2022anal5fe6cralloy pages 1-2)

### 3) Key failure modes setting each bound

**At/above conservative bound (~0.10 wt% Fe):**
- **Fe-rich intermetallic embrittlement risk (trace-control regime):** Even small Fe increases in Al-Si(-Mg) systems can promote Fe-intermetallics during solidification/heat treatment; keeping Fe at ~0.1 wt% aligns with common commercial LPBF powders and minimizes sensitivity to powder-lot variability. (bohm2020dilutionratioand pages 1-3, bohm2020dilutionratioand media 07f52da1)
- **Corrosion/fatigue scatter from intermetallic particles:** Fe-bearing particles can act as initiation sites; conservative Fe reduces this risk (general LPBF qualification practice implied by use of low-Fe commercial powders). (bohm2020dilutionratioand pages 1-3)

**At/above non-conservative bound (~5 wt% Fe):**
- **Solidification cracking / brittle phase networks:** In high-Fe Al–Fe alloys, brittle θ-Al13Fe4 decorating melt-pool boundaries is associated with macroscopic cracking and a very narrow processing window (demonstrated strongly at Al–15%Fe). This motivates keeping the aggressive Fe cap well below the clearly problematic hypereutectic regime, despite some crack-free processing being possible there. (wang2021processabilityandoptimization pages 1-2)
- **Primary intermetallic formation & loss of ductility:** Equilibrium Fe solubility in α-Al is extremely low and Fe additions promote intermetallic formation; without careful co-alloying and rapid solidification control, toughness/ductility can degrade. (qi2020laserpowderbed pages 1-2, yamasaki2019effectoffe pages 1-3)
- **Process window shrinkage / sensitivity to LPBF parameters:** High Fe increases likelihood that small changes in P–v–h–t lead to cracks/defects (shown for Al–15%Fe). (wang2021processabilityandoptimization pages 1-2)

Mineral-burden note: Fe is generally low criticality/import reliance relative to many palette elements; thus Fe itself is unlikely to be penalized strongly by the mineral-burden objective compared with, e.g., Sc/Er/Ce (not directly evidenced in retrieved sources). 

### 4) Element-specific caveats & interactions for follow-up joint-constraints analysis
- **Strong interactions with Si (and Ni) in Al alloys:** Prior practice and Yamasaki et al. discussion emphasize that slow cooling can form coarse **β-Al5FeSi** (brittle) in Fe-bearing Al alloys, while rapid solidification (SLM/LPBF) can instead produce finer Fe-containing dispersoids with better ductility/high-T strength; thus Fe bounds should be coupled to constraints on Si/Ni and solidification metrics (Scheil freezing range, eutectic fraction). (yamasaki2019effectoffe pages 1-3)
- **Fe with Cr/Mn can change phase selection and morphology:** Demonstrated by dense LPBF of **Al–5Fe–6Cr**, suggesting that if Fe is pushed above ~1–2 wt%, co-alloying with transition metals (Cr, Mn, possibly Zr) may be important to avoid deleterious Fe-phase morphologies and to maintain printability. (perezprado2022anal5fe6cralloy pages 1-2)
- **CALPHAD/TCAl10 applicability in high-order, high-Fe corners:** Even if LPBF can process ~5 wt% Fe in some systems, joint searches up to ~9 components may exceed well-assessed TCAl10 composition subspaces for multicomponent Fe intermetallics; consider adding a “TCAl10 assessment coverage” or “phase-description confidence” penalty when Fe is high and multiple transition elements are simultaneously high (not directly evidenced here, but consistent with the project’s stated database-trust rationale).

**Recommended BOFN implementation detail:** treat Fe as a *two-tier* bound depending on whether the candidate is in a “commercial-like AlSi/AlMg” region (cap 0.1 wt%) vs. a “high-temperature transition-metal Al alloy” region (allow up to 5 wt% with additional constraints on cracking susceptibility / intermetallic fraction). (yamasaki2019effectoffe pages 1-3, perezprado2022anal5fe6cralloy pages 1-2, wang2021processabilityandoptimization pages 1-2)

References

1. (bohm2020dilutionratioand pages 1-3): Constantin Böhm, Martin Werz, and Stefan Weihe. Dilution ratio and the resulting composition profile in dissimilar laser powder bed fusion of alsi10mg and al99.8. Metals, 10:1222, Sep 2020. URL: https://doi.org/10.3390/met10091222, doi:10.3390/met10091222. This article has 10 citations.

2. (bohm2020dilutionratioand media 07f52da1): Constantin Böhm, Martin Werz, and Stefan Weihe. Dilution ratio and the resulting composition profile in dissimilar laser powder bed fusion of alsi10mg and al99.8. Metals, 10:1222, Sep 2020. URL: https://doi.org/10.3390/met10091222, doi:10.3390/met10091222. This article has 10 citations.

3. (yamasaki2019effectoffe pages 1-3): Shigeto Yamasaki, Tomo Okuhira, Masatoshi Mitsuhara, Hideharu Nakashima, Jun Kusui, and Mitsuru Adachi. Effect of fe addition on heat-resistant aluminum alloys produced by selective laser melting. Metals, 9:468, Apr 2019. URL: https://doi.org/10.3390/met9040468, doi:10.3390/met9040468. This article has 39 citations.

4. (perezprado2022anal5fe6cralloy pages 1-2): M.T. Pérez-Prado, A. Martin, D.F. Shi, S. Milenkovic, and C.M. Cepeda-Jiménez. An al-5fe-6cr alloy with outstanding high temperature mechanical behavior by laser powder bed fusion. Additive Manufacturing, 55:102828, Jul 2022. URL: https://doi.org/10.1016/j.addma.2022.102828, doi:10.1016/j.addma.2022.102828. This article has 64 citations and is from a highest quality peer-reviewed journal.

5. (wang2021processabilityandoptimization pages 1-2): Wenyuan Wang, Naoki Takata, Asuka Suzuki, Makoto Kobashi, and Masaki Kato. Processability and optimization of laser parameters for densification of hypereutectic al–fe binary alloy manufactured by laser powder bed fusion. ArXiv, 11:320, Mar 2021. URL: https://doi.org/10.3390/cryst11030320, doi:10.3390/cryst11030320. This article has 16 citations.

6. (qi2020laserpowderbed pages 1-2): Xing Qi, Naoki Takata, Asuka Suzuki, Makoto Kobashi, and Masaki Kato. Laser powder bed fusion of a near-eutectic al–fe binary alloy: processing and microstructure. Additive Manufacturing, 35:101308, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101308, doi:10.1016/j.addma.2020.101308. This article has 101 citations and is from a highest quality peer-reviewed journal.

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


TASK — Element-specific bound: Fe
Fe is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Fe LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Fe) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Fe) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Fe).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
