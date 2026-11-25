# MS&T '26 — Additional Symposia and Candidate Abstracts

Follow-up to [#79](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/issues/79)
("Prepare abstract for MS&T '26"), which targets the *Autonomous Synthesis and
Characterization: Experiments and Digital Twins for Theory-Enhanced
Self-Driving Laboratories of the Future* symposium organized by Yongtao Liu et
al. (ACerS Basic Science Division).

This document proposes **six additional candidate talks**, each scoped to a
different sub-area of the vertical-cloud-lab / FLAIME / digital-wetlab program
and matched to a specific MS&T '26 symposium drawn from the list circulated in
the parent issue. Titles and 4–6 sentence abstracts are first-draft and
intended for Edison-Scientific persona review (per the workflow established in
#79) and PI sign-off before any are submitted via ProgramMaster.

For each entry: **Symposium →** the MS&T '26 host symposium, **Lead workstream
→** the corresponding internal repository / project, **Suggested speaker →**
TBD pending PI assignment.

Per the portal rules surfaced in [#80](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/80)
(also applicable to ACerS-hosted symposia at MS&T '26): each abstract is
capped at **150 words**, titles use **sentence case**, the submission text
takes **no hard returns** (lines wrap naturally), and any special characters
or italics/sub-/superscripts are entered with the portal's `\####;`-style
codes. The drafts below already meet the word cap and use sentence-case
titles; portal-ready single-paragraph versions with character-code
substitutions can be derived per submission, in the same style as
`conference-abstracts/mst26/submission.txt` from #80.

---

## 1. BOFN-specific talk

- **Symposium:** [Additive Manufacturing Modeling, Simulation, and Machine
  Learning: Microstructure, Mechanics, and
  Process](https://www.programmaster.org/PM/PM.nsf/UpcomingSymposia/12CC01C3171EE1BE85258CAB0057886E?OpenDocument)
- **Lead workstream:** [`bofn-llm-bo-synthesis.md`](./bofn-llm-bo-synthesis.md),
  [`benchmarks/bofn_pkgfn_demo.py`](./benchmarks/bofn_pkgfn_demo.py),
  [`benchmarks/bofn_llm_warmstart.py`](./benchmarks/bofn_llm_warmstart.py)
- **Title:** *Bayesian optimization of function networks for composition–
  process–microstructure–property pipelines in laser powder bed fusion*

**Abstract** (≈140 words). Closed-loop alloy design for additive
manufacturing typically treats the composition-to-property map as a single
black-box objective, leaving information about intermediate atomization,
LPBF processing, and microstructural responses unused by the acquisition
function. We apply Bayesian Optimization of Function Networks (BOFN) to the
full critical-mineral-lean Al-alloy pipeline, modeling CALPHAD-derived
solidification descriptors, particle-packing surrogates, and post-build
microstructural metrics as composable Gaussian-process nodes whose
intermediate observations are explicitly conditioned on. Initial synthetic
results comparing pKGFN with TS-FN on a particle-packing function-network
benchmark seeded with public Zenodo datasets and a CrabNet composition
emulator motivate an upcoming flat-BO regret comparison against vanilla
qNEI. We further outline how LLM-generated proposals can be fused with the
BOFN posterior as a structured prior in the cold-start regime, and close
with open challenges around heteroskedastic noise on intermediate nodes and
exposing function-network structure to self-driving-lab schedulers.

---

## 2. Atomization-workflow talk

- **Symposium:** [Additive Manufacturing: Development of
  Powders](https://www.programmaster.org/PM/PM.nsf/UpcomingSymposia/C8ED22C6E0AB6FD685258CAB00611756?OpenDocument)
- **Lead workstream:** AMAZEMET ultrasonic-atomization integration, Valimet
  collaboration
- **Title:** *Closing the loop on ultrasonic atomization: active-learning
  process maps for on-demand aluminum-alloy powders*

**Abstract** (≈140 words). Ultrasonic atomization platforms such as the
AMAZEMET rePOWDER make it feasible to produce gram- to kilogram-scale lots
of non-standard, critical-mineral-lean aluminum alloys, but mapping the
composition × frequency × power × atmosphere space is prohibitive when each
lot must be sieved, imaged, and rheologically characterized before LPBF
qualification. We describe an autonomous atomization-to-LPBF workflow in
which composition is co-optimized with atomization parameters under yield,
particle-size-distribution, and flowability constraints, using multi-
fidelity Bayesian optimization that treats SEM morphology and Hall-flow
measurements as cheap-but-biased proxies for printability. Baseline
atomization data on candidate compositions screened with the Thermo-Calc
TCAl10 database and AM Module are in hand; the active-learning loop is
being staged for first campaign runs and is expected to reach a Pareto
front substantially faster than one-factor-at-a-time. We close with the
provenance spine that links atomizer, sieving station, and morphology
pipeline to the optimizer.

---

## 3. Automated powder-dispensing and generative-CAD talk

- **Symposium:** [Additive Manufacturing: Equipment, Instrumentation and
  In-Situ Process
  Monitoring](https://www.programmaster.org/PM/PM.nsf/UpcomingSymposia/DAE6A6CD0A45F7A885258D1D006A0C17?OpenDocument)
- **Lead workstream:** automated powder dispensing, generative CAD for
  dispenser hardware
- **Title:** *Generative CAD and robotic powder dispensing for high-
  throughput composition libraries: hardware, calibration, and closed-loop
  operation*

**Abstract** (≈140 words). Combinatorial alloy discovery is bottlenecked
less by optimization algorithms than by the tedious physical step of
accurately dispensing milligram-to-gram quantities of multiple elemental
powders into hundreds of crucible positions per day. We describe a
developing automated powder-dispensing cell in which end-effectors,
hoppers, and tip geometries are produced by a generative-CAD pipeline that
takes powder rheology, particle size, and target dispense mass as inputs
and emits printable STL files together with a calibration recipe. The
planned closed loop pairs vision-plus-load-cell feedback with the
generative-CAD layer so that hardware geometry, not just dispense
kinematics, can be tuned per powder across materials that differ in
flowability by more than an order of magnitude. We share initial dispensing
demonstrations and a roadmap for composition libraries feeding arc-melting,
ultrasonic atomization, and ink-based deposition, together with the failure
modes — cohesive clumping, electrostatic carry-over, tip wear — that
motivate the generative-CAD layer.

---

## 4. Digital-wetlab talk

- **Symposium:** [18th Symposium on Green and Sustainable Technologies for
  Materials Manufacturing and
  Processing](https://www.programmaster.org/PM/PM.nsf/UpcomingSymposia/A710C21C1069E55A85258CA000520F4B?OpenDocument)
- **Lead workstream:**
  [`vertical-cloud-lab/digital-wetlab`](https://github.com/vertical-cloud-lab/digital-wetlab)
  (chemical reasoning agents, liquid-handling automations,
  petroleum-focused research)
- **Title:** *Chemical-reasoning agents and automated liquid handling for
  sustainable petroleum-adjacent materials workflows*

**Abstract** (≈140 words). Sustainable processing of petroleum-derived
feedstocks — upcycled polymers, asphaltene-rich residues, bio-derived
substitutes — requires structured screens of catalysts, solvents, and
reaction conditions that are awkward in conventional DOE software but
natural for an LLM-backed chemical-reasoning agent. We describe a digital-
wetlab architecture in which an agent decomposes a high-level objective
("maximize aromatic conversion at minimum solvent intensity") into
structured reaction templates, dispatches them to commercial liquid-
handling robots through a shared device-abstraction layer, and ingests the
resulting GC, NMR, and gravimetric data into a typed knowledge graph that
informs the next round of proposals. We highlight three case studies from
active branches of the `digital-wetlab` repository: agent-guided solvent
down-selection for a petroleum-adjacent extraction, autonomous re-running
of failed reactions with chemically motivated parameter adjustments, and
integration hooks for sharing campaigns with a metals self-driving lab on
the same orchestration spine.

---

## 5. Echem-cell talk

- **Symposium:** [Energy Materials for Sustainable
  Development](https://www.programmaster.org/PM/PM.nsf/UpcomingSymposia/43A5F6B73452B1F685258C9A002D6C4D?OpenDocument)
- **Lead workstream:**
  [`AccelerationConsortium/echem-cell`](https://github.com/AccelerationConsortium/echem-cell)
  hardware and electrochemistry-AI integration
- **Title:** *Open hardware and AI-driven electrochemistry for accelerated
  electrode and electrolyte discovery*

**Abstract** (≈140 words). Reproducible, AI-ready electrochemical
characterization is constrained by a long tail of bespoke cell designs,
idiosyncratic potentiostat drivers, and brittle data-analysis scripts that
prevent results from one lab being directly consumed by another. We present
recent progress on the open-source `echem-cell` platform — a low-cost,
modular three-electrode cell with documented CAD, BOM, and assembly
procedure — and its integration with a self-driving electrochemistry
orchestrator that selects voltammetric sequences, EIS sweeps, and rest
steps based on online posterior estimates of diffusivity, exchange current,
and degradation rate. The same hardware/software pair has been used for
both electrode-coating lifecycle testing and rapid electrolyte-additive
screening, with raw waveforms, provenance metadata, and inferred
descriptors flowing into a shared schema suitable for downstream Bayesian
optimization. We discuss calibration and standardization challenges when
many copies run in parallel across institutions, and close with priorities
for an open electrochemistry-AI ecosystem.

---

## 6. Vertical-cloud-lab concept talk (VLM-centric)

- **Symposium:** [Autonomous Synthesis and Characterization: Experiments and
  Digital Twins for Theory-Enhanced Self-Driving Laboratories of the
  Future](https://www.programmaster.org/PM/PM.nsf/UpcomingSymposia/ACB5B3037005D69F85258CA500291AF1?OpenDocument)
  *(same symposium as the parent #79 talk, but a distinct, hardware-centric
  contribution; can be repointed to "Applied Machine Learning in ICME
  Frameworks on Ceramics and Glassworks" if a single-talk-per-symposium rule
  applies)*
- **Lead workstream:**
  [`vertical-cloud-lab`](https://github.com/vertical-cloud-lab#vertical-automation)
  — vertical-automation thrust built around a **vertical lift module (VLM)**
  that brings synthesis and characterization equipment to a single
  human/robot workstation, paired with cloud experimentation and frugal twins
- **Title:** *Vertical lift modules as the backbone of self-driving
  materials labs: trading floor space for throughput in autonomous
  synthesis and characterization*

**Abstract** (≈135 words). Most self-driving-lab demonstrations are
organized *horizontally* — a row of instruments along a long robot track —
which spends lab floor space on aisles and forces every new instrument to
negotiate its own integration. We argue instead for a **vertical**
organizing principle with a vertical lift module (VLM) at the center: an
"electrified" multi-tray tower that brings synthesis and characterization
equipment to a single human-or-robot workstation in tens of seconds,
recovering several-fold more automation-friendly footprint. We describe
how this hardware spine integrates with the broader vertical-cloud-lab
program — cloud experimentation exposing VLM-resident equipment for
remote, quota-based access, and frugal twins such as AMPERE-2 that let
operators rehearse experiments on low-cost copies before committing
production trays. We close with design choices that surface once a VLM is
a first-class scheduler resource: tray topology, vibration and thermal
isolation, a device-abstraction layer, and provenance hooks for cross-tray
audit trails.

---

## Suggested next steps

1. Run each abstract through the Edison-Scientific persona-review workflow
   established in #79 (organizers + likely audience members for the chosen
   symposium), and revise.
2. Confirm with PI which talks to actually submit (avoid over-committing —
   each accepted talk implies a presenter and travel).
3. For any abstract that is greenlit, mirror the relevant workstream branch
   into a focused write-up and prepare the ProgramMaster submission.
4. Track acceptances and presenter assignments in a follow-up issue or in
   `edison-trajectories/venues.md`.
