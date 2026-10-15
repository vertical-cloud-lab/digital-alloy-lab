# §2 — Project Objectives (Edison Draft)


## §2 — Project Objectives (LaTeX, ~247 words)

```latex
\section{Project Objectives}\pagebudget{0.5}
\label{sec:objectives}

\begin{enumerate}[label=\textbf{O\arabic*.},leftmargin=2em]
  \item Demonstrate a closed-loop BOFN/pKGFN platform for autonomous,
        cost-aware alloy screening across the full powder-to-property pipeline.
  \item Screen $\geq$200 Al-alloy compositions computationally via CALPHAD
        with an integrated mineral-burden objective.
  \item Validate $\geq$200 compositions experimentally through the MVS
        pipeline (2~compositions/day, 6~days/week, 9~months; $\sim$468
        theoretical max, $\geq$200 after ramp-up).
  \item Achieve overall discovery yield $\geq$3\% (compositions meeting all
        family-specific targets / total screened; complementary:
        $\geq$20\% Tier~1 pass rate among fully tested compositions).
  \item Demonstrate AI acceleration factor $\geq$3$\times$ vs.\ a
        pre-registered random baseline, with bootstrap confidence intervals
        across $\geq$20 seeds.
\end{enumerate}

\noindent Collectively, these objectives demonstrate that BOFN-guided
autonomous experimentation can simultaneously accelerate alloy discovery
\emph{and} reduce critical mineral dependence---the dual mandate of
Topic~3B. Phase~I focuses exclusively on Al alloys processed by LPBF,
with Cu-Cr-Zr as a stretch demonstration.

FLAIME advances from TRL~2 (BOFN DAG + CALPHAD pipeline designed)
to TRL~4 at Phase~I exit (closed-loop validated on real Al alloys)
to TRL~6 in Phase~II (system in relevant environment with
industry-scale powders).

The Be-Cu replacement market represents \$250--400M/yr; FLAIME's
industry pathway proceeds from powder production (Valimet) through
qualification to commercial feedstock supply (Fehrmann
Materials~GmbH). The platform will be released open-source; a Month-6
internal review will assess selective IP protection for top
compositions to best serve commercialization.

Phase~II will extend FLAIME to AMMTO priority alloys (e.g., 316H for
nuclear structural applications), leveraging transfer learning from
Phase~I surrogates. Technology transfer is further enabled by
integration of BOFN/pKGFN tutorials into the Honegumi platform and
Meta's BoTorch ecosystem.
```

### Content verification

All 8 priority-tier blocks from the user specification are present:

- **MUST-HAVE (~70w):** O1–O5 numbered list, front-loaded immediately after section header ✅
- **MUST-HAVE (~30w):** TRL 2 → 4 → 6 advancement with project-specific definitions ✅
- **MUST-HAVE (~15w):** Scope statement ("Phase I focuses exclusively on Al alloys processed by LPBF, with Cu-Cr-Zr as a stretch demonstration") ✅
- **HIGH (~40w):** Market sizing ($250–400M/yr Be-Cu replacement) + industry pathway (Valimet → Fehrmann Materials GmbH) ✅
- **HIGH (~25w):** IP strategy ("platform open-source; Month-6 internal review to assess selective IP for top compositions") ✅
- **HIGH (~15w):** Integrating sentence linking dual mandate of Topic 3B ✅
- **MEDIUM (~25w):** Phase II vision with one vivid example (316H for nuclear structural applications) ✅
- **MEDIUM (~20w):** Technology transfer sentence (Honegumi + BoTorch ecosystem) ✅

Total: ~247 words against a ~250 word budget.

### Sourcing notes

All quantitative targets, KPI definitions, TRL definitions, market figures, partner names, and throughput calculations are drawn directly from the attached documents:
- O1–O5 objectives and their numerical thresholds: `proposal-population-plan.md` §2 and `project-metrics-v4-edison-refined.md`
- Discovery yield dual-metric formulation (3% overall / 20% Tier 1): `proposal-population-plan.md` (PI-confirmed target + R9 H3 clarification)
- Throughput math (2 comp/day × 6 days/week × 9 months ≈ 468 theoretical max): `proposal-population-plan.md` §2 O3
- AI acceleration factor ≥3× vs. random: `edison-kpi3-acceleration-review.md` (conservative relative to median AF=6 across published SDL campaigns)
- TRL 2→4→6: `proposal-population-plan.md` §2 (R2 fix)
- $250–400M/yr Be-Cu market: `edison-3b-deepdive-synthesis.md` Part E
- Valimet → Fehrmann pathway: `ai-advantage-statement.md` partnership section
- IP strategy: `proposal-population-plan.md` §2 (D6 directive)
- 316H Phase II example: `proposal-population-plan.md` §2 (D3 directive, R14 revision)

### Discretionary analytical decisions

- **Word allocation across tiers:** Allocated slightly more words (~75w) to the O1–O5 list than the ~70w target to ensure each objective is self-contained and quantitatively precise, compensating by trimming the technology transfer sentence to ~15w (vs. ~20w target). Different writers might compress the objectives further or expand the market/IP paragraphs.

- **Omitted LOW-priority TRL definitions:** The TRL definitions (e.g., "concept formulated") were tagged as LOW (~30w) in the population plan and marked as movable to an appendix. I kept the TRL line compact (~30w) without spelling out the full DOE TRL definition text, relying on the parenthetical glosses to be self-explanatory. A more conservative writer might include the full definitions.

- **Chose "overall discovery yield ≥3%" as the headline metric rather than "≥20% Tier 1 pass rate":** The population plan notes both are valid and can coexist. I led with the ≥3% overall yield (PI-confirmed target) and presented the ≥20% Tier 1 pass rate as a complementary metric, following the R9 H3 clarification. A different writer might reverse the emphasis.

- **Used "cost-aware" in O1 rather than elaborating the pKGFN partial-evaluation mechanism:** This keeps the objective concise for a scanning reviewer; the technical detail of how cost-awareness is implemented (partial Knowledge Gradient over function networks) is better suited to §3 Methods. Another writer might omit "cost-aware" here to save words.

- **Placed the integrating sentence and scope statement as a single bridging paragraph after O1–O5 rather than as a separate paragraph:** This avoids paragraph fragmentation in a tight 0.5-page section. Some writers might prefer a more visually separated scope callout.

- **Selected 316H as the sole Phase II example:** The population plan lists 316H, IN718, and Hastelloy N as options. I chose 316H for nuclear structural applications because it is the most vivid single example tying to DOE mission relevance (nuclear energy). Another writer might choose IN718 (aerospace) or list multiple alloys.

- **Did not include the "to best serve" qualifier in the IP sentence:** The population plan's full D6 rationale discusses the PI's preference for fully open data. I compressed to a neutral "to best serve commercialization" phrasing rather than editorializing about the PI's open-science values, which are better placed in §5 Data Sources. A different writer might add the open-science framing.
