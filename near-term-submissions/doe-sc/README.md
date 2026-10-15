# DOE Office of Science FY 2027 open call: BES pre-application (white paper)

Draft prepared 2026-10-10. Nothing has been submitted or emailed.

| File | What it is |
|---|---|
| `white-paper.tex`, `white-paper.pdf` | Pre-application: title page + 3 pages (figures and references inside the 3 pages), Times New Roman 11 pt, 1 in margins, letter paper |
| `email.md` | PAMS submission steps, plus an optional follow-up email to the program manager (149-word body) |
| `preview/page-*.png` | Page renders at 110 dpi |

Build: `xelatex white-paper.tex` twice. Lint: `cringe-filter lint -c proposal white-paper.tex` gives 0 findings, 0 errors; the email body gives 0 findings, 0 errors with `-c email`. The PDF has 4 pages: title page plus 3 body pages.

## Program and sources

- NOFO: DE-FOA-0003665, "FY 2027 Continuation of Solicitation for the Office of Science Financial Assistance Program". Posted September 30, 2026; open until September 30, 2027, 11:59 PM ET. Page: <https://science.osti.gov/grants/FOAs/FOAs/2027/DE-FOA-0003665>. Part 1: <https://science.osti.gov/-/media/grants/pdf/foas/2027/DE-FOA-0003665-Part-1.pdf> (130 pages, footer "Version 4.1"). Part 2: <https://science.osti.gov/-/media/grants/pdf/foas/2027/DE-FOA-0003665-Part-2.pdf> (68 pages). Page numbers below are the printed "Page X of N" numbers.
- Target topic: Basic Energy Sciences (BES), Materials Sciences and Engineering Division, (c) Synthesis and Processing Science, Part 1 pp. 24-25. Subprogram contact: Shawn Chen, shawn.chen@doe.gov (Part 1 p. 25). The program page <https://science.osti.gov/bes/mse/Research-Areas/Synthesis-and-Processing-Science> says "please contact Dr. Shawn Chen".

## What the NOFO says (verified, with pages)

**White paper or pre-application?** The same thing. "A pre-application (also called white paper) is recommended but optional for many topics" (Part 1, Section IV.A.2, p. 105). BES: "Although not required, we strongly encourage white papers or pre-applications" (Part 1 p. 21).

**Target date.** Synthesis and Processing Science: "We strongly encourage white papers or pre-applications, which should be submitted by November 30, 2026. Applications submitted by February 1, 2027, will be considered for funding in FY 2027. Applications submitted after February 1, 2027, are not guaranteed consideration for funding this fiscal year" (Part 1 p. 25). BES target dates "are not hard deadlines and applications are accepted throughout the fiscal year" (Part 1 pp. 21-22).

**How to submit.** Through DOE SC PAMS only: "must be submitted electronically through the DOE SC PAMS website. You cannot draft or edit a pre-application in PAMS. Do not submit a pre-application through FedConnect or Grants.gov" (Part 1 p. 107). "You must select a program manager when you submit your pre-application using the DOE SC PAMS website" (Part 1 p. 106). Click-by-click steps are in Part 2, Section 6, pp. 17-18, copied into `email.md`. Single file, .pdf/.docx/.doc, file name at most 50 characters (Part 2 p. 17). The PI may submit; so may anyone at BYU with the PAMS "Submit to DOE" privilege (Part 1 p. 107). Email submission is asked for only in Experimental Condensed Matter Physics (Part 1 p. 27), not in Synthesis and Processing Science.

**Format (Part 1 p. 106).**
- Title page first, not counted. At its top: title; PI name and job title; lead institution; PI phone and email; NOFO number; list of all senior/key personnel at the applicant and any team institutions. The draft follows this order.
- Then "a clear and concise description of the objectives and technical approach". At most three pages, letter size, 1 in margins, body text not smaller than 11 point. "Figures and references, if included, must fit within the three-page limit."
- Also required: a list of senior/key personnel and a list of individuals who should not serve as merit reviewers, uploaded as an "Additional Attachment" in PAMS; it does not count toward the page limit (Part 1 p. 106). Rules for that list: Part 2, Section 10, pp. 25-26 (advisors, advisees, and co-authors, collaborators, co-editors, co-investigators, and close associates of the past 48 months; never list BYU people). **Not written yet** (needs Sterling's co-author list).
- Machine-readable, not a scan (Part 1 p. 106).

**What happens next.** BES gives no decision date for white papers. Part 1 p. 106: "Feedback from DOE to the principal investigator is optional, but you are encouraged to use your submitted pre-application or white paper to initiate a discussion with the listed program manager." "The absence of an optional pre-application will not negatively affect an evaluation of a responsive application" (p. 106). The full application goes through Grants.gov (Part 1 p. 107), by February 1, 2027 for FY 2027 consideration (p. 25). BES project narratives are "typically ... 15-20 pages" (Part 1 p. 22). There is no formal encourage/discourage step for BES in this NOFO; that language appears only for specific ASCR panels (e.g., Part 1 p. 15).

**Career stage.** No early-career limit is stated for the BES topics. Eligibility is in Part 1 Section II (p. 8 onward); not read line by line in this pass.

**Scope limits that shape the draft (Part 1 p. 25).**
- "Applications must be hypothesis-driven or directly address specific scientific challenges. Applications will be evaluated based on their ability to formulate and address 'why' questions related to processes or mechanisms that enable the synthesis of materials."
- "Applications solely focused on materials synthesis, material characterization, software development, automation, AI-implementation, device fabrication, process engineering, or any iterative optimization based on known processing or synthesis principles fall outside the subprogram's scope and will not be supported."
- Key phenomena: "diffusion, nucleation, and phase transitions" and "time-temperature-transformation" relationships, and "the influence of ... external stimuli (electromagnetic fields) ... on growth" (pp. 24-25).
- FY 2027 increased emphasis: "(1) using localized external fields to direct growth processes, (2) precisely controlling defects and disorder during film, single crystal, and bulk synthesis; and (3) developing low-energy alternatives to traditional, energy-intensive physical synthesis processes" (p. 25). The NOFO does not define "localized external fields"; its only example is electromagnetic fields, and the program page speaks of "external and substrate derived fields". The draft therefore does **not** claim this emphasis. It states only that the laser is a moving, localized heat source whose thermal gradient and solidification speed direct grain growth, and the optional email asks the program manager whether that counts.
- Multi-PI or national laboratory co-PI ideas should be discussed with the contact first (p. 25). The draft is single-PI.

## Other routes in the same NOFO

- **BES Mechanical Behavior and Radiation Effects** (Part 1 pp. 30-31; John Vetrano, john.vetrano@doe.gov). White papers by November 30, 2026, but applications by **January 1, 2027**. It excludes work "primarily aimed at optimizing properties of materials for specific applications or focused on developing simple structure-property correlations" and "mechanics of materials (rather than materials science)". A fit only if the cracking question (H2) becomes the lead.
- **ASCR Applied Mathematics** (Part 1 pp. 14-15; contact David Rabson, david.rabson@doe.gov). ASCR "awards most of its funding for basic research using targeted solicitations or specific panels"; this NOFO is "generally used for" PIs changing institutions, conference support, and standards work; "However, in extraordinary circumstances, applications, generally preceded by submission of a pre-application, may result in an award. Early communication with the appropriate subprogram contact is recommended ... Program managers are unable to advise if funding is available" (p. 14). Applied Mathematics lists "optimization techniques" and "foundational research in scientific machine learning and AI" (p. 14). Its one scheduled panel is on sparse linear algebra (pre-applications by February 19, 2027; p. 15), which does not fit. The multi-objective and asynchronous method work would go here only after a call with Rabson.

## Relation to the Early Career Research Program (ECRP)

<https://science.osti.gov/early-career> (read 2026-10-10) still shows the **FY 2026** cycle: mandatory pre-applications due March 24, 2026, 5:00 p.m. ET, applications June 2, 2026, and only encouraged pre-applicants may apply. No FY 2027 ECRP notice was found. The page states eligibility as an untenured, tenure-track assistant or associate professor within 10 years of the doctorate (Sterling: Ph.D. August 2023; check against the FY 2027 notice when it appears). If the FY 2027 cycle follows FY 2026, its pre-application would come around March 2027 (an inference, not a published date). This open-call white paper does not block an ECRP pre-application, but the two would need to be distinct or coordinated; ask Shawn Chen whether BES prefers one route for a new investigator. `early-career-award-adaptation.md` Section 3 has the earlier ECRP notes.

## Facts used in the white paper and where they come from

- Capabilities (atomizer with induction-melting module only, so aluminum only; four compositions per week; LPBF builds on a purchase order from a University of Utah user facility at $800 per build; BYU Microscopy Center SEM/EDS/EBSD; BYU HPC; CALPHAD workflow; powder-to-part demo on a baseline aluminum alloy with SEM, EDS, tensile data): taken from the submitted AFOSR A.2.c white paper (`afosr-yip-white-paper/afosr-yip-white-paper-a2c.tex`) and the task brief.
- "Dozens of tracks" per plate: from the A.2.c paper ("A build plate holds dozens of tracks and cubes").
- Simulation result (3.8 times less spending, 90% CI 2.0 to 5.7, hand-built and noise-free, CALPHAD crack screen ignoring zirconium): `benchmarks/bofn-prelim/README.md`.
- References, checked against Crossref on 2026-10-10: Martin et al., Nature 549, 365-369 (2017); Kou, Acta Mater. 88, 366-374 (2015); DebRoy et al., Prog. Mater. Sci. 92, 112-224 (2018); Hunt, Mater. Sci. Eng. 65, 75-83 (1984). Astudillo and Frazier (NeurIPS 2021) and Buathong et al. (ICML 2024) are copied from the A.2.c paper. The claims about Martin et al. (columnar grains and periodic cracks; zirconium-based nanoparticles on the powder; crack-free, equiaxed, fine-grained result) follow the paper's abstract.
- H1 to H3 are new hypotheses written for this draft. Their physics is standard (primary Al3Zr and Al3(Sc,Zr) nucleants, Hunt's criterion, Kou's index, solute trapping), but no source is cited for the specific predictions. Sterling should check them.

## Open questions for Sterling

1. Is Synthesis and Processing Science the right home, or should the cracking question go to Mechanical Behavior and Radiation Effects (applications due January 1, 2027)?
2. Duration and team: the draft says three years, one Ph.D. student, two part-time undergraduates (copied from the A.2.c paper). Is that right for DOE? No budget appears in the white paper; none is required.
3. Alloy system: the draft names an Al-Zn-Mg-Cu base near 7075 with Zr and Sc. Is scandium affordable at the planned powder volumes, and which base alloy was used in the powder-to-part demo?
4. Reviewer exclusion list (Part 2 pp. 25-26): needs co-authors and collaborators from the past 48 months plus Ph.D. and postdoctoral advisors and any advisees. Who should be on it?
5. Is the PI registered in PAMS? Part 2 asks for registration at least a week before the target date.
6. Should the email to Shawn Chen go before PAMS submission (to test fit) or after? The NOFO supports both (Part 1 pp. 21 and 106).
7. Do you want the ECRP route instead of, or in addition to, this open-call application?
8. The NOFO says the pre-application must be a single file (Part 2 p. 17) and also that the reviewer list goes in an "Additional Attachment" (Part 1 p. 106). If PAMS shows only one upload slot, should the list be appended after the three pages? The PAMS help desk (855-818-1846) can confirm.
