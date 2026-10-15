# FLAIME LaTeX Proposal Population Plan — v5.6 (R14 A-grade, narrative improvements + Appendix 5 fixes)

> **Target:** `genesis-mission-proposal/flaime-genesis-proposal.tex`
> **Constraint:** 5-page Project Narrative (FOA §IV.C), all figures/tables count against limit
> **Source corpus:** 100+ Edison trajectory outputs, benchmark code, figure assets, PI CV (`bios/baird-CV.pdf`)
> **Estimated output:** ~1,570 words body text + 4 figures + 1 table + appendix content
> **Edison grades:** R1: B → R2: A- → R3: A- → R4: A- → R5: A-(strong) → Checklist R6-R8: A → **R9-R14: A**
> **Status:** R14 narrative improvements integrated (urgency lead, "why now", scope statement, competitive sharpening). Appendix 5 Activity 4 strengthened + AM reference added. Budget footnote added. Writing sprint approved — zero blocking items. Continuing Edison cycles.

### PI-Confirmed Resolutions (2026-04-14)

| #   | Item                | Resolution                                                                                                                  |
| --- | ------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Personnel**       | PI + 2 MS + 10 UGs (PI-confirmed 2026-04-14)                                                                                |
| 2   | **Partners**        | Valimet (funded partner) and AMAZEMET (funded partner) submit independent applications; Thermo-Calc AB is an unfunded collaborator  |
| 3   | **Discovery yield** | ≥3% target confirmed                                                                                                        |
| 4   | **Fig 3**           | Include **both** 4-panel composite AND tensile data — use 4 narrative figures (tight but feasible at ~1.5 pages of figures) |

### PI Directives (2026-04-14, comment 4241412845)

The PI provided detailed narrative guidance to strengthen the plan. These directives are woven into the relevant sections below but are collected here for traceability:

| #   | Directive                                                                                                                                                                                             | Where Addressed                                    |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| D1  | **PI Background — SDL at scale:** Lean into ability to deploy SDL solutions at scale, reusable software, tutorials, training. Frequent involvement in standardization (POSE, AC, FAIR, GCMAC, etc.)   | §1 Background, §3 Methods (Activity 3), Biosketch  |
| D2  | **Honegumi + BoTorch tutorials:** Integrate new tutorials into Honegumi platform and source code into Meta's BoTorch tutorials. Note letter of support from Meta.                                     | §3 Methods (Activity 3), §5 Data Sources           |
| D3  | **Broader Genesis Mission applicability:** Describe how the FLAIME framework could apply to other Genesis Mission avenues — nuclear, quantum, etc. Specific motivating examples tying to CMS pillars. | §1 Background, §2 Objectives (Phase II vision)     |
| D4  | **Human-in-the-loop SDL leader:** Point to the frugal twin review paper. Recognized leader in SDLs for structural materials (lead author on SDL review paper structural materials section).           | §1 Background, Biosketch                           |
| D5  | **Workflow orchestration leadership:** Especially while at the Acceleration Consortium.                                                                                                               | §3 Methods, Biosketch                              |
| D6  | **Open-source vs proprietary IP:** PI leans fully open-source but unsure about path to greatest impact vs. grant acceptance likelihood. Address both strategies.                                      | §2 Objectives (Commercialization), §5 Data Sources |
| D7  | **Open data contributions:** Lean into Zenodo, Figshare contributions. Point to heavy reuse of MPTS-52 dataset among crystal structure generative AI community as evidence of data impact.            | §5 Data Sources, Biosketch                         |
| D8  | **SciENcv biosketch:** PI CV at `bios/baird-CV.pdf`. Biosketch should use SciENcv format.                                                                                                             | Phase 4: Budget & Forms                            |

---

## Figure & Visual Asset Inventory

### Available Generated Figures (in repo)

| Asset                       | Path                                                            | Description                                                                                    | Proposal Use                                  |
| --------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **4-panel composite** (a–d) | `edison-trajectories/fig_compositor.py`                         | Multi-fidelity pipeline (a), throughput comparison (b), defect hierarchy (c), MVS validation set (d) | **Narrative Fig. 3** — experimental framework |
| Multi-fidelity subfigure    | `edison-trajectories/subfig_stagegate.py`                       | 10-stage pipeline with BOFN loop callout                                               | Panel (a) of composite                        |
| Throughput subfigure        | `edison-trajectories/subfig_throughput.py`                      | FLAIME vs. traditional cost/time comparison                                                    | Panel (b) of composite                        |
| Defect hierarchy subfigure  | `edison-trajectories/subfig_defects.py`                         | Al alloy defect evaluation priority map                                                         | Panel (c) of composite                        |
| MVS subfigure               | `edison-trajectories/subfig_mvs.py`                             | Minimum viable validation set per alloy                                                        | Panel (d) of composite                        |
| LPBF parameter space        | `figures/lpbf_parameter_space.png`                              | 36-parameter taxonomy tile grid                                                                | Appendix 2 (Facilities)                       |
| Panel A: parameter grid     | `figures/panels/panel_a_parameter_grid.py`                      | Tile grid of LPBF parameters by category                                                       | Appendix 2                                    |
| Panel B: dimensionality     | `figures/panels/panel_b_dimensionality.py`                      | Dimensionality reduction visualization                                                         | Appendix 2                                    |
| Panel C: network            | `figures/panels/panel_c_network.py`                             | BOFN function-network DAG visual                                                               | Integrated into Fig. 1                        |
| AM test structures          | `edison-trajectories/fig-am-test-structures-schematics.png`     | Build plate layout schematics (single tracks → tensile bars)                                   | Appendix 2                                    |
| AM scaleup progression      | `edison-trajectories/fig-am-scaleup-validation-progression.png` | Validation progression from Phase I → Phase II                                                 | Appendix 2                                    |
| BOFN DAG                    | `benchmarks/figures/bofn_dag.png`                               | 4-node function network DAG                                                                    | **Narrative Fig. 1** (AI framework)           |
| pKGFN convergence           | `benchmarks/figures/pkgfn_convergence.png`                      | pKGFN vs. baselines convergence curves                                                         | **Narrative Fig. 1** (convergence subplot)    |
| pKGFN cost efficiency       | `benchmarks/figures/pkgfn_cost_efficiency.png`                  | Cost-aware evaluation comparison                                                               | Text reference in §6                          |
| pKGFN DAG                   | `benchmarks/figures/pkgfn_dag.png`                              | pKGFN partial evaluation DAG                                                                   | Text reference in §3                          |
| pKGFN node selection        | `benchmarks/figures/pkgfn_node_selection.png`                   | Node selection frequency analysis                                                              | Text reference                                |
| CALPHAD landscape           | `benchmarks/figures/calphad_landscape.png`                      | CALPHAD evaluation landscape                                                                    | **Narrative Fig. 2** (left panel)             |
| GP accuracy                 | `benchmarks/figures/gp_accuracy.png`                            | GP surrogate model accuracy                                                                    | Text reference                                |
| Cost evaluation             | `benchmarks/figures/cost_screening.png`                         | Cost-aware evaluation behavior                                                                  | Text reference                                |
| LLM warmstart               | `benchmarks/figures/llm_warmstart_convergence.png`              | LLM-guided warmstart convergence                                                               | Text reference                                |
| LPBF process window         | `benchmarks/figures/lpbf_process_window.png`                    | Process window visualization                                                                   | Appendix 2                                    |
| **SEM/EDS images**          | *✅ Data in hand (PI confirmed)*                                 | SEM/EDS of precursor powders + AMAZEMET-atomized mixture                                       | **Narrative Fig. 2** (right panels)           |
| **Tensile data**            | *✅ Data in hand (PI confirmed)*                                 | AlSi10Mg stress-strain curves + YS/UTS/EL bars                                                 | **Narrative Fig. 4**                          |

### Figure Allocation for 5-Page Narrative (REVISED per Edison feedback)

Aligned with preliminary-results-roadmap.md triage (Edison 8.0/10) — **experimental evidence now in narrative**:

| Slot        | Content                                                                                                                                    | Source Asset(s)                                    | Section                    | Est. Space |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------- | -------------------------- | ---------- |
| **Fig. 1**  | pKGFN closed-loop pipeline: (a) BOFN DAG + workflow schematic, (b) convergence curves showing cost-aware advantage                         | `bofn_dag.png` + `pkgfn_convergence.png` composite | Methods §3                 | ~0.35 page |
| **Fig. 2**  | CALPHAD evaluation + experimental evidence: (left) evaluation landscape, (right) SEM/EDS multi-panel of precursor powders + atomized mixture | `calphad_landscape.png` + SEM/EDS images from PI   | Background §1 / Methods §3 | ~0.4 page  |
| **Fig. 3**  | 4-panel composite: (a) multi-fidelity pipeline, (b) throughput comparison, (c) defect hierarchy, (d) MVS validation set                          | `fig_compositor.py`                                | Methods §3                 | ~0.35 page |
| **Fig. 4**  | Tensile data: AlSi10Mg stress-strain curves + YS/UTS/EL bar chart (experimental evidence from U Utah and 3D Powder Tech)                   | Tensile data from PI                               | Results / Methods §3       | ~0.25 page |
| **Table 1** | KPI / go-no-go dashboard with triggered optimizer actions                                                                                  | From `project-metrics-v4-edison-refined.md`        | Milestones §4              | ~0.25 page |

**Total figure/table space:** ~1.6 pages (tight but feasible within 5-page limit — may need word count compression to ~1,570 words)

### Figure Overflow Contingency (R3 improvement #5)
**Trigger:** Compiled LaTeX PDF exceeds 5.0 pages.
- **Fallback A:** Drop Fig 3 (4-panel composite) — saves ~0.35 page
- **Fallback B:** Merge Fig 4 (tensile) into Fig 2 as additional panels — saves ~0.25 page
- **Fallback C:** Shrink Table 1 from 5 KPIs to 3 headline KPIs — saves ~0.1 page

### Adjusted Word-Count Targets (R3 improvement #6)
With 4 figures + 1 table (~1.6-2.0 pages), text budget drops to ~1,570 words across 6 sections:
| Section               | Old Target  | New Target                     |
| --------------------- | ----------- | ------------------------------ |
| §0 Overview paragraph | —           | ~80w                           |
| §1 Background         | ~500w       | ~300w (R10 rebalance)          |
| §2 Objectives         | ~250w       | ~250w (R10 expanded from 180w) |
| §3 Methods            | ~750w       | ~400w                          |
| §4 Milestones         | ~350w       | ~200w + table                  |
| §5 Data Sources       | ~200w       | ~160w                          |
| §6 Decision Gates     | ~250w       | ~180w (R10 rebalance)          |
| **Total**             | **~2,500w** | **~1,570w**                    |

**Appendix figures** (no page limit):
- AMAZEMET atomizer installation photo → Appendix 2 (Facilities)
- LPBF parameter space tile grid → Appendix 2
- AM test structure schematics → Appendix 2
- Expanded pKGFN results (cost efficiency, node selection) → Appendix 2
- LPBF process window → Appendix 2

---

## Hierarchical Search Space Architecture (from Edison Search Space Reframing Assessment)

> **Source:** `edison-trajectories/edison-search-space-reframing.md` (Edison graded current framing B → proposed reframing A-)
> **Addresses:** PR #26 "trivial satisfaction" risk — broad palette creates genuine MBS variance

### 15-Element Al-Alloy Palette

| Tier                              | Elements               | Rationale                                                                    |
| --------------------------------- | ---------------------- | ---------------------------------------------------------------------------- |
| **Core** (high TCAl10 coverage)   | Mn, Cr, Zr, Mg, Si, Cu | Established Al alloying elements; strong binary/ternary assessment in TCAl10 |
| **Expanded** (moderate coverage)  | Ti, Fe, Ni, Ce, Sc     | Important for AM alloys; partially assessed ternaries                        |
| **Exploratory** (sparse coverage) | Li, Er, Zn, Sn         | Emerging/niche elements; some binary-only extrapolation                      |

**Supply-risk variance:** Fe = 0% USGS import reliance → Sc = 100% import reliance. This full span ensures the mineral-burden score (MBS) produces genuine supply-chain tradeoffs — directly addressing the PR #26 concern that restricting to inherently low-critical-mineral elements makes the KPI trivially satisfied.

### Two-Level Search Architecture

**Level 1 — Element Combination Selection (computational, under 1 hour on HPC):**
- Evaluate all C(15,k) for k=2..8 = **22,803 sub-systems** spanning ternary through 9-component alloys:
  - C(15,2) = 105 ternary (e.g., Al-Fe-Si)
  - C(15,3) = 455 quaternary (e.g., Al-Mn-Cr-Zr)
  - C(15,4) = 1,365 quinary
  - C(15,5) = 3,003 senary
  - C(15,6) = 5,005 septenary
  - C(15,7) = 6,435 octonary
  - C(15,8) = 6,435 nonary
- Level 1 uses an **asynchronous, cost-aware multi-fidelity framework**:

  **Fidelity 1 (pycalphad, $0):** Sobol/LHS coarse sampling (~50 compositions per sub-system, ~1.13M total evaluations) computes equilibrium phase fractions, Scheil solidification curves, crack-susceptibility index (CSI), and mineral-burden scores for all 22,803 sub-systems. At ~10 calcs/sec/core on 64 cores, completes in under one hour on a single BYU HPC node.

  **Fidelity 2 (TC-Python + TCAl10, licensed):** Targeted sub-systems receive Scheil solidification with back-diffusion (MOBAL8 solver), TC-PRISMA precipitation kinetics (e.g., L₁₂-Al₃Zr nucleation and coarsening), and fully assessed multicomponent thermodynamics with ternary interaction parameters unavailable in free databases.

  **Fidelity 3 (Thermo-Calc AM Module):** Selected compositions receive steady-state printability maps (lack-of-fusion/stable/keyhole regimes), melt-pool geometry, G/R conditions overlaid on the columnar-to-equiaxed transition (CET), and Scheil curves with solute-trapping extension at LPBF cooling rates (10⁴–10⁶ K/s). Identifies unprintable candidates before any powder is atomized.

- All fidelity levels run at maximum HPC parallelism (fairshare-limited, not algorithm-sequenced); async BO treats pending jobs as fantasy samples, updating the surrogate as each completes
- CALPHAD outputs (phase fractions, solidification range, CSI) flow as features to all downstream GP nodes — not discarded after evaluation
- GP scaling: exact GP for ≤5 components (≤3,876 compositions), SVDKL deep kernel GP for 6–7 components (15K–54K), SVDKL+RF for 8 components (170K+)
- Cost-aware pKGFN decides which expensive evaluations to request next based on all available data
- **Novel contribution:** NChooseK element-combination selection via Bayesian optimization with mineral-burden objective — no published precedent
- **Published precedents for scale:** Vazquez 2023 (500K TC-Python evals), Wang 2025 (150K→2B via ML surrogate), Sundar 2025 (CALPHAD BO)

**Level 2 — Composition Optimization (experimental, 9-month campaign):**
- pKGFN optimizes compositions within top 3–6 sub-systems through the full powder-to-tensile pipeline
- Al-Mn-Cr-Zr and Al-Zr are guaranteed "anchor" systems — receive experimental validation regardless of Level 1 rankings
- Composition dimensionality per sub-system: 4-component = 816 compositions (exact GP tractable), 6-component = 155K (SVDKL needed)
- Experimental budget: 100–200 compositions through MVS pipeline

### TCAl10 Coverage Note

Al-Mn-Cr-Zr has 0/4 constituent ternaries assessed in TCAl10 — all predictions rely on binary extrapolation. This is acceptable for dilute Al-rich compositions but should be acknowledged as a limitation. The 15-element palette achieves 53.3% assessed ternary coverage overall, which is strong for quaternary prediction.

---

## Phase 1: Title Page & Abstract

### §0 — Project Summary / Abstract (Field 7, drafting copy)
- **Sources:** `ai-advantage-statement.md`, `edison-3b-deepdive-synthesis.md`, `project-metrics-v4-edison-refined.md`, `edison-search-space-reframing.md`
- **Action:** Replace `\lipsum` with ~250-word abstract:
  - Vision: autonomous closed-loop platform for critical-mineral-lean Al alloy discovery
  - AI advantage thesis: BOFN + pKGFN reduces experiments 10× vs. conventional DOE
  - **Hierarchical search:** Screen $\sum_{k=2}^{8} C(15,k) = 22,803$ sub-systems (ternary through 9-component) from 15-element palette, then focus experiments on top 3–6 (including Al-Mn-Cr-Zr and Al-Zr anchors)
  - Critical minerals relevance: 15-element palette spans 0%–100% USGS import reliance
  - Expected outcomes: 100–200 compositions screened experimentally, digital thread on AmSC
  - **TRL statement:** FLAIME enters Phase I at TRL 2 → targets TRL 4 exit (Edison fix #9)
- **Fix title:** "Fast Learning AI for Materials Engineering" → **"FLAIME: Fast Learning AI for Mineral Efficiency — Autonomous Discovery of Critical-Mineral-Lean Alloys for Advanced Manufacturing"** (Edison fix #10: PI-confirmed Topic 3B backronym, shortened)

### DOE Title Page
- **Sources:** `budget-breakdown-phase1.md`, `team-skill-chart.md`, partnership structure
- **Action:** Fill Senior/Key Personnel table, update budget to $750K, correct Focus Area field to **Topic 3B** (not 12-F — Edison fix #1 flagged stale reference)
- **Partnership table:** BYU (Lead, PI: Baird), Valimet (GA), AMAZEMET (UA), Thermo-Calc (CALPHAD)
- **2-of-3 team composition:** Explicitly confirm FOA §II.E compliance — BYU (IHE, category 3) + Valimet (Industry, category 2). Ames National Lab letter of support provides DOE Lab connection (category 1) though not as formal team member. (Edison fix #5)
- **Merit Reviewer Conflicts (Field 12):** Add to checklist — currently omitted from plan (Edison fix #1)

---

## Phase 2: Project Narrative (5 pages)

### §0 — Project Overview (opening paragraph, ~80 words)
- **Rationale:** Per PI feedback, the first page should lead with a brief project overview/executive summary before diving into background. Common in DOE proposals — gives merit reviewers the "elevator pitch" immediately.
- **Draft content (R4-revised, ~85 words — opens with the problem, not the acronym):**
  > The U.S. depends on foreign sources for 100% of its manganese and the majority of its chromium and zirconium — elements central to high-performance aluminum alloys for advanced manufacturing. FLAIME (Fast Learning AI for Mineral Efficiency) is an autonomous closed-loop platform that discovers aluminum alloys meeting structural performance targets while minimizing critical mineral content. By integrating AI-guided optimization with a complete powder-to-print-to-test manufacturing pipeline — the first to unify computational evaluation, powder atomization, laser powder bed fusion, and mechanical testing in one loop — FLAIME targets ≥3× acceleration over conventional approaches.
- **Placement:** Immediately after the Buy America statement (which FOA requires in first 2 pages), before §1 body text
- **NOT a separate section header** — just an opening paragraph within §1 Background

### §1 — Background and Introduction (~300 words — trimmed per R10 H1 rebalance)
- **Sources:** `edison-3b-deepdive-synthesis.md`, `literature-search-synthesis.md`, `genesis-mission-gotchas.md`, `materials_criticality_databases.md`, `bios/baird-CV.pdf`, `pareto-am-al-alloys/downstream_applications.md`, `pareto-am-al-alloys/pareto_front_analysis.md`
- **Content (prioritized per R9 H1 — explicit word budgets):**
  - **MUST-HAVE (~200w):**
    1. Critical minerals challenge: Mn 100% import-reliant, Cr/Zr on USGS list → AMMTO alignment
    2. **[R14] Lead with urgency, not just statistics:** After import-reliance stat, add consequence: "A single supply disruption could idle U.S. additive manufacturing production dependent on these elements"
    3. **Quantified impact numbers** (Edison fix #7): 347,000 kg Be/year in alloys (84% from one mine); ~$250-400M/yr Be-Cu market; ~6,245 tonnes Mg displacement potential; CMI Hub precedent >$80M follow-on
    4. **DOE CMS pillar language** (Edison fix #7): Explicitly reference DOE Critical Materials Strategy pillars — Pillar 2 (Develop Alternatives), Pillar 3 (Materials & Manufacturing Efficiency), Pillar 5 (Enabling Activities)
    5. Gap: no existing SDL integrates powder → LPBF → tensile in closed loop (strongest differentiator)
    6. **[PR #51 insight]** All confirmed AM Al alloy deployments (AlSi10Mg satellites, Scalmalloy >100 telecom parts in orbit, AL250C engine) use LPBF — no DED/WAAM deployments found in literature. This validates FLAIME's LPBF + ultrasonic atomizer focus as the qualification-relevant pathway (see `pareto-am-al-alloys/downstream_applications.md`)
  - **HIGH (~100w):**
    6. FLAIME's contribution: BOFN-guided autonomous platform with mineral-burden objective
    7. **[R14] Sharpen competitive landscape** with single contrast: "Existing platforms either stop at powder synthesis (A-Lab) or optimize process parameters without closing the composition loop (ORNL Peregrine) — FLAIME is the first to unify composition discovery with full manufacturing qualification"
    8. **[R14] "Why now" signal** (~15w): "Recent advances in cost-aware BO and multi-stage function networks make autonomous powder-to-property optimization tractable for the first time"
  - **MEDIUM (~50w, trim if space-constrained):**
    7. **[D4] PI as human-in-the-loop SDL leader** (1-2 sentences only; detailed credentials in §3 and biosketch): Reference frugal twin review paper and SDL review paper (structural materials lead author). Also cite Fehrmann Materials GmbH prior contract ($34K for ML representations of Al alloys) as domain-adjacent evidence.
  - **MOVED to §2** (R9 fix M4): D3 broader Genesis Mission applicability content — detailed nuclear/quantum examples belong in Phase II vision, not Background. Keep only a brief forward reference in §1: "The FLAIME architecture generalizes beyond Al alloys to other Genesis Mission priorities (§2)."
- **Figure:** Reference Fig. 2 (CALPHAD evaluation + SEM/EDS experimental evidence) — shows both computational and physical execution readiness
- **Buy America:** Keep existing compliance statement

### §2 — Project Objectives (~250 words, ~0.5 page — expanded per R10 H1: steal from §6 and §1)
- **Sources:** `ai-advantage-statement.md`, `project-metrics-v4-edison-refined.md`
- **Content:** 3–5 quantitative objectives:
  - O1: Demonstrate closed-loop BOFN/pKGFN platform for autonomous alloy exploration
  - O2: Screen ≥22,803 element combinations ($k=2$–$8$ from 15-element palette) and 100–200 compositions within selected sub-systems via CALPHAD + mineral-burden objective
  - O3: Validate 100–200 compositions experimentally through the MVS pipeline (based on throughput of up to 2 unique compositions/day, 6 days/week over 9 months; ~468 theoretical max, ≥200 accounts for ramp-up and pipeline failures)
  - O4: Achieve discovery yield ≥3% (PI-confirmed target — **clarification per R9 H3:** this is the *overall* discovery yield across all screened compositions, i.e., compositions meeting all target properties / total compositions screened. The metrics doc's ≥20% figure refers to Tier 1 "Full Pass" among only the *fully tested* compositions. Both metrics are valid and can coexist: report 3% overall yield AND 20% Tier 1 pass rate as complementary KPIs.)
  - O5: Demonstrate AI acceleration factor ≥3× vs. random baseline (conservative, defensible)
  - **TRL advancement** (R2 fix: project-specific definitions): TRL 2 (concept formulated: BOFN DAG + CALPHAD pipeline designed) → TRL 4 in Phase I (closed-loop validated on real Al alloys in lab) → TRL 6 in Phase II (system demonstrated in relevant environment with industry-scale powders)
- **Commercialization content (prioritized per R11 — explicit tiers for 250w budget):**
  - **MUST-HAVE (~70w):** 5 quantitative objectives (O1-O5) as numbered list — **[R14] front-load immediately after section header for scanning reviewers**
  - **MUST-HAVE (~30w):** TRL 2→4→6 advancement path
  - **MUST-HAVE (~15w, R14 new):** **Scope statement:** "Phase I focuses exclusively on Al alloys processed by LPBF, with Cu-Cr-Zr as a stretch demonstration"
  - **HIGH (~40w):** Market sizing ($250-400M/yr Be-Cu) + industry pathway (Valimet → Fehrmann)
  - **HIGH (~25w):** **[D6] IP strategy** compressed: "FLAIME platform open-source; Month-6 internal review to assess selective IP for top compositions"
  - **HIGH (~15w, R14 new):** **Integrating sentence** after O1-O5 list: "Collectively, these objectives demonstrate that BOFN-guided autonomous experimentation can simultaneously accelerate alloy discovery AND reduce critical mineral dependence — the dual mandate of Topic 3B"
  - **MEDIUM (~25w):** **[D3] Phase II vision** — **[R14] ONE vivid example:** "Phase II will extend FLAIME to AMMTO priority alloys (e.g., 316H for nuclear structural applications)"
  - **MEDIUM (~20w):** Technology transfer sentence
  - **LOW (~30w):** TRL definitions (can move to appendix if space-constrained)
  - **Total: ~245w — fits within 250w budget**

  **Full D6 IP strategy rationale (for writer reference, compress to ~25w in narrative):**
  The FLAIME software platform (BOFN/pKGFN workflow engine, Honegumi tutorial framework) will be released fully open-source to maximize adoption and community contribution. This mirrors the PI's track record of high-impact open data (MPTS-52 dataset heavily reused in crystal structure generative AI, Zenodo/Figshare contributions). **For alloy compositions:** The default path is fully open data publication (consistent with PI's open-science values and FAIR principles), but the plan includes a deliberate **internal team evaluation at Month 6** (concurrent with but separate from the DOE programmatic review — R9 fix M2) to assess whether selective IP protection of the highest-performing compositions would better serve commercialization via Valimet/Fehrmann pathway. The PI notes that fully open data has historically produced the greatest downstream impact (citation count, industry adoption) and is the preferred path.

  **Full D3 Phase II vision (for writer reference, compress to ~30w in narrative):**
  FLAIME's modular BOFN + closed-loop architecture generalizes beyond Al alloys to other Genesis Mission priorities: (a) nuclear structural materials (Topic 1: radiation-tolerant steels, BOFN optimizing creep + corrosion + irradiation simultaneously); (b) quantum materials (Topic 2: superconducting compounds with multi-fidelity CALPHAD + experimental loops); (c) any multi-stage manufacturing workflow where pKGFN partial evaluations reduce cost. Ties to **CMS Pillar 5 (Enabling Activities)** — FLAIME as reusable AI infrastructure for the entire Genesis Mission ecosystem. Phase II could target AMMTO priority materials (316H, IN718) or pivot to nuclear/quantum domains.
- Technology transfer sentence addressing AMMTO commercialization criterion

### §3 — Proposed Research and Methods (~400 words, ~1.5 pages)
- **Sources:** `calphad_alloy_design.md`, `bofn-edison-review1/2.md`, `am-scaleup-test-structures.md`, `alloy-workflow-review.md`, `high-throughput-calphad.md`, `preliminary-results-roadmap.md`, `bios/baird-CV.pdf`
- **Content:** 3 activity blocks with PI/budget attribution:
  - **Activity 1: AI-Guided Computational Exploration** — BOFN DAG over CALPHAD nodes, pKGFN acquisition function, mineral-burden multi-objective. HPC parallelization on BYU cluster. **Two-level hierarchical search with asynchronous multi-fidelity CALPHAD evaluation:** Level 1 explores all C(15,k) for k=2..8 = 22,803 sub-systems from a 15-element Al-alloy palette (Al + Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn). Fidelity 1 (pycalphad, $0): coarse Sobol/LHS evaluation (~50 comps/sub-system, ~1.13M evals, <1 hour on HPC). Fidelity 2 (TC-Python/TCAl10): Scheil with back-diffusion, TC-PRISMA precipitation kinetics for targeted sub-systems. Fidelity 3 (AM Module): printability maps, melt-pool geometry, G/R + CET, Scheil with solute trapping for selected compositions. All fidelities run at max HPC parallelism; data feeds unified surrogate continuously; pKGFN decides next expensive evaluation. Level 2 optimizes compositions within top 3–6 sub-systems through full experimental pipeline. Al-Mn-Cr-Zr and Al-Zr are guaranteed "anchor" systems. *Responsibility: PI (BYU).*
  - **Activity 2: Experimental Validation Pipeline** — Ultrasonic atomization (AMAZEMET at BYU) + gas atomization (Valimet subaward), LPBF printing (partner access), MVS progression (single tracks → density cubes → tensile bars per Fig. 3d). *Responsibility: PI + partners.*
  - **Activity 3: Closed-Loop Integration, Dissemination & Qualification** — Autonomous campaign orchestration, pKGFN-driven experiment selection, ISO 52902 benchmark geometry, digital thread assembly. *Responsibility: PI.*
    - **[D1] Scalable deployment and standardization:** The PI has a demonstrated track record of deploying SDL solutions at scale through reusable software, tutorials, and training materials. Key standardization involvements: POSE (Pathways to Open Source Ecosystems), Acceleration Consortium community standards, FAIR data practices, GCMAC (Global Committee on Materials and Advanced Ceramics), and multiple other national/international standards efforts. These ensure FLAIME outputs are not isolated prototypes but production-ready, community-adopted tools.
    - **[D2] Honegumi + BoTorch integration:** New BOFN/pKGFN tutorials will be integrated into the Honegumi platform (PI's open-source tutorial framework for Bayesian optimization in materials science). Source code contributions targeted for Meta's BoTorch tutorials (noting a letter of support from Meta). This ensures FLAIME's AI methods are immediately accessible to the broader materials science community and have institutional backing from a major AI research organization.
    - **[D5] Workflow orchestration expertise:** The PI brings unique workflow orchestration leadership developed at the Acceleration Consortium, where he designed and deployed multi-step materials discovery workflows. This expertise directly maps to FLAIME's 4-stage pipeline (CALPHAD → atomization → LPBF → testing), ensuring robust autonomous campaign management.
- **Project management paragraph** (Edison fix #3, expanded to ~75-100 words per R2): Weekly PI-partner sync calls, monthly all-hands reviews, shared FAIR-compliant database with version control, PI retains final decision authority on go/no-go gates. Data-sharing via Genesis Mission AmSC platform. **UG supervision model** (R2 fix): shift-based lab roles with PI/MS oversight, each UG assigned specific pipeline stage. **Conflict resolution**: PI escalation for technical disagreements; partner disputes resolved via monthly all-hands.
- **UG team throughput framing** (R3 improvement #7): Frame 10 UGs as throughput ADVANTAGE — shift-based model enables 6-day/week operation → ≥8 compositions/month → statistically meaningful BOFN benchmarking within 9-month Phase I. This is a feature, not a limitation: high UG count provides personnel depth for parallel experimental streams (atomization, characterization, tensile testing).
- **Risk mitigation** (Edison fix #8, 2-3 sentences):
  - If atomization yield is low → fallback to Valimet gas atomization (subaward)
  - If BOFN advantage is modest → honest reporting via time-ledger decomposition showing total platform acceleration
  - Tiered evaluation: ~50 full tensile + ~150 hardness/density only to manage throughput risk
  - **LPBF access contingency** (R2 fix #3): If U of Utah LPBF access is disrupted, 3D Powder Tech (letter of support) provides backup printing capacity
- **Figures:** Reference Fig. 1 (pKGFN pipeline + convergence) and Fig. 3 (4-panel composite with multi-fidelity pipeline/throughput/defects/MVS)
- **Preliminary results** woven in: pKGFN implementation verified on manufacturing benchmark (convergence plot), Thermo-Calc simulations running on BYU HPC, SEM/EDS of atomized powders confirming composition control (shown in Fig. 2), AlSi10Mg tensile baseline from U Utah
- "Relationship to Prior Work" paragraph

### §4 — Milestones in the Nine Months (~350 words + table, ~1 page)
- **Sources:** `project-metrics-v4-edison-refined.md`, `preliminary-results-roadmap.md`
- **Content:** Replace placeholder milestone table:
  - M1 (Mo 1): BOFN DAG + multi-fidelity CALPHAD evaluation pipeline operational; Level 1 element-combination assessment (22,803 sub-systems) complete; Al-Mn-Cr-Zr and Al-Zr anchor compositions selected for experimental validation
  - M2 (Mo 2): First atomized powder batches characterized (PSD, SEM/EDS, flow)
  - M3/G1 (Mo 3): **Go/No-Go G1** — ≥50 compositions screened, surrogate RMSE < threshold
  - M4/G2 (Mo 5): **Go/No-Go G2** — Closed-loop cycle demonstrated end-to-end
  - M5/G3 (Mo 7): **Go/No-Go G3** — ≥1 alloy meeting YS≥250 MPa, EL≥5% (or ≥1 AI-discovered sub-system alloy meeting equivalent thresholds)
  - M6 (Mo 9): Final deliverables: digital thread, Phase II readiness assessment
- **Table 1:** KPI/go-no-go dashboard with 5 KPIs, thresholds, measurement methods, triggered optimizer actions
- Brief narrative framing 6-month DOE review point

### §5 — Data Sources and Models (~130 words, ~0.5 page)
- **Sources:** `alloy-databases.md`, `thermocalc-discussion-transcript.md`, `high-throughput-calphad.md`
- **Content:**
  1. Data sources: Thermo-Calc TCAl10/TCMG6 databases, Materials Project, MMPDS
  2. Team access: BYU HPC Thermo-Calc license, TC collaboration letter, API access
  3. AI models/frameworks: BoTorch/BOFN, pKGFN acquisition, GPyTorch surrogates
  4. **Genesis Mission platform integration** (Edison fix #6, strengthened + R2 bidirectional fix): FLAIME will host its digital thread, alloy database, and BOFN/pKGFN models on the American Science Cloud (AmSC); team will participate in Genesis Mission coordination activities; BOFN/pKGFN released as domain-specific "plug-and-play" capability per GM framework. **Bidirectional**: FLAIME will leverage other GM teams' validated data (e.g., shared characterization databases, benchmark alloy property sets) to accelerate CALPHAD surrogate training.
  5. **[D7] Open data and software dissemination:** All experimental data (compositions, processing parameters, properties) will be published on Zenodo and Figshare with DOIs for long-term accessibility and citation tracking. The PI has a strong track record: the MPTS-52 dataset (PI contribution) has been heavily reused by the crystal structure generative AI community, demonstrating that open materials data generates outsized downstream impact. BOFN/pKGFN code released as open-source Python packages with Honegumi tutorials. Software contributions targeted for Meta's BoTorch tutorial ecosystem (letter of support from Meta).
- **No computing resources here** (FOA: goes in Appendix 2)

### §6 — Decision Gate Metrics (~180 words — trimmed per R10 H1 rebalance, ~0.4 page)
- **Sources:** `project-metrics-v4-edison-refined.md`, `ai-advantage-statement.md`, `edison-kpi1-discovery_yield-review.md` through `kpi6`
- **Content:** 3 quantitative Phase I go/no-go metrics:
  1. **AI Acceleration Factor** (AF = n_baseline / n_BOFN): target ≥3× vs. random baseline (conservative). **Baseline structure (R3 fix #10):** 4 baselines (B1=random, B2=expert DOE, B3=standard BO, B4=BOFN−mineral ablation) + BOFN as method under test. AF computed against each baseline independently.
  2. **Discovery Yield** (compositions meeting targets / total screened): target ≥3% (PI-confirmed)
  3. **Mineral-Burden Reduction** (critical mineral wt% vs. incumbent alloy): target ≥40% reduction
- Scaling behavior statement: performance improves as CALPHAD database and experimental data grow
- **AI Tool Disclosure** statement (FOA requirement)

---

## Phase 3: Appendices

### Appendix 1 — Bibliography & References Cited
- **Required citations** (from template `\instruct`): Abolhasani & Kumacheva 2023 (Nat. Synth.), Stach et al. 2021 (Matter), Hart et al. 2021 (Nat. Rev. Mater., BYU co-author), Astudillo & Frazier 2019 (ICML/BOFN), Khatamsaz et al. 2023 (npj Comput. Mater.), AMMT Roadmap 2025 (DOE AMMTO), Liang et al. 2025 (Sci. Adv.)
- **Additional:** Bukkapatnam 2023 (AMDM framework), Chawla et al. 2025 (cost-aware BO), Alvi et al. 2026 (npj), ISO 52902, ASTM E8/E8M, ISO 52907
- ~15–20 total references

### Appendix 2 — Facilities & Other Resources (≤0.5 page)
- BYU lab: AMAZEMET ultrasonic atomizer (installed, operational), SEM/EDS/EBSD suite, universal testing machine (ASTM E8)
- Partner LPBF: U Utah (Prof.\ Ashley Spear's lab), 3D Powder Tech
- Computing: BYU HPC cluster, Thermo-Calc licenses (TC-Python)
- **Appendix figure:** Atomizer installation photo if available

### Appendix 3 — Equipment (≤0.5 page)
- Already partially populated; update with AMAZEMET atomizer specs, BYU characterization equipment

### Appendix 4 — DMSP (planning placeholder per FOA)

### Appendix 5 — Synergistic Activities (≤5 per person, ≤1 page)

**Activity 1: SDL Leadership & Community Building** — npj Computational Materials Guest Editor for "Self-driving Labs for Chemistry and Materials Science" collection (2024-present); Chemical Reviews SDL review lead author (structural materials section); Frugal Twin review lead author (Lo et al. 2024); AC BO Hackathon solo organizer (120 participants, 62 orgs, 14 countries); MRS Fall 2025 presentation on "Autonomous Vertical Cloud Lab for Additively Manufactured Aerospace Alloys."

**Activity 2: Open-Source Software & Community Infrastructure** — 17,000+ open-source code contributions (15K commits, 1.5K issues, 913 PRs); Honegumi tutorial framework (JOSS 2025); Meta BoTorch Technical Consultant (Nov 2024–Jan 2025, letter of support); xtal2png (JOSS 2022); 350+ SDL kits deployed worldwide.

**Activity 3: Training & Workforce Development** — ~5,000 person-hours of SDL training to ~700 individuals across ~62 organizations; built AC Dev Lab from scratch ($600K, 500 line items, 24 months); 200+ hours course content; supervised 12 staff + 8 students.

**Activity 4: Standardization & Open Science** — POSE (Pathways to Open Source Ecosystems) PI for materials informatics toolchain; Acceleration Consortium community standards contributor (data schema, experiment specification formats); FAIR data practices: developed schema.org metadata templates for SDL datasets; GCMAC presenter (2024, 2025); NSF TIP Directorate Review Panelist (2026); international standards engagement through IEC/ISO materials data working groups.

**Activity 5: Open Data Impact & Domain Expertise** — MPTS-52 dataset heavily reused by crystal structure generative AI community; Matbench-genmetrics benchmarking framework (JOSS 2024); Fehrmann Materials GmbH contract ($34K, ML for Al alloys); Zenodo/Figshare deposits with documented reuse metrics.

### Appendix 6 — Foreign Connections
- AMAZEMET (Białystok, Poland) — ultrasonic atomizer supplier/collaborator
- Thermo-Calc (Stockholm, Sweden) — CALPHAD software collaborator

### Appendix 7 — Other Attachments
- Letters of Collaboration (strict 2-sentence FOA format):
  - Valimet (gas atomization services)
  - AMAZEMET (ultrasonic atomization technology)
  - Thermo-Calc (CALPHAD/AM Module software + support)
- Letters of Support: Ames National Lab, Fehrmann Alloys, Taylor Sparks, Ashley Spear, Adam Clare, Chris Stiles, Jae Hattrick-Simpers, Keith Brown

---

## Phase 4: Budget & Forms

- Update illustrative budget table to $750K scenario from `budget-breakdown-phase1.md`
- **Personnel (PI-confirmed):** PI + 2 MS + 10 UGs @ $30/hr
- **Funded Partners:** Valimet (gas atomization) and AMAZEMET (ultrasonic atomization equipment) submit independent applications. Thermo-Calc AB is an unfunded collaborator.
- **Budget mechanism (PI-confirmed 2026-04-14):** Valimet and AMAZEMET are funded partners submitting independent applications.  Thermo-Calc AB is an unfunded collaborator (CALPHAD database access via existing BYU license).
- Partner budgets: [per-partner amounts removed from the public copy]
- **[D8] Biographical sketch — SciENcv format:** Use the SciENcv (Science Experts Network Curriculum Vitae) format as required/preferred by DOE. Source: `bios/baird-CV.pdf`. Key PI differentiators to highlight:
  - **[D1] SDL deployment at scale:** Track record of reusable software (Honegumi, ac-bo-hackathon, multiple open-source packages), tutorials, training programs. Standardization leadership: POSE (Pathways to Open Source Ecosystems), Acceleration Consortium standards, FAIR data practices, GCMAC.
  - **[D4] Human-in-the-loop SDL leader:** Frugal twin review paper (resource-efficient autonomous experimentation). Lead author on structural materials section of comprehensive SDL review paper.
  - **[D5] Workflow orchestration at AC:** Designed and deployed multi-step materials discovery workflows at the Acceleration Consortium. **[R9 M6]** Built $600K Dev Lab from scratch, 500 equipment items deployed in 24 months — concrete execution credibility for FLAIME's pipeline build.
  - **[D7] Open data impact:** Zenodo/Figshare contributions. MPTS-52 dataset heavily reused in crystal structure generative AI. High citation/reuse evidence.
  - **[R9 M5] Domain-adjacent expertise:** Fehrmann Materials GmbH prior contract ($34K for ML representations of Al alloys) — demonstrates PI has paid industry work in the specific alloy domain, partially addressing the LPBF/CALPHAD publication gap.
  - **[R9 M7] Quantified community impact:** ~5,000 person-hours of SDL training delivered to ~700 individuals across ~62 organizations; 350+ SDL kits deployed; BO Hackathon at scale.
  - SDL publications record, BO/materials informatics expertise, ac-bo-hackathon community building
  - **[R12 M4] Additional CV highlights:** (a) *npj Computational Materials* Guest Editor for "Self-driving Labs for Chemistry and Materials Science" collection (2024-present) — editorial leadership in exact field, add to Synergistic Activities; (b) NSF TIP Directorate Review Panelist (2026) — shows PI trusted to evaluate tech innovation proposals, relevant to AMMTO; (c) 17,000+ open-source code contributions (15K commits, 1.5K issues, 913 PRs) — quantitative signal for D1
  - Other notable: Abolhasani et al. 2026 "Call to Action" co-author; Sayeed et al. 2025 "Honegumi RAG Assistant"; Pelkie et al. 2025 "Democratizing self-driving labs"
- Update Current & Pending placeholder

---

## Phase 5: Cleanup

- Remove all `\lipsum` package usage and `\usepackage{lipsum}` import
- Verify all `\instruct{}`, `\guidance{}`, `\required{}`, `\note{}` annotations addressed
- Keep `\todo` annotations active (`make clean-pdf` generates submission PDF without notes)
- Verify narrative page count ≤5 after all figures/tables
- Compile LaTeX to check cross-references and page count
- Update all figure paths and `\includegraphics` references
- **Update Focus Area** from "12-F" to "Topic 3B" in all locations (Edison fix #1), including `proposal-checklist.md` §A.3 (R2 fix #5)
- **Verify title consistency** across all documents (Edison fix #10)
- **Strengthen 6-month DOE review** language in §4: "M3-M5 are structured to demonstrate sufficient progress for the Month 6 DOE programmatic review" (R2 fix #9)

---

## Edison Round 1 Feedback Integration Log

Edison ANALYSIS task `56165379` returned overall grade **B** with 10 improvements.
All 10 items addressed in v3:

| #   | Edison Improvement                                  | Priority    | How Addressed in v3                                                                                                 |
| --- | --------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------- |
| 1   | Resolve figure strategy conflict (plan vs. roadmap) | CRITICAL    | Realigned Fig. 1-3 to lead with pKGFN pipeline, add SEM/EDS experimental evidence, move 4-panel composite to Fig. 3 |
| 2   | Add commercialization content for Criterion 4       | HIGH        | Expanded §2 Objectives with market sizing, industry pathway, IP strategy, Phase II targeting                        |
| 3   | Add team management narrative to §3                 | HIGH        | Added project management paragraph with communication cadence, data-sharing, decision authority                     |
| 4   | Resolve personnel/budget/yield inconsistencies      | HIGH        | Flagged 4 reconciliation items with ⚠️ for PI resolution                                                             |
| 5   | Verify 2-of-3 team composition                      | HIGH        | Added explicit §II.E compliance statement with category assignments                                                 |
| 6   | Strengthen Genesis Mission platform integration     | MEDIUM-HIGH | Expanded §5 with AmSC hosting, coordination participation, plug-and-play release                                    |
| 7   | Incorporate quantified impact numbers               | MEDIUM-HIGH | Added to §1: Be market, Mg displacement, CMI Hub precedent, CMS pillar language, competitive landscape table        |
| 8   | Add risk mitigation to §3                           | MEDIUM      | Added 3 risk/fallback pairs: atomization yield, BOFN advantage, screening throughput                                |
| 9   | Add TRL advancement path                            | MEDIUM      | Added TRL 2→4→6 in §0 abstract and §2 objectives                                                                    |
| 10  | Update and align project title                      | MEDIUM      | Updated to full Topic 3B-aligned title in §0, noted consistency check in cleanup                                    |

## Key Differences from v2 Plan

1. **Figure strategy resolved** (Edison CRITICAL): pKGFN pipeline leads as Fig. 1, SEM/EDS experimental evidence in Fig. 2, 4-panel composite as Fig. 3 — aligns with preliminary-results-roadmap.md triage
2. **Experimental evidence in narrative**: SEM/EDS images now in Fig. 2 right panels — AMMTO reviewers need physical execution readiness, not just schematics
3. **Commercialization expanded**: From 1 sentence → 4 bullet points in §2 covering market sizing, industry pathway, IP strategy, Phase II targeting
4. **Team management added**: Project management paragraph in §3 with communication cadence and decision authority
5. **Risk mitigation added**: 3 explicit risk/fallback pairs in §3
6. **TRL path added**: TRL 2→4 in Phase I, TRL 6 in Phase II
7. **Genesis Mission integration strengthened**: Specific AmSC hosting + plug-and-play release language in §5
8. **Quantified impact numbers**: Concrete market/supply risk data in §1
9. **DOE CMS pillar language**: Explicit Pillar 2, 3, 5 references in §1
10. **4 reconciliation items flagged**: Personnel, subawards, discovery yield, title — marked ⚠️ for PI resolution

---

## Edison Review Log

| Round         | Task ID    | Grade           | Key Issues                                                                                                                                                                                                                                                                                                                           |
| ------------- | ---------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1             | `56165379` | **B**           | Figure conflict (CRITICAL), commercialization thin (C grade), personnel inconsistency, no experimental evidence in figures                                                                                                                                                                                                           |
| 2             | `117ddacb` | **A-**          | All 10 R1 fixes verified ✅. Residual: Fig 3 discrepancy, management paragraph thin, LPBF contingency, TRL definitions, checklist stale ref                                                                                                                                                                                           |
| 3             | `cdd6315c` | **A-**          | 55 files reviewed. Backronym still "Materials Engineering" in template (CRITICAL, fixed), figure budget tight at 4 figs + table (~1.6-2.0 pages), UG team not framed as advantage, word count targets need revision                                                                                                                  |
| 4             | `29c70a55` | **A-**          | 68 files reviewed. Template budget/personnel mismatch (CRITICAL, fixed), checklist 12-F refs (CRITICAL, fixed), Phase II budget in template (fixed), word count targets too high (revised to ~1,600w), overview paragraph weak hook (revised to lead with problem)                                                                   |
| 5             | `b081159c` | **A-** (strong) | 71 files reviewed. 0 critical blockers, execution-ready. 5 HIGH items remain                                                                                                                                                                                                                                                         |
| 6 (checklist) | `82f705e4` | **A-**          | 12 files. Checklist restructure verified. Added FLAIME params, CMS pillars, scaling behavior                                                                                                                                                                                                                                         |
| 7 (checklist) | `86ea48bd` | **A**           | 13 files. All R6 HIGH items verified. Added guardrails, targets, benchmark                                                                                                                                                                                                                                                           |
| 8 (checklist) | `64c177d2` | **A**           | 9 files. Confirmed: 225 checkboxes, 0 factual errors, 0 stale references                                                                                                                                                                                                                                                             |
| 9             | `263d7170` | **A**           | 60 files. 8/8 directives integrated. 3 HIGH: §1 word budget overload (fixed: added priority tiers), template stale content (tracked), discovery yield discrepancy (fixed: clarified 3% overall vs 20% Tier 1). 7 MEDIUM fixes applied (M2 IP phrasing, M4 D3 move to §2, M5 Fehrmann contract, M6 AC Dev Lab, M7 community metrics). |
| 10            | `79439b3c` | **A**           | 61 files. R9 fixes 9/10 verified ✅. 2 NEW HIGH: §2 word budget overload (fixed: rebalanced §1→300w, §2→250w, §6→180w), Ce feedstock in budget doc (fixed: replaced with Zr/Mn/Cr). R10 also fixed: budget doc "Industry Subawards" header → "Industry Partner Costs" with type column. Phase II budget verified correct per FAQ.     |
| 11            | `064ddff5` | **A**           | 61 files. R10 fixes 3/3 verified with residuals. 5 HIGH cross-doc propagation: §2 priority tiers (fixed), Ce relic L140 (fixed), budget L34 phrasing (fixed), template word count conflict (tracked), template partner placeholders (tracked). Path to A+ defined.                                                                   |
| 12            | *pending*  | —               | Plan v5.3 with R11 fixes + §2 priority tiers                                                                                                                                                                                                                                                                                         |

### R4 Improvements Incorporated (v4.2)
1. ✅ Fixed template budget table: PI + 2 MS + 10 UGs at $393K, Valimet subaward (CRITICAL; later updated: 2 MS + 10 UGs per PI directive, then Valimet/AMAZEMET as funded partners)
2. ✅ Fixed checklist 12-F → 3-B reference (CRITICAL)
3. ✅ Updated template personnel guidance note
4. ✅ Updated template figure/table strategy guidance (4 figures + contingency)
5. ✅ Revised word-count targets from ~1,880w → ~1,600w (R4 analysis: 4 figs leaves only 3.0-3.2 text pages)
6. ✅ Revised overview paragraph to lead with national problem, not acronym definition (~85 words)
7. ✅ Updated figure inventory: SEM/EDS and tensile data marked as "✅ Data in hand"
8. ✅ Phase II budget reference verified (guidance note retained as FOA-sourced)
