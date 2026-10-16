# Phase 1 — Per-element bound: Cr

*Edison task: `ff7dbd72-632d-4ec9-9cf6-f760d214c51e`*

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


TASK — Element-specific bound: Cr
Cr is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Cr LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Cr) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Cr) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Cr).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Element-specific compositional bounds (wt%) for Cr in Al-rich LPBF alloys

### 1) CONSERVATIVE upper bound: **Cr ≤ 0.30 wt%**
A defensible conservative cap is ~0.30 wt% Cr, consistent with commercial wrought AA7075 powder used in LPBF studies (measured Cr = 0.25 wt%, with an ISO range 0.18–0.28 wt% reported alongside the measurement). This keeps Cr at levels already present in widely studied LPBF feedstocks without intentionally pushing into high-transition-metal alloy regimes. (stopyra2020laserpowderbed pages 9-13, stopyra2020laserpowderbed media afe4449f)

### 2) NON-CONSERVATIVE upper bound: **Cr ≤ 6.0 wt%**
A defensible aggressive cap is ~6 wt% Cr, supported by published LPBF processing of an Al-5Fe-6Cr (wt%) alloy that achieved dense builds (~99.8% relative density) after parameter optimization and delivered high-temperature strength attributed to nanoscale intermetallic/i-phase precipitation. This bound is also consistent with Al–Cr–Zr LPBF work at **4 wt% Cr** (Al–4Cr–1.5Zr) demonstrating atomizable powder and LPBF feasibility, indicating that multi-wt% Cr additions can be viable in Al-rich LPBF when the alloy is intentionally designed for it. (kimura2021microstructuraldevelopmentand pages 16-17, kimura2021microstructuraldevelopmentand pages 1-3)

### 3) Key failure modes setting each bound

**Conservative bound (~0.30 wt% Cr):**
- **Avoidance of primary Al–Cr intermetallics / embrittlement risk:** staying near trace-to-minor Cr levels reduces likelihood of forming significant fractions of brittle Al–Cr compounds during solidification/heat treatment.
- **Maintain broad densification/process window:** high-alloy-content Al systems can show **limited process windows for densification**; conservative Cr avoids entering that regime. (kimura2021microstructuraldevelopmentand pages 14-16)
- **CALPHAD extrapolation conservatism / model trust:** lower Cr reduces reliance on higher-order extrapolations and reduces sensitivity to poorly assessed multicomponent Al–Cr interactions.

**Non-conservative bound (~6 wt% Cr):**
- **Narrowed LPBF process window / densification sensitivity:** literature notes high-alloy-content Al often has poorer PBF processability (limited densification window). (kimura2021microstructuraldevelopmentand pages 14-16)
- **Primary intermetallic formation during solidification:** Scheil predictions in Al–4Cr–1.5Zr indicate formation of **Al5Cr and Al7Cr** (β) and possible coarse intermetallics (coarse phase attributed to Al7Cr with substitutions), which can degrade ductility and increase cracking/defect sensitivity if not controlled. (kimura2021microstructuraldevelopmentand pages 7-9)
- **Hot-cracking / anisotropy risk via grain structure:** coarse/textured columnar grains can drive hot-cracking and anisotropic properties; high-alloy systems are explicitly discussed as susceptible unless alloy design promotes favorable grain structures. (kimura2021microstructuraldevelopmentand pages 14-16)
- **Powder production constraints:** Al–4Cr–1.5Zr was explicitly selected to keep solute levels within what can be produced by “general gas-atomizing equipment,” implying that pushing beyond multi-wt% Cr may become a feedstock manufacturability risk (yield, satellites, oxygen pickup, cost). (kimura2021microstructuraldevelopmentand pages 1-3)
- **Mineral-burden objective (project-specific):** Cr is not on the provided “critical” palette list, but increased Cr will still incur mass-based penalty if your objective weights overall import reliance/criticality; treat as a scalar cost term rather than a hard feasibility limit.

### 4) Element-specific caveats / interactions for follow-up joint-constraints
- **Cr–Zr coupling (designed HT alloys):** In Al–4Cr–1.5Zr, Zr (via primary/secondary Al3Zr) is used to enable strengthening and influences grain structure; Cr participates in forming Al–Cr compounds under Scheil solidification. If exploring Cr > ~1 wt%, consider co-varying Zr (and/or other grain refiners) rather than treating Cr independently. (kimura2021microstructuraldevelopmentand pages 1-3, kimura2021microstructuraldevelopmentand pages 7-9)
- **Cr solubility vs rapid solidification:** Equilibrium maximum solubility of Cr in Al is reported as **~0.77 mass%**, but LPBF cooling (10^5–10^6 K/s) can trap/supersaturate Cr beyond equilibrium; this can be beneficial for strengthening but may also promote later precipitation/coarsening and brittleness depending on thermal history. (kimura2021microstructuraldevelopmentand pages 7-9)
- **Cr with Fe (Al–Fe–Cr families):** The successful Al-5Fe-6Cr LPBF alloy suggests that Fe+Cr can be a deliberate design route (nanoscale i-phase/intermetallic precipitation). If Fe is allowed to vary in your palette, joint constraints should allow “high Cr only when Fe is also high” to avoid exploring isolated high-Cr, low-Fe corners that may favor brittle Al–Cr intermetallics. (kimura2021microstructuraldevelopmentand pages 16-17)
- **Impurity sensitivity / oxide films:** While not Cr-specific, LPBF Al cracking is sensitive to oxide films and boundary features; high transition-metal additions that alter melt-pool boundary phases could interact with oxide-related crack initiation—worth including as a printability constraint proxy (e.g., via Scheil solidification range + predicted solid fraction slope metrics). (mehta2022al–mn–cr–zrbasedalloystailored pages 3-4, kotadiaUnknownyear…a pages 26-30)


References

1. (stopyra2020laserpowderbed pages 9-13): Wojciech Stopyra, Konrad Gruber, Irina Smolina, Tomasz Kurzynowski, and Bogumiła Kuźnicka. Laser powder bed fusion of aa7075 alloy: influence of process parameters on porosity and hot cracking. Additive manufacturing, 35:101270, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101270, doi:10.1016/j.addma.2020.101270. This article has 309 citations and is from a highest quality peer-reviewed journal.

2. (stopyra2020laserpowderbed media afe4449f): Wojciech Stopyra, Konrad Gruber, Irina Smolina, Tomasz Kurzynowski, and Bogumiła Kuźnicka. Laser powder bed fusion of aa7075 alloy: influence of process parameters on porosity and hot cracking. Additive manufacturing, 35:101270, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101270, doi:10.1016/j.addma.2020.101270. This article has 309 citations and is from a highest quality peer-reviewed journal.

3. (kimura2021microstructuraldevelopmentand pages 16-17): Takahiro Kimura, Takayuki Nakamoto, Tomoatsu Ozaki, Takao Miki, Isao Murakami, Yoshiki Hashizume, and Akiei Tanaka. Microstructural development and aging behavior of al–cr–zr heat-resistant alloy fabricated using laser powder bed fusion. Journal of Materials Research and Technology, 15:4193-4207, Nov 2021. URL: https://doi.org/10.1016/j.jmrt.2021.10.027, doi:10.1016/j.jmrt.2021.10.027. This article has 39 citations and is from a peer-reviewed journal.

4. (kimura2021microstructuraldevelopmentand pages 1-3): Takahiro Kimura, Takayuki Nakamoto, Tomoatsu Ozaki, Takao Miki, Isao Murakami, Yoshiki Hashizume, and Akiei Tanaka. Microstructural development and aging behavior of al–cr–zr heat-resistant alloy fabricated using laser powder bed fusion. Journal of Materials Research and Technology, 15:4193-4207, Nov 2021. URL: https://doi.org/10.1016/j.jmrt.2021.10.027, doi:10.1016/j.jmrt.2021.10.027. This article has 39 citations and is from a peer-reviewed journal.

5. (kimura2021microstructuraldevelopmentand pages 14-16): Takahiro Kimura, Takayuki Nakamoto, Tomoatsu Ozaki, Takao Miki, Isao Murakami, Yoshiki Hashizume, and Akiei Tanaka. Microstructural development and aging behavior of al–cr–zr heat-resistant alloy fabricated using laser powder bed fusion. Journal of Materials Research and Technology, 15:4193-4207, Nov 2021. URL: https://doi.org/10.1016/j.jmrt.2021.10.027, doi:10.1016/j.jmrt.2021.10.027. This article has 39 citations and is from a peer-reviewed journal.

6. (kimura2021microstructuraldevelopmentand pages 7-9): Takahiro Kimura, Takayuki Nakamoto, Tomoatsu Ozaki, Takao Miki, Isao Murakami, Yoshiki Hashizume, and Akiei Tanaka. Microstructural development and aging behavior of al–cr–zr heat-resistant alloy fabricated using laser powder bed fusion. Journal of Materials Research and Technology, 15:4193-4207, Nov 2021. URL: https://doi.org/10.1016/j.jmrt.2021.10.027, doi:10.1016/j.jmrt.2021.10.027. This article has 39 citations and is from a peer-reviewed journal.

7. (mehta2022al–mn–cr–zrbasedalloystailored pages 3-4): Bharat Mehta, Lars Nyborg, Karin Frisk, and Eduard Hryha. Al–mn–cr–zr-based alloys tailored for powder bed fusion-laser beam process: alloy design, printability, resulting microstructure and alloy properties. Journal of Materials Research, 37:1256-1268, Mar 2022. URL: https://doi.org/10.1557/s43578-022-00533-1, doi:10.1557/s43578-022-00533-1. This article has 20 citations and is from a peer-reviewed journal.

8. (kotadiaUnknownyear…a pages 26-30): HR Kotadia. … , a and howes, pd a review of laser powder bed fusion additive manufacturing of aluminium alloys: microstructure and properties http://researchonline. ljmu …. Unknown journal, Unknown year.

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


TASK — Element-specific bound: Cr
Cr is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Cr LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Cr) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Cr) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Cr).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
