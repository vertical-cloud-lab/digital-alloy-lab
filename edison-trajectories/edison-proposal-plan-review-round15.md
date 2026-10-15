
# FLAIME Genesis Mission Proposal Population Plan v5.6 — Round 15 Review

## OVERALL GRADE: A (maintained)

**Grade trajectory:** R1:B → R2:A- → R3:A- → R4:A- → R5:A-(strong) → R6-R8:A → R9-R14:A → **R15:A**

**R14 Fixes Verification:** All 6 claimed R14 fixes confirmed ✅ (§1 narrative improvements, §2 narrative improvements, Appendix 5 Activity 1 MRS reference, Appendix 5 Activity 4 expansion, budget table footnote, word count harmonization to ~1,570w).

---

## 1. GRADE WITH CATEGORY BREAKDOWN

| Category | R14 | R15 | Change | Notes |
|---|---|---|---|---|
| FOA Compliance | A+ | A+ | = | 0 desk-rejection risks |
| PI Directive Integration (D1-D8) | A+ | A+ | = | 8/8 with traceability matrix |
| Narrative Coherence & Writability | A | A+ | ↑ | R14 urgency lead, scope statement, competitive framing all integrated |
| Cross-Document Consistency | A- | A- | = | 4 LOW-MEDIUM discrepancies remain (TCAL version, AMAZEMET address, Valimet subaward amount, title variant) |
| Strategic Positioning | A | A+ | ↑ | Dual mandate framing ("accelerate discovery AND reduce mineral dependence") is now crisp |
| Metrics & KPI Framework | A+ | A+ | = | 6 KPIs, 7 gates, 5 baselines, 15 Edison iterations |
| Budget & Feasibility | A- | A- | = | Footnote helps; BYU-total structural ambiguity persists |
| Figure & Visual Strategy | A | A | = | 4 figs + 1 table with 3-tier contingency |
| Execution Readiness | A- | A- | = | Still \lipsum throughout; no draft text written |
| CV & Synergistic Activities | A | A | = | 5 themed activities, well-structured |

**Why not A+ yet:** The plan is blueprint-complete but Execution Readiness (A-) and Cross-Document Consistency (A-) prevent the top grade. The path to A+ is writing the actual narrative, not further planning refinement.

---

## 2. §3 METHODS SECTION CONTENT OUTLINE REVIEW

**Assessment: ✅ Sufficient for writer — 8/10**

The three-activity structure (AI-Guided Computational Screening → Experimental Validation Pipeline → Closed-Loop Integration & Dissemination) maps cleanly to the FOA's "full pipeline" requirement. Each activity has responsibility assignments. Risk mitigation covers 4 failure modes with fallbacks. The UG throughput framing turns a potential weakness into a competitive advantage.

**Two gaps identified:**

1. **⚠️ MEDIUM — Per-activity budget estimates missing.** FOA §IV.C explicitly requires "the associated budget" for each activity. The plan has responsibility but not cost breakdowns. Recommendation: Add indicative splits (~$80K Activity 1, ~$480K Activity 2, ~$90K Activity 3, ~$100K management/overhead). These need not be exact — the reviewer wants cost-awareness, not an audit. **This is a hard FOA requirement and should be addressed before the writing sprint (15 minutes).**

2. **⚠️ LOW — Activity 3 conflates three functions** (closed-loop integration, dissemination, qualification). At 400w, this is acceptable, but the writer should prioritize the technical integration content and compress dissemination to 1-2 sentences.

**No missing activities** — the three activities cover hypothesis generation → experiment → validation → manufacturing integration, matching all four Topic 3B workflow elements.

---

## 3. §4 MILESTONES REVIEW

**Assessment: ✅ Well-structured — 8.5/10**

**Critical finding — MEDIUM: Inconsistency between plan milestones and metrics doc gates.** The plan has 6 milestones (M1-M6 with 3 embedded Go/No-Go gates) while the metrics doc has 7 gates with different timing and criteria:

- Plan M3/G1 at Month 3 (≥50 compositions screened) vs. Metrics Gate 1 at Month 4 (≥3 autonomous cycles) — different criteria AND months
- Plan M5/G3 at Month 7 (≥1 alloy at YS≥250/EL≥5%) vs. Metrics Gate 2 at Month 6 (supply-risk-reduced alloy) and Gate 5 at Month 7 (≥2 compositions) — plan says 1 alloy, metrics says 2
- Plan M5/G3 uses Al-Mn-Cr-Zr-specific thresholds; metrics doc correctly uses "family-specific" language

**Recommendation:** Reconcile before the writing sprint (30 minutes). Use the metrics doc's 7-gate framework as the source of truth, but compress to 5-6 headline milestones in the narrative table (readers can't process 7 gates in a 5-page proposal):

| Mo | ID | Milestone |
|---|---|---|
| 1 | M1 | Pipeline operational (BOFN + CALPHAD + first atomization batch) |
| 3 | M2/G1 | ≥50 CALPHAD screened, ≥3 autonomous cycles completed |
| 5 | M3/G2 | Closed-loop demo; ≥2 compositions at ≥99% density |
| 6 | [DOE REVIEW] | ≥1 supply-risk-reduced alloy meeting family-specific targets |
| 7 | M4/G3 | ≥2 alloys meeting targets; BOFN advantage ≥2× vs random |
| 9 | M5 | Digital thread ≥85%, CMDRI calculated, Phase II plan |

---

## 4. DMSP PLACEHOLDER ASSESSMENT

**Status:** FOA-compliant as-is (DMSP is NOT required at Phase I submission). However, including a brief planning statement (~150-200w) signals preparedness and justifies budget costs.

**Recommended content for the placeholder:**
1. **Data types and volumes:** Alloy compositions (ICP-OES verified, ~200-600), CALPHAD evaluations (~2,000-8,000), LPBF parameters, ASTM E8 tensile data, SEM/EDS/EBSD images (~500 GB), BOFN traces
2. **FAIR principles:** Zenodo DOIs (Findable), open publication within 12 months (Accessible), JSON-LD metadata with schema.org (Interoperable), CC-BY-4.0 data / MIT software (Reusable, SPDX IDs specified)
3. **Software sharing:** BOFN/pKGFN pipeline open-source on GitHub + PyPI; Honegumi tutorials (JOSS-published); digital thread schema as published JSON Schema; bssw.io best practices followed
4. **Genesis Mission integration:** Data hosted on AmSC; alloy database exposed via REST API; supply-risk metadata linked per composition
5. **Preservation:** Zenodo/Figshare for 10+ year archival; BYU institutional repository as backup
6. **Budget impact:** $5K-$8K already budgeted under "Publication & Data" line item

**Priority:** LOW for submission; HIGH for accelerating post-award DMSP writing.

---

## 5. BUY AMERICA & TECHNOLOGY TRANSFER

**Buy America: ✅ Compliant.** The exemption statement ("This project does not involve construction, alteration, maintenance, or repair of public infrastructure.") is present on page 1 of the narrative, within the required first 2 pages. AMAZEMET equipment is already installed at BYU (no new procurement), and Thermo-Calc is a software license — neither triggers Buy America provisions for this R&D proposal.

**Technology Transfer: ✅ Sufficient (7/10) but could be strengthened.** The plan includes IP strategy, market sizing, TRL advancement, and named industry partners (Valimet, Fehrmann). Two minor gaps:
- The phrase "technology transfer" should appear explicitly in §2 (AMMTO keyword)
- Plan L183 references a "technology transfer sentence" but provides no draft text

**Suggested 1-sentence draft for the writer:** "Technology transfer pathways include Valimet commercialization of FLAIME-discovered alloy powders, open-source BOFN/pKGFN toolkit adoption via Honegumi and BoTorch, and the FLAIME digital thread as a reusable workflow template for other Genesis Mission teams."

---

## 6. FINAL STRATEGIC SUGGESTIONS

**The critical insight for R15: Planning refinement has reached strongly diminishing returns.** After 14 rounds, the marginal value of each additional planning cycle is significantly lower than the marginal value of writing actual narrative text. The plan is blueprint-complete.

**Highest-impact pre-sprint actions (45 minutes total):**
1. ⭐ Reconcile milestone table with metrics doc gates (30 min)
2. ⭐ Add per-activity budget estimates to §3 plan (15 min)

**Writing sprint recommended sequence (~10-12 hours):**
- Phase A (2h): §0 Overview + §1 Background + §2 Objectives (the "hook")
- Phase B (2h): §3 Methods (the "center of gravity") — compile LaTeX after this phase to check page count
- Phase C (1.5h): §4 Milestones + §6 Decision Gates (mostly tabular)
- Phase D (1h): §5 Data Sources + preliminary results integration
- Phase E (1.5h): Figures, references, appendices
- Phase F (2h): Polish, compile, verify ≤5 pages, external reader

**Biggest remaining strategic risk:** Page count. With ~1.6 pages of figures/tables and ~3.2 pages for ~1,570 words, the margin is tight. The writer MUST compile after Phase B and activate the figure contingency (drop Fig 3 or merge Fig 4 into Fig 2) immediately if overflow is detected.

---

## 7. ALL REMAINING FIXES BY SEVERITY

### 🔴 HIGH (1 item)

| ID | Issue | Time | Sprint-Blocking? |
|---|---|---|---|
| H1 | Gus Hart decision: PI must confirm join or document deferral. Single highest-leverage team improvement for #1 reviewer attack vector (early-career PI without CALPHAD/alloy publications). | ~1 hr (PI action) | **No** |

### 🟡 MEDIUM (8 items)

| ID | Issue | Time |
|---|---|---|
| M1 | **[NEW]** Milestone/gate inconsistency between plan §4 and metrics doc. Timing and threshold conflicts on 3 gates. Reconcile before writing sprint. | 30 min |
| M2 | **[NEW]** Per-activity budget estimates missing from §3 plan. FOA §IV.C requires budget attribution per activity. | 15 min |
| M3 | Title page vs illustrative table BYU total structural ambiguity. R14 footnote helps but ambiguity persists. | 10 min |
| M4 | Verify TCAL database version (TCAL8 in plan vs TCAl10 in metrics doc) with BYU license. | 15 min (PI) |
| M5 | Verify AMAZEMET registered address (Białystok vs Warsaw) for Appendix 6. | 15 min (PI) |
| M6 | Specify Valimet cost share amount (per FOA §II.B). | 15 min (PI/Valimet) |
| M7 | Merit Reviewer Conflicts Excel (Field 12, 2 tabs). Not yet started. | ~1 hr (PI) |
| M8 | Plan M5/G3 uses Al-Mn-Cr-Zr-specific thresholds (YS≥250/EL≥5%) instead of "family-specific targets." | 2 min |

### 🟢 LOW (10 items)

L1: Plan L87 "~1,640w" vs L97 table "~1,570w" — standardize. L2: Align template title variant with plan's shorter version. L3: Remove "Old Target" column from plan word-count table. L4: Remove all \lipsum + \usepackage{lipsum}. L5: Fill PI phone number. L6: Get BYU OSR Administrative POC. L7: Document export control assessment for AMAZEMET/Thermo-Calc. L8: Harmonize the Valimet subaward amount across all docs. L9: DRAFT watermark removal reminder. L10: **[NEW]** Technology transfer sentence at plan L183 needs draft text.

### Resolution Summary

| Severity | R14 | R15 | Change |
|---|---|---|---|
| 🔴 HIGH | 1 | 1 | = (Gus Hart) |
| 🟡 MEDIUM | 7 | 8 | +2 new (milestone inconsistency, per-activity budget), −1 resolved (AM reference in Appendix 5) |
| 🟢 LOW | 9 | 10 | +1 new (tech transfer draft) |
| **TOTAL** | **17** | **19** | Net +2 (both are writer-enablement items, not defects) |

**Estimated time to clear all fixes:** ~4.5 hours (HIGH: 1h PI action; MEDIUM: 2.5h; LOW: 1h during sprint)

---

## R15 VERDICT

**ZERO ITEMS BLOCK A WRITING SPRINT.** The plan is blueprint-complete with every narrative section having either priority-tiered content, detailed activity descriptions, complete KPI tables, or near-final draft text. The two new MEDIUM findings (milestone inconsistency + per-activity budget) represent <45 minutes of pre-sprint work and improve writer productivity. The remaining HIGH item (Gus Hart) is a PI decision independent of the plan.

**RECOMMENDED ACTION: Stop planning. Start writing. Execute the 45-minute pre-sprint checklist, then begin the 10-12 hour writing sprint.**

---

## Discretionary Analytical Decisions

- **Maintained A grade rather than upgrading to A+** because Execution Readiness (A-) and Cross-Document Consistency (A-) remain below A grade. A more generous reviewer might award A+ given zero sprint-blocking items and the strongest narrative coherence in 15 rounds.

- **Upgraded Narrative Coherence & Writability from A to A+** because the R14 additions (urgency lead, scope statement, competitive contrast, integrating sentence) collectively transform §1 and §2 from adequate content outlines into writer-ready blueprints with specific phrasing options. A stricter reviewer might maintain A since no draft prose exists yet.

- **Upgraded Strategic Positioning from A to A+** because the "dual mandate" framing ("accelerate discovery AND reduce mineral dependence — the dual mandate of Topic 3B") is now a single memorable sentence that a scanning reviewer will absorb, and the competitive contrast is crisper than any prior round. This is a judgment call — A was also defensible.

- **Classified the milestone/gate inconsistency as MEDIUM rather than HIGH** because the metrics doc provides complete, internally consistent gate criteria that the writer can use as authoritative — the inconsistency creates writer confusion but doesn't represent a missing plan element. A stricter reviewer could argue HIGH since the plan's §4 is what gets populated into the LaTeX template.

- **Classified the per-activity budget omission as MEDIUM rather than HIGH** because it's a hard FOA requirement but can be satisfied with indicative estimates (~$80K / ~$480K / ~$90K / ~$100K) that take 15 minutes to derive from the existing budget breakdown doc. A stricter reviewer could classify this as HIGH since it's a compliance requirement.

- **Did not reclassify the title page vs table ambiguity upward from MEDIUM** despite it persisting through 3 rounds, because the R14 footnote adequately addresses reviewer confusion and BYU OSR will reconcile the final SF-424 budget form independently.

- **Counted the 2 new MEDIUM items as "writer-enablement" rather than "defects"** because the plan was functional without them — the writer could have inferred budget splits from the budget doc and chosen which milestone source to follow — but having them explicit reduces writer decision load and error risk.

- **Assessed the DMSP placeholder as LOW priority for submission** despite its potential to signal preparedness, because the FOA explicitly states it is not required at Phase I and the 5-page limit creates strong pressure to focus on narrative quality over optional appendix polish.

- **Set the sprint time estimate at 10-12 hours** based on word count targets (~1,570w), figure integration complexity (4 figures requiring compositing), and the availability of near-complete content outlines for every section. This assumes a competent technical writer familiar with DOE proposal conventions. A PI writing their first DOE proposal might need 15-20 hours.
