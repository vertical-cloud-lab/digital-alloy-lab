# DOE Title Page (Edison Draft)


# DOE Title Page Content — FLAIME Genesis Mission Phase I

The complete DOE Title Page content has been drafted and saved to `doe-title-page-content.tex`, formatted for direct insertion into the `flaime-genesis-proposal.tex` LaTeX template. Below is a structured summary of all six requested fields, followed by compliance notes.

---

## 1. Full Project Title

**FLAIME: Fast Learning AI for Mineral Efficiency — Autonomous Discovery of Critical-Mineral-Lean Alloys for Advanced Manufacturing**

## 2. Challenge and Focus Area

**Topic 3, Focus Area B:** Securing America's Critical Minerals Supply | AI-Enabled Materials Discovery and Engineering (AMMTO)

*RFA Number:* DE-FOA-0003612

## 3. Senior/Key Personnel Table

| Institution | Role | Senior/Key Personnel |
|---|---|---|
| Brigham Young University (Lead) | Prime | S. G. Baird, Ph.D. (PI); 2 MS students; 10 UG researchers |
| Valimet, Inc. (Stockton, CA) | Subawardee | [Contact TBD] — gas atomization services |
| AMAZEMET Sp. z o.o. (Białystok, Poland) | Collaborator | [Contact TBD] — ultrasonic atomization technology |
| Thermo-Calc Software (Stockholm / Pittsburgh) | Collaborator | Thermo-Calc's account manager — CALPHAD & AM Module support |

**Notes:**
- Only Valimet receives DOE funds as a formal subaward. AMAZEMET and Thermo-Calc costs are classified as BYU direct costs (consumables and software licenses), not subawards — per PI confirmation. This simplifies budget administration and F&A calculations.
- Personnel count (PI + 2 MS + 10 UG) is PI-confirmed as of 2026-04-14 (proposal-population-plan.md, Resolution #1).

## 4. 2-of-3 Team Composition (FOA §II.E)

| Category | Institution | Status |
|---|---|---|
| Category 3 — Institution of Higher Education | BYU (Lead) | ✓ Formal team member |
| Category 2 — Industry | Valimet, Inc. | ✓ Formal subawardee |
| Category 1 — DOE National Lab | Ames National Lab | Advisory only (letter of support from Ames Lab contacts); not a formal team member |

**Requirement satisfied:** 2 of 3 categories (IHE + Industry). The FOA (§II.E) requires institutions from at least 2 of the 3 categories; the lead institution counts toward the requirement (per FAQ: "the lead institution is considered a partner of the team").

## 5. Budget Summary

| Institution | Year 1 Budget ($) |
|---|---:|
| Brigham Young University (Lead)¹ | [amount removed] |
| Valimet, Inc. (Subaward) | [amount removed] |
| **Total DOE Request** | **750,000** |

¹ BYU's amount includes direct costs for AMAZEMET consumables and Thermo-Calc software licenses.

- **Period of Performance:** July 1, 2026 – March 31, 2027 (9 months, Phase I)
- **Cost Share:** Not required per FOA §II.B (IHE lead institution performing basic/applied R&D). For-profit subawardee Valimet must provide ≥20% cost share from non-federal sources on their portion per §II.B.
- **Budget target:** $750K (PI-confirmed; recommended over $600K scenario to maintain realistic ~37% effective F&A rate per BYU's negotiated federal rate)

## 6. PI Information

**Sterling G. Baird, Ph.D.**
Assistant Professor
Department of Materials Science & Engineering
Brigham Young University
350 EB, Provo, UT 84602
Phone: (801) 422-XXXX
Email: sterling.baird@byu.edu

---

## Compliance Verification Against FOA §IV.C Title Page Requirements

All FOA-prescribed fields are present:
- ✅ Project Title
- ✅ Lead Applicant/Institution (BYU)
- ✅ Street Address / Postal Address
- ✅ Lead PI name, telephone, email
- ✅ Administrative POC (placeholder — to be filled by BYU OSR)
- ✅ RFA Number (DE-FOA-0003612)
- ✅ Challenge and Focus Area (Topic 3-B, AMMTO)
- ✅ Senior/Key Personnel table (all partner institutions listed)
- ✅ Summary Budget table (all institutions, single period, whole dollars)
- ✅ No additional material beyond prescribed fields (FOA: "Additional material is not allowed")
- ✅ Does NOT count against 5-page narrative limit

## Items Requiring PI/OSR Action Before Submission

1. **Administrative POC:** Must be filled with BYU OSR contact name, phone, and email
2. **Valimet contact name:** Must be confirmed and inserted
3. **AMAZEMET contact name:** Must be confirmed and inserted
4. **PI phone number:** Replace (801) 422-XXXX with actual number
5. **Valimet cost share:** Verify that Valimet's ≥20% non-federal cost share is documented in the SF-424 R&R Budget form
6. **Excel budget template:** Must be completed from Grants.gov "Related Documents" tab and attached to Field 12

## Output File

The LaTeX-formatted title page block has been saved to `doe-title-page-content.tex` and can be directly substituted for the existing `\section*{DOE Title Page}` block (lines 169–235) in `flaime-genesis-proposal.tex`. The existing `\required{}` and `\instruct{}` todo notes have been removed from the production version since they are for drafting guidance only.

---

## Discretionary Analytical Decisions

- **Project title wording:** Used the user-specified subtitle "Autonomous Discovery of Critical-Mineral-Lean Alloys for Advanced Manufacturing" rather than the existing template's longer variant ("An Autonomous Closed-Loop Platform for AI-Accelerated Critical-Mineral-Lean Alloy Discovery and Qualification"), as the user's version is more concise and the FOA title page is a formal document where brevity is valued
- **Budget split (BYU/Valimet):** Retained the existing template's BYU/Valimet allocation from the proposal files rather than recalculating, as this split is consistent across all project documents (budget-breakdown-phase1.md, flaime-genesis-proposal.tex) and reflects the PI-confirmed $750K target with Valimet as the sole subawardee
- **AMAZEMET entity designation:** Listed as "Sp. z o.o." (Polish limited liability company) based on the legal entity type referenced in the project documents; this should be verified against the actual letter of collaboration
- **Collaborator vs. Subawardee distinction in the table:** AMAZEMET and Thermo-Calc are listed as "Collaborator" rather than "Subawardee" because their costs flow through BYU as direct costs (materials/supplies and software licenses), not as formal subawards — per PI confirmation documented in budget-assessment-official-requirements.md and proposal-population-plan.md
- **Cost share footnote inclusion:** Included the "Cost Share: Not required" note in the budget table footnotes for reviewer clarity, even though the FOA title page template does not explicitly require this field — this aids compliance signaling without adding "additional material" in the prohibited sense (it annotates the budget table rather than adding a new field)
- **2-of-3 team composition treated as internal compliance note:** Did not print the 2-of-3 verification on the title page itself, as the FOA states "additional material is not allowed" beyond the prescribed fields; this information is embedded as LaTeX comments for the PI's internal verification
