> **⚠️ Archived/Raw Output (Pre-Pivot):** This file is a raw Edison Scientific output generated before the Topic 3B pivot. It was originally framed for "Topic 12 Focus Area F" and assumes a 25–30 page proposal. The current roadmap targets **Topic 3B (Critical Minerals — AI-Enabled Materials Discovery, AMMTO)** with a **5-page Project Narrative** limit. Treat this as a historical input artifact, not current guidance. See `preliminary-results-roadmap.md` for the current synthesized roadmap.

Question: You are acting as a panel of DOE program managers and expert reviewers evaluating a Phase I proposal for the DOE Genesis Mission (DE-FOA-0003612), Topic 12 Focus Area F (AI-Enabled Materials Discovery, Development, and Qualification under AMMTO).

The project is FLAIME: an autonomous closed-loop platform for AI-guided alloy discovery via LPBF (laser powder bed fusion). The pipeline: CALPHAD screening → gas atomization → LPBF printing → characterization → Bayesian optimization (BOFN = Bayesian Optimization with Function Networks). The PI is early-career at BYU.

EXISTING PRELIMINARY WORK (already completed):
1. BOFN 4-node and 9-node function network implementations verified in BoTorch (cost-aware, 88% cost savings vs naive, MAE≈0.003)
2. LLM-warmstart POC for Bayesian optimization (LLAMBO-style, Al-Si-Mg compositions)
3. LPBF parameter space dimensionality mapped (130+ parameters identified, 36 critical)
4. AM test structure validation progression documented (8-stage, A-grade figure)
5. 5 headline KPIs + 8 go/no-go gates + 18 condensed metrics defined
6. LaTeX proposal template with DOE-compliant formatting
7. Budget modeled ($600K-$750K, 2 scenarios)
8. Topic fit analysis (12-F primary, 11C comparison)
9. Multiple Edison-refined figures (parameter space 8/10, test structures A-grade)

THE DEADLINE IS APRIL 28, 2026 (as of 2026-04-09, 19 days remained).

Please provide a detailed assessment structured as follows:

**Section A: Mock Program Officer (AMMTO) Feedback**
- What 5 preliminary results would most strengthen this proposal?
- Rate each by impact (1-10) and feasibility in 19 days (1-10)
- What specific figures and figure captions would be most compelling?
- What narrative sections would benefit most from additional preliminary data?

**Section B: Mock Enthusiastic Reviewer**
- What results would push this from "good" to "must-fund"?
- Which existing results are strongest? Which are weakest?

**Section C: Mock Skeptical Reviewer**
- What are the biggest gaps in preliminary results?
- What would you need to see to believe the BOFN approach works for real alloys (not just synthetic data)?
- What concerns about feasibility of the 19-day timeline?

**Section D: Mock Moderate Reviewer**
- Prioritized list of 8-10 preliminary results, ranked by proposal impact
- For each: what would the figure look like? What would the caption say? Where in the proposal does it go?

**Section E: Synthesis and Action Plan**
- Top 5 "must-have" results (core, achievable in 19 days)
- Top 3 "stretch" results (high impact but time-risky)
- Specific figure specifications (size, content, caption draft) for each must-have
- How each result maps to proposal sections (Background, Preliminary Results, Technical Approach, etc.)

Focus on what would actually appear in the proposal document: figures, tables, narrative text supporting those figures, and how they demonstrate feasibility.

## Evidence-grounded framing (for proposal narrative)
Autonomous materials discovery/manufacturing is commonly framed as a cyberphysical system with an “intelligent software brain” coupled to a “hardware body” of synthesis/manufacturing and measurement equipment; the need is driven by iterative, expensive experiments in high-dimensional design spaces, making closed-loop decision-making central to accelerating discovery and qualification (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3). Reviews also highlight that many systems remain semi-automatic and that increasing process complexity/cost motivates stronger sequential experimentation and acquisition strategies that consider resources (bukkapatnam2023autonomousmaterialsdiscovery pages 10-11). In real experimental workflows, cost-aware Bayesian optimization has been demonstrated to materially improve throughput by explicitly modeling instrument/experiment costs and forming a closed loop between surrogate modeling and automated experimentation (chawla2025acceleratedmaterialsdiscovery pages 1-4, chawla2025acceleratedmaterialsdiscovery pages 21-24). Peer-reviewed work in complex materials design campaigns similarly argues for cost-aware BO that balances inexpensive computational queries (e.g., CALPHAD/low-fidelity surrogates) against expensive experiments to reduce total discovery cost/time (alvi2026deepgaussianprocessbased pages 2-4, alvi2026deepgaussianprocessbased pages 1-2).

## Proposal-strengthening artifacts (for direct insertion)

| Rank | Preliminary result to generate in 19 days | Why it matters to AMMTO/Genesis | Impact score (1-10) | Feasibility in 19 days (1-10) | What the figure/table would look like (1 sentence) | Where it goes in the proposal (section/subsection) | Key risk it retires |
|---|---|---|---:|---:|---|---|---|
| 1 | End-to-end closed-loop digital demonstration on a realistic alloy/LPBF surrogate: CALPHAD-informed candidate set → BOFN selects next experiments under cost constraints → simulated characterization feedback → convergence to target printability/property region | Most directly shows the core Phase I claim: autonomous decision-making across the full FLAIME workflow rather than isolated model components; aligns with AMMTO emphasis on accelerated qualification and reduced experimental burden | 10 | 8 | A pipeline schematic annotated with numbered steps and a convergence plot showing BOFN reaching the target frontier with fewer experiments than random/EI baselines | Preliminary Results; Technical Approach - Closed-Loop Learning Architecture | Integration risk that the pieces do not function as one coherent autonomous loop |
| 2 | Retrospective BOFN benchmark using literature or prior Al-Si-Mg/alloy-process datasets with multi-fidelity and multi-objective targets (e.g., density, crack tendency, hardness) | Demonstrates that BOFN is relevant to real alloy/process data, not only synthetic functions; reviewers will want evidence of value on noisy, constrained AM data | 10 | 7 | Multi-panel figure with learning curves, Pareto hypervolume vs experiments, and recommended candidates overlaying known good regions | Preliminary Results; Technical Approach - Bayesian Optimization Engine | Risk that BOFN performance collapses on sparse, noisy, heteroscedastic materials data |
| 3 | CALPHAD-to-print shortlist for 3-5 candidate compositions, including phase stability, solidification range, crack susceptibility proxies, and atomization/LPBF screening criteria | Converts the concept into an actionable experimental starting set and shows manufacturability-aware down-selection, which is critical for Genesis feasibility | 9 | 9 | A screening funnel from broad composition space to a small ranked candidate list with columns for CALPHAD outputs and printability heuristics | Background and Motivation; Preliminary Results - Candidate Alloy Space Definition | Risk of proposing compositions that are thermodynamically interesting but impractical to atomize or print |
| 4 | BOFN ablation study comparing 4-node vs 9-node function networks, with and without cost-awareness, on a surrogate matching FLAIME workflow nodes | Builds on existing BoTorch verification and shows why the proposed architecture is necessary; strengthens technical originality and design choices | 8 | 9 | Bar and line plots comparing simple BO, BOFN-4, BOFN-9, and cost-aware BOFN for regret, MAE, and cost-to-target | Preliminary Results - Algorithm Validation | Risk that the proposed BOFN complexity is unnecessary or unjustified relative to simpler BO |
| 5 | LLM warm-start study showing improved initial candidate proposals versus uninformed initialization for an alloy system relevant to LPBF | Supports novelty in combining domain knowledge extraction with BO and can improve early-iteration efficiency, important in expensive AM experiments | 7 | 8 | Side-by-side comparison of first 5-10 suggested compositions/process settings from random, expert-rule, and LLM-warm-start initializations with downstream BO performance | Preliminary Results - AI Initialization Strategy | Risk that the LLM component is viewed as gimmicky rather than useful for reducing early search cost |
| 6 | LPBF parameter-space reduction from 130+ variables to an experimentally actionable 8-12 parameter subset tied to the selected test structures and sensors | Shows credible experimental scope and execution discipline for Phase I; reviewers need confidence that the search space is not intractable | 9 | 10 | Sankey or pruning diagram showing the reduction from 130+ parameters to 36 critical to a final controllable subset with rationale categories | Technical Approach - Experimental Design Space; Preliminary Results | Risk that the proposed search is too high-dimensional to execute within budget and schedule |
| 7 | Test structure matrix and validation data linking the 8-stage progression to measurable outputs for density, cracking, microstructure, and mechanical proxies | Gives reviewers confidence that characterization is matched to decision-making and that each print generates information useful to the optimizer | 8 | 9 | A matrix figure with specimen geometry images in rows and measurable outputs/decision gates in columns, highlighting the minimum informative build set | Preliminary Results - Test Vehicle Strategy; Technical Approach - Characterization | Risk that printed samples will not yield the right observables for fast go/no-go decisions |
| 8 | KPI/go-no-go dashboard instantiated on a mock or retrospective dataset, showing thresholds, pass/fail logic, and how decisions trigger next BOFN actions | Turns the existing KPI framework into evidence of operational readiness and disciplined project management, which program officers value | 8 | 10 | A dashboard-style table with the 5 headline KPIs, 8 gates, threshold values, current status, and the action each gate triggers in the loop | Statement of Project Objectives; Work Plan and Milestones; Preliminary Results | Risk that success criteria are vague or not tied to machine-actionable decisions |
| 9 | Data architecture and interoperability demonstration: schema linking CALPHAD outputs, powder metadata, LPBF parameters, characterization results, and BOFN inputs/outputs | Closed-loop autonomy depends on robust data plumbing; a clear schema reduces concern that integration work will dominate Phase I | 8 | 9 | A data-flow diagram showing entities, fields, provenance, and interfaces between modeling, manufacturing, characterization, and optimization modules | Technical Approach - Data Infrastructure and Automation | Risk that automation/integration is underdeveloped and the project becomes a manual workflow |
| 10 | Phase I execution table with week-by-week experiment cadence, decision points, and budget-to-data yield estimate for the chosen scenario ($600K-$750K) | Strengthens credibility of the early-career PI by showing realistic operational planning, staffing, and throughput assumptions under the actual budget envelope | 7 | 10 | A compact Gantt-style table listing weeks, tasks, dependencies, expected data outputs, and spend categories tied to go/no-go gates | Project Management Plan; Schedule and Milestones; Budget Justification | Risk that the proposed work cannot be completed on time or within budget by the team as assembled |


*Table: This table prioritizes the most valuable preliminary results to add before the April 28 deadline, balancing proposal impact with 19-day feasibility. It is designed to help decide which figures, tables, and validation activities will most strengthen the FLAIME Genesis Topic 12-F Phase I proposal.*

| Day range | Task | Output artifact/figure | Dependencies | Owner role | Risk/mitigation |
|---|---|---|---|---|---|
| D1-2 (Apr 9-10) | Lock proposal thesis, evaluation rubric, and 5 must-have preliminary results; assign owners and freeze scope | One-page evidence matrix mapping each result to claim, figure, section, and go/no-go metric | Existing KPI/gates list, topic-fit analysis, budget scenarios | PI | Risk: scope creep; mitigation: limit to 5 core + 3 stretch results and require every task to map to a proposal claim |
| D1-4 (Apr 9-12) | Build end-to-end FLAIME digital closed-loop demo using existing BOFN stack and a realistic alloy/LPBF surrogate workflow | Figure 1: pipeline schematic + convergence plot versus random/EI baselines; short methods paragraph | Existing 4-node/9-node BOFN code, surrogate problem definition, pipeline block diagram | Student with PI oversight | Risk: integration bugs; mitigation: use mock interfaces/CSV handoffs first, then polish visuals rather than overengineering automation |
| D2-5 (Apr 10-13) | Run BOFN ablation study: 4-node vs 9-node, with/without cost-awareness, common budget and stopping criteria | Figure 2: regret/cost/hypervolume or target-attainment comparison; compact results table | Existing verified BoTorch implementations | Student | Risk: unclear advantage between variants; mitigation: predefine success metrics and emphasize cost-to-target if absolute performance is similar |
| D2-6 (Apr 10-14) | Assemble retrospective real-data benchmark from literature/internal Al-Si-Mg or LPBF-relevant dataset; clean, normalize, and define objectives/constraints | Figure 3: retrospective benchmark learning curves on noisy real data; dataset summary table | Accessible dataset, property/process labels, PI decisions on objectives | PI + student | Risk: dataset quality or incompleteness; mitigation: use a smaller but defensible retrospective benchmark and state limitations clearly |
| D4-7 (Apr 12-15) | Produce CALPHAD-to-print shortlist for 3-5 candidate compositions with phase stability, freezing range, and printability heuristics | Figure 4: screening funnel from broad composition space to ranked shortlist; candidate table | CALPHAD outputs, alloy system choice, manufacturability heuristics | Collaborator + PI | Risk: weak differentiation among candidates; mitigation: rank with transparent criteria and include uncertainty/decision logic |
| D5-8 (Apr 13-16) | Reduce LPBF search space from 130+ parameters to a defendable Phase I subset linked to selected test structures and sensors | Figure 5: parameter pruning diagram from 130+ to final controllable set; rationale table | Existing parameter map, test-structure plan | PI | Risk: reviewers view subset as arbitrary; mitigation: classify by controllability, sensitivity, and information value |
| D6-9 (Apr 14-17) | Convert test-structure progression into a decision-ready characterization matrix tied to KPIs and go/no-go gates | Figure 6: test structure matrix with outputs (density, cracking, microstructure, hardness proxy) and gate logic | Existing 8-stage validation figure, KPI framework | Student + PI | Risk: too many structures/metrics; mitigation: highlight minimum informative build set for Phase I |
| D7-10 (Apr 15-18) | Instantiate KPI/go-no-go dashboard on mock or retrospective data; connect thresholds to BOFN next-step decisions | Table/Figure 7: dashboard of 5 headline KPIs, 8 gates, thresholds, and triggered actions | Existing KPI definitions, benchmark outputs | PI | Risk: dashboard feels managerial rather than technical; mitigation: explicitly link each gate to experimental/algorithmic decisions |
| D9-12 (Apr 17-20) | Draft and polish all preliminary-results captions, methods snippets, and section text around the new figures | Proposal-ready captions and 1-2 paragraphs per figure inserted into Background, Preliminary Results, and Technical Approach | Completion of core analyses and figure drafts | PI | Risk: figures exist but narrative is weak; mitigation: write claim-evidence-impact text directly under each figure while results are fresh |
| D11-14 (Apr 19-22) | Integrate schedule, staffing, and budget realism with the preliminary evidence; create execution table tied to milestones | Compact Gantt/execution table and revised budget justification language | Core technical figures, budget scenarios, go/no-go gates | PI | Risk: early-career PI credibility concerns; mitigation: show narrow, phased scope with explicit collaborator roles and fallback options |
| D15-17 (Apr 23-25) | Red-team review by skeptical colleague/mentor focusing on feasibility, real-data validation, and overclaiming | Annotated review memo and issue tracker; revised figures/captions | Near-final draft with all core artifacts inserted | Collaborator + PI | Risk: late discovery of major holes; mitigation: ask reviewers to score novelty, feasibility, and evidence sufficiency against DOE criteria |
| D18-19 (Apr 26-28) | Final compliance pass: DOE formatting, page limits, references, figure readability, and consistency across narrative, milestones, and budget | Submission-ready PDF with compliance checklist and final quality-control signoff | Full draft, template, all figures/tables | PI | Risk: last-minute formatting or inconsistency errors; mitigation: freeze technical content by D17 and reserve final 2 days strictly for QA/compliance |


*Table: This table lays out a realistic April 9-28, 2026 sprint plan for an early-career PI and small team to generate the highest-value preliminary results, integrate them into the FLAIME proposal, and complete red-team and compliance review before submission.*

## Section A: Mock Program Officer (AMMTO) Feedback

### A1. What 5 preliminary results would most strengthen this proposal?
Selection logic: DOE/AMMTO Phase I reviewers most reward evidence that (i) the full closed loop is credible (software brain ↔ hardware body), (ii) the optimization is cost-aware and robust to real/noisy data, and (iii) the experimental plan is scoped and qualification-relevant.

1) **End-to-end closed-loop demonstration (digital twin / surrogate) that mirrors CALPHAD→atomization constraints→LPBF→characterization→BOFN**
- *Why AMMTO cares*: AMDM is explicitly a brain/body cyberphysical loop, and Phase I must show the loop can be orchestrated coherently (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3).
- *Impact*: **10/10**
- *Feasibility in 19 days*: **8/10**

2) **Retrospective BOFN benchmark on real alloy/process data (not synthetic), with noise/missingness**
- *Why AMMTO cares*: Real workflows exhibit instrument noise and overhead; cost-aware BO has shown large practical gains when tied to real instruments (chawla2025acceleratedmaterialsdiscovery pages 1-4).
- *Impact*: **10/10**
- *Feasibility*: **7/10**

3) **Cost-aware decision-making demonstration with explicit cost model linked to the workflow nodes**
- *Why AMMTO cares*: Real-world materials workflows are cost/time constrained, and cost-aware BO is a proven lever for accelerating experimental campaigns (alvi2026deepgaussianprocessbased pages 2-4, chawla2025acceleratedmaterialsdiscovery pages 1-4).
- *Impact*: **9/10**
- *Feasibility*: **8/10**

4) **CALPHAD-to-print shortlist (3–5 candidate compositions) with manufacturability-aware screening criteria**
- *Why AMMTO cares*: Establishes that the project will start from an actionable, feasible alloy space rather than open-ended exploration.
- *Impact*: **9/10**
- *Feasibility*: **9/10**

5) **Decision-ready KPI/go-no-go dashboard wired to autonomous actions (optimizer/experiment triggers)**
- *Why AMMTO cares*: In closed-loop systems, gates should not be “reporting”; they must be machine-actionable decisions that manage risk and cost (bukkapatnam2023autonomousmaterialsdiscovery pages 10-11).
- *Impact*: **8/10**
- *Feasibility*: **10/10**

### A2. What specific figures and captions would be most compelling?
(These are written as proposal-ready captions; replace bracketed items with your specifics.)

**Figure A (highest value): “Software brain / hardware body” end-to-end loop + convergence**
- *Figure content*: Two panels.
  - (a) Function-network workflow diagram: CALPHAD screen → powder/atomization constraints → LPBF controllables → characterization outputs → BOFN decision engine.
  - (b) Convergence: cost-to-target (or probability of meeting constraints) vs iteration, BOFN vs baseline strategies.
- *Caption draft*: “FLAIME closed-loop autonomous materials discovery and qualification workflow, consistent with AMDM cyberphysical ‘software brain’ + ‘hardware body’ architectures (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3). BOFN-guided, cost-aware experiment selection reaches the target feasible region faster and at lower total cost than baseline policies under matched budgets.”

**Figure B: Real-data retrospective benchmark (robustness to noise/overhead)**
- *Figure content*: (a) dataset summary; (b) learning curves/hypervolume; (c) qualitative overlay of suggested next points.
- *Caption draft*: “Retrospective evaluation on a noisy real-world dataset, motivated by demonstrations that cost-aware BO in closed-loop experimental systems can yield order-of-magnitude efficiency improvements in practice (chawla2025acceleratedmaterialsdiscovery pages 1-4, chawla2025acceleratedmaterialsdiscovery pages 21-24).”

**Figure C: Cost model tied to workflow nodes (partial evaluation narrative)**
- *Figure content*: A node-cost table/diagram showing relative cost of CALPHAD/cheap proxies vs printing vs characterization, and how BOFN uses this.
- *Caption draft*: “Cost-aware autonomy: BOFN weights information gain by the true workflow cost, favoring inexpensive computational queries for broad exploration and reserving expensive experimental evaluations for targeted exploitation, consistent with cost-aware BO strategies for complex materials campaigns (alvi2026deepgaussianprocessbased pages 2-4).”

**Figure D: CALPHAD-to-print shortlist funnel**
- *Figure content*: funnel from composition space to 3–5 candidates; small table with key screening fields.
- *Caption draft*: “Thermodynamics- and manufacturability-aware down-selection to an actionable Phase I candidate set, enabling disciplined closed-loop iteration rather than open-ended exploration.”

**Table E: KPI/go-no-go dashboard with triggered actions**
- *Figure content*: 5 KPIs + 8 gates + thresholds + measurement method + “optimizer action.”
- *Caption draft*: “Decision-ready success criteria. Gates are tied to autonomous next actions (e.g., shift exploration between composition/process subspaces; request replicates; terminate unpromising branches), enabling efficient sequential experimentation in costly, high-dimensional settings (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3).”

### A3. What narrative sections benefit most from additional preliminary data?
1) **Preliminary Results**: needs at least one end-to-end closed-loop result to establish cyberphysical integration credibility (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3).
2) **Technical Approach—Optimization and cost-awareness**: strengthened by a real-data retrospective benchmark and explicit cost model, reflecting demonstrated gains of cost-aware BO in real experimental loops (chawla2025acceleratedmaterialsdiscovery pages 1-4, alvi2026deepgaussianprocessbased pages 2-4).
3) **Technical Approach—Experimental scope**: strengthened by parameter reduction and test-structure/characterization matrix to prove tractability.
4) **Milestones/Risk management**: strengthened by KPI/go-no-go dashboard that triggers clear decisions, consistent with sequential experimentation framing (bukkapatnam2023autonomousmaterialsdiscovery pages 10-11).

## Section B: Mock Enthusiastic Reviewer

### B1. What results push “good” → “must-fund”
1) **Real-data BOFN win with strong baselines**: clear learning-curve advantage and/or large cost-to-target reduction, mirroring real closed-loop cost-aware BO success stories (chawla2025acceleratedmaterialsdiscovery pages 1-4, alvi2026deepgaussianprocessbased pages 2-4).
2) **End-to-end autonomy demonstration** showing a genuine “brain/body” loop and disciplined sequential experimentation under cost constraints (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3).
3) **Explicit cost model + decision logic** that matches the realities of AM campaigns (cheap computations vs expensive builds/characterization) (alvi2026deepgaussianprocessbased pages 2-4).

### B2. Existing results: strongest vs weakest
**Strongest (already listed by you)**
- BOFN implementations and cost-aware savings: strong technical credibility, and aligned with cost-aware BO relevance in real workflows (chawla2025acceleratedmaterialsdiscovery pages 1-4, alvi2026deepgaussianprocessbased pages 2-4).
- LPBF parameter mapping and test-structure progression: strong feasibility and experimental realism signals.
- KPI/go-no-go gates: strong execution discipline.

**Weakest / most vulnerable**
- LLM warm-start POC: reviewers may see it as peripheral unless you quantify benefit on the same benchmark used to justify BOFN.
- Any claims not tied to a closed-loop demonstration: AMDM reviewers expect integrated cyberphysical evidence, not modular proofs (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3).

## Section C: Mock Skeptical Reviewer

### C1. Biggest gaps in preliminary results
1) **No proof on real/noisy data**: the field has examples where cost-aware BO is validated on real instruments; reviewers will ask for analogous evidence for your setting (chawla2025acceleratedmaterialsdiscovery pages 1-4).
2) **Closed-loop integration risk**: AMDM is defined as an integrated brain/body system; without end-to-end evidence, you look like a set of components (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3).
3) **Cost realism**: reviewers will demand an explicit cost model and evidence that your method uses it effectively, since cost-awareness is central in the literature (alvi2026deepgaussianprocessbased pages 2-4).

### C2. What I would need to see to believe BOFN works for real alloys (not synthetic)
- **Retrospective on real dataset with noise handling**: at minimum, repeated runs, baselines, and uncertainty calibration.
- **Cost-aware advantage** demonstrated under a realistic cost model, consistent with prior cost-aware BO successes in real experimental loops (chawla2025acceleratedmaterialsdiscovery pages 1-4, chawla2025acceleratedmaterialsdiscovery pages 21-24).
- **Ablations**: show where BOFN’s gain comes from (function-network structure vs standard BO), to avoid “overfit architecture” concerns.

### C3. Concerns about feasibility of the 19-day timeline
- The only truly schedule-threatening items are (i) acquiring/cleaning a defensible real dataset and (ii) building a polished end-to-end demo; these should dominate the sprint.
- Attempting new atomization + LPBF printing purely for prelims is high risk unless machine time/powder logistics are guaranteed.

## Section D: Mock Moderate Reviewer

### D1. Prioritized list of 8–10 preliminary results (ranked by proposal impact)
(With figure look, caption intent, and where it goes.)

1) **End-to-end closed-loop demo**
- *Figure*: architecture + convergence.
- *Caption*: emphasizes AMDM brain/body framing and cost/time pressure (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3).
- *Where*: Preliminary Results (lead), then referenced in Approach.

2) **Real-data retrospective benchmark**
- *Figure*: learning curves + robustness.
- *Caption*: ties to demonstrated real-world value of cost-aware BO in closed loops (chawla2025acceleratedmaterialsdiscovery pages 1-4).
- *Where*: Preliminary Results (second).

3) **Cost model and cost-aware acquisition behavior**
- *Figure*: node cost table + “cheap exploration vs expensive exploitation” illustration.
- *Caption*: echoes cost-aware BO campaign framing (alvi2026deepgaussianprocessbased pages 2-4).
- *Where*: Approach (Optimization), with small prelim inset.

4) **BOFN ablation (4 vs 9 nodes; cost-aware vs not)**
- *Figure*: cost-to-target and performance.
- *Where*: Preliminary Results (algorithm validation).

5) **CALPHAD-to-print shortlist**
- *Figure*: funnel + candidate table.
- *Where*: Background + Prelims.

6) **LPBF parameter-space reduction to Phase I controllables**
- *Figure*: pruning diagram.
- *Where*: Approach (Experimental design space).

7) **Test-structure/characterization matrix tied to gates**
- *Figure*: matrix linking each structure to observables and decisions.
- *Where*: Approach (Qualification/characterization).

8) **KPI/go-no-go dashboard (instantiated)**
- *Table*: thresholds + actions.
- *Where*: Milestones/Work plan.

9) **Data schema / interoperability**
- *Figure*: dataflow/entity diagram.
- *Where*: Approach (Data management and autonomy).

10) **Execution cadence + cost-to-data yield**
- *Table*: week-by-week builds/characterization throughput.
- *Where*: Management plan and budget.

## Section E: Synthesis and Action Plan

### E1. Top 5 “must-have” results (core, achievable in 19 days)
1) End-to-end closed-loop demo (digital surrogate) (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3)
2) Real-data retrospective benchmark (chawla2025acceleratedmaterialsdiscovery pages 1-4)
3) Explicit cost model tied to workflow nodes + cost-aware behavior demo (alvi2026deepgaussianprocessbased pages 2-4)
4) BOFN ablation study (structure + cost-awareness)
5) KPI/go-no-go dashboard wired to autonomous actions

### E2. Top 3 “stretch” results (high impact but time-risky)
1) Minimal experimental pilot coupons (only if logistics guaranteed)
2) Multi-fidelity demonstration (cheap proxies + expensive evaluations), aligning with cost-aware campaign logic (alvi2026deepgaussianprocessbased pages 2-4)
3) Automated data plumbing demo (end-to-end ingestion/export)

### E3. Figure specifications (size/content/caption draft) for each must-have

**Must-have 1: End-to-end closed-loop demo**
- *Size*: full-width (two-column), ~0.45–0.55 page.
- *Content*: (a) brain/body function network; (b) cost-to-target; (c) constraint satisfaction probability.
- *Caption*: use Figure A draft above; cite AMDM brain/body framing (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3).

**Must-have 2: Real-data retrospective benchmark**
- *Size*: full-width half-page with 3 panels.
- *Content*: dataset summary + learning curves + qualitative overlay.
- *Caption*: connect to real closed-loop cost-aware BO improvements (chawla2025acceleratedmaterialsdiscovery pages 1-4, chawla2025acceleratedmaterialsdiscovery pages 21-24).

**Must-have 3: Cost model + cost-aware acquisition behavior**
- *Size*: quarter-page figure + small adjacent table.
- *Content*: node-cost table; schematic of query selection frequency by node.
- *Caption*: emphasize “cheap exploration / expensive exploitation” campaign framing (alvi2026deepgaussianprocessbased pages 2-4).

**Must-have 4: BOFN ablation**
- *Size*: quarter- to half-page.
- *Content*: regret/performance + cost-to-target bars.
- *Caption*: “BOFN structure and cost-awareness reduce cost-to-target under matched budgets.”

**Must-have 5: KPI/go-no-go dashboard**
- *Size*: full-width table.
- *Content*: KPI, gate, threshold, measurement, cadence, triggered optimizer action.
- *Caption*: tie to sequential experimentation under costly evaluations (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3).

### E4. Mapping of must-have results to proposal sections
- **Background/Motivation**: cite AMDM as cyberphysical brain/body and emphasize costliness/high dimensionality (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3).
- **Preliminary Results**: Figures A–D + real-data benchmark (chawla2025acceleratedmaterialsdiscovery pages 1-4, alvi2026deepgaussianprocessbased pages 2-4).
- **Technical Approach**: cost model + multi-fidelity strategy (alvi2026deepgaussianprocessbased pages 2-4) + closed-loop decision logic.
- **Work Plan/Milestones/Risk**: KPI/go-no-go dashboard and explicit pivots; reinforce need for disciplined sequential experimentation (bukkapatnam2023autonomousmaterialsdiscovery pages 10-11).

### Execution emphasis
Because cost-aware BO has demonstrated large throughput improvements in real closed-loop experimentation (chawla2025acceleratedmaterialsdiscovery pages 1-4, chawla2025acceleratedmaterialsdiscovery pages 21-24), the fastest path to strengthening reviewer confidence is to prioritize (i) a defensible real-data retrospective benchmark and (ii) an end-to-end closed-loop demo, and to treat LLM warm-start as optional unless it produces a clear, quantified gain on the same benchmark.


References

1. (bukkapatnam2023autonomousmaterialsdiscovery pages 1-3): Satish T.S. Bukkapatnam. Autonomous materials discovery and manufacturing (amdm): a review and perspectives. IISE Transactions, 55:75-93, Aug 2023. URL: https://doi.org/10.1080/24725854.2022.2089785, doi:10.1080/24725854.2022.2089785. This article has 26 citations.

2. (bukkapatnam2023autonomousmaterialsdiscovery pages 10-11): Satish T.S. Bukkapatnam. Autonomous materials discovery and manufacturing (amdm): a review and perspectives. IISE Transactions, 55:75-93, Aug 2023. URL: https://doi.org/10.1080/24725854.2022.2089785, doi:10.1080/24725854.2022.2089785. This article has 26 citations.

3. (chawla2025acceleratedmaterialsdiscovery pages 1-4): Vivek Chawla, S. Puplampu, Haochen Zhu, Philip D. Rack, D. Penumadu, and Sergei V. Kalinin. Accelerated materials discovery through cost-aware bayesian optimization of real-world indentation workflows. ArXiv, Nov 2025. URL: https://doi.org/10.48550/arxiv.2511.16930, doi:10.48550/arxiv.2511.16930. This article has 2 citations.

4. (chawla2025acceleratedmaterialsdiscovery pages 21-24): Vivek Chawla, S. Puplampu, Haochen Zhu, Philip D. Rack, D. Penumadu, and Sergei V. Kalinin. Accelerated materials discovery through cost-aware bayesian optimization of real-world indentation workflows. ArXiv, Nov 2025. URL: https://doi.org/10.48550/arxiv.2511.16930, doi:10.48550/arxiv.2511.16930. This article has 2 citations.

5. (alvi2026deepgaussianprocessbased pages 2-4): Sk Md Ahnaf Akif Alvi, Brent Vela, V. Attari, Jan Janssen, Danny Perez, Douglas L. Allaire, and Raymundo Arróyave. Deep gaussian process-based cost-aware batch bayesian optimization for complex materials design campaigns. npj Computational Materials, Feb 2026. URL: https://doi.org/10.1038/s41524-026-01981-7, doi:10.1038/s41524-026-01981-7. This article has 2 citations and is from a peer-reviewed journal.

6. (alvi2026deepgaussianprocessbased pages 1-2): Sk Md Ahnaf Akif Alvi, Brent Vela, V. Attari, Jan Janssen, Danny Perez, Douglas L. Allaire, and Raymundo Arróyave. Deep gaussian process-based cost-aware batch bayesian optimization for complex materials design campaigns. npj Computational Materials, Feb 2026. URL: https://doi.org/10.1038/s41524-026-01981-7, doi:10.1038/s41524-026-01981-7. This article has 2 citations and is from a peer-reviewed journal.