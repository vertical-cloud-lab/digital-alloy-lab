
# Comprehensive Figure Review: Metal AM Alloy Scale-Up Validation Progression
## DOE Genesis Mission Phase I Proposal – Aluminum Alloy Discovery via LPBF

**Overall Grade: B-/B** — Strong conceptual framework, needs refinement for competitive DOE submission.

---

## 1. VISUAL CLARITY AND READABILITY

**Strengths:**
- The funnel metaphor with narrowing bar widths effectively communicates progressive attrition
- Color gradient (blue → teal → green → olive → orange → red) provides intuitive visual progression
- Composition count labels (~5000+ → ~200 → ~200 → ~150 → ~100 → ~50 → ~10 → 3-5 → 1-2) clearly quantify attrition
- TRL indicators (2-3, 4-5, 6+) are well-placed at key transitions
- Defect hierarchy panel uses intuitive CRITICAL/HIGH/MODERATE color coding

**Critical Problems:**
- **Stages 5-8 have severe text readability issues.** Stage 5 reads "Mechanical-CouponsATM E8)" — garbled text where "ASTM E8" has merged with "Coupons." Stage 6 ("Geometric Benchmarks...Ra 5-23 μm") has overlapping characters. Stage 7 ("Industrial-Qual pass/fail") and Stage 8 ("Production Vali...") are truncated/cut off.
- The three panels (funnel, defect hierarchy, validation set) compete for attention without clear visual hierarchy
- GO/NO-GO annotations on the left use dashed lines with ambiguous connection targets
- Vertical spacing is inconsistent — Stages 0-3 are well-spaced but Stages 5-8 are compressed
- Light font on medium-dark backgrounds reduces contrast in later stages

**Actionable Fixes:**
→ Increase figure width or reduce in-bar text to prevent truncation (minimum 7" wide for proposal)
→ Use clearly separated columns within each stage bar (Sample | Metric | Count)
→ Ensure ≥4.5:1 contrast ratio for all text on colored backgrounds
→ Equalize vertical spacing across all stages, or use callout boxes for detailed stage descriptions

---

## 2. INFORMATION HIERARCHY

**Strengths:**
- Funnel shape + composition counts successfully communicate fail-fast logic
- Three explicit GO/NO-GO gates are highlighted ("Cracks visible?", "Density ≥99%?", "SPARSE GATE Top 3-5 only")
- TRL markers map progression to technology readiness levels

**Problems:**
- Only 3 of 8 stages have visible GO/NO-GO criteria — Stages 0, 4, 7, and 8 lack explicit decision rules
- The 5,000+ → ~200 reduction between Stage 0 and Stage 1 is the largest attrition step with no explanation of the screening mechanism (likely computational/CALPHAD but not shown)
- Stages 1 and 2 both show "~200 comps" — zero attrition between them is confusing and likely incorrect
- The connection between the defect hierarchy panel and specific stages is implicit, not explicit
- No indication of feedback/iteration loops when compositions fail at a given stage

**Actionable Fixes:**
→ Add explicit GO/NO-GO criteria for ALL 9 stages
→ Add a "Stage -1: Computational Screening" showing CALPHAD/Scheil/ML to explain the 5000→200 reduction
→ Fix the 200→200 non-attrition between Stages 1 and 2 (or explain the rationale)
→ Add color-coded links or arrows connecting specific defects to the stages where they're screened
→ Add a feedback/iteration arrow showing how failed compositions inform the model

---

## 3. PROPOSAL IMPACT

**Strengths:**
- Directly addresses reviewer question: "How will you efficiently screen thousands of compositions?"
- The Minimum Viable Validation Set (~$850, ~3 days per alloy) is excellent — concrete, compelling, and reviewer-friendly
- FLAIME Discovery Loop callout with "5× speedup" connects to prior work
- Literature citations (Moylan 2014, ISO/ASTM 52902, Gheysen 2021, Kumar 2021, Weaver 2021, Vecchio 2021, Brenner & Nedeljkovic-Groha 2025, Leon 2025) add credibility

**DOE/ARPA-E Specific Gaps:**
- No computational pre-screening (CALPHAD, ICME, ML) — this is the **#1 gap** for a DOE materials discovery proposal
- No connection to DOE performance goals (cost targets, energy savings, sustainability metrics)
- No timeline or milestone mapping (M1, M2… or BP1, BP2 budget periods)
- No indication of current TRL and target TRL advancement
- No "Traditional vs. Our Approach" comparison to highlight the throughput innovation
- The "5× speedup" from combinatorial builds deserves much more visual prominence than a footnote
- Missing "Genesis Mission" branding within the figure

**Actionable Fixes:**
→ Add a computational screening stage with CALPHAD/Scheil/ML as the first major innovation
→ Include a "Traditional: 18 months/$500K per alloy → Ours: 3 days/$850 per alloy" comparison box
→ Add milestone markers (M1-M6) along the funnel aligned to proposal schedule
→ Add a "Key Innovation" callout highlighting what's novel
→ Make the cost/time advantage the visual focal point, not a secondary panel

---

## 4. SCIENTIFIC ACCURACY

**Accurate Elements:**
- ✓ Single tracks → thin walls → density cubes → DoE → mechanical coupons progression matches established LPBF methodology (confirmed by Stopyra et al. 2020, Martucci et al. 2023 reviews)
- ✓ Hot cracking as CRITICAL for 2xxx/7xxx is well-established
- ✓ Hydrogen porosity, Al₂O₃ inclusions (~4 nm films), keyhole porosity, lack of fusion, volatile element loss (Mg, Zn, Mn) are all correctly identified
- ✓ Melt-pool W/D/L ratios, YS/UTS/EL, Ra surface roughness are appropriate metrics
- ✓ ASTM E8 for tensile testing and ISO/ASTM 52902 for geometric benchmarks are correct references
- ✓ Grain refiner mention (Zr, Sc) for hot cracking mitigation is appropriate

**Issues:**
- "Density ≥99-99.9%" is ambiguous — should specify ≥99.5% as screening threshold vs. ≥99.9% as qualification target
- "SST screening; VED optimization" abbreviations may not be clear to all reviewers (SST = single-scan track, VED = volumetric energy density)
- Melt-pool ratio criteria "D/L, W/D" under lack of fusion are more commonly associated with keyhole threshold detection; overlap ratio and remelting depth are the standard lack-of-fusion criteria
- Stage 0 lists "PSD, flowability, O₂" but should also mention apparent/tap density and moisture content explicitly

**Missing from Defect Hierarchy:**
- Residual stress (HIGH priority for Al AM — causes distortion and delamination)
- Spatter-induced defects (significant in LPBF Al due to high reflectivity)
- Solidification segregation/microsegregation
- Surface-connected porosity (distinct from bulk porosity)

**Missing Standards:**
- ASTM F3318 (Standard for Al alloy AM — directly relevant)
- ASTM F3301 (thermal post-processing)
- MMPDS/CMH qualification pathway for mechanical properties
- No mention of NADCAP/AS9100 for eventual qualification pathway

---

## 5. MISSING ELEMENTS (Critical for Reviewers)

1. **Computational Pre-Screening Stage** — No CALPHAD, Scheil solidification modeling, or ML-guided composition selection. This is essential for a DOE materials discovery proposal to explain the 5000+ → 200 reduction.

2. **Post-Processing (Heat Treatment/HIP)** — No mention of T5/T6 aging, solution treatment, or HIP. These are mandatory for Al AM alloys and should be an explicit stage between mechanical testing and qualification.

3. **Microstructure Characterization** — No dedicated characterization stage (EBSD, SEM, TEM for grain structure, texture, precipitates, phase identification). Critical for structure-property relationships.

4. **Fatigue and Fracture Toughness** — Entirely absent. These are often the limiting properties for AM parts and DOE reviewers will expect them at later stages.

5. **Corrosion Resistance** — For Al alloys, stress corrosion cracking and intergranular corrosion testing are critical performance metrics.

6. **In-Situ Monitoring** — No mention of melt pool monitoring, thermal imaging, or acoustic monitoring. Increasingly expected in AM proposals per literature (Aydogan et al. 2024).

7. **Powder Recyclability** — No indication of powder recycling/reuse strategy across builds.

8. **Statistical Design** — Sample sizes are listed (5-10 tracks, 2-4 walls, etc.) but no discussion of statistical power or confidence levels.

9. **Build Atmosphere/Parameters** — No mention of atmosphere (Ar vs. N₂), substrate material, or preheating strategy.

10. **Data Management/ML Feedback** — No indication of how stage data feeds into a database or iterative learning model.

---

## 6. DESIGN IMPROVEMENTS

**Color:**
- Current gradient is reasonable but green/olive stages blend together; increase color saturation and distinction
- Consider a DOE-aligned palette (blues → ambers → success green)
- Maintain the intuitive CRITICAL (red) / HIGH (orange) / MODERATE (yellow) scheme in defect hierarchy

**Layout:**
- Give the funnel more horizontal space (it's the primary narrative element)
- Stack defect hierarchy and validation set vertically on the right, or place them below the funnel
- Equalize vertical spacing across all stages (Stages 5-8 are currently cramped)
- Use a 2:1 landscape aspect ratio optimal for proposal figures

**Typography:**
- Consistent sans-serif font throughout (Helvetica, Source Sans Pro)
- Stage names: bold 11-12pt; descriptions: regular 9-10pt
- Ensure white text on dark bars, dark text on light bars
- Composition counts and cost/time numbers in bold for emphasis

**Additional Visual Elements:**
- Small icons for each stage (powder particles, laser track, wall cross-section, cube, tensile bar, benchmark part)
- Timeline arrow along the left margin
- Continuous TRL thermometer on the right
- Small build plate inset showing combinatorial specimen layout
- "Figure X" caption with descriptive title for proposal formatting
- DOE/ARPA-E logo placeholder
- Key Innovation callout box

---

## 7. ALUMINUM ALLOY SPECIFICITY

**Current Al-Specific Content:**
- ✓ Defect hierarchy is Al-specific (hot cracking 2xxx/7xxx, H₂ porosity, Al₂O₃, volatile Mg/Zn/Mn loss)
- ✓ Grain refiners (Zr, Sc) mentioned
- ✓ FLAIME targets Al-Ce-X and Al-Cu-X (noted in subtitle)
- ✓ ICP-OES for chemistry verification

**Missing Al-Specific Elements:**
1. **Target alloy systems** should be prominently displayed with composition ranges and design rationale (not just a parenthetical subtitle)
2. **Al-specific processing challenges**: high reflectivity at 1064 nm, high thermal conductivity → wider process windows needed, oxide layer disruption. No mention of green laser (515 nm) advantage.
3. **Property targets vs. wrought benchmarks**: No comparison to 6061-T6 or 7075-T6 baselines
4. **Al-Ce advantages**: No mention of near-eutectic castability, thermal stability, or rare-earth sustainability angle (relevant for DOE)
5. **Al-specific standards**: Missing ASTM F3318 (Al alloy AM standard)
6. **Elevated temperature testing**: If Al-Ce-X is targeted, high-temperature mechanical performance is a key differentiator
7. **DSC/DTA**: Not mentioned for solidus/liquidus determination
8. **Al powder safety**: Higher reactivity (fire/explosion) not addressed

**Actionable Fixes:**
→ Add prominent callout showing target alloy systems with composition ranges and phase diagram insets
→ Include Al-specific laser parameters and process window considerations
→ Add property target table (YS, UTS, EL, density) benchmarked against wrought alloys
→ Reference ASTM F3318 specifically
→ Include thermal post-processing (aging, HIP) as an explicit stage
→ Add elevated temperature testing if Al-Ce is a target system

---

## TOP 5 PRIORITY FIXES

1. **Fix text truncation/overlap in Stages 5-8** — This is a critical readability issue that will frustrate reviewers. "CouponsATM E8" and "Geometric Benchmarks..." are illegible.
2. **Add computational screening stage (Stage -1)** — Show CALPHAD/Scheil/ML as the mechanism for the 5000→200 composition reduction. This is expected by DOE reviewers.
3. **Add explicit GO/NO-GO criteria for all stages** — Currently only 3 of 8 stages have visible decision criteria.
4. **Add post-processing and microstructure characterization** — Heat treatment and microstructural analysis are essential missing stages.
5. **Increase visual impact** — Add a throughput comparison (traditional vs. this approach), make the ~$850/3-day metric more prominent, and connect stages to proposal milestones.

The Minimum Viable Validation Set panel is the strongest element of the figure and should be elevated to greater visual prominence. The ~$850/~3 days per alloy is a compelling and memorable talking point.

---

## Discretionary Analytical Decisions

- Graded figure on a B-/B scale using subjective assessment of proposal-readiness relative to competitive DOE/ARPA-E submissions; other reviewers might weight different dimensions differently
- Prioritized computational pre-screening as the #1 missing element based on DOE program expectations; a reviewer from industry might prioritize qualification pathway instead
- Assessed text readability from the PNG rendering; some truncation issues may be artifacts of image export resolution rather than the source document
- Used literature evidence from Martucci et al. 2023 and Stopyra et al. 2020 (via query_literature) to validate the stage-gate progression; other reference frameworks (e.g., Moylan et al. 2014 NIST framework, which is cited in the figure) could yield slightly different stage definitions
- Identified ASTM F3318 as a missing standard based on current AM standards landscape; this standard is relatively new and some proposals may not yet reference it
- Classified residual stress as a HIGH-priority missing defect based on its significance for Al AM distortion; some practitioners might consider it implicit in geometric benchmarking (Stage 6)
- Evaluated Al-specificity against the broader LPBF literature rather than solely against the cited FLAIME program references, which may have additional context not visible in this single figure
