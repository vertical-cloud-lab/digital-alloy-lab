# Phase 1 — Per-element bound: Al

*Edison task: `cd97bf21-0430-4c8b-975a-b1cdd7294e3e`*

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


TASK — Element-specific bound: Al
Al is the matrix/solvent. Provide a CONSERVATIVE and NON-CONSERVATIVE LOWER bound on the Al weight fraction (since the alloy must remain Al-rich) AND any practical UPPER bound (e.g. essentially 1.0, or a slightly tighter value if a minimum amount of solute is required for printability/strengthening).

Please return:
1. CONSERVATIVE bound (wt% of Al) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Al) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for common solutes).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


This response sets Al (matrix element) bounds by anchoring to compositions that are widely demonstrated as LPBF-printable (AlSi10Mg; Al–Mg–Sc–Zr/Scalmalloy) and by noting how high-solute chemistries increase solidification/freezing-range-driven hot cracking and volatile-solute instability.

| Bound type | Bound (Al wt%) | Equivalent total solute (wt%) | Literature anchor examples (with compositions) | Primary drivers / failure modes |
|---|---:|---:|---|---|
| Conservative lower bound | **94 wt%** | **≤ 6 wt%** | Scalmalloy LPBF powder/as-printed computes to **Al ≈ 93.7–94.1 wt%** from Mg 4.7→4.3, Sc 0.7, Zr 0.27, Mn 0.48, Fe 0.12–0.13, Si 0.06 wt%; demonstrated printable Al-Mg-Sc-Zr benchmark (mehta2021laserpowderbed pages 2-4) | Keeps search space in a demonstrated printable Al-rich regime; beyond this, cumulative solute raises risk of wider freezing range, non-Al primary/intermetallic formation, and reduced CALPHAD trust for higher-order extrapolations. Hot cracking and porosity risk rise as chemistry moves toward HS-Al-like regimes (kumar2021additivemanufacturingof pages 1-5, dixit2022laseradditivemanufacturing pages 1-2) |
| Non-conservative lower bound | **90 wt%** | **≤ 10 wt%** | AlSi10Mg uses **Si 9–11 wt%**, Mg **0.20–0.45 wt%**, Al balance; ~10 wt% Si improves flowability and can eliminate solidification cracking in LPBF. Supplier example: Si 9.84, Mg 0.32, Fe 0.10 wt%, Al balance (hyer2020understandingthelaser pages 1-2, bohm2020dilutionratioand pages 1-3) | Allows exploration up to the classic high-Si printable envelope; below ~90 wt% Al, chemistry increasingly enters non-anchor/high-solute territory where wide freezing range, hot cracking, brittle eutectic/intermetallic networks, and volatile-solute effects (Mg/Zn sputtering, porosity) become more likely, especially for Cu/Mg/Zn-rich combinations (kumar2021additivemanufacturingof pages 1-5, rosito2023processabilityofa6061 pages 1-2, rosito2023processabilityofa6061 pages 2-3) |
| Practical upper bound | **100 wt%** *(or 99.5 wt% if requiring at least trace solute)* | **0 wt%** *(or ≥ 0.5 wt% solute)* | Near-pure **99.5 wt% Al + 0.5 wt% Si** was reported to reduce cracking by approaching a single freezing point; increasing Si generally reduces crack density (dixit2022laseradditivemanufacturing pages 2-3, rosito2023processabilityofa6061 pages 2-3) | Pure Al is physically admissible, but if the design space requires intrinsic strengthening/printability assistance, impose a tiny minimum-solute floor (e.g., 0.5 wt%). Otherwise failure is not "too much Al" but inadequate strengthening and weaker crack-resistance margin versus lightly alloyed Al-Si cases (dixit2022laseradditivemanufacturing pages 2-3, hyer2020understandingthelaser pages 1-2) |


*Table: This table summarizes conservative and non-conservative lower bounds, plus a practical upper bound, for Al in an Al-rich LPBF alloy BO search space. It ties each bound to demonstrated printable alloy anchors and the main failure modes that emerge as total solute increases.*

## 1) CONSERVATIVE bound (Al wt%)
**Al ≥ 94 wt%** (i.e., total solute ≤ 6 wt%). This is conservative because a well-established LPBF alloy class (Scalmalloy®/Al–Mg–Sc–Zr) has Al as “remainder,” which computes to **~93.7–94.1 wt% Al** from its reported solute levels (Mg, Sc, Zr plus minor Mn/Fe/Si), demonstrating printability at ~94 wt% Al while keeping total solute modest. (mehta2021laserpowderbed pages 2-4)

## 2) NON-CONSERVATIVE bound (Al wt%)
**Al ≥ 90 wt%** (i.e., total solute ≤ 10 wt%). This bound corresponds to the classic LPBF-printable near-(hypo)eutectic Al–Si family: AlSi10Mg powder typically contains **Si 9–11 wt%** and **Mg ~0.20–0.45 wt%** (Al balance), and the high Si content is explicitly reported to improve melt flowability and eliminate solidification cracking in LPBF; near-eutectic compositions are reported to enable full density without solidification cracking. (hyer2020understandingthelaser pages 1-2, bohm2020dilutionratioand pages 1-3)

## 3) Practical UPPER bound (Al wt%)
**Al ≤ 100 wt%** (no practical upper limit needed for “Al-richness”); optionally, if you want to enforce a minimum solute floor for microstructural/printability margin, use **Al ≤ 99.5 wt%** (i.e., require ≥0.5 wt% solute). A near-pure alloy of **99.5 wt% Al + 0.5 wt% Si** has been reported to reduce cracking by approaching an almost single freezing point (rather than a freezing range), illustrating that very high Al is not intrinsically disallowed from a cracking standpoint. (dixit2022laseradditivemanufacturing pages 2-3)

## 4) Key failure modes that set each bound
### Why the conservative lower bound is ~94 wt% Al
- **Hot cracking from wide freezing range / poor feeding as total solute increases:** LPBF hot cracking is associated with alloys exhibiting a wide freezing range; moving toward high-solute, high-strength wrought chemistries increases this risk. (kumar2021additivemanufacturingof pages 1-5, dixit2022laseradditivemanufacturing pages 1-2)
- **Volatile-solute instability (composition drift → porosity/cracking scatter):** volatilization of elements such as **Zn and Mg** during LPBF is linked to turbulent melt pools, sputtering, and porosity—risks that generally grow as total solute (and especially volatile solute fraction) increases. (kumar2021additivemanufacturingof pages 1-5)
- **Brittle intermetallic/eutectic network formation at higher solute:** increasing non-Al content raises the likelihood of continuous low-ductility phases (system-dependent), which can amplify cracking sensitivity under LPBF thermal gradients (mechanism discussed broadly for HS-Al AM). (dixit2022laseradditivemanufacturing pages 1-2)

### Why the non-conservative lower bound can be pushed to ~90 wt% Al
- **High-Si alloys are a known exception that remain printable at higher solute:** ~10 wt% Si improves fluidity and (per LPBF AlSi10Mg literature) can eliminate solidification cracking; this supports allowing Al down to ~90 wt% specifically because Si-rich compositions behave differently than Cu/Mg/Zn-rich high-strength wrought chemistries. (hyer2020understandingthelaser pages 1-2, rosito2023processabilityofa6061 pages 2-3)
- **Below ~90 wt% Al, multi-solute combinations more often mimic HS-Al “crack-prone” behavior:** HS-Al alloys are described as prone to cracking due to extensive solidification range and low melt fluidity; composition modification is emphasized as needed to restore printability. (dixit2022laseradditivemanufacturing pages 1-2, dixit2022laseradditivemanufacturing pages 15-16)

## 5) Caveats / interactions for follow-up joint-constraints analysis
- **Si is the main “enabler” that lets you tolerate lower Al:** high Si narrows the solidification range and increases fluidity, reducing crack density. (hyer2020understandingthelaser pages 1-2, rosito2023processabilityofa6061 pages 2-3)
- **Mg and Zn (and likely Li) volatility becomes a coupling constraint with both LPBF parameters and atomization:** LPBF volatilization of Mg/Zn is linked to sputtering/porosity and composition drift; this argues for joint constraints such as (Mg+Zn+Li) upper bounds, or explicit evaporation-robustness objectives. (kumar2021additivemanufacturingof pages 1-5, rosito2023processabilityofa6061 pages 1-2)
- **Grain-refining solutes can relax the Al lower bound locally:** additions such as Sc/Zr (forming Al3(Sc,Zr)) are cited as crack-mitigation strategies in HS-Al AM by promoting equiaxed grains; such effects mean the Al lower bound could be loosened *conditional* on adequate grain refiners and/or eutectic-formers being present. (dixit2022laseradditivemanufacturing pages 2-3, dixit2022laseradditivemanufacturing pages 15-16)
- **Cu/Mg/Zn-rich corners (2xxx/7xxx-like) are disproportionately risky at a given Al%:** wide freezing range and hot cracking are repeatedly emphasized for high-strength wrought families; if BOFN explores substantial Cu+Mg+Zn simultaneously, you may need additional joint constraints beyond the scalar Al bound. (dixit2022laseradditivemanufacturing pages 1-2, kumar2021additivemanufacturingof pages 1-5)

Proposed implementation for BOFN search space (Al only):
- **Conservative:** Al ∈ [94, 100] wt%
- **Non-conservative:** Al ∈ [90, 100] wt%
- Optional: enforce **Al ≤ 99.5 wt%** only if you want to require ≥0.5 wt% total solute for baseline alloying. (dixit2022laseradditivemanufacturing pages 2-3)

References

1. (mehta2021laserpowderbed pages 2-4): Bharat Mehta, Arvid Svanberg, and Lars Nyborg. Laser powder bed fusion of an al-mg-sc-zr alloy: manufacturing, peak hardening response and thermal stability at peak hardness. Metals, 12:57, Dec 2021. URL: https://doi.org/10.3390/met12010057, doi:10.3390/met12010057. This article has 19 citations.

2. (kumar2021additivemanufacturingof pages 1-5): Manoj Kumar, Gregory J. Gibbons, Amitabha Das, Indranil Manna, David Tanner, and Hiren R. Kotadia. Additive manufacturing of aluminium alloy 2024 by laser powder bed fusion: microstructural evolution, defects and mechanical properties. Rapid Prototyping Journal, 27:1388-1397, Jul 2021. URL: https://doi.org/10.1108/rpj-10-2020-0241, doi:10.1108/rpj-10-2020-0241. This article has 54 citations and is from a peer-reviewed journal.

3. (dixit2022laseradditivemanufacturing pages 1-2): Som Dixit and Shunyu Liu. Laser additive manufacturing of high-strength aluminum alloys: challenges and strategies. Journal of Manufacturing and Materials Processing, 6:156, Dec 2022. URL: https://doi.org/10.3390/jmmp6060156, doi:10.3390/jmmp6060156. This article has 68 citations.

4. (hyer2020understandingthelaser pages 1-2): Holden Hyer, Le Zhou, Sharon Park, Guilherme Gottsfritz, George Benson, Bjorn Tolentino, Brandon McWilliams, Kyu Cho, and Yongho Sohn. Understanding the laser powder bed fusion of alsi10mg alloy. Metallography, Microstructure, and Analysis, 9:484-502, Jul 2020. URL: https://doi.org/10.1007/s13632-020-00659-w, doi:10.1007/s13632-020-00659-w. This article has 171 citations.

5. (bohm2020dilutionratioand pages 1-3): Constantin Böhm, Martin Werz, and Stefan Weihe. Dilution ratio and the resulting composition profile in dissimilar laser powder bed fusion of alsi10mg and al99.8. Metals, 10:1222, Sep 2020. URL: https://doi.org/10.3390/met10091222, doi:10.3390/met10091222. This article has 10 citations.

6. (rosito2023processabilityofa6061 pages 1-2): Michele Rosito, Matteo Vanzetti, Elisa Padovano, Flavia Gili, Roberta Sampieri, Federica Bondioli, and Claudio Francesco Badini. Processability of a6061 aluminum alloy using laser powder bed fusion by in situ synthesis of grain refiners. Metals, 13:1128, Jun 2023. URL: https://doi.org/10.3390/met13061128, doi:10.3390/met13061128. This article has 18 citations.

7. (rosito2023processabilityofa6061 pages 2-3): Michele Rosito, Matteo Vanzetti, Elisa Padovano, Flavia Gili, Roberta Sampieri, Federica Bondioli, and Claudio Francesco Badini. Processability of a6061 aluminum alloy using laser powder bed fusion by in situ synthesis of grain refiners. Metals, 13:1128, Jun 2023. URL: https://doi.org/10.3390/met13061128, doi:10.3390/met13061128. This article has 18 citations.

8. (dixit2022laseradditivemanufacturing pages 2-3): Som Dixit and Shunyu Liu. Laser additive manufacturing of high-strength aluminum alloys: challenges and strategies. Journal of Manufacturing and Materials Processing, 6:156, Dec 2022. URL: https://doi.org/10.3390/jmmp6060156, doi:10.3390/jmmp6060156. This article has 68 citations.

9. (dixit2022laseradditivemanufacturing pages 15-16): Som Dixit and Shunyu Liu. Laser additive manufacturing of high-strength aluminum alloys: challenges and strategies. Journal of Manufacturing and Materials Processing, 6:156, Dec 2022. URL: https://doi.org/10.3390/jmmp6060156, doi:10.3390/jmmp6060156. This article has 68 citations.

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


TASK — Element-specific bound: Al
Al is the matrix/solvent. Provide a CONSERVATIVE and NON-CONSERVATIVE LOWER bound on the Al weight fraction (since the alloy must remain Al-rich) AND any practical UPPER bound (e.g. essentially 1.0, or a slightly tighter value if a minimum amount of solute is required for printability/strengthening).

Please return:
1. CONSERVATIVE bound (wt% of Al) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Al) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for common solutes).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
