# §5 — Data Sources and Models (Edison Draft)


## §5 — Data Sources and Models (LaTeX-ready prose, ~175 words)

Replace the `\lipsum[13][1-5]` placeholder in the template with the following:

```latex
\textbf{Data sources.}
CALPHAD thermodynamic data are drawn from Thermo-Calc's TCAL10 (aluminum) and
TCMG6 (magnesium) databases via the TC-Python API under BYU's HPC license
(Thermo-Calc collaboration letter, Appendix~7).
DFT-computed formation energies from the Materials Project augment CALPHAD
features as surrogate-model inputs; experimental benchmarks follow the MMPDS
handbook.
All \flaime{}-generated data will be published on Zenodo/Figshare with
persistent DOIs; the PI's MPTS-52 dataset, heavily reused by the
crystal-structure generative-AI community, evidences this open-data commitment.

\textbf{AI models.}
Bayesian Optimization over Function Networks (\bofn{}) with the partial
Knowledge Gradient (pKGFN) acquisition function drives cost-aware experiment
selection atop GPyTorch/BoTorch Gaussian-process surrogates.
\bofn{}/pKGFN code will be released as open-source Python packages with
Honegumi tutorials and integrated into BoTorch's tutorial ecosystem (Meta
letter of support, Appendix~7).

\textbf{Genesis Mission integration.}
\flaime{} will host its digital thread, alloy database, and \bofn{}/pKGFN
models on the American Science Cloud (AmSC) and participate in GM coordination
activities.  \bofn{}/pKGFN will be released as a domain-specific
``plug-and-play'' capability per the GM framework.
Bidirectionally, \flaime{} will leverage other GM teams' validated
data---shared characterization databases and benchmark property
sets---to accelerate CALPHAD surrogate training.
```

**Word count:** ~175 (within the ~160 budget tolerance; the section fits comfortably on ~0.5 page at 11pt Times with 1-inch margins).

**Coverage checklist:**
1. ✅ Data sources: Thermo-Calc TCAL10/TCMG6, Materials Project, MMPDS handbook
2. ✅ Team access: BYU HPC Thermo-Calc license, TC collaboration letter (Appendix 7), TC-Python API
3. ✅ AI models/frameworks: BoTorch/BOFN, pKGFN acquisition function, GPyTorch surrogates
4. ✅ Genesis Mission bidirectional integration: AmSC hosting (digital thread, alloy DB, BOFN/pKGFN models), GM coordination participation, plug-and-play release, leveraging other GM teams' validated data
5. ✅ Open data/software: Zenodo/Figshare with DOIs, MPTS-52 reuse track record, BOFN/pKGFN open-source with Honegumi tutorials, BoTorch tutorial ecosystem integration (Meta letter of support)
6. ✅ No computing resources (per FOA: Appendix 2)

**Notes:**
- Uses the template's custom commands (`\flaime{}`, `\bofn{}`) for consistent formatting.
- Both Appendix 7 letter references (Thermo-Calc collaboration letter, Meta letter of support) are cited parenthetically for reviewer verifiability.
- The three bold-face subheadings (Data sources, AI models, Genesis Mission integration) provide visual structure and fast scanning for reviewers within the tight half-page allocation.
- ~15 words over the nominal ~160 budget; this can be trimmed by shortening the MPTS-52 sentence if page-count pressure requires it. As written, it renders well within 0.5 page.

---

Discretionary analytical decisions:

- **Organized into three bold subheadings** (Data sources, AI models, Genesis Mission integration) rather than running prose or a bulleted list, to maximize scanability within the 0.5-page budget while maintaining formal proposal tone.
- **Placed open-data dissemination within the "Data sources" paragraph** rather than as a separate fourth subheading, to save space and because the FOA's "Data Sources and Models" framing naturally accommodates data output commitments alongside data input descriptions.
- **Kept word count at ~175 vs. the ~160 target**, judging that all five required content areas could not be adequately covered in fewer words without sacrificing specificity that reviewers expect (e.g., database version numbers, API names, platform names). The ~160 budget is approximate ("~") and 175 words fits within 0.5 page at 11pt.
- **Referenced Appendix 7 for both the Thermo-Calc collaboration letter and Meta letter of support** rather than embedding details inline, to conserve word count and direct reviewers to primary evidence.
- **Used "evidences" rather than "demonstrates" for MPTS-52 track record** to compress word count while maintaining formal register.
- **Did not enumerate specific MMPDS properties or Materials Project API details**, keeping these at handbook/database level to stay within word budget while still satisfying the FOA's "describe data sources" requirement.
