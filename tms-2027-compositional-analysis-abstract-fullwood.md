# TMS 2027 Abstract — Fullwood-symposium spin-off (CALIBER, EBSD-forward)

> **Spin-off, not the primary submission.** The primary version of this abstract targets **Flyer 022
> (AI/ML/Data Informatics for Materials Discovery)** and lives in
> [`tms-2027-compositional-analysis-abstract.md`](tms-2027-compositional-analysis-abstract.md) +
> [`tms-2027-compositional-analysis-abstract-draft.md`](tms-2027-compositional-analysis-abstract-draft.md)
> (v5 / CALIBER). **This file is a separate, deliberately re-pitched version** tailored to the
> **Microstructure-Sensitive Design & Advanced Characterization** symposium honoring **David T. Fullwood**
> — kept apart so the 022 submission is untouched. Requested by @sgbaird on this PR.
>
> The same platform (**CALIBER**) and the same underlying work ([byu-vcl#95](https://github.com/vertical-cloud-lab/byu-vcl/pull/95))
> back both; only the *framing* changes. Where 022 leads with the agentic/RAG **system** as the
> contribution, this version leads with **EBSD pattern quality as the upstream enabler of trustworthy
> HR-EBSD / GND / MSD** — the room's core science.

---

## Why the reframe (one paragraph)

The Fullwood symposium's Topic 2 is *verbatim* "advanced electron-based characterization (EBSD, HR-EBSD
techniques)," and the room's thesis is **microstructure → mechanical behavior** via HR-EBSD elastic
strain, GND density, and statistical microstructure descriptors (the Adams/Fullwood/Kalidindi lineage).
Our load-bearing result — raising EBSD confidence-index yield on LPBF Al–Si from ~40% → ~77% via beam
current + a custom AlSi10Mg/diamond-cubic-Si phase model — is an **indexing-/pattern-quality** contribution
that sits directly upstream of every HR-EBSD or MSD measurement this audience makes: *garbage patterns in →
garbage GND/strain/descriptors out.* So the pitch is not "an AI data system" (that reads as instrument
informatics here) but "**the pattern-quality gatekeeper that makes your downstream mechanics defensible,
plus a reproducible dataset of how it's done.**" Full rationale + Edison persona-panel verdict
(**SUBMIT-IF-RETAILORED, confidence High, ~5–2 for**) in
[`edison-trajectories/tms-2027-fullwood-msd-symposium-fit/`](edison-trajectories/tms-2027-fullwood-msd-symposium-fit/symposium-fit-analysis.md).

---

## Submission metadata

**Symposium:** Microstructure-Sensitive Design and Advanced Characterization — An MPMD/SMD Symposium
Honoring David T. Fullwood (TMS 2027). ProgramMaster UNID `30252AD623C2640085258D49005F2294`.
**Sponsors:** MPMD + SMD; Advanced Characterization/Testing/Simulation, Computational Materials Science &
Engineering, and Mechanical Behavior of Materials committees.
**Presentation preference:** Oral Presentation.
**Authors:** Ronnie Guymon (presenting), Gage Erickson, Xavier Zaitzeff, Carl Robison, Sterling Baird
(corresponding / PI) — all Brigham Young University. *(Same list as the 022 submission; the BYU home venue
makes microscopy-facility staff — Mike Standing / Paul — natural acknowledgees, per byu-vcl#95.)*

> ⚠️ **Deadline:** this symposium lists **Abstract Submissions Due July 15, 2026.** As of today
> (2026-07-16) that date has **passed** — confirm the live deadline / late-submission status on
> ProgramMaster, and coordinate with the BYU organizers (Johnson / Homer / Miles), before submitting.

---

## Abstract — submission version (EBSD-forward, 149 words)

> Trustworthy microstructure-sensitive design begins with trustworthy patterns: HR-EBSD elastic-strain and
> GND-density measurements, and the statistical microstructure descriptors they feed, are only as reliable
> as the upstream EBSD acquisition — yet that step is fragile and operator-dependent. On
> laser-powder-bed-fusion Al–Si, EBSD indexing yield rose from ~40% to ~77% of points above CI = 0.1 once
> beam current and a custom AlSi10Mg / diamond-cubic-Si phase model were corrected; standardless SEM-EDS
> separately over-reported trace Mg several-fold. We present CALIBER, an uncertainty-aware platform that
> recommends and iteratively refines EBSD — and complementary EDS/XRF — acquisition parameters for a given
> sample and analysis goal. Recommendations are grounded in retrieval over characterization standards and
> HR-EBSD literature, electron-beam and interaction-volume simulation, and a growing provenance-tracked
> dataset of parameter sweeps. The result is a reproducible, transferable route to high-quality patterns,
> and a labeled dataset for statistical microstructure quantification, that makes downstream HR-EBSD, GND,
> and MSD analyses defensible.

*Word count 149 (`wc -w`), under the ~150-word cap. Longest sentence 38 words — if the room prefers
Ronnie's shorter-sentence voice, split the opening sentence at the em-dash.*

### Title

Recommended (leads with the enabling argument, names the platform, signals EBSD/MSD fit):

> **Patterns First: A Retrieval-Augmented, Uncertainty-Aware Platform (CALIBER) for High-Fidelity EBSD
> Acquisition to Enable Microstructure-Sensitive Design**

Alternatives, by flavor:

| Title | Flavor |
| --- | --- |
| CALIBER: Optimizing EBSD Acquisition and Phase Models to Enable Trustworthy HR-EBSD and GND Analysis of Additively Manufactured Alloys | Names the downstream methods; concrete |
| Garbage Patterns In, Garbage MSD Out: A Literature- and Physics-Grounded Platform for High-Fidelity EBSD Acquisition | Catchy lead; may read as too informal for the honoree session |
| Upstream of Microstructure-Sensitive Design: Reproducible, Uncertainty-Aware EBSD Parameter Selection for AM Alloys | Name-free; emphasizes the enabling role |

---

## Expanded / alternate version (leans into the HR-EBSD/MSD enabling argument)

Microstructure-sensitive design (MSD) and the HR-EBSD measurements that anchor it — elastic strain via
cross-correlation, geometrically-necessary-dislocation density from lattice-curvature, and the statistical
microstructure descriptors built on indexed orientation maps — all inherit their fidelity from a single,
often-undocumented upstream step: how the EBSD scan was acquired. Beam energy and current, working
distance, camera gain and binning, exposure, the phase list, and Hough/dictionary indexing settings jointly
determine pattern quality and indexing yield, and they are typically chosen by tacit operator expertise that
is rarely captured with enough provenance to reproduce or transfer between instruments. The cost is
concrete and reproducible in our own laboratory: on laser-powder-bed-fusion AlSi10Mg, the fraction of
points above CI = 0.1 rose from ~40% to ~77% once the beam current was raised from 1.6 to 6.4 nA and a
custom AlSi10Mg (plus diamond-cubic Si) phase model was loaded; separately, standardless eZAF SEM-EDS
over-reported Mg by several-fold relative to nominal, traced to the Mg Kα / Al Kα overlap and soft-X-ray
background modeling near 1–2 keV. We present CALIBER, an uncertainty-aware, closed-loop platform that, given
a sample and an analysis goal, proposes and then iteratively refines acquisition and indexing parameters —
primarily for EBSD, with complementary EDS and XRF for composition. Three grounding sources keep the
recommendations defensible: (1) retrieval-augmented generation over characterization standards and the
EBSD/HR-EBSD methods literature (e.g., ASTM E2627 for EBSD grain size, indexing- and pattern-quality
practice); (2) physics-based simulation of the electron beam and interaction volume — Monte Carlo / φ(ρz)
estimates of the current and geometry needed for adequate pattern quality without excess carbon
deposition; and (3) an accumulating, fully provenance-tracked dataset of systematic parameter sweeps on
well-characterized samples, so the lab grows its own labeled record of how each parameter shifts indexing
yield, pattern quality, and measured composition. We frame this explicitly as the enabler of the room's
core science: reliable HR-EBSD elastic strain and GND density require high-quality patterns upstream, and
reproducible statistical microstructure quantification requires trustworthy, consistently-acquired
orientation maps. We validate on commercial AlSi10Mg and lean, supply-chain-resilient aluminum alloys in
both atomized-powder and LPBF-printed form, benchmarking EDS/XRF composition against orthogonal ICP-MS/MS,
and we release a labeled EBSD/characterization-parameter dataset — with full sample provenance — as a
community resource for reproducible MSD inputs. We close on the forward path: validated acquisition feeding
HR-EBSD → GND / CPFE and DIC-EBSD workflows, i.e., the process → structure → property chain this symposium
is built to advance.

---

## Referenced version (with in-text citations — for a proceedings manuscript or extended abstract)

> **Note:** citation markers push this over the ProgramMaster word limit; submit the
> [149-word version](#abstract--submission-version-ebsd-forward-149-words) and reserve this for a
> manuscript, extended/poster abstract, or internal review. References are real, peer-reviewed or
> standards sources.

Microstructure-sensitive design and the HR-EBSD measurements that underpin it — cross-correlation elastic
strain and GND density [1,2] and the statistical microstructure descriptors built on indexed maps [3,4] —
are only as trustworthy as the EBSD acquisition upstream of them: pattern quality and indexing yield gate
every downstream cross-correlation and descriptor [1,5]. That upstream step is tacit and operator-dependent,
and the community is actively asking how far AI can automate characterization without over-promising [6],
with early progress in autonomous/agentic microscopy [7,8]. The need is concrete in our own data: on LPBF
Al–Si, EBSD confidence-index yield rose from ~40% to ~77% once beam current and a custom AlSi10Mg /
diamond-cubic-Si phase model were corrected — consistent with the reporting and cleanup conventions of ASTM
E2627 [9] and with dictionary-/Hough-indexing pattern-quality practice [5,10]; and standardless eZAF SEM-EDS
over-reported trace Mg several-fold, consistent with the Mg Kα / Al Kα overlap and soft-X-ray background
modeling that standardless routines handle poorly [11,12]. We present CALIBER, an uncertainty-aware
closed-loop platform that recommends and iteratively refines EBSD (and complementary EDS/XRF) parameters for
a given sample and goal, grounded in (1) retrieval over standards and the HR-EBSD/MSD literature, (2)
electron-beam and interaction-volume simulation, and (3) a growing provenance-tracked dataset of parameter
sweeps acting as in-house standards. We validate on commercial (AlSi10Mg) and supply-chain-resilient
aluminum in powder and printed form, benchmark EDS/XRF against orthogonal ICP-MS/MS, and release a labeled
dataset to make expert EBSD setup reproducible and transferable — the enabling input for defensible
HR-EBSD, GND, and statistical-microstructure analyses [3,4,7].

**References**

1. T. B. Britton, A. J. Wilkinson. "High resolution electron backscatter diffraction measurements of
   elastic strain variations." *Ultramicroscopy* (2011). doi:[10.1016/j.ultramic.2011.08.002](https://doi.org/10.1016/j.ultramic.2011.08.002)
2. D. T. Fullwood, B. L. Adams, et al. — HR-EBSD / GND density via lattice curvature (representative of the
   honoree's body of work; confirm the exact citation with the organizers).
3. S. R. Niezgoda, D. T. Fullwood, S. R. Kalidindi. "Delineation of the space of 2-point correlations in a
   composite material system." *Acta Materialia* (2008). doi:[10.1016/j.actamat.2008.07.005](https://doi.org/10.1016/j.actamat.2008.07.005)
4. A. Cecen, T. Fast, S. R. Kalidindi. "Versatile algorithms for the computation of 2-point spatial
   correlations." *Integrating Materials and Manufacturing Innovation* (2016).
   doi:[10.1186/s40192-016-0044-5](https://doi.org/10.1186/s40192-016-0044-5)
5. S. I. Wright, M. M. Nowell. "EBSD image quality mapping." *Microscopy and Microanalysis* (2006).
   doi:[10.1017/S1431927606060090](https://doi.org/10.1017/S1431927606060090)
6. E. A. Stach et al. "Mind the Gap: Bridging the Divide Between AI Aspirations and the Reality of
   Autonomous Characterization." *arXiv* 2502.18604 (2025). [arXiv:2502.18604](https://arxiv.org/abs/2502.18604)
7. M. Jamali, M. Aghazadeh, J. Kacher. "Thinking Microscopes." *npj Computational Materials* (2026).
   doi:[10.1038/s41524-026-02077-y](https://doi.org/10.1038/s41524-026-02077-y)
8. Evaluating large language model agents for automation of atomic force microscopy. *Nature
   Communications* **16** (2025). doi:[10.1038/s41467-025-64105-7](https://doi.org/10.1038/s41467-025-64105-7)
9. ASTM E2627-13. "Standard Practice for Determining Average Grain Size Using Electron Backscatter
   Diffraction (EBSD) in Fully Recrystallized Polycrystalline Materials." ASTM International.
   doi:[10.1520/E2627-13](https://doi.org/10.1520/E2627-13)
10. K. Marquardt, M. De Graef, et al. — dictionary indexing of EBSD patterns (Ram & De Graef 2018; confirm
    exact citation). doi:[10.1016/j.ultramic.2017.08.005](https://doi.org/10.1016/j.ultramic.2017.08.005)
11. ASTM E1508-12a. "Standard Guide for Quantitative Analysis by Energy-Dispersive Spectroscopy." ASTM
    International. doi:[10.1520/E1508-12A](https://doi.org/10.1520/E1508-12A)
12. J. Goldstein et al. *Scanning Electron Microscopy and X-Ray Microanalysis*, 4th ed. Springer (2018).
    doi:[10.1007/978-1-4939-6676-9](https://doi.org/10.1007/978-1-4939-6676-9)

> Refs 2 and 10 are placeholders to confirm against the organizers' preferred citations (the honoree's own
> HR-EBSD/GND papers and the Ram & De Graef dictionary-indexing paper) — the fit analysis lists specific
> candidates (Hansen et al. 2017, `10.1017/S1431927617000204`; Wiesman & Wallis 2026).

---

## What changed vs. the 022 submission (so nothing is lost)

| Dimension | 022 version (primary) | Fullwood version (this file) |
| --- | --- | --- |
| **Lead / hero** | The agentic RAG + provenance **system** is the contribution | **EBSD pattern quality** as the upstream enabler of HR-EBSD/GND/MSD |
| **Modalities** | SEM/EDS/EBSD/XRF as multimodal breadth | **EBSD foregrounded**; EDS/XRF/ICP demoted to supporting cast |
| **The 40%→77% result** | One hook among several | **The headline** |
| **Downstream tie-in** | FAIR dataset as community resource | Dataset as **MSD / statistical-microstructure input**; closes with HR-EBSD → GND / CPFE / DIC-EBSD |
| **Citations that matter** | Autonomous-characterization / LLM-microscopy | **HR-EBSD (Britton/Wilkinson, Fullwood), MSD (Niezgoda/Kalidindi), indexing quality (Wright/Nowell, Ram & De Graef), "Thinking Microscopes" (Kacher)** |
| **Biggest risk to manage** | Reads as "just aluminum results" to a data-native room | Reads as "instrument informatics" unless it bridges to mechanics — the closing sentence does that |

**Bottom line:** this spin-off is the version to submit *if* the target is the Fullwood symposium; the
files in the repo root remain the version to submit for Flyer 022. Both are kept side-by-side so the group
can pick per room without losing either framing.
