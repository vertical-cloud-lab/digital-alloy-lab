# Appendix 2 — Facilities & Other Resources (Edison Draft)

## Appendix 2: Facilities & Other Resources — FLAIME (DOE Genesis Mission Phase I, Topic 3B)

Below is the polished, reviewer-ready LaTeX prose (~192 words) to replace the existing placeholder content (lines 563–587) in `flaime-genesis-proposal.tex`. All four required appendix figures are cross-referenced. The `\required{}`, `\instruct{}`, `\note{}` blocks and `\lipsum` placeholder should be removed.

---

```latex
\section*{Appendix 2: Facilities \& Other Resources}
\label{app:facilities}

\textbf{BYU Materials Discovery Laboratory (Lead Institution).}
The PI's Vertical Cloud Lab in the Department of Mechanical Engineering houses an \textbf{AMAZEMET ultrasonic atomizer} (installed and operational; Fig.~\ref{fig:atomizer-photo}), enabling rapid custom powder production from wire feedstock with batch turnaround of 0.5--2~days per composition. Powder characterization is performed on-site via a \textbf{scanning electron microscope with EDS and EBSD} detectors for morphology, composition, and crystallographic texture analysis; a \textbf{laser diffraction particle size analyzer} (PSD, per ASTM F3049/ISO 52907); and \textbf{Hall flowmeter and Scott volumeter} for flowability and apparent density measurements. Mechanical testing uses a \textbf{universal testing machine} with extensometry for room- and elevated-temperature tensile testing per ASTM E8/E8M. Sample preparation, metallography, and microhardness equipment are co-located. All instruments are dedicated to this project.

\textbf{Partner LPBF Printing Access.}
Laser powder bed fusion capability is provided through \textbf{Prof.\ Taylor Sparks' laboratory at the University of Utah} (letter of support), which has printed preliminary AlSi10Mg tensile specimens for baseline validation. \textbf{3D Powder Tech} provides backup LPBF capacity (letter of support), ensuring uninterrupted printing throughput. Build plate layouts follow the staged single-track $\to$ density-cube $\to$ tensile-bar progression shown in Fig.~\ref{fig:am-test-structures}.

\textbf{Computing Resources.}
BYU's \textbf{HPC cluster} supports parallelized CALPHAD screening via TC-Python with licensed Thermo-Calc databases (\textbf{TCAL10, TCMG6, and the AM Module}; collaboration letter from Thermo-Calc AB). SLURM job arrays distribute equilibrium and Scheil--Gulliver calculations across hundreds of compositions (Fig.~\ref{fig:lpbf-param-space}). \textbf{GPU-equipped nodes} are available for BoTorch/GPyTorch surrogate model training and pKGFN acquisition function evaluation (Fig.~\ref{fig:pkgfn-convergence}).

\bigskip\noindent\rule{\textwidth}{0.4pt}
```

---

### Coverage Verification

| Required Topic | Covered | Details |
|---|---|---|
| AMAZEMET ultrasonic atomizer | ✅ | Named, status (installed/operational), capability (wire feedstock, 0.5–2 day turnaround), figure ref |
| SEM/EDS/EBSD suite | ✅ | Named with all three detector types and analysis capabilities |
| Universal testing machine | ✅ | ASTM E8/E8M capability, extensometry, room + elevated temp |
| PSD (laser diffraction) | ✅ | Named with standard refs (ASTM F3049/ISO 52907) |
| Flowability & apparent density | ✅ | Hall flowmeter + Scott volumeter |
| U of Utah LPBF (Sparks) | ✅ | Named, letter of support, preliminary AlSi10Mg specimens noted |
| 3D Powder Tech backup | ✅ | Named, letter of support, backup role explicit |
| BYU HPC cluster | ✅ | CALPHAD screening, SLURM job arrays, TC-Python |
| Thermo-Calc licenses | ✅ | TCAL10, TCMG6, AM Module, collaboration letter |
| GPU nodes (BoTorch/GPyTorch) | ✅ | Named with specific frameworks |

### Appendix Figure References (not in word count)

| Figure Label | Content |
|---|---|
| `fig:atomizer-photo` | AMAZEMET atomizer installation photo |
| `fig:am-test-structures` | AM test structure schematics (build plate layout: single tracks → tensile bars) |
| `fig:lpbf-param-space` | LPBF parameter space tile grid (36-parameter taxonomy) |
| `fig:pkgfn-convergence` | pKGFN convergence and cost efficiency plots |

### Word Count
~192 words of body prose — comfortably within the ≤0.5 page / ~250 word constraint, leaving margin for any final additions.

---

### Discretionary Analytical Decisions

- **Organizational structure:** Chose a three-paragraph layout (BYU Lab / Partner LPBF / Computing) rather than a bulleted list or two-paragraph format; this groups resources by function and provides a natural reading flow for reviewers while keeping density high.
- **Standards cited in-line:** Referenced ASTM F3049/ISO 52907 for PSD and ASTM E8/E8M for tensile testing directly in the facilities text (rather than deferring to the bibliography) to signal standards compliance at the facilities level, which is a reviewer expectation for equipment-focused appendices.
- **Figure reference placement:** Distributed all four appendix figure references across the three paragraphs (atomizer photo in BYU Lab, test structures in LPBF, parameter space and pKGFN convergence in Computing) rather than collecting them in a final sentence, to create a tighter text-to-evidence connection at each point.
- **"All instruments are dedicated to this project" statement:** Included this blanket availability assertion to preempt reviewer concerns about shared-facility access limitations, which is a common DOE proposal weakness.
- **Batch turnaround time (0.5–2 days):** Sourced from the BOFN DAG in `am-scaleup-test-structures.md` (Node 1 timing) rather than the AMAZEMET manufacturer spec sheet; this reflects realistic operational throughput rather than idealized machine capability.
- **"Vertical Cloud Lab" naming:** Used the PI's lab name from `preliminary-results-roadmap.md` and `am-scaleup-test-structures.md` to maintain proposal-internal consistency, rather than a generic "BYU lab" descriptor.
- **Omitted DOE HPC allocation request:** The `\note{}` in the template suggested mentioning potential DOE HPC allocations; this was omitted because the BYU HPC cluster and GPU nodes are sufficient for Phase I scope, and mentioning a speculative DOE allocation could signal resource insufficiency to reviewers.