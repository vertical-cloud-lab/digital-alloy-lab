# §4 — Milestones (Edison Draft)

## §4 — Milestones in the Nine Months (~200 words + Table 1)

### Narrative Text (for LaTeX insertion)

FLAIME's nine-month execution plan is structured around six milestones, three of which are formal Go/No-Go gates timed to bracket the Month 6 DOE programmatic review. Months 1–3 establish infrastructure: the BOFN decision engine, CALPHAD screening pipeline (Thermo-Calc TCAl10 + AM Module on BYU HPC), and first atomized powder batches for Al-Zr and Al-Mn-Cr-Zr candidates. Gate G1 (Month 3) verifies that the computational surrogate is learning — ≥50 compositions screened with surrogate RMSE below a pre-registered threshold — ensuring the AI backbone is functional before committing to expensive LPBF builds.

Months 4–5 transition to steady-state closed-loop operation. Gate G2 (Month 5) requires a complete, end-to-end autonomous CALPHAD→atomization→LPBF→tensile→BOFN cycle, demonstrating cyberphysical integration rather than isolated components. Milestones M3–M5 collectively provide the evidence base for the 6-month DOE review: by Month 7, Gate G3 demands ≥1 supply-risk-reduced alloy meeting family-specific mechanical thresholds (Al-Mn-Cr-Zr: YS≥250 MPa, EL≥5%; Al-Zr: YS≥200 MPa, EL≥8%), verified by ASTM E8 testing with ≥3 replicates. Month 9 deliverables include the complete digital thread (≥85% provenance completeness with supply-risk metadata), CMDRI calculations vs. Scalmalloy, and a Phase II readiness assessment. Decision-ready KPIs and triggered optimizer actions are summarized in Table 1.

---

### Milestone Table (for LaTeX insertion — replaces placeholder)

```latex
\begin{table}[H]
\centering\small
\caption{Phase~I milestones and deliverables (9~months).}
\label{tab:milestones}
\begin{tabularx}{\textwidth}{clX}
\toprule
\textbf{Mo.} & \textbf{ID} & \textbf{Milestone / Deliverable} \\
\midrule
1 & M1 & BOFN DAG deployed; CALPHAD screening pipeline (TCAl10 + AM Module) operational on BYU HPC; first Al-Zr and Al-Mn-Cr-Zr candidate compositions selected; Helbig SRI calculator built and Scalmalloy benchmark computed \\
2 & M2 & First atomized powder batches characterized (PSD, SEM/EDS, flowability); pre-registered 5-baseline benchmark design frozen; formal provenance schema deployed \\
3 & M3/G1 & \textbf{Go/No-Go G1:} $\geq$50 compositions screened computationally; GP surrogate RMSE $<$ pre-registered threshold on nested CV. \textit{If fail: retrain surrogate with augmented CALPHAD data; extend G1 by 1~month.} \\
5 & M4/G2 & \textbf{Go/No-Go G2:} $\geq$1 complete autonomous CALPHAD$\to$atomization$\to$LPBF$\to$tensile$\to$BOFN cycle demonstrated end-to-end; $\geq$2 compositions at $\geq$99.0\% relative density. \textit{If fail: decouple pipeline; run semi-autonomous with manual handoffs.} \\
7 & M5/G3 & \textbf{Go/No-Go G3:} $\geq$1 alloy meeting family-specific thresholds (Al-Mn-Cr-Zr: YS$\geq$250~MPa, EL$\geq$5\%; Al-Zr: YS$\geq$200~MPa, EL$\geq$8\%) with SRI$_\text{mean}$ $\geq$25\% below Scalmalloy; ASTM~E8 data with $\geq$3 replicates. \textit{If fail: pivot to strongest partial-pass composition; intensify BOFN exploitation.} \\
9 & M6 & Final deliverables: digital thread ($\geq$85\% completeness with supply-risk metadata); CMDRI calculation vs.\ Scalmalloy ($\geq$40\% reduction target) and AlSi10Mg; pre-registered AI benchmark report (AF, win rate, bootstrap CI); Phase~II readiness assessment \\
\bottomrule
\end{tabularx}
\end{table}
```

---

### Table 1 — KPI/Go-No-Go Dashboard (LaTeX, booktabs)

```latex
\begin{table}[H]
\centering\small
\caption{KPI/Go-No-Go dashboard with triggered optimizer actions. Gates are tied to autonomous next actions, enabling efficient sequential experimentation in costly, high-dimensional settings.}
\label{tab:kpi-dashboard}
\setlength{\tabcolsep}{4pt}
\begin{tabularx}{\textwidth}{@{}lllX@{}}
\toprule
\textbf{KPI} & \textbf{Threshold} & \textbf{Measurement} & \textbf{Triggered Optimizer Action} \\
\midrule
AI Acceleration Factor & $\geq$3$\times$ vs.\ random; $\geq$1.5$\times$ vs.\ std.\ BO & Pre-registered 5-baseline benchmark, $\geq$20 seeds, bootstrap CI & If AF${<}$2$\times$: widen BOFN exploration; increase batch diversity; report total platform acceleration via time-ledger decomposition \\
\addlinespace
Discovery Yield & $\geq$3\% overall; $\geq$20\% Tier~1 among fully tested & ASTM~E8 tensile + ICP-OES + Helbig SRI; family-specific thresholds & If yield${<}$3\%: shift BOFN to exploit mode near best partial-pass compositions; request additional replicates for borderline alloys \\
\addlinespace
Mineral-Burden Reduction (CMDRI) & $\geq$40\% SRI$_\text{mean}$ reduction vs.\ Scalmalloy & Helbig 12-indicator + Ferro \& Bonollo ACI; element-level waterfall & If CMDRI${<}$25\%: activate mineral-burden scalarization weight increase in BOFN; expand search to lower-Zr compositions \\
\addlinespace
Surrogate RMSE (YS) & $\leq$40~MPa (MAE, nested CV) & GP surrogate on BOFN function network; prospective holdout & If MAE${>}$50~MPa: augment training with CALPHAD-derived features; increase experimental replicates at informative compositions \\
\addlinespace
Closed-Loop Throughput & $\geq$8 comp./month sustained; pipeline completion $\geq$70\% & Compositions with complete tensile records per month (primary) & If throughput${<}$5/month: switch to tiered screening (density-only for 60\% of compositions); activate Valimet gas atomization fallback \\
\bottomrule
\end{tabularx}
\end{table}
```

---

### Discretionary Analytical Decisions

- **Selected 5 KPIs for Table 1 from the 6 headline KPIs in the metrics document**: Chose AI Acceleration Factor, Discovery Yield, CMDRI, Surrogate RMSE, and Closed-Loop Throughput as the five most reviewer-salient metrics for a compact dashboard. Omitted Mineral-Burden Optimization Efficacy (hypervolume ratio) and Digital Thread Completeness as standalone table rows to fit the ~0.25 page budget; Digital Thread completeness is captured in the M6 milestone row instead.

- **Used PI-confirmed ≥3% overall discovery yield target alongside the metrics document's ≥20% Tier 1 pass rate**: These are complementary metrics (3% is compositions meeting all targets / total screened; 20% is Tier 1 Full Pass among only fully tested compositions). Both are reported in the Discovery Yield KPI row rather than choosing one.

- **Set CMDRI threshold at ≥40% vs. Scalmalloy (Expected target) rather than ≥25% (Base target)**: The Expected target is more impactful for a reviewer-facing table; the Base target of ≥25% is the mandatory Go gate minimum documented in the go/no-go framework.

- **Used ≥250 MPa YS / ≥5% EL for the M5/G3 milestone narrative text rather than listing both family-specific thresholds in the short narrative**: The Al-Mn-Cr-Zr thresholds are the more stringent of the two families and serve as a single memorable number. Both family-specific thresholds (Al-Mn-Cr-Zr: YS≥250/EL≥5%; Al-Zr: YS≥200/EL≥8%) are specified in the milestone table itself for precision.

- **Included "If fail" fallback actions in the milestone table**: This is a stylistic choice — some proposal writers keep fallbacks in narrative text only. Including them directly in the table signals risk awareness to reviewers within the tight 5-page limit.

- **Chose Surrogate RMSE as the 4th KPI over Digital Thread Completeness or Mineral-Burden Optimization Efficacy**: Surrogate RMSE (≤40 MPa MAE) is the most directly measurable AI-specific metric at the G1 gate and signals model quality to reviewers. Digital Thread is captured in M6; Mineral-Burden Efficacy (hypervolume ratio) is a Month 7 deliverable better suited to §6 Decision Gate Metrics.

- **Set narrative word count at approximately 200 words**: Consistent with the proposal population plan's ~200w + table budget for §4, leaving room for the table within the ~1 page allocation.

- **Framed 6-month DOE review around M3–M5 (Months 3–7) rather than a single Month 6 milestone**: The FOA specifies a "go/no-go evaluation at 6 months." Rather than creating an artificial Month 6 milestone, the narrative explains that three gates bracketing Month 6 collectively demonstrate sufficient progress, which is more defensible given that experimental timelines may not align exactly with calendar months.

- **Used Scalmalloy (SRI ≈ 0.65) as the primary CMDRI comparator rather than AlSi10Mg (SRI ≈ 0.25)**: Per the metrics document's recommendation, comparison against Scalmalloy produces a more impactful and defensible supply-risk reduction claim (~40% reduction is achievable and meaningful vs. Sc-dominated incumbent). AlSi10Mg comparison (≥15%) is noted in the full metrics but omitted from the compact Table 1 for space.

- **Included bootstrap CI requirement in the AI Acceleration Factor measurement column**: This follows the pre-registered benchmark protocol from the metrics document and signals statistical rigor to reviewers, though it adds ~3 words to an already dense table.