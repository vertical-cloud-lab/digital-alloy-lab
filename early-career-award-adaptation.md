# Adapting the FLAIME Genesis Mission Proposal for Early-Career Awards

*Companion analysis to [`grant-targeting-analysis.md`](grant-targeting-analysis.md).
Source proposal: PR [#58](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/58) — `genesis-mission-proposal/flaime-genesis-proposal.tex` (9-month, \$750K, DE-FOA-0003612 Topic 3B).*

This document maps the FLAIME proposal section-by-section onto two early-career
vehicles the PI is eligible for:

1. **AFOSR Young Investigator Program (YIP)** — Air Force Office of Scientific Research
2. **DOE Early Career Research Program (ECRP)** — DOE Office of Science

Both are single-PI, no-subaward, longer-horizon mechanisms. FLAIME as written
(team-based, 9 months, applied AMMTO framing) cannot be submitted to either
unchanged; the table below isolates what must change and what can carry over
verbatim.

> **Verify each cycle.** Eligibility windows, page limits, and topic lists
> change yearly. Numbers below reflect the most recent published calls as of
> 2026-05. Always cross-check the active BAA / FOA before drafting.
>
> **AFOSR rows updated 2026-10-06** against the FY27 YIP NOFO
> [FA955026S0003](https://simpler.grants.gov/opportunity/c342c01d-4f34-440f-8bb2-4bdd4d763df0)
> (posted 2026-09-08), its
> [Sep 24 Q&A](https://files.simpler.grants.gov/opportunities/c342c01d-4f34-440f-8bb2-4bdd4d763df0/attachments/9cf2fa75-6fdf-4713-a203-3f849f3001af/FA955026S0003_Qs_and_As.pdf),
> and the AFOSR open BAA
> [FA955026S0001, Amendment 0001](https://simpler.grants.gov/opportunity/de479d2e-aad1-466a-acc3-d5d11cf7918d)
> (2026-08-21). Two earlier claims in this document were wrong: Sayir's
> portfolio does not take structural-materials proposals (§2.1), and YIP
> does not allow collaborators of any kind, funded or unfunded (§2.3).

---

## 1. Program Comparison at a Glance

| Dimension | FLAIME (as submitted) | AFOSR YIP | DOE ECRP |
|---|---|---|---|
| Mechanism | DE-FOA-0003612 Genesis Mission Phase I | AFOSR BAA YIP solicitation | DE-FOA Early Career Research Program |
| Sponsor office | DOE EERE / AMMTO | DAF / AFRL / AFOSR | DOE SC (BES preferred; ASCR alt.) |
| Award size | \$750K total | ~\$450K / 3 yr (≈\$150K/yr) | \$875K / 5 yr (\$175K/yr academia) |
| Period | 9 months | 36 months | 60 months |
| PI model | PI + 3 funded industry partners + 8 LOS | **Single PI, one institution, no subawards, no collaborators funded or unfunded** (FY27 Q&A Q14); students and postdocs allowed (Q15) | **Single PI, one institution, no subawards** |
| Eligibility | Open | PhD on or after 2019-04-01 (FY27); full-time permanent, career-competitive, or tenure-track position (tenured is OK, Q16); US citizen, national, or permanent resident | Untenured tenure-track within 10 yr of PhD |
| Pre-app | None (full 5-page narrative) | **Mandatory white paper** via Qualtrics: ≤5 pp. plus cover page, CV, and references; Times New Roman or Garamond 12 pt; 1.5 spacing | **Mandatory 3-page pre-application** |
| Page limit (full) | 5 pages narrative | ~15 pages (varies by BAA) | ~20 pages (varies) |
| TRL window | TRL 2 → TRL 4 | TRL 1 → TRL 3 (6.1 basic) | TRL 1 → TRL 3 (basic science) |
| Cost share | None | None | None |
| Typical deadline | Apr 28, 2026 (closed) | FY27: NOFO 2026-09-08 → white paper 2026-10-09 → feedback by 2026-11-06 → invited full proposal 2026-12-04 | 2026 cycle: pre-app 2026-03-24, full 2026-06-02 (plan on ~Mar 2027 for the next pre-app) |

---

## 2. AFOSR YIP Adaptation

### 2.1 Target portfolio and PM

- **Primary fit:** BAA §A.3.a Aerospace Materials for Extreme Environments.
  **Dr. Ali Sayir, AFOSR/RESB**, `extreme.environment@us.af.mil`,
  (703) 696-7236. Use the portfolio mailbox the BAA lists, not a personal
  address.
  - Scope as written in the current BAA: discovery and characterization of
    materials, aiming *"to fundamentally shift the paradigm of materials science
    from serendipitous discovery to materials synthesis by design."* Subtopics
    are Materials Synthesis by Design, Novel Materials Functionalities, and
    Materials for Quantum Information Science.
  - **Exclusion:** *"proposals focused primarily on structural or organic
    materials, device engineering, systems integration, or exploring the
    physics of known condensed matter phenomena … are not a fit for this
    program."* The FY25 BAA had a similar line, so this document's earlier
    description of the portfolio as "high-temperature structural materials"
    was wrong from the start.
  - **Where the project fits:** the Materials Synthesis by Design subtopic asks
    how *"external stimuli—such as electric fields, lasers, or acoustic
    waves—can guide the formation of desired material structures,"* with UQ
    that gives *"a predictive confidence level for achieving any target
    microstructure."* LPBF is laser-driven synthesis, ultrasonic atomization is
    acoustic, and Gaussian-process BOFN quantifies uncertainty. Lead with
    synthesis → target microstructure with calibrated confidence, and treat
    mechanical properties as validation of the structure-to-function link.
- **No metallic-materials portfolio:** the current BAA has none and does not
  list Dr. Jaimie Tiley. §A.1.e Aerospace Composite Materials (also Sayir,
  `ACMaterials@us.af.mil`) says *"Metal-based materials, while not excluded,
  are not a priority."*
- **Methodology-first alternative:** §A.2.c Dynamic Data and Information
  Processing, **Dr. Erik Blasch, AFOSR/RESA**, `D2IP@us.af.mil`. It covers
  DDDAS, physics-enhanced ML, and UQ, and suits a pitch that leads with the
  BOFN method and uses the alloys as the test case.

**Action (FY27 cycle):** the white paper is **mandatory** and is due
**2026-10-09, 11:59 PM ET** through the
[Qualtrics portal](https://afosr.gov1.qualtrics.com/jfe/form/SV_eKuTqm9qezoDYep),
even if a PO has already given feedback (NOFO p. 21). The NOFO-format draft
is [`afosr-yip-white-paper/`](afosr-yip-white-paper/afosr-yip-white-paper.tex)
([compiled PDF](afosr-yip-white-paper/afosr-yip-white-paper.pdf)), and the
fit-check email to the portfolio mailbox is
[`fit-check-email.md`](afosr-yip-white-paper/fit-check-email.md). More than one
white paper is allowed (Q13) if each one says so, which leaves room for a
§A.2.c version if Sayir says no.

### 2.2 Scope reframe: critical minerals → extreme-environment alloys

FLAIME's "reduce critical-mineral burden in Al alloys" framing does not map to
AFOSR's mission. The closed-loop discovery platform does. Two viable pivots:

1. **Co/Re-lean Ni-superalloy variants for turbine hot sections** —
   keep the *closed-loop discovery* and *AI-guided composition exploration*
   narrative; swap the objective from "minimize mineral burden" to "maintain
   creep/oxidation resistance at reduced strategic-element content."
   Critical-mineral framing is *secondary* benefit (Air Force also cares about
   supply chain resilience for Co, Re, Hf), not the lead.
2. **Refractory complex-concentrated alloys (RCCAs) for hypersonic leading
   edges** — fully extreme-environment framing; reuse the BOFN/CALPHAD/AM
   pipeline but swap Al palette → Mo-Nb-Ta-W-Hf-Zr-Ti space. Higher novelty
   risk, larger CALPHAD-database gap (TCHEA vs. TCAl10), but better PM alignment.

Either pivot keeps the methodological novelty (multi-fidelity BOFN +
function-network DAG over the powder-to-part pipeline) intact while replacing
the application target. For the Sayir portfolio, either pivot has to be
pitched as synthesis science (how laser and acoustic processing set the
microstructure, with quantified confidence) because of the structural-materials
exclusion in §2.1.

**Hardware constraint on both pivots.** The rePOWDER induction module only
melts alloys up to about 1300 °C, so it covers the aluminum work but neither
Ni superalloys nor RCCAs. Both pivots need the plasma/arc module, which belongs
in a DURIP request (§2.3, Equipment row). Until then, refractory compositions
can be made by in situ alloying of blended elemental or master-alloy powders
during LPBF, which also makes melt-pool mixing part of the synthesis question.

### 2.3 Section-by-section adaptation

| FLAIME section | AFOSR YIP version |
|---|---|
| Abstract (1 p) | Rewrite around extreme-environment alloy challenge. Drop "FLAIME" branding or recast acronym (Air Force should not see DOE branding). Drop industry-partner roster from key personnel block. |
| Background & Introduction (1 p) | Lead with the synthesis question: how laser (and later acoustic) processing sets microstructure in Ni-superalloy and RCCA space, and how confidently it can be predicted. Keep the high-T / oxidation / creep gap as motivation. Citing AFRL alloy programs is fine; naming AFRL staff as collaborators is not (Q14). |
| Project Objectives (0.5 p) | Reduce from 3 partner-coupled objectives to 2-3 single-PI objectives focused on methodology validation. Keep BOFN/pKGFN, drop AMAZEMET-specific atomization milestones. |
| Proposed Research & Methods (1.5 p) | Keep CALPHAD + Bayesian Optimization architecture. Replace the "Valimet GA + AMAZEMET UA" subaward arm with in-house routes only: induction ultrasonic atomization (≤1300 °C alloys) plus in situ alloying of blended powders for refractory compositions, with the plasma module requested separately through DURIP. **No collaborators, funded or unfunded** (FY27 Q&A Q14), so the earlier "unfunded AFRL-Materials & Manufacturing Directorate collaboration" option is out. Government-owned facilities may be used if named in the proposal (Q17). |
| Milestones (1 p) | **Expand from 9 months → 36 months.** Year 1: CALPHAD+BOFN framework + single-track validation. Year 2: density + microstructure closed loop. Year 3: high-T mechanical testing + open-source release. Avoid quarter-level granularity at YIP scale; semester-level is appropriate. |
| Data Sources & Models (0.5 p) | Mostly carries over. Note shift to Thermo-Calc TCHEA / TCNI if pivot 1; TCHEA if pivot 2. |
| Decision Gate Metrics (0.5 p) | Replace "≥3% discovery yield, ≤16 compositions/week" with metrics aligned to **methodology** rather than throughput (e.g., posterior-uncertainty reduction per experiment, regret vs. random search baseline). |
| Facilities (App. 2) | BYU, plus LPBF builds bought from the University of Utah user facility at \$800 per build on a purchase order (fee-for-service, not a subaward; Sterling, PR #90, 2026-10-10). Drop Valimet/AMAZEMET facility paragraphs. The no-collaborators sentence (NOFO §B, p. 9, repeated as the Q&A answer to Q14) sits in the paragraph on co-PIs, so it covers people who share direction of the research, not services bought at a set rate. Q17 also allows named government-owned facilities. |
| Equipment (App. 3) | Mostly carries; emphasize what is already on hand. AFOSR YIP is not an equipment vehicle — push equipment requests to a future **DURIP** submission (see [grant-targeting-analysis §8 — DURIP](grant-targeting-analysis.md#8-dod-durip--after-establishing-dod-relationship-early-2027)). |
| DMSP (App. 4) | Reuse with minor swap (DoD STINFO + AFOSR data-rights language replaces DOE Genesis Mission digital-thread requirement). |
| Biosketches (separate) | PI-only. Drop industry-partner senior personnel. The white paper also needs a CV listing all publications and presentations (excluded from the page count). |
| Budget | Single-PI, ≤\$150K/yr (no single year over \$150K; proposals over the cap may be rejected without review). Personnel = PI summer + 1 PhD student + part-time UG; postdocs are also allowed (Q15). No subawards. No partner cost-share line. BYU F&A 51.5% MTDC applies. |

### 2.4 What FLAIME assets carry over directly

- BOFN/pKGFN code and the cost-aware multi-fidelity formulation (these are the
  methodological *meat* AFOSR will care about)
- pycalphad / TC-Python orchestration scripts
- Preliminary AlSi10Mg tensile data and SEM/EDS of atomized powders (frame as
  feasibility evidence for the new alloy system, not as the project itself)
- HPC CALPHAD scaling demonstration on BYU resources
- Bibliography sections on Bayesian optimization for alloys, autonomous SDLs,
  and CALPHAD-AM coupling

### 2.5 What must be cut or rewritten

- Three industry-partner subawards (Valimet, AMAZEMET, Thermo-Calc) → removed
  entirely. Q14 bars unfunded collaborators too, so no partner letters of
  collaboration. Buying software licenses, powder, or services from vendors is
  procurement and stays allowed.
- "Reduce critical-mineral demand" as primary motivation
- DOE AMMTO programmatic alignment language
- Genesis Mission digital-thread / FAIR-via-Genesis-platform commitments
- Phase II handoff narrative (YIP is standalone, not Phase-gated)

---

## 3. DOE Early Career Research Program (ECRP) Adaptation

### 3.1 Target office and core research area

DOE ECRP awards are administered by the six Office of Science program offices.
Routing decision matters more here than for AFOSR.

- **Primary route: BES → Materials Sciences and Engineering Division →
  Synthesis & Processing Science** — best alignment with FLAIME's
  atomization-to-LPBF processing science. Solicits work on understanding
  fundamental mechanisms in materials synthesis and processing.
- **Secondary route: BES → MSE → Mechanical Behavior of Materials** — if
  framing emphasizes deformation/failure mechanisms in AI-designed alloys.
- **Alternative: ASCR → AI/ML for Science** — if methodology (Bayesian
  optimization, function-network surrogates, active learning) is the lead and
  the alloy work is the demonstration vehicle. Higher novelty bar against
  applied-math/CS competition; lower applied-materials competition.
- **Not a fit: EERE-AMMTO** — does not run an early-career program. Genesis
  Mission and AMMTO FOAs remain the EERE vehicles.

**Action:** Identify the topic line in the next published ECRP FOA before
drafting; topics rotate annually within each office. Pre-app submission to the
right office is the gating step.

### 3.2 Scope reframe: applied manufacturing → basic processing science

ECRP is explicitly a **basic-research** program. FLAIME's strongest ECRP-eligible
content is the *science behind the engineering*: solidification dynamics in
ultrasonic atomization, defect-formation pathways during LPBF rapid
solidification, and ML-informed extrapolation of CALPHAD thermodynamic models
into sparsely-measured high-order phase space.

Concrete reframe — three candidate ECRP titles:

1. **"Active-learning discovery of metastable solidification pathways in
   additively manufactured multicomponent alloys"** (BES Synthesis & Processing)
2. **"Function-network Bayesian optimization for closed-loop processing-science
   investigation of rapidly solidified alloys"** (BES Mechanical Behavior, or
   ASCR cross-cut)
3. **"Multi-fidelity CALPHAD-experiment coupling for thermodynamic-model
   refinement in under-characterized phase regions"** (BES Synthesis & Processing)

All three preserve FLAIME's technical core while motivating it as *understanding*
rather than *deployment*.

### 3.3 Section-by-section adaptation

| FLAIME section | DOE ECRP version |
|---|---|
| Pre-application (3 p) | New artifact, must come first. Title, hypothesis-driven motivation, 3-5 specific aims, 1-paragraph approach, biosketch summary. ~70% of pre-apps are discouraged at this stage — invest in this. |
| Project Summary / Abstract | Rewrite with **hypothesis-driven** language (DOE SC convention) rather than capability/deliverable language (DOE EERE convention used in FLAIME). |
| Background & Introduction | Lead with the *open scientific question* (e.g., "how does cooling-rate distribution in ultrasonic atomization couple to metastable phase retention in multicomponent Al alloys?") rather than the supply-chain motivation. |
| Project Objectives | 3 specific aims, each hypothesis-driven, falsifiable, with quantitative success criteria. Avoid milestone language; ECRP reviewers expect scientific aims, not engineering milestones. |
| Proposed Research & Methods | **Expand significantly** — ECRP narratives are ~20 pages vs. FLAIME's 5. Add: mechanistic hypotheses; statistical analysis plan; risk/mitigation per aim; alternative approaches. The BOFN/pKGFN machinery can occupy a full subsection on its own. |
| Milestones | Recast as 5-year aim timeline with annual go/no-go decisions rather than 9-month sprint. Add **graduate-student training milestones** (DOE ECRP cares about workforce development even though there is no separate ed. plan like NSF CAREER). |
| Data Sources & Models | Carries over. Add explicit alignment with DOE SC data-management requirements (PAGES, FAIR). |
| Decision Gate Metrics | Replace process-throughput KPIs with **scientific decision criteria** (e.g., posterior-belief shift on phase-stability predictions, model-falsification thresholds). |
| Facilities | BYU + Spear LPBF + ORNL / Ames National Lab user-facility collaboration (CALPHAD validation, neutron diffraction). Cite the existing Ames LOS from PR #58 as the basis for a stronger DOE-lab tie. |
| Equipment | Same trim as YIP — ECRP is not an equipment vehicle. |
| DMSP | Reuse with DOE-SC Public Access Plan language replacing Genesis Mission digital-thread language. |
| Biosketches | PI-only. |
| Budget | \$175K/yr × 5 = \$875K. Personnel = PI + 1 PhD student (full 5 yr) + UG support + summer salary. Modest computing + characterization consumables. BYU F&A 51.5% MTDC. No subawards. |

### 3.4 What FLAIME assets carry over directly

- BOFN/pKGFN methodology and code (frame as a **scientific method** for
  closed-loop materials science, not as a manufacturing platform)
- CALPHAD + Scheil + AM Module simulation pipeline
- BYU HPC throughput demonstration
- Preliminary AlSi10Mg tensile data, SEM/EDS, atomized-powder characterization
- Ames National Lab LOS from PR #58 (strengthen to a substantive collaboration)
- Bibliography on Bayesian optimization for alloys, autonomous SDLs, CALPHAD-AM

### 3.5 What must be cut or rewritten

- Industry-partner subawards (same constraint as AFOSR)
- AMMTO programmatic and "critical minerals" framing → demoted to single
  paragraph on broader impact, not the lead motivation
- Genesis Mission digital-thread commitments
- 9-month milestone cadence → 5-year hypothesis-driven aim structure
- Engineering deliverable language → scientific-question language throughout

---

## 4. Cross-cutting Strategy

### 4.1 Sequencing recommendation

Per the timeline in [`grant-targeting-analysis.md`](grant-targeting-analysis.md):

1. **NSF CAREER (Jul 2026)** remains the top early-career target — broadest
   scope, longest period (5 yr), education plan compatible with VCL outreach.
2. **AFOSR YIP (FY27 cycle: white paper 2026-10-09, invited proposals
   2026-12-04)** is the natural Air Force vehicle and can run in parallel with
   CAREER if scope-differentiated (CAREER = AI methodology + alloy discovery
   generally; YIP = synthesis by design of laser-processed extreme-environment
   alloys).
3. **DOE ECRP** is the natural successor to a *not-funded* Genesis Mission
   outcome — same DOE sponsor lineage, recyclable preliminary results,
   different program office. The 2026 cycle took pre-apps in March, so plan on
   a ~March 2027 pre-app.

### 4.2 Scope deconfliction

NSF CAREER + AFOSR YIP + DOE ECRP overlap is allowed but reviewers (and program
officers) read each other's portfolios. A defensible deconfliction:

- **NSF CAREER:** AI methodology for closed-loop materials discovery + education plan
- **AFOSR YIP:** Synthesis by design: predicting, with quantified confidence, the microstructure that laser processing produces in extreme-environment aerospace alloys
- **DOE ECRP:** Basic-science questions in solidification/processing physics that the methodology enables

Each proposal must include a Current & Pending section disclosing the others
honestly; the *scope* must be genuinely distinct in aims and deliverables, not
just in framing.

### 4.3 Eligibility window

The PI's PhD date determines AFOSR YIP (~7-yr window) and DOE ECRP (10-yr
window) eligibility. Confirm the calendar-year cutoff against each FOA before
investing drafting effort. If the AFOSR window is closing first, prioritize that
cycle and defer DOE ECRP one year.

---

## 5. Open Questions for the PI

1. Which alloy-system pivot do you prefer for AFOSR YIP — Ni-superalloy
   variants (Pivot 1, lower technical risk) or RCCAs (Pivot 2, better PM
   alignment)?
2. For DOE ECRP, BES Synthesis & Processing Science vs. BES Mechanical Behavior
   of Materials vs. ASCR AI-for-Science — preference depends on how you want
   your scholarly identity framed for the next 5+ years.
3. Are you willing to drop the funded industry-partner model entirely for these
   single-PI vehicles? For AFOSR YIP this is settled: Q14 bars in-kind and
   no-cost collaborators too. For DOE ECRP it is still open.
4. ~~Should we draft the AFOSR YIP white paper for Sayir now?~~ Done; see
   [`afosr-yip-white-paper/`](afosr-yip-white-paper/). Still open: does Sayir
   accept a synthesis-by-design pitch on refractory alloys (see
   [`fit-check-email.md`](afosr-yip-white-paper/fit-check-email.md)), or should
   the FY27 white paper also go to §A.2.c?
