Question: CONTEXT: FLAIME is a DOE Genesis Mission Phase I proposal ($500-750K, 9 months) for Topic 3B: "AI-Enabled Materials Discovery and Engineering — Reducing Demand for Critical Minerals" (AMMTO). It is an autonomous closed-loop alloy discovery platform: CALPHAD → ultrasonic atomization → LPBF 3D printing → ASTM E8 tensile testing → BOFN (Bayesian Optimization with Function Networks) optimization. Material strategy: Al-Zr and Al-Mn-Cr-Zr families PRIMARY (~80%), Cu-Cr-Zr COMPLEMENT (~20% stretch for Be-Cu replacement). AlSi10Mg is benchmark only.

KPI UNDER REVIEW: "Mineral-Lean Discovery Yield" — fraction of BOFN-proposed alloys meeting BOTH performance threshold (YS≥250 MPa AND EL≥5%) AND critical-mineral avoidance (0 wt% Mg/Sc/REE/Be). Phase I target: ≥30% of tested compositions. Phase II target: ≥50%.

Provide a critical literature-grounded review of this KPI:
1. Is ≥30% Discovery Yield realistic for a 9-month Phase I on novel Al-Zr and Al-Mn-Cr-Zr LPBF alloys? What does the literature say about typical hit rates in BOFN-guided or BO-guided alloy discovery campaigns? Reference specific SDL campaigns (e.g., BIRDSHOT/ULTIMATE, A-Lab, Abolhasani SDL campaigns) and their yield fractions.
2. Is YS≥250 MPa AND EL≥5% the right threshold for mineral-lean Al alloys? Compare against Ge et al. (2025) Al-Zr-Er-Ni (279 MPa as-built, 16% EL but with Er REE), Arena et al. (2024) Al-5Mn-0.8Cr-0.6Zr (250 MPa as-printed), and the AlSi10Mg benchmark (250-300 MPa / 5-10% EL). Should the threshold be family-specific?
3. Is "0 wt% Mg/Sc/REE/Be" the right mineral-avoidance definition? The USGS critical minerals list includes Zr, Mn, Cr — should these be addressed? How does the framing "reduce dependence on supply-constrained critical minerals (Mg, Sc, REEs)" differ from "mineral-lean"?
4. What improvements or alternative formulations would make this KPI stronger for a DOE reviewer?

# Critical Literature-Grounded Review of the FLAIME "Mineral-Lean Discovery Yield" KPI

## 1. Is ≥30% Discovery Yield Realistic for a 9-Month Phase I?

### Benchmarking Against Published SDL/BO Campaigns

The proposed 30% discovery yield—defined as the fraction of BOFN-proposed alloys meeting both performance (YS≥250 MPa AND EL≥5%) and mineral-avoidance (0 wt% Mg/Sc/REE/Be) criteria—can be benchmarked against several published autonomous and BO-guided materials discovery campaigns.

| Campaign/Platform | Domain | Optimization Method | Number Tested | Number Successful/Meeting Targets | Hit Rate/Success Rate | Time Frame |
|---|---|---|---|---|---|---|
| BIRDSHOT/ULTIMATE | Refractory HEAs / compositionally complex alloys | Batch Bayesian optimization with high-throughput synthesis/characterization | 140 unique alloys synthesized overall; 24 alloys in reported iteration 2 | 10 of 24 iteration-2 alloys dominated all iteration-1 alloys on both objectives | ~42% in iteration 2 (10/24); full campaign target-hit fraction not explicitly reported | ~2 years program-scale; two full design cycles completed in a few months (paramore2025twoshotoptimizationof pages 16-18, arroyave2024ultimatebirdshot.final pages 9-11, paramore2025twoshotoptimizationof pages 1-3, arroyave2024ultimatebirdshot.final pages 1-5) |
| A-Lab | Autonomous inorganic solid-state synthesis / ceramics | Active learning + thermodynamics + ML recipe generation | 58 targets; 355 experiments/recipes | 41 of 58 targets realized | 71% target success; ~37% recipe-level success | 17 days (szymanski2023anautonomouslaboratory pages 2-3, szymanski2023anautonomouslaboratory pages 4-5, szymanski2023anautonomouslaboratory pages 3-4, szymanski2023anautonomouslaboratory pages 1-2) |
| Abolhasani SDL campaigns | Perovskite nanocrystals / photocatalysts / fluidic materials optimization | BO, ensemble ML, and RL in self-driving fluidic labs | 250 autonomously selected experiments in one campaign; 688 experiments in another | Not consistently reported as a simple hit fraction; reported as discovery/optimization acceleration | 10-1000× acceleration vs conventional methods; 60-fold fewer experiments in one optimization example | Days to weeks; e.g. 8-day unattended run (abolhasani2023theriseof pages 3-4, volk2024performancemetricsto pages 1-2) |
| FLAIME target | LPBF Al alloy discovery (Al-Zr, Al-Mn-Cr-Zr; mineral-lean focus) | BOFN over a closed-loop process network (CALPHAD → atomization → LPBF → tensile test) | Not yet reported; Phase I target defined over tested compositions | Target: ≥30% of tested compositions meeting both performance and mineral-avoidance criteria | ≥30% target in Phase I; ≥50% target in Phase II | 9 months Phase I (astudillo2021bayesianoptimizationof pages 1-2, buathong2023bayesianoptimizationof pages 1-2, zhang2024practicalandtheoretical pages 64-68) |


*Table: This table compares published self-driving and BO-guided materials discovery campaigns with the proposed FLAIME KPI target. It helps benchmark whether a 30% Phase I discovery yield is conservative, aggressive, or roughly aligned with prior autonomous discovery programs.*

**BIRDSHOT/ULTIMATE (ARPA-E refractory HEAs).** This is the most directly comparable campaign in spirit: high-throughput alloy synthesis and characterization with batch Bayesian optimization. The BIRDSHOT program synthesized 140 unique refractory high-entropy alloy compositions, characterized 108 by SEM/EDX/XRD, and performed Vickers microhardness on 60 as-cast and 108 homogenized samples (arroyave2024ultimatebirdshot.final pages 9-11, arroyave2024ultimatebirdshot.final pages 1-5). In the "two-shot" optimization reported by Paramore et al. (2025), the second BO-guided iteration of 24 alloys yielded 10 compositions (42%) that dominated all first-iteration alloys on both target objectives (specific hardness and specific modulus), with a 54% improvement in Pareto hypervolume (paramore2025twoshotoptimizationof pages 16-18, paramore2025twoshotoptimizationof pages 1-3). However, the BIRDSHOT campaign did not report a formal "hit rate" against predefined performance thresholds analogous to the FLAIME KPI, and the full campaign operated over approximately two years with multiple iterations—substantially longer than a 9-month Phase I (arroyave2024ultimatebirdshot.final pages 5-7).

**A-Lab (Berkeley autonomous synthesis).** The A-Lab achieved a 71% target-level success rate (41 of 58 novel inorganic compounds synthesized) over 17 days, though the per-recipe success rate was much lower at ~37% (130/355 experiments) (szymanski2023anautonomouslaboratory pages 2-3, szymanski2023anautonomouslaboratory pages 4-5, szymanski2023anautonomouslaboratory pages 3-4). This high target-level success rate reflects that the A-Lab operated in a domain (solid-state ceramics synthesis) with substantial prior computational screening (Materials Project + GNoME predictions) and extensive literature-trained recipe generation. The FLAIME context is fundamentally different: there is no equivalent prior computational database for LPBF-printable Al alloy compositions, and the testing pipeline (atomization → LPBF → tensile testing) is orders of magnitude slower than powder mixing and furnace synthesis.

**Abolhasani SDL campaigns (flow chemistry/nanocrystals).** Abolhasani's self-driving fluidic laboratories have demonstrated 10–1,000× acceleration over conventional methods, with campaigns of 250–688 experiments finding optimal conditions autonomously (abolhasani2023theriseof pages 3-4). A key advantage of these platforms is fully integrated online characterization (spectroscopy), enabling experiment cycle times of minutes. The FLAIME pipeline—powder atomization, LPBF printing, ASTM E8 tensile testing—has cycle times of days to weeks per composition, fundamentally limiting the number of BO iterations achievable in 9 months.

### Assessment of the 30% Target

The 30% threshold is **ambitious but defensible** for the following reasons:

*Arguments supporting feasibility:* (i) BOFN, which models each node in the CALPHAD→atomization→LPBF→testing pipeline with separate Gaussian processes, can exploit intermediate outputs to prune unpromising compositions before full tensile testing, improving sample efficiency compared to standard BO (astudillo2021bayesianoptimizationof pages 1-2, buathong2023bayesianoptimizationof pages 1-2); (ii) the BIRDSHOT "two-shot" result of 42% domination in the second iteration demonstrates that BO-guided alloy campaigns can achieve high improvement rates in early iterations; (iii) the Al-Mn-Cr-Zr system already has demonstrated baseline compositions near the threshold (see Section 2), providing an informed starting point.

*Arguments suggesting risk:* (i) No published SDL campaign has operated a closed-loop CALPHAD→LPBF→tensile testing pipeline; the throughput bottleneck of LPBF printing and ASTM E8 testing may limit the total number of compositions tested to 15–30 over 9 months, making a 30% yield target (i.e., 5–10 hits out of 15–30 tested) sensitive to statistical fluctuations; (ii) the compound constraint of meeting both YS AND EL simultaneously AND the mineral screen narrows the feasible space substantially compared to single-objective campaigns; (iii) the A-Lab's high success rate was predicated on substantial prior computational screening, and without an equivalent pre-filtering of LPBF-viable compositions, early BOFN iterations will likely include more exploration (and failures).

**Recommendation:** Consider defining the Phase I target as ≥20–25% with an aspirational stretch of ≥30%, or explicitly tie the yield to iteration number (e.g., "≥30% in the final BO iteration, ≥15% averaged across all iterations"). This would be more defensible while still demonstrating BOFN's value proposition.

---

## 2. Is YS≥250 MPa AND EL≥5% the Right Threshold?

### Literature Benchmarks

| Alloy System | Condition | Yield Strength (MPa) | Elongation (%) | Contains Critical Minerals (Mg/Sc/REE/Be)? | Source Reference |
|---|---|---:|---:|---|---|
| AlSi10Mg | As-built, XY | ~261 | ~15.7 | Yes (contains Mg) | Arena 2024 (arena2024novelaluminumalloy pages 6-8) |
| AlSi10Mg | As-built, Z | ~220 | ~10.7 | Yes (contains Mg) | Arena 2024 (arena2024novelaluminumalloy pages 6-8) |
| Al-HS1 / Al-5Mn-0.8Cr-0.6Zr | As-printed | ~250 | Not explicitly specified | No (Mg/Sc/REE/Be-free in reported composition) | Arena 2024 (arena2024novelaluminumalloy pages 4-6) |
| Al-HS1 / Al-5Mn-0.8Cr-0.6Zr | Heat-treated, XY | ~356 | ~10.4 | No (Mg/Sc/REE/Be-free in reported composition) | Arena 2024 (arena2024novelaluminumalloy pages 6-8) |
| Al-HS1 / Al-5Mn-0.8Cr-0.6Zr | Heat-treated, Z | ~343 | ~4.8 | No (Mg/Sc/REE/Be-free in reported composition) | Arena 2024 (arena2024novelaluminumalloy pages 6-8) |
| Al-Zr-Er-Ni optimized | As-built | ~279 | ~19 | Yes (contains Er, a REE) | Ge 2025 (ge2025highstrengthadditivelymanufacturable pages 1-2) |
| Al-Zr-Er-Ni benchmark | As-built | Not numerically stated in excerpt; described as higher-strength benchmark | ~0.9 | Yes (contains Er, a REE) | Ge 2025 (ge2025highstrengthadditivelymanufacturable pages 1-2) |
| FLAIME KPI threshold | Pass criterion | ≥250 | ≥5 | Must be No (0 wt% Mg/Sc/REE/Be) | Proposal KPI definition |
| Al-HS1 / Al-5Mn-0.8Cr-0.6Zr | KPI assessment, as-printed | Pass on YS; EL unknown | Unknown | Pass mineral screen | Derived from Arena 2024 (arena2024novelaluminumalloy pages 4-6) |
| Al-HS1 / Al-5Mn-0.8Cr-0.6Zr | KPI assessment, heat-treated XY | Pass | Pass | Pass mineral screen | Derived from Arena 2024 (arena2024novelaluminumalloy pages 6-8) |
| Al-HS1 / Al-5Mn-0.8Cr-0.6Zr | KPI assessment, heat-treated Z | Pass | Fail | Pass mineral screen | Derived from Arena 2024 (arena2024novelaluminumalloy pages 6-8) |
| AlSi10Mg | KPI assessment, as-built XY | Pass | Pass | Fail mineral screen | Derived from Arena 2024 (arena2024novelaluminumalloy pages 6-8) |
| AlSi10Mg | KPI assessment, as-built Z | Fail | Pass | Fail mineral screen | Derived from Arena 2024 (arena2024novelaluminumalloy pages 6-8) |
| Al-Zr-Er-Ni optimized | KPI assessment, as-built | Pass | Pass | Fail mineral screen | Derived from Ge 2025 (ge2025highstrengthadditivelymanufacturable pages 1-2) |
| Al-Zr-Er-Ni benchmark | KPI assessment, as-built | Strength likely pass; excerpt insufficient for exact YS | Fail | Fail mineral screen | Derived from Ge 2025 (ge2025highstrengthadditivelymanufacturable pages 1-2) |


*Table: This table compares literature LPBF aluminum alloys against the proposed FLAIME screening threshold of YS≥250 MPa and EL≥5%, while separately flagging whether each alloy violates the mineral-avoidance screen. It is useful for showing that some literature alloys meet mechanics but fail the mineral screen, while Al-Mn-Cr-Zr variants appear closer to the intended FLAIME target space.*

**Al-Mn-Cr-Zr (Al-HS1, forAM®).** Arena et al. (2024) report the Al-5Mn-0.8Cr-0.6Zr alloy (Al-HS1) achieves ~250 MPa yield strength in the as-printed condition, rising to 343–356 MPa after heat treatment at 375°C (arena2024novelaluminumalloy pages 6-8, arena2024novelaluminumalloy pages 4-6). Elongation in the heat-treated condition is 10.4% (XY direction) but only 4.8% (Z direction). This means the flagship mineral-lean alloy in the literature *just barely* meets the 250 MPa YS threshold as-printed and fails the EL≥5% criterion in one build orientation after heat treatment. The threshold therefore sits precisely at the boundary of current state-of-the-art for this alloy family, which is appropriate for a "discovery" metric but leaves no margin for the as-printed condition.

**Al-Zr-Er-Ni.** Ge et al. (2025) report 279 MPa YS and 19% elongation in the as-built condition for their optimized Al-0.5Zr-0.4Er-0.6Ni alloy (ge2025highstrengthadditivelymanufacturable pages 1-2). This alloy clearly exceeds the FLAIME threshold on both metrics but contains erbium (a rare earth element), which would fail the mineral-avoidance screen. It demonstrates that the YS≥250 MPa / EL≥5% target is achievable for LPBF Al alloys with appropriate microstructural design, but the elimination of Er as a grain-refining/strengthening agent makes reaching this target substantially harder.

**AlSi10Mg benchmark.** LPBF AlSi10Mg shows wide property ranges depending on build orientation and post-processing: YS of 220–261 MPa, UTS of 267–473 MPa, and elongation of 3.5–15.7% across studies (wang2024areviewon pages 9-11, arena2024novelaluminumalloy pages 6-8). The FLAIME threshold of YS≥250 MPa / EL≥5% is broadly comparable to AlSi10Mg performance in favorable orientations, which is appropriate for a benchmark-matching metric. However, AlSi10Mg itself fails the mineral-avoidance screen due to Mg content.

**Al-Mn-Cr-Zr variants (Mehta et al./Hossain et al.).** Broader Al-Mn-Cr-Zr family studies report yield strengths in the range of 250–500 MPa and elongations of 5–25% depending on composition, Zr content, and heat treatment (hossain2026additivemanufacturingof pages 6-8). The wide range reflects the strong dependence on precipitation state and suggests that BOFN optimization within this family has considerable room to navigate the YS-EL trade-off.

### Should the Threshold Be Family-Specific?

**Yes—this is strongly recommended.** The Al-Zr binary family (without Mn/Cr) relies primarily on L1₂ Al₃Zr nanoprecipitates for strengthening. Without the solid-solution and precipitation-hardening contributions from Mn and Cr, the as-built YS of binary Al-Zr alloys may be substantially below 250 MPa, while elongation could be higher. In contrast, Al-Mn-Cr-Zr alloys achieve high strength through combined solid-solution and precipitation hardening (martucci2023developmentandcharacterisation pages 130-132, martucci2023developmentandcharacterisation pages 126-130) but may trade off elongation. For the Cu-Cr-Zr complement (~20% of effort), the relevant performance targets would involve conductivity and hardness rather than tensile properties analogous to Al alloys.

**Recommendation:** Define family-specific tiers: (i) Al-Mn-Cr-Zr: YS≥250 MPa AND EL≥5% (as proposed, appropriate); (ii) Al-Zr binary: YS≥200 MPa AND EL≥8% (lower strength, higher ductility expected); (iii) Cu-Cr-Zr: use a conductivity-hardness metric rather than tensile YS/EL. The overall "Discovery Yield" can still be reported as the aggregate fraction across families, but family-specific sub-metrics will be more credible to reviewers.

Additionally, consider specifying whether the threshold applies to the as-printed or heat-treated condition. The Al-HS1 data show that as-printed properties (~250 MPa) differ substantially from heat-treated properties (~350 MPa), and the FLAIME pipeline as described ends at tensile testing without specifying a heat-treatment step (arena2024novelaluminumalloy pages 4-6).

---

## 3. Is "0 wt% Mg/Sc/REE/Be" the Right Mineral-Avoidance Definition?

### The USGS Critical Minerals Problem

| Element | On USGS 2022 Critical List? | Role in FLAIME Alloys | Supply Risk Context | Implication for KPI Definition |
|---|---|---|---|---|
| Zr | Yes | Primary alloying element in Al-Zr and Al-Mn-Cr-Zr families | USGS 2022 list includes zirconium; U.S. production exists from heavy-mineral sands, indicating some domestic supply but continued criticality designation (hartmann2022draftcriticalminerals pages 13-15, hammarstrom2022…andpuerto pages 16-20, humphries2019criticalmineralsand pages 18-20) | KPI currently excludes only Mg/Sc/REE/Be, but Zr is also critical; reviewer may see a mismatch between “critical-mineral avoidance” and actual chemistry |
| Mn | Yes | Primary alloying element in Al-Mn-Cr-Zr (~5 wt%) | USGS 2022 list includes manganese; reports note no U.S. mine production and strong import dependence/high supply risk (hartmann2022draftcriticalminerals pages 13-15, staff2024usgsmineralreview pages 6-8, hammarstrom2022…andpuerto pages 16-20, humphries2019criticalmineralsand pages 18-20) | Major KPI gap: Mn is itself critical, so the current mineral-avoidance definition may overstate “mineral-lean” performance |
| Cr | Yes | Primary alloying element in Al-Mn-Cr-Zr (~0.8 wt%) | USGS 2022 list includes chromium; reports note no U.S. mine production and high import reliance/supply vulnerability (hartmann2022draftcriticalminerals pages 13-15, staff2024usgsmineralreview pages 6-8, hammarstrom2022…andpuerto pages 16-20, mudd2024uk2024criticality pages 45-51) | Important gap: Cr is critical yet remains a core design element, so the KPI should acknowledge reduction/substitution rather than absolute avoidance |
| Mg | Yes | Explicitly excluded by KPI (0 wt%) | USGS 2022 list includes magnesium; some U.S. production exists but DOE also flags Mg as near-critical/critical depending on time horizon (hartmann2022draftcriticalminerals pages 13-15, mudd2024uk2024criticality pages 45-51, humphries2019criticalmineralsand pages 18-20, bauer20232023criticalmaterials pages 16-18) | Correctly excluded under the current KPI and aligned with DOE concern around supply-constrained Mg |
| Sc | Yes | Explicitly excluded by KPI (0 wt%) | USGS 2022 list includes scandium; very limited production and no meaningful U.S. mine production in cited summaries, consistent with strong supply constraint (hartmann2022draftcriticalminerals pages 13-15, staff2024usgsmineralreview pages 6-8, humphries2019criticalmineralsand pages 18-20) | Correctly excluded; this is one of the clearest elements to justify in a “reduced dependence” framing |
| Be | Yes | Explicitly excluded by KPI (0 wt%) | USGS 2022 list includes beryllium; U.S. is a major producer, but supply is concentrated among few producers and substitution is limited; toxicity concerns add practical motivation for avoidance (hartmann2022draftcriticalminerals pages 13-15, staff2024usgsmineralreview pages 6-8, hammarstrom2022…andpuerto pages 16-20) | Correctly excluded; especially defensible for the Cu-Cr-Zr stretch goal framed as Be-Cu replacement |
| REEs (Er, etc.) | Yes | Explicitly excluded by KPI (0 wt%); relevant because Ge et al. alloy uses Er | USGS 2022 list includes rare earth elements individually; cited summaries note strong dependence on China and limited U.S. production history, especially for separated REEs (hartmann2022draftcriticalminerals pages 13-15, staff2024usgsmineralreview pages 6-8, humphries2019criticalmineralsand pages 18-20, bauer20232023criticalmaterials pages 16-18) | Correctly excluded; helps distinguish FLAIME from strong LPBF alloys that rely on Er/other REEs |


*Table: This table maps FLAIME-relevant alloying elements to the USGS 2022 critical minerals list and summarizes the supply-risk logic a DOE reviewer may apply. It is useful for showing that the current KPI correctly excludes Mg/Sc/REE/Be but does not fully capture the fact that Zr, Mn, and Cr are also critical minerals.*

This is the **most significant vulnerability** in the current KPI formulation. The USGS 2022 Final List of Critical Minerals contains 50 mineral commodities and explicitly includes not only Mg, Sc, Be, and REEs (which the KPI correctly excludes) but also **zirconium, manganese, and chromium**—the three primary alloying elements in FLAIME's target alloy families (hartmann2022draftcriticalminerals pages 13-15, hammarstrom2022…andpuerto pages 16-20). Manganese is particularly problematic: the U.S. has no domestic mine production and is 100% import-reliant (humphries2019criticalmineralsand pages 18-20). Chromium similarly has no U.S. mine production (hammarstrom2022…andpuerto pages 16-20). A DOE reviewer familiar with the USGS list would immediately recognize that an alloy containing 5 wt% Mn and 0.8 wt% Cr is not "mineral-lean" in the comprehensive sense, even if it avoids Mg, Sc, REEs, and Be.

### "Reduce Dependence" vs. "Mineral-Lean"

The DOE AMMTO framework for critical minerals reduction emphasizes three pillars: (1) diversifying supply, (2) developing substitutes, and (3) improving recycling and efficiency (hartmann2023strategicplandecrease pages 1-5, hartmann2023strategicplandecrease pages 54-56, hartmann2023strategicplandecrease pages 12-14, lograsso2024criticalmaterialsinstitute pages 6-9). "Reducing demand" is defined broadly as substitution of high-risk elements, advanced manufacturing-enabled material savings (~30% material efficiency gains from AM), and recovery/recycling (hartmann2023strategicplandecrease pages 48-51, hartmann2022draftcriticalminerals pages 54-57). The framing of "reduce dependence on supply-constrained critical minerals (Mg, Sc, REEs)" is a narrower and more defensible claim than "mineral-lean," because it acknowledges that all elements exist on a spectrum of supply risk and that the goal is *relative reduction* in the most constrained elements, not absolute elimination of all critical minerals.

### Recommendation: Reframe the Avoidance Definition

Instead of "0 wt% Mg/Sc/REE/Be" (a binary pass/fail on a subset of critical minerals), consider a **Critical Mineral Intensity (CMI) score** that weights each element by its supply-risk factor. This would:

1. **Acknowledge that Zr, Mn, and Cr are critical** but argue that they have lower supply risk than Sc, REEs, and Be due to (a) larger global reserves, (b) some U.S. production capacity (Zr), and (c) recycling potential;
2. **Quantify improvement** over benchmark alloys (e.g., "50% reduction in weighted critical-mineral content vs. Al-Sc or Al-Mg-Sc-Zr baseline alloys");
3. **Align with DOE language** about "reducing demand" and "developing substitutes" rather than claiming absolute avoidance (hartmann2023strategicplandecrease pages 12-14, lograsso2024criticalmaterialsinstitute pages 6-9).

At minimum, the KPI definition should explicitly state: "Avoidance of the highest-supply-risk elements (Sc, Be, Mg, REEs) while utilizing lower-risk critical minerals (Mn, Cr, Zr) at concentrations ≤X wt% total." This preempts the obvious reviewer objection and aligns with the AMMTO Topic 3B framing of "reducing demand" rather than "eliminating use."

---

## 4. Recommendations for Strengthening the KPI

### 4.1 Decompose into Leading and Lagging Indicators

The current KPI is a single lagging metric (fraction of tested compositions meeting threshold). For a 9-month Phase I where the total number of tested compositions may be small (15–30), this creates high variance. Consider adding leading indicators:

- **BOFN Convergence Rate:** Number of BO iterations to achieve a specified improvement in predicted Pareto hypervolume. This leverages the BOFN framework's ability to model intermediate nodes and can be assessed computationally before physical experiments (astudillo2021bayesianoptimizationof pages 1-2, zhang2024practicalandtheoretical pages 64-68).
- **Printability Yield:** Fraction of BOFN-proposed compositions that achieve ≥99% relative density and crack-free microstructure in LPBF, separate from the tensile-property threshold.
- **Property Improvement per Iteration:** Demonstrate that each successive BOFN batch shows monotonic improvement in the best-achieved YS×EL product.

### 4.2 Adopt a Multi-Tier Discovery Classification

Instead of a single pass/fail, classify outcomes as:

| Tier | Criteria | Phase I Target |
|------|----------|---------------|
| Tier 1 (Full Pass) | YS≥250 MPa AND EL≥5% AND mineral-avoidance | ≥20% |
| Tier 2 (Partial Pass) | Meets YS OR EL threshold AND mineral-avoidance | ≥40% |
| Tier 3 (Printable) | Crack-free, ≥99% density, any properties | ≥70% |

This gives credit for partial successes that inform subsequent BOFN iterations and better reflects the reality that most early-campaign compositions will be informative rather than optimal.

### 4.3 Replace "Mineral-Lean" with "Supply-Risk-Reduced"

As discussed in Section 3, reframe the mineral-avoidance criterion quantitatively. A suggested formulation: **"Supply-Risk Reduction Score ≥ 80%"** defined as: SRR = 1 − (Σᵢ wᵢ × SRᵢ) / (Σᵢ wᵢ_baseline × SRᵢ), where wᵢ is the weight fraction of element i and SRᵢ is its USGS supply-risk score. This metric captures that a 5% Mn alloy is better than a 0.5% Sc alloy even though both elements are critical, and provides a continuous rather than binary evaluation.

### 4.4 Specify Condition and Build Orientation

The current KPI does not specify whether properties are evaluated as-built or post-heat-treatment, nor which build orientation is assessed. Given that the Al-HS1 alloy shows 10.4% elongation in XY but only 4.8% in Z after heat treatment (arena2024novelaluminumalloy pages 6-8), this distinction is significant. **Recommendation:** Define the KPI for both as-printed and optimally heat-treated conditions in the most conservative build orientation (typically Z), or require that the alloy meets threshold in at least one tested orientation with both conditions reported.

### 4.5 Benchmark BOFN Against Random and Expert Baselines

To demonstrate the value of the BOFN approach specifically, include a comparison metric: **"BOFN Acceleration Factor"** = (Discovery Yield with BOFN) / (Estimated Discovery Yield with random sampling from same design space). This directly quantifies the AI-enabled value proposition, which is the core of Topic 3B. The BIRDSHOT campaign demonstrated that BO achieved 10/24 (42%) dominance in the second iteration from a space of millions of candidates (paramore2025twoshotoptimizationof pages 16-18), and Abolhasani's SDLs report 60-fold reductions in required experiments (abolhasani2023theriseof pages 3-4). Reporting an analogous metric would strengthen the proposal's alignment with DOE's AI-enabled discovery theme.

### Summary Assessment

The "Mineral-Lean Discovery Yield" KPI is a reasonable first attempt but contains several vulnerabilities that a DOE reviewer would likely flag:

1. **The ≥30% target is ambitious** given the slow LPBF pipeline and compound constraints. A ≥20% target with ≥30% stretch goal would be more defensible.
2. **The YS≥250 MPa / EL≥5% threshold is well-calibrated** to the AlSi10Mg benchmark and near the demonstrated performance of Al-Mn-Cr-Zr alloys, but should be family-specific and condition-specific.
3. **The "0 wt% Mg/Sc/REE/Be" definition has a critical gap**: Zr, Mn, and Cr are all on the USGS 2022 critical minerals list. Reframing as "supply-risk reduction" with a quantitative score is essential.
4. **Decomposing the KPI** into leading indicators, multi-tier outcomes, and BOFN acceleration metrics would significantly strengthen the proposal for DOE reviewers focused on both AI-enabled discovery and critical mineral impact.

References

1. (paramore2025twoshotoptimizationof pages 16-18): James D. Paramore, Trevor Hastings, Brady G. Butler, Michael T. Hurst, Daniel O. Lewis, Eli Norris, Benjamin Barkai, Joshua Cline, Braden Miller, Jose Cortes, Ibrahim Karaman, George M. Pharr, and Raymundo Arróyave. Two-shot optimization of compositionally complex refractory alloys. Acta Materialia, pages 120820, Feb 2025. URL: https://doi.org/10.1016/j.actamat.2025.120820, doi:10.1016/j.actamat.2025.120820. This article has 9 citations and is from a highest quality peer-reviewed journal.

2. (arroyave2024ultimatebirdshot.final pages 9-11): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

3. (paramore2025twoshotoptimizationof pages 1-3): James D. Paramore, Trevor Hastings, Brady G. Butler, Michael T. Hurst, Daniel O. Lewis, Eli Norris, Benjamin Barkai, Joshua Cline, Braden Miller, Jose Cortes, Ibrahim Karaman, George M. Pharr, and Raymundo Arróyave. Two-shot optimization of compositionally complex refractory alloys. Acta Materialia, pages 120820, Feb 2025. URL: https://doi.org/10.1016/j.actamat.2025.120820, doi:10.1016/j.actamat.2025.120820. This article has 9 citations and is from a highest quality peer-reviewed journal.

4. (arroyave2024ultimatebirdshot.final pages 1-5): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

5. (szymanski2023anautonomouslaboratory pages 2-3): Nathan J. Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E. Kumar, Tanjin He, David Milsted, Matthew J. McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, Haegyeom Kim, Anubhav Jain, Christopher J. Bartel, Kristin Persson, Yan Zeng, and Gerbrand Ceder. An autonomous laboratory for the accelerated synthesis of inorganic materials. Nature, 624:86-91, Nov 2023. URL: https://doi.org/10.1038/s41586-023-06734-w, doi:10.1038/s41586-023-06734-w. This article has 1064 citations and is from a highest quality peer-reviewed journal.

6. (szymanski2023anautonomouslaboratory pages 4-5): Nathan J. Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E. Kumar, Tanjin He, David Milsted, Matthew J. McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, Haegyeom Kim, Anubhav Jain, Christopher J. Bartel, Kristin Persson, Yan Zeng, and Gerbrand Ceder. An autonomous laboratory for the accelerated synthesis of inorganic materials. Nature, 624:86-91, Nov 2023. URL: https://doi.org/10.1038/s41586-023-06734-w, doi:10.1038/s41586-023-06734-w. This article has 1064 citations and is from a highest quality peer-reviewed journal.

7. (szymanski2023anautonomouslaboratory pages 3-4): Nathan J. Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E. Kumar, Tanjin He, David Milsted, Matthew J. McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, Haegyeom Kim, Anubhav Jain, Christopher J. Bartel, Kristin Persson, Yan Zeng, and Gerbrand Ceder. An autonomous laboratory for the accelerated synthesis of inorganic materials. Nature, 624:86-91, Nov 2023. URL: https://doi.org/10.1038/s41586-023-06734-w, doi:10.1038/s41586-023-06734-w. This article has 1064 citations and is from a highest quality peer-reviewed journal.

8. (szymanski2023anautonomouslaboratory pages 1-2): Nathan J. Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E. Kumar, Tanjin He, David Milsted, Matthew J. McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, Haegyeom Kim, Anubhav Jain, Christopher J. Bartel, Kristin Persson, Yan Zeng, and Gerbrand Ceder. An autonomous laboratory for the accelerated synthesis of inorganic materials. Nature, 624:86-91, Nov 2023. URL: https://doi.org/10.1038/s41586-023-06734-w, doi:10.1038/s41586-023-06734-w. This article has 1064 citations and is from a highest quality peer-reviewed journal.

9. (abolhasani2023theriseof pages 3-4): Milad Abolhasani and Eugenia Kumacheva. The rise of self-driving labs in chemical and materials sciences. Nature Synthesis, 2:483-492, Jan 2023. URL: https://doi.org/10.1038/s44160-022-00231-0, doi:10.1038/s44160-022-00231-0. This article has 650 citations and is from a peer-reviewed journal.

10. (volk2024performancemetricsto pages 1-2): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 80 citations and is from a highest quality peer-reviewed journal.

11. (astudillo2021bayesianoptimizationof pages 1-2): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 74 citations.

12. (buathong2023bayesianoptimizationof pages 1-2): Poompol Buathong, Jiayue Wan, Raul Astudillo, Samuel Daulton, Maximilian Balandat, and Peter I. Frazier. Bayesian optimization of function networks with partial evaluations. ArXiv, Nov 2023. URL: https://doi.org/10.48550/arxiv.2311.02146, doi:10.48550/arxiv.2311.02146. This article has 11 citations.

13. (zhang2024practicalandtheoretical pages 64-68): D Zhang. Practical and theoretical advances in constrained bayesian optimization and bayesian optimization for machine learning …. Unknown journal, 2024.

14. (arroyave2024ultimatebirdshot.final pages 5-7): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

15. (arena2024novelaluminumalloy pages 6-8): Maurizio Arena, Bharat Mehta, Tommaso Tirelli, Paolo Ambrogiani, Martina Castaldo, Sven Bengtsson, and Lars Nyborg. Novel aluminum alloy tailored for additive manufacturing: structural characterization and qualification perspectives. Applied Sciences, 14:4647, May 2024. URL: https://doi.org/10.3390/app14114647, doi:10.3390/app14114647. This article has 0 citations.

16. (arena2024novelaluminumalloy pages 4-6): Maurizio Arena, Bharat Mehta, Tommaso Tirelli, Paolo Ambrogiani, Martina Castaldo, Sven Bengtsson, and Lars Nyborg. Novel aluminum alloy tailored for additive manufacturing: structural characterization and qualification perspectives. Applied Sciences, 14:4647, May 2024. URL: https://doi.org/10.3390/app14114647, doi:10.3390/app14114647. This article has 0 citations.

17. (ge2025highstrengthadditivelymanufacturable pages 1-2): Zhaoxuan Ge, Shaolou Wei, Zehua Liu, Tomasz Choma, Lukasz Zrodowski, Marc De Graef, A. John Hart, and S. Mohadeseh Taheri-Mousavi. High-strength additively manufacturable al-zr-er-ni alloys with high as-built ductility and thermal stability. May 2025. URL: https://doi.org/10.21203/rs.3.rs-6558867/v1, doi:10.21203/rs.3.rs-6558867/v1.

18. (wang2024areviewon pages 9-11): Xin Wang, Dongyun Zhang, Ang Li, Denghao Yi, and Tianci Li. A review on traditional processes and laser powder bed fusion of aluminum alloy microstructures, mechanical properties, costs, and applications. Materials, 17:2553, May 2024. URL: https://doi.org/10.3390/ma17112553, doi:10.3390/ma17112553. This article has 39 citations.

19. (hossain2026additivemanufacturingof pages 6-8): Md Arman Hossain, Shipon Chandra Barman, and S M Tarikul Islam. Additive manufacturing of lightweight, fire-resistant alloys for automotive and aerospace applications. Journal of Mechanical, Civil and Industrial Engineering, 7:06-16, Mar 2026. URL: https://doi.org/10.32996/jmcie.2026.7.3.2, doi:10.32996/jmcie.2026.7.3.2. This article has 0 citations.

20. (martucci2023developmentandcharacterisation pages 130-132): A Martucci. Development and characterisation of al-based alloys processed by pbf-lb/m. Unknown journal, 2023.

21. (martucci2023developmentandcharacterisation pages 126-130): A Martucci. Development and characterisation of al-based alloys processed by pbf-lb/m. Unknown journal, 2023.

22. (hartmann2022draftcriticalminerals pages 13-15): Thomas Hartmann, Stuart Maloy, and Isabella Johanna van Rooyen. Draft critical minerals evaluation report: advanced materials and manufacturing technology. ArXiv, Sep 2022. URL: https://doi.org/10.2172/2478110, doi:10.2172/2478110. This article has 2 citations.

23. (hammarstrom2022…andpuerto pages 16-20): JM Hammarstrom, CL Dicken, and LG Woodruff. … and puerto rico—antimony, barite, beryllium, chromium, fluorspar, hafnium, helium, magnesium, manganese, potash, uranium, vanadium, and zirconium. Unknown journal, 2022.

24. (humphries2019criticalmineralsand pages 18-20): M Humphries. Critical minerals and us public policy. Unknown journal, 2019.

25. (staff2024usgsmineralreview pages 6-8): U Staff. Usgs mineral review. Unknown journal, 2024.

26. (mudd2024uk2024criticality pages 45-51): G Mudd, P Josso, R Shaw, A Luce, N Singh, and S Horn. Uk 2024 criticality assessment. Unknown journal, 2024.

27. (bauer20232023criticalmaterials pages 16-18): Diana Bauer, Helena Khazdozian, Jeremy Mehta, Ruby Nguyen, Michael Severson, Bjorn Vaagensmith, Lionel Toba, Bo Zhang, Tasmin Hossain, Adam Sibal, Braeton Smith, Matthew Riddle, Diane Graziano, Tony Mathew, Patrick Cuscaden, Qiang Dai, Chukwunwike Iloeje, Lesley Edgemon, Caitlyn Sarna, and Julian Quaresima. 2023 critical materials strategy. ArXiv, Jul 2023. URL: https://doi.org/10.2172/1998242, doi:10.2172/1998242. This article has 18 citations.

28. (hartmann2023strategicplandecrease pages 1-5): Thomas Hartmann, Praveen Thallapally, and Isabella Johanna van Rooyen. Strategic plan: decrease critical minerals waste through enabling advanced manufacturing techniques. ArXiv, Jul 2023. URL: https://doi.org/10.2172/2481581, doi:10.2172/2481581. This article has 1 citations.

29. (hartmann2023strategicplandecrease pages 54-56): Thomas Hartmann, Praveen Thallapally, and Isabella Johanna van Rooyen. Strategic plan: decrease critical minerals waste through enabling advanced manufacturing techniques. ArXiv, Jul 2023. URL: https://doi.org/10.2172/2481581, doi:10.2172/2481581. This article has 1 citations.

30. (hartmann2023strategicplandecrease pages 12-14): Thomas Hartmann, Praveen Thallapally, and Isabella Johanna van Rooyen. Strategic plan: decrease critical minerals waste through enabling advanced manufacturing techniques. ArXiv, Jul 2023. URL: https://doi.org/10.2172/2481581, doi:10.2172/2481581. This article has 1 citations.

31. (lograsso2024criticalmaterialsinstitute pages 6-9): Thomas Lograsso, Bruce Moyer, and Melinda Thach. Critical materials institute (cmi) year 10 cumulative report. ArXiv, Apr 2024. URL: https://doi.org/10.2172/2338076, doi:10.2172/2338076. This article has 1 citations.

32. (hartmann2023strategicplandecrease pages 48-51): Thomas Hartmann, Praveen Thallapally, and Isabella Johanna van Rooyen. Strategic plan: decrease critical minerals waste through enabling advanced manufacturing techniques. ArXiv, Jul 2023. URL: https://doi.org/10.2172/2481581, doi:10.2172/2481581. This article has 1 citations.

33. (hartmann2022draftcriticalminerals pages 54-57): Thomas Hartmann, Stuart Maloy, and Isabella Johanna van Rooyen. Draft critical minerals evaluation report: advanced materials and manufacturing technology. ArXiv, Sep 2022. URL: https://doi.org/10.2172/2478110, doi:10.2172/2478110. This article has 2 citations.