# Phase 1 — Per-element bound: Si

*Edison task: `792b16bb-4708-4933-a5ac-674d40a10e1c`*

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


TASK — Element-specific bound: Si
Si is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Si LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Si) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Si) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Si).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Element-specific compositional bound (Si, wt%) for Al-rich LPBF BOFN space

### 1) CONSERVATIVE upper bound: **Si ≤ 11 wt%**
AlSi10Mg (DIN EN 1706 / EN AC-43000) is the dominant commercial LPBF Al powder, with a specified silicon range of **9–11 wt% Si** (and typical measured powders ≈9.8–10.3 wt% Si). (kreitcberg2025effectoftemperature media 164b1d91, bohm2020dilutionratioand pages 1-3, wang2021effectofinput pages 2-3, kreitcberg2025effectoftemperature pages 2-5)

### 2) NON-CONSERVATIVE upper bound: **Si ≤ 15 wt%**
The Al–Si eutectic is near **≈12 wt% Si**, and LPBF/SLM literature includes AlSi12 and also higher-Si alloys (e.g., AlSi18/20) and even much higher-Si hypereutectic builds, demonstrating that Si above 11 wt% can be processed when energy input/melt-pool control are adequate; setting **15 wt%** is an aggressive but still Al-rich limit (keeps Al ≥85 wt%) that extends moderately beyond eutectic while remaining plausible for LPBF exploration. (brock2020laserpowderbed pages 28-32, hanemann2019insitualloyingof pages 1-3)

### 3) Key failure modes that set each bound

**Conservative bound (~11 wt% Si)** is set by:
- **Qualification / printability envelope:** anchored to an established LPBF alloy standard (EN AC-43000 AlSi10Mg at 9–11 wt% Si). (kreitcberg2025effectoftemperature media 164b1d91, kreitcberg2025effectoftemperature pages 2-5)
- **Hot/solidification cracking risk management:** hot cracks are highlighted as dominant LPBF process errors in Al alloy combinations; staying within the widely used AlSi10Mg range is a risk-minimizing choice. (bohm2020dilutionratioand pages 1-3)

**Non-conservative bound (~15 wt% Si)** is set by:
- **Transition across/above eutectic:** above ≈12 wt% Si, microstructures trend hypereutectic with primary Si; coarser/brittle primary Si is associated with cracking/ductility loss in general, motivating a moderate extension rather than very high Si in an Al-rich search. (brock2020laserpowderbed pages 28-32, risse2023microstructureandmechanical pages 1-2)
- **Porosity sensitivity to process window:** higher-Si (and/or Si-enriched) LPBF/SLM is prone to lack-of-fusion porosity with unmelted particles at low energy and pore formation at high-power/low-speed regimes; this tightens the viable parameter window. (hanemann2019insitualloyingof pages 3-6)
- **Al vaporization → effective Si enrichment:** at excessive energy input, Al can boil/vaporize, increasing measured Si fraction (e.g., ~16→22 wt% in one SLM study) and promoting balling/dross and degraded density/properties. (kang2016wearbehaviorand pages 8-13)

### 4) Si-specific caveats / interactions for follow-on joint-constraints
- **Mg interaction (Mg2Si):** in Al–Si–Mg systems, Si availability controls Mg2Si precipitation/age-hardening response; bounds on Si should be considered jointly with Mg for target strength/ductility and heat-treatment strategy (and for CALPHAD/Scheil phase fraction constraints). (brock2020laserpowderbed pages 28-32)
- **Powder blending / in-situ alloying:** when achieving higher Si via Si additions, incomplete melting and inhomogeneous Si distribution (unmolten Si particles) can occur, implying a coupled constraint with LPBF energy density, scan strategy, and atomization/powder-mix approach. (hanemann2019insitualloyingof pages 1-3, hanemann2019insitualloyingof pages 3-6)
- **Process–chemistry coupling:** the same nominal Si can behave differently depending on whether Al vaporization occurs (raising *effective* Si) and on melt-pool mode (conduction vs keyhole), so composition bounds should be paired with process constraints that avoid vaporization/keyholing regimes. (kang2016wearbehaviorand pages 8-13, brock2020laserpowderbed pages 28-32)
- **TCAl10 validity / model trust region:** if Al is constrained to be ≥85 wt% for CALPHAD extrapolation trust, then Si ≤15 wt% is a hard coupled constraint with the total non-Al sum; higher-Si hypereutectic LPBF literature (e.g., ≥25 wt% Si) is informative on mechanisms but is outside the Al-rich BOFN region by design. (risse2023microstructureandmechanical pages 12-13)
- **Mineral-burden objective:** Si is generally not a USGS “critical mineral” driver compared with rare earths/Sc/etc.; thus Si bounds are more likely governed by printability/solidification behavior than mineral burden (flag for your separate criticality scoring).


References

1. (kreitcberg2025effectoftemperature media 164b1d91): Alena Kreitcberg, Mohamed Khaled Trigui, Abdelberi Chandoul, Roger Pelletier, and Vincent Demers. Effect of temperature, heating rate, and cooling rate on bonding and nitriding of alsi10mg powder occurring during supersolidus liquid-phase sintering. Journal of Manufacturing and Materials Processing, 9:296, Sep 2025. URL: https://doi.org/10.3390/jmmp9090296, doi:10.3390/jmmp9090296. This article has 1 citations.

2. (bohm2020dilutionratioand pages 1-3): Constantin Böhm, Martin Werz, and Stefan Weihe. Dilution ratio and the resulting composition profile in dissimilar laser powder bed fusion of alsi10mg and al99.8. Metals, 10:1222, Sep 2020. URL: https://doi.org/10.3390/met10091222, doi:10.3390/met10091222. This article has 10 citations.

3. (wang2021effectofinput pages 2-3): Pusong Wang, Adib Salandari-Rabori, Qingshan Dong, and Vahid Fallah. Effect of input powder attributes on optimized processing and as-built tensile properties in laser powder bed fusion of alsi10mg alloy. Journal of Manufacturing Processes, 64:633-647, Apr 2021. URL: https://doi.org/10.1016/j.jmapro.2021.02.024, doi:10.1016/j.jmapro.2021.02.024. This article has 26 citations and is from a peer-reviewed journal.

4. (kreitcberg2025effectoftemperature pages 2-5): Alena Kreitcberg, Mohamed Khaled Trigui, Abdelberi Chandoul, Roger Pelletier, and Vincent Demers. Effect of temperature, heating rate, and cooling rate on bonding and nitriding of alsi10mg powder occurring during supersolidus liquid-phase sintering. Journal of Manufacturing and Materials Processing, 9:296, Sep 2025. URL: https://doi.org/10.3390/jmmp9090296, doi:10.3390/jmmp9090296. This article has 1 citations.

5. (brock2020laserpowderbed pages 28-32): L Brock. Laser powder bed fusion of alsi10mg for fabrication of fluid power components. Unknown journal, 2020.

6. (hanemann2019insitualloyingof pages 1-3): Theresa Hanemann, Luke N. Carter, Moritz Habschied, Nicholas J.E. Adkins, Moataz M. Attallah, and Martin Heilmaier. In-situ alloying of alsi10mg+si using selective laser melting to control the coefficient of thermal expansion. Journal of Alloys and Compounds, Jul 2019. URL: https://doi.org/10.1016/j.jallcom.2019.04.260, doi:10.1016/j.jallcom.2019.04.260. This article has 51 citations and is from a peer-reviewed journal.

7. (risse2023microstructureandmechanical pages 1-2): Jan Henning Risse, Matthias Trempa, Florian Huber, Heinz Werner Höppel, Dominic Bartels, Michael Schmidt, Christian Reimann, and Jochen Friedrich. Microstructure and mechanical properties of hypereutectic al-high si alloys up to 70 wt.% si-content produced from pre-alloyed and blended powder via laser powder bed fusion. Materials, 16:657, Jan 2023. URL: https://doi.org/10.3390/ma16020657, doi:10.3390/ma16020657. This article has 19 citations.

8. (hanemann2019insitualloyingof pages 3-6): Theresa Hanemann, Luke N. Carter, Moritz Habschied, Nicholas J.E. Adkins, Moataz M. Attallah, and Martin Heilmaier. In-situ alloying of alsi10mg+si using selective laser melting to control the coefficient of thermal expansion. Journal of Alloys and Compounds, Jul 2019. URL: https://doi.org/10.1016/j.jallcom.2019.04.260, doi:10.1016/j.jallcom.2019.04.260. This article has 51 citations and is from a peer-reviewed journal.

9. (kang2016wearbehaviorand pages 8-13): Nan Kang, Pierre Coddet, Hanlin Liao, Tiphaine Baur, and Christian Coddet. Wear behavior and microstructure of hypereutectic al-si alloys prepared by selective laser melting. Applied Surface Science, 378:142-149, Aug 2016. URL: https://doi.org/10.1016/j.apsusc.2016.03.221, doi:10.1016/j.apsusc.2016.03.221. This article has 215 citations and is from a domain leading peer-reviewed journal.

10. (risse2023microstructureandmechanical pages 12-13): Jan Henning Risse, Matthias Trempa, Florian Huber, Heinz Werner Höppel, Dominic Bartels, Michael Schmidt, Christian Reimann, and Jochen Friedrich. Microstructure and mechanical properties of hypereutectic al-high si alloys up to 70 wt.% si-content produced from pre-alloyed and blended powder via laser powder bed fusion. Materials, 16:657, Jan 2023. URL: https://doi.org/10.3390/ma16020657, doi:10.3390/ma16020657. This article has 19 citations.

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


TASK — Element-specific bound: Si
Si is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Si LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Si) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Si) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Si).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
