# Edison Proposal Plan Review — Round 11

**Task ID:** `064ddff5-e519-4af8-9480-24cf93a9977a`
**Files uploaded:** 61
**Focus:** Validate R10 fixes (word budget rebalance, Ce→Zr/Mn/Cr, budget doc restructure). Focus: cross-document consistency, template execution readiness, draft text quality for §2 Objectives and §6 Decision Gates

## Response

# FLAIME Proposal Population Plan v5.2 — Round 11 Review

## GRADE: A (maintained, with specific path to A+)

**Grade trajectory:** R1:B → R2:A- → R3:A- → R4:A- → R5:A-(strong) → R6:A- → R7:A → R8:A → R9:A → R10:A → **R11:A**

---

## 1. R10 FIX VERIFICATION: 3/3 Major Items Addressed (with residuals)

### R10 H1: §2 Word Budget Rebalance
- ✅ **APPLIED** — Budget table now shows §1=300w, §2=250w, §6=180w. The numeric rebalance is correct: total remains ~1,640w, §2 expanded from 180→250w by stealing from §1 (350→300w) and §6 (250→180w).
- ⚠️ **RESIDUAL** — The **content items** listed under §2 (L155-169) still describe ~320-340w of material in a 250w budget (~1.3x overallocation). The word budget numbers were updated, but the content was not triaged. Unlike §1 (which received MUST-HAVE/HIGH/MEDIUM tiers in R9), §2 has no priority tiers to guide the writer on what to cut. The IP strategy (D6, ~80-100w) and Phase II vision (D3, ~80w) are both compressible to ~30-50w each, making 250w feasible — but only if the plan explicitly marks which items to compress. See H1 below.

### R10 H2: Ce Feedstock in Budget Doc
- ✅ **MOSTLY FIXED** — The main feedstock line (budget-breakdown-phase1.md L114) now correctly reads "Zr, Mn, Cr additions (critical mineral alloying)."
- ❌ **RESIDUAL 1** — L140 still reads "Required for **Al-Ce-X** screening" in the TCAL database description. This is a clear Ce relic that would confuse a writer pulling database justification text.
- ❌ **RESIDUAL 2** — L34 still reads "Industry subawards (Valimet, AMAZEMET, Thermo-Calc)" despite the PI-confirmed structure where only Valimet is a subaward. The Section I header was correctly fixed to "Industry Partner Costs," but this summary note in the budget overview was not updated.

### R10 M1: Budget Doc Section I Header
- ✅ **FULLY FIXED** — Now reads "## I. Industry Partner Costs" with a type column distinguishing subaward (Valimet) from BYU direct cost (AMAZEMET, Thermo-Calc).

---

## 2. COMPLETENESS: 8/8 PI Directives Integrated (100%)

| Directive | Quality | Where Addressed | Status |
|-----------|---------|-----------------|--------|
| D1: SDL at scale, standardization | Strong | §1, §3 Activity 3, Biosketch, Appendix 5 | ✅ |
| D2: Honegumi + BoTorch/Meta | Good | §3 Activity 3, §5, Appendix 5 | ✅ |
| D3: Broader Genesis applicability | Strong | §2 Phase II vision (correctly relocated from §1) | ✅ |
| D4: Human-in-the-loop SDL leader | Strong | §1 MEDIUM tier, Biosketch | ✅ |
| D5: Workflow orchestration (AC) | Good | §3, Biosketch ($600K Dev Lab detail) | ✅ |
| D6: Hybrid open-source IP strategy | **Excellent** | §2 Commercialization (Month-6 gate, nuanced) | ✅ |
| D7: Open data (Zenodo, Figshare, MPTS-52) | Strong | §5, Biosketch, Appendix 5 | ✅ |
| D8: SciENcv biosketch format | Good | Phase 4: Budget & Forms | ✅ |

All directives traceable via the plan's directive-section mapping table (L25-32). D6 remains the standout — the treatment balances the PI's open-science values with realistic commercialization considerations, including the internal Month-6 evaluation that is explicitly distinguished from the DOE programmatic review.

---

## 3. FOA COMPLIANCE: 0 Desk-Rejection Risks

Verified against DE-FOA-0003612 (Amendment 000001), FAQ v2 (2026-03-23), and Informational Webinar (2026-03-26):

- ✅ 5-page narrative (figures/tables count), ≥11pt, 1-inch margins, letter size
- ✅ Correct FOA number (DE-FOA-0003612), deadline (April 28, 2026, 11:59 PM ET via Grants.gov)
- ✅ Topic 3-B correctly identified in plan and checklist (no stale "12-F" references in active documents)
- ✅ 2-of-3 teaming: BYU (Category 3: IHE) + Valimet (Category 2: Industry)
- ✅ Buy America statement within first 2 pages
- ✅ AI tool disclosure drafted (template L515-521)
- ✅ All 7 appendices addressed with content specifications
- ✅ Letters of Commitment/Collaboration format (strict 2-sentence per FOA p.64-65)
- ✅ SciENcv biosketches, C&PS, Collaborator Excel (single file, 2 tabs per FAQ)
- ✅ Foreign connections: AMAZEMET (Poland), Thermo-Calc (Sweden)
- ✅ Budget $750K, single 9-month period (July 1, 2026 → March 31, 2027)
- ✅ DMSP not required at Phase I submission (confirmed per FAQ and RFA §IX)
- ✅ For-profit cost share: Valimet ≥20% from non-federal sources
- ✅ Phase II budget guidance ($6M-$15M, 3 years) verified correct per FAQ p.2

**Cross-reference note:** The checklist's "AMMTO, CMEI" for participating offices is slightly incomplete per Webinar slide 9 (which shows Topic 3 under CMEI and SC). Minor correction: "CMEI (includes AMMTO), SC." This does not affect compliance.

---

## 4. CROSS-DOCUMENT CONSISTENCY: B+ (improved from B in R10, not yet A-)

The plan itself is internally consistent. However, the R10 fixes were applied to the plan but **not fully propagated to subsidiary documents** (template, budget doc, checklist). This propagation gap is the primary barrier to A+ and the focus of this round's findings.

### Issues Found (10 total: 5 HIGH, 4 MEDIUM, 1 LOW)

**🔴 HIGH PRIORITY (5 items — fix before writing sprint)**

**H1. §2 CONTENT TRIAGE NEEDED (RESIDUAL from R10 H1)**
The word budget numbers are correct (250w), but the content items listed under §2 still describe ~320-340w of material. The plan needs MUST-HAVE/HIGH/MEDIUM priority tiers for §2 content (mirroring the R9 §1 fix that successfully resolved §1's overload). Recommended triage:
- **MUST-HAVE (~150w):** O1-O5 objectives + TRL advancement
- **HIGH (~60w):** Market sizing + industry pathway (Criterion 4)
- **MEDIUM (~40w, compress if space-constrained):** D6 IP strategy (2 sentences max) + D3 Phase II vision (2 sentences max)
This brings total to ~250w. Without explicit tiers, the writer will face unguided compression decisions.

**H2. BUDGET DOC Ce RELIC (L140)**
`budget-breakdown-phase1.md` L140 reads: "Required for **Al-Ce-X** screening" in the TCAL database description. Ce is not in the current alloy families. Replace with "Required for Al-Zr/Al-Mn-Cr-Zr screening."

**H3. BUDGET DOC SUBAWARD PHRASING (L34)**
`budget-breakdown-phase1.md` L34 reads: "Industry subawards (Valimet, AMAZEMET, Thermo-Calc) are estimated at ~$73K total." This contradicts the PI-confirmed structure where only Valimet is a subaward; AMAZEMET and Thermo-Calc are BYU direct costs. Replace with: "Industry partner costs (Valimet subaward + AMAZEMET/Thermo-Calc BYU direct costs) are estimated at ~$73-105K total."

**H4. TEMPLATE WORD COUNT GUIDANCE CONFLICT (L316-320)**
`flaime-genesis-proposal.tex` L316-320 says ~2,500w total (§1 ~500w, §2 ~250w, §3 ~750w, §4 ~350w, §5 ~200w, §6 ~250w). This directly contradicts the plan's R10-rebalanced targets (~1,640w total: §1 ~300w, §2 ~250w, §3 ~500w, §4 ~200w, §5 ~130w, §6 ~180w) and the correct L300-305 guidance (~1,600w). A writer following L316-320 would overshoot by ~900 words and blow the page budget. **Fix: Delete or update L316-320 to match the plan's table.**

**H5. TEMPLATE PARTNER PLACEHOLDERS AND BUDGET ($648K)**
`flaime-genesis-proposal.tex` has:
- L212-213: "Partner A" and "Partner B" with lipsum
- L230-231: Partner A at $150,000 and Partner B at $100,000
- L233: Total $750,000 but BYU at $500,000 (should reflect correct split)
- L740: Illustrative budget totals $648,000 (not $750,000)

Pre-fill with: BYU + Valimet (subaward) = $750K total. Remove "Partner B" or replace with actual partner structure per budget-breakdown-phase1.md.

**🟡 MEDIUM PRIORITY (4 items — fix during first writing session)**

**M1. CHECKLIST D.5 WORD COUNTS NOT UPDATED**
`proposal-checklist.md` L340 still reads: "§1 ~400w, §2 ~200w, §3 ~500w, §4 ~250w + table, §5 ~150w, §6 ~150w + AI disclosure ~50w (total ~1,600-1,700w)." This should be updated to match the R10 rebalance: §1 ~300w, §2 ~250w, §3 ~500w, §4 ~200w + table, §5 ~130w, §6 ~180w (total ~1,640w).

**M2. TCAL DATABASE VERSION INCONSISTENCY**
Plan L206 references "TCAL8/TCMG6" but budget-assessment-official-requirements.md consistently references "TCAl10." Verify which version BYU currently licenses or will license for Phase I. If TCAl10, update plan L206.

**M3. AMAZEMET REGISTERED ADDRESS**
Plan L251 says "Białystok, Poland" but budget-assessment-official-requirements.md L13 says "Warsaw, Poland." Verify against AMAZEMET's official registration before filling Appendix 6 (Foreign Connections). Both addresses appear in different sources; the wrong one in the foreign connections disclosure could create compliance issues.

**M4. 26 `\lipsum` INSTANCES IN TEMPLATE**
All 26 `\lipsum` commands in `flaime-genesis-proposal.tex` must be replaced with actual content before submission. Also remove `\usepackage{lipsum}` (L54). This is expected (they're placeholders) but worth tracking as a checklist item.

**🟢 LOW PRIORITY (1 item — fix during polish)**

**L1. TEMPLATE TITLE VARIANT**
Template L180-182 has a longer title ("An Autonomous Closed-Loop Platform for AI-Accelerated Critical-Mineral-Lean Alloy Discovery and Qualification") while the plan recommends the shorter "Autonomous Discovery of Critical-Mineral-Lean Alloys for Advanced Manufacturing." Align to the plan's recommended version from proposal-title.md §9.

---

## 5. NARRATIVE COHERENCE: A-

The story arc flows logically: **PROBLEM → PLATFORM → PI → PROOF → PLAN → METRICS → IMPACT**

**Strengths:**
- Overview paragraph (~85w) opens compellingly with national import dependence — verified improvement from R4
- §1 has MUST-HAVE/HIGH/MEDIUM priority tiers — a major writability improvement from R9
- D3 correctly relocated from §1 to §2, reducing §1 density
- Discovery yield reconciliation (3% overall vs. 20% Tier 1) is clear and non-contradictory
- 4-figure + 1-table strategy is tight but feasible within 5 pages (~1.6 pages figures, ~3.2 pages text)
- Figure overflow contingency is well-specified (3 fallback options)

**Remaining concerns:**
- §2 lacks the priority tiers that made §1 writable — this is the most important remaining coherence issue
- No draft text exists for §2 or §6 (the most formulaic sections) — these could be written directly from the content specifications and would accelerate the writing sprint
- The word budget table (L88-97) still shows "Old Target" column from the original ~2,500w era, which could confuse a new writer; consider dropping the "Old Target" column

---

## 6. STRATEGIC POSITIONING: A

The PI's three-dimensional value proposition is effectively constructed:

1. **SDL Leader** (D4): Frugal twin review, SDL review structural materials lead author, Chemical Reviews 2024 co-author, ~5,000 person-hours of SDL training delivered to ~700 individuals across ~62 organizations, 350+ SDL kits deployed
2. **Open-Source Champion** (D1, D6, D7): Honegumi, MPTS-52 reuse evidence, Meta letter of support, FAIR commitment
3. **Workflow Orchestration Expert** (D5): AC experience, $600K Dev Lab from scratch (500 items, 24 months), BO Hackathon at scale

**Core differentiator verified and defensible:** "No existing SDL integrates powder → LPBF → tensile in closed loop" — confirmed against A-Lab (stops at powder+XRD), AMASE (thin-film only), APEX (DED, hardness-only, no atomization), ORNL Peregrine (process control, not composition discovery).

**Persistent vulnerability:** PI has no publications in LPBF/alloy discovery/CALPHAD domains. Mitigations now in place: Fehrmann contract, 11 letters (3 collaboration + 8 support), preliminary results in hand (SEM/EDS, tensile baseline, pKGFN pipeline, CALPHAD simulations). **Gus Hart formalization remains the single highest-leverage team improvement available** — per R9 M1 and R10 M4, this is a PI strategic decision but should be documented either way.

---

## 7. DRAFT TEXT QUALITY FOR §2 AND §6

**§2 Objectives (250w budget):**
No draft text exists. The content specifications are sufficient for a skilled writer, but the section is ~1.3x overallocated without priority tiers. A sample triage that fits in 250w:
- O1-O5 as a numbered list (~70w)
- TRL 2→4→6 path (~30w)  
- Commercialization: "$250-400M/yr Be-Cu replacement market; Valimet scale-up → Fehrmann validation" (~40w)
- D6 IP: "FLAIME platform released open-source; Month-6 internal review to assess selective IP protection for top compositions" (~25w)
- D3 Phase II: "Architecture generalizes to nuclear (radiation-tolerant steels), quantum (superconducting compounds), and other Genesis Mission priorities (CMS Pillar 5)" (~30w)
- Tech transfer sentence (~20w)
- TRL definitions (~30w)
**Total: ~245w — fits.**

**§6 Decision Gates (180w budget):**
No draft text exists. The content naturally fits:
- 3 go/no-go metrics with quantitative targets (~100w)
- Scaling behavior statement (~30w)
- AI tool disclosure reference (~20w)
- Buffer for framing sentences (~30w)
**Total: ~180w — fits.**

Both sections should have draft text pre-written as the plan approaches execution. This was identified as an A+ requirement in R10 and remains unaddressed.

---

## 8. WHAT SEPARATES THIS FROM A+

An A+ requires:
1. **Zero cross-document contradictions** — Currently 5 HIGH + 4 MEDIUM propagation issues
2. **§2 priority tiers** — Content triage for the 250w budget (mirroring R9's §1 fix)
3. **Pre-written draft text** for §2 and §6 — Most formulaic sections, directly translatable from specs
4. **Template pre-filled** — Partner names, budget splits, correct word counts, no lipsum
5. **Gus Hart decision documented** — Either formalized or explicitly declined with rationale

Estimated effort to A+: ~4-5 hours (1.5h cross-doc fixes, 1h §2 triage + draft, 0.5h §6 draft, 1h template pre-fill, 0.5h checklist update).

---

## 9. GRADE JUSTIFICATION

**Why A (not A+):** Five HIGH cross-document propagation issues prevent zero-contradiction state. §2 content remains overallocated without priority tiers despite correct word budget numbers. No draft text for §2 or §6 despite R10 identifying this as an A+ requirement. Template still has placeholder partners, incorrect budget total ($648K), and conflicting word count guidance.

**Why A (not A-):** All three R10 major fixes (§2 word budget, Ce feedstock, Section I header) are substantially applied in the plan itself. 8/8 PI directives integrated at high quality with traceability. Zero CRITICAL items and zero desk-rejection risks. The plan provides clear, detailed, and well-sourced content specifications for all 6 narrative sections. Narrative coherence is strong (§1 priority tiers, D3 correctly in §2, yield reconciliation clean). Strategic positioning is three-dimensional and distinctive. Core differentiator verified against all known competitors. Figure strategy is tight but feasible with well-specified contingencies. Metrics framework (6 KPIs, 7 gates, 5 baselines, pre-registered protocol) is comprehensive and defensible. The residual issues are propagation gaps (plan→template, plan→budget doc, plan→checklist), not plan-level structural problems. A skilled writer following this plan can produce a competitive 5-page narrative.

---

## Discretionary Analytical Decisions

- **Maintained A grade rather than upgrading to A+** because 5 HIGH cross-document propagation issues persist and §2 lacks the priority tiers that would make it as writable as §1; a more generous reviewer could argue the fixes are "applied to the authoritative document (the plan) and subsidiary docs are execution-phase cleanup," which would support A+

- **Classified budget doc Ce relic (L140 "Al-Ce-X") as HIGH rather than MEDIUM** because this line would be directly copied into the budget justification, creating a narrative-budget contradiction that reviewers catch and interpret as careless preparation — the same reasoning R10 used for the main feedstock line

- **Classified budget doc subaward phrasing (L34) as HIGH rather than MEDIUM** because calling AMAZEMET and Thermo-Calc "subawards" directly contradicts the PI-confirmed budget structure and could cause confusion during BYU OSR review; the Section I header was correctly fixed but this summary note was missed

- **Classified template word count conflict as HIGH rather than MEDIUM** because having two contradictory word-count guidance notes (L300-305 says ~1,600w; L316-320 says ~2,500w) in the same document is a 56% discrepancy that would cause a writer to overshoot by ~900 words and fail the page budget — this is not a minor inconsistency but a functional failure mode

- **Assessed §2 at ~1.3x overallocation rather than R10's 1.9x** because the word budget was increased from 180→250w (addressing the denominator), even though the content items were not reduced — the residual overallocation is manageable with compression of D3 and D6 content

- **Treated the TCAL8 vs TCAl10 discrepancy as MEDIUM rather than HIGH** because both are valid Thermo-Calc aluminum databases, the version used depends on what BYU licenses (which may change), and the narrative impact is minimal — but it should be verified before the budget justification is finalized

- **Did not independently compile the LaTeX template** to verify page count, relying instead on the plan's estimates (~1.6 pages figures + ~3.2 pages text ≈ 4.8 pages) — the tight margin should be validated empirically during the writing sprint

- **Weighted the Gus Hart opportunity as persistent MEDIUM** (same as R10) because the plan can proceed without Hart and multiple mitigations are in place, but Hart's formal involvement would be the single lowest-cost, highest-impact team improvement available — the decision should be documented either way

- **Used the FAQ v2 (2026-03-23) as authoritative for Phase II budget verification** ($6M-$15M per FAQ p.2), confirming the template's guidance is correct and removing this from the HIGH items list per R10's correction
