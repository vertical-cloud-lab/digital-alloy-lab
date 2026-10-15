# §0 — Project Summary / Abstract (Edison Draft)


**FLAIME Project Summary / Abstract (Field 7) — ~251 words, LaTeX-ready**

---

The United States imports 100\% of its manganese and the majority of its chromium and zirconium---elements central to high-performance aluminum alloys for advanced manufacturing. A single supply disruption could idle domestic additive-manufacturing production dependent on these materials. FLAIME (Fast Learning AI for Mineral Efficiency) addresses this vulnerability with an autonomous closed-loop platform that discovers and qualifies aluminum alloys meeting structural performance targets while minimizing critical mineral content, directly supporting DOE Critical Materials Strategy Pillars~2 (Develop Alternatives) and~3 (Materials and Manufacturing Efficiency).

FLAIME integrates Bayesian Optimization over Function Networks (BOFN) with the partial Knowledge Gradient for Function Networks (pKGFN) acquisition function to jointly optimize alloy composition, printability, and mechanical properties across the full powder-to-part pipeline---from CALPHAD screening through ultrasonic and gas atomization, laser powder bed fusion (LPBF), and ASTM~E8 tensile testing. By modeling every manufacturing stage as a node in a cost-aware function-network DAG with an embedded mineral-burden objective, BOFN selects maximally informative experiments at each stage, reducing powder-to-tensile iterations by an estimated 10$\times$ versus conventional design of experiments. No existing self-driving laboratory closes this complete composition-discovery and manufacturing-qualification loop.

Phase~I targets the Al--Mn--Cr--Zr and Al--Zr alloy families, screening $\geq$200 compositions (up to 2~unique compositions/day, 6~days/week) with a discovery yield $\geq$3\%. All experimental data and BOFN models will be hosted on the American Science Cloud as a FAIR-compliant digital thread. The project enters Phase~I at TRL~2 (concept formulated) and targets TRL~4 (closed-loop validated in laboratory) at the conclusion of the 9-month, \$750K effort.

---

**Discretionary analytical/drafting decisions:**

- **Led with the national urgency framing ("100% of its manganese…") rather than the technology or PI.** The population plan and Edison feedback recommended opening with the problem/policy urgency for AMMTO reviewers, following the R14 directive. An alternative valid approach would lead with the platform capability or the FOA topic alignment.

- **Cited DOE CMS Pillars 2 and 3 explicitly rather than the broader set (Pillars 2, 3, and 5).** Pillar 5 (Enabling Activities) is also relevant but was omitted to stay within word budget; including it would require cutting quantitative details. Chose specificity of outcomes over breadth of policy alignment.

- **Used "estimated 10×" for the AI acceleration claim rather than the more conservative "≥3×" Phase I go/no-go target.** The 10× figure comes from the project's AI advantage thesis (BOFN + pKGFN vs. conventional DOE), while the ≥3× target is the minimum go/no-go gate vs. random search. The abstract uses the aspirational thesis figure since the project plan document and AI advantage statement both frame the 10× as the motivating claim, with 3× as the conservative gate.

- **Included both alloy families (Al–Mn–Cr–Zr and Al–Zr) but omitted Cu–Cr–Zr stretch goal.** Cu–Cr–Zr is only ~20% of Phase I effort and introducing it would require additional context about Be-Cu replacement that could not fit in ~250 words without sacrificing quantitative specifics about the primary alloy system.

- **Structured as three paragraphs (problem → method → outcomes) rather than a single-paragraph block or five-paragraph structure.** This three-part structure mirrors the FOA's implicit evaluation flow (why → how → what) and is common in successful DOE proposals, though a single dense paragraph is also an accepted format.

- **Included the "no existing self-driving laboratory" differentiator claim.** This is the strongest competitive positioning identified across multiple Edison iterations (DD-5, Part C #1 of the synthesis). An alternative would soften this to "few existing platforms" but the source documents confirm this is defensible.

- **Omitted PI name, team composition, and co-investigator details from the body text.** Per FOA §IV.C, these are listed separately in the header fields of the Grants.gov form and "do not count against the limit," so narrative space was preserved for technical content. The team details (PI + 2 MS + 10 UG; Valimet subaward) would appear in the header block above the abstract body.

- **Used "discovery yield ≥3%" (overall project target) rather than "≥20% Tier 1 Full Pass rate."** The 3% figure is the PI-confirmed overall discovery yield target; the 20% applies only to the subset of fully tested compositions. The abstract uses the overall figure as it is more conservative and broadly interpretable.
