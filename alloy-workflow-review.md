# Alloy Workflow Review

Review of the alloy synthesis, processing, characterization, and performance work tracked in [vertical-cloud-lab/byu-vcl](https://github.com/vertical-cloud-lab/byu-vcl). This document is intended as a reference for planning and prioritization in the [digital-alloy-private](https://github.com/vertical-cloud-lab/digital-alloy-private) repository.

## Overview

The BYU Vertical Cloud Lab (VCL) is building an integrated alloy development pipeline:

```
Raw Materials → Powder Dispensing → Ultrasonic Atomization → LPBF Printing → Characterization → Performance Testing
```

The target alloy system is **aluminum-based** (Al–Si with AlSi10Mg), with the initial goal of producing custom alloy powders via ultrasonic atomization, printing specimens via laser powder bed fusion (LPBF), and characterizing them through microscopy (SEM/EDS/EBSD) and mechanical testing (tensile, hardness, PIP indentation plastometry).

## 1. Synthesis — Powder Production

### Raw materials ([#8](https://github.com/vertical-cloud-lab/byu-vcl/issues/8) ✅ closed)

Stock materials have been procured:

- **1100 Al wire** — from McMaster-Carr / OnlineMetals
- **Si powder** — ~45 µm from McMaster-Carr
- **AlSi10Mg powder** — 15–45 µm from MSE Supplies

SDS documents are stored in the byu-vcl repo.

### Test mixture preparation ([#16](https://github.com/vertical-cloud-lab/byu-vcl/issues/16))

Four test mixtures have been created and are stored in the lab (far left cupboard). Target composition was approximately `80% Al (wire)`, `12% Si (powder)`, `8% AlSi10Mg (powder)`, with some variation across mixtures.

Measured masses (from [issue #16 comments](https://github.com/vertical-cloud-lab/byu-vcl/issues/16#issuecomment-4012488827)):

| Sample | Al wire (g) | Si powder (g) | AlSi10Mg (g) | Total (g) |
|---|---|---|---|---|
| SGB initial | 4.9221 | 2.6189 | 7.632 | 15.173 |
| Powder 1 | 4.7244 | 2.607 | 6.0845 | 13.416 |
| Powder 2 | 3.5494 | 1.8541 | 7.0205 | 12.424 |
| Powder 3 | 4.5365 | 1.8044 | 7.0033 | 13.344 |
| 100 g mixture | 38.164 | 20.3042 | 41.5472 | 100.015 |

A compiled SOP video is available at <https://youtu.be/WTrs3JU2HF0> (see also [#28](https://github.com/vertical-cloud-lab/byu-vcl/issues/28)).

### Ultrasonic atomization

As of 2026-02-18, samples had been shipped to [Amazemet](https://platform.edisonscientific.com/) (Poland) for ultrasonic atomization proof-of-concept testing. The package was shipped via BYU Post Office on 2026-02-18, with an estimated arrival of 2026-02-26. Materials were confirmed non-hazardous per IATA by MSE Supplies.

This is a key milestone — the returned atomized powders will be among the first custom alloy powders produced by the lab's pipeline and will feed directly into characterization ([#49](https://github.com/vertical-cloud-lab/byu-vcl/issues/49)).

### Silicon powder flow issues ([#58](https://github.com/vertical-cloud-lab/byu-vcl/issues/58))

The McMaster Si powder (~45 µm) was gumming up the autotrickler and not flowing well. Options being explored include sourcing coarser silicon and processing the existing powder to improve flowability.

### Autotrickler status ([#10](https://github.com/vertical-cloud-lab/byu-vcl/issues/10) ✅ closed, [#63](https://github.com/vertical-cloud-lab/byu-vcl/issues/63))

The AutoTrickler v4 is set up and operational. It had jammed due to silicon powder infiltrating the auger tube gap, causing scratches and binding. The tube was disassembled, cleaned, and reassembled — now functional. Lubrication may be needed; contamination from lubricant is a consideration.

### OpenTrickler ([#14](https://github.com/vertical-cloud-lab/byu-vcl/issues/14))

An open-source alternative powder trickler ([eamars/OpenTrickler](https://github.com/eamars/OpenTrickler)) is being considered. Bill of materials and sourcing are in progress.

## 2. Processing — Laser Powder Bed Fusion (LPBF)

### Existing LPBF system ([#45](https://github.com/vertical-cloud-lab/byu-vcl/issues/45))

The Crabtree building houses a **Concept Laser M2 Cusing** (GE Additive) LPBF printer. Key findings:

- The machine has been **down for nearly 2 years**
- Dr. Nathan Crane's students were the last operators
- It has a history of frequent problems
- **New cost:** ~$400K (comparable current model: [M2 Series 5](https://www.colibriumadditive.com/printers/l-pbf-printers/m2-series-5))
- **Used cost:** ~$150K ([CAE Online](https://caeonline.com/buy/screen-printers/concept-laser-m2/293754281), [Resale.biz](https://www.resale.biz/concept-laser/used-concept-laser/))

Plans include obtaining official quotes and potentially moving the existing machine to the VCL lab for better environmental control.

### LPBF acquisition ([#61](https://github.com/vertical-cloud-lab/byu-vcl/issues/61))

Given the existing printer's downtime, the lab is actively exploring acquisition of a used or refurbished LPBF printer ($44K–$210K estimated range). Quotes are being gathered.

### Printing strategy

The initial strategy (from [#45](https://github.com/vertical-cloud-lab/byu-vcl/issues/45)):

1. Begin with commercial stainless steel powders (already available from Kevin)
2. Print tensile specimens at different orientations (flat, perpendicular, angled)
3. Print repeat specimens to characterize variability
4. Track metadata (videos, humidity, powder exposure)
5. Target near-24/6 machine usage for preliminary data and publications
6. Eventually transition to custom powders from atomization

## 3. Characterization

### SEM, EDS, and EBSD ([#49](https://github.com/vertical-cloud-lab/byu-vcl/issues/49), [#48](https://github.com/vertical-cloud-lab/byu-vcl/issues/48))

The lab is building capabilities with BYU's [electron microscopy facilities](https://microscopy.byu.edu/):

- Training sessions are being arranged for multiple lab members ([#48](https://github.com/vertical-cloud-lab/byu-vcl/issues/48))
- Initial priority: characterize the starting materials from ultrasonic atomizer test samples
- Follow-up: characterize standard tensile specimens and returned atomized powders
- Data storage under consideration (Box, OneDrive, Zenodo, MongoDB + S3)

### Mechanical testing ([#46](https://github.com/vertical-cloud-lab/byu-vcl/issues/46))

Plans for mechanical testing include:

- Acquiring ASTM tensile testing standards for common alloys
- Procuring commercial or collaboration-based specimens (matching stainless steel powder composition, plus 3D-printed and cast variants)
- Hardness measurements in addition to tensile tests
- Other properties: electrical, thermal, mechanical
- Spatially correlated follow-up characterization (SEM, EDS, EBSD, optical)
- Smaller tensile specimens for "transfer learning" to predict scale-up potential
- Primary concern: cracking from low as-built ductility

## 4. Performance — PIP Testing ([#65](https://github.com/vertical-cloud-lab/byu-vcl/issues/65))

Profilometry-based Indentation Plastometry (PIP) testing via [Plastometrex](https://www.plastometrex.com) is being explored:

- Prep and send 3–5 characteristic samples as proof-of-concept
- High-temperature testing is of particular interest
- ASTM E3499-25 standard (2025) strengthens the case for PIP equipment in grant proposals
- Estimated system cost: ~$100K–$200K
- NASA has published results using PIP testing for revealing hidden property variations

## 5. Supporting Infrastructure

### Safety and environment

| Need | Issue | Status |
|---|---|---|
| Fumehood | [#29](https://github.com/vertical-cloud-lab/byu-vcl/issues/29) | Being sourced (possible from old welding room) |
| Gloveboxes | [#30](https://github.com/vertical-cloud-lab/byu-vcl/issues/30) | Open |
| Explosion-proof vacuum | [#24](https://github.com/vertical-cloud-lab/byu-vcl/issues/24) | Open |
| Class D fire extinguisher | [#19](https://github.com/vertical-cloud-lab/byu-vcl/issues/19) | Open |
| HEPA filtration | [#23](https://github.com/vertical-cloud-lab/byu-vcl/issues/23) | Open |
| Dehumidifiers | [#42](https://github.com/vertical-cloud-lab/byu-vcl/issues/42) | Open — target ~25% RH |
| N₂/Ar gas supply | [#41](https://github.com/vertical-cloud-lab/byu-vcl/issues/41) | Open — needed for gloveboxes and potentially the LPBF |
| Drench hose | [#18](https://github.com/vertical-cloud-lab/byu-vcl/issues/18) | Open |

### Powder handling SOPs ([#28](https://github.com/vertical-cloud-lab/byu-vcl/issues/28))

A standard operating procedure for powder dispensing has been compiled from video recordings. Key safety considerations include flammability and respiratory protection, especially for AlSi10Mg and fine metal powders.

### Equipment opportunities ([#52](https://github.com/vertical-cloud-lab/byu-vcl/issues/52))

An automotive industry auction was flagged as a potential source for aluminum casting equipment relevant to alloy development.

## 6. Equipment Funding

A comprehensive equipment funding sources document has been prepared in [byu-vcl PR #67](https://github.com/vertical-cloud-lab/byu-vcl/pull/67) (see also [#66](https://github.com/vertical-cloud-lab/byu-vcl/issues/66)).

### Target equipment

| Equipment | Est. Cost | Issue |
|---|---|---|
| LPBF metal 3D printer | $44K–$210K | [#61](https://github.com/vertical-cloud-lab/byu-vcl/issues/61) |
| Ultrasonic atomizer | ~$100K–$500K | [#16](https://github.com/vertical-cloud-lab/byu-vcl/issues/16) |
| PIP testing system | ~$100K–$200K | [#65](https://github.com/vertical-cloud-lab/byu-vcl/issues/65) |

### Recommended funding strategy

> **⚠️ EPSCoR eligibility correction:** PR #67 recommended DOE EPSCoR as the lead funding option based on Utah's EPSCoR eligibility. However, **Utah is NOT eligible for DOE, NSF, or NASA EPSCoR** — Utah has surpassed the EPSCoR funding threshold for these agencies ([utepscor.org](https://utepscor.org/), [DOE EPSCoR eligible states](https://science.osti.gov/bes/epscor)). Utah is only eligible for USDA EPSCoR. The strategy below is revised accordingly.

1. **FY27 cycle (~early 2027):** Submit **DoD DURIP** proposal for specific equipment (e.g., LPBF printer or atomizer) framed for defense-relevant alloy research. Sole PI eligible, no cost sharing, up to $3M.
2. **Fall 2026 (Oct–Nov):** Submit **NSF MRI** proposal for the full integrated pipeline (atomizer + LPBF + PIP). Requires multi-user framing and BYU internal limited-submission competition. Cost sharing waived through 2026.
3. **Jul 2026:** Submit **NSF CAREER** proposal (deadline Jul 22, 2026). $400K–$500K+ over 5 years; can include equipment budget with justification. Requires integrated research/education plan.
4. **Rolling:** Submit **NSF AM/MEP** or **NSF DMR TMRP** proposals for research funding that can include equipment. Standard single-PI research grants.
5. **When available:** Monitor **DOE AMMTO**, **America Makes**, and **NSF Future Manufacturing** calls for additive manufacturing and alloy research opportunities.

Key sole-PI-eligible programs for early career faculty: DoD DURIP, NSF MRI, NSF CAREER, NSF AM/MEP, NSF DMR TMRP.

### Additional early-career equipment / seed grant programs

Beyond the primary strategy above, the following DoD Young Investigator Programs (YIPs) can fund equipment as part of research budgets and are well-suited for defense-relevant alloy/AM work:

| Program | Award | Duration | Next Deadline (est.) | Notes |
|---|---|---|---|---|
| **[DARPA YFA](https://www.darpa.mil/)** | $500K base + $500K option | 2–3 yr | ~Oct 2026 (exec summary) | Early-career tenure-track; no prior DARPA funding; can include equipment |
| **[ONR YIP](https://www.onr.navy.mil/)** | Up to $750K | 3 yr | ~Aug 2026 | PhD on/after Jan 2018; naval-relevant materials/manufacturing |
| **[AFOSR YIP](https://www.afrl.af.mil/)** | $150K/yr ($450K total) | 3 yr | ~Jul–Sep 2026 | PhD on/after Apr 2018; advanced materials and manufacturing |
| **[ARO YIP](https://arl.devcom.army.mil/)** | $120K/yr ($360K total) | 3 yr | Rolling (check BAA) | Army-relevant materials science; equipment in budget OK |

All four require U.S. citizenship/permanent residency and tenure-track position. Contact program officers before submitting. Deadlines above are estimated based on FY2026 cycles; verify current BAAs on [Grants.gov](https://www.grants.gov/) or [SAM.gov](https://sam.gov/).

### Near-term non-equipment research grants (deadlines ~Mar–Jul 2026)

The following research-focused (non-equipment) programs have near-term deadlines and are relevant to digital alloy development and additive manufacturing:

| Program | Award | Deadline | Scope / Notes |
|---|---|---|---|
| **[America Makes PADAM 2.0](https://www.americamakes.us/project_calls/powder-alloy-development-for-additive-manufacturing-padam-2-0/)** | Up to $2M/award ($6M total) | Mar 25, 2026 | Powder alloy development for AM; refractory alloy systems, supply chain. AFRL-funded via America Makes |
| **[America Makes AIM-4AM](https://www.americamakes.us/)** | $2M (two phases) | Mar 25, 2026 | AI for material allowables in AM; process-structure-property relations. OSD ManTech-funded |
| **[NSF DMR TMRP](https://www.nsf.gov/funding/opportunities/dmr-tmrp-division-materials-research-topical-materials-research)** (Metals & Metallic Nanostructures) | Standard research grant | Rolling (avoid Apr 15–Jun 15) | Submit before Apr 15 or after Jun 15. 1 proposal/PI/fiscal year across all DMR TMRPs |
| **[NSF AM](https://www.nsf.gov/funding/opportunities/am-advanced-manufacturing)** (Advanced Manufacturing) | Standard research grant | Rolling (no fixed deadline) | Fundamental manufacturing research incl. LPBF and materials processing. Email PO a 1-page summary first |
| **[NSF MEP](https://www.nsf.gov/funding/opportunities/mep-materials-engineering-processing)** (Materials Engineering & Processing) | Standard research grant | Rolling (no fixed deadline) | Materials processing, structure-property relationships. Email mep@nsf.gov 4 weeks before submission |
| **[NSF EAGER](https://www.nsf.gov/funding/early-career-researchers)** | Up to $300K | Rolling (PO discussion required) | High-risk exploratory work; requires prior conversation with program officer |
| **[NSF CAREER](https://www.nsf.gov/funding/opportunities/career-faculty-early-career-development-program)** | $400K–$500K+ / 5 yr | Jul 22, 2026 | Already in strategy above. Integrated research + education plan required |

**Note:** BYU is classified R1, so [LEAPS-MPS](https://www.nsf.gov/funding/opportunities/leaps-mps) and [ERI](https://www.nsf.gov/funding/opportunities/eri-engineering-research-initiation) (both restricted to non-R1 institutions) are not eligible. NSF EAGER proposals require a Concept Outline emailed to the PO before submission ([PAPPG 24-1, Ch. II.F.3](https://www.nsf.gov/policies/pappg/24-1/ch-2-proposal-preparation#2F3)) — contact Dr. Jonathan Madison (jmadison@nsf.gov, DMR MMN), Dr. Alexis Lewis (mep@nsf.gov, CMMI MEP), or the AM program (AdvancedManufacturing@nsf.gov; best-fit PDs for VCL are **Linkan Bian** for AI/ML+AM and **Satish Bukkapatnam** for smart manufacturing/digital twins) to discuss feasibility. See the [NSF EAGER section in grant-targeting-analysis.md](grant-targeting-analysis.md#8-nsf-eager--opportunistic) for official requirements, related documents, contact guidance, and vertical cloud lab framing. Deadlines verified as of early March 2026; check program pages for updates.

#### America Makes competitiveness notes

America Makes project calls (PADAM 2.0, AIM-4AM) have no explicit PI rank restrictions — assistant professors can serve as PI if their institution authorizes it. However, there are practical barriers:

- **Membership required:** The lead organization must be an [America Makes member](https://www.americamakes.us/membership/member-benefits/) at submission time. Membership starts at $15K/yr (Silver). **BYU is not currently listed as a member** ([current members](https://www.americamakes.us/membership/current-members/)).
- **Scale and competition:** PADAM 2.0 awards are up to $2M each with only 4 anticipated awards from $6M total. These typically go to established teams with industry partnerships and prior DoD AM track records.
- **Scope fit:** PADAM 2.0 focuses on refractory alloys (Mo, Nb, Ta, W systems) for high-temperature DoD applications — not directly aligned with the digital alloy composition space unless reframed for refractory systems.
- **Recommendation:** For an early-career sole PI, the NSF rolling programs (DMR TMRP, AM, MEP) and DARPA DSO BAA (see below) may offer more competitive entry points than America Makes calls, which favor larger collaborative teams.

### HTMDEC-adjacent programs and DARPA DSO BAA

The [High-Throughput Materials Discovery for Extreme Conditions (HTMDEC)](https://arl.devcom.army.mil/htmdec/) program, run by ARL with Texas A&M's [BIRDSHOT Center](https://birdshot.tamu.edu/), remains active through ~2027. No direct "HTMDEC 2.0" successor has been announced, but several related opportunities exist:

| Program | Award | Deadline | Scope / Notes |
|---|---|---|---|
| **[DARPA DSO Office-Wide BAA](https://www.darpa.mil/work-with-us/opportunities)** (HR001125S0013) | Varies | Rolling through Jun 2, 2026 | "Materials, Manufacturing, and Structures" is an explicit topic area. Covers novel alloy design, accelerated discovery platforms, advanced processing. Submit an executive summary first to gauge DARPA interest. Open to all proposers |
| **[ARL Open Campus](https://arl.devcom.army.mil/)** | Collaborative | Ongoing | Facility access, internships, post-docs for academic partners in materials research. Contact ARL technical leads directly |
| **[ARL Cooperative Agreements](https://arl.devcom.army.mil/)** (e.g., LHEAD) | Multi-million, multi-year | By invitation / BAA | Existing programs (Lehigh/OSU LHEAD, $25M through 2027) cover high-entropy alloys, superalloy discovery, additive processing. Watch for new BAAs |

The **DARPA DSO BAA** is the most accessible near-term option — it's a rolling open call that explicitly seeks revolutionary materials discovery ideas, and there's no membership requirement. Early-career PIs can submit executive summaries to test the waters before committing to a full proposal. Contact: HR001125S0013@darpa.mil.

#### DARPA DSO BAA — detailed submission guidance

The DSO Office-Wide BAA (HR001125S0013) is particularly well-suited for the VCL digital alloy program. Here's a detailed breakdown:

**Why it fits:**
- The **"Materials, Manufacturing, and Structures"** thrust area explicitly covers novel alloy design, accelerated discovery platforms, and advanced processing — directly aligned with AI-driven digital alloy development and LPBF additive manufacturing
- DARPA values **revolutionary leap-ahead capabilities**, not incremental improvements. The VCL's approach — combining AI/ML-accelerated alloy screening, autonomous powder production (ultrasonic atomization with AI-driven rePOWDER), and rapid LPBF validation — represents a paradigm shift from traditional trial-and-error alloy development
- Related active DARPA programs include **METALS** (Multi-objective Engineering and Testing of ALloy Structures, PM: Andrew Detor) focusing on property-on-demand alloy design, and **SURGE** (Structures Uniquely Resolved to Guarantee Performance) on real-time defect inspection for 3D-printed metals

**Submission process (3-stage, low initial commitment):**

| Stage | What | Format | Timeline |
|---|---|---|---|
| 1. **Executive Summary** | 1-page concept pitch using [official template](https://simpler.grants.gov/opportunity/15d9d591-bf91-4bdd-a065-75055dd53903) (Attachment A) | Email to HR001125S0013@darpa.mil | Rolling through Jun 2, 2026, 4:00 PM ET |
| 2. **Abstract** (optional) | More detailed concept, ~2–4 pages (Attachment C template) | Same email submission | After positive exec summary feedback |
| 3. **Full Proposal** | Complete technical/management volume + cost volume (Attachments E/F) | Via grants.gov | After DARPA encouragement |

**Executive summary content (1 page):**
- Project title and proposer information
- Technical thrust area: "Materials, Manufacturing, and Structures"
- Problem statement: current alloy development cycles are too slow (years) for defense needs
- Proposed solution: AI-accelerated digital alloy discovery pipeline integrating computational screening → autonomous powder synthesis → rapid LPBF validation → automated characterization
- Why revolutionary (not evolutionary): closed-loop autonomous discovery compresses multi-year timelines to weeks; generalizable to any alloy system
- DoD/national security impact: rapid fielding of mission-optimized alloys for extreme environments

**Pitch framing for VCL capabilities:**
- **AI/ML alloy screening** — computational prediction of composition-property relationships, Bayesian optimization for alloy design space exploration
- **Autonomous powder production** — AI-driven ultrasonic atomization (Amazemet rePOWDER) enabling rapid iteration of custom alloy powders
- **Rapid LPBF validation** — digital manufacturing with automated parameter optimization, in-situ monitoring
- **High-throughput characterization** — automated SEM/EDS/EBSD, PIP indentation plastometry for rapid mechanical property mapping
- **Closed-loop integration** — AI orchestration connecting all stages into an autonomous discovery pipeline

**Key contacts and next steps:**
1. Review the [full BAA document](https://files.simpler.grants.gov/opportunities/359239/attachments/348001/HR001125S0013.pdf) and download the executive summary template (Attachment A)
2. Check [active DSO programs](https://www.darpa.mil/about/offices/dso) to ensure no duplication with METALS, SURGE, or other running efforts
3. Contact DSO PMs to discuss alignment — Andrew Detor (METALS PM) is the most relevant for alloy/AM topics
4. Draft and submit 1-page executive summary — low commitment, fast feedback cycle
5. If encouraged, develop abstract and then full proposal

**Advantages for early-career PI:**
- No membership requirements (unlike America Makes)
- No team size bias — DARPA regularly funds single-PI university efforts
- Executive summary is low-effort (1 page) with fast feedback — ideal for testing ideas
- The AI/automation angle is a strong differentiator that aligns with DARPA's interest in revolutionary approaches
- Vendor collaborations (Amazemet, Plastometrex, Citrine) can be included as unfunded collaborators or sub-awardees to strengthen the proposal

### Industry-sponsored projects and vendor collaborative research

Beyond government grants, industry-sponsored research agreements (ISRAs) and collaborative R&D partnerships with vendors offer a complementary funding path — often with shorter lead times, equipment/software loans, and no overhead negotiations. Several vendors already in the VCL workflow are active in academic partnerships:

#### Existing vendor relationships with collaboration potential

| Vendor | Relevance to VCL | Partnership Model | Potential Value |
|---|---|---|---|
| **[Amazemet](https://www.amazemet.com/)** | Ultrasonic atomization (samples currently shipped for PoC) | Equipment co-development, joint publications, atomization service (from €1K/50 g batches). AI-driven rePOWDER systems with autonomous process control. Active university partnerships with TUM, RWTH Aachen | Leverage existing PoC relationship → co-authored validation data, potential equipment loan/discount, joint proposals |
| **[Plastometrex](https://www.plastometrex.com/)** | PIP indentation plastometry (PoC planned) | University case studies (Cambridge, Limerick), ASTRO America defense partnership. AI/numerical modeling for rapid mechanical property extraction | Propose beta-testing / case study partnership for digital alloy characterization. Could provide PLX-Benchtop access or discounted testing |
| **[Citrine Informatics](https://citrine.io/)** | Materials informatics / AI-driven alloy design | External Research Department partners on grant-funded academic projects. Requires external funding but provides AI platform access and co-publication | Joint proposal on AI-accelerated alloy discovery (pair with NSF AM or DARPA DSO BAA). Citrine provides platform, BYU provides experimental validation |
| **[Elementum 3D](https://www.elementum3d.com/)** | Novel printable alloy powders (RAM technology for Al, Ni alloys) | Active America Makes and NASA partnerships. Collaborated with Colorado School of Mines on solidification modeling | Potential powder supply partnership for printing novel Al-alloy compositions. Joint qualification dataset generation |

#### LPBF machine vendor partnerships

If acquiring a new/used LPBF system, vendor partnerships can offset costs and provide ongoing support:

| Vendor | Program Type | Notes |
|---|---|---|
| **EOS** | Academic partnership / university pricing | Large installed base, established university programs globally. Often provides training, application support, and software access |
| **Nikon SLM Solutions** | Academic collaboration | Part of Leading Minds Consortium for AM adoption. University partnerships for process development |
| **Trumpf** | Research partnerships | Strong in process monitoring and quality control. Patent cross-licensing with other OEMs |
| **Renishaw** | University labs / process metrology | Particularly strong in in-process monitoring and metrology, relevant to data-driven AM research |

#### How to structure vendor collaborations

1. **In-kind equipment / software loans** — Vendors often loan equipment to universities in exchange for published case studies, conference presentations, and student training. Amazemet and Plastometrex are good candidates given the existing PoC relationships.
2. **Joint proposal teaming** — Vendors can be sub-awardees or unfunded collaborators on government proposals (NSF, DARPA, DoD). This strengthens proposals with industry relevance and provides vendors with R&D data. Citrine and Elementum 3D fit this model.
3. **Sponsored research agreements (SRAs)** — Direct industry funding (typically $50K–$200K/yr) for specific R&D tasks. More common with larger companies. The AI/automation angle (autonomous atomization, ML-driven alloy screening, automated characterization) is a strong selling point for attracting vendor interest.
4. **SBIR/STTR sub-awards** — Vendors pursuing Phase I/II SBIR topics sometimes need university partners for fundamental research. Monitor relevant [SBIR topics](https://www.sbir.gov/) in materials / AM.

#### Recommended near-term actions

- **Amazemet:** After PoC powder return, propose a formal collaboration — joint paper on ultrasonic atomization of custom Al-Si blends, potential equipment evaluation agreement for rePOWDER system
- **Plastometrex:** Request a beta-testing / case study partnership for PIP characterization of AM specimens, leveraging their interest in building AM case studies
- **Citrine Informatics:** Reach out to their External Research Department about joint proposals. Their platform + BYU experimental data is a natural fit for NSF AM or DARPA DSO submissions
- **LPBF vendor:** When pursuing printer acquisition, negotiate academic pricing + research partnership terms as part of the purchase

## 7. Pipeline Status Summary

| Stage | Status | Key Blockers |
|---|---|---|
| **Raw materials** | ✅ Procured | — |
| **Powder dispensing** | ✅ Operational (AutoTrickler v4) | Si flow issues; lubrication needed |
| **Test mixtures** | ✅ 4 samples + 100 g mixture prepared | — |
| **Ultrasonic atomization** | 🔄 Samples shipped to Amazemet | Awaiting returned powders |
| **LPBF printing** | ⏳ Existing machine down ~2 years | Needs repair or acquisition of new/used printer |
| **SEM/EDS/EBSD** | 🔄 Training in progress | Need facility access for lab members |
| **Tensile testing** | ⏳ Standards and specimens needed | Dependent on LPBF availability |
| **PIP testing** | ⏳ Proof-of-concept planned | Samples need to be prepped and sent |
| **Safety infrastructure** | 🔄 Partially in place | Fumehood, glovebox, vacuum, fire extinguisher needed |
| **Equipment funding** | 🔄 Funding sources identified | DOE EPSCoR ineligible (see note above); DURIP FY27, NSF MRI Fall 2026 are next targets |

## 8. Cross-References

All alloy-related issues in [vertical-cloud-lab/byu-vcl](https://github.com/vertical-cloud-lab/byu-vcl):

**Synthesis & Powder Production:**
[#8](https://github.com/vertical-cloud-lab/byu-vcl/issues/8),
[#10](https://github.com/vertical-cloud-lab/byu-vcl/issues/10),
[#14](https://github.com/vertical-cloud-lab/byu-vcl/issues/14),
[#16](https://github.com/vertical-cloud-lab/byu-vcl/issues/16),
[#28](https://github.com/vertical-cloud-lab/byu-vcl/issues/28),
[#58](https://github.com/vertical-cloud-lab/byu-vcl/issues/58),
[#63](https://github.com/vertical-cloud-lab/byu-vcl/issues/63)

**Processing (LPBF):**
[#45](https://github.com/vertical-cloud-lab/byu-vcl/issues/45),
[#61](https://github.com/vertical-cloud-lab/byu-vcl/issues/61)

**Characterization:**
[#46](https://github.com/vertical-cloud-lab/byu-vcl/issues/46),
[#48](https://github.com/vertical-cloud-lab/byu-vcl/issues/48),
[#49](https://github.com/vertical-cloud-lab/byu-vcl/issues/49)

**Performance:**
[#65](https://github.com/vertical-cloud-lab/byu-vcl/issues/65)

**Infrastructure & Safety:**
[#18](https://github.com/vertical-cloud-lab/byu-vcl/issues/18),
[#19](https://github.com/vertical-cloud-lab/byu-vcl/issues/19),
[#23](https://github.com/vertical-cloud-lab/byu-vcl/issues/23),
[#24](https://github.com/vertical-cloud-lab/byu-vcl/issues/24),
[#29](https://github.com/vertical-cloud-lab/byu-vcl/issues/29),
[#30](https://github.com/vertical-cloud-lab/byu-vcl/issues/30),
[#41](https://github.com/vertical-cloud-lab/byu-vcl/issues/41),
[#42](https://github.com/vertical-cloud-lab/byu-vcl/issues/42),
[#52](https://github.com/vertical-cloud-lab/byu-vcl/issues/52)

**Funding:**
[#66](https://github.com/vertical-cloud-lab/byu-vcl/issues/66),
[PR #67](https://github.com/vertical-cloud-lab/byu-vcl/pull/67)
