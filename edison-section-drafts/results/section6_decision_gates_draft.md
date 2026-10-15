# §6 — Decision Gate Metrics (Edison Draft)

## §6 — Decision Gate Metrics (LaTeX Draft, ~176 words)

```latex
\section{Decision Gate Metrics}\pagebudget{0.5}
\label{sec:gates}

Three quantitative metrics define Phase~I go/no-go evaluation.
%
\textbf{(1)~AI Acceleration Factor.}
$\mathrm{AF}(y) = n_{\mathrm{baseline}} / n_{\mathrm{BOFN}}$ measures the iteration reduction \bofn{} achieves relative to each of four pre-registered baselines---random search~(B1), expert DOE~(B2), standard BO~(B3), and a \bofn{} ablation without the mineral-burden objective~(B4)---with $\geq$20 replicate seeds, bootstrap confidence intervals, and win-rate reporting.
Phase~I target: AF\,$\geq$\,3$\times$ vs.\ random (conservative; the cross-study SDL median is $\sim$6$\times$~[Adesiji et al., 2026]).
%
\textbf{(2)~Discovery Yield.}
Fraction of BOFN-proposed compositions satisfying all family-specific mechanical thresholds (e.g., Al-Mn-Cr-Zr: YS\,$\geq$\,250\,MPa, EL\,$\geq$\,5\%; verified per ASTM E8) \emph{and} supply-risk reduction versus the Scalmalloy incumbent.
Phase~I target: $\geq$\,3\%.
%
\textbf{(3)~Mineral-Burden Reduction.}
Weighted critical-mineral content (wt\,\%) of the best-performing FLAIME alloy versus the Scalmalloy incumbent (Al-Mg-Sc-Zr).
Phase~I target: $\geq$\,30\% reduction.

\textbf{Scaling behavior.}
BOFN surrogate accuracy (cross-validated MAE) and acquisition efficiency improve monotonically as CALPHAD-screened and experimentally validated compositions accumulate, demonstrating increasing performance with additional data.

\medskip
\textbf{AI Tool Disclosure.}
This project uses AI tools including large language models for literature synthesis. All AI-generated content is reviewed and validated by the PI.
```

### Design rationale

This draft satisfies the ~180-word budget at ~176 words and addresses all specified requirements:

1. **AI Acceleration Factor** — Defined with the exact formula AF(y) = n_baseline / n_BOFN. The 4-baseline pre-registered benchmark structure (B1–B4) is enumerated explicitly so reviewers see the ablation design that isolates BOFN's function-network advantage (B3 vs. BOFN) from the mineral-burden objective's contribution (B4 vs. BOFN). Statistical rigor signaled via ≥20 seeds, bootstrap CI, and win-rate reporting per Turner et al. (2021) and Adesiji et al. (2026). The ≥3× target is anchored as "conservative" against the literature median of ~6× (Adesiji et al., 2026, *Digital Discovery*), preempting reviewer skepticism about feasibility.

2. **Discovery Yield** — Uses the PI-confirmed ≥3% target (from the proposal-population-plan.md PI resolution). Family-specific thresholds are mentioned with the Al-Mn-Cr-Zr example (YS ≥ 250 MPa, EL ≥ 5%) per the KPI deep-dive recommendations, and the dual gate (mechanical performance AND supply-risk reduction vs. Scalmalloy) ties directly to Topic 3B's mandate.

3. **Mineral-Burden Reduction** — Defined as wt% reduction against the Scalmalloy incumbent (Al-Mg-Sc-Zr), which is the primary supply-risk comparator from the metrics framework (SRI_mean ≈ 0.65, Sc-dominated). The ≥30% target is well-supported by the CMDRI analysis showing that Al-Mn-Cr-Zr and Al-Zr families have substantially lower Helbig SRI than Scalmalloy.

4. **Scaling behavior** — Uses the FOA's exact language ("increasing performance with additional data") and names two concrete, measurable indicators: cross-validated MAE improvement and acquisition efficiency.

5. **AI Tool Disclosure** — Verbatim from the user specification, satisfying the FOA requirement (§IV.C, p.71–72) and FAQ guidance.

### Discretionary analytical decisions

- **Chose Scalmalloy as the sole named incumbent comparator** for both Discovery Yield and Mineral-Burden Reduction, rather than also naming AlSi10Mg. Rationale: within a ~180-word budget, naming one high-supply-risk incumbent (SRI_mean ≈ 0.65) produces a cleaner, more impactful claim than splitting the comparison across two benchmarks. The metrics framework supports both comparators, but Scalmalloy yields a more dramatic and defensible reduction figure.

- **Cited Adesiji et al. (2026) as the literature anchor for the AF target** rather than citing multiple individual SDL campaigns (Kusne et al. 2020, MacLeod et al. 2022, etc.). Rationale: the cross-study median from a benchmarking review is more authoritative and word-efficient than listing individual AF values.

- **Used "weighted critical-mineral content (wt%)" as the mineral-burden metric** rather than the full Helbig 12-indicator + Ferro & Bonollo dual-index framework described in project-metrics-v4. Rationale: the word budget does not permit explaining the composite index methodology; "weighted critical-mineral content" is accurate, interpretable to reviewers, and the detailed methodology can be elaborated in §3 (Methods) or appendices.

- **Omitted explicit mention of the Enhancement Factor (EF)** and time-ledger decomposition from §6 to stay within word budget. These are covered in the AI advantage statement elsewhere in the narrative (§3/§5). The three go/no-go metrics are the most critical for §6.

- **Used ≥3% Discovery Yield (PI-confirmed) rather than the ≥20% Tier 1 target** from the full metrics framework. The PI explicitly confirmed 3% as the overall target (proposal-population-plan.md, PI resolution #3), which is the aggregate across all compositions screened (including CALPHAD-only), not just the Tier 1 rate among experimentally tested compositions.

- **Included "family-specific mechanical thresholds" with one example** (Al-Mn-Cr-Zr) rather than listing all three families (Al-Zr, Al-Mn-Cr-Zr, Cu-Cr-Zr). Rationale: word budget constraint; "e.g." signals that other families have their own thresholds.

- **Placed AI Tool Disclosure at the end of §6** consistent with the existing template structure (line 513–519 of flaime-genesis-proposal.tex), which already has a disclosure statement in this location. The updated text matches the user's specified wording exactly.