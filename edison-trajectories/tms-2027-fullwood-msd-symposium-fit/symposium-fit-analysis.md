# TMS 2027 fit analysis — "Microstructure-Sensitive Design and Advanced Characterization: An MPMD/SMD Symposium Honoring David T. Fullwood"

**ProgramMaster:** `30252AD623C2640085258D49005F2294`
**Abstract deadline:** 2026-07-15
**Sponsors:** TMS Materials Processing & Manufacturing Division + Structural Materials Division; Advanced Characterization/Testing/Simulation, Computational Materials Science & Engineering, and Mechanical Behavior of Materials Committees.
**Edison persona mock review:** task `3423e22e-5734-4b2f-923f-2ef2ee09c0cd` (`LITERATURE_HIGH`) — result in [`edison-mock-review-result.md`](edison-mock-review-result.md).

## Scope (as published)
Honors Prof. David T. Fullwood; emphasizes **advanced characterization techniques and modeling to link a material's microstructure to its mechanical behavior.** Core topics:
1. Microstructure-Sensitive Design (MSD) and statistical microstructure descriptions
2. **Advanced electron-based characterization (EBSD, HR-EBSD techniques)**
3. Computational + experimental mechanics integration
4. Multiscale deformation analysis (atomic → macroscopic)

## Organizers & personas
| Organizer | Affiliation | Persona / relevance |
|---|---|---|
| **Oliver K. Johnson** | BYU (ME) | Grain-boundary structure–property, network/graph analysis, ML for microstructure, EBSD. **Same dept as this abstract.** |
| **Eric R. Homer** | BYU (ME) | Grain-boundary structure, **HR-EBSD, GND**, atomistics, ML GB representations; co-directs BYU Microstructure lab. **Same dept.** |
| **Michael P. Miles** | BYU (Mfg) | Friction-stir, formability, EBSD, DIC. **Same institution.** |
| **Stephen R. Niezgoda** | Ohio State | MSD, texture, statistical microstructure descriptors, UQ, ICME (Kalidindi/Adams/Fullwood school). |
| **Marko Knezevic** | UNH | Crystal plasticity, texture evolution, AM, multiscale deformation. |
| **Josh Kacher** | Georgia Tech | In-situ TEM deformation, EBSD, local-chemistry effects on defects, multiscale defect characterization. |
| **Tim J. Ruggles** | Sandia | **HR-EBSD / cross-correlation EBSD**, local stress + GND density, in-situ HR-EBSD+DIC, indexing/pattern-quality methodology. |
| _(honoree)_ **David T. Fullwood** | BYU | HR-EBSD, GND, MSD, spherical-harmonic microstructure representation — thematic anchor. |

## My honest read (before Edison firms it up): **strongest fit of all symposia considered**
Two reasons this is the natural home:
1. **Scientific overlap is real, not stretched.** Topic 2 is *verbatim* "advanced electron-based characterization (EBSD, HR-EBSD)," and the title's second half is "**Advanced Characterization**." Our load-bearing result — raising EBSD confidence-index yield on LPBF Al–Si from ~40% → ~77% via beam current + a custom AlSi10Mg/diamond-cubic-Si phase model — is an EBSD **indexing-quality / pattern-quality / phase-model** contribution. That is squarely in the room's wheelhouse, and it is a fitting tribute to Fullwood's HR-EBSD legacy: you cannot do trustworthy HR-EBSD/GND (Ruggles, Homer, Fullwood) without good patterns and correct indexing upstream.
2. **Venue politics favor us.** This is a **BYU-hosted symposium honoring a BYU professor**, with three BYU ME/Mfg organizers. The presenting author (Ronnie Guymon) and PI (Sterling Baird) are BYU **Mechanical Engineering** — the honoree's own department. A friendly home venue with a genuine topical hook is the best-case scenario.

**The one honest gap:** classic MSD is about *microstructure → mechanical behavior* linkage and *statistical microstructure descriptors*; our abstract stops at **measurement fidelity / acquisition-parameter optimization** and does not (yet) compute GNDs, elastic strain, or property predictions. So we sit on the **"Advanced Characterization"** side of the title, lighter on the **"Microstructure-Sensitive Design"** side. This is a sharpening/emphasis problem, not a mismatch.

## Tailoring to sharpen fit (my recommendation)
- **Lead with EBSD.** Foreground the EBSD indexing-yield / pattern-quality / phase-model result as the headline; treat EDS/XRF/ICP as the multi-modal supporting cast.
- **Connect upstream to HR-EBSD/GND/MSD.** Frame acquisition-parameter fidelity as the *enabler* of trustworthy HR-EBSD, GND density, and statistical microstructure quantification — the inputs Fullwood/Ruggles/Homer/Niezgoda's methods depend on. "Garbage patterns in → garbage MSD out."
- **Position the dataset as an MSD community resource** for reproducible microstructure inputs.
- Cite the EBSD indexing-quality / dictionary-indexing and HR-EBSD literature (Wright, Nolze, Wilkinson & Britton, Fullwood/Adams) so the room sees you speak their language.

## Edison verdict (landed) — **SUBMIT-IF-RETAILORED, confidence High (~5–2 in favor)**
Panel of 7 organizer personas (full report: [`edison-mock-review-result.md`](edison-mock-review-result.md)). Tally: **3 Accept** (Miles, Kacher, Ruggles), **3 Lean-Accept** contingent on reframing (Johnson, Homer, Niezgoda), **1 Lean-Reject** softened by home venue (Knezevic). This confirms the pre-Edison read: **strongest fit of all symposia considered**, with the friendly BYU home venue lowering the acceptance threshold.

- **Strongest overlap = Topic 2** (advanced EBSD). The 40%→77% CI result + custom AlSi10Mg/diamond-cubic-Si phase model is squarely in the room's lane and a genuine tribute to Fullwood's HR-EBSD legacy — pattern quality is *the* gatekeeper for reliable cross-correlation strain/GND (Ruggles, Homer both stress this).
- **Kacher is an easy Accept** — he co-authored "Thinking Microscopes" (Jamali, Aghazadeh, Kacher 2026, 10.1038/s41524-026-02077-y); our agentic closed-loop is a concrete realization of his vision. **Cite it.**
- **Single biggest risk:** reads as "instrument informatics" rather than "microstructure science" if it never bridges to the room's mechanics core (GNDs, elastic strain, statistical descriptors).

**Highest-impact tailoring (panel-sourced, ordered):**
1. **Foreground the HR-EBSD/GND enabling argument** — state that pattern quality/indexing yield are prerequisites for reliable HR-EBSD strain/GND. Cite Hansen et al. 2017 (10.1017/S1431927617000204 — a Fullwood/Homer paper) and Wiesman & Wallis 2026 (10.1016/j.ultramic.2026.114330). If feasible, one before/after cross-correlation-quality figure (optimized vs baseline scan).
2. **Connect the dataset to reproducible statistical microstructure quantification** (MSD inputs) — cite Niezgoda/Kanjarla/Kalidindi 2013 (10.1186/2193-9772-2-3), Cecen/Fast/Kalidindi 2016, Niezgoda/Fullwood/Kalidindi 2008.
3. **Position phase-model construction as an advanced EBSD contribution** (Ram & De Graef 2018; Wright & Nowell 2006).
4. **Cite the agentic/autonomous-characterization literature explicitly** (Jamali/Kacher 2026; Kalinin et al. 2024).
5. **One forward-looking mechanics sentence** (validated EBSD → CPFE / DIC-EBSD / process–structure–property) to satisfy Knezevic.
6. Optional retitle to signal EBSD/HR-EBSD fit.

## Edison v2 verdict (post-reframe, on the actual CALIBER submission draft) — **SUBMIT, confidence High (~5–2 in favor)**
A second panel (task `72852aae`, full report: [`edison-mock-review-result-v2-caliber.md`](edison-mock-review-result-v2-caliber.md)) reviewed the **actual EBSD-forward CALIBER submission draft** (title *"Patterns First…"*), not the pre-reframe abstract. Verdict **upgraded from SUBMIT-IF-RETAILORED → clean SUBMIT**. Tally: **3 Accept** (Homer, Kacher, Ruggles), **1 Soft-Accept** (Johnson), **1 Soft-Accept on home-venue grounds** (Miles), **2 Borderline-but-persuadable** (Niezgoda, Knezevic). **No reject.** The reframe successfully moved the abstract from "instrument informatics" into the room's science; the "Patterns First / garbage patterns in → garbage MSD out" argument landed with the HR-EBSD organizers (Homer, Ruggles).

**Residual risk:** it's still an *enabler* abstract — computes no GND/strain/property itself. Dissolves if the *talk* shows even preliminary enabled downstream analysis. Two low-cost abstract sharpeners the panel still wants (both optional, neither blocks submission): (1) one forward-looking mechanics sentence (validated EBSD → CPFE / process–structure–property) to convert Knezevic; (2) name a concrete MSD descriptor class (ODFs / 2-point statistics / phase fractions) instead of generic "statistical microstructure quantification" to convert Niezgoda.

## Bottom line
**Lead candidate — recommend SUBMIT with the EBSD-forward + HR-EBSD-enabling reframe above.** Edison rates fit **High** (now a clean SUBMIT on the actual draft), clearly ahead of Fatigue (~60%), Flyer 009 tramp-elements (~70% only if heavily retailored), and the Rapid-Acquisition symposium (~3.4/5). ⚠️ Deadline Jul 15, 2026 — **passed** as of 2026-07-16; confirm live/late-submission status on ProgramMaster and coordinate with the BYU organizers.
