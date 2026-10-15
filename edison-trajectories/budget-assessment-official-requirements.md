# Genesis Mission Budget Assessment Based on Official Requirements

*Analysis of budget considerations for DOE Genesis Mission Phase I (DE-FOA-0003612, **Amendment 000001**) targeting **Topic 3B — Critical Minerals: AI-Enabled Materials Discovery & Engineering (AMMTO)**. References the official RFA (Amendment 000001, 165 pp.), FAQ v2 (updated 2026-04-10, 10 pp.), and Informational Webinar slides (21 pp.). Cross-referenced with the existing FLAIME budget breakdown and proposal strategy from PR #26. Verified by Edison Scientific ANALYSIS against the official source documents. Updated April 2026 to reflect the Topic 3B targeting decision and current partnership strategy.*

> **⚠️ IMPORTANT: Page Number Reference Note**
> Page references in this document are based on the original RFA release. Amendment 000001 added approximately 14 pages of content (primarily Phase II application sections), shifting most page numbers in §IV.C onward by ~14 pages. Section designations (§II.B, §II.E, §III.E, §IV.C, §VI.B, §VII.A) remain accurate. Page numbers for §II.B–§II.E are approximately +1 from cited values; §IV.C and later sections are approximately +14. Verify all page numbers against Amendment 000001 before citing in the proposal.

### Partnership Structure

**Letters of collaboration** (formal team members — termed "letters of commitment" in the RFA/FAQ):
- **Valimet** (Stockton, CA) — gas atomization service for 3–5 novel Al alloy compositions
- **AMAZEMET** (Warsaw, Poland) — ultrasonic atomization equipment, consumables, and process support (rePOWDER system installed at BYU)
- **Thermo-Calc** (Pittsburgh, PA / Stockholm) — CALPHAD screening via TC-Python/TCAl10, AM Module simulations

**Letters of support** (advisory/endorsement — supplementary to the required "letters of commitment"):
- **Ames National Laboratory** — Phase II pathway (Powder Group lead; Materials Preparation Center manager); note: if Phase II is pursued in the current round, it would be under a Phase-II-eligible focus area (Topic 3B does not accept Phase II in this solicitation)
- **Fehrmann Alloys** — feedstock validation and alloy development
- **Taylor Sparks** (University of Utah) — LPBF printing access and AM characterization
- **Ashley Speer** — materials characterization expertise
- **Adam Clare** — AM process expertise
- **Chris Stiles** — AM process engineering
- **Jae Hattrick-Simpers** — autonomous materials experimentation
- **Keith Brown** (Boston University) — SDL validation and autonomous experimentation

### Preliminary Results Available for Proposal

The following experimental and computational results are in hand or in progress for inclusion in the Phase I proposal:

1. **AMAZEMET rePOWDER atomizer installed** at BYU — operational ultrasonic atomization capability
2. **3D printed tensile specimen** (AlSi10Mg) printed at University of Utah using sourced powder
3. **Tensile data** for the U of U AlSi10Mg specimen
4. **Tensile specimen from 3D Powder Tech** (AlSi10Mg) — independent commercial baseline
5. **SEM and EDS** for precursor powders (AlSi10Mg, Si powder) and the atomized mixture returned by AMAZEMET (slight composition change from original AlSi10Mg through addition of Al wire and Si)
6. **High-temperature tensile data** using a standard aluminum tensile specimen
7. **Thermo-Calc AM Module simulations** — provided by Thermo-Calc for FLAIME alloy systems
8. **Full pKGFN (partial-Knowledge Gradient for Flow Networks) pipeline** — implemented BOFN framework for multi-stage alloy optimization
9. **Thermo-Calc CALPHAD simulations** run on BYU's HPC clusters (pycalphad + TC-Python)
10. **Automated powder dispensing demonstration** — key component of the closed-loop autonomous workflow

---

> **⚠️ UNRESOLVED ACTION ITEM: Topic 3B-Specific Cost Share Requirements**
> ~~Some focus areas in this RFA have additional cost share instructions beyond the general rules. Whether Topic 3B mandates cost share from the university (beyond the for-profit partner 20% requirement) has NOT been verified.~~ **RESOLVED (Edison spot check #5, task `65ab7c4f`):** Topic 3B has **NO focus-area-specific cost share requirements** — only the general §II.B rules apply (no cost share required for basic/applied research, except for-profit entities must provide ≥20% cost share from non-federal sources). No additional university cost share is required.

> **⚠️ Topic 3B Phase II Note (This Round Only)**
> The RFA (Amendment 000001) states: **"PHASE II APPLICATIONS WILL NOT BE ACCEPTED IN THIS FOCUS AREA"** for Topic 3-B. This is a **round-specific constraint** — it means Phase II applications under Topic 3B are not accepted in *this* solicitation, not that Phase II will never exist for this work. Future Genesis Mission rounds may include Phase II opportunities for materials discovery focus areas. Within this round, the FAQ clarifies that Phase II projects "may include multiple Phase I teams, remove Phase I team members, add external researchers, and/or address additional focus areas provided in the RFA," so a Phase I team in Topic 3B **can pivot to a different, Phase-II-eligible focus area** for Phase II in the current round if needed. The Phase I→II escalation strategy in Section 4 should be read with this nuance — the Phase II work described there would be submitted under a Phase-II-eligible focus area in the current round or under Topic 3B in a future round.

## Summary of Key Findings

| Question | Answer | Key Constraint | Reference |
|---|---|---|---|
| **Is equipment allowed?** | **Yes**, with justification | Must be necessary, reasonable, and allowable under the applicable OT structure; milestone-based OT explicitly exempts 2 CFR 200 cost principles (§IV.C, p. 74†); cost-reimbursement OT cost principles determined post-selection under 2 CFR 930.210; federal equipment threshold is ≥$5,000 (2 CFR §200.1) | RFA §IV.C (pp. 73–74†), §III.E (p. 59†) |
| **Could a desktop LPBF (~$40K) fit in Phase I?** | **Yes, but strategically risky** | Feasible within the $500K–$750K budget; must be justified as essential (not general-purpose); significant % of budget for equipment may weaken cost-effectiveness score | RFA Criterion 5 (p. 82), analysis in this document |
| **Can funding flow to industry?** | **Yes**, expected up to 20% of total budget | "Envisioned" expectation (not a hard cap); for-profit partners must provide ≥20% cost share on their portion; check focus-area-specific cost share requirements | RFA §II.E (p. 7), FAQ "Budgets" section, Webinar slide 12 |
| **Plasma/arc atomization as Phase II upgrade?** | **Strongly viable** | Phase II budget is $6M–$15M over 3 years; $100K–$500K for atomization modules is well within scope | FAQ (Phase II funding), analysis in this document |

---

## 1. Is Equipment Allowed?

### Official RFA Position

The RFA uses the standard **Research and Related Budget** form (SF-424) which includes an equipment category. The RFA explicitly states:

> "You may request funds under any of the categories listed as long as the item and amount are necessary to perform the proposed work, meet all the criteria for allowability under the applicable Federal cost principles, and are not prohibited by the funding restrictions in this RFA."
> — RFA §IV.C, p. 73

The **Program Unallowable Costs** section (RFA §III.E, p. 59) is notably brief:

> "Applications will be informed of cost principles and standards that comply with 2 C.F.R. § 930.210 after selection."

This means **equipment is not explicitly prohibited**. Critically, this RFA is issued under Other Transaction Authority (2 CFR 930), not standard grant authority — the specific cost principles that will govern are communicated **after selection**. The OT agreement type determines the level of cost-principle compliance:

1. **Cost-reimbursement OT** (similar to a grant): likely follows 2 CFR §200 cost principles, where equipment is generally allowable as a direct cost. Under standard federal practice (2 CFR §200.1/§200.439), equipment with a per-unit acquisition cost of ≥$5,000 may require prior written approval — though the RFA itself does not specify this threshold, and the actual cost principles will be determined post-selection under 2 CFR 930.210.
2. **Milestone-based OT**: the RFA states that "the budget provided does not need to comply with the cost principles in 2 C.F.R. § 200" (RFA §IV.C, p. 74). This gives **greater flexibility** for equipment purchases, as payments are tied to milestone completion rather than cost categories.

### Practical Implications

- **Equipment is allowable** in the Genesis Mission budget.
- Under cost-reimbursement OT, capital equipment (per-unit cost ≥$5,000 per 2 CFR §200.1) may require prior written approval from DOE under standard federal practice — though the RFA defers cost-principle identification to post-selection (§III.E, p. 59). Note: some institutions use a higher threshold (e.g., $10,000); verify BYU's institutional equipment threshold with OSR.
- Under milestone-based OT, equipment can be procured as part of achieving milestones without strict cost-category compliance.
- **Buy America Preference** (RFA p. 86, full text p. 114): Awards for infrastructure projects require iron, steel, and manufactured products to be produced in the United States. Applicability to Genesis Mission research awards is not certain — the requirement may apply only to specific project types. For equipment procured from foreign manufacturers (e.g., AMAZEMET's rePOWDER system), evaluate whether the provision applies and consider domestic sourcing alternatives or a waiver request if needed.
- Review Criterion 3 asks: *"Are the proposed facilities, equipment, and other resources, including access to data and AI models, adequate and appropriate for conducting the research/development?"* (RFA p. 82). This means reviewers will evaluate whether existing equipment is **insufficient** and new purchases are **necessary**.
- Review Criterion 5 asks: *"Is the proposed budget reasonable, well-justified, and appropriate for the scope and scale of the proposed work?"* (RFA p. 82). Large equipment purchases will be scrutinized for cost-effectiveness.

### Recommendation

Equipment purchases are allowed and can be included in the budget. However, each item should be justified as **essential** to the research workflow — i.e., the work cannot be accomplished without it, or alternatives (e.g., shared facility access) are demonstrably inferior. BYU's provision of space, facilities, or equipment at no charge can also be listed as institutional commitment (RFA §II.B, p. 5) to strengthen the proposal without consuming budget.

---

## 2. Could a Desktop LPBF Machine (~$40K) Be Part of the Budget?

### Market Landscape (2025–2026)

| System | Est. Price | Build Volume | Laser | Notes |
|---|---|---|---|---|
| Matrix SLM120D | $28K–$45K | 120 × 80 mm (dia × h) | 300W | Lab-ready with integrated ancillaries; smallest build volume |
| Xact Metal XM200C | ~$65K | 125 × 125 × 125 mm | 100–400W | Best value workhorse for small shops/labs |
| Metal 1.0 (Metal Base) | ~$15K–$20K | 128 × 100 mm (dia × h) | 60W diode | Kickstarter-funded; limited industrial value |
| AO Metal A30 | ~$59K+ | TBD | 200–1000W blue | High precision; open materials; newly launched |
| Xact Metal XM200G µHD | ~$90K–$100K | 140 × 140 × 150–290 mm | 100–400W | Ships mid-2026; micro-resolution capability |

At a strict **$40K budget**, options are limited to the **Matrix SLM120D** or similar compact systems. The Xact Metal XM200C at ~$65K is outside this range but could potentially be negotiated closer with academic pricing or a demo unit.

### Budget Impact Analysis

Using the existing $750K scenario:

| Scenario | Equipment Line | % of Total Direct Costs | Notes |
|---|---|---|---|
| **Current plan** (U of U access) | $12K (consumables + access fees) | 2.2% | Low equipment risk; relies on U of U LPBF service |
| **Desktop LPBF ($40K)** | $52K ($40K machine + $12K consumables) | 9.5% | Eliminates daily BYU↔U of U commute ($4K savings); enables on-site rapid iteration |
| **Desktop LPBF ($65K)** | $77K ($65K machine + $12K consumables) | 14.0% | Stronger capability; higher budget risk |

### Pros and Cons

**Arguments for including a desktop LPBF:**
- **Eliminates daily BYU↔U of U commute** (80 mi round trip, 6 days/week = $3K–$4K in mileage alone, plus ~2 hrs/day of student time lost).
- **Enables rapid closed-loop iteration** — the BOFN autonomous loop requires fast turnaround from powder → print → test. On-site LPBF removes the scheduling bottleneck of shared facility access.
- **Strengthens autonomy narrative** — reviewers evaluating the autonomous closed-loop platform will value having all workflow stages co-located.
- **Aligns with Topic 3B** — "deploy automated discovery platforms to accelerate material discovery, manufacturing, and qualification through closed-loop systems … reducing demand for critical minerals."

**Arguments against:**
- **Large single-item cost** in a 9-month project may raise cost-effectiveness concerns (Criterion 5).
- **Build volume limitations** — at ~$40K, desktop systems have small build volumes (120 mm or less), which may limit the number/size of tensile specimens per build.
- **Reviewers may question necessity** — if the U of U already has LPBF access, reviewers may view the purchase as duplicative. The justification must demonstrate that shared facility access is insufficient for the autonomous loop's throughput requirements.
- **Equipment stays with institution** — under 2 CFR 200, equipment purchased under federal awards is subject to disposition requirements. For a 9-month project, some reviewers may view this as the university acquiring equipment using federal funds rather than advancing the science.

### Recommendation

A desktop LPBF machine at ~$40K is **feasible but should be carefully justified**. The strongest justification frame is:

> *"The autonomous closed-loop FLAIME platform requires sub-24-hour powder-to-data turnaround to discover Al alloys that reduce dependence on supply-constrained critical minerals (Mg, Sc, REEs) within the 9-month performance period. Shared facility scheduling at the University of Utah introduces 3–5 day latency per build cycle, reducing the number of autonomous iterations from ~50 to ~15. An on-site desktop LPBF system eliminates this bottleneck and is essential to achieving the go/no-go milestone of demonstrating ≥30 closed-loop iterations across the Al-Zr and Al-Mn-Cr-Zr composition spaces."*

**Alternative strategy**: List the desktop LPBF as **institutional commitment** (BYU provides the machine at no charge, funded from other sources such as startup funds or a pending DURIP proposal). This removes the cost from the DOE budget, strengthens the institutional commitment section, and avoids the cost-effectiveness concern while still having the machine available.

---

## 3. Can Funding Flow to Industry?

### Official RFA Position

**Yes.** The RFA, FAQ, and webinar all indicate an expectation (not a hard cap) of up to 20%:

> "It is envisioned that DOE funding for all industrial partners combined could be up to 20% of the total requested budget for specific project-relevant research efforts."
> — RFA §II.E, p. 7

The FAQ reinforces this:

> "Q. Are companies allowed to request funding under this RFA?
> A. Yes. It is envisioned that DOE funding for all participating companies combined could be up to 20% of the total requested budget for specific project-relevant research efforts."
> — FAQ, "Budgets" section

The webinar slides also confirm:

> "The total funding to all industrial partners on a Phase I or Phase II award is expected to be up to 20% of the total requested budget for specific project-relevant research efforts."
> — Webinar, slide 12

### Cost Share Requirements for Industry Partners

For-profit entities (whether prime or subrecipient) must provide:
- **≥20% cost share** for basic and applied research activities
- **≥50% cost share** for demonstration and commercial application tasks

This cost share must originate from **non-federal sources** (RFA §II.B, p. 5).

### Budget Implications for Phase I ($500K–$750K)

| Total Budget | Expected Industry DOE Funding (~20%) | Industry Cost Share (≥20% of total project cost for their portion) | Notes |
|---|---|---|---|
| $500,000 | $100,000 | ≥$25,000 from company (non-federal) | Cost share is additive — company contributes $25K+ on top of $100K DOE funding |
| $600,000 | $120,000 | ≥$30,000 from company (non-federal) | Total industry project cost: ≥$150K ($120K DOE + $30K company) |
| $750,000 | [partner-specific amount removed] | [removed] | [removed] |

### Potential Industry Partner Budget Scenarios

| Partner | Role | Est. Budget | Justification | Status |
|---|---|---|---|---|
| **Valimet** (Stockton, CA) | Gas atomization service provider for 3–5 novel Al alloy compositions at 5–10 kg batch scale; Phase I GA validation partner | [partner amount removed] | Custom GA production + powder QC for UA→GA transfer validation (TRL 2–3 → TRL 4–5); official Category 2 (Industry) team member; budget mechanism (subaward vs. service contract) to be confirmed with BYU OSR — subaward if counting toward teaming, service contract if Valimet is commodity provider only | **Letter of collaboration** — phone contact made April 8–9; awaiting follow-up |
| **AMAZEMET** (Warsaw, Poland) | Ultrasonic atomization equipment support, consumables (sonotrode tips, crucibles), process optimization for Al alloy compositions | [partner amount removed] | rePOWDER system installed at BYU; ongoing consumables, custom crucible development, and process support for novel Al-Zr and Al-Mn-Cr-Zr compositions; Buy America considerations for Polish company | **Letter of collaboration** — existing equipment relationship; atomizer installed and operational |
| **Thermo-Calc** (Pittsburgh/Stockholm) | CALPHAD screening via TC-Python/TCAl10, AM Module simulations for printability maps, process parameter optimization | [partner amount removed] | License upgrade (TCAl8→TCAl10 + AM Module), TC-Python API access for HPC screening; already providing AM Module simulation results for proposal preliminary data; periodic project calls and student training | **Letter of collaboration** — advisory role agreed; AM Module simulations being provided; will provide letter after seeing proposal draft |
| **Downstream adopter** (e.g., Fehrmann Alloys, Framatome, BWXT) | Requirements definition, specifications review, qualification framework input | Unfunded | Letter of support for downstream pathway; strengthens Criterion 4 if applicable | **Fehrmann Alloys: letter of support** target |

### Unfunded Partners

The RFA explicitly allows unfunded partners:

> "To meet this requirement, partners must provide intellectual contributions to the proposed project but do not need to be funded by DOE."
> — RFA §II.E, p. 7

This means an industry partner can satisfy the teaming requirement without receiving DOE funding. The partner's intellectual contribution must be described in the proposal, and a letter of commitment is required (FAQ, Application Process section).

### Recommendation

- **Fund Valimet as the primary GA industry partner**, well within the ~20% expectation. **Budget mechanism note**: If Valimet participates as a collaborative team member (satisfying teaming requirements), the appropriate budget mechanism is a **subaward or collaborative agreement** — not a simple service contract, which typically covers commodity services and may not count toward teaming. Resolve this distinction with BYU OSR and DOE guidance. Note: the 20% figure is an "envisioned" expectation, not a hard cap — a single partner at 2–5% is conservative and well-justified.
- **Fund AMAZEMET as a collaborative equipment/process partner** for consumables, custom crucible development, and process optimization. The rePOWDER atomizer is already installed at BYU (demonstrated in preliminary results). AMAZEMET's ongoing support ensures the ultrasonic atomization node of the FLAIME closed loop operates at full capability for novel Al-Zr and Al-Mn-Cr-Zr compositions. Buy America Preference considerations: as a Polish company, evaluate whether the provision applies and consider structuring the budget to emphasize services (not manufactured goods) to reduce Buy America exposure.
- **Fund Thermo-Calc as a CALPHAD/simulation partner** for license upgrade (TCAl10 + AM Module) and TC-Python API access for HPC screening. Thermo-Calc is already providing AM Module simulation results for the proposal's preliminary data and has agreed to periodic project calls, student training, and ongoing consultation. Their letter of collaboration strengthens the CALPHAD integration narrative and directly enables the mineral-burden screening workflow.
- **Total funded industry partners**: $45K–$105K combined (6–14% of $750K budget), comfortably within the ~20% industry funding expectation.
- **List 8 letter-of-support partners** as unfunded advisory/endorsement partners: Ames National Lab (Phase II GARS pathway), Fehrmann Alloys (feedstock validation), Taylor Sparks (U of Utah LPBF/AM), Ashley Speer (characterization), Adam Clare (AM process), Chris Stiles (AM engineering), Jae Hattrick-Simpers (autonomous materials), Keith Brown (Boston U SDL). These satisfy teaming requirements and strengthen Criteria 3 (Team/Resources) without consuming budget.
- **Ames National Lab (letter of support for Phase II)**: Ames's Powder Group confirmed interest in collaborating on GA scale-up validation. However, Ames had an internal Genesis Mission intent-to-submit cut-off date (prior to April 10, 2026) which may preclude a letter of collaboration for Phase I. Target a **letter of support** pointing to Phase II GARS partnership (note: if Phase II is pursued in the current round, it would be under a Phase-II-eligible focus area since Topic 3B does not accept Phase II in this solicitation; future rounds may accept Phase II under this focus area). If Ames makes an exception on their internal deadline, upgrade to letter of collaboration (subaward). Note: if Ames joins as a subaward, the National Lab subaward deduction rule applies (RFA p. 75†) — DOE deducts that amount and pays the lab directly.
- DOE **prefers collaborative applications** over subaward arrangements (RFA p. 56†) and the FAQ/Webinar "strongly encourage" collaborative structures (FAQ p. 9; Webinar slide 15). Having three industry collaborators (Valimet, AMAZEMET, Thermo-Calc) as collaborative team members aligns strongly with this preference.
- Remember that funded industry partners must provide ≥20% cost share from non-federal sources. Ensure all three funded partners (Valimet, AMAZEMET, Thermo-Calc) are willing and able to meet this requirement.
- **Focus-area-specific cost share: RESOLVED** — Topic 3B has no additional cost share requirements beyond the general §II.B rules. Only for-profit entities must provide ≥20% cost share from non-federal sources. No university cost share is required for basic/applied research under Topic 3B.

---

## 4. Could Plasma or Arc Casting Atomization Modules Be Part of a Phase II Upgrade?

### Phase II Budget Context

The FAQ states that Phase II projects are *"approximately 3 to 5 times the level of effort of Phase I projects per year for three years."* The Webinar (slide 14) specifies total estimated awards of *"$6,000,000 to $15,000,000 pending out year appropriations."* The implied per-year calculation is: annualized Phase I rate ($500K × 12/9 ≈ $667K/yr to $750K × 12/9 ≈ $1M/yr) × 3–5× multiplier ≈ $2M–$5M/yr, yielding $6M–$15M over 3 years.

### Atomization Module Cost Estimates

| Module Type | Est. Cost Range | Temperature Capability | Suitable Alloys |
|---|---|---|---|
| **Induction crucible (current)** | Already available (AMAZEMET rePOWDER — installed at BYU, letter of collaboration partner) | Up to ~1300°C | Al, Cu, Mg, Zn, Sn alloys — Phase I primary (Al-Zr, Al-Mn-Cr-Zr), stretch (Cu-Cr-Zr) |
| **Enhanced induction crucible** | $20K–$50K upgrade | Up to ~1500–1600°C | + Some stainless steels, lower-melting Ni alloys |
| **Plasma arc melting module** | $100K–$300K | Up to ~3000°C+ | Refractory metals (W, Mo, Nb, Ta), Ti alloys, Ni superalloys |
| **Arc melting + gas atomization** | $200K–$600K (complete system) | Up to ~3500°C | Full range including refractory HEAs |
| **Plasma atomization system** (turn-key) | $300K–$700K | Up to ~3000°C+ | High-purity spherical powders; Ti, Ni, refractory alloys |

### Phase II Budget Fit

At $6M–$15M total Phase II budget, atomization module upgrades represent:

| Module | Cost | % of $6M Budget | % of $15M Budget |
|---|---|---|---|
| Plasma arc module ($200K) | $200,000 | 3.3% | 1.3% |
| Full arc + gas atomization ($500K) | $500,000 | 8.3% | 3.3% |
| Turn-key plasma atomization ($500K) | $500,000 | 8.3% | 3.3% |

These represent **modest fractions** of the Phase II budget and are well-justified given the RFA's emphasis on scaling the platform to reduce critical mineral demand across alloy families. The Phase II atomization upgrade enables the platform to address Be-Cu replacement (Cu-Cr-Zr at higher temperatures) and potentially Co/Ni-lean structural alloys for clean energy applications.

### Strategic Framing: Phase I → Phase II Escalation

> **⚠️ Topic 3B Phase II Note (This Round)**: The RFA (Amendment 000001) states that "PHASE II APPLICATIONS WILL NOT BE ACCEPTED IN THIS FOCUS AREA" for Topic 3-B in this solicitation. This is round-specific — future Genesis Mission rounds may accept Phase II under this focus area. Within this round, Phase I teams in Topic 3B can pivot to a different, Phase-II-eligible focus area for Phase II. The strategy below describes the technical escalation; if Phase II is pursued in the current round, it would be submitted under a broader materials discovery topic.

The reusable Phase I→II strategy, restated here for reference and aligned with Topic 3B (Critical Minerals), is:

> **Phase I (9 months, $500K–$750K):** Demonstrate the autonomous BOFN platform on **Al alloys that reduce dependence on supply-constrained critical minerals** (Al-Zr, Al-Mn-Cr-Zr families — avoiding Mg, Sc, and REE dependency) using the installed AMAZEMET rePOWDER ultrasonic atomizer (~1300°C capability) at BYU. Validate 3–5 top compositions via gas atomization at Valimet (UA→GA transfer). Leverage Thermo-Calc CALPHAD screening (TC-Python/TCAl10 on BYU HPC + AM Module simulations) for composition space prioritization. Demonstrate the full pKGFN pipeline for multi-stage optimization. Prove the closed-loop iteration concept with preliminary results including AlSi10Mg tensile specimens (U of U + 3D Powder Tech), SEM/EDS powder characterization, high-temperature tensile testing, and automated powder dispensing. Cu-Cr-Zr feasibility demonstration (~20% stretch effort) establishes Be-Cu replacement pathway.
>
> **Phase II (3 years, $6M–$15M, upgraded hardware + expanded team):** Scale the platform to **full critical mineral substitution portfolios**: (1) Cu-Cr-Zr full optimization for Be-Cu replacement (primary Phase II material — eliminates beryllium, a highly supply-constrained critical mineral with <1% recycling rate), (2) Al-Ce alloy expansion (leveraging AMMTO's CMI Hub Al-Ce precedent at TRL 9 — Al-Ce reduces Sc/REE-heavy incumbent alloy dependency while utilizing domestically available Ce from existing rare-earth processing), (3) advanced Al-Mn-Cr-Zr families. Upgrade atomization to plasma arc capability (up to 3000°C+) for refractory/Ni alloys. Partner with Ames National Lab for GARS scale-up validation at 10–25 kg batch scale. Industry partner for downstream qualification (Fehrmann Alloys, Framatome, BWXT, or equivalent).

The Phase II teaming requirements also support this: Phase II **must** include at least one partner from both category (1) (DOE/NNSA National Laboratory) and category (2) (Industry). Ames National Lab (letter of support targeting Phase II — either under a Phase-II-eligible focus area in the current round, or under Topic 3B in a future round) and Valimet + AMAZEMET (letters of collaboration for Phase I, continuing into Phase II) provide a natural upgrade path. An industry partner specializing in atomization equipment (e.g., Arcast or Retech for plasma arc) could join the Phase II team for the hardware upgrade.

> **Critical minerals framing note**: While Zr, Mn, and Cr are themselves on the 2022 USGS Critical Minerals List, they have significantly more secure domestic supply chains than the elements being displaced (Mg is DOE near-critical→critical; Sc is critical with no domestic production; REEs are dominated by Chinese supply). The narrative is "substituting high-supply-risk critical minerals (Mg, Sc, REEs, Be) with lower-supply-risk alternatives (Zr, Mn, Cr) that have domestic production capacity and recycling infrastructure" — not claiming the alloys are "critical-mineral-free."

### Recommendation

- **Explicitly describe the Phase II atomization upgrade pathway** in the Phase I proposal narrative to show scalability and long-term vision.
- Frame it as: *"The AI/BOFN framework is the invariant asset; the heating hardware is the expandable variable. Phase I proves the autonomous loop on Al alloys that reduce Mg/Sc/REE dependency; Phase II scales into full critical mineral substitution portfolios (Cu-Cr-Zr for Be elimination, advanced Al alloys for broader supply chain optimization) using the same data schemas, Bayesian optimizer, and qualification metrics."*
- **Do not include plasma/arc atomization costs in Phase I budget** — this would consume too large a fraction and is not needed for the Al alloy demonstration.
- **Identify Valimet as the Phase I GA partner** (letter of collaboration), **AMAZEMET as the UA equipment/process partner** (letter of collaboration), and **Arcast or Retech as a potential Phase II industry partner** for the plasma arc hardware upgrade, strengthening the commercialization pathway narrative.

---

## Cross-Reference with Existing Budget Documents

### Changes to `budget-breakdown-phase1.md`

The existing budget breakdown should be updated to reflect:

1. **Equipment line item reconsideration**: The current $8K–$12K "Equipment & Consumables" line is for minor items. If a desktop LPBF is included, this increases to $48K–$77K. If the LPBF is listed as institutional commitment, the equipment line stays minimal.
2. **Industry partnerships (three funded collaborators)**:
   - **Valimet GA partnership**: funding for gas atomization of 3–5 Al alloy compositions. Budget mechanism (subaward vs. service contract) to be confirmed with BYU OSR.
   - **AMAZEMET consumables/process support**: funding for sonotrode tips, custom crucibles, and process optimization for novel compositions. Buy America considerations apply (Polish company).
   - **Thermo-Calc license/simulation support**: funding for TCAl10 + AM Module license upgrade and TC-Python API access. Already providing AM Module simulations as preliminary data.
   - If subaward mechanisms, F&A exclusion rules apply (first $25K of each subaward typically included in MTDC base). Consult with BYU OSR on mechanism for each partner.
3. **Milestone-based OT option**: If selecting a milestone-based OT agreement, the budget justification has more flexibility on equipment categories. Note the RFA explicitly states: *"For milestone based OT agreements … the budget provided does not need to comply with the cost principles in 2 C.F.R. § 200"* (p. 74). Also note that OT agreements are described as "non-negotiable" and "fast-track" (§VII.A, p. 85; Webinar slide 15).
4. **National Lab subaward deduction**: If Ames National Lab joins as a Phase I subaward (unlikely but possible), DOE will deduct that amount from the award and pay the lab directly (RFA p. 75). More likely for Phase II.
5. **Unfunded partners (no budget impact)**: 8 letter-of-support partners (Ames, Fehrmann Alloys, Taylor Sparks, Ashley Speer, Adam Clare, Chris Stiles, Jae Hattrick-Simpers, Keith Brown) satisfy teaming requirements without consuming budget.

### Revised Budget Scenario ($750K with Desktop LPBF + 3 Industry Collaborators)

| Category | Original $750K | Revised $750K | Delta | Notes |
|---|---|---|---|---|
| A. Personnel | $393,880 | $320,000 | -$73,880 | Reduce to 8 undergrads (eliminate 2 LPBF travel roles); add savings from eliminated commute |
| B. Fringe | $42,510 | $35,000 | -$7,510 | Adjusted for reduced personnel |
| C. Materials & Supplies | $55,000 | $40,000 | -$15,000 | Remove U of U access fees ($12K); reduce travel consumables |
| D. Software & Licenses | $18,000 | $8,000 | -$10,000 | Reduced — some licence costs moved to partner budgets |
| E. Equipment | $12,000 | $52,000 | +$40,000 | Add desktop LPBF system (~$40K) |
| F. Travel | $14,000 | $8,000 | -$6,000 | Eliminate daily BYU↔U of U trips |
| G. Publication & Data | $8,000 | $8,000 | $0 | Unchanged |
| H. Other Direct Costs | $6,000 | $6,000 | $0 | Unchanged |
| **I. Valimet GA (subaward)** | — | [partner amount removed] | — | Gas atomization of 3–5 Al alloy compositions at 5–10 kg batch scale |
| **J. AMAZEMET (subaward)** | — | [partner amount removed] | — | Consumables, custom crucibles, process optimization for novel Al compositions |
| **K. Thermo-Calc (subaward)** | — | [partner amount removed] | — | TCAl10 + AM Module license, TC-Python API, screening support |
| **Direct Subtotal** | $549,390 | $550,000 | +$610 | |
| Indirect (F&A, est.) | ~$200,610 | ~$200,000* | -$610 | Illustrative estimate only; actual F&A must be calculated using BYU's negotiated rate and applicable base (for example, MTDC, including the standard subaward treatment — first $25K of each subaward typically in MTDC base) |
| **TOTAL** | **$750,000** | **$750,000 target** | **$0 target** | Final total depends on OSR-confirmed indirect calculation |

> **Note:** This is an illustrative scenario. The revised indirect amount is an estimate, not a balancing figure, and should be confirmed with BYU's Office of Sponsored Research using BYU's negotiated F&A rate and the applicable base/exclusions (for example, MTDC treatment of subawards). Total industry subaward: $73K (9.7% of $750K), well within the ~20% expectation. All three funded partners must provide ≥20% cost share from non-federal sources.

---

## Key RFA References

> **Note:** Page references marked with † are from the original RFA. Amendment 000001 shifted page numbers — early sections (§II) by ~1 page, later sections (§IV.C onward) by ~14 pages. Verify against Amendment 000001 before citing in the proposal.

| Document | Section | Topic | Key Quote |
|---|---|---|---|
| RFA (DE-FOA-0003612, Amend. 000001) | §II.B, p. 5† (~p. 6) | Cost sharing | "Cost sharing is not required for basic and applied research awarded under this RFA … except for-profit entities" |
| RFA | §II.E, p. 7† (~p. 8) | Industry funding expectation | "It is envisioned that DOE funding for all industrial partners combined could be up to 20% of the total requested budget" |
| RFA | §III.E, p. 59† (~p. 61) | Cost principles deferred | "Applications will be informed of cost principles and standards that comply with 2 C.F.R. § 930.210 after selection" |
| RFA | p. 56† | Collaborative preference | DOE "prefers" collaborative applications over subaward arrangements; FAQ/Webinar "strongly encourage" collaborative structures |
| RFA | p. 86† (~p. 72 in Amend.), p. 114† (~pp. 130–135) | Buy America Preference | Awards for infrastructure projects require iron, steel, and manufactured products produced in the U.S. |
| RFA | §IV.C, p. 73† (~p. 87) | Budget categories | "You may request funds under any of the categories listed as long as the item and amount are necessary" |
| RFA | §IV.C, p. 74† (~p. 88) | Milestone OT flexibility | "For milestone based OT agreements … the budget provided does not need to comply with the cost principles in 2 C.F.R. § 200" |
| RFA | p. 75† (~p. 89) | National Lab subaward deduction | DOE deducts National Lab/FFRDC subaward amounts and pays labs directly |
| RFA | §VI.B, p. 82† (~pp. 94–97) | Criterion 3 | "Are the proposed facilities, equipment, and other resources, including access to data and AI models, adequate and appropriate?" |
| RFA | §VI.B, p. 82† (~pp. 94–97) | Criterion 4 (conditional) | Commercialization Potential — "will only be considered by applied technology development applications" |
| RFA | §VI.B, p. 82† (~pp. 94–97) | Criterion 5 | "Is the proposed budget reasonable, well-justified, and appropriate for the scope and scale?" |
| RFA | §VII.A, p. 85† (~pp. 98–99) | OT types | Two options: milestone-based OT (non-negotiable, fast-track) or cost-reimbursement OT |
| RFA | Topic 3-B | **Phase II exclusion (this round)** | **"PHASE II APPLICATIONS WILL NOT BE ACCEPTED IN THIS FOCUS AREA"** — round-specific; Phase I teams can pivot to a different focus area for Phase II in this round, or pursue Phase II under Topic 3B in a future round |
| FAQ v2 (2026-04-10) | Budgets | Cost share | "Cost share is not required … except for-profit entities" |
| FAQ v2 | Budgets | Industry funding | "DOE funding for all participating companies combined could be up to 20%" |
| FAQ v2 | Phase I/II Awards | Phase II scale | "$6 million to $15 million" estimated total Phase II award |
| FAQ v2 | Budgets | Budget period | "July 1, 2026, to March 31, 2027" (9 months) |
| FAQ v2 | Budgets | Focus-area cost share | "Some focus areas in this RFA have further instructions on cost share" — Topic 3B has none |
| FAQ v2 | Application Process, p. 10 | Letters of commitment | "A letter of commitment, signed by a person authorized to commit the participating institution" — official terminology |
| Webinar | Slide 12 | Industry expectation | "expected to be up to 20% of the total requested budget" |
| 2 CFR §200.1/§200.439 | Equipment | Capital threshold (external) | Equipment with per-unit cost ≥$5,000 is "equipment" under federal definition; may require prior written approval — note: external regulation, not stated in RFA; applicability to OT agreements is undetermined until post-selection |
