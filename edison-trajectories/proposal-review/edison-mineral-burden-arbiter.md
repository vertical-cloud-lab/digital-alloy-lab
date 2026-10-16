# Edison task 43d807d1-ae14-4595-a0e8-3baea047737c

Based on the quantitative analysis and review of the DoE FOA, the Baird 2023 roadmap, and the FLAIME proposal text, here is the adjudication of the two prior Edison approaches and a recommended path forward for the May 1 deadline.

### 1. Which approach better aligns with the Baird framework?
**Neither Approach A nor B perfectly captures the Baird framework alone, but a Hybrid approach best aligns with both Baird's philosophy and DoE merit criteria.**

- **Approach A (Dual-Baseline: Scalmalloy + AlSi10Mg)** captures Baird’s preference for multi-axis constraints over fragile single-scalar indices. By using two independent gates (a cost-weighted Sc-screen and a raw NIR backfill screen), it prevents one dimension from overwhelming the other. A materials skeptic reviewer would prefer this because it establishes clear physical boundaries (Sc must be eliminated; other critical minerals cannot exceed an industry-standard floor).
- **Approach B (Log-Cost CMDRI)** relies on a mathematical trick (log compression) to tune a single scalar index so that Sc dominates (64%) without swallowing the entire objective (99.5%). This is precisely the kind of "tuned composite index with hidden calibration" that Baird 2023 warns against (citing Schellens & Gisladottir). An AI/ML reviewer might appreciate the continuous differentiable gradient this provides the BOFN surrogate, but a materials skeptic would find the log-cost weighting arbitrary and non-physical. 

**Recommendation:** A **Hybrid Approach** is the most defensible. It preserves Approach A's rigorous dual-baseline architecture (Sc-screen + AlSi10Mg backfill screen) but integrates Approach B's log-cost mathematical continuous gradient for the internal BOFN objective. Most importantly, it introduces structured 2D reporting (Import Reliance vs. Market Concentration) to directly satisfy Baird's multi-axis visualization imperative. 

### 2. Are both missing HHI?
**Yes, both prior tasks completely omitted HHI.** Baird 2023 explicitly emphasizes HHI (market concentration) as an orthogonal dimension to import reliance (e.g., Magnesium is only 50% import reliant but has a very high HHI of 5500 due to >70% Chinese production; Manganese is 100% import reliant but has a moderate HHI of 1800 from diverse sources).

**How cheaply can it be fixed?**
Do *not* multiply HHI into the CMDRI gate formula. When HHI is added as a weight factor, the discrimination collapses (all non-Sc alloys cluster around ~65% reduction) because the triple-product (NIR × Cost × HHI) over-compresses the metric. Instead, HHI should enter as **required reporting metadata and a secondary BOFN contextual node**. The M6 deliverable must include a DoE-style 2D criticality matrix plotting NIR vs. HHI for all evaluated compositions.

### 3. Data/Terminology Precision
The proposal currently conflates four terms: MBS, SRI, CMDRI, and Mineral-Burden Reduction. This must be standardized. 

**Terminology Standardization:**
- **MBS_linear:** The linear cost-weighted formula used *only* for the Gate 3a Sc-elimination screen.
- **CMDRI_log:** The log-cost weighted formula used for the Gate 3b backfill ceiling and the BOFN objective.
- Drop "SRI" entirely to avoid confusion with the Helbig SRI scores mentioned in Appendix 4. 

**Data Provenance & Versioning:**
- **Freeze at campaign start (Month 1):** USGS MCS 2024 Net Import Reliance (NIR) figures, computed HHI_production from the same 2024 data, and the 3-year trailing average metal prices (2022–2024). Freezing ensures the BOFN algorithm has a stationary target across the 9-month Phase I pipeline.
- **Contextual Note:** The 2025 USGS final list (89 FR 106015) explicitly added Aluminum and Silicon as critical minerals. The proposal text must note this addition but specify that the CMDRI formula excludes the base element (Al) so the alloying penalty remains measurable.

### 4. Hybrid Draft: Reviewer-Ready G3 Paragraph
Here is the hybrid synthesis for insertion into Section 6 (Decision Gate Metrics, Table 2 replacement) that resolves the critique:

> **Mineral-Burden Reduction (Gate G3, Month 7).** We assess supply-risk reduction through a dual-baseline gate inspired by the DoE 2011 two-axis criticality framework [Baird & Sparks 2022, §2; DoE 2011]:
> 
> **Gate G3a — Scandium-elimination screen.** MBS_linear(alloy) ≤ 0.10 × MBS_linear(Scalmalloy), where MBS_linear = Σ_{i≠Al} NIR_i · (c_i / c_Al) · x_i, NIR_i is the USGS net import reliance for element i (MCS 2024, frozen at campaign start), c_i is the 3-year average metal price (2022–2024), and x_i is the weight fraction. Because scandium contributes 99.5% of Scalmalloy's MBS_linear (at ~$5,000/kg and 100% import reliance for only 0.7 wt%), any Sc-free alloy passes this screen trivially. G3a therefore functions as a confirmatory check that the BOFN mineral-burden objective has steered the campaign away from Sc dependence.
> 
> **Gate G3b — Backfill-prevention ceiling.** CMDRI_log(alloy) ≤ 1.5 × CMDRI_log(AlSi10Mg), where CMDRI_log = Σ_{i≠Al} NIR_i · log₁₀(1 + c_i/c_Al) · x_i. The logarithmic compression reduces the Sc:Mn cost ratio from ~2500:1 to ~13:1, ensuring Sc no longer dominates the continuous BOFN surrogate while still penalizing expensive, import-reliant additions (e.g., Zr at $35/kg and 100% NIR). The AlSi10Mg baseline—the most widely adopted unpatented LPBF aluminum alloy—establishes a credible industry-standard supply-risk floor. At the 1.5× threshold, Al–3Mn–1Cr–1Zr (ratio 1.41×) passes while Al–5Mn–1.5Cr–0.5Zr (ratio 1.53×) fails, providing meaningful discrimination among candidate alloy families without permitting unconstrained heavy-element backfilling.
> 
> **Reporting (M6).** For every composition evaluated through tensile testing, the digital thread records per-element NIR, HHI_production, HHI_reserve (USGS MCS 2024), and 3-year average cost, enabling post-hoc visualization as a DoE-style 2D criticality matrix (import reliance vs. market concentration, bubble size proportional to wt%) per the methodology reviewed in [12]. This structured decomposition ensures auditability and compatibility with evolving DOE and USGS criticality designations, including the 2025 USGS final list that adds Al, Si, and Cu as critical minerals.

### 5. Risk of Proposal Correctness (Editing Checklist)
To implement this cleanly before May 1, update these specific locations in the `flaime-genesis-proposal-clean.pdf`:

1. **Page 1 (Abstract):** Replace "≥40% mineral-burden reduction vs. Scalmalloy" with "dual-baseline G3 mineral-burden gates (Scalmalloy Sc-elimination and AlSi10Mg backfill ceilings)."
2. **Page 4 (§2, Objective O4):** Replace "≥40% mineral-burden reduction vs. Scalmalloy" with "satisfying the dual-baseline Gate G3 mineral-burden constraints vs. Scalmalloy and AlSi10Mg."
3. **Page 5 (§3, Activity 1):** Update the MBS formula sentence to reflect the dual mathematical definitions (`MBS_linear` for the gate, `CMDRI_log` for the continuous BOFN objective node). 
4. **Page 5 (§3, Activity 1):** Clarify that HHI, Graedel, and ESSENZ factors are captured as "digital thread reporting metadata" rather than collapsing them directly into the scalar BOFN node.
5. **Page 7 (Table 1, M5/G3 Go/No-Go):** Delete "SRI mean ≥25% below Scalmalloy" and replace with "G3a MBS_linear ≤ 10% of Scalmalloy AND G3b CMDRI_log ≤ 1.5× AlSi10Mg".
6. **Page 7 (Table 1, M6 Final Deliverables):** Delete "CMDRI calculation vs. Scalmalloy (≥40% reduction target)" and replace with "Dual-gate CMDRI validation and 2D DoE-style criticality matrix reporting."
7. **Page 7 (§6, Table 2):** Replace the entire "Mineral-Burden Reduction" row definition with the hybrid G3 draft text above.
8. **Page 12 (App 4, DMSP §4):** Append ", HHI_production, HHI_reserve, and 3-year average cost derived from the frozen USGS MCS 2024 dataset" after "Helbig SRI scores."

*Note: No downstream budget adjustments or physical pipeline milestones are triggered by this swap, as the analytical nodes execute freely on the HPC.*

***

### Discretionary Analytical Decisions
- **Selection of multiple baselines vs. composite index:** Chose to retain two distinct formulas (a linear cost-weighted MBS for the Scandium gate, and a log-cost weighted CMDRI for the AlSi10Mg backfill gate) rather than attempting to forge a single composite scalar. This aligns with the Baird paper's critique of fragile single metrics.
- **HHI reporting structure:** Decided against incorporating HHI into the gating formulas. Quantitative testing demonstrated that a triple-product weight (NIR × Cost × HHI) over-compresses the scoring distribution, causing discrimination between Sc-free alloys to collapse to a ~65% reduction baseline.
- **Alloy reference choices:** Maintained the proposal's choice of Scalmalloy (as the Sc-bearing maximum boundary) and AlSi10Mg (as the industry-standard minimum boundary), rejecting alternative theoretical zero-criticality baselines to ensure the metric stays grounded in deployable AM physics.
- **Threshold calibration:** Maintained the 1.5× AlSi10Mg threshold developed in Task A and the 10% Scalmalloy threshold for the linear gate based on the derived mathematical impact of Sc removal (which naturally achieves 99.5% reduction in linear cost-weighted sum).
- **Versioning strategy:** Elected to freeze USGS MCS 2024 values and 2022-2024 trailing average prices at campaign kickoff (Month 1) rather than dynamically updating them through the 9-month Phase I, ensuring the BOFN objective gradient remains stationary for fair comparability between M1 and M9 compositions.
