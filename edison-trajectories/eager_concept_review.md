# Edison Scientific: NSF AM Program Director Review of EAGER Concept Outline

*Edison Scientific LITERATURE_HIGH query — March 2026*

**Question:** Review the EAGER concept outline for the Vertical Cloud Lab as if you were an NSF AM program director, providing detailed feedback on scientific merit, feasibility, budget, strengths, weaknesses, and recommendations.

**Concept reviewed:** [`eager-concept-outline.md`](../eager-concept-outline.md) / [`eager-concept-outline.tex`](../eager-concept-outline.tex)

**PI:** Sterling Baird, Ph.D. — Brigham Young University
**Program:** ENG/CMMI — Advanced Manufacturing (AM)
**Requested Funding:** ~$300K / 2 years

---

## 1. Overall Assessment: Is This Genuinely High-Risk/High-Reward? Is EAGER the Right Mechanism?

**Verdict: EAGER is an appropriate mechanism, but the scope must be significantly narrowed.**

The core question — whether an industrial vertical lift module (VLM) with electrified trays can serve as a viable backbone for multi-instrument autonomous scientific workflows — is genuinely untested. No published literature describes VLMs being repurposed for scientific instrument integration in any discipline. This is not incremental research; it is a fundamentally novel architectural concept for laboratory automation that could fail for reasons ranging from vibration interference to thermal management to the basic question of whether powered instruments can operate reliably on moving trays. This satisfies the high-risk criterion.

The high-reward potential is also credible. If successful, a VLM-based lab architecture that provides 3× the automation-friendly footprint in a compact vertical form factor and enables cloud-accessible alloy discovery would address a well-documented need. NIST SP 1320 explicitly calls for modular autonomous testbed facilities, user-facility models for materials R&D, and standards-based ecosystems — all of which the VCL concept aspires to provide (trautt2024drivingu.s.innovation pages 5-9, trautt2024drivingu.s.innovation pages 1-5). The alloy processability gap is well-documented, with CALPHAD+Bayesian optimization workflows showing clear promise for LPBF alloy design (taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 7-9, taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 1-4).

However, the proposal currently reads as a full autonomous materials discovery system rather than a focused proof-of-concept. An EAGER should answer one or two key questions — here, the primary question should be: *Can a VLM with electrified trays reliably integrate and operate diverse scientific instruments?* The proposal instead promises AI-driven screening, autonomous powder production, parallel LPBF printing, automated characterization, cloud scheduling, AND closed-loop iteration — all within $300K and 2 years. This overreach risks undermining the EAGER case because reviewers may perceive the scope as unrealistic, which paradoxically makes the concept appear less credible rather than more ambitious.

---

## 2. Scientific Merit

**The technical claims are partially well-supported but contain significant gaps.**

**Well-supported claims:**
- The alloy processability gap is a genuine bottleneck. CALPHAD-based screening and Bayesian optimization are demonstrably effective for LPBF alloy design (taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 7-9, taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 1-4, taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 4-7).
- The PI's dual CALPHAD approach (Thermo-Calc/TC-Python for high-fidelity calculations + pycalphad for rapid open-source screening) is technically sound and mirrors the approach validated by AMASE, which demonstrated real-time CALPHAD+active learning for autonomous phase diagram mapping, achieving ~6× speedup over grid search (liang2025realtimeexperimenttheoryclosedloop pages 7-11, liang2025realtimeexperimenttheoryclosedloop pages 3-7, liang2025realtimeexperimenttheoryclosedloop pages 1-3).
- The competitive landscape analysis is largely accurate: APEX uses DED (not LPBF) and produces up to 48 samples/day but lacks autonomous powder production (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8); AMASE operates on thin films only (liang2025realtimeexperimenttheoryclosedloop pages 11-13, liang2025realtimeexperimenttheoryclosedloop pages 1-3).
- Amazemet ultrasonic atomization is validated for small-batch powder production (1 g to a few kg), producing spherical powders suitable for AM, and has been adopted at multiple institutions including Oak Ridge National Laboratory (zach2023sphericalpowderscontrol pages 4-4, ciftcli2025alloydevelopmentfrom pages 1-3, zach2023sphericalpowderscontrol pages 1-2).

**Gaps in the scientific argument:**
- The claim of "autonomous powder production" significantly understates the difficulty. Ultrasonic atomization requires arc/plasma/induction melting with process efficiency ranging from 15–50% depending on heat source and parameters (jedynak2024processabilityofaluminummatrix pages 3-6). Volatile element loss (Zn, Mn evaporation) has been documented as a significant challenge (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6). The proposal does not address how atomization would be robotically automated — currently, this is a highly manual process involving feedstock loading, melting, collection, and sieving.
- The VLM vibration claim (40× optical microscope maintained focus during tray movement) is from a vendor test, not independent validation. The relevant question is not whether a microscope can maintain focus, but whether LPBF printers and ultrasonic atomizers can operate on or adjacent to VLM trays without thermal/vibrational crosstalk.
- The 10–100× throughput increase claim is unsupported by any quantitative analysis. Even APEX, a well-resourced national lab system, produces 48 samples/day — the proposal should provide a realistic throughput estimate based on bottleneck analysis.
- The proposal cites a "€20M German SDL with 0% utilization" and Cooper's modular bot "requiring an entire Ph.D. student's time" — but the Lunt et al. (2024) paper actually demonstrates a functional 12-step autonomous PXRD workflow using three robots, with practical challenges that are typical of early integration work (heterogeneous vendor programming, safety force limits, ~1 hour per PXRD sample) rather than fundamental failure (lunt2024modularmultirobotintegration pages 4-8, lunt2024modularmultirobotintegration pages 8-16, lunt2024modularmultirobotintegration pages 1-4). The negative framing is somewhat misleading.

---

## 3. Feasibility Concerns

**The biggest risks, in order of severity:**

1. **Scope vs. resources mismatch.** The proposal describes building a complete end-to-end autonomous alloy discovery system with one graduate student and ~$91K of non-equipment direct costs over 2 years. The literature consistently shows that multi-instrument autonomous lab integration requires dedicated engineering staff — even well-resourced systems face heterogeneous vendor interfaces, safety constraints, and complex orchestration challenges (wolf2022towardsroboticlaboratory pages 8-12, trautt2024drivingu.s.innovation pages 12-15, seifrid2022autonomouschemicalexperiments pages 8-9). NIST SP 1320 envisions ~35 FTE for a national-scale facility, and even single-workflow autonomous systems like Lunt et al.'s PXRD pipeline required multiple vendor-specific programming languages and orchestration frameworks (lunt2024modularmultirobotintegration pages 4-8, lunt2024modularmultirobotintegration pages 8-16).

2. **Autonomous atomization is not credible at this stage.** The Amazemet system is a manual instrument requiring feedstock preparation, crucible setup, arc/plasma initiation, atmosphere control, and post-processing (sieving, removal of unatomized material, vapor condensate cleaning) (zach2023sphericalpowderscontrol pages 4-4, ciftcli2025alloydevelopmentfrom pages 3-6). Automating this process would be a major robotics challenge in its own right — likely requiring a separate EAGER-scale effort.

3. **Powder changeover for desktop LPBF printers.** The parallel printing strategy is conceptually appealing but the proposal does not address how powder will be loaded, recovered, and changed between different alloy compositions. Cross-contamination between compositions is a fundamental concern in LPBF, and no automation strategy for powder changeover is described. This is particularly critical because the entire value proposition depends on rapid iteration across compositions.

4. **Timeline realism.** Year 1 includes VLM procurement, commissioning, procurement and setup of two LPBF printers, integration of the ultrasonic atomizer, robotic arm integration, AprilTag-based tray identification, cloud scheduling interface development, AND establishment of the CALPHAD screening pipeline. Any one of these tasks could consume a year. Year 2 escalates to full multi-station pipeline operation with external users. This timeline is highly unrealistic without a larger team.

5. **UofT-to-BYU transition.** The fact that the VLM deployment "was not approved at UofT" raises questions about why. If the Acceleration Consortium — one of the world's premier self-driving lab organizations — declined to proceed, the proposal should transparently address what concerns were raised and how BYU's approach differs or mitigates them.

---

## 4. Budget Assessment

| Budget Category | Proposed Amount | % of Total | Assessment/Concern |
|---|---:|---:|---|
| VLM system & electrified trays | $80,000 | 27.0% | High-risk integration backbone; confirm safety, power/data rails, and vibration isolation; expect extra engineering (wolf2022towardsroboticlaboratory pages 26-31, wolf2022towardsroboticlaboratory pages 1-5). |
| 2× Mastrex MX-100 LPBF printers | $78,000 | 26.4% | Parallelization valuable; plan for powder changeover, contamination control, and maintenance; low-cost LPBF may limit performance; add spares/filters (trautt2024drivingu.s.innovation pages 12-15). |
| Graduate student (2 yrs) | $40,000 | 13.5% | Insufficient for scope; integration and operations typically require dedicated engineer/technician support (seifrid2022autonomouschemicalexperiments pages 8-9, trautt2024drivingu.s.innovation pages 12-15). |
| Thermo-Calc licenses/databases (2 yrs) | [licence cost removed] | — | Reasonable for CALPHAD; ensure database coverage (TCFE/TCHEA); leverage pycalphad to control costs (liang2025realtimeexperimenttheoryclosedloop pages 24-29). |
| Integration engineering | $15,000 | 5.1% | Very low given heterogeneous device integration and standards gaps; expect higher effort (wolf2022towardsroboticlaboratory pages 8-12, trautt2024drivingu.s.innovation pages 12-15). |
| Cloud infrastructure/software | $8,000 | 2.7% | Likely inadequate for secure remote scheduling, data management, provenance, and UI; plan for more (canty2025scienceaccelerationand pages 8-9, lo2023reviewoflowcost pages 22-24, silva2024shapingthefuture pages 4-6). |
| Materials and supplies | $8,000 | 2.7% | Lean for powders/consumables, PPE, and filters; anticipate higher recurring costs (trautt2024drivingu.s.innovation pages 12-15). |
| Indirect costs (F&A) | $47,000 | 15.9% | Consistent with 51.5% on MTDC; reduces available funds for integration/ops. |
| Total | $296,000 | 100.0% | Equipment-heavy; minimal contingency; risk of under-resourcing integration and cloud facility needs (trautt2024drivingu.s.innovation pages 5-9, trautt2024drivingu.s.innovation pages 12-15). |


*Table: Line-item breakdown of the proposed $296K EAGER budget with percentage shares and risk-based assessments. Notes highlight where integration and cloud user-facility needs are likely underfunded, referencing standards and infrastructure challenges documented by the community.*

The budget is heavily equipment-weighted (53% of total costs), which is structurally concerning for an integration-intensive project. Key issues:

- **Graduate student support ($40K)** appears to represent partial support for a single student over 2 years (~$20K/yr). This is the sole personnel allocation for a project requiring mechanical integration, software development, robotics programming, CALPHAD implementation, and experimental materials science. The proposal's listed BYU collaborators (Crane, Homer, Killpack) are described as "available for consultation" — unfunded consultation is unreliable as a staffing strategy.
- **Integration engineering ($15K)** is grossly insufficient. The laboratory automation community has documented that integrating even a few vendor instruments requires substantial custom engineering, with systems often requiring proprietary drivers, custom grippers, and bespoke orchestration software (wolf2022towardsroboticlaboratory pages 8-12, trautt2024drivingu.s.innovation pages 12-15, wolf2022towardsroboticlaboratory pages 1-5).
- **Cloud infrastructure ($8K)** cannot deliver a secure, production-quality remote-access scheduling system with livestream monitoring, data management, and provenance tracking. Cloud lab implementations at institutions like CMU required orders-of-magnitude more investment (lo2023reviewoflowcost pages 22-24).
- **Materials and supplies ($8K)** is lean for 2 years of LPBF powder experiments across multiple alloy compositions, especially given that metal powders for AM are expensive and the atomizer itself may have significant consumable costs.
- The budget arithmetic is correct (equipment excluded from MTDC base, 51.5% F&A applied to $91K MTDC = ~$47K), but the allocation leaves effectively no contingency.

---

## 5. Competitive Landscape

| Platform | Institution | Manufacturing Method | Powder Production | Closed-Loop AI | Characterization | Cloud Access | Key limitations |
|---|---|---|---|---|---|---|---|
| VCL (proposed) | Brigham Young Univ. | LPBF with dual desktop printers; VLM-based station integration | In-house ultrasonic atomization (Amazemet) for small-batch custom powders (zach2023sphericalpowderscontrol pages 4-4, ciftcli2025alloydevelopmentfrom pages 1-3, uhlmann2024acomparativeevaluation pages 2-4) | CALPHAD (Thermo-Calc/pycalphad) + Bayesian optimization; autonomous planning intended (liang2025realtimeexperimenttheoryclosedloop pages 3-7, taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 7-9) | SEM/EDS/EBSD; PIP hardness planned | Intended remote user-facility model aligned with NIST SP 1320 vision; cloud scheduling proposed (trautt2024drivingu.s.innovation pages 5-9, trautt2024drivingu.s.innovation pages 17-20, lo2023reviewoflowcost pages 22-24) | Unproven VLM electrified backbone; high integration risk (power/thermal/vibration); autonomous atomization and powder changeover challenging; ambitious scope vs. EAGER budget (trautt2024drivingu.s.innovation pages 12-15) |
| APEX | LLNL | Directed Energy Deposition (DED), not LPBF | No autonomous custom powder production reported (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8) | Integrated with Materials Acceleration Platform (MAP); autonomous design–build–test loop (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8) | Automated prep; optical microscopy; hardness; compression (conn2025selfdrivinglabto pages 1-8) | Not reported as a public cloud user facility (conn2025selfdrivinglabto pages 8-8) | DED modality differs from LPBF processability; no custom powder loop; complex multi-module integration (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8) |
| AMASE | Univ. of Maryland/NIST | Thin-film combinatorial deposition and heating; not 3D printing | N/A (thin films) | Real-time closed-loop active learning + CALPHAD to map phase diagrams (liang2025realtimeexperimenttheoryclosedloop pages 11-13, liang2025realtimeexperimenttheoryclosedloop pages 7-11, liang2025realtimeexperimenttheoryclosedloop pages 24-29, liang2025realtimeexperimenttheoryclosedloop pages 3-7, liang2025realtimeexperimenttheoryclosedloop pages 22-24) | In situ XRD with ML peak detection (liang2025realtimeexperimenttheoryclosedloop pages 7-11, liang2025realtimeexperimenttheoryclosedloop pages 3-7) | Not reported | Thin-film only; does not validate LPBF powder/process interactions (liang2025realtimeexperimenttheoryclosedloop pages 11-13, liang2025realtimeexperimenttheoryclosedloop pages 1-3) |
| PAL 2.0 | Johns Hopkins Univ. | Manual arc melting workflows reported in community discussions; not LPBF | None | Not reported | Not specified in retrieved sources | Not reported | Manual melting; lacks autonomous powder/LPBF loop; limited generality for AM processability (lo2024reviewoflowcost pages 11-12) |
| Cooper group modular SDL | Univ. of Liverpool | Modular multi-robot lab integration for solid-state workflows (e.g., PXRD); not AM | N/A | Orchestrated via ARChemist/ROS; multi-robot coordination; not focused on AI-driven composition optimization (lunt2024modularmultirobotintegration pages 8-16) | Automated PXRD workflow; multi-step sample handling (lunt2024modularmultirobotintegration pages 4-8, lunt2024modularmultirobotintegration pages 1-4) | Not reported | Significant integration effort across heterogeneous vendor software/hardware; safety/force limits; long acquisition times limit utilization (lunt2024modularmultirobotintegration pages 4-8, lunt2024modularmultirobotintegration pages 1-4) |


*Table: Side-by-side comparison of the proposed Vertical Cloud Lab and prominent autonomous lab efforts on manufacturing modality, powder handling, autonomy, characterization, and cloud access. Citations highlight where capabilities are demonstrated and where gaps remain relevant to LPBF alloy discovery.*

The PI's competitive landscape analysis is largely accurate in identifying gaps:

- **APEX (LLNL)** is confirmed as a DED-based autonomous alloy discovery platform with automated sample fabrication, preparation, and characterization, coupled with the Materials Acceleration Platform for ML-driven iteration (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8). It does not use LPBF and does not include autonomous powder production.
- **AMASE (UMD/NIST)** is a thin-film-only system that couples autonomous XRD measurements with real-time CALPHAD/Thermo-Calc thermodynamic modeling, achieving 6× experiment reduction through active learning (liang2025realtimeexperimenttheoryclosedloop pages 7-11, liang2025realtimeexperimenttheoryclosedloop pages 3-7, liang2025realtimeexperimenttheoryclosedloop pages 1-3). It validates experiment-theory closed-loop concepts but does not address LPBF processability.
- **Cooper group (Liverpool)** demonstrated modular multi-robot integration for solid-state chemistry (PXRD), illustrating both the potential and the integration challenges of multi-instrument autonomous workflows (lunt2024modularmultirobotintegration pages 4-8, lunt2024modularmultirobotintegration pages 8-16, lunt2024modularmultirobotintegration pages 1-4).

The genuine differentiation of the VCL would be the combination of custom powder production + LPBF printing + characterization in a closed loop — no existing platform achieves this. However, the differentiation from platforms like A-Lab (Berkeley) and AlabOS-based systems (canty2025scienceaccelerationand pages 8-9) should also be discussed. The PI should also acknowledge that the CALPHAD+Bayesian optimization component, while well-conceived, is not novel — AMASE has demonstrated this, and Taheri-Mousavi et al. (2026) have shown CALPHAD+BO for LPBF alloy design (taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 7-9). The novelty is in the hardware architecture and the end-to-end integration, not the computational approach.

---

## 6. Strengths

1. **Genuinely novel architectural concept.** The VLM-as-lab-backbone idea has no precedent in the literature. If it works, the space efficiency (3× footprint utilization claimed), single-point robotic access, and electrified tray concept could be transformative for modular lab automation.

2. **Well-identified gap in the ecosystem.** The alloy processability gap is real and well-documented (taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 7-9, taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 1-4). No existing platform closes the loop from computational screening through custom powder production to LPBF validation and characterization.

3. **Strong computational pipeline design.** The dual CALPHAD approach (Thermo-Calc for high-fidelity + pycalphad for rapid screening) combined with Bayesian optimization over function networks represents a sophisticated and well-supported computational strategy (liang2025realtimeexperimenttheoryclosedloop pages 7-11, liang2025realtimeexperimenttheoryclosedloop pages 3-7).

4. **PI's relevant expertise.** The PI co-authored the influential "frugal twin" review (79 citations) and has published on minimal self-driving lab implementations, demonstrating understanding of both the vision and practical challenges of autonomous experimentation (lo2024reviewoflowcost pages 1-3, lo2024reviewoflowcost pages 3-4, canty2025scienceaccelerationand pages 8-9).

5. **Strategic alignment with NIST SP 1320.** The cloud user-facility model, modular architecture, and standards-aligned design directly address the NIST roadmap's calls for distributed autonomous testbed facilities and democratized access (trautt2024drivingu.s.innovation pages 5-9, trautt2024drivingu.s.innovation pages 17-20, trautt2024drivingu.s.innovation pages 1-5).

6. **Cost-effective LPBF parallelization.** The insight that sub-$40K desktop LPBF printers enable dual-printer strategies that would be cost-prohibitive with industrial systems ($500K+) is clever and could be a template for other labs.

7. **Leverage of startup funds.** Using ~$220K of startup funds for the ultrasonic atomizer demonstrates institutional commitment and significantly extends the effective budget.

---

## 7. Weaknesses

1. **Critical scope overreach.** The proposal attempts to simultaneously develop a novel lab architecture (VLM backbone), build a cloud user facility, demonstrate autonomous powder production, establish parallel LPBF printing, implement CALPHAD+BO screening, automate characterization, and run a pilot alloy discovery campaign. Each of these is a substantial research effort. This should be 3–5 proposals, not one EAGER.

2. **Insufficient personnel.** One partially-supported graduate student cannot execute this scope. The lack of funded engineering support is the single most critical budgetary weakness, particularly given the literature's consistent finding that multi-instrument integration requires dedicated technical staff (trautt2024drivingu.s.innovation pages 12-15, lunt2024modularmultirobotintegration pages 4-8).

3. **Autonomous atomization is not feasible within scope.** The Amazemet system requires manual feedstock loading, melting control, and post-processing. Automating this involves significant robotics challenges (handling molten metal, inert atmosphere management, sieving/classification) that are not addressed (zach2023sphericalpowderscontrol pages 4-4, ciftcli2025alloydevelopmentfrom pages 1-3, jedynak2024processabilityofaluminummatrix pages 3-6).

4. **Powder contamination strategy absent.** Rapid alloy iteration requires frequent powder changeover in LPBF printers. The proposal does not describe how this will be accomplished without cross-contamination — a problem that typically requires thorough cleaning between materials and is one of the most time-consuming steps in multi-material LPBF research.

5. **Opaque UofT departure.** The VLM concept was developed at the Acceleration Consortium but "not approved" for deployment. The proposal should address what specific concerns or circumstances led to this decision and what the PI learned from the experience.

6. **Unsubstantiated throughput claims.** The "10–100× throughput increase" is stated without analysis. Given that LPBF builds typically take hours, powder atomization takes hours, and characterization takes hours, a realistic bottleneck analysis might show far more modest gains from automation (time savings primarily from eliminating human scheduling delays and enabling overnight operation).

7. **Cloud facility as Year 2 deliverable is premature.** Building a production-quality cloud interface with security, scheduling, data provenance, and external user support is a major software engineering effort. Existing cloud labs (CMU, Emerald) required massive investment (lo2023reviewoflowcost pages 22-24). An $8K allocation is insufficient.

8. **Missing risk mitigation plan.** The proposal identifies risks well but does not provide mitigation strategies or decision points. What happens if VLM vibrations are unacceptable for LPBF? What if the Mastrex MX-100 proves unsuitable for custom alloy powders? What are the go/no-go criteria?

---

## 8. Specific Recommendations

**A. Narrow the scope dramatically.** Reframe the EAGER around a single, testable hypothesis: *Can a VLM with electrified trays serve as a viable integration backbone for a multi-instrument autonomous materials workflow?* The proof-of-concept should demonstrate:
- VLM procurement and electrified tray commissioning
- Integration of 3–4 instruments (e.g., OT-2, AutoTrickler, one LPBF printer, a characterization instrument)
- Automated sample transfer between stations via robotic arm
- A simple closed-loop demonstration (e.g., parameter optimization for a single known alloy, not novel alloy discovery)
Drop the autonomous atomization, cloud user facility, and full alloy discovery campaign from the EAGER scope. These should be deferred to a follow-on proposal.

**B. Rebalance the budget toward personnel.** Consider reducing from two LPBF printers to one (saving ~$39K) and apply savings toward a part-time technician or automation engineer. Alternatively, seek cost-share from BYU for engineering support. The integration engineering line item should be at least $30–40K.

**C. Address the UofT transition transparently.** Include a brief, honest account of why the VLM was not deployed at UofT and what was learned. Frame BYU as a more favorable environment (e.g., lab space availability, startup funds, departmental support) rather than leaving the reader to speculate.

**D. Add explicit go/no-go milestones.** Define quantitative success criteria: e.g., (1) VLM tray positioning repeatability within ±X mm; (2) instrument vibration levels below Y during tray retrieval; (3) successful autonomous completion of N print-characterize cycles without human intervention. These help reviewers evaluate feasibility.

**E. Provide a bottleneck analysis.** Replace the 10–100× throughput claim with a realistic time-and-motion analysis showing expected cycle times for each step (CALPHAD screening: minutes; powder atomization: hours; LPBF printing: hours; characterization: hours; total cycle: days). Show where automation gains come from (e.g., overnight operation, reduced scheduling gaps, parallel printing during changeover).

**F. Engage BYU collaborators more formally.** The listed collaborators (Crane for LPBF, Killpack for robotics, Homer for computational materials) should provide letters of collaboration or small unfunded commitments specifying their roles. "Available for consultation" is too weak for review.

**G. Consider the One Click Metal alternative more seriously.** The cartridge-based powder management system of the BoldSeries may partially address the powder changeover/contamination problem — a single cartridge-based printer might be strategically more valuable than two low-cost printers that require manual powder management.

**H. Strengthen the CALPHAD section.** The computational pipeline is a strength but needs more specificity: Which thermodynamic databases (TCFE12? TCHEA5?) will cover the target alloy systems? What is the target composition space (the Al-based alloys mentioned in Year 2 are too vague)? How will the Bayesian optimization handle the function network topology?

**I. Discuss safety.** Operating an ultrasonic atomizer (arc/plasma melting of metals) and LPBF printers (Class 4 lasers, metal powder handling) in an automated/unattended configuration raises significant EHS concerns. The proposal should address how these will be managed.

---

## Summary Recommendation

This concept has genuine merit and is appropriate for the EAGER mechanism in principle. The VLM-as-lab-backbone idea is truly novel, the alloy processability gap is a real problem, and the PI has relevant expertise in self-driving lab design. However, the proposal in its current form is too ambitious for a $300K/2-year EAGER. The most impactful revision would be to **narrow the scope to a focused VLM integration proof-of-concept**, defer the full alloy discovery campaign and cloud facility to follow-on work, and rebalance the budget to ensure adequate personnel support for the integration engineering that will make or break this project. With these changes, this could be a compelling EAGER submission that, if successful, would provide the credibility needed for a larger follow-on proposal to NSF AM or other programs.

References

1. (trautt2024drivingu.s.innovation pages 5-9): Zachary Trautt, Austin McDannald, Brian DeCost, A Gilad Kusne, and Francesca Tavazza. Driving U.S. innovation in materials and manufacturing using AI and autonomous labs. National Institute of Standards and Technology (U.S.), Aug 2024. URL: https://doi.org/10.6028/nist.sp.1320, doi:10.6028/nist.sp.1320.

2. (trautt2024drivingu.s.innovation pages 1-5): Zachary Trautt, Austin McDannald, Brian DeCost, A Gilad Kusne, and Francesca Tavazza. Driving U.S. innovation in materials and manufacturing using AI and autonomous labs. National Institute of Standards and Technology (U.S.), Aug 2024. URL: https://doi.org/10.6028/nist.sp.1320, doi:10.6028/nist.sp.1320.

3. (taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 7-9): S. Mohadeseh Taheri‐Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mirko Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high‐strength aluminum alloys with coarsening‐resistant microstructures achieved via rapid solidification. Advanced Materials, Oct 2026. URL: https://doi.org/10.1002/adma.202509507, doi:10.1002/adma.202509507. This article has 6 citations and is from a highest quality peer-reviewed journal.

4. (taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 1-4): S. Mohadeseh Taheri‐Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mirko Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high‐strength aluminum alloys with coarsening‐resistant microstructures achieved via rapid solidification. Advanced Materials, Oct 2026. URL: https://doi.org/10.1002/adma.202509507, doi:10.1002/adma.202509507. This article has 6 citations and is from a highest quality peer-reviewed journal.

5. (taheri‐mousavi2026additivelymanufacturablehigh‐strength pages 4-7): S. Mohadeseh Taheri‐Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mirko Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high‐strength aluminum alloys with coarsening‐resistant microstructures achieved via rapid solidification. Advanced Materials, Oct 2026. URL: https://doi.org/10.1002/adma.202509507, doi:10.1002/adma.202509507. This article has 6 citations and is from a highest quality peer-reviewed journal.

6. (liang2025realtimeexperimenttheoryclosedloop pages 7-11): Haotong Liang, Chuangye Wang, Heshan Yu, Dylan Kirsch, Rohit Pant, Austin McDannald, A. Gilad Kusne, Ji-Cheng Zhao, and Ichiro Takeuchi. Real-time experiment-theory closed-loop interaction for autonomous materials science. Science Advances, Jul 2025. URL: https://doi.org/10.1126/sciadv.adu7426, doi:10.1126/sciadv.adu7426. This article has 14 citations and is from a highest quality peer-reviewed journal.

7. (liang2025realtimeexperimenttheoryclosedloop pages 3-7): Haotong Liang, Chuangye Wang, Heshan Yu, Dylan Kirsch, Rohit Pant, Austin McDannald, A. Gilad Kusne, Ji-Cheng Zhao, and Ichiro Takeuchi. Real-time experiment-theory closed-loop interaction for autonomous materials science. Science Advances, Jul 2025. URL: https://doi.org/10.1126/sciadv.adu7426, doi:10.1126/sciadv.adu7426. This article has 14 citations and is from a highest quality peer-reviewed journal.

8. (liang2025realtimeexperimenttheoryclosedloop pages 1-3): Haotong Liang, Chuangye Wang, Heshan Yu, Dylan Kirsch, Rohit Pant, Austin McDannald, A. Gilad Kusne, Ji-Cheng Zhao, and Ichiro Takeuchi. Real-time experiment-theory closed-loop interaction for autonomous materials science. Science Advances, Jul 2025. URL: https://doi.org/10.1126/sciadv.adu7426, doi:10.1126/sciadv.adu7426. This article has 14 citations and is from a highest quality peer-reviewed journal.

9. (conn2025selfdrivinglabto pages 1-8): Shelby Conn and Alex Baker. Self-driving lab to automate the discovery of novel alloys. Office of Scientific and Technical Information (OSTI), Aug 2025. URL: https://doi.org/10.2172/2584738, doi:10.2172/2584738.

10. (conn2025selfdrivinglabto pages 8-8): Shelby Conn and Alex Baker. Self-driving lab to automate the discovery of novel alloys. Office of Scientific and Technical Information (OSTI), Aug 2025. URL: https://doi.org/10.2172/2584738, doi:10.2172/2584738.

11. (liang2025realtimeexperimenttheoryclosedloop pages 11-13): Haotong Liang, Chuangye Wang, Heshan Yu, Dylan Kirsch, Rohit Pant, Austin McDannald, A. Gilad Kusne, Ji-Cheng Zhao, and Ichiro Takeuchi. Real-time experiment-theory closed-loop interaction for autonomous materials science. Science Advances, Jul 2025. URL: https://doi.org/10.1126/sciadv.adu7426, doi:10.1126/sciadv.adu7426. This article has 14 citations and is from a highest quality peer-reviewed journal.

12. (zach2023sphericalpowderscontrol pages 4-4): Michael Zach, Dane Brashear, Jonah Duran, Łukasz Żrodowski, Bartosz Kalicki, Tomasz Choma, Marcin Sołowiow, and Steven Adler. Spherical powders: control over the size and morphology of powders for additive manufacturing and enriched stable isotope nuclear targets. EPJ Web of Conferences, 285:03002, Jan 2023. URL: https://doi.org/10.1051/epjconf/202328503002, doi:10.1051/epjconf/202328503002. This article has 3 citations and is from a peer-reviewed journal.

13. (ciftcli2025alloydevelopmentfrom pages 1-3): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 3 citations.

14. (zach2023sphericalpowderscontrol pages 1-2): Michael Zach, Dane Brashear, Jonah Duran, Łukasz Żrodowski, Bartosz Kalicki, Tomasz Choma, Marcin Sołowiow, and Steven Adler. Spherical powders: control over the size and morphology of powders for additive manufacturing and enriched stable isotope nuclear targets. EPJ Web of Conferences, 285:03002, Jan 2023. URL: https://doi.org/10.1051/epjconf/202328503002, doi:10.1051/epjconf/202328503002. This article has 3 citations and is from a peer-reviewed journal.

15. (jedynak2024processabilityofaluminummatrix pages 3-6): A JEDYNAK, S HÄRTEL, R PIPPIG, and T CHOMA. Processability of aluminum-matrix composite (amc) by ultrasonic powder atomization. Materials Research Proceedings, 41:156-163, May 2024. URL: https://doi.org/10.21741/9781644903131-17, doi:10.21741/9781644903131-17. This article has 0 citations.

16. (ciftcli2025alloydevelopmentfrom pages 3-6): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 3 citations.

17. (lunt2024modularmultirobotintegration pages 4-8): Amy. M. Lunt, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Alexander White, Nicola Rankin, Rob Clowes, Ben Alston, Lucia Gigli, Graeme M. Day, Andrew I. Cooper, and Samantha Y. Chong. Modular, multi-robot integration of laboratories: an autonomous workflow for solid-state chemistry. Chemical Science, 15:2456-2463, Jan 2024. URL: https://doi.org/10.1039/d3sc06206f, doi:10.1039/d3sc06206f. This article has 99 citations and is from a highest quality peer-reviewed journal.

18. (lunt2024modularmultirobotintegration pages 8-16): Amy. M. Lunt, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Alexander White, Nicola Rankin, Rob Clowes, Ben Alston, Lucia Gigli, Graeme M. Day, Andrew I. Cooper, and Samantha Y. Chong. Modular, multi-robot integration of laboratories: an autonomous workflow for solid-state chemistry. Chemical Science, 15:2456-2463, Jan 2024. URL: https://doi.org/10.1039/d3sc06206f, doi:10.1039/d3sc06206f. This article has 99 citations and is from a highest quality peer-reviewed journal.

19. (lunt2024modularmultirobotintegration pages 1-4): Amy. M. Lunt, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Alexander White, Nicola Rankin, Rob Clowes, Ben Alston, Lucia Gigli, Graeme M. Day, Andrew I. Cooper, and Samantha Y. Chong. Modular, multi-robot integration of laboratories: an autonomous workflow for solid-state chemistry. Chemical Science, 15:2456-2463, Jan 2024. URL: https://doi.org/10.1039/d3sc06206f, doi:10.1039/d3sc06206f. This article has 99 citations and is from a highest quality peer-reviewed journal.

20. (wolf2022towardsroboticlaboratory pages 8-12): Ádám Wolf, David Wolton, Josef Trapl, Julien Janda, Stefan Romeder-Finger, Thomas Gatternig, Jean-Baptiste Farcet, Péter Galambos, and Károly Széll. Towards robotic laboratory automation plug &amp; play: the “lapp” framework. SLAS Technology, 27:18-25, Feb 2022. URL: https://doi.org/10.1016/j.slast.2021.11.003, doi:10.1016/j.slast.2021.11.003. This article has 55 citations and is from a peer-reviewed journal.

21. (trautt2024drivingu.s.innovation pages 12-15): Zachary Trautt, Austin McDannald, Brian DeCost, A Gilad Kusne, and Francesca Tavazza. Driving U.S. innovation in materials and manufacturing using AI and autonomous labs. National Institute of Standards and Technology (U.S.), Aug 2024. URL: https://doi.org/10.6028/nist.sp.1320, doi:10.6028/nist.sp.1320.

22. (seifrid2022autonomouschemicalexperiments pages 8-9): Martin Seifrid, Robert Pollice, Andrés Aguilar-Granda, Zamyla Morgan Chan, Kazuhiro Hotta, Cher Tian Ser, Jenya Vestfrid, Tony C. Wu, and Alán Aspuru-Guzik. Autonomous chemical experiments: challenges and perspectives on establishing a self-driving lab. Accounts of Chemical Research, 55:2454-2466, Aug 2022. URL: https://doi.org/10.1021/acs.accounts.2c00220, doi:10.1021/acs.accounts.2c00220. This article has 294 citations and is from a domain leading peer-reviewed journal.

23. (wolf2022towardsroboticlaboratory pages 26-31): Ádám Wolf, David Wolton, Josef Trapl, Julien Janda, Stefan Romeder-Finger, Thomas Gatternig, Jean-Baptiste Farcet, Péter Galambos, and Károly Széll. Towards robotic laboratory automation plug &amp; play: the “lapp” framework. SLAS Technology, 27:18-25, Feb 2022. URL: https://doi.org/10.1016/j.slast.2021.11.003, doi:10.1016/j.slast.2021.11.003. This article has 55 citations and is from a peer-reviewed journal.

24. (wolf2022towardsroboticlaboratory pages 1-5): Ádám Wolf, David Wolton, Josef Trapl, Julien Janda, Stefan Romeder-Finger, Thomas Gatternig, Jean-Baptiste Farcet, Péter Galambos, and Károly Széll. Towards robotic laboratory automation plug &amp; play: the “lapp” framework. SLAS Technology, 27:18-25, Feb 2022. URL: https://doi.org/10.1016/j.slast.2021.11.003, doi:10.1016/j.slast.2021.11.003. This article has 55 citations and is from a peer-reviewed journal.

25. (liang2025realtimeexperimenttheoryclosedloop pages 24-29): Haotong Liang, Chuangye Wang, Heshan Yu, Dylan Kirsch, Rohit Pant, Austin McDannald, A. Gilad Kusne, Ji-Cheng Zhao, and Ichiro Takeuchi. Real-time experiment-theory closed-loop interaction for autonomous materials science. Science Advances, Jul 2025. URL: https://doi.org/10.1126/sciadv.adu7426, doi:10.1126/sciadv.adu7426. This article has 14 citations and is from a highest quality peer-reviewed journal.

26. (canty2025scienceaccelerationand pages 8-9): Richard B. Canty, Jeffrey A. Bennett, Keith A. Brown, Tonio Buonassisi, Sergei V. Kalinin, John R. Kitchin, Benji Maruyama, Robert G. Moore, Joshua Schrier, Martin Seifrid, Shijing Sun, Tejs Vegge, and Milad Abolhasani. Science acceleration and accessibility with self-driving labs. Nature Communications, Apr 2025. URL: https://doi.org/10.1038/s41467-025-59231-1, doi:10.1038/s41467-025-59231-1. This article has 60 citations and is from a highest quality peer-reviewed journal.

27. (lo2023reviewoflowcost pages 22-24): Stanley Lo, Sterling Baird, Joshua Schrier, Ben Blaiszik, Sergei Kalinin, Helen Tran, Taylor Sparks, and Alán Aspuru-Guzik. Review of low-cost self-driving laboratories: the "frugal twin" concept. ChemRxiv, Sep 2023. URL: https://doi.org/10.26434/chemrxiv-2023-6z9mq, doi:10.26434/chemrxiv-2023-6z9mq. This article has 4 citations.

28. (silva2024shapingthefuture pages 4-6): Rafael Ferreira Da Silva, Rob Moore II, Ben Mintz, Rigoberto Advincula, Anees Alnajjar, Luke Baldwin, Craig Bridges, Ryan Coffee, Ewa Deelman, Christian Engelmann, Brian Etz, Millie Firestone, Ian Foster, Panchapakesan Ganesh, Leslie Hamilton, Dale Huber, Ilia Ivanov, Shantenu Jha, Ying Li, Yongtao Liu, Jay Lofstead, Anirban Mandal, Hector Martin, Theresa Mayer, Marshall McDonnell, Vijayakumar Murugesan, Sal Nimer, Nageswara Rao, Martin Seifrid, Mitra Taheri, Michela Taufer, and Konstantinos Vogiatzis. Shaping the future of self-driving autonomous laboratories workshop. ArXiv, Dec 2024. URL: https://doi.org/10.2172/2481197, doi:10.2172/2481197. This article has 17 citations.

29. (uhlmann2024acomparativeevaluation pages 2-4): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Materials, 17:3396, Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 7 citations.

30. (trautt2024drivingu.s.innovation pages 17-20): Zachary Trautt, Austin McDannald, Brian DeCost, A Gilad Kusne, and Francesca Tavazza. Driving U.S. innovation in materials and manufacturing using AI and autonomous labs. National Institute of Standards and Technology (U.S.), Aug 2024. URL: https://doi.org/10.6028/nist.sp.1320, doi:10.6028/nist.sp.1320.

31. (liang2025realtimeexperimenttheoryclosedloop pages 22-24): Haotong Liang, Chuangye Wang, Heshan Yu, Dylan Kirsch, Rohit Pant, Austin McDannald, A. Gilad Kusne, Ji-Cheng Zhao, and Ichiro Takeuchi. Real-time experiment-theory closed-loop interaction for autonomous materials science. Science Advances, Jul 2025. URL: https://doi.org/10.1126/sciadv.adu7426, doi:10.1126/sciadv.adu7426. This article has 14 citations and is from a highest quality peer-reviewed journal.

32. (lo2024reviewoflowcost pages 11-12): Stanley Lo, Sterling G. Baird, Joshua Schrier, B. Blaiszik, Nessa Carson, Ian T. Foster, Andrés Aguilar-Granda, Sergei V. Kalinin, Benji Maruyama, Maria Politi, Helen Tran, Taylor D. Sparks, and Alán Aspuru-Guzik. Review of low-cost self-driving laboratories in chemistry and materials science: the "frugal twin" concept. Digital Discovery, 3:842-868, Jan 2024. URL: https://doi.org/10.1039/d3dd00223c, doi:10.1039/d3dd00223c. This article has 79 citations and is from a peer-reviewed journal.

33. (lo2024reviewoflowcost pages 1-3): Stanley Lo, Sterling G. Baird, Joshua Schrier, B. Blaiszik, Nessa Carson, Ian T. Foster, Andrés Aguilar-Granda, Sergei V. Kalinin, Benji Maruyama, Maria Politi, Helen Tran, Taylor D. Sparks, and Alán Aspuru-Guzik. Review of low-cost self-driving laboratories in chemistry and materials science: the "frugal twin" concept. Digital Discovery, 3:842-868, Jan 2024. URL: https://doi.org/10.1039/d3dd00223c, doi:10.1039/d3dd00223c. This article has 79 citations and is from a peer-reviewed journal.

34. (lo2024reviewoflowcost pages 3-4): Stanley Lo, Sterling G. Baird, Joshua Schrier, B. Blaiszik, Nessa Carson, Ian T. Foster, Andrés Aguilar-Granda, Sergei V. Kalinin, Benji Maruyama, Maria Politi, Helen Tran, Taylor D. Sparks, and Alán Aspuru-Guzik. Review of low-cost self-driving laboratories in chemistry and materials science: the "frugal twin" concept. Digital Discovery, 3:842-868, Jan 2024. URL: https://doi.org/10.1039/d3dd00223c, doi:10.1039/d3dd00223c. This article has 79 citations and is from a peer-reviewed journal.