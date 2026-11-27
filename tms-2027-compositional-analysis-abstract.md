# TMS 2027 Abstract — CALIBER: A Retrieval-Augmented, Uncertainty-Aware Platform for Selecting High-Fidelity Characterization Parameters for Novel Alloys

**Title (submission):** CALIBER: A Retrieval-Augmented, Uncertainty-Aware Platform for Selecting High-Fidelity Characterization Parameters for Novel Alloys

**Platform name:** **CALIBER** — a plain word (no forced acronym) whose every association fits a metrology platform: *caliber* is a measurement term, *high-caliber* evokes the high-fidelity target, and it echoes *calibrate* (what the ICP-MS/MS-benchmarked loop does). See the [naming note in the draft file](tms-2027-compositional-analysis-abstract-draft.md#platform-name) for alternatives (SETPOINT, SAGE, COMPASS, METIS).

**Prior working title (superseded):** Closing the Loop on Characterization Setup: A Physics- and Literature-Grounded System for Selecting High-Fidelity SEM/EDS/EBSD/XRD/XRF Parameters for Additively Manufactured Alloys

**Authors (all Brigham Young University unless noted):**

| Author | Email | Role |
| --- | --- | --- |
| Ronnie Guymon | [student email removed] | Presenting author |
| Gage Erickson | [student email removed] | Co-author |
| Xavier Zaitzeff | [student email removed] | Co-author |
| Carl Robison | [student email removed] | Co-author |
| Sterling Baird | sterling.baird@byu.edu | Corresponding author / PI |

> **Author list needs confirmation.** Ronnie Guymon leads this thread (per issue #102 and byu-vcl#95), so he is listed as presenting author. Consider adding BYU microscopy-facility staff (e.g., **Mike Standing**, **Paul** — EBSD/SEM setup expertise repeatedly credited in byu-vcl#95) as co-authors or in the acknowledgements, and confirm whether a University of Utah / Utah Nanofab collaborator belongs on the list.

**Meeting:** TMS 2027 Annual Meeting & Exhibition, March 14–18, 2027, Orlando, FL
**Presentation preference:** Oral Presentation
**Symposium (current decision):** **AI/ML/Data Informatics for Materials Discovery: Bridging Experiment, Theory, and Modeling** — Flyer **022**. Updated 2026-07-13: Ronnie (presenting author) is aligning to 022 after learning Carl is submitting to **AI-ICME (Flyer 024)** — routing Ronnie to 022 (where @sgbaird holds an invited talk) de-conflicts the two BYU abstracts and gives the group two rooms. AI-ICME (024) remains the fallback. Both ranked top-2 across the whole 106-symposium sweep (022 #1, 024 #2). The earlier "Novel Strategies for Rapid Acquisition and Processing of Large Datasets" candidate is **superseded** (fit downgraded — see [Symposium selection](#symposium-selection-tms-2027)).
**Abstract submission:** Via [ProgramMaster](https://www.programmaster.org/TMS2027) ([TMS 2027 technical program](https://www.tms.org/TMS2027/TMS2027/Programming/TMS2027_Technical_Program.aspx))

> **Ronnie's submission-candidate draft (v4, 022-tailored) lives in [`tms-2027-compositional-analysis-abstract-draft.md`](tms-2027-compositional-analysis-abstract-draft.md)** — inlaid from issue #102 and reframed for Flyer 022 (v3 AI-ICME framing kept there as the fallback). That file holds the version closest to submission; the versions below are the earlier system-forward framings kept for reference and reuse.

> Context: part of the FLAIME project on AI-guided, supply-chain-resilient aluminum alloy discovery for additive manufacturing. This is the **characterization / metrology** companion to the ultrasonic-atomization abstract (#98, *making* the powder) and the LPBF process-parameter abstract (#100, *printing* the part). This one covers *measuring* what was made — closing the powder → print → **characterize** loop. Led by Ronnie Guymon. Grounded in the SEM/EDS/EBSD compositional-analysis work in [byu-vcl#95](https://github.com/vertical-cloud-lab/byu-vcl/pull/95).

---

## Abstract (submission version, 144 words)

High-fidelity compositional and microstructural analysis of additively manufactured aluminum is
bottlenecked less by the instruments than by how they are configured: standardless SEM-EDS routinely
over-reports trace Mg in AlSi10Mg by several-fold, and EBSD indexing of laser-powder-bed-fusion Al–Si
collapses without an adequate beam current and phase model. We are building a closed-loop system that
recommends and iteratively refines acquisition parameters across SEM, EDS, EBSD, XRD, and XRF for a
given sample and analysis goal. Recommendations are grounded in three sources of truth: retrieval over
characterization standards and texts (e.g., ASTM E1508, E2627), electron-beam and interaction-volume
simulation, and an accumulating, provenance-tracked dataset of parameter sweeps that functions as
in-house "standards." We validate on commercial and supply-chain-resilient aluminum powders and prints,
benchmarking EDS/XRF composition against orthogonal ICP-MS/MS. We report emerging parameter–fidelity
relationships and describe a labeled characterization dataset intended to make expert instrument setup
reproducible and transferable.

---

## Expanded / alternate version (leans harder into the dataset + agentic decision-support)

Quantitative compositional and microstructural characterization of metal additive-manufacturing (AM)
feedstock and parts is gated by tacit, operator-dependent choices — beam energy and current, live time,
amplifier time constant, working distance, phase list, cleanup filters, standards — that are rarely
documented with enough provenance to reproduce or transfer between instruments. The cost is concrete: in
our own laboratory, standardless eZAF quantification reported Mg in AlSi10Mg at roughly 1.4–1.6 wt%
against a 0.2–0.45 wt% nominal (a several-fold overestimate that persisted even after metallographic
polishing removed surface oxide), traced to the Mg Kα / Al Kα overlap and background modeling near
1–2 keV; and EBSD confidence-index yield on LPBF AlSi10Mg jumped from ~40% to ~77% of points above
CI = 0.1 once the beam current was raised from 1.6 to 6.4 nA and a custom AlSi10Mg (plus diamond-cubic
Si) phase model was loaded. We are building a closed-loop, agentic decision-support system that, given a
sample and an analysis goal, proposes and then iteratively refines acquisition and processing parameters
across SEM, EDS, EBSD, XRD, and XRF. Three grounding sources keep the recommendations defensible:
(1) retrieval-augmented generation over characterization sources of truth — ASTM standards
(E1508 for EDS, E2627 for EBSD grain size, E1097/E3061 for ICP), microanalysis texts, and instrument
SOPs; (2) physics-based simulation of the electron beam and interaction volume (e.g., Monte Carlo /
φ(ρz) estimates of sampling depth and the beam current needed for adequate EBSD pattern quality without
excess carbon deposition); and (3) an accumulating, fully provenance-tracked dataset of systematic
parameter sweeps on well-characterized samples, so that the lab effectively grows its own labeled
"standards" describing how each parameter shifts measured composition and indexing quality. We validate
on a commercial anchor composition (AlSi10Mg) and lean, supply-chain-resilient aluminum alloys, in both
gas-/ultrasonically-atomized powder and LPBF-printed form, benchmarking EDS/XRF composition against an
orthogonal bulk technique (ICP-MS/MS on an Agilent 8900). We report emerging parameter–fidelity
relationships, discuss where automated recommendation already matches expert setup and where a human
still wins, and describe a labeled characterization-parameter dataset — with full sample provenance —
intended as a shareable resource for the metal-AM compositional-analysis community.

---

## Referenced version (with in-text citations)

> **Note:** This version carries in-text citations for the load-bearing factual claims (autonomous /
> AI-assisted characterization, SEM beam auto-optimization, LLM/agentic microscopy, standardless-EDS
> error, EBSD standards). The citation markers push it over the ProgramMaster word limit, so submit the
> [144-word version](#abstract-submission-version-144-words) to ProgramMaster and reserve this version
> for a proceedings manuscript, extended/poster abstract, internal review, or a grant/report blurb. All
> references are real, peer-reviewed or preprint sources (DOIs / arXiv IDs below).

Quantitative compositional and microstructural characterization of additively manufactured aluminum is
gated less by hardware than by operator-dependent acquisition choices, and the community is actively
asking how far AI can close that gap — often with more aspiration than delivery [1]. Autonomous and
AI-assisted microscopy has begun to automate individual pieces: SEM beam optimization via beam-kernel
estimation [2], expert-knowledge-guided and active-learning acquisition [3,4], and LLM/agentic control
of microscopes and their workflows [5,6,7]. What is missing for metal AM is a system that spans
*modalities* (SEM, EDS, EBSD, XRD, XRF) and is *grounded* in characterization standards and physics
rather than pixels alone. The need is concrete in our own data: standardless eZAF over-reported Mg in
AlSi10Mg by several-fold relative to nominal, consistent with the Mg Kα / Al Kα overlap and
soft-X-ray background modeling that standardless routines handle poorly [8,9]; and EBSD confidence-index
yield on LPBF Al–Si rose sharply once beam current and the phase model were corrected, consistent with
the reporting and cleanup conventions of ASTM E2627 [10]. We are building a closed-loop system that
recommends and iteratively refines parameters across all five modalities for a given sample and goal,
grounded in (1) retrieval over standards and texts (ASTM E1508 for EDS [8], E2627 for EBSD [10]),
(2) electron-beam and interaction-volume simulation, and (3) an accumulating, provenance-tracked dataset
of parameter sweeps acting as in-house standards. We validate on commercial (AlSi10Mg) and
supply-chain-resilient aluminum, in powder and printed form, benchmarking EDS/XRF against orthogonal
ICP-MS/MS, and release a labeled characterization dataset to make expert setup reproducible and
transferable.

**References**

1. E. A. Stach et al. "Mind the Gap: Bridging the Divide Between AI Aspirations and the Reality of
   Autonomous Characterization." *arXiv* 2502.18604 (2025).
   [arXiv:2502.18604](https://arxiv.org/abs/2502.18604)
2. Automatic beam optimization method for scanning electron microscopy based on electron beam kernel
   estimation. *Communications Engineering* **3**, (2024).
   doi:[10.1038/s44172-024-00230-3](https://doi.org/10.1038/s44172-024-00230-3)
3. Mic-hackathon 2024: Hackathon on Machine Learning for Electron and Scanning Probe Microscopy.
   *arXiv* 2506.08423 (2025). [arXiv:2506.08423](https://arxiv.org/abs/2506.08423)
4. "Scientific Exploration with Expert Knowledge (SEEK) in Autonomous Scanning Probe Microscopy with
   Active Learning." *arXiv* 2408.02071 (2024). [arXiv:2408.02071](https://arxiv.org/abs/2408.02071)
5. TEM Agent: enhancing transmission electron microscopy (TEM) with modern AI tools. *arXiv* 2511.08819
   (2025). [arXiv:2511.08819](https://arxiv.org/abs/2511.08819)
6. Evaluating large language model agents for automation of atomic force microscopy. *Nature
   Communications* **16**, (2025).
   doi:[10.1038/s41467-025-64105-7](https://doi.org/10.1038/s41467-025-64105-7)
7. "Synergizing Human Expertise and AI Efficiency with Language Model for Microscopy Operation and
   Automated Experiment Design." *arXiv* 2401.13803 (2024).
   [arXiv:2401.13803](https://arxiv.org/abs/2401.13803)
8. ASTM E1508-12a. "Standard Guide for Quantitative Analysis by Energy-Dispersive Spectroscopy." ASTM
   International. doi:[10.1520/E1508-12A](https://doi.org/10.1520/E1508-12A)
9. J. Goldstein et al. *Scanning Electron Microscopy and X-Ray Microanalysis*, 4th ed. Springer (2018).
   doi:[10.1007/978-1-4939-6676-9](https://doi.org/10.1007/978-1-4939-6676-9)
10. ASTM E2627-13. "Standard Practice for Determining Average Grain Size Using Electron Backscatter
    Diffraction (EBSD) in Fully Recrystallized Polycrystalline Materials." ASTM International.
    doi:[10.1520/E2627-13](https://doi.org/10.1520/E2627-13)

---

## Symposium selection (TMS 2027)

> **⚠️ Deadline note:** The [TMS 2027 CFA flyer](https://www.tms.org/tms2027/downloads/flyers/TMS2027-CFA-Flyer-012.pdf)
> lists **Abstract Submissions Due July 1, 2026** for this symposium. As of the current review (2026-07-07)
> that date has **passed**. Before doing anything else, confirm on ProgramMaster whether the deadline was
> extended or whether a late/rolling submission is possible — otherwise this target is moot for TMS 2027 and
> the work should be re-aimed at a 2028 meeting or a different venue.

The three abstracts in this repo are deliberately routed to **three different symposia** so the powder →
print → characterize story reaches three distinct audiences (atomization in #98, printing in #100,
characterization here). This section was **reassessed against the actual CFA flyer** (organizers, scope, and
topic list below), and the earlier "near-literal fit" claim is **downgraded** — see the honest fit read.

### What the symposium actually asks for (from the CFA flyer)

*"Novel Strategies for Rapid Acquisition and Processing of Large Datasets From Advanced Characterization
Techniques"* — Advanced Characterization Methods track, **TMS Structural Materials Division**, sponsored by
the **Advanced Characterization, Testing, and Simulation Committee**. The scope centers on **large datasets**
produced by **multiscale, high-throughput, autonomous, and in-situ** characterization, and the **rapid /
efficient** extraction of actionable microstructural information from them. Named techniques emphasize
OM, SEM, **S/TEM, neutron and synchrotron X-ray, APT, and XCT**. The five topic bullets are: (1)
high-throughput characterization for rapid discovery; (2) ML/AI **real-time or post-facto reduction of
high-volume datasets acquired during in-situ** microstructure-evolution studies; (3) **FAIR** curation of
large characterization metadata; (4) accelerated feature extraction from large imaging/spectroscopy/
diffraction datasets via CV/ML; (5) **on-the-fly** data extraction and feedback for AM via **in-situ
monitoring**.

### Organizing committee (personas, for reviewer-fit)

| Organizer | Affiliation | Research persona | Likely stance on this abstract |
| --- | --- | --- | --- |
| **Sriram Vijayan** | Michigan Tech | *In-situ* TEM of far-from-equilibrium phenomena, phase transformations, MEMS in-situ heating, AM emulation in the TEM | Cool — wants **dynamic, time-resolved** evolution; ours is static/ex-situ |
| **Rakesh Kamath** | Argonne (APS) | Synchrotron X-ray scattering, **large-dataset curation, FAIR-izing** synchrotron data | Warm *only* on the provenance/FAIR dataset angle; cool on lab-scale SEM/EDS scope |
| **Fan Zhang** | NIST | Multiscale synchrotron USAXS/SAXS/WAXS, **in-situ metrology of far-from-equilibrium AM**, structural metrology & standards | Respects the metrology rigor; scope is synchrotron/in-situ, not benchtop |
| **Austin McDannald** | NIST | **Autonomous experimentation**, physics-informed ML / Bayesian active learning, closed-loop control (ANDiE, Hermes, AMASE) | **Most sympathetic** — our recommend-and-refine loop is close to his active-learning acquisition work |
| **Sarshad Rommel** | UConn (Aindow group) | **Al alloys for AM**, powder-processed Al, SEM/EDS/FIB/HRTEM/STEM/XRD, corrosion | Closest to our **material system**; ally on sound Al microanalysis |

### Honest fit read (downgraded from "near-literal")

The central tension @sgbaird flagged is real. This symposium is about **processing LARGE datasets from
RAPID / HIGH-THROUGHPUT / AUTONOMOUS / IN-SITU** acquisition. Our thesis is closer to **"collect *less*
data, more intentionally"** — choosing high-fidelity acquisition parameters up front for **ex-situ, static**
compositional/microstructural metrology. Those are nearly inverse framings: the symposium presumes you are
*drowning in* data and need to reduce it fast; we argue for acquiring the *right* data deliberately.

**Two of five organizers (Vijayan, Fan Zhang) and much of the scope emphasis are in-situ / synchrotron /
big-data — not our lane.** The honest overlaps are narrower:

- **The active-learning bridge (McDannald).** "Autonomous / active-learning-driven acquisition to collect
  the *right* data efficiently" *is* legitimately in-scope — it is exactly what ANDiE does (reduce
  experiment time by navigating parameter space). If the abstract leads with the **closed-loop, active
  parameter-selection** angle (fewer, better-chosen acquisitions ⇒ less wasted data), the "collect less,
  more intentionally" pitch becomes a defensible answer to the symposium's efficiency question rather than
  an off-scope one.
- **The FAIR / provenance-dataset bridge (Kamath).** The provenance-tracked parameter-sweep dataset maps
  onto topic (3) — FAIR curation of large characterization metadata — *if* framed as a community dataset,
  not just an internal calibration aid.
- **The material-system ally (Rommel).** Al-AM microanalysis keeps at least one organizer close to the
  content.

**Verdict:** *Plausible with a real reframe, but not a natural home.* As currently written (static,
ex-situ, benchtop SEM/EDS/EBSD/XRD/XRF, high-fidelity setup) it is a **stretch** for a symposium built
around rapid/large/in-situ data. Either (a) **reframe hard** around autonomous/active-learning acquisition
efficiency and the FAIR dataset to fit *this* symposium, or (b) **redirect** to a better-matched home.

### Better-matched alternatives (if not reframing)

- **AI/ML/Data Informatics for Materials Discovery: Bridging Experiment, Theory, and Modeling** — best fit
  if we lead with RAG / agentic decision-support grounded in standards + simulation.
- A **quantitative microanalysis / EDS-EBSD methods** or **phase-analysis** symposium — matches the actual
  content (trace-Mg EDS accuracy, EBSD indexing) far better than a big-data/in-situ room.
- **AI-Enabled Materials Processing: Integrating Accelerated Experimental Workflows and Processing-Aware
  Machine Learning** — conceptually close, **but #100 already targets it**, so routing #102 here would
  collide two FLAIME abstracts in one room. Last-resort fallback only.

*(A persona-grounded mock review by all five named organizers was requested via Edison Scientific; see
[`edison-trajectories/tms-2027-compositional-analysis-abstract-review/organizer-persona-review.md`](edison-trajectories/tms-2027-compositional-analysis-abstract-review/organizer-persona-review.md)
once available.)*

---

## Pre-submission checklist (per TMS abstract guidelines)

- [x] Draft submission abstract within the typical ~150-word / 1500-character TMS limit. — **144 words**
      (`wc -w`), submission version.
- [x] Select target symposium. — **Novel Strategies for Rapid Acquisition and Processing of Large
      Datasets From Advanced Characterization Techniques.**
- [x] Choose oral vs. poster preference. — **Oral Presentation.**
- [x] Ground every load-bearing claim in a real source or our own data (standardless-EDS Mg
      overestimate, EBSD CI jump with beam current, ASTM E1508/E2627). — done; see referenced version.
- [x] Keep claims defensible for an early-stage group — the system is described as one we **are building**
      and results as **emerging**, not solved; the LLM/RAG layer is framed as grounded decision-support,
      not autonomous replacement of the operator.
- [ ] **Confirm the author list** — add BYU microscopy-facility staff (Mike Standing / Paul) as co-authors
      or acknowledgees; confirm the presenting author and any external collaborators.
- [ ] Confirm whether "supply-chain-resilient" (vs. "critical-mineral-lean") is the agreed descriptor —
      matches the resolution adopted in #98.
- [ ] Note FLAIME / DOE funding acknowledgement if required by the program.
- [ ] Verify the symposium is accepting abstracts and check the exact deadline on ProgramMaster.
- [ ] Optionally spell out ICP-MS/MS validation instrument access (BYU Agilent 8900, per byu-vcl#95) if
      reviewers want the orthogonal-method detail.

---

## Mock symposium-organizer review

> **Update (2026-07-07):** the CFA flyer has now been read and the **five named organizers** identified
> (Vijayan, Kamath, Fan Zhang, McDannald, Rommel — see [Symposium selection](#symposium-selection-tms-2027)).
> A **live, persona-grounded Edison `ANALYSIS` mock review** role-playing each organizer was run; its output
> lives in
> [`.../organizer-persona-review.md`](edison-trajectories/tms-2027-compositional-analysis-abstract-review/organizer-persona-review.md).
> The two rounds below predate that and role-play only the symposium *scope* — read them as the earlier pass,
> superseded by the persona review and the downgraded fit read above.

Two rounds of scope-based mock review are saved under
[`edison-trajectories/tms-2027-compositional-analysis-abstract-review/`](edison-trajectories/tms-2027-compositional-analysis-abstract-review/)
([round 1](edison-trajectories/tms-2027-compositional-analysis-abstract-review/round1-organizer-feedback.md),
[round 2](edison-trajectories/tms-2027-compositional-analysis-abstract-review/round2-organizer-feedback.md)).
Net changes adopted from the review:

- **Reframed the pitch around the *data*, not the AI.** The symposium is about acquisition and dataset
  processing, so the abstract leads with the parameter–fidelity dataset and the acquisition-recommendation
  loop, and treats the LLM/RAG layer as one grounding source among three (standards, simulation, data) —
  not the headline.
- **Anchored the motivation in a concrete, reproducible failure** (standardless Mg overestimate; EBSD CI
  yield vs. beam current) rather than a generic "AI will help" claim — reviewers in this room respect
  hard microanalysis numbers.
- **Scoped honestly for an early-stage group** — "we are building," "emerging relationships," validation
  against orthogonal ICP-MS/MS — avoiding any claim that the system already replaces expert judgment.
- **Made the deliverable a shareable dataset**, which this symposium's audience values (labeled,
  provenance-tracked characterization-parameter data is scarce for metal AM).

## Reference / model context

- Compositional-analysis groundwork and raw data threads: [byu-vcl#95](https://github.com/vertical-cloud-lab/byu-vcl/pull/95)
  (SEM-EDS Mg quantification, eZAF cross-comparison, ICP-MS/MS validation, EBSD phase model / beam-current
  study, SEM/EDS SOP).
- Companion abstracts: ultrasonic atomization (#98) and LPBF process-parameter optimization (#100).
