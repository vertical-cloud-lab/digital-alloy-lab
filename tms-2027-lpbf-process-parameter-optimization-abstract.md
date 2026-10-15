# TMS 2027 Abstract — LPBF Process Parameter Optimization

**Working title:** Accelerated, Transfer-Aware Optimization of Laser Powder Bed Fusion Process Parameters: Coupling Thermo-Calc Printability Maps, Bayesian Optimization, and an LLM Agent Across a Wide Aluminum Composition Space and Machines

**Authors (Brigham Young University unless noted):**

| # | Author | Affiliation | Role |
| --- | --- | --- | --- |
| 1 | Carl Robison | BYU | First author / presenting author (characterization) |
| 2 | Ronnie Guymon | BYU | LPBF builds / SEM characterization |
| 3 | Xavier Zaitzeff | BYU | Optimization / software |
| 4 | Gage Erickson | BYU | Powder / feedstock |
| 5 | Alik Nielsen | University of Utah (Mechanical Engineering) | LPBF printing (Aconity MIDI) |
| 6 | Ashley Spear | University of Utah (Mechanical Engineering) | Mechanics / characterization |
| 7 | Sterling Baird | BYU | Corresponding author / PI |

> ⚠️ **Verify before submission:** author order, presenting author, affiliations, and emails.
> Author order per PI direction (2026-07-02): **Carl Robison (first)**, Ronnie Guymon, Xavier Zaitzeff,
> Gage Erickson, Alik Nielsen (U of Utah Mech Eng), Ashley Spear (U of Utah Mech Eng), Sterling Baird.
> Emails for the BYU authors are carried over from the [TMS 2027 atomization abstract](tms-2027-ultrasonic-atomization-abstract.md).
> - **Name-spelling check:** confirm **"Ashley Spear"** (U of Utah Mechanical Engineering) — several older
>   FLAIME docs (e.g. [`publication_strategy.md`](edison-trajectories/publication_strategy.md)) write
>   "Ashley Speer" and sometimes list a BYU affiliation; reconcile the two before submission.
> - **LPBF partner change:** the Aconity MIDI work is now credited to **Alik Nielsen / Ashley Spear (U of Utah
>   Mechanical Engineering)** as co-authors, superseding the earlier placeholder that named Taylor Sparks
>   (a FLAIME Letter-of-Support partner) as the print-side co-author. Confirm the correct U of Utah
>   collaborator(s) and whether Taylor Sparks should also appear as co-author or in the acknowledgements.

**Meeting:** TMS 2027 Annual Meeting & Exhibition, March 14–18, 2027, Orlando, FL
**Presentation preference:** Oral Presentation
**Symposium (selected):** AI-Enabled Materials Processing: Integrating Accelerated Experimental Workflows and Processing-Aware Machine Learning
**Abstract submission:** via [ProgramMaster](https://www.programmaster.org/TMS2027) ([TMS2027 technical program](https://www.tms.org/TMS2027/TMS2027/Programming/TMS2027_Technical_Program.aspx))

> Context: part of the FLAIME project on AI-guided, supply-chain-resilient aluminum alloy discovery for additive
> manufacturing. Companion to the [ultrasonic atomization abstract](tms-2027-ultrasonic-atomization-abstract.md)
> (feedstock production) — this abstract covers the **downstream printing / parameter-qualification** half of the
> powder-to-part loop. See [Publication Strategy](edison-trajectories/publication_strategy.md).

---

## Abstract (submission version, 150 words)

Locking in laser powder bed fusion (LPBF) process parameters for a new powder still relies on large,
machine-specific sweeps that rarely transfer between systems — or even between two instances of the same
machine — and must be repeated for every new alloy. We present an accelerated, processing-aware workflow
coupling Thermo-Calc AM Module printability maps (keyholing, lack-of-fusion, balling) with Bayesian
optimization to narrow the laser-power/scan-speed/hatch-spacing space before printing, then validate on an
Aconity MIDI at the University of Utah. Spanning a wide aluminum palette — from AlSi10Mg baselines to lean,
supply-chain-resilient compositions — we climb an escalating test ladder (single-track scans, density cubes,
ISO/ASTM artifacts, tensile bars) relating parameters to melt-pool geometry, density, and mechanical
properties, and map where CALPHAD-based printability predictions hold and where they break down in
under-characterized composition space. We test cross-machine/instance transfer, pilot an LLM-agent layer, and
report data-driven windows and the experimental budget each requires.

---

## Expanded / alternate version (leans harder into the AI + transfer story)

Qualifying a new metal powder for laser powder bed fusion (LPBF) still means burning through large,
one-factor-at-a-time or full-factorial parameter sweeps — and the resulting windows are notoriously
machine-specific, often failing to transfer not only between vendors but between two nominally identical
instruments. This work presents a processing-aware, budget-conscious workflow for locking in LPBF parameters
that treats simulation, optimization, and characterization as one loop. We first use the Thermo-Calc AM Module
to compute alloy-specific printability maps (steady-state melt-pool geometry and keyholing / lack-of-fusion /
balling boundaries in power–speed space) directly from CALPHAD thermophysical properties, seeding a physically
informed prior. Bayesian optimization then proposes an efficient sequence of experiments within that prior,
which we execute on an Aconity MIDI open-architecture system at the University of Utah. For each powder type we
climb a standard escalating test ladder — single-track scans (melt-pool width/depth and defect onset), density
cubes (relative density via Archimedes and cross-sectional imaging), ISO/ASTM 52902 geometric benchmark
artifacts, and tensile bars (yield strength, UTS, elongation) — accumulating roughly two dozen builds per
powder into a parameter–property dataset spanning commercial baselines (e.g., AlSi10Mg) and novel
supply-chain-resilient aluminum compositions. Across this dataset we ask three questions the field has largely
left open: how well the Thermo-Calc AM Module's printability predictions hold as composition moves away from the
well-assessed alloys its CALPHAD databases and absorptivity model were calibrated on — i.e., *where in
composition space the simulation can be trusted and where experiment must take over*; how much of an optimized
window transfers across machines and across instances of the same machine; and how few experiments a
transfer-aware model needs to re-qualify a powder on a second system. Finally, we
pilot an LLM-agent layer — analogous to the agentic SEM-characterization workflows we are developing in-house —
that drafts candidate parameter sets, calls the Thermo-Calc and optimization tools, and helps interpret melt-pool
and SEM imagery, testing where language-model reasoning usefully augments (rather than replaces) the statistical
loop. We present composition-specific processing windows, an honest accounting of the experimental budget each
requires, and early evidence on cross-machine transferability.

---

## Alternate submission version — *AM Modeling, Simulation & AI* symposium (simulation-forward, 147 words)

> **When to use this one.** Submit this variant instead of the [150-word version](#abstract-submission-version-150-words)
> if the talk targets **Additive Manufacturing Modeling, Simulation, and Artificial Intelligence: Microstructure,
> Mechanics, and Process** (see [symposium selection](#symposium-selection-tms-2027)). It re-centers the same
> campaign on the committee's vocabulary — **model validation, melt-pool/microstructure prediction, mechanics, and
> the model↔experiment feedback loop** — promoting the Thermo-Calc AM Module from a supporting prior to a co-lead
> and demoting the LLM agent to keep the room's focus. Same authors, same experiments; different emphasis.

Physics-based process models promise to shortcut the machine-specific parameter sweeps that still dominate laser
powder bed fusion (LPBF) qualification, but their melt-pool and defect predictions need experimental validation,
especially for novel alloys far from the compositions their databases were assessed on. We couple Thermo-Calc AM
Module simulations — CALPHAD-derived thermophysical
properties predicting melt-pool geometry and keyholing, lack-of-fusion, and balling boundaries in power–speed
space — with Bayesian optimization and a matched experimental campaign on an Aconity MIDI at the University of
Utah. Spanning a wide aluminum palette from AlSi10Mg baselines to lean, supply-chain-resilient compositions, we
climb an escalating test ladder (single-track cross-sections, density cubes, ISO/ASTM 52902 artifacts, tensile
bars), validating predicted melt-pool width and depth, melting-mode transitions, density, and mechanics against
measurement. Cross-section data feeds back to calibrate the module's aluminum absorptivity, and we map where
predictions degrade in under-characterized composition space and how well validated windows transfer across
machines and instances.

> **Framing deltas vs. the AI-Enabled-Materials-Processing version (why each word moved):**
> - **Leads with simulation/validation**, not with the accelerated-workflow/optimization story — the AM-modeling
>   room rewards *predict-then-validate* over *optimize-then-report*.
> - **Thermo-Calc AM Module is the protagonist:** melt-pool geometry, melting-mode transitions, and
>   keyhole/LOF/balling boundaries are framed as *predictions to be tested*, mapping onto the symposium's
>   "Microstructure" and "Process" axes; the tensile/mechanical-response thread maps onto "Mechanics" (Ashley
>   Spear's contribution).
> - **The calibration-feedback loop is promoted into the submission abstract itself** (single-track cross-sections
>   → absorptivity calibration → refined predictions), because in this room the model↔experiment loop *is* the
>   contribution rather than an optional aside. This is the one place the [Optional angle](#optional-angle--thermo-calc-am-module-calibration-feedback-documented-not-committed-in-the-submission-abstract)
>   is worth spending scarce words on. Keep it honest — *"feeds back to calibrate,"* a thing we can do with data
>   in hand, not a promised validated result.
> - **The LLM agent is dropped** from the 150-word box (it reads as off-topic to a modeling/mechanics committee);
>   keep it for the expanded/talk versions if asked. Add it back only if the organizers' scope note explicitly
>   welcomes agentic/AI-workflow content.
> - **Transferability is retained** but reframed as *"how well validated windows transfer"* — a model-generalization
>   question, which this audience reads as a modeling result rather than a pure process-engineering one.
> - **Composition is now a co-headline** (added 2026-07-07 per PI direction). Both submission versions foreground
>   the *wide aluminum elemental palette* (AlSi10Mg baselines → lean, supply-chain-resilient compositions) and,
>   crucially, frame **where the simulation breaks down in under-characterized composition space** as a measured
>   result rather than a caveat. This lands especially well in this room: CALPHAD databases and the AM Module's
>   thermophysical-property/absorptivity models are most reliable near well-assessed alloys, so *quantifying the
>   composition-space envelope of trust* — and using the cross-section calibration loop to push it outward — is a
>   genuine model-validation contribution, not a limitation to be hidden. See
>   [Composition emphasis](#composition-emphasis--wide-elemental-palette--simulation-reliability-in-new-composition-space).

An **expanded, simulation-forward** paragraph (for the talk, proceedings, or a referenced version) can graft the
model-validation framing above onto the existing [expanded version](#expanded--alternate-version-leans-harder-into-the-ai--transfer-story):
lead with the AM Module printability-map computation, spend a sentence on *quantitative* melt-pool agreement
(predicted vs. measured width/depth and melting-mode boundaries), then add the G/R equiaxed-transition and
Scheil-based crack-susceptibility validations from the [Optional angle](#optional-angle--thermo-calc-am-module-calibration-feedback-documented-not-committed-in-the-submission-abstract)
as further model↔experiment tests, and close with cross-machine transfer as a model-generalization check.

---

## Alternate submission version — *AI-ICME* symposium (composition-forward ICME loop, 150 words)
<!-- wc -w = 150 (counts the three standalone em-dashes as words); at the ~150-word ProgramMaster limit. Excluding em-dashes: 147. -->

> **When to use this one.** Submit this variant if the talk targets **Artificial Intelligence Applications in
> Integrated Computational Materials Engineering (AI-ICME)** (see [symposium selection](#symposium-selection-tms-2027)).
> It re-centers the same campaign as an **ICME loop** in the committee's native vocabulary — CALPHAD-derived
> properties → Thermo-Calc AM Module printability prediction → Bayesian optimization → experiment → data fed
> *back* — and, per the organizer read on
> [PR #101](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/101#issuecomment-4870800010)
> (Pilania/GE Aerospace, Devanathan/PNNL, Mishra/LANL, Miller/UF — a CALPHAD-native, DOE-lab + industry room),
> foregrounds the axis this audience cares about most: **how CALPHAD-based printability predictions hold up as
> composition moves into new, sparsely-calibrated regions of a wide aluminum elemental palette.** Same authors,
> same experiments; the composition-space and model-feedback story is the protagonist.

Integrated computational materials engineering (ICME) promises to compress laser powder bed fusion (LPBF)
parameter qualification by predicting printable windows before printing — but CALPHAD-based predictions are least
tested exactly where new alloys live: unexplored regions of composition space. We build an ICME loop spanning a
wide aluminum elemental palette. Thermo-Calc AM Module simulations translate CALPHAD-derived thermophysical
properties into melt-pool geometry and keyholing/lack-of-fusion/balling boundaries in power–speed space; Bayesian
optimization proposes an efficient experiment sequence; and a matched campaign on an Aconity MIDI at the
University of Utah climbs an escalating ladder (single-track cross-sections, density cubes, ISO/ASTM 52902
artifacts, tensile bars). Single-track cross-sections feed back to calibrate the module's aluminum absorptivity,
testing where predictions hold — and where they degrade — as composition moves away from calibrated baselines. An
LLM agent orchestrates the simulation and optimization tool calls. We report
composition-resolved model–experiment agreement, cross-machine/instance transfer, and the experimental budget
each alloy requires.

> **Framing deltas vs. the AI-Enabled and AM-Modeling versions (why each word moved):**
> - **Leads with ICME + composition space**, not with workflow acceleration (AI-Enabled) or predict-then-validate
>   melt-pool modeling (AM-Modeling). The load-bearing claim is that CALPHAD/AM-Module predictions are *least
>   validated where new alloys live* — the failure-in-new-composition-space question raised in
>   [PR comment #4909…](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/101) — which is
>   exactly the tension a CALPHAD-native audience finds compelling.
> - **Composition is the protagonist, framed as ICME generalization.** All three variants now foreground the
>   wide-composition-space angle, but this one makes *composition-resolved model–experiment agreement* the
>   headline deliverable and casts the elemental-palette exploration as a test of where CALPHAD/AM-Module
>   predictions generalize — the ICME-native reading — rather than as one clause inside a workflow or
>   melt-pool-validation story.
> - **The whole thing is framed as one ICME loop** (properties → prediction → optimization → experiment →
>   calibration feedback), matching the symposium's ICME identity; the calibration-feedback sentence stays in
>   because closing the compute↔experiment loop *is* the ICME contribution here.
> - **The LLM agent is kept but demoted to one orchestration clause** — this room is AI-forward (unlike the
>   AM-Modeling committee, where it was dropped), so an agentic ICME-tool-orchestration layer reads as on-scope,
>   but Bayesian optimization / CALPHAD remain the substance.
> - **Transferability is retained** but sits after the composition story rather than leading it.

---

## Referenced version (with in-text citations)

> **Note:** carries in-text citations for the load-bearing factual claims (cross-machine
> non-transferability, transfer learning, Thermo-Calc AM Module printability maps, Bayesian/statistical LPBF
> optimization, and LLM/agentic AM systems). Citation markers push it over the ~150-word ProgramMaster box —
> use it only where references are allowed (proceedings manuscript, extended/poster abstract, internal review,
> grant blurb). Submit the [150-word version](#abstract-submission-version-150-words) to ProgramMaster.

Locking in laser powder bed fusion (LPBF) process parameters for a new powder still relies on large,
machine-specific parameter sweeps, and a recognized barrier to broader L-PBF adoption is that
parameter–property correlations are highly platform-specific and transfer poorly between machines and
environments [1,2]. Transfer-learning schemes are emerging to move process knowledge from an established source
machine to a target machine with different hardware while limiting the number of expensive tensile tests [1,3].
We present a processing-aware workflow that first computes alloy-specific printability maps — keyholing,
lack-of-fusion, and balling boundaries in power–speed space — using the Thermo-Calc AM Module, whose
CALPHAD-derived thermophysical properties predict melt-pool geometry and melting-mode transitions without
per-alloy property measurements [4,5]. Bayesian and statistical optimization then propose an efficient
experiment sequence within that physically informed prior, following established single-track-to-bulk LPBF
optimization practice in which laser power, scan speed, and hatch spacing govern melt-pool formation, density,
and mechanical properties [6,7,8]. We execute the campaign on an Aconity MIDI open-architecture system at the
University of Utah, climbing an escalating test ladder — single-track scans, density cubes, ISO/ASTM 52902
artifacts, and tensile bars — across a wide aluminum palette (AlSi10Mg baselines to lean, supply-chain-resilient
compositions), mapping where the CALPHAD-based predictions hold and where they break down in under-characterized
composition space, and we explicitly quantify how well an optimized window transfers across machines and across
instances of the same machine [2,3]. Finally, we pilot an
LLM-agent layer that drafts parameter sets, dispatches tool calls (printability and optimization), and helps
interpret characterization — building on recent demonstrations that large language models can predict LPBF
defect regimes from process parameters and reason over alloy printability through agentic, tool-calling
workflows [9,10].

**References**

1. Cross-platform laser powder bed fusion process–property modeling with active transfer learning.
   *ScienceDirect* (2025).
   [S152661252500605X](https://www.sciencedirect.com/science/article/abs/pii/S152661252500605X)
2. Transferability of process parameters in laser powder bed fusion processes for an energy- and cost-efficient
   manufacturing. *Sustainability* **12**(4), 1565 (2020).
   doi:[10.3390/su12041565](https://doi.org/10.3390/su12041565)
3. Knowledge transfer between machines in laser powder bed fusion — transfer learning with small training
   datasets. *Metals* **16**(4), 438 (2026).
   doi:[10.3390/met16040438](https://doi.org/10.3390/met16040438)
4. Thermo-Calc Additive Manufacturing (AM) Module — printability maps (keyholing / lack-of-fusion / balling)
   from CALPHAD thermophysical properties. See the repository review
   [`edison-trajectories/thermocalc_am_module.md`](edison-trajectories/thermocalc_am_module.md) and Thermo-Calc
   Software documentation.
5. Hosseini et al. Effect of laser parameters and melting modes in L-PBF of Al6061 evaluated with the Thermo-Calc
   AM Module (TCAl9); optimized window (44.64–50 J/mm³) → ~99% relative density (2025). (Summarized with citations
   in [`thermocalc_am_module.md`](edison-trajectories/thermocalc_am_module.md).)
6. A high-throughput approach for statistical process optimization in laser powder bed fusion.
   *Journal of Manufacturing Processes* (2025).
   [S1526612525004992](https://www.sciencedirect.com/science/article/abs/pii/S1526612525004992)
7. Understanding melt pool characteristics in laser powder bed fusion: an overview of single- and multi-track
   melt pools for process optimization. *ScienceDirect* (2023).
   [S2772834X23000295](https://www.sciencedirect.com/science/article/pii/S2772834X23000295)
8. Comprehensive study on statistical methods for optimization of process parameters and material properties of
   AlSi10Mg in laser powder bed fusion. *Discover Mechanical Engineering* (2024).
   doi:[10.1007/s44245-024-00073-4](https://doi.org/10.1007/s44245-024-00073-4)
9. AdditiveLLM: large language models predict defects in metals additive manufacturing.
   *arXiv* 2501.17784 (2025). [arXiv:2501.17784](https://arxiv.org/abs/2501.17784)
10. Agentic additive manufacturing alloy evaluation (MCP-based tool-calling for printability / lack-of-fusion
    maps). *arXiv* 2510.02567 (2025). [arXiv:2510.02567](https://arxiv.org/abs/2510.02567)

---

## Optional angle — Thermo-Calc AM-Module calibration feedback (documented, *not* committed in the submission abstract)

Per the [Thermo-Calc discussion transcript](thermocalc-discussion-transcript.md) (Thermo-Calc's account manager and a Thermo-Calc specialist, 2026-04-09)
and PR comment [#4870561417](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/101#issuecomment-4870561417),
there is a low-cost, high-leverage way to strengthen the Thermo-Calc partnership out of data this campaign *already
collects*:

- **The data is already in the test ladder.** The first rung — **single-track cross-sections** (melt-pool
  width/depth, defect onset) — is exactly the measurement Thermo-Calc uses to calibrate the AM Module. Feeding it
  back is a framing/positioning move, **not new experimental scope.**
- **It fixes the AM Module's known weak spot for aluminum.** Thermo-Calc's account manager flagged **absorptivity** as the module's
  biggest aluminum challenge: it computes liquid-phase absorptivity from an electrical-resistivity model with *no
  oxide film*, so users must apply an empirical pre-factor. The recommended calibration is precisely *"measure the
  melt-pool shape — do a cross section, give the boundary width and depth."* Running that across many
  power/speed points and multiple compositions yields a genuinely useful calibration/validation dataset.
- **It moves the partnership up the value ladder.** Thermo-Calc's main interest is
  **database/model-development work**, the one category they'd
  engage on more materially. Cross-section-driven absorptivity calibration (plus optional G/R equiaxed-transition
  and Scheil-based crack-susceptibility validation) is exactly that kind of case-study/database contribution, and
  both explicitly offered to write it into the **Letter of Support**.

**Recommendation (matches the "not requiring a change" note):** keep this **out of the 150-word submission
abstract** — it costs scarce words and would over-promise a validation collaboration that isn't yet formalized.
Instead, hold it for the **expanded / referenced / proceedings versions, the talk, and the FLAIME proposal /
Thermo-Calc Letter of Support**, where the space and the audience fit. A single, defensible, ready-to-drop-in
sentence for those longer versions:

> *Because the single-track cross-sections we collect (melt-pool width and depth versus laser power and scan
> speed) are exactly the measurements used to calibrate the Thermo-Calc AM Module's aluminum absorptivity, the
> same characterization doubles as a feedback dataset for validating and refining printability predictions across
> parameters and compositions.*

Framed this way it stays **honest** (something we *can* do with data in hand, not a promised result) and keeps the
abstract's reviewer-credibility posture intact.

---

## Composition emphasis — wide elemental palette & simulation reliability in new composition space

Per PI direction (2026-07-07), composition is promoted from an implicit "per powder" detail to a **co-headline of
the abstract**, for two reasons that reinforce each other and strengthen the novelty case rather than dilute it:

1. **A wide elemental palette is the FLAIME mission, not a side note.** The project exists to find
   *supply-chain-resilient* aluminum compositions — deliberately lean or off-standard alloys that sit *outside* the
   handful of commercial LPBF powders (AlSi10Mg, Scalmalloy, etc.) the field has parameter-qualified. Framing the
   campaign as "qualify one powder" undersells it; framing it as "qualify **across a broad composition space**"
   matches what we actually do and what distinguishes it from routine parameter tuning.

2. **New composition space is exactly where the simulation is least trustworthy — and saying so is a strength.**
   The Thermo-Calc AM Module's printability predictions inherit two composition-dependent uncertainties:
   - **CALPHAD database coverage.** Thermophysical properties are most reliable near well-assessed alloys;
     extrapolating to novel multicomponent / lean-Al chemistries carries growing uncertainty in the very inputs
     (thermal conductivity, heat capacity, solidus/liquidus, surface tension) that set melt-pool geometry.
   - **Aluminum absorptivity.** Per the [Thermo-Calc transcript](thermocalc-discussion-transcript.md), absorptivity
     is computed from a liquid-phase electrical-resistivity model with *no oxide film*, so it needs an empirical,
     composition-sensitive pre-factor calibrated from melt-pool cross-sections.

   Rather than hide this, the abstract makes **"where do the physics-based predictions hold, and where do they
   break down as composition moves into under-characterized space?"** an explicit, measured deliverable. This is
   honest (it matches the reviewer-credibility posture in the rest of the doc), scientifically interesting (a
   *composition-space envelope of trust* for CALPHAD-seeded printability maps is genuinely novel), and it converts
   a limitation into a contribution — the wider the palette we probe, the more valuable the resulting map of model
   reliability, and the more useful the [cross-section calibration-feedback loop](#optional-angle--thermo-calc-am-module-calibration-feedback-documented-not-committed-in-the-submission-abstract)
   that pushes the envelope outward.

**Where this lands hardest.** The composition-space-reliability angle is *most* at home in the
[*AM Modeling, Simulation & AI* variant](#alternate-submission-version--am-modeling-simulation--ai-symposium-simulation-forward-147-words),
where model validation is the room's native language — "we map the composition envelope over which the AM Module
can be trusted" reads as a headline model-generalization result there. It is retained (more compactly) in the
[AI-Enabled version](#abstract-submission-version-150-words) and expanded in the
[expanded](#expanded--alternate-version-leans-harder-into-the-ai--transfer-story) and
[referenced](#referenced-version-with-in-text-citations) versions.

> **Honesty guardrail (unchanged posture):** keep the claim framed as *"we map where predictions hold and break
> down"* — an open question we measure — not *"the AM Module fails for lean alloys,"* which would over-claim a
> result before the data is in. The Edison [literature-high report](edison-trajectories/tms-2027-lpbf-parameter-abstract-review/edison-literature-high-report.md)
> already supports the enabling caveat that identical volumetric energy density yields different defect regimes
> across conditions, i.e. property/composition detail matters beyond simple scaling.

---

## Symposium selection (TMS 2027)

**✅ Selected — submitting here (Oral Presentation):**

1. **AI-Enabled Materials Processing: Integrating Accelerated Experimental Workflows and Processing-Aware
   Machine Learning.**
   Strongest fit. The abstract's core contribution — an *accelerated experimental workflow* (Thermo-Calc
   prior → Bayesian optimization → escalating physical test ladder on the Aconity MIDI) driven by
   *processing-aware ML*, plus an LLM-agent layer — is essentially the symposium's title restated for LPBF.
   The audience is exactly the processing-aware-ML community whose feedback we want, and it lets us lead with
   the AI/optimization and cross-machine-transfer story rather than with metallurgy alone.

**Strong alternatives (pick based on how the talk is framed):**

2. **Artificial Intelligence Applications in Integrated Computational Materials Engineering (AI-ICME).**
   Strongest *topical* fit for the Thermo-Calc-forward story: the workflow **is** an ICME pipeline
   (CALPHAD properties → AM Module printability prediction → Bayesian optimization → experiment → calibration
   feedback), and no FLAIME talk is in this room yet. A **composition-forward** 150-word abstract for it is
   drafted above: [*AI-ICME* submission version](#alternate-submission-version--ai-icme-symposium-composition-forward-icme-loop-150-words).
   Organizer note ([PR #101](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/101#issuecomment-4870800010)):
   a CALPHAD-native, DOE-lab + industry committee (Pilania/GE Aerospace, Devanathan/PNNL, Mishra/LANL, Miller/UF),
   so the variant foregrounds **how CALPHAD/AM-Module predictions hold up in new regions of composition space** and
   the compute↔experiment feedback loop — the axis this audience rewards most.

3. **Additive Manufacturing Modeling, Simulation, and Artificial Intelligence: Microstructure, Mechanics, and
   Process.**
   Best fit if we lead with the *simulation* side — Thermo-Calc AM Module printability maps and melt-pool
   modeling validated against single-track / density-cube data — and treat ML as the glue. A deeper, more
   AM-modeling-native room; slightly less emphasis on the closed-loop experimental-workflow angle. A tuned,
   simulation-forward 150-word abstract for this room is drafted above:
   [*AM Modeling, Simulation & AI* submission version](#alternate-submission-version--am-modeling-simulation--ai-symposium-simulation-forward-150-words).
   Organizer note ([PR #101](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/101)): this
   committee is **defense-funding-dense** (an ONR AM program officer, ARL, and JHU-APL), so the simulation-forward
   variant deliberately foregrounds model validation / reliability and the Thermo-Calc physics engine over the
   LLM-agent layer.

4. **Additive Manufacturing and Innovative Feedstock Processing for Multifunctional Materials.**
   Best fit if we frame the talk as *feedstock-to-print qualification* and pair it directly with the companion
   ultrasonic-atomization abstract (per-powder-type parameter optimization as the bridge from novel feedstock
   to qualified parts). Emphasizes powder → parameter → property over AI methodology.

**Decision:** Symposium 1 (AI-Enabled Materials Processing) is documented as the original target; the
**AI-ICME** (#2) and **AM Modeling/Sim/AI** (#3) rooms are the two computationally-forward alternatives now
carrying tuned abstract variants (composition-forward and simulation-forward, respectively). Pick one lane —
submitting the same abstract to more than one symposium is discouraged by TMS. Mock organizer reviews for the
AM-Modeling and AI-ICME variants are being run via Edison (see
[`edison-trajectories/tms-2027-lpbf-parameter-abstract-review/`](edison-trajectories/tms-2027-lpbf-parameter-abstract-review/)).

> **Coordination note:** this and the companion **atomization** abstract ([#98](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/98))
> deliberately target *different* symposia (AI-Enabled Materials Processing here vs. the Honoring-Iver-Anderson
> atomization symposium there), so the two halves of the powder-to-part loop reach two distinct audiences
> without self-competition.

---

## Pre-submission checklist (per TMS abstract guidelines)

- [x] Confirm final author list and order — set per PI direction (2026-07-02): **Carl Robison (first)**, Ronnie
      Guymon, Xavier Zaitzeff, Gage Erickson, Alik Nielsen (U of Utah Mech Eng), Ashley Spear (U of Utah Mech Eng),
      Sterling Baird. **Still verify:** presenting author, affiliations/emails, the "Spear" vs. "Speer" spelling,
      and whether Taylor Sparks (Letter-of-Support partner) should also be a co-author or acknowledged.
- [x] Choose oral vs. poster preference. — **Oral Presentation.**
- [x] Select target symposium. — **AI-Enabled Materials Processing: Integrating Accelerated Experimental
      Workflows and Processing-Aware Machine Learning.**
- [x] Trim to the symposium's word limit (TMS abstracts are typically ~150 words / 1500 characters). —
      AI-Enabled submission version is **150 words**; the *AM Modeling, Simulation & AI* variant is **147 words**
      (both ≤150, per `wc -w`).
- [x] Lead with the AI/workflow contribution (fits the symposium) and state a concrete, results-oriented takeaway
      (data-driven processing windows + experimental-budget accounting + cross-machine transfer evidence).
- [x] Keep claims defensible for an early-stage group: "pilot an LLM-agent layer" (not a finished system),
      "test how well a window transfers" (an open question we measure, not a solved result), and avoid quoting a
      specific density/parameter number before the data is in.
- [x] Decide whether to name a lead powder/alloy explicitly (e.g., AlSi10Mg baseline + one lean Al composition)
      or keep it powder-type-agnostic. — **Named, per PI direction (2026-07-07):** both submission versions now
      foreground the **wide aluminum elemental palette** (AlSi10Mg baseline → lean, supply-chain-resilient
      compositions) and the **composition-space reliability of the simulation** as an explicit, measured result.
      See [Composition emphasis](#composition-emphasis--wide-elemental-palette--simulation-reliability-in-new-composition-space).
- [ ] Note FLAIME / DOE funding acknowledgement if required by the program.
- [ ] Verify the symposium is accepting abstracts and check the submission deadline on ProgramMaster.
- [ ] (Optional) Run the actual Edison Scientific LITERATURE_HIGH query in
      [`edison-trajectories/tms-2027-lpbf-parameter-abstract-review/literature-scoping.md`](edison-trajectories/tms-2027-lpbf-parameter-abstract-review/literature-scoping.md)
      to deepen the transferability / LLM prior-art review beyond the web-search scoping done here.

## Scoping and mock-organizer review

The literature scoping for this abstract (what the campaign entails, and prior work on parameter tuning,
cross-machine/instance transfer, ML/AI optimization, and LLM/agentic approaches) and the mock symposium-organizer
review are in
[`edison-trajectories/tms-2027-lpbf-parameter-abstract-review/`](edison-trajectories/tms-2027-lpbf-parameter-abstract-review/)
([literature scoping](edison-trajectories/tms-2027-lpbf-parameter-abstract-review/literature-scoping.md),
[round 1](edison-trajectories/tms-2027-lpbf-parameter-abstract-review/round1-organizer-feedback.md),
[round 2](edison-trajectories/tms-2027-lpbf-parameter-abstract-review/round2-organizer-feedback.md)).

> **Method note (transparency):** the issue asked to "send an Edison Scientific search." The Edison
> Scientific / PaperQA3 pipeline is not available from this automated environment, so the scoping below was
> built with live **web search** (WebSearch/WebFetch) instead, and the mock organizer review role-plays the
> symposium's stated scope rather than named, verified organizers. A ready-to-paste Edison `LITERATURE_HIGH`
> prompt is included in the scoping doc so the deeper query can be run manually to match the depth of the other
> `edison-trajectories/` reports.
