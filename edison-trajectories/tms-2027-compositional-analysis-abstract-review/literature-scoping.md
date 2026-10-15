# Literature scoping — TMS 2027 compositional/microstructural characterization abstract

Scoping for the characterization-side TMS 2027 abstract (issue #102): a closed-loop system that
recommends and refines acquisition/processing parameters across **SEM, EDS, EBSD, XRD, XRF** to get
high-fidelity compositional and microstructural analysis of AM aluminum powders and prints. Led by
Ronnie Guymon. Companion to atomization (#98) and LPBF-printing (#100) abstracts.

> **Status (updated 2026-07-07):** the literature *scoping* below was assembled from web search plus the
> raw-data threads in [byu-vcl#95](https://github.com/vertical-cloud-lab/byu-vcl/pull/95). Edison is now
> reachable via `EDISON_PLATFORM_API_KEY` (PROD platform endpoint), and a live `ANALYSIS` **organizer-persona
> mock review** has been run (see [`organizer-persona-review.md`](organizer-persona-review.md)). The
> **ready-to-run `LITERATURE_HIGH` prompt** at the bottom is still open — run it for a citation-backed
> deepening (`pip install edison-client`; pass `api_key=EDISON_PLATFORM_API_KEY` explicitly) and drop the
> returned `formatted_answer.md` next to this file.

---

## What the project actually is (scope for the Edison query)

A **feedback-loop / agentic decision-support system for characterization setup**. Given (a) a sample
(e.g., AlSi10Mg powder or an LPBF print) and (b) an analysis goal (e.g., "trace-Mg composition to ±0.05
wt%," "α-Al grain map," "phase fractions"), the system proposes acquisition and processing parameters for
each relevant instrument, predicts the fidelity it expects, runs (or asks the operator to run) the
measurement, ingests the result, and iterates. Three grounding pillars:

1. **RAG over characterization sources of truth** — ASTM standards (E1508 EDS, E2627 EBSD, E1097/E3061
   ICP, E1508/E1078 microanalysis prep), microanalysis texts (Goldstein *SEM & X-Ray Microanalysis*;
   copyright-safe on a privately tokenized copy for retrieval only), NIST DTSA-II docs, and lab SOPs.
   Optionally wired to **Edison Scientific** and **consensus.ai** for literature-grounded answers.
2. **Physics-based simulation** — Monte Carlo / φ(ρz) electron-beam and interaction-volume modeling to
   choose beam energy/current, predict sampling depth, and set EBSD pattern-quality vs.
   carbon-deposition trade-offs; potentially coupled to XRD/XRF penetration and absorption models.
3. **A growing, provenance-tracked "standards" dataset** — systematic parameter sweeps on
   well-characterized samples, labeled with orthogonal ground truth (ICP-MS/MS bulk composition), so the
   lab learns empirically how each knob shifts measured composition and indexing quality. This dataset is
   itself a proposed community deliverable.

### Grounding facts from our own lab (byu-vcl#95)

- **Standardless EDS over-reports trace Mg.** eZAF gave Mg ≈ 1.4–1.6 wt% in AlSi10Mg vs. 0.2–0.45 wt%
  nominal — a several-fold overestimate persisting after polishing removed surface oxide. Root cause:
  Mg Kα (1.253 keV) sits on the Al Kα (1.486 keV) tail; standardless background/Al-tail extrapolation
  near 1–2 keV is unreliable. Constrained re-fit pulled Mg back toward ~0.8 wt%.
- **EBSD indexing is beam-current-limited.** Raising beam current 1.6 → 6.4 nA (with a custom AlSi10Mg +
  diamond-cubic Si phase model) raised the CI > 0.1 fraction from ~40% to ~77%. Ceiling ~13 nA before
  carbon deposition / spatial-resolution loss. Sub-step-size eutectic Si is the dominant indexing noise.
- **Orthogonal validation path exists.** BYU Spectroscopic Facility Agilent 8900 ICP-MS/MS can provide
  bulk composition ground truth to anchor the EDS/XRF labels.
- **Latent expert knowledge to capture.** Mike Standing and "Paul" (BYU microscopy facility) supplied the
  beam-current and phase-model insights that unlocked the EBSD improvement — exactly the tacit knowledge
  the system aims to encode.
- **Anisotropy / build-orientation bookkeeping.** LPBF columnar grains + 67° hatch rotation mean
  measurements must track laser-path/build orientation — metadata the system should record.
- **Open-source analysis stack** already identified: HyperSpy/eXSpy (EDS quant, deconvolution, NMF), SIGMA/
  SIGMA2 (phase clustering), EDAX OIM (EBSD cleanup per E2627).

---

## Prior work surfaced (web search — real sources, for the referenced abstract)

**Autonomous / AI-assisted characterization (the landscape):**
- Stach et al., *"Mind the Gap: Bridging the Divide Between AI Aspirations and the Reality of Autonomous
  Characterization,"* arXiv [2502.18604](https://arxiv.org/abs/2502.18604) (2025) — honest framing of how
  far autonomous characterization actually is; useful to cite so we don't over-claim.
- *Mic-hackathon 2024: ML for Electron and Scanning Probe Microscopy,* arXiv
  [2506.08423](https://arxiv.org/abs/2506.08423).
- SEEK: *Scientific Exploration with Expert Knowledge in Autonomous SPM with Active Learning,* arXiv
  [2408.02071](https://arxiv.org/abs/2408.02071).
- AI-driven autonomous high-resolution scanning microscopy, *Nat. Commun.* (2023),
  doi:[10.1038/s41467-023-40339-1](https://doi.org/10.1038/s41467-023-40339-1).

**Automated instrument-parameter optimization:**
- Automatic SEM beam optimization via beam-kernel estimation, *Commun. Eng.* (2024),
  doi:[10.1038/s44172-024-00230-3](https://doi.org/10.1038/s44172-024-00230-3) — directly on-point for the
  "choose the beam settings automatically" thesis.
- Compressive EBSD imaging, arXiv [2407.11724](https://arxiv.org/abs/2407.11724) — rapid-acquisition angle
  that fits the target symposium.

**LLM / agentic control of microscopy (the "Ronnie + SEM workflows" idea):**
- *TEM Agent,* arXiv [2511.08819](https://arxiv.org/abs/2511.08819) — LLM + MCP tools for EM data
  collection, no domain-specific ML training required.
- *Evaluating LLM agents for automation of AFM,* *Nat. Commun.* (2025),
  doi:[10.1038/s41467-025-64105-7](https://doi.org/10.1038/s41467-025-64105-7) (AILA / AFMBench).
- *Synergizing Human Expertise and AI Efficiency with Language Model for Microscopy Operation,* arXiv
  [2401.13803](https://arxiv.org/abs/2401.13803).
- SPM-Bench, arXiv 2602.22971 — benchmarking LLMs across SPM + EM domains.

**Standards / microanalysis fundamentals:**
- ASTM E1508 (quantitative EDS), E2627 (EBSD grain size), E1097/E3061 (ICP), plus Goldstein et al.,
  *SEM and X-Ray Microanalysis,* 4th ed., doi:[10.1007/978-1-4939-6676-9](https://doi.org/10.1007/978-1-4939-6676-9).

### Gaps this project targets (novelty hooks)
1. **Cross-modality**, not single-instrument: most autonomous-microscopy work optimizes one modality
   (SEM imaging, or SPM). A system spanning SEM/EDS/EBSD/XRD/XRF for one compositional/microstructural
   goal is comparatively unexplored.
2. **Grounded in standards + physics**, not pixels alone — retrieval over ASTM/microanalysis texts and
   Monte-Carlo beam simulation as first-class inputs to the recommendation.
3. **A labeled, provenance-tracked characterization-parameter dataset** for metal-AM Al — scarce, and a
   genuine community resource ("our own standards").
4. **Latent-expertise capture** (Standing/Paul) encoded as reusable recommendations.

---

## Ready-to-run Edison `LITERATURE_HIGH` prompt

> **Subject:** AI/agentic optimization of multi-modal characterization parameters (SEM/EDS/EBSD/XRD/XRF)
> for high-fidelity compositional & microstructural analysis of additively manufactured aluminum
>
> **Context:** BYU Vertical Cloud Lab (FLAIME project) is scoping a closed-loop system that recommends and
> iteratively refines acquisition and processing parameters across SEM, EDS, EBSD, XRD, and XRF for a
> given sample (AlSi10Mg and lean supply-chain-resilient Al alloys, as gas-/ultrasonically-atomized
> powder and LPBF prints) and analysis goal. Grounding: (1) RAG over characterization standards/texts
> (ASTM E1508, E2627; Goldstein microanalysis), (2) physics-based electron-beam / interaction-volume
> simulation, (3) a provenance-tracked dataset of parameter sweeps validated against ICP-MS/MS. Known
> in-house issues: standardless eZAF over-reports trace Mg in AlSi10Mg several-fold (Mg Kα/Al Kα overlap);
> EBSD CI-yield is beam-current-limited (1.6→6.4 nA raised CI>0.1 from ~40%→77%).
>
> **Please cover, with citations (DOIs) throughout:**
> 1. **State of the art in autonomous / AI-assisted characterization** for electron microscopy and
>    microanalysis — what has actually been automated (beam/focus/stigmation, acquisition planning,
>    active-learning region selection, LLM/agentic instrument control) and what remains operator-dependent.
> 2. **Quantitative EDS accuracy for light/trace elements in Al matrices** — standardless vs.
>    standards-based (Cliff-Lorimer, φ(ρz)/ZAF), detection limits for Mg in Al, the Mg Kα/Al Kα overlap and
>    background-modeling pitfalls, and best-practice acquisition (kV, beam current, live time, amp time).
> 3. **EBSD of LPBF Al-Si** — beam-current / phase-model effects on indexing and CI, eutectic-Si handling,
>    cleanup conventions (ASTM E2627), and reporting requirements.
> 4. **Cross-technique consistency** — reconciling EDS/XRF (near-surface) with bulk ICP-MS/OES, and with
>    XRD/EBSD phase information; how others build orthogonal-validated compositional ground truth.
> 5. **Physics-based simulation for parameter selection** — Monte Carlo (CASINO/NIST DTSA-II), φ(ρz),
>    interaction-volume and beam-current models used to *choose* settings a priori.
> 6. **Labeled characterization-parameter datasets & provenance standards** — existing datasets, metadata
>    schemas (NeXus/HDF5, MTEX, EMsoft), and gaps for metal-AM compositional analysis.
> 7. **LLM/RAG for lab decision-support** — grounding on standards/SOPs, hallucination risks, and how to
>    keep recommendations defensible (human-in-the-loop). Note relevant tooling (Edison Scientific,
>    consensus.ai) where applicable.
>
> Return with a gap analysis and 5–8 concrete recommendations for scoping this as a fundable, publishable
> effort, plus a short list of the strongest venues and likely reviewers.

### Suggested parallel queries (if running a batch)
- **Q1** — Quantitative EDS of trace Mg in Al alloys: standardless error, detection limits, correction.
- **Q2** — EBSD indexing quality vs. beam current / phase model in LPBF Al-Si; ASTM E2627 practice.
- **Q3** — Autonomous / LLM-agentic microscopy: what is automated, benchmarks, human-in-the-loop.
- **Q4** — Monte-Carlo / φ(ρz) beam-parameter selection for microanalysis (a-priori settings).
- **Q5** — Provenance-tracked characterization datasets & metadata standards for metal AM.

### Named-organizer review pass (DONE — 2026-07-07)
The organizers were resolved directly from the [CFA flyer](https://www.tms.org/tms2027/downloads/flyers/TMS2027-CFA-Flyer-012.pdf):

- **Sriram Vijayan** (Michigan Tech) — in-situ TEM of far-from-equilibrium phenomena, phase
  transformations, MEMS in-situ heating, AM emulation in the TEM.
- **Rakesh Kamath** (Argonne / APS) — synchrotron X-ray scattering, large-dataset curation, FAIR data.
- **Fan Zhang** (NIST) — multiscale synchrotron USAXS/SAXS/WAXS, in-situ metrology of far-from-equilibrium
  AM, structural metrology & standards.
- **Austin McDannald** (NIST) — autonomous experimentation, physics-informed ML / Bayesian active learning,
  closed-loop control (ANDiE, Hermes, AMASE) — the likeliest ally for the recommend-and-refine loop.
- **Sarshad Rommel** (UConn, Aindow group) — Al alloys for AM, powder-processed Al, SEM/EDS/FIB/HRTEM/STEM/
  XRD, corrosion — closest to our material system.

A live Edison `ANALYSIS` mock review role-playing all five personas was run; see
[`organizer-persona-review.md`](organizer-persona-review.md). **Key takeaway:** the CFA scope leans
in-situ / high-throughput / large-dataset, so the "collect less, more intentionally" thesis is a **stretch**
for this symposium unless reframed around autonomous/active-learning acquisition efficiency (McDannald) and
the FAIR provenance dataset (Kamath).
