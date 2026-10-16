# Phase 1 — Per-element bound: Mn

*Edison task: `0ae4892f-563e-46cb-9c55-a4721dac86b0`*

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


TASK — Element-specific bound: Mn
Mn is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Mn LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Mn) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Mn) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Mn).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Mn compositional bounds for BOFN search space (Al-rich LPBF)

| Mn upper-bound class | Recommended upper bound (wt%) | 1–2 sentence justification | Key evidence compositions | Primary failure modes / constraints | Caveats / interactions |
|---|---:|---|---|---|---|
| Conservative | **0.7 wt% Mn** | A conservative BOFN cap is **0.7 wt% Mn**, anchored to established commercial/commercial-like Al alloys already used or seriously studied in LPBF: EN AW-5083 is AlMg4.5Mn0.7, LPBF 2024 feedstock is reported at ~0.60 wt% Mn, and Scalmalloy-type LPBF alloys are ~0.5 wt% Mn. This keeps Mn within the envelope of known AM-relevant compositions rather than relying on LPBF-enabled metastable supersaturation. (aversa2019newaluminumalloys pages 8-10) | AlMg4.5Mn0.7 (5083); Al-4.35Cu-1.50Mg-0.60Mn (2024); Scalmalloy review composition with ~0.5 wt% Mn (aversa2019newaluminumalloys pages 8-10) | Bound is set mainly by **lack of broad qualification history above ~0.7 wt% Mn** in commercial LPBF Al alloys; once Mn is pushed higher, design increasingly depends on rapid-solidification supersaturation and tailored grain-refiner chemistry rather than established alloy practice. Conventional Al alloys without suitable solidification control remain vulnerable to hot cracking/limited process windows. (aversa2019newaluminumalloys pages 8-10) | Mn alone is not the dominant crack mitigator at these levels; printability is often controlled more strongly by **Si, Sc/Zr, TiB2, or Zr/Ti inoculation strategy**. In a joint-constraints analysis, Mn should not be credited as sufficient to overcome cracking in Cu/Mg-rich systems without complementary grain refiners or eutectic modifiers. (aversa2019newaluminumalloys pages 8-10) |
| Non-conservative | **5.0 wt% Mn** | A defensible aggressive cap is **5.0 wt% Mn**, because LPBF/PBF-LB studies have actually processed Al-rich alloys at **4.8 wt% Mn** with **99.9% density** and at **~4.7–5.0 wt% Mn** in Al–Mn–Cr–Zr alloys; separate analyses report Mn retained in supersaturated solid solution up to **~4.3–4.5 wt%**, while rapid-solidification literature cited by Mehta suggests metastable Mn solubility can extend to **~6–8 wt%**. Using **5 wt%** stays inside demonstrated LPBF compositions while remaining below the more speculative rapid-solidification limit. (mair2022microstructuralfeaturesand pages 2-3, mair2022microstructuralfeaturesand pages 6-7, mehta2022al–mn–cr–zrbasedalloystailored pages 2-3, martucci2022theinfluenceof pages 1-2, mehta2022al–mn–cr–zrbasedalloystailored pages 2-2, mehta2022al–mn–cr–zrbasedalloystailored pages 1-2) | Mair Al-Mn-Ti-Zr: 4.8 wt% Mn, ~99.9% density; Mehta Al-Mn-Cr-Zr: ~4.7–5.0 wt% Mn; Martucci: up to ~4.3 wt% Mn retained in supersaturated solution; Mair cites up to ~4.5 wt% Mn in solution; Mehta cites rapid-solidification Mn solubility ~6–8 wt% (mair2022microstructuralfeaturesand pages 2-3, mair2022microstructuralfeaturesand pages 6-7, mehta2022al–mn–cr–zrbasedalloystailored pages 2-3, martucci2022theinfluenceof pages 1-2, mair2022microstructuralfeaturesand pages 1-2, mehta2022al–mn–cr–zrbasedalloystailored pages 2-2) | Above ~4–5 wt% Mn, the practical limits shift to **segregation and primary/interdendritic phase formation**: Mn rejected from solution forms grain-boundary/interdendritic **AlxMn(Fe,Si)** quasicrystal/intermetallic networks and Mn-rich precipitates, especially when Fe/Si are present. In Mn-Cr-Zr families, cracking has been observed in **Mg-containing, Zr-low** variants with Mn-rich precipitates near melt-pool boundaries; thermal history also strongly controls how much Mn remains metastably dissolved. (mair2022microstructuralfeaturesand pages 6-7, mair2022microstructuralfeaturesand pages 4-6, mehta2023advancingnovelalmncrzr pages 3-5) | Strong follow-up joint constraints are warranted for **Fe + Si** (promote Mn-rich quasicrystal/intermetallic networks), **Zr/Ti/Cr** (needed for inoculation, grain refinement, and precipitation control), and **Mg** (can lower solidus and worsen cracking when combined with insufficient Zr). Mn benefits from low vapor pressure/high boiling point for LPBF, but high Mn designs are **cooling-rate sensitive** and may be outside the most trustworthy CALPHAD extrapolation space in higher-order systems. (mair2022microstructuralfeaturesand pages 6-7, mehta2023advancingnovelalmncrzr pages 3-5, martucci2022theinfluenceof pages 1-2, mair2022microstructuralfeaturesand pages 1-2) |


*Table: This table summarizes a conservative and a more aggressive Mn upper bound for the BOFN search space, tied to LPBF literature and rapid-solidification arguments. It also flags the main processability constraints and element interactions that should become joint constraints in later search-space refinement.*

### 1) CONSERVATIVE upper bound (Mn, wt%)
**Mn ≤ 0.7 wt%**. This is anchored to established commercial/commercial-like Al alloys used or seriously explored in LPBF: EN AW‑5083 is AlMg4.5Mn0.7, LPBF 2024 feedstock is reported at ~0.60 wt% Mn, and Scalmalloy-type LPBF alloys are ~0.5 wt% Mn (these are within the published “known-printable / qualified powder” ecosystem rather than relying on metastable supersaturation). (aversa2019newaluminumalloys pages 8-10)

### 2) NON-CONSERVATIVE upper bound (Mn, wt%)
**Mn ≤ 5.0 wt%**. Multiple LPBF/PBF‑LB studies report successful processing of Al‑rich alloys at ~4.8–5.0 wt% Mn: Mair et al. used a pre-alloyed powder with **4.80 wt% Mn** and achieved **99.9 ± 0.1% density**, with substantial Mn retained in supersaturated α‑Al; Mehta et al. report printed Al–Mn–Cr–Zr alloys retaining ~4.7–5.0 wt% Mn, and independent analyses report Mn retained in supersaturated solution up to ~4.3–4.5 wt% under rapid solidification. A more aggressive thermodynamic argument exists (rapid-solidification Mn solubility cited as ~6–8 wt%), but **5 wt%** stays aligned with demonstrated LPBF compositions and is thus the recommended “non-conservative but defensible” cap. (mair2022microstructuralfeaturesand pages 2-3, mair2022microstructuralfeaturesand pages 6-7, mehta2022al–mn–cr–zrbasedalloystailored pages 2-3, martucci2022theinfluenceof pages 1-2, mehta2022al–mn–cr–zrbasedalloystailored pages 2-2)

### 3) Key failure modes setting each bound
**At/near the conservative bound (~0.7 wt%):**
- **Qualification / precedent constraint**: above ~0.6–0.7 wt% Mn you quickly leave the envelope of standard LPBF Al alloy families (5083/2024/Scalmalloy-type compositions) and enter “LPBF-tailored” Al–Mn designs, which typically require co-alloying/inoculants to be crack-free and robust. (aversa2019newaluminumalloys pages 8-10)

**At/near the non-conservative bound (~5 wt%):**
- **Interdendritic / grain-boundary Mn-rich phase formation**: when Mn exceeds metastable solubility, rejected Mn partitions to boundaries and forms Mn-rich intermetallic/quasicrystalline networks such as **AlxMn(Fe,Si)**; even minor Fe/Si promotes/stabilizes these phases, which can be brittle and act as crack-initiation sites. (mair2022microstructuralfeaturesand pages 6-7, mair2022microstructuralfeaturesand pages 4-6)
- **Primary Mn-rich precipitates at melt-pool/solidification boundaries**: in Al–Mn–Cr–Zr families, increasing precipitation area fraction was attributed largely to Mn-rich precipitates; cracking was observed in a **Zr-low, Mg-containing** variant with cracks originating around melt-pool boundaries. (mehta2023advancingnovelalmncrzr pages 3-5)
- **Cooling-rate sensitivity**: high Mn strategies depend on rapid solidification to retain Mn in α‑Al; altered thermal histories (e.g., increased platform temperature or lower cooling rates) reduce supersaturation and can shift microstructure toward more boundary phases/precipitation. (mair2022microstructuralfeaturesand pages 6-7)

### 4) Mn-specific caveats / interactions for follow-up joint-constraints
- **Fe and Si (strong interaction)**: Fe/Si strongly promote formation of grain-boundary/interdendritic **AlxMn(Fe,Si)** phases in high‑Mn LPBF alloys; joint constraints on Fe/Si impurities become more critical as Mn approaches 4–5 wt%. (mair2022microstructuralfeaturesand pages 6-7, mair2022microstructuralfeaturesand pages 4-6)
- **Zr/Ti/Cr as enablers**: high-Mn LPBF alloys commonly rely on Zr/Ti/Cr for inoculation/grain refinement and precipitation control; Zr-high variants can mitigate cracking risk compared with Zr-low variants. (mehta2023advancingnovelalmncrzr pages 3-5, martucci2022theinfluenceof pages 1-2)
- **Mg coupling risk**: Mg-containing, Zr-low variants in Al–Mn–Cr–Zr families exhibited cracking originating near melt-pool boundaries, consistent with Mg lowering solidus and increasing cracking susceptibility when grain refinement/precipitation control is insufficient. (mehta2023advancingnovelalmncrzr pages 3-5)
- **Modeling note for CALPHAD/TCAl10**: pushing Mn toward the cited rapid-solidification “solubility extension” (6–8 wt%) is more speculative and likely to incur greater uncertainty in high-order extrapolations and Scheil/hot-cracking surrogates, so it is better treated as an exploration regime beyond the recommended non-conservative bound. (mehta2022al–mn–cr–zrbasedalloystailored pages 2-2)

References

1. (aversa2019newaluminumalloys pages 8-10): Alberta Aversa, Giulio Marchese, Abdollah Saboori, Emilio Bassini, Diego Manfredi, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. New aluminum alloys specifically designed for laser powder bed fusion: a review. Materials, 12:1007, Mar 2019. URL: https://doi.org/10.3390/ma12071007, doi:10.3390/ma12071007. This article has 304 citations.

2. (mair2022microstructuralfeaturesand pages 2-3): Philipp Mair, Ilse Letofsky-Papst, and Gerhard Leichtfried. Microstructural features and mechanical properties of a novel ti- and zr-modified al-mn alloy processed by laser powder bed fusion. Journal of Alloys and Compounds, 897:163156, Mar 2022. URL: https://doi.org/10.1016/j.jallcom.2021.163156, doi:10.1016/j.jallcom.2021.163156. This article has 25 citations and is from a peer-reviewed journal.

3. (mair2022microstructuralfeaturesand pages 6-7): Philipp Mair, Ilse Letofsky-Papst, and Gerhard Leichtfried. Microstructural features and mechanical properties of a novel ti- and zr-modified al-mn alloy processed by laser powder bed fusion. Journal of Alloys and Compounds, 897:163156, Mar 2022. URL: https://doi.org/10.1016/j.jallcom.2021.163156, doi:10.1016/j.jallcom.2021.163156. This article has 25 citations and is from a peer-reviewed journal.

4. (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3): Bharat Mehta, Lars Nyborg, Karin Frisk, and Eduard Hryha. Al–mn–cr–zr-based alloys tailored for powder bed fusion-laser beam process: alloy design, printability, resulting microstructure and alloy properties. Journal of Materials Research, 37:1256-1268, Mar 2022. URL: https://doi.org/10.1557/s43578-022-00533-1, doi:10.1557/s43578-022-00533-1. This article has 20 citations and is from a peer-reviewed journal.

5. (martucci2022theinfluenceof pages 1-2): Alessandra Martucci, Bharat Mehta, Mariangela Lombardi, and Lars Nyborg. The influence of processing parameters on the al-mn enriched nano-precipitates formation in a novel al-mn-cr-zr alloy tailored for power bed fusion-laser beam process. Metals, 12:1387, Aug 2022. URL: https://doi.org/10.3390/met12081387, doi:10.3390/met12081387. This article has 5 citations.

6. (mehta2022al–mn–cr–zrbasedalloystailored pages 2-2): Bharat Mehta, Lars Nyborg, Karin Frisk, and Eduard Hryha. Al–mn–cr–zr-based alloys tailored for powder bed fusion-laser beam process: alloy design, printability, resulting microstructure and alloy properties. Journal of Materials Research, 37:1256-1268, Mar 2022. URL: https://doi.org/10.1557/s43578-022-00533-1, doi:10.1557/s43578-022-00533-1. This article has 20 citations and is from a peer-reviewed journal.

7. (mehta2022al–mn–cr–zrbasedalloystailored pages 1-2): Bharat Mehta, Lars Nyborg, Karin Frisk, and Eduard Hryha. Al–mn–cr–zr-based alloys tailored for powder bed fusion-laser beam process: alloy design, printability, resulting microstructure and alloy properties. Journal of Materials Research, 37:1256-1268, Mar 2022. URL: https://doi.org/10.1557/s43578-022-00533-1, doi:10.1557/s43578-022-00533-1. This article has 20 citations and is from a peer-reviewed journal.

8. (mair2022microstructuralfeaturesand pages 1-2): Philipp Mair, Ilse Letofsky-Papst, and Gerhard Leichtfried. Microstructural features and mechanical properties of a novel ti- and zr-modified al-mn alloy processed by laser powder bed fusion. Journal of Alloys and Compounds, 897:163156, Mar 2022. URL: https://doi.org/10.1016/j.jallcom.2021.163156, doi:10.1016/j.jallcom.2021.163156. This article has 25 citations and is from a peer-reviewed journal.

9. (mair2022microstructuralfeaturesand pages 4-6): Philipp Mair, Ilse Letofsky-Papst, and Gerhard Leichtfried. Microstructural features and mechanical properties of a novel ti- and zr-modified al-mn alloy processed by laser powder bed fusion. Journal of Alloys and Compounds, 897:163156, Mar 2022. URL: https://doi.org/10.1016/j.jallcom.2021.163156, doi:10.1016/j.jallcom.2021.163156. This article has 25 citations and is from a peer-reviewed journal.

10. (mehta2023advancingnovelalmncrzr pages 3-5): Bharat Mehta, Karin Frisk, and Lars Nyborg. Advancing novel al-mn-cr-zr based family of alloys tailored for powder bed fusion-laser beam process. Journal of Alloys and Compounds, 967:171685, Dec 2023. URL: https://doi.org/10.1016/j.jallcom.2023.171685, doi:10.1016/j.jallcom.2023.171685. This article has 14 citations and is from a peer-reviewed journal.

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


TASK — Element-specific bound: Mn
Mn is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Mn LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Mn) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Mn) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Mn).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
