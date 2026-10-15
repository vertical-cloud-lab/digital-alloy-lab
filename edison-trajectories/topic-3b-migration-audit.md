# Topic 3B Migration Audit

*Generated April 11, 2026 — Comprehensive audit of all files and PRs requiring updates after the pivot from Topic 12F/Focus Area F to Topic 3B (Critical Minerals, AMMTO).*

---

## Decision Summary

**Old target:** Topic 12, Focus Area F — "AI-Enabled Materials Discovery, Development, and Qualification" (AMMTO)
**New target:** Topic 3, Focus Area B — "Critical Minerals: AI-Enabled Materials Discovery & Engineering" (AMMTO)

**Decision basis:** 21 Edison Scientific queries (~671K chars) across 7 topic assessments + 10 deep-dives + 1 synthesis. Topic 3B scored 7.5/10 with ~48% expected funding probability (vs. 12F at 4/10 with 3–6%).

**Key framing shift:** Al alloys are no longer a "surrogate" for Ni/Fe (which was 12F's fatal flaw). Under 3B, Al alloys ARE the primary deliverable — specifically, critical-mineral-lean Al alloy families (Al-Zr, Al-Mn-Cr-Zr) that reduce dependence on supply-constrained elements (Mg, Sc, REEs). Cu-Cr-Zr is a ~20% Phase I complement for Be-Cu replacement.

---

## Files in This PR (#26) — Status

### ✅ Already 3B-Aligned (no changes needed)
| File | Status |
|---|---|
| `edison-topic3b-fit-assessment.md` | Current 3B assessment (7.2/10) |
| `edison-topic4d-fit-assessment.md` | 3B comparison; 12F only as reference score |
| `edison-topic5a-fit-assessment.md` | 3B comparison; 12F only as reference score |
| `edison-topic-selection-synthesis.md` | Recommends 3B; 12F correctly ranked lowest |
| `edison-comprehensive-focus-area-scan.md` | Already notes "3B is clearly stronger" |
| `edison-3b-deepdive-{1..10}-*.md` | 3B deep-dives (10 files) |
| `edison-3b-deepdive-synthesis.md` | 3B validation synthesis |
| `topic-fit-comparative-assessment.md` | Summary table with 3B as top-ranked |
| `gas-atomization-scaleup-plan.md` | Updated with Valimet/Ames strategy for 3B |

### ⚠️ Deprecation Notices Added (April 11, 2026)
| File | Old Target | Notice Type |
|---|---|---|
| `genesis-mission-topic12-focus-area-f.md` | 12F (entire doc) | SUPERSEDED — retained for partner contacts & ORNL/MDF info |
| `full-proposal-strategy.md` | 12F strategy | SUPERSEDED — also flags 5-page limit correction |
| `informal-feedback-competitive-strategy.md` | 12F ("Submit to Focus Area F") | SUPERSEDED |
| `informal-feedback-v2-competitive-strategy.md` | 12F ("Submit to Focus Area F") | SUPERSEDED |
| `mock-reviews-phase1-strategy.md` | 12F (Ni/Fe scope) | SUPERSEDED — notes 3B eliminates key reviewer concerns |
| `edison-topic12f-fit-assessment.md` | 12F (4/10) | ARCHIVED |
| `edison-topic1b-fit-assessment.md` | 1B (5/10) | ARCHIVED |
| `edison-topic12b-fit-assessment.md` | 12B (4.5/10) | ARCHIVED |
| `edison-topic11c-fit-assessment.md` | 11C (5.8/10) | ARCHIVED — remains backup option |
| `edison-induction-materials-analysis.md` | 12F context | CONTEXT UPDATE — technical analysis still valid |
| `edison-topic-fit-synthesis.md` | Early 1B/12B/12F comparison | HISTORICAL — flagged as early-stage |

### 🟡 No Change Needed (comparative/technical mentions only)
| File | Reason |
|---|---|
| `ultrasonic-atomization-temperature-assessment.md` | Single comparative mention of 12F; technical analysis valid regardless |
| `edison-ga-scaleup-feedback.md` | Technical GA plan; not topic-specific |
| `budget-breakdown-phase1.md` | Budget mechanics; not topic-specific |
| `team-skill-chart.md` | Team capabilities; not topic-specific |
| Other technical literature files | General research infrastructure |

---

## Other Open PRs — 3B Migration Status

### ✅ Already Updated for 3B
| PR | Title | Evidence |
|---|---|---|
| **#40** | Budget assessment (Topic 3B) | Title explicitly references 3B |
| **#42** | Publication strategy (reassessed for Topic 3B) | Title + 3B alignment ratings |
| **#44** | Preliminary results roadmap | Updated for 3B in commit d824f55 |
| **#46** | Proposal gotchas (updated for Topic 3B) | Title + 3B-specific risk analysis |

### ⚠️ May Need 3B Updates (Genesis Mission–specific)
| PR | Title | What Needs Updating |
|---|---|---|
| **#28** | Project naming + proposal title research | Already contains 3B title assessment + backronym. Verify that 12F-era titles are clearly marked as superseded. |
| **#34** | Brainstorm metrics and measurables | project-metrics-v3-final.md may need 3B framing (critical minerals metrics, mineral burden reduction as KPI). Check if existing metrics are topic-neutral. |
| **#38** | Bare bones LaTeX template | Verify template header says Topic 3B, not 12F. Check if proposal title is updated. |
| **#30** | AM scale-up validation test structures | Test structure analysis is largely topic-neutral, but framing language may reference 12F. Quick check recommended. |

### 🟢 No 3B Changes Needed (general research infrastructure)
| PR | Title | Reason |
|---|---|---|
| **#4** | Thermo-Calc/CALPHAD | General capability — Thermo-Calc analysis is topic-neutral |
| **#6** | Deep literature search + BOFN demo | Technical method research — BOFN applies to any topic |
| **#8** | Survey alloy databases | Database survey — topic-neutral |
| **#10** | NSF EAGER | Different funding program entirely |
| **#12** | NSF funding opportunities | Different funding programs |
| **#14** | BOFN + LLM-BO synthesis | Technical AI/ML method — topic-neutral |
| **#16** | Company landscape analysis | Industry landscape — topic-neutral |
| **#18** | Welding data integration | Technical trajectory — topic-neutral |
| **#20** | LPBF processing parameters | Technical analysis — topic-neutral |
| **#22** | LPBF superalloy powders literature | Historical literature — useful for Phase II reference |
| **#24** | Thermo-Calc AM Module | General capability — topic-neutral |
| **#32** | Slicing software literature | Technical infrastructure — topic-neutral |
| **#36** | PR merge strategy | Meta/process — topic-neutral |

---

## Partnership Structure (Updated April 12, 2026)

### Letters of Collaboration (3 — official team members)
| Partner | Role | Budget | Status |
|---|---|---|---|
| **Valimet** | Gas atomization service provider (Phase I GA scale-up, 5–10 kg batches) | [partner amount removed] | Contacted; awaiting response week of April 14 |
| **AMAZEMET** | Ultrasonic atomizer vendor + consumables/process support (atomizer installed at BYU) | [partner amount removed] | Atomizer installed; letter of collaboration expected |
| **Thermo-Calc** | CALPHAD/AM Module provider — simulations running on BYU HPC | [partner amount removed] | Funded collaboration; AM Module simulations already provided |

### Letters of Support (8 — advisors and collaborators)
| Partner | Affiliation | Role |
|---|---|---|
| **Ames National Lab** | DOE National Lab (an Ames Lab contact, Powder Group) | Phase II GARS partnership pathway |
| **Fehrmann Alloys** | Industry | Master alloy / feedstock expertise |
| **Taylor Sparks** | University of Utah | LPBF printing access; AlSi10Mg specimen already printed |
| **Ashley Speer** | BYU | Departmental support |
| **Adam Clare** | University of Nottingham / UBC (FREng) | AM process expertise |
| **Chris Stiles** | JHU APL | Defense/nuclear application pathway |
| **Jae Hattrick-Simpers** | University of Toronto | Autonomous experimentation expertise |
| **Keith Brown** | Boston University | SDL pioneer; closed-loop experimentation |

### Draft Reply to Ames Lab
See `gas-atomization-scaleup-plan.md` Section 7A — draft email to an Ames Lab contact with letter of support / collaboration options (added commit 7840343).

---

## Preliminary Results in Hand (April 2026)

| # | Evidence Item | Status |
|:---:|---|---|
| 1 | AMAZEMET rePOWDER ultrasonic atomizer installed at BYU | ✅ Complete |
| 2 | AlSi10Mg tensile specimen printed at University of Utah (Taylor Sparks) | ✅ Complete |
| 3 | Tensile data (stress-strain, YS/UTS/elongation) for U of U specimen | ✅ Complete |
| 4 | AlSi10Mg tensile specimen from 3D Powder Tech | ✅ Complete |
| 5 | SEM + EDS for precursor powders (AlSi10Mg, Si powder) | ✅ Complete |
| 6 | SEM + EDS for AMAZEMET-atomized mixture (composition change from Al wire + Si addition) | ✅ Complete |
| 7 | High-temperature tensile data (standard aluminum specimen) | ✅ Complete |
| 8 | Thermo-Calc AM Module simulations (provided by Thermo-Calc) | ✅ Complete |
| 9 | Thermo-Calc CALPHAD simulations on BYU HPC clusters | ✅ Complete |
| 10 | Full pKGFN (partial Knowledge Gradient for Function Networks) pipeline implementation | ✅ Complete |
| 11 | Automated powder dispensing demonstration | ✅ Complete |

---

## Remaining Action Items

1. **PR #28 (naming):** Verify 12F-era titles are marked superseded; ensure 3B backronym ("Fast-Learning AI for Mineral-Efficient Alloy Design") is prominent
2. **PR #34 (metrics):** Add "critical mineral burden reduction" as explicit KPI if not already present
3. **PR #38 (LaTeX template):** Update Topic field to "Topic 3, Focus Area B" and proposal title to 3B version
4. **PR #30 (test structures):** Quick framing check
5. **Ongoing:** As proposal draft develops, update `full-proposal-strategy.md` (or supersede with 3B-specific strategy doc)
