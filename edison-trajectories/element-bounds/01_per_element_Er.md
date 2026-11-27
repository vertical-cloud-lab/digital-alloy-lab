# Phase 1 — Per-element bound: Er

*Edison task: `ab2f5e02-d7fb-4676-8618-f65c6a5ce13e`*

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


TASK — Element-specific bound: Er
Er is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Er LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Er) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Er) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Er).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


This response proposes element-specific erbium (Er) upper bounds (wt%) for the BOFN/GA inner-solver search space, grounded in published LPBF aluminum-alloy compositions and known LPBF failure modes.

| Bound type | Proposed Er upper bound (wt%) | Anchor literature composition(s) and observed outcomes | Main justification | Key failure modes controlling the bound |
|---|---:|---|---|---|
| Conservative | 0.5 | LPBF Al-6.5Zn-2.5Mg-1.5Cu-2.0Si-0.16Zr-0.15Er used a modest Er microalloy level specifically for grain refinement / crack mitigation; LPBF Al-4.88Mn-1.66Mg-0.69Sc-0.33Zr with 0.5 wt% Er addition achieved 99.8% density and improved strength-ductility, showing 0.5 wt% is already demonstrated in printable Al-rich LPBF systems (zhang2023effectofpostheat pages 1-3, 谢启东2026effectofaddition pages 1-2) | 0.5 wt% brackets the published LPBF microalloy regime (0.15-0.5 wt% Er) and is a conservative, defensible search cap tied to actual printable Al-rich alloys rather than speculative binary Al-Er compositions (zhang2023effectofpostheat pages 1-3, 谢启东2026effectofaddition pages 1-2) | Low Er solubility in Al; reduced thermal stability / coarsening of Al3(Er,Zr) during aging; tendency toward larger grains than Sc-containing analogs; mineral-burden/cost penalty if Er is used where Zr/Sc-free benefit is small (zhang2023effectofpostheat pages 5-7, aversa2019newaluminumalloys pages 10-12) |
| Non-conservative | 10 | Binary Al-3Er single-track LPBF was scarcely processable with strong balling, discontinuous tracks, and zero penetration under typical settings, but recent LPBF Al-Er eutectic-alloy design uses near-eutectic Al-10Er and cites the Al-Er eutectic at ~12.7 wt% Er, leveraging a narrow solidification interval and eutectic nano-skeleton for printability/strength (aversa2018lasersinglescan pages 4-7, li2026strong3dprintedaluminium pages 5-10, li2026strong3dprintedaluminium media 3d73e394) | 10 wt% is an aggressive but still Al-rich cap below the ~12.7 wt% Al-Er eutectic; it reaches the demonstrated near-eutectic LPBF design space while avoiding the full eutectic limit and preserving some margin for multicomponent additions and TCAl10 trustworthiness (li2026strong3dprintedaluminium pages 5-10, li2026strong3dprintedaluminium media 3d73e394) | Outside eutectic-tailored design, intermediate Er can worsen processability (balling/poor absorptivity in binary Al-3Er); high Al3Er/intermetallic fraction can embrittle and reduce ductility; Er strongly perturbs freezing-range/printability descriptors and interacts with Zr/Ni/Y/Yb phase selection, so joint constraints are essential (aversa2018lasersinglescan pages 4-7, li2026strong3dprintedaluminium pages 5-10, taherimousavi2024additivelymanufacturablehighstrength pages 7-9) |


*Table: This table summarizes conservative and non-conservative erbium upper bounds for the LPBF aluminum BO search space, anchored to reported LPBF compositions and observed processing behavior. It is useful for setting an evidence-based Er search limit while flagging the mechanisms that should become joint constraints.*

1) CONSERVATIVE Er upper bound (wt%)

Er ≤ 0.5 wt%.

Justification: Published LPBF Al alloys commonly use Er as a microalloying addition (≈0.1–0.5 wt%) for grain refinement and precipitate-assisted strengthening; for example, an LPBF Al–Zn–Mg–Cu–Si–Zr–Er alloy was designed with 0.15 wt% Er (Al-6.5Zn-2.5Mg-1.5Cu-2.0Si-0.16Zr-0.15Er, wt%) (zhang2023effectofpostheat pages 1-3), and an LPBF Al-Mn-Mg-Sc-Zr alloy with 0.5 wt% Er addition achieved 99.8% density and formed Al3Er (谢启东2026effectofaddition pages 1-2).

2) NON-CONSERVATIVE Er upper bound (wt%)

Er ≤ 10 wt%.

Justification: A recent LPBF Al–Er eutectic-alloy design explicitly targets near-eutectic compositions and cites an Al–Er eutectic at ~12.7 wt% Er while using Al–10Er (wt%) as a representative near-eutectic composition, leveraging the narrow solidification interval for improved resistance to solidification cracking/printability (li2026strong3dprintedaluminium pages 5-10, li2026strong3dprintedaluminium media 3d73e394). Setting 10 wt% stays below the eutectic limit while reaching the demonstrated near-eutectic LPBF design space.

3) Key failure modes that set each bound

Conservative bound (≤0.5 wt%):
- Precipitate thermal stability / coarsening: Er has low solubility in Al and Er-containing L12 precipitates have reduced thermal stability and readily grow with ageing; in an LPBF Al–Zn–Mg–Cu–Si–Zr–Er alloy, Al3(Er,Zr) coarsened markedly with heat treatment (≈79→248 nm), and coarsening was linked to loss of strengthening (zhang2023effectofpostheat pages 5-7, aversa2019newaluminumalloys pages 10-12).
- Solidification grain structure: Review evidence indicates Er can lead to larger solidification grains than Sc-containing analogs (aversa2019newaluminumalloys pages 10-12), which is unfavorable for cracking resistance in many AM Al systems.
- Mineral-burden objective: Er is a rare earth and will typically carry a higher criticality/import reliance penalty than common alloying elements; keeping Er microalloyed reduces that penalty while still allowing Er–Zr/Er–(Sc,Zr) L12 precipitation pathways (aversa2019newaluminumalloys pages 10-12).

Non-conservative bound (≤10 wt%):
- LPBF processability sensitivity at intermediate Er in binary-like systems: single-track LPBF tests on Al-3 wt% Er were “scarcely processable” with strong balling, discontinuous tracks, and essentially zero substrate penetration under typical parameters—implying that without co-alloying to improve absorptivity/solidification behavior, Er additions can sharply degrade printability and narrow the process window (aversa2018lasersinglescan pages 4-7).
- Intermetallic fraction / embrittlement-strength–ductility tradeoff: near-eutectic Al alloys can embrittle because intermetallics can fracture readily; even in eutectic-strengthened concepts there is an inherent trade-off where very high strength is commonly associated with low elongation (li2026strong3dprintedaluminium pages 5-10).
- Feedstock heterogeneity risk (if Er introduced via particulates/in-situ alloying): Er-bearing nanoparticle additions can aggregate, promoting cracks and lack-of-fusion cavities; laser heating can dissociate particles and form intermetallic phases (jandaghi2023developmentofthe pages 136-138).
- Multi-component phase competition: ML/CALPHAD-based LPBF alloy design finds Er strongly influences freezing-range/printability metrics and interacts with Zr (and Ni/Y/Yb) in Scheil/solidification; excessive Er can drive undesirable solidification-formed phases unless jointly constrained (taherimousavi2024additivelymanufacturablehighstrength pages 7-9).

4) Element-specific caveats / interactions for joint-constraints analysis

- Strong co-dependence with Zr (and sometimes Ni): In LPBF alloy design, Er and Zr jointly control L12 fraction and coarsening, and Er can help partition Zr into L12 rather than forming brittle Al3Zr; bounds on Er should therefore be co-enforced with Zr (and possibly Ni) to avoid coarse primary intermetallics and maintain printability descriptors (taherimousavi2024additivelymanufacturablehighstrength pages 7-9).
- Absorptivity/Si interaction: Poor LPBF processability of Al-3Er was attributed partly to low laser absorption “probably caused by the lack of Si,” suggesting Er-rich compositions should be coupled to absorptivity-enhancing additions (e.g., Si) and/or parameter windows; otherwise balling/poor penetration can dominate (aversa2018lasersinglescan pages 4-7).
- Eutectic-targeted versus precipitation-targeted regimes: The ~10–13 wt% Er regime is justified only if the alloy is explicitly designed around Al–Er near-eutectic solidification (narrow freezing range, eutectic skeleton) (li2026strong3dprintedaluminium pages 5-10, li2026strong3dprintedaluminium media 3d73e394); it is not a general-purpose upper bound for conventional Al-rich precipitation-strengthened LPBF alloys.
- Heat-treatment sensitivity: Even at microalloy levels, Al3(Er,Zr) coarsening under T6/RRA-type cycles can erase strengthening; any BO objective using heat treatment should treat Er effectiveness as process-path dependent (zhang2023effectofpostheat pages 5-7, zhang2023effectofpostheat pages 9-11).


References

1. (zhang2023effectofpostheat pages 1-3): Zhiqian Zhang, Dehua Li, Shengci Li, Hui Tang, Yu Zhang, Tingting Dong, Weirong Li, Yanfang Li, and Olanrewaju A. Ojo. Effect of post-heat treatment on the microstructure, mechanical, and corrosion properties of laser powder bed fused al–zn–mg–cu–si–zr–er alloys. Journal of Materials Research and Technology, 27:1350-1364, Nov 2023. URL: https://doi.org/10.1016/j.jmrt.2023.10.009, doi:10.1016/j.jmrt.2023.10.009. This article has 24 citations and is from a peer-reviewed journal.

2. (谢启东2026effectofaddition pages 1-2): 李素丽， 张晏泽， 杨蒙佳， 张龙博， 谢启东. Effect of addition of er-tib2 dual-phase nanoparticles on strength-ductility of al-mn-mg-sc-zr alloy prepared by laser powder bed fusion. Unknown journal, 2026. URL: https://doi.org/10.0000/1002-185x(2025)01-0009-09, doi:10.0000/1002-185x(2025)01-0009-09.

3. (zhang2023effectofpostheat pages 5-7): Zhiqian Zhang, Dehua Li, Shengci Li, Hui Tang, Yu Zhang, Tingting Dong, Weirong Li, Yanfang Li, and Olanrewaju A. Ojo. Effect of post-heat treatment on the microstructure, mechanical, and corrosion properties of laser powder bed fused al–zn–mg–cu–si–zr–er alloys. Journal of Materials Research and Technology, 27:1350-1364, Nov 2023. URL: https://doi.org/10.1016/j.jmrt.2023.10.009, doi:10.1016/j.jmrt.2023.10.009. This article has 24 citations and is from a peer-reviewed journal.

4. (aversa2019newaluminumalloys pages 10-12): Alberta Aversa, Giulio Marchese, Abdollah Saboori, Emilio Bassini, Diego Manfredi, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. New aluminum alloys specifically designed for laser powder bed fusion: a review. Materials, 12:1007, Mar 2019. URL: https://doi.org/10.3390/ma12071007, doi:10.3390/ma12071007. This article has 304 citations.

5. (aversa2018lasersinglescan pages 4-7): A Aversa, F Bosio, S Marola, and M Lorusso. Laser single scan tracks of new aluminium alloys compositions. Unknown journal, 2018.

6. (li2026strong3dprintedaluminium pages 5-10): Yang Li, Tingting Chen, Shengyi Zhong, Haixing Fang, Pucong Sheng, Siming Ma, Han Chen, Yuchi Cui, Gang Ji, Yihao Wang, Yirui Chang, Lei Hu, Mingliang Wang, Shixin Nie, Haowei Wang, and Zhe Chen. Strong 3d-printed aluminium reinforced with ductile-transformable eutectic nano-skeleton. Nature Communications, Apr 2026. URL: https://doi.org/10.1038/s41467-026-72256-4, doi:10.1038/s41467-026-72256-4. This article has 0 citations and is from a highest quality peer-reviewed journal.

7. (li2026strong3dprintedaluminium media 3d73e394): Yang Li, Tingting Chen, Shengyi Zhong, Haixing Fang, Pucong Sheng, Siming Ma, Han Chen, Yuchi Cui, Gang Ji, Yihao Wang, Yirui Chang, Lei Hu, Mingliang Wang, Shixin Nie, Haowei Wang, and Zhe Chen. Strong 3d-printed aluminium reinforced with ductile-transformable eutectic nano-skeleton. Nature Communications, Apr 2026. URL: https://doi.org/10.1038/s41467-026-72256-4, doi:10.1038/s41467-026-72256-4. This article has 0 citations and is from a highest quality peer-reviewed journal.

8. (taherimousavi2024additivelymanufacturablehighstrength pages 7-9): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

9. (jandaghi2023developmentofthe pages 136-138): M Jandaghi. Development of the additively manufactured stainless steel 316l and alsi10mg alloys by in situ alloying and post-process treatment. Unknown journal, 2023.

10. (zhang2023effectofpostheat pages 9-11): Zhiqian Zhang, Dehua Li, Shengci Li, Hui Tang, Yu Zhang, Tingting Dong, Weirong Li, Yanfang Li, and Olanrewaju A. Ojo. Effect of post-heat treatment on the microstructure, mechanical, and corrosion properties of laser powder bed fused al–zn–mg–cu–si–zr–er alloys. Journal of Materials Research and Technology, 27:1350-1364, Nov 2023. URL: https://doi.org/10.1016/j.jmrt.2023.10.009, doi:10.1016/j.jmrt.2023.10.009. This article has 24 citations and is from a peer-reviewed journal.

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


TASK — Element-specific bound: Er
Er is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Er LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Er) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Er) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Er).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
