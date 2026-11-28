# Edison Scientific: Mock NSF Program-Officer Memos (3 distinct POs) on EAGER Concept Outline

*Edison Scientific ANALYSIS query — Job: `job-futurehouse-data-analysis-crow-high`*
*Task ID:* `5514f243-a937-4c19-b90b-75d4de5ef54f` (submitted 2026-05-02)
*Uploaded file:* `eager-concept-outline.pdf` → `data_entry:655d386d-98f9-49e4-9ef9-db483fb750a2`
*Submission script:* `/tmp/edison_eager_mock_po.py`

**Question:** Simulate three distinct NSF program officers most likely to be asked to review the EAGER concept outline (FLAIME-VCL Vertical Cloud Lab, PI Sterling Baird, BYU). Pick three real, currently-serving NSF POs; write internal memos in distinct voices; finish with a lead-PO synthesis. The 1-page outline PDF (with both VLM figures) was uploaded so the model could read it directly.

**Concept reviewed:** [`eager-concept-outline.pdf`](../eager-concept-outline.pdf) (compiled from [`eager-concept-outline.tex`](../eager-concept-outline.tex)).

**POs simulated:**

- **PO-1 — Dr. Kevin Chou** (NSF CMMI Advanced Manufacturing; metal LPBF/EBM, thermal modeling) — likely *lead* PO.
- **PO-2 — Dr. Linkan Bian** (NSF CMMI Advanced Manufacturing; data-driven AM, in-situ process monitoring, ML for AM quality) — co-reviewer for the autonomy/AI/BOFN angle.
- **PO-3 — Dr. Alexis Lewis** (NSF DMR Materials Engineering and Processing; microstructure-via-processing, powder/LPBF, 3D characterization) — cross-divisional consult for the powder atomization / microstructure side.

---

## PO-1: Dr. Kevin Chou, NSF CMMI Advanced Manufacturing
**Recommendation:** Approve with revisions
**Confidence:** Medium

**Why this would land on my desk:** Advanced Manufacturing in CMMI is the natural home for an LPBF-centric autonomous workflow proposal that explicitly cites NIST SP 1320 and the alloy processability gap, and the PI puts the unit as ENG/CMMI Advanced Manufacturing on the front matter. The single testable hypothesis is hardware architecture for an LPBF loop, which is squarely within my portfolio.

**What I like:** The concept is unusually disciplined for an EAGER. It commits to one falsifiable hypothesis, “a VLM with electrified trays can reliably integrate and operate diverse scientific instruments as the backbone of an autonomous materials workflow,” and it gives four numerical Y1 go/no-go gates: tray positioning ≤±2 mm, vibration during retrieval <50 µm, ≥20 fully autonomous print→characterize cycles, and ≥24 h continuous powered cross-tray operation. That is exactly the kind of bounded de-risking exercise EAGER is for. I also like that the budget is honest about scope. The outline separates the requested equipment, about $119K for the VLM (~$80K) and Mastrex MX-100 (~$39K), from what is outside the request: the startup-funded ultrasonic atomizer (~$220K) and the BYU EHS work for Class 4 lasers, Class D aluminum fines, NFPA 484, and oxygen monitoring. Finally, the Toronto Acceleration Consortium feasibility study is a useful prior signal. The claim that a single VLM provided 273 ft² of tray area in 92 ft², retrieved any tray in ≤60 s, and preserved 40× optical focus during belt-driven motion is not proof of this system, but it is enough to make the architecture plausible.

**What worries me:** The Mastrex MX-100 desktop LPBF choice is the load-bearing assumption in this whole concept, and the outline gives me no real process-physics case for it. If that machine cannot produce repeatable AlSi10Mg builds with adequate inerting and dimensional consistency, the autonomous loop is just moving weak data around faster. The vibration requirement is also asserted without a measurement plan. I see the <50 µm retrieval threshold, but not how it will be measured, where sensors sit, or what operational windows are allowed during printing. The figures are helpful concept art, but they are not integration drawings. The first figure shows the VLM, operation table, and cross-tray transfer idea clearly, yet I do not see a concrete mechanical layout, cable/power routing approach for electrified trays, or failure handling. The $32K integration-engineering line may be light for the amount of custom integration implied.

**What I would require before approving:** I would require a short LPBF technical addendum that explains why the MX-100 is fit for closed-loop AlSi10Mg work, including atmosphere control and expected print quality. I would require a measurement protocol for the ±2 mm positioning and <50 µm vibration gates, including instruments, sampling, and pass/fail logic. I would require a compact risk-mitigation table covering at least the MX-100, electrified tray power/data delivery, and robotic cross-tray transfer. I would also require real Letters of Collaboration to replace the placeholders, especially for Crane at BYU and the Spear group at Utah.

**Likelihood I would champion this in my division:** Moderate. This is the right shape for an EAGER in Advanced Manufacturing, but I would want the LPBF reliability case and the measurement plan tightened before I signed off.

## PO-2: Dr. Linkan Bian, NSF CMMI Advanced Manufacturing
**Recommendation:** Approve with revisions
**Confidence:** Medium

**Why this would land on my desk:** This would plausibly come to me because the concept is not just about hardware handling. It explicitly proposes Honegumi with Ax/BoTorch and a Bayesian optimization function network acquisition over a CALPHAD pipeline using Thermo-Calc/TC-Python with TCAL8/TCHEA5 and pycalphad pre-screening. That is the data-driven AM and autonomy angle within CMMI Advanced Manufacturing.

**What I like:** The strongest part for me is that the software stack is named, not hand-waved. The preliminary evidence cites “pKGFN BOFN convergence/cost benchmarks” and “vectorized pycalphad equilibria sustained at >100 calcs/s,” which tells me the optimization layer already exists in some operational form. I also like the choice of autonomy metric. The Y1 gate of “≥20 fully autonomous print→characterize cycles (no human between print kickoff and data export)” is the right standard for an EAGER on an autonomous manufacturing backbone. It forces the PI to prove that scheduling, instrument orchestration, and data return all work together. The plan to release the VLM driver on GitHub under vertical-cloud-lab is also a plus because infrastructure EAGERs are more defensible when the tooling is reusable.

**What worries me:** The weak point is the data layer. I still do not know what observations the loop uses. The outline names an optical microscope and a benchtop hardness/PIP station, but it does not specify what features are extracted, what the objective is for the AlSi10Mg pilot, what constraints are enforced, or how noise is handled. A BOFN can be a good fit here, but right now the optimization target is underspecified. I also do not see a real data-management plan at the concept level. If the loop is going to run ≥20 autonomous cycles, I want to know the provenance model, what metadata accompany each build, and whether the PI is storing raw versus derived data. Finally, the concept appears to close the loop only on post-print characterization. That may be the right scope for a $300K EAGER, but then it should say plainly that in-situ process monitoring on the MX-100 is out of scope, rather than leaving readers to infer it.

**What I would require before approving:** I would require a concise data-flow description from instrument to feature extraction to BOFN to next experiment. I would require an explicit optimization problem statement for the AlSi10Mg pilot: objective, design variables, constraints, and what counts as success within a 20-cycle budget. I would require the PI to state directly whether any in-situ monitoring is included or deliberately excluded. I would also ask for a plan to release at least structured experimental data and metadata, not only the VLM driver.

**Likelihood I would champion this in my division:** I would support it as a co-reviewer if CMMI AM leads. The autonomy claim is credible enough for EAGER, but the proposal needs a much cleaner statement of what data the loop actually learns from.

## PO-3: Dr. Alexis Lewis, NSF DMR Materials Engineering and Processing (MEP)
**Recommendation:** Encourage resubmission as standard / decline as DMR co-handle
**Confidence:** Medium

**Why this would land on my desk:** MEP is a plausible cross-divisional stop because the concept touches powder processing, LPBF, and downstream microstructure characterization. The outline mentions operator-assisted ultrasonic atomization, AlSi10Mg printing, and eventual coupling to BYU SEM/EDS/EBSD, which are recognizable MEP themes.

**What I like:** The proposal is at least honest about where the materials science starts and stops. It does not pretend the atomizer is autonomous now; it states “ultrasonic atomizer (operator-assisted, this phase),” which is the right level of restraint. The preliminary evidence includes “SEM/EDS of operator-assisted ultrasonic-atomized Al powders,” so there is at least some materials characterization in hand. I also like that Y2 does not stop at optical microscopy and benchtop hardness. The outline says the loop will couple to BYU SEM/EDS/EBSD, which is where this begins to intersect actual processing-microstructure science. The reference to the alloy processability gap and the role of custom powder atomization also lands with this program.

**What worries me:** From a DMR perspective, this is still fundamentally a hardware integration concept, not a materials science concept. The single testable hypothesis is about whether a VLM with electrified trays can integrate diverse instruments. That may be appropriate for EAGER, but it means the science return for MEP during the funded period is thin. The “pilot closed-loop process-parameter optimization on AlSi10Mg, then a custom composition” is not enough by itself. AlSi10Mg is a standard proving ground, and the custom composition is not defined. I am also not convinced by the characterization stack inside the VLM. Optical microscopy and benchtop hardness are useful screens, but they do not resolve the microstructural variables that would justify claims about alloy discovery. On the powder side, the outline gives me almost nothing on particle size distribution, sphericity, oxygen pickup, or flowability, even though those will determine whether the LPBF data are interpretable.

**What I would require before approving:** If DMR were asked to co-handle or co-fund, I would want a paragraph that clearly states this EAGER is not asking DMR to back a mature materials-science campaign and that the main purpose is hardware de-risking. I would require a powder QC plan covering at least PSD, morphology/sphericity, and oxygen control for the operator-assisted atomizer output. I would require a firmer Y2 statement on how SEM/EDS/EBSD will be integrated into the workflow rather than named as a future aspiration. I would also ask the PI to specify what “custom composition” means in practice.

**Likelihood I would champion this in my division:** Low. I would not want DMR to lead this. If CMMI wants to fund it as a hardware-backbone EAGER, I would not object, but I do not see a strong case for DMR ownership.

## Cross-PO synthesis (lead-PO digest)

**Convergent concerns across all three POs.** The biggest shared concern is that the concept is much sharper on integration milestones than on the quality and interpretability of what the integrated system will produce. Chou wants the LPBF machine case and the measurement protocol behind the ±2 mm and <50 µm thresholds. Bian wants the data model and the BOFN problem statement. Lewis wants the powder QC and the path to meaningful microstructural characterization. These are different versions of the same complaint: the backbone is described more concretely than the scientific payload. All three also converge on the need to replace placeholder collaborations with real commitments and on the absence of a compact risk-mitigation table for a proposal centered on custom hardware integration.

**Divergent concerns.** The main split is not about whether the idea is interesting; it is about where it belongs. Chou and Bian both see a plausible CMMI Advanced Manufacturing EAGER because the hypothesis is narrow, high-risk, and falsifiable. Lewis sees limited DMR value because the funded work does not yet promise strong processing-microstructure science. For an EAGER decision, the lead should weight the CMMI view more heavily. This concept is explicitly framed as “Off-program” hardware-architecture feasibility with no preliminary integration data, which is a much better fit for CMMI EAGER logic than for DMR co-ownership. There is also a smaller divergence on process monitoring: Bian would like the scope boundary around in-situ sensing stated more clearly, while Chou would likely accept a post-print-only loop if the PI is explicit.

**Net recommendation to the lead PO:** Approve with revisions.

**Single most important revision before a formal EAGER request goes in:** The PI should add a one-page risk-and-measurement addendum that ties the hardware concept to credible experimental outputs. At minimum it should cover the MX-100 suitability for closed-loop AlSi10Mg work, the actual protocol for measuring the ±2 mm positioning and <50 µm vibration gates, and fallback plans for the three load-bearing components: the desktop LPBF system, electrified tray power/data delivery, and robotic cross-tray transfer.

- Selected Kevin Chou, Linkan Bian, and Alexis Lewis as the three most plausible officers based on the user-supplied candidates and the concept outline’s stated home in ENG/CMMI Advanced Manufacturing with a plausible DMR cross-divisional consult.
- Treated Kevin Chou as the likely lead because the core hypothesis is LPBF hardware integration rather than general autonomy or materials science.
- Kept the analysis strictly to content visible in the PDF page and the two attached figures, plus the user-provided background assumptions; I did not add external facts about officer portfolios beyond the roles the user proposed.
- Interpreted the PDF’s “placeholder Letter of Collaboration” language as applying at minimum to the Spear group and BYU collaborators named in the outline, and flagged that as a concept-stage weakness.
- Read the DMR role conservatively: Lewis was framed as a plausible but non-leading cross-divisional reviewer, so her memo reflects lower enthusiasm for division ownership rather than hostility to the project itself.
- Because the request was a simulation of internal NSF memos rather than a statistical analysis task, no inferential tests were applicable.
