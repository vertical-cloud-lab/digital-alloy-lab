# Phase 1 — Per-element bound: Sn

*Edison task: `a99be181-350a-4992-863d-2a80ce674a9e`*

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


TASK — Element-specific bound: Sn
Sn is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Sn LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Sn) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Sn) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Sn).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Element-specific compositional bounds (Sn, wt%) for BOFN search space

This response proposes two Sn upper bounds: a conservative “commercially qualified LPBF alloy” cap and a non-conservative “Al-rich exploratory” cap that still respects your stated Al≥85 wt% constraint.

| Bound type | Sn upper bound (wt%) | Evidence basis (cite LPBF/commercial or experimental) | Main constraint/failure mode |
|---|---:|---|---|
| Conservative upper bound | 0.05 | Commercial/qualified LPBF AlSi10Mg feedstock shows Sn measured at `<0.01 wt%`, with manufacturer spec that no individual impurity exceeds `0.05 wt%`; this is a defensible conservative cap for a commercial-style search space absent a Sn-bearing qualified alloy benchmark (specht2021shockcompressionresponse pages 2-4) | Keeps Sn at impurity-trace level; avoids entering the Al-Sn miscibility-gap regime associated with segregation and Sn-rich intergranular films not represented by mainstream qualified LPBF Al alloys (specht2021shockcompressionresponse pages 2-4, rusin2025effectoflaser pages 1-2) |
| Non-conservative upper bound | 15 | Aggressive but still Al-rich: project constraint `Al ≥ 85 wt%` implies `Sn ≤ 15 wt%`. This remains below the `20 wt%` Sn limit cited in LPBF Al-Sn-Pb literature/GOST to avoid continuous intergranular Sn layers, while experimental LPBF has printed much higher-Sn Al/Sn `80/20 vol%` material (~`40 wt%` Sn), showing 15 wt% is experimentally defensible though aggressive (rusin2025effectoflaser pages 1-2, confalonieri2022effectofprocess pages 2-4, confalonieri2021alsnmiscibilitygap pages 18-19, confalonieri2022effectofprocess pages 8-11) | Approaching 15 wt% raises risk of continuous/intergranular Sn films, incomplete Al melting or nonuniform soft-phase distribution at low energy density, crack formation with Sn-filled cracks, segregation along melt-pool boundaries, and coarsening/liquid-phase redistribution during thermal cycling (confalonieri2021alsnmiscibilitygap pages 18-19, confalonieri2022effectofprocess pages 8-11, rusin2025effectoflaser pages 1-2, rusin2025effectoflaser pages 4-6) |


*Table: This table gives compact conservative and non-conservative Sn upper bounds for Al-rich LPBF alloy design, anchored to commercial impurity specifications and experimental Al-Sn LPBF studies. It also summarizes the dominant failure modes that justify each bound.*

### 1) CONSERVATIVE Sn upper bound: **0.05 wt% Sn**
Commercial LPBF AlSi10Mg feedstock data (Carpenter Additive) report Sn at trace levels (<0.01 wt% in powder, 0 in as-built) and specify that *no individual impurity element* exceeds 0.05 wt% (with total unmeasured impurities <0.15 wt%), making 0.05 wt% a defensible conservative upper bound aligned to established LPBF powder specifications. (specht2021shockcompressionresponse pages 2-4)

### 2) NON-CONSERVATIVE Sn upper bound: **15 wt% Sn**
A defensible aggressive bound is 15 wt% Sn because it satisfies the programmatic/processability constraint of remaining Al-rich (Al≥85 wt% ⇒ Sn≤15 wt%) while staying below a cited guideline that tin in Al “should be limited to 20 wt.%” to avoid continuous intergranular Sn layers that prevent formation of a strong load-bearing Al framework. (rusin2025effectoflaser pages 1-2)

(For context, LPBF feasibility has been demonstrated at far higher Sn: Al/Sn=80/20 by volume, reported as ≈40 wt% Sn, including solid and lattice builds, so 15 wt% is aggressive but not unprecedented in LPBF processing—though the associated failure modes become increasingly dominant.) (confalonieri2022effectofprocess pages 2-4)

### 3) Key failure modes that set each bound

**Conservative bound (≤0.05 wt% Sn):**
- **Qualification/specification alignment:** mainstream LPBF Al alloys (e.g., AlSi10Mg) treat Sn as a trace impurity; bounding Sn at ≤0.05 wt% matches a manufacturer impurity maximum and avoids leaving the “commercial alloy” design regime. (specht2021shockcompressionresponse pages 2-4)
- **Avoidance of miscibility-gap behavior:** higher Sn pushes toward Al–Sn immiscibility with Sn segregation to grain boundaries / melt-pool bands and intergranular Sn films, which is outside typical qualified structural LPBF Al alloys. (confalonieri2022effectofprocess pages 8-11)

**Non-conservative bound (≤15 wt% Sn):**
- **Intergranular Sn films → embrittlement / loss of ductility:** high Sn promotes continuous Sn interlayers along Al grain boundaries; a cited standard/guideline recommends limiting Sn to ~20 wt% because these films prevent strong Al framework bonding and act as localized shear bands that rapidly thin and fracture. (rusin2025effectoflaser pages 1-2)
- **Hot cracking / solidification cracking propensity:** LPBF Al–Sn reports cracking tied to prolonged solid–liquid coexistence (Sn melting ≈232 °C vs much higher Al-rich liquidus), rupture of intergranular liquid, and crack networks (often Sn-filled). Crack frequency increases at low volumetric energy density (VED). (confalonieri2021alsnmiscibilitygap pages 18-19, confalonieri2022effectofprocess pages 8-11)
- **Segregation / banding:** Sn-rich zones tracing melt-pool bands indicate incomplete mixing/segregation; Sn can appear as intergranular/film-like features at low-energy conditions. (confalonieri2022effectofprocess pages 8-11)
- **Processing-window sensitivity:** low laser energy density can produce incomplete Al melting and non-uniform distribution of soft Sn-rich inclusions; achieving acceptable uniformity may require higher VED. (rusin2025effectoflaser pages 1-2)
- **Thermal-cycle instability:** thermal cycling across Sn melting can cause Sn droplet formation and whiskers/coarsening, implying risks for service/HT schedules that enter the Sn liquid regime. (confalonieri2022effectofprocess pages 8-11)

### 4) Sn-specific caveats / interactions for follow-up joint-constraints analysis

- **VED/process coupling:** because Sn-related cracking/segregation is highly VED-dependent (cracks increase at low VED; incomplete melting/nonuniformity at low energy density), consider a joint constraint that tightens the feasible LPBF-process window as Sn increases (e.g., require minimum VED or limit scan speed range when Sn is high). (confalonieri2022effectofprocess pages 8-11, rusin2025effectoflaser pages 1-2)
- **Thermal history constraints:** if solutionizing/stress relief/post-build thermal cycles can cross ~232 °C (Sn melting) or dwell near it, add constraints or penalties at higher Sn due to observed coarsening/droplet formation/redistribution. (confalonieri2022effectofprocess pages 8-11)
- **Pb interaction (if ever introduced outside your palette):** Pb can fragment continuous Sn films and improve ductility but lowers strength; not directly applicable to your element palette, but it flags the general principle that low-melting immiscible additions can strongly change film morphology and mechanical response. (rusin2025effectoflaser pages 2-4, rusin2025effectoflaser pages 4-6)
- **CALPHAD/model-validity note:** Al–Sn is a miscibility-gap system with strong segregation; even if TCAl10 contains assessed binaries, multi-component extrapolations at elevated Sn may be uncertain, so consider a model-validity penalty that rises with Sn (especially above trace levels) unless supported by targeted assessments/validation. (confalonieri2022effectofprocess pages 8-11)


References

1. (specht2021shockcompressionresponse pages 2-4): Paul E. Specht and Nathan P. Brown. Shock compression response of additively manufactured alsi10mg. Journal of Applied Physics, Dec 2021. URL: https://doi.org/10.1063/5.0076604, doi:10.1063/5.0076604. This article has 17 citations and is from a peer-reviewed journal.

2. (rusin2025effectoflaser pages 1-2): Nikolay M. Rusin, Alexander L. Skorentsev, Kirill O. Akimov, Vadim E. Likharev, Dmitry P. Il’yashchenko, and Andrey I. Dmitriev. Effect of laser energy density during lpbf on the structure and mechanical properties of al–15sn–5pb alloy. Materials, 18:5268, Nov 2025. URL: https://doi.org/10.3390/ma18235268, doi:10.3390/ma18235268. This article has 0 citations.

3. (confalonieri2022effectofprocess pages 2-4): Chiara Confalonieri, Riccardo Casati, and Elisabetta Gariboldi. Effect of process parameters on laser powder bed fusion of al-sn miscibility gap alloy. Quantum Beam Science, 6:17, Apr 2022. URL: https://doi.org/10.3390/qubs6020017, doi:10.3390/qubs6020017. This article has 12 citations.

4. (confalonieri2021alsnmiscibilitygap pages 18-19): Chiara Confalonieri and Elisabetta Gariboldi. Al-sn miscibility gap alloy produced by power bed laser melting for application as phase change material. Journal of Alloys and Compounds, 881:160596, Nov 2021. URL: https://doi.org/10.1016/j.jallcom.2021.160596, doi:10.1016/j.jallcom.2021.160596. This article has 43 citations and is from a peer-reviewed journal.

5. (confalonieri2022effectofprocess pages 8-11): Chiara Confalonieri, Riccardo Casati, and Elisabetta Gariboldi. Effect of process parameters on laser powder bed fusion of al-sn miscibility gap alloy. Quantum Beam Science, 6:17, Apr 2022. URL: https://doi.org/10.3390/qubs6020017, doi:10.3390/qubs6020017. This article has 12 citations.

6. (rusin2025effectoflaser pages 4-6): Nikolay M. Rusin, Alexander L. Skorentsev, Kirill O. Akimov, Vadim E. Likharev, Dmitry P. Il’yashchenko, and Andrey I. Dmitriev. Effect of laser energy density during lpbf on the structure and mechanical properties of al–15sn–5pb alloy. Materials, 18:5268, Nov 2025. URL: https://doi.org/10.3390/ma18235268, doi:10.3390/ma18235268. This article has 0 citations.

7. (rusin2025effectoflaser pages 2-4): Nikolay M. Rusin, Alexander L. Skorentsev, Kirill O. Akimov, Vadim E. Likharev, Dmitry P. Il’yashchenko, and Andrey I. Dmitriev. Effect of laser energy density during lpbf on the structure and mechanical properties of al–15sn–5pb alloy. Materials, 18:5268, Nov 2025. URL: https://doi.org/10.3390/ma18235268, doi:10.3390/ma18235268. This article has 0 citations.

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


TASK — Element-specific bound: Sn
Sn is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Sn LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Sn) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Sn) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Sn).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
