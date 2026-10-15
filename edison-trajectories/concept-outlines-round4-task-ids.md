# Round-4 Edison concept-outline submissions — task IDs

Submitted 2026-05-02. Each Round-3-revised concept outline (commit `c9134ac`)
was uploaded as its own ANALYSIS task with the agency-matched program-manager
persona used in Round 3, plus an explicit "delta vs Round 3" instruction so
the personas can compare against their prior critiques (`4f3ccc3d`,
`3693bf31`, `7f0d73b0`).

**Results have not been polled.** A future session should fetch these three
task IDs and synthesize the responses into a Round-4 feedback document
analogous to `concept-outline-round3-{persona}-feedback.md`.

The submission script is `/tmp/edison_round4_submit.py` (not committed; the
prompt template lives in that script and is identical across the three tasks
except for the persona / agency-focus block and the round-3 reference task ID
threaded into the "delta vs Round 3" instruction).

| key             | persona                                                   | PDF                                     | round-3 task                             | round-4 task                             |
| --------------- | --------------------------------------------------------- | --------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| `nsf_dmref`     | NSF DMR Program Director (DMREF, NSF 25-508)              | `concept-outlines/01_nsf_dmref.pdf`     | `4f3ccc3d-84c3-47a7-b8a9-52891f760ebb`   | `02080e2b-a391-4419-a03e-e5bd23ffe2f2`   |
| `doe_ammto_cmi` | DOE EERE AMMTO PM coordinating with the CMI Hub Director  | `concept-outlines/02_doe_ammto_cmi.pdf` | `3693bf31-7609-44fc-ad8b-c58f995ac98b`   | `b10eb415-1665-4471-9815-f559649a4fee`   |
| `darpa_dso`     | DARPA DSO Program Manager (Office-Wide BAA)               | `concept-outlines/03_darpa_dso.pdf`     | `7f0d73b0-603c-4234-8934-0335e64cb24c`   | `ffcad0d4-3882-4a0f-a866-e6b23218387b`   |

Each task asked the persona to address the same eight items as Round 3:
(a) first-impression, (b) program fit, (c) partnership structure, (d)
preliminary-results credibility, (e) figures/layout/typography (the shared
TikZ DAG was redrawn with larger fonts and a scientific-feedback loop-closure
label), (f) concrete next-move email, (g) Genesis-Mission double-dipping
red-flags (the revision adds explicit task-level T1–T5 scope separation),
and (h) **delta vs Round 3** — what improved, what is still weak, and any
new issues the Round-4 revision introduced.

## Round-4 changes implemented per Round-3 feedback

### NSF DMREF (`4f3ccc3d`)
- Replaced "Al + 15-element bounded composition vector" with "Al + dilute
  Mn/Cr/Zr/Si/Fe, ≤6 active solute elements" to resolve the inconsistency
  between the focused chemistry in the "Fundamental question" section and the
  broader search-space claim in the "Idea" section.
- Demoted UA + LPBF parameters from co-equal design dimensions to "nuisance
  variables, not design targets" so the page no longer reads as process
  optimization.
- Restructured the Multi-PI paragraph into Funded / Unfunded-U.S. /
  Unfunded-international / Unfunded-NL / Industrial collaborator blocks.
  Toronto is now an "unfunded international collaborator" with explicit
  NSERC support; Utah Spear lab is an "unfunded U.S. collaborator" with a
  no-cost MOU. Both are now visible in prose, not just in the figure.
- Softened the closing ask ("a brief read on whether this concept appears
  potentially responsive to DMREF and whether a short scoping call would be
  useful") instead of "confirming program fit".
- Sharpened Genesis scope-separation as task-level T1/T2/T3 instead of
  narrative.
- Added a "Y1 scientific milestone" describing the prediction-validation
  example DMREF reviewers should expect (BOFN-CALPHAD posterior predicts a
  metastable phase that the public Al-database equilibrium assessment ranks
  differently, with SEM/TEM phase ID on a UA + LPBF coupon to confirm).

### DOE AMMTO + CMI (`3693bf31`)
- Added explicit mapping to the 2023 DOE Critical Materials List: the
  substitution targets directly displace Co (Critical 2025–2035), Sc/REE
  (Critical), and Ni (Near-Critical), with a per-element exposure score
  traceable to the current list.
- Rewrote the BABA paragraph to **name the manufactured articles** (UA-derived
  powder + LPBF-produced Al alloy coupon and tested article), confirm both
  are produced in the U.S., and address the EU mirror-site interaction as
  knowledge exchange only with no end product crossing the project boundary.
- Added a T1–T5 task-level scope separation against Genesis Topic 3B with
  per-task labor itemization and alloy-family-specific data packages.
- Acknowledged the downstream-adopter gap honestly with two named
  close-out paths (LPBF service bureau OR automotive/aerospace tier-1
  evaluator) to be disclosed before the full white paper.
- Added a Y1 risk-retiring milestone (one Al-Mn-Cr-Zr or Al-Zr LPBF coupon
  set with printability, RT tensile vs. AlSi10Mg, and per-element exposure
  delta vs. an Sc/REE-bearing comparator).

### DARPA DSO (`7f0d73b0`)
- **Retitled** away from "Built Strictly from Wire/Scrap Feedstock" to
  "Metastable L1₂/D0₂₂ Strengthening Phases in Rapidly Solidified Dilute
  Al-MPEAs Inaccessible to Equilibrium CALPHAD" so the page leads with the
  fundamental science wager, not the supply-chain integration story.
- Named the candidate phase family concretely: coherent L1₂-Al₃(Zr,Ti,X) and
  D0₂₂-related ordered nanoprecipitates in dilute Al-Mn-Cr-Zr-Si-Ti at
  10⁴–10⁶ K/s cooling rates.
- Sharpened the benchmark to "as-built UTS retention at 200 °C ≥ 85% of
  published Al-10Ce-3Ni and Al-2Sc-1Zr datasets at matched product form
  (LPBF coupon, no T6)".
- Clarified JHU APL transition path through AFRL Manufacturing & Industrial
  Technologies Division and Army DEVCOM Armaments Center, with APL as the
  FFRDC bridge to a named DoD program office (not the end customer).
- Made U. Utah Spear lab's role explicit in the partnership prose ("no-cost
  LPBF baseline coupon access via existing MOU"); previously only visible in
  the figure.
- Added T1–T4 task-level Genesis scope separation.
- Stated explicitly that "wire/scrap feedstock is downstream transition
  value, not the proposed DSO risk".

### Shared figure (`_pipeline_dag.tex`)
- Box font enlarged from `\footnotesize`/`\scriptsize` to `\small`/
  `\footnotesize` to fix the "5.6–6.4 pt sublabels" complaint shared across
  all three personas.
- pKGFN BOFN now bolded as the inference engine; the test box was renamed
  "Phase ID + Test" with SEM/TEM, tensile sublabel.
- Loop-closure label rewritten from "composition / process / property /
  supply-risk record" to "closed-loop feedback: phase ID + property update
  CALPHAD priors and BOFN posterior" so the figure visually foregrounds the
  scientific inference loop rather than the process chain.
