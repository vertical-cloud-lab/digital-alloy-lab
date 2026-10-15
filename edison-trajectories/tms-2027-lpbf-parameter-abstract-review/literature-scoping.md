# LPBF Process-Parameter Optimization — Literature Scoping

*Scoping for the TMS 2027 abstract [`tms-2027-lpbf-process-parameter-optimization-abstract.md`](../../tms-2027-lpbf-process-parameter-optimization-abstract.md).*

> **Method note.** Issue #100 asked to "send an Edison Scientific search" to scope this work. This file is the
> lighter-weight **web-search** scoping (WebSearch/WebFetch, July 2026) that was assembled first. The full-depth
> Edison Scientific / PaperQA3 `LITERATURE_HIGH` query **has since been run** (the ready-to-paste prompt in §4)
> and its report is saved alongside this file as
> [`edison-literature-high-report.md`](./edison-literature-high-report.md) — ~54 K characters, 87 retrieved
> contexts, ~48 unique DOIs, and a 20-row ranked reference table (task `d65ddcc0…`, 2026-07-02). Consult that
> report for the load-bearing citations; this file remains a quick orientation.
>
> **Key convergences from the Edison report** (which independently confirm and sharpen this scoping):
> Liu et al. 2020 (GP-assisted AlSi10Mg optimization, `10.1016/j.actamat.2020.10.010`) is the single most
> aligned reference; Sheikh et al. 2024 (`10.1038/s41524-024-01436-x`) is the best CALPHAD/Eagar-Tsai
> printability-map prior; Reijonen et al. 2021 (`10.1016/j.matdes.2021.109684`) is the strongest cross-machine
> transfer-gap evidence (~7 % tensile, ~20 % impact-toughness variation, 316L across SLM 125 HL vs. EOS M290);
> and Edison rates the **same-model instance-to-instance transfer** and the **agentic-LLM parameter-selection**
> claims as only *weakly supported* in the literature — i.e., the two clearest novelty hooks for the abstract.

---

## 1. What the campaign actually is (scope of the experimental work)

From the issue: a series of **a couple dozen runs** on the **Aconity MIDI** open-architecture LPBF system at the
**University of Utah** (Taylor Sparks' lab, a FLAIME Letter-of-Support partner), optimizing print parameters
**per individual powder type**. The escalating experimental ladder:

| Stage | Artifact | Primary measurement | What it locks in |
| --- | --- | --- | --- |
| 1 | **Single tracks** (no powder / on powder) | melt-pool width & depth, defect onset (balling, humping) | laser power × scan speed feasible band; melting mode |
| 2 | **Density cubes** | relative density (Archimedes + cross-section imaging) | hatch spacing, layer-coupling; ~99%+ density window |
| 3 | **ISO / ASTM geometric artifacts** | dimensional accuracy, features (ISO/ASTM 52902) | build-quality / repeatability across the window |
| 4 | **Tensile bars** | YS / UTS / elongation | mechanical validation of the chosen parameter set |

Supporting tooling:
- **Thermo-Calc AM Module** — CALPHAD-derived, alloy-specific printability maps (keyholing / lack-of-fusion /
  balling in power–speed space) and steady-state melt-pool geometry, used as a **physically informed prior** to
  narrow the search *before* burning build plates. (See the repository review
  [`../thermocalc_am_module.md`](../thermocalc_am_module.md); e.g., Hosseini et al. 2025 mapped an Al6061 window
  of 44.64–50 J/mm³ → ~99% density with the TCAl9 database.)
- **ML / Bayesian optimization** — sequential experiment design over the printability prior to reach a qualified
  window in as few builds as possible.
- **LLM-agent layer** — a tool-calling assistant that drafts parameter sets, calls the Thermo-Calc / optimizer
  tools, and helps interpret SEM + melt-pool imagery (analogous to the in-house agentic **SEM-characterization**
  workflows the group is developing — the "Ronnie / SEM workflows" idea in the issue).

---

## 2. Prior work — the four questions the issue asked to check

### 2.1 Tuning LPBF process parameters (the baseline practice)

The dominant levers on single-track and bulk quality are **laser power (P)**, **scan speed (V)**, and
**hatch spacing**, often collapsed to a **linear or volumetric energy density** (E = P/V, or P/(V·h·t)).
Established practice climbs from single tracks (melting-mode / defect maps) → density cubes → mechanical bars,
and uses design-of-experiments (central composite / full-factorial) plus melt-pool modeling to place the window.

- *Understanding melt-pool characteristics in LPBF — single- & multi-track melt pools for process optimization*
  (2023). [S2772834X23000295](https://www.sciencedirect.com/science/article/pii/S2772834X23000295)
- *Optimization of LPBF using melt-pool modeling + DoE: density control* — MDPI *JMMP* **3**(1), 21.
  [mdpi.com/2504-4494/3/1/21](https://www.mdpi.com/2504-4494/3/1/21)
- *Systematic parameter optimization for LPBF of low-alloy steel based on melting modes* — *Int. J. Adv. Manuf.
  Technol.* (2023). doi:[10.1007/s00170-023-11377-2](https://doi.org/10.1007/s00170-023-11377-2)
- *Development of L-PBF parameters & scan strategy for new alloy grades: a holistic method* —
  [PMC6316907](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6316907/) (a good template for the per-new-powder
  workflow this abstract describes).

**Takeaway for the abstract:** the *practice* is well established, so novelty is **not** "we tune parameters."
Novelty is (a) the simulation-seeded, budget-aware loop, (b) the explicit **transfer** study, and (c) the
**LLM-agent** layer.

### 2.2 Transferability across machines / instances (the strongest novelty hook)

This is the clearest open problem and the best differentiator. Parameter windows are **highly
platform-specific** and transfer poorly — not only across vendors but even across nominally identical machines
and environments; per-platform models often require laborious repeat tensile testing to rebuild from scratch.
Transfer-learning is the emerging remedy.

- *Cross-platform LPBF process–property modeling with active transfer learning* (2025) — reduces tensile-test
  burden by leveraging knowledge from other platforms making similar materials.
  [S152661252500605X](https://www.sciencedirect.com/science/article/abs/pii/S152661252500605X)
- *Knowledge transfer between machines in LPBF — transfer learning with small training datasets* — *Metals*
  **16**(4), 438 (2026). doi:[10.3390/met16040438](https://doi.org/10.3390/met16040438) (source→target across
  different hardware; inductive transfer / parameter transfer).
- *Transferability of process parameters in LPBF for energy- & cost-efficient manufacturing* — *Sustainability*
  **12**(4), 1565 (2020). doi:[10.3390/su12041565](https://doi.org/10.3390/su12041565)
- *EBM & LPBF of Ti-6Al-4V: transferability of process parameters* (2022, ResearchGate) — cross-**process**
  transfer as an even harder bound.

**Takeaway:** framing the abstract around "how much of an optimized window transfers across machines **and across
instances of the same machine**, and how few experiments a transfer-aware model needs to re-qualify" is
well-motivated and, per the literature, **largely unresolved** — especially the same-model, instance-to-instance
case, which is under-reported. Keep it as a **question we measure**, not a solved claim (credibility for an
early-stage group).

### 2.3 ML / AI for locking in print parameters

- *A high-throughput approach for statistical process optimization in LPBF* — *J. Manuf. Process.* (2025):
  high-throughput single tracks + GAN melt-pool extraction + statistical/ML modeling.
  [S1526612525004992](https://www.sciencedirect.com/science/article/abs/pii/S1526612525004992)
- *Designing materials by LPBF with ML-driven bi-objective optimization* — *J. Mater. Res. Technol.* (2024).
  [S2238785424010883](https://www.sciencedirect.com/science/article/pii/S2238785424010883)
- *Comprehensive study on statistical methods for optimization of AlSi10Mg in LPBF* — *Discover Mech. Eng.*
  (2024). doi:[10.1007/s44245-024-00073-4](https://doi.org/10.1007/s44245-024-00073-4)
- *ML-assisted optimisation of PBF-LB parameters for H13 on a 350 °C preheated platform* —
  [PMC12787040](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12787040/)
- Bayesian optimization is the natural fit for **uncertainty-aware, sequential** parameter search; batch BO
  addresses parallel builds but is noted as practically challenging. This dovetails with the group's existing
  BOFN / pKGFN optimization stack.

**Takeaway:** BO over a Thermo-Calc printability prior is a defensible, on-trend method; the differentiator vs.
prior ML-LPBF papers is the **prior-seeded + transfer-aware + agent-assisted** integration, not the optimizer
itself.

### 2.4 LLMs / agentic systems (the "Ronnie / SEM workflows" analogy)

A young but fast-moving thread: LLMs for **parameter selection**, **defect prediction**, and **agentic
tool-calling** over AM tasks.

- *AdditiveLLM: LLMs predict defects in metals AM* — predicts keyholing / lack-of-fusion / balling / none from
  material + power + velocity. [arXiv:2501.17784](https://arxiv.org/abs/2501.17784)
- *Agentic Additive Manufacturing Alloy Evaluation* — LLM agents dispatch **MCP** tool calls (thermophysical
  property diagrams, lack-of-fusion process-map generation) to reason about printability.
  [arXiv:2510.02567](https://arxiv.org/abs/2510.02567)
- *LLM-ADAM: generalizable LLM-agent framework for pre-print anomaly detection in AM*
  [arXiv:2605.03328](https://arxiv.org/abs/2605.03328)
- *AutoMEX: AI agents (LLM + knowledge graph) streamlining material-extrusion process/parameter selection* —
  *Addit. Manuf.* (2025). [S0264127525000644](https://www.sciencedirect.com/science/article/pii/S0264127525000644)

**Takeaway:** an LLM-agent that drafts parameter sets, calls Thermo-Calc/optimizer tools (MCP-style), and
interprets SEM/melt-pool imagery is a **credible, current** research direction with direct prior art — and it
mirrors the group's own agentic SEM-characterization work. Position it as a **pilot** that *augments* the
statistical loop, not a replacement (matches the reviewer-credibility posture used on the atomization abstract).

---

## 3. Gap statement (one sentence for the talk)

> Parameter qualification is well-practiced per machine, but the field lacks a **budget-aware loop that seeds
> the search with CALPHAD printability priors, measures how far an optimized window transfers across machines and
> instances, and tests where an LLM agent usefully augments the optimization** — which is exactly what this
> campaign delivers, per powder, on the Aconity MIDI.

---

## 4. Ready-to-run Edison Scientific `LITERATURE_HIGH` prompt

Paste this into Edison Scientific to produce the full-depth review (to match the other `edison-trajectories/`
reports) and drop the result alongside this file:

```
Question: What is the published literature (2018–2026) on optimizing laser powder bed fusion (LPBF/PBF-LB)
process parameters for individual metal powders, and how well do optimized parameter windows transfer between
machines? Cover, with citations and DOIs:
(1) Standard parameter-optimization workflows: single-track melt-pool studies, density cubes, ISO/ASTM 52902
    geometric artifacts, and tensile-bar qualification; the roles of laser power, scan speed, hatch spacing,
    layer thickness, and linear/volumetric energy density; and design-of-experiments vs. sequential methods.
(2) Transferability and reproducibility of LPBF process parameters ACROSS machines, across vendors, and across
    two instances of the SAME machine model; quantified transfer gaps; and transfer-learning / domain-adaptation
    approaches that reduce re-qualification cost on a target machine.
(3) Machine-learning and Bayesian-optimization methods for LPBF parameter selection, including uncertainty-aware
    sequential design, batch BO for parallel builds, and surrogate/printability-map-seeded optimization.
(4) Use of the Thermo-Calc AM Module (and comparable CALPHAD-based printability maps / Eagar-Tsai / Rosenthal
    models) to define keyholing / lack-of-fusion / balling windows as a prior for experiment design.
(5) Large-language-model and agentic (tool-calling / MCP) systems for AM process-parameter selection, defect
    prediction, and characterization interpretation (e.g., SEM image analysis).

Context: BYU Vertical Cloud Lab (FLAIME project). A couple dozen LPBF runs per powder on an Aconity MIDI
open-architecture system at the University of Utah (Taylor Sparks), optimizing parameters for individual powder
types — commercial AlSi10Mg baseline and novel supply-chain-resilient aluminum compositions — using a
Thermo-Calc-AM-Module prior + Bayesian optimization + an LLM-agent layer, with an explicit cross-machine /
cross-instance transferability study. Rank the most load-bearing references and note which claims are strongly
vs. weakly supported.
```

---

## 5. Sources consulted (web search, July 2026)

- ProgramMaster / TMS2027 technical program: [programmaster.org/TMS2027](https://www.programmaster.org/TMS2027),
  [tms.org TMS2027 technical program](https://www.tms.org/TMS2027/TMS2027/Programming/TMS2027_Technical_Program.aspx)
- Transferability: [S152661252500605X](https://www.sciencedirect.com/science/article/abs/pii/S152661252500605X),
  [met16040438](https://doi.org/10.3390/met16040438), [su12041565](https://doi.org/10.3390/su12041565)
- ML / BO for LPBF: [S1526612525004992](https://www.sciencedirect.com/science/article/abs/pii/S1526612525004992),
  [S2238785424010883](https://www.sciencedirect.com/science/article/pii/S2238785424010883),
  [S2772834X23000295](https://www.sciencedirect.com/science/article/pii/S2772834X23000295),
  [s44245-024-00073-4](https://doi.org/10.1007/s44245-024-00073-4)
- LLM / agentic AM: [AdditiveLLM arXiv:2501.17784](https://arxiv.org/abs/2501.17784),
  [Agentic AM Alloy Evaluation arXiv:2510.02567](https://arxiv.org/abs/2510.02567),
  [LLM-ADAM arXiv:2605.03328](https://arxiv.org/abs/2605.03328),
  [AutoMEX S0264127525000644](https://www.sciencedirect.com/science/article/pii/S0264127525000644)
- Thermo-Calc AM Module: repository review [`../thermocalc_am_module.md`](../thermocalc_am_module.md)
