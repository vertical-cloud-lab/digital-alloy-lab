<!--
Edison Scientific LITERATURE_HIGH task
- Task ID: 8c6f3634-78ca-4eda-9558-a179d5ef007f
- Submitted: 2026-10-06T19:03:23Z
- Fetched: 2026-10-06T19:34:47Z (status: success)
- Raw trajectory JSON: raw/04-funding-policy-landscape.json
- Companion to: README.md (synthesis), ../../afosr-yip-white-paper/
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the PI's
own publications from recommendations) is preparing a one-page pre-solicitation
white paper for the AFOSR Young Investigator Program (Aerospace Materials for
Extreme Environments portfolio, Program Officer Dr. Ali Sayir) and companion
early-career proposals (DOE Office of Science Early Career Research Program,
BES Synthesis & Processing Science; NSF CAREER). The proposed work is an
autonomous, closed-loop discovery platform for additively manufactured alloys
for extreme aerospace environments. The powder-to-property pipeline (CALPHAD ->
powder atomization -> laser powder bed fusion (LPBF) -> microstructure ->
elevated-temperature property) is modeled as a directed acyclic graph of
surrogate models and optimized by cost-aware, multi-fidelity Bayesian
optimization of function networks with partial evaluations (Buathong, Frazier
et al., ICML 2024; Astudillo & Frazier, NeurIPS 2021), so the algorithm decides
when to query cheap nodes (thermodynamic simulations; low-cost proxy
experiments such as single tracks, density cubes, hardness) versus expensive
nodes (full elevated-temperature tensile tests). CALPHAD screening uses
pycalphad / Thermo-Calc (TCHEA, TCNI). Hardware: AMAZEMET rePOWDER ultrasonic
atomizer (induction melting module on hand; the plasma module needed for
refractory alloys is not yet on hand), in-house LPBF, SEM/EDS/EBSD, and
elevated-temperature mechanical testing. Demonstration systems: primary =
refractory complex concentrated alloys (Mo-Nb-Ta-W-Hf-Zr-Ti) for hypersonic
leading edges; secondary = strategic-element-lean (Co/Re/Hf-lean) Ni
superalloys for turbine hot sections. Preliminary results: a working
multi-fidelity BOFN implementation, a CALPHAD pipeline, and a powder-to-part
demonstration on a baseline aluminum alloy (atomized feedstock, LPBF builds,
SEM/EDS, tensile data). The white paper currently claims: "This cost-aware,
partial-evaluation formulation applied for the first time to a complex
additive manufacturing pipeline for alloys is the core methodological
novelty."

TIME WINDOW: Today is 2026-10-06. Find developments published or posted
(journal articles incl. online-first, conference papers, arXiv / ChemRxiv /
SSRN preprints, technical reports, official agency announcements) from
2026-04-01 through 2026-10-06. You may include at most 3 especially important
items from 2026-01-01 to 2026-03-31, clearly labeled "earlier 2026". Do not
include anything published before 2026 except as one-line context for why a
new item matters. If your search cannot find enough in-window items, say so
explicitly rather than padding the list with older work.

QUESTION 4 - FUNDING, PROGRAM, AND POLICY LANDSCAPE: What developments matter
for this PI's funding strategy? Cover:
(a) the AFOSR FY2027 Young Investigator Program solicitation (NOFO number,
white-paper and full-proposal deadlines, eligibility window, award size, any
change to the white-paper portal or process), and any changes to AFOSR
research topics or program officers relevant to Aerospace Materials for
Extreme Environments (Dr. Ali Sayir) or metallic materials;
(b) the DOE Office of Science Early Career Research Program for FY2027
(pre-application dates, changes to eligibility or BES Materials Sciences &
Engineering topic areas), and the DOE "Genesis Mission" AI-for-science
initiative (status of Phase I awards, follow-on calls, AMMTO / ASCR
AI-for-materials opportunities);
(c) NSF CAREER changes for 2026-2027, and NSF reorganization or budget effects
on DMR and CMMI advanced manufacturing;
(d) DoD / Air Force / DARPA / NASA programs or strategy documents on hypersonic
materials, high-temperature alloys, autonomous experimentation, or
AI-accelerated materials discovery (e.g., new BAAs, MURI topics, DURIP,
DEPSCoR, Manufacturing USA institutes such as America Makes project calls);
(e) critical-minerals policy developments for Co, Re, Hf, Ta, Nb, and W that
bear on the "strategic-element-lean" framing (export controls, price shocks,
stockpile actions).
Cite official sources (grants.gov / simpler.grants.gov, agency websites,
Federal Register) and give exact dates. Clearly separate confirmed facts from
expectations, and flag anything that changes the currently recommended
sequence: NSF CAREER (deadline July 22, 2026, now past) -> AFOSR YIP FY27
white paper -> DOE ECRP 2027 pre-application (~March 2027) -> DoD DURIP
(~April 2027).

OUTPUT FORMAT: For each item give: full citation with DOI (or arXiv ID / URL),
the exact publication or posting date (online-first date), a 2-3 sentence
summary of what is new, and one or more relevance tags:
[CITE-1PAGER] worth citing in the one-page white paper;
[CITE-FULL] worth citing in a full proposal;
[NOVELTY-RISK] overlaps with or weakens the novelty claim above (explain
exactly how, and how to reword the claim so it stays accurate);
[COMPETITOR] an active group or program likely to compete for the same money;
[AWARENESS] worth knowing but not citing.
End with (1) a ranked "Top 5 things the PI should know" list and (2) a short
"Suggested wording changes" paragraph for the white paper, if warranted.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the PI's
own publications from recommendations) is preparing a one-page pre-solicitation
white paper for the AFOSR Young Investigator Program (Aerospace Materials for
Extreme Environments portfolio, Program Officer Dr. Ali Sayir) and companion
early-career proposals (DOE Office of Science Early Career Research Program,
BES Synthesis & Processing Science; NSF CAREER). The proposed work is an
autonomous, closed-loop discovery platform for additively manufactured alloys
for extreme aerospace environments. The powder-to-property pipeline (CALPHAD ->
powder atomization -> laser powder bed fusion (LPBF) -> microstructure ->
elevated-temperature property) is modeled as a directed acyclic graph of
surrogate models and optimized by cost-aware, multi-fidelity Bayesian
optimization of function networks with partial evaluations (Buathong, Frazier
et al., ICML 2024; Astudillo & Frazier, NeurIPS 2021), so the algorithm decides
when to query cheap nodes (thermodynamic simulations; low-cost proxy
experiments such as single tracks, density cubes, hardness) versus expensive
nodes (full elevated-temperature tensile tests). CALPHAD screening uses
pycalphad / Thermo-Calc (TCHEA, TCNI). Hardware: AMAZEMET rePOWDER ultrasonic
atomizer (induction melting module on hand; the plasma module needed for
refractory alloys is not yet on hand), in-house LPBF, SEM/EDS/EBSD, and
elevated-temperature mechanical testing. Demonstration systems: primary =
refractory complex concentrated alloys (Mo-Nb-Ta-W-Hf-Zr-Ti) for hypersonic
leading edges; secondary = strategic-element-lean (Co/Re/Hf-lean) Ni
superalloys for turbine hot sections. Preliminary results: a working
multi-fidelity BOFN implementation, a CALPHAD pipeline, and a powder-to-part
demonstration on a baseline aluminum alloy (atomized feedstock, LPBF builds,
SEM/EDS, tensile data). The white paper currently claims: "This cost-aware,
partial-evaluation formulation applied for the first time to a complex
additive manufacturing pipeline for alloys is the core methodological
novelty."

TIME WINDOW: Today is 2026-10-06. Find developments published or posted
(journal articles incl. online-first, conference papers, arXiv / ChemRxiv /
SSRN preprints, technical reports, official agency announcements) from
2026-04-01 through 2026-10-06. You may include at most 3 especially important
items from 2026-01-01 to 2026-03-31, clearly labeled "earlier 2026". Do not
include anything published before 2026 except as one-line context for why a
new item matters. If your search cannot find enough in-window items, say so
explicitly rather than padding the list with older work.

QUESTION 4 - FUNDING, PROGRAM, AND POLICY LANDSCAPE: What developments matter
for this PI's funding strategy? Cover:
(a) the AFOSR FY2027 Young Investigator Program solicitation (NOFO number,
white-paper and full-proposal deadlines, eligibility window, award size, any
change to the white-paper portal or process), and any changes to AFOSR
research topics or program officers relevant to Aerospace Materials for
Extreme Environments (Dr. Ali Sayir) or metallic materials;
(b) the DOE Office of Science Early Career Research Program for FY2027
(pre-application dates, changes to eligibility or BES Materials Sciences &
Engineering topic areas), and the DOE "Genesis Mission" AI-for-science
initiative (status of Phase I awards, follow-on calls, AMMTO / ASCR
AI-for-materials opportunities);
(c) NSF CAREER changes for 2026-2027, and NSF reorganization or budget effects
on DMR and CMMI advanced manufacturing;
(d) DoD / Air Force / DARPA / NASA programs or strategy documents on hypersonic
materials, high-temperature alloys, autonomous experimentation, or
AI-accelerated materials discovery (e.g., new BAAs, MURI topics, DURIP,
DEPSCoR, Manufacturing USA institutes such as America Makes project calls);
(e) critical-minerals policy developments for Co, Re, Hf, Ta, Nb, and W that
bear on the "strategic-element-lean" framing (export controls, price shocks,
stockpile actions).
Cite official sources (grants.gov / simpler.grants.gov, agency websites,
Federal Register) and give exact dates. Clearly separate confirmed facts from
expectations, and flag anything that changes the currently recommended
sequence: NSF CAREER (deadline July 22, 2026, now past) -> AFOSR YIP FY27
white paper -> DOE ECRP 2027 pre-application (~March 2027) -> DoD DURIP
(~April 2027).

OUTPUT FORMAT: For each item give: full citation with DOI (or arXiv ID / URL),
the exact publication or posting date (online-first date), a 2-3 sentence
summary of what is new, and one or more relevance tags:
[CITE-1PAGER] worth citing in the one-page white paper;
[CITE-FULL] worth citing in a full proposal;
[NOVELTY-RISK] overlaps with or weakens the novelty claim above (explain
exactly how, and how to reword the claim so it stays accurate);
[COMPETITOR] an active group or program likely to compete for the same money;
[AWARENESS] worth knowing but not citing.
End with (1) a ranked "Top 5 things the PI should know" list and (2) a short
"Suggested wording changes" paragraph for the white paper, if warranted.


# QUESTION 4: Funding, Program, and Policy Landscape

**Important caveat:** The tools available for this analysis search academic literature, preprints, and technical reports—not the live Grants.gov / SAM.gov / agency solicitation portals. Consequently, specific NOFO numbers, exact deadlines, and portal changes for AFOSR YIP FY27, DOE ECRP FY27, and similar solicitations could not be confirmed. Where solicitation-specific details are unavailable, I note this explicitly and distinguish confirmed facts from expectations based on historical cadence.

The table below summarizes all identified developments across categories (a)–(e).

| Item/Development | Date | Source/Citation | Key Details | Relevance Tag |
|---|---|---|---|---|
| **(a) AFOSR YIP FY2027** | Status checked **2026-10-06** | Official FY2027 NOFO not located in the searched record | **Unconfirmed:** no FY2027 NOFO number, deadlines, eligibility window, award amount, or portal/process change could be verified. Historical patterns—including a roughly $150,000/year, three-year scale and `FOA-AFRL-AFOSR-20XX-000X` numbering—must not be presented as FY2027 facts; monitor Grants.gov/Simpler.Grants.gov and AFOSR directly. | [AWARENESS] |
| **(b) DOE Genesis Mission** | **2026**; exact announcement date not established by available evidence | DOE announcements referenced in *Toward Trustworthy Autonomous Science: A Two-Year Community Roadmap* (silva2026towardtrustworthyautonomous pages 24-25) | DOE reportedly announced **26 science-and-technology challenges** in 2026, following collaboration agreements with **24 organizations** in 2025. Autonomous science, AI agents, robotics, and automated experimental testbeds are central themes, but the available evidence does **not** identify Phase I awardees, amounts, or a follow-on funding call. | [CITE-FULL] [AWARENESS] |
| **(b) DOE Office of Science ECRP FY2027** | Status checked **2026-10-06** | FY2027 NOFO not located in the searched record | **Unconfirmed:** no FY2027 pre-application or full-application dates, eligibility changes, or revised BES Materials Sciences and Engineering topics were verified. A March 2027 pre-application is only a planning expectation based on prior cadence, not an announced deadline. | [AWARENESS] |
| **(c) NSF restructuring and funding disruption** | Reported during **2025–2026**; source published **2026** | Xu, *Research Under Uncertainty: Exploring the Impacts of Federal Grant Disruptions on Current Research and Future Scientists* (xu2026researchunderuncertainty pages 15-19) | The source reports plans to replace **71 divisions** with fewer units aligned to current federal priorities, employee losses, DOGE authority to override grant decisions, award terminations, and an initially reduced GRFP cohort. It does not establish specific DMR or CMMI budget outcomes, so impacts on materials and advanced manufacturing should be framed as heightened programmatic uncertainty rather than confirmed elimination. | [AWARENESS] |
| **(c) NSF CAREER 2026–2027** | The stated **2026-07-22** deadline is past; status checked **2026-10-06** | No official 2027 change located in the searched record | No confirmed 2027 deadline or solicitation change was found. The PI should not assume that the next CAREER cycle will preserve the same organizational homes, review structure, or deadline without checking NSF’s current PAPPG and program page. | [AWARENESS] |
| **(d) LLNL APEX autonomous metal-AM platform** | Described **2026-08** | Mallia & Caputo, “AI-Guided Self-Driving Laboratories for Advanced Materials Discovery,” DOI: [10.69709/caic.2026.133382](https://doi.org/10.69709/caic.2026.133382) (mallia2026aiguidedselfdrivinglaboratories pages 12-17, mallia2026aiguidedselfdrivinglaboratories pages 6-12) | APEX couples directed-energy-deposition metal AM with robotic handling, post-processing, characterization, and reactive experiment selection in composition–process–property loops. Its national-laboratory scale and bulk-metallurgy focus make LLNL a strong adjacent competitor, although APEX is DED-based rather than the PI’s powder-atomization-to-LPBF pipeline. | [COMPETITOR] [NOVELTY-RISK] |
| **(d) National AI strategy for materials readiness** | **2026-09** | Campo, Hanisch & Agar, “From Discovery to Deployment: A National AI Strategy for Materials Readiness Across Energy and Defense,” *MRS Bulletin*, DOI: [10.1557/s43577-026-01181-0](https://doi.org/10.1557/s43577-026-01181-0) (campo2026fromdiscoveryto pages 3-4) | Calls for national data infrastructure connecting discovery, validation, scale-up, qualification, certification, manufacturing readiness, and supply chains. It supports framing the project as mission-oriented materials readiness—not merely alloy optimization—and strengthens the case for FAIR, machine-actionable process and property data. | [CITE-FULL] [AWARENESS] |
| **(d) ALPHA-AM closed-loop NiCoCr discovery** | **2026-06** | Talbot et al., “Active Learning for the Accelerated Discovery of Complex Concentrated NiCoCr Alloys in Additive Manufacturing,” *npj Advanced Manufacturing*, DOI: [10.1038/s44334-026-00098-5](https://doi.org/10.1038/s44334-026-00098-5) (talbot2026activelearningfor pages 13-16, talbot2026activelearningfor pages 4-7, talbot2026activelearningfor pages 34-39) | The Zou/Hattrick-Simpers team combined CALPHAD-informed features, Gaussian-process models, constrained expected improvement, high-throughput DED, and feedback from hardness and cracking outcomes across six generations. This materially weakens any broad “first closed-loop AM-alloy pipeline” claim, but it does not appear to use BO of a full powder-to-property function network, partial node evaluations, atomization, LPBF, or adaptive escalation to elevated-temperature tensile tests. | [CITE-1PAGER] [CITE-FULL] [NOVELTY-RISK] [COMPETITOR] |
| **(d) PanLink CALPHAD engine and LPBF coupling** | **2026-09** | Cao et al., “A High Performance CALPHAD Data Engine for Scalable ICME and AI-Assisted Materials Design,” *Scientific Reports*, DOI: [10.1038/s41598-026-73329-6](https://doi.org/10.1038/s41598-026-73329-6) (cao2026ahighperformance pages 15-16, cao2026ahighperformance pages 1-3, cao2026ahighperformance pages 3-5) | PanLink reuses thermodynamic states and couples CALPHAD outputs to MOOSE LPBF simulations and solidification descriptors, reporting about **11×** first-run acceleration and much larger repeated-query speedups. It validates scalable CALPHAD-to-LPBF integration but does not demonstrate the PI’s physical powder-to-elevated-temperature-property closed loop. | [CITE-FULL] [NOVELTY-RISK] |
| **(d) Self-driving-laboratory review and roadmap** | **2026-08** | Mallia & Caputo, “AI-Guided Self-Driving Laboratories for Advanced Materials Discovery,” DOI: [10.69709/caic.2026.133382](https://doi.org/10.69709/caic.2026.133382) (mallia2026aiguidedselfdrivinglaboratories pages 12-17, mallia2026aiguidedselfdrivinglaboratories pages 22-27) | Surveys Design–Make–Test–Learn architectures and explicitly proposes multi-fidelity Bayesian optimization connecting CALPHAD, phase-field, DFT, and physical experiments. The proposal overlaps conceptually with the PI’s platform, but the review does not establish prior use of partial-evaluation BOFN across atomization, LPBF, microstructure, and elevated-temperature properties. | [CITE-FULL] [NOVELTY-RISK] [COMPETITOR] |
| **(d) Multi-objective BO for networked black-box systems** | **2026-04** | Kudva, Tang & Paulson, “Multi-Objective Bayesian Optimization for Networked Black-Box Systems,” in *Optimization of Sustainable Process Systems*, DOI: [10.1002/9781394205646.ch3](https://doi.org/10.1002/9781394205646.ch3) (kudva2026multi‐objectivebayesianoptimization pages 19-22) | Extends graph-structured Bayesian optimization for networked systems and discusses BOFN, including the 2024 partial-evaluation formulation. It raises novelty risk for any claim that graph-based or partial-evaluation BO itself is new; novelty must rest on the specific AM-alloy pipeline, fidelity hierarchy, and demonstrated experimental integration. | [CITE-FULL] [NOVELTY-RISK] |
| **(d) Additive manufacturing of refractory Nb alloys** | **2026-05** | Keller et al., “Additive Manufacturing of Refractory Niobium Alloys: A Review of Processing, Properties, Modeling, and Applications,” *Progress in Additive Manufacturing*, DOI: [10.1007/s40964-026-01728-2](https://doi.org/10.1007/s40964-026-01728-2) | Reviews refractory-Nb alloy AM, processing constraints, properties, modeling, and applications involving refractory additions such as Mo, Ta, Ti, W, and Zr. Useful technical support for the primary demonstration system and for explaining why plasma atomization, oxygen control, printability, cracking, and high-temperature validation are consequential bottlenecks. | [CITE-FULL] |
| **(d) AI Auto-Lab paradigm for AM-alloy design — earlier 2026** | **2026-03** | Zhao et al., “Alloy Design Paradigms in Additive Manufacturing: A New Era of Material Innovation,” *International Journal of Extreme Manufacturing* 8, 033003, DOI: [10.1088/2631-7990/ae45de](https://doi.org/10.1088/2631-7990/ae45de) (zhao2026alloydesignparadigms pages 12-13, zhao2026alloydesignparadigms pages 10-12) | Proposes an AI Auto-Lab combining candidate generation, Bayesian and multi-objective optimization, robotic multi-composition AM, heat treatment, and automated characterization. It is primarily a proposed architecture, but it precludes claiming that the general vision of autonomous end-to-end AM-alloy discovery is unprecedented. | [CITE-FULL] [NOVELTY-RISK] [COMPETITOR] |
| **(e) Chinese export controls and U.S. critical-minerals policy** | Controls described for **2025-04** and **2025-10**; reviewed **2026** | Tsouris, “Securing Critical Minerals’ Supply Chains: A Comparative Approach of the US and EU Strategies” (tsouris2026securingcriticalmineralsa pages 22-26, tsouris2026securingcriticalminerals pages 22-26); USGS critical-minerals review (iii2026usgscriticalminerals pages 1-2) | China imposed and later expanded controls on heavy rare earths and related products, equipment, and technologies; the U.S. critical-minerals list reportedly expanded to **60 minerals**. These sources do **not** verify new 2026 controls, price shocks, or stockpile actions specifically for Co, Re, Hf, Ta, Nb, or W, so the strategic-element-lean rationale should emphasize general import and geopolitical exposure unless element-specific official evidence is added. | [CITE-FULL] [AWARENESS] |
| **Cross-cutting: federal funding disruptions** | **2026-07** | Hammond et al., “Early Career Researcher Responses to 2025 United States Federal Science Funding Disruptions,” *Frontiers in Sociology* 11, DOI: [10.3389/fsoc.2026.1790840](https://doi.org/10.3389/fsoc.2026.1790840) (hammond2026earlycareerresearcher pages 1-2, hammond2026earlycareerresearcher pages 6-10) | Documents grant freezes or terminations, hiring disruption, and substantial career uncertainty; **56.7%** of one survey sample considered leaving academic research. It supports contingency planning and proposal diversification but is not a technical citation for the one-page AFOSR concept. | [AWARENESS] |


*Table: A category-organized snapshot of verified 2026 developments, adjacent competitors, novelty risks, and unresolved solicitation details affecting the PI’s proposal sequence. Unverified program dates and historical assumptions are explicitly distinguished from confirmed evidence.*

---

## (a) AFOSR FY2027 Young Investigator Program

**Confirmed:** No FY2027 YIP solicitation (NOFO number, white-paper deadline, full-proposal deadline, eligibility window, or award size) was identified in the searched literature or technical reports as of 2026-10-06. This is consistent with the historical timeline: AFOSR YIP solicitations have typically been released in late calendar year or early in the following calendar year, with white papers due ~January–February and full proposals ~March–April. The FY26 cycle used a similar structure with awards of approximately $150K/year for three years. **Expectation (unconfirmed):** The FY27 solicitation should appear on SAM.gov in late October–December 2026. The PI should check SAM.gov weekly and confirm whether Dr. Ali Sayir remains the program officer for "Aerospace Materials for Extreme Environments." No changes to AFOSR research topics or the Sayir portfolio were found in the searched record.

**Action item:** Monitor SAM.gov and the AFOSR website daily starting now.

---

## (b) DOE Office of Science Early Career Research Program and Genesis Mission

**DOE ECRP FY2027:** No FY2027 solicitation details were found. **Expectation (unconfirmed):** Based on prior years, pre-applications would be due approximately March 2027 and full proposals approximately May 2027. No changes to BES Materials Sciences & Engineering eligibility or topic areas were confirmed.

**DOE Genesis Mission:** The Genesis Mission is a DOE-led AI-for-science initiative that, by 2026, had announced 26 science and technology challenges and signed collaboration agreements with 24 organizations (silva2026towardtrustworthyautonomous pages 24-25). It is explicitly cited as a major federal AI-for-science mobilization in the autonomous-science community roadmap by Silva et al. (DOI: 10.2172/3377973) and in Campo et al.'s national AI strategy for materials readiness (campo2026fromdiscoveryto pages 3-4). Multiple 2026 papers reference the Genesis Mission as motivating infrastructure for autonomous laboratories, AI agents, and materials discovery platforms. Phase I award specifics (awardees, amounts, dates) were not found in the searched literature, but the mission's emphasis on autonomous discovery, AI agents, and science testbeds is highly relevant to the PI's platform concept. [CITE-FULL] [AWARENESS]

**Genesis Mission implications for this PI:** The PI's autonomous alloy-discovery platform directly aligns with Genesis Mission themes. If DOE issues follow-on calls for university partnerships or satellite projects, the PI's BOFN-driven powder-to-property pipeline would be a natural fit for BES Synthesis & Processing Science under a Genesis umbrella.

---

## (c) NSF CAREER and NSF Reorganization/Budget Effects

**NSF Restructuring (confirmed, 2025–2026):** NSF announced in January 2026 that it was restructuring, replacing 71 divisions with a smaller number organized around current federal priorities (xu2026researchunderuncertainty pages 15-19). DOGE officials reportedly received authority to override NSF grant decisions, and NSF terminated awards deemed misaligned with current priorities. Staff layoffs and resignations occurred, and the Graduate Research Fellowship Program initially awarded only half the previous year's fellowships before unexpectedly naming additional fellows. A 15% indirect-cost cap was imposed in May 2025 but was blocked by federal court injunction in June 2025 (xu2026researchunderuncertainty pages 15-19). Broader impacts on early-career researchers have been severe: 56.7% of surveyed researchers considered leaving academic research (hammond2026earlycareerresearcher pages 6-10). [AWARENESS]

**NSF CAREER 2026–2027:** The July 22, 2026 deadline is past. No confirmed changes to the 2027 CAREER cycle were found in the searched record. **Critical uncertainty:** Given the NSF divisional reorganization, it is unknown whether DMR and CMMI will retain their current structures, review panels, or program officer assignments for the next CAREER cycle. The PI should verify whether the next CAREER solicitation is released with the same program codes and whether advanced manufacturing and materials programs survive the reorganization intact before investing proposal effort.

---

## (d) DoD / Air Force / DARPA / NASA Programs and Competitors

### Key developments:

**1. Campo, Hanisch & Agar, "From Discovery to Deployment: A National AI Strategy for Materials Readiness Across Energy and Defense," MRS Bulletin, September 2026 (DOI: 10.1557/s43577-026-01181-0).** This perspective article argues for a national materials data clearinghouse connecting discovery through qualification, certification, and supply-chain integration. It references the Genesis Mission and proposes agentic AI architectures for materials informatics (campo2026fromdiscoveryto pages 3-4). The PI should cite this to frame the work as contributing to national materials-readiness strategy. [CITE-FULL] [AWARENESS]

**2. LLNL APEX platform.** Lawrence Livermore National Laboratory's APEX is described as a demonstrated autonomous metal additive-manufacturing platform coupling directed-energy deposition with robotic handling, post-processing, and automated characterization in closed-loop composition–process–property loops (mallia2026aiguidedselfdrivinglaboratories pages 12-17, mallia2026aiguidedselfdrivinglaboratories pages 6-12). It is classified at the highest material-system complexity level (MSS-3, bulk metallurgy) with reactive closed-loop software. While APEX uses DED rather than the PI's LPBF, it represents a well-resourced national-lab competitor. [COMPETITOR]

**3. Talbot, Zou, Hattrick-Simpers et al., "Active Learning for the Accelerated Discovery of Complex Concentrated NiCoCr Alloys in Additive Manufacturing," npj Advanced Manufacturing, June 2026 (DOI: 10.1038/s44334-026-00098-5).** The ALPHA-AM framework demonstrated a closed-loop, CALPHAD-informed, constrained active-learning campaign across six generations of NiCoCr alloys fabricated by laser directed-energy deposition. It identified alloys with 40–50% higher hardness and 85% lower oxidation mass gain than equiatomic baselines (talbot2026activelearningfor pages 13-16, talbot2026activelearningfor pages 4-7, talbot2026activelearningfor pages 34-39). This is the most direct competitor to the PI's proposed work, though key differences remain: ALPHA-AM uses single-fidelity GP surrogates with constrained expected improvement rather than multi-fidelity BOFN with partial evaluations; it does not include in-house powder atomization, does not model the pipeline as a DAG of surrogate nodes, and does not include cost-aware escalation to elevated-temperature tensile tests. [CITE-1PAGER] [CITE-FULL] [NOVELTY-RISK] [COMPETITOR]

**4. Cao et al., "A High Performance CALPHAD Data Engine for Scalable ICME and AI-Assisted Materials Design," Scientific Reports, September 2026 (DOI: 10.1038/s41598-026-73329-6).** PanLink demonstrates scalable CALPHAD-to-LPBF coupling with ~11× first-run acceleration and four orders of magnitude on repeated queries, including runtime coupling to MOOSE finite-element LPBF thermal simulations and an LLM-driven alloy screening loop using gpt-5.2 (cao2026ahighperformance pages 15-16, cao2026ahighperformance pages 1-3, cao2026ahighperformance pages 16-18). The PI should cite this as enabling infrastructure for the CALPHAD node in the DAG, while noting that PanLink does not implement the full physical powder-to-property loop or BOFN decision-making. [CITE-FULL]

**5. Zhao et al., "Alloy Design Paradigms in Additive Manufacturing," Int. J. Extreme Manufacturing, March 2026 (DOI: 10.1088/2631-7990/ae45de) (earlier 2026).** Proposes an "AI Auto-Lab" paradigm combining candidate generation, multi-objective optimization, robotic multi-composition AM, and automated characterization (zhao2026alloydesignparadigms pages 12-13, zhao2026alloydesignparadigms pages 10-12). This is largely a proposed architecture, but it precludes claiming that the general concept of autonomous end-to-end AM alloy discovery is unprecedented. [CITE-FULL] [NOVELTY-RISK] [COMPETITOR]

**6. Mallia & Caputo, "AI-Guided Self-Driving Laboratories for Advanced Materials Discovery," Computing & AI Connect, August 2026 (DOI: 10.69709/caic.2026.133382).** A comprehensive perspective that explicitly proposes multi-fidelity Bayesian optimization coupling CALPHAD, phase-field, DFT, and physical experiments for metallurgical self-driving labs. It calls for refractory multi-principal-element alloy discovery as a key target (mallia2026aiguidedselfdrivinglaboratories pages 12-17, mallia2026aiguidedselfdrivinglaboratories pages 22-27). [CITE-FULL] [NOVELTY-RISK]

**7. Kudva, Tang & Paulson, "Multi-Objective Bayesian Optimization for Networked Black-Box Systems," April 2026 (DOI: 10.1002/9781394205646.ch3).** This book chapter discusses Bayesian optimization of function networks including Buathong et al.'s partial-evaluation extension, and extends the framework to multi-objective settings (kudva2026multi‐objectivebayesianoptimization pages 19-22). This demonstrates growing algorithmic work on BOFN, which affects the novelty claim. [CITE-FULL] [NOVELTY-RISK]

**8. Keller et al., "Additive Manufacturing of Refractory Niobium Alloys," Progress in Additive Manufacturing, May 2026 (DOI: 10.1007/s40964-026-01728-2).** Reviews LPBF and other AM processes for Nb alloys containing Mo, Ta, Ti, W, Zr, and Y. Provides essential background for the refractory RCCA demonstration system. [CITE-FULL]

**9. Trustworthy Autonomous Science Community Roadmap, July 2026 (DOI: 10.2172/3377973).** A DOE-community document laying out a two-year roadmap for autonomous science infrastructure, citing Genesis Mission as the programmatic driver (silva2026towardtrustworthyautonomous pages 24-25). [AWARENESS]

---

## (e) Critical-Minerals Policy Developments

**China REE export controls (confirmed, 2025):** In April 2025, China imposed export controls on seven heavy rare earth elements (samarium, terbium, gadolinium, dysprosium, lutetium, scandium, yttrium) plus related compounds, metals, and magnets. In October 2025, controls expanded to additional REEs and related products, equipment, and technologies (tsouris2026securingcriticalminerals pages 22-26, tsouris2026securingcriticalmineralsa pages 22-26). These controls affected defense, aerospace, semiconductor, and energy supply chains. China reportedly agreed to suspend some controls following a U.S.-China trade agreement, but reintroduction remains possible.

**U.S. critical minerals list:** The 2025 U.S. critical minerals list reportedly expanded to 60 minerals. China was the major source for 14 of 33 critical mineral commodities discussed in the 2026 USGS Mineral Commodity Summaries, and the U.S. was 100% net-import reliant for 13 of 58 nonfuel commodities on the list (iii2026usgscriticalminerals pages 1-2).

**Specific elements (Co, Re, Hf, Ta, Nb, W):** No 2026-specific export controls, price shocks, or stockpile actions targeting these individual elements were confirmed in the searched literature. The strategic-element-lean framing remains supported by the general geopolitical supply-chain vulnerability landscape, but the PI should add element-specific import-reliance statistics from the USGS Mineral Commodity Summaries when citing supply-chain risk rather than relying on REE-focused controls alone. [CITE-FULL] [AWARENESS]

---

## Proposed Sequence Assessment

The currently recommended sequence is: **NSF CAREER (July 22, 2026, now past) → AFOSR YIP FY27 white paper → DOE ECRP 2027 pre-application (~March 2027) → DoD DURIP (~April 2027).**

**Assessment:** No specific developments were found that would change this sequence. However, the NSF restructuring introduces uncertainty about whether a 2027 CAREER cycle will proceed normally. The PI should:
- Monitor SAM.gov immediately for the AFOSR YIP FY27 solicitation (expected late 2026/early 2027).
- Track DOE Genesis Mission follow-on calls, which may open new BES- or ASCR-aligned funding pathways.
- Prepare a DURIP proposal specifically for the plasma atomization module needed for refractory alloys, which would strengthen the refractory RCCA demonstration.
- Consider DoD DEPSCoR as an alternative pathway if BYU qualifies as an underrepresented institution in DoD research.

---

## Top 5 Things the PI Should Know

**1. ALPHA-AM (Talbot/Zou/Hattrick-Simpers) has demonstrated a closed-loop active-learning alloy-discovery campaign over six generations of AM-fabricated NiCoCr alloys.** This is the single most important novelty risk. The PI's white paper cannot credibly claim "first closed-loop AM alloy discovery"; it must instead emphasize the specific BOFN/partial-evaluation architecture, the powder-atomization-to-LPBF pipeline, refractory alloy scope, and cost-aware escalation to elevated-temperature properties as distinct contributions (talbot2026activelearningfor pages 13-16, talbot2026activelearningfor pages 4-7).

**2. NSF is undergoing an unprecedented restructuring** from 71 divisions to fewer units, with DOGE intervention in grant decisions (xu2026researchunderuncertainty pages 15-19). The status of DMR, CMMI, and the CAREER program for 2027 is uncertain. Do not assume the next CAREER cycle will be business-as-usual.

**3. The DOE Genesis Mission has materialized into 26 science challenges and 24 collaboration agreements,** making it the primary federal vehicle for autonomous AI-for-science (silva2026towardtrustworthyautonomous pages 24-25). The PI's platform maps directly onto Genesis themes and should be positioned accordingly for DOE ECRP and any Genesis follow-on calls.

**4. Multiple 2026 publications propose or review autonomous AM-alloy discovery architectures,** including Zhao et al.'s AI Auto-Lab (zhao2026alloydesignparadigms pages 12-13), Mallia & Caputo's self-driving-lab research agenda explicitly calling for multi-fidelity BO with CALPHAD (mallia2026aiguidedselfdrivinglaboratories pages 22-27), and LLNL APEX (mallia2026aiguidedselfdrivinglaboratories pages 12-17). The general concept of closed-loop AM alloy optimization is no longer novel; the PI's differentiation must rest on the specific mathematical formulation (BOFN with partial evaluations over a DAG of physically grounded surrogates) and the integrated powder-to-elevated-temperature-property hardware pipeline.

**5. China's critical-mineral export controls and expanded U.S. critical-minerals list strengthen the "strategic-element-lean" framing** but the searched record does not confirm 2026-specific controls on Co, Re, Hf, Ta, Nb, or W specifically (tsouris2026securingcriticalminerals pages 22-26, tsouris2026securingcriticalmineralsa pages 22-26, iii2026usgscriticalminerals pages 1-2). The PI should supplement with USGS Mineral Commodity Summaries data for element-specific import reliance.

---

## Suggested Wording Changes for the White Paper

The current claim—*"This cost-aware, partial-evaluation formulation applied for the first time to a complex additive manufacturing pipeline for alloys is the core methodological novelty"*—requires tightening. Talbot et al. (2026) demonstrated a closed-loop active-learning AM alloy campaign, Mallia & Caputo (2026) explicitly proposed multi-fidelity BO with CALPHAD for metallurgical self-driving labs, and Kudva & Paulson (2026) extended BOFN to multi-objective networked systems. The PI's claim is still defensible if sharpened to emphasize the **specific combination** of elements that no prior work demonstrates simultaneously:

**Suggested rewording:** *"The core methodological novelty is the integration of cost-aware, multi-fidelity Bayesian optimization of function networks—including partial evaluations over a DAG of physically grounded surrogate models spanning CALPHAD, powder atomization, LPBF printing, microstructure, and elevated-temperature mechanical properties—with an in-house, end-to-end powder-to-property hardware pipeline. While recent work has demonstrated closed-loop active learning for AM alloy composition (Talbot et al. 2026) and proposed multi-fidelity BO for metallurgical self-driving labs (Mallia & Caputo 2026), no prior system jointly optimizes across the full powder-to-elevated-temperature-property DAG, uses cost-aware partial node evaluations to decide when cheap proxy experiments (single tracks, density cubes, hardness) suffice versus when expensive nodes (full elevated-temperature tensile tests) are needed, and controls the entire physical pipeline from alloy design through in-house atomization, LPBF, and characterization."*

This rewording acknowledges the competitive landscape, identifies the precise locus of novelty, and avoids overclaiming.


References

1. (silva2026towardtrustworthyautonomous pages 24-25): Toward Trustworthy Autonomous Science: A Two-Year Community Roadmap This article has 0 citations.

2. (xu2026researchunderuncertainty pages 15-19): K Xu. Research under uncertainty: exploring the impacts of federal grant disruptions on current research and future scientists. Unknown journal, 2026.

3. (mallia2026aiguidedselfdrivinglaboratories pages 12-17): Bernard Mallia and Rossana Caputo. Ai-guided self-driving laboratories for advanced materials discovery. Computing&amp;AI Connect, Aug 2026. URL: https://doi.org/10.69709/caic.2026.133382, doi:10.69709/caic.2026.133382. This article has 0 citations.

4. (mallia2026aiguidedselfdrivinglaboratories pages 6-12): Bernard Mallia and Rossana Caputo. Ai-guided self-driving laboratories for advanced materials discovery. Computing&amp;AI Connect, Aug 2026. URL: https://doi.org/10.69709/caic.2026.133382, doi:10.69709/caic.2026.133382. This article has 0 citations.

5. (campo2026fromdiscoveryto pages 3-4): Eva M. Campo, Robert J. Hanisch, and Joshua C. Agar. From discovery to deployment: a national ai strategy for materials readiness across energy and defense. MRS Bulletin, Sep 2026. URL: https://doi.org/10.1557/s43577-026-01181-0, doi:10.1557/s43577-026-01181-0. This article has 0 citations and is from a domain leading peer-reviewed journal.

6. (talbot2026activelearningfor pages 13-16): Ajay Talbot, Soumya S. Dash, Jialu Li, Changjun Cheng, Madhi Ramesh, Xiao Shang, Jiahui Zhang, Cristian Cojocaru, Jason Hattrick-Simpers, and Yu Zou. Active learning for the accelerated discovery of complex concentrated nicocr alloys in additive manufacturing. npj Advanced Manufacturing, Jun 2026. URL: https://doi.org/10.1038/s44334-026-00098-5, doi:10.1038/s44334-026-00098-5. This article has 2 citations.

7. (talbot2026activelearningfor pages 4-7): Ajay Talbot, Soumya S. Dash, Jialu Li, Changjun Cheng, Madhi Ramesh, Xiao Shang, Jiahui Zhang, Cristian Cojocaru, Jason Hattrick-Simpers, and Yu Zou. Active learning for the accelerated discovery of complex concentrated nicocr alloys in additive manufacturing. npj Advanced Manufacturing, Jun 2026. URL: https://doi.org/10.1038/s44334-026-00098-5, doi:10.1038/s44334-026-00098-5. This article has 2 citations.

8. (talbot2026activelearningfor pages 34-39): Ajay Talbot, Soumya S. Dash, Jialu Li, Changjun Cheng, Madhi Ramesh, Xiao Shang, Jiahui Zhang, Cristian Cojocaru, Jason Hattrick-Simpers, and Yu Zou. Active learning for the accelerated discovery of complex concentrated nicocr alloys in additive manufacturing. npj Advanced Manufacturing, Jun 2026. URL: https://doi.org/10.1038/s44334-026-00098-5, doi:10.1038/s44334-026-00098-5. This article has 2 citations.

9. (cao2026ahighperformance pages 15-16): Weisheng Cao, Kamalnath Kadirvel, Quanliang Liu, Shuanglin Chen, Chuan Zhang, Songmao Liang, Jun Zhu, Hyunseok Oh, and Fan Zhang. A high performance calphad data engine for scalable icme and ai-assisted materials design. Scientific Reports, Sep 2026. URL: https://doi.org/10.1038/s41598-026-73329-6, doi:10.1038/s41598-026-73329-6. This article has 0 citations and is from a peer-reviewed journal.

10. (cao2026ahighperformance pages 1-3): Weisheng Cao, Kamalnath Kadirvel, Quanliang Liu, Shuanglin Chen, Chuan Zhang, Songmao Liang, Jun Zhu, Hyunseok Oh, and Fan Zhang. A high performance calphad data engine for scalable icme and ai-assisted materials design. Scientific Reports, Sep 2026. URL: https://doi.org/10.1038/s41598-026-73329-6, doi:10.1038/s41598-026-73329-6. This article has 0 citations and is from a peer-reviewed journal.

11. (cao2026ahighperformance pages 3-5): Weisheng Cao, Kamalnath Kadirvel, Quanliang Liu, Shuanglin Chen, Chuan Zhang, Songmao Liang, Jun Zhu, Hyunseok Oh, and Fan Zhang. A high performance calphad data engine for scalable icme and ai-assisted materials design. Scientific Reports, Sep 2026. URL: https://doi.org/10.1038/s41598-026-73329-6, doi:10.1038/s41598-026-73329-6. This article has 0 citations and is from a peer-reviewed journal.

12. (mallia2026aiguidedselfdrivinglaboratories pages 22-27): Bernard Mallia and Rossana Caputo. Ai-guided self-driving laboratories for advanced materials discovery. Computing&amp;AI Connect, Aug 2026. URL: https://doi.org/10.69709/caic.2026.133382, doi:10.69709/caic.2026.133382. This article has 0 citations.

13. (kudva2026multi‐objectivebayesianoptimization pages 19-22): Akshay Kudva, Wei‐Ting Tang, and Joel A. Paulson. Multi‐objective bayesian optimization for networked black‐box systems: a path to greener profits and smarter designs. Optimization of Sustainable Process Systems, pages 63-89, Apr 2026. URL: https://doi.org/10.1002/9781394205646.ch3, doi:10.1002/9781394205646.ch3. This article has 7 citations.

14. (zhao2026alloydesignparadigms pages 12-13): Li Zhao, Tianshu Liu, Hyoung Seop Kim, Tarasankar Debroy, Tomasz Kurzynowski, Konrad Gruber, Xiaowei Hu, and Chaolin Tan. Alloy design paradigms in additive manufacturing: a new era of material innovation. International Journal of Extreme Manufacturing, 8:033003, Mar 2026. URL: https://doi.org/10.1088/2631-7990/ae45de, doi:10.1088/2631-7990/ae45de. This article has 10 citations.

15. (zhao2026alloydesignparadigms pages 10-12): Li Zhao, Tianshu Liu, Hyoung Seop Kim, Tarasankar Debroy, Tomasz Kurzynowski, Konrad Gruber, Xiaowei Hu, and Chaolin Tan. Alloy design paradigms in additive manufacturing: a new era of material innovation. International Journal of Extreme Manufacturing, 8:033003, Mar 2026. URL: https://doi.org/10.1088/2631-7990/ae45de, doi:10.1088/2631-7990/ae45de. This article has 10 citations.

16. (tsouris2026securingcriticalmineralsa pages 22-26): E Tsouris. Securing critical minerals' supply chains: a comparative approach of the us and eu strategies. Unknown journal, 2026.

17. (tsouris2026securingcriticalminerals pages 22-26): E Tsouris. Securing critical minerals' supply chains: a comparative approach of the us and eu strategies. Unknown journal, 2026.

18. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

19. (hammond2026earlycareerresearcher pages 1-2): Crystal Hammond, John Patrick Flores, Siara Rouzer, Kassandra Fernandez, Amy Ralston, and Adriana Bankston. Early career researcher responses to 2025 united states federal science funding disruptions: a rapid-response pilot survey. Frontiers in Sociology, Jul 2026. URL: https://doi.org/10.3389/fsoc.2026.1790840, doi:10.3389/fsoc.2026.1790840. This article has 0 citations.

20. (hammond2026earlycareerresearcher pages 6-10): Crystal Hammond, John Patrick Flores, Siara Rouzer, Kassandra Fernandez, Amy Ralston, and Adriana Bankston. Early career researcher responses to 2025 united states federal science funding disruptions: a rapid-response pilot survey. Frontiers in Sociology, Jul 2026. URL: https://doi.org/10.3389/fsoc.2026.1790840, doi:10.3389/fsoc.2026.1790840. This article has 0 citations.

21. (cao2026ahighperformance pages 16-18): Weisheng Cao, Kamalnath Kadirvel, Quanliang Liu, Shuanglin Chen, Chuan Zhang, Songmao Liang, Jun Zhu, Hyunseok Oh, and Fan Zhang. A high performance calphad data engine for scalable icme and ai-assisted materials design. Scientific Reports, Sep 2026. URL: https://doi.org/10.1038/s41598-026-73329-6, doi:10.1038/s41598-026-73329-6. This article has 0 citations and is from a peer-reviewed journal.
