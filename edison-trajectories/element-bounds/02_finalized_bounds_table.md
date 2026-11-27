# Phase 2 — Finalized bounds table (Edison ANALYSIS)

*Edison task: `caec5419-4ced-44f3-b902-68a3e84fadf6`*

## Answer

### Finalized BOFN compositional search-space bounds

| Element | Lower bound (wt%) | Recommended upper bound (wt%) | Conservative upper (wt%) | Non-conservative upper (wt%) | Primary failure mode setting upper bound | Notes / caveats | Key citations |
|---|---:|---:|---:|---:|---|---|---|
| **Al** | **85.0** | **100.0** | 99.5 | 99.9 | Balance element; practical simplex / leaving Al-rich CALPHAD region if too low | Use **Al as balance** with an explicit **Al_min = 85 wt%**. This keeps BOFN in the Al-rich TCAl10/Muggianu region while still allowing up to 15 wt% total solute for k=3..8 active elements. | `01_simultaneous_all_bounds`; `01_per_element_Al`; `01_lower_bound` |
| **Mn** | 0.0 | **5.0** | 5.0 | 8.0 | Mn-rich intermetallic precipitation / loss of metastable supersaturation | I chose 5.0 wt% because LPBF evidence supports it, it covers the Al-Mn-Cr-Zr anchor family, and simplex + Mn+Cr joint constraints stop pathological combined loading. The 0.05–0.10 wt% activity floor is enough when Mn is “on.” | `mair2022microstructuralfeaturesand`; `mehta2022al–mn–cr–zrbasedalloystailored`; `martucci2022theinfluenceof` |
| **Cr** | 0.0 | **3.0** | 3.0 | 6.0 | Primary Al-Cr intermetallic formation and narrowed LPBF process window | The per-element file allowed up to 6 wt% Cr, but the joint synthesis pulled this back to 3 wt% to stay in a more credible TCAl10 region and reduce risk of coarse Al₅Cr/Al₇Cr phases. | `kimura2021microstructuraldevelopmentand`; `stopyra2020laserpowderbed`; `01_simultaneous_all_bounds` |
| **Zr** | 0.0 | **1.0** | 1.0 | 2.0 | Primary Al₃Zr formation / coarsening and porosity sensitivity | 1 wt% is the practical BOFN cap. It captures the grain-refining benefit seen in LPBF without leaning too hard on poorly assessed high-Zr corners. If Sc and Zr are both active, treat **0.2 wt% each** as a practical minimum and enforce **Sc+Zr ≤ 1.5 wt%** conservatively. | `mertens2021laserpowderbed`; `yu2022processingandcharacterization`; `glerum2020synthesisofprecipitationstrengthened` |
| **Mg** | 0.0 | **5.0** | 5.0 | 8.0 | Evaporation / spatter / composition drift, plus hot cracking | 8 wt% Mg has been printed in tailored systems, but evaporation is already serious there. For BOFN, 5 wt% is the cleaner choice because it respects LPBF transfer-function reality and avoids spending too much search volume on Mg-burnoff corners. Consider joint cap **Mg+Zn+Li ≤ 10 wt%**. | `babu2021developmentofhigh`; `zhou2019microstructureandmechanical`; `li2020developingahighstrength` |
| **Si** | 0.0 | **12.0** | 12.0 | 14.0 | Transition to hypereutectic behavior with primary Si precipitation | 12 wt% captures the eutectic Al-Si printable regime and the main crack-mitigation role of Si. Going higher is possible, but it starts to trade BOFN volume toward coarse primary Si and stronger process sensitivity. If Si is active for crack suppression, a functional floor around **3–4 wt%** is defensible. | `brock2020laserpowderbed`; `bohm2020dilutionratioand`; `li2021investigationofsolidification` |
| **Cu** | 0.0 | **4.0** | 4.0 | 7.0 | Wide freezing range / solidification cracking and θ-Al₂Cu segregation | Per-element literature found higher Cu possible in tailored systems, but for a single shared search space 4 wt% is the safer BOFN choice because Cu strongly worsens cracking in broad Al-rich multicomponent regions and also carries mineral-burden penalty. Enforce **Cu+Mg ≤ 5 wt%** conservatively. | `belelli2022effectofcu`; `mair2021microstructureandmechanical`; `bosio2021strengtheningstrategiesfor` |
| **Ti** | 0.0 | **0.5** | 0.5 | 1.5 | Primary Al₃Ti / hyperperitectic intermetallic formation | I used the joint conservative value. Higher Ti only makes sense on a specific Ti-B manifold; otherwise it mostly creates Al₃Ti risk and atomization trouble. This is a place where the literature is conditional rather than broad. | `larini2023microstructuralevolutionof`; `belelli2021investigationontwo`; `mair2022microstructuralfeaturesand` |
| **Fe** | 0.0 | **0.5** | 0.5 | 2.0 | Brittle Fe-rich intermetallics, especially β-Al₅FeSi-type morphologies | The per-element file noted 5 wt% Fe in dedicated high-temperature Al-Fe-Cr systems, but the joint synthesis reduced Fe to 0.5 wt% for a general BOFN space. That’s the right call here. If Fe is intentionally elevated above 0.3 wt%, use Mn to redirect phase morphology and watch Fe+Si. | `yamasaki2019effectoffe`; `wang2021processabilityandoptimization`; `perezprado2022anal5fe6cralloy` |
| **Ni** | 0.0 | **0.5** | 0.5 | 2.0 | Brittle Al-Ni intermetallic networks and cracking | Per-element Ni had a eutectic-targeted non-conservative ceiling around 5.7 wt%, but for the shared BOFN space 0.5 wt% is the better recommendation. Ni also adds mineral-burden cost and has thin evidence outside targeted eutectic designs. | `deng2021ahighstrengthheatresistant`; `koutny2018influenceofscanning`; `wang2023influenceofni` |
| **Ce** | 0.0 | **6.0** | 6.0 | 12.0 | Primary Al₁₁Ce₃ and Ce-rich network formation | The per-element file went as high as 10–15 wt% Ce in near-eutectic systems. I recommend 6 wt% for BOFN because it preserves access to Ce-containing discovery space without overcommitting the search to rare-earth-heavy, oxidation-sensitive corners. Pre-alloyed feedstock is preferred over elemental blending. | `zhou2020laserpowderbed`; `hesselmann2022effectofprecipitationforming`; `yakubov2022laserpowderbed` |
| **Sc** | 0.0 | **0.8** | 0.8 | 1.5 | Cost/criticality plus primary Al₃(Sc,Zr) formation that wastes solute | 0.8 wt% matches Scalmalloy-class practice and is the obvious BOFN cap. Higher Sc is possible, but it quickly becomes a mineral-burden loser and starts consuming Sc in primary phases rather than useful nano-precipitates. | `janus2025microstructureandmechanical`; `glerum2020synthesisofprecipitationstrengthened`; `yan2023microstructuresandhigh` |
| **Li** | 0.0 | **2.0** | 2.0 | 3.0 | Evaporation / atmosphere sensitivity and δ′(Al₃Li)-related embrittlement | I kept the joint conservative value. LPBF at 3 wt% Li exists, but density penalties and Li loss are already substantial. This is a candidate for explicit transfer-function correction if BOFN insists on exploring it. | `qi2019analuminumlithiumallloy`; `shao2024microstructureandmechanical`; `yurekliaUnknownyear3dprintingof` |
| **Er** | 0.0 | **0.5** | 0.5 | 1.5 | Al₃Er intermetallic formation / coarsening; poor general LPBF robustness outside targeted eutectics | Per-element Er had a very high non-conservative ceiling in near-eutectic Al-Er concepts, but the evidence for broad use is thin. For BOFN, 0.5 wt% is the defensible cap. Treat higher Er as a follow-up branch, not default search volume. | `zhang2023effectofpostheat`; `aversa2019newaluminumalloys`; `li2026strong3dprintedaluminium` |
| **Zn** | 0.0 | **8.0** | 8.0 | 15.0 | Zn evaporation / composition drift plus hot cracking in Al-Zn-Mg corridors | Per-element work found 6.5 wt% conservative and 14.5 wt% non-conservative; the joint synthesis originally listed 8/20, but the non-conservative ceiling is **capped at 15 wt%** because the simplex constraint with **Al_min = 85 wt%** caps any single non-Al element at 15 wt%. I recommend **8 wt%** because it preserves 7xxx-like exploration but avoids dedicating too much search to Zn-loss-dominated space. Enforce volatile-elements cap **Mg+Zn+Li ≤ 10 wt%** conservatively. | `babu2020laserpowderbed`; `babu2021onthecorrosion`; `mertens2021laserpowderbed` |
| **Sn** | 0.0 | **0.1** | 0.1 | 0.5 | Monotectic immiscibility and low-melting Sn-rich grain-boundary films | This one is simple: keep Sn near trace level in the default BOFN space. The per-element file had a much larger exploratory ceiling under the project’s Al-rich constraint, but the LPBF evidence is thin and failure modes are ugly. | `confalonieri2021alsnmiscibilitygap`; `specht2021shockcompressionresponse`; `schmidfetzer2009thermodynamicaspectsof` |

**Implementation note:** for all non-Al elements, use **global lower bound = 0 wt%**. If an element is active, apply a **practical activity floor of 0.05–0.10 wt%** to reflect AMAZEMET rePOWDER dosing/reproducibility limits and to prevent pseudo-active trace values. For Si, Sc, and Zr, you may optionally enforce stronger functional floors in downstream experiments, but I would not hard-code them into the global BOFN box bounds.

1. **Chosen Al_min:** **85 wt%**.

   Why 85 wt%:
   - It matches the joint-synthesis recommendation and keeps the search in the Al-rich corner where **TCAl10 + Muggianu binary/ternary extrapolation** is still reasonably trustworthy.
   - It leaves **15 wt% total non-Al budget**, which is enough for the anchor Al-Mn-Cr-Zr family, Al-Si-type crack-mitigated systems, and moderate 7xxx-like exploration, while still respecting the project’s LPBF-processability premise.
   - With **k = 3..8 active non-Al elements**, 85 wt% Al gives enough room that the optimizer can allocate meaningful multi-element doses instead of wasting the budget on floors, but it does not open the door too far into high-solute, crack-prone, poorly assessed corners.

2. **Cases with substantial conservative vs non-conservative disagreement, and how I resolved them:**

   - **Mn:** per-element conservative/non-conservative was **0.7 / 5.0 wt%**, while the joint synthesis used **5 / 8 wt%**. I adopted **5 wt% recommended** because Mn is central to the anchor system and LPBF evidence at ~5 wt% is solid.
   - **Cr:** per-element **0.3 / 6 wt%** vs joint **3 / 6 wt%**. I used **3 wt% recommended** because it is a cleaner compromise between demonstrated high-Cr LPBF feasibility and TCAl10 coverage.
   - **Cu:** per-element **4.5 / 12 wt%** vs joint **4 / 7 wt%**. I used **4 wt% recommended** because the broader BOFN space should not spend much volume in high-Cu cracking territory.
   - **Ti:** per-element **1.0 / 3.7 wt%** with the high end only valid on a **Ti-B manifold**; joint **0.5 / 1.5 wt%**. I used **0.5 wt% recommended** because the broad search space should not assume Ti-B stoichiometric pairing unless encoded explicitly.
   - **Fe:** per-element **0.1 / 5 wt%** vs joint **0.5 / 2 wt%**. I used **0.5 wt% recommended** as a compromise that still keeps Fe mostly out of the search unless intentionally used.
   - **Ni:** per-element **1.5 / 5.7 wt%** vs joint **0.5 / 2 wt%**. I used **0.5 wt% recommended** because high-Ni LPBF evidence is narrow and eutectic-specific.
   - **Ce:** per-element **10 / 15 wt%** vs joint **6 / 12 wt%**. I used **6 wt% recommended** to preserve Ce exploration without over-weighting rare-earth-heavy corners.
   - **Er:** per-element **0.5 / 10 wt%** vs joint **0.5 / 1.5 wt%**. I used **0.5 wt% recommended** because the 10 wt% case is really a separate near-eutectic Al-Er design branch, not a general BOFN bound.
   - **Zn:** per-element **6.5 / 14.5 wt%** vs joint **8 / 20 wt%**. I used **8 wt% recommended** because it aligns with exploratory 7xxx-like design while keeping Zn-loss burden somewhat bounded. The joint non-conservative value of 20 wt% is **capped at 15 wt%** to respect the Al_min = 85 wt% simplex constraint (no single non-Al element can exceed 1 − Al_min = 15 wt%).
   - **Sn:** per-element **0.05 / 15 wt%** vs joint **0.1 / 0.5 wt%**. I used **0.1 wt% recommended** because the high-Sn space is far outside the robust LPBF alloy-design region intended here.

3. **Elements with thin or contradictory evidence that should get follow-up CALPHAD or experiment in Activity 1/2:**

   - **Sn:** strongest candidate. Evidence outside trace levels is thin and dominated by immiscibility failure modes.
   - **Er:** contradictory because microalloying looks plausible, but high-Er eutectic concepts are a different regime entirely.
   - **Ti:** literature support is conditional on Ti-B coupling; broad Ti-alone bounds are weak.
   - **Ni:** high-Ni feasibility is mostly eutectic-targeted, not general multicomponent Al-rich LPBF design.
   - **Ce:** workable in dedicated pre-alloyed near-eutectic systems, but transferability to multicomponent BOFN corners is uncertain.
   - **Li:** strong process sensitivity to atmosphere and evaporation means nominal composition is a poor proxy for retained composition.
   - **High-Zn / high-Mg / high-Li corners generally:** these need explicit powder-to-build composition transfer functions or at least a volatility penalty, because nominal bounds alone will misrepresent the realized alloy.

- Applied **global lower bound = 0 wt%** for all non-Al elements, while preserving a **practical activity floor of 0.05–0.10 wt%** when an element is switched on.
- Chose **Al_min = 85 wt%** from the joint synthesis rather than the stricter 90–95 wt% values in some lower-bound trajectories, because 85 wt% better fits the project’s k=3..8 sparse multicomponent search while still staying in the Al-rich TCAl10 region.
- Treated the **joint/simultaneous synthesis** as the main arbiter for conservative and non-conservative ceilings when it materially disagreed with single-element files, because the BOFN search space is shared across all elements rather than optimized one element at a time.
- Selected **recommended upper bounds** to favor the **joint conservative value**, except where strong LPBF evidence and project relevance justified a slightly broader recommendation within the joint framework (notably Mn at 5 wt% and Zn at 8 wt%).
- Prioritized **TCAl10 coverage and LPBF realizability** over isolated literature demonstrations in specialized eutectic systems when choosing the recommended upper bound.
- Treated **mineral-burden / criticality** as a real down-selection pressure when setting recommended bounds for **Sc, Ce, Er, Ni, and Cu**.
- Interpreted **AMAZEMET rePOWDER dosing/reproducibility** as affecting **lower practical activity floors**, not as the primary determinant of upper bounds.
- Preserved several **joint constraints** from the simultaneous-bounds synthesis as implementation notes rather than forcing them into the per-element box-bound columns: e.g. **Mn+Cr ≤ 7 wt%**, **Sc+Zr ≤ 1.5 wt%**, **Cu+Mg ≤ 5 wt%**, **Cu+Li ≤ 4 wt%**, **Mg+Si ≤ 6 wt% with caution near Mg/Si ≈ 1.5–2.0**, and **Mg+Zn+Li ≤ 10 wt%** conservatively.

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


TASK — FINALIZED BOUNDS TABLE (synthesis)

Attached are the markdown trajectories from a batch of LITERATURE-mode
Edison queries that asked, separately and jointly, for upper / lower
compositional bounds on each of the 16 elements:
    Al, Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn

Synthesize ALL of the attached trajectories (per-element upper-bound
queries, the lower-bound query, and the joint simultaneous-bounds query)
into ONE finalized markdown bounds table that the FLAIME team can drop
directly into the BOFN search-space definition. The table must contain,
for each element, exactly these columns:

| Element | Lower bound (wt%) | Recommended upper bound (wt%) | Conservative upper (wt%) | Non-conservative upper (wt%) | Primary failure mode setting upper bound | Notes / caveats | Key citations |

Conventions:
  * Recommended upper bound = the bound the FLAIME team should USE in the
    BOFN search space (justify the choice between conservative and
    non-conservative based on TCAl10 coverage, dosing accuracy of the
    AMAZEMET rePOWDER induction crucible, and the project's k=3..8 sparsity
    pattern).
  * Lower bound is 0 wt% for non-Al elements unless the synthesis
    determines a defensible nonzero floor (e.g. dosing detection limit ~0.05
    wt% if present at all).
  * Al lower bound: pick a single Al_min and justify it.

Below the table:
  1. State the chosen Al_min in wt% and explain.
  2. Note any per-element cases where the conservative and non-conservative
    estimates from the LITERATURE queries disagreed substantially, and how
    you resolved it.
  3. Flag any elements where Edison's LITERATURE responses had thin or
    contradictory evidence — these are candidates for follow-up CALPHAD or
    experimental verification in Activity 1 / Activity 2.

Output: a single, copy-pasteable markdown section.
```
