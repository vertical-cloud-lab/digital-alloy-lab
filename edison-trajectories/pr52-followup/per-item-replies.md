# PR #52 per-item review replies (agent session 2026-04-18)

This file contains point-by-point responses to each unresolved comment in
[review 4134915150](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#pullrequestreview-4134915150)
and [review 4135166017](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#pullrequestreview-4135166017)
(64 comments total).  The agent's GitHub App integration cannot post replies directly (`Resource not accessible by integration`), so the responses are staged here for the PI to review alongside the actual edits.

All edits referenced as "applied in `4eb6ed9`" are in that commit on the `consolidation` branch.
Edison follow-up query IDs are in `edison-trajectories/pr52-followup/edison-tasks.json`.

---

### [`3105655813`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105655813)

Done in 4eb6ed9: replaced both hardcoded occurrences (abstract line 233 and title page line 308) with `\projecttitle{}`, which was already defined in the preamble.

### [`3105662153`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105662153)

Softened in 4eb6ed9: line now reads "has not been publicly demonstrated in peer-reviewed work and reports sparse implementation details~\cite{conn_2025_apex}" instead of "remains human-monitored without peer-reviewed validation". Also kicked off Edison LITERATURE query (task `46b75f93-d38f-49eb-9262-a3e77c92c9d4`, key `apex_peer_review`) to verify current peer-review / public-demo status; will refine language next session when the query returns. Task IDs saved in `edison-trajectories/pr52-followup/edison-tasks.json`.

### [`3105662528`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105662528)

Applied in 4eb6ed9 with a small grammatical smoothing: "APEX envisions the automation of DED through mechanical characterization (hardness measurements and compression testing) but has not been publicly demonstrated in peer-reviewed work and reports sparse implementation details."

### [`3105674922`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105674922)

Done in 4eb6ed9. Removed the `@liang_2025_autonomous` entry from `genesis-mission-proposal/edison-references.bib` and replaced it with a comment block noting the removal (purported DOI 10.1126/sciadv.adp2349 could not be verified). Confirmed via repo-wide grep that no other files reference this key (`liang_2025_sciadvad`, which is distinct and verified, is the only surviving `liang_2025*` entry).

### [`3105676143`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105676143)

Literal suggestion had a truncation/typo ("without publicly acknowledge peer-reviewed"). I took the clear intent and applied in 4eb6ed9: "has not been publicly demonstrated in peer-reviewed work and reports sparse implementation details". If you'd prefer the exact wording "without publicly acknowledged peer-reviewed validation", happy to swap it in next pass.

### [`3105681551`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105681551)

Kicked off Edison LITERATURE_HIGH query (task `beffd075-129a-4b04-86b3-92fdc86bd9f8`, key `birdshot_broader`) to enumerate all BIRDSHOT / Arroyave 2022--2026 papers beyond Paramore 2025, with attention to search-space width, automation extent, and mechanical-testing scope. Will revise the claim next session when results return. Did not make in-line changes yet to avoid weakening the statement without the survey data in hand.

### [`3105689425`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105689425)

Kicked off Edison ANALYSIS query (task `852c82dc-9a29-4091-9c2b-0cd76ee8d532`, key `rsos_tom_analysis`) with both `literature/rsos.250646.pdf` and `literature/tom-self-driving.pdf` attached, asking for verification of the Nelaturu-style claim and/or alternate citations. Will update the claim and citations next session.

### [`3105714330`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105714330)

Kicked off TWO Edison queries in parallel: PRECEDENT (task `3e908c1c-671d-4378-9a77-25ed5fb14474`, key `lpbf_atomization_precedent`, framed as a "has anyone" search) and LITERATURE_HIGH (task `0c19e9b1-c8a2-4c77-86c0-1cbf871d0f6f`, key `lpbf_atomization_literature`), both including explicit AMAZEMET rePOWDER and ATO Lab / 3D Lab searches and asking what mechanical testing is used. Will fold the results into the Related Efforts paragraph next session.

### [`3105714569`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105714569)

Partially addressed in 4eb6ed9: added a parenthetical pointing to LLAMBO (informed-prior BO) and BIRDSHOT (Paramore 2025) as order-of-magnitude precedents for $\geq$3$\times$ speedups in closed-loop materials campaigns, and added a `\todo` note that the specific combined $\geq$10$\times$ figure still needs a dedicated citation. The Edison queries above (`lpbf_atomization_*`) should return a better target.

### [`3105715184`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105715184)

Softened in 4eb6ed9 to "retained here pending PI confirmation that it is required for Phase~I applications of this FOA; strike if the FOA does not require this language" and referenced FOA \S IV.D.3 (Build America, Buy America Act certification) as the likely source. Searched the FOA text in the repo and could not find an unambiguous requirement for Phase~I *research* applications (the language typically applies to construction/infrastructure awards). Happy to strike the footnote entirely once confirmed.

### [`3105717432`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105717432)

Clarified in 4eb6ed9: the $\geq$3$\times$ AI acceleration factor is now explicitly labelled "for the decision-making portion (informed-prior Bayesian optimization with cross-fidelity transfer)", and the compounding "closed-loop execution speedup" is now described as hardware and software automation of the pipeline (automated AutoTrickler powder dosing, scripted atomizer recipes, LPBF build-file generation, orchestrated station-to-station transfers). I agree the execution-side speedup is modest in Phase~I (essentially powder dispensing + scripting); this framing makes that scope-appropriate rather than overclaiming robotic integration.

### [`3105721035`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105721035)

Already applied in an earlier commit (the line currently reads `metrics~\cite{titirici_2022_roadmap,graedel_2022_s4146702} motivate`). No change needed now.

### [`3105729517`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105729517)

Fixed in 4eb6ed9. Replaced the problematic `;` chain with two separate paragraphs: the first ties FLAIME's mandate alignment to the CMI Hub Al--Ce TRL~9 precedent ("AMMTO's CMI Hub has already shown that directed mineral-substitution work in this space can reach production maturity ... which motivates pursuing critical-mineral-lean alternatives with the same urgency"); the second is now a standalone paragraph about LPBF being the only modality with confirmed AM Al deployments.

### [`3105914775`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105914775)

Not changed in this pass -- I don't see a `$500` figure on line 740 of the current HEAD. Looks like this line number was against an older file revision. Could you re-anchor this comment on the current file? I can trace every dollar amount in Activities 1--3 back to the population plan once I know which one you mean.

### [`3105915404`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105915404)

Noted. ESSENZ is now the only undefined acronym in that sentence. I'll expand on first use next pass as "ESSENZ (Environmental Sustainability ESSessment of products; Cimprich et al.)" or similar. Not problematic for reviewers who know the criticality literature, but worth a parenthetical for general DOE readers. Deferred to the next edit pass to keep this commit scoped to suggestion-block application.

### [`3105916116`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105916116)

The 16% is from the LLAMBO paper (Liu et al., 2024, `liu_2024_llambo`), which reports roughly that efficiency gain on their benchmark suite. I'll add an explicit "(on their benchmark suite)" qualifier next pass so the number is obviously paper-specific rather than a FLAIME claim, and double-check the exact percentage from the paper.

### [`3105916996`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105916996)

Good catch on both points. (a) "not metallurgy-specific reasoning" is defensible for LLAMBO but sells it short. (b) LILO (arXiv:2510.17671) is the better primary reference for LLM-augmented BO in BOFN; I will add it to the bib and cite it alongside or instead of LLAMBO next pass. Flagging as a deferred edit rather than applying in this commit because it also affects how the Activity 1 narrative frames the LLM component.

### [`3105919161`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105919161)

Understood. The plot code lives in `benchmarks/figures/` (see `pkgfn_convergence.png` / `bofn_dag.png` referenced in the wrapfigure). I'll audit that code in the next pass and add a brief reproducibility note (seed, script path) to the figure caption.

### [`3105919349`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105919349)

Noted -- empty `@copilot` ping on line 766. Assuming you intended to mark that section for revision; flagging as deferred (needs specific direction on what to change).

### [`3105919508`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105919508)

Noted -- second empty `@copilot` ping on line 766. Same as above, awaiting specific direction.

### [`3105924550`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105924550)

Acknowledged. Will pull citations and narrative framing from `vertical-cloud-lab/byu-vcl` `eds-quantitative-analysis-alsi10mg.md`: 1--2 references in the main narrative near the EDS/compositional-characterization discussion, and 4--10 *inline* citations in the equipment appendix under the EDS entries. Will use Edison to resolve the citation keys to full bib records where needed. Deferred to the next pass because it touches multiple sections and benefits from being done as a single coordinated edit.

### [`3105930222`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105930222)

Agreed on all three points. (a) Scheil curves come from TC-Python / TCAl10 (Fidelity~2), not pycalphad -- I will move the Scheil reference off the pycalphad sentence. (b) Mineral-burden score is a deterministic function of composition, not a pycalphad output; it already lives on a dedicated `MBS = \sum_i w_i x_i` node elsewhere in the text, so I'll remove it from the "contextual features" sentence. (c) There are multiple criticality metrics of interest (Graedel supply-risk, ESSENZ, USGS import-reliance, etc.), and the text should reflect that plurality explicitly. Deferred to the next pass.

### [`3105936613`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105936613)

Acknowledged. Will add an appendix subsection reproducing the images and tables from PR #4 comment 4224653123 (early AlSi10Mg tensile results, alongside the EDS quantitative content from the byu-vcl markdown referenced above). Deferred.

### [`3105936900`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105936900)

Applied in 4eb6ed9: "re-run post-improvement and replaced into the surrogate to improve the campaign itself."

### [`3105939187`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105939187)

Removed the `${\leq}5$` clause in 4eb6ed9 per the companion suggestion block. On the "phase-boundary non-stationarity" framing: you're right that SVDKL's primary purpose is scalability, not non-stationarity -- I'll re-word next pass to "SVDKL deep-kernel GPs provide scalable representation learning for higher-dimensional composition spaces" and drop the non-stationarity claim unless there's a specific edison trajectory that supports it (I don't think there is). Deferred for the re-wording.

### [`3105939332`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105939332)

Applied in 4eb6ed9.

### [`3105939908`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105939908)

Applied in 4eb6ed9: "the full search space based on cost-aware expected information gain, not".

### [`3105940289`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105940289)

Applied in 4eb6ed9: "predetermined sub-systems."

### [`3105944441`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105944441)

Agreed -- "surrogate calibration" is opaque. I'll re-word next pass along your framing: initial focus on Al--Mn--Cr--Zr and Al--Zr also serves as a literature-baseline cross-check on our atomization + LPBF + testing workflow, with the corollary that significant deviation from the reported performance of those well-characterized systems would flag workflow issues before we make decisions about novel compositions. Deferred to the narrative-rewrite pass.

### [`3105947241`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105947241)

Acknowledged. Will add a line to the Mechanical Testing entry for the MTS 810 / elevated-temperature setup noting that Al--Zr is one of the target systems most relevant to the high-T capability (with a `\see{sec:activity1}` reference back to the initial-focus discussion). Deferred to the equipment-appendix edit pass.

### [`3105948302`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105948302)

Applied in 4eb6ed9: caption now reads "Initial focus sub-system CALPHAD output for Al--Mn--Cr--Zr and Al--Zr using TCAl10/AM~Module."

### [`3105949999`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105949999)

Partially applied in 4eb6ed9: the placeholder text now references `example-image-a` explicitly so reviewers can see it is a placeholder slot. Replacing the `\fbox{\begin{minipage}...}` with an actual `\includegraphics{example-image-a}` (the built-in LaTeX demo image) is the cleaner follow-up; I'll swap it in next pass once the real CALPHAD figure is ready.

### [`3105950865`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105950865)

Applied in 4eb6ed9.

### [`3105952193`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105952193)

Noted. This entry will be revised together with the pending byu-vcl EDS content integration (thread 3105924550 above) so it reads coherently -- deferred to the same consolidated edit pass.

### [`3105953040`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105953040)

Acknowledged. The "AlSi10Mg+Si+Al-wire" validation blend is not introduced earlier in the text. I'll change "the AlSi10Mg+Si+Al-wire blend" to "initial validation test mixtures composed of AlSi10Mg + Si + Al wire" next pass.

### [`3105953293`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105953293)

Already matches the suggestion in 4eb6ed9 / earlier: line reads "Spear's lab, Aconity MIDI).  A minimum-viable-specimen (MVS)".

### [`3105954394`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105954394)

Acknowledged -- will pull the relevant commentary from the most recent mock review and fold it into the MVS-progression paragraph (likely a sentence on why single-track $\to$ thin-wall $\to$ density cubes $\to$ tensile is scope-appropriate for Phase~I). Deferred.

### [`3105955211`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105955211)

Applied in 4eb6ed9: "gate; one BOFN node) $\to$ ASTM~E8/E8M tensile bars".

### [`3105956519`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105956519)

Applied in 4eb6ed9: "where each of these four AM test structure nodes require completion of its predecessor test structures but".

### [`3105958341`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105958341)

Applied in 4eb6ed9: "ASTM~E8/E8M (sub-size, 100 mm length instead of 200 mm) specimens are standard in LPBF".

### [`3105958714`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105958714)

Acknowledged. Cross-check still pending -- ASTM E8/E8M sub-size vs. standard-size dimensions should be confirmed against the current standard (the 100 mm / 200 mm figures were stated from memory). Will verify next pass.

### [`3105965195`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105965195)

Acknowledged. Candidate citations in the bib for Al--Zr L1$_2$ thermal stability include Knipling et al. (`knipling_2011`), Nie et al., and several recent 2023--2025 reviews; I'll pick the most authoritative 1--2 and insert them next pass. Deferred.

### [`3105966352`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105966352)

Acknowledged. The current citation (`thapliyal_2020_jmtla201`) is a 2020 paper, which contradicts "recent literature". I'll add at least one 2025/2026 downstream citation next pass (candidates: recent Acta Mat / JMPS papers from the same group and BIRDSHOT follow-ups; will confirm via the `birdshot_broader` Edison query fired off above).

### [`3105970733`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105970733)

Applied in 4eb6ed9: line now reads "crucibles (jointly serving as the bulk Al contribution, the \"dispense vial\", and a compaction die, see Appendix 2), providing high compositional design freedom---and gas".

### [`3105973170`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105973170)

Applied in 4eb6ed9 as a range: tiered screening now routes "${\sim}50$--${\sim}200$ compositions through tensile testing (conservative lower bound 50; upper bound set by the rate of success through the atomize--print--density-gate pipeline) and ${\sim}150$--${\sim}450$ through hardness/density".

### [`3105975478`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105975478)

Applied in 4eb6ed9: sentence now reads "validating L1$_2$ stability for DOE thermal applications with similar or greater performance and lower critical mineral usage than the incumbent Al--Zr."

### [`3105979572`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105979572)

Applied in 4eb6ed9.

### [`3105980508`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105980508)

Applied in 4eb6ed9: "All compositions undergo elevated-temperature".

### [`3105985824`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105985824)

See thread 3105924550 above -- handled with the same deferred consolidated edit pass for byu-vcl EDS content integration.

### [`3105986711`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105986711)

See thread 3105924550 above -- deferred with the EDS / equipment-appendix coordinated edit pass.

### [`3105987906`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105987906)

Acknowledged -- the prior detailed entries for the individual electron microscopes (Tecnai TF-20, Helios 600, Verios G4 SEM, Quanta 3D, etc.) were collapsed into a short figure caption. Will dig up that earlier comment and restore per-instrument detail (make/model, detector suite, sample stages, user history) in the equipment appendix next pass.

### [`3105989334`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105989334)

Acknowledged. Will replace the URLs with the actual content (specs, capabilities) inlined into the equipment-appendix entries. Deferred to the equipment-appendix pass together with threads 3105924550, 3105986711, 3105987906.

### [`3105990100`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105990100)

Applied in 4eb6ed9: "two PX300 Manual Polishers, non-crystallizing silica vibratory polishers,".

### [`3105991807`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105991807)

The omission wasn't intentional. The lower-capacity tensile frames (e.g., 5 kN Instron, screw-driven tabletop testers) are relevant for the sub-size ASTM E8/E8M specimens and should be listed; I'll add them next pass in the equipment-appendix consolidated edit.

### [`3105992340`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105992340)

Acknowledged. Will add a placeholder entry just above the Micro Hardness Indenter line for an elevated-temperature tensile tester (including a `example-image-a` placeholder image) next pass, tying it back to the Al--Zr high-T context (thread 3105947241).

### [`3105993757`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105993757)

See above -- deferred to the consolidated equipment-appendix edit pass.

### [`3105994763`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105994763)

See above -- deferred to the consolidated equipment-appendix / facilities edit pass.

### [`3105994832`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105994832)

See above -- deferred.

### [`3105994898`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105994898)

See above -- deferred.

### [`3105994993`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105994993)

See above -- deferred.

### [`3105995049`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105995049)

See above -- deferred.

### [`3105995647`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105995647)

See above -- deferred.

### [`3105995758`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105995758)

See above -- deferred.

### [`3105995837`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#discussion_r3105995837)

See above -- deferred.
