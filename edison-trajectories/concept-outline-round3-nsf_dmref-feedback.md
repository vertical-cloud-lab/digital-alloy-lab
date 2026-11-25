# Round-3 Edison feedback — nsf_dmref

Task: `4f3ccc3d-84c3-47a7-b8a9-52891f760ebb`

---

(a) FIRST-IMPRESSION
Keep reading. This revision now looks like a real concept note rather than an overstuffed abstract. In the first 30 seconds I see a clear title, a visible process diagram across the top, and an opening section explicitly labeled “Fundamental question.” Those three things buy you attention. The main thing still working against you is density: the first paragraph under the figure is long, and the note still reads like you are trying to prove program fit, technical novelty, and partnership legality all at once.

(b) PROGRAM FIT
This is closer to DMREF than the earlier draft because you now state the scientific question in DMR language: “What controls the printability and elevated-temperature phase stability... in the regime where conventional CALPHAD assessments are sparse and rapid-solidification AM thermal histories drive non-equilibrium phase selection?” That is the right move. The best-fit program element here is DMREF through the Materials Genome Initiative framing: coupled computation, experiment, and data infrastructure aimed at fundamental understanding of phase selection and phase stability.

What still does not fully fit is the amount of proposal real estate spent on process plumbing. “Ultrasonic atomization,” “LPBF parameters,” “feedstock wire / scrap / powder,” and “supply-risk record” keep pulling this toward manufacturing workflow optimization. DMR is not going to fund this because it is a clever feedstock-to-coupon pipeline. The case has to stand or fall on fundamental non-equilibrium thermodynamics and phase selection in dilute Al-MPEA space. Right now the note says that, but it also keeps advertising applied deliverables. If I were reading this for fit, I would say: possible DMREF fit, but only if the full proposal sharply demotes manufacturing optimization and supply-chain framing to enabling context.

(c) PARTNERSHIP STRUCTURE
No absolute showstopper, but still a few things I would flag immediately.

First, the Ames issue is handled better. You now say, “The CMI Hub at Ames... participates as an unfunded collaborator... per DMREF rules Ames brings its own funding.” Good. That removes one obvious compliance problem.

Second, the international structure is better than before because the Germany/Fraunhofer complication appears to be gone. A BYU plus Toronto collaboration is much cleaner than a three-country stack. But the phrase “U. Toronto... Canada track via NSERC” is still too casual for a DMREF concept note. I need to know whether Toronto is an unfunded collaborator with separate support, or whether you are imagining some coordinated but administratively linked effort. NSF will not fund a foreign co-PI in the ordinary sense here, and multi-international-PI structures make these things harder, not easier.

Third, the top diagram includes “LPBF Spear lab, U. Utah,” but Utah is not described in the “Multi-PI structure” paragraph. That creates ambiguity about who is actually in the proposing team, who is a service provider, and who needs budget or subaward treatment.

Fourth, nothing here addresses research security or data/governance posture beyond deposition to the Materials Data Facility. For a one-pager that is fine, but if foreign collaboration remains in the plan, that piece will matter.

BABA is not really the issue for NSF DMREF. The bigger issues are: who is fundable, who is formally on the project, and whether the international collaborator is indispensable enough to justify the complexity.

(d) PRELIMINARY-RESULTS CREDIBILITY
Still the weak point. The preliminary section proves you have hardware and workflow pieces in place: “AMAZEMET rePOWDER UA atomizer installed and operational,” “working pKGFN BOFN implementation,” “Thermo-Calc AM Module simulations,” “CALPHAD jobs on BYU HPC.” That lowers execution risk, but it does not yet prove the central scientific claim for this agency.

What DMREF reviewers will want is evidence that the closed loop can reveal a real gap in current thermodynamic knowledge. The single most valuable additional result would be one concrete prediction-validation example showing that the loop identifies a metastable or unexpected phase outcome in a defined Al-Mn-Cr-Zr composition/process window that standard CALPHAD misses or mis-ranks, and that experiment confirms it. One figure with predicted phase selection vs measured phase ID under rapid solidification would do more than the current list of operational milestones.

(e) FIGURES / LAYOUT / TYPOGRAPHY
Materially improved. There is now an actual top-of-page workflow figure: Feedstock → CALPHAD → pKGFN BOFN → Ultrasonic Atomization → LPBF → Test, plus a dashed “loop closure” return path. That was the right fix.

The page is readable. The text is no longer running off the right edge. Based on the rendered PDF, margins are intact and line lengths are long but acceptable for a one-pager. Font size looks roughly 10 pt body text with bold section heads; I can read it without strain, but it is still dense.

The figure is functional, not polished. It reads as a linear process flow more than a scientific hypothesis diagram. The boxes “Ultrasonic Atomization” and “LPBF” are visually prominent, which again pushes the note toward process engineering. If the real pitch is a closed-loop materials-discovery engine for non-equilibrium phase stability, then CALPHAD, BOFN, and phase-ID feedback should visually dominate. Also, “Spear lab, U. Utah” embedded inside the LPBF box is the sort of partner-label detail that belongs in text or a caption, not in the main schematic.

One more layout point: the lower half is still paragraph-heavy. You fixed the missing figure problem, but not the compression problem. I’d cut 15–20% of the text and use that space for one compact evidence panel or a cleaner three-part structure: question, hypothesis, proof-of-feasibility.

(f) CONCRETE NEXT MOVE
Sterling,

Thanks for sending this revision. This is closer to DMREF: the fundamental question and the closed-loop computation/experiment framing are clearer now. If you want to keep pursuing DMR fit, I’d suggest a short call or a tighter 2-page follow-up that makes the fundamental non-equilibrium phase-stability question primary, clarifies the role/funding status of Toronto and Utah, and shows one concrete prediction-to-validation preliminary result.

(g) RED FLAGS — CURRENT & PENDING / DOUBLE-DIPPING
Better than before, not fully convincing yet. The new scope-separation language is directionally right: “Genesis... funds the autonomous-platform construction... this DMREF funds the scientific use of the CALPHAD-BOFN loop for fundamental Al-MPEA phase-stability research.” That is the correct distinction to try to make.

But if this reached panel in its current form, I would still expect someone to flag overlap risk. Why? Because the DMREF concept still leans heavily on the same integrated platform stack: BOFN, scheduler-like loop logic, atomization, LPBF, and test. If DOE is paying to build the platform and NSF is paying to run the same platform against a specific alloy family, reviewers may reasonably ask whether the DMREF science depends on capabilities that are themselves still platform development.

To survive that scrutiny, the scope split needs to be more operationally explicit than “platform vs published thermodynamics.” I would want to see language along the lines of: DOE supports hardware/software integration and general autonomous infrastructure that is alloy-agnostic; DMREF supports hypothesis-driven studies of non-equilibrium phase selection in a defined Al compositional regime, associated thermodynamic model correction, and the resulting open scientific data products. Without that sharper boundary, I would flag double-dipping as a foreseeable panel issue.

(h) DELTA VS ROUND 2
Materially better:
- The note now contains an actual figure. That matters.
- You added a section explicitly labeled “Fundamental question,” which makes the DMR hook much clearer.
- You added explicit scope-separation language for the pending DOE Genesis Topic 3B proposal.
- The prior cross-border sprawl appears reduced; at least on this page, the Germany piece is gone.
- The page is visually cleaner and no longer has the obvious right-margin failure.

Still weak:
- The pitch still toggles between fundamental phase-stability science and process optimization. The words “printability,” “ultrasonic-atomization parameters,” “LPBF parameters,” and “supply-risk record” keep muddying the center of gravity.
- Preliminary results still show readiness more than discovery. You have infrastructure, not yet the critical scientific proof point.
- The collaboration stack is still not cleanly specified. Toronto and Utah roles are not fully normalized into NSF-style project structure.
- “15-element bounded composition vector” is too broad relative to the more focused chemistry named elsewhere. It sounds like a search-space boast, not a tractable scientific design.

New issues introduced in the revision:
- There is now a mismatch between the focused chemistry in the “Fundamental question” section (“Mn/Cr/Zr/Si/Fe additions”) and the much broader “Al + 15-element bounded composition vector” in the “Idea” section. That inconsistency will make reviewers wonder whether the project is hypothesis-driven or just high-dimensional exploration.
- The figure foregrounds the processing chain more than the scientific inference loop. In fixing the no-figure problem, you may have over-corrected toward workflow.
- The request at the end asks for “confirming program fit... and the multi-PI BYU + Toronto structure,” which is a little too leading. Better to ask whether the concept appears potentially responsive to DMREF and whether a brief call would be useful.

- Discretionary analytical decisions made during the analysis
- Used the rendered PDF itself, rather than text extraction alone, to assess figure presence, margin integrity, and visual emphasis.
- Treated the prior Edison review as the NSF DMREF subsection of task 115ffc21 and used it only to identify deltas, not to restate the earlier critique.
- Interpreted “Toronto... Canada track via NSERC” as an international collaborator with separate support, but flagged it as ambiguous because the concept note does not specify the exact administrative structure.
- Focused the program-fit critique on NSF DMR/DMREF priorities and did not evaluate whether the concept might be stronger for other agencies, except where that affected DMREF fit directly.
