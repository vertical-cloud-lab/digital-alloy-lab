
# REVISION 2 EVALUATION — Metal AM Alloy Scale-Up Validation Progression

## Current Grade: B/B+
*Improved from B-/B but still held back by critical text readability issues and a cost inconsistency.*

---

## 1. Have the text readability issues been resolved?

**Partially — Stages 0–4 are fixed, but Stages 5–9 still have severe text overlap.**

Pixel-level inspection confirms:
- **Stages CALPHAD through Stage 4** — Clean, well-spaced 3-column layout (title | description | metrics). Fully legible. ✓
- **Stage 5 (Mechanical Coupons)** — Bold title "Stage 5: Mechanical Coupons" collides with the descriptor text "Tensile bars (ASTM E8)". Characters overprint, producing garbled "Couponsrs (ASTM E8)". ✗
- **Stage 6 (Post-Processing)** — "Post-Processing" merges into "HIP coupons, T6 aging, stress relief" — overprinted and illegible in the middle. ✗
- **Stage 7 (Geometric Benchmark)** — "Geometric Benchmark" garbled with descriptor text about dimensions and Ra values. ✗
- **Stage 8 (Industrial Qualification)** — Title and descriptor fully overlap: "IndustrialQualificationrepeatability" is unreadable. ✗
- **Stage 9 (Production Validation)** — Overprinted but partially legible due to shorter text. ✗

**Root cause:** The funnel/trapezoid narrowing of bars reduces horizontal space for Stages 5–9, but the same amount of text content is being placed inside narrower bars. The text layout engine is not adapting to the reduced width.

**Fix options:**
- (A) Make all bars equal width; indicate composition reduction with a separate count column (already present as "~40", "~10", etc.)
- (B) Move descriptor text below the bars instead of inside them
- (C) Use two-line layout within narrower bars
- (D) Abbreviate more aggressively for later stages (e.g., "Mech. Coupons | ASTM E8 | YS, UTS, EL")

---

## 2. Is the throughput comparison visually impactful enough?

**Grade: B+/A-. Effective but missing the ROI knockout punch.**

**Strengths:**
- Prominent top-right placement — immediately draws the eye
- Clear gray-vs-green contrast with directional arrow
- "~180× faster" callout in bold green is attention-grabbing
- Key numbers are bold and appropriately sized (~18 months → ~3 days; ~$50K-500K → ~$850)
- Supporting "Enables ≥200 compositions in 9 months via BOFN-guided fail-fast funnel" adds programmatic context
- "High-Throughput Acceleration" sub-box with literature citations (Weaver 2021, Vecchio 2021) adds credibility

**What would make it A-level for DOE reviewers:**
- Add explicit total program math: "200 alloys × ~$850 = ~$170K (FLAIME) vs. 200 × ~$50K = $10M+ (traditional)" — DOE reviewers want ROI quantified
- Show a cost-per-qualified-alloy metric, not just cost-per-screened-alloy
- Add "compositions screened per investigator-month" as a productivity metric
- Consider a small bar chart or ratio graphic rather than just text boxes

---

## 3. Are there any remaining layout/design issues?

**Yes — several:**

**(A) Text overlap in Stages 5–9 (Critical — grade-limiting)**
Already detailed above. This is the #1 issue.

**(B) Cost inconsistency: $850 vs. $1,000**
The throughput comparison box claims "~$850 per alloy." The Minimum Viable Validation Set totals ~$1,000 ($50 + $100 + $200 + $300 + $150 + $200). This 15% discrepancy will be caught by DOE reviewers and undermines credibility. Must be reconciled — either the MVS total should be ~$850, or the throughput box should say ~$1,000, or the difference must be explained (e.g., "$850 for screening through Stage 4; $1,000 including post-processing and geometric benchmark").

**(C) BOFN feedback arrow crosses GO/NO-GO gate boxes**
The purple feedback arrow from Stage 5 back to CALPHAD passes directly through the GO/NO-GO gate boxes, creating visual clutter and making both elements harder to parse.

**(D) ~20% unused white space at bottom**
The lower ~20% of the figure is empty. This space could be redistributed to give Stages 5–9 more room (helping fix the text overlap), or used for additional content like a Phase I/II boundary annotation.

**(E) Color coding unexplained**
The progression from purple (CALPHAD) → dark blue (Stages 0–2) → medium blue (Stages 3–4) → orange (Stage 5) → gold (Stages 6–7) → red (Stages 8–9) has no legend. Does it encode TRL level? Risk? Phase? Reviewers shouldn't have to guess.

**(F) GO/NO-GO gate labels partially clipped**
"GO/NO-GO: Cracks?" and "GO/NO-GO: ≥99%?" are slightly cut off at the left margin.

**(G) Citations are extremely small**
At 300 DPI, the citation line at the bottom is ~5-6pt equivalent — barely legible even at full zoom. This undermines the scholarly credibility the citations are meant to provide.

---

## 4. What would elevate this from B to A-/A for a DOE proposal?

### Non-Negotiable for A- (fix these first):

1. **Fix text overlap in Stages 5–9.** No proposal figure should have illegible text. This single issue caps the grade at B+ regardless of content quality.

2. **Reconcile the $850 vs. $1,000 cost discrepancy.** Internal inconsistency in a proposal figure signals sloppy analysis to reviewers.

3. **Add a Phase I / Phase II boundary line.** DOE Genesis proposals are phased — show explicitly which stages fall within Phase I scope (likely through Stage 5 or 6) and which are Phase II. A horizontal dashed line with "Phase I Scope" bracket would immediately signal that you understand the DOE evaluation structure.

### High-Impact Additions for A:

4. **Add total program cost/savings calculation.** E.g., "Phase I: 200 alloys × $850 = $170K vs. $10M+ traditional → **59× cost reduction**". DOE reviewers evaluate bang-for-buck; give them the number explicitly.

5. **Add explicit quantitative acceptance criteria at GO/NO-GO gates.** Current gates say "Cracks?" and "≥99%?" — good start. Make them more specific: "Hot crack index < 0.1 (Kou criterion)", "ρ_rel ≥ 99.5% (Archimedes)", "UTS > 300 MPa (ASTM E8)". This demonstrates scientific rigor.

6. **Show what happens at NO-GO explicitly.** Arrow to "BOFN feedback → reformulate" or "Reject → archive data". Shows the decision logic is complete.

7. **Add a color legend.** Even a simple 3-word annotation: "Screening → Optimization → Qualification" aligned with the blue → gold → red gradient.

8. **Add deliverable callouts at key stages.** E.g., Stage 4: "→ Process Map", Stage 5: "→ Property Database", Stage 7: "→ Design Allowables". DOE wants to know what they're buying.

### Polish-Level Improvements:

9. Connect the defect hierarchy (right panel) to stages (left panel) with subtle visual links — matching colors, dashed lines, or numbered callouts.

10. Increase citation font size or switch to superscript number format with a compact reference block.

11. Add sample size justification: "40 compositions × 3-6 tensile bars = 120-240 specimens → sufficient for alloy-to-alloy statistical comparison at α=0.05."

---

## 5. Any remaining scientific accuracy issues?

**(A) COST INCONSISTENCY (Critical):** $850/alloy (throughput box) ≠ $1,000/alloy (MVS total). See above.

**(B) Hot cracking attrition rate may be too low.** The funnel shows ~200 → ~180 (10% failure) at Stage 2 (Thin Walls / crack screening). For novel Al alloys (especially 2xxx/7xxx and Al-Cu systems mentioned in the subtitle), literature suggests 30–50% of candidate compositions may exhibit hot cracking. A 10% elimination rate at the crack screening stage could appear naive to an expert reviewer. Consider either increasing this attrition rate or adding a note that CALPHAD pre-screening has already eliminated the worst crack-prone compositions.

**(C) H₂ porosity mitigation is oversimplified.** The defect hierarchy maps H₂ porosity → "Stage 0: Powder pre-dry." While powder drying reduces moisture-driven porosity, H₂ porosity in Al LPBF is also influenced by dissolved hydrogen in the melt pool, process parameters (scan speed, energy density), and atmospheric control. Labeling it solely as a Stage 0 issue may be seen as incomplete. Consider "Stage 0-1: Powder pre-dry + process params."

**(D) TRL 4 at Stage 6 (Post-Processing) is borderline.** TRL 4 formally requires "component validation in laboratory environment." HIP coupons alone may not fully satisfy this — typically TRL 4 involves testing sub-scale components, not just coupons. This is defensible but could be challenged.

**(E) Missing relevant standards.** ASTM E1019 (gas content analysis, relevant for H₂ porosity quantification) and ASTM B311 or equivalent (density measurement methodology for the density cubes) would strengthen the standards framework.

**(F) "52902 Z-Artefact" terminology.** ASTM 52902 defines benchmark test artifacts — the term "Z-Artefact" is informal. Consider "ASTM 52902 Benchmark Artifact" for precision.

**(G) Per-alloy time claim ambiguity.** "~3 days per alloy" is consistent with the MVS breakdown (~34 hours ≈ 3.5 working days), but this assumes serial processing. Since the "High-Throughput Acceleration" box mentions combinatorial builds (3-4 compositions per build plate), the actual per-alloy time would be lower when parallelized. The claim is conservative, which is fine, but could be stated more precisely.

---

## Summary: Priority-Ordered Action Items

| Priority | Item | Impact on Grade |
|----------|------|----------------|
| 1 | Fix text overlap Stages 5-9 | B+ → A- |
| 2 | Reconcile $850 vs $1,000 | Removes factual error |
| 3 | Add Phase I/II boundary | Shows DOE awareness |
| 4 | Add total program ROI math | Strengthens value prop |
| 5 | Add quantitative gate criteria | Demonstrates rigor |
| 6 | Add color legend | Improves interpretability |
| 7 | Reconsider hot cracking attrition rate | Improves scientific defensibility |
| 8 | Increase citation font size | Improves professionalism |

Items 1-3 would move the grade to **A-**. Items 1-6 would approach **A**.

---

## Discretionary Analytical Decisions

- Assessed text legibility via pixel-level cropping at native 300 DPI resolution rather than relying on thumbnail viewing, which may miss overlap artifacts
- Evaluated scientific accuracy of attrition rates against general Al AM literature rather than specific alloy system data (Al-Ce-X, Al-Cu-X), which could shift the expected hot cracking failure rate
- Judged TRL assignments against standard DOD/DOE TRL definitions rather than any project-specific TRL mapping that may exist
- Assessed cost consistency by summing the MVS itemized costs directly ($50+$100+$200+$300+$150+$200=$1,000) and comparing against the throughput box claim ($850), treating any discrepancy >5% as material
- Evaluated the throughput comparison visual impact partly on DOE reviewer expectations (quantitative ROI focus) rather than general academic figure standards
- Judged the hot cracking screening attrition rate (~10%) against published literature ranges (30-50% for novel Al alloys) while acknowledging that prior CALPHAD screening may have already filtered the most crack-prone compositions
