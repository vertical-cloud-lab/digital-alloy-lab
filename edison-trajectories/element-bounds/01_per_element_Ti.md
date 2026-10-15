# Phase 1 — Per-element bound: Ti

*Edison task: `da117924-dac8-448e-bb45-6331e37b41cf`*

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


TASK — Element-specific bound: Ti
Ti is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Ti LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Ti) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Ti) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Ti).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Element-specific bound: Ti (wt%) for Al-rich LPBF BO search space

### 1) CONSERVATIVE Ti upper bound: **1.0 wt% Ti**
Ti at ~0.77 wt% (Al–Mn–Ti–Zr) produced LPBF parts with **99.9 ± 0.1% density** and **no pores or solidification cracks**, demonstrating robust printability in an Al-rich, B-free grain-refiner approach. (mair2022microstructuralfeaturesand pages 3-4)  A separate Zr–Ti-modified 2139 alloy reported **Ti ≈ 1.08 wt%** (measured) with **~99.67% density** and **no hot-cracks**, supporting ~1 wt% Ti as a conservative ceiling for crack-free processing where Ti functions mainly as an inoculant/solute for CET rather than a bulk intermetallic former. (larini2023microstructuralevolutionof pages 4-6, larini2023microstructuralevolutionof pages 2-4)

### 2) NON-CONSERVATIVE Ti upper bound: **3.7 wt% Ti**
Commercial/AM-targeted TiB2-grain-refined Al alloys demonstrate successful LPBF at **Ti ≈ 3.25–3.7 wt%** when Ti is intentionally paired with B: A20X is reported with **~3.7 wt% Ti** (with B) and, along with Ti/B-modified 2618 variants (2.3–3.5 wt% Ti), achieved **>99.7% density** and **crack-free microstructures** after parameter optimization. (belelli2021investigationontwo pages 1-2)  Similarly, an A205 (Al–Cu–Ag–Mg–Ti–B) powder with **3.25 wt% Ti** produced **crack-free LPBF samples** at **99.5 ± 0.1% relative density**, consistent with a defensible aggressive Ti ceiling in Al-rich LPBF when operating on a Ti–B (TiB2-forming) manifold. (mair2021microstructureandmechanical pages 1-2)

### 3) Key failure modes that set each bound

**Conservative bound (~1 wt% Ti): what it avoids**
- **Coarse/brittle trialuminides under non-rapid cooling or certain post-build thermal histories:** Ti (with Zr) can form trialuminides; at hyperperitectic levels, slow-cooling conditions can favor coarsened, brittle tetragonal Al3Ti/Al3Zr-type phases rather than fine coherent L12 precipitates, which is an embrittlement risk. (mair2022microstructuralfeaturesand pages 6-7)
- **Over-reliance on TiB2 chemistry:** keeping Ti ≤1 wt% enables Ti/Zr (or Ti/Sc) inoculation strategies without requiring B additions and associated powder-production complications. (mair2022microstructuralfeaturesand pages 3-4, larini2023microstructuralevolutionof pages 4-6)

**Non-conservative bound (~3.7 wt% Ti): what starts to break first**
- **Powder production risk (gas atomization):** high Ti+B levels can create practical atomization problems including **nozzle clogging**, explicitly noted as a motivation to reduce Ti/B additions. (belelli2021investigationontwo pages 1-2)
- **Intermetallic fraction / embrittlement risk if Ti is not tied up as TiB2:** at high Ti, if B is insufficient (or other elements shift phase selection), excess Ti can promote more Al3Ti-related pathways; Ti is also observed to be supersaturated in as-built α-Al under LPBF cooling, reflecting strong non-equilibrium partitioning that can increase sensitivity to processing window and heat treatment. (mair2021microstructureandmechanical pages 6-7)
- **Process/property sensitivity:** the TiB2 mechanism depends on particle size distribution and nucleant potency; coarse particles are less effective nucleants, so “high Ti” does not guarantee grain refinement unless TiB2 formation and particle refinement are controlled. (mair2021microstructureandmechanical pages 6-7)

### 4) Element-specific caveats / interactions to flag for joint-constraints
- **Ti–B coupling is essential above ~2 wt% Ti:** the best-supported high-Ti LPBF compositions are explicitly **TiB2-grain-refined systems** (e.g., 3.25–3.7 wt% Ti with ~0.8–1.6 wt% B), so a joint constraint such as a Ti:B stoichiometry window (plus allowance for “excess Ti”) should be enforced if exploring Ti > 1 wt%. (belelli2021investigationontwo pages 1-2, mair2021microstructureandmechanical pages 3-5)
- **Ti–Zr synergy (B-free inoculation route):** modest Ti with Zr forms coherent Al3(Zr,Ti) or L12 Al3(Ti,Zr)-type inoculants that enable CET and crack suppression at high density; thus Ti and Zr should be co-analyzed in CALPHAD/Scheil for primary trialuminide formation vs solute trapping. (larini2023microstructuralevolutionof pages 4-6, mair2022microstructuralfeaturesand pages 6-7)
- **Interaction with Cu/Mg (high-strength alloys):** in TiB2-containing Al–Cu alloys, precipitates (e.g., Al2Cu) were observed to nucleate at pores and TiB2 particles and Ti can remain in solution at supersaturated levels, so composition/process changes that alter segregation may change cracking/porosity sensitivity. (mair2021microstructureandmechanical pages 6-7, mair2021microstructureandmechanical pages 1-2)
- **Modeling caveat (CALPHAD/TCAl10):** once Ti is pushed into the ~3–4 wt% regime in multicomponent spaces, predicted primary phase fields (Al3Ti, Al3(Zr,Ti), TiB2 if B present) become a dominant driver of solidification range and crack susceptibility; treat CALPHAD coverage/extrapolation risk as increasing with component count and with Ti–B–Zr interactions.

### Summary table (for direct BO bound entry)
| Bound class | Bound (wt% Ti) | Literature basis (brief examples) | Justification | Key failure modes that set bound | Key caveats/interactions |
|---|---:|---|---|---|---|
| Conservative upper bound | 1.0 | Al-Mn-Ti-Zr LPBF alloy: Ti = 0.77 wt% in as-built material, 99.9 ± 0.1% density, no pores or solidification cracks; Al2139ZrTi LPBF alloy: measured Ti = 1.08 wt%, 99.67% density, no hot-cracks (mair2022microstructuralfeaturesand pages 3-4, larini2023microstructuralevolutionof pages 4-6) | 1.0 wt% Ti stays within the demonstrated crack-free LPBF regime for Al-rich alloys where Ti acts mainly as a grain-refining/inoculant addition (often with Zr) rather than a bulk intermetallic former. | Above this level, risk grows for hyperperitectic trialuminide formation and, under slower local cooling/heat treatment, coarsening toward brittle tetragonal Al3Ti/Al3Zr-type phases rather than benign fine L12 inoculants; excessive Ti also increases intermetallic fraction without broad commercial LPBF precedent in B-free systems (mair2022microstructuralfeaturesand pages 6-7, larini2023microstructuralevolutionof pages 2-4). | Strong synergy with Zr/Sc: Ti is much safer near 1 wt% when paired to form coherent L12 Al3(Ti,Zr) or Al3(Sc,Ti); if B is absent, do not assume 2–4 wt% Ti remains printable across the joint space; Ti also carries some mineral-burden penalty. |
| Non-conservative upper bound | 3.7 | A20X contains ~3.7 wt% Ti and ~1.6 wt% B; modified 2618 variants used 2.3–3.5 wt% Ti with 0.8–1.2 wt% B and achieved >99.7% density and crack-free LPBF; A205 used 3.25 wt% Ti + 1.25 wt% B and produced crack-free 99.5 ± 0.1% dense LPBF parts (belelli2021investigationontwo pages 1-2, mair2021microstructureandmechanical pages 1-2, mair2021microstructureandmechanical pages 3-5) | 3.7 wt% Ti is an aggressive but defensible ceiling because it matches the upper end of published/commercial LPBF Al alloys in which high Ti is intentionally paired with B to form TiB2 nuclei and suppress hot cracking. | This bound is set by practical atomization and metallurgical limits: high Ti+B can cause gas-atomization nozzle clogging; if Ti is not tied up as TiB2, excess Ti can promote coarse/intermetallic-rich microstructures, possible Al3Ti-mediated brittleness, and stronger sensitivity to non-equilibrium supersaturation/phase-selection uncertainty (belelli2021investigationontwo pages 1-2, mair2021microstructureandmechanical pages 6-7, mair2022microstructuralfeaturesand pages 6-7). | Treat 3.7 wt% as valid mainly on a Ti-B manifold; impose follow-up joint constraints on Ti:B stoichiometry (for TiB2 formation), and review interactions with Zr/Sc/Cu/Mg because Ti can participate in Al3Ti or Al3(Zr,Ti) pathways, alter constitutional undercooling, and shift CALPHAD confidence as multicomponent complexity rises (larini2023microstructuralevolutionof pages 4-6, mair2021microstructureandmechanical pages 6-7, mair2022microstructuralfeaturesand pages 6-7). |


*Table: This table summarizes conservative and aggressive Ti upper bounds for Al-rich LPBF alloy search spaces, anchored to published crack-free/high-density compositions. It also highlights the failure modes and coupling constraints that matter when translating these literature examples into BO search bounds.*

References

1. (mair2022microstructuralfeaturesand pages 3-4): Philipp Mair, Ilse Letofsky-Papst, and Gerhard Leichtfried. Microstructural features and mechanical properties of a novel ti- and zr-modified al-mn alloy processed by laser powder bed fusion. Journal of Alloys and Compounds, 897:163156, Mar 2022. URL: https://doi.org/10.1016/j.jallcom.2021.163156, doi:10.1016/j.jallcom.2021.163156. This article has 25 citations and is from a peer-reviewed journal.

2. (larini2023microstructuralevolutionof pages 4-6): Federico Larini, Riccardo Casati, Silvia Marola, and Maurizio Vedani. Microstructural evolution of a high-strength zr-ti-modified 2139 aluminum alloy for laser powder bed fusion. Metals, 13:924, May 2023. URL: https://doi.org/10.3390/met13050924, doi:10.3390/met13050924. This article has 14 citations.

3. (larini2023microstructuralevolutionof pages 2-4): Federico Larini, Riccardo Casati, Silvia Marola, and Maurizio Vedani. Microstructural evolution of a high-strength zr-ti-modified 2139 aluminum alloy for laser powder bed fusion. Metals, 13:924, May 2023. URL: https://doi.org/10.3390/met13050924, doi:10.3390/met13050924. This article has 14 citations.

4. (belelli2021investigationontwo pages 1-2): F. Belelli, R. Casati, F. Larini, M. Riccio, and M. Vedani. Investigation on two ti–b-reinforced al alloys for laser powder bed fusion. Materials Science and Engineering: A, 808:140944, Mar 2021. URL: https://doi.org/10.1016/j.msea.2021.140944, doi:10.1016/j.msea.2021.140944. This article has 56 citations.

5. (mair2021microstructureandmechanical pages 1-2): P. Mair, L. Kaserer, Jakob Braun, N. Weinberger, I. Letofsky-Papst, and G. Leichtfried. Microstructure and mechanical properties of a tib2-modified al–cu alloy processed by laser powder-bed fusion. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 799:140209, Jan 2021. URL: https://doi.org/10.1016/j.msea.2020.140209, doi:10.1016/j.msea.2020.140209. This article has 150 citations.

6. (mair2022microstructuralfeaturesand pages 6-7): Philipp Mair, Ilse Letofsky-Papst, and Gerhard Leichtfried. Microstructural features and mechanical properties of a novel ti- and zr-modified al-mn alloy processed by laser powder bed fusion. Journal of Alloys and Compounds, 897:163156, Mar 2022. URL: https://doi.org/10.1016/j.jallcom.2021.163156, doi:10.1016/j.jallcom.2021.163156. This article has 25 citations and is from a peer-reviewed journal.

7. (mair2021microstructureandmechanical pages 6-7): P. Mair, L. Kaserer, Jakob Braun, N. Weinberger, I. Letofsky-Papst, and G. Leichtfried. Microstructure and mechanical properties of a tib2-modified al–cu alloy processed by laser powder-bed fusion. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 799:140209, Jan 2021. URL: https://doi.org/10.1016/j.msea.2020.140209, doi:10.1016/j.msea.2020.140209. This article has 150 citations.

8. (mair2021microstructureandmechanical pages 3-5): P. Mair, L. Kaserer, Jakob Braun, N. Weinberger, I. Letofsky-Papst, and G. Leichtfried. Microstructure and mechanical properties of a tib2-modified al–cu alloy processed by laser powder-bed fusion. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 799:140209, Jan 2021. URL: https://doi.org/10.1016/j.msea.2020.140209, doi:10.1016/j.msea.2020.140209. This article has 150 citations.

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


TASK — Element-specific bound: Ti
Ti is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Ti LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Ti) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Ti) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Ti).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
